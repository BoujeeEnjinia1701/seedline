"""SeedLine product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: powder-coated bolted frame with rounded tube edges and
end caps, hex bolts and washers, a pressed steel disc drive wheel with its lugs (a spoked wheel is a labelled render option), a trolley-type press wheel with a
rubber tread, toothed sprockets and a roller chain behind a printed guard with a raised wordmark, a
filleted hopper without a window (decided 2026-10-02), a lid with hinge knuckles, a one-piece metering
housing with a 13 mm slot and a clear UV-stabilized side door that shows the printed maize plate (seeds in its
cells) and its two printed liners, a knurled plate knob, a strip brush, rubber handle grips, height-adjust collars and a starter
set of printed plates for other crops. A compact strip of tilled soil gives the ground context.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and the derived functions in model.py.
Axes as model.py: X is the direction of travel (+X forward), Y across the row (chain on the -Y side),
Z up, ground at Z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))

from build123d import (Axis, Box, Compound, Cylinder, Plane, Pos, Rectangle, RegularPolygon, Rot,
                       SlotOverall, Text, Torus, chamfer, extrude, fillet, loft)
from model import (PARAMS, build_parts, cell_size, centers, handle_points, hopper_solids, make_plate, make_liners,
                   sprocket_pd, tube3, ycyl, box)


def derived(P=PARAMS):
    """Derived quantities used here (model.py exposes them as functions)."""
    (ax, az), (bx, bz) = centers()
    clen, cdep, thk = cell_size()
    return {"wheel_c": (ax, az), "shaft_c": (bx, bz), "ra": sprocket_pd(P["T_WHEEL"]) / 2,
            "rb": sprocket_pd(P["T_PLATE"]) / 2, "cell": (clen, cdep, thk), "handle": handle_points()}


TITLE = "SeedLine: push seeder with 3D-printed seed plates"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation), on the chain side; "
             "drive wheel at right, hopper with its lid in the middle, handle rising to the left, "
             "on a strip of tilled soil"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): lid and hopper on top, "
             "printed maize plate, brush and housing below them, chain and guard toward the viewer, drive "
             "wheel at right, press wheel and handle at left, opener and covering chains below; the "
             "row-marker kit and three more crop plates at far right"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 20, "az": 60,
     "note": "Detail view of the metering unit on its own, from the left side of the seeder (opposite the "
             "chain) and ahead of it, about 20 deg elevation: printed maize plate with seeds in its cells "
             "and its two printed liners behind the clear housing door, knurled plate knob, strip brush and plate shaft"},
]

# Colours (restrained product palette; kit accent for the printed plate and collars)
C_FRAME = "#3A4048"      # powder-coated steel
C_DARK = "#23272D"       # caps, knob, holder
C_RUBBER = "#1E2227"
C_ACCENT = "#0F766E"
C_ZINC = "#B4BAC2"
C_STEEL = "#8F969E"
C_HOPPER = "#E4E7EA"     # PETG print, light
C_LID = "#F1F2F4"
C_HOUSING = "#CDD2D8"
C_BEZEL = "#9AA3AE"
C_GUARD = "#D2A13A"      # guard, muted safety amber
C_WINDOW = "#DCEBF5"
C_MAIZE = "#E2B34A"
C_TUBE = "#8E969F"
C_HUB = "#C9CED4"
C_SOIL = "#6E5240"
C_CLOD = "#5E4535"
C_TEXT = "#F3F4F6"

FONT = str(HERE.parents[2] / ".kit" / "fonts" / "IBMPlexSans-SemiBold.ttf")

# Other crops in the starter set of printed plates (BOM 6), seed sizes and cell counts from SDL-CAL-001
# (docs/04-calcs/01-sizing.md): label, cells, seed (L, W, T) mm, colour
SPARE_PLATES = [("BEAN 9", 9, (13.0, 8.0, 6.0), "#7C2D12"),
                ("SORGHUM 6", 6, (4.5, 4.0, 3.0), "#3F6212"),
                ("GROUNDNUT 6", 6, (15.0, 9.0, 8.0), "#334155")]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _rbox(x0, x1, y0, y1, z0, z1, r, axis):
    """Box with the edges parallel to `axis` rounded (fallback to smaller radii)."""
    b = box(x0, x1, y0, y1, z0, z1)
    return _fillet_try(b, b.edges().filter_by(axis), [r, r * 0.6, r * 0.3])


def _comp(shapes):
    shapes = [s for s in shapes if s is not None]
    return Compound(children=shapes)


def _hex_y(x, y0, z, side, af=10.0, h=4.0):
    """Hex bolt head and washer on a face at y0, standing out toward side (-1 or +1) along Y."""
    rot = Rot(90, 0, 0) if side < 0 else Rot(-90, 0, 0)
    washer = Pos(x, y0 + side * 0.6, z) * Rot(90, 0, 0) * Cylinder(af * 0.66, 1.2)
    head = Pos(x, y0 + side * 1.2, z) * rot * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)
    head = _fillet_try(head, head.faces().sort_by(Axis.Y)[0 if side < 0 else -1].edges(), [0.6, 0.3])
    return washer + head


def _hex_z(x, y, z0, af=10.0, h=4.0):
    """Hex bolt head and washer on an upward face at z0."""
    washer = Pos(x, y, z0 + 0.6) * Cylinder(af * 0.66, 1.2)
    head = Pos(x, y, z0 + 1.2) * extrude(RegularPolygon(af / math.sqrt(3), 6), amount=h)
    head = _fillet_try(head, head.faces().sort_by(Axis.Z)[-1].edges(), [0.6, 0.3])
    return washer + head


def _text_y(txt, size, x, y0, z, side, depth=0.6, angle=0.0, font=FONT):
    """Raised text on a face normal to Y at y0, standing out toward side, reading along +X (from -Y)
    or along -X (from +Y); angle tilts the baseline about Y."""
    t = extrude(Text(txt, font_size=size, font_path=font), amount=depth)
    if side < 0:
        return Pos(x, y0, z) * Rot(0, angle, 0) * Rot(90, 0, 0) * t
    return Pos(x, y0, z) * Rot(0, angle, 0) * Rot(0, 0, 180) * Rot(90, 0, 0) * t


def _kernel(seed=(12.0, 8.0, 5.0)):
    """One seed as a block rounded along its length (cheap to tessellate): length X, width Y, thickness Z."""
    L, W, T = seed
    k = Box(L, W, T)
    return _fillet_try(k, k.edges().filter_by(Axis.X), [min(T, W) * 0.45, min(T, W) * 0.3])


# ---------------------------------------------------------------------------
# Part builders
# ---------------------------------------------------------------------------
def _drive_wheel(P, D, spoked=False):
    """Steel disc wheel by default (decided 2026-10-02); spoked=True is the labelled render option."""
    xw, zw = D["wheel_c"]
    rim_r = zw - P["LUG_H"]
    W = P["WHEEL_W"]
    rim = ycyl(xw, 0, zw, rim_r, W) - ycyl(xw, 0, zw, rim_r - 12, W + 2)
    rim = _fillet_try(rim, rim.edges(), [2.0, 1.0])
    web = ycyl(xw, 0, zw, rim_r - 10, 5) - ycyl(xw, 0, zw, 21, 6)
    for k in range(6 if spoked else 0):   # lightening holes between six spokes (render option only)
        t = 2 * math.pi * (k + 0.5) / 6
        web -= ycyl(xw + 76 * math.cos(t), 0, zw + 76 * math.sin(t), 30, 8)
    web = _fillet_try(web, web.edges(), [1.5, 0.8])
    lug_proto = Box(P["LUG_H"] + 1, W, 12)
    lug_proto = _fillet_try(lug_proto, lug_proto.edges().filter_by(Axis.Y), [2.0, 1.0])
    lugs = []
    for k in range(P["N_LUGS"]):
        t = 2 * math.pi * k / P["N_LUGS"]
        rr = rim_r + P["LUG_H"] / 2 - 0.5
        lugs.append(Pos(xw + rr * math.cos(t), 0, zw + rr * math.sin(t)) * Rot(0, -math.degrees(t), 0) * lug_proto)
    wheel = _comp([rim, web] + lugs)
    hub = ycyl(xw, 0, zw, 22, W)
    hub = _fillet_try(hub, hub.edges(), [2.0, 1.0])
    yc, ry = P["Y_CHAIN"], P["RAIL_Y"]
    y0, y1 = yc - 8, ry + 25
    axle = Pos(xw, (y0 + y1) / 2, zw) * Rot(90, 0, 0) * Cylinder(P["AXLE_D"] / 2, y1 - y0)
    y_nut = ry + P["RAIL_S"] / 2 + 6          # outer face of the axle drop plate
    nuts = [Pos(xw, y_nut, zw) * Rot(-90, 0, 0) * extrude(RegularPolygon(13.9, 6), amount=10)]
    return wheel, _comp([hub, axle] + nuts)


def _sprocket(x, y, z, teeth, width=5.0):
    pr = sprocket_pd(teeth) / 2
    s = ycyl(x, y, z, pr + 4.2, width)
    for k in range(teeth):
        t = 2 * math.pi * k / teeth
        s -= ycyl(x + pr * math.cos(t), y, z + pr * math.sin(t), 3.3, width + 2)
    s += ycyl(x, y, z, 14, width + 12)
    return s


def _chain(P, D):
    """Roller chain: side plates and rollers along both strands and around both sprockets."""
    (ax, az), (bx, bz) = D["wheel_c"], D["shaft_c"]
    ra, rb, yc, p = D["ra"], D["rb"], P["Y_CHAIN"], P["PITCH"]
    dx, dz = bx - ax, bz - az
    L = math.hypot(dx, dz)
    beta = math.asin((ra - rb) / L)
    base = math.atan2(dz, dx)
    pts = []
    for s in (1, -1):
        ang = base + s * (math.pi / 2 - beta)
        nx, nz = math.cos(ang), math.sin(ang)
        a = (ax + ra * nx, az + ra * nz)
        b = (bx + rb * nx, bz + rb * nz)
        n = max(int(math.hypot(b[0] - a[0], b[1] - a[1]) / p), 1)
        for i in range(n + 1):
            f = i / n
            pts.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    # wraps: the half turns around each sprocket
    for (cx, cz, r, a0) in ((ax, az, ra, base + math.pi / 2), (bx, bz, rb, base - math.pi / 2)):
        n = max(int(math.pi * r / p), 1)
        for i in range(1, n):
            t = a0 + math.pi * i / n
            pts.append((cx + r * math.cos(t), cz + r * math.sin(t)))
    roller = Rot(90, 0, 0) * Cylinder(3.2, 5.6)
    plate = Box(p + 5, 1.0, 8.0)
    plate = _fillet_try(plate, plate.edges().filter_by(Axis.Y), [3.8, 2.5])
    pieces = []
    for (x, z) in pts:
        pieces.append(Pos(x, yc, z) * roller)
    # side plates along the straight strands
    for s in (1, -1):
        ang = base + s * (math.pi / 2 - beta)
        nx, nz = math.cos(ang), math.sin(ang)
        a = (ax + ra * nx, az + ra * nz)
        b = (bx + rb * nx, bz + rb * nz)
        seg = math.hypot(b[0] - a[0], b[1] - a[1])
        n = max(int(seg / p), 1)
        deg = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        for i in range(n):
            f = (i + 0.5) / n
            x, z = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            for sy in (-3.4, 3.4):
                pieces.append(Pos(x, yc + sy, z) * Rot(0, -deg, 0) * plate)
    return _comp(pieces)


def _idler(P, D):
    (ax, az), (bx, bz) = D["wheel_c"], D["shaft_c"]
    yc, ry, rz, rs = P["Y_CHAIN"], P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
    dx, dz = bx - ax, bz - az
    L = math.hypot(dx, dz)
    ux, uz = dx / L, dz / L
    mid = ((ax + bx) / 2, (az + bz) / 2)
    ix, iz = mid[0] + 20 * uz, mid[1] - 20 * ux
    wheel = _sprocket(ix, yc, iz - 12, 10, 4.0)
    arm = tube3((ix, yc, iz - 12), (ix, -ry - rs / 2, rz - rs / 2), 4)
    return wheel + arm


def _guard(P, D, m):
    g = m[3]
    g2 = _fillet_try(g, g.edges(), [1.2, 0.6])
    (ax, az), (bx, bz) = D["wheel_c"], D["shaft_c"]
    mx, mz = (ax + bx) / 2, (az + bz) / 2
    y_face = P["Y_CHAIN"] - 12.0
    ang = math.degrees(math.atan2(bz - az, ax - bx))    # baseline slope, reading toward the wheel
    word = _text_y("SeedLine", 26.0, mx, y_face, mz - 4, -1, 0.8, ang)
    ux, uz = (ax - bx), (az - bz)
    Lc = math.hypot(ux, uz)
    ux, uz = ux / Lc, uz / Lc
    bolts = [_hex_y(mx + f * ux, y_face, mz + f * uz + 26, -1, 8.0, 3.2) for f in (-100, 100)]
    return g2, word, _comp(bolts)


def _hopper(P):
    x = P["X_METER"]
    outer, inner = hopper_solids()
    body = outer - inner
    # round the upright corners of the upper box, outside and inside
    oe = [e for e in body.edges().filter_by(Axis.Z)
          if abs(abs(e.center().X - x) - 85) < 0.5 and abs(abs(e.center().Y) - 60) < 0.5]
    body = _fillet_try(body, oe, [9.0, 6.0, 3.0])
    ie = [e for e in body.edges().filter_by(Axis.Z)
          if abs(abs(e.center().X - x) - 82) < 0.5 and abs(abs(e.center().Y) - 57) < 0.5]
    body = _fillet_try(body, ie, [6.0, 4.0, 2.0])
    # rolled rim at the top
    lip = _rbox(x - 88, x + 88, -63, 63, 482, 490, 11.5, Axis.Z) - _rbox(x - 84, x + 84, -59, 59, 480, 492, 7.5, Axis.Z)
    lip = _fillet_try(lip, lip.faces().sort_by(Axis.Z)[0].edges(), [1.5, 0.8])
    body = body + lip
    lid = _rbox(x - 89, x + 89, -64, 64, 490, 496, 12, Axis.Z)
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Z)[-1].edges(), [3.0, 2.0, 1.0])
    lid = lid + (_rbox(x - 83.6, x + 83.6, -58.6, 58.6, 484, 490.5, 7, Axis.Z)
                 - _rbox(x - 80.6, x + 80.6, -55.6, 55.6, 483, 491, 5, Axis.Z))   # locating skirt
    tab = _rbox(x + 86, x + 100, -22, 22, 490, 494, 4, Axis.Z)
    knuckles = _comp([Pos(x - 92, y, 493) * Rot(90, 0, 0) * Cylinder(4.2, 24) for y in (-36, 36)])
    return body, lid, tab, knuckles


def _hopper_seed(P):
    x = P["X_METER"]
    _, inner = hopper_solids()
    fill = inner & box(x - 100, x + 100, -70, 70, 300, 444)
    k = _kernel(P["SEED"])
    rnd = random.Random(7)
    kernels = []
    for i in range(12):
        for j in range(8):
            kx = x - 74 + i * 13.4 + rnd.uniform(-3, 3)
            ky = -49 + j * 14.0 + rnd.uniform(-3, 3)
            kernels.append(Pos(kx, ky, 445.2 + rnd.uniform(-0.6, 0.6)) *
                           Rot(rnd.uniform(-12, 12), rnd.uniform(-12, 12), rnd.uniform(0, 180)) * k)
    return fill, _comp(kernels)


def _housing(P, D):
    xm, zs = P["X_METER"], P["Z_SHAFT"]
    slot = P["SLOT_W"]
    yo = slot / 2 + 6
    hx0, hx1, hz0, hz1 = xm - 80, xm + 66, 165.0, 330.0     # outer faces as model.py
    h = _rbox(hx0, hx1, -yo, yo, hz0, hz1, 10.0, Axis.Y)
    h = h - box(hx0 + 6, hx1 - 3, -slot / 2, slot / 2, hz0 + 6, hz1 + 1)
    h = h - box(xm + 20, xm + 44, -slot / 2, slot / 2, hz0 - 1, hz0 + 7)          # outlet to the drop tube
    h = h - box(xm - 66, xm + 62, slot / 2 - 1, yo + 1, 179.0, 311.0)             # side door opening (model.py)
    h = h - box(hx0 - 1, hx0 + 7, -slot / 2, slot / 2, zs + 35, zs + 45)          # brush slot in the rear wall
    # printed whole (decided 2026-10-02): no parting line
    door = _rbox(xm - 70, xm + 66, yo, yo + 3, 175.0, 315.0, 5, Axis.Y)
    door = _fillet_try(door, door.faces().sort_by(Axis.Y)[-1].edges(), [0.8, 0.4])
    screws = []
    for sx, zz in ((-58.0, 300.0), (54.0, 190.0)):
        hd = Pos(xm + sx, yo + 3 + 0.9, zz) * Rot(90, 0, 0) * Cylinder(3.6, 1.8)
        hd = _fillet_try(hd, hd.faces().sort_by(Axis.Y)[-1].edges(), [0.8, 0.4])
        hd -= Pos(xm + sx, yo + 3 + 1.8, zz) * Box(4.0, 1.4, 0.8)
        screws.append(hd)
    # knurled plate knob on the door boss (same place and size as model.py)
    yk = yo + 10
    knob = ycyl(xm, yk, zs, 14, 14)
    for k in range(20):
        t = 2 * math.pi * k / 20
        knob -= ycyl(xm + 14.6 * math.cos(t), yk, zs + 14.6 * math.sin(t), 1.7, 16)
    knob = _fillet_try(knob, knob.faces().sort_by(Axis.Y)[-1].edges(), [1.5, 0.8])
    cap = ycyl(xm, yk + 7.3, zs, 8, 0.8)
    return h, door, _comp(screws), knob, cap


def _bearings(P):
    xm, zs = P["X_METER"], P["Z_SHAFT"]
    ry, rz, rs = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
    out, bolts = [], []
    for s in (-1, 1):
        y = s * (ry + rs / 2 + 5)
        fl = _rbox(xm - 24, xm + 24, y - 3, y + 3, rz + rs / 2, zs + 22, 8, Axis.Y)
        cup = ycyl(xm, y, zs, 18, 10)
        fl = fl + _fillet_try(cup, cup.edges(), [2.0, 1.0])
        fl = fl + ycyl(xm, y + s * 7, zs, 11, 6)                 # locking collar
        out.append(fl)
        for bx in (-16, 16):
            bolts.append(_hex_y(xm + bx, y + s * 3, rz + rs / 2 + 9, s, 8.0, 3.2))
    return _comp(out), _comp(bolts)


def _plate_parts(P, D):
    xm, zs = P["X_METER"], P["Z_SHAFT"]
    clen, cdep, thk = D["cell"]
    plate = make_plate(at=(xm, zs))
    r = P["PLATE_D"] / 2
    circ = [e for e in plate.edges() if e.geom_type == "CIRCLE" and abs(e.radius - r) < 0.1]
    plate = _fillet_try(plate, circ, [1.0, 0.6])
    label = _text_y("MAIZE 4", 8.0, xm, thk / 2, zs - 30, 1, 0.6)
    L, W, T = P["SEED"]
    k = _kernel((W, T, L))    # width radial (X), thickness across (Y), length tangential (Z)
    seeds = []
    for i in range(1, P["N_CELLS"]):   # the cell at the outlet (0 deg, forward) has just dropped its seed
        t = 2 * math.pi * i / P["N_CELLS"]
        cx, cz = xm + (r - cdep / 2 - 0.3) * math.cos(t), zs + (r - cdep / 2 - 0.3) * math.sin(t)
        seeds.append(Pos(cx, 0, cz) * Rot(0, -math.degrees(t), 0) * k)
    return plate, label, _comp(seeds)


def _brush(P, D):
    """Brush on the housing's rear wall, strip through the rear slot (same place and size as model.py)."""
    xm, zs = P["X_METER"], P["Z_SHAFT"]
    slot = P["SLOT_W"]
    hy, hb = slot / 2 + 6, xm - 80
    r = P["PLATE_D"] / 2
    zb = zs + 40.0
    x_rim = xm - math.sqrt(r ** 2 - 36.0 ** 2)
    holder = _rbox(hb - 6.0, hb, -hy, hy, zs + 25, zs + 60, 2.0, Axis.X)
    bristles = box(hb, x_rim - 1.5, -slot / 2 + 0.5, slot / 2 - 0.5, zb - 4, zb + 4)
    for k in range(10):
        bristles -= box(hb + 1.0 + 4.1 * k, hb + 1.5 + 4.1 * k, -slot, slot, zb - 5, zb - 1)
    return holder, bristles


