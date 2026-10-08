"""The GUI's saved-login and config-file pages (ROADMAP.md §2i, slice gui-3).

Saved logins: listed straight from the session store, which can only return
metadata (label, site, dates), never a cookie. Adding and removing run the real
`spoor session add` / `spoor session remove`. An uploaded login file is written
to a private temporary folder for the command and deleted as soon as it ends.

Config files: listed, opened, checked and saved through `configs.py`, which
confines them to `.yaml`/`.yml` files inside the working folder. A request
naming any other path gets a 404, never a file.

Every POST here sits behind the app's guard (token, Host, Origin), so another
site can neither add a login nor overwrite a config.
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import UploadFile

from spoor.gui import configs
from spoor.gui.commands import CommandSpec
from spoor.gui.jobs import Job, JobManager
from spoor.security.session_store import SessionStore

Render = Callable[..., HTMLResponse]

#: Largest login file accepted for upload.
MAX_LOGIN_BYTES = 5_000_000


def _outcome(job: Job, finished: bool) -> tuple[bool, list[str]]:
    """Whether a short command succeeded, and the lines to show about it."""
    _, lines = job.lines_from(0)
    shown = [line for line in lines if line.strip()]
    if not finished:
        return False, [
            "The command took too long and was stopped. Check the list below to "
            "see whether the login was saved before it stopped.",
            *shown,
        ]
    if job.status != "succeeded":
        return False, shown or [f"The command failed (exit code {job.exit_code})."]
    return True, shown[-1:] or ["Done."]


def add_manage_routes(
    app: FastAPI, *, jobs: JobManager, render: Render
) -> None:
    """Register the gui-3 pages and endpoints on `app`."""

    def logins_page(
        status_code: int = 200,
        *,
        ok: bool | None = None,
        messages: list[str] | None = None,
        values: dict[str, str] | None = None,
    ) -> HTMLResponse:
        return render(
            "logins.html",
            status_code=status_code,
            logins=SessionStore().list(),
            ok=ok,
            messages=messages or [],
            v=values or {},
        )

    @app.get("/logins", response_class=HTMLResponse)
    def logins() -> HTMLResponse:
        return logins_page()

    @app.post("/logins/add", response_class=HTMLResponse)
    async def add_login(request: Request) -> HTMLResponse:
        form = await request.form()
        label = str(form.get("label", "")).strip()
        site = str(form.get("site", "")).strip()
        upload = form.get("file")
        values = {"label": label, "site": site}

        def refuse(message: str) -> HTMLResponse:
            return logins_page(400, ok=False, messages=[message], values=values)

        if not label:
            return refuse("Give the login a name.")
        if not site:
            return refuse("Enter the site this login is for.")
        if not isinstance(upload, UploadFile) or not upload.filename:
            return refuse("Choose the login file to upload.")
        data = await upload.read(MAX_LOGIN_BYTES + 1)
        if len(data) > MAX_LOGIN_BYTES:
            return refuse("That file is larger than 5 MB; it can't be a login file.")

        # A private folder of its own, removed with the file as soon as the
        # command ends — however it ends.
        folder = Path(tempfile.mkdtemp(prefix="spoor-login-"))
        try:
            path = folder / "storage-state.json"
            path.write_bytes(data)
            # "--" ends the options, so a site or name starting with "-" is
            # still read as a value, never as an option.
            spec = CommandSpec(
                "session add",
                ["session", "add", "--label", label, "--", str(path), site],
            )
            job, finished = await run_in_threadpool(jobs.run_and_wait, spec)
        finally:
            shutil.rmtree(folder, ignore_errors=True)
        ok, messages = _outcome(job, finished)
        return logins_page(ok=ok, messages=messages, values={} if ok else values)

    @app.post("/logins/remove", response_class=HTMLResponse)
    async def remove_login(request: Request) -> HTMLResponse:
        form = await request.form()
        site = str(form.get("site", "")).strip()
        label = str(form.get("label", "")).strip()
        if not site or not label:
            return logins_page(400, ok=False, messages=["Choose a login to remove."])
        spec = CommandSpec("session remove", ["session", "remove", "--", site, label])
        job, finished = await run_in_threadpool(jobs.run_and_wait, spec)
        ok, messages = _outcome(job, finished)
        return logins_page(ok=ok, messages=messages)

    # --- Config files -------------------------------------------------------------

    def config_path(relative: str) -> Path:
        path = configs.resolve(jobs.workdir, relative)
        if path is None:
            raise HTTPException(status_code=404)
        return path

    def editor(
        relative: str,
        text: str,
        *,
        problems: list[str] | None,
        saved: bool = False,
        status_code: int = 200,
    ) -> HTMLResponse:
        context: dict[str, Any] = {
            "path": relative,
            "text": text,
            "problems": problems,
            "saved": saved,
            "run_href": "/new/run?" + urlencode({"config": relative}),
        }
        return render("config_edit.html", status_code=status_code, **context)

    @app.get("/configs", response_class=HTMLResponse)
    def config_list() -> HTMLResponse:
        return config_list_page()

    def config_list_page(
        error: str | None = None, new_path: str = "", status_code: int = 200
    ) -> HTMLResponse:
        return render(
            "configs.html",
            status_code=status_code,
            configs=configs.find(jobs.workdir),
            workdir=str(jobs.workdir),
            error=error,
            new_path=new_path,
        )

    @app.get("/configs/edit", response_class=HTMLResponse)
    def edit_config(path: str = Query(...)) -> HTMLResponse:
        target = config_path(path)
        if not target.is_file():
            raise HTTPException(status_code=404)
        try:
            text = configs.read(target)
        except ValueError as exc:
            # No editor at all: an empty one with a Save button would let one
            # click overwrite the file with nothing.
            return config_list_page(f"{path}: {exc}", status_code=400)
        return editor(path, text, problems=None)

    async def posted(request: Request) -> tuple[str, Path, str]:
        form = await request.form()
        relative = str(form.get("path", ""))
        text = str(form.get("text", ""))
        target = config_path(relative)
        if target.exists() and not target.is_file():
            raise HTTPException(status_code=404)
        if len(text.encode("utf-8")) > configs.MAX_BYTES:
            raise HTTPException(status_code=413)
        return relative, target, text

    @app.post("/configs/check", response_class=HTMLResponse)
    async def check_config(request: Request) -> HTMLResponse:
        relative, _, text = await posted(request)
        return editor(relative, text, problems=configs.check(text))

    @app.post("/configs/save", response_class=HTMLResponse)
    async def save_config(request: Request) -> HTMLResponse:
        relative, target, text = await posted(request)
        configs.write(target, text)
        return editor(relative, text, problems=configs.check(text), saved=True)

    @app.post("/configs/new", response_model=None)
    async def new_config(request: Request) -> RedirectResponse | HTMLResponse:
        form = await request.form()
        relative = str(form.get("path", "")).strip()

        def refuse(message: str) -> HTMLResponse:
            return config_list_page(message, new_path=relative, status_code=400)

        target = configs.resolve(jobs.workdir, relative)
        if target is None:
            return refuse(
                "Choose a .yaml or .yml file name inside the working folder "
                "(not in a hidden or output folder)."
            )
        if target.exists():
            return refuse(f"{relative} already exists. Open it from the list instead.")
        configs.write(target, configs.STARTER)
        return RedirectResponse(
            "/configs/edit?" + urlencode({"path": relative}), status_code=303
        )
