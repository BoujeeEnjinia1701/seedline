---
doc_id: SDL-FEA-001
title: SeedLine feasibility assessment
project: SeedLine
doc_type: Feasibility assessment
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade), for the current design (option A), closed at stage P3"
---

# SeedLine feasibility assessment

SeedLine is feasible to build and to work on paper: every part can be made with a saw, drill, taps, spanners and a desktop 3D printer from stock sold in regional towns, and the drive, metering, structure and work rate check out at first order (SDL-STM-001, SDL-CAL-001). The open feasibility questions are performance ones that only a bench or field test can settle at TRL 4: whether the printed cells fill reliably at the walking-speed rule, the miss and double rates behind the spacing uniformity, and the push force on real soils. Method: STANDARDS section 23.

Table 1. Feasibility by aspect.

| Aspect | Assessment | Rating | Risks and notes | Evidence |
| --- | --- | --- | --- | --- |
| Design (working principle) | A ground wheel driving a cell plate through a chain is the established principle of plate seeders; spacing follows travel with 1.2 to 1.7 % skid; 22 to 589 mm spacing range with the ratio kit | High | Cell fill at 0.299 m/s against an assumed 0.30 m/s limit (STM S6); spacing uniformity set by assumed miss and double rates (S7) | SDL-STM-001 S1 to S7; SDL-CAL-001 sections 2, 3, 6, 10 |
| Design (operator) | Push 132 N horizontal in the design case, 14.8 kg with the marker kit, grip 850 to 1,050 mm | Medium | Push on heavy, loose seedbeds about 179 N; sustained pushing over a planting day not yet assessed (S9, SDL-REG-001 G5); mass margin 0.18 kg | SDL-CAL-001 sections 5, 6; SDL-STM-001 S8 to S10 |
| Materials | Painted mild steel tube, plate and flat bar; PETG prints (ASA in sun); bought wheels, bearings, #35 chain and sprockets; aluminium tube for the optional marker arm | High | PETG creeps and ages in sun (S20); plate wear life unknown (PR-015); treated seed contact with plastics not assessed | SDL-STM-001 S19, S20; `bom/bom.csv` |
| Manufacturing and assembly | Cut, drill, tap, bend and bolt; no welding; housing printed whole with supports; 24 making sketches and a 17-step build plan; every part checked for fit in the kit 1.9 model (98 constructability checks and the CAD fidelity check) | High | Four fit details found by the detailed model and fixed (SDL-DEC-001 F1 to F4); tapped M5 and M6 holes in 3 mm plate are shallow (use inserts or nuts if they strip) | SDL-BLD-001; `cad/fidelity.json`; `python cad/src/model.py --check` |
| Power and controls | Human-powered; no electronics; spacing set by plate and sprocket choice | High | None at TRL 3 | SDL-PRC-001 |
| Supply of parts | Steel sections, bearings, trolley wheels and roller chain are common in regional towns; desktop printers are in towns, universities and maker spaces, rare in villages | Medium | Hubbed #35 sprockets and a go-kart chain tensioner may need ordering; who prints plates is open (SDL-PRB-001 open questions) | `bom/bom.csv`; SDL-MKT-001 |
| Cost | USD 224.10 base, USD 266.10 with both kits, against value-engineering targets of about USD 200 and USD 400 | Medium | Base seeder USD 24.10 over its target; savings listed in SDL-DEC-001 | SDL-CAL-001 section 11 |

Ratings: High, Medium, Low.

Feasibility is closed at P3 for paper work: no aspect is rated Low. The Medium ratings carry into the risk register (SDL-RSK-001) and the TRL 4 plan on hold (SDL-PLN-001).
