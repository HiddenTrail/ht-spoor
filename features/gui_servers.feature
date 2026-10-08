# Local GUI, slice gui-4: server controls — ROADMAP.md §2i.
#
# The Servers page starts and stops the map API server (`spoor serve`) as a
# supervised job: the real command, on this computer only (there is no host
# field), at most one at a time, shown as running only once it actually
# answers its own health check. For AI agents it shows a ready-to-paste MCP
# configuration for `spoor serve-mcp` instead of running it: an MCP client
# launches that itself, over stdio.
#
# An MCP client starts the server in a folder of its own choosing, so the
# configuration tells it where this GUI's maps are through SPOOR_CACHE_DIR, the
# environment variable that sets Spoor's local cache location (gui-4 mechanics
# decision; the cache stays on this computer either way).
#
# Nothing here is site-specific (§0).

Feature: Controlling Spoor's map servers from the local GUI
  As an operator who would rather not use the command line
  I want to start the map API server and set up MCP for my agents from the browser
  So that scripts and AI agents can use what Spoor mapped, without a terminal

  Background:
    Given the GUI app is running jobs with a fake runner

  # --- The map API server -------------------------------------------------------

  Scenario: Starting the map server runs spoor serve on this computer only
    When I start the map server on port "8123"
    Then the fake runner was started with "serve --port 8123"
    And I am taken back to the servers page

  Scenario: The map server can be started with re-checking allowed
    When I start the map server on port "8123" with re-checking allowed
    Then the fake runner was started with "serve --port 8123 --recheck"

  Scenario: The form has no way to choose a non-local address
    When I open the servers page
    Then the page has no field for the server's address

  Scenario Outline: A port that isn't a valid port is refused and nothing starts
    When I start the map server on port "<port>"
    Then the response status is 400
    And the page says "The port must be a whole number from 1 to 65535."
    And the fake runner was never started

    Examples:
      | port  |
      | 0     |
      | 65536 |
      | http  |
      |       |

  Scenario: A server that doesn't answer yet is shown as starting
    Given the fake command keeps running until it is killed
    And the map server's health check does not answer yet
    When I start the map server on port "8123"
    And I open the servers page
    Then the page says the map server is starting

  Scenario: A server that answers its health check is shown as running, with its address
    Given the fake command keeps running until it is killed
    And the map server's health check answers
    When I start the map server on port "8123"
    And I open the servers page
    Then the page says the map server is running at "http://127.0.0.1:8123"
    And the page links to "http://127.0.0.1:8123/domains"

  Scenario: Only one map server runs at a time
    Given the fake command keeps running until it is killed
    When I start the map server on port "8123"
    And I start the map server on port "8124"
    Then the response status is 400
    And the page says "A map server is already running"
    And the fake runner was started 1 time

  Scenario: Stopping the map server ends it
    Given the fake command keeps running until it is killed
    And the map server's health check answers
    When I start the map server on port "8123"
    And I stop the map server
    Then the fake process was killed
    And the page says the map server is not running

  Scenario: A server that fails to start shows why
    Given the fake command will print "error while attempting to bind on address" and exit 1
    When I start the map server on port "8123"
    And the server job finishes
    And I open the servers page
    Then the page says the map server stopped with an error
    And the page shows "error while attempting to bind on address"

  Scenario: Another site can't start a map server
    When another site starts the map server on port "8123"
    Then the response status is 403
    And the fake runner was never started

  # --- MCP for AI agents --------------------------------------------------------

  Scenario: The servers page shows a ready-to-paste MCP configuration
    When I open the servers page
    Then the MCP configuration runs "-m spoor.cli serve-mcp" with this Python
    And the MCP configuration sets SPOOR_CACHE_DIR to this GUI's cache folder as an absolute path
    And the page shows the claude mcp add command for the same server

  Scenario: The pasted MCP configuration serves this GUI's maps, wherever it is started
    Given a map store that has mapped "https://shop.example/products"
    When an MCP client runs the configuration from the servers page in an unrelated folder
    Then the MCP server lists the mapped site "shop.example"

  # --- Where Spoor keeps its local cache ------------------------------------------

  Scenario: SPOOR_CACHE_DIR sets where Spoor keeps its local cache
    When Spoor starts with SPOOR_CACHE_DIR set to a folder
    Then its local cache is that folder

  Scenario: Without SPOOR_CACHE_DIR, the cache stays in the working folder
    When Spoor starts without SPOOR_CACHE_DIR
    Then its local cache is ".spoor-cache" in the working folder

  # --- End to end in a real browser ----------------------------------------------

  @browser
  Scenario: Starting, using and stopping the map server from a real browser
    Given the GUI is running on loopback with the real command runner
    And a map store that has mapped "https://shop.example/products"
    When a real browser starts the map server on a free port
    Then the browser shows the map server running
    And the running server lists the mapped site "shop.example"
    When the browser stops the map server
    Then the server no longer answers
