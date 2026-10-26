#!/usr/bin/env python3
"""Build the separately scoped 16-day guide; no network or dependencies required."""
import html
import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'complete'
# This independent archive supplies its own Week 2 rows; avoid duplicating
# the root dashboard's newly integrated Days 10–16.
old = [r for r in json.loads((ROOT / 'data/itinerary.json').read_text()) if r['day'] <= 9]
new = json.loads((OUT / 'additions.json').read_text())
rows = old + new
# The root dataset retains a legacy KORAIL URL that now returns 404. For this
# generated companion only, route inherited rows through KORAIL's current official
# English booking/search page; do not edit or write back the root-owned dataset.
legacy_korail_url = 'https://smart.letskorail.com/ebizbf/EbizBfTicketSearchM.do?lang=EN'
current_korail_url = 'https://www.korail.com/global/eng/main'
for row in old:
    if row.get('source') == legacy_korail_url:
        row['source'] = current_korail_url
        row['sourceLabel'] = 'KORAIL official ticket search'
# Preserve the itinerary's labels exactly enough to expose ambiguity; never infer a
# year or turn weekday-only Week 2 labels into calendar dates.
DATES = [
    'Sun · Oct 31 / Nov 1 (year unresolved)',
    'Mon · Nov 2, 2006 (as supplied)',
    'Tue · Nov 3 (year not supplied)',
    'Wed · Nov 4 (year not supplied)',
    'Thu · Nov 5 (year not supplied)',
    'Fri · Nov 6 (year not supplied)',
    'Sat · Nov 7 (year not supplied)',
    'Sun · Nov 8 (year not supplied)',
    'Mon · Nov 9 (year not supplied)',
    'Tue · date/year not supplied',
    'Wed · date/year not supplied',
    'Thu · date/year not supplied',
    'Fri · date/year not supplied',
    'Sat · date/year not supplied',
    'Sun · date/year not supplied',
    'Mon · date/year not supplied',
]
TITLES = ['Arrival in Seoul', 'N Seoul Tower + Myeongdong', 'Palace + Bukchon ⚠', 'Seongsu + DDP', 'COEX + Gangnam', 'Ikseon + Insadong', 'Itaewon · open', 'Seoul · open', 'KTX to Busan', 'Haeundae + Dongbaek', 'Gamcheon + Songdo + Nampo', 'Aquarium + Haeundae', 'Busan · open', 'Gwangalli drone show', 'Busan · open', 'KTX to Seoul + Hongdae']
assert len(DATES) == len(TITLES) == 16
assert set(r['day'] for r in rows) == set(range(1,17))
for n, r in enumerate(rows, 1):
    assert r['item'] and r['plan'] and r['category'], n
    assert urlparse(r['source']).scheme == 'https' and urlparse(r['source']).netloc, n
    for source in r.get('additionalSources', []):
        assert source.get('label') and urlparse(source.get('url', '')).scheme == 'https' and urlparse(source.get('url', '')).netloc, (n, source)
    assert r.get('facts') or r.get('flag'), f'No source facts or caution at row {n}'
    # Every new row without a source-confirmed detail must visibly stay unverified.
    if n > len(old):
        r['verification'] = 'verified' if r['facts'] else 'unverified'
    assert r.get('verification') in ('verified', 'unverified'), n

