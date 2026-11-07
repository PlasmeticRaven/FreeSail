"""Package 75, B3.4: the schooner's mast (`Ship.on_schooner_mast`), the lead's ruling of
2026-11-06 on docs/design/Design-Ship-PrinceDeNeufchatel.md §12.2a, "the rule in the key's
place": "An after mast with yards and no yard on its lower mast handles as a fore-and-after's
mast", read from the parts as filed, once a ship, the yards under the bowsprit not counted. It
is read at two places (docs/design/Design-ShipsEngineExtensions.md §4.2): place 1,
`scripts._masts_with_yards`, which skips such yards, and place 3, `physics.sails._square_rigged`,
which counts none; and, by the lead's ruling 1 of 2026-11-06 on place 2's timing (after Luce
1884 p. 417), for the time of the tack's swing at "mainsail haul", short for a schooner's light
main yards (`scripts.TackScript._after_swing_s`).

No committed ship file trips it (the guard, every file of `data/ships/` with the boats), so no
file's classing moves: the golden table's own run (`tests/test_rig_classing.py`, and the razee's
and the 64's rows in `tests/test_indefatigable.py`) is that proof, and is not repeated here.
Here: the rigs in memory (`tests/rig_fixtures.py`) classed through the golden table's gates, the
topsail schooner with the *Neufchatel*'s main topgallant and with a main topsail (Eng §3.3's
trial B) fore-and-afters with the fore's yards their head yards and the main's their after yards
and the fore laid aback, trial A as it was, the tartane classed as the cutter is and the polacre
with her main her one mast with yards; the yards under the bowsprit, a lug's and a lateen yard
counted for nothing; a brig whose main yard is shot away and sent down a brig still; the answer
held once a ship, and the schooner whose fore yards are all shot away pinned as she stands (the
case reported to the lead); the pickle and the checkpoint of a rig that has read the rule as
they were before it read it; and the short after swing, a schooner's light main yards' alone,
trial B's tack with it, and the word they are hauled by, "Main-topsail haul" (the lead's ruling
2, Luce 1884 p. 417: her main crosses no course).
"""

from __future__ import annotations

import copy
import pickle
from pathlib import Path

import pytest
from rig_fixtures import (
    frigate_with_mizen_yard,
    polacre_probe,
    schooner_with_fore_course,
    schooner_with_main_topgallant,
    schooner_with_main_topsail,
    schooner_with_main_topsail_doc,
    tartane_probe,
    write_ship,
)

from freesail.api.session import make_world
from freesail.core.replay import checkpoint_bytes, read_checkpoint, write_checkpoint
from freesail.core.world import Scenario
from freesail.evolutions import EVOLUTIONS, scripts
from freesail.physics.sails import _square_rigged
from freesail.ship import graph
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))


def _under_plain_sail(ship: Ship) -> Ship:
    """Her plain sail set, as the golden table reads a rig (the polar's way)."""
    for sid in ship.groups.get("plain sail", []):
        ship.sails[sid].state = SailState.SET
    return ship


def _classing(ship: Ship) -> dict:
    """The golden table's gates, by id: the masts with yards, the head and after yards, the
    yards laid aback to heave to (with sail set on them, as the heave-to takes them), whether
    she is square-rigged, the driver brailed up hove to, and the gaff sails on a boom she gets
    under way under."""
    head, after = scripts.head_and_after_yards(ship)
    back = scripts.yards_to_back(ship)
    return {
        "masts": [m.id for m in scripts._masts_with_yards(ship)],
        "head": [y.id for y in head],
        "after": [y.id for y in after],
        "backed": ship.mast_of(back[0]).id if back else None,
        "to_back": [y.id for y in back],
        "to_back_set": [y.id for y in scripts.yards_to_back_set(ship)],
        "square": _square_rigged(ship),
        "driver": [s.id for s in scripts.after_gaff_sails(ship)],
        "boom_mainsails": [s.id for s in scripts._boom_mainsails(ship)],
    }


FORE = ["fore.yard", "fore.topsail.yard", "fore.topgallant.yard"]
SCHOONER_MAINSAILS = ["main.sail", "storm_trysail"]

