"""SeedLine TRL 3 sizing (SDL-CAL-001).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes
docs/04-calcs/results.csv (requirement, value, target, status).

Geometry comes from cad/src/model.py (PARAMS and helper functions) and prices from
bom/bom.csv, so the model, the drawing SDL-DWG-001, the BOM and this note agree.
All values are first-principles estimates on paper; nothing here is measured.
"""
import csv
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
import model  # noqa: E402
from model import PARAMS as P  # noqa: E402

G = 9.81
OUT = []          # (requirement, quantity, value, target, status)


def h(title):
    print(f"\n== {title} ==")


def req(rid, quantity, value, target, status):
    OUT.append((rid, quantity, value, target, status))


# ---------------------------------------------------------------------------
# 1. Assumptions
# ---------------------------------------------------------------------------
V_WALK = 2.9 / 3.6            # m/s, design case: walking-speed rule for R1 (SDL-DDR-002 item 5; was 3.0 km/h)
SLIP_TYP = 0.05               # typical travel reduction used for the spacing tables
CELL_V_LIMIT = 0.30           # m/s, assumed working limit for cell fill (to be checked by bench test)
FDM_TOL = 0.2                 # mm, cell size tolerance on a 0.4 mm nozzle (R6)
TOL_RATIO_MAX = 0.10          # tolerance must be 10 % or less of the smallest cell dimension
PRINT_RATE = 6.0              # mm^3/s average volumetric rate on a common desktop FDM printer, incl. travel
INFILL = 0.25                 # infill fraction for a plate
SKIN, WALL = 1.6, 1.2         # mm: top plus bottom skins, perimeter wall thickness
RHO_PETG = 1.27               # g/cm^3
PETG_USD_KG = 25.0
STEEL = 7.85e-6               # kg/mm^3
T_METER = 1.0                 # N m at the plate shaft, design value (first-principles estimate below)
# Soil cases: cone index CI (kPa) for Brixius mobility, specific opener resistance k_o (kPa), covering drag (N)
SOIL = {"good": (300.0, 20.0, 10.0), "design": (200.0, 30.0, 15.0), "heavy": (100.0, 40.0, 20.0)}
OPENER_W, OPENER_WEFF = 18.0, 2.5   # mm runner width; effective failure-zone width factor for a narrow tool
LAT_GRIP = 100.0              # N lateral load at the grip while steering (structural check)
IMPACT = 3.0                  # dynamic factor for drops and stones
YIELD = 235.0                 # MPa, S235 class tube and bar

# ---------------------------------------------------------------------------
# 2. Drive, spacing and range (R3, R4)
# ---------------------------------------------------------------------------
h("2 Drive and spacing")
D = P["WHEEL_D"]
travel = math.pi * D
ratios = {12: 12 / 15, 15: 1.0, 18: 18 / 15}
C = model.center_distance()
print(f"travel per wheel turn {travel:.1f} mm; chain center distance {C:.1f} mm")
for t in (12, 15, 18):
    print(f"  {t} T: pitch diameter {model.sprocket_pd(t):.2f} mm, ratio i = {ratios[t]:.2f}")
links = {}
for t in (12, 15, 18):
    exact = model.chain_links_exact(t, 15, C)
    n = math.ceil(exact)
    slack = (n - exact) * P["PITCH"]
    defl = math.sqrt(slack * C / 2)
    links[t] = (exact, n, slack, defl)
    print(f"  chain for {t} T wheel sprocket: {exact:.2f} pitches exact, fit {n} links "
          f"({'offset link' if n % 2 else 'even'}), slack {slack:.1f} mm, idler deflection {defl:.0f} mm")
IDLER_TRAVEL = max(v[3] for v in links.values())


def spacing(n, i, slip=0.0):
    return travel / (n * i) / (1 - slip)


plates = [("Maize", 250, 4, 1.0), ("Sorghum, groundnut", 150, 6, 1.0), ("Common bean", 100, 9, 1.0),
          ("Spinach", 50, 16, 1.2), ("Carrot, lettuce (pelleted)", 25, 30, 1.2),
          ("Skip-cell, 2 cells", 400, 2, 1.2), ("Skip-cell, 2 cells", 450, 2, 1.0),
          ("Skip-cell, 2 cells", 600, 2, 0.8), ("Shortest", None, 36, 1.2)]
