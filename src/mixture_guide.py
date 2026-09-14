"""Source-pinned game preparation walkthroughs with a static HTML fallback."""
from html import escape
import json

REVISION = "98d18bb3f60dc9be8cdaf4a43419bb57483c3a3f"
BASE = f"https://github.com/hesherson/ACM-Extended/blob/{REVISION}/addons/acm_extended/functions/"


def step(title, body, fill, contents):
    return {"title": title, "body": body, "fill": fill, "contents": contents}


RECIPES = [
    {
        "id": "ketofol", "title": "Ketofol", "kind": "syringe",
        "subtitle": "10 mL compound syringe · ketamine + propofol",
        "intro": "The named game recipe combines equal liquid volumes of two different stock concentrations. Its mass ratio is <b>5:1 ketamine to propofol</b>.",
        "stocks": [("Ketamine", "5 mL at 50 mg/mL", "250 mg"), ("Propofol", "5 mL at 10 mg/mL", "50 mg")],
        "components": [{"name": "Ketamine", "amount": 250, "unit": "mg"}, {"name": "Propofol", "amount": 50, "unit": "mg"}],
        "volume": 10, "summary": "10 mL contains 250 mg ketamine + 50 mg propofol. Each 1 mL contains 25 mg + 5 mg.",
        "tag": ["KET 25 mg/mL", "PROP 5 mg/mL", "10 mL total"],
        "steps": [
            step("Choose a 10 mL syringe", "Open the syringe draw view in the Narc Box and select a <b>10 mL</b> empty syringe. Compounding is already the default; there is no separate Mix mode.", 0, "Empty 10 mL syringe"),
            step("Draw 5 mL ketamine", "Select <b>ketamine 50 mg/mL</b>, pull the plunger to <b>5 mL</b>, then press <b>Draw</b>. This locks in 250 mg and leaves room for the second component.", 5, "5 mL: ketamine 250 mg"),
            step("Add 5 mL propofol", "Select <b>propofol 10 mg/mL</b>. Pull from the existing 5 mL level to <b>10 mL total</b>, then press <b>Draw</b> again. The added 5 mL supplies 50 mg propofol.", 10, "10 mL: ketamine 250 mg + propofol 50 mg"),
            step("Check the label and Save", "Use <b>Select Syringe Tag</b> to record both concentrations, then press <b>Save</b>. The recognized label reads <b>Ketamine 250 mg + propofol 50 mg (10 mL; 5:1 mg ratio)</b>. Confirm the selected syringe before administering a measured volume.", 10, "Saved 10 mL compound: 25 mg + 5 mg per mL"),
        ],
        "caution": "This describes the full prepared container. It does not make 10 mL a single dose. Ketamine and propofol both contribute to the active hypnotic load; titrate to the game patient's response, ventilation and perfusion.",
    },
    {
        "id": "push-epinephrine", "title": "Push-dose epinephrine", "kind": "syringe",
        "subtitle": "10 mL dilution · cardiac-strength source",
        "intro": "The recognized dilution uses the <b>0.1 mg/mL cardiac vial</b> and a prefilled saline flush. The finished syringe contains <b>10 mcg/mL</b>.",
        "stocks": [("Saline flush", "10 mL initially; waste 1 mL", "9 mL retained"), ("Epinephrine cardiac vial", "1 mL at 0.1 mg/mL", "100 mcg")],
        "components": [{"name": "Epinephrine", "amount": 100, "unit": "mcg"}],
        "volume": 10, "summary": "10 mL contains 100 mcg. Each 1 mL contains 10 mcg; 2 mL contains 20 mcg.",
        "tag": ["EPI 10 mcg/mL", "1 mL = 10 mcg", "10 mL = 100 mcg"],
        "steps": [
            step("Choose the 10 mL saline flush", "Select the prefilled <b>10 mL saline flush</b> in the syringe draw view. The flush supplies its own syringe.", 10, "10 mL saline"),
            step("Waste 1 mL", "Use the flush waste workflow to reduce the saline to <b>9 mL</b>. This creates exactly 1 mL of room for the cardiac-strength source.", 9, "9 mL saline retained"),
            step("Draw 1 mL from the cardiac vial", "Choose <b>epinephrine 0.1 mg/mL</b> and draw <b>1 mL</b> into the retained saline. Complete the flush preparation. The exact recipe is 9 mL saline + 1 mL cardiac-strength epinephrine.", 10, "10 mL: epinephrine 100 mcg in saline"),
            step("Read concentration before selecting a push", "Check the prepared syringe label <b>10 mcg/mL</b>. Its stored administration options include <b>1 mL</b>, <b>2 mL</b> and the full remaining volume. Keep the container total distinct from the selected push volume.", 10, "Prepared concentration: epinephrine 10 mcg/mL"),
        ],
        "caution": "The 1 mg/mL epinephrine stock is ten times stronger and is not the source for this named dilution. A full 10 mL syringe contains 100 mcg; it is not one 10 mcg push.",
    },
    {
        "id": "norepinephrine-bag", "title": "Norepinephrine bag", "kind": "bag",
        "subtitle": "4 mg added to 250 mL normal saline",
        "intro": "A simple game preparation example for tracking one pressor at a time. Injected medication solution adds to the carrier volume.",
        "stocks": [("Normal saline", "250 mL carrier", "250 mL"), ("Norepinephrine", "4 mL at 1 mg/mL", "4 mg")],
        "components": [{"name": "Norepinephrine", "amount": 4000, "unit": "mcg"}],
        "volume": 254, "summary": "250 mL saline + 4 mL medication = 254 mL. Concentration: 4,000 mcg ÷ 254 mL ≈ 15.748 mcg/mL.",
        "tag": ["NOREPI 4 mg", "FINAL 254 mL", "15.748 mcg/mL"],
        "steps": [
            step("Select the saline set", "Choose the prepared/spiked <b>250 mL normal saline</b> set, then select <b>Prep Infusion</b>. This opens the draw view in bag preparation mode.", 0, "Empty syringe for the selected saline set"),
            step("Draw 4 mL norepinephrine", "Choose <b>norepinephrine 1 mg/mL</b> and measure <b>4 mL</b>. The syringe contains 4 mg before transfer.", 4, "4 mL: norepinephrine 4 mg"),
            step("Inject Into Bag", "Press <b>Inject Into Bag</b>. The selected set now contains <b>4 mg in 254 mL</b>. Use the bag's generated label to verify the medication total and final volume.", 0, "Transferred to bag: 4 mg in 254 mL"),
            step("Set flow and reassess", "Attach through a functioning access site, set the roller clamp and confirm actual drainage. Check pressure, perfusion, rhythm and the site. The flow preview below calculates solution content per minute.", 0, "Prepared bag concentration: about 15.748 mcg/mL"),
        ],
        "caution": "The bag total is a preparation example, not a target dose or serum level. Poor volume, acidosis, cold and low calcium can reduce pressor benefit. Check the vesicant guidance when selecting and monitoring the site.",
    },
    {
        "id": "epinephrine-bag", "title": "Epinephrine bag", "kind": "bag",
        "subtitle": "1 mg added to 100 mL normal saline",
        "intro": "This bag example uses the <b>1 mg/mL epinephrine stock</b>. Its source and final concentration differ from the cardiac-vial flush recipe above.",
        "stocks": [("Normal saline", "100 mL carrier", "100 mL"), ("Epinephrine", "1 mL at 1 mg/mL", "1 mg")],
        "components": [{"name": "Epinephrine", "amount": 1000, "unit": "mcg"}],
        "volume": 101, "summary": "100 mL saline + 1 mL medication = 101 mL. Concentration: 1,000 mcg ÷ 101 mL ≈ 9.901 mcg/mL.",
        "tag": ["EPI 1 mg", "FINAL 101 mL", "9.901 mcg/mL"],
        "steps": [
            step("Select the saline set", "Choose the prepared/spiked <b>100 mL normal saline</b> set, then select <b>Prep Infusion</b>.", 0, "Empty syringe for the selected saline set"),
            step("Draw 1 mL epinephrine", "Choose the <b>1 mg/mL</b> stock and draw <b>1 mL</b>. If using the 0.1 mg/mL cardiac vial instead, the same 1 mg requires 10 mL and creates a different final concentration.", 1, "1 mL: epinephrine 1 mg"),
            step("Inject Into Bag", "Press <b>Inject Into Bag</b>. This stock creates <b>1 mg in 101 mL</b>. Recheck the prepared set's label before attaching it.", 0, "Transferred to bag: 1 mg in 101 mL"),
            step("Set flow and reassess", "Open the clamp to the intended setting and confirm actual drainage. Track rate, rhythm and perfusion along with pressure; follow the access site for leakage or irritation.", 0, "Prepared bag concentration: about 9.901 mcg/mL"),
        ],
        "caution": "Epinephrine has its own cardiac drive and rhythm risks. Neither a target MAP nor a healthy-looking serum display alone establishes that escalation is beneficial.",
    },
    {
        "id": "shared-pressors", "title": "Two pressors in one bag", "kind": "bag",
        "subtitle": "Norepinephrine + epinephrine · shared flow demonstration",
        "intro": "The preparation code can retain multiple components in the same saline set. This is a demonstration of that game mechanic, with <b>one flow setting controlling both drugs</b>.",
        "stocks": [("Normal saline", "250 mL carrier", "250 mL"), ("Norepinephrine", "4 mL at 1 mg/mL", "4 mg"), ("Epinephrine", "1 mL at 1 mg/mL", "1 mg")],
        "components": [{"name": "Norepinephrine", "amount": 4000, "unit": "mcg"}, {"name": "Epinephrine", "amount": 1000, "unit": "mcg"}],
        "volume": 255, "summary": "250 + 4 + 1 = 255 mL. Norepinephrine ≈ 15.686 mcg/mL; epinephrine ≈ 3.922 mcg/mL.",
        "tag": ["NOREPI 4 mg + EPI 1 mg", "FINAL 255 mL", "ONE CLAMP: BOTH DRUGS"],
        "steps": [
            step("Select one 250 mL saline set", "Open <b>Prep Infusion</b> on the selected normal saline set. Keep this same set selected for both additions.", 0, "Empty syringe for the selected saline set"),
            step("Add norepinephrine first", "Draw <b>4 mL norepinephrine 1 mg/mL</b>, then press <b>Inject Into Bag</b>. The set now contains 4 mg in 254 mL.", 4, "Draw before transfer: norepinephrine 4 mg in 4 mL"),
            step("Add epinephrine to the same set", "Reopen <b>Prep Infusion</b> for that same set. Draw <b>1 mL epinephrine 1 mg/mL</b> and press <b>Inject Into Bag</b>. Verify both components on the resulting 255 mL bag label.", 1, "Second draw before transfer: epinephrine 1 mg in 1 mL"),
            step("Follow both rates together", "The single clamp now changes both rates in a fixed <b>4:1 mass ratio</b>. Use separately controlled bags and access paths when the game situation requires independent adjustment.", 0, "Prepared bag: norepinephrine 4 mg + epinephrine 1 mg in 255 mL"),
        ],
        "caution": "There is no special named combination bonus for this bag. Each component retains its own effects and risks. Menu support does not establish real-world chemical compatibility, and this example is not a preferred treatment recipe.",
    },
]


