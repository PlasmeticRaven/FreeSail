"""Compare two tackmx outputs: python3 -I tmxcmp.py OLD.jsonl NEW.jsonl
'round' is judged from her signed angle off the wind (+ = the new, larboard tack): > 22.5 deg at
the end and at +300 s round; |rel| <= 22.5 in irons; < -22.5 her old tack."""
import json
import sys
from collections import Counter

DECL = {  # (ship) -> rules the brief declares on her
    "hermaphrodite-brig": "A", "privateer-schooner": "A", "topsail-schooner": "A",
    "brig": "C", "merchant-brig": "C", "frigate-36": "D", "razee-44": "D",
}


def load(p):
    out = {}
    for l in open(p):
        r = json.loads(l)
        if "error" in r:
            print("ERROR", p, r["ship"], r["kn"], r["seed"], r["error"][-300:])
            continue
        out[(r["ship"], r["kn"], r["seed"], str(r["hd"]), r["sail"])] = r
    return out


def judge(rel):
    return "round" if rel > 22.5 else ("irons" if rel >= -22.5 else "old")


def summ(r):
    e = r.get("end")
    if r.get("end") == "refused":
        return {"word": "refused", "s": None, "truth": "-", "t300": "-"}
    word = {"ship.tacked": "T", "ship.missed_stays": "M", "evolution.failed": "F", "none": "."}[e["kind"]]
    return {"word": word, "s": e["s"], "truth": judge(e["rel"]), "t300": judge(r["rel300"]),
            "text": e["text"], "minu": round(r["minu_kn"], 1), "stern": r["stern_s"],
            "lost": round(r["helm_kn"] - r["minv_kn"], 1), "rel": round(e["rel"]), "rel300": round(r["rel300"])}


def main():
    old, new = load(sys.argv[1]), load(sys.argv[2])
    keys = sorted(set(old) | set(new), key=str)
    cnt = Counter()
    bad = []
    for k in keys:
        if k not in old or k not in new:
            print("MISSING", k, k in old, k in new)
            continue
        o, n = summ(old[k]), summ(new[k])
        cnt["cells"] += 1
        for tag, s in (("old", o), ("new", n)):
            if s["word"] == "refused":
                cnt[tag + " refused"] += 1
                continue
            made = s["truth"] == "round" and s["t300"] == "round"
            cnt[f"{tag} made"] += made
            if s["word"] == "T" and s["truth"] != "round":
                bad.append((tag, "said Tacked but " + s["truth"], k, s))
            if s["word"] == "M" and s["truth"] == "round":
                bad.append((tag, "said Missed but round", k, s))
            if s["word"] == "T" and s["truth"] == "round" and s["t300"] != "round":
                bad.append((tag, "Tacked, round at end, not at +300 (" + s["t300"] + ")", k, s))
        om = o["word"] != "refused" and o["truth"] == "round" and o["t300"] == "round"
        nm = n["word"] != "refused" and n["truth"] == "round" and n["t300"] == "round"
        if om and not nm:
            bad.append(("new", "TACK LOST", k, {"old": o, "new": n}))
        if nm and not om:
            cnt["tack gained"] += 1
        oline = [x[1:] for x in old[k].get("lines", [])]
        nline = [x[1:] for x in new[k].get("lines", [])]
        same = (o == n) and oline == nline and old[k].get("reply") == new[k].get("reply") \
            and old[k].get("short_reply") == new[k].get("short_reply")
        if not same:
            cnt["changed"] += 1
            d = DECL.get(k[0], "UNDECLARED-SHIP")
            print(f"CHANGED [{d}] {k}: old {o['word']}{o['s']} {o.get('truth')}/{o.get('t300')} "
                  f"rel {o.get('rel')}/{o.get('rel300')} minu {o.get('minu')} stern {o.get('stern')} | "
                  f"new {n['word']}{n['s']} {n.get('truth')}/{n.get('t300')} rel {n.get('rel')}/{n.get('rel300')} "
                  f"minu {n.get('minu')} stern {n.get('stern')}"
                  + ("  SHORT-REPLY DIFFERS" if old[k].get("short_reply") != new[k].get("short_reply") else ""))
    print()
    for b in bad:
        print("FLAG", b[0], b[1], b[2], {kk: b[3].get(kk) for kk in ("word", "s", "rel", "rel300", "text")} if "old" not in b[3] else b[3])
    print()
    for k, v in sorted(cnt.items()):
        print(k, v)
    # outcome table per ship
    tab = Counter()
    for k in keys:
        if k in old and k in new:
            for tag, src in (("O", old), ("N", new)):
                s = summ(src[k])
                tab[(k[0], k[4], tag, s["word"] + ("" if s["word"] == "refused" else ":" + s["truth"]))] += 1
    print()
    for kk in sorted(tab):
        print(kk, tab[kk])


main()
