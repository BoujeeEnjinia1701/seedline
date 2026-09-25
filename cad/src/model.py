"""SeedLine parametric model (build123d), TRL 3 massing-plus level.

Run from the repo root:  python cad/src/model.py
Exports STEP into cad/step and STL into cad/stl:
  seedline-assembly     whole seeder, marker deployed at the set row spacing
  seedline-plate-maize  printed seed plate for the design case (4 cells, maize)
  seedline-hopper       seed hopper (printed or cut from HDPE)
  seedline-housing      metering housing (printed)

Coordinates in mm. X is the direction of travel (+X forward), Y is across the row,
Z is up, ground at Z = 0. The seed row runs along the X axis at Y = 0. The chain
drive sits on the -Y side. Correct interfaces and main dimensions; not fabrication
detail. PRELIMINARY, NOT FOR FABRICATION.

Decisions carried by this model (Amish, 2026-09-25, SDL-DDR-001): vertical cell plate
on a transverse shaft driven by #35 chain (item 1), front drive wheel and rear press
wheel (item 7), 12, 15 or 18 T wheel sprocket with a spring idler (item 4), bolted
square-tube frame (item 8), telescoping marker arm as the row-spacing kit (item 3).
"""
import copy
import math
from pathlib import Path

from build123d import (Box, Cylinder, Compound, Plane, Pos, Rectangle, Rot, Solid, Vector,
                       export_step, export_stl, loft)

# ---------------------------------------------------------------------------
# Parameters (mm unless noted). Edit these, not the geometry below.
# ---------------------------------------------------------------------------
PARAMS = {
    # Wheels
    "WHEEL_D": 300.0,        # drive wheel diameter over the lug tips
    "WHEEL_W": 45.0,
    "LUG_H": 10.0,           # lug height above the rim
    "N_LUGS": 18,
    "PRESS_D": 200.0,
    "PRESS_W": 70.0,
    "AXLE_D": 16.0,
    # Layout along the row
    "X_WHEEL": 0.0,
    "X_METER": -270.0,
    "X_PRESS": -580.0,
    # Frame: two side rails of square tube, bolted
    "RAIL_Y": 60.0,          # rail centerline offset from the row
    "RAIL_Z": 215.0,         # rail centerline height
    "RAIL_S": 25.0,          # square tube size
    "RAIL_T": 1.5,           # tube wall (SDL-CAL-001 section 7)
    # Metering
    "PLATE_D": 120.0,
    "Z_SHAFT": 245.0,
    "SHAFT_D": 12.0,
    "N_CELLS": 4,            # design case: maize, 250 mm target
    "SEED": (12.0, 8.0, 5.0),  # maize kernel length, width, thickness
    # Drive: #35 chain, 9.525 mm pitch
    "PITCH": 9.525,
    "T_PLATE": 15,
    "T_WHEEL": 15,           # 12, 15 or 18 (ratio 0.8, 1.0, 1.2)
    "Y_CHAIN": -92.0,
    # Opener
    "DEPTH": 50.0,           # sowing depth below the seedbed surface, 10 to 60 in 10 mm steps
    # Handle
    "GRIP_H": 950.0,         # grip height, 850 to 1,050 by telescoping
    "HANDLE_ANGLE": 50.0,    # degrees above the ground
    # Row marker (row-spacing kit)
    "ROW_SPACING": 750.0,    # maize on 0.75 m rows
    "MARKER_D": 140.0,
}

NAMES = {
    1: "Ground drive wheel, 300 mm lugged",
    2: "Chain drive, sprockets, chain and idler",
    3: "Chain guard",
    4: "Seed hopper",
    5: "Metering housing, shaft and bearings",
    6: "Printed seed plate (per crop)",
    7: "Singulator brush",
    8: "Seed drop tube",
    9: "Furrow opener and depth bracket",
    10: "Covering chains",
    11: "Press wheel, 200 mm concave",
    12: "Steel frame, bolted",
    13: "Handle, height adjustable",
    14: "Row marker arm (row-spacing kit)",
}


# ---------------------------------------------------------------------------
# Derived quantities (also used by docs/04-calcs/sizing.py)
# ---------------------------------------------------------------------------
def sprocket_pd(teeth, pitch=None):
    """Pitch diameter of a roller chain sprocket."""
    p = pitch or PARAMS["PITCH"]
    return p / math.sin(math.pi / teeth)


def centers():
    """(x, z) of the wheel axle and the plate shaft in the chain plane."""
    P = PARAMS
    return (P["X_WHEEL"], P["WHEEL_D"] / 2), (P["X_METER"], P["Z_SHAFT"])


def center_distance():
    (ax, az), (bx, bz) = centers()
    return math.hypot(bx - ax, bz - az)


def chain_links_exact(t1, t2, c=None, pitch=None):
    """Chain length in pitches for two sprockets at center distance c (standard formula)."""
    p = pitch or PARAMS["PITCH"]
    c = c or center_distance()
    return 2 * c / p + (t1 + t2) / 2 + ((t2 - t1) / (2 * math.pi)) ** 2 * p / c


def cell_size(seed=None):
    """Cell length along the rim, radial depth and plate thickness for a seed (L, W, T)."""
    L, W, T = seed or PARAMS["SEED"]
    return 1.15 * L + 0.5, 1.05 * W + 0.3, max(6.0, math.ceil(1.2 * T))


def cell_circle_d(seed=None):
    """Diameter of the circle through the seed centers."""
    _, depth, _ = cell_size(seed)
    return PARAMS["PLATE_D"] - depth


def handle_points():
    """Handle base and grip points (x, z)."""
    P = PARAMS
    bx, bz = P["X_PRESS"] - 30, P["RAIL_Z"]
    gx = bx - (P["GRIP_H"] - bz) / math.tan(math.radians(P["HANDLE_ANGLE"]))
    return (bx, bz), (gx, P["GRIP_H"])


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
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


# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------
def make_plate(n_cells=None, seed=None, at=None):
    """Printed vertical seed plate: disc with n rim cells sized to the seed, 12 mm D-bore.
    n_cells of 1 or 2 is a skip-cell plate (SDL-DDR-001 item 5)."""
    P = PARAMS
    n = n_cells or P["N_CELLS"]
    clen, cdep, thk = cell_size(seed)
    x, z = at or (0.0, 0.0)
    r = P["PLATE_D"] / 2
    plate = ycyl(x, 0, z, r, thk)
    for k in range(n):
        t = 2 * math.pi * k / n
        c = (x + (r - cdep / 2) * math.cos(t), z + (r - cdep / 2) * math.sin(t))
        cutter = Pos(c[0], 0, c[1]) * Rot(0, -math.degrees(t), 0) * Box(cdep + 1, thk + 2, clen)
        plate = plate - cutter
    bore = ycyl(x, 0, z, P["SHAFT_D"] / 2 + 0.2, thk + 2) - box(x - 10, x + 10, -thk, thk, z + 4.6, z + 10)
    return plate - bore


def hopper_solids():
    """Outer shell and inner cavity of the hopper: straight upper box on a funnel to a throat."""
    P = PARAMS
    x = P["X_METER"]
    z0, z1, z2 = 330.0, 390.0, 490.0       # throat, top of funnel, rim
    t = 3.0

    def frustum(ax, ay, bx, by, za, zb):
        return loft([Pos(x, 0, za) * Rectangle(ax, ay), Pos(x, 0, zb) * Rectangle(bx, by)])
    outer = frustum(60 + 2 * t, 30 + 2 * t, 170, 120, z0, z1) + box(x - 85, x + 85, -60, 60, z1, z2)
    inner = frustum(60, 30, 170 - 2 * t, 120 - 2 * t, z0 - 0.01, z1) + box(x - 85 + t, x + 85 - t, -60 + t, 60 - t, z1, z2 + 0.01)
    return outer, inner


def hopper_volume_l():
    _, inner = hopper_solids()
    return inner.volume / 1e6


def build_parts():
    P = PARAMS
    xw, xm, xp = P["X_WHEEL"], P["X_METER"], P["X_PRESS"]
    ry, rz, rs = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
    zw = P["WHEEL_D"] / 2
    zp = P["PRESS_D"] / 2
    zs = P["Z_SHAFT"]
    yc = P["Y_CHAIN"]
    parts = {}

    # 1 Ground drive wheel: rim, lugs, hub and 16 mm axle through both drop plates to the chain plane
    rim_r = zw - P["LUG_H"]
    wheel = ycyl(xw, 0, zw, rim_r, P["WHEEL_W"]) - ycyl(xw, 0, zw, rim_r - 25, P["WHEEL_W"] - 16)
    wheel = wheel + ycyl(xw, 0, zw, 22, P["WHEEL_W"])
    for k in range(P["N_LUGS"]):
        t = 2 * math.pi * k / P["N_LUGS"]
        wheel = wheel + (Pos(xw + (rim_r + P["LUG_H"] / 2) * math.cos(t), 0, zw + (rim_r + P["LUG_H"] / 2) * math.sin(t))
                         * Rot(0, -math.degrees(t), 0) * Box(P["LUG_H"], P["WHEEL_W"], 12))
    axle_y0, axle_y1 = yc - 8, ry + 25
    wheel = wheel + Pos(xw, (axle_y0 + axle_y1) / 2, zw) * Rot(90, 0, 0) * Cylinder(P["AXLE_D"] / 2, axle_y1 - axle_y0)
    parts[1] = wheel

    # 2 Chain drive: wheel and plate sprockets at their pitch radii, both strands, spring idler
    (ax, az), (bx, bz) = centers()
    ra, rb = sprocket_pd(P["T_WHEEL"]) / 2, sprocket_pd(P["T_PLATE"]) / 2
    dx, dz = bx - ax, bz - az
    L = math.hypot(dx, dz)
    ux, uz = dx / L, dz / L
    beta = math.asin((ra - rb) / L)
    strands = []
    for s in (1, -1):
        # external tangent: normal rotated from the center line by (90 deg - beta)
        ang = math.atan2(uz, ux) + s * (math.pi / 2 - beta)
        nx, nz = math.cos(ang), math.sin(ang)
        strands.append(tube3((ax + ra * nx, yc, az + ra * nz), (bx + rb * nx, yc, bz + rb * nz), 3.5))
    sprockets = ycyl(ax, yc, az, ra + 4, 5) + ycyl(bx, yc, bz, rb + 4, 5)
    mid = ((ax + bx) / 2, (az + bz) / 2)
    ix, iz = mid[0] + 20 * uz, mid[1] - 20 * ux          # idler below the lower strand
    idler = ycyl(ix, yc, iz - 12, 14, 5) + tube3((ix, yc, iz - 12), (ix, -ry - rs / 2, rz - rs / 2), 4)
    parts[2] = sprockets + union(strands) + idler

    # 3 Chain guard: band around the chain loop, open on the inboard side
    def stadium(r, w):
        ang = math.degrees(math.atan2(dz, dx))
        body = Pos(mid[0], yc, mid[1]) * Rot(0, -ang, 0) * Box(L, w, 2 * r)
        return body + ycyl(ax, yc, az, r, w) + ycyl(bx, yc, bz, r, w)
    rg = max(ra, rb) + 16
    band = stadium(rg + 3, 24) - stadium(rg, 30)
    # outboard face plate so fingers cannot reach the sprockets from the side
    face = Pos(0, -11, 0) * stadium(rg + 3, 2)
    parts[3] = band + face

    # 4 Seed hopper
    outer, inner = hopper_solids()
    parts[4] = outer - inner

    # 5 Metering housing around the plate, with side door boss, shaft and two flange bearings
    _, _, thk = cell_size()
    hx0, hx1, hz0, hz1 = xm - 80, xm + 80, 165.0, 330.0
    slot = thk + 3
    housing = box(hx0, hx1, -slot / 2 - 6, slot / 2 + 6, hz0, hz1) - box(hx0 + 6, hx1 - 6, -slot / 2, slot / 2, hz0 + 6, hz1 + 1)
    housing = housing - box(xm + 20, xm + 44, -slot / 2, slot / 2, hz0 - 1, hz0 + 7)        # outlet to the drop tube
    housing = housing - box(xm - 60, xm + 60, slot / 2 - 1, slot / 2 + 7, hz0 + 20, hz1 - 20)  # side door opening
    door = box(xm - 64, xm + 64, slot / 2 + 6, slot / 2 + 9, hz0 + 16, hz1 - 16) + ycyl(xm, slot / 2 + 16, zs, 14, 14)
    shaft = Pos(xm, (yc - 6 + ry + 20) / 2, zs) * Rot(90, 0, 0) * Cylinder(P["SHAFT_D"] / 2, ry + 26 - yc)
    bearings = union([ycyl(xm, y, zs, 18, 10) + box(xm - 24, xm + 24, y - 3, y + 3, rz + rs / 2, zs + 22)
                      for y in (-ry - rs / 2 - 5, ry + rs / 2 + 5)])
    parts[5] = housing + door + shaft + bearings

    # 6 Printed seed plate for the design case
    parts[6] = make_plate(at=(xm, zs))

    # 7 Singulator brush on its holder, at the top rear of the plate
    r = P["PLATE_D"] / 2
    parts[7] = box(xm - 34, xm - 8, -slot / 2, slot / 2, zs + r - 3, zs + r + 22) + box(xm - 40, xm - 2, -slot / 2 - 6, slot / 2 + 6, zs + r + 22, zs + r + 28)

    # 8 Seed drop tube from the housing outlet into the opener boot
    parts[8] = tube3((xm + 32, 0, hz0), (xm + 12, 0, 20 - P["DEPTH"] + 30), 10) - tube3((xm + 32, 0, hz0 + 1), (xm + 12, 0, -P["DEPTH"] + 49), 8)

    # 9 Furrow opener: runner shoe and boot on a steel shank in a slotted clamp bracket
    d = P["DEPTH"]
    shank = box(xm + 45, xm + 65, -6, 6, -d + 40, rz + 60)
    for k in range(6):   # 10 mm step holes for 10 to 60 mm depth
        shank = shank - Pos(xm + 55, 0, rz + 5 + 10 * k) * Rot(90, 0, 0) * Cylinder(3.5, 20)
    clamp = box(xm + 38, xm + 72, -ry - rs / 2, ry + rs / 2, rz + rs / 2, rz + rs / 2 + 6) + box(xm + 38, xm + 72, -12, 12, rz + rs / 2 + 6, rz + 50)
    shoe = box(xm - 30, xm + 70, -9, 9, -d, -d + 45) + Pos(xm + 88, 0, -d + 18) * Rot(0, 35, 0) * Box(40, 18, 30)
    parts[9] = shank + clamp + shoe

    # 10 Covering chains on a bracket behind the opener
    cover = union([tube3((xm - 60, y, 60), (xm - 210, y * 1.6, 3), 4) for y in (-22, 22)])
    parts[10] = cover + box(xm - 70, xm - 50, -30, 30, 55, rz - rs / 2)

    # 11 Press wheel, concave tread
    press = ycyl(xp, 0, zp, zp, P["PRESS_W"]) - ycyl(xp, 0, zp, zp + 1, 20) + ycyl(xp, 0, zp, zp - 8, 22)
    press = press - ycyl(xp, 0, zp, zp - 30, P["PRESS_W"] - 20) + ycyl(xp, 0, zp, 20, P["PRESS_W"])
    press = press + ycyl(xp, 0, zp, P["AXLE_D"] / 2, 2 * ry + 50)
    parts[11] = press

    # 12 Bolted frame: two side rails, three cross members, axle drop plates, hopper posts, corner brackets
    x_front, x_rear = xw + 60, xp - 40
    rails = union([box(x_rear, x_front, y - rs / 2, y + rs / 2, rz - rs / 2, rz + rs / 2) for y in (-ry, ry)])
    xs_cross = (x_front - rs / 2, xm - 130, x_rear + rs / 2)
    cross = union([box(x - rs / 2, x + rs / 2, -ry + rs / 2, ry - rs / 2, rz - rs / 2, rz + rs / 2) for x in xs_cross])
    drops = union([box(xw - 20, xw + 20, y - 3, y + 3, zw - 20, rz + rs / 2) for y in (-ry - rs / 2 - 3, ry + rs / 2 + 3)]
                  + [box(xp - 20, xp + 20, y - 3, y + 3, zp - 20, rz + rs / 2) for y in (-ry - rs / 2 - 3, ry + rs / 2 + 3)])
    posts = union([box(xm + sx - 10, xm + sx + 10, sy - 10, sy + 10, rz + rs / 2, 392)
                   for sx in (-75, 75) for sy in (-ry + 5, ry - 5)])
    brackets = union([box(x - 22, x + 22, y - 1.5, y + 1.5, rz - rs / 2, rz + rs / 2)
                      for x in xs_cross for y in (-ry + rs / 2 + 1.5, ry - rs / 2 - 1.5)])
    parts[12] = rails + cross + drops + posts + brackets

    # 13 Handle: two tubes from the rear of the rails to a cross grip, with a brace
    (hbx, hbz), (gx, gz) = handle_points()
    spread = 4.2
    handle = union([tube3((hbx, y, hbz), (gx, y * spread, gz), 12.5) for y in (-ry, ry)])
    handle = handle + tube3((gx - 10, -ry * spread - 45, gz), (gx - 10, ry * spread + 45, gz), 12.5)
    mx, mz = hbx + (gx - hbx) * 0.45, hbz + (gz - hbz) * 0.45
    parts[13] = handle + tube3((mx, -ry * (1 + 0.45 * (spread - 1)), mz), (mx, ry * (1 + 0.45 * (spread - 1)), mz), 9)

    # 14 Row marker arm on the front cross member, disc at the set row spacing on the -Y side
    mxk = x_front - rs / 2
    arm = (box(mxk - 15, mxk + 15, -ry - 40, -ry - rs / 2, rz - 15, rz + 15)
           + tube3((mxk, -ry - 40, rz), (mxk, -P["ROW_SPACING"] + 30, P["MARKER_D"] / 2 + 5), 10))
    rm = P["MARKER_D"] / 2
    parts[14] = arm + ycyl(mxk, -P["ROW_SPACING"], rm, rm, 5) + ycyl(mxk, -P["ROW_SPACING"] + 12, rm, 14, 26)
    return parts


def assembly(parts=None):
    parts = parts or build_parts()
    # copies, so the parts keep no parent and can still be exported on their own
    return Compound(children=[copy.copy(parts[k]) for k in sorted(parts)])


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    step_dir, stl_dir = root / "cad/step", root / "cad/stl"
    step_dir.mkdir(parents=True, exist_ok=True)
    stl_dir.mkdir(parents=True, exist_ok=True)
    parts = build_parts()
    asm = assembly(parts)
    exports = {
        "seedline-assembly": asm,
        "seedline-plate-maize": make_plate(),
        "seedline-hopper": parts[4],
        "seedline-housing": parts[5],
    }
    for name, shape in exports.items():
        export_step(shape, str(step_dir / f"{name}.step"))
        export_stl(shape, str(stl_dir / f"{name}.stl"))
    bb = asm.bounding_box()
    print(f"assembly {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (L x W x H, marker deployed)")
    cl, cd, th = cell_size()
    print(f"center distance {center_distance():.1f} mm; hopper {hopper_volume_l():.2f} L; "
          f"maize cell {cl:.1f} x {cd:.1f} mm, plate {th:.0f} mm thick")
    print("exported:", ", ".join(exports))
