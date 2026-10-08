"""Read-only test, in memory, on the game's last checkpoint (moored in Brest road, both
bowers down at 68 fathoms): what do the ground-tackle orders do with an anchor's name and
with 'to N fathoms'? Nothing is written anywhere; each trial starts from a fresh load.

usage: tackle_words_test.py SAVE.json
"""
import sys

from freesail.core import replay as R
from freesail.ship.parts import GroundTackle

path = sys.argv[1]


def state(world):
    t = world.ship.extra.get("ground_tackle")
    out = []
    for a in t.anchors:
        if a.down:
            out.append(f"{a.name} {a.scope_fathoms:.0f} fm{' (heaving)' if a.heaving else ''}")
    return "; ".join(out), t.riding_by().name if hasattr(t, "riding_by") and t.riding_by() else "?"


def trial(order, ticks=900):
    _, world = R.read_checkpoint(R.checkpoint_path(path))
    before, riding = state(world)
    n0 = len(world.log.all())
    world.submit(order, actor="captain")
    for _ in range(ticks):
        world.tick()
    said = [e.text for e in world.log.all()[n0:] if e.kind in ("order.accepted", "order.rejected", "cable.veered", "cable.hove_short", "ship.aweigh", "ship.weighed", "evolution.failed", "evolution.started", "cable.hove_in")]
    after, _ = state(world)
    print(f"ORDER: {order!r}   (riding by {riding})")
    print(f"   before: {before}")
    print(f"   after {ticks // 60} min: {after}")
    for s in said[:4]:
        print(f"   log: {s[:150]}")


for o in (
    "veer to 80 fathoms",
    "veer the best bower to 80 fathoms",
    "veer the small bower to 80 fathoms",
    "veer 10 fathoms",
    "veer cable on the small bower 10 fathoms",
):
    trial(o)
for o in ("weigh the small bower", "weigh the best bower", "heave short the small bower", "heave short"):
    trial(o, 2400)
