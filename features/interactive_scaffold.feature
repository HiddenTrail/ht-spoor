# Interactive-round config scaffold — ROADMAP.md §2e, issue #131.
#
# The first, scoped piece of the planned second (interactive) exploration round: after
# a normal read-only crawl, write a human-editable YAML file listing what that future
# round would need — discovered fields with a best-guess generator, discovered login
# points, and discovered actions the safety gate flagged destructive. Consuming a
# filled-in scaffold to actually run round two is a separate, later piece; this slice
# only generates the file, built pure like the wiki renderer and the testgen generator
# (`build_scaffold`, no disk/browser) with a thin disk writer (`render_scaffold`).
#
# Login points are informational only, never a fillable credential (§2h,
# bring-your-own-session, decided): Spoor does not automate logins, so a discovered
# password field becomes a flag pointing at the existing session: mechanism, not a
# username/password pair. destructive_actions entries are informational too — nothing
# here grants permission; the sandbox-only rule holds regardless of what a filled-in
# scaffold says. Nothing here is site-specific (§0): one generator for every target.

Feature: Scaffold an interactive-round config from an exploration graph
  As a team that has mapped a site with Spoor
  I want a template listing the fields, logins, and destructive actions it found
  So that I know exactly what a future interactive round would need me to fill in

  Background:
    Given a discovered state "home":
      | role    | name           | input_type |
      | textbox | Email          | email      |
      | textbox | Password       | password   |
      | textbox | Promo code     |            |
      | button  | Delete account |            |

  Scenario: A recognized field gets an inferred kind, a note, and a blank value
    When I scaffold a config for "https://shop.example"
    Then the scaffold has a field named "Email" with kind "email"
    And that field has a blank value to fill in

  Scenario: An unrecognized field is flagged unknown, never a guessed default
    When I scaffold a config for "https://shop.example"
    Then the scaffold has a field named "Promo code" with kind "unknown"

  Scenario: A password field becomes a login point, never a generatable field
    When I scaffold a config for "https://shop.example"
    Then the scaffold has a login point named "Password"
    And no field in the scaffold is named "Password"
    And that login point has no credential keys, only a blank session

  Scenario: A destructive skip appears as informational, not as permission
    Given "Delete account" on "home" was skipped as destructive
    When I scaffold a config for "https://shop.example"
    Then the scaffold has a destructive action named "Delete account"
    And that destructive action is not allowed by default

  Scenario: A destructive-looking name skipped for an unrelated reason is not listed
    # "Delete account" is skipped here too, but for being covered by an overlay, not
    # for being destructive outside a sandbox — the scaffold must go by what actually
    # happened, never re-guess from the label alone.
    Given "Delete account" on "home" was skipped for an unrelated reason
    When I scaffold a config for "https://shop.example"
    Then no destructive action in the scaffold is named "Delete account"

  Scenario: Field names are redacted before they reach the scaffold
    Given a discovered state "vault":
      | role    | name                            | input_type |
      | textbox | Bearer sk-supersecrettoken12345 | text       |
    When I scaffold a config for "https://shop.example"
    Then no generated scaffold contains the raw secret "sk-supersecrettoken12345"

  Scenario: A graph with no states scaffolds nothing
    Given an empty discovered graph
    When I scaffold a config for "https://shop.example"
    Then no scaffold is written

  @browser
  Scenario: A live crawl's password field becomes a login point in the written file
    Given a live crawl of "explore_login.html" was mapped at depth 1
    When I write that crawl's scaffold to a directory
    Then the written scaffold file has a login point
