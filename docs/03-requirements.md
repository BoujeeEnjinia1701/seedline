---
doc_id: SDL-PRS-001
title: SeedLine product requirements and specifications
project: SeedLine
doc_type: Product requirements and specifications
version: "0.8"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2, with concept status against each
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply SDL-DDR-001 (R3 kept with skip-cell plates, R5 redefined for pelleted small seed, R6 materials, R13 marker arm, R18 bolted frame); status from SDL-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Status from SDL-CAL-001 v0.3 on the constructable design (SDL-DDR-003); R16 and R17 reported against value-engineering targets
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R17: USD 219.50 accepted for the prototype (SDL-DDR-003 A3, 2026-10-02); no status changed"
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Figures from SDL-CAL-001 v0.5 after the decisions of 2026-10-02 (13 mm slot with liners, UV-stabilized door): R11, R16 and R17 values updated; no status changed"
- version: "0.8"
  date: '2026-10-24'
  author: Amish Chadha
  change: "Kit 1.8 and 1.9.1 upgrade: migrated from SDL-REQ-001 to SDL-PRS-001 (PR-001 to PR-018, old R numbers in 'Was'), traced to SDL-URS-001, tolerance and units added; R11 figures from SDL-CAL-001 v0.6 (fasteners weighed from the detailed model, mass fix F6)"
---

# SeedLine product requirements and specifications

What the design must do, each requirement traced to a user need in SDL-URS-001. Version 0.8 migrates the requirements of SDL-REQ-001 to this format without changing any target: each R number becomes a PR with the same target, verification and status, and the old number stays in the "Was" column. The targets are still proposals checked on paper at TRL 3 in SDL-CAL-001; none has been validated with users, and they will be revised after co-design sessions (SDL-PRB-001). Statuses follow SDL-CAL-001 v0.6. The traceability matrix is generated in SDL-RTM-001. Method: STANDARDS section 22.

The **design case** is maize at 250 mm in-row spacing on 0.75 m rows, sown 50 mm deep in a tilled loam seedbed at a walking speed of 2.9 km/h (about 0.81 m/s). **Walking-speed rule** (SDL-DDR-002 item 5): walk at about 2.9 km/h or slower with the 0.8 and 1.0 ratios, and about 2.4 km/h or slower with the 1.2 ratio, so the cells stay within the assumed 0.30 m/s fill limit. The **small-seed case** is pelleted carrot or lettuce seed (about 3.3 mm pellets) at 25 to 50 mm spacing on a prepared vegetable bed; vegetable plates are the second plate set.

Table 1. Product requirements and specifications.

