"""Gate 4a, item 8: a standing order in the dialect and its twin in Python give one log.

Run from the repository root:

    py tools/python_twin.py

Two frigates are built from seed 7 at 19:40 on 1 June 1805, head south with the wind
north at 15 knots, and both make all sail. One is given the night routine at the prompt,
in the dialect; the other is given the same rule in Python, through the API of
`freesail.standing` (spec M4 §4). Both run twenty-five minutes through sunset. The
script prints the Python rule's firing lines, whether every event after the tick the
rules were given is the same text at the same tick in both logs, and the Python rule's
entry in the book. It is a demonstration, not a test: truth 40 (tests/test_python_api.py)
asserts the same with the studding sails set.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

# Run as a script from a checkout that is not installed, the repository root must be
# importable (as tools/gen_ships.py does).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from freesail.api.session import make_world  # noqa: E402
from freesail.core.world import Scenario  # noqa: E402
from freesail.standing import at, bind, order  # noqa: E402

SHIP = "data/ships/frigate-36.yaml"
SEED = 7
DIALECT = (
    'standing order "night routine": at sunset then take in the studdingsails; take in the royals'
)


def scenario() -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 1, 19, 40),
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        ship_heading_deg=180.0,
    )


def main() -> None:
    dialect = make_world(SEED, SHIP, scenario())
    python = make_world(SEED, SHIP, scenario())
    for world in (dialect, python):
        world.submit("make all sail")

    dialect.submit(DIALECT)

    bind(python)

    @at("sunset", name="night routine")
    def night_routine():
        order("take in the studdingsails")
        order("take in the royals")

    dialect.run(1500)
    python.run(1500)

    print("The Python rule's lines:")
    for e in python.log:
        if e.actor.startswith("standing"):
            print("  " + e.line())

    after = lambda w: [(e.tick, e.text) for e in w.log if e.tick > 0]  # noqa: E731
    print("same log after the order:", after(dialect) == after(python))
    print(python.submit('show standing order "night routine"').text)


if __name__ == "__main__":
    main()
