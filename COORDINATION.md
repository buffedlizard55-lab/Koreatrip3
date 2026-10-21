# Coordination Board — Koreatrip3

Shared task board for the Korea itinerary site project. All sessions claim tasks here before working.

## Session
- Current branch: `arena/dd80b342-koreatrip3`
- Session ID: `single-session-1` (sole agent this session)

## Task status
| # | Task | Status | Owner | Files touched | Sources / verification | Notes |
|---|------|--------|-------|---------------|------------------------|-------|
| 1 | Create COORDINATION.md task board | done | single-session-1 | COORDINATION.md | n/a | Initial claim |
| 2 | Research official sources for all itinerary items (hours, locations, transport, hotels) | in progress | single-session-1 | docs/sources.md | official sites linked per item | Verification in progress |
| 3 | Build site structure + landing page (dashboard UI, mobile-friendly) | unclaimed | — | index.html, css/, js/ | n/a | Static HTML/CSS |
| 4 | Build day-by-day itinerary subpages (Days 1–9) | unclaimed | — | days/day*.html | per-item sources | Table format per row |
| 5 | Build category subpages (transport, accommodation, dining, attractions, shopping) | unclaimed | — | categories/*.html | per-item sources | Linked from dashboard |
| 6 | Build verification + "Flagged for Review" page (unverified items) | unclaimed | — | verification.html, flagged.html | n/a | Links to official sources |
| 7 | Add GitHub Pages config, build check, no broken links | unclaimed | — | .github/workflows/, _config.yml (if Jekyll) | n/a | Static site OK |
| 8 | Create PR from integration branch to main, merge, confirm Pages deploy | unclaimed | — | n/a | n/a | Final integration |
| 9 | Record PR link + merge result in COORDINATION.md | unclaimed | single-session-1 | COORDINATION.md | n/a | Final step |

## Conventions
- Every table row must carry a source link to an official/verified site.
- If a value cannot be confirmed from an official source, leave it blank and mark "unverified" — never infer.
- Claim a task by writing session ID + file scope, then commit + push immediately.
- Never start a task another session has claimed.
