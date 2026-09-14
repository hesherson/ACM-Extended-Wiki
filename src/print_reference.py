"""Compact, static reference sheets. Browser printing needs no service or plugin."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).parent


def text(value):
    return '<br>'.join(escape(line) for line in value.split('\n'))


def table(headings, rows, widths=None, css=''):
    cols = ''.join(f'<col style="width:{w}%">' for w in widths) if widths else ''
    return (f'<div class="scroll"><table class="t print-table {css}">'
            + (f'<colgroup>{cols}</colgroup>' if cols else '')
            + '<thead><tr>' + ''.join(f'<th scope="col">{h}</th>' for h in headings)
            + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(f'<td>{v}</td>' for v in row) + '</tr>' for row in rows)
            + '</tbody></table></div>')


def sheet(title, code, body, footer):
    return (f'<article class="print-sheet" data-sheet="{code}">'
            f'<header class="print-sheet-header"><div><p>ACM EXTENDED · ARMA 3 GAME REFERENCE</p><h3>{title}</h3></div>'
            f'<span class="sheet-code">{code}</span></header>{body}'
            f'<footer class="print-sheet-footer">{footer}<span>hesherson.github.io/ACM-Extended-Wiki</span></footer></article>')


def pack(key, title, description, contents):
    return (f'<section class="print-pack" id="{key}-chart" data-print-pack="{key}">'
            f'<div class="print-pack-heading"><div><h2 id="{key}-print-heading">{title}</h2><p>{description}</p></div>'
            f'<button type="button" class="print-button" data-print-chart="{key}" hidden>Print {title.lower()}</button></div>'
            + contents + '</section>')


def render_print_reference():
    out = ['<div class="eyebrow">ACM EXTENDED / QUICK REFERENCE</div><h1>Printable quick reference</h1>',
           '<p class="lede">Medication, ventilator, access, rhythm and TBI charts for a second screen or a printed reference beside you.</p>',
           '<div class="print-toolbar"><button class="print-button" type="button" data-print-chart="all" hidden>Print all charts</button>'
           '<p>Choose a chart below. Print in <b>landscape</b> on A4 or US Letter, or choose <b>Save as PDF</b>. '
           'Site navigation and interactive controls are removed automatically. Background printing is optional.</p>'
           '<noscript>Use your browser’s Print command. All seven sheets remain available without JavaScript.</noscript></div>',
           '<nav class="print-jump" aria-label="Printable charts"><a href="#medications-chart">Medications · 3 sheets</a>'
           '<a href="#ventilator-chart">Ventilator · 1 sheet</a><a href="#access-chart">IV / IO · 1 sheet</a>'
           '<a href="#rhythms-chart">Rhythms · 1 sheet</a><a href="#tbi-chart">TBI · 1 sheet</a></nav>']
    medication_sheets = []
    data = json.loads((ROOT / 'print-medications.json').read_text())
    for index, group in enumerate(data['groups'], 1):
        rows = []
        for row in group['rows']:
            name = f'<a href="medications.html#d-{row["id"]}">{escape(row["name"])}</a>'
            if row['id'] == 'dimercaprol':
                name += '<strong class="print-unavailable">NOT IN GAME</strong>'
            rows.append([name] + [text(row[k]) for k in ('use','route','stock','dose','watch')])
        legend = ('<p class="print-legend"><b>IV</b> intravenous · <b>IO</b> intraosseous · <b>IM</b> intramuscular · '
                  '<b>IN</b> intranasal · <b>INH</b> inhaled · <b>PO</b> oral · <b>BUC</b> buccal<br>'
                  '<b>Reference amounts are game model amounts, not safe maxima.</b> Weight examples use 83 kg. '
                  'Check <a href="access.html#slow-medication-pushes">Hardcore push timing</a>, breathing and pressure before repeating.</p>')
        content = legend + table(['Medication','Use','Route','Stock / concentration','Game reference / action','Key cautions'], rows, [12,15,7,14,26,26], 'medication-print-table')
        if group['id'] == 'adjuncts':
            content += ('<p class="print-note"><b>Dedicated osmotherapy pushes:</b> 23.4% HTS, 30 mL: '
                        'about 0.96 mmHg ICP reduction and +0.36 mEq/L sodium. Mannitol 20%, 50 g push item: '
                        'about 0.8 mmHg ICP reduction, no sodium rise. Both complete in 6 s and share the sodium ceiling gate; '
                        'these are game action results, not the full-bag response.</p>')
        footer = ('Read the <a href="medications.html">full medication cards</a> and '
                  '<a href="access.html#infusion-dose-ranges">infusion rate / accumulation limits</a>. '
                  'HR = heart rate; BP = blood pressure; AT = atrial tachycardia; RVR = rapid ventricular response.')
        medication_sheets.append(sheet(group['title'], f'M{index} / 3', content, footer))
    out.append(pack('medications','Medication chart','All 33 medication entries, including the clearly marked unavailable legacy entry. Names link to their full cards.', ''.join(medication_sheets)))

    vent_rows = [
        ['Healthy lung needing support','SIMV VC PS','5','21–40%','VTi 6–8 mL/kg\nI:E 1:2','Supports reduced drive. Follow delivered VTe, MV and patient effort.'],
        ['Pulmonary edema','SIMV VC PS; supported spontaneous path may use CPAP','10–15','40–60%','VTi 6–8 mL/kg\nI:E 1:2 to 1:1.5','PEEP recruits lung units. Watch perfusion, PIP and VTe; treat the fluid problem.'],
        ['Blast lung / ARDS','SIMV PC starting option','5–8','60–95%','VTe 5–6 mL/kg reference\nI:E 1:1.5','Adjust PInsp to delivered volume. Healing depends on support, FiO2 and pressure, not the mode name alone.'],
        ['Pneumothorax','Chest assessment / drainage first; then support as indicated','5 reference after effective drainage','As needed','VTi 6 mL/kg reference\nI:E 1:2','PEEP cannot remove pleural air. Positive pressure can increase leakage; follow chest findings and perfusion.'],
        ['Hemothorax','Assess drainage AND circulating volume','5 reference','As needed','VTi 6 mL/kg reference\nI:E 1:2','Pleural blood and lost blood volume are separate problems. PEEP does not drain the chest.'],
        ['Active CPR','IMV VC (CPR)','0','Per available support','10 breaths/min\nVTi 6 mL/kg, bounded 300–500 mL','Triggering off; unsynchronized breaths. These are configurable defaults. Reassess after ROSC.'],
    ]
    vent = '<p class="print-legend">Starting references from <a href="ventilator.html">Ventilator Settings &amp; Tips</a>. Select settings by the modeled injury and reassess the actual response.</p>'
    vent += table(['Pattern','Mode / priority','PEEP\ncmH2O','FiO2','Volume / timing','Why / reassess'], [[text(c) for c in row] for row in vent_rows], [15,19,10,9,20,27])
    vent += '<div class="print-callouts">'
    for title, body in [
        ('Read delivered ventilation','VTi = inspiratory tidal-volume target; VTe = delivered exhaled volume. MV = minute ventilation. Example: 0.5 L × 12 breaths/min = 6 L/min before delivery limitations.'),
        ('Sedation before paralysis','Ketamine-associated nystagmus supports the sedation assessment. Rocuronium prevents movement but provides no hypnosis or analgesia. Reassess sedation during ventilation.'),
        ('SpO2 is only part of the picture','A high saturation does not prove adequate oxygen delivery during blood loss. Falling peripheral perfusion also makes the reading less dependable. Assess pulse, pressure, chest, EtCO2 and volume.'),
    ]:
        vent += f'<div><h4>{title}</h4><p>{body}</p></div>'
    vent += '</div>'
    out.append(pack('ventilator','Ventilator chart','Six common situations with starting references and what to reassess.', sheet('Ventilator settings & reassessment','V1 / 1',vent,'Game defaults can be changed by mission settings. VTi targets do not guarantee delivered VTe.')))

    access = '<p class="print-legend"><b>Critical patient:</b> establish IO early for urgent medication access. Preserve useful IV sites for independently attached bags. Only one bag can use a site at a time.</p>'
    access += table(['Access','Base capacity / margin','Choose when','Important limitation'], [
        ['14G IV','375 mL/min · 0.65× target','High flow is needed and a large, usable vein supports it.','Tightest insertion margin; oversized attempts add penalties.'],
        ['16G IV','250 mL/min · 0.85× target','Substantial fluid capacity with a suitable vein.','Still needs vein size; oversized for the modeled popliteal target.'],
        ['18G IV','125 mL/min · 1.15× target','A more forgiving target and moderate flow meet the need.','Half the configured 16G flow before other limits.'],
        ['20G IV','87.5 mL/min · 1.35× target','Successful placement in a small/difficult vein is the priority.','Lowest IV capacity. Repeated attempts must not delay IO in a critical patient.'],
        ['IO','Urgent medication route','Poor peripheral access; critical patient; reserve IVs for fluid.','Avoids the peripheral IV leak model, but not systemic drug effects or every cause of stopped delivery.'],
    ], [13,23,30,34])
    access += '<div class="print-callouts">'
    for title, body in [
        ('Choose the site','Palpate a usable vein. Low pressure narrows peripheral targets. After a missed or removed IV, move above the damaged site, use another limb, or choose IO. The same tier alone does not prove safe placement.'),
        ('Vesicants change the plan','Pressors, calcium and other irritants can damage tissue if they leak. IO is useful for urgent pushes. Upper IVs and EJ are not immune. Reassess pain, bruising and delivery at the exact site.'),
        ('Check what reaches the patient','Remove the constricting band. Select the correct site and open the clamp. Flush when required. Bag loss can exceed admitted volume; watch the patient, not just the bag counter.'),
    ]:
        access += f'<div><h4>{title}</h4><p>{body}</p></div>'
    access += '</div><p class="print-note"><b>Drip calculation:</b> mL/min = gtt/min ÷ gtt/mL. Drug/min = concentration × actual admitted mL/min. <b>Example:</b> 30 gtt/min ÷ 60 gtt/mL = 0.5 mL/min. At 10 mcg/mL, this is 5 mcg/min before delivery losses.</p>'
    out.append(pack('access','IV / IO chart','Gauge choice, site selection, vesicants and a compact delivery check.',sheet('Vascular access & delivery','A1 / 1',access,'Base capacity is not guaranteed flow. See <a href="access.html">IV access &amp; infusions</a> for controls, site limits and calculations.')))

    rhythm_notes = {
        'sinus': ('Sinus rhythm','Confirm a pulse; assess perfusion and cause.'),
        'sinus-bradycardia': ('Sinus bradycardia','Slow sinus rate. Assess perfusion and reversible causes.'),
        'sinus-tachycardia': ('Sinus tachycardia','Treat the cause; do not equate all fast rates with SVT.'),
        'atrial-fibrillation': ('Atrial fibrillation','Irregular rhythm. Assess rate, stability and perfusion.'),
        'afib-rvr': ('AFib with RVR','Assess stability; rate control or appropriate synchronized treatment.'),
        'atrial-tachycardia': ('Atrial tachycardia','Organized tachyarrhythmia. Confirm pulse; assess SYNC treatment.'),
        'svt': ('SVT','Regular fast rhythm. Adenosine targets this with a pulse.'),
        'vt-with-pulse': ('VT with a pulse','Pulse separates this from arrest. Assess SYNC treatment.'),
        'pulseless-vt': ('Pulseless VT','Shockable arrest: CPR, ventilation, defibrillation; SYNC off.'),
        'vf': ('Ventricular fibrillation','Shockable arrest: CPR, ventilation, defibrillation; SYNC off.'),
        'torsades': ('Torsades','Game shockable arrest path; magnesium and reversible causes.'),
        'pea': ('PEA','Electrical activity without a pulse. CPR; no defibrillation.'),
        'asystole': ('Asystole','Nonshockable arrest. CPR, ventilation and correct causes.'),
    }
    article = (ROOT / 'content/circulation.html').read_text()
    figures = dict(re.findall(r'<figure class="rhythm-monitor"[^>]*data-rhythm="([^"]+)"[^>]*>(.*?)</figure>',article,re.S))
    rhythms = '<p class="print-legend"><b>Check the pulse:</b> a monitor trace cannot prove perfusion. These are six-second game examples, not calibrated ECG recordings. SYNC = synchronized cardioversion.</p><div class="print-rhythm-grid">'
    for key, (name, note) in rhythm_notes.items():
        figure = figures[key]
        figure = re.sub(r'\b(id|aria-labelledby)="([^"]+)"', lambda m: f'{m[1]}="'+ ' '.join('print-'+v for v in m[2].split())+'"',figure)
        rhythms += f'<div class="print-rhythm"><h4>{name}</h4><figure class="rhythm-monitor" data-no-glossary data-rhythm="{key}">{figure}</figure><p>{note}</p></div>'
    rhythms += '<div class="print-rhythm print-rhythm-key"><h4>Before choosing a treatment</h4><p>Pulse first. Then stability and rhythm. Motion/CPR artifact and a brief post-shock trace can mislead. Reassess after the transient clears.</p></div></div>'
    out.append(pack('rhythms','Cardiac rhythm chart','All 13 monitor examples alongside the treatment category.',sheet('Rhythm recognition & pulse check','R1 / 1',rhythms,'See <a href="circulation.html">Cardiac rhythms</a> for gates, treatment effects and reversible causes. Shapes retain the reviewed game examples.')))

    tbi = ('<p class="print-legend"><b>Structural severity:</b> lasting injury history that sets available reserve. '
           '<b>Acute severity:</b> active burden that can improve. Stable mild/moderate injury can resolve its acute burden to zero; '
           'history can remain without continuing to drive ICP. ICP returns toward its normal <b>10 mmHg baseline</b>, not zero. '
           'Prior herniation can impose a lasting acute severity floor.</p>')
    tbi += table(['Structural grade (S)','Direct hypotension floor','Recovery MAP minimum','Recovery CPP minimum'], [
        ['Mild · S ≤ 0.35','60 mmHg','65 mmHg','No added minimum'],
        ['Moderate · 0.35 < S ≤ 0.60','60–65 mmHg','65 mmHg','No added minimum'],
        ['Severe · 0.60 < S ≤ 0.80','65–75 mmHg','65–75 mmHg','55 mmHg'],
        ['Critical · 0.80 < S ≤ 1.00','75–85 mmHg','75–85 mmHg','60 mmHg'],
    ], [29,23,25,23])
    tbi += ('<p class="print-note"><b>Read the ranges:</b> thresholds rise continuously with structural severity inside each band. '
            'Recovery MAP minimum = the greater of <b>65</b> and the hypotension floor. Below the recovery gate, low CPP can still add injury. '
            '<b>Brain CPP = effective brain MAP − ICP.</b> Head elevation subtracts 6 mmHg from MAP in this check; '
            'the debug CPP display uses unadjusted MAP. These are game defaults, not universal MAP 85 / CPP 70 requirements.</p>')
    tbi += '<div class="print-callouts">'
    for title, body in [
        ('Recovery needs every gate','Meet the grade’s MAP and CPP gates, ICP ≤ 25 mmHg, SpO2 ≥ 90%, ventilation ratio ≥ 0.9, and no active oxygen-delivery deficit. New insults can still add burden; Perfusion OK alone does not prove recovery.'),
        ('Normal SpO2 is not enough','The modeled oxygen-delivery deficit starts below 70% and clears at 78% or higher. Hemorrhage can prevent brain recovery despite normal saturation. Restore delivery and assess volume, pressure and ventilation together.'),
        ('Reserve still matters','Mild autoregulation is essentially preserved; moderate impairment is small. Severe/critical injury keeps less reserve. Low CPP becomes more damaging; excessive CPP can add ICP as autoregulation fails. A higher number is not always better.'),
    ]:
        tbi += f'<div><h4>{title}</h4><p>{body}</p></div>'
    tbi += '</div>'
    tbi += table(['Autonomic state','Systemic effect','Custom junctional bleeding connection'], [
        ['Stable injury','TBI tone near neutral.','No fixed TBI bleeding multiplier. Treat the wound and assess delivery.'],
        ['Rising ICP / compensation','Positive tone supports vasoconstriction, resistance and MAP.','Higher peripheral resistance reduces junctional flow, other factors equal.'],
        ['Reserve failing','Tone becomes labile; constriction and dilation can alternate.','Compensatory vessel spasm weakens as autonomic integrity falls. Full Cushing vitals are not required.'],
        ['Advanced / terminal failure','Negative tone and dominant vasodilation can lower resistance and MAP.','Lower resistance permits more junctional flow; reassess bleeding and perfusion together.'],
    ], [22,35,43])
    tbi += ('<p class="print-note"><b>Autoreg</b> = cerebral autoregulation. <b>Auto</b> = systemic autonomic integrity / signed tone (−1 to +1). '
            '<b>Junctional compensation ability = 25% + 75% × integrity.</b> This scales available compensation, not bleeding directly. '
            'Signed tone already acts through systemic resistance and is not applied again inside the junctional equation.</p>')
    out.append(pack('tbi','TBI chart','Structural injury, recovery gates and the link between autonomic failure and hemorrhage.',
                    sheet('TBI recovery & autonomic response','T1 / 1',tbi,
                          'Game defaults reviewed against <a href="https://github.com/hesherson/ACM-Extended/commit/98d18bb3f60dc9be8cdaf4a43419bb57483c3a3f">dev B119 · 98d18bb</a>. '
                          'In-engine and multiplayer validation pending. See <a href="tbi.html">Head injury</a> and <a href="debug.html">debug fields</a>.')))
    return '\n'.join(out)
