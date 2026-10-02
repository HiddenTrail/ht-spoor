# Resumable, persisted crawl state (ROADMAP.md §2d, closes #175).
#
# A `crawl:`-driven run (or a plain `pagination.next` chain) has no way to pick
# up where an earlier run left off by default — every run starts its frontier
# fresh from the target. Opting in (`resume: true`) persists the set of URLs
# already seen and the remaining frontier to the local-only cache at the end
# of a run, and continues from it on the next one instead of restarting.
#
# This deliberately reuses neither §2e's exploration-mode `--resume-from`
# (a state-graph model needing anchor resolution and a live browser replay —
# the wrong shape for a flat URL frontier) nor change detection (a resumed run
# never re-checks an already-visited URL; it only continues past where the
# frontier stopped — re-verifying old pages is `change_detection`'s job, a
# separate, already-existing feature combo). Scope is both tiers, since the
# frontier/seen shape is identical in each and persistence only touches it
# before the loop starts and after it ends.

Feature: A crawl resumes its frontier from where an earlier run left off
  As someone running a large crawl across several invocations
  I want a resumed run to continue past where the last one stopped
  So that I never re-fetch a page already visited, and never lose progress

  Background:
    Given a fixture server with an index page linking to 4 item pages

  Scenario: A run that hit its page cap persists the remaining frontier
    Given resume is enabled and the per-run page cap is 2
    When I run the crawl
    Then exactly 2 pages were fetched
    And a resumable frontier was persisted for the target

  Scenario: A resumed run continues past where the capped run stopped
    Given resume is enabled and the per-run page cap is 2
    And a first run already hit that cap
    When I resume the crawl with no page cap
    Then the resumed run fetches only the 3 pages the first run never reached
    And none of the first run's pages are fetched again

  Scenario: A run that completes on its own clears its persisted state
    Given resume is enabled
    And a first run already completed the whole crawl
    When I run the crawl again
    Then every page is fetched again, not skipped as already done

  Scenario: Without resume enabled, nothing persists across runs
    Given resume is not configured
    When I run the crawl twice
    Then every page is fetched again on the second run
    And no resumable frontier file exists for the target

  @browser
  Scenario: A resumed run continues past where the capped run stopped, in the browser tier
    Given resume is enabled and the per-run page cap is 2
    And a first browser run already hit that cap
    When I resume the crawl in the browser tier with no page cap
    Then the resumed run fetches only the 3 pages the first run never reached
