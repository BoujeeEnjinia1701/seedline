---
doc_id: SDL-PRC-001
title: SeedLine design precis
project: SeedLine
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, metering numbers, work rate, push force, cost, safety, media)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record decisions (SDL-DDR-001); numbers replaced by SDL-CAL-001 results; parametric model, SDL-DWG-001 and refreshed media
---

# SeedLine design precis

SeedLine is a single-row push seeder. A 300 mm lugged ground wheel drives a vertical, 3D-printed seed plate through a #35 roller chain, so seeds are placed at a spacing set by distance travelled, not by walking speed. A runner opener cuts the furrow, chains cover the seed and a concave press wheel firms the row. Crop and spacing change by swapping a printed plate (1 to 36 cells) and, if needed, one of three wheel sprockets. An optional telescoping marker arm scratches the line of the next row. The TRL 3 calculations (SDL-CAL-001) give an in-row spacing range of 22 to 589 mm, a work rate of 0.145 ha/h for maize on 0.75 m rows (6.9 h/ha against about 56 h/ha by hoe), a push of about 136 N in the design case, a mass of 14.6 kg (15.6 kg with the marker kit) and a parts cost of about $214 for the base seeder and $238 with the marker kit. Mass with the kit (R11) and the base cost (R17) miss their targets; placement quality (R1, R2), depth control (R8) and push effort (R10) are at risk.

![Hero render](../media/hero.png)

*Figure 1. SeedLine from the TRL 3 parametric model (`cad/src/model.py`), with the row marker deployed at 0.75 m, the opener at 50 mm working depth and a 1.75 m person for scale. Direction of travel is toward the lower right.*

## How it works

1. **Load.** The operator pours up to about 2 L of seed into the hopper (item 4), which feeds the metering housing (item 5) below it.
2. **Drive.** As the seeder is pushed, the lugged ground wheel (item 1) turns. A 15-tooth #35 sprocket on its axle drives a 15-tooth sprocket on the plate shaft through a roller chain (item 2). Fitting a 12 T or 18 T sprocket on the wheel changes the plate speed by 0.8 or 1.2 times; the chain is set to 74, 76 or 77 links and a spring idler takes up the remaining slack.
3. **Meter.** The printed seed plate (item 6) turns upright inside the housing. Cells on its rim pass through the seed pool at the bottom of the hopper, each picking up a seed. A brush (item 7) at the top of the plate sweeps off extra seeds, so each cell carries one.
4. **Drop.** As a cell passes the outlet on the forward side of the housing, its seed falls through the drop tube (item 8) into the furrow cut by the runner opener (item 9), just behind the opener's point.
5. **Cover and firm.** Two drag chains (item 10) pull soil over the seed and the concave press wheel (item 11) firms it, which improves seed-soil contact.
6. **Mark the next row.** The marker arm (item 14), clipped to the front cross member, drags a small disc at the set row spacing. On the return pass the operator follows that line with the ground wheel.

The frame (item 12) is two 25 x 25 x 1.5 mm square steel rails with bolted cross members, corner plates and axle drop plates; the handle (item 13) telescopes for operator height. The general arrangement is drawing SDL-DWG-001.

![Seed flow](../media/flow.png)

*Figure 2. Seed flow over 100 m of row for the maize plate at 250 mm spacing. All values are estimates (the miss and double rates are assumptions carried into SDL-CAL-001); doubles add seeds, so more seeds are dropped than cells are filled.*

## Main components

