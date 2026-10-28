---
doc_id: SDL-STM-001
title: SeedLine STEM check
project: SeedLine
doc_type: STEM check
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First STEM check (kit 1.8 and 1.9.1 upgrade) of the current design (option A) and option B; six details fixed under Amish's standing instruction of 2026-10-23 (SDL-DEC-001 F1 to F4, F6, F8); independent review recorded"
---

# SeedLine STEM check

**Verdict: open.** SeedLine's working principle, a ground wheel driving a printed cell plate through a chain so that spacing follows travel, sits within known physics, and no claim of either option fails. Of 37 rows, 28 are within known science and 9 are plausible, all nine open because only a bench test, a print, an ergonomic assessment, weighing or a field trial can close them: cell fill at the walking-speed rule (S6), spacing uniformity with assumed miss and double rates (S7), the push in the design case with an assumed opener draft (S8), whether one operator sustains it (S9), mass with 0.18 kg of margin (S10), groundnut plate print time (S16), print accuracy against the cell clearance (S17), and option B's seed delivery timing (OB4) and jaw opening (OB6). `project.yaml` records `stem_check: open`. The detailed kit 1.9 model found four fit details that failed (S24 to S27) and, once every fastener was weighed, a mass over the 15 kg target (S10); the independent review refuted the print time (S16). Each was fixed in the design under Amish's standing instruction of 2026-10-23 and is recorded in SDL-DEC-001 (F1 to F4, F6, F8). Method: STANDARDS section 20. Calculations: `docs/04-calcs/stem_check.py`, results in `docs/04-calcs/stem_results.csv`.

## Claims checked

Table 1. Claims, governing science and verdicts.

