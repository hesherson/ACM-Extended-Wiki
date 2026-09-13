#!/usr/bin/env python3
"""Check generated wiki navigation and compare the checked-in build with its sources."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            value = values["id"]
            if value in self.ids:
                self.duplicates.append(value)
            self.ids.add(value)
        for name in ("href", "src"):
            if name in values:
                self.links.append(values[name])

def normalize(text):
    # Build dates and JSON object ordering are not content changes.
    text = re.sub(r"Updated \d{4}-\d{2}-\d{2}", "Updated DATE", text)
    def data(match):
        return "var " + match.group(1) + "=" + json.dumps(
            json.loads(match.group(2)), ensure_ascii=True, sort_keys=True,
            separators=(",", ":")
        ) + ";"
    return re.sub(r"var (TERMS|IDX)=(.*);", data, text)

pages = {path.name: Page(path.read_text(encoding="utf-8"))
         for path in DOCS.glob("*.html")}
errors = []
for filename, page in pages.items():
    errors.extend(f"{filename}: duplicate id {value}" for value in page.duplicates)
    for href in page.links:
        url = urlsplit(href)
        if url.scheme or url.netloc:
            continue
        path = unquote(url.path) or filename
        target = (DOCS / path).resolve()
        if not target.is_relative_to(DOCS.resolve()):
            errors.append(f"{filename}: reference escapes docs: {href}")
        elif not target.is_file():
            errors.append(f"{filename}: missing target {href}")
        elif url.fragment and path in pages and unquote(url.fragment) not in pages[path].ids:
            errors.append(f"{filename}: missing anchor {href}")
    original = subprocess.run(
        ["git", "show", f"HEAD:docs/{filename}"],
        cwd=ROOT, check=False, capture_output=True, text=True
    )
    if original.returncode:
        errors.append(f"{filename}: generated page is not checked in")
    else:
        generated = (DOCS / filename).read_text(encoding="utf-8")
        if normalize(original.stdout) != normalize(generated):
            errors.append(f"{filename}: checked-in output differs from build.py output")

if errors:
    raise SystemExit("\n".join(errors))
print(f"Checked {len(pages)} pages: generated content, IDs, local links and assets match.")
