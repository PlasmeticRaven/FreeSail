"""Spar probe: a ship on passage under the game's own captain, a spar carried away by the
game's own means (strain._wreck_spar), minute-by-minute way, aback, astern; the log kept.

    cd <tree> && PYTHONPATH=$PWD python3 -P sparprobe.py OUT.jsonl [-j 4] [--only a,b]

Cases are built in CASES below (ship, spars, wind, events)."""

from __future__ import annotations

import json
import math
import sys
import tempfile
import traceback
from multiprocessing import Pool
from pathlib import Path

PASSAGE = """
name: a passage
seed: 7
start: 1805-06-14T08:00
position: 48 40 N 5 05 W
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: 0
  speed_kn: 5
  glass: true
intent: bound for Falmouth
ports: [falmouth, plymouth, brest]
wind: {{from_deg: {wind_from}, knots: {kn}, gustiness: 0.0, variability: 0.0}}
orders:
  - set plain sail
"""

SHIPS = ["frigate-36", "privateer-schooner", "merchant-brig", "bilander", "hermaphrodite-brig",
         "cutter", "brig", "seventy-four"]
SPARS = {
    "frigate-36": ["main.topmast", "main.topgallant_mast", "fore.topsail.yard", "jib_boom",
                   "fore.topmast.studdingsail_boom.starboard"],
    "privateer-schooner": ["fore.topmast", "fore.topsail.yard", "jib_boom"],
    "merchant-brig": ["main.topmast", "fore.topsail.yard"],
    "bilander": ["fore.topmast", "main.topsail.yard"],
    "hermaphrodite-brig": ["fore.topmast", "fore.topsail.yard", "fore.topmast.studdingsail_boom.starboard"],
    "cutter": ["main.topgallant_mast"],
    "seventy-four": ["main.topmast.studdingsail_boom.starboard"],
    "brig": [],
}


def build_cases():
    cases = []
    for ship in SHIPS:
        for i, spar in enumerate(SPARS[ship]):
            for kn in (12, 25):
                cases.append({"id": f"{ship}|{spar}|{kn}", "ship": ship, "spars": [spar], "kn": kn,
                              "wind_from": 270, "events": []})
            if i == 0:
                # the wind heads her 30 min after: she must tack/wear while the work runs
                cases.append({"id": f"{ship}|{spar}|12head", "ship": ship, "spars": [spar], "kn": 12,
                              "wind_from": 270, "events": [[40, "wind", 20, 12]]})
                # rising wind 20 -> 38 over 30 min starting 30 min after
                cases.append({"id": f"{ship}|{spar}|rise", "ship": ship, "spars": [spar], "kn": 20,
                              "wind_from": 270, "events": [[40, "ramp", 270, 20, 38, 30]]})
    for ship in SHIPS:  # and the same with nothing carried away (all three mends idle)
        cases.append({"id": f"{ship}|none|12", "ship": ship, "spars": [], "kn": 12, "wind_from": 270,
                      "events": []})
    return cases


CASES = build_cases()


def run_case(case):
    from freesail import units
    from freesail.physics import strain as ST
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    rec = {"id": case["id"], "minutes": [], "events": [], "error": None}
    w = None
    try:
        path = Path(tempfile.mkdtemp()) / "p.yaml"
        path.write_text(PASSAGE.format(ship=case["ship"], kn=case["kn"], wind_from=case["wind_from"]))
        sf = load_scenario(str(path))
        w = make_scenario_world(sf)
        begin(w, sf)
        w.run(600)
        for sid in case["spars"]:
            ST._wreck_spar(w.ship, ST.strain_state(w.ship), w.ship.spars[sid], 2.0)
        rec["n0"] = len(w.log)
        x0, y0 = w.ship.dyn.x, w.ship.dyn.y
        ev = {e[0]: e for e in case["events"]}
        ramp = None
        for minute in range(180):
            if minute in ev:
                e = ev[minute]
                if e[1] == "wind":
                    w.wind.follow(units.wrap_2pi(units.deg_to_rad(e[2])), units.knots_to_ms(e[3]))
                elif e[1] == "ramp":
                    ramp = (minute, e[2], e[3], e[4], e[5])
            if ramp is not None and minute <= ramp[0] + ramp[4]:
                kn = ramp[2] + (ramp[3] - ramp[2]) * (minute - ramp[0]) / ramp[4]
                w.wind.follow(units.wrap_2pi(units.deg_to_rad(ramp[1])), units.knots_to_ms(kn))
            w.run(60)
            d = w.ship.dyn
            sq = None
            try:
                p = w.captain.perceive() if hasattr(w.captain, "perceive") else None
                sq = bool(getattr(p, "square_none_drawing", None)) if p is not None else None
            except Exception:
                sq = None
            rec["minutes"].append([round(float(d.u) * 1.943844, 3), round(math.degrees(d.heading) % 360, 1),
                                   round(d.x - x0, 1), round(d.y - y0, 1)])
        rec["sails"] = {sid: [sl.state.name, sl.reefs] for sid, sl in sorted(w.ship.sails.items())}
        rec["spars"] = {sid: bool(sp.wrecked) for sid, sp in sorted(w.ship.spars.items()) if sp.wrecked}
        rec["state"] = getattr(w.captain, "state", None)
    except Exception:
        rec["error"] = traceback.format_exc()[-3000:]
    if w is not None:
        for e in w.log:
            rec["events"].append([e.tick, e.kind, e.severity.value, e.text, str(getattr(e, "actor", ""))])
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
