"""Write a scenario's day as the log saw it, one line per event, with its digest: a tool
for comparing a day between two machines (gate 5a, 2026-09-30: the owner's Windows run
of the day under systems matched every tick, every loss and the line count of the build
machine's and differed in the digest alone, so one line's text differs somewhere; this
prints them all to find it).

    py tools/day_log.py data/scenarios/gate-5a-day.yaml --hours 29 --out day-log.txt

The scenario is run at its own seed under its standing orders, as the truths run it
(tests/test_known_truths.py), for the hours given; each line is `tick  kind  text` and
the last line the digest. Send the file back and the lead diffs it against the build
machine's.

Package 33a (gate 5b): `--ship FILE` sails another ship through the same scenario and
orders (the cutter and the brig through the passage's), and `--reckoning` adds the
passage's account against the truth at the end of the file and on the terminal: at each
noon, at each cast, at the landfall and at the end, the reckoning beside the truth (the
author's view: the truth is in the world and the tests, never in a reading), the error
in miles, the ellipse's axes; and the ticks of the notable moments.

    py tools/day_log.py data/scenarios/gate-5b-passage.yaml --hours 22 --reckoning
    py tools/day_log.py data/scenarios/gate-5b-passage-schooner.yaml --hours 6 --reckoning \\
        --ship data/ships/cutter.yaml
"""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from freesail import units  # noqa: E402
from freesail.core.events import Severity  # noqa: E402
from freesail.world.geo import bearing_and_distance, format_position  # noqa: E402
from freesail.world.scenarios import begin, load_scenario, make_scenario_world  # noqa: E402

# The moments the account is set beside the truth at (the log's kinds).
ACCOUNT_KINDS = ("reckoning.noon", "sounding", "bearing.taken", "reckoning.set")


def account_lines(world, moments: list[tuple]) -> list[str]:
    """The reckoning against the truth at each moment and at the end."""
    out = ["# the account against the truth (the author's view)"]
    nav = world.navigation
    for tick, kind, text, truth, account, ellipse in moments:
        if truth is None or account is None:
            continue
        _, err = bearing_and_distance(truth, account)
        out.append(
            f"{tick}\t{kind}\ttruth {format_position(truth)}; "
            f"account {format_position(account)}; error {err / units.NAUTICAL_MILE:.1f} miles; "
            f"ellipse {ellipse['sigma_east_nm']:.1f} E-W by {ellipse['sigma_north_nm']:.1f} N-S "
            f"(sigma) | {text}"
        )
    if nav is not None and world.position is not None:
        now = nav.account_now()
        _, err = bearing_and_distance(world.position, now)
        e = nav.reckoning.ellipse()
        out.append(
            f"{world.clock.tick}\tend\ttruth {format_position(world.position)}; account "
            f"{format_position(now)}; error {err / units.NAUTICAL_MILE:.1f} miles; ellipse "
            f"{e['sigma_east_nm']:.1f} E-W by {e['sigma_north_nm']:.1f} N-S (sigma); "
            f"{nav.reckoning.uncertainty_words}"
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenario")
    ap.add_argument("--hours", type=float, default=29.0)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--ship", default=None, help="another ship file through the same scenario")
    ap.add_argument("--reckoning", action="store_true", help="the account against the truth")
    ap.add_argument("--out", default="day-log.txt")
    args = ap.parse_args()
    sf = load_scenario(args.scenario)
    world = make_scenario_world(sf, seed=args.seed, ship=args.ship)
    moments: list[tuple] = []
    if args.reckoning and world.navigation is not None:

        def watch(e) -> None:
            landfall = e.kind == "lookout.sighting" and e.data.get("landfall")
            if e.kind in ACCOUNT_KINDS or landfall:
                nav = world.navigation
                moments.append(
                    (
                        e.tick,
                        "landfall" if landfall else e.kind,
                        e.text,
                        world.position,
                        nav.account_now(),
                        nav.reckoning.ellipse(),
                    )
                )

        world.log.subscribe(watch)
    begin(world, sf)
    world.run(int(args.hours * 3600))
    lines = [f"{e.tick}\t{e.kind}\t{e.text}" for e in world.log]
    digest = world.log.digest()[:16]
    head = [
        f"# {args.scenario} seed {world.seed} hours {args.hours} ship {world.ship.name}",
        f"# {platform.platform()} python {platform.python_version()}",
        f"# lines {len(world.log)} digest {digest}",
    ]
    tail: list[str] = []
    if args.reckoning:
        tail = account_lines(world, moments)
        tail.append("# the notable moments")
        for e in world.log:
            if e.severity is not Severity.ROUTINE:
                tail.append(f"{e.tick}\t{e.ship_time:%d %H:%M}\t{e.kind}\t{e.text}")
    Path(args.out).write_text("\n".join(head + lines + tail) + "\n", encoding="utf-8")
    print(f"{len(world.log)} lines, digest {digest}, written to {args.out}")
    for line in tail:
        print(line)


if __name__ == "__main__":
    main()
