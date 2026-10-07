"""Page templates for the local GUI (ROADMAP.md §2i).

Inline Jinja2 templates in a `DictLoader`, the same approach the §2e wiki takes
(`spoor/exploration/wiki.py`): no package data files to ship, and autoescape is
on for every template, so a captured value can never inject markup into the page.
Everything shown is already §2h-redacted by `views.map_view` before it gets here.
"""

from __future__ import annotations

from jinja2 import DictLoader, Environment, select_autoescape

_LAYOUT = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}Spoor{% endblock %}</title>
    <style>
      :root {
        --bg: #f7f6f3; --surface: #ffffff; --text: #1f1c1b; --muted: #6b6560;
        --border: #e2ded8; --accent: #2f6f5e; --warn-bg: #fdf3e2; --warn: #8a5a00;
      }
      @media (prefers-color-scheme: dark) {
        :root {
          --bg: #1f1c1b; --surface: #2a2724; --text: #eeeae4; --muted: #a59e96;
          --border: #3d3934; --accent: #7cc4ad; --warn-bg: #3a2f1c; --warn: #f0c070;
        }
      }
      * { box-sizing: border-box; }
      body {
        margin: 0; background: var(--bg); color: var(--text);
        font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif;
      }
      header {
        background: var(--surface); border-bottom: 1px solid var(--border);
        padding: 12px 16px;
      }
      header a { color: var(--text); font-weight: 600; text-decoration: none; }
      main { max-width: 1100px; margin: 0 auto; padding: 20px 16px 48px; }
      a { color: var(--accent); }
      h1 { font-size: 1.4rem; margin: 0 0 4px; overflow-wrap: anywhere; }
      h2 { font-size: 1.1rem; margin: 28px 0 8px; }
      .muted { color: var(--muted); }
      .crumbs { font-size: 0.9rem; margin-bottom: 12px; }
      .card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 12px 16px;
      }
      .scroll { overflow-x: auto; }
      table { border-collapse: collapse; width: 100%; }
      th, td {
        text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--border);
        vertical-align: top; overflow-wrap: anywhere;
      }
      th { font-weight: 600; color: var(--muted); font-size: 0.85rem; }
      ul.plain { list-style: none; padding: 0; margin: 0; }
      ul.plain li { padding: 6px 0; border-bottom: 1px solid var(--border); }
      ul.plain li:last-child { border-bottom: 0; }
      pre {
        margin: 0; white-space: pre-wrap; overflow-wrap: anywhere;
        font: 13px/1.45 ui-monospace, Consolas, monospace;
      }
      .skip { background: var(--warn-bg); color: var(--warn); }
    </style>
  </head>
  <body>
    <header><a href="/">Spoor</a></header>
    <main>{% block body %}{% endblock %}</main>
  </body>
</html>
"""

_HOME = """{% extends "layout.html" %}
{% block body %}
<h1>Mapped sites</h1>
{% if domains %}
<p class="muted">Pick a site to see the pages Spoor has mapped on it.</p>
<div class="card">
  <ul class="plain">
  {% for d in domains %}
    <li><a href="{{ d.href }}">{{ d.name }}</a></li>
  {% endfor %}
  </ul>
</div>
{% else %}
<div class="card">
  <p>Nothing has been mapped yet.</p>
  <p class="muted">Once you run an exploration or an extraction, the sites it
  mapped show up here.</p>