| # | Claim | Field | Branch | Governing law or source | First-order check | Verdict | Closed by |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | In-row spacing follows travel: 4-cell maize plate at ratio 1.0 gives 236 mm nominal for the 250 mm target, about 220 to 240 mm with the 1.2 to 1.7 % skid and up to 6.7 % shorter rolling radius, so spacing is calibrated per seedbed | Mathematics | Units and dimensional analysis | Spacing = pi D / (cells x ratio); D = 300 mm over the lug tips | claimed 236 mm, estimate 236 mm (ratio 1.00) | **Within known science** | SDL-CAL-001 section 2 |
| S2 | The 76-link #35 chain fits the 286 mm sprocket centres, the spring tensioner taking up the slack | Engineering and technology | Manufacturing tolerances | Chain length L/p = 2C/p + (T1 + T2)/2 + ((T2 - T1)/2 pi)^2 p/C; idler deflection sqrt(slack C / 2) within the tensioner's 45 mm | 35 mm idler deflection <= 45 mm idler deflection | **Within known science** | SDL-CAL-001 section 2 |
| S3 | Meter torque at the plate shaft stays under the 1.0 N m design value | Physics | Mechanics and statics | Janssen wall pressure of a 0.2 m seed head on the lower quarter of the plate, friction 0.4; brush drag; bearings and chain 0.1 N m | 0.2 N m <= 1 N m | **Within known science** | SDL-CAL-001 section 3a |
| S4 | Chain tension at the design meter torque with a 1.2 service factor is far below the #35 chain's minimum tensile strength | Physics | Strength of materials | T = torque / pitch radius; #35 roller chain minimum tensile strength about 7.8 kN (ANSI B29.1 class) | 52 N (limit is 10 % of the minimum tensile strength) <= 780 N (limit is 10 % of the minimum tensile strength) | **Within known science** | SDL-CAL-001 section 7 |
| S5 | Wheel skid from the meter torque stays under 8 %, so spacing follows travel | Physics | Mechanics and statics | Traction ratio = drive force / wheel load; Brixius traction relation for a rigid wheel in a cone index of 100 to 300 kPa | 1.7 % <= 8 % | **Within known science** | SDL-CAL-001 section 6a |
| S6 | Each maize cell fills with one seed at 0.299 m/s cell speed (walking-speed rule 2.9 km/h) | Physics | Mechanics and statics | Gravity fill of a cell passing a seed pool; the assumed 0.30 m/s working limit for vertical cell plates is not from a cited test; the kinematic indicator for a still seed (the seed falls its own depth while the open cell passes) is 0.20 m/s | 0.299 m/s against an assumed 0.30 m/s, no margin; a seed dragged by the plate fills at higher speed than a still seed | **Plausible, to confirm at TRL 3** | Open |
| S7 | Spacing coefficient of variation of 31 % of all spacings, design case (target 30 %) | Mathematics | Statistics and uncertainty | Monte Carlo of 20,000 cells with an assumed 5 % miss, 4 % double, 15 mm drop scatter and 5 +/- 1.5 % slip; the result is set by the assumed miss and double rates, which only a bench test gives | 31 % of all spacings, 9 % for singles, against 30 %; within the uncertainty of the assumed inputs | **Plausible, to confirm at TRL 3** | Open |
| S8 | Horizontal component of the push in the design case is 150 N or less (the push applied along the 50 deg handle is 205 N, 157 N of it downward) | Physics | Mechanics and statics | Planar statics with Brixius motion resistance (used outside its calibrated range for small rigid wheels), opener draft from an assumed 30 kPa specific resistance (68 of the 133 N) | 132 N <= 150 N | **Plausible, to confirm at TRL 3** | Open |
| S9 | One operator sustains the push: 132 N horizontal (205 N along the handle) at 0.81 m/s is 106 W of external work while walking, with a 15 s turn every 62 s | Biology | Ergonomics | Sustained pushing guidance (ISO 11228-2 method) depends on distance, frequency, height and the population; not yet assessed. The kit's screening value for sustained cranking is 75 W | 106 W external against a 75 W cranking screen; walking push uses larger muscle groups; ISO 11228-2 assessment to do | **Plausible, to confirm at TRL 3** | Open |
| S10 | Seeder with the marker kit weighs 15 kg or less | Physics | Mechanics and statics | Mass build-up from the model's part volumes (steel 7,850 kg/m3, PETG 1,270 kg/m3, aluminium 2,700 kg/m3), every fastener from the model, and about 4.5 kg of catalogue-class bought parts whose 5 % error is about 0.2 kg | 14.8 kg <= 15 kg | **Plausible, to confirm at TRL 3** | Open |
| S11 | Side rails stay below yield with a dynamic factor of 3 for drops and stones | Physics | Strength of materials | Beam bending of 25 x 25 x 1.5 square tube, S235 yield 235 MPa (EN 10025-2) | 70 MPa (limit is yield / 1.5) <= 156.7 MPa (limit is yield / 1.5) | **Within known science** | SDL-CAL-001 section 7 |
| S12 | Handle side tube (22 x 1.2) stays below yield under a 100 N side load at the grip together with the heavy-seedbed push (221 N at 36 deg) | Physics | Strength of materials | Cantilever bending of round tube in two planes, combined; S235 yield 235 MPa (independent review of 2026-10-24 added the push component) | 143 MPa (limit is yield / 1.5) <= 156.7 MPa (limit is yield / 1.5) | **Within known science** | SDL-CAL-001 section 7 (fatigue to test at TRL 4) |
| S13 | A seed in a cell is not thrown out of the cell by the plate's rotation | Physics | Mechanics and statics | Centripetal acceleration omega^2 r at the cell circle against g | 1.6 m/s2 <= 9.81 m/s2 | **Within known science** | This file |
| S14 | Field capacity 0.142 ha/h (7.1 h/ha) for maize on 0.75 m rows at 2.9 km/h | Mathematics | Orders of magnitude | Capacity = row spacing x speed x field efficiency (65 %: 50 m rows, 15 s turns, 90 s refills, 85 % working time) | claimed 0.142 ha/h, estimate 0.141 ha/h (ratio 1.00) | **Within known science** | SDL-CAL-001 section 8 |
| S15 | One 2.42 L hopper fill sows about 1,450 m of maize row at 250 mm | Mathematics | Orders of magnitude | Row length = volume x bulk density (0.72 kg/L) / seed mass (0.30 g) x spacing | claimed 1451 m, estimate 1.45e+03 m (ratio 1.00) | **Within known science** | SDL-CAL-001 section 8 |
| S16 | The 10 mm groundnut plate, the slowest, prints in 2 h or less | Engineering and technology | Manufacturing tolerances | Print time = deposited volume / 6 mm3/s average rate (unsourced; 1.6 mm skins, 1.2 mm walls round the rim, every cell and the bore, 20 % infill since SDL-DEC-001 F8). With the cell ends left out and 25 % infill it read 1.96 h; corrected it was 2.05 h, a fail, fixed by F8 | 1.9 h <= 2 h | **Plausible, to confirm at TRL 3** | Open |
| S17 | A desktop FDM print holds the cell size closely enough: +/-0.2 mm on the pelleted carrot cell (3.8 mm deep for a 3.3 mm pellet) | Engineering and technology | Manufacturing tolerances | Tolerance ratio 0.2 / 3.8 mm = 5.3 % of the cell, but 43 % of its 0.47 mm clearance over the pellet; FDM holes and slots print undersize (a bias, not only a tolerance) | 5.3 % of the cell against the 10 % rule; tight against the clearance; a printed test coupon of cells sets the offset | **Plausible, to confirm at TRL 3** | Open |
| S18 | A drive-wheel bump moves the opener by 0.69 of the bump, so +/-10 mm depth holds for bumps up to about +/-14.5 mm (ploughed seedbed) | Physics | Mechanics and statics | Rigid frame on two wheels: the opener point, 181 mm behind the drive axle on a 580 mm wheelbase, moves (x - x_press) / wheelbase of a drive wheel rise | 0.69 of a drive-wheel rise <= 1 of a drive-wheel rise | **Within known science** | SDL-CAL-001 section 9 |
| S19 | Printed PETG plate takes the drive at its D-flat without yielding | Chemistry | Materials and polymer chemistry | Bearing stress = torque x 1.2 / (lever arm x flat area); PETG tensile yield about 50 MPa (typical datasheet value) | 5.7 MPa (limit is yield / 3 for a printed part) <= 16.67 MPa (limit is yield / 3 for a printed part) | **Within known science** | SDL-CAL-001 section 7 |
| S20 | PETG plates degrade in strong sun; ASA is used where plates stay in the sun, PLA for trials only | Chemistry | Materials and polymer chemistry | UV photo-oxidation of polyesters; ASA's acrylic outer phase is UV stable (polymer supplier datasheets) | Material rule decided (SDL-DDR-001 item 9); plates inspected each season (PRC Safety) | **Within known science** | SDL-PRC-001 Safety |
| S21 | Treated seed is toxic; gloves, no eating or drinking while filling, cleaning outdoors and a hopper never used for food control the exposure | Biology | Toxicology | Seed treatment labels and humanitarian guidance require PPE, especially gloves (ICRC, Warning: treated seeds) | Safety claim only; the design adds no exposure route beyond filling and cleaning | **Within known science** | SDL-PRC-001 Safety |
| S22 | Maize sown at 50 mm sits within the recommended seeding depth | Biology | Ecology and agronomy | Purdue University Department of Agronomy (2022): most common recommended corn seeding depths are 1.5 to 2 inches (38 to 51 mm); the design case sits at the top of the range and +/-10 mm control spans 40 to 60 mm | 50 mm <= 51 mm | **Within known science** | Purdue Agronomy (2022); depth set per crop on the shank |
| S23 | Even spacing raises yield: about 140 to 160 kg/ha of maize per 25 mm less spacing standard deviation, less at smallholder yield levels | Biology | Ecology and agronomy | Nielsen, Purdue University plant spacing trials | Cited effect; SeedLine claims only that spacing follows travel, not a yield figure | **Within known science** | SDL-PRB-001 |
| S24 | The housing door's two thumb screws land in solid housing wall | Engineering and technology | Manufacturing tolerances | Fit check in the detailed model: as drawn at kit 1.7 the screws at 12 mm from the door's rear edge stood over the 128 x 132 opening, not over wall | Fixed: door 146 x 150 to the housing's edges; screws at 7 mm from the rear edge (rear wall band) and 7 mm up (floor band), into M4 heat-set inserts | **Within known science** | SDL-DEC-001 F1 (decided under the standing instruction of 2026-10-23) |
| S25 | The wheel hub cross bolt clears the wheel's disc web | Engineering and technology | Manufacturing tolerances | Fit check in the detailed model: the cross hole at 107 mm put the bolt head and nut in the plane of the 2 mm web | Fixed: cross hole moved to 122 mm from the axle's chain-side end, 15 mm off the web, inside the 45 mm hub | **Within known science** | SDL-DEC-001 F2 (decided under the standing instruction of 2026-10-23) |
| S26 | The tensioner's pivot fixing clears the chain's upper strand | Engineering and technology | Manufacturing tolerances | Fit check in the detailed model: a head or nut on the boss's outer end sits in the upper strand (7 mm above the pivot) at the real 12 mm chain width | Fixed: M8 x 40 screw from inside the frame through the rail into the tensioner's tapped boss | **Within known science** | SDL-DEC-001 F3 (decided under the standing instruction of 2026-10-23) |
| S27 | The hopper's M5 heat-set inserts fit their bosses | Engineering and technology | Standards practice | Insert makers specify a hole of about 6.4 mm for M5 heat-set inserts; the bosses were drawn with 4.0 mm holes (a tap drill size) | Fixed: 6.5 mm holes in the eight bosses | **Within known science** | SDL-DEC-001 F4 (decided under the standing instruction of 2026-10-23) |
| S28 | A jammed plate does not damage the steel drive: the wheel drives until it skids (about 11 N m at the plate shaft), and the printed plate's bore strips first | Physics | Strength of materials | Traction about 0.7 of the drive-wheel load at 150 mm; chain tension against 7.8 kN; D-flat bearing stress against about 50 MPa for PETG (independent review of 2026-10-24) | 497 N chain tension (limit 10 % of minimum tensile); the plate's D-flat reaches about 54 MPa, so the plate is the sacrificial part <= 780 N chain tension (limit 10 % of minimum tensile); the plate's D-flat reaches about 54 MPa, so the plate is the sacrificial part | **Within known science** | SDL-CAL-001 section 7; spare plate in the kit |
| S29 | The tensioner takes up chain wear until about 0.8 % elongation; the chain is then shortened by a link pair or replaced | Engineering and technology | Manufacturing tolerances | Idler deflection sqrt(slack x C / 2): 35 mm new, 48 mm at 1 % elongation, against 45 mm of take-up (independent review of 2026-10-24) | 45 mm take-up against mm needed at 1 % elongation (the claim is the wear limit) <= 48 mm take-up against mm needed at 1 % elongation (the claim is the wear limit) | **Within known science** | SDL-BLD-001 first checks; wear limit in the build plan |
| S30 | The 20 x 2 mm hopper uprights carry the hopper sideways: they sway 1 mm before the hopper's neck bears in the housing collar, which takes the rest | Physics | Strength of materials | Cantilever deflection F L^3 / 3 E I limited to the collar's 1 mm clearance (SDL-DDR-003 P7); free-standing they would reach about 300 MPa at three times the full hopper's weight sideways (independent review of 2026-10-24) | 10 MPa at 1 mm sway (limit yield / 1.5) <= 156.7 MPa at 1 mm sway (limit yield / 1.5) | **Within known science** | SDL-CAL-001 section 7 |
| S31 | The aluminium marker arm stays below yield at its full 900 mm reach with a dynamic factor of 3 | Physics | Strength of materials | Cantilever bending of 20 x 1.5 tube under 20 N side drag; 6061-T6 tube, typical minimum yield about 240 MPa (6063-T6 about 170 MPa would give a factor of 1.3); independent review of 2026-10-24 | 128 MPa (limit is yield / 1.5) <= 160 MPa (limit is yield / 1.5) | **Within known science** | SDL-CAL-001 section 7; 6061-T6 in the BOM |
| OB1 | Option B: six punches on a 480 mm rim give 251 mm spacing | Mathematics | Units and dimensional analysis | Spacing = 2 pi R / N (rim rolling on the surface; sinkage shortens it) | claimed 251 mm, estimate 251 mm (ratio 1.00) | **Within known science** | SDL-OPT-001 |
| OB2 | Option B: the wheel's weight presses a punch 50 mm into tilled soil (32 N needed at a 200 kPa cone index) | Physics | Mechanics and statics | Penetration force about cone index x punch section; wheel share of a 12.4 kg machine about 75 % | 32 N <= 91 N | **Within known science** | SDL-OPT-001 |
| OB3 | Option B is limited to tilled seedbeds, as option A is: in firm untilled soil (1.5 MPa cone index) a punch needs about 243 N, more than the wheel's share plus 100 N of downward push; the crossover is near 1.2 MPa | Physics | Mechanics and statics | As OB2; firm untilled soils reach cone indexes of 1 to 2 MPa (typical range, to confirm with partner data). The claim is the limitation, so the check is that the force needed exceeds the force available | 243 N needed against N available >= 191 N needed against N available | **Within known science** | SDL-OPT-001 (no untilled-soil advantage claimed) |
| OB4 | Option B: a seed released at -15 deg reaches the punch's jaws before the jaw opens at the bottom (arrives at -78 deg; the punch enters the soil at -54 deg; at about 3.3 km/h it arrives after 90 deg) | Physics | Mechanics and statics | Seed sliding out along a rotating tube: gravity, centrifugal and Coriolis terms with wall friction 0.4, at 2.9 km/h | 78 deg past forward (the jaw opens near 90) <= 90 deg past forward (the jaw opens near 90) | **Plausible, to confirm at TRL 3** | Open |
| OB5 | Option B: the hub cell ring's cells move at 0.23 m/s, under the 0.30 m/s fill limit assumed for option A | Physics | Mechanics and statics | Cell speed = wheel angular speed x cell radius (69 mm) | 0.23 m/s <= 0.3 m/s | **Within known science** | SDL-OPT-001 |
| OB6 | Option B: soil pushes the trailing jaw open in the soil and a torsion spring closes it as the punch lifts out | Physics | Mechanics and statics | Punch planters with hinged jaws are established (jab planters; Molin et al. 1998 report a punch planter prototype with synchronisation and soil-sticking problems) | Working in principle; jaw opening timing, soil sticking and spring force not calculated | **Plausible, to confirm at TRL 3** | Open |

