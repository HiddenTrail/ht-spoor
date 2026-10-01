# Request/response hooks (ROADMAP.md §2d, part of #150).
#
# docs/COMPETITIVE_PLAN.md names Crawlee/Scrapy-style request/response
# middleware as a gap: a way for an operator to extend a run — add a header,
# transform a fetched page before extraction — without writing site-specific
# code into `spoor/core/` (§0). Hooks are plain Python callables supplied when
# Spoor is used as a library (`extract.run_report(cfg, hooks=...)`), the same
# injection seam `healer`/`sleep`/`client` already use — not a config field,
# since a hook is code, not declarative per-target config.
#
# Two safety properties this file proves, not just documents: a hook can only
# *add* headers, never change which URL is fetched, so it can never be used to
# route a request around the politeness gate's robots.txt check (the gate
# decides and blocks a URL before any hook ever sees it); and a response hook
# only ever sees pre-extraction HTML text, upstream of the output pipeline's
# schema validation and §2h redaction — it has no path to shared output that
# skips either.
#
# Crawljax-style exploration hooks (on-state/on-transition) are the other half
# of #150 and are deliberately out of scope here — a separate design pass,
# tracked as its own issue.

Feature: Operator-supplied request/response hooks extend a run
  As someone running Spoor as a library
  I want to add headers to outgoing requests and transform fetched pages
  So that I can extend a run without writing site-specific code into Spoor itself

  Scenario: An on_request hook adds a header to every fetch
    Given a fixture server that reports the headers it received
    And an on_request hook that adds an "X-Api-Key" header
    When I run a static config with that hook
    Then the server received the "X-Api-Key" header with that value

  Scenario: An on_request hook returning nothing changes no headers
    Given a fixture server that reports the headers it received
    And an on_request hook that returns nothing
    When I run a static config with that hook
    Then the server received no "X-Api-Key" header

  Scenario: An on_response hook transforms the page before extraction
    Given a fixture server serving a page with a wrapped title
    And an on_response hook that unwraps the title
    When I run a static config with that hook
    Then the extracted title is the unwrapped value

  Scenario: An on_response hook returning nothing leaves the page unchanged
    Given a fixture server serving a page with a wrapped title
    And an on_response hook that returns nothing
    When I run a static config with that hook
    Then the extracted title is the wrapped value

  Scenario: A robots-blocked URL is never offered to either hook
    Given a fixture server whose robots.txt disallows the target
    And an on_request hook that records every URL it is called with
    And an on_response hook that records every URL it is called with
    When I run a static config with both hooks
    Then neither hook was called
    And the URL is reported blocked

  Scenario: Omitting hooks entirely reproduces today's behavior unchanged
    Given a fixture server that reports the headers it received
    When I run a static config with no hooks
    Then the server received no "X-Api-Key" header

  @browser
  Scenario: Both hooks apply identically on the browser tier
    Given a fixture server that reports the headers it received and serves a page with a wrapped title
    And an on_request hook that adds an "X-Api-Key" header
    And an on_response hook that unwraps the title
    When I run a browser config with both hooks
    Then the server received the "X-Api-Key" header with that value
    And the extracted title is the unwrapped value
