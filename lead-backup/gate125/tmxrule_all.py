import json, sys
def load(p):
    return {(r["ship"], r["kn"], r["seed"], str(r["hd"]), r["sail"]): r for r in map(json.loads, open(p)) if "error" not in r}
o, n = load(sys.argv[1]), load(sys.argv[2])
DA = {"hermaphrodite-brig", "privateer-schooner", "topsail-schooner"}
DC = {"brig", "merchant-brig"}
DD = {("frigate-36", 25), ("razee-44", 25)}
for k in sorted(set(o) & set(n), key=str):
    a, b = o[k], n[k]
    if a.get("short_reply") != b.get("short_reply"):
        rule = "D"
        ok = (k[0], k[1]) in DD
        first = "short reply"
    else:
        la = [l for l in a.get("lines", []) if l[1] != "ship.leeway"]
        lb = [l for l in b.get("lines", []) if l[1] != "ship.leeway"]
        if la == lb and a.get("end") == b.get("end"):
            continue
        i = next((i for i, (x, y) in enumerate(zip(la, lb)) if x != y), min(len(la), len(lb)))
        x = la[i] if i < len(la) else None
        y = lb[i] if i < len(lb) else None
        t = (x or ["", "", ""])[2] + " | " + (y or ["", "", ""])[2]
        if "aul" in t and ("ainsail haul" in t or "opsail haul" in t or "hangs in stays" in t or "Let fly" in t or "through the wind" in t):
            rule, ok = "A", k[0] in DA
        elif "Missed stays: she came through" in t or "Missed stays: she lies in irons" in t:
            rule, ok = "C", k[0] in DC
        else:
            rule, ok = "?", False
        first = f"@{(x or y)[0]} OLD:{x} NEW:{y}"
    if True:
        eo, en = a.get("end"), b.get("end")
        fo = eo if isinstance(eo, str) else f"{eo['kind']}{eo['s']} rel{round(eo['rel'])}/{round(a['rel300'])}"
        fn = en if isinstance(en, str) else f"{en['kind']}{en['s']} rel{round(en['rel'])}/{round(b['rel300'])}"
        print(f"UNDECL {rule} {k}: OLD {fo} NEW {fn} :: {first[:300]}")
