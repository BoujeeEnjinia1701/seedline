"""SeedLine concept option B: punch wheel with a hub meter (kit 1.9, detail level D3).

Option B is an alternative concept, modelled to the same detail level as the chosen design (Amish, 2026-10-24:
"Detail every option"). It is not carried to the drawing, the priced BOM or the build plan.

Working principle: a 480 mm wheel rolls on the seedbed on a narrow steel rim; six punches on the rim, 251 mm apart
round it, are pressed into the soil by the wheel's weight as it rolls, so there is no furrow to open or cover.
Seed is metered inside the hub: a printed cell ring turning with the wheel carries one seed per cell from the pool
in a stationary seed chamber on the fixed axle, past a brush, over the top on a stationary shoe to a release window
low on the front; there the seed drops through into the radial tube of the punch about to enter the soil, slides to
the punch's closed jaws and is left in the hole when the soil pushes the trailing jaw open at the bottom of the turn.
A torsion spring closes the jaw as the punch lifts out.

Axes as option A: X forward, Y across (-Y is the left, bearing side), Z up, ground at z = 0. The wheel rolls on its
rim, so the axle is at the rim radius; one punch is drawn straight down, in the soil. Angles (theta) are measured in
the XZ plane from forward (+X), positive upward; rolling forward, theta of a point on the wheel decreases with time.
Units mm. CONCEPT, NOT FOR FABRICATION.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for _p in (str(HERE), str(HERE.parents[1] / ".kit")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from build123d import (Axis, Box, Compound, Cylinder, Face, Plane, Polygon, Polyline, Pos, Rectangle,  # noqa: E402
                       Rot, Sketch, Torus, Vector, Wire, extrude, loft, revolve)
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import sdl_parts as sp  # noqa: E402

B = {
    "RIM_R": 240.0,          # rim outside radius (rolls on the seedbed)
    "RIM": (40.0, 4.0),      # rim flat bar, width (Y) x thickness
    "N_PUNCH": 6,            # punches: spacing = 2 pi R / N = 251 mm, the maize design case
    "PUNCH_L": 55.0,         # punch length beyond the rim: 50 mm sowing depth plus 5 mm
    "PUNCH_W": 24.0,         # punch width at the rim (Y)
    "JAW_T": 2.5,            # jaw sheet
    "DRUM_R": 80.0,          # hub drum outside radius (rolled 3 mm sheet)
    "DRUM_T": 3.0,
    "DRUM_Y": (-40.0, 30.0), # drum from and to (Y)
    "AXLE_D": 25.0,
    "AXLE_Y": (-102.0, 144.0),
    "TUBE": (20.0, 1.5),     # seed tubes, drum to rim
    "RING": (66.0, 72.0),    # printed cell ring: inner radius, outer radius of the cell band
    "BAND_HW": 6.0,          # cell band half width (Y)
    "CELL": (14.3, 9.0),     # cell slot: length round the ring, width across (maize, as option A's plate)
    "CHAMBER_R": 65.0,       # stationary seed chamber outside radius
    "SHOE": (72.5, 76.5),    # stationary shoe under the cells, radii
    "RELEASE": (-45.0, -15.0),   # release window (theta), where the shoe is cut away
    "POOL": (-150.0, -60.0),     # pool window in the chamber wall (theta)
    "LEG": (50.0, 8.0),      # fork legs, flat bar
    "LEG_Y": (-76.0, 118.0), # fork leg inner faces (left leg from -84 to -76, right from 118 to 126)
    "LEG_ANGLE": 50.0,       # fork legs and handle above the ground
    "LEG_L": 400.0,
    "GRIP_H": 950.0,
    "GRIP_Y": 230.0,
}


def _ax_y(r, y0, y1, x=0.0, z=None):
    """Cylinder along Y from y0 to y1 at (x, z) (z defaults to the axle height)."""
    z = B["RIM_R"] if z is None else z
    return Pos(x, (y0 + y1) / 2, z) * Rot(90, 0, 0) * Cylinder(r, abs(y1 - y0))


def _ring_y(r_out, r_in, y0, y1):
    return _ax_y(r_out, y0, y1) - _ax_y(r_in, y0 - 1, y1 + 1)


def _sector(r_in, r_out, y0, y1, a0, a1):
    """Annular sector about the axle between radii r_in and r_out, y0 to y1, angles a0 to a1 (degrees, a0 < a1)."""
    f = Face(Wire(Polyline((r_in, y0, 0), (r_out, y0, 0), (r_out, y1, 0), (r_in, y1, 0), close=True)))
    sw = revolve(f, Axis.Y, a1 - a0)            # covers theta from -(a1 - a0) to 0
    return Pos(0, 0, B["RIM_R"]) * Rot(0, -a1, 0) * sw


def _radial(theta, r, y=0.0):
    t = math.radians(theta)
    return (r * math.cos(t), y, B["RIM_R"] + r * math.sin(t))


def _outward(theta):
    t = math.radians(theta)
    return Vector(math.cos(t), 0, math.sin(t))


def _local(theta):
    """Plane at the axle centre: local +Z radially out at theta, local +X along the rim's direction of travel there,
    local +Y along world +Y."""
    t = math.radians(theta)
    return Plane(origin=(0, 0, B["RIM_R"]), x_dir=(math.sin(t), 0, -math.cos(t)), z_dir=(math.cos(t), 0, math.sin(t)))


def _radial_hole(theta, r, d, y=0.0, length=20.0):
    x, yy, z = _radial(theta, r, y)
    return Plane(origin=(x, yy, z), x_dir=(0, 1, 0), z_dir=tuple(_outward(theta))).from_local_coords(Cylinder(d / 2, length))


def _ring_weld(r, leg, y_face, toward, outside=True):
    """Fillet weld bead round a cylinder of radius r (axis along Y at the axle) where it meets a plate face at
    y = y_face; the bead lies on the 'toward' side (+1 or -1 in Y) of the face, outside or inside the cylinder."""
    tri = [(r, 0.0), (r + leg, 0.0), (r, leg)] if outside else [(r, 0.0), (r - leg, 0.0), (r, leg)]
    f = Face(Wire(Polyline(*[(a, b, 0) for a, b in tri], close=True)))   # radius along X, height along Y
    ring = revolve(f, Axis.Y)
    if toward < 0:
        ring = Rot(0, 0, 180) * ring
    return Pos(0, y_face, B["RIM_R"]) * ring


def _tube_weld(p_face, normal, r_tube, leg, gap=0.0):
    """Fillet weld bead round a tube of radius r_tube standing square on a face: p_face the tube axis point on the
    face, normal the face normal along the tube (gap lifts the bead off a curved face so it does not cut in)."""
    tri = [(r_tube, gap), (r_tube + leg, gap), (r_tube, gap + leg)]
    f = Face(Wire(Polyline(*[(a, 0, b) for a, b in tri], close=True)))
    ring = revolve(f, Axis.Z)
    n = Vector(*normal).normalized()
    ref = Vector(0, 1, 0) if abs(n.Y) < 0.9 else Vector(1, 0, 0)
    return Plane(origin=tuple(p_face), x_dir=tuple(ref.cross(n).normalized()), z_dir=tuple(n)).from_local_coords(ring)


def _line_weld(p0, edge_dir, leg_a, leg_b, length, leg=3.0):
    """Fillet weld bead from p0 along edge_dir for 'length', its legs along leg_a and leg_b (unit vectors)."""
    e, a, b = Vector(*edge_dir).normalized(), Vector(*leg_a).normalized(), Vector(*leg_b).normalized()
    p0 = Vector(*p0)
    if e.cross(a).dot(b) < 0:
        p0 = p0 + e * length
        e = -e
    return Plane(origin=tuple(p0), x_dir=tuple(e), z_dir=tuple(b)).from_local_coords(cp.weld_fillet(length, leg))


def _yz_plate(pts, y0, y1):
    """Plate whose outline [(x, z)] lies in the XZ plane, from y0 to y1."""
    s = extrude(Polygon(*pts, align=None), amount=abs(y1 - y0))      # outline in XY, thickness +Z
    return Pos(0, max(y0, y1), 0) * (Rot(90, 0, 0) * s)               # outline into XZ, thickness toward -Y


def _jaw(xb, xt, wb, wt, zb, zt, t, sign):
    """Jaw plate in the punch frame: inner face from x = xb at the base (z = zb) to xt at the tip (z = zt), thickness
    t toward sign * X, width wb to wt centred on Y = 0."""
    def quad(x0, w, z):
        return Face(Wire(Polyline((x0, -w / 2, z), (x0 + sign * t, -w / 2, z), (x0 + sign * t, w / 2, z), (x0, w / 2, z), close=True)))
    return loft([quad(xb, wb, zb), quad(xt, wt, zt)])


# ---------------------------------------------------------------------------------------------------------------
# One punch, built in its local frame (+Z radial out, +X leading), then placed on the rim at theta
# ---------------------------------------------------------------------------------------------------------------
def punch_parts(k, theta):
    R, L, W, t = B["RIM_R"], B["PUNCH_L"], B["PUNCH_W"], B["JAW_T"]
    tag = f" (punch {k + 1})"
    out = []
    fj = cp.break_edges(_jaw(7.0, 1.0, W, 12.0, R, R + L, t, +1), 0.4)
    out.append(part(f"Fixed jaw{tag}", fj, "mild_steel", "made", group="punches"))
    hinge = (-9.0, R + 5.0)
    for s in (-1, 1):
        y0, y1 = s * W / 2, s * (W / 2 + 3.0)
        ch = _yz_plate([(-14.0, R), (7.0 + t, R), (1.0 + t, R + L - 6.0), (-2.0, R + L - 14.0), (-14.0, R + 9.0)], y0, y1)
        ch = ch - Pos(hinge[0], 0, hinge[1]) * Rot(90, 0, 0) * Cylinder(2.7, 80)
        out.append(part(f"Jaw cheek, {'left' if s < 0 else 'right'}{tag}", cp.break_edges(ch, 0.4), "mild_steel", "made", group="punches"))
    mj = _jaw(-7.0, -1.0, W - 1.0, 11.0, R + 9.5, R + L, t, -1)
    knuckle = Pos(hinge[0], 0, hinge[1]) * Rot(90, 0, 0) * (Cylinder(4.5, W - 1.0) - Cylinder(2.7, W + 2))
    neck = Pos(-8.6, 0, R + 9.0) * Box(3.4, W - 1.0, 3.0)
    out.append(part(f"Moving jaw{tag}", mj + knuckle + neck, "mild_steel", "made", group="punches"))
    for n, s_ in sp.clevis_pin_vec(5, (hinge[0], -(W / 2 + 3.0), hinge[1]), (0, 1, 0), W + 6.0 + 8.0, f", jaw hinge{tag}"):
        out.append(part(n, s_, "zinc_plated", "fastener", group="punches"))
    coils = [Pos(hinge[0], W / 2 + 3.0 + 1.0 + 1.15 * i, hinge[1]) * Rot(90, 0, 0) * Torus(4.0, 0.55) for i in range(5)]
    arm1 = Pos(hinge[0] + 4.0, W / 2 + 4.0, hinge[1] + 8.0) * Cylinder(0.55, 16.0)
    out.append(part(f"Jaw return spring, torsion{tag}", Compound(coils + [arm1]), "stainless", "bought", group="punches"))
    out.append(part(f"Weld, fixed jaw to rim{tag}", _line_weld((7.0 + t, -W / 2, R), (0, 1, 0), (1, 0, 0), (0, 0, 1), W, 3.0),
                    "mild_steel", "weld", group="punches"))
    for s in (-1, 1):
        out.append(part(f"Weld, {'left' if s < 0 else 'right'} cheek to rim{tag}",
                        _line_weld((-14.0, s * (W / 2 + 3.0), R), (1, 0, 0), (0, s, 0), (0, 0, 1), 21.0 + t, 2.5), "mild_steel", "weld", group="punches"))
    pl = _local(theta)
    placed = []
    for p in out:
        q = dict(p)
        q["shape"] = pl.from_local_coords(p["shape"])
        placed.append(q)
    return placed


def option_b():
    R = B["RIM_R"]
    rw, rt = B["RIM"]
    N = B["N_PUNCH"]
    dr, dt = B["DRUM_R"], B["DRUM_T"]
    dy0, dy1 = B["DRUM_Y"]
    tod, tt = B["TUBE"]
    ad = B["AXLE_D"]
    out = []
    thetas = [-90.0 + k * 360.0 / N for k in range(N)]
    screw_th = [th + 30.0 for th in thetas]          # cell ring screws, half way between the tubes

    # ---- wheel: rim, drum, end plate, web plate, end ring, seed tubes, all welded
    rim = _ring_y(R, R - rt, -rw / 2, rw / 2)
    for th in thetas:
        rim = rim - _radial_hole(th, R - rt / 2, 17.0, length=12.0)
    out.append(part("Rim, 40 x 4 flat bar rolled to 480 mm", cp.break_edges(rim, 0.6), "painted_steel", "made", group="wheel"))
    drum = _ring_y(dr, dr - dt, dy0, dy1)
    for th in thetas:
        drum = drum - _radial_hole(th, dr - dt / 2, 17.0, length=10.0)
    for th in screw_th:
        drum = drum - _radial_hole(th, dr - dt / 2, 4.5, y=-8.0, length=10.0)
    out.append(part("Hub drum, 3 mm sheet rolled to 160 mm", drum, "painted_steel", "made", group="wheel"))
    bsq = 32.0
    endp = _ax_y(dr, dy0 - 5.0, dy0) - _ax_y(15.0, dy0 - 6, dy0 + 1)
    for sx in (-1, 1):
        for sz in (-1, 1):
            endp = endp - _ax_y(4.25, dy0 - 6, dy0 + 1, x=sx * bsq, z=R + sz * bsq)
    out.append(part("Drum end plate, left, 5 mm", cp.break_edges(endp, 0.5), "painted_steel", "made", group="wheel"))
    wy0, wy1 = -22.0, -18.0                       # web plate carrying the second bearing
    web = _ax_y(dr - dt, wy0, wy1) - _ax_y(21.0, wy0 - 1, wy1 + 1) - _ax_y(4.25, wy0 - 1, wy1 + 1, x=-30.0) - _ax_y(4.25, wy0 - 1, wy1 + 1, x=30.0)
    out.append(part("Drum web plate, 4 mm", web, "painted_steel", "made", group="wheel"))
    out.append(part("Drum end ring, right, 4 mm", cp.break_edges(_ring_y(dr, 52.0, dy1, dy1 + 4.0), 0.5), "painted_steel", "made", group="wheel"))
    out.append(part("Weld, left end plate to drum", _ring_weld(dr, 3.0, dy0, +1), "painted_steel", "weld", group="wheel"))
    out.append(part("Weld, right end ring to drum", _ring_weld(dr, 3.0, dy1, -1), "painted_steel", "weld", group="wheel"))
    out.append(part("Weld, web plate in drum", _ring_weld(dr - dt, 2.5, wy1, +1, outside=False), "painted_steel", "weld", group="wheel"))
    for k, th in enumerate(thetas):
        n = _outward(th)
        p0, p1 = _radial(th, dr), _radial(th, R - rt)
        pl = Plane(origin=p0, x_dir=(0, 1, 0), z_dir=tuple(n))
        out.append(part(f"Seed tube {k + 1}, 20 x 1.5", pl.from_local_coords(cp.round_tube(tod, tt, R - rt - dr - 0.3)), "painted_steel", "made", group="wheel"))
        out.append(part(f"Weld, seed tube {k + 1} to drum", _tube_weld(p0, tuple(n), tod / 2, 3.0, gap=0.3), "painted_steel", "weld", group="wheel"))
        out.append(part(f"Weld, seed tube {k + 1} to rim", _tube_weld(p1, tuple(-n), tod / 2, 3.0, gap=0.4), "painted_steel", "weld", group="wheel"))
        out += punch_parts(k, th)

    # ---- bearings on the fixed axle: 4-bolt flange bearing on the left end plate, 2-bolt on the web plate
    fl = cp.break_edges(Pos(0, dy0 - 5.0 - 6.0, R) * Box(86.0, 12.0, 86.0), 3.0)
    for sx in (-1, 1):
        for sz in (-1, 1):
            fl = fl - _ax_y(4.25, dy0 - 20, dy0, x=sx * bsq, z=R + sz * bsq)
    brg = fl + _ax_y(31.0, dy0 - 5.0 - 30.0, dy0 - 5.0 - 12.0) - _ax_y(ad / 2, -300, 300)
    out.append(part("Flange bearing, 4-bolt, 25 mm bore (catalogue envelope)", brg, "cast_aluminium", "bought", group="wheel"))
    fl2 = cp.break_edges(Pos(0, wy0 - 5.0, R) * Box(72.0, 10.0, 34.0), 3.0)
    fl2 = fl2 - _ax_y(4.25, wy0 - 20, wy0 + 1, x=-30.0) - _ax_y(4.25, wy0 - 20, wy0 + 1, x=30.0)
    brg2 = fl2 + _ax_y(20.0, wy0, wy1 + 4.0) - _ax_y(ad / 2, -300, 300)     # boss through the web plate's 42 mm hole
    out.append(part("Flange bearing, 2-bolt, 25 mm bore (catalogue envelope)", brg2, "cast_aluminium", "bought", group="wheel"))
    for sx in (-1, 1):
        for sz in (-1, 1):
            for n_, s_ in sp.bolt_set(8, (sx * bsq, dy0 - 17.0, R + sz * bsq), "+y", 17.0, ", left bearing to end plate"):
                out.append(part(n_, s_, "zinc_plated", "fastener", group="wheel"))
    for sx in (-1, 1):
        L8 = 25
        pcs = [(f"M8x{L8} hex bolt (ISO 4017), web bearing to web plate", Pos(sx * 30.0, wy0 - 10.0, R) * sp.to_axis(Pos(0, 0, 1.6) * cp.hex_bolt(8, L8), "-y")),
               ("M8 washer (ISO 7089), web bearing to web plate", Pos(sx * 30.0, wy0 - 10.0, R) * sp.to_axis(cp.washer(8), "-y")),
               ("M8 washer (ISO 7089), web bearing to web plate", Pos(sx * 30.0, wy1, R) * sp.to_axis(cp.washer(8), "+y")),
               ("M8 hex nut (ISO 4032), web bearing to web plate", Pos(sx * 30.0, wy1 + 1.6, R) * sp.to_axis(cp.hex_nut(8), "+y"))]
        for n_, s_ in pcs:
            out.append(part(n_, s_, "zinc_plated", "fastener", group="wheel"))

    # ---- fixed axle, shaft collars, fork legs, crossbar
    ay0, ay1 = B["AXLE_Y"]
    out.append(part("Fixed axle, 25 mm bright bar", Pos(0, ay0, R) * Rot(-90, 0, 0) * cp.round_bar(ad, ay1 - ay0, 1.0),
                    "mild_steel", "made", group="frame"))
    lw, lt = B["LEG"]
    ly_l, ly_r = B["LEG_Y"]
    ang = math.radians(B["LEG_ANGLE"])
    u = Vector(-math.cos(ang), 0, math.sin(ang))
    nvec = Vector(0, 1, 0).cross(u).normalized()
    L = B["LEG_L"]
    for side, y0 in (("left", ly_l - lt), ("right", ly_r)):
        leg = Pos((L + 60.0) / 2 - 30.0, 0, lt / 2) * Box(L + 60.0, lw, lt)
        leg = leg - Cylinder(ad / 2 + 0.25, 50)
        for d_ in (L - 15.0, L + 15.0):
            leg = leg - Pos(d_, 0, 0) * Cylinder(4.25, 50)
        leg = cp.break_edges(leg, 1.0)
        pl = Plane(origin=(0, y0, R), x_dir=tuple(u), z_dir=(0, 1, 0))
        out.append(part(f"Fork leg, {side}, 50 x 8 flat bar", pl.from_local_coords(leg), "painted_steel", "made", group="frame"))
    c0 = Vector(0, 0, R) + u * 330.0
    pl_cb = Plane(origin=(c0.X, ly_l, c0.Z), x_dir=tuple(u), z_dir=(0, 1, 0))
    out.append(part("Fork crossbar, 40 x 20 x 2 RHS", pl_cb.from_local_coords(cp.rhs(40.0, 20.0, 2.0, ly_r - ly_l)), "painted_steel", "made", group="frame"))
    for side, y_face, sgn in (("left", ly_l, +1), ("right", ly_r, -1)):
        for s_ in (-1, 1):
            p0 = Vector(c0.X, y_face, c0.Z) + u * (s_ * 20.0) - nvec * 10.0
            out.append(part(f"Weld, crossbar to {side} leg", _line_weld(tuple(p0), tuple(nvec), (0, sgn, 0), tuple(u * s_), 20.0, 3.0),
                            "painted_steel", "weld", group="frame"))
    for y_c, nm in ((ly_l - lt - 16.0, "left outer"), (ly_r - 16.0, "right inner"), (ly_r + lt, "right outer")):
        col = _ax_y(22.5, y_c, y_c + 16.0) - _ax_y(ad / 2, -300, 300) - Pos(0, y_c + 8.0, R + 18.0) * Cylinder(3.0, 14.0)
        out.append(part(f"Shaft collar, 25 mm, {nm}", cp.break_edges(col, 0.8), "zinc_plated", "bought", group="frame"))
        out.append(part(f"M6x10 set screw (ISO 4026), collar {nm}", Pos(0, y_c + 8.0, R + 22.5) * sp.set_screw(6, 10.0), "zinc_plated", "fastener", group="frame"))

    # ---- hub meter: cell ring (turns with the wheel), seed chamber with shoe (fixed on the axle), brush, hopper
    r_in, r_out = B["RING"]
    hw = B["BAND_HW"]
    ring = _ring_y(r_out, r_in, -hw, hw) + _ring_y(dr - dt, r_in, -hw - 4.0, -hw)      # cell band and its left flange
    cl, cw = B["CELL"]
    for th in thetas:                                                                   # cells on the tube lines
        x, _, z = _radial(th, (r_in + r_out) / 2)
        ring = ring - Plane(origin=(x, 0, z), x_dir=tuple(Vector(0, 1, 0).cross(_outward(th))), z_dir=tuple(_outward(th))).from_local_coords(Box(cl, cw, 20.0))
    for th in screw_th:
        ring = ring - _radial_hole(th, (r_in + dr - dt) / 2, 5.2, y=-8.0, length=12.5)
    out.append(part("Cell ring, printed PETG (6 cells, maize)", ring, "hdpe_natural", "made", group="meter", color="#0F766E"))
    for th in screw_th:
        n = _outward(th)
        x, y, z = _radial(th, dr, -8.0)
        out.append(part("M4x8 pan head screw (ISO 7045), cell ring to drum",
                        Plane(origin=(x, y, z), x_dir=(0, 1, 0), z_dir=tuple(n)).from_local_coords(sp.pan_screw(4, 8.0)), "zinc_plated", "fastener", group="meter"))
        xi, yi, zi = _radial(th, dr - dt, -8.0)
        out.append(part("M4 heat-set insert (brass), cell ring",
                        Plane(origin=(xi, yi, zi), x_dir=(0, 1, 0), z_dir=tuple(n)).from_local_coords(sp.heat_set_insert(4, 5.7)), "brass", "fastener", group="meter"))
    cr = B["CHAMBER_R"]
    s0, s1 = B["SHOE"]
    cy0 = -7.5                                                                          # chamber's left end wall, clear of the web bearing
    cy1 = dy1 - 2.0                                                                     # right end wall, inside the drum's end ring
    ch = _ax_y(cr, cy0, cy1) - _ax_y(cr - 3.0, cy0 + 3.0, cy1 - 3.0)                    # chamber shell
    ch = ch + _ax_y(18.0, cy0, cy1)                                                     # boss clamped on the axle
    ch = ch - _sector(cr - 4.0, cr + 1.0, -hw + 0.5, hw - 0.5, *B["POOL"])              # pool window to the cells
    web_s = _ring_y(s1, cr - 1.0, hw + 0.5, hw + 4.0)                                    # web beside the band, to the shoe
    shoe = _ring_y(s1, s0, -hw + 0.5, hw + 0.5) - _sector(s0 - 1.0, s1 + 1.0, -hw, hw + 1.0, *B["RELEASE"])
    neck = _ax_y(46.0, cy1, dy1 + 26.0) - _ax_y(43.0, cy1 - 3.0, dy1 + 27.0)
    ch = ch + web_s + shoe + neck - _ax_y(ad / 2 + 0.1, -300, 300)
    ch = ch - Pos(0, dy1 + 14.0, R + 44.0) * Box(18.0, 12.0, 8.0)                       # inlet from the hopper's funnel
    ch = ch - Pos(0, 0.0, R + 12.5 + 7.0) * Cylinder(3.0, 16.0)                         # set screw hole in the boss
    out.append(part("Seed chamber with shoe, printed PETG (fixed on the axle)", ch, "hdpe_natural", "made", group="meter", color="#CBD5E1"))
    out.append(part("M6x8 set screw (ISO 4026), seed chamber boss", Pos(0, 0.0, R + 18.0) * sp.set_screw(6, 5.5), "zinc_plated", "fastener", group="meter"))
    x_b, _, z_b = _radial(B["POOL"][0] + 6.0, cr - 1.5)
    brush = Plane(origin=(x_b, 0, z_b), x_dir=tuple(Vector(0, 1, 0).cross(_outward(B["POOL"][0] + 6.0))),
                  z_dir=tuple(_outward(B["POOL"][0] + 6.0))).from_local_coords(Box(3.0, 2 * hw - 2.0, 1.8))
    out.append(part("Singulator brush strip, nylon", brush, "hdpe_black", "bought", group="meter"))
    # hopper above and beside the neck, outside the end ring, 1.7 L (2.1 L with the chamber)
    yh = dy1 + 52.0
    hz0 = R + 90.0                                  # hopper floor; its chute drops about 50 degrees to the neck
    HW, HD, HH = 160.0, 60.0, 205.0
    hop = cp.break_edges(Pos(0, yh, hz0 + HH / 2) * Box(HW, HD, HH), 4.0) - Pos(0, yh, hz0 + HH / 2 + 3.0) * Box(HW - 6.0, HD - 6.0, HH)
    funnel = loft([Pos(0, yh, hz0 + 0.5) * Rectangle(60.0, 30.0), Pos(0, dy1 + 14.0, R + 46.5) * Rectangle(24.0, 18.0)])
    f_in = loft([Pos(0, yh, hz0 + 1.0) * Rectangle(54.0, 24.0), Pos(0, dy1 + 14.0, R + 45.5) * Rectangle(18.0, 12.0)])
    hop = hop + funnel - f_in - Pos(0, yh, hz0 + 3.0) * Box(54.0, 24.0, 6.0)
    hop = hop - Pos(-78.5, yh + 22.0, R + 140.0) * Rot(0, 90, 0) * Cylinder(3.25, 6.0)          # bracket insert hole
    out.append(part("Seed hopper, printed PETG, 1.7 L", hop, "hdpe_natural", "made", group="meter", color="#E5E7EB"))
    out.append(part("Hopper lid, printed PETG", cp.break_edges(Pos(0, yh, hz0 + HH + 1.0) * Box(HW + 4.0, HD + 4.0, 2.0), 0.6), "hdpe_natural", "made", group="meter", color="#94A3B8"))
    # hopper bracket, 25 x 25 x 3 angle: one leg on the hopper's rear face, one on the right fork leg's inside face
    zb_ = R + 140.0
    br_a = Pos(-92.5, ly_r - 1.5, zb_) * Box(25.0, 3.0, 25.0)
    br_b = Pos(-81.5, ly_r - 12.5, zb_) * Box(3.0, 25.0, 25.0)
    brk = (br_a + br_b) - Pos(-97.0, ly_r - 1.5, zb_) * Rot(90, 0, 0) * Cylinder(3.25, 10) - Pos(-81.5, yh + 22.0, zb_) * Rot(0, 90, 0) * Cylinder(2.75, 10)
    out.append(part("Hopper bracket, 25 x 25 x 3 angle", cp.break_edges(brk, 0.4), "painted_steel", "made", group="frame"))
    for p in out:
        if p["name"].startswith("Fork leg, right"):
            p["shape"] = p["shape"] - Pos(-97.0, ly_r + 4.0, zb_) * Rot(90, 0, 0) * Cylinder(3.25, 20.0)
    for n_, s_ in sp.bolt_set(6, (-97.0, ly_r - 3.0, zb_), "+y", 3.0 + B["LEG"][1], ", hopper bracket to fork leg"):
        out.append(part(n_, s_, "zinc_plated", "fastener", group="frame"))
    out.append(part("M5 heat-set insert (brass), hopper bracket", Pos(-80.0, yh + 22.0, zb_) * sp.to_axis(sp.heat_set_insert(5, 3.0), "-x"), "brass", "fastener", group="meter"))
    for n_, s_ in sp.screw_set(5, (-83.0, yh + 22.0, zb_), "+x", 6, ", hopper bracket"):
        out.append(part(n_, s_, "zinc_plated", "fastener", group="frame"))

    # ---- handle: two 22 x 1.2 tubes, flattened at the bottom and bolted to the outside of the fork legs
    top = Vector(0, 0, R) + u * L
    grip_holes = []
    gz = B["GRIP_H"]
    gx = top.X - (gz - top.Z) / math.tan(ang)
    for side, s in (("left", -1), ("right", 1)):
        y_face = (ly_l - lt) if s < 0 else (ly_r + lt)
        tab_c = Vector(0, y_face + s * 2.5, R) + u * L
        tab = Plane(origin=tuple(tab_c), x_dir=tuple(u), z_dir=(0, 1, 0)).from_local_coords(Box(64.0, 30.0, 5.0))
        for d_ in (-15.0, 15.0):
            tab = tab - Pos(*(tuple(tab_c + u * d_))) * Rot(90, 0, 0) * Cylinder(4.25, 20)
        a = tab_c + u * 32.0 + Vector(0, s * 8.5, 0)
        g = Vector(gx, s * B["GRIP_Y"], gz)
        d = (g - a).normalized()
        nn = Vector(0, 1, 0).cross(d).normalized()
        if nn.Z < 0:
            nn = -nn
        top_c = g + nn * 13.5                              # flattened top end on the grip, as option A
        e = top_c - d * 20.0
        tube = sp._plane(tuple(a), tuple(e - a)).from_local_coords(cp.round_tube(22.0, 1.2, (e - a).length))
        ww = nn.cross(d).normalized()
        ttab = Plane(origin=tuple(top_c - d * 20.0 - ww * 17.0 - nn * 2.5), x_dir=tuple(d), z_dir=tuple(nn)).from_local_coords(
            Pos(20.0, 17.0, 2.5) * Box(40.0, 34.0, 5.0))
        ttab = ttab - sp._plane(tuple(top_c - nn * 10), tuple(nn)).from_local_coords(Pos(0, 0, 10) * Cylinder(3.25, 20.0))
        out.append(part(f"Handle tube, {side}, 22 x 1.2, flattened ends", tab + tube + ttab, "painted_steel", "made", group="frame"))
        for n_, s_ in sp.bolt_set_vec(6, tuple(top_c + nn * 2.5), tuple(-nn), 16.0 + sp.curved_face_offset(11.0, 6.0), f", handle top to grip, {side}"):
            out.append(part(n_, s_, "zinc_plated", "fastener", group="frame"))
        grip_holes.append(sp._plane(tuple(top_c - nn * 32), tuple(nn)).from_local_coords(Pos(0, 0, 18) * Cylinder(3.25, 36.0)))
        for d_ in (-15.0, 15.0):
            pnt = tab_c + u * d_
            for n_, s_ in sp.bolt_set(8, (pnt.X, y_face + s * 5.0, pnt.Z), "-y" if s > 0 else "+y", 5.0 + lt, f", handle to {side} fork leg"):
                out.append(part(n_, s_, "zinc_plated", "fastener", group="frame"))
    gp = Pos(gx, -(B["GRIP_Y"] + 45.0), gz) * Rot(-90, 0, 0) * cp.round_tube(22.0, 1.2, 2 * B["GRIP_Y"] + 90.0)
    for h_ in grip_holes:
        gp = gp - h_
    out.append(part("Cross grip, 22 x 1.2 tube", gp, "painted_steel", "made", group="frame"))
    for s in (-1, 1):
        y0 = s * (B["GRIP_Y"] - 20.0)
        rg = Pos(gx, min(y0, y0 - s * 110.0), gz) * Rot(-90, 0, 0) * cp.round_tube(30.0, 3.9, 110.0)
        out.append(part(f"Rubber grip, {'left' if s < 0 else 'right'}", cp.break_edges(rg, 1.0), "epdm", "bought", group="frame"))
    return out
