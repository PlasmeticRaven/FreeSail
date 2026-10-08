"""Read-only analysis of the builder's FIRST-PASS merchant run (its own dump: every event
and the truth and account at every tick). For each `take a fix` the book's rules made:
which marks it used, how far off they were, whether the mark of the bearing just taken (the
nearest land) was among them, and how far the account stood from the truth before the
bearing-and-fix and after. No game code is run.

usage: fix_vs_bearing.py DUMP_DIR
"""
import json
import math
import statistics
import sys

d = sys.argv[1]
NM = 1852.0


def dist_nm(lat1, lon1, lat2, lon2):
    dn = (lat2 - lat1) * 60.0
    de = (lon2 - lon1) * 60.0 * math.cos(math.radians(0.5 * (lat1 + lat2)))
    return math.hypot(de, dn)


track = {}
with open(f"{d}/5c-merchant.track.txt", encoding="utf-8") as f:
    for line in f:
        p = line.split()
        if len(p) >= 5 and p[3] != "None":
            track[int(p[0])] = tuple(float(x) for x in p[1:5])

events = [json.loads(line) for line in open(f"{d}/5c-merchant.full.jsonl", encoding="utf-8")]
by_tick = {}
for e in events:
    by_tick.setdefault(e["tick"], []).append(e)

rows = []
for tick in sorted(by_tick):
    evs = by_tick[tick]
    fixes = [e for e in evs if e["kind"] == "reckoning.fix"]
    bears = [e for e in evs if e["kind"] == "bearing.taken"]
    if not fixes or tick not in track or tick - 1 not in track:
        continue
    fx = fixes[0]["data"]
    tlat, tlon, alat, alon = track[tick]
    plat, plon, palat, palon = track[tick - 1]
    before = dist_nm(plat, plon, palat, palon)  # account before the bearing and the fix
    fix_err = dist_nm(tlat, tlon, fx["lat_deg"], fx["lon_deg"])
    marks = fx["marks"]
    dists = [dist_nm(tlat, tlon, m["mark_lat_deg"], m["mark_lon_deg"]) for m in marks]
    b = bears[0]["data"] if bears else None
    b_dist = dist_nm(tlat, tlon, b["mark_lat_deg"], b["mark_lon_deg"]) if b else None
    used = bool(b) and any(m["id"] == b["id"] for m in marks)
    rows.append(
        {
            "tick": tick,
            "rule": fixes[0]["actor"],
            "before": before,
            "fix_err": fix_err,
            "sigma": fx.get("sigma_nm"),
            "hat_nm": None if fx.get("hat_m") is None else fx["hat_m"] / NM,
            "n": len(marks),
            "names": [m["name"] for m in marks],
            "dists": dists,
            "bearing_mark": b["name"] if b else None,
            "bearing_dist": b_dist,
            "bearing_moved": b["moved_nm"] if b else None,
            "used": used,
            "fix_moved": fx.get("moved_nm"),
        }
    )


def summary(label, rs):
    if not rs:
        print(f"{label}: none")
        return
    print(f"\n== {label}: {len(rs)} fixes, ticks {rs[0]['tick']} to {rs[-1]['tick']}")
    med = statistics.median
    print(
        f"   account's error BEFORE the bearing and fix: median {med(r['before'] for r in rs):.2f} nm, "
        f"mean {statistics.mean(r['before'] for r in rs):.2f}"
    )
    print(
        f"   the FIX's own error from the truth:          median {med(r['fix_err'] for r in rs):.2f} nm, "
        f"mean {statistics.mean(r['fix_err'] for r in rs):.2f}, worst {max(r['fix_err'] for r in rs):.2f}"
    )
    worse = sum(r["fix_err"] > r["before"] for r in rs)
    print(f"   fixes that left the account WORSE than it was a second before: {worse} of {len(rs)}")
    said = [r["sigma"] for r in rs if r["sigma"] is not None]
    print(f"   the fix's stated doubt ('good to'): median {med(said):.2f} nm")
    over = sum(r["fix_err"] > 2 * r["sigma"] for r in rs if r["sigma"])
    print(f"   fixes whose true error was more than twice their stated doubt: {over} of {len(rs)}")
    bd = [r["bearing_dist"] for r in rs if r["bearing_dist"] is not None]
    if bd:
        print(f"   the bearing's own mark (the nearest land): median {med(bd):.1f} nm off")
    print(
        f"   the fix's marks: median distance {med(x for r in rs for x in r['dists']):.1f} nm; "
        f"nearest of each fix median {med(min(r['dists']) for r in rs):.1f}; farthest median {med(max(r['dists']) for r in rs):.1f}"
    )
    u = sum(r["used"] for r in rs if r["bearing_mark"])
    nb = sum(1 for r in rs if r["bearing_mark"])
    print(f"   the nearest land's mark was one of the fix's marks in {u} of {nb}")
    hats = [r["hat_nm"] for r in rs if r["hat_nm"] is not None]
    if hats:
        print(f"   cocked hats (three-mark fixes, {len(hats)}): median {med(hats):.2f} nm, worst {max(hats):.2f}")


iroise = [r for r in rows if 86000 <= r["tick"] <= 101400]
goulet = [r for r in rows if 111000 <= r["tick"] <= 114000]
falmouth = [r for r in rows if r["tick"] <= 30000]
summary("Falmouth, getting out", falmouth)
summary("the Iroise and the road of Bertheaume (pilot water)", iroise)
summary("the Goulet, to the strike", goulet)
print("\n== a sample from the Iroise: tick | before | fix err | said | hat | bearing's mark (nm) used? | fix's marks (nm)")
for r in iroise[:: max(1, len(iroise) // 14)]:
    marks = ", ".join(f"{n} {x:.1f}" for n, x in zip(r["names"], r["dists"]))
    hat = "  -  " if r["hat_nm"] is None else f"{r['hat_nm']:.2f}"
    print(
        f"   {r['tick']:>6} | {r['before']:.2f} | {r['fix_err']:.2f} | {r['sigma']:.2f} | {hat} | "
        f"{r['bearing_mark']} {r['bearing_dist']:.1f} {'yes' if r['used'] else 'NO '} | {marks}"
    )
