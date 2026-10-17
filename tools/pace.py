"""The pace of the game on this machine (package 43's measurement, kept as a tool after the
owner asked for it on 2026-10-17): the frigate alone on the station trial, the frigate with
the dozen ships of the merchant passage at far detail, and the frigate with one, three, six
and twelve fully crewed ships under rules-based captains ticked at once, each in truth 51's
form (a thousand ticks to settle, the best of three thousands), printed as ticks a second
with the machine's load beside. Run it on a quiet machine:

    py tools/pace.py                 # all three measures, the crewed at 1, 3, 6 and 12
    py tools/pace.py alone           # the frigate alone
    py tools/pace.py far             # with the dozen at far detail
    py tools/pace.py crewed --ships 3 6   # with so many crewed ships
    py tools/pace.py crewed --profile     # and a profile of three crewed ships' ticks

Sixty ticks a second is the owner's play at 60x; the crewed cap (`freesail/world/crews.py`,
`CREWED_CAP`) was chosen from these figures on the build machine (TuningNotes, package 43).
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.getcwd())

from freesail.api.session import make_world  # noqa: E402
from freesail.core.world import Scenario  # noqa: E402
from freesail.world.scenarios import begin, load_scenario, make_scenario_world  # noqa: E402

TRIAL = "data/scenarios/trials/trial-station-stranger.yaml"

# twelve ships in the Channel with intents, a mix of the four files
SHIPS = [
    ("data/ships/brig.yaml", 49.2, -5.6, "bound for Falmouth"),
    ("data/ships/topsail-schooner.yaml", 49.4, -5.0, "bound for Plymouth"),
    ("data/ships/cutter.yaml", 49.6, -5.9, "keep the station off the Lizard within 8 miles"),
    ("data/ships/frigate-36.yaml", 48.6, -5.6, "keep the station off Ushant within 15 miles"),
    ("data/ships/brig.yaml", 48.9, -5.2, "run home to Brest"),
    ("data/ships/topsail-schooner.yaml", 49.0, -6.0, "bound for Brest"),
    ("data/ships/brig.yaml", 49.5, -4.6, "bound for Falmouth"),
    ("data/ships/cutter.yaml", 49.8, -5.3, "carry this letter to Plymouth"),
    ("data/ships/frigate-36.yaml", 49.3, -6.3, "bound for Plymouth"),
    ("data/ships/brig.yaml", 48.8, -6.2, "bound for the Start"),
    ("data/ships/topsail-schooner.yaml", 49.7, -4.9, "bound for Brest"),
    ("data/ships/cutter.yaml", 49.1, -4.8, "bound for Falmouth"),
]


def crewed(sf, i, ship_file, lat, lon, intent):
    sc = Scenario(**{k: v for k, v in sf.scenario.to_dict().items() if k != "start_time"})
    sc.start_time = sf.scenario.start_time
    sc.position = {"lat_deg": lat, "lon_deg": lon}
    sc.ships = []
    sc.world_orders = []
    sc.intent = intent
    sc.books = []
    sc.glass = False
    sc.ship_heading_deg = 200.0
    sc.ship_speed_kn = 5.0
    w = make_world(7 + i, ship_file, sc)
    w.submit("set plain sail")
    return w


def measure(worlds, label):
    for w in worlds:
        w.run(1000)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        for _ in range(1000):
            for w in worlds:
                w.tick()
        best = max(best, 1000 / (time.perf_counter() - t0))
    print(f"{label}: {best:.0f} ticks a second (load {os.getloadavg()[0]:.2f})", flush=True)
    return best


def main(which: str = "all", ships: list[int] | None = None, profile: bool = False) -> None:
    sf = load_scenario(TRIAL)
    player = make_scenario_world(sf)
    begin(player, sf)
    if which in ("all", "alone"):
        measure([player], "the frigate alone (the station trial)")
    if which in ("all", "far"):
        from freesail.world.ships import vessel_from_spec

        sf2 = load_scenario("data/scenarios/merchant-passage.yaml")
        far = make_scenario_world(sf)
        begin(far, sf)
        for spec in sf2.scenario.ships:
            far.vessels.serial += 1
            far.vessels.add(vessel_from_spec(far, dict(spec), far.vessels.serial))
        measure([far], "the frigate with the dozen ships at far detail")
    if which in ("all", "crewed"):
        ns = ships or [1, 3, 6, 12]
        crews = [crewed(sf, i, *s) for i, s in enumerate(SHIPS)]
        for n in ns:
            measure([player] + crews[:n], f"the frigate with {n} crewed ship(s)")
        if profile:
            import cProfile
            import pstats

            pr = cProfile.Profile()
            pr.enable()
            for _ in range(600):
                for w in crews[:3]:
                    w.tick()
            pr.disable()
            pstats.Stats(pr).sort_stats("cumulative").print_stats(45)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("which", nargs="?", default="all", choices=["all", "alone", "far", "crewed"])
    ap.add_argument("--ships", type=int, nargs="+", help="how many crewed ships, each a measure")
    ap.add_argument("--profile", action="store_true", help="profile three crewed ships' ticks")
    args = ap.parse_args()
    main(args.which, args.ships, args.profile)
