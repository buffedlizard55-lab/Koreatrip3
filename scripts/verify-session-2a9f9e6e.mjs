import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
let errors = 0;

function fail(msg) {
  console.error(`FAIL: ${msg}`);
  errors += 1;
}

// 1. Validate session JSON datasets
for (const rel of [
  "data/session-2a9f9e6e/verified-items.json",
  "data/session-2a9f9e6e/transit-matrix.json",
  "data/session-2a9f9e6e/flagged-irregularities.json"
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

// 2. Collect all HTML files across entire repo (excluding .git / node_modules / _site)
function collectHtmlFiles(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if ([".git", "node_modules", "_site"].includes(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      collectHtmlFiles(full, out);
    } else if (entry.name.endsWith(".html")) {
      out.push(full);
    }
  }
  return out;
}

const htmlFiles = collectHtmlFiles(ROOT);
if (htmlFiles.length === 0) {
  fail("No HTML files found in repository!");
}

// Build map of anchors per HTML file
const idsByFile = new Map();
for (const file of htmlFiles) {
  const content = fs.readFileSync(file, "utf8");
  const ids = new Set();
  for (const m of content.matchAll(/\bid="([^"]+)"/g)) {
    ids.add(m[1]);
  }
  idsByFile.set(file, ids);
}

// 3. Check all internal links, assets, anchors, and table row source links
let checkedLinks = 0;
let checkedPortalRows = 0;

for (const file of htmlFiles) {
  const relFile = path.relative(ROOT, file);
  const content = fs.readFileSync(file, "utf8");

  // Check every href and src attribute
  for (const m of content.matchAll(/\b(?:href|src)="([^"]+)"/g)) {
    const raw = m[1].trim();
    if (
      !raw ||
      raw.startsWith("http://") ||
      raw.startsWith("https://") ||
      raw.startsWith("mailto:") ||
      raw.startsWith("tel:") ||
      raw.startsWith("javascript:") ||
      raw.startsWith("data:")
    ) {
      continue;
    }
    checkedLinks += 1;
    const [targetPart, hashPart] = raw.split("#");
    const targetFile = targetPart
      ? path.resolve(path.dirname(file), targetPart)
      : file;

    if (!fs.existsSync(targetFile)) {
      fail(`${relFile}: broken relative target "${raw}" -> missing ${path.relative(ROOT, targetFile)}`);
      continue;
    }

    if (hashPart && targetFile.endsWith(".html")) {
      const targetIds = idsByFile.get(targetFile);
      if (targetIds && !targetIds.has(hashPart)) {
        fail(`${relFile}: broken anchor "${raw}" -> missing id="#${hashPart}" in ${path.relative(ROOT, targetFile)}`);
      }
    }
  }

  const OUR_ROOT_SLUGS = new Set([
    "itinerary.html",
    "attractions.html",
    "dining.html",
    "shopping.html",
    "analysis.html",
    "flagged.html"
  ]);

  // Strictly audit every <tbody><tr> on /portal/ pages and our non-overlapping root pages
  if (OUR_ROOT_SLUGS.has(relFile) || relFile.startsWith("portal/")) {
    for (const tbodyMatch of content.matchAll(/<tbody>([\s\S]*?)<\/tbody>/g)) {
      const tbody = tbodyMatch[1];
      for (const trMatch of tbody.matchAll(/<tr\b[^>]*>([\s\S]*?)<\/tr>/g)) {
        checkedPortalRows += 1;
        const trInner = trMatch[1];
        if (!/<a\b[^>]*href="https?:\/\/[^"]+"/.test(trInner)) {
          fail(`${relFile}: table row missing official http(s) link: ${trInner.slice(0, 120)}`);
        }
        for (const emptyTd of trInner.matchAll(/<td\b[^>]*class="empty-cell"[^>]*>([\s\S]*?)<\/td>/g)) {
          if (emptyTd[1] !== "") {
            fail(`${relFile}: unverified empty-cell contains text "${emptyTd[1]}"`);
          }
        }
      }
    }
  }
}

if (errors > 0) {
  console.error(`Verification failed with ${errors} error(s).`);
  process.exit(1);
}

console.log(
  `OK: Verified ${htmlFiles.length} HTML files, ${checkedLinks} internal links/anchors, and ${checkedPortalRows} sourced dashboard table rows with 0 errors.`
);
