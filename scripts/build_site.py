#!/usr/bin/env python3
"""Build the static Korea itinerary site (docs/) from data/*.json and verify it.

Usage:
    python3 scripts/build_site.py          # validate data, build docs/, check links
    python3 scripts/build_site.py --check  # validate data and internal links only

Exit code is non-zero if any verification rule or link check fails.
"""
import datetime as dt
import html
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
OUT = os.path.join(ROOT, "docs")

STATUS_LABEL = {
    "Verified": ("ok", "Verified"),
    "Conflict": ("bad", "Conflict"),
    "Partly verified": ("warn", "Partly verified"),
    "Unverified": ("grey", "Unverified"),
    "Plan note": ("blue", "Plan note"),
    "No plan": ("grey", "No plan"),
    "Reference": ("teal", "Reference"),
}
OFFICIAL_STATUSES = {"Verified", "Conflict", "Partly verified", "Reference"}
NO_VALUE_STATUSES = {"Unverified", "Plan note", "No plan"}
OFFICIAL_FIELDS = ["official_hours", "official_fee", "official_location", "official_transit", "official_detail"]
REQUIRED_FIELDS = ["id", "day", "date", "category", "item", "submitted", "status", "sources", "context", "flag", "notes"] + OFFICIAL_FIELDS
SEVERITY_CLASS = {"High": "bad", "Medium": "warn", "Low": "grey"}

errors = []


def fail(msg):
    errors.append(msg)


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


sources_doc = load("sources.json")
records_doc = load("records.json")
findings = load("findings.json")
SOURCES = {s["id"]: s for s in sources_doc["sources"]}
RECORDS = records_doc["records"]
RECORD_IDS = {r["id"] for r in RECORDS}
TRIP = records_doc["trip"]
VERIFIED_ON = TRIP["verified_on"]

OFFICIAL_DOMAINS = {
    "royalpalacekr.org", "kh.or.kr", "nseoultower.co.kr", "english.seoul.go.kr",
    "airportlimousine.co.kr", "hotelofseoul.com", "busan-hotel.com", "korail.com",
    "english.visitkorea.or.kr", "english.visitseoul.net", "www.visitkorea.or.kr",
    "global.lotteshopping.com", "myeongdongtown.oliveyoung.com", "m.starfield.co.kr",
    "www.starfield.co.kr", "ddp.or.kr", "www.visitbusan.net", "guide.michelin.com",
    "www.jongno.go.kr",
}


def domain_ok(url):
    host = urlparse(url).hostname or ""
    return host in OFFICIAL_DOMAINS or any(host.endswith("." + d) for d in OFFICIAL_DOMAINS)


# ---------- validation ----------
def validate():
    ids = set()
    for s in sources_doc["sources"]:
        if s["type"] not in ("official", "context"):
            fail(f"source {s['id']} has bad type {s['type']}")
        if not s["url"].startswith("https://"):
            fail(f"source {s['id']} URL is not https")
        if s["type"] == "official" and not domain_ok(s["url"]):
            fail(f"source {s['id']} domain not on official allow-list: {s['url']}")
    for r in RECORDS:
        rid = r.get("id", "?")
        if rid in ids:
            fail(f"duplicate id {rid}")
        ids.add(rid)
        for k in REQUIRED_FIELDS:
            if k not in r:
                fail(f"{rid}: missing field {k}")
        st = r.get("status")
        if st not in STATUS_LABEL:
            fail(f"{rid}: unknown status {st}")
            continue
        for sid in r.get("sources", []):
            if sid not in SOURCES:
                fail(f"{rid}: unknown source {sid}")
            elif SOURCES[sid]["type"] != "official":
                fail(f"{rid}: source {sid} is not official but is used for values")
        for cid in r.get("context", []):
            if cid not in SOURCES:
                fail(f"{rid}: unknown context source {cid}")
            elif SOURCES[cid]["type"] != "context":
                fail(f"{rid}: context entry {cid} should be a context source")
        has_value = any(str(r.get(f, "")).strip() for f in OFFICIAL_FIELDS)
        if st in OFFICIAL_STATUSES:
            if not r.get("sources"):
                fail(f"{rid}: status {st} requires at least one official source link")
            if not has_value:
                fail(f"{rid}: status {st} requires at least one official value")
        if st in NO_VALUE_STATUSES:
            if has_value:
                fail(f"{rid}: status {st} must leave official values blank")
            if r.get("sources"):
                fail(f"{rid}: status {st} must not carry official source links")
    for day in range(1, 10):
        if not any(r.get("day") == day for r in RECORDS):
            fail(f"day {day} has no records")
    for irr in findings["irregularities"]:
        for rid in irr.get("rows", []):
            if rid not in RECORD_IDS:
                fail(f"{irr['id']}: unknown row {rid}")
        for sid in irr.get("sources", []):
            if sid not in SOURCES:
                fail(f"{irr['id']}: unknown source {sid}")
    return ids


