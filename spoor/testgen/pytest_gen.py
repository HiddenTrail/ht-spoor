"""Generate replayable pytest regression tests from an exploration graph (§2g).

Sub-slice 2g-i, the pure generator — no browser and no disk in `build_tests`, exactly
the split the wiki renderer took (6a). §2g's premise is that a captured map is already
a golden-master record (state X, action Y, produced signal bundle Z), so exporting it
as a runnable test is the last-mile step. For each mapped `Transition` this emits a
pytest test that drives Playwright to **replay the reset-and-replay path** that reached
the transition's from-state (reconstructed from the recorded edges), **fire the
action**, and **assert the signals the action was recorded to add** still appear — a
real regression test the consuming team runs against the live product, not a check of
the map's own internal consistency.

The generated files are a **shared-output surface**, so §2h redaction is mandatory:
every captured value written into them (console lines, storage keys, request URLs,
action names, the target URL) passes through `spoor.security.redaction.redact` first.
That has a consequence the wiki did not face — a generated test *asserts* recorded
values against the live page's *raw* runtime values, so both sides must be redacted
like-for-like or a redacted expectation could never match. The suite therefore redacts
the live values it observes with the same primitive before comparing (`redact_all` in
the emitted `_spoor_testkit`), so an assertion checks that behaviour *as Spoor records
and shares it* is unchanged, and no raw secret is ever baked into a test. Running the
suite consequently needs `ht-spoor` (for `redact`) and `playwright` installed — a
deliberate, recorded dependency, taken because the §2h-safe alternative (emitting the
raw secret so the assertion matches) is a non-negotiable violation.

Two honest limitations are recorded here. (1) Only the **additive string signals**
(console, storage, network) are asserted; the accessibility-node delta and the
screenshot hash are not, because reproducing them in the generated runtime needs
Spoor's CDP a11y read and visual hasher — a larger surface deferred to a follow-on,
the same staged deferral the wiki took for screenshot *images*. (2) An action whose
accessible **name itself contains a secret** is redacted like any shared value, so the
emitted role locator would not match the live element — accepted as rare (accessible
names are UI labels, essentially never secrets) and preferred over the §2h violation of
writing the raw name. Nothing here is site-specific (§0): one emitter for every target.

**Reverse assertion, opt-in (closes #128).** The checks above are all one-directional:
"these recorded values must still appear." They say nothing about the inverse — a
backend change that makes a transition start firing an *extra* request or logging a
new console line produces no assertion failure, since nothing new was ever checked
for. `assert_no_new_signals=True` (threaded from
`spoor explore --assert-no-new-signals`, which requires `--gen-tests`) adds, per
signal kind, a closed-world check: the live replay's observed values must be a
subset of everything recorded as added *anywhere on
the replayed path that reaches this transition* — not just this transition's own
diff, since the generated test's console/network listeners are attached for the whole
replay (every earlier hop's additions are still "in view" when the final assertion
runs; checking only the leaf transition's own set would false-positive on each earlier
transition's legitimate additions). The closed set also unconditionally includes the
**root state's own captured signals** (its full snapshot, not a diff): every generated
test's replay starts with a bare `page.goto(TARGET)` before any action fires, so
whatever that navigation alone produces (an analytics beacon, a consent-banner console
line, a theme preference already in storage) is in view from the first line of the
test — but it is never recorded as any transition's own "added" diff, since there is
no "before" state to diff the landing page against. Seeding it from the root's
snapshot is what keeps this check usable on an ordinary real site rather than
false-positiving on page-load noise for any touched signal kind. The check is still
emitted only for a kind with at least one value in its closed set — root noise alone
can be enough to emit one even for a kind no transition ever added to. This is a first
slice with no noise normalization (ROADMAP.md §2g/#211 decision note — the
"freshness by re-observation" design, previously mis-cited there as #107): a value that
legitimately varies run to run (a timestamp query parameter, a random request id) is
asserted literally, so a generated suite using this flag can still be noisier than one
without it — an explicit, documented trade-off, not an oversight.
"""

from __future__ import annotations

from pathlib import Path

from spoor.exploration.capture import StateSignals
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.graph import (
    ExplorationGraph,
    Transition,
    path_steps_from_root,
    paths_from_root,
)
from spoor.security.redaction import redact

