import sys, json
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.physics import strain as ST
SEQS = {
  "bilander": ("fore.topmast", ["clear away the wreck of the fore topmast"], ["reef the main topsail", "heave to", "take in the mainsail"]),
  "brig": ("main.topmast", ["clear away the wreck of the main topmast"], ["take in the fore topgallant", "reef the fore topsail", "heave to"]),
  "merchant-brig": ("main.topmast", ["clear away the wreck of the main topmast"], ["heave to", "take in the jib"]),
}
out = {}
for ship, (spar, first, then) in SEQS.items():
    w = make_world(7, f"data/ships/{ship}.yaml", Scenario(wind_from_deg=270, wind_speed_kn=18, gustiness=0.0, variability=0.0, ship_heading_deg=0, ship_speed_kn=5))
    w.submit("set plain sail"); w.run(900)
    ST._wreck_spar(w.ship, ST.strain_state(w.ship), w.ship.spars[spar], 2.0)
    n0 = len(w.log); rep = []
    for o in first:
        rep.append([w.clock.tick, o, w.submit(o).text]); w.run(180)
    for o in then:
        rep.append([w.clock.tick, o, w.submit(o).text]); w.run(300)
    w.run(5400)
    out[ship] = {"replies": rep, "events": [[e.tick, e.kind, e.severity.value, e.text] for e in w.log[n0:]],
                 "wrecked": sorted(k for k, s in w.ship.spars.items() if s.wrecked and not s.sent_down)}
json.dump(out, open(sys.argv[1], "w"))
