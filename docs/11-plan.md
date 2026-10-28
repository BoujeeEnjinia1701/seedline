---
doc_id: SDL-PLN-001
title: SeedLine project plan
project: SeedLine
doc_type: Project plan
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade): workstreams, resources, stage gates, next steps and the reference list"
---

# SeedLine project plan

SeedLine is at stage P3 (design outputs, TRL 3) with the kit 1.9.1 pipeline documents and a detailed model of both concept options. The next gate, P4 (verification, TRL 4), is on hold under the portfolio's TRL cap of 3. The decision requested from Amish is the concept choice (SDL-DEC-001: option A, the current design, recommended) and approval of the fixes made under his standing instruction of 2026-10-23 (F1 to F8), which he can reverse. Method: STANDARDS sections 19 and 23.

## Workstreams

Table 1. Workstreams.

| Workstream | Owner (role) | Deliverable | Status |
| --- | --- | --- | --- |
| Concept and requirements | Design lead | PRB, STM, OPT, URS, PRS, RTM | Done at P3 (2026-10-24); concept choice awaiting Amish |
| Calculations | Design lead | SDL-CAL-001 (`docs/04-calcs/sizing.py`), STEM check script | Done at P3; R1, R2 and R10 at risk; push endurance to assess |
| CAD and drawings | Design lead | `cad/src/model.py` at D3 for options A and B, STEP, SDL-DWG-001 and making sketches SDL-DWG-101 to 124 | Done at P3 (`cad/fidelity.json`) |
| Build plan and decisions | Design lead | SDL-BLD-001, SDL-DEC-001 | Done at P3 |
| Regulatory, risk and market | Design lead | SDL-REG-001, SDL-RSK-001, SDL-MKT-001 | First issue; items "to assess" listed |
| Co-design partner | Project lead (Amish) | Partner agreement, co-design sessions, soil data | Not started; first candidate named (SDL-DEC-001) |
| Bench and field tests | Test lead | TST documents: metering bench test, push test, fatigue test | On hold (P4, TRL cap 3) |
| Renders and storefront | Coordinator | `media/options.png`, photoreal renders, cards | Scenes exported; rendered on Amish's Mac |

## Resources needed

Table 2. Resources (costs are the BOM estimates where a BOM line exists; others to assess).

| Resource | Deliverable | Effort | Estimated cost (USD) |
| --- | --- | --- | --- |
| Prototype parts (P4) | One prototype with both kits | Purchasing and printing | 266.10 (BOM estimate) |
| Workshop time (P4) | Frame, opener, handle and marker made to SDL-BLD-001 | About 1.5 h of cutting and drilling (in BOM line 12) plus assembly, about 1 to 2 days | In BOM line 12; assembly to assess |
| Desktop FDM printer time (P4) | Plates, hopper, housing, guard, liners, knob | About 1.5 to 2 h per plate; hopper, housing and guard to assess | Printer time not costed |
| Bench test rig (P4) | Sticky-belt metering test to ISO 7256-1 terms | To assess | To assess |
| Partner field trial (P5) | Field counts, push and depth on partner soils | To assess with the partner | To assess |
| Regulatory review | Items "to assess" in SDL-REG-001 | To assess | To assess |

## Stage gates

Table 3. Stages (P4 to P6 on hold while the stage cap is P3).

| Stage | Gate criteria | Status |
| --- | --- | --- |
| P0 Proposal | PRB, STM, OPT, REG, FEA, PLN | Met (kit 1.8 documents added 2026-10-24) |
| P1 Definition | URS, PRS, RSK, MKT | Met |
| P2 Design inputs | PRS with targets and verification, CAL, RTM, concept selection DDR, STEM check and feasibility closed | Met, except the STEM check: open (rows S6 to S10, S16 and S17 need bench, print, weighing or ergonomic data; option B rows OB4 and OB6 open) and the concept choice awaiting Amish (SDL-DDR-004) |
| P3 Design outputs | Model at D3, STEP, DWG, priced BOM, BLD, DEC, design FMEA, traceability complete | Met (2026-10-24) |
| P4 Verification | Bench tests of metering, push and fatigue; verification report; RSK updated | On hold (TRL cap 3) |
| P5 Validation | Partner field trials, human factors, certification status in REG | On hold |
| P6 Commercialization | Launch plan with a named deployment partner | On hold |

## Next steps and decision requested

1. Amish: decide the concept (SDL-DEC-001 D1; option A recommended, 169 against 131 of 230 weighted points) and review the eight fixes made under the standing instruction (F1 to F8).
2. Coordinator: render `media/options.png` and the product renders from the exported scenes on Amish's Mac.
3. When the TRL cap lifts: metering bench test (PR-001, PR-002), push and endurance assessment (PR-010, ISO 11228-2), plate wear and handle fatigue tests.
4. Approach the first candidate partner and replace the assumed soils, crops and spacings with partner data.

## References

Every source cited in this repository's documents, in Chicago author-date style.

