"""Step definitions for features/interactive_scaffold_apply.feature (§2e, #131).

Two tiers. The fast-tier steps build a graph directly in-process (state names double
as their ids, same convention `test_testgen_writer_steps.py` already uses) and drive a
hand-rolled fake driver — no browser. The `@browser` step proves the one thing that
needs a real page: that `driver.fill` actually changes a live field's DOM value, read
back afterward, not just that the call was made.
"""

from __future__ import annotations

from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.capture import StateSignals
from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.driver import PlaywrightDriver
from spoor.exploration.explorer import ActionError, explore
from spoor.exploration.graph import ExplorationGraph
from spoor.scaffold.apply import AppliedField, FailedField, apply_scaffold

scenarios("interactive_scaffold_apply.feature")


class _FakeDriver:
    """Records what it was asked to do; never touches a real page."""

    def __init__(self) -> None:
        self.current_url = "http://localhost/"
        self.fail_reset = False
        self.resets = 0
        self.performed: list[str] = []
        self.filled: dict[str, str] = {}
        # When False (the default), state_html() never changes, so a fill's own
        # observe-and-merge step (§2e issue #137) sees no change and adds nothing new
        # to the graph — the behaviour every scenario not about that feature expects.
        self.reveals_new_state = False

    def reset(self) -> None:
        self.resets += 1
        self.filled.clear()
        if self.fail_reset:
            raise ActionError("reset failed")
        self.performed = []

    def perform(self, action: ActionableElement) -> None:
        self.performed.append(action.name)

    def fill(self, action: ActionableElement, value: str) -> None:
        self.filled[action.name] = value

    def state_html(self) -> str:
        # apply_scaffold is root-state-only (the existing navigation restriction), so
        # every group's starting state is always the graph's root — "home" in every
        # scenario in this file. Paired with the `compute_state_id -> identity`
        # monkeypatch the `apply` step installs, returning "home" here round-trips to
        # exactly the graph's own root id, the same way a real driver's unchanged page
        # hashes back to the state it started at.
        if not self.reveals_new_state:
            return "home"
        # Distinct per fill step so a group of several fills chains through a
        # distinct state after each one, exactly as a real page would.
        return f"home+{sorted(self.filled.items())}"

    def ax_nodes(self) -> list[dict[str, object]]:
        return []

    def capture_signals(self) -> StateSignals:
        return StateSignals()


@pytest.fixture
def context() -> dict[str, Any]:
    return {"graph": ExplorationGraph(), "scaffold": {"fields": []}, "driver": None}


# --- Given -------------------------------------------------------------------


@given(parsers.parse('a mapped graph with a field "{name}" on state "{state}"'))
def a_mapped_graph(context: dict[str, Any], name: str, state: str) -> None:
    context["graph"].add_state(
        state, [ActionableElement(role="textbox", name=name, backend_node_id=1)]
    )


@given(parsers.parse('the scaffold pins "{name}" on "{state}" to "{value}"'))
def scaffold_pins(context: dict[str, Any], name: str, state: str, value: str) -> None:
    context["scaffold"]["fields"].append({"state": state, "name": name, "value": value})


@given(parsers.parse('the scaffold pins "{name}" on "{state}" to a blank value'))
def scaffold_pins_blank(context: dict[str, Any], name: str, state: str) -> None:
    context["scaffold"]["fields"].append({"state": state, "name": name, "value": ""})


@given("an empty scaffold")
def empty_scaffold(context: dict[str, Any]) -> None:
    context["scaffold"] = {"fields": []}


@given(
    parsers.parse(
        'the scaffold asks to generate "{name}" on "{state}" with kind "{kind}"'
    )
)
def scaffold_generate(
    context: dict[str, Any], name: str, state: str, kind: str
) -> None:
    context["scaffold"]["fields"].append(
        {"state": state, "name": name, "value": "", "kind": kind, "generate": True}
    )


@given("that same field also asks to generate with kind \"email\"")
def also_generate(context: dict[str, Any]) -> None:
    context["scaffold"]["fields"][-1]["kind"] = "email"
    context["scaffold"]["fields"][-1]["generate"] = True