| ID | Traces to | Category | Title | Requirement | Target | Tolerance | Units | Verification | Status | Was |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PR-001 | UR-001 | Performance | Single-seed placement | In the design case the seeder shall leave misses and multiples of 5 % or less of cells each, in the terms of ISO 7256-1 | 5 | max, each | % of cells | Analysis, cell speed against the fill limit (CAL section 3), TRL 3; sticky-belt bench test, TRL 4 | At risk: cell speed 0.299 m/s at the 2.9 km/h rule against an assumed 0.30 m/s limit, no margin; misses and multiples cannot be calculated | R1 |
| PR-002 | UR-002 | Performance | Spacing uniformity | The coefficient of variation of in-row spacing shall be 30 % or less in the design case | 30 | max | % | Analysis, Monte Carlo (CAL section 10), TRL 3; field count, TRL 5 | At risk: 31 % of all spacings with the assumed miss and double rates; 9 % for single spacings | R2 |
| PR-003 | UR-003 | Performance | Spacing range | In-row spacing shall be settable from 25 to 400 mm by plate cell count (skip-cell plates of one or two cells included) and, where needed, one sprocket change from the optional ratio kit | 25 to 400 | each target within 15 % | mm | Analysis, spacing formula (CAL section 2), TRL 3 | Met on paper with the ratio kit: 22 to 589 mm nominal, every target within 11.1 %; the base seeder (15 T only) covers 26 to 471 mm, within 17.3 % | R3 |
| PR-004 | UR-004 | Performance | Spacing follows travel | Seed spacing shall be set by distance travelled, not speed, with wheel slip of 8 % or less | 8 | max | % slip | Analysis, traction estimate (CAL section 6a), TRL 3; field test, TRL 5 | Met on paper: skid 1.2 to 1.7 %; rolling radius uncertain by up to 6.7 %, so calibrate per seedbed | R4 |
| PR-005 | UR-003, UR-005 | Performance | Seed size range | Plates of one diameter shall meter raw seed from 3.5 to 15 mm in its largest dimension; seed under 2 mm shall be sown pelleted | 3.5 to 15 | cell rule 1.15 L + 0.5 by 1.05 W + 0.3 | mm | Analysis, cell tolerance rule (CAL section 4), TRL 3; bench test, TRL 4 | Met on paper: 3.5 to 15 mm raw seed; pelleted carrot fits; raw 1 to 2 mm seed does not | R5 |
| PR-006 | UR-005 | Materials | Printable plates | Each plate shall print in 2 h or less on a 180 x 180 mm bed with no supports, in PETG (default) or ASA (strong sun), PLA for trials only, with cell size within the tolerance | 2 | cell size +/-0.2 mm | h | Analysis, print estimate (CAL section 4), TRL 3; measurement, TRL 4 | Met on paper: 1.39 h (maize) to 1.87 h (groundnut) at 20 % infill (SDL-DEC-001 F8), small margin for thick plates; accuracy to verify at TRL 4 | R6 |
| PR-007 | UR-005 | Usability | Crop change | A plate shall be swapped by hand with no tools, without emptying more than the seed in the housing | 2 | max | min | Inspection of the model, TRL 3; timed trial, TRL 4 | To verify at TRL 4: side door and hand knob in the model; one 13 mm slot takes the 6, 8 and 10 mm plates with a printed liner pair | R7 |
| PR-008 | UR-006 | Performance | Sowing depth | Depth shall be adjustable from 10 to 60 mm in 10 mm steps and held on a ploughed field-crop seedbed (rough, hand-tilled seedbeds to be reviewed with partner data) | 10 to 60 | +/-10 | mm | Analysis, depth geometry (CAL section 9), TRL 3; field check, TRL 5 | Met on paper: +/-10 mm holds for drive-wheel bumps within about +/-15 mm, taken as the ploughed-seedbed condition | R8 |
| PR-009 | UR-007 | Performance | Work rate | Field capacity shall be 0.1 ha/h or more in the design case, including turns and refills | 0.1 | min | ha/h | Analysis, field capacity (CAL section 8), TRL 3 | Met on paper: 0.142 ha/h (7.1 h/ha) at 2.9 km/h | R9 |
| PR-010 | UR-008 | Usability | Push effort | The horizontal push force shall be 150 N or less in the design case | 150 | max | N | Analysis, planar statics with a soil model (CAL section 6), TRL 3; spring-scale test, TRL 4 | At risk: 132 N horizontal pushing along the handle (206 N along it) in the design case; 179 N at best on a heavy, loose seedbed | R10 |
| PR-011 | UR-009 | Physical architecture | Handling | Mass with the marker kit shall be 15 kg or less; grip height adjustable from 850 to 1,050 mm; one person lifts and turns it at a row end | 15 | max | kg | Analysis, mass build-up (CAL section 5), TRL 3; weighing, TRL 4 | Met on paper: 14.2 kg base, 14.8 kg with the marker kit (0.18 kg margin), with every fastener weighed from the detailed model and the mass fix of SDL-DEC-001 F6 | R11 |
| PR-012 | UR-010, UR-017 | Usability | Hopper | The hopper shall hold 2 L or more, fill from a jug without spilling and empty in 1 min or less when changing crops | 2 | min | L | Inspection, model volume (CAL section 8), TRL 3; timed trial, TRL 4 | Met on paper: 2.42 L | R12 |
| PR-013 | UR-011 | Usability | Row-spacing kit | A telescoping marker arm (decided, SDL-DDR-001 item 3) shall mark the next row at 200 to 900 mm from the current row | 200 to 900 | +/-25 | mm | Inspection of the model, TRL 3 | Met by design | R13 |
| PR-014 | UR-012 | Safety | Guarding | Chain and sprocket nip points shall be covered on the side facing the operator's hands and feet, with no exposed sharp edges above the opener | covered | none exposed | n/a | Inspection of the model, TRL 3 | Met by design: printed shroud with an outboard face plate over both sprockets, the chain and the tensioner's full travel | R14 |
| PR-015 | UR-013 | Environment and durability | Durability | Frame, drive and opener shall last 5 seasons of about 2 ha each with only chain, brush and plate replacement; plates shall last 1 season or more | 5 | min | seasons | Analysis, stress checks (CAL section 7), TRL 3; wear test, TRL 4 | To verify at TRL 4: stresses are low, wear life unknown | R15 |
| PR-016 | UR-014 | Physical architecture | Prototype cost | Prototype parts shall be reported against the USD 400 value-engineering target (`budget_usd`) | 400 | value-engineering target | USD | Analysis, priced BOM (`bom/bom.csv`), TRL 3 | Met on paper: USD 266.10 estimated, USD 133.90 under the target | R16 |
| PR-017 | UR-015 | Physical architecture | Replication cost | The base seeder (all items except the row marker kit and the optional ratio kit) shall cost about USD 200 in parts, a value-engineering target | 200 | value-engineering target | USD | Analysis, priced BOM, TRL 3 | Over target: USD 224.10 estimated, USD 24.10 over; USD 219.50 accepted for the prototype on 2026-10-02 (SDL-DDR-003 A3), and the plate liners and UV-stabilized door added USD 4.60 after it | R17 |
| PR-018 | UR-016 | Materials | Local build | Frame, handle and opener shall be made from common steel sections with a drill and bolts (default, SDL-DDR-001 item 8) or a welder; the drive from standard #35 roller chain or bicycle parts | common parts | n/a | n/a | Inspection of the model and build plan, TRL 3 | Met by design | R18 |

