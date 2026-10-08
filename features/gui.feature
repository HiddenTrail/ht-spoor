# Local GUI, slice gui-1: the shell, its security posture, and browsing maps — ROADMAP.md §2i.
#
# `spoor gui` starts a local web app and opens the operator's browser on it, so
# Spoor can be operated without the command line. This first slice is
# deliberately read-only: it lists mapped domains and shows a URL's map. It
# can't start a run or touch a target. It also holds the introduction page the
# GUI opens on (clicking "Spoor" returns to it): what Spoor is, what it does,
# who it's for, how it stays safe, where to start, and a link to the repository. Running jobs (gui-2), sessions and
# configs (gui-3), and server controls (gui-4) arrive in their own .feature
# files.
#
# The GUI is a separate local CONTROL PLANE, not part of the §2f serving layer:
# it lives in spoor/gui/, and spoor/serving/ gains no route, tool or flag for it.
# It reuses the serving layer's shared `views.map_view`, so a map looks exactly
# as redacted in the GUI as it does over REST/MCP (§2h) — secrets stay
# [REDACTED] even on the operator's own screen.
#
# Security posture (§2i, decided as part of the capability, not later
# hardening): loopback-only bind with no host option; a random per-launch access
# token, handed to the browser once in the launch URL and then held in an
# HttpOnly, SameSite=Strict cookie; and Host/Origin checks against DNS
# rebinding and cross-site requests.
#
# Nothing here is site-specific (§0).

Feature: A local GUI browses captured maps safely
  As an operator who would rather not use the command line
  I want to open Spoor in my browser and look through what it has mapped
  So that I can see a site's map without remembering commands or flags,
  and without any other local process or web page being able to drive Spoor

  Background:
    Given a map store that has mapped "https://shop.example/products"
    And the GUI app is created with a known access token

  # --- Security posture -----------------------------------------------------

  Scenario: The GUI only ever binds to loopback
    When I ask the GUI launcher to bind to "0.0.0.0"
    Then the launch is refused with a message that the GUI is local-only

  Scenario: The launch URL hands the token to the browser once, as a cookie
    When I open the launch URL carrying the access token
    Then I am redirected to the home page without the token in the URL
    And the response sets an HttpOnly, SameSite=Strict token cookie

  Scenario: A request without the access token is rejected
    When I request the home page without the access token
    Then the response status is 403

  Scenario: A request with a wrong access token is rejected
    When I request the home page with the access token "not-the-token"
    Then the response status is 403

  Scenario: A request whose Host header is not loopback is rejected
    When I request the home page with the access token and Host header "evil.example"
    Then the response status is 403

  Scenario: A form submission from another site is rejected
    When I POST to the home page with the access token and Origin "https://evil.example"
    Then the response status is 403

  Scenario: The GUI adds nothing to the read-only serving layer
    Then the read-only serving app's routes are unchanged by the GUI

  # --- The introduction page ----------------------------------------------

  Scenario: Clicking Spoor opens an introduction to the product
    When I request the home page with the access token
    Then the page introduces Spoor with what it is for
    And the page describes what Spoor does and who it is for
    And the page says how Spoor stays safe by default
    And the page links to the Spoor repository
    And the top bar's Spoor logo links to the introduction and Maps to the maps page

  Scenario: The introduction says where to start and how much is mapped
    When I request the home page with the access token
    Then the page links to exploring a site, extracting, the maps and the servers
    And the page says 1 site is mapped so far

  Scenario: Pages carry the Spoor logo in the top bar and as the browser-tab icon
    When I request the home page with the access token
    Then the page shows the Spoor logo in the top bar and as its browser-tab icon

  Scenario: Pages offer a day/night switch and follow the system by default
    When I request the home page with the access token
    Then the page has the day/night switch and follows the system setting
    And the page carries the night logo and the day logo, one shown per mode

  # --- Browsing maps --------------------------------------------------------

  Scenario: The maps page lists every mapped domain
    When I open the maps page with the access token
    Then the page lists the domain "shop.example"

  Scenario: An empty store shows a getting-started message, not an error
    Given an empty map store
    When I open the maps page with the access token
    Then the response status is 200
    And the page says nothing has been mapped yet

  Scenario: A domain page lists that domain's mapped URLs
    When I open the domain page for "shop.example" with the access token
    Then the page links to the map for "https://shop.example/products"

  Scenario: A map page shows when the URL was captured and how old that is
    When I open the map page for "https://shop.example/products" with the access token
    Then the page shows the capture time and its age

  Scenario: A map page shows the URL's records
    When I open the map page for "https://shop.example/products" with the access token
    Then the page shows the mapped records

  Scenario: A secret in a mapped record is shown redacted in the GUI
    Given the mapped records for "https://shop.example/products" contain "Bearer abc.def.ghi"
    When I open the map page for "https://shop.example/products" with the access token
    Then the page shows "[REDACTED]"
    And the page never shows "abc.def.ghi"

  Scenario: A map page shows the exploration graph with its safety-gate skips
    Given "https://shop.example/products" has an explored graph with a skipped destructive action
    When I open the map page for "https://shop.example/products" with the access token
    Then the page lists the graph's states and transitions
    And the page lists the skipped action with its reason

  Scenario: An unmapped URL shows a not-mapped page, never a made-up map
    When I open the map page for "https://shop.example/unmapped" with the access token
    Then the response status is 404
    And the page says the URL has not been mapped

  # --- End to end in a real browser ------------------------------------------

  @browser
  Scenario: Day and night in a real browser, remembered across GUI launches
    Given the GUI is running on loopback
    When a real browser set to light mode opens the launch URL
    Then the page is in day mode with the day logo
    When the browser switches to night mode
    Then the page is in night mode with the night logo
    When the GUI is restarted on another port and the browser opens it again
    Then the page is in night mode with the night logo

  @browser
  Scenario: Launching the GUI and opening a mapped domain in a real browser
    Given the GUI is running on loopback
    When a real browser opens the launch URL
    And opens the maps page
    And clicks the domain "shop.example"
    And clicks the mapped URL "https://shop.example/products"
    Then the browser shows the map for "https://shop.example/products"
