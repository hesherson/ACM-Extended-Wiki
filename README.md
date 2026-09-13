# ACM Extended Wiki

Static reference site for ACM Extended. The existing Python builder produces self-contained HTML pages in `docs/`, with offline search, inline styles and inline browser scripts.

## Edit and build

- `src/content/*.html`: article bodies
- `src/_pillar.css`: shared styles
- `src/reference.js`: drip calculator, keyboard shortcut, anchor reveal and printing
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

Checked against ACM Extended commit `5bce47c26e70924ec5832eac792b19988e86e22c`:

- 33 medication/product cards and 39 native effect-envelope graphs
- 14G, 16G, 18G, 20G, EJ and IO reference
- Roller-clamp formula and requested-flow calculator
- Admitted fluid, leakage, volume compartments and gradual conversion
- Examination thresholds and 38 shared descriptor pairs

Source links are attached to the corresponding articles. Medication effect references, stock concentrations and infusion registry targets are labeled separately. The card graphs use the route-specific native function, without claiming to predict separate ACME drug systems.

The other system articles remain available with a review notice. Remove an article from that notice only after checking it against the current fork, then add its slug to `REVIEWED` in `build.py`.

## Remaining rewrite work

- Integrate the supplied ACM Extended logo. Its image bytes could not be accessed during the reference refresh; the header currently uses text.
- Verify the retained airway, ventilator, circulation, bleeding, TBI, altitude, interface, settings and Zeus articles.
- Verify the remaining terminology and code-mechanism pages against the fork.
- Inspect the attached upstream ACM, ACE3 and Animate archives when the local workspace is available.
- Review the layout in desktop and mobile browsers, including zoom, drawer focus, calculator entry and print output.

## Hosting

Preserve the existing GitHub Pages source: the `main` branch, `/docs` directory. The reference refresh is prepared on a separate branch for review.

No external font request is required. Each HTML page contains the shared search index, glossary definitions, styling and reference controls.

## Texture conversion

The existing `paa2png.py` supports the DXT5 workflow documented in its source and uses `python-lzo` for compressed textures. Converted figures belong in `src/img/` so rebuilding `docs/` preserves them.
