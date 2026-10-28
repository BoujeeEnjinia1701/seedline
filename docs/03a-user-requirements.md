---
doc_id: SDL-URS-001
title: SeedLine user requirements
project: SeedLine
doc_type: User requirements
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade): user requirements drawn from the users, stakeholders and constraints in SDL-PRB-001"
---

# SeedLine user requirements

These are the needs of the people who would use, build and support SeedLine, written from their side. They come from the users and stakeholders in SDL-PRB-001 (Tables 1 and 2) and its constraints; none has yet been checked with a co-design partner, so every priority is a proposal for review (SDL-PRB-001, "User research and co-design"). The product requirements that meet them are in SDL-PRS-001 (`03-requirements.md`), and the links are generated in SDL-RTM-001 (`03b-traceability.md`). Method: STANDARDS section 22.

Table 1. User requirements.

| ID | Category | Title | Need | Priority | Source |
| --- | --- | --- | --- | --- | --- |
| UR-001 | Performance | One seed per station | Each planting station gets one seed, so seed is not wasted and the stand does not need thinning | High | Smallholder farmer; market gardener (PRB Table 1) |
| UR-002 | Performance | Even spacing | Plants come up evenly along the row, without the clumps and gaps of hand dropping | High | Smallholder farmer; extension worker (PRB Table 1; Nielsen, Purdue) |
| UR-003 | Performance | Spacings for local crops | The seeder sows the in-row spacings of the crops grown, maize, beans, sorghum and groundnut first and vegetables later, from about 25 to 400 mm | High | Smallholder farmer; market gardener (PRB Table 1; SDL-DDR-001 item 2) |
| UR-004 | Performance | Spacing independent of pace | Spacing stays the same when the operator walks faster or slower or stops | Medium | Smallholder farmer (PRB) |
| UR-005 | Usability | Crop change by a printed part | A crop or seed size is changed in the field by swapping a part a cooperative or local maker can print on a common desktop printer | High | Cooperative or agro-dealer with a printer (PRB Table 1) |
| UR-006 | Performance | Right sowing depth | Seed is placed at the depth the crop needs and held there along the row | High | Smallholder farmer; extension worker (PRB) |
| UR-007 | Performance | Faster than the hoe | Planting a plot takes much less labour than hoe or jab planting, so it fits in the short planting window | High | Smallholder farmer (PRB, about 56 h/ha by hoe) |
| UR-008 | Usability | One person can push it | One person can push the seeder at walking pace on a tilled seedbed | High | Smallholder farmer, often one worker (PRB constraints) |
| UR-009 | Usability | Light and fits the operator | One person can lift and turn it at a row end, and the handle suits the operator's height | High | Smallholder farmer (PRB) |
| UR-010 | Usability | Seed capacity and easy filling | It holds enough seed for long runs, fills from a jug without spilling and empties quickly for a crop change | Medium | Smallholder farmer; market gardener (PRB) |
| UR-011 | Usability | Next row marked | The next row is marked at the chosen row spacing, so rows come out straight and parallel | Medium | Smallholder farmer (SDL-DDR-001 item 3) |
| UR-012 | Safety | No pinch points or sharp edges in use | Hands, feet and clothing cannot be caught by moving parts, and there are no exposed sharp edges | High | Every user (PRB; PRC Safety) |
| UR-013 | Environment and durability | Lasts several seasons | Frame, drive and opener last several seasons on small plots with only wear parts replaced | Medium | Smallholder farmer; cooperative (PRB) |
| UR-014 | Cost | Prototype within the value-engineering target | The proof-of-concept prototype's parts stay within the hypothetical USD 400 value-engineering target | Medium | Amish Chadha, `project.yaml` budget_usd (STANDARDS section 18) |
| UR-015 | Cost | Affordable to replicate | A replicated base seeder costs no more than a low-cost plate seeder, about USD 200 in parts | High | Smallholder farmer; cooperative (PRB constraints) |
| UR-016 | Deployment and assembly | Built and repaired locally | A local workshop can build and repair it from common steel sections, bicycle or roller chain parts and bearings, with a drill and spanners or a welder | High | Local welder or maker (PRB Table 1) |
| UR-017 | Safety | Treated seed handled safely | Seed dressed with pesticide can be filled, emptied and cleaned out with little contact | Medium | Smallholder farmer; extension worker (PRB operating environment; PRC Safety) |

Categories: deployment and assembly, performance, usability, safety, environment and durability, logistics, maintenance, cost, regulatory. Priorities: High, Medium, Low.
