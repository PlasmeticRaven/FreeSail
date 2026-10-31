"""Package 75, stage 0: the hull's profile and the gun deck's keys (docs/design/Build-Ships.md
§3.1 items 1 to 16 and 28, §5.1, §5.2).

A ship file's `hull.profile` gives the top of the side, the half-breadths, the decks and one
side's ports as lines of points, x forward of midships and z above the file's waterline; the
schema refuses in words what §5.2 refuses, and `freesail/ship/profile.py` reads it, straight
between points and held at the ends. A gun names its `deck`, a deck word, and where the
profile gives ports a gun with a port names a deck that has them. A file's armament may
default to `unarmed`, whose fit is None. A document that carries none of these, built here in
the test, loads as it always did, and a gun's, a gun spec's and the hull spec's pickles are as
before while they hold no deck or profile. A pivot gun names its own arc, refused without one
after the side; the one pivot on file, the privateer schooner's, gives it already.

The generator (items 1 to 9) runs the four ships' modules after the eight, each a stub
writing nothing, with `gen_ships` the running script; its `hull_profile` writes the
profile in the schema's form to the centimetre and refuses at generation what the load
would; its `dump` sets each line of the profile on one line with its notes; and its gun
helpers take a deck and the centimetre.

The gun deck's, the readings' and the world's hooks (items 17 to 25): the lee ports' update
shuts nothing and a gun in `Battery._shut` neither works nor fires; their two events are
registered absent and said nowhere; `/api/ship` serves a profile only where the file gives
one; the lookups by a sail's class read `curve_class`; a description carries its file's `fit`
and `roles`, a far ship's `role:` is refused outside them, and her saved forms are as before
while she has none and her fit is her file's default; her role comes first for her captain,
carried in by her far brain, and the sixty-four, the razee and the seventy-four are King's
ships, ranked and counted men of war, the razee's words matched first.
"""

from __future__ import annotations

import ast
import copy
import importlib.util
import json
import pickle
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail.api.queries import _sail_entry, ship_graph
from freesail.api.readings import EVENTS, sail_reading
from freesail.api.session import make_world
from freesail.combat import ports
from freesail.combat.action import _far_weight
from freesail.combat.far import far_ship
from freesail.combat.guns import Battery, Firer
from freesail.core.world import Scenario
from freesail.ship import charges
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict, spec_from_dict
from freesail.ship.parts import Charge, Sail, SailState, charge_lb
from freesail.ship.profile import (
    deck_at,
    half_breadth_at_sill,
    interp,
    ports_of,
    rail_at,
    sill_at,
)
from freesail.ship.schema import (
    _PORT_GUN_PLACES,
    DECK_WORDS,
    PROFILE_KEYS,
    UNARMED,
    HullProfile,
    ShipFileError,
    _parse_gun,
)
from freesail.world import brains, captains, regimes, squadrons
from freesail.world import ships as S
from freesail.world.geo import Position

ROOT = Path(__file__).resolve().parents[1]
BRIG = "data/ships/brig.yaml"

# A frigate's profile, hand-built (not a ship's: round figures, each line easy to reckon): a
# quarterdeck and a forecastle over a gun deck open in the waist, ports on the gun deck and
# the quarterdeck.
PROFILE = {
    "rail_m": [[-20.0, 5.0], [0.0, 4.0], [20.0, 5.0]],
    "breadth_m": [[-20.0, 3.0, 3.5], [0.0, 5.0, 5.4], [20.0, 2.0, 3.0]],
    "keel_m": [[-19.0, -4.5], [17.0, -4.4]],
    "stem_m": [[20.5, -4.0], [21.0, 0.0], [21.5, 5.2]],
    "stern_m": [[-19.5, -4.3], [-20.0, 0.0], [-21.0, 5.0]],
    "wales_m": [[-18.0, 0.8, 1.4], [0.0, 0.6, 1.2], [18.0, 0.9, 1.5]],
    "section_m": [[-4.4, 0.2], [-2.0, 4.0], [0.0, 5.0], [2.0, 5.3], [4.0, 5.4]],
    "decks_m": {
        "upper": [[-20.0, 1.9], [0.0, 1.5], [18.0, 1.9]],
        "quarterdeck": [[-20.0, 3.8], [-8.0, 3.5]],
        "forecastle": [[12.0, 3.4], [19.0, 3.6]],
    },
    "ports_m": {
        "upper": [
            [-16.0, 2.5, 4.0],
            [-8.0, 2.2, 4.8],
            [0.0, 2.0, 5.0],
            [8.0, 2.2, 4.6],
            [16.0, 2.6, 3.4],
        ],
        "quarterdeck": [[-18.0, 4.2, 3.5], [-12.0, 4.1, 3.8]],
    },
    "port_size_m": {"upper": [0.9, 0.8], "quarterdeck": [0.8, 0.7]},
}


def _gun(gid: str, **kw) -> dict:
    gun = {
        "id": gid,
        "kind": "long",
        "pounder": 12,
        "place": "broadside",
        "number": 1,
        "side": "starboard",
        "x_m": 0.0,
        "height_m": 2.0,
        "crew": 7,
        "weight_cwt": 34.0,
    }
    gun.update(kw)
    return {k: v for k, v in gun.items() if v is not None}


def _doc(profile: dict | None = None, guns: list[dict] | None = None, **armament) -> dict:
    """A small ship of one mast, with the profile and the guns given."""
    hull = {
        "length_waterline_m": 40.0,
        "beam_m": 11.0,
        "draught_m": 4.5,
        "displacement_kg": 900000,
        "gm_m": 1.2,
        "deck_height_m": 1.5,
    }
    if profile is not None:
        hull["profile"] = copy.deepcopy(profile)
    doc = {
        "ship": {"name": "Test", "rig": "ship"},
        "hull": hull,
        "spars": [{"id": "main", "class": "mast", "x_m": 0.0, "height_m": 20.0, "rating_kn": 400}],
    }
    if guns is not None:
        doc["armament"] = {"fits": {"as built": {"guns": guns}}, **armament}
    return doc


@pytest.fixture(scope="module")
def profile() -> HullProfile:
    p = spec_from_dict(_doc(PROFILE), "p.yaml").hull.profile
    assert p is not None
    return p


