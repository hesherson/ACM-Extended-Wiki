#!/usr/bin/env python3
"\nGLOSSARY. Every advanced term used anywhere in the guide, defined for someone with no medical background.\n\nRules for writing these:\n  - Assume the reader knows nothing. No term may be defined using another undefined term.\n  - Two or three short sentences. If it needs more, it is a page, not a glossary entry.\n  - Say what it IS, then why it matters to a medic. Skip etymology and history.\n  - Plain words over correct but opaque ones. \"Squeeze\" beats \"contractility\" in the first sentence.\n\nUsed two ways: build.py turns {{term}} in content into a clickable popup, and glossary.html is generated\nfrom this same dict so the two can never disagree.\n"

TERMS = {
 # ---- Circulation ----
 "map": ("MAP", "Mean arterial pressure. The average pressure in the arteries over a whole heartbeat, which is what actually pushes blood into organs. Around 65 is the usual minimum for keeping organs alive."),
 "preload": ("Preload", "How full the heart is when it starts to squeeze. A heart with nothing in it has nothing to pump, so bleeding drops output even if the heart itself is fine."),
 "stroke-volume": ("Stroke volume", "How much blood the heart pushes out with one beat. Multiply it by heart rate and you get cardiac output, the total flow around the body."),
 "cardiac-output": ("Cardiac output", "The total amount of blood moved per minute. It is heart rate times how much each beat pushes out, and almost everything in shock comes back to it."),
 "frank-starling": ("Frank Starling", "The rule that a fuller heart squeezes harder, up to a point. It matters because losing volume costs you output faster than you would expect, rather than in a straight line."),
 "vasoconstriction": ("Vasoconstriction", "Blood vessels tightening up, which narrows the pipes and raises pressure. Drugs that do this buy you pressure without adding any actual blood."),
 "pressor": ("Pressor", "A drug that raises blood pressure, usually by tightening blood vessels. It moves the number without fixing why the number was low."),
 "tachyphylaxis": ("Tachyphylaxis", "When a drug works less well each time you give it, over minutes to hours. The dose has not changed, the body has stopped responding to it as strongly."),
 "perfusion": ("Perfusion", "Blood actually reaching tissue and delivering oxygen to it. A casualty can have a pulse and still be perfusing badly."),
 "rosc": ("ROSC", "Return of spontaneous circulation. The heart starting to beat on its own again after cardiac arrest, which is the goal of everything you do during CPR."),
 "chronotropy": ("Chronotropy", "Anything affecting how fast the heart beats. Positive speeds it up, negative slows it down."),

 # ---- Bleeding ----
 "coagulopathy": ("Coagulopathy", "When blood has stopped clotting properly. Bleeding that should have been controllable keeps going, and it is usually caused by the treatment and the environment rather than the wound."),
 "lethal-triad": ("Lethal triad", "Three things that each stop blood clotting and get worse together: being cold, being acidic, and having lost too much blood. Each one makes the other two worse."),
 "permissive-hypotension": ("Permissive hypotension", "Deliberately keeping blood pressure lower than normal while bleeding is uncontrolled, because lower pressure means less blood pushed out of the hole."),
 "ionised-calcium": ("Ionised calcium", "The free, usable form of calcium in blood. Clotting needs it and the heart needs it to squeeze properly, so running low costs you both at once."),
 "citrate": ("Citrate", "The chemical added to stored blood to stop it clotting in the bag. Once inside a casualty it does the same thing to them, by soaking up their calcium."),
 "antifibrinolytic": ("Antifibrinolytic", "A drug that stops the body dissolving clots it has already made. It does not create clot, it protects what is there."),
 "hypovolaemia": ("Hypovolaemia", "Not enough blood or fluid in the circulation. Usually from bleeding, and it is the reason most trauma casualties are unstable."),

 # ---- Airway and breathing ----
 "peep": ("PEEP", "Positive end expiratory pressure. Pressure the ventilator holds in the lungs between breaths so the small air sacs do not collapse shut. It helps oxygen get across, and too much of it squeezes the heart."),
 "tidal-volume": ("Tidal volume", "The size of one breath, measured in millilitres. Too small and they build up carbon dioxide, too big and you tear the lung."),
 "pip": ("PIP", "Peak inspiratory pressure. The highest pressure reached while pushing a breath in. A rising number means the lungs are getting stiffer."),
 "barotrauma": ("Barotrauma", "Damage caused by pressure. Forcing air into a lung harder than it can take can tear it, which is why a rising pressure reading matters."),
 "shunt": ("Shunt", "Blood flowing past parts of the lung that are not working, so it comes back still unoxygenated. Giving more oxygen barely helps, because the blood never meets it."),
 "compliance": ("Compliance", "How easily lungs stretch. Stiff lungs have low compliance, so the same push moves less air."),
 "ards": ("ARDS", "Acute respiratory distress syndrome. The lungs flood with fluid from inflammation rather than from a failing heart, so they stiffen and oxygen struggles to cross into the blood. It needs low volumes and real PEEP, and it is why a lung can look clear from the outside and still be almost impossible to ventilate."),
 "ie-ratio": ("I:E ratio", "How long the machine spends pushing a breath in compared with letting it out. 1:2 means expiration lasts twice as long as inspiration. Too little expiratory time and the next breath starts before the last one has finished leaving, which stacks pressure in the chest."),
 "apnea": ("Apnea", "Not breathing. In a sedated or paralysed casualty this is expected and you breathe for them, and in anyone else it is an emergency."),
 "etco2": ("EtCO2", "The carbon dioxide measured in exhaled breath. It tells you both that the lungs are working and that blood is actually circulating, which is why it drops during cardiac arrest."),
 "hypoventilation": ("Hypoventilation", "Breathing too little, so carbon dioxide builds up. Slow, shallow, or not often enough, and the casualty becomes acidic."),
 "pneumothorax": ("Pneumothorax", "Air trapped in the chest outside the lung, pressing on it. A simple one is uncomfortable, and a tension one squeezes the heart and kills quickly."),
 "hemothorax": ("Hemothorax", "Blood collecting in the space around a lung, usually from a torn vessel rather than the lung itself. It presses the lung down from below, so the casualty cannot fill it however hard the machine pushes, and the fix is to drain it rather than to raise the pressure."),
 "tension-pneumothorax": ("Tension pneumothorax", "Air building up in the chest with no way out, squashing the lung and the heart. It is rapidly fatal and is fixed with a needle or a tube."),
 "ncd": ("NCD", "Needle chest decompression. Putting a needle through the chest wall to let trapped air escape and relieve a tension pneumothorax."),
 "ppv": ("PPV", "Positive pressure ventilation. Pushing air into someone's lungs rather than letting them suck it in. It works, and it also squeezes the veins returning blood to the heart."),
 "intrathoracic-pressure": ("Intrathoracic pressure", "The pressure inside the chest cavity. Raising it, which is what any ventilator does, makes it harder for blood to flow back into the heart."),
 "fio2": ("FiO2", "The fraction of oxygen in the air being delivered, as a percentage. Room air is 21 percent, and this ventilator can enrich up to 95."),
 "iatrogenic": ("Iatrogenic", "Caused by the treatment rather than the injury. A pneumothorax you made with a needle is iatrogenic."),

 # ---- Oxygen ----
 "spo2": ("SpO2", "Oxygen saturation. The percentage of the blood's oxygen carriers that are loaded up. It says nothing about how many carriers there are, which is why it looks fine in someone who has bled out."),
 "haemoglobin": ("Haemoglobin", "The protein in red blood cells that carries oxygen. Lose blood and you lose carriers, so you can be fully saturated and still delivering almost nothing."),
 "oxygen-delivery": ("Oxygen delivery", "How much oxygen actually reaches the tissues per minute. It combines how many carriers there are, how loaded they are, and how fast blood is moving."),
 "hypoxia": ("Hypoxia", "Not enough oxygen reaching tissue. Organs start failing, and the brain is the first to complain and the first to be permanently damaged."),
 "dissociation-curve": ("Dissociation curve", "The S shaped relationship between oxygen pressure and how loaded the blood is. Its shape means a healthy person can lose a lot of pressure safely and a sick one cannot."),
 "acidosis": ("Acidosis", "Blood becoming too acidic, from poor circulation or from carbon dioxide building up. It stops blood clotting and stops pressor drugs working."),
 "colloid": ("Colloid", "A fluid with large molecules that stay inside blood vessels rather than leaking out. It holds volume better than salt water does."),
 "crystalloid": ("Crystalloid", "Plain salt based fluid such as saline. It fills the tank temporarily but carries no oxygen and leaks out of the circulation over time."),

 # ---- Head injury ----
 "icp": ("ICP", "Intracranial pressure. Pressure inside the skull. The skull cannot expand, so any swelling raises it and squeezes the brain."),
 "cpp": ("CPP", "Cerebral perfusion pressure. What is left to push blood into the brain after skull pressure is subtracted from blood pressure. Low blood pressure or high skull pressure both starve the brain."),
 "herniation": ("Herniation", "Brain tissue being squeezed out of position by pressure. It is the point at which damage becomes permanent, and it is the only irreversible state in this addon."),
 "secondary-insult": ("Secondary insult", "Extra brain damage happening after the original impact, caused by low oxygen, low blood pressure or high carbon dioxide. It is the part you can prevent."),
 "osmotherapy": ("Osmotherapy", "Using a concentrated fluid to pull water out of swollen brain tissue, which lowers pressure inside the skull."),
 "obtundation": ("Obtundation", "Reduced alertness. The casualty is not unconscious but is dulled, slow to respond, and not fully with you."),

 # ---- Drugs ----
 "moa": ("Mechanism of action", "How a drug actually produces its effect at the level of the body's machinery, rather than what it is used for."),
 "vesicant": ("Vesicant", "A drug that damages tissue if it leaks out of the vein. The injury develops over hours, so a bad line causes a problem you find out about later."),
 "extravasation": ("Extravasation", "A drug leaking out of the vein into surrounding tissue. Harmless with some drugs and destructive with others."),
 "antiarrhythmic": ("Antiarrhythmic", "A drug that corrects an abnormal heart rhythm, usually by changing how electrical signals move through heart muscle."),
 "neuromuscular-blocker": ("Neuromuscular blocker", "A drug that paralyses muscles. It does nothing for pain or awareness, so a casualty given one without sedation is awake and unable to move or tell you."),
 "rsi": ("RSI", "Rapid sequence intubation. Giving a sedative and a paralytic together to place a breathing tube quickly and safely."),
 "sympathomimetic": ("Sympathomimetic", "A drug that mimics the fight or flight response. Raises heart rate, blood pressure and alertness."),
 "half-life": ("Half-life", "The time it takes for half the drug to leave the body. Short means it wears off fast and needs repeating, long means a mistake stays with you."),
 "therapeutic-window": ("Therapeutic window", "The gap between enough drug to work and enough to poison. A narrow window means small dosing errors matter."),
 "clearance": ("Clearance", "How fast the body removes a drug. Poor circulation and other drugs can slow it, which makes a normal dose build up to a dangerous level."),

 # ---- Flight ----
 "boyles-law": ("Boyle's Law", "Gas expands as the surrounding pressure drops. Climb in an aircraft and any trapped air in the body gets bigger, which is why a small pneumothorax becomes a big one."),
 "daltons-law": ("Dalton's Law", "The pressure driving oxygen into the blood falls as you climb, even though the air is still 21 percent oxygen. A casualty who was borderline at ground level becomes hypoxic in the air."),
 "henrys-law": ("Henry's Law", "Gas dissolved in liquid comes out of solution as pressure falls, like opening a fizzy drink. It matters for anyone who has been diving recently."),
 "cabin-altitude": ("Cabin altitude", "The effective altitude inside the aircraft. A helicopter has none, so the cabin is at whatever height it is flying."),

 # ---- Access ----
 "io": ("IO", "Intraosseous. A needle drilled into bone marrow when a vein cannot be found. It works as fast as a vein and is far more reliable in shock."),
 "iv": ("IV", "Intravenous. Into a vein, which is the usual route for fluids and drugs when you can find one."),
 "cannulation": ("Cannulation", "Getting a plastic tube into a vein so fluid and drugs can be given. Each failed attempt damages the vein and makes the next one harder."),
 "gauge": ("Gauge", "The thickness of a needle or cannula. Confusingly, a lower number means a wider tube, and wider means faster flow."),
 "bolus": ("Bolus", "A quick, measured amount of fluid or drug given all at once rather than dripped in."),

 # ---- Pharmacology, added for the drug cards ----
 "anxiolysis": ("Anxiolysis", "Taking the edge off fear and agitation without knocking someone out. A casualty who is calm rather than fighting you is easier and safer to treat."),
 "gaba": ("GABA A agonist", "A drug that boosts the brain's main calming signal. The result is sedation, and at higher doses unconsciousness. Most sedatives work this way."),
 "alpha-1": ("Alpha 1 receptor", "A switch on blood vessels. Turn it on and the vessels tighten, which raises blood pressure without adding any blood."),
 "beta-1": ("Beta 1 receptor", "A switch on the heart. Turn it on and the heart beats faster and squeezes harder. Block it and it slows down."),
 "svr": ("Systemic vascular resistance", "How tight the whole network of blood vessels is. Tighter pipes mean higher pressure for the same amount of blood moving through them."),
 "contractility": ("Contractility", "How hard the heart squeezes on each beat, separate from how fast it beats or how full it is."),
 "coronary-perfusion": ("Coronary perfusion", "Blood reaching the heart muscle itself. During CPR this is the thing chest compressions are trying to achieve, because a starved heart will not restart."),
 "nmda": ("NMDA antagonist", "A drug that blocks a specific brain signal involved in pain and awareness. Ketamine works this way, which is why it dulls pain without shutting down breathing."),
 "dissociation": ("Dissociation", "A state where someone is disconnected from what is happening to them rather than asleep. Their eyes may be open and they keep breathing, but they are not present."),
 "mu-opioid": ("Mu opioid receptor", "The main switch opioids act on. Turning it on blocks pain, and turning it on too hard slows or stops breathing."),
 "histamine": ("Histamine release", "Some drugs make the body dump histamine, which widens blood vessels and drops blood pressure. It is why morphine is a poor choice in someone who is bleeding."),
 "vasodilation": ("Vasodilation", "Blood vessels widening. The pipes get bigger, so pressure falls even though the amount of blood has not changed."),
 "amnesia": ("Anterograde amnesia", "Not forming new memories from the moment the drug takes effect. The casualty may be responsive at the time and remember none of it afterwards."),
 "competitive-antagonist": ("Competitive antagonist", "A drug that competes with something else for the same receptor and wins by outnumbering it. Give enough and it displaces whatever was there."),
 "acetylcholine": ("Acetylcholine", "The chemical messenger nerves use to tell muscles to contract. Block it and the muscle cannot move, however hard the nerve tries."),
 "nmj": ("Neuromuscular junction", "The gap where a nerve meets a muscle and tells it to move. Paralytic drugs work here, which is why they stop movement without touching consciousness."),
 "potassium-channel": ("Potassium channel", "A gate in heart cells that controls how quickly the cell resets between beats. Blocking it lengthens the reset, which is how some rhythm drugs work."),
 "repolarisation": ("Repolarisation", "The heart cell resetting electrically after a beat so it is ready for the next one. Slow it too much and the rhythm becomes unstable."),
 "refractory-period": ("Refractory period", "The short window after a beat when heart muscle cannot fire again. Lengthening it stops fast abnormal rhythms from sustaining themselves."),
 "sodium-channel": ("Sodium channel", "The gate that starts each heartbeat's electrical signal. Blocking it slows conduction, which suppresses extra beats coming from damaged muscle."),
 "ectopy": ("Ectopy", "Extra heartbeats fired from the wrong place. A few are harmless, and a run of them can turn into a lethal rhythm."),
 "afterdepolarisation": ("Afterdepolarisation", "A stray electrical twitch happening while the heart cell is still resetting. It is the trigger that starts torsades."),
 "plasmin": ("Plasmin", "The enzyme that dissolves clots. Useful for clearing old clot, and unhelpful when it dismantles the clot holding a wound shut."),
 "plasminogen": ("Plasminogen", "The inactive form of the clot dissolving enzyme, sitting in blood waiting to be switched on. Blocking that switch protects clot you have already made."),
 "osmotic": ("Osmotic gradient", "Water moving toward whatever is more concentrated. Put concentrated fluid in the blood and water is pulled out of swollen tissue into it."),
 "diuresis": ("Diuresis", "Making someone produce a lot of urine. It removes water from the whole body, which is unhelpful if they are already short of volume."),
 "cardioselective": ("Cardioselective", "A drug that acts mainly on the heart and mostly leaves the lungs alone. It matters because non selective versions can close the airways of an asthmatic."),
 "ht3": ("5 HT3 receptor", "A serotonin switch in the brain and gut that triggers vomiting. Blocking it is how most antiemetics work."),
 "emesis": ("Emesis", "Vomiting. In a casualty with a poor airway it is far more dangerous than it sounds, because what comes up can go down into the lungs."),
 "beta-lactam": ("Beta lactam", "The largest family of antibiotics, including penicillins and cephalosporins. They kill bacteria by preventing them building a cell wall."),
 "broad-spectrum": ("Broad spectrum", "An antibiotic that covers many different bacteria rather than one specific type. The right choice when you do not know what is in the wound."),
 "qt": ("QT interval", "A measurement on the ECG of how long the heart takes to reset between beats. Stretch it too far and the heart becomes prone to a lethal rhythm called torsades."),
 "hypernatraemia": ("Hypernatraemia", "Too much sodium in the blood. A risk when giving concentrated salt solutions, and correcting it too fast causes its own harm."),
 "myelinolysis": ("Central pontine myelinolysis", "Brain damage caused by correcting a sodium problem too quickly. It is the reason concentrated salt is given carefully rather than fast."),
 "myocardial-depression": ("Myocardial depression", "The heart squeezing more weakly than it should. Some drugs cause it directly, and it is worst in a casualty who has nothing in reserve."),
 "catecholamine": ("Catecholamine", "The family of fight or flight chemicals including adrenaline. They raise heart rate, squeeze blood vessels and raise blood pressure."),
 "chelate": ("Chelate", "To chemically grab and hold onto something so the body cannot use it. Citrate in stored blood chelates calcium, which is why transfusion costs you calcium."),
 "precipitate": ("Precipitate", "Two compatible looking fluids reacting in the line and forming solid particles. It blocks the line and can send solid material into the casualty."),
 "anaphylaxis": ("Anaphylaxis", "A severe, whole body allergic reaction. Blood vessels dump their pressure and the airway swells shut, and it kills within minutes without adrenaline."),
 "bradycardia": ("Bradycardia", "A heart rate that is too slow. In a shocked casualty it usually means the body has run out of ability to compensate."),
 "tachycardia": ("Tachycardia", "A heart rate that is too fast. Often the first sign of blood loss, because the body speeds up to make up for smaller beats."),
 "atropine": ("Atropine", "A drug that speeds up a heart that is beating too slowly, by removing the brake the nervous system keeps on it."),
 "adenosine": ("Adenosine", "A drug that briefly stops the heart to reset a fast abnormal rhythm. It is first choice for SVT and works within seconds."),
 "torsades": ("Torsades de pointes", "A specific lethal rhythm where the ECG trace twists around the baseline. It is caused by a stretched QT interval, and magnesium is the treatment."),
 "hyperkalaemia": ("Hyperkalaemia", "Too much potassium in the blood, which stops the heart conducting properly. Crush injuries and burns release it from damaged muscle."),
 "hypocalcaemia": ("Hypocalcaemia", "Too little usable calcium. Blood stops clotting properly and the heart squeezes more weakly, both at once."),
 "amide": ("Amide anaesthetic", "One of the two chemical families of local anaesthetic, which includes lidocaine. Allergy to one family does not mean allergy to the other."),
 "sympathetic-outflow": ("Sympathetic outflow", "The fight or flight nerve signal that raises heart rate and blood pressure. Ketamine leans on it, which is why it usually supports pressure rather than dropping it."),
 "serum-level": ("Serum level", "How much of a drug is actually in the blood right now, as opposed to how much you gave. It is what decides whether a drug is working or poisoning."),
 "plateau-level": ("Plateau", "The steady level a drug settles at when what you are giving matches what the body is removing. Raise the rate or slow the clearance and the plateau climbs."),
 "titrate": ("Titrate", "Giving a drug in small steps and watching the effect, rather than giving a set dose and hoping. You stop when you get what you wanted."),
 "ett": ("ETT", "Endotracheal tube. The breathing tube that goes through the vocal cords into the windpipe. It is the most secure airway there is."),
 "otfc": ("OTFC", "Oral transmucosal fentanyl citrate. A fentanyl lozenge absorbed through the cheek, used when there is no line. Slower and harder to control than an injection."),
 "rvr": ("RVR", "Rapid ventricular response. The lower chambers of the heart beating too fast because the upper chambers are firing chaotically. The heart pumps poorly at that rate."),
 "analgesia": ("Analgesia", "Pain relief. Worth separating from sedation, because a drug can make someone unresponsive while leaving them fully able to feel pain."),
 "sedation": ("Sedation", "Making someone drowsy or unconscious. It does nothing for pain on its own, which is why sedatives and painkillers are often given together."),
}

