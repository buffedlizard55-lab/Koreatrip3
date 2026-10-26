import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const DATA_DIR = path.join(ROOT, "data/session-49c638ef");
const OUT_DIR = path.join(ROOT, "full-itinerary");
const ASSETS_DIR = path.join(OUT_DIR, "assets");

fs.mkdirSync(ASSETS_DIR, { recursive: true });

const items = JSON.parse(
  fs.readFileSync(path.join(DATA_DIR, "verified-items.json"), "utf8")
);
const hotels = JSON.parse(
  fs.readFileSync(path.join(DATA_DIR, "hotels.json"), "utf8")
);
const transitMatrix = JSON.parse(
  fs.readFileSync(path.join(DATA_DIR, "transit-matrix.json"), "utf8")
);
const irregularities = JSON.parse(
  fs.readFileSync(path.join(DATA_DIR, "flagged-irregularities.json"), "utf8")
);

// Build and save unique official sources register
const sourceMap = new Map();
for (const row of [...items, ...hotels, ...transitMatrix, ...irregularities]) {
  const url = row.officialSourceUrl;
  const label = row.officialSourceLabel;
  if (url && !sourceMap.has(url)) {
    sourceMap.set(url, {
      officialSourceLabel: label,
      officialSourceUrl: url
    });
  }
}
fs.writeFileSync(
  path.join(DATA_DIR, "sources.json"),
  JSON.stringify([...sourceMap.values()], null, 2) + "\n"
);

