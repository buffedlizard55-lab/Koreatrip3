#!/usr/bin/env python3
"""
build_site.py — generates the static Korea-trip itinerary verification site.

Reads data/*.json and writes flat HTML pages to the repo root
(served by GitHub Pages from the main branch root):
  index.html        landing dashboard
  itinerary.html    day-by-day view (all 9 days)
  transport.html    getting there & getting around
  hotels.html       hotel verification
  food.html         food, cafes, bars & markets
  shopping.html     shopping & experiences
  attractions.html  sights & attractions
  flagged.html      flagged-for-review register (all irregularities)

No external assets, no JS frameworks — inline CSS, mobile-first.
Usage: python3 build_site.py [--check]   (--check runs the internal link check only)
"""
import json
import os
import re
import sys
import html as H
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

# ---------------------------------------------------------------- load data
def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)

trip = load("trip.json")
transport = load("transport.json")
hotels = load("hotels.json")
v13 = load("venues-days1-3.json")
v48 = load("venues-days4-8.json")
v9 = load("venues-day9.json")
flags = load("flags.json")

venues = v13["rows"] + v48["rows"] + v9["rows"]
flags_by_id = {f["id"]: f for f in flags["flags"]}
days = trip["days"]
trip_meta = trip["trip"]

STATUS_LABEL = {"verified": "Verified", "partial": "Partial", "unverified": "Unverified"}
STATUS_CLASS = {"verified": "b-v", "partial": "b-p", "unverified": "b-u"}
SEV_CLASS = {"critical": "s-c", "warning": "s-w", "info": "s-i"}
SEV_LABEL = {"critical": "Critical", "warning": "Warning", "info": "Info"}

# ---------------------------------------------------------------- helpers
def esc(s):
    return H.escape(str(s), quote=True)

def src_links(row, max_show=4):
    srcs = row.get("sources") or []
    if not srcs:
        return '<span class="nosrc">no official source — see flag</span>'
    out = []
    for i, s in enumerate(srcs[:max_show], 1):
        out.append(
            f'<a class="src" href="{esc(s["url"])}" target="_blank" rel="noopener" '
            f'title="{esc(s["label"])}">[{i}]&nbsp;{esc(s["label"])}</a>'
        )
    return "<br>".join(out)

def badge(status):
    return f'<span class="b {STATUS_CLASS[status]}">{STATUS_LABEL[status]}</span>'

def flagchip(fid):
    return (f'<a class="fl" href="flagged.html#{fid}" title="{esc(flags_by_id[fid]["title"])}">'
            f'⚑ {fid}</a>')

def flagchips(row):
    ids = row.get("flag_ids") or []
    return " ".join(flagchip(i) for i in ids if i in flags_by_id)

def venue_table(rows, show_day=True):
    if not rows:
        return "<p class='muted'>No entries.</p>"
    out = ['<div class="tw"><table class="tbl">']
    out.append("<thead><tr>"
               + ("<th>Day</th>" if show_day else "")
               + "<th>Venue / item</th><th>Original itinerary said</th>"
                 "<th>Verified details (official sources)</th><th>Status</th><th>Sources</th>"
               + "</tr></thead><tbody>")
    for r in rows:
        det = []
        if r.get("address"):
            det.append(f'<div><b>Address:</b> {esc(r["address"])}</div>')
        if r.get("hours"):
            det.append(f'<div><b>Hours:</b> {esc(r["hours"])}</div>')
        if r.get("price"):
            det.append(f'<div><b>Price:</b> {esc(r["price"])}</div>')
        if r.get("notes"):
            det.append(f'<div class="note">{esc(r["notes"])}</div>')
        if r.get("transit"):
            det.append(f'<div class="transit">🚇 {esc(r["transit"])}</div>')
        if not det:
            det = ['<div class="muted">— left blank: not confirmable from an official source</div>']
        name = esc(r["name"])
        if r.get("ko"):
            name += f' <span class="ko">{esc(r["ko"])}</span>'
        if r.get("district"):
            name += f'<div class="dist">{esc(r["district"])}</div>'
        daycell = f'D{r["day"]}' if show_day else ""
        out.append(
            "<tr>"
            + (f"<td class='daycell'>{daycell}</td>" if show_day else "")
            + f'<td class="namecell">{name}<div class="chips">{flagchips(r)}</div></td>'
            f'<td class="claim">{esc(r.get("claim","—"))}</td>'
            f'<td class="detcell">{"".join(det)}</td>'
            f'<td>{badge(r["status"])}</td>'
            f'<td class="srccell">{src_links(r)}</td>'
            "</tr>"
        )
    out.append("</tbody></table></div>")
    return "".join(out)