def _syringe(recipe):
    # Original game PNGs share the same 1024-pixel canvas. The window also allows
    # the full plunger to extend below that canvas at the 10 mL mark.
    return f'''<figure class="mixture-figure">
<div class="mixture-syringe-window" aria-hidden="true"><div class="mixture-syringe-canvas" style="--mixture-fill:1">
<img class="mixture-syringe-layer mixture-back" src="img/syringes/syringe_10_backbit_ca.png" alt="" width="1024" height="1024" loading="lazy"/>
<span class="mixture-liquid"></span>
<img class="mixture-syringe-layer mixture-plunger" src="img/syringes/syringe_10_plunger_ca.png" alt="" width="1024" height="1024" loading="lazy"/>
<img class="mixture-syringe-layer mixture-barrel" src="img/syringes/syringe_10_barrel_ca.png" alt="" width="1024" height="1024" loading="lazy"/>
</div></div><figcaption><b>Original game syringe</b><span data-mixture-drawing>10 mL capacity</span><small>The tint illustrates volume. Preparation steps show the measured draw.</small></figcaption></figure>'''


def _recipe(recipe):
    rid = recipe["id"]
    stocks = "".join(f'<li><b>{escape(name)}</b><span>{escape(draw)}</span><strong>{escape(amount)}</strong></li>' for name, draw, amount in recipe["stocks"])
    steps = "".join(f'''<li class="mixture-step" data-mixture-fill="{s['fill']}" data-mixture-contents="{escape(s['contents'], quote=True)}"><h4><span>{i + 1:02d}</span> {escape(s['title'])}</h4><p>{s['body']}</p></li>''' for i, s in enumerate(recipe["steps"]))
    controls = "".join(f'<button type="button" data-mixture-go="{i}" aria-label="Step {i + 1}: {escape(s["title"], quote=True)}">{i + 1:02d}</button>' for i, s in enumerate(recipe["steps"]))
    tag = "".join(f'<span>{escape(line)}</span>' for line in recipe["tag"])
    kind = recipe["kind"]
    if kind == "syringe":
        preview = f'''<label for="mixture-volume-{rid}">Selected syringe volume (mL)</label><div class="mixture-volume-control"><input id="mixture-volume-{rid}" type="number" data-mixture-quantity min="0" max="10" step="0.1" value="1" inputmode="decimal"/><input type="range" data-mixture-range aria-label="Selected syringe volume in milliliters" min="0" max="10" step="0.1" value="1"/></div>'''
        static = "Each 1 mL contains " + " + ".join(f'{c["amount"] / recipe["volume"]:g} {c["unit"]} {c["name"].lower()}' for c in recipe["components"]) + "."
        note = "The preview shows the contents of the selected volume. It does not predict serum concentration or the patient's response."
    else:
        preview = f'''<label for="mixture-flow-{rid}">Solution flow (mL/h)</label><input id="mixture-flow-{rid}" type="number" data-mixture-quantity min="0" max="1000" step="1" value="60" inputmode="decimal"/>'''
        static = "At 60 mL/h: " + "; ".join(f'{c["name"]} ≈ {c["amount"] / recipe["volume"]:.3f} {c["unit"]}/min' for c in recipe["components"]) + "."
        note = "Arithmetic assumes this much solution reaches the circulation. A closed clamp, blocked site or leakage changes actual delivery. The two-pressor example shares one flow setting."
    return f'''<article class="mixture-recipe" id="mixture-{rid}" data-mixture-recipe="{rid}" data-mixture-kind="{kind}" data-mixture-total="{recipe['volume']}" data-mixture-components="{escape(json.dumps(recipe['components']), quote=True)}">
<header class="mixture-recipe-header"><h3>{escape(recipe['title'])}</h3><p>{escape(recipe['subtitle'])}</p></header>
<p>{recipe['intro']}</p><ul class="mixture-stocks">{stocks}</ul>
<div class="mixture-workbench">{_syringe(recipe)}<div class="mixture-instructions">
<nav class="mixture-step-picker" aria-label="{escape(recipe['title'], quote=True)} preparation steps" hidden>{controls}</nav>
<ol class="mixture-steps">{steps}</ol>
<div class="mixture-step-controls" hidden><button type="button" data-mixture-previous>&lt; Previous</button><span data-mixture-step-count aria-live="polite"></span><button type="button" data-mixture-next>Next &gt;</button></div>
<div class="mixture-total"><b>Finished contents</b><p>{escape(recipe['summary'])}</p></div>
<div class="mixture-tag"><b>{'Example syringe tag' if kind == 'syringe' else 'Bag label check'}</b><div>{tag}</div></div>
</div></div>
<div class="mixture-preview"><h4>{'Preview a measured volume' if kind == 'syringe' else 'Preview component rates'}</h4>
<div class="mixture-interactive" hidden>{preview}<p class="mixture-input-error" data-mixture-error hidden>Enter a number within the shown range.</p></div>
<div class="mixture-output" data-mixture-output aria-live="polite"><p>{escape(static)}</p></div>
<p class="mixture-preview-note">{escape(note)}</p></div>
<p class="mixture-caution"><b>Keep in view:</b> {recipe['caution']}</p>
</article>'''


