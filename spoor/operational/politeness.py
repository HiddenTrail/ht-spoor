"""Runtime politeness gate: robots.txt + crawl-delay + concurrency (ROADMAP.md §2d, §6).

The declarative knobs live in `spoor.core.config.PolitenessPolicy`; this module
is the runtime that enforces them against a live crawl. §6 commits Spoor to
respecting `robots.txt` and rate-limiting by default, with overriding it an
explicit opt-out. Per §0 there is nothing site-specific here — robots.txt is
fetched and parsed the same generic way for every target.

Scope: allow/deny checks, per-domain crawl-delay spacing, and a per-domain
concurrency bound (ROADMAP.md §2d, #174) over the tier-1 fetch path. This
class is called from multiple threads once `max_concurrent_per_domain > 1`
(`Tier1Resolver` dispatches fetches through a thread pool), so every method
here is safe to call concurrently — see `acquire`/`release`.
"""

from __future__ import annotations

import threading
import time
import xml.etree.ElementTree as ET
from collections import deque
from collections.abc import Callable
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser

import httpx

from spoor.core.config import PolitenessPolicy

# The product token we present to robots.txt for user-agent matching.
USER_AGENT = "spoor"

# Bounds on sitemap-seed discovery (ROADMAP.md §2d) — a sitemap is a remote,
# origin-declared resource, so these guard the same way _MAX_PAGES guards the
# crawl itself: a cyclic or unbounded sitemap index must not hang a run or
# flood it with more seeds than any real site needs.
_MAX_SITEMAPS_FETCHED = 50
_MAX_SITEMAP_URLS = 50_000


def _local_tag(tag: str) -> str:
    """An XML tag's name without its namespace prefix (`{ns}urlset` -> `urlset`).

    Real-world sitemaps declare the sitemaps.org namespace; some don't. Both
    are read the same way rather than requiring one specific namespace.
    """
    return tag.rsplit("}", 1)[-1]


def _fetch_sitemap(client: httpx.Client, url: str) -> tuple[list[str], list[str]]:
    """One sitemap's page URLs and, if it's an index, its child sitemap URLs.

    A `<urlset>` yields its `<url><loc>` entries as pages; a `<sitemapindex>`
    yields its `<sitemap><loc>` entries as more sitemaps to fetch, never as
    pages themselves. A fetch failure, a non-200, or XML that doesn't parse
    (or whose root is neither) yields nothing from that source — the same
    tolerant degrade `Politeness._parser` already takes for a missing or
    unreadable robots.txt, never a crashed run.
    """
    try:
        response = client.get(url)
    except httpx.HTTPError:
        return [], []
    if response.status_code != 200:
        return [], []
    try:
        root = ET.fromstring(response.content)
    except ET.ParseError:
        return [], []
    if _local_tag(root.tag) == "urlset":
        return [
            loc.text.strip()
            for entry in root
            if _local_tag(entry.tag) == "url"
            for loc in entry
            if _local_tag(loc.tag) == "loc" and loc.text
        ], []
    if _local_tag(root.tag) == "sitemapindex":
        return [], [
            loc.text.strip()
            for entry in root
            if _local_tag(entry.tag) == "sitemap"
            for loc in entry
            if _local_tag(loc.tag) == "loc" and loc.text
        ]
    return [], []


