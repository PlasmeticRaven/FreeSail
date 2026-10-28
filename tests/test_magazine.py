"""The magazine by kind, with the powder below (practice and resupply, between packages 72
and 73; docs/design/Build-PracticeAndResupply.md §1.1, §1.2, §2, §8.1).

The filled cartridges are kept by the gun's kind and calibre and the loose powder in the
barrels below; the gunner fills from the one into the other (`Magazine.fill`), the ports'
issues come in by `receive`, and what she wants to be complete is `wanting`. A magazine of
packages 70 to 72, keyed by calibre, is converted once when it is first asked for. The
ship files carry the charges, the barrels, a King's fit's charges for exercise and the
bill's men filling cartridges, all written by tools/gen_ships.py.
"""

from __future__ import annotations

import copy
import pickle

import pytest
import yaml

from freesail.api.session import make_world
from freesail.combat.filling import filling_of
from freesail.ship.loader import load_ship, load_spec, spec_from_dict
from freesail.ship.parts import (
    BARREL_LB,
    Charge,
    Magazine,
    charge_lb,
    fill_seconds,
    fit_levels,
    magazine,
    split_by_kind,
)
from freesail.ship.schema import FitSpec, QuarterBillSpec, ShipFileError

PRIVATEER = "data/ships/privateer-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
LONG_12 = ("long", 12.0)
CARR_12 = ("carronade", 12.0)
SWIVEL = ("swivel", 0.5)


def _long_tom() -> tuple[object, Magazine]:
    ship = load_ship(PRIVATEER)
    return ship, magazine(ship)


# -- the charges (§2) -------------------------------------------------------------------


@pytest.mark.parametrize(
    "kind,pounder,charge,seconds",
    [
        ("long", 18, 6.0, 210),
        ("long", 12, 4.0, 180),
        ("long", 9, 3.0, 165),
        ("long", 6, 2.0, 150),
        ("long", 3, 1.0, 135),
        ("carronade", 32, 2.6875, 160),
        ("carronade", 12, 1.0, 135),
        ("swivel", 0.5, 0.25, 124),
    ],
)
def test_the_charges_and_the_filling_times_are_the_build_designs_table(
    kind, pounder, charge, seconds
):
    """A long gun a third of its shot's weight, a carronade a twelfth, a swivel a half, to
    the ounce (§2; UNVERIFIED until Table No. 29 is read); a cartridge filled in 120
    man-seconds and fifteen a pound of its charge, the table's seconds rounded."""
    assert charge_lb(kind, pounder) == charge
    assert fill_seconds(charge) == pytest.approx(seconds, abs=0.5)


# -- has and take, by kind ----------------------------------------------------------------


def test_has_and_take_go_by_the_guns_kind_and_the_long_toms_carronades_leave_the_pivots():
    """The long Tom's carronades emptied (blank charges, so that the shot stays) leave the
    pivot's 55 of the same calibre; double wants two round, blank none, as before."""
    _, mag = _long_tom()
    assert mag.layout == 2 and not mag.short
    for _ in range(220):
        mag.take("carronade", 12, Charge.BLANK)
    assert mag.filled_of("carronade", 12) == 0 and mag.short
    assert not mag.has("carronade", 12, Charge.ROUND)
    assert mag.filled_of("long", 12) == 55 and mag.has("long", 12, Charge.ROUND)
    assert mag.fired[CARR_12] == 220 and mag.shot[12.0]["round"] == 200
    with pytest.raises(ValueError):
        mag.take("carronade", 12, Charge.ROUND)
    mag.take("long", 12, Charge.ROUND)
    assert mag.filled_of("long", 12) == 54 and mag.shot[12.0]["round"] == 199
    assert mag.fired[LONG_12] == 1
    mag.shot[12.0]["round"] = 1
    assert not mag.has("long", 12, Charge.DOUBLE) and mag.has("long", 12, Charge.ROUND)
    mag.shot[12.0]["round"] = 0
    assert not mag.has("long", 12, Charge.ROUND) and mag.has("long", 12, Charge.BLANK)
    mag.take("long", 12, Charge.BLANK)
    assert mag.shot[12.0]["round"] == 0 and mag.filled_of("long", 12) == 53


# -- the filling --------------------------------------------------------------------------


