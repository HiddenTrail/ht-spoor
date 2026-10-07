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
- **`docker-compose.yml`** — the §5.1 archetype bench. It now stands up five
  live targets: **OWASP Juice Shop** (an Angular SPA — a real, uncontrolled
  tier-2 target, port 3000), **Sauce Demo** (a second, login-gated SPA, port
  3001), **PrestaShop** (a server-rendered PHP/MySQL storefront, port 8080 —
  the first deeply-linked, stateful, multi-page site, standing in for the kind of
  large storefront §2e exploration mode maps), **streaming-clone** (a
  purpose-built, login-gated media-browsing app, port 3002 — see below), and
  **Odoo** (a self-hosted ERP/eCommerce suite, port 8069 — see below). Each
  joined when the phase that can exercise it arrived (see the "Phase-1 in-vivo
  bench" decision in ROADMAP §5.1). Bring the bench up with
  `docker compose -f fixtures/docker-compose.yml up -d`. PrestaShop ships as two
  services (`prestashop` + its `prestashop-db` MariaDB) and **auto-installs on
  first boot** — the first `up` takes a few minutes while it builds the schema
  and demo catalog; the installed state persists in a Docker volume, so later
  boots are fast. Odoo is the same two-service shape (`odoo` + its `odoo-db`
  PostgreSQL) but, unlike PrestaShop, is **not** auto-installed by `up -d` —
  measured empirically, Odoo's install flags (`-i`) redo real work (re-walking
  every targeted module's view/data XML) on *every* start, not just the first
  (81s per boot in testing, against ~7s plain), so baking them into the
  steady-state command would tax every future `up`/restart forever. Instead,
  **before the first `up`**, run the one-time init once:
  ```
  docker compose -f fixtures/docker-compose.yml up -d odoo-db
  docker compose -f fixtures/docker-compose.yml run --rm odoo \
    odoo -d spoor_demo -i base,website_sale --without-demo=False --stop-after-init
  ```
  This takes a few minutes (installing `base` + `website_sale` with demo data
  is genuinely heavier than PrestaShop's install) and exits when done
  (`--stop-after-init`); after that, `docker compose ... up -d` starts the
  `odoo` service in a few seconds against the now-seeded `spoor_demo` database,
  persisted in a Docker volume. **Skipping this step doesn't fail loudly** —
  Odoo auto-bootstraps a minimal, demo-data-free `base`-only database the first
  time it sees nothing named `spoor_demo` exists, so `up -d odoo` alone still
  "works" (`/web/login` answers 200) but `/shop` 404s, since `website_sale`
  was never installed; run the init command above if the storefront 404s.
  The seeded storefront needs no login (`/shop`); the backend admin UI
  (`/odoo`) does, with demo credentials
  `admin`/`admin`. Host ports are overridable (`SAUCE_DEMO_PORT`,
  `PRESTASHOP_PORT`, `STREAMING_CLONE_PORT`, `ODOO_PORT`) for machines already
  using the defaults. The integration tests under `tests/` skip when a target
  isn't reachable, so the fast unit gate stays Docker-free.
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
- **Odoo** — the fifth archetype, joining now that API discovery (§2b) has
  shipped (this was the gate the earlier version of this entry named). The
  official Community-edition image (`odoo:17.0`), seeded via the one-time init
  command above with a `spoor_demo` database carrying `base` + `website_sale`
  (Odoo's eCommerce module) and demo data, so there's a real storefront
  (`/shop` — products, categories, cart) to scrape without a manual
  setup-wizard click. Structurally unlike every prior archetype: the backend
  admin UI (`/odoo`) is itself a heavy SPA sitting in front of JSON-RPC/XML-RPC
  web-service endpoints, while `/shop` is a server-rendered storefront in the
  *same* app — one target exercising both API-discovery shapes at once. No
  login is needed to reach the storefront or browse products; the backend
  admin UI is login-gated (default demo credentials: `admin` /
  `admin`) if a future slice wants to exercise that surface too.

Planned (added as their phases need them):

- **More static fixture pages** — one mechanism each (class name changes every
  reload → tier-3 healing; WebSocket traffic → §2c capture).

Public scraping-practice sandboxes (`books.toscrape.com`,
`quotes.toscrape.com`) are used for integration tests/demos but are not vendored
here.
