import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
let errors = 0;

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  errors += 1;
}

// 1. Validate session-49c638ef JSON datasets
for (const rel of [
  "data/session-49c638ef/verified-items.json",
  "data/session-49c638ef/hotels.json",
  "data/session-49c638ef/transit-matrix.json",
  "data/session-49c638ef/flagged-irregularities.json",
  "data/session-49c638ef/sources.json"
]) {
  const full = path.join(ROOT, rel);
  if (!fs.existsSync(full)) {
    fail(`Missing required dataset: ${rel}`);
    continue;
  }
  const data = JSON.parse(fs.readFileSync(full, "utf8"));
  if (!Array.isArray(data) || data.length === 0) {
    fail(`Empty dataset: ${rel}`);
    continue;
  }
  for (const row of data) {
    if (!/^https?:\/\//.test(row.officialSourceUrl || "")) {
      fail(`${rel} row missing official http(s) URL: ${JSON.stringify(row)}`);
    }
    if (!row.officialSourceLabel) {
      fail(`${rel} row missing officialSourceLabel`);
    }
  }
}

// Confirm all 16 days exist in verified-items.json
const items = JSON.parse(
  fs.readFileSync(path.join(ROOT, "data/session-49c638ef/verified-items.json"), "utf8")
);
const daySet = new Set(items.map((i) => i.dayNumber));
for (let d = 1; d <= 16; d += 1) {
  if (!daySet.has(d)) {
    fail(`Missing Day ${d} in data/session-49c638ef/verified-items.json`);
  }
}

// 2. Check all 25 HTML pages in full-itinerary/
const SITE_DIR = path.join(ROOT, "full-itinerary");
const requiredSlugs = [
  "index.html",
  "itinerary.html",
  "stays.html",
  "transit.html",
  "attractions.html",
  "dining.html",
  "shopping.html",
  "analysis.html",
  "flagged-for-review.html",
  "flagged.html",
  ...Array.from({ length: 16 }, (_, i) => `day-${i + 1}.html`)
];

for (const slug of requiredSlugs) {
  if (!fs.existsSync(path.join(SITE_DIR, slug))) {
    fail(`Missing page in full-itinerary/: ${slug}`);
  }
}

let checkedRows = 0;
for (const slug of requiredSlugs) {
  const full = path.join(SITE_DIR, slug);
  if (!fs.existsSync(full)) continue;
  const html = fs.readFileSync(full, "utf8");
  for (const tbodyMatch of html.matchAll(/<tbody>([\s\S]*?)<\/tbody>/g)) {
    const tbody = tbodyMatch[1];
    for (const trMatch of tbody.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/g)) {
      checkedRows += 1;
      const trInner = trMatch[1];
      if (!/<a\b[^>]*href="https?:\/\/[^"]+"/.test(trInner)) {
        fail(`full-itinerary/${slug}: table row missing official http(s) link: ${trInner.slice(0, 120)}`);
      }
      for (const emptyTd of trInner.matchAll(/<td\b[^>]*class="empty-cell"[^>]*>([\s\S]*?)<\/td>/g)) {
        if (emptyTd[1] !== "") {
          fail(`full-itinerary/${slug}: unverified empty-cell contains text "${emptyTd[1]}"`);
        }
      }
    }
  }
}

if (errors > 0) {
  console.error(`session-49c638ef verification failed with ${errors} error(s).`);
  process.exit(1);
}

console.log(
  `OK: session-49c638ef verified ${items.length} items across Days 1–16, ${requiredSlugs.length} HTML pages in full-itinerary/, and ${checkedRows} sourced table rows with 0 errors.`
);
