# TBI reference update — B119

Reviewed 14 September 2026 against [ACM Extended dev revision 98d18bb](https://github.com/hesherson/ACM-Extended/commit/98d18bb3f60dc9be8cdaf4a43419bb57483c3a3f). At review, main remained `5416332cf899f11f5170c9bcb9768edabb8827e5`. This wiki update documents the supplied TBI patch; it does not modify, publish or merge the mod.

## References updated

- Main TBI guide and printable TBI chart: acute versus structural injury, baseline ICP recovery, pressure gates, reserve and autonomic progression.
- Hemorrhage, oxygen delivery, head injury assessment, overview, blast exposure, obtundation, ventilator tips and settings: connected effects and revised recovery assumptions.
- Zeus: fresh injury initialization and Clear TBI behavior.
- Debug and glossary: current fields, their meanings and the earlier screenshot's limitations.
- Home page: scoped source revision; other systems retain their existing review pins.

## Source details that matter

| Topic | Implementation reviewed | Documentation consequence |
| --- | --- | --- |
| Acute and structural state | `fn_tbiInit`, `fn_headInjuryTBI`, `fn_tbiBlast`, `fn_tbiHandle` | `severity` is acute; `structuralSeverity` preserves injury history. Repeat trauma can raise acute burden below the old structural maximum. Herniation can impose a recovery floor. |
| Pressure gates | `fn_tbiHandle`, `fn_initTbiProgressionConfig` | Structural boundaries are 0.35, 0.60 and 0.80. MAP floors interpolate inside grades; recovery MAP is at least 65. Severe adds CPP 55; critical adds CPP 60. |
| Complete recovery | `fn_tbiHandle` | Pressure predicate plus no active DO2 deficit, SpO2 ≥ 90 and ventilation ratio ≥ 0.9. DO2 deficit starts below 0.70 and clears at 0.78. PerfOK alone is insufficient. |
| Brain versus overlay CPP | `fn_tbiHandle`, `fn_debugMenuClinical` | Head elevation subtracts 6 mmHg from the brain's MAP by default; the clinical overlay uses systemic MAP−ICP. Fixed overlay CPP colors at 50/70 do not express the new recovery gates. |
| Autoregulation | `fn_tbiHandle`, `fn_initTbiProgressionConfig` | Separate cerebral integrity controls low CPP vulnerability and the high CPP pressure-passive contribution. Structural reserve remains reduced in severe/critical history. |
| Autonomic failure | `fn_tbiHandle`, `fn_tbiApplyVitals` | Stateful integrity, signed tone and decompensation; vascular-only path does not require full Cushing vital changes. Nonterminal vital-target limits are not a whole-patient survival guarantee. |
| Junctional bleeding | `fn_junctionalStartBleed`, `fn_circHandle` | Compensation ability is 0.25 + 0.75 × integrity. Tone already acts through systemic resistance. The circulation update retains one blood-volume debit. |
| Current state bounds | `fn_tbiHandle` | Both integrities stop at 0.05; the junctional equation's theoretical 25% endpoint therefore corresponds to 28.75% at the current controller minimum. This is compensation ability, not a loss multiplier. |
| Zeus presets/reset | `fn_zeusTBIApplyLocal`, `fn_zeusClearTBILocal` | Fresh severity initializes both injury scores and controller states; Clear TBI clears the state and named offsets/flags. Other injuries remain. |

The source patch contains 11 changed runtime files. Its supplied validation report covers source structure, state transitions, model checks, relevant existing tests and ZIP integrity. That report is not an in-engine validation result. The website build and browser checks validate this wiki, not Arma physiology.

## Outstanding Arma staging checks

Use identical mission settings, record the loaded build, and capture both debug pages. Values below are scenario starting points, not guarantees about a complete casualty. MAP examples must account for head elevation before comparison with the handler's effective brain MAP.

1. Mild injury around 0.25–0.30, MAP 70+, adequate oxygen delivery and ventilation, no new insult: watch Acute fall toward 0 and ICP approach baseline while Struct persists.
2. Moderate structural injury around 0.50–0.55, MAP around 70, adequate delivery: confirm progressive recovery without an artificial universal 85 mmHg requirement.
3. Severe structural injury 0.75, effective MAP 80, ICP 14, CPP 66: confirm possible stabilization with the other gates met; reduced reserve should remain visible.
4. Severe injury with rising ICP: watch positive tone, resistance/MAP support and the Cushing response develop.
5. Severe injury with prolonged poor perfusion: watch integrity decline, labile tone and eventual negative tone with falling resistance and MAP. Include a case without the full Cushing vital pattern.
6. Severe injury with junctional hemorrhage: compare early sympathetic compensation with late failure; verify local compensation weakens, loss is counted once per circulation update, and behavior remains consistent across multiplayer ownership changes.

Also verify that empty TBI debug defaults are not mistaken for a recovered patient, and compare head-up versus level positioning when reading displayed CPP and PerfOK.

## Wiki verification

- Build and independent rebuild match: 28 pages, 264 search records and 324 glossary definitions; local links, IDs and referenced assets pass.
- Existing article anchors retained, including the earlier TBI assessment, pupil and recovery links.
- All six browser suites pass, including mobile table reflow at 320, 390, 768, 1024 and 1905 pixels, enlarged text, print selection/reset and JavaScript-disabled fallbacks.
- All seven printable sheets fit on both A4 and US Letter in landscape; the TBI chart occupies one page. Print margins and rendered layout were checked.
- Existing medication cards, infusion guides, catheter animations, tooltip behavior, rhythm traces, capnography and chest seal controls remain covered by the passing suites.

The screenshot test now scrolls lazy-loaded Zeus/debug images into view and waits for decoding before checking them. This avoids treating a correctly deferred image as a missing asset after article text moves it below the initial viewport.
