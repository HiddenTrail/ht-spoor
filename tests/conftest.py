"""Shared test fixtures and pytest-bdd hooks.

Extraction scenarios target `http://localhost:8000/...` URLs. Rather than run a
real socket server, we serve the checked-in static fixtures (fixtures/static)
through an httpx MockTransport — fully deterministic, no ports, no network.
"""

from __future__ import annotations

import threading
from collections.abc import Iterator
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import httpx
import pytest

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures" / "static"


def _serve(request: httpx.Request) -> httpx.Response:
    rel = request.url.path.lstrip("/") or "index.html"
    target = (FIXTURES_DIR / rel).resolve()
    # Stay within the fixtures dir; serve the file if it exists.
    if FIXTURES_DIR in target.parents and target.is_file():
        return httpx.Response(200, text=target.read_text(encoding="utf-8"))
    return httpx.Response(404, text=f"no fixture for {request.url.path}")


@pytest.fixture
def mock_client() -> Iterator[httpx.Client]:
    """An httpx client that serves the static fixtures for any localhost URL."""
    with httpx.Client(transport=httpx.MockTransport(_serve)) as client:
        yield client


@pytest.fixture
def live_server() -> Iterator[str]:
    """Serve the static fixtures over loopback HTTP for tier-2 browser tests.

    A real browser can't use the `httpx.MockTransport` the tier-1 tests rely on,
    so tier-2 scenarios need an actual socket. Binds an ephemeral port on
    127.0.0.1, serves `fixtures/static`, and yields the base URL.
    """
    handler = partial(SimpleHTTPRequestHandler, directory=str(FIXTURES_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        # We bound to the 127.0.0.1 literal above; only the ephemeral port is
        # assigned by the OS (server_address[0] is typed as possibly bytes).
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture(autouse=True)
def _isolated_cache_root(
    tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Give every test its own local cache, never the developer's real one.

    Commands that record a map (`spoor run`, `spoor explore`) write under
    `storage.CACHE_ROOT`. Without this, a test that didn't redirect it wrote into
    the repository's real `.spoor-cache`, filling a developer's map store (and
    the GUI's Maps page) with test entries. Tests that set their own root still
    do; this is only the safe default underneath.
    """
    from spoor.security import storage

    monkeypatch.setattr(
        storage, "CACHE_ROOT", tmp_path_factory.mktemp("spoor-cache") / ".spoor-cache"
    )
