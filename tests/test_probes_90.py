"""Package 90, stage 0: the inert hooks for the Spanish and Mediterranean ships
(docs/design/Plan-Package90.md §5.1 items 1 to 10).

Nothing in the game moves: no committed file carries a new key, and each registry's new words
are read only where a description names them. Here:
- the four probes of `tests/rig_fixtures.py` (the lead's tartane and polacre, and the engine's
  note's xebec and three-decker, Design-Package90-Engine.md §0), classed through the golden
  table's gates as measured at stage 0's head; the two new ones load, and load again from their
  files;
- no committed file carries `sweeps:`, a towed boat, a hull's `helm` (`tiller` or any), or a
  whole lateen with `dipping`, read off the file itself and again as loaded;
- each new key's refusals in words, what each takes, and each spec pickled as before while the
  key holds its default;
- the generator's five new modules, stubs writing nothing, named after package 75's four, and
  `lateen.py` a docstring alone; `period.py`'s two units;
- every description of the game ranks as before (`captains.SIZE_RANK`, `size_of_words`,
  `size_rank_of`, `size_of_file`), by the figures measured at stage 0's head and by the word
  table with package 90's words taken out; and package 90's words rank as the plan places them,
  each before any row that matches inside the words that name her;
- the men-of-war sets, `role_of_vessel` and the hail's words take the corvette, the
  three-decker and the xebec.

Stage 0L (the plan's §5.2), the whole lateen's interfaces, laid as inert:
- each probe with a whole lateen (the tartane, the polacre, the xebec) loads with `dipping` on
  its whole lateens and classes as it does without it, the key changing nothing else of her;
- the refusals that touch `dipping`, for a lateen cut at the mast, for every class refused
  before, and for a lug, word for word as measured at stage 0's head (94ea1dba);
- `Sail.lug_side` kept for a dipping lateen by the plain class default, no new class;
- the ship's practice for the yard, `ship.extra["lateen_practice"]`, read with its default and
  set by nothing.
"""

from __future__ import annotations

import ast
import copy
import dataclasses
import importlib.util
import pickle
from functools import cache
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from rig_fixtures import (
    THREE_DECKER_COMPLEMENT,
    brig_with_settee_doc,
    polacre_probe,
    polacre_probe_doc,
    tartane_probe,
    tartane_probe_doc,
    three_decker_probe,
    three_decker_probe_doc,
    write_ship,
    xebec_probe,
    xebec_probe_doc,
)

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders import signals
from freesail.physics.sails import _square_rigged, against_the_mast
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, ship_from_dict, spec_from_dict
from freesail.ship.parts import Sail, SailState
from freesail.ship.schema import (
    BOAT_KEYS,
    FIT_KEYS,
    FIT_OWN_BILL,
    HELM_KINDS,
    SWEEPS_KEYS,
    ShipFileError,
    SweepsSpec,
)
from freesail.world import brains, captains, regimes, squadrons
from freesail.world import ships as S

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
NEW_MODULES = ("tartane", "polacre", "xebec", "diana", "concepcion")
PACKAGE_90_WORDS = (
    "three-decker",
    "first rate",
    "corvette",
    "ship-sloop",
    "ship sloop",
    "xebec",
    "polacre",
    "tartane",
)
SWEEPS = {"number": 16, "men_each": 3, "thrust_n": 50, "power_w": 60, "tiring_h": 3.0}


# -- the four probes (items 9 and 10) ---------------------------------------------------------


def _classing(ship: Ship) -> dict:
    """The golden table's gates (tests/test_rig_classing.py), plain sail set, by id."""
    for sid in ship.groups.get("plain sail", []):
        ship.sails[sid].state = SailState.SET
    head, after = scripts.head_and_after_yards(ship)
    back = scripts.yards_to_back(ship)
    _, stagger = yard_trim.stagger(ship, {y.id: y.brace_limit for y in scripts.working_yards(ship)})
    return {
        "masts": [m.id for m in scripts._masts_with_yards(ship)],
        "head": [y.id for y in head],
        "after": [y.id for y in after],
        "backed": ship.mast_of(back[0]).id if back else None,
        "to_back": [y.id for y in back],
        "square": _square_rigged(ship),
        "stagger": None if stagger is None else round(stagger, 1),
        "driver": [s.id for s in scripts.after_gaff_sails(ship)],
        "boom": [s.id for s in scripts.boom_sails(ship)],
        "dipping": [s.id for s in scripts.dipping_lugs(ship)],
        "schooner_mast": [p for p in ship.parts if ship.on_schooner_mast(p)],
    }