def _opener(P, m):
    xm, rz, rs, d = P["X_METER"], P["RAIL_Z"], P["RAIL_S"], P["DEPTH"]
    ry = P["RAIL_Y"]
    shank = box(xm + 45, xm + 65, -6, 6, -d + 40, rz + 60)
    shank = _fillet_try(shank, shank.edges().filter_by(Axis.Z), [2.0, 1.0])
    for k in range(6):
        shank = shank - Pos(xm + 55, 0, rz + 5 + 10 * k) * Rot(90, 0, 0) * Cylinder(3.5, 20)
    clamp = _rbox(xm + 38, xm + 72, -ry - rs / 2, ry + rs / 2, rz + rs / 2, rz + rs / 2 + 6, 3, Axis.Z) + \
        _rbox(xm + 38, xm + 72, -12, 12, rz + rs / 2 + 6, rz + 50, 3, Axis.Z)
    shoe = box(xm - 30, xm + 70, -9, 9, -d, -d + 45) + Pos(xm + 88, 0, -d + 18) * Rot(0, 35, 0) * Box(40, 18, 30)
    shoe = _fillet_try(shoe, shoe.edges().filter_by(Axis.Y), [3.0, 1.5])
    pin = Pos(xm + 55, 0, rz + 55) * Rot(90, 0, 0) * Cylinder(3.2, 40)
    pin += Pos(xm + 55, 20, rz + 55) * Rot(90, 0, 0) * Cylinder(6, 3)
    ring = Pos(xm + 55, -21, rz + 55 - 7) * Rot(90, 0, 0) * Torus(7.0, 1.2)
    bolts = [_hex_z(xm + 55, yy, rz + rs / 2 + 6, 13.0, 5.0) for yy in (-ry, ry)]
    return shank, clamp, shoe, _comp([pin, ring]), _comp(bolts)


