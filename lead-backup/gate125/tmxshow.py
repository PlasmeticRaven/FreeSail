import json, sys, difflib
def load(p):
    return {(r["ship"], r["kn"], r["seed"], str(r["hd"]), r["sail"]): r for r in map(json.loads, open(p)) if "error" not in r}
o, n = load(sys.argv[1]), load(sys.argv[2])
k = (sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], sys.argv[7])
for tag, d in (("OLD", o), ("NEW", n)):
    r = d[k]
    print("=====", tag, r.get("reply"), "| short:", r.get("short_reply", "")[-400:])
if "--diff" in sys.argv:
    a = [f"{l[0]} {l[1]} {l[2]}" for l in o[k].get("lines", []) if l[1] != "ship.leeway"]
    b = [f"{l[0]} {l[1]} {l[2]}" for l in n[k].get("lines", []) if l[1] != "ship.leeway"]
    for x in difflib.unified_diff(a, b, lineterm="", n=1):
        print(x)