# Each rig's gates as the rule classes it, measured on this tree (the tuning notes, "The
# schooner's mast", old beside new). Trial A has no yard on her main and is a fore-and-after with
# or without the rule; the two with yards on the main above its lower mast were brigs before it.
ROWS = {
    "fore course (trial A)": (
        schooner_with_fore_course,
        {
            "masts": ["fore.mast"],
            "head": FORE,
            "after": [],
            "backed": "fore.mast",
            "to_back": FORE,
            "to_back_set": FORE,
            "square": False,
            "driver": [],
            "boom_mainsails": SCHOONER_MAINSAILS,
        },
    ),
    "main topgallant": (
        schooner_with_main_topgallant,
        {
            "masts": ["fore.mast"],
            "head": FORE,
            "after": ["main.topsail.yard", "main.topgallant.yard"],
            "backed": "fore.mast",
            "to_back": FORE,
            "to_back_set": FORE,
            "square": False,
            "driver": [],
            "boom_mainsails": SCHOONER_MAINSAILS,
        },
    ),
    "main topsail (trial B)": (
        schooner_with_main_topsail,
        {
            "masts": ["fore.mast"],
            "head": FORE,
            "after": ["main.topsail.yard"],
            "backed": "fore.mast",
            "to_back": FORE,
            "to_back_set": FORE,
            "square": False,
            "driver": [],
            "boom_mainsails": SCHOONER_MAINSAILS,
        },
    ),
    "polacre": (
        polacre_probe,
        {
            "masts": ["main.mast"],
            "head": ["main.yard", "main.topsail.yard"],
            "after": [],
            "backed": "main.mast",
            "to_back": ["main.yard", "main.topsail.yard"],
            "to_back_set": ["main.yard", "main.topsail.yard"],
            "square": False,
            "driver": [],
            "boom_mainsails": [],
        },
    ),
}


# -- the guard: no committed file trips the rule --------------------------------------------


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_no_committed_ship_file_has_a_yard_or_a_square_sail_on_a_schooners_mast(path):
    """Every file of `data/ships/`, the boats among them: on every after mast with yards a yard
    is crossed on the lower mast itself (the brigs and the three-masted ships), or one mast
    carries every braced yard (the schooners, the cutter, the smack), or none does (the lugger
    and the boats, whose yards are lug yards). So places 1 and 3 read every committed file as
    before the rule."""
    ship = load_ship(path)
    yards = [p for p in ship.spars.values() if p.cls == "yard"]
    squares = [s for s in ship.sails.values() if s.cls == "square"]
    assert [p.id for p in yards + squares if ship.on_schooner_mast(p)] == []
    assert [pid for pid in ship.parts if ship.on_schooner_mast(pid)] == []


def test_the_guard_reads_fifteen_files_and_the_brigs_main_yards_among_them():
    """The guard is not empty: the fifteen files of the tree, and the brig's main topsail,
    topgallant and royal yards, which a rule without its lower-yard test would name."""
    assert len(SHIP_FILES) == 15
    brig = load_ship(ROOT / "data" / "ships" / "brig.yaml")
    upper = ["main.topsail.yard", "main.topgallant.yard", "main.royal.yard"]
    assert all(brig.spars[y].parent != "main.mast" for y in upper)
    assert brig.spars["main.yard"].parent == "main.mast"
    assert not any(brig.on_schooner_mast(y) for y in upper)


# -- the rigs in memory ------------------------------------------------------------------------


@pytest.mark.parametrize("name", list(ROWS))
def test_each_rig_is_classed_through_the_golden_tables_gates(name):
    build, row = ROWS[name]
    assert _classing(_under_plain_sail(build())) == row


@pytest.mark.parametrize(
    "build, named",
    [
        (schooner_with_main_topgallant, ["main.topsail.yard", "main.topgallant.yard"]),
        (schooner_with_main_topsail, ["main.topsail.yard"]),
    ],
    ids=["main topgallant", "main topsail"],
)
def test_the_yards_on_the_schooners_main_are_hers_and_the_main_is_no_mast_with_yards(build, named):
    """The rule's yards and their square sails, and nothing else; the yards still braced
    (`working_yards`, her design's §12.2 item 5) and her after yards; the main's own yards the
    aftermost mast's no longer (`after_square_yards` the fore's)."""
    ship = _under_plain_sail(build())
    sails = [ship.sail_of(y).id for y in named if ship.sail_of(y) is not None]
    assert sorted(p for p in ship.parts if ship.on_schooner_mast(p)) == sorted(named + sails)
    assert set(named) <= {y.id for y in scripts.working_yards(ship)}
    assert [y.id for y in scripts.after_square_yards(ship)] == FORE
    assert [y.id for y in scripts.head_and_after_yards(ship)[1]] == named