print("plate table: crop, target, cells, ratio, nominal, with 5 % slip")
for crop, tgt, n, i in plates:
    print(f"  {crop:28s} {str(tgt or '-'):>4s} {n:3d} {i:.1f} {spacing(n, i):6.1f} {spacing(n, i, SLIP_TYP):6.1f}")
s_min, s_max = spacing(36, 1.2), spacing(1, 0.8)
s_max2 = spacing(2, 0.8)
print(f"nominal range {s_min:.1f} mm (36 cells, 1.2) to {s_max2:.1f} mm (2 cells, 0.8); "
      f"{s_max:.0f} mm with a 1-cell plate")
# Resolution: every target 25 to 400 mm, best plate (1 to 36 cells) and ratio, with the 5 % slip allowance
worst = (0, None)
for tgt in range(25, 401):
    best = min((abs(spacing(n, i, SLIP_TYP) - tgt) / tgt, n, i) for n in range(1, 37) for i in ratios.values())
    if best[0] > worst[0]:
        worst = (best[0], (tgt, best[1], best[2]))
print(f"worst spacing error over 25 to 400 mm with the best plate: {100 * worst[0]:.1f} % "
      f"(target {worst[1][0]} mm, {worst[1][1]} cells at {worst[1][2]:.1f})")
# Base seeder with the 15 T wheel sprocket only (the 12 and 18 T are the optional ratio kit, SDL-DDR-002 item 4)
worst1 = (0, None)
for tgt in range(25, 401):
    best = min((abs(spacing(n, 1.0, SLIP_TYP) - tgt) / tgt, n) for n in range(1, 37))
    if best[0] > worst1[0]:
        worst1 = (best[0], (tgt, best[1]))
print(f"base seeder, 15 T only (ratio 1.0): {spacing(36, 1.0):.1f} to {spacing(2, 1.0):.1f} mm nominal; worst error over "
      f"25 to 400 mm {100 * worst1[0]:.1f} % (target {worst1[1][0]} mm, {worst1[1][1]} cells)")
req("R3", "Spacing range", f"{s_min:.0f} to {s_max2:.0f} mm nominal with the ratio kit, every 25 to 400 mm target within "
    f"{100 * worst[0]:.1f} %; base 15 T only {spacing(36, 1.0):.0f} to {spacing(2, 1.0):.0f} mm, within {100 * worst1[0]:.0f} %",
    "25 to 400 mm", "met")

# ---------------------------------------------------------------------------
# 3. Metering speed and cell fill (R1)
# ---------------------------------------------------------------------------
h("3 Metering speed")
n_wheel = V_WALK / (travel / 1000)          # rev/s
print(f"wheel {60 * n_wheel:.1f} rpm at {3.6 * V_WALK:.1f} km/h")
dc = model.cell_circle_d() / 1000
cellv = {}
for t, i in ratios.items():
    v = math.pi * dc * n_wheel * i
    vmax = CELL_V_LIMIT / v * 3.6 * V_WALK
    cellv[i] = v
    print(f"  ratio {i:.1f}: plate {60 * n_wheel * i:.1f} rpm, cell speed {v:.3f} m/s (maize cell circle "
          f"{1000 * dc:.1f} mm), walking speed for {CELL_V_LIMIT} m/s: {vmax:.2f} km/h")
print(f"cells per second: maize 4 cells at 1.0 = {4 * n_wheel:.1f}; 36 cells at 1.2 = {36 * 1.2 * n_wheel:.1f}")
# Kinematic fill indicator: the seed must fall its own depth while the open cell passes it
L, Wd, T = P["SEED"]
clen, cdep, cthk = model.cell_size()
v_fill = (clen - 0.5 * L) / 1000 * math.sqrt(G / (2 * cdep / 1000))
print(f"kinematic fill indicator, maize cell {clen:.1f} x {cdep:.1f} mm: {v_fill:.2f} m/s "
      f"(a still seed; seeds dragged by the plate fill at higher cell speeds)")
v_design = cellv[1.0]
req("R1", "Single-seed placement (cell speed as the paper check)",
    f"cell speed {v_design:.3f} m/s at the {3.6 * V_WALK:.1f} km/h walking-speed rule, against an assumed {CELL_V_LIMIT:.2f} m/s limit (no margin); "
    f"misses and multiples not calculable",
    "misses 5 % or less, multiples 5 % or less", "at risk")

