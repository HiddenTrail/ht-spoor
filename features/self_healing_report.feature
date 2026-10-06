# Healing report: surface tier-3 heal events as an actionable report
# (ROADMAP.md §2/§2d, closes #154).
#
# docs/COMPETITIVE_PLAN.md flags Healenium/Testim's healing reports (old locator,
# new locator, confidence, suggested fix) as worth adapting. Tier 3 already
# records a `HealEvent` per heal attempt and `RunSummary` already counts them
# (features/self_healing_runs.feature), but neither names what broke or what
# tier 3 found instead — a heal is a silent runtime recovery, visible only as a
# number. This slice turns the same events into a readable markdown report: per
# field, the selector that stopped matching, the locator tier 3 re-resolved it
# to, its confidence, and — for a confident heal — a suggested config fix.
#
# Confident heals and uncertain matches are reported in separate sections: a
# confident heal's suggestion is something to act on; an uncertain match's best
# guess is something to *review*, never apply blindly (§2, §1 — tier 3 never
# guesses on your behalf, and neither does this report).
#
# Pure-logic scenarios, built directly against `HealEvent` — the engine itself
# (and the wiring that populates `old_selector`/`new_locator` from a real run)
# is pinned by features/self_healing_runs.feature; this file covers only the
# report-rendering step.

Feature: Tier-3 heal events render as a readable healing report
  As someone whose scrape config has drifted from the live site
  I want a report naming what broke and what tier 3 found instead
  So that I can update my config instead of relying on healing forever

  Scenario: A confident heal is reported with its suggested fix
    Given a confident heal of "price" from ".price-old" to ".price-new" with confidence "0.91"
    When I render the healing report
    Then the report lists "price" as a confident heal
    And the report shows the old selector ".price-old" and the suggested selector ".price-new"
    And the report suggests updating the config

  Scenario: An uncertain match is reported separately, flagged for review
    Given an uncertain heal of "sku" from ".sku-old" to ".sku-maybe" with confidence "0.42"
    When I render the healing report
    Then the report lists "sku" as an uncertain match
    And the report says uncertain matches are flagged for review, not applied

  Scenario: Confident heals and uncertain matches are reported in separate sections
    Given a confident heal of "price" from ".price-old" to ".price-new" with confidence "0.91"
    And an uncertain heal of "sku" from ".sku-old" to ".sku-maybe" with confidence "0.42"
    When I render the healing report
    Then the report lists "price" as a confident heal
    And the report lists "sku" as an uncertain match

  Scenario: No heal events produce no report
    Given no heal events this run
    When I render the healing report
    Then no report is rendered

  Scenario: A secret-shaped locator is redacted before it reaches the report
    Given a confident heal of "token" from "#old-id" to "Bearer sk-supersecrettoken12345" with confidence "0.95"
    When I render the healing report
    Then the report does not contain the raw secret "sk-supersecrettoken12345"
