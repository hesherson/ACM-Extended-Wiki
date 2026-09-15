# Calcium and transfusion reference

Reviewed 15 September 2026. These are ACM Extended game mechanics. The website remains version 1.2.1.

## Reviewed revisions

- Main: [5416332cf899f11f5170c9bcb9768edabb8827e5](https://github.com/hesherson/ACM-Extended/tree/5416332cf899f11f5170c9bcb9768edabb8827e5)
- Dev: [a9ae90c9abd448844861f16747f4b29e7ac3d510](https://github.com/hesherson/ACM-Extended/tree/a9ae90c9abd448844861f16747f4b29e7ac3d510)

The native transfusion HR adjustment, blood burden clearance, calcium callback, deficit defaults, salt equivalence and toxicity calculations agree in the inspected main/dev files. Manual medication timing differs. Other wiki systems retain their existing source reviews.

## What changed

- Added a grouped calcium reference to Fluids & blood volume with separate subsections for first/fourth-unit decisions, salt/duration comparisons, untreated effects, clearance, redosing and branch differences.
- Linked both calcium medication cards, both infusion guides and the bleeding/triad summary to the reference.
- Made the full-dose gluconate warning explicit in the Hardcore push guidance: 3 g over 120 seconds supplies 139.5 mg/min elemental calcium, above the 100 mg/min fast-rate onset. A 300-second example supplies 55.8 mg/min.
- Corrected the bleeding card's ambiguous threshold and incorrect 40 mmHg-per-unit implication. The normalized calcium floor is 0.55, so its default maximum pressure suppression target is `(1 - 0.55) * 40 = 18 mmHg`. The circulation handler applies the effect gradually; this is not a guaranteed isolated cuff change.
- Preserved the dark palette, cream body text, yellow headings, article hierarchy, plots and interaction logic.

## Source map

| Mechanic | Source |
| --- | --- |
| HR target adjustment above 0.05 L | [Native vitals](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/core/overrides/fnc_handleUnitVitals.sqf) |
| Admitted blood, clearance, count cap, warmed blood flow | [Blood volume change](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/circulation/functions/fnc_getBloodVolumeChange.sqf) |
| First gram gives 2.5 native count; later grams give 2 | [Calcium callback](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/circulation/functions/fnc_handleMed_CalciumChlorideLocal.sqf) |
| Gluconate forwarding and cumulative equivalent credit | [Apply calcium credit](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_applyCalciumCredit.sqf) |
| 1 L deficit threshold, 0.18/L cost, 0.12/g credit, 0.55 floor | [Resuscitation defaults](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_initResuscitationConfig.sqf) |
| Salt conversion and flush list | [Infusion configuration](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_initInfusionConfig.sqf) |
| Pressure, bleeding, pressor response and calcium excess | [Circulation handler](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_circHandle.sqf) |
| Elemental fractions, rate and accumulation limits | [Drug physiology defaults](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_initDrugPhysiologyConfig.sqf) |
| Main manual dose and rate input | [Exposure](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_medicationExposure.sqf), [drive queue](https://github.com/hesherson/ACM-Extended/blob/5416332cf899f11f5170c9bcb9768edabb8827e5/addons/acm_extended/functions/fn_medicationDriveAdd.sqf) |
| Dev normal-mode windows and Hardcore defaults | [Drive queue](https://github.com/hesherson/ACM-Extended/blob/a9ae90c9abd448844861f16747f4b29e7ac3d510/addons/acm_extended/functions/fn_medicationDriveAdd.sqf), [suggested push time](https://github.com/hesherson/ACM-Extended/blob/a9ae90c9abd448844861f16747f4b29e7ac3d510/addons/acm_extended/functions/fn_medicationSuggestedPushSec.sqf) |

## Interpretation limits

The 50 mL rule is a native HR target adjustment. The additional normalized calcium deficit starts above 1 L of remaining burden at default tuning. Neither is a fixed countdown from the end of a blood bag, and neither creates a special fourth-unit event.

The five-minute delivery examples are arithmetic derived from configured elemental fractions and toxicity thresholds. They are not blanket safety guarantees, and do not replace checking prior calcium or actual line admission. A 300-second Hardcore default is a duration for the selected syringe contents, not a fixed dose. Main does not contain the reviewed dev implementation of the Hardcore calcium timing controls.

The spendable native calcium count, cumulative CaCl2-equivalent credit and excess-calcium toxicity accumulator are separate state variables. Active transfusion does not turn off the excess/rate toxicity checks. When burden is very small, the native loop can spend more count than the liters of burden removed that tick, so a dose cannot be translated into a guaranteed number of protected blood bags.

The 1 min 40 s / 6 min 40 s clearance examples assume no further blood entering and sufficient count. The 2 min 30 s / 10 min examples assume 100 mL/min of continued admitted blood and sufficient count throughout. They describe ideal backlog reduction at 300 or 200 mL/min respectively, not medication administration or guaranteed physiological recovery. While blood continues, ordinary discrete ticks can retain a small current-flow residual.

## Validation

- Checked the arithmetic against the reviewed source constants: equivalent doses, elemental rates, five-minute steady excess, untreated unit 1–4 calcium/pressure/bleeding values, fourth-unit pressor gate, clearance and count duration.
- Rebuilt all 28 pages and checked article structure, source disclosure nesting, local links, original anchors and generated output consistency.
- Retained all existing plots, controls, style files and JavaScript. This update changes reference text and cross-links only.
- Browser preview remains blocked by the available browser security policy. No fresh visual or in-engine multiplayer test is claimed.

This package has not been pushed or deployed from this session.
