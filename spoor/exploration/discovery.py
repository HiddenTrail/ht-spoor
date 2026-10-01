"""Actionable-element discovery for exploration mode (ROADMAP.md §2e).

The third §2e slice, still pure logic. The explorer must decide what to try next on
a screen; this answers "what *can* be interacted with here?" without a new
mechanism, by reusing the §2c accessibility-tree signal. That snapshot (the CDP
`Accessibility.getFullAXTree` node list, as `AccessibilityCollector` captures it)
already labels every node with a generic ARIA role, so discovery is: keep the nodes
whose role is interactive and that aren't ignored — except a native `<video>`/
`<audio>` element's own control children (play/mute/volume/scrubber/fullscreen/...),
which live inside the browser's closed user-agent shadow DOM and can never pass the
live click-verification every other element relies on (`_has_media_ancestor`) — and
read each one's role, accessible name, backend DOM node id, and — when the driver
enriched the node with one — its destination hint (a link's target URL path, read
from `href`; §2e slice 9b) and its DOM `input_type` (an `<input>` element's `type`
attribute).

The accessible name is the label the safety gate (`safety.py`) classifies; the
backend node id is kept so the (later) explorer loop can locate the element to act
on it. This slice only discovers — driving actions is the explorer loop. Generic to
every target (§0): the interactive-role set, and the media-control exclusion, are
the same for all.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

# Interactive ARIA roles — a node with one of these is something a user can act on.
# A maintainable, PR-extendable set (§2e), never a runtime config or site-specific.
ACTIONABLE_ROLES = frozenset(
    {
        "button",
        "link",
        "checkbox",
        "radio",
        "textbox",
        "searchbox",
        "combobox",
        "listbox",
        "option",
        "menuitem",
        "menuitemcheckbox",
        "menuitemradio",
        "tab",
        "switch",
        "slider",
        "spinbutton",
        "treeitem",
    }
)


@dataclass(frozen=True)
class ActionableElement:
    """One thing the explorer could interact with on a screen (§2e).

    `role` and `name` come straight from the accessibility node (the name is the
    label the safety gate classifies, and `role`+`name` are what the live driver
    re-locates the element by when it acts). `backend_node_id` is the CDP node
    handle *within the snapshot it was discovered in* — it does not survive a page
    reload, so it is kept for correlation/debugging rather than for clicking after a
    reset-and-replay; None when the node carried none.

    `destination` is a *hint* at where activating this element leads — the URL path
    of a link's target, read from its `href` before any click (§2e slice 9b) — or
    None when the element carries no static destination (a button, a JS-driven
    control, a non-navigational `href` like `javascript:`). It is only a hint: the
    real state reached is still whatever clicking produces, so the explorer clicks
    regardless. It lets the walk fire structural, shallow-destination links first
    (peel the site outward in priority order) and lets the map name a link's target
    even when the budget stops the run before it is clicked. None when the driver
    reports no destination, which every non-link element and every URL-less fake keep.

    `input_type` is the DOM `type` of the backing `<input>` element (e.g. `"password"`,
    `"email"`, `"text"`) when the driver enriched the node with one — a scaffold
    generator's only signal for telling a login field apart from any other text box,
    since the accessibility tree alone reports both as `role="textbox"`. None for every
    non-`<input>` element and every fake that supplies none.

    `fill_value` marks this element as a *typed* transition rather than a clicked one
    (§2e, issue #137): when set, it is the value an interactive-round scaffold typed
    into this field to reach the transition's destination state, and a replayer must
    call `driver.fill(action, action.fill_value)` for this hop, never `driver.perform`
    (which clicks). None for every element discovery itself ever produces — only
    `spoor/scaffold/apply.py` constructs one with this set, when it records what a
    scaffold's fill revealed as a real, replayable graph edge.
    """

    role: str
    name: str
    backend_node_id: int | None
    destination: str | None = None
    input_type: str | None = None
    fill_value: str | None = None


def _ax_string(field: object) -> str:
    """Read a CDP AX value object (`{"value": ...}`) as a string, tolerantly."""
    if isinstance(field, Mapping):
        value = field.get("value", "")
        return str(value) if value is not None else ""
    return "" if field is None else str(field)


def _backend_node_id(node: Mapping[str, object]) -> int | None:
    raw = node.get("backendDOMNodeId")
    return raw if isinstance(raw, int) else None


def _destination(node: Mapping[str, object]) -> str | None:
    """The element's destination hint, if the driver enriched the node with one (9b).

    A plain string on the node under `destination` (the live driver injects the URL
    path of a link's `href`; a fake supplies it directly). Absent, empty, or non-string
    yields None — the pre-slice-9b shape every URL-less driver keeps.
    """
    raw = node.get("destination")
    return raw if isinstance(raw, str) and raw else None


def _input_type(node: Mapping[str, object]) -> str | None:
    """The element's DOM `type`, if the driver enriched the node with one.

    A plain string on the node under `input_type` (the live driver injects an
    `<input>` element's `type` attribute; a fake supplies it directly). Absent, empty,
    or non-string yields None — the pre-enrichment shape every such driver keeps.
    """
    raw = node.get("input_type")
    return raw if isinstance(raw, str) and raw else None


# A node whose accessibility-tree ancestor is one of these is inside a native
# <video>/<audio> element's closed user-agent shadow tree (play/mute/volume/
# scrubber/fullscreen/the overflow menu) — browser chrome for the media tag, not
# site-authored content, and never reliably actionable regardless (see
# `_has_media_ancestor`). Chromium reports these internal roles capitalized,
# unlike the lowercase ARIA roles every site-authored element carries; matched
# case-insensitively since that capitalization is an implementation detail, not
# a contract.
_MEDIA_ROLES = frozenset({"video", "audio"})


def _has_media_ancestor(
    node: Mapping[str, object], by_node_id: Mapping[object, Mapping[str, object]]
) -> bool:
    """Whether `node` descends from a `<video>`/`<audio>` element's AX node (§2e).

    Native media controls live in the browser's own *closed* user-agent shadow
    DOM. `document.elementFromPoint` always retargets a hit anywhere inside that
    shadow tree back to the `<video>`/`<audio>` host itself — verified directly
    against a real Chromium build, not assumed — so the actuation-verification
    step every other discovered element relies on (§2e 7a: the click lands on the
    element the same accessibility read resolved, confirmed live before it fires)
    can never succeed for one. That is a structural fact of the shadow boundary,
    true on every site with a plain `<video controls>`/`<audio controls>`
    element (§0), not a timing or visibility issue — so rather than discover
    something that would always fail its own verification (and cost three
    wasted replay attempts doing it), these are excluded here, from the same
    accessibility-tree read discovery already has: no extra CDP round-trip, and
    no change to how any other element is verified.

    Walks the node's own `parentId` chain (cycle-guarded, since a malformed or
    fake node list is not this function's contract to enforce); a node missing
    `parentId`/`nodeId` — any discovery input that predates this check, and every
    existing fake in the test suite — simply never matches an ancestor, the same
    "include it" default `discover_actions` already takes for any other missing
    field.
    """
    seen: set[int] = set()
    current: Mapping[str, object] | None = by_node_id.get(node.get("parentId"))
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if _ax_string(current.get("role")).lower() in _MEDIA_ROLES:
            return True
        current = by_node_id.get(current.get("parentId"))
    return False


def discover_actions(
    ax_nodes: Sequence[Mapping[str, object]],
) -> list[ActionableElement]:
    """Discover the actionable elements in an accessibility-tree node list (§2e).

    Keeps document order and every interactive occurrence — the explorer decides
    later what to do with each; deduplication is not this slice's job. Ignored
    nodes, non-interactive roles, and native `<video>`/`<audio>` control children
    (`_has_media_ancestor` — never actionable regardless, see its docstring) are
    dropped. Tolerant of missing fields: a node with no name yields an empty
    label, a node with no backend id yields None.
    """
    by_node_id = {node.get("nodeId"): node for node in ax_nodes}
    discovered: list[ActionableElement] = []
    for node in ax_nodes:
        if node.get("ignored") is True:
            continue
        role = _ax_string(node.get("role"))
        if role not in ACTIONABLE_ROLES:
            continue
        if _has_media_ancestor(node, by_node_id):
            continue
        discovered.append(
            ActionableElement(
                role=role,
                name=_ax_string(node.get("name")),
                backend_node_id=_backend_node_id(node),
                destination=_destination(node),
                input_type=_input_type(node),
            )
        )
    return discovered
