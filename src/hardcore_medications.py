"""Source-pinned push guidance shared by access instructions and medication cards."""
from html import escape
import re

REVISION = 'bc90fc7661fa6612cef5f4382f3b181fd5868f11'
SOURCE = f'https://github.com/hesherson/ACM-Extended/blob/{REVISION}/addons/acm_extended/functions/'

PUSHES = [
    ('adenosine', 'Adenosine', 3, 'Keep this one rapid. Slow delivery weakens its brief SVT conversion effect.', 'The manual bolus speed penalty is absent with Hardcore off. Adenosine infusion still has a weak conversion multiplier.'),
    ('ketamine', 'Ketamine', 30, 'Rapid IV / IO delivery can add a temporary loss of respiratory drive on top of the dose effect.', 'The added rapid-ketamine load is absent with Hardcore off; dose, sedation and combination effects remain.'),
    ('calcium-chloride', 'Calcium chloride', 300, 'Check elemental calcium delivery rate and accumulated excess. Excessive delivery can cause severe cardiovascular toxicity.', 'Normal mode spreads manual toxicity input over a reference window. Calcium replacement and excessive accumulated calcium still matter.'),
    ('calcium-gluconate', 'Calcium gluconate', 120, 'Its elemental fraction is lower than calcium chloride, but a large or rapid load can still cause calcium toxicity.', 'Normal mode spreads manual toxicity input over a reference window. This salt remains distinct from calcium chloride.'),
    ('amiodarone', 'Amiodarone', 300, 'Fast delivery can lower vascular resistance and pressure. Follow rhythm, pressure and cumulative dose.', 'Normal mode spreads the custom bolus drive over at least 600 seconds. This is an internal physiology window, not the visible push timer.'),
    ('norepinephrine', 'Norepinephrine', 60, 'The actual push rate feeds existing pressor support. Follow pressure, perfusion and rhythm; no separate rapid-norepinephrine syndrome is added.', 'Normal mode spreads the custom bolus drive over at least 60 seconds. Infusions continue to use actual delivered flow.'),
    ('esmolol', 'Esmolol', 60, 'Delivery builds the concentration that controls heavy blockade, bradycardia and hypotension.', 'Normal mode spreads custom bolus input over at least 60 seconds. Concentration-dependent toxicity remains active.'),
    ('lidocaine', 'Lidocaine', 60, 'Follow accumulated concentration as well as push speed. Seizures and cardiac toxicity remain possible as exposure rises.', 'Normal mode spreads custom bolus input over at least 120 seconds. Existing concentration toxicity and clearance modifiers remain.'),
    ('magnesium', 'Magnesium sulfate', 300, 'Fast delivery can cause bradycardia and hypotension. Check the delivered mass per minute.', 'Normal mode spreads custom bolus input over at least 300 seconds. Actual infusion-rate hazards remain active.'),
    ('propofol', 'Propofol', 30, 'Rapid delivery can add a sharper temporary fall in respiratory drive, vascular resistance and pressure.', 'The added rapid-propofol load is absent with Hardcore off. Normal hypnosis, pressure effects and interactions remain.'),
    ('midazolam', 'Midazolam', 60, 'Rapid delivery can add temporary respiratory and hemodynamic depression, especially with other sedatives.', 'The added rapid-midazolam load is absent with Hardcore off. Normal sedation and combination effects remain.'),
    ('fentanyl', 'Fentanyl', 30, 'Rapid delivery can add temporary opioid respiratory and cardiovascular depression. Include other sedatives in the assessment.', 'The added rapid-opioid load is absent with Hardcore off. Opioid effects, overdose and interactions remain.'),
    ('morphine', 'Morphine', 60, 'Rapid delivery can add temporary opioid respiratory and cardiovascular depression. Allow for effects already on board.', 'The added rapid-opioid load is absent with Hardcore off. Opioid effects, overdose and interactions remain.'),
    ('rocuronium', 'Rocuronium', 30, 'Rapid delivery can modestly accelerate establishment of blockade. Dose remains dominant; paralysis supplies no sedation.', 'The rapid-delivery multiplier is absent with Hardcore off. Native dose-dependent paralysis remains.'),
]


def card_id(key):
    return 'magnesium-sulfate' if key == 'magnesium' else key


