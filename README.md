# Korea, together — current 16-day travel dashboard

**Live site:** https://buffedlizard55-lab.github.io/Koreatrip3/
**Current review register:** https://buffedlizard55-lab.github.io/Koreatrip3/flagged-for-review.html

The primary site now covers **all 16 days for two adult travelers**: Seoul / Myeongdong → Busan / Haeundae → Seoul / Hongdae. Select a day, search/filter category tables, inspect official-source links, or print/save the itinerary. All content is statically rendered and remains readable without JavaScript or third-party resources after loading. A new offline network fetch is not required to switch days; this is not a service-worker offline app.

## Build and checks

No runtime dependencies or package install required; Python 3 and Node are sufficient.

```sh
npm run check
python3 scripts/build_site.py --check
python3 source-audit/scripts/validate_site.py
node scripts/verify-session-2a9f9e6e.mjs
python3 -m http.server 8080 --bind 0.0.0.0
```

`data/full-trip.json` is the **current** primary source of truth (105 entries / 16 days). `data/current-sources.json` records 44 official references, checked evidence, methods and limitations on 26 October 2026. `scripts/build-full-trip.py` deterministically generates the 13 root pages. PR CI checks empty-field/evidence invariants and all local links. The Pages workflow repeats checks and publishes the primary site plus preserved archives.

Optional real-browser checks: install `playwright-core` and `@sparticuz/chromium` in a temporary directory outside the repository, set `NODE_PATH` to that installation's `node_modules`, provide the Chromium shared libraries appropriate to your environment, and run `npm run test:browser` against the separately running preview. `BASE_URL` overrides the default local test-server URL. The site itself never calls localhost.

## Evidence policy / important limitations

- No travel year inferred from inconsistent dates. Day 3 retains the Tuesday palace closure conflict; no silent rescheduling.
- Only **displayed nonempty factual fields** have source support. `partial` never means a whole itinerary row, reservation or future visit is verified. Context-only links explicitly do not verify the proposed venue.
- Unconfirmed hours, closed days, addresses and prices are blank. No USD conversions or guessed exact transit times. Official source excerpts are labeled when used instead of full-page reads.
- Kyoja's official-tourism English/Korean addresses disagree; Cheongsapo's official closing times conflict. Exact affected fields remain blank.
- Sky Capsule journeys are one-way; return transport needs separate confirmation. X the SKY repeats on Days 10 and 12. Day 9 duplicate consolidated; open Days 8, 13 and 15 remain open.
- Sources are an audit snapshot, not live operating status. No hotel, train, flight or attraction booking was made.
- Attempted blocked/error sources: `data/audit-attempts.md`. Submitted Week 2 plan: `data/full-trip-addendum.md`. Earlier Days 1–9 transcription remains `data/itinerary-raw.md`.

## Prior parallel-session material (historical, not current primary facts)

The concurrently published dashboard is preserved at `/previous-dashboard/`, alongside `/complete/` and `/guide/`. All earlier archived sites remain intact under `/docs/`, `/docs/trip-guide/`, `/trip/`, `/portal/`, `/source-audit/`, `/verified/`. The current site labels them as historical research and does not inherit their assumptions (including 2026 dates, secondary-source store data or unsupported KTX fares). The concurrent `data/itinerary.json` remains unchanged for archive compatibility. `npm run build:archives` and `npm run verify:archives` preserve the older portal commands. Do not regenerate older archives as a way to build the current root site.

The earlier README is preserved below as a historical log; its counts, verification claims and primary-site descriptions are superseded by this section.

---

# Korea Trip — source-audited itinerary

A lightweight, mobile-friendly GitHub Pages travel dashboard for two adults, built from the supplied South Korea trip outline. The current data preserves proposed activities and distinguishes them from facts checked against official city, tourism, transit, rail, and hotel sources.

## Pages

- **Itinerary** — day-by-day list, searchable and filterable by day.
- **Transit** — official Seoul Subway route-planning, AREX, and KORAIL links.
- **Food & shopping** — every named restaurant, café, bar, market, and shop supplied in the notes.
- **Stays** — Seoul and Busan hotel entries.
- **Flagged for review** — all unverified details, source gaps, and schedule conflicts.

## Verification policy