# ---------- html helpers ----------
def e(x):
    return html.escape(str(x if x is not None else ""), quote=True)


def badge(status):
    cls, label = STATUS_LABEL[status]
    return f'<span class="badge b-{cls}">{e(label)}</span>'


def src_links(ids):
    out = []
    for sid in ids:
        s = SOURCES[sid]
        out.append(f'<a class="src" href="{e(s["url"])}" target="_blank" rel="noopener" title="{e(s["title"])} — {e(s["publisher"])}">{e(sid)}</a>')
    return " ".join(out) if out else '<span class="muted">—</span>'


def ctx_links(ids):
    if not ids:
        return ""
    return " ".join(f'<a class="src ctx" href="{e(SOURCES[c]["url"])}" target="_blank" rel="noopener" title="Context only — not used for values">{e(c)}</a>' for c in ids)


def cell(val):
    return e(val) if val else '<span class="blank">blank — unverified</span>'


def weekday(date_str):
    if not date_str:
        return ""
    return dt.date.fromisoformat(date_str).strftime("%A")


def pretty_date(date_str):
    if not date_str:
        return ""
    return dt.date.fromisoformat(date_str).strftime("%b %d, %Y")


def page(title, active, body, desc=""):
    nav = [
        ("index.html", "Dashboard"),
        ("itinerary.html", "Itinerary"),
        ("transit.html", "Transit"),
        ("hours-locations.html", "Hours & locations"),
        ("costs.html", "Costs & fees"),
        ("analysis.html", "Analysis"),
        ("flagged.html", "Flagged for Review"),
        ("sources.html", "Sources"),
    ]
    link_parts = []
    for href, label in nav:
        cls = []
        if href == active:
            cls.append("on")
        if href == "flagged.html":
            cls.append("flag-link")
        class_attr = (' class="' + " ".join(cls) + '"') if cls else ""
        link_parts.append('<a href="' + href + '"' + class_attr + ">" + e(label) + "</a>")
    links = "".join(link_parts)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · Korea Trip 2026</title>
<meta name="description" content="{e(desc or 'Korea trip itinerary with official-source verification.')}">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="index.html">Korea Trip 2026</a><span>Seoul → Busan · 2 adults · Nov 1–9</span></div>
  <nav class="nav">{links}</nav>
</header>
<main class="wrap">
{body}
</main>
<footer class="foot">
  Values were checked against official sources on {e(VERIFIED_ON)}. Blank cells are unverified and are not filled in. Check schedules, fares and hours before you travel.
</footer>
</body>
</html>
"""


def table(headers, rows, cls=""):
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    trs = "".join("<tr>" + "".join(f'<td data-label="{e(headers[i])}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def counts(records):
    c = {k: 0 for k in STATUS_LABEL}
    for r in records:
        c[r["status"]] += 1
    return c


PLAN = [r for r in RECORDS if r["day"] is not None]
REFS = [r for r in RECORDS if r["day"] is None]
PLAN_COUNTS = counts(PLAN)
FLAGGED = [r for r in RECORDS if r["flag"] or r["status"] in ("Conflict", "Partly verified", "Unverified")]
ISSUE_STATUSES = ("Conflict", "Partly verified", "Unverified")


def official_summary(r):
    parts = []
    for label, field in [("Hours", "official_hours"), ("Fee", "official_fee"), ("Location", "official_location"), ("Transit", "official_transit"), ("Detail", "official_detail")]:
        if r.get(field):
            parts.append(f"<div><b>{label}:</b> {e(r[field])}</div>")
    return "".join(parts) if parts else '<span class="blank">blank — unverified</span>'


# ---------- pages ----------
def page_index():
    total_plan = len(PLAN)
    verified = PLAN_COUNTS["Verified"]
    conflicts = PLAN_COUNTS["Conflict"]
    partly = PLAN_COUNTS["Partly verified"]
    unver = PLAN_COUNTS["Unverified"]
    high = [i for i in findings["irregularities"] if i["severity"] == "High"]
    kpis = f"""
