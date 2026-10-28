"""SeedLine concept media (TRL 3, kit 1.9), generated from the detailed model of the chosen design.

Run from the repo root:  python cad/src/concept_media.py          (everything)
                         python cad/src/concept_media.py web      (media/model.glb and media/viewer.html only)
                         python cad/src/concept_media.py <name>   (hero, cutaway, exploded, flow or blueprint only)

Parts come from cad/src/model.py components("A"), grouped by BOM line so the exploded callouts match bom/bom.csv;
fasteners ride with their line in the exploded view and are left out of the blueprint sheet (hidden-line projection
of some 350 fasteners adds hours and nothing at sheet scale). Writes media/hero.png (1.75 m scale figure),
media/cutaway.png (section on the row centreline, seen from the chain side with that half removed),
media/exploded.png, media/model.glb and media/viewer.html, media/flow.png (seed flow; values are estimates from
SDL-CAL-001) and media/concept-blueprint.png and .pdf (SDL-DWG-010). CONCEPT, NOT FOR FABRICATION.

Coordinates in mm: X the direction of travel (+X forward), Y across the row (chain on the -Y side), Z up, ground at
Z = 0.
"""
import csv
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
import build123d  # noqa: E402
from build123d import Box, Compound, Pos  # noqa: E402
import concept as K  # noqa: E402
from concept import Part  # noqa: E402
import model  # noqa: E402

# the kit exports model.glb at build123d's default 0.001 mm chord; 0.15 mm and 0.3 rad keep it small for the web
_export_gltf = build123d.export_gltf


def _coarse_gltf(*a, **k):
    k.setdefault("linear_deflection", 0.15)
    k.setdefault("angular_deflection", 0.3)
    return _export_gltf(*a, **k)


build123d.export_gltf = _coarse_gltf

PROJECT, TITLE, DWG = "SeedLine", "Push seeder concept", "SDL-DWG-010"
MD = ROOT / "media"
COLOURS = {1: "#374151", 2: "#B45309", 3: "#FBBF24", 4: "#E5E7EB", 5: "#94A3B8", 6: "#0F766E", 7: "#7C3AED",
           8: "#0EA5E9", 9: "#6B7280", 10: "#57534E", 11: "#1F2937", 12: "#4B5563", 13: "#115E59", 14: "#D97706",
           15: "#111827"}
KEY_FIGURES = ["Single row; 300 mm ground wheel drives the plate by #35 chain",
               "Spacing = 942 mm / (cells x ratio); 22 to 589 mm nominal",
               "Printed plates: 1 to 36 cells; ratio 1.0 (0.8, 1.2 with ratio kit)",
               "0.142 ha/h at 0.75 m rows, 2.9 km/h (SDL-CAL-001)",
               "Push 132 N horizontal (206 N along the handle), design case; R10 at risk",
               "14.2 kg base, 14.8 kg with marker; parts $224 base, $266 with kits"]


def names():
    return {int(r["item"].split()[0]): " ".join(r["item"].split()[1:]) for r in csv.DictReader(open(ROOT / "bom/bom.csv"))}


def grouped():
    """One Part per BOM line (numbered), and one unnumbered Part per line for its fasteners."""
    nm = names()
    body, fix = {}, {}
    explode = {}
    for p in model.components(model.CHOSEN):
        if p["kind"] == "context":
            continue
        b = p.get("bom") or 15
        explode[b] = p.get("explode", (0, 0, 0))
        (fix if p["kind"] == "fastener" else body).setdefault(b, []).append(p["shape"])
    out = []
    for b in sorted(body):
        out.append(Part(nm.get(b, f"Line {b}"), Compound(children=body[b]), COLOURS.get(b, "#9CA3AF"), b, explode[b]))
    for b in sorted(fix):
        out.append(Part(f"Fixings, line {b}", Compound(children=fix[b]), "#1F2937", None, explode.get(b, (0, 0, 0))))
    return out


