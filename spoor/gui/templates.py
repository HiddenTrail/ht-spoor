"""Page templates for the local GUI (ROADMAP.md §2i).

Inline Jinja2 templates in a `DictLoader`, the same approach the §2e wiki takes
(`spoor/exploration/wiki.py`): no package data files to ship, and autoescape is
on for every template, so a captured value can never inject markup into the page.
Everything shown is already §2h-redacted by `views.map_view` before it gets here.

The look is the wiki's own: the layout embeds Spoor's shared stylesheet
(`spoor/exploration/theme.py`) and adds only GUI-specific rules (forms, buttons,
job status, the log) built from the same colour tokens, so the GUI and a wiki it
links to read as one product.
"""

from __future__ import annotations

import base64
from importlib.resources import files

from jinja2 import DictLoader, Environment, select_autoescape

from spoor.exploration.theme import (
    STYLESHEET,
    THEME_SCRIPT,
    TOGGLE_BUTTON,
    TOGGLE_CSS,
)

_GUI_CSS = """
      /* GUI-only rules, layered on Spoor's shared stylesheet (the wiki's theme,
         spoor/exploration/theme.py) and built from the same tokens, so the GUI
         and the wiki read as one product. */
      nav .brand {
        align-items: center;
        color: var(--accent);
        display: inline-flex;
        font-weight: 700;
        gap: 0.45rem;
      }
      nav .brand img { height: 1.6rem; width: auto; }
      /* Night: the orange hexagon; day: the black hexagon, which needs a light
         background to show its shape. */
      .logo-night { display: var(--night-only); }
      .logo-day { display: var(--day-only); }
      .muted { color: var(--text-muted); }
      .crumbs { color: var(--text-muted); font-size: 0.9rem; margin: 0 0 0.4rem; }
      .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin: 0 0 1rem;
        padding: 0.9rem 1.1rem;
      }
      .card p:last-child { margin-bottom: 0; }
      /* Only code and paths may break mid-word: letting every cell do so lets a
         table squeeze short columns until words split ("Wik / i"). */
      td { overflow-wrap: break-word; }
      td code, td pre { overflow-wrap: anywhere; }
      ul.changes { font-size: 0.9em; }
      pre {
        font-family: var(--mono);
        font-size: 0.85rem;
        line-height: 1.45;
        margin: 0;
        overflow-wrap: anywhere;
        white-space: pre-wrap;
      }
      tr.skip td:first-child { box-shadow: inset 3px 0 var(--yellow); }
      .notice { margin: 0 0 1rem; }
      .notice.notice-error { border-left-color: var(--accent); }

      /* Forms */
      fieldset {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin: 0 0 1rem;
        padding: 0.6rem 1.1rem 1.1rem;
      }
      legend { color: var(--teal); font-weight: 700; padding: 0 0.4rem; }
      label { display: block; font-weight: 600; margin: 0.8rem 0 0.3rem; }
      label.check {
        align-items: baseline;
        display: flex;
        font-weight: 600;
        gap: 0.5rem;
      }
      label.check input { accent-color: var(--accent); }
      .hint { color: var(--text-muted); font-size: 0.85rem; margin: 0.2rem 0 0; }
      input[type=text], select, textarea {
        background: var(--surface-2);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        color: var(--text);
        font: inherit;
        padding: 0.45rem 0.6rem;
        width: 100%;
      }
      input[type=text]:focus, select:focus, textarea:focus {
        border-color: var(--accent);
        outline: none;
      }
      textarea { font-family: var(--mono); min-height: 4.5rem; }
      textarea.editor { line-height: 1.5; margin: 0 0 0.5rem; min-height: 26rem; }
      input[type=file] { color: var(--text-muted); }
      .notice ul { margin: 0.4rem 0 0; }
      .notice pre { margin: 0; }
      .grid {
        display: grid;
        gap: 0 1rem;
        grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
      }
      .indent { margin-left: 1.6rem; }
      .spaced { margin-top: 0.8rem; }
      button {
        background: var(--accent);
        border: 1px solid var(--accent);
        border-radius: var(--radius-sm);
        color: var(--bg);
        cursor: pointer;
        font: inherit;
        font-weight: 700;
        padding: 0.45rem 1.1rem;
      }
      button:hover { background: var(--yellow); border-color: var(--yellow); }
      button.secondary { background: transparent; color: var(--accent); }
      button.secondary:hover { color: var(--yellow); }
      form.inline { display: inline; }

      /* Jobs */
      code.cmd {
        background: var(--surface-2);
        display: block;
        overflow-wrap: anywhere;
        padding: 0.6rem 0.8rem;
        white-space: pre-wrap;
      }
      .status { font-weight: 700; }
      .status-running { color: var(--teal); }
      .status-failed { color: var(--accent); }
      .status-stopped { color: var(--yellow); }
      pre.log {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        max-height: 60vh;
        overflow: auto;
        padding: 0.8rem 1rem;
      }
"""