Categories: physical architecture, performance, materials, usability, packaging and transport, safety, electrical, software. Status: met on paper, met by design, at risk, not met, over target, withdrawn, to verify at TRL 4.

## Requirements not met or at risk

No requirement is not met on paper. Three are at risk and one cost requirement is over its value-engineering target:

- **PR-001 at risk:** under the walking-speed rule (2.9 km/h) the maize cells move at 0.299 m/s, at the assumed 0.30 m/s fill limit with no margin, and the limit itself needs a bench test. Plate size is revisited only with bench data (SDL-DDR-002 item 5).
- **PR-002 at risk:** the all-spacings coefficient of variation depends on miss and double rates that need a bench test.
- **PR-010 at risk:** the design case is inside 150 N with a 12 % margin on assumed soil values; a heavy, loose seedbed needs about 179 N. Whether one operator sustains the design-case push for a planting day is not yet assessed (SDL-STM-001 row S9).
- **PR-011 met with a small margin:** the kit 1.9 model weighs every bolt, nut, washer and pin, which added about 0.6 kg to the 0.58 kg fastener estimate of SDL-CAL-001 v0.5 and took the seeder with the marker kit to 15.5 kg. Under Amish's standing instruction of 2026-10-23 the mass was brought back under 15 kg (SDL-DEC-001 F6: 3 mm drop plates and bearing plate, 20 x 2 mm hopper uprights, an aluminium marker arm and a 1.5 mm marker disc): 14.8 kg with 0.18 kg of margin.
- **PR-017 over its value-engineering target:** base parts USD 224.10 against about USD 200, USD 24.10 over. Savings worth trying are in the design decisions register (SDL-DEC-001).
- **PR-008 restated:** met on paper for ploughed field-crop seedbeds; the rigid opener follows the wheels, so clods under the drive wheel on rough, hand-tilled seedbeds will change the depth.

## Assumptions

All assumptions are listed in SDL-CAL-001 section 1. The main ones are a 300 mm drive wheel over the lug tips (942.5 mm travel per turn), a 0.30 m/s cell fill limit, a Brixius rolling resistance model with cone indexes of 100 to 300 kPa, and the TRL 2 miss and double rates of 5 % and 4 %.
