"""Unit tests for the local GUI's helpers (ROADMAP.md §2i).

The behaviour-level contract lives in features/gui.feature; these pin the small
boundaries the scenarios don't reach directly.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from spoor.gui.app import create_app, human_age, token_cookie
from spoor.gui.launch import GuiError, start_gui
from spoor.security import storage
from spoor.serving.store import MapStore


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (-5, "just now"),
        (0, "just now"),
        (59, "just now"),
        (60, "1 minute ago"),
        (119, "1 minute ago"),
        (3600, "1 hour ago"),
        (7200, "2 hours ago"),
        (86399, "23 hours ago"),
        (86400, "1 day ago"),
        (10 * 86400, "10 days ago"),
    ],
)
def test_human_age_boundaries(seconds: float, expected: str) -> None:
    assert human_age(seconds) == expected


@pytest.mark.parametrize(
    "host", ["0.0.0.0", "::", "192.168.1.5", "localhost.evil.example", ""]
)
def test_launcher_refuses_every_non_loopback_host(host: str) -> None:
    with pytest.raises(GuiError, match="local-only"):
        start_gui(MapStore(), host=host)


def test_a_same_origin_post_passes_the_guard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The guard lets this GUI's own origin through (405: no POST route exists in
    # gui-1), so the 403 in the cross-site scenario really is the Origin check.
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    app = create_app(MapStore(), token="t", port=9000)
    client = TestClient(app, base_url="http://127.0.0.1:9000")
    client.cookies.set(token_cookie(9000), "t")
    response = client.post("/", headers={"origin": "http://127.0.0.1:9000"})
    assert response.status_code == 405


def test_a_non_ascii_token_is_rejected_not_crashed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    app = create_app(MapStore(), token="t", port=9000)
    client = TestClient(app, base_url="http://127.0.0.1:9000")
    response = client.get("/launch", params={"token": "tö"})
    assert response.status_code == 403


def test_a_gui_on_another_loopback_address_accepts_its_own_host(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Any 127.x address is loopback, so the launcher allows it; the app must then
    # accept requests addressed to that same address, not only 127.0.0.1.
    import httpx

    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path)
    gui = start_gui(MapStore(), host="127.0.0.2")
    try:
        response = httpx.get(gui.launch_url, follow_redirects=True)
        assert response.status_code == 200
        assert "Nothing has been mapped yet" in response.text
    finally:
        gui.stop()