def render_mixture_guide():
    options = "".join(f'<option value="{r["id"]}">{escape(r["title"])}</option>' for r in RECIPES)
    links = [("Named syringe recipes", "fn_skCompoundLabel.sqf"), ("Draw and Save", "fn_skCompoundCommit.sqf"), ("Cardiac-vial dilution", "fn_epinephrineRecipe.sqf"), ("Prepared syringe pushes", "fn_epinephrinePushStored.sqf"), ("Bag components and final volume", "fn_registerPreparedBag.sqf"), ("Combined hypnotic load", "fn_sedationComponents.sqf"), ("Sedation and reserve", "fn_sedationPhysiology.sqf"), ("Drug interactions", "fn_medicationInteractions.sqf"), ("Pressor pathways", "fn_circHandle.sqf")]
    source_links = " · ".join(f'<a href="{BASE}{path}">{name}</a>' for name, path in links)
    return f'''<section class="sec mixture-guide" id="medication-mixtures" data-mixture-guide>
<div class="sec-head"><h2>Medication mixtures and preparation</h2></div>
<p>Choose a recipe to walk through the in-game controls and watch the syringe fill. The examples use the mod's stock concentrations and preparation rules. Each component keeps its own dose and effects after it reaches the patient.</p>
<p class="infusion-mode-note">With <a href="settings.html#hardcore-medications">Hardcore Medications</a> on, compound syringes use the longest component push time. Ketofol defaults to <b>30 seconds for the current target volume</b>. Read <a href="#slow-medication-pushes">how to set the push rate, stop a partial syringe and continue with menus closed</a>.</p>
<div class="mixture-picker" hidden><label for="mixture-recipe-picker">Preparation example</label><select id="mixture-recipe-picker" data-mixture-picker>{options}</select></div>
{''.join(_recipe(r) for r in RECIPES)}
<div class="mixture-interactions"><h3>What the combinations actually do</h3>
<div class="mixture-effect-grid">
<article><h4>Ketamine + propofol</h4><p>Their induction-normalized active loads add to hypnosis. Ketamine can support heart rate and vascular resistance when reserve is intact. Severe hypovolemia and acidosis reduce that support; propofol's depressant effect can then dominate.</p><p><b>Watch:</b> response, ventilation, pressure and perfusion. Equal milliliters do not mean equal milligrams or guaranteed pressure stability.</p></article>
<article><h4>Hypnotic + opioid</h4><p>Fentanyl or morphine can amplify a hypnotic's effect. Opioids alone do not supply the model's stand-alone hypnosis. Opioid combinations also add respiratory and cardiovascular depression.</p><p><b>Watch:</b> respiratory drive and accumulating sedation. Effects interact whether drugs share a syringe or arrive separately.</p></article>
<article><h4>Propofol + midazolam</h4><p>The model adds a bounded hypnosis synergy while both drugs remain active. It also models extra respiratory and pressure burden. The extra hypnosis fades as either component wears off.</p><p><b>Watch:</b> the combined active load, not just the most recently administered drug.</p></article>
<article><h4>Norepinephrine + epinephrine</h4><p>Norepinephrine's support enters peripheral resistance; epinephrine retains its own cardiac drive. Both contributions still depend on the patient's condition. Combining them does not bypass volume, calcium, temperature or acidosis effects.</p><p><b>Watch:</b> pressure, flow and rhythm. With a shared bag, increasing the clamp increases both component rates together.</p></article>
</div><p>For the relevant game thresholds and serum display limits, use the <a href="#infusion-dose-ranges">infusion dose and risk guide</a>. For ketamine sedation assessment, see <a href="ventilator.html">Ventilator Settings &amp; Tips</a>.</p></div>
<p class="source-note">Game preparation and interaction review {REVISION[:7]}: {source_links}. The syringe images are original mod artwork.</p>
</section>'''
