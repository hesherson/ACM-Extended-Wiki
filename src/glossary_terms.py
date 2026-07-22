#!/usr/bin/env python3
"""
GLOSSARY. Every advanced term used anywhere in the guide, defined for someone with no medical background.

Rules for writing these:
  - Assume the reader knows nothing. No term may be defined using another undefined term.
  - Two or three short sentences. If it needs more, it is a page, not a glossary entry.
  - Say what it IS, then why it matters to a medic. Skip etymology and history.
  - Plain words over correct-but-opaque ones. "Squeeze" beats "contractility" in the first sentence.

Used two ways: build.py turns {{term}} in content into a clickable popup, and glossary.html is generated
from this same dict so the two can never disagree.
"""

TERMS = {
 # ---- Circulation ----
 "map": ("MAP", "Mean arterial pressure. The average pressure in the arteries over a whole heartbeat, which is what actually pushes blood into organs. Around 65 is the usual minimum for keeping organs alive."),
 "preload": ("Preload", "How full the heart is when it starts to squeeze. A heart with nothing in it has nothing to pump, so bleeding drops output even if the heart itself is fine."),
 "stroke-volume": ("Stroke volume", "How much blood the heart pushes out with one beat. Multiply it by heart rate and you get cardiac output, the total flow around the body."),
 "cardiac-output": ("Cardiac output", "The total amount of blood moved per minute. It is heart rate times how much each beat pushes out, and almost everything in shock comes back to it."),
 "frank-starling": ("Frank-Starling", "The rule that a fuller heart squeezes harder, up to a point. It matters because losing volume costs you output faster than you would expect, rather than in a straight line."),
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
 "apnea": ("Apnea", "Not breathing. In a sedated or paralysed casualty this is expected and you breathe for them, and in anyone else it is an emergency."),
 "etco2": ("EtCO2", "The carbon dioxide measured in exhaled breath. It tells you both that the lungs are working and that blood is actually circulating, which is why it drops during cardiac arrest."),
 "hypoventilation": ("Hypoventilation", "Breathing too little, so carbon dioxide builds up. Slow, shallow, or not often enough, and the casualty becomes acidic."),
 "pneumothorax": ("Pneumothorax", "Air trapped in the chest outside the lung, pressing on it. A simple one is uncomfortable, and a tension one squeezes the heart and kills quickly."),
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
 "dissociation-curve": ("Dissociation curve", "The S-shaped relationship between oxygen pressure and how loaded the blood is. Its shape means a healthy person can lose a lot of pressure safely and a sick one cannot."),
 "acidosis": ("Acidosis", "Blood becoming too acidic, from poor circulation or from carbon dioxide building up. It stops blood clotting and stops pressor drugs working."),
 "colloid": ("Colloid", "A fluid with large molecules that stay inside blood vessels rather than leaking out. It holds volume better than salt water does."),
 "crystalloid": ("Crystalloid", "Plain salt-based fluid such as saline. It fills the tank temporarily but carries no oxygen and leaks out of the circulation over time."),

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
 "sympathomimetic": ("Sympathomimetic", "A drug that mimics the fight-or-flight response. Raises heart rate, blood pressure and alertness."),
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
}
