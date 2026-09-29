"""Typing-only consumption of a filled interactive-round scaffold (§2e, issue #131).

Issue #131 shipped scaffold *generation* only (`spoor/scaffold/interactive_config.py`).
This module is the first, deliberately narrow slice of *consuming* one: given a
scaffold a human has filled in, navigate to each field's recorded state and type its
pinned value in. Never presses Enter, never clicks a submit control, never applies the
value in any way — this stays entirely inside the "types a scaffold's pinned values
into their fields" exception `docs/ROADMAP.md` §2e records ahead of keyword-list
localization (issue #101). Applying a value is still fully gated on #101 and the
separate "how a filled field's value gets applied" open question.

Navigation reuses two already-public, already-proven pieces rather than inventing a new
"go to this state" primitive: `spoor.exploration.graph.paths_from_root` (the same
reset-and-replay path `spoor/testgen/pytest_gen.py`'s generated tests already replay)
gives the path of actions from the root to any mapped state, and `driver.perform` fires
each step exactly as exploration itself does. Nothing here crawls or discovers a new
state — it only replays a path already recorded in the graph, then types into one
field on the state it lands on.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import yaml

from spoor.exploration.discovery import ActionableElement
from spoor.exploration.explorer import ActionError
from spoor.exploration.graph import ExplorationGraph, paths_from_root
from spoor.scaffold.interactive_config import FIELD_ROLES


class ApplyDriver(Protocol):
    """What this module needs from a driver: replay a path, then type into a field.

    Deliberately narrower than the full `BrowserDriver` Protocol (`explorer.py`) —
    this never discovers, probes, or reads signals, so a driver or test fake doesn't
    need any of that to satisfy it, only the three methods actually called here.
    """

    def reset(self) -> None:
        """Return to the start state (e.g. re-navigate to the entry URL)."""
        ...

    def perform(self, action: ActionableElement) -> None:
        """Fire an action (e.g. click the element it names), replaying a path step."""
        ...

    def fill(self, action: ActionableElement, value: str) -> None:
        """Type `value` into `action`'s field. Never submits, never clicks elsewhere."""
        ...


@dataclass(frozen=True)
class FieldToApply:
    """One scaffold `fields:` entry with a non-blank value, ready to type in."""

    state: str
    name: str
    value: str


@dataclass(frozen=True)
class AppliedField:
    """A field that was successfully typed into."""

    state: str
    name: str


@dataclass(frozen=True)
class FailedField:
    """A field that could not be applied, and why — never a silent skip."""

    state: str
    name: str
    reason: str


def load_scaffold(path: Path) -> dict[str, Any]:
    """Parse a scaffold YAML file back into a dict (the inverse of `build_scaffold`).

    A malformed or non-mapping document parses to an empty dict rather than raising,
    so `applicable_fields` on it simply finds nothing to apply — the same "nothing to
    do" outcome an empty scaffold gives, not a crash on a file a human hand-edited.
    """
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def applicable_fields(scaffold: dict[str, Any]) -> list[FieldToApply]:
    """Every `fields:` entry with a non-blank value — pure, no I/O.

    A blank or missing `value:` means the user chose not to fill this one in; skipped
    silently, not an error. A malformed entry (missing `state`/`name`, or either not a
    string) is skipped the same way — this stays a best-effort reader of a hand-edited
    file, never a strict parser that crashes on one bad row.
    """
    fields = scaffold.get("fields")
    if not isinstance(fields, list):
        return []
    result: list[FieldToApply] = []
    for entry in fields:
        if not isinstance(entry, dict):
            continue
        state, name, value = entry.get("state"), entry.get("name"), entry.get("value")
        if not isinstance(state, str) or not isinstance(name, str):
            continue
        if not isinstance(value, str) or not value:
            continue
        result.append(FieldToApply(state=state, name=name, value=value))
    return result


def _resolve_state(graph: ExplorationGraph, prefix: str) -> str | None:
    """The one state id `prefix` matches, or None on zero or more than one match.

    Never guesses: an ambiguous or unresolved prefix is the caller's problem to report,
    the same posture `spoor/exploration/selector.py` already takes for `id:` selectors.
    """
    matches = [state_id for state_id in graph.states if state_id.startswith(prefix)]
    return matches[0] if len(matches) == 1 else None


def apply_scaffold(
    driver: ApplyDriver, graph: ExplorationGraph, scaffold: dict[str, Any]
) -> tuple[list[AppliedField], list[FailedField]]:
    """Type each applicable field's pinned value in. Never submits, never clicks
    anything beyond what typing itself requires (focusing the field).

    One field's failure — an unresolved state prefix, a field no longer on that state,
    a vanished or covered element — is recorded and the rest still run, mirroring the
    explorer's own skip-and-continue posture rather than aborting the whole pass on one
    bad entry. Nothing here raises for a single field; only a genuinely broken `graph`/
    `scaffold` argument would. Two fields sharing the same name on the same state (rare
    — e.g. a repeated "Notes" box) are not disambiguated: the first matching action on
    that state is used, not reported ambiguous the way an unresolved *state* prefix is.
    """
    paths = paths_from_root(graph)
    applied: list[AppliedField] = []
    failed: list[FailedField] = []
    for field in applicable_fields(scaffold):
        state_id = _resolve_state(graph, field.state)
        if state_id is None:
            failed.append(
                FailedField(
                    field.state,
                    field.name,
                    "state prefix did not resolve to exactly one mapped state",
                )
            )
            continue
        path = paths.get(state_id)
        if path is None:
            failed.append(
                FailedField(state_id, field.name, "no path from the root to this state")
            )
            continue
        driver.reset()
        for step in path:
            driver.perform(step)
        matches = [
            a
            for a in graph.node(state_id).actions
            if a.name == field.name and a.role in FIELD_ROLES
        ]
        if not matches:
            failed.append(
                FailedField(state_id, field.name, "no matching field on this state")
            )
            continue
        try:
            driver.fill(matches[0], field.value)
        except ActionError as exc:
            failed.append(FailedField(state_id, field.name, str(exc)))
            continue
        applied.append(AppliedField(state_id, field.name))
    return applied, failed
