"""Replay a save to a tick, then count which far captain plans, and time it, over the next ticks.
usage: python3 -P -E who_plans.py <tree> <save> <at_tick> <span>"""
import sys, os, time, collections
tree, save, at, span = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, tree); os.chdir(tree)
from freesail.core import replay as R
from freesail.world import brains as B
data = R.load_file(save)
w = R.replay(data, until_tick=at)
print("at", w.clock.tick, w.clock.ship_time)
calls = collections.Counter(); spent = collections.Counter()
orig_plan = B.FarCaptain._plan
def _plan(self):
    t = time.perf_counter()
    try:
        return orig_plan(self)
    finally:
        calls[self.vessel.id] += 1; spent[self.vessel.id] += time.perf_counter() - t
B.FarCaptain._plan = _plan
def show(tag):
    print(tag)
    for v in w.vessels.vessels:
        b = getattr(v, "brain", None)
        if b is None: continue
        it = getattr(b, "intent", None)
        print(f"  {v.id:14s} state={getattr(b,'state',None)!s:24s} intent={getattr(it,'words',None)!s:48.48s} plan={str(getattr(v,'plan',None))[:90]} saved={'y' if getattr(v,'saved_plan',None) else 'n'} warn={getattr(v,'warning',None)}")
show("BEFORE")
t0 = time.perf_counter()
for _ in range(span):
    w.tick()
el = time.perf_counter() - t0
print(f"{span} ticks in {el:.1f} s = {span/el:.0f} t/s")
for k, n in calls.most_common():
    print(f"  {k}: _plan called {n} times, {spent[k]:.1f} s")
show("AFTER")
