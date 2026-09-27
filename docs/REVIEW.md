# Review note: SeedLine

## Session 2026-09-25: /populate to a strong TRL 2 (overnight batch run)

### What was done

- `docs/01-problem.md` (SDL-PRB-001 v0.2): problem with sourced figures (farm sizes, hoe planting labor, spacing yield loss, seeder prices), users, operating environment, constraints, out of scope, prior work with links, open questions, and a co-design checklist.
- `docs/03-requirements.md` (SDL-REQ-001 v0.2): 18 measurable requirements (R1 to R18) with targets, verification and concept status, a defined design case, and a list of requirements not met or at risk.
- `docs/02-concept.md` (SDL-PRC-001 v0.2): how it works, 14 numbered components, spacing formula and plate table, metering speed, work rate, placement quality, push force, mass and cost, design choices, safety and open questions.
- `cad/src/concept_media.py`: massing model with 14 BOM-numbered parts (drive wheel, chain drive, guard, hopper, metering housing, printed plate, brush, drop tube, opener, covering chains, press wheel, frame, handle, marker arm) and a 1.75 m scale figure.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with BOM callouts, `cutaway.png` (plate inside the housing), `flow.png` (seed flow per 100 m, estimates), `model.glb` and `viewer.html`. Renderer temporary folders removed.
- `bom/bom.csv`: 15 lines with indicative USD costs, items 1 to 14 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line before "## Problem"; concept paragraph, component list and a short safety note updated to match the concept.
- `docs/pdf/`: branded PDFs of the three controlled documents.
- `project.yaml` unchanged. The pitch and problem still match the numbers found.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| In-row spacing range | about 22 to 393 mm nominal (942 mm / cells x ratio) | **R3 (25 to 400 mm) not met** at the long end |
| Maize plate, 250 mm target | 4 cells at 1:1, 236 mm nominal, about 248 mm with 5 % slip | |
| Misses and multiples, maize | about 5 % and 4 % | R1 met, no margin |
| Wheel slip | 3 to 8 % | R4 met, thin margin |
| Work rate, maize on 0.75 m rows | about 0.14 ha/h (about 7 h/ha, against about 56 h/ha by hoe) | R9 met |
| Push force | about 100 N good seedbed, about 220 N heavy seedbed | **R10 (150 N) at risk** |
| Smallest seed | cells for 1 to 2 mm seed near FDM accuracy | **R5 at risk** |
| Mass | about 13.1 kg base, 14.1 kg with marker | R11 (15 kg) met, thin margin |
| Hopper | about 2.1 L, about 1,250 m of maize row per fill | R12 met |
| Parts cost | about $199 base, about $223 with marker kit | R16 ($400) met; R17 ($200 base) met with no margin |

Requirements not met or at risk: **R3 not met**; **R5 and R10 at risk**; R1, R4, R11 and R17 met with thin or no margin; R2, R8 (depth control on rough seedbeds) and R15 unverified.

Budget: the prototype parts cost (about $223) is inside `budget_usd` ($400). No budget change is proposed.

### Proposed, awaiting Amish

1. **Metering type.** A: vertical cell plate on a transverse shaft, chain driven (modeled). B: horizontal plate with a right-angle drive. C: printed cell roller. Recommendation: A.
2. **First user group.** A: smallholder field crops (maize, beans, sorghum, groundnut on 0.75 m rows). B: market-garden vegetables. Recommendation: A first, vegetable plates second.
3. **Meaning of the row-spacing kit.** A: marker arm (modeled). B: gang bar for two or three metering units. Recommendation: A now, B as a later bed-seeding variant.
4. **Ratio change.** A: plate cells plus a 12, 15 or 18 T wheel sprocket and an idler. B: fixed 1:1 drive, plates only. Recommendation: A.
5. **R3 long spacings.** Relax R3 to 390 mm, or add skip-cell plates or a 10 T sprocket. Recommendation: skip-cell plates, keep R3.
6. **Small seed (R5).** Pelleted seed only, a 0.25 mm nozzle, or resin plates. Recommendation: specify pelleted seed for 1 to 2 mm seed at first.
7. **Wheel layout.** Front drive wheel and rear press wheel (modeled), or drive from the press wheel. Recommendation: front drive.
8. **Frame joining.** Bolted tube for builders without a welder, or welded. Recommendation: bolted as the default.
9. **Plate material.** PETG default, ASA in strong sun, PLA for trials only.
10. **Co-design partner and region.** Not proposed; needs Amish.