def transport_table(rows):
    out = ['<div class="tw"><table class="tbl">',
           "<thead><tr><th>Leg / mode</th><th>Original itinerary said</th>"
           "<th>Verified time / fare</th><th>Frequency & notes</th><th>Status</th><th>Sources</th>"
           "</tr></thead><tbody>"]
    for r in rows:
        out.append(
            f'<tr><td class="namecell"><b>{esc(r["route"])}</b>'
            f'<div class="dist">{esc(r["mode"])}</div><div class="chips">{flagchips(r)}</div></td>'
            f'<td class="claim">{esc(r.get("claim","—"))}</td>'
            f'<td class="detcell"><div><b>Time:</b> {esc(r.get("verified_time","—"))}</div>'
            f'<div><b>Fare:</b> {esc(r.get("verified_fare","—"))}</div></td>'
            f'<td class="detcell"><div><b>Frequency:</b> {esc(r.get("frequency","—"))}</div>'
            f'<div class="note">{esc(r.get("notes",""))}</div></td>'
            f'<td>{badge(r["status"])}</td>'
            f'<td class="srccell">{src_links(r)}</td></tr>'
        )
    out.append("</tbody></table></div>")
    return "".join(out)

# ---------------------------------------------------------------- page shell
PAGES = [
    ("index.html", "Dashboard"),
    ("itinerary.html", "Itinerary"),
    ("transport.html", "Transport"),
    ("hotels.html", "Hotels"),
    ("food.html", "Food & Cafes"),
    ("shopping.html", "Shopping"),
    ("attractions.html", "Attractions"),
    ("flagged.html", "Flagged"),
]

