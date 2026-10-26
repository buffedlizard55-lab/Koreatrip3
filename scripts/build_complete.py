#!/usr/bin/env python3
"""Build the separately scoped 16-day guide; no network or dependencies required."""
import html
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'complete'
old = json.loads((ROOT / 'data/itinerary.json').read_text())
new = json.loads((OUT / 'additions.json').read_text())
rows = old + new
DATES = ['Sun · Oct 31 / Nov 1', 'Mon · Nov 2', 'Tue · Nov 3', 'Wed · Nov 4', 'Thu · Nov 5', 'Fri · Nov 6', 'Sat · Nov 7', 'Sun · Nov 8', 'Mon · Nov 9', 'Tue · Nov 10', 'Wed · Nov 11', 'Thu · Nov 12', 'Fri · Nov 13', 'Sat · Nov 14', 'Sun · Nov 15', 'Mon · Nov 16']
TITLES = ['Arrival in Seoul', 'N Seoul Tower + Myeongdong', 'Palace + Bukchon ⚠', 'Seongsu + DDP', 'COEX + Gangnam', 'Ikseon + Insadong', 'Itaewon · open', 'Seoul · open', 'KTX to Busan', 'Haeundae + Dongbaek', 'Gamcheon + Songdo + Nampo', 'Aquarium + Haeundae', 'Busan · open', 'Gwangalli drone show', 'Busan · open', 'KTX to Seoul + Hongdae']
assert len(DATES) == len(TITLES) == 16
assert set(r['day'] for r in rows) == set(range(1,17))
for n, r in enumerate(rows, 1):
    assert r['item'] and r['plan'] and r['category'], n
    assert urlparse(r['source']).scheme == 'https' and urlparse(r['source']).netloc, n
    assert r.get('facts') or r.get('flag'), f'No source facts or caution at row {n}'
    # Every new row without a source-confirmed detail must visibly stay unverified.
    if n > len(old):
        r['verification'] = 'verified' if r['facts'] else 'unverified'
    assert r.get('verification') in ('verified', 'unverified'), n

E = lambda x: html.escape(str(x or ''), quote=True)
def nav(active):
    links = [('index.html','Overview'), ('days.html','Every day'), ('transit.html','Transit'), ('places.html','Places'), ('flagged.html','Flagged for review')]
    return '<nav aria-label="Main navigation">' + ''.join(f'<a {"aria-current=page" if active == label else ""} href="{url}">{E(label)}</a>' for url,label in links) + '</nav>'
def page(title, active, body):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#113c39"><title>{E(title)} | Korea field guide</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#content">Skip to content</a><header><div class="brand"><a href="index.html">K / Korea field guide</a><span>16 days · 2 adults · Seoul ↔ Busan</span></div>{nav(active)}</header><main id="content">{body}</main><footer>Research checked 26 Oct 2026 · Times and fares may change. Proposed dates are <strong>not confirmed bookings</strong>. <a href="../index.html">All existing research portals</a></footer></body></html>'''
def table(items):
    if not items: return '<p class="notice">No matching entries.</p>'
    cells = []
    for r in items:
        facts = E(r.get('facts')) if r.get('facts') else '<span class="unknown">Not confirmed</span>'
        status = 'Partly sourced' if r.get('facts') else 'Unverified'
        flag = f'<p class="caution"><b>Check:</b> {E(r["flag"])}</p>' if r.get('flag') else ''
        link = f'<a target="_blank" rel="noopener noreferrer" href="{E(r["source"])}">{E(r.get("sourceLabel") or urlparse(r["source"]).netloc)} ↗</a>'
        cells.append(f'<tr><td data-label="Plan item"><strong>{E(r["item"])}</strong><small>{E(r["category"])}</small></td><td data-label="Your plan">{E(r["plan"])}</td><td data-label="Official detail">{facts}{flag}</td><td data-label="Source and status"><span class="pill {"red" if not r.get("facts") else "green"}">{status}</span><br>{link}</td></tr>')
    return '<div class="table-wrap"><table><thead><tr><th>Plan item</th><th>Your plan (not verified)</th><th>Official detail / caveat</th><th>Status & official source</th></tr></thead><tbody>' + ''.join(cells) + '</tbody></table></div>'
