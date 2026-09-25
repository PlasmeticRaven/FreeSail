import copy

import pytest

from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState
from freesail.ship.schema import ShipFileError

MINIMAL = {
    "ship": {"name": "Test", "rig": "sloop"},
    "hull": {
        "length_waterline_m": 20.0,
        "beam_m": 6.0,
        "draught_m": 2.5,
        "displacement_kg": 80000,
        "gm_m": 0.9,
    },
    "spars": [
        {"id": "mast", "class": "mast", "x_m": 2.0, "height_m": 15.0, "rating_kn": 200},
        {"id": "topmast", "class": "topmast", "steps_on": "mast", "height_m": 8.0},
        {
            "id": "topsail.yard",
            "class": "yard",
            "on": "topmast",
            "length_m": 9.0,
            "height_m": 17.0,
            "brace_limit_deg": 42,
        },
        {"id": "gaff", "class": "gaff", "on": "mast", "length_m": 6.0, "height_m": 13.0},
        {"id": "boom", "class": "boom", "on": "mast", "length_m": 9.0, "height_m": 1.5},
        {"id": "bowsprit", "class": "bowsprit", "x_m": 11.0, "length_m": 7.0, "height_m": 2.0},
    ],
    "sails": [
        {
            "id": "topsail",
            "class": "square",
            "yard": "topsail.yard",
            "area_m2": 40,
            "reef_bands": 1,
            "x_m": 2.0,
            "centre_height_m": 15.0,
        },
        {
            "id": "mainsail",
            "class": "gaff",
            "mast": "mast",
            "gaff": "gaff",
            "boom": "boom",
            "area_m2": 90,
            "reef_bands": 2,
            "x_m": -2.0,
            "centre_height_m": 7.0,
        },
        {
            "id": "jib",
            "class": "jibheaded",
            "stay": "jib.stay",
            "area_m2": 30,
            "x_m": 9.0,
            "centre_height_m": 6.0,
        },
    ],
    "lines": [
        {"id": "topsail.yard.halyard", "class": "halyard", "of": "topsail.yard"},
        {
            "id": "topsail.yard.brace.starboard",
            "class": "brace",
            "of": "topsail.yard",
            "side": "starboard",
        },
        {
            "id": "topsail.yard.brace.larboard",
            "class": "brace",
            "of": "topsail.yard",
            "side": "larboard",
        },
        {"id": "topsail.sheet.starboard", "class": "sheet", "of": "topsail", "side": "starboard"},
        {"id": "topsail.sheet.larboard", "class": "sheet", "of": "topsail", "side": "larboard"},
        {"id": "gaff.throat_halyard", "class": "throat_halyard", "of": "gaff"},
        {"id": "gaff.peak_halyard", "class": "peak_halyard", "of": "gaff"},
        {"id": "mainsail.sheet", "class": "sheet", "of": "mainsail"},
        {"id": "jib.stay", "class": "stay", "of": "topmast", "rating_kn": 60},
        {"id": "jib.halyard", "class": "halyard", "of": "jib"},
        {"id": "jib.sheet.starboard", "class": "sheet", "of": "jib", "side": "starboard"},
        {"id": "jib.sheet.larboard", "class": "sheet", "of": "jib", "side": "larboard"},
    ],
    "groups": {"square sails": ["topsail"], "headsails": ["jib"]},
    "aliases": {"the main": "mainsail", "kites": "square sails"},
}


def minimal(**changes):
    d = copy.deepcopy(MINIMAL)
    for path, value in changes.items():
        d[path] = value
    return d


