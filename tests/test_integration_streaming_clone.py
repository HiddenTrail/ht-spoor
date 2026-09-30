"""Live boot proof for the fourth archetype: streaming-clone (§5.1).

Unlike the Sauce Demo/PrestaShop tests, this does not yet run Spoor's extraction
pipeline against the fixture (see the PrestaShop "deliberately not shipped" note in
ROADMAP.md §5.1 for the same reasoning: that's its own BDD-first slice, wiring the
archetype into the automated exploration/extraction bench). This test instead proves
the fixture itself behaves as documented — the login gate is real, the catalog API is
reachable once authenticated, and an unauthenticated request is rejected — the same
"stand the target up and prove its own contract" step PrestaShop's own decision note
records as landing first.

Marked `integration`: it needs the docker bench up
(`docker compose -f fixtures/docker-compose.yml up -d`) and skips cleanly when the
container isn't reachable, so the fast unit gate stays Docker-free. The bench host
port defaults to 3002; set SPOOR_STREAMING_CLONE_BASE (and the matching
STREAMING_CLONE_PORT for compose) when running on a different port.
"""

from __future__ import annotations

import os

import httpx
import pytest

STREAMING_CLONE_BASE = os.environ.get(
    "SPOOR_STREAMING_CLONE_BASE", "http://127.0.0.1:3002"
)
_USERNAME = "viewer"
_PASSWORD = "spoor-viewer-pw"

pytestmark = pytest.mark.integration


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


def test_catalog_is_gated_without_a_session(streaming_clone: str) -> None:
    response = httpx.get(f"{streaming_clone}/api/catalog", timeout=3.0)
    assert response.status_code == 401


def test_login_then_catalog_returns_the_seeded_rows(streaming_clone: str) -> None:
    with httpx.Client(base_url=streaming_clone, timeout=3.0) as client:
        login = client.post(
            "/api/login", json={"username": _USERNAME, "password": _PASSWORD}
        )
        assert login.status_code == 200

        catalog = client.get("/api/catalog")
        assert catalog.status_code == 200

        rows = catalog.json()["rows"]
        assert rows, "expected at least one category row"
        titles = [title for row in rows for title in row["titles"]]
        assert len(titles) == 6
        assert {title["title"] for title in titles} >= {
            "Ridge & Static",
            "Nightshift Arcade",
            "Perihelion",
        }


def test_wrong_password_is_rejected(streaming_clone: str) -> None:
    response = httpx.post(
        f"{streaming_clone}/api/login",
        json={"username": _USERNAME, "password": "not-the-password"},
        timeout=3.0,
    )
    assert response.status_code == 401


def test_every_seeded_title_has_a_playable_video(streaming_clone: str) -> None:
    # The §2c media/streaming-capture signal this archetype exists to exercise
    # needs a real, servable clip behind every title, not just the wiring.
    with httpx.Client(base_url=streaming_clone, timeout=3.0) as client:
        client.post("/api/login", json={"username": _USERNAME, "password": _PASSWORD})
        catalog = client.get("/api/catalog").json()
        titles = [title for row in catalog["rows"] for title in row["titles"]]
        assert titles
        for title in titles:
            detail = client.get(f"/api/titles/{title['id']}")
            assert detail.status_code == 200
            video_response = client.get(detail.json()["video"])
            assert video_response.status_code == 200
            assert video_response.headers["content-type"] == "video/mp4"
