# Bounded concurrent fetching, in-house (ROADMAP.md §2d, #174).
#
# Split out of #148 after D1 (#146) decided against adopting Crawlee. The
# tier-1 frontier (#169) made concurrency meaningful: `PolitenessPolicy.
# max_concurrent_per_domain` bounds how many fetches to the same domain may be
# in flight at once, over a stdlib `concurrent.futures.ThreadPoolExecutor` —
# not asyncio, since Spoor's core (httpx.Client, Playwright's sync API) is
# synchronous throughout, and introducing an asyncio seam for this one feature
# was the specific cost D1 weighed against adopting Crawlee's `AutoscaledPool`.
#
# Scope is the tier-1 fetch path only. The browser tier stays single-threaded
# — Playwright's sync API isn't safe to drive from more than one thread — so
# `max_concurrent_per_domain` has no effect there beyond the default of 1 it
# already behaves as.
#
# The default (`max_concurrent_per_domain: 1`, i.e. omitting it) reproduces
# the fully-sequential behavior every run had before this existed — a
# regression guard, not just a new-feature test.

Feature: Bounded concurrent fetching, per domain
  As someone crawling a site with many pages
  I want fetches to the same domain to overlap, up to a cap, while still being politely spaced
  So that a large crawl finishes faster without hammering any one origin

  Background:
    Given a config with a "title" field

  Scenario: The default cap of 1 fetches one page at a time
    Given a slow fixture server that records how many requests are in flight at once
    And a config crawling 4 pages on that server with no concurrency cap set
    When I run the crawl
    Then at most 1 request to that server was ever in flight at once

  Scenario: A higher cap allows overlapping fetches to the same domain, bounded by the cap
    Given a slow fixture server that records how many requests are in flight at once
    And a config crawling 4 pages on that server with a concurrency cap of 2
    When I run the crawl
    Then at most 2 requests to that server were ever in flight at once
    And more than 1 request to that server was in flight at some point

  Scenario: Concurrent fetches to the same domain still respect the crawl-delay
    Given a slow fixture server that records when each request started
    And a config crawling 4 pages on that server with a concurrency cap of 2 and a crawl-delay of 0.3 seconds
    When I run the crawl
    Then consecutive request start times on that server are spaced at least 0.3 seconds apart

  @browser
  Scenario: The browser tier is unaffected by a concurrency cap
    Given a slow fixture server that records how many requests are in flight at once
    And a config crawling 4 pages on that server with a concurrency cap of 4
    When I run the crawl in the browser tier
    Then at most 1 request to that server was ever in flight at once
