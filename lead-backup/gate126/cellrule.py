import json, re, sys
sys.path.insert(0, ".")
import tests.test_mends_126 as T
from collections import defaultdict
recs = {}
for path in sys.argv[1:]:
    for l in open(path):
        r = json.loads(l); recs[r["id"]] = r
cells = defaultdict(dict)
for k, r in recs.items():
    ship, wind, seed, how = k.split("|")
    cells[(ship, wind, int(seed))][how] = r
SHORT = re.compile(r"(the rest are|the watch is|the hands are)[^.]*(clearing away the wreck|shifting the|rigging a jury mast)")
outside_undeclared = []
print(f"{'cell-seed':30s} {'made trunk/inst/new':>22s} {'astern':>13s} {'aback':>10s} {'brought t/n':>13s} by      verdict  belays allH short declared")
for key in sorted(cells):
    c = cells[key]
    if not all(h in c and not c[h].get("error") for h in ("old", "instant", "mine")):
        print(key, "MISSING/ERR", {h: (c.get(h) or {}).get("error", "missing")[:80] if c.get(h) is None or c[h].get("error") else "ok" for h in ("old","instant","mine")}); continue
    t, i, m = c["old"], c["instant"], c["mine"]
    v = T._seed_verdict(t, i, m)
    dec = key in T.PASSAGE_DECLARED
    ev = [e for e in m["events"] if e[0] >= 600]
    bel = sum(1 for e in ev if e[3].startswith(("Belayed clearing", "Belayed shifting", "Belayed rigging")))
    allh = sum(1 for e in ev if "calling all hands (to clear" in e[3])
    sh = [e for e in ev if SHORT.search(e[3])]
    if v["why"] and not dec: outside_undeclared.append(key)
    f = lambda r: f"{r['made_good']:.2f}"
    print(f"{'|'.join(map(str,key)):30s} {f(t):>6s}/{f(i):>6s}/{f(m):>6s} {t['astern']:3d}/{i['astern']:3d}/{m['astern']:3d} {t['aback']:2d}/{i['aback']:2d}/{m['aback']:2d} {str(t['brought_to']):>6s}/{str(m['brought_to']):>6s} {v['by']:7s} {'OUT:'+','.join(v['why']) if v['why'] else 'ok':8s} {bel:4d} {allh:3d} {len(sh):3d} {'DECLARED' if dec else ''}")
    for e in sh[:2]: print("     SHORT", e[0], e[3][:140])
print("OUTSIDE AND UNDECLARED:", outside_undeclared)
