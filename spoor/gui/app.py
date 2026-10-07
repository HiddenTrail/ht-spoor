"""The local GUI's FastAPI app (ROADMAP.md §2i, slice gui-1: browse maps).

Every request passes one guard before any page runs (§2i security posture):

1. **Host check** — the `Host` header must name the loopback address and port the
   GUI was launched on. A page on another site that rebinds its own hostname to
   127.0.0.1 (DNS rebinding) arrives with *its* hostname and is refused.
2. **Origin check** — a request that could change something (anything but
   GET/HEAD) must carry this GUI's own `Origin`, so another site's form can't
   submit to it.
3. **Access token** — a random per-launch token, handed to the browser once via
   `/launch?token=…` and then held in an HttpOnly, SameSite=Strict cookie. A
   request without it is refused, so neither another local user nor another web
   page can drive the GUI.

The pages only read the map store, through the serving layer's shared
`views.map_view` — the same §2h-redacted view the REST/MCP surfaces answer with,
so a secret-shaped value shows as ``[REDACTED]`` here too.
"""

from __future__ import annotations

import hmac
import json
from collections.abc import Awaitable, Callable
from datetime import UTC, datetime
from typing import Any, cast
from urllib.parse import urlencode

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from starlette.responses import Response

from spoor.gui.templates import environment
from spoor.serving.store import MapStore
from spoor.serving.views import map_view


def token_cookie(port: int) -> str:
    """The access-token cookie's name for a GUI on `port`.

    Cookies aren't scoped by port, so a fixed name would let a second running GUI
    overwrite the first one's token and lock its tab out; the port keeps each
    launch's cookie separate.
    """
    return f"spoor_gui_token_{port}"


_SAFE_METHODS = frozenset({"GET", "HEAD"})
_FORBIDDEN_TEXT = (
    "Forbidden. Open Spoor using the link printed when `spoor gui` started."
)


def _same_token(given: str, expected: str) -> bool:
    """Constant-time token comparison; tolerant of non-ASCII input."""
    return hmac.compare_digest(given.encode(), expected.encode())


def human_age(seconds: float) -> str:
    """A plain-language age like "3 hours ago" (never negative)."""
    seconds = max(0, int(seconds))
    for unit, size in (("day", 86400), ("hour", 3600), ("minute", 60)):
        if seconds >= size:
            n = seconds // size
            return f"{n} {unit}{'' if n == 1 else 's'} ago"
    return "just now"


def _cell(value: object) -> str:
    """A record value as table text: scalars as-is, structures as compact JSON."""
    if value is None:
        return ""
    if isinstance(value, str | int | float | bool):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def _map_href(url: str) -> str:
    return "/map?" + urlencode({"url": url})


def create_app(
    store: MapStore, *, token: str, port: int, host: str = "127.0.0.1"
) -> FastAPI:
    """Build the GUI app over `store`, guarded by `token`, for a loopback `port`.

    A factory so tests can inject a temp-backed store and a known token; the
    launcher (`spoor.gui.launch.start_gui`) generates a fresh token per launch
    and passes the loopback `host` it bound (bracketed if IPv6), which the Host
    check accepts alongside the usual loopback names.
    """
    allowed_hosts = {
        f"{name}:{port}" for name in (host, "127.0.0.1", "localhost", "[::1]")
    }
    allowed_origins = {f"http://{host}" for host in allowed_hosts}
    env = environment()
    cookie_name = token_cookie(port)

    app = FastAPI(
        title="Spoor GUI",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    @app.middleware("http")
    async def guard(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        if request.headers.get("host", "") not in allowed_hosts:
            return PlainTextResponse(_FORBIDDEN_TEXT, status_code=403)
        if request.method not in _SAFE_METHODS:
            if request.headers.get("origin", "") not in allowed_origins:
                return PlainTextResponse(_FORBIDDEN_TEXT, status_code=403)
        # /launch checks the token from its query string itself; everything else
        # needs the cookie /launch sets.
        if request.url.path != "/launch":
            cookie = request.cookies.get(cookie_name, "")
            if not _same_token(cookie, token):
                return PlainTextResponse(_FORBIDDEN_TEXT, status_code=403)
        return await call_next(request)

    def render(name: str, status_code: int = 200, **values: Any) -> HTMLResponse:
        html = env.get_template(name).render(**values)
        return HTMLResponse(html, status_code=status_code)

    @app.get("/launch")
    def launch(token_param: str = Query("", alias="token")) -> Response:
        if not _same_token(token_param, token):
            return PlainTextResponse(_FORBIDDEN_TEXT, status_code=403)
        # Move the token out of the URL (and so out of later history entries)
        # into a cookie scripts can't read and other sites never send.
        response = RedirectResponse("/", status_code=303)
        response.set_cookie(
            cookie_name, token, httponly=True, samesite="strict", path="/"
        )
        return response

    @app.get("/", response_class=HTMLResponse)
    def home() -> HTMLResponse:
        domains = [
            {"name": d, "href": "/domain?" + urlencode({"name": d})}
            for d in store.domains()
        ]
        return render("home.html", domains=domains)

    @app.get("/domain", response_class=HTMLResponse)
    def domain(name: str = Query(...)) -> HTMLResponse:
        urls = [
            {
                "url": url,
                "href": _map_href(url),
                "captured_at": captured_at,
                "age": human_age(_age_seconds(captured_at)),
            }
            for url, captured_at in store.urls(name)
        ]
        return render("domain.html", domain=name, urls=urls)

    @app.get("/map", response_class=HTMLResponse)
    def map_page(url: str = Query(...)) -> HTMLResponse:
        entry = store.get(url)
        if entry is None:
            # Never fabricate a map for a URL that was never mapped.
            return render("not_mapped.html", status_code=404, url=url)
        view = map_view(entry)
        records = cast("list[dict[str, object]]", view["records"])
        columns: list[str] = []
        for record in records:
            for key in record:
                if key not in columns:
                    columns.append(key)
        rows = [[_cell(r.get(c)) for c in columns] for r in records]
        return render(
            "map.html",
            view=view,
            domain_href="/domain?" + urlencode({"name": entry.domain}),
            age=human_age(cast(float, view["age_seconds"])),
            columns=columns,
            rows=rows,
            api_surface=_pretty(view["api_surface"]),
            exploration=view["exploration"] or None,
            to_json=_cell,
        )

    return app


def _age_seconds(captured_at: str) -> float:
    return (datetime.now(UTC) - datetime.fromisoformat(captured_at)).total_seconds()


def _pretty(value: object) -> str | None:
    """Indented JSON for a structured section, or None when there's nothing."""
    if not value:
        return None
    return json.dumps(value, indent=2, ensure_ascii=False)
