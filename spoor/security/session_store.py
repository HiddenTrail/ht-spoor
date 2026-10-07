"""Named, stored browser sessions, scoped per site (ROADMAP.md §2h, closes #215).

Phase B of the sparred #184 design (epic #216). Today's `--session <file>` is
purely a CLI-supplied, read-only input (`spoor/security/session.py`): Spoor
never writes one, never names one, never holds more than the one a run was
given. This module adds a **second**, opt-in way to supply the same thing — a
session stored once under a label, scoped to a site, and reused by name across
runs instead of re-pointing at a file path every time — without changing
anything about the first.

**Security posture, called out explicitly (§2h):** storing session data makes
Spoor a persistent holder of live login cookies for the first time; the
`sessions` table gets the same local-only, git-ignored, never-served treatment
every other raw capture already gets (§0/§2h non-negotiable). `SessionMeta`,
the only shape `list()` returns, carries a label and timestamps and nothing
else — never storage-state contents — so even a bug in a CLI command's display
logic cannot leak a cookie value by accident; the shape itself doesn't carry
one. There is deliberately **no serving-layer (MCP/REST) surface at all** for
stored sessions in this slice — purely a CLI-side convenience, so nothing here
touches the §2f read-only non-negotiable.

Shares `spoor/security/db.py`'s connection/migration machinery with
`spoor/serving/store.py:MapStore` — one database, one `sites` table (a session
and a mapped URL for the same domain share the same `site_id`), not two.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import cast
from urllib.parse import urlsplit

from spoor.security import db


@dataclass(frozen=True)
class SessionMeta:
    """A stored session's metadata — label, site, timestamps. Never its contents.

    This is the *only* shape `SessionStore.list()` returns, by design (§2h): a
    cookie/storage-state value is never part of what gets listed, printed, or
    handed to a caller that only asked "what's stored", so a display bug can't
    leak one.
    """

    label: str
    domain: str
    created_at: str  # ISO-8601 UTC
    last_used_at: str | None  # ISO-8601 UTC, or None if never resolved via get()


def domain_of(url_or_domain: str) -> str:
    """The site a session is scoped to, from a URL or a bare domain.

    `urlsplit` only finds a netloc when the string has a scheme (`https://...`);
    a bare domain (`shop.example`) has no netloc, so it's returned as-is —
    accepting either shape. Used by `spoor session add/list/remove`'s `site`
    argument, so a session and a mapped URL for the same site resolve to the
    same `sites.domain` whether the caller pasted a bare domain or a full URL.
    """
    netloc = urlsplit(url_or_domain).netloc
    return netloc or url_or_domain


class SessionStore:
    """Read/write access to named, per-site stored sessions (§2h, closes #215).

    Connects via `spoor.security.db.connect()` — a fresh connection per call,
    migrated to the latest schema, never held across calls or shared across
    threads (see that module for the full connection posture).
    """

    def add(
        self, domain: str, label: str, storage_state: dict[str, object]
    ) -> None:
        """Store `storage_state` under `label`, scoped to `domain`.

        Upserts: adding under a label that already exists for this site replaces
        its stored state (a re-captured session, re-added under the same name) and
        resets `last_used_at` to unset — the old state is gone, so "last used"
        before this call no longer describes what's stored now.
        """
        conn = db.connect()
        try:
            with conn:
                site_id = db.get_or_create_site(conn, domain)
                conn.execute(
                    "INSERT INTO sessions"
                    " (site_id, label, storage_state_json, created_at, last_used_at)"
                    " VALUES (?, ?, ?, ?, NULL)"
                    " ON CONFLICT(site_id, label) DO UPDATE SET"
                    "   storage_state_json = excluded.storage_state_json,"
                    "   created_at = excluded.created_at,"
                    "   last_used_at = NULL",
                    (
                        site_id,
                        label,
                        json.dumps(storage_state),
                        datetime.now(UTC).isoformat(),
                    ),
                )
        finally:
            conn.close()

    def get(self, domain: str, label: str) -> dict[str, object] | None:
        """The stored storage-state for `label` under `domain`, or None if unknown.

        Marks the session as used (`last_used_at` set to now) as a side effect of
        a successful lookup — so `list()` can show when a stored session was last
        actually resolved into a run, not just when it was added.
        """
        conn = db.connect()
        try:
            row = conn.execute(
                "SELECT sessions.id, sessions.storage_state_json"
                " FROM sessions JOIN sites ON sessions.site_id = sites.id"
                " WHERE sites.domain = ? AND sessions.label = ?",
                (domain, label),
            ).fetchone()
            if row is None:
                return None
            session_id, raw_json = row
            with conn:
                conn.execute(
                    "UPDATE sessions SET last_used_at = ? WHERE id = ?",
                    (datetime.now(UTC).isoformat(), session_id),
                )
        finally:
            conn.close()
        return cast("dict[str, object]", json.loads(raw_json))

    def list(self, domain: str | None = None) -> list[SessionMeta]:
        """Every stored session's metadata, optionally scoped to one `domain`.

        Sorted by domain then label. Never includes storage-state contents — see
        `SessionMeta`.
        """
        conn = db.connect()
        try:
            if domain is None:
                rows = conn.execute(
                    "SELECT sessions.label, sites.domain, sessions.created_at,"
                    " sessions.last_used_at"
                    " FROM sessions JOIN sites ON sessions.site_id = sites.id"
                    " ORDER BY sites.domain, sessions.label"
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT sessions.label, sites.domain, sessions.created_at,"
                    " sessions.last_used_at"
                    " FROM sessions JOIN sites ON sessions.site_id = sites.id"
                    " WHERE sites.domain = ?"
                    " ORDER BY sessions.label",
                    (domain,),
                ).fetchall()
        finally:
            conn.close()
        return [
            SessionMeta(
                label=label,
                domain=site_domain,
                created_at=created,
                last_used_at=used,
            )
            for label, site_domain, created, used in rows
        ]

    def remove(self, domain: str, label: str) -> bool:
        """Delete the stored session for `label` under `domain`.

        Returns whether a session was actually deleted, so a caller (the `spoor
        session remove` command) can tell "removed" from "there was nothing to
        remove" apart.
        """
        conn = db.connect()
        try:
            with conn:
                cursor = conn.execute(
                    "DELETE FROM sessions WHERE label = ? AND site_id IN"
                    " (SELECT id FROM sites WHERE domain = ?)",
                    (label, domain),
                )
        finally:
            conn.close()
        return cursor.rowcount > 0