<section class="kpis">
  <a class="kpi" href="itinerary.html"><b>9</b><span>Days</span></a>
  <a class="kpi" href="itinerary.html"><b>{total_plan}</b><span>Plan rows</span></a>
  <a class="kpi ok" href="analysis.html"><b>{verified}</b><span>Verified</span></a>
  <a class="kpi partly" href="flagged.html"><b>{partly}</b><span>Partly verified</span></a>
  <a class="kpi bad" href="flagged.html"><b>{conflicts}</b><span>Conflicts</span></a>
  <a class="kpi grey" href="flagged.html"><b>{unver}</b><span>Unverified</span></a>
</section>"""
    cards = [
        ("itinerary.html", "Day-by-day itinerary", "All 9 days, every line as submitted, with its official check and status."),
        ("transit.html", "Getting around", "Airport train and bus, taxis, subway access, KTX, and hotel-to-station walks."),
        ("hours-locations.html", "Hours & locations", "Official opening hours and addresses, with source links."),
        ("costs.html", "Costs & fees", "Official fares and admission prices. Unverified prices are left blank."),
        ("analysis.html", "Analysis & findings", "Repo review, verification method, and the key findings."),
        ("flagged.html", "Flagged for Review", "Conflicts, unverified items and irregularities, with source links."),
        ("sources.html", "Sources", "Every official source used, with its link and the rows it supports."),
    ]
    card_html = "".join(f'<a class="card" href="{h}"><h3>{e(t)}</h3><p>{e(d)}</p></a>' for h, t, d in cards)
    rows = []
    for d in range(1, 10):
        rs = [r for r in PLAN if r["day"] == d]
        date = rs[0]["date"] if rs else None
        c = counts(rs)
        title = {1: "Travel to Seoul; check in, Myeongdong", 2: "Namsan Tower & Myeongdong", 3: "Gyeongbokgung & Bukchon", 4: "Seongsu", 5: "Starfield COEX Mall", 6: "Ikseon-dong & Insadong", 7: "Itaewon", 8: "(no plan entered)", 9: "KTX Seoul → Busan; Haeundae"}[d]
        status_bits = []
        if c["Conflict"]:
            status_bits.append(f'<span class="badge b-bad">{c["Conflict"]} conflict</span>')
        if c["Partly verified"]:
            status_bits.append(f'<span class="badge b-warn">{c["Partly verified"]} partly</span>')
        if c["Verified"]:
            status_bits.append(f'<span class="badge b-ok">{c["Verified"]} verified</span>')
        if c["Unverified"]:
            status_bits.append(f'<span class="badge b-grey">{c["Unverified"]} unverified</span>')
        if not rs or all(r["status"] == "No plan" for r in rs):
            status_bits = ['<span class="badge b-grey">No plan entered</span>']
        rows.append([f'<a href="itinerary.html#day{d}">Day {d}</a>', e(title), e(f"{weekday(date)}, {pretty_date(date)}") if date else "—", " ".join(status_bits)])
    day_table = table(["Day", "Plan", "Date", "Status summary"], rows)
    critical = "".join(
        f'<li><span class="badge b-bad">{e(i["severity"])}</span> <b>{e(i["title"])}</b> — {e(i["detail"])} <a href="flagged.html#{e(i["id"])}">details</a></li>'
        for i in high)
    body = f"""
<section class="hero">
  <h1>Korea Trip 2026</h1>
  <p>Seoul (Myeongdong) → Busan, for two adults. Every line of your itinerary is listed below with its official check. Where an official source could not confirm a value, the cell is left blank and the item is flagged.</p>
  <p class="muted">Verified against official sources on {e(VERIFIED_ON)}.</p>
</section>
{kpis}
<section>
  <h2>Action needed first</h2>
  <ul class="alert">{critical}</ul>
</section>
<section>
  <h2>Sections</h2>
  <div class="cards">{card_html}</div>
