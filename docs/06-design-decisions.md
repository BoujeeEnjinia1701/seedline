---
doc_id: SDL-DEC-001
title: SeedLine design decisions register
project: SeedLine
doc_type: Design decisions register
version: "0.1"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the build plan; budget treated as a value-engineering target
---

# SeedLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | Accept the design-for-construction changes P1 to P16 (opener cross member, axle bearings, chain-side shaft support, housing collar and lugs, hopper uprights, tensioner and guard fixing, handle joints, rear tie through the press axle, and the rest) | Accept as made; or ask for any change to be reworked | Accept | The whole build plan follows these changes | SDL-DDR-003, Table 1 |
| 2 | Housing slot width against plate thickness (plates are 6 to 10 mm; the slot is 9 mm, for 6 mm plates) | (a) one housing with a 13 mm slot and printed side liners per plate thickness; (b) every plate 6 mm thick; (c) a housing per thickness | (a) | Housing print; liners for the bean and groundnut plates. The first prototype uses the 6 mm maize plate and is not affected | SDL-DDR-003, A1 |
| 3 | How the housing is printed | (a) whole, with supports under the lugs and collar; (b) two halves split on the row centre, screwed together | (a) for the prototype; (b) if prints fail | Housing print (build plan section 3.7) | SDL-DDR-003, A2; REVIEW 2026-09-26, item 3 |
| 4 | Base cost over its value-engineering target (USD 219.50 against about USD 200) | (a) accept for the prototype, look for savings at TRL 4; (b) try the savings below now | (a) | None for the prototype | SDL-DDR-003, A3; SDL-CAL-001 section 11 |
| 5 | Clear housing door | (a) clear polycarbonate door, so cell fill and plate identity show; (b) printed door | (a); the build plan already uses it | Door (build plan section 3.11) | REVIEW 2026-09-26, appearance item 2; SDL-DDR-003, P5 |
| 6 | Hopper side window for the seed level | (a) one clear window on the chain side; (b) none | (a) | None yet: the prototype hopper has no window | REVIEW 2026-09-26, appearance item 1 |
| 7 | Drive wheel form | (a) keep open (steel disc wheel in the plan); (b) spoked steel wheel as rendered | (a) | Drive wheel purchase | REVIEW 2026-09-26, appearance item 4 |
| 8 | Appearance items: handle collars and clevis, colours and wordmark, illustrative hardware, marker out of the hero render | Accept as illustrative | Accept; naming and branding stay Amish's | None in the build | REVIEW 2026-09-26, appearance items 5 to 8 |
| 9 | Co-design partner and region | Per the portfolio rule, chosen per area later | None | Crops, plate set and soil data for the first trials | SDL-DDR-001 item 10; SDL-DDR-002 |
| 10 | Standalone plate generator | Publish the model's plate function as a separate tool for printers, or not | None | None in the build | SDL-DDR-001 item 11; SDL-DDR-002 |

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

Value-engineering target: USD 400 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 261.50 for the prototype with both kits (USD 138.50 under the target). The base seeder's own target (R17) is about USD 200; its estimated cost is USD 219.50 (USD 19.50 over). Main cost drivers and savings worth trying:

- The largest lines are the chain drive (USD 38: hubbed sprockets about USD 9 each and the spring tensioner about USD 12), the frame (USD 30), the drive wheel with its axle and bearings (USD 30), the metering housing, shaft and bearings (USD 23), fasteners (USD 19) and the press wheel (USD 17).
- Making the design buildable added USD 22.00 to the base seeder: two axle flange bearings and lug strip (line 1), hubbed sprockets and a bought tensioner (line 2), the door, collar and knob (line 5), more fasteners (line 15), clips, uprights and the opener cross member (line 12), less the opener clamp plate (line 9).
- Savings worth trying: a fixed, slotted idler in place of the bought spring tensioner (about USD 8, but the spring idler is a decided item); oil-impregnated bronze bushings in the drop plates in place of the two axle flange bearings (about USD 5); welding the lugs where a welder is available (fewer screws, about USD 2); a printed knob and brush holder already in place; buying sprockets, chain and bearings as one kit from a go-kart parts supplier.

## Decisions made

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | TRL 2 review items: vertical cell plate on #35 chain, smallholder field crops first, telescoping marker arm, ratio change by plate and 12, 15 or 18 T sprocket with an idler, skip-cell plates for R3, pelleted small seed, front drive wheel, bolted frame, PETG plates | Amish: go with the TRL 2 recommendations | SDL-DDR-001 |
| 2026-09-25 | TRL 3 recommendations: 22 x 1.2 mm handle tube, 12 and 18 T sprockets in an optional ratio kit, walking-speed rule of about 2.9 km/h, rigid opener for ploughed field-crop seedbeds | Amish: "i accept all your recommendations, go with them across all repos." | SDL-DDR-002 |
| 2026-09-30 | Write the prototype build plan with pictures, and make the design physically buildable where the concept cannot be built | Amish: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." | SDL-DDR-003 (Draft, open for review) |
| 2026-09-30 | Outstanding decisions live in this register, not in the build plan | Amish: "don't log outstanding decisions in this build plan - that is not the place for it. that should be in a separate design document logged and named as such" | This register |
| 2026-10-01 | Budgets are value-engineering targets, not limits | Amish: "the budgets are a hypothethical control target to ensure we are thinking along a value engineering lens. its ok to ensure wording reflects that the hypothesis budget was x - the real cost being accrued is y" | SDL-CAL-001 v0.3, section 11 |