def test_trial_a_classes_as_it_did_before_the_rule():
    """Trial A has no yard on her main: the rule names nothing in her, so her row is the row
    she had before it, a fore-and-after with three head yards (Eng §3.3)."""
    ship = _under_plain_sail(schooner_with_fore_course())
    assert [p for p in ship.parts if ship.on_schooner_mast(p)] == []
    assert _classing(ship) == ROWS["fore course (trial A)"][1]


def test_the_tartane_classes_as_the_cutter_does():
    """Her lateen yard is no braced yard, so her square topsail's mast is her one mast with
    yards, as the cutter's is: the same gates, her topsail laid aback hove to, not
    square-rigged, no driver. Her sails differ (no gaff mainsail on a boom), so the gates that
    name sails are her own."""
    tartane = _classing(_under_plain_sail(tartane_probe()))
    cutter = _classing(_under_plain_sail(load_ship(ROOT / "data" / "ships" / "cutter.yaml")))
    gates = ("masts", "after", "backed", "square", "driver")
    assert {k: tartane[k] for k in gates} == {k: cutter[k] for k in gates}
    assert tartane["masts"] == ["main.mast"] and tartane["head"] == ["topsail.yard"]
    assert tartane["to_back"] == ["topsail.yard"] and tartane["boom_mainsails"] == []
    ship = tartane_probe()
    assert {s.cls for s in ship.spars.values() if s.id.endswith("lateen_yard")} == {"lateen_yard"}
    assert not any(ship.on_schooner_mast(p) for p in ship.parts)


def test_the_polacre_has_her_square_main_between_two_lateens_for_her_one_mast_with_yards():
    """A record of the reading, as the lead ruled it, more than a test of the rule: her lateens
    are no braced yards and her main has its lower yard, so the rule names nothing in her
    whether it counts lower yards or not (her classing is the row above)."""
    ship = polacre_probe()
    assert [s.id for s in ship.spars.values() if s.cls == "lateen_yard"] == [
        "fore.lateen_yard",
        "mizzen.lateen_yard",
    ]
    assert ship.spars["main.yard"].parent == "main.mast"
    assert not any(ship.on_schooner_mast(p) for p in ship.parts)


# -- what counts for nothing --------------------------------------------------------------------

# A hand-built rig (round figures, not a ship's): a fore with a lower yard, a main with a yard
# on its topmast alone, a mizen with a lug yard on its lower mast and a topsail yard over it,
# and a spritsail yard under the bowsprit.
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
        {"id": "fore.yard", "class": "yard", "on": "fore.mast", "length_m": 16.0, "height_m": 14.0},
        {"id": "main.mast", "class": "mast", "x_m": 0.0, "height_m": 20.0},
        {"id": "main.topmast", "class": "topmast", "steps_on": "main.mast", "height_m": 8.0},
        {
            "id": "main.topsail.yard",
            "class": "yard",
            "on": "main.topmast",
            "length_m": 10.0,
            "height_m": 24.0,
        },
        {"id": "mizzen.mast", "class": "mast", "x_m": -10.0, "height_m": 16.0},
        {"id": "mizzen.topmast", "class": "topmast", "steps_on": "mizzen.mast", "height_m": 6.0},
        {"id": "mizzen.lug_yard", "class": "lug_yard", "on": "mizzen.mast", "length_m": 9.0},
        {
            "id": "mizzen.topsail.yard",
            "class": "yard",
            "on": "mizzen.topmast",
            "length_m": 7.0,
            "height_m": 19.0,
        },
        {"id": "bowsprit", "class": "bowsprit", "x_m": 20.0, "length_m": 12.0, "height_m": 2.0},
        {
            "id": "spritsail.yard",
            "class": "yard",
            "on": "bowsprit",
            "length_m": 12.0,
            "height_m": 3.0,
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
            "id": "main.topsail",
            "class": "square",
            "yard": "main.topsail.yard",
            "area_m2": 60,
            "x_m": 0.0,
            "centre_height_m": 22.0,
        },
        {
            "id": "mizzen.lug",
            "class": "lug",
            "yard": "mizzen.lug_yard",
            "area_m2": 40,
            "x_m": -11.0,
            "centre_height_m": 8.0,
        },
        {
            "id": "mizzen.topsail",
            "class": "square",
            "yard": "mizzen.topsail.yard",
            "area_m2": 30,
            "x_m": -10.0,
            "centre_height_m": 18.0,
        },
        {
            "id": "spritsail",
            "class": "square",
            "yard": "spritsail.yard",
            "area_m2": 50,
            "x_m": 24.0,
            "centre_height_m": 3.0,
        },
    ],
    "lines": [],
}


