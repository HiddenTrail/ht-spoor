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

Feature: Type a filled-in interactive-round scaffold's values into their fields
  As a team that has filled in a scaffold Spoor generated
  I want each pinned value typed into its recorded field
  So that I can see the value land before anything about applying it is built

  Background:
    Given a mapped graph with a field "Email" on state "home"

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

  @browser
  Scenario: A live crawl's field is typed into and the DOM value actually changes
    Given a live crawl of "explore_login.html" was mapped at depth 1
    And the scaffold pins "Nickname" on the crawled state to "trail-fox"
    When I apply the scaffold against the live driver
    Then the live page's "Nickname" field now reads "trail-fox"
