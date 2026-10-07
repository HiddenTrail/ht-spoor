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
      nav { display: flex; flex-wrap: wrap; gap: 4px 18px; align-items: baseline; }
      nav a { color: var(--text); text-decoration: none; }
      nav a:hover { color: var(--accent); }
      nav .brand { font-weight: 700; margin-right: 8px; }
      fieldset {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 12px 16px 16px; margin: 0 0 16px;
      }
      legend { font-weight: 600; padding: 0 6px; }
      label { display: block; margin: 10px 0 4px; font-weight: 500; }
      label.check { display: flex; gap: 8px; align-items: baseline; font-weight: 500; }
      .hint { color: var(--muted); font-size: 0.85rem; margin: 2px 0 0; }
      input[type=text], input[type=number], select, textarea {
        width: 100%; padding: 7px 9px; font: inherit; color: var(--text);
        background: var(--bg); border: 1px solid var(--border); border-radius: 6px;
      }
      textarea { min-height: 70px; font-family: ui-monospace, Consolas, monospace; }
      .grid {
        display: grid; gap: 0 16px;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      }
      .indent { margin-left: 26px; }
      .spaced { margin-top: 12px; }
      button {
        font: inherit; padding: 8px 16px; border-radius: 6px; cursor: pointer;
        border: 1px solid var(--accent); background: var(--accent); color: var(--bg);
      }
      button.secondary { background: transparent; color: var(--accent); }
      form.inline { display: inline; }
      .error {
        background: var(--warn-bg); color: var(--warn); border-radius: 8px;
        padding: 10px 14px; margin-bottom: 16px;
      }
      .status { font-weight: 600; }
      .status-running { color: var(--accent); }
      .status-failed { color: var(--warn); }
      pre.log {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 8px; padding: 10px 12px; max-height: 60vh; overflow: auto;
      }
      code.cmd { display: block; white-space: pre-wrap; overflow-wrap: anywhere;
        font: 13px/1.45 ui-monospace, Consolas, monospace; }
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
    <header>
      <nav>
        <a class="brand" href="/">Spoor</a>
        <a href="/">Maps</a>
        <a href="/new/explore">Explore</a>
        <a href="/new/run">Extract</a>
        <a href="/new/apply-scaffold">Apply scaffold</a>
        <a href="/jobs">Jobs</a>
      </nav>
    </header>
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
  resolved by tier {{ view.tier }}{% endif %} ·
  <a href="{{ explore_href }}">Explore this page again</a>
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
{% if error %}<div class="error">{{ error }}</div>{% endif %}
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
    {{ m.number("max_depth", "Max depth (clicks from the start)", v) }}
  </div>
</fieldset>
<fieldset>
  <legend>Login and resuming</legend>
  {{ m.text("session", "Saved login (optional)", v,
    "The name of a login saved with Spoor's sessions, or the path of a "
    ~ "storage-state file you captured. Spoor never logs in on its own.") }}
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
{% if error %}<div class="error">{{ error }}</div>{% endif %}
<form id="job-form" method="post" action="/new/run">
<fieldset>
  <legend>Config</legend>
  {{ m.text("config", "Config file", v, placeholder="configs/shop.yaml") }}
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
{% if error %}<div class="error">{{ error }}</div>{% endif %}
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
    "Only needed if the fields are behind a login.") }}
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
<div class="card scroll">
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
<div class="card scroll">
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
}


def environment() -> Environment:
    """A Jinja2 environment with autoescape on for every template (§2h defence)."""
    return Environment(
        loader=DictLoader(_TEMPLATES),
        autoescape=select_autoescape(default=True, default_for_string=True),
        trim_blocks=True,
        lstrip_blocks=True,
    )
