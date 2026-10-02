---
doc_id: SDL-CAL-001
title: SeedLine sizing and first-principles checks
project: SeedLine
doc_type: Calculation note
version: "0.4"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (drive and spacing, metering, plates, mass, push force, slip, structure, work rate, depth, uniformity, cost) against every requirement
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Re-run on the constructable design (SDL-DDR-003); mass from the model's parts, hopper, depth geometry, push force, cost against value-engineering targets
- version: "0.4"
  date: '2026-10-02'
  author: Amish Chadha
  change: "SDL-DDR-003 accepted and R17 cost accepted for the prototype (2026-10-02)"
---

# SeedLine sizing and first-principles checks

On paper the seeder works as a ground-driven single-row planter: the drive covers 22 to 589 mm of in-row spacing with the optional ratio kit, slip from the metering load is under 2 %, the parts are lightly stressed and the work rate is about 0.142 ha/h. Version 0.2 applies the recommendations Amish accepted on 2026-09-25 (SDL-DDR-002): a lighter 22 x 1.2 mm handle tube, the 12 and 18 T wheel sprockets moved to an optional ratio kit, a design-case walking speed of 2.9 km/h (the walking-speed rule for R1), and R8 accepted for field crops on ploughed land. Version 0.3 re-runs every figure on the constructable design of SDL-DDR-003 (2026-10-01), which adds the bearings, spacers, clips, brackets and fixings the concept left out and moves the opener forward of the metering housing; the mass is now taken part by part from the model. Eleven of the eighteen requirements are met on paper, R11 with a thin margin (14.9 kg with the marker kit against 15 kg), and two cannot be verified at TRL 3. Three are **at risk**: R1 (cell speed 0.299 m/s at 2.9 km/h against an assumed 0.30 m/s limit, no margin), R2 (spacing CV about 31 % with assumed miss, double and scatter rates) and R10 (132 N push in the design case, but 178 N at best on a heavy, loose seedbed). None is not met. The two cost requirements are value-engineering targets (STANDARDS section 18): the prototype is USD 138.50 under its USD 400 target (R16), and the base seeder is USD 19.50 over its about USD 200 target (R17).

Every number in this note is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the key dimensions, sprocket geometry, cell sizes, hopper volume and handle geometry from the parametric model `cad/src/model.py`, and the prices from `bom/bom.csv`, so the model, the drawing SDL-DWG-001, the BOM and this note agree. All values are first-principles estimates; nothing here is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design unless marked as decided.*

| Input | Value | Basis |
| --- | --- | --- |
| Architecture | Vertical cell plate, #35 chain, front drive wheel, rear press wheel, bolted frame, marker arm; 15 T wheel sprocket on the base seeder, 12 and 18 T in an optional ratio kit; 22 x 1.2 mm handle tube | Decided, SDL-DDR-001 items 1, 3, 4, 7 and 8; SDL-DDR-002 items 3 and 4 |
| Constructable design | Drive axle turning in two flange bearings with the wheel fixed to it; plate shaft held from the chain side only; opener cross member ahead of the housing; spring tensioner; parts as in `cad/src/model.py` | SDL-DDR-003 (accepted by Amish, 2026-10-02) |
| Design case | Maize at 250 mm on 0.75 m rows, 50 mm deep, 2.9 km/h (0.81 m/s), the walking-speed rule for R1 | SDL-REQ-001 v0.4; SDL-DDR-002 item 5 (was 3 km/h) |
| Drive wheel | 300 mm over the lug tips, 45 mm wide, 10 mm lugs; travel 942.5 mm per turn before slip | Model parameter |
| Typical slip for spacing tables | 5 % | Allowance; the calculated skid (section 6) is lower |
| Cell fill limit | 0.30 m/s cell speed | Assumed working limit for a gravity-filled cell plate; to be checked by bench test at TRL 4 |
| Cell size | Length 1.15 L + 0.5 mm, depth 1.05 W + 0.3 mm, plate thickness the larger of 6 mm and 1.2 T (L, W, T: seed length, width, thickness) | Rule used by `make_plate` in the model |
| Seed dimensions | Maize 12 x 8 x 5 mm, sorghum 4.5 x 4 x 3, groundnut kernel 15 x 9 x 8, common bean 13 x 8 x 6, spinach 3.5 x 3 x 2.5, pelleted carrot 3.3 mm, raw carrot 3 x 1.2 x 0.6 | Typical values; varieties differ |
| Print | ±0.2 mm on a 0.4 mm nozzle, tolerance limited to 10 % of the smallest cell dimension; 1.6 mm of skins, 1.2 mm walls, 25 % infill; 6 mm³/s average rate; PETG 1.27 g/cm³ at $25/kg | Common desktop FDM printer |
| Meter torque | 1.0 N·m at the plate shaft (design value) | First-principles estimate is 0.20 N·m (section 3); the design value is five times higher |
| Soil | Cone index 300, 200 and 100 kPa for good, design and heavy (loose, cloddy) seedbeds; opener specific resistance 20, 30 and 40 kPa; covering chains and press 10, 15 and 20 N | Assumed; no soil data from a partner region yet |
| Rolling resistance | Brixius motion resistance, MR/W = 1/Bn + 0.04, with Bn = CI b d / W / (1 + 3 b/d) for a rigid wheel | Brixius (1987), an empirical model fitted to larger tires; used here outside its calibrated range |
| Opener draft | Specific resistance x 2.5 x 18 mm opener width x depth (12 mm shank between two 3 mm boot plates) | Narrow-tool failure zone taken as 2.5 tool widths |
| Field work | 50 m rows, 15 s per turn, 90 s per refill, 85 % working time | Assumed for a small plot and one operator |
| Structure | S235 class steel, yield 235 MPa; dynamic factor 3 for drops and stones; 100 N side load at the grip | Assumed |
| Uniformity model | 5 % misses, 4 % doubles (second seed 0 to 30 mm behind), 15 mm drop scatter, slip 5 ± 1.5 % | The miss and double rates are the TRL 2 estimates; not calculable from first principles |

