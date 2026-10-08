"""The GUI's Servers page: the map API server and MCP setup (ROADMAP.md §2i, gui-4).

The map API server is the real `spoor serve`, run as a supervised job (so it
also shows in Jobs, and closing the GUI stops it). There is no host field: it
stays on `serve`'s loopback default. At most one runs at a time, and it is shown
as running only once it answers its own `/healthz`.

`spoor serve-mcp` talks over stdio to the AI client that launches it, so the
GUI doesn't run it; it shows a ready-to-paste configuration instead. That
configuration sets `SPOOR_CACHE_DIR` to this GUI's cache as an absolute path,
because a client starts the server in a folder of its own choosing.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool
from starlette.responses import Response

from spoor.gui.commands import CommandSpec
from spoor.gui.jobs import Job, JobManager
from spoor.security import storage

Render = Callable[..., HTMLResponse]
HealthCheck = Callable[[int], bool]

_PORT_ERROR = "The port must be a whole number from 1 to 65535."


def check_health(port: int) -> bool:
    """Whether a map server on this computer's `port` answers its health check."""
    try:
        response = httpx.get(f"http://127.0.0.1:{port}/healthz", timeout=0.5)
    except httpx.HTTPError:
        return False
    return response.status_code == 200


def cache_dir(workdir: Path) -> Path:
    """This GUI's local cache as an absolute path (what its jobs read and write)."""
    return Path(os.path.abspath(workdir / storage.CACHE_ROOT))


def mcp_setup(workdir: Path) -> tuple[str, str]:
    """The MCP client configuration (JSON) and the equivalent `claude mcp add` line.

    Both run `python -m spoor.cli serve-mcp` with this Python, pointed at this
    GUI's cache through `SPOOR_CACHE_DIR`, so the server reads the same maps
    wherever the client starts it.
    """
    cache = str(cache_dir(workdir))
    server = {
        "command": sys.executable,
        "args": ["-m", "spoor.cli", "serve-mcp"],
        "env": {storage.CACHE_DIR_ENV: cache},
    }
    config = json.dumps({"mcpServers": {"spoor": server}}, indent=2)
    argv = [
        "claude", "mcp", "add", "spoor",
        "--env", f"{storage.CACHE_DIR_ENV}={cache}",
        "--", sys.executable, "-m", "spoor.cli", "serve-mcp",
    ]
    if sys.platform == "win32":
        line = subprocess.list2cmdline(argv)
    else:
        line = shlex.join(argv)
    return config, line


class MapServer:
    """The one managed `spoor serve` job, if any, and the port it was given."""

    def __init__(self) -> None:
        self.job: Job | None = None
        self.port: int | None = None

    @property
    def running(self) -> bool:
        return self.job is not None and self.job.running


def _port(value: str) -> int | None:
    try:
        port = int(value.strip())
    except ValueError:
        return None
    return port if 1 <= port <= 65535 else None


def add_server_routes(
    app: FastAPI, *, jobs: JobManager, render: Render, health: HealthCheck
) -> None:
    """Register the gui-4 page and endpoints on `app`."""
    server = MapServer()
    setup = mcp_setup(jobs.workdir)

    def page(
        *, status_code: int = 200, error: str | None = None, port: str = ""
    ) -> HTMLResponse:
        state = "none"
        lines: list[str] = []
        if server.job is not None:
            _, lines = server.job.lines_from(0)
            if server.job.running:
                assert server.port is not None
                state = "running" if health(server.port) else "starting"
            elif server.job.status == "failed":
                state = "failed"
            else:
                state = "stopped"
        return render(
            "servers.html",
            status_code=status_code,
            state=state,
            job=server.job,
            url=f"http://127.0.0.1:{server.port}" if server.port else None,
            log=lines[-40:],
            error=error,
            port=port or str(server.port or 8000),
            mcp_json=setup[0],
            mcp_command=setup[1],
        )

    @app.get("/servers", response_class=HTMLResponse)
    async def servers() -> HTMLResponse:
        # The health check is a blocking request; keep it off the event loop.
        return await run_in_threadpool(page)

    @app.post("/servers/start", response_model=None)
    async def start(request: Request) -> Response:
        form = await request.form()
        raw_port = str(form.get("port", ""))
        recheck = str(form.get("recheck", "")) not in ("", "off", "false")
        if server.running:
            return await run_in_threadpool(
                lambda: page(
                    status_code=400,
                    error="A map server is already running. Stop it first to start "
                    "another.",
                    port=raw_port,
                )
            )
        port = _port(raw_port)
        if port is None:
            return await run_in_threadpool(
                lambda: page(status_code=400, error=_PORT_ERROR, port=raw_port)
            )
        args = ["serve", "--port", str(port)] + (["--recheck"] if recheck else [])
        server.job = jobs.start(CommandSpec("serve", args))
        server.port = port
        return RedirectResponse("/servers", status_code=303)

    @app.post("/servers/stop")
    def stop() -> RedirectResponse:
        job = server.job
        if job is not None and job.running:
            jobs.kill(job)
            # Give it a moment to exit, so the page doesn't still show it running.
            deadline = time.monotonic() + 5.0
            while job.running and time.monotonic() < deadline:
                time.sleep(0.02)
        return RedirectResponse("/servers", status_code=303)