# -- profile.py on a hand-built profile ------------------------------------------------------


def test_the_profile_is_read_into_tuples_in_the_files_order(profile):
    assert PROFILE_KEYS[:2] == ("rail_m", "breadth_m") and DECK_WORDS[2] == "upper"
    assert profile.rail_m == ((-20.0, 5.0), (0.0, 4.0), (20.0, 5.0))
    assert profile.breadth_m[1] == (0.0, 5.0, 5.4)
    assert profile.stern_m[-1] == (-21.0, 5.0)
    assert [w for w, _ in profile.decks_m] == ["upper", "quarterdeck", "forecastle"]
    assert [w for w, _ in profile.ports_m] == ["upper", "quarterdeck"]
    assert dict(profile.port_size_m) == {"upper": (0.9, 0.8), "quarterdeck": (0.8, 0.7)}
    with pytest.raises(AttributeError):
        profile.rail_m = ()  # frozen
    # a file without one has none
    assert spec_from_dict(_doc(), "p.yaml").hull.profile is None


def test_interp_is_straight_between_points_and_held_at_the_ends():
    line = [(-10.0, 1.0), (0.0, 3.0), (10.0, 2.0)]
    assert interp(line, -5.0) == pytest.approx(2.0)
    assert interp(line, 5.0) == pytest.approx(2.5)
    assert interp(line, 0.0) == 3.0 and interp(line, 10.0) == 2.0  # a point's own value
    assert interp(line, -30.0) == 1.0 and interp(line, 30.0) == 2.0  # held
    assert interp([(0.0, 7.0, 99.0)], 4.0) == 7.0  # a triple's third is not read
    with pytest.raises(ValueError):
        interp([], 0.0)


def test_the_rail_and_the_uppermost_deck(profile):
    assert rail_at(profile, -10.0) == pytest.approx(4.5)
    assert rail_at(profile, 25.0) == 5.0
    # abaft the waist the quarterdeck is uppermost, in it the gun deck, forward the forecastle
    assert deck_at(profile, -15.0) == pytest.approx(3.8 - 0.3 * 5.0 / 12.0)
    assert deck_at(profile, 0.0) == pytest.approx(1.5)
    assert deck_at(profile, 15.0) == pytest.approx(3.4 + 0.2 * 3.0 / 7.0)
    assert deck_at(profile, -20.0) == 3.8  # both decks begin there: the higher
    # beyond every deck's extent, the nearest deck's end, held
    assert deck_at(profile, 19.5) == 3.6
    assert deck_at(profile, -25.0) == 3.8
    bare = spec_from_dict(_doc({k: PROFILE[k] for k in ("rail_m", "breadth_m")}), "p.yaml")
    assert deck_at(bare.hull.profile, 0.0) is None


def test_the_ports_their_sills_and_the_half_breadths_at_the_sills(profile):
    assert ports_of(profile, "upper")[2] == (0.0, 2.0, 5.0)
    assert len(ports_of(profile, "quarterdeck")) == 2
    assert ports_of(profile, "forecastle") == ()
    assert sill_at(profile, "upper", 4.0) == pytest.approx(2.1)
    assert half_breadth_at_sill(profile, "upper", 4.0) == pytest.approx(4.8)
    assert sill_at(profile, "upper", 0.0) == 2.0
    assert half_breadth_at_sill(profile, "upper", -8.0) == 4.8
    assert sill_at(profile, "upper", 20.0) == 2.6 and sill_at(profile, "upper", -30.0) == 2.5
    assert half_breadth_at_sill(profile, "quarterdeck", -15.0) == pytest.approx(3.65)
    # a deck with no ports: none, and the lee ports' rule takes half the beam
    assert sill_at(profile, "forecastle", 15.0) is None
    assert half_breadth_at_sill(profile, "lower", 0.0) is None


# -- §5.2's refusals --------------------------------------------------------------------------


def _with(change) -> dict:
    p = copy.deepcopy(PROFILE)
    change(p)
    return p


def _set(path: str, value):
    """A change that sets the profile's key (or a deck's line, 'ports_m.upper') to value."""

    def change(p):
        key, _, deck = path.partition(".")
        if deck:
            p[key][deck] = value
        else:
            p[key] = value

    return change


def _drop(key: str):
    return lambda p: p.pop(key)