## 2. Drive, spacing and range (R3, R4)

The spacing is s = π D / (n i) / (1 − σ), with π D = 942.5 mm, n plate cells, ratio i = wheel teeth / 15 and travel reduction σ. The three wheel sprockets give i = 0.8, 1.0 and 1.2 (pitch diameters 36.80, 45.81 and 54.85 mm; plate sprocket 15 T). The base seeder carries the 15 T wheel sprocket (i = 1.0); the 12 and 18 T sprockets are an optional ratio kit (SDL-DDR-002 item 4).

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

With skip-cell plates (one or two cells; decided, SDL-DDR-001 item 5) and the ratio kit the nominal range is **21.8 to 589 mm**, and 1,178 mm with a single cell, so **R3 (25 to 400 mm) is met**. The settings are discrete: choosing the best plate and ratio for every target from 25 to 400 mm, the worst error is 11.1 % (a 372 mm target falls between 331 mm and 413 mm). The spacing card should list the nearest setting for each crop. The base seeder alone (15 T only) covers 26.2 to 471 mm nominal, but its settings are coarser at long spacings: the worst error is 17.3 % (a 400 mm target falls between 331 mm and 496 mm). The ratio kit is needed for the 25 mm pelleted-seed plate at 1.2 and for close settings above about 300 mm.

**Chain.** The sprocket centers are 286.2 mm apart. A #35 chain needs 73.61, 75.10 and 76.61 pitches for the 12, 15 and 18 T wheel sprockets, so the chain is set to 74, 76 or 77 links (the 77-link length needs one offset link). The largest slack left over is 8.6 mm (15 T, 76 links), which the spring tensioner takes up by deflecting the slack (lower) strand by about 35 mm. The tensioner in `bom/bom.csv` has about 45 mm of take-up, and the chain guard encloses its full travel.

## 3. Metering speed and cell fill (R1)

Amish accepted the walking-speed rule on 2026-09-25 (SDL-DDR-002 item 5): the operator walks at about 2.9 km/h with the 0.8 and 1.0 ratios and about 2.4 km/h with the 1.2 ratio. The design case now uses 2.9 km/h (it was 3 km/h in v0.1). At 2.9 km/h the wheel turns at 51.3 rpm. For the maize plate the seed centers sit on a 111.3 mm circle, so:

*Table 3. Plate and cell speeds at 2.9 km/h.*

| Ratio | Plate speed (rpm) | Cell speed (m/s) | Walking speed for 0.30 m/s (km/h) |
| --- | --- | --- | --- |
| 0.8 | 41.0 | 0.239 | 3.64 |
| 1.0 | 51.3 | 0.299 | 2.91 |
| 1.2 | 61.5 | 0.359 | 2.43 |

