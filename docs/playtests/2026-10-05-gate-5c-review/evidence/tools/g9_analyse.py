"""Read-only analysis of replay_probe.py's output for the m5c-c game (the brig, Falmouth to
Roscoff to Brest). Reads PREFIX.series.jsonl and PREFIX.events.jsonl; runs no game code.

usage: g9_analyse.py PREFIX [section ...]   sections: overall fixes bearings sights doubt hove goulet anchor
"""
import bisect
import json
import math
import statistics
import sys

pre = sys.argv[1]
want = set(sys.argv[2:]) or {"overall", "fixes", "bearings", "sights", "doubt", "hove", "goulet", "anchor"}
S = [json.loads(x) for x in open(pre + ".series.jsonl", encoding="utf-8")]
S = [r for r in S if "err" in r]
E = [json.loads(x) for x in open(pre + ".events.jsonl", encoding="utf-8")]
ticks = [r["tick"] for r in S]


def at(t):
    """The series sample at or just before tick t."""
    i = bisect.bisect_right(ticks, t) - 1
    return S[max(i, 0)]


def before(t):
    i = bisect.bisect_left(ticks, t) - 1
    return S[max(i, 0)]


def nm(lat1, lon1, lat2, lon2):
    dn = (lat2 - lat1) * 60.0
    de = (lon2 - lon1) * 60.0 * math.cos(math.radians(0.5 * (lat1 + lat2)))
    return math.hypot(de, dn)


def clock(t):
    # the game began 1805-06-12 05:00
    s = 5 * 3600 + t
    d = 12 + s // 86400
    s %= 86400
    return f"{d} Jun {s // 3600:02d}:{(s % 3600) // 60:02d}"


def stats(v):
    v = sorted(v)
    if not v:
        return "none"
    n = len(v)
    return (
        f"median {v[n // 2]:.2f}, mean {statistics.mean(v):.2f}, 9 in 10 under {v[int(0.9 * (n - 1))]:.2f}, "
        f"worst {v[-1]:.2f}; over 1 nm {sum(x > 1 for x in v) / n:.0%}, over 3 nm {sum(x > 3 for x in v) / n:.0%}"
    )


def rel(r):
    """Wind relative to her head, degrees: + on the starboard side, - on the larboard."""
    return ((r["wind_from"] - r["head"] + 180.0) % 360.0) - 180.0


if "overall" in want:
    print("== THE ACCOUNT'S ERROR FROM THE TRUTH (miles), a sample a minute")
    print("   whole game:", stats([r["err"] for r in S]))
    for lo, hi, what in (
        (0, 86400, "Falmouth to the Bas landfall (owner alone, open Channel)"),
        (86400, 131000, "the landfall to anchor at Roscoff (owner alone)"),
        (131000, 185400, "at anchor, Roscoff"),
        (185400, 199800, "out of Roscoff along the coast (officer conning)"),
        (199800, 212400, "four hours of fog, standing off"),
        (212400, 255600, "round Ushant by night"),
        (255600, 277300, "into the Iroise"),
        (277300, 298900, "hove to in fog, six hours"),
        (298900, 327600, "light airs and calm off Ar Men"),
        (327600, 370800, "working east on the flood and ebb"),
        (370800, 386000, "noon to the mouth of the Goulet"),
        (386000, 387700, "the Goulet to the first anchor"),
        (387700, 417900, "at anchor in the Goulet"),
        (417900, 422400, "the Goulet to Brest road"),
    ):
        v = [r["err"] for r in S if lo <= r["tick"] < hi]
        print(f"   {what:<58} {stats(v)}")