Numbers match the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Ground drive wheel | 300 mm diameter, 45 mm wide, 18 lugs, on a 16 mm axle with bearings | Lugs limit slip; a narrow wheel runs in the tilled row |
| 2 | Chain drive | #35 roller chain, 15 T plate sprocket; 12, 15 or 18 T wheel sprocket; spring idler | 74, 76 or 77 links at 286 mm centers; idler deflects up to 35 mm |
| 3 | Chain guard | Band around the chain loop with an outboard face plate, PETG or sheet steel | Covers the nip points from above, below and outside |
| 4 | Seed hopper | 2.4 L, 170 x 120 mm top on a funnel to a 60 x 30 mm throat, printed or cut from HDPE, lid | 1.73 kg of maize, 1,438 m of row per fill |
| 5 | Metering housing, shaft and bearings | Printed housing with seed outlet and side door; 12 mm shaft in two flange bearings | Side door and hand knob give tool-free plate changes |
| 6 | Printed seed plate | 120 mm diameter, 6 to 10 mm thick, 1 to 36 rim cells sized to the seed (`make_plate` in the model) | 40 to 54 g of PETG, 1.5 to 2.0 h to print; one plate per crop and spacing |
| 7 | Singulator brush | Nylon strip brush on a printed holder, adjustable gap | Wear part |
| 8 | Seed drop tube | 20 mm tube, housing outlet to the opener | Short drop limits bounce |
| 9 | Furrow opener and depth bracket | Runner shoe on a steel shank, clamped in a slotted bracket (10 to 60 mm depth) | Depth set against the wheels |
| 10 | Covering chains | Two short lengths of light chain on a bracket | Low cost, self-cleaning |
| 11 | Press wheel | 200 mm diameter, 70 mm wide concave rubber tread | Firms the row; carries part of the load |
| 12 | Steel frame | 25 x 25 x 1.5 mm square tube rails and cross members, 6 mm axle drop plates, 20 mm hopper posts, corner plates | Bolted (decided); welding optional |
| 13 | Handle | Two 25 x 1.5 mm round tubes with a cross grip and brace, telescoping for 850 to 1,050 mm grip height | Model grip at 950 mm, 50° to the ground; 3.0 kg |
| 14 | Row marker arm (row-spacing kit) | Telescoping arm and 140 mm marker disc, 200 to 900 mm reach, folds up for transport | Optional kit |

![Exploded view](../media/exploded.png)

*Figure 3. Exploded view with numbered callouts matching the BOM.*

![Cutaway](../media/cutaway.png)

*Figure 4. Section on the row centerline, seen from the chain side with that half removed. The four-cell maize plate sits upright in the housing under the hopper funnel, with the brush at the top and the outlet feeding the drop tube into the opener. The drive wheel is on the right, the press wheel on the left.*

## Key numbers (SDL-CAL-001)

The TRL 2 estimates in version 0.2 are replaced by the calculations in SDL-CAL-001 v0.1, which reads its geometry from the parametric model. The main results:

*Table 1. Key numbers from SDL-CAL-001.*

| Quantity | Value | Requirement |
| --- | --- | --- |
| Spacing | s = 942.5 mm / (cells x ratio), longer by 1 / (1 − slip); 22 to 589 mm nominal with 1 to 36 cells and ratios 0.8, 1.0, 1.2 | R3 met |
| Maize plate | 4 cells at 1.0: 236 mm nominal, 248 mm with 5 % slip | Design case |
| Cell speed, design case | 0.31 m/s at 3 km/h; 0.30 m/s (assumed fill limit) at 2.9 km/h | R1 at risk |
| Skid from meter torque | 1.2 to 1.7 %; rolling radius uncertain by up to 6.7 % | R4 met |
| Spacing CV, maize | 31 % of all spacings, 9 % of single spacings (assumed miss and double rates) | R2 at risk |
| Plates | 40 to 54 g PETG, 1.5 to 2.0 h each; raw seed 3.5 to 15 mm, smaller seed pelleted | R5 met, R6 met with no margin |
| Push force (horizontal part) | 83 N good, 136 N design case along the handle; 178 N at best on a heavy, loose seedbed | R10 at risk |
| Mass | 14.6 kg base, 15.6 kg with the marker kit | R11 not met |
| Work rate | 0.145 ha/h (6.9 h/ha) on 0.75 m rows | R9 met |
| Hopper | 2.40 L, 1,438 m of maize row per fill | R12 met |
| Depth | ±10 mm needs wheel-path bumps within about ±15 mm under the drive wheel | R8 at risk |
| Parts cost | $214 base, $238 with the marker kit | R16 met, R17 not met |

