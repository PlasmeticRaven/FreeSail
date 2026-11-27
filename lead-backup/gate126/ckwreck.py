import sys
sys.path.insert(0, ".")
from freesail.core.replay import write_checkpoint, read_checkpoint
mode, path = sys.argv[1], sys.argv[2]
if mode == "write":
    from freesail.physics import strain as ST
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world
    sf = load_scenario(sys.argv[3]); w = make_scenario_world(sf); begin(w, sf)
    w.run(600)
    ST._wreck_spar(w.ship, ST.strain_state(w.ship), w.ship.spars["main.topmast"], 2.0)
    w.run(60)
    write_checkpoint(w, path)
    print("written", w.clock.tick, [ (i.evo.id, i.paused, i.waiting) for i in w.ship.extra["evolutions"].instances])
else:
    _, w = read_checkpoint(path)
    n0 = len(w.log)
    print("loaded", w.clock.tick, [(i.evo.id, i.paused, i.waiting) for i in w.ship.extra["evolutions"].instances])
    w.run(int(sys.argv[3]))
    for e in w.log[n0:]:
        if str(e.actor).startswith("captain") and "course" not in e.text or e.kind in ("wreck.cleared", "spar.shifted", "evolution.belayed", "evolution.failed", "order.rejected"):
            print(" ", e.tick, e.kind, e.text[:170])
    print("wrecked:", sorted(k for k, s in w.ship.spars.items() if s.wrecked))
