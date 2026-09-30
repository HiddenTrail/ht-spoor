# `fixtures/` — test fixtures (ROADMAP.md §5.1)

Fixtures are the opposite of integrations (§0): they exist purely to prove the
**generic** tiers hold up across different architectural shapes. If a fixture
only passes with a special case added for it, that's a bug in the general
mechanism, never a reason to add the special case.

Present:

- **`static/`** — hand-built HTML fixtures for §2a extraction tests
  (`products.html`, `listing.html`, `catalog/page-{1,2,3}.html` for
  pagination, `feed.html` for the tier-2 infinite-scroll case, and
  `js-rendered.html` — an empty shell populated by JS on load, for the
  content-driven tier-1→tier-2 escalation case). The static ones are served
  deterministically via an `httpx.MockTransport` (no sockets); the
  browser-backed ones (`feed.html`, `js-rendered.html`) are served over a
  loopback `http.server`, since a real browser can't use the mock transport.
- **`docker-compose.yml`** — the §5.1 archetype bench. It now stands up four
  live targets: **OWASP Juice Shop** (an Angular SPA — a real, uncontrolled
  tier-2 target, port 3000), **Sauce Demo** (a second, login-gated SPA, port
  3001), **PrestaShop** (a server-rendered PHP/MySQL storefront, port 8080 —
  the first deeply-linked, stateful, multi-page site, standing in for the kind of
  large storefront §2e exploration mode maps), and **streaming-clone** (a
  purpose-built, login-gated media-browsing app, port 3002 — see below). Each
  joined when the phase that can exercise it arrived (see the "Phase-1 in-vivo
  bench" decision in ROADMAP §5.1). Bring the bench up with
  `docker compose -f fixtures/docker-compose.yml up -d`. PrestaShop ships as two
  services (`prestashop` + its `prestashop-db` MariaDB) and **auto-installs on
  first boot** — the first `up` takes a few minutes while it builds the schema
  and demo catalog; the installed state persists in a Docker volume, so later
  boots are fast. Host ports are overridable (`SAUCE_DEMO_PORT`,
  `PRESTASHOP_PORT`, `STREAMING_CLONE_PORT`) for machines already using the
  defaults. The integration tests under `tests/` skip when a target isn't
  reachable, so the fast unit gate stays Docker-free.
- **`streaming-clone/`** — source for the fourth archetype. Third-party
  "Netflix clone" projects were vetted and ruled out (every one needed either
  real video files plus a transcoding pipeline, or a hard dependency on an
  external SaaS like Clerk/Stripe/TMDB — see the Dockerfile's header comment
  for the full list), so this one is a small, purpose-built Express app: a
  same-origin JSON API behind a login-gated session cookie, a static frontend,
  and a checked-in seed catalog (`streaming-clone/seed/catalog.json`) with
  generated placeholder posters and one short, low-bitrate video clip per
  title (`streaming-clone/seed/videos/`), so the `<video>` playback-state
  signal (ROADMAP §2c) is exercised out of the box — see
  `streaming-clone/seed/videos/README.md` for the filename contract if a
  catalog entry's clip is ever missing (the detail view degrades to "Preview
  unavailable" rather than failing). Since it's login-gated, `spoor explore`
  needs a captured session (`--session`, added alongside this archetype) to
  map anything past the login screen — see `README.md`'s "Exploring a
  logged-in site" for how to capture one.

Planned (added as their phases need them):

- **More static fixture pages** — one mechanism each (class name changes every
  reload → tier-3 healing; WebSocket traffic → §2c capture).
- **The rest of the archetype matrix** — a self-hosted ERPNext/Odoo, added to
  `docker-compose.yml` once API discovery (§2b/§2.5) needs it, declared
  `sandbox: true` like the rest of the bench. (Sauce Demo, PrestaShop, and
  streaming-clone have since landed — see above.)

Public scraping-practice sandboxes (`books.toscrape.com`,
`quotes.toscrape.com`) are used for integration tests/demos but are not vendored
here.