REFUSALS = [
    # a key not in PROFILE_KEYS, or a deck word not in DECK_WORDS
    ("an unknown key", _set("sheer_m", [[0.0, 4.0]]), "has 'sheer_m', which it does not take"),
    ("an unknown deck", _set("decks_m.orlop", [[0.0, 0.5]]), "names the deck 'orlop'"),
    ("an unknown port deck", _set("ports_m.gun", [[0.0, 2.0, 5.0]]), "names the deck 'gun'"),
    # without the rail or the half-breadths
    ("no rail", _drop("rail_m"), "wants rail_m and breadth_m"),
    ("no breadths", _drop("breadth_m"), "wants rail_m and breadth_m"),
    ("an empty rail", _set("rail_m", []), "not a list of \\[x, z\\] points"),
    # a point that is not two numbers (three in breadth_m, wales_m and a port triple)
    ("a short rail point", _set("rail_m", [[-20.0, 5.0], [0.0]]), "not two numbers"),
    ("a word for a number", _set("keel_m", [[0.0, "deep"]]), "not two numbers"),
    ("a true for a number", _set("stem_m", [[20.0, True]]), "not two numbers"),
    ("a breadth of two", _set("breadth_m", [[0.0, 5.0]]), "not three numbers"),
    ("a wale of two", _set("wales_m", [[0.0, 0.6]]), "not three numbers"),
    ("a port of two", _set("ports_m.upper", [[0.0, 2.0]]), "not three numbers"),
    ("a port size of one", _set("port_size_m.upper", [0.9]), "not two numbers"),
    ("a number not finite", _set("section_m", [[0.0, float("nan")]]), "not two numbers"),
    # x not increasing in the rail, the breadths, the keel, the wales, a deck, a deck's ports
    ("the rail aft", _set("rail_m", [[0.0, 4.0], [-20.0, 5.0]]), "each x greater"),
    ("the rail stepped", _set("rail_m", [[0.0, 4.0], [0.0, 5.0]]), "each x greater"),
    ("the breadths aft", _set("breadth_m", [[1.0, 5.0, 5.4], [0.0, 5.0, 5.4]]), "each x greater"),
    ("the keel aft", _set("keel_m", [[17.0, -4.4], [-19.0, -4.5]]), "each x greater"),
    ("the wales aft", _set("wales_m", [[1.0, 0.6, 1.2], [0.0, 0.6, 1.2]]), "each x greater"),
    ("a deck aft", _set("decks_m.upper", [[0.0, 1.5], [-20.0, 1.9]]), "each x greater"),
    ("the ports aft", _set("ports_m.upper", [[0.0, 2.0, 5.0], [-8.0, 2.2, 4.8]]), "each x greater"),
    # z not increasing in the stem and the stern
    ("the stem down", _set("stem_m", [[21.5, 5.2], [21.0, 0.0]]), "each z greater"),
    ("the stern down", _set("stern_m", [[-20.0, 0.0], [-19.5, -4.3]]), "each z greater"),
    # a deck at side above the rail; a sill at or above the rail, or below its deck
    ("a deck above the rail", _set("decks_m.forecastle", [[12.0, 4.7]]), "above the rail"),
    ("a sill at the rail", _set("ports_m.upper", [[0.0, 4.0, 5.0]]), "at or above the rail"),
    ("a sill over the rail", _set("ports_m.upper", [[0.0, 4.5, 5.0]]), "at or above the rail"),
    ("a sill under its deck", _set("ports_m.upper", [[0.0, 1.4, 5.0]]), "below its deck"),
    # a half-breadth not positive
    ("no breadth at the water", _set("breadth_m", [[0.0, 0.0, 5.4]]), "more than nothing"),
    ("a breadth at the rail less", _set("breadth_m", [[0.0, 5.0, -1.0]]), "more than nothing"),
    ("a section of nothing", _set("section_m", [[0.0, 0.0]]), "more than nothing"),
    ("a port's breadth of nothing", _set("ports_m.upper", [[0.0, 2.0, 0.0]]), "more than nothing"),
    # a ports_m or port_size_m deck that is not in decks_m
    ("ports of no deck", _set("ports_m.lower", [[0.0, 0.5, 5.0]]), "which its decks_m does not"),
    ("a port size of no deck", _set("port_size_m.middle", [0.9, 0.8]), "decks_m does not"),
    ("ports and no decks", _drop("decks_m"), "which its decks_m does not"),
    # the shapes
    ("a deck list for a mapping", _set("decks_m", [[0.0, 1.5]]), "decks_m is not a mapping"),
]


@pytest.mark.parametrize("words, change, match", REFUSALS, ids=[r[0] for r in REFUSALS])
def test_the_schema_refuses_what_5_2_refuses_in_words(words, change, match):
    with pytest.raises(ShipFileError, match=match) as e:
        spec_from_dict(_doc(_with(change)), "p.yaml")
    assert str(e.value).startswith("p.yaml: ")


def test_the_profile_is_a_mapping_and_its_refusals_name_the_line():
    with pytest.raises(ShipFileError, match="the hull's profile is not a mapping"):
        spec_from_dict(_doc([[0.0, 1.0]]), "p.yaml")
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(_doc(_with(_set("ports_m.upper", [[0.0, 1.4, 5.0]]))), "p.yaml")
    assert str(e.value) == (
        "p.yaml: the profile's port on the upper deck at x 0 has its sill at 1.4 m, below its "
        "deck (1.50 m there)."
    )
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(_doc(_with(_set("stem_m", [[21.5, 5.2], [21.0, 0.0]]))), "p.yaml")
    assert str(e.value) == (
        "p.yaml: the profile's stem_m goes from z 5.2 to 0; its points run low to high, each z "
        "greater than the last."
    )


def test_a_deck_or_a_sill_on_the_lines_own_points_stands():
    """A deck at the rail's own height is at it, not above it; a sill on its deck is not
    below it."""
    p = _with(_set("decks_m.forecastle", [[12.0, 4.6], [19.0, 3.6]]))
    p["ports_m"]["upper"] = [[-16.0, 1.82, 4.0], [0.0, 2.0, 5.0]]
    assert spec_from_dict(_doc(p), "p.yaml").hull.profile.decks_m[2][1][0] == (12.0, 4.6)


# -- the gun deck --------------------------------------------------------------------------


def test_a_gun_names_its_deck_and_it_is_carried_to_the_part():
    swivel = _gun("swivel", kind="swivel", pounder=0.5, place="rail", number=None, side=None)
    spec = spec_from_dict(_doc(PROFILE, [_gun("gun.1.starboard", deck="upper"), swivel]), "p.yaml")
    assert [g.deck for g in spec.armament.fit().guns] == ["upper", None]
    ship = Ship(spec)
    assert ship.guns["gun.1.starboard"].deck == "upper"
    assert ship.guns["swivel"].deck is None
    g = ship.guns["gun.1.starboard"]
    del g.deck  # a gun pickled before package 75: the class's default
    assert g.deck is None


def test_a_gun_and_a_hull_are_pickled_as_before_while_the_new_keys_hold_their_defaults():
    """The checkpoint (the owner's rule for stage 0): a `Gun`, its `GunSpec` and the
    `HullSpec` leave `deck` and `profile` out of their pickled state while None, and read the
    class's None back; a deck or a profile given is kept."""
    ship = ship_from_dict(_doc(None, [_gun("gun.1.starboard")]), "p.yaml")  # with neither
    plain = (
        (ship.guns["gun.1.starboard"], "deck"),
        (ship.spec.armament.fit().guns[0], "deck"),
        (ship.spec.hull, "profile"),
    )
    for obj, key in plain:
        assert key not in obj.__getstate__()
        again = pickle.loads(pickle.dumps(obj))
        assert key not in again.__dict__ and getattr(again, key) is None and again == obj
    spec = spec_from_dict(_doc(PROFILE, [_gun("gun.1.starboard", deck="upper")]), "p.yaml")
    given = (
        (Ship(spec).guns["gun.1.starboard"], "deck"),
        (spec.armament.fit().guns[0], "deck"),
        (spec.hull, "profile"),
    )
    for obj, key in given:
        again = pickle.loads(pickle.dumps(obj))
        assert getattr(again, key) is not None and getattr(again, key) == getattr(obj, key)


