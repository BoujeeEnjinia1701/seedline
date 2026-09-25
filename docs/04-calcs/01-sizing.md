---
doc_id: SDL-CAL-001
title: SeedLine sizing and first-principles checks
project: SeedLine
doc_type: Calculation note
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (drive and spacing, metering, plates, mass, push force, slip, structure, work rate, depth, uniformity, cost) against every requirement
---

# SeedLine sizing and first-principles checks

On paper the seeder works as a ground-driven single-row planter: the drive covers 22 to 589 mm of in-row spacing, slip from the metering load is under 2 %, the parts are lightly stressed and the work rate is about 0.145 ha/h. Ten of the eighteen requirements are met and two cannot be verified at TRL 3. Four are **at risk**: R1 (cell speed at 3 km/h is 0.31 m/s against an assumed 0.30 m/s limit), R2 (spacing CV about 31 % with assumed miss, double and scatter rates), R8 (depth holds ±10 mm only for wheel-path bumps of about ±15 mm) and R10 (136 N push in the design case, but 178 N at best on a heavy, loose seedbed). Two are **not met**: R11 (15.6 kg with the marker kit against 15 kg) and R17 (base seeder parts about $214 against about $200).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the key dimensions, sprocket geometry, cell sizes, hopper volume and handle geometry from the parametric model `cad/src/model.py`, and the prices from `bom/bom.csv`, so the model, the drawing SDL-DWG-001, the BOM and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Architecture | Vertical cell plate, #35 chain, front drive wheel, rear press wheel, bolted frame, marker arm | Decided, SDL-DDR-001 items 1, 3, 4, 7 and 8 |
| Design case | Maize at 250 mm on 0.75 m rows, 50 mm deep, 3 km/h (0.83 m/s) | SDL-REQ-001 |
| Drive wheel | 300 mm over the lug tips, 45 mm wide, 10 mm lugs; travel 942.5 mm per turn before slip | Model parameter |
| Typical slip for spacing tables | 5 % | Allowance; the calculated skid (section 6) is lower |
| Cell fill limit | 0.30 m/s cell speed | Assumed working limit for a gravity-filled cell plate; to be checked by bench test at TRL 4 |
| Cell size | Length 1.15 L + 0.5 mm, depth 1.05 W + 0.3 mm, plate thickness the larger of 6 mm and 1.2 T (L, W, T: seed length, width, thickness) | Rule used by `make_plate` in the model |
| Seed dimensions | Maize 12 x 8 x 5 mm, sorghum 4.5 x 4 x 3, groundnut kernel 15 x 9 x 8, common bean 13 x 8 x 6, spinach 3.5 x 3 x 2.5, pelleted carrot 3.3 mm, raw carrot 3 x 1.2 x 0.6 | Typical values; varieties differ |
| Print | ±0.2 mm on a 0.4 mm nozzle, tolerance limited to 10 % of the smallest cell dimension; 1.6 mm of skins, 1.2 mm walls, 25 % infill; 6 mm³/s average rate; PETG 1.27 g/cm³ at $25/kg | Common desktop FDM printer |
| Meter torque | 1.0 N·m at the plate shaft (design value) | First-principles estimate is 0.20 N·m (section 3); the design value is five times higher |
| Soil | Cone index 300, 200 and 100 kPa for good, design and heavy (loose, cloddy) seedbeds; opener specific resistance 20, 30 and 40 kPa; covering chains and press 10, 15 and 20 N | Assumed; no soil data from a partner region yet |
| Rolling resistance | Brixius motion resistance, MR/W = 1/Bn + 0.04, with Bn = CI b d / W / (1 + 3 b/d) for a rigid wheel | Brixius (1987), an empirical model fitted to larger tires; used here outside its calibrated range |
| Opener draft | Specific resistance x 2.5 x 18 mm runner width x depth | Narrow-tool failure zone taken as 2.5 tool widths |
| Field work | 50 m rows, 15 s per turn, 90 s per refill, 85 % working time | Assumed for a small plot and one operator |
| Structure | S235 class steel, yield 235 MPa; dynamic factor 3 for drops and stones; 100 N side load at the grip | Assumed |
| Uniformity model | 5 % misses, 4 % doubles (second seed 0 to 30 mm behind), 15 mm drop scatter, slip 5 ± 1.5 % | The miss and double rates are the TRL 2 estimates; not calculable from first principles |

