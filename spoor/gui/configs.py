"""Config files for the GUI's config editor (ROADMAP.md §2i, slice gui-3).

The editor works only on `.yaml`/`.yml` files inside the GUI's working folder,
never in hidden folders, the local cache, run output, or dependency folders, so
it can't be used to read or write arbitrary files. Every path a request names is
resolved and checked here before anything is opened. Checking a config uses
`load_config`, the exact loader `spoor run` uses, so "valid" in the GUI means
valid for the command.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml
from pydantic import ValidationError

from spoor.core.config import load_config

SUFFIXES = (".yaml", ".yml")
#: Folders never listed or opened (besides any hidden folder, e.g. .spoor-cache).
SKIP_DIRS = frozenset({"spoor-output", "node_modules", "venv", "__pycache__"})
MAX_DEPTH = 4
MAX_FILES = 200
#: Largest config the editor reads or writes.
MAX_BYTES = 1_000_000

#: What a new config starts as: the README's quickstart example.
STARTER = """\
# A Spoor extraction config. Change the target and selectors for your site.
target: https://example.com/products
item: "li.product-card"  # optional: one output record per match
fields:
  title: { selector: "h2.title" }               # element text (default)
  url:   { selector: "h2.title a", attr: href } # or an attribute value
  price: { selector: ".price", type: number }
pagination:
  next: "a.next-page"
"""


@dataclass(frozen=True)
class ConfigFile:
    """A config found in the working folder, and whether it validates."""

    path: str  # relative to the working folder, with forward slashes
    problems: int


def _allowed_parts(parts: tuple[str, ...]) -> bool:
    """No hidden folder or file, and no skipped folder, anywhere in the path."""
    return all(not p.startswith(".") and p not in SKIP_DIRS for p in parts)


def resolve(workdir: Path, relative: str) -> Path | None:
    """The config at `relative` inside `workdir`, or None if it isn't allowed.

    Allowed means: a `.yaml`/`.yml` name, resolving (symlinks followed) to a
    path inside the working folder, through no hidden or skipped folder. The
    file doesn't have to exist yet.
    """
    if not relative or not relative.lower().endswith(SUFFIXES):
        return None
    root = workdir.resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or target == root:
        return None
    if not _allowed_parts(target.relative_to(root).parts):
        return None
    return target


def check(text: str) -> list[str]:
    """Every problem with a config's text, each saying where; empty when valid."""
    try:
        load_config(text)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        problem = getattr(exc, "problem", None) or str(exc)
        if mark is not None:
            return [
                f"Not valid YAML on line {mark.line + 1}, column {mark.column + 1}: "
                f"{problem}"
            ]
        return [f"Not valid YAML: {problem}"]
    except ValidationError as exc:
        return [
            f"{'.'.join(str(p) for p in err['loc']) or 'the whole file'}: {err['msg']}"
            for err in exc.errors()
        ]
    return []


def read(path: Path) -> str:
    """A config's text, or raise ValueError if it can't be edited here safely.

    Too large, or not UTF-8 text: either way the editor refuses rather than show
    something that saving would then truncate or corrupt.
    """
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("This file is too large to edit here.")
    try:
        return path.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError(
            "This file isn't UTF-8 text, so it can't be edited here."
        ) from None


def write(path: Path, text: str) -> None:
    """Save a config, keeping the line-break style the file already has.

    A browser always submits a text area with CRLF line breaks, whatever the
    file used. They're normalized, then written back in the existing file's
    style (CRLF if it had any, else LF; LF for a new file). Otherwise merely
    opening and saving a file would rewrite every line ending, a whole-file
    change in version control with no real edit.
    """
    newline = "\n"
    if path.is_file() and b"\r\n" in path.read_bytes():
        newline = "\r\n"
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(normalized.replace("\n", newline))


def find(workdir: Path) -> list[ConfigFile]:
    """The configs in the working folder, sorted, each with its problem count."""
    root = workdir.resolve()
    found: list[ConfigFile] = []

    def walk(folder: Path, depth: int) -> None:
        try:
            entries = sorted(folder.iterdir())
        except OSError:
            return
        for entry in entries:
            if len(found) >= MAX_FILES:
                return
            if entry.name.startswith(".") or entry.name in SKIP_DIRS:
                continue
            if entry.is_dir() and not entry.is_symlink():
                if depth < MAX_DEPTH:
                    walk(entry, depth + 1)
            elif entry.suffix.lower() in SUFFIXES and entry.is_file():
                relative = entry.relative_to(root).as_posix()
                if resolve(root, relative) is None:
                    # E.g. a symlink pointing outside the folder: the editor
                    # would refuse it, so it isn't listed either.
                    continue
                try:
                    problems = len(check(read(entry)))
                except (OSError, ValueError):
                    problems = 1
                found.append(ConfigFile(relative, problems))

    walk(root, 1)
    return found