const DAY_META = [
  {
    dayNumber: 1,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Sunday",
    dateLabel: "Oct 31 / Nov 1 (2026 calendar alignment)",
    title: "Travel from SFO to Seoul & Check into Stanford Hotel Myeongdong",
    city: "Incheon -> Seoul (Myeongdong)",
    hotel: "Stanford Hotel Myeongdong (84 Namdaemun-ro, Jung-gu)",
    summary: "Arrive at Incheon Int'l Airport (ICN), transfer to Myeongdong via Airport Limousine Bus 6015 (17,000 KRW direct to hotel block) or AREX train, check in at Stanford Hotel Myeongdong (9F lobby, from 15:00), and take a light neighborhood walk."
  },
  {
    dayNumber: 2,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Monday",
    dateLabel: "Nov 2 (draft says 'Nov 2,2006' — flagged)",
    title: "Namsan Seoul Tower, Myeongdong Shopping & Night Markets",
    city: "Seoul (Namsan / Myeongdong / Jongno)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Morning Namsan Shuttle Bus 01A/01B (1,500 KRW) or Namsan Cable Car (15,000 KRW RT) to N Seoul Tower Observatory (29,000 KRW, 10:00–22:30), afternoon Myeongdong shopping (Lotte/Shinsegae 10:30–20:00, Olive Young 10:00–22:30), and evening Gwangjang/Myeongdong/Mangwon market or Michelin-listed Myeongdong Kyoja (relocated 2026 to 129 Toegye-ro)."
  },
  {
    dayNumber: 3,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Tuesday",
    dateLabel: "Nov 3",
    title: "Gyeongbokgung Palace, Bukchon Hanok Village & Traditional Tea House",
    city: "Seoul (Jongno-gu)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "CRITICAL SCHEDULE ALERT: Gyeongbokgung Palace & the Royal Guard Ceremony are CLOSED on Tuesdays! Swap Day 3 with Day 4 (Wednesday) or visit Changdeokgung/Deoksugung instead. Also note Bukchon Hanok Village Red Zone tourist hours (10:00–17:00) and Cha Masineun Tteul Tuesday closure."
  },
  {
    dayNumber: 4,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Wednesday",
    dateLabel: "Nov 4",
    title: "Seongsu-dong ('Brooklyn of Seoul') & Dongdaemun Design Plaza (DDP)",
    city: "Seoul (Seongdong-gu / Jung-gu)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Direct Line 2 subway (17 min from Euljiro 1-ga) to Seongsu Station for Solsot pot rice, Hanjungsun fruit mochi, Jayeondo salt bread, Cafe Onion Seongsu, Cafe Far Ben, Musinsa, Blue Elephant, Marge Sherwood, Ader Error, and DDP (10:00–20:00)."
  },
  {
    dayNumber: 5,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Thursday",
    dateLabel: "Nov 5",
    title: "Starfield COEX Mall, Starfield Library & Gangnam Style Statue",
    city: "Seoul (Gangnam-gu)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Direct Line 2 subway from Euljiro 1(il)-ga Station to Samseong Station Exit 5/6 (~30 min, 1,550 KRW) into Starfield COEX Mall & Starfield Library (10:30–22:00, free) and the Gangnam Style Horse Dance Statue at COEX East Square."
  },
  {
    dayNumber: 6,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Friday",
    dateLabel: "Nov 6",
    title: "Ikseon-dong Hanok Alley & Insadong",
    city: "Seoul (Jongno-gu)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Explore Ikseon-dong Hanok Village & Insadong cultural street (Line 2->Line 3 to Anguk or Jongno 3-ga, ~8 min): Chwihyang (Favorite of Ikseon), Rain Report Rainbow (10:30–20:30), and Jayeondo Saltbread."
  },
  {
    dayNumber: 7,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Saturday",
    dateLabel: "Nov 7",
    title: "Itaewon District (Open / Unspecified Schedule)",
    city: "Seoul (Yongsan-gu)",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Draft lists only header 'Day 7: Saturday - Itaewon(Nov 7)' with no specific stops. Accessible via Line 4 Myeongdong -> Samgakji -> Line 6 Itaewon Station (~16 min, 1,550 KRW)."
  },
  {
    dayNumber: 8,
    week: "Week 1 — Seoul (Myeongdong)",
    weekday: "Sunday",
    dateLabel: "Nov 8",
    title: "Open / Unassigned Seoul Day",
    city: "Seoul",
    hotel: "Stanford Hotel Myeongdong",
    summary: "Draft lists only header 'Day 8: Sunday -(Nov 8)' with no scheduled activities. Kept blank per zero-inference verification policy."
  },
  {
    dayNumber: 9,
    week: "Week 1 -> Week 2 Transition",
    weekday: "Monday",
    dateLabel: "Nov 9 (appears at end of Week 1 & start of Week 2)",
    title: "Travel from Seoul to Busan via KTX & Check into L7 Haeundae",
    city: "Seoul -> Busan (Haeundae)",
    hotel: "Check out Stanford Myeongdong (by 12:00) -> Check in L7 HAEUNDAE by LOTTE (from 15:00)",
    summary: "Morning checkout from Stanford Hotel Myeongdong, KTX high-speed train from Seoul Station to Busan Station (~2h 45m, 54,400 KRW), transfer to L7 HAEUNDAE by LOTTE (55 Haeun-daero 570beon-gil), and evening walk to Haeundae Beach & Haeundae Traditional Market (09:00–22:00)."
  },
  {
    dayNumber: 10,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Tuesday",
    dateLabel: "Implied Nov 10",
    title: "Haeundae Beach, Amso Galbi, Dongbaekseom, Nurimaru, Sky Capsule & Daritdol Skywalk",
    city: "Busan (Haeundae / Dongbaekseom / Mipo / Cheongsapo)",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "Walk Haeundae Beach, lunch at MICHELIN-selected Haeundae Amso Galbijip (opens 11:30), loop Dongbaekseom Coastal Trail & free Nurimaru APEC House (09:00–18:00), ride Haeundae Blueline Park Sky Capsule from Mipo to Cheongsapo, walk Cheongsapo Daritdol Observatory (09:00–21:00, free), optional BUSAN X the SKY, and dinner at Haeundae Market."
  },
  {
    dayNumber: 11,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Wednesday",
    dateLabel: "Implied Nov 11",
    title: "Gamcheon Culture Village, Songdo Beach / Cloud Trails / Cable Car & Old Downtown (BIFF / Jagalchi / Gukje / Nampo)",
    city: "Busan (Saha-gu / Seo-gu / Jung-gu)",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "Morning trip to Gamcheon Culture Village (09:00–18:00 alley hours, free) & Coffee It House, followed by BIFF Square, Jagalchi Fish Market (05:00–22:00, open Wed), Songdo Beach, Songdo Cloud Trails (06:00–23:00, free), optional Busan Air Cruise Cable Car (09:00–21:00, 17,000–22,000 KRW RT), Gukje Market (09:00–20:00, open Wed) & Nampo-dong Gwangbok-ro shopping."
  },
  {
    dayNumber: 12,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Thursday",
    dateLabel: "Implied Nov 12",
    title: "BUSAN X the SKY, SEA LIFE Busan Aquarium & Haeundae Shopping",
    city: "Busan (Haeundae Beach)",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "10:00–11:30 AM at BUSAN X the SKY observation deck in LCT Landmark Tower (10:00–21:00, 29,000 KRW adult), beachfront lunch, afternoon at SEA LIFE Busan Aquarium (weekday hours 10:00–19:00, 32,000 KRW official adult gate fee vs draft's '$15'), and Haeundae shopping/dinner."
  },
  {
    dayNumber: 13,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Friday",
    dateLabel: "Implied Nov 13",
    title: "Open / Unassigned Busan Day (Friday)",
    city: "Busan",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "Draft lists only header 'Day 13: Friday' with no scheduled items. Preserved as an open day with blank official fields."
  },
  {
    dayNumber: 14,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Saturday",
    dateLabel: "Implied Nov 14",
    title: "Gwangalli Beach Evening & Gwangalli M Drone Light Show (7:00 PM Winter Show)",
    city: "Busan (Suyeong-gu)",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "Open daytime, then head at 17:00 via Busan Metro Line 2 (Haeundae -> Gwangan Station Exit 3/5, ~23 min door-to-door, 1,600 KRW) to Gwangalli Beach for early dinner and the free Saturday Gwangalli M Drone Light Show (winter Oct–Feb schedule: 19:00 & 21:00, ~10–12 min)."
  },
  {
    dayNumber: 15,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Sunday",
    dateLabel: "Implied Nov 15",
    title: "Open / Unassigned Busan Day (Sunday)",
    city: "Busan",
    hotel: "L7 HAEUNDAE by LOTTE",
    summary: "Draft lists only header 'Day 15: Sunday' with no scheduled items. Note: Nov 15, 2026 is the 3rd Sunday of the month, when Gukje Market observes its regular 1st/3rd Sunday closure."
  },
  {
    dayNumber: 16,
    week: "Week 2 — Busan & Return to Seoul (Hongdae)",
    weekday: "Monday",
    dateLabel: "Implied Nov 16",
    title: "Travel from Busan to Seoul (KTX + AREX) & Check into Mercure Ambassador Seoul Hongdae",
    city: "Busan (Haeundae) -> Seoul (Hongdae)",
    hotel: "Check out L7 HAEUNDAE (before 11:00) -> Check in Mercure Ambassador Seoul Hongdae (from 15:00)",
    summary: "Check out of L7 HAEUNDAE before 11:00 AM, transfer to Busan Station (Metro Line 2->1 ~42 min at 1,800 KRW or Uber/taxi), take KTX to Seoul Station (54,400 KRW), ride AREX All-Stop Train (NOT Express!) 2 stops to Hongik Univ. Station (~7 min, 1,550 KRW), and walk via Exit 8 (elevator) or Exit 9 to Mercure Ambassador Seoul Hongdae (144 Yanghwa-ro)."
  }
];

const NAV_ITEMS = [
  { slug: "index.html", label: "Dashboard" },
  { slug: "itinerary.html", label: "All 16 Days" },
  { slug: "stays.html", label: "3 Hotels" },
  { slug: "transit.html", label: "Public Transit" },
  { slug: "attractions.html", label: "Attractions" },
  { slug: "dining.html", label: "Dining & Cafes" },
  { slug: "shopping.html", label: "Shopping & Markets" },
  { slug: "analysis.html", label: "Analysis & Costs" },
  { slug: "flagged-for-review.html", label: "Flagged for Review", flagged: true }
];

