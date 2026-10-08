"""Read-only: replay a save (a scratch COPY of it) on the build given by PYTHONPATH, and
record along the way how far the account stood from the truth, the master's doubt, and the
ship's head, way and wind. Checks at the end that the replay is the game that was played
(the log's digest against the checkpoint's). Writes only to OUT_PREFIX.* in the scratchpad.

usage: replay_probe.py SAVE.json OUT_PREFIX [EVERY_TICKS]
"""
import json
import math
import sys
import time

from freesail import units
from freesail.api.session import ship_factory
from freesail.core import replay as R

path, out = sys.argv[1], sys.argv[2]
every = int(sys.argv[3]) if len(sys.argv) > 3 else 60
data = R.load_file(path)
header, cw = R.read_checkpoint(R.checkpoint_path(path))
print("save build", data.get("build"), "| this build", R.build_stamp(), "| same:", R.same_build(R.stamp_of(data)))

world = R.build_world(data, ship_factory)
end = data["end_tick"]
inputs = data["inputs"]

WATCH = {
    "reckoning.fix", "bearing.taken", "reckoning.lunar", "lunar.taken", "reckoning.noon",
    "sounding", "ship.hove_to", "ship.filled_away", "ship.aback", "ship.anchored",
    "anchor.dragging", "anchor.holding", "ship.aweigh", "ship.weighed", "lookout.land_ahead",
    "lookout.sighting", "port.pilot_aboard", "port.pilot_left", "ship.moored", "ship.wore",
    "ship.tacked", "master.place", "ship.swung", "cable.veered", "ship.brought_up",
    "ship.unmoored", "ship.aground", "agent.deck", "course.shaped",
}


def deg(rad):
    return round(math.degrees(rad) % 360.0, 1)


def snap():
    truth = world.position
    nav = getattr(world, "navigation", None)
    row = {"tick": world.clock.tick}
    if truth is None or nav is None:
        return row
    r = nav.reckoning
    acc = nav.account_now()
    dn = (acc.lat_deg - truth.lat_deg) * 60.0
    de = (acc.lon_deg - truth.lon_deg) * 60.0 * math.cos(math.radians(truth.lat_deg))
    d = getattr(world.ship, "dyn", None)
    row.update(
        t_lat=round(truth.lat_deg, 5), t_lon=round(truth.lon_deg, 5),
        a_lat=round(acc.lat_deg, 5), a_lon=round(acc.lon_deg, 5),
        err=round(math.hypot(de, dn), 3), err_e=round(de, 3), err_n=round(dn, 3),
        sig_e=round(r.sigma_east_nm, 3), sig_n=round(r.sigma_north_nm, 3),
        run_fix=round(r.run_since_fix_nm, 2),
        head=deg(world.ship.heading),
        u_kn=round(units.ms_to_knots(d.u), 2) if d is not None else None,
        v_kn=round(units.ms_to_knots(d.v), 2) if d is not None and hasattr(d, "v") else None,
        wind_from=deg(world.wind.direction_from),
        wind_kn=round(units.ms_to_knots(world.wind.effective_speed), 1),
        hove="hove_to" in (getattr(world.ship, "extra", None) or {}),
    )
    try:
        dn_ = nav.doubt_now()
        row["doubt_nm"] = round(float(dn_["semi_major_nm"]), 3)
    except Exception as e:
        row["doubt_nm"] = None
        row["doubt_err"] = str(e)[:60]
    chart = getattr(world, "chart", None)
    if chart is not None:
        tide = float(getattr(world, "tide_height_m", 0.0))
        dt, da = chart.depth_at(truth), chart.depth_at(acc)
        row.update(
            tide_m=round(tide, 2),
            depth_true_fm=None if dt is None else round(units.m_to_fathoms(dt + tide), 2),
            chart_true_fm=None if dt is None else round(units.m_to_fathoms(dt), 2),
            chart_acc_fm=None if da is None else round(units.m_to_fathoms(da), 2),
        )
        try:
            row["allow_m"] = round(float(nav._tide_allowance_m()), 2)
        except Exception as e:
            row["allow_m"] = str(e)[:40]
    return row


series = open(out + ".series.jsonl", "w", encoding="utf-8")
events = open(out + ".events.jsonl", "w", encoding="utf-8")


def watch(e):
    if e.kind in WATCH:
        row = snap()
        row.update(kind=e.kind, actor=e.actor, text=e.text, sev=e.severity.value)
        try:
            row["data"] = json.loads(json.dumps(e.data, default=str))
        except Exception:
            row["data"] = None
        events.write(json.dumps(row, ensure_ascii=False) + "\n")


world.log.subscribe(watch)
t0 = time.time()
i = 0
while True:
    while i < len(inputs) and int(inputs[i]["tick"]) == world.clock.tick:
        R._give(world, inputs[i])
        i += 1
        for agent in list(world.agents.values()):
            agent.on_input()
    if world.clock.tick >= end:
        break
    world.tick()
    if world.clock.tick % every == 0:
        series.write(json.dumps(snap()) + "\n")
    if world.clock.tick % 50000 == 0:
        print(f"  tick {world.clock.tick} after {time.time() - t0:.0f}s", flush=True)
world.log.unsubscribe(watch)
series.close()
events.close()
a, b = cw.log.all(), world.log.all()
print(f"replayed {end} ticks in {time.time() - t0:.0f}s")
print(f"checkpoint log {len(a)} lines, digest {cw.log.digest()[:16]}; replayed log {len(b)} lines, digest {world.log.digest()[:16]}")
print("IDENTICAL:", cw.log.digest() == world.log.digest())
if cw.log.digest() != world.log.digest():
    n = min(len(a), len(b))
    first = next((k for k in range(n) if (a[k].tick, a[k].kind, a[k].actor, a[k].text) != (b[k].tick, b[k].kind, b[k].actor, b[k].text)), n)
    print(f"first difference at line {first} of {n}")
    for k in range(max(0, first - 2), min(n, first + 4)):
        print("  played  :", a[k].tick, a[k].kind, a[k].actor, a[k].text[:140])
        print("  replayed:", b[k].tick, b[k].kind, b[k].actor, b[k].text[:140])