def test_a_gun_deck_is_a_deck_word_and_a_port_deck_where_the_profile_gives_ports():
    # not a deck word: refused with a profile or without
    for profile in (PROFILE, None):
        with pytest.raises(ShipFileError, match="stands on the 'orlop' deck; a deck is one of"):
            spec_from_dict(_doc(profile, [_gun("gun.1.starboard", deck="orlop")]), "p.yaml")
    # a gun with a port on a deck the profile gives no ports: refused
    for place, extra in (
        ("broadside", {}),
        ("bow", {"number": None, "side": "starboard"}),
        ("stern", {"number": None, "side": None}),
    ):
        gun = _gun("g", place=place, deck="forecastle", **extra)
        with pytest.raises(ShipFileError, match="where the hull's profile gives no ports") as e:
            spec_from_dict(_doc(PROFILE, [gun]), "p.yaml")
    assert str(e.value) == (
        "p.yaml: the gun 'g' of the fit 'as built' is a stern gun on the forecastle, where the "
        "hull's profile gives no ports (the decks with ports: upper, quarterdeck)."
    )
    # a pivot and a rail gun fire over the rail: any deck; and with no profile, any deck word
    pivot = _gun("pivot", place="pivot", number=None, side=None, arc_deg=[60, 140])
    swivel = _gun("swivel", kind="swivel", pounder=0.5, place="rail", number=None, side=None)
    for gun in (dict(pivot, deck="forecastle"), dict(swivel, deck="roundhouse")):
        assert spec_from_dict(_doc(PROFILE, [gun]), "p.yaml").armament.fit().guns[0].deck
    assert spec_from_dict(_doc(None, [_gun("g", deck="lower")]), "p.yaml")
    # a profile with no ports: no port deck to name
    bare = {k: PROFILE[k] for k in ("rail_m", "breadth_m", "decks_m")}
    assert spec_from_dict(_doc(bare, [_gun("g", deck="middle")]), "p.yaml")


# -- unarmed -------------------------------------------------------------------------------


def test_unarmed_is_a_fit_of_no_guns_named_or_by_default():
    assert UNARMED == "unarmed"
    spec = spec_from_dict(_doc(None, [_gun("gun.1.starboard")], default=UNARMED), "p.yaml")
    assert spec.armament.default == UNARMED
    assert spec.armament.fit() is None and spec.armament.fit(UNARMED) is None
    assert spec.armament.fit("as built").guns[0].id == "gun.1.starboard"
    ship = Ship(spec)
    assert ship.fit_spec is None and ship.guns == {} and ship.fit == ""
    assert Ship(spec, fit="as built").guns
    # a file armed by default, a scenario naming her unarmed
    armed = spec_from_dict(_doc(None, [_gun("gun.1.starboard")]), "p.yaml")
    assert armed.armament.fit(UNARMED) is None and Ship(armed, fit=UNARMED).guns == {}
    assert load_ship(BRIG, fit=UNARMED).guns == {}


def test_every_caller_of_fit_takes_unarmed():
    """graph.py and far.py took None already; action.py's weight of the far ship's broadside
    is taught it (Build-Ships.md §3.1 item 12)."""
    assert _far_weight(SimpleNamespace(ship_file=BRIG, fit=UNARMED)) == 0.0
    assert _far_weight(SimpleNamespace(ship_file=BRIG, fit="")) > 0.0
    assert far_ship(BRIG, "British", fit=UNARMED).guns == []
    assert far_ship(BRIG, "British").guns


def test_a_fit_named_unarmed_and_a_default_of_no_fit_are_refused():
    doc = _doc(None, [_gun("gun.1.starboard")])
    doc["armament"]["fits"][UNARMED] = doc["armament"]["fits"]["as built"]
    with pytest.raises(ShipFileError, match="names a fit 'unarmed', the word for no guns"):
        spec_from_dict(doc, "p.yaml")
    with pytest.raises(ShipFileError, match="is none of its fits \\(as built\\) and not 'unarmed'"):
        spec_from_dict(_doc(None, [_gun("gun.1.starboard")], default="disarmed"), "p.yaml")


# -- the pivot's own arc -------------------------------------------------------------------


def test_a_pivot_without_an_arc_is_refused_and_no_side_is_still_heard_first():
    pivot = _gun("pivot", place="pivot", number=None, side=None)
    with pytest.raises(ShipFileError, match="is a pivot gun and gives no arc_deg"):
        _parse_gun(pivot, 0, "the fit 'long tom'", "test")
    with pytest.raises(ShipFileError, match="no side"):
        _parse_gun(dict(pivot, side="starboard"), 0, "the fit 'long tom'", "test")
    assert _parse_gun(dict(pivot, arc_deg=[55, 135]), 0, "f", "test").arc_deg == (55.0, 135.0)
    # the one pivot on file carries its arc
    tom = load_ship("data/ships/privateer-schooner.yaml").guns["pivot"]
    assert tom.arc_deg == (60.0, 140.0)


# -- the other hooks of stage 0 ------------------------------------------------------------


def test_a_sails_curve_class_is_its_class():
    ship = load_ship(BRIG)
    assert ship.sails and all(s.curve_class == s.cls for s in ship.sails.values())


def test_charge_lb_reads_the_table_first_and_the_share_where_it_has_none(monkeypatch):
    # a long 7-pounder: no calibre of the game, so the table never gives it
    assert charge_lb("long", 7) == round(7 / 3 * 16) / 16
    monkeypatch.setitem(charges.CHARGE_TABLE_LB, ("long", 7.0), 2.5)
    assert charge_lb("long", 7) == 2.5
    assert charge_lb("carronade", 7) == round(7 / 12 * 16) / 16


def test_a_ship_from_a_dict_with_a_profile_builds():
    ship = ship_from_dict(_doc(PROFILE, [_gun("gun.1.starboard", deck="upper")]), "p.yaml")
    assert ship.spec.hull.profile.rail_m[0] == (-20.0, 5.0)


# -- the generator (items 1 to 9) ----------------------------------------------------------

