"""Step definitions for features/exploration_element_rules.feature (ROADMAP.md §2e,
closes #152).

Exercised in-process against a fake app, the same way the loop
(`exploration_loop.feature`) and recovery (`exploration_recovery.feature`) scenarios
are. Most scenarios reuse the loop's plain transition-table app; the one scope-boundary
scenario (an excluded element must still be usable by layer recovery to clear a
blocker in front of some other, included action) also needs a covering layer, so the
fake here borrows that shape from the recovery fixture directly rather than importing
across step-def modules (no step-def file in this codebase imports another's fixture).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.actuation import ActuationVerdict, CoveringElement, Verdict
from spoor.exploration.capture import StateSignals
from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.element_rules import ElementRules
from spoor.exploration.explorer import ElementCovered, ElementNotLocated, explore
from spoor.exploration.state import state_id

scenarios("exploration_element_rules.feature")


@dataclass(frozen=True)
class _LayerStep:
    action: ActionableElement
    advances: bool


class _FakeApp:
    """A deterministic app, optionally with one state covered by a layer."""

    def __init__(self) -> None:
        self.root = ""
        self._actions: dict[str, list[ActionableElement]] = {}
        self._transitions: dict[tuple[str, str, str], str] = {}
        self._layers: dict[str, list[_LayerStep]] = {}
        self._next_id = 0

    def _make(self, label: str, role: str) -> ActionableElement:
        self._next_id += 1
        return ActionableElement(role=role, name=label, backend_node_id=self._next_id)

    def add(self, from_state: str, label: str, role: str, to_state: str) -> None:
        action = self._make(label, role)
        self._actions.setdefault(from_state, []).append(action)
        self._actions.setdefault(to_state, [])  # ensure sink states exist
        self._transitions[(from_state, role, label)] = to_state

    def add_layer(self, state: str, steps: Sequence[tuple[str, str, bool]]) -> None:
        self._layers[state] = [
            _LayerStep(self._make(label, role), advances)
            for label, role, advances in steps
        ]
        self._actions.setdefault(state, [])

    def html(self, name: str) -> str:
        return f"<html><body><h1>{name}</h1></body></html>"

    def underlying(self, name: str) -> list[ActionableElement]:
        return list(self._actions.get(name, []))

    def layer_action(self, name: str, step: int) -> ActionableElement | None:
        steps = self._layers.get(name, [])
        return steps[step].action if 0 <= step < len(steps) else None

    def layer_advances(self, name: str, step: int) -> bool:
        return self._layers[name][step].advances

    def ax_nodes(self, name: str, step: int) -> list[dict[str, object]]:
        elements = self.underlying(name)
        layer = self.layer_action(name, step)
        if layer is not None:
            elements = [*elements, layer]
        return [
            {
                "role": {"value": e.role},
                "name": {"value": e.name},
                "ignored": False,
                "backendDOMNodeId": e.backend_node_id,
            }
            for e in elements
        ]

    def next_state(self, name: str, action: ActionableElement) -> str:
        return self._transitions[(name, action.role, action.name)]

    def state_id_of(self, name: str) -> str:
        return state_id(self.html(name))


class _FakeDriver:
    """A BrowserDriver over a _FakeApp, modelling a covering layer when one is set."""

    def __init__(self, app: _FakeApp) -> None:
        self._app = app
        self._current = app.root
        self._layer_step: dict[str, int] = {}

    def reset(self) -> None:
        self._current = self._app.root
        self._layer_step = {}

    def _step(self, state: str) -> int:
        return self._layer_step.get(state, 0)

    def state_html(self) -> str:
        return self._app.html(self._current)

    def ax_nodes(self) -> Sequence[Mapping[str, object]]:
        return self._app.ax_nodes(self._current, self._step(self._current))

    def _present(self, state: str, action: ActionableElement) -> bool:
        return any(
            (e.role, e.name) == (action.role, action.name)
            for e in self._app.underlying(state)
        )

    def probe(self, action: ActionableElement) -> ActuationVerdict:
        state = self._current
        step = self._step(state)
        layer = self._app.layer_action(state, step)
        if layer is not None and (action.role, action.name) == (
            layer.role,
            layer.name,
        ):
            return ActuationVerdict(Verdict.ACTUATE)
        if not self._present(state, action):
            return ActuationVerdict(Verdict.NOT_LOCATED)
        if layer is not None:
            return ActuationVerdict(
                Verdict.COVERED, CoveringElement(layer.role, layer.name)
            )
        return ActuationVerdict(Verdict.ACTUATE)

    def perform(self, action: ActionableElement) -> None:
        verdict = self.probe(action)
        if verdict.verdict is Verdict.NOT_LOCATED:
            raise ElementNotLocated(action.role, action.name)
        if verdict.verdict is Verdict.COVERED:
            assert verdict.covering is not None
            raise ElementCovered(verdict.covering.role, verdict.covering.text)
        state = self._current
        step = self._step(state)
        layer = self._app.layer_action(state, step)
        if layer is not None and (action.role, action.name) == (
            layer.role,
            layer.name,
        ):
            if self._app.layer_advances(state, step):
                self._layer_step[state] = step + 1
            return
        self._current = self._app.next_state(state, action)

    def capture_signals(self) -> StateSignals:
        return StateSignals()


@pytest.fixture
def context() -> dict[str, Any]:
    return {
        "app": _FakeApp(),
        "target": "http://localhost:8000/",
        "declared_sandbox": False,
        "budget": RunBudget(),
        "include": [],
        "exclude": [],
    }


# --- Given ---------------------------------------------------------------


@given("a sandbox target")
def sandbox_target(context: dict[str, Any]) -> None:
    context["target"] = "http://localhost:8000/"


@given("a real target")
def real_target(context: dict[str, Any]) -> None:
    context["target"] = "https://shop.example.com/"


@given(parsers.parse('an include pattern "{pattern}"'))
def include_pattern(context: dict[str, Any], pattern: str) -> None:
    context["include"].append(pattern)


@given(parsers.parse('an exclude pattern "{pattern}"'))
def exclude_pattern(context: dict[str, Any], pattern: str) -> None:
    context["exclude"].append(pattern)


@given("an app whose actions are:")
def an_app(context: dict[str, Any], datatable: list[list[str]]) -> None:
    header, *rows = datatable
    app: _FakeApp = context["app"]
    for row in rows:
        fields = dict(zip(header, row, strict=True))
        app.add(fields["from"], fields["label"], fields["role"], fields["to"])


@given(parsers.parse('the "{state}" state is covered by a layer whose actions are:'))
def covered_by_layer(
    context: dict[str, Any], state: str, datatable: list[list[str]]
) -> None:
    header, *rows = datatable
    app: _FakeApp = context["app"]
    steps = [
        (fields["label"], fields["role"], fields["clears"].strip() == "yes")
        for fields in (dict(zip(header, row, strict=True)) for row in rows)
    ]
    app.add_layer(state, steps)


# --- When ------------------------------------------------------------------


@when(parsers.parse('I explore from "{root}"'))
def i_explore(context: dict[str, Any], root: str) -> None:
    app: _FakeApp = context["app"]
    app.root = root
    controller = RunController(context["budget"])
    element_rules = ElementRules(
        include=tuple(context["include"]) if context["include"] else None,
        exclude=tuple(context["exclude"]) if context["exclude"] else None,
    )
    context["graph"] = explore(
        _FakeDriver(app),
        target=context["target"],
        controller=controller,
        declared_sandbox=context["declared_sandbox"],
        element_rules=element_rules,
    )


# --- Then --------------------------------------------------------------


@then(parsers.parse('the graph has a transition "{frm} --{label}--> {to}"'))
def graph_has_transition(
    context: dict[str, Any], frm: str, label: str, to: str
) -> None:
    app: _FakeApp = context["app"]
    from_id = app.state_id_of(frm)
    to_id = app.state_id_of(to)
    found = [
        t
        for t in context["graph"].transitions
        if t.from_state == from_id and t.to_state == to_id and t.action.name == label
    ]
    assert found, f"no transition {frm} --{label}--> {to}"


@then(parsers.parse('the action "{label}" from "{frm}" is skipped'))
def action_is_skipped(context: dict[str, Any], label: str, frm: str) -> None:
    app: _FakeApp = context["app"]
    from_id = app.state_id_of(frm)
    skipped = [
        s
        for s in context["graph"].skipped
        if s.from_state == from_id and s.action.name == label
    ]
    assert skipped, f"expected {label!r} from {frm!r} to be skipped"
    fired = [
        t
        for t in context["graph"].transitions
        if t.from_state == from_id and t.action.name == label
    ]
    assert not fired, f"{label!r} was skipped but also fired"