@given(
    parsers.parse(
        'the scaffold has "{name}" on "{state}" with a blank value and generate: false'
    )
)
def scaffold_generate_false(context: dict[str, Any], name: str, state: str) -> None:
    context["scaffold"]["fields"].append(
        {"state": state, "name": name, "value": "", "kind": "email", "generate": False}
    )


# --- When --------------------------------------------------------------------


@when("I apply the scaffold")
def apply(context: dict[str, Any], monkeypatch: pytest.MonkeyPatch) -> None:
    driver = _FakeDriver()
    driver.fail_reset = context.get("fail_reset", False)
    driver.reveals_new_state = context.get("reveals_new_state", False)
    context["driver"] = driver
    context["states_before"] = list(context["graph"].states)
    # The fast tier's graph states are plain labels ("home"), not real content
    # hashes (see the module docstring) — `apply_scaffold`'s post-fill observation
    # (§2e issue #137) otherwise hashes `_FakeDriver.state_html()` for real, which
    # could never equal a plain label. Identity here makes the fake's own labels
    # round-trip as themselves, exactly like a real driver's hash of an unchanged
    # page round-trips to the state it started at.
    monkeypatch.setattr("spoor.scaffold.apply.compute_state_id", lambda html: html)
    applied, failed = apply_scaffold(
        driver, context["graph"], context["scaffold"],
        target=context.get("target", "http://localhost/"),
    )
    context["applied"] = applied
    context["failed"] = failed


# --- Then --------------------------------------------------------------------


def _find_applied(context: dict[str, Any], name: str, state: str) -> AppliedField:
    match = [
        f for f in context["applied"] if f.name == name and f.state.startswith(state)
    ]
    assert match, f"{name!r} on {state!r} was not applied: {context['applied']!r}"
    return match[0]


def _find_failed(context: dict[str, Any], name: str, state: str) -> FailedField:
    match = [
        f for f in context["failed"] if f.name == name and f.state.startswith(state)
    ]
    assert match, f"{name!r} on {state!r} did not fail: {context['failed']!r}"
    return match[0]


@then(parsers.parse('"{name}" on "{state}" was applied'))
def was_applied(context: dict[str, Any], name: str, state: str) -> None:
    _find_applied(context, name, state)


@then(parsers.parse('the driver typed "{value}" into "{name}"'))
def driver_typed(context: dict[str, Any], value: str, name: str) -> None:
    assert context["driver"].filled.get(name) == value


@then(parsers.parse('"{name}" on "{state}" was applied as a generated value'))
def was_applied_generated(context: dict[str, Any], name: str, state: str) -> None:
    field = _find_applied(context, name, state)
    assert field.generated is True


@then(parsers.parse('the driver typed an email-shaped value into "{name}"'))
def driver_typed_email_shaped(context: dict[str, Any], name: str) -> None:
    value = context["driver"].filled.get(name)
    assert value is not None and "@" in value


@then(parsers.parse('the driver replayed the path to "{state}" before typing'))
def driver_replayed(context: dict[str, Any], state: str) -> None:
    assert context["driver"].resets >= 1


@then("no field was applied")
def no_field_applied(context: dict[str, Any]) -> None:
    assert context["applied"] == []


@then("no field failed")
def no_field_failed(context: dict[str, Any]) -> None:
    assert context["failed"] == []


@then(parsers.parse('"{name}" on "{state}" failed with reason "{reason}"'))
def failed_with_reason(
    context: dict[str, Any], name: str, state: str, reason: str
) -> None:
    entry = _find_failed(context, name, state)
    assert entry.reason == reason


# --- Live (@browser) -----------------------------------------------------


@given(parsers.parse('a live crawl of "{page}" was mapped at depth {depth:d}'))
def live_crawl(
    context: dict[str, Any], live_server: str, page: str, depth: int
) -> None:
    url = f"{live_server}/{page}"
    context["target"] = url
    with PlaywrightDriver(url) as driver:
        context["graph"] = explore(
            driver,
            target=url,
            controller=RunController(RunBudget(max_depth=depth)),
        )
    assert context["graph"].states, "the live crawl mapped no states"
    context["crawled_state"] = context["graph"].states[0]


