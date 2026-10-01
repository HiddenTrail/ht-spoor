"""Operator-supplied request/response hooks (ROADMAP.md §2d, part of #150).

A way to extend a run — add a header, transform a fetched page before
extraction — without writing site-specific code into `spoor/core/` (§0). Hooks
are plain Python callables, supplied at the same injection seam `healer`/
`sleep`/`client` already use (`extract.run_report(cfg, hooks=...)`), not a
config field: a hook is code the operator brings, not declarative per-target
config `load_config` could parse from YAML.

Both resolution tiers call these identically, so a hook written once works
against either. Two safety properties hold by construction, not by convention:

- `on_request` may only *add* headers to a URL the politeness gate has already
  decided to fetch — it cannot change or redirect that URL, so it can never be
  used to route a request around the gate's robots.txt check.
- `on_response` only ever sees pre-extraction HTML text, upstream of the
  output pipeline's schema validation and §2h redaction — it has no path to
  shared output that skips either.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

#: Called with the URL about to be fetched; may return extra headers to merge
#: into that request, or None to add nothing.
OnRequest = Callable[[str], dict[str, str] | None]

#: Called with the URL and its fetched/rendered HTML, before extraction; may
#: return replacement HTML to extract from instead, or None to leave it as is.
OnResponse = Callable[[str, str], str | None]


@dataclass
class RunHooks:
    """The hooks a run was supplied, if any. Omitted fields do nothing."""

    on_request: OnRequest | None = None
    on_response: OnResponse | None = None
