---
doc_id: SDL-REG-001
title: SeedLine regulatory and standards register
project: SeedLine
doc_type: Regulatory and standards register
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 pipeline, kit 1.9.1 upgrade), completed for the current design (option A) at stage P3"
---

# SeedLine regulatory and standards register

No product certification is known to apply to a hand-pushed seeder: the EU machinery rules start from a drive system "other than directly applied human or animal effort" (G1), and ISO 4254-1 covers self-propelled, mounted, semi-mounted and trailed agricultural machines (G2). The test method for single-seed drills (G3) is the reference for the placement requirements, the guarding reference (G4) and the manual-handling references (G5, G6) are used as good practice, and treated seed is controlled by its label and national pesticide rules (G7). National rules in the partner's country are not yet known (G8). Not legal advice; anything marked "to assess" needs a qualified reviewer before any product claim. Nothing here needs certification before TRL 4. Method: STANDARDS section 23.

Table 1. Regulatory and standards register.

| # | Standard or regulation | Jurisdiction | What it covers | Applicability to this design | Owner (role) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| G1 | Directive 2006/42/EC (Machinery Directive), Article 2(a); Regulation (EU) 2023/1230 (Machinery Regulation) | European Union | Safety of machinery placed on the market; "machinery" is an assembly "fitted with or intended to be fitted with a drive system other than directly applied human or animal effort" | SeedLine is pushed by hand and has no other drive system, so it appears to fall outside the definition; to confirm for the Regulation's text and for any later powered variant | Design lead | Does not apply (to confirm with a qualified reviewer) |
| G2 | ISO 4254-1:2013, Agricultural machinery, Safety, Part 1: General requirements | International | Safety requirements for self-propelled ride-on, mounted, semi-mounted and trailed agricultural machines | A pedestrian-pushed seeder is not in the stated scope; used only as a reference for guarding and marking practice | Design lead | Does not apply (reference only, to assess) |
| G3 | ISO 7256-1:1984, Sowing equipment, Test methods, Part 1: Single seed drills (precision drills) | International | Test methods for seed spacing (misses, multiples, uniformity) | PR-001 and PR-002 are written in its terms; the TRL 4 bench test and the field counts follow it | Test lead (TRL 4) | Applies (method; tests on hold at the TRL 3 cap) |
| G4 | ISO 13857:2019, Safety of machinery, Safety distances to prevent hazard zones being reached by upper and lower limbs | International | Guard opening sizes and reach distances | The chain guard (PR-014); the guard openings are not yet checked against its tables | Design lead | To assess (good practice; not mandatory for an unpowered seeder) |
| G5 | ISO 11228-2, Ergonomics, Manual handling, Part 2: Pushing and pulling | International | Recommended force limits for pushing and pulling | The design-case push of 132 N horizontal, 206 N along the handle (PR-010) and whether one operator sustains it over a planting day (SDL-STM-001 row S9) | Design lead | To assess |
| G6 | ISO 11228-1, Ergonomics, Manual handling, Part 1: Lifting and carrying | International | Mass limits for manual lifting | 14.8 kg with the marker kit, lifted and turned by one person at row ends (PR-011) | Design lead | To assess |
| G7 | Pesticide product labels and national pesticide regulations for treated seed | Country of use | Personal protective equipment, handling and disposal of seed dressed with fungicide or insecticide | Filling, emptying and cleaning the hopper and housing (UR-017, PRC Safety) | Co-design partner; user | Applies (follow the label); national rules to assess |
| G8 | National agricultural machinery testing or standards schemes in the partner's country (for example national standards bodies in Eastern and Southern Africa) | Country of deployment | Testing or certification of hand planters, where a scheme exists | Unknown until the partner and country are fixed (first candidate: CIMMYT small-scale mechanization work in Eastern and Southern Africa, SDL-DEC-001) | Co-design partner | To assess |
| G9 | CERN-OHL-S-2.0 and MIT licences; REUSE specification | Open hardware practice | Licensing of the design files and software | Every file in the repository (`REUSE.toml`) | Design lead | Met by design |

Status: to assess, applies, does not apply, met by design, certification needed later.

## Sources

- Directive 2006/42/EC of the European Parliament and of the Council (Machinery Directive), Article 2, https://www.legislation.gov.uk/eudr/2006/42/article/2/data.htm, accessed 2026-10-24.
- Regulation (EU) 2023/1230 (Machinery Regulation), https://eur-lex.europa.eu/eli/reg/2023/1230, accessed 2026-10-24 (definition not re-read for this register; G1 to confirm).
- ISO 4254-1:2013 scope as published by the Swedish Institute for Standards, https://www.sis.se/en/produkter/agriculture/agricultural-machines-implements-and-equipment/general/iso425412013/, accessed 2026-10-24.
- ISO 7256-1:1984, title and status, https://www.iso.org/standard/13910.html, accessed 2026-10-24.
- ISO 13857:2019, title as listed by Genorma, https://genorma.com/en/standards/iso-13857-2019, accessed 2026-10-24.
- International Committee of the Red Cross, *Warning: Treated Seeds*, https://www.icrc.org/en/publication/4688-warning-treated-seeds, accessed 2026-10-24.
- Standards G5 and G6 are cited by number and title only; their texts were not consulted for this register, and each applicability is to be confirmed by the role named.
