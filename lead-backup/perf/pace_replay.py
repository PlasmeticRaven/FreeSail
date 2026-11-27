"""Replay one of the owner's saves on a tree and print the pace per block of ticks.
usage: python3 -P -E pace_replay.py <tree> <save.json> <block> [profile_from profile_to]"""
import sys, time, json, os
tree, save, block = sys.argv[1], sys.argv[2], int(sys.argv[3])
prof = (int(sys.argv[4]), int(sys.argv[5])) if len(sys.argv) > 5 else None
sys.path.insert(0, tree)
os.chdir(tree)
from freesail.core import replay as R
data = R.load_file(save)
st = {"t": time.perf_counter(), "n": 0}
pr = None
def on_tick(w):
    global pr
    k = w.clock.tick
    if prof and k == prof[0]:
        import cProfile
        pr = cProfile.Profile(); pr.enable()
    if prof and k == prof[1] and pr is not None:
        pr.disable()
        import pstats, io
        s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(60)
        open(save + ".profile.txt", "w").write(s.getvalue())
        print("PROFILE WRITTEN", flush=True)
        return True
    if k % block == 0:
        now = time.perf_counter()
        rate = block / (now - st["t"]); st["t"] = now
        vs = getattr(w.vessels, "vessels", [])
        crewed = list(getattr(w.vessels, "crewed_ids", ()) or ())
        near = getattr(w.vessels, "near_ids", None)
        print(f"tick {k:7d} {rate:7.0f} t/s vessels {len(vs):3d} crewed {len(crewed)} {crewed} hulls {len(w.hulls)} near {near if near is None else len(near)}", flush=True)
    return False
w = R.replay(data, on_tick=on_tick)
print("END", w.clock.tick)
