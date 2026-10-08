# Exploration settling also waits while a loading indicator is on screen — §2e (7g).
#
# 7b settles on DOM quiescence, 7e widens "is the page quiet?" to the network, and 7f to
# urgent announcements. A maintainer report showed a fourth capture-timing race: a
# React/MUI app shows a loading screen (one indeterminate spinner) for about half a
# second after every load, with no DOM mutation and no request in flight (the spinner
# is a CSS animation; the delay a client-side timer). DOM-quiet and network-idle both
# fire during that lull, so a capture reads the loading screen instead of the real one.
# The first capture of the run happened to read the real screen and every reset read
# the spinner, so reset-and-replay (7d) found "reset did not return to the start state"
# for all 20 actions and mapped a single state.
#
# 7g treats a *visible loading indicator* as page activity: an element marked
# aria-busy="true", an indeterminate role="progressbar" (no aria-valuenow), or an HTML
# <progress> without a value. Deliberately narrow, as 7f was: a progress bar that shows
# a value is durable status (that app keeps one at 0 on its finished screen) and never
# holds the wait, and an indicator that isn't displayed doesn't count. The bound is
# unchanged: an indicator that never clears leaves the page unsettled at the safety
# timeout, recorded, never a hang. Nothing here is site-specific (§0): the rule keys on
# standard accessibility semantics, the same for every target.

Feature: Exploration waits for a loading indicator to clear before it reads the page
  As the exploration engine mapping a page that shows a spinner while it loads
  I want the settle wait to treat a visible loading indicator as page activity
  So that a capture reads the loaded screen, not the loading screen, and a reset
  returns to the same start state every time

  Scenario: A loading indicator holds the page unsettled until it clears
    # DOM quiet and network idle the whole time, but a spinner is on screen until
    # 600 ms. The wait must not settle during the lull; only after the spinner goes and
    # a further quiet window passes.
    Given a quiet window of 200 ms and a settle timeout of 5000 ms
    And a page whose DOM is quiet but a loading indicator is showing until 600 ms
    When the explorer waits for the page to settle
    Then it reports the page settled
    And the wait lasted at least 600 ms
    And it did not wait the full timeout

  Scenario: A loading indicator that never clears is reported unsettled, not hung
    Given a quiet window of 200 ms and a settle timeout of 1000 ms
    And a page whose DOM is quiet but a loading indicator never clears
    When the explorer waits for the page to settle
    Then it reports the page did not settle
    And the wait ended at the timeout

  @browser
  Scenario: A capture waits for a loading spinner to give way to the real screen
    # The entry page first shows only an indeterminate spinner, then (past the quiet
    # window, with no request in flight) replaces it with the real screen and its
    # button. Settling on DOM-quiet alone would read the spinner screen.
    Given a live site whose entry page shows an indeterminate spinner before its content
    When the explorer resets the browser
    Then the discovered actions include the "button" named "Start job"

  @browser
  Scenario: A capture waits for an aria-busy region to finish loading
    Given a live site whose entry page marks its content aria-busy while it loads
    When the explorer resets the browser
    Then the discovered actions include the "button" named "Start job"

  @browser
  Scenario: A progress bar showing a value, or a hidden spinner, never holds the wait
    # A durable status gauge (aria-valuenow set) and a spinner that isn't displayed
    # stay in the page forever; neither means "still loading", so the settle wait
    # finishes promptly instead of running to the timeout.
    Given a live site whose settled page keeps a determinate progress bar and a hidden spinner
    When the explorer resets the browser
    Then the reset settled well before the settle timeout
    And the discovered actions include the "button" named "Start job"
