For the September 15 package, use [DEPLOY.md](DEPLOY.md) for the current PowerShell commands and validation scope. The earlier browser results below describe previous updates, not a fresh browser pass of this package.

# Publish this update

The ZIP includes the rebuilt site in `docs`, the editable source and the build scripts. You do not need Python to publish the included build.

1. Open GitHub Desktop and select **ACM-Extended-Wiki**, then select **main**.
2. Click **Fetch origin**, then **Pull origin** if offered. Preserve any work you already have before replacing files.
3. Choose **Repository > Show in Explorer**.
4. Extract this ZIP somewhere else. Copy the contents of its `ACM-Extended-Wiki` folder into the repository folder. Replace matching files. `build.py`, `src` and `docs` belong directly inside the repository, not inside a second nested folder.
5. Delete `docs/ov_traps.html` if that retired page remains from an older build. The source copy is no longer part of the published site.
6. Open `docs/index.html` in a browser. Check the grouped IV access, airway, ventilator and Settings pages on desktop and at phone width. Try the section menu, IV slideshow and a copy-section link. Check Printable charts in the A4 or US Letter preview.
7. Return to GitHub Desktop. Review **Changes**, enter `Explain ACME calcium timing during transfusion`, click **Commit to main**, then **Push origin**.
8. On GitHub, check the **Actions** tab for the wiki checks and Pages deployment. Wait for deployment to finish before refreshing the live site.

The repository's documented publishing source is **Settings > Pages > Deploy from a branch > main > /docs**. Keep that source. Uploading the ZIP file itself does not update the website; publish its extracted contents.

# Future updates

| Change | Edit |
| --- | --- |
| Article text | `src/content/<page>.html` |
| Shared colors and layout | `src/_pillar.css` and `src/visual-reference.css` |
| Topic groups and subsection hierarchy | `src/page-groups.json` and `src/reading_layout.py` |
| Reading layout and section links | `src/reading-layout.css` and `src/reading-layout.js` |
| Tooltip definitions | `src/glossary_terms.py` |
| Graph controls and calculators | `src/reference.js` and `src/chart-readouts.js` |
| IV slideshow timing and controls | `src/slideshow.js` |
| Suction motion | `src/suction-guide.js` |
| Sound previews | `src/audio` |
| Capnography explorer | `src/capnography.js` and `src/capnography.css` |
| Language picker | `src/languages.js` and `src/languages.css` |
| Infusion dose and risk text | `src/infusion-ranges.json` |
| Infusion filtering and layout | `src/infusion-guide.js` and `src/infusion-guide.css` |
| ECG examples | `src/rhythm-waveforms.js` and `src/rhythm-waveforms.css` |
| Chest seal demonstration | `src/chest-seal.js` and `src/chest-seal.css` |
| Navigation or new pages | `build.py` and the matching content file |
| Images | `src/img` |

After editing source, double-click **BUILD-WIKI.cmd**. It needs Python 3.9 or newer and rebuilds every page, checks local links and compares the result with a fresh build. Preview `docs/index.html`, then commit both source changes and rebuilt `docs` in GitHub Desktop. Repeat Fetch/Pull before beginning the next update.

Avoid editing only `docs`: the next rebuild replaces those files from `src`.

# Optional terminal commands

From the repository folder, after copying the update:

```powershell
git status
git diff --check
git add build.py paa2png.py src docs scripts .github README.md BUILD-WIKI.cmd MOD-ASSET-SOURCES.md PUBLISH-WITH-GITHUB-DESKTOP.md DEPLOY.md SOURCE-REVIEW.md CALCIUM-REVIEW.md
git commit -m "Explain ACME calcium timing during transfusion"
git push origin main
```

For future source edits, run these before the Git commands:

```powershell
py -3 build.py
py -3 scripts\check_wiki.py
```

# Earlier browser coverage

The build, JavaScript syntax, local links, anchors and reproducibility checks passed. Chromium checked all 28 pages at 390, 1905 and 5120 pixels, including quiet glossary terms, vial placement, automatic/manual slideshow controls, reduced-motion and JavaScript-disabled fallbacks, ventilator cards, graph readouts and loadable suction audio. The added checks also cover calculator label alignment, VTi/VTe definitions, the capnography controls, upward suction motion, the debug reference and language controls. Live-translation links are checked for the selected language and current page; Google provides the external translation. The new checks cover both chest seal corners, full and partial lifts, easing and pause/resume, reduced motion, all 13 ECG traces and their readouts, JavaScript-disabled ECG display and the MV hover definition. The GitHub workflow repeats the browser checks on future updates.

Official guidance: [GitHub Desktop commits and pushing](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop), [GitHub Pages publishing source](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

US/UK English work in the ZIP preview. German, French, Spanish and Russian open automatic live-page translations after publication, with an internet connection. The language selector does not create separate translated source files.

The infusion update retains the existing repository and `/docs` publishing source. Its additional checks cover all 18 agents, 19 recipe links, empty-search and hash navigation, 33 medication images, cream headings and the relocated nystagmus section. No new workspace or hosting setup is required.


The mobile/print update adds `src/mobile-layout.css`, `src/responsive_tables.py`, `src/print-medications.json`, `src/print_reference.py`, `src/print-reference.css` and `src/print-reference.js`. Rebuild after editing them. The included `docs/quick-reference.html` contains all charts and uses the browser's own print dialog; you do not need to install anything to print.

The phone checks include every article table with disclosures open, down to 320 pixels, plus enlarged text. The seven-sheet print layout was rendered and visually checked on both A4 and US Letter with background printing disabled.
