"""Operator-supplied exploration hooks (ROADMAP.md §2e, closes #187).

Part 2 of #150: a way to extend an exploration run — observe a newly
discovered state, observe a fired transition — without writing site-specific
code into Spoor itself. Hooks are plain Python callables, supplied at the
same injection seam `explore()`'s existing `progress` parameter already uses
(`explore(..., hooks=...)`), not a config/CLI flag, since a hook is code the
operator brings.

Two safety properties hold by construction, not by convention:

- A hook can never drive or influence a new interaction. Both hooks fire only
  *after* the state/transition they describe is already committed to the
  graph and the §2e destructive-action gate (`evaluate_action`) has already
  been fully consumed for that action — `explore()`'s walk never reads a
  hook's return value or inspects it for side effects, so there is no path
  from a hook back into which actions get attempted.
- A hook never sees a raw, unredacted signal. `on_state_discovered`/
  `on_transition_taken` receive `ExploredState`/`ExploredTransition` — built
  fresh here from the graph's `StateSignals`/`TransitionSignals`, never those
  dataclasses themselves — carrying only counts and `redact()`-passed text,
  the same primitive §2h's shared-output paths (the wiki, the MCP/API layer)
  already use. This is deliberately independent of `spoor/exploration/
  wiki.py`'s own per-state/per-transition view builders (reusing them would
  mean calling mid-walk into code shaped and tested for a one-shot, end-of-run
  render) — a small amount of parallel logic, in exchange for zero regression
  risk to the existing wiki output.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from spoor.exploration.capture import StateSignals, TransitionSignals
from spoor.exploration.discovery import ActionableElement
from spoor.security.redaction import redact


@dataclass(frozen=True)
class ExploredState:
    """A newly discovered state, redaction-safe (ROADMAP.md §2e, #187).

    `actions` are `(role, name)` pairs — the same accessible name the safety
    gate itself classifies on, already a label meant to be visible, not a
    captured value. `signal_counts` is `None` when the state carried no
    signal bundle (signals aren't always captured); otherwise counts only —
    never the console lines, storage keys, or network requests themselves.
    """

    state_id: str
    actions: tuple[tuple[str, str], ...]
    signal_counts: SignalCounts | None


@dataclass(frozen=True)
class SignalCounts:
    """Counts-only summary of a `StateSignals` bundle — no raw values."""

    ax_node_count: int
    console_count: int
    storage_count: int
    network_count: int


@dataclass(frozen=True)
class ExploredTransition:
    """A fired, already-recorded transition, redaction-safe (ROADMAP.md §2e, #187).

    `changed` summarizes what the action's before/after diff showed: a count
    of each additive signal, plus the console/storage-key lines themselves —
    `redact()`-passed, never raw — since what specifically newly appeared
    (not just how much) is the whole point of a transition diff. Network
    requests are counted only, matching the wiki's own treatment of them
    (bucketed by kind there; a bare count here, no URLs).
    """

    from_state: str
    action_role: str
    action_name: str
    to_state: str
    recovered_via: str | None
    changed: ChangeSummary | None


@dataclass(frozen=True)
class ChangeSummary:
    """Counts-only, redacted-text summary of a `TransitionSignals` diff."""

    ax_node_delta: int
    console_added: tuple[str, ...]
    storage_added: tuple[str, ...]
    storage_removed: tuple[str, ...]
    network_added_count: int
    screenshot_changed: bool


def build_explored_state(
    state_id: str, actions: list[ActionableElement], signals: StateSignals | None
) -> ExploredState:
    counts = (
        None
        if signals is None
        else SignalCounts(
            ax_node_count=signals.ax_node_count,
            console_count=len(signals.console_messages),
            storage_count=len(signals.storage_keys),
            network_count=len(signals.network_requests),
        )
    )
    return ExploredState(
        state_id=state_id,
        actions=tuple((a.role, a.name) for a in actions),
        signal_counts=counts,
    )


def build_explored_transition(
    from_state: str,
    action: ActionableElement,
    to_state: str,
    recovered_via: str | None,
    signals: TransitionSignals | None,
) -> ExploredTransition:
    changed = (
        None
        if signals is None
        else ChangeSummary(
            ax_node_delta=signals.ax_node_delta,
            console_added=tuple(redact(line) for line in signals.console_added),
            storage_added=tuple(redact(key) for key in signals.storage_added),
            storage_removed=tuple(redact(key) for key in signals.storage_removed),
            network_added_count=len(signals.network_added),
            screenshot_changed=signals.screenshot_changed,
        )
    )
    return ExploredTransition(
        from_state=from_state,
        action_role=action.role,
        action_name=action.name,
        to_state=to_state,
        recovered_via=recovered_via,
        changed=changed,
    )


#: Called once per newly discovered state, after it is already in the graph.
OnStateDiscovered = Callable[[ExploredState], None]

#: Called once per newly recorded transition, after it is already in the graph.
OnTransitionTaken = Callable[[ExploredTransition], None]


@dataclass
class ExplorationHooks:
    """The hooks an exploration run was supplied, if any. Omitted fields do nothing."""

    on_state_discovered: OnStateDiscovered | None = None
    on_transition_taken: OnTransitionTaken | None = None
