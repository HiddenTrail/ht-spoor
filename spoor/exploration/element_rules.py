"""User-configurable clickable-element rules for exploration (ROADMAP.md §2e,
closes #152).

docs/COMPETITIVE_PLAN.md flags Crawljax's clickable-element rules (including
exclusions) as worth adapting: an explicit, user-set allow/exclude list for which
actionable elements exploration mode is willing to attempt, matched against each
element's visible accessible label (`ActionableElement.name`) with a glob pattern —
an explicit rule the operator wrote, never an inferred heuristic (§1 "not an agent").

This scopes what exploration *attempts*, and is deliberately independent of, and
never a substitute for, the sandbox-only destructive-action gate (`safety.py`): an
include pattern that happens to match a destructive action's label does not relax
that non-negotiable — both the element rules and the safety gate must separately
allow an action before the explorer fires it (ROADMAP.md §2e non-negotiable,
CLAUDE.md). The caller (the explorer loop) is responsible for applying both checks;
nothing here reads or touches the sandbox registry.

Patterns are matched case-sensitively (`fnmatch.fnmatchcase`), the same choice the
scoped-crawl `include`/`exclude` glob fields make, for the same reason: a pattern
means exactly what it says, with no locale-dependent case folding to surprise an
operator who wrote it to match a label verbatim.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass

from spoor.exploration.discovery import ActionableElement

NOT_INCLUDED_SKIP_REASON = "skipped: did not match an --include-element pattern"
EXCLUDED_SKIP_REASON = "skipped: matched an --exclude-element pattern"


@dataclass(frozen=True)
class RuleDecision:
    """The element rules' verdict for one candidate action: attempt it, or skip it."""

    allowed: bool
    reason: str


_ALLOWED = RuleDecision(allowed=True, reason="element rules permit this action")


def _matches_any(patterns: tuple[str, ...], label: str) -> bool:
    return any(fnmatch.fnmatchcase(label, pattern) for pattern in patterns)


@dataclass(frozen=True)
class ElementRules:
    """An operator's allow/exclude list for which elements exploration attempts.

    `include`/`exclude` are glob patterns (`fnmatch`) matched against an element's
    visible accessible label. Left unset (the default, `None`), every discovered
    element is a candidate — today's behavior, unchanged. When `exclude` matches,
    the action is skipped regardless of `include` (exclude wins, the same
    composition rule the scoped-crawl `include`/`exclude` fields use); when
    `include` is set and nothing in it matches, the action is skipped; otherwise
    it is permitted to proceed to the separate sandbox-only safety gate.
    """

    include: tuple[str, ...] | None = None
    exclude: tuple[str, ...] | None = None

    def evaluate(self, element: ActionableElement) -> RuleDecision:
        """Decide whether these rules permit attempting `element` (§2e, #152)."""
        if self.exclude and _matches_any(self.exclude, element.name):
            return RuleDecision(allowed=False, reason=EXCLUDED_SKIP_REASON)
        if self.include and not _matches_any(self.include, element.name):
            return RuleDecision(allowed=False, reason=NOT_INCLUDED_SKIP_REASON)
        return _ALLOWED