CSS = """
:root{--ink:#0f172a;--mut:#64748b;--line:#e2e8f0;--bg:#f1f5f9;--card:#ffffff;
--acc:#0f766e;--accd:#134e4a;--amber:#b45309;--red:#b91c1c;}
*{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
color:var(--ink);background:var(--bg);line-height:1.55;font-size:15px}
a{color:var(--acc)}
header.site{background:#0f172a;color:#e2e8f0;padding:10px 16px}
.hwrap{max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;gap:8px;align-items:baseline;justify-content:space-between}
.brand{font-weight:800;font-size:17px;color:#fff;text-decoration:none;letter-spacing:.2px}
.brand span{color:#5eead4}
nav.top{display:flex;gap:2px;overflow-x:auto;max-width:100%;-webkit-overflow-scrolling:touch}
nav.top a{color:#cbd5e1;text-decoration:none;font-size:13px;padding:6px 10px;border-radius:6px;white-space:nowrap}
nav.top a:hover{background:#1e293b;color:#fff}
nav.top a.on{background:var(--acc);color:#fff;font-weight:700}
main{max-width:1100px;margin:0 auto;padding:18px 16px 60px}
h1{font-size:24px;margin:6px 0 4px}
h2{font-size:19px;margin:26px 0 10px;padding-top:10px;border-top:2px solid var(--line)}
h2:first-of-type{border-top:none}
h3{font-size:16px;margin:16px 0 8px}
p.lede{color:var(--mut);margin-bottom:14px}
.muted{color:var(--mut)}
.small{font-size:12.5px}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0;box-shadow:0 1px 2px rgba(15,23,42,.04)}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.stat{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center}
.stat .n{font-size:26px;font-weight:800}
.stat .l{font-size:12px;color:var(--mut);text-transform:uppercase;letter-spacing:.4px}
.sv{color:var(--acc)} .sp{color:var(--amber)} .su{color:var(--red)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;background:var(--card);border:1px solid var(--line);border-radius:12px}
table.tbl{border-collapse:collapse;width:100%;min-width:760px;font-size:13.5px}
.tbl th{text-align:left;font-size:11px;text-transform:uppercase;letter-spacing:.5px;color:var(--mut);
padding:10px 10px 8px;border-bottom:2px solid var(--line);background:#f8fafc;position:sticky;top:0}
.tbl td{padding:10px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:none}
.namecell{font-weight:700;min-width:150px}
.ko{font-weight:400;color:var(--mut);font-size:12px}
.dist{font-weight:400;color:var(--mut);font-size:12px;margin-top:2px}
.claim{color:#475569;font-size:12.5px;min-width:140px}
.detcell{min-width:220px}
.note{font-size:12.5px;color:#475569;margin-top:4px}
.transit{font-size:12.5px;color:var(--acc);margin-top:4px}
.srccell{min-width:170px;font-size:12px}
.src{display:block;margin:2px 0;color:var(--acc);text-decoration:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:230px}
.src:hover{text-decoration:underline}
.nosrc{color:var(--red);font-size:12px}
.daycell{font-weight:800;color:var(--mut);white-space:nowrap}
.b{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11px;font-weight:700;white-space:nowrap}
.b-v{background:#dcfce7;color:#166534}.b-p{background:#fef3c7;color:#92400e}.b-u{background:#fee2e2;color:#991b1b}
.fl{display:inline-block;margin:3px 4px 0 0;font-size:11px;font-weight:700;text-decoration:none;
background:#fff7ed;color:#9a3412;border:1px solid #fed7aa;border-radius:999px;padding:1px 8px}
.s{display:inline-block;padding:1px 9px;border-radius:999px;font-size:11px;font-weight:700;white-space:nowrap}
.s-c{background:#fee2e2;color:#991b1b}.s-w{background:#fef3c7;color:#92400e}.s-i{background:#e0f2fe;color:#075985}
.alert{border-left:4px solid var(--red);background:#fef2f2;border-radius:8px;padding:12px 14px;margin:14px 0}
.alert b{color:var(--red)}
.tip{border-left:4px solid var(--acc);background:#f0fdfa;border-radius:8px;padding:12px 14px;margin:14px 0}
.dayhead{display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;margin-top:30px}
.dayhead .dn{background:var(--accd);color:#fff;font-weight:800;border-radius:8px;padding:2px 10px;font-size:14px}
.dayhead h2{border:none;margin:0;padding:0;flex:1 1 200px}
.dayhead .dd{color:var(--mut);font-size:13px}
.daynote{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 12px;margin:8px 0 10px;font-size:13.5px}
.sugg{background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;padding:10px 12px;margin:8px 0 10px;font-size:13.5px}
.kv{display:grid;grid-template-columns:130px 1fr;gap:4px 10px;font-size:13.5px}
.kv b{color:var(--mut);font-weight:600}
.flagcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:12px 0}
.flagcard.crit{border-left:4px solid var(--red)}
.flagcard.warn{border-left:4px solid var(--amber)}
.flagcard.info{border-left:4px solid #0284c7}
.flagcard h3{margin:2px 0 6px}
.flagcard .act{background:#f0fdfa;border-radius:6px;padding:8px 10px;margin-top:8px;font-size:13px}
footer.site{border-top:1px solid var(--line);color:var(--mut);font-size:12px;padding:18px 16px;text-align:center;background:var(--card)}
.hero{background:linear-gradient(135deg,#134e4a,#0f766e);color:#fff;border-radius:14px;padding:22px 20px;margin:6px 0 16px}
.hero h1{color:#fff;font-size:26px}
.hero p{color:#ccfbf1}
.chips{margin-top:2px}
.toc{columns:2;column-gap:24px}
@media(max-width:640px){.toc{columns:1}}
ul.clean{list-style:none}
ul.clean li{padding:3px 0;border-bottom:1px dashed var(--line);break-inside:avoid}
"""

