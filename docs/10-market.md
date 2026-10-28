---
doc_id: SDL-MKT-001
title: SeedLine market and viability
project: SeedLine
doc_type: Market and viability
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade): segments, cited benchmarks with dates, cost per unit from the BOM, open route"
---

# SeedLine market and viability

SeedLine is for smallholders planting maize, beans, sorghum and groundnut on 0.2 to 2 ha, and later for market gardeners, who today plant by hoe, stick or jab planter or with a low-cost plate seeder that drops several seeds per cell. Its estimated parts cost (USD 224.10 for the base seeder) sits just above a low-cost plate seeder and well under a singulating roller seeder before rollers; the open design matters because the part that must match each crop, the plate, becomes a print file a cooperative or local maker can produce rather than a spare part bought from one maker. Prices are cited with the date they were checked; nothing here is a sales forecast. Method: STANDARDS section 23.

Table 1. Market segments.

| Segment | Target users and region | Competitive benchmark (cited price) | Estimated cost per unit (USD) | Value proposition |
| --- | --- | --- | --- | --- |
| Smallholder field crops | Farmers on 0.2 to 2 ha, maize, beans, sorghum and groundnut on 0.75 m rows; Eastern and Southern Africa first (partner rule, SDL-DEC-001), South Asia and Central America later | Hoe planting, about 56 h/ha for one worker, and jab planters at about a third of that time (CSBE study, accessed 2026-10-24); jab planter prices to assess | 224.10 (base seeder, parts only, `bom/bom.csv`); labour and margin not included | About 7.1 h/ha at 0.142 ha/h (SDL-CAL-001), spacing set by travel, depth set by the opener; plates printed for local varieties |
| Market gardens and urban farms | Growers sowing beds of 3 to 6 rows with pelleted vegetable seed; North America and Europe as well as peri-urban farms elsewhere | Earthway 1001-B Precision Garden Seeder with six plates, USD 170.16 (DoMyOwn, accessed 2026-10-24; about USD 187 in UMN Extension, 2024); Jang JP-1 push seeder without rollers, USD 498.00 (Neversink Tools sale price, accessed 2026-10-24), rollers sold separately, about USD 25 each (UMN Extension, 2024) | 224.10 base; 266.10 with the marker and ratio kits | Single-seed metering with a printed plate per seed and spacing, between the plate seeder's price and the roller seeder's |
| Cooperatives, agro-dealers and seed companies | Rural towns with one desktop printer; dealers selling seed varieties | No printed-plate service known; stock plates come from the seeder's maker (Paperpot Co., accessed 2026-10-24) | Plate about USD 1.25 of filament (BOM line 6); printer time not costed | Print plates on demand for members' varieties; rent seeders |
| Extension, NGOs and research | Demonstration plots, conservation agriculture programmes, spacing trials | Hand planting and jab planters in programmes (FAO jab planter manual, accessed 2026-10-24) | 266.10 (prototype with kits) | A low-cost tool whose spacing is set by a file, for demonstrations and trials |

Prices are list or sale prices from one seller each on the date shown, before shipping and duties; they are benchmarks, not quotes. A replicated seeder's selling price, margin and labour are not estimated at TRL 3.

## Open route

SeedLine is published under CERN-OHL-S-2.0 (hardware) and MIT (software), so a workshop, cooperative, NGO or university can build, repair and adapt it without a licence fee, and changes to the design stay open. The intended route is a co-design partner already working with smallholder maize and bean farmers (first candidate: CIMMYT's small-scale mechanization work in Eastern and Southern Africa; nothing is agreed), local welders and makers building frames from the build plan (SDL-BLD-001), and cooperatives or agro-dealers printing plates with the plate generator in `cad/src/model.py` once bench tests confirm its cell sizes (SDL-DEC-001, decided 2026-10-02). Who prints plates in practice, and how plates reach villages without printers, are open questions for the partner (SDL-PRB-001).

## Sources

- Baudron et al., cited in a CSBE study of jab planters, https://library.csbe-scgab.ca/docs/meetings/2010/CSBE101037.pdf, accessed 2026-10-24.
- DoMyOwn, "Earthway 1001-B Precision Garden Seeder," https://www.domyown.com/earthway-1001b-precision-garden-seeder-p-21609.html, accessed 2026-10-24 (USD 170.16, six plates included).
- Neversink Tools, "Jang JP-1 Push Seeder," https://neversinktools.com/products/jang-jp-1-push-seeder, accessed 2026-10-24 (sale price USD 498.00, regular USD 510.00; rollers sold separately).
- University of Minnesota Extension, "Lower-cost equipment for seeding and transplanting," 2024, https://blog-fruit-vegetable-ipm.extension.umn.edu/2024/11/lower-cost-equipment-for-seeding-and.html, accessed 2026-10-24.
- Paperpot Co., "Jang Seeder vs Earthway," https://paperpot.co/jang-seeder-vs-earthway-josh-sattin/, accessed 2026-10-24.
- FAO, jab planter user manual, https://www.fao.org/family-farming/detail/en/c/1619181/, accessed 2026-10-24.