</section>
<section>
  <h2>Day at a glance</h2>
  {day_table}
</section>
"""
    return page("Dashboard", "index.html", body, "Korea trip itinerary dashboard with official-source verification.")


def page_itinerary():
    parts = ['<h1>Itinerary</h1><p class="muted">Each line from your submission, in order, with its official check. Blank cells are unverified.</p>']
    for d in range(1, 10):
        rs = [r for r in RECORDS if r["day"] == d]
        date = rs[0]["date"] if rs else None
        head = f"Day {d} · {weekday(date)}, {pretty_date(date)}" if date else f"Day {d}"
        rows = []
        for r in rs:
            rows.append([
                e(r["id"]),
                f'<b>{e(r["item"])}</b><div class="muted small">Submitted: {e(r["submitted"])}</div>',
                e(r["category"]),
                official_summary(r),
                badge(r["status"]),
                src_links(r["sources"]) + (" " + ctx_links(r["context"]) if r["context"] else ""),
                e(r["notes"]) + (' <span class="flagtag">FLAG</span>' if r["flag"] else ""),
            ])
        parts.append(f'<section id="day{d}"><h2>{e(head)}</h2>' + table(["ID", "Plan item", "Type", "Official check", "Status", "Source", "Notes"], rows, "itin") + "</section>")
    return page("Itinerary", "itinerary.html", "".join(parts), "Day-by-day Korea itinerary with verification status.")


def page_transit():
    rs = [r for r in RECORDS if r["category"] in ("Transit",) or r["category"] == "Reference" and r["official_transit"] or r["id"] in ("REF-01", "REF-02", "REF-03", "REF-04")]
    rows = []
    for r in rs:
        rows.append([
            e(r["id"]),
            e(f"Day {r['day']}") if r["day"] else "Reference",
            f"<b>{e(r['item'])}</b>",
            official_summary({k: r.get(k, "") for k in OFFICIAL_FIELDS}),
            badge(r["status"]),
            src_links(r["sources"]),
            e(r["notes"]),
        ])
    intro = """
<h1>Getting around</h1>
<p class="muted">Public transport and transfers linked to the planned hotels and cities. Official values only; blanks are unverified.</p>
<div class="callout"><b>Hotel-to-transit basics (official):</b> Stanford Hotel Myeongdong is about 5 minutes on foot from Euljiro 1-ga Station; Seoul Station connects to KTX and AREX; the airport limousine route 6001 stops at Myeongdong Station; the N Seoul Tower cable car starts from Myeongdong Station Exit 3.</div>
"""
    return page("Transit", "transit.html", intro + table(["ID", "Day", "Item", "Official transit & fare details", "Status", "Source", "Notes"], rows, "itin"), "Public transportation for the Korea trip: airport, subway, KTX.")


def page_hours():
    rs = [r for r in RECORDS if r["official_hours"] or r["official_location"]]
    rows = []
    for r in rs:
        rows.append([
            e(r["id"]),
            e(f"Day {r['day']}") if r["day"] else "Reference",
            f"<b>{e(r['item'])}</b>",
            cell(r["official_hours"]),
            cell(r["official_location"]),
            badge(r["status"]),
            src_links(r["sources"]),
        ])
    intro = "<h1>Hours & locations</h1><p class=\"muted\">Official opening hours and addresses only. Blank means no official value was confirmed. Hours can change; check before you go.</p>"
    return page("Hours & locations", "hours-locations.html", intro + table(["ID", "Day", "Place", "Official hours", "Official location", "Status", "Source"], rows, "itin"), "Verified opening hours and addresses for Korea trip stops.")


def page_costs():
    rs = [r for r in RECORDS if r["official_fee"]]
    rows = []
    for r in rs:
        rows.append([
            e(r["id"]),
            e(f"Day {r['day']}") if r["day"] else "Reference",
            f"<b>{e(r['item'])}</b><div class=\"muted small\">Submitted: {e(r['submitted'])}</div>",
            cell(r["official_fee"]),
            badge(r["status"]),
            src_links(r["sources"]),
            e(r["notes"]),
        ])
    intro = "<h1>Costs & fees</h1><p class=\"muted\">Official prices in Korean won (₩). USD amounts from your notes were not converted because no official exchange rate was used. Items with no official price are not listed here; see Flagged for Review.</p>"
    return page("Costs & fees", "costs.html", intro + table(["ID", "Day", "Item", "Official fee", "Status", "Source", "Notes"], rows, "itin"), "Official fares and admission prices for the Korea trip.")


def page_analysis():
    c = PLAN_COUNTS
    total = len(PLAN)
    stats = table(["Measure", "Count", "Meaning"], [
        ["Plan rows (from your submission)", str(total), "Every submitted line, grouped by day."],
        ["Verified against official sources", str(c["Verified"]), "Matches an official page."],
        ["Conflict", str(c["Conflict"]), "Official page disagrees with the submission. Official value shown."],
        ["Partly verified", str(c["Partly verified"]), "Some parts match, others not confirmed."],
        ["Unverified", str(c["Unverified"]), "No official source found. Value left blank."],
        ["Plan note / No plan", str(c["Plan note"] + c["No plan"]), "Advice or empty days; nothing to verify."],
        ["Reference rows added", str(len(REFS)), "Official transit facts that help with the plan (not from your submission)."],
        ["Irregularities logged", str(len(findings["irregularities"])), "See Flagged for Review."],
    ])
    rr = findings["repo_review"]
    repo = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in rr["files_found"]) + "</ul><h3>Work done</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in rr["actions"]) + "</ul><h3>Limits of this review</h3><ul>" + "".join(f"<li>{e(x)}</li>" for x in rr["limitations"]) + "</ul>"
    method = """<ol>