class Politeness:
    """Enforces a `PolitenessPolicy` across the fetches of one run.

    Fetches and caches `robots.txt` per origin (scheme + host) on first need,
    answers `can_fetch`, and gates each fetch through `acquire`/`release`
    (`before_fetch`/`after_fetch` are the same pair, under their established
    names), which together bound concurrency and space dispatches, per domain
    (`netloc` — host and port, matching `urlsplit`). An injectable `sleep` lets
    tests assert delay timing without real waiting.

    Thread-safety: a single `_registry_lock` guards creation of the per-domain
    primitives below (the robots.txt cache, each domain's semaphore and
    dispatch lock) — held only long enough to look up or create an entry,
    never across a fetch or a sleep, so unrelated domains never wait on each
    other. Robots.txt itself is fetched outside that lock (it's a network
    call) using a double-checked read, so two threads racing on the same
    uncached origin both do a harmless redundant fetch rather than blocking
    one another.
    """

    def __init__(
        self,
        policy: PolitenessPolicy,
        client: httpx.Client,
        *,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._policy = policy
        self._client = client
        self._sleep = sleep
        self._registry_lock = threading.Lock()
        self._robots: dict[tuple[str, str], RobotFileParser] = {}
        self._semaphores: dict[str, threading.Semaphore] = {}
        self._dispatch_locks: dict[str, threading.Lock] = {}
        self._dispatched: dict[str, bool] = {}

    def _domain(self, url: str) -> str:
        return urlsplit(url).netloc

    def _parser(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        origin = (parts.scheme, parts.netloc)
        with self._registry_lock:
            cached = self._robots.get(origin)
        if cached is not None:
            return cached
        parser = RobotFileParser()
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        try:
            response = self._client.get(robots_url)
        except httpx.HTTPError:
            response = None
        if response is not None and response.status_code == 200:
            parser.parse(response.text.splitlines())
        elif response is not None and response.status_code >= 500:
            # RFC 9309: a server error means the rules are unavailable, so be
            # conservative and treat the whole origin as disallowed rather than
            # crawling it as if unrestricted. A transport failure (no response)
            # falls through to allow-all — a transient client-side hiccup should
            # not silently lock out an otherwise-open site.
            parser.parse(["User-agent: *", "Disallow: /"])
        else:
            # Absent robots.txt (404) or otherwise unreadable: nothing to obey.
            parser.parse([])
        with self._registry_lock:
            # Another thread may have raced us to the same origin; keep
            # whichever landed first so every caller sees one consistent
            # parser rather than silently swapping underneath a concurrent
            # reader — the redundant fetch above was the only cost of the race.
            self._robots.setdefault(origin, parser)
            return self._robots[origin]

    def sitemap_seed_urls(self, target: str) -> list[str]:
        """Every page URL named by the target origin's robots.txt `Sitemap:`
        directive(s) (ROADMAP.md §2d).

        Reads whichever `Sitemap:` lines the already-fetched/cached robots.txt
        declares (`RobotFileParser.site_maps()` — the same parser `can_fetch`
        already uses, so this costs no extra robots.txt fetch), then fetches
        and parses each one via `_fetch_sitemap`, following a sitemap index's
        children breadth-first, bounded by `_MAX_SITEMAPS_FETCHED` and
        `_MAX_SITEMAP_URLS` against a cyclic or unbounded index. No `Sitemap:`
        directive, or every sitemap failing to fetch/parse, yields an empty
        list — the caller composes this with its own scope rules, so an empty
        result here just means no sitemap seeds, not a run-wide failure.
        """
        queue: deque[str] = deque(self._parser(target).site_maps() or [])
        fetched: set[str] = set()
        urls: list[str] = []
        while (
            queue
            and len(fetched) < _MAX_SITEMAPS_FETCHED
            and len(urls) < _MAX_SITEMAP_URLS
        ):
            sitemap_url = queue.popleft()
            if sitemap_url in fetched:
                continue
            fetched.add(sitemap_url)
            pages, children = _fetch_sitemap(self._client, sitemap_url)
            urls.extend(pages)
            queue.extend(children)
        return urls[:_MAX_SITEMAP_URLS]

    def can_fetch(self, url: str) -> bool:
        """Whether robots.txt permits fetching `url` (always True when opted out)."""
        if not self._policy.respect_robots:
            return True
        return self._parser(url).can_fetch(USER_AGENT, url)

    def crawl_delay(self, url: str) -> float:
        """Seconds to wait before fetching `url`.

        An explicit config `delay` wins; otherwise the robots.txt crawl-delay
        (when robots is respected); otherwise zero.
        """
        if self._policy.delay is not None:
            return self._policy.delay
        if not self._policy.respect_robots:
            return 0.0
        declared = self._parser(url).crawl_delay(USER_AGENT)
        return float(declared) if declared is not None else 0.0

    def _semaphore(self, domain: str) -> threading.Semaphore:
        with self._registry_lock:
            sem = self._semaphores.get(domain)
            if sem is None:
                sem = threading.Semaphore(self._policy.max_concurrent_per_domain)
                self._semaphores[domain] = sem
            return sem

    def _dispatch_lock(self, domain: str) -> threading.Lock:
        with self._registry_lock:
            lock = self._dispatch_locks.get(domain)
            if lock is None:
                lock = threading.Lock()
                self._dispatch_locks[domain] = lock
            return lock

    def acquire(self, url: str) -> None:
        """Block until a concurrency slot for `url`'s domain is free and the
        crawl-delay since the last dispatch to that domain has elapsed.

        The two are independent: the per-domain semaphore bounds how many
        fetches to that domain may be *in flight* at once
        (`max_concurrent_per_domain`), while the dispatch lock below only
        serializes the brief "may I start now" check-and-sleep so concurrent
        slot-holders for the same domain still start at least `delay` apart —
        it is released before the caller's actual fetch, so the fetches
        themselves run concurrently once released to start. A domain's
        first-ever dispatch never sleeps, matching the old sequential path's
        "never delay the very first fetch" behavior, now scoped per domain
        rather than once for the whole run (observable only once a `crawl:`
        targets more than one domain — a single-domain run, the common case,
        sees no difference).
        """
        domain = self._domain(url)
        self._semaphore(domain).acquire()
        with self._dispatch_lock(domain):
            delay = self.crawl_delay(url)
            if self._dispatched.get(domain, False) and delay > 0:
                self._sleep(delay)
            self._dispatched[domain] = True

    def release(self, url: str) -> None:
        """Free the concurrency slot `acquire` took for `url`'s domain.

        Always pair with `acquire` via `try`/`finally` — an unreleased slot
        permanently reduces that domain's effective concurrency for the rest
        of the run (deadlocking it entirely once every slot leaks).
        """
        self._semaphore(self._domain(url)).release()

    # Established call-site names, kept for `Tier1Resolver`/`Tier2Resolver` —
    # `acquire`/`release` are the same pair, named for what they actually do
    # now that there's concurrency to bound.
    before_fetch = acquire
    after_fetch = release
