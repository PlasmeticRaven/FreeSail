"""Read-only: from the builder's dumps of the merchant passage (before 37d, first pass,
final), the account's error from the truth on the two pilot-water legs, tick by tick, and
just after each firing of the book's five-minute 'pilot water' rule. No game code is run.

usage: legs_compare.py SCRATCH_37D_DIR
"""
import json
import math
import statistics
import sys

base = sys.argv[1]


def dist_nm(lat1, lon1, lat2, lon2):
    dn = (lat2 - lat1) * 60.0
    de = (lon2 - lon1) * 60.0 * math.cos(math.radians(0.5 * (lat1 + lat2)))
    return math.hypot(de, dn)


def load(tag):
    track = {}
    with open(f"{base}/{tag}/5c-merchant.track.txt", encoding="utf-8") as f:
        for line in f:
            p = line.split()
            if len(p) >= 5 and p[3] != "None":
                v = [float(x) for x in p[1:5]]
                track[int(p[0])] = dist_nm(*v)
    events = [json.loads(x) for x in open(f"{base}/{tag}/5c-merchant.full.jsonl", encoding="utf-8")]
    return track, events


def stats(vals):
    vals = sorted(vals)
    if not vals:
        return "none"
    n = len(vals)
    return (
        f"median {vals[n // 2]:.2f}, mean {statistics.mean(vals):.2f}, "
        f"9 in 10 under {vals[int(0.9 * (n - 1))]:.2f}, worst {vals[-1]:.2f}"
    )


for tag, label in (("before", "BEFORE 37d"), ("after", "FIRST PASS (bearing then fix)"), ("after5", "FINAL (bearing alone in pilot water)")):
    track, events = load(tag)
    road = next(e["tick"] for e in events if e["kind"] == "ship.anchored" and e["tick"] > 86400)
    under = next(
        (e["tick"] for e in events if e["kind"] in ("ship.under_way", "ship.weighed") and e["tick"] > road),
        None,
    )
    end = next(
        (e["tick"] for e in events if e["kind"] in ("ship.anchored", "ship.aground") and under and e["tick"] > under),
        None,
    )
    print(f"\n== {label}")
    leg1 = [track[t] for t in range(86400, road) if t in track]
    print(f"   the Iroise to the road of Bertheaume (ticks 86400 to {road}): {stats(leg1)}")
    if under and end:
        leg2 = [track[t] for t in range(under, end) if t in track]
        what = next(e["kind"] for e in events if e["tick"] == end and e["kind"] in ("ship.anchored", "ship.aground"))
        print(f"   the Goulet (under way {under} to {what} {end}): {stats(leg2)}")
    fired = sorted(
        {
            e["tick"]
            for e in events
            if e["actor"] == "standing order 'pilot water'" and e["kind"] in ("bearing.taken", "reckoning.fix")
        }
    )
    a = [track[t] for t in fired if 86400 <= t < road and t in track]
    b = [track[t] for t in fired if under and end and under <= t < end and t in track]
    print(f"   just after each firing of the five-minute rule, Iroise leg ({len(a)}): {stats(a)}")
    print(f"   just after each firing of the five-minute rule, Goulet leg ({len(b)}): {stats(b)}")
    kinds = {}
    for e in events:
        if e["actor"] == "standing order 'pilot water'":
            kinds[e["kind"]] = kinds.get(e["kind"], 0) + 1
    print(f"   the rule's lines: {kinds}")
