"""Gate 125 r3, D: the jib kept, an hour on, player (no intent) and captain (intent set), the wind
rising 12 kn over the hour, default gusts. cd <tree>; PYTHONPATH=$PWD python3 -P dprobe2.py OUT -j N"""
import json, sys, traceback
from datetime import datetime
from multiprocessing import Pool
CELLS = [(s, h, k, sd) for (s, h, k, sd) in [
    ("brig", "close", 30, 7), ("brig", "close", 30, 11), ("brig", "close", 35, 7),
    ("hermaphrodite-brig", "close", 30, 11), ("hermaphrodite-brig", "close", 35, 7),
    ("razee-44", "close", 28, 11), ("razee-44", "close", 30, 11), ("frigate-36", "close", 25, 11),
    ("frigate-36", "close", 25, 7), ("corvette-20", "close", 25, 7), ("corvette-20", "close", 25, 11),
    ("privateer-schooner", "abeam", 40, 7), ("topsail-schooner", "abeam", 40, 7),
    ("seventy-four", "close", 30, 7), ("sixty-four", "close", 30, 7), ("merchant-brig", "close", 30, 7)]]
def one(key):
    ship, how, kn, seed = key[:4]; mode = key[4]
    from freesail import units
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    rec = {"key": list(key)}
    try:
        sc = Scenario(start_time=datetime(1805, 6, 12, 10, 0), wind_from_deg=0.0, wind_speed_kn=float(kn),
                      ship_heading_deg=292.5 if how == "close" else 270.0, ship_speed_kn=4.0,
                      position={"lat_deg": 48.5, "lon_deg": -7.5}, region="channel-west", ports=["falmouth", "plymouth", "brest"])
        w = make_world(seed, f"data/ships/{ship}.yaml", sc)
        w.submit("set plain sail"); w.submit("brace sharp up on the starboard tack" if how == "close" else "trim sails")
        for limit in (4000, 600):
            for _ in range(limit):
                if not getattr(w.ship.extra.get("evolutions"), "instances", None): break
                w.tick()
            if limit == 4000: w.submit("trim sails")
        w.run(60)
        n0 = len(w.log)
        r = w.submit("shorten sail"); rec["reply"] = r.text
        rec["kept"] = "left on her" in r.text
        if mode == "captain":
            w.captain.set_intent("passage to 49 30 N 7 30 W")
        jibs = [sid for sid in (w.ship.groups.get("jibs") or []) if sid in w.ship.sails]
        most = {}; in_at = {}; first_warn = {}
        for i in range(3600):
            if i % 60 == 0:
                w.wind.follow(w.wind.direction_from, units.knots_to_ms(kn + 12.0 * i / 3600.0))
            w.tick()
            for sid in jibs:
                sl = w.ship.sails[sid]
                if sl.is_set and sl.effective_cloth_rating_kn > 0:
                    most[sid] = max(most.get(sid, 0), sl.load_kn / sl.effective_cloth_rating_kn)
                elif sid not in in_at:
                    in_at[sid] = i
        lines = [[e.tick, e.kind, e.subject, e.text] for e in w.log[n0:]]
        t0 = lines[0][0] if lines else 0
        rec["lines"] = [[l[0] - t0] + l[1:] for l in lines if l[1] not in ("ship.leeway", "wind.gust", "clock.bell")]
        rec["most"] = most; rec["in_at"] = in_at
        rec["blown"] = [l for l in rec["lines"] if l[1] == "sail.blown_out"]
        rec["jibwarn"] = [l for l in rec["lines"] if l[1] == "strain.warning" and l[2] in jibs][:3]
        rec["jibstate"] = {sid: w.ship.sails[sid].state.name for sid in jibs}
    except Exception:
        rec["error"] = traceback.format_exc()[-1500:]
    return rec
if __name__ == "__main__":
    keys = [c + (m,) for c in CELLS for m in ("player", "captain")]
    with Pool(int(sys.argv[3]) if len(sys.argv) > 3 else 2) as p, open(sys.argv[1], "w") as f:
        for r in p.imap_unordered(one, keys):
            f.write(json.dumps(r) + "\n"); f.flush()
