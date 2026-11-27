"""mode 'save' (run in OLD): settle, tack, checkpoint at the tick after "helm's a-lee" + 15 s (before
the haul); mode 'load' (run in NEW): read it, run to the tack's end and 300 s on; mode 'straight'
(either tree): the same run without the checkpoint."""
import sys, math
sys.path.insert(0, "/tmp/claude-0/-home-user-FreeSail/e2d459f1-79d4-50d6-9285-0413fe7ccd0b/scratchpad/rev125-probes/gate")
import tackmx
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.core.replay import write_checkpoint, read_checkpoint
mode, ship, kn, path = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
def setup():
    w = make_world(7, f"data/ships/{ship}.yaml", Scenario(wind_from_deg=0.0, wind_speed_kn=kn, ship_heading_deg=292.5, ship_speed_kn=4.0))
    w.submit("set plain sail"); w.submit("brace sharp up on the starboard tack")
    tackmx.idle(w, 4000); w.submit("trim sails"); tackmx.idle(w, 600)
    for _ in range(60): w.tick()
    w.submit("tack ship")
    for _ in range(15): w.tick()
    return w
def finish(w):
    t0 = w.clock.tick; n = len(w.log)
    for _ in range(1200):
        w.tick()
    for e in w.log[n:]:
        if e.kind in ("evolution.step", "ship.tacked", "ship.missed_stays", "evolution.failed", "helm.order"):
            print(e.tick, e.kind, e.text)
    print("end rel", round(tackmx.rel(w), 1), "tick", w.clock.tick)
if mode == "save":
    w = setup()
    print([e.text for e in w.log if e.kind == "evolution.step"][-1:], "rel", tackmx.rel(w))
    write_checkpoint(w, path); print("saved", w.clock.tick)
elif mode == "load":
    _, w = read_checkpoint(path)
    finish(w)
else:
    finish(setup())
