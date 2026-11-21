"""Package 90, A5: a yard's level read from its order on its lower mast (`Ship.yard_level`).

The engine read a yard's level from the class of the spar it hangs on (`mast` a course, `topmast` a
topsail, and up), at twelve places (docs/design/Design-Ship-Polacre.md §5.1). On a pole mast, the
mast and topmast in one stick, a topsail yard crosses the mast's own head and was a course. One
predicate now: the level of the spar it hangs on and one more for each braced yard on the same
spar below it; a square yard over a whole lateen with no braced yard below it counts the lateen
yard as its level below (JUDGEMENT, the lead's lean ruled, Plan §13.1 item 2). On every committed
file but the smack it is what the spar's class gave; her topsail becomes a topsail, so that hove to
with it set it goes to the mast as a fore-and-after's topsail does, and she lies a-try under it.
docs/dev/TuningNotes.md, "Package 90, A5 and A6".
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from rig_fixtures import polacre_probe_doc, tartane_probe_doc, write_ship

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.orders import verbs
from freesail.ship.loader import load_ship

SHIP_FILES = sorted(Path("data/ships").glob("*.yaml"))
SPAR_LEVELS = ("mast", "topmast", "topgallant_mast", "royal_mast")


def _by_its_spar(ship, yard) -> int:
    """The level as the engine read it before A5: the class of the spar it hangs on."""
    if ship.under_bowsprit(yard):
        return -1
    parent = ship.parent_of(yard)
    return SPAR_LEVELS.index(parent.cls) if parent is not None and parent.cls in SPAR_LEVELS else 0


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_every_files_yard_levels_are_as_they_were_but_the_smacks_topsail(path):
    """The guard, old beside new: every braced yard of every committed file at the level the
    class of its spar gave it, the smack's topsail alone moving, 0 (a course) to 1 (a topsail):
    the one committed yard crossing a mast's own head over another (`data/ships/smack.yaml`)."""
    ship = load_ship(path)
    moved = {
        sp.id: (_by_its_spar(ship, sp), ship.yard_level(sp))
        for sp in ship.spars.values()
        if sp.cls == "yard" and _by_its_spar(ship, sp) != ship.yard_level(sp)
    }
    assert moved == ({"topsail.yard": (0, 1)} if path.stem == "smack" else {})


def _pole_polacre(tmp_path) -> Path:
    """The polacre probe with her main a pole: the topsail yard crossing the lower mast's head."""
    doc = polacre_probe_doc()
    for s in doc["spars"]:
        if s["id"] == "main.topsail.yard":
            s["on"], s["height_m"] = "main.mast", 15.6
    return write_ship(doc, tmp_path, "pole-polacre")


def test_on_a_pole_main_the_topsail_yard_is_a_topsail_at_every_place(tmp_path):
    """Her main course 0 and its topsail 1 though both hang on the lower mast; so the courses are
    the course alone (`lowest_square_sails`: the heave-to's "Hauled up the courses."), the topsails
    the topsail (lie a-try's, the gale's), the take-in's word a topsail's ("clew up", not "haul
    up"), and the trim's stagger braces it in from the yard below."""
    ship = load_ship(_pole_polacre(tmp_path))
    assert ship.parent_of("main.topsail.yard").id == "main.mast"
    assert [ship.yard_level(y) for y in ("main.yard", "main.topsail.yard")] == [0, 1]
    assert [sl.id for sl in scripts.lowest_square_sails(ship)] == ["main.course"]
    assert [sl.id for sl in scripts._topsails(ship)] == ["main.topsail"]
    assert verbs._take_in_kind(ship, ship.sails["main.topsail"]) == "square"
    assert verbs._take_in_kind(ship, ship.sails["main.course"]) == "course"
    yards = [ship.spars["main.yard"], ship.spars["main.topsail.yard"]]
    assert scripts._topsails_on(ship, yards) == [ship.sails["main.topsail"]]


