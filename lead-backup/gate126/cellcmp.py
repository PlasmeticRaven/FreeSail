import json, re, sys
from collections import defaultdict
recs = {}
for path in sys.argv[1:]:
    for l in open(path):
        r = json.loads(l); recs[r["id"]] = r
cells = defaultdict(dict)
for k, r in recs.items():
    ship, wind, seed, how = k.split("|")
    cells[(ship, wind, int(seed))][how] = r
SPARW = re.compile(r"(the rest are|the watch is|the hands are)[^.]*(clearing away the wreck|shifting the|rigging a jury mast)")
def spar_stats(r):
    ev = [e for e in r.get("events", []) if e[0] >= 600]
    short = [e for e in ev if (e[1] in ("evolution.short_handed", "evolution.waiting", "order.rejected", "evolution.failed")) and SPARW.search(e[3])
             and not e[3].startswith(("Belayed",))]
    belays = [e for e in ev if e[3].startswith("Belayed clearing") or e[3].startswith("Belayed shifting") or e[3].startswith("Belayed rigging")]
    allh = [e for e in ev if "calling all hands (to clear away" in e[3]]
    pipe = [e for e in ev if "piping down (the wreck cleared" in e[3]]
    return short, belays, allh, pipe
print(f"{'cell-seed':32s} {'made old/inst/new':>22s} {'astern o/i/n':>14s} {'aback o/i/n':>12s} {'brought o/n':>14s} short belays allH pipe")
worse = []
for key in sorted(cells):
    c = cells[key]
    if "old" not in c or "mine" not in c: continue
    o, n, i = c["old"], c["mine"], c.get("instant")
    if o.get("error") or n.get("error"): print(key, "ERROR", (o.get("error") or n.get("error"))[-300:]); continue
    f = lambda r, k: (f"{r[k]:.2f}" if isinstance(r.get(k), float) else str(r.get(k))) if r else "-"
    short, belays, allh, pipe = spar_stats(n)
    flags = []
    if n["made_good"] < o["made_good"] - 0.3: flags.append("WAY")
    if n["astern"] > o["astern"] + 5: flags.append("ASTERN")
    if n["aback"] > o["aback"] + 1: flags.append("ABACK")
    if o["brought_to"] is not None and (n["brought_to"] is None or n["brought_to"] - o["brought_to"] > 600): flags.append("BROUGHT-LATE")
    if flags: worse.append((key, flags))
    print(f"{'|'.join(map(str,key)):32s} {f(o,'made_good'):>6s}/{f(i,'made_good'):>6s}/{f(n,'made_good'):>6s} {o['astern']:4d}/{(i or {}).get('astern','-')!s:>4s}/{n['astern']:4d} {o['aback']:3d}/{(i or {}).get('aback','-')!s:>3s}/{n['aback']:3d} {str(o['brought_to']):>6s}/{str(n['brought_to']):>6s} {len(short):5d} {len(belays):6d} {len(allh):4d} {len(pipe):4d} {' '.join(flags)}")
    for e in short[:3]: print("      SHORT", e[0], e[3][:150])
print("WORSE THAN OLD:", worse)