## 2. Drive, spacing and range (R3, R4)

The spacing is s = π D / (n i) / (1 − σ), with π D = 942.5 mm, n plate cells, ratio i = wheel teeth / 15 and travel reduction σ. The three wheel sprockets give i = 0.8, 1.0 and 1.2 (pitch diameters 36.80, 45.81 and 54.85 mm; plate sprocket 15 T).

*Table 2. Example plates. Nominal spacing, and with the 5 % slip allowance.*

| Crop | Target (mm) | Cells | Ratio | Nominal (mm) | With 5 % slip (mm) |
| --- | --- | --- | --- | --- | --- |
| Maize (design case) | 250 | 4 | 1.0 | 235.6 | 248.0 |
| Sorghum, groundnut | 150 | 6 | 1.0 | 157.1 | 165.3 |
| Common bean | 100 | 9 | 1.0 | 104.7 | 110.2 |
| Spinach | 50 | 16 | 1.2 | 49.1 | 51.7 |
| Carrot, lettuce (pelleted) | 25 | 30 | 1.2 | 26.2 | 27.6 |
| Skip-cell plate | 400 | 2 | 1.2 | 392.7 | 413.4 |
| Skip-cell plate | 450 | 2 | 1.0 | 471.2 | 496.0 |
| Skip-cell plate | 600 | 2 | 0.8 | 589.0 | 620.1 |
| Shortest | | 36 | 1.2 | 21.8 | 23.0 |

With skip-cell plates (one or two cells; decided, SDL-DDR-001 item 5) the nominal range is **21.8 to 589 mm**, and 1,178 mm with a single cell, so **R3 (25 to 400 mm) is met**. The settings are discrete: choosing the best plate and ratio for every target from 25 to 400 mm, the worst error is 11.1 % (a 372 mm target falls between 331 mm and 413 mm). The spacing card should list the nearest setting for each crop.

**Chain.** The sprocket centers are 286.2 mm apart. A #35 chain needs 73.61, 75.10 and 76.61 pitches for the 12, 15 and 18 T wheel sprockets, so the chain is set to 74, 76 or 77 links (the 77-link length needs one offset link). The largest slack left over is 8.6 mm (15 T, 76 links), which a spring idler takes up by deflecting the slack strand by about 35 mm. The idler in `bom/bom.csv` has 45 mm of travel.

## 3. Metering speed and cell fill (R1)

At 3 km/h the wheel turns at 53.1 rpm. For the maize plate the seed centers sit on a 111.3 mm circle, so:

*Table 3. Plate and cell speeds at 3 km/h.*

| Ratio | Plate speed (rpm) | Cell speed (m/s) | Walking speed for 0.30 m/s (km/h) |
| --- | --- | --- | --- |
| 0.8 | 42.4 | 0.247 | 3.64 |
| 1.0 | 53.1 | 0.309 | 2.91 |
| 1.2 | 63.7 | 0.371 | 2.43 |

The design case runs at 0.309 m/s, just above the assumed 0.30 m/s limit, so **R1 is at risk**: the operator should walk at about 2.9 km/h, or 2.4 km/h with a 1.2 ratio plate. A simple kinematic indicator (a still seed must fall the cell depth while the open cell passes it) gives 0.20 m/s for the maize cell; seeds in the pool are dragged along by the plate, so real plates fill at higher speeds, but the indicator confirms that cell speed, not the drive, sets the walking speed. The maize plate passes 3.5 cells per second; the 36-cell plate at 1.2 passes 38.2 cells per second, which is demanding for the brush. Misses and multiples depend on seed shape, brush setting and cell speed and cannot be calculated on paper; they need the bench test that TRL 4 would bring.

**Meter torque.** Friction of the seed pool on the lower quarter of both plate faces (Janssen-type wall pressure under a 0.2 m seed head) is about 0.051 N·m, the brush about 0.048 N·m and the bearings and chain about 0.10 N·m, a total of **0.20 N·m**. The calculations below use 1.0 N·m, five times this estimate, to cover seed jamming at the brush.

A smaller plate would lower the cell speed in proportion to the cell circle: see the review note for this as an option.

## 4. Plates per crop (R5, R6)

*Table 4. Cell sizes, print tolerance, mass and print time for each starter plate.*

