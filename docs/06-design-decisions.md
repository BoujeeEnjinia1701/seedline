---
doc_id: SDL-DEC-001
title: SeedLine design decisions register
project: SeedLine
doc_type: Design decisions register
version: "0.4"
status: Draft
date: '2026-10-24'
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
  - version: "0.4"
    date: '2026-10-24'
    author: Amish Chadha
    change: "Kit 1.9.1 upgrade: concept selection D1 (Proposed, awaiting Amish); fixes F1 to F8 found by the detailed model, the STEM check and its independent review, decided under Amish's standing instruction of 2026-10-23; two items to confirm when parts are bought"
---

# SeedLine design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| D1 | Concept selection (Proposed, awaiting Amish) | (A) cell plate on a chain drive, the current design; (B) punch wheel with a hub meter | (A): 169 of 230 weighted points against 131 (29 % apart); it keeps the printed plate per crop, the spacing range, adjustable depth and the bolted build. Option B's best idea, a smaller metering radius, is the smaller plate already deferred to bench data (SDL-DDR-002 item 5) | Nothing if (A); a redesign if (B) | SDL-OPT-001, SDL-DDR-004 |

Every fix in Table F below was made under Amish's standing instruction of 2026-10-23 and can be reversed by him.

## To confirm when parts are bought

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | Bolt spacing of the two 16 mm and two 12 mm pressed-steel flange bearings | They set the bearing holes in the front drop plates and the bearing plate | SDL-DDR-003, P2, P5 |
| 2 | The steel drive wheel has a flat rim about 45 mm wide and 280 mm across, and a plain 16 mm hub that can be cross-drilled | The lugs sit on the rim; the hub is bolted to the axle | SDL-DDR-003, P2, P13 |
| 3 | The press wheel has an inner spacer tube between its two bearings, 16 mm bore | The clamped axle ties the rails at the rear | SDL-DDR-003, P10 |
| 4 | The spring tensioner fits #35 chain, mounts on one M8 bolt and reaches the lower strand about 50 mm from its pivot | The pivot hole in the rail and the guard outline assume this | SDL-DDR-003, P12 |
| 5 | Hubbed 15 T #35 sprockets with 16 mm and 12 mm bores (or pilot bores the supplier can open out) | Set screws on the axle and shaft flats | SDL-DDR-003, P12 |
| 6 | The tensioner's spring keeps the chain taut at the 0.8 and 1.2 ratios (74- and 77-link chains) | Ratio kit changes | SDL-CAL-001 section 2 |
| 7 | The tensioner's pivot boss is threaded M8, or can be tapped M8 | The pivot screw comes from inside the frame into the boss (F3) | F3 |
| 8 | M4 heat-set inserts suit the printed housing wall (about 5.2 mm holes, 5.7 mm long) | The door screws and the brush holder screw into them (F1) | F1 |

## Fixes made under the standing instruction of 2026-10-23 (kit 1.9.1 upgrade)

Table F. Each fix keeps the working principle, the pitch and the scope; each closes a STEM check row (SDL-STM-001) and is carried into the model, BOM, calculations, drawings and build plan.

