---
doc_id: SDL-DDR-003
title: SeedLine design for construction
project: SeedLine
doc_type: Design decision record
version: "0.3"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-02'
  author: Amish Chadha
  change: "Accepted by Amish (2026-10-02), with A1 to A3 as recommended; status kept Draft"
- version: "0.3"
  date: '2026-10-02'
  author: Amish Chadha
  change: "A1 carried into the model, making sketches and build plan (13 mm slot, printed liners); cost and mass figures updated"
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** accepted. Amish, 2026-10-02: "i approve your recommendations for all 555 open decisions." This covers every change in Tables 1 and 2 and the recommendations for A1 to A3 in Table 3, which are now decided as recommended and recorded in the design decisions register (SDL-DEC-001).

## Context

On 2026-09-30 Amish asked for a prototype build plan that shows how each component is made and how it fits the next, with pictures, and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The TRL 3 model of SDL-DDR-002 showed what SeedLine does, but it was a massing model: checking it with build123d found parts running through each other (the front cross member through the drive wheel, about 12,400 mm³; the opener shank and clamp through the metering housing and the seed plate, about 21,400 mm³; the covering chain bracket through the housing, about 9,900 mm³; the handle tubes inside the rails, about 8,600 mm³) and parts with no fixing at all (the shaft bearings, the hopper, the housing, the chain guard, the idler, the handle, the marker arm).