_LAYOUT = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% block title %}Spoor{% endblock %}</title>
    <link rel="icon" type="image/svg+xml" href="{{ logo }}" />
    {% block head %}{% endblock %}
    <style>""" + STYLESHEET + TOGGLE_CSS + _GUI_CSS + """    </style>
    """ + THEME_SCRIPT + """
  </head>
  <body>
    <nav>
      <a class="brand" href="/">
        <img class="logo-night" src="{{ logo }}" alt="" />
        <img class="logo-day" src="{{ logo_day }}" alt="" />Spoor</a>
      <a href="/">Maps</a>
      <a href="/new/explore">Explore</a>
      <a href="/new/run">Extract</a>
      <a href="/new/apply-scaffold">Apply scaffold</a>
      <a href="/jobs">Jobs</a>
      <a href="/logins">Logins</a>
      <a href="/configs">Configs</a>
      <a href="/servers">Servers</a>
      """ + TOGGLE_BUTTON + """
    </nav>
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
  <ul class="index-list">
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
<div class="table-wrap">
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
  resolved by tier {{ view.tier }}{% endif %} ·
  <a href="{{ explore_href }}">Explore this page again</a>
</p>

<h2>Records</h2>
{% if rows %}
<div class="table-wrap">
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
<div class="card"><pre>{{ api_surface }}</pre></div>
{% endif %}

{% if exploration %}
{% set counts = exploration.counts or {} %}
<h2>Exploration</h2>
<div class="stats">
  <div class="stat"><strong>{{ counts.states or 0 }}</strong> screens</div>
  <div class="stat"><strong>{{ counts.transitions or 0 }}</strong> actions fired</div>
  <div class="stat"><strong>{{ counts.skipped or 0 }}</strong> skipped by the safety
    check</div>
</div>

<h2>Screens</h2>
<div class="table-wrap">
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
<div class="table-wrap">
  <table>
    <thead><tr><th>From</th><th>Action</th><th>To</th><th>What changed</th></tr></thead>
    <tbody>
    {% for t in exploration.transitions %}
      <tr>
        <td>{{ t["from"] }}</td>
        <td>{{ t.action.role }} “{{ t.action.name }}”</td>
        <td>{{ t.to }}</td>
        <td>
          <ul class="changes">
          {% for change in describe_changes(t.changed) %}
            <li>{{ change }}</li>
          {% endfor %}
          </ul>
        </td>
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
<div class="table-wrap">
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

