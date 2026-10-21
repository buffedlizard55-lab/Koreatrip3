#!/usr/bin/env python3
"""Offline structural and source-link validation for the static Korea trip site."""
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [
    "index.html",
    "itinerary.html",
    "attractions.html",
    "shopping.html",
    "food.html",
    "stays.html",
    "getting-around.html",
    "sources.html",
    "flagged-for-review.html",
]


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.has_main = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(str(attr["id"]))
        if tag == "main":
            self.has_main = True
        for key in ("href", "src"):
            if attr.get(key):
                self.links.append(str(attr[key]))


def read_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(message: str) -> None:
    errors.append(message)


errors: list[str] = []
itinerary = read_json("data/itinerary.json")
transit = read_json("data/transit.json")
sources = read_json("data/sources.json")
flags = read_json("data/flags.json")
source_by_id = {source["id"]: source for source in sources}
entry_by_id = {entry["id"]: entry for entry in itinerary["entries"]}
flag_ids = {flag["id"] for flag in flags}
day_ids = {day["id"] for day in itinerary["days"]}

if len(source_by_id) != len(sources):
    fail("Duplicate source IDs found.")
if len(entry_by_id) != len(itinerary["entries"]):
    fail("Duplicate itinerary entry IDs found.")
if len(flag_ids) != len(flags):
    fail("Duplicate flag IDs found.")
if len(day_ids) != len(itinerary["days"]):
    fail("Duplicate day IDs found.")
if len(itinerary["days"]) != 9:
    fail(f"Expected 9 day cards; found {len(itinerary['days'])}.")

by_day = {day["id"]: day for day in itinerary["days"]}
if by_day.get("day-1", {}).get("rawDate") != "Oct.31/Nov 1":
    fail("Day 1 raw date string changed or is missing.")
if by_day.get("day-2", {}).get("rawDate") != "Monday—Nov 2,2006":
    fail("Day 2 raw date string changed or is missing.")
for day_id in ("day-7", "day-8"):
    if by_day.get(day_id, {}).get("emptyNote") != "Blank in the supplied itinerary; intentionally not filled in.":
        fail(f"{day_id} must remain explicitly blank.")

for source in sources:
    url = source.get("url", "")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        fail(f"Source {source.get('id')} has an invalid external URL: {url}")
    for field in ("publisher", "title", "evidenceType", "notes", "checkedOn"):
        if not source.get(field):
            fail(f"Source {source.get('id')} is missing {field}.")

for entry in itinerary["entries"]:
    if not entry.get("sourceIds"):
        fail(f"Itinerary row {entry['id']} has no official source link.")
    for source_id in entry["sourceIds"]:
        if source_id not in source_by_id:
            fail(f"Itinerary row {entry['id']} references missing source {source_id}.")
    if entry.get("dayId") and entry["dayId"] not in day_ids:
        fail(f"Itinerary row {entry['id']} references missing day {entry['dayId']}.")
    for flag_id in entry.get("flagIds", []):
        if flag_id not in flag_ids:
            fail(f"Itinerary row {entry['id']} references missing flag {flag_id}.")
    if entry.get("status") in {"review", "conflict"} and not entry.get("flagIds"):
        fail(f"Review/conflict row {entry['id']} has no linked review flag.")
    for field in ("name", "planned", "address", "hours", "days", "price", "officialFacts", "reviewNote", "status"):
        if field not in entry:
            fail(f"Itinerary row {entry['id']} is missing field {field}.")

for route in transit["routes"]:
    if not route.get("sourceIds"):
        fail(f"Transit row {route['id']} has no official source link.")
    for source_id in route["sourceIds"]:
        if source_id not in source_by_id:
            fail(f"Transit row {route['id']} references missing source {source_id}.")

for flag in flags:
    if not flag.get("sourceIds"):
        fail(f"Review flag {flag['id']} has no official source link.")
    for source_id in flag["sourceIds"]:
        if source_id not in source_by_id:
            fail(f"Review flag {flag['id']} references missing source {source_id}.")
    for affected_id in flag.get("affectedIds", []):
        if affected_id not in entry_by_id:
            fail(f"Review flag {flag['id']} references missing itinerary entry {affected_id}.")

html_parsers: dict[str, LinkParser] = {}
for file_name in HTML_FILES:
    path = ROOT / file_name
    if not path.exists():
        fail(f"Required page is missing: {file_name}")
        continue
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    html_parsers[file_name] = parser
    if not parser.has_main:
        fail(f"Page {file_name} has no semantic <main> element.")
    if "assets/site.css" not in parser.links:
        fail(f"Page {file_name} does not load the shared stylesheet.")
    if "assets/app.js" not in parser.links:
        fail(f"Page {file_name} does not load the shared application script.")

all_dynamic_ids = flag_ids | set(entry_by_id) | day_ids
for file_name, parser in html_parsers.items():
    page_path = ROOT / file_name
    for href in parser.links:
        if href.startswith(("https://", "http://", "mailto:", "tel:", "data:")):
            continue
        if href.startswith("//"):
            continue
        path_part, _, fragment = href.partition("#")
        if path_part:
            local_path = (page_path.parent / path_part).resolve()
            if not local_path.exists():
                fail(f"Broken local link in {file_name}: {href}")
                continue
            if fragment and local_path.suffix == ".html":
                target_name = local_path.name
                target_parser = html_parsers.get(target_name)
                if target_parser and fragment not in target_parser.ids and fragment not in all_dynamic_ids:
                    fail(f"Missing anchor in {file_name}: {href}")
        elif fragment and fragment not in parser.ids and fragment not in all_dynamic_ids:
            fail(f"Missing page anchor in {file_name}: {href}")

for data_path in ("data/itinerary.json", "data/transit.json", "data/sources.json", "data/flags.json"):
    if not (ROOT / data_path).is_file():
        fail(f"Required runtime data file is missing: {data_path}")

if errors:
    print("Site validation FAILED:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(
    "Site validation passed: "
    f"{len(HTML_FILES)} pages, {len(itinerary['days'])} days, "
    f"{len(itinerary['entries'])} itinerary rows, {len(transit['routes'])} transit routes, "
    f"{len(sources)} official source links, {len(flags)} review notes."
)
