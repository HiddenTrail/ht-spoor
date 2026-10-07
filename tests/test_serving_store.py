"""Unit tests for the map store's shareable projections and SQLite backing
(ROADMAP.md §2f/§2h, closes #214).

The serving surfaces answer from projections built here, not from live objects, so
the projection is where the §2h split is enforced. `shareable_exploration_map`
mirrors `shareable_api_surface`: a pure structural reduction of an exploration graph
to plain strings/ints/bools that `map_view` can redact wholesale — per-state signals
as counts only (raw values stay local), per-transition the actual before/after diff
(the "what changed" §2f serves). These pin its shape and its empty-graph contract
directly, below the BDD scenarios.

The `MapStore`-specific tests below pin internal behavior the BDD scenarios in
`features/serving.feature`/`features/serving_mcp.feature` don't reach directly:
that run history is actually retained in the database (not just that `get()`
answers with the latest — the BDD recheck scenario already proves that), that the
migration runner is idempotent, and that concurrent writers from multiple threads
don't corrupt the database.
"""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Any

import pytest

from spoor.exploration.capture import StateSignals, TransitionSignals
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.graph import ExplorationGraph
from spoor.security import storage
from spoor.serving.store import MapStore, shareable_exploration_map


def test_empty_graph_projects_to_none() -> None:
    # An unexplored URL stores nothing rather than an empty shell — the same stance
    # shareable_api_surface takes when nothing was observed.
    assert shareable_exploration_map(ExplorationGraph()) is None


def _built_graph() -> ExplorationGraph:
    graph = ExplorationGraph()
    open_menu = ActionableElement(role="button", name="Open menu", backend_node_id=1)
    delete = ActionableElement(role="button", name="Delete", backend_node_id=2)
    graph.add_state(
        "s-home",
        [open_menu, delete],
        StateSignals(
            ax_node_count=7,
            console_messages=("boot", "ready"),
            storage_keys=("cartId",),
            network_requests=("GET /", "GET /app.js", "GET /api/me"),
        ),
    )
    graph.add_state("s-menu", [], StateSignals(ax_node_count=11))
    graph.add_transition(
        "s-home",
        open_menu,
        "s-menu",
        TransitionSignals(
            ax_node_delta=4,
            console_added=("opened",),
            storage_added=("menuOpen",),
            storage_removed=(),
            network_added=("GET /api/menu",),
            screenshot_changed=True,
        ),
    )
    graph.record_skip("s-home", delete, "destructive action skipped outside a sandbox")
    return graph


def test_projection_shape_states_transitions_skips_and_counts() -> None:
    projected: Any = shareable_exploration_map(_built_graph())
    assert projected is not None

    assert projected["counts"] == {"states": 2, "transitions": 1, "skipped": 1}

    states = projected["states"]
    assert [s["id"] for s in states] == ["s-home", "s-menu"]
    assert states[0]["actions"] == [
        {"role": "button", "name": "Open menu"},
        {"role": "button", "name": "Delete"},
    ]
    # Per-state signals are counts only — no raw console/storage/network values.
    assert states[0]["signals"] == {
        "ax_node_count": 7,
        "console_count": 2,
        "storage_count": 1,
        "network_count": 3,
    }

    (transition,) = projected["transitions"]
    assert transition["from"] == "s-home"
    assert transition["to"] == "s-menu"
    assert transition["action"] == {"role": "button", "name": "Open menu"}
    # The transition carries the actual diff — what clicking the action changed.
    assert transition["changed"] == {
        "ax_node_delta": 4,
        "console_added": ["opened"],
        "storage_added": ["menuOpen"],
        "storage_removed": [],
        "network_added": ["GET /api/menu"],
        "screenshot_changed": True,
    }

    (skip,) = projected["skipped"]
    assert skip["from"] == "s-home"
    assert skip["action"] == {"role": "button", "name": "Delete"}
    assert skip["reason"] == "destructive action skipped outside a sandbox"


