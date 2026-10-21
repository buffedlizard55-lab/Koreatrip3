# COORDINATION.md — Shared Task Board (Koreatrip3)

This is the shared task board for all agent sessions working on this repo.
Protocol: read this before starting work. Claim a task by writing your session
ID + file scope, then commit and push immediately. Never start a task another
session has claimed. `needs review` items are published on the site's
"Flagged for Review" page and do not block anything.

> **Branch note (Arena sessions):** Arena-managed sessions are restricted to
> their own session branch by the platform. Session `arena-641974df` therefore
> does all work (research, data, site build, integration, publish) on branch
> `arena/641974df-koreatrip3`, which serves as the work branch **and** the
> final integration branch. The PR to `main` is opened from that branch.
> Non-Arena sessions should still use `session-<id>/<task>` branches as
> described in the project instructions.

---

## Task board

| # | Task | Status | Owner session | Files (scope) |
|---|------|--------|---------------|---------------|
| T1 | Create & maintain coordination board | done | arena-641974df | COORDINATION.md |
| T2 | Verify transportation (AREX, limousine bus, Seoul Metro routes, Namsan bus, KTX, Busan Metro) | in progress | arena-641974df | data/transport.json |
| T3 | Verify hotels (Stanford Hotel Myeongdong, L7 Haeundae by LOTTE) | in progress | arena-641974df | data/hotels.json |
| T4 | Verify Days 1–3 venues (N Seoul Tower, Namsan Cable Car, Myeongdong stores, Gwangjang/Mangwon markets, Gyeongbokgung, Bukchon, restaurants) | in progress | arena-641974df | data/venues-days1-3.json |
| T5 | Verify Days 4–8 venues (Seongsu, DDP, COEX, Ikseon-dong/Insa-dong, Itaewon, cafes/shops/restaurants) | in progress | arena-641974df | data/venues-days4-8.json |
| T6 | Verify Day 9 / Busan venues (KTX arrival, L7, Haeundae Beach, Haeundae Market) | in progress | arena-641974df | data/venues-day9.json |
| T7 | Build static itinerary site (landing page + category subpages + Flagged for Review page) | in progress | arena-641974df | assets/, build_site.py, *.html (generated) |
| T8 | Final integration: merge to main, re-verify data, link check, publish GitHub Pages | in progress | arena-641974df | repo root site files, COORDINATION.md |

(All tasks were unclaimed when this session started — the repo contained only
README.md and no COORDINATION.md. No other branches existed. This session
claimed all tasks at once because no other session is active; see log.)

---

## Work log

### arena-641974df
- **2026-10-21 (UTC):** Session start. Repo contained only `README.md`.
  Created this board; claimed T1–T8 (no other sessions/branches present).
  Committed and pushed claim immediately.
- Trip context: 2 adults; SFO→ICN; Stanford Hotel Myeongdong (Seoul,
  Nights 1–8); L7 Haeundae by LOTTE (Busan, Night 9); KTX Seoul→Busan.
  Dates line up with **2026**: Nov 1 2026 = Sunday (Day 1 arrival), Nov 2 =
  Monday (Day 2) … Nov 9 = Monday (Day 9). Original itinerary wrote
  "Nov 2, 2006" — treated as typo for 2026 (flagged).

### Sources & verification record
(Filled in as tasks complete — every site table row links its official
source; anything not confirmable from an official source is left blank and
flagged as unverified. See the site's "Flagged for Review" page.)

### Irregularities & handoffs
(None yet.)