# The stable filenames of the two fixed support modules the suite always carries.
_TESTKIT = "_spoor_testkit.py"
_CONFTEST = "conftest.py"
_SHORT_ID = 12  # state ids are 64-char hashes; a short prefix labels a test readably

_TESTKIT_SOURCE = '''\
"""Shared helpers for the generated Spoor regression suite (ROADMAP.md §2g).

Generated by Spoor from a captured exploration map; do not edit by hand. Running the
suite needs `ht-spoor` and `playwright` installed: the tests drive a real browser and
redact the live values they observe with Spoor's own redaction primitive before
comparing, so an assertion checks that behaviour as Spoor records and shares it is
unchanged and no raw secret is baked into a test.
"""

from __future__ import annotations

from spoor.security.redaction import redact

TARGET = {target!r}


def redact_all(items):
    """Redact each observed value, so it compares like-for-like with a recorded one."""
    return [redact(item) for item in items]


def storage_keys(page):
    """The live page's localStorage + sessionStorage keys."""
    return page.evaluate(
        "() => [...Object.keys(localStorage), ...Object.keys(sessionStorage)]"
    )


def fire(page, role, name):
    """Click an element by ARIA role and optional accessible name, first match."""
    if name:
        locator = page.get_by_role(role, name=name, exact=True)
    else:
        locator = page.get_by_role(role)
    locator.first.click()
    page.wait_for_load_state()


def fill(page, role, name, value):
    """Type into an element by ARIA role and accessible name, first match.

    Mirrors PlaywrightDriver.fill: click to focus, select any existing content, then
    type with real keystrokes -- a typed transition (§2e issue #137), not a click.
    """
    if name:
        locator = page.get_by_role(role, name=name, exact=True)
    else:
        locator = page.get_by_role(role)
    locator.first.click()
    page.keyboard.press("Control+A")
    page.keyboard.type(value)
    page.wait_for_load_state()


def reach(page, path):
    """Reset to the target and replay the recorded path of (role, name, value) steps.

    `value` is None for a clicked step (replayed with `fire`) or a string for a typed
    step (replayed with `fill`) -- a fill-revealed state's own incoming edge is typed,
    never clicked (§2e issue #137).
    """
    page.goto(TARGET)
    page.wait_for_load_state()
    for role, name, value in path:
        if value is None:
            fire(page, role, name)
        else:
            fill(page, role, name, value)
'''

_CONFTEST_SOURCE = '''\
"""Pytest fixtures for the generated Spoor regression suite (ROADMAP.md §2g).

Generated by Spoor; do not edit by hand.
"""

from __future__ import annotations

import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture
def page():
    """A fresh Chromium page recording the console messages and requests it sees."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        pg = browser.new_context().new_page()
        pg.spoor_console = []
        pg.spoor_network = []
        pg.on("console", lambda message: pg.spoor_console.append(message.text))
        pg.on("request", lambda request: pg.spoor_network.append(request.url))
        try:
            yield pg
        finally:
            browser.close()
'''


def build_tests(
    graph: ExplorationGraph, *, target: str, assert_no_new_signals: bool = False
) -> dict[str, str]:
    """Render an exploration graph into a pytest suite: filename -> source (§2g).

    Emits nothing for a graph with no transitions (there is nothing to replay). For a
    non-empty graph, returns the two fixed support modules plus one `test_transition_N`
    file per mapped transition, in the graph's transition order. Pure — no disk, no
    browser; `render_suite` (a thin writer, sub-slice 2g-ii) puts these on disk.

    `assert_no_new_signals` adds the opt-in reverse assertion described in the module
    docstring (closes #128) to every generated test.
    """
    transitions = graph.transitions
    if not transitions:
        return {}
    paths = paths_from_root(graph)
    files = {
        _TESTKIT: _TESTKIT_SOURCE.format(target=redact(target)),
        _CONFTEST: _CONFTEST_SOURCE,
    }
    # Computed once, not per transition (closes a review finding against #128):
    # both are whole-graph structures, so rebuilding them inside the loop below
    # was O(T) work repeated T times for no reason.
    by_edge = _edge_index(graph) if assert_no_new_signals else {}
    steps_from_root = path_steps_from_root(graph) if assert_no_new_signals else {}
    root_id = graph.states[0]
    root_signals = graph.node(root_id).signals if assert_no_new_signals else None
    for index, transition in enumerate(transitions):
        path = paths.get(transition.from_state, [])
        closed_world = (
            _closed_world_signals(
                transition, root_id, by_edge, steps_from_root, root_signals
            )
            if assert_no_new_signals
            else None
        )
        files[f"test_transition_{index}.py"] = _render_test(
            index, transition, path, closed_world
        )
    return files


