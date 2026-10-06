"""Runtime-execution regression tests for the --assert-no-new-signals reverse
assertion (ROADMAP.md §2g, closes #128; review follow-up fixes).

features/testgen.feature's scenarios only inspect the *source text* of a
generated test, never execute it — which is exactly how a `set <= list`
TypeError shipped undetected in the original #128 PR (valid Python syntax,
guaranteed runtime crash). These tests close that gap by actually executing
the generated assertion lines.
"""

from __future__ import annotations

from spoor.exploration.capture import StateSignals, diff_signals
from spoor.exploration.discovery import ActionableElement
from spoor.exploration.graph import ExplorationGraph
from spoor.testgen.pytest_gen import build_tests


def _action(label: str) -> ActionableElement:
    return ActionableElement(role="button", name=label, backend_node_id=1)


def test_the_closed_world_assertion_lines_actually_execute_without_raising() -> None:
    """The generated `assert set(x) <= set([...])` lines must be real, runnable
    Python — not just syntactically valid source (closes the set-vs-list
    TypeError a review found: `set(x) <= [...]` raises at runtime on every
    execution, which `ast.parse`-only checks can never catch)."""
    graph = ExplorationGraph()
    home = StateSignals(
        ax_node_count=1,
        console_messages=("home ready",),
        storage_keys=("session",),
        network_requests=("/home.js",),
    )
    menu = StateSignals(
        ax_node_count=2,
        console_messages=("home ready", "menu opened"),
        storage_keys=("session", "token"),
        network_requests=("/home.js", "/menu.js"),
    )
    graph.add_state("home", [], home)
    graph.add_state("menu", [], menu)
    action = _action("Open menu")
    graph.node("home").actions.append(action)
    graph.add_transition("home", action, "menu", diff_signals(home, menu))

    files = build_tests(
        graph, target="https://shop.example", assert_no_new_signals=True
    )
    src = files["test_transition_0.py"]

    closed_world_lines = [
        line.strip()
        for line in src.splitlines()
        if line.strip().startswith(("assert set(", "assert all(any(u in request"))
    ]
    assert closed_world_lines, "expected at least one closed-world assertion line"

    # Execute each line for real, against stand-ins for the generated test's own
    # `console`/`storage`/`network` locals — a live subset should pass silently,
    # proving the comparison is runnable, not just parseable.
    for line in closed_world_lines:
        namespace = {
            "console": ["home ready", "menu opened"],
            "storage": ["session", "token"],
            "network": ["https://shop.example/home.js", "https://shop.example/menu.js"],
        }
        exec(line, {}, namespace)  # noqa: S102 — executing our own generated source

    # And a genuinely unexpected value must fail the check, not silently pass —
    # the assertion still does its job after the fix.
    bad_line = next(line for line in closed_world_lines if "console" in line)
    try:
        exec(bad_line, {}, {"console": ["an utterly unexpected console line"]})
    except AssertionError:
        pass
    else:
        raise AssertionError(
            "expected the closed-world check to reject an unseen value"
        )


def test_duplicate_edges_union_their_signals_instead_of_dropping_one() -> None:
    """Two distinct `Transition` objects sharing the same edge signature (from,
    action, to) must both contribute to the closed-world union — a review
    finding: a single-value dict keyed by the edge would silently keep only
    the last one, dropping an earlier transition's legitimately-recorded
    signals from the set a later transition's reverse assertion checks
    against."""
    graph = ExplorationGraph()
    root = StateSignals(ax_node_count=1)
    mid = StateSignals(ax_node_count=1, console_messages=("from first copy",))
    leaf = StateSignals(ax_node_count=1, console_messages=("leaf added",))
    graph.add_state("root", [], root)
    graph.add_state("mid", [], mid)
    graph.add_state("leaf", [], leaf)
    hop = _action("Go")
    graph.node("root").actions.append(hop)
    # Two distinct Transition objects, same (from, action.role, action.name, to)
    # edge signature, but different recorded signals -- as could arise from two
    # separate runs merged by --resume-from.
    graph.add_transition("root", hop, "mid", diff_signals(root, mid))
    other_mid = StateSignals(ax_node_count=1, console_messages=("from second copy",))
    graph.add_transition("root", hop, "mid", diff_signals(root, other_mid))
    leaf_action = _action("Finish")
    graph.node("mid").actions.append(leaf_action)
    graph.add_transition("mid", leaf_action, "leaf", diff_signals(mid, leaf))

    files = build_tests(
        graph, target="https://shop.example", assert_no_new_signals=True
    )
    # The leaf transition is test_transition_2 (index order: root->mid (#0),
    # root->mid dup (#1), mid->leaf (#2)).
    src = files["test_transition_2.py"]
    # Both duplicate hops' own console additions must appear in the closed set
    # the leaf's reverse assertion checks against -- not just whichever one a
    # single-value dict happened to keep last.
    assert "from first copy" in src
    assert "from second copy" in src