if "fixes" in want:
    F = [e for e in E if e["kind"] == "reckoning.fix"]
    print(f"\n== THE FIXES ({len(F)})")
    worse = 0
    rows = []
    for e in F:
        b = before(e["tick"])
        d = e.get("data") or {}
        marks = d.get("marks") or []
        dist = [nm(e["t_lat"], e["t_lon"], m["mark_lat_deg"], m["mark_lon_deg"]) for m in marks]
        fix_err = nm(e["t_lat"], e["t_lon"], d.get("lat_deg", e["a_lat"]), d.get("lon_deg", e["a_lon"]))
        rows.append((e["tick"], b["err"], fix_err, d.get("sigma_nm"), d.get("hat_m"), len(marks), dist, e["actor"], [m["name"] for m in marks]))
        if fix_err > b["err"]:
            worse += 1
    print("   the account before each fix:", stats([r[1] for r in rows]))
    print("   the fix's own error:        ", stats([r[2] for r in rows]))
    print(f"   fixes that left the account worse than it was: {worse} of {len(rows)}")
    said = [r[3] for r in rows if r[3]]
    print(f"   'good to' (stated doubt): median {statistics.median(said):.2f} nm; true error over twice the stated doubt in {sum(r[2] > 2 * r[3] for r in rows if r[3])} of {len(said)}")
    print(f"   marks' distance: median {statistics.median(x for r in rows for x in r[6]):.1f} nm; nearest mark of each fix median {statistics.median(min(r[6]) for r in rows if r[6]):.1f}")
    print("   tick | when | by | account before | fix error | said | hat nm | marks (nm off)")
    for r in rows:
        hat = "  -  " if r[4] is None else f"{r[4] / 1852:.2f}"
        who = "capt" if r[7] == "captain" else ("offr" if "officer" in r[7] else "book")
        marks = ", ".join(f"{n} {x:.1f}" for n, x in zip(r[8], r[6]))
        flag = "  WORSE" if r[2] > r[1] else ""
        print(f"   {r[0]:>6} | {clock(r[0])} | {who} | {r[1]:.2f} | {r[2]:.2f} | {r[3]} | {hat} | {marks}{flag}")

if "bearings" in want:
    B = [e for e in E if e["kind"] == "bearing.taken"]
    print(f"\n== THE BEARINGS ({len(B)}); those whose distance was laid down, or that moved the account over half a mile")
    ap = [e for e in B if (e.get("data") or {}).get("distance_applied")]
    print(f"   distance laid down in {len(ap)} of {len(B)}")
    better = 0
    for e in B:
        d = e.get("data") or {}
        b = before(e["tick"])
        if d.get("distance_applied") or (d.get("moved_nm") or 0) > 0.5:
            mark_nm = nm(e["t_lat"], e["t_lon"], d["mark_lat_deg"], d["mark_lon_deg"])
            est = (d.get("estimate_m") or 0) / 1852
            if e["err"] < b["err"]:
                better += 1
            print(
                f"   {e['tick']:>6} {clock(e['tick'])} {d.get('name', '?'):<24} true {mark_nm:5.1f} nm, judged {est:5.1f}; "
                f"account error {b['err']:.2f} -> {e['err']:.2f}; doubt E/N {b['sig_e']:.2f}/{b['sig_n']:.2f} -> {e['sig_e']:.2f}/{e['sig_n']:.2f}; "
                f"{'LAID DOWN' if d.get('distance_applied') else 'line only'}"
            )
    print(f"   of these, the account was the truer afterwards in {better}")

if "sights" in want:
    print("\n== THE SIGHTS: noon latitudes and the lunar")
    for e in E:
        if e["kind"] in ("reckoning.noon", "reckoning.lunar"):
            b = before(e["tick"])
            a = at(e["tick"] + 60)
            print(f"   {e['tick']:>6} {clock(e['tick'])} {e['kind']}: {e['text'][:150]}")
            print(
                f"          truth {e['t_lat']:.3f} N {abs(e['t_lon']):.3f} W; account before {b['a_lat']:.3f} N {abs(b['a_lon']):.3f} W (error {b['err']:.2f}: {b['err_e']:+.2f} E, {b['err_n']:+.2f} N; doubt E/N {b['sig_e']:.2f}/{b['sig_n']:.2f}; run since obs {b['run_fix']})"
            )
            print(
                f"          account after  {e['a_lat']:.3f} N {abs(e['a_lon']):.3f} W (error {e['err']:.2f}: {e['err_e']:+.2f} E, {e['err_n']:+.2f} N; doubt E/N {e['sig_e']:.2f}/{e['sig_n']:.2f})"
            )

