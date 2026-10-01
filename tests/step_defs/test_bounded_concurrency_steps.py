"""Step definitions for features/bounded_concurrency.feature (ROADMAP.md §2d, #174).

Driven against a real loopback server (not a mock transport) because the
point is genuine OS-thread concurrency and real elapsed time — a fake `sleep`
can prove dispatch *logic* (covered separately in
`tests/test_politeness_concurrency.py`) but not that two fetches actually
overlapped in wall-clock time. Each "slow" page sleeps a short, real
`ARTIFICIAL_DELAY` before responding, long enough that two concurrent
requests measurably overlap but short enough the suite stays fast.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.core import extract
from spoor.core.config import load_config

scenarios("bounded_concurrency.feature")

ARTIFICIAL_DELAY = 0.15
_INDEX_PATH = "/index.html"
_ITEM_COUNT = 4


def _index_body() -> bytes:
    links = "".join(
        f'<a href="/item-{n}.html">{n}</a>' for n in range(1, _ITEM_COUNT + 1)
    )
    return f"<html><body><h1>Index</h1>{links}</body></html>".encode()


def _item_body(n: int) -> bytes:
    return f"<html><body><h1>Item {n}</h1></body></html>".encode()


class _SlowServer(ThreadingHTTPServer):
    """Serves an index page linking to several slow "item" pages.

    Tracks, for the slow pages only: how many requests are concurrently in
    flight (`peak_active`, updated under a lock as each request starts/ends)
    and the real start timestamp of each one (`start_times`), so a scenario
    can assert on genuine overlap and genuine dispatch spacing.
    """

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _SlowHandler)
        self.lock = threading.Lock()
        self.active = 0
        self.peak_active = 0
        self.start_times: list[float] = []

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _SlowHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        server: _SlowServer = self.server  # type: ignore[assignment]
        if self.path == _INDEX_PATH:
            self._respond(_index_body())
            return
        if self.path.startswith("/item-") and self.path.endswith(".html"):
            n = int(self.path.removeprefix("/item-").removesuffix(".html"))
            with server.lock:
                server.active += 1
                server.peak_active = max(server.peak_active, server.active)
                server.start_times.append(time.monotonic())
            try:
                time.sleep(ARTIFICIAL_DELAY)
                self._respond(_item_body(n))
            finally:
                with server.lock:
                    server.active -= 1
            return
        self.send_response(404)
        self.end_headers()

    def _respond(self, body: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args: Any) -> None:  # silence per-request stderr log
        pass


@pytest.fixture
def context() -> dict[str, Any]:
    return {}


@pytest.fixture
def server() -> Iterator[_SlowServer]:
    srv = _SlowServer()
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()
    thread.join(timeout=5)


# --- Given -------------------------------------------------------------


@given("a config with a \"title\" field")
def base_config(context: dict[str, Any]) -> None:
    context["fields_yaml"] = 'fields:\n  title: { selector: "h1" }\n'


@given("a slow fixture server that records how many requests are in flight at once")
@given("a slow fixture server that records when each request started")
def slow_server(context: dict[str, Any], server: _SlowServer) -> None:
    context["server"] = server


def _politeness_yaml(cap: int | None, delay: float | None) -> str:
    if cap is None and delay is None:
        return ""
    lines = ["politeness:"]
    if cap is not None:
        lines.append(f"  max_concurrent_per_domain: {cap}")
    if delay is not None:
        lines.append(f"  delay: {delay}")
    return "\n".join(lines) + "\n"


def _assert_fixture_page_count(count: int) -> None:
    # The fixture server always serves exactly `_ITEM_COUNT` item pages; the
    # Gherkin text's {count:d} is a readability device, not a real parameter
    # -- this guards against a scenario silently drifting out of sync with
    # what the fixture actually serves if either one is ever edited alone.
    assert count == _ITEM_COUNT


def _config_text(
    context: dict[str, Any], *, cap: int | None, delay: float | None
) -> str:
    server: _SlowServer = context["server"]
    return (
        f"target: {server.base}{_INDEX_PATH}\n"
        f"{context['fields_yaml']}"
        "crawl:\n"
        '  include: ["/item-*"]\n'
        f"{_politeness_yaml(cap, delay)}"
    )


@given(
    parsers.parse(
        "a config crawling {count:d} pages on that server with no concurrency cap set"
    )
)
def config_no_cap(context: dict[str, Any], count: int) -> None:
    _assert_fixture_page_count(count)
    context["config_text"] = _config_text(context, cap=None, delay=None)


@given(
    parsers.parse(
        "a config crawling {count:d} pages on that server with a concurrency "
        "cap of {cap:d}"
    )
)
def config_with_cap(context: dict[str, Any], count: int, cap: int) -> None:
    _assert_fixture_page_count(count)
    context["config_text"] = _config_text(context, cap=cap, delay=None)


@given(
    parsers.parse(
        "a config crawling {count:d} pages on that server with a concurrency cap of "
        "{cap:d} and a crawl-delay of {delay:g} seconds"
    )
)
def config_with_cap_and_delay(
    context: dict[str, Any], count: int, cap: int, delay: float
) -> None:
    _assert_fixture_page_count(count)
    context["config_text"] = _config_text(context, cap=cap, delay=delay)


# --- When ----------------------------------------------------------------


@when("I run the crawl")
def run_crawl(context: dict[str, Any]) -> None:
    cfg = load_config(context["config_text"])
    context["result"] = extract.run_report(cfg, tiers=(extract.Tier1Resolver(),))


@when("I run the crawl in the browser tier")
def run_crawl_browser(context: dict[str, Any]) -> None:
    cfg = load_config(context["config_text"])
    context["result"] = extract.run_report(cfg, tiers=(extract.Tier2Resolver(),))


# --- Then ------------------------------------------------------------------


@then(
    parsers.parse("at most {n:d} request to that server was ever in flight at once")
)
@then(
    parsers.parse(
        "at most {n:d} requests to that server were ever in flight at once"
    )
)
def peak_at_most(context: dict[str, Any], n: int) -> None:
    assert context["server"].peak_active <= n


@then(
    parsers.parse(
        "more than {n:d} request to that server was in flight at some point"
    )
)
def peak_more_than(context: dict[str, Any], n: int) -> None:
    assert context["server"].peak_active > n


@then(
    parsers.parse(
        "consecutive request start times on that server are spaced at least "
        "{delay:g} seconds apart"
    )
)
def dispatches_spaced(context: dict[str, Any], delay: float) -> None:
    starts = sorted(context["server"].start_times)
    assert len(starts) == _ITEM_COUNT
    # Intentionally unequal-length pairing (starts vs. starts[1:]) to compute
    # consecutive gaps -- not a zip() misuse, so no strict=True here.
    gaps = [b - a for a, b in zip(starts, starts[1:], strict=False)]
    # A small tolerance for scheduling jitter -- real threads, real clock.
    tolerance = 0.03
    assert all(gap >= delay - tolerance for gap in gaps), gaps
