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