Verdicts: **Within known science**, **Plausible, to confirm at TRL 3**, **Fails, fix proposed**, **Fails**.

## Fixes made under the standing instruction

1. **Door screws (S24, F1).** The door's thumb screws stood over the housing's opening. The door now reaches the housing's rear and bottom edges (146 x 150 mm) and the screws go into M4 heat-set inserts in the solid wall.
2. **Hub cross bolt (S25, F2).** The bolt fixing the wheel hub to the axle lay in the plane of the wheel's web. The cross hole moves to 122 mm from the axle's chain-side end, 15 mm off the web.
3. **Tensioner pivot (S26, F3).** A bolt head or nut on the boss's outer end sat in the chain's upper strand. The pivot is now an M8 x 40 screw from inside the frame into the boss.
4. **Hopper insert holes (S27, F4).** The bosses had 4.0 mm holes; M5 heat-set inserts need about 6.4 mm. They are now 6.5 mm.
5. **Mass (S10, F6).** Weighing every bolt, nut, washer and pin from the model added about 0.5 kg to SDL-CAL-001's fastener estimate, and the real M16 press axle bolt 0.08 kg, taking the seeder with the marker kit to 15.5 kg against 15 kg. The drop plates and bearing plate are now 3 mm, the hopper uprights 20 x 2 mm flat bar, the marker arm aluminium tube and the marker disc 1.5 mm: 14.8 kg with 0.18 kg of margin, every stress checked (SDL-CAL-001 v0.6 section 7).
6. **Print time (S16, F8).** The independent review found that the print estimate counted only two sides of each cell; with all four it was 2.05 h against 2 h. Plate infill drops from 25 to 20 %, which the plates' stresses allow (S19, S28): 1.87 h.

