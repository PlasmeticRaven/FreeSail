"""Replay the owner's save on a tree until it raises; say which crewed vessels there are and what ship each holds.
usage: python3 -P -E crash_probe.py <tree> <save.json>"""
import sys, os, traceback
tree, save = sys.argv[1], sys.argv[2]
sys.path.insert(0, tree); os.chdir(tree)
from freesail.core import replay as R
from freesail.api.session import ship_factory as SF  # the game's own: without it the player's ship is a stub
data = R.load_file(save)
box = {}
def on_tick(w):
    box["w"] = w
    return False
try:
    w = R.replay(data, SF, on_tick=on_tick)
    print("END no error", w.clock.tick)
except Exception as e:
    w = box["w"]
    print("RAISED at tick", w.clock.tick, type(e).__name__, e)
    tb = traceback.extract_tb(e.__traceback__)
    print("  where:", [(f.name, f.lineno) for f in tb][-6:])
    for v in getattr(w.vessels, "vessels", []):
        c = getattr(v, "crew", None)
        if c is None:
            continue
        b = getattr(v, "brain", None)
        print("  crewed", v.id, "kind", getattr(v, "kind", None), "class", getattr(v, "ship_class", None) or getattr(v, "ship_ref", None),
              "shape", getattr(c, "shape", None), "ship", type(getattr(c, "ship", None)).__name__,
              "state", getattr(b, "state", None), "done", getattr(v, "done", None),
              "intent", getattr(getattr(b, "intent", None), "words", None))
    print("  hulls", [(getattr(h, "shape", None), type(getattr(h, "ship", None)).__name__) for h in w.hulls])
