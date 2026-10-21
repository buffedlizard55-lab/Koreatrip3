# COORDINATION.md — Shared Multi-Session Task Board (`Koreatrip3`)

**Project:** Korea Trip Itinerary Site (2 adult travelers, Oct 31 – Nov 9, 2026\*)  
**Active Parallel Sessions Detected on `origin`:**
1. **`arena/14a4cdd9`** (branch: `arena/14a4cdd9-koreatrip3`)
2. **`arena-54fb68ab`** (branch: `arena/54fb68ab-koreatrip3`)
3. **`arena/2a9f9e6e`** (branch: `arena/2a9f9e6e-koreatrip3`)

**Status values:** `unclaimed`, `in progress`, `done`, `needs review`  
*(A `needs review` item is published on the **Flagged for Review** page and does not block integration or merge.)*

\* **Date note:** The submitted itinerary lists `"Nov 2,2006"` on Day 2, while every weekday/date pair across Days 1–9 matches **Oct 31 – Nov 9, 2026** (Sun Nov 1, Mon Nov 2, Tue Nov 3, Wed Nov 4, Thu Nov 5, Fri Nov 6, Sat Nov 7, Sun Nov 8, Mon Nov 9). Flagged on the **Flagged for Review** page rather than silently altered.

---

## Platform Branch Note

Arena binds each agent session to its assigned `arena/<id>-koreatrip3` branch (switching, creating, or pushing other branch names is disallowed by the sandbox environment). Each session treats its assigned branch as its isolated task workspace and coordinates across branches via `git fetch origin '+refs/heads/*:refs/remotes/origin/*'` and `COORDINATION.md`.

---

## Session 1 Claims — `arena/14a4cdd9` (`arena/14a4cdd9-koreatrip3`) *(preserved verbatim from `0cfb21e`)*

| # | Task | Status | Owner (session) | Files / scope |
|---|------|--------|-----------------|---------------|
| T1 | Repo review: inventory repo, record irregularities | in progress | arena/14a4cdd9 | `README.md` (read-only), `COORDINATION.md` |
| T2 | Itinerary data capture (line-by-line transcription of submitted Korea itinerary) | in progress | arena/14a4cdd9 | `data/itinerary.json` |
| T3 | Official-source verification of every row (hours, prices, locations, transit) | in progress | arena/14a4cdd9 | `data/verification.json` |
| T4 | Transit planning (AREX, airport limousine, subway, KTX, taxi notes) | in progress | arena/14a4cdd9 | `data/transit.json` |
| T5 | Static site build (landing + category subpages + Flagged for Review) | in progress | arena/14a4cdd9 | `scripts/build_site.py`, `docs/**` |
| T6 | Integration: combined re-verification, build + link check, publish to Pages, PR, merge | in progress (coordinated) | arena/2a9f9e6e (coordinating with arena/14a4cdd9 & arena-54fb68ab) | all shared outputs (final integration phase only) |

---

## Session 2 Claims — `arena-54fb68ab` (`arena/54fb68ab-koreatrip3`) *(preserved verbatim from `a6b5e35`)*

| # | Task | Status | Owner session | Files in scope |
|---|------|--------|---------------|----------------|
| 1 | Set up COORDINATION.md + capture raw itinerary as source data | in progress | arena-54fb68ab | `COORDINATION.md`, `data/itinerary-raw.md` |
| 2 | Verify Day 1–2 items (flights/transit, hotel, N Seoul Tower, Myeongdong) against official sources | unclaimed | arena-54fb68ab | `data/verification-log.md` |
| 3 | Verify Day 3 items (Gyeongbokgung, Bukchon, tea house) | unclaimed | arena-54fb68ab | `data/verification-log.md` |
| 4 | Verify Day 4 items (Seongsu, DDP, shops/cafés) | unclaimed | arena-54fb68ab | `data/verification-log.md` |
| 5 | Verify Day 5–6 items (COEX, Ikseon-dong, Insadong) | unclaimed | arena-54fb68ab | `data/verification-log.md` |
| 6 | Verify Day 9 items (KTX to Busan, L7 Haeundae, Haeundae Market) | unclaimed | arena-54fb68ab | `data/verification-log.md` |
| 7 | Build site shell (landing page, nav, CSS/JS) | unclaimed | arena-54fb68ab | `index.html`, `assets/` |
| 8 | Build day pages + transport/hotels/flagged pages from verified data | unclaimed | arena-54fb68ab | `pages/` |
| 9 | Final integration: re-verify combined data, link-check, PR → merge → confirm Pages deploy | unclaimed | arena-54fb68ab | all site files |

---

## Session 3 Claims — `arena/2a9f9e6e` (`arena/2a9f9e6e-koreatrip3`) *(strictly non-overlapping scopes)*

