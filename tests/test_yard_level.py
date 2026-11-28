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
import yaml
from rig_fixtures import polacre_probe_doc, tartane_probe_doc, write_ship

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.orders import verbs
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState

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


# Every committed file's braced yards and their levels as the files stand (the lead's nudge 56):
# a table, as stage 0's `KEY_CARRIERS` is (`tests/test_probes_90.py`), held both ways. The guard
# above works the old formula again and so catches a change to the code; this catches a change
# to a file, where the formula and the level would move together. A step that adds, takes away
# or moves a committed yard moves its row here, old beside new in docs/dev/TuningNotes.md.
COMMITTED_YARD_LEVELS: dict[str, dict[str, int]] = {
    "bilander": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "main.crossjack.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "spritsail.yard": -1,
    },
    "boat-cutter-23": {},
    "boat-cutter-28": {},
    "boat-launch-25": {},
    "boat-launch-31": {},
    "boat-yawl-16": {},
    "brig": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
    },
    # the Diana's (package 90, her builder): the frigate-36's twelve yards at their levels, read
    # off her file as committed. Old: no row, before her file
    "corvette-20": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
        "mizzen.topsail.yard": 1,
        "mizzen.topgallant.yard": 2,
        "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0,
    },
    "cutter": {"square_sail.yard": 0, "topsail.yard": 1, "topgallant.yard": 2},
    "frigate-36": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
        "mizzen.topsail.yard": 1,
        "mizzen.topgallant.yard": 2,
        "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0,
    },
    "hermaphrodite-brig": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
    },
    "lugger": {},
    "merchant-brig": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
    },
    "privateer-schooner": {"fore.topsail.yard": 1, "fore.topgallant.yard": 2},
    "razee-44": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
        "mizzen.topsail.yard": 1,
        "mizzen.topgallant.yard": 2,
        "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0,
        "spritsail.yard": -1,
    },
    "seventy-four": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
        "mizzen.topsail.yard": 1,
        "mizzen.topgallant.yard": 2,
        "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0,
        "spritsail.yard": -1,
        "sprit_topsail.yard": -1,
    },
    "sixty-four": {
        "fore.yard": 0,
        "fore.topsail.yard": 1,
        "fore.topgallant.yard": 2,
        "fore.royal.yard": 3,
        "main.yard": 0,
        "main.topsail.yard": 1,
        "main.topgallant.yard": 2,
        "main.royal.yard": 3,
        "mizzen.topsail.yard": 1,
        "mizzen.topgallant.yard": 2,
        "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0,
        "spritsail.yard": -1,
        "sprit_topsail.yard": -1,
    },
    "smack": {"square_sail.yard": 0, "topsail.yard": 1},
    "topsail-schooner": {"fore.topsail.yard": 1, "fore.topgallant.yard": 2},
}


def test_the_table_of_yard_levels_has_a_row_for_every_committed_file_and_no_other():
    assert set(COMMITTED_YARD_LEVELS) == {p.stem for p in SHIP_FILES}
    # 91 before the Diana's file (package 90), her twelve the frigate-36's yards
    assert sum(len(row) for row in COMMITTED_YARD_LEVELS.values()) == 103


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_each_committed_files_yards_are_the_yards_of_its_row_at_their_levels(path):
    """A yard in a file and not in its row fails, a row's yard the file does not have fails, and
    a yard at another level fails."""
    ship = load_ship(path)
    levels = {sp.id: ship.yard_level(sp) for sp in ship.spars.values() if sp.cls == "yard"}
    assert levels == COMMITTED_YARD_LEVELS[path.stem]


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


def _cut_moved(sail: dict, yard: dict, height_m: float) -> None:
    """A probe's yard moved to `height_m` with its sail's cut: its centre kept at its depth below
    the yard, so that its foot (`graph._square_foot_m`) moves with it."""
    sail["centre_height_m"] = round(height_m - (yard["height_m"] - sail["centre_height_m"]), 2)
    yard["height_m"] = height_m