@given(parsers.parse('the scaffold pins "{name}" on the crawled state to "{value}"'))
def scaffold_pins_crawled(context: dict[str, Any], name: str, value: str) -> None:
    context["scaffold"] = {
        "fields": [
            {"state": context["crawled_state"], "name": name, "value": value}
        ]
    }


@when("I apply the scaffold against the live driver")
def apply_live(context: dict[str, Any]) -> None:
    with PlaywrightDriver(context["target"]) as driver:
        applied, failed = apply_scaffold(
            driver, context["graph"], context["scaffold"],
            target=context.get("target", "http://localhost/"),
        )
        context["applied"] = applied
        context["failed"] = failed
        # Read the live field's value back while this same driver/page is still open,
        # before the `with` block closes it — the actual end-to-end proof.
        selector = context.get("live_field_selector", "#nickname")
        context["live_value"] = driver._live_page.locator(  # noqa: SLF001
            selector
        ).input_value()


@given(parsers.parse('the live field to check is "{selector}"'))
def live_field_selector(context: dict[str, Any], selector: str) -> None:
    context["live_field_selector"] = selector


@then(parsers.parse('the live page\'s "{name}" field now reads "{value}"'))
def live_field_reads(context: dict[str, Any], name: str, value: str) -> None:
    assert context["failed"] == [], f"apply reported failures: {context['failed']!r}"
    assert context["live_value"] == value


@then(parsers.parse('the live page\'s "{name}" field still reads "{value}"'))
def live_field_still_reads(context: dict[str, Any], name: str, value: str) -> None:
    assert context["live_value"] == value


@given("the apply target is not a sandbox")
def production_target(context: dict[str, Any]) -> None:
    context["target"] = "https://production.invalid/"


@given("the scaffold contains an unquoted numeric value")
def numeric_value(context: dict[str, Any]) -> None:
    context["scaffold"] = {"fields": [{"state": "home", "name": "Email", "value": 42}]}


@given(parsers.parse('another field "{name}" on "{state}"'))
def another_field(context: dict[str, Any], name: str, state: str) -> None:
    context["graph"].node(state).actions.append(
        ActionableElement(role="textbox", name=name, backend_node_id=2)
    )


@given("resetting the apply driver fails")
def failing_reset(context: dict[str, Any]) -> None:
    context["fail_reset"] = True


@given("a field on a state reached by clicking")
def deeper_field(context: dict[str, Any]) -> None:
    graph = context["graph"]
    graph.add_state(
        "detail", [ActionableElement(role="textbox", name="Email", backend_node_id=1)]
    )
    link = ActionableElement(role="link", name="Details", backend_node_id=2)
    graph.add_transition("home", link, "detail")


@then("the driver was not reset")
def not_reset(context: dict[str, Any]) -> None:
    assert context["driver"].resets == 0


@then("the driver was reset exactly once")
def reset_once(context: dict[str, Any]) -> None:
    assert context["driver"].resets == 1


@given("filling a field on this driver reveals a new page")
def reveals_new_state(context: dict[str, Any]) -> None:
    context["reveals_new_state"] = True


@then("a new state was added to the graph")
def new_state_added(context: dict[str, Any]) -> None:
    before = set(context["states_before"])
    after = set(context["graph"].states)
    assert after - before, f"no new state; graph still has {sorted(before)}"


@then("no new state was added to the graph")
def no_new_state_added(context: dict[str, Any]) -> None:
    assert list(context["graph"].states) == context["states_before"]


@then(parsers.parse('its incoming transition was typed with "{value}", not clicked'))
def incoming_transition_typed(context: dict[str, Any], value: str) -> None:
    before = set(context["states_before"])
    new_states = set(context["graph"].states) - before
    assert len(new_states) == 1, f"expected exactly one new state, got {new_states!r}"
    (new_state,) = new_states
    matches = [t for t in context["graph"].transitions if t.to_state == new_state]
    assert matches, f"no transition leads to the new state {new_state!r}"
    assert matches[0].action.fill_value == value
