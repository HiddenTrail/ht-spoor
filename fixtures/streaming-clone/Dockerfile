# ROADMAP.md §5.1 archetype bench -- the fourth archetype, a purpose-built
# streaming-clone fixture.
#
# Third-party "Netflix clone" candidates were vetted and ruled out: every one
# found was either a production media server needing real video files and a
# transcoding pipeline (zoriya/Kyoo and the LocalFlix/netflix-local family),
# or a thin frontend hard-wired to an external SaaS (Apestein/nextflix needs
# Clerk+Neon+Stripe+TMDB; ridhwaans/homehost needs TMDB+Spotify; others need a
# TMDB key with no backend of their own at all). None matched this bench's
# pattern -- a self-contained app with its own data and its own same-origin
# API, no external accounts required (cf. Juice Shop's pinned image, Sauce
# Demo's pinned-source-commit build).
#
# So this one is authored by us: a small Express app (server/) serving a
# same-origin JSON API behind a session cookie, a static frontend (public/),
# and a checked-in seed catalog (seed/) -- no compile step, no database, no
# upstream commit to pin. It gives the bench a login-gated, media/detail-view
# target structurally unlike the other three, and is the first fixture to
# exercise the <video> playback-state surface ROADMAP.md §2c names but none of
# the others trigger.
FROM node:24-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY server ./server
COPY public ./public
COPY seed ./seed
EXPOSE 80
CMD ["node", "server/index.js"]
