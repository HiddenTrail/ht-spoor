"""Step definitions for features/exploration_hooks.feature (ROADMAP.md §2e, #187).

The explorer loop is exercised in-process against a fake deterministic app,
the same `_FakeApp`/`_FakeDriver` shape `test_exploration_loop_steps.py`
uses (each step-def file keeps its own self-contained fake, the established
pattern in this test suite — no cross-file imports between them).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.actuation import ActuationVerdict, Verdict
from spoor.exploration.capture import StateSignals
from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.driver import PlaywrightDriver
from spoor.exploration.explorer import explore
from spoor.exploration.hooks import ExplorationHooks, ExploredState, ExploredTransition
from spoor.exploration.state import state_id

scenarios("exploration_hooks.feature")

_BEARER_TOKEN = "abcdef1234567890x"


class _FakeApp:
    """A deterministic state machine described by the scenario's transition table."""

    def __init__(self) -> None:
        self.root = ""
        self._actions: dict[str, list[ActionableElement]] = {}
        self._transitions: dict[tuple[str, ActionableElement], str] = {}
        self._console: dict[str, tuple[str, ...]] = {}
        self._next_id = 0

    def add(self, from_state: str, label: str, role: str, to_state: str) -> None:
        self._next_id += 1
        action = ActionableElement(role=role, name=label, backend_node_id=self._next_id)
        self._actions.setdefault(from_state, []).append(action)
        self._actions.setdefault(to_state, [])  # ensure sink states exist
        self._transitions[(from_state, action)] = to_state

    def set_console(self, state_name: str, messages: tuple[str, ...]) -> None:
        self._console[state_name] = messages

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

    def state_id_of(self, name: str) -> str:
        return state_id(self.html(name))

    def console_for(self, name: str) -> tuple[str, ...]:
        return self._console.get(name, ())


class _FakeDriver:
    """A BrowserDriver over a _FakeApp; tracks the current state name."""

    def __init__(self, app: _FakeApp) -> None:
        self._app = app
        self._current = app.root

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
        return StateSignals(console_messages=self._app.console_for(self._current))


