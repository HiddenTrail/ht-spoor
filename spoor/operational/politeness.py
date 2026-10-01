"""Runtime politeness gate: robots.txt + crawl-delay (ROADMAP.md §2d, §6).

The declarative knobs live in `spoor.core.config.PolitenessPolicy`; this module
is the runtime that enforces them against a live crawl. §6 commits Spoor to
respecting `robots.txt` and rate-limiting by default, with overriding it an
explicit opt-out. Per §0 there is nothing site-specific here — robots.txt is
fetched and parsed the same generic way for every target.

Scope (Phase 1): allow/deny checks and run-level crawl-delay spacing over the
sequential crawl. Concurrency caps and Retry-After honoring are deferred
until a request pool / retry mechanism exists (see the ROADMAP §2d note).
"""

from __future__ import annotations

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
    answers `can_fetch`, and spaces requests via `before_fetch` using an
    run-level "first fetch happened" flag plus an injectable `sleep` (so tests
    can assert timing without real waiting).
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
        self._robots: dict[tuple[str, str], RobotFileParser] = {}
        self._fetched_any = False

    def _parser(self, url: str) -> RobotFileParser:
        parts = urlsplit(url)
        origin = (parts.scheme, parts.netloc)
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
        self._robots[origin] = parser
        return parser

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

    def before_fetch(self, url: str) -> None:
        """Sleep before every fetch but the first fetch of the run."""
        delay = self.crawl_delay(url)
        if self._fetched_any and delay > 0:
            self._sleep(delay)
        self._fetched_any = True
