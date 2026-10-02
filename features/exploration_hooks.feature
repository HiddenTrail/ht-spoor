# Operator-supplied exploration hooks (ROADMAP.md §2e, closes #187).
#
# Part 2 of #150: a way to extend an exploration run — observe a newly
# discovered state, observe a fired transition — without writing site-specific
# code into Spoor itself. Hooks are plain Python callables supplied the same
# way `explore()`'s existing `progress` callback already is
# (`explore(..., hooks=...)`), not a config/CLI flag, since a hook is code.
#
# Two safety properties this file proves, not just documents: a hook fires
# only after its state/transition is already committed to the graph and the
# §2e destructive-action gate has already decided (so a destructive action
# skipped outside a sandbox is never offered to `on_transition_taken` at
# all — there is no transition to report), and a hook only ever receives a
# redaction-safe view — counts and `redact()`-passed text — never a raw
# captured console line, storage value, or network request.

Feature: Exploration hooks observe discovered states and recorded transitions
  As someone running exploration as a library
  I want to observe each newly discovered state and fired transition
  So that I can extend a run without writing site-specific code into Spoor itself

  Background:
    Given an app whose actions are:
      | from  | label      | role | to   |
      | start | Go to page | link | page |

  Scenario: on_state_discovered fires once per newly discovered state
    When I explore from "start" with hooks recording discovered states
    Then the hook recorded 2 discovered states
    And the hook recorded "start" exactly once

  Scenario: on_transition_taken fires once per recorded transition
    When I explore from "start" with hooks recording transitions
    Then the hook recorded 1 transition
    And the hook recorded a transition "start --Go to page--> page"

  Scenario: A hook never sees a raw captured secret, only redacted text
    Given the state "page" carries a console message with a bearer token
    When I explore from "start" with hooks recording transitions
    Then the hook's recorded transition carries no raw token
    And the hook's recorded transition carries the redacted marker

  Scenario: A destructive action skipped outside a sandbox offers no transition to any hook
    Given the action "Delete account" leads to a new state
    And the target is a real, non-sandbox site
    When I explore from "start" with hooks recording transitions
    Then the hook recorded no transition for "Delete account"

  Scenario: Omitting hooks entirely reproduces today's behavior unchanged
    When I explore from "start" with no hooks
    Then the graph has 2 states

  @browser
  Scenario: Hooks fire the same way against a real browser-driven exploration
    Given a live browser on the exploration fixture "explore_home.html"
    When I explore it live with hooks recording states and transitions
    Then the hook recorded 2 discovered states
    And the hook recorded 2 transitions
