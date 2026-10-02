"""Sandbox registry for exploration mode (ROADMAP.md §2e / §2h).

Exploration may perform destructive/irreversible actions *only* against a sandbox:
a target the operator controls. This module answers the one question "is this
target a sandbox?", so the interaction gate (`spoor/exploration/safety.py`) can
enforce the §2e non-negotiable that destructive actions never fire on a real site.

A target counts as a sandbox when either:

- its host is loopback — ``localhost``, ``127.0.0.0/8`` (any ``127.*``), or IPv6
  ``::1`` — i.e. self-hosted on the operator's own machine, with no declaration
  needed; or
- the operator has explicitly declared it one (``sandbox: true`` in config, passed
  in as ``declared``) **and** the host is also loopback or a private-range IP
  (RFC1918, link-local, or one of the other ranges `ipaddress` classifies as
  private — see `_is_private_host`).

`declared` is an operator *assertion*, not an unchecked bypass (closes #102): it
only ever widens what counts as a sandbox to a host that is itself at least
private-range, never to an arbitrary real, publicly-routable host. A declared
sandbox pointed at a real site (``sandbox: true`` against ``shop.example``) is
still refused — there is no config or flag that can talk the gate into treating a
real site as safe. Deliberately no site knowledge here: the rule is generic to any
target.
"""

from __future__ import annotations

import ipaddress
from urllib.parse import urlsplit


def _is_loopback_host(host: str) -> bool:
    """Whether `host` (a URL hostname) is loopback: ``localhost`` or a loopback IP.

    Loopback IPs are decided by the `ipaddress` module — the whole ``127.0.0.0/8``
    range and IPv6 ``::1`` — never by string prefix, so a *hostname* like
    ``127.evil.com`` (attacker-registerable, not loopback) is correctly rejected.
    """
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        # Not an IP literal (an ordinary hostname) — not loopback.
        return False


def _is_private_host(host: str) -> bool:
    """Whether `host` is a private-range IP literal (includes loopback).

    Decided by `ipaddress.ip_address(...).is_private` — the same module already
    used for loopback, covering RFC1918, link-local, loopback, and the other
    ranges IANA reserves as non-public. Only an IP *literal* qualifies: an
    ordinary hostname (including one an attacker registers, like
    ``10.0.0.5.evil.com``) never parses as an IP address, so it's never private
    by this check regardless of what it looks like.
    """
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return False


def is_sandbox(target: str, *, declared: bool = False) -> bool:
    """Whether `target` may host destructive exploration actions (§2e).

    True when its host is loopback (``localhost``, any ``127.0.0.0/8`` address, or
    IPv6 ``::1``) — no declaration needed — or when the operator declared it a
    sandbox *and* its host is at least a private-range IP. A declared sandbox whose
    host is a real, publicly-routable address (or an ordinary hostname that isn't
    an IP literal at all) still returns False: `declared` can never make a real
    site count as a sandbox, only confirm one the host already looks like.
    """
    host = (urlsplit(target).hostname or "").lower()
    if _is_loopback_host(host):
        return True
    return declared and _is_private_host(host)