def test_a_square_yard_over_a_whole_lateen_counts_the_lateen_yard_below_it(tmp_path):
    """The tartane probe with her topsail yard on her pole main's head (its cut moved with it, its
    foot 10.2 m above the deck: 12.0 m before the lead's nudge 88, item 3, the centre above the
    water set against the yard above the deck) and no braced yard below it, her great lateen's yard
    below at 10 m: a topsail (1), not a course, being set over the lateen, its foot clear above the
    lateen's yard. With a gaff sail in the lateen's place it is the mast's lowest braced yard, a
    course, as the rule has always read."""
    doc = tartane_probe_doc()
    yard = next(s for s in doc["spars"] if s["id"] == "topsail.yard")
    yard["on"] = "main.mast"
    _cut_moved(next(s for s in doc["sails"] if s["id"] == "topsail"), yard, 15.6)
    ship = load_ship(write_ship(doc, tmp_path, "pole-tartane"))
    assert ship.yard_level("topsail.yard") == 1
    assert scripts.lowest_square_sails(ship) == []
    assert [sl.id for sl in scripts._topsails(ship)] == ["topsail"]
    again = load_ship(write_ship(doc, tmp_path, "pole-tartane-2"))
    again.sails["main.lateen"].cls = "gaff"  # no whole lateen below it now
    assert again.yard_level("topsail.yard") == 0


def test_a_square_sail_whose_foot_comes_below_the_lateens_yard_is_the_course(tmp_path):
    """The clause narrowed (nudge 39, ruling 1): a square sail is a topsail by the lateen's yard
    below it only where it is set over the lateen, its foot clear above that yard. The same probe,
    its yard at 15.5 m, with the sail cut down to near the deck (its centre 8.75 m above the
    water, its foot 1.0 m above the deck) is the course: the mast's lowest braced yard, whose foot
    comes down past the lateen's yard. So is a foot at the lateen's yard's own height (10 m): not
    clear above it. A foot at 10.25 m is clear above it, a topsail. (Heights exact in binary, so
    the tie is a tie: her deck at 0.5 m above the water.) Old, before the foot was taken at one
    datum (the lead's nudge 88, item 3): the cutter's deck at 0.9 m, the centres 8.25, 12.75 and
    12.875 m, the feet 1.0, 10 and 10.25 m by the centre above the water set against the yard
    above the deck; by the deck those feet are 0.8 m lower, -0.8, 8.2 and 8.45 m, each a course."""
    for centre, level in ((8.75, 0), (13.25, 0), (13.375, 1)):
        doc = tartane_probe_doc()
        doc["hull"]["deck_height_m"] = 0.5
        yard = next(s for s in doc["spars"] if s["id"] == "topsail.yard")
        yard["on"], yard["height_m"] = "main.mast", 15.5
        next(s for s in doc["sails"] if s["id"] == "topsail")["centre_height_m"] = centre
        ship = load_ship(write_ship(doc, tmp_path, f"to-the-deck-{centre}"))
        assert ship.yard_level("topsail.yard") == level, centre
        courses = [sl.id for sl in scripts.lowest_square_sails(ship)]
        assert courses == ([] if level else ["topsail"])


def _tartane_with_her_treou(
    tmp_path,
    treou_m: float | None,
    lateen_m: float = 10.0,
    topsail_m: float = 15.6,
    treou_first: bool = False,
    cuts: tuple[float, float] | None = None,
    flying: bool = False,
    deck_m: float | None = None,
) -> Path:
    """The tartane probe (its rig, not her file: her file is not on this branch) with her pole
    main as Tar-D §4.1 files it, no topmast and the topsail yard on the main's own head at
    `topsail_m`, her great lateen's yard crossing the mast at `lateen_m`; with the tréou's yard
    crossed on the main at `treou_m` (the cutter's square sail and its gear, renamed), filed
    after the great lateen's yard or, `treou_first`, before it; or not crossed (`None`). Each
    sail's cut moves with its yard (`_cut_moved`: the cutter's topsail's foot 5.4 m below its
    yard, its square sail's 7.4 m, her deck 0.9 m above the water; 3.6 and 5.6 m before the
    lead's nudge 88, item 3), or `cuts` gives the topsail's and the tréou's centres; `flying`,
    the tréou set flying as her file sets it (its yard sent down with it, furled); and `deck_m`,
    her deck's height above the water, where not the cutter's."""
    doc = tartane_probe_doc()
    if deck_m is not None:
        doc["hull"]["deck_height_m"] = deck_m
    gone = {"main.topmast", "main.topgallant_mast"}
    doc["spars"] = [s for s in doc["spars"] if s["id"] not in gone]
    doc["lines"] = [ln for ln in doc["lines"] if ln.get("of") not in gone or ln["id"] == "jib.stay"]
    for ln in doc["lines"]:
        if ln["id"] == "jib.stay":
            ln["of"] = "main.mast"
    for name in ("topmasts", "topgallant masts"):
        doc["groups"].pop(name)
    sails = {s["id"]: s for s in doc["sails"]}
    for s in doc["spars"]:
        if s["id"] == "topsail.yard":
            s["on"] = "main.mast"
            _cut_moved(sails["topsail"], s, topsail_m)
        if s["id"] == "main.lateen_yard":
            s["height_m"] = lateen_m
    if treou_m is not None:
        cutter = yaml.safe_load(Path("data/ships/cutter.yaml").read_text(encoding="utf-8"))
        ours = {"square_sail", "square_sail.yard"}
        for part in ("spars", "sails", "lines"):
            for item in cutter[part]:
                if item["id"] in ours or item.get("of") in ours:
                    named = ("id", "of", "yard")
                    doc[part].append(
                        {
                            k: v.replace("square_sail", "main.treou") if k in named else v
                            for k, v in item.items()
                        }
                    )
        treou = next(s for s in doc["spars"] if s["id"] == "main.treou.yard")
        _cut_moved(next(s for s in doc["sails"] if s["id"] == "main.treou"), treou, treou_m)
        if treou_first:
            doc["spars"].remove(treou)
            at = next(i for i, s in enumerate(doc["spars"]) if s["id"] == "main.lateen_yard")
            doc["spars"].insert(at, treou)
        doc["groups"]["square sails"].append("main.treou")
    if cuts is not None:
        sails = {s["id"]: s for s in doc["sails"]}
        sails["topsail"]["centre_height_m"] = cuts[0]
        if "main.treou" in sails:
            sails["main.treou"]["centre_height_m"] = cuts[1]
    if flying:  # as her file has it: set flying, and no reef bands (never reefed aloft)
        treou_sail = next(s for s in doc["sails"] if s["id"] == "main.treou")
        treou_sail["flying"] = True
        treou_sail.pop("reef_bands", None)
        doc["lines"] = [ln for ln in doc["lines"] if ln["id"] not in REEF_TACKLES]
    return write_ship(doc, tmp_path, "tartane-treou")


