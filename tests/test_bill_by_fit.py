"""Package 75, Phase 5: the quarter bill by fit, the lead's ruling 13 of 2026-11-14 (the razee's
trimmers by fit), beside B1's marines by fit (the lead's ruling (4) of 2026-11-13).

A ship file bears one quarter bill, set against her default fit; a fit whose guns want other men
gives its own figure for a key of the bill (`schema.FIT_OWN_BILL`: the marines kept in their
division, and now the trimmers told off by station), which the beat reads in place of the bill's
when she carries it (`crew.quarters._on_her_fit`, one road for every such key). The razee's 'as
razeed 1795' tells off 51 trimmers (9, 12, 14, 7 and 9), the bill's rule on its guns (her 238
seamen less the 185 at one side's guns and the 2 at the wheel), JUDGEMENT in the fit's note, so
that every crew of that fit is manned; the bill's 79 are the 1796 fit's. No other fit of any file
gives its own trimmers, and a fit without them, or one pickled before them, keeps the bill's.
"""

from __future__ import annotations

import copy
import pickle
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail.ship.loader import load_ship, spec_from_dict
from freesail.ship.schema import FIT_KEYS, ShipFileError

ROOT = Path(__file__).resolve().parents[1]
SIXTY_FOUR = ROOT / "data" / "ships" / "sixty-four.yaml"
RAZEE = ROOT / "data" / "ships" / "razee-44.yaml"
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
# the fits that tell off their own trimmers (the lead's ruling 13), by file
FIT_TRIMMERS = {
    "razee-44.yaml": {
        "as razeed 1795": {
            "forecastle": 9,
            "fore_top": 12,
            "main_top": 14,
            "mizzen_top": 7,
            "afterguard": 9,
        }
    },
}
# A real checkpoint of the razee on 'as razeed 1795' at muster, ten ticks in at seed 7
# (`tests.test_brains.world_at`), written by the commit before the trimmers by fit (53c14457):
# her fit pickled with no trimmers. A kept save (`tests/test_checkpoint.py`): a change that
# breaks it is mended with a class default or a step in `core.replay._rebind`, never by
# changing it.
PRE_RULING_13 = (
    ROOT / "tests" / "fixtures" / "saves" / "pre-ruling-13-razee-as-razeed-1795.checkpoint"
)
# The files whose bill keeps marines in their division (the 74's, the 64's and the razee's: the
# bill by deck, B7.b), and every fit of each: the ships whose bill is read on her fit
BILL_BY_DECK = [
    (p, name)
    for p in SHIP_FILES
    for s in [load_ship(p).spec]
    if s.crew is not None
    and s.crew.quarter_bill is not None
    and s.crew.quarter_bill.marines is not None
    and s.armament is not None
    for name in s.armament.fits
]


def _doc() -> dict:
    with open(SIXTY_FOUR, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _beat(path: Path, fit: str):
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, str(path), fit=fit)
    assert w.ship.fit == fit
    w.run(10)
    said = w.submit("beat to quarters")
    w.run(30)
    return w, said, quarters_of(w.ship)


def _by_station(sailors) -> dict[str, int]:
    out: dict[str, int] = {}
    for s in sailors:
        out[s.station.value] = out.get(s.station.value, 0) + 1
    return out


def test_a_fit_may_give_its_own_marines_and_trimmers_and_no_other_key_of_the_bill():
    from freesail.ship.schema import FIT_OWN_BILL

    assert FIT_OWN_BILL == ("marines", "trimmers")
    assert FIT_KEYS[-2:] == FIT_OWN_BILL


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_a_fit_gives_its_own_trimmers_only_where_ruled_and_pickles_as_before_without(path):
    """The razee's 'as razeed 1795' alone tells off its own trimmers; every other fit of every
    file gives none, and its pickled state holds no `trimmers`; a fit with them pickles them and
    reads them back."""
    arm = load_ship(path).spec.armament
    if arm is None:
        return
    given = FIT_TRIMMERS.get(path.name, {})
    for name, fit in arm.fits.items():
        assert getattr(fit, "trimmers", None) == given.get(name), name
        assert ("trimmers" in fit.__getstate__()) is (name in given), name
        if name in given:
            assert list(fit.__getstate__())[-2:] == ["marines", "trimmers"], name
        again = pickle.loads(pickle.dumps(fit))
        assert again == fit and getattr(again, "trimmers", None) == given.get(name)
        if name not in given:
            assert "trimmers" not in again.__dict__


