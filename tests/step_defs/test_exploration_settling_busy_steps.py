"""Step definitions for features/exploration_settling_busy.feature (§2e, 7g).

Two halves, mirroring 7f. The pure quiescence decision runs with no browser: a fake
clock advanced only by the injected `sleep`, a constant (quiet) mutation signal, and a
scripted `loading` predicate reporting a loading indicator on screen for a bounded time
(or forever). The live half stands up a loopback server per scenario whose entry page
shows a loading indicator (an indeterminate spinner, or an aria-busy region) and swaps
in the real content on a timer past the quiet window, with no request in flight, or
keeps a determinate progress bar and a hidden spinner forever. The real driver's
loading probe must hold the settle wait for the first two and not for the third.
"""

from __future__ import annotations

import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.discovery import discover_actions
from spoor.exploration.driver import PlaywrightDriver
from spoor.exploration.settling import wait_for_quiescence

scenarios("exploration_settling_busy.feature")

_POLL_INTERVAL_MS = 50.0

# Live timings: a quiet window short enough that DOM-quiet alone would fire while the
# spinner is up, a load delay comfortably past it, and a timeout well above the sum.
_QUIET_WINDOW_S = 0.3
_LOAD_DELAY_MS = 700
_SETTLE_TIMEOUT_S = 4.0

_CONTENT = "<h1>Ready</h1><button>Start job</button>"


@pytest.fixture
def context() -> dict[str, Any]:
    return {"now": 0.0}


@pytest.fixture(autouse=True)
def _teardown(context: dict[str, Any]) -> Any:
    yield
    driver = context.get("driver")
    if driver is not None:
        driver.close()
    server = context.get("server")
    if server is not None:
        server.shutdown()
        server.server_close()
        context["thread"].join(timeout=5)


# --- Pure decision (fake clock + scripted loading signal) ----------------


@given(
    parsers.parse("a quiet window of {quiet:d} ms and a settle timeout of {to:d} ms")
)
def windows(context: dict[str, Any], quiet: int, to: int) -> None:
    context["quiet_window"] = float(quiet)
    context["timeout"] = float(to)


@given(
    parsers.parse(
        "a page whose DOM is quiet but a loading indicator is showing "
        "until {until:d} ms"
    )
)
def loading_until(context: dict[str, Any], until: int) -> None:
    context["loading"] = lambda: context["now"] < float(until)


@given("a page whose DOM is quiet but a loading indicator never clears")
def loading_forever(context: dict[str, Any]) -> None:
    context["loading"] = lambda: True


@when("the explorer waits for the page to settle")
def wait_to_settle(context: dict[str, Any]) -> None:
    def clock() -> float:
        return float(context["now"])

    def sleep(dt: float) -> None:
        context["now"] += dt

    context["result"] = wait_for_quiescence(
        observe=lambda: 0,  # DOM quiet throughout
        clock=clock,
        sleep=sleep,
        quiet_window=context["quiet_window"],
        timeout=context["timeout"],
        poll_interval=_POLL_INTERVAL_MS,
        loading=context["loading"],
    )


@then("it reports the page settled")
def reports_settled(context: dict[str, Any]) -> None:
    assert context["result"].settled is True


@then("it reports the page did not settle")
def reports_unsettled(context: dict[str, Any]) -> None:
    assert context["result"].settled is False


@then("it did not wait the full timeout")
def under_timeout(context: dict[str, Any]) -> None:
    assert context["result"].elapsed < context["timeout"]


@then("the wait ended at the timeout")
def ended_at_timeout(context: dict[str, Any]) -> None:
    assert context["result"].elapsed >= context["timeout"]


@then(parsers.parse("the wait lasted at least {ms:d} ms"))
def lasted_at_least(context: dict[str, Any], ms: int) -> None:
    assert context["result"].elapsed >= float(ms), context["result"].elapsed


# --- Live half (a loopback server per page) ------------------------------


def _swap_in(delay_ms: int) -> str:
    """Replace the loading screen with the real content after `delay_ms`, client-side
    only (a timer, no request), exactly like the app that prompted 7g."""
    return (
        "<script>setTimeout(() => {"
        f"document.getElementById('app').innerHTML = {_CONTENT!r};"
        f"}}, {delay_ms});</script>"
    )


_PAGES = {
    "spinner": (
        "<html><body><div id='app'>"
        "<span role='progressbar' class='spinner'>…</span>"
        "</div>" + _swap_in(_LOAD_DELAY_MS) + "</body></html>"
    ),
    "busy": (
        "<html><body><div id='app' aria-busy='true'><p>Loading…</p></div>"
        "<script>setTimeout(() => {"
        "const app = document.getElementById('app');"
        f"app.innerHTML = {_CONTENT!r}; app.removeAttribute('aria-busy');"
        f"}}, {_LOAD_DELAY_MS});</script></body></html>"
    ),
    "durable": (
        "<html><body><div id='app'>" + _CONTENT + "</div>"
        "<span role='progressbar' aria-valuenow='0' aria-valuemin='0' "
        "aria-valuemax='100'>gauge</span>"
        "<span role='progressbar' style='display:none'>hidden spinner</span>"
        "</body></html>"
    ),
}


def _serve(context: dict[str, Any], page: str) -> None:
    payload = _PAGES[page].encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args: Any) -> None:  # silence per-request stderr log
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    driver = PlaywrightDriver(
        f"http://127.0.0.1:{server.server_address[1]}/",
        quiet_window=_QUIET_WINDOW_S,
        settle_timeout=_SETTLE_TIMEOUT_S,
    )
    driver.__enter__()
    context.update(server=server, thread=thread, driver=driver)


@given(
    "a live site whose entry page shows an indeterminate spinner before its content"
)
def live_spinner(context: dict[str, Any]) -> None:
    _serve(context, "spinner")


@given("a live site whose entry page marks its content aria-busy while it loads")
def live_busy(context: dict[str, Any]) -> None:
    _serve(context, "busy")


@given(
    "a live site whose settled page keeps a determinate progress bar "
    "and a hidden spinner"
)
def live_durable(context: dict[str, Any]) -> None:
    _serve(context, "durable")


@when("the explorer resets the browser")
def reset_browser(context: dict[str, Any]) -> None:
    started = time.monotonic()
    context["driver"].reset()
    context["reset_seconds"] = time.monotonic() - started


@then(parsers.parse('the discovered actions include the "{role}" named "{name}"'))
def discovered_includes(context: dict[str, Any], role: str, name: str) -> None:
    actions = discover_actions(context["driver"].ax_nodes())
    assert any(a.role == role and a.name == name for a in actions), actions


@then("the reset settled well before the settle timeout")
def settled_promptly(context: dict[str, Any]) -> None:
    assert context["reset_seconds"] < _SETTLE_TIMEOUT_S / 2, context["reset_seconds"]