<li>Each line of the submitted itinerary was transcribed into one row, in order (data/records.json).</li>
<li>Each fact (hours, fee, address, transit time, hotel details) was looked up on an official site (tourism organisation, operator, government, or venue site). Links are in the Source column.</li>
<li>A value that could not be confirmed is left blank and the row is marked Unverified. Values are never inferred or converted.</li>
<li>Calendar: weekdays were computed from the dates (Nov 1, 2026 = Sunday; Nov 3, 2026 = Tuesday).</li>
<li>Build checks (scripts/build_site.py): every Verified, Conflict, Partly verified or Reference row must link at least one official source with a value; every link must point to an allow-listed official domain; internal links must resolve.</li>
</ol>"""
    high = [i for i in findings["irregularities"] if i["severity"] == "High"]
    key = "<ul>" + "".join(f"<li><b>{e(i['title'])}.</b> {e(i['detail'])}</li>" for i in high) + "</ul>"
    body = f"""
<h1>Analysis & findings</h1>
<h2>Summary</h2>{stats}
<h2>Key findings (high severity)</h2>{key}
<p><a href="flagged.html">See all {len(findings['irregularities'])} irregularities on Flagged for Review →</a></p>
<h2>Verification method</h2>{method}
<h2>Repo review</h2>{repo}
<p class="muted">Checked on {e(rr['checked_on'])}. Branch: {e(rr['branch'])}.</p>
"""
    return page("Analysis", "analysis.html", body, "Analysis and findings for the Korea trip itinerary.")


def page_flagged():
    irr_cards = []
    for i in findings["irregularities"]:
        links = " ".join(src_links([s]) for s in i.get("sources", [])) if i.get("sources") else '<span class="muted">no official source (see notes)</span>'
        ctx = ctx_links(i.get("context", []))
        rows = ", ".join(i.get("rows", []))
        irr_cards.append(f"""<article class="irr" id="{e(i['id'])}">
  <div class="irr-head"><span class="badge b-{SEVERITY_CLASS[i['severity']]}">{e(i['severity'])}</span> <b>{e(i['id'])}</b> · {e(i['title'])}</div>
  <p>{e(i['detail'])}</p>
  <p class="small"><b>Rows:</b> {e(rows)} &nbsp; <b>Action:</b> {e(i['action'])}</p>
  <p class="small"><b>Official sources:</b> {links} {ctx}</p>
</article>""")
    rows = []
    for r in FLAGGED:
        rows.append([
            e(r["id"]),
            e(f"Day {r['day']}") if r["day"] else "Reference",
            f"<b>{e(r['item'])}</b><div class=\"muted small\">Submitted: {e(r['submitted'])}</div>",
            badge(r["status"]),
            src_links(r["sources"]) + (" " + ctx_links(r["context"]) if r["context"] else ""),
            e(r["notes"]),
        ])
    intro = f"""