# Each probe's classing, measured at stage 0's head (before the schema's three keys and the
# words, and again after them: the same). The three-decker classes as the 74 does
# (tests/test_bellerophon.py, her classing); the xebec, three whole lateens and no braced yard,
# has no mast with yards (docs/design/Design-Ship-Xebec.md §4.3, observed on the probe).
FORE_74 = ["fore.yard", "fore.topsail.yard", "fore.topgallant.yard", "fore.royal.yard"]
MAIN_74 = ["main.yard", "main.topsail.yard", "main.topgallant.yard", "main.royal.yard"]
MIZEN_74 = ["mizzen.topsail.yard", "mizzen.topgallant.yard", "mizzen.royal.yard"]
NONE = {
    "after": [],
    "square": False,
    "stagger": None,
    "driver": [],
    "boom": [],
    "dipping": [],
    "schooner_mast": [],
}
CLASSING = {
    "tartane": (
        tartane_probe,
        {
            **NONE,
            "masts": ["main.mast"],
            "head": ["topsail.yard"],
            "backed": "main.mast",
            "to_back": ["topsail.yard"],
        },
    ),
    "polacre": (
        polacre_probe,
        {
            **NONE,
            "masts": ["main.mast"],
            "head": ["main.yard", "main.topsail.yard"],
            "backed": "main.mast",
            "to_back": ["main.yard", "main.topsail.yard"],
        },
    ),
    "xebec": (
        xebec_probe,
        {**NONE, "masts": [], "head": [], "backed": None, "to_back": []},
    ),
    "three-decker": (
        three_decker_probe,
        {
            "masts": ["fore.mast", "main.mast", "mizzen.mast"],
            "head": [*FORE_74, "spritsail.yard", "sprit_topsail.yard"],
            "after": [*MAIN_74, *MIZEN_74, "mizzen.crossjack.yard"],
            "backed": "main.mast",
            "to_back": MAIN_74,
            "square": True,
            "stagger": 2.0,
            "driver": ["mizzen.course"],
            "boom": ["mizzen.course"],
            "dipping": [],
            "schooner_mast": [],
        },
    ),
}


@pytest.mark.parametrize("name", list(CLASSING))
def test_each_probe_classes_as_measured_at_stage_0(name):
    build, want = CLASSING[name]
    assert _classing(build()) == want


def test_the_three_decker_classes_as_the_74_she_is_made_from():
    seventy_four = _classing(load_ship(ROOT / "data" / "ships" / "seventy-four.yaml"))
    assert _classing(three_decker_probe()) == seventy_four


@pytest.mark.parametrize(
    "name, build, doc",
    [
        ("xebec", xebec_probe, xebec_probe_doc),
        ("three-decker", three_decker_probe, three_decker_probe_doc),
    ],
)
def test_the_two_new_probes_load_and_load_again_from_their_files(name, build, doc, tmp_path):
    ship = build()
    assert ship.spec.warnings == []
    again = load_ship(write_ship(doc(), tmp_path, name))
    assert again.spec.warnings == []
    assert again.spec.spars == ship.spec.spars and again.spec.sails == ship.spec.sails
    assert again.spec.lines == ship.spec.lines and again.groups == ship.groups


def test_the_xebec_probe_has_three_whole_lateens_and_no_square_sail():
    ship = xebec_probe()
    lateens = [s.id for s in ship.sails.values() if s.cls == "lateen"]
    assert lateens == ["fore.lateen", "mizzen.lateen", "main.lateen"]
    assert not any(s.cut_at_mast for s in ship.sails.values())
    assert {s.cls for s in ship.spars.values() if s.id.endswith("lateen_yard")} == {"lateen_yard"}
    assert not [s.id for s in ship.sails.values() if s.cls in ("square", "studding")]
    assert ship.spars["main.lateen_yard"].length_m == 19.0
    assert ship.sails["main.lateen"].area_m2 == 150


def test_the_three_decker_probe_has_three_gun_decks_and_her_company():
    ship = three_decker_probe()
    decks = [word for word, _ in ship.spec.hull.profile.decks_m]
    assert decks == ["lower", "middle", "upper", "quarterdeck", "forecastle", "roundhouse"]
    assert ship.spec.crew.complement == THREE_DECKER_COMPLEMENT
    assert sum(ship.spec.crew.stations.values()) + len(ship.spec.crew.posts) == 839
    for fit in ship.spec.armament.fits.values():
        by_deck = {d: sum(1 for g in fit.guns if g.deck == d) for d in ("lower", "middle", "upper")}
        assert by_deck["middle"] == by_deck["upper"] == by_deck["lower"] == 28, fit.name


# -- the stage-0 keys and the files that carry them (item 10; one table since A3) -------------
#
# Each key stage 0 laid inert, with exactly the committed files that carry it (the lead's nudge
# 31). The step that writes a key into a file moves its row here, old beside new in
# docs/dev/TuningNotes.md; the test holds the files to the table both ways: a file in a row
# carries the key, and no file outside it does. Before A3 it was one guard that no file carried
# any of them.
TILLER_FILES = (
    "cutter",
    "hermaphrodite-brig",
    "lugger",
    "privateer-schooner",
    "smack",
    "topsail-schooner",
)
KEY_CARRIERS: dict[str, frozenset[str]] = {
    "sweeps": frozenset(),  # a ship's own sweeps, or a fit's: step A7, the xebec's
    "towed": frozenset(),  # a boat towed astern: step A4, the tartane's
    "helm": frozenset(TILLER_FILES),  # the hull's helm: step A3, the six tiller-steered files
    "dipping": frozenset(),  # a whole lateen dipped: the lateen hulls' files, after stage 0L
}