def test_the_gunner_fills_the_neediest_kind_at_its_pace_and_counts_the_empty_barrels():
    """The neediest by its share of the level, equal shares in GUN_KINDS order and then
    the larger calibre; each cartridge its man-seconds and its charge from below; the
    man-seconds banked between calls, and gone back to nought with nothing to fill."""
    _, mag = _long_tom()
    assert mag.powder_lb == 300.0 == mag.reserve_lb
    assert mag.fill(500.0) == [] and mag.fill_s == 0.0  # complete: nothing to fill
    mag.set_filled("long", 12, 50)  # 50 of 55 and 200 of 220: the same share
    mag.set_filled("carronade", 12, 200)
    assert mag.short and mag.neediest() == LONG_12
    assert mag.fill(180.0) == [LONG_12]  # 120 + 15 x 4 lb
    assert mag.powder_lb == 296.0 and mag.fill_s == 0.0 and mag.filled_by_gunner == 1
    assert mag.fill(134.0) == [] and mag.fill_s == 134.0  # banked: a carronade's is 135
    assert mag.fill(1.0) == [CARR_12] and mag.fill_s == 0.0
    assert mag.powder_lb == 295.0 and mag.barrels_emptied == 0
    # a barrel emptied as the powder falls through its hundred
    mag.powder_lb = 101.0
    assert mag.fill(180.0) == [CARR_12]  # 201 of 220 is the neediest now
    assert mag.powder_lb == 100.0 and mag.barrels_emptied == 1
    mag.fill(135.0)
    assert mag.powder_lb == 99.0 and mag.barrels_emptied == 1
    assert mag.return_barrels() == 1 and mag.return_barrels() == 0
    # nothing below that will fill what is short: nothing filled, nothing banked
    mag.set_filled("carronade", 12, 220)
    mag.powder_lb = 3.0
    assert mag.short and mag.neediest() is None
    assert mag.fill(1000.0) == [] and mag.fill_s == 0.0
    # held by order
    mag.powder_lb = 50.0
    mag.filling_held = True
    assert mag.fill(1000.0) == [] and mag.filled_of("long", 12) == 51
    mag.filling_held = False
    # the frigate's: equal shares of one kind, the larger calibre first; long before carronade
    frigate = magazine(load_ship(FRIGATE))
    for key in list(frigate.cartridges):
        frigate.set_filled(key[0], key[1], 0)
    order = frigate.fill(fill_seconds(6.0) + fill_seconds(3.0) + fill_seconds(2.6875))
    assert order == [("long", 18.0), ("long", 9.0), ("carronade", 32.0)]


# -- the receipt, what she wants, and the damp ------------------------------------------


def test_receive_wanting_and_spoil_go_by_kind_and_the_wanting_is_to_the_nearest_barrel():
    _, mag = _long_tom()
    w = mag.wanting()
    assert w.empty and w.barrels == 0 and w.powder_lb == 0.0 and w.shot == {}
    for _ in range(10):
        mag.take("long", 12, Charge.ROUND)
    w = mag.wanting()
    assert w.powder_lb == 40.0 and w.barrels == 0  # forty pounds: no whole barrel
    assert w.shot == {12.0: {"round": 10}} and not w.empty
    mag.fill(10_000.0)  # the gunner fills from below: the powder held is the same
    assert mag.filled_of("long", 12) == 55 and mag.powder_lb == 260.0
    assert mag.wanting().powder_lb == 40.0
    for _ in range(5):
        mag.take("long", 12, Charge.ROUND)
    w = mag.wanting()
    assert w.powder_lb == 60.0 and w.barrels == 1  # sixty pounds: the nearest barrel
    mag.report_filled = False
    mag.said_powder_out = True
    mag.report_due = True
    mag.receive(
        150.0, {"12": {"round": 10, "grape": 0}}, when="1805-06-14", words="Received a barrel."
    )
    assert mag.powder_lb == 410.0 and mag.shot[12.0]["round"] == 195
    # a new request for the report, none of it due yet
    assert mag.report_filled and not mag.report_due and not mag.said_powder_out
    w = mag.wanting()
    assert w.powder_lb == 0.0 and w.barrels == 0  # more than the establishment: capped
    assert w.shot == {12.0: {"round": 5}}
    assert mag.account_lines() == ["1805-06-14: Received a barrel."]
    mag.receive(words="Nothing but words.")
    assert mag.account_lines(1) == ["Nothing but words."] and len(mag.account) == 2
    # the damp, by kind, the barrels left alone
    _, mag = _long_tom()
    lost = mag.spoil(0.5)
    assert lost == 27 + 110 + 88
    assert mag.cartridges == {LONG_12: 28, CARR_12: 110, SWIVEL: 88}
    assert mag.powder_lb == 300.0 and mag.short


