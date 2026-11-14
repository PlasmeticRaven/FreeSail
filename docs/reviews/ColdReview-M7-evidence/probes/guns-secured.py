import sys; sys.path.insert(0, ".")  # run from the repository root
from freesail.world.scenarios import load_scenario, make_scenario_world, begin
from freesail.combat.guns import battery_of
sf = load_scenario("data/scenarios/first-action.yaml")
w = make_scenario_world(sf); begin(w, sf)
n0 = len(w.log)
for o in ("beat to quarters", "engage her to starboard", "fire as they bear"):
    r = w.submit(o); print(">", o, "=>", r.kind, "|", r.text)
    w.run(30)
w.run(1800)
r = w.submit("fire"); print("> fire =>", r.kind, "|", r.text)
w.run(1800)
print("guns reading:", w.readings.words("guns"))
b = battery_of(w.ship); print("battery mode", b.mode, "target", b.target, "cast", [g.cast_loose for g in w.ship.guns.values()][:4])
for e in w.log[n0:]:
    t = e.text
    if any(k in (e.kind or "") for k in ("guns","action","quarters","crew","order","captain")) or "gun" in t.lower():
        print(e.tick, e.kind, "|", t[:220])
