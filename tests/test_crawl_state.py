"""Unit tests for the resumable crawl frontier store (ROADMAP.md §2d, #175).

The `.feature` scenarios exercise resume end-to-end through two real crawl
runs; these probe `CrawlStateStore` directly — load/record/clear, per-target
keying within a shared per-domain file, and the edge cases (a corrupt store,
a malformed entry, multiple targets sharing one domain) that must degrade to
"nothing to resume", never crash a run.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from spoor.operational.crawl_state import (
    CrawlStateStore,
    FrontierState,
    crawl_state_for_target,
    store_path_for_target,
)
from spoor.security import storage

_URL = "http://localhost:8000/catalog.html"
_OTHER_URL = "http://localhost:8000/other.html"


@pytest.fixture
def store(tmp_path: Path) -> CrawlStateStore:
    return CrawlStateStore(tmp_path / "store.json", _URL)


def test_a_first_run_has_nothing_to_resume(store: CrawlStateStore) -> None:
    assert store.load() is None


def test_recorded_state_is_returned_by_load(store: CrawlStateStore) -> None:
    store.record({_URL, "http://localhost:8000/a"}, [("http://localhost:8000/b", 1)])
    seen, frontier = store.load()  # type: ignore[misc]
    assert seen == {_URL, "http://localhost:8000/a"}
    assert list(frontier) == [("http://localhost:8000/b", 1)]


def test_clear_removes_this_target_only(tmp_path: Path) -> None:
    # Sequential instances, each reloading the current file -- the realistic
    # access pattern (one `CrawlStateStore` per run, never two held open
    # concurrently against the same path), not two in-memory instances
    # independently overwriting a file neither has the other's latest write.
    path = tmp_path / "store.json"
    first = CrawlStateStore(path, _URL)
    first.record({_URL}, [("http://localhost:8000/next", 1)])
    first.save()

    second = CrawlStateStore(path, _OTHER_URL)
    second.record({_OTHER_URL}, [("http://localhost:8000/other-next", 1)])
    second.save()

    third = CrawlStateStore(path, _URL)
    third.clear()
    third.save()

    assert CrawlStateStore(path, _URL).load() is None
    # The other target on the same domain's file is untouched.
    assert CrawlStateStore(path, _OTHER_URL).load() is not None


def test_the_store_persists_across_instances(tmp_path: Path) -> None:
    path = tmp_path / "store.json"
    first = CrawlStateStore(path, _URL)
    first.record({_URL}, [("http://localhost:8000/next", 1)])
    first.save()

    reopened = CrawlStateStore(path, _URL)
    seen, frontier = reopened.load()  # type: ignore[misc]
    assert seen == {_URL}
    assert list(frontier) == [("http://localhost:8000/next", 1)]


def test_save_is_a_noop_when_nothing_was_recorded(tmp_path: Path) -> None:
    path = tmp_path / "store.json"
    CrawlStateStore(path, _URL).save()
    assert not path.exists()  # never write an empty store / create the dir for nothing


def test_record_is_dirty_only_on_a_real_change(tmp_path: Path) -> None:
    path = tmp_path / "store.json"
    store = CrawlStateStore(path, _URL)
    store.record({_URL}, [("http://localhost:8000/next", 1)])
    store.save()
    mtime = path.stat().st_mtime_ns

    # Recording the identical state again is a no-op, so save writes nothing.
    store.record({_URL}, [("http://localhost:8000/next", 1)])
    store.save()
    assert path.stat().st_mtime_ns == mtime


def test_clear_on_an_absent_target_is_a_noop(store: CrawlStateStore) -> None:
    store.clear()
    store.save()
    assert store.load() is None


def test_a_corrupt_store_loads_empty_rather_than_raising(tmp_path: Path) -> None:
    path = tmp_path / "store.json"
    path.write_text("{not valid json", encoding="utf-8")
    store = CrawlStateStore(path, _URL)  # must not raise
    assert store.load() is None


def test_a_malformed_entry_is_skipped(tmp_path: Path) -> None:
    path = tmp_path / "store.json"
    # One good entry, one with a non-list "seen" — the bad one is dropped, the
    # good one still loads (a hand-edited or truncated store never fails a run).
    path.write_text(
        '{"'
        + _URL
        + '": {"seen": ["' + _URL + '"], "frontier": [["http://x/n", 1]]}, '
        '"' + _OTHER_URL + '": {"seen": "not-a-list", "frontier": []}}',
        encoding="utf-8",
    )
    good = CrawlStateStore(path, _URL)
    bad = CrawlStateStore(path, _OTHER_URL)
    good_seen, good_frontier = good.load()  # type: ignore[misc]
    assert good_seen == {_URL}
    assert list(good_frontier) == [("http://x/n", 1)]
    assert bad.load() is None


def test_store_path_is_per_domain_under_the_cache_root(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / "cache")
    path = store_path_for_target(_URL)
    assert path.parent == tmp_path / "cache" / "crawl_state"
    assert path.name == "localhost_8000.json"  # colon sanitized for Windows


def test_crawl_state_for_target_is_local_only_under_the_cache_root(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(storage, "CACHE_ROOT", tmp_path / "cache")
    store = crawl_state_for_target(_URL)
    assert isinstance(store, CrawlStateStore)


def test_frontier_state_equality_backs_the_noop() -> None:
    # The record no-op relies on value equality of the frozen dataclass.
    a = FrontierState(seen=("x",), frontier=(("y", 0),))
    b = FrontierState(seen=("x",), frontier=(("y", 0),))
    assert a == b
