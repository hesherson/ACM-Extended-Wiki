# ACM Extended Wiki

Static reference site for ACM Extended. The existing Python builder produces self-contained HTML pages in `docs/`, with offline search, inline styles and inline browser scripts.

## Edit and build

- `src/content/*.html`: article bodies
- `src/_pillar.css`: base palette and layout
- `src/visual-reference.css`: quiet glossary terms, visual cards, calculations and procedure layouts
- `src/reference.js`: calculators, medication curves, automatic glossary links and printing
- `src/chart-readouts.js`: access-capacity, fluid-conversion and waveform inspection
- `src/slideshow.js`: fading IV stages, grouped insertion frames and manual controls
- `src/suction-guide.js`: repeating suction sweep and motion controls
- `src/capnography.js` and `src/capnography.css`: interactive waveform examples
- `src/languages.js` and `src/languages.css`: language picker and English spelling preferences
- `src/rhythm-waveforms.js` and `src/rhythm-waveforms.css`: monitor traces and inspection
- `src/chest-seal.js` and `src/chest-seal.css`: chest seal burping demonstration
- `src/audio/`: original mod sound previews
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

The checker compares docs with an independent build and validates local links and IDs. It works in a ZIP copy without Git. The builder uses Python's standard library. Windows users can double-click BUILD-WIKI.cmd.

Add a page to `PAGES` in `build.py` and create its body in `src/content/`. Put images in `src/img/` and sound clips in `src/audio/`; the builder copies these into the matching `docs/` directories.

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

- All 47 quantitative charts support pointer/touch inspection with dots and readouts: 39 medication curves, five physiology curves, access capacity, fluid conversion and the capnography explorer. The unscaled ventilator waveform has a phase cursor without invented pressure values.
- Medication readouts show seconds, delivered reference dose and relative game effect. They do not claim measured serum concentration.
- Route-specific peak values are listed vertically. Matching medication fields share row sizing across adjacent desktop cards.
- The glossary provides 317 definitions, with automatic links in article text and support for common abbreviations, inflections and spelling variants.
- Example prepared-bag concentrations round upward to two decimals with explicit units; unrounded calculations remain available for arithmetic.
- The sidebar branding is centered; Ventilator Settings and Pulse labels are explicit.
- The cardiology table distinguishes direct volume/resistance calculations, indirect calcium and acid-base effects, and physiology not independently simulated. This check uses ACM Extended commit `302b811ba90b4e2347b5614b8c74fb41b5442245`.

## September 14 update

- Shared medication-card palette across headings, panels, tables, navigation and links
- Gold page titles, cream metric labels, spaced paragraphs and `>` disclosure markers
- New obtundation and blast-overpressure references with code-backed thresholds and treatment nuances
- Ketamine nystagmus conditions and fracture-pressure awakening added with cross-links
- Head injury, airway, ventilator and accessibility articles rewritten for quick reference
- Corrected pressure-limited volume delivery, CPAP backup, recovery floors and Zeus reset wording
- Screenshot placeholders removed; prior section links preserved
- 27 built pages, 317 glossary entries, 33 medication cards and 39 medication curves
- Publishing and future-edit instructions in PUBLISH-WITH-GITHUB-DESKTOP.md

The new system references use ACM Extended source 4848f63b200a45362eb576dcef469484202b6a80. Existing medication, circulation and other references keep their stated earlier snapshots; this update does not claim to audit every later change to the entire mod.

Build, local-link, anchor, asset and reproducibility checks are provided in `scripts/check_wiki.py`. The four Chromium suites in `scripts/` cover the complete site and the updated visual controls; the GitHub workflow repeats them after updates.

## Hosting

Preserve the existing GitHub Pages source: the `main` branch, `/docs` directory. Copy this ZIP’s extracted contents into the existing repository and commit the rebuilt `docs/` with the source changes.

No external font request is required. Each HTML page contains the shared search index, glossary definitions, styling and reference controls.

## Texture conversion

The existing `paa2png.py` supports the DXT5 workflow documented in its source and uses `python-lzo` or `lzokay` for compressed textures. Converted figures belong in `src/img/` so rebuilding `docs/` preserves them.

