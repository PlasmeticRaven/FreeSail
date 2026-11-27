"""C's cells followed 20 minutes after the tack's end, no further order (cd <tree>; OUT.jsonl)."""
import sys, json, math
sys.path.insert(0, "/tmp/claude-0/-home-user-FreeSail/e2d459f1-79d4-50d6-9285-0413fe7ccd0b/scratchpad/rev125-probes/gate")
import tackmx
from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from multiprocessing import Pool
CELLS = [("brig", 20, 7, h, s) for h in (290.0, 292.5, 295.0) for s in ("plain", "short")] + \
        [("brig", 20, 11, h, "plain") for h in (290.0, 292.5)] + \
        [("merchant-brig", 20, 11, h, "plain") for h in (292.5, 295.0)] + \
        [("merchant-brig", 20, 7, h, "plain") for h in (295.0, "fb")]
def one(c):
    ship, kn, seed, hd, sail = c
    w = make_world(seed, f"data/ships/{ship}.yaml", Scenario(wind_from_deg=0.0, wind_speed_kn=float(kn), ship_heading_deg=292.5, ship_speed_kn=4.0))
    w.submit("set plain sail"); w.submit("brace sharp up on the starboard tack")
    tackmx.idle(w, 4000); w.submit("trim sails"); tackmx.idle(w, 600)
    for _ in range(60): w.tick()
    if sail == "short":
        w.submit("shorten sail"); w.tick(); tackmx.idle(w, 1500)
        for _ in range(60): w.tick()
    w = tackmx.derive(w, hd)
    n0 = len(w.log); t0 = w.clock.tick
    w.submit("tack ship")
    end = None; samples = []; stern = irons = 0; y0 = w.ship.dyn.y; x0 = w.ship.dyn.x
    for i in range(900 + 1200):
        w.tick(); d = w.ship.dyn
        if end is None:
            if any(e.kind in tackmx.ENDS for e in w.log[n0:]):
                end = i; ye = d.y
        if end is not None:
            if d.u < 0: stern += 1
            if abs(tackmx.rel(w)) <= 22.5: irons += 1
            if (i - end) % 60 == 0:
                samples.append([i - end, round(tackmx.rel(w)), round(units.ms_to_knots(d.u), 1), round(d.y - y0)])
            if i - end >= 1200: break
    return {"cell": c, "end": end, "stern_after": stern, "irons_after": irons, "dy_total": d.y - y0, "dx_total": d.x - x0,
            "samples": samples, "lines": [[e.tick - t0, e.kind, e.text] for e in w.log[n0:] if e.kind not in ("ship.leeway", "strain.warning", "wind.gust")]}
if __name__ == "__main__":
    with Pool(int(sys.argv[2]) if len(sys.argv) > 2 else 2) as p, open(sys.argv[1], "w") as f:
        for r in p.imap_unordered(one, CELLS):
            f.write(json.dumps(r) + "\n"); f.flush()