def page(fname, title, body, active):
    nav = "".join(
        f'<a href="{f}" class="{"on" if f == fname else ""}">{label}</a>' for f, label in PAGES
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} — Korea Trip Nov 2026 · Verified Itinerary</title>
<meta name="description" content="Verified 9-day South Korea itinerary (Seoul + Busan, Nov 1-9 2026): every venue checked against official sources, with hours, prices, transport and flagged irregularities.">
<style>{CSS}</style>
</head>
<body>
<header class="site"><div class="hwrap">
<a class="brand" href="index.html">🇰🇷 Korea Trip <span>· Verified</span></a>
<nav class="top">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer class="site">
<p><b>Korea Trip Verification Site</b> — Seoul (Myeongdong) + Busan (Haeundae), Nov 1–9 2026 · 2 adults.</p>
<p>Every table row links its official source. Values that could not be confirmed from an official
source are left blank and flagged on the <a href="flagged.html">Flagged for Review</a> page.
Built from <code>data/*.json</code> via <code>build_site.py</code>. Last generated: 2026-10-21 UTC.</p>
</footer>
</body>
</html>"""

def write(fname, title, body, active=None):
    active = active or fname
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(page(fname, title, body, active))

# ---------------------------------------------------------------- stats
n_v = sum(1 for r in venues if r["status"] == "verified")
n_p = sum(1 for r in venues if r["status"] == "partial")
n_u = sum(1 for r in venues if r["status"] == "unverified")
n_t = len(venues)
n_tv = sum(1 for r in transport["rows"] if r["status"] == "verified")
n_hv = sum(1 for r in hotels["rows"] if r["status"] == "verified")
n_flags = len(flags["flags"])
n_crit = sum(1 for f in flags["flags"] if f["severity"] == "critical")
n_warn = sum(1 for f in flags["flags"] if f["severity"] == "warning")

# ---------------------------------------------------------------- index.html
day_cards = []
for d in days:
    rows = [r for r in venues if r["day"] == d["n"]]
    nv = sum(1 for r in rows if r["status"] == "verified")
    np_ = sum(1 for r in rows if r["status"] == "partial")
    nu = sum(1 for r in rows if r["status"] == "unverified")
    alert = " daycrit" if d["n"] == 3 else ""
    day_cards.append(f"""<a class="daylink{alert}" href="itinerary.html#day-{d['n']}">
<div class="card" style="margin:0;height:100%">
<div class="small muted">Day {d['n']} · {esc(d['dow'])} · Nov {d['n']}, 2026</div>
<div style="font-weight:800;margin:2px 0">{esc(d['title'])}</div>
<div class="small muted" style="min-height:34px">{esc(d['theme'])}</div>
<div class="small">{nv} <span class="sv">✓</span> · {np_} <span class="sp">◐</span> · {nu} <span class="su">⚠</span>
{('<div class="small" style="color:var(--red);font-weight:700;margin-top:4px">⚠ closed-venue conflict</div>') if d['n'] == 3 else ''}</div>
</div></a>""")
day_cards_html = "".join(day_cards)

extra_css_index = """
.daylink{text-decoration:none;color:inherit;display:block}
.daycrit .card{border-color:#fecaca;background:#fffafa}
.grid.days{margin-top:6px}
"""

crit_flags = [f for f in flags["flags"] if f["severity"] == "critical"]
crit_html = "".join(
    f'<div class="alert"><b>⚑ {esc(f["id"])} — {esc(f["title"])}</b><br>{esc(f["detail"])}'
    f'<br><span class="small">Recommended: {esc(f["action"])}</span> '
    f'<a class="small" href="flagged.html#{f["id"]}">details →</a></div>'
    for f in crit_flags
)

index_body = f"""
<style>{extra_css_index}</style>
<div class="hero">
<h1>South Korea, Nov 1–9 2026 — the itinerary, fact-checked</h1>
<p>2 adults · SFO → Incheon · 8 nights Stanford Hotel Myeongdong (Seoul) · KTX to Busan ·
1 night L7 HAEUNDAE by LOTTE. Every line of the original itinerary was checked against
official sources (venues' own sites, Korea Tourism Organization, Seoul & Busan city sites,
Michelin Guide, major news outlets). Unverifiable values were left blank — never guessed.</p>
</div>

<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">
<div class="stat"><div class="n sv">{n_v + n_tv + n_hv}</div><div class="l">Verified entries</div></div>
<div class="stat"><div class="n sp">{n_p + (1 if n_hv < len(hotels['rows']) else 0)}</div><div class="l">Partially verified</div></div>
<div class="stat"><div class="n su">{n_u}</div><div class="l">Unverified</div></div>
<div class="stat"><div class="n">{n_t + len(transport['rows']) + len(hotels['rows'])}</div><div class="l">Itinerary lines checked</div></div>
<div class="stat"><div class="n" style="color:var(--red)">{n_crit}</div><div class="l">Critical flags</div></div>
<div class="stat"><div class="n" style="color:var(--amber)">{n_warn}</div><div class="l">Warnings</div></div>
</div>

{crit_html}

<h2>The 9 days</h2>
<div class="grid days">
{day_cards_html}
</div>

<h2>Browse by category</h2>
<div class="grid">
<a class="daylink" href="transport.html"><div class="card" style="margin:0"><b>🚄 Transport</b><div class="small muted">AREX & limousine bus, city metro routes, Namsan access, KTX, Busan metro — times & fares from official sources</div></div></a>
<a class="daylink" href="hotels.html"><div class="card" style="margin:0"><b>🏨 Hotels</b><div class="small muted">Stanford Hotel Myeongdong · L7 HAEUNDAE — check-in/out, addresses, fees</div></div></a>
<a class="daylink" href="food.html"><div class="card" style="margin:0"><b>🍜 Food, cafes & bars</b><div class="small muted">Myeongdong Kyoja, Gwangjang, Seongsu cafes, Ikseon-dong, speakeasies</div></div></a>
<a class="daylink" href="shopping.html"><div class="card" style="margin:0"><b>🛍 Shopping & experiences</b><div class="small muted">Dept stores, Olive Young, Seongsu K-fashion, photo booths</div></div></a>
<a class="daylink" href="attractions.html"><div class="card" style="margin:0"><b>🏛 Attractions</b><div class="small muted">Palaces, N Seoul Tower, Bukchon, DDP, COEX, Haeundae</div></div></a>
<a class="daylink" href="flagged.html"><div class="card" style="margin:0"><b>⚑ Flagged for review ({n_flags})</b><div class="small muted">Every irregularity & unverified item, with sources and recommended fixes</div></div></a>
</div>

<h2>How this was verified</h2>
<div class="card">
<ul class="clean small" style="line-height:1.9">
<li>✅ <b>Official sources first:</b> each row links the venue's own site or a government/tourism-board page (VisitKorea = Korea Tourism Organization, VisitSeoul, Seoul Metropolitan Government, Busan city, palace foundations, brand sites).</li>
<li>✅ <b>Trusted secondary sources:</b> Michelin Guide, major news (Korea Times, SBS, Yonhap), and consistent Korean directories (DiningCode, CatchTable) are used only for corroboration and are labeled as such.</li>
<li>✅ <b>No guessing:</b> if hours or prices could not be confirmed from an official source, the field was left blank and the item flagged <span class="b b-u">Unverified</span> or <span class="b b-p">Partial</span>.</li>
<li>✅ <b>Dates:</b> the original itinerary's "Nov 2, 2006" is treated as a typo for <b>2026</b> (Nov 1 2026 = Sunday, arrival day). All day-of-week checks use 2026.</li>
<li>✅ <b>Currency:</b> ₩1,000 ≈ $0.70-0.75 (Oct 2026); the site quotes official ₩ values and keeps the itinerary's $ figures for comparison.</li>
</ul>
</div>

<div class="tip"><b>Start here:</b> the one thing that truly needs a schedule change is
<b>Day 3 (Tue Nov 3) — Gyeongbokgung is closed on Tuesdays</b>. Everything else is either
confirmed or a small hours correction. See <a href="flagged.html#F2">flag F2</a>.</div>
"""
write("index.html", "Dashboard", index_body)

# ---------------------------------------------------------------- itinerary.html
sec = []
sec.append('<h1>Day-by-day itinerary — verified</h1>'
           '<p class="lede">All entries from the original plan, checked against official sources. '
           'Rows marked <span class="b b-p">Partial</span> or <span class="b b-u">Unverified</span> '
           'appear on the <a href="flagged.html">Flagged</a> page. '
           'Items prefixed “SUGGESTION” are additions, not part of the original plan.</p>')
for d in days:
    rows = [r for r in venues if r["day"] == d["n"]]
    note = ""
    if d["n"] == 1:
        note = ('<div class="daynote">✈️ <b>Arrival:</b> SFO → Incheon (ICN), landing Sunday Nov 1. '
                'Airport transfer options (AREX Express/All-Stop, Limousine Bus 6015, taxi) are on the '
                '<a href="transport.html">Transport page</a>. Hotel check-in from 15:00 — store bags if early. '
                'Evening: Myeongdong street food (informal — see <a href="flagged.html#F22">F22</a>).</div>')
    elif d["n"] == 3:
        note = ('<div class="daynote">⛔ <b>Conflict:</b> Gyeongbokgung Palace and the Royal Guard Changing '
                'Ceremony do not operate on Tuesdays. Day 3 is <b>Tuesday, Nov 3</b>. Move the palace to '
                'another day, or visit Changdeokgung instead (closed Mondays, open today). '
                'See <a href="flagged.html#F2">flag F2</a>.</div>')
    elif d["n"] == 7:
        note = ('<div class="sugg">💙 <b>Open day (Itaewon):</b> the original itinerary plans nothing here. '
                'Verified suggestions below — Leeum Museum of Art (open Sat), Rain Report Gyeongnidan flagship, '
                'Pig Restaurant 2 for dinner. See <a href="flagged.html#F24">F24</a>.</div>')
    elif d["n"] == 8:
        note = ('<div class="sugg">💙 <b>Free day:</b> no venues planned. Suggestion below: Changdeokgung Palace '
                '(open Sundays; ₩3,000; pairs with Bukchon & Ikseon-dong). See <a href="flagged.html#F24">F24</a>.</div>')
    elif d["n"] == 9:
        note = ('<div class="daynote">🚄 <b>Travel day:</b> morning KTX Seoul → Busan (₩54,400, ~2h15-3h), '
                'Busan Metro Line 1 → Seomyeon → Line 2 → Haeundae. L7 check-in from 15:00. '
                'Evening: Haeundae Beach + Haeundae Market (to 22:00).</div>')
    sec.append(f'<div class="dayhead" id="day-{d["n"]}"><span class="dn">Day {d["n"]}</span>'
               f'<h2>{esc(d["title"])}</h2><span class="dd">{esc(d["dow"])}, Nov {d["n"]} 2026 · {esc(d["hotel"])}</span></div>')
    sec.append(note)
    sec.append(venue_table(rows, show_day=False))
write("itinerary.html", "Itinerary", "".join(sec))

# ---------------------------------------------------------------- transport.html
body = ('<h1>Transport — verified times & fares</h1>'
        '<p class="lede">Airport transfers, city routing, the Namsan climb and the Seoul→Busan KTX, '
        'with the official source for every number. A T-money/Cashbee card works on Seoul metro/buses '
        'and in Busan; buy one at any convenience store.</p>'
        '<h2>Incheon Airport ⇄ Seoul / Myeongdong</h2>'
        + transport_table([r for r in transport["rows"] if r["id"] in ("TR1","TR2","TR3","TR4","TR5")])
        + '<h2>Getting around Seoul (from Myeongdong)</h2>'
        + transport_table([r for r in transport["rows"] if r["id"] in ("TR6","TR7","TR8")])
        + '<div class="tip"><b>Seoul basics:</b> Myeongdong Station (Line 4) and Euljiro 1-ga (Line 2) '
          'serve the hotel area; Line 2 (green) hits Seongsu, DDP (Dongdaemun Hist. & Culture Park), '
          'and Samseong/COEX directly; Jongno 3-ga (Lines 1/3/5) serves Ikseon-dong; '
          'Anguk (Line 3) serves Bukchon/Gyeongbokgung/Changdeokgung.</div>'
        + '<h2>Seoul → Busan (Day 9) & Busan</h2>'
        + transport_table([r for r in transport["rows"] if r["id"] in ("TR9","TR10")]))
write("transport.html", "Transport", body)

# ---------------------------------------------------------------- hotels.html
hcards = []
for r in hotels["rows"]:
    hcards.append(f"""<div class="card">
<h3>{esc(r['name'])} <span class="ko">{esc(r.get('ko',''))}</span> {badge(r['status'])}</h3>
<div class="kv">
<b>Nights</b><span>{esc(r['nights'])}</span>
<b>Address</b><span>{esc(r['address'])}</span>
<b>Check-in</b><span>{esc(r['checkin'])}</span>
<b>Check-out</b><span>{esc(r['checkout'])}</span>
<b>Notes</b><span>{esc(r['other'])}</span>
<b>Transit</b><span>🚇 {esc(r['transit'])}</span>
<b>Itinerary said</b><span>{esc(r['claim'])}</span>
</div>
<div style="margin-top:10px">{src_links(r)}</div>
<div class="chips" style="margin-top:8px">{flagchips(r)}</div>
</div>""")
write("hotels.html", "Hotels",
      "<h1>Hotels</h1><p class='lede'>Check-in/check-out times, addresses and policies, "
      "verified against the hotels' own materials or clearly-labeled booking platforms.</p>"
      + "".join(hcards))

# ---------------------------------------------------------------- category pages
def cat_page(fname, title, lede, cats, emoji):
    rows = [r for r in venues if r.get("category") in cats]
    rows.sort(key=lambda r: (r["day"], r["name"]))
    return (f'<h1>{emoji} {title}</h1><p class="lede">{lede}</p>'
            + venue_table(rows))

write("food.html", "Food, Cafes & Bars", cat_page(
    "food.html", "Food, Cafes & Bars",
    "Every restaurant, cafe, bar and market in the plan — the itinerary's claim next to the "
    "officially verified hours, addresses and prices.", {"food", "cafe", "bar", "market"}, "🍜"))

write("shopping.html", "Shopping & Experiences", cat_page(
    "shopping.html", "Shopping & Experiences",
    "Department stores, K-beauty, Seongsu K-fashion & eyewear, and the photo experiences — "
    "with verified hours and locations.", {"shopping", "photo"}, "🛍"))

write("attractions.html", "Attractions", cat_page(
    "attractions.html", "Attractions",
    "Palaces, towers, villages, plazas and beaches — hours, closures and admission fees from "
    "official sources. ⛔ Note Day 3's Tuesday closure of Gyeongbokgung (flag F2).",
    {"attraction"}, "🏛"))

# ---------------------------------------------------------------- flagged.html
sev_order = {"critical": 0, "warning": 1, "info": 2}
fl = sorted(flags["flags"], key=lambda f: (sev_order[f["severity"]], f["id"]))
fcards = []
for f in fl:
    srcs = "".join(
        f'<a class="src" href="{esc(s["url"])}" target="_blank" rel="noopener" title="{esc(s["label"])}">[{i}]&nbsp;{esc(s["label"])}</a>'
        for i, s in enumerate(f.get("sources", []), 1)
    )
    fcards.append(f"""<div class="flagcard {'crit' if f['severity']=='critical' else ('warn' if f['severity']=='warning' else 'info')}" id="{f['id']}">
<h3><span class="s {SEV_CLASS[f['severity']]}">{SEV_LABEL[f['severity']]}</span> {esc(f['id'])} · {esc(f['title'])}</h3>
<p>{esc(f['detail'])}</p>
<div class="act"><b>What to do:</b> {esc(f['action'])}</div>
<p class="small muted" style="margin-top:6px">Affects: {esc(', '.join(f.get('affects', []))) or '—'}</p>
{('<div style="margin-top:6px">' + srcs + '</div>') if srcs else '<p class="small muted" style="margin-top:6px">(no source — informational note)</p>'}
</div>""")
flagged_body = (
    '<h1>⚑ Flagged for Review</h1>'
    '<p class="lede">Everything that could not be fully confirmed, plus every discrepancy found between '
    'the original itinerary and official sources. <b>None of these block the trip</b> — they are '
    'published transparently so you can double-check before departure. Items marked '
    '<span class="s s-c">Critical</span> change the plan; <span class="s s-w">Warning</span> items need '
    'a call or a re-check; <span class="s s-i">Info</span> items are confirmations and notes.</p>'
    f'<div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">'
    f'<div class="stat"><div class="n" style="color:var(--red)">{n_crit}</div><div class="l">Critical</div></div>'
    f'<div class="stat"><div class="n" style="color:var(--amber)">{n_warn}</div><div class="l">Warnings</div></div>'
    f'<div class="stat"><div class="n" style="color:#0369a1">{n_flags - n_crit - n_warn}</div><div class="l">Info</div></div>'
    f'<div class="stat"><div class="n">{n_flags}</div><div class="l">Total flags</div></div></div>'
    + "".join(fcards)
)
write("flagged.html", "Flagged for Review", flagged_body)

# ---------------------------------------------------------------- link check
def link_check():
    problems = []
    files = [f for f, _ in PAGES]
    anchors = {}
    links = defaultdict(list)
    for fn in files:
        path = os.path.join(ROOT, fn)
        if not os.path.exists(path):
            problems.append(f"missing file {fn}")
            continue
        txt = open(path, encoding="utf-8").read()
        for m in re.finditer(r'id="([^"]+)"', txt):
            anchors.setdefault(fn, set()).add(m.group(1))
        for m in re.finditer(r'href="([^"]+)"', txt):
            links[fn].append(m.group(1))
    ok = bad = ext = 0
    for fn, hrefs in links.items():
        for h in hrefs:
            if h.startswith("http://") or h.startswith("https://"):
                ext += 1
                if " " in h.strip():
                    problems.append(f"{fn}: external URL contains space: {h}")
            elif h.startswith("#"):
                if h[1:] not in anchors.get(fn, set()):
                    problems.append(f"{fn}: dangling anchor {h}")
                    bad += 1
                else:
                    ok += 1
            elif re.match(r"^[^#]+\.html(#.*)?$", h):
                target = h.split("#")[0]
                frag = h.split("#")[1] if "#" in h else None
                if not os.path.exists(os.path.join(ROOT, target)):
                    problems.append(f"{fn}: broken page link {h}")
                    bad += 1
                elif frag and frag not in anchors.get(target, set()):
                    problems.append(f"{fn}: dangling anchor in {h}")
                    bad += 1
                else:
                    ok += 1
            elif h.startswith(("mailto:", "tel:")):
                continue
            else:
                problems.append(f"{fn}: unrecognized href {h}")
                bad += 1
    # external URL sanity in data files
    allrows = venues + transport["rows"] + hotels["rows"] + flags["flags"]
    for r in allrows:
        for s in r.get("sources", []):
            u = s["url"]
            if not u.startswith(("http://", "https://")):
                problems.append(f"bad source URL in data: {u}")
    print(f"link check: internal ok={ok} bad={bad} external={ext}")
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
    return bad == 0 and not problems

if __name__ == "__main__":
    ok = link_check()
    print("generated pages:", ", ".join(f for f, _ in PAGES))
    sys.exit(0 if ok else 1)
