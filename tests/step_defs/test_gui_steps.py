"""Step definitions for features/gui.feature (ROADMAP.md §2i, slice gui-1).

The GUI is a separate local control plane over the same map store the serving
layer reads. These steps back the store with a temp cache root, drive the GUI's
FastAPI app in-process with a test client addressed at a loopback host (so the
Host check sees what a real browser would send), and pin the security posture:
loopback-only bind, per-launch token, Host/Origin checks, redacted display, and
an untouched read-only serving app. The one `@browser` scenario launches the real
server on an ephemeral loopback port and drives it with headless Chromium.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from _serving_fixtures import explored_graph
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.gui.app import create_app, token_cookie
from spoor.gui.launch import GuiError, start_gui
from spoor.security import storage
from spoor.serving.api import create_app as create_serving_app
from spoor.serving.store import MapStore, shareable_exploration_map

scenarios("gui.feature")

_TOKEN = "known-test-token"
_PORT = 8765
_BASE = f"http://127.0.0.1:{_PORT}"
_URL = "https://shop.example/products"


@pytest.fixture
def context() -> Iterator[dict[str, Any]]:
    """Shared state carried across steps within one scenario."""
    ctx: dict[str, Any] = {}
    yield ctx
    if "browser" in ctx:
        pw, browser = ctx["browser"]
        browser.close()
        pw.stop()
    gui = ctx.get("gui")
    if gui is not None:
        gui.stop()


@pytest.fixture(autouse=True)
def temp_cache_root(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect the local cache root so the map store writes under a temp dir."""
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")


def _client(context: dict[str, Any], *, with_token: bool = True) -> TestClient:
    client = TestClient(context["app"], base_url=_BASE, follow_redirects=False)
    if with_token:
        client.cookies.set(token_cookie(_PORT), _TOKEN)
    return client


# --- Given ---------------------------------------------------------------


@given(parsers.parse('a map store that has mapped "{url}"'))
def mapped_store(context: dict[str, Any], url: str) -> None:
    store = MapStore()
    store.record(
        url,
        [{"title": "Blue mug", "price": "12.00"}],
        tier=1,
        captured_at=datetime.now(UTC) - timedelta(hours=3),
    )
    context["store"] = store


@given("the GUI app is created with a known access token")
def gui_app(context: dict[str, Any]) -> None:
    context["app"] = create_app(context["store"], token=_TOKEN, port=_PORT)


@given("an empty map store")
def empty_store(
    context: dict[str, Any], tmp_path: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    # MapStore reads the cache root at call time, so pointing it at a fresh,
    # empty directory empties the store the already-built app reads from.
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / "empty-cache")


@given(parsers.parse('the mapped records for "{url}" contain "{value}"'))
def records_with_value(context: dict[str, Any], url: str, value: str) -> None:
    context["store"].record(url, [{"note": value}], tier=1)


@given(
    parsers.parse(
        '"{url}" has an explored graph with a skipped destructive action'
    )
)
def explored(context: dict[str, Any], url: str) -> None:
    context["store"].record(
        url, [], exploration=shareable_exploration_map(explored_graph())
    )


@given("the GUI is running on loopback")
def gui_running(context: dict[str, Any]) -> None:
    context["gui"] = start_gui(context["store"])


# --- When ----------------------------------------------------------------


@when(parsers.parse('I ask the GUI launcher to bind to "{host}"'))
def bind_to(context: dict[str, Any], host: str) -> None:
    try:
        context["gui"] = start_gui(context["store"], host=host)
    except GuiError as exc:
        context["error"] = exc


@when("I open the launch URL carrying the access token")
def open_launch(context: dict[str, Any]) -> None:
    client = _client(context, with_token=False)
    context["response"] = client.get(f"/launch?token={_TOKEN}")


@when("I request the home page without the access token")
def home_without_token(context: dict[str, Any]) -> None:
    context["response"] = _client(context, with_token=False).get("/")


@when(parsers.parse('I request the home page with the access token "{token}"'))
def home_with_wrong_token(context: dict[str, Any], token: str) -> None:
    client = _client(context, with_token=False)
    client.cookies.set(token_cookie(_PORT), token)
    context["response"] = client.get("/")


@when(
    parsers.parse(
        'I request the home page with the access token and Host header "{host}"'
    )
)
def home_with_host(context: dict[str, Any], host: str) -> None:
    context["response"] = _client(context).get("/", headers={"host": host})


@when(
    parsers.parse(
        'I POST to the home page with the access token and Origin "{origin}"'
    )
)
def post_with_origin(context: dict[str, Any], origin: str) -> None:
    context["response"] = _client(context).post("/", headers={"origin": origin})


