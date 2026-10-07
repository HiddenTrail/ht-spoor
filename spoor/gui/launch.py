"""Start the local GUI on a loopback-only socket (ROADMAP.md §2i).

`start_gui` refuses any non-loopback address before a socket is ever opened —
there is deliberately no CLI option to pass one (§2i: loopback-only,
non-configurable); the `host` parameter exists so the guard itself can be tested.
It binds the socket itself, so the real port is known (an ephemeral port by
default, avoiding clashes) before the app is built around it, generates a fresh
per-launch access token, and runs uvicorn in a background thread so the caller
can open a browser and then wait.
"""

from __future__ import annotations

import ipaddress
import secrets
import socket
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlencode

import uvicorn

from spoor.gui.app import create_app
from spoor.gui.jobs import JobManager, SubprocessRunner
from spoor.serving.store import MapStore

LOOPBACK = "127.0.0.1"
_STARTUP_TIMEOUT_SECONDS = 10.0


class GuiError(Exception):
    """The GUI could not be started (e.g. a non-loopback address was asked for)."""


def _is_loopback_literal(host: str) -> bool:
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


@dataclass
class RunningGui:
    """A GUI server running in a background thread."""

    url: str
    launch_url: str
    _server: uvicorn.Server
    _thread: threading.Thread
    _jobs: JobManager

    def wait(self, poll_seconds: float = 0.5) -> None:
        """Block until the server stops; Ctrl+C stops it cleanly."""
        try:
            while self._thread.is_alive():
                self._thread.join(poll_seconds)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        """Stop the server, force-stopping any job still running first.

        A job left running after the GUI closes would be an unsupervised browser
        nobody can see or stop, so closing the GUI ends them (§2i gui-2).
        """
        self._jobs.shutdown()
        self._server.should_exit = True
        self._thread.join(_STARTUP_TIMEOUT_SECONDS)


def start_gui(
    store: MapStore,
    *,
    host: str = LOOPBACK,
    port: int = 0,
    workdir: Path | None = None,
) -> RunningGui:
    """Start the GUI on `host:port` (loopback only) and return once it's serving.

    Jobs started from it run the real CLI in `workdir` (default: the current
    working directory), which is also where relative form paths are taken from
    and where the child's local cache lives.

    Raises GuiError for a non-loopback `host` (nothing is bound), or when the
    port can't be bound or the server doesn't come up.
    """
    if not _is_loopback_literal(host):
        raise GuiError(
            f"The Spoor GUI is local-only: it can only listen on this computer "
            f"(for example {LOOPBACK}), not on {host!r}."
        )
    family = socket.AF_INET6 if ":" in host else socket.AF_INET
    sock = socket.socket(family, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
    except OSError as exc:
        sock.close()
        raise GuiError(f"Could not listen on {host}:{port}: {exc}") from exc
    bound_port = sock.getsockname()[1]

    shown_host = f"[{host}]" if family == socket.AF_INET6 else host
    token = secrets.token_urlsafe(32)
    workdir = workdir or Path.cwd()
    app = create_app(
        store,
        token=token,
        port=bound_port,
        host=shown_host,
        jobs=JobManager(SubprocessRunner(workdir), workdir),
    )
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning"))
    thread = threading.Thread(
        target=server.run, kwargs={"sockets": [sock]}, daemon=True
    )
    thread.start()

    deadline = time.monotonic() + _STARTUP_TIMEOUT_SECONDS
    while not server.started:
        if not thread.is_alive() or time.monotonic() > deadline:
            server.should_exit = True
            sock.close()
            raise GuiError("The Spoor GUI server did not start.")
        time.sleep(0.05)

    url = f"http://{shown_host}:{bound_port}"
    return RunningGui(
        url=url,
        launch_url=f"{url}/launch?" + urlencode({"token": token}),
        _server=server,
        _thread=thread,
        _jobs=app.state.jobs,
    )