# Circulation and flight physiology reference updates.
TERMS.update({
    "stroke-volume": [
        "Stroke volume",
        "The volume ejected by a ventricle with each effective heartbeat. It depends on filling, contraction strength and the load the ventricle ejects against."
    ],
    "svr": [
        "Systemic vascular resistance",
        "Resistance to blood flow through the systemic circulation. Arteriolar narrowing increases it; a maintained blood pressure can coexist with reduced cardiac output."
    ],
    "oxygen-delivery": [
        "Oxygen delivery",
        "Oxygen reaching the tissues through the circulation. It is cardiac output multiplied by arterial oxygen content, so normal saturation alone does not establish adequate delivery."
    ],
    "vasoconstriction": [
        "Vasoconstriction",
        "Narrowing of blood vessels as their smooth muscle contracts. Arteriolar constriction raises resistance; venous constriction can support venous return."
    ],
    "poiseuille": [
        "Poiseuille’s law",
        "An ideal laminar flow relationship: flow increases with pressure difference and the fourth power of internal radius, and decreases with viscosity and length. The assumptions limit direct application to living vessels and ventilator circuits."
    ]
})


# Shared plain-language definitions and corrections used throughout the wiki.
TERMS.update({
    "aed": [
        "AED",
        "Automated external defibrillator: a device that analyzes heart rhythm and can deliver a shock for suitable arrest rhythms."
    ],
    "afib": [
        "Atrial fibrillation (AFib)",
        "Disorganized activity in the upper heart chambers that produces an irregular heartbeat. RVR means the lower chambers are also beating rapidly."
    ],
    "afterload": [
        "Afterload",
        "The pressure and resistance the heart must overcome to push blood out. ACME changes vascular resistance and blood pressure, but the reviewed flow calculations do not use a separate afterload value."
    ],
    "agonal": [
        "Agonal respirations",
        "Occasional gasping that does not provide normal effective breathing."
    ],
    "agonist": [
        "Agonist",
        "A substance that activates a receptor and produces an effect."
    ],
    "alveolar": [
        "Alveolar",
        "Related to the tiny air sacs in the lungs where gases pass between air and blood."
    ],
    "alveoli": [
        "Alveoli",
        "Tiny air sacs in the lungs where oxygen enters the blood and carbon dioxide leaves it."
    ],
    "amiodarone": [
        "Amiodarone",
        "A medication used by the mod for selected abnormal heart rhythms. Its card lists the supported rhythms and dose related effects."
    ],
    "anisocoria": [
        "Anisocoria",
        "Unequal pupil sizes."
    ],
    "antagonist": [
        "Antagonist",
        "A substance that blocks or reduces another substance's effect."
    ],
    "anticoagulation": [
        "Anticoagulation",
        "Reduction of the blood's ability to form clots."
    ],
    "arrhythmia": [
        "Arrhythmia",
        "An abnormal heart rhythm, which may be too fast, too slow, irregular or ineffective."
    ],
    "arteriole": [
        "Arteriole",
        "A small artery that helps control resistance and the amount of blood reaching nearby tissue."
    ],
    "aspiration": [
        "Aspiration",
        "Material such as vomit entering the airway or lungs."
    ],
    "asystole": [
        "Asystole",
        "No effective electrical activity from the heart. The monitor shows a near flat trace and there is no pulse."
    ],
    "atelectasis": [
        "Atelectasis",
        "Collapse or loss of air in part of the lung, reducing the area available for gas exchange."
    ],
    "atrial-kick": [
        "Atrial kick",
        "The extra filling supplied when the upper heart chambers squeeze before the lower chambers. The reviewed DO2 calculation does not track this separately."
    ],
    "atrial-tachycardia": [
        "Atrial tachycardia",
        "A fast rhythm that begins in the upper chambers of the heart, outside the usual pacemaker."
    ],
    "atrium": [
        "Atrium",
        "One of the heart's two upper chambers, which receives returning blood."
    ],
    "auscultation": [
        "Auscultation",
        "Listening to body sounds with a stethoscope, such as breath sounds in the chest."
    ],
    "auto-peep": [
        "Auto-PEEP",
        "Pressure left in the lungs because the patient did not fully breathe out before the next breath."
    ],
    "av-node": [
        "AV node",
        "The electrical relay between the upper and lower heart chambers. Slowing this relay can slow some fast rhythms."
    ],
    "barometric": [
        "Barometric pressure",
        "The pressure of the surrounding air. It falls as altitude increases."
    ],
    "benzodiazepine": [
        "Benzodiazepine",
        "A medication group that can calm, sedate and treat seizures."
    ],
    "bilateral": [
        "Bilateral",
        "Present on both sides of the body."
    ],
    "bpm": [
        "BPM",
        "Beats per minute, the unit used for heart rate."
    ],
    "bradypnea": [
        "Bradypnea",
        "Slow breathing."
    ],
    "bronchospasm": [
        "Bronchospasm",
        "Tightening of the muscles around smaller airways, narrowing them and making airflow harder."
    ],
    "buccal": [
        "Buccal",
        "Delivered against the inside of the cheek, where medication can be absorbed through the lining of the mouth."
    ],
    "bvm": [
        "BVM",
        "Bag valve mask: a hand squeezed bag used to provide breaths. In the game, active bagging is a continuing provider action."
    ],
    "calcium-chloride": [
        "Calcium chloride",
        "A calcium containing medication. The mod uses delivered calcium to correct modeled calcium deficit and tracks excess exposure."
    ],
    "calcium-gluconate": [
        "Calcium gluconate",
        "A calcium containing medication with less elemental calcium per gram than calcium chloride. The mod accounts for this difference."
    ],
    "capillary-refill": [
        "Capillary refill",
        "How long color takes to return after pressure is released from a fingertip or similar area. It is one clue about circulation."
    ],
    "cardiac-arrest": [
        "Cardiac arrest",
        "Loss of effective circulation because the heart is not pumping useful blood flow."
    ],
    "cardioversion": [
        "Cardioversion",
        "An electrical shock timed to an organized heartbeat to treat an appropriate abnormal rhythm."
    ],
    "catheter": [
        "Catheter",
        "A small tube placed in the body. An IV catheter provides a route for fluid and medication into a vein."
    ],
    "cbrn": [
        "CBRN",
        "Chemical, biological, radiological and nuclear hazards."
    ],
    "ceftriaxone": [
        "Ceftriaxone",
        "An antibiotic medication. Its card describes the routes and effects supported in the game."
    ],
    "cerebral": [
        "Cerebral",
        "Related to the brain."
    ],
    "coagulation": [
        "Coagulation",
        "The process of forming a blood clot."
    ],
    "contraindication": [
        "Contraindication",
        "A reason a treatment should not be used or needs special caution."
    ],
    "coronary": [
        "Coronary",
        "Related to the blood vessels that supply the heart muscle."
    ],
    "cpr": [
        "CPR",
        "Cardiopulmonary resuscitation: chest compressions and breathing support during cardiac arrest."
    ],
    "cumulative": [
        "Cumulative dose",
        "The total amount given across repeated doses."
    ],
    "cushing-response": [
        "Cushing response",
        "A pattern associated with severe pressure inside the skull: rising blood pressure, slowing pulse and abnormal breathing."
    ],
    "cyanosis": [
        "Cyanosis",
        "A blue or dusky appearance of skin or visible tissue."
    ],
    "dead-space": [
        "Dead space",
        "Air that is moved with breathing but does not take part in gas exchange."
    ],
    "defibrillation": [
        "Defibrillation",
        "An electrical shock used to stop a shockable cardiac arrest rhythm."
    ],
    "diaphoretic": [
        "Diaphoretic",
        "Sweaty."
    ],
    "diastole": [
        "Diastole",
        "The part of the heartbeat when the heart relaxes and fills with blood."
    ],
    "diastolic": [
        "Diastolic pressure",
        "The lower number in a blood pressure reading, measured between heartbeats."
    ],
    "dimercaprol": [
        "Dimercaprol",
        "A medication used for the mod's lewisite chemical exposure treatment."
    ],
    "distributive-shock": [
        "Distributive shock",
        "Poor circulation caused partly by blood vessels losing their normal tone and distributing blood ineffectively."
    ],
    "ecg": [
        "ECG",
        "Electrocardiogram: a recording of the heart's electrical activity. It shows rhythm but does not confirm a pulse."
    ],
    "ej": [
        "External jugular (EJ)",
        "A vein near the surface of the side of the neck. The mod provides a separate IV placement site here."
    ],
    "elemental-calcium": [
        "Elemental calcium",
        "The actual calcium contained in a calcium salt. Equal masses of different calcium salts do not contain equal amounts of calcium."
    ],
    "endobronchial": [
        "Endobronchial",
        "Inside one of the main branches of the windpipe. A tube placed too deeply can ventilate mainly one lung."
    ],
    "epinephrine": [
        "Epinephrine",
        "A medication with heart rate and pressure effects. The mod has separate reference amounts and delivery rules for standard and measured push doses."
    ],
    "ertapenem": [
        "Ertapenem",
        "An antibiotic medication with route specific timing in the game."
    ],
    "esketamine": [
        "Esketamine",
        "A ketamine related medication supplied as a nasal product in the game."
    ],
    "esmolol": [
        "Esmolol",
        "A medication that slows heart rate. The mod also models reduced pressure and dose related toxicity."
    ],
    "fentanyl": [
        "Fentanyl",
        "An opioid pain medication available in injectable and lozenge forms. The mod handles their doses and onset differently."
    ],
    "fibrin": [
        "Fibrin",
        "Protein strands that form the supporting mesh of a blood clot."
    ],
    "fibrinolysis": [
        "Fibrinolysis",
        "The process that breaks down blood clots."
    ],
    "fowlers": [
        "Fowler's position",
        "Sitting with the upper body raised."
    ],
    "heart-rate": [
        "Heart rate",
        "The number of heartbeats per minute. A monitor may show electrical activity even when there is no effective pulse."
    ],
    "hematocrit": [
        "Hematocrit",
        "The fraction of blood volume occupied by red blood cells."
    ],
    "hemodilution": [
        "Hemodilution",
        "A lower concentration of blood cells after fluid is added to the circulation."
    ],
    "hemorrhage": [
        "Hemorrhage",
        "Bleeding, either outside the body or into an internal space."
    ],
    "hemostasis": [
        "Hemostasis",
        "Stopping bleeding through vessel response, clot formation or treatment."
    ],
    "hyaluronidase": [
        "Hyaluronidase",
        "A local treatment for selected medication leak injuries in the mod. It is applied around the affected tissue."
    ],
    "hypercapnia": [
        "Hypercapnia",
        "Too much carbon dioxide in the blood, commonly from inadequate breathing."
    ],
    "hypertension": [
        "Hypertension",
        "High blood pressure."
    ],
    "hyperthermia": [
        "Hyperthermia",
        "An abnormally high body temperature."
    ],
    "hypertonic-saline": [
        "Hypertonic saline",
        "A salt solution more concentrated than ordinary saline. The mod uses 3% saline for its brain pressure treatment system."
    ],
    "hyperventilation": [
        "Hyperventilation",
        "Breathing that removes carbon dioxide faster than the body produces it."
    ],
    "hypnosis": [
        "Hypnosis",
        "Medication induced reduction in awareness or consciousness. It does not by itself describe pain relief or muscle paralysis."
    ],
    "hypocapnia": [
        "Hypocapnia",
        "Less carbon dioxide in the blood than normal, often from breathing more than needed."
    ],
    "hypoglycemia": [
        "Hypoglycemia",
        "Low blood sugar."
    ],
    "hypokalemia": [
        "Hypokalemia",
        "Low potassium in the blood. Potassium helps heart and muscle cells work electrically."
    ],
    "hypoperfusion": [
        "Hypoperfusion",
        "Too little blood flow reaching the tissues."
    ],
    "hypotension": [
        "Hypotension",
        "Blood pressure that is low. Interpret it together with pulse, mental status, bleeding and other signs of blood flow."
    ],
    "hypothermia": [
        "Hypothermia",
        "An abnormally low body temperature. In the mod, severe cooling affects clotting, circulation and medication response."
    ],
    "hypovolemic-shock": [
        "Hypovolemic shock",
        "Poor circulation caused by too little circulating fluid or blood."
    ],
    "hypoxemia": [
        "Hypoxemia",
        "Too little oxygen in the arterial blood. This differs from poor tissue oxygen delivery caused by inadequate blood flow."
    ],
    "im": [
        "IM",
        "Intramuscular: medication delivered into a muscle. It must be absorbed before reaching the bloodstream."
    ],
    "infiltration": [
        "Infiltration",
        "Fluid leaking from an IV into nearby tissue instead of entering the bloodstream."
    ],
    "inhaled": [
        "Inhaled",
        "Breathed into the lungs."
    ],
    "intranasal": [
        "Intranasal",
        "Delivered through the nose, usually as a spray or mist."
    ],
    "intubation": [
        "Intubation",
        "Placing a breathing tube into the windpipe to provide an airway for ventilation."
    ],
    "ischemia": [
        "Ischemia",
        "Insufficient blood supply to a tissue, reducing the oxygen and nutrients it receives."
    ],
    "jaundice": [
        "Jaundice",
        "Yellow discoloration of skin or the whites of the eyes."
    ],
    "ketamine": [
        "Ketamine",
        "A medication used in the mod for pain relief and sedation, with different effects depending on dose and route."
    ],
    "laminar": [
        "Laminar flow",
        "Smooth flow in layers. Poiseuille's relationship assumes this type of flow."
    ],
    "laryngoscopy": [
        "Laryngoscopy",
        "Using a scope to see the opening of the windpipe during breathing tube placement."
    ],
    "laryngospasm": [
        "Laryngospasm",
        "A sudden tightening at the voice box that can block airflow."
    ],
    "lateral-recumbent": [
        "Lateral recumbent",
        "Lying on one side."
    ],
    "lidocaine": [
        "Lidocaine",
        "A medication used in the mod for selected ventricular rhythms and local pain treatment. Its effect depends on route and dose."
    ],
    "local-anesthetic": [
        "Local anesthetic",
        "A medication that reduces sensation in a particular area."
    ],
    "lumen": [
        "Lumen",
        "The hollow inside of a tube, catheter or blood vessel."
    ],
    "magnesium-sulfate": [
        "Magnesium sulfate",
        "A medication used by the mod to treat torsades. The infusion effect develops as the medication is delivered."
    ],
    "mannitol": [
        "Mannitol",
        "A medication used to draw water out of swollen tissue. In the game its brain pressure effect depends on the delivery action and amount."
    ],
    "metabolic": [
        "Metabolic",
        "Related to chemical processes in the body's cells, such as using energy and producing waste."
    ],
    "midazolam": [
        "Midazolam",
        "A medication used for sedation and selected seizure treatments in the mod. It can reduce breathing and blood pressure."
    ],
    "minute-ventilation": [
        "Minute ventilation (MV)",
        "The volume of air moved in one minute, usually expressed in L/min: breath volume multiplied by breathing rate. In this wiki, MV adequacy is a game support ratio rather than a volume in L/min."
    ],
    "miosis": [
        "Miosis",
        "Small or narrowed pupils."
    ],
    "morphine": [
        "Morphine",
        "An opioid pain medication. The mod also models reduced breathing and other dose related effects."
    ],
    "mottled": [
        "Mottled",
        "Patchy changes in skin color, often seen when circulation is poor."
    ],
    "mydriasis": [
        "Mydriasis",
        "Large or widened pupils."
    ],
    "myocardial": [
        "Myocardial",
        "Related to the heart muscle."
    ],
    "naloxone": [
        "Naloxone",
        "A medication that reverses opioid effects. Other causes of sedation or unconsciousness can remain."
    ],
    "newtonian": [
        "Newtonian fluid",
        "A fluid whose viscosity stays constant as its rate of flow changes. This is one assumption in the ideal Poiseuille equation."
    ],
    "norepinephrine": [
        "Norepinephrine",
        "A medication used to support blood pressure, mainly through increased vascular resistance in the reviewed game model."
    ],
    "obstructive-shock": [
        "Obstructive shock",
        "Poor circulation caused by a physical obstacle to blood flow, such as pressure from a tension pneumothorax."
    ],
    "occlusion": [
        "Occlusion",
        "A blockage that prevents normal flow."
    ],
    "ondansetron": [
        "Ondansetron",
        "A medication used to reduce nausea and vomiting."
    ],
    "opioid": [
        "Opioid",
        "A medication group used for pain relief that can also reduce breathing and alertness."
    ],
    "oral": [
        "Oral",
        "Taken by mouth and swallowed."
    ],
    "p-wave": [
        "P wave",
        "The ECG wave representing electrical activation of the upper heart chambers."
    ],
    "paco2": [
        "PaCO2",
        "The pressure of carbon dioxide in arterial blood. ACME tracks retained carbon dioxide separately from the exhaled EtCO2 reading."
    ],
    "palpation": [
        "Palpation",
        "Checking by touch, such as feeling for a pulse or vein."
    ],
    "pao2": [
        "PaO2",
        "The pressure of oxygen dissolved in arterial blood. It is different from the percentage of hemoglobin carrying oxygen."
    ],
    "pao2-alveolar": [
        "Alveolar oxygen pressure",
        "The oxygen pressure inside the tiny air sacs of the lungs, before oxygen enters the blood."
    ],
    "paracetamol": [
        "Paracetamol",
        "A pain medication delivered through a fixed product treatment action in the game."
    ],
    "paralysis": [
        "Paralysis",
        "Loss of muscle movement. A paralytic can stop breathing without providing pain relief or unconsciousness."
    ],
    "partial-pressure": [
        "Partial pressure",
        "The contribution of one gas, such as oxygen, to the total pressure of a gas mixture."
    ],
    "patency": [
        "Patency",
        "How open a passage is. An open airway permits airflow; an open IV line permits fluid flow."
    ],
    "pea": [
        "Pulseless electrical activity (PEA)",
        "Electrical activity appears on the monitor, but the heart is not producing an effective pulse. The game treats true PEA as having no mechanical cardiac output."
    ],
    "penthrox": [
        "Penthrox",
        "An inhaled pain relief product supplied through a treatment action in the game."
    ],
    "peripheral-resistance": [
        "Peripheral resistance",
        "The resistance opposing blood flow through the body. The game combines several effects into a resistance value used to calculate blood pressure; its scale is not a clinical SVR measurement."
    ],
    "perrl": [
        "PERRL",
        "Pupils equal, round and reactive to light."
    ],
    "pfc": [
        "PFC",
        "Prolonged field care: continued casualty care when evacuation is delayed."
    ],
    "phentolamine": [
        "Phentolamine",
        "A local treatment for selected vasopressor leak injuries in the mod."
    ],
    "platelet": [
        "Platelet",
        "A small blood component that helps form a plug at an injured vessel."
    ],
    "pleural": [
        "Pleural",
        "Related to the thin lining around the lung and the space between the lung and chest wall."
    ],
    "pneumothorax-simple": [
        "Simple pneumothorax",
        "Air between the lung and chest wall that reduces lung expansion without the pressure effects of tension pneumothorax."
    ],
    "preload": [
        "Preload",
        "The heart's filling and stretch before a contraction. ACME estimates its contribution from circulating volume and applies an additional penalty during positive pressure ventilation when volume is low."
    ],
    "prone": [
        "Prone",
        "Lying face down."
    ],
    "prophylaxis": [
        "Prophylaxis",
        "Treatment intended to prevent a problem."
    ],
    "propofol": [
        "Propofol",
        "A sedative that reduces awareness. The mod also models effects on breathing and blood pressure."
    ],
    "pulsatile": [
        "Pulsatile",
        "Changing in pulses with each heartbeat."
    ],
    "pulse-pressure": [
        "Pulse pressure",
        "The difference between systolic and diastolic pressure. For 120/80, pulse pressure is 40 mmHg."
    ],
    "pupillary": [
        "Pupillary",
        "Related to the pupils, the openings in the eyes that change size in response to light."
    ],
    "qrs": [
        "QRS complex",
        "The main spike on an ECG. It represents electrical activation of the lower pumping chambers."
    ],
    "receptor": [
        "Receptor",
        "A target on or inside a cell that responds to a chemical signal or medication."
    ],
    "reperfusion": [
        "Reperfusion",
        "Restoring blood flow to tissue that previously received too little."
    ],
    "respiratory-depression": [
        "Respiratory depression",
        "Breathing that becomes slower or less effective, sometimes because of medication."
    ],
    "respiratory-drive": [
        "Respiratory drive",
        "The body's signal to take breaths. Sedatives, opioids and injury can change it."
    ],
    "respiratory-rate": [
        "Respiratory rate",
        "The number of breaths taken or delivered in one minute."
    ],
    "rocuronium": [
        "Rocuronium",
        "A medication that blocks muscle movement, including breathing. It provides neither pain relief nor unconsciousness."
    ],
    "rr-interval": [
        "R-R interval",
        "The time between successive main ECG spikes. A shorter interval means a faster electrical rate."
    ],
    "scleral-icterus": [
        "Scleral icterus",
        "Yellow discoloration of the whites of the eyes."
    ],
    "semi-fowlers": [
        "Semi-Fowler's position",
        "Lying with the head and upper body partly raised."
    ],
    "sepsis": [
        "Sepsis",
        "A harmful body wide response to infection that can impair organ function."
    ],
    "serum-level": [
        "Serum level",
        "The concentration of a substance in the liquid portion of blood. The wiki's medication graphs show a relative game effect envelope, not a measured blood concentration."
    ],
    "sinus-rhythm": [
        "Sinus rhythm",
        "A rhythm started by the heart's normal pacemaker. It can still be too fast or too slow for the patient's condition."
    ],
    "stroke-volume": [
        "Stroke volume",
        "The amount of blood pushed out by a lower heart chamber with each effective beat. The game uses simplified filling based estimates in its pressure and oxygen delivery calculations."
    ],
    "sugammadex": [
        "Sugammadex",
        "A medication that binds available rocuronium and reduces its paralytic effect. In the mod, reversal depends on the amounts and active effects of both drugs."
    ],
    "supine": [
        "Supine",
        "Lying flat on the back, face up."
    ],
    "svt": [
        "Supraventricular tachycardia (SVT)",
        "A fast rhythm that starts above the lower pumping chambers of the heart. In this guide, SVT means the mod's specific regular fast rhythm."
    ],
    "sync": [
        "SYNC",
        "Synchronization mode: times a shock to a detected heartbeat. The game uses it for cardioversion of suitable organized fast rhythms."
    ],
    "systemic": [
        "Systemic",
        "Affecting the body through the circulation, rather than only the place where treatment was applied."
    ],
    "systole": [
        "Systole",
        "The part of the heartbeat when the heart contracts and pushes blood out."
    ],
    "systolic": [
        "Systolic pressure",
        "The upper number in a blood pressure reading, measured during the pumping part of the heartbeat."
    ],
    "t-wave": [
        "T wave",
        "The ECG wave showing the lower heart chambers resetting electrically after a beat."
    ],
    "tachyarrhythmia": [
        "Tachyarrhythmia",
        "An abnormal heart rhythm that is fast."
    ],
    "tachypnea": [
        "Tachypnea",
        "Fast breathing."
    ],
    "tbi": [
        "TBI",
        "Traumatic brain injury: damage to the brain caused by trauma."
    ],
    "tccc": [
        "TCCC",
        "Tactical Combat Casualty Care: a framework for treating casualties in a tactical setting."
    ],
    "tfc": [
        "TFC",
        "Tactical field care: casualty treatment during the tactical phase after immediate fire related danger is addressed."
    ],
    "thoracostomy": [
        "Thoracostomy",
        "An opening through the chest wall into the space around the lung, used to release trapped air or fluid."
    ],
    "toxicity": [
        "Toxicity",
        "Harmful effects caused by a substance or medication."
    ],
    "tranexamic-acid": [
        "Tranexamic acid (TXA)",
        "A medication that reduces clot breakdown. It supports bleeding treatment but does not close a wound or replace lost blood."
    ],
    "trendelenburg": [
        "Trendelenburg",
        "A position with the head lower than the legs."
    ],
    "turbulent": [
        "Turbulent flow",
        "Flow with irregular mixing and swirls. It does not follow the simple laminar flow relationship."
    ],
    "unilateral": [
        "Unilateral",
        "Present on one side of the body."
    ],
    "venous-return": [
        "Venous return",
        "Blood flowing back to the heart through the veins."
    ],
    "ventricle": [
        "Ventricle",
        "One of the heart's two lower pumping chambers. The right sends blood to the lungs; the left sends it to the body."
    ],
    "vf": [
        "Ventricular fibrillation (VF)",
        "Chaotic electrical activity in the lower heart chambers that prevents effective pumping. This is a shockable cardiac arrest rhythm in the game."
    ],
    "viscosity": [
        "Viscosity",
        "How strongly a fluid resists flowing. A more viscous fluid needs more pressure to move through the same tube."
    ],
    "vt": [
        "Ventricular tachycardia (VT)",
        "A fast rhythm starting in the heart's lower pumping chambers. A patient may have a pulse or may be in cardiac arrest, so check directly."
    ],
    "acidosis": [
        "Acidosis",
        "An increase in body acidity, which can develop with poor circulation or carbon dioxide retention. In the mod, worsening acidosis increases bleeding and reduces pressure support effects."
    ],
    "adenosine": [
        "Adenosine",
        "A medication that briefly slows electrical conduction through the AV node. The mod uses a rapid delivered dose to attempt conversion of its SVT rhythm; it does not deliberately create asystole."
    ],
    "antifibrinolytic": [
        "Antifibrinolytic",
        "A medication that slows the breakdown of existing blood clots."
    ],
    "barotrauma": [
        "Barotrauma",
        "Tissue damage caused by a pressure difference, including injury to the lungs during excessive pressure."
    ],
    "beta-1": [
        "Beta 1 receptor",
        "A target for chemical signals that can increase heart rate and contraction strength."
    ],
    "alpha-1": [
        "Alpha 1 receptor",
        "A target for chemical signals that can narrow blood vessels and increase resistance."
    ],
    "boyles-law": [
        "Boyle's Law",
        "For a fixed amount of gas at constant temperature, lower surrounding pressure permits a larger gas volume. Body structures and leaks can limit how trapped gas actually expands."
    ],
    "catecholamine": [
        "Catecholamine",
        "A group of chemical messengers that includes epinephrine and norepinephrine. Their effects on the heart and blood vessels depend on the substance and dose."
    ],
    "chelate": [
        "Chelate",
        "To bind a substance chemically so less of it remains freely available."
    ],
    "citrate": [
        "Citrate",
        "A chemical used in stored blood to prevent clotting by binding calcium. Large transfusions can reduce the recipient's available calcium."
    ],
    "coagulopathy": [
        "Coagulopathy",
        "Impaired blood clotting. It can make bleeding harder to control."
    ],
    "crystalloid": [
        "Crystalloid",
        "A fluid containing dissolved small substances, such as salts. Saline and PlasmaLyte are examples; they add fluid without adding red blood cells."
    ],
    "etco2": [
        "EtCO2",
        "Carbon dioxide measured at the end of an exhaled breath. It is influenced by breathing, circulation and measurement conditions."
    ],
    "frank-starling": [
        "Frank Starling",
        "The relationship between heart filling and the force of contraction, within limits. The mod uses a simplified volume based relationship to estimate stroke volume."
    ],
    "herniation": [
        "Herniation",
        "Brain tissue displaced by pressure inside the skull. It is a severe complication of swelling or bleeding."
    ],
    "hyperkalaemia": [
        "Hyperkalaemia",
        "An elevated potassium level in the blood. Large changes can disrupt the heart's electrical activity."
    ],
    "hypocalcaemia": [
        "Hypocalcaemia",
        "A low level of available calcium. Calcium is needed for clotting, muscle contraction and other cell functions."
    ],
    "icp": [
        "ICP",
        "Intracranial pressure: pressure inside the skull. Swelling or bleeding can raise it and reduce blood flow to the brain."
    ],
    "ionised-calcium": [
        "Ionised calcium",
        "The freely available form of calcium in blood, used in processes including clotting and muscle contraction."
    ],
    "lethal-triad": [
        "Lethal triad",
        "Hypothermia, acidosis and impaired clotting occurring together in severe injury. The mod also tracks calcium deficit as a contributor to worsening bleeding and circulation."
    ],
    "mu-opioid": [
        "Mu opioid receptor",
        "A cell target through which opioid medications produce effects including pain relief, sedation and reduced breathing."
    ],
    "myocardial-depression": [
        "Myocardial depression",
        "Reduced strength of heart muscle contraction."
    ],
    "nmda": [
        "NMDA antagonist",
        "A substance that blocks a brain receptor involved in pain and awareness. Ketamine acts through this pathway; breathing can still be impaired, particularly with other medications."
    ],
    "nmj": [
        "Neuromuscular junction",
        "The connection where a motor nerve signals a muscle to contract. Blocking this signal can stop movement without reducing awareness."
    ],
    "peep": [
        "PEEP",
        "Positive end expiratory pressure: pressure maintained in the lungs between breaths. It can help keep air sacs open but can also reduce blood returning to the heart."
    ],
    "pneumothorax": [
        "Pneumothorax",
        "Air in the space between the lung and chest wall, which reduces lung expansion. Its effect depends on the amount of air and whether pressure is building."
    ],
    "ppv": [
        "PPV",
        "Positive pressure ventilation: delivering breaths by pushing air into the lungs. In the mod, active support adds a filling penalty when circulating volume is low."
    ],
    "refractory-period": [
        "Refractory period",
        "The brief time after electrical activation when heart cells cannot activate again normally."
    ],
    "sedation": [
        "Sedation",
        "Medication induced reduction in alertness, ranging from drowsiness to unconsciousness. Pain relief and paralysis are separate effects."
    ],
    "spo2": [
        "SpO2",
        "An estimate of the percentage of hemoglobin carrying oxygen. It does not measure the amount of hemoglobin present or the blood flow reaching tissues."
    ],
    "sympathetic-outflow": [
        "Sympathetic outflow",
        "Nerve signals that help the body respond to stress, including changes in heart rate and blood vessel tone."
    ],
    "tachyphylaxis": [
        "Tachyphylaxis",
        "A decreasing response to repeated doses over a short period. The same dose can produce less effect."
    ],
    "therapeutic-window": [
        "Therapeutic window",
        "The range between a useful medication exposure and one likely to cause harmful effects."
    ],
    "titrate": [
        "Titrate",
        "Adjust a medication dose or delivery rate in steps while reassessing its effect."
    ],
    "cardiac-output": [
        "Cardiac output",
        "The amount of blood pumped over time. It depends on heart rate and the amount ejected with each effective beat."
    ]
})