def _cover_chains(P):
    xm, rz, rs = P["X_METER"], P["RAIL_Z"], P["RAIL_S"]
    bracket = _rbox(xm - 70, xm - 50, -30, 30, 55, rz - rs / 2, 3, Axis.Z)
    link = extrude(SlotOverall(13.0, 7.5) - SlotOverall(8.6, 3.1), amount=1.6, both=True)
    links = []
    for y in (-22, 22):
        a = (xm - 60, y, 60)
        b = (xm - 210, y * 1.6, 3)
        v = [b[i] - a[i] for i in range(3)]
        Lc = math.sqrt(sum(c * c for c in v))
        n = int(Lc / 7.0)
        yaw = math.degrees(math.atan2(v[1], v[0]))
        pitch = math.degrees(math.atan2(-v[2], math.hypot(v[0], v[1])))
        for i in range(n):
            f = (i + 0.5) / n
            p = Pos(a[0] + v[0] * f, a[1] + v[1] * f, a[2] + v[2] * f)
            # link long axis along the chain: squash the torus into an oval by two overlapping rings
            ori = Rot(0, 0, yaw) * Rot(0, pitch, 0) * (Rot(90, 0, 0) if i % 2 else Rot(0, 0, 0))
            links.append(p * ori * link)
    return bracket, _comp(links)


