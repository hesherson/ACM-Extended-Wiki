#!/usr/bin/env python3
"""
PILLAR guide builder.

WHY THIS EXISTS. Every output page is SELF-CONTAINED: css inlined, no external stylesheet, no framework. That is
what lets a card survive being emailed, saved to a phone, opened with no signal, and printed. The cost of that is
duplication, so the duplication is moved to build time: you edit one stylesheet and one layout, run this, and every
page is rewritten.

    python3 build.py

    src/_pillar.css       the stylesheet. Edit once, applies everywhere.
    src/content/*.html    one file per page. Body content ONLY, no <html>, no <style>.
    docs/                 output. This is the folder GitHub Pages serves.

ADDING A PAGE: drop a file in src/content/ and add a line to PAGES below. That is the whole process.
ADDING AN IMAGE: put it in docs/img/ and reference it as img/thing.png from any page.
"""
import os, re, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
OUT = os.path.join(ROOT, "docs")

VERSION = "0.9.873"

# slug, filename, nav title, nav group.
# Order here is the order in the sidebar. Groups are emitted in first-seen order.
PAGES = [
    ("index",        "index.html",        "Start here",          "Overview"),
    ("ventilator",   "ventilator.html",   "Ventilator",          "Systems"),
    ("oxygen",       "oxygen.html",       "Oxygen delivery",     "Systems"),
    ("bleeding",     "bleeding.html",     "Bleeding and shock",  "Systems"),
    ("airway",       "airway.html",       "Airway and chest",    "Systems"),
    ("circulation",  "circulation.html",  "Rhythms and drugs",   "Systems"),
    ("medications",  "medications.html",  "Medications",         "Systems"),
    ("access",       "access.html",       "Access and blood",    "Systems"),
    ("tbi",          "tbi.html",          "Head injury",         "Systems"),
    ("flight",       "flight.html",       "Flight and altitude", "Systems"),
    ("menu",         "menu.html",         "Medical menu",        "Interface"),
    ("accessibility","accessibility.html","Accessibility",       "Interface"),
    ("settings",     "settings.html",     "Settings reference",  "Reference"),
    ("zeus",         "zeus.html",         "Zeus modules",        "Reference"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;900&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>
<div class="shell">
"""

FOOT = """
<footer>
  <span class="brand">PILLAR</span> // ACM EXTENDED FIELD GUIDE // v{version} // BUILT {built}
</footer>
</main>
</div>
</body>
</html>
"""


def sidebar(current):
    """Sidebar nav. Groups in first-seen order, current page marked."""
    out = ['<aside class="side">',
           '  <div class="brand">PILL<span>A</span>R</div>',
           f'  <div class="ver">ACM Extended // v{VERSION}</div>',
           '  <nav class="nav">']
    seen = []
    for slug, fname, title, group in PAGES:
        if group not in seen:
            seen.append(group)
            out.append(f'    <div class="grp">{group}</div>')
        cls = ' class="on"' if slug == current else ""
        out.append(f'    <a href="{fname}"{cls}>{title}</a>')
    out += ['  </nav>', '</aside>', '<main class="main">']
    return "\n".join(out)


def build():
    css = open(os.path.join(SRC, "_pillar.css"), encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    built = datetime.date.today().isoformat()
    written = 0
    missing = []

    for slug, fname, title, group in PAGES:
        cpath = os.path.join(SRC, "content", slug + ".html")
        if not os.path.exists(cpath):
            missing.append(slug)
            continue
        body = open(cpath, encoding="utf-8").read()
        page = (HEAD.format(title=f"PILLAR | {title}", css=css)
                + sidebar(slug) + "\n" + body
                + FOOT.format(version=VERSION, built=built))
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(page)
        written += 1

    # .nojekyll stops GitHub Pages running Jekyll over the output, which otherwise
    # silently eats any file or folder beginning with an underscore.
    open(os.path.join(OUT, ".nojekyll"), "w").write("")

    print(f"built {written} page(s) into docs/")
    if missing:
        print("no content file yet for: " + ", ".join(missing))
        print("  create src/content/<slug>.html to fill one in")


if __name__ == "__main__":
    build()