TERMS.update({'nystagmus': ['Nystagmus', "Rapid involuntary eye movements. In ACM Extended, pupil assessment can add this finding during ketamine dominant deep sedation under specific conditions."], 'overpressure': ['Overpressure', 'Pressure above the surrounding air pressure during a blast. The mod estimates it from charge, distance and nearby geometry.'], 'impulse': ['Blast impulse', 'Pressure accumulated over the brief duration of a blast wave. The mod records an estimate; its main injury gates use effective peak pressure.'], 'tympanic': ['Tympanic injury', "Injury involving the eardrum. The mod records this at a configured blast pressure threshold."], 'anisocoria': ['Anisocoria', "Pupils of unequal size. In the mod, an asymmetric brain injury pupil state can produce this finding."], 'refractory': ['Refractory', 'Resistant to improvement, or temporarily less responsive to a new trigger, depending on context.'], 'dyssynchrony': ['Dyssynchrony', 'A mismatch between the patient’s breathing effort and the breaths delivered by the ventilator.'], 'compliance': ['Compliance', 'How easily a lung expands. Lower compliance means less volume moves for the same pressure.'], 'perrl': ['PERRL', 'Pupils equal, round and reactive to light.'], 'obtundation': ['Obtundation', 'Reduced alertness while still awake. The game can apply visual, hearing and speech effects while the player retains movement.']})