# Meter torque, first principles
h("3a Meter torque")
rho_b = 720.0
pool_p = rho_b * G * 0.20 * 0.4                          # Janssen-type wall pressure, 0.2 m seed head, K = 0.4
a_pool = 2 * 0.25 * math.pi * (P["PLATE_D"] / 2000) ** 2   # both faces, lower quarter of the plate in the pool
t_pool = pool_p * a_pool * 0.4 * 0.04                     # friction 0.4 at a 40 mm mean radius
t_brush = 2.0 * 0.4 * P["PLATE_D"] / 2000
t_bear = 0.10
t_fp = t_pool + t_brush + t_bear
print(f"pool friction {t_pool:.3f} N m + brush {t_brush:.3f} + bearings and chain {t_bear:.2f} = {t_fp:.2f} N m; "
      f"design value {T_METER:.1f} N m")

# ---------------------------------------------------------------------------
# 4. Plates per crop (R5, R6)
# ---------------------------------------------------------------------------
h("4 Plates per crop")
CROPS = [("Maize", (12.0, 8.0, 5.0), 4), ("Sorghum", (4.5, 4.0, 3.0), 6), ("Groundnut kernel", (15.0, 9.0, 8.0), 6),
         ("Common bean", (13.0, 8.0, 6.0), 9), ("Spinach", (3.5, 3.0, 2.5), 16),
         ("Carrot, pelleted", (3.3, 3.3, 3.3), 30), ("Carrot, raw", (3.0, 1.2, 0.6), 30)]