def _press_wheel(P):
    xp = P["X_PRESS"]
    zp = P["PRESS_D"] / 2
    W = P["PRESS_W"]
    ry = P["RAIL_Y"]
    tread = ycyl(xp, 0, zp, zp, W) - ycyl(xp, 0, zp, zp + 1, 20) + ycyl(xp, 0, zp, zp - 8, 22)
    tread = tread - ycyl(xp, 0, zp, zp - 30, W + 2)
    circ = [e for e in tread.edges() if e.geom_type == "CIRCLE" and abs(e.radius - zp) < 0.2]
    tread = _fillet_try(tread, circ, [6.0, 4.0, 2.0])
    rim = ycyl(xp, 0, zp, zp - 29.5, W - 20) - ycyl(xp, 0, zp, zp - 38, W - 16)
    web = ycyl(xp, 0, zp, zp - 36, 6) - ycyl(xp, 0, zp, 19, 8)
    for k in range(5):
        t = 2 * math.pi * k / 5
        web -= ycyl(xp + 42 * math.cos(t), 0, zp + 42 * math.sin(t), 12, 10)
    hub = ycyl(xp, 0, zp, 20, W)
    hub = _fillet_try(hub, hub.edges(), [2.0, 1.0])
    rimhub = rim + web + hub
    axle = ycyl(xp, 0, zp, P["AXLE_D"] / 2, 2 * ry + 50)
    y_nut = ry + P["RAIL_S"] / 2 + 6
    nuts = [Pos(xp, s * y_nut, zp) * (Rot(-90, 0, 0) if s > 0 else Rot(90, 0, 0)) * extrude(RegularPolygon(13.9, 6), amount=10)
            for s in (-1, 1)]
    return tread, rimhub, _comp([axle] + nuts)