The design case runs at 0.299 m/s, at the assumed 0.30 m/s limit with no margin, and the limit itself is an assumption, so **R1 stays at risk**. A simple kinematic indicator (a still seed must fall the cell depth while the open cell passes it) gives 0.20 m/s for the maize cell; seeds in the pool are dragged along by the plate, so real plates fill at higher speeds, but the indicator confirms that cell speed, not the drive, sets the walking speed. The maize plate passes 3.4 cells per second; the 36-cell plate at 1.2 passes 36.9 cells per second at 2.9 km/h, which is demanding for the brush (the rule of 2.4 km/h at 1.2 lowers that further). Misses and multiples depend on seed shape, brush setting and cell speed and cannot be calculated on paper; they need the bench test that TRL 4 would bring.

**Meter torque.** Friction of the seed pool on the lower quarter of both plate faces (Janssen-type wall pressure under a 0.2 m seed head) is about 0.051 N·m, the brush about 0.048 N·m and the bearings and chain about 0.10 N·m, a total of **0.20 N·m**. The calculations below use 1.0 N·m, five times this estimate, to cover seed jamming at the brush.

A smaller plate would lower the cell speed in proportion to the cell circle. Under SDL-DDR-002 item 5 the plate size is revisited only with bench data, which is TRL 4 work and on hold.

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

From v0.3 the steel and printed parts are weighed from the volumes of the constructable model (steel 7.85 g/cm³, PETG printed solid at 1.27 g/cm³, polycarbonate door 1.2 g/cm³); bought parts keep catalogue-class estimates.

*Table 5. Mass by group.*

| Group | Mass (kg) | Notes |
| --- | --- | --- |
| Wheels and axles (items 1, 11) | 4.29 | Drive wheel body 1.70 kg (bought estimate) and 18 lugs 0.42 kg (model); drive axle, two 16 mm flange bearings (0.12 kg each) and spacers; press wheel 1.20 kg with its axle bolt, nuts and spacers |
| Drive and metering (items 2 to 8) | 2.35 | Hubbed sprockets, chain and spring tensioner 0.75 kg; guard, hopper with lid and housing from the model volumes; shaft, two flange bearings, collar, plate, brush, drop tube |
| Opener and covering (items 9, 10) | 1.20 | Shank and boot plates from the model; covering chains and bracket |
| Frame and handle (items 12, 13) | 5.61 | Frame 3.44 kg (two 700 mm rails, two cross members, four clips, four 4 mm drop plates, bearing plate, four uprights); handle 2.17 kg (two 973 mm side tubes of 22 x 1.2 round tube, grip, brace, sleeves, rubber grips) |
| Hardware (item 15) | 0.58 | About 50 M6 and M8 bolt sets, 36 M5 lug screws, inserts, paint |
| **Base seeder** | **14.03** | |
| Row marker kit (item 14) | 0.79 | Mount, telescoping arm and 2 mm disc from the model |
| **With marker kit** | **14.81** | |

Making the design constructable (SDL-DDR-003) added about 0.9 kg of bearings, spacers, clips, brackets, uprights and fixings and took off about 0.8 kg: the opener clamp plate and the rear cross member went, the drop plates are 4 mm instead of 6 mm, the marker kit, measured from the model, is 0.21 kg lighter than the 1.0 kg estimate, and the handle sleeves are now sized. The seeder is 14.0 kg base and 14.8 kg with the marker kit. **R11 is met, with 0.19 kg of margin** with the kit fitted (0.06 kg in v0.2). In v0.1 the handle was 25 x 1.5 mm round tube, which put the seeder over 15 kg; the 22 x 1.2 mm tube Amish accepted on 2026-09-25 (SDL-DDR-002 item 3) saves 0.64 kg. The side tube's factor on yield under the 100 N side load is 1.9 (section 7). The center of mass of the base seeder is 349 mm behind the drive axle and 245 mm above the ground; a full hopper adds 1.74 kg of maize.

## 6. Push force and slip (R10, R4)

The push is found from the planar statics of the seeder on its two wheels, with the operator's force at the grip (950 mm high, 647 mm behind the press wheel) at an angle φ below the horizontal. Rolling resistance acts at ground level and the opener draft 25 mm below it. For each case the script finds the smallest horizontal push that balances the resistance with both wheels on the ground.

