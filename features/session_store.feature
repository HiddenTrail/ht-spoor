# Named, stored browser sessions, scoped per site — §2h Phase B, closes #215.
#
# Today's --session <file> is purely a CLI-supplied, read-only input: a
# storage-state file the user captured once, never persisted by Spoor, never
# named, no concept of "several for the same site". This slice adds a SECOND
# way to supply the same thing: store a captured session once under a label,
# scoped to a site, and reuse it by name across runs instead of re-pointing at
# a file path every time. The file-path behavior is completely unchanged — a
# real file always wins over a same-named stored label.
#
# Security posture (§2h, called out explicitly in #215): storing session data
# makes Spoor a persistent holder of live login cookies for the first time.
# `SessionStore.list()` therefore returns metadata only (label, site,
# timestamps) and NEVER storage-state contents — there is no code path that
# could leak a cookie value through a listing, because the shape returned
# doesn't carry one. There is deliberately no serving-layer (MCP/REST)
# surface for stored sessions in this slice, so none of this touches the §2f
# read-only non-negotiable.
#
# Nothing here is site-specific (§0): the same storage/lookup/resolution
# applies to every site, keyed only by the domain a URL already carries.

Feature: Named, stored browser sessions, scoped per site
  As a user running Spoor repeatedly against the same authenticated site
  I want to store a captured session once, under a name, and reuse it by name
  So that I control multiple logged-in sessions for a site without re-pointing
  at a file path every run, and nothing stored ever exposes a cookie value
  through a listing

  Background:
    Given a storage-state file captured for "shop.example"

  Scenario: Storing a session makes it listed under its site
    When I store that session for "shop.example" labeled "customer"
    Then listing sessions for "shop.example" shows "customer"

  Scenario: A listing never includes the stored storage-state contents
    When I store that session for "shop.example" labeled "customer"
    Then listing sessions for "shop.example" shows only metadata, never values

  Scenario: Sessions are scoped per site, not shared across sites
    When I store that session for "shop.example" labeled "customer"
    Then listing sessions for "other.example" shows no sessions

  Scenario: Listing with no site given shows every stored session
    Given a storage-state file captured for "other.example"
    When I store that session for "shop.example" labeled "customer"
    And I store that session for "other.example" labeled "customer"
    Then listing every stored session shows "shop.example" and "other.example"

  Scenario: Re-adding a label replaces what it points to
    When I store that session for "shop.example" labeled "customer"
    And I store a different session for "shop.example" labeled "customer"
    Then resolving "customer" for "shop.example" loads the newer session

  Scenario: Removing a stored session takes it out of the listing
    Given I store that session for "shop.example" labeled "customer"
    When I remove the session "customer" for "shop.example"
    Then listing sessions for "shop.example" shows no sessions

  Scenario: Removing a session that was never stored reports nothing removed
    When I remove the session "ghost" for "shop.example"
    Then removing reports nothing was removed

  Scenario: --session resolves a stored label when no file exists at that path
    Given I store that session for "shop.example" labeled "customer"
    When I load the session "customer" for "shop.example"
    Then it resolves to the session stored under "customer"

  Scenario: A real file always wins over a same-named stored label
    Given a storage-state file captured for "shop.example" at path "customer"
    And I store that session for "shop.example" labeled "customer"
    When I load the session "customer" for "shop.example"
    Then it resolves to the file at path "customer", not the stored session

  Scenario: A label that is neither a file nor a stored session fails loudly
    When I try to load the session "nope" for "shop.example"
    Then it fails because no session file or stored session named "nope" exists
