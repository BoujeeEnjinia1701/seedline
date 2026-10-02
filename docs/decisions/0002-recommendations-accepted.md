---
doc_id: SDL-DDR-002
title: SeedLine TRL 3 recommendations accepted
project: SeedLine
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record Amish's acceptance of all open recommendations (TRL 3 review items 3 to 6) and the items that remain open
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Partner and plate generator decided by Amish on 2026-10-02 (SDL-DEC-001)"
---

# 0002: TRL 3 recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted (items 3 to 6 of the TRL 3 review); the co-design partner and region and the standalone plate generator decided by Amish on 2026-10-02 (SDL-DEC-001)

## Context

The TRL 3 section of `docs/REVIEW.md` (session 2026-09-25) listed six items as "Proposed, awaiting Amish", four of them with a recommendation. On 2026-09-25 Amish wrote in chat: "i accept all your recommendations, go with them across all repos." Every open item that carried a recommendation is therefore decided as recommended. Items without a recommendation stay open. TRL 4 remains on hold by Amish's instruction, and SeedLine stays at TRL 3.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 3 section, "Proposed, awaiting Amish"). They are not repeated here.

## Decision

*Table 1. Newly decided items. Each is "Decided by Amish, 2026-09-25: go with recommendation".*

| # | Item | Decision | What changed in the repo |
| --- | --- | --- | --- |
| 3 | R11, mass with the marker kit | Lighter handle of 22 x 1.2 mm round tube (was 25 x 1.5 mm), checked at this design pass | `cad/src/model.py` (HANDLE_OD, HANDLE_T); `bom/bom.csv` line 13 ($16.00 to $14.00); SDL-CAL-001 v0.2 section 5: handle 2.99 to 2.34 kg, seeder 14.6 to 13.9 kg base and 15.6 to 14.9 kg with the marker kit, so R11 moves from not met to met (0.06 kg margin); handle factor on yield 2.9 to 1.9; SDL-DWG-001 Rev P2 |
| 4 | R17, base cost | Keep the target; move the 12 and 18 T wheel sprockets to an optional ratio kit | `bom/bom.csv` line 2 ($47.00 to $33.00) and new line 16, optional ratio kit ($16.00); base seeder $213.50 to $197.50, so R17 moves from not met to met (1.2 % margin); total with both kits stays $237.50; R3 met with the ratio kit, base 15 T only covers 26 to 471 mm |
| 5 | R1, cell speed | Walking-speed rule: about 2.9 km/h (2.4 km/h with the 1.2 ratio); plate size revisited only with bench data | SDL-REQ-001 v0.4 design case 3 to 2.9 km/h; cell speed 0.309 to 0.299 m/s; work rate 0.145 to 0.142 ha/h; R1 stays at risk (no margin, assumed limit); plate resize on hold as TRL 4 bench work |
| 6 | R8, depth on rough seedbeds | Accept the rigid opener for field crops on ploughed land; review with partner data | SDL-REQ-001 v0.4 R8 restated for a ploughed field-crop seedbed; R8 moves from at risk to met on paper; no spring-loaded opener or depth-gauge shoe added |

Budget, pitch and problem line: no recommendation proposed a change, so `budget_usd: 400`, the pitch and the problem line stay as they are. The prototype parts total ($237.50) is inside the budget.

Knock-on numbers from the lighter seeder: design-case push 136 to 132 N along the handle; heavy, loose seedbed 178 N at 35° to 177 N at 36°. R10 stays at risk.

Documents changed: SDL-PRC-001 v0.3 to v0.4, SDL-REQ-001 v0.3 to v0.4, SDL-CAL-001 v0.1 to v0.2, SDL-DWG-001 Rev P1 to P2, `bom/bom.csv`, `bom/bom-notes.md`, `cad/src/model.py`, `cad/src/concept_media.py` (key figures), `README.md`.

### Items that remain open

*Table 2. Items open on 2026-09-25 (no recommendation to accept then), decided on 2026-10-02.*

| # | Item | Why it is open |
| --- | --- | --- |
| 1 | Co-design partner and region (SDL-DDR-001 item 10) | No recommendation; under the portfolio rule, community designs pick co-design partners per area later. Decided by Amish, 2026-10-02: a partner already working with smallholder maize and bean farmers on 0.75 m rows on ploughed land; first candidate to approach, CIMMYT's small-scale mechanization work in Eastern and Southern Africa (SDL-DEC-001) |
| 2 | Standalone plate generator (SDL-DDR-001 item 11) | No recommendation; `make_plate` in the model already does the job, and publishing it as a separate tool was Amish's call. Decided by Amish, 2026-10-02: kept in this repo with a usage note; published as a separate tool only after bench tests confirm its cell sizes (SDL-DEC-001) |

## Consequences

- With the recommendations applied, no requirement is not met on paper: 13 met, 3 at risk (R1, R2, R10), 2 not verifiable at TRL 3 (R7, R15).
- R11 and R17 are met with thin margins (0.06 kg and $2.50), so any added part needs a matching saving.
- The base seeder covers 26 to 471 mm with coarser steps; the ratio kit is needed for 25 mm pelleted seed and close settings above about 300 mm.
- TRL 4 work (bench tests of cell fill and spacing, a plate-size change based on bench data, partner soil and depth data, fatigue of the lighter handle) is recorded as decided where applicable but on hold by Amish's instruction.
