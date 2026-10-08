"""Spoor's shared stylesheet: night and day palettes stay complete and readable.

The theme (`spoor/exploration/theme.py`) is shared by the exploration wiki and
the local GUI. These tests pin WCAG contrast for the text colours in both
palettes, so a later colour tweak can't silently make text unreadable, and check
the two palettes define the same tokens.
"""

from __future__ import annotations

import re

import pytest

from spoor.exploration import theme

_TOKEN = re.compile(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6});")


def _night() -> dict[str, str]:
    block = theme.STYLESHEET[theme.STYLESHEET.index(":root {") :]
    block = block[: block.index("}")]
    return dict(_TOKEN.findall(block))


def _day() -> dict[str, str]:
    return dict(_TOKEN.findall(theme._DAY_TOKENS))


def _luminance(hex_colour: str) -> float:
    channels = [int(hex_colour[i : i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [
        c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def _contrast(a: str, b: str) -> float:
    high, low = sorted((_luminance(a), _luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def test_day_and_night_define_the_same_colour_tokens() -> None:
    assert set(_day()) == set(_night())


def test_day_applies_when_chosen_and_when_the_system_prefers_it() -> None:
    assert theme.STYLESHEET.count(theme._DAY_TOKENS) == 2
    assert ':root[data-theme="light"] {' in theme.STYLESHEET
    assert ':root:not([data-theme="dark"]) {' in theme.STYLESHEET


# (text token, background token, minimum ratio). 4.5 is WCAG AA for body text;
# headings (teal, large and bold) need 3. Yellow is the code colour, on surface-2.
_PAIRS = [
    ("text", "bg", 7.0),
    ("text", "surface", 7.0),
    ("text-muted", "bg", 4.5),
    ("text-muted", "surface", 4.5),
    ("accent", "bg", 4.5),
    ("accent", "surface", 4.5),
    ("yellow", "surface-2", 4.5),
    ("teal", "bg", 3.0),
]


@pytest.mark.parametrize("palette", ["night", "day"])
@pytest.mark.parametrize(("fg", "bg", "minimum"), _PAIRS)
def test_text_colours_are_readable(
    palette: str, fg: str, bg: str, minimum: float
) -> None:
    tokens = _night() if palette == "night" else _day()
    ratio = _contrast(tokens[fg], tokens[bg])
    assert ratio >= minimum, f"{palette}: --{fg} on --{bg} is {ratio:.2f}:1"


def test_button_text_is_readable_on_the_accent_in_both_palettes() -> None:
    # GUI buttons draw --bg-coloured text on an --accent background.
    for tokens in (_night(), _day()):
        assert _contrast(tokens["bg"], tokens["accent"]) >= 4.5