# her file's heights and cuts (`data/ships/tartane.yaml` on her branch): the great lateen's yard
# and the tréou's both at the main's hounds, 8.31 m, the topsail's yard at 15.78 m; the topsail's
# centre 12.6 m above the water and the tréou's 5.8 m, her deck 0.54 m above it. Their feet above
# the deck 8.34 m and 2.21 m (the lead's nudge 88, item 3: her topsail's foot 0.03 m above the
# great lateen's yard). Old: the deck the cutter's (0.9 m), not hers, and the feet 9.42 and 3.29 m,
# the centre above the water set against the yard above the deck; with the cutter's deck and the
# feet by the deck, her topsail's would be 7.62 m, below the lateen's yard, and a course.
HER_FILE = {"lateen_m": 8.31, "topsail_m": 15.78, "cuts": (12.6, 5.8), "deck_m": 0.54}
REEF_TACKLES = {"main.treou.reef_tackle.starboard", "main.treou.reef_tackle.larboard"}


@pytest.mark.parametrize(
    "treou_m, shape",
    [
        (None, {}),
        (None, HER_FILE),
        (8.0, {}),
        (13.0, {}),
        (8.31, HER_FILE),
        (8.31, dict(HER_FILE, treou_first=True)),
    ],
    ids=[
        "not-crossed",
        "her-file-not-crossed",
        "below",
        "above",
        "her-files-tie",
        "her-files-tie-the-treou-filed-first",
    ],
)
def test_the_tartanes_topsail_is_a_topsail_whether_the_treous_yard_is_crossed_or_not(
    tmp_path, treou_m, shape
):
    """Her tréou is set flying (Tar-D decision 9, §5.1a, §15 risk 5): its yard sent up with it and
    struck with it, so in plain sail no yard stands under her topsail. Her topsail reads the same
    both ways, a topsail (1) on the pole and handed by the pole's way: with no yard below it, by the
    great lateen's yard below it, being set over the lateen (the clause as ruled, nudge 39 ruling
    1); with the tréou's yard crossed, by the braced yard below it. **The tréou is her course
    wherever its yard crosses** (ruling 1): its foot comes down past the great lateen's yard toward
    the deck, so the clause does not reach it, below the great lateen's yard (8 m), above it (13 m,
    its foot 5.6 m above the deck; 7.4 m before the lead's nudge 88, item 3), or at one height with
    it as her file has them (8.31 m), in either order of the file. The answer hangs on the sail's
    cut, not on two yards' heights."""
    path = _tartane_with_her_treou(tmp_path, treou_m, **shape)
    ship = load_ship(path)
    assert ship.yard_level("topsail.yard") == 1
    assert ship.is_pole_mast("main.mast") and ship.on_pole("topsail")
    assert verbs._take_in_kind(ship, ship.sails["topsail"]) == "pole"
    assert [sl.id for sl in scripts._topsails(ship)] == ["topsail"]
    if treou_m is None:
        assert "main.treou.yard" not in ship.spars
        assert scripts.lowest_square_sails(ship) == []
    else:
        order = [sp.id for sp in ship.spars.values()]
        treou_at, lateen_at = order.index("main.treou.yard"), order.index("main.lateen_yard")
        assert (treou_at < lateen_at) is shape.get("treou_first", False)  # as filed
        assert ship.yard_level("main.treou.yard") == 0
        assert [sl.id for sl in scripts.lowest_square_sails(ship)] == ["main.treou"]
        assert not ship.on_pole("main.treou")
        assert verbs._take_in_kind(ship, ship.sails["main.treou"]) == "course"


