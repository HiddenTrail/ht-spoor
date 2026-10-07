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
from datetime import datetime
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

from spoor.gui.commands import BUILDERS, RUN_FORMATS, FormError
from spoor.gui.jobs import Job, JobManager
from spoor.serving.store import MapStore

Render = Callable[..., HTMLResponse]

#: Form kind → (page title, template).
_FORMS = {
    "explore": ("Explore a site", "form_explore.html"),
    "run": ("Extract with a config", "form_run.html"),
    "apply-scaffold": ("Apply a filled-in scaffold", "form_apply_scaffold.html"),
}

#: Seconds between checks for new log lines while a job's log is being streamed.
_POLL_SECONDS = 0.2


def _default_folder(workdir: Path) -> Path:
    """A fresh per-form output folder, so one run never overwrites another's."""
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return workdir / "spoor-output" / stamp


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
        )

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
        values = _defaults(kind, jobs.workdir)
        # Pre-fill from the query (e.g. a map page's "Explore again" link).
        values.update({k: v for k, v in request.query_params.items() if k == "url"})
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
        return render("jobs.html", jobs=jobs.all(), status_text=_status_text)

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