E = lambda x: html.escape(str(x or ''), quote=True)
def nav(active):
    links = [
        ('index.html', 'Overview'), ('days.html', 'Every day'),
        ('transit.html', 'Transit'), ('food.html', 'Food'),
        ('shopping.html', 'Shopping'), ('attractions.html', 'Attractions'),
        ('stays.html', 'Stays'), ('places.html', 'Places'),
        ('analysis.html', 'Analysis'), ('flagged.html', 'Flagged for review'),
    ]
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
        links = [(r.get('sourceLabel') or urlparse(r['source']).netloc, r['source'])]
        links.extend((s.get('label') or urlparse(s['url']).netloc, s['url']) for s in r.get('additionalSources', []))
        source_links = '<br>'.join(f'<a target="_blank" rel="noopener noreferrer" href="{E(url)}">{E(label)} ↗</a>' for label, url in links)
        cells.append(f'<tr><td data-label="Plan item"><strong>{E(r["item"])}</strong><small>{E(r["category"])}</small></td><td data-label="Your plan">{E(r["plan"])}</td><td data-label="Official detail">{facts}{flag}</td><td data-label="Source and status"><span class="pill {"red" if not r.get("facts") else "green"}">{status}</span><br>{source_links}</td></tr>')
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
transit_tools = [
    ('Busan Metro Cyber Station', 'Official English station map and route planner for transfers such as Haeundae → Seomyeon → Busan Station.', 'https://www2.humetro.busan.kr/homepage/cyberstation/mapeng.do', 'Busan Transportation Corporation'),
    ('Busan real-time road information', 'Official Busan ITS page for current road conditions, traffic notices and camera feeds; it is not a bus timetable.', 'https://its.busan.go.kr/', 'Busan Metropolitan City'),
    ('Seoul Subway route search', 'Official Seoul visitor resource for subway route search and live timetable information.', 'https://english.seoul.go.kr/new-subway-app-exclusive-for-foreign-residents-and-tourists/', 'Seoul Metropolitan Government'),
    ('KORAIL date-specific train search', 'Search the actual Busan–Seoul date for services, departure times, fares and seat availability.', 'https://www.korail.com/global/eng/main', 'KORAIL'),
    ('AREX Express vs All-Stop guidance', 'Korea Tourism Organization confirms the All-Stop train serves Hongik Univ.; the Express does not.', 'https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=140654', 'Korea Tourism Organization'),
]
tool_cards = ''.join(f'<a class="tool-card" target="_blank" rel="noopener noreferrer" href="{E(url)}"><strong>{E(title)}</strong><span>{E(description)}</span><small>{E(provider)} ↗</small></a>' for title,description,url,provider in transit_tools)
tool_section = '<section><h2>Official route and live-service tools</h2><p>Use these operator or government links for the exact travel date. This guide deliberately leaves unconfirmed fares and door-to-door times blank.</p><div class="tool-grid">'+tool_cards+'</div></section>'
transit_body = intro('HOTEL TO HOTEL','Transit & transfers','Use the named hotel bases and verified station sequences; check exact times, fares and entrances in official live tools for the actual travel date.')+'<aside class="notice"><b>Return to Seoul:</b> From L7 Haeundae, the official metro map supports a Line 2 → Seomyeon transfer → Line 1 to Busan Station. Then use KORAIL to Seoul Station and AREX All-Stop to Hongik Univ. (the non-stop Express does not stop there). Hotel-to-station walks, live timetable, fare and KTX booking remain unconfirmed.</aside>'+tool_section+intro('SOURCE-LINKED ROUTES','Transit items in the itinerary','Each row links to official evidence; unsupported hotel-door details and journey-time estimates stay flagged.')+table(transit)
(OUT/'transit.html').write_text(page('Transit','Transit',transit_body))
places = [x for x in rows if x['category'] not in ('Transit','Travel')]
category_cards = '<div class="tool-grid"><a class="tool-card" href="food.html"><strong>Food</strong><span>Meals, cafés and unassigned breakfasts/dinners.</span><small>Browse food items →</small></a><a class="tool-card" href="shopping.html"><strong>Shopping</strong><span>Markets, shops and shopping districts.</span><small>Browse shopping items →</small></a><a class="tool-card" href="attractions.html"><strong>Attractions</strong><span>Sights, activities and open-day notes.</span><small>Browse activities →</small></a><a class="tool-card" href="stays.html"><strong>Stays</strong><span>Named hotels and checkout/check-in questions.</span><small>Browse hotel items →</small></a></div>'
(OUT/'places.html').write_text(page('Places','Places',intro('BROWSE BY CATEGORY','Places & opening times','Choose a category or browse the combined list. Official details are separated from proposals; unknown facts remain blank.')+category_cards+table(places)))
for filename,label,categories,subtitle in [
    ('food.html','Food',{'Food','Nightlife'},'Meals and cafés from the supplied plan. Unnamed venues remain blank rather than being invented.'),
    ('shopping.html','Shopping',{'Shopping'},'Markets, shops and shopping areas from the supplied plan. Branch-level details remain flagged when unconfirmed.'),
    ('attractions.html','Attractions',{'Activities'},'Sights, scheduled activities and explicitly open days, with verified facts separated from planning proposals.'),
    ('stays.html','Stays',{'Stay'},'The named hotel bases, booking/check-in status and unresolved departure details.'),
]:
    category_rows = [x for x in rows if x['category'] in categories]
    (OUT/filename).write_text(page(label,label,intro('CATEGORY VIEW',label,subtitle)+table(category_rows)))