@when("I request the home page with the access token")
def home_with_token(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/")


@when(parsers.parse('I open the domain page for "{domain}" with the access token'))
def open_domain(context: dict[str, Any], domain: str) -> None:
    context["response"] = _client(context).get("/domain", params={"name": domain})


@when(parsers.parse('I open the map page for "{url}" with the access token'))
def open_map(context: dict[str, Any], url: str) -> None:
    context["response"] = _client(context).get("/map", params={"url": url})


@when("a real browser opens the launch URL")
def browser_opens(context: dict[str, Any]) -> None:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    context["browser"] = (pw, browser)
    context["page"] = page
    page.goto(context["gui"].launch_url)


@when(parsers.parse('clicks the domain "{domain}"'))
def click_domain(context: dict[str, Any], domain: str) -> None:
    context["page"].get_by_role("link", name=domain).click()


@when(parsers.parse('clicks the mapped URL "{url}"'))
def click_url(context: dict[str, Any], url: str) -> None:
    context["page"].get_by_role("link", name=url).click()


# --- Then ----------------------------------------------------------------


def _text(context: dict[str, Any]) -> str:
    return str(context["response"].text)


@then("the launch is refused with a message that the GUI is local-only")
def launch_refused(context: dict[str, Any]) -> None:
    assert "gui" not in context, "the GUI must not start on a non-loopback host"
    assert "local-only" in str(context["error"])


@then("I am redirected to the home page without the token in the URL")
def redirected_home(context: dict[str, Any]) -> None:
    response = context["response"]
    assert response.status_code == 303
    assert response.headers["location"] == "/"


@then("the response sets an HttpOnly, SameSite=Strict token cookie")
def sets_token_cookie(context: dict[str, Any]) -> None:
    cookie = context["response"].headers["set-cookie"]
    assert f"{token_cookie(_PORT)}={_TOKEN}" in cookie
    assert "httponly" in cookie.lower()
    assert "samesite=strict" in cookie.lower()


@then(parsers.parse("the response status is {status:d}"))
def response_status(context: dict[str, Any], status: int) -> None:
    assert context["response"].status_code == status


@then("the read-only serving app's routes are unchanged by the GUI")
def serving_unchanged(context: dict[str, Any]) -> None:
    serving = create_serving_app(context["store"])
    paths = {getattr(r, "path", "") for r in serving.routes}
    methods = set().union(*(getattr(r, "methods", set()) for r in serving.routes))
    api_paths = paths - {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
    assert api_paths == {"/healthz", "/domains", "/map"}
    assert methods <= {"GET", "HEAD"}


@then(parsers.parse('the page lists the domain "{domain}"'))
def lists_domain(context: dict[str, Any], domain: str) -> None:
    assert context["response"].status_code == 200
    assert f">{domain}</a>" in _text(context)


@then("the page says nothing has been mapped yet")
def nothing_mapped(context: dict[str, Any]) -> None:
    assert "Nothing has been mapped yet" in _text(context)


@then(parsers.parse('the page links to the map for "{url}"'))
def links_to_map(context: dict[str, Any], url: str) -> None:
    assert context["response"].status_code == 200
    assert 'href="/map?url=https%3A%2F%2Fshop.example%2Fproducts"' in _text(context)
    assert f">{url}</a>" in _text(context)


@then("the page shows the capture time and its age")
def shows_age(context: dict[str, Any]) -> None:
    text = _text(context)
    entry = context["store"].get(_URL)
    assert entry.captured_at in text
    assert "3 hours ago" in text


@then("the page shows the mapped records")
def shows_records(context: dict[str, Any]) -> None:
    text = _text(context)
    assert "Blue mug" in text
    assert "12.00" in text


@then(parsers.parse('the page shows "{value}"'))
def shows_value(context: dict[str, Any], value: str) -> None:
    assert value in _text(context)


@then(parsers.parse('the page never shows "{value}"'))
def never_shows(context: dict[str, Any], value: str) -> None:
    assert value not in _text(context)


@then("the page lists the graph's states and transitions")
def lists_graph(context: dict[str, Any]) -> None:
    text = _text(context)
    assert "state-a" in text
    assert "state-b" in text
    assert "Open menu" in text


@then("the page lists the skipped action with its reason")
def lists_skip(context: dict[str, Any]) -> None:
    text = _text(context)
    assert "Delete account" in text
    assert "destructive action skipped outside a sandbox" in text


@then("the page says the URL has not been mapped")
def says_not_mapped(context: dict[str, Any]) -> None:
    assert "has not been mapped" in _text(context)


@then(parsers.parse('the browser shows the map for "{url}"'))
def browser_shows_map(context: dict[str, Any], url: str) -> None:
    page = context["page"]
    assert page.get_by_role("heading", name=url).is_visible()
    assert page.get_by_text("Blue mug").is_visible()


@then("the page shows the Spoor logo in the top bar and as its browser-tab icon")
def shows_logo(context: dict[str, Any]) -> None:
    from spoor.gui.templates import logo_data_uri

    text = _text(context)
    night = logo_data_uri("night")
    # The orange hexagon is the tab icon in both modes: it reads on any tab bar.
    assert f'<link rel="icon" type="image/svg+xml" href="{night}" />' in text
    assert f'<img class="logo-night" src="{night}" alt="" />' in text


@then("the page has the day/night switch and follows the system setting")
def has_theme_switch(context: dict[str, Any]) -> None:
    from spoor.exploration.theme import THEME_SCRIPT, TOGGLE_BUTTON

    text = _text(context)
    assert THEME_SCRIPT in text
    assert TOGGLE_BUTTON in text
    assert "@media (prefers-color-scheme: light)" in text
    # Nothing chosen server-side: the browser's setting decides until the reader
    # picks a mode.
    assert '<html lang="en">' in text


@then("the page carries the night logo and the day logo, one shown per mode")
def has_both_logos(context: dict[str, Any]) -> None:
    from spoor.gui.templates import logo_data_uri

    text = _text(context)
    assert f'<img class="logo-night" src="{logo_data_uri("night")}" alt="" />' in text
    assert f'<img class="logo-day" src="{logo_data_uri("day")}" alt="" />' in text
    assert ".logo-night { display: var(--night-only); }" in text
    assert ".logo-day { display: var(--day-only); }" in text


@when("a real browser set to light mode opens the launch URL")
def light_browser_opens(context: dict[str, Any]) -> None:
    from playwright.sync_api import sync_playwright

    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    context["browser"] = (pw, browser)
    page = browser.new_context(color_scheme="light").new_page()
    context["page"] = page
    page.goto(context["gui"].launch_url)


@when("the browser switches to night mode")
def switch_to_night(context: dict[str, Any]) -> None:
    context["page"].get_by_role("button", name="Switch to night mode").click()


@when("the GUI is restarted on another port and the browser opens it again")
def restart_gui(context: dict[str, Any]) -> None:
    old = context["gui"]
    old.stop()
    context["gui"] = start_gui(context["store"])
    assert context["gui"].url != old.url
    context["page"].goto(context["gui"].launch_url)


def _mode(context: dict[str, Any]) -> tuple[str, bool, bool]:
    page = context["page"]
    background = page.evaluate("getComputedStyle(document.body).backgroundColor")
    return (
        background,
        page.locator("nav .logo-day").is_visible(),
        page.locator("nav .logo-night").is_visible(),
    )


@then("the page is in day mode with the day logo")
def in_day_mode(context: dict[str, Any]) -> None:
    assert _mode(context) == ("rgb(255, 255, 255)", True, False)


@then("the page is in night mode with the night logo")
def in_night_mode(context: dict[str, Any]) -> None:
    assert _mode(context) == ("rgb(31, 28, 27)", False, True)


@when("I open the maps page with the access token")
def open_maps(context: dict[str, Any]) -> None:
    context["response"] = _client(context).get("/maps")


@when("opens the maps page")
def browser_opens_maps(context: dict[str, Any]) -> None:
    context["page"].get_by_role("link", name="Maps", exact=True).click()


@then("the page introduces Spoor with what it is for")
def intro_headline(context: dict[str, Any]) -> None:
    assert context["response"].status_code == 200
    text = _text(context)
    assert "Give your agents a map of the web." in text
    assert "map of the site" in text


def _readable(context: dict[str, Any]) -> str:
    """The page as a reader sees its words: entities decoded, whitespace collapsed."""
    import html

    return " ".join(html.unescape(_text(context)).split())


@then("the page describes what Spoor does and who it is for")
def intro_does_and_who(context: dict[str, Any]) -> None:
    text = _readable(context)
    for heading in (
        "What Spoor does",
        "Maps a site's screens and actions",
        "Extracts data that survives redesigns",
        "Shows the API behind the page",
        "Hands the map to scripts and agents",
        "Who it's for",
        "Test automation.",
        "Building AI agents.",
    ):
        assert heading in text, heading


@then("the page says how Spoor stays safe by default")
def intro_safety(context: dict[str, Any]) -> None:
    text = _text(context)
    assert "Safe by default" in text
    assert "Stays on your computer." in text
    assert "never uploaded anywhere" in text
    assert "Never deletes, buys or pays on a real site." in text


@then("the page links to the Spoor repository")
def intro_repo(context: dict[str, Any]) -> None:
    from spoor.gui.app import project_urls

    repo = project_urls()["Repository"]
    assert repo == "https://github.com/HiddenTrail/ht-spoor"
    assert f'href="{repo}"' in _text(context)


@then("the top bar's Spoor logo links to the introduction and Maps to the maps page")
def nav_links(context: dict[str, Any]) -> None:
    text = _text(context)
    assert '<a class="brand" href="/">' in text
    assert '<a href="/maps">Maps</a>' in text


@then("the page links to exploring a site, extracting, the maps and the servers")
def intro_start_links(context: dict[str, Any]) -> None:
    text = _text(context)
    for href in ("/new/explore", "/new/run", "/maps", "/servers"):
        assert f'<a class="card" href="{href}">' in text, href


@then(parsers.parse("the page says {count:d} site is mapped so far"))
def intro_count(context: dict[str, Any], count: int) -> None:
    assert f"{count} site mapped so far." in _readable(context)