A sixth fit detail found by the model (the rear drop plate's front rail bolt under the handle's flattened end, SDL-DEC-001 F7) is a constructability fix with no STEM row.

## Fields not relevant

Every field has at least one row. Electromagnetism, optics, acoustics, thermodynamics and nuclear radiation are not relevant: the seeder has no electrics, heat source or radiation, and its noise is that of a chain at walking pace. Microbiology and epidemiology are not relevant beyond the treated-seed toxicology in S21.

## Concept options

- **Option A, cell plate on a chain drive (the current design):** no row fails; S6 to S10, S16 and S17 open (rows S1 to S31).
- **Option B, punch wheel with a hub meter:** no row fails; OB4 (seed reaches the jaws at about 78 degrees past forward against the jaw opening near 90, at 2.9 km/h) and OB6 (jaw opening by soil reaction) open; OB3 records that B gives no untilled-soil advantage without ballast (rows OB1 to OB6).

## Independent review

A second agent, run headless with `claude -p` and given only this check, SDL-CAL-001, SDL-PRS-001 and `sizing.py`, tried to refute every row on 2026-10-24. It could not import the CAD model, so it re-implemented the calculations, reading CAD values back from the tabulated results. Its findings and the actions taken:

Table 2. Independent review findings and actions.

| Row | Finding | Action |
| --- | --- | --- |
| S16 | Refuted: the cell perimeter counted two sides of each cell (2.04 h, over 2 h); the 6 mm3/s rate is unsourced | Fixed under the standing instruction (F8, 20 % infill, 1.87 h); verdict Plausible with the rate flagged |
| S8 | The 133 N is the horizontal component; along the 50 degree handle the push is 207 N, 158 N of it downward; opener draft is 68 N of it from an assumed 30 kPa | Relabelled; resultant and vertical force stated; row open (not closed by a note that marks R10 at risk) |
| S9 | Quoted stale figures (132 N, 106 W); a cranking screen does not suit pushing | Figures updated; ISO 11228-2 assessment stays open |
| S10 | About 4.5 kg of catalogue estimates, 5 % error about 0.2 kg, against 0.18 kg of margin | Verdict Plausible, closed by weighing |
| S12 | Lateral load only; the push across the tube adds about 53 N | Combined case added: 143 MPa, factor 1.6 on yield (passes yield / 1.5) |
| S19 | Jammed plate: wheel torque is set by traction (about 11 N m), not 1.0 N m | New row S28: chain 497 N against 780 N; the plate's D-flat (about 54 MPa) strips first, so the printed plate is the sacrificial part; a shear pin or slip clutch is a suggestion for Amish |
| S2 | Chain wear missing: 1 % elongation needs 48 mm of take-up against 45 mm | New row S29: wear limit about 0.8 %, then shorten or replace the chain (build plan) |
| Missing | Hopper upright lateral load | New row S30: the uprights sway 1 mm before the hopper neck bears in the housing collar (10 MPa) |
| Missing | Marker arm at 900 mm with a dynamic factor | New row S31: 128 MPa; specified as 6061-T6 (yield about 240 MPa) in the BOM |
| S1 | Slip and rolling radius give 220 to 240 mm, not 248 mm | Band quoted; spacing calibrated per seedbed |
| S17 | Judge against the 0.47 mm clearance; FDM holes print undersize | Verdict Plausible; a printed cell coupon sets the offset |
| S4 | The 1.2 is a service factor | Relabelled |
| S22 | Citation did not match the source list; 50 mm is the top of the range | Citation fixed; depth set per crop on the shank |
| OB3, OB4 | Cone index threshold about 1.2 MPa; arrival passes 90 degrees near 3.3 km/h | Stated in the rows |
| S6, S7 | Indicator 0.20 m/s against 0.299 m/s; CV sensitive to the drop scatter and miss rates | Kept Plausible; the TRL 4 bench test is a gate (SDL-PLN-001) |

