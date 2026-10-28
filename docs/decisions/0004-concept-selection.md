---
doc_id: SDL-DDR-004
title: SeedLine concept selection
project: SeedLine
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Concept selection argued for the kit 1.8 and 1.9.1 upgrade: option A (the current design) recommended over option B (punch wheel); Proposed, awaiting Amish"
---

# 0004: Concept selection

- **Date:** 2026-10-24
- **Status:** proposed. Proposed, awaiting Amish (SDL-DEC-001 D1).

## Context

Kit 1.8 asks every design to compare at least two working principles before it commits (STANDARDS section 21), and kit 1.9 asks for every option to be modelled to the repo's detail level (Amish, 2026-10-24: "Detail every option"). SeedLine was designed before kit 1.8, so its current design is option A and does not change without Amish's go. Option B was added on 2026-10-24 with a different working principle: it plants into punched holes instead of an opened furrow, and meters seed in the wheel's hub instead of from a chain-driven plate. Both options were modelled to detail level D3 in `cad/src/model.py` and `cad/src/punch_wheel.py` and checked by `python .kit/cad_check.py`; both were put through the STEM check (SDL-STM-001); both were scored against the user requirements of SDL-URS-001 (SDL-OPT-001).

## Options considered

1. **Option A, cell plate on a chain drive (the current design).** A 300 mm lugged ground wheel turns a printed vertical cell plate through a #35 chain; a runner opener cuts a furrow, each cell drops one seed into it, and drag chains and a press wheel cover and firm the row. Spacing 22 to 589 mm from plate cell count and the optional ratio kit; depth 10 to 60 mm in 10 mm steps; 14.8 kg with the marker kit; USD 224.10 base. STEM: no row fails; cell fill (S6), spacing uniformity (S7) and push endurance (S9) open.
2. **Option B, punch wheel with a hub meter.** A 480 mm wheel presses six punches into the seedbed as it rolls; a printed cell ring in the hub drops one seed down the tube of the punch about to enter the soil, and the punch's trailing jaw opens in the ground. One spacing per wheel (251 mm with six punches), depth fixed by punch length, about 12 kg, no chain, no opener draft, cells at 0.23 m/s. STEM: no row fails; seed delivery timing (OB4) and jaw opening (OB6) open; no untilled-soil advantage without ballast (OB3).

## Recommendation

Option A, 169 of 230 weighted points against option B's 131 (SDL-OPT-001 Table 2), a gap of 29 %, so the choice is not within 10 % and a pick is made. Option A meets the requirements that define the pitch, a crop change by swapping a printed plate (UR-005) and spacings for local crops (UR-003), which option B cannot meet without a new wheel for each spacing; it is bolted together with a drill and spanners (UR-016), where option B needs a rolled rim and drum and welded punches; and its depth is adjustable (UR-006). Option B is lighter, has no chain nip points and no opener draft, and meters on a smaller radius; its best idea for option A is that smaller metering radius, which lowers cell speed at the same walking pace and so the risk on PR-001. For option A that is the smaller plate Amish chose to revisit only with bench data (SDL-DDR-002 item 5), so it is recorded here, not made.

Proposed, awaiting Amish. Until he decides, `project.yaml` leaves `concept_chosen` unset and the drawing, BOM and build plan stay on option A as they were.

## Consequences

- If option A is chosen: no design change; option B stays in `cad/src/punch_wheel.py` as a recorded alternative.
- If option B is chosen: a redesign at TRL 2 to 3 (new drawing, BOM, build plan and calculations), and the plate-per-crop pitch would need restating, because a spacing change would need a new punch wheel.
