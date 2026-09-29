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

from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.driver import PlaywrightDriver
from spoor.exploration.explorer import explore
from spoor.exploration.graph import ExplorationGraph
from spoor.scaffold.apply import AppliedField, FailedField, apply_scaffold

scenarios("interactive_scaffold_apply.feature")


class _FakeDriver:
    """Records what it was asked to do; never touches a real page."""

    def __init__(self) -> None:
        self.resets = 0
        self.performed: list[str] = []
        self.filled: dict[str, str] = {}

    def reset(self) -> None:
        self.resets += 1
        self.performed = []

    def perform(self, action: ActionableElement) -> None:
        self.performed.append(action.name)

    def fill(self, action: ActionableElement, value: str) -> None:
        self.filled[action.name] = value


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


# --- When --------------------------------------------------------------------


@when("I apply the scaffold")
def apply(context: dict[str, Any]) -> None:
    driver = _FakeDriver()
    context["driver"] = driver
    applied, failed = apply_scaffold(driver, context["graph"], context["scaffold"])
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
        applied, failed = apply_scaffold(driver, context["graph"], context["scaffold"])
        context["applied"] = applied
        context["failed"] = failed
        # Read the live field's value back while this same driver/page is still open,
        # before the `with` block closes it — the actual end-to-end proof.
        context["live_value"] = driver._live_page.locator(  # noqa: SLF001
            "#nickname"
        ).input_value()


@then(parsers.parse('the live page\'s "{name}" field now reads "{value}"'))
def live_field_reads(context: dict[str, Any], name: str, value: str) -> None:
    assert context["failed"] == [], f"apply reported failures: {context['failed']!r}"
    assert context["live_value"] == value
