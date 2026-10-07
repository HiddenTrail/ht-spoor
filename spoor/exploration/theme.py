"""Spoor's shared HTML stylesheet: the exploration wiki's theme, reused by the GUI.

One dark, token-driven theme (CSS custom properties for background, surface,
border, text and accent colours) for every HTML surface Spoor renders: the §2e
wiki (`wiki.py`, where it was designed; see the slice 6h/6i notes there) and the
§2i local GUI (`spoor/gui/templates.py`, which adds only its own form and job
rules on top). Kept in one string so the two can't drift apart: change a token
here and both surfaces follow.

Generic to Spoor's own output (§0): no target branding, and only system fonts,
so nothing fails to load for a reader without them installed.
"""

STYLESHEET = """
      :root {
        --bg: #1f1c1b;
        --surface: #2a2724;
        --surface-2: #322e2b;
        --surface-3: #3a3531;
        --border: #3d3835;
        --border-hover: #5a5550;
        --text: #f0ece8;
        --text-muted: #aaa39d;
        --accent: #f85840;
        --teal: #208e98;
        --yellow: #d8fd1b;
        --radius: 8px;
        --radius-sm: 5px;
        --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono",
          monospace;
      }
      * { box-sizing: border-box; }
      html { scroll-behavior: smooth; }
      body {
        background: var(--bg);
        color: var(--text);
        font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        line-height: 1.6;
        margin: 0 auto;
        max-width: 64rem;
        padding: 0 1.5rem 4rem;
      }
      h1, h2, h3 { font-weight: 700; letter-spacing: 0; line-height: 1.25; }
      h1 {
        color: var(--accent);
        font-size: 2rem;
        margin: 0 0 0.6rem;
        word-break: break-word;
      }
      h2 {
        border-bottom: 1px solid var(--border);
        color: var(--teal);
        font-size: 1.2rem;
        margin: 2.5rem 0 1rem;
        padding-bottom: 0.4rem;
      }
      h3 { color: var(--text); font-size: 0.95rem; margin: 1.25rem 0 0.5rem; }
      p { margin: 0 0 1rem; }
      a { color: var(--accent); text-decoration: none; }
      a:hover { color: var(--yellow); text-decoration: underline; }
      ul, dl { margin: 0; padding-left: 0; }
      ul { list-style: none; }

      /* Sticky top nav: a quiet, always-reachable way back to the overview or
         help page, never competing with a page's own content for attention. */
      nav {
        align-items: center;
        background: linear-gradient(var(--bg) 85%, transparent);
        border-bottom: 1px solid var(--border);
        display: flex;
        flex-wrap: wrap;
        font-size: 0.9rem;
        gap: 0.4rem 1.25rem;
        margin: 0 -1.5rem 2rem;
        padding: 1.1rem 1.5rem 1rem;
        position: sticky;
        top: 0;
        z-index: 10;
      }
      nav a { color: var(--text-muted); font-weight: 600; }
      nav a:hover { color: var(--accent); text-decoration: none; }
      nav span { color: var(--text-muted); }
      main { display: block; }

      /* Index-page summary: three counts as scannable tiles instead of a bare
         bullet list, the first thing a reader's eye should land on. */
      .stats {
        display: grid;
        gap: 0.75rem;
        grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
        margin: 0 0 1.5rem;
      }
      .stat {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.9rem 1.1rem;
      }
      .stat strong {
        color: var(--accent);
        display: block;
        font-size: 1.6rem;
        line-height: 1.2;
      }

      /* Plain index lists read as a quiet rail of rows, not a wall of
         underlined links — each row gets room and a hover affordance. */
      .index-list li {
        border-bottom: 1px solid var(--border);
        padding: 0.6rem 0.1rem;
      }
      .index-list li:last-child { border-bottom: none; }
      .index-list a { color: var(--text); font-weight: 600; }
      .index-list a:hover { color: var(--accent); }

      .table-wrap {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin: 0 0 1rem;
        overflow-x: auto;
      }
      table {
        background: var(--surface);
        border-collapse: collapse;
        width: 100%;
      }
      th, td {
        border-bottom: 1px solid var(--border);
        padding: 0.6rem 0.85rem;
        text-align: left;
        vertical-align: middle;
      }
      tr:last-child td { border-bottom: none; }
      tbody tr:hover td { background: var(--surface-2); }
      th {
        background: var(--surface-2);
        color: var(--text-muted);
        font-size: 0.74em;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        white-space: nowrap;
      }
      /* A table cell's <em> reads as a quiet status pill (a type name, or a
         "none" placeholder) rather than plain italics — scoped to table cells
         only, so prose emphasis elsewhere is untouched. */
      td em {
        background: var(--surface-3);
        border-radius: 999px;
        color: var(--text-muted);
        font-size: 0.8em;
        font-style: normal;
        padding: 0.15rem 0.6rem;
        white-space: nowrap;
      }
      code {
        background: var(--surface-2);
        border-radius: 4px;
        color: var(--yellow);
        font-family: var(--mono);
        font-size: 0.9em;
        padding: 0.1rem 0.4rem;
      }
      pre.mermaid {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow-x: auto;
        padding: 1.25rem;
      }
      .count { color: var(--text-muted); font-size: 0.85em; }
      .screenshot {
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        height: auto;
        max-width: 100%;
        transition: border-color 0.15s ease, transform 0.15s ease;
      }
      .screenshot:hover { border-color: var(--border-hover); }
      .screenshot-crop { max-width: none; }
      /* A full-size state screenshot (outside a table) gets room to breathe and
         a lift on hover; a thumbnail inside a table row stays row-sized. */
      td .screenshot { max-height: 7rem; width: auto; }
      h2 + .screenshot, h2 + p + .screenshot {
        box-shadow: 0 4px 24px rgb(0 0 0 / 0.35);
        display: block;
        max-width: 42rem;
      }
      h2 + .screenshot:hover, h2 + p + .screenshot:hover {
        transform: translateY(-2px);
      }

      /* Settle warnings and interactive-round notices read as alert banners,
         not plain paragraphs, so they're not mistaken for ordinary prose. */
      .notice {
        background: var(--surface);
        border-left: 3px solid var(--yellow);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
        padding: 0.75rem 1rem;
      }
      .notice.notice-info { border-left-color: var(--teal); }

      /* Help-page glossary: each term/definition pair as a small card, instead
         of a long run of <dt>/<dd> pairs with no visual separation. */
      dl { display: flex; flex-direction: column; }
      dl + h2 { margin-top: 2.5rem; }
      dt {
        color: var(--accent);
        font-weight: 700;
        padding: 0.9rem 0 0.1rem;
      }
      dd { color: var(--text-muted); margin: 0 0 0.9rem; }

      @media (max-width: 30rem) {
        body { padding: 0 1rem 3rem; }
        nav { margin: 0 -1rem 1.5rem; padding: 1rem 1rem 0.85rem; }
        h1 { font-size: 1.6rem; }
      }
    """
