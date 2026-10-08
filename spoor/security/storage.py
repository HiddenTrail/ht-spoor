"""Local-only run cache for raw captures (ROADMAP.md §2h).

§2h non-negotiable: raw, unredacted captures (a full HAR, a full storage state)
stay in a local-only cache and never reach shared output without a separate,
explicit export step. This module owns *where* that cache lives — a per-run
subdirectory of a git-ignored cache root — and nothing more. It deliberately
does not touch the output pipeline, the wiki, or any MCP/API response: routing a
raw capture to a shared surface is the (not-yet-built) export action, not a side
effect of writing one here.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

#: The environment variable that sets where the local cache lives.
CACHE_DIR_ENV = "SPOOR_CACHE_DIR"


def cache_root_from(environ: Mapping[str, str]) -> Path:
    """The cache root an environment asks for: `SPOOR_CACHE_DIR` when set.

    Set and non-empty: that path (`~` expanded; a relative value is taken from
    the working directory). Otherwise `.spoor-cache` in the working directory,
    git-ignored. Either way the cache stays on this machine (§2h); this only
    says where. Decided in ROADMAP §2i (gui-4 mechanics): an MCP client
    launches `spoor serve-mcp` from a folder of its own choosing, and the GUI's
    MCP setup points it at the right maps through this variable.
    """
    value = environ.get(CACHE_DIR_ENV, "").strip()
    return Path(value).expanduser() if value else Path(".spoor-cache")


# The cache root, read once at start-up. Every store reads it at call time
# through this module, so tests redirect it by monkeypatching it.
CACHE_ROOT = cache_root_from(os.environ)

# The filename a run's captured HAR is written under, inside its run directory.
HAR_FILENAME = "network.har"

# The filename a run's captured console log (JSON Lines) is written under (§2c).
CONSOLE_FILENAME = "console.jsonl"

# The filename a run's accessibility-tree snapshots are written under (§2c).
ACCESSIBILITY_FILENAME = "accessibility.json"

# The filename a run's raw response headers are written under (§2c).
HEADERS_FILENAME = "headers.json"

# The filename a run's raw, unredacted client-side storage state is written
# under (§2c/§2h) — cookies + localStorage, all values.
STORAGE_STATE_FILENAME = "storage_state.json"

# The filename a run's static JS-bundle-discovered endpoint candidates are
# written under (§2b layer 6) — unconfirmed string matches, never fetched.
BUNDLE_ENDPOINTS_FILENAME = "bundle_endpoints.json"


def new_run_id() -> str:
    """A sortable, collision-resistant id for one run's cache subdirectory.

    A UTC timestamp keeps directories in run order for a human browsing the
    cache; the random suffix keeps two runs started in the same second apart.
    """
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    return f"{stamp}-{uuid4().hex[:8]}"


def new_run_cache_dir() -> Path:
    """Create and return a fresh, empty per-run cache directory under CACHE_ROOT.

    CACHE_ROOT is read at call time (not import), so a monkeypatch of it in a
    test takes effect here.
    """
    run_dir = CACHE_ROOT / new_run_id()
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir
