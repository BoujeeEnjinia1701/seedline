"""SeedLine concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm. X is the direction of travel (+X forward), Y is across the row,
Z is up, ground at Z = 0. The seed row runs along the X axis at Y = 0.
The chain drive sits on the -Y side so it is visible in the hero view.
"""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot, Solid, Plane, Vector
from concept import Part, render_all

# Main dimensions (mm)
WHEEL_D, WHEEL_W = 300.0, 45.0          # front ground drive wheel
PRESS_D, PRESS_W = 200.0, 70.0          # rear press wheel
X_WHEEL, X_METER, X_PRESS = 0.0, -270.0, -580.0
RAIL_Y, RAIL_Z, RAIL_S = 60.0, 215.0, 25.0   # side rails, 25 mm square tube
PLATE_D, PLATE_T = 120.0, 6.0           # printed seed plate
Z_SHAFT = 245.0                         # plate shaft height
SPROCKET_R = 23.0                       # 15 T #35 sprocket, about 46 mm pitch diameter (12 T or 18 T on the wheel to change ratio)
Y_CHAIN = -92.0                         # chain plane, outboard of the -Y rail
ROW_SPACING = 750.0                     # marker set for maize at 0.75 m rows


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
    """Round bar between two 3D points."""
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def ycyl(x, y, z, r, w):
    """Cylinder with its axis along Y, centered at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# 1 Ground drive wheel with lugs and axle
zw = WHEEL_D / 2
wheel = ycyl(X_WHEEL, 0, zw, zw - 10, WHEEL_W)
lugs = []
for k in range(18):
    t = math.radians(k * 20)
    lugs.append(Pos(X_WHEEL + (zw - 5) * math.cos(t), 0, zw + (zw - 5) * math.sin(t))
                * Rot(0, -math.degrees(t), 0) * Box(10, WHEEL_W, 14))
wheel = wheel + union(lugs) + ycyl(X_WHEEL, 0, zw, 8, 2 * RAIL_Y + 30)

# 2 Chain drive: 15 T sprocket on the wheel axle, 15 T on the plate shaft, #35 chain
A = (X_WHEEL, zw); B = (X_METER, Z_SHAFT)
dx, dz = B[0] - A[0], B[1] - A[1]; L = math.hypot(dx, dz)
nx, nz = -dz / L, dx / L
sprockets = ycyl(A[0], Y_CHAIN, A[1], SPROCKET_R, 6) + ycyl(B[0], Y_CHAIN, B[1], SPROCKET_R, 6)
strands = (tube3((A[0] + nx * SPROCKET_R, Y_CHAIN, A[1] + nz * SPROCKET_R),
                 (B[0] + nx * SPROCKET_R, Y_CHAIN, B[1] + nz * SPROCKET_R), 4)
           + tube3((A[0] - nx * SPROCKET_R, Y_CHAIN, A[1] - nz * SPROCKET_R),
                   (B[0] - nx * SPROCKET_R, Y_CHAIN, B[1] - nz * SPROCKET_R), 4))
chain = sprockets + strands + ycyl(A[0], Y_CHAIN, A[1], SPROCKET_R + 4, 3) + ycyl(B[0], Y_CHAIN, B[1], SPROCKET_R + 4, 3)


# 3 Chain guard: open-sided band around the chain loop, so the drive stays visible
def stadium(r, w):
    ang = math.degrees(math.atan2(dz, dx))
    mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
    body = Pos(mid[0], Y_CHAIN, mid[1]) * Rot(0, -ang, 0) * Box(L, w, 2 * r)
    return body + ycyl(A[0], Y_CHAIN, A[1], r, w) + ycyl(B[0], Y_CHAIN, B[1], r, w)


guard = stadium(SPROCKET_R + 16, 22) - stadium(SPROCKET_R + 12, 30)

# 5 Metering housing (open-backed box around the plate) with shaft and flange bearings
H_X0, H_X1, H_Z0, H_Z1 = X_METER - 80, X_METER + 80, 165.0, 320.0
housing = box(H_X0, H_X1, -35, 35, H_Z0, H_Z1) - box(H_X0 + 5, H_X1 - 5, -30, 30, H_Z0 + 5, H_Z1 + 1)
housing = housing - ycyl(X_METER + 30, 0, H_Z0 + 2, 11, 40)          # seed outlet to the drop tube
shaft = ycyl(X_METER, (Y_CHAIN + 0) / 2, Z_SHAFT, 6, abs(Y_CHAIN) + 20)
bearings = ycyl(X_METER, -RAIL_Y - 18, Z_SHAFT, 16, 8) + box(X_METER - 20, X_METER + 20, -RAIL_Y - 22, -RAIL_Y - 14, RAIL_Z, Z_SHAFT)
meter = housing + shaft + bearings

# 4 Seed hopper, about 2 L, tapered by a lower funnel block
hop_out = box(X_METER - 85, X_METER + 85, -60, 60, 320, 480)
hop_in = box(X_METER - 80, X_METER + 80, -55, 55, 325, 481)
hopper = hop_out - hop_in + box(X_METER - 85, X_METER + 85, -60, 60, 478, 484) - box(X_METER - 60, X_METER + 60, -45, 45, 470, 490)

# 6 Printed seed plate (vertical disc on the shaft, cells on its rim)
plate = ycyl(X_METER, 0, Z_SHAFT, PLATE_D / 2, PLATE_T)
for k in range(12):
    t = math.radians(k * 30)
    plate = plate - Pos(X_METER + (PLATE_D / 2) * math.cos(t), 0, Z_SHAFT + (PLATE_D / 2) * math.sin(t)) * Box(10, PLATE_T + 2, 10)

# 7 Singulator brush and strike-off, at the top of the plate
brush = box(X_METER - 30, X_METER - 5, -14, 14, Z_SHAFT + PLATE_D / 2 - 4, Z_SHAFT + PLATE_D / 2 + 20)

# 8 Seed drop tube, housing outlet down into the opener
drop = tube3((X_METER + 30, 0, H_Z0), (X_METER + 5, 0, 35), 10)

# 9 Furrow opener: runner shoe on a shank clamped in a slotted depth bracket
shank = box(X_METER + 45, X_METER + 65, -8, 8, 40, RAIL_Z) + box(X_METER + 35, X_METER + 75, -RAIL_Y + 12, RAIL_Y - 12, RAIL_Z - 12, RAIL_Z + 12)
shoe = box(X_METER - 40, X_METER + 70, -9, 9, 0, 45) + Pos(X_METER + 88, 0, 18) * Rot(0, 35, 0) * Box(40, 18, 30)
opener = shank + shoe

# 10 Covering chains, two short drags behind the opener
cover = union([tube3((X_METER - 60, y, 60), (X_METER - 210, y * 1.6, 3), 4) for y in (-22, 22)])
cover = cover + box(X_METER - 70, X_METER - 50, -30, 30, 55, RAIL_Z)

# 11 Press wheel, concave rubber tread
zp = PRESS_D / 2
press = ycyl(X_PRESS, 0, zp, zp, PRESS_W) - ycyl(X_PRESS, 0, zp, zp + 1, 20) + ycyl(X_PRESS, 0, zp, zp - 8, 22)
press = press + ycyl(X_PRESS, 0, zp, 8, 2 * RAIL_Y + 30)

# 12 Steel frame: two side rails, cross members and axle drop plates
rails = union([box(X_PRESS - 40, X_WHEEL + 60, y - RAIL_S / 2, y + RAIL_S / 2, RAIL_Z - RAIL_S / 2, RAIL_Z + RAIL_S / 2)
               for y in (-RAIL_Y, RAIL_Y)])
cross = union([box(x - RAIL_S / 2, x + RAIL_S / 2, -RAIL_Y, RAIL_Y, RAIL_Z - RAIL_S / 2, RAIL_Z + RAIL_S / 2)
               for x in (X_WHEEL + 60, X_METER - 130, X_PRESS - 40)])
drops = union([box(X_WHEEL - 20, X_WHEEL + 20, y - 3, y + 3, zw - 20, RAIL_Z) for y in (-RAIL_Y - 15.5, RAIL_Y + 15.5)]
              + [box(X_PRESS - 20, X_PRESS + 20, y - 3, y + 3, zp - 20, RAIL_Z) for y in (-RAIL_Y - 15.5, RAIL_Y + 15.5)])
hopper_posts = union([box(X_METER + sx - 6, X_METER + sx + 6, sy - 6, sy + 6, RAIL_Z, 320)
                      for sx in (-80, 80) for sy in (-RAIL_Y, RAIL_Y)])
frame = rails + cross + drops + hopper_posts

# 13 Handle: two tubes rising to a cross grip at about 950 mm, telescoping for height
GRIP = (X_PRESS - 650, 950.0)
handle = union([tube3((X_PRESS - 30, y, RAIL_Z), (GRIP[0], y * 4.2, GRIP[1]), 13) for y in (-RAIL_Y, RAIL_Y)])
handle = handle + tube3((GRIP[0] - 20, -RAIL_Y * 4.2 - 40, GRIP[1]), (GRIP[0] - 20, RAIL_Y * 4.2 + 40, GRIP[1]), 14)
mid = (X_PRESS - 30 + (GRIP[0] - X_PRESS + 30) * 0.45, RAIL_Z + (GRIP[1] - RAIL_Z) * 0.45)
handle = handle + tube3((mid[0], -RAIL_Y * 2.5, mid[1]), (mid[0], RAIL_Y * 2.5, mid[1]), 9)

# 14 Row marker arm (row-spacing kit): telescoping arm and marker disc set to the next row
MX = X_WHEEL + 60
arm = (box(MX - 15, MX + 15, -RAIL_Y - 40, -RAIL_Y - 12, RAIL_Z - 15, RAIL_Z + 15)
       + tube3((MX, -RAIL_Y - 40, RAIL_Z), (MX, -ROW_SPACING + 30, 75), 10))
marker = arm + ycyl(MX, -ROW_SPACING, 70, 70, 6) + ycyl(MX, -ROW_SPACING + 10, 70, 12, 30)

parts = [
    Part("Ground drive wheel, 300 mm lugged", wheel, "#374151", 1, (260, 0, 0)),
    Part("Chain drive, sprockets and chain", chain, "#B45309", 2, (0, -260, -60)),
    Part("Chain guard", guard, "#FBBF24", 3, (-150, -330, 330)),
    Part("Seed hopper, about 2 L", hopper, "#E5E7EB", 4, (0, 0, 330)),
    Part("Metering housing, shaft and bearings", meter, "#94A3B8", 5, (0, 170, 90)),
    Part("Printed seed plate (per crop)", plate, "#0F766E", 6, (0, -170, 240)),
    Part("Singulator brush", brush, "#7C3AED", 7, (520, -250, 120)),
    Part("Seed drop tube", drop, "#0EA5E9", 8, (80, 0, -90)),
    Part("Furrow opener and depth bracket", opener, "#6B7280", 9, (140, 0, -200)),
    Part("Covering chains", cover, "#57534E", 10, (-280, 0, -200)),
    Part("Press wheel, 200 mm concave", press, "#1F2937", 11, (-220, 0, -40)),
    Part("Steel frame", frame, "#4B5563", 12, (0, 0, 0)),
    Part("Handle, height adjustable", handle, "#115E59", 13, (350, 450, -150)),
    Part("Row marker arm (row-spacing kit)", marker, "#D97706", 14, (0, -250, 0)),
]

render_all(
    parts, project="SeedLine", title="Push seeder concept", dwg_no="SDL-DWG-010",
    key_figures=["Single row; 300 mm ground wheel drives the plate by chain",
                 "Spacing = 942 mm / (cells x ratio); about 20 to 390 mm",
                 "Printed plates: 3 to 36 cells, swapped by hand",
                 "About 0.14 ha/h at 0.75 m rows, 3 km/h (estimate)",
                 "About 14 kg; parts about $223 with marker (indicative)"],
    cut_exclude=("Row marker arm (row-spacing kit)", "Handle, height adjustable"),
    flow={"title": "seeds per 100 m of row, maize plate at 250 mm; 16 doubles add seeds (all values are estimates)",
          "unit": "seeds",
          "stages": [("Cells passing outlet", 400), ("Filled cells", 380),
                     ("Seeds dropped", 396), ("Seeds covered, firmed", 392)],
          "losses": [(0, "Empty cells, misses (5 %)", 20), (2, "Bounced, left exposed (1 %)", 4)]},
)
