---
doc_id: SDL-DDR-001
title: SeedLine TRL 2 review decisions
project: SeedLine
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's 2026-09-25 decisions on the TRL 2 review and the items that remain open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** accepted (items 1 to 9); item 10 and the plate generator question remain proposed, awaiting Amish

## Context

The TRL 2 review note (`docs/REVIEW.md`, session 2026-09-25, /populate) listed ten items as "Proposed, awaiting Amish". On 2026-09-25 Amish reviewed the review points for every portfolio repo and wrote: "proceed with all of your recommendations across all batches. Make sure we don't proceed to TRL 4 on any of them." The same instruction set a portfolio rule that community designs pick co-design partners per area later. The cross-cutting SwapCell decisions do not apply: SeedLine has no battery or electronics.

This record lists what that instruction decides and what it leaves open because there was no recommendation to accept. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 section) and SDL-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Decision | Where it now lives |
| --- | --- | --- | --- |
| 1 | Metering type | Decided by Amish, 2026-09-25: go with recommendation. Vertical cell plate on a transverse shaft, driven directly by the #35 chain (option A) | SDL-PRC-001 v0.3, `cad/src/model.py` |
| 2 | First user group | Decided by Amish, 2026-09-25: go with recommendation. Smallholder field crops first (maize, beans, sorghum, groundnut on 0.75 m rows), with vegetable plates as a second plate set | SDL-PRB-001 v0.3, SDL-REQ-001 v0.3 design case |
| 3 | Meaning of the row-spacing kit | Decided by Amish, 2026-09-25: go with recommendation. A telescoping marker arm now; a gang bar for two or three metering units is recorded as a later bed-seeding variant | SDL-PRC-001 v0.3, SDL-REQ-001 R13, `bom/bom.csv` line 14 |
| 4 | Ratio change | Decided by Amish, 2026-09-25: go with recommendation. Plate cell count plus a 12, 15 or 18 T wheel sprocket, with a spring idler (option A) | SDL-CAL-001 section 2, `bom/bom.csv` line 2 |
| 5 | R3 long spacings | Decided by Amish, 2026-09-25: go with recommendation. Keep R3 (25 to 400 mm) and add skip-cell plates (plates with one or two cells) | SDL-REQ-001 R3, SDL-CAL-001 section 2 |
| 6 | Small seed (R5) | Decided by Amish, 2026-09-25: go with recommendation. Specify pelleted seed for 1 to 2 mm seed at first | SDL-REQ-001 R5 (redefined), SDL-CAL-001 section 4 |
| 7 | Wheel layout | Decided by Amish, 2026-09-25: go with recommendation. Front drive wheel, rear press wheel | SDL-PRC-001 v0.3, `cad/src/model.py` |
| 8 | Frame joining | Decided by Amish, 2026-09-25: go with recommendation. Bolted square tube as the default; welding stays an option for workshops that weld | SDL-REQ-001 R18, `bom/bom.csv` line 12, SDL-DWG-001 |
| 9 | Plate material | Decided by Amish, 2026-09-25: go with recommendation. PETG as the default, ASA where plates sit in strong sun, PLA for trials only | SDL-REQ-001 R6, `bom/bom.csv` line 6 |

Budget, pitch and problem line: the TRL 2 review proposed no change, so `budget_usd: 400`, the pitch and the problem line stay as they are.

### Items that remain open

*Table 2. Items still proposed, awaiting Amish.*

| # | Item | Why it is open |
| --- | --- | --- |
| 10 | Co-design partner and region | The TRL 2 review made no recommendation. Under the portfolio rule of 2026-09-25, community designs pick co-design partners per area later, so this stays open |
| 11 | Standalone plate generator | SDL-PRC-001 v0.2 listed a parametric plate generator as a suggestion without a recommendation. The TRL 3 model has a parametric plate function (`make_plate` in `cad/src/model.py`); whether to publish it as a separate tool for printers is still for Amish |

## Consequences

- R3 is now met on paper through skip-cell plates (SDL-CAL-001 section 2).
- R5 is redefined: seed under 2 mm is sown only as pelleted seed. The paper check shows raw 1 to 2 mm seed would need cells finer than a 0.4 mm FDM nozzle holds.
- The bolted frame adds brackets and bolts, which raises the base parts cost to about $214 and contributes to R17 (about $200) not being met; see SDL-CAL-001 section 11.
- TRL 4 work (bench tests of cell fill and spacing, field trials, build procedures) is on hold by Amish's instruction.