def test_minimal_loads_and_indexes():
    ship = ship_from_dict(MINIMAL, "minimal")
    assert ship.name == "Test"
    assert set(ship.spars) == {"mast", "topmast", "topsail.yard", "gaff", "boom", "bowsprit"}
    assert ship.sails["topsail"].state is SailState.FURLED
    assert ship.yard_of("topsail").id == "topsail.yard"
    assert ship.sail_of("topsail.yard").id == "topsail"
    assert ship.sail_of("gaff").id == "mainsail"
    assert [s.id for s in ship.spar_chain("topsail")] == ["topsail.yard", "topmast", "mast"]
    assert [s.id for s in ship.spar_chain("jib")] == ["topmast", "mast"]
    assert ship.mast_of("topsail").id == "mast"
    assert {ln.id for ln in ship.braces_of("topsail.yard")} == {
        "topsail.yard.brace.starboard",
        "topsail.yard.brace.larboard",
    }
    assert ship.line_of("topsail.yard", "brace", "larboard").id == "topsail.yard.brace.larboard"
    assert ship.halyard_of("topsail").id == "topsail.yard.halyard"
    assert ship.halyard_of("mainsail").id == "gaff.peak_halyard"
    assert ship.halyard_of("jib").id == "jib.halyard"
    dep = {p.id for p in ship.dependents("topmast")}
    assert {
        "topsail.yard",
        "topsail",
        "topsail.yard.halyard",
        "jib",
        "jib.stay",
        "jib.halyard",
    } <= dep
    assert "mainsail" not in dep
    assert {s.id for s in ship.sails_on("mast")} == {"topsail", "mainsail", "jib"}


def test_default_ratings_are_filled_with_one_warning_per_class():
    ship = ship_from_dict(MINIMAL, "minimal")
    assert ship.spars["topmast"].rating_kn > 0
    assert ship.lines["topsail.sheet.starboard"].rating_kn > 0
    kinds = [w.split(" of class ")[1].split(" ")[0] for w in ship.spec.warnings]
    assert len(kinds) == len(set(kinds))  # one warning per class
    assert any("brace" in w for w in ship.spec.warnings)


@pytest.mark.parametrize(
    "mutate, message",
    [
        (lambda d: d["ship"].pop("name"), "ship.name"),
        (lambda d: d.pop("hull"), "'hull' is missing"),
        (lambda d: d["hull"].pop("gm_m"), "missing 'gm_m'"),
        (lambda d: d["spars"][2].update({"class": "spinnaker_pole"}), "not a spar class"),
        (lambda d: d["spars"][2].update({"on": "nowhere"}), "no spar with that id"),
        (lambda d: d["spars"][1].pop("steps_on"), "only a mast or bowsprit"),
        (lambda d: d["spars"][0].update({"steps_on": "topmast"}), "stands on itself"),
        (lambda d: d["sails"][0].pop("yard"), "has no 'yard'"),
        (lambda d: d["sails"][0].update({"yard": "gaff"}), "that is a gaff"),
        (lambda d: d["sails"][1].pop("gaff"), "has no 'gaff'"),
        (lambda d: d["sails"][2].pop("stay"), "neither a 'stay'"),
        (lambda d: d["sails"][2].update({"stay": "jib.halyard"}), "not a stay"),
        (lambda d: d["sails"][0].update({"boom": "boom"}), "does not take a 'boom'"),
        (lambda d: d["sails"][0].update({"class": "parachute"}), "not a sail class"),
        (lambda d: d["sails"][0].update({"reef_bands": -1}), "reef_bands"),
        (lambda d: d["lines"][0].update({"of": "ghost"}), "no spar or sail with that id"),
        (
            lambda d: d["lines"][0].update({"class": "brace", "of": "topsail"}),
            "cannot be of a sail",
        ),
        (lambda d: d["lines"][1].update({"of": "gaff"}), "not a yard"),
        (lambda d: d["lines"][1].update({"side": "left"}), "starboard or larboard"),
        (lambda d: d["sails"].append(dict(d["sails"][0])), "used for both"),
        (lambda d: d["groups"].update({"topsail": ["jib"]}), "same name as a part"),
        (lambda d: d["groups"].update({"kites2": ["nothing"]}), "not a part"),
        (lambda d: d["aliases"].update({"x": "nothing"}), "not a part or a group"),
        (
            lambda d: d["spars"].append(
                {"id": "sb", "class": "studdingsail_boom", "on": "topsail.yard", "length_m": 4}
            ),
            "needs a 'side'",
        ),
    ],
)
def test_validation_rejects_with_a_sentence(mutate, message):
    d = copy.deepcopy(MINIMAL)
    mutate(d)
    with pytest.raises(ShipFileError) as e:
        ship_from_dict(d, "bad.yaml")
    assert message in str(e.value)
    assert str(e.value).startswith("bad.yaml:")