def _topsail_lines(world, order: str, secs: int) -> list[str]:
    n0 = len(world.log.all())
    world.submit(order)
    world.run(secs)
    kinds = ("evolution.started", "evolution.step", "sail.taken_in", "sail.furled")
    return [e.text for e in world.log.all()[n0:] if e.kind in kinds and "topsail" in e.text]


@pytest.mark.parametrize("treou", ["not-filed", "set-flying-and-sent-down", "crossed"])
def test_the_tartanes_topsail_on_her_pole_comes_down_to_the_hounds_where_no_yard_is_below(
    tmp_path, treou
):
    """Nudge 39, ruling 2: with no tréou's yard crossed the yard below her topsail is her great
    lateen's, so the pole's words are of the pole alone: lowered to the hounds, clewed up there,
    furled on its own yard. So with no tréou's yard in the file, and so in her plain sail as her
    file has it, the tréou set flying and furled, sent down on deck with its yard. With the
    tréou's yard crossed (the cutter's square sail, not set flying), the yard below's words. The
    probe at her file's heights and cuts (seed 7, 15 kn from 0°, plain sail set, 600 s)."""
    path = _tartane_with_her_treou(
        tmp_path,
        None if treou == "not-filed" else 8.31,
        flying=treou == "set-flying-and-sent-down",
        **HER_FILE,
    )
    world = make_world(
        7,
        str(path),
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=15.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=292.5,
            ship_speed_kn=5.0,
        ),
    )
    world.submit("set plain sail")
    world.run(600)
    taken = _topsail_lines(world, "take in the topsail", 400)
    furled = _topsail_lines(world, "furl the topsail", 500)
    if treou == "crossed":
        assert taken == [
            "Let go the topsail halyards; hands to the clewlines and buntlines.",
            "Lowered the topsail down onto the yard below and clewed it up there.",
            "Took in the topsail; lowered on the yard below, hanging in the gear.",
        ]
        assert furled == [
            "Lay out on the yard below and furl the topsail.",
            "Furled the topsail on the yard below.",
        ]
    else:
        assert taken == [
            "Let go the topsail halyards; hands to the clewlines and buntlines.",
            "Lowered the topsail down to the hounds and clewed it up there.",
            "Took in the topsail; lowered to the hounds, hanging in the gear.",
        ]
        assert furled == [
            "Lay aloft to the hounds and furl the topsail.",
            "Furled the topsail on its own yard, lowered to the hounds.",
        ]


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


def _smack_with_her_topsail(knots: float, topsail: bool = True):
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
    if topsail:
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


def test_the_smacks_lie_a_try_is_refused_furled_in_her_topsails_words_and_set_she_lies_a_try():
    """Nudge 39, ruling 3, held (the lead's nudge 56): at `lie a-try` the smack follows the cutter,
    no further. Her topsail furled under her plain sail, she is refused in the words of a topsail
    not set, with no "close-reefed" (it has no reef band); before A5, "She has no topsail to lie
    a-try under.". Set, she lies a-try under it. Each from the settle with 300 s more, the trims
    done (as the report's table of the smack): measured, seed 7, 15 kn, lying a-try at +348 s."""
    furled = _smack_with_her_topsail(15.0, topsail=False)
    furled.run(300)
    assert furled.ship.sails["topsail"].state is SailState.FURLED
    answer = furled.submit("lie a-try")
    assert (answer.kind, answer.text) == (
        "order.rejected",
        "Order not carried out ('lie a-try'): The topsail is not set; set it to lie a-try under "
        "it.",
    )
    world = _smack_with_her_topsail(15.0)
    world.run(300)
    n0 = len(world.log.all())
    assert world.submit("lie a-try").kind == "order.accepted"
    world.run(600)
    lines = [(e.kind, e.text) for e in world.log.all()[n0:]]
    assert not [x for k, x in lines if k in ("evolution.failed", "order.rejected")], lines
    assert ("ship.hove_to", "Lying a-try under the topsail and the foresail, helm a-lee.") in lines
    assert world.ship.sails["topsail"].is_set
