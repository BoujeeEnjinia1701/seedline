"""SeedLine parametric model (build123d), kit 1.9 interface, TRL 3 (stage P3, detail level D3).

Run from the repo root:
    python .kit/cad_check.py --export  CAD fidelity check of both options; STEP per part (option A) and per assembly
    python cad/src/model.py            export STL into cad/stl, print key figures and the constructability checks
    python cad/src/model.py --check    print the constructability checks only (exit 1 if any fails)

Two concept options are modelled to D3 (STANDARDS section 24; Amish, 2026-10-24: "Detail every option"):

  A  Cell plate on a chain drive (the current design, CHOSEN until Amish decides SDL-DEC-001 D1): a 300 mm lugged
     ground wheel turns a printed vertical cell plate through a #35 roller chain; a runner opener cuts the furrow, each
     cell drops one seed, drag chains and a press wheel cover and firm the row. Built here in build_components().
  B  Punch wheel with a hub meter (alternative, not carried to the drawing, BOM or build plan): cad/src/punch_wheel.py.

STL exports in cad/stl (0.15 mm chord): seedline-assembly (made and bought parts, marker deployed), seedline-plate-maize
(printed seed plate, 4 cells), seedline-hopper, seedline-housing.

Coordinates in mm. X is the direction of travel (+X forward), Y is across the row, Z is up, ground at Z = 0. The seed
row runs along the X axis at Y = 0. The chain drive sits on the -Y side ("chain side"); +Y is the "door side".

Every component is a single made or bought piece (or a matched set of fixings, each a real ISO bolt, nut, washer,
screw, pin or insert from .kit/cad_parts.py and cad/src/sdl_parts.py), held in build_components(). components("A")
turns them into cad_parts.part() dicts, one per piece. build_parts() groups them by bill-of-materials line for the
drawing and the calculation note. checks() tests, with build123d, that parts which must touch do touch and parts
which must stay apart are apart.

Decisions carried by this model (Amish, 2026-09-25, SDL-DDR-001): vertical cell plate on a transverse shaft driven by
#35 chain (item 1), front drive wheel and rear press wheel (item 7), 12, 15 or 18 T wheel sprocket with a spring idler
(item 4), bolted square-tube frame (item 8), telescoping marker arm as the row-spacing kit (item 3). Accepted by Amish,
2026-09-25 (SDL-DDR-002): lighter 22 x 1.2 mm handle tube (R11); the 12 and 18 T wheel sprockets move to an optional
ratio kit (R17). Design for construction (SDL-DDR-003, accepted 2026-10-02). Kit 1.9 fixes made under Amish's standing
instruction of 2026-10-23 (SDL-DEC-001 F1 to F8): door and door screws, hub cross bolt position, tensioner pivot screw,
hopper insert holes, bought wheel envelopes, mass fix, rail bolt through the handle tab.
CONCEPT, NOT FOR FABRICATION.
"""
import copy
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from build123d import (Box, Cylinder, Compound, Plane, Polyline, Pos, Rectangle, Rot, Solid, Vector,
                       export_stl, extrude, loft, make_face)

