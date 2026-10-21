# Koreatrip3

Korea trip itinerary (Seoul → Busan, two adults, Nov 1–9, 2026), with every line checked against official sources.

- **Live site (GitHub Pages):** https://buffedlizard55-lab.github.io/Koreatrip3/
- `data/records.json` — one row per itinerary line, with its official values, status and source IDs
- `data/sources.json` — source registry (official sources and context-only references)
- `data/findings.json` — repo review and irregularities for review
- `scripts/build_site.py` — validates the data, builds `docs/` and checks internal links

## Rebuild

```bash
python3 scripts/build_site.py          # validate + build docs/ + link check
python3 scripts/build_site.py --check  # validate + link check only
```

Rules enforced by the build: a row marked Verified, Conflict, Partly verified or Reference must link at least one official source and carry an official value; Unverified rows keep their official fields blank; every source URL must be on an allow-listed official domain.

Coordination for parallel sessions is in `COORDINATION.md`.