| Plate | Cell length x depth (mm) | Plate thickness (mm) | Cells (maximum) | Tolerance / smallest cell dimension | Mass (g PETG) | Print time (h) |
| --- | --- | --- | --- | --- | --- | --- |
| Maize | 14.3 x 8.7 | 6 | 4 (21) | 2.3 % | 40.0 | 1.46 |
| Sorghum | 5.7 x 4.5 | 6 | 6 (47) | 4.4 % | 41.1 | 1.50 |
| Groundnut kernel | 17.8 x 9.8 | 10 | 6 (17) | 2.1 % | 53.8 | 1.96 |
| Common bean | 15.4 x 8.7 | 8 | 9 (20) | 2.3 % | 45.8 | 1.67 |
| Spinach | 4.5 x 3.5 | 6 | 16 (56) | 5.8 % | 41.1 | 1.50 |
| Carrot, pelleted | 4.3 x 3.8 | 6 | 30 (58) | 5.3 % | 41.1 | 1.50 |
| Carrot, raw | 3.9 x 1.6 | 6 | 30 (62) | **12.8 %, too fine** | 41.2 | 1.50 |

Raw seed from 3.5 mm (spinach) to 15 mm (groundnut) fits the tolerance rule. Raw carrot seed needs a 1.6 mm deep cell, where ±0.2 mm is 12.8 % of the cell, so 1 to 2 mm seed must be sown pelleted (about 3.3 mm pellets), as decided (SDL-DDR-001 item 6). With that redefinition **R5 is met** on paper. Every starter plate prints in 2 h or less, but the 10 mm groundnut plate takes 1.96 h, so **R6 is met with almost no margin** for thick plates; the ±0.2 mm cell accuracy cannot be verified at TRL 3. The TRL 2 estimate of about 25 g and 1 h per plate was low; the model gives 40 to 54 g and 1.5 to 2.0 h.

## 5. Mass and center of mass (R11)

*Table 5. Mass by group.*

| Group | Mass (kg) | Notes |
| --- | --- | --- |
| Wheels and axles (items 1, 11) | 3.94 | 2.2 kg drive wheel, 1.2 kg press wheel, two 16 mm axles |
| Drive and metering (items 2 to 8) | 2.00 | Hopper from the model volume, 3 mm PETG walls |
| Opener and covering (items 9, 10) | 1.59 | |
| Frame and handle (items 12, 13) | 6.61 | Frame 3.63 kg (1.65 m of 25 x 25 x 1.5 tube, drops, posts, brackets); handle 2.99 kg (two 978 mm side tubes of 25 x 1.5 round tube, grip, brace, sleeves) |
| Hardware (item 15) | 0.45 | |
| **Base seeder** | **14.59** | |
| Row marker kit (item 14) | 1.00 | |
| **With marker kit** | **15.59** | |

The base seeder meets 15 kg with 0.4 kg to spare, but with the marker kit fitted it is 15.6 kg, so **R11 is not met**. The TRL 2 figure (about 14.1 kg with the marker) left out the extra tube length and brackets of the bolted frame and underestimated the handle. The center of mass of the base seeder is 383 mm behind the drive axle and 260 mm above the ground; a full hopper adds 1.73 kg of maize. The rails were sized down from 2 mm to 1.5 mm wall because the stresses are low (section 7); a lighter handle is the next place to save mass.

## 6. Push force and slip (R10, R4)

The push is found from the planar statics of the seeder on its two wheels, with the operator's force at the grip (950 mm high, 647 mm behind the press wheel) at an angle φ below the horizontal. Rolling resistance acts at ground level and the opener draft 25 mm below it. For each case the script finds the smallest horizontal push that balances the resistance with both wheels on the ground.

*Table 6. Push force (horizontal component) with a full hopper, 160 N total weight.*

| Seedbed | Along the handle (50°) | Lowest push, at angle | Angles that balance | Rolling / opener / chains (N) | Wheel loads, drive / press (N) |
| --- | --- | --- | --- | --- | --- |
| Good | 83 N | 71 N at 16° | 7 to 50° | 28 / 45 / 10 | 85 / 174 |
| Design | **136 N** | 109 N at 28° | 20 to 50° | 54 / 68 / 15 | 103 / 220 |
| Heavy, loose | no balance | **178 N at 35°** | 29 to 47° | 68 / 90 / 20 | 214 / 71 (at 35°) |