def _carried(doc: dict) -> dict[str, bool]:
    """Which of the stage-0 keys a file's document carries, read off the file itself."""
    fits = ((doc.get("armament") or {}).get("fits") or {}).values()
    whole = [s for s in doc["sails"] if s["class"] == "lateen" and not s.get("cut_at_mast")]
    return {
        "sweeps": "sweeps" in doc or any("sweeps" in f for f in fits),
        "towed": any("towed" in b for b in doc.get("boats") or []),
        "helm": "helm" in doc["hull"],
        "dipping": any("dipping" in s for s in whole),
    }


def test_the_table_of_carriers_names_committed_files_and_the_four_keys():
    stems = {p.stem for p in SHIP_FILES}
    assert set(KEY_CARRIERS) == {"sweeps", "towed", "helm", "dipping"}
    assert all(name in stems for files in KEY_CARRIERS.values() for name in files)


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_each_stage_0_key_is_carried_by_exactly_the_files_of_its_row(path):
    """Read off the file itself, and again as loaded: a file outside a key's row is as stage 0
    left it, and a file in it carries the key and is read so."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    carried = _carried(doc)
    for key, files in KEY_CARRIERS.items():
        assert carried[key] == (path.stem in files), (key, path.stem)
    ship = load_ship(path)
    dipping = [s.id for s in ship.sails.values() if _whole(s) and s.dipping]  # stage 0L
    assert bool(dipping) == (path.stem in KEY_CARRIERS["dipping"])
    assert (ship.spec.sweeps is not None) == ("sweeps" in doc)
    assert ship.spec.hull.helm == doc["hull"].get("helm", "wheel")
    assert ship.spec.hull.helm == ("tiller" if path.stem in TILLER_FILES else "wheel")
    assert any(b.towed for b in ship.spec.boats) == (path.stem in KEY_CARRIERS["towed"])
    if ship.spec.armament is not None and path.stem not in KEY_CARRIERS["sweeps"]:
        assert all(f.sweeps is None for f in ship.spec.armament.fits.values())


# -- each new key: what it takes, its refusals and its pickle (items 3 to 5, 10) --------------


@cache
def _read(name: str) -> dict:
    return yaml.safe_load((ROOT / "data" / "ships" / f"{name}.yaml").read_text(encoding="utf-8"))


def _doc(name: str = "brig", **top) -> dict:
    """A committed file's document, a fresh copy, with the top-level keys given set."""
    doc = copy.deepcopy(_read(name))
    doc.update(top)
    return doc


def _with(doc: dict, path: tuple, value) -> dict:
    """The document with the key at `path` (keys and list indices) set to `value`."""
    at = doc
    for key in path[:-1]:
        at = at[key]
    at[path[-1]] = value
    return doc


def test_the_keys_are_known_where_they_belong():
    assert SWEEPS_KEYS == ("number", "men_each", "thrust_n", "power_w", "tiring_h")
    assert "towed" in BOAT_KEYS and HELM_KINDS == ("wheel", "tiller")
    assert "sweeps" in FIT_KEYS and FIT_KEYS[-2:] == FIT_OWN_BILL  # the bill's own keys last


def test_sweeps_load_onto_the_ship_and_a_fit_ships_them():
    doc = _doc(sweeps=dict(SWEEPS))
    first = next(iter(doc["armament"]["fits"]))
    _with(doc, ("armament", "fits", first, "sweeps"), 16)
    spec = spec_from_dict(doc, "sweeps.yaml")
    assert spec.sweeps == SweepsSpec(16, 3, 50.0, 60.0, 3.0)
    fits = spec.armament.fits
    assert fits[first].sweeps == 16
    assert all(f.sweeps is None for name, f in fits.items() if name != first)


def _first_fit(doc: dict) -> str:
    return next(iter(doc["armament"]["fits"]))


@pytest.mark.parametrize(
    "change, message",
    [
        (lambda d: d.update(sweeps=16), "'sweeps' is not a mapping."),
        (
            lambda d: d.update(sweeps={**SWEEPS, "oars_each": 1}),
            "the sweeps have 'oars_each', which they do not take; the keys are number, "
            "men_each, thrust_n, power_w, tiring_h.",
        ),
        (
            lambda d: d.update(sweeps={k: v for k, v in SWEEPS.items() if k != "number"}),
            "the number of sweeps is None; it must be a whole number, not negative.",
        ),
        (
            lambda d: d.update(sweeps={**SWEEPS, "men_each": 2.5}),
            "the men at each sweep is 2.5; it must be a whole number, not negative.",
        ),
        (
            lambda d: d.update(sweeps={**SWEEPS, "thrust_n": "fifty"}),
            "the sweeps has 'thrust_n' = 'fifty', which is not a number.",
        ),
        (
            lambda d: d.update(sweeps={**SWEEPS, "number": 0}),
            "the sweeps want a number, the men at each, a thrust, a power and hours over nought.",
        ),
        (
            lambda d: d.update(sweeps={**SWEEPS, "men_each": 0}),
            "the sweeps want a number, the men at each, a thrust, a power and hours over nought.",
        ),
        (
            lambda d: d.update(sweeps={**SWEEPS, "tiring_h": 0}),
            "the sweeps want a number, the men at each, a thrust, a power and hours over nought.",
        ),
        (
            lambda d: d["armament"]["fits"][_first_fit(d)].update(sweeps=16),
            "ships 16 sweeps, and the file gives no 'sweeps' section for them; give her sweeps, "
            "or leave the fit without.",
        ),
    ],
    ids=[
        "not a mapping",
        "an unknown key",
        "no number",
        "men not whole",
        "a thrust not a number",
        "no sweeps",
        "no men",
        "no hours",
        "a fit with no section",
    ],
)
def test_sweeps_are_refused_in_words_where_they_are_wrong(change, message):
    doc = _doc()
    change(doc)
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(doc, "bad.yaml")
    assert message in str(e.value) and str(e.value).startswith("bad.yaml:")