HERE = Path(__file__).resolve().parent
for _p in (str(HERE), str(HERE.parents[1] / ".kit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import cad_parts as cpl  # noqa: E402
import sdl_parts as sp  # noqa: E402
from sdl_parts import fix_compound  # noqa: E402

# ---------------------------------------------------------------------------
# Parameters (mm unless noted). Edit these, not the geometry below.
# ---------------------------------------------------------------------------
PARAMS = {
    # Wheels
    "WHEEL_D": 300.0,        # drive wheel diameter over the lug tips
    "WHEEL_W": 45.0,
    "WHEEL_RIM_T": 2.0,      # bought disc wheel rim and web, 2 mm pressed steel (kit 1.9 D3 model, SDL-DEC-001 F5)
    "LUG_H": 10.0,           # lug height above the rim
    "N_LUGS": 18,
    "PRESS_D": 200.0,
    "PRESS_W": 70.0,
    "AXLE_D": 16.0,
    "CROSS_BOLT_Y": 15.0,    # wheel hub cross bolt, off the disc web (kit 1.9 D3 model, SDL-DEC-001 F2; was 0, at the web)
    # Layout along the row
    "X_WHEEL": 0.0,
    "X_METER": -270.0,
    "X_PRESS": -580.0,
    # Frame: two side rails of square tube, bolted
    "RAIL_Y": 60.0,          # rail centerline offset from the row
    "RAIL_Z": 215.0,         # rail centerline height
    "RAIL_S": 25.0,          # square tube size
    "RAIL_T": 1.5,           # tube wall (SDL-CAL-001 section 7)
    "X_FRONT": 80.0,         # front end of the rails (DDR-003: 20 mm longer for the marker plate)
    "X_REAR": -620.0,        # rear end of the rails
    "X_MID": -400.0,         # middle cross member centre
    "OPENER_BAR_X": -171.0,  # opener cross member centre (40 x 20 x 1.5 rectangular tube, 40 tall)
    "DROP_T": 3.0,           # axle drop plates (SDL-DEC-001 F6, mass: was 4)
    "BPLATE_T": 3.0,         # bearing plate on the chain-side rail (F6: was 4)
    "UPRIGHT_T": 2.0,        # hopper uprights, 20 mm flat bar (F6: was 3)
    # Metering
    "PLATE_D": 120.0,
    "Z_SHAFT": 245.0,
    "SHAFT_D": 12.0,
    "SLOT_W": 13.0,          # housing slot width (SDL-DEC-001, 2026-10-02: one slot for 6, 8 and 10 mm plates)
    "SLOT_GAP": 1.5,
    "DOOR": (-80.0, 66.0, 165.0, 315.0),   # door x from and to (from the shaft) and z from and to; 146 x 150 (SDL-DEC-001 F1; was 136 x 140)
    "DOOR_SCREWS": ((-73.0, 300.0), (54.0, 172.0)),   # (x from the shaft, z) of the two M4 thumb screws (F1; were (-58, 300), (54, 190))         # clearance each side of a plate, kept by the printed side liners
    "HUB_Y": 14.0,           # plate hub end, from the plate centre plane (the hub is longer on a thinner plate)
    "LINER_R": 61.0,         # radius of the printed side liners
    "LINER_DOOR_T": 2.0,     # door-side liner thickness
    "N_CELLS": 4,            # design case: maize, 250 mm target
    "SEED": (12.0, 8.0, 5.0),  # maize kernel length, width, thickness
    # Drive: #35 chain, 9.525 mm pitch
    "PITCH": 9.525,
    "T_PLATE": 15,
    "T_WHEEL": 15,           # base 15 (ratio 1.0); 12 or 18 T in the optional ratio kit (0.8, 1.2)
    "T_IDLER": 10,
    "Y_CHAIN": -104.0,       # chain plane (DDR-003: was -92, moved out to clear the outboard bearing)
    "IDLER_PIVOT": (-140.0, 215.0),   # spring tensioner pivot on the chain-side rail (x, z)
    "IDLER_X": -100.0,       # where the idler meets the slack (lower) strand
    "IDLER_DEFL": 12.0,      # strand deflection drawn; the tensioner covers 0 to 45 mm
    # Opener
    "DEPTH": 50.0,           # sowing depth below the seedbed surface, 10 to 60 in 10 mm steps
    "SHANK": (20.0, 12.0, 305.0),     # along X, across Y, length
    "BOOT": (70.0, 80.0, 3.0),        # boot side plate length (X), height, thickness
    # Hopper
    "HOPPER_Z0": 340.0,      # throat bottom (DDR-003: was 330; the throat now sits in a collar on the housing)
    # Handle
    "GRIP_H": 950.0,         # grip height, 850 to 1,050 by telescoping
    "HANDLE_ANGLE": 50.0,    # degrees above the ground
    "HANDLE_OD": 22.0,       # round tube outside diameter (SDL-DDR-002; was 25)
    "HANDLE_T": 1.2,         # round tube wall (SDL-DDR-002; was 1.5)
    "GRIP_Y": 252.0,         # side tube top, each side of the row
    # Row marker (row-spacing kit)
    "ROW_SPACING": 750.0,    # maize on 0.75 m rows
    "MARKER_D": 140.0,
    "MARKER_T": 1.5,         # marker disc steel (F6: was 2)
}

NAMES = {
    1: "Ground drive wheel, 300 mm lugged",
    2: "Chain drive, sprockets, chain and tensioner",
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
KITS = {14: "Row marker kit", 16: "Optional ratio kit"}   # optional kits (BOM lines); the concept options are OPTIONS below


@dataclass
class Comp:
    """One component: a single made or bought piece, or a matched set of fixings."""
    name: str
    shape: object
    bom: int
    kind: str          # "made", "bought" or "fixing"


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
    """Handle base and grip points (x, z) on the side-tube axis."""
    P = PARAMS
    bx, bz = P["X_PRESS"] - 30, P["RAIL_Z"]
    gx = bx - (P["GRIP_H"] - bz) / math.tan(math.radians(P["HANDLE_ANGLE"]))
    return (bx, bz), (gx, P["GRIP_H"])


def frame_y():
    """Y positions: rail inner and outer faces, drop plate outer face, handle base."""
    P = PARAMS
    ri = P["RAIL_Y"] - P["RAIL_S"] / 2
    ro = P["RAIL_Y"] + P["RAIL_S"] / 2
    return {"rail_in": ri, "rail_out": ro, "drop_out": ro + P["DROP_T"],
            "handle_base": ro + P["DROP_T"] + P["HANDLE_OD"] / 2}


def handle_geometry():
    """Side tube length, grip tube length, brace length (mm) for the mass build-up."""
    P = PARAMS
    (bx, bz), (gx, gz) = handle_points()
    yb = frame_y()["handle_base"]
    side = math.dist((bx, yb, bz), (gx, P["GRIP_Y"], gz))
    yb3 = yb + 0.3 * (P["GRIP_Y"] - yb)
    return {"side": side, "grip": 2 * (P["GRIP_Y"] + 45), "brace": 2 * (yb3 - 12.4), "tab": 60.0}


def opener_front_x():
    """Front face of the opener shank (the leading edge of the opener in the soil)."""
    return PARAMS["OPENER_BAR_X"] - 10.0


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def tube3(a, b, r):
    a = Vector(*a); b = Vector(*b); d = b - a
    return Solid.make_cylinder(r, d.length, Plane(origin=a, z_dir=d.normalized()))


def htube3(a, b, ro, ri):
    """Hollow round tube between two points."""
    return tube3(a, b, ro) - tube3(a, b, ri)


def ycyl(x, y, z, r, w):
    """Cylinder with its axis along Y, centered at (x, y, z)."""
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, w)


def ycyl2(x, z, r, y0, y1):
    """Cylinder along Y from y0 to y1."""
    return ycyl(x, (y0 + y1) / 2, z, r, abs(y1 - y0))


def xcyl2(y, z, r, x0, x1):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, abs(x1 - x0))


def zcyl2(x, y, r, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, abs(z1 - z0))


def union(shapes):
    out = None
    for s in shapes:
        if s is None:
            continue
        out = s if out is None else out + s
    return out


def sq_tube_y(x, z, s_x, s_z, t, y0, y1):
    """Rectangular tube along Y: outside s_x (along X) by s_z (along Z), wall t."""
    return box(x - s_x / 2, x + s_x / 2, y0, y1, z - s_z / 2, z + s_z / 2) - \
        box(x - s_x / 2 + t, x + s_x / 2 - t, y0 - 1, y1 + 1, z - s_z / 2 + t, z + s_z / 2 - t)


def sq_tube_x(y, z, s, t, x0, x1):
    return box(x0, x1, y - s / 2, y + s / 2, z - s / 2, z + s / 2) - \
        box(x0 - 1, x1 + 1, y - s / 2 + t, y + s / 2 - t, z - s / 2 + t, z + s / 2 - t)


def hull2d(pts):
    """Convex hull of 2D points (monotone chain)."""
    pts = sorted(set((round(x, 4), round(y, 4)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    return lo[:-1] + hi[:-1]


def xz_prism(pts, y0, y1):
    """Prism from a closed polygon in the XZ plane, between y0 and y1."""
    w = Polyline(*[(x, z) for x, z in pts], close=True)
    f = make_face(w)
    s = extrude(f, amount=abs(y1 - y0))          # in the XY plane, along +Z
    # map local (x, y, z) -> world (x, y0 + z, y): rotate the XY plane onto XZ
    s = Rot(90, 0, 0) * s                        # (x, y, z) -> (x, -z, y)
    return Pos(0, max(y0, y1), 0) * s


def circle_pts(cx, cz, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


# ---------------------------------------------------------------------------
# Parts used by more than one view
# ---------------------------------------------------------------------------
def make_plate(n_cells=None, seed=None, at=None):
    """Printed vertical seed plate: disc with n rim cells sized to the seed, 12 mm D-bore, and a
    20 mm hub on its chain-side face that runs in the housing wall (DDR-003).
    n_cells of 1 or 2 is a skip-cell plate (SDL-DDR-001 item 5)."""
    P = PARAMS
    n = n_cells or P["N_CELLS"]
    clen, cdep, thk = cell_size(seed)
    x, z = at or (0.0, 0.0)
    r = P["PLATE_D"] / 2
    plate = ycyl(x, 0, z, r, thk) + ycyl2(x, z, 10.0, -P["HUB_Y"], -thk / 2)
    for k in range(n):
        t = 2 * math.pi * k / n
        c = (x + (r - cdep / 2) * math.cos(t), z + (r - cdep / 2) * math.sin(t))
        cutter = Pos(c[0], 0, c[1]) * Rot(0, -math.degrees(t), 0) * Box(cdep + 1, thk + 2, clen)
        plate = plate - cutter
    bore = ycyl2(x, z, P["SHAFT_D"] / 2 + 0.2, -P["HUB_Y"] - 2, thk / 2 + 2) - \
        box(x - 10, x + 10, -P["HUB_Y"] - 2, thk + 2, z + 4.6, z + 10)
    return plate - bore


def liner_sizes(seed=None):
    """(chain-side liner thickness, door-side liner thickness, door-side liner inner face y) for a plate.
    The 13 mm slot is wider than the plate by SLOT_GAP on each side plus the liners."""
    P = PARAMS
    _, _, thk = cell_size(seed)
    t_chain = max(0.0, (P["SLOT_W"] - thk - 2 * P["SLOT_GAP"]) / 2)
    return t_chain, P["LINER_DOOR_T"], thk / 2 + P["SLOT_GAP"]


def make_liners(seed=None, at=None):
    """Printed side liners that keep the seed in a slot only as wide as the plate (SDL-DEC-001, 2026-10-02).
    Returns (chain-side liner or None, door-side liner). The chain-side liner lies on the slot wall and is
    pegged into it; the door-side liner stands off the door on two pegs and is clamped by the door."""
    P = PARAMS
    x, z = at or (P["X_METER"], P["Z_SHAFT"])
    t_c, t_d, y_in = liner_sizes(seed)
    hy = P["SLOT_W"] / 2 + 6.0
    rl = P["LINER_R"]
    notch = box(x - 80, x - 30, -50, 50, z + 32.0, z + 48.0)          # clear of the singulator brush strip

    def disc(y0, y1):
        return ycyl2(x, z, rl, y0, y1) - ycyl2(x, z, 11.0, y0 - 1, y1 + 1) - notch

    chain = None
    if t_c > 0.05:
        y1 = -y_in
        chain = disc(y1 - t_c, y1)
        chain = chain + union([ycyl2(x + dx, z, 1.5, y1 - t_c - 4.0, y1 - t_c) for dx in (-48.0, 48.0)])
    door = disc(y_in, y_in + t_d)
    door = door + union([ycyl2(x + dx, z, 2.5, y_in + t_d, hy) for dx in (-48.0, 48.0)])
    return chain, door


def hopper_solids():
    """Outer shell and inner cavity of the hopper: straight upper box on a funnel to a throat."""
    P = PARAMS
    x = P["X_METER"]
    z0 = P["HOPPER_Z0"]
    zn = z0 + 12.0                       # straight neck that sits in the housing collar (DDR-003)
    z1, z2 = zn + 60.0, zn + 160.0       # top of funnel, rim
    t = 3.0

    def frustum(ax, ay, bx, by, za, zb):
        return loft([Pos(x, 0, za) * Rectangle(ax, ay), Pos(x, 0, zb) * Rectangle(bx, by)])
    outer = box(x - 30 - t, x + 30 + t, -15 - t, 15 + t, z0, zn) + frustum(60 + 2 * t, 30 + 2 * t, 170, 120, zn, z1) + box(x - 85, x + 85, -60, 60, z1, z2)
    inner = box(x - 30, x + 30, -15, 15, z0 - 0.01, zn + 0.01) + frustum(60, 30, 170 - 2 * t, 120 - 2 * t, zn, z1) + box(x - 85 + t, x + 85 - t, -60 + t, 60 - t, z1, z2 + 0.01)
    return outer, inner


def hopper_volume_l():
    _, inner = hopper_solids()
    return inner.volume / 1e6


def chain_path(p=None):
    """Tangent points of the chain and the tensioner idler centre, in the chain plane (x, z)."""
    P = p or PARAMS
    (ax, az), (bx, bz) = centers()
    ra, rb = sprocket_pd(P["T_WHEEL"]) / 2, sprocket_pd(P["T_PLATE"]) / 2
    dx, dz = bx - ax, bz - az
    L = math.hypot(dx, dz)
    ux, uz = dx / L, dz / L
    beta = math.asin((ra - rb) / L)
    tang = {}
    for s, key in ((1, "lower"), (-1, "upper")):
        ang = math.atan2(uz, ux) + s * (math.pi / 2 - beta)
        nx, nz = math.cos(ang), math.sin(ang)
        tang[key] = ((ax + ra * nx, az + ra * nz), (bx + rb * nx, bz + rb * nz))
    # the lower strand is the slack one (the drive sprocket's top runs forward, away from the plate sprocket)
    (p1, p2) = tang["lower"]
    if p1[1] > tang["upper"][0][1]:
        tang["lower"], tang["upper"] = tang["upper"], tang["lower"]
        (p1, p2) = tang["lower"]
    xi = P["IDLER_X"]
    t = (xi - p1[0]) / (p2[0] - p1[0])
    p0 = (xi, p1[1] + t * (p2[1] - p1[1]))
    sx, sz = p2[0] - p1[0], p2[1] - p1[1]
    sl = math.hypot(sx, sz)
    n_out = (sz / sl, -sx / sl)                     # outward (downward) normal of the lower strand
    if n_out[1] > 0:
        n_out = (-n_out[0], -n_out[1])
    ri = sprocket_pd(P["T_IDLER"]) / 2

    def idler(defl):
        c = (p0[0] + defl * n_out[0], p0[1] + defl * n_out[1])
        return c, (c[0] - ri * n_out[0], c[1] - ri * n_out[1])
    contact, icentre = idler(P["IDLER_DEFL"])
    _, imax = idler(45.0)
    return {"upper": tang["upper"], "lower": tang["lower"], "contact": contact, "idler": icentre,
            "idler_max": imax, "r_idler": ri, "ra": ra, "rb": rb}


def chain_pins(p=None):
    """Pin centres (x, z) of the 76-link chain round both sprockets and the tensioner idler, and the angle of the
    first seated pin on each sprocket (so the sprocket teeth can be turned to seat the rollers). On each sprocket the
    pins sit in the tooth seats, one per tooth; along the two strands they are spaced evenly (the tensioner takes up
    the difference from a whole number of pitches)."""
    P = p or PARAMS
    c = chain_path(P)
    (ax, az), (bx, bz) = centers()
    ra, rb = c["ra"], c["rb"]
    pitch = P["PITCH"]

    def ang(pt, cx, cz):
        return math.atan2(pt[1] - cz, pt[0] - cx)
    # wheel sprocket (front): from the lower tangent point round the front to the upper one, counterclockwise in XZ
    a_lo, a_up = ang(c["lower"][0], ax, az), ang(c["upper"][0], ax, az)
    while a_up < a_lo:
        a_up += 2 * math.pi
    dw = 2 * math.pi / P["T_WHEEL"]
    wheel = [a_lo + k * dw for k in range(int((a_up - a_lo) / dw) + 1)]
    # plate sprocket (rear): from the upper tangent point round the rear to the lower one
    b_up, b_lo = ang(c["upper"][1], bx, bz), ang(c["lower"][1], bx, bz)
    while b_lo < b_up:
        b_lo += 2 * math.pi
    dp = 2 * math.pi / P["T_PLATE"]
    plate = [b_up + k * dp for k in range(int((b_lo - b_up) / dp) + 1)]
    pw = [(ax + ra * math.cos(a), az + ra * math.sin(a)) for a in wheel]
    pp = [(bx + rb * math.cos(a), bz + rb * math.sin(a)) for a in plate]

    def strand(p0, p1, via=None):
        pts = [p0] + ([via] if via else []) + [p1]
        L = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        n = max(1, round(L / pitch))
        out = []
        for k in range(1, n):
            s_ = L * k / n
            for i in range(len(pts) - 1):
                seg = math.dist(pts[i], pts[i + 1])
                if s_ <= seg:
                    f = s_ / seg
                    out.append((pts[i][0] + f * (pts[i + 1][0] - pts[i][0]), pts[i][1] + f * (pts[i + 1][1] - pts[i][1])))
                    break
                s_ -= seg
        return out
    upper = strand(pw[-1], pp[0])                    # wheel top to plate top
    lower = strand(pp[-1], pw[0], via=c["contact"])  # plate bottom, over the idler, to the wheel bottom
    pins = pw + upper + pp + lower
    return pins, (wheel[0], plate[0])


def guard_outline(grow=0.0):
    """Inside outline of the chain guard in the XZ plane (convex hull of the drive, the sprockets
    with margin and the tensioner's full travel)."""
    (ax, az), (bx, bz) = centers()
    cp = chain_path()
    pts = circle_pts(ax, az, 43 + grow) + circle_pts(bx, bz, 43 + grow) + \
        circle_pts(*cp["idler_max"], cp["r_idler"] + 16 + grow) + circle_pts(*cp["idler"], cp["r_idler"] + 16 + grow)
    return hull2d(pts)


# ---------------------------------------------------------------------------
# Fixings: a bolt is drawn as a head and a nut on the outside faces; the hole is cut in the parts
# ---------------------------------------------------------------------------
def bolt_y(x, z, d, y_head, y_nut, nut=True, length=None, tag=""):
    """ISO 4017 bolt along Y with its head on the face y_head. With a nut: two ISO 7089 washers and an ISO 4032 nut
    on the face y_nut (grip |y_nut - y_head|). Without one (nut=False): a screw of 'length' with a washer under the head,
    into a tapped hole, a captive nut or an insert. Returns a list of (name, shape)."""
    sh = "+y" if y_nut > y_head else "-y"
    if nut:
        return sp.bolt_set(d, (x, y_head, z), sh, abs(y_nut - y_head), tag)
    return sp.screw_set(d, (x, y_head, z), sh, length or 5 * math.ceil((abs(y_nut - y_head) + 1.5 * d) / 5), tag)


def bolt_x(y, z, d, x_head, x_nut, nut=True, length=None, tag=""):
    sh = "+x" if x_nut > x_head else "-x"
    if nut:
        return sp.bolt_set(d, (x_head, y, z), sh, abs(x_nut - x_head), tag)
    return sp.screw_set(d, (x_head, y, z), sh, length or 5 * math.ceil((abs(x_nut - x_head) + 1.5 * d) / 5), tag)


def hole_y(x, z, d, y0=-400, y1=400):
    return ycyl2(x, z, d / 2, y0, y1)


def hole_x(y, z, d, x0=-1000, x1=400):
    return xcyl2(y, z, d / 2, x0, x1)


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------
def build_components(p=None, marker=True):
    """Every component of the seeder, keyed by a short name. Returns {key: Comp}."""
    P = p or PARAMS
    C = {}

    def add(key, name, shape, bom, kind):
        C[key] = Comp(name, shape, bom, kind)

    xw, xm, xp = P["X_WHEEL"], P["X_METER"], P["X_PRESS"]
    ry, rz, rs, rt = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"], P["RAIL_T"]
    zw, zp, zs = P["WHEEL_D"] / 2, P["PRESS_D"] / 2, P["Z_SHAFT"]
    yc = P["Y_CHAIN"]
    FY = frame_y()
    ri, ro, do_ = FY["rail_in"], FY["rail_out"], FY["drop_out"]
    rz0, rz1 = rz - rs / 2, rz + rs / 2
    dt, bt, ut = P["DROP_T"], P["BPLATE_T"], P["UPRIGHT_T"]
    xf, xr = P["X_FRONT"], P["X_REAR"]
    xo = P["OPENER_BAR_X"]
    ob0, ob1 = xo - 10, xo + 10                 # opener bar along X
    xmid = P["X_MID"]
    xu_f, xu_r = ob0 - 15.0, xm - 75.0          # hopper upright centres (front one shares the clip bolt)
    _, _, thk = cell_size()
    slot = P["SLOT_W"]
    hy = slot / 2 + 6.0                          # housing side wall outer face (12.5)
    hf = xm + 66.0                               # housing front outer face
    hb = xm - 80.0                               # housing rear outer face
    hz0, hz1 = 165.0, 330.0
    cp = chain_path(P)
    ra, rb = cp["ra"], cp["rb"]

    # ------------------------------------------------------------- frame (12)
    # bolt positions through the rails (x, z), shared by the parts they hold together
    b_drop_f = [(-12.0, rz), (12.0, rz)]
    b_drop_r = [(xp - 15.0, rz), (xp + 15.0, rz)]
    b_bplate = [(xm - 35.0, rz), (xm + 35.0, rz)]          # also hold the housing lugs (chain side)
    b_upr = [(xu_f, rz), (xu_r, rz)]
    b_mid = [(xmid - rs / 2 - 15.0, rz)]                   # middle clips to the rails
    b_marker = [(xf - 40.0, rz), (xf - 12.0, rz)]
    b_idler = P["IDLER_PIVOT"]
    rail_holes = union([hole_y(x, z, 6.5) for x, z in b_drop_f + b_drop_r + b_upr + b_mid]
                       + [hole_y(x, z, 6.5, -400, 0) for x, z in b_bplate + b_marker] + [hole_y(*b_idler, 8.5, -400, 0)]
                       + [hole_y(xm, zs - 24, 6.5, -400, 0)])
    rails = {}
    for side, y in (("l", -ry), ("r", ry)):
        rails[side] = sq_tube_x(y, rz, rs, rt, xr, xf) - rail_holes
    add("rail_l", "Side rail, chain side", rails["l"], 12, "made")
    add("rail_r", "Side rail, door side", rails["r"], 12, "made")

    # cross members between the rails: middle and rear 25 x 25, opener bar 40 x 20 (40 tall)
    # (DDR-003: the concept's front cross member ran through the drive wheel and its rear one passed 4 mm
    # over the press tyre; the opener cross member replaces the first, and the press axle, clamped through
    # its spacers between the rear drop plates, ties the rails at the rear in place of the second)
    cm_holes = union([hole_x(y, rz, 6.5) for y in (-35.0, -10.0, 10.0, 35.0)])
    add("cross_mid", "Middle cross member", sq_tube_y(xmid, rz, rs, rs, rt, -ri, ri) - cm_holes, 12, "made")
    obz = rz0 + 20.0
    bar_bolts_z = (obz - 10.0, obz + 10.0)
    ob_holes = union([hole_x(0, z, 6.5) for z in bar_bolts_z] + [hole_x(y, rz, 6.5) for y in (-35.0, 35.0)])
    add("opener_bar", "Opener cross member", sq_tube_y(xo, obz, 20.0, 40.0, rt, -ri, ri) - ob_holes, 12, "made")

    # corner clips: 25 x 25 x 3 angle, 25 long; one leg on the rail's inner face, one on the cross member
    def clip(face_x, toward, y_sign):
        """face_x: the cross member face; toward: -1 if the clip lies behind the face (rear side)."""
        a0, a1 = sorted((face_x, face_x + toward * 25.0))
        b0, b1 = sorted((face_x, face_x + toward * 3.0))
        leg_a = box(a0, a1, ri - 3.0, ri, rz0, rz1) if y_sign > 0 else box(a0, a1, -ri, -ri + 3.0, rz0, rz1)
        leg_b = box(b0, b1, ri - 25.0, ri, rz0, rz1) if y_sign > 0 else box(b0, b1, -ri, -ri + 25.0, rz0, rz1)
        return leg_a + leg_b
    clips = []
    for face_x, toward in ((ob0, -1), (xmid - rs / 2, -1)):
        for ys in (-1, 1):
            clips.append(clip(face_x, toward, ys))
    clip_holes = union([hole_y(x, z, 6.5) for x, z in b_upr + b_mid]) + \
        union([hole_x(y, rz, 6.5) for y in (-35.0, 35.0)])
    add("clips", "Corner clips (4)", union(clips) - clip_holes, 12, "made")

    # axle drop plates: front pair (drive axle, bearings inboard), rear pair (press axle, handle on the outside)
    def drop(x0, x1, z0, z1, side):
        y0, y1 = (ro, ro + dt) if side > 0 else (-ro - dt, -ro)
        return box(x0, x1, y0, y1, z0, z1)
    f_holes = union([hole_y(x, z, 6.5) for x, z in b_drop_f]) + hole_y(xw, zw, 20.0) + \
        union([hole_y(xw, zw + dz, 6.5) for dz in (-28.0, 28.0)])
    guard_pts = guard_spacer_points()
    f_holes = f_holes + hole_y(guard_pts[0][0], guard_pts[0][1], 4.2, -400, 0)
    add("drop_front", "Front drop plates (2)", union([drop(xw - 25, xw + 25, zw - 40, rz1, s) for s in (-1, 1)]) - f_holes, 12, "made")
    tabp = handle_tab_points()
    r_holes = union([hole_y(x, z, 6.5) for x, z in b_drop_r]) + hole_y(xp, zp, 16.5) + \
        union([hole_y(x, z, 8.5) for x, z in tabp["bolts"]])
    add("drop_rear", "Rear drop plates (2)", union([drop(xp - 25, xp + 25, zp - 20, rz1, s) for s in (-1, 1)]) - r_holes, 12, "made")

    # bearing plate on the outer face of the chain-side rail, for the plate shaft bearings
    bp_holes = union([hole_y(x, z, 6.5) for x, z in b_bplate]) + hole_y(xm, zs, 16.0) + \
        union([hole_y(xm, zs + dz, 6.5) for dz in (-24.0, 24.0)]) + \
        union([hole_y(xm + dx, zs, 6.5) for dx in (-24.0, 24.0)]) + \
        hole_y(guard_pts[1][0], guard_pts[1][1], 4.2)
    add("bplate", "Bearing plate", box(xm - 45, xm + 45, -ro - bt, -ro, rz0, zs + 45) - bp_holes, 12, "made")

    # hopper uprights: 20 x 3 flat bar on the outer faces of the rails, up to the hopper bosses
    hz_b = (P["HOPPER_Z0"] + 100.0, P["HOPPER_Z0"] + 150.0)    # boss bolt heights
    ups = []
    for xu in (xu_f, xu_r):
        for s in (-1, 1):
            y0, y1 = (ro, ro + ut) if s > 0 else (-ro - ut, -ro)
            u = box(xu - 10, xu + 10, y0, y1, rz0, P["HOPPER_Z0"] + 165.0)
            u = u - hole_y(xu, rz, 6.5) - union([hole_y(xu, z, 5.5) for z in hz_b])
            ups.append(u)
    add("uprights", "Hopper uprights (4)", union(ups), 12, "made")

    # frame fixings: heads and nuts
    fx = []
    for x, z in b_drop_f:
        for s in (-1, 1):
            fx.append(bolt_y(x, z, 6, s * do_, s * ri, tag=", front drop plate to rail"))
    for x, z in b_drop_r:
        for s in (-1, 1):
            if x < xp:      # passes the handle tab as well (F7)
                fx.append(bolt_y(x, z, 6, s * (do_ + 5.0), s * ri, tag=", handle tab and rear drop plate to rail"))
            else:
                fx.append(bolt_y(x, z, 6, s * do_, s * ri, tag=", rear drop plate to rail"))
    for x, z in b_mid:
        for s in (-1, 1):
            fx.append(bolt_y(x, z, 6, s * ro, s * (ri - 3.0), tag=", middle clip to rail"))
    for x, z in b_upr:
        for s in (-1, 1):
            fx.append(bolt_y(x, z, 6, s * (ro + ut), s * (ri - 3.0 if x == xu_f else ri), tag=", hopper upright to rail"))
    for y in (-35.0, 35.0):
        fx.append(bolt_x(y, rz, 6, ob0 - 3.0, ob1, tag=", clip to opener cross member"))
        fx.append(bolt_x(y, rz, 6, xmid - rs / 2 - 3.0, xmid + rs / 2, tag=", clip to middle cross member"))
    add("frame_bolts", "Frame bolts, M6", fix_compound(fx), 15, "fixing")

    # ------------------------------------------------------------- drive wheel (1)
    rim_r = zw - P["LUG_H"]
    ww = P["WHEEL_W"]
    wt = P["WHEEL_RIM_T"]
    # bought pressed-steel disc wheel: 2 mm rim and 2 mm web with six lightening holes (kit 1.9 D3 model, F5)
    wheel = ycyl(xw, 0, zw, rim_r, ww) - ycyl(xw, 0, zw, rim_r - wt, ww + 2)
    web_ = ycyl(xw, 0, zw, rim_r - wt + 0.5, 2.0) - ycyl(xw, 0, zw, 22.0, 4.0)
    for k in range(6):
        a = math.radians(30.0 + 60.0 * k)
        web_ = web_ - ycyl(xw + 80.0 * math.cos(a), 0, zw + 80.0 * math.sin(a), 25.0, 4.0)
    wheel = wheel + web_
    wheel = wheel + ycyl(xw, 0, zw, 22.0, ww) - ycyl(xw, 0, zw, P["AXLE_D"] / 2, ww + 2)  # hub, plain 16 mm bore
    # M6 cross bolt, hub to axle, 15 mm off the disc web toward the door side (kit 1.9 D3 model: at the web plane, as
    # first drawn, the bolt head and nut would sit in the web; SDL-DEC-001 item F2)
    y_cross = P["CROSS_BOLT_Y"]
    cross = xcyl2(y_cross, zw, 3.25, xw - 30, xw + 30)
    wheel = wheel - cross
    # the lug screws pass through the rim: 5.5 mm holes, two per lug
    lug_pts = []
    for k in range(P["N_LUGS"]):
        t = 360.0 * k / P["N_LUGS"]
        for y in (-12.5, 12.5):
            lug_pts.append((t, y))
    rim_holes = union([Pos(xw, 0, zw) * Rot(0, -t, 0) * (Pos(rim_r - 2.0, y, -1.5) * Rot(0, 90, 0) * Cylinder(2.75, 12)) for t, y in lug_pts])
    wheel = wheel - rim_holes
    add("wheel", "Drive wheel, steel, plain bore", wheel, 1, "bought")
    lugs = []
    for k in range(P["N_LUGS"]):
        t = 360.0 * k / P["N_LUGS"]
        foot = box(rim_r, rim_r + 3.0, -ww / 2, ww / 2, -7.5, 7.5)
        for y in (-12.5, 12.5):            # countersunk 5.5 mm holes, countersink on the outside of the foot
            foot = foot - Pos(rim_r + 3.0, y, -1.5) * Rot(0, 90, 0) * sp.csk_recess(5, 4.0)
        up = box(rim_r + 3.0, rim_r + P["LUG_H"], -ww / 2, ww / 2, 4.5, 7.5)
        lugs.append(Pos(xw, 0, zw) * Rot(0, -t, 0) * (foot + up))
    add("lugs", "Wheel lugs (18)", union(lugs), 1, "made")
    lf = []
    for t, y in lug_pts:                   # M5 x 12 countersunk screw, nut and washer inside the rim
        place = lambda sh, t=t: Pos(xw, 0, zw) * Rot(0, -t, 0) * sh  # noqa: E731
        lf.append(("M5x12 countersunk screw (ISO 10642), lug to rim", place(Pos(rim_r + 3.0, y, -1.5) * Rot(0, 90, 0) * sp.csk_screw(5, 12))))
        lf.append(("M5 washer (ISO 7089), lug screw", place(Pos(rim_r - wt, y, -1.5) * Rot(0, -90, 0) * cpl.washer(5))))
        lf.append(("M5 hex nut (ISO 4032), lug screw", place(Pos(rim_r - wt - 1.0, y, -1.5) * Rot(0, -90, 0) * cpl.hex_nut(5))))
    add("lug_screws", "Lug screws, M5 countersunk (36)", fix_compound(lf), 1, "fixing")
    ax_y0, ax_y1 = yc - 3.0, ri + 12.0 + 10.5
    add("axle", "Drive axle, 16 mm", ycyl2(xw, zw, P["AXLE_D"] / 2, ax_y0, ax_y1) - cross, 1, "made")
    add("cross_bolt", "Wheel hub cross bolt, M6", fix_compound(sp.bolt_set(6, (xw + 22.0, y_cross, zw), "-x", 44.0, ", wheel hub to axle")), 1, "fixing")
    brg = []
    for s in (-1, 1):
        flange = box(xw - 18, xw + 18, *sorted((s * ro, s * (ro - 3.0))), zw - 36, zw + 36)
        hous = ycyl2(xw, zw, 17.0, s * (ro - 3.0), s * (ro - 12.0))
        flange = flange - union([hole_y(xw, zw + dz, 6.5) for dz in (-28.0, 28.0)])
        brg.append(flange + hous - ycyl2(xw, zw, P["AXLE_D"] / 2, -200, 200))
    add("axle_bearings", "Drive axle flange bearings (2)", union(brg), 1, "bought")
    add("axle_bearing_bolts", "Axle bearing bolts, M6 (4)",
        fix_compound([bolt_y(xw, zw + dz, 6, s * do_, s * (ro - 3.0), tag=", axle bearing to drop plate") for s in (-1, 1) for dz in (-28.0, 28.0)]), 1, "fixing")
    add("axle_spacers", "Drive axle spacers (2)", union([ycyl2(xw, zw, 10.5, s * ww / 2, s * (ro - 12.0)) - ycyl2(xw, zw, P["AXLE_D"] / 2, -200, 200)
                                                        for s in (-1, 1)]), 1, "made")

    # ------------------------------------------------------------- chain drive (2)
    (ax, az), (bx, bz) = centers()
    pins, phase = chain_pins(P)
    spro, setscr = [], []
    for (x, z, t, bore), ph in zip(((ax, az, P["T_WHEEL"], P["AXLE_D"]), (bx, bz, P["T_PLATE"], P["SHAFT_D"])), phase):
        sk = sp.sprocket(t, bore=bore, width=4.3, hub_d=30.0, hub_len=10.5 - 2.15)
        sk = Pos(x, yc, z) * Rot(-90, 0, 0) * Rot(0, 0, -math.degrees(ph)) * sk
        y_ss = yc + 2.15 + (10.5 - 2.15) / 2            # set screw in the middle of the hub, on top
        sk = sk - zcyl2(x, y_ss, 3.0, z + bore / 2 - 0.5, z + 16.0)
        spro.append(sk)
        setscr.append(("M6x6 set screw (ISO 4026), sprocket hub", Pos(x, y_ss, z + bore / 2 + 6.0) * sp.set_screw(6, 6.0)))
    add("sprocket_wheel", "Wheel sprocket, 15 T", spro[0], 2, "bought")
    add("sprocket_plate", "Plate sprocket, 15 T", spro[1], 2, "bought")
    add("sprocket_screws", "Sprocket set screws, M6 (2)", fix_compound(setscr), 2, "fixing")
    add("chain", "Roller chain, #35, 76 links", fix_compound(sp.roller_chain(pins, yc)), 2, "bought")
    # the tensioner's arm swings to take up slack: draw its idler where its pitch circle meets the nearest chain pin,
    # with a tooth seat on that pin
    cx_, cz_ = cp["contact"]
    n_o = ((cx_ - cp["idler"][0]) / cp["r_idler"], (cz_ - cp["idler"][1]) / cp["r_idler"])
    pin_c = min(pins, key=lambda q: math.dist(q, (cx_, cz_)))
    ix, iz = pin_c[0] - cp["r_idler"] * n_o[0], pin_c[1] - cp["r_idler"] * n_o[1]
    ph_i = math.atan2(pin_c[1] - iz, pin_c[0] - ix)
    px, pz = b_idler
    ten = ycyl2(px, pz, 8.0, -ro, yc + 11.0)                                   # pivot boss and spring housing
    ten = ten + xz_prism(hull2d(circle_pts(px, pz, 7.0, 24) + circle_pts(ix, iz, 7.0, 24)), yc + 8.0, yc + 11.0)   # arm
    ten = ten - hole_y(px, pz, 6.8)                                            # boss tapped M8 for the pivot screw
    idl = Pos(ix, yc, iz) * Rot(-90, 0, 0) * Rot(0, 0, -math.degrees(ph_i)) * sp.sprocket(P["T_IDLER"], bore=8.0, width=4.3, hub_d=14.0, hub_len=8.0 - 2.15)
    ten = ten + idl
    add("tensioner", "Spring chain tensioner with 10 T idler", ten, 2, "bought")
    # M8 pivot screw from inside the frame through the rail into the tensioner's tapped boss (kit 1.9 D3 model: a
    # head or nut on the boss's outer end would sit in the chain's upper strand, SDL-DEC-001 item F3)
    add("tensioner_bolt", "Tensioner pivot screw, M8", fix_compound(sp.screw_set(8, (px, -ri, pz), "-y", 40, ", tensioner pivot, into tapped hole")), 2, "fixing")

    # ------------------------------------------------------------- chain guard (3): printed shroud on two spacers
    gin = guard_outline(0.0)
    gout = guard_outline(3.0)
    gy_in, gy_out = yc + 12.0, yc - 14.0
    band = xz_prism(gout, gy_out, gy_in) - xz_prism(gin, gy_out - 1, gy_in + 1)
    face = xz_prism(gin, gy_out, gy_out + 2.0)
    gh = union([ycyl2(x, z, 2.75, gy_out - 1, gy_out + 3) for x, z in guard_pts])       # 5.5 mm clearance holes
    add("guard", "Chain guard", band + face - gh, 3, "made")
    gsp, gsc = [], []
    for (x, z), y_face in zip(guard_pts, (-do_, -ro - bt)):
        gsp.append(ycyl2(x, z, 4.0, y_face, gy_out + 2.0) - ycyl2(x, z, 2.6, -400, 0))
        gsc.append(sp.screw_set(5, (x, gy_out, z), "+y", 45, ", chain guard, into tapped hole"))
    add("guard_spacers", "Guard spacer tubes (2)", union(gsp), 3, "made")
    add("guard_screws", "Guard screws, M5 x 45 (2)", fix_compound(gsc), 3, "fixing")

    # ------------------------------------------------------------- hopper (4)
    outer, inner = hopper_solids()
    bosses = union([box(x - 10, x + 10, s * 60.0 if s > 0 else -ro, ro if s > 0 else -60.0, z - 10, z + 10)
                    for x in (xu_f, xu_r) for s in (-1, 1) for z in hz_b])
    # 6.5 mm holes for M5 heat-set inserts (kit 1.9 D3 model; were drawn 4.0 mm, the tap drill size, SDL-DEC-001 F4)
    bh = union([hole_y(x, z, 6.5, 61.0, 80.0) + hole_y(x, z, 6.5, -80.0, -61.0) for x in (xu_f, xu_r) for z in hz_b])
    add("hopper", "Seed hopper", (outer - inner) + bosses - bh, 4, "made")
    z2 = P["HOPPER_Z0"] + 172.0
    lid = box(xm - 87, xm + 87, -62, 62, z2, z2 + 2.0) + (box(xm - 82, xm + 82, -57, 57, z2 - 6.0, z2) - box(xm - 80.5, xm + 80.5, -55.5, 55.5, z2 - 7, z2 + 1))
    add("lid", "Hopper lid", lid, 4, "made")
    hf_ = []
    for x in (xu_f, xu_r):
        for s in (-1, 1):
            for z in hz_b:
                hf_.append(("M5 heat-set insert (brass), hopper boss", Pos(x, s * ro, z) * sp.to_axis(sp.heat_set_insert(5, 8.0), "+y" if s > 0 else "-y")))
                hf_.append(sp.screw_set(5, (x, s * (ro + ut), z), "-y" if s > 0 else "+y", 10, ", hopper to upright"))
    add("hopper_screws", "Hopper screws, M5, and heat-set inserts (8)", fix_compound(hf_), 4, "fixing")

    # ------------------------------------------------------------- metering housing, shaft, bearings (5)
    housing = box(hb, hf, -hy, hy, hz0, hz1) - box(hb + 6, hf - 3, -slot / 2, slot / 2, hz0 + 6, hz1 - 6)
    housing = housing - box(xm - 30, xm + 30, -slot / 2, slot / 2, hz1 - 7, hz1 + 1)          # feed opening from the collar
    housing = housing - box(xm - 66, xm + 62, slot / 2 - 1, hy + 1, 179.0, 311.0)              # side door opening
    housing = housing - ycyl2(xm, zs, 11.0, -hy - 1, 0)                                        # plate hub runs here
    housing = housing - box(hb - 1, hb + 7, -slot / 2, slot / 2, zs + 35, zs + 45)            # brush slot in the rear wall
    housing = housing - union([ycyl2(xm + dx, zs, 1.7, -slot / 2 - 5.0, -slot / 2 + 0.5) for dx in (-48.0, 48.0)])   # liner peg holes
    housing = housing - zcyl2(xm + 32, 0, 7.0, hz0 - 1, hz0 + 7)                               # seed outlet
    spig_z0 = hz0 - 60.0
    housing = housing + (zcyl2(xm + 32, 0, 8.0, spig_z0, hz0) - zcyl2(xm + 32, 0, 6.0, spig_z0 - 1, hz0 + 1))
    collar = box(xm - 40, xm + 40, -24, 24, hz1, hz1 + 20) - box(xm - 34, xm + 34, -19, 19, hz1 + 10, hz1 + 21)
    collar = collar - loft([Pos(xm, 0, hz1 - 0.01) * Rectangle(60, slot), Pos(xm, 0, hz1 + 10.01) * Rectangle(60, 30)])
    lugs_h = union([box(xm + dx - 10, xm + dx + 10, -ri, -hy, rz0, rz1) for dx in (-35.0, 35.0)])
    lugs_h = lugs_h - union([hole_y(xm + dx, rz, 6.5) for dx in (-35.0, 35.0)])
    lugs_h = lugs_h - union([box(xm + dx - 6.3, xm + dx + 6.3, -36.0, -27.0, rz0 - 1.0, rz + 6.5) for dx in (-35.0, 35.0)])   # M6 nut slots
    # door screws: two M4 heat-set inserts in the door-side wall, where the wall is solid round the opening (kit 1.9 D3
    # model: as first drawn the screws stood over the opening; the door is now 146 x 150 to reach the wall, SDL-DEC-001 F1)
    dsx = [(xm + dx, z) for dx, z in P["DOOR_SCREWS"]]
    hpk = union([ycyl2(x, z, 2.6, hy - 5.7, hy + 0.5) for x, z in dsx])
    add("housing", "Metering housing", housing + collar + lugs_h - hpk, 5, "made")
    dx0, dx1, dz0, dz1 = P["DOOR"]
    door = box(xm + dx0, xm + dx1, hy, hy + 3.0, dz0, dz1) - ycyl2(xm, zs, 6.5, 0, 50) - \
        union([ycyl2(x, z, 2.25, 0, 50) for x, z in dsx])
    add("door", "Housing door, clear", door, 5, "made")
    ds = []
    for x, z in dsx:
        ds.append(("M4 heat-set insert (brass), housing door", Pos(x, hy, z) * sp.to_axis(sp.heat_set_insert(4, 5.7), "+y")))
        ds.append(("M4x8 thumb screw, housing door", Pos(x, hy + 3.0, z) * sp.to_axis(sp.thumb_screw(4, 8.0), "+y")))
    add("door_screws", "Door thumb screws, M4, and inserts (2)", fix_compound(ds), 5, "fixing")
    knob = ycyl2(xm, zs, 6.0, thk / 2, hy + 3.0) + ycyl2(xm, zs, 14.0, hy + 3.0, hy + 13.0)
    knob = cpl.break_edges(knob, 0.8)
    add("knob", "Plate knob", knob, 5, "made")
    add("knob_stud", "Plate knob stud, M6 x 25", fix_compound([("M6x25 hex screw (ISO 4017), knob stud, into tapped hole",
                                                               Pos(xm, hy + 9.0, zs) * sp.to_axis(cpl.hex_bolt(6, 25), "+y"))]), 5, "fixing")
    sh_y0 = yc - 3.0
    shaft = ycyl2(xm, zs, P["SHAFT_D"] / 2, sh_y0, thk / 2) - box(xm - 10, xm + 10, thk / 2 - 25.0, thk / 2 + 1, zs + 4.6, zs + 10)
    shaft = shaft - ycyl2(xm, zs, 2.5, thk / 2 - 15.0, thk / 2 + 1)                       # M6 tapped end for the knob
    add("shaft", "Plate shaft, 12 mm", shaft, 5, "made")
    yb_out0 = -ro - bt
    sbr = []
    # outboard bearing: flange bolts vertical; inboard bearing: flange bolts horizontal
    sbr.append(box(xm - 15, xm + 15, yb_out0 - 3.0, yb_out0, zs - 36, zs + 36) + ycyl2(xm, zs, 15.0, yb_out0 - 3.0, yb_out0 - 12.0))
    sbr.append(box(xm - 36, xm + 36, -ro, -ro + 3.0, zs - 15, zs + 15) + ycyl2(xm, zs, 15.0, -ro + 3.0, -ro + 12.0))
    sbr_holes = union([hole_y(xm, zs + dz, 6.5) for dz in (-24.0, 24.0)] + [hole_y(xm + dx, zs, 6.5) for dx in (-24.0, 24.0)])
    add("shaft_bearings", "Plate shaft flange bearings (2)", union(sbr) - ycyl2(xm, zs, P["SHAFT_D"] / 2, -300, 300) - sbr_holes, 5, "bought")
    col = ycyl2(xm, zs, 11.0, -P["HUB_Y"] - 8.0, -P["HUB_Y"]) - ycyl2(xm, zs, P["SHAFT_D"] / 2, -300, 300)
    col = col - zcyl2(xm, -P["HUB_Y"] - 4.0, 2.5, zs + 5.0, zs + 12.0)
    add("collar", "Shaft collar, 12 mm", col, 5, "bought")
    hb_ = []
    for dz in (-24.0, 24.0):
        hb_.append(bolt_y(xm, zs + dz, 6, yb_out0 - 3.0, -ro if dz > 0 else -ri))
    for dx in (-24.0, 24.0):
        hb_.append(bolt_y(xm + dx, zs, 6, -ro + 3.0, yb_out0))
    for dx in (-35.0, 35.0):        # bearing plate, rail and housing lug, nut in the lug's slot
        hb_.append(sp.bolt_set(6, (xm + dx, yb_out0, rz), "+y", -36.0 - yb_out0, ", bearing plate and housing lug to rail"))
    hb_.append([("M5x5 set screw (ISO 4026), shaft collar", Pos(xm, -P["HUB_Y"] - 4.0, zs + 11.0) * sp.set_screw(5, 5.0))])
    add("housing_bolts", "Bearing and housing bolts, M6", fix_compound(hb_), 5, "fixing")

    # ------------------------------------------------------------- seed plate (6)
    add("plate", "Seed plate (maize, 4 cells)", make_plate(at=(xm, zs)), 6, "made")
    liner_c, liner_d = make_liners(at=(xm, zs))
    if liner_c is not None:
        add("liner_chain", "Plate liner, chain side (printed)", liner_c, 5, "made")
    add("liner_door", "Plate liner, door side (printed)", liner_d, 5, "made")

    # ------------------------------------------------------------- brush (7): holder on the rear wall, strip through the slot
    r = P["PLATE_D"] / 2
    zb = zs + 40.0
    x_rim = xm - math.sqrt(r ** 2 - 36.0 ** 2)          # rim at the strip's lower edge
    holder = box(hb - 6.0, hb, -hy, hy, zs + 25, zs + 60)
    strip = box(hb, x_rim - 1.5, -slot / 2 + 0.5, slot / 2 - 0.5, zb - 4, zb + 4)
    bscr = [zs + 29.0, zs + 56.0]
    holder = holder - union([box(hb - 7.0, hb + 1.0, -2.25, 2.25, z - 3.0, z + 3.0) for z in bscr])   # slotted holes, 4.5 wide
    holder = cpl.break_edges(holder, 0.6)
    housing_sh = C["housing"].shape - union([xcyl2(0, z, 2.6, hb - 0.5, hb + 5.7) for z in bscr])
    C["housing"] = Comp(C["housing"].name, housing_sh, 5, "made")
    add("brush", "Singulator brush and holder", holder + strip, 7, "bought")
    bs = []
    for z in bscr:
        bs.append(("M4 heat-set insert (brass), brush holder", Pos(hb, 0, z) * sp.to_axis(sp.heat_set_insert(4, 5.7), "-x")))
        bs.append(("M4x10 pan head screw (ISO 7045), brush holder", Pos(hb - 6.0, 0, z) * sp.to_axis(sp.pan_screw(4, 10.0), "-x")))
    add("brush_screws", "Brush holder screws, M4, and inserts (2)", fix_compound(bs), 7, "fixing")

    # ------------------------------------------------------------- seed drop tube (8)
    d = P["DEPTH"]
    bl, bh_, btk = P["BOOT"]
    boot_top = -d + bh_
    xt = xm + 32.0
    tube_top = boot_top + 95.0
    add("drop_tube", "Seed drop tube", zcyl2(xt, 0, 10.0, boot_top, tube_top) - zcyl2(xt, 0, 8.0, boot_top - 1, tube_top + 1), 8, "bought")

    # ------------------------------------------------------------- opener (9)
    sx, sy, sl = P["SHANK"]
    sh_x0, sh_x1 = ob0 - sx, ob0
    shank = box(sh_x0, sh_x1, -sy / 2, sy / 2, -d, -d + sl)
    shank = shank - (Pos(sh_x1, 0, -d) * Rot(0, 45, 0) * Box(12, sy + 2, 12))            # chamfered nose
    for k in range(8):
        shank = shank - xcyl2(0, -d + 222.5 + 10 * k, 2.5, sh_x1 - 15, sh_x1 + 1)          # tapped M6, 15 deep
    boot_bolts = [(sh_x0 + 8.0, -d + 15.0), (sh_x0 + 8.0, -d + 40.0)]
    for x, z in boot_bolts:
        shank = shank - hole_y(x, z, 6.5)
    add("shank", "Opener shank", shank, 9, "made")
    bx0 = sh_x1 - 16.0 - bl + 0.0
    plates = []
    for s in (-1, 1):
        y0, y1 = (sy / 2, sy / 2 + btk) if s > 0 else (-sy / 2 - btk, -sy / 2)
        bp = box(bx0, sh_x1 - 4.0, y0, y1, -d, boot_top)
        bp = bp - union([hole_y(x, z, 6.5) for x, z in boot_bolts]) - hole_y(bx0 + 7.0, -d + 65.0, 6.5)
        plates.append(bp)
    add("boot", "Boot side plates (2)", union(plates), 9, "made")
    ob = [bolt_y(x, z, 6, -sy / 2 - btk, sy / 2 + btk, tag=", boot plates to shank") for x, z in boot_bolts]
    ob.append(bolt_y(bx0 + 7.0, -d + 65.0, 6, -sy / 2 - btk, sy / 2 + btk, tag=", boot plates and rear spacer"))
    add("boot_spacer", "Boot rear spacer", cpl.break_edges(ycyl2(bx0 + 7.0, -d + 65.0, 5.0, -sy / 2, sy / 2), 0.4) - hole_y(bx0 + 7.0, -d + 65.0, 6.5), 9, "made")
    ob += [bolt_x(0, z, 6, ob1, ob0, nut=False, length=30, tag=", opener cross member to shank, into tapped hole") for z in bar_bolts_z]
    add("opener_bolts", "Opener bolts, M6", fix_compound(ob), 9, "fixing")

    # ------------------------------------------------------------- covering chains (10)
    xb = xmid - rs / 2
    bracket = box(xb - 3.0, xb, -20, 20, rz0, rz1) + box(xb - 25.0, xb, -20, 20, rz0, rz0 + 3.0)
    bracket = bracket - union([hole_x(y, rz, 6.5) for y in (-10.0, 10.0)]) - union([zcyl2(xb - 15.0, y, 3.0, 0, 400) for y in (-14.0, 14.0)])
    add("chain_bracket", "Covering chain bracket", cpl.break_edges(bracket, 0.5), 10, "made")
    add("chain_bracket_bolts", "Chain bracket bolts, M6 (2)", fix_compound([bolt_x(y, rz, 6, xb - 3.0, xmid + rs / 2, tag=", covering chain bracket") for y in (-10.0, 10.0)]), 10, "fixing")
    cch = []
    for y in (-14.0, 14.0):
        ring_c = (xb - 21.5, y, rz0 + 1.5)          # top ring through the bracket hole and round its rear edge
        ring = Pos(*ring_c) * Rot(90, 0, 0) * sp.Torus(6.5, 1.75)
        cch.append(("Covering chain top ring", ring))
        for k, lk in enumerate(sp.link_chain((ring_c[0], y, ring_c[2] - 6.5 - 4.0), (xb - 70.0, y * 1.6, 4.0), wire=3.5, inner_len=14.0, inner_w=7.0)):
            cch.append(("Covering chain link", lk))
    add("cover_chains", "Covering chains (2)", fix_compound(cch), 10, "bought")

    # ------------------------------------------------------------- press wheel (11)
    # bought press wheel: pneumatic-class tyre (6 mm wall, 8 mm concave groove) on a split pressed-steel rim with a
    # hub (kit 1.9 D3 model, F5; the outside sizes are unchanged)
    pw_ = P["PRESS_W"]
    tyre = ycyl(xp, 0, zp, zp, pw_) - ycyl(xp, 0, zp, zp + 1, 20) + ycyl(xp, 0, zp, zp - 8, 22)
    tyre = tyre - ycyl(xp, 0, zp, zp - 30, pw_ + 2)
    tyre = tyre - (ycyl(xp, 0, zp, zp - 12.0, pw_ - 8) - ycyl(xp, 0, zp, zp - 26, pw_ - 6))
    rimw = ycyl(xp, 0, zp, zp - 30, 52.0) - ycyl(xp, 0, zp, zp - 32, 54.0)
    discs = []
    for s_ in (-1, 1):
        dsk = ycyl(xp, s_ * 8.0, zp, zp - 31.0, 1.5) - ycyl(xp, s_ * 8.0, zp, 14.0, 3.0)
        for k in range(6):
            a = math.radians(60.0 * k)
            dsk = dsk - ycyl(xp + 42.0 * math.cos(a), s_ * 8.0, zp + 42.0 * math.sin(a), 12.0, 3.0)
        discs.append(dsk)
    discs = union(discs)
    hubp = ycyl(xp, 0, zp, 14, pw_) - ycyl(xp, 0, zp, P["AXLE_D"] / 2, pw_ + 2)
    press = tyre + rimw + discs + hubp
    add("press", "Press wheel, 200 mm", press, 11, "bought")
    add("press_axle", "Press axle bolt, M16", fix_compound(sp.bolt_set(16, (xp, -do_, zp), "+y", 2 * do_, ", press wheel axle")), 11, "fixing")
    add("press_spacers", "Press axle spacers (2)", union([ycyl2(xp, zp, 10.5, s * P["PRESS_W"] / 2, s * ro) - ycyl2(xp, zp, P["AXLE_D"] / 2, -200, 200)
                                                          for s in (-1, 1)]), 11, "made")

    # ------------------------------------------------------------- handle (13)
    (hbx, hbz), (gx, gz) = handle_points()
    hod, ht = P["HANDLE_OD"], P["HANDLE_T"]
    yb = FY["handle_base"]
    gy = P["GRIP_Y"]
    tubes, sleeves, tabs, grip_pts, hfix, side_frames = [], [], [], [], [], []
    for s in (-1, 1):
        g = Vector(gx, s * gy, gz)
        a0 = Vector(hbx, s * yb, hbz)
        d0 = (g - a0).normalized()
        n0 = Vector(0, 1, 0).cross(d0).normalized()               # forward and up, square to the tube
        T = g + n0 * (2.5 + hod / 2)                                  # centre of the flattened top end
        d = (T - a0).normalized()
        n = Vector(0, 1, 0).cross(d).normalized()
        w = n.cross(d).normalized()
        a = tuple(a0)
        e = tuple(T - d * 20.0)
        f = lambda t, a=a, e=e: tuple(a[i] + t * (e[i] - a[i]) for i in range(3))  # noqa: E731
        # sleeve pins: one into the lower tube, one into the upper (pin holes every 50 mm set the grip height)
        pin_pts = [Vector(*f(0.46)), Vector(*f(0.60))]
        pin_holes = union([tube3(tuple(q - n * 20), tuple(q + n * 20), 3.1) for q in pin_pts])
        tubes.append(htube3(a, f(0.52), hod / 2, hod / 2 - ht) - pin_holes)
        tubes.append(htube3(f(0.53), e, hod / 2, hod / 2 - ht) - pin_holes)
        sleeves.append(htube3(f(0.40), f(0.66), 12.5, 11.3) - pin_holes)
        tabs.append(handle_tab(s))
        o = T - d * 20.0 - w * 17.0 - n * 2.5
        top = Solid.make_box(40.0, 34.0, 5.0, Plane(origin=tuple(o), x_dir=tuple(d), z_dir=tuple(n)))
        tabs.append(top - tube3(tuple(T - n * 10), tuple(T + n * 10), 3.25))
        grip_pts.append((T, n))
        hfix.append([sp.clevis_pin_vec(6, tuple(q + n * sp.curved_face_offset(12.5, 4.8)), tuple(-n), sp.curved_face_offset(12.5, 4.8) + 12.5,
                                       ", handle sleeve") for q in pin_pts])
        hfix.append(sp.bolt_set_vec(6, tuple(T + n * 2.5), tuple(-n), 16.0 + sp.curved_face_offset(hod / 2, 6.0), ", handle top to cross grip"))
        side_frames.append((a0, d, n))
    add("handle_lower", "Handle lower tubes (2)", union(tubes[0::2] + tabs[0::2]), 13, "made")
    add("handle_upper", "Handle upper tubes (2)", union(tubes[1::2] + tabs[1::2]), 13, "made")
    add("sleeves", "Handle sleeves (2)", union(sleeves), 13, "made")
    T0, n_ = grip_pts[0]
    gc = T0 - n_ * (2.5 + hod / 2)                                   # grip axis, behind the flattened ends
    grip = htube3((gc.X, -gy - 45, gc.Z), (gc.X, gy + 45, gc.Z), hod / 2, hod / 2 - ht)
    grip = grip - union([tube3(tuple(T - nn * 32), tuple(T + nn * 5), 3.25) for T, nn in grip_pts])   # bolt holes through the grip
    grip = grip + union([htube3((gc.X, s * (gy - 22), gc.Z), (gc.X, s * (gy - 132), gc.Z), hod / 2 + 4, hod / 2 + 0.01) for s in (-1, 1)])
    add("grip", "Cross grip with rubber grips", grip, 13, "made")
    # brace at 30 % up the lower tubes, across the front of the side tubes (flattened ends bolted through them)
    t3 = 0.3
    bxp, bzp = hbx + t3 * (gx - hbx), hbz + t3 * (gz - hbz)
    yb3 = yb + t3 * (gy - yb)
    brace_holes = []
    xb_ = bxp + (hod / 2) / math.sin(math.radians(P["HANDLE_ANGLE"])) + 10.5
    brace = htube3((xb_, -yb3 + 12.4, bzp), (xb_, yb3 - 12.4, bzp), 9.0, 7.5)
    # flattened ends lie on the front of the lower tubes, one M6 bolt each through the tube (kit 1.9 D3 model)
    for (a0, d, n), s in zip(side_frames, (-1, 1)):
        bpt = Vector(xb_, s * yb3, bzp)                     # brace axis where it meets this side
        c = a0 + d * (bpt - a0).dot(d)                      # nearest point on the lower tube's axis
        w = n.cross(d).normalized()
        wy = 1 if w.Y * s > 0 else -1
        tab = Solid.make_box(26.0, 32.0, 4.0, Plane(origin=tuple(c + n * 11.0 - d * 13.0 - w * (wy * 22.0 if wy > 0 else 10.0)),
                                                    x_dir=tuple(d), z_dir=tuple(n)))
        tab = tab - tube3(tuple(c + n * 20), tuple(c - n * 20), 3.25)
        brace = brace + tab
        hfix.append(sp.bolt_set_vec(6, tuple(c + n * 15.0), tuple(-n), 15.0 + sp.curved_face_offset(hod / 2, 6.0), ", handle brace"))
        brace_holes.append(tube3(tuple(c + n * 20), tuple(c - n * 20), 3.25))
    add("brace", "Handle brace", brace, 13, "made")
    C["handle_lower"] = Comp(C["handle_lower"].name, C["handle_lower"].shape - union(brace_holes), 13, "made")
    hb2 = [bolt_y(x, z, 8, s * (do_ + 5.0), s * ro, tag=", handle to rear drop plate") for x, z in tabp["bolts"] for s in (-1, 1)]
    add("handle_bolts", "Handle bolts, M8 and M6, and sleeve pins", fix_compound(hb2 + hfix), 13, "fixing")

    # ------------------------------------------------------------- row marker (14)
    if marker:
        mx0, mx1 = xf - 50.0, xf
        mp = box(mx0, mx1, -ro - 3.0, -ro, rz0 - 7.5, rz1 + 7.5) - union([hole_y(x, z, 6.5) for x, z in b_marker])
        xa = (mx0 + mx1) / 2
        lugs_m = union([box(xa + dx - 1.5, xa + dx + 1.5, -ro - 28.0, -ro - 3.0, rz0 - 7.5, rz1 + 7.5) for dx in (-23.5, 23.5)])
        lugs_m = lugs_m - xcyl2(-ro - 18.0, rz, 4.2, xa - 30, xa + 30)
        add("marker_mount", "Marker mount plate", cpl.break_edges(mp + lugs_m, 0.5), 14, "made")
        rm = P["MARKER_D"] / 2
        piv = (xa, -ro - 18.0, rz)
        end = (xa, -P["ROW_SPACING"] + 22.0, rm + 4.0)
        f = lambda t: tuple(piv[i] + t * (end[i] - piv[i]) for i in range(3))  # noqa: E731
        L_arm = math.dist(piv, end)
        tpin = f(0.52)                                         # telescoping lock pin, through both tubes
        lock = xcyl2(tpin[1], tpin[2], 3.1, xa - 20, xa + 20)
        # outer tube runs 12 mm past the pivot so the pin passes through solid tube; its end is cut square to clear the mount
        # aluminium tubes 20 x 1.5 and 16 x 1.5 (SDL-DEC-001 F6, mass: were steel 20 x 1.2 and 16 x 1.2)
        arm = htube3(f(-12.0 / L_arm), f(0.58), 10.0, 8.5) - box(xa - 20, xa + 20, -ro - 9.0, 0, -100, 1000)
        arm = arm + (htube3(f(0.45), end, 8.0, 6.5))
        arm = arm - xcyl2(-ro - 18.0, rz, 4.2, xa - 30.0, xa + 30.0) - lock
        add("marker_arm", "Marker arm, telescoping", arm, 14, "made")
        spc = union([xcyl2(-ro - 18.0, rz, 6.0, xa + sg * 10.0, xa + sg * 22.0) for sg in (-1, 1)]) - xcyl2(-ro - 18.0, rz, 4.2, xa - 30, xa + 30)
        add("marker_spacers", "Marker pivot spacers (2)", spc, 14, "made")
        mfx = sp.clevis_pin_vec(8, (xa + 25.0, -ro - 18.0, rz), (-1, 0, 0), 50.0, ", marker pivot")
        mfx += sp.clevis_pin_vec(6, (xa + sp.curved_face_offset(10.0, 4.8), tpin[1], tpin[2]), (-1, 0, 0), 2 * sp.curved_face_offset(10.0, 4.8) + 0.0, ", marker telescoping lock")
        disc = ycyl(xa, -P["ROW_SPACING"], rm, rm, P["MARKER_T"]) + (ycyl2(xa, rm, 14.0, -P["ROW_SPACING"] - 6.0, -P["ROW_SPACING"] + 22.0) - ycyl2(xa, rm, 8.0, -P["ROW_SPACING"] + 2.0, -P["ROW_SPACING"] + 23.0))
        add("marker_disc", "Marker disc and hub", disc, 14, "made")
        add("marker_bolts", "Marker bolts, M6 (2), and pins", fix_compound([bolt_y(x, z, 6, -ro - 3.0, -ri, tag=", marker mount to rail") for x, z in b_marker] + [mfx]), 14, "fixing")
    return C


def guard_spacer_points():
    """Where the two guard spacers meet the chain-side drop plate and the bearing plate (x, z)."""
    P = PARAMS
    (ax, az), (bx, bz) = centers()
    a1, a2 = math.radians(-60.0), math.radians(200.0)
    return [(ax + 34.0 * math.cos(a1), az + 34.0 * math.sin(a1)), (bx + 34.0 * math.cos(a2), bz + 34.0 * math.sin(a2))]


def handle_tab_points():
    """The flattened lower end of each side tube lies on the rear drop plate; returns the bolt points."""
    P = PARAMS
    (hbx, hbz), (gx, gz) = handle_points()
    L = math.hypot(gx - hbx, gz - hbz)
    ux, uz = (hbx - gx) / L, (hbz - gz) / L          # down the tube, forward
    return {"u": (ux, uz), "bolts": [(hbx + s * ux, hbz + s * uz) for s in (26.0, 50.0)]}


def handle_tab(side):
    """Flattened lower end of a side tube, 60 long, 34 wide, 5 thick, on the drop plate's outer face."""
    P = PARAMS
    (hbx, hbz), _ = handle_points()
    tp = handle_tab_points()
    ux, uz = tp["u"]
    do_ = frame_y()["drop_out"]
    ang = math.degrees(math.atan2(uz, ux))
    c = (hbx + 30.0 * ux, hbz + 30.0 * uz)
    y0, y1 = (do_, do_ + 5.0) if side > 0 else (-do_ - 5.0, -do_)
    tab = Pos(c[0], (y0 + y1) / 2, c[1]) * Rot(0, -ang, 0) * Box(60.0, 5.0, 34.0)
    holes = union([hole_y(x, z, 8.5) for x, z in tp["bolts"]])
    # the rear drop plate's front rail bolt lies under the tab, so it clamps the tab too (kit 1.9 D3 model, SDL-DEC-001 F7)
    holes = holes + hole_y(P["X_PRESS"] - 15.0, P["RAIL_Z"], 6.5)
    # the tube's end meets the tab's top edge (kit 1.9: the short flattening neck drawn before sat where the shared
    # rail bolt's head goes, F7)
    return tab - holes


def build_parts(p=None, marker=True, fixings=True):
    """Components grouped by bill-of-materials line 1 to 14 (fixings go with their line, or are left out with
    fixings=False, as on the general arrangement drawing)."""
    C = build_components(p, marker=marker)
    groups = {}
    for k, c in C.items():
        if c.bom == 15 or (not fixings and c.kind == "fixing"):
            continue
        groups.setdefault(c.bom, []).append(c.shape)
    # a compound per line, not a fused solid: fusing touching parts (lugs on the rim, say) can leave
    # faces that will not tessellate for the concept media
    return {b: (v[0] if len(v) == 1 else Compound(children=[copy.copy(x) for x in v])) for b, v in sorted(groups.items())}


def assembly(parts=None):
    parts = parts or build_parts()
    # copies, so the parts keep no parent and can still be exported on their own
    return Compound(children=[copy.copy(parts[k]) for k in sorted(parts)])


# ---------------------------------------------------------------------------
# Kit 1.9 interface (STANDARDS section 24): concept options, each modelled to D3
# ---------------------------------------------------------------------------
TITLE = "SeedLine"
OPTIONS = {"A": "Cell plate on a chain drive", "B": "Punch wheel with a hub meter"}
PRINCIPLES = {
    "A": "A lugged ground wheel turns a printed vertical cell plate through a #35 chain; a runner opener cuts a furrow, "
         "each cell drops one seed into it, and chains and a press wheel cover and firm the row.",
    "B": "A 480 mm wheel presses six punches into the seedbed as it rolls; a printed cell ring in the hub drops one seed "
         "down the tube of the punch about to enter the soil, and its jaw opens in the ground.",
}
CHOSEN = "A"
OPTION_VIEWS = {"A": {"el": 22, "az": -55, "ground_z": 0}, "B": {"el": 22, "az": -55, "ground_z": 0}}
# Parts that are meant to overlap: screws in tapped holes (drawn at the tap drill size) and in the knob, the chain-side
# liner's pegs pressed into the slot wall, the marker disc's hub on the arm end
ALLOWED_CONTACTS = [("into tapped hole", "Opener shank"), ("into tapped hole", "Front drop plate"), ("into tapped hole", "Bearing plate"),
                    ("into tapped hole", "Spring chain tensioner"), ("knob stud", "Plate knob"), ("knob stud", "Plate shaft"),
                    ("Plate liner, chain side", "Metering housing"), ("Marker disc", "Marker arm")]

# materials and colours by component key (cad_parts.MATERIALS has no PETG: printed PETG parts are drawn as HDPE, so
# their mass in cad/fidelity.json is about 25 % low; SDL-CAL-001 section 5 carries the PETG masses)
_MAT = {
    "rail_l": ("painted_steel", None), "rail_r": ("painted_steel", None), "cross_mid": ("painted_steel", None),
    "opener_bar": ("painted_steel", None), "clips": ("painted_steel", None), "drop_front": ("painted_steel", None),
    "drop_rear": ("painted_steel", None), "bplate": ("painted_steel", None), "uprights": ("painted_steel", None),
    "wheel": ("painted_steel", "#374151"), "lugs": ("painted_steel", "#B45309"), "axle": ("mild_steel", None),
    "axle_bearings": ("galvanised", None), "axle_spacers": ("mild_steel", None), "sprocket_wheel": ("mild_steel", None),
    "sprocket_plate": ("mild_steel", None), "chain": ("mild_steel", "#3F3F46"), "tensioner": ("zinc_plated", "#C2410C"),
    "guard": ("hdpe_natural", "#F59E0B"), "guard_spacers": ("zinc_plated", None), "hopper": ("hdpe_natural", "#E5E7EB"),
    "lid": ("hdpe_natural", "#94A3B8"), "housing": ("hdpe_natural", "#0F766E"), "door": ("polycarbonate", None),
    "knob": ("hdpe_black", None), "shaft": ("mild_steel", None), "shaft_bearings": ("galvanised", None),
    "collar": ("zinc_plated", None), "plate": ("hdpe_natural", "#14B8A6"), "liner_chain": ("hdpe_natural", "#C4B5FD"),
    "liner_door": ("hdpe_natural", "#C4B5FD"), "brush": ("hdpe_black", "#7C2D12"), "drop_tube": ("hdpe_black", "#0EA5E9"),
    "shank": ("painted_steel", "#4B5563"), "boot": ("painted_steel", "#6B7280"), "boot_spacer": ("mild_steel", None),
    "chain_bracket": ("painted_steel", None), "cover_chains": ("zinc_plated", None), "press": ("epdm", None),
    "press_spacers": ("mild_steel", None), "handle_lower": ("painted_steel", None), "handle_upper": ("painted_steel", None),
    "sleeves": ("painted_steel", None), "grip": ("painted_steel", None), "brace": ("painted_steel", None),
    "marker_mount": ("safety_yellow", None), "marker_arm": ("aluminium", "#E3B21C"), "marker_spacers": ("zinc_plated", None),
    "marker_disc": ("safety_yellow", None),
}
_EXPLODE = {1: (260, 0, 0), 2: (0, -260, -60), 3: (-150, -330, 330), 4: (0, 0, 330), 5: (0, 170, 90), 6: (0, -170, 240),
            7: (520, -250, 120), 8: (80, 0, -90), 9: (140, 0, -200), 10: (-280, 0, -200), 11: (-220, 0, -40), 12: (0, 0, 0),
            13: (350, 450, -150), 14: (0, -250, 0), 15: (0, 0, 0), 16: (0, 0, 0)}
_SINGLE = {"wheel", "chain", "cover_chains", "tensioner", "hopper", "housing", "guard", "plate", "press", "grip"}


def _solids(shape):
    try:
        ss = list(shape.solids())
    except Exception:
        ss = [shape]
    return ss or [shape]


def option_a(marker=True):
    """Option A, the current design (SDL-DDR-001 to 003), as cad_parts.part() dicts: every made or bought piece on
    its own with its BOM line, every fixing as its own ISO part (kind fastener)."""
    C = build_components(marker=marker)
    out = []
    for key, c in C.items():
        ex = _EXPLODE.get(c.bom, (0, 0, 0))
        if c.kind == "fixing":
            for leaf in sp.leaves(c.shape):
                nm = getattr(leaf, "label", "") or c.name
                mat = "brass" if "insert" in nm else ("stainless" if "Split pin" in nm else "zinc_plated")
                out.append(cpl.part(nm, leaf, mat, "fastener", bom=c.bom, explode=ex))
            continue
        mat, col = _MAT.get(key, ("painted_steel", None))
        if key == "press":                           # rubber tyre on a steel centre
            zp = PARAMS["PRESS_D"] / 2
            tyre_zone = ycyl(PARAMS["X_PRESS"], 0, zp, zp + 5, PARAMS["PRESS_W"] + 10) - ycyl(PARAMS["X_PRESS"], 0, zp, zp - 29.9, PARAMS["PRESS_W"] + 12)
            tyre = c.shape & tyre_zone
            centre = c.shape - tyre_zone
            out.append(cpl.part("Press wheel tyre, 200 mm concave", tyre, "epdm", "bought", bom=11, explode=ex))
            out.append(cpl.part("Press wheel centre, pressed steel", centre, "galvanised", "bought", bom=11, explode=ex))
            continue
        if key == "grip":                            # tube and two rubber grips
            ss = sorted(_solids(c.shape), key=lambda x: -x.volume)
            out.append(cpl.part("Cross grip, 22 x 1.2 tube", ss[0], "painted_steel", "made", bom=13, explode=ex))
            for i, g in enumerate(ss[1:], 1):
                out.append(cpl.part(f"Rubber grip {i}", g, "epdm", "bought", bom=13, explode=ex))
            continue
        if key == "chain":                           # one part per link (plates, roller, pin), so checks stay small
            links = {}
            for leaf in sp.leaves(c.shape):
                links.setdefault(leaf.label.split(":")[0], []).append(leaf)
            for nm, ls in links.items():
                out.append(cpl.part(f"Roller chain #35, {nm.lower()}", Compound(children=ls), mat, "bought", bom=2, color=col, explode=ex))
            continue
        kind = "bought" if c.kind == "bought" else "made"
        ss = [c.shape] if key in _SINGLE else _solids(c.shape)
        base = c.name.split(" (")[0]
        for i, sh in enumerate(ss, 1):
            nm = base if len(ss) == 1 else f"{base} {i}"
            out.append(cpl.part(nm, sh, mat, kind, bom=c.bom, color=col, explode=ex))
    return out


def components(option=None):
    option = option or CHOSEN
    if option == "A":
        return option_a()
    if option == "B":
        import punch_wheel
        return punch_wheel.option_b()
    raise ValueError(f"unknown option {option}")


# ---------------------------------------------------------------------------
# Constructability checks
# ---------------------------------------------------------------------------
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=None):
    """Pairs that must touch and pairs that must stay apart. Returns a list of
    (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def pieces(sh):
        """Leaf solids of a compound (a chain, a set of fixings), so each check stays small."""
        kids = sp.leaves(sh)
        return kids if len(kids) > 1 else [sh]

    def chk(desc, a, b_, expect):
        """expect: 'touch' (no overlap, gap 0) or a minimum clearance in mm."""
        a = S(a) if isinstance(a, str) else a
        b_ = S(b_) if isinstance(b_, str) else b_
        reach = (expect if isinstance(expect, float) else 1.0) + 5.0
        v, gp = 0.0, float("inf")
        for pa in pieces(a):
            ba = pa.bounding_box()
            for pb in pieces(b_):
                bb = pb.bounding_box()
                if (ba.min.X > bb.max.X + reach or bb.min.X > ba.max.X + reach or ba.min.Y > bb.max.Y + reach or
                        bb.min.Y > ba.max.Y + reach or ba.min.Z > bb.max.Z + reach or bb.min.Z > ba.max.Z + reach):
                    continue
                vv = _vol(pa, pb)
                v += vv if vv == vv else 0.0
                gp = min(gp, pa.distance_to(pb))
        if gp == float("inf"):
            gp = 1e3                              # nothing within reach: clear by more than the check needs
        if expect == "fit":                    # sliding or clamped fit: no overlap, gap 0.5 mm or less
            ok = v < 1e-2 and gp <= 0.5
        elif expect == "joined":                 # pinned or set into the other part: must meet, may overlap
            ok = gp < 0.05
        else:
            ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))
        import gc
        gc.collect()

    def grp(*ks):
        """Several components checked together, as a compound (fusing them is slow and memory-hungry)."""
        out = []
        for k in ks:
            out += pieces(S(k) if isinstance(k, str) else k)
        return Compound(children=out)

    rails = grp("rail_l", "rail_r")
    P_GAP = (p or PARAMS)["SLOT_GAP"]
    # frame
    chk("Middle cross member between the rails", "cross_mid", rails, "touch")
    chk("Opener cross member between the rails", "opener_bar", rails, "touch")
    chk("Corner clips on the rails", "clips", rails, "touch")
    chk("Corner clips on the cross members", "clips", grp("cross_mid", "opener_bar"), "touch")
    chk("Front drop plates on the rails", "drop_front", rails, "touch")
    chk("Rear drop plates on the rails", "drop_rear", rails, "touch")
    chk("Bearing plate on the chain-side rail", "bplate", "rail_l", "touch")
    chk("Hopper uprights on the rails", "uprights", rails, "touch")
    # drive wheel and axle
    chk("Drive wheel clear of the opener cross member (mud)", grp("wheel", "lugs"), "opener_bar", 15.0)
    chk("Drive wheel clear of the rails", grp("wheel", "lugs"), rails, 15.0)
    chk("Drive wheel clear of the front drop plates", grp("wheel", "lugs"), "drop_front", 10.0)
    chk("Lugs on the wheel rim", "lugs", "wheel", "touch")
    chk("Wheel hub on the axle", "wheel", "axle", "touch")
    chk("Axle bearings on the front drop plates", "axle_bearings", "drop_front", "touch")
    chk("Axle in its bearings", "axle", "axle_bearings", "touch")
    chk("Axle spacers between hub and bearings", "axle_spacers", grp("wheel", "axle_bearings"), "touch")
    chk("Axle clear of the drop plate holes", "axle", "drop_front", 1.0)
    # chain drive and guard
    chk("Wheel sprocket on the axle", "sprocket_wheel", "axle", "touch")
    chk("Plate sprocket on the shaft", "sprocket_plate", "shaft", "touch")
    chk("Wheel sprocket clear of the front drop plate", "sprocket_wheel", "drop_front", 3.0)
    chk("Plate sprocket clear of the outboard bearing", "sprocket_plate", "shaft_bearings", 2.0)
    chk("Tensioner pivot on the chain-side rail", "tensioner", "rail_l", "touch")
    chk("Tensioner clear of the chain-side drop plate and bearing plate", "tensioner", grp("drop_front", "bplate"), 3.0)
    chk("Chain clear of the drop plate, bearing plate and bearings", "chain", grp("drop_front", "bplate", "shaft_bearings", "axle_bearings"), 5.0)
    # running clearance from the chain's side plates to the guard (the TRL 3 model drew the chain as a 7 mm band; the
    # kit 1.9 model has the real #35 links, 12 mm across their pins, so the same guard gives 6.8 mm)
    chk("Chain clear of the guard", "chain", "guard", 5.0)
    chk("Sprockets clear of the guard", grp("sprocket_wheel", "sprocket_plate"), "guard", 5.0)
    chk("Tensioner clear of the guard", "tensioner", "guard", 3.0)
    chk("Guard spacers on the drop plate and bearing plate", "guard_spacers", grp("drop_front", "bplate"), "touch")
    chk("Guard spacers on the guard", "guard_spacers", "guard", "touch")
    chk("Guard spacers clear of the chain", "guard_spacers", "chain", 2.0)
    chk("Guard clear of the frame, bearings and uprights", "guard",
        grp("drop_front", "bplate", "shaft_bearings", rails, "uprights", "frame_bolts", "housing_bolts"), 2.0)
    chk("Guard clear of the drive wheel", "guard", grp("wheel", "lugs"), 10.0)
    # metering
    chk("Plate shaft in its bearings", "shaft", "shaft_bearings", "touch")
    chk("Shaft bearings on the bearing plate", "shaft_bearings", "bplate", "touch")
    chk("Inboard bearing clear of the rail top", "shaft_bearings", "rail_l", 1.0)
    chk("Housing lugs on the chain-side rail", "housing", "rail_l", "touch")
    chk("Housing clear of the shaft (shaft runs free)", "housing", "shaft", 0.5)
    chk("Housing clear of the plate (plate turns free)", "housing", "plate", 0.5)
    chk("Plate on the shaft collar", "plate", "collar", "touch")
    chk("Shaft collar on the shaft", "collar", "shaft", "touch")
    chk("Collar clear of the housing and bearings", "collar", grp("housing", "shaft_bearings"), 1.0)
    chk("Chain-side liner on the slot wall", "liner_chain", "housing", "joined")
    chk("Chain-side liner clear of the plate and its hub", "liner_chain", "plate", 1.0)
    chk("Chain-side liner clear of the brush", "liner_chain", "brush", 2.0)
    chk("Door-side liner clear of the plate", "liner_door", "plate", P_GAP - 1e-3)
    chk("Door-side liner pegs on the door", "liner_door", "door", "touch")
    chk("Door-side liner clear of the housing", "liner_door", "housing", 0.5)
    chk("Door-side liner clear of the brush and knob", "liner_door", grp("brush", "knob"), 2.0)
    chk("Door-side liner clear of the door screws", "liner_door", "door_screws", 10.0)
    # the 8 and 10 mm plates in the same slot (groundnut and sorghum class seed)
    xm_, zs_ = (p or PARAMS)["X_METER"], (p or PARAMS)["Z_SHAFT"]
    for label, seed in (("8 mm", (13.0, 9.0, 6.5)), ("10 mm", (16.0, 10.0, 8.1))):
        pl = make_plate(seed=seed, at=(xm_, zs_))
        lc, ld = make_liners(seed=seed, at=(xm_, zs_))
        if lc is not None:
            chk(f"{label} plate: chain-side liner clear of the plate", lc, pl, 1.0)
            chk(f"{label} plate: chain-side liner on the slot wall", lc, "housing", "joined")
        chk(f"{label} plate: door-side liner clear of the plate", ld, pl, P_GAP - 1e-3)
        chk(f"{label} plate: door-side liner pegs on the door", ld, "door", "touch")
        chk(f"{label} plate: housing clear of the plate", "housing", pl, 0.5)
        chk(f"{label} plate: hub end on the shaft collar", pl, "collar", "touch")
        chk(f"{label} plate: knob clear of the door-side liner", "knob", ld, 0.2)
    chk("Knob on the plate", "knob", "plate", "touch")
    chk("Knob clear of the housing", "knob", "housing", 0.2)
    chk("Door on the housing", "door", "housing", "touch")
    chk("Door screw inserts in the housing wall (kit 1.9, F1)", "door_screws", "housing", "touch")
    chk("Brush holder on the housing", "brush", "housing", "touch")
    chk("Brush clear of the plate rim", "brush", "plate", 1.0)
    chk("Hopper throat in the housing collar", "hopper", "housing", "touch")
    chk("Hopper on the uprights", "hopper", "uprights", "touch")
    chk("Lid on the hopper", "lid", "hopper", "touch")
    chk("Housing clear of the opener cross member", "housing", "opener_bar", 10.0)
    chk("Housing clear of the clips and uprights", "housing", grp("clips", "uprights"), 2.0)
    chk("Hopper clear of the bearing plate and guard", "hopper", grp("bplate", "guard"), 5.0)
    # opener and seed path
    chk("Shank on the opener cross member", "shank", "opener_bar", "touch")
    chk("Shank clear of the housing", "shank", "housing", 2.0)
    chk("Shank clear of the drive wheel", "shank", grp("wheel", "lugs"), 20.0)
    chk("Boot plates on the shank", "boot", "shank", "touch")
    chk("Drop tube on the housing spigot", "drop_tube", "housing", "touch")
    chk("Drop tube on the boot", "drop_tube", "boot", "touch")
    chk("Drop tube clear of the shank", "drop_tube", "shank", 5.0)
    chk("Opener bolt heads clear of the drive wheel", "opener_bolts", grp("wheel", "lugs"), 10.0)
    # covering and press
    chk("Chain bracket on the middle cross member", "chain_bracket", "cross_mid", "touch")
    chk("Covering chains clear of the press wheel", "cover_chains", "press", 10.0)
    chk("Covering chains clear of the housing and boot", "cover_chains", grp("housing", "boot", "drop_tube"), 20.0)
    chk("Press wheel on its spacers", "press", "press_spacers", "touch")
    chk("Press spacers on the rear drop plates", "press_spacers", "drop_rear", "touch")
    chk("Press wheel clear of the rails and clips", "press", grp(rails, "clips"), 10.0)
    chk("Press axle through the rear drop plates", "press_axle", "drop_rear", "touch")
    # handle
    chk("Handle tabs on the rear drop plates", "handle_lower", "drop_rear", "touch")
    chk("Handle clear of the rails", grp("handle_lower", "handle_upper"), rails, 2.0)
    chk("Sleeves on the handle tubes (sliding fit)", "sleeves", grp("handle_lower", "handle_upper"), "fit")
    chk("Grip on the upper tubes", "grip", "handle_upper", "touch")
    chk("Brace against the lower tubes", "brace", "handle_lower", "fit")
    chk("Handle clear of the press wheel", grp("handle_lower", "handle_upper"), "press", 20.0)
    # marker
    chk("Marker mount on the chain-side rail", "marker_mount", "rail_l", "touch")
    chk("Marker mount clear of the front drop plate and guard", "marker_mount", grp("drop_front", "guard"), 3.0)
    chk("Marker pivot spacers on the mount lugs", "marker_spacers", "marker_mount", "touch")
    chk("Marker arm between its pivot spacers", "marker_arm", "marker_spacers", 0.0)
    chk("Marker arm clear of the guard and drive", "marker_arm", grp("guard", "wheel", "lugs", "chain"), 10.0)
    chk("Marker disc on the arm", "marker_disc", "marker_arm", "joined")
    return rows


def print_checks(p=None):
    rows = checks(p)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = exp if isinstance(exp, str) else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:9.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    root = Path(__file__).resolve().parents[2]
    stl_dir = root / "cad/stl"
    stl_dir.mkdir(parents=True, exist_ok=True)
    parts = build_parts(fixings=False)
    asm = assembly(parts)
    exports = {"seedline-assembly": asm, "seedline-plate-maize": make_plate(), "seedline-hopper": parts[4], "seedline-housing": parts[5]}
    for name, shape in exports.items():
        # 0.15 mm chord and 0.3 rad: fine for printing and viewing (build123d's 0.001 mm default makes huge files)
        export_stl(shape, str(stl_dir / f"{name}.stl"), tolerance=0.15, angular_tolerance=0.3)
    bb = asm.bounding_box()
    print(f"assembly {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm (L x W x H, marker deployed)")
    cl, cd, th = cell_size()
    print(f"center distance {center_distance():.1f} mm; hopper {hopper_volume_l():.2f} L; "
          f"maize cell {cl:.1f} x {cd:.1f} mm, plate {th:.0f} mm thick")
    print("exported:", ", ".join(exports))
    print_checks()
