# User-configurable clickable-element rules for exploration — ROADMAP.md §2e,
# closes #152.
#
# docs/COMPETITIVE_PLAN.md flags Crawljax's clickable-element rules (incl.
# exclusions) as worth adapting: an explicit, user-set allow/exclude list for which
# actionable elements exploration mode is willing to attempt, matched against each
# element's visible label — an explicit rule the operator wrote, never an inferred
# heuristic (§1 "not an agent").
#
# Scoping, not permission (§2e non-negotiable, unaffected by this capability): these
# rules only narrow what exploration *attempts*. The sandbox-only destructive-action
# gate (exploration_safety.feature) still applies to whatever passes this filter —
# an --include-element pattern that happens to match a destructive label can never
# make it fire on a non-sandbox target; both checks must independently allow an
# action before the explorer performs it.

Feature: Element rules scope which actionable elements exploration attempts
  As someone pointing exploration at a target
  I want to set include/exclude label patterns for which elements it clicks
  So that exploration stays scoped to what I actually want mapped

  Scenario: With no rules set, every discovered element is attempted
    Given a sandbox target
    And an app whose actions are:
      | from | label        | role   | to   |
      | home | Add to cart  | button | cart |
      | home | View details | button | info |
    When I explore from "home"
    Then the graph has a transition "home --Add to cart--> cart"
    And the graph has a transition "home --View details--> info"

  Scenario: An include pattern limits exploration to matching elements
    Given a sandbox target
    And an include pattern "Add to cart*"
    And an app whose actions are:
      | from | label        | role   | to   |
      | home | Add to cart  | button | cart |
      | home | View details | button | info |
    When I explore from "home"
    Then the graph has a transition "home --Add to cart--> cart"
    And the action "View details" from "home" is skipped

  Scenario: An exclude pattern blocks matching elements, others still fire
    Given a sandbox target
    And an exclude pattern "*Logout*"
    And an app whose actions are:
      | from | label        | role   | to   |
      | home | Logout       | button | gone |
      | home | View details | button | info |
    When I explore from "home"
    Then the action "Logout" from "home" is skipped
    And the graph has a transition "home --View details--> info"

  Scenario: An exclude pattern wins over a matching include pattern
    Given a sandbox target
    And an include pattern "*"
    And an exclude pattern "*Logout*"
    And an app whose actions are:
      | from | label  | role   | to   |
      | home | Logout | button | gone |
    When I explore from "home"
    Then the action "Logout" from "home" is skipped

  Scenario: Patterns are matched case-sensitively
    Given a sandbox target
    And an include pattern "add to cart*"
    And an app whose actions are:
      | from | label       | role   | to   |
      | home | Add to cart | button | cart |
    When I explore from "home"
    Then the action "Add to cart" from "home" is skipped

  Scenario: An element rule never relaxes the sandbox-only destructive-action gate
    # The §2e non-negotiable holds regardless: an include pattern matching a
    # destructive action's label grants it nothing — the separate sandbox check
    # still blocks it on a real target, exactly as without any element rules set.
    Given a real target
    And an include pattern "Delete*"
    And an app whose actions are:
      | from | label          | role   | to   |
      | home | Delete account | button | gone |
    When I explore from "home"
    Then the action "Delete account" from "home" is skipped

  Scenario: An exclude rule does not stop layer recovery from using the element
    # Scope decision (§2e, #152): element rules narrow the *graph* — which actions
    # become mapped transitions — not the internal layer-recovery mechanism that
    # clears a covering overlay so some *other*, included action can be reached.
    # Excluding "Dismiss" must not leave a covered, included action unreachable.
    Given a sandbox target
    And an exclude pattern "Dismiss"
    And an app whose actions are:
      | from | label | role   | to   |
      | home | Next  | button | away |
    And the "home" state is covered by a layer whose actions are:
      | label   | role   | clears |
      | Dismiss | button | yes    |
    When I explore from "home"
    Then the graph has a transition "home --Next--> away"