@pytest.mark.parametrize("given", [0, -2, "16", True, 2.0])
def test_a_fits_sweeps_are_a_whole_number_of_one_or_more(given):
    doc = _doc(sweeps=dict(SWEEPS))
    first = _first_fit(doc)
    _with(doc, ("armament", "fits", first, "sweeps"), given)
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(doc, "bad.yaml")
    assert f"the fit '{first}' ships {given!r} sweeps; say the number of sweeps she ships" in str(
        e.value
    )


def test_sweeps_are_refused_on_a_hull_with_oars_and_on_a_boats_rig():
    """The boats pull oars, and a file with `oars:` is a boat to the game
    (`world.boats.is_boat`); a boat's rig with no oars is refused for its rig."""
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(_doc("boat-yawl-16", sweeps=dict(SWEEPS)), "bad.yaml")
    assert "gives both 'sweeps' and 'oars'; a hull with oars is a boat" in str(e.value)
    oarless = _doc("boat-yawl-16", sweeps=dict(SWEEPS))
    del oarless["oars"]
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(oarless, "bad.yaml")
    assert "a boat's file gives 'sweeps'; a boat pulls oars" in str(e.value)
    oars = _doc(oars={"number": 20, "thrust_n": 50, "power_w": 60, "tiring_h": 4.0})
    oars["sweeps"] = dict(SWEEPS)
    with pytest.raises(ShipFileError, match="gives both 'sweeps' and 'oars'"):
        spec_from_dict(oars, "bad.yaml")


def test_a_boat_may_be_towed_and_is_on_deck_by_default():
    doc = _doc()
    _with(doc, ("boats", 0, "towed"), True)
    boats = spec_from_dict(doc, "towed.yaml").boats
    assert boats[0].towed is True and not any(b.towed for b in boats[1:])
    _with(doc, ("boats", 0, "towed"), False)
    assert spec_from_dict(doc, "towed.yaml").boats[0].towed is False
    _with(doc, ("boats", 0, "towed"), None)  # null is the key left out, as `helm` and `sweeps`
    assert spec_from_dict(doc, "towed.yaml").boats[0].towed is False


@pytest.mark.parametrize("given", ["yes", 1, 0.0])
def test_a_boats_towed_is_true_or_false(given):
    doc = _doc()
    _with(doc, ("boats", 0, "towed"), given)
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(doc, "bad.yaml")
    want = f"boat '{doc['boats'][0]['id']}' has towed = {given!r}; say true (towed astern) or"
    assert want in str(e.value)


@pytest.mark.parametrize("given, helm", [("tiller", "tiller"), ("wheel", "wheel"), (None, "wheel")])
def test_the_hulls_helm_is_a_wheel_or_a_tiller_the_wheel_unless_said(given, helm):
    doc = _doc()
    _with(doc, ("hull", "helm"), given)
    assert spec_from_dict(doc, "helm.yaml").hull.helm == helm


@pytest.mark.parametrize("given", ["rudder", "Tiller", 1, True, ["tiller"]])
def test_the_hulls_helm_is_refused_in_words_when_it_is_neither(given):
    doc = _doc()
    _with(doc, ("hull", "helm"), given)
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(doc, "bad.yaml")
    assert f"the hull's helm is {given!r}; she steers by a wheel or a tiller." in str(e.value)


def test_each_spec_is_pickled_as_before_while_its_key_holds_its_default():
    """The checkpoint (the owner's rule for stage 0): a ship spec without sweeps, a hull that
    steers by the wheel, a boat on deck and a fit with no sweeps leave the key out of their
    pickled state, and read the class's default back; a key given is kept."""
    spec = spec_from_dict(_doc(), "brig.yaml")
    plain = [(spec, "sweeps"), (spec.hull, "helm")]
    plain += [(b, "towed") for b in spec.boats] + [
        (f, "sweeps") for f in spec.armament.fits.values()
    ]
    for obj, key in plain:
        default = getattr(obj, key)
        assert key not in obj.__getstate__(), (type(obj).__name__, key)
        again = pickle.loads(pickle.dumps(obj))
        assert key not in again.__dict__ and getattr(again, key) == default and again == obj
    doc = _doc(sweeps=dict(SWEEPS))
    _with(doc, ("hull", "helm"), "tiller")
    _with(doc, ("boats", 0, "towed"), True)
    _with(doc, ("armament", "fits", _first_fit(doc), "sweeps"), 16)
    given = spec_from_dict(doc, "given.yaml")
    again = pickle.loads(pickle.dumps(given))
    assert again.sweeps == SweepsSpec(16, 3, 50.0, 60.0, 3.0) and again.hull.helm == "tiller"
    assert again.boats[0].towed is True and again.armament.fits[_first_fit(doc)].sweeps == 16
    assert again == given