*Table 6. Push force (horizontal component) with a full hopper, 155 N total weight.*

| Seedbed | Along the handle (50°) | Lowest push, at angle | Angles that balance | Rolling / opener / chains (N) | Wheel loads, drive / press (N) |
| --- | --- | --- | --- | --- | --- |
| Good | 80 N | 71 N at 21° | 11 to 50° | 25 / 45 / 10 | 91 / 160 |
| Design | **132 N** | 109 N at 31° | 22 to 50° | 49 / 68 / 15 | 108 / 204 |
| Heavy, loose | no balance | **178 N at 37°** | 30 to 48° | 68 / 90 / 20 | 210 / 79 (at 37°) |

Three findings follow. First, a purely horizontal push has no balance in any case: at grip height it pitches the seeder forward and lifts the press wheel, so the TRL 2 comparison of a horizontal push against a push along the handle does not apply. Second, in the design case the push along the handle is 132 N, inside the 150 N target with a 12 % margin that rests on assumed soil values; the constructable design moves the center of mass about 9 mm forward and leaves this figure unchanged. Third, on a heavy, loose seedbed a push along the handle drives the press wheel into the soil faster than it moves the seeder (no balance), and the best push is 178 N at 37°. **R10 is at risk.** The equivalent rolling coefficients are 0.102, 0.158 and 0.235, inside the 0.2 to 0.3 range assumed at TRL 2 only for the heavy case.

**Slip.** The drive wheel must supply the meter torque through the chain: 6.7 N at the rim at a 1.0 ratio and 8.0 N at 1.2. Against 91 to 210 N of wheel load, the Brixius traction relation gives a skid of **1.2 to 1.7 %**, well inside the 8 % of R4. The larger uncertainty is the rolling radius: if the lugs sink fully, the wheel rolls on its rim and travels up to 6.7 % less per turn, which makes the spacing shorter, not longer. The two effects partly cancel. **R4 is met on paper**; the spacing card should be calibrated by counting wheel turns over a measured 10 m on the user's own seedbed.

## 7. Structure

*Table 7. Stress checks.*

| Part | Load case | Result |
| --- | --- | --- |
| Side rails, 25 x 25 x 1.5 tube | Heavy case wheel and push loads, factor 3, plus opener moment | 71 MPa, factor 3.3 on yield |
| Handle side tube, 22 x 1.2 round (SDL-DDR-002) | 100 N side load at the grip | 126 MPa, factor 1.9 (was 80 MPa, factor 2.9, with 25 x 1.5 tube) |
| Press axle, 16 mm | Heavy case load, factor 3 | 21 MPa |
| #35 chain | 1.2 N·m on the 15 T plate sprocket | 52 N against about 7.8 kN minimum tensile strength (typical catalog value) |
| Plate hub D-flat | 1.2 N·m in PETG | 5.7 MPa bearing stress |

The frame and drive are lightly stressed. The lighter handle is the most highly stressed steel part, still with a factor of 1.9 on yield under a static side load; fatigue of the telescoping joint is a TRL 4 question. Durability (R15) depends on wear of the plates, brush, chain and opener, which cannot be calculated at TRL 3.

## 8. Work rate and hopper (R9, R12)

The theoretical capacity on 0.75 m rows at the 2.9 km/h design walking speed is 0.217 ha/h. With 50 m rows, 15 s turns, 90 s refills and 85 % working time the field efficiency is 65 %, so the field capacity is **0.142 ha/h (7.1 h/ha)**, which meets R9 and compares with about 56 h/ha for hoe planting (SDL-PRB-001). The walking-speed rule costs about 0.003 ha/h against the v0.1 figure at 3 km/h (0.145 ha/h). On 0.3 m vegetable rows the capacity is 0.057 ha/h.

The hopper cavity in the model is **2.42 L** (R12 met), including the 12 mm straight neck that now drops into the housing collar. It holds 1.74 kg of maize, about 5,805 seeds, enough for 1,451 m of row or 0.109 ha per fill. Maize at 0.75 x 0.25 m needs 53,333 seeds per hectare.

## 9. Depth control (R8)

