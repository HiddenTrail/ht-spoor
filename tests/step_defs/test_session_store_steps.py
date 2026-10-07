"""Step definitions for features/session_store.feature (ROADMAP.md §2h, closes #215).

Drives `SessionStore` and `load_session`'s label-resolution path directly —
the public contract a `spoor session add/list/remove` command and a
label-valued `--session` both sit on top of. The map store's temp-cache-root
pattern (`test_serving_steps.py`) is reused unchanged: both stores share the
same database, so redirecting `storage.CACHE_ROOT` isolates this suite's
database the same way.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.security import storage
from spoor.security.session import SessionError, load_session
from spoor.security.session_store import SessionStore

scenarios("session_store.feature")


@pytest.fixture
def context() -> dict[str, Any]:
    """Shared state carried across steps within one scenario."""
    return {}


@pytest.fixture(autouse=True)
def temp_cache_root(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    """Redirect the local cache root so the session store writes under a temp dir."""
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")


def _storage_state(marker: str) -> dict[str, object]:
    return {
        "cookies": [
            {"name": "session", "value": marker, "domain": "x", "path": "/"}
        ],
        "origins": [],
    }


# --- Given ------------------------------------------------------------------


@given(parsers.parse('a storage-state file captured for "{domain}"'))
def captured_file(context: dict[str, Any], domain: str) -> None:
    context.setdefault("captured", {})[domain] = _storage_state(f"captured-{domain}")


@given(parsers.parse('a storage-state file captured for "{domain}" at path "{name}"'))
def captured_file_at_path(
    context: dict[str, Any],
    domain: str,
    name: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # chdir so the bare relative name (what "I load the session <name>" passes,
    # exactly as a --session value would) resolves against this file, proving
    # load_session checks the filesystem before ever trying a stored label.
    monkeypatch.chdir(tmp_path)
    path = tmp_path / name
    path.write_text(json.dumps(_storage_state(f"file-{domain}")), encoding="utf-8")
    context["file_path"] = path
    # A distinct marker from the file's own, so a scenario can tell "resolved
    # from the file" and "resolved from the store" apart by content.
    context.setdefault("captured", {})[domain] = _storage_state(f"captured-{domain}")


@given(parsers.parse('I store that session for "{domain}" labeled "{label}"'))
def given_store_session(context: dict[str, Any], domain: str, label: str) -> None:
    SessionStore().add(domain, label, context["captured"][domain])


# --- When ---------------------------------------------------------------


@when(parsers.parse('I store that session for "{domain}" labeled "{label}"'))
def store_session(context: dict[str, Any], domain: str, label: str) -> None:
    SessionStore().add(domain, label, context["captured"][domain])


@when(parsers.parse('I store a different session for "{domain}" labeled "{label}"'))
def store_different_session(context: dict[str, Any], domain: str, label: str) -> None:
    newer = _storage_state(f"newer-{domain}")
    context.setdefault("captured", {})[domain] = newer
    SessionStore().add(domain, label, newer)


@when(parsers.parse('I remove the session "{label}" for "{domain}"'))
def remove_session(context: dict[str, Any], domain: str, label: str) -> None:
    context["removed"] = SessionStore().remove(domain, label)


@when(parsers.parse('I load the session "{label}" for "{domain}"'))
def load_session_step(context: dict[str, Any], domain: str, label: str) -> None:
    context["loaded"] = load_session(label, domain=domain)


@when(parsers.parse('I try to load the session "{label}" for "{domain}"'))
def try_load_session_step(context: dict[str, Any], domain: str, label: str) -> None:
    try:
        load_session(label, domain=domain)
    except SessionError as exc:
        context["error"] = exc


# --- Then ---------------------------------------------------------------


@then(parsers.parse('listing sessions for "{domain}" shows "{label}"'))
def listing_shows_label(context: dict[str, Any], domain: str, label: str) -> None:
    labels = [m.label for m in SessionStore().list(domain)]
    assert labels == [label]


@then(parsers.parse('listing sessions for "{domain}" shows no sessions'))
def listing_shows_none(context: dict[str, Any], domain: str) -> None:
    assert SessionStore().list(domain) == []


@then('listing sessions for "shop.example" shows only metadata, never values')
def listing_is_metadata_only(context: dict[str, Any]) -> None:
    meta = SessionStore().list("shop.example")
    assert len(meta) == 1
    fields = vars(meta[0])
    assert set(fields) == {"label", "domain", "created_at", "last_used_at"}
    rendered = repr(meta[0])
    assert "captured-shop.example" not in rendered


@then(parsers.parse('listing every stored session shows "{d1}" and "{d2}"'))
def listing_every_shows_both(context: dict[str, Any], d1: str, d2: str) -> None:
    domains = {m.domain for m in SessionStore().list()}
    assert domains == {d1, d2}


@then(parsers.parse('resolving "{label}" for "{domain}" loads the newer session'))
def resolving_loads_newer(context: dict[str, Any], label: str, domain: str) -> None:
    stored = SessionStore().get(domain, label)
    assert stored == context["captured"][domain]


@then("removing reports nothing was removed")
def removing_reports_nothing(context: dict[str, Any]) -> None:
    assert context["removed"] is False


@then(parsers.parse('it resolves to the session stored under "{label}"'))
def resolves_to_stored(context: dict[str, Any], label: str) -> None:
    loaded = context["loaded"]
    assert loaded.path is None
    assert loaded.raw == context["captured"]["shop.example"]


@then(parsers.parse('it resolves to the file at path "{name}", not the stored session'))
def resolves_to_file(context: dict[str, Any], name: str) -> None:
    loaded = context["loaded"]
    assert loaded.path is not None
    assert loaded.path.name == name
    assert loaded.raw != context["captured"]["shop.example"]


@then(
    parsers.parse(
        'it fails because no session file or stored session named "{label}" exists'
    )
)
def fails_with_clear_message(context: dict[str, Any], label: str) -> None:
    error = context["error"]
    assert isinstance(error, SessionError)
    assert label in str(error)
