"""Step definitions for features/resumable_crawl_state.feature (ROADMAP.md §2d, #175).

Driven against a real loopback server (not a mock transport) so a genuine
multi-page `crawl:` frontier is exercised across two real `run_report` calls,
the same "run it twice" pattern `test_change_detection_steps.py` uses.
`storage.CACHE_ROOT` is monkeypatched to a per-scenario temp directory so the
persisted frontier file never touches the real `.spoor-cache/`, and
`extract._MAX_PAGES` is monkeypatched down to simulate a run stopped partway
through a crawl without needing 1000 real pages to do it.

Which URLs a run actually dispatched is tracked via a `RunHooks.on_request`
callback, not the server's raw request log: `run_report` also probes the
target's origin for a published API spec alongside the extraction fetch
(§2b) — including a fallback scan that independently re-fetches the landing
page itself — so the raw server log is polluted with requests the crawl
loop's own frontier never made. The hook fires only for a URL the resolver's
frontier itself dispatches, immune to that noise.
"""

from __future__ import annotations

import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.core import extract
from spoor.core.config import load_config
from spoor.operational import crawl_state
from spoor.operational.hooks import RunHooks
from spoor.security import storage

scenarios("resumable_crawl_state.feature")

_INDEX_PATH = "/index.html"
_ITEM_COUNT = 4


def _index_body() -> bytes:
    links = "".join(
        f'<a href="/item-{n}.html">{n}</a>' for n in range(1, _ITEM_COUNT + 1)
    )
    return f"<html><body><h1>Index</h1>{links}</body></html>".encode()


def _item_body(n: int) -> bytes:
    return f"<html><body><h1>Item {n}</h1></body></html>".encode()


class _IndexServer(ThreadingHTTPServer):
    """An index page linking to several item pages."""

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _IndexHandler)

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _IndexHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        if self.path == _INDEX_PATH:
            self._respond(_index_body())
            return
        if self.path.startswith("/item-") and self.path.endswith(".html"):
            n = int(self.path.removeprefix("/item-").removesuffix(".html"))
            self._respond(_item_body(n))
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
def context(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> dict[str, Any]:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / "cache")
    return {"monkeypatch": monkeypatch}


@pytest.fixture
def server() -> Iterator[_IndexServer]:
    srv = _IndexServer()
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()
    thread.join(timeout=5)


# --- Given -------------------------------------------------------------


@given("a fixture server with an index page linking to 4 item pages")
def index_server(context: dict[str, Any], server: _IndexServer) -> None:
    context["server"] = server


def _config_text(context: dict[str, Any], *, resume: bool) -> str:
    server: _IndexServer = context["server"]
    text = (
        f"target: {server.base}{_INDEX_PATH}\n"
        'fields:\n  title: { selector: "h1" }\n'
        "crawl:\n"
        '  include: ["/item-*"]\n'
    )
    if resume:
        text += "resume: true\n"
    return text


@given(parsers.parse("resume is enabled and the per-run page cap is {cap:d}"))
def resume_with_cap(context: dict[str, Any], cap: int) -> None:
    context["monkeypatch"].setattr(extract, "_MAX_PAGES", cap)
    context["config_text"] = _config_text(context, resume=True)


@given("resume is enabled")
def resume_enabled(context: dict[str, Any]) -> None:
    context["config_text"] = _config_text(context, resume=True)


@given("resume is not configured")
def resume_not_configured(context: dict[str, Any]) -> None:
    context["config_text"] = _config_text(context, resume=False)


def _run(context: dict[str, Any], tier: str = "static") -> list[str]:
    """Run once, returning the paths the crawl's own frontier dispatched."""
    dispatched: list[str] = []

    def on_request(url: str) -> None:
        dispatched.append(urlsplit(url).path)

    cfg = load_config(context["config_text"])
    tiers = (
        (extract.Tier1Resolver(),) if tier == "static" else (extract.Tier2Resolver(),)
    )
    context["result"] = extract.run_report(
        cfg, tiers=tiers, hooks=RunHooks(on_request=on_request)
    )
    context["last_run_requests"] = dispatched
    return dispatched


@given("a first run already hit that cap")
def first_run_hit_cap(context: dict[str, Any]) -> None:
    context["first_run_requests"] = _run(context)


@given("a first browser run already hit that cap")
def first_browser_run_hit_cap(context: dict[str, Any]) -> None:
    context["first_run_requests"] = _run(context, tier="browser")


@given("a first run already completed the whole crawl")
def first_run_completed(context: dict[str, Any]) -> None:
    # No cap restriction here -- the default _MAX_PAGES is far larger than the
    # 5 pages (index + 4 items) this fixture ever has to offer.
    context["monkeypatch"].setattr(extract, "_MAX_PAGES", 1000)
    _run(context)


# --- When ----------------------------------------------------------------


@when("I run the crawl")
def run_once(context: dict[str, Any]) -> None:
    _run(context)


@when("I resume the crawl with no page cap")
def resume_no_cap(context: dict[str, Any]) -> None:
    context["monkeypatch"].setattr(extract, "_MAX_PAGES", 1000)
    _run(context)


@when("I resume the crawl in the browser tier with no page cap")
def resume_no_cap_browser(context: dict[str, Any]) -> None:
    context["monkeypatch"].setattr(extract, "_MAX_PAGES", 1000)
    _run(context, tier="browser")


@when("I run the crawl again")
def run_again(context: dict[str, Any]) -> None:
    _run(context)


@when("I run the crawl twice")
def run_twice(context: dict[str, Any]) -> None:
    context["first_run_requests"] = _run(context)
    context["last_run_requests"] = _run(context)


# --- Then ------------------------------------------------------------------


@then(parsers.parse("exactly {count:d} pages were fetched"))
def exactly_n_pages(context: dict[str, Any], count: int) -> None:
    assert len(context["last_run_requests"]) == count


@then("a resumable frontier was persisted for the target")
def frontier_persisted(context: dict[str, Any]) -> None:
    target = f"{context['server'].base}{_INDEX_PATH}"
    store = crawl_state.crawl_state_for_target(target)
    resumed = store.load()
    assert resumed is not None
    _seen, frontier = resumed
    assert len(frontier) > 0


@then(
    parsers.parse(
        "the resumed run fetches only the {count:d} pages the first run never reached"
    )
)
def resumed_fetches_remaining(context: dict[str, Any], count: int) -> None:
    assert len(context["last_run_requests"]) == count


@then("none of the first run's pages are fetched again")
def no_overlap(context: dict[str, Any]) -> None:
    first = set(context["first_run_requests"])
    second = set(context["last_run_requests"])
    assert first.isdisjoint(second)


@then("every page is fetched again, not skipped as already done")
def every_page_refetched(context: dict[str, Any]) -> None:
    assert len(context["last_run_requests"]) == 1 + _ITEM_COUNT


@then("every page is fetched again on the second run")
def every_page_refetched_second_run(context: dict[str, Any]) -> None:
    assert len(context["first_run_requests"]) == 1 + _ITEM_COUNT
    assert len(context["last_run_requests"]) == 1 + _ITEM_COUNT


@then("no resumable frontier file exists for the target")
def no_frontier_file(context: dict[str, Any]) -> None:
    target = f"{context['server'].base}{_INDEX_PATH}"
    path = crawl_state.store_path_for_target(target)
    assert not path.exists()
