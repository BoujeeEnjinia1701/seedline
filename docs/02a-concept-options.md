---
doc_id: SDL-OPT-001
title: SeedLine concept options
project: SeedLine
doc_type: Concept options
version: "0.1"
status: Draft
date: '2026-10-24'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-24'
    author: Amish Chadha
    change: "First issue (kit 1.8 and 1.9.1 upgrade): the current design as option A and a punch wheel with a hub meter as option B, both modelled to detail level D3, STEM-checked and scored; option A recommended, Proposed, awaiting Amish"
---

# SeedLine concept options

Option A, the current design (a cell plate on a chain drive), is recommended: it scores 169 of 230 weighted points against 131 for option B (a punch wheel with a hub meter), 29 % apart, so a pick is made; the choice is Proposed, awaiting Amish (SDL-DEC-001 D1, argued in SDL-DDR-004). Both options are modelled to detail level D3 in `cad/src/model.py` (`OPTIONS`, `components(option)`) and pass the CAD fidelity check (`cad/fidelity.json`). Method: STANDARDS section 21.

![Concept options side by side at one scale](../media/options.png)

*Figure 1. The two options from their D3 models, rendered at one scale with a 1.75 m figure (`python .kit/options.py`, rendered by the coordinator on Amish's Mac).*

## The options

### Option A: cell plate on a chain drive (the current design)

**Working principle.** A 300 mm lugged ground wheel turns a printed vertical cell plate through a #35 roller chain; a runner opener cuts a furrow, each cell drops one seed into it, and drag chains and a press wheel cover and firm the row.

This is the design carried to TRL 3 (SDL-PRC-001, SDL-DDR-001 to 003): a bolted frame of 25 mm square tube, a 120 mm printed plate with 1 to 36 cells per crop, a 15 T sprocket pair with a spring tensioner (12 and 18 T in the optional ratio kit), a 2.4 L hopper, a runner opener with six depth settings, a 200 mm press wheel, a telescoping handle and an optional marker arm. First-order numbers come from SDL-CAL-001: 22 to 589 mm in-row spacing, 0.142 ha/h, 132 N horizontal push in the design case, 14.8 kg with the marker kit, USD 224.10 for the base seeder. **Key risks:** cell fill at 0.299 m/s against an assumed 0.30 m/s limit (SDL-STM-001 S6); spacing uniformity set by assumed miss and double rates (S7); push on heavy seedbeds (S8, S9). **Needs from a co-design partner:** crops, spacings and soil data; a bench and field trial at TRL 4 and 5.

### Option B: punch wheel with a hub meter

**Working principle.** A 480 mm wheel presses six punches into the seedbed as it rolls; a printed cell ring in the hub drops one seed down the tube of the punch about to enter the soil, and the punch's trailing jaw opens in the ground.

The wheel rolls on a 40 x 4 mm steel rim; six punches (a welded fixed jaw with two cheeks and a hinged trailing jaw closed by a torsion spring) stand 55 mm proud of it, 251 mm apart round the rim, so the spacing is fixed by the wheel. Six 20 mm tubes run from a 160 mm hub drum to the punches. Inside the drum, on the fixed 25 mm axle, a stationary printed seed chamber holds the seed pool; a printed cell ring turning with the drum picks one seed per cell, a brush sweeps off extras, a stationary shoe carries the seeds over the top, and a 30 degree release window low on the front drops each seed into its tube (cells at 0.23 m/s, slower than option A's). A 1.7 L hopper on the chamber's neck, outside the drum, feeds the chamber (2.1 L in all). Two flange bearings in the drum carry it on the axle; a fork of 50 x 8 mm flat bar and a 22 mm tube handle complete it. It leaves no furrow to cover, has no chain and no opener draft. **Key risks:** seed delivery timing (the seed reaches the jaws at about 78 degrees past forward, against the jaw opening near 90, at 2.9 km/h; OB4); jaw opening and soil sticking (OB6, and Molin et al. 1998 reported synchronisation and soil-sticking problems on a punch planter prototype); one spacing per wheel; depth fixed by punch length; welded and rolled parts. **Needs from a co-design partner:** a welding and rolling workshop; trials on tilled and on untilled soil.

## First-order numbers

Table 1. Options compared.

| Quantity | Option A | Option B |
| --- | --- | --- |
| Estimated parts cost (USD) | 224.10 base, 266.10 with both kits (priced BOM) | Not priced; by analogy with option A's BOM lines, of the order of USD 150 to 200 in parts, to assess |
| Mass (kg) | 14.8 with the marker kit (SDL-CAL-001); 14.5 in `cad/fidelity.json` (printed parts at HDPE density) | 12.4 (`cad/fidelity.json`, printed parts at HDPE density) |
| Output or throughput | 0.142 ha/h on 0.75 m rows at 2.9 km/h; spacing 22 to 589 mm | About the same at the same speed; one spacing per wheel (251 mm with six punches) |
| Energy or effort | 132 N horizontal push in the design case (68 N of it opener draft) | No opener draft; rolling resistance of a 480 mm rim; punches need about 32 N each in tilled soil, carried by the wheel's weight |
| Depth | 10 to 60 mm in 10 mm steps | Fixed by punch length (50 mm), less any rim sinkage |
| Parts count (`cad/fidelity.json`) | 509 parts (163 made or bought, 346 fasteners, no welds) | 173 parts (61 made or bought, 75 fasteners, 37 welds) |
| STEM check (SDL-STM-001) | No row fails; S6 to S10, S16 and S17 open | No row fails; OB4 and OB6 open; no untilled-soil advantage without ballast (OB3) |

## Scoring

Table 2. Weighted scoring (weights: High UR 3, Medium 2, Low 1; scores 1 to 5).

| Criterion | Source | Weight | A | B | Reason |
| --- | --- | --- | --- | --- | --- |
| One seed per station | UR-001 | 3 | 3 | 3 | A's cells run at the assumed fill limit; B's run slower (0.23 m/s) but its seed delivery timing is marginal |
| Even spacing | UR-002 | 3 | 3 | 4 | B places seed into holes punched at a fixed pitch, so drop scatter and bounce do not add; A's CV is 31 % with assumed rates |
| Spacings for local crops | UR-003 | 3 | 5 | 1 | A: 22 to 589 mm by plate and sprocket; B: one spacing per wheel, a new wheel for each |
| Spacing independent of pace | UR-004 | 2 | 4 | 4 | Both are ground driven; A's skid 1.2 to 1.7 %, B's rim sinkage changes its rolling radius |
| Crop change by a printed part | UR-005 | 3 | 5 | 2 | A swaps a printed plate by hand in the field; B's cell ring is printable but sits inside the hub, and spacing needs a new wheel |
| Right sowing depth | UR-006 | 3 | 4 | 2 | A: adjustable 10 to 60 mm; B: fixed by the punches, varies with rim sinkage |
| Faster than the hoe | UR-007 | 3 | 4 | 4 | Same walking speed and row spacing |
| One person can push it | UR-008 | 3 | 3 | 4 | B has no opener draft (68 of A's 132 N) |
| Light and fits the operator | UR-009 | 3 | 3 | 4 | 14.8 kg against about 12.4 kg; both have a telescoping or fixed 950 mm grip |
| Seed capacity and easy filling | UR-010 | 2 | 4 | 4 | 2.42 L against 2.1 L, both over 2 L |
| Next row marked | UR-011 | 2 | 5 | 2 | A has the marker kit; B would need one added |
| No pinch points or sharp edges | UR-012 | 3 | 3 | 2 | A's chain is guarded; B's six hinged jaws and punch points turn exposed round the wheel |
| Lasts several seasons | UR-013 | 2 | 3 | 2 | B's jaws, hinge pins and springs work in the soil |
| Prototype within the value-engineering target | UR-014 | 2 | 4 | 4 | Both well under USD 400 (B to assess) |
| Affordable to replicate | UR-015 | 3 | 3 | 3 | A USD 24.10 over its about USD 200 target; B not priced, of the same order |
| Built and repaired locally | UR-016 | 3 | 4 | 2 | A is cut, drilled and bolted; B needs a rolled rim and drum and welded punches |
| Treated seed handled safely | UR-017 | 2 | 3 | 2 | B's seed chamber is inside the hub and harder to empty and clean |
| Maintenance | STANDARDS section 21 | 1 | 3 | 2 | A: chain, brush and plates; B: jaws, springs and soil cleaning |
| **Weighted total (of 230)** | | | **169** | **131** | |

## Recommendation

Option A, 169 against 131 (29 % apart). It keeps the two things that make SeedLine worth building, a printed plate per crop changed in the field (UR-005) and the full spacing range (UR-003), it is bolted together with common tools (UR-016), and its depth is adjustable (UR-006). Option B is lighter, has no chain to guard and no opener to pull, and its punches set the spacing more evenly, but a spacing change needs a new wheel and it needs rolling and welding. The runner-up's best idea to graft onto option A is B's smaller metering radius, which lowers cell speed at the same walking pace and so the risk on PR-001; for option A this is the smaller plate Amish chose to revisit only with bench data (SDL-DDR-002 item 5), so it stays a recorded idea, not a change. Recorded as Proposed, awaiting Amish in SDL-DEC-001 (D1) and argued in SDL-DDR-004; `concept_chosen` stays unset in `project.yaml` until he decides.

## Sources

- Molin, J. P., L. L. Bashford, R. D. Grisso, and A. J. Jones. 1998. "Population Rate Changes and Other Evaluation Parameters for a Punch Planter Prototype." *Transactions of the ASAE* 41 (5): 1265 to 1270. https://agris.fao.org/search/en/records/65df271f63b8185d9cab2427, accessed 2026-10-24.
- Manual punch planter design and development for smallholder farmers (Lesotho), *International Journal of Industrial and Systems Design Engineering*, 2018, https://www.inderscience.com/filter.php?aid=96730, accessed 2026-10-24.