| # | What failed | Options weighed | Fix made | Cost and mass | STEM row |
| --- | --- | --- | --- | --- | --- |
| F1 | The housing door's two thumb screws, 12 mm in from its rear edge, stood over the 128 x 132 mm opening, not over housing wall, so they had nothing to screw into (found by the detailed kit 1.9 model) | (a) move the screws into the solid wall bands and enlarge the door to reach them; (b) add printed bosses inside the opening; (c) a clip-on door | (a): door 146 x 150 mm, to the housing's rear and bottom edges; screws 7 mm from the rear edge at 300 mm up and 134 mm from it at 7 mm up, into two M4 heat-set inserts in the wall. (b) would narrow the opening the cells are watched through; (c) is a new part to design and test | Door cut from the same 300 x 300 mm offcut; two inserts within BOM line 15; no cost change | S24 |
| F2 | The wheel hub's M6 cross bolt, drilled at 107 mm from the axle's chain-side end, lay in the plane of the wheel's disc web, so its head and nut sat in the web | (a) move the hole 15 mm toward the door side, inside the 45 mm hub; (b) a hub with a set-screw collar instead | (a): cross hole at 122 mm from the chain-side end. (b) adds a part and relies on a set screw for the drive | None | S25 |
| F3 | The tensioner's pivot bolt head or nut, on the boss's outer end, sat in the chain's upper strand at the real 12 mm chain width | (a) an M8 screw from inside the frame through the rail into the boss, tapped M8; (b) move the pivot down 10 mm | (a): M8 x 40 screw from inside, through the rail into the boss. (b) would move the guard outline and the tensioner's reach | Within BOM line 15 | S26 |
| F4 | The hopper bosses had 4.0 mm holes (a tap drill size), too small for the M5 heat-set inserts in the BOM | (a) 6.5 mm insert holes; (b) tap the 4.0 mm holes M5 in the print | (a): 6.5 mm holes. (b) gives weak threads in PETG | None | S27 |
| F5 | The bought drive and press wheels were drawn as solid steel discs, heavier than the catalogue-class estimates in SDL-CAL-001 | Draw them as pressed-steel wheels of the class priced | Drive wheel with a 2 mm rim and a 2 mm web with six lightening holes; press wheel with a tyre of 6 mm wall on a split rim with a hub; outside sizes unchanged | None; model masses now near the CAL estimates (1.8 kg and 1.6 kg against 1.70 kg and 1.20 kg) | Model only |
| F6 | With every fastener weighed from the detailed model (about 1.0 kg against the 0.58 kg estimate) and the real M16 press axle bolt, the seeder with the marker kit came to 15.5 kg, over the 15 kg of PR-011 (row S10) | (a) lighter plate and bar where stresses are low, and an aluminium marker arm; (b) a 20 x 20 mm frame (a redesign of every joint); (c) ask Amish to accept 15.5 kg (a change to a user-facing target) | (a): front and rear drop plates and the bearing plate 3 mm (were 4); hopper uprights 20 x 2 mm flat bar (were 20 x 3); marker arm in 6061-T6 aluminium tube 20 x 1.5 and 16 x 1.5 (was steel 20 x 1.2 and 16 x 1.2; 6061-T6 rather than 6063 after the independent review checked the full 900 mm reach with the dynamic factor: 128 MPa, factor 1.9); marker disc 1.5 mm (was 2). Checks: drop plate 45 MPa at three times the row-end lift (factor 5.2), upright Euler load 72 N against 16 N (factor 5), arm 35 MPa (factor 6.9) | Minus 0.72 kg: 14.2 kg base, 14.8 kg with the marker kit (0.18 kg margin); BOM estimates unchanged (thinner steel is cheaper; the aluminium arm price is to confirm) | S10 |
| F7 | The rear drop plate's front rail bolt sat under the handle's flattened lower end (its head would clash with the tube's end), and the chain guard's M5 x 50 screws would reach the drive axle bearing's flange behind the drop plate (found by the detailed model) | (a) let the rail bolt pass the flattened end too and clamp it, and use M5 x 45 guard screws; (b) move the handle base | (a): a 6.5 mm hole in each flattened end for the rail bolt (now M6 x 45); guard screws M5 x 45. (b) would move the grip point the push calculation uses | None | Model only (constructability) |
| F8 | The independent review of 2026-10-24 found that the print-time estimate left out the inner ends of the plate cells; corrected, the 10 mm groundnut plate takes 2.05 h, over the 2 h of PR-006 (row S16) | (a) print every plate at 20 % infill instead of 25 %; (b) a 9 mm groundnut plate (breaks the cell rule of 1.2 times the seed thickness); (c) a faster print profile | (a): 1.87 h for the groundnut plate, 1.39 h for maize. The walls and skins, which carry the drive and hold the cell shape, are unchanged; (b) would let kernels stand proud of the cells; (c) costs cell accuracy | Slightly less filament; no cost change | S16 |

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
| 2026-10-24 | F1 to F8 (Table F): door and door screws, hub cross bolt position, tensioner pivot screw, hopper insert holes, bought wheel envelopes, mass fix, rail bolt through the handle tab and guard screw length, plate print infill | Decided under Amish's standing instruction of 2026-10-23 ("whenever a STEM check fails propose and implement the best fix to the design and constructability"); Amish can reverse any of them | This register, Table F; SDL-STM-001 rows S10, S16, S24 to S27 |
