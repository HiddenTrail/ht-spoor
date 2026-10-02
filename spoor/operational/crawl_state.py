"""Resumable, persisted crawl frontier state (ROADMAP.md §2d, closes #175).

A `crawl:`-driven run (or a plain `pagination.next` chain) has no way to pick
up where an earlier run left off by default — every run starts its frontier
fresh from the target (plus sitemap seeds, if enabled). Opting in (`resume:
true` on the §2a config) persists exactly the two structures both tiers'
fetch loops already carry in memory — the `seen` set and the remaining
`frontier` — so the next run against the same target continues instead of
restarting.

This deliberately does **not** reuse §2e's exploration-mode `--resume-from`
machinery (`spoor/exploration/persisted_map.py`/`resume.py`): that is a
state-graph model built to resolve a named anchor *state* and re-drive a live
browser through a replay path to re-establish position — real complexity that
exists because exploration's unit of progress is a screen reached by a
sequence of actions. A crawl frontier has no actions, no states, no replay —
just URLs and depths — so none of that machinery applies. The right
precedent instead is `spoor/operational/change_detection.py:ChangeDetector`
and `spoor/core/fingerprint_cache.py:FingerprintCache`: a small per-domain
JSON store, loaded once at the start of a run and saved once at the end (in a
`finally`), a `_dirty`-flag-gated write that never raises on I/O failure, with
`storage.CACHE_ROOT` read at call time (not import time) so a test's
monkeypatch takes effect — the same contract every persistent store here
holds to.

Local-only (§2h): a URL only ever appears as runtime-discovered state, never a
source literal (§0's sanctioned "runtime-learned" exception, the same class as
the fingerprint cache and the change-detection store).
"""

from __future__ import annotations

import json
import re
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from spoor.security import storage

# Subdirectory of the cache root holding the persistent per-domain frontier
# stores. Read through `storage.CACHE_ROOT` at call time (see module docstring).
CRAWL_STATE_DIRNAME = "crawl_state"

# Anything outside this set is replaced in a netloc before it becomes a filename
# (a colon is invalid on Windows) — same pattern as the change-detection store.
_UNSAFE_FILENAME_CHARS = re.compile(r"[^A-Za-z0-9._-]")


@dataclass(frozen=True)
class FrontierState:
    """One target's persisted frontier: every URL already seen, and what's left.

    `seen` and `frontier` are stored as tuples (hashable, comparable) so two
    states can be compared by equality to decide whether anything changed.
    """

    seen: tuple[str, ...]
    frontier: tuple[tuple[str, int], ...]


class CrawlStateStore:
    """Per-domain, persistent frontier state for one target, keyed by its URL.

    One file per domain (several distinct crawl targets on the same domain
    share it, each under its own key — the same reason the exploration
    `MapStore` keys its per-domain file by URL), loaded on construction. A
    missing or corrupt file, or a malformed individual entry, yields an empty
    store rather than an error — a first run for this target, never a crash.
    """

    def __init__(self, path: Path, target: str) -> None:
        self._path = path
        self._target = target
        self._store: dict[str, FrontierState] = {}
        self._dirty = False
        self._load()

    def _load(self) -> None:
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return  # no store yet, or a corrupt one — start clean, never raise
        if not isinstance(raw, dict):
            return
        for url, entry in raw.items():
            state = _parse_entry(entry)
            if state is not None:
                self._store[url] = state

    def load(self) -> tuple[set[str], deque[tuple[str, int]]] | None:
        """This target's persisted `(seen, frontier)`, or None to start fresh.

        None means either nothing was ever recorded for this target, or its
        prior run's frontier finished naturally (`clear` removed the entry) —
        both cases a caller should seed its own fresh frontier for, same as
        `resume: false` always does.
        """
        state = self._store.get(self._target)
        if state is None:
            return None
        return set(state.seen), deque(state.frontier)

    def record(self, seen: set[str], frontier: Sequence[tuple[str, int]]) -> None:
        """Remember the current `(seen, frontier)` for this target, for next time.

        A no-op when it's identical to what's already stored. `seen` is sorted
        before storing so the comparison (and the written file) is stable
        rather than depending on set-iteration order.
        """
        entry = FrontierState(seen=tuple(sorted(seen)), frontier=tuple(frontier))
        if self._store.get(self._target) == entry:
            return
        self._store[self._target] = entry
        self._dirty = True

    def clear(self) -> None:
        """Forget this target's persisted state — its crawl finished naturally.

        A no-op if nothing was stored for it. Called once a run's frontier
        empties on its own, so a later run (resumed or not) starts fresh
        instead of finding an already-exhausted frontier forever.
        """
        if self._store.pop(self._target, None) is not None:
            self._dirty = True

    def save(self) -> None:
        """Persist the store to its file if anything changed; never raises."""
        if not self._dirty:
            return
        doc = {
            url: {
                "seen": list(state.seen),
                "frontier": [list(pair) for pair in state.frontier],
            }
            for url, state in self._store.items()
        }
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
            self._dirty = False
        except OSError:
            return


def _parse_entry(entry: object) -> FrontierState | None:
    """A validated `FrontierState` from one raw JSON entry, or None if malformed.

    Skips the single bad entry rather than failing the whole load — the same
    tolerant-degrade posture every persistent store here already takes.
    """
    if not isinstance(entry, dict):
        return None
    seen = entry.get("seen")
    frontier = entry.get("frontier")
    if not isinstance(seen, list) or not all(isinstance(s, str) for s in seen):
        return None
    if not isinstance(frontier, list):
        return None
    parsed: list[tuple[str, int]] = []
    for item in frontier:
        if (
            isinstance(item, list)
            and len(item) == 2
            and isinstance(item[0], str)
            and isinstance(item[1], int)
        ):
            parsed.append((item[0], item[1]))
        else:
            return None
    return FrontierState(seen=tuple(seen), frontier=tuple(parsed))


def store_path_for_target(target: str) -> Path:
    """The persistent frontier-store file for `target`'s domain, under the cache.

    Reads `storage.CACHE_ROOT` at call time (not import) so a test monkeypatch
    redirects it. The domain is the URL's netloc; a target with none falls back
    to a fixed name so the store still works for an odd input.
    """
    netloc = urlsplit(target).netloc or "_nohost"
    safe = _UNSAFE_FILENAME_CHARS.sub("_", netloc)
    return storage.CACHE_ROOT / CRAWL_STATE_DIRNAME / f"{safe}.json"


def crawl_state_for_target(target: str) -> CrawlStateStore:
    """The persistent frontier-resume store for `target` (§2d, §0)."""
    return CrawlStateStore(store_path_for_target(target), target)
