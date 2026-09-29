# Live URL reporting for the crawl frontier — ROADMAP.md §2e (slice 9).
#
# The live half of slice 9. exploration_traversal.feature pins the pure breadth-first
# walk, the depth bound, and the URL-path frontier fork against a fake site; but the
# fork is worth nothing unless the real driver actually reports the page URL — and
# reports it *after* a navigation, not the stale entry URL. This scenario proves that
# end to end in a headless browser: the real PlaywrightDriver's current_url tracks a
# real navigation from one page to the next, which is the signal the explorer forks on.
#
# The second scenario is the live half of the destination-hint prioritisation (slice
# 9b): the real driver must read a link's href off the page and report it as a URL-path
# destination on the discovered element, so the explorer can order the walk by depth.
#
# The third scenario is the live half of the input_type enrichment (interactive-round
# scaffold, slice 1, issue #131): the real driver must read a text field's DOM `type`
# attribute off the page, so a future scaffold generator can tell a login field
# (type="password") apart from any other text box — the accessibility tree alone
# reports both identically as role="textbox". It runs against its own dedicated
# fixture (explore_login.html), not the two-page one, so it doesn't perturb the
# state/transition counts exploration_browser.feature hardcodes for that fixture.
#
# Nothing here is site-specific (§0): current_url reads Playwright's live page URL for
# every target, the destination is read generically from each anchor's href, and the
# input type is read generically from each <input>'s type attribute.

@browser
Feature: The live driver reports the current page URL for the crawl frontier
  As the exploration engine forking its frontier on the URL path
  I want the driver to report the URL of the page actually loaded now
  So that a navigation to a distinct page is seen as a distinct thing to explore

  Scenario: The reported URL tracks a navigation from one page to the next
    Given a live browser on the traversal fixture "explore_home.html"
    Then the driver reports a current URL ending in "explore_home.html"
    When I actuate the "link" named "Open next"
    Then the driver reports a current URL ending in "explore_next.html"

  Scenario: The driver reads a link's destination path from its href
    Given a live browser on the traversal fixture "explore_home.html"
    Then the discovered "link" named "Open next" has destination "/explore_next.html"

  Scenario: The driver reads a text field's DOM input type
    Given a live browser on the traversal fixture "explore_login.html"
    Then the discovered "textbox" named "Password" has input type "password"
