"""Dump the components of run.py's state hash for one case at given ticks, to find what differs.

    cd <tree> && PYTHONPATH=$PWD python3 -P <probes>/gate/statedump.py CASES.py CASE_ID OUT.json T1 [T2 ...]

Runs the case's steps (only "order"/"run"/"py" steps, run cut at the last tick asked) and writes
{tick: {component: value}}; diff two such files with `python3 -I statedump.py --diff A B`.
"""
import json
import sys


def comps(w):
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    import run as R

    s = w.ship
    out = {"dyn": [(k, R._prim(v)) for k, v in R._fields(s.dyn).items()]}
    for pid, p in s.parts.items():
        out[pid] = [(k, R._prim(v)) for k, v in R._fields(p).items() if R._prim(v) is not None]
    st = s.extra.get("strain")
    if st is not None:
        out["strain"] = json.dumps(st.snapshot(), default=str)
        out["strain.last"] = sorted((k, repr(v)) for k, v in st.last_warning_s.items())
    vs = w.vessels.vessels
    items = vs.items() if isinstance(vs, dict) else ((getattr(v, "id", i), v) for i, v in enumerate(vs))
    for vid, v in items:
        pos = getattr(v, "position", None)
        out[f"vessel:{vid}"] = [repr(getattr(pos, "lat_deg", pos)), repr(getattr(pos, "lon_deg", None)),
                                repr(getattr(v, "heading", None)), repr(getattr(v, "speed", None))]
    return out


def main(argv):
    if argv[0] == "--diff":
        a, b = json.load(open(argv[1])), json.load(open(argv[2]))
        for t in a:
            for k in sorted(set(a[t]) | set(b.get(t, {}))):
                if a[t].get(k) != b.get(t, {}).get(k):
                    print(t, k, str(a[t].get(k))[:300], "|", str(b.get(t, {}).get(k))[:300])
        return
    ns = {}
    exec(open(argv[0]).read(), ns)
    case = next(c for c in ns["CASES"] if c["id"] == argv[1])
    ticks = sorted(int(x) for x in argv[3:])
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    import run as R

    w = R.make(case)
    res = {}
    for t in ticks:
        w.run(t - w.clock.tick)
        res[str(t)] = comps(w)
    json.dump(res, open(argv[2], "w"), default=str)


if __name__ == "__main__":
    main(sys.argv[1:])