def _rig(*gone: str) -> Ship:
    doc = copy.deepcopy(RIG)
    doc["spars"] = [s for s in doc["spars"] if s["id"] not in gone]
    doc["sails"] = [s for s in doc["sails"] if s.get("yard") not in gone]
    return ship_from_dict(doc, "rig.yaml")


def test_a_lug_yard_is_no_lower_yard_and_the_bowsprits_yards_count_for_nothing():
    """The main's topsail yard and the mizen's are on schooner's masts: neither mast has a
    braced yard on its lower mast, the mizen's lug yard being none (judgement: a lug's and a
    lateen yard have classes of their own). The spritsail yard is on no mast and is never
    one; the fore, the foremost with yards, never."""
    ship = _rig()
    named = {"main.topsail.yard", "main.topsail", "mizzen.topsail.yard", "mizzen.topsail"}
    assert {p for p in ship.parts if ship.on_schooner_mast(p)} == named
    assert [m.id for m in scripts._masts_with_yards(ship)] == ["fore.mast"]
    assert _square_rigged(ship) is False
    assert not ship.on_schooner_mast("mizzen.lug_yard") and not ship.on_schooner_mast("spritsail")


def test_with_no_yard_on_the_fore_the_main_is_the_foremost_and_the_bowsprit_no_mast():
    """Without the fore's yard the main is the foremost lower mast with yards, though the
    spritsail yard is crossed forward of it: the yards under the bowsprit count for nothing,
    not even to make the bowsprit the foremost. The mizen abaft the main is a schooner's."""
    ship = _rig("fore.yard")
    assert {p for p in ship.parts if ship.on_schooner_mast(p)} == {
        "mizzen.topsail.yard",
        "mizzen.topsail",
    }
    assert [m.id for m in scripts._masts_with_yards(ship)] == ["main.mast"]
    assert scripts.head_and_after_yards(ship)[0][0].id == "main.topsail.yard"


def test_the_frigates_crossjack_keeps_her_mizen_a_mast_with_a_lower_yard():
    """The frigate's fixture, her mizen course a lateen cut at the mast on its lateen yard: the
    crossjack yard crossed on the mizen's lower mast beside it keeps the mizen a mast with a
    lower yard, so her mizen topsail, topgallant and royal yards are no schooner's, and her
    spritsail and sprit-topsail yards under the bowsprit are named nothing. (That the yards
    under the bowsprit make no foremost mast is the hand-built rig's test above: the fore
    here has its own yards and is the foremost either way.)"""
    ship = frigate_with_mizen_yard()
    assert ship.spars["mizzen.crossjack.yard"].parent == "mizzen.mast"
    assert ship.spars["mizzen.yard"].cls == "lateen_yard"
    assert not any(ship.on_schooner_mast(p) for p in ship.parts)
    assert "mizzen.mast" in [m.id for m in scripts._masts_with_yards(ship)]


# -- as filed, and once a ship -------------------------------------------------------------------


def _shot_away(ship: Ship, *yards: str) -> None:
    for y in yards:
        ship.spars[y].wrecked = True
        ship.spars[y].sent_down = True


def test_a_brig_whose_main_yard_is_shot_away_and_sent_down_stays_a_brig():
    """Read from the parts as filed, wrecked or sent down or not: the brig's main yard wrecked
    and sent down before the rule is first read leaves her main a mast with a lower yard, so
    her main topsail, topgallant and royal yards are no schooner's and she is a brig still,
    square-rigged, her spanker her driver."""
    brig = _under_plain_sail(load_ship(ROOT / "data" / "ships" / "brig.yaml"))
    _shot_away(brig, "main.yard")
    assert "main.yard" not in {y.id for y in scripts.working_yards(brig)}
    assert not any(brig.on_schooner_mast(p) for p in brig.parts)
    assert [m.id for m in scripts._masts_with_yards(brig)] == ["fore.mast", "main.mast"]
    assert _square_rigged(brig) is True
    assert [s.id for s in scripts.after_gaff_sails(brig)] == ["main.spanker"]