def _frame(P):
    xw, xm, xp = P["X_WHEEL"], P["X_METER"], P["X_PRESS"]
    ry, rz, rs = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
    zw, zp = P["WHEEL_D"] / 2, P["PRESS_D"] / 2
    x_front, x_rear = xw + 60, xp - 40
    pieces = []
    for y in (-ry, ry):
        pieces.append(_rbox(x_rear, x_front, y - rs / 2, y + rs / 2, rz - rs / 2, rz + rs / 2, 2.5, Axis.X))
    xs_cross = (x_front - rs / 2, xm - 130, x_rear + rs / 2)
    for x in xs_cross:
        pieces.append(_rbox(x - rs / 2, x + rs / 2, -ry + rs / 2 - 0.5, ry - rs / 2 + 0.5, rz - rs / 2, rz + rs / 2, 2.5, Axis.Y))
    for (xa, za) in ((xw, zw), (xp, zp)):
        for y in (-ry - rs / 2 - 3, ry + rs / 2 + 3):
            pieces.append(_rbox(xa - 20, xa + 20, y - 3, y + 3, za - 20, rz + rs / 2, 8, Axis.Y))
    for sx in (-75, 75):
        for sy in (-ry + 5, ry - 5):
            pieces.append(_rbox(xm + sx - 10, xm + sx + 10, sy - 10, sy + 10, rz + rs / 2, 392, 2.0, Axis.Z))
    for x in xs_cross:
        for y in (-ry + rs / 2 + 1.5, ry - rs / 2 - 1.5):
            pieces.append(_rbox(x - 22, x + 22, y - 1.5, y + 1.5, rz - rs / 2, rz + rs / 2, 4, Axis.Y))
    # handle clevis plates at the rear of the rails
    (hbx, hbz), _ = handle_points()
    for y in (-ry - rs / 2 - 3, ry + rs / 2 + 3):
        pieces.append(_rbox(hbx - 26, hbx + 22, y - 3, y + 3, rz - 30, rz + 30, 8, Axis.Y))
    frame = _comp(pieces)
    caps = []
    for y in (-ry, ry):
        for (x0, x1) in ((x_front, x_front + 3), (x_rear - 3, x_rear)):
            c = _rbox(x0, x1, y - rs / 2 - 0.4, y + rs / 2 + 0.4, rz - rs / 2 - 0.4, rz + rs / 2 + 0.4, 3.0, Axis.X)
            caps.append(c)
    bolts = []
    for x in xs_cross[:2]:   # the rear cross member is clamped by the handle clevis bolt
        for s in (-1, 1):
            for dxb in (-12, 12):
                bolts.append(_hex_y(x + dxb, s * (ry + rs / 2), rz, s))
    for (xa, za) in ((xw, zw), (xp, zp)):
        for s in (-1, 1):
            bolts.append(_hex_y(xa, s * (ry + rs / 2 + 6), rz, s))
    for s in (-1, 1):
        bolts.append(_hex_y(hbx, s * (ry + rs / 2 + 6), rz + 14, s, 13.0, 5.0))
    return frame, _comp(caps), _comp(bolts)


