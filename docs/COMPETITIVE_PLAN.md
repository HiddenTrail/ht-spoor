# Competitive plan — what Spoor takes from the landscape

> **Status: working draft, maintainer-editable.** This is a planning file, not a
> decision record. Nothing here is decided until it is recorded in
> `docs/ROADMAP.md` (which wins on any conflict). Edit freely: change an
> approach, strike a row, move items between phases, fill in the decision fields.
>
> Legend for **Approach**: **Depend** = use the library as an engine underneath
> Spoor · **Adapt** = take the idea, build Spoor's own generic version · **Build** =
> small, Spoor-native · **Skip** = deliberately not matched (see "Deliberate
> non-goals").
>
> Competitor facts below are from general knowledge, not a fresh survey —
> verify current feature lists before quoting any of them externally.

## 1. Goal

Reach roughly **90% of what the comparable tools do** on the table stakes, while
keeping what makes Spoor distinct — not by becoming a grab bag of every feature,
but by being the robust, deterministic, safe tool in the space.

The LLM-assisted paths (browser-use-style form filling, LLM-generated configs)
are on the horizon as an **optional** tier, never the default run loop.

## 2. Findings that shape the plan

- **The biggest gap is basic crawling, not advanced features.** Spoor extracts
  from a target URL and follows *pagination* (next-link, infinite scroll), but has
  no request queue/frontier, no cross-site link following, no sitemap ingestion,
  no scope rules, and no concurrency. That is exactly what Scrapy and Crawlee are
  built on.
- **ROADMAP / code mismatch to resolve.** ROADMAP §2d says "Crawlee's autoscaling
  pool already handles per-domain concurrency and backoff," but `crawlee` is not a
  dependency in `pyproject.toml`, and `spoor/core/config.py` says concurrency caps
  are "deferred until a request pool exists." Either adopt Crawlee (decision D1)
  or correct §2d.
- **"Glue several tools side by side" doesn't work.** Spoor's guarantees —
  destructive actions sandbox-only, redaction on by default, deterministic runs,
  read-only serving — hold only if **one layer owns every action that reaches the
  target and every output that leaves**. Four tools means four places actions fire
  and four output paths. **Depending on libraries as engines *underneath*
  Spoor's layer** does work: Spoor stays the part that holds the guarantees and
  builds the map.

## 3. Decisions needed

| ID | Decision | Options | Owner | Decision / date |
|---|---|---|---|---|
| D1 | Adopt Crawlee (Python) as the crawl engine? | Depend on Crawlee · build a minimal frontier · correct §2d and stay single-URL | maintainer | _open_ |
| D2 | Record "LLM once, replay forever" as the model for the optional LLM tier? | Yes · no · decide later | maintainer | _open_ |
| D3 | _add your own_ | | | |

## 4. What to take, by source

### Crawlee / Scrapy — scraper table stakes

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Request queue + link following with scope rules (include/exclude patterns, depth, same-origin) | Depend (Crawlee) | The core gap; rebuilding it would take years to catch up | 1 | |
| Autoscaling concurrency, per-domain limits, backoff | Depend (comes with the queue) | Spoor's politeness/retry code becomes configuration on top | 1 | |
| Sitemap and robots.txt as sources of URLs to crawl | Depend or Adapt | Cheap; users expect it | 1 | |
| Resumable, persisted crawl state | Depend | Fits the existing resume story | 1 | |
| Proxy support (bring your own) | Adapt | Already designed in §2d; Spoor never provides proxies | 1 | |
| Output sinks: SQLite, Parquet | Build (small) | Already planned (#108) | 1 | |
| Request/response hooks (middleware) | Adapt | Lets users extend without forking; keeps site-specific logic out of core (§0) | 2 | |

### Scrapling — self-healing

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Adaptive element relocation and its similarity scoring | **Benchmarked, closes #151** — Scrapling scored worse; not adapted | Measured on the identical mutation corpus (`scripts/benchmark_scrapling.py`): tier 3 ≥99.3%, Scrapling ~88-89% across two independent seeds — see the §5.3 decision note in ROADMAP.md | 2 | |
| Stealth fetchers / fingerprint spoofing | Skip | Spoor's stance is "detect bot challenges, never bypass them" (§2d) | — | |

### Crawljax — exploration (closest prior art to §2e)

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Configurable state equivalence (which DOM differences count as "same state") | Adapt | Addresses #104 (DOM-identical screens collapse) and the §2e settling races | 2 | |
| Clickable-element rules incl. exclusions | **Adapted, closes #152** | User-set rules, not heuristics — fits the §1 "not an agent" principle; `--include-element`/`--exclude-element`, see the §2e decision note in ROADMAP.md | 2 | |
| Form input specifications | Adapt, feeding #103 | Deterministic form filling before any LLM | 2 | |
| Plugin hooks (on new state, on transition) | Adapt | Same extension point as the middleware row | 2 | |
| Invariants (assertions checked during a crawl) | Skip | A verdict — belongs in generated tests (§2g), per the observe-vs-judge boundary in the §2f freshness note | — | |

### browser-use / Skyvern / Stagehand — the LLM horizon

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| "LLM once, replay forever": an LLM works out an action, Spoor records it as a deterministic step and replays without the model (cf. Stagehand's action caching) | Adapt (optional LLM tier) | How LLMs fit Spoor's determinism: model for discovery, every later run free and repeatable | 3 | depends on D2 |
| LLM form filling in a sandbox | Adapt, gated by the existing sandbox registry | Covers the form-filling work; the safety gate already exists | 3 | |
| Accessibility-tree page representation for prompts | Adapt | Spoor already captures accessibility trees (§2c) | 3 | |
| Autonomous goal-driven agents | Skip | §1: Spoor is "not an agent" | — | |

### Crawl4AI / Firecrawl — content for LLMs

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Page → clean markdown output | Build (small; a sink) | Cheap parity with a highly visible feature | 1 or 2 | |
| LLM generates the extraction config once, then runs deterministically (cf. Crawl4AI's schema generation) | Adapt | Same "LLM once" pattern; eases the hardest onboarding step (writing configs) | 3 | depends on D2 |

### OWASP ZAP / Katana — discovery

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Extract endpoints/routes from JS bundles without executing them | **Adapted, closes #153** — `spoor/api_discovery/bundle_endpoints.py` | Finds API calls no click triggered; generic; see the §2b layer-6 decision note in ROADMAP.md | 2 | |
| Scope configuration | Covered by the Crawlee row | | 1 | |

### Healenium / Testim — healing reports

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Healing report: old locator, new locator, confidence, suggested fix | Adapt | Spoor already records heal events (§2); surfacing them as suggested config/test fixes makes tier 3 visible | 2 | |

## 5. Deliberate non-goals

Stated plainly in the README as choices, not gaps:

- Stealth / anti-bot evasion and CAPTCHA solving
- A hosted or distributed platform
- Autonomous, goal-driven agents
- Verdicts inside Spoor (pass/fail, severity, invariants) — consumers judge

## 6. Phases

- [ ] **Phase 1 — scraper table stakes.** Decide D1; request queue + link
      following + scope rules; sitemaps; concurrency; proxy hook; SQLite/Parquet
      sinks; (optionally) markdown output. Until this lands, "scraper" is not a
      fair claim.
- [ ] **Phase 2 — robustness.** Configurable state equivalence; Scrapling
      benchmark on the tier-3 corpus; healing reports; JS-bundle endpoint
      extraction; request and exploration hooks; form input specifications.
- [ ] **Phase 3 — optional LLM tier ("LLM once, replay forever").** Decide D2;
      config generation; sandbox form filling; action caching for replay.

Each item still goes through the normal workflow when picked up: a ROADMAP
decision note, then the `.feature` file first (CLAUDE.md, BDD first).

## 7. Why continue

The gap is concentrated in crawling basics — the part a library supplies most
cheaply. The differentiators are broader than signals, wikis and MCP:

1. Self-healing measured against an honest, merge-blocking bar (≥95%, §5.3)
2. Safety guarantees built into the design (sandbox-only destructive actions,
   redaction by default, read-only serving)
3. Deterministic, local runs with no API key
4. The map as the product — generated tests, drift detection (§2f freshness
   note), and agent serving all built on it

None of the tools above has more than two of these. 90% parity is realistic
because most of that 90% is crawling basics; the effort spreads too thin only if
Spoor *builds* the basics as well as the differentiators.

## 8. Open notes

_Space for your own notes, links, benchmark results._
