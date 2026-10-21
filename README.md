# Koreatrip3 — Korea Itinerary (Nov 1–9, 2026)

A verified, mobile-friendly travel itinerary site for two adult travelers:
**Seoul (Myeongdong base) → Busan (Haeundae)**, built from the owner's raw itinerary
and checked line by line against official sources (venues, operators, government).

🌐 **Live site:** https://buffedlizard55-lab.github.io/Koreatrip3/

## What's inside

| Path | Purpose |
|---|---|
| `index.html`, `pages/` | The published site (GitHub Pages serves repo root on `main`) |
| `assets/` | CSS/JS for the site |
| `scripts/build_site.py` | Site generator — all content/data lives here; re-run to rebuild |
| `scripts/check_links.py` | Internal link/anchor checker |
| `data/itinerary-raw.md` | The itinerary exactly as provided (source of record) |
| `data/verification-log.md` | Line-by-line verification trail with official sources |
| `COORDINATION.md` | Shared task board for parallel agent sessions |

## Verification rules

- Every table row links an **official** source.
- Values that can't be confirmed officially are left **blank** and flagged
  **Unverified** on the site's *Flagged for Review* page — never inferred.
- Conflicts between the itinerary and official sources are flagged, not silently fixed.

## Rebuild the site

```bash
python3 scripts/build_site.py   # regenerate index.html, pages/, assets/
python3 scripts/check_links.py  # verify no broken internal links
python3 -m http.server 8000     # local preview
```
