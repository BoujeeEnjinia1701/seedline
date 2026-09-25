---
doc_id: SDL-REQ-001
title: SeedLine requirements
project: SeedLine
doc_type: Requirements
version: "0.3"
status: Draft
date: '2026-09-25'
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
---

# SeedLine requirements

These requirements are proposals checked on paper at TRL 3 in SDL-CAL-001. They are not yet validated with users and will be revised after co-design sessions (see SDL-PRB-001). Version 0.3 applies the decisions Amish made on 2026-09-25 (SDL-DDR-001): the first user group is smallholder field crops, R3 is kept and met with skip-cell plates, and R5 is redefined so that seed under 2 mm is sown pelleted.

The **design case** is maize at 250 mm in-row spacing on 0.75 m rows, sown 50 mm deep in a tilled loam seedbed at a walking speed of 3 km/h (about 0.83 m/s). The **small-seed case** is pelleted carrot or lettuce seed (about 3.3 mm pellets) at 25 to 50 mm spacing on a prepared vegetable bed; vegetable plates are the second plate set.

## Table 1. Requirements

Status is from SDL-CAL-001 v0.1: met, at risk, not met, or not verifiable at TRL 3.

| ID | Requirement | Target | Verification | Status (SDL-CAL-001) |
| --- | --- | --- | --- | --- |
| R1 | Single-seed placement, design case | Misses 5 % or less and multiples 5 % or less of cells, in the terms of ISO 7256-1 | Cell-speed check (CAL section 3); bench test on a sticky belt at TRL 4 | **At risk:** cell speed 0.31 m/s at 3 km/h against an assumed 0.30 m/s limit; misses and multiples cannot be calculated |
| R2 | Spacing uniformity | Coefficient of variation of in-row spacing 30 % or less in the design case | Monte Carlo (CAL section 10); field count later | **At risk:** 31 % of all spacings with the assumed miss and double rates; 9 % for single spacings |
| R3 | Spacing range | 25 to 400 mm in-row spacing, set by plate cell count (including skip-cell plates of one or two cells) and one sprocket change | Spacing formula (CAL section 2) | Met: 22 to 589 mm nominal; every target from 25 to 400 mm within 11.1 % |
| R4 | Spacing follows travel | Seed spacing set by distance travelled, not speed; wheel slip 8 % or less | Traction estimate (CAL section 6); field test later | Met: skid 1.2 to 1.7 %; rolling radius uncertain by up to 6.7 %, so calibrate per seedbed |
| R5 | Seed size range | Raw seed from 3.5 to 15 mm in its largest dimension with plates of the same diameter; seed under 2 mm sown as pelleted seed (redefined, SDL-DDR-001 item 6) | Cell tolerance rule (CAL section 4); bench test later | Met on paper: 3.5 to 15 mm raw seed; pelleted carrot fits; raw 1 to 2 mm seed does not |
| R6 | Printable plates | Each plate prints in 2 h or less on a 180 x 180 mm bed with no supports, in PETG (default) or ASA (strong sun); PLA for trials only; cell size within ±0.2 mm | Print estimate (CAL section 4); measurement later | Met: 1.46 h (maize) to 1.96 h (groundnut), no margin for thick plates; accuracy not verifiable at TRL 3 |
| R7 | Crop change | Plate swapped in 2 min or less by hand, with no tools, without emptying more than the seed in the housing | Design review; timed trial later | Not verifiable at TRL 3: side door and hand knob are in the model |
| R8 | Sowing depth | Adjustable 10 to 60 mm in 10 mm steps, held within ±10 mm on a tilled seedbed | Depth geometry (CAL section 9); field check later | **At risk:** ±10 mm holds only for wheel-path bumps of about ±15 mm under the drive wheel |
| R9 | Work rate | 0.1 ha/h or more in the design case, including turns and refills | Field capacity (CAL section 8) | Met: 0.145 ha/h (6.9 h/ha) |
| R10 | Push effort | Horizontal push force 150 N or less in the design case | Planar statics with soil model (CAL section 6); spring-scale test later | **At risk:** 136 N along the handle in the design case; 178 N at best on a heavy, loose seedbed |
| R11 | Handling | Mass 15 kg or less; handle grip height adjustable from 850 to 1,050 mm; lifted and turned at a row end by one person | Mass build-up (CAL section 5); weighing later | **Not met:** 14.6 kg base, 15.6 kg with the marker kit |
| R12 | Hopper | 2 L or more, fills from a jug without spilling, empties in 1 min or less when changing crops | Model volume (CAL section 8) | Met: 2.40 L |
| R13 | Row-spacing kit | Telescoping marker arm (decided, SDL-DDR-001 item 3) sets the next row at 200 to 900 mm from the current row, within ±25 mm | Design review | Met on paper |
| R14 | Guarding | Chain and sprocket nip points covered on the side facing the operator's hands and feet; no exposed sharp edges above the opener | Design review | Met on paper: band guard with an outboard face plate |
| R15 | Durability | Frame, drive and opener last 5 seasons of about 2 ha each with only chain, brush and plate replacement; plates last 1 season or more | Stress checks (CAL section 7); wear test later | Not verifiable at TRL 3: stresses are low, wear life unknown |
| R16 | Prototype cost | Prototype parts within the $400 budget | Priced BOM (`bom/bom.csv`) | Met: $238 |
| R17 | Replication cost | Base seeder (all items except the row marker kit) about $200 or less in parts | Priced BOM | **Not met:** $214 |
| R18 | Local build | Frame, handle and opener made from common steel sections with a drill and bolts (default, SDL-DDR-001 item 8) or a welder; drive from standard #35 roller chain or bicycle parts | Design review | Met on paper |

## Requirements not met or at risk

- **R11 not met:** 15.6 kg with the marker kit fitted. The base seeder is 14.6 kg. A lighter handle is the largest available saving (options in `docs/REVIEW.md`).
- **R17 not met:** base parts about $214. The four sprockets and idler for the ratio change and the brackets of the bolted frame are the main causes.
- **R1 at risk:** at 3 km/h the maize cells move at 0.31 m/s, just above the assumed 0.30 m/s fill limit. Walking at about 2.9 km/h (2.4 km/h with 1.2 ratio plates) keeps within it.
- **R2 at risk:** the all-spacings CV depends on miss and double rates that need a bench test.
- **R8 at risk:** the rigid opener follows the wheels, so clods under the drive wheel change the depth.
- **R10 at risk:** the design case is inside 150 N with a 9 % margin on assumed soil values; a heavy, loose seedbed needs about 178 N.

## Assumptions

All assumptions are listed in SDL-CAL-001 section 1. The main ones are a 300 mm drive wheel over the lug tips (942.5 mm travel per turn), a 0.30 m/s cell fill limit, a Brixius rolling resistance model with cone indexes of 100 to 300 kPa, and the TRL 2 miss and double rates of 5 % and 4 %.
