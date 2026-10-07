"""Unit tests for the bring-your-own-session loader (ROADMAP.md §2h).

The `.feature` scenarios drive session loading end to end through the tiers; these
probe `load_session`/`_cookies_from` directly at the boundaries Gherkin isn't the
grain for — the failure modes (missing / malformed / wrong-typed file), the
tolerant cookie shape-reading (a bad entry skipped, not raised), and the
host-scoped default for a cookie missing domain/path — plus that `apply_cookies`
scopes what the client will actually send.

The stored-label resolution path (§2h Phase B, closes #215) is covered end to
end by `features/session_store.feature`; the two tests at the bottom of this
file pin one boundary case that feature's scenarios don't: that `domain=`
being omitted entirely reproduces the exact pre-#215 behavior (never attempts
a label lookup, even for a string that happens to match no file) — the
guarantee every pre-existing `load_session(path)` call site (none of which are
changed by #215, only given a new keyword) depends on.
"""

from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from spoor.security import storage
from spoor.security.session import (
    SessionCookie,
    SessionError,
    apply_cookies,
    load_session,
    storage_state_arg,
)
from spoor.security.session_store import SessionStore


def _write(tmp_path: Path, data: object) -> str:
    path = tmp_path / "session.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_a_missing_file_raises_session_error(tmp_path: Path) -> None:
    with pytest.raises(SessionError):
        load_session(tmp_path / "nope.json")


def test_malformed_json_raises_session_error(tmp_path: Path) -> None:
    path = tmp_path / "session.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(SessionError):
        load_session(path)


def test_a_non_object_state_raises_session_error(tmp_path: Path) -> None:
    with pytest.raises(SessionError):
        load_session(_write(tmp_path, ["not", "an", "object"]))


def test_a_valid_state_with_no_cookies_loads_empty(tmp_path: Path) -> None:
    session = load_session(_write(tmp_path, {"cookies": [], "origins": []}))
    assert session.cookies == ()


def test_raw_carries_the_parsed_state_verbatim(tmp_path: Path) -> None:
    # `raw` is the exploration driver's re-application source (ROADMAP.md §2e):
    # the parsed storage-state object itself, not routed through SessionCookie.
    data = {
        "cookies": [{"name": "a", "value": "b", "domain": "x", "path": "/"}],
        "origins": [
            {"origin": "http://x", "localStorage": [{"name": "n", "value": "v"}]}
        ],
    }
    session = load_session(_write(tmp_path, data))
    assert session.raw == data


def test_a_state_missing_keys_loads_empty(tmp_path: Path) -> None:
    # A localStorage-only export may carry no `cookies` key at all.
    session = load_session(_write(tmp_path, {"origins": []}))
    assert session.cookies == ()


def test_cookies_are_read_with_scope(tmp_path: Path) -> None:
    session = load_session(
        _write(
            tmp_path,
            {
                "cookies": [
                    {"name": "sid", "value": "abc", "domain": "x.test", "path": "/app"}
                ]
            },
        )
    )
    assert session.cookies == (SessionCookie("sid", "abc", "x.test", "/app"),)


def test_a_cookie_missing_scope_falls_back_to_host_root(tmp_path: Path) -> None:
    session = load_session(_write(tmp_path, {"cookies": [{"name": "s", "value": "v"}]}))
    assert session.cookies == (SessionCookie("s", "v", "", "/"),)


def test_a_bad_cookie_entry_is_skipped_not_raised(tmp_path: Path) -> None:
    # A non-dict entry, a non-list cookies value, and an entry with a non-string
    # name/value are each ignored — a real browser export degrades gracefully.
    session = load_session(
        _write(
            tmp_path,
            {
                "cookies": [
                    "not-a-dict",
                    {"name": "ok", "value": "v", "domain": "d", "path": "/"},
                    {"name": 1, "value": "v"},
                    {"name": "x", "value": None},
                ]
            },
        )
    )
    assert session.cookies == (SessionCookie("ok", "v", "d", "/"),)


def test_non_list_cookies_yields_empty(tmp_path: Path) -> None:
    session = load_session(_write(tmp_path, {"cookies": "nonsense"}))
    assert session.cookies == ()


def test_apply_cookies_scopes_what_the_client_sends(tmp_path: Path) -> None:
    # A cookie scoped to one host is sent there and not to another host.
    cookie = {"name": "sid", "value": "v", "domain": "in.test", "path": "/"}
    session = load_session(_write(tmp_path, {"cookies": [cookie]}))
    with httpx.Client() as client:
        apply_cookies(session, client)
        in_scope = client.cookies.get("sid", domain="in.test")
        assert in_scope == "v"
        assert client.cookies.get("sid", domain="out.test", default=None) is None


# --- domain= / stored-label resolution (§2h Phase B, closes #215) ----------


def test_omitting_domain_never_attempts_a_label_lookup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Every pre-#215 call site passes no domain at all. A session genuinely IS
    # stored under this exact label — proving the omission isn't just "nothing
    # to find anyway" but that the lookup is never even attempted without a
    # domain to scope it to.
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    SessionStore().add("shop.example", "some-label", {"cookies": [], "origins": []})
    with pytest.raises(SessionError):
        load_session("some-label")


def test_domain_given_falls_back_to_a_stored_label(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    stored: dict[str, object] = {
        "cookies": [{"name": "s", "value": "v", "domain": "x", "path": "/"}]
    }
    SessionStore().add("shop.example", "customer", stored)
    session = load_session("customer", domain="shop.example")
    assert session.path is None
    assert session.raw == stored
    assert session.cookies == (SessionCookie("s", "v", "x", "/"),)


def test_a_file_wins_over_a_same_named_stored_label(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    SessionStore().add("shop.example", "customer", {"cookies": [], "origins": []})
    file_path = _write(tmp_path, {"cookies": [], "origins": [], "marker": "file"})
    session = load_session(file_path, domain="shop.example")
    assert session.path == Path(file_path)
    assert session.raw.get("marker") == "file"


def test_neither_file_nor_label_raises_a_message_naming_both(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    with pytest.raises(SessionError, match="nope"):
        load_session("nope", domain="shop.example")


def test_storage_state_arg_is_the_path_for_a_file_backed_session(
    tmp_path: Path,
) -> None:
    session = load_session(_write(tmp_path, {"cookies": [], "origins": []}))
    assert storage_state_arg(session) == str(session.path)


def test_storage_state_arg_is_the_raw_dict_for_a_stored_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    stored: dict[str, object] = {"cookies": [], "origins": []}
    SessionStore().add("shop.example", "customer", stored)
    session = load_session("customer", domain="shop.example")
    assert storage_state_arg(session) == stored