### Safety concerns

- Chain and sprocket nip points that move whenever the wheel turns; the guard is mandatory and plate changes must be done with the wheel held still.
- Sharp opener point and wheel lugs; transport cover needed.
- Toxic treated seed during filling and cleaning; gloves, label rules, no reuse of the hopper for food.
- Marker arm striking people at row ends; fold for turns and transport.
- Back and shoulder strain from pushing on heavy soil (R10) and lifting at row ends.

### Problems and notes

- No SwapCell pack is used or proposed; SeedLine has no battery or electronics.
- In the exploded view the singulator brush (item 7) is small and its callout sits almost on top of it. The callout is readable, but the part is hard to see at this scale.
- The legacy `cad/src/model.py` placeholder is untouched (TRL 3 work).
- Miss, multiple, slip, rolling resistance and opener draft figures are typical-value estimates, not measurements or sourced values for this plate; they are flagged as estimates in the documents.

### Suggestions (not started)

- A parametric plate generator (seed dimensions, cell count, shaft) as part of the TRL 3 model, since it carries the "plate per crop" idea.
- A spacing table per crop with a slip allowance, printed on a card that stays with the seeder.

### Recommended next step

Review this note and the media, then decide items 1 to 5. If approved, run `/advance-trl3` to check metering speed, placement quality, slip and push force by calculation, and to produce the parametric model, plate generator and drawing sheet.

## Session 2026-09-25: TRL 3

