# Deploy the September 15 calcium reference update

This full package adds the first/fourth-unit calcium reference, salt and rate comparisons, medication links and corrected calcium bleeding summary. It retains the dark charcoal/navy surfaces, cream body text and yellow titles (`#F1BD59`). New information blocks and link highlights match the dark palette. It includes the editable source and rebuilt `docs` site, with the grouped layout retained. The website version remains **1.2.1**. It adds grouped topics, indented subsections and labeled explanations to the existing package, including the Hardcore settings, slow-push guide, infusion tools, printable charts and graph updates.

Use the existing **hesherson/ACM-Extended-Wiki** repository. GitHub Pages continues to publish **main /docs**. No npm install or Python build is needed to publish the included HTML.

## PowerShell

Save `ACM-Extended-Wiki.zip` to Downloads. Open PowerShell in your existing **ACM-Extended-Wiki repository folder**, then run:

```powershell
$ErrorActionPreference = "Stop"
$wikiOrigin = git remote get-url origin
if ($LASTEXITCODE -ne 0 -or $wikiOrigin -notmatch 'github\.com[:/]hesherson/ACM-Extended-Wiki(?:\.git)?/?$') {
    throw "Open PowerShell in the ACM-Extended-Wiki repository."
}
if (git status --porcelain) {
    throw "Commit or preserve your existing changes before applying this ZIP."
}
git switch main
if ($LASTEXITCODE -ne 0) { throw "Could not switch to main." }
git pull --ff-only origin main
if ($LASTEXITCODE -ne 0) { throw "Pull failed. Resolve it before copying the update." }

$wikiStage = Join-Path $env:TEMP ("acme-wiki-" + [guid]::NewGuid().ToString("N"))
Expand-Archive -LiteralPath "$env:USERPROFILE\Downloads\ACM-Extended-Wiki.zip" -DestinationPath $wikiStage
$wikiSource = Join-Path $wikiStage "ACM-Extended-Wiki"
if (!(Test-Path "$wikiSource\docs\index.html")) { throw "The extracted site is missing." }
Get-ChildItem -LiteralPath $wikiSource -Force | Copy-Item -Destination . -Recurse -Force
if (Test-Path "docs\ov_traps.html") { Remove-Item "docs\ov_traps.html" }

git add -- src docs scripts .github build.py README.md PUBLISH-WITH-GITHUB-DESKTOP.md DEPLOY.md SOURCE-REVIEW.md CALCIUM-REVIEW.md
if ($LASTEXITCODE -ne 0) { throw "Could not stage the wiki update." }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "Fix the reported whitespace errors before committing." }
git diff --cached --stat
```

Open `docs/index.html` to preview, and review the staged changes. This ZIP is a full saved website snapshot; check any changes that would replace newer work in your checkout. When ready, publish:

```powershell
git commit -m "Explain ACME calcium timing during transfusion"
if ($LASTEXITCODE -ne 0) { throw "Commit failed; nothing was pushed." }
git push origin main
if ($LASTEXITCODE -ne 0) { throw "Push failed. The local commit is retained." }
```

Wait for the repository's **Wiki build** checks and **Pages build and deployment** to finish in GitHub's Actions tab. The Pages setting should remain **Deploy from a branch > main > /docs**. Do not upload the ZIP itself into the repository as a substitute for its extracted contents.

[GitHub Pages publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Rebuilding after future edits

```powershell
py -3 build.py
py -3 scripts\check_wiki.py
```

Commit both `src` and rebuilt `docs`. Editing only `docs` will be overwritten by the next build.

## Changes and validation

Latest update: source-checked calcium timing, controlled chloride/gluconate delivery, first/fourth-unit reassessment, untreated effects and recovery examples. Both medication cards and infusion guides link to the new reference. The bleeding summary now distinguishes the early HR rule from the later normalized deficit, and correctly gives its maximum pressure-suppression target as 18 mmHg at default tuning. CALCIUM-REVIEW.md records the reviewed main/dev differences and validation.

* 25 parent topics across eight long articles, with smaller yellow subsection headings and a subtle left rule
* Five subgroup headings for the 21 Hardcore setting comparisons
* 71 labels that make explanations, in-game behavior and cautions easier to scan
* Shorter prose lines, compact spacing and a smaller phone indent; wide tables and charts retain their space
* 44 optional source disclosures, with treatment information and slideshow instructions kept visible
* Parent and subsection navigation, preserved original anchors and section copy links with a manual-copy fallback
* Source revision inventory and future review priorities in SOURCE-REVIEW.md

Passed in this handoff: the Python build, an independent rebuild comparison, article structure and disclosure nesting, all 28 pages' local links, anchors and assets, and syntax checks for every source JavaScript file. The earlier layout comparison preserved the original article text and structure. This calcium update changes the documented calcium paragraphs and adds three reference tables; existing section anchors, plots and controls are retained. Search contains 339 records. The build retains 33 medication cards, 39 medication curves, 21 Hardcore setting comparisons, 18 infusion guides, 14 push-time rows and 324 glossary entries.

The preview browser's security policy blocked local preview URLs. This handoff therefore does not claim a fresh visual, mobile, clipboard or browser-interaction pass. The seven existing browser suites remain in the GitHub workflow, with heading selectors adjusted for the new hierarchy. Preview IV access, airway, ventilator and Settings at desktop and phone widths before publishing; check the section menu, IV slideshow and a copy-section link. No mod runtime or calculator equations changed. This update adds source-checked calcium explanations and links pinned to main 5416332 and dev a9ae90c; other articles keep their earlier review pins.

This package has not been pushed to GitHub or deployed from this session.
