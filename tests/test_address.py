"""Completing an address typed without http:// or https:// (spoor/core/address.py)."""

from __future__ import annotations

import pytest

from spoor.core.address import complete_address


@pytest.mark.parametrize(
    ("typed", "completed"),
    [
        ("localhost:3000", "http://localhost:3000"),
        ("  localhost  ", "http://localhost"),
        ("app.localhost/x", "http://app.localhost/x"),
        ("127.0.0.1:8000", "http://127.0.0.1:8000"),
        ("[::1]:8080", "http://[::1]:8080"),
        ("10.0.0.5", "http://10.0.0.5"),
        ("192.168.1.20/app", "http://192.168.1.20/app"),
        ("myserver:8080", "http://myserver:8080"),
        ("printer.local", "http://printer.local"),
        ("shop.example/sale", "https://shop.example/sale"),
        ("8.8.8.8", "https://8.8.8.8"),
        ("http://x.example", "http://x.example"),
        ("HTTPS://Up.example/", "HTTPS://Up.example/"),
        ("", ""),
    ],
)
def test_complete_address(typed: str, completed: str) -> None:
    assert complete_address(typed) == completed


def test_a_completed_local_address_is_recognised_as_a_sandbox() -> None:
    # The point of completing: without a scheme the sandbox check can't see the
    # host, so a local target was treated like a real site.
    from spoor.security.sandbox import is_sandbox

    assert not is_sandbox("localhost:3000")
    assert is_sandbox(complete_address("localhost:3000"))
