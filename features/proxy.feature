# Bring-your-own-proxy (ROADMAP.md §2d).
#
# Spoor never discovers or provides a proxy itself — only routes a run through
# one already in hand, the same bring-your-own posture as `session:` for
# authenticated targets (session.feature). Set via the config's `proxy:`
# block, it reaches every outbound fetch a run makes: the static tier's httpx
# client, the browser tier's own httpx client (used for the politeness gate's
# robots.txt and sitemap requests, since it reuses that same client), and the
# browser tier's Chromium process. Omitted entirely, nothing changes — a run
# connects directly, exactly as it always has.

Feature: A run routes its traffic through a supplied proxy (bring-your-own-proxy)
  As someone scraping from a network where direct requests are blocked or unwanted
  I want to hand Spoor a proxy I already have
  So that a run's traffic goes through it, without Spoor sourcing a proxy itself

  Scenario: A static run routes its fetch through the supplied proxy
    Given a target fixture server
    And a forwarding proxy server
    When I run a static config naming that proxy
    Then the proxy server received the request
    And the item is extracted

  Scenario: A static run with no proxy configured connects directly
    Given a target fixture server
    And a forwarding proxy server
    When I run a static config with no proxy
    Then the proxy server received no request
    And the item is extracted

  Scenario: Supplied proxy credentials travel with the request
    Given a target fixture server
    And a forwarding proxy server that requires a username and password
    When I run a static config naming that proxy with credentials
    Then the proxy server saw the matching credentials

  @browser
  Scenario: The browser tier routes its traffic through the supplied proxy
    Given a target fixture server
    And a forwarding proxy server
    When I run a browser config naming that proxy
    Then the proxy server received the request
    And the item is extracted
