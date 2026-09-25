# SeedLine

![TRL 3](https://img.shields.io/badge/TRL-3%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 3 of 9 (proof of concept on paper) · **Prototype budget:** about $400 USD · **Difficulty:** 2 of 5

Push seeder whose metering plates are 3D printed per crop and driven by the ground wheel, with an optional row-spacing kit.

![SeedLine concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [General arrangement SDL-DWG-001 (PDF)](cad/drawings/SDL-DWG-001.pdf) · [Calculations SDL-CAL-001](docs/04-calcs/01-sizing.md) · [Review note](docs/REVIEW.md)

## Problem

Hand-seeding is slow and uneven, and precision planters are too costly for small plots.

## Concept

A single-row push seeder for smallholder field crops first, with vegetable plates to follow. A 300 mm lugged ground wheel drives an upright, 3D-printed seed plate through a #35 roller chain, so seed spacing follows distance travelled rather than walking speed. A runner opener cuts the furrow, drag chains cover the seed and a press wheel firms it. Swapping the printed plate (1 to 36 cells, including skip-cell plates for long spacings) and one of three wheel sprockets sets in-row spacing from 22 to 589 mm. Seed under 2 mm is sown pelleted. A marker arm sets the next row at 200 to 900 mm. The frame bolts together from 25 mm square tube.

TRL 3 calculations (SDL-CAL-001): 0.145 ha/h for maize on 0.75 m rows, about 136 N push in the design case, 14.6 kg (15.6 kg with the marker kit) and about $214 in parts for the base seeder ($238 with the marker kit). The mass with the kit and the base cost miss their targets; placement quality, depth control and push effort on heavy seedbeds are at risk.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 300 mm lugged ground drive wheel
- #35 chain drive with 12, 15 and 18 T wheel sprockets, a spring idler and a chain guard
- 2.4 L seed hopper and metering housing
- 3D-printed PETG seed plates, one per crop and spacing, with a singulator brush
- Runner furrow opener with depth bracket and covering chains
- 200 mm concave press wheel
- Bolted steel frame and telescoping handle
- Row marker arm (optional row-spacing kit)

The priced bill of materials is in [bom/bom.csv](bom/bom.csv). The parametric model is [cad/src/model.py](cad/src/model.py), with STEP and STL exports in `cad/step/` and `cad/stl/`.

## Safety

> **Safety:** The chain drive turns whenever the wheel turns and has nip points; keep the guard fitted and hold the wheel still for plate changes and cleaning. The opener and wheel lugs are sharp. Seed treated with pesticides is toxic: follow the seed label, wear gloves and never reuse the hopper for food. See the safety section of [docs/02-concept.md](docs/02-concept.md).

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (SDL-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `SDL-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

Part of the open hardware portfolio at [amishchadha.com](https://amishchadha.com).