Not acted on in this session, listed for the next step in `docs/REVIEW.md`: drive axle and wheel impact checks, drop plate net section at the bolt holes, differential wheel sinkage, runner opener vertical force at 60 mm, seed size variation and doubles, creep of printed parts in sun, and chain polygonal action (about 2 %).

## Sources

- Brixius, W. W. 1987. "Traction Prediction Equations for Bias Ply Tires." ASAE Paper 87-1622 (rolling resistance and traction, S5, S8).
- EN 10025-2, hot rolled structural steel (S235 yield 235 MPa; S11, S12), cited by title.
- ANSI B29.1 roller chain class, #35 minimum tensile strength about 7.8 kN (S4), as used in SDL-CAL-001.
- International Committee of the Red Cross, *Warning: Treated Seeds*, https://www.icrc.org/en/publication/4688-warning-treated-seeds, accessed 2026-10-24 (S21).
- ISO 11228-2, Ergonomics, Manual handling, Part 2: Pushing and pulling (S9), cited by title; not yet applied.
- Molin, J. P., et al. 1998. "Population Rate Changes and Other Evaluation Parameters for a Punch Planter Prototype." *Transactions of the ASAE* 41 (5): 1265 to 1270 (OB6).
- Nielsen, R. L. 2004. "Effect of Plant Spacing Variability on Corn Grain Yield." Purdue University, https://www.agry.purdue.edu/ext/corn/research/psv/update2004.html (S23).
- Purdue University Department of Agronomy. 2022. "How Deep Should Corn Be Planted?" https://ag.purdue.edu/news/department/agronomy/kernel-news/2022/12/how-deep-corn-planted.html, accessed 2026-10-24 (S22).
- SDL-CAL-001, `docs/04-calcs/sizing.py`, for every option A figure.
