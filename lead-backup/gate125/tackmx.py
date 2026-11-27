"""Gate 125: the tack matrix. Run from inside a tree:
    cd <tree> && PYTHONPATH=$PWD python3 -P tackmx.py OUT.jsonl [-j 4] [--only ship,ship]
One line per cell: ship, wind, seed, heading, sail (plain/short), the tack's end (kind, text,
seconds), her signed angle off the wind (deg, + = wind on her larboard side, i.e. round) at the
end and at +300 s, the least headway (sternway), the way at the helm's a-lee and the least way,
seconds with sternway, and every log line from the order to +300 s. A world settled once per
(ship, wind, seed, heading) and deep-copied for the shortened cell. Default gusts (0.3/0.3)."""
from __future__ import annotations

import copy
import glob
import json
import math
import os
import sys
import traceback
from multiprocessing import Pool

ENDS = ("ship.tacked", "ship.missed_stays", "evolution.failed")
WINDS = (8, 12, 15, 20, 25, 30)
HEADINGS = (290.0, 292.5, 295.0, "fb")
SEEDS = (7, 11)


def rel(w):
    from freesail import units
    return math.degrees(units.wrap_pi(w.ship.dyn.heading - w.wind.direction_from))


def idle(w, limit, trim_every=0):
    for i in range(limit):
        r = w.ship.extra.get("evolutions")
        if not getattr(r, "instances", None):
            return i
        w.tick()
        if trim_every and i % trim_every == trim_every // 2:
            w.submit("trim sails")
    return limit


def tack(w):
    from freesail import units
    start = w.clock.tick
    nlog = len(w.log)
    rep = w.submit("tack ship")
    out = {"reply_kind": rep.kind, "reply": rep.text}
    if rep.kind == "order.rejected":
        out["end"] = "refused"
        return out
    minu, stern, minv, helm_v = 99.0, 0, 99.0, None
    end = None
    for i in range(900 + 300):
        w.tick()
        d = w.ship.dyn
        minu = min(minu, d.u)
        minv = min(minv, d.speed)
        if d.u < 0:
            stern += 1
        if helm_v is None:
            for inst in getattr(w.ship.extra.get("evolutions"), "instances", []) or []:
                sv = getattr(inst.script, "speed_at_helm", None)
                if sv:
                    helm_v = sv
        if end is None:
            done = [e for e in w.log[nlog:] if e.kind in ENDS]
            if done:
                end = {"kind": done[0].kind, "text": done[0].text, "sev": done[0].severity.value,
                       "s": w.clock.tick - start, "rel": rel(w)}
                t_end = i
        if end is not None and i >= t_end + 300:
            break
        if end is None and i >= 899:
            end = {"kind": "none", "text": "", "s": 900, "rel": rel(w)}
            t_end = i
    out.update(end=end, rel300=rel(w), minu_kn=units.ms_to_knots(minu),
               stern_s=stern, helm_kn=units.ms_to_knots(helm_v or 0), minv_kn=units.ms_to_knots(minv),
               lines=[[e.tick - start, e.kind, e.text] for e in w.log[nlog:]])
    return out


def clone(w):
    """A copy by the checkpoint's own pickling, its hooks rebound (deepcopy leaves the ship's
    note hook on the original world)."""
    from freesail.core.replay import trial_copy
    c = trial_copy(w, raising=True)
    c.__dict__.pop("dry_run", None)
    return c


def derive(base, hd):
    from freesail import units
    w = clone(base)
    if hd == "fb":
        w.submit("keep her full and by")
        for _ in range(300):
            w.tick()
    else:
        h = units.deg_to_rad(hd)
        w.ship.dyn.heading = h
        w.ship.dyn.target_heading = h
        for _ in range(90):
            w.tick()
    return w


def group(key):
    """One settle per (ship, wind, seed) at 292.5; the starting headings 290, 292.5, 295 by her
    head and the helm's target set there and 90 s run, and full and by (300 s); the shortened
    cells from one `shorten sail` of the settled world, run to its end and 60 s."""
    ship, kn, seed = key
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    res = []
    try:
        w = make_world(seed, f"data/ships/{ship}.yaml",
                       Scenario(wind_from_deg=0.0, wind_speed_kn=float(kn), ship_heading_deg=292.5,
                                ship_speed_kn=4.0))
        w.submit("set plain sail")
        w.submit("brace sharp up on the starboard tack")
        idle(w, 4000)
        w.submit("trim sails")
        idle(w, 600)
        for _ in range(60):
            w.tick()
        ws = clone(w)
        rep = ws.submit("shorten sail")
        ws.tick()
        idle(ws, 1500)
        for _ in range(60):
            ws.tick()
        for sail, base in (("plain", w), ("short", ws)):
            for hd in HEADINGS:
                if hd == "fb" and seed != 7:
                    continue
                r = tack(derive(base, hd))
                r.update(ship=ship, kn=kn, seed=seed, hd=hd, sail=sail)
                if sail == "short":
                    r["short_reply"] = rep.text
                res.append(r)
    except Exception:
        res.append({"ship": ship, "kn": kn, "seed": seed, "error": traceback.format_exc()})
    return res


def main():
    out = sys.argv[1]
    j = 4
    only = None
    a = sys.argv[2:]
    if "-j" in a:
        j = int(a[a.index("-j") + 1])
    if "--only" in a:
        only = a[a.index("--only") + 1].split(",")
    ships = sorted(os.path.basename(f)[:-5] for f in glob.glob("data/ships/*.yaml"))
    if only:
        ships = [s for s in ships if s in only]
    keys = [(s, k, sd) for s in ships for k in WINDS for sd in SEEDS]
    with open(out, "w") as f, Pool(j) as p:
        for rs in p.imap_unordered(group, keys):
            for r in rs:
                f.write(json.dumps(r) + "\n")
            f.flush()


if __name__ == "__main__":
    main()
