"""End-to-end authenticated extraction against streaming-clone (§5.1, §2h).

Follows on from `test_integration_streaming_clone.py` (which proves the fixture's
own HTTP contract) by wiring it into Spoor's actual extraction pipeline -- the same
follow-on step PrestaShop's own decision note in ROADMAP.md §5.1 described and Sauce
Demo already completed. This is a second, structurally different bring-your-own-
session (§2h) proof point: Sauce Demo's session is an SPA login-route redirect;
streaming-clone's is a server-set session cookie behind a same-page login form (the
view toggles via JS, no URL change on success) -- a different login mechanic, same
generic capability.

Spoor performs no login itself (§2h, §0): the session below is captured by driving a
real Chromium through the login form exactly as a user would, and only the resulting
`storage_state()` is handed to Spoor via the config's `session:` field.

Marked `integration`: it needs the docker bench up
(`docker compose -f fixtures/docker-compose.yml up -d`) and skips cleanly when the
container isn't reachable, so the fast unit gate stays Docker-free. The bench host
port defaults to 3002; set SPOOR_STREAMING_CLONE_BASE (and the matching
STREAMING_CLONE_PORT for compose) when running on a different port.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
import pytest

from spoor.core import extract
from spoor.core.config import load_config

STREAMING_CLONE_BASE = os.environ.get(
    "SPOOR_STREAMING_CLONE_BASE", "http://127.0.0.1:3002"
)
_DEFAULT_BASE = "http://127.0.0.1:3002"
_USERNAME = "viewer"
_PASSWORD = "spoor-viewer-pw"

_REPO_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _REPO_ROOT / "fixtures" / "configs" / "streaming-clone-catalog.yaml"
# Committed baseline for §5.4 dogfooding: the catalog is static checked-in seed data
# (unlike PrestaShop's variable demo catalog), so an exact golden master fits here.
_GOLDEN_PATH = (
    Path(__file__).resolve().parent / "golden" / "streaming-clone-catalog.json"
)
_RUN_OUTPUT_PATH = _REPO_ROOT / "test-output" / "streaming-clone-catalog.json"

pytestmark = pytest.mark.integration


def _sorted_by_title(records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Stable ordering for comparison -- row/render order isn't a contract."""
    return sorted(records, key=lambda record: str(record["title"]))


def _config_text(session_path: str | None) -> str:
    """The committed fixture config, retargeted to this bench and given a session."""
    text = _CONFIG_PATH.read_text(encoding="utf-8")
    text = text.replace(_DEFAULT_BASE, STREAMING_CLONE_BASE)
    if session_path is not None:
        text += f"session: {session_path}\n"
    return text


@pytest.fixture(scope="module")
def streaming_clone() -> str:
    """Skip the module unless the streaming-clone bench answers on its port."""
    try:
        response = httpx.get(f"{STREAMING_CLONE_BASE}/api/session", timeout=3.0)
        response.raise_for_status()
    except (httpx.HTTPError, OSError) as exc:
        pytest.skip(
            "streaming-clone bench not reachable — start it with "
            "`docker compose -f fixtures/docker-compose.yml up -d` "
            f"({exc})"
        )
    return STREAMING_CLONE_BASE


@pytest.fixture(scope="module")
def captured_session(
    streaming_clone: str, tmp_path_factory: pytest.TempPathFactory
) -> str:
    """Log in as a user would and capture the browser session (§2h input side).

    Unlike Sauce Demo's login (a route redirect), a successful login here just
    toggles the same-page view via JS and renders the catalog -- so readiness is
    "the catalog rendered" (a `.tile` attached), not a URL change.
    """
    from playwright.sync_api import sync_playwright

    path = tmp_path_factory.mktemp("session") / "streaming-clone-session.json"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            context = browser.new_context()
            page = context.new_page()
            page.goto(f"{streaming_clone}/")
            page.fill("#username", _USERNAME)
            page.fill("#password", _PASSWORD)
            page.click("#login-form button[type=submit]")
            page.wait_for_selector(".tile", timeout=10_000)
            state = context.storage_state()
        finally:
            browser.close()
    path.write_text(json.dumps(state), encoding="utf-8")
    return str(path)


def test_browser_tier_without_a_session_is_gated(streaming_clone: str) -> None:
    # No session: the app never fetches or renders the catalog, so no ".tile" ever
    # attaches and the browser tier extracts nothing -- the gate is real.
    result = extract.run_report(load_config(_config_text(None)))
    assert result.blocked == []
    assert result.records == []


def test_authenticated_run_escalates_and_matches_golden(
    streaming_clone: str, captured_session: str
) -> None:
    # tier 1 sees the empty static shell, the dispatcher escalates to the browser
    # tier, which replays the captured session and extracts the rendered catalog
    # (ROADMAP §2, §2h).
    result = extract.run_report(load_config(_config_text(captured_session)))
    assert result.blocked == []
    records = _sorted_by_title(result.records)

    _RUN_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _RUN_OUTPUT_PATH.write_text(
        json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    golden = json.loads(_GOLDEN_PATH.read_text(encoding="utf-8"))
    assert records == golden, (
        "streaming-clone extraction drifted from the golden master; inspect "
        f"{_RUN_OUTPUT_PATH} against {_GOLDEN_PATH}"
    )
