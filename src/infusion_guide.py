"""Render the source-reviewed infusion guide as static, searchable article content."""
import json
from html import escape
from pathlib import Path
from infusion_explorer import load_levels, level_label

SOURCES = {
    "drug": ("Drug thresholds", "addons/acm_extended/functions/fn_initDrugPhysiologyConfig.sqf"),
    "circ": ("Circulation effects", "addons/acm_extended/functions/fn_circHandle.sqf"),
    "tox": ("Active overdose burden", "addons/acm_extended/functions/fn_medicationToxicityTick.sqf"),
    "meds": ("Extended medication data", "addons/acm_extended/config.cpp"),
    "native": ("Native medication data", "addons/core/ACM_Medication.hpp"),
    "sedation": ("Sedation physiology", "addons/acm_extended/functions/fn_sedationPhysiology.sqf"),
    "components": ("Combined sedation", "addons/acm_extended/functions/fn_sedationComponents.sqf"),
    "interactions": ("Drug interactions", "addons/acm_extended/functions/fn_medicationInteractions.sqf"),
    "unstable": ("Conditional instability", "addons/circulation/functions/fnc_isOverdosed.sqf"),
    "overdose": ("Supported overdose handlers", "addons/circulation/functions/fnc_handleOverdose.sqf"),
    "lido": ("Lidocaine toxicity", "addons/acm_extended/functions/fn_lidoToxTick.sqf"),
    "options": ("Addon Options defaults", "addons/acm_extended/XEH_preInit.sqf"),
    "registry": ("Preparation amounts", "addons/acm_extended/functions/fn_initInfusionConfig.sqf"),
    "delivery": ("Admitted medication", "addons/acm_extended/functions/fn_infusionDeliver.sqf"),
    "rhythm": ("Rhythm gates", "addons/acm_extended/functions/fn_initRhythmThresholdRuntime.sqf"),
    "calcium": ("Calcium replacement credit", "addons/acm_extended/functions/fn_applyCalciumCredit.sqf"),
    "osmo": ("Osmotherapy", "addons/acm_extended/functions/fn_tbiApplyOsmotherapy.sqf"),
}

def render_infusion_guide():
    data = json.loads(Path(__file__).with_name("infusion-ranges.json").read_text(encoding="utf-8"))
    levels = {row["id"]: row for row in load_levels()["rows"]}
    cards = []
    for row in data["rows"]:
        level = levels[row["id"]]
        target = escape(level_label(level))
        links = []
        for key in row["sources"]:
            label, path = SOURCES[key]
            links.append(f'<a href="https://github.com/hesherson/ACM-Extended/blob/{data["revision"]}/{path}">{label}</a>')
        # The explanatory fields contain intentional, locally authored inline markup.
        cards.append(f'''<details class="dd infusion-guide" id="infusion-risk-{escape(row['id'])}" data-infusion-name="{escape(row['name'])}">
<summary><span class="dd-mark"></span><span class="infusion-heading"><span class="dd-name">{escape(row['name'])}<span class="infusion-target"><b>Game level:</b> {target}</span></span><span class="infusion-summary">{escape(row['summary'])}</span></span><span class="infusion-category">{escape(row['group'])}</span></summary>
<div class="dd-body"><button type="button" class="infusion-level-action" data-explore-infusion="{escape(row['id'])}" hidden>Explore delivery and game levels &gt;</button><div class="infusion-bands">
<div class="infusion-band band-reference"><h3>Reference range</h3><p>{row['reference']}</p></div>
<div class="infusion-band band-caution"><h3>Increasing exposure</h3><p>{row['caution']}</p></div>
<div class="infusion-band band-danger"><h3>Danger and limits</h3><p>{row['danger']}</p></div>
</div><div class="infusion-followup"><p><b>Reassess:</b> {row['watch']}</p><p><b>Allow for timing:</b> {row['peak']}</p></div>
<p class="source-note">Source review {data['revision'][:7]}: {' · '.join(links)}.</p></div></details>''')
    return '\n'.join(cards)
