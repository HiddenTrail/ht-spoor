# Local GUI, slice gui-3: saved logins and config files — ROADMAP.md §2i.
#
# Saved logins (stored browser sessions): the GUI lists them from the session
# store, which can only return metadata (label, site, dates), never a cookie.
# Adding and removing one runs the real `spoor session add` / `spoor session
# remove` commands; an uploaded login file is written to a private temporary
# file for the command and deleted as soon as the command ends.
#
# Config files: the GUI lists, opens, checks and saves extraction configs, but
# only .yaml/.yml files inside its working folder. Checking uses the same
# loader `spoor run` uses, so "valid" in the GUI means valid for the command.
# The editor shows a config exactly as it is on disk (it's the operator's own
# input; blanking a token would write [REDACTED] back into the file).
#
# The scenarios use the fake runner from gui-2 for the session commands; the
# @browser scenarios run the real CLI and a real browser.
#
# Nothing here is site-specific (§0).

Feature: Managing saved logins and config files from the local GUI
  As an operator who would rather not use the command line
  I want to add and remove saved logins and edit config files in the browser
  So that I can prepare authenticated and configured runs without a terminal,
  without a saved login's contents ever appearing on screen

  Background:
    Given the GUI app is running jobs with a fake runner

  # --- Saved logins ---------------------------------------------------------------

  Scenario: The logins page lists stored logins with their dates, never their contents
    Given a login "customer" is stored for "shop.example" with the secret marker "COOKIE-VALUE-123"
    When I open the logins page
    Then the page lists the login "customer" for "shop.example"
    And the page never shows "COOKIE-VALUE-123"

  Scenario: With nothing stored, the logins page explains how to add one
    When I open the logins page
    Then the page says "No saved logins yet."

  Scenario: Adding a login runs spoor session add with a temporary copy of the upload
    Given the fake command will report the upload it was given and exit 0
    When I add a login "customer" for "https://shop.example/account" from an uploaded file
    Then the fake runner was started with "session add --label customer -- <upload> https://shop.example/account"
    And the command saw the uploaded file's contents
    And the temporary copy of the upload is gone
    And the page says "Stored session"

  Scenario: A login the command rejects shows the command's error and leaves nothing behind
    Given the fake command will print "Error: not a storage-state file" and exit 2
    When I add a login "customer" for "shop.example" from an uploaded file
    Then the page says "not a storage-state file"
    And the temporary copy of the upload is gone

  Scenario: Adding a login without a name launches nothing
    When I add a login "" for "shop.example" from an uploaded file
    Then the response status is 400
    And the page says "Give the login a name."
    And the fake runner was never started

  Scenario: Adding a login without a file launches nothing
    When I add a login "customer" for "shop.example" without a file
    Then the response status is 400
    And the page says "Choose the login file to upload."
    And the fake runner was never started

  Scenario: A login command that hangs is stopped and its upload still removed
    Given the fake command keeps running until it is killed
    And the GUI waits at most 0.2 seconds for a login command
    When I add a login "customer" for "shop.example" from an uploaded file
    Then the fake process was killed
    And the temporary copy of the upload is gone
    And the page says "took too long"

  Scenario: Removing a login runs spoor session remove
    Given a login "customer" is stored for "shop.example" with the secret marker "x"
    When I remove the login "customer" for "shop.example"
    Then the fake runner was started with "session remove -- shop.example customer"

  Scenario: A login whose name starts with "-" is passed as a name, not an option
    Given the fake command will report the upload it was given and exit 0
    When I add a login "-admin" for "shop.example" from an uploaded file
    Then the fake runner was started with "session add --label -admin -- <upload> shop.example"

  Scenario: The explore form suggests stored login names
    Given a login "customer" is stored for "shop.example" with the secret marker "COOKIE-VALUE-123"
    When I open the explore form
    Then the page offers the login name "customer"
    And the page never shows "COOKIE-VALUE-123"

  Scenario: Another site can't add a login
    When another site posts a login "customer" for "shop.example"
    Then the response status is 403
    And the fake runner was never started

  # --- Config files ---------------------------------------------------------------

  Scenario: The configs page lists YAML configs in the working folder and whether each is valid
    Given the working folder has a valid config "configs/shop.yaml"
    And the working folder has an invalid config "configs/broken.yml"
    And the working folder has a YAML file "spoor-output/run/interactive.yaml"
    And the working folder has a YAML file ".spoor-cache/x.yaml"
    When I open the configs page
    Then the page lists the config "configs/shop.yaml" as valid
    And the page lists the config "configs/broken.yml" as not valid
    And the page does not list "spoor-output/run/interactive.yaml"
    And the page does not list ".spoor-cache/x.yaml"

  Scenario: Opening a config shows it exactly as it is on disk
    Given the working folder has a valid config "configs/shop.yaml" with a header "Authorization: Bearer abcdef1234567890x"
    When I open the config "configs/shop.yaml"
    Then the editor contains "Bearer abcdef1234567890x"

  Scenario: Checking a config lists each problem with where it is, without saving
    Given the working folder has a valid config "configs/shop.yaml"
    When I check the config "configs/shop.yaml" with the text:
      """
      target: https://shop.example/products
      fields:
        price: { selector: ".price", type: money }
      """
    Then the page says "fields.price.type"
    And the config file "configs/shop.yaml" is unchanged

  Scenario: Checking text that isn't YAML says where it went wrong
    Given the working folder has a valid config "configs/shop.yaml"
    When I check the config "configs/shop.yaml" with the text:
      """
      target: [unclosed
      """
    Then the page says "line"
    And the config file "configs/shop.yaml" is unchanged

  Scenario: Saving a valid config writes it and offers to run it
    Given the working folder has a valid config "configs/shop.yaml"
    When I save the config "configs/shop.yaml" with the text:
      """
      target: https://shop.example/sale
      fields:
        title: { selector: "h2" }
      """
    Then the config file "configs/shop.yaml" contains "https://shop.example/sale"
    And the page says "Saved. The config is valid."
    And the page links to the extract form pre-filled with "configs/shop.yaml"

  Scenario: Saving a config that isn't valid yet still writes it, and says so
    Given the working folder has a valid config "configs/shop.yaml"
    When I save the config "configs/shop.yaml" with the text:
      """
      fields: {}
      """
    Then the config file "configs/shop.yaml" contains "fields: {}"
    And the page says "Saved, but the config is not valid yet"
    And the page says "target"

  Scenario: A new config starts from the example and never overwrites a file
    When I create the config "configs/new.yaml"
    Then the config file "configs/new.yaml" contains "target:"
    And I am taken to the editor for "configs/new.yaml"
    When I create the config "configs/new.yaml"
    Then the response status is 400
    And the page says "already exists"

  Scenario Outline: Only YAML files inside the working folder can be opened
    Given a file exists at "<path>" relative to the working folder
    When I open the config "<path>"
    Then the response status is 404

    Examples:
      | path              |
      | ../outside.yaml   |
      | configs/notes.txt |
      | .spoor-cache/x.yaml |

  Scenario: Only YAML files inside the working folder can be saved
    When I save the config "../outside.yaml" with the text:
      """
      target: https://shop.example/
      """
    Then the response status is 404
    And no file "../outside.yaml" was written

  Scenario: The extract form can be pre-filled with a config
    When I open the extract form for the config "configs/shop.yaml"
    Then the config field is pre-filled with "configs/shop.yaml"

  # --- End to end in a real browser ------------------------------------------------

  @browser
  Scenario: Saving a login from the GUI stores it through the real command
    Given the GUI is running on loopback with the real command runner
    And a captured login file for "shop.example" marked "REAL-COOKIE-456"
    When a real browser adds that login as "customer" for "shop.example"
    Then the browser lists the login "customer" for "shop.example"
    And the browser page never shows "REAL-COOKIE-456"
    And the session store has the login "customer" for "shop.example"

  @browser
  Scenario: Fixing a config in the editor in a real browser
    Given the GUI is running on loopback with the real command runner
    And the working folder has an invalid config "configs/broken.yml"
    When a real browser opens "configs/broken.yml" in the editor
    And replaces its text with a valid config and saves
    Then the browser says "Saved. The config is valid."
