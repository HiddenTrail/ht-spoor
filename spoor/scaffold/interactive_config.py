"""Interactive-round config scaffold generation (ROADMAP.md §2e, issue #131).

Round-one exploration (`spoor explore`) is strictly read-only: it never types into a
field or logs in. This module is the first, scoped piece of the planned *second*
round — the "second-round interactive exploration" design note in `docs/ROADMAP.md`
§2e — and covers scaffold *generation* only: turning an already-completed
`ExplorationGraph` into a human-editable YAML file listing what a future interactive
round would need. Consuming a filled-in scaffold to actually run round two is out of
scope here; nothing in this module reads or enforces anything a user fills in.

Mirrors the pure-builder / thin-disk-writer split `spoor/testgen/pytest_gen.py` and
the wiki renderer already use: `build_scaffold` is pure (no disk, no browser),
`render_scaffold` is the thin writer.

Three sections, each generic (§0) — no site-specific logic anywhere in this module:

- **fields** — every discovered text-entry-like element (textbox/searchbox/combobox/
  listbox) that is *not* a login field, each with a best-guess `kind` inferred from
  its DOM `input_type` (§2e scaffold slice 1's `ActionableElement.input_type`
  enrichment) and a blank `value:` for the user to pin. An element whose input type
  isn't recognized gets an honest `kind: unknown` rather than a guessed default.
- **login_points** — every discovered `input_type == "password"` field. These are
  never generatable: Spoor does not automate logins (`docs/ROADMAP.md` §2h,
  bring-your-own-session, decided). An entry is a flag plus a blank `session:` key
  pointing at the same storage-state mechanism a `§2a` config already uses — never a
  username/password pair.
- **destructive_actions** — every skip whose recorded reason is exactly the safety
  gate's own `DESTRUCTIVE_SKIP_REASON` (`spoor/exploration/safety.py`) — matching what
  actually happened during the crawl, not re-deriving a guess from the action's label,
  which would misclassify a destructive-looking name skipped for an unrelated reason
  (e.g. an overlay blocking it). Informational only: nothing here grants permission,
  and an `allow:` key the user flips is not read or enforced by anything yet.
"""

from __future__ import annotations

from pathlib import Path

from spoor.exploration.discovery import ActionableElement
from spoor.exploration.graph import ExplorationGraph, paths_from_root
from spoor.exploration.safety import DESTRUCTIVE_SKIP_REASON
from spoor.security.redaction import redact

# Field-like roles worth a generator guess — checkboxes/radios/buttons are actions to
# fire, not values to provision, so they stay out of `fields:` entirely. Public: also
# the set `spoor/scaffold/apply.py` matches a scaffold field's name against, so the two
# stay in lockstep by construction rather than by two separately-maintained lists.
FIELD_ROLES = frozenset({"textbox", "searchbox", "combobox", "listbox"})

_SHORT_ID = 12  # state ids are 64-char hashes; a short prefix labels a scaffold entry

# DOM input_type -> (generator kind, human-readable note, example value). Deliberately
# small and honest: an input_type outside this table gets `kind: unknown` rather than
# a guessed default, never a silently-wrong generator.
_GENERATOR_TABLE: dict[str, tuple[str, str, str]] = {
    "email": ("email", "looks like an email address", "jane.doe@example.com"),
    "tel": ("phone", "looks like a phone number", "+1-555-0100"),
    "url": ("url", "looks like a URL", "https://example.com"),
    "number": ("number", "looks like a number", "42"),
    "date": ("date", "looks like a date", "2026-01-15"),
    "search": ("text", "a search box", "example search term"),
    "text": ("text", "free text", "example text"),
}


def _yaml_str(value: str) -> str:
    """A YAML-safe inline scalar for `value` (quoted/escaped only when it needs it).

    `yaml.safe_dump` treats its input as a whole document, so a plain (unquoted)
    scalar comes back with a trailing `...` document-end marker on its own line —
    harmless in a real document but wrong to splice inline. Only the first line is
    ever the scalar itself, so that's all this keeps.
    """
    import yaml

    return yaml.safe_dump(value, default_style=None).split("\n", 1)[0]


def infer_field(element: ActionableElement) -> tuple[str, str, str | None]:
    """A (kind, note, example) guess for a non-login field, from its DOM input type.

    Pure and total — never raises, never guesses silently wrong. `input_type` values
    this module doesn't recognize (including None, when the driver had nothing to
    enrich the node with) fall back to `kind="unknown"`, honestly flagging that the
    user needs to fill this one in by hand. A `combobox`/`listbox` role without a
    recognized `input_type` gets its own note (a fixed-options field whose options
    this slice doesn't enumerate), rather than the generic unknown note.
    """
    if element.input_type is not None and element.input_type in _GENERATOR_TABLE:
        return _GENERATOR_TABLE[element.input_type]
    if element.role in ("combobox", "listbox"):
        return ("choice", "a fixed-options field — options not enumerated", None)
    return ("unknown", "no generator inferred", None)


