---
doc_id: SDL-DEC-001
title: SeedLine design decisions register
project: SeedLine
doc_type: Design decisions register
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
  - version: "0.2"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Amish approved the recommendations for open decisions 1 to 10 (2026-10-02); moved to decisions made (SDL-DDR-003 accepted)"
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Value engineering figures updated for the plate liners and the UV-stabilized door (SDL-CAL-001 v0.5)"
---

# SeedLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

None. All open decisions were decided on 2026-10-02.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Bolt spacing of the two 16 mm and two 12 mm pressed-steel flange bearings | They set the bearing holes in the front drop plates and the bearing plate | SDL-DDR-003, P2, P5 |
| 2 | The steel drive wheel has a flat rim about 45 mm wide and 280 mm across, and a plain 16 mm hub that can be cross-drilled | The lugs sit on the rim; the hub is bolted to the axle | SDL-DDR-003, P2, P13 |
| 3 | The press wheel has an inner spacer tube between its two bearings, 16 mm bore | The clamped axle ties the rails at the rear | SDL-DDR-003, P10 |
| 4 | The spring tensioner fits #35 chain, mounts on one M8 bolt and reaches the lower strand about 50 mm from its pivot | The pivot hole in the rail and the guard outline assume this | SDL-DDR-003, P12 |
| 5 | Hubbed 15 T #35 sprockets with 16 mm and 12 mm bores (or pilot bores the supplier can open out) | Set screws on the axle and shaft flats | SDL-DDR-003, P12 |
| 6 | The tensioner's spring keeps the chain taut at the 0.8 and 1.2 ratios (74- and 77-link chains) | Ratio kit changes | SDL-CAL-001 section 2 |

## Value engineering

Value-engineering target: USD 400 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 266.10 for the prototype with both kits (USD 133.90 under the target). The base seeder's own target (R17) is about USD 200; its estimated cost is USD 224.10 (USD 24.10 over). Main cost drivers and savings worth trying:

- The largest lines are the chain drive (USD 38: hubbed sprockets about USD 9 each and the spring tensioner about USD 12), the frame (USD 30), the drive wheel with its axle and bearings (USD 30), the metering housing, liners, UV-stabilized door, shaft and bearings (USD 27.60), fasteners (USD 19) and the press wheel (USD 17).
- Making the design buildable added USD 22.00 to the base seeder: two axle flange bearings and lug strip (line 1), hubbed sprockets and a bought tensioner (line 2), the door, collar and knob (line 5), more fasteners (line 15), clips, uprights and the opener cross member (line 12), less the opener clamp plate (line 9). The decisions of 2026-10-02 added USD 4.60 more: two printed plate liners (about USD 1.60 of filament) and the UV-stabilized door grade (about USD 3.00).
- Savings worth trying: a fixed, slotted idler in place of the bought spring tensioner (about USD 8, but the spring idler is a decided item); oil-impregnated bronze bushings in the drop plates in place of the two axle flange bearings (about USD 5); welding the lugs where a welder is available (fewer screws, about USD 2); a printed knob and brush holder already in place; buying sprockets, chain and bearings as one kit from a go-kart parts supplier.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items: vertical cell plate on #35 chain, smallholder field crops first, telescoping marker arm, ratio change by plate and 12, 15 or 18 T sprocket with an idler, skip-cell plates for R3, pelleted small seed, front drive wheel, bolted frame, PETG plates | Amish: go with the TRL 2 recommendations | SDL-DDR-001 |
| 2026-09-25 | TRL 3 recommendations: 22 x 1.2 mm handle tube, 12 and 18 T sprockets in an optional ratio kit, walking-speed rule of about 2.9 km/h, rigid opener for ploughed field-crop seedbeds | Amish: "i accept all your recommendations, go with them across all repos." | SDL-DDR-002 |
| 2026-09-30 | Write the prototype build plan with pictures, and make the design physically buildable where the concept cannot be built | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SDL-DDR-003 (changes accepted on 2026-10-02, below) |
| 2026-09-30 | Outstanding decisions live in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | SDL-CAL-001 v0.3, section 11 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P16 (opener cross member, axle bearings, chain-side shaft support, housing collar and lugs, hopper uprights, tensioner and guard fixing, handle joints, rear tie through the press axle, and the rest) and their knock-on changes, as made | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-003, Table 1 |
| 2026-10-02 | Housing slot: option (a). One housing with a 13 mm slot and printed side liners for each plate thickness (6, 8 and 10 mm plates) | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-003, A1 |
| 2026-10-02 | Housing print: option (a). Print the housing whole for the prototype; split it on the row centre only if the supported print fails | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-003, A2; REVIEW 2026-09-26, item 3 |
| 2026-10-02 | Base cost (R17): option (a). Accept USD 219.50 for the prototype and try the bronze bushing and go-kart kit savings at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-003, A3; SDL-CAL-001 section 11 |
| 2026-10-02 | Housing door: option (a). Clear polycarbonate door, in a UV-stabilized grade | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, appearance item 2; SDL-DDR-003, P5 |
| 2026-10-02 | Hopper side window: option (b) for the prototype, no window (changed from the register's (a)); reconsider at TRL 4 if field users ask for it | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, appearance item 1 |
| 2026-10-02 | Drive wheel: option (a). Keep the steel disc drive wheel in the plan; the spoked wheel is a render option | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, appearance item 4 |
| 2026-10-02 | Appearance items accepted as illustrative: handle collars and clevis, colours, illustrative hardware and the marker out of the hero render; the SeedLine name and wordmark stay Amish's branding call | Amish: "i approve your recommendations for all 555 open decisions." | REVIEW 2026-09-26, appearance items 5 to 8 |
| 2026-10-02 | Co-design partner: one already working with smallholder maize and bean farmers on 0.75 m rows on ploughed land, ideally with field trial capacity. First candidate to approach: CIMMYT's small-scale mechanization work in Eastern and Southern Africa | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-001 item 10; SDL-DDR-002 |
| 2026-10-02 | Plate generator: keep it in this repo with a short usage note; publish it as a separate tool only after bench tests confirm the cell sizes it produces | Amish: "i approve your recommendations for all 555 open decisions." | SDL-DDR-001 item 11; SDL-DDR-002 |
