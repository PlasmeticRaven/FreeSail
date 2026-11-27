"""Gate 125, D: `shorten sail` with a jib loaded, close-hauled (292.5, wind N) and abeam (270).
    cd <tree> && PYTHONPATH=$PWD python3 -P dprobe.py OUT.jsonl [-j N] [--hour CELLS.json]
Phase 1 (default): every ship with a jib, winds 20/25/30/35/40, seeds 7 and 11: the settle, the
order's reply, every jib's load/rating at the order, the jibs set 15 min on. With --hour, the
cells listed run an hour after the order (helm, heading, jib loads, strain/blow-out/carry-away
lines), then the wind risen 10 kn, 5 min, a second `shorten sail`, 10 min: the jibs set."""
from __future__ import annotations

import glob
import json
import math
import os
import sys
import traceback
from multiprocessing import Pool

WINDS = (20, 25, 30, 35, 40)
HEADS = {"close": 292.5, "abeam": 270.0}
SEEDS = (7,)


def idle(w, limit):
    for i in range(limit):
        r = w.ship.extra.get("evolutions")
        if not getattr(r, "instances", None):
            return i
        w.tick()
    return limit


def jibs(w):
    s = w.ship
    out = []
    for sid in s.groups.get("jibs") or []:
        sl = s.sails.get(sid)
        if sl is None:
            continue
        r = sl.effective_cloth_rating_kn
        out.append([sid, sl.state.name, round(sl.load_kn / r, 3) if r > 0 else None])
    return out


def cell(key, hour=False):
    ship, how, kn, seed = key
    from freesail import units
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    rec = {"ship": ship, "how": how, "kn": kn, "seed": seed}
    try:
        w = make_world(seed, f"data/ships/{ship}.yaml",
                       Scenario(wind_from_deg=0.0, wind_speed_kn=float(kn), ship_heading_deg=HEADS[how],
                                ship_speed_kn=4.0))
        w.submit("set plain sail")
        w.submit("brace sharp up on the starboard tack" if how == "close" else "trim sails")
        idle(w, 4000)
        w.submit("trim sails")
        idle(w, 600)
        for _ in range(60):
            w.tick()
        rec["jibs_at_order"] = jibs(w)
        rec["helm_at_order"] = math.degrees(w.ship.dyn.weather_helm)
        try:
            from freesail.orders import storm
            t, k = storm.loaded_jibs(w.ship)
            rec["kept"] = [s.id for s in k]
            rec["taken"] = [s.id for s in t]
            rec["helm_without"] = [math.degrees(storm.helm_without(w.ship, [s])) for s in k + t]
        except AttributeError:
            pass
        n0 = len(w.log)
        t0 = w.clock.tick
        rep = w.submit("shorten sail")
        rec["reply"] = rep.text
        secs = 3600 if hour else 900
        helm, off, minu = [], [], 99
        jmax = {}
        for i in range(secs):
            w.tick()
            d = w.ship.dyn
            if i % 10 == 0:
                helm.append(math.degrees(d.weather_helm))
                off.append(abs(math.degrees(units.wrap_pi(d.heading - w.wind.direction_from))))
                for sid, st, ld in jibs(w):
                    if ld is not None and st == "SET":
                        jmax[sid] = max(jmax.get(sid, 0), ld)
            minu = min(minu, d.u)
        rec["jibs_end"] = jibs(w)
        rec["helm_max"] = max(helm) if helm else None
        rec["helm_mean_last30"] = sum(helm[-180:]) / max(1, len(helm[-180:]))
        rec["off_min"], rec["off_max"] = min(off), max(off)
        rec["off_mean_last30"] = sum(off[-180:]) / max(1, len(off[-180:]))
        rec["minu_kn"] = units.ms_to_knots(minu)
        rec["jib_load_max_set"] = jmax
        rec["speed_end"] = units.ms_to_knots(w.ship.dyn.speed)
        rec["lines"] = [[e.tick - t0, e.kind, e.severity.value, e.text] for e in w.log[n0:]]
        if hour:
            w.wind.follow(w.wind.direction_from, units.knots_to_ms(kn + 10.0))
            for _ in range(300):
                w.tick()
            n1 = len(w.log)
            rec["jibs_before_second"] = jibs(w)
            rep2 = w.submit("shorten sail")
            rec["reply2"] = rep2.text
            for _ in range(600):
                w.tick()
            rec["jibs_after_second"] = jibs(w)
            rec["lines2"] = [[e.tick - t0, e.kind, e.severity.value, e.text] for e in w.log[n1:]]
    except Exception:
        rec["error"] = traceback.format_exc()[-2000:]
    return rec


def _hour(key):
    return cell(key, True)


def main():
    out = sys.argv[1]
    a = sys.argv[2:]
    j = int(a[a.index("-j") + 1]) if "-j" in a else 4
    if "--hour" in a:
        keys = [tuple(k) for k in json.load(open(a[a.index("--hour") + 1]))]
        fn = _hour
    else:
        import yaml
        ships = []
        for f in sorted(glob.glob("data/ships/*.yaml")):
            d = yaml.safe_load(open(f))
            if (d.get("groups") or {}).get("jibs"):
                ships.append(os.path.basename(f)[:-5])
        keys = [(s, h, k, sd) for s in ships for h in HEADS for k in WINDS for sd in SEEDS]
        fn = cell
    with open(out, "w") as f, Pool(j) as p:
        for r in p.imap_unordered(fn, keys):
            f.write(json.dumps(r) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
