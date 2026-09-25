"""Measure sustained load-to-rating ratios on a reference ship with the real engine.

Run from the repository root, for example:

    python tools/measure_loads.py data/ships/frigate-36.yaml --wind 35 --twa 90 \
        --sail "make all sail" --brace "brace the yards up on the starboard tack"

It builds a World exactly as the console does (steady wind, no gusts), gives
the sail and brace orders, lets the evolutions finish and the ship settle,
then averages every part's `load_kn` over the last `--window` ticks and
prints the parts with the highest ratio of load to `rating_kn`. Package 8
used it to size the spar ratings in `tools/gen_ships.py` (the
SUSTAINED_FRACTION constant there); packages 9 and 10 can re-run it after a
tuning change to see where the strain rule will bite. It is a tool, not a
test: nothing here is asserted.

Wind is given as a true-wind angle off the bow (`--twa`, positive from
starboard); the ship steers north and the wind is set to come from that
bearing. `--speed` gives her way at the start so she does not spend the
run gathering it.

Trim: with `--trim best` (the default) every yard is braced each tick so
that its chord makes BEST_ALPHA_DEG with the deck-level apparent wind,
within its brace limit, which is what package 13's `trim` order does; the
brace order given with `--brace` is then only the starting point. With
`--trim orders` the yards stay where that order put them. A yard braced
"up" (30 degrees from square) on a beam reach has its chord within ten
degrees of the apparent wind and gives almost nothing, so `orders` mostly
measures how little an untrimmed ship loads her gear.
"""

from __future__ import annotations

import argparse
import math
import sys
from collections import defaultdict

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario

BEST_ALPHA_DEG = 35.0  # angle of attack at the square class's peak lift (data/sail_classes.yaml)


def best_trim(ship) -> None:
    """Brace every yard so its chord sits BEST_ALPHA_DEG off the deck apparent wind."""
    awa = ship.dyn.apparent_wind_angle
    chord = max(abs(awa) - math.radians(BEST_ALPHA_DEG), 0.0)
    for spar in ship.spars.values():
        if not spar.is_yard:
            continue
        limit = spar.brace_limit if spar.brace_limit > 0 else math.pi / 2
        brace = min(max(math.pi / 2 - chord, 0.0), limit)
        spar.brace_angle = math.copysign(brace, awa) if awa != 0 else 0.0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("ship")
    ap.add_argument("--wind", type=float, default=35.0, help="true wind, knots")
    ap.add_argument("--twa", type=float, default=90.0, help="true wind angle off the bow, degrees")
    ap.add_argument("--speed", type=float, default=6.0, help="starting speed, knots")
    ap.add_argument("--sail", action="append", default=None, help="sail order(s), in order")
    ap.add_argument("--brace", default="brace the yards up on the starboard tack")
    ap.add_argument("--trim", choices=("best", "orders"), default="best")
    ap.add_argument("--settle", type=int, default=1500, help="ticks before sampling begins")
    ap.add_argument("--window", type=int, default=300, help="ticks averaged")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)

    sail_orders = args.sail or ["make all sail"]
    scenario = Scenario(
        wind_from_deg=args.twa % 360.0,
        wind_speed_kn=args.wind,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        ship_speed_kn=args.speed,
    )
    world = make_world(args.seed, args.ship, scenario)
    ship = world.ship
    for text in sail_orders:
        world.submit(text)
    world.submit("steer north")
    # let the sails go up before bracing, so the brace evolutions find them set
    world.run(max(1, args.settle // 2))
    world.submit(args.brace)
    # a second round of the sail orders catches what could not be set at once (studding
    # sails wait for the sail beside them); a sail already set is refused harmlessly
    for text in sail_orders:
        world.submit(text)
    for _ in range(args.settle - args.settle // 2):
        if args.trim == "best":
            best_trim(ship)
        world.tick()

    sums: dict[str, float] = defaultdict(float)
    peak: dict[str, float] = defaultdict(float)
    speed = heel = awa = aws = 0.0
    for _ in range(args.window):
        if args.trim == "best":
            best_trim(ship)
        world.tick()
        for part in ship.parts.values():
            sums[part.id] += part.load_kn
            peak[part.id] = max(peak[part.id], part.load_kn)
        speed += ship.dyn.speed
        heel += abs(ship.dyn.heel)
        awa += abs(ship.dyn.apparent_wind_angle)
        aws += ship.dyn.apparent_wind_speed
    n = float(args.window)
    set_sails = sorted(s.id for s in ship.sails.values() if s.is_set)
    print(
        f"{args.ship}: wind {args.wind:g} kn at {args.twa:g} deg; "
        f"speed {units.ms_to_knots(speed / n):.1f} kn, heel {math.degrees(heel / n):.1f} deg, "
        f"apparent {math.degrees(awa / n):.0f} deg at {units.ms_to_knots(aws / n):.1f} kn"
    )
    print(f"set: {', '.join(set_sails)}")
    rows = []
    for part in ship.parts.values():
        mean = sums[part.id] / n
        if mean <= 0.0:
            continue
        rating = getattr(part, "rating_kn", 0.0) or 0.0
        ratio = mean / rating if rating > 0 else float("inf")
        rows.append((ratio, part.id, mean, peak[part.id], rating))
    rows.sort(reverse=True)
    print(f"{'ratio':>6}  {'part':45s} {'mean kN':>8} {'peak kN':>8} {'rating':>8}")
    for ratio, pid, mean, pk, rating in rows[: args.top]:
        print(f"{ratio:6.2f}  {pid:45s} {mean:8.1f} {pk:8.1f} {rating:8.1f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
