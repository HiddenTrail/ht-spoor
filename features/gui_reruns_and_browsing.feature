# Local GUI: re-running jobs, dates on jobs, and a folder browser — ROADMAP.md §2i.
#
# Every run job gets a "…" menu (Jobs list and job page) with the follow-ups
# that make sense for it: Rerun (at once, same settings), Rerun with changes
# (the form, filled in), Apply scaffold (for an exploration that wrote one),
# Edit config (for an extraction whose config is in the working folder) and
# View map. A rerun never overwrites the earlier run's output: a folder under
# spoor-output/<date and time>/ moves to a fresh date-and-time folder, while a
# folder the operator chose elsewhere is reused.
#
# Folder and file fields get a "Browse…" button opening an in-page folder
# browser. It lists names only, never file contents, and never writes.
#
# The job scenarios use the fake runner shared with gui-2; nothing here is
# site-specific (§0).

Feature: Re-running jobs and picking folders in the local GUI
  As an operator who would rather not use the command line
  I want one click to run a job again, or to start from it with changes,
  and to pick folders instead of typing paths
  So that repeat work is quick and output never lands somewhere I didn't mean

  Background:
    Given the GUI app is running jobs with a fake runner

  # --- Dates and times -----------------------------------------------------------

  Scenario: The jobs list shows each job's start date and time and its duration
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    Then the jobs list shows that job's start date and time
    And the jobs list shows that job's duration

  Scenario: A job page shows when the job started and finished
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    Then the job page shows when it started and when it finished

  # --- The "…" menu ----------------------------------------------------------------

  Scenario: An exploration's menu offers rerun, rerun with changes and its map
    Given the fake command will write a scaffold and a wiki, record a map, and exit 0
    When I start an explore job with a wiki and a scaffold
    And the job finishes
    Then the job's menu offers "Rerun", "Rerun with changes", "Apply scaffold" and "View map"
    And the jobs list offers the same menu for that job

  Scenario: An exploration without a scaffold doesn't offer to apply one
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    Then the job's menu does not offer "Apply scaffold"

  Scenario: An extraction whose config is in the working folder offers to edit it
    Given the working folder has a config "configs/shop.yaml"
    When I start a run job for "configs/shop.yaml"
    And the job finishes
    Then the job's menu offers "Rerun", "Rerun with changes" and "Edit config"
    And "Edit config" opens the editor for "configs/shop.yaml"

  # --- Rerun --------------------------------------------------------------------------

  Scenario: Rerun starts the same command again, with fresh default folders
    When I start an explore job with a wiki and a scaffold
    And the job finishes
    And I choose "Rerun" for the job
    Then a second job was started with the same settings
    And its default output folders are in a new date-and-time folder
    And I am taken to the new job's page

  Scenario: Rerun reuses an output folder I chose myself
    When I start an explore job for "http://127.0.0.1:9/app" with the wiki in "my-wikis/shop"
    And the job finishes
    And I choose "Rerun" for the job
    Then the second job writes its wiki to "my-wikis/shop" again

  Scenario: Another site can't rerun a job
    When I start an explore job for "http://127.0.0.1:9/app"
    And the job finishes
    And another site asks to rerun the job
    Then the response status is 403
    And only one job was ever started

  Scenario: Rerunning a job that doesn't exist is not found
    When I ask to rerun the job "nope"
    Then the response status is 404

  # --- Rerun with changes, and follow-ups -------------------------------------------

  Scenario: Rerun with changes opens the form with every original value filled in
    When I start an explore job with every option set
    And the job finishes
    And I choose "Rerun with changes" for the job
    Then the explore form is filled in with every original value
    And its default output folders are in a new date-and-time folder

  Scenario: Rerun with changes for an extraction fills in its form
    Given the working folder has a config "configs/shop.yaml"
    When I start a run job for "configs/shop.yaml" as "csv" into "out/shop.csv"
    And the job finishes
    And I choose "Rerun with changes" for the job
    Then the extract form has the config "configs/shop.yaml", the output "out/shop.csv" and the format "csv"

  Scenario: Apply scaffold fills in the apply-scaffold form from the exploration
    Given the fake command will write a scaffold and a wiki, record a map, and exit 0
    When I start an explore job with a wiki and a scaffold
    And the job finishes
    And I choose "Apply scaffold" for the job
    Then the apply-scaffold form has the exploration's address, its scaffold file and its wiki
    And the apply-scaffold form keeps the exploration's sandbox and login choices

  # --- The folder browser -----------------------------------------------------------

  Scenario: Folder and file fields have a Browse button
    When I open the explore form
    Then the wiki, tests and scaffold folder fields each have a Browse button for a folder
    When I open the extract form
    Then the config field has a Browse button for a YAML file
    And the records and healing report fields have a Browse button that keeps the file name

  Scenario: The folder browser lists a folder's subfolders, not its files
    Given the working folder has the folders "alpha" and "beta" and the file "notes.yaml"
    When I browse the working folder for a folder
    Then the listing shows the folders "alpha" and "beta"
    And the listing does not show "notes.yaml"
    And the listing names the working folder's parent

  Scenario: Browsing for a file lists matching files beside the folders
    Given the working folder has the folders "alpha" and "beta" and the file "notes.yaml"
    And the working folder has the file "readme.txt"
    When I browse the working folder for a YAML file
    Then the listing shows the file "notes.yaml"
    And the listing does not show "readme.txt"

  Scenario: Hidden folders are not listed
    Given the working folder has the folders "alpha" and ".secret"
    When I browse the working folder for a folder
    Then the listing does not show ".secret"

  Scenario: The browser starts at the working folder, or the nearest folder that exists
    When I browse without a starting folder
    Then the listing is for the working folder
    When I browse starting from a folder that doesn't exist inside the working folder
    Then the listing is for the working folder

  Scenario: The folder browser shows names only and never writes
    Given the working folder has the folders "alpha" and "beta" and the file "notes.yaml"
    When I browse the working folder for a YAML file
    Then the listing contains no file contents
    And browsing changed nothing in the working folder

  @browser
  Scenario: Picking the wiki folder with the browser in a real browser
    Given the GUI is running on loopback with the real command runner
    And the working folder has the folders "alpha" and "beta" and the file "notes.yaml"
    When a real browser opens the explore form and browses for the wiki folder
    And opens "alpha" and chooses it with the new folder name "shop-wiki"
    Then the wiki folder field holds the "alpha/shop-wiki" folder inside the working folder
