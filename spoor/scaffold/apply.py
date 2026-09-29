"""Typing-only consumption of a filled interactive-round scaffold (§2e, issue #131).

Issue #131 shipped scaffold *generation* only (`spoor/scaffold/interactive_config.py`).
This module is the first, deliberately narrow slice of *consuming* one: given a
scaffold a human has filled in, type its pinned values into fields on the root state
the crawl started from. Never presses Enter, never clicks a submit control, never
applies the value in any way — this stays entirely inside the "types a scaffold's
pinned values into their fields" exception `docs/ROADMAP.md` §2e records ahead of
keyword-list localization (issue #101). Applying a value is still fully gated on #101
and the separate "how a filled field's value gets applied" open question.

Restricted to the root state and to declared-sandbox targets only (§2e non-negotiable:
destructive-or-not, any interaction beyond passive observation is sandbox-only). A
field reached only by replaying prior navigation clicks is refused, never attempted —
even a click that only exists to *reach* a field is a click this module's "types a
value, clicks nothing else" contract cannot make. `spoor.exploration.graph.
paths_from_root` (the same reset-and-replay path `spoor/testgen/pytest_gen.py`'s
generated tests already replay) is used only to detect that case, never to actually
replay it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import yaml

from spoor.exploration.discovery import ActionableElement
from spoor.exploration.explorer import ActionError
from spoor.exploration.graph import ExplorationGraph, paths_from_root
from spoor.exploration.safety import evaluate_action
from spoor.scaffold.interactive_config import FIELD_ROLES
from spoor.security.sandbox import is_sandbox


class ApplyDriver(Protocol):
    """What this module needs from a driver: reset to the entry URL, then type.

    Deliberately narrower than the full `BrowserDriver` Protocol (`explorer.py`) —
    this never discovers, probes, reads signals, or clicks anything, so a driver or
    test fake doesn't need any of that to satisfy it, only the two methods actually
    called here.
    """

    def reset(self) -> None:
        """Return to the start state (e.g. re-navigate to the entry URL)."""
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


def applicable_fields(
    scaffold: dict[str, Any],
) -> tuple[list[FieldToApply], list[FailedField]]:
    """Every `fields:` entry with a non-blank value, plus any entry that is invalid.

    A blank or missing `value:` means the user chose not to fill this one in; skipped
    silently, not an error. A malformed entry (missing `state`/`name`, or either not a
    string) is skipped the same way — this stays a best-effort reader of a hand-edited
    file, never a strict parser that crashes on one bad row.

    A `value:` that parsed as something other than a string — e.g. an unquoted `42`,
    which YAML reads as an integer — is different: it *was* an attempt to fill the
    field in, so it is reported as a `FailedField`, not silently dropped, with guidance
    to quote it.
    """
    fields = scaffold.get("fields")
    if not isinstance(fields, list):
        return [], []
    ready: list[FieldToApply] = []
    invalid: list[FailedField] = []
    for entry in fields:
        if not isinstance(entry, dict):
            continue
        state, name, value = entry.get("state"), entry.get("name"), entry.get("value")
        if not isinstance(state, str) or not isinstance(name, str):
            continue
        if value is None or value == "":
            continue
        if not isinstance(value, str):
            invalid.append(
                FailedField(state, name, "value must be a quoted YAML string")
            )
            continue
        ready.append(FieldToApply(state=state, name=name, value=value))
    return ready, invalid


def _resolve_state(graph: ExplorationGraph, prefix: str) -> str | None:
    """The one state id `prefix` matches, or None on zero or more than one match.

    Never guesses: an ambiguous or unresolved prefix is the caller's problem to report,
    the same posture `spoor/exploration/selector.py` already takes for `id:` selectors.
    """
    matches = [state_id for state_id in graph.states if state_id.startswith(prefix)]
    return matches[0] if len(matches) == 1 else None


def apply_scaffold(
    driver: ApplyDriver,
    graph: ExplorationGraph,
    scaffold: dict[str, Any],
    *,
    target: str,
    declared_sandbox: bool = False,
) -> tuple[list[AppliedField], list[FailedField]]:
    """Type each applicable field's pinned value in. Never submits, never clicks
    anything beyond what typing itself requires (focusing the field).

    Sandbox-gated, matching the §2e non-negotiable that any interaction beyond passive
    observation is sandbox-only: `target` must resolve to a registry sandbox match
    (`is_sandbox`) before the driver is touched at all. Against anything else, nothing
    is applied and the driver is never reset — the same "always skipped and logged"
    posture the exploration-mode destructive-action gate already takes, not a
    config-flag-relaxable exception.

    Restricted to the root state: a field reached only by replaying prior navigation
    clicks is refused, not attempted — the "types a value, never clicks anything else"
    exception this module lives inside is written against a session that clicks nothing
    but the field itself, and replaying a path to get there would break that. Fields on
    the root state (an empty path) are the only ones this can type into today.

    Fields on the same resolved state share one `driver.reset()` — typing into one
    field must not blow away a value already typed into another field on the same page.
    A reset failure fails every field in that group (the page was never reached, so
    none of them could be typed into) without aborting other groups' fields.

    One field's failure — an unresolved state prefix, a field no longer on that state,
    a vanished or covered element — is recorded and the rest still run, mirroring the
    explorer's own skip-and-continue posture rather than aborting the whole pass on one
    bad entry. Two fields sharing the same name on the same state (rare — e.g. a
    repeated "Notes" box) are not disambiguated: the first matching action on that
    state is used, not reported ambiguous the way an unresolved *state* prefix is.

    Every field also passes the same `evaluate_action` gate exploration itself uses
    (docs/ROADMAP.md #134) before it is filled — belt-and-suspenders alongside the
    `is_sandbox` check above: `evaluate_action` alone would allow any field whose name
    doesn't match a destructive keyword even outside a sandbox, so the up-front check
    is still required, but a field oddly labelled "Delete" is still refused here too,
    the same as it would be during exploration.
    """
    ready, failed = applicable_fields(scaffold)

    if not is_sandbox(target, declared=declared_sandbox):
        for field in ready:
            failed.append(
                FailedField(field.state, field.name, "target is not a declared sandbox")
            )
        return [], failed

    paths = paths_from_root(graph)
    applied: list[AppliedField] = []
    groups: dict[str, list[FieldToApply]] = {}
    for field in ready:
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
        if path:
            failed.append(
                FailedField(
                    state_id,
                    field.name,
                    "navigation replay is outside the typing-only scope",
                )
            )
            continue
        groups.setdefault(state_id, []).append(field)

    for state_id, group_fields in groups.items():
        try:
            driver.reset()
        except ActionError as exc:
            for field in group_fields:
                failed.append(FailedField(state_id, field.name, str(exc)))
            continue
        node = graph.node(state_id)
        for field in group_fields:
            matches = [
                a
                for a in node.actions
                if a.name == field.name and a.role in FIELD_ROLES
            ]
            if not matches:
                failed.append(
                    FailedField(state_id, field.name, "no matching field on this state")
                )
                continue
            target_action = matches[0]
            decision = evaluate_action(
                target,
                field.name,
                role=target_action.role,
                declared_sandbox=declared_sandbox,
            )
            if not decision.allowed:
                failed.append(FailedField(state_id, field.name, decision.reason))
                continue
            try:
                driver.fill(target_action, field.value)
            except ActionError as exc:
                failed.append(FailedField(state_id, field.name, str(exc)))
                continue
            applied.append(AppliedField(state_id, field.name))
    return applied, failed
