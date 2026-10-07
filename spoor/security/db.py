"""Shared SQLite connection and migration machinery for Spoor's durable store.

One database (`spoor.db`, under the git-ignored cache root) holds every table
Spoor's local, durable stores need. `spoor/serving/store.py:MapStore` (§2f,
closes #214) and `spoor/security/session_store.py:SessionStore` (§2h, closes
#215) are both thin, table-specific wrappers over the connection and migration
machinery here — one place that opens the file, one busy_timeout/foreign-key
posture, one ordered migration list — rather than two SQLite implementations of
the same database quietly drifting apart. `sqlite3` is stdlib, so neither store
adds a new dependency; both follow the house style the existing SQLite output
sink (`spoor/operational/output.py`) already set: plain SQL, no ORM.
"""

from __future__ import annotations

import sqlite3
from typing import cast

from spoor.security import storage

# The database file holding every durable store's tables, under the
# git-ignored cache root.
DB_FILENAME = "spoor.db"

# Schema migrations, applied in order and tracked via `PRAGMA user_version`
# (index + 1 = the version that script brings the database to). Each script may
# hold multiple statements (`executescript`, not `execute`). Append, never edit,
# a shipped migration — the same "schema only ever grows forward" discipline
# any persistent store needs. Migration 1 is MapStore's original schema
# (closes #214); migration 2 adds SessionStore's table (closes #215).
_MIGRATIONS: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS sites (
        id INTEGER PRIMARY KEY,
        domain TEXT NOT NULL UNIQUE
    );
    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY,
        site_id INTEGER NOT NULL REFERENCES sites(id),
        url TEXT NOT NULL,
        captured_at TEXT NOT NULL,
        tier INTEGER,
        records_json TEXT NOT NULL,
        api_surface_json TEXT,
        exploration_json TEXT,
        config_json TEXT
    );
    CREATE INDEX IF NOT EXISTS idx_runs_url_captured
        ON runs(url, captured_at DESC, id DESC);
    CREATE INDEX IF NOT EXISTS idx_runs_site ON runs(site_id);
    """,
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY,
        site_id INTEGER NOT NULL REFERENCES sites(id),
        label TEXT NOT NULL,
        storage_state_json TEXT NOT NULL,
        created_at TEXT NOT NULL,
        last_used_at TEXT,
        UNIQUE(site_id, label)
    );
    """,
)


def _migrate(conn: sqlite3.Connection) -> None:
    """Apply any schema migrations this connection's database hasn't seen yet."""
    (current,) = conn.execute("PRAGMA user_version").fetchone()
    for version, script in enumerate(_MIGRATIONS, start=1):
        if version > current:
            conn.executescript(script)
            # PRAGMA doesn't accept bound parameters; `version` is our own loop
            # counter, never external input, so the f-string carries no
            # injection risk.
            conn.execute(f"PRAGMA user_version = {version}")
    conn.commit()


def connect() -> sqlite3.Connection:
    """Open a connection to the shared database, migrated to the latest schema.

    The cache root is read from `spoor.security.storage.CACHE_ROOT` at call time
    (not import), so a test's monkeypatch of it takes effect without reconstructing
    a store. A fresh connection is expected per call (never held across calls or
    shared across threads) — `spoor serve` may field genuinely concurrent requests,
    and SQLite connections aren't safe to share across threads.
    """
    path = storage.CACHE_ROOT / DB_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    # busy_timeout: without this, a writer that loses a race for SQLite's file
    # lock gets an immediate "database is locked" error instead of waiting
    # briefly and retrying. Deliberately NOT switching to WAL journal mode: that
    # switch itself requires an exclusive lock, so issuing it from every
    # connection racing to open a brand-new database file is a real
    # deadlock-shaped bug, not a hypothetical one (found by MapStore's own
    # concurrent-writer test, see the #214 decision note). WAL is a
    # concurrent-reader-during-write performance optimization Spoor's actual
    # write pattern (occasional CLI runs, rare recheck calls) doesn't need; the
    # default rollback-journal mode plus busy_timeout is correct and sufficient.
    conn = sqlite3.connect(path, timeout=5.0)
    conn.execute("PRAGMA busy_timeout = 5000")
    conn.execute("PRAGMA foreign_keys=ON")
    _migrate(conn)
    return conn


def get_or_create_site(conn: sqlite3.Connection, domain: str) -> int:
    """The `sites.id` for `domain`, inserting a row first if needed."""
    conn.execute("INSERT OR IGNORE INTO sites (domain) VALUES (?)", (domain,))
    (site_id,) = conn.execute(
        "SELECT id FROM sites WHERE domain = ?", (domain,)
    ).fetchone()
    return cast(int, site_id)