_MACROS = """{% macro text(name, label, v, hint=None, placeholder="", list=None) %}
<label for="{{ name }}">{{ label }}</label>
<input type="text" id="{{ name }}" name="{{ name }}" value="{{ v.get(name, '') }}"
  placeholder="{{ placeholder }}"{% if list %} list="{{ list }}"{% endif %} />
{% if hint %}<p class="hint">{{ hint }}</p>{% endif %}
{% endmacro %}

{% macro number(name, label, v) %}
<div>
<label for="{{ name }}">{{ label }}</label>
<input type="text" inputmode="decimal" id="{{ name }}" name="{{ name }}"
  value="{{ v.get(name, '') }}" placeholder="no limit" />
</div>
{% endmacro %}

{% macro check(name, label, v, hint=None) %}
<label class="check">
  <input type="checkbox" name="{{ name }}"{% if v.get(name) %} checked{% endif %} />
  <span>{{ label }}</span>
</label>
{% if hint %}<p class="hint indent">{{ hint }}</p>{% endif %}
{% endmacro %}

{% macro output(tick, path_name, label, v) %}
{{ check(tick, label, v) }}
<div class="indent">
  <input type="text" name="{{ path_name }}" value="{{ v.get(path_name, '') }}"
    aria-label="{{ label }}: folder" />
</div>
{% endmacro %}

{% macro saved_logins(logins) %}
<datalist id="saved-logins">
{% for login in logins %}
  <option value="{{ login.label }}">{{ login.domain }}</option>
{% endfor %}
</datalist>
{% endmacro %}

{% macro sandbox(v, what) %}
{{ check("sandbox", "This is a sandbox I own (allow destructive actions)", v,
  "Only for a local or test system you own. Spoor then also " ~ what ~
  ". On any real, public site those actions are always skipped, whether or not "
  ~ "you tick this.") }}
{% endmacro %}

{% macro footer(kind) %}
<fieldset>
  <legend>Command</legend>
  <p class="hint">This is the exact command that will run.</p>
  <code class="cmd" id="preview">…</code>
</fieldset>
<button type="submit">Start</button>
<script>
(() => {
  const form = document.getElementById("job-form");
  const preview = document.getElementById("preview");
  let timer = null;
  async function refresh() {
    const body = new URLSearchParams(new FormData(form));
    try {
      const response = await fetch("/preview/{{ kind }}", { method: "POST", body });
      preview.textContent = await response.text();
      preview.classList.toggle("muted", !response.ok);
    } catch (e) {
      preview.textContent = "Preview unavailable.";
    }
  }
  form.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(refresh, 250);
  });
  refresh();
})();
</script>
{% endmacro %}
"""

_FORM_EXPLORE = """{% extends "layout.html" %}
{% import "macros.html" as m %}
{% block title %}{{ title }} · Spoor{% endblock %}
{% block body %}
<h1>{{ title }}</h1>
<p class="muted">Spoor opens the site in a hidden browser, finds everything you can
click on each screen, tries it, and records where it leads.</p>
{% if error %}<div class="notice notice-error">{{ error }}</div>{% endif %}
<form id="job-form" method="post" action="/new/explore">
<fieldset>
  <legend>Site</legend>
  {{ m.text("url", "Start address", v, placeholder="https://example.com/",
    list="mapped-urls") }}
  <datalist id="mapped-urls">
  {% for u in mapped_urls %}<option value="{{ u }}"></option>{% endfor %}
  </datalist>
  {{ m.sandbox(v, "tries actions such as delete, buy or pay") }}
</fieldset>
<fieldset>
  <legend>Limits</legend>
  <p class="hint">Leave empty for no limit. You can also stop a run at any time.</p>
  <div class="grid">
    {{ m.number("max_states", "Max screens", v) }}
    {{ m.number("max_requests", "Max actions", v) }}
    {{ m.number("max_seconds", "Time limit (seconds)", v) }}
    {{ m.number("max_depth", "Max clicks from the start", v) }}
  </div>
</fieldset>
<fieldset>
  <legend>Login and resuming</legend>
  {{ m.text("session", "Saved login (optional)", v,
    "The name of a login saved on the Logins page, or the path of a "
    ~ "storage-state file you captured. Spoor never logs in on its own.",
    list="saved-logins") }}
  {{ m.saved_logins(saved_logins) }}
  {{ m.text("resume_from", "Continue from screen (optional)", v,
    "Continue an earlier exploration of this address instead of starting over: "
    ~ "id: followed by the start of a screen id, as shown on its map.") }}
</fieldset>
<fieldset>
  <legend>What to write</legend>
  {{ m.output("wiki", "wiki_dir", "A browsable wiki", v) }}
  <div class="indent">
  {{ m.check("screenshots", "Include screenshots in the wiki", v,
    "Pictures can show secrets that can't be blanked out the way text is. "
    ~ "Only tick this if you're comfortable sharing the images.") }}
  </div>
  {{ m.output("gen_tests", "gen_tests_dir", "A runnable regression test suite", v) }}
  <div class="indent">
  {{ m.check("assert_no_new_signals", "Also fail a test on unexpected new activity",
    v, "Fails if a later run logs, stores or requests something this run never saw.") }}
  </div>
  {{ m.output("scaffold", "scaffold_dir", "A form-filling scaffold (interactive.yaml)",
    v) }}
</fieldset>
<fieldset>
  <legend>Which elements to try</legend>
  <label for="include_elements">Only try elements whose label matches</label>
  <textarea id="include_elements" name="include_elements"
    placeholder="Add to cart*">{{ v.get("include_elements", "") }}</textarea>
  <label for="exclude_elements">Never try elements whose label matches</label>
  <textarea id="exclude_elements" name="exclude_elements"
    placeholder="*Logout*">{{ v.get("exclude_elements", "") }}</textarea>
  <p class="hint">One pattern per line; * and ? are wildcards. "Never" wins over
  "only". Neither can allow a destructive action outside a sandbox.</p>
</fieldset>
{{ m.footer(kind) }}
</form>
{% endblock %}
"""

