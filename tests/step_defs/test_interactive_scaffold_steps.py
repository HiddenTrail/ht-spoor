"""Step definitions for features/interactive_scaffold.feature (§2e, issue #131).

Two tiers, mirroring the testgen step modules' shape. The fast-tier steps build a
graph directly in-process (states keyed by friendly names, exactly as elsewhere) and
exercise `build_scaffold` — pure, no disk, no browser. The `@browser` step proves the
one thing that needs a real page: that the driver's `input_type` enrichment (slice 1)
actually reaches a real password field, end to end, and lands in a written file.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.exploration.control import RunBudget, RunController
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.driver import PlaywrightDriver
from spoor.exploration.explorer import explore
from spoor.exploration.graph import ExplorationGraph
from spoor.exploration.safety import DESTRUCTIVE_SKIP_REASON
from spoor.scaffold.interactive_config import build_scaffold, render_scaffold

scenarios("interactive_scaffold.feature")


@pytest.fixture
def context() -> dict[str, Any]:
    return {"graph": ExplorationGraph()}


# --- Given: build a graph directly (fast tier) ----------------------------


@given(parsers.parse('a discovered state "{state}":'))
def a_discovered_state(
    context: dict[str, Any], state: str, datatable: list[list[str]]
) -> None:
    header, *rows = datatable
    elements = [
        ActionableElement(
            role=f["role"],
            name=f["name"],
            backend_node_id=None,
            input_type=f.get("input_type") or None,
        )
        for f in (dict(zip(header, row, strict=True)) for row in rows)
    ]
    context["graph"].add_state(state, elements)


@given("an empty discovered graph")
def empty_graph(context: dict[str, Any]) -> None:
    context["graph"] = ExplorationGraph()


@given(parsers.parse('"{action_name}" on "{state}" was skipped as destructive'))
def skipped_as_destructive(
    context: dict[str, Any], action_name: str, state: str
) -> None:
    node = context["graph"].node(state)
    match = next(a for a in node.actions if a.name == action_name)
    context["graph"].record_skip(state, match, DESTRUCTIVE_SKIP_REASON)


@given(
    parsers.parse('"{action_name}" on "{state}" was skipped for an unrelated reason')
)
def skipped_unrelated(context: dict[str, Any], action_name: str, state: str) -> None:
    node = context["graph"].node(state)
    match = next(a for a in node.actions if a.name == action_name)
    context["graph"].record_skip(
        state, match, "blocked by an unresolved layer: div 'Cookie banner'"
    )


# --- When ------------------------------------------------------------------


@when(parsers.parse('I scaffold a config for "{target}"'))
def scaffold(context: dict[str, Any], target: str) -> None:
    text = build_scaffold(context["graph"], target=target)
    context["scaffold_text"] = text
    context["scaffold"] = yaml.safe_load(text) if text else None


# --- Then --------------------------------------------------------------------


def _find(items: list[dict[str, Any]], name: str) -> dict[str, Any]:
    match = [item for item in items if item["name"] == name]
    assert match, f"no entry named {name!r} in {items!r}"
    return match[0]


@then(parsers.parse('the scaffold has a field named "{name}" with kind "{kind}"'))
def has_field(context: dict[str, Any], name: str, kind: str) -> None:
    field = _find(context["scaffold"]["fields"], name)
    assert field["kind"] == kind
    context["last_field"] = field


@then("that field has a blank value to fill in")
def field_value_blank(context: dict[str, Any]) -> None:
    assert context["last_field"]["value"] is None


@then(parsers.parse('the scaffold has a login point named "{name}"'))
def has_login_point(context: dict[str, Any], name: str) -> None:
    login = _find(context["scaffold"]["login_points"], name)
    context["last_login"] = login


@then(parsers.parse('no field in the scaffold is named "{name}"'))
def no_field_named(context: dict[str, Any], name: str) -> None:
    assert all(f["name"] != name for f in context["scaffold"]["fields"])


@then("that login point has no credential keys, only a blank session")
def login_point_shape(context: dict[str, Any]) -> None:
    login = context["last_login"]
    assert set(login) == {"state", "name", "session"}
    assert login["session"] is None


@then(parsers.parse('the scaffold has a destructive action named "{name}"'))
def has_destructive_action(context: dict[str, Any], name: str) -> None:
    entry = _find(context["scaffold"]["destructive_actions"], name)
    context["last_destructive"] = entry


@then("that destructive action is not allowed by default")
def destructive_not_allowed(context: dict[str, Any]) -> None:
    assert context["last_destructive"]["allow"] is False


@then(parsers.parse('no destructive action in the scaffold is named "{name}"'))
def no_destructive_named(context: dict[str, Any], name: str) -> None:
    assert all(
        d["name"] != name for d in context["scaffold"]["destructive_actions"]
    )


@then(parsers.parse('no generated scaffold contains the raw secret "{secret}"'))
def no_raw_secret(context: dict[str, Any], secret: str) -> None:
    assert secret not in context["scaffold_text"]


@then("no scaffold is written")
def no_scaffold(context: dict[str, Any]) -> None:
    assert context["scaffold_text"] == ""


# --- Live (@browser) -------------------------------------------------------


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


@when("I write that crawl's scaffold to a file")
def write_live_scaffold(context: dict[str, Any], tmp_path: Path) -> None:
    out_path = tmp_path / "scaffold.yaml"
    context["out_path"] = render_scaffold(
        context["graph"], out_path, target=context["target"]
    )


@then("the written scaffold file has a login point")
def written_has_login_point(context: dict[str, Any]) -> None:
    out_path = context["out_path"]
    assert out_path is not None, "nothing was written"
    parsed = yaml.safe_load(out_path.read_text(encoding="utf-8"))
    assert parsed["login_points"], "no login points in the written scaffold"
