"""Fog scan: the World's own minute weather (`_tick_weather`) driven without the ship's
physics, the clock advanced a minute at a time and the ship's point moved along a track at
a set speed. Records every minute's weather/visibility/fog degree and every weather line.

    cd <tree> && PYTHONPATH=$PWD python3 -P fogscan.py OUT.jsonl [-j 4]
"""

from __future__ import annotations

import json
import math
import sys
import traceback
from datetime import datetime
from multiprocessing import Pool

CASES = []
import os
CASE_DAYS = float(os.environ.get("FOG_DAYS", 10))
CASE_DAYS2 = float(os.environ.get("FOG_DAYS2", 20))
# climatology, June, several seeds, a ship working along the coast off Falmouth/Lizard at 6 kn
for seed in (3, 7, 11, 19, 23, 42, 57, 77):
    for start_day in (1, 15):
        CASES.append({"id": f"clim-s{seed}-d{start_day}", "seed": seed, "kind": "clim",
                      "start": datetime(1805, 6, start_day, 0, 0).isoformat(), "days": CASE_DAYS,
                      "lat": 50.05, "lon": -5.0, "speed_kn": 6.0})
# the test's high over the channel, standing off Falmouth (still) and sailing (6 kn)
for seed in (7, 8, 9):
    for spd in (0.0, 6.0):
        CASES.append({"id": f"high-s{seed}-v{int(spd)}", "seed": seed, "kind": "high",
                      "start": datetime(1805, 6, 1, 0, 0).isoformat(), "days": CASE_DAYS2,
                      "lat": 50.12, "lon": -5.03, "speed_kn": spd})


def make(case):
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    start = datetime.fromisoformat(case["start"])
    kw = dict(start_time=start, wind_from_deg=270.0, wind_speed_kn=8.0, gustiness=0.0,
              variability=0.0, position={"lat_deg": case["lat"], "lon_deg": case["lon"]},
              region="channel-west")
    if case["kind"] == "clim":
        kw["climatology"] = True
    else:
        kw["systems"] = [{"name": "the high", "kind": "high", "radius_km": 1200,
                          "track": [{"at": start.isoformat(), "x_km": 0, "y_km": 0, "hpa": 1028}]}]
    return make_world(case["seed"], "data/ships/topsail-schooner.yaml", Scenario(**kw))


def run_case(case):
    rec = {"id": case["id"], "minutes": [], "lines": [], "error": None}
    try:
        w = make(case)
        n0 = len(w.log)
        v = case["speed_kn"] * 0.514444 * 60.0  # metres a minute
        # a track: east 20 km, south 10, west 20, north 10, ... (a box off the coast)
        legs = [(90, 20000), (180, 10000), (270, 20000), (0, 10000)]
        leg, done = 0, 0.0
        for m in range(int(case["days"] * 1440)):
            w.clock.tick += 60
            if v > 0:
                b, L = legs[leg % 4]
                w.ship.dyn.x += v * math.sin(math.radians(b))
                w.ship.dyn.y += v * math.cos(math.radians(b))
                done += v
                if done >= L:
                    leg, done = leg + 1, 0.0
            w._tick_weather()
            c = w.conditions
            rec["minutes"].append([c.weather, c.visibility, float(getattr(c, "fog", 0.0) or 0.0), c.sector])
        for e in w.log[n0:]:
            if e.kind.startswith("weather"):
                minute = e.tick // 60
                rec["lines"].append([minute, e.kind, e.severity.value, e.text])
    except Exception:
        rec["error"] = traceback.format_exc()[-3000:]
    return rec


def main(argv):
    out = argv[0]
    jobs = int(argv[argv.index("-j") + 1]) if "-j" in argv else 1
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    cases = [c for c in CASES if not only or any(c["id"].startswith(o) for o in only)]
    with open(out, "w") as f, Pool(jobs) as pool:
        for rec in pool.imap_unordered(run_case, cases):
            f.write(json.dumps(rec) + "\n")
            f.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