def add_push_card_notes(body):
    """Insert one separate note, preserving the existing aligned medication facts."""
    rows = {name: (key, seconds, why, off) for key, name, seconds, why, off in PUSHES}
    parts = re.split(r'(<div\b[^>]*class="[^"]*\bdrug\b[^"]*"[^>]*>)', body)
    for i in range(2, len(parts), 2):
        name = re.search(r'class="dn"[^>]*>([^<]+)</', parts[i])
        if not name or name[1] not in rows:
            continue
        key, seconds, why, off = rows[name[1]]
        note = f'''<aside class="sect push-card-note" data-push-medication="{key}"><h4>Hardcore IV / IO push</h4><p><strong>{seconds} s default</strong> for the current target volume. {escape(why)}</p><p><a href="access.html#slow-push-{key}">Push timing, Stop Push and when speed matters &gt;</a></p></aside>'''
        parts[i] = parts[i].replace('<div class="med-details">', '<div class="med-details">' + note, 1)
    return ''.join(parts)


def render_slow_push_guide():
    rows = []
    for key, name, seconds, why, off in PUSHES:
        minutes = f' ({seconds // 60} min)' if seconds >= 60 and seconds % 60 == 0 else ''
        rows.append(f'''<tr id="slow-push-{key}" data-push-default="{seconds}"><th scope="row"><a href="medications.html#d-{card_id(key)}">{escape(name)}</a></th><td><strong>{seconds} s{minutes}</strong></td><td>{escape(why)}<details class="push-off-note"><summary>With Hardcore off</summary><p>{escape(off)}</p></details></td></tr>''')
    links = [('Suggested times', 'fn_medicationSuggestedPushSec.sqf'), ('Normal and incremental administration', 'fn_skConfirmInjection.sqf'), ('Push start and target volume', 'fn_hardcorePushStart.sqf'), ('Continuous flow and leash', 'fn_hardcorePushTick.sqf'), ('Stop and remaining contents', 'fn_hardcorePushStop.sqf'), ('Corner syringe', 'fn_hardcorePushOverlay.sqf'), ('Reopen the same treatment', 'fn_hardcorePushReopen.sqf'), ('Rapid medication effects', 'fn_hardcoreMedicationRateEffect.sqf'), ('Manual and infusion rate handling', 'fn_medicationDriveAdd.sqf'), ('Flush consolidation', 'fn_medicationLineLocal.sqf')]
    sources = ' · '.join(f'<a href="{SOURCE}{path}">{name}</a>' for name, path in links)
    return f'''<section class="sec slow-push-guide" id="slow-medication-pushes">
<div class="sec-head"><h2>Slow and incremental medication pushes</h2></div>
<p class="lede">With <a href="settings.html#hardcore-medications">[HARDCORE] Medications</a> enabled, IV and IO pushes deliver continuously. Choose a duration, watch the remaining volume and use <b>Stop Push</b> when you want administration to stop.</p>
<div class="callout"><p><b>Check the amount as well as the time.</b> The default times below are game presets, not guaranteed safe limits. A larger or more concentrated syringe delivers more medication per second at the same selected duration. Most drugs benefit from avoiding an abrupt peak; adenosine is the deliberate rapid-push exception.</p></div>
<div class="quick-grid push-mode-grid">
<article class="quick-card"><h3>Hardcore on</h3><p>IV / IO medication enters in measured portions. <b>Push</b> becomes a red <b>Stop Push</b> button. Closing or reopening either medical menu keeps the same push running at its original rate.</p><p>Drug-specific defaults and rapid manual-push consequences apply. IM uses its original administration path.</p></article>
<article class="quick-card"><h3>Hardcore off</h3><p>The normal administration path commits the medication at completion. Closing the dialog before completion cancels that uncommitted administration. The optional IV / IO duration field remains, normally blank with a 3-second default.</p><p>Normal dose effects, interactions, overdose and actual infusion-rate hazards remain active.</p></article>
</div>
<h3 id="push-duration-and-dose">Set the time for the actual contents</h3>
<div class="push-instructions">
<figure class="push-syringe-reference"><img src="img/syringes/syringe_10_ca.png" width="256" height="256" alt="Original 10 mL syringe inventory artwork" loading="lazy"><figcaption>Read the remaining mL and medication contents before starting.</figcaption></figure>
<ol><li>Select the patient, the intended <b>IV / IO site</b> and the prepared syringe.</li><li>Set <b>Seconds to Push over:</b> to <b>1–300 seconds</b>. With Hardcore on, a blank field uses the medication's suggested time.</li><li>The timer covers the <b>current target volume</b>, ordinarily all remaining drug and saline in the syringe. Prepared measured epinephrine uses its selected 1 mL, 2 mL or remaining-volume choice.</li><li>Press <b>Push</b>. The selected syringe, duration and site are locked while it runs. Follow the actual remaining volume and patient response.</li></ol>
</div>
<div class="formula push-rate-example"><strong>Example: 5.00 mL over 30 seconds</strong><div class="math-row"><span class="math-term"><small>Selected volume</small><strong>5.00 mL</strong></span><span aria-hidden="true">÷</span><span class="math-term"><small>Selected time</small><strong>30 s</strong></span><span aria-hidden="true">=</span><span class="math-term"><small>Solution rate</small><strong>0.167 mL/s</strong></span></div><p>After 15 seconds of uninterrupted delivery, about 2.50 mL has been pushed and 2.50 mL remains. Drug mass per second also depends on concentration. This volume example does not select a medication dose.</p></div>
<h3 id="push-default-times">Hardcore default push times</h3>
<p><b>Compounded syringes use the longest component default.</b> Ketofol uses 30 seconds because both ketamine and propofol default to 30 seconds. Other unlisted drugs use the 3-second fallback. The preset does not replace checking the syringe's total medication content.</p>
<div class="scroll" role="region" tabindex="0" aria-label="Hardcore medication push defaults and reasons"><table class="t push-default-table"><thead><tr><th scope="col">Medication</th><th scope="col">Default time</th><th scope="col">Why duration matters</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<details class="dd"><summary><span class="dd-mark"></span><span class="dd-name">Why a default time can still produce a fast medication rate</span></summary><div class="dd-body"><p><b>150 mg amiodarone over 300 seconds = 30 mg/min.</b> That is above the model's 25 mg/min onset for its fast-rate pressure penalty. The 300-second preset does not bypass that threshold. Total dose, elapsed time and response must be considered together.</p><p>Adding saline while keeping the same medication mass and total push time does not reduce the average medication mass per minute. Stopping early reduces the total amount delivered, but does not change the rate that was running before the stop.</p><p>Adenosine uses a different rule: with Hardcore on, the speed multiplier is strongest through 5 seconds per 6 mg equivalent and weakens as delivery slows. The default is 3 seconds. See its card for supported rhythms and flushing.</p><p>The card effect curves describe native timing after a reference dose reaches the patient. An incremental push spreads that dose across time; do not read the curve's peak as a countdown from pressing Push.</p></div></details>
<h3 id="push-stop-and-menus">Stop, close menus and resume</h3>
<div class="quick-grid push-state-grid">
<article class="quick-card"><h4>Close either menu</h4><p>The running push continues. When the Narc Box is closed, the syringe appears in the lower right corner with its actual artwork, moving plunger, <b>remaining mL</b> and <b>mL/s</b>.</p></article>
<article class="quick-card"><h4>Click the corner syringe</h4><p>Return to the same patient, Body Map, IV / IO site and syringe. The red <b>Stop Push</b> button is available. Opening the menu preserves the current timer and rate.</p></article>
<article class="quick-card"><h4>Press Stop Push</h4><p>The remaining contents return to the same carousel syringe, tracked to <b>0.01 mL</b>. Medication already admitted stays delivered. Drug and saline components are removed in their mixture proportions.</p></article>
<article class="quick-card"><h4>Restart the partial syringe</h4><p>Select the remaining syringe and check the duration again. A new run divides its remaining target volume by that duration. It can therefore have a different mL/s from the previous run.</p></article>
</div>
<h3 id="push-leash-and-flush">Stay in range and confirm delivery</h3>
<div class="quick-grid push-mode-grid">
<article class="quick-card"><h4>AED distance limit</h4><p>Stay within the configured <b>AED distance limit</b>. Both people must be outside vehicles or in the same vehicle. The fallback distance is 5 m; use your mission's actual setting.</p><p>Leaving that range or vehicle context stops administration. The push also stops if the selected vascular access is removed or replaced, or the provider becomes incapable of continuing.</p></article>
<article class="quick-card"><h4>Flush-required medication</h4><p>With <b>Require saline flush after push</b> enabled, applicable doses still wait for the required flush. A long incremental push is kept as one logical load per medication, catheter and uninterrupted push session, retaining accumulated dose and elapsed push time.</p><p>Flushing therefore does not turn its many delivery portions into separate simultaneous rapid pushes. Prepared measured epinephrine follows its dedicated delivery path.</p></article>
</div>
<p class="dim">A stopped push can briefly show <b>Stopping...</b> while network acknowledgements settle. Rejected portions are restored to the same syringe; delayed requests are retried. Closing a menu is not a stop command while the Hardcore push is active.</p>
<p>For infusion concentrations and risk ranges, use the <a href="#infusion-dose-ranges">infusion reference</a>. For preparation, see <a href="#medication-mixtures">Ketofol and pressor mixtures</a>. For every Hardcore switch, use the <a href="settings.html#hardcore-settings">Hardcore settings comparison</a>.</p>
<p class="source-note">Push behavior reviewed against ACM Extended dev <b>{REVISION[:7]}</b>: {sources}.</p>
</section>'''
