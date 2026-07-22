# PILLAR // ACM Extended Field Guide

Living documentation. Every output page is self-contained: CSS inlined, no external stylesheet, no framework,
no build dependency at read time. That is deliberate. It means a page survives being emailed, saved to a phone,
opened with no signal, and printed.

## Editing

    src/_pillar.css        the stylesheet. Edit once, applies to every page.
    src/content/*.html     one file per page. BODY CONTENT ONLY, no <html>, no <style>.
    build.py               inlines the CSS into the layout and writes docs/
    docs/                  output. This is what GitHub Pages serves.

Rebuild after any change:

    python3 build.py

It prints which pages still have no content file, so the to-do list maintains itself.

## Adding a page

1. Create `src/content/myslug.html` with body content only.
2. Add a line to `PAGES` in `build.py`: slug, filename, nav title, nav group.
3. Run `python3 build.py`. The sidebar updates itself everywhere.

## Adding a picture

Drop it in `docs/img/` and reference it as `img/name.png`:

    <figure>
      <img src="img/vent-panel.png" alt="Ventilator panel">
      <figcaption>Sparrow panel, live screen</figcaption>
    </figure>

There is a dashed placeholder style for pictures you have not taken yet:

    <figure class="placeholder">Panel screenshot goes here</figure>

## Components

    .principle        the one-thing callout at the top of a page
    details.dd        dropdown for anything needing a long explanation
    .card + .grid     a discrete thing with settings in cells
    table.t           plain table, wrap in .scroll if wide
    .flags            red flags list
    figure            picture, or figure.placeholder for a gap

## Hosting on GitHub Pages

Settings, Pages, source: deploy from branch, folder `/docs`. Nothing else.
`.nojekyll` is written automatically so Jekyll does not eat underscore files.

## Known limitation

Fonts load from Google Fonts, so offline they fall back to system defaults. The layout survives, the
typography does not. To fix, drop the woff2 files into `docs/fonts/` and swap the `<link>` in `build.py`
for a local `@font-face` block.

## Converting game textures to figures

`paa2png.py` decodes the addon's `.paa` textures so they can be used as figures.

    python3 paa2png.py <paa-dir> <out-dir> [name-filter ...]
    python3 paa2png.py ../work4/acmi_infusion/ui docs/img alarm HPMK

Every texture in this addon is DXT5 (type 0xFF05), which is the only codec implemented. Anything else is
reported and skipped rather than written as a corrupt image. LZO decompression uses `python-lzo`:

    pip install python-lzo

Two practical notes. Decoding is pure Python, so a 2048x2048 texture takes a while; the 256 and 512 icons
are near instant and are usually what a figure wants anyway. And a name filter is worth using, because
converting all 213 at once is slow and most of them are body overlays that mean nothing out of context.

## Glossary terms

Terms live in `src/glossary_terms.py`. The glossary page and the in-page popups are both generated from
that one dict, so they cannot disagree.

To link a term in any content file:

    {{peep}}                 renders as the term's own name
    {{peep|hold pressure}}   renders your wording, same popup

Unknown slugs are reported by name at build time rather than shipped as literal braces.

Writing rules for definitions: assume no medical background, never define a term using another undefined
term, two or three short sentences, and say what it IS before why it matters.

## Search

`build.py` builds one search record per section and inlines the index into every page, so search works
even opened from disk with no server. Section anchors are generated automatically from h2 text.

Large guides will grow the index. If page weight becomes a problem, switch to a single `search-index.json`
fetched on demand, at the cost of search no longer working offline from a file.