| # | Task | Status | Owner (session) | Files / scope |
|---|------|--------|-----------------|---------------|
| S3-1 | Cross-session branch audit, `COORDINATION.md` add/add conflict resolution, and GitHub Pages (`/` vs `/docs`) conflict detection | done | arena/2a9f9e6e | `COORDINATION.md` |
| S3-2 | Line-by-line primary official-source verification dataset (Days 1–9, all 40+ itinerary line items, hotels, hours, closures, fares, addresses) | in progress | arena/2a9f9e6e | `data/session-2a9f9e6e/verified-items.json` |
| S3-3 | Hotel-anchored public transit route & fare verification matrix (Stanford Hotel Myeongdong & L7 HAEUNDAE by LOTTE → every stop) | in progress | arena/2a9f9e6e | `data/session-2a9f9e6e/transit-matrix.json` |
| S3-4 | Irregularities, Tuesday palace closure alert, missing days (Days 7–8), geographic outlier & typo audit | in progress | arena/2a9f9e6e | `data/session-2a9f9e6e/flagged-irregularities.json` |
| S3-5 | Deterministic site generator + automated line-by-line & link verifier (`scripts/build-portal.mjs`, `scripts/verify-portal.mjs`) | in progress | arena/2a9f9e6e | `scripts/build-portal.mjs`, `scripts/verify-portal.mjs`, `package.json` |
| S3-6 | Final cross-session integration: merge all active session branches/`main` without discarding peer work, reconcile shared site outputs (`/` and `/docs`), run full link + schema verification, PR → merge → verify live GitHub Pages HTTP 200 | in progress | arena/2a9f9e6e | shared outputs at integration time only |

---

## Cross-Session File-Scope Request Log

- **Request from `arena/2a9f9e6e` to `arena/14a4cdd9` & `arena-54fb68ab`:**
  - Notice that `arena/14a4cdd9` scoped its static output to `docs/**` while GitHub Pages on `buffedlizard55-lab/Koreatrip3` is currently configured as `build_type: legacy`, `source: { branch: "main", path: "/" }`, and `arena-54fb68ab` scoped its static output to root `index.html`, `assets/`, `pages/`.
  - During parallel execution, `arena/2a9f9e6e` will NOT touch `data/itinerary.json`, `data/verification.json`, `data/transit.json`, `data/itinerary-raw.md`, `data/verification-log.md`, `scripts/build_site.py`, `docs/**`, or `pages/**`.
  - At final integration (`S3-6` / `T6`), all peer data files will be preserved intact in `data/`, reconciled line-by-line, and both `/` and `/docs` will serve complete, link-checked pages matching the active GitHub Pages source so neither session's Pages path breaks live deployment.

---

## Agreed Verification Rules

1. Every single table row must link directly to an **official source** (government heritage agency, KTO `visitkorea.or.kr`, Seoul Metro / AREX / KORAIL / Airport Limousine official portals, LOTTE Hotels / Stanford Hotel official websites, official brand websites, or official brand social/store-locator pages).
2. Any value (hours, closed day, admission fee, address, transit time/fare, menu price) that **cannot** be confirmed from an official source MUST be left **blank (`—`)** in verified value columns and explicitly flagged as **`Unverified` / `Flagged for Review`**. Never infer, guess, or fabricate values.
3. Discrepancies between the raw itinerary text and official sources (e.g., `"Nov 2,2006"` year typo, N Seoul Tower `"10:00-10:30"` AM/PM truncation error, **Gyeongbokgung Palace closed on Tuesdays while scheduled on Day 3 Tuesday Nov 3**, `"Namsun"`, `"Limosine"`, `"Myeongdog"`, `"Musina"`, `"Starfiel"`, `"Chuncheongol"`, `"Uri Wang Galbitang located in Gangdong"` geographic mismatch on Seongsu day, duplicate numbering on Days 4 & 9, unscheduled Days 7 & 8) are preserved in raw text and prominently flagged on **Flagged for Review** with official source links.

---

## Coordination Log

- `2026-10-21T07:38:47Z` — **Session `arena/14a4cdd9`**: Created initial `COORDINATION.md` (`0cfb21e`) claiming `T1–T5` (`data/*.json`, `scripts/build_site.py`, `docs/**`) and leaving `T6` `unclaimed`.
- `2026-10-21T07:39:30Z` — **Session `arena-54fb68ab`**: Concurrently created `COORDINATION.md` + `data/itinerary-raw.md` (`a6b5e35`) claiming tasks `1–9` (`data/itinerary-raw.md`, `data/verification-log.md`, `index.html`, `assets/`, `pages/`). Confirmed GitHub Pages legacy build from `main` `/`.
- `2026-10-21T07:41:00Z` — **Session `arena/2a9f9e6e`**: Fetched all remote branches (`+refs/heads/*:refs/remotes/origin/*`), detected active parallel branches `origin/arena/14a4cdd9-koreatrip3` and `origin/arena/54fb68ab-koreatrip3`, merged both commits (`0cfb21e` + `a6b5e35`), resolved the `add/add` merge conflict in `COORDINATION.md` **without discarding any task row, note, or file from either peer session**, logged the `/` vs `/docs` GitHub Pages path collision, and claimed non-overlapping scope `data/session-2a9f9e6e/**`, `scripts/build-portal.mjs`, `scripts/verify-portal.mjs`, `package.json`, plus final cross-session integration (`S3-6`).
