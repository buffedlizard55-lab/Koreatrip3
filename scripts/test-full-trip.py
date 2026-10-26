#!/usr/bin/env python3
"""Evidence invariants + generated-page completeness. No external network needed."""
import json, re, hashlib, subprocess, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/full-trip.json').read_text()); S={s['id']:s for s in json.loads((ROOT/'data/current-sources.json').read_text())}
assert D['travelYear'] is None and D['travelers']==2
assert [d['day'] for d in D['days']]==list(range(1,17))
assert set(r['day'] for r in D['rows'])==set(range(1,17))
assert len({r['id'] for r in D['rows']})==len(D['rows'])
allowed={'english.visitseoul.net','english.seoul.go.kr','english.visitkorea.or.kr','www.stanford-hotel.com','www.nseoultower.co.kr','www.korail.com','www2.humetro.busan.kr','www.lottehotel.com','all.accor.com','www.visitbusan.net','visitbusan.net','www.bluelinepark.com','www.busanxthesky.com','www.visitsealife.com','www.gwangallimdrone.co.kr','locations.musinsa.com','global.margesherwood.com','www.adererror.com'}
for s in S.values():
 u=urlparse(s['url']); assert u.scheme=='https' and u.hostname in allowed, s
 assert s['checked']=='2026-10-26' and s['evidence'] and s['method']
for r in D['rows']:
 assert r['sourceIds'] and all(k in S for k in r['sourceIds']), r
 assert r['flag'] and r['status'] in {'partial','unverified'}
 fields=[r[k] for k in ['hours','closed','address','price','facts']]
 if r['status']=='unverified':assert not any(fields),r
 else:assert any(fields),r
 assert all('$' not in r[k] for k in ['hours','closed','address','price','facts']),r
 assert r['checked']=='2026-10-26'
byid={r['id']:r for r in D['rows']}
assert byid['R018']['address']=='' # unresolved Kyoja address
assert byid['R075']['hours']=='' # unresolved Cheongsapo hours
assert byid['R061']['price']=='' and '45 minutes' in byid['R062']['flag']
assert 'Tuesdays' in byid['R023']['closed']
for i in [8,13,15]: assert len([r for r in D['rows'] if r['day']==i])==1
class Audit(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.rows=[];self.row=None
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id' in a:self.ids.append(a['id'])
  if t=='tr':self.row={'id':a.get('id'),'links':[]}
  if t=='a' and self.row is not None and a.get('href','').startswith('https://'):self.row['links'].append(a['href'])
 def handle_endtag(self,t):
  if t=='tr' and self.row is not None:self.rows.append(self.row);self.row=None
files=list(ROOT.glob('*.html'))
for f in files:
 p=Audit();p.feed(f.read_text());assert len(p.ids)==len(set(p.ids)),f'Duplicate IDs: {f}'
 for row in p.rows:
  if row['id'] and row['id'] in byid:assert row['links'],f'Unsourced row {row} in {f}'
 if f.name in ['itinerary.html','flagged-for-review.html']:
  assert {r['id'] for r in p.rows if r['id']}==set(byid),f'Incomplete dataset on {f}'
 assert '<h1>' in f.read_text() and 'name="viewport"' in f.read_text()
# Deterministic rebuild: fails if committed HTML is stale.
before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
subprocess.run([sys.executable,str(ROOT/'scripts/build-full-trip.py')],cwd=ROOT,check=True)
for f in files:assert before[f.name]==hashlib.sha256(f.read_bytes()).hexdigest(),f'Stale generated file: {f.name}'
print(f'PASS: {len(D["rows"])} entries, 16 days, {len(S)} official references, empty-field/evidence invariants, unique IDs and deterministic HTML')