def _handle(P):
    ry = P["RAIL_Y"]
    (hbx, hbz), (gx, gz) = handle_points()
    spread = 4.2
    rh = P["HANDLE_OD"] / 2
    tubes = [tube3((hbx, y, hbz), (gx, y * spread, gz), rh) for y in (-ry, ry)]
    tubes.append(tube3((gx - 10, -ry * spread - 45, gz), (gx - 10, ry * spread + 45, gz), rh))
    mx, mz = hbx + (gx - hbx) * 0.45, hbz + (gz - hbz) * 0.45
    my = ry * (1 + 0.45 * (spread - 1))
    brace = tube3((mx, -my, mz), (mx, my, mz), 9)
    frame = _comp(tubes + [brace])
    # telescoping sleeve collars with pin knobs (accent)
    collars = []
    f = 0.62
    for y in (-ry, ry):
        a = (hbx + (gx - hbx) * f, y * (1 + f * (spread - 1)), hbz + (gz - hbz) * f)
        d = (gx - hbx, y * (spread - 1), gz - hbz)
        Ld = math.sqrt(sum(c * c for c in d))
        u = [c / Ld for c in d]
        c = tube3((a[0] - u[0] * 25, a[1] - u[1] * 25, a[2] - u[2] * 25),
                  (a[0] + u[0] * 25, a[1] + u[1] * 25, a[2] + u[2] * 25), rh + 3.5)
        c = _fillet_try(c, c.edges(), [2.0, 1.0])
        s = 1 if y > 0 else -1
        knobp = tube3(a, (a[0], a[1] + s * (rh + 12), a[2]), 5.5)
        knobp = _fillet_try(knobp, knobp.edges(), [1.5, 0.8])
        collars.append(c + knobp)
    grips = []
    for s in (-1, 1):
        y0, y1 = s * 185, s * (ry * spread + 45)
        lo, hi = min(y0, y1), max(y0, y1)
        g = Pos(gx - 10, (lo + hi) / 2, gz) * Rot(90, 0, 0) * Cylinder(rh + 2.6, hi - lo)
        for k in range(int((hi - lo - 16) / 9)):
            yy = lo + 12 + 9 * k
            g -= Pos(gx - 10, yy, gz) * Rot(90, 0, 0) * (Cylinder(rh + 4, 2.0) - Cylinder(rh + 1.8, 2.2))
        end = Pos(gx - 10, y1 + s * 3, gz) * Rot(90, 0, 0) * Cylinder(rh + 3.2, 6)
        end = _fillet_try(end, end.faces().sort_by(Axis.Y)[0 if s < 0 else -1].edges(), [3.0, 2.0])
        grips.append(g + end)
    return frame, _comp(collars), _comp(grips)


def _marker(P):
    ry, rz, rs = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
    x_front = P["X_WHEEL"] + 60
    mxk = x_front - rs / 2
    clip = _rbox(mxk - 15, mxk + 15, -ry - 40, -ry - rs / 2, rz - 15, rz + 15, 4, Axis.Y)
    a = (mxk, -ry - 40, rz)
    b = (mxk, -P["ROW_SPACING"] + 30, P["MARKER_D"] / 2 + 5)
    arm_outer = tube3(a, (a[0], a[1] + (b[1] - a[1]) * 0.55, a[2] + (b[2] - a[2]) * 0.55), 10)
    arm_inner = tube3((a[0], a[1] + (b[1] - a[1]) * 0.5, a[2] + (b[2] - a[2]) * 0.5), b, 8)
    f = 0.55
    cpos = (a[0], a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f)
    d = (0, b[1] - a[1], b[2] - a[2])
    Ld = math.hypot(d[1], d[2])
    u = (0, d[1] / Ld, d[2] / Ld)
    collar = tube3((cpos[0], cpos[1] - u[1] * 18, cpos[2] - u[2] * 18),
                   (cpos[0], cpos[1] + u[1] * 6, cpos[2] + u[2] * 6), 13)
    collar = _fillet_try(collar, collar.edges(), [2.0, 1.0])
    collar += tube3(cpos, (cpos[0], cpos[1], cpos[2] + 22), 5)
    rm = P["MARKER_D"] / 2
    disc = ycyl(mxk, -P["ROW_SPACING"], rm, rm, 5)
    disc = _fillet_try(disc, disc.edges(), [1.5, 0.8])
    hub = ycyl(mxk, -P["ROW_SPACING"] + 12, rm, 14, 26)
    hub = _fillet_try(hub, hub.edges(), [2.0, 1.0])
    return _comp([clip, arm_outer, arm_inner]), collar, disc, hub


