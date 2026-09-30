# Seed videos

`seed/catalog.json` names one `.mp4` per title (e.g. `ridge-and-static.mp4`), but no
video bytes ship in this repo yet — generating a real, valid, tiny clip needs an
encoder this environment doesn't have.

Drop real files here, one per catalog entry, matching the filenames already in
`catalog.json`. Keep each clip short (a few seconds) and low-bitrate so the repo stays
light, the same discipline `seed/posters/` already follows.

Until a file exists, the detail view's `<video>` element 404s gracefully and the
frontend shows "Preview unavailable" instead of failing — the catalog, login gate, and
API are fully usable without real video bytes. Add the clips before relying on the
`<video>` playback-state surface (ROADMAP.md §2c) for anything beyond wiring.
