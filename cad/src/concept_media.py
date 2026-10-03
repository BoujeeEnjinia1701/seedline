"""SeedLine concept media (TRL 3), generated from the parametric model in cad/src/model.py.

Run from the repo root:  python cad/src/concept_media.py
Constructable model (SDL-DDR-003); CONCEPT, NOT FOR FABRICATION.

Coordinates in mm. X is the direction of travel (+X forward), Y is across the row,
Z is up, ground at Z = 0. The chain drive sits on the -Y side so it shows in the hero view.
Numbers on the key-figure list and the flow diagram come from docs/04-calcs/sizing.py
(SDL-CAL-001).
"""
import shutil
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import concept  # noqa: E402
from build123d import Box, Pos  # noqa: E402
from concept import Part, render_all  # noqa: E402

from model import NAMES, build_parts  # noqa: E402  (single source of geometry: cad/src/model.py)

_p = build_parts()
_style = {1: ("#374151", (260, 0, 0)), 2: ("#B45309", (0, -260, -60)), 3: ("#FBBF24", (-150, -330, 330)),
          4: ("#E5E7EB", (0, 0, 330)), 5: ("#94A3B8", (0, 170, 90)), 6: ("#0F766E", (0, -170, 240)),
          7: ("#7C3AED", (520, -250, 120)), 8: ("#0EA5E9", (80, 0, -90)), 9: ("#6B7280", (140, 0, -200)),
          10: ("#57534E", (-280, 0, -200)), 11: ("#1F2937", (-220, 0, -40)), 12: ("#4B5563", (0, 0, 0)),
          13: ("#115E59", (350, 450, -150)), 14: ("#D97706", (0, -250, 0))}
parts = [Part(NAMES[k], _p[k], _style[k][0], k, _style[k][1]) for k in sorted(_p)]

if __name__ == "__main__":
    render_all(
        parts, project="SeedLine", title="Push seeder concept", dwg_no="SDL-DWG-010",
        date="2026-10-01",
        key_figures=["Single row; 300 mm ground wheel drives the plate by #35 chain",
                     "Spacing = 942 mm / (cells x ratio); 22 to 589 mm nominal",
                     "Printed plates: 1 to 36 cells; ratio 1.0 (0.8, 1.2 with ratio kit)",
                     "0.142 ha/h at 0.75 m rows, 2.9 km/h (SDL-CAL-001)",
                     "Push 132 N along the handle, design case (R10 at risk)",
                     "14.1 kg base, 14.9 kg with marker; parts $224 base, $266 with kits"],
        cut=False,
        flow={"title": "seeds per 100 m of row, maize plate at 250 mm; doubles add seeds (all values are estimates, SDL-CAL-001)",
              "unit": "seeds",
              "stages": [("Cells passing outlet", 400), ("Filled cells", 380),
                         ("Seeds dropped", 396), ("Seeds covered, firmed", 392)],
              "losses": [(0, "Empty cells, misses (5 %)", 20), (2, "Bounced, left exposed (1 %)", 4)]},
    )
    # Section on the row centerline (Y = 0), seen from the chain side with the -Y half removed, so the
    # plate cells, brush, outlet and drop tube show. The kit's cutaway cuts at the mean part center,
    # which misses the plate here, so the same kit renderer is called with a centerline cutter.
    keep = Pos(0, 2000, 0) * Box(6000, 4000, 6000)
    cut_parts = []
    for p in parts:
        if p.bom in (13, 14):
            continue
        s = p.shape & keep
        if s.volume > 1e-6:
            cut_parts.append(Part(p.name, s, p.color, p.bom, p.explode, p.alpha))
    concept._render(cut_parts, Path("media") / "cutaway.png", azim=-90, elev=18, title="SeedLine: cutaway")
    for d in Path("media").glob("_views*"):
        shutil.rmtree(d, ignore_errors=True)
