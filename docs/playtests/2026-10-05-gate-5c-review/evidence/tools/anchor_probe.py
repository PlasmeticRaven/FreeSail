"""Read-only: replay a scratch copy of the save to END_TICK and record, while any anchor is
down in the given window, each anchor's place on the ground, scope, load, holding and the
dragging flag, with the ship's own place. Writes OUT (jsonl) in the scratchpad only.

usage: anchor_probe.py SAVE.json OUT.jsonl FROM_TICK END_TICK [EVERY]
"""
import json
import math
import sys

from freesail.api.session import ship_factory
from freesail.core import replay as R
from freesail.ship.parts import GroundTackle

path, out, lo, hi = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
every = int(sys.argv[5]) if len(sys.argv) > 5 else 30
data = R.load_file(path)
world = R.build_world(data, ship_factory)
inputs = data["inputs"]
f = open(out, "w", encoding="utf-8")
i = 0
while True:
    while i < len(inputs) and int(inputs[i]["tick"]) == world.clock.tick:
        R._give(world, inputs[i])
        i += 1
        for agent in list(world.agents.values()):
            agent.on_input()
    if world.clock.tick >= hi:
        break
    world.tick()
    t = world.clock.tick
    if t >= lo and t % every == 0:
        tackle = world.ship.extra.get("ground_tackle")
        if isinstance(tackle, GroundTackle):
            d = world.ship.dyn
            row = {"tick": t, "x": round(d.x, 1), "y": round(d.y, 1), "head": round(math.degrees(d.heading) % 360, 1), "anchors": []}
            for a in tackle.anchors:
                if a.down:
                    row["anchors"].append(
                        {
                            "id": a.id,
                            "gx": None if a.ground_x is None else round(a.ground_x, 1),
                            "gy": None if a.ground_y is None else round(a.ground_y, 1),
                            "scope_m": round(a.scope_m, 1),
                            "depth_m": round(a.depth_m, 1),
                            "load_kn": round(a.cable_load_kn, 2),
                            "hold_kn": round(a.holding_kn, 2),
                            "taut": bool(a.taut),
                            "dragging": bool(a.dragging),
                            "drag_s": round(getattr(a, "drag_s", 0.0), 0),
                            "bottom": a.bottom,
                            "heaving": bool(a.heaving),
                        }
                    )
            if row["anchors"]:
                f.write(json.dumps(row) + "\n")
f.close()
print("done", world.clock.tick)
