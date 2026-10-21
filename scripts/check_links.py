#!/usr/bin/env python3
"""Internal link checker: verify every local href/src (and #anchor) resolves."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATTR = re.compile(r'(?:href|src)="([^"]+)"')
IDS = re.compile(r'id="([^"]+)"')

pages = []
for dirpath, _, files in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.join(dirpath, f))

id_cache = {}
def ids_of(path):
    if path not in id_cache:
        with open(path, encoding="utf-8") as fh:
            id_cache[path] = set(IDS.findall(fh.read()))
    return id_cache[path]

errors = []
external = 0
for page in sorted(pages):
    with open(page, encoding="utf-8") as fh:
        content = fh.read()
    for link in ATTR.findall(content):
        if link.startswith(("http://", "https://")):
            external += 1
            continue
        if link.startswith(("mailto:", "tel:", "javascript:")):
            continue
        path_part, _, anchor = link.partition("#")
        target = page if not path_part else os.path.normpath(os.path.join(os.path.dirname(page), path_part))
        if not os.path.exists(target):
            errors.append(f"{os.path.relpath(page, ROOT)} -> MISSING FILE {link}")
            continue
        if anchor and target.endswith(".html") and anchor not in ids_of(target):
            errors.append(f"{os.path.relpath(page, ROOT)} -> MISSING ANCHOR {link}")

print(f"checked {len(pages)} pages, {external} external links (not fetched)")
if errors:
    print("ERRORS:")
    for e in errors:
        print(" ", e)
    sys.exit(1)
print("all internal links OK")