Three findings follow. First, a purely horizontal push has no balance in any case: at grip height it pitches the seeder forward and lifts the press wheel, so the TRL 2 comparison of a horizontal push against a push along the handle does not apply. Second, in the design case the push along the handle is 136 N, inside the 150 N target with a 9 % margin that rests on assumed soil values. Third, on a heavy, loose seedbed a push along the handle drives the press wheel into the soil faster than it moves the seeder (no balance), and the best push is 178 N at 35°. **R10 is at risk.** The equivalent rolling coefficients are 0.107, 0.167 and 0.239, inside the 0.2 to 0.3 range assumed at TRL 2 only for the heavy case.

**Slip.** The drive wheel must supply the meter torque through the chain: 6.7 N at the rim at a 1.0 ratio and 8.0 N at 1.2. Against 85 to 214 N of wheel load, the Brixius traction relation gives a skid of **1.2 to 1.7 %**, well inside the 8 % of R4. The larger uncertainty is the rolling radius: if the lugs sink fully, the wheel rolls on its rim and travels up to 6.7 % less per turn, which makes the spacing shorter, not longer. The two effects partly cancel. **R4 is met on paper**; the spacing card should be calibrated by counting wheel turns over a measured 10 m on the user's own seedbed.

## 7. Structure

*Table 7. Stress checks.*

| Part | Load case | Result |
| --- | --- | --- |
| Side rails, 25 x 25 x 1.5 tube | Heavy case wheel and push loads, factor 3, plus opener clamp moment | 70 MPa, factor 3.4 on yield |
| Handle side tube, 25 x 1.5 round | 100 N side load at the grip | 80 MPa, factor 2.9 |
| Press axle, 16 mm | Heavy case load, factor 3 | 19 MPa |
| #35 chain | 1.2 N·m on the 15 T plate sprocket | 52 N against about 7.8 kN minimum tensile strength (typical catalog value) |
| Plate hub D-flat | 1.2 N·m in PETG | 5.7 MPa bearing stress |

The frame and drive are lightly stressed. Durability (R15) depends on wear of the plates, brush, chain and opener, which cannot be calculated at TRL 3.

## 8. Work rate and hopper (R9, R12)

The theoretical capacity on 0.75 m rows at 3 km/h is 0.225 ha/h. With 50 m rows, 15 s turns, 90 s refills and 85 % working time the field efficiency is 65 %, so the field capacity is **0.145 ha/h (6.9 h/ha)**, which meets R9 and compares with about 56 h/ha for hoe planting (SDL-PRB-001). If the walking speed is cut to 2.9 km/h for R1, the capacity falls in proportion to about 0.14 ha/h. On 0.3 m vegetable rows the capacity is 0.058 ha/h.

The hopper cavity in the model is **2.40 L** (R12 met). It holds 1.73 kg of maize, about 5,754 seeds, enough for 1,438 m of row or 0.108 ha per fill. Maize at 0.75 x 0.25 m needs 53,333 seeds per hectare.

## 9. Depth control (R8)

The depth bracket gives 10 to 60 mm in 10 mm steps (six holes in the shank). The opener point is 182 mm behind the drive axle, so the frame, riding on its two wheels, raises the opener by 0.69 of any rise under the drive wheel and 0.31 of any rise under the press wheel. Holding ±10 mm therefore needs the wheel path to stay within about ±15 mm under the drive wheel or ±32 mm under the press wheel. A 50 mm clod under the drive wheel lifts the opener by 34 mm. **R8 is at risk** on rough, hand-tilled seedbeds; a spring-loaded opener or a depth-gauge shoe would decouple the opener from the wheels, but that is a design change for review.

## 10. Spacing uniformity (R2)

A Monte Carlo run of 20,000 cells for the maize plate, with the assumed rates in Table 1, gives a coefficient of variation of **30.7 %** for all plant-to-plant spacings, against a target of 30 % or less. The precision of the single spacings (those between 0.5 and 1.5 times the mean) is 8.9 %, with a miss index of 4.8 % and a multiple index of 3.9 %. The all-spacings CV is driven almost entirely by the misses and doubles, not by drop scatter or slip. **R2 is at risk**; it hinges on miss and double rates that only a bench test can give.

## 11. Cost (R16, R17)

All 15 BOM lines are priced. The base seeder (items 1 to 13 and 15) costs **$213.50** and the marker kit $24.00, a total of **$237.50** against the $400 budget in `project.yaml` (R16 met). The base cost exceeds the about $200 target of R17 by about 7 %, so **R17 is not met**. The main causes are the four #35 sprockets and idler for the decided ratio change ($47) and the extra brackets and bolts of the bolted frame.

