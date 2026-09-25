# SeedLine

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Agriculture · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $400 USD · **Difficulty:** 2 of 5

Push seeder whose metering plates are 3D printed per crop and driven by the ground wheel, with an optional row-spacing kit.

![SeedLine concept](media/hero.png)

[Interactive 3D model](media/viewer.html) · [Concept blueprint (PDF)](media/concept-blueprint.pdf) · [Review note](docs/REVIEW.md)

## Problem

Hand-seeding is slow and uneven, and precision planters are too costly for small plots.

## Concept

A single-row push seeder. A 300 mm lugged ground wheel drives an upright, 3D-printed seed plate through a roller chain, so seed spacing follows distance travelled rather than walking speed. A runner opener cuts the furrow, drag chains cover the seed and a press wheel firms it. Swapping the printed plate (3 to 36 cells) and one sprocket sets in-row spacing from about 20 to 390 mm. An optional marker arm sets the next row at 200 to 900 mm. Estimates: about 0.14 ha/h for maize on 0.75 m rows, about 14 kg, and about $223 in parts with the marker kit.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- 300 mm lugged ground drive wheel
- #35 chain drive with alternate sprockets and a chain guard
- 2 L seed hopper and metering housing
- 3D-printed seed plates, one per crop and spacing, with a singulator brush
- Runner furrow opener with depth bracket and covering chains
- 200 mm concave press wheel
- Steel frame and telescoping handle
- Row marker arm (optional row-spacing kit)

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

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
