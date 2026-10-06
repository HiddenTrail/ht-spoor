"""Step definitions for features/self_healing_report.feature (ROADMAP.md §2,
closes #154).

Pure-logic scenarios built directly against `HealEvent` — no run, no browser, no
disk. The engine wiring that populates `old_selector`/`new_locator` from a real
run is pinned separately by features/self_healing_runs.feature; this file
exercises only `render_healing_report`.
"""

from __future__ import annotations

from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from spoor.core.self_healing import HealEvent
from spoor.operational.healing_report import render_healing_report

scenarios("self_healing_report.feature")


@pytest.fixture
def context() -> dict[str, Any]:
    return {"events": []}


# --- Given ---------------------------------------------------------------


@given(
    parsers.parse(
        'a confident heal of "{field}" from "{old}" to "{new}" '
        'with confidence "{conf}"'
    )
)
def confident_heal(
    context: dict[str, Any], field: str, old: str, new: str, conf: str
) -> None:
    context["events"].append(
        HealEvent(
            field=field,
            confidence=float(conf),
            used=True,
            old_selector=old,
            new_locator=new,
        )
    )


@given(
    parsers.parse(
        'an uncertain heal of "{field}" from "{old}" to "{new}" '
        'with confidence "{conf}"'
    )
)
def uncertain_heal(
    context: dict[str, Any], field: str, old: str, new: str, conf: str
) -> None:
    context["events"].append(
        HealEvent(
            field=field,
            confidence=float(conf),
            used=False,
            old_selector=old,
            new_locator=new,
        )
    )


@given("no heal events this run")
def no_events(context: dict[str, Any]) -> None:
    context["events"] = []


# --- When ------------------------------------------------------------------


@when("I render the healing report")
def render(context: dict[str, Any]) -> None:
    context["report"] = render_healing_report(context["events"])


# --- Then --------------------------------------------------------------


@then(parsers.parse('the report lists "{field}" as a confident heal'))
def lists_confident(context: dict[str, Any], field: str) -> None:
    report = context["report"]
    assert report is not None
    assert "## Confident heals" in report
    confident_section = report.split("## Confident heals", 1)[1]
    section = confident_section.split("## Uncertain matches", 1)[0]
    assert field in section


@then(parsers.parse('the report lists "{field}" as an uncertain match'))
def lists_uncertain(context: dict[str, Any], field: str) -> None:
    report = context["report"]
    assert report is not None
    assert "## Uncertain matches" in report
    section = report.split("## Uncertain matches", 1)[1]
    assert field in section


@then(
    parsers.parse(
        'the report shows the old selector "{old}" and the suggested selector "{new}"'
    )
)
def shows_selectors(context: dict[str, Any], old: str, new: str) -> None:
    report = context["report"]
    assert report is not None
    assert old in report
    assert new in report


@then("the report suggests updating the config")
def suggests_update(context: dict[str, Any]) -> None:
    report = context["report"]
    assert report is not None
    assert "update your config" in report.lower()


@then("the report says uncertain matches are flagged for review, not applied")
def says_flagged(context: dict[str, Any]) -> None:
    report = context["report"]
    assert report is not None
    assert "flagged for review" in report.lower()
    assert "never guesses" in report.lower()


@then("no report is rendered")
def no_report(context: dict[str, Any]) -> None:
    assert context["report"] is None


@then(parsers.parse('the report does not contain the raw secret "{secret}"'))
def no_raw_secret(context: dict[str, Any], secret: str) -> None:
    report = context["report"]
    assert report is not None
    assert secret not in report
