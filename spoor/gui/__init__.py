"""Local GUI: operate Spoor from a browser instead of the command line (ROADMAP.md §2i).

A separate local *control plane*, deliberately not part of the read-only serving
layer (`spoor/serving/`, §2f): this package adds no route, tool or flag there. It
only *reads* through the serving layer's shared helpers (`MapStore`,
`views.map_view`) so a map looks exactly as redacted here as it does over REST/MCP.

- `app.py` — the FastAPI app: the security guard (access token, Host and Origin
  checks) and the pages.
- `launch.py` — starts the app on a loopback-only socket with a fresh per-launch
  token (`spoor gui`).
- `templates.py` — the Jinja2 page templates, inline like the §2e wiki's.

Requires the optional GUI extras: ``pip install 'ht-spoor[gui]'``.
"""
