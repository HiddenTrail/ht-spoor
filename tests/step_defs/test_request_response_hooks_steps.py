"""Step definitions for features/request_response_hooks.feature (ROADMAP.md §2d, #150).

The fast-tier scenarios drive an in-memory httpx `MockTransport` routing table,
the same pattern `test_operational_steps.py` uses for robots.txt/politeness —
deterministic, no ports, no real network. The one `@browser` scenario needs a
real loopback server, since the browser tier navigates a real Chromium to a
real URL rather than going through an injected httpx client.
"""

from __future__ import annotations

import re
import threading
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import httpx
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.core import extract
from spoor.core.config import load_config
from spoor.operational.hooks import RunHooks

scenarios("request_response_hooks.feature")

_HEADER_NAME = "X-Api-Key"
_HEADER_VALUE = "secret-api-key-value"
_WRAPPED_TITLE = "[[Widget]]"
_UNWRAPPED_TITLE = "Widget"
_TARGET_PATH = "/item.html"


def _config(target: str) -> str:
    return f'target: {target}\nfields:\n  title: {{ selector: "h1" }}\n'


def _unwrap(html: str) -> str:
    return re.sub(r"\[\[(.*?)\]\]", r"\1", html)


@pytest.fixture
def context() -> dict[str, Any]:
    return {"routes": {}}


# --- Given: fast-tier (MockTransport) routing table -----------------------


@given("a fixture server that reports the headers it received")
def headers_server(context: dict[str, Any]) -> None:
    context["routes"][_TARGET_PATH] = (
        200,
        f'<html><body><h1>{_UNWRAPPED_TITLE}</h1></body></html>',
    )


@given("a fixture server serving a page with a wrapped title")
def wrapped_title_server(context: dict[str, Any]) -> None:
    context["routes"][_TARGET_PATH] = (
        200,
        f"<html><body><h1>{_WRAPPED_TITLE}</h1></body></html>",
    )


@given("a fixture server whose robots.txt disallows the target")
def disallowing_robots_server(context: dict[str, Any]) -> None:
    context["routes"]["/robots.txt"] = (
        200,
        f"User-agent: *\nDisallow: {_TARGET_PATH}\n",
    )
    context["routes"][_TARGET_PATH] = (
        200,
        f"<html><body><h1>{_UNWRAPPED_TITLE}</h1></body></html>",
    )


# --- Given: hooks -----------------------------------------------------------


@given(parsers.parse('an on_request hook that adds an "{header}" header'))
def on_request_adds_header(context: dict[str, Any], header: str) -> None:
    assert header == _HEADER_NAME

    def hook(url: str) -> dict[str, str]:
        return {_HEADER_NAME: _HEADER_VALUE}

    context["on_request"] = hook


@given("an on_request hook that returns nothing")
def on_request_returns_nothing(context: dict[str, Any]) -> None:
    context["on_request"] = lambda url: None


@given("an on_response hook that unwraps the title")
def on_response_unwraps(context: dict[str, Any]) -> None:
    context["on_response"] = lambda url, html: _unwrap(html)


@given("an on_response hook that returns nothing")
def on_response_returns_nothing(context: dict[str, Any]) -> None:
    context["on_response"] = lambda url, html: None


@given("an on_request hook that records every URL it is called with")
def on_request_records(context: dict[str, Any]) -> None:
    calls: list[str] = []
    context["request_calls"] = calls

    def hook(url: str) -> None:
        calls.append(url)
        return None

    context["on_request"] = hook


@given("an on_response hook that records every URL it is called with")
def on_response_records(context: dict[str, Any]) -> None:
    calls: list[str] = []
    context["response_calls"] = calls

    def hook(url: str, html: str) -> None:
        calls.append(url)
        return None

    context["on_response"] = hook


# --- When: fast tier --------------------------------------------------------


def _mock_client(context: dict[str, Any]) -> httpx.Client:
    routes = context["routes"]
    # A list per path, not one dict overwritten per request: `run_report` also
    # probes the target's origin for a published API spec (§2b) alongside the
    # extraction fetch, an unrelated second request to the same path that
    # carries no hook header -- recording every request, not just the last,
    # is what lets the assertions below tell "the extraction fetch carried
    # the header" apart from "nothing ever did".
    received_headers: dict[str, list[dict[str, str]]] = {}
    context["received_headers"] = received_headers

    def handler(request: httpx.Request) -> httpx.Response:
        received_headers.setdefault(request.url.path, []).append(
            dict(request.headers)
        )
        if request.url.path in routes:
            status, body = routes[request.url.path]
            return httpx.Response(status, text=body)
        return httpx.Response(404, text="not found")

    return httpx.Client(transport=httpx.MockTransport(handler))


