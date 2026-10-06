"""Tier-3 healing report: render heal events as an actionable markdown report
(ROADMAP.md §2/§2d, closes #154).

docs/COMPETITIVE_PLAN.md flags Healenium/Testim's healing reports (old locator,
new locator, confidence, suggested fix) as worth adapting: tier 3 already records
a `HealEvent` per heal attempt (`spoor/core/self_healing.py`) and `RunSummary`
already counts them, but neither names what broke or what tier 3 found instead —
a heal today is a silent runtime recovery, visible only as a number. This module
turns the same events already on `RunResult.heal_events` into a human-readable
report: per field, the selector that stopped matching, the locator tier 3
re-resolved it to, its confidence, and — for a confident heal — a suggested
config fix so the next run doesn't need to heal at all.

Confident heals and uncertain matches are reported in separate sections: a
confident heal's suggestion is something to act on directly; an uncertain
match's best guess is something to *review*, never apply blindly — tier 3 never
silently guesses (§2, §1), and this report doesn't either. Every captured value
is a structural locator string (a tag/id/class shape), never the matched page
text (§2h, same boundary `HealEvent` itself already holds), but is still
`redact()`-ed before it reaches this shared-output surface, the same defensive
posture the generated-test writer (§2g) takes on every value it bakes in.
"""

from __future__ import annotations

from collections.abc import Sequence

from spoor.core.self_healing import HealEvent
from spoor.security.redaction import redact


def render_healing_report(heal_events: Sequence[HealEvent]) -> str | None:
    """Render `heal_events` as a markdown healing report, or None if there's
    nothing to report (closes #154).

    Confident heals come first — each with a suggested config-selector fix —
    then uncertain matches, flagged for manual review rather than suggested as
    something to adopt outright. Returns None for an empty run, the same "no
    shell report" posture every other generated-output function in this
    codebase takes for an empty input.
    """
    if not heal_events:
        return None
    confident = [e for e in heal_events if e.used]
    uncertain = [e for e in heal_events if not e.used]
    lines = [
        "# Healing report",
        "",
        f"Tier 3 (self-healing) re-resolved {len(heal_events)} selector(s) this "
        f"run: {len(confident)} confidently, {len(uncertain)} flagged for review.",
        "",
    ]
    if confident:
        lines += _confident_section(confident)
    if uncertain:
        lines += _uncertain_section(uncertain)
    return "\n".join(lines) + "\n"


def _row(event: HealEvent) -> str:
    old = redact(event.old_selector) if event.old_selector else "?"
    new = redact(event.new_locator) if event.new_locator else "(none)"
    return f"| {redact(event.field)} | `{old}` | `{new}` | {event.confidence:.2f} |"


def _confident_section(events: Sequence[HealEvent]) -> list[str]:
    return [
        "## Confident heals",
        "",
        "| Field | Old selector | Suggested new selector | Confidence |",
        "|---|---|---|---|",
        *(_row(e) for e in events),
        "",
        "Suggested fix: update your config's selector for each field above from "
        "its old value to the suggested new one — tier 3 healed it at runtime, "
        "but a config update stops it from needing to again next time.",
        "",
    ]


def _uncertain_section(events: Sequence[HealEvent]) -> list[str]:
    return [
        "## Uncertain matches (flagged for review)",
        "",
        "| Field | Old selector | Best candidate (unconfirmed) | Confidence |",
        "|---|---|---|---|",
        *(_row(e) for e in events),
        "",
        "These did not clear the confidence threshold and were left null this "
        "run. Review manually before adopting any candidate above — tier 3 "
        "never guesses on your behalf (§2).",
    ]