The opener shank is clamped to the opener cross member by two bolts into two of eight tapped holes at 10 mm pitch, which gives 10 to 60 mm in 10 mm steps. The front of the shank, the opener's leading edge, is 181 mm behind the drive axle (182 mm in the concept), so the frame, riding on its two wheels, raises the opener by 0.69 of any rise under the drive wheel and 0.31 of any rise under the press wheel. Holding ±10 mm therefore needs the wheel path to stay within about ±15 mm under the drive wheel or ±32 mm under the press wheel. A 50 mm clod under the drive wheel lifts the opener by 34 mm. Amish accepted the recommendation on 2026-09-25 (SDL-DDR-002 item 6): the rigid opener is accepted for field crops on ploughed land, and R8 is restated for a ploughed field-crop seedbed, where the ±15 mm wheel-path condition is expected to hold. On that basis **R8 is met on paper**; on rough, hand-tilled seedbeds depth will vary more, and a spring-loaded opener or depth-gauge shoe is to be reviewed with partner data.

## 10. Spacing uniformity (R2)

A Monte Carlo run of 20,000 cells for the maize plate, with the assumed rates in Table 1, gives a coefficient of variation of **30.7 %** for all plant-to-plant spacings, against a target of 30 % or less. The precision of the single spacings (those between 0.5 and 1.5 times the mean) is 8.9 %, with a miss index of 4.8 % and a multiple index of 3.9 %. The all-spacings CV is driven almost entirely by the misses and doubles, not by drop scatter or slip. **R2 is at risk**; it hinges on miss and double rates that only a bench test can give.

## 11. Cost (R16, R17)

All 16 BOM lines are priced; costs are estimates, not quotes. Both cost requirements are value-engineering targets, not limits (STANDARDS section 18; Amish, 2026-10-01).

- **R16, prototype.** Value-engineering target: USD 400 (`budget_usd`). Estimated cost of the constructable design: USD 261.50 for the base seeder with the marker kit (USD 24.00) and the optional ratio kit (USD 18.00), **USD 138.50 under the target**.
- **R17, base seeder.** Value-engineering target: about USD 200. Estimated cost of the constructable design: USD 219.50 for items 1 to 13 and 15, **USD 19.50 over the target**. The concept was USD 197.50; the parts that make it buildable add USD 22.00: the drive axle's two flange bearings and the lug strip (line 1, +6.00), hubbed sprockets and a bought spring tensioner (line 2, +5.00), the clear door, collar and knob (line 5, +4.00), more fasteners and the 36 lug screws (line 15, +3.00), the frame's clips, uprights and opener cross member (line 12, +2.00) and smaller items, less the opener clamp plate (line 9, −2.00). The main cost drivers and the savings worth trying are listed in the design decisions register (SDL-DEC-001, Value engineering).

## 12. Results against requirements

*Table 8. Every requirement in SDL-REQ-001 v0.5, at-risk items first (none is not met).*

| ID | Requirement | Value (this note) | Target | Status |
| --- | --- | --- | --- | --- |
| R1 | Single-seed placement | Cell speed 0.299 m/s at the 2.9 km/h walking-speed rule against an assumed 0.30 m/s limit, no margin | Misses and multiples 5 % or less each | **At risk** |
| R2 | Spacing uniformity | CV 31 % of all spacings; 9 % for singles (assumed rates) | CV 30 % or less | **At risk** |
| R10 | Push effort | 132 N along the handle (design case); 178 N at best on a heavy, loose seedbed | 150 N or less | **At risk** |
| R7 | Crop change | Side door and hand knob in the model | 2 min or less, no tools | Not verifiable at TRL 3 |
| R15 | Durability | Stresses low (section 7); wear life unknown | 5 seasons; plates 1 season | Not verifiable at TRL 3 |
| R11 | Mass and handling | 14.0 kg base; 14.8 kg with the marker kit | 15 kg or less | Met, 0.19 kg margin |
| R17 | Replication cost | USD 219.50 base seeder | About USD 200 (value-engineering target) | USD 19.50 over the target; accepted for the prototype on 2026-10-02 |
| R8 | Sowing depth | 10 to 60 mm in 10 mm steps; ±10 mm for wheel-path bumps within about ±15 mm | ±10 mm on a ploughed field-crop seedbed (restated) | Met on paper |
| R3 | Spacing range | 22 to 589 mm nominal with the ratio kit, every 25 to 400 mm target within 11.1 %; base seeder 26 to 471 mm, within 17.3 % | 25 to 400 mm | Met (with the ratio kit) |
| R4 | Spacing follows travel | Skid 1.2 to 1.7 %; rolling radius uncertain by up to 6.7 % | Slip 8 % or less | Met |
| R5 | Seed size range | 3.5 to 15 mm raw seed; 1 to 2 mm seed as pellets of about 3.3 mm | 1.5 to 15 mm, seed under 2 mm pelleted | Met |
| R6 | Printable plates | 1.46 h and 40 g (maize); up to 1.96 h (groundnut); accuracy not verifiable | 2 h or less | Met, no margin for thick plates |
| R9 | Work rate | 0.142 ha/h (7.1 h/ha) | 0.1 ha/h or more | Met |
| R12 | Hopper | 2.42 L; 1,451 m of maize row per fill | 2 L or more | Met |
| R13 | Row-spacing kit | Marker reach 200 to 900 mm, set at 750 mm in the model | 200 to 900 mm, ±25 mm | Met (design review) |
| R14 | Guarding | Printed shroud with an outboard face plate over both sprockets, the chain and the tensioner's full travel | Nip points covered | Met (design review) |
| R16 | Prototype cost | USD 261.50 | USD 400 value-engineering target | USD 138.50 under the target |
| R18 | Local build | Bolted 25 mm square tube, 4 mm plate, angle and flat bar, #35 chain; saw, drill, tap and bolts | Common sections, drill and bolts | Met (design review) |