def test_a_square_yard_over_a_whole_lateen_counts_the_lateen_yard_below_it(tmp_path):
    """The tartane probe with her topsail yard on her pole main's head and no braced yard below
    it, her great lateen's yard below: a topsail (1), not a course. With a gaff sail in the
    lateen's place it is the mast's lowest braced yard, a course, as the rule has always read."""
    doc = tartane_probe_doc()
    for s in doc["spars"]:
        if s["id"] == "topsail.yard":
            s["on"], s["height_m"] = "main.mast", 15.6
    ship = load_ship(write_ship(doc, tmp_path, "pole-tartane"))
    assert ship.yard_level("topsail.yard") == 1
    assert scripts.lowest_square_sails(ship) == []
    assert [sl.id for sl in scripts._topsails(ship)] == ["topsail"]
    again = load_ship(write_ship(doc, tmp_path, "pole-tartane-2"))
    again.sails["main.lateen"].cls = "gaff"  # no whole lateen below it now
    assert again.yard_level("topsail.yard") == 0


def test_the_yards_under_the_bowsprit_stand_apart(tmp_path):
    """A spritsail yard is no mast's (`under_bowsprit`): level -1, never a course, as before."""
    ship = load_ship("data/ships/seventy-four.yaml")
    under = [sp for sp in ship.spars.values() if sp.cls == "yard" and ship.under_bowsprit(sp)]
    assert under and all(ship.yard_level(sp) == -1 for sp in under)
    assert not any(ship.under_bowsprit(sl) for sl in scripts.lowest_square_sails(ship))


def test_the_levels_are_held_beside_her_and_never_pickled():
    """Read once a ship and held beside her, as the schooner's yards are: a checkpoint is the same
    bytes whether the levels have been read or not."""
    world = make_world(7, "data/ships/smack.yaml", Scenario(wind_from_deg=0.0, wind_speed_kn=12.0))
    from freesail.ship import graph

    graph._YARD_LEVELS.pop(world.ship, None)
    before = replay.checkpoint_bytes(world)
    assert world.ship.yard_level("topsail.yard") == 1
    assert replay.checkpoint_bytes(world) == before


def _smack_with_her_topsail(knots: float):
    world = make_world(
        7,
        "data/ships/smack.yaml",
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=knots,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=292.5,
            ship_speed_kn=5.0,
        ),
    )
    world.submit("set plain sail")
    world.run(120)
    world.submit("set the topsail")
    for i in range(900):
        if i % 120 == 0 and i > 300:
            world.submit("trim sails")
        world.tick()
    return world


def test_the_smack_hove_to_with_her_topsail_set_lays_it_to_the_mast():
    """Measured, seed 7, 15 kn: before A5 she hauled her topsail up as a course and lay under her
    fore-and-aft canvas (47.3 degrees off, 2.61 kn); now the fore-and-after's rule lays it to the
    mast as well ("to the mast as well if it is set"), 50.5 degrees off at 2.87 kn by 900 s."""
    world = _smack_with_her_topsail(15.0)
    n0 = len(world.log.all())
    world.submit("heave to")
    world.run(900)
    lines = [e.text for e in world.log.all()[n0:]]
    assert "Hauled up the courses." not in lines
    assert "Hove to on the starboard tack, topsail to the mast, helm a-lee." in lines
    assert world.ship.sails["topsail"].is_set
    off = abs(math.degrees(units.wrap_pi(world.ship.dyn.heading - world.wind.direction_from)))
    assert 45.0 <= off <= 65.0


def test_the_smack_lies_a_try_under_her_topsail_where_before_she_was_refused():
    """Measured, seed 7, 30 kn: before A5, "Could not bring her to: She has no topsail to lie
    a-try under."; now she lies a-try under the topsail and the foresail (49.3 degrees off at
    3.64 kn by 1,800 s)."""
    world = _smack_with_her_topsail(30.0)
    n0 = len(world.log.all())
    world.submit("lie a-try")
    world.run(1800)
    lines = [(e.kind, e.text) for e in world.log.all()[n0:]]
    assert not [x for k, x in lines if k == "evolution.failed"], lines
    assert ("ship.hove_to", "Lying a-try under the topsail and the foresail, helm a-lee.") in lines
