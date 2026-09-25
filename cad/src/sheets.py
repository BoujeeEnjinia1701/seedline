"""SeedLine general arrangement drawing SDL-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/SDL-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses SDL-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P  # noqa: E402

parts = model.build_parts()
asm = model.assembly(parts)
bb = asm.bounding_box()
(hbx, hbz), (gx, gz) = model.handle_points()
cl, cd, th = model.cell_size()

work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)

s = Sheet(project="SeedLine", title="General arrangement, TRL 3 model", dwg_no="SDL-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Bolted 25 x 25 x 1.5 steel tube frame; PETG printed plate, housing, hopper; #35 chain. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA from the TRL 3 model (SDL-CAL-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 80, label="Isometric view", sublabel="Not to scale; marker deployed")
s.add_notes("Key dimensions (mm) and data", [
    f"Overall {bb.size.X:.0f} L x {bb.size.Y:.0f} W x {bb.size.Z:.0f} H (marker at {P['ROW_SPACING']:.0f})",
    f"Drive wheel {P['WHEEL_D']:.0f} dia x {P['WHEEL_W']:.0f}, {P['N_LUGS']} lugs; press wheel {P['PRESS_D']:.0f} x {P['PRESS_W']:.0f}",
    f"Wheelbase {P['X_WHEEL'] - P['X_PRESS']:.0f}; plate shaft {P['X_WHEEL'] - P['X_METER']:.0f} behind drive axle, {P['Z_SHAFT']:.0f} high",
    f"Chain #35, centers {model.center_distance():.0f}; plate 15 T; wheel 12, 15 or 18 T",
    f"Plate {P['PLATE_D']:.0f} dia; maize cells {P['N_CELLS']} x {cl:.1f} long x {cd:.1f} deep; t = {th:.0f}",
    f"Rails {P['RAIL_S']:.0f} sq x {P['RAIL_T']} at {2 * P['RAIL_Y']:.0f} centers, {P['RAIL_Z']:.0f} high",
    f"Opener depth {P['DEPTH']:.0f} shown; 10 to 60 in 10 mm steps",
    f"Grip {P['GRIP_H']:.0f} high (850 to 1,050); handle {P['HANDLE_ANGLE']:.0f} deg",
    f"Hopper {model.hopper_volume_l():.1f} L; marker reach 200 to 900",
    "Mass 14.6 kg base, 15.6 kg with marker (SDL-CAL-001)",
    "Chain guard must be fitted in use",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=124, width=140)
s.save(ROOT / "cad/drawings/SDL-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/SDL-DWG-001.svg, .pdf, .png")