## 12. Results against requirements

*Table 8. Every requirement in SDL-REQ-001 v0.3, not met items first.*

| ID | Requirement | Value (this note) | Target | Status |
| --- | --- | --- | --- | --- |
| R11 | Mass and handling | 14.6 kg base; 15.6 kg with the marker kit | 15 kg or less | **Not met** |
| R17 | Replication cost | $214 base seeder | About $200 or less | **Not met** |
| R1 | Single-seed placement | Cell speed 0.31 m/s at 3 km/h against an assumed 0.30 m/s limit | Misses and multiples 5 % or less each | **At risk** |
| R2 | Spacing uniformity | CV 31 % of all spacings; 9 % for singles (assumed rates) | CV 30 % or less | **At risk** |
| R8 | Sowing depth | 10 to 60 mm in 10 mm steps; ±10 mm only for wheel-path bumps of about ±15 mm | ±10 mm on a tilled seedbed | **At risk** |
| R10 | Push effort | 136 N along the handle (design case); 178 N at best on a heavy, loose seedbed | 150 N or less | **At risk** |
| R7 | Crop change | Side door and hand knob in the model | 2 min or less, no tools | Not verifiable at TRL 3 |
| R15 | Durability | Stresses low (section 7); wear life unknown | 5 seasons; plates 1 season | Not verifiable at TRL 3 |
| R3 | Spacing range | 22 to 589 mm nominal; every 25 to 400 mm target within 11.1 % | 25 to 400 mm | Met |
| R4 | Spacing follows travel | Skid 1.2 to 1.7 %; rolling radius uncertain by up to 6.7 % | Slip 8 % or less | Met |
| R5 | Seed size range | 3.5 to 15 mm raw seed; 1 to 2 mm seed as pellets of about 3.3 mm | 1.5 to 15 mm, seed under 2 mm pelleted | Met |
| R6 | Printable plates | 1.46 h and 40 g (maize); up to 1.96 h (groundnut); accuracy not verifiable | 2 h or less | Met, no margin for thick plates |
| R9 | Work rate | 0.145 ha/h (6.9 h/ha) | 0.1 ha/h or more | Met |
| R12 | Hopper | 2.40 L; 1,438 m of maize row per fill | 2 L or more | Met |
| R13 | Row-spacing kit | Marker reach 200 to 900 mm, set at 750 mm in the model | 200 to 900 mm, ±25 mm | Met (design review) |
| R14 | Guarding | Band guard with an outboard face plate over both sprockets and the idler | Nip points covered | Met (design review) |
| R16 | Prototype cost | $238 | $400 or less | Met |
| R18 | Local build | Bolted 25 mm square tube, 6 mm plate, #35 chain | Common sections, drill and bolts | Met (design review) |

Summary: 10 met, 4 at risk, 2 not met, 2 not verifiable at TRL 3.

## 13. Corrections to the TRL 2 figures

| Quantity | TRL 2 (SDL-PRC-001 v0.2) | TRL 3 (this note) |
| --- | --- | --- |
| Spacing range | About 22 to 393 mm; R3 not met | 21.8 to 589 mm with skip-cell plates; R3 met |
| Plate mass and print time | About 25 g, about 1 h | 40 to 54 g, 1.5 to 2.0 h |
| Hopper | About 2.1 L, about 1,250 m per fill | 2.40 L, 1,438 m per fill |
| Mass | 13.1 kg base, 14.1 kg with marker | 14.6 kg base, 15.6 kg with marker |
| Push force | About 100 N good, about 220 N heavy | 83 N good, 136 N design, 178 N heavy at best |
| Slip | 3 to 8 % | 1.2 to 1.7 % skid, plus up to 6.7 % rolling radius uncertainty |
| Work rate | About 0.14 ha/h | 0.145 ha/h |
| Parts cost | $199 base, $223 with marker | $214 base, $238 with marker |
| Meter torque | 0.5 to 1.0 N·m | 0.20 N·m estimated; 1.0 N·m used |

> **Safety:** These figures are paper estimates. The chain drive, opener point and wheel lugs remain hazards whatever the numbers say; the guard must be fitted in use and plate changes done with the wheel held still (SDL-PRC-001, Safety). Treated seed is toxic; follow the seed label.