_FORM_RUN = """{% extends "layout.html" %}
{% import "macros.html" as m %}
{% block title %}{{ title }} · Spoor{% endblock %}
{% block body %}
<h1>{{ title }}</h1>
<p class="muted">Runs an extraction config against its site and writes the records
it finds.</p>
{% if error %}<div class="notice notice-error">{{ error }}</div>{% endif %}
<form id="job-form" method="post" action="/new/run">
<fieldset>
  <legend>Config</legend>
  {{ m.text("config", "Config file", v, placeholder="configs/shop.yaml",
    hint="Relative to the folder Spoor's GUI was started in. Edit configs on the "
    ~ "Configs page.") }}
</fieldset>
<fieldset>
  <legend>Output</legend>
  {{ m.text("output", "Write records to", v) }}
  <label for="format">Format</label>
  <select id="format" name="format">
  {% for f in formats %}
    <option value="{{ f }}"{% if v.get("format", "") == f %} selected{% endif %}>
      {{- f or "From the file name" -}}</option>
  {% endfor %}
  </select>
  <div class="spaced">
  {{ m.output("healing_report", "healing_report_path",
    "A report of selectors that stopped matching and how they were repaired", v) }}
  </div>
</fieldset>
{{ m.footer(kind) }}
</form>
{% endblock %}
"""

_FORM_APPLY_SCAFFOLD = """{% extends "layout.html" %}
{% import "macros.html" as m %}
{% block title %}{{ title }} · Spoor{% endblock %}
{% block body %}
<h1>{{ title }}</h1>
<p class="muted">Types the values from a filled-in scaffold into their fields on an
explored page. It only types: it never presses Enter or clicks submit.</p>
{% if error %}<div class="notice notice-error">{{ error }}</div>{% endif %}
<form id="job-form" method="post" action="/new/apply-scaffold">
<fieldset>
  <legend>Page and scaffold</legend>
  {{ m.text("url", "Explored address", v, list="mapped-urls") }}
  <datalist id="mapped-urls">
  {% for u in mapped_urls %}<option value="{{ u }}"></option>{% endfor %}
  </datalist>
  {{ m.text("scaffold", "Filled-in scaffold file", v,
    placeholder="spoor-output/.../scaffold/interactive.yaml") }}
  {{ m.sandbox(v, "types into fields") }}
  <p class="hint">Without a sandbox, nothing is typed.</p>
  {{ m.text("session", "Saved login (optional)", v,
    "Only needed if the fields are behind a login.", list="saved-logins") }}
  {{ m.saved_logins(saved_logins) }}
</fieldset>
<fieldset>
  <legend>What to update</legend>
  {{ m.output("wiki", "wiki_dir", "Refresh the wiki in this folder", v) }}
</fieldset>
{{ m.footer(kind) }}
</form>
{% endblock %}
"""