plate_rows = []
for crop, seed, n in CROPS:
    cl, cd, th = model.cell_size(seed)
    circ = math.pi * (P["PLATE_D"] - cd)
    nmax = int(circ // (cl + 2.0))
    tol = FDM_TOL / min(cd, cl)
    area = math.pi * (P["PLATE_D"] / 2) ** 2 - n * cl * cd - math.pi * (P["SHAFT_D"] / 2) ** 2
    perim = math.pi * P["PLATE_D"] + 2 * n * cd + math.pi * P["SHAFT_D"]
    v_print = area * SKIN + perim * WALL * th + INFILL * max(area * (th - SKIN) - perim * WALL * th, 0)
    t_h = v_print / PRINT_RATE / 3600
    g = v_print / 1000 * RHO_PETG
    ok = "ok" if tol <= TOL_RATIO_MAX else "too fine"
    plate_rows.append((crop, cl, cd, th, n, nmax, tol, g, t_h, ok))
    print(f"  {crop:18s} cell {cl:5.1f} x {cd:4.1f}, plate {th:4.1f} mm, {n:2d} cells (max {nmax:2d}), "
          f"tolerance {100 * tol:4.1f} % {ok:8s} {g:5.1f} g, {t_h:.2f} h")
mz = plate_rows[0]
worst_print = max(r[8] for r in plate_rows)
req("R5", "Seed size range", "3.5 to 15 mm raw seed (spinach to groundnut); 1 to 2 mm seed only as pelleted seed (about 3.3 mm pellets)",
    "1.5 to 15 mm; seed under 2 mm pelleted (redefined, DDR-001 item 6)", "met")
req("R6", "Printable plates", f"{mz[8]:.1f} h, {mz[7]:.0f} g PETG (maize); up to {worst_print:.1f} h for the "
    f"10 mm groundnut plate; +/-0.2 mm accuracy not verifiable", "2 h or less; +/-0.2 mm",
    "at risk" if worst_print > 2.0 else "met")

# ---------------------------------------------------------------------------
# 5. Mass, center of mass and structure (R11)
# ---------------------------------------------------------------------------
h("5 Mass")
(hbx, hbz), (gx, gz) = model.handle_points()
spread = 4.2
tube25x15 = (25 ** 2 - 22 ** 2) * STEEL * 1000         # kg/m, 25 x 25 x 1.5 square tube
tube20x15 = (20 ** 2 - 17 ** 2) * STEEL * 1000
HOD, HT = P["HANDLE_OD"], P["HANDLE_T"]
rnd_h = math.pi / 4 * (HOD ** 2 - (HOD - 2 * HT) ** 2) * STEEL * 1000   # handle round tube (SDL-DDR-002)
rnd25x15 = math.pi / 4 * (25 ** 2 - 22 ** 2) * STEEL * 1000              # TRL 3 v0.1 handle, for comparison
rnd18x15 = math.pi / 4 * (18 ** 2 - 15 ** 2) * STEEL * 1000
ry, rz, rs = P["RAIL_Y"], P["RAIL_Z"], P["RAIL_S"]
rail_len = 2 * ((P["X_WHEEL"] + 60) - (P["X_PRESS"] - 40)) / 1000
cross_len = 3 * (2 * ry - rs) / 1000
drop_f = 2 * 40 * (rz + rs / 2 - (P["WHEEL_D"] / 2 - 20)) * 6 * STEEL
drop_r = 2 * 40 * (rz + rs / 2 - (P["PRESS_D"] / 2 - 20)) * 6 * STEEL
posts = 4 * (392 - (rz + rs / 2)) / 1000 * tube20x15
brackets = 6 * 2 * 44 * 25 * 3 * STEEL
frame = rail_len * tube25x15 + cross_len * tube25x15 + drop_f + drop_r + posts + brackets
h_len = math.dist((hbx, ry, hbz), (gx, ry * spread, gz)) / 1000
grip_len = 2 * (ry * spread + 45) / 1000
brace_len = 2 * ry * (1 + 0.45 * (spread - 1)) / 1000
handle = (2 * h_len + grip_len) * rnd_h + brace_len * rnd18x15 + 2 * 0.25 * 0.98 + 0.10
handle_old = (2 * h_len + grip_len) * rnd25x15 + brace_len * rnd18x15 + 2 * 0.25 * 0.98 + 0.10
axle = lambda length: math.pi / 4 * P["AXLE_D"] ** 2 * length * STEEL  # noqa: E731
_parts = model.build_parts()
hopper_kg = _parts[4].volume / 1000 * RHO_PETG / 1000
plate_kg = mz[7] / 1000
shank = 20 * 12 * (rz + 60 + P["DEPTH"] - 40) * STEEL
xm, xp = P["X_METER"], P["X_PRESS"]
MASS = [  # (item, group, kg, x of center in mm, z of center in mm)
    ("Drive wheel, 300 mm, with bearings", "wheels", 2.20, 0, 150),
    ("Drive axle, 16 mm", "wheels", axle(P["Y_CHAIN"] * -1 + ry + 17), 0, 150),
    ("Press wheel, 200 mm, with bearings", "wheels", 1.20, xp, 100),
    ("Press axle, 16 mm", "wheels", axle(2 * ry + 50), xp, 100),
    ("Chain, sprockets fitted, idler", "drive and metering", 0.24 + 0.25 + 0.15, -135, 200),
    ("Chain guard, PETG", "drive and metering", 0.15, -135, 200),
    ("Hopper, PETG (model volume)", "drive and metering", hopper_kg, xm, 420),
    ("Housing, shaft, bearings, knob", "drive and metering", 0.30 + axle(1) * 0 + math.pi / 4 * 144 * 178 * STEEL + 0.30 + 0.03, xm, 245),
    ("Seed plate, brush, drop tube", "drive and metering", plate_kg + 0.05 + 0.03, xm, 230),
    ("Opener shoe, shank, clamp", "opener and covering", 0.35 + shank + 0.30, -215, 100),
    ("Covering chains and bracket", "opener and covering", 0.40, -380, 80),
    ("Frame: rails, cross members, drops, posts, brackets", "frame and handle", frame, -280, 215),
    ("Handle, grip, brace, sleeves", "frame and handle", handle, (hbx + gx) / 2, (hbz + gz) / 2),
    ("Fasteners, pins, paint", "hardware", 0.45, -300, 215),
]
MARKER = ("Row marker kit", "marker", 1.0, 47, 150)
base = sum(m[2] for m in MASS)
xcg = sum(m[2] * m[3] for m in MASS) / base
zcg = sum(m[2] * m[4] for m in MASS) / base
full = base + MARKER[2]
groups = {}
for m in MASS + [MARKER]:
    groups[m[1]] = groups.get(m[1], 0) + m[2]
for k, v in groups.items():
    print(f"  {k:22s} {v:5.2f} kg")
print(f"frame {frame:.2f} kg ({rail_len + cross_len:.2f} m of 25 x 25 x 1.5 tube); handle {handle:.2f} kg "
      f"({h_len * 1000:.0f} mm per side tube, {HOD:.0f} x {HT} round); 25 x 1.5 handle would be {handle_old:.2f} kg, "
      f"saving {handle_old - handle:.2f} kg")
print(f"base seeder {base:.2f} kg, with marker kit {full:.2f} kg; center of mass x = {xcg:.0f} mm, z = {zcg:.0f} mm")
seed_kg = model.hopper_volume_l() * 0.72
print(f"seed load, full hopper of maize: {seed_kg:.2f} kg")
print(f"margin to 15 kg: base {15 - base:.2f} kg, with marker {15 - full:.2f} kg")
req("R11", "Mass and handling", f"{base:.1f} kg base; {full:.1f} kg with the marker kit; grip 850 to 1,050 mm",
    "15 kg or less", "met" if full <= 15 else "not met")

# ---------------------------------------------------------------------------
# 6. Wheel loads, push force and slip (R4, R10)
# ---------------------------------------------------------------------------
h("6 Push force")
theta = math.radians(P["HANDLE_ANGLE"])
x_op, z_op = xm + 20, -P["DEPTH"] / 2
W = (base + seed_kg) * G
xcg_s = (base * xcg + seed_kg * xm) / (base + seed_kg)


def brixius_mr(Nw, b, d, ci):
    bn = ci * 1000 * b * d / max(Nw, 1e-6) / (1 + 3 * b / d)
    return Nw * (1 / bn + 0.04), bn


def statics(case, H, phi):
    """Wheel loads and rolling resistance for a push H (horizontal part) at phi degrees below horizontal.
    Rolling forces act at ground level, so they add no moment about the press wheel contact."""
    ci, ko, dc = SOIL[case]
    draft = ko * 1000 * (OPENER_WEFF * OPENER_W / 1000) * (P["DEPTH"] / 1000)
    V = H * math.tan(math.radians(phi))
    # moments about the press wheel contact (x = xp, z = 0), positive nose-down
    m = (H * (gz / 1000) - V * (xp - gx) / 1000 + draft * (-z_op / 1000) + W * (xcg_s - xp) / 1000)
    N1 = m / ((P["X_WHEEL"] - xp) / 1000)
    N2 = W + V - N1
    if N1 <= 0 or N2 <= 0:
        return None
    R1, bn1 = brixius_mr(N1, P["WHEEL_W"] / 1000, P["WHEEL_D"] / 1000, ci)
    R2, bn2 = brixius_mr(N2, P["PRESS_W"] / 1000, P["PRESS_D"] / 1000, ci)
    return dict(H=H, V=V, N1=N1, N2=N2, R1=R1, R2=R2, draft=draft, dc=dc, bn1=bn1, bn2=bn2, phi=phi,
                resid=H - (R1 + R2 + draft + dc))


def solve(case, phi):
    """Smallest push H that balances the resistance at push angle phi, or None if no balance exists
    (a wheel lifts, or the press wheel sinks faster than the push grows)."""
    Hs = np.arange(1.0, 600.0, 0.5)
    for H in Hs:
        st = statics(case, H, phi)
        if st and st["resid"] >= 0:
            return st
    return None


PUSH = {}
for case in SOIL:
    along = solve(case, P["HANDLE_ANGLE"])
    horiz = solve(case, 0.0)
    feas = [r for r in (solve(case, float(f)) for f in range(0, int(P["HANDLE_ANGLE"]) + 1)) if r]
    best = min(feas, key=lambda r: r["H"]) if feas else None
    use = along or best
    PUSH[case] = dict(along=along, horiz=horiz, best=best, use=use,
                      band=(min(r["phi"] for r in feas), max(r["phi"] for r in feas)) if feas else None)
    fmt = lambda r: "no balance" if r is None else f"{r['H']:.0f} N"  # noqa: E731
    print(f"  {case:6s}: along the handle {fmt(along)}; horizontal {fmt(horiz)}; "
          f"lowest {fmt(best)} at {best['phi']:.0f} deg; balance possible from {PUSH[case]['band'][0]:.0f} "
          f"to {PUSH[case]['band'][1]:.0f} deg")
    u = use
    print(f"          at {u['phi']:.0f} deg: V = {u['V']:.0f} N, rolling {u['R1'] + u['R2']:.0f} N "
          f"(coefficient {(u['R1'] + u['R2']) / (u['N1'] + u['N2']):.3f}), opener {u['draft']:.0f} N, "
          f"chains and press {u['dc']:.0f} N; wheel loads {u['N1']:.0f} / {u['N2']:.0f} N, Bn {u['bn1']:.0f} / {u['bn2']:.0f}")
print(f"handle angle {P['HANDLE_ANGLE']:.0f} deg; grip at x = {gx:.0f} mm, {P['GRIP_H']:.0f} mm high; "
      f"seeder plus full hopper {W:.0f} N, center of mass {xcg_s - xp:.0f} mm ahead of the press wheel")
pd = PUSH["design"]["along"]["H"]
print(f"grip {xp - gx:.0f} mm behind the press wheel; design case margin to 150 N: {100 * (150 - pd) / 150:.0f} %")
ph = PUSH["heavy"]["best"]
req("R10", "Push effort, design case", f"{pd:.0f} N along the handle, {PUSH['design']['best']['H']:.0f} N at the best "
    f"angle ({PUSH['design']['best']['phi']:.0f} deg); heavy loose seedbed {ph['H']:.0f} N at best, no balance along the handle",
    "150 N or less", "not met" if pd > 150 else "at risk")

h("6a Slip")
SLIP = {}
for case in SOIL:
    a = PUSH[case]["use"]
    for i in (1.0, 1.2):
        F = T_METER * i / (P["WHEEL_D"] / 2000)
        mu = F / a["N1"]
        cap = 0.88 * (1 - math.exp(-0.1 * a["bn1"]))
        s = -math.log(1 - mu / cap) / 7.5 if mu < cap else float("inf")
        SLIP[(case, i)] = s
        print(f"  {case:6s} ratio {i:.1f}: drive force {F:.1f} N on {a['N1']:.0f} N wheel load, "
              f"traction ratio {mu:.3f}, skid {100 * s:.2f} %")
rim_err = P["LUG_H"] / (P["WHEEL_D"] / 2)
print(f"rolling radius band (lugs fully sunk to lug tips): up to {100 * rim_err:.1f} % shorter travel per turn")
s_worst = max(SLIP.values())
req("R4", "Spacing follows travel; slip", f"skid {100 * min(SLIP.values()):.1f} to {100 * s_worst:.1f} % from meter torque; "
    f"rolling radius uncertain by up to {100 * rim_err:.1f} %", "8 % or less", "met")

# ---------------------------------------------------------------------------
# 7. Structure (R15 support, R18)
# ---------------------------------------------------------------------------
h("7 Structure")
Z_rail = (25 ** 4 - 22 ** 4) / (6 * 25)
Z_rnd = math.pi * (HOD ** 4 - (HOD - 2 * HT) ** 4) / (32 * HOD)
Z_rnd_old = math.pi * (25 ** 4 - 22 ** 4) / (32 * 25)
F_rail = (W + PUSH["heavy"]["use"]["V"]) / 2
M_rail = F_rail * (P["X_WHEEL"] - P["X_PRESS"]) / 4 / 1000 * IMPACT
M_clamp = PUSH["heavy"]["use"]["draft"] * (rz + P["DEPTH"] / 2) / 1000 / 2
s_rail = (M_rail + M_clamp) * 1000 / Z_rail
M_h = LAT_GRIP * h_len / 2
s_h = M_h * 1000 / Z_rnd
Z_ax = math.pi * 16 ** 3 / 32
M_ax = PUSH["heavy"]["use"]["N2"] * (2 * ry + rs) / 4 / 1000 * IMPACT
s_ax = M_ax * 1000 / Z_ax
chain_t = T_METER * 1.2 / (model.sprocket_pd(15) / 2000)
dflat = T_METER * 1.2 / 0.005 / (6 * 7)
print(f"rail: M = {M_rail:.1f} N m (x{IMPACT:.0f} impact) + clamp {M_clamp:.1f} N m on Z = {Z_rail:.0f} mm^3: "
      f"{s_rail:.0f} MPa, factor {YIELD / s_rail:.1f}")
print(f"handle side tube {HOD:.0f} x {HT}: {LAT_GRIP:.0f} N lateral at the grip, M = {M_h:.0f} N m per tube, "
      f"{s_h:.0f} MPa, factor {YIELD / s_h:.1f} (25 x 1.5 tube: factor {YIELD / (M_h * 1000 / Z_rnd_old):.1f})")
print(f"press axle: {M_ax:.1f} N m (x{IMPACT:.0f}), {s_ax:.0f} MPa; chain tension {chain_t:.0f} N "
      f"(about 7.8 kN minimum tensile for #35); plate D-flat bearing {dflat:.1f} MPa in PETG")

# ---------------------------------------------------------------------------
# 8. Work rate and hopper (R9, R12)
# ---------------------------------------------------------------------------
h("8 Work rate and hopper")
ROW_M, TURN_S, REFILL_S, REST = 50.0, 15.0, 90.0, 0.85
row_sp = P["ROW_SPACING"] / 1000
theo = row_sp * V_WALK * 3600 / 1e4
hop_l = model.hopper_volume_l()
seeds_fill = hop_l * 720 / 0.30
row_fill = seeds_fill * 0.25
t_row = ROW_M / V_WALK
eff = t_row / (t_row + TURN_S) * (row_fill / V_WALK) / (row_fill / V_WALK + REFILL_S) * REST
cap = theo * eff
print(f"theoretical {theo:.3f} ha/h; field efficiency {100 * eff:.0f} % ({ROW_M:.0f} m rows, {TURN_S:.0f} s turns, "
      f"{REFILL_S:.0f} s refills, {100 * REST:.0f} % working time); field capacity {cap:.3f} ha/h ({1 / cap:.1f} h/ha)")
veg = 0.30 * V_WALK * 3600 / 1e4 * eff
print(f"0.3 m vegetable rows: {veg:.3f} ha/h; maize seeds per hectare {1e4 / (row_sp * 0.25):,.0f}")
print(f"hopper {hop_l:.2f} L (model cavity), {hop_l * 0.72:.2f} kg maize, {seeds_fill:,.0f} seeds, {row_fill:,.0f} m of row, "
      f"{row_fill * row_sp / 1e4:.3f} ha per fill")
print(f"at the R1 walking speed of {CELL_V_LIMIT / cellv[1.0] * 3.6 * V_WALK:.2f} km/h: {cap * CELL_V_LIMIT / cellv[1.0]:.3f} ha/h")
req("R9", "Work rate", f"{cap:.3f} ha/h ({1 / cap:.1f} h/ha)", "0.1 ha/h or more", "met" if cap >= 0.1 else "not met")
req("R12", "Hopper", f"{hop_l:.2f} L; {row_fill:,.0f} m of maize row per fill", "2 L or more", "met")

# ---------------------------------------------------------------------------
# 9. Depth control (R8)
# ---------------------------------------------------------------------------
h("9 Depth")
x_tip = xm + 88
kf = (x_tip - xp) / (P["X_WHEEL"] - xp)
print(f"opener point x = {x_tip:.0f} mm: depth changes by {kf:.2f} of a front wheel rise and {1 - kf:.2f} of a press wheel rise")
print(f"+/-10 mm depth allows +/-{10 / kf:.0f} mm under the front wheel or +/-{10 / (1 - kf):.0f} mm under the press wheel; "
      f"a 50 mm clod under the front wheel lifts the opener {50 * kf:.0f} mm")
req("R8", "Sowing depth", f"10 to 60 mm in 10 mm steps; +/-10 mm for wheel-path bumps of +/-{10 / kf:.0f} mm or less "
    f"under the drive wheel (ploughed field-crop seedbed)", "10 to 60 mm; +/-10 mm on a ploughed field-crop seedbed (restated, DDR-002)", "met")

# ---------------------------------------------------------------------------
# 10. Spacing uniformity (R2), Monte Carlo
# ---------------------------------------------------------------------------
h("10 Spacing uniformity")
rng = np.random.default_rng(7256)
N_CELLS_MC = 20000
P_MISS, P_DOUBLE, SIG_DROP, SIG_SLIP = 0.05, 0.04, 15.0, 0.015
s_nom = spacing(4, 1.0)
slip = np.clip(rng.normal(SLIP_TYP, SIG_SLIP, N_CELLS_MC), 0, 0.2)
x_cells = np.cumsum(np.full(N_CELLS_MC, s_nom) / (1 - slip))
u = rng.random(N_CELLS_MC)
pos = []
for x, uu in zip(x_cells, u):
    if uu < P_MISS:
        continue
    pos.append(x + rng.normal(0, SIG_DROP))
    if uu > 1 - P_DOUBLE:
        pos.append(x + rng.uniform(0, 30) + rng.normal(0, SIG_DROP))
pos = np.sort(np.array(pos))
sp = np.diff(pos)
mean = sp.mean()
cv_all = sp.std() / mean
xref = s_nom / (1 - SLIP_TYP)
singles = sp[(sp > 0.5 * xref) & (sp <= 1.5 * xref)]
cv_single = singles.std() / singles.mean()
miss_i = np.mean(sp > 1.5 * xref)
mult_i = np.mean(sp <= 0.5 * xref)
print(f"miss {100 * P_MISS:.0f} %, doubles {100 * P_DOUBLE:.0f} %, drop scatter {SIG_DROP:.0f} mm, slip {100 * SLIP_TYP:.0f} +/- {100 * SIG_SLIP:.1f} %")
print(f"CV of all spacings {100 * cv_all:.1f} %; precision (CV of singles, 0.5 to 1.5 x) {100 * cv_single:.1f} %; "
      f"miss index {100 * miss_i:.1f} %, multiple index {100 * mult_i:.1f} %")
req("R2", "Spacing uniformity", f"CV {100 * cv_all:.0f} % of all spacings; {100 * cv_single:.0f} % for singles (inputs assumed)",
    "CV 30 % or less", "at risk" if cv_all > 0.30 else "met")

# ---------------------------------------------------------------------------
# 11. Cost (R16, R17)
# ---------------------------------------------------------------------------
h("11 Cost")
rows = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
marker = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("14 "))
ratio_kit = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("16 "))
base_usd = tot - marker - ratio_kit
budget = 400
print(f"BOM {len(rows)} lines, all priced: base ${base_usd:.2f}, marker kit ${marker:.2f}, ratio kit ${ratio_kit:.2f}, "
      f"total ${tot:.2f} against budget_usd ${budget}")
