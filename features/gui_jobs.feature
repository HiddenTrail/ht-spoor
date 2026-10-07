# Local GUI, slice gui-2: run jobs (explore / run / apply-scaffold) — ROADMAP.md §2i.
#
# The GUI gets forms for the three commands that act on a site. Submitting one
# starts the REAL command as a subprocess (`python -m spoor.cli <args>`) — the
# GUI only builds the argument list and supervises the process, so every safety
# gate applies exactly as it does from a terminal: the destructive-action gate,
# the sandbox host check behind --sandbox, redaction, and session pre-checks.
# The GUI never re-implements a command's own validation; a command's error
# shows up in its job's log.
#
# These scenarios drive the GUI with a FAKE runner standing in for the
# subprocess, so argument building, live logs, Stop, and output links are
# checked without launching Spoor. The one @browser scenario runs the real
# command end to end against a local static fixture.
#
# A supervised `spoor explore` is told two things through its environment
# (gui-2 mechanics decision, §2i): SPOOR_PROGRESS=lines (print plain progress
# lines a log can show) and SPOOR_STOP_FILE (stop after the current action once
# this file appears — the same graceful stop Ctrl-C gives, but portable).
#
# Nothing here is site-specific (§0).

Feature: Running Spoor's commands from the local GUI
  As an operator who would rather not use the command line
  I want to fill in a form, start a run, watch it, and stop it
  So that I can explore and extract from sites without remembering flags,
  while every safety rule still applies exactly as on the command line

  Background:
    Given the GUI app is running jobs with a fake runner

  # --- Building the command ----------------------------------------------------

  Scenario: Submitting the explore form runs the matching spoor explore command
    When I submit the explore form with:
      | field      | value                  |
      | url        | http://127.0.0.1:9/app |
      | max_states | 5                      |
      | wiki       | on                     |
      | wiki_dir   | out/wiki               |
    Then the fake runner was started with "explore http://127.0.0.1:9/app --max-states 5 --wiki <abs:out/wiki>"
    And I am taken to that job's page, which shows the command

  Scenario: An unticked output is not passed, even if its folder is filled in
    When I submit the explore form with:
      | field    | value                  |
      | url      | http://127.0.0.1:9/app |
      | wiki_dir | out/wiki               |
    Then the fake runner was started with "explore http://127.0.0.1:9/app"

  Scenario: The sandbox checkbox passes --sandbox and nothing more
    When I submit the explore form with:
      | field   | value                  |
      | url     | http://127.0.0.1:9/app |
      | sandbox | on                     |
    Then the fake runner was started with "explore http://127.0.0.1:9/app --sandbox"

  Scenario: Element patterns, one per line, become repeated options
    When I submit the explore form with:
      | field            | value                  |
      | url              | http://127.0.0.1:9/app |
      | include_elements | Add to cart*\nDetails  |
      | exclude_elements | *Logout*               |
    Then the fake runner was started with "explore http://127.0.0.1:9/app --include-element 'Add to cart*' --include-element Details --exclude-element '*Logout*'"

  Scenario: Every explore option the command has can be set from the form
    When I submit the explore form with:
      | field                 | value                  |
      | url                   | http://127.0.0.1:9/app |
      | sandbox               | on                     |
      | max_states            | 5                      |
      | max_requests          | 40                     |
      | max_seconds           | 90                     |
      | max_depth             | 2                      |
      | resume_from           | id:ab12                |
      | session               | customer               |
      | wiki                  | on                     |
      | wiki_dir              | out/wiki               |
      | screenshots           | on                     |
      | gen_tests             | on                     |
      | gen_tests_dir         | out/tests              |
      | assert_no_new_signals | on                     |
      | scaffold              | on                     |
      | scaffold_dir          | out/scaffold           |
      | include_elements      | Buy*                   |
      | exclude_elements      | Logout                 |
    Then the fake runner was started with "explore http://127.0.0.1:9/app --sandbox --max-states 5 --max-requests 40 --max-seconds 90 --max-depth 2 --resume-from id:ab12 --session customer --wiki <abs:out/wiki> --screenshots --gen-tests <abs:out/tests> --assert-no-new-signals --scaffold <abs:out/scaffold> --include-element 'Buy*' --exclude-element Logout"

  Scenario: Submitting the extraction form runs the matching spoor run command
    When I submit the run form with:
      | field              | value                |
      | config             | configs/shop.yaml    |
      | output             | out/products.csv     |
      | format             | csv                  |
      | healing_report     | on                   |
      | healing_report_path | out/healing.md      |
    Then the fake runner was started with "run <abs:configs/shop.yaml> --output <abs:out/products.csv> --format csv --healing-report <abs:out/healing.md>"

  Scenario: Submitting the apply-scaffold form runs the matching command
    When I submit the apply-scaffold form with:
      | field    | value                         |
      | url      | http://127.0.0.1:9/app        |
      | scaffold | out/scaffold/interactive.yaml |
      | sandbox  | on                            |
      | session  | customer                      |
      | wiki     | on                            |
      | wiki_dir | out/wiki                      |
    Then the fake runner was started with "apply-scaffold http://127.0.0.1:9/app <abs:out/scaffold/interactive.yaml> --sandbox --session customer --wiki <abs:out/wiki>"

  Scenario: A missing required field re-shows the form with a message, launching nothing
    When I submit the explore form with:
      | field      | value |
      | max_states | 5     |
    Then the response status is 400
    And the page says "Enter the address of the site to explore."
    And the fake runner was never started

  Scenario: A number field that isn't a number re-shows the form with a message
    When I submit the explore form with:
      | field      | value                  |
      | url        | http://127.0.0.1:9/app |
      | max_states | lots                   |
    Then the response status is 400
    And the page says "Max screens must be a whole number."
    And the fake runner was never started

  Scenario: An address that looks like an option is refused, not passed as one
    When I submit the explore form with:
      | field | value     |
      | url   | --sandbox |
    Then the response status is 400
    And the page says "The address can&#39;t start with &#39;-&#39;."
    And the fake runner was never started

  Scenario: The command preview shows exactly what would run, without running it
    When I preview the explore form with:
      | field   | value                  |
      | url     | http://127.0.0.1:9/app |
      | sandbox | on                     |
    Then the preview reads "spoor explore http://127.0.0.1:9/app --sandbox"
    And the fake runner was never started

  Scenario: An explore job is told to print progress lines and where its stop file is
    When I submit the explore form with:
      | field | value                  |
      | url   | http://127.0.0.1:9/app |
    Then the fake runner was started with SPOOR_PROGRESS set to "lines"
    And the fake runner was started with a SPOOR_STOP_FILE that does not exist yet

  # --- Watching a job ------------------------------------------------------------

  Scenario: A job's log streams to the page as it runs
    Given the fake command will print "Explored http://127.0.0.1:9/app" and exit 0
    When I start an explore job for "http://127.0.0.1:9/app"
    And I read the job's live log until it ends
    Then the live log contains "Explored http://127.0.0.1:9/app"
    And the live log ends with status "succeeded"

  Scenario: A secret printed by a job is redacted in its log
    Given the fake command will print "auth header Bearer abcdef1234567890x" and exit 0
    When I start an explore job for "http://127.0.0.1:9/app"
    And I read the job's live log until it ends
    Then the live log contains "Bearer [REDACTED]"
    And the live log never contains "abcdef1234567890x"

  Scenario: A command that fails shows as failed, with its exit code and error
    Given the fake command will print "Error: --screenshots needs --wiki" and exit 2
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    Then the job page shows status "failed" with exit code 2
    And the job page shows "--screenshots needs --wiki"

  Scenario: The jobs page lists every job started in this GUI session
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    Then the jobs page lists that job with its command

  # --- Where the output landed ----------------------------------------------------

  Scenario: A finished job lists where each requested output landed
    Given the fake command will write a wiki and exit 0
    When I start an explore job for "http://127.0.0.1:9/app" with a wiki folder
    And the job finishes
    Then the job page shows the wiki folder's absolute path
    And the job page links to the wiki's index page
    And the job page links to the map for "http://127.0.0.1:9/app"

  Scenario: A job's wiki is served from its own folder only
    Given the fake command will write a wiki and exit 0
    When I start an explore job for "http://127.0.0.1:9/app" with a wiki folder
    And the job finishes
    Then the job's wiki index page is served
    And a request for "../secret.txt" under the job's wiki is refused

  Scenario: Open folder opens only the job's own output folder
    Given the fake command will write a wiki and exit 0
    When I start an explore job for "http://127.0.0.1:9/app" with a wiki folder
    And the job finishes
    And I ask to open the job's "wiki" folder
    Then the folder opener was asked to open the job's wiki folder
    And asking to open the job's "elsewhere" folder is refused

  # --- Stopping a job -------------------------------------------------------------

  Scenario: Stopping an exploration asks it to finish gracefully
    Given the fake command keeps running until its stop file appears, then exits 0
    When I start an explore job for "http://127.0.0.1:9/app"
    And I press Stop on the job
    And the job finishes
    Then the job's stop file was created
    And the job page shows status "stopped"
    And the job page says what was mapped so far was saved

  Scenario: Force stop ends an exploration immediately
    Given the fake command keeps running until it is killed
    When I start an explore job for "http://127.0.0.1:9/app"
    And I press Force stop on the job
    And the job finishes
    Then the fake process was killed
    And the job page shows status "stopped"

  Scenario: Stopping an extraction run ends it immediately
    Given the fake command keeps running until it is killed
    When I start a run job for "configs/shop.yaml"
    And I press Stop on the job
    And the job finishes
    Then the fake process was killed

  Scenario: Closing the GUI stops jobs that are still running
    Given the fake command keeps running until it is killed
    When I start an explore job for "http://127.0.0.1:9/app"
    And the GUI shuts down
    Then the fake process was killed

  # --- Safety ---------------------------------------------------------------------

  Scenario: A job form submitted from another site is refused and launches nothing
    When another site submits the explore form for "http://127.0.0.1:9/app"
    Then the response status is 403
    And the fake runner was never started

  Scenario: A map page offers to explore the URL again with the form pre-filled
    Given a map store that has mapped "https://shop.example/products"
    When I open the map page for "https://shop.example/products" with the access token
    Then the page links to the explore form pre-filled with "https://shop.example/products"

  # --- End to end in a real browser -----------------------------------------------

  @browser
  Scenario: Exploring a local site from the GUI writes a wiki I can open
    Given the GUI is running on loopback with the real command runner
    And a local static site is being served
    When a real browser fills in the explore form for the local site with a wiki
    And starts the job and waits for it to finish
    Then the browser shows the job succeeded
    And the browser shows where the wiki was written
    And the wiki folder contains an index page