def test_the_answer_is_found_once_a_ship_and_held_through_the_fight():
    """Read once, held: the schooner with a main topsail keeps her main topsail yard a
    schooner's with her fore yards all shot away and sent down after the first reading (her
    main would be the foremost with working yards then), and the brig keeps her main a brig's
    with her main yard gone after it. The same set answers every reading."""
    ship = schooner_with_main_topsail()
    assert ship.on_schooner_mast("main.topsail.yard")
    held = ship._schooner_yards()
    _shot_away(ship, *FORE)
    assert ship.on_schooner_mast("main.topsail.yard") and ship.on_schooner_mast("main.topsail")
    assert ship._schooner_yards() is held
    brig = load_ship(ROOT / "data" / "ships" / "brig.yaml")
    assert not brig.on_schooner_mast("main.topsail.yard")
    _shot_away(brig, "main.yard")
    assert not any(brig.on_schooner_mast(p) for p in brig.parts)


def test_with_every_fore_yard_shot_away_her_main_yards_are_in_neither_list():
    """The case reported to the lead at B3.4, pinned as it stands, place 2 being left: the rule
    is the rig's, so with every fore yard shot away her main is a schooner's still, no mast
    carries yards at place 1, and `head_and_after_yards` gives her neither head yards nor after
    yards, where before the rule her main topsail yard was her head yard; it is a working yard
    still, braced by the brace orders and "trim sails". A ruling at place 2 moves this pin."""
    ship = schooner_with_main_topsail()
    _shot_away(ship, *FORE)
    assert [y.id for y in scripts.working_yards(ship)] == ["main.topsail.yard"]
    assert scripts._masts_with_yards(ship) == []
    assert scripts.head_and_after_yards(ship) == ([], [])
    assert scripts.yards_to_back(ship) == []


def test_each_ship_finds_her_own():
    """Held a ship, not a file or a class: two ships built from one file (the topsail
    schooner's, with a main topsail and without) answer apart."""
    one, two = schooner_with_main_topsail(), schooner_with_fore_course()
    assert one.on_schooner_mast("main.topsail.yard")
    assert not any(two.on_schooner_mast(p) for p in two.parts)
    assert one._schooner_yards() is not two._schooner_yards()


# -- the short after swing (the lead's ruling 1 of 2026-11-06, place 2's timing) -------------------


def _after_swing_s(ship: Ship) -> float:
    """The tack's after swing at "mainsail haul" for her, before the weather and the hands."""
    return scripts.TackScript(ship, {}, EVOLUTIONS["tack"].timing)._after_swing_s()


@pytest.mark.parametrize(
    ("build", "seconds"),
    [
        (schooner_with_main_topsail, 20.0),
        (schooner_with_main_topgallant, 20.0),
        (schooner_with_fore_course, 45.0),
        (polacre_probe, 45.0),
        (frigate_with_mizen_yard, 45.0),
    ],
    ids=["trial B", "main topgallant", "trial A", "polacre", "frigate with a mizen yard"],
)
def test_the_short_after_swing_is_a_schooners_light_main_yards_alone(build, seconds):
    """The short after swing, `light_after_swing_s` (20 s), when every after yard is on a
    schooner's mast: trial B's main topsail yard, the main topgallant's two light yards. Trial A
    and the polacre have no after yards and the frigate's are on masts with lower yards: each
    swings in `brace_s` (45 s) as before the ruling (and an empty swing is done at once)."""
    assert _after_swing_s(build()) == seconds


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_no_committed_ship_file_swings_her_after_yards_short(path):
    """No file has a yard on a schooner's mast (the guard above), so every ship of every file,
    the brig's and the frigate's after yards among them, swings in `brace_s` at "mainsail haul"
    as before: the short swing for every ship's after yards is the lead's, not built."""
    assert _after_swing_s(load_ship(path)) == EVOLUTIONS["tack"].timing["brace_s"]


@pytest.mark.parametrize(
    ("build", "said"),
    [
        (schooner_with_main_topsail, "Rise tacks and sheets. Main-topsail haul"),
        (schooner_with_main_topgallant, "Rise tacks and sheets. Main-topsail haul"),
        (polacre_probe, None),
        (schooner_with_fore_course, None),
    ],
    ids=["trial B", "main topgallant", "polacre", "trial A"],
)
def test_a_schooners_main_yards_are_hauled_by_main_topsail_haul(build, said):
    """The lead's ruling 2 of 2026-11-06 (Luce 1884 p. 417): a schooner's main crosses no course,
    so her mainsail is never set and her after yards, the main topsail yard or the main
    topgallant's two, are hauled by "Main-topsail haul!", her fore course's tacks and sheets
    risen with it while it is set ("Rise tacks and sheets. Mainsail haul." before the ruling).
    The polacre and trial A have no after yards and say nothing at the haul, as before."""
    ship = _under_plain_sail(build())
    tack = scripts.TackScript(ship, {}, EVOLUTIONS["tack"].timing)
    assert (tack._haul_words() if tack.after else None) == said


