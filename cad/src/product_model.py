"""SeedLine product model for photoreal renders (kit 1.9), TRL 3, constructable design (SDL-DDR-003, SDL-DEC-001).

Every part of the chosen design comes from cad/src/model.py components("A") as it is: frame, drive wheel with its
lugs and screws, axle and bearings, sprockets, roller chain and tensioner, chain guard, hopper, metering housing with
its clear door, seed plate and liners, brush, drop tube, opener, covering chains, press wheel, handle, row marker kit
and every fastener. Only the scene is added as context parts: a strip of tilled seedbed with clods (its surface at
z = 0, the opener 50 mm into it), the row already sown behind the press wheel, the marker's scratched line, and a
1.75 m mannequin pushing at the grip. CONCEPT, NOT FOR FABRICATION.

Groups: "shell" (the seeder), "internal" (the metering unit: hopper, housing, door, plate, liners, knob, brush, drop
tube), "accessory" (the row marker kit) and "context" (site and figure).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Pos, Rot, Sphere  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part  # noqa: E402
import model  # noqa: E402
from model import PARAMS as P  # noqa: E402

TITLE = "SeedLine: push seeder with 3D-printed seed plates"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 18, "az": -38,
     "args": ["--scene=outdoor", "--ground=soil", "--ground-z=0", "--sun=40,-70", "--lens=40"],
     "note": "Site render from the front, chain side, about 18 deg elevation: the seeder on a tilled seedbed with the "
             "opener in the soil, the marker arm out at 0.75 m scratching the next row, the sown row firmed behind the "
             "press wheel and a 1.75 m operator pushing at the grip"},
    {"name": "studio", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 24, "az": -50,
     "note": "Studio render from the front, chain side, about 24 deg elevation: frame, drive wheel and lugs, chain "
             "guard, hopper and metering housing, opener, press wheel, handle and the folded-out marker arm"},
    {"name": "detail", "groups": ["internal"], "explode": False, "el": 20, "az": 60,
     "note": "Detail of the metering unit from the door side and ahead, about 20 deg elevation: the printed maize plate "
             "and its liners behind the clear door, the thumb screws into the housing wall, the knob, brush and drop tube"},
]

INTERNAL = {4, 5, 6, 7, 8}


def _group(p):
    if p["kind"] == "context":
        return "context"
    b = p.get("bom")
    if b in INTERNAL:
        return "internal"
    if b == 14:
        return "accessory"
    return "shell"


def scene():
    """Tilled seedbed strip with clods, the sown row behind the press wheel, the marker line and the operator."""
    out = [part("Tilled seedbed (site)", Pos(-700, -350, -60) * Box(3400, 1700, 120), "soil", "context")]
    rnd = random.Random(7256)
    for k in range(90):
        x = rnd.uniform(-2300, 900)
        y = rnd.uniform(-1150, 450)
        if abs(y) < 60 or abs(y + P["ROW_SPACING"]) < 40:
            continue
        r = rnd.uniform(8, 26)
        out.append(part(f"Clod {k + 1} (site)", Pos(x, y, -r * 0.45) * Sphere(r), "soil", "context"))
    # the sown row behind the press wheel: a firmed strip a little below the seedbed, reaching below ground
    xp = P["X_PRESS"]
    out.append(part("Firmed row behind the press wheel (site)", Pos(xp - 900, 0, -3.0 - 30) * Box(1700, 70, 60), "mud", "context"))
    out.append(part("Marker line scratched in the seedbed (site)", Pos(-650, -P["ROW_SPACING"], -2.5 - 30) * Box(1300, 12, 60), "mud", "context"))
    from context_parts import mannequin, mannequin_landmarks
    lm = mannequin_landmarks(1750, "push")
    hands = lm["hands"]
    hx = sum(h[0] for h in hands) / 2
    hy = sum(h[1] for h in hands) / 2
    hz = sum(h[2] for h in hands) / 2
    (hbx, hbz), (gx, gz) = model.handle_points()
    # the figure faces -Y; turned 90 degrees it faces +X, the direction of travel, hands on the cross grip
    cx, cy = -hy, hx                                 # hand midpoint after Rot(0, 0, 90): (x, y) -> (-y, x)
    person = Pos(gx - 18.0 - cx, 0.0 - cy, 0) * Rot(0, 0, 90) * mannequin(1750, "push")
    out.append(part("Operator, 1.75 m mannequin (scale)", person, "skin", "context"))
    return out


def product_parts():
    out = []
    for p in model.components(model.CHOSEN):
        q = dict(p)
        q["group"] = _group(p)
        out.append(q)
    for p in scene():
        q = dict(p)
        q["group"] = "context"
        out.append(q)
    return out


if __name__ == "__main__":
    ps = product_parts()
    from collections import Counter
    print(Counter(p["group"] for p in ps))
    for p in ps:
        if p["group"] == "context" and "Clod" not in p["name"]:
            bb = p["shape"].bounding_box()
            print(f"{p['name']:50s} z {bb.min.Z:7.0f} to {bb.max.Z:7.0f}  valid={p['shape'].is_valid}")
    print(len(ps), "parts")