Amish reviewed the TRL 2 points and wrote on 2026-09-25: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." This session advanced SeedLine from TRL 2 to TRL 3 and stopped there. **TRL 4 is on hold by Amish's instruction.**

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (SDL-DDR-001 v0.1): items 1 to 9 recorded as "Decided by Amish, 2026-09-25: go with recommendation"; the open items listed.
- `docs/04-calcs/01-sizing.md` (SDL-CAL-001 v0.1) and `docs/04-calcs/sizing.py`: drive and spacing, chain lengths and idler, metering speed and meter torque, plates per crop, mass and center of mass, push force by planar statics with a Brixius soil model, slip, stress checks, work rate, hopper, depth sensitivity, a Monte Carlo spacing check and cost, with a results table for all 18 requirements. The script prints every quoted number and writes `docs/04-calcs/results.csv`.
- `cad/src/model.py`: parametric build123d model (wheels, sprockets from tooth counts, plate cells from seed size, hopper, handle angle, depth and marker reach as parameters) exporting `cad/step/` and `cad/stl/` for the assembly, the maize plate, the hopper and the housing.
- `cad/src/sheets.py` and `cad/drawings/SDL-DWG-001.svg`, `.pdf`, `.png`: general arrangement at Rev P1, marked "CONCEPT, NOT FOR FABRICATION" and "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps SDL-DWG-010, so the general arrangement takes SDL-DWG-001 as named in `/advance-trl3`.
- `bom/bom.csv`: all 15 lines priced with a supplier type; `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds from `model.py`; all media in `media/` refreshed and checked by eye. The cutaway is cut on the row centerline with the kit renderer so the plate cells show. Temporary `_views` folders removed.
- `docs/01-problem.md`, `docs/02-concept.md`, `docs/03-requirements.md` bumped to v0.3 with the decisions and the SDL-CAL-001 numbers; `README.md` and `project.yaml` (trl: 3, trl_target: 3, trl_evidence) updated. PDFs in `docs/pdf/`.

### Requirements summary (SDL-CAL-001 Table 8)

10 met, 4 at risk, 2 not met, 2 not verifiable at TRL 3.

| ID | Status | Value |
| --- | --- | --- |
| R11 | **Not met** | 14.6 kg base, 15.6 kg with the marker kit (target 15 kg) |
| R17 | **Not met** | $214 base seeder (target about $200) |
| R1 | At risk | Cell speed 0.31 m/s at 3 km/h against an assumed 0.30 m/s fill limit |
| R2 | At risk | Spacing CV 31 % (all spacings) with assumed 5 % misses and 4 % doubles |
| R8 | At risk | ±10 mm depth only for wheel-path bumps of about ±15 mm |
| R10 | At risk | 136 N along the handle in the design case; 178 N at best on a heavy, loose seedbed |
| R7, R15 | Not verifiable at TRL 3 | Plate change time; wear life |
| R3, R4, R5, R6, R9, R12, R13, R14, R16, R18 | Met | Spacing 22 to 589 mm; skid 1.2 to 1.7 %; raw seed 3.5 to 15 mm plus pelleted small seed; plates 1.5 to 2.0 h; 0.145 ha/h; 2.40 L hopper; $238 total |

Numbers that changed from TRL 2: the plates are 40 to 54 g and 1.5 to 2.0 h (not 25 g and 1 h), the mass is about 0.5 kg higher, the push is lower in the design case (136 N) and in the heavy case (178 N), and a purely horizontal push turns out not to balance at all. Table 13 of SDL-CAL-001 lists every correction.

### Decisions recorded (SDL-DDR-001)

Decided by Amish, 2026-09-25, go with recommendation: (1) vertical cell plate; (2) smallholder field crops first, vegetable plates second; (3) marker arm now, gang bar later; (4) 12, 15 or 18 T wheel sprocket with an idler; (5) keep R3 and add skip-cell plates; (6) pelleted seed for 1 to 2 mm seed; (7) front drive wheel; (8) bolted frame by default; (9) PETG default, ASA in strong sun, PLA for trials. The budget ($400), pitch and problem line stay unchanged, as the TRL 2 review proposed no change. The SwapCell decisions do not apply (no battery).

### Proposed, awaiting Amish (status updated 2026-09-25, see SDL-DDR-002)

1. **Co-design partner and region** (TRL 2 item 10). Still proposed, awaiting Amish. No recommendation; open under the rule that community designs pick partners per area later.
2. **Standalone plate generator.** `make_plate` in the model already does the job; publishing it as a tool for printers is Amish's call. Still proposed, awaiting Amish.
3. **R11, mass with the marker kit.** Options: a lighter handle (for example 22 x 1.2 mm tube, about 0.6 kg saved, factor on yield falls from 2.9 to about 1.8 under the 100 N side load), apply the 15 kg limit to the base seeder only, or relax it to 16 kg. Recommendation: the lighter handle, checked at the next design pass. **Decided by Amish, 2026-09-25: go with recommendation.**
4. **R17, base cost.** Options: bicycle-standard sprockets and chain, supply the 12 and 18 T sprockets as an optional kit, or relax the target to about $215. Recommendation: keep the target and move the alternate sprockets to an optional ratio kit, which would bring the base under $200 on paper. **Decided by Amish, 2026-09-25: go with recommendation.**
5. **R1, cell speed.** Options: tell operators to walk at about 2.9 km/h (2.4 km/h with 1.2 ratio plates), or reduce the plate to about 100 mm diameter. Recommendation: the walking-speed rule for now; revisit plate size only with bench data. **Decided by Amish, 2026-09-25: go with recommendation.**
6. **R8, depth on rough seedbeds.** Options: accept, or add a spring-loaded opener or depth-gauge shoe. Recommendation: accept for field crops on ploughed land and review with partner data. **Decided by Amish, 2026-09-25: go with recommendation.**

### Safety concerns

- Chain and sprocket nip points move whenever the wheel turns. The guard now has an outboard face plate; it must be fitted in use and plate changes done with the wheel held still.
- Sharp opener point and wheel lugs; transport cover needed.
- Toxic treated seed during filling and cleaning; gloves, label rules, no reuse of the hopper for food.
- Marker arm striking people at row ends; fold it for turns and transport.
- Manual handling: 15.6 kg with the marker kit, and a 178 N push on heavy, loose seedbeds. Pushing down hard along the handle on loose soil sinks the press wheel, so operators should push at a flatter angle there.

### Other notes

- No TRL 4 material exists in the repo (`build-log/` holds only its README; `electronics/` and `firmware/` are empty), and none was created.
- The TRL 2 review listed no unchecked citations, so none were re-verified in this session. The research push planter data cited in SDL-PRB-001 have not yet been compared with SDL-CAL-001.
- The Brixius rolling resistance model is used outside its calibrated range (small, rigid wheels), and the cell fill limit, miss and double rates are assumptions. These carry R1, R2 and R10.
- In the exploded view the singulator brush (item 7) is still small; its callout is readable.

### Recommended next step

Review SDL-CAL-001 and decide items 3 to 6 above. Any follow-up should stay at TRL 3: a design pass on the handle mass and the optional ratio kit, then a rerun of `sizing.py`. TRL 4 is on hold by Amish's instruction. For the record, TRL 4 would need: a bench rig with a sticky belt to measure misses, multiples and spacing CV for printed plates at several cell speeds; a built prototype weighed and pushed with a spring scale on tilled soil; a wear check of plates and brush; a test report (TST) with `environment: lab`; and build-log entries.

## Session 2026-09-25: recommendations accepted

Amish wrote on 2026-09-25: "i accept all your recommendations, go with them across all repos." Every open item with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**, recorded in `docs/decisions/0002-recommendations-accepted.md` (SDL-DDR-002 v0.1). **TRL 4 remains on hold by Amish's instruction**; `trl: 3` and `trl_target: 3` are unchanged.

### Decisions applied and what changed

| Item | Decision | Before | After |
| --- | --- | --- | --- |
| 3, R11 mass | 22 x 1.2 mm handle tube (was 25 x 1.5) | Handle 2.99 kg; 14.6 kg base, 15.6 kg with marker (not met) | Handle 2.34 kg; 13.9 kg base, 14.9 kg with marker (met, 0.06 kg margin); handle factor on yield 2.9 to 1.9 |
| 4, R17 base cost | 12 and 18 T wheel sprockets moved to an optional ratio kit (BOM line 16, $16) | Base $213.50 (not met); item 2 $47; handle $16 | Base $197.50 (met, 1.2 % margin); item 2 $33; handle $14; total with both kits $237.50 (unchanged) |
| 5, R1 cell speed | Walking-speed rule, 2.9 km/h (2.4 km/h at 1.2); plate size only with bench data | Design case 3 km/h, cell speed 0.309 m/s, 0.145 ha/h | Design case 2.9 km/h, cell speed 0.299 m/s, 0.142 ha/h; R1 still at risk |
| 6, R8 depth | Accept rigid opener for field crops on ploughed land; review with partner data | R8 at risk | R8 restated for ploughed field-crop seedbeds, met on paper |

Knock-on: design-case push 136 to 132 N; heavy seedbed 178 N at 35° to 177 N at 36°. Budget unchanged at $400 (no recommendation to change it); pitch and problem line unchanged.

Files changed: `cad/src/model.py` (handle parameters), STEP and STL re-exported; `cad/src/sheets.py` and SDL-DWG-001 Rev P1 to P2; `docs/04-calcs/sizing.py`, `results.csv` and SDL-CAL-001 v0.1 to v0.2 (new Table 14 of changes); SDL-REQ-001 v0.3 to v0.4; SDL-PRC-001 v0.3 to v0.4; `bom/bom.csv` (16 lines) and `bom/bom-notes.md`; `cad/src/concept_media.py` key figures and all media regenerated; `README.md`.

Also this session: all PDFs, drawings and media regenerated so the footers show designmolecule.com; README now has "Concept rationale", "Burning platform", "Where it could be used" and "What sparked the idea" sections. The inspiration point is Jethro Tull's 1701 seed drill with a grooved feeding cylinder.

### Requirement status (SDL-CAL-001 v0.2)

13 met, 3 at risk, 0 not met, 2 not verifiable at TRL 3 (was 10 met, 4 at risk, 2 not met, 2 not verifiable).

- **Not met:** none.
- **At risk:** R1 (cell speed 0.299 m/s against an assumed 0.30 m/s limit, no margin); R2 (spacing CV 31 %, assumed miss and double rates); R10 (132 N design case; 177 N at best on a heavy, loose seedbed).
- **Not verifiable at TRL 3:** R7 (plate change time), R15 (wear life).
- **Met, thin margin:** R11 (14.9 kg against 15 kg), R17 ($197.50 against about $200), R6 (groundnut plate 1.96 h against 2 h).
- **Met:** R3 (with the ratio kit), R4, R5, R8 (restated), R9, R12, R13, R14, R16, R18.

### Still proposed, awaiting Amish

1. Co-design partner and region (no recommendation).
2. Standalone plate generator (no recommendation).

### Cross-repo actions

None. No decision needs another repo to change.

### Decided but on hold (TRL 4)

- Revisiting the plate diameter with bench data on cell fill (item 5).
- Reviewing depth control with partner soil data (item 6).
- Bench and fatigue check of the lighter handle and its telescoping joint (item 3).

TRL 4 remains on hold by Amish's instruction; none of this was started.

### Safety

Unchanged hazards (chain nip points, sharp opener and lugs, treated seed, marker arm, manual handling). The lighter handle has a factor of 1.9 on yield under a 100 N static side load; fatigue at the telescoping joint is unverified and should be checked before any build.

## Session 2026-09-26: sources strengthened

README.md only; no controlled document changed.

| Where | Old source | New source |
| --- | --- | --- |
| Burning platform, farm-size share | Our World in Data alone | Lowder, Skoet and Raney, *World Development* 87 (2016), with Our World in Data kept alongside |
| Burning platform, hoe planting labor | CSBE jab planter study | Same study, now attributed to Baudron et al. as cited there |
| Country row: Malawi, Zambia and Zimbabwe | FAO jab planter user manual (could not be fetched) | Replaced by "Zambia and southern Africa": Haggblade and Tembo, IFPRI (2003), and the CSBE jab planter study |
| Country row: Ethiopia and Kenya | None | Replaced by "Ethiopia and Tanzania": FAO small family farms country factsheets for Ethiopia and Tanzania |
| Country row: Guatemala and Central America | None | Rewritten as "Guatemala": FAO small family farms country factsheet for Guatemala |
| What sparked the idea | ASME and Wikipedia | ASME and two Science Museum Group collection pages; Wikipedia removed. Inspiration event unchanged |

Not re-verified this session (links kept, fetch not possible here): Purdue University spacing trial (Nielsen) and University of Minnesota Extension seeder prices. Both are university primary sources. `docs/01-problem.md` still cites Paperpot Co. and 3D Printing Industry for prior-work notes; these are outside the README claims and were not changed.

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26.

### What was done

- New `cad/src/product_model.py`: an appearance model for photoreal renders. `product_parts()` returns 56 parts (35 shell, 11 internal, 8 accessory, 2 context) with colour, material class, BOM line, group and exploded-view offset. `TITLE` and `RENDER_VIEWS` define three views: `hero` (front right, about 30 deg), `exploded` (front right, about 28 deg) and `detail` (the metering unit alone, from the side opposite the chain).
- README hero image now points to `media/render-hero.png`, with a link to `media/render-exploded.png`. The render files are produced separately; they were not created in this session.

### What the appearance model adds

- Powder-coated frame and handle with rounded tube edges, plastic end caps, hex bolts and washers at the cross members, axle drop plates and handle clevis.
- Spoked drive wheel with filleted lugs; press wheel as a rubber concave tread on a light rim and hub; axle nuts.
- Toothed 15 T sprockets, a roller chain and the spring idler behind a printed amber chain guard carrying a raised "SeedLine" wordmark and two bolts.
- Hopper with rounded corners, a rolled rim, clear side windows with bezels and fill-level ticks, maize seed visible inside, and a lid with a teal tab and hinge knuckles.
- Metering housing with a parting line, a clear side door with four screws, a knurled plate knob with a teal cap, and pressed-steel flange bearings.
- Printed maize plate (teal) with a raised "MAIZE 4" label and kernels in three of its four cells; strip brush with bristle slots.
- Opener with a zinc-plated shank, depth pin and ring clip; covering chains built from links.
- Handle rubber grips with ribs and teal height-adjust collars.
- Accessories: the row-marker kit (telescoping arm, collar, disc and hub) and three more printed plates from the starter set (common bean 9 cells, sorghum 6 cells, groundnut 6 cells, seed sizes and cell counts from SDL-CAL-001) with raised crop labels.
- Context: a compact strip of tilled soil with an open furrow at the opener, a firmed press-wheel track and clods.

All main dimensions and interfaces come from `PARAMS` and the helper functions in `cad/src/model.py`; `model.py`, the BOM and the controlled documents are unchanged.

### Differences from model.py, Proposed, awaiting Amish

1. **Hopper windows.** The appearance model cuts a clear window into each side wall of the hopper so the seed level shows. Neither `model.py` nor the BOM has windows. Recommendation: keep one window on the chain side as a seed-level check; it costs one clear insert and a few grams of print.
2. **Clear housing door.** The side door is shown in clear polycarbonate so the plate and its cells show. `model.py` does not set a material; the BOM prices a printed PETG housing. Recommendation: adopt a clear door. It lets the operator see cell fill and plate identity without opening the housing.
3. **Housing in two halves.** A parting line at the row centerline shows the housing printed as two halves. Recommendation: accept as the print orientation to explore at TRL 4, not now.
4. **Drive wheel form.** The wheel is shown as a spoked steel wheel with six lightening holes and a separate hub. `model.py` has a closed disc with a hollow rim, and the BOM allows a solid-rubber or steel wheel. Recommendation: keep the BOM choice open. The render shows one credible option only.
5. **Handle details.** Rubber grips, collars at the telescoping joints (placed about 60 % of the way up the tubes) and clevis plates at the rear of the rails are shown. `model.py` does not locate the telescoping joint or the handle mounting. Recommendation: accept as illustrative; fix the joint position when the handle fatigue check (TRL 4, on hold) is done.
6. **Colours and wordmark.** Amber chain guard, teal plate and accents, graphite powder coat and a raised "SeedLine" wordmark on the guard. Recommendation: accept; naming and branding stay Amish's decision.
7. **Hardware positions.** Bolt, screw and nut positions are illustrative, not a fastener schedule. Recommendation: accept as illustrative.
8. **Row marker out of the hero.** The row-marker kit is grouped as an accessory, so the hero render shows the base seeder without it (the earlier concept hero showed it deployed at 0.75 m); it appears, at its `model.py` position plus an offset, in the exploded render. Recommendation: accept, since the kit is optional and the base seeder then fills the frame.

### TRL

This is an appearance model only: no tolerances, no fabrication detail. `trl` stays 3 and TRL 4 remains on hold.

### Recommended next step

Render the three views with `.kit/photoreal.py`, then review the hero and the detail view with Amish, including items 1 and 2 above.
