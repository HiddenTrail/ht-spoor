# Seed videos

One short, low-bitrate `.mp4` per catalog entry, matching the filenames in
`seed/catalog.json` (e.g. `ridge-and-static.mp4`) — same discipline
`seed/posters/` follows: small enough that the repo stays light (each clip is
a few seconds, well under 1 MB).

If a file is ever missing (a new catalog entry added without its clip yet),
the detail view's `<video>` element 404s gracefully and the frontend shows
"Preview unavailable" instead of failing — the catalog, login gate, and API
stay fully usable either way.