def intro(kicker, title, subtitle): return f'<div class="heading"><p class="eyebrow">{E(kicker)}</p><h1>{E(title)}</h1><p>{E(subtitle)}</p></div>'
warning = '<aside class="notice"><strong>Schedule warning · Tuesday palace closure</strong><p>Day 3 is marked Tuesday but Gyeongbokgung is closed Tuesdays. The supplied “Nov 2, 2006” also conflicts with the weekday sequence; year/flight dates need confirmation. No bookings or itinerary swaps are assumed. See <a href="flagged.html">all flags</a>.</p></aside>'
daylinks = '<div class="day-grid">' + ''.join(f'<a href="day-{d}.html"><small>DAY {d:02d} · {E(DATES[d-1])}</small><strong>{E(TITLES[d-1])}</strong><span>{sum(x["day"]==d for x in rows)} plan {"item" if sum(x["day"]==d for x in rows)==1 else "items"} →</span></a>' for d in range(1,17)) + '</div>'
(OUT/'index.html').write_text(page('16-day dashboard','Overview',intro('THE TRIP AT A GLANCE','A full 16-day field guide','Choose a day, check the source-linked table, and travel with the unresolved details in view.') + warning + '<div class="metrics"><div><b>16</b><span>days in the brief</span></div><div><b>'+str(len(rows))+'</b><span>source-linked rows</span></div><div><b>'+str(sum(bool(x.get('flag')) for x in rows))+'</b><span>cautions to review</span></div></div><h2>Pick a day</h2>'+daylinks+'<p class="notice">Seoul base: Stanford Hotel Myeongdong (Days 1–9). Busan base: L7 Haeundae (Days 9–16). Return: Mercure Ambassador Seoul Hongdae (Day 16). Hotels named in the brief are not confirmed reservations. <a href="transit.html">See transport notes →</a></p>'))
(OUT/'days.html').write_text(page('Every day','Every day',intro('DAY-BY-DAY','All 16 days','Each day has its own readable plan and official-source table.')+warning+daylinks))
for d in range(1,17):
    group = [x for x in rows if x['day']==d]
    prev = f'<a href="day-{d-1}.html">← Day {d-1}</a>' if d>1 else '<a href="days.html">← All days</a>'
    nxt = f'<a href="day-{d+1}.html">Day {d+1} →</a>' if d<16 else '<a href="days.html">All days →</a>'
    body = intro(f'DAY {d:02d} · {DATES[d-1]}',TITLES[d-1],f'{len(group)} entries · proposed order only; times not booked.')
    if d == 3: body += warning
    if d in (7,8,13,15): body += '<aside class="notice">This day has no detailed stops in the original brief. Nothing has been invented to fill it.</aside>'
    body += '<div class="pager">'+prev+nxt+'</div>'+table(group)+'<div class="pager">'+prev+nxt+'</div>'
    (OUT/f'day-{d}.html').write_text(page(f'Day {d} · {TITLES[d-1]}','Every day',body))
transit = [x for x in rows if x['category']=='Transit' or x['item'].startswith('KTX')]
(OUT/'transit.html').write_text(page('Transit','Transit',intro('HOTEL TO HOTEL','Transit & transfers','Check live routes at the linked operator: exact departure, platform, walk, fare and travel time depend on the actual date.')+'<aside class="notice"><b>Key return leg:</b> L7 Haeundae → Busan Station (route/taxi quote unverified) → KORAIL KTX to Seoul Station → AREX <b>all-stop</b> to Hongik Univ. → Mercure Ambassador Seoul Hongdae. The non-stop AREX Express does not stop at Hongik Univ.</aside>'+table(transit)))
places = [x for x in rows if x['category'] not in ('Transit','Travel')]
(OUT/'places.html').write_text(page('Places','Places',intro('FOOD · STAYS · SIGHTS','Places & opening times','Officially sourced details are separated from proposals. Blank fields mean the specific venue detail was not confirmed.')+table(places)))
flags = [x for x in rows if x.get('flag') or not x.get('facts')]
(OUT/'flagged.html').write_text(page('Flagged for review','Flagged for review',intro('BEFORE YOU GO','Flagged for review',f'{len(flags)} rows contain unresolved timing, location, booking, source or schedule issues. Context-only links do not verify named venues.')+warning+table(flags)))
print(f'Built {len(rows)} rows across 16 days; {len(flags)} flagged; 21 HTML pages')