- Every data row in `data/itinerary.json` carries a source link.
- Only factual values supported by official sources are shown in “Officially sourced detail.” Empty values intentionally display as **Not confirmed**.
- “Source-linked” indicates an official source was consulted for some part of that row; it does not mean every proposed detail is confirmed. Caveats are shown inline and the row is also included on the review page.
- Some official links provide only district-level context and are explicitly flagged as not verifying a named business. No crowd estimates, route durations, prices, schedules, or reservations are inferred.
- Opening hours and transit information can change. The official operator/venue source should be checked again for the actual travel dates.

## Important unresolved source-plan issues

- The date/year is ambiguous. The source outline contains Oct 31/Nov 1 and several dates explicitly labeled 2006; weekdays and dated entries do not resolve to one reliable calendar. The site does not guess the year.
- Day 3 is labeled Tuesday, while the official Gyeongbokgung listing says the palace is closed on Tuesdays; the guard ceremony page also excludes Tuesdays.
- The Seoul hotel is listed in the plan as Stanford Hotel Myeongdong; the Busan hotel as L7 HAEUNDAE by LOTTE HOTELS. No reservations were provided.
- Specific routes from hotels, individual store hours, and many named businesses' current details could not be confirmed from official venue pages. See the review page.

## Local checks

The site is static and has no build dependencies. From the repository root:

```sh
python3 -m json.tool data/itinerary.json >/dev/null
python3 - <<'PY'
import json
items=json.load(open('data/itinerary.json'))
assert items and all(i.get('source','').startswith('https://') for i in items)
assert all(i.get('item') and i.get('verification') in {'verified','unverified'} for i in items)
print(f'{len(items)} rows; {sum(bool(i.get("flag")) for i in items)} flagged')
PY
```

GitHub Pages deploys from the included GitHub Actions workflow after updates reach `main`.

---

## Verified data site — `docs/` (session arena/14a4cdd9-koreatrip3)

A second, source-audited build of the same trip. Its data is `data/records.json` (72 rows) with `data/sources.json` and `data/findings.json`. It is generated by `scripts/build_site.py` into `docs/`, and is published at `/docs/` on the Pages site: https://buffedlizard55-lab.github.io/Koreatrip3/docs/

```bash
python3 scripts/build_site.py          # validate + build docs/ + link check
python3 scripts/build_site.py --check  # validate + link check only
```

Build rules: a row marked Verified, Conflict, Partly verified or Reference must link an official source and carry an official value; Unverified rows keep official fields blank; every source URL must be on an allow-listed official domain. Coordination with the other session is in `COORDINATION.md`.

---

## Trip guide — `docs/trip-guide/` (session arena/ae3cc5b4-koreatrip3)