print(f"base cost {100 * (base_usd / 200 - 1):+.1f} % against the about $200 target of R17")
req("R16", "Prototype cost", f"${tot:.0f}", "$400 or less", "met" if tot <= budget else "not met")
req("R17", "Replication cost, base seeder", f"${base_usd:.0f}", "about $200 or less",
    "met" if base_usd <= 200 else "not met")

# ---------------------------------------------------------------------------
# Design-review requirements (no number to calculate at TRL 3)
# ---------------------------------------------------------------------------
req("R7", "Crop change", "Side door and hand knob in the model; no tools", "2 min or less, no tools", "not verifiable at TRL 3")
req("R13", "Row spacing kit", f"Marker reach 200 to 900 mm in the model, set at {P['ROW_SPACING']:.0f} mm", "200 to 900 mm, +/-25 mm", "met")
req("R14", "Guarding", "Band guard with an outboard face plate over both sprockets and the idler", "Nip points covered", "met")
req("R15", "Durability", "Stresses low (section 7); wear life of plates, brush and chain unknown", "5 seasons; plates 1 season", "not verifiable at TRL 3")
req("R18", "Local build", "Bolted 25 mm square tube, 6 mm plate, #35 chain; drill and bolts", "Common sections and parts", "met")

h("Requirements")
order = {"not met": 0, "at risk": 1, "not verifiable at TRL 3": 2, "met": 3}
OUT.sort(key=lambda r: int(r[0][1:]))
for r in OUT:
    print(f"  {r[0]:4s} {r[4]:24s} {r[2]}")
counts = {k: sum(1 for r in OUT if r[4] == k) for k in order}
print("counts:", ", ".join(f"{k} {v}" for k, v in counts.items()), f"(total {len(OUT)})")
with (Path(__file__).parent / "results.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["requirement", "quantity", "value", "target", "status"])
    w.writerows(OUT)
print("wrote docs/04-calcs/results.csv")
