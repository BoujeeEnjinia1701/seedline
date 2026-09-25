---
doc_id: SDL-PRB-001
title: SeedLine problem statement
project: SeedLine
doc_type: Problem statement
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-24'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Populate to TRL 2 (problem, users, context, constraints, out of scope, prior work with sources)
---

# SeedLine problem statement

Hand-seeding is slow and uneven, and precision planters are too costly for small plots. The gap is a push seeder that places one seed at a time at a set spacing, costs about the same as the cheapest plate seeder, and can be adapted to any crop by printing a new metering plate instead of buying one.

## The problem

Most of the world's farms are small. About 84 % of the world's roughly 570 million farms are under 2 ha ([Our World in Data, from Lowder et al.](https://ourworldindata.org/smallholder-food-production)). On these plots and on market gardens, seed is still sown by hand with a hoe, a stick or a jab planter, or dribbled from a cheap plate seeder.

Three problems follow:

1. **Labor.** Hand planting with a hoe has been estimated at about 56 h per hectare for one worker in southern Africa, and a jab planter cuts that to about a third ([Baudron et al., cited in a CSBE jab planter study](https://library.csbe-scgab.ca/docs/meetings/2010/CSBE101037.pdf)). Planting happens in a short window after the first rains, so slow planting delays part of the crop.
2. **Uneven spacing.** Hand-dropped seed lands in clumps and gaps. Uneven stands cost yield: Purdue trials on maize found a loss of about 2.2 to 2.5 bu/acre (about 140 to 160 kg/ha) for each inch (25 mm) increase in the standard deviation of plant-to-plant spacing ([Nielsen, Purdue University](https://www.agry.purdue.edu/ext/corn/research/psv/update2004.html)). Clumped vegetable seed also has to be thinned by hand.
3. **Cost and fit of existing tools.** Low-cost plate seeders such as the Earthway 1001-B (about $187 with six plates) pick up several seeds at a time, so crops usually need thinning, while singulating roller seeders such as the Jang JP-1 cost about $499 before rollers at about $25 each ([University of Minnesota Extension, 2024](https://blog-fruit-vegetable-ipm.extension.umn.edu/2024/11/lower-cost-equipment-for-seeding-and.html)). Users also report that the Earthway is inaccurate with small seed and has no in-row spacing adjustment ([Paperpot Co.](https://paperpot.co/jang-seeder-vs-earthway-josh-sattin/)). A farmer whose crop or seed size does not match a stock plate has no easy way to get one.

SeedLine is a single-row push seeder whose ground wheel drives a vertical metering plate through a chain. The plate is 3D printed for each crop and seed size, so a farmer, a cooperative or a local maker with a printer can make a plate for any seed. An optional row-marker kit sets the spacing between rows.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Smallholder farmer | Plant maize, beans, sorghum or groundnuts at the right spacing in the planting window, with less labor and less seed | Plots of 0.2 to 2 ha, hand-tilled or ox-ploughed soil, rain-fed, often one worker |
| Market gardener | Sow vegetables in beds without thinning, at low cost | Beds of 0.75 to 1.2 m, fine tilled soil, 3 to 6 rows per bed |
| Cooperative or agro-dealer with a printer | Print plates on demand for members' crops and varieties; lend or rent seeders | Rural town, one FDM printer, basic tools |
| Local welder or maker | Build and repair the frame from common steel tube and bicycle parts | Workshop with a welder or drill, bicycle spares available |
| Extension worker or researcher | Recommend spacings and check stands | Field demonstrations, trial plots |

### Operating environment

- **Soil:** tilled loam to sandy loam, with clods, crop residue and stones up to about 50 mm; seedbed quality varies widely on hand-tilled plots.
- **Seed:** from maize and beans (8 to 15 mm) down to vegetable seed of 1 to 2 mm; some seed is treated with fungicide or insecticide.
- **Climate:** 10 to 40 °C, strong sun, dust; rain and mud at planting time.
- **Supply chain:** steel tube, bicycle chain and sprockets, bearings and wheelbarrow or trolley wheels are common in regional towns; 3D printers are uncommon in villages but increasingly present in towns, universities and maker spaces.

## Constraints

- Garage-buildable prototype, about $400 USD (`project.yaml`).
- A replicated base seeder (without the marker kit) should cost no more than a low-cost plate seeder, about $200 in parts.
- Metering plates printable in PLA, PETG or ASA on a common desktop FDM printer, without supports.
- Frame and drive from common steel sections, bicycle chain parts and bearings that local workshops stock.
- Pushed by one person at walking speed on a tilled seedbed.
- No engine, battery or electronics in the base design.

## Out of scope

- Tractor or animal-drawn planters.
- Fertilizer placement (a later option, not part of this concept).
- Transplanting, seed-tape or paper-pot systems.
- Seed treatment, seed supply or agronomic advice beyond the plate spacing tables.
- Vacuum or air-assisted metering.

## Prior work

- **Commercial push seeders.** The Earthway plate seeder and the Jang roller seeder set the price and performance range for push seeders ([UMN Extension](https://blog-fruit-vegetable-ipm.extension.umn.edu/2024/11/lower-cost-equipment-for-seeding-and.html); [Paperpot Co.](https://paperpot.co/jang-seeder-vs-earthway-josh-sattin/)). Both use interchangeable plates or rollers bought from the maker.
- **Open 3D-printed seeders.** The Hour Farm published a hackable, 3D-printed precision seeder with interchangeable printed seed discs on FarmHack in 2019 under CC BY 4.0 ([FarmHack](https://farmhack.org/tools/hackable-3d-printed-precision-seeder)). It shows that printed discs work for vegetable seed at bed scale.
- **Printed parts in precision metering.** A Norfolk farmer printed singulator discs and sprockets for a six-row vacuum maize planter, reporting about 99 % singulation and no visible wear after 70 ha ([3D Printing Industry, 2019](https://3dprintingindustry.com/news/farmer-builds-diy-seed-metering-system-with-3d-printed-parts-161204/)). This is a tractor planter, but it supports the durability of printed metering parts.
- **Jab planters.** Hand jab planters are promoted for conservation agriculture in Africa and cut planting time to about a third of hoe planting ([CSBE study](https://library.csbe-scgab.ca/docs/meetings/2010/CSBE101037.pdf); [FAO jab planter user manual](https://www.fao.org/family-farming/detail/en/c/1619181/)). They place seed hill by hill, so spacing depends on the operator.
- **Research push planters.** Many university studies build and test manual single-row planters with plate or cell-wheel metering (for example, [a manually operated planter for different seeds](https://www.academia.edu/77427641/Manually_Operated_Planter_for_Planting_Different_Seeds_in_Small_Areas)). Their field capacity and seed placement data will be reviewed at TRL 3 to check the estimates in SDL-PRC-001.

## Open questions

- Which users first: smallholder field crops (maize and beans at 0.75 m rows) or market-garden vegetables? This changes the wheel, opener and plate range. Proposed, awaiting Amish (see SDL-PRC-001).
- Which partner and region for co-design and field trials? Proposed, awaiting Amish.
- Who prints plates in practice: the farmer, a cooperative, an agro-dealer or a central maker who mails them?
- How common is treated seed among target users, and what handling rules apply?
- Is the row marker enough, or do users want two or three units ganged on one frame?

## User research and co-design

Requirements must come from the people who will use the seeder.

- [ ] Identify a local partner organization (farmer cooperative, extension service, NGO or university)
- [ ] Run co-design sessions with intended users; record who, where and what was learned
- [ ] Validate crop list, spacing, soil and cost assumptions in the field
- [ ] Revise requirements (REQ) from findings before freezing the design