# -- a magazine of packages 70 to 72 --------------------------------------------------------


def _old_magazine(cartridges: dict, fired: dict | None = None) -> Magazine:
    """A magazine as packages 70 to 72 pickled it: three fields, keyed by calibre."""
    old = Magazine.__new__(Magazine)
    old.__dict__.update(
        {
            "cartridges": dict(cartridges),
            "shot": {12.0: {"round": 200, "grape": 30, "chain": 20}, 0.5: {"round": 160}},
            "fired": dict(fired or {}),
        }
    )
    return pickle.loads(pickle.dumps(old))


@pytest.mark.parametrize("n12,long_n,carr_n", [(275, 55, 220), (100, 20, 80), (101, 20, 81)])
def test_a_package_70_magazine_is_split_by_kind_once_and_logs_and_draws_nothing(
    n12, long_n, carr_n
):
    """The long Tom's calibre-keyed store split over her one long 12 and four carronades
    by the largest remainder (ties in GUN_KINDS order); the rounds fired the same way; the
    level, charges and shot's level from the fit; no powder below and the fit's barrels
    established. Nothing is logged and no stream is opened."""
    w = make_world(7, PRIVATEER)
    old = _old_magazine({12.0: n12, 0.5: 176}, {12.0: 5})
    assert "layout" not in vars(old) and old.layout == 1 and old.level is None
    w.ship.extra["magazine"] = old
    lines, streams = len(w.log), w.rng.stream_names()
    mag = magazine(w.ship)
    assert mag is old and mag.layout == 2
    assert mag.cartridges == {LONG_12: long_n, CARR_12: carr_n, SWIVEL: 176}
    assert mag.fired == {LONG_12: 1, CARR_12: 4}
    assert mag.level == {LONG_12: 55, CARR_12: 220, SWIVEL: 176}
    assert mag.charges == {LONG_12: 4.0, CARR_12: 1.0, SWIVEL: 0.25}
    assert mag.shot_level == {12.0: {"round": 200, "grape": 30, "chain": 20}, 0.5: {"round": 160}}
    assert mag.powder_lb == 0.0 and mag.reserve_lb == 300.0
    assert mag.short == (n12 < 275)
    assert len(w.log) == lines and w.rng.stream_names() == streams
    assert split_by_kind({12.0: n12}, w.ship.fit_spec.guns) == {LONG_12: long_n, CARR_12: carr_n}
    # converted once: asked again, the same store, untouched
    mag.powder_lb = 12.0
    assert magazine(w.ship) is mag and mag.powder_lb == 12.0


def test_an_old_fit_and_an_old_bill_read_their_plain_defaults():
    """A FitSpec and a QuarterBillSpec pickled before this build: the fit's calibre-keyed
    cartridges split by kind (`fit_levels`), no charges (charge_lb's), no barrels and no
    allowance for exercise; the bill's filling reckoned one to every four cannon."""
    ship = load_ship(PRIVATEER)
    new = ship.fit_spec
    old = FitSpec.__new__(FitSpec)
    old.__dict__.update(
        {
            "name": new.name,
            "guns": new.guns,
            "cartridges": {12.0: 275, 0.5: 176},
            "shot": {12.0: {"round": 200}, 0.5: {"round": 160}},
            "source": new.source,
        }
    )
    old = pickle.loads(pickle.dumps(old))
    assert old.charges is None and old.powder_barrels == 0 and old.exercise_charges == 0
    assert fit_levels(old) == {LONG_12: 55, CARR_12: 220, SWIVEL: 176}
    ship.fit_spec = old
    mag = magazine(ship)
    assert mag.level == {LONG_12: 55, CARR_12: 220, SWIVEL: 176}
    assert mag.charges == {LONG_12: 4.0, CARR_12: 1.0, SWIVEL: 0.25}
    assert mag.powder_lb == 0.0 == mag.reserve_lb and not mag.short
    bill = ship.spec.crew.quarter_bill
    assert bill.filling == 1
    was = QuarterBillSpec.__new__(QuarterBillSpec)
    was.__dict__.update({"trimmers": dict(bill.trimmers), "helm": bill.helm, "powder": bill.powder})
    was.__dict__["priority"] = bill.priority
    was = pickle.loads(pickle.dumps(was))
    assert was.filling is None
    ship.spec.crew.quarter_bill = was
    assert filling_of(ship) == 1  # five cannon (the swivels are not cannon): one
    frigate = load_ship(FRIGATE)
    frigate.spec.crew.quarter_bill = copy.copy(frigate.spec.crew.quarter_bill)
    frigate.spec.crew.quarter_bill.filling = None
    assert filling_of(frigate) == 10  # forty cannon