if "doubt" in want:
    print("\n== THE MASTER'S DOUBT AGAINST THE TRUE ERROR, at moments (doubt = one sigma east / north, miles)")
    for lo, hi, step, what in (
        (199800, 212460, 1800, "fog 12:00-16:00 on 14 June, standing off under sail"),
        (277320, 300000, 1800, "hove to in fog 10:00-16:00 on 15 June, then the Beniguet bearing at 299,944"),
        (306000, 328000, 1800, "becalmed off Ar Men, the deep-sea lead every glass"),
        (356400, 371000, 1800, "the ebb, forenoon of 16 June, to the noon sight"),
    ):
        print(f"   -- {what}")
        for t in range(lo, hi, step):
            r = at(t)
            print(
                f"      {r['tick']:>6} {clock(r['tick'])}  error {r['err']:5.2f} ({r['err_e']:+.2f} E, {r['err_n']:+.2f} N)   doubt {r['sig_e']:.2f} / {r['sig_n']:.2f}   run since last observation {r['run_fix']:5.2f}   way {r['u_kn']} kn"
            )
    print("   -- observations in those windows that changed the doubt (kind, doubt before -> after, error before -> after)")
    for e in E:
        if e["kind"] in ("sounding", "bearing.taken", "reckoning.fix", "reckoning.noon") and (277320 <= e["tick"] <= 328000):
            b = before(e["tick"])
            a = at(e["tick"] + 60)
            if abs(a["sig_e"] - b["sig_e"]) > 0.05 or abs(a["sig_n"] - b["sig_n"]) > 0.05 or abs(a["err"] - b["err"]) > 0.3:
                print(
                    f"      {e['tick']:>6} {clock(e['tick'])} {e['kind']:<14} doubt {b['sig_e']:.2f}/{b['sig_n']:.2f} -> {a['sig_e']:.2f}/{a['sig_n']:.2f}; error {b['err']:.2f} -> {a['err']:.2f}; {e['text'][:90]}"
                )

