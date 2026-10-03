"""SeedLine prototype build plan pictures (SDL-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps ...] [only=NNN,...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/SDL-DWG-101 to 124        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import gc
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P, build_components, box, union  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
REV2 = {"107", "111", "112", "113", "114", "115"}      # making sketches revised by the decisions of 2026-10-02
C = build_components()
XM, ZS, YC = P["X_METER"], P["Z_SHAFT"], P["Y_CHAIN"]

COL = {"rail": "#64748B", "cross": "#475569", "clip": "#1D4ED8", "drop": "#0E7490", "bplate": "#0369A1",
       "upright": "#7C3AED", "wheel": "#374151", "lugs": "#B45309", "axle": "#111827", "bearing": "#D4A017",
       "sprocket": "#9A3412", "chain": "#57534E", "tensioner": "#C2410C", "housing": "#0F766E",
       "door": "#93C5FD", "liner": "#C4B5FD", "knob": "#115E59", "plate": "#14B8A6", "brush": "#7C2D12", "hopper": "#CBD5E1",
       "lid": "#94A3B8", "shank": "#6B7280", "boot": "#9CA3AF", "tube": "#0EA5E9", "press": "#1F2937",
       "spacer": "#A8A29E", "cover": "#78716C", "guard": "#F59E0B", "handle": "#115E59", "grip": "#0F172A",
       "marker": "#D97706", "bolt": "#111827"}


def S(*ks):
    """Several components drawn together. A compound, not a fused solid: fusing touching parts
    (lugs on a rim, say) can leave faces that will not tessellate."""
    if len(ks) == 1:
        return C[ks[0]].shape
    import copy
    from build123d import Compound
    return Compound(children=[copy.copy(C[k].shape) for k in ks])


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def side(shape, sgn):
    """The half of a mirrored pair on one side of the row (sgn -1 chain side, +1 door side)."""
    return shape & (box(-3000, 3000, 0, 3000, -3000, 3000) if sgn > 0 else box(-3000, 3000, -3000, 0, -3000, 3000))


def at_origin(shape):
    import build123d as b
    c = shape.bounding_box().center()
    return b.Pos(-c.X, -c.Y, -c.Z) * shape


def flat(shape, origin, x_dir, z_dir):
    import build123d as b
    return b.Plane(origin=origin, x_dir=x_dir, z_dir=z_dir).to_local_coords(shape)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return [
        ("rails", part("Side rails (2)", S("rail_l", "rail_r"), COL["rail"])),
        ("cross", part("Middle and opener cross members", S("cross_mid", "opener_bar"), COL["cross"])),
        ("clips", part("Corner clips (4)", S("clips"), COL["clip"])),
        ("dropf", part("Front drop plates (2)", S("drop_front"), COL["drop"])),
        ("wheel", part("Drive wheel and lugs", S("wheel", "lugs"), COL["wheel"])),
        ("axle", part("Drive axle, bearings, spacers", S("axle", "axle_bearings", "axle_spacers"), COL["bearing"])),
        ("housing", part("Metering housing", S("housing"), COL["housing"])),
        ("bplate", part("Bearing plate", S("bplate"), COL["bplate"])),
        ("shaft", part("Plate shaft, bearings, collar", S("shaft", "shaft_bearings", "collar"), COL["bearing"])),
        ("sprockets", part("Sprockets (2)", S("sprocket_wheel", "sprocket_plate"), COL["sprocket"])),
        ("chain", part("Chain and spring tensioner", S("chain", "tensioner"), COL["tensioner"])),
        ("plate", part("Seed plate and knob", S("plate", "knob"), COL["plate"])),
        ("door", part("Housing door and plate liners", S("door", "liner_chain", "liner_door"), COL["door"])),
        ("brush", part("Singulator brush", S("brush"), COL["brush"])),
        ("uprights", part("Hopper uprights (4)", S("uprights"), COL["upright"])),
        ("hopper", part("Hopper and lid", S("hopper", "lid"), COL["hopper"])),
        ("opener", part("Opener shank and boot", S("shank", "boot"), COL["shank"])),
        ("tube", part("Seed drop tube", S("drop_tube"), COL["tube"])),
        ("cover", part("Covering chains and bracket", S("chain_bracket", "cover_chains"), COL["cover"])),
        ("dropr", part("Rear drop plates (2)", S("drop_rear"), COL["drop"])),
        ("press", part("Press wheel, axle, spacers", S("press", "press_axle", "press_spacers"), COL["press"])),
        ("guard", part("Chain guard and spacers", S("guard", "guard_spacers"), COL["guard"])),
        ("handle", part("Handle: tubes, sleeves, brace, grip", S("handle_lower", "handle_upper", "sleeves", "brace", "grip"), COL["handle"])),
        ("marker", part("Row marker kit (option)", S("marker_mount", "marker_arm", "marker_disc"), COL["marker"])),
    ]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"rails": (0, 0, 0), "cross": (0, 0, 160), "clips": (0, 0, 280), "dropf": (120, 0, -260),
           "wheel": (420, 0, -60), "axle": (420, 0, -380), "housing": (0, 320, 120), "bplate": (150, -260, -40),
           "shaft": (220, -420, 140), "sprockets": (420, -560, -120), "chain": (380, -760, -200), "plate": (0, 500, 140),
           "door": (0, 660, 140), "brush": (-480, 380, 300), "uprights": (0, 0, 430), "hopper": (0, 0, 760),
           "opener": (200, 0, -440), "tube": (0, 360, -330), "dropr": (-260, 0, -200), "press": (-480, 0, -400),
           "cover": (-300, 0, -640), "guard": (300, -980, 320), "handle": (-420, 0, 200), "marker": (700, 150, 520)}
    parts = []
    for k, p in M:
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "SeedLine prototype: every component, pulled apart",
                       subtitle="Numbered in build order; 24 is the row marker kit. Seen from the front, chain side, and above",
                       elev=24, azim=-58, size=(12, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    base = dict(project="SeedLine", date=DATE)
    out = []
    ctx_frame = [part("rails", S("rail_l", "rail_r"), "#999")]

    def sheet(no, name, shape, neighbours, title, material, notes, view_shape=None, inset_view=(24, -130)):
        if only and no not in only:
            return
        rv = {}
        if no in REV2:
            rv = dict(rev="P2", revisions=[("P1", "Making sketch for the prototype build plan", "2026-10-01", "AC"),
                                           ("P2", "SDL-DEC-001: 13 mm slot, plate liners, UV-stabilized door", "2026-10-02", "AC")])
        out.append(bv.component_sheet(Part(name, shape, COL.get("rail")), neighbours, dwg_no=f"SDL-DWG-{no}", **rv,
                                      title=f"SeedLine {title}: making sketch", material=material, notes=notes,
                                      view_shape=at_origin(view_shape if view_shape is not None else shape),
                                      inset_view=inset_view, **base))
        gc.collect()

    def nb(*ks):
        return [part(k, S(k), "#999") for k in ks]

    sheet("101", "Side rail", C["rail_l"].shape, nb("rail_r", "cross_mid", "opener_bar", "drop_front", "drop_rear", "bplate"),
          "side rail (make 2: a chain-side and a door-side)", "Steel square tube 25 x 25 x 1.5 mm, S235 class",
          ["Cut two 700 mm lengths of 25 x 25 x 1.5 tube; square and deburr the ends.",
           "Every hole goes through both side walls, square to the side faces, on",
           "  the centre line of the side face; distances from the front end.",
           "Both rails, 6.5 mm: 68 and 92 (front drop plate), 276 (front upright",
           "  and clip), 425 (rear upright), 507.5 (middle clip), 645 and 675",
           "  (rear drop plate). Clamp the pair together and drill these at once.",
           "Chain-side rail only: 6.5 mm at 12 and 40 (marker kit), 315 and 385",
           "  (bearing plate and housing lugs), 350 at 6 mm above the centre line",
           "  (lower bearing bolt); 8.5 mm at 220 (tensioner pivot).",
           "Deburr inside each hole so the bolts pass freely; do not crush the tube:",
           "  bolts through it are tightened snug, not hard.",
           "Check: lay the drop plates, clips and bearing plate on the rail and look",
           "  through each hole."],
          view_shape=C["rail_l"].shape)

    xu_f, xu_r = P["OPENER_BAR_X"] - 25.0, XM - 75.0
    sheet("102", "Middle cross member", C["cross_mid"].shape, nb("rail_l", "rail_r", "clips", "chain_bracket"),
          "middle cross member", "Steel square tube 25 x 25 x 1.5 mm, S235 class",
          ["Cut one 95 mm length of 25 x 25 x 1.5 tube; the ends must be square,",
           "  since they butt against the inside faces of the rails.",
           "Four 6.5 mm holes front to back through both walls, on the centre",
           "  line of the side face, at 12.5, 37.5, 57.5 and 82.5 mm from one end.",
           "  The outer two take the corner clips, the inner two the chain bracket.",
           "Fit: between the rails, 400 mm behind the drive axle (480 mm from the",
           "  front end of the rails), held by two corner clips on its rear face.",
           "Check: it fits between the rails with no gap and no forcing."])
    sheet("103", "Opener cross member", C["opener_bar"].shape, nb("rail_l", "rail_r", "clips", "shank", "wheel"),
          "opener cross member", "Steel rectangular tube 40 x 20 x 1.5 mm, S235 class",
          ["Cut one 95 mm length of 40 x 20 x 1.5 tube; square ends. It stands",
           "  40 mm tall, 20 mm front to back.",
           "Four 6.5 mm holes front to back through both 40 mm faces:",
           "  clip holes 12.5 mm from each end, 12.5 mm up from the bottom;",
           "  shank holes at mid-length (47.5 mm), 10 and 30 mm up from the bottom.",
           "Fit: between the rails, its bottom flush with the rail bottoms and its",
           "  front face 161 mm behind the drive axle (241 mm from the rail front),",
           "  held by two corner clips on its rear face. It carries the opener",
           "  shank on its rear face; the drive wheel lugs pass 19 mm in front.",
           "Check: square to the rails; the top stands 15 mm above the rails."])
    clip1 = C["clips"].shape & box(-215, -175, 0, 60, 190, 240)
    sheet("104", "Corner clip", clip1, nb("rail_r", "opener_bar", "uprights"),
          "corner clip (make 4)", "Steel equal angle 25 x 25 x 3 mm",
          ["Cut four 25 mm lengths of 25 x 25 x 3 angle; deburr.",
           "Rail leg: one 6.5 mm hole 10 mm from the leg's free end and",
           "  12.5 mm up (centred on the 25 mm length).",
           "Cross member leg: one 6.5 mm hole 12.5 mm from its free end, 12.5 up.",
           "The four clips are the same; a left one is a right one turned over.",
           "Fit: one leg flat on the inside face of a rail, the other flat on the",
           "  rear face of a cross member, heel in the corner. The rail-leg bolt",
           "  also holds a hopper upright (opener clips) or goes alone (middle).",
           "Check: both legs sit flat with the cross member square to the rail."], inset_view=(30, 60))
    dropf = side(C["drop_front"].shape, -1)
    sheet("105", "Front drop plate", dropf, nb("rail_l", "axle_bearings", "axle", "wheel", "guard_spacers"),
          "front drop plate (make 2)", "Steel plate 4 mm, S235 class",
          ["Cut two 50 x 117.5 mm blanks of 4 mm plate; round the corners 3 mm.",
           "Measure down from the top edge and sideways from the centre line:",
           "  rail bolts 6.5 mm at 12.5 down, 12 each side of centre;",
           "  axle hole 20 mm at 77.5 down, centred;",
           "  bearing bolts 6.5 mm at 49.5 and 105.5 down, centred.",
           "Chain-side plate only: drill 4.2 mm and tap M5 at 107 down, 17 mm",
           "  forward of centre, for the guard spacer screw.",
           "Drill the pair clamped together for the shared holes.",
           "Fit: on the outside face of each rail, top edge flush with the rail top,",
           "  centred on the drive axle 80 mm behind the rail front; the axle",
           "  bearing bolts flat to its inside face.",
           "Check: the axle hole lines up across both plates (sight through)."])
    dropr = side(C["drop_rear"].shape, 1)
    sheet("106", "Rear drop plate", dropr, nb("rail_r", "press_axle", "press_spacers", "handle_lower"),
          "rear drop plate (make 2)", "Steel plate 4 mm, S235 class",
          ["Cut two 50 x 147.5 mm blanks of 4 mm plate; round the corners 3 mm.",
           "Measure down from the top edge and sideways from the centre line:",
           "  rail bolts 6.5 mm at 12.5 down, 15 each side of centre;",
           "  press axle hole 16.5 mm at 127.5 down, centred;",
           "  handle bolts 8.5 mm at 32.4 down, 13.3 to the rear of centre,",
           "  and at 50.8 down, 2.1 forward of centre.",
           "Drill the pair clamped together.",
           "Fit: on the outside face of each rail, top edge flush with the rail top,",
           "  centred 660 mm behind the rail front. The flattened lower end of a",
           "  handle tube bolts flat to its outside face.",
           "Check: the axle hole lines up across both plates."])
    sheet("107", "Bearing plate", C["bplate"].shape, nb("rail_l", "shaft_bearings", "shaft", "housing"),
          "bearing plate", "Steel plate 4 mm, S235 class",
          ["Cut one 90 x 87.5 mm blank of 4 mm plate; round the corners 3 mm.",
           "Measure up from the bottom edge and sideways from the centre line:",
           "  rail and housing bolts 6.5 mm at 12.5 up, 35 each side;",
           "  shaft clearance hole 16 mm at 42.5 up, centred;",
           "  outboard bearing bolts 6.5 mm on the centre line, 18.5 and 66.5 up;",
           "  inboard bearing bolts 6.5 mm at 42.5 up, 24 each side.",
           "Drill 4.2 mm and tap M5 at 30.9 up, 31.9 to the rear of centre",
           "  (guard spacer screw).",
           "Measure your two bearings first: move the bolt holes to suit them.",
           "Fit: on the outside face of the chain-side rail, bottom edge flush with",
           "  the rail bottom, centred 350 mm behind the rail front; one bearing",
           "  on each face, the inboard one clear of the rail top by 2.5 mm.",
           "Check: the shaft hole is square to the plate; bearing bolts line up."])
    up1 = C["uprights"].shape & box(xu_r - 15, xu_r + 15, 0, 100, 0, 600)
    sheet("108", "Hopper upright", up1, nb("rail_r", "hopper", "clips"),
          "hopper upright (make 4)", "Steel flat bar 20 x 3 mm",
          ["Cut four 302.5 mm lengths of 20 x 3 flat bar; round the top corners.",
           "On the centre line, from the bottom end: 6.5 mm at 12.5 (rail bolt);",
           "  5.5 mm at 237.5 and 287.5 (hopper screws).",
           "Drill all four clamped together so the hopper holes match.",
           "Fit: flat on the outside face of a rail, bottom end flush with the",
           "  rail bottom, at 276 mm (front pair) and 425 mm (rear pair) from",
           "  the rail front. The front bolt also passes the corner clip inside.",
           "  The hopper's side bosses sit flat on the uprights' inside faces.",
           "Check: each upright stands square to the rail (use a square)."])
    lug1 = C["lugs"].shape & box(125, 160, -40, 40, 135, 165)
    sheet("109", "Wheel lug", lug1, nb("wheel"),
          "wheel lug (make 18)", "Steel strip 25 x 3 mm, bent",
          ["Cut eighteen 45 mm lengths of 25 x 3 strip.",
           "Bend each along its length into an L: a 15 mm foot and a 10 mm",
           "  upstand (inside sizes). A vice and a hammer will do.",
           "Two 5.5 mm holes in the foot, 10 mm from each end, countersunk",
           "  on the outside for M5 countersunk screws.",
           "Fit: the foot lies flat across the 45 mm rim, upstand outward at the",
           "  trailing edge, spaced every 20 degrees (about 49 mm round the rim).",
           "  Mark the rim through the lug, drill 5.5 mm, fit the screws with the",
           "  nuts inside the rim and threadlocker. Round the upstand corners.",
           "Lug tips sit on a 300 mm circle: this sets the spacing (942.5 mm",
           "  per wheel turn).",
           "Check: measure across opposite lug tips: 300 mm, within 2 mm."], inset_view=(20, -60))
    sheet("110", "Drive axle", C["axle"].shape, nb("axle_bearings", "axle_spacers", "drop_front", "sprocket_wheel"),
          "drive axle and spacers", "Bright steel round bar 16 mm (or 5/8 in); tube 21 x 2.5 mm",
          ["Cut a 177 mm length of 16 mm bright bar; chamfer both ends 1 mm.",
           "From the chain-side end: file a 1 mm flat 0 to 12 mm (sprocket set",
           "  screw), 34.5 to 46.5 mm and 165 to 177 mm (bearing set screws).",
           "Drill a 6.5 mm cross hole at 107 mm, through the centre: this takes",
           "  the M6 bolt that fixes the wheel hub to the axle. Drill it with the",
           "  hub fitted, so the holes line up.",
           "Spacers: two 38 mm lengths of 21 x 2.5 mm tube (16 mm bore), ends",
           "  square; one each side of the hub, out to the bearings.",
           "Fit: the axle turns in the two flange bearings inside the drop plates",
           "  and carries the wheel and the wheel sprocket with it.",
           "Check: the axle turns freely by hand in both bearings."], inset_view=(25, 30))
    sheet("111", "Plate shaft", C["shaft"].shape, nb("shaft_bearings", "bplate", "collar", "plate", "sprocket_plate"),
          "plate shaft", "Bright steel round bar 12 mm",
          ["Cut a 110 mm length of 12 mm bright bar; chamfer the ends 0.5 mm.",
           "From the chain-side end: file 1 mm flats 0 to 12 mm (sprocket) and",
           "  at each bearing (16 to 28 mm and 34 to 46 mm).",
           "File a D-flat 1.4 mm deep over the last 25 mm (85 to 110 mm): the",
           "  collar set screw, the plate's hub and the plate sit on it.",
           "Drill 5.0 mm, 18 deep, in the plate end and tap M6, 15 deep, for",
           "  the plate knob. Centre it in a vice V-block under a drill stand.",
           "Fit: held from the chain side only, in two bearings on the bearing",
           "  plate; its plate end stops level with the plate's door-side face.",
           "Check: a seed plate slides on and off the D-flat by hand."], inset_view=(25, 30))
    sheet("112", "Metering housing", C["housing"].shape, nb("rail_l", "bplate", "hopper", "plate", "door", "shank"),
          "metering housing", "PETG, 3D printed, 4 walls, 40 % infill",
          ["Body 146 long x 25 wide x 165 tall; a 13 mm slot inside holds a 6,",
           "  8 or 10 mm plate with its liners; front wall 3 mm, others 6 mm.",
           "On top: a collar 80 x 48 x 20 with a 68 x 38 pocket, 10 deep, and a",
           "  funnel from 60 x 30 down to the 60 x 13 slot. The hopper neck drops in.",
           "Chain side: a 22 mm hole for the plate hub; two lugs 20 x 37 x 25 with",
           "  6.5 mm holes and an M6 nut slot, 35 mm each side of the shaft.",
           "Door side: an opening 128 x 132; two M4 heat-set inserts for the door.",
           "Rear wall: a 13 x 10 slot 35 to 45 mm above the shaft for the brush.",
           "Chain-side slot wall: two 3.4 mm peg holes, 5 deep, 48 mm each side of the shaft.",
           "Under the outlet: a spigot 16 mm outside, 12 mm bore, 60 long.",
           "Print standing on its bottom face; support the lugs and collar.",
           "Fit: lugs on the chain-side rail's inside face, on the bearing plate",
           "  bolts; the plate turns in the slot without touching.",
           "Check: a 6 mm plate with both liners turns in the slot, door on."], inset_view=(20, -60))
    import build123d as _b
    _pl = lambda sh, dx: _b.Pos(dx, 0, 0) * sh  # noqa: E731
    _lc, _ld = C["liner_chain"].shape, C["liner_door"].shape
    sheet("113", "Door, liners and knob", S("door", "knob", "liner_chain", "liner_door"), nb("housing", "plate", "door_screws"),
          "housing door, plate liners and plate knob", "UV-stabilized clear polycarbonate sheet 3 mm; liners and knob PETG printed",
          ["Door: cut 136 x 140 mm from 3 mm UV-stabilized clear polycarbonate (score and snap,",
           "  or a fine saw); round the corners 5 mm; keep the film on to drill.",
           "  13 mm hole for the knob stem, 70 mm from the rear edge, 70 mm up.",
           "  4.5 mm holes for the thumb screws: 12 from the rear edge 125 up,",
           "  and 124 from the rear edge 15 up.",
           "Knob: print a 28 mm head, 10 thick, on a 12 mm stem 10.5 long; press",
           "  an M6 x 25 screw through its centre as a stud (head moulded in).",
           "Fit: the door covers the opening on the housing's door side with two",
           "  M4 thumb screws; the knob stem passes the door and screws into the",
           "  shaft end, clamping the plate against the shaft collar.",
           "Liners: two discs 122 mm across, 2 mm thick, with a 22 mm hole and a notch",
           "  16 mm tall at the brush. Chain side: two 3 mm pegs 4 long, 48 mm each",
           "  side of centre. Door side: two 5 mm pegs, 6 long, that rest on the door.",
           "  For an 8 mm plate the chain-side liner is 1 mm; a 10 mm plate has none.",
           "Check: door off and knob out in under a minute, no tools."],
          view_shape=_b.Compound(children=[S("door", "knob"), _pl(_lc, -170.0), _pl(_ld, 170.0)]), inset_view=(20, 50))
    sheet("114", "Seed plate", C["plate"].shape, nb("housing", "shaft", "collar"),
          "seed plate (maize, 4 cells)", "PETG, 3D printed (ASA in strong sun)",
          ["Disc 120 mm across, 6 mm thick, with a hub 20 mm across, 11 mm long,",
           "  on its chain-side face (14 mm from the centre plane, so a thicker plate",
           "  has a shorter hub). Bore 12.4 mm with a flat 4.6 mm from centre.",
           "Maize plate: 4 cells in the rim, 14.3 mm long, 8.7 mm deep, through",
           "  the thickness. Other crops: cells from the rule in the model (seed",
           "  length x 1.15 + 0.5, width x 1.05 + 0.3; thickness at least 6).",
           "Print flat, hub up, no supports: about 44 g and 1.5 h in PETG.",
           "Mark the crop and cell count on the face (raised text).",
           "Fit: slides onto the shaft's D-flat until the hub meets the collar; the",
           "  hub runs in the housing's 22 mm hole; the knob holds it.",
           "Check: a kernel sits in each cell level with the rim, not proud of it."], view_shape=make_plate_local(), inset_view=(20, 50))
    sheet("115", "Hopper and lid", S("hopper", "lid"), nb("uprights", "housing"),
          "seed hopper and lid", "PETG, 3D printed, 3 mm walls (lid 2 mm)",
          ["Box 170 x 120 x 100 on a funnel 60 tall down to a 66 x 36 neck,",
           "  12 tall, 3 mm walls throughout; 2.42 L inside.",
           "Four bosses on each long side face, 20 x 12.5 x 20, at 100 and 150",
           "  mm above the neck bottom, 74 mm ahead and 75 mm behind the centre,",
           "  with 4 mm holes for M5 heat-set inserts pressed in with a soldering iron.",
           "Lid: 174 x 124 x 2 with a 6 mm skirt that drops inside the rim.",
           "Print the hopper upside down on its rim, the lid flat.",
           "Fit: the neck drops into the housing collar with 1 mm all round and",
           "  rests on the funnel shoulder; the bosses sit flat on the uprights,",
           "  two M5 screws each.",
           "Check: fill with water to the rim: no leaks; 2.4 L."], inset_view=(20, -60))
    sheet("116", "Chain guard", C["guard"].shape, nb("drop_front", "bplate", "sprocket_wheel", "sprocket_plate", "chain", "guard_spacers"),
          "chain guard", "PETG, 3D printed (amber), about 180 g",
          ["A shroud: a 3 mm band 26 mm deep round the outline in the front view,",
           "  closed on the outside by a 2 mm face; open on the frame side.",
           "The outline clears both sprockets by 17 mm and the tensioner over",
           "  its full 45 mm of travel. 362 mm long, 192 mm tall.",
           "Two 4.5 mm holes in the face: 17 mm ahead of and 29 mm below the",
           "  drive axle; 32 mm behind and 12 mm below the plate shaft.",
           "Print face down, no supports; split in two at mid-length and glue",
           "  if your printer bed is under 370 mm.",
           "Spacers: 8 mm tube, 38.5 mm (drive end) and 39.5 mm (plate end).",
           "Fit: two M5 x 50 screws through the face and spacers into the tapped",
           "  holes in the drop plate and bearing plate.",
           "Check: turn the wheel: nothing touches the guard."], inset_view=(15, -100))
    sheet("117", "Opener shank", C["shank"].shape, nb("opener_bar", "boot", "wheel"),
          "opener shank", "Steel flat bar 20 x 12 mm, S235 class",
          ["Cut 305 mm of 20 x 12 flat bar. The 12 mm faces are front and back.",
           "Grind a 45 degree chamfer, 8 mm, on the front bottom corner: the nose.",
           "Front face: eight holes, drill 5.0 and tap M6, 15 mm deep, centred, at",
           "  222.5 to 292.5 mm from the bottom, every 10 mm (depth settings).",
           "Two 6.5 mm holes across, 8 mm from the rear face, 15 and 40 mm",
           "  from the bottom, for the boot plates.",
           "Fit: front face flat on the rear of the opener cross member, two M6",
           "  bolts from the front into two tapped holes 20 mm apart. Using the",
           "  lowest pair gives 60 mm depth; each pair up is 10 mm shallower.",
           "Check: the shank hangs square to the frame; the nose points forward."], inset_view=(20, -60))
    sheet("118", "Boot side plate", side(C["boot"].shape, 1), nb("shank", "drop_tube"),
          "boot side plate (make 2)", "Steel plate 3 mm, S235 class",
          ["Cut two 82 x 80 mm blanks of 3 mm plate; break the edges.",
           "6.5 mm holes, measured from the front edge and up from the bottom:",
           "  8 from the front, 15 and 40 up (shank bolts);",
           "  7 from the rear edge, 65 up (rear spacer).",
           "Two 4 mm holes 3 mm below the top edge, 45 and 60 from the front,",
           "  for the cable tie that holds the drop tube.",
           "Fit: one each side of the shank's lower end, front edges 4 mm behind",
           "  the shank front; a 12 mm spacer and M6 bolt at the rear keep them",
           "  12 mm apart. Seed falls between them into the furrow.",
           "Check: the bottom edges are level with the shank bottom."], inset_view=(20, -60))
    sheet("119", "Covering chain bracket", C["chain_bracket"].shape, nb("cross_mid", "cover_chains", "clips"),
          "covering chain bracket", "Steel equal angle 25 x 25 x 3 mm",
          ["Cut 40 mm of 25 x 25 x 3 angle.",
           "Upright leg: two 6.5 mm holes 10 mm each side of centre, 12.5 up.",
           "Flat leg: two 6 mm holes 15 mm from the heel, 14 mm each side of",
           "  centre, for the chain end links (M5 bolt or shackle each).",
           "Fit: upright leg flat on the rear face of the middle cross member,",
           "  flat leg at the bottom pointing rearward; two M6 bolts.",
           "Hang the two 250 mm chains; they drag on the soil behind the opener",
           "  and clear the press wheel by at least 15 mm.",
           "Check: the chains hang free and swing without catching."], inset_view=(25, 150))
    # handle side tubes and sleeve, one side, laid flat
    (hbx, hbz), (gx, gz) = model.handle_points()
    yb = model.frame_y()["handle_base"]
    import build123d as b
    a0 = b.Vector(hbx, yb, hbz); g = b.Vector(gx, P["GRIP_Y"], gz)
    d = (g - a0).normalized(); n = b.Vector(0, 1, 0).cross(d).normalized()
    hs = side(S("handle_lower", "handle_upper", "sleeves"), 1)
    L = model.handle_geometry()["side"]
    sheet("120", "Handle side tubes", hs, nb("drop_rear", "grip", "brace"),
          "handle side tubes and sleeve (one side; make 2 sets)", "Steel round tube 22 x 1.2 mm; sleeve 25 x 1.2 mm",
          [f"Lower tube: cut 560 mm of 22 x 1.2 tube. Flatten the bottom 60 mm",
           "  in a vice to about 5 mm thick, off-centre so one face stays in line",
           "  with the tube wall; drill two 8.5 mm holes 26 and 50 mm from the",
           "  bottom end. Set the flat about 10 degrees to the tube (the splay).",
           "Upper tube: cut 490 mm. Flatten the top 40 mm, drill 6.5 mm 20 mm",
           "  from the end, at right angles to the flat.",
           "Sleeve: 250 mm of 25 x 1.2 tube (22.6 mm bore). Pin holes 6.5 mm:",
           "  through sleeve and lower tube once; in the upper tube every 25 mm",
           "  over 250 mm, for 850 to 1,050 mm grip height.",
           "Fit: the lower flat on the rear drop plate's outside face, two M8 bolts.",
           "Check: the upper tube slides in the sleeve by hand; pins go in freely."],
          view_shape=flat(hs, tuple(a0), tuple(n), tuple(d)), inset_view=(20, -150))
    sheet("121", "Cross grip", C["grip"].shape, nb("handle_upper"),
          "cross grip", "Steel round tube 22 x 1.2 mm; rubber grips",
          ["Cut 594 mm of 22 x 1.2 tube; deburr; fit end plugs.",
           "Two 6.5 mm holes square through the tube, 45 mm from each end, both",
           "  in the same plane.",
           "Push a 110 mm rubber grip on from each end to 22 mm inside each hole",
           "  (soapy water helps); the hands hold just inside the side tubes.",
           "Fit: across the back of the flattened tops of the upper tubes, one M6",
           "  bolt each through the flat and the grip.",
           "Check: grip level when the seeder stands on both wheels."], inset_view=(20, -150))
    sheet("122", "Handle brace", C["brace"].shape, nb("handle_lower"),
          "handle brace", "Steel round tube 18 x 1.5 mm",
          ["Cut 275 mm of 18 x 1.5 tube.",
           "Flatten 13 mm at each end and set each flat to lie on the front of a",
           "  side tube (about 10 degrees); length between the flats 249 mm.",
           "Drill 6.5 mm through each flat.",
           "Fit: across the front of the two lower tubes, about 30 % of the way",
           "  up from the drop plates; drill each lower tube through the flat and",
           "  bolt with an M6 bolt and nyloc nut.",
           "Check: the side tubes stay parallel to the grip ends with the brace on."], inset_view=(20, -150))
    sheet("123", "Marker mount", C["marker_mount"].shape, nb("rail_l", "drop_front", "marker_arm"),
          "row marker mount (row-spacing kit)", "Steel strip 40 x 3 mm, bent",
          ["Cut 100 mm of 40 x 3 strip. Bend 25 mm at each end to 90 degrees,",
           "  same way, to make a U: base 50 mm, two lugs 25 mm.",
           "Base: two 6.5 mm holes, 10 and 38 mm from the rear end, centred.",
           "Lugs: one 8 mm hole each, 15 mm from the base face, centred.",
           "Fit: base flat on the outside of the chain-side rail at its front end,",
           "  lugs pointing outward; two M6 bolts through the rail.",
           "The arm pivots on an M8 pin through both lugs with a 12 mm spacer",
           "  each side of the arm; it folds up and is held by a spring clip.",
           "Check: the arm swings up and down freely and stops level."], inset_view=(20, -60))
    import build123d as b2
    ma = S("marker_arm", "marker_disc")
    piv = b2.Vector(55.0, -P["RAIL_Y"] - 12.5 - 18.0, P["RAIL_Z"])
    end = b2.Vector(55.0, -P["ROW_SPACING"] + 22.0, P["MARKER_D"] / 2 + 4.0)
    da = (end - piv).normalized()
    sheet("124", "Marker arm and disc", ma, nb("marker_mount", "rail_l"),
          "row marker arm and disc (row-spacing kit)", "Steel tube 20 x 1.2 and 16 x 1.2 mm; disc 2 mm plate",
          ["Outer arm: 380 mm of 20 x 1.2 tube; 8 mm cross hole 10 mm from one",
           "  end (pivot); 6.5 mm pin holes every 50 mm along the last 250 mm.",
           "Inner arm: 360 mm of 16 x 1.2 tube; 6.5 mm hole near one end; slides",
           "  in the outer arm for 200 to 900 mm reach; one pin sets it.",
           "Disc: cut a 140 mm disc from 2 mm plate, 16.5 mm centre hole; bolt it",
           "  to a hub of 28 mm bar 28 long, bored 16 mm, which takes the inner",
           "  arm's end and turns on an M8 bolt.",
           "Set the reach so the disc runs at the next row's centre (750 mm for",
           "  maize), measured from the row being sown.",
           "Check: disc runs true; the marked line is within 25 mm of the set row."],
          view_shape=flat(ma, tuple(piv), tuple(da), (1, 0, 0)), inset_view=(30, -60))
    return out


def make_plate_local():
    return model.make_plate()


# ----------------------------------------------------------------- joints
def win(sh, x0, x1, y0, y1, z0, z1):
    b_ = box(x0, x1, y0, y1, z0, z1)
    try:
        r = sh & b_
        if r is not None and r.volume > 1e-6:
            return r
    except Exception:
        pass
    pieces = []
    for so in sh.solids():          # fall back to solid by solid when a fused shape will not cut
        try:
            q = so & b_
            if q is not None and q.volume > 1e-6:
                pieces.append(q)
        except Exception:
            pass
    return union(pieces)


def joints(only=None):
    out = []
    xo = P["OPENER_BAR_X"]

    def j(n, items, box_, title, sub, elev, azim, size=(8, 6)):
        if only and f"{n:02d}" not in only:
            return
        parts = [part(name, win(S(*ks) if isinstance(ks, tuple) else ks, *box_), col) for name, ks, col in items]
        out.append(bv.joint(parts, OUT / f"joint-{n:02d}.png", f"Joint {n}: {title}", subtitle=sub, elev=elev, azim=azim, size=size))
        gc.collect()

    j(1, [("Side rail (door side)", ("rail_r",), COL["rail"]), ("Opener cross member", ("opener_bar",), COL["cross"]),
          ("Corner clip", ("clips",), COL["clip"]), ("Hopper upright, outside the rail", ("uprights",), COL["upright"]),
          ("M6 bolts and nuts", ("frame_bolts",), COL["bolt"])],
      (-215, -165, 15, 80, 195, 250), "corner clip at the opener cross member (door side)",
      "Seen from behind, inside and above. One bolt holds upright, rail and clip; one holds clip and cross member", 48, -125)
    j(2, [("Front drop plate", ("drop_front",), COL["drop"]), ("Side rail", ("rail_l",), COL["rail"]),
          ("Flange bearing, inside the plate", ("axle_bearings",), COL["bearing"]), ("Drive axle", ("axle",), COL["axle"]),
          ("Spacer", ("axle_spacers",), COL["spacer"]), ("Wheel hub", ("wheel",), COL["wheel"]),
          ("Wheel sprocket, outside", ("sprocket_wheel",), COL["sprocket"])],
      (0, 40, -112, 0, 100, 232), "drive axle at the chain-side drop plate (cut on the axle centre)",
      "Seen from the front. The axle turns in the bearing and carries the wheel hub and the sprocket", 15, -25)
    j(3, [("Bearing plate", ("bplate",), COL["bplate"]), ("Side rail", ("rail_l",), COL["rail"]),
          ("Two flange bearings, one each face", ("shaft_bearings",), COL["bearing"]), ("Plate shaft", ("shaft",), COL["axle"]),
          ("Housing lug", ("housing",), COL["housing"]), ("Plate sprocket", ("sprocket_plate",), COL["sprocket"]),
          ("Bolts", ("housing_bolts",), COL["bolt"])],
      (XM, XM + 60, -112, -10, 196, 300), "plate shaft bearings on the bearing plate (cut on the shaft centre)",
      "Seen from the front. The housing lug shares the bearing plate's bolt through the rail", 18, -30)
    j(4, [("Metering housing", ("housing",), COL["housing"]), ("Seed plate and its hub", ("plate",), COL["plate"]),
          ("Plate shaft", ("shaft",), COL["axle"]), ("Shaft collar", ("collar",), COL["bearing"]),
          ("Plate knob", ("knob",), COL["knob"]), ("Door", ("door",), COL["door"]),
          ("Plate liners (2)", ("liner_chain", "liner_door"), COL["liner"])],
      (XM - 60, XM, -30, 30, ZS - 35, ZS + 35), "seed plate on the shaft (housing cut on the shaft centre)",
      "Seen from the front. The collar and the knob clamp the plate; its hub runs in the housing wall; a liner lies each side of the plate", 8, -20)
    j(5, [("Housing collar", ("housing",), COL["housing"]), ("Hopper neck", ("hopper",), COL["hopper"])],
      (XM - 60, XM + 60, -40, 0, 300, 390), "hopper neck in the housing collar (cut on the row centre)",
      "Seen from the door side. The neck drops into the pocket and rests on the funnel shoulder", 15, 90)
    xu_r = XM - 75.0
    j(6, [("Hopper boss", ("hopper",), COL["hopper"]), ("Upright", ("uprights",), COL["upright"]),
          ("M5 screws into inserts", ("hopper_screws",), COL["bolt"])],
      (xu_r - 25, xu_r + 25, 40, 90, 410, 505), "hopper boss on a rear upright (door side)",
      "Seen from outside and above. Two M5 screws through the upright into heat-set inserts", 20, 55)
    j(7, [("Opener cross member", ("opener_bar",), COL["cross"]), ("Shank", ("shank",), COL["shank"]),
          ("Boot side plates", ("boot",), COL["boot"]), ("Bolts and rear spacer", ("opener_bolts",), COL["bolt"]),
          ("Seed drop tube (lower end)", ("drop_tube",), COL["tube"])],
      (-280, -150, -30, 30, -55, 260), "opener shank on the opener cross member",
      "Seen from the door side. Two M6 bolts from the front into tapped holes in the shank set the depth", 12, 70, size=(8, 7))
    j(8, [("Chain-side rail", ("rail_l",), COL["rail"]), ("Spring tensioner and idler", ("tensioner",), COL["tensioner"]),
          ("Chain", ("chain",), COL["chain"]), ("Wheel sprocket", ("sprocket_wheel",), COL["sprocket"])],
      (-230, 40, -115, -60, 100, 260), "spring tensioner on the slack (lower) strand, guard off",
      "Seen from the chain side. The pivot bolts through the rail; the idler presses the lower strand down", 8, -90)
    j(9, [("Chain guard (part)", ("guard",), COL["guard"]), ("Spacer and M5 screw", ("guard_spacers",), COL["bolt"]),
          ("Bearing plate", ("bplate",), COL["bplate"]), ("Outboard bearing", ("shaft_bearings",), COL["bearing"]),
          ("Plate sprocket", ("sprocket_plate",), COL["sprocket"])],
      (-330, -240, -125, -70, 205, 262), "chain guard fixing at the plate end (a piece of the guard shown)",
      "Seen from the chain side, behind. An M5 screw runs through the guard face and a spacer into the tapped bearing plate", 20, -130)
    j(10, [("Rear drop plate", ("drop_rear",), COL["drop"]), ("Side rail", ("rail_r",), COL["rail"]),
           ("Handle lower tube, flattened end", ("handle_lower",), COL["handle"]), ("M8 bolts", ("handle_bolts",), COL["bolt"]),
           ("Press axle and nut", ("press_axle",), COL["axle"]), ("Spacer", ("press_spacers",), COL["spacer"]),
           ("Press wheel", ("press",), COL["press"])],
      (-640, -540, 20, 110, 60, 240), "handle and press axle on the rear drop plate (door side)",
      "Seen from outside, behind. The clamped axle and spacers also tie the two rails together", 15, 140)
    (hbx, hbz), (gx, gz) = model.handle_points()
    gy = P["GRIP_Y"]
    j(11, [("Upper tube, flattened top", ("handle_upper",), COL["handle"]), ("Cross grip", ("grip",), COL["grip"])],
      (gx - 70, gx + 50, gy - 60, gy + 60, gz - 70, gz + 50), "upper tube to the cross grip (door side)",
      "Seen from behind the seeder. One M6 bolt through the flat and the grip", 20, -160)
    import build123d as b3
    ro = P["RAIL_Y"] + P["RAIL_S"] / 2
    piv = (55.0, -ro - 18.0, P["RAIL_Z"])
    endp = (55.0, -P["ROW_SPACING"] + 22.0, P["MARKER_D"] / 2 + 4.0)
    L = math.dist(piv, endp)
    stub_end = tuple(piv[i] + 70.0 * (endp[i] - piv[i]) / L for i in range(3))
    stub = b3.Compound(children=[model.htube3(piv, stub_end, 10.0, 8.8), model.xcyl2(piv[1], piv[2], 4.0, 30.0, 80.0)]
                       + [model.xcyl2(piv[1], piv[2], 6.0, 55.0 + sg * 10.0, 55.0 + sg * 22.0) for sg in (-1, 1)])
    j(12, [("Marker mount", ("marker_mount",), COL["marker"]), ("Marker arm (stub), M8 pin and spacers", stub, "#92400E"),
           ("Chain-side rail", ("rail_l",), COL["rail"]), ("M6 bolts", ("marker_bolts",), COL["bolt"])],
      (15, 95, -125, -40, 180, 250), "row marker pivot on the rail front",
      "Seen from the front, chain side. The arm folds up about the M8 pin", 25, -60)
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    out = []

    def p(name, keys, color, e=(0, 0, 0)):
        return Part(name, S(*keys), color, None, tuple(e), 1.0)

    def st(n, done, new, title, sub, **kw):
        if only and f"{n:02d}" not in only:
            return
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))
        gc.collect()

    rails = p("Side rails", ("rail_l", "rail_r"), COL["rail"])
    frame = p("Frame", ("rail_l", "rail_r", "cross_mid", "opener_bar", "clips"), COL["rail"])
    fdrop = p("Front drop plates", ("drop_front",), COL["drop"])
    wheel = p("Drive wheel", ("wheel", "lugs", "axle", "axle_bearings", "axle_spacers"), COL["wheel"])
    hous = p("Housing and bearing plate", ("housing", "bplate"), COL["housing"])
    shaft = p("Shaft and bearings", ("shaft", "shaft_bearings", "collar"), COL["bearing"])
    spro = p("Sprockets", ("sprocket_wheel", "sprocket_plate"), COL["sprocket"])
    chain = p("Chain and tensioner", ("chain", "tensioner"), COL["tensioner"])
    meter = p("Plate, liners, knob, door, brush", ("plate", "knob", "door", "brush", "liner_chain", "liner_door"), COL["plate"])
    hop = p("Uprights and hopper", ("uprights", "hopper", "lid"), COL["hopper"])
    opener = p("Opener and drop tube", ("shank", "boot", "drop_tube"), COL["shank"])
    rear = p("Rear drop plates and press wheel", ("drop_rear", "press", "press_axle", "press_spacers"), COL["press"])
    cover = p("Covering chains", ("chain_bracket", "cover_chains"), COL["cover"])
    guard = p("Chain guard", ("guard", "guard_spacers"), COL["guard"])
    handle = p("Handle", ("handle_lower", "handle_upper", "sleeves", "brace", "grip"), COL["handle"])
    kw = dict(elev=22, azim=-55)

    st(1, [rails], [p("Opener cross member", ("opener_bar",), COL["cross"], (0, 0, 120)),
                    p("Middle cross member", ("cross_mid",), COL["cross"], (0, 0, 120)),
                    p("Corner clips (4)", ("clips",), COL["clip"], (-60, 0, 60))],
       "frame: cross members and clips between the rails",
       "Lay the rails 95 mm apart on a flat bench; clips on the rear faces; M6 bolts snug, check square", **kw)
    kw = dict(elev=22, azim=-55, label_done=False)
    st(2, [frame], [p("Front drop plates", ("drop_front",), COL["drop"], (0, 0, -120))],
       "front drop plates", "On the outside faces at the front, top edges flush; two M6 bolts each through the rail", **kw)
    st(3, [p("Drive wheel", ("wheel",), COL["wheel"])], [p("Wheel lugs (18)", ("lugs",), COL["lugs"], (0, -60, 0))],
       "lugs onto the drive wheel", "Every 20 degrees, upstand trailing; two M5 countersunk screws each, threadlocker",
       elev=15, azim=-70)
    st(4, [frame, fdrop], [p("Wheel with axle, spacers and bearings", ("wheel", "lugs", "axle", "axle_bearings", "axle_spacers"), COL["wheel"], (0, 0, -220))],
       "drive wheel into the front drop plates",
       "Bearings bolt to the plates' inside faces; cross bolt through hub and axle; set screws tight", **kw)
    st(5, [frame, fdrop, wheel], [p("Metering housing", ("housing",), COL["housing"], (0, 200, 0)),
                                  p("Bearing plate", ("bplate",), COL["bplate"], (0, -150, 0))],
       "metering housing and bearing plate on the chain-side rail",
       "The same two M6 bolts pass bearing plate, rail and housing lugs; nuts in the lug slots", **kw)
    near = [p("Chain-side rail", ("rail_l",), COL["rail"]), hous]
    st(6, near, [p("Shaft bearings (2)", ("shaft_bearings",), COL["bearing"], (0, -90, 0))],
       "plate shaft bearings", "One on each face of the bearing plate, four M6 bolts (the inboard one shown pulled out too)",
       elev=15, azim=-70, label_done=False)
    st(7, near + [p("Bearings", ("shaft_bearings",), COL["bearing"])],
       [p("Plate shaft", ("shaft",), COL["axle"], (0, -160, 0)), p("Shaft collar", ("collar",), COL["bearing"], (0, 60, 40))],
       "plate shaft and collar", "Shaft in from the chain side through both bearings; collar on the D-flat 12 mm short of the housing",
       elev=15, azim=-70, label_done=False)
    st(8, [p("Chain-side rail", ("rail_l",), COL["rail"]), fdrop, wheel, hous, shaft],
       [p("Wheel sprocket", ("sprocket_wheel",), COL["sprocket"], (0, -120, 0)),
        p("Plate sprocket", ("sprocket_plate",), COL["sprocket"], (0, -120, 0))],
       "sprockets", "Hubs inward; line the two up with a straight edge; set screws on the flats", elev=12, azim=-80, label_done=False)
    st(9, [frame, fdrop, wheel, hous, shaft, spro], [p("Chain (76 links)", ("chain",), COL["chain"], (0, -140, 0)),
                                                     p("Spring tensioner", ("tensioner",), COL["tensioner"], (0, -90, -40))],
       "tensioner and chain", "Tensioner pivot bolt through the rail; chain round both sprockets, idler on the lower strand",
       elev=8, azim=-88, label_done=False)
    st(10, [frame, fdrop, wheel, hous, shaft, spro, chain],
       [p("Chain-side liner", ("liner_chain",), COL["liner"], (0, 60, 0)), p("Seed plate", ("plate",), COL["plate"], (0, 130, 0)),
        p("Door-side liner", ("liner_door",), COL["liner"], (0, 190, 0)), p("Door", ("door",), COL["door"], (0, 250, 0)),
        p("Knob", ("knob",), COL["knob"], (0, 320, 0)), p("Brush", ("brush",), COL["brush"], (-120, 0, 0))],
       "brush, liners, seed plate, door and knob", "Brush through the rear slot, gap 1 to 2 mm; chain-side liner on its pegs; plate on the D-flat; door-side liner on the door; door; knob finger tight",
       elev=18, azim=60, label_done=False)
    st(11, [frame, fdrop, wheel, hous, shaft, spro, chain, meter],
       [p("Hopper uprights (4)", ("uprights",), COL["upright"], (0, 0, 0)), p("Hopper and lid", ("hopper", "lid"), COL["hopper"], (0, 0, 200))],
       "hopper uprights and hopper", "Uprights on the rails (front ones share the clip bolts); neck into the collar; eight M5 screws",
       **kw)
    st(12, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop],
       [p("Shank and boot", ("shank", "boot"), COL["shank"], (0, 0, -200)), p("Seed drop tube", ("drop_tube",), COL["tube"], (0, 0, -120))],
       "opener and seed drop tube", "Two M6 bolts from the front of the cross member; tube on the spigot, tied to the boot",
       elev=12, azim=60, label_done=False)
    st(13, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop, opener],
       [p("Chain bracket and covering chains", ("chain_bracket", "cover_chains"), COL["cover"], (-100, 0, -100))],
       "covering chains", "Bracket on the rear face of the middle cross member; chains hang behind the opener",
       elev=20, azim=-150, label_done=False)
    st(14, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop, opener, cover],
       [p("Rear drop plates", ("drop_rear",), COL["drop"], (0, 0, 0)), p("Press wheel, axle, spacers", ("press", "press_axle", "press_spacers"), COL["press"], (0, 0, -180))],
       "rear drop plates and press wheel", "Plates on the rails; axle through plates, spacers and wheel; nuts tight to clamp the stack",
       **kw)
    st(15, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop, opener, rear, cover],
       [p("Chain guard and spacers", ("guard", "guard_spacers"), COL["guard"], (0, -160, 0))],
       "chain guard", "Two M5 x 50 screws through the face and spacers into the tapped plates; turn the wheel: nothing rubs",
       elev=12, azim=-75, label_done=False)
    st(16, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop, opener, rear, cover, guard],
       [p("Handle", ("handle_lower", "handle_upper", "sleeves", "brace", "grip"), COL["handle"], (-150, 0, 80))],
       "handle", "Flattened ends on the rear drop plates, two M8 bolts each; sleeves, upper tubes, brace and grip",
       elev=20, azim=-60, label_done=False)
    st(17, [frame, fdrop, wheel, hous, shaft, spro, chain, meter, hop, opener, rear, cover, guard, handle],
       [p("Row marker kit", ("marker_mount", "marker_arm", "marker_disc"), COL["marker"], (200, -150, 120))],
       "row marker kit (option)", "Mount at the front of the chain-side rail, two M6 bolts; arm on the M8 pin; set the reach",
       elev=25, azim=-50, label_done=False)
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("only=")]
    only = None
    for a in sys.argv[1:]:
        if a.startswith("only="):
            only = set(a[5:].split(","))
    what = args or ["overview", "sheets", "joints", "steps"]
    fns = {"overview": overview, "sheets": lambda: sheets(only), "joints": lambda: joints(only), "steps": lambda: steps(only)}
    for w in what:
        r = fns[w]()
        print(w, "->", r)
