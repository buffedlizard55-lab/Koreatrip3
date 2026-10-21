# Korea Trip · Seoul + Busan

A mobile-friendly, source-linked travel-planning site for two adult travelers. The itinerary audit separates supplied plan notes from facts found on official operator, government, tourism, and first-party business pages.

## Browse

- **Overview:** [`index.html`](index.html)
- **Day-by-day itinerary:** [`itinerary.html`](itinerary.html)
- **Attractions:** [`attractions.html`](attractions.html)
- **Shopping and markets:** [`shopping.html`](shopping.html)
- **Food and cafés:** [`food.html`](food.html)
- **Hotels:** [`stays.html`](stays.html)
- **Public transit:** [`getting-around.html`](getting-around.html)
- **Official source register:** [`sources.html`](sources.html)
- **Flagged for Review:** [`flagged-for-review.html`](flagged-for-review.html)

## Research and schedule policy

- Every itinerary, transit, and review-register table/card links to an official source for manual review.
- Unsupported values remain blank and are called out on **Flagged for Review**; conflicts are not silently corrected.
- Original date strings are preserved exactly as recorded: `Oct.31/Nov 1` and `Monday—Nov 2,2006`. No trip year is inferred.
- Day 7 and Day 8 remain blank. Venue notes whose day order could not be established stay in **Not assigned to a day**.
- Search-result excerpts, dynamic pages, and blocked/redirecting sources are labeled as such; recheck date-sensitive hours, fares, closures, and service details before travel.

## Run locally

This is a dependency-free static site. From the repository root, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000`. The pages load local JSON data, so they should be served over HTTP rather than opened directly as `file://` URLs.

Run the offline structure/data/link check with:

```sh
python3 scripts/validate_site.py
```

## GitHub Pages

A GitHub Actions workflow in `.github/workflows/pages.yml` validates the site and deploys it on pushes to `main`. After the first successful deployment, the expected project-site address is:

<https://buffedlizard55-lab.github.io/Koreatrip3/>

Deployment must be confirmed from the repository's Actions/Pages status after merge.
