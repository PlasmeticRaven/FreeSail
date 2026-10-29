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

Stage 0E (Ext §8 items 1, 2 and 4), on a hand-built rig: the three keys (`settee`,
`cut_at_mast`, `heave_to_aback`) load onto their parts and are refused in words where they
cannot stand; a sail cut at the mast takes the gaff's curve (`Sail.curve_class`) and every
other sail its own; `Ship.under_bowsprit` names the yards under the bowsprit and their square
sails, and no part of the eight files; and the eight files' sails and spars, their specs and
the whole ship pickle as before, the new fields left out while they hold their defaults.

Stage 0E (Ext §8 items 5 to 8), on the fixtures (`tests/rig_fixtures.py`): no file of the
eight carries a new key, a lateen yard or a yard under the bowsprit, read off the file
itself; each fixture loads and validates, cut to its contract (Ext §3.4, §4.1, §5.1); the
runner's `class: settee` takes a settee and nothing else, and its `wanted_sheet(sail)` the
sheet of the sail's curve class; and the served graph and snapshot carry `settee`,
`cut_at_mast` and `yard_lowered` only where they hold.

The driver's stage 0 (Ext §17.4, §17.7, §17.8): a lateen cut at the mast may name a boom, and a
whole lateen naming one is refused in words; no file of the eight carries a lateen naming a
boom (the probe); and `frigate_with_driver()` loads, bent and unbent, cut to §17.2's contract.
"""

from __future__ import annotations

import copy
import math
import pickle
from dataclasses import fields
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from rig_fixtures import (
    DRIVER_BOOM_M,
    DRIVER_STEEL_AREA_M2,
    DRIVER_YARD_M,
    area_centroid,
    brig_with_settee,
    brig_with_settee_doc,
    frigate_with_driver,
    frigate_with_driver_doc,
    frigate_with_mizen_yard,
    frigate_with_mizen_yard_doc,
    write_ship,
)

from freesail.api import queries
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner, expr, scripts
from freesail.evolutions import trim as yard_trim
from freesail.evolutions.runner import Instance
from freesail.physics.sails import _square_rigged
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState
from freesail.ship.schema import ShipFileError
from freesail.ship.stub import OrderError

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


# -- stage 0E: the three keys, the curve and the predicate ---------------------------------

# A hand-built rig of three masts and a bowsprit (round figures, not a ship's): a fore course
# on its yard; a settee on a lug yard on the main, the mast laid aback to heave to; a lateen
# mizen course cut at the mast on a lateen yard; a spritsail yard under the bowsprit and a
# sprit-topsail yard under the jib-boom, each with its square sail; and a jib on a stay of the
# jib-boom, whose chain roots at the bowsprit too.
RIG: dict = {
    "ship": {"name": "Test", "rig": "ship"},
    "hull": {
        "length_waterline_m": 40.0,
        "beam_m": 11.0,
        "draught_m": 4.5,
        "displacement_kg": 900000,
        "gm_m": 1.2,
    },
    "spars": [
        {"id": "fore.mast", "class": "mast", "x_m": 10.0, "height_m": 20.0},
        {
            "id": "fore.yard",
            "class": "yard",
            "on": "fore.mast",
            "length_m": 16.0,
            "height_m": 14.0,
            "brace_limit_deg": 40,
        },
        {"id": "main.mast", "class": "mast", "x_m": 0.0, "height_m": 22.0, "heave_to_aback": True},
        {
            "id": "main.yard",
            "class": "lug_yard",
            "on": "main.mast",
            "length_m": 18.0,
            "height_m": 15.0,
        },
        {"id": "mizzen.mast", "class": "mast", "x_m": -10.0, "height_m": 16.0},
        {
            "id": "mizzen.yard",
            "class": "lateen_yard",
            "on": "mizzen.mast",
            "length_m": 16.0,
            "height_m": 9.0,
        },
        {"id": "bowsprit", "class": "bowsprit", "x_m": 20.0, "length_m": 12.0, "height_m": 2.0},
        {"id": "jib_boom", "class": "jib_boom", "on": "bowsprit", "length_m": 9.0, "height_m": 5.0},
        {
            "id": "spritsail.yard",
            "class": "yard",
            "on": "bowsprit",
            "length_m": 12.0,
            "height_m": 3.0,
            "brace_limit_deg": 30,
        },
        {
            "id": "sprit_topsail.yard",
            "class": "yard",
            "on": "jib_boom",
            "length_m": 7.0,
            "height_m": 6.0,
            "brace_limit_deg": 30,
        },
    ],
    "sails": [
        {
            "id": "fore.course",
            "class": "square",
            "yard": "fore.yard",
            "area_m2": 120,
            "x_m": 10.0,
            "centre_height_m": 10.0,
        },
        {
            "id": "main.settee",
            "class": "lug",
            "yard": "main.yard",
            "mast": "main.mast",
            "dipping": True,
            "settee": True,
            "corners_m": [[2.0, 1.5], [3.0, 5.0], [-9.0, 15.0], [-8.0, 1.5]],
            "area_m2": 110,
            "x_m": -3.0,
            "centre_height_m": 8.0,
        },
        {
            "id": "mizzen.course",
            "class": "lateen",
            "yard": "mizzen.yard",
            "mast": "mizzen.mast",
            "cut_at_mast": True,
            "corners_m": [[-10.0, 1.5], [-10.0, 8.0], [-17.0, 14.0], [-17.0, 1.5]],
            "area_m2": 60,
            "x_m": -13.5,
            "centre_height_m": 7.0,
        },
        {
            "id": "spritsail",
            "class": "square",
            "yard": "spritsail.yard",
            "area_m2": 50,
            "x_m": 24.0,
            "centre_height_m": 3.0,
        },
        {
            "id": "sprit_topsail",
            "class": "square",
            "yard": "sprit_topsail.yard",
            "area_m2": 30,
            "x_m": 28.0,
            "centre_height_m": 7.0,
        },
        {
            "id": "jib",
            "class": "jibheaded",
            "stay": "jib.stay",
            "area_m2": 40,
            "x_m": 22.0,
            "centre_height_m": 9.0,
        },
    ],
    "lines": [{"id": "jib.stay", "class": "stay", "of": "jib_boom"}],
}

# The fields stage 0E adds to the runtime parts and their specs: left out of the pickled
# state while they hold their defaults, so that the eight files' checkpoints are as before.
NEW_SAIL = ("settee", "yard_lowered", "cut_at_mast")
NEW_SAIL_SPEC = ("settee", "cut_at_mast")
NEW_SPAR = ("heave_to_aback",)


def _rig(part: str = "", **keys) -> dict:
    """The hand-built rig with `keys` set on the spar or sail `part`, a key given None taken
    out of it."""
    doc = copy.deepcopy(RIG)
    for item in doc["spars"] + doc["sails"]:
        if item["id"] == part:
            item.update(keys)
            for k in [k for k, v in keys.items() if v is None]:
                del item[k]
    return doc


def test_the_three_keys_load_onto_their_parts_and_nowhere_else():
    ship = ship_from_dict(RIG, "rig.yaml")
    assert [s.id for s in ship.sails.values() if s.settee] == ["main.settee"]
    assert [s.id for s in ship.sails.values() if s.cut_at_mast] == ["mizzen.course"]
    assert [s.id for s in ship.spars.values() if s.heave_to_aback] == ["main.mast"]
    assert not any(s.yard_lowered for s in ship.sails.values())  # runtime only
    assert [s.id for s in ship.spec.sails if s.settee] == ["main.settee"]
    assert [s.id for s in ship.spec.sails if s.cut_at_mast] == ["mizzen.course"]
    assert [s.heave_to_aback for s in ship.spec.spars[:3]] == [None, None, True]


@pytest.mark.parametrize(
    "part, keys, message",
    [
        # the settee (Ext §5.2): a dipping lug naming its mast with four corners, never
        # sheeted to another sail or set flying
        ("main.settee", {"settee": "yes"}, "has settee = 'yes'; say true or false."),
        ("fore.course", {"settee": True}, "is a square sail; only a lug is a settee."),
        ("main.settee", {"dipping": None}, "is a settee and is not dipping"),
        ("main.settee", {"mast": None}, "is a settee and names no 'mast'"),
        ("main.settee", {"corners_m": None}, "is a settee and does not give four corners_m"),
        (
            "main.settee",
            {"corners_m": [[2.0, 1.5], [-9.0, 15.0], [-8.0, 1.5]]},
            "is a settee and does not give four corners_m",
        ),
        ("main.settee", {"sheeted_to": "main.settee"}, "is a settee sheeted to 'main.settee'"),
        ("main.settee", {"flying": True}, "is a settee set flying"),
        # the lateen cut at the mast (Ext §3.1): a lateen naming its mast with four corners
        ("mizzen.course", {"cut_at_mast": 1}, "has cut_at_mast = 1; say true or false."),
        ("main.settee", {"cut_at_mast": True}, "is a lug sail; only a lateen is cut at the mast."),
        ("mizzen.course", {"mast": None}, "is cut at the mast and names no 'mast'"),
        ("mizzen.course", {"corners_m": None}, "is cut at the mast and does not give four"),
        # the mast laid aback (Ext §5.7): a lower mast's key, and one mast's
        ("main.mast", {"heave_to_aback": "yes"}, "has heave_to_aback = 'yes'; say true"),
        ("fore.yard", {"heave_to_aback": True}, "is a yard; only a lower mast takes"),
        ("bowsprit", {"heave_to_aback": False}, "is a bowsprit; only a lower mast takes"),
        ("jib_boom", {"heave_to_aback": True}, "is a jib boom; only a lower mast takes"),
        (
            "mizzen.mast",
            {"heave_to_aback": True},
            "spar 'mizzen.mast' is laid aback to heave to as well as 'main.mast'",
        ),
    ],
)
def test_the_three_keys_are_refused_in_words_where_they_cannot_stand(part, keys, message):
    with pytest.raises(ShipFileError) as e:
        ship_from_dict(_rig(part, **keys), "bad.yaml")
    assert message in str(e.value)
    assert str(e.value).startswith("bad.yaml:")


def test_a_key_said_false_is_no_key_and_a_lateen_without_it_is_whole():
    """A key said false is taken as no key; a lateen without `cut_at_mast` is a whole
    lateen (the tartane's, a later package's), which need name no mast and give no corners."""
    ship = ship_from_dict(_rig("fore.course", settee=False, cut_at_mast=False), "rig.yaml")
    assert not ship.sails["fore.course"].settee and not ship.sails["fore.course"].cut_at_mast
    whole = _rig("mizzen.course", cut_at_mast=None, mast=None, corners_m=None)
    assert not ship_from_dict(whole, "rig.yaml").sails["mizzen.course"].cut_at_mast
    off = ship_from_dict(_rig("main.mast", heave_to_aback=False), "rig.yaml")
    assert not off.spars["main.mast"].heave_to_aback
    assert off.spec.spars[2].heave_to_aback is False


def test_a_sail_cut_at_the_mast_takes_the_gaffs_curve_and_every_other_sail_its_own():
    ship = ship_from_dict(RIG, "rig.yaml")
    assert ship.sails["mizzen.course"].curve_class == "gaff"
    assert {s.id: s.curve_class for s in ship.sails.values() if not s.cut_at_mast} == {
        "fore.course": "square",
        "main.settee": "lug",  # a settee keeps the lug's curve (D44(a))
        "spritsail": "square",
        "sprit_topsail": "square",
        "jib": "jibheaded",
    }
    whole = ship_from_dict(_rig("mizzen.course", cut_at_mast=None), "rig.yaml")
    assert whole.sails["mizzen.course"].curve_class == "lateen"
    for name in TABLE:
        ship = load_ship(f"data/ships/{name}.yaml")
        assert all(s.curve_class == s.cls for s in ship.sails.values()), name


def test_under_bowsprit_names_the_yards_under_it_and_their_square_sails_alone():
    """Ext §4.2: a yard whose chain roots at the bowsprit, and the square sail bent to one;
    not the bowsprit, the jib-boom or the jib, whose chains root there too, nor anything on
    a mast. By id or by part; no part of the eight files."""
    ship = ship_from_dict(RIG, "rig.yaml")
    under = {"spritsail.yard", "sprit_topsail.yard", "spritsail", "sprit_topsail"}
    assert {pid for pid in ship.parts if ship.under_bowsprit(pid)} == under
    assert ship.mast_of("jib").id == "bowsprit" and not ship.under_bowsprit("jib")
    assert ship.under_bowsprit(ship.sails["sprit_topsail"])
    assert not ship.under_bowsprit(ship.spars["fore.yard"])
    assert not ship.under_bowsprit("jib.stay")  # a line is neither
    for name in TABLE:
        ship = load_ship(f"data/ships/{name}.yaml")
        assert not any(ship.under_bowsprit(pid) for pid in ship.parts), name


@pytest.mark.parametrize("name", list(TABLE))
def test_a_ships_sails_and_spars_are_pickled_as_before_stage_0e(name):
    """The checkpoint (the owner's rule for stage 0E): every `Sail`, `Spar`, `SailSpec` and
    `SparSpec` of the eight files pickles its fields as before, in their order, the new ones
    left out while they hold their defaults; the whole ship's pickle names none of them; and
    what is unpickled reads the class's default back."""
    ship = load_ship(f"data/ships/{name}.yaml")
    for objs, new in (
        (ship.sails.values(), NEW_SAIL),
        (ship.spars.values(), NEW_SPAR),
        (ship.spec.sails, NEW_SAIL_SPEC),
        (ship.spec.spars, NEW_SPAR),
    ):
        for obj in objs:
            before = [f.name for f in fields(obj) if f.name not in new]
            assert list(obj.__getstate__()) == before, obj.id
            again = pickle.loads(pickle.dumps(obj))
            assert again == obj and not set(new) & set(again.__dict__), obj.id
    whole = pickle.dumps(ship)
    for key in (*NEW_SAIL, *NEW_SPAR):
        assert key.encode() not in whole, key
    again = pickle.loads(whole)
    assert not any(s.settee or s.cut_at_mast or s.yard_lowered for s in again.sails.values())
    assert not any(s.heave_to_aback for s in again.spars.values())


def test_the_keys_set_are_kept_in_the_pickle():
    ship = ship_from_dict(RIG, "rig.yaml")
    ship.sails["main.settee"].yard_lowered = True
    again = pickle.loads(pickle.dumps(ship))
    settee, course = again.sails["main.settee"], again.sails["mizzen.course"]
    assert settee.settee and settee.yard_lowered
    assert course.cut_at_mast and course.curve_class == "gaff"
    assert again.spars["main.mast"].heave_to_aback
    assert again.spec.sails[1].settee and again.spec.spars[2].heave_to_aback is True
    assert not again.sails["fore.course"].yard_lowered
    assert "yard_lowered" not in again.sails["fore.course"].__dict__


# -- stage 0E: the probe, the fixtures, the runner's hooks, the served fields --------------


def _root(spars: dict[str, dict], s: dict) -> dict:
    """The spar at the foot of a spar's chain in a file's document: its lower mast or its
    bowsprit."""
    while s.get("on") or s.get("steps_on"):
        s = spars[s.get("on") or s.get("steps_on")]
    return s


@pytest.mark.parametrize("name", list(TABLE))
def test_no_file_of_the_eight_carries_a_new_key_a_lateen_yard_or_a_yard_under_the_bowsprit(name):
    """Ext §8 item 8, the probe, read off the file itself and again as loaded: what keeps
    every extension inert on the eight files until a ship's builder writes it; from the
    driver's stage 0 (Ext §17.7), a lateen naming a boom among them."""
    doc = yaml.safe_load((ROOT / "data" / "ships" / f"{name}.yaml").read_text(encoding="utf-8"))
    spars = {s["id"]: s for s in doc["spars"]}
    assert [s["id"] for s in doc["sails"] if {"settee", "cut_at_mast"} & set(s)] == []
    assert [s["id"] for s in doc["sails"] if s["class"] == "lateen" and "boom" in s] == []
    assert [s["id"] for s in doc["spars"] if "heave_to_aback" in s] == []
    assert [s["id"] for s in doc["spars"] if s["class"] == "lateen_yard"] == []
    yards = [s for s in doc["spars"] if s["class"] == "yard"]
    assert [s["id"] for s in yards if _root(spars, s)["class"] == "bowsprit"] == []
    ship = load_ship(f"data/ships/{name}.yaml")
    assert not any(s.settee or s.cut_at_mast or s.yard_lowered for s in ship.sails.values())
    assert not any(s.heave_to_aback for s in ship.spars.values())


FIXTURES = {
    "frigate": (frigate_with_mizen_yard, frigate_with_mizen_yard_doc),
    "brig": (brig_with_settee, brig_with_settee_doc),
    "frigate-driver": (frigate_with_driver, frigate_with_driver_doc),
    "frigate-driver-bent": (
        lambda: frigate_with_driver(bent=True),
        lambda: frigate_with_driver_doc(bent=True),
    ),
}


@pytest.mark.parametrize("name", list(FIXTURES))
def test_each_fixture_loads_and_validates_in_memory_and_from_its_file(name, tmp_path):
    """Ext §8 item 8: each fixture is a ship the loader takes, every new spar and line rated
    (no default taken with a warning), and the same ship written out and loaded again."""
    build, doc = FIXTURES[name]
    ship = build()
    assert ship.spec.warnings == []
    again = load_ship(write_ship(doc(), tmp_path, name))
    assert again.spec.warnings == []
    assert again.spec.spars == ship.spec.spars and again.spec.sails == ship.spec.sails
    assert again.spec.lines == ship.spec.lines
    assert again.groups == ship.groups and again.aliases == ship.aliases


def _off_the_mast(mast, x: float, z: float) -> float:
    """How far a point `z` above the deck lies off a lower mast's raked line, fore and aft."""
    return x - (mast.x_m - math.tan(mast.rake) * z)


def _cut_from_its_corners(sail, deck: float) -> None:
    area, cx, cz = area_centroid(sail.corners_m)
    assert sail.area_m2 == pytest.approx(area, abs=0.5)
    assert sail.x_m == pytest.approx(cx, abs=0.05)
    assert sail.centre_height_m == pytest.approx(deck + cz, abs=0.05)  # above the water


def test_the_frigates_fixture_carries_the_mizen_course_on_its_yard_and_the_sprit_yards():
    """Ext §3.4 and §4.1, the parts and their places: the spanker, its gaff and boom and the
    ringtail on the boom gone; the course a lateen cut at the mast on the lateen yard, one
    sheet and one tack and no brace, filed where the spanker was and never among the
    courses; the two yards under the bowsprit and the jib-boom with their square sails, the
    spritsail yard with no halyard, in their own group and "all sail" alone."""
    ship = frigate_with_mizen_yard()
    assert not {"mizzen.spanker", "mizzen.gaff", "mizzen.boom", "ringtail"} & set(ship.parts)
    course = ship.sails["mizzen.course"]
    assert (course.cls, course.cut_at_mast, course.curve_class) == ("lateen", True, "gaff")
    assert ship.yard_of(course).cls == "lateen_yard"
    assert ship.mast_of(course).id == "mizzen.mast" and course.roles["mast"] == "mizzen.mast"
    assert [s.id for s in ship.sails.values() if s.cut_at_mast] == ["mizzen.course"]
    assert not any(s.settee for s in ship.sails.values())
    assert not any(s.heave_to_aback for s in ship.spars.values())
    assert [(ln.cls, ln.side) for ln in ship.lines_of(course)] == [("sheet", None), ("tack", None)]
    assert ship.braces_of("mizzen.yard") == []
    assert {g for g, m in ship.groups.items() if "mizzen.course" in m} == {
        "plain sail",
        "all sail",
        "fore-and-aft sails",
    }
    assert ship.sails["storm_mizzen"].in_place_of == "mizzen.course"
    under = {"spritsail.yard", "sprit_topsail.yard", "spritsail", "sprit_topsail"}
    assert {pid for pid in ship.parts if ship.under_bowsprit(pid)} == under
    assert ship.spars["sprit_topsail.yard"].parent == "jib_boom"
    assert ship.halyard_of("spritsail") is None  # in slings: set as a course, no hoist
    assert ship.halyard_of("sprit_topsail") is not None
    assert {g for g, m in ship.groups.items() if "spritsail" in m} == {"spritsails", "all sail"}


def test_the_frigates_fixture_is_cut_to_the_contracts():
    """Ext §3.4: the course's tack and throat on the mizzen mast's raked line and its throat
    at the yard's truss, within 0.1 m, the head rising aft; its area, x and centre its
    corners'. Ext §4.1 and §6.2: the sprit-topsail yard forward of and above the spritsail
    yard, and the spritsail's foot above the water at no heel, its area hung over nine-tenths
    of its yard as the drawing hangs it."""
    ship = frigate_with_mizen_yard()
    deck = ship.hull.spec.deck_height_m
    mast, yard = ship.spars["mizzen.mast"], ship.spars["mizzen.yard"]
    course = ship.sails["mizzen.course"]
    tack, throat, peak, _clew = course.corners_m
    for x, z in (tack, throat):
        assert abs(_off_the_mast(mast, x, z)) <= 0.1
    assert abs(throat[1] - yard.height_m) <= 0.1
    assert peak[0] < throat[0] and peak[1] > throat[1]
    _cut_from_its_corners(course, deck)
    sprit, sprit_top = ship.spars["spritsail.yard"], ship.spars["sprit_topsail.yard"]
    assert sprit_top.x_m > sprit.x_m and sprit_top.height_m > sprit.height_m
    foot = deck + sprit.height_m - ship.sails["spritsail"].area_m2 / (0.9 * sprit.length_m)
    assert foot > 0.5


def test_the_brigs_fixture_carries_a_settee_on_the_main_and_the_dry_main_yard():
    """Ext §5.1 and §5.7: the main course, the spanker, its gaff and boom and the storm
    trysail gone; the settee a dipping lug on a lug yard on the main, with its own lines (the
    jeers, the derrick, the vangs, the ourses, the tacks, one unsided sheet, the clewlines and
    buntline), among "courses", "plain sail" and "all sail" and called the mainsail; the main
    yard kept bare under the main topsail; the main mast, and it alone, laid aback."""
    ship = brig_with_settee()
    gone = {"main.course", "main.spanker", "main.gaff", "main.boom", "storm_trysail"}
    assert not gone & set(ship.parts)
    settee = ship.sails["main.settee"]
    assert (settee.cls, settee.dipping, settee.settee, settee.curve_class) == (
        "lug",
        True,
        True,
        "lug",
    )
    assert ship.yard_of(settee).id == "main.lug_yard" and settee.roles["mast"] == "main.mast"
    assert [s.id for s in ship.sails.values() if s.settee] == ["main.settee"]
    assert not any(s.cut_at_mast or s.yard_lowered for s in ship.sails.values())
    assert [s.id for s in ship.spars.values() if s.heave_to_aback] == ["main.mast"]
    assert [ln.side for ln in ship.sheets_of(settee)] == [None]
    gear = ("main.lug_yard", "main.settee")
    assert {(ln.cls, ln.of) for ln in ship.lines.values() if ln.of in gear} == {
        ("halyard", "main.lug_yard"),
        ("lift", "main.lug_yard"),
        ("vang", "main.lug_yard"),
        ("guy", "main.lug_yard"),
        ("tack", "main.settee"),
        ("sheet", "main.settee"),
        ("clewline", "main.settee"),
        ("buntline", "main.settee"),
    }
    assert {g for g, m in ship.groups.items() if "main.settee" in m} == {
        "courses",
        "plain sail",
        "all sail",
    }
    assert ship.aliases["mainsail"] == "main.settee"
    assert not any(s.roles.get("yard") == "main.yard" for s in ship.sails.values())
    assert ship.yard_of("main.topsail").id == "main.topsail.yard"


def test_the_brigs_settee_is_cut_to_d5a_and_corrects_the_scratch_variants_faults():
    """D5(a) and Ext §5.1: the luff 0.16 of the leech, the leech and the foot 0.72 of the
    head, the yard at 44 degrees; the point a third along throat to peak on the main mast's
    raked line at the yard's height, within 0.1 m. Eng §4.4's two faults corrected: the
    centre is the corners' centroid above the water (the deck's height above the
    centroid's), and the peak, and the clew with it, are inside the stern."""
    ship = brig_with_settee()
    deck = ship.hull.spec.deck_height_m
    settee = ship.sails["main.settee"]
    tack, throat, peak, clew = settee.corners_m
    head, leech = math.dist(throat, peak), math.dist(peak, clew)
    assert math.dist(tack, throat) / leech == pytest.approx(0.16, abs=0.01)
    assert leech / head == pytest.approx(0.72, abs=0.01)
    assert math.dist(tack, clew) / head == pytest.approx(0.72, abs=0.01)
    slope = math.degrees(math.atan2(peak[1] - throat[1], throat[0] - peak[0]))
    assert slope == pytest.approx(44.0, abs=0.5)
    sling = (throat[0] + (peak[0] - throat[0]) / 3.0, throat[1] + (peak[1] - throat[1]) / 3.0)
    assert abs(_off_the_mast(ship.spars["main.mast"], *sling)) <= 0.1
    assert abs(sling[1] - ship.spars["main.lug_yard"].height_m) <= 0.1
    _cut_from_its_corners(settee, deck)
    stern = -ship.hull.spec.length_waterline_m / 2.0
    assert peak[0] > stern and clew[0] > stern


def _env(ship: Ship, sail) -> expr.Env:
    """The runner's expression environment with `sail` the subject, as an evolution on it
    reads it."""
    inst = Instance(evo=SimpleNamespace(id="test"), subject=sail, subject_id=sail.id, params={})
    return Runner(ship)._env(ship, inst)


def test_class_settee_takes_a_settee_and_nothing_else_and_the_lugs_rows_take_it_too():
    """Ext §5.2: `class: settee` takes a sail with `settee` true, as `class: flying` takes a
    sail set flying; a lug that is no settee and a square sail are refused in the runner's
    words; the settee is still a lug, so the lug's own rows (reef, shake out, trim) take it."""
    brig, lugger = brig_with_settee(), load_ship("data/ships/lugger.yaml")
    evo = SimpleNamespace(id="set_settee", verb="set", applies_to={"class": "settee"})
    Runner._check_applies(evo, brig.sails["main.settee"], "main.settee", brig)
    with pytest.raises(OrderError, match="is a lug sail; 'set_settee' is for a settee sail"):
        Runner._check_applies(evo, lugger.sails["main.lug"], "main.lug", lugger)
    with pytest.raises(OrderError, match="is a square sail; 'set_settee' is for a settee"):
        Runner._check_applies(evo, brig.sails["fore.course"], "fore.course", brig)
    lug = SimpleNamespace(id="reef_lug", verb="reef", applies_to={"class": "lug"})
    Runner._check_applies(lug, brig.sails["main.settee"], "main.settee", brig)


def test_wanted_sheet_is_the_sheet_of_the_sails_curve_class_at_the_apparent_wind():
    """Ext §3.6 and §5.3: `wanted_sheet(sail)` is `trim.wanted_sheet_angle` for the sail's
    curve class: 40 degrees off the wind, a lateen cut at the mast at the gaff's floor of 18
    degrees where a whole lateen and the settee take 15; a square sail, trimmed by its
    braces, is refused in words."""
    awa = math.radians(-40.0)
    frigate, brig = frigate_with_mizen_yard(), brig_with_settee()
    whole = frigate_with_mizen_yard_doc()
    next(s for s in whole["sails"] if s["id"] == "mizzen.course").pop("cut_at_mast")
    whole_ship = ship_from_dict(whole, "whole.yaml")
    for ship, sid, cls, deg in (
        (frigate, "mizzen.course", "gaff", 18.0),
        (whole_ship, "mizzen.course", "lateen", 15.0),
        (brig, "main.settee", "lug", 15.0),
        (frigate, "jib", "jibheaded", 15.0),
    ):
        ship.dyn.apparent_wind_angle = awa
        wanted = expr.evaluate_text("wanted_sheet(sail)", _env(ship, ship.sails[sid]))
        assert wanted == pytest.approx(yard_trim.wanted_sheet_angle(cls, awa))
        assert math.degrees(wanted) == pytest.approx(deg), sid
    with pytest.raises(expr.ExpressionError, match="'fore.course' is not a sail trimmed by"):
        expr.evaluate_text("wanted_sheet(sail)", _env(frigate, frigate.sails["fore.course"]))


def test_the_graph_and_the_snapshot_serve_the_keys_only_where_they_hold(tmp_path):
    """Ext §6.4: `settee` and `cut_at_mast` in the sail's entry of the graph, and
    `yard_lowered` in the snapshot's sail, each only while true, so that every existing
    ship's graph and snapshot are as before."""
    keys = {"settee", "cut_at_mast"}
    for ship, key, sid in (
        (frigate_with_mizen_yard(), "cut_at_mast", "mizzen.course"),
        (brig_with_settee(), "settee", "main.settee"),
    ):
        sails = queries.ship_graph(ship)["sails"]
        assert [(s["id"], s[key]) for s in sails if key in s] == [(sid, True)]
        assert not [s["id"] for s in sails if (keys - {key}) & set(s)]
    for name in TABLE:
        sails = queries.ship_graph(load_ship(f"data/ships/{name}.yaml"))["sails"]
        assert not [s["id"] for s in sails if keys & set(s)], name
    world = make_world(7, write_ship(brig_with_settee_doc(), tmp_path, "brig"), Scenario())
    assert not [s["id"] for s in queries.snapshot(world)["sails"] if "yard_lowered" in s]
    world.ship.sails["main.settee"].yard_lowered = True
    sails = queries.snapshot(world)["sails"]
    assert [(s["id"], s["yard_lowered"]) for s in sails if "yard_lowered" in s] == [
        ("main.settee", True)
    ]


# -- the driver's stage 0 (Ext §17.4, §17.7, §17.8) ----------------------------------------


def _rig_with_boom(**course) -> dict:
    """The hand-built rig with a boom on the mizzen mast and the mizen course naming it, the
    course's keys given `course` (None taking a key out)."""
    doc = _rig("mizzen.course", boom="mizzen.boom", **course)
    boom = {"id": "mizzen.boom", "class": "boom", "on": "mizzen.mast", "length_m": 12.0}
    doc["spars"].insert(6, dict(boom, height_m=3.0))
    return doc


def test_a_boom_spreads_a_lateen_cut_at_the_mast_and_is_refused_on_a_whole_one():
    """Ext §17.4: a lateen cut at the mast (a driver) names a boom and loads with the role; a
    whole lateen naming one is refused in words; a lateen's boom is a boom."""
    ship = ship_from_dict(_rig_with_boom(), "rig.yaml")
    course = ship.sails["mizzen.course"]
    assert course.roles["boom"] == "mizzen.boom" and course.cut_at_mast
    assert ship.spec.sails[2].roles == {
        "yard": "mizzen.yard",
        "mast": "mizzen.mast",
        "boom": "mizzen.boom",
    }
    whole = _rig_with_boom(cut_at_mast=None, mast=None, corners_m=None)
    with pytest.raises(ShipFileError) as e:
        ship_from_dict(whole, "bad.yaml")
    assert str(e.value) == (
        "bad.yaml: sail 'mizzen.course' is a whole lateen and names a boom; only a lateen cut at "
        "the mast (a driver) is spread on a boom."
    )
    yard_for_boom = _rig_with_boom()
    next(s for s in yard_for_boom["sails"] if s["id"] == "mizzen.course")["boom"] = "fore.yard"
    with pytest.raises(ShipFileError, match="names 'fore.yard' as its boom, but that is a yard"):
        ship_from_dict(yard_for_boom, "bad.yaml")


def _off_the_line(p, a, b) -> float:
    """How far the point p lies off the straight line through a and b."""
    (x, z), (x0, z0), (x1, z1) = p, a, b
    return abs((x1 - x0) * (z0 - z) - (x0 - x) * (z1 - z0)) / math.hypot(x1 - x0, z1 - z0)


def test_the_driver_fixture_is_cut_to_its_contract():
    """Ext §17.2's generator assertions on the fixture (§17.8): the throat at the course's
    throat, and the tack on the mast's raked line at the boom's jaws, within 0.1 m; the foot on
    the boom's line, the clew within the boom's length; the peak on the mizen yard's line within
    0.1 m, abaft and above the yard's peak by no more than two-thirds of the driver yard; the four
    corners' area within 10% of Steel's rule, and the sail's area, x and centre its corners'."""
    ship = frigate_with_driver()
    deck = ship.hull.spec.deck_height_m
    mast, boom = ship.spars["mizzen.mast"], ship.spars["mizzen.boom"]
    driver, course = ship.sails["mizzen.driver"], ship.sails["mizzen.course"]
    tack, throat, peak, clew = driver.corners_m
    _c_tack, c_throat, yard_peak, _c_clew = course.corners_m
    assert math.dist(throat, c_throat) <= 0.1
    assert abs(_off_the_mast(mast, *tack)) <= 0.1 and abs(tack[1] - boom.height_m) <= 0.1
    assert boom.length_m == DRIVER_BOOM_M
    assert clew[1] == pytest.approx(boom.height_m, abs=0.1)  # the boom lies level
    assert 0.0 < tack[0] - clew[0] <= boom.length_m
    assert _off_the_line(peak, c_throat, yard_peak) <= 0.1
    assert peak[0] < yard_peak[0] and peak[1] > yard_peak[1]
    assert math.dist(peak, yard_peak) <= 2.0 / 3.0 * DRIVER_YARD_M
    area, _cx, _cz = area_centroid(driver.corners_m)
    assert area == pytest.approx(DRIVER_STEEL_AREA_M2, rel=0.10)
    _cut_from_its_corners(driver, deck)


def test_the_driver_is_filed_in_the_courses_place_with_its_boom_lines_and_names():
    """Ext §17.2 and §17.8: the driver a lateen cut at the mast on the mizen yard, the mast and
    the boom, filed after the course (the yard's sail stays the course) in its place, in the sail
    room with one spare; the storm mizzen in the course's place too; no ringtail; its group the
    occasional sails' alone, its names, and Steel's four lines; bent, the course is in the sail
    room in its stead."""
    ship = frigate_with_driver()
    driver = ship.sails["mizzen.driver"]
    order = [s.id for s in ship.spec.sails]
    assert order.index("mizzen.driver") == order.index("mizzen.course") + 1
    assert (driver.cls, driver.cut_at_mast, driver.curve_class) == ("lateen", True, "gaff")
    assert driver.roles == {"yard": "mizzen.yard", "mast": "mizzen.mast", "boom": "mizzen.boom"}
    assert driver.state == SailState.UNBENT and driver.reef_bands == 0
    assert ship.sail_of("mizzen.yard").id == "mizzen.course"
    assert {s.id for s in ship.spec.sails if s.in_place_of == "mizzen.course"} == {
        "mizzen.driver",
        "storm_mizzen",
    }
    assert not {"ringtail", "ringtail_boom", "mizzen.gaff", "mizzen.spanker"} & set(ship.parts)
    assert ship.spars["mizzen.boom"].parent == "mizzen.mast"
    assert {g for g, m in ship.groups.items() if "mizzen.driver" in m} == {"occasional sails"}
    assert {a for a, t in ship.aliases.items() if t == "mizzen.driver"} == {
        "driver",
        "spanker",
        "driver boomsail",
    }
    assert {a for a, t in ship.aliases.items() if t == "mizzen.boom"} == {
        "driver boom",
        "spanker boom",
    }
    lines = {(ln.cls, ln.side, ln.parts) for ln in ship.lines_of(driver)}
    assert lines == {
        ("halyard", None, 1),
        ("tack", None, 1),
        ("sheet", None, 2),
        ("downhaul", None, 1),
    }
    room = frigate_with_driver_doc()["crew"]["stores"]["sails"]
    assert [s["canvas_no"] for s in room if s["kind"] == "mizzen.driver"] == [5]
    bent = frigate_with_driver(bent=True)
    assert bent.sails["mizzen.driver"].state != SailState.UNBENT
    assert bent.sails["mizzen.course"].state == SailState.UNBENT
    assert bent.sails["mizzen.driver"].corners_m == driver.corners_m