# The generator run as the script it is, `importlib.import_module` watched: for each ship's
# module it imports, whether `gen_ships` was then the running script, and the files in the
# output before and after the module's build.
HOOK_PROBE = """
import importlib, os, runpy, sys

script, out = sys.argv[1], sys.argv[2]
sys.argv = [script, out]
sys.path.insert(0, os.path.dirname(script))  # as a script's own directory is
seen = []
import_module = importlib.import_module


def watched(name, package=None):
    module = import_module(name, package)
    if name.startswith("ships."):
        aliased = sys.modules.get("gen_ships") is sys.modules["__main__"]
        build = module.build

        def counted(out_dir):
            before = sorted(os.listdir(out_dir))
            build(out_dir)
            seen.append((name, aliased, before, sorted(os.listdir(out_dir))))

        module.build = counted
    return module


importlib.import_module = watched
runpy.run_path(script, run_name="__main__")
print(repr(seen))
"""


# The files each ships module writes, in the lead's order (Build-Ships.md §4.1): a stub writes
# none, and a built module its own files only.
MODULE_FILES = {
    "ships.indefatigable": ["razee-44.yaml", "sixty-four.yaml"],
    "ships.neufchatel": [],
    "ships.bilander": [],
    "ships.bellerophon": [],
}


def test_the_hook_runs_the_four_ships_modules_after_the_eight_each_writing_its_own(tmp_path):
    """Build-Ships.md §3.1 items 1, 2 and 28: the generator writes the eight files, then imports
    each module in the lead's order (the Indefatigable, the Prince de Neufchatel,
    the bilander, the 74) after `gen_ships` is made the running script; each build adds its
    own files and no other (§4.1), a stub none."""
    out = tmp_path / "ships"
    run = subprocess.run(
        [sys.executable, "-c", HOOK_PROBE, str(ROOT / "tools" / "gen_ships.py"), str(out)],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    seen = ast.literal_eval(run.stdout.strip())
    committed = sorted(p.name for p in (ROOT / "data" / "ships").glob("*.yaml"))
    eight = sorted(set(committed) - {f for files in MODULE_FILES.values() for f in files})
    # the generator's own files: the eight ships and the five boats of the ships' lists
    # (package 82, item 4: `boat-*.yaml`, written by `__main__` after the eight)
    assert len(eight) == 13 and sum(1 for f in eight if f.startswith("boat-")) == 5
    assert [name for name, *_ in seen] == list(MODULE_FILES)
    assert seen[0][2] == eight
    for name, aliased, before, after in seen:
        assert aliased, name
        assert set(before) <= set(after), name
        assert sorted(set(after) - set(before)) == MODULE_FILES[name], name
    for name in committed:
        made = (out / name).read_text(encoding="utf-8")
        assert made == (ROOT / "data" / "ships" / name).read_text(encoding="utf-8"), name


def test_period_is_constants_importing_nothing():
    """Build-Ships.md §3.1 item 3: `tools/ships/period.py` imports nothing, and the 74's
    patterns are lengths of Adye's table."""
    path = ROOT / "tools" / "ships" / "period.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    assert not [n for n in ast.walk(tree) if isinstance(n, ast.Import | ast.ImportFrom)]
    spec = importlib.util.spec_from_file_location("period_under_test", path)
    period = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(period)
    weights = {p: period.ADYE_LONG_GUN_CWT[p][n] for p, n in period.SEVENTY_FOUR_PATTERNS.items()}
    assert weights == {32: 55.0, 18: 40.0, 9: 24.5}
    assert period.ADYE_CARRONADE_CWT[32] == 17 + 14 / 112  # 17 cwt 0 qr 14 lb
    assert period.FALCONER_CREW[24] == 11 and period.DOUGLAS_CARRONADE_CREW == 4


@pytest.fixture(scope="module")
def gen():
    """The generator as a module, not run: its helpers as a ship's module takes them."""
    spec = importlib.util.spec_from_file_location(
        "gen_ships_under_test", ROOT / "tools" / "gen_ships.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _parts(p: dict) -> dict:
    """A profile's lines but the rail and the breadth, as `hull_profile`'s parts."""
    return {k.removesuffix("_m"): v for k, v in p.items() if k not in ("rail_m", "breadth_m")}


def test_hull_profile_is_the_schemas_form_to_the_centimetre(gen):
    p = gen.hull_profile(
        [(-20.004, 5.0), (0.0, 4.0), (20.0, 5.0)],
        PROFILE["breadth_m"],
        port_size={"upper": (0.9, 0.8)},
        ports={"upper": PROFILE["ports_m"]["upper"]},
        decks={"upper": [[-20.0, 1.9], [-0.001, 1.5], [18.0, 1.9]]},
        stem=PROFILE["stem_m"],
        keel=None,  # a part the sources do not give is left out
    )
    assert list(p) == ["rail_m", "breadth_m", "stem_m", "decks_m", "ports_m", "port_size_m"]
    assert p["rail_m"] == [[-20.0, 5.0], [0.0, 4.0], [20.0, 5.0]]
    assert p["decks_m"]["upper"][1] == [0.0, 1.5]
    assert str(p["decks_m"]["upper"][1][0]) == "0.0"  # never -0.0
    assert p["port_size_m"] == {"upper": [0.9, 0.8]}
    assert spec_from_dict(_doc(p), "p.yaml").hull.profile.rail_m[0] == (-20.0, 5.0)


# §5.2's refusals but the unknown key, which `hull_profile` refuses as a part it does not take
GENERATED_REFUSALS = [r for r in REFUSALS if r[0] != "an unknown key"]


@pytest.mark.parametrize(
    "words, change, match", GENERATED_REFUSALS, ids=[r[0] for r in GENERATED_REFUSALS]
)
def test_hull_profile_refuses_at_generation_what_the_load_would(gen, words, change, match):
    p = _with(change)
    with pytest.raises(ValueError, match=match) as e:
        gen.hull_profile(p.get("rail_m"), p.get("breadth_m"), **_parts(p))
    assert str(e.value).startswith("hull_profile")


def test_hull_profile_refuses_a_part_it_does_not_take_in_its_own_words(gen):
    with pytest.raises(ValueError, match="takes no part 'keel_m'; beside the rail and the breadth"):
        gen.hull_profile(PROFILE["rail_m"], PROFILE["breadth_m"], keel_m=PROFILE["keel_m"])
    with pytest.raises(ValueError) as e:
        gen.hull_profile(PROFILE["rail_m"], PROFILE["breadth_m"], stem=[[21.5, 5.2], [21.0, 0.0]])
    assert str(e.value) == (
        "hull_profile: the profile's stem_m goes from z 5.2 to 0; its points run low to high, "
        "each z greater than the last."
    )


def test_dump_writes_each_line_of_the_profile_on_one_line_with_its_notes(gen, tmp_path):
    hull = _doc()["hull"]
    hull["profile"] = gen.hull_profile(PROFILE["rail_m"], PROFILE["breadth_m"], **_parts(PROFILE))
    notes = {
        "deck_height_m": "The datum.",
        "profile": "The profile's sources.",
        "profile.rail_m": "The rail, judgement.",
        "profile.decks_m.quarterdeck": "The quarterdeck, measured.",
        "profile.port_size_m.upper": "The gun deck's port, measured.",
    }
    b = gen.Builder("Test", "ship", "A test.", hull, hull_notes=notes)
    b.spar("main", "mast", x_m=0.0, height_m=20.0, rating_kn=400.0)
    path = tmp_path / "test.yaml"
    b.dump(str(path), "# A test.\n")
    text = path.read_text(encoding="utf-8")
    assert (
        "  # The datum.\n  deck_height_m: 1.5\n"
        "  # The profile's sources.\n  profile:\n"
        "    # The rail, judgement.\n    rail_m: [[-20.0, 5.0], [0.0, 4.0], [20.0, 5.0]]\n"
        "    breadth_m: [[-20.0, 3.0, 3.5], [0.0, 5.0, 5.4], [20.0, 2.0, 3.0]]\n"
    ) in text
    assert (
        "    decks_m:\n      upper: [[-20.0, 1.9], [0.0, 1.5], [18.0, 1.9]]\n"
        "      # The quarterdeck, measured.\n      quarterdeck: [[-20.0, 3.8], [-8.0, 3.5]]\n"
    ) in text
    assert "      # The gun deck's port, measured.\n      upper: [0.9, 0.8]\n" in text
    assert "    section_m: [[-4.4, 0.2], [-2.0, 4.0], [0.0, 5.0], [2.0, 5.3], [4.0, 5.4]]\n" in text
    assert yaml.safe_load(text)["hull"]["profile"] == hull["profile"]
    assert load_ship(path).spec.hull.profile == spec_from_dict(_doc(PROFILE), "p.yaml").hull.profile


def test_the_gun_helpers_take_a_deck_and_the_centimetre_and_keep_todays_form(gen):
    (g, note), (larboard, _) = gen.broadside_pair(3, "long", 24, 49.5, 1.25, 2.35, note="n")
    assert note == "n" and "deck" not in g and "deck" not in larboard
    assert (g["x_m"], g["height_m"]) == (round(1.25, 1), round(2.35, 1))  # today's form
    (g, _), _ = gen.broadside_pair(3, "long", 24, 49.5, 1.2345, 2.0049, deck="upper", round_to=0.01)
    assert (g["x_m"], g["height_m"]) == (1.23, 2.0) and list(g)[-1] == "deck"
    for guns in (
        gen.chasers("bow", "long", 12, 34.0, 20.04, 4.251, deck="forecastle", round_to=0.01),
        gen.pivot_gun("long", 18, 42.0, 0.0, 2.316, (60, 140), deck="upper", round_to=0.01),
        gen.swivels(2, [10.0], 3.333, deck="quarterdeck", round_to=0.01),
    ):
        for g, _ in guns:
            assert list(g)[-1] == "deck" and g["height_m"] == round(g["height_m"], 2)
    assert gen.pivot_gun("long", 18, 42.0, 0.04, 2.316, (60, 140))[0][0]["height_m"] == 2.3
    with pytest.raises(ValueError, match="round to 0.1 or 0.01 m"):
        gen.swivels(2, [10.0], 3.0, round_to=0.05)


def test_the_exercise_allowance_is_a_third_in_ships_of_two_or_three_decks(gen):
    assert gen.exercise_allowance(26) == 6  # a fourth: the razee, one deck
    assert gen.exercise_allowance(26, decks=2) == 8  # a third: the 64
    assert gen.exercise_allowance(30, decks=3) == 10
    with pytest.raises(ValueError):
        gen.exercise_allowance(26, decks=4)


def test_the_rating_pass_knows_the_lateen(gen):
    assert gen.PEAK_COEFF["lateen"] == 1.25
    assert gen.static_kn([(10.0, 10.0, "lateen")], 20.0) > 0.0


# -- the gun deck's hooks (items 17 to 19) -------------------------------------------------


def test_the_lee_ports_update_shuts_nothing_and_a_shut_gun_neither_works_nor_fires():
    """Build-Ships.md §3.1 items 17 and 18: `ports.update` gives two empty sets and leaves the
    battery's `_shut` its class default, empty; a gun put in it by hand has no work, and a
    gun named to fire waits behind its port until it is opened."""
    assert ports.PORT_PLACES == ("broadside", "bow", "stern") == _PORT_GUN_PLACES
    assert ports.PORT_REOPEN_M == 0.15
    ship = load_ship(BRIG)
    battery = Battery(ship)
    firer = Firer(
        heel_deg=0.0,
        roll_deg=0.0,
        sea_height_m=0.0,
        weather_factor=1.0,
        half_beam_m=4.0,
        heading_rad=0.0,
        position=None,
    )
    assert ports.update(battery, firer) == (frozenset(), frozenset())
    assert battery._shut == frozenset() and "_shut" not in battery.__dict__
    gun = ship.guns["gun.1.starboard"]
    assert battery.wants_work(gun)  # empty, it wants loading
    battery._shut = frozenset({gun.id})
    assert not battery.wants_work(gun)
    gun.loaded, gun.primed, gun.run_out = Charge.ROUND, True, True
    battery.single = [gun.id]
    battery._fire(None, firer, None, None, 0, None, None)
    assert battery.single == [gun.id] and gun.fired == 0
    battery._shut = frozenset()
    battery._fire(None, firer, None, None, 0, None, None)
    assert battery.single == [] and gun.fired == 1


def test_the_lee_ports_events_are_registered_and_said_nowhere_yet():
    """Item 19: the two events for `at` and a stand-by, never emitted until the rule is
    built (no module records either kind), and absent till then: the brief and the
    stand-by tool offer neither, and a standing order at one is refused in its words."""
    from freesail.agents.agent import STAND_BY_WORDS
    from freesail.agents.tools import STAND_BY_EVENTS
    from freesail.api.practice_readings import LEE_PORTS_ABSENT
    from freesail.orders.errors import OrderError
    from freesail.standing.grammar import parse_standing

    assert EVENTS["the lee ports shut"].kind == "guns.ports_shut"
    assert EVENTS["the lee ports opened"].kind == "guns.ports_opened"
    for words in ("the lee ports shut", "the lee ports opened"):
        assert EVENTS[words].absent == LEE_PORTS_ABSENT
        assert words not in STAND_BY_EVENTS and words not in STAND_BY_WORDS
    with pytest.raises(OrderError, match="Nothing shuts the lee ports yet"):
        parse_standing(
            load_ship(BRIG), 'standing order "ports": at the lee ports shut then beat to quarters'
        )
    named = [
        p.name
        for p in sorted((ROOT / "freesail").rglob("*.py"))
        if '"guns.ports_' in p.read_text(encoding="utf-8")
    ]
    assert named == ["practice_readings.py"]


# -- the readings' hooks (items 20 and 21) -------------------------------------------------


def test_the_ship_graph_serves_the_profile_where_the_file_gives_one():
    plain = ship_graph(ship_from_dict(_doc(), "p.yaml"))["hull"]
    assert "profile" not in plain  # a document with none: its graph as before
    served = ship_graph(ship_from_dict(_doc(PROFILE), "p.yaml"))["hull"]["profile"]
    assert served == PROFILE and list(served) == list(PROFILE)
    assert json.loads(json.dumps(served)) == served  # plain lists, as the file's
    # a line the file does not give is not served
    lean = {k: PROFILE[k] for k in ("rail_m", "breadth_m")}
    assert ship_graph(ship_from_dict(_doc(lean), "p.yaml"))["hull"]["profile"] == lean


def test_the_lookups_by_a_sails_class_read_its_curve_class(monkeypatch):
    """Items 20 to 22: the served reef factor, the readings' luff and the polar's sheets
    read `Sail.curve_class` (each sail's own class, the gaff's for a lateen cut at the mast:
    every sail's own on the brig), shown by giving every sail another curve for the length of
    the test."""
    from freesail.evolutions import trim
    from freesail.physics import sails as sails_mod

    ship = load_ship(BRIG)
    course = ship.sails["fore.course"]
    assert _sail_entry(course)["reef_factor"] == 0.2  # the square class's
    monkeypatch.setattr(Sail, "curve_class", property(lambda s: "gaff"))
    assert _sail_entry(course)["reef_factor"] == 0.25  # the gaff's
    asked: list[str] = []

    class Classes(dict):
        def get(self, key, default=None):
            asked.append(key)
            return super().get(key, default)

    monkeypatch.setattr(sails_mod, "SAIL_CLASSES", Classes(sails_mod.SAIL_CLASSES))
    monkeypatch.setattr(Sail, "curve_class", property(lambda s: "the curve's class"))
    course.state = SailState.SET
    assert sail_reading(ship, course)["shaking"] is False and "the curve's class" in asked
    sheeted: list[str] = []
    monkeypatch.setattr(trim, "wanted_sheet_angle", lambda cls, awa: sheeted.append(cls) or 0.3)
    ship.sails["main.spanker"].state = SailState.SET
    S._trim_for(ship, 1.0)
    assert sheeted and set(sheeted) == {"the curve's class"}


# -- the world's hooks (items 22 to 25) ----------------------------------------------------


def _sea():
    """The frigate south-west of the Lizard, as `tests/test_ships.py` puts her."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
        position=Position(49.60, -5.40).to_dict(),
        region="channel-west",
    )
    return make_world(7, "data/ships/frigate-36.yaml", sc)


def test_a_descriptions_fit_and_roles_are_its_files_and_absent_where_it_gives_none(monkeypatch):
    """Item 22 (§8.1): `description` carries the file's own `fit` and `roles` for it, the
    roles kept a list; no file gives either yet, so every description is as it was."""
    for key in S.DESCRIPTIONS:
        assert set(S.description(key)) == {"file", "rig", "what"}, key
    assert S._description_value("roles", ["cruiser", "kings-ship"]) == ["cruiser", "kings-ship"]
    assert S._description_value("roles", "merchant") == ["merchant"]
    assert S._description_value("what", 1) == "1"
    assert S._default_fit(BRIG) == "diligence class 1796"
    assert S._default_fit("data/ships/topsail-schooner.yaml") == UNARMED  # no armament
    own = {"brig-sloop": {"what": "a brig-sloop", "fit": "carronades", "roles": ["cruiser"]}}
    monkeypatch.setattr(S, "file_descriptions", lambda ship_file: own)
    d = S.description("brig-sloop")
    assert (d["fit"], d["roles"], d["what"], d["rig"]) == (
        "carronades",
        ["cruiser"],
        "a brig-sloop",
        "a brig",
    )
    assert d["roles"] is not own["brig-sloop"]["roles"]  # the cached file's list kept apart


def test_a_far_ships_role_and_her_descriptions_fit_and_her_saved_forms(monkeypatch):
    """Item 22 (§8.1): `role:` is one of her description's roles and of `captains.ROLES`, or
    refused in words; with no `fit:` she takes her description's fit only where it is not
    her file's default; while she has no role and the default fit, `to_dict` and the
    checkpoint's pickle hold nothing new."""
    world = _sea()
    own = {"brig-sloop": {"fit": "diligence class 1796", "roles": ["cruiser", "kings-ship"]}}
    monkeypatch.setattr(S, "file_descriptions", lambda ship_file: own)
    spec = {
        "description": "brig-sloop",
        "name": "Hazard",
        "nation": "britain",
        "position": Position(49.5, -5.5).to_dict(),
        "goal": "bound for Falmouth",
    }
    plain = S.vessel_from_spec(world, dict(spec), 1)
    assert (plain.role, plain.fit) == ("", "")  # her file's default: nothing set
    assert "role" not in plain.to_dict() and "fit" not in plain.to_dict()
    assert "role" not in plain.__getstate__()
    again = pickle.loads(pickle.dumps(plain))
    assert again.role == "" and "role" not in again.__dict__  # the class default
    given = S.vessel_from_spec(world, dict(spec, role="kings-ship"), 2)
    assert given.role == "kings-ship" and given.to_dict()["role"] == "kings-ship"
    assert pickle.loads(pickle.dumps(given)).role == "kings-ship"
    assert brains.role_of_vessel(given, None) == "kings-ship"
    assert brains.role_of_vessel(plain, None) == "cruiser"
    with pytest.raises(ValueError, match="'privateer' is no role a brig-sloop takes"):
        S.vessel_from_spec(world, dict(spec, role="privateer"), 3)
    with pytest.raises(ValueError, match="'pirate' is no captain's role"):
        S.vessel_from_spec(world, dict(spec, role="pirate"), 3)
    own["brig-sloop"] = {"fit": UNARMED}
    with pytest.raises(ValueError, match="her file gives a brig-sloop no role"):
        S.vessel_from_spec(world, dict(spec, role="cruiser"), 3)
    unarmed = S.vessel_from_spec(world, dict(spec), 4)
    assert unarmed.fit == UNARMED and unarmed.to_dict()["fit"] == UNARMED
    named = S.vessel_from_spec(world, dict(spec, fit="diligence class 1796"), 5)
    assert named.fit == "diligence class 1796"  # the scenario's fit over the description's


def test_the_vessels_role_comes_first_and_the_new_men_of_war_are_kings_ships():
    """Item 23: `role_of_vessel` and `role_for` take the vessel's role first; the
    sixty-four, the razee and the seventy-four sail by the King's ship's doctrine."""
    v = S.Vessel("x", "X", "a ship", BRIG, "britain", Position(49.4, -5.4))
    for key in ("frigate", "sixty-four", "razee", "seventy-four"):
        v.description = key
        assert brains.role_of_vessel(v, None) == "kings-ship", key
    v.description = "merchant brig"
    assert brains.role_of_vessel(v, None) == "merchant"
    v.role = "packet"
    assert brains.role_of_vessel(v, None) == "packet"
    # the near captain's: a role given (a crewed ship's, from her far brain), and none
    assert captains.role_for(SimpleNamespace(), None, "packet") == "packet"
    assert captains.role_for(SimpleNamespace(), None) == "merchant"


def test_a_crewed_captain_takes_his_vessels_role_from_her_far_brain(monkeypatch):
    """Item 23 through a real crewed World: her far brain carries the role her scenario gave
    her into her captain at the promotion (`FarCaptain.fold_in`), and he keeps it when his
    intent is changed (a squadron's goal by the book); a vessel with none is promoted as
    before, nothing new on her captain."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    own = {"merchant brig": {"roles": ["merchant", "packet"]}}
    monkeypatch.setattr(S, "file_descriptions", lambda ship_file: own)
    made = []
    for name, role, where in (
        ("Swift", "packet", "49 33 N 5 30 W"),
        ("Plain", "", "49 31 N 5 31 W"),
    ):
        w.vessels.serial += 1
        spec = {
            "description": "merchant brig",
            "name": name,
            "nation": "britain",
            "position": where,
            "goal": "bound for Falmouth",
            "intent": "bound for Falmouth",
            "role": role,
        }
        made.append(S.vessel_from_spec(w, spec, w.vessels.serial))
        w.vessels.add(made[-1])
    w.run(61)
    swift, plain = (v.crew.captain for v in made)
    assert (swift.role, swift.scenario_role, swift.doctrine.role) == ("packet",) * 3
    swift.set_intent("bound for Plymouth")
    assert swift.role == "packet" and swift.doctrine.role == "packet"
    assert plain.role == "merchant" and "scenario_role" not in plain.__dict__
    plain.set_intent("bound for Plymouth")
    assert plain.role == captains.role_for(plain.world, plain.intent)  # by his intent, as before


def test_the_size_words_rank_the_new_ships_the_razees_first():
    """Item 24 (Indf §8): the ranks, and the words matched in order, the razee's first."""
    rank = captains.SIZE_RANK
    assert (rank["razee"], rank["sixty-four"], rank["seventy-four"]) == (3, 4, 4)
    assert (rank["hermaphrodite brig"], rank["bilander"]) == (2, 1)
    assert [w for w, _ in captains._SIZE_WORDS[:7]] == [
        "razee",
        "sixty-four",
        "seventy-four",
        "ship of the line",
        "two-decker",
        "bilander",
        "frigate",
    ]
    razee = "a razee, a heavy frigate cut down from a sixty-four, one tier of twenty-four-pounders"
    assert captains.size_of_words(razee) == 3 and captains.size_rank_of(razee) == 3
    assert captains.size_rank_of("a cut-down sixty-four razee") == 3
    sixty_four = "a sixty-four, a ship of the line of two tiers of ports"
    assert captains.size_of_words(sixty_four) == 4 and captains.size_rank_of(sixty_four) == 4
    assert captains.size_rank_of("a ship of the line") == captains.size_rank_of("two-decker") == 4
    assert captains.size_rank_of("a bilander") == 1
    # the words of today's sail rank as before
    assert captains.size_of_words("a brig-sloop of war, sixteen ports a side") == 2
    assert captains.size_of_words("a ship") == captains.size_rank_of("a French frigate") == 3
    assert captains.size_rank_of("a chasse-marée") == 1 and captains.size_of_words("a sail") == 0


def test_the_man_of_war_sets_hold_the_new_ships(monkeypatch):
    """Item 25: the two sets of men of war by description, and the escort's."""
    new = {"sixty-four", "razee", "seventy-four"}
    assert new < regimes._MAN_OF_WAR_DESCRIPTIONS and new < squadrons._MAN_OF_WAR_DESCRIPTIONS
    body = SimpleNamespace(brain=None, description="")
    monkeypatch.setattr(squadrons, "_body", lambda world, vid: body)
    me = SimpleNamespace(commander="c")
    for key in ("frigate", "brig-sloop", *sorted(new)):
        body.description = key
        assert squadrons.Squadron._is_escort(me, None, "x"), key
    body.description = "merchant brig"
    assert not squadrons.Squadron._is_escort(me, None, "x")
