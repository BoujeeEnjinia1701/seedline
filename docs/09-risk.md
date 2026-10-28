---
doc_id: SDL-RSK-001
title: SeedLine risk register and hazard analysis
project: SeedLine
doc_type: Risk register and hazard analysis
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade): project risks, preliminary hazard analysis and first-pass design FMEA for the current design (option A)"
---

# SeedLine risk register and hazard analysis

The top project risks are that the printed cells do not fill reliably at walking pace (R1), that no co-design partner is engaged to validate crops, soils and spacings (R2), and that the push on heavy seedbeds is more than one operator can sustain (R3). The top hazards are the chain and sprocket nip points (H1) and contact with treated seed (H3), both controlled by design and instruction. The highest design FMEA items are a cracked or worn plate stopping the drive (F3) and a misfilled or skipped cell going unnoticed in the field (F1). Likelihood, impact, severity and occurrence are scored 1 (low) to 5 (high); detection 1 (certain to be detected) to 5 (unlikely). Method: STANDARDS section 23.

## Project risk register

Table 1. Project risks.

| # | Risk | Cause | Effect | Likelihood | Impact | Owner (role) | Response |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Cells do not fill reliably at the walking-speed rule | 0.299 m/s cell speed against an assumed 0.30 m/s limit; the limit is not from a cited test (SDL-STM-001 S6) | Misses above 5 %, PR-001 and PR-002 not met | 3 | 4 | Design lead | Bench test at TRL 4 (on hold); fallback is a smaller plate or slower walking, decided by Amish with bench data (SDL-DDR-002 item 5) |
| R2 | No co-design partner engaged | Partner not yet approached (first candidate CIMMYT, SDL-DEC-001) | Requirements, crops and soils stay unvalidated; design frozen on assumptions | 3 | 4 | Project lead (Amish) | Approach the first candidate; until then targets stay proposals |
| R3 | Push too hard on heavy or loose seedbeds | Brixius rolling resistance used outside its calibrated range; no partner soil data; 179 N on a heavy seedbed | Operator fatigue; PR-010 not met in the field | 3 | 3 | Design lead | ISO 11228-2 assessment (SDL-REG-001 G5); soil data from the partner; spring-scale test at TRL 4 |
| R4 | Printed plates wear or crack within a season | PETG abrasion by soil-laden seed, UV ageing, cold impact | Spacing drifts; drive jams | 2 | 3 | Design lead | ASA in strong sun; inspect each season (PRC Safety); wear test at TRL 4 |
| R5 | Plate printing capacity is not where farmers are | Printers rare in villages | Crop change depends on a town or a mailed plate | 3 | 3 | Co-design partner | Settle who prints plates with the partner (SDL-PRB-001 open questions) |
| R6 | Mass margin eroded by later changes | 0.18 kg margin to 15 kg with the marker kit (SDL-CAL-001 v0.6) | PR-011 not met | 3 | 2 | Design lead | Any added part needs a matching saving (SDL-DEC-001 value engineering) |
| R7 | Base seeder over its replication cost target | Bearings, hubbed sprockets, tensioner and fixings (USD 24.10 over) | Less affordable than a plate seeder | 4 | 2 | Design lead | Savings in SDL-DEC-001 tried at TRL 4 (decided 2026-10-02) |
| R8 | Bought parts differ from the assumed envelopes | Bearing bolt spacings, wheel rim and hub, tensioner reach not yet confirmed | Holes moved; parts redrawn | 3 | 2 | Builder | Confirm when bought (SDL-DEC-001, to confirm when parts are bought) |

## Preliminary hazard analysis

Table 2. Hazards.

