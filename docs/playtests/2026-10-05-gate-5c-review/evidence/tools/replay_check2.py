"""Read-only: replay a save and say HOW its log differs from the checkpoint's log:
only in the order of lines within a tick, or in substance. Writes nothing into any tree.

usage: replay_check2.py SAVE.json
"""
import collections
import sys
import time

from freesail.api.session import ship_factory
from freesail.core import replay as R

path = sys.argv[1]
data = R.load_file(path)
header, cw = R.read_checkpoint(R.checkpoint_path(path))
t0 = time.time()
w = R.replay(data, ship_factory)
print(f"replayed {path} in {time.time() - t0:.1f}s")
a = cw.log.all()
b = w.log.all()


def key(e):
    return (e.tick, e.severity.value, e.kind, e.actor, e.text)


print(f"lines: played {len(a)}, replayed {len(b)}; digests equal: {cw.log.digest() == w.log.digest()}")
ca = collections.Counter(key(e) for e in a)
cb = collections.Counter(key(e) for e in b)
only_a = ca - cb
only_b = cb - ca
print(f"lines only in the played log: {sum(only_a.values())}; only in the replayed log: {sum(only_b.values())}")
if not only_a and not only_b:
    # same lines; where does the ORDER differ?
    ticks = []
    i = 0
    n = len(a)
    while i < n:
        if key(a[i]) != key(b[i]):
            ticks.append(a[i].tick)
        i += 1
    tset = sorted(set(ticks))
    print(f"same set of lines; order differs at {len(ticks)} positions, in {len(tset)} ticks: {tset[:20]}")
    for t in tset[:3]:
        print(f"--- tick {t}, played order then replayed order")
        for e in [x for x in a if x.tick == t]:
            print(f"   played  : {e.kind} | {e.actor} | {e.text[:110]}")
        for e in [x for x in b if x.tick == t]:
            print(f"   replayed: {e.kind} | {e.actor} | {e.text[:110]}")
else:
    first_a = min((k[0] for k in only_a), default=None)
    first_b = min((k[0] for k in only_b), default=None)
    print(f"first tick with a line only in played: {first_a}; only in replayed: {first_b}")
    for k in sorted(only_a)[:12]:
        print(f"   only played  : {k[0]} | {k[1]} | {k[2]} | {k[3]} | {k[4][:140]}")
    for k in sorted(only_b)[:12]:
        print(f"   only replayed: {k[0]} | {k[1]} | {k[2]} | {k[3]} | {k[4][:140]}")
# final state, the ship's place and the account
try:
    pa, pb = cw.position, w.position
    print(f"true position played   : {pa}")
    print(f"true position replayed : {pb}")
except Exception as e:  # noqa: BLE001
    print("position compare failed:", e)
for a_ in (w.agents or {}).values():
    m = getattr(a_, "model", None)
    if m is not None and hasattr(m, "entries"):
        print(f"station {a_.station.name}: transcript entries used {m.at} of {len(m.entries)}")
st = [(r["station"].get("name"), r.get("stationed_tick"), r.get("stationed_after_orders"), r.get("door")) for r in data.get("agents") or []]
print("stationed (name, tick, after_orders, door):", st)
print("first inputs:", [(e.get("tick"), "line" if "line" in e else e.get("order", e.get("world_order")))[:2] for e in (data.get("inputs") or [])[:4]])
