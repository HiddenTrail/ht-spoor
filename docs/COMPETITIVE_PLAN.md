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

- ~~**The biggest gap is basic crawling, not advanced features.**~~ **Resolved —
  closed.** This was true when this plan was written; it no longer is. A request
  queue/frontier with scope rules (#169), sitemap/robots.txt ingestion (#170),
  bounded per-domain concurrency (#174), resumable persisted crawl state (#175),
  bring-your-own-proxy (#149), SQLite/Parquet sinks (#108), and request/response +
  exploration hooks (#150, #187) have all shipped, in-house. See the §3 D1 row and
  the updated §4 Crawlee/Scrapy table below.
- ~~**ROADMAP / code mismatch to resolve.**~~ **Resolved.** D1 (#146) decided
  against Crawlee; `spoor/core/config.py`'s concurrency comment and ROADMAP.md
  were brought in line with the shipped in-house implementation (#174). No
  `crawlee` dependency exists in `pyproject.toml`.
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
| D1 | Adopt Crawlee (Python) as the crawl engine? | Depend on Crawlee · build a minimal frontier · correct §2d and stay single-URL | maintainer | **decided 2026-10-01 — build in-house (#146, closed).** Rationale: Crawlee's `AutoscaledPool` needs an asyncio seam in a codebase that's synchronous throughout (`httpx.Client`, Playwright's *sync* API) — that cost, not a capability gap, is what tipped it. Every item the §4 table below named as gated on this decision has since shipped in-house with zero new dependencies (see that table). |
| D2 | Record "LLM once, replay forever" as the model for the optional LLM tier? | Yes · no · decide later | maintainer | **decided 2026-09-30 — yes (#147, closed).** An LLM works out an action or config once, Spoor records it as a deterministic step, and every later run replays it without the model — fits Spoor's core determinism guarantee (§1: the model is consulted only for discovery, never something a later run's correctness depends on). See the "shape of the future optional LLM tier" decision note in ROADMAP.md §9. Not yet implemented — this only settled the *shape*, Phase 3 itself hasn't started. |
| D3 | _add your own_ | | | |

## 4. What to take, by source

### Crawlee / Scrapy — scraper table stakes

**All seven rows below are shipped, in-house, with no `crawlee` (or other crawl-engine) dependency — see the D1 row in §3.** This table's rows were written when D1 was still open and this whole section was the plan's "biggest gap"; kept here, corrected, as the record of what closed it.

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Request queue + link following with scope rules (include/exclude patterns, depth, same-origin) | **Built in-house, closes #169** | A `deque`-based frontier + `crawl:` config block; no engine dependency needed | 1 | See the "link following with scope rules" decision note in ROADMAP.md §2d |
| Autoscaling concurrency, per-domain limits, backoff | **Built in-house, closes #174** | `concurrent.futures.ThreadPoolExecutor` + a per-domain semaphore — no asyncio seam, which is exactly the cost that tipped D1 against Crawlee | 1 | See the "bounded concurrent fetching, in-house" decision note in ROADMAP.md §2d |
| Sitemap and robots.txt as sources of URLs to crawl | **Built in-house, closes #170** | Cheap; users expect it — no engine dependency needed for this either | 1 | See the "sitemap.xml and robots.txt as crawl seed sources" decision note in ROADMAP.md §2d |
| Resumable, persisted crawl state | **Built in-house, closes #175** | Fits the existing resume story | 1 | See the "resumable, persisted crawl state" decision note in ROADMAP.md §2d |
| Proxy support (bring your own) | **Built in-house, closes #149** | Already designed in §2d; Spoor never provides proxies | 1 | See the "bring-your-own-proxy" decision note in ROADMAP.md §2d |
| Output sinks: SQLite, Parquet | **Built, closes #108** | Small, Spoor-native sinks | 1 | |
| Request/response hooks (middleware) | **Built in-house, closes #150 (+ exploration hooks #187)** | Lets users extend without forking; keeps site-specific logic out of core (§0) | 2 | See the "request/response hooks" and "exploration hooks" decision notes in ROADMAP.md |

### Scrapling — self-healing

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Adaptive element relocation and its similarity scoring | **Benchmarked, closes #151** — Scrapling scored worse; not adapted | Measured on the identical mutation corpus (`scripts/benchmark_scrapling.py`): tier 3 ≥99.3%, Scrapling ~88-89% across two independent seeds — see the §5.3 decision note in ROADMAP.md | 2 | |
| Stealth fetchers / fingerprint spoofing | Skip | Spoor's stance is "detect bot challenges, never bypass them" (§2d) | — | |

### Crawljax — exploration (closest prior art to §2e)

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Configurable state equivalence (which DOM differences count as "same state") | **Adapted, closes #104** | Addresses DOM-identical screens collapsing, and the §2e settling races; see the "visual state identity" decision note in ROADMAP.md | 2 | |
| Clickable-element rules incl. exclusions | **Adapted, closes #152** | User-set rules, not heuristics — fits the §1 "not an agent" principle; `--include-element`/`--exclude-element`, see the §2e decision note in ROADMAP.md | 2 | |
| Form input specifications | **Adapted, closes #103** | Deterministic form filling before any LLM | 2 | |
| Plugin hooks (on new state, on transition) | **Adapted, closes #187** | Same extension point as the middleware row (#150) | 2 | |
| Invariants (assertions checked during a crawl) | Skip | A verdict — belongs in generated tests (§2g), per the observe-vs-judge boundary in the §2f freshness note | — | |

### browser-use / Skyvern / Stagehand — the LLM horizon

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| "LLM once, replay forever": an LLM works out an action, Spoor records it as a deterministic step and replays without the model (cf. Stagehand's action caching) | Adapt (optional LLM tier) | How LLMs fit Spoor's determinism: model for discovery, every later run free and repeatable | 3 | D2 decided (yes); not yet built |
| LLM form filling in a sandbox | Adapt, gated by the existing sandbox registry | Covers the form-filling work; the safety gate already exists | 3 | |
| Accessibility-tree page representation for prompts | Adapt | Spoor already captures accessibility trees (§2c) | 3 | |
| Autonomous goal-driven agents | Skip | §1: Spoor is "not an agent" | — | |

### Crawl4AI / Firecrawl — content for LLMs

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Page → clean markdown output | **Built — shipped** (`spoor run -f md`) | Cheap parity with a highly visible feature | 1 or 2 | |
| LLM generates the extraction config once, then runs deterministically (cf. Crawl4AI's schema generation) | Adapt | Same "LLM once" pattern; eases the hardest onboarding step (writing configs) | 3 | D2 decided (yes); not yet built |

### OWASP ZAP / Katana — discovery

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Extract endpoints/routes from JS bundles without executing them | **Adapted, closes #153** — `spoor/api_discovery/bundle_endpoints.py` | Finds API calls no click triggered; generic; see the §2b layer-6 decision note in ROADMAP.md | 2 | |
| Scope configuration | Covered by the scope-rules row above (#169, shipped) | | 1 | |

### Healenium / Testim — healing reports

| Feature | Approach | Why | Phase | Notes |
|---|---|---|---|---|
| Healing report: old locator, new locator, confidence, suggested fix | **Adapted, closes #154** — `spoor run --healing-report`, `spoor/operational/healing_report.py` | Spoor already records heal events (§2); surfacing them as a suggested config fix makes tier 3 visible — see the Phase-3 tier-3 healing-report decision note in ROADMAP.md | 2 | |

## 5. Deliberate non-goals

Stated plainly in the README as choices, not gaps:

- Stealth / anti-bot evasion and CAPTCHA solving
- A hosted or distributed platform
- Autonomous, goal-driven agents
- Verdicts inside Spoor (pass/fail, severity, invariants) — consumers judge

## 6. Phases

- [x] **Phase 1 — scraper table stakes. Done.** D1 decided (build in-house,
      #146); request queue + link following + scope rules (#169); sitemaps
      (#170); concurrency (#174); resumable crawl state (#175); proxy hook
      (#149); SQLite/Parquet sinks (#108); markdown output (`-f md`, shipped
      alongside the other sinks). "Scraper" is now a fair claim.
- [x] **Phase 2 — robustness. Done.** Configurable state equivalence (#104);
      Scrapling benchmark on the tier-3 corpus (#151, not adapted — tier 3
      measured better); healing reports (#154); JS-bundle endpoint extraction
      (#153); request and exploration hooks (#150, #187); form input
      specifications (#103); generated-test reverse assertion (#128, a scoped
      first piece — the fuller "freshness by re-observation" mechanism remains
      open as #211, low priority, tracked separately).
- [ ] **Phase 3 — optional LLM tier ("LLM once, replay forever").** D2 decided
      (#147, closed — "LLM once, replay forever"); not yet implemented: config
      generation; sandbox form filling; action caching for replay.

Each item still goes through the normal workflow when picked up: a ROADMAP
decision note, then the `.feature` file first (CLAUDE.md, BDD first).

## 7. Why continue

Phases 1 and 2 are done — the crawling-basics gap this plan opened with is
closed, in-house, with no new dependency tree. What's left is Phase 3 (the
optional LLM tier — its shape is decided, D2, but it isn't built yet) and
whatever this plan doesn't yet name. The differentiators were always broader
than signals, wikis and MCP:

1. Self-healing measured against an honest, merge-blocking bar (≥95%, §5.3)
2. Safety guarantees built into the design (sandbox-only destructive actions,
   redaction by default, read-only serving)
3. Deterministic, local runs with no API key
4. The map as the product — generated tests, drift detection (§2f freshness
   note), and agent serving all built on it

None of the tools above has more than two of these. Most of the §1 90%-parity
goal *was* crawling basics, and that's now built — the remaining gap to that
goal is narrower than this plan's original framing, concentrated in whatever
Phase 3 and §8's open notes turn out to name.

## 8. Open notes

_Space for your own notes, links, benchmark results._
