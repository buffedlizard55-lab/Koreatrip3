# COORDINATION.md — Shared task board

Session ID for this session: `arena/ae3cc5b4-koreatrip3` (branch fixed by Arena; do not rename)

| # | Task | Status | Owner | Files in scope | Sources / notes |
|---|------|--------|-------|----------------|-----------------|
| 1 | Create board + claim all tasks (only session present) | done | arena/ae3cc5b4 | COORDINATION.md | this file |
| 2 | Research & verify itinerary line-by-line vs official sources | done | arena/ae3cc5b4 | docs/ (data in HTML), COORDINATION.md | see verification log below |
| 3 | Build GitHub Pages site (landing + day/category subpages + Flagged page) | done | arena/ae3cc5b4 | docs/** |  |
| 4 | Link/build check, PR to main, merge, confirm Pages deploy | in progress | arena/ae3cc5b4 | .github/workflows/pages.yml, COORDINATION.md |  |

## Rules (from task brief)
- Every table row needs an official-source link; unconfirmed values left blank + flagged "Unverified". Never infer.
- Flagged/needs-review items are published on "Flagged for Review" page; they do NOT block merge.
- Small frequent commits; `git pull --rebase` before push; never edit files claimed by another session.
- Note: Arena fixes this session to branch `arena/ae3cc5b4-koreatrip3`; the brief's `session-<id>/<task>` naming cannot be used here.

## Handoff / conflict log
- (none — single session; internal link/anchor/tag check passed 2026-10-21; local preview served all 5 pages HTTP 200)

## Verification log (checked 2026-10-21)
- Dates: weekday alignment Nov 2=Mon … Nov 9=Mon fits **2026 only**; "2006" in brief is a typo (Nov 2 2006 was Thu). Flag F1.
- AREX official (arex.or.kr): Express 43 min T1 / 51 min T2, adult ₩13,000; All-stop 59/66 min. Seoul city gov page concurs.
- Airport Limousine official 6015: ₩17,000 adult / ₩12,000 child; stops incl. Lotte Hotel·IBIS Myeongdong, Royal Hotel (Euljiro 1-ga).
- N Seoul Tower official: Observatory Mon–Fri 10:00–22:30, weekends/holidays 10:00–23:00, last entry 30 min before close, adult ₩29,000; Cable car 10:00–23:00, adult return ₩15,000 (separate ticket/operator page on same official site).
- Gyeongbokgung (VISITKOREA/KTO + royal.khs.go.kr): Nov–Feb 09:00–17:00 last adm. 16:00, **closed Tuesdays**, adult ₩3,000, guard ceremony 10:00 & 14:00 Wed–Mon. → Day 3 (Tue Nov 3) impossible. Flag F2 (critical).
- Bukchon (Seoul Metropolitan gov notice): Red Zone (Bukchon-ro 11-gil) tourist visits restricted 17:00–10:00, fine ₩100,000 since 2025-03-01.
- DDP official: 10:00–20:00, closed Jan 1/Seollal/Chuseok only.
- Starfield COEX official: 10:30–22:00; Starfield Library same hours.
- Gwangjang (VISITKOREA): general 09:00–18:00, food street 09:00–23:00; general closed Sundays, food street year-round. Mangwon (Visit Seoul): 10:00–21:00 varies by store.
- Lotte Dept Main (Lotte Shopping official global): 10:30–20:00, extended 10:30–20:30. Shinsegae Main (VISITKOREA): Mon–Thu 10:30–20:00, Fri–Sun 10:30–20:30. Olive Young Myeongdong Town official: 10:00–22:30 (brief's 08:00–24:00 NOT confirmed).
- Myeongdong Kyoja: Michelin Guide + VISITKOREA agree 10:30–21:00; **address conflict** (29 Myeongdong 10-gil vs 129 Toegye-ro). Flag F14.
- Cafe Onion Anguk official (onionkr.com): Mon–Fri 07:00–22:00, weekends/holidays 09:00–22:00, last order 21:30.
- Stanford Hotel Myeongdong official FAQ: 84 Namdaemun-ro, Jung-gu; check-in after 15:00, check-out before 12:00.
- L7 Haeundae: official Lotte page exists but renders no check-in/out text; secondary sources conflict (11:00 vs 12:00 check-out) → left blank/unverified. Flag F13.
- KTX: official booking = Korail (letskorail.com/korail.com). Secondary fares conflict (₩54,400 vs ₩59,800, Sept-2026 fare change reported) → fare/time for a specific Nov 9 train left blank to check on Korail. Flag F12.
- Seoul Metro official: adult card base fare ₩1,550 ≤10 km. Climate Card tourist passes (VISITKOREA/Seoul gov): card ₩3,000; 1d ₩5,000 / 2d ₩8,000 / 3d ₩10,000 / 5d ₩15,000 / 7d ₩20,000, cash only, excl. Sinbundang/GTX.
- Entry: MOFA notice — US included in K-ETA temporary exemption extended to 2026-12-31; e-Arrival Card portal e-arrivalcard.go.kr (file within 3 days before arrival per MOJ notices reported by KPMG/EY).
- No official source found (hours/prices/address left BLANK, flagged): SFO–ICN flight, Pig Restaurant 2, Hongojib, Sookhee, Solsot Seongsu, Hanjungsun, caricature shop, Eternalog, Blue Elephant, Cafe Far Ben, Rain Report Cafe, Jayeondo price, Musinsa Standard/Margesherwood/Ader Error/Brandy Melville Seongsu branches, Break Silence, Chuncheongol Dakgalbi, Uri Wang Galbitang, Soul Market COEX, Chwihyang, Favorite of Ikseon, Crystal Jade Shinsegae-basement branch, all USD prices in brief, all door-to-door transit times in brief.

