"""Read-only check: does a save replay, on the build given by PYTHONPATH, to the same log
that its checkpoint holds? Writes nothing into any tree.

usage: replay_check.py SAVE.json
"""
import sys
import time

from freesail.api.session import ship_factory
from freesail.core import replay as R

path = sys.argv[1]
data = R.load_file(path)
header, cw = R.read_checkpoint(R.checkpoint_path(path))
agents = data.get("agents") or []
print(f"save: {path}")
print(
    f"end tick {data['end_tick']}; inputs {len(data.get('inputs') or [])}; "
    f"stations {[(a['station'].get('name'), a.get('model_name'), len(a.get('transcript') or [])) for a in agents]}"
)
t0 = time.time()
try:
    w = R.replay(data, ship_factory)
except Exception as e:  # report, do not hide
    print(f"REPLAY RAISED after {time.time() - t0:.1f}s: {type(e).__name__}: {e}")
    raise
dt = time.time() - t0
a = cw.log.all()
b = w.log.all()
print(f"replayed in {dt:.1f}s")
print(f"checkpoint log: {len(a)} lines, digest {cw.log.digest()[:16]} (header {str(header.get('digest'))[:16]})")
print(f"replayed log:   {len(b)} lines, digest {w.log.digest()[:16]}")
print(f"IDENTICAL: {cw.log.digest() == w.log.digest()}")
if cw.log.digest() != w.log.digest():
    n = min(len(a), len(b))
    first = next(
        (i for i in range(n) if (a[i].tick, a[i].kind, a[i].actor, a[i].text) != (b[i].tick, b[i].kind, b[i].actor, b[i].text)),
        n,
    )
    print(f"first difference at line {first} of {n}")
    for i in range(max(0, first - 2), min(n, first + 4)):
        mark = "  " if i < first else ">>"
        print(f"{mark} played  : {a[i].tick} | {a[i].kind} | {a[i].actor} | {a[i].text[:150]}")
        print(f"{mark} replayed: {b[i].tick} | {b[i].kind} | {b[i].actor} | {b[i].text[:150]}")
    if first < n:
        print(f"ship's time of the first difference: tick {a[first].tick}")
for a_ in w.agents.values() if getattr(w, "agents", None) else []:
    m = getattr(a_, "model", None)
    if m is not None and hasattr(m, "entries"):
        print(f"station {a_.station.name}: transcript entries used {m.at} of {len(m.entries)}")
