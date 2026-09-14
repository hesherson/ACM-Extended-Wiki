"""Static shell and reviewed data for the infusion concentration explorer."""
import json
from html import escape
from pathlib import Path


def load_levels():
    return json.loads(Path(__file__).with_name('infusion-levels.json').read_text(encoding='utf-8'))


def level_label(row):
    low, high = row.get('bandLow'), row.get('bandHigh')
    if low is not None and high is not None:
        return f"{low:g}–{high:g} {row['unit']}"
    if high is not None:
        return f"Caution boundary: {high:g} {row['unit']}"
    return 'No serum target in this model'


def render_infusion_explorer():
    data = load_levels()
    options = ''.join(f'<option value="{escape(r["id"])}">{escape(r["medication"])}</option>' for r in data['rows'])
    payload = json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<div class="infusion-explorer" id="infusion-explorer" data-infusion-explorer>
<div class="explorer-heading"><div><h3>Explore delivery and concentration</h3><p>Choose a medication, change its actual delivered rate and inspect how its game value accumulates or clears.</p></div><a href="#medication-mixtures" class="explorer-link">Prepare a mixture &gt;</a></div>
<p class="infusion-mode-note">{escape(data["modeNote"])} <a href="#slow-medication-pushes">Manual push guidance &gt;</a></p>
<div class="explorer-controls" data-explorer-controls hidden>
<label class="explorer-drug"><span>Medication</span><select data-level-drug>{options}</select></label>
<label data-model-control><span>Delivered rate <span data-rate-unit>(mg/min)</span></span><input data-level-rate type="number" min="0" step="any" value="15" inputmode="decimal"></label>
<label data-model-control><span>Chart duration (min)</span><select data-level-duration><option value="15">15</option><option value="30">30</option><option value="60" selected>60</option><option value="120">120</option><option value="240">240</option><option value="360">360</option></select></label>
<label data-weight-control hidden><span>Patient weight (kg)</span><input data-level-weight type="number" min="30" max="200" step="1" value="83" inputmode="decimal"></label>
<div class="explorer-rate-track" data-model-control><label for="level-rate-slider">Adjust delivered rate</label><input id="level-rate-slider" data-level-rate-slider type="range" min="0" max="120" step="0.1" value="15"><span>Slider limits are examples, not dose limits.</span></div>
<div class="explorer-stop" data-model-control><label class="explorer-check"><input data-level-stop-enabled type="checkbox"><span>Stop delivery during the chart</span></label><label><span>Stop at (min)</span><input data-level-stop type="number" min="0" max="60" step="1" value="30" disabled></label></div>
<fieldset class="explorer-modifiers" data-lidocaine-controls hidden><legend>Lidocaine clearance modifiers</legend><label class="explorer-check"><input type="checkbox" data-level-shock><span>Shock modifier (0.6× clearance)</span></label><label class="explorer-check"><input type="checkbox" data-level-esmolol><span>Esmolol proxy &gt; 0.1 (0.7× clearance)</span></label></fieldset>
</div>
<p class="ref-error" data-level-error hidden role="status"></p>
<div data-level-output hidden>
<div class="explorer-metrics"><div><h4 data-level-reference-label>Configured reference</h4><strong data-level-band></strong><span data-level-band-note></span></div><div><h4 data-level-current-label>At the selected time</h4><strong data-level-current></strong><span data-level-time></span></div><div><h4 data-level-plateau-label>With continuous delivery</h4><strong data-level-plateau></strong><span data-level-half-life></span></div></div>
<div class="explorer-plot" data-level-plot>
<p class="explorer-unit" data-level-axis></p>
<svg data-level-svg viewBox="0 0 780 270" role="img" aria-labelledby="level-chart-title level-chart-desc"><title id="level-chart-title">Estimated game concentration over time</title><desc id="level-chart-desc">Use the time slider or touch the curve for exact values. Shading shows the configured debug reference, where one exists.</desc><g data-level-grid></g><rect data-level-shade fill="#f1bd59" opacity="0.10"></rect><g data-level-boundaries></g><path data-level-path fill="none" stroke="#55baf3" stroke-width="3" stroke-linejoin="round"></path><line data-level-cursor stroke="#a8b7c3" stroke-dasharray="4 5" y1="14" y2="226"></line><circle data-level-dot r="5" fill="#f1bd59" stroke="#071015" stroke-width="2"></circle><rect x="60" y="14" width="704" height="212" fill="transparent" data-level-hit></rect></svg>
<div class="explorer-legend"><span><i class="legend-line"></i>Estimated game value</span><span data-level-shade-key><i class="legend-band"></i>Configured reference</span><span>Time in minutes</span></div>
<label class="explorer-time"><span>Inspect time <output data-level-cursor-time>60 min</output></span><input data-level-time-slider type="range" min="0" max="60" step="0.1" value="60"></label>
<p class="explorer-readout" data-level-readout aria-live="polite" aria-atomic="true"></p>
</div>
<p class="explorer-meaning" data-level-meaning></p>
<ul class="explorer-boundaries" data-level-thresholds></ul>
<a data-level-card-link href="#infusion-risk-amiodarone">Dose ranges and cautions &gt;</a>
</div>
<noscript><p>Enable JavaScript for the concentration explorer. Every medication's reference band, timing and cautions remain available in the expandable guide below.</p></noscript>
<details class="explorer-assumptions"><summary>What these numbers can tell you</summary><div><p><strong>There is no universal ideal serum level.</strong> Most bands here are configured debug references. Sedation, pressor response and overdose may read different variables. Lidocaine, esmolol and calcium have explicit concentration or excess thresholds; those boundaries are not a guarantee of safety below them.</p><p>The curve starts at zero, holds actual admitted delivery constant and uses the default configuration. It estimates the source's accumulation in one second steps, including calcium and amiodarone input easing. A prior bolus, changing perfusion, lost IV fluid, addon settings or another drug can change the live result. Calcium is an excess accumulator shared by both salts, not a laboratory calcium measurement. Magnesium's debug band does not align with its raw proxy scale at native treatment rates.</p><p><strong>IV and IO:</strong> the same amount admitted to circulation feeds this estimate. Check the site's actual delivery; a leaking IV can drain a bag without admitting that entire dose.</p></div></details>
<p class="source-note">Concentration and mixture review: <a href="https://github.com/{data['repository']}/tree/{data['revision']}">ACM Extended dev {data['revision'][:7]}</a>. Manual push comparison: <a href="https://github.com/{data['repository']}/blob/{data['rateReviewRevision']}/addons/acm_extended/functions/fn_medicationDriveAdd.sqf">{data['rateReviewRevision'][:7]}</a>. Individual source links accompany each medication below.</p>
<script type="application/json" id="infusion-level-data">{payload}</script>
</div>'''