@pytest.fixture
def context() -> dict[str, Any]:
    return {
        "app": _FakeApp(),
        "target": "http://localhost:8000/",
        "declared_sandbox": False,
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


@given(
    parsers.parse(
        'the state "{name}" carries a console message with a bearer token'
    )
)
def state_carries_secret(context: dict[str, Any], name: str) -> None:
    app: _FakeApp = context["app"]
    app.set_console(name, (f"Bearer {_BEARER_TOKEN}",))


@given(parsers.parse('the action "{label}" leads to a new state'))
def destructive_action_leads_somewhere(context: dict[str, Any], label: str) -> None:
    app: _FakeApp = context["app"]
    app.add("start", label, "button", "deleted")


@given("the target is a real, non-sandbox site")
def real_target(context: dict[str, Any]) -> None:
    context["target"] = "https://shop.example.com/"


# --- Given/When/Then: live (@browser) ---------------------------------


@given(parsers.parse('a live browser on the exploration fixture "{page}"'))
def live_browser(context: dict[str, Any], live_server: str, page: str) -> None:
    url = f"{live_server}/{page}"
    driver = PlaywrightDriver(url)
    driver.__enter__()
    context["driver"] = driver
    context["live_url"] = url


@pytest.fixture(autouse=True)
def _teardown(context: dict[str, Any]) -> Any:
    yield
    driver = context.get("driver")
    if driver is not None:
        driver.close()


@when("I explore it live with hooks recording states and transitions")
def explore_live_with_hooks(context: dict[str, Any]) -> None:
    states: list[ExploredState] = []
    transitions: list[ExploredTransition] = []
    context["recorded_states"] = states
    context["recorded_transitions"] = transitions
    hooks = ExplorationHooks(
        on_state_discovered=states.append, on_transition_taken=transitions.append
    )
    context["graph"] = explore(
        context["driver"],
        target=context["live_url"],
        controller=RunController(RunBudget()),
        hooks=hooks,
    )


# --- When --------------------------------------------------------------


def _hooks_recording_states(context: dict[str, Any]) -> ExplorationHooks:
    recorded: list[ExploredState] = []
    context["recorded_states"] = recorded
    return ExplorationHooks(on_state_discovered=recorded.append)


def _hooks_recording_transitions(context: dict[str, Any]) -> ExplorationHooks:
    recorded: list[ExploredTransition] = []
    context["recorded_transitions"] = recorded
    return ExplorationHooks(on_transition_taken=recorded.append)


def _explore(
    context: dict[str, Any], root: str, hooks: ExplorationHooks | None
) -> None:
    app: _FakeApp = context["app"]
    app.root = root
    controller = RunController(context["budget"])
    context["graph"] = explore(
        _FakeDriver(app),
        target=context["target"],
        controller=controller,
        declared_sandbox=context["declared_sandbox"],
        hooks=hooks,
    )


@when(parsers.parse('I explore from "{root}" with hooks recording discovered states'))
def explore_recording_states(context: dict[str, Any], root: str) -> None:
    _explore(context, root, _hooks_recording_states(context))


@when(parsers.parse('I explore from "{root}" with hooks recording transitions'))
def explore_recording_transitions(context: dict[str, Any], root: str) -> None:
    _explore(context, root, _hooks_recording_transitions(context))


@when(parsers.parse('I explore from "{root}" with no hooks'))
def explore_with_no_hooks(context: dict[str, Any], root: str) -> None:
    _explore(context, root, None)


# --- Then ------------------------------------------------------------------


@then(parsers.parse("the hook recorded {n:d} discovered states"))
def hook_recorded_n_states(context: dict[str, Any], n: int) -> None:
    assert len(context["recorded_states"]) == n


@then(parsers.parse('the hook recorded "{name}" exactly once'))
def hook_recorded_state_once(context: dict[str, Any], name: str) -> None:
    app: _FakeApp = context["app"]
    want = app.state_id_of(name)
    matches = [s for s in context["recorded_states"] if s.state_id == want]
    assert len(matches) == 1


@then(parsers.parse("the hook recorded {n:d} transition"))
@then(parsers.parse("the hook recorded {n:d} transitions"))
def hook_recorded_n_transitions(context: dict[str, Any], n: int) -> None:
    assert len(context["recorded_transitions"]) == n


@then(
    parsers.parse(
        'the hook recorded a transition "{frm} --{label}--> {to}"'
    )
)
def hook_recorded_transition(
    context: dict[str, Any], frm: str, label: str, to: str
) -> None:
    app: _FakeApp = context["app"]
    from_id = app.state_id_of(frm)
    to_id = app.state_id_of(to)
    matches = [
        t
        for t in context["recorded_transitions"]
        if t.from_state == from_id
        and t.to_state == to_id
        and t.action_name == label
    ]
    assert len(matches) == 1


@then("the hook's recorded transition carries no raw token")
def transition_carries_no_raw_token(context: dict[str, Any]) -> None:
    transition = context["recorded_transitions"][0]
    assert transition.changed is not None
    assert all(
        _BEARER_TOKEN not in line for line in transition.changed.console_added
    )


@then("the hook's recorded transition carries the redacted marker")
def transition_carries_redacted_marker(context: dict[str, Any]) -> None:
    transition = context["recorded_transitions"][0]
    assert transition.changed is not None
    assert any("REDACTED" in line for line in transition.changed.console_added)


@then(parsers.parse('the hook recorded no transition for "{label}"'))
def hook_recorded_no_transition_for(context: dict[str, Any], label: str) -> None:
    matches = [
        t for t in context["recorded_transitions"] if t.action_name == label
    ]
    assert matches == []


@then(parsers.parse("the graph has {n:d} states"))
def graph_has_n_states(context: dict[str, Any], n: int) -> None:
    assert len(context["graph"].states) == n
