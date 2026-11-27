import json, sys
cid = sys.argv[3]
for path in sys.argv[1:3]:
    for l in open(path):
        r = json.loads(l)
        if r["id"] != cid: continue
        print("=====", path.split("/")[-1], cid, "end state", r.get("state"))
        m = r["minutes"]
        print("u by 10 min:", [m[i][0] for i in range(0, len(m), 10)])
        kinds = sys.argv[4].split(",") if len(sys.argv) > 4 else None
        for e in r["events"][r["n0"]:]:
            if kinds and not any(k in e[1] for k in kinds) and not any(k in e[4] for k in kinds): continue
            print(f"{(e[0]-600)//60:4d}m {e[1]:22s} {e[3][:170]}")
        print("sails:", {k: v for k, v in r["sails"].items() if v[0] != "FURLED"})
        print("wrecked:", r["spars"])
