"""Gate probe: what a model's seat is served, and every order of a list answered, per ship file.

    cd <tree> && PYTHONPATH=$PWD python3 -P <probes>/gate/seat.py OUT.json [ship files...] [--orders FILE]

For each ship (default: every data/ships/*.yaml) a world is made (seed 7, 15 kn from north,
heading 90, 4 kn), its plain sail set and run 600 s; then served at the station
`officer of the watch`: every reading (tools.readings), the state (tools.state), the library
contents and every topic (whole, and each section), and the tool descriptions. Then each order
of the list (one per line; default ORDERS below) is given on a fresh copy of that world
(`core.replay.trial_copy`) and run 5 s: its reply kind and text and the log lines it made.
Compare two outputs with seatdiff.py.
"""

from __future__ import annotations

import glob
import json
import sys
import traceback

ORDERS = """set plain sail
make all sail
shorten sail
take in all sail
furl all
take in the mainsail
set the mainsail
reef the topsails
shake out the reefs
take in the topgallants
set the topgallants
set the jib
take in the jib
set the spanker
brace the yards up on the larboard tack
square the yards
tack ship
wear ship
heave to
fill away
lie a try
scud
box her off
steer E
come up two points
bear away
keep her full
helm a-lee
right the helm
clear for action
beat to quarters
cast loose the guns
run out the guns
run in the guns
secure the guns
load with round shot
man the pumps
secure the pumps
call all hands
pipe down
all hands
belay all work
belay that
heave the log
heave the lead
come to an anchor
let go the best bower
weigh
get under way
make the signal to tack
make the signal No. 16
rig preventer braces
send down the topgallant yards
strike the topmasts
swifter in the catharpins
set the storm staysails
step the mast
out oars
give way
easy all
send the boat ashore
tow her with the boat
muster
the booms
the sail room
take a fix
work up the reckoning
ask the watcher how she goes
stand down the lookout
batten down the hatches
take in the studdingsails
set the topsail
furl the main topsail
take in the fore topsail
set the fore topsail""".splitlines()


def serve(w, station):
    from freesail.agents import tools

    out = {}

    def grab(key, fn):
        try:
            v = fn()
            out[key] = v if isinstance(v, (str, dict, list)) else str(v)
        except Exception as e:  # noqa: BLE001
            out[key] = "ERROR " + type(e).__name__ + ": " + str(e)[:300]

    grab("readings", lambda: tools.readings(w, station))
    grab("state", lambda: tools.state(w, station))
    grab("library:contents", lambda: str(tools.library(w, station, "contents")))
    try:
        topics = tools._every_topic(w)
    except Exception as e:  # noqa: BLE001
        topics = []
        out["topics_error"] = str(e)
    for top in topics:
        grab(f"library:{top.key}", lambda: str(tools.library_by(w, None, top.key)))
        for sec in getattr(top, "sections", ()) or ():
            grab(f"library:{top.key}#{sec.heading}", lambda: str(tools.library_by(w, None, top.key, sec.heading)))
    for name in tools.tool_names():
        grab(f"tool:{name}", lambda: tools.description_of(name))
    return out


def main(argv):
    out_path = argv[0]
    ships = [a for a in argv[1:] if a.endswith(".yaml")] or sorted(glob.glob("data/ships/*.yaml"))
    orders = ORDERS
    if "--orders" in argv:
        orders = [x for x in open(argv[argv.index("--orders") + 1]).read().splitlines() if x.strip()]
    from freesail.api.session import make_world
    from freesail.core.replay import trial_copy
    from freesail.core.world import Scenario

    res = {}
    for path in ships:
        rec = {"served": {}, "orders": {}}
        try:
            sc = Scenario(wind_from_deg=0.0, wind_speed_kn=15.0, gustiness=0.0, variability=0.0,
                          ship_heading_deg=90.0, ship_speed_kn=4.0)
            w = make_world(7, path, sc)
            w.submit("set plain sail")
            w.run(600)
            rec["served"] = serve(w, "officer of the watch")
            for text in orders:
                c = trial_copy(w, raising=True)
                n0 = len(c.log)
                try:
                    r = c.submit(text)
                    c.run(5)
                    rec["orders"][text] = {
                        "kind": getattr(r, "kind", None), "text": getattr(r, "text", str(r)),
                        "lines": [[e.tick, e.kind, e.severity.value, e.text] for e in list(c.log)[n0:]],
                    }
                except Exception:  # noqa: BLE001
                    rec["orders"][text] = {"error": traceback.format_exc()[-800:]}
        except Exception:  # noqa: BLE001
            rec["error"] = traceback.format_exc()[-2000:]
        res[path] = rec
    json.dump(res, open(out_path, "w"), indent=0)


if __name__ == "__main__":
    main(sys.argv[1:])