The changes below keep what the seeder does: the same wheel sizes and wheelbase, plate size, shaft height and chain centres (so the 76-link chain and every spacing figure stand), the same opener depth range and leading-edge position, hopper volume, handle angle and grip height, row marker reach and every decided item in SDL-DDR-001 and SDL-DDR-002. Nothing here changes the pitch or the safety case; the chain guard now covers more than before. Every change is in `cad/src/model.py`, which now builds each component separately and runs 78 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 78 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The front cross member, 47.5 mm ahead of the drive axle at rail height, ran through the drive wheel. | Removed. A new opener cross member of 40 x 20 x 1.5 mm rectangular tube, standing 40 mm tall, sits between the rails with its front face 161 mm behind the drive axle, 19 mm clear of the lug tips. | It is the only place between the wheel and the metering housing where a cross member fits, and it gives the opener a rigid mount (P3). |
| P2 | The drive wheel ran on its own bearings, so it could not turn the axle or the sprocket on it; the axle passed through the drop plates with no bearings. | The wheel has a plain 16 mm bore and is fixed to the axle by an M6 cross bolt. The axle turns in two pressed-steel flange bearings bolted to the inside faces of the front drop plates, located by two spacer tubes either side of the hub. | This is how a ground-drive wheel turns a sprocket; the bearings sit inboard so the sprocket and guard stay outboard. |
| P3 | The opener shank and its clamp ran through the metering housing and the seed plate. | The 20 x 12 mm shank sits against the rear face of the opener cross member, 3 mm ahead of the housing, held by two M6 bolts from the front into two of eight tapped holes in its front face (10 mm pitch: six depth settings, 10 to 60 mm). The boot is two 3 mm side plates bolted to the shank's lower end with a rear spacer; seed falls between them. The opener's leading edge is 181 mm behind the drive axle (182 mm in the concept). | No nut behind the shank (the housing is 3 mm away). Depth range, opener width (18 mm) and leading-edge position are unchanged, so the draft, push force and depth figures stand. |
| P4 | The covering chain bracket ran through the housing and hung from nothing. | A 40 mm piece of 25 x 25 x 3 mm angle bolted to the rear face of the middle cross member; the two chains hang from it and drag behind the opener, at least 15 mm clear of the press wheel. | Uses an existing member; the chains still cover the row behind the seed drop. |
| P5 | The housing floated on the plate shaft with no mounting, and the plate could not come off: the shaft ran through bearings on both rails with the knob part-way along it. | The 12 mm shaft is held from the chain side only, in two flange bearings, one on each face of a 4 mm bearing plate bolted to the chain-side rail. The housing hangs on two printed lugs that share the bearing plate's bolts through the rail. The plate has a 20 mm hub that runs in the housing wall and stops on a shaft collar; a printed knob screws into the shaft end. The door side of the housing is a clear 3 mm polycarbonate door on two thumb screws. | Plate change by hand: knob out, door off, plate off (R7). Sharing the bolts keeps the shaft and the housing slot in line. The clear door follows the appearance-model recommendation still open for Amish (SDL-DEC-001). |
| P6 | The shaft bearings stood on nothing beside the rails. | As P5: both bearings on the bearing plate; the inboard one clears the rail top by 2.5 mm. | |
| P7 | The hopper throat (66 x 36 mm) was wider than the housing (21 mm), and the hopper sat on four posts with no fixing. | The housing has a printed collar on top with a 68 x 38 mm pocket and a funnel down to the 9 mm slot. The hopper has a 12 mm straight neck that drops into the pocket (1 mm all round) and sits 10 mm higher. The posts are replaced by four 20 x 3 mm flat-bar uprights bolted to the outside faces of the rails; the hopper carries printed bosses with M5 heat-set inserts, two screws per upright. | The funnel feeds the slot; the uprights carry the weight and the collar keeps the hopper from racking. Hopper volume is now 2.42 L (2.40 L). |
| P8 | The brush holder stood in the path of the hopper throat. | The brush passes through a 9 x 10 mm slot in the housing's rear wall, 35 to 45 mm above the shaft, with its holder screwed to the outside of the wall in slotted holes. | The brush still sweeps the rising cells; the gap is set from outside. |
| P9 | The handle tubes ended inside the rails with no fixing; the grip and brace were tube-to-tube tees with no joint; the telescoping joint was not placed. | The lower ends of the side tubes are flattened and bolted to the outside of the rear drop plates with two M8 bolts each; the upper tubes are flattened at the top and bolted to the back of the cross grip; 250 mm sleeves of 25 x 1.2 mm tube join lower and upper tubes, with pin holes for 850 to 1,050 mm grip height; the brace (18 mm tube, flattened ends) is bolted across the front of the lower tubes at 30 % of their length. | Flattened, drilled tube ends are a common, tool-light joint; the grip point (950 mm high, 50°) is unchanged, so the push figures stand. |
| P10 | The rear cross member passed 4 mm above the press tyre. | Removed. The press axle, clamped by its nuts through two spacer tubes and the wheel's inner spacer between the rear drop plates, ties the rails at the rear. Rear drop plates are 50 mm wide. | A clamped axle stack is a stiff tie; the tyre now has 12.7 mm or more to every frame part. |
| P11 | The six corner plates were flat plates lying across the ends of the cross members. | Four corner clips of 25 x 25 x 3 mm angle, one leg bolted to a rail's inside face and one to a cross member's rear face. At the opener cross member the rail bolt also holds the front hopper upright. | Square-tube cross members butt the rails; an angle clip is the simplest bolted corner. |
| P12 | The chain guard had no fixing; the idler arm ended at a rail corner with no pivot, and the guard did not cover the idler's travel; the outboard bearing would have hit the sprocket. | A bought spring-loaded #35 chain tensioner (go-kart class) pivots on an M8 bolt through the chain-side rail, between the strands, with its 10 T idler on the slack (lower) strand. The printed guard's outline encloses both sprockets and the tensioner's full 45 mm of travel, and it is held by two M5 screws through 8 mm spacer tubes into tapped holes in the chain-side drop plate and the bearing plate. The chain plane moves 12 mm outward (from 92 to 104 mm off the row) and the sprockets have hubs with set screws. | The spring idler is kept (SDL-DDR-001 item 4); a bought tensioner is simpler than a made arm and spring. The chain still runs at least 8.5 mm from the guard. |
| P13 | The wheel lugs had no fixing. | Eighteen L-shaped lugs bent from 25 x 3 mm strip (15 mm foot, 10 mm upstand), each fixed to the steel rim with two M5 countersunk screws. | Drill and bolts only (R18); the lug tips stay on a 300 mm circle. |
| P14 | The marker arm clipped to the front cross member, which P1 removes. | A U-bracket bent from 40 x 3 mm strip is bolted to the front of the chain-side rail (rails are 20 mm longer, 700 mm); the arm pivots on an M8 pin with a spacer each side and folds up. Disc 2 mm (was 3 mm); arm tubes 1.2 mm wall. | Keeps the marker where the concept had it and the 200 to 900 mm reach. |
| P15 | The seed drop tube was a fixed length that could not follow the six depth settings, and it ended inside the shoe. | The tube slides on a 60 mm printed spigot under the housing outlet, rests on the top edges of the boot plates and is tied to them, so it moves with the opener over the full 50 mm range. | |
| P16 | Mass: the added bearings, clips, uprights and fixings put the seeder with the marker kit over 15 kg. | Drop plates 4 mm (was 6 mm); lid 2 mm; marker parts as P14. | Keeps R11 met (14.9 kg with the marker kit after the decisions of 2026-10-02). |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 14.0 kg base (13.9), 14.8 kg with the marker kit (14.9), now weighed part by part from the model; R11 met with 0.19 kg of margin. | Parts added for construction, less those removed (SDL-CAL-001 v0.3 section 5). |
| Cost | Base seeder USD 224.10 after the decisions of 2026-10-02 (USD 219.50 at this record's v0.2; was USD 197.50), USD 24.10 over the about USD 200 value-engineering target of R17; prototype with both kits USD 261.50, USD 138.50 under the USD 400 value-engineering target (`budget_usd`, unchanged). BOM lines 1 to 16 respecified and lines 1, 2, 3, 4, 5, 9, 10, 11, 12, 15 and 16 repriced. | Bearings, hubbed sprockets, tensioner, clips, uprights and fixings (SDL-CAL-001 v0.3 section 11). |
| Calculations | SDL-CAL-001 v0.3: push 132 N design case (unchanged), 178 N heavy seedbed (177 N); depth figures unchanged; hopper 2.42 L. | Follows the model. |
| Requirements | SDL-REQ-001 v0.5: no requirement changes status; R16 and R17 are reported against value-engineering targets. | |
| Drawings | SDL-DWG-001 Rev P3; making sketches SDL-DWG-101 to 124 added. | Follows the model. |
| Media | Concept media regenerated from the model. The photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept and are stale until re-rendered on Amish's Mac. | |

*Table 3. Items proposed to Amish; accepted as recommended on 2026-10-02 (SDL-DEC-001).*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | The housing slot is 9 mm, sized for the 6 mm plates; the bean (8 mm) and groundnut (10 mm) plates need a wider slot, and a wide slot lets small seed slip past a thin plate. | (a) one housing with a 13 mm slot and printed side liners for each plate thickness; (b) print every plate 6 mm thick and accept shallower cells for big seed; (c) a housing for each plate thickness. | (a): one housing, cheap liners. Accepted 2026-10-02: one housing with a 13 mm slot and printed side liners for each plate thickness. |
| A2 | The housing is printed whole, with supports under the lugs and collar. | (a) print whole; (b) print in two halves split on the row centre and screw them together (the appearance model's parting line). | (a) for the prototype; (b) if prints fail. Accepted 2026-10-02. |
| A3 | Base cost is USD 19.50 over the about USD 200 value-engineering target of R17. | (a) accept for the prototype and look for savings at TRL 4; (b) try the savings listed in SDL-DEC-001 now. | (a). Accepted 2026-10-02: USD 219.50 for the prototype; the bronze bushing and go-kart kit savings are tried at TRL 4. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan SDL-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- With A1 accepted on 2026-10-02, the housing slot becomes 13 mm with printed side liners; the model, the housing making sketch and the build plan now show the 13 mm slot, with a printed liner each side for the 6 and 8 mm plates and a door-side liner for all three. The liners add USD 1.60 and 0.06 kg; the UV-stabilized door adds USD 3.00.
- Requirement status: 11 met, 3 at risk (R1, R2, R10), 2 not verifiable at TRL 3 (R7, R15), and R16 and R17 reported against their value-engineering targets (under and over). None is not met.
- The appearance model `cad/src/product_model.py` now matches the constructable model (13 mm slot and liners, no hopper window, steel disc drive wheel) and the render scenes are exported; the photoreal renders are made on Amish's Mac, where Blender is.
- The bearings, wheel, press wheel and tensioner are chosen when the parts are bought (TRL 4); their bolt spacings, bores and the press wheel's inner spacer must be checked then and the holes moved to suit.