from collections import Counter
by_day = Counter(x['day'] for x in rows)
by_category = Counter(x['category'] for x in rows)
max_rows = max(by_day.values())
dense_days = [d for d in range(1,17) if by_day[d] == max_rows]
dense_label = ', '.join(f'<a href="day-{d}.html">Day {d}</a>' for d in dense_days)
open_days = [7,8,13,15]
open_labels = ', '.join(f'<a href="day-{d}.html">Day {d}</a>' for d in open_days)
category_summary = ''.join(f'<div><b>{E(category)}</b><span>{count} {"row" if count == 1 else "rows"}</span></div>' for category,count in sorted(by_category.items()))
analysis_body = intro('PACE · CONFLICTS · DECISIONS','Trip analysis','A source-aware planning review of the supplied 16-day sequence. Row counts are not time estimates, and no calendar year is inferred.')
analysis_body += '<div class="metrics"><div><b>16</b><span>days represented</span></div><div><b>'+str(len(rows))+'</b><span>source-linked plan rows</span></div><div><b>'+str(max_rows)+'</b><span>largest day row-count</span></div></div>'
analysis_body += '<section class="analysis-card"><h2>Calendar labels remain unresolved</h2><p>Day 1 preserves “Oct 31 / Nov 1”; Day 2 preserves “Nov 2, 2006” as written, with the weekday conflict flagged. Days 10–16 retain only the supplied weekday labels because no calendar dates or year were supplied. Nothing is normalized or inferred.</p></section>'
analysis_body += '<section class="analysis-card"><h2>Pacing and coverage</h2><p>The largest raw row count is on '+dense_label+' ('+str(max_rows)+' rows). This is a content-density signal only—not a duration, priority or recommendation to remove a stop. Days 7, 8, 13 and 15 remain open because no activities were supplied: '+open_labels+'.</p><div class="category-summary">'+category_summary+'</div></section>'
analysis_body += '<section class="analysis-card"><h2>Decisions to resolve before booking</h2><ul><li><b>Day 3:</b> Gyeongbokgung is closed Tuesdays on the official listing; a date change is not assumed.</li><li><b>Days 10 and 12:</b> Busan X the SKY is duplicated; its operator and Visit Busan list different adult prices, so choose one visit and recheck the operator before purchase.</li><li><b>Day 10:</b> Sky Capsule bookings are one-way; confirm the return mode and date-specific availability.</li><li><b>Day 11:</b> The supplied order returns to BIFF/Jagalchi/Nampo after Songdo; possible regrouping is noted, not silently applied.</li><li><b>Day 14:</b> Gwangalli show type depends on which Saturday of the month; the recurring schedule does not specify fifth Saturdays, and organizer/tourism listings differ on duration.</li><li><b>Day 16:</b> Busan–Seoul KTX, hotel checkout, fares and departure times are not booked or confirmed.</li></ul><p>See <a href="flagged.html">Flagged for review</a> for row-by-row gaps and source conflicts.</p></section>'
analysis_body += '<aside class="notice"><b>No invented trip total:</b> Flight, hotel, train and restaurant costs or reservations are incomplete. Prices with conflicting official listings remain flagged; only source-backed details appear in itinerary rows.</aside>'
(OUT/'analysis.html').write_text(page('Trip analysis','Analysis',analysis_body))
flags = [x for x in rows if x.get('flag') or not x.get('facts')]
(OUT/'flagged.html').write_text(page('Flagged for review','Flagged for review',intro('BEFORE YOU GO','Flagged for review',f'{len(flags)} rows contain unresolved timing, location, booking, source or schedule issues. Context-only links do not verify named venues.')+warning+table(flags)))
print(f'Built {len(rows)} rows across 16 days; {len(flags)} flagged; 26 HTML pages')
