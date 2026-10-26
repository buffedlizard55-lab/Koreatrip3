#!/usr/bin/env python3
"""Validate full-trip coverage and strict new-row evidence invariants."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
rows = json.loads((root/'data/itinerary.json').read_text())
assert {r['day'] for r in rows} == set(range(1, 17))
assert len(rows) == 109
for n, r in enumerate(rows, 1):
    assert all(k in r for k in ('day','date','category','item','plan','facts','source','sourceLabel','verification','flag','checkedAt','sourceScope')), n
    assert r['source'].startswith('https://'), n
    assert r['verification'] in ('verified','unverified'), n
    if r['day'] >= 10:
        assert r['checkedAt'] == '2026-10-26', n
        assert r['flag'], n
        assert (bool(r['facts']) == (r['verification'] == 'verified')), n
        assert 'date and year not supplied' in r['date'], n
for day in (13,15):
    assert len([r for r in rows if r['day']==day]) == 1
    assert not next(r for r in rows if r['day']==day)['facts']
audit = json.loads((root/'data/week2-audit.json').read_text())
assert audit['rows'] == len([r for r in rows if r['day']>=10]) == 41
known={s['url'] for s in audit['sources']}
assert all(r['source'] in known for r in rows if r['day']>=10)
print('PASS: 16 days, 109 rows; all 41 Week 2 rows source-linked and flagged, unknown facts blank')
