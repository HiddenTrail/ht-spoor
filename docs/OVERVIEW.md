# Spoor — what it is, what it does, what's gone into it

> A narration/briefing doc for presenting Spoor to colleagues. Skimmable top to
> bottom; each section stands on its own. Paired with a runnable demo in `demo/`
> (see the last section).

---

## In one sentence

**Spoor gives your agents — and your team — a map of the web.** Point it at a site and
it either *extracts structured data* from it or *autonomously explores it* and produces a
browsable wiki of everything the site does: every screen, every action, and the signals
(network, console, storage, screenshots) each one produces.

It is **local-first and deterministic by default**: it runs entirely on your machine, no
API key required, and uses classical techniques (DOM fingerprinting, perceptual hashing,
scored similarity) instead of a model call for its resilience. An LLM is an *optional,
off-by-default* last resort, never in the loop for a routine run.

---

## Why it exists (the gap it fills)

The popular "smart scraping" tools — Crawl4AI, browser-use, Skyvern — are all **LLM-first**:
a model is in the loop for most decisions. That means API cost, latency, non-determinism,
and a hard dependency on a cloud provider (or a heavy local model) for basic runs.

Spoor's niche is the opposite: **local-first, deterministic, reproducible.** The same run
gives the same map. That matters for two audiences it serves deliberately:

- **Internal (Hidden Trail):** feed a mapped product's behavior into agent/LLM workflows,
  and generate test-automation runs from a captured map.
- **Open source:** anyone who wants to scrape a system or turn it into a wiki.

One design rule keeps those from being in tension — **§0: never site-tailored.** Nothing
in the core may hardcode knowledge of one website (no `if domain == …`, no selectors
written against one named site). Everything works on a target it has never seen, using
only what it observes at runtime. HT's own use is just the first, most demanding user of
the exact same generic tool everyone else gets.

**Not an "agent."** Spoor doesn't decide on its own what's "interesting." It records
exactly what it's told to — via config, via signal flags, via an explicit exploration
request. Every "the system flags X" is really "X matches an explicit, user-set rule."

---

## What it does — four things, four commands

| Command | What it does |
|---|---|
| `spoor run <config.yaml>` | **Extract** structured data from a target using a config (selectors, fields, pagination). Outputs JSON / JSONL / CSV, schema-validated. |
| `spoor explore <url>` | **Explore** a site autonomously: map every reachable screen and action into a state-action graph, and (with `--wiki`) render a browsable wiki of it. Optional screenshots and generated tests. |
| `spoor serve` | Serve a captured map over a **read-only HTTP API** — answer questions about what was mapped, trigger new read-only runs. |
| `spoor serve-mcp` | The same, over **MCP**, so an agent can query the map as a tool. Read-only, always. |

### 1. Extraction — the resolution ladder

A scrape config declares what to pull (`fields`, an optional repeating `item`, pagination).
Spoor resolves each target by **escalating through tiers, only as deep as the site needs**:

- **Tier 1** — fast static selectors (`httpx` + `parsel`), no browser.
- **Tier 2** — JS-rendered pages (headless Chromium via Playwright), reusing the *same*
  selectors on the rendered DOM. Handles infinite scroll, client-populated listings.
- **Tier 3** — **self-healing**: when a selector breaks, resolve the element by DOM
  fingerprint + attribute similarity + a perceptual hash of a cropped screenshot — *no
  model call*. Every healed match logs its confidence and the runner-up candidates, so
  "why did it pick this element" is always answerable. A low-confidence match is flagged
  for review, never silently guessed.
- **Tier 3.5 (optional)** — an LLM/VLM fallback for the small residue nothing else
  resolves. Off by default.

A small per-domain cache remembers which tier last worked, so routine runs skip straight
to it. **Reliability is the non-negotiable** — a scraper that sometimes finds the button
is worse than useless — so tier 3 is treated as the highest-priority engineering in the
whole project, held to an honest standard by the test bench (below).

### 2. Exploration — the flagship

`spoor explore` turns the machinery outward. Instead of "pull these fields," it asks
"**what can a user do here, and what happens when they do it?**" It:

1. Loads the page in a real browser and reads the **accessibility tree** to discover every
   actionable element (buttons, links, form controls) — generically, via ARIA roles, not
   site-specific selectors.