| # | Hazard | Cause | Harm | Severity | Likelihood | Control | Residual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | Chain and sprocket nip points | The chain moves whenever the wheel turns, including when carried or cleaned | Finger crush or amputation; clothing drawn in | 4 | 2 | Printed guard over both sprockets, the chain and the tensioner's travel (PR-014); wheel lifted and held still for plate changes and cleaning; children do not push the seeder | Low, if the guard is fitted |
| H2 | Pointed opener and wheel lugs | Contact with shins and feet in use and transport | Cuts and bruises | 2 | 3 | Deburred edges, rounded lug tips, opener cover for transport | Low |
| H3 | Treated seed | Seed dressed with fungicide or insecticide handled when filling, emptying or cleaning | Poisoning, skin and eye irritation | 4 | 3 | Follow the seed label; gloves; no eating, drinking or smoking while filling; clean outdoors; hopper never used for food or feed (PRC Safety, SDL-REG-001 G7) | Medium, depends on use |
| H4 | Marker arm strike | Arm deployed up to 0.9 m to the side | Blow to a person; snag at row ends | 2 | 2 | Fold the arm for turns near people and for transport | Low |
| H5 | Manual handling | Lifting and turning at row ends; pushing on heavy soil | Back and shoulder strain | 3 | 3 | Handle height set to the operator; two people or wheel it over rough ground; mass under 15 kg (PR-011) | Medium until ISO 11228-1 and 11228-2 are assessed |
| H6 | Plate or printed part failure | Cracked plate jams the drive; door or guard cracks in cold or sun | Sudden stop and stumble; exposed chain if the guard breaks | 2 | 2 | Inspect printed parts each season; replace cracked parts; guard in PETG or sheet steel | Low |
| H7 | Workshop hazards when building | Cutting, drilling, tapping and bending steel; printing | Cuts, eye injury, burns from the print nozzle or bed | 3 | 2 | Build plan safety stops and tool notes (SDL-BLD-001 sections 6 and 7) | Low |

## Design FMEA (first pass, P3)

Table 3. Failure modes. RPN = severity x occurrence x detection.

| # | Item | Function | Failure mode | Effect | Cause | S | O | D | RPN | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F1 | Seed plate cells | Carry one seed per cell to the outlet | Cell empty (miss) or two seeds (double) | Gaps or doubles in the row; yield and seed lost | Cell speed near the fill limit; seed size outside the cell rule; brush gap wrong | 4 | 3 | 4 | 48 | Bench test of miss and double rates at TRL 4; walking-speed rule; brush gap set from outside (SDL-BLD-001 section 3.11) |
| F2 | Ground drive wheel and lugs | Turn the plate in step with travel | Wheel skids or lugs clog with mud | Spacing longer than set | Wet or loose soil; low wheel load | 3 | 2 | 3 | 18 | Lugs on the trailing edge; calibrate per seedbed (PR-004) |
| F3 | Seed plate and shaft D-flat | Transmit the drive to the plate | Plate cracks or its bore rounds off | Metering stops; row unsown until noticed | PETG ageing, cold impact, wear at the D-flat | 4 | 2 | 4 | 32 | ASA in sun; inspect plates before each season; spare plates in the kit |
| F4 | Chain and tensioner | Drive the plate shaft | Chain jumps a sprocket or the tensioner spring weakens | Metering stops or slips | Slack at the 0.8 and 1.2 ratios; worn spring | 3 | 2 | 3 | 18 | Confirm the tensioner's take-up at 74 and 77 links when bought (SDL-DEC-001) |
| F5 | Opener and drop tube | Cut the furrow and guide seed into it | Opener or tube blocks with wet soil | Seed left on the surface | Sticky soil; residue | 3 | 3 | 2 | 18 | Clean at row ends; tube slides on its spigot and is easy to clear |
| F6 | Depth setting | Hold depth within +/-10 mm | Depth varies over clods | Uneven emergence | Rigid opener follows the wheels (0.69 of a drive-wheel rise) | 3 | 3 | 3 | 27 | Restated for ploughed seedbeds (PR-008); spring-loaded opener reviewed with partner data |
| F7 | Housing door and liners | Keep seed in the slot | Door loose or liner misplaced after a plate change | Seed leaks; plate rubs | Thumb screws not tightened; liner on the wrong side | 2 | 2 | 2 | 8 | Door screws into heat-set inserts in solid wall (SDL-DEC-001 F1); liners pegged |
| F8 | Frame joints | Hold the wheels, meter and handle in line | Bolted joints loosen | Misalignment; chain runs off | Vibration on rough ground; crushed tube walls | 3 | 2 | 2 | 12 | Threadlocker; bolts snug, not hard (SDL-BLD-001); check at first use |
| F9 | Handle telescoping joint and tabs | Carry the push and lifting loads | Tube cracks at a pin hole or flattened end | Loss of control | Fatigue at a factor of 1.9 on static side load | 4 | 2 | 3 | 24 | Fatigue test at TRL 4; sleeve and pin details in the model |
| F10 | Hopper | Feed seed to the housing | Seed bridges in the funnel | Pool runs dry; misses | Seed with awns or treatment dust; damp seed | 3 | 2 | 3 | 18 | Funnel to a 60 x 30 mm throat; check seed flow at TRL 4 |

The FMEA is a first pass on paper; occurrence and detection scores are estimates until bench and field data exist.