def render_suite(
    graph: ExplorationGraph,
    out_dir: Path,
    *,
    target: str,
    assert_no_new_signals: bool = False,
) -> list[Path]:
    """Write the generated pytest suite for `graph` under `out_dir` (§2g, 2g-ii).

    The thin on-disk counterpart to `build_tests`, mirroring the wiki writer (6a):
    render the sources purely, then write each `filename -> source` as UTF-8, creating
    `out_dir` (and parents) if needed. Returns the written paths sorted, for a stable,
    testable result. A graph with no transitions renders nothing, so nothing is written
    and the returned list is empty — no empty shell of a suite. Every value baked into
    the sources was already §2h-redacted by `build_tests`; this writer adds no new
    captured value, so it introduces no redaction surface of its own. Nothing here is
    site-specific (§0).
    """
    files = build_tests(
        graph, target=target, assert_no_new_signals=assert_no_new_signals
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name in sorted(files):
        path = out_dir / name
        path.write_text(files[name], encoding="utf-8")
        written.append(path)
    return written


def _edge_index(
    graph: ExplorationGraph,
) -> dict[tuple[str, str, str, str], list[Transition]]:
    """Every transition, grouped by the edge it fires (from/action/to) (§2g, #128).

    A list per edge, not a single transition: two distinct `Transition` objects
    can legitimately share the same edge signature (e.g. after a `--resume-from`
    merge), and a single-value dict would silently keep only the last one seen,
    dropping an earlier transition's own recorded signals from the closed-world
    union below. Grouping instead means every such transition's signals are
    counted — a closed-world set can only get *more* inclusive from that, which
    is the safe direction for a check whose whole job is "don't false-positive
    on something that really was seen."
    """
    index: dict[tuple[str, str, str, str], list[Transition]] = {}
    for t in graph.transitions:
        key = (t.from_state, t.action.role, t.action.name, t.to_state)
        index.setdefault(key, []).append(t)
    return index


def _closed_world_signals(
    transition: Transition,
    root_id: str,
    by_edge: dict[tuple[str, str, str, str], list[Transition]],
    steps_from_root: dict[str, list[tuple[ActionableElement, str]]],
    root_signals: StateSignals | None,
) -> tuple[frozenset[str], frozenset[str], frozenset[str]]:
    """The redacted union of console/storage/network values recorded as added across
    every transition on the replay path that reaches `transition`, including the
    transition itself (§2g, closes #128).

    The generated test's console/network listeners are attached for the whole replay,
    not scoped to the final hop, so the closed set a reverse assertion checks against
    must be the union across the path too — otherwise an earlier hop's own recorded
    addition would false-positive the check on the later transition's test.

    `root_signals` (the root state's own full captured snapshot, not a diff) is
    unioned in unconditionally: every generated test's replay starts with
    `page.goto(TARGET)` before any action fires, so whatever that bare navigation
    alone produces (an analytics beacon, a consent-banner console warning, a
    theme preference already in storage) is in view from the first line — but
    it is never recorded as *any* transition's own "added" diff, since there is
    no "before" state to diff the landing page against. Without seeding it here,
    that ordinary page-load noise would false-positive the very first generated
    test for any touched signal kind on any real site that logs or requests
    anything on load — not just an edge case, the common case.
    """
    steps = steps_from_root.get(transition.from_state, [])
    chain: list[Transition] = []
    current = root_id
    for action, landed in steps:
        chain.extend(by_edge.get((current, action.role, action.name, landed), []))
        current = landed
    chain.append(transition)
    console: set[str] = set()
    storage: set[str] = set()
    network: set[str] = set()
    if root_signals is not None:
        console.update(redact(v) for v in root_signals.console_messages)
        storage.update(redact(v) for v in root_signals.storage_keys)
        network.update(redact(v) for v in root_signals.network_requests)
    for hop in chain:
        if hop.signals is None:
            continue
        console.update(redact(v) for v in hop.signals.console_added)
        storage.update(redact(v) for v in hop.signals.storage_added)
        network.update(redact(v) for v in hop.signals.network_added)
    return frozenset(console), frozenset(storage), frozenset(network)


def _locator_args(action: ActionableElement) -> str:
    """The `fire(...)` arguments for a clicked action: role and redacted name."""
    return f"{action.role!r}, {redact(action.name)!r}"


def _fill_value_repr(action: ActionableElement) -> str:
    """The redacted `fill_value` literal for a path/action step, or `None`'s repr."""
    return "None" if action.fill_value is None else repr(redact(action.fill_value))


def _path_step_repr(action: ActionableElement) -> str:
    """One `_PATH` tuple: role, redacted name, and redacted fill value or `None`."""
    return f"({action.role!r}, {redact(action.name)!r}, {_fill_value_repr(action)})"


def _fire_line(action: ActionableElement) -> str:
    """The final replay line for a transition's own action: `fire(...)`/`fill(...)`."""
    if action.fill_value is None:
        return f"    fire(page, {_locator_args(action)})\n"
    return f"    fill(page, {_locator_args(action)}, {_fill_value_repr(action)})\n"


def _render_test(
    index: int,
    transition: Transition,
    path: list[ActionableElement],
    closed_world: tuple[frozenset[str], frozenset[str], frozenset[str]] | None,
) -> str:
    """Render one transition's regression test source (§2g)."""
    action = transition.action
    label = redact(action.name) or "(unnamed)"
    heading = (
        f"{transition.from_state[:_SHORT_ID]} --{label}--> "
        f"{transition.to_state[:_SHORT_ID]}"
    )
    path_lines = "".join(f"    {_path_step_repr(step)},\n" for step in path)
    body = _assertion_body(transition, closed_world)
    return (
        "from __future__ import annotations\n\n"
        "from _spoor_testkit import fill, fire, reach, redact_all, storage_keys\n\n"
        f"_PATH = [\n{path_lines}]\n\n\n"
        f"def test_transition_{index}(page):\n"
        f'    """{heading} (replay, fire, assert)."""\n'
        "    reach(page, _PATH)\n"
        f"{_fire_line(action)}"
        f"{body}"
    )


def _assertion_body(
    transition: Transition,
    closed_world: tuple[frozenset[str], frozenset[str], frozenset[str]] | None = None,
) -> str:
    """The capture-and-assert lines for a transition's recorded additive signals (§2g).

    Only the additive string signals are asserted (see the module note on the deferred
    a11y/screenshot deltas). A transition with no recorded change gets a smoke test: it
    still replayed and fired the action above, and asserts nothing it never recorded.

    `closed_world`, when given, is the three redacted closed sets
    `_closed_world_signals` computed (closes #128): a reverse "and nothing else" check
    is appended for each kind that has at least one entry, alongside (not instead of)
    the existing per-item checks.
    """
    signals = transition.signals
    closed_console, closed_storage, closed_network = closed_world or (
        frozenset(),
        frozenset(),
        frozenset(),
    )
    lines: list[str] = []
    if (signals is not None and signals.console_added) or closed_console:
        lines.append("    console = redact_all(page.spoor_console)")
        for message in signals.console_added if signals is not None else ():
            lines.append(f"    assert {redact(message)!r} in console")
        if closed_console:
            lines.append(
                f"    assert set(console) <= set({sorted(closed_console)!r}), "
                '"unexpected console message(s) not seen during the original crawl"'
            )
    if (signals is not None and signals.storage_added) or closed_storage:
        lines.append("    storage = redact_all(storage_keys(page))")
        for key in signals.storage_added if signals is not None else ():
            lines.append(f"    assert {redact(key)!r} in storage")
        if closed_storage:
            lines.append(
                f"    assert set(storage) <= set({sorted(closed_storage)!r}), "
                '"unexpected storage key(s) not seen during the original crawl"'
            )
    if (signals is not None and signals.network_added) or closed_network:
        lines.append("    network = redact_all(page.spoor_network)")
        for url in signals.network_added if signals is not None else ():
            lines.append(
                f"    assert any({redact(url)!r} in request for request in network)"
            )
        if closed_network:
            lines.append(
                "    assert all(any(u in request for u in "
                f"{sorted(closed_network)!r}) for request in network), "
                '"unexpected network request(s) not seen during the original crawl"'
            )
    if not lines:
        lines.append("    # no signal changes were recorded for this transition")
    return "\n".join(lines) + "\n"
