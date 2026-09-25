---
doc_id: SDL-REQ-001
title: SeedLine requirements
project: SeedLine
doc_type: Requirements
version: "0.2"
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
---

# SeedLine requirements

These are first-pass requirements for the concept. Targets are proposals for review, not yet validated with users, and will be checked by calculation at TRL 3 and revised after co-design sessions (see SDL-PRB-001).

The **design case** is maize at 250 mm in-row spacing on 0.75 m rows, sown 50 mm deep in a tilled loam seedbed at a walking speed of 3 km/h (about 0.83 m/s). The **small-seed case** is carrot or lettuce seed of 1 to 2 mm at 25 to 50 mm spacing on a prepared vegetable bed.

## Table 1. Requirements

| ID | Requirement | Target | Verification (TRL 3 or later) | Concept status (estimate) |
| --- | --- | --- | --- | --- |
| R1 | Single-seed placement, design case | Misses 5 % or less and multiples 5 % or less of cells, in the terms of ISO 7256-1 | Metering calculation; later bench test on a sticky belt | About 5 % misses, 4 % multiples: met on paper, no margin |
| R2 | Spacing uniformity | Coefficient of variation of in-row spacing 30 % or less in the design case | Later field count | Unverified; depends on seed bounce in the drop tube |
| R3 | Spacing range | 25 to 400 mm in-row spacing, set by plate cell count and one sprocket change | Spacing formula (SDL-PRC-001) | About 22 to 390 mm: **not met** above 390 mm |
| R4 | Spacing follows travel | Seed spacing set by distance travelled, not speed; wheel slip 8 % or less | Slip estimate; later field test | 3 to 8 % slip estimated: met, thin margin |
| R5 | Seed size range | Seeds from 1.5 to 15 mm in their largest dimension with plates of the same diameter | Plate design review; later bench test | **At risk** below about 2 mm (FDM cell accuracy) |
| R6 | Printable plates | Each plate prints in 2 h or less on a 180 x 180 mm bed in PLA, PETG or ASA with no supports; cell size within ±0.2 mm | Slicer estimate; later measurement | About 1 h, 25 g PETG: met on paper; accuracy unverified |
| R7 | Crop change | Plate swapped in 2 min or less by hand, with no tools, without emptying more than the seed in the housing | Design review; later timed trial | Side door and hand knob proposed: met on paper |
| R8 | Sowing depth | Adjustable 10 to 60 mm in 10 mm steps, held within ±10 mm on a tilled seedbed | Design review; later field check | Slotted shank bracket: met on paper; control on rough seedbeds unverified |
| R9 | Work rate | 0.1 ha/h or more in the design case, including turns and refills | Field capacity estimate | About 0.14 ha/h: met |
| R10 | Push effort | Horizontal push force 150 N or less in the design case | Force estimate; later spring-scale test | About 100 N on a good seedbed, up to about 220 N on a heavy one: **at risk** |
| R11 | Handling | Mass 15 kg or less; handle grip height adjustable from 850 to 1,050 mm; lifted and turned at a row end by one person | Mass estimate; later weighing | About 14 kg: met, thin margin |
| R12 | Hopper | 2 L or more, fills from a jug without spilling, empties in 1 min or less when changing crops | Model volume | About 2.1 L: met |
| R13 | Row spacing kit | Marker sets the next row at 200 to 900 mm from the current row, within ±25 mm | Design review | Telescoping arm: met on paper |
| R14 | Guarding | Chain and sprocket nip points covered on the side facing the operator's hands and feet; no exposed sharp edges above the opener | Design review | Band guard in the model: met on paper |
| R15 | Durability | Frame, drive and opener last 5 seasons of about 2 ha each with only chain, brush and plate replacement; plates last 1 season or more | Design review; later wear test | Unverified |
| R16 | Prototype cost | Prototype parts within the $400 budget | Priced BOM (`bom/bom.csv`) | About $223: met |
| R17 | Replication cost | Base seeder (all items except the row marker kit) about $200 or less in parts | Priced BOM | About $199: met, no margin |
| R18 | Local build | Frame, handle and opener made from common steel sections with a drill and a welder or bolts; drive from standard #35 roller chain or bicycle parts | Design review | Met on paper |

## Requirements not met or at risk

- **R3 not met:** the longest spacing is about 390 mm with three cells and the smallest wheel sprocket. Wider spacings would need a plate with fewer cells, a 10 T sprocket or a skip-cell plate. Proposed: relax the target to 390 mm or add a skip plate, awaiting Amish.
- **R5 at risk:** cells for 1 to 2 mm seed are near the accuracy of a 0.4 mm FDM nozzle. Pelleted seed, a 0.25 mm nozzle or resin-printed plates may be needed.
- **R10 at risk:** the force estimate is about 100 N on a good seedbed but reaches about 220 N on a heavy or cloddy one, mostly from opener draft and from the downward share of the push along a steep handle.
- **R1, R4 and R11** are met only with thin or no margin.

## Assumptions

- Ground wheel effective diameter 300 mm (942 mm travel per turn) before slip.
- Walking speed 3 km/h; field efficiency 65 % for turns, refills and stops.
- Soil rolling resistance coefficient 0.2 to 0.3 on tilled soil for narrow wheels; opener draft 40 to 80 N at 50 mm depth. Both are estimates to check at TRL 3.
- Miss and multiple rates follow typical figures for cell-type mechanical meters with a brush; they are estimates, not measured values for this plate.