def test_the_razees_1795_trimmers_are_the_bills_rule_on_its_guns():
    """The arithmetic, from the file: her seamen less the seamen at one side's guns of the fit
    (the chasers included, the marines taking the carronades first) and the wheel, split as the
    bill's are; the bill's own the same rule on the default fit's guns."""
    spec = load_ship(RAZEE).spec
    st = spec.crew.stations
    seamen = sum(st[k] for k in ("forecastle", "fore_top", "main_top", "mizzen_top"))
    seamen += st["afterguard"] + st["waisters"]
    bill = spec.crew.quarter_bill

    def told_off(fit) -> int:
        one_side = [g for g in fit.guns if g.place != "broadside" or g.side == "starboard"]
        men = sum(g.crew for g in one_side)
        marines = min(sum(g.crew for g in one_side if g.kind == "carronade"), st["marines"])
        return seamen - (men - marines) - bill.helm

    fit = spec.armament.fits["as razeed 1795"]
    assert (seamen, told_off(fit), sum(fit.trimmers.values())) == (238, 51, 51)
    default = spec.armament.fits[spec.armament.default]
    assert (told_off(default), sum(bill.trimmers.values())) == (79, 79)
    # split by the bill's shares, station by station no more than the bill's
    assert list(fit.trimmers) == list(bill.trimmers)
    assert all(fit.trimmers[k] <= bill.trimmers[k] for k in bill.trimmers)


@pytest.mark.parametrize("path, fit", BILL_BY_DECK, ids=[f"{p.stem}-{f}" for p, f in BILL_BY_DECK])
def test_every_fit_of_a_ship_whose_bill_keeps_marines_mans_every_crew_at_the_beat(path, fit):
    """The cause's level (the lead's ruling 13): a bill set against her default fit and read on
    another whose guns want more seamen left the razee's 1795 fit three crews short (Nos. 12 and
    13 unmanned, No. 17 1 of 7). On every fit of every ship whose bill keeps marines in their
    division (the 74's three, the 64's two and the razee's two, read from the files), the beat
    at muster mans every gun crew, tells off at least the trimmers the bill gives on her fit,
    station by station, and says no gun unmanned."""
    from freesail.crew.quarters import TRIMMERS

    w, said, q = _beat(path, fit)
    short = {k: (len(gc.members), gc.wanted) for k, gc in q.crews.items()}
    short = {k: v for k, v in short.items() if v[0] != v[1]}
    assert short == {}, short
    assert "Not hands enough" not in said.text
    told = _by_station(q.divisions[TRIMMERS])
    own = getattr(w.ship.fit_spec, "trimmers", None)
    for station, n in (own if own is not None else q.ship.spec.crew.quarter_bill.trimmers).items():
        assert told.get(station, 0) >= n, station


def test_the_bill_on_her_fit_is_one_road_for_every_key_a_fit_may_give():
    """`_on_her_fit`: for each key a fit may give, the fit's own where it gives one, else the
    bill's; a ship with no fit, or a fit pickled before the key (no attribute), the bill's."""
    from freesail.crew.quarters import _marines_kept, _on_her_fit
    from freesail.ship.schema import FIT_OWN_BILL

    bill = SimpleNamespace(marines=14, trimmers={"forecastle": 14})
    own = {"marines": 38, "trimmers": {"forecastle": 9}}
    for key in FIT_OWN_BILL:
        crew = SimpleNamespace(quarter_bill=bill)
        given = SimpleNamespace(
            fit_spec=SimpleNamespace(**{key: own[key]}), spec=SimpleNamespace(crew=crew)
        )
        assert _on_her_fit(given, key) == own[key]
        none = SimpleNamespace(
            fit_spec=SimpleNamespace(**{key: None}), spec=SimpleNamespace(crew=crew)
        )
        assert _on_her_fit(none, key) == getattr(bill, key)
        before = SimpleNamespace(fit_spec=SimpleNamespace(), spec=SimpleNamespace(crew=crew))
        assert _on_her_fit(before, key) == getattr(bill, key)
        unarmed = SimpleNamespace(fit_spec=None, spec=SimpleNamespace(crew=crew))
        assert _on_her_fit(unarmed, key) == getattr(bill, key)
    assert _marines_kept(SimpleNamespace(fit_spec=None, spec=SimpleNamespace(crew=None))) is None


