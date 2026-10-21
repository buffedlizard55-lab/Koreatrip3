# COORDINATION.md — Shared Task Board

**Project:** Korea Trip Itinerary site (2 adult travelers, Oct 31 – Nov 9, 2026*)
**Last updated:** 2026-10-21 by session `arena-54fb68ab`

\* The raw itinerary says "Nov 2, 2006" — treated as a typo for 2026 because every
weekday/date pair in the itinerary matches Nov 2026 exactly (Nov 2 2026 = Monday,
Nov 9 2026 = Monday). **Flagged for owner confirmation** on the Flagged for Review page.

## Branch note

The Arena platform fixes this session's branch as `arena/54fb68ab-koreatrip3`
(work on any other branch is not tracked by the session), so the
`session-<id>/<task>` branch convention is mapped onto that single branch.
Session ID for all claims below: **`arena-54fb68ab`**.

## Task board

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

Single active session this run: `arena-54fb68ab` claims tasks 1–9 sequentially on
branch `arena/54fb68ab-koreatrip3`. Any other session: check this board before
touching files; if a claim is >60 min old with no commits you may take over and log it here.

## Verification rules (agreed)

- Every table row carries a link to an **official** source (venue/operator/government).
- Values that cannot be confirmed from an official source are left **blank** and the
  row is marked **Unverified** and mirrored on the Flagged for Review page.
- Prices shown in the raw itinerary (USD estimates) are kept only as "as written in
  itinerary — unverified" unless an official source confirms them. Never inferred.
- Conflicts between the itinerary and official sources are flagged, not silently fixed.

## Log

- 2026-10-21 — Session arena-54fb68ab: created board, claimed tasks 1–9 on branch
  `arena/54fb68ab-koreatrip3`. Confirmed GitHub Pages is enabled (legacy build, main `/`).
  Date check: itinerary weekdays match Nov 2026; "2006" flagged as probable typo.
