"""Package 75, stage 0: the golden classing table of the eight files (docs/design/Build-Ships.md
§3.1 item 27; docs/design/Design-ShipsEngineExtensions.md §10.1).

How the manoeuvres class a rig, read through the engine's own gates on each file as it
stands, plain sail set: the masts that carry braced yards (`scripts._masts_with_yards`,
over `working_yards` and `Spar.is_yard`); the head yards, on the foremost of them, and the
after yards (`head_and_after_yards`); the mast whose yards are laid aback to heave to
(`yards_to_back`, the most square sail); whether her helm steers by the highest square sail
(`physics.sails._square_rigged`, yards on two masts or more); the after yards' stagger braced
sharp up (`trim.stagger` with every yard at its limit: the main yard's limit less the
fore's, in degrees, None with the yards on one mast); the driver brailed up hove to
(`after_gaff_sails`); the sails hauled aft at helm's a-lee (`boom_sails`); and a lugger's
dipping lugs (`dipping_lugs`).

The figures are Ext §10.1's, measured again on this tree at stage 0. The engine's
extensions (a lateen yard out of the braced yards, the yards under the bowsprit, the
settee) are built so that no existing file's classing moves: each of their steps runs this
file, and a row that moves is a fault of the step, not a figure to repin.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from freesail.evolutions import scripts
from freesail.evolutions import trim as yard_trim
from freesail.physics.sails import _square_rigged
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState

ROOT = Path(__file__).resolve().parents[1]

# Ext §10.1, by file: the masts with yards (by id, as `_masts_with_yards` finds them), the
# head and after yards' numbers, the mast backed, square-rigged, the stagger (degrees, to the
# tenth), the driver, the boom sails and the dipping lugs (each by id, in the file's order).
TABLE: dict[str, tuple] = {
    "frigate-36": (
        ["fore.mast", "main.mast", "mizzen.mast"],
        (4, 8),
        "main.mast",
        True,
        2.0,
        ["mizzen.spanker"],
        ["mizzen.spanker"],
        [],
    ),
    "brig": (
        ["fore.mast", "main.mast"],
        (4, 4),
        "main.mast",
        True,
        2.0,
        ["main.spanker"],
        ["main.spanker"],
        [],
    ),
    "merchant-brig": (
        ["fore.mast", "main.mast"],
        (4, 4),
        "main.mast",
        True,
        2.0,
        ["main.spanker"],
        ["main.spanker"],
        [],
    ),
    "cutter": (["main.mast"], (3, 0), "main.mast", False, None, [], ["main.sail"], []),
    "topsail-schooner": (["fore.mast"], (2, 0), "fore.mast", False, None, [], ["main.sail"], []),
    "privateer-schooner": (["fore.mast"], (2, 0), "fore.mast", False, None, [], ["main.sail"], []),
    "smack": (["main.mast"], (2, 0), "main.mast", False, None, [], ["main.sail"], []),
    "lugger": ([], (0, 0), None, False, None, [], ["mizen.lug"], ["fore.lug", "main.lug"]),
}


def _under_plain_sail(name: str) -> Ship:
    """The file's ship as it loads, its plain sail set (the polar's way:
    `world.ships._rigged_for_plain_sail`)."""
    ship = load_ship(f"data/ships/{name}.yaml")
    for sid in ship.groups.get("plain sail", []):
        ship.sails[sid].state = SailState.SET
    return ship


def test_the_table_holds_the_eight_files():
    assert len(TABLE) == 8
    for name in TABLE:
        assert (ROOT / "data" / "ships" / f"{name}.yaml").is_file(), name


@pytest.mark.parametrize("name", list(TABLE))
def test_each_files_classing_is_as_measured_at_stage_0(name):
    masts, (head_n, after_n), backed, square, stagger, driver, boom, dipping = TABLE[name]
    ship = _under_plain_sail(name)
    assert [m.id for m in scripts._masts_with_yards(ship)] == masts
    head, after = scripts.head_and_after_yards(ship)
    assert (len(head), len(after)) == (head_n, after_n)
    to_back = scripts.yards_to_back(ship)
    assert (ship.mast_of(to_back[0]).id if to_back else None) == backed
    assert _square_rigged(ship) is square
    targets = {y.id: y.brace_limit for y in scripts.working_yards(ship)}
    _, diff = yard_trim.stagger(ship, targets)
    if stagger is None:
        assert diff is None
    else:
        assert diff == pytest.approx(stagger, abs=0.05)
    assert [s.id for s in scripts.after_gaff_sails(ship)] == driver
    assert [s.id for s in scripts.boom_sails(ship)] == boom
    assert [s.id for s in scripts.dipping_lugs(ship)] == dipping
