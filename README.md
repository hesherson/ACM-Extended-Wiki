# ACM Extended Wiki

Static reference site for ACM Extended. The existing Python builder produces self-contained HTML pages in `docs/`, with offline search, inline styles and inline browser scripts.

## Edit and build

- `src/content/*.html`: article bodies
- `src/_pillar.css`: shared styles
- `src/reference.js`: calculators, curve inspection, automatic glossary links, keyboard controls and printing
- `src/glossary_terms.py`: glossary definitions
- `src/reference-data.json`: source snapshot used for the reference refresh
- `build.py`: navigation, layout, glossary expansion and search index
- `docs/`: output served by the existing GitHub Pages configuration

Run:

```sh
python3 build.py
python3 scripts/check_wiki.py
node --check src/reference.js
```

The output comparison in `check_wiki.py` is intended for CI after generated pages are committed. During editing, it reports the pages that need to be rebuilt and included in the commit. The builder uses Python's standard library.

Add a page to `PAGES` in `build.py` and create its body in `src/content/`. Put images in `src/img/`; the builder copies them into `docs/img/`.

## Current reference review

The medication, rhythm, settings and medical-menu references were updated against ACM Extended commit `eabd2f2e88fba4754d81bda8543b81303a72964d`:

- 33 medication cards, each with the same nine clinical game-reference fields
- 39 effect graphs with 0%, 50% and 100% marks, onset markers, peak and duration labels
- 13 rhythm presentations, entry patterns, transition timing, causes and treatment responses
- Visible Addon Options labels in place of internal-code instructions
- Stable disclosure spacing; removed Known traps page and navigation

The build workflow runs Chromium checks at desktop and mobile widths for disclosure position, section menus, medication fields, graph labels and interaction search.

Earlier reference review:

Checked against ACM Extended commit `5bce47c26e70924ec5832eac792b19988e86e22c`:

- 33 medication/product cards and 39 native effect-envelope graphs
- 14G, 16G, 18G, 20G, EJ and IO reference
- Roller-clamp formula and requested-flow calculator
- Admitted fluid, leakage, volume compartments and gradual conversion
- Examination thresholds and 38 shared descriptor pairs

Source links are attached to the corresponding articles. Medication effect references, stock concentrations and infusion registry targets are labeled separately. The card graphs use the route-specific native function, without claiming to predict separate ACME drug systems.

The other system articles remain available with a review notice. Remove an article from that notice only after checking it against the current fork, then add its slug to `REVIEWED` in `build.py`.

## Latest reference controls

- All 39 medication curves and five physiology curves support pointer/touch inspection and numeric input.
- Medication readouts show seconds, delivered reference dose and relative game effect. They do not claim measured serum concentration.
- Route-specific peak values are listed vertically. Matching medication fields share row sizing across adjacent desktop cards.
- The glossary provides 305 definitions, with automatic links in article text and support for common abbreviations, inflections and spelling variants.
- Example prepared-bag concentrations round upward to two decimals with explicit units; unrounded calculations remain available for arithmetic.
- The sidebar branding is centered; Ventilator Settings and Pulse labels are explicit.
- The cardiology table distinguishes direct volume/resistance calculations, indirect calcium and acid-base effects, and physiology not independently simulated. This check uses ACM Extended commit `302b811ba90b4e2347b5614b8c74fb41b5442245`.

## Remaining rewrite work

- Complete the detailed review of the airway, ventilator, bleeding, TBI, altitude, accessibility and Zeus articles.
- Review the remaining terminology and the detailed mechanics behind the shorter supplementary overviews.
- Inspect the attached upstream ACM, ACE3 and Animate archives when the local workspace is available.
- Complete manual visual review, zoom and print checks. Automated browser checks cover the updated medication and rhythm pages.

## Hosting

Preserve the existing GitHub Pages source: the `main` branch, `/docs` directory. The reference refresh is prepared on a separate branch for review.

No external font request is required. Each HTML page contains the shared search index, glossary definitions, styling and reference controls.

## Texture conversion

The existing `paa2png.py` supports the DXT5 workflow documented in its source and uses `python-lzo` for compressed textures. Converted figures belong in `src/img/` so rebuilding `docs/` preserves them.
