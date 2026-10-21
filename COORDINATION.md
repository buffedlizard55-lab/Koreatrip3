# Coordination board — Koreatrip3

Shared task board. Status values: `unclaimed`, `in progress`, `done`, `needs review`.
A `needs review` item is published on the Flagged for Review page and does not block anything.

**Branch note:** this session is bound to the branch `arena/14a4cdd9-koreatrip3`. Per the session rules,
this session does not create or push other branches (`session-<id>/<task>`); all tasks below are
executed sequentially by the same session on this branch, so no concurrent edits to shared files occur.

**Session ID:** `arena/14a4cdd9` (session branch: `arena/14a4cdd9-koreatrip3`)

| # | Task | Status | Owner (session) | Files / scope |
|---|------|--------|-----------------|---------------|
| T1 | Repo review: inventory repo, record irregularities | done | arena/14a4cdd9 | README.md (read-only), COORDINATION.md |
| T2 | Itinerary data capture (line-by-line transcription of submitted Korea itinerary) | done | arena/14a4cdd9 | data/itinerary.json |
| T3 | Official-source verification of every row (hours, prices, locations, transit) | done | arena/14a4cdd9 | data/verification.json |
| T4 | Transit planning (AREX, airport limousine, subway, KTX, taxi notes) | done | arena/14a4cdd9 | data/transit.json |
| T5 | Static site build (landing + category subpages + Flagged for Review) | done | arena/14a4cdd9 | scripts/build_site.py, docs/** |
| T6 | Integration: combined re-verification, build + link check, publish to Pages, PR, merge | in progress | arena/14a4cdd9 | all shared outputs |

## Log

- **Claim** (arena/14a4cdd9): T1–T5 claimed; T6 reserved for the integration step of this same session.

### T1 — Repo review (done)
- **Sources:** `git ls-files` on `main` @ fa82001; README.md (contents: `# Koreatrip3`).
- **Verification:** repo contains no itinerary, data, site or COORDINATION file before this session.
- **Irregularities:** none in repo content; the itinerary was supplied in the task text, not in the repo.

### T2 — Itinerary data (done)
- **Output:** `data/records.json` — 72 rows: 68 plan rows (every submitted line, in order) + 4 official reference rows.
- **Verification:** each line keeps its submitted text; statuses assigned per row (Verified 9, Partly verified 7, Conflict 7, Unverified 40, plan notes/no-plan 5).
- **Irregularities:** see IRR-12 to IRR-15, IRR-18 and IRR-20 in `data/findings.json`.

### T3 — Official-source verification (done)
- **Sources (official):** Gyeongbokgung Palace hours & admissions (royalpalacekr.org); Korea Heritage Service guard ceremony (kh.or.kr); N SEOUL TOWER hours, admission, cable car (nseoultower.co.kr); Seoul Metropolitan Government airport access (english.seoul.go.kr); Airport Limousine route 6001 (airportlimousine.co.kr); Stanford Hotel Myeongdong and L7 Haeundae property pages; Korail notice 2025-08-18; VisitKorea and Visit Seoul/Visit Busan listings; Lotte store page; Olive Young Myeongdong store page; DDP (ddp.or.kr); Starfield COEX Mall; Michelin Guide; Jongno-gu Office. Full list: `data/sources.json`.
- **Method:** each row checked against an official page; unverified values left blank and flagged; no currency conversion.
- **Irregularities:** IRR-01 to IRR-11 (critical: Tuesday palace visit; Olive Young and N Seoul Tower hours; palace fee for ages 7–18; AREX and airport bus fares; KTX time/fare not verified; Myeongdong Kyoja address; Lotte closure on Nov 9; Pig Restaurant 2 location; hotel pages on booking-network domains).

### T4 — Transit planning (done)
- **Output:** Transit page; rows D1-02, D1-03, D2-04, D5-02, D9-02, D9-04 and reference rows REF-01 to REF-04.
- **Verified:** AREX express 43/51 min and ₩13,000; all-stop ₩4,150–4,750; airport limousine 6001 ₩17,000; cable car access from Myeongdong Station Exit 3; Samseong Station Exit 5/6 to COEX; Seoul Station connects to KTX.
- **Not verified:** KTX timetable and fare; bus to N Seoul Tower; taxi times; Myeongdong→Seoul Station fare.

### T5 — Static site build (done)
- **Output:** `scripts/build_site.py`, `docs/` (index, itinerary, transit, hours & locations, costs & fees, analysis, Flagged for Review, sources). GitHub Pages source to be set to `main /docs` (see T6).
- **Checks:** `python3 scripts/build_site.py` → OK, 0 errors.

### T6 — Integration (in progress, session arena/14a4cdd9)
- Re-verify combined data: `python3 scripts/build_site.py --check` (validation + internal link check).
- Create PR `arena/14a4cdd9-koreatrip3` → `main`, merge, confirm GitHub Pages deploy, record PR link and merge result here.

### Handoff / branch note
- Session branch fixed to `arena/14a4cdd9-koreatrip3`; the `session-<id>/<task>` branch scheme was not used because the session branch is bound to this session. No conflicting edits from other sessions were observed on this branch.