_JOB = """{% extends "layout.html" %}
{% block title %}Job {{ job.id }} · Spoor{% endblock %}
{% block body %}
<div class="crumbs"><a href="/jobs">Jobs</a> /</div>
<h1>{{ job.spec.kind|capitalize }} job</h1>
<div class="card">
  <code class="cmd">{{ job.spec.command_line }}</code>
</div>
<p>
  <span class="status status-{{ job.status }}">{{ job.status|capitalize }}</span>
  {% if job.exit_code is not none %} · exit code {{ job.exit_code }}{% endif %}
  · {{ status_text }}
</p>
{% if job.running %}
<p>
  {% if job.graceful_stop and not job.stop_requested %}
  <form class="inline" method="post" action="/jobs/{{ job.id }}/stop">
    <button type="submit">Stop</button>
  </form>
  {% endif %}
  <form class="inline" method="post" action="/jobs/{{ job.id }}/kill">
    <button type="submit" class="secondary">Force stop</button>
  </form>
</p>
<p class="hint">
  {% if job.graceful_stop %}Stop finishes the current action, then saves what was
  mapped so far and writes the outputs. {% endif %}Force stop ends the run at once;
  nothing more from it is saved.
</p>
{% endif %}

{% if not job.running and (outputs or map_href) %}
<h2>Where the output landed</h2>
<div class="table-wrap">
  <table>
    <tbody>
    {% for o in outputs %}
      <tr>
        <td>{{ o.label|capitalize }}</td>
        <td><code>{{ o.path }}</code>{% if not o.exists %}
          <span class="muted">(not written)</span>{% endif %}</td>
        <td>
          {% if o.browse %}
          <a href="{{ o.browse }}" target="_blank" rel="noopener">Open wiki</a>
          {% endif %}
          {% if o.exists %}
          <form class="inline" method="post"
            action="/jobs/{{ job.id }}/open/{{ o.label|urlencode }}">
            <button type="submit" class="secondary">Open folder</button>
          </form>
          {% endif %}
        </td>
      </tr>
    {% endfor %}
    {% if map_href %}
      <tr>
        <td>Map</td>
        <td colspan="2"><a href="{{ map_href }}">View the map</a></td>
      </tr>
    {% endif %}
    </tbody>
  </table>
</div>
{% endif %}

<h2>Log</h2>
<pre class="log" id="log">{% for line in lines %}{{ line }}
{% endfor %}</pre>
{% if job.running %}
<script>
(() => {
  const log = document.getElementById("log");
  const events = new EventSource("/jobs/{{ job.id }}/events?from={{ next_line }}");
  events.onmessage = (e) => {
    const atBottom = log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
    log.append(e.data + "\\n");
    if (atBottom) log.scrollTop = log.scrollHeight;
  };
  events.addEventListener("done", () => {
    events.close();
    location.reload();
  });
})();
</script>
{% endif %}
{% endblock %}
"""

_JOBS = """{% extends "layout.html" %}
{% block title %}Jobs · Spoor{% endblock %}
{% block body %}
<h1>Jobs</h1>
{% if jobs %}
<div class="table-wrap">
  <table>
    <thead><tr><th>Started</th><th>Command</th><th>Status</th></tr></thead>
    <tbody>
    {% for job in jobs %}
      <tr>
        <td>{{ job.started_at.astimezone().strftime("%H:%M:%S") }}</td>
        <td>
          <a href="/jobs/{{ job.id }}"><code>{{ job.spec.command_line }}</code></a>
        </td>
        <td class="status status-{{ job.status }}">{{ job.status|capitalize }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<div class="card">
  <p>No jobs yet in this session.</p>
  <p class="muted">Start one from <a href="/new/explore">Explore</a>,
  <a href="/new/run">Extract</a> or <a href="/new/apply-scaffold">Apply scaffold</a>.
  Jobs are listed until you close the GUI.</p>
</div>
{% endif %}
{% endblock %}
"""

_LOGINS = """{% extends "layout.html" %}
{% block title %}Logins · Spoor{% endblock %}
{% block body %}
<h1>Saved logins</h1>
<p class="muted">Saved logins let Spoor explore or extract a site as a logged-in
user. Spoor never logs in on its own: you log in once yourself and save the
browser's login state as a file, then add it here under a name.</p>
{% if messages %}
<div class="notice{% if not ok %} notice-error{% else %} notice-info{% endif %}">
  {% for m in messages %}<pre>{{ m }}</pre>{% endfor %}
</div>
{% endif %}

{% if logins %}
<div class="table-wrap">
  <table>
    <thead>
      <tr><th>Site</th><th>Name</th><th>Saved</th><th>Last used</th><th></th></tr>
    </thead>
    <tbody>
    {% for login in logins %}
      <tr>
        <td>{{ login.domain }}</td>
        <td><strong>{{ login.label }}</strong></td>
        <td>{{ login.created_at[:16]|replace("T", " ") }}</td>
        <td>{{ (login.last_used_at or "never")[:16]|replace("T", " ") }}</td>
        <td>
          <form class="inline" method="post" action="/logins/remove"
            onsubmit="return confirm('Remove this saved login?')">
            <input type="hidden" name="site" value="{{ login.domain }}" />
            <input type="hidden" name="label" value="{{ login.label }}" />
            <button type="submit" class="secondary">Remove</button>
          </form>
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<div class="card"><p>No saved logins yet.</p></div>
{% endif %}

<h2>Add a login</h2>
<form method="post" action="/logins/add" enctype="multipart/form-data">
<fieldset>
  <label for="label">Name</label>
  <input type="text" id="label" name="label" value="{{ v.get('label', '') }}"
    placeholder="customer" />
  <p class="hint">What you'll pick in the forms, e.g. "customer" or "admin". Saving
  under a name that already exists for the site replaces it.</p>
  <label for="site">Site</label>
  <input type="text" id="site" name="site" value="{{ v.get('site', '') }}"
    placeholder="shop.example or https://shop.example/" />
  <label for="file">Login file</label>
  <input type="file" id="file" name="file" accept=".json,application/json" />
  <p class="hint">A browser storage-state file (JSON), for example saved with
  Playwright's <code>context.storage_state()</code> after you logged in. Spoor
  checks it, stores it on this computer only, and never shows its contents.</p>
</fieldset>
<button type="submit">Add login</button>
</form>
{% endblock %}
"""

