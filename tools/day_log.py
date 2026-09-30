"""Write a scenario's day as the log saw it, one line per event, with its digest: a tool
for comparing a day between two machines (gate 5a, 2026-09-30: the owner's Windows run
of the day under systems matched every tick, every loss and the line count of the build
machine's and differed in the digest alone, so one line's text differs somewhere; this
prints them all to find it).

    py tools/day_log.py data/scenarios/gate-5a-day.yaml --hours 45 --out day-log.txt

The scenario is run at its own seed under its standing orders, as the truths run it
(tests/test_known_truths.py), for the hours given; each line is `tick  kind  text` and
the last line the digest. Send the file back and the lead diffs it against the build
machine's.
"""

from __future__ import annotations

import argparse
import platform
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from freesail.world.scenarios import begin, load_scenario, make_scenario_world  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenario")
    ap.add_argument("--hours", type=float, default=45.0)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--out", default="day-log.txt")
    args = ap.parse_args()
    sf = load_scenario(args.scenario)
    world = make_scenario_world(sf, seed=args.seed)
    begin(world, sf)
    world.run(int(args.hours * 3600))
    lines = [f"{e.tick}\t{e.kind}\t{e.text}" for e in world.log]
    digest = world.log.digest()[:16]
    head = [
        f"# {args.scenario} seed {world.seed} hours {args.hours}",
        f"# {platform.platform()} python {platform.python_version()}",
        f"# lines {len(world.log)} digest {digest}",
    ]
    Path(args.out).write_text("\n".join(head + lines) + "\n", encoding="utf-8")
    print(f"{len(world.log)} lines, digest {digest}, written to {args.out}")


if __name__ == "__main__":
    main()
