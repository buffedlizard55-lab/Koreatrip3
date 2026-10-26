#!/usr/bin/env python3
"""Structural guardrails for the user-facing, 16-day root itinerary dataset."""
import collections
import json
from pathlib import Path
from urllib.parse import urlparse

DATA = Path(__file__).resolve().parents[1] / "data" / "itinerary.json"
rows = json.loads(DATA.read_text(encoding="utf-8"))
assert isinstance(rows, list) and rows, "Root itinerary must be a non-empty JSON array"

seen_days = set()
for number, row in enumerate(rows, start=1):
    context = f"Row {number} ({row.get('item')!r})"
    assert isinstance(row.get("day"), int) and 1 <= row["day"] <= 16, f"{context}: day must be 1–16"
    seen_days.add(row["day"])
    for field in ("date", "category", "item", "plan", "sourceLabel", "source"):
        assert isinstance(row.get(field), str) and row[field].strip(), f"{context}: missing {field}"
    assert row.get("verification") in {"verified", "unverified"}, f"{context}: invalid verification status"
    assert urlparse(row["source"]).scheme == "https" and urlparse(row["source"]).netloc, f"{context}: source must be HTTPS"
    if row["verification"] == "unverified":
        assert row.get("flag", "").strip(), f"{context}: unverified row must have a review flag"
    for source in row.get("sourceAlternates", []):
        assert source.get("label", "").strip(), f"{context}: alternate source needs a label"
        url = urlparse(source.get("url", ""))
        assert url.scheme == "https" and url.netloc, f"{context}: alternate source must be HTTPS"

expected = set(range(1, 17))
assert seen_days == expected, f"Day coverage mismatch: missing {sorted(expected - seen_days)}; unexpected {sorted(seen_days - expected)}"
for day in (13, 15):
    day_rows = [row for row in rows if row["day"] == day]
    assert day_rows and all(row["verification"] == "unverified" for row in day_rows), f"Day {day} is deliberately unscheduled and must remain flagged"

counts = collections.Counter(row["verification"] for row in rows)
print(f"Root itinerary valid: {len(rows)} rows across Days 1–16; verified/source-linked={counts['verified']}, unverified/flagged={counts['unverified']}; every row has an HTTPS source.")