# -- the generator's modules and units (items 1 and 2) ----------------------------------------


def _module(path: Path):
    spec = importlib.util.spec_from_file_location(f"probes_90_{path.stem}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The modules a builder has filled since stage 0, each writing its own file
# (tests/test_profile.py's `MODULE_FILES` holds what it writes): the Diana's (package 90, her
# builder) and the Concepción's (package 90, her builder). Old: none, the five stubs; then the
# Diana's alone.
FILLED = ("diana", "concepcion")


def test_the_five_modules_follow_the_four_and_each_stub_writes_nothing(tmp_path):
    """Stage 0 (Plan-Package90.md §5.1 item 1): the five modules named after package 75's four,
    each a docstring and a `build` writing nothing until its builder fills it; a filled one
    (`FILLED`) is held by tests/test_profile.py's hook test. Old: all five stubs; the Diana's
    filled since her builder's file, and the Concepción's since hers."""
    gen = _module(ROOT / "tools" / "gen_ships.py")
    assert gen.SHIP_MODULES == (
        "indefatigable",
        "neufchatel",
        "bilander",
        "bellerophon",
        *NEW_MODULES,
    )
    assert set(FILLED) <= set(NEW_MODULES)
    for name in (n for n in NEW_MODULES if n not in FILLED):
        path = ROOT / "tools" / "ships" / f"{name}.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert ast.get_docstring(tree), name
        assert [type(n).__name__ for n in tree.body] == ["Expr", "FunctionDef"], name
        out = tmp_path / name
        out.mkdir()
        _module(path).build(str(out))
        assert list(out.iterdir()) == [], name


def test_the_lateens_cut_is_a_docstring_alone_until_the_tartanes_builder_fills_it():
    tree = ast.parse((ROOT / "tools" / "ships" / "lateen.py").read_text(encoding="utf-8"))
    assert [type(n).__name__ for n in tree.body] == ["Expr"]
    assert "whole lateen's cut" in ast.get_docstring(tree)


def test_period_gives_the_pie_de_burgos_and_the_pied_du_roi():
    period = _module(ROOT / "tools" / "ships" / "period.py")
    assert period.PIE_DE_BURGOS_M == 0.278635  # Winfield et al. 2023, pp. 41-46
    assert round(period.PIE_DE_BURGOS_M, 4) == 0.2786  # the tree's value since package 39d
    assert period.PIED_DU_ROI_M == 0.3248


# -- the ranks (item 6) -----------------------------------------------------------------------

# Every description's rank, measured at stage 0's head before package 90's words: each the same
# by every reading (her key in `SIZE_RANK` and by `size_rank_of`, her rig's and her made-out
# words by `size_of_words` and `size_rank_of`, her file by `size_of_file`).
RANKS_BEFORE = {
    "frigate": 3,
    "schooner": 1,
    "privateer schooner": 1,
    "cutter": 1,
    "revenue cutter": 1,
    "hired armed cutter": 1,
    "coasting cutter": 1,
    "brig-sloop": 2,
    "merchant brig": 2,
    "lugger": 1,
    "privateer lugger": 1,
    "smack": 0,
    "sixty-four": 4,
    "razee": 3,
    "hermaphrodite brig": 2,
    "bilander": 1,
    "seventy-four": 4,
}


def _readings(key: str) -> list:
    d = S.description(key)
    return [
        captains.SIZE_RANK.get(key),
        captains.size_rank_of(key),
        captains.size_of_words(d["rig"]),
        captains.size_of_words(d["what"]),
        captains.size_rank_of(d["rig"]),
        captains.size_rank_of(d["what"]),
        captains.size_of_file(d["file"]),
    ]


def _words_of_before() -> list[str]:
    """Every description's own words before package 90: her key, her rig's and her made-out
    words, and the scenario's words that name her (`ships._DESCRIPTION_WORDS`)."""
    words = []
    for key in RANKS_BEFORE:
        d = S.description(key)
        words += [key, d["rig"], d["what"]]
    words += [w for w, key in S._DESCRIPTION_WORDS.items() if key in RANKS_BEFORE]
    return words


def test_every_description_ranks_as_measured_before_the_new_words():
    assert set(RANKS_BEFORE) <= set(S.DESCRIPTIONS)
    for key, rank in RANKS_BEFORE.items():
        assert _readings(key) == [rank] * 7, key


def test_every_descriptions_words_rank_as_they_do_without_package_90s_words(monkeypatch):
    """The word table with package 90's words taken out is the table as it was: every word of
    every description ranks the same by it as by the table as it is."""
    words = _words_of_before()
    now = [(captains.size_of_words(w), captains.size_rank_of(w)) for w in words]
    before = tuple((w, r) for w, r in captains._SIZE_WORDS if w not in PACKAGE_90_WORDS)
    assert len(before) == len(captains._SIZE_WORDS) - len(PACKAGE_90_WORDS)
    monkeypatch.setattr(captains, "_SIZE_WORDS", before)
    assert [(captains.size_of_words(w), captains.size_rank_of(w)) for w in words] == now


def test_package_90s_words_rank_her_each_before_any_row_that_matches_inside_her_words():
    """The tartane the cutter's class, the polacre, the xebec and the corvette a brig's, and the
    three-decker (the owner's question 8) a class above the line, which every reader compares
    and none indexes by."""
    rank = captains.SIZE_RANK
    assert {k: rank[k] for k in ("tartane", "polacre", "xebec", "corvette", "three-decker")} == {
        "tartane": 1,
        "polacre": 2,
        "xebec": 2,
        "corvette": 2,
        "three-decker": 5,
    }
    assert rank["three-decker"] > captains.LINE_OF_BATTLE_RANK
    words = dict(captains._SIZE_WORDS)
    assert [words[w] for w in PACKAGE_90_WORDS] == [5, 5, 2, 2, 2, 2, 2, 1]
    order = [w for w, _ in captains._SIZE_WORDS]
    for word in PACKAGE_90_WORDS:
        assert order.index(word) < order.index("a ship") < order.index("brig"), word
    for word in ("three-decker", "first rate"):
        assert order.index(word) < order.index("ship of the line"), word
    assert captains.size_rank_of("a three-decker, a ship of the line of three tiers") == 5
    assert captains.size_rank_of("a first rate, a ship of the line") == 5
    assert captains.size_rank_of("a ship-sloop") == captains.size_rank_of("a ship sloop") == 2
    assert captains.size_rank_of("a polacre-ship") == captains.size_rank_of("a polacre brig") == 2
    assert captains.size_of_words("a xebec of war, nine ports a side") == 2
    assert captains.size_of_words("a corvette, flush-decked, eleven ports a side") == 2
    assert captains.size_rank_of("a tartane") == 1


# -- the men of war and the hail (item 7) -----------------------------------------------------


def test_the_men_of_war_and_the_hail_take_the_corvette_the_three_decker_and_the_xebec(
    monkeypatch,
):
    new = ("corvette", "three-decker", "xebec")
    assert set(new) < regimes._MAN_OF_WAR_DESCRIPTIONS
    assert set(new) < squadrons._MAN_OF_WAR_DESCRIPTIONS
    body = SimpleNamespace(brain=None, description="")
    monkeypatch.setattr(squadrons, "_body", lambda world, vid: body)
    me = SimpleNamespace(commander="c")
    for key in new:
        body.description = key
        assert squadrons.Squadron._is_escort(me, None, "x"), key
        assert brains.role_of_vessel(SimpleNamespace(description=key, role=""), None) == (
            "kings-ship"
        ), key
        assert signals._names_a_sail(None, f"the {key}"), key
        assert signals._names_a_sail(None, f"a {key}", by_rig=True), key


# -- stage 0L: the whole lateen's interfaces, laid inert (the plan's §5.2) -------------------

# The probes with a whole lateen (class lateen, not cut at the mast); the three-decker's mizen
# course, the 74's, is a lateen cut at the mast and keeps its refusal (below).
WHOLE_LATEEN_PROBES = {
    "tartane": (tartane_probe_doc, ["main.lateen", "mizzen.lateen"]),
    "polacre": (polacre_probe_doc, ["fore.lateen", "mizzen.lateen"]),
    "xebec": (xebec_probe_doc, ["fore.lateen", "mizzen.lateen", "main.lateen"]),
}


def _whole(sail) -> bool:
    """A whole lateen, on a sail or its spec: class lateen and not cut at the mast."""
    return sail.cls == "lateen" and not sail.cut_at_mast


def _dipping(doc: dict) -> dict:
    """The document with `dipping: true` on each of its whole lateens."""
    for s in doc["sails"]:
        if s["class"] == "lateen" and not s.get("cut_at_mast"):
            s["dipping"] = True
    return doc


@pytest.mark.parametrize("name", list(WHOLE_LATEEN_PROBES))
def test_each_probe_with_a_whole_lateen_loads_with_dipping_and_classes_as_without_it(name):
    """Given the key on every whole lateen, the probe loads with no warning, and it changes
    nothing of her but the key itself: her classing through the golden table's gates is the
    probe's as measured at stage 0, and her sails, spars, lines and groups are as without it,
    each lateen's side not yet found (None), so that it draws as it did."""
    build, whole = WHOLE_LATEEN_PROBES[name]
    plain = ship_from_dict(build(), f"tests/rig_fixtures.py:{name}")
    keyed = ship_from_dict(_dipping(build()), f"tests/rig_fixtures.py:{name}")
    assert keyed.spec.warnings == []
    assert [s.id for s in keyed.spec.sails if _whole(s)] == whole
    assert [s.id for s in keyed.spec.sails if s.dipping] == whole
    assert [s.id for s in keyed.sails.values() if s.dipping] == whole
    assert not any(s.dipping for s in plain.spec.sails if _whole(s))
    unkeyed = [dataclasses.replace(s, dipping=False) for s in keyed.spec.sails]
    assert unkeyed == plain.spec.sails
    assert keyed.spec.spars == plain.spec.spars and keyed.spec.lines == plain.spec.lines
    assert keyed.groups == plain.groups and keyed.aliases == plain.aliases
    for sid in whole:
        sail = keyed.sails[sid]
        assert type(sail) is Sail and sail.lug_side is None, sid
        assert not against_the_mast(sail, 1.0) and not against_the_mast(sail, -1.0), sid
    assert _classing(keyed) == _classing(plain) == CLASSING[name][1]


# Every refusal that touches `dipping`, word for word as stage 0's head (94ea1dba) gave it, run
# before the narrowing: a lateen cut at the mast keeps the sentence every class but the lug is
# refused in, and so does one whose `cut_at_mast` is said otherwise than true or false (the
# dipping refused first, as before); a lug's own refusals stand.
def _committed(name: str, sid: str, **keys) -> dict:
    """A committed file's document with `keys` set on the sail `sid`, a key given None taken
    out of it."""
    doc = _doc(name)
    sail = next(s for s in doc["sails"] if s["id"] == sid)
    for key, value in keys.items():
        if value is None:
            sail.pop(key, None)
        else:
            sail[key] = value
    return doc


def _keyed(doc: dict, sid: str, **keys) -> dict:
    next(s for s in doc["sails"] if s["id"] == sid).update(keys)
    return doc


ONLY_A_LUG = "bad.yaml: sail '{}' is a {} sail; only a lug is dipped."
REFUSED_AS_BEFORE = [
    (
        "a lateen cut at the mast",
        lambda: _committed("seventy-four", "mizzen.course", dipping=True),
        ONLY_A_LUG.format("mizzen.course", "lateen"),
    ),
    (
        "a lateen cut at the mast said 1",
        lambda: _committed("seventy-four", "mizzen.course", dipping=True, cut_at_mast=1),
        ONLY_A_LUG.format("mizzen.course", "lateen"),
    ),
    (
        "a whole lateen whose cut_at_mast is said null",  # an older key: a null refused, as before
        lambda: _keyed(tartane_probe_doc(), "main.lateen", dipping=True, cut_at_mast=None),
        ONLY_A_LUG.format("main.lateen", "lateen"),
    ),
    (
        "a whole lateen said to be cut at the mast",
        lambda: _keyed(tartane_probe_doc(), "main.lateen", dipping=True, cut_at_mast=True),
        ONLY_A_LUG.format("main.lateen", "lateen"),
    ),
    (
        "a square sail",
        lambda: _committed("brig", "fore.course", dipping=True),
        ONLY_A_LUG.format("fore.course", "square"),
    ),
    (
        "a gaff sail",
        lambda: _committed("brig", "main.spanker", dipping=True),
        ONLY_A_LUG.format("main.spanker", "gaff"),
    ),
    (
        "a jib-headed sail",
        lambda: _committed("brig", "jib", dipping=True),
        ONLY_A_LUG.format("jib", "jibheaded"),
    ),
    (
        "a studding sail",
        lambda: _committed("brig", "fore.lower.studdingsail.starboard", dipping=True),
        ONLY_A_LUG.format("fore.lower.studdingsail.starboard", "studding"),
    ),
    (
        "a sprit sail",
        lambda: _committed("brig", "fore.course", dipping=True, **{"class": "sprit"}),
        ONLY_A_LUG.format("fore.course", "sprit"),
    ),
    (
        "a dipping lug's key not a bool",
        lambda: _committed("lugger", "fore.lug", dipping="yes"),
        "bad.yaml: sail 'fore.lug' has dipping = 'yes'; say true or false.",
    ),
    (
        "a standing lug's key not a bool",
        lambda: _committed("lugger", "mizen.lug", dipping=1),
        "bad.yaml: sail 'mizen.lug' has dipping = 1; say true or false.",
    ),
    (
        "a lug cut at the mast",
        lambda: _committed("lugger", "fore.lug", cut_at_mast=True),
        "bad.yaml: sail 'fore.lug' is a lug sail; only a lateen is cut at the mast.",
    ),
    (
        "a settee not dipping",
        lambda: _keyed(brig_with_settee_doc(), "main.settee", dipping=False),
        "bad.yaml: sail 'main.settee' is a settee and is not dipping; a settee is a dipping lug "
        "(say dipping: true).",
    ),
    (
        "a whole lateen's key not a bool",
        lambda: _keyed(tartane_probe_doc(), "main.lateen", dipping="yes"),
        "bad.yaml: sail 'main.lateen' has dipping = 'yes'; say true or false.",
    ),
]


@pytest.mark.parametrize(
    "build, message",
    [case[1:] for case in REFUSED_AS_BEFORE],
    ids=[case[0] for case in REFUSED_AS_BEFORE],
)
def test_the_refusals_for_a_lateen_cut_at_the_mast_and_for_a_lug_are_unchanged(build, message):
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(build(), "bad.yaml")
    assert str(e.value) == message


@pytest.mark.parametrize(
    "keys, message",
    [
        ({"settee": True}, "is a lateen sail; only a lug is a settee."),
        (
            {"sheeted_to": "mizzen.lateen"},
            "is a lateen sail; only a lug topsail is sheeted to another sail.",
        ),
    ],
    ids=["a settee", "sheeted to another sail"],
)
def test_a_dipping_whole_lateen_is_no_lug_its_keys_refused_as_without_dipping(keys, message):
    """A lug's own keys on a whole lateen are refused in the words a lateen without `dipping`
    is refused in (at stage 0's head the dipping's sentence came first)."""
    for dipping in (False, True):
        doc = _keyed(tartane_probe_doc(), "main.lateen", **keys)
        if dipping:
            _keyed(doc, "main.lateen", dipping=True)
        with pytest.raises(ShipFileError) as e:
            spec_from_dict(doc, "bad.yaml")
        assert str(e.value) == f"bad.yaml: sail 'main.lateen' {message}", dipping


def test_a_dipping_whole_lateen_keeps_its_side_as_a_dipping_lug_does_by_the_plain_default():
    """`Sail.lug_side` is the plain class default, a field of `Sail` and no class of its own;
    on a dipping whole lateen it starts unfound, is kept once given, and is pickled with the
    sail as a lug's is. The key adds nothing to the sail's pickled state but itself."""
    assert {f.name: f.default for f in dataclasses.fields(Sail)}["lug_side"] is None
    keyed = ship_from_dict(_dipping(tartane_probe_doc()), "tests/rig_fixtures.py:tartane")
    plain = ship_from_dict(tartane_probe_doc(), "tests/rig_fixtures.py:tartane")
    sail = keyed.sails["main.lateen"]
    state, before = sail.__getstate__(), plain.sails["main.lateen"].__getstate__()
    assert set(state) == set(before)
    assert {k for k in state if state[k] != before[k]} == {"dipping"}
    sail.lug_side = "larboard"
    again = pickle.loads(pickle.dumps(sail))
    assert type(again) is Sail and again.dipping and again.lug_side == "larboard"
    lug = load_ship(ROOT / "data" / "ships" / "lugger.yaml").sails["fore.lug"]
    assert type(lug) is type(sail) and lug.dipping and lug.lug_side is None


def test_the_ships_lateen_practice_is_read_with_its_default():
    """`ship.extra["lateen_practice"]`, in stays and in wearing, "shift" in both by default (the
    owner's "preferred"); a kept occasion is read over its default, and the reading is a fresh
    dict, so that changing it changes nothing kept."""
    assert scripts.LATEEN_PRACTICE == "lateen_practice"
    ship = ship_from_dict(_dipping(xebec_probe_doc()), "tests/rig_fixtures.py:xebec")
    assert scripts.LATEEN_PRACTICE not in ship.extra
    assert scripts.lateen_practice(ship) == {"stays": "shift", "wearing": "shift"}
    ship.extra[scripts.LATEEN_PRACTICE] = {"stays": "leave"}
    got = scripts.lateen_practice(ship)
    assert got == {"stays": "leave", "wearing": "shift"}
    got["wearing"] = "leave"
    assert ship.extra[scripts.LATEEN_PRACTICE] == {"stays": "leave"}
    assert scripts.lateen_practice(ship) == {"stays": "leave", "wearing": "shift"}


def test_no_world_gives_a_ship_a_lateen_practice(tmp_path):
    """Set by nothing: neither the xebec probe with the key, nor the lugger as filed, is given
    a practice by her world's making or two minutes of its sailing."""
    path = write_ship(_dipping(xebec_probe_doc()), tmp_path, "xebec")
    for ship_path in (path, ROOT / "data" / "ships" / "lugger.yaml"):
        world = make_world(7, ship_path, Scenario())
        world.run(120)
        assert scripts.LATEEN_PRACTICE not in world.ship.extra, ship_path.name
        assert scripts.lateen_practice(world.ship) == {"stays": "shift", "wearing": "shift"}


# -- the Spanish list's nation and Spain's kit (the lead's follow-ups of nudge 25) ---------------


def test_every_names_list_has_its_nation():
    """The cause of the follow-up, held at its level: every list of `data/crew/names.yaml` has
    its nation in `NAMES_TO_NATION`, so that no list reads as Britain's by the table's floor
    alone, and every nation the table names is a nation of `data/nations.yaml`."""
    from freesail.world.nations import NAMES_TO_NATION, load_nations

    lists = yaml.safe_load((ROOT / "data" / "crew" / "names.yaml").read_text(encoding="utf-8"))
    assert set(NAMES_TO_NATION) == {k for k, v in lists.items() if isinstance(v, dict)}
    nations = load_nations()
    assert all(nation in nations.nations for nation in NAMES_TO_NATION.values())


def test_truth_7_680_a_ship_drawn_from_the_spanish_list_with_no_nation_given_is_spains(tmp_path):
    """Package 90 (the lead's nudge 25): a ship whose company is drawn from the Spanish list,
    her scenario giving no nation, reads as Spain's: her nation by her list, her marines Spain's
    kit, and her people Spanish names. Before the list had its row she read as Britain's, with
    the Royal Marines' kit."""
    from freesail.combat import small_arms

    names = yaml.safe_load((ROOT / "data" / "crew" / "names.yaml").read_text(encoding="utf-8"))
    doc = _doc("frigate-36")
    doc["crew"]["names"] = "spanish"
    world = make_world(7, write_ship(doc, tmp_path, "frigate-36-spanish"), Scenario())
    assert world.scenario.nation is None
    assert world.dealings.ship_nation == "spain"
    marines = small_arms.describe(world, world.ship)
    assert marines["kit"] == "spanish"
    assert "(the Spanish navy's infantry and artillery; " in marines["words"]
    for sailor in world.ship.extra["crew"].sailors:
        given, surname = sailor.name.split(" ", 1)
        assert given in names["spanish"]["given"] and surname in names["spanish"]["surnames"]