A third parallel, independently verified build of the same trip (phone-first day-by-day guide with a recommended Days 3↔4 swap around Gyeongbokgung's Tuesday closure, and a 2026 date-alignment analysis explicitly flagged for traveler confirmation): https://buffedlizard55-lab.github.io/Koreatrip3/docs/trip-guide/ — sources and Flags F1–F20 are inside its pages; coordination/conflict log in `COORDINATION.md`.

---

## Day-by-day field guide — `trip/` (session arena/54fb68ab-koreatrip3)

A fourth parallel, independently verified build of the same trip: a 13-page mobile-first
site (dashboard, one page per day, Transport, Hotels, Flagged for Review F1–F20), generated
by `scripts/build_trip_site.py` and published at https://buffedlizard55-lab.github.io/Koreatrip3/trip/ .
Its line-by-line verification trail is `data/verification-log.md` and the unedited brief is
preserved in `data/itinerary-raw.md`. Findings agree with the other builds on all material
points; dates are presented as Nov 2026 with that assumption flagged (F3) for the traveler
to confirm. Rebuild: `python3 scripts/build_trip_site.py`, then
`python3 scripts/check_links.py` (checks all 57 pages across every site in the repo after `/source-audit/` is included).

---

## Unified Verified Portal & Hotel Public-Transit Matrix — `portal/` & category subpages (`session arena/2a9f9e6e-koreatrip3`)

A fifth parallel, zero-inference primary-source verification & public-transit build covering all 52 itinerary items (`data/session-2a9f9e6e/verified-items.json`), 13 door-to-door hotel public-transit legs (`data/session-2a9f9e6e/transit-matrix.json`), and 13 structural/schedule irregularities (`data/session-2a9f9e6e/flagged-irregularities.json`). Preserves 100% of `/`, `/docs/`, `/docs/trip-guide/`, and `/trip/`:

- **Portal Dashboard:** https://buffedlizard55-lab.github.io/Koreatrip3/portal/
- **Hotel Public-Transit Matrix:** https://buffedlizard55-lab.github.io/Koreatrip3/portal/transit.html
- **Flagged for Review Audit:** https://buffedlizard55-lab.github.io/Koreatrip3/portal/flagged-for-review.html

```bash
npm run check   # build portal + verify internal links across all 6 sites
```

---

## Source-audited companion — `source-audit/` (session `arena/b1177e35-koreatrip3`)

A sixth, independently maintained companion dashboard with a day-by-day itinerary, category pages, hotel-based public-transit guidance, an official source register, and a clearly labeled **Flagged for Review** page. Its separate dataset retains 40 itinerary rows, 11 transit routes, 57 official source links, and 30 review notes across nine day cards. It is published at <https://buffedlizard55-lab.github.io/Koreatrip3/source-audit/> and linked from the root landing page. Existing root, `/docs/`, `/docs/trip-guide/`, `/trip/`, and `/portal/` sites and their datasets remain intact.

Run its offline structural check with `python3 source-audit/scripts/validate_site.py`; the combined Pages workflow also validates its data and packages the directory.

## Full 16-day dashboard update — 26 October 2026

The root dashboard now covers the entire newly supplied trip: Days 1–16, 109 rows,
including 41 Week 2 rows, the Busan–Seoul return, and Mercure Hongdae. Use the day
buttons or share `index.html#day-16` to select a day. Print uses the current filter.
The same dataset drives Transit, Stays, Food & Shopping, and Flagged for Review.

- New input preservation: [`data/week2-input.md`](data/week2-input.md).
- Official source register and rejected URLs: [`data/week2-audit.json`](data/week2-audit.json).
- Week 2 invariants: `python3 scripts/verify-week2.py`.
- Historical Days 1–9 retain the previous 21 October audit date. This update does
  **not** certify all older facts or contradictory assumptions in companion sites.
- Blank days stay unassigned. No year, extra calendar dates, USD conversion,
  restaurant branch, transit duration, or booking is invented.
- Official recurring hours are not date-specific opening guarantees. Source links
  marked context do not verify a venue. External checks are documented per source;
  internal-link tests do not validate external pages.

---

## Complete 16-day field guide — `guide/` (session arena/1745f6a4)

Mobile tap-a-day guide covering **all 16 days** (31 Oct-16 Nov 2026; brief's '2006' flagged as F1), 3 hotels, per-day transit, verified facts only from official sources, and Flags F1-F10: https://buffedlizard55-lab.github.io/Koreatrip3/guide/ - data in `guide/data.json`, no build step.

---

## Full 16-Day Verified Dashboard, Per-Day Guides & 3-Hotel Transit Matrix — `full-itinerary/` (session `arena/49c638ef-koreatrip3`)

A complete, independently maintained 26-page mobile-friendly dashboard and category portal covering all 16 days (Week 1 Seoul Myeongdong + Week 2 Busan + Day 16 return to Seoul Hongdae):
- **82 line-by-line verified itinerary items** (`data/session-49c638ef/verified-items.json`), **3 planned hotels** (`data/session-49c638ef/hotels.json`), **24 door-to-door public-transit legs** (`data/session-49c638ef/transit-matrix.json`), and **25 flagged irregularities** (`data/session-49c638ef/flagged-irregularities.json`).
- Includes clickable standalone pages for every day (`full-itinerary/day-1.html` through `full-itinerary/day-16.html`), plus category subpages (`itinerary.html`, `stays.html`, `transit.html`, `attractions.html`, `dining.html`, `shopping.html`, `analysis.html`, and `flagged-for-review.html`).
- Published at https://buffedlizard55-lab.github.io/Koreatrip3/full-itinerary/ . Build & verify locally with `node scripts/build-session-49c638ef.mjs && node scripts/verify-session-49c638ef.mjs`.

