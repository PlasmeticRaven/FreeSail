"""Pytest plugin: record a recorded passage's whole state trace while its test runs.

    cd <tree> && TRACE_OUT=out.json TRACE_EVERY=60 PYTHONPATH=$PWD:<probes>/gate \
        python3 -P -m pytest -p traceplug -p no:cacheprovider -o addopts="" -q --slow <node ids>

Every World built during the run is traced (in creation order): its state hash (run.py's phys,
the player's ship and every vessel) every TRACE_EVERY ticks, and at the end of the session its
log (tick, kind, severity, text). Compare two outputs with `python3 -I traceplug.py A B`.
Run one test at a time (no -n) so the worlds' order is the test's own.
"""

import json
import os
import sys


def pytest_configure(config):
    from freesail.core import world as W

    import run as R

    every = int(os.environ.get("TRACE_EVERY", "60"))
    worlds = []
    orig = W.World.tick

    def tick(self, *a, **k):
        out = orig(self, *a, **k)
        d = self.__dict__
        if "_trace_id" not in d:
            d["_trace_id"] = len(worlds)
            worlds.append({"world": self, "hashes": []})
        if self.clock.tick % every == 0:
            try:
                worlds[d["_trace_id"]]["hashes"].append([self.clock.tick, R.phys(self)])
            except Exception as e:  # noqa: BLE001
                worlds[d["_trace_id"]]["hashes"].append([self.clock.tick, "ERR " + str(e)[:80]])
        return out

    W.World.tick = tick
    config._trace_worlds = worlds


def pytest_unconfigure(config):
    worlds = getattr(config, "_trace_worlds", [])
    res = []
    for w in worlds:
        wd = w["world"]
        res.append({"hashes": w["hashes"], "end_tick": wd.clock.tick,
                    "log": [[e.tick, e.kind, e.severity.value, e.text] for e in wd.log]})
    json.dump(res, open(os.environ.get("TRACE_OUT", "trace.json"), "w"))


if __name__ == "__main__" and len(sys.argv) == 3:
    import difflib
    from collections import Counter

    sys.path.insert(0, os.path.dirname(__file__))
    from compare import classify

    a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    print("worlds", len(a), len(b))
    for i, (x, y) in enumerate(zip(a, b)):
        hx, hy = dict(map(tuple, x["hashes"])), dict(map(tuple, y["hashes"]))
        common = sorted(set(hx) & set(hy))
        first = next((t for t in common if hx[t] != hy[t]), None)
        lx = [tuple(e) for e in x["log"]]
        ly = [tuple(e) for e in y["log"]]
        sm = difflib.SequenceMatcher(None, lx, ly, autojunk=False)
        c = Counter()
        sev_moved = 0
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            for e in lx[i1:i2]:
                if any(f[0] == e[0] and f[1] == e[1] and f[3] == e[3] and f[2] != e[2] for f in ly[j1:j2]):
                    sev_moved += 1
                c[("-", classify(e[1], e[2], e[3], "-"), e[2], e[1])] += 1
            for e in ly[j1:j2]:
                c[("+", classify(e[1], e[2], e[3], "+"), e[2], e[1])] += 1
        print(f"world {i}: ticks {x['end_tick']}/{y['end_tick']}; hashes compared {len(common)}, first differing: {first}; "
              f"lines {len(lx)} -> {len(ly)}; lines whose severity alone moved: {sev_moved}")
        for k, v in sorted(c.items()):
            print(f"    {v:4d} {k}")