def test_jibheaded_on_a_mast_is_allowed():
    d = copy.deepcopy(MINIMAL)
    d["sails"].append(
        {
            "id": "gaff_topsail",
            "class": "jibheaded",
            "mast": "topmast",
            "area_m2": 20,
            "x_m": -1.0,
            "centre_height_m": 18.0,
        }
    )
    ship = ship_from_dict(d, "ok")
    assert [s.id for s in ship.spar_chain("gaff_topsail")] == ["topmast", "mast"]


def test_missing_file_is_a_sentence(tmp_path):
    with pytest.raises(ShipFileError) as e:
        load_ship(tmp_path / "nope.yaml")
    assert "no such ship file" in str(e.value)


def test_bad_yaml_is_a_sentence(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("ship: [unclosed")
    with pytest.raises(ShipFileError) as e:
        load_ship(p)
    assert "not valid YAML" in str(e.value)


@pytest.mark.parametrize("path", ["data/ships/frigate-36.yaml", "data/ships/topsail-schooner.yaml"])
def test_reference_ships_load(path):
    ship = load_ship(path)
    assert ship.sails and ship.spars and ship.lines
    # every sail has a spar chain that reaches a root spar
    for sail in ship.sails.values():
        chain = ship.spar_chain(sail)
        assert chain, sail.id
        assert chain[-1].parent is None
    # every yard has two braces and every square sail two sheets
    for sail in ship.sails.values():
        if sail.cls == "square":
            assert len(ship.braces_of(ship.yard_of(sail))) == 2, sail.id
            assert len(ship.sheets_of(sail)) == 2, sail.id
    # studding sails know their side and their parent yard
    for sail in ship.sails.values():
        if sail.cls == "studding":
            assert sail.side in {"starboard", "larboard"}
            assert ship.spar_of_role(sail, "boom").side == sail.side


def test_frigate_has_the_cool_obscure_kit():
    ship = load_ship("data/ships/frigate-36.yaml")
    stuns = [s for s in ship.sails.values() if s.cls == "studding"]
    assert len(stuns) == 10  # fore lower, fore/main topmast, fore/main topgallant, both sides
    assert "mizzen.spanker" in ship.sails
    assert ship.aliases["driver"] == "mizzen.spanker"


def test_schooner_is_mostly_fore_and_aft():
    ship = load_ship("data/ships/topsail-schooner.yaml")
    fa = sum(s.area_m2 for s in ship.sails.values() if s.is_fore_and_aft)
    sq = sum(s.area_m2 for s in ship.sails.values() if s.cls == "square")
    assert fa > sq


def test_frigate_particulars_stay_in_period():
    """Package 8: the frigate is a 36-gun 18-pounder of 1795 (the full set of checks is in
    tests/test_ship_particulars.py; these are the three an edit is most likely to break)."""
    ship = load_ship("data/ships/frigate-36.yaml")
    plain = sum(ship.sails[i].area_m2 for i in ship.groups["plain sail"])
    assert 1_300 <= plain <= 1_860  # about 17,000 sq ft of plain sail
    assert 1_100_000 <= ship.hull.spec.displacement_kg <= 1_450_000  # 1.2 to 1.5 x 933 bm
    main_truck = (
        sum(s.height_m for s in ship.spar_chain("main.royal_mast"))
        + ship.spars["main.royal_mast"].height_m
    )
    assert 40.0 <= main_truck <= 48.0  # metres above the deck; she is 43.6 m on the gundeck
    assert 20.0 <= ship.spars["main.mast"].height_m <= 24.0  # a 74 ft lower mast above deck
    assert 23.5 <= ship.spars["main.yard"].length_m <= 25.7  # 78 to 84 ft
