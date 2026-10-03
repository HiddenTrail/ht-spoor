"""Typing-only consumption of a filled interactive-round scaffold (§2e, issue #131).

Issue #131 shipped scaffold *generation* only (`spoor/scaffold/interactive_config.py`).
This module is the first, deliberately narrow slice of *consuming* one: given a
scaffold a human has filled in, type its pinned — or, since #103, generated — values
into fields on the root state the crawl started from. Never presses Enter, never
clicks a submit control, never applies the value in any way — this stays entirely
inside the "types a scaffold's values into their fields" exception `docs/ROADMAP.md`
§2e records ahead of keyword-list localization (issue #101, now delivered).

A field's value comes from one of two places, in order: a non-blank `value:` the
operator typed in directly (always wins, never second-guessed), or — opt-in, only
when `generate: true` is also set on a blank-valued field — a freshly generated,
realistic-looking value from the Faker-backed generator seam
(`interactive_config.generate_value`, closes #103). Neither path is new scope beyond
what this module already did: a generated value is typed in exactly the same way,
through the same sandbox/safety gates, as a pinned one.

Restricted to the root state and to declared-sandbox targets only (§2e non-negotiable:
destructive-or-not, any interaction beyond passive observation is sandbox-only). A
field reached only by replaying prior navigation clicks is refused, never attempted —
even a click that only exists to *reach* a field is a click this module's "types a
value, clicks nothing else" contract cannot make. `spoor.exploration.graph.
paths_from_root` (the same reset-and-replay path `spoor/testgen/pytest_gen.py`'s
generated tests already replay) is used only to detect that case, never to actually
replay it.

After a successful fill, the resulting page is *observed* the same read-only way
exploration observes after any click — `discover_actions` + `capture_signals`, no new
mechanism (§2e issue #137) — and, if the value changed what's on screen, recorded as a
real graph edge: a new state and a transition whose `action.fill_value` marks it as
typed rather than clicked. This mutates the `graph` object passed in, in place, the
same way `explorer.walk()` mutates the graph it is given; persisting the enriched
graph and re-rendering the wiki from it is the caller's job (`spoor/cli.py`), not
this function's — `apply_scaffold` stays a pure-ish, driver-and-graph function a fast
test can exercise without any I/O.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import yaml

from spoor.exploration.capture import StateSignals, diff_signals
from spoor.exploration.discovery import ActionableElement, discover_actions
from spoor.exploration.explorer import ActionError
from spoor.exploration.graph import ExplorationGraph, paths_from_root
from spoor.exploration.safety import evaluate_action
from spoor.exploration.state import state_id as compute_state_id
from spoor.scaffold import interactive_config
from spoor.scaffold.interactive_config import FIELD_ROLES
from spoor.security.sandbox import is_sandbox


class ApplyDriver(Protocol):
    """What this module needs from a driver: reset, type, and observe the result.

    Deliberately narrower than the full `BrowserDriver` Protocol (`explorer.py`) —
    this never probes or clicks, so a driver or test fake doesn't need any of that to
    satisfy it, only the methods actually called here. `state_html`/`ax_nodes`/
    `capture_signals` are exactly the three the explorer itself calls to observe a
    state after firing an action (§2e issue #137) — reused, not reinvented, for
    observing the state a fill reveals.
    """

    def reset(self) -> None:
        """Return to the start state (e.g. re-navigate to the entry URL)."""
        ...

    def fill(self, action: ActionableElement, value: str) -> None:
        """Type `value` into `action`'s field. Never submits, never clicks elsewhere."""
        ...

    def state_html(self) -> str:
        """The current DOM, for computing the abstract state id after a fill."""
        ...

    def ax_nodes(self) -> Sequence[Mapping[str, object]]:
        """The current accessibility-tree nodes, for discovering the fill result."""
        ...

    def capture_signals(self) -> StateSignals:
        """The free-signal bundle for the current state, before and after a fill."""
        ...


@dataclass(frozen=True)
class FieldToApply:
    """One scaffold `fields:` entry ready to type in — pinned or generated."""

    state: str
    name: str
    value: str
    generated: bool = False


@dataclass(frozen=True)
class AppliedField:
    """A field that was successfully typed into."""

    state: str
    name: str
    generated: bool = False


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
    """Every `fields:` entry ready to apply — pinned or generated — plus any invalid.

    A non-blank `value:` always wins and is used as-is, exactly as before #103: a
    pinned literal is an explicit operator decision, never second-guessed by the
    generator seam even when `generate: true` is also set on the same entry.

    A blank `value:` with `generate: true` (closes #103, opt-in — unset or `false`
    behaves exactly as before #103) asks the generator seam for a fresh value keyed
    by the entry's `kind:`. A `kind` the seam can't generate for (e.g. `choice`,
    `unknown`, or a `kind` missing/malformed) is reported as a `FailedField`, not
    silently skipped — `generate: true` was an explicit ask, so failing to honor it
    is not the same "user chose not to fill this in" outcome a plain blank value is.

    A blank `value:` with no `generate: true` means the user chose not to fill this
    one in; skipped silently, not an error — unchanged from before #103. A malformed
    entry (missing `state`/`name`, or either not a string) is skipped the same way —
    this stays a best-effort reader of a hand-edited file, never a strict parser
    that crashes on one bad row.

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
        if value is not None and value != "":
            if not isinstance(value, str):
                invalid.append(
                    FailedField(state, name, "value must be a quoted YAML string")
                )
                continue
            ready.append(FieldToApply(state=state, name=name, value=value))
            continue
        if entry.get("generate") is not True:
            continue
        kind = entry.get("kind")
        generated = (
            interactive_config.generate_value(kind) if isinstance(kind, str) else None
        )
        if generated is None:
            invalid.append(
                FailedField(
                    state, name, f"no generator available for kind {kind!r}"
                )
            )
            continue
        ready.append(
            FieldToApply(state=state, name=name, value=generated, generated=True)
        )
    return ready, invalid


def _observe_and_merge(
    driver: ApplyDriver,
    graph: ExplorationGraph,
    from_state: str,
    filled_action: ActionableElement,
    before: StateSignals,
) -> str:
    """Record what a fill revealed as a real graph edge, and return the landed state.

    Mirrors the explorer's own after-action observation (`explorer.py`'s `walk`):
    compute the new state id, add it (with its discovered actions and signals) if the
    graph hasn't seen it before, and add a transition for it if this exact hop isn't
    already recorded — idempotent, so re-running `apply_scaffold` with an unchanged
    scaffold against an unchanged target adds nothing a second time. `filled_action`
    already carries `fill_value` (set by the caller), so the added transition is
    self-marking: any consumer can tell it apart from a clicked one without guessing.
    An unchanged state (the fill had no observable effect) adds nothing at all — the
    same "nothing new is written" outcome as before, now reached by comparison rather
    than by never observing in the first place.
    """
    landed = compute_state_id(driver.state_html())
    after = driver.capture_signals()
    if not graph.has_state(landed):
        graph.add_state(landed, discover_actions(driver.ax_nodes()), after)
    if landed == from_state:
        return landed
    already_recorded = any(
        t.from_state == from_state
        and t.action.role == filled_action.role
        and t.action.name == filled_action.name
        and t.action.fill_value == filled_action.fill_value
        and t.to_state == landed
        for t in graph.transitions
    )
    if not already_recorded:
        graph.add_transition(
            from_state, filled_action, landed, diff_signals(before, after)
        )
    return landed


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
        # Tracks where the driver actually is as fills within this group chain
        # (§2e issue #137): each field is matched against the *current* page's own
        # action inventory, not the group's original state, since an earlier fill in
        # this same group may already have revealed a new one.
        current_state = state_id
        for field in group_fields:
            matches = [
                a
                for a in graph.node(current_state).actions
                if a.name == field.name and a.role in FIELD_ROLES
            ]
            if not matches:
                failed.append(
                    FailedField(
                        current_state, field.name, "no matching field on this state"
                    )
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
                failed.append(FailedField(current_state, field.name, decision.reason))
                continue
            before = driver.capture_signals()
            try:
                driver.fill(target_action, field.value)
            except ActionError as exc:
                failed.append(FailedField(current_state, field.name, str(exc)))
                continue
            applied.append(
                AppliedField(current_state, field.name, generated=field.generated)
            )
            filled_action = ActionableElement(
                role=target_action.role,
                name=target_action.name,
                backend_node_id=None,
                fill_value=field.value,
            )
            current_state = _observe_and_merge(
                driver, graph, current_state, filled_action, before
            )
    return applied, failed