A purely horizontal push at the grip pitches the seeder forward and lifts the press wheel, so the operator pushes down along the handle; on a heavy, loose seedbed a push along the full 50° handle angle sinks the press wheel, and a flatter push of about 35° works best. The base seeder costs a little more than an Earthway 1001-B with six plates (about $187) and well under a Jang JP-1 without rollers (about $499) ([UMN Extension](https://blog-fruit-vegetable-ipm.extension.umn.edu/2024/11/lower-cost-equipment-for-seeding-and.html)).

With the Purdue figure of about 2.2 to 2.5 bu/acre lost per inch of spacing standard deviation ([Nielsen, Purdue University](https://www.agry.purdue.edu/ext/corn/research/psv/update2004.html)), each 25 mm of spacing variation avoided is worth about 140 to 160 kg/ha of maize at those yield levels; smallholder yields are lower, so the absolute gain will be smaller.

## Key design choices

Decided by Amish on 2026-09-25 (SDL-DDR-001: go with the TRL 2 recommendations):

- **Metering type:** a vertical cell plate on a transverse shaft, driven directly by the chain. The plate is a flat print with no supports.
- **First user group:** smallholder field crops (maize, beans, sorghum, groundnut on 0.75 m rows) first; vegetable plates as a second plate set.
- **Row-spacing kit:** a telescoping marker arm. A gang bar for two or three metering units is recorded as a later variant for vegetable beds.
- **Ratio change:** plate cell count plus a 12, 15 or 18 T wheel sprocket, with a spring idler.
- **Long spacings (R3):** keep the 400 mm target and add skip-cell plates with one or two cells.
- **Small seed (R5):** pelleted seed for 1 to 2 mm seed at first.
- **Wheel layout:** front drive wheel, rear press wheel.
- **Frame joining:** bolted square tube by default; welding stays an option for workshops that weld.
- **Plate material:** PETG by default, ASA where plates sit in strong sun, PLA for trials only.

Still proposed, awaiting Amish:

- **Standalone plate generator.** The model's `make_plate` function already makes a plate from seed dimensions and cell count. Whether to publish it as a separate tool for printers is open.
- **Partner and region for co-design.** Left open under the portfolio rule that community designs pick co-design partners per area later.

## Safety

> **Safety:** SeedLine has an exposed roller chain driven by the wheel, a pointed steel opener and lugs, and is often used with chemically treated seed. Treat each as a hazard during use, cleaning, transport and plate changes.

- **Chain and sprocket nip points.** The chain moves whenever the wheel turns, including when the seeder is pushed or carried with the wheel spinning. Fingers, loose clothing and plant material can be drawn into the sprockets. The chain guard (item 3) must be fitted whenever the seeder is used, and plate changes and cleaning must be done with the wheel lifted clear and held still. Children should not push the seeder.
- **Sharp and pointed parts.** The opener point and the wheel lugs can cut shins and feet. Deburr all cut edges, round the lug tips and fit a cover over the opener for transport and storage.
- **Treated seed.** Seed dressed with fungicides or insecticides is toxic. Follow the seed label: wear gloves, do not eat, drink or smoke while filling, keep treated seed away from children and animals, and clean the hopper and housing outdoors. Never use the hopper for food or feed.
- **Row marker arm.** The deployed arm sticks out up to about 0.9 m to the side and can strike people or catch on posts at row ends. Fold it for turns near people and for transport.
- **Manual handling.** Lifting and turning at row ends and pushing on heavy soil can strain the back and shoulders (R10 and R11). Handle height must be set for the operator, and the seeder should be carried by two people or wheeled over rough ground.
- **Printed parts.** Plates, hopper and housing are plastic and can crack in cold or sun; a cracked plate can jam the drive. Inspect plates before each season and replace any that are cracked or worn.

## Open questions

TRL 4 is on hold by Amish's instruction. These questions remain for review:

- How to recover R11 (15.6 kg with the marker kit): a lighter handle, a lighter drive wheel, or applying the 15 kg limit to the base seeder only.
- How to recover R17 ($214 base): cheaper bicycle-standard sprockets and chain, fewer alternate sprockets, or relaxing the target.
- Whether to reduce the plate diameter to lower cell speed (R1), at the cost of fewer cells for small seed.
- Whether a spring-loaded opener or a depth-gauge shoe is needed on rough seedbeds (R8).
- Soil data (cone index, opener draft) from the partner region to firm up the push force (R10).
- The miss and double rates of printed plates, which only a bench test can give (R1, R2).
- The co-design partner, region and first crops and spacings to support.

Concept media: [blueprint sheet](../media/concept-blueprint.pdf), [interactive 3D model](../media/viewer.html). General arrangement: [SDL-DWG-001](../cad/drawings/SDL-DWG-001.pdf). Calculations: [SDL-CAL-001](04-calcs/01-sizing.md).