# Visual reference terms added with the waveform and volume guides.
TERMS.update({
    "vti": ("Inspired tidal volume (VTi)", "The volume of gas delivered into the airway during one breath. On the ventilator, compare it with the expired volume, VTe, to see whether delivered gas is returning."),
    "vte": ("Expired tidal volume (VTe)", "The volume of gas measured coming back out during one breath. A leak can make this lower than VTi even when the ventilator's set volume looks adequate."),
    "capnography": ("Capnography", "A continuous graph of carbon dioxide in breathing gas over time. Its height, baseline and shape help you assess exhalation, airflow and the measurement connection."),
    "capnogram": ("Capnogram", "The waveform drawn by a capnograph. It rises as carbon dioxide rich gas is exhaled and normally falls toward zero during inspiration."),
    "curare-cleft": ("Curare cleft", "A notch in the exhaled carbon dioxide plateau. In ACM Extended, the cleft shape is linked to spontaneous effort while the ventilator is connected; read it with the patient's breathing and support settings."),
    "breachers-syndrome": ("Breacher’s syndrome", "A term used for symptoms reported after repeated low level blast exposure, including headache, poor concentration, dizziness and sleep disturbance. It is not a single diagnostic test or a separate named disease state in the mod.")
})

# TBI recovery and controller terminology, verified against B119 / 98d18bb.
TERMS.update({
    "tbi": ("TBI", "Traumatic brain injury: injury to the brain caused by trauma. ACM Extended separates lasting structural severity from active acute burden, which can improve when pressure, oxygen delivery and ventilation are adequate."),
    "acute-severity": ("Acute severity", "The currently active TBI burden, stored as severity in the game state. It can resolve toward zero under suitable conditions, unless past herniation imposes a recovery floor; it is separate from the lasting injury record."),
    "structural-severity": ("Structural severity", "The lasting record of brain injury severity, used to set remaining reserve and pressure requirements. It can stay elevated after acute symptoms resolve, without itself continuing to produce raised ICP or unconsciousness."),
    "cerebral-autoregulation": ("Cerebral autoregulation", "The brain’s ability to adjust its vessels as blood pressure changes. Severe structural TBI reduces this reserve, making low pressure more damaging and excessive pressure more likely to add to ICP."),
    "autonomic-integrity": ("Autonomic integrity", "How much of the brain’s automatic control of systemic blood vessel tone remains functional. In the mod it changes over time, separately from cerebral autoregulation, and also limits the compensatory ability of junctional vessels."),
    "autonomic-tone": ("Autonomic tone", "The TBI controller’s signed influence on systemic blood vessels, from −1 to +1. Positive favours tightening, zero is neutral, and negative favours widening; the value is an influence on resistance, not a blood pressure measurement."),
    "autonomic-decompensation": ("Autonomic decompensation", "Failure of the brain’s automatic vascular control as reserve is exhausted or herniation progresses. In the game, tone can become unstable before late failure favours vessel widening and falling resistance."),
    "pressure-passive": ("Pressure passive", "A state in which cerebral blood flow and pressure follow systemic pressure more directly because local regulation is impaired. In severe TBI, more CPP is therefore not always protective: excessive pressure can add to ICP."),
    "icp": ("ICP", "Intracranial pressure: pressure inside the skull. In ACM Extended it returns toward a normal baseline, usually 10 mmHg, as acute TBI resolves; recovery does not mean a target ICP of zero."),
    "cpp": ("CPP", "Cerebral perfusion pressure: effective pressure reaching the brain minus ICP. The game’s TBI recovery gate adds CPP minima of 55 mmHg for severe structural injury and 60 for critical injury; mild and moderate injury do not receive that added high CPP requirement."),
    "cushing-response": ("Cushing response", "A raised ICP response that can support blood pressure while slowing the pulse and disturbing breathing. In ACM Extended, exhausted autonomic control can affect vascular resistance before the full vital sign pattern appears, and late failure can replace the initial pressure rise with collapse."),
    "map": ("MAP", "Mean arterial pressure: the average pressure in the arteries across a heartbeat. The game uses it in organ perfusion, but adequate MAP alone does not prove adequate oxygen delivery; TBI recovery requirements also depend on structural injury and ICP."),
    "secondary-insult": ("Secondary insult", "An additional burden on the injured brain after the original trauma, such as inadequate oxygen delivery, poor perfusion or retained carbon dioxide. Preventing these insults allows the game’s acute TBI burden to recover when its other gates are met."),
    "herniation": ("Herniation", "Brain tissue displaced by pressure inside the skull. The game tracks current and maximum stages; past progression can impose an acute recovery floor even after pressure improves."),
    "permissive-hypotension": ("Permissive hypotension", "Accepting a lower pressure while hemorrhage is uncontrolled to reduce pressure driven loss. In the game, this must be weighed against oxygen delivery and severity specific brain perfusion requirements, particularly the reduced reserve of severe or critical TBI.")
})