def build_scaffold(graph: ExplorationGraph, *, target: str) -> str:
    """Render an exploration graph into a YAML config-scaffold (pure, §2e issue #131).

    No disk, no browser — mirrors `pytest_gen.build_tests`. Returns an empty string
    for a graph with no states, so `render_scaffold` writes nothing.
    """
    if not graph.states:
        return ""

    paths = paths_from_root(graph)
    field_lines: list[str] = []
    login_lines: list[str] = []
    for state_id in graph.states:
        node = graph.node(state_id)
        short = state_id[:_SHORT_ID]
        for action in node.actions:
            if action.role not in FIELD_ROLES:
                continue
            name = redact(action.name) or "(unnamed)"
            if action.input_type == "password":
                path = paths.get(state_id, [])
                via = " -> ".join(redact(step.name) or "(unnamed)" for step in path)
                login_lines.append(
                    f"  - state: {short}\n"
                    f"    name: {_yaml_str(name)}\n"
                    f"    # reached via: {via or '(start state)'}\n"
                    f"    # fill with a path to a storage-state JSON — see the\n"
                    f"    # session: field in a §2a config. Spoor never automates\n"
                    f"    # logging in; supply a session you authenticated yourself.\n"
                    f"    session:\n"
                )
                continue
            kind, note, example = infer_field(action)
            example_line = (
                f"    example: {_yaml_str(example)}\n" if example is not None else ""
            )
            field_lines.append(
                f"  - state: {short}\n"
                f"    name: {_yaml_str(name)}\n"
                f"    kind: {kind}  # {note}\n"
                f"{example_line}"
                f"    value:  # fill in to pin this field's value\n"
            )

    destructive_lines: list[str] = []
    for skip in graph.skipped:
        # Match the gate's own recorded reason, not a re-derived guess: an element
        # whose label happens to contain a destructive keyword but was skipped for an
        # unrelated reason (e.g. an overlay blocking it) must not be misreported here.
        if skip.reason != DESTRUCTIVE_SKIP_REASON:
            continue
        name = redact(skip.action.name) or "(unnamed)"
        short = skip.from_state[:_SHORT_ID]
        destructive_lines.append(
            f"  - state: {short}\n"
            f"    name: {_yaml_str(name)}\n"
            f"    role: {skip.action.role}\n"
            f"    # informational only — flipping this does not grant permission;\n"
            f"    # destructive actions stay sandbox-only regardless (§2e).\n"
            f"    allow: false\n"
        )

    parts = [
        "# Interactive-round config scaffold — generated by Spoor (ROADMAP.md §2e).\n"
        "# This is a starting point for a *planned*, not-yet-built interactive round;\n"
        "# filling it in does nothing on its own today. Nothing here was typed into\n"
        f"# the target, which was mapped read-only. Target: {target}\n",
        "fields:\n" + ("".join(field_lines) if field_lines else "  []\n"),
        "\n",
        "# Spoor does not automate logins (docs/ROADMAP.md §2h). Each entry below is\n"
        "# a flag, not a fillable credential — point session: at a storage-state file\n"
        "# you already exported by authenticating yourself.\n"
        "login_points:\n" + ("".join(login_lines) if login_lines else "  []\n"),
        "\n",
        "# Every skip the safety gate made for being destructive outside a sandbox.\n"
        "# allow: is not read by anything yet — see the module docstring.\n"
        "destructive_actions:\n"
        + ("".join(destructive_lines) if destructive_lines else "  []\n"),
    ]
    return "".join(parts)


SCAFFOLD_FILENAME = "interactive.yaml"
"""The fixed filename every `render_scaffold` call writes, inside the given directory.

A named constant, not a caller-chosen name: `--scaffold` takes a directory, the same
as `--wiki`/`--gen-tests`, so there is one flag *shape* to remember across every
output a run can produce, not a mix of "this one wants a file, that one wants a
folder" — the mismatch that let `--wiki` and `--scaffold` collide on the same path in
a real incident before this changed (§2e issue #131 follow-up).
"""


def render_scaffold(
    graph: ExplorationGraph, out_dir: Path, *, target: str
) -> Path | None:
    """Write the config scaffold for `graph` into `out_dir` (thin writer, issue #131).

    Mirrors `pytest_gen.render_suite`/`wiki.render_wiki`: pure `build_scaffold` first,
    then a plain UTF-8 write to `out_dir/{SCAFFOLD_FILENAME}`, creating `out_dir` if
    needed. A graph with no states writes nothing and returns None, matching
    `render_suite`'s empty-graph contract.
    """
    text = build_scaffold(graph, target=target)
    if not text:
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / SCAFFOLD_FILENAME
    out_path.write_text(text, encoding="utf-8")
    return out_path