def hero(ps):
    shown = K.with_scale_figure(ps)
    return K._render(shown, MD / "hero.png", title=PROJECT,
                     note="Seen from the front right and above, 24 deg elevation. Grey figure: 1.75 m person for scale")


def exploded(ps):
    return K._render(ps, MD / "exploded.png", offsets=True, labels=True, title=f"{PROJECT}: exploded view",
                     note="Seen from the front right and above, 24 deg elevation; numbers match bom/bom.csv")


def cutaway(ps):
    """Section on the row centreline (Y = 0), seen from the chain side with the -Y half removed, so the plate cells,
    brush, outlet and drop tube show; the handle and the marker kit are left out."""
    import gc
    keep = Pos(0, 2000, 0) * Box(6000, 4000, 6000)
    cut = []
    for p in ps:
        if p.bom in (13, 14) or p.name in ("Fixings, line 13", "Fixings, line 14"):
            continue
        # one solid at a time (a boolean on a whole BOM line's compound runs out of memory); solids wholly on the
        # kept side are kept as they are, wholly on the removed side dropped, and only those across Y = 0 are cut
        kept = []
        for sol in p.shape.solids():
            bb = sol.bounding_box()
            if bb.min.Y >= 0:
                kept.append(sol)
            elif bb.max.Y > 0:
                c = sol & keep
                if c is not None and c.volume > 1e-6:
                    kept.extend(c.solids() if hasattr(c, "solids") else [c])
        gc.collect()
        if kept:
            cut.append(Part(p.name, Compound(children=kept), p.color, p.bom, p.explode, p.alpha))
    return K._render(cut, MD / "cutaway.png", azim=-90, elev=18, title=f"{PROJECT}: cutaway",
                     note="Section on the row centreline, seen from the chain side with that half removed, 18 deg elevation")


def flow():
    return K.flow_diagram([("Cells passing outlet", 400), ("Filled cells", 380), ("Seeds dropped", 396), ("Seeds covered, firmed", 392)],
                          MD / "flow.png",
                          f"{PROJECT}: seeds per 100 m of row, maize plate at 250 mm; doubles add seeds (all values are estimates, SDL-CAL-001)",
                          "seeds", [(0, "Empty cells, misses (5 %)", 20), (2, "Bounced, left exposed (1 %)", 4)])


def blueprint(ps):
    from drawing import Sheet, project_views
    body = [p for p in ps if p.bom is not None]
    views = project_views(Compound(children=[p.shape for p in body]), MD / "_views")
    views["iso"] = project_views(Compound(children=[p.shape for p in K.with_scale_figure(body)]), MD / "_views_fig")["iso"]
    s = Sheet(project=PROJECT, title=TITLE, dwg_no=DWG, rev="P2", author="Amish Chadha", date="2026-10-24",
              theme="blueprint", material="Concept model from the kit 1.9 detailed model; fasteners not drawn at this scale",
              revisions=[("P1", "Concept sheet", "2026-10-01", "AC"), ("P2", "Kit 1.9 detailed model", "2026-10-24", "AC")])
    s.add_ortho(views)
    s.add_svg(views["iso"], 276, 32, 140, 118, label="Isometric view", sublabel="Not to scale; figure is a 1.75 m person")
    s.add_notes("Key figures", KEY_FIGURES, x=276, y=168, width=140)
    s.save(MD / "concept-blueprint")
    for d in ("_views", "_views_fig"):
        shutil.rmtree(MD / d, ignore_errors=True)
    return MD / "concept-blueprint.png"


def web(ps):
    return K.export_web_model(ps, "media", title=f"{PROJECT}: {TITLE}")


if __name__ == "__main__":
    what = sys.argv[1:] or ["hero", "exploded", "cutaway", "flow", "web", "blueprint"]
    ps = grouped() if set(what) - {"flow"} else []
    for w in what:
        r = {"hero": hero, "exploded": exploded, "cutaway": cutaway, "web": web, "blueprint": blueprint}.get(w)
        print(w, "->", flow() if w == "flow" else r(ps), flush=True)