@when("I run a static config with that hook")
@when("I run a static config with both hooks")
def run_static_with_hooks(context: dict[str, Any]) -> None:
    hooks = RunHooks(
        on_request=context.get("on_request"), on_response=context.get("on_response")
    )
    cfg = load_config(_config(f"http://localhost{_TARGET_PATH}"))
    with _mock_client(context) as client:
        context["result"] = extract.run_report(
            cfg, client=client, hooks=hooks, tiers=(extract.Tier1Resolver(),)
        )


@when("I run a static config with no hooks")
def run_static_without_hooks(context: dict[str, Any]) -> None:
    # No `hooks=` at all -- proves the default (no kwarg passed) behaves exactly
    # like today's pre-#150 call shape, not just like a RunHooks with both
    # fields None.
    cfg = load_config(_config(f"http://localhost{_TARGET_PATH}"))
    with _mock_client(context) as client:
        context["result"] = extract.run_report(
            cfg, client=client, tiers=(extract.Tier1Resolver(),)
        )


# --- Given/When: browser tier (real loopback server) -----------------------


class _HookServer(ThreadingHTTPServer):
    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _HookHandler)
        # Every request to the target path, not just the last: `run_report`
        # also probes the target's origin for a published API spec (§2b)
        # alongside the browser-tier fetch -- an unrelated second request to
        # the same path, from plain httpx, carrying no hook header.
        self.received_requests: list[dict[str, str]] = []

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _HookHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        server: _HookServer = self.server  # type: ignore[assignment]
        if self.path == _TARGET_PATH:
            # Lowercased, matching the fast-tier assertions below -- the raw
            # `email.message.Message` preserves whatever case the client sent
            # a header name in, which isn't the comparison that matters here.
            server.received_requests.append(
                {k.lower(): v for k, v in self.headers.items()}
            )
            body = f"<html><body><h1>{_WRAPPED_TITLE}</h1></body></html>".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, *args: Any) -> None:  # silence per-request stderr log
        pass


@pytest.fixture
def browser_server() -> Iterator[_HookServer]:
    server = _HookServer()
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield server
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)


@given(
    "a fixture server that reports the headers it received and serves "
    "a page with a wrapped title"
)
def browser_headers_and_wrapped_server(
    context: dict[str, Any], browser_server: _HookServer
) -> None:
    context["browser_server"] = browser_server


@when("I run a browser config with both hooks")
def run_browser(context: dict[str, Any]) -> None:
    hooks = RunHooks(
        on_request=context.get("on_request"), on_response=context.get("on_response")
    )
    server = context["browser_server"]
    cfg = load_config(_config(f"{server.base}{_TARGET_PATH}"))
    context["result"] = extract.run_report(
        cfg, hooks=hooks, tiers=(extract.Tier2Resolver(),)
    )


# --- Then --------------------------------------------------------------


@then(parsers.parse('the server received the "{header}" header with that value'))
def server_received_header(context: dict[str, Any], header: str) -> None:
    assert header == _HEADER_NAME
    if "browser_server" in context:
        requests = context["browser_server"].received_requests
        assert any(r.get(_HEADER_NAME.lower()) == _HEADER_VALUE for r in requests)
        return
    requests = context["received_headers"].get(_TARGET_PATH, [])
    assert any(r.get(_HEADER_NAME.lower()) == _HEADER_VALUE for r in requests)


@then(parsers.parse('the server received no "{header}" header'))
def server_received_no_header(context: dict[str, Any], header: str) -> None:
    assert header == _HEADER_NAME
    requests = context["received_headers"].get(_TARGET_PATH, [])
    assert all(_HEADER_NAME.lower() not in r for r in requests)


@then("the extracted title is the unwrapped value")
def extracted_title_unwrapped(context: dict[str, Any]) -> None:
    records = context["result"].records
    assert len(records) == 1
    assert records[0]["title"] == _UNWRAPPED_TITLE


@then("the extracted title is the wrapped value")
def extracted_title_wrapped(context: dict[str, Any]) -> None:
    records = context["result"].records
    assert len(records) == 1
    assert records[0]["title"] == _WRAPPED_TITLE


@then("neither hook was called")
def neither_hook_called(context: dict[str, Any]) -> None:
    assert context["request_calls"] == []
    assert context["response_calls"] == []


@then("the URL is reported blocked")
def url_reported_blocked(context: dict[str, Any]) -> None:
    assert context["result"].blocked == [f"http://localhost{_TARGET_PATH}"]
