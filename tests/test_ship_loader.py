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


SHIPS = [
    "data/ships/frigate-36.yaml",
    "data/ships/topsail-schooner.yaml",
    "data/ships/cutter.yaml",  # package 32b: the four ships
    "data/ships/brig.yaml",
]


@pytest.mark.parametrize("path", SHIPS)
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
    # studding sails on a yard know their side and their parent yard. Milestone 3b (package
    # 22): the ringtail and the water sail are studding-class sails on a gaff sail's boom,
    # lying in that sail's plane, and have no side (spec 3b §6.4).
    for sail in ship.sails.values():
        if sail.cls == "studding" and sail.roles.get("yard"):
            assert sail.side in {"starboard", "larboard"}
            assert ship.spar_of_role(sail, "boom").side == sail.side
        elif sail.cls == "studding":
            boom = ship.spar_of_role(sail, "boom")
            assert sail.side is None and boom.side is None
            assert boom.cls == "boom" or ship.parent_of(boom).cls == "boom"


def test_frigate_has_the_cool_obscure_kit():
    ship = load_ship("data/ships/frigate-36.yaml")
    # the studding sails proper (the "studdingsails" group); milestone 3b added three more
    # studding-class sails, the ringtail and two save-alls, kept in the sail room (spec 3b §6.4)
    stuns = [s for s in ship.sails.values() if s.cls == "studding"]
    assert len(ship.groups["studdingsails"]) == 10  # fore lower, fore/main topmast and topgallant
    assert len(stuns) == 13
    assert set(ship.groups["occasional sails"]) == {s.id for s in stuns} - set(
        ship.groups["studdingsails"]
    )
    assert "mizzen.spanker" in ship.sails
    assert ship.aliases["driver"] == "mizzen.spanker"


def test_schooner_is_mostly_fore_and_aft():
    ship = load_ship("data/ships/topsail-schooner.yaml")
    fa = sum(s.area_m2 for s in ship.sails.values() if s.is_fore_and_aft)
    sq = sum(s.area_m2 for s in ship.sails.values() if s.cls == "square")
    assert fa > sq


def test_cutter_is_a_one_master_with_a_running_bowsprit():
    """Package 32b (spec M5 §23): one mast, a gaff mainsail on a boom over the counter, a
    square sail, a topsail and a topgallant on three yards, the foresail on the forestay,
    the jib on the running bowsprit, the storm trysail and storm jib in the sail room."""
    ship = load_ship("data/ships/cutter.yaml")
    assert ship.spec.warnings == []
    assert [s.id for s in ship.spars.values() if s.cls == "mast"] == ["main.mast"]
    assert sorted(s.id for s in ship.spars.values() if s.is_yard) == [
        "square_sail.yard",
        "topgallant.yard",
        "topsail.yard",
    ]
    bent = [s for s in ship.sails.values() if s.state is not SailState.UNBENT]
    fa = sum(s.area_m2 for s in bent if s.is_fore_and_aft)
    sq = sum(s.area_m2 for s in bent if s.cls == "square")
    assert fa > sq
    assert ship.groups["plain sail"] == ["main.sail", "fore.staysail", "jib", "topsail"]
    assert ship.aliases["foresail"] == "fore.staysail"  # a cutter's foresail is her staysail
    assert ship.aliases["the crossjack"] == "square_sail"  # Steel's name for the square sail
    assert ship.sails["main.sail"].reef_bands == 4  # Steel 1794 p. 120
    assert ship.sails["storm_trysail"].in_place_of == "main.sail"
    assert ship.sails["storm_jib"].in_place_of == "jib"
    bowsprit = ship.spars["bowsprit"]
    assert bowsprit.running and bowsprit.rigged_out
    assert 0.0 < bowsprit.housed_length_m < bowsprit.full_length_m == bowsprit.length_m
    assert ship.sails["jib"].roles["halyard_spar"] == "bowsprit"
    assert ship.spar_chain("jib")[0] is bowsprit  # the jib loads the bowsprit its tack rides
    assert "halyard_spar" not in ship.sails["storm_jib"].roles  # its tack lies at the reef
    assert ship.line_of(bowsprit, "outhaul") is not None  # the heel-rope
    assert ship.spec.crew is not None and ship.spec.crew.complement == 30
    assert ship.spec.crew.stations["fore_top"] == ship.spec.crew.stations["main_top"] == 0