<h1>Flagged for Review</h1>
<div class="callout warn"><b>For your review after the site is live.</b> These items did not match, could not be verified, or need your decision. Flagged items do not block the publish. Each entry links its official source where one exists.</div>
<h2>Irregularities ({len(findings['irregularities'])})</h2>
<div class="irrs">{''.join(irr_cards)}</div>
<h2>Itinerary rows needing review ({len(FLAGGED)})</h2>
"""
    return page("Flagged for Review", "flagged.html", intro + table(["ID", "Day", "Plan item", "Status", "Source", "Notes"], rows, "itin"), "Flagged for review: conflicts, unverified items and irregularities in the Korea itinerary.")


def page_sources():
    used = {}
    for r in RECORDS:
        for s in r["sources"]:
            used.setdefault(s, []).append(r["id"])
        for s in r["context"]:
            used.setdefault(s, []).append(r["id"] + " (context)")
    for i in findings["irregularities"]:
        for s in i.get("sources", []):
            used.setdefault(s, []).append(i["id"])
    rows = []
    for s in sources_doc["sources"]:
        u = used.get(s["id"], [])
        rows.append([
            f"<b>{e(s['id'])}</b>",
            e(s["title"]),
            e(s["publisher"]),
            ('<span class="badge b-ok">Official</span>' if s["type"] == "official" else '<span class="badge b-grey">Context only</span>'),
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["url"])}</a>',
            e(", ".join(u)) if u else "—",
        ])
    intro = f"<h1>Sources</h1><p class=\"muted\">Accessed {e(sources_doc['accessed'])}. Official sources are used for values. Context sources are listed for transparency only and never supply a value.</p>"
    return page("Sources", "sources.html", intro + table(["ID", "Title", "Publisher", "Type", "URL", "Used by"], rows, "itin"), "Sources used for the Korea trip itinerary verification.")


CSS = """
:root{--ink:#1b2430;--muted:#5d6b7a;--line:#e3e8ef;--bg:#f6f8fb;--card:#fff;--brand:#1f4e8c;--ok:#1e7d4f;--bad:#b42318;--warn:#b26a00;--grey:#5d6b7a;--blue:#2457a6;--teal:#0f766e}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--brand)}
.wrap{max-width:1180px;margin:0 auto;padding:16px}
.top{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.brand{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:baseline;padding:12px 16px 4px;max-width:1180px;margin:0 auto}
.brand a{font-weight:700;font-size:18px;color:var(--ink);text-decoration:none}
.brand span{color:var(--muted);font-size:13px}
.nav{display:flex;flex-wrap:wrap;gap:6px;padding:6px 16px 10px;max-width:1180px;margin:0 auto}
.nav a{padding:6px 10px;border-radius:999px;text-decoration:none;color:var(--ink);background:#eef2f7;font-size:13px}
.nav a.on{background:var(--brand);color:#fff}
.nav a.flag-link{background:#fde8e6;color:var(--bad);font-weight:600}
.nav a.flag-link.on{background:var(--bad);color:#fff}
h1{font-size:26px;margin:14px 0 6px}
h2{font-size:19px;margin:24px 0 8px}
h3{font-size:16px;margin:16px 0 6px}
.hero{background:linear-gradient(135deg,#1f4e8c,#2e6fb8);color:#fff;border-radius:14px;padding:20px 22px}
.hero h1{color:#fff;margin-top:0}
.hero p{margin:6px 0}
.hero .muted{color:#dbe7f5}
.muted{color:var(--muted)}
.small{font-size:13px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin:14px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column}
.kpi b{font-size:26px;line-height:1.1}
.kpi span{color:var(--muted);font-size:13px}
.kpi.ok b{color:var(--ok)} .kpi.bad b{color:var(--bad)} .kpi.partly b{color:var(--warn)} .kpi.grey b{color:var(--grey)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-decoration:none;color:var(--ink)}
.card h3{margin:0 0 4px;color:var(--brand)}
.card p{margin:0;color:var(--muted);font-size:14px}
.alert{list-style:none;padding:0;margin:0}
.alert li{background:#fff;border:1px solid var(--line);border-left:4px solid var(--bad);border-radius:8px;padding:8px 12px;margin-bottom:8px}
.callout{background:#eef6ff;border:1px solid #cfe3f9;border-radius:10px;padding:10px 14px;margin:12px 0}
.callout.warn{background:#fff7e6;border-color:#f5d28a}
.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:12px;margin:8px 0}
table{border-collapse:collapse;width:100%;min-width:640px;font-size:14px}
th,td{text-align:left;vertical-align:top;padding:9px 10px;border-bottom:1px solid var(--line)}
th{background:#f0f4fa;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}
tr:last-child td{border-bottom:0}
td .small{margin-top:3px}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:600;white-space:nowrap;color:#fff;background:var(--grey)}
.b-ok{background:var(--ok)} .b-bad{background:var(--bad)} .b-warn{background:var(--warn)} .b-grey{background:var(--grey)} .b-blue{background:var(--blue)} .b-teal{background:var(--teal)}
.src{display:inline-block;margin:1px 3px 1px 0;padding:1px 7px;border-radius:6px;background:#e8f0fb;color:var(--brand);text-decoration:none;font-weight:600;font-size:12px}
.src.ctx{background:#eef0f3;color:#44505e}
.blank{color:#9aa5b1;font-style:italic;font-size:13px}
.flagtag{display:inline-block;background:#fde8e6;color:var(--bad);font-weight:700;font-size:11px;padding:1px 6px;border-radius:6px;margin-left:4px}
.irrs{display:grid;gap:10px}
.irr{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.irr-head{margin-bottom:4px}
.foot{max-width:1180px;margin:20px auto;padding:12px 16px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
ol,ul{padding-left:22px}
section{margin-bottom:8px}
@media (max-width:640px){
  body{font-size:14px}
  .wrap{padding:10px}
  h1{font-size:22px}
  .hero{padding:16px}
  .nav a{font-size:12px;padding:5px 8px}
  table{min-width:0}
  .tablewrap{overflow:visible;background:transparent;border:0}
  table thead{display:none}
  table,tbody,tr,td{display:block;width:100%}
  tr{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:10px;padding:6px 10px}
  td{border:0;padding:5px 0}
  td::before{content:attr(data-label);display:block;font-size:11px;text-transform:uppercase;color:var(--muted);letter-spacing:.03em}
}
"""


def write(path, text):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def check_links():
    html_files = [f for f in os.listdir(OUT) if f.endswith(".html")]
    existing = set(html_files) | {"assets/style.css"}
    for f in html_files:
        text = open(os.path.join(OUT, f), encoding="utf-8").read()
        for href in re.findall(r'href="([^"]+)"', text):
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            target = href.split("#")[0]
            if not target:
                # same-page anchor: verify id exists
                anchor = href[1:]
                if anchor and f'id="{anchor}"' not in text:
                    fail(f"{f}: broken anchor #{anchor}")
                continue
            if target not in existing:
                fail(f"{f}: broken internal link {href}")
            elif "#" in href:
                anchor = href.split("#", 1)[1]
                other = open(os.path.join(OUT, target), encoding="utf-8").read() if target.endswith(".html") else ""
                if anchor and f'id="{anchor}"' not in other:
                    fail(f"{f}: broken anchor {href}")


def main():
    check_only = "--check" in sys.argv
    validate()
    if not check_only:
        os.makedirs(OUT, exist_ok=True)
        write("assets/style.css", CSS)
        write("index.html", page_index())
        write("itinerary.html", page_itinerary())
        write("transit.html", page_transit())
        write("hours-locations.html", page_hours())
        write("costs.html", page_costs())
        write("analysis.html", page_analysis())
        write("flagged.html", page_flagged())
        write("sources.html", page_sources())
        write(".nojekyll", "")
        check_links()
    else:
        pass
    if errors:
        print("FAILED checks:")
        for m in errors:
            print(" -", m)
        sys.exit(1)
    print(f"OK: {len(RECORDS)} records ({len(PLAN)} plan rows), {len(SOURCES)} sources, "
          f"{len(findings['irregularities'])} irregularities. Verified={PLAN_COUNTS['Verified']} "
          f"Conflict={PLAN_COUNTS['Conflict']} Partly={PLAN_COUNTS['Partly verified']} Unverified={PLAN_COUNTS['Unverified']}")


if __name__ == "__main__":
    main()
