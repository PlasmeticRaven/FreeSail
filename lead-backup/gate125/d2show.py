import json, sys
o = {tuple(r["key"]): r for r in map(json.loads, open(sys.argv[1]))}
n = {tuple(r["key"]): r for r in map(json.loads, open(sys.argv[2]))}
for k in sorted(n, key=str):
    a, b = o.get(k), n[k]
    for tag, r in (("OLD", a), ("NEW", b)):
        if r is None or "error" in r:
            print(k, tag, "ERR", (r or {}).get("error", "missing")[-300:]); continue
        bl = [l[2] for l in r["blown"]]
        jw = [(l[0], l[3][:70]) for l in r["jibwarn"][:2]]
        cap = [(l[0], l[3][:80]) for l in r["lines"] if l[3].startswith("By the captain") and "jib" in l[3].lower()][:2]
        print(k, tag, "KEPT" if r["kept"] else "-", "most", {s: round(v, 2) for s, v in r["most"].items()}, "in_at", r["in_at"], "blown", bl, "state", r["jibstate"])
        if tag == "NEW" and r["kept"]:
            print("      firstwarn", jw, "| captain", cap)
            said = [l for l in r["lines"] if "left on her" in l[3]]
            if "storm" in r["reply"]: print("      REPLY has storm:", r["reply"][-250:])