</div>
{% endif %}
{% endblock %}
"""

_DOMAIN = """{% extends "layout.html" %}
{% block title %}{{ domain }} · Spoor{% endblock %}
{% block body %}
<div class="crumbs"><a href="/">Mapped sites</a> /</div>
<h1>{{ domain }}</h1>
{% if urls %}
<div class="card scroll">
  <table>
    <thead><tr><th>Page</th><th>Last captured</th></tr></thead>
    <tbody>
    {% for u in urls %}
      <tr>
        <td><a href="{{ u.href }}">{{ u.url }}</a></td>
        <td title="{{ u.captured_at }}">{{ u.age }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<div class="card"><p>No pages have been mapped on this site.</p></div>
{% endif %}
{% endblock %}
"""

_MAP = """{% extends "layout.html" %}
{% block title %}{{ view.url }} · Spoor{% endblock %}
{% block body %}
<div class="crumbs">
  <a href="/">Mapped sites</a> / <a href="{{ domain_href }}">{{ view.domain }}</a> /
</div>
<h1>{{ view.url }}</h1>
<p class="muted">
  Captured {{ view.captured_at }} ({{ age }}){% if view.tier %} ·
  resolved by tier {{ view.tier }}{% endif %}
</p>

<h2>Records</h2>
{% if rows %}
<div class="card scroll">
  <table>
    <thead><tr>{% for c in columns %}<th>{{ c }}</th>{% endfor %}</tr></thead>
    <tbody>
    {% for row in rows %}
      <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<p class="muted">No records were extracted for this page.</p>
{% endif %}

{% if api_surface %}
<h2>Observed API</h2>
<div class="card scroll"><pre>{{ api_surface }}</pre></div>
{% endif %}

{% if exploration %}
{% set counts = exploration.counts or {} %}
<h2>Exploration</h2>
<p class="muted">
  {{ counts.states or 0 }} screens, {{ counts.transitions or 0 }} actions fired,
  {{ counts.skipped or 0 }} skipped by the safety check.
</p>

<h2>Screens</h2>
<div class="card scroll">
  <table>
    <thead><tr><th>Screen</th><th>Actions found</th></tr></thead>
    <tbody>
    {% for s in exploration.states or [] %}
      <tr>
        <td>{{ s.id }}</td>
        <td>
          {%- for a in s.actions or [] -%}
          {{ a.role }} “{{ a.name }}”{{ ", " if not loop.last }}
          {%- endfor -%}
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>

<h2>Actions fired</h2>
{% if exploration.transitions %}
<div class="card scroll">
  <table>
    <thead><tr><th>From</th><th>Action</th><th>To</th><th>What changed</th></tr></thead>
    <tbody>
    {% for t in exploration.transitions %}
      <tr>
        <td>{{ t["from"] }}</td>
        <td>{{ t.action.role }} “{{ t.action.name }}”</td>
        <td>{{ t.to }}</td>
        <td><pre>{{ to_json(t.changed) }}</pre></td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<p class="muted">No actions were fired.</p>
{% endif %}

{% if exploration.skipped %}
<h2>Skipped by the safety check</h2>
<div class="card scroll">
  <table>
    <thead><tr><th>On screen</th><th>Action</th><th>Why it was skipped</th></tr></thead>
    <tbody>
    {% for s in exploration.skipped %}
      <tr class="skip">
        <td>{{ s["from"] }}</td>
        <td>{{ s.action.role }} “{{ s.action.name }}”</td>
        <td>{{ s.reason }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% endif %}
{% endif %}
{% endblock %}
"""

_NOT_MAPPED = """{% extends "layout.html" %}
{% block title %}Not mapped · Spoor{% endblock %}
{% block body %}
<div class="crumbs"><a href="/">Mapped sites</a> /</div>
<h1>{{ url }}</h1>
<div class="card"><p>This page has not been mapped yet.</p></div>
{% endblock %}
"""

_TEMPLATES = {
    "layout.html": _LAYOUT,
    "home.html": _HOME,
    "domain.html": _DOMAIN,
    "map.html": _MAP,
    "not_mapped.html": _NOT_MAPPED,
}


def environment() -> Environment:
    """A Jinja2 environment with autoescape on for every template (§2h defence)."""
    return Environment(
        loader=DictLoader(_TEMPLATES),
        autoescape=select_autoescape(default=True, default_for_string=True),
        trim_blocks=True,
        lstrip_blocks=True,
    )
