# Exploration element discovery: what can be interacted with — ROADMAP.md §2e.
#
# The third slice of exploration mode (§2e), still pure logic. Reuses the §2c
# accessibility-tree signal rather than inventing a new mechanism: that snapshot
# already labels every node with a generic ARIA role (button/link/textbox/…), so
# discovering "what can the explorer act on here" is filtering that node list to the
# interactive roles and reading each one's accessible name. No site knowledge (§0):
# the same role set for every target.
#
# The accessible name doubles as the label the safety gate (slice 1) classifies, and
# the backend DOM node id is kept so the (later) explorer loop can locate the element
# to act on it. This slice only *discovers*; driving the actions is the explorer loop.

Feature: Exploration discovers the actionable elements on a page
  As the explorer that must decide what to try next on a screen
  I want the interactive elements pulled from the accessibility tree
  So that every actionable role is a candidate action, labelled and locatable

  Scenario: Only interactive, non-ignored roles become actionable elements
    Given an accessibility tree:
      | role    | name        | ignored |
      | button  | Add to cart | false   |
      | link    | Home        | false   |
      | textbox | Search      | false   |
      | heading | Welcome     | false   |
      | text    | lorem ipsum | false   |
      | img     | logo        | false   |
      | button  | Hidden      | true    |
    When I discover the actionable elements
    Then the discovered elements are:
      | role    | name        |
      | button  | Add to cart |
      | link    | Home        |
      | textbox | Search      |

  Scenario: A discovered element preserves its accessible name and DOM handle
    Given an accessibility tree:
      | role   | name           | ignored | backend_node_id |
      | button | Confirm order  | false   | 42              |
    When I discover the actionable elements
    Then the first discovered element has role "button" and name "Confirm order"
    And the first discovered element keeps backend node id 42

  Scenario: An unnamed interactive element is still discovered
    # An icon-only button exposes an empty accessible name; it is still a candidate
    # action (the explorer can still click it), just with no label.
    Given an accessibility tree:
      | role   | name | ignored |
      | button |      | false   |
    When I discover the actionable elements
    Then the first discovered element has role "button" and name ""

  Scenario: A link's destination hint is read from its enriched node
    # When the driver enriches a node with a destination (a link's href path, §2e
    # slice 9b), discovery carries it as a hint; an element with none carries None.
    Given an accessibility tree:
      | role   | name       | ignored | destination |
      | link   | Art        | false   | /9-art      |
      | button | Add to cart| false   |             |
    When I discover the actionable elements
    Then the first discovered element has destination "/9-art"
    And the second discovered element has no destination

  Scenario: A text field's DOM input type is read from its enriched node
    # When the driver enriches a node with an input_type (an <input> element's DOM
    # `type` attribute), discovery carries it — the only signal that tells a login
    # field (type="password") apart from any other text box, since both report the
    # same accessibility role. An element with none carries None.
    Given an accessibility tree:
      | role    | name     | ignored | input_type |
      | textbox | Password | false   | password   |
      | textbox | Search   | false   |            |
    When I discover the actionable elements
    Then the first discovered element has input type "password"
    And the second discovered element has no input type

  Scenario: A native video/audio control child is never discovered
    # Native <video controls>/<audio controls> elements (play, mute, volume, the
    # scrubber, fullscreen, the overflow menu) live in the browser's own *closed*
    # shadow DOM -- a real Chromium build confirms elementFromPoint always
    # retargets a hit inside it back to the <video>/<audio> host, so the live
    # click-verification every other element passes through (§2e 7a) can never
    # succeed for one. A structural fact of the browser, true on every site with a
    # plain media element (§0), not a timing or visibility issue -- so discovery
    # excludes them, walking only the ancestor chain the same accessibility read
    # already carries (no extra CDP round-trip).
    Given an accessibility tree:
      | node_id | parent_id | role   | name        | ignored |
      | 1       |           | Video  |             | false   |
      | 2       | 1         | button | play        | false   |
      | 3       | 1         | slider | volume      | false   |
      | 4       |           | button | Add to cart | false   |
    When I discover the actionable elements
    Then the discovered elements are:
      | role   | name        |
      | button | Add to cart |

  Scenario: An ordinary wrapped element is still discovered
    # A non-media ancestor (a plain wrapping <div>) must not trip the exclusion --
    # only an actual <video>/<audio> ancestor does.
    Given an accessibility tree:
      | node_id | parent_id | role    | name   | ignored |
      | 1       |           | generic |        | false   |
      | 2       | 1         | button  | Submit | false   |
    When I discover the actionable elements
    Then the discovered elements are:
      | role   | name   |
      | button | Submit |

  Scenario: A malformed cyclic ancestor chain does not hang discovery
    # A node whose parentId chain cycles back on itself (never true of a real
    # CDP tree, but not this function's contract to assume) must not hang --
    # the walk gives up rather than loop, and the element is still discovered.
    Given an accessibility tree:
      | node_id | parent_id | role   | name   | ignored |
      | 1       | 2         | generic|        | false   |
      | 2       | 1         | generic|        | false   |
      | 3       | 1         | button | Submit | false   |
    When I discover the actionable elements
    Then the discovered elements are:
      | role   | name   |
      | button | Submit |

  Scenario: A page with no interactive roles yields no actions
    Given an accessibility tree:
      | role      | name    | ignored |
      | heading   | Welcome | false   |
      | paragraph | body    | false   |
    When I discover the actionable elements
    Then no actionable elements are discovered