def test_missing_signals_project_to_none_not_empty() -> None:
    # A graph built before signal capture was wired in (signals=None) must not
    # crash the projection; the per-state and per-transition signal slots are None.
    graph = ExplorationGraph()
    action = ActionableElement(role="link", name="Next", backend_node_id=1)
    graph.add_state("s-1", [action])  # signals default None
    graph.add_state("s-2", [])
    graph.add_transition("s-1", action, "s-2")  # signals default None

    projected: Any = shareable_exploration_map(graph)
    assert projected is not None
    assert projected["states"][0]["signals"] is None
    assert projected["transitions"][0]["changed"] is None


# --- MapStore: SQLite backing (closes #214) -------------------------------


@pytest.fixture
def store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> MapStore:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / ".spoor-cache")
    return MapStore()


def test_get_on_an_unmapped_url_returns_none(store: MapStore) -> None:
    # No database file exists yet at all -- must not raise, just report unmapped.
    assert store.get("https://shop.example/never-mapped") is None


def test_record_then_get_round_trips_every_field(store: MapStore) -> None:
    entry = store.record(
        "https://shop.example/p/1",
        [{"title": "Widget"}],
        tier=1,
        api_surface={"spec": {"kind": "openapi", "version": "3.0", "url": "x"}},
        config={"target": "https://shop.example/p/1"},
        exploration={"states": [], "transitions": [], "skipped": [], "counts": {}},
    )
    fetched = store.get("https://shop.example/p/1")
    assert fetched == entry
    assert fetched is not None
    assert fetched.domain == "shop.example"
    assert fetched.records == [{"title": "Widget"}]
    assert fetched.tier == 1
    assert fetched.api_surface == {
        "spec": {"kind": "openapi", "version": "3.0", "url": "x"}
    }
    assert fetched.config == {"target": "https://shop.example/p/1"}
    assert fetched.exploration == {
        "states": [],
        "transitions": [],
        "skipped": [],
        "counts": {},
    }


def test_record_retains_history_not_just_the_latest(store: MapStore) -> None:
    # get() answers with only the latest (features/serving.feature's force-recheck
    # scenario already pins that), but the earlier row must still be in the
    # database -- real history, the whole point of moving off the old
    # overwrite-only per-domain JSON file.
    store.record("https://shop.example/p/1", [{"title": "Widget v1"}])
    store.record("https://shop.example/p/1", [{"title": "Widget v2"}])
    conn = sqlite3.connect(storage.CACHE_ROOT / "spoor.db")
    try:
        (count,) = conn.execute(
            "SELECT COUNT(*) FROM runs WHERE url = ?", ("https://shop.example/p/1",)
        ).fetchone()
    finally:
        conn.close()
    assert count == 2
    assert store.get("https://shop.example/p/1").records == [{"title": "Widget v2"}]  # type: ignore[union-attr]


def test_domains_lists_every_distinct_domain_once(store: MapStore) -> None:
    store.record("https://shop.example/p/1", [{"title": "A"}])
    store.record("https://shop.example/p/2", [{"title": "B"}])
    store.record("https://other.example/x", [{"title": "C"}])
    assert store.domains() == ["other.example", "shop.example"]


def test_domains_on_an_empty_store_returns_empty_list(store: MapStore) -> None:
    assert store.domains() == []


def test_migration_runner_is_idempotent(store: MapStore) -> None:
    # Opening the database repeatedly (every MapStore call does) must not re-run
    # already-applied migrations or raise on a table that already exists.
    store.record("https://shop.example/p/1", [{"title": "A"}])
    store.record("https://shop.example/p/2", [{"title": "B"}])  # second _connect()
    assert store.get("https://shop.example/p/1") is not None
    assert store.get("https://shop.example/p/2") is not None


def test_concurrent_writers_do_not_corrupt_the_database(store: MapStore) -> None:
    # spoor serve may field concurrent requests (each recheck call writes); a
    # fresh connection per call plus busy_timeout must survive genuinely
    # concurrent writers without a "database is locked" error or lost writes.
    urls = [f"https://shop.example/p/{i}" for i in range(20)]

    def _record(url: str) -> None:
        store.record(url, [{"title": url}])

    threads = [threading.Thread(target=_record, args=(url,)) for url in urls]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    for url in urls:
        entry = store.get(url)
        assert entry is not None
        assert entry.records == [{"title": url}]
    assert len(store.domains()) == 1