_CONFIGS = """{% extends "layout.html" %}
{% block title %}Configs · Spoor{% endblock %}
{% block body %}
<h1>Configs</h1>
<p class="muted">Extraction configs (<code>.yaml</code> / <code>.yml</code>) in
<code>{{ workdir }}</code>, the folder Spoor's GUI was started in.</p>
{% if error %}<div class="notice notice-error">{{ error }}</div>{% endif %}
{% if configs %}
<div class="table-wrap">
  <table>
    <thead><tr><th>Config</th><th>Status</th></tr></thead>
    <tbody>
    {% for c in configs %}
      <tr>
        <td><a href="/configs/edit?path={{ c.path|urlencode }}">{{ c.path }}</a></td>
        <td>{% if c.problems %}<em>not valid</em>{% else %}valid{% endif %}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
</div>
{% else %}
<div class="card"><p>No configs in this folder yet.</p></div>
{% endif %}

<h2>New config</h2>
<form method="post" action="/configs/new">
<fieldset>
  <label for="path">File name</label>
  <input type="text" id="path" name="path" value="{{ new_path }}"
    placeholder="configs/my-site.yaml" />
  <p class="hint">Starts from an example you then edit.</p>
</fieldset>
<button type="submit">Create</button>
</form>
{% endblock %}
"""

_CONFIG_EDIT = """{% extends "layout.html" %}
{% block title %}{{ path }} · Spoor{% endblock %}
{% block body %}
<div class="crumbs"><a href="/configs">Configs</a> /</div>
<h1>{{ path }}</h1>
{% if problems is not none %}
  {% if problems %}
  <div class="notice notice-error">
    <strong>{% if saved %}Saved, but the config is not valid yet:{% else %}The config
    is not valid:{% endif %}</strong>
    <ul>{% for p in problems %}<li><code>{{ p }}</code></li>{% endfor %}</ul>
  </div>
  {% else %}
  <div class="notice notice-info">
    {% if saved %}Saved. The config is valid.{% else %}The config is valid (not saved
    yet).{% endif %}
    <a href="{{ run_href }}">Run this config</a>
  </div>
  {% endif %}
{% endif %}
<form method="post" action="/configs/save">
  <input type="hidden" name="path" value="{{ path }}" />
  <textarea name="text" class="editor" spellcheck="false"
    aria-label="Config text">{{ text }}</textarea>
  <p class="hint">Shown exactly as saved on disk: Spoor doesn't hide secrets here,
  because hiding them would also remove them from the file when you save.</p>
  <button type="submit" formaction="/configs/check" class="secondary">Check</button>
  <button type="submit">Save</button>
</form>
{% endblock %}
"""