def test_trial_b_hauls_her_main_topsail_yard_short_and_comes_round_as_trial_a_does(tmp_path):
    """Trial B tacked at seed 7 in 15 knots, settled 2,400 s under plain sail braced sharp up and
    trimmed every two minutes (B3.4's measure; the tuning notes, "The lead's four rulings,
    built"): "Rise tacks and sheets. Main-topsail haul." at 32 s, her head 9 degrees short of
    the wind (her main crossing no course, the word is Luce's for the mainsail not set, the
    lead's ruling 2; "Rise tacks and sheets. Mainsail haul." before it, the rise of her fore
    course's tacks and sheets kept); the main topsail yard swung in 26 s (the short swing's 20 s
    by the weather and the hands) where the 45-s swing took 59 s; "Let go and haul." at 58 s
    where it waited to 91 s, the fore yards no longer held aback with her head through the wind;
    tacked in 151 s where it was 219 s, within the schooner's two and a half minutes and 2 s over
    trial A's 149 s."""
    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
    )
    world = make_world(7, write_ship(schooner_with_main_topsail_doc(), tmp_path), sc)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    for i in range(2400):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    start = world.clock.tick
    world.submit("tack ship")
    ends = ("ship.tacked", "ship.missed_stays", "ship.fell_off", "evolution.failed")
    done: list = []
    while not done and world.clock.tick - start < 900:
        world.tick()
        done = [e.kind for e in world.log if e.tick > start and e.kind in ends]
    haul = "Rise tacks and sheets. Main-topsail haul."
    said: dict[str, int] = {}
    for e in world.log:
        for key in (haul, "Mainsail haul", "Let go and haul"):
            if e.tick >= start and key in e.text:
                said.setdefault(key, e.tick - start)
    assert done == ["ship.tacked"]
    assert set(said) == {haul, "Let go and haul"}  # no "Mainsail haul" (ruling 2)
    assert 20 <= said["Let go and haul"] - said[haul] <= 30  # 26 s; 59 s on brace_s
    assert 90 <= world.clock.tick - start <= 180  # 151 s; 219 s on brace_s
    assert world.ship.dyn.tack == "larboard"


# -- the pickle and the checkpoint -----------------------------------------------------------------


def test_the_pickle_of_a_rig_that_has_read_the_rule_is_as_before_it_read_it():
    """The answer is held beside the ship and not in her, and found without `mast_of`'s memo,
    so her pickled state is the same byte for byte; read back, she finds the same yards."""
    ship = schooner_with_main_topsail()
    assert graph._SCHOONER_YARDS.get(ship) is None  # not read yet
    before = pickle.dumps(ship)
    named = {p for p in ship.parts if ship.on_schooner_mast(p)}
    assert named == {"main.topsail.yard", "main.topsail"}
    after = pickle.dumps(ship)
    assert after == before
    again = pickle.loads(after)
    assert {p for p in again.parts if again.on_schooner_mast(p)} == named


def test_a_checkpoint_of_a_rig_that_has_read_the_rule_is_as_before_it(tmp_path):
    """The checkpoint (`core.replay`, which pickles the ship's own state): a World on the
    schooner with a main topsail, its checkpoint taken before the rule is read and after, at
    the start and after a minute's sailing, the same bytes; a World read back from it answers
    the rule as the one that ran on."""
    world = make_world(7, write_ship(schooner_with_main_topsail_doc(), tmp_path), Scenario())
    ship = world.ship
    assert graph._SCHOONER_YARDS.get(ship) is None  # not read yet
    before = checkpoint_bytes(world)
    named = {p for p in ship.parts if ship.on_schooner_mast(p)}
    assert named == {"main.topsail.yard", "main.topsail"}
    assert checkpoint_bytes(world) == before
    world.run(60)
    ran = checkpoint_bytes(world)
    assert not _square_rigged(ship)  # the helm's mark has read the rule
    assert {p for p in ship.parts if ship.on_schooner_mast(p)} == named
    assert checkpoint_bytes(world) == ran
    _header, back = read_checkpoint(write_checkpoint(world, tmp_path / "rig.checkpoint"))
    assert {p for p in back.ship.parts if back.ship.on_schooner_mast(p)} == named
    assert [m.id for m in scripts._masts_with_yards(back.ship)] == ["fore.mast"]
