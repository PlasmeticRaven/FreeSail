import json, sys, math
def load(p): return {json.loads(l)["id"]: json.loads(l) for l in open(p)}
A, B = load(sys.argv[1]), load(sys.argv[2])
def stats(r):
    m = r["minutes"]
    if not m: return None
    u = [x[0] for x in m]
    made = m[-1][3] / 1852.0  # north (toward Falmouth), nm
    dist = sum(abs(x) for x in u) / 60.0
    ev = r["events"][r.get("n0", 0):]
    aback = sum(1 for e in ev if e[1] == "ship.aback")
    astern = sum(1 for x in u if x < 0)
    short = sum(1 for e in ev if "hands" in e[3] and ("short" in e[3] or "only" in e[3]))
    refused = sum(1 for e in ev if e[1] in ("order.rejected", "evolution.failed", "evolution.refused") )
    third = sum(u[120:]) / max(1, len(u[120:]))
    return dict(made=round(made, 2), dist=round(dist, 2), third=round(third, 2), aback=aback, astern=astern,
                short=short, refused=refused, state=r.get("state"))
print(f"{'case':55s} {'made o/n':>13s} {'3rd-hr o/n':>13s} {'aback':>7s} {'astern':>9s} {'short':>7s} {'refus':>7s}")
for cid in sorted(A):
    a, b = stats(A[cid]), stats(B[cid])
    if A[cid]["error"] or B[cid]["error"]:
        print(cid, "ERROR", (A[cid]["error"] or "")[-200:], (B[cid]["error"] or "")[-200:]); continue
    flag = ""
    if b["made"] < a["made"] - 0.3 or b["third"] < a["third"] - 0.3: flag += " WORSE-WAY"
    if b["aback"] > a["aback"]: flag += " MORE-ABACK"
    if b["astern"] > a["astern"] + 2: flag += " MORE-ASTERN"
    if b["short"] > a["short"]: flag += " MORE-SHORT"
    if b["refused"] > a["refused"]: flag += " MORE-REFUSED"
    print(f"{cid:55s} {a['made']:6.2f}/{b['made']:6.2f} {a['third']:6.2f}/{b['third']:6.2f} {a['aback']:3d}/{b['aback']:3d} {a['astern']:4d}/{b['astern']:4d} {a['short']:3d}/{b['short']:3d} {a['refused']:3d}/{b['refused']:3d} {a['state']}/{b['state']}{flag}")