_SERVERS = """{% extends "layout.html" %}
{% block title %}Servers · Spoor{% endblock %}
{% block head %}{% if state == "starting" %}
<meta http-equiv="refresh" content="2" />{% endif %}{% endblock %}
{% block body %}
<h1>Servers</h1>
<p class="muted">Let scripts and AI agents use what Spoor has mapped. Both servers
only read the maps; neither can change anything on a site.</p>

<h2>Map API server</h2>
<p class="muted">A small web API on this computer that answers questions about
mapped pages, for scripts and dashboards.</p>
{% if error %}<div class="notice notice-error">{{ error }}</div>{% endif %}
{% if state == "running" %}
<div class="notice notice-info">
  The map server is running at <a href="{{ url }}/domains" target="_blank"
  rel="noopener">{{ url }}</a>.
  Try <a href="{{ url }}/domains" target="_blank" rel="noopener">{{ url }}/domains</a>.
</div>
{% elif state == "starting" %}
<div class="notice">The map server is starting at {{ url }}…</div>
{% elif state == "failed" %}
<div class="notice notice-error">The map server stopped with an error. Its log
  is below.</div>
{% else %}
<div class="card"><p>The map server is not running.</p></div>
{% endif %}

{% if state in ("running", "starting") %}
<form method="post" action="/servers/stop">
  <button type="submit">Stop the map server</button>
  {% if job %}<a href="/jobs/{{ job.id }}">See its log</a>{% endif %}
</form>
{% else %}
<form method="post" action="/servers/start">
<fieldset>
  <label for="port">Port</label>
  <input type="text" inputmode="numeric" id="port" name="port" value="{{ port }}" />
  <p class="hint">It listens on this computer only (127.0.0.1).</p>
  <label class="check">
    <input type="checkbox" name="recheck" />
    <span>Allow callers to ask for a fresh read of a mapped page</span>
  </label>
  <p class="hint indent">A fresh read re-runs that page's extraction (it reads the
  site again; it never changes anything there). Off by default.</p>
</fieldset>
<button type="submit">Start the map server</button>
</form>
{% endif %}
{% if log %}
<h2>Recent log</h2>
<pre class="log">{% for line in log %}{{ line }}
{% endfor %}</pre>
{% endif %}

<h2>For AI agents (MCP)</h2>
<p class="muted">AI clients such as Claude start Spoor's MCP server themselves, so it
isn't started here. Add this to your client's MCP configuration; it points the
server at the maps this GUI uses, wherever the client starts it.</p>
<div class="card">
  <pre id="mcp-json">{{ mcp_json }}</pre>
</div>
<button type="button" class="secondary" data-copy="mcp-json">Copy</button>
<p class="hint">Or, for Claude Code, run:</p>
<div class="card">
  <pre id="mcp-command">{{ mcp_command }}</pre>
</div>
<button type="button" class="secondary" data-copy="mcp-command">Copy</button>
<p class="hint">To let agents ask for a fresh read of a mapped page, add
<code>--recheck</code> after <code>serve-mcp</code>.</p>
<script>
document.querySelectorAll("button[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const text = document.getElementById(button.dataset.copy).textContent;
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = "Copied";
    } catch (e) {
      button.textContent = "Select the text and copy it";
    }
  });
});
</script>
{% endblock %}
"""

_TEMPLATES = {
    "layout.html": _LAYOUT,
    "home.html": _HOME,
    "domain.html": _DOMAIN,
    "map.html": _MAP,
    "not_mapped.html": _NOT_MAPPED,
    "macros.html": _MACROS,
    "form_explore.html": _FORM_EXPLORE,
    "form_run.html": _FORM_RUN,
    "form_apply_scaffold.html": _FORM_APPLY_SCAFFOLD,
    "job.html": _JOB,
    "jobs.html": _JOBS,
    "logins.html": _LOGINS,
    "configs.html": _CONFIGS,
    "config_edit.html": _CONFIG_EDIT,
    "servers.html": _SERVERS,
}


#: The GUI's copies of the brand logos in docs/assets/ (a test keeps them
#: identical): night mode and the browser tab use the orange hexagon
#: (Spoor_O_B), day mode the black hexagon (Spoor_B_O).
LOGOS = {"night": "spoor-logo-night.svg", "day": "spoor-logo-day.svg"}


def logo_data_uri(variant: str = "night") -> str:
    """One of Spoor's logos as an inline `data:` URI.

    Inlined so every page carries its own logo and favicon with no extra route
    or request. "night" (the orange hexagon) is also the browser-tab icon,
    because it reads on both light and dark tab bars.
    """
    svg = files("spoor.gui").joinpath("assets", LOGOS[variant]).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(svg).decode("ascii")


def environment() -> Environment:
    """A Jinja2 environment with autoescape on for every template (§2h defence)."""
    env = Environment(
        loader=DictLoader(_TEMPLATES),
        autoescape=select_autoescape(default=True, default_for_string=True),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["logo"] = logo_data_uri("night")
    env.globals["logo_day"] = logo_data_uri("day")
    return env
