# Bring-your-own-session for `spoor explore` — ROADMAP.md §2e, §2h (issue #164).
#
# `spoor run` already supported a supplied session (`session.feature`); exploration
# mode did not, because `PlaywrightDriver.reset()` deliberately clears cookies and
# web storage before every navigation so a reset is always a true first visit
# (§2e, 7b) -- which would silently wipe a session loaded only at context creation.
# The fix makes a supplied session survive every reset: cookies are re-added after
# each clear, and localStorage is restored via an init script that runs before any
# page script on every document the context loads.
#
# The fixture server gates a link to a second page on a cookie, and that second
# page in turn gates a link to a *third* page on a localStorage token -- so mapping
# past both pages needs both mechanisms to survive not just the first page load,
# but the second and third resets reset-and-replay performs while exploring. Spoor
# never logs in itself (§2h, §0): the session below is supplied, already captured.

@browser
Feature: Exploring a live, login-gated site with a supplied session
  As an operator with a session I already captured myself
  I want spoor explore to replay it across the whole crawl
  So that a login-gated site's real content is mapped, not just its login screen

  Scenario: Without a session, the crawl never gets past the gate
    Given an auth-gated fixture server whose deeper pages need a cookie then a token
    When I run spoor explore against it with no session
    Then it reports 1 states discovered
    And it reports 0 transitions

  Scenario: A cookie-only session reaches the second page but not the third
    Given an auth-gated fixture server whose deeper pages need a cookie then a token
    And a session file carrying only the server's cookie
    When I run spoor explore against it with that session
    Then it reports 2 states discovered
    And it reports 1 transitions

  Scenario: A full session survives every reset, reaching every gated page
    Given an auth-gated fixture server whose deeper pages need a cookie then a token
    And a session file carrying both the cookie and the localStorage token
    When I run spoor explore against it with that session
    Then it reports 3 states discovered
    And it reports 2 transitions