Summary: 11 met, 3 at risk, 0 not met, 2 not verifiable at TRL 3, and the two cost requirements reported against their value-engineering targets (R16 under, R17 over). (v0.2: 13 met, counting both cost requirements as met; v0.1: 10 met, 4 at risk, 2 not met, 2 not verifiable.)

## 13. Corrections to the TRL 2 figures

| Quantity | TRL 2 (SDL-PRC-001 v0.2) | TRL 3 (v0.1 of this note; see Table 14 for v0.2) |
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

*Table 14. Changes in v0.2 from the recommendations accepted by Amish (SDL-DDR-002).*

| Quantity | v0.1 | v0.2 |
| --- | --- | --- |
| Handle tube | 25 x 1.5 mm, 2.99 kg handle | 22 x 1.2 mm, 2.34 kg handle |
| Mass | 14.6 kg base, 15.6 kg with marker (R11 not met) | 13.9 kg base, 14.9 kg with marker (R11 met) |
| Base parts cost | $213.50 (R17 not met) | $197.50 (R17 met); ratio kit $16.00 optional |
| Design walking speed | 3 km/h, cell speed 0.309 m/s | 2.9 km/h, cell speed 0.299 m/s |
| Work rate | 0.145 ha/h | 0.142 ha/h |
| Push, design case | 136 N along the handle | 132 N along the handle |
| Push, heavy seedbed | 178 N at 35° | 177 N at 36° |
| Handle side tube | Factor 2.9 on yield | Factor 1.9 on yield |
| R8 | At risk | Restated for ploughed field-crop seedbeds; met on paper |

*Table 15. Changes in v0.3 from the constructable design (SDL-DDR-003).*

| Quantity | v0.2 | v0.3 |
| --- | --- | --- |
| Mass | 13.9 kg base, 14.9 kg with marker (0.06 kg margin) | 14.0 kg base, 14.8 kg with marker (0.19 kg margin), weighed from the model |
| Hopper | 2.40 L, 1,438 m per fill | 2.42 L (straight neck added), 1,451 m per fill |
| Opener leading edge | 182 mm behind the drive axle | 181 mm; depth figures unchanged |
| Push, design case | 132 N along the handle | 132 N along the handle |
| Push, heavy seedbed | 177 N at 36° | 178 N at 37° |
| Base parts cost | USD 197.50 (reported as met) | USD 219.50, USD 19.50 over the about USD 200 value-engineering target |
| Prototype parts cost | USD 237.50 | USD 261.50, USD 138.50 under the USD 400 value-engineering target |
| Slack take-up | Spring idler | Bought spring tensioner, 45 mm take-up, inside the guard |

> **Safety:** These figures are paper estimates. The chain drive, opener point and wheel lugs remain hazards whatever the numbers say; the guard must be fitted in use and plate changes done with the wheel held still (SDL-PRC-001, Safety). Treated seed is toxic; follow the seed label.