if "hove" in want:
    print("\n== HOVE TO: her head against the wind (wind relative to her head: + starboard side, - larboard; 0 = head to wind)")
    eps = []
    cur = None
    for r in S:
        if r["hove"] and cur is None:
            cur = [r]
        elif r["hove"] and cur is not None:
            cur.append(r)
        elif not r["hove"] and cur is not None:
            eps.append(cur)
            cur = None
    if cur:
        eps.append(cur)
    for ep in eps:
        if ep[-1]["tick"] - ep[0]["tick"] < 300:
            continue
        rels = [rel(r) for r in ep]
        # crossings of head-to-wind (sign change with |rel| small) and of stern-to-wind
        thru_head = sum(1 for a, b in zip(rels, rels[1:]) if a * b < 0 and abs(a) < 90 and abs(b) < 90)
        thru_stern = sum(1 for a, b in zip(rels, rels[1:]) if a * b < 0 and abs(a) > 90 and abs(b) > 90)
        wk = [r["wind_kn"] for r in ep]
        anch = "  (AT ANCHOR or moored: the record carried over)" if max(abs(r["u_kn"] or 0) for r in ep) < 0.05 else ""
        print(
            f"   {ep[0]['tick']:>6} to {ep[-1]['tick']:>6} ({clock(ep[0]['tick'])}, {(ep[-1]['tick'] - ep[0]['tick']) / 3600:.1f} h), wind {min(wk):.0f}-{max(wk):.0f} kn: "
            f"through head-to-wind {thru_head} times, stern through the wind {thru_stern} times{anch}"
        )
        line = []
        for r in ep[:: max(1, len(ep) // 16)][:17]:
            line.append(f"{(r['tick'] - ep[0]['tick']) // 60}m:{rel(r):+.0f}")
        print("          minutes:wind-on-bow  " + "  ".join(line))

if "goulet" in want:
    print("\n== THE GOULET (16 June, 16:10 to the first anchor)")
    ming = next((e["data"] for e in E if e["kind"] == "bearing.taken" and (e.get("data") or {}).get("id", "").startswith("mingan")), None)
    if ming is None:
        ming = next((m for e in E if e["kind"] == "reckoning.fix" for m in (e["data"].get("marks") or []) if "ingan" in m["name"]), None)
    if ming:
        mlat, mlon = ming["mark_lat_deg"], ming["mark_lon_deg"]
        best = min((nm(r["t_lat"], r["t_lon"], mlat, mlon), r["tick"]) for r in S if 385000 <= r["tick"] <= 388000)
        print(f"   the Mingan at {mlat:.4f} N {abs(mlon):.4f} W: nearest truth {best[0] * 10:.1f} cables at tick {best[1]} ({clock(best[1])})")
        for t in range(386400, 387721, 120):
            r = at(t)
            print(
                f"      {r['tick']} {clock(r['tick'])}  Mingan true {nm(r['t_lat'], r['t_lon'], mlat, mlon) * 10:4.1f} cables, by the account {nm(r['a_lat'], r['a_lon'], mlat, mlon) * 10:4.1f}; account error {r['err'] * 10:4.1f} cables; way {r['u_kn']} kn, wind {r['wind_kn']} kn"
            )
    for e in E:
        if 386200 <= e["tick"] <= 387700 and e["kind"] in ("reckoning.fix", "bearing.taken", "lookout.land_ahead"):
            b = before(e["tick"])
            print(f"   {e['tick']} {e['kind']:<18} error {b['err'] * 10:.1f} -> {e['err'] * 10:.1f} cables | {e['text'][:140]}")

if "anchor" in want:
    print("\n== AT ANCHOR: did she move when the anchors were said to drag?")
    for lo, hi, what in ((130800, 131400, "Roscoff, coming to"), (169300, 170200, "Roscoff, weighing in fog"), (387700, 417900, "the Goulet"), (422400, 423000, "Brest road")):
        seg = [r for r in S if lo <= r["tick"] <= hi]
        if not seg:
            continue
        r0 = seg[0]
        far = max(nm(r0["t_lat"], r0["t_lon"], r["t_lat"], r["t_lon"]) for r in seg)
        path = sum(nm(a["t_lat"], a["t_lon"], b["t_lat"], b["t_lon"]) for a, b in zip(seg, seg[1:]))
        n = sum(1 for e in E if e["kind"] == "anchor.dragging" and lo <= e["tick"] <= hi)
        print(f"   {what}: {n} dragging lines; she ended {nm(r0['t_lat'], r0['t_lon'], seg[-1]['t_lat'], seg[-1]['t_lon']) * 10:.1f} cables from where she began, farthest {far * 10:.1f}, path {path * 10:.1f} cables")
    print("   the Goulet, each dragging line and how far she moved over the ground in the ten minutes after it:")
    for e in E:
        if e["kind"] in ("anchor.dragging", "ship.anchored", "ship.swung") and 387700 <= e["tick"] <= 417900:
            a = at(e["tick"])
            b = at(e["tick"] + 600)
            print(f"      {e['tick']} {clock(e['tick'])} {e['kind']:<16} moved {nm(a['t_lat'], a['t_lon'], b['t_lat'], b['t_lon']) * 10:4.1f} cables in 10 min | {e['text'][:70]} | data {json.dumps(e.get('data'))[:160]}")