2. Fires each permitted action, observes the resulting screen, and records it as a
   **state-action graph**: nodes are distinct screens (deduplicated by a normalized-DOM
   hash so an AJAX app doesn't explode into infinite near-duplicates), edges are actions.
3. Captures a **free-signal bundle** at every step — accessibility node count, console
   messages, storage keys, network requests, and (opt-in) screenshots — and diffs them
   per transition, so the map shows what each action *changed*.
4. Renders it all into a **browsable static wiki** (`--wiki <dir>`): an overview with a
   Mermaid diagram, one page per screen (leading with an Actions table), one page per
   transition (showing the before/after diff), and a help/glossary page.

The map is **honest about its own boundaries**: it reports what was *actually observed or
explored*, never a guaranteed-exhaustive census. And it shows what it *didn't* do — an
action the safety gate refused to fire is recorded as a **skip**, with the reason.

### 3. Serving — read-only, always

A captured map is useful live, not just as files. `spoor serve` / `serve-mcp` expose it to
an API client or an agent: ask what screens exist, what an action does, trigger a fresh
read-only observation run. **It can never expose a tool that causes a state-changing action
on a target** — that's a hard boundary, not a config option.

### 4. Test generation — a map is already a golden master

A captured transition ("from state X, action Y produced signals Z") is 90% of a regression
test. `spoor explore --gen-tests <dir>` exports each transition as a runnable **pytest +
Playwright** test that replays the path, fires the action, and asserts the recorded signals
still appear. Re-running the suite later against the live product is exactly how drift gets
caught. *(This is the piece we're now re-shaping: Spoor will emit a framework-neutral data
contract, and Playwright / Robot Framework / Cypress converters become plugins on top of
it.)*

---

## The safety spine — non-negotiables, not features

These are enforced as hard rules, weakened only by an explicit recorded decision — never by
a config flag or a "just this once":

- **§0 — never site-tailored.** A CI check (`scripts/check_genericity.py`) scans the core
  and fails the build if a hostname or site-specific branch leaks in.
- **Destructive actions are sandbox-only.** During exploration, an action flagged
  destructive/irreversible is fired *only* against a recognized sandbox (`localhost`,
  `127.0.0.1`, or a declared sandbox whose host also checks out as loopback/private —
  a declaration alone is never enough). Against anything else it is always
  skipped and logged. No flag relaxes this.
- **The serving layer is read-only, always.** (Above.)
- **Secret redaction on shared output is on by default.** Bearer tokens, session-cookie
  shapes, API-key formats are redacted before anything reaches the wiki, the API, or a
  generated test. Raw captures stay local-only. A screenshot is *pixels* — which text
  redaction can't scrub — so embedding screenshots in shared output is **opt-in**, off by
  default.
- **Politeness.** `robots.txt` and crawl-delay respected by default. Anti-bot walls are
  *detected and flagged loudly*, never bypassed. Spoor is a technical capability, not a
  grant of permission.

---

## What's actually gone into it (the depth that isn't obvious)

The hard part of a crawler isn't the happy path — it's not being flaky. A large share of
the engineering is **reliability under real, uncooperative sites**, especially in the
exploration engine:

- **Deterministic replay.** Exploration is depth-bounded breadth-first with
  *reset-and-replay* navigation: to revisit a screen it resets the browser and replays the
  path that first reached it. Every replay is **verified** (each step must land on the
  exact screen it first mapped) and **retried** on a transient miss — so one flaky step
  doesn't kill a whole subtree, and a genuine divergence is reported honestly, not hidden.
- **Settling.** Before reading a screen, Spoor waits for it to actually go quiet — DOM
  mutations stopped, network idle, and urgent ARIA live-region announcements cleared —
  rather than a fixed sleep. A page that never settles is *recorded as such*, not silently
  mis-captured. (Each of these was found by diagnosing a specific real SPA — Juice Shop,
  PrestaShop — and fixed generically, never special-cased.)
- **Layer recovery.** When an overlay (cookie banner, modal) covers the target, Spoor
  treats the blocker as its own state and interacts *past* it — safety-gated, bounded by
  progress, and flagged with a reason when it can't.
- **Robust actuation.** It reads and acts on an element through *one* engine end-to-end
  (the CDP accessibility tree), verifying the click point resolves to the intended element
  before clicking — so "found it but clicked the wrong thing" can't happen silently.
- **Screenshot economy.** Comprehensive crawls dedupe identical captures and store an
  element clip as a *crop reference* into its page screenshot, so a deep run doesn't write
  the same picture thousands of times or run out of memory.

**How it's built:** strict **BDD-first** — every capability starts as a plain-language
Gherkin `.feature` describing "done," then step definitions, then implementation, then a
full local gate (lint, types, fast tests, a mutation-test corpus held at ≥95%, the
genericity check) and an adversarial self-review before merge. There's a **test bench** of
deliberately different architectures — OWASP Juice Shop, Sauce Demo, a self-hosted ERP, a
media SPA — whose only job is to prove the *generic* mechanisms hold across shapes. If a
fixture only passes with a special case, that's a bug in the general mechanism, not a
reason to add the case.

---

## The demo (`demo/`)

There are two, and it's worth opening both (see `demo/README.md`):

- **`demo/wiki-prestashop/index.html`** — a **real, live crawl** of the PrestaShop
  archetype (a full PHP/MySQL storefront). 12 real screens (Home, Clothes, Best sellers,
  Login, Registration, Sitemap, …), 18 transitions, real screenshots, and 18 generated
  regression tests. The headline: the crawl embedded **853 element clips**, which the
  deduplicating store collapsed to **27 image files** on disk — the screenshot-economy
  work, visible in a real run rather than described. (No skips here: `127.0.0.1` is
  loopback, recognized as a sandbox, so destructive actions *fired* — the scripted demo
  below is where the safety gate refusing them is on show.)
- **`demo/wiki/index.html`** — a scripted shop, below, staging the safety-gate skips and
  redaction that a live crawl won't reliably produce on demand.

`demo/build_demo_wiki.py` builds a small, realistic e-commerce exploration graph — the
same `ExplorationGraph` a live crawl produces — and renders it through Spoor's **real**
wiki renderer. It's fast, offline, and deterministic, but exercises the production code
path. Rebuild it any time with:

```bash
python demo/build_demo_wiki.py      # → demo/wiki/index.html
```

**Open `demo/wiki/index.html`** and walk through it. Things to point at:

- **The overview** — a Mermaid diagram of the whole map, screen counts, and a
  **"skipped actions"** list showing *Delete account* and *Empty cart* were refused
  because the target isn't a sandbox (the safety gate, visible).
- **A state page** (e.g. *Blue Runner*) — leads with the **Actions table** (label, type,
  screen-capture clip, opened-contents clip, destination), then the captured signals:
  **network requests grouped by kind** (Documents / Scripts / Styles / Images / Fonts /
  Media / Data), console output, storage keys.
- **Redaction** — the Home page logged a bearer token to the console; the wiki shows it as
  `[REDACTED]`. The raw token appears **nowhere** in the output.
- **A "Did not settle" flag** on the Sign-in page — an honestly-recorded best-effort
  capture of a page that never quiesced.
- **Screenshots and layout** — full-page captures and per-element clips, laid out under a
  `screenshots/` subfolder; pages live under `states/` and `transitions/` with
  `index.html` / `help.html` at the root, and every cross-link resolves.
- **The help/glossary page** — defines every term in plain language for a reader who
  didn't build Spoor.

`demo/generated-tests/` holds the **pytest + Playwright regression suite** generated from
the *same* graph (`spoor explore --gen-tests`). Open `test_transition_4.py`: it replays
*Shop all → Blue Runner*, fires *Add to cart*, and asserts the cart signals — a real drift
test, exported from the map.

---

## Status & what's next

**Shipping today:** config-driven extraction (tiers 1–3 + optional AI fallback), the full
operational layer (run summaries, retry/dead-letter, anti-bot detection, change detection,
politeness), passive API-surface and client-signal capture, the complete §2e exploration
engine (traversal, safety gate, signal capture, robustness, resume), the browsable wiki
(with opt-in screenshots), read-only API + MCP serving, and pytest test generation.

**Next / in design:**
- **Framework-neutral test export** — a documented data contract so Playwright / Robot /
  Cypress script generation becomes a plugin, rather than baked into the core.
- **Interactive exploration v2** — a second, opt-in round driven by a config the first run
  generates for that specific site (authenticate, fill forms, exercise flows), with the
  destructive-action boundary above kept fully intact.

**Deliberately out of scope:** native desktop apps, mobile emulators, remote device farms —
each needs a different automation stack. Current scope is web UI + the API surface reachable
from a browser session.
