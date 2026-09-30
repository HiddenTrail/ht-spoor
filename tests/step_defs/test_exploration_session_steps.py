"""Step definitions for features/exploration_session.feature (ROADMAP.md §2e, §2h).

Runs the real `spoor explore` CLI against a small dynamic loopback server whose
pages are gated on a cookie and then a localStorage token, mirroring
`tests/step_defs/test_session_steps.py`'s auth server -- extended here to a
second gate a step deeper, so a multi-page crawl genuinely exercises reset-and-
replay's *repeated* resets, not just the first page load. The "it reports N
states discovered" / "it reports N transitions" steps are defined in
`test_exploration_browser_steps.py` and reused here (pytest-bdd resolves step
implementations across every collected step-definition module).
"""

from __future__ import annotations

import json
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from spoor.cli import app
from spoor.security import storage

scenarios("exploration_session.feature")

_COOKIE_NAME = "session"
_COOKIE_VALUE = "s3ss10n-c00k1e-value"
_TOKEN_NAME = "token"
_TOKEN_VALUE = "l0calStorage-t0ken-value"


class _GatedServer(ThreadingHTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _GatedHandler)

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _GatedHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        cookie_ok = f"{_COOKIE_NAME}={_COOKIE_VALUE}" in self.headers.get("Cookie", "")
        if self.path == "/":
            body = self._root(cookie_ok)
        elif self.path == "/deep.html" and cookie_ok:
            body = self._deep()
        elif self.path == "/deeper.html" and cookie_ok:
            body = "<html><body><p>The deepest page.</p></body></html>"
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"not found")
            return
        payload = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _root(self, cookie_ok: bool) -> str:
        # The link to the second page is server-rendered only when the request
        # carries the cookie -- unreachable by a fetch (or a browser context)
        # that hasn't replayed a supplied session's cookies.
        link = '<a href="/deep.html">Deeper</a>' if cookie_ok else ""
        return f"<html><body>{link}</body></html>"

    def _deep(self) -> str:
        # The link to the third page is injected by page JS only when the
        # browser context carries the matching localStorage token -- reachable
        # only if that token survived every reset since context creation, not
        # just the very first page load.
        return (
            "<html><body>"
            '<div id="more"></div>'
            "<script>"
            f"if (localStorage.getItem('{_TOKEN_NAME}') === '{_TOKEN_VALUE}') {{"
            "  var a = document.createElement('a');"
            "  a.href = '/deeper.html';"
            "  a.textContent = 'Deepest';"
            "  document.getElementById('more').appendChild(a);"
            "}"
            "</script>"
            "</body></html>"
        )

    def log_message(self, *args: Any) -> None:  # silence the per-request stderr log
        pass


@pytest.fixture
def context() -> Iterator[dict[str, Any]]:
    ctx: dict[str, Any] = {}
    yield ctx
    server = ctx.get("server")
    if server is not None:
        server.shutdown()
        server.server_close()
        ctx["thread"].join(timeout=5)


@pytest.fixture(autouse=True)
def temp_cache_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")


@given("an auth-gated fixture server whose deeper pages need a cookie then a token")
def gated_server(context: dict[str, Any]) -> None:
    server = _GatedServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    context["server"] = server
    context["thread"] = thread


@given("a session file carrying only the server's cookie")
def cookie_only_session(context: dict[str, Any], tmp_path: Path) -> None:
    path = tmp_path / "cookie-session.json"
    state = {
        "cookies": [
            {
                "name": _COOKIE_NAME,
                "value": _COOKIE_VALUE,
                "domain": "127.0.0.1",
                "path": "/",
                "sameSite": "Lax",
            }
        ],
        "origins": [],
    }
    path.write_text(json.dumps(state), encoding="utf-8")
    context["session_path"] = str(path)


@given("a session file carrying both the cookie and the localStorage token")
def full_session(context: dict[str, Any], tmp_path: Path) -> None:
    path = tmp_path / "full-session.json"
    state = {
        "cookies": [
            {
                "name": _COOKIE_NAME,
                "value": _COOKIE_VALUE,
                "domain": "127.0.0.1",
                "path": "/",
                "sameSite": "Lax",
            }
        ],
        "origins": [
            {
                "origin": context["server"].base,
                "localStorage": [{"name": _TOKEN_NAME, "value": _TOKEN_VALUE}],
            }
        ],
    }
    path.write_text(json.dumps(state), encoding="utf-8")
    context["session_path"] = str(path)


@when("I run spoor explore against it with no session")
def run_explore_anonymous(context: dict[str, Any]) -> None:
    result = CliRunner().invoke(
        app,
        [
            "explore",
            context["server"].base,
            "--max-states",
            "10",
            "--max-requests",
            "50",
        ],
    )
    assert result.exit_code == 0, result.output
    context["output"] = result.output


@then(parsers.parse("it reports {n:d} states discovered"))
def reports_states(context: dict[str, Any], n: int) -> None:
    assert f"states discovered: {n}" in context["output"], context["output"]


@then(parsers.parse("it reports {n:d} transitions"))
def reports_transitions(context: dict[str, Any], n: int) -> None:
    assert f"transitions:       {n}" in context["output"], context["output"]


@when("I run spoor explore against it with that session")
def run_explore_with_session(context: dict[str, Any]) -> None:
    result = CliRunner().invoke(
        app,
        [
            "explore",
            context["server"].base,
            "--max-states",
            "10",
            "--max-requests",
            "50",
            "--session",
            context["session_path"],
        ],
    )
    assert result.exit_code == 0, result.output
    context["output"] = result.output
