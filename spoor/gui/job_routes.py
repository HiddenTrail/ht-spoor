"""The GUI's run-job pages and endpoints (ROADMAP.md §2i, slice gui-2).

Forms for `explore`, `run` and `apply-scaffold`; a command preview; the job
pages with a live log over Server-Sent Events; Stop / Force stop; "open folder";
and the generated wiki served from the job's own output folder.

All of it sits behind the app's guard (token, Host, and Origin on every POST), so
another site can neither start a job nor stop one. A job only ever runs the real
CLI (`spoor.gui.jobs`), and only the output paths a job recorded can be opened or
served: no endpoint takes a filesystem path from the request.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    StreamingResponse,
)
from starlette.responses import Response

from spoor.gui import configs
from spoor.gui.commands import (
    BUILDERS,
    OUTPUT_ROOT,
    RUN_FORMATS,
    FormError,
    fresh_output_form,
)
from spoor.gui.jobs import Job, JobManager
from spoor.security.session_store import SessionStore
from spoor.serving.store import MapStore

Render = Callable[..., HTMLResponse]

#: Form kind → (page title, template).
_FORMS = {
    "explore": ("Explore a site", "form_explore.html"),
    "run": ("Extract with a config", "form_run.html"),
    "apply-scaffold": ("Apply a filled-in scaffold", "form_apply_scaffold.html"),
}

#: The file a `--scaffold` folder holds (what apply-scaffold reads).
SCAFFOLD_FILE = "interactive.yaml"

#: Seconds between checks for new log lines while a job's log is being streamed.
_POLL_SECONDS = 0.2


def _fresh_stamp(workdir: Path) -> str:
    """A date-and-time folder name not yet used under spoor-output/.

    Two runs started in the same second (say, a rerun right after its job)
    would otherwise share a folder, so a counter is added when needed.
    """
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    root = workdir / OUTPUT_ROOT
    candidate, n = stamp, 2
    while (root / candidate).exists() or candidate in _issued_stamps:
        candidate, n = f"{stamp}-{n}", n + 1
    _issued_stamps.add(candidate)
    return candidate


#: Stamps handed out in this GUI session (a form can be opened before any of its
#: folders exist on disk, so the disk alone can't tell which are taken).
_issued_stamps: set[str] = set()


def _default_folder(workdir: Path) -> Path:
    """A fresh per-form output folder, so one run never overwrites another's."""
    return workdir / OUTPUT_ROOT / _fresh_stamp(workdir)


def when(moment: datetime | None) -> str:
    """A moment as a local date and time, e.g. \"2026-10-08 14:32:05\"."""
    return moment.astimezone().strftime("%Y-%m-%d %H:%M:%S") if moment else ""


def duration(job: Job) -> str:
    """How long a job ran (or has been running), e.g. \"1 min 05 s\"."""
    end = job.finished_at or datetime.now(UTC)
    seconds = max(0, int((end - job.started_at).total_seconds()))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours} h {minutes:02d} min"
    if minutes:
        return f"{minutes} min {secs:02d} s"
    return f"{secs} s"


def _defaults(kind: str, workdir: Path) -> dict[str, str]:
    base = _default_folder(workdir)
    if kind == "explore":
        return {
            "wiki_dir": str(base / "wiki"),
            "gen_tests_dir": str(base / "tests"),
            "scaffold_dir": str(base / "scaffold"),
        }
    if kind == "run":
        return {
            "output": str(base / "output.json"),
            "healing_report_path": str(base / "healing-report.md"),
        }
    return {"wiki_dir": ""}


def _status_text(job: Job) -> str:
    """One plain sentence about how the job ended (or that it's still going)."""
    if job.running:
        if job.stop_requested:
            return "Stopping: finishing the current action, then saving."
        return "Running."
    if job.status == "succeeded":
        return "Finished."
    if job.status == "failed":
        return "The log below says why."
    if job.killed:
        if job.spec.kind == "serve":
            # A read-only server has nothing to save.
            return "Stopped."
        return "Force-stopped. Nothing more was saved from this run."
    return "Stopped at your request. What was mapped so far was saved."


