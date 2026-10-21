# Coordination board — Koreatrip3

Shared task board. Status values: `unclaimed`, `in progress`, `done`, `needs review`.
A `needs review` item is published on the Flagged for Review page and does not block anything.

**Branch note:** this session is bound to the branch `arena/14a4cdd9-koreatrip3`. Per the session rules,
this session does not create or push other branches (`session-<id>/<task>`); all tasks below are
executed sequentially by the same session on this branch, so no concurrent edits to shared files occur.

**Session ID:** `arena/14a4cdd9` (session branch: `arena/14a4cdd9-koreatrip3`)

| # | Task | Status | Owner (session) | Files / scope |
|---|------|--------|-----------------|---------------|
| T1 | Repo review: inventory repo, record irregularities | in progress | arena/14a4cdd9 | README.md (read-only), COORDINATION.md |
| T2 | Itinerary data capture (line-by-line transcription of submitted Korea itinerary) | in progress | arena/14a4cdd9 | data/itinerary.json |
| T3 | Official-source verification of every row (hours, prices, locations, transit) | in progress | arena/14a4cdd9 | data/verification.json |
| T4 | Transit planning (AREX, airport limousine, subway, KTX, taxi notes) | in progress | arena/14a4cdd9 | data/transit.json |
| T5 | Static site build (landing + category subpages + Flagged for Review) | in progress | arena/14a4cdd9 | scripts/build_site.py, docs/** |
| T6 | Integration: combined re-verification, build + link check, publish to Pages, PR, merge | unclaimed | — | all shared outputs |

## Log

- **Claim** (arena/14a4cdd9): T1–T5 claimed; T6 reserved for the integration step of this same session.
