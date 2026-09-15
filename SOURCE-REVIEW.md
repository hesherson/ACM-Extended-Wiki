# Article source revision inventory

Inventory date: 15 September 2026. This accompanies the reading layout update; the website version remains 1.2.1.

This is an inventory of the ACM Extended commit links already present in the 28 built articles, not a fresh validation of the mod. Article text, dose data, equations, existing links and source pins are unchanged in this update. Source notes are now optional disclosures; the IV slideshow instructions remain beside its controls.

## What still needs source review

The articles cite different snapshots. A page can intentionally use several revisions for different features or original asset provenance. Do not replace those pins with one newer commit without reviewing the corresponding code. The linked revision describes the stated section review, not necessarily every section on that page.

The saved website identifies dev revision `bc90fc7661fa6612cef5f4382f3b181fd5868f11` for Hardcore medication behavior and dev revision `98d18bb3f60dc9be8cdaf4a43419bb57483c3a3f` for B119 TBI and the infusion/mixture models. Those are historical review statements from the package; this update does not establish the current main or dev branch head.

A current ACM Extended repository read was unavailable in this session. The supplied ACM, ACE3 and Animate source archives do not establish the current ACM Extended fork revision. A future content audit should retrieve the actual current fork and compare each reviewed subsystem before changing any in-game value.

Recommended review order:

1. Medication cards and general access/flow reference: compare their earlier reviews with the later Hardcore delivery paths, keeping bolus timing separate from concentration accumulation.
2. Ventilator and airway: reconcile the individual delivery, waveform, suction and chest recovery pins with the selected target branch.
3. TBI, hemorrhage and oxygen: confirm whether the documented B119 dev behavior has reached the chosen release branch.
4. Overview and printable pages: update these alongside their full articles whenever a source-backed rule changes.

## Pins found in article links

10 distinct commit pins appear across 22 pages. Asset and behavioral review links are both counted.

| Commit | Pages containing a link to it |
| --- | --- |
| [21f8694](https://github.com/hesherson/ACM-Extended/commit/21f86948b8a03507146297742ea84983987d5be1) | [IV access & infusions](docs/access.html), [Airway and chest](docs/airway.html), [Blast overpressure](docs/blast.html), [Debug menu reference](docs/debug.html), [Oxygen delivery](docs/oxygen.html), [Ventilator Settings & Tips](docs/ventilator.html), [Zeus Modules](docs/zeus.html) |
| [302b811](https://github.com/hesherson/ACM-Extended/commit/302b811ba90b4e2347b5614b8c74fb41b5442245) | [Bleeding and shock](docs/bleeding.html), [Oxygen delivery](docs/oxygen.html) |
| [4848f63](https://github.com/hesherson/ACM-Extended/commit/4848f63b200a45362eb576dcef469484202b6a80) | [Accessibility](docs/accessibility.html), [Airway and chest](docs/airway.html), [Blast overpressure](docs/blast.html), [ACM Extended Wiki](docs/index.html), [Obtunded states](docs/obtunded.html), [Traumatic brain injury](docs/tbi.html), [Ventilator Settings & Tips](docs/ventilator.html) |
| [488a5e5](https://github.com/hesherson/ACM-Extended/commit/488a5e54efd10e5289245bcb2f7db7a40bbabcb0) | [Ventilator Settings & Tips](docs/ventilator.html) |
| [5bce47c](https://github.com/hesherson/ACM-Extended/commit/5bce47c26e70924ec5832eac792b19988e86e22c) | [IV access & infusions](docs/access.html), [Clinical descriptors](docs/descriptors.html), [Fluids & blood volume](docs/fluids.html), [ACM Extended Wiki](docs/index.html), [Flow calculation reference](docs/ov_access.html) |
| [98d18bb](https://github.com/hesherson/ACM-Extended/commit/98d18bb3f60dc9be8cdaf4a43419bb57483c3a3f) | [IV access & infusions](docs/access.html), [Blast overpressure](docs/blast.html), [Bleeding and shock](docs/bleeding.html), [Debug menu reference](docs/debug.html), [ACM Extended Wiki](docs/index.html), [Obtunded states](docs/obtunded.html), [Head injury assessment](docs/ov_tbi.html), [Oxygen delivery](docs/oxygen.html), [Printable quick reference](docs/quick-reference.html), [Traumatic brain injury](docs/tbi.html), [Ventilator Settings & Tips](docs/ventilator.html), [Zeus Modules](docs/zeus.html) |
| [abf6253](https://github.com/hesherson/ACM-Extended/commit/abf6253d4876b4a7a5563f84a3b060de53a0290d) | [IV access & infusions](docs/access.html), [Medication reference](docs/medications.html) |
| [bc90fc7](https://github.com/hesherson/ACM-Extended/commit/bc90fc7661fa6612cef5f4382f3b181fd5868f11) | [IV access & infusions](docs/access.html), [ACM Extended Wiki](docs/index.html), [Addon options](docs/settings.html) |
| [dd50edf](https://github.com/hesherson/ACM-Extended/commit/dd50edf34497588d473ffe3c70797f2eaa52f6f8) | [Airway and chest](docs/airway.html), [Cardiac rhythms](docs/circulation.html) |
| [eabd2f2](https://github.com/hesherson/ACM-Extended/commit/eabd2f2e88fba4754d81bda8543b81303a72964d) | [IV access & infusions](docs/access.html), [Bleeding and shock](docs/bleeding.html), [Cardiac rhythms](docs/circulation.html), [Flight Physiology](docs/flight.html), [ACM Extended Wiki](docs/index.html), [Medication reference](docs/medications.html), [Medical menu](docs/menu.html), [Oxygen delivery](docs/oxygen.html) |

## Pages without a direct commit link

These pages may draw on other articles, generated definitions or the site review banner; the absence of a direct commit link is an audit gap, not proof that the content is wrong.

- [Glossary](docs/glossary.html)
- [Bleeding and resuscitation](docs/ov_bleeding.html)
- [Breathing support](docs/ov_chest.html)
- [Rhythm treatment reference](docs/ov_circ.html)
- [How systems connect](docs/ov_intro.html)
- [Oxygen readings](docs/ov_oxygen.html)

## Validation for this layout update

- Compared every built article with the preceding website package, excluding the new labels, topic headings and navigation. Original article text, all 899 existing article anchors, links, images, 161 tables and 137 form/button controls were preserved.
- The independent build comparison and HTML structure checks pass on all 28 pages. The structure check rejects wrapper crossings and newly nested source disclosures.
- Search indexes 332 records. Both page navigation surfaces include parent topics and marked subsections; the older subsection anchors remain valid.
- Browser preview was blocked by the available browser security policy. A fresh visual, mobile, clipboard and browser-interaction pass remains outstanding. The seven existing browser suites remain in the GitHub workflow; their heading selectors were adjusted where this hierarchy changed.
- This package has not been pushed or deployed from this session.
