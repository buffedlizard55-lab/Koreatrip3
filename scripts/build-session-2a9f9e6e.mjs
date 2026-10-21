import fs from "node:fs";
import path from "node:path";

const ROOT = process.cwd();
const PORTAL_DIR = path.join(ROOT, "portal");
fs.mkdirSync(PORTAL_DIR, { recursive: true });

const items = JSON.parse(
  fs.readFileSync(path.join(ROOT, "data/session-2a9f9e6e/verified-items.json"), "utf8")
);
const transitMatrix = JSON.parse(
  fs.readFileSync(path.join(ROOT, "data/session-2a9f9e6e/transit-matrix.json"), "utf8")
);
const irregularities = JSON.parse(
  fs.readFileSync(path.join(ROOT, "data/session-2a9f9e6e/flagged-irregularities.json"), "utf8")
);

const NAV_ITEMS = [
  { slug: "index.html", label: "Overview" },
  { slug: "itinerary.html", label: "Days 1–9 Itinerary" },
  { slug: "stays.html", label: "Hotels" },
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

function renderItemRows(list) {
  return list
    .map(
      (row) => `<tr id="item-${esc(row.id)}" data-filterable="1" data-status="${esc(row.status)}" data-day="Day ${esc(row.dayNumber)}">
      <td data-label="Day / Area"><strong>${esc(row.day)}</strong><br><span class="submitted-quote">${esc(row.weekday)} · ${esc(row.area)}</span></td>
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
      <td data-label="Status">${statusBadge(row.status)}${row.flagCode ? `<div class="submitted-quote">${esc(row.flagCode)}</div>` : ""}</td>
      <td data-label="Official Source"><a class="source-btn" href="${esc(row.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(row.officialSourceLabel)}</a></td>
    </tr>`
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
      <option value="all">All 9 Days</option>
      ${[1, 2, 3, 4, 5, 6, 7, 8, 9]
        .map((n) => `<option value="Day ${n}">Day ${n}</option>`)
        .join("")}
    </select>`
        : ""
    }
    <span class="submitted-quote" data-row-count></span>
  </div>`;
}

function pageShell({ slug, title, subtitle, bodyHtml, assetPrefix }) {
  const hasDocs = fs.existsSync(path.join(ROOT, "docs/index.html"));
  const hasTripGuide = fs.existsSync(path.join(ROOT, "docs/trip-guide/index.html"));
  const hasPages = fs.existsSync(path.join(ROOT, "pages/day-1.html"));
  const rootPrefix = assetPrefix === "./" ? "./" : "../";

  const peerLinks = [
    `<a href="${rootPrefix}index.html">Root Dashboard</a>`,
    `<a href="${rootPrefix}portal/index.html">Full Portal (/portal/)</a>`,
    hasDocs ? `<a href="${rootPrefix}docs/index.html">Data Tables (/docs/)</a>` : "",
    hasTripGuide ? `<a href="${rootPrefix}docs/trip-guide/index.html">Day-Swap Guide (/docs/trip-guide/)</a>` : "",
    hasPages ? `<a href="${rootPrefix}pages/day-1.html">Day Views (/pages/)</a>` : ""
  ]
    .filter(Boolean)
    .join(" · ");

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${esc(title)} — South Korea Trip Portal (Oct 31 – Nov 9, 2026)</title>
  <link rel="stylesheet" href="${assetPrefix}assets/portal-2a9f9e6e.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header">
    <div class="header-inner">
      <div class="brand-row">
        <a class="brand-title" href="index.html">
          <span class="brand-mark">KR</span>
          <span>Seoul &amp; Busan Verified Itinerary</span>
        </a>
        <span class="trip-meta-pill">2 Adults · SFO &rarr; ICN · Oct 31 – Nov 9, 2026</span>
      </div>
      <nav class="nav-bar" aria-label="Primary sections">
        ${NAV_ITEMS.map((nav) => {
          const isCurrent =
            nav.slug === slug ||
            (slug === "flagged.html" && nav.slug === "flagged-for-review.html") ||
            (slug === "food-shopping.html" && nav.slug === "shopping.html");
          return `<a href="${nav.slug}"${nav.flagged ? ' class="nav-flagged"' : ""}${
            isCurrent ? ' aria-current="page"' : ""
          }>${esc(nav.label)}</a>`;
        }).join("\n        ")}
      </nav>
    </div>
  </header>

  <main id="main-content" class="container">
    <section class="hero">
      <p class="eyebrow">Official Source Line-by-Line Verification</p>
      <h1>${esc(title)}</h1>
      <p>${esc(subtitle)}</p>
    </section>
    ${bodyHtml}
  </main>

  <footer class="site-footer">
    <div class="footer-inner">
      <div>
        <strong>Verification Standard:</strong> Every table row links directly to an official government, transit, or primary brand source. Unconfirmed fields remain blank and flagged <a href="flagged-for-review.html">Flagged for Review</a>.
      </div>
      <div>${peerLinks}</div>
    </div>
  </footer>
  <script src="${assetPrefix}assets/portal-2a9f9e6e.js" defer></script>
</body>
</html>
`;
}

// Compute counts from verified dataset
const totalItems = items.length;
const verifiedCount = items.filter((i) => i.status === "verified").length;
const conflictCount = items.filter((i) => i.status === "conflict" || i.status === "partial").length;
const unverifiedRows = items.filter(
  (i) => i.status === "unverified" || i.status === "needs_review"
);

// 1. Overview Page
function buildOverviewBody() {
  const daySummaryRows = [
    {
      day: "Day 1 · Sun Nov 1",
      plan: "Arrive ICN -> Airport Limousine Bus 6015 direct to Myeongdong -> Check in at Stanford Hotel Myeongdong (after 15:00)",
      transit: "Bus 6015 (17,000 KRW/adult; buy ticket at kiosk first)",
      status: "verified",
      note: "Zero stairs with luggage; 2-min flat walk to hotel 9F desk",
      label: "Airport Limousine 6015",
      url: "https://airportlimousine.co.kr/en/sub/sub01.php?cat_no=47"
    },
    {
      day: "Day 2 · Mon Nov 2",
      plan: "N Seoul Tower (Bus 01A/01B or Cable Car) -> Myeongdong Flagships -> Dinner BEFORE 19:30 -> Gwangjang Food Street",
      transit: "Shuttle 01A/01B (1,500 KRW) + Line 2 to Euljiro 4-ga (1,550 KRW)",
      status: "conflict",
      note: "Draft had '2006' typo, wrong 10:30 close, wrong Olive Young hours & relocated Myeongdong Kyoja HQ (129 Toegye-ro)",
      label: "N Seoul Tower Official",
      url: "https://www.nseoultower.co.kr/eng/visit/use.asp"
    },
    {
      day: "Day 3 · Tue Nov 3 (SWAP!)",
      plan: "CRITICAL: Gyeongbokgung is CLOSED TUESDAYS! Swap Day 3 <-> Day 4 so Wednesday covers Palace & Seongsu moves to Tuesday",
      transit: "Line 2 direct from Euljiro 1-ga -> DDP (205) -> Seongsu (211)",
      status: "critical",
      note: "Nov 3, 2026 is a regular Tuesday (not a public holiday) — Palace gates & Guard Ceremony are closed",
      label: "VisitKorea — Gyeongbokgung",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=87740"
    },
    {
      day: "Day 4 · Wed Nov 4 (SWAP!)",
      plan: "Cafe Onion Anguk (07:00) -> Gyeongbokgung Palace (09:00) & 10:00 Guard Ceremony -> Bukchon Hanok Village (10:00–17:00 curfew)",
      transit: "Line 2 -> Line 3 to Gyeongbokgung Stn Exit 5 (1,550 KRW)",
      status: "verified",
      note: "Respect Bukchon Red Zone 10:00–17:00 mandatory visiting window",
      label: "Visit Seoul — Bukchon Curfew",
      url: "https://english.visitseoul.net/attractions/Bukchon-Hanok-Village_/263"
    },
    {
      day: "Day 5 · Thu Nov 5",
      plan: "Starfield COEX Mall, Starfield Library & Gangnam Style Statue (East Gate Plaza)",
      transit: "Line 2 direct: Euljiro 1-ga -> Samseong Stn Exits 5 & 6 (1,650 KRW)",
      status: "verified",
      note: "'Soul Market' tenant in draft is unverified — left blank & flagged",
      label: "VisitKorea — Starfield COEX",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=73375"
    },
    {
      day: "Day 6 · Fri Nov 6",
      plan: "Ikseon-dong & Insadong: Rain Report Rainbow (10:30–20:30), Jayeondo Salt Bread & Ikseon Chwihyang",
      transit: "18-min walk OR Line 2 -> Line 3 to Jongno 3-ga Exit 4 (1,550 KRW)",
      status: "partial",
      note: "Draft listed 'Chwihyang' & 'Favorite of Ikseon' separately — they are the same restaurant",
      label: "Visit Seoul — Rain Report Rainbow",
      url: "https://english.visitseoul.net/restaurants/rainreport/ENP933ykf"
    },
    {
      day: "Day 7 · Sat Nov 7",
      plan: "Itaewon District (Open day — great fit for Day 2's Itaewon BBQ stop + Leeum / Noksapyeong stroll)",
      transit: "Line 4 Myeongdong -> Samgakji -> Line 6 Itaewon Stn (1,550 KRW)",
      status: "needs_review",
      note: "Submitted itinerary had header only with zero scheduled activities",
      label: "Seoul Metro Official",
      url: "http://www.seoulmetro.co.kr/en/page.do?menuIdx=348"
    },
    {
      day: "Day 8 · Sun Nov 8",
      plan: "Open / Unscheduled Seoul Day (Ideal overflow day for Mangwon Market + surplus Seongsu cafes)",
      transit: "Covered by 7-Day Climate Card unlimited Seoul pass (20,000 KRW)",
      status: "needs_review",
      note: "Note: General goods stores at Gwangjang close Sundays, while Food Street stays open daily",
      label: "VisitKorea — Climate Card",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140663"
    },
    {
      day: "Day 9 · Mon Nov 9",
      plan: "Check out 10:00 -> KTX Seoul Station to Busan Station -> L7 HAEUNDAE Check-In (15:00) -> Haeundae Beach & Market",
      transit: "KTX (~2h 15m–2h 50m) -> Busan Metro Line 1 -> Line 2 Haeundae Exit 5",
      status: "verified",
      note: "Pre-book KTX on korail.com; arrive at Seoul Station 20 min before departure (no ticket gates)",
      label: "LOTTE HOTELS — L7 Haeundae",
      url: "https://www.lottehotel.com/haeundae-l7/en"
    }
  ];

  return `
  <div class="alert-banner" role="region" aria-label="Critical itinerary alerts">
    <h2>Immediate Action Items Before Booking</h2>
    <ul>
      <li><strong>Swap Tuesday Nov 3 &amp; Wednesday Nov 4:</strong> Gyeongbokgung Palace &amp; the Royal Guard Ceremony are <strong>closed every Tuesday</strong> (Nov 3, 2026 is not a public holiday). Visit DDP + Seongsu on Tuesday and Gyeongbokgung + Bukchon on Wednesday.</li>
      <li><strong>Myeongdong Kyoja Relocated in 2026:</strong> Official <a href="http://mdkj.co.kr/en/restaurant/head.php" target="_blank" rel="noopener noreferrer">mdkj.co.kr</a> confirms the Main Headquarters moved in 2026 to <strong>129 Toegye-ro, Jung-gu</strong> (Michelin Guide still shows old 29 Myeongdong 10-gil).</li>
      <li><strong>Hours &amp; Curfew Corrections:</strong> N Seoul Tower Observatory is open until <strong>22:30</strong> weekdays / <strong>23:00</strong> weekends (Cable Car <strong>10:00–23:00</strong>, not 10:30 AM); Olive Young Global Town is <strong>10:00–22:30</strong>; Crystal Jade Shinsegae B1 closes <strong>20:00</strong> Mon–Fri; Bukchon Red Zone restricts tourists strictly to <strong>10:00–17:00</strong>.</li>
      <li><strong>Transit Pass Strategy (2 Adults):</strong> Buy two <strong>7-Day Seoul Climate Cards</strong> (3,000 KRW card + 20,000 KRW pass = 23,000 KRW/person unlimited Seoul subways &amp; buses for Days 2–8) plus <strong>T-money cards</strong> for Busan on Day 9.</li>
    </ul>
  </div>

  <div class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Audited Lines</div>
      <div class="kpi-value">${totalItems}</div>
      <div class="kpi-sub">Every line across Days 1–9 checked against primary sources</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Verified Clean</div>
      <div class="kpi-value">${verifiedCount}</div>
      <div class="kpi-sub">Official address, hours, open days &amp; transit confirmed</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Conflicts &amp; Alerts</div>
      <div class="kpi-value">${conflictCount}</div>
      <div class="kpi-sub">Closed day, hours errors, 2026 relocation &amp; fare mismatches</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Unverified Blank Rows</div>
      <div class="kpi-value">${unverifiedRows.length}</div>
      <div class="kpi-sub">Unconfirmed values kept strictly blank — see <a href="flagged-for-review.html">Flagged for Review</a></div>
    </div>
  </div>

  <section class="section-card">
    <div class="section-header">
      <h2>9-Day Master Plan &amp; Recommended Day Swap</h2>
      <p class="section-sub">Two adult travelers · Seoul (Nights 1–8) &rarr; Busan (Night 9)</p>
    </div>
    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>Day &amp; Date (2026)</th>
            <th>Recommended Route</th>
            <th>Public Transit Plan</th>
            <th>Audit Status</th>
            <th>Key Finding</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          ${daySummaryRows
            .map(
              (r) => `<tr>
            <td data-label="Day &amp; Date"><strong>${esc(r.day)}</strong></td>
            <td data-label="Recommended Route">${esc(r.plan)}</td>
            <td data-label="Public Transit">${esc(r.transit)}</td>
            <td data-label="Audit Status">${statusBadge(r.status)}</td>
            <td data-label="Key Finding">${esc(r.note)}</td>
            <td data-label="Official Source"><a class="source-btn" href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">${esc(r.label)}</a></td>
          </tr>`
            )
            .join("\n")}
        </tbody>
      </table>
    </div>
  </section>

  <section class="section-card">
    <div class="section-header">
      <h2>Quick Navigation by Category</h2>
      <p class="section-sub">Jump directly to verified tables, transit routes, or flagged review items</p>
    </div>
    <div class="cards-grid">
      <div class="info-card">
        <h3><a href="itinerary.html">Complete Line-by-Line Itinerary</a></h3>
        <p>All ${totalItems} rows from Days 1–9 with instant search, day jump anchors, official hours, blank unconfirmed cells, and official links.</p>
      </div>
      <div class="info-card">
        <h3><a href="transit.html">Public Transit &amp; Hotel Routing</a></h3>
        <p>ICN Airport Limousine 6015 vs AREX, 7-Day Climate Card + T-money setup, exact subway exits from both hotels, and KTX Seoul&rarr;Busan guide.</p>
      </div>
      <div class="info-card">
        <h3><a href="stays.html">Hotels &amp; Check-In Logistics</a></h3>
        <p>Stanford Hotel Myeongdong (84 Namdaemun-ro, 9F Reception) and L7 HAEUNDAE by LOTTE (55 Haeun-daero 570beon-gil, 3F Reception).</p>
      </div>
      <div class="info-card">
        <h3><a href="flagged-for-review.html">Flagged for Review (${irregularities.length} Flags + ${unverifiedRows.length} Unverified)</a></h3>
        <p>Complete audit log of Tuesday palace closure, hours conflicts, duplicate venues, year typo, and every blank unverified cell.</p>
      </div>
    </div>
  </section>`;
}

// 2. Full Day-by-Day Itinerary Page
function buildItineraryBody() {
  const daySections = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    .map((dayNum) => {
      const dayItems = items.filter((x) => x.dayNumber === dayNum);
      const first = dayItems[0];
      return `<section class="section-card" id="day-${dayNum}">
        <div class="section-header">
          <h2>Day ${dayNum}: ${esc(first ? first.weekday : "")} (Draft Date: ${esc(first ? first.submittedDate : "")})</h2>
          <p class="section-sub">${esc(first ? `${first.city} · ${dayItems.length} item(s)` : "")}</p>
        </div>
        ${itemTable(dayItems, `day-${dayNum}-table`)}
      </section>`;
    })
    .join("\n");

  return `
  <div class="day-jump-strip" aria-label="Jump to day">
    ${[1, 2, 3, 4, 5, 6, 7, 8, 9]
      .map((d) => `<a href="#day-${d}">Day ${d}</a>`)
      .join("")}
  </div>
  ${filterControls(true)}
  ${daySections}`;
}

// 3. Stays Page
function buildStaysBody() {
  const hotelRows = items.filter((i) => i.category === "hotel");
  return `
  <section class="section-card">
    <div class="section-header">
      <h2>Confirmed Hotel Bases (Seoul &amp; Busan)</h2>
      <p class="section-sub">All public transit directions across this site originate from these two properties</p>
    </div>
    <div class="cards-grid">
      <div class="info-card">
        <h3>Stanford Hotel Myeongdong (Seoul · Nights 1–8)</h3>
        <p>Central Line 2 &amp; Airport Bus hub at the entrance to Myeongdong and Lotte Main Store.</p>
        <dl>
          <dt>Address</dt><dd>84 Namdaemun-ro, Jung-gu, Seoul (Check-in on 9F)</dd>
          <dt>Check-In / Out</dt><dd>Check-in from 15:00 · Check-out until 12:00</dd>
          <dt>Subway</dt><dd>Line 2 Euljiro 1(il)-ga Station Exits 5 &amp; 6 (2-min flat walk)</dd>
          <dt>Airport Bus</dt><dd>Route 6015 stop "Lotte Hotel / IBIS Myeong-dong" (17,000 KRW)</dd>
          <dt>Official Site</dt><dd><a href="https://stanford.webhelper.co.kr/myeongdong/en/room/view/12" target="_blank" rel="noopener noreferrer">Stanford Hotel Myeongdong</a></dd>
        </dl>
      </div>
      <div class="info-card">
        <h3>L7 HAEUNDAE by LOTTE HOTELS (Busan · Night 9)</h3>
        <p>Steps from both Haeundae Beach sand and Haeundae Traditional Market food alley.</p>
        <dl>
          <dt>Address</dt><dd>55 Haeun-daero 570beon-gil, Haeundae-gu, Busan (Check-in on 3F)</dd>
          <dt>Check-In / Out</dt><dd>Check-in 15:00 · Check-out 11:00</dd>
          <dt>Subway</dt><dd>Busan Metro Line 2 Haeundae Station Exit 5 (5-min flat walk along Gunam-ro)</dd>
          <dt>Official Site</dt><dd><a href="https://www.lottehotel.com/haeundae-l7/en" target="_blank" rel="noopener noreferrer">LOTTE HOTELS — L7 Haeundae</a></dd>
        </dl>
      </div>
    </div>
  </section>
  <section class="section-card">
    <div class="section-header">
      <h2>Hotel Verification Records</h2>
      <p class="section-sub">Check-in, check-out, address &amp; transit audit</p>
    </div>
    ${itemTable(hotelRows, "stays-table")}
  </section>`;
}

// 4. Transit Page
function buildTransitBody() {
  const transitItems = items.filter((i) => i.category === "transit");
  return `
  <section class="section-card">
    <div class="section-header">
      <h2>Hotel-to-Destination Public Transit Matrix (2 Adults)</h2>
      <p class="section-sub">Official fares, exact lines/exits, and luggage-friendly recommendations</p>
    </div>
    <div class="table-wrap">
      <table class="data-table" id="transit-matrix-table">
        <thead>
          <tr>
            <th>Leg / Day</th>
            <th>Origin &rarr; Destination</th>
            <th>Recommended Transit Mode</th>
            <th>Step-by-Step Exits &amp; Transfers</th>
            <th>Verified Duration</th>
            <th>Fare (1 Adult)</th>
            <th>Fare (2 Adults)</th>
            <th>Status</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          ${transitMatrix
            .map(
              (leg) => `<tr id="${esc(leg.legId)}">
            <td data-label="Leg / Day"><strong>${esc(leg.legId)}</strong><br><span class="submitted-quote">${esc(leg.day)}</span></td>
            <td data-label="Origin -> Dest"><strong>${esc(leg.origin)}</strong> &rarr; ${esc(leg.destination)}${
              leg.notes ? `<div class="note-text">${esc(leg.notes)}</div>` : ""
            }</td>
            <td data-label="Mode">${esc(leg.recommendedMode)}</td>
            <td data-label="Step-by-Step">${esc(leg.stepByStep)}</td>
            ${cell("Duration", leg.duration)}
            ${cell("Fare (1 Adult)", leg.farePerAdult)}
            ${cell("Fare (2 Adults)", leg.fareTwoAdults)}
            <td data-label="Status">${statusBadge(leg.status)}</td>
            <td data-label="Official Source"><a class="source-btn" href="${esc(leg.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(leg.officialSourceLabel)}</a></td>
          </tr>`
            )
            .join("\n")}
        </tbody>
      </table>
    </div>
  </section>

  <section class="section-card">
    <div class="section-header">
      <h2>Submitted Transit Line Items (Line-by-Line Verification)</h2>
      <p class="section-sub">Comparing draft transit notes against official 2026 operator schedules</p>
    </div>
    ${itemTable(transitItems, "transit-items-table")}
  </section>`;
}

// 5. Category Page Builder
function buildCategoryBody(heading, sub, list) {
  return `
  ${filterControls(true)}
  <section class="section-card">
    <div class="section-header">
      <h2>${esc(heading)} (${list.length} Rows)</h2>
      <p class="section-sub">${esc(sub)}</p>
    </div>
    ${itemTable(list, "category-table")}
  </section>`;
}

// 6. Analysis & Confirmed Cost Floor Page
function buildAnalysisBody() {
  const confirmedCosts = [
    {
      item: "ICN -> Myeongdong Airport Limousine Bus 6015 (Recommended Arrival)",
      unit: "17,000 KRW / adult",
      twoAdults: "34,000 KRW",
      status: "verified",
      label: "Airport Limousine 6015",
      url: "https://airportlimousine.co.kr/en/sub/sub01.php?cat_no=47"
    },
    {
      item: "7-Day Seoul Climate Card Pass (Unlimited Seoul Subways + Buses Days 2–8)",
      unit: "23,000 KRW / adult (3,000 card + 20,000 load)",
      twoAdults: "46,000 KRW",
      status: "verified",
      label: "VisitKorea — Climate Card",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140663"
    },
    {
      item: "N Seoul Tower Observatory Ticket (Ages 13+)",
      unit: "29,000 KRW / adult",
      twoAdults: "58,000 KRW",
      status: "verified",
      label: "N Seoul Tower Official",
      url: "https://www.nseoultower.co.kr/eng/visit/use.asp"
    },
    {
      item: "Optional Namsan Cable Car Round-Trip (Skip if riding Bus 01A/01B on Climate Card)",
      unit: "15,000 KRW / adult",
      twoAdults: "30,000 KRW",
      status: "verified",
      label: "Namsan Cable Car Official",
      url: "http://www.cablecar.co.kr/eng/guide/fare.html"
    },
    {
      item: "Gyeongbokgung Palace Admission (Ages 19–64; move visit to Wednesday!)",
      unit: "3,000 KRW / adult",
      twoAdults: "6,000 KRW",
      status: "verified",
      label: "VisitKorea — Gyeongbokgung",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=87740"
    },
    {
      item: "Flights (SFO<->ICN), Hotel Room Rates, KTX Nov 9 Fare & Restaurant Menu Totals",
      unit: "",
      twoAdults: "",
      status: "unverified",
      label: "KORAIL Official Booking",
      url: "https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140656"
    }
  ];

  return `
  <section class="section-card">
    <div class="section-header">
      <h2>Pacing &amp; Logistics Analysis Across Days 1–9</h2>
      <p class="section-sub">Key structural findings from auditing the draft itinerary</p>
    </div>
    <div class="cards-grid">
      <div class="info-card">
        <h3>1. Calendar Year = 2026 (9/9 Weekday Match)</h3>
        <p>Every single weekday/date pair in the draft (Sun Nov 1 through Mon Nov 9) aligns exclusively with <strong>2026</strong>. Day 2's <code>Nov 2,2006</code> is a 1-digit typo (Nov 2, 2006 was a Thursday).</p>
      </div>
      <div class="info-card">
        <h3>2. Severe Front-Loading vs Empty Weekend</h3>
        <p><strong>Day 2 (14 entries)</strong> and <strong>Day 4 (16 entries)</strong> pack 58% of the entire trip into two days while <strong>Day 7 (Itaewon)</strong> and <strong>Day 8 (Sunday)</strong> have zero scheduled venues. Moving Itaewon BBQ + Mangwon Market + surplus cafes to Days 7–8 makes every day relaxed.</p>
      </div>
      <div class="info-card">
        <h3>3. Green Line 2 Advantage</h3>
        <p>Stanford Hotel Myeongdong sits 2 minutes from <strong>Euljiro 1(il)-ga (<code>202</code>)</strong>, putting Gwangjang (<code>204</code>), DDP (<code>205</code>), Seongsu (<code>211</code>), and COEX (<code>219</code>) on the exact same subway line with zero transfers.</p>
      </div>
    </div>
  </section>

  <section class="section-card">
    <div class="section-header">
      <h2>Confirmed Official Cost Floor (Strictly Non-Inferred KRW Figures)</h2>
      <p class="section-sub">Only officially published fixed fares/admissions are summed; variable or unconfirmed prices remain blank</p>
    </div>
    <div class="table-wrap">
      <table class="data-table" id="cost-floor-table">
        <thead>
          <tr>
            <th>Expense Item</th>
            <th>Confirmed Per Adult</th>
            <th>Confirmed for 2 Adults</th>
            <th>Status</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          ${confirmedCosts
            .map(
              (c) => `<tr>
            <td data-label="Expense Item"><strong>${esc(c.item)}</strong></td>
            ${cell("Per Adult", c.unit)}
            ${cell("2 Adults", c.twoAdults)}
            <td data-label="Status">${statusBadge(c.status)}</td>
            <td data-label="Official Source"><a class="source-btn" href="${esc(c.url)}" target="_blank" rel="noopener noreferrer">${esc(c.label)}</a></td>
          </tr>`
            )
            .join("\n")}
        </tbody>
      </table>
    </div>
  </section>`;
}

// 7. Flagged for Review Page
function buildFlaggedBody() {
  const allNonClean = items.filter((i) => i.status !== "verified");
  return `
  <section class="section-card">
    <div class="section-header">
      <h2>Part 1: Schedule Blockers, Hours/Fare Conflicts &amp; Structural Irregularities (${irregularities.length})</h2>
      <p class="section-sub">Every discrepancy between the submitted draft and official primary sources</p>
    </div>
    <div class="table-wrap">
      <table class="data-table" id="irregularities-table">
        <thead>
          <tr>
            <th>Flag ID</th>
            <th>Priority</th>
            <th>Day</th>
            <th>Item</th>
            <th>Submitted Draft Claim</th>
            <th>Official Verification Finding</th>
            <th>Recommended Action</th>
            <th>Official Source</th>
          </tr>
        </thead>
        <tbody>
          ${irregularities
            .map(
              (f) => `<tr id="${esc(f.flagId)}">
            <td data-label="Flag ID"><strong>${esc(f.flagId)}</strong></td>
            <td data-label="Priority">${statusBadge(f.severity)}</td>
            <td data-label="Day">${esc(f.day)}</td>
            <td data-label="Item"><strong>${esc(f.item)}</strong></td>
            <td data-label="Submitted Claim">${esc(f.submittedClaim)}</td>
            <td data-label="Official Finding">${esc(f.officialFinding)}</td>
            <td data-label="Action">${esc(f.recommendedAction)}</td>
            <td data-label="Official Source"><a class="source-btn" href="${esc(f.officialSourceUrl)}" target="_blank" rel="noopener noreferrer">${esc(f.officialSourceLabel)}</a></td>
          </tr>`
            )
            .join("\n")}
        </tbody>
      </table>
    </div>
  </section>

  <section class="section-card">
    <div class="section-header">
      <h2>Part 2: All Unverified &amp; Conflict Rows (${allNonClean.length} Rows — Unconfirmed Cells Left Blank)</h2>
      <p class="section-sub">Any address, operating hour, open day, or fare not explicitly confirmed on an official source is left strictly blank</p>
    </div>
    ${filterControls(true)}
    ${itemTable(allNonClean, "unverified-registry-table")}
  </section>`;
}

const PAGES = [
  {
    slug: "index.html",
    title: "South Korea Itinerary Dashboard (Oct 31 – Nov 9, 2026)",
    subtitle:
      "Line-by-line official verification, hotel-to-venue public transit directions, and schedule conflict review for two adult travelers in Seoul and Busan.",
    body: buildOverviewBody
  },
  {
    slug: "itinerary.html",
    title: "Complete Day-by-Day Verified Itinerary (Days 1–9)",
    subtitle:
      "Every submitted line item checked against official government, transit, and primary brand sources. Unconfirmed fields remain strictly blank.",
    body: buildItineraryBody
  },
  {
    slug: "stays.html",
    title: "Hotels & Base Logistics (Myeongdong & Haeundae)",
    subtitle:
      "Verified addresses, elevator lobby floors, check-in/check-out windows, and airport/rail links for Stanford Hotel Myeongdong and L7 HAEUNDAE by LOTTE.",
    body: buildStaysBody
  },
  {
    slug: "transit.html",
    title: "Public Transportation Guide & Fare Matrix",
    subtitle:
      "Step-by-step subway, bus, airport limousine, shuttle, and KTX directions from your hotels — calibrated for two adults.",
    body: buildTransitBody
  },
  {
    slug: "attractions.html",
    title: "Attractions, Palaces & Landmarks",
    subtitle:
      "Official opening hours, last-admission cutoffs, closed days, and ticket prices across Seoul and Busan landmarks.",
    body: () =>
      buildCategoryBody(
        "Attractions, Palaces & Sightseeing",
        "Official operating hours, closed days & admission fees",
        items.filter((i) => i.category === "attraction" || i.category === "open_day")
      )
  },
  {
    slug: "dining.html",
    title: "Dining, Bakeries, Cafes & Nightlife",
    subtitle:
      "Official restaurant hours, Myeongdong Kyoja's 2026 headquarters relocation alert, department-store closing cutoffs, and unverified indie spots.",
    body: () =>
      buildCategoryBody(
        "Restaurants, Bakeries, Cafes & Bars",
        "Official hours & locations; unverified independent venues left blank and flagged",
        items.filter((i) => i.category === "dining")
      )
  },
  {
    slug: "shopping.html",
    title: "Shopping, Flagships & Traditional Markets",
    subtitle:
      "Verified hours for Myeongdong flagships, Seongsu megastores, COEX Mall, and Gwangjang, Mangwon & Haeundae markets.",
    body: () =>
      buildCategoryBody(
        "Shopping Flagships & Traditional Markets",
        "Bring physical passports for instant tax-free VAT refund (>= 15,000 KRW)",
        items.filter((i) => i.category === "shopping")
      )
  },
  {
    slug: "food-shopping.html",
    title: "Combined Food, Cafes, Shopping & Markets",
    subtitle:
      "Unified table of all dining, bakery, flagship retail, and traditional market entries across Seoul and Busan.",
    body: () =>
      buildCategoryBody(
        "All Dining, Cafes, Shopping & Markets",
        "Combined category view with strict official verification links",
        items.filter((i) => i.category === "dining" || i.category === "shopping")
      )
  },
  {
    slug: "analysis.html",
    title: "Trip Analysis, Pacing Audit & Confirmed Costs",
    subtitle:
      "Day-load balancing, Green Line 2 transit efficiency, and non-inferred KRW cost floor for two adults.",
    body: buildAnalysisBody
  },
  {
    slug: "flagged-for-review.html",
    title: "Flagged for Review — Conflicts & Unverified Items",
    subtitle:
      "Every schedule blocker, operating-hour discrepancy, duplicate venue, date typo, and blank unverified field across Days 1–9.",
    body: buildFlaggedBody
  },
  {
    slug: "flagged.html",
    title: "Flagged for Review — Conflicts & Unverified Items",
    subtitle:
      "Every schedule blocker, operating-hour discrepancy, duplicate venue, date typo, and blank unverified field across Days 1–9.",
    body: buildFlaggedBody
  }
];

const PEER_OWNED_ROOT_SLUGS = new Set([
  "index.html",
  "stays.html",
  "transit.html",
  "food-shopping.html",
  "flagged-for-review.html"
]);

for (const page of PAGES) {
  const bodyHtml = page.body();
  if (!PEER_OWNED_ROOT_SLUGS.has(page.slug) || !fs.existsSync(path.join(ROOT, page.slug))) {
    fs.writeFileSync(
      path.join(ROOT, page.slug),
      pageShell({
        slug: page.slug,
        title: page.title,
        subtitle: page.subtitle,
        bodyHtml,
        assetPrefix: "./"
      }),
      "utf8"
    );
  }
  fs.writeFileSync(
    path.join(PORTAL_DIR, page.slug),
    pageShell({
      slug: page.slug,
      title: page.title,
      subtitle: page.subtitle,
      bodyHtml,
      assetPrefix: "../"
    }),
    "utf8"
  );
}

fs.writeFileSync(path.join(ROOT, ".nojekyll"), "", "utf8");
console.log(`Built ${PAGES.length} root pages + ${PAGES.length} /portal/ pages successfully.`);