## Visual update and IV guide

The shared palette uses charcoal backgrounds, navy panels, gold headings, blue links and cream labels. Glossary terms inherit their surrounding text color and use subtle rectangular outlines, a filling underline and a short popup fade. Pages expand to the available browser width; wide tables scroll within their own container on small screens.

The medication page includes 21 original vial images. The access page presents the 15 original IV frames in six fading scenes, each held for seven seconds. Frames 01–06 play as one advancing motion and frames 07–11 play as one threading motion. Both use brief crossfades; a thin progress line shows the remaining scene time. Previous/next buttons, keyboard navigation, a stage selector, pause and show-all remain available. Reduced-motion starts paused; without JavaScript all scenes are visible. The unused LINE instruction is omitted. Slideshow controls belong to the website; game inputs appear in the captions and controls table.

The access decision guide explains urgency, vesicants, intact anatomy, gauge tradeoffs and early IO for critical game casualties. It preserves the prepared-set rule: one running bag or Y set per access site, including the Y set’s clamped saline reserve. IO priority is a gameplay recommendation, not a claim that the engine mandates IO for every critical patient.

Six ventilator cards restore at-a-glance settings for healthy lungs, edema, blast/ARDS, pneumothorax, hemothorax and CPR. Named inputs and worked steps simplify the pressure, volume, perfusion and infusion examples.

Trauma sections use original mod equipment icons. The suction guide repeats a short S sweep from bottom to top with more horizontal turns, a pause at the top and a fade before resetting. Three original sound clips have manual playback controls. The motion pauses offscreen, in a hidden tab and for reduced-motion preferences.

Assets and IV controls were checked against ACM Extended commit `abf6253d4876b4a7a5563f84a3b060de53a0290d`. See `MOD-ASSET-SOURCES.md` for provenance. The access decision rules and suction controls/assets were separately checked at `21f86948b8a03507146297742ea84983987d5be1`. Ventilator references and other content retain their stated review revisions.

## Languages and the latest reference additions

The sidebar offers US English, UK English, German, French, Spanish and Russian. US/UK change common English spellings locally and retain the preference. German, French, Spanish and Russian open the current published page in Google’s website translator in a new tab; they require internet access and are automatic translations. The ZIP does not contain independently translated offline editions. Language changes require pressing the clearly labeled apply/open button; pages do not redirect on load.

`PUBLIC_URL` in `build.py` is the conventional GitHub Pages URL for this repository. Update it if the site moves to a custom domain. Local file and localhost previews retain the English modes and explain that live translation becomes available on the published site. Code and key labels retain their original text. [Google’s website translation instructions](https://support.google.com/translate/answer/2534559?hl=en&co=GENIE.Platform%3DDesktop).

The Airway & Breathing article now includes selectable capnography patterns with time/CO₂ inspection. The oxygen article distinguishes underlying oxygen state from player pulse-oximeter readings, and the blast article explains Breacher’s syndrome with separate game-model limits. The Zeus article documents available modules and fridge settings; the new Debug menu article explains the supplied screenshot field by field. Source links identify the reviewed implementation and medical background.

## Chest seal and rhythm update

Airway & Breathing includes an eased chest seal demonstration using both original corner sequences, with pause, replay and manual inspection. It explains the full-lift mouse wheel action, why a blocked outlet matters, and how leak healing, drainage, pressure relief and residual collapse differ in the mod.

All 13 cardiac rhythm blocks include bright green, six-second monitor examples with pointer, touch and keyboard inspection. The traces use the mod’s native/custom waveform formulas; vertical values are relative monitor deflection, not calibrated millivolts. They remain visible without JavaScript. MV now opens the minute-ventilation definition, including the distinction between L/min and the game’s MV adequacy ratio. Unnecessary hyphens have been removed from article prose while preserving links and code identifiers.

The chest seal mechanics, pneumothorax recovery and ECG generation were checked against commit `dd50edf34497588d473ffe3c70797f2eaa52f6f8`. Other references retain their stated review revisions. `scripts/check_chest_rhythms.mjs` checks these additions, and the existing suites cover the retained site controls.
