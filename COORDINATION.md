# Coordination board

This board tracks the Korea itinerary source audit, static site, verification, and publication. The active Arena session is fixed to `arena/b1177e35-koreatrip3`; all work remains on that branch.

| Task | Status | Owner / session ID | File scope |
|---|---|---|---|
| Full itinerary-source audit, structured findings, responsive GitHub Pages site, verification, and publication | in progress — implementation and pre-merge checks | `arena/b1177e35-koreatrip3` | `COORDINATION.md`, `README.md`, `index.html`, category HTML pages, `assets/`, `data/`, `.nojekyll`, `.gitignore`, `scripts/`, `.github/workflows/` |

## Handoff / coordination notes

- Initial repository check found only `README.md`. The current session claimed the full integration scope before research and immediately committed/pushed the claim as `08e3d04` (`Claim itinerary research and site integration`). No competing task claim was found.
- This session uses the fixed Arena branch and will not switch or create another branch.
- No parallel tasks or handoffs are active. Shared itinerary data, source index, navigation, and integration are owned by this session.
- Research policy: every published itinerary/transit/review row links to an official source; only explicitly supported facts are populated. Unsupported location, hours, days, fares, and prices stay blank and are called out on **Flagged for Review**. Date-sensitive details are snapshots checked 2026-10-21, not promises for an unknown trip date.
- The original source itinerary itself was not present in the checkout at handoff. The available session notes preserve the date strings, named venues, high-confidence day assignments, and flags. Unknown day placements remain unassigned; Day 7/8 remain blank. No attempt is made to recreate missing lines from inference.

## Source verification notes

- Official sources directly fetched include: Incheon airport arrival procedures; Airport Limousine 6015; Seoul Metro FAQ; L7 Haeundae location/directions; N Seoul Tower hours/admission/shuttle; Olive Young Myeongdong Town; Myeongdong district; Hanjungsun; Crystal Jade Shinsegae Main; Busan Metro route map; and official hotel/tourism/business location pages noted in `data/sources.json`.
- Official tourism pages/results were used for Gyeongbokgung hours/Tuesday closure, royal ceremony schedule, Bukchon restrictions, DDP, COEX, markets, the KTX general booking window, and Busan Haeundae Market. The U.S. Naval Observatory's official Gregorian/Julian date calculator is linked for checking the raw Day 2 weekday/date pairing; the literal Nov 2, 2006 computes to Thursday, not Monday, and the displayed plan text is not edited.
- Primary-source limitations are disclosed in the source register: AREX pages rendered an error image; Stanford FAQ redirected; Blue Elephant was blocked by Cloudflare; the Rain Report KTO page returned a transient 400; some official business details are indexed profile excerpts only. They are not mislabeled as direct page verification.
- High-priority findings: the raw Day 2 date/weekday string needs correction from the traveler but remains unchanged; Day 3 says Tuesday while Gyeongbokgung is normally closed Tuesdays; the AREX “$7 / 45 minutes” value does not identify a service; the supplied N Seoul Tower `$31` package is not confirmed; KTX fare/train and the 45-minute station-arrival rule are not established; Myeongdong Kyoja official address records conflict.
- Store/restaurant branch or schedule gaps include the exact intended branches for Rain Report, Chuncheongol Dakgalbi, Uri Wang Galbitang, Hongojib, Pig Restaurant 2, ADER, Brandy Melville, “Soul Market,” and the unnamed COEX café/pastry stop. Exact unverified values remain blank.

## Files and verification

- `data/itinerary.json` — days and all retained itinerary/location notes; every entry has a source ID and status.
- `data/transit.json` — station-level, hotel-based public-transit guidance with no invented door-to-door times.
- `data/sources.json` — source URL, publisher, evidence type, check date, and limitations.
- `data/flags.json` — review log and next checks.
- `scripts/validate_site.py` — offline check for JSON references, source links, blank-day/date preservation, and local page links.
- `.github/workflows/pages.yml` — validates and deploys the static site on pushes to `main`.

Pre-merge checks and publication result will be recorded below after final validation and GitHub Pages deployment. Flagged/unverified items do not block merge if the site and workflow are healthy.

## Checks / publication log

- Claim: committed and pushed as `08e3d04` before research/implementation.
- Local validation passed: `python3 scripts/validate_site.py` (9 pages, 9 days, 40 itinerary rows, 11 transit routes, 57 official source links, 30 review notes); JSON parsing; `node --check assets/app.js`; and `git diff --check`.
- The local HTTP preview returned 200 for the dashboard, itinerary, JSON data, JavaScript, and stylesheet. The Pages workflow has been manually reviewed; its validation step will run in GitHub Actions on the main-branch deployment.
- Implementation is complete locally. Pull request, merge, and GitHub Pages deployment remain in progress.
