# Typing-only consumption of a filled interactive-round scaffold — ROADMAP.md §2e,
# issue #131 follow-on.
#
# Issue #131 shipped scaffold *generation* only. This is the first, deliberately
# narrow slice of *consuming* one: given a scaffold a human has filled in, navigate to
# each field's recorded state — replaying the same reset-and-replay path exploration
# itself used to reach it (spoor/testgen/pytest_gen.py's generated tests already prove
# this pattern) — and type its pinned value in. Never presses Enter, never clicks a
# submit control, never applies the value in any way. This stays entirely inside the
# maintainer-approved exception docs/ROADMAP.md §2e records ahead of keyword-list
# localization (#101): typing a value isn't a DESTRUCTIVE_KEYWORDS match, and applying
# one is still fully blocked on #101.
#
# One field's failure (an unresolved state, a field no longer there, a vanished or
# covered element) is reported and the rest still run — the explorer's own
# skip-and-continue posture, never an abort on one bad entry. Nothing here is
# site-specific (§0): one applier for every target.
#
# When a fill actually changes the page, that's observed the same read-only way
# exploration observes after any click (issue #137) and recorded as a real graph
# edge — a new state and a transition whose action carries the typed value, so it is
# replayable and clearly distinguishable from a clicked one, never a second-class or
# unreachable addition. A fill with no observable effect adds nothing new, same as
# before this was built.

Feature: Type a filled-in interactive-round scaffold's values into their fields
  As a team that has filled in a scaffold Spoor generated
  I want each pinned value typed into its recorded field
  So that I can see the value land before anything about applying it is built

  Background:
    Given a mapped graph with a field "Email" on state "home"

  Scenario: Production targets are rejected before any browser interaction
    Given the scaffold pins "Email" on "home" to "jane@example.com"
    And the apply target is not a sandbox
    When I apply the scaffold
    Then no field was applied
    And the driver was not reset

  Scenario: Numeric YAML values produce an actionable failure
    Given the scaffold contains an unquoted numeric value
    When I apply the scaffold
    Then "Email" on "home" failed with reason "value must be a quoted YAML string"

  Scenario: Multiple fields share one page visit
    Given another field "Nickname" on "home"
    And the scaffold pins "Email" on "home" to "jane@example.com"
    And the scaffold pins "Nickname" on "home" to "fox"
    When I apply the scaffold
    Then the driver was reset exactly once
    And the driver typed "jane@example.com" into "Email"
    And the driver typed "fox" into "Nickname"

  Scenario: A reset failure is reported for every affected field
    Given the scaffold pins "Email" on "home" to "jane@example.com"
    And resetting the apply driver fails
    When I apply the scaffold
    Then "Email" on "home" failed with reason "reset failed"

  Scenario: Navigation clicks are outside the typing-only exception
    Given a field on a state reached by clicking
    And the scaffold pins "Email" on "detail" to "jane@example.com"
    When I apply the scaffold
    Then "Email" on "detail" failed with reason "navigation replay is outside the typing-only scope"

  Scenario: A filled field is typed into the correct state
    Given the scaffold pins "Email" on "home" to "jane@example.com"
    When I apply the scaffold
    Then "Email" on "home" was applied
    And the driver typed "jane@example.com" into "Email"
    And the driver replayed the path to "home" before typing

  Scenario: A blank value is skipped, never applied
    Given the scaffold pins "Email" on "home" to a blank value
    When I apply the scaffold
    Then no field was applied
    And no field failed

  Scenario: An unresolved state prefix is reported, never guessed
    Given the scaffold pins "Email" on "nonexistent" to "jane@example.com"
    When I apply the scaffold
    Then "Email" on "nonexistent" failed with reason "state prefix did not resolve to exactly one mapped state"

  Scenario: A field no longer on its state is reported, never guessed
    Given the scaffold pins "Vanished field" on "home" to "anything"
    When I apply the scaffold
    Then "Vanished field" on "home" failed with reason "no matching field on this state"

  Scenario: A scaffold with no applicable fields applies nothing
    Given an empty scaffold
    When I apply the scaffold
    Then no field was applied
    And no field failed

  Scenario: A fill that changes the page adds a real, typed graph edge
    Given the scaffold pins "Email" on "home" to "jane@example.com"
    And filling a field on this driver reveals a new page
    When I apply the scaffold
    Then "Email" on "home" was applied
    And a new state was added to the graph
    And its incoming transition was typed with "jane@example.com", not clicked

  Scenario: A fill with no observable effect adds nothing new to the graph
    Given the scaffold pins "Email" on "home" to "jane@example.com"
    When I apply the scaffold
    Then "Email" on "home" was applied
    And no new state was added to the graph

  @browser
  Scenario: A live crawl's field is typed into and the DOM value actually changes
    Given a live crawl of "explore_login.html" was mapped at depth 1
    And the scaffold pins "Nickname" on the crawled state to "trail-fox"
    When I apply the scaffold against the live driver
    Then the live page's "Nickname" field now reads "trail-fox"

  @browser
  Scenario: A read-only field's non-change is reported, never claimed a success
    Given a live crawl of "explore_login.html" was mapped at depth 1
    And the live field to check is "#account-id"
    And the scaffold pins "Account ID" on the crawled state to "ACC-002"
    When I apply the scaffold against the live driver
    Then no field was applied
    And the live page's "Account ID" field still reads "ACC-001"