def test_a_real_checkpoint_from_before_the_trimmers_by_fit_loads_and_beats_as_before(tmp_path):
    """A fit pickled before ruling 13 loads as before: the razee's 1795 fit read from the kept
    checkpoint has no trimmers of its own, the beat tells off the bill's 79 and leaves her three
    crews short as it did ("Not hands enough for every gun: the guns, Nos. 12 to 13 and 17 stand
    unmanned."), and written again it pickles as before. (The same fit fresh from the file mans
    all 22: the test above.) A guard: it passes before ruling 13 and after."""
    from freesail.core import replay
    from freesail.crew.quarters import MARINES, TRIMMERS, quarters_of

    header, w = replay.read_checkpoint(PRE_RULING_13)
    assert header["end_tick"] == w.clock.tick == 10
    assert w.log.digest() == header["digest"]
    assert w.ship.fit == "as razeed 1795"
    assert "trimmers" not in w.ship.fit_spec.__dict__
    assert getattr(w.ship.fit_spec, "trimmers", None) is None
    assert w.ship.fit_spec.marines == 38
    said = w.submit("beat to quarters")
    w.run(30)
    q = quarters_of(w.ship)
    assert said.text == (
        "Beat to quarters! Quarters: 19 gun crews manned, the trimmers 79, the helm 2, the powder "
        "22, the marines 38. Not hands enough for every gun: the guns, Nos. 12 to 13 and 17 stand "
        "unmanned."
    )
    assert (len(q.divisions[TRIMMERS]), len(q.divisions[MARINES])) == (79, 38)
    path = replay.write_checkpoint(w, tmp_path / "again.checkpoint")
    _, again = replay.read_checkpoint(path)
    assert "trimmers" not in again.ship.fit_spec.__dict__
    assert len(quarters_of(again.ship).divisions[TRIMMERS]) == 79


@pytest.mark.parametrize(
    "value, match",
    [
        ("sixty", r"the fit 'ardent class 1794''s 'trimmers' is not a mapping\."),
        (
            {"bosun": 3},
            r"the fit 'ardent class 1794''s trimmers name the station 'bosun', which is not one "
            r"the engine knows\. Known: forecastle, ",
        ),
        (
            {"forecastle": -1},
            r"the fit 'ardent class 1794''s trimmers of the forecastle is -1; it must be a whole "
            r"number, not negative\.",
        ),
        ({"forecastle": 2.5}, r"'s trimmers of the forecastle is 2\.5; it must be a whole number"),
        (
            {"forecastle": 55},
            r"the fit 'ardent class 1794' wants 55 trimmers of the forecastle, and the station "
            r"has 54\.",
        ),
    ],
)
def test_a_fits_trimmers_are_refused_in_words_where_they_cannot_be(value, match):
    doc = _doc()
    doc["armament"]["fits"]["ardent class 1794"]["trimmers"] = value
    with pytest.raises(ShipFileError, match=match):
        spec_from_dict(doc, "s.yaml")


def test_a_fits_trimmers_up_to_the_whole_of_a_station_are_read_in_the_bills_form():
    doc = _doc()
    for told in ({}, {"forecastle": 0}, {"main_top": 30, "forecastle": 54}):
        doc["armament"]["fits"]["ardent class 1794"]["trimmers"] = copy.deepcopy(told)
        fit = spec_from_dict(doc, "s.yaml").armament.fits["ardent class 1794"]
        assert fit.trimmers == told and list(fit.trimmers) == list(told)
        assert fit.marines == 68


@pytest.mark.parametrize(
    "value, match",
    [
        ("sixty", r"s\.yaml: the quarter bill's 'trimmers' is not a mapping\.$"),
        (
            {"bosun": 3},
            r"s\.yaml: the crew section names the station 'bosun', which is not one the engine "
            r"knows\.",
        ),
        (
            {"forecastle": -1},
            r"s\.yaml: the trimmers of the forecastle is -1; it must be a whole number, not "
            r"negative\.$",
        ),
        (
            {"forecastle": 55},
            r"s\.yaml: the quarter bill wants 55 trimmers of the forecastle, and the station has "
            r"54\.$",
        ),
    ],
)
def test_the_bills_own_trimmers_are_refused_in_the_words_they_were(value, match):
    """The bill's trimmers go by the same parse and the same check as a fit's, in their own
    words as before (the guard: passes before ruling 13 and after)."""
    doc = _doc()
    doc["crew"]["quarter_bill"]["trimmers"] = value
    with pytest.raises(ShipFileError, match=match):
        spec_from_dict(doc, "s.yaml")
