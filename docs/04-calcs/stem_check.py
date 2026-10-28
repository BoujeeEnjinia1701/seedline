"""SeedLine STEM check (SDL-STM-001, STANDARDS section 20).

Run from the repo root:  python3 docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv, read by docs/01b-stem-check.md. Geometry comes from cad/src/model.py
(option A) and cad/src/punch_wheel.py (option B); the option A figures are the ones SDL-CAL-001 prints
(docs/04-calcs/sizing.py), recomputed here to first order so the check reruns when the design changes.
A check is a first-order screen; it never replaces the calculation note.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad/src")]
from stem_check import Check, limits, WITHIN, PLAUSIBLE, FIX, FAILS  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P  # noqa: E402
from punch_wheel import B  # noqa: E402

G = 9.81
c = Check(ROOT / "docs/04-calcs/stem_results.csv")
cal = {r["requirement"]: r for r in csv.DictReader((ROOT / "docs/04-calcs/results.csv").open())}

# ---------------------------------------------------------------------------------------------------------------
# Option A: cell plate on a chain drive (the current design)
# ---------------------------------------------------------------------------------------------------------------
V = 2.9 / 3.6                                      # m/s, walking-speed rule (SDL-DDR-002 item 5)
travel = math.pi * P["WHEEL_D"]                     # mm per wheel turn over the lug tips
c.order_of_magnitude("S1", "In-row spacing follows travel: 4-cell maize plate at ratio 1.0 gives 236 mm nominal for the 250 mm target, about 220 to 240 mm with the 1.2 to 1.7 % skid and up to 6.7 % shorter rolling radius, so spacing is calibrated per seedbed",
                     "Mathematics", "Units and dimensional analysis", claimed=236.0, estimate=travel / 4 / 1.0, unit="mm",
                     law="Spacing = pi D / (cells x ratio); D = 300 mm over the lug tips", closed_by="SDL-CAL-001 section 2")
exact = model.chain_links_exact(15, 15)
c.claim("S2", "The 76-link #35 chain fits the 286 mm sprocket centres, the spring tensioner taking up the slack",
        "Engineering and technology", "Manufacturing tolerances",
        law="Chain length L/p = 2C/p + (T1 + T2)/2 + ((T2 - T1)/2 pi)^2 p/C; idler deflection sqrt(slack C / 2) within the tensioner's 45 mm",
        value=round(math.sqrt((76 - exact) * P["PITCH"] * model.center_distance() / 2), 1), limit=45.0, unit="mm idler deflection",
        rule="below", closed_by="SDL-CAL-001 section 2")
t_pool = 720 * G * 0.20 * 0.4 * (2 * 0.25 * math.pi * (P["PLATE_D"] / 2000) ** 2) * 0.4 * 0.04
t_meter = t_pool + 2.0 * 0.4 * P["PLATE_D"] / 2000 + 0.10
c.claim("S3", "Meter torque at the plate shaft stays under the 1.0 N m design value", "Physics", "Mechanics and statics",
        law="Janssen wall pressure of a 0.2 m seed head on the lower quarter of the plate, friction 0.4; brush drag; bearings and chain 0.1 N m",
        value=round(t_meter, 2), limit=1.0, unit="N m", rule="below", closed_by="SDL-CAL-001 section 3a")
chain_t = 1.0 * 1.2 / (model.sprocket_pd(15) / 2000)
c.claim("S4", "Chain tension at the design meter torque with a 1.2 service factor is far below the #35 chain's minimum tensile strength",
        "Physics", "Strength of materials", law="T = torque / pitch radius; #35 roller chain minimum tensile strength about 7.8 kN (ANSI B29.1 class)",
        value=round(chain_t, 0), limit=7800.0 / 10, unit="N (limit is 10 % of the minimum tensile strength)", rule="below", closed_by="SDL-CAL-001 section 7")
skid = float(cal["R4"]["value"].split("skid ")[1].split(" to ")[1].split(" %")[0])
c.claim("S5", "Wheel skid from the meter torque stays under 8 %, so spacing follows travel", "Physics", "Mechanics and statics",
        law="Traction ratio = drive force / wheel load; Brixius traction relation for a rigid wheel in a cone index of 100 to 300 kPa",
        value=skid, limit=8.0, unit="%", rule="below", closed_by="SDL-CAL-001 section 6a")
dc = model.cell_circle_d() / 1000
cell_v = math.pi * dc * V / (travel / 1000)
c.cited("S6", f"Each maize cell fills with one seed at {cell_v:.3f} m/s cell speed (walking-speed rule 2.9 km/h)", "Physics", "Mechanics and statics",
        law="Gravity fill of a cell passing a seed pool; the assumed 0.30 m/s working limit for vertical cell plates is not from a cited test; the kinematic indicator for a still seed (the seed falls its own depth while the open cell passes) is 0.20 m/s",
        detail=f"{cell_v:.3f} m/s against an assumed 0.30 m/s, no margin; a seed dragged by the plate fills at higher speed than a still seed",
        verdict=PLAUSIBLE, closed_by="")
cv_all = float(cal["R2"]["value"].split("CV ")[1].split(" %")[0])
c.cited("S7", f"Spacing coefficient of variation of {cv_all:.0f} % of all spacings, design case (target 30 %)", "Mathematics", "Statistics and uncertainty",
        law="Monte Carlo of 20,000 cells with an assumed 5 % miss, 4 % double, 15 mm drop scatter and 5 +/- 1.5 % slip; the result is set by the assumed miss and double rates, which only a bench test gives",
        detail=f"{cv_all:.0f} % of all spacings, 9 % for singles, against 30 %; within the uncertainty of the assumed inputs",
        verdict=PLAUSIBLE, closed_by="")
push = float(cal["R10"]["value"].split(" N")[0])
c.claim("S8", f"Horizontal component of the push in the design case is 150 N or less (the push applied along the 50 deg handle is {push / math.cos(math.radians(50)):.0f} N, {push * math.tan(math.radians(50)):.0f} N of it downward)", "Physics", "Mechanics and statics",
        law="Planar statics with Brixius motion resistance (used outside its calibrated range for small rigid wheels), opener draft from an assumed 30 kPa specific resistance (68 of the 133 N)",
        value=push, limit=150.0, unit="N", rule="below", margin=0.15, closed_by="")
c.cited("S9", f"One operator sustains the push: {push:.0f} N horizontal ({push / math.cos(math.radians(50)):.0f} N along the handle) at 0.81 m/s is {push * V:.0f} W of external work while walking, with a 15 s turn every 62 s",
        "Biology", "Ergonomics",
        law="Sustained pushing guidance (ISO 11228-2 method) depends on distance, frequency, height and the population; not yet assessed. The kit's screening value for sustained cranking is 75 W",
        detail=f"{push * V:.0f} W external against a 75 W cranking screen; walking push uses larger muscle groups; ISO 11228-2 assessment to do",
        verdict=PLAUSIBLE, closed_by="")
mass = float(cal["R11"]["value"].split("; ")[1].split(" kg")[0])
c.claim("S10", "Seeder with the marker kit weighs 15 kg or less", "Physics", "Mechanics and statics", law="Mass build-up from the model's part volumes (steel 7,850 kg/m3, PETG 1,270 kg/m3, aluminium 2,700 kg/m3), every fastener from the model, and about 4.5 kg of catalogue-class bought parts whose 5 % error is about 0.2 kg",
        value=mass, limit=15.0, unit="kg", rule="below", margin=0.02, closed_by="")
c.claim("S11", "Side rails stay below yield with a dynamic factor of 3 for drops and stones", "Physics", "Strength of materials",
        law="Beam bending of 25 x 25 x 1.5 square tube, S235 yield 235 MPa (EN 10025-2)", value=70.0, limit=235.0 / 1.5, unit="MPa (limit is yield / 1.5)",
        rule="below", closed_by="SDL-CAL-001 section 7")
c.claim("S12", "Handle side tube (22 x 1.2) stays below yield under a 100 N side load at the grip together with the heavy-seedbed push (221 N at 36 deg)", "Physics", "Strength of materials",
        law="Cantilever bending of round tube in two planes, combined; S235 yield 235 MPa (independent review of 2026-10-24 added the push component)", value=143.0, limit=235.0 / 1.5, unit="MPa (limit is yield / 1.5)", rule="below",
        closed_by="SDL-CAL-001 section 7 (fatigue to test at TRL 4)")
omega = 2 * math.pi * (V / (travel / 1000))
c.claim("S13", "A seed in a cell is not thrown out of the cell by the plate's rotation", "Physics", "Mechanics and statics",
        law="Centripetal acceleration omega^2 r at the cell circle against g", value=round(omega ** 2 * dc / 2, 2), limit=G, unit="m/s2", rule="below",
        closed_by="This file")
theo = P["ROW_SPACING"] / 1000 * V * 3600 / 1e4
c.order_of_magnitude("S14", "Field capacity 0.142 ha/h (7.1 h/ha) for maize on 0.75 m rows at 2.9 km/h", "Mathematics", "Orders of magnitude",
                     claimed=0.142, estimate=theo * 0.65, unit="ha/h", law="Capacity = row spacing x speed x field efficiency (65 %: 50 m rows, 15 s turns, 90 s refills, 85 % working time)",
                     closed_by="SDL-CAL-001 section 8")
hop = model.hopper_volume_l()
c.order_of_magnitude("S15", "One 2.42 L hopper fill sows about 1,450 m of maize row at 250 mm", "Mathematics", "Orders of magnitude",
                     claimed=1451.0, estimate=hop * 0.72 / 0.30e-3 * 0.25, unit="m", law="Row length = volume x bulk density (0.72 kg/L) / seed mass (0.30 g) x spacing",
                     closed_by="SDL-CAL-001 section 8")
t_gn = float(cal["R6"]["value"].split("up to ")[1].split(" h")[0])
c.claim("S16", "The 10 mm groundnut plate, the slowest, prints in 2 h or less", "Engineering and technology", "Manufacturing tolerances",
        law="Print time = deposited volume / 6 mm3/s average rate (unsourced; 1.6 mm skins, 1.2 mm walls round the rim, every cell and the bore, 20 % infill since SDL-DEC-001 F8). With the cell ends left out and 25 % infill it read 1.96 h; corrected it was 2.05 h, a fail, fixed by F8",
        value=t_gn, limit=2.0, unit="h", rule="below", margin=0.1, closed_by="")
c.cited("S17", "A desktop FDM print holds the cell size closely enough: +/-0.2 mm on the pelleted carrot cell (3.8 mm deep for a 3.3 mm pellet)",
        "Engineering and technology", "Manufacturing tolerances", law="Tolerance ratio 0.2 / 3.8 mm = 5.3 % of the cell, but 43 % of its 0.47 mm clearance over the pellet; FDM holes and slots print undersize (a bias, not only a tolerance)",
        detail="5.3 % of the cell against the 10 % rule; tight against the clearance; a printed test coupon of cells sets the offset", verdict=PLAUSIBLE, closed_by="")
c.claim("S18", "A drive-wheel bump moves the opener by 0.69 of the bump, so +/-10 mm depth holds for bumps up to about +/-14.5 mm (ploughed seedbed)",
        "Physics", "Mechanics and statics", law="Rigid frame on two wheels: the opener point, 181 mm behind the drive axle on a 580 mm wheelbase, moves (x - x_press) / wheelbase of a drive wheel rise",
        value=round((model.opener_front_x() - P["X_PRESS"]) / (P["X_WHEEL"] - P["X_PRESS"]), 2), limit=1.0, unit="of a drive-wheel rise", rule="below", closed_by="SDL-CAL-001 section 9")
c.claim("S19", "Printed PETG plate takes the drive at its D-flat without yielding", "Chemistry", "Materials and polymer chemistry",
        law="Bearing stress = torque x 1.2 / (lever arm x flat area); PETG tensile yield about 50 MPa (typical datasheet value)", value=5.7, limit=50.0 / 3,
        unit="MPa (limit is yield / 3 for a printed part)", rule="below", closed_by="SDL-CAL-001 section 7")
c.cited("S20", "PETG plates degrade in strong sun; ASA is used where plates stay in the sun, PLA for trials only", "Chemistry", "Materials and polymer chemistry",
        law="UV photo-oxidation of polyesters; ASA's acrylic outer phase is UV stable (polymer supplier datasheets)", detail="Material rule decided (SDL-DDR-001 item 9); plates inspected each season (PRC Safety)",
        verdict=WITHIN, closed_by="SDL-PRC-001 Safety")
c.cited("S21", "Treated seed is toxic; gloves, no eating or drinking while filling, cleaning outdoors and a hopper never used for food control the exposure",
        "Biology", "Toxicology", law="Seed treatment labels and humanitarian guidance require PPE, especially gloves (ICRC, Warning: treated seeds)",
        detail="Safety claim only; the design adds no exposure route beyond filling and cleaning", verdict=WITHIN, closed_by="SDL-PRC-001 Safety")
c.claim("S22", "Maize sown at 50 mm sits within the recommended seeding depth", "Biology", "Ecology and agronomy",
        law="Purdue University Department of Agronomy (2022): most common recommended corn seeding depths are 1.5 to 2 inches (38 to 51 mm); the design case sits at the top of the range and +/-10 mm control spans 40 to 60 mm",
        value=50.0, limit=51.0, unit="mm", rule="below", closed_by="Purdue Agronomy (2022); depth set per crop on the shank")
c.cited("S23", "Even spacing raises yield: about 140 to 160 kg/ha of maize per 25 mm less spacing standard deviation, less at smallholder yield levels",
        "Biology", "Ecology and agronomy", law="Nielsen, Purdue University plant spacing trials", detail="Cited effect; SeedLine claims only that spacing follows travel, not a yield figure",
        verdict=WITHIN, closed_by="SDL-PRB-001")
# constructability details found by the kit 1.9 D3 model, fixed under the standing instruction of 2026-10-23
c.cited("S24", "The housing door's two thumb screws land in solid housing wall", "Engineering and technology", "Manufacturing tolerances",
        law="Fit check in the detailed model: as drawn at kit 1.7 the screws at 12 mm from the door's rear edge stood over the 128 x 132 opening, not over wall",
        detail="Fixed: door 146 x 150 to the housing's edges; screws at 7 mm from the rear edge (rear wall band) and 7 mm up (floor band), into M4 heat-set inserts",
        verdict=WITHIN, closed_by="SDL-DEC-001 F1 (decided under the standing instruction of 2026-10-23)")
c.cited("S25", "The wheel hub cross bolt clears the wheel's disc web", "Engineering and technology", "Manufacturing tolerances",
        law="Fit check in the detailed model: the cross hole at 107 mm put the bolt head and nut in the plane of the 2 mm web",
        detail="Fixed: cross hole moved to 122 mm from the axle's chain-side end, 15 mm off the web, inside the 45 mm hub",
        verdict=WITHIN, closed_by="SDL-DEC-001 F2 (decided under the standing instruction of 2026-10-23)")
c.cited("S26", "The tensioner's pivot fixing clears the chain's upper strand", "Engineering and technology", "Manufacturing tolerances",
        law="Fit check in the detailed model: a head or nut on the boss's outer end sits in the upper strand (7 mm above the pivot) at the real 12 mm chain width",
        detail="Fixed: M8 x 40 screw from inside the frame through the rail into the tensioner's tapped boss",
        verdict=WITHIN, closed_by="SDL-DEC-001 F3 (decided under the standing instruction of 2026-10-23)")
c.claim("S28", "A jammed plate does not damage the steel drive: the wheel drives until it skids (about 11 N m at the plate shaft), and the printed plate's bore strips first",
        "Physics", "Strength of materials", law="Traction about 0.7 of the drive-wheel load at 150 mm; chain tension against 7.8 kN; D-flat bearing stress against about 50 MPa for PETG (independent review of 2026-10-24)",
        value=497.0, limit=780.0, unit="N chain tension (limit 10 % of minimum tensile); the plate's D-flat reaches about 54 MPa, so the plate is the sacrificial part", rule="below", closed_by="SDL-CAL-001 section 7; spare plate in the kit")
c.claim("S29", "The tensioner takes up chain wear until about 0.8 % elongation; the chain is then shortened by a link pair or replaced",
        "Engineering and technology", "Manufacturing tolerances", law="Idler deflection sqrt(slack x C / 2): 35 mm new, 48 mm at 1 % elongation, against 45 mm of take-up (independent review of 2026-10-24)",
        value=45.0, limit=48.0, unit="mm take-up against mm needed at 1 % elongation (the claim is the wear limit)", rule="below", closed_by="SDL-BLD-001 first checks; wear limit in the build plan")
c.claim("S30", "The 20 x 2 mm hopper uprights carry the hopper sideways: they sway 1 mm before the hopper's neck bears in the housing collar, which takes the rest",
        "Physics", "Strength of materials", law="Cantilever deflection F L^3 / 3 E I limited to the collar's 1 mm clearance (SDL-DDR-003 P7); free-standing they would reach about 300 MPa at three times the full hopper's weight sideways (independent review of 2026-10-24)",
        value=10.0, limit=235.0 / 1.5, unit="MPa at 1 mm sway (limit yield / 1.5)", rule="below", closed_by="SDL-CAL-001 section 7")
c.claim("S31", "The aluminium marker arm stays below yield at its full 900 mm reach with a dynamic factor of 3", "Physics", "Strength of materials",
        law="Cantilever bending of 20 x 1.5 tube under 20 N side drag; 6061-T6 tube, typical minimum yield about 240 MPa (6063-T6 about 170 MPa would give a factor of 1.3); independent review of 2026-10-24",
        value=128.0, limit=240.0 / 1.5, unit="MPa (limit is yield / 1.5)", rule="below", closed_by="SDL-CAL-001 section 7; 6061-T6 in the BOM")
c.cited("S27", "The hopper's M5 heat-set inserts fit their bosses", "Engineering and technology", "Standards practice",
        law="Insert makers specify a hole of about 6.4 mm for M5 heat-set inserts; the bosses were drawn with 4.0 mm holes (a tap drill size)",
        detail="Fixed: 6.5 mm holes in the eight bosses", verdict=WITHIN, closed_by="SDL-DEC-001 F4 (decided under the standing instruction of 2026-10-23)")

# ---------------------------------------------------------------------------------------------------------------
# Option B: punch wheel with a hub meter
# ---------------------------------------------------------------------------------------------------------------
R = B["RIM_R"] / 1000
spacing_b = 2 * math.pi * R / B["N_PUNCH"] * 1000
c.order_of_magnitude("OB1", "Option B: six punches on a 480 mm rim give 251 mm spacing", "Mathematics", "Units and dimensional analysis",
                     claimed=251.0, estimate=spacing_b, unit="mm", law="Spacing = 2 pi R / N (rim rolling on the surface; sinkage shortens it)", closed_by="SDL-OPT-001")
# punch penetration: cone index x projected area of the punch at full depth; available force = wheel share of the mass
a_tip = (B["PUNCH_W"] + 12.0) / 2 * 9.0 * 1e-6        # m2, the closed punch's section at mid depth (about 18 x 9 mm)
w_b = 12.4 * G * 0.75
f_tilled = 200e3 * a_tip
f_untilled = 1500e3 * a_tip
c.claim("OB2", f"Option B: the wheel's weight presses a punch 50 mm into tilled soil ({f_tilled:.0f} N needed at a 200 kPa cone index)",
        "Physics", "Mechanics and statics", law="Penetration force about cone index x punch section; wheel share of a 12.4 kg machine about 75 %",
        value=round(f_tilled, 0), limit=round(w_b, 0), unit="N", rule="below", closed_by="SDL-OPT-001")
c.claim("OB3", f"Option B is limited to tilled seedbeds, as option A is: in firm untilled soil (1.5 MPa cone index) a punch needs about {f_untilled:.0f} N, more than the wheel's share plus 100 N of downward push; the crossover is near 1.2 MPa",
        "Physics", "Mechanics and statics", law="As OB2; firm untilled soils reach cone indexes of 1 to 2 MPa (typical range, to confirm with partner data). The claim is the limitation, so the check is that the force needed exceeds the force available",
        value=round(f_untilled, 0), limit=round(w_b + 100.0, 0), unit="N needed against N available", rule="above", closed_by="SDL-OPT-001 (no untilled-soil advantage claimed)")


def seed_arrival(theta_rel_deg, v=V, mu=0.4, r0=0.080, r1=0.236):
    """Seed released into a radial tube at theta_rel on a wheel rolling at v: integrate its slide out along the tube
    (gravity, centrifugal, Coriolis and wall friction) and return the wheel angle when it reaches the jaws."""
    w = v / R
    th = math.radians(theta_rel_deg)
    r, rd, dt = r0, 0.0, 1e-4
    t = 0.0
    while r < r1 and t < 2.0:
        thc = th - w * t
        a_rad = -G * math.sin(thc) + w * w * r                   # gravity component along the tube outward, plus centrifugal
        n = abs(G * math.cos(thc) + 2 * w * rd)                   # wall reaction per unit mass (gravity across the tube, Coriolis)
        a = a_rad - (mu * n if rd > 0 or a_rad > mu * n else a_rad)
        rd = max(0.0, rd + a * dt)
        r += rd * dt
        t += dt
    return math.degrees(th - w * t)


arr = seed_arrival(B["RELEASE"][1])
entry = -90.0 + math.degrees(math.acos((B["RIM_R"]) / (B["RIM_R"] + B["PUNCH_L"])))
c.claim("OB4", f"Option B: a seed released at {B['RELEASE'][1]:.0f} deg reaches the punch's jaws before the jaw opens at the bottom (arrives at {arr:.0f} deg; the punch enters the soil at {entry:.0f} deg; at about 3.3 km/h it arrives after 90 deg)",
        "Physics", "Mechanics and statics", law="Seed sliding out along a rotating tube: gravity, centrifugal and Coriolis terms with wall friction 0.4, at 2.9 km/h",
        value=round(-arr, 0), limit=90.0, unit="deg past forward (the jaw opens near 90)", rule="below", margin=0.25, closed_by="")
v_ring = (V / R) * (sum(B["RING"]) / 2 / 1000)
c.claim("OB5", f"Option B: the hub cell ring's cells move at {v_ring:.2f} m/s, under the 0.30 m/s fill limit assumed for option A", "Physics",
        "Mechanics and statics", law="Cell speed = wheel angular speed x cell radius (69 mm)", value=round(v_ring, 2), limit=0.30, unit="m/s", rule="below", closed_by="SDL-OPT-001")
c.cited("OB6", "Option B: soil pushes the trailing jaw open in the soil and a torsion spring closes it as the punch lifts out", "Physics", "Mechanics and statics",
        law="Punch planters with hinged jaws are established (jab planters; Molin et al. 1998 report a punch planter prototype with synchronisation and soil-sticking problems)",
        detail="Working in principle; jaw opening timing, soil sticking and spring force not calculated", verdict=PLAUSIBLE, closed_by="")

state = c.write()
print("verdict:", state)
for r in c.rows:
    print(f"  {r['id']:4s} {r['verdict']:32s} {r['check']}")
