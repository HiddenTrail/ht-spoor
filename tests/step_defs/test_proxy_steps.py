"""Step definitions for features/proxy.feature (ROADMAP.md §2d).

Bring-your-own-proxy is proven against a real loopback forward-proxy server,
because the point is that a run's traffic actually travels *through* the
supplied proxy rather than merely accepting the config option. The proxy
server is a plain `http.server` handler that does what a forward proxy does
for a plain-http target (no CONNECT tunnel): the client sends the absolute
target URL as the request line and the proxy fetches it itself, so the proxy
seeing that URL in `self.path` is direct proof the request was routed through
it, not sent straight to the target. The credentials scenario asserts on the
`Proxy-Authorization` header the same way `session.feature` asserts on a
`Cookie` header for bring-your-own-session.
"""

from __future__ import annotations

import base64
import threading
import urllib.request
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest
from pytest_bdd import given, scenarios, then, when

from spoor.core import extract
from spoor.core.config import load_config

scenarios("proxy.feature")

_PATH = "/item.html"
_BODY = (
    '<html><body><ul><li class="item">'
    '<span class="name">Widget</span></li></ul></body></html>'
)
_USERNAME = "proxy-user"
_PASSWORD = "proxy-pa@ss"


class _TargetServer(ThreadingHTTPServer):
    """A plain loopback server standing in for the scraped site."""

    def __init__(self) -> None:
        super().__init__(("127.0.0.1", 0), _TargetHandler)

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _TargetHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        payload = _BODY.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args: Any) -> None:  # silence the per-request stderr log
        pass


class _ProxyServer(ThreadingHTTPServer):
    """A minimal forward proxy: fetches whatever absolute URL it's asked for.

    Records every request it forwards (and the `Proxy-Authorization` header
    presented with it) so a scenario can assert traffic actually passed
    through it. When `require_auth` is set, a request without the matching
    Basic credentials is rejected with 407, same as a real authenticating
    proxy would.
    """

    def __init__(self, *, require_auth: tuple[str, str] | None = None) -> None:
        super().__init__(("127.0.0.1", 0), _ProxyHandler)
        self.requests: list[str] = []
        self.auth_headers: list[str | None] = []
        self.require_auth = require_auth

    @property
    def base(self) -> str:
        return f"http://127.0.0.1:{self.server_address[1]}"


class _ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (BaseHTTPRequestHandler's required name)
        server: _ProxyServer = self.server  # type: ignore[assignment]
        auth_header = self.headers.get("Proxy-Authorization")
        server.requests.append(self.path)
        server.auth_headers.append(auth_header)
        if server.require_auth is not None:
            user, password = server.require_auth
            expected = "Basic " + base64.b64encode(
                f"{user}:{password}".encode()
            ).decode("ascii")
            if auth_header != expected:
                self.send_response(407)
                self.send_header("Proxy-Authenticate", 'Basic realm="proxy"')
                self.end_headers()
                return
        with urllib.request.urlopen(self.path, timeout=5) as upstream:  # noqa: S310
            body = upstream.read()
            self.send_response(upstream.status)
            self.send_header("Content-Type", upstream.headers.get("Content-Type", ""))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, *args: Any) -> None:  # silence the per-request stderr log
        pass


def _config(target_base: str, *, proxy: str | None) -> str:
    text = (
        f"target: {target_base}{_PATH}\n"
        'item: ".item"\n'
        "fields:\n"
        '  name: { selector: ".name" }\n'
    )
    if proxy is not None:
        text += f"proxy:\n  server: {proxy}\n"
    return text


def _config_with_credentials(target_base: str, proxy_base: str) -> str:
    return (
        f"target: {target_base}{_PATH}\n"
        'item: ".item"\n'
        "fields:\n"
        '  name: { selector: ".name" }\n'
        "proxy:\n"
        f"  server: {proxy_base}\n"
        f"  username: {_USERNAME}\n"
        f"  password: {_PASSWORD}\n"
    )


@pytest.fixture
def context() -> Iterator[dict[str, Any]]:
    """Per-scenario state; tears down any loopback servers it started."""
    ctx: dict[str, Any] = {}
    yield ctx
    for key in ("target", "proxy"):
        server = ctx.get(key)
        if server is not None:
            server.shutdown()
            server.server_close()
            ctx[f"{key}_thread"].join(timeout=5)


def _start(server_cls: type, context: dict[str, Any], key: str, **kwargs: Any) -> Any:
    server = server_cls(**kwargs)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    context[key] = server
    context[f"{key}_thread"] = thread
    return server


# --- Given ------------------------------------------------------------------


@given("a target fixture server")
def target_server(context: dict[str, Any]) -> None:
    _start(_TargetServer, context, "target")


@given("a forwarding proxy server")
def proxy_server(context: dict[str, Any]) -> None:
    _start(_ProxyServer, context, "proxy")


@given("a forwarding proxy server that requires a username and password")
def proxy_server_with_auth(context: dict[str, Any]) -> None:
    _start(_ProxyServer, context, "proxy", require_auth=(_USERNAME, _PASSWORD))


# --- When ---------------------------------------------------------------


@when("I run a static config naming that proxy")
def run_static_with_proxy(context: dict[str, Any]) -> None:
    cfg = load_config(
        _config(context["target"].base, proxy=context["proxy"].base)
    )
    context["result"] = extract.run_report(
        cfg, sleep=lambda _s: None, tiers=(extract.Tier1Resolver(),)
    )


@when("I run a static config with no proxy")
def run_static_without_proxy(context: dict[str, Any]) -> None:
    cfg = load_config(_config(context["target"].base, proxy=None))
    context["result"] = extract.run_report(
        cfg, sleep=lambda _s: None, tiers=(extract.Tier1Resolver(),)
    )


@when("I run a static config naming that proxy with credentials")
def run_static_with_proxy_credentials(context: dict[str, Any]) -> None:
    cfg = load_config(
        _config_with_credentials(context["target"].base, context["proxy"].base)
    )
    context["result"] = extract.run_report(
        cfg, sleep=lambda _s: None, tiers=(extract.Tier1Resolver(),)
    )


@when("I run a browser config naming that proxy")
def run_browser_with_proxy(context: dict[str, Any]) -> None:
    cfg = load_config(
        _config(context["target"].base, proxy=context["proxy"].base)
    )
    context["result"] = extract.run_report(
        cfg, sleep=lambda _s: None, tiers=(extract.Tier2Resolver(),)
    )


# --- Then -----------------------------------------------------------------


@then("the proxy server received the request")
def proxy_received_request(context: dict[str, Any]) -> None:
    assert any(_PATH in path for path in context["proxy"].requests)


@then("the proxy server received no request")
def proxy_received_no_request(context: dict[str, Any]) -> None:
    assert context["proxy"].requests == []


@then("the item is extracted")
def item_extracted(context: dict[str, Any]) -> None:
    records = context["result"].records
    assert len(records) == 1
    assert records[0]["name"] == "Widget"


@then("the proxy server saw the matching credentials")
def proxy_saw_credentials(context: dict[str, Any]) -> None:
    expected = "Basic " + base64.b64encode(
        f"{_USERNAME}:{_PASSWORD}".encode()
    ).decode("ascii")
    assert expected in context["proxy"].auth_headers