function esc(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function statusBadge(status) {
  const map = {
    verified: ["badge-verified", "Verified"],
    conflict: ["badge-conflict", "Conflict Flagged"],
    partial: ["badge-partial", "Partial / Check Note"],
    unverified: ["badge-unverified", "Unverified"],
    needs_review: ["badge-needs_review", "Unverified / Review"],
    critical: ["badge-critical", "Critical Blocker"],
    high: ["badge-high", "High Priority"],
    medium: ["badge-medium", "Medium Priority"],
    low: ["badge-low", "Unverified Blank"]
  };
  const [cls, text] = map[status] || ["badge-unverified", "Unverified"];
  return `<span class="badge ${cls}">${esc(text)}</span>`;
}

function cell(label, value) {
  if (value === undefined || value === null || String(value).trim() === "") {
    return `<td data-label="${esc(label)}" class="empty-cell"></td>`;
  }
  return `<td data-label="${esc(label)}">${esc(value)}</td>`;
}

function dayPickerGrid(activeDay = null) {
  return `<section class="section-card" aria-label="Click or choose a day">
    <div class="section-header">
      <div>
        <h2>Click or Choose a Day (Days 1–16 · Weeks 1 &amp; 2)</h2>
        <p class="section-subtitle">Tap any day card below to open its dedicated mobile field guide with verified hours, hotel transit directions, and flagged warnings.</p>
      </div>
      <a class="source-btn" href="itinerary.html">View All 16 Days in One Table</a>
    </div>
    <div class="day-grid">
      ${DAY_META.map((d) => {
        const dayItems = items.filter((i) => i.dayNumber === d.dayNumber);
        const flagCount = dayItems.filter((i) => i.status !== "verified").length;
        const isActive = activeDay === d.dayNumber ? " active-day-card" : "";
        const weekTag = d.dayNumber <= 8 ? "Week 1 · Seoul" : d.dayNumber === 9 ? "W1→W2 · KTX" : d.dayNumber <= 15 ? "Week 2 · Busan" : "Day 16 · Hongdae";
        return `<a class="day-tile${isActive}" href="day-${d.dayNumber}.html">
          <div class="day-tile-top">
            <span class="day-num">Day ${d.dayNumber}</span>
            <span class="day-week-tag">${esc(weekTag)}</span>
          </div>
          <div class="day-tile-weekday">${esc(d.weekday)} · ${esc(d.dateLabel)}</div>
          <div class="day-tile-title">${esc(d.title)}</div>
          <div class="day-tile-meta">${dayItems.length} row(s) · ${flagCount} flagged/note</div>
        </a>`;
      }).join("\n")}
    </div>
  </section>`;
}

function dayPillBar(activeDay = null) {
  return `<nav class="day-pill-bar" aria-label="Quick day switcher">
    <a class="day-pill${activeDay === null ? " active" : ""}" href="itinerary.html">All 16 Days</a>
    ${DAY_META.map(
      (d) =>
        `<a class="day-pill${activeDay === d.dayNumber ? " active" : ""}" href="day-${d.dayNumber}.html">Day ${d.dayNumber} (${esc(d.weekday.slice(0, 3))})</a>`
    ).join("")}
  </nav>`;
}

function renderItemRows(list) {
  const knownFlagIds = new Set(irregularities.map((f) => f.flagCode || f.flagId));
  return list
    .map(
      (row) => {
        const fc = row.flagCode;
        const flagHtml = fc
          ? knownFlagIds.has(fc)
            ? `<div class="submitted-quote"><a href="flagged-for-review.html#${esc(fc)}">${esc(fc)}</a></div>`
            : `<div class="submitted-quote"><a href="flagged-for-review.html#item-${esc(row.id)}">${esc(fc)}</a></div>`
          : "";
        return `<tr id="item-${esc(row.id)}" data-filterable="1" data-status="${esc(row.status)}" data-day="Day ${esc(row.dayNumber)}">
      <td data-label="Day / Area"><a class="day-link" href="day-${esc(row.dayNumber)}.html"><strong>${esc(row.day)}</strong></a><br><span class="submitted-quote">${esc(row.weekday)} · ${esc(row.area)}</span></td>
      <td data-label="Item &amp; Draft Line">
        <span class="item-title">${esc(row.itemTitle)}</span>
        <span class="submitted-quote">Draft: "${esc(row.submittedLine)}"</span>
        ${row.verificationNotes ? `<div class="note-text">${esc(row.verificationNotes)}</div>` : ""}
      </td>
      ${cell("Location", row.verifiedLocation)}
      ${cell("Hours", row.verifiedHours)}
      ${cell("Open Days", row.verifiedOpenDays)}
      ${cell("Confirmed Cost", row.verifiedCost)}
      ${cell("Transit from Hotel", row.hotelTransit)}
      <td data-label="Status">${statusBadge(row.status)}${flagHtml}</td>
      <td data-label="Official Source"><a class="source-btn" href="${esc(row.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(row.officialSourceLabel)}</a></td>
    </tr>`;
      }
    )
    .join("\n");
}

function itemTable(list, tableId = "items-table") {
  return `<div class="table-wrap">
    <table class="data-table" id="${esc(tableId)}">
      <thead>
        <tr>
          <th>Day / Area</th>
          <th>Item &amp; Draft Line</th>
          <th>Official Location</th>
          <th>Official Hours</th>
          <th>Open / Closed</th>
          <th>Confirmed Cost</th>
          <th>Public Transit from Hotel</th>
          <th>Status</th>
          <th>Official Source</th>
        </tr>
      </thead>
      <tbody>
        ${renderItemRows(list)}
      </tbody>
    </table>
  </div>`;
}

function renderTransitRows(list) {
  return list
    .map(
      (tr) => `<tr id="transit-${esc(tr.id)}">
      <td data-label="Leg / Day"><strong>${esc(tr.id)}</strong><br><span class="submitted-quote">${esc(tr.day)}</span></td>
      <td data-label="Origin (Hotel / Hub)">${esc(tr.origin)}</td>
      <td data-label="Destination">${esc(tr.destination)}</td>
      <td data-label="Recommended Mode"><strong>${esc(tr.recommendedMode)}</strong></td>
      <td data-label="Step-by-Step Directions">${esc(tr.stepByStepRoute)}</td>
      ${cell("Verified Duration", tr.verifiedDuration)}
      ${cell("Verified Fare", tr.verifiedFare)}
      <td data-label="Official Source"><a class="source-btn" href="${esc(tr.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(tr.officialSourceLabel)}</a></td>
    </tr>`
    )
    .join("\n");
}

function transitTable(list, tableId = "transit-table") {
  return `<div class="table-wrap">
    <table class="data-table" id="${esc(tableId)}">
      <thead>
        <tr>
          <th>Leg / Day</th>
          <th>Origin (Hotel / Hub)</th>
          <th>Destination</th>
          <th>Recommended Public Transit Mode</th>
          <th>Step-by-Step Directions &amp; Station Exits</th>
          <th>Verified Duration</th>
          <th>Official Fare (KRW)</th>
          <th>Official Source</th>
        </tr>
      </thead>
      <tbody>
        ${renderTransitRows(list)}
      </tbody>
    </table>
  </div>`;
}

function renderFlagRows(list) {
  return list
    .map(
      (f) => `<tr id="${esc(f.flagCode)}">
      <td data-label="Flag ID"><strong>${esc(f.flagCode)}</strong><br>${statusBadge(f.severity)}</td>
      <td data-label="Affected Day">${esc(f.day)}</td>
      <td data-label="Submitted Text"><span class="submitted-quote">"${esc(f.submittedText)}"</span></td>
      <td data-label="Issue Type"><strong>${esc(f.issueType)}</strong></td>
      <td data-label="Official Finding">${esc(f.officialFinding)}</td>
      <td data-label="Traveler Action">${esc(f.actionRequired)}</td>
      <td data-label="Official Source"><a class="source-btn" href="${esc(f.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(f.officialSourceLabel)}</a></td>
    </tr>`
    )
    .join("\n");
}

function flagTable(list, tableId = "flags-table") {
  return `<div class="table-wrap">
    <table class="data-table" id="${esc(tableId)}">
      <thead>
        <tr>
          <th>Flag ID</th>
          <th>Affected Day</th>
          <th>Submitted Draft Text</th>
          <th>Irregularity Type</th>
          <th>Official Source Finding</th>
          <th>Recommended Traveler Action</th>
          <th>Official Source</th>
        </tr>
      </thead>
      <tbody>
        ${renderFlagRows(list)}
      </tbody>
    </table>
  </div>`;
}

function filterControls(includeDayFilter = true) {
  return `<div class="filter-bar">
    <input type="search" class="filter-input" data-table-search placeholder="Search venue, station, neighborhood, or note..." aria-label="Search itinerary rows">
    <select class="filter-select" data-status-filter aria-label="Filter by verification status">
      <option value="all">All Statuses</option>
      <option value="verified">Verified Only</option>
      <option value="flagged">All Flagged / Unverified</option>
      <option value="conflict">Conflicts Only</option>
      <option value="unverified">Unverified Blank Rows</option>
    </select>
    ${
      includeDayFilter
        ? `<select class="filter-select" data-day-filter aria-label="Filter by day">
      <option value="all">All 16 Days (Weeks 1 &amp; 2)</option>
      ${Array.from({ length: 16 }, (_, i) => i + 1)
        .map((n) => `<option value="Day ${n}">Day ${n}</option>`)
        .join("")}
    </select>`
        : ""
    }
    <span class="submitted-quote" data-row-count></span>
  </div>`;
}

function pageShell({ slug, title, subtitle, bodyHtml }) {
  const flaggedCount = irregularities.length;
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(title)} — Korea 16-Day Verified Trip Dashboard</title>
  <link rel="stylesheet" href="assets/styles.css">
  <script defer src="assets/app.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand-title" href="index.html">
          <span class="brand-k">KR</span>
          <span>Korea 16-Day Trip Dashboard <small>Week 1 Seoul (Myeongdong) · Week 2 Busan · Day 16 Hongdae · 2 Adults</small></span>
        </a>
        <div class="peer-links">
          <a href="../index.html">Root Hub</a> ·
          <a href="../portal/index.html">/portal/</a> ·
          <a href="../complete/index.html">/complete/</a> ·
          <a href="../guide/index.html">/guide/</a> ·
          <a href="../verified/index.html">/verified/</a>
        </div>
      </div>
      <nav class="main-nav" aria-label="Category navigation">
        ${NAV_ITEMS.map((nav) => {
          const isActive = nav.slug === slug ? " active" : "";
          const flagBadge = nav.flagged ? ` <span class="flag-pill">${flaggedCount}</span>` : "";
          return `<a class="nav-link${isActive}${nav.flagged ? " nav-flagged" : ""}" href="${nav.slug}">${esc(nav.label)}${flagBadge}</a>`;
        }).join("")}
      </nav>
    </div>
  </header>
  <main class="container">
    <section class="page-hero">
      <h1>${esc(title)}</h1>
      <p>${esc(subtitle)}</p>
    </section>
    ${bodyHtml}
  </main>
  <footer class="site-footer">
    <p><strong>Zero-Inference Verification Policy:</strong> Every table row links directly to an official government, transit, or primary brand source. Unconfirmed values are left blank (empty cells) and published on <a href="flagged-for-review.html">Flagged for Review</a>.</p>
  </footer>
</body>
</html>`;
}

// Copy & enhance styles + interactive filter script in full-itinerary/assets/
const baseCss = fs.readFileSync(path.join(ROOT, "assets/portal-2a9f9e6e.css"), "utf8");
const extraCss = `
.brand-k {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.45rem;
  background: #1d4ed8;
  color: #fff;
  font-weight: 800;
  margin-right: 0.5rem;
}
.brand-title {
  display: inline-flex;
  align-items: center;
  text-decoration: none;
  color: #0f172a;
  font-weight: 700;
  font-size: 1.05rem;
}
.brand-title small {
  display: block;
  font-size: 0.78rem;
  font-weight: 500;
  color: #475569;
}
.peer-links {
  font-size: 0.8rem;
  color: #475569;
}
.peer-links a {
  color: #1d4ed8;
  text-decoration: none;
}
.flag-pill {
  background: #dc2626;
  color: #fff;
  border-radius: 999px;
  padding: 0.08rem 0.45rem;
  font-size: 0.72rem;
  margin-left: 0.25rem;
}
.day-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 0.75rem;
  margin-top: 0.85rem;
}
.day-tile {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.65rem;
  background: #ffffff;
  text-decoration: none;
  color: #0f172a;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.day-tile:hover, .day-tile.active-day-card {
  border-color: #1d4ed8;
  box-shadow: 0 2px 8px rgba(29, 78, 216, 0.14);
  background: #f8fafc;
}
.day-tile-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3rem;
}
.day-num {
  font-weight: 800;
  color: #1d4ed8;
  font-size: 0.95rem;
}
.day-week-tag {
  font-size: 0.7rem;
  padding: 0.12rem 0.45rem;
  border-radius: 999px;
  background: #e2e8f0;
  color: #334155;
  font-weight: 600;
}
.day-tile-weekday {
  font-size: 0.78rem;
  color: #475569;
  margin-bottom: 0.25rem;
}
.day-tile-title {
  font-size: 0.88rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 0.4rem;
}
.day-tile-meta {
  font-size: 0.74rem;
  color: #64748b;
}
.day-pill-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 0.38rem;
  margin: 0.85rem 0 1.15rem;
  padding: 0.65rem;
  background: #f1f5f9;
  border-radius: 0.65rem;
}
.day-pill {
  padding: 0.34rem 0.65rem;
  border-radius: 999px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #1e293b;
  text-decoration: none;
  font-size: 0.78rem;
  font-weight: 600;
}
.day-pill.active, .day-pill:hover {
  background: #1d4ed8;
  border-color: #1d4ed8;
  color: #ffffff;
}
.day-nav-buttons {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin: 1rem 0;
}
.day-link {
  color: #1d4ed8;
  text-decoration: none;
}
.day-link:hover {
  text-decoration: underline;
}
`;
fs.writeFileSync(path.join(ASSETS_DIR, "styles.css"), baseCss + "\n" + extraCss);
fs.copyFileSync(
  path.join(ROOT, "assets/portal-2a9f9e6e.js"),
  path.join(ASSETS_DIR, "app.js")
);

// 1. Build index.html (Dashboard)
const verifiedCount = items.filter((i) => i.status === "verified").length;
const indexBody = `
  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">PLANNED DURATION</div>
      <div class="kpi-value">16 Days (Weeks 1 &amp; 2)</div>
      <div class="kpi-sub">Days 1–8 Seoul · Days 9–15 Busan · Day 16 Hongdae</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">AUDITED LINE ITEMS</div>
      <div class="kpi-value">${items.length} Rows</div>
      <div class="kpi-sub">${verifiedCount} fully verified · ${items.length - verifiedCount} with flags/blanks</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">PLANNED HOTELS</div>
      <div class="kpi-value">${hotels.length} Stays</div>
      <div class="kpi-sub">Stanford Myeongdong · L7 Haeundae · Mercure Hongdae</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">HOTEL TRANSIT LEGS</div>
      <div class="kpi-value">${transitMatrix.length} Routes</div>
      <div class="kpi-sub">Subway exits, AREX, Bus 6015, KTX &amp; Busan transfers</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">FLAGGED FOR REVIEW</div>
      <div class="kpi-value">${irregularities.length} Flags</div>
      <div class="kpi-sub"><a href="flagged-for-review.html">View all conflicts &amp; blank items</a></div>
    </div>
  </div>

  <section class="alert-banner alert-critical">
    <strong>Top Schedule &amp; Transit Alerts to Know Before Departure:</strong>
    <ul>
      <li><strong>Day 3 (Tuesday Nov 3) — Gyeongbokgung Palace is CLOSED on Tuesdays:</strong> Swap Day 3 and Day 4 (Wednesday Seongsu/DDP) so you visit Gyeongbokgung and the 10:00/14:00 Royal Guard Ceremony on Wednesday.</li>
      <li><strong>Day 10 (Tuesday Nov 10) — Haeundae Sky Capsule Tickets Are Sold One-Way Only:</strong> Book Mipo &rarr; Cheongsapo in advance on <a href="https://www.bluelinepark.com/eng/" target="_blank" rel="noopener noreferrer">bluelinepark.com</a>, walk 5–8 min to Cheongsapo Daritdol Observatory, and return via the Haeundae Beach Train, a second one-way capsule, or Village Bus Haeundae-gu 2.</li>
      <li><strong>Day 10 (#7) &amp; Day 12 (#2) — BUSAN X the SKY Scheduled Twice:</strong> Keep either the Day 10 late-afternoon slot (3 min walk from Mipo Station) OR the Day 12 10:00 AM slot before SEA LIFE Busan Aquarium.</li>
      <li><strong>Day 11 — Nampo-dong Backtracking Fix:</strong> BIFF Square &amp; Jagalchi Fish Market are listed both before (#5–#6) and after (#10) Songdo Beach. Visit Gamcheon &rarr; Songdo Beach/Cloud Trails/Cable Car &rarr; BIFF Square, Jagalchi Market, Gukje Market &amp; Nampo-dong in one continuous loop.</li>
      <li><strong>Day 16 — Seoul Station to Hongdae AREX Boarding Rule:</strong> Board the <strong>AREX All-Stop Train (B3)</strong> (2 stops, ~7 min, 1,550 KRW) to Hongik Univ. Station — do NOT board the AREX Express Train, which runs nonstop to Incheon Airport and skips Hongdae! Use <strong>Hongik Univ. Station Exit 8 (elevator)</strong> with luggage for Mercure Ambassador Seoul Hongdae.</li>
    </ul>
  </section>

  ${dayPickerGrid(null)}

  <section class="section-card">
    <div class="section-header">
      <div>
        <h2>Complete 16-Day Line-by-Line Verified Schedule (${items.length} Sourced Rows)</h2>
        <p class="section-subtitle">Search or filter by day (Day 1–Day 16) or verification status. Unconfirmed values are strictly left blank.</p>
      </div>
    </div>
    ${filterControls(true)}
    ${itemTable(items, "dashboard-items-table")}
  </section>
`;

fs.writeFileSync(
  path.join(OUT_DIR, "index.html"),
  pageShell({
    slug: "index.html",
    title: "South Korea 16-Day Verified Itinerary Dashboard (Weeks 1 & 2)",
    subtitle: "Complete line-by-line verified travel plan for two adult travelers: Week 1 Seoul (Myeongdong) + Week 2 Busan (Haeundae, Gamcheon, Songdo, Nampo, Gwangalli) + Day 16 Return to Seoul (Hongdae).",
    bodyHtml: indexBody
  })
);

// 2. Build itinerary.html (All 16 Days)
const itineraryBody = `
  ${dayPillBar(null)}
  <section class="section-card">
    <div class="section-header">
      <div>
        <h2>Master 16-Day Itinerary Table (Days 1–16)</h2>
        <p class="section-subtitle">Click any Day label to open its standalone mobile day guide, or use the filters below.</p>
      </div>
    </div>
    ${filterControls(true)}
    ${itemTable(items, "all-days-table")}
  </section>
`;
fs.writeFileSync(
  path.join(OUT_DIR, "itinerary.html"),
  pageShell({
    slug: "itinerary.html",
    title: "All 16 Days Itinerary (Week 1 Seoul & Week 2 Busan -> Hongdae)",
    subtitle: "Every submitted line item across Days 1–16 verified against official government, transit, and operator sources.",
    bodyHtml: itineraryBody
  })
);

// 3. Build individual Day pages: day-1.html .. day-16.html
for (const d of DAY_META) {
  const dayItems = items.filter((i) => i.dayNumber === d.dayNumber);
  const prevDay = d.dayNumber > 1 ? d.dayNumber - 1 : null;
  const nextDay = d.dayNumber < 16 ? d.dayNumber + 1 : null;
  const dayFlagCodes = new Set(dayItems.map((i) => i.flagCode).filter(Boolean));
  const dayFlags = irregularities.filter(
    (f) => dayFlagCodes.has(f.flagCode) || f.day.includes(`Day ${d.dayNumber}`)
  );
  const dayTransit = transitMatrix.filter(
    (t) =>
      t.day.includes(`Day ${d.dayNumber}`) ||
      (d.dayNumber <= 8 && t.id === "TR-00") ||
      (d.dayNumber >= 9 && d.dayNumber <= 16 && t.id === "TR-13")
  );

  const dayBody = `
    ${dayPillBar(d.dayNumber)}
    <div class="day-nav-buttons">
      ${
        prevDay
          ? `<a class="source-btn" href="day-${prevDay}.html">&larr; Previous: Day ${prevDay}</a>`
          : `<a class="source-btn" href="index.html">&larr; Back to Dashboard</a>`
      }
      <a class="source-btn" href="itinerary.html">All 16 Days Table</a>
      ${
        nextDay
          ? `<a class="source-btn" href="day-${nextDay}.html">Next: Day ${nextDay} &rarr;</a>`
          : `<a class="source-btn" href="flagged-for-review.html">Flagged for Review &rarr;</a>`
      }
    </div>

    <section class="section-card">
      <div class="kpi-grid">
        <div class="kpi-card">
          <div class="kpi-label">DAY &amp; WEEKDAY</div>
          <div class="kpi-value">Day ${d.dayNumber} · ${esc(d.weekday)}</div>
          <div class="kpi-sub">${esc(d.dateLabel)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">CITY / REGION</div>
          <div class="kpi-value">${esc(d.city)}</div>
          <div class="kpi-sub">${esc(d.week)}</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">PLANNED HOTEL BASE</div>
          <div class="kpi-value">${esc(d.hotel)}</div>
          <div class="kpi-sub"><a href="stays.html">View hotel check-in &amp; exit guide</a></div>
        </div>
      </div>
      <p style="margin-top:0.75rem;"><strong>Day ${d.dayNumber} Overview:</strong> ${esc(d.summary)}</p>
    </section>

    <section class="section-card">
      <h2>Day ${d.dayNumber} Verified Line Items (${dayItems.length} Row${dayItems.length === 1 ? "" : "s"})</h2>
      ${itemTable(dayItems, `day-${d.dayNumber}-items`)}
    </section>

    <section class="section-card">
      <h2>Day ${d.dayNumber} Public Transit Routes &amp; Pass Rules</h2>
      ${transitTable(dayTransit, `day-${d.dayNumber}-transit`)}
    </section>

    ${
      dayFlags.length > 0
        ? `<section class="section-card">
      <h2>Flagged Irregularities &amp; Verification Notes for Day ${d.dayNumber}</h2>
      ${flagTable(dayFlags, `day-${d.dayNumber}-flags`)}
    </section>`
        : ""
    }
  `;

  fs.writeFileSync(
    path.join(OUT_DIR, `day-${d.dayNumber}.html`),
    pageShell({
      slug: "itinerary.html",
      title: `Day ${d.dayNumber} (${d.weekday}): ${d.title}`,
      subtitle: `${d.week} · ${d.dateLabel} · Base: ${d.hotel}`,
      bodyHtml: dayBody
    })
  );
}

// 4. Build stays.html (All 3 Hotels)
const stayItems = items.filter((i) => i.category === "stays");
const staysBody = `
  <section class="section-card">
    <h2>Planned Hotels Across Seoul &amp; Busan (3 Official Properties)</h2>
    <p class="section-subtitle">Official addresses, check-in/check-out windows, luggage-friendly subway exits, and taxi/airport transfer instructions.</p>
    <div class="table-wrap">
      <table class="data-table" id="hotels-summary-table">
        <thead>
          <tr>
            <th>Hotel Name</th>
            <th>City &amp; Stay Window</th>
            <th>Official Street Address &amp; Lobby Floor</th>
            <th>Official Check-In</th>
            <th>Official Check-Out</th>
            <th>Nearest Subway / Airport Bus Exit</th>
            <th>Luggage &amp; Taxi Notes</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          ${hotels
            .map(
              (h) => `<tr id="${esc(h.id)}">
            <td data-label="Hotel Name"><strong>${esc(h.name)}</strong></td>
            <td data-label="City &amp; Stay Window">${esc(h.city)}<br><span class="submitted-quote">${esc(h.days)}</span></td>
            <td data-label="Address">${esc(h.address)}</td>
            <td data-label="Check-In">${esc(h.checkIn)}</td>
            <td data-label="Check-Out">${esc(h.checkOut)}</td>
            <td data-label="Nearest Transit">${esc(h.nearestTransit)}</td>
            <td data-label="Luggage Notes">${esc(h.luggageNotes)}</td>
            <td data-label="Official Source"><a class="source-btn" href="${esc(h.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(h.officialSourceLabel)}</a></td>
          </tr>`
            )
            .join("\n")}
        </tbody>
      </table>
    </div>
  </section>

  <section class="section-card">
    <h2>Itinerary Check-In / Check-Out Line Items</h2>
    ${itemTable(stayItems, "stays-items-table")}
  </section>
`;
fs.writeFileSync(
  path.join(OUT_DIR, "stays.html"),
  pageShell({
    slug: "stays.html",
    title: "Planned Hotels & Check-In / Check-Out Guide (3 Properties)",
    subtitle: "Stanford Hotel Myeongdong (Days 1–9), L7 HAEUNDAE by LOTTE (Days 9–16), and Mercure Ambassador Seoul Hongdae (Day 16).",
    bodyHtml: staysBody
  })
);

// 5. Build transit.html (24-Leg Public Transit Matrix + Transit Rows)
const transitItems = items.filter((i) => i.category === "transit");
const transitBody = `
  <section class="section-card">
    <h2>Door-to-Door Hotel Public-Transit Matrix (${transitMatrix.length} Verified Legs)</h2>
    <p class="section-subtitle">Exact subway lines, bus numbers, station exits, transfer rules, and official KRW fares from Stanford Hotel Myeongdong, L7 HAEUNDAE by LOTTE, and Mercure Ambassador Seoul Hongdae.</p>
    ${transitTable(transitMatrix, "master-transit-matrix")}
  </section>

  <section class="section-card">
    <h2>Submitted Transit Line Items (Days 1–16)</h2>
    ${filterControls(true)}
    ${itemTable(transitItems, "transit-items-table")}
  </section>
`;
fs.writeFileSync(
  path.join(OUT_DIR, "transit.html"),
  pageShell({
    slug: "transit.html",
    title: "Public Transportation Playbook & Hotel Route Matrix",
    subtitle: "Step-by-step subway, bus, AREX, Sky Capsule, and KTX directions connecting all three planned hotels across Seoul and Busan.",
    bodyHtml: transitBody
  })
);

// 6. Build attractions.html, dining.html, shopping.html
const attractionItems = items.filter((i) => i.category === "attractions");
fs.writeFileSync(
  path.join(OUT_DIR, "attractions.html"),
  pageShell({
    slug: "attractions.html",
    title: "Attractions, Palaces, Observatories, Skywalks & Beaches (Weeks 1 & 2)",
    subtitle: `${attractionItems.length} attraction entries verified for operating hours, closed days, admission fees, and public transit access.`,
    bodyHtml: `<section class="section-card">
      <h2>Verified Attractions &amp; Sightseeing (${attractionItems.length} Rows)</h2>
      ${filterControls(true)}
      ${itemTable(attractionItems, "attractions-table")}
    </section>`
  })
);

const diningItems = items.filter((i) => i.category === "dining");
fs.writeFileSync(
  path.join(OUT_DIR, "dining.html"),
  pageShell({
    slug: "dining.html",
    title: "Dining, Restaurants, Cafes, Bakeries, Tea Houses & Bars (Weeks 1 & 2)",
    subtitle: `${diningItems.length} dining and cafe entries audited line-by-line. Unconfirmed private business hours/prices are left blank and flagged.`,
    bodyHtml: `<section class="section-card">
      <h2>Verified Dining, Cafes &amp; Nightlife (${diningItems.length} Rows)</h2>
      ${filterControls(true)}
      ${itemTable(diningItems, "dining-table")}
    </section>`
  })
);

const shoppingItems = items.filter((i) => i.category === "shopping");
fs.writeFileSync(
  path.join(OUT_DIR, "shopping.html"),
  pageShell({
    slug: "shopping.html",
    title: "Shopping Districts, Department Stores & Traditional Markets (Weeks 1 & 2)",
    subtitle: `${shoppingItems.length} shopping and market entries across Seoul (Myeongdong, Seongsu, COEX, Insadong) and Busan (Haeundae Market, BIFF Square, Jagalchi, Gukje, Nampo-dong).`,
    bodyHtml: `<section class="section-card">
      <h2>Verified Shopping &amp; Markets (${shoppingItems.length} Rows)</h2>
      ${filterControls(true)}
      ${itemTable(shoppingItems, "shopping-table")}
    </section>`
  })
);

// 7. Build analysis.html (Analysis, Schedule Optimization & Official KRW Costs)
const costRows = items.filter((i) => i.verifiedCost && i.verifiedCost.trim() !== "");
const analysisBody = `
  <section class="section-card">
    <h2>Key Schedule &amp; Route Analysis (Weeks 1 &amp; 2)</h2>
    <div class="table-wrap">
      <table class="data-table" id="schedule-analysis-table">
        <thead>
          <tr>
            <th>Topic / Day</th>
            <th>Submitted Plan</th>
            <th>Official Verification Finding</th>
            <th>Recommended Fix for 2 Travelers</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td data-label="Topic"><strong>Calendar Alignment (Days 1–16)</strong></td>
            <td data-label="Submitted Plan">Oct.31/Nov 1 (Sun), Nov 2,2006 (Mon) ... Nov 9 (Mon), Days 10–16 (Tue–Mon)</td>
            <td data-label="Finding">Nov 2, 2006 was a Thursday. Every weekday in the 16-day plan (Sun Nov 1 through Mon Nov 16) aligns with <strong>November 2026</strong>.</td>
            <td data-label="Recommended Fix">Confirm 2026 travel year; Week 1 = Nov 1–9, 2026; Week 2 = Nov 9–16, 2026.</td>
            <td data-label="Official Source"><a class="source-btn" href="https://english.visitkorea.or.kr/" target="_blank" rel="noopener noreferrer">VisitKorea Official</a></td>
          </tr>
          <tr>
            <td data-label="Topic"><strong>Day 3 Tuesday Closure Blocker</strong></td>
            <td data-label="Submitted Plan">Day 3 (Tuesday Nov 3): Gyeongbokgung Palace + Guard Ceremony + Cha Masineun Tteul</td>
            <td data-label="Finding">Gyeongbokgung Palace, the Royal Guard Changing Ceremony, and Cha Masineun Tteul Tea House are all <strong>CLOSED on Tuesdays</strong>.</td>
            <td data-label="Recommended Fix">Swap Day 3 (Tuesday) with Day 4 (Wednesday Seongsu-dong &amp; DDP).</td>
            <td data-label="Official Source"><a class="source-btn" href="https://royal.khs.go.kr/ENG/contents/E101010000.do" target="_blank" rel="noopener noreferrer">Korea Heritage Service</a></td>
          </tr>
          <tr>
            <td data-label="Topic"><strong>Day 10 Sky Capsule &amp; Daritdol Skywalk</strong></td>
            <td data-label="Submitted Plan">Take Sky Capsule toward Cheongsapo. Book round trip tickets. If not, walk Cheongsapo Daritdol Observatory.</td>
            <td data-label="Finding">Sky Capsule tickets are sold <strong>one-way only</strong> per cabin. Daritdol Observatory is a free glass skywalk 5–8 min from Cheongsapo Station (not a walk back to Haeundae).</td>
            <td data-label="Recommended Fix">Book one-way Sky Capsule (Mipo &rarr; Cheongsapo), walk 5–8 min to Daritdol Observatory, and return via Beach Train or Bus Haeundae-gu 2.</td>
            <td data-label="Official Source"><a class="source-btn" href="https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=34413" target="_blank" rel="noopener noreferrer">VisitKorea Blueline Park</a></td>
          </tr>
          <tr>
            <td data-label="Topic"><strong>Day 10 &amp; Day 12 Duplicate BUSAN X the SKY</strong></td>
            <td data-label="Submitted Plan">Listed on Day 10 #7 (optional, $17.59 on Klook) and Day 12 #2 (10:00–11:30 AM).</td>
            <td data-label="Finding">Official adult ticket counter price is <strong>29,000 KRW</strong> (10:00–21:00 daily). Listed twice across Day 10 and Day 12.</td>
            <td data-label="Recommended Fix">Visit once — either on Day 12 morning before SEA LIFE Aquarium (32,000 KRW) or on Day 10 late afternoon next to Mipo Station.</td>
            <td data-label="Official Source"><a class="source-btn" href="https://english.visitkorea.or.kr/svc/whereToGo/locIntrdn/rgnContentsView.do?vcontsId=33642" target="_blank" rel="noopener noreferrer">VisitKorea BUSAN X the SKY</a></td>
          </tr>
          <tr>
            <td data-label="Topic"><strong>Day 11 Nampo-dong / Songdo Backtracking</strong></td>
            <td data-label="Submitted Plan">Gamcheon &rarr; #5 BIFF Square &amp; #6 Jagalchi &rarr; #7–9 Songdo Beach/Skywalk/Cable Car &rarr; #10 Jagalchi, BIFF Square, Gukje Market &amp; Nampo-dong.</td>
            <td data-label="Finding">BIFF Square and Jagalchi Market are visited twice on Day 11, forcing an extra round-trip bus ride between Nampo-dong and Songdo Beach.</td>
            <td data-label="Recommended Fix">Go Gamcheon &rarr; Songdo Beach, Cloud Trails &amp; Cable Car &rarr; BIFF Square, Jagalchi Market, Gukje Market &amp; Nampo-dong once.</td>
            <td data-label="Official Source"><a class="source-btn" href="https://english.visitkorea.or.kr/enu/TRV/TV_ENG_3_7.jsp?cid=2364630" target="_blank" rel="noopener noreferrer">VisitKorea Busan Course</a></td>
          </tr>
          <tr>
            <td data-label="Topic"><strong>Day 16 Seoul Station &rarr; Hongdae AREX Transfer</strong></td>
            <td data-label="Submitted Plan">Take KTX to Seoul Station &rarr; Take AREX from Seoul Station to Hongik Univ. Station &rarr; 8 min walk to Mercure Ambassador Seoul Hongdae.</td>
            <td data-label="Finding">AREX Express skips Hongik Univ. Station; only the <strong>AREX All-Stop Train (B3)</strong> stops at Hongik Univ. Station (2 stops, ~7 min, 1,550 KRW). Exit 8 has an elevator for luggage.</td>
            <td data-label="Recommended Fix">Board AREX All-Stop at Seoul Station B3, exit at Hongik Univ. Station Exit 8 (elevator), and walk 4–5 min via the rear alley to Mercure Hongdae.</td>
            <td data-label="Official Source"><a class="source-btn" href="https://all.accor.com/hotel/B696/index.en.shtml" target="_blank" rel="noopener noreferrer">Accor Mercure Hongdae</a></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section class="section-card">
    <h2>Officially Confirmed Costs &amp; Fares (${costRows.length} Sourced Items)</h2>
    <p class="section-subtitle">Only official KRW fares and admission fees confirmed from primary sources are listed below; unconfirmed third-party USD quotes remain blank in the main dataset.</p>
    ${itemTable(costRows, "confirmed-costs-table")}
  </section>
`;
fs.writeFileSync(
  path.join(OUT_DIR, "analysis.html"),
  pageShell({
    slug: "analysis.html",
    title: "Itinerary Analysis, Route Optimization & Confirmed KRW Costs",
    subtitle: "Structural findings across Weeks 1 & 2, recommended day/route adjustments, and officially verified fares and admission fees.",
    bodyHtml: analysisBody
  })
);

// 8. Build flagged-for-review.html (and flagged.html alias)
const nonVerifiedItems = items.filter((i) => i.status !== "verified" || Boolean(i.flagCode));
const flaggedBody = `
  <section class="section-card">
    <h2>Master Register of Flagged Irregularities (${irregularities.length} Flags: FLG-01 to FLG-25)</h2>
    <p class="section-subtitle">Every schedule conflict, hours/fare discrepancy, duplicate block, spelling irregularity, and unverified item across Days 1–16 with direct links to official sources for manual review.</p>
    ${flagTable(irregularities, "master-flags-table")}
  </section>

  <section class="section-card">
    <h2>All Unverified, Partial &amp; Conflict Itinerary Rows (${nonVerifiedItems.length} Rows)</h2>
    <p class="section-subtitle">Any field that could not be confirmed from an official primary source is left strictly blank (empty cell) below.</p>
    ${filterControls(true)}
    ${itemTable(nonVerifiedItems, "flagged-items-table")}
  </section>
`;

const flaggedHtml = pageShell({
  slug: "flagged-for-review.html",
  title: "Flagged for Review — Conflicts, Unverified Items & Source Gaps",
  subtitle: `${irregularities.length} flagged irregularities and ${nonVerifiedItems.length} rows requiring confirmation across Week 1 (Seoul) and Week 2 (Busan & Hongdae).`,
  bodyHtml: flaggedBody
});

fs.writeFileSync(path.join(OUT_DIR, "flagged-for-review.html"), flaggedHtml);
fs.writeFileSync(path.join(OUT_DIR, "flagged.html"), flaggedHtml);

console.log(
  `Built full-itinerary/ site: 25 HTML pages (index, itinerary, 16 day pages day-1..day-16, stays, transit, attractions, dining, shopping, analysis, flagged-for-review, flagged).`
);
