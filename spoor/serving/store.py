"""Persisted map that the read-only serving layer answers from (§2f).

The serving layer (`spoor/serving/api.py`) is a *thin* read-over of what a run
already produced — it holds no capture or analysis logic of its own (§2f). This
module is that data: a run records its extracted records for a URL here, with
the capture time; the API reads it back and attaches a freshness age (§2f
"always show the age, never auto-recheck" in v1).

Placement (§0/§2h): the map holds the same extracted records the output pipeline
already writes to shared output — not a raw local-only capture (HAR/storage
state), which never enters here.

**Storage (closes #214, epic #216).** A single SQLite database under the
git-ignored cache root (`spoor.db`), replacing the earlier one-JSON-file-per-domain
convention — `sqlite3` is stdlib, so this adds no new dependency, and matches the
house style the existing SQLite *output sink* (`spoor/operational/output.py`)
already set: plain `sqlite3`, explicit SQL, no ORM. Every `record()` call is an
**insert**, not an overwrite — real run history is kept (a thing the old
per-domain-JSON approach could not do without an unbounded full-file rewrite on
every run) — but `get()` still returns only the **latest** row for a URL, so the
public behavior every caller already depends on (`record()` "replaces" what
`get()` answers) is unchanged; history exists in the table but isn't exposed
through this interface yet. Schema migrations are tracked with SQLite's own
`PRAGMA user_version` (a tiny, Spoor-native migration runner — no
Alembic/SQLAlchemy). A missing or freshly-created database is simply "nothing
mapped yet", never an error. Existing `.spoor-cache/maps/*.json` files from
before this change are orphaned, not imported — Spoor is pre-alpha, and every
record in them is re-capturable by re-running.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, cast
from urllib.parse import urlsplit

from spoor.api_discovery.correlation import ActionCorrelation
from spoor.api_discovery.discovery import DiscoveredSpec
from spoor.api_discovery.graphql import DiscoveredGraphQL
from spoor.api_discovery.synthesis import SynthesizedSpec
from spoor.security import storage

if TYPE_CHECKING:
    # Type-only: the projection reads the graph's attributes, so serving never
    # imports the exploration package at runtime and stays light for the `serve`
    # extra (the graph model is pure, but the type hints don't force the import).
    from spoor.exploration.capture import StateSignals, TransitionSignals
    from spoor.exploration.discovery import ActionableElement
    from spoor.exploration.graph import ExplorationGraph

# The SQLite database file holding the map, under the git-ignored cache root.
DB_FILENAME = "spoor.db"

# Schema migrations, applied in order and tracked via `PRAGMA user_version`
# (index + 1 = the version that script brings the database to). Each script may
# hold multiple statements (`executescript`, not `execute`). Append, never edit,
# a shipped migration — the same "schema only ever grows forward" discipline
# any persistent store needs.
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


def shareable_api_surface(
    *,
    api_spec: DiscoveredSpec | None,
    graphql: DiscoveredGraphQL | None,
    synthesized_spec: SynthesizedSpec | None,
    action_correlation: ActionCorrelation | None,
    bundle_endpoint_count: int = 0,
) -> dict[str, object] | None:
    """Project a run's observed API surface to the §2h-shareable facts only.

    Mirrors the observability layer's §2h split. The published spec and GraphQL
    endpoint are non-sensitive and kept whole (kind/version/url, url/types), but
    the *synthesized* spec and action correlation are reduced to **counts only** —
    their templated paths (and the local-only ``doc_path``) can embed an
    un-clustered secret segment, so they never enter this shared surface at all.
    `bundle_endpoint_count` (§2b layer 6, closes #153) is the same count-only
    treatment, for the same reason, plus one more: a bundle-discovered candidate
    was never even fetched to confirm it is real. Returns None when nothing was
    observed, so a URL with no API surface stores nothing rather than an empty
    shell.
    """
    surface: dict[str, object] = {}
    if api_spec is not None:
        surface["spec"] = {
            "kind": api_spec.kind,
            "version": api_spec.version,
            "url": api_spec.url,
        }
    if graphql is not None:
        surface["graphql"] = {"url": graphql.url, "types": graphql.types}
    if synthesized_spec is not None:
        # Counts only — the templated endpoint paths and doc_path stay local (§2h).
        surface["synthesized"] = {
            "endpoint_count": synthesized_spec.endpoint_count,
            "request_count": synthesized_spec.request_count,
        }
    if action_correlation is not None:
        # Counts only — the per-action templated endpoints stay local (§2h).
        surface["correlation"] = {
            "action_count": action_correlation.action_count,
            "request_count": action_correlation.request_count,
        }
    if bundle_endpoint_count > 0:
        # Count only — the templated candidate paths stay local (§2h); every
        # candidate is unconfirmed by construction (never fetched to validate).
        surface["bundle_endpoints"] = {"endpoint_count": bundle_endpoint_count}
    return surface or None


def _action_label(action: ActionableElement) -> dict[str, str]:
    """A fired/discovered action as its accessibility role and name (both shared).

    Also carries `fill_value` when the action represents a scaffold-typed field
    (§2e issue #137) rather than a click, so a persisted-map round-trip preserves
    which transitions were reached by typing and what was typed. Kept raw/local
    like `name` already is — redaction happens at the wiki/testgen render boundary,
    not on the way into the local-only cache.
    """
    label = {"role": action.role, "name": action.name}
    if action.fill_value is not None:
        label["fill_value"] = action.fill_value
    return label


def _state_signal_counts(signals: StateSignals | None) -> dict[str, int] | None:
    """A state's free-signal bundle reduced to counts (§2h counts-only, like the
    synthesized API surface). The raw console/storage/network *values* captured at
    a state stay in the local-only cache; only their sizes are shareable here."""
    if signals is None:
        return None
    return {
        "ax_node_count": signals.ax_node_count,
        "console_count": len(signals.console_messages),
        "storage_count": len(signals.storage_keys),
        "network_count": len(signals.network_requests),
    }


def _transition_changes(signals: TransitionSignals | None) -> dict[str, object] | None:
    """What one fired action changed — the before/after signal diff. Unlike the
    per-state counts, this carries the actual *added* values (console lines, storage
    keys, request URLs), because "what did clicking X change" is the answer §2f
    exists to serve; each is a plain string that `map_view` redacts on the way out."""
    if signals is None:
        return None
    return {
        "ax_node_delta": signals.ax_node_delta,
        "console_added": list(signals.console_added),
        "storage_added": list(signals.storage_added),
        "storage_removed": list(signals.storage_removed),
        "network_added": list(signals.network_added),
        "screenshot_changed": signals.screenshot_changed,
    }


def shareable_exploration_map(
    graph: ExplorationGraph,
) -> dict[str, object] | None:
    """Project an exploration graph to the §2h-shareable facts for serving (§2f).

    Mirrors `shareable_api_surface`: a structural projection to plain
    strings/ints/bools/lists, so `map_view` can redact it wholesale on the way out
    (§2h) and both serving surfaces answer with the same shape. Per state: the
    abstract state id, its discovered action inventory (role + name), and its
    free-signal bundle as **counts only** (raw signal values stay local-only). Per
    transition: the from/to state ids, the action fired, and what it *changed* (the
    before/after signal diff — the "what happens when I click X" payload §2f exists
    to answer). Plus every action the safety gate skipped, with its reason, and the
    three counts. Returns None for an empty graph (nothing explored yet), so an
    unexplored URL stores nothing rather than an empty shell — the same "no shell"
    stance `shareable_api_surface` takes.
    """
    state_ids = graph.states
    if not state_ids:
        return None
    states = [
        {
            "id": node.state_id,
            "actions": [_action_label(a) for a in node.actions],
            "signals": _state_signal_counts(node.signals),
        }
        for node in (graph.node(sid) for sid in state_ids)
    ]
    transitions = [
        {
            "from": t.from_state,
            "action": _action_label(t.action),
            "to": t.to_state,
            "changed": _transition_changes(t.signals),
        }
        for t in graph.transitions
    ]
    skipped = [
        {"from": s.from_state, "action": _action_label(s.action), "reason": s.reason}
        for s in graph.skipped
    ]
    return {
        "states": states,
        "transitions": transitions,
        "skipped": skipped,
        "counts": {
            "states": len(states),
            "transitions": len(transitions),
            "skipped": len(skipped),
        },
    }

@dataclass(frozen=True)
class MapEntry:
    """One mapped URL: its extracted records, resolving tier, and capture time."""

    url: str
    domain: str
    records: list[dict[str, object]]
    tier: int | None
    captured_at: str  # ISO-8601 UTC, e.g. "2026-09-13T12:00:00+00:00"
    # The §2h-shareable projection of the run's observed API surface (spec whole,
    # synthesized/correlation as counts only), or None if nothing was observed.
    api_surface: dict[str, object] | None = None
    # The serialized ExtractionConfig this entry was produced from, kept so a
    # caller-forced recheck can re-run the exact same extraction (§2f). LOCAL-ONLY:
    # it is never projected into `map_view`, so it never reaches a served surface.
    config: dict[str, object] | None = None
    # The §2h-shareable projection of an exploration run's state-action graph (see
    # `shareable_exploration_map`), or None if the URL was mapped by extraction only.
    exploration: dict[str, object] | None = None


def _domain_of(url: str) -> str:
    """The network location (host[:port]) a URL maps under."""
    return urlsplit(url).netloc


def _get_or_create_site(conn: sqlite3.Connection, domain: str) -> int:
    """The `sites.id` for `domain`, inserting a row first if needed."""
    conn.execute("INSERT OR IGNORE INTO sites (domain) VALUES (?)", (domain,))
    (site_id,) = conn.execute(
        "SELECT id FROM sites WHERE domain = ?", (domain,)
    ).fetchone()
    return cast(int, site_id)


def _dump(value: dict[str, object] | None) -> str | None:
    return None if value is None else json.dumps(value)


def _load(value: str | None) -> dict[str, object] | None:
    return None if value is None else cast("dict[str, object]", json.loads(value))


class MapStore:
    """Read/write access to the persisted map (§2f), a single SQLite database.

    The cache root is read from `spoor.security.storage.CACHE_ROOT` at call time
    (not import), so a test's monkeypatch of it — or a future configurable base —
    takes effect without reconstructing the store. A fresh `sqlite3.Connection` is
    opened per call (never held across calls or shared across threads), matching
    this store's existing "open, do the one thing, close" posture — `spoor serve`
    may field concurrent requests, and SQLite connections aren't safe to share
    across threads.
    """

    @property
    def _db_path(self) -> Path:
        return storage.CACHE_ROOT / DB_FILENAME

    def _connect(self) -> sqlite3.Connection:
        path = self._db_path
        path.parent.mkdir(parents=True, exist_ok=True)
        # busy_timeout: `spoor serve` may field genuinely concurrent requests, each
        # opening its own connection (see the class docstring) — without this, a
        # writer that loses a race for SQLite's file lock gets an immediate
        # "database is locked" error instead of waiting briefly and retrying.
        # Deliberately NOT switching to WAL journal mode: that switch itself
        # requires an exclusive lock, so issuing it from every connection racing
        # to open a brand-new database file is a real deadlock-shaped bug, not a
        # hypothetical one — caught by this module's own concurrent-writer test.
        # WAL is a concurrent-reader-during-write performance optimization Spoor's
        # actual write pattern (occasional CLI runs, rare recheck calls) doesn't
        # need; the default rollback-journal mode plus busy_timeout is correct and
        # sufficient.
        conn = sqlite3.connect(path, timeout=5.0)
        conn.execute("PRAGMA busy_timeout = 5000")
        conn.execute("PRAGMA foreign_keys=ON")
        _migrate(conn)
        return conn

    def record(
        self,
        url: str,
        records: list[dict[str, object]],
        *,
        tier: int | None = None,
        captured_at: datetime | None = None,
        api_surface: dict[str, object] | None = None,
        config: dict[str, object] | None = None,
        exploration: dict[str, object] | None = None,
    ) -> MapEntry:
        """Remember a run's result for `url` so the API can serve it later.

        Inserted as a new row — `get()` still answers with only the *latest* one
        for the URL, so callers see the same "this run's result replaces what's
        served" behavior as before; the earlier row isn't deleted, it's simply
        not the one `get()` returns (real run history, not yet exposed through
        this interface — see the module docstring). Defaults the capture time to
        now (UTC). `api_surface` is the already-§2h-projected surface (see
        `shareable_api_surface`), or None. `config` is the serialized
        ExtractionConfig the result came from, kept local-only so a forced
        recheck can re-run the same extraction (§2f). `exploration` is the
        already-§2h-projected exploration graph (see `shareable_exploration_map`),
        or None for an extraction-only run.
        """
        domain = _domain_of(url)
        stamp = (captured_at or datetime.now(UTC)).isoformat()
        entry = MapEntry(
            url=url,
            domain=domain,
            records=records,
            tier=tier,
            captured_at=stamp,
            api_surface=api_surface,
            config=config,
            exploration=exploration,
        )
        conn = self._connect()
        try:
            with conn:
                site_id = _get_or_create_site(conn, domain)
                conn.execute(
                    "INSERT INTO runs (site_id, url, captured_at, tier,"
                    " records_json, api_surface_json, exploration_json,"
                    " config_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        site_id,
                        url,
                        stamp,
                        tier,
                        json.dumps(records),
                        _dump(api_surface),
                        _dump(exploration),
                        _dump(config),
                    ),
                )
        finally:
            conn.close()
        return entry

    def get(self, url: str) -> MapEntry | None:
        """The latest mapped entry for `url`, or None if it has never been mapped."""
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT sites.domain, runs.tier, runs.captured_at,"
                " runs.records_json, runs.api_surface_json,"
                " runs.exploration_json, runs.config_json"
                " FROM runs JOIN sites ON runs.site_id = sites.id"
                " WHERE runs.url = ?"
                " ORDER BY runs.captured_at DESC, runs.id DESC LIMIT 1",
                (url,),
            ).fetchone()
        finally:
            conn.close()
        if row is None:
            return None
        domain, tier, captured_at, records_json, surface_json, expl_json, cfg_json = (
            row
        )
        return MapEntry(
            url=url,
            domain=domain,
            records=cast("list[dict[str, object]]", json.loads(records_json)),
            tier=tier,
            captured_at=captured_at,
            api_surface=_load(surface_json),
            config=_load(cfg_json),
            exploration=_load(expl_json),
        )

    def domains(self) -> list[str]:
        """Every domain with at least one mapped URL, sorted."""
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT DISTINCT sites.domain FROM sites"
                " JOIN runs ON runs.site_id = sites.id"
                " ORDER BY sites.domain"
            ).fetchall()
        finally:
            conn.close()
        return [row[0] for row in rows]
