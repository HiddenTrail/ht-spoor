"""Step definitions for features/exploration_visual_identity.feature (§9, #104).

Same `_FakeApp`/`_FakeDriver` shape `test_exploration_loop_steps.py` uses (each
step-def file keeps its own self-contained fake, the established pattern in this
test suite), extended with a per-state queue of screenshot hashes to return from
successive `capture_signals()` calls, and a capture-call counter to pin the "a
revisit costs exactly one extra capture" cost model directly.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping, Sequence
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.actuation import ActuationVerdict, Verdict
from spoor.exploration.capture import StateSignals
from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.explorer import explore

scenarios("exploration_visual_identity.feature")


class _FakeApp:
    """A deterministic state machine described by the scenario's transition table."""

    def __init__(self) -> None:
        self.root = ""
        self._actions: dict[str, list[ActionableElement]] = {}
        self._transitions: dict[tuple[str, ActionableElement], str] = {}
        self._next_id = 0
        # Per-state-name queue of screenshot hashes, popped one per visit to that
        # state. Exhausted (or never configured) means "no hash available" — the
        # fallback-to-DOM-only path.
        self._screenshots: dict[str, deque[str | None]] = {}

    def add(self, from_state: str, label: str, role: str, to_state: str) -> None:
        self._next_id += 1
        action = ActionableElement(role=role, name=label, backend_node_id=self._next_id)
        self._actions.setdefault(from_state, []).append(action)
        self._actions.setdefault(to_state, [])
        self._transitions[(from_state, action)] = to_state

    def set_screenshots(self, name: str, hashes: list[str | None]) -> None:
        self._screenshots[name] = deque(hashes)

    def html(self, name: str) -> str:
        return f"<html><body><h1>{name}</h1></body></html>"

    def ax_nodes(self, name: str) -> list[dict[str, object]]:
        return [
            {
                "role": {"value": action.role},
                "name": {"value": action.name},
                "ignored": False,
                "backendDOMNodeId": action.backend_node_id,
            }
            for action in self._actions.get(name, [])
        ]

    def next_state(self, name: str, action: ActionableElement) -> str:
        return self._transitions[(name, action)]

    def next_screenshot(self, name: str) -> str | None:
        queue = self._screenshots.get(name)
        return queue.popleft() if queue else None


class _FakeDriver:
    """A BrowserDriver over a _FakeApp; tracks the current state name."""

    def __init__(self, app: _FakeApp) -> None:
        self._app = app
        self._current = app.root
        self.capture_calls = 0

    def reset(self) -> None:
        self._current = self._app.root

    def state_html(self) -> str:
        return self._app.html(self._current)

    def ax_nodes(self) -> Sequence[Mapping[str, object]]:
        return self._app.ax_nodes(self._current)

    def probe(self, action: ActionableElement) -> ActuationVerdict:
        return ActuationVerdict(Verdict.ACTUATE)

    def perform(self, action: ActionableElement) -> None:
        self._current = self._app.next_state(self._current, action)

    def capture_signals(self) -> StateSignals:
        self.capture_calls += 1
        return StateSignals(screenshot_hash=self._app.next_screenshot(self._current))


@pytest.fixture
def context() -> dict[str, Any]:
    return {
        "app": _FakeApp(),
        "target": "http://localhost:8000/",
        "budget": RunBudget(),
    }


# --- Given -----------------------------------------------------------------


@given("an app whose actions are:")
def an_app(context: dict[str, Any], datatable: list[list[str]]) -> None:
    header, *rows = datatable
    app: _FakeApp = context["app"]
    for row in rows:
        fields = dict(zip(header, row, strict=True))
        app.add(fields["from"], fields["label"], fields["role"], fields["to"])


@given(parsers.parse('"{name}" is screenshotted as "{first}" then "{second}"'))
def set_screenshots(
    context: dict[str, Any], name: str, first: str, second: str
) -> None:
    context["app"].set_screenshots(name, [first, second])


@given(parsers.parse('"{name}" is never screenshotted'))
def no_screenshots(context: dict[str, Any], name: str) -> None:
    context["app"].set_screenshots(name, [None, None])


# --- When --------------------------------------------------------------------


@when(parsers.parse('I explore from "{root}"'))
def explore_from(context: dict[str, Any], root: str) -> None:
    app: _FakeApp = context["app"]
    app.root = root
    driver = _FakeDriver(app)
    context["driver"] = driver
    context["graph"] = explore(
        driver, target=context["target"], controller=RunController(context["budget"])
    )


# --- Then ------------------------------------------------------------------


@then(parsers.parse("the graph has {n:d} states"))
def graph_has_n_states(context: dict[str, Any], n: int) -> None:
    assert len(context["graph"].states) == n


def _target_state(context: dict[str, Any], label: str) -> str:
    graph = context["graph"]
    (transition,) = [t for t in graph.transitions if t.action.name == label]
    return transition.to_state


@then('"Go A" and "Go B" lead to different states')
def lead_to_different_states(context: dict[str, Any]) -> None:
    a, b = _target_state(context, "Go A"), _target_state(context, "Go B")
    assert a != b, f"expected distinct states, both landed on {a!r}"


@then('"Go A" and "Go B" lead to the same state')
def lead_to_same_state(context: dict[str, Any]) -> None:
    a, b = _target_state(context, "Go A"), _target_state(context, "Go B")
    assert a == b, f"expected the same state, got {a!r} and {b!r}"


@then(parsers.parse("exactly {n:d} signal captures were taken"))
def exact_capture_count(context: dict[str, Any], n: int) -> None:
    assert context["driver"].capture_calls == n


@then("no state id is a string-prefix of another state id")
def no_state_id_is_a_prefix_of_another(context: dict[str, Any]) -> None:
    # The exact bug class a composite "dom_id:hash"-style id would reintroduce:
    # apply.py's _resolve_state (and --resume-from's selector resolution) match a
    # saved id by str.startswith(prefix), so a composite id sharing its base
    # dom_id as a literal prefix would make that lookup wrongly ambiguous.
    states = list(context["graph"].states)
    for i, a in enumerate(states):
        for b in states[i + 1 :]:
            assert not a.startswith(b) and not b.startswith(a), (a, b)