def _spare_plates(P):
    """Starter set of plates for other crops, standing in a row in front of the seeder."""
    plates, labels = [], []
    for i, (lab, n, seed, col) in enumerate(SPARE_PLATES):
        _, _, thk = cell_size(seed)
        x = 330 + 150 * i
        z = P["PLATE_D"] / 2
        pl = Pos(0, -300, 0) * make_plate(n_cells=n, seed=seed, at=(x, z))
        r = P["PLATE_D"] / 2
        circ = [e for e in pl.edges() if e.geom_type == "CIRCLE" and abs(e.radius - r) < 0.1]
        pl = _fillet_try(pl, circ, [1.0, 0.6])
        plates.append((lab, pl, col))
        labels.append(_text_y(lab, 7.0 if len(lab) > 7 else 8.0, x, -300 - thk / 2, z - 32, -1, 0.6))
    return plates, _comp(labels)


def _soil(P):
    """Compact strip of tilled soil with an open furrow at the opener and a few clods."""
    x0, x1, w, dep = -820.0, 260.0, 230.0, 80.0
    strip = loft([Pos(0, 0, -dep) * Pos((x0 + x1) / 2, 0, 0) * Rectangle(x1 - x0 + 60, 2 * w + 60),
                  Pos((x0 + x1) / 2, 0, 0) * Rectangle(x1 - x0, 2 * w)])
    xm, d = P["X_METER"], P["DEPTH"]
    strip = strip - box(xm - 150, xm + 120, -14, 14, -d - 2, 1)          # open furrow around the opener
    strip = strip - box(x0 - 10, P["X_PRESS"] + 60, -32, 32, -3, 1)  # press-wheel firmed track
    rnd = random.Random(11)
    clods = []
    for _ in range(34):
        x = rnd.uniform(x0 + 40, x1 - 40)
        y = rnd.choice((-1, 1)) * rnd.uniform(80, w - 22)
        s = rnd.uniform(14, 34)
        c = Box(s, s * rnd.uniform(0.6, 0.9), s * rnd.uniform(0.4, 0.6))
        try:
            c = chamfer(c.edges(), s * 0.14)
        except Exception:
            pass
        clods.append(Pos(x, y, s * 0.1) * Rot(rnd.uniform(-15, 15), rnd.uniform(-15, 15), rnd.uniform(0, 180)) * c)
    return strip, _comp(clods)


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------
def product_parts(P=PARAMS, wheel_style="disc"):
    """wheel_style: "disc" (decided default) or "spoked" (labelled render option)."""
    D = derived(P)
    m = build_parts()
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # 1 Drive wheel
    wheel, hub = _drive_wheel(P, D, spoked=(wheel_style == "spoked"))
    add("Drive wheel rim, disc and lugs" if wheel_style != "spoked" else "Drive wheel rim, spokes and lugs (render option)", wheel, C_FRAME, "painted", 1, "shell", (300, 0, 0))
    add("Drive wheel hub, axle and nut", hub, C_ZINC, "metal", 1, "shell", (300, 0, 0))

    # 2 Chain drive (behind the guard)
    (ax, az), (bx, bz) = D["wheel_c"], D["shaft_c"]
    yc = P["Y_CHAIN"]
    spr = _sprocket(ax, yc, az, P["T_WHEEL"]) + _sprocket(bx, yc, bz, P["T_PLATE"])
    add("Sprockets, 15 T", spr, C_STEEL, "metal", 2, "shell", (0, -150, -30))
    add("Roller chain, #35", _chain(P, D), "#4B5058", "metal", 2, "shell", (0, -150, -30))
    add("Spring idler", _idler(P, D), C_STEEL, "metal", 2, "shell", (0, -150, -30))

    # 3 Chain guard
    guard, word, gbolts = _guard(P, D, m)
    add("Chain guard (printed PETG)", guard, C_GUARD, "plastic", 3, "shell", (0, -300, -170))
    add("Chain guard wordmark", word, C_DARK, "plastic", 3, "shell", (0, -300, -170))
    add("Chain guard bolts", gbolts, C_ZINC, "metal", 15, "shell", (0, -300, -170))

    # 4 Hopper (no window), lid
    body, lid, tab, knuckles = _hopper(P)
    add("Seed hopper", body, C_HOPPER, "plastic", 4, "shell", (0, 0, 330))
    add("Hopper lid", lid, C_LID, "plastic", 4, "shell", (0, 0, 470))
    add("Hopper lid tab", tab, C_ACCENT, "plastic", 4, "shell", (0, 0, 470))
    add("Hopper lid hinge knuckles", knuckles, C_BEZEL, "plastic", 4, "shell", (0, 0, 470))

    # 5 Metering housing, door, knob, shaft and bearings
    h, door, screws, knob, cap = _housing(P, D)
    add("Metering housing (printed, one piece)", h, C_HOUSING, "plastic", 5, "internal", (0, 190, 60))
    add("Housing side door, clear", door, C_WINDOW, "clear", 5, "internal", (0, 280, 60))
    add("Door screws", screws, C_ZINC, "metal", 15, "internal", (0, 280, 60))
    add("Plate knob, knurled", knob, C_DARK, "plastic", 5, "internal", (0, 340, 60))
    add("Plate knob cap", cap, C_ACCENT, "plastic", 5, "internal", (0, 340, 60))
    xm, zs, ry = P["X_METER"], P["Z_SHAFT"], P["RAIL_Y"]
    shaft = Pos(xm, (yc - 6 + ry + 20) / 2, zs) * Rot(90, 0, 0) * Cylinder(P["SHAFT_D"] / 2, ry + 26 - yc)
    add("Plate shaft, 12 mm D-flat", shaft, C_ZINC, "metal", 5, "internal", (0, -60, 170))
    brg, bbolts = _bearings(P)
    add("Flange bearings, pressed steel", brg, C_ZINC, "metal", 5, "shell", (0, 0, 90))
    add("Bearing bolts", bbolts, C_STEEL, "metal", 15, "shell", (0, 0, 90))

    # 6 Printed seed plate (maize, 4 cells) with seed in three cells
    plate, plabel, pseeds = _plate_parts(P, D)
    add("Printed seed plate, maize 4 cell", plate, C_ACCENT, "plastic", 6, "internal", (0, -40, 170))
    add("Seed plate crop label", plabel, C_TEXT, "plastic", 6, "internal", (0, -40, 170))
    add("Maize seed in the plate cells", pseeds, C_MAIZE, "plastic", None, "internal", (0, -40, 170))

    liner_c, liner_d = make_liners(at=(xm, zs))
    add("Plate liner, chain side (printed)", liner_c, C_HOUSING, "plastic", 5, "internal", (0, -20, 170))
    add("Plate liner, door side (printed, clear render option)", liner_d, C_WINDOW, "clear", 5, "internal", (0, 120, 170))

    # 7 Singulator brush
    holder, bristles = _brush(P, D)
    add("Brush holder", holder, C_DARK, "plastic", 7, "internal", (0, 0, 250))
    add("Singulator brush bristles", bristles, "#2A2D33", "fabric", 7, "internal", (0, 0, 250))

    # 8 Drop tube
    add("Seed drop tube, PVC", m[8], C_TUBE, "plastic", 8, "shell", (60, 0, -120))

    # 9 Opener
    shank, clamp, shoe, pin, obolts = _opener(P, m)
    add("Opener shank, zinc plated", shank, C_ZINC, "metal", 9, "shell", (90, 0, -250))
    add("Opener clamp bracket", clamp, C_FRAME, "painted", 9, "shell", (90, 0, -170))
    add("Runner shoe and boot", shoe, C_FRAME, "painted", 9, "shell", (90, 0, -250))
    add("Depth pin and ring", pin, C_ZINC, "metal", 9, "shell", (90, 0, -250))
    add("Opener clamp bolts", obolts, C_ZINC, "metal", 15, "shell", (90, 0, -170))

    # 10 Covering chains
    cbr, clinks = _cover_chains(P)
    add("Covering chain bracket", cbr, C_FRAME, "painted", 10, "shell", (-260, 0, -120))
    add("Covering chains", clinks, "#6B7280", "metal", 10, "shell", (-260, 0, -120))

    # 11 Press wheel
    tread, rimhub, paxle = _press_wheel(P)
    add("Press wheel tread, rubber", tread, C_RUBBER, "rubber", 11, "shell", (-300, 0, 0))
    add("Press wheel rim and hub", rimhub, C_HUB, "plastic", 11, "shell", (-300, 0, 0))
    add("Press wheel axle and nuts", paxle, C_ZINC, "metal", 11, "shell", (-300, 0, 0))

    # 12 Frame
    frame, caps, fbolts = _frame(P)
    add("Frame, bolted square tube (powder coat)", frame, C_FRAME, "painted", 12, "shell", (0, 0, 0))
    add("Tube end caps", caps, C_DARK, "plastic", 12, "shell", (0, 0, 0))
    add("Frame bolts and washers", fbolts, C_ZINC, "metal", 15, "shell", (0, 0, 0))

    # 13 Handle
    htubes, collars, grips = _handle(P)
    add("Handle tubes and brace (powder coat)", htubes, C_FRAME, "painted", 13, "shell", (-120, 0, 90))
    add("Height-adjust collars and pins", collars, C_ACCENT, "plastic", 13, "shell", (-120, 0, 90))
    add("Handle grips, rubber", grips, C_RUBBER, "rubber", 13, "shell", (-120, 0, 90))

    # 14 Row-marker kit (accessory, shown deployed at the set row spacing)
    arm, mcollar, mdisc, mhub = _marker(P)
    add("Row marker arm and clip", arm, C_FRAME, "painted", 14, "accessory", (470, 0, 0))
    add("Row marker collar and pin", mcollar, C_ACCENT, "plastic", 14, "accessory", (470, 0, 0))
    add("Row marker disc", mdisc, C_STEEL, "metal", 14, "accessory", (470, 0, 0))
    add("Row marker hub", mhub, C_DARK, "plastic", 14, "accessory", (470, 0, 0))

    # 6 Starter set of plates for other crops (accessory)
    plates, labels = _spare_plates(P)
    for lab, pl, col in plates:
        add(f"Printed seed plate, {lab.split()[0].lower()}", pl, col, "plastic", 6, "accessory", (330, 330, 0))
    add("Spare plate crop labels", labels, C_TEXT, "plastic", 6, "accessory", (330, 330, 0))

    # Context: compact strip of tilled soil
    strip, clods = _soil(P)
    add("Tilled soil strip", strip, C_SOIL, "rubber", None, "context", (0, 0, 0))
    add("Soil clods", clods, C_CLOD, "rubber", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.1f} cm3")
