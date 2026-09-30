// ROADMAP.md §5.1 archetype bench -- streaming-clone fixture server.
//
// A tiny, purpose-built Express app: a same-origin JSON API (login, catalog,
// title detail) behind a server-set session cookie, plus the static frontend
// and seeded media. No database -- the catalog is a small checked-in JSON file
// loaded into memory once at startup.
"use strict";

const path = require("path");
const express = require("express");
const cookieSession = require("cookie-session");
const catalog = require("../seed/catalog.json");

const app = express();
const PORT = process.env.PORT || 80;

// A single seeded fixture account -- this is a test fixture, not a real auth
// system, so the credential is an obvious, documented placeholder.
const SEED_USER = { username: "viewer", password: "spoor-viewer-pw" };

app.use(express.json());
app.use(
  cookieSession({
    name: "streaming_clone_session",
    keys: ["spoor-streaming-clone-fixture-session-key"],
    maxAge: 24 * 60 * 60 * 1000,
  })
);

function requireSession(req, res, next) {
  if (!req.session || !req.session.loggedIn) {
    res.status(401).json({ error: "not authenticated" });
    return;
  }
  next();
}

app.post("/api/login", (req, res) => {
  const { username, password } = req.body || {};
  if (username === SEED_USER.username && password === SEED_USER.password) {
    req.session.loggedIn = true;
    res.json({ ok: true });
    return;
  }
  res.status(401).json({ error: "invalid credentials" });
});

app.post("/api/logout", (req, res) => {
  req.session = null;
  res.json({ ok: true });
});

app.get("/api/session", (req, res) => {
  res.json({ loggedIn: Boolean(req.session && req.session.loggedIn) });
});

function summarize(entry) {
  return {
    id: entry.id,
    title: entry.title,
    category: entry.category,
    poster: `/media/posters/${entry.poster}`,
  };
}

app.get("/api/catalog", requireSession, (req, res) => {
  const byCategory = new Map();
  for (const entry of catalog) {
    if (!byCategory.has(entry.category)) byCategory.set(entry.category, []);
    byCategory.get(entry.category).push(summarize(entry));
  }
  const rows = Array.from(byCategory, ([category, titles]) => ({ category, titles }));
  res.json({ rows });
});

app.get("/api/titles/:id", requireSession, (req, res) => {
  const entry = catalog.find((item) => item.id === req.params.id);
  if (!entry) {
    res.status(404).json({ error: "not found" });
    return;
  }
  res.json({
    id: entry.id,
    title: entry.title,
    category: entry.category,
    synopsis: entry.synopsis,
    poster: `/media/posters/${entry.poster}`,
    video: `/media/videos/${entry.video}`,
  });
});

app.use("/media/posters", express.static(path.join(__dirname, "..", "seed", "posters")));
app.use("/media/videos", express.static(path.join(__dirname, "..", "seed", "videos")));
app.use(express.static(path.join(__dirname, "..", "public")));

app.listen(PORT, () => {
  console.log(`streaming-clone fixture listening on ${PORT}`);
});
