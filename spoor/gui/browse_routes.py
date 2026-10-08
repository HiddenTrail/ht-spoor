"""The GUI's folder browser: what "Browse…" buttons list (ROADMAP.md §2i).

A web page can't learn real paths from the operating system's own picker, so
"Browse…" opens a small browser in the page, fed by `GET /browse`. It answers
with one folder's subfolders (and, when picking a file, its `.yaml`/`.yml`
files), the folder's parent and, on Windows, the drives.

It lists names only, never file contents, and never writes: choosing "new
folder" just adds a name to the path, and Spoor creates the folder when a run
writes into it. Like every page it sits behind the access token, Host check and
same-site cookie, so another site can neither call it nor read its answer. It
isn't confined to the working folder (output may go anywhere the operator
likes); folder names are what a native dialog would show the same person.
"""

from __future__ import annotations

import os
import stat
import string
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query

from spoor.gui.configs import SUFFIXES

#: Most entries listed for one folder.
MAX_ENTRIES = 1000


def _hidden(entry: os.DirEntry[str]) -> bool:
    """Dot-named, or (on Windows) marked hidden or system, like AppData."""
    if entry.name.startswith("."):
        return True
    attributes = getattr(entry.stat(follow_symlinks=False), "st_file_attributes", 0)
    hidden_or_system = stat.FILE_ATTRIBUTE_HIDDEN | stat.FILE_ATTRIBUTE_SYSTEM
    return bool(attributes & hidden_or_system)


def _start(raw: str, workdir: Path) -> Path:
    """The folder to list: `raw` (relative to the working folder), or the nearest
    folder that exists above it; a file stands for its folder."""
    path = Path(os.path.abspath(workdir / Path(raw).expanduser())) if raw else workdir
    path = Path(os.path.abspath(path))
    while not path.exists() and path.parent != path:
        path = path.parent
    return path.parent if path.is_file() else path


def _drives() -> list[str]:
    if sys.platform != "win32":
        return []
    return [f"{d}:\\" for d in string.ascii_uppercase if os.path.exists(f"{d}:\\")]


def listing(raw: str, mode: str, workdir: Path) -> dict[str, Any]:
    """One folder's subfolders (and YAML files when `mode` is "file")."""
    folder = _start(raw, workdir)
    folders: list[dict[str, str]] = []
    files: list[dict[str, str]] = []
    error = None
    truncated = False
    try:
        with os.scandir(folder) as entries:
            for entry in sorted(entries, key=lambda e: e.name.lower()):
                if len(folders) + len(files) >= MAX_ENTRIES:
                    truncated = True
                    break
                try:
                    if _hidden(entry):
                        continue
                    if entry.is_dir():
                        folders.append({"name": entry.name, "path": entry.path})
                    elif mode == "file" and entry.name.lower().endswith(SUFFIXES):
                        files.append({"name": entry.name, "path": entry.path})
                except OSError:
                    continue
    except OSError:
        error = "This folder can't be opened."
    parent = folder.parent if folder.parent != folder else None
    return {
        "path": str(folder),
        "parent": str(parent) if parent else None,
        "separator": os.sep,
        "folders": folders,
        "files": files,
        "drives": _drives(),
        "truncated": truncated,
        "error": error,
    }


def add_browse_routes(app: FastAPI, *, workdir: Path) -> None:
    """Register `GET /browse` on `app`."""

    @app.get("/browse")
    def browse(
        path: str = Query(""), mode: str = Query("dir", pattern="^(dir|file|save)$")
    ) -> dict[str, Any]:
        return listing(path, mode, workdir)