# -- the schema -------------------------------------------------------------------------


def _privateer_doc() -> dict:
    with open(PRIVATEER, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _tom(doc: dict) -> dict:
    return doc["armament"]["fits"]["long tom"]


def test_the_schema_reads_both_forms_of_cartridges_and_refuses_in_words():
    doc = _privateer_doc()
    fit = spec_from_dict(copy.deepcopy(doc), "p.yaml").armament.fit()
    assert fit.cartridges == {LONG_12: 55, CARR_12: 220, SWIVEL: 176}
    assert fit.charges == {LONG_12: 4.0, CARR_12: 1.0, SWIVEL: 0.25}
    assert fit.powder_barrels == 3 and fit.exercise_charges == 0
    # by calibre alone, where one kind has the calibre (the letter of marque's)
    d = copy.deepcopy(doc)
    marque = d["armament"]["fits"]["letter of marque"]
    marque["cartridges"] = {6: 330, 0.5: 176}
    del marque["charges"]
    del marque["powder_barrels"]
    fit = spec_from_dict(d, "p.yaml").armament.fit("letter of marque")
    assert fit.cartridges == {("long", 6.0): 330, SWIVEL: 176}
    assert fit.charges is None and fit.powder_barrels == 0
    # by calibre alone where two kinds share it
    d = copy.deepcopy(doc)
    _tom(d)["cartridges"] = {12: 275, 0.5: 176}
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(d, "p.yaml")
    assert str(e.value) == (
        "p.yaml: the fit 'long tom''s cartridges of 12 are for guns of two kinds (long, "
        "carronade); say them by kind: cartridges: {long: {12: n}, carronade: {12: n}}."
    )
    # a kind and calibre she has no gun of
    d = copy.deepcopy(doc)
    _tom(d)["cartridges"]["carronade"] = {32: 10}
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(d, "p.yaml")
    assert str(e.value) == (
        "p.yaml: the fit 'long tom''s magazine holds cartridges for 32-pounder carronades, "
        "and no gun of that kind and calibre."
    )
    d = copy.deepcopy(doc)
    _tom(d)["charges"]["swivel"] = {0.5: 0.25, 3: 0.5}
    with pytest.raises(ShipFileError, match="holds cartridges for 3-pounder swivels, and no"):
        spec_from_dict(d, "p.yaml")
    d = copy.deepcopy(doc)
    _tom(d)["cartridges"]["pivot"] = {12: 1}
    with pytest.raises(ShipFileError, match="name the kind 'pivot'; the kinds are long"):
        spec_from_dict(d, "p.yaml")
    d = copy.deepcopy(doc)
    _tom(d)["charges"] = {12: 4.0}
    with pytest.raises(ShipFileError, match="charges are said by calibre alone"):
        spec_from_dict(d, "p.yaml")
    d = copy.deepcopy(doc)
    _tom(d)["charges"]["long"] = {12: 0}
    with pytest.raises(ShipFileError, match="say the pounds of powder in a cartridge"):
        spec_from_dict(d, "p.yaml")
    d = copy.deepcopy(doc)
    _tom(d)["powder_barrels"] = -1
    with pytest.raises(ShipFileError, match="powder barrels is -1"):
        spec_from_dict(d, "p.yaml")
    d = copy.deepcopy(doc)
    _tom(d)["powder"] = 3
    with pytest.raises(ShipFileError, match="has 'powder', which a fit does not take"):
        spec_from_dict(d, "p.yaml")
    # the bill's men filling cartridges
    d = copy.deepcopy(doc)
    del d["crew"]["quarter_bill"]["filling"]
    assert spec_from_dict(d, "p.yaml").crew.quarter_bill.filling is None
    d["crew"]["quarter_bill"]["filling"] = -2
    with pytest.raises(ShipFileError, match="the hands filling cartridges is -2"):
        spec_from_dict(d, "p.yaml")


# -- the committed files (§1.2) -------------------------------------------------------------

# (file, fit, filled by kind and calibre, filled powder lb, barrels, exercise charges)
TABLE = [
    (
        FRIGATE,
        None,
        {("long", 18.0): 2054, ("carronade", 32.0): 790, ("long", 9.0): 316},
        15395.125,
        77,
        6,
    ),
    ("data/ships/brig.yaml", None, {("carronade", 32.0): 1264, ("long", 6.0): 158}, 3713.0, 19, 4),
    (CUTTER, "carronades", {CARR_12: 330}, 330.0, 2, 1),
    (CUTTER, "long guns", {("long", 3.0): 330, SWIVEL: 352}, 418.0, 3, 0),
    (PRIVATEER, "long tom", {LONG_12: 55, CARR_12: 220, SWIVEL: 176}, 484.0, 3, 0),
    (PRIVATEER, "letter of marque", {("long", 6.0): 330, SWIVEL: 176}, 704.0, 4, 0),
    ("data/ships/merchant-brig.yaml", None, {("long", 6.0): 104}, 208.0, 2, 0),
]
BILL_FILLING = {
    FRIGATE: 10,
    "data/ships/brig.yaml": 4,
    CUTTER: 1,
    PRIVATEER: 1,
    "data/ships/merchant-brig.yaml": 1,
}


@pytest.mark.parametrize("path,fit,filled,powder,barrels,exercise", TABLE)
def test_the_committed_files_hold_the_build_designs_table(
    path, fit, filled, powder, barrels, exercise
):
    spec = load_spec(path)
    fs = spec.armament.fit(fit)
    assert fs.cartridges == filled
    assert sum(n * fs.charges[k] for k, n in fs.cartridges.items()) == powder
    assert fs.powder_barrels == barrels and fs.exercise_charges == exercise
    assert spec.crew.quarter_bill.filling == BILL_FILLING[path]
    mag = magazine(load_ship(path, fit))
    assert mag.cartridges == filled == mag.level and not mag.short
    assert mag.powder_lb == mag.reserve_lb == barrels * BARREL_LB


@pytest.mark.parametrize("path", sorted(BILL_FILLING))
def test_the_bills_filling_is_one_to_every_four_cannon(path):
    """Falconer's quarter-gunner to every four cannon, the swivels not cannon, one at the
    least; for every fit of the file alike."""
    spec = load_spec(path)
    for fs in spec.armament.fits.values():
        cannon = sum(1 for g in fs.guns if g.kind != "swivel")
        assert spec.crew.quarter_bill.filling == max(1, cannon // 4), fs.name


# -- the words ------------------------------------------------------------------------------


def test_the_reading_counts_the_filled_cartridges_the_powder_below_and_the_shot():
    _, mag = _long_tom()
    for _ in range(25):
        mag.take("long", 12, Charge.ROUND)
    mag.shot[12.0]["round"] = 175
    mag.fired[CARR_12] = 124
    mag.powder_lb = 240.0
    assert mag.describe() == [
        "Filled cartridges: 30 of 55 for the long 12-pounder, 220 of 220 for the 12-pounder "
        "carronades, 176 of 176 for the half-pounder swivels; the gunner filling for the "
        "long 12-pounder.",
        "Powder below: 2 barrels and 40 pounds, of 3 barrels established.",
        "Shot: 12-pounder 175 round, 30 grape, 20 chain; half-pounder 160 round.",
        "149 rounds fired.",
    ]
    mag.filling_held = True
    assert mag.describe()[0].endswith("; the filling stopped by order.")
    mag.filling_held = False
    mag.powder_lb = 3.0  # under a long 12's four pounds: too little, and said so
    assert mag.describe()[0].endswith("; too little powder below to fill more.")
    assert mag.describe()[1] == "Powder below: 3 pounds, of 3 barrels established."
    mag.powder_lb = 0.0
    assert mag.describe()[0].endswith("; no powder below to fill more.")
    assert mag.describe()[1] == "Powder below: none, of 3 barrels established."
    # a ship without guns keeps its words
    assert magazine(load_ship("data/ships/topsail-schooner.yaml")).describe() == [
        "The magazine is empty: she carries no powder."
    ]
    assert Magazine(layout=2).describe() == ["The magazine is empty: she carries no powder."]
