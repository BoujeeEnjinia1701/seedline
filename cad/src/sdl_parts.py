"""SeedLine repo-specific CAD helpers (kit 1.9). Built on .kit/cad_parts.py; nothing here belongs in .kit/.

Helpers the parts library does not have (suggested kit additions are listed in docs/REVIEW.md):
    to_axis(shape, d)                turn a part built along +Z so that +Z points along '+x', '-x', '+y', '-y', '+z', '-z'
    labelled(name, shape)            give a solid a label, so a compound of fixings can be split into named parts
    fix_compound(pieces)             a compound of labelled fixings (no fusing: fusing 50 bolts is slow and loses labels)
    bolt_set(d, xyz, shank, grip)    ISO 4017 bolt, two ISO 7089 washers and an ISO 4032 nut clamping a joint
    screw_set(d, xyz, shank, L)      ISO 4017 screw and washer into a tapped hole or a heat-set insert
    csk_screw(d, L), csk_recess()    ISO 10642 class countersunk screw and its countersunk hole
    pan_screw(d, L), thumb_screw()   ISO 7045 class pan head screw; knurled thumb screw
    heat_set_insert(d, L)            brass heat-set insert with a knurled outside
    set_screw(d, L)                  ISO 4026 class flat-point set screw (grub screw)
    sprocket(t, ...)                 roller chain sprocket with tooth seats and a hub
    roller_chain(points, ...)        roller chain links (rollers, inner and outer plates, pins) along a closed path
    link_chain(p0, p1, wire, ...)    light round-link chain between two points
    curved_face_offset(r, w)         where a washer or pin head seated on a round tube sits (tangent at the centre line)
All sizes in millimetres. Threads are drawn as plain shanks, as is usual in assembly CAD.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for _p in (str(HERE), str(HERE.parents[1] / ".kit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from build123d import (Axis, Circle, Compound, Cone, Cylinder, Polygon, Pos, RegularPolygon, Rot, Sketch,  # noqa: E402
                       Torus, extrude, chamfer)
import cad_parts as cp  # noqa: E402

ROT_TO = {"+z": (0, 0, 0), "-z": (180, 0, 0), "+x": (0, 90, 0), "-x": (0, -90, 0), "+y": (-90, 0, 0), "-y": (90, 0, 0)}
OPP = {"-z": "+z", "+z": "-z", "+x": "-x", "-x": "+x", "+y": "-y", "-y": "+y"}


def to_axis(shape, d):
    """Rotate a shape built along +Z so that its +Z points along d."""
    return Rot(*ROT_TO[d]) * shape


def labelled(name, shape):
    shape.label = name
    return shape


def fix_compound(pieces):
    """pieces: list of (name, shape) or lists of them. Returns a compound whose children carry the names."""
    flat = []

    def walk(x):
        if isinstance(x, (list, tuple)) and x and isinstance(x[0], str):
            flat.append(labelled(x[0], x[1]))
        elif isinstance(x, (list, tuple)):
            for y in x:
                walk(y)
    walk(pieces)
    return Compound(children=flat)


def leaves(shape):
    """Labelled leaf shapes of a compound made by fix_compound (or the shape itself)."""
    kids = list(getattr(shape, "children", []) or [])
    if not kids:
        return [shape]
    out = []
    for k in kids:
        out += leaves(k)
    return out


def bolt_set(d, xyz, shank, grip, tag=""):
    """Bolt, two washers and nut. xyz is the joint face on the head side, shank the direction the bolt points
    into the joint ('+y' and so on), grip the joint thickness. Returns [(name, shape), ...]."""
    up = OPP[shank]
    return [(f"{n}{tag}", Pos(*xyz) * to_axis(s, up)) for n, s in cp.hex_bolt_set(d, grip)]


def screw_set(d, xyz, shank, length, tag="", washer=True):
    """ISO 4017 screw of the given length with a washer under the head, into a tapped hole or an insert.
    xyz is the face the washer sits on."""
    h = cp.ISO[d][4] if washer else 0.0
    up = OPP[shank]
    out = [(f"M{d}x{length:g} hex screw (ISO 4017){tag}", Pos(*xyz) * to_axis(Pos(0, 0, h) * cp.hex_bolt(d, length), up))]
    if washer:
        out.append((f"M{d} washer (ISO 7089){tag}", Pos(*xyz) * to_axis(cp.washer(d), up)))
    return out


def csk_screw(d, length):
    """Countersunk screw (ISO 10642 class, 90 degree head of diameter 2d) along -Z: head top flush at z = 0,
    shank down to z = -length, hexagon socket in the head."""
    head = Pos(0, 0, -d / 4) * Cone(d / 2, d, d / 2)
    shank = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    sock = Pos(0, 0, -d * 0.15) * extrude(RegularPolygon(d * 0.29, 6), d * 0.3, both=True)
    return (head + shank) - sock


def csk_recess(d, depth):
    """The countersunk clearance hole for csk_screw, along -Z from z = 0 (cut it from the part)."""
    return Pos(0, 0, -d / 4 + 0.05) * Cone(d / 2 + 0.1, d + 0.1, d / 2 + 0.1) + Pos(0, 0, -depth / 2) * Cylinder(d / 2 + 0.25, depth + 0.2)


def pan_screw(d, length):
    """Pan head screw (ISO 7045 class) along -Z: head on top from z 0 to 0.7d, shank down to -length."""
    head = Pos(0, 0, 0.35 * d) * Cylinder(d, 0.7 * d)
    head = cp.break_edges(head, 0.25 * d)
    slot = Pos(0, 0, 0.6 * d) * Rot(0, 0, 0) * extrude(Sketch() + Polygon((-d, -0.12 * d), (d, -0.12 * d), (d, 0.12 * d), (-d, 0.12 * d)), 0.4 * d)
    return head - slot + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def thumb_screw(d, length, head_d=10.0, head_h=6.0):
    """Knurled thumb screw along -Z: head from z 0 to head_h with a ring of knurls, shank down to -length."""
    head = Pos(0, 0, head_h / 2) * Cylinder(head_d / 2, head_h)
    knurl = [Rot(0, 0, k * 360 / 16) * Pos(head_d / 2, 0, head_h / 2) * Cylinder(0.45, head_h + 1) for k in range(16)]
    for kn in knurl:
        head = head - kn
    return cp.break_edges(head, 0.4) + Pos(0, 0, -length / 2) * Cylinder(d / 2, length)


def heat_set_insert(d, length):
    """Brass heat-set insert along -Z from z = 0: knurled outside about 1.3d, threaded bore d."""
    od = 1.3 * d
    body = Pos(0, 0, -length / 2) * Cylinder(od / 2, length)
    for k in range(3):
        body = body - Pos(0, 0, -length * (k + 0.5) / 3) * (Cylinder(od / 2 + 1, 0.5) - Cylinder(od / 2 - 0.25, 0.5))
    return body - Pos(0, 0, -length / 2) * Cylinder(d / 2, length + 1)


def set_screw(d, length):
    """Flat-point set screw (ISO 4026 class) along -Z from z = 0, hexagon socket at the top."""
    body = Pos(0, 0, -length / 2) * Cylinder(d / 2, length)
    body = cp.break_edges(body, 0.12 * d)
    sock = Pos(0, 0, -d * 0.2) * extrude(RegularPolygon(d * 0.29, 6), d * 0.25, both=True)
    return body - sock


def curved_face_offset(r_tube, r_part=0.0):
    """Where a flat washer, nut or pin head sits on a round tube, measured from the tube axis: tangent to the
    tube at its centre line, so the full tube radius (its rim stands off the surface, as a real nut on a tube does)."""
    return r_tube


# ---------------------------------------------------------------------------------------------------------
# Chain drive
# ---------------------------------------------------------------------------------------------------------
PITCH_35, ROLLER_35, INNER_W_35, PLATE_T_35, PLATE_H_35 = 9.525, 5.08, 4.68, 1.27, 9.0


def sprocket(teeth, pitch=PITCH_35, roller=ROLLER_35, width=4.3, bore=12.0, hub_d=30.0, hub_len=8.0):
    """Roller chain sprocket in the XY plane, centred at the origin, tooth plate from z -width/2 to +width/2 and a
    hub from z +width/2 to +width/2 + hub_len. Tooth seats of radius 0.505 roller + 0.069 at the pitch points, flanks
    cut to a point, tips trimmed to the outside diameter p (0.6 + cot(180/t))."""
    pd = pitch / math.sin(math.pi / teeth)
    od = pitch * (0.6 + 1 / math.tan(math.pi / teeth))
    rs = 0.505 * roller + 0.069
    sk = Sketch() + Circle(od / 2)
    for k in range(teeth):
        a = 2 * math.pi * k / teeth
        cx, cy = pd / 2 * math.cos(a), pd / 2 * math.sin(a)
        sk -= Pos(cx, cy) * Circle(rs)
        # flank wedge: from the seat outward, opening toward the tips of the two neighbouring teeth
        ux, uy = math.cos(a), math.sin(a)
        vx, vy = -uy, ux
        w0, w1, L = rs * 0.98, pitch * 0.42, od / 2 - pd / 2 + 3.0
        pts = [(cx + vx * w0, cy + vy * w0), (cx + ux * L + vx * w1, cy + uy * L + vy * w1),
               (cx + ux * L - vx * w1, cy + uy * L - vy * w1), (cx - vx * w0, cy - vy * w0)]
        sk -= Polygon(*pts, align=None)
    sk -= Circle(bore / 2)
    plate = Pos(0, 0, -width / 2) * extrude(sk, width)
    hub = Pos(0, 0, width / 2 + hub_len / 2) * (Cylinder(hub_d / 2, hub_len) - Cylinder(bore / 2, hub_len + 1))
    try:
        hub = chamfer(hub.edges().filter_by(Axis.Z, reverse=True).sort_by(Axis.Z)[-2:], 0.6)
    except Exception:
        pass
    return plate + hub


def _stadium(a, b, r, t):
    """A link plate in the XZ plane from point a to point b (x, z), end radius r, thickness t along Y centred on 0."""
    ax, az = a
    bx, bz = b
    L = math.hypot(bx - ax, bz - az)
    ang = math.degrees(math.atan2(bz - az, bx - ax))
    sk = Sketch() + Pos(L / 2, 0) * (Polygon((-L / 2, -r * 0.82), (L / 2, -r * 0.82), (L / 2, r * 0.82), (-L / 2, r * 0.82)))
    sk += Circle(r)
    sk += Pos(L, 0) * Circle(r)
    s = Pos(0, 0, -t / 2) * extrude(sk, t)          # in XY, thickness along Z
    s = Rot(90, 0, 0) * s                             # into XZ (local y -> world z? use mapping below)
    # Rot(90,0,0): (x, y, z) -> (x, -z, y); the sketch's y becomes world z, thickness along -Y (centred, so fine)
    return Pos(ax, 0, az) * Rot(0, -ang, 0) * s


def roller_chain(pins, y0, pitch=PITCH_35):
    """Roller chain whose pin centres are the closed list 'pins' [(x, z), ...] in the plane y = y0. Link k runs from
    pin k to pin k + 1; even links are inner links, odd links outer links. Every pin carries a roller between the inner
    plates. Plates have pin holes, so nothing overlaps. Returns a list of (name, shape), each named "Chain link k: ..."."""
    n = len(pins)
    ri = INNER_W_35 / 2
    t = PLATE_T_35
    out = []
    for k in range(n):
        a, b = pins[k], pins[(k + 1) % n]
        inner = k % 2 == 0
        off = ri + t / 2 if inner else ri + t + t / 2 + 0.05
        for s in (-1, 1):
            pl = Pos(0, y0 + s * off, 0) * _stadium(a, b, PLATE_H_35 / 2 - 0.3, t)
            for (x, z) in (a, b):
                pl = pl - Pos(x, y0, z) * Rot(90, 0, 0) * Cylinder(1.6, 20)
            out.append((f"Chain link {k + 1}: {'inner' if inner else 'outer'} plate", pl))
        x, z = a
        out.append((f"Chain link {k + 1}: roller", Pos(x, y0, z) * Rot(90, 0, 0) * (Cylinder(ROLLER_35 / 2, INNER_W_35 - 0.1) - Cylinder(1.8, INNER_W_35))))
        out.append((f"Chain link {k + 1}: pin", Pos(x, y0, z) * Rot(90, 0, 0) * Cylinder(1.59, INNER_W_35 + 4 * t + 0.6)))
    return out


def path_points(segments, step=0.5):
    """Sample a closed path made of ('line', (x0, z0), (x1, z1)) and ('arc', (cx, cz), r, a0, a1) segments
    (angles in radians, a0 to a1 in the direction of travel). Returns a list of (x, z)."""
    pts = []
    for seg in segments:
        if seg[0] == "line":
            (x0, z0), (x1, z1) = seg[1], seg[2]
            L = math.hypot(x1 - x0, z1 - z0)
            m = max(2, int(L / step))
            pts += [(x0 + (x1 - x0) * i / m, z0 + (z1 - z0) * i / m) for i in range(m)]
        else:
            (cx, cz), r, a0, a1 = seg[1], seg[2], seg[3], seg[4]
            L = abs(a1 - a0) * r
            m = max(2, int(L / step))
            pts += [(cx + r * math.cos(a0 + (a1 - a0) * i / m), cz + r * math.sin(a0 + (a1 - a0) * i / m)) for i in range(m)]
    return pts


def pins_along(pts, n):
    """n points evenly spaced by arc length along the closed polyline pts."""
    cum = [0.0]
    for i in range(1, len(pts) + 1):
        a, b = pts[i - 1], pts[i % len(pts)]
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    total = cum[-1]
    out, j = [], 0
    for k in range(n):
        s = total * k / n
        while cum[j + 1] < s:
            j += 1
        a, b = pts[j], pts[(j + 1) % len(pts)]
        f = (s - cum[j]) / max(cum[j + 1] - cum[j], 1e-9)
        out.append((a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1])))
    return out, total


def link_chain(p0, p1, wire=3.5, inner_len=14.0, inner_w=7.0):
    """Light oval-link chain from p0 to p1 (x, y, z): links of 'wire' diameter, alternate links turned 90 degrees.
    Returns a list of solids."""
    from build123d import Box, Plane, Vector
    a, b = Vector(*p0), Vector(*p1)
    d = b - a
    L = d.length
    u = d.normalized()
    pitch = inner_len
    n = max(1, int(L / pitch))
    rw = wire / 2
    rm = (inner_w + wire) / 2
    straight = max(inner_len + wire - 2 * rm, 0.1)
    ref = Vector(0, 0, 1) if abs(u.Z) < 0.95 else Vector(1, 0, 0)
    side1 = u.cross(ref).normalized()
    side2 = u.cross(side1).normalized()
    big = 4 * (rm + rw)
    right = Pos(straight / 2, 0, 0) * (Torus(rm, rw) & Pos(big / 2, 0, 0) * Box(big, big, big))
    left = Pos(-straight / 2, 0, 0) * (Torus(rm, rw) & Pos(-big / 2, 0, 0) * Box(big, big, big))
    bars = [Pos(0, s * rm, 0) * Rot(0, 90, 0) * Cylinder(rw, straight) for s in (-1, 1)]
    link = right + left + bars[0] + bars[1]
    out = []
    for k in range(n):
        c = a + u * (pitch * (k + 0.5))
        sd = side1 if k % 2 == 0 else side2
        pl = Plane(origin=tuple(c), x_dir=tuple(u), z_dir=tuple(sd))
        out.append(pl.from_local_coords(link))
    return out


def _plane(origin, z_dir):
    from build123d import Plane, Vector
    z = Vector(*z_dir).normalized()
    ref = Vector(0, 1, 0) if abs(z.Y) < 0.9 else Vector(1, 0, 0)
    x = ref.cross(z).normalized()
    return Plane(origin=tuple(origin), x_dir=tuple(x), z_dir=tuple(z))


def bolt_set_vec(d, xyz, shank_dir, grip, tag=""):
    """As bolt_set, along any direction: xyz is the head-side joint face, shank_dir the way the bolt points."""
    pl = _plane(xyz, tuple(-c for c in shank_dir))
    return [(f"{n}{tag}", pl.from_local_coords(s)) for n, s in cp.hex_bolt_set(d, grip)]


def clevis_pin_vec(d, xyz, shank_dir, grip, tag=""):
    """ISO 2341 B clevis pin with an ISO 1234 split pin: head on the face at xyz, pin along shank_dir through a
    joint 'grip' thick, split pin square to it beyond the joint."""
    pl = _plane(xyz, tuple(-c for c in shank_dir))
    pin = cp.clevis_pin(d, grip)
    spl = Pos(0, 0, -grip - d) * cp.split_pin(d)
    return [(f"Clevis pin {d} mm (ISO 2341 B){tag}", pl.from_local_coords(pin)),
            (f"Split pin for {d} mm pin (ISO 1234){tag}", pl.from_local_coords(spl))]
