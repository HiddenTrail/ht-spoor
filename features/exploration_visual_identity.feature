# Visual state identity — ROADMAP.md §9, closes #104.
#
# State identity (`spoor/exploration/state.py:state_id`) normalizes and hashes a
# page's DOM/text alone — it has no visual component. Two screens that are
# genuinely different to look at (a modal overlay, a color-only status change)
# but whose DOM and text normalize identically therefore collapse into a single
# mapped state today, undercounting the real state-action graph.
#
# This slice folds the perceptual screenshot hash already captured per state
# (`StateSignals.screenshot_hash`) into how a revisit is told apart from a new
# state — without changing `state_id()` itself (it stays DOM/text-only, so every
# existing scenario in exploration_state.feature is untouched) and without
# requiring a locale/flag to declare visual identity on: it is opportunistic,
# based only on whatever screenshot hash the driver happens to produce.
#
# The cost model is deliberate, not incidental (confirmed with the maintainer):
# every state but the root is reached by firing an action, which already
# captures a before/after signal bundle for the transition diff — that bundle is
# reused as the revisit probe, so splitting a visual variant costs zero extra
# driver calls in the walk's normal path. The one exception is a *resumed* run's
# root, which already lives in the loaded map: confirming it costs one extra
# capture, once per resume — harmless, since the visual-variant map starts empty
# every run and so can never find a baseline to split against there, but a real,
# documented cost rather than a silently-claimed zero (see the explorer.py
# decision note). A driver that never produces a screenshot hash (or a DOM id
# with no recorded hash to compare against at all) falls back to the original
# DOM-only dedup, byte-for-byte.
#
# Resume/replay verification deliberately stays DOM-only (out of scope here,
# see the decision note) — a narrower first cut, not an oversight.

Feature: Visually distinct screens that share a DOM hash become distinct states
  As the exploration engine mapping a target with no config
  I want a screenshot hash to split apart two screens whose DOM looks identical
  So that a modal, overlay, or color-only change isn't silently folded into one state

  Scenario: Two DOM-identical visits with different screenshots become two states
    Given an app whose actions are:
      | from | label  | role | to    |
      | home | Go A   | link | lobby |
      | home | Go B   | link | lobby |
    And "lobby" is screenshotted as "hashA" then "hashB"
    When I explore from "home"
    Then the graph has 3 states
    And "Go A" and "Go B" lead to different states

  Scenario: Two DOM-identical visits with the same screenshot stay one state
    Given an app whose actions are:
      | from | label  | role | to    |
      | home | Go A   | link | lobby |
      | home | Go B   | link | lobby |
    And "lobby" is screenshotted as "hashA" then "hashA"
    When I explore from "home"
    Then the graph has 2 states
    And "Go A" and "Go B" lead to the same state

  Scenario: With no screenshot hash available, revisits dedup exactly as before
    Given an app whose actions are:
      | from | label  | role | to    |
      | home | Go A   | link | lobby |
      | home | Go B   | link | lobby |
    And "lobby" is never screenshotted
    When I explore from "home"
    Then the graph has 2 states
    And "Go A" and "Go B" lead to the same state

  Scenario: A genuinely new state adds no capture beyond the existing before/after diff
    # 3 = capturing the root, plus the before/after pair already taken around firing
    # "Go" to compute its transition diff (an existing mechanism, unrelated to visual
    # identity) — landing on a brand-new state reuses the "after" bundle rather than
    # capturing a fourth time.
    Given an app whose actions are:
      | from | label | role | to   |
      | home | Go    | link | page |
    When I explore from "home"
    Then exactly 3 signal captures were taken

  Scenario: Splitting off a new visual variant adds no capture beyond the existing before/after diff
    # 5 = capturing the root, plus a before/after pair for each of the two actions
    # fired from it — confirming "lobby" is a new visual variant (not a dedup) and
    # recording it both reuse the second pair's "after" bundle as the probe, rather
    # than taking a capture of their own.
    Given an app whose actions are:
      | from | label  | role | to    |
      | home | Go A   | link | lobby |
      | home | Go B   | link | lobby |
    And "lobby" is screenshotted as "hashA" then "hashB"
    When I explore from "home"
    Then exactly 5 signal captures were taken