def test_brig_is_the_frigate_less_a_mast():
    """Package 32b (spec M5 §25): two square-rigged masts with royals, the spanker on the
    main, the head sails complete, the staysails between the masts, studding sails by the
    frigate's rule, the storm canvas of a brig."""
    ship = load_ship("data/ships/brig.yaml")
    assert ship.spec.warnings == []
    assert [s.id for s in ship.spars.values() if s.cls == "mast"] == ["fore.mast", "main.mast"]
    assert "mizzen.mast" not in ship.spars
    for name in ("fore", "main"):
        for level in ("topsail", "topgallant", "royal"):
            assert f"{name}.{level}" in ship.sails
        assert f"{name}.course" in ship.sails
    assert ship.aliases["spanker"] == "main.spanker" == ship.aliases["driver"]
    assert ship.aliases["mainsail"] == "main.course"  # as the frigate's, the square one
    assert ship.groups["headsails"] == ["fore.topmast_staysail", "jib", "flying_jib"]
    assert ship.groups["staysails"] == [
        "fore.topmast_staysail",
        "main.staysail",
        "main.topmast_staysail",
        "main.topgallant_staysail",
    ]
    assert len(ship.groups["studdingsails"]) == 10
    assert set(ship.groups["storm canvas"]) == {
        "fore.storm_staysail",
        "main.storm_staysail",
        "storm_trysail",
    }
    assert ship.sails["storm_trysail"].in_place_of == "main.spanker"
    assert not ship.spars["bowsprit"].running and ship.spars["bowsprit"].rigged_out
    assert ship.spec.crew is not None and ship.spec.crew.complement == 121
    assert [p.post for p in ship.spec.crew.posts][:2] == ["commander", "lieutenant"]


def _bowsprit(**keys):
    d = {"id": "bowsprit", "class": "bowsprit", "x_m": 10.0, "length_m": 8.0}
    d.update(keys)
    return d


@pytest.mark.parametrize(
    "spar, message",
    [
        ({"id": "yard2", "class": "yard", "on": "mast", "running": True}, "only a bowsprit runs"),
        (_bowsprit(running=True), "gives no 'housed_length_m'"),
        (_bowsprit(running=True, housed_length_m=9.0), "shorter than its full outboard"),
        (_bowsprit(housed_length_m=5.0), "not a running bowsprit"),
        (_bowsprit(rigged_out=False), "only a studding sail boom or a running bowsprit"),
    ],
)
def test_the_running_bowsprit_is_validated_in_words(spar, message):
    """Package 32b: the running bowsprit's flag and its housed length are checked by the
    loader as every other key is, with a sentence."""
    import copy

    d = copy.deepcopy(MINIMAL)
    d["spars"] = [s for s in d["spars"] if s["id"] != "bowsprit"] + [spar]
    with pytest.raises(ShipFileError, match=message):
        ship_from_dict(d, "bowsprit")


def test_a_running_bowsprit_starts_where_its_file_says():
    import copy

    d = copy.deepcopy(MINIMAL)
    d["spars"] = [s for s in d["spars"] if s["id"] != "bowsprit"]
    d["spars"].append(_bowsprit(running=True, housed_length_m=5.0, rigged_out=False))
    ship = ship_from_dict(d, "bowsprit")
    bowsprit = ship.spars["bowsprit"]
    assert bowsprit.running and not bowsprit.rigged_out
    assert bowsprit.length_m == 5.0 and bowsprit.full_length_m == 8.0
    d["spars"][-1].pop("rigged_out")
    assert ship_from_dict(d, "bowsprit").spars["bowsprit"].length_m == 8.0


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


def test_mast_rake_is_read_and_bounded():
    import copy

    d = copy.deepcopy(MINIMAL)
    d["spars"][0]["rake_deg"] = 4.5
    ship = ship_from_dict(d, "raked")
    assert ship.spars["mast"].rake == pytest.approx(0.0785, abs=1e-3)
    d["spars"][0]["rake_deg"] = -6.0  # a polacre's forward-raking fore mast is allowed
    assert ship_from_dict(d, "raked").spars["mast"].rake < 0
    d["spars"][0]["rake_deg"] = 45.0
    with pytest.raises(ShipFileError, match="rakes between"):
        ship_from_dict(d, "raked")
    d["spars"][0]["rake_deg"] = 2.0
    d["spars"][2]["rake_deg"] = 2.0  # a yard does not rake
    with pytest.raises(ShipFileError, match="only a mast"):
        ship_from_dict(d, "raked")


def test_reference_ships_carry_their_rake():
    frigate = load_ship("data/ships/frigate-36.yaml")
    rakes = {m: frigate.spars[f"{m}.mast"].rake for m in ("fore", "main", "mizzen")}
    assert rakes["fore"] < rakes["main"] < rakes["mizzen"]
    schooner = load_ship("data/ships/topsail-schooner.yaml")
    assert schooner.spars["fore.mast"].rake == pytest.approx(schooner.spars["main.mast"].rake)
    assert schooner.spars["main.mast"].rake > frigate.spars["mizzen.mast"].rake
