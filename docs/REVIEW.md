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