def add_job_routes(
    app: FastAPI,
    *,
    jobs: JobManager,
    store: MapStore,
    render: Render,
    opener: Callable[[Path], None],
) -> None:
    """Register the gui-2 pages and endpoints on `app`."""

    def form_page(
        kind: str, values: dict[str, str], error: str | None, status_code: int = 200
    ) -> HTMLResponse:
        title, template = _FORMS[kind]
        return render(
            template,
            status_code=status_code,
            kind=kind,
            title=title,
            v=values,
            error=error,
            formats=RUN_FORMATS,
            mapped_urls=[u for d in store.domains() for u, _ in store.urls(d)],
            # Names only: SessionStore.list() can't return a login's contents.
            saved_logins=SessionStore().list(),
        )

    def actions(job: Job) -> list[dict[str, str]]:
        """The job's \"…\" menu: label, link and method of each follow-up."""
        kind = job.spec.kind
        if kind not in _FORMS or not job.spec.form:
            return []
        items = [
            {"label": "Rerun", "href": f"/jobs/{job.id}/rerun", "method": "post"},
            {
                "label": "Rerun with changes",
                "href": f"/new/{kind}?" + urlencode({"from": job.id}),
                "method": "get",
            },
        ]
        scaffold = job.spec.outputs.get("scaffold")
        if kind == "explore" and scaffold and (scaffold / SCAFFOLD_FILE).is_file():
            items.append(
                {
                    "label": "Apply scaffold",
                    "href": "/new/apply-scaffold?" + urlencode({"from": job.id}),
                    "method": "get",
                }
            )
        if kind == "run":
            relative = _config_in_workdir(job)
            if relative is not None:
                items.append(
                    {
                        "label": "Edit config",
                        "href": "/configs/edit?" + urlencode({"path": relative}),
                        "method": "get",
                    }
                )
        if job.spec.map_url and store.get(job.spec.map_url):
            items.append(
                {
                    "label": "View map",
                    "href": "/map?" + urlencode({"url": job.spec.map_url}),
                    "method": "get",
                }
            )
        return items

    def _config_in_workdir(job: Job) -> str | None:
        """The run's config relative to the working folder, if the editor allows it."""
        config = job.spec.form.get("config", "").strip()
        if not config:
            return None
        root = jobs.workdir.resolve()
        target = (jobs.workdir / config).resolve()
        if not target.is_relative_to(root):
            return None
        relative = target.relative_to(root).as_posix()
        path = configs.resolve(jobs.workdir, relative)
        return relative if path is not None and path.is_file() else None

    def prefill_from(kind: str, job: Job) -> dict[str, str]:
        """Form values for `kind`, started from an earlier job."""
        stamp = _fresh_stamp(jobs.workdir)
        if kind == job.spec.kind:
            return fresh_output_form(kind, job.spec.form, jobs.workdir, stamp)
        if kind == "apply-scaffold" and job.spec.kind == "explore":
            scaffold = job.spec.outputs.get("scaffold")
            if scaffold is None:
                raise HTTPException(status_code=404)
            source = job.spec.form
            values = {
                "url": source.get("url", ""),
                "scaffold": str(scaffold / SCAFFOLD_FILE),
                "sandbox": source.get("sandbox", ""),
                "session": source.get("session", ""),
            }
            wiki = job.spec.outputs.get("wiki")
            if wiki is not None:
                values.update(wiki="on", wiki_dir=str(wiki))
            return values
        raise HTTPException(status_code=404)

    def known_kind(kind: str) -> None:
        if kind not in _FORMS:
            raise HTTPException(status_code=404)

    def get_job(job_id: str) -> Job:
        job = jobs.get(job_id)
        if job is None:
            raise HTTPException(status_code=404)
        return job

    async def form_values(request: Request) -> dict[str, str]:
        form = await request.form()
        return {k: v for k, v in form.items() if isinstance(v, str)}

    @app.get("/new/{kind}", response_class=HTMLResponse)
    def new_job_form(kind: str, request: Request) -> HTMLResponse:
        known_kind(kind)
        source = request.query_params.get("from")
        if source is not None:
            # "Rerun with changes" / "Apply scaffold" from an earlier job.
            return form_page(kind, prefill_from(kind, get_job(source)), None)
        values = _defaults(kind, jobs.workdir)
        # Pre-fill from the query: a map page's "Explore this page again" link
        # (url), or a config editor's "Run this config" link (config).
        values.update(
            {k: v for k, v in request.query_params.items() if k in ("url", "config")}
        )
        return form_page(kind, values, None)

    @app.post("/new/{kind}")
    async def start_job(kind: str, request: Request) -> Response:
        known_kind(kind)
        values = await form_values(request)
        try:
            spec = BUILDERS[kind](values, jobs.workdir)
        except FormError as exc:
            return form_page(kind, values, str(exc), status_code=400)
        job = jobs.start(spec)
        return RedirectResponse(f"/jobs/{job.id}", status_code=303)

    @app.post("/preview/{kind}")
    async def preview(kind: str, request: Request) -> PlainTextResponse:
        known_kind(kind)
        try:
            spec = BUILDERS[kind](await form_values(request), jobs.workdir)
        except FormError as exc:
            return PlainTextResponse(str(exc), status_code=400)
        return PlainTextResponse(spec.command_line)

    @app.get("/jobs", response_class=HTMLResponse)
    def job_list() -> HTMLResponse:
        return render(
            "jobs.html",
            jobs=jobs.all(),
            status_text=_status_text,
            actions=actions,
            when=when,
            duration=duration,
        )

    @app.post("/jobs/{job_id}/rerun")
    def rerun(job_id: str) -> RedirectResponse:
        job = get_job(job_id)
        kind = job.spec.kind
        if kind not in BUILDERS or not job.spec.form:
            raise HTTPException(status_code=404)
        form = fresh_output_form(
            kind, job.spec.form, jobs.workdir, _fresh_stamp(jobs.workdir)
        )
        try:
            spec = BUILDERS[kind](form, jobs.workdir)
        except FormError as exc:  # pragma: no cover - it was valid the first time
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return RedirectResponse(f"/jobs/{jobs.start(spec).id}", status_code=303)

    @app.get("/jobs/{job_id}", response_class=HTMLResponse)
    def job_page(job_id: str) -> HTMLResponse:
        job = get_job(job_id)
        next_line, lines = job.lines_from(0)
        outputs: list[dict[str, Any]] = []
        for label, path in job.spec.outputs.items():
            index = path / "index.html"
            outputs.append(
                {
                    "label": label,
                    "path": str(path),
                    "exists": path.exists(),
                    "browse": (
                        f"/jobs/{job.id}/files/{label}/index.html"
                        if label == "wiki" and index.is_file()
                        else None
                    ),
                }
            )
        map_href = None
        if not job.running and job.spec.map_url and store.get(job.spec.map_url):
            map_href = "/map?" + urlencode({"url": job.spec.map_url})
        return render(
            "job.html",
            job=job,
            lines=lines,
            next_line=next_line,
            outputs=outputs,
            map_href=map_href,
            status_text=_status_text(job),
            actions=actions(job),
            when=when,
            duration=duration,
        )

    @app.get("/jobs/{job_id}/events")
    async def job_events(
        job_id: str, start: int = Query(0, alias="from")
    ) -> StreamingResponse:
        job = get_job(job_id)

        async def stream() -> AsyncIterator[str]:
            position = start
            while True:
                # Read the status before the lines: a job that has finished has
                # printed everything, so no line can be missed after "done".
                finished = not job.running
                position, lines = job.lines_from(position)
                for offset, line in enumerate(lines, start=position - len(lines)):
                    yield f"id: {offset}\ndata: {line}\n\n"
                if finished:
                    yield f"event: done\ndata: {job.status}\n\n"
                    return
                await asyncio.sleep(_POLL_SECONDS)

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-store"},
        )

    @app.post("/jobs/{job_id}/stop")
    def stop_job(job_id: str) -> RedirectResponse:
        jobs.stop(get_job(job_id))
        return RedirectResponse(f"/jobs/{job_id}", status_code=303)

    @app.post("/jobs/{job_id}/kill")
    def kill_job(job_id: str) -> RedirectResponse:
        jobs.kill(get_job(job_id))
        return RedirectResponse(f"/jobs/{job_id}", status_code=303)

    @app.post("/jobs/{job_id}/open/{label}")
    def open_output(job_id: str, label: str) -> RedirectResponse:
        job = get_job(job_id)
        path = job.spec.outputs.get(label)
        if path is None or not path.exists():
            raise HTTPException(status_code=404)
        opener(path)
        return RedirectResponse(f"/jobs/{job_id}", status_code=303)

    @app.get("/jobs/{job_id}/files/{label}/{file_path:path}")
    def job_file(job_id: str, label: str, file_path: str) -> FileResponse:
        job = get_job(job_id)
        root = job.spec.outputs.get(label)
        if root is None or not root.is_dir():
            raise HTTPException(status_code=404)
        root = root.resolve()
        target = (root / file_path).resolve()
        # Only files inside this job's own output folder, never a path that
        # climbs out of it.
        if not target.is_relative_to(root) or not target.is_file():
            raise HTTPException(status_code=404)
        return FileResponse(target)