- ASME. n.d. "Jethro Tull." https://www.asme.org/topics-resources/content/jethro-tull.
- Baudron, F., et al. Cited in "Jab Planter" study, CSBE/SCGAB annual meeting paper CSBE101037, 2010. https://library.csbe-scgab.ca/docs/meetings/2010/CSBE101037.pdf.
- Brixius, W. W. 1987. "Traction Prediction Equations for Bias Ply Tires." ASAE Paper 87-1622.
- DoMyOwn. n.d. "Earthway 1001-B Precision Garden Seeder." Accessed October 24, 2026. https://www.domyown.com/earthway-1001b-precision-garden-seeder-p-21609.html.
- European Parliament and Council. 2006. Directive 2006/42/EC on machinery, Article 2. https://www.legislation.gov.uk/eudr/2006/42/article/2/data.htm.
- European Parliament and Council. 2023. Regulation (EU) 2023/1230 on machinery. https://eur-lex.europa.eu/eli/reg/2023/1230.
- FAO. n.d. Jab planter user manual. https://www.fao.org/family-farming/detail/en/c/1619181/.
- FAO. 2018. Country factsheets on small family farms: Ethiopia (https://www.fao.org/3/I8911EN/i8911en.pdf), Tanzania (https://www.fao.org/3/I8356EN/i8356en.pdf) and Guatemala (https://www.fao.org/3/I8357EN/i8357en.pdf).
- FarmHack. 2019. "Hackable 3D Printed Precision Seeder." https://farmhack.org/tools/hackable-3d-printed-precision-seeder.
- Government of India. 2019. *Agriculture Census 2015-16*. https://www.fao.org/fileadmin/templates/ess/ess_test_folder/World_Census_Agriculture/WCA_2020/WCA_2020_new_doc/IND_REP_ENG_2015_2016.pdf.
- Haggblade, Steven, and Gelson Tembo. 2003. *Conservation Farming in Zambia*. IFPRI. https://cgspace.cgiar.org/items/90eae4be-ba6d-448a-8d95-77e7a87ad25c.
- International Committee of the Red Cross. n.d. *Warning: Treated Seeds*. https://www.icrc.org/en/publication/4688-warning-treated-seeds.
- ISO. 1984. ISO 7256-1, *Sowing Equipment, Test Methods, Part 1: Single Seed Drills (Precision Drills)*. https://www.iso.org/standard/13910.html.
- ISO. 2013. ISO 4254-1, *Agricultural Machinery, Safety, Part 1: General Requirements*. Scope via https://www.sis.se/en/produkter/agriculture/agricultural-machines-implements-and-equipment/general/iso425412013/.
- ISO. 2019. ISO 13857, *Safety of Machinery, Safety Distances to Prevent Hazard Zones Being Reached by Upper and Lower Limbs*.
- ISO. ISO 11228-1 and ISO 11228-2, *Ergonomics, Manual Handling*, Parts 1 and 2 (cited by title; texts not consulted).
- Lowder, Sarah K., Jakob Skoet, and Terri Raney. 2016. "The Number, Size, and Distribution of Farms, Smallholder Farms, and Family Farms Worldwide." *World Development* 87: 16 to 29. https://www.sciencedirect.com/science/article/pii/S0305750X15002703.
- Manually operated planter for planting different seeds in small areas. n.d. https://www.academia.edu/77427641/Manually_Operated_Planter_for_Planting_Different_Seeds_in_Small_Areas.
- Molin, J. P., L. L. Bashford, R. D. Grisso, and A. J. Jones. 1998. "Population Rate Changes and Other Evaluation Parameters for a Punch Planter Prototype." *Transactions of the ASAE* 41 (5): 1265 to 1270. https://agris.fao.org/search/en/records/65df271f63b8185d9cab2427.
- Neversink Tools. n.d. "Jang JP-1 Push Seeder." Accessed October 24, 2026. https://neversinktools.com/products/jang-jp-1-push-seeder.
- Nielsen, R. L. (Bob). 2004. "Effect of Plant Spacing Variability on Corn Grain Yield." Purdue University. https://www.agry.purdue.edu/ext/corn/research/psv/update2004.html.
- Our World in Data. n.d. "Smallholder Food Production." https://ourworldindata.org/smallholder-food-production.
- Paperpot Co. n.d. "Jang Seeder vs Earthway." https://paperpot.co/jang-seeder-vs-earthway-josh-sattin/.
- Purdue University Department of Agronomy. 2022. "How Deep Should Corn Be Planted?" https://ag.purdue.edu/news/department/agronomy/kernel-news/2022/12/how-deep-corn-planted.html.
- Science Museum Group. n.d. "1:4 Scale Model of Jethro Tull's Seed Drill" and "Jethro Tull." https://collection.sciencemuseumgroup.org.uk/objects/co39077/1-4-scale-model-of-jethro-tulls-seed-drill.
- 3D Printing Industry. 2019. "Farmer Builds DIY Seed Metering System with 3D Printed Parts." https://3dprintingindustry.com/news/farmer-builds-diy-seed-metering-system-with-3d-printed-parts-161204/.
- University of Minnesota Extension. 2024. "Lower-Cost Equipment for Seeding and Transplanting." https://blog-fruit-vegetable-ipm.extension.umn.edu/2024/11/lower-cost-equipment-for-seeding-and.html.
- Manual punch planter design for smallholder farmers (Lesotho). 2018. *International Journal of Industrial and Systems Design Engineering*. https://www.inderscience.com/filter.php?aid=96730.
