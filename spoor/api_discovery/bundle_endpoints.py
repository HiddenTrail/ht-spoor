"""Static JS-bundle endpoint discovery — §2b layer 6 (ROADMAP.md §2b, closes #153).

docs/COMPETITIVE_PLAN.md flags OWASP ZAP/Katana's static JS-bundle analysis: finding
API endpoints/routes referenced in a page's JavaScript without ever executing it.
This complements the runtime API-surface discovery layers (observed traffic, layer
4; action correlation, layer 5) with a path that finds calls no click ever
triggered — an endpoint only referenced in a bundle's string literals, never fired
during this run.

Like layer 1's own JS-bundle scan (`discovery.py`, finding a *spec* reference), this
fetches the landing page and its same-origin `<script src>` bundles and scans the
raw text — no JS parsing, no execution, nothing beyond what layer 1 already does for
spec discovery (the same known, deferred optimization applies: re-fetching the
landing page here, separately from the resolver's own fetch and from layer 1's own
fetch, is accepted for the same reason layer 1 accepts it — see its module
docstring). Finding *endpoints* instead of a spec reference needs a different,
broader pattern: any quoted string literal that looks like an absolute path
(`/api/users/42`), filtered against an obvious-static-asset denylist (images,
stylesheets, fonts, source maps) so the bundle's own asset references don't flood
the result. A string match here is a **candidate only** — nothing is fetched to
confirm it exists, matching the "never execute it" premise literally and keeping
this layer free of any network probing beyond the bundle fetches layer 1 already
makes routine. Paths are templated with the same generic ID rule layer 4 uses
(`_template_path`), so `/users/42` and `/users/43` found in different strings
collapse into one `/users/{id}` candidate instead of two.

Bounded claim (§2b): a reported endpoint is a string literal that *looks*
path-shaped, never confirmed to be real, reachable, or actually called — false
positives (a CSS class string that happens to start with `/`, a comment, dead code)
are expected and accepted, the same trade-off layer 1's loose spec-reference
matching already makes. Nothing here is site-specific (§0): the extraction pattern
and the asset denylist are generic conventions, identical for every target.
"""

from __future__ import annotations

import re
from urllib.parse import urlsplit

import httpx

from spoor.api_discovery.discovery import _fetch, _script_srcs
from spoor.api_discovery.synthesis import _template_path
from spoor.core.config import PolitenessPolicy
from spoor.operational.politeness import Politeness

# Same bound layer 1's own bundle scan uses, for the same reason: keeps a page
# that loads many scripts a bounded, near-free companion probe.
_MAX_SCRIPT_BUNDLES = 10

# A hard ceiling on how many distinct templated candidates are returned, so a
# bundle packed with path-shaped strings (minified vendor code, i18n route
# tables) can't produce an unbounded result.
_MAX_ENDPOINTS = 200

# A quoted string literal (single/double/backtick), kept short enough that a
# whole minified line can't be swallowed as "one string".
_QUOTED_STRING = re.compile(r"""["'`]([^"'`\n]{2,200})["'`]""")

# Extensions that mark a path-shaped string as a static asset, not an API
# endpoint — a generic denylist (§0), not a target-specific one.
_STATIC_EXTENSIONS = (
    ".js",
    ".mjs",
    ".cjs",
    ".css",
    ".map",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".webp",
    ".avif",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".otf",
    ".mp4",
    ".mp3",
    ".wav",
    ".pdf",
    ".html",
    ".htm",
)


def _looks_like_endpoint(candidate: str) -> bool:
    """Whether a quoted string looks like an absolute API path, not noise (§2b).

    Conservative on purpose: must be an absolute path (starts with exactly one
    `/`), carry no whitespace or `<`/`>` (a stray HTML/JSX fragment, not a path),
    and not end in a known static-asset extension. Everything else that clears
    this bar is reported as a candidate — the string-literal match is inherently
    loose (see the module docstring); this only filters out the obvious non-matches.
    """
    if not candidate.startswith("/") or candidate.startswith("//"):
        return False
    path = candidate.split("?", 1)[0].split("#", 1)[0]
    if path in ("", "/"):
        return False
    if any(ch.isspace() for ch in path) or "<" in path or ">" in path:
        return False
    if path.lower().endswith(_STATIC_EXTENSIONS):
        return False
    return any(segment for segment in path.split("/"))


def _endpoint_candidates(js_text: str) -> set[str]:
    """Templated endpoint candidates found in one bundle's raw text (§2b)."""
    found: set[str] = set()
    for match in _QUOTED_STRING.finditer(js_text):
        candidate = match.group(1)
        if _looks_like_endpoint(candidate):
            path = candidate.split("?", 1)[0].split("#", 1)[0]
            found.add(_template_path(path))
    return found


def discover_bundle_endpoints(
    target: str,
    client: httpx.Client,
    *,
    policy: PolitenessPolicy | None = None,
) -> tuple[str, ...]:
    """Find endpoint-shaped strings in `target`'s same-origin JS bundles (§2b, #153).

    Fetches the landing page, then each same-origin `<script src>` bundle it loads
    (capped at `_MAX_SCRIPT_BUNDLES`, robots-honored like every §2b probe, never
    crawl-delay-spaced — a bounded, one-time companion scan, not a crawl), scanning
    each for quoted strings that look like an absolute API path. Never raises: a
    failed landing-page fetch or bundle fetch simply contributes nothing. Returns
    templated, de-duplicated, sorted candidates, capped at `_MAX_ENDPOINTS`. Every
    candidate is unconfirmed — nothing is fetched to validate it exists, matching
    the "without ever executing it" premise literally.
    """
    parts = urlsplit(target)
    if not parts.scheme or not parts.netloc:
        return ()
    gate = Politeness(policy or PolitenessPolicy(), client)
    response = _fetch(client, target, gate)
    if response is None:
        return ()
    html = response.text
    page_url = str(response.url)
    found: set[str] = set()
    for src in _script_srcs(html, page_url)[:_MAX_SCRIPT_BUNDLES]:
        bundle = _fetch(client, src, gate)
        if bundle is None:
            continue
        found |= _endpoint_candidates(bundle.text)
    return tuple(sorted(found))[:_MAX_ENDPOINTS]
