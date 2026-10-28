"""The pivot gun (PROVISIONAL: the owner's ask of 2026-10-25, ahead of package 75; spec M7
§7, §8 in package 70's shape): a long gun on a slide carriage turning about a bolt on the
deck's racers, amidships, with no side of its own. It is served whichever side is engaged,
bears over either side between the fore rigging and the main once its crew has trained it
round on the mark, trains half a circle in a minute with its full crew and in proportion
short-handed, and is on the lee side when trained to leeward. The privateer schooner
(`data/ships/privateer-schooner.yaml`) carries one, the long Tom, in her default fit, beside
four carronades; her letter of marque's fit of six long 6-pounders is the other."""

from __future__ import annotations

import math

import pytest

from freesail.combat import guns as G
from freesail.orders.gunnery import guns_named
from freesail.ship.loader import load_ship
from freesail.ship.schema import ShipFileError, _parse_gun

PRIVATEER = "data/ships/privateer-schooner.yaml"


def _firer(heading_deg: float = 0.0, heel_deg: float = 0.0) -> G.Firer:
    return G.Firer(
        heel_deg=heel_deg,
        roll_deg=0.0,
        sea_height_m=0.0,
        weather_factor=1.0,
        half_beam_m=3.65,
        heading_rad=math.radians(heading_deg),
        position=None,
    )


def _target(bearing_deg: float) -> G.Target:
    return G.Target(
        id="mark",
        words="a cutter",
        bearing_rad=math.radians(bearing_deg),
        range_m=500.0,
        heading_rad=0.0,
        length_m=20.0,
        heel_deg=0.0,
        nation=None,
        body=None,
        world=None,
    )


class _Quarters:
    """The bill's answer at the pivot: so many hands of so many wanted."""

    def __init__(self, hands: int, wanted: int) -> None:
        self.hands, self.wanted = hands, wanted

    def hands_at(self, gun):
        return [object()] * self.hands

    def wanted_at(self, gun):
        return self.wanted


@pytest.fixture
def ship():
    return load_ship(PRIVATEER)


def _pivot(ship):
    (g,) = [g for g in ship.guns.values() if g.place == "pivot"]
    return g


def test_the_long_tom_fit_has_a_pivot_gun_with_no_side_and_four_carronades(ship):
    g = _pivot(ship)
    assert (g.kind, g.pounder, g.side) == ("long", 12.0, None)
    assert g.name == "the pivot gun"
    assert g.pair_key == "gun:pivot"  # its own crew, not a broadside pair
    carronades = [x for x in ship.guns.values() if x.kind == "carronade"]
    assert len(carronades) == 4 and {x.side for x in carronades} == {"starboard", "larboard"}
    other = load_ship(PRIVATEER, fit="letter of marque")
    assert not [x for x in other.guns.values() if x.place == "pivot"]


def test_a_pivot_bears_over_either_side_once_trained_and_never_ahead_or_astern(ship):
    b = G.Battery(ship)
    g = _pivot(ship)
    g.train_deg = 90.0
    assert b.bears(g, math.radians(90.0))
    assert not b.bears(g, math.radians(-90.0))  # the mark to larboard: not trained on her
    g.train_deg = -90.0
    assert b.bears(g, math.radians(-90.0))
    for ahead in (0.0, 15.0, -170.0):  # the fore rigging, the main and the boom in the way
        g.train_deg = ahead
        assert not b.bears(g, math.radians(ahead))
    # the owner's arc of 2026-10-25: sixty to a hundred and forty off the bow, either side
    for deg, bears in ((55.0, False), (61.0, True), (139.0, True), (145.0, False)):
        for sign in (1.0, -1.0):
            g.train_deg = sign * deg
            assert b.bears(g, math.radians(sign * deg)) is bears, (sign * deg, bears)


def test_the_crew_trains_it_round_half_a_circle_a_minute_and_slower_short_handed(ship):
    b = G.Battery(ship)
    g = _pivot(ship)
    g.cast_loose = True
    firer = _firer(heading_deg=0.0)
    starboard = _target(90.0)
    for _ in range(20):  # twenty seconds: sixty degrees of ninety
        b._train_pivots(1.0, None, firer, starboard)
    assert g.train_deg == pytest.approx(60.0)
    assert not b.bears(g, math.radians(90.0))
    for _ in range(12):
        b._train_pivots(1.0, None, firer, starboard)
    assert g.train_deg == pytest.approx(90.0) and b.bears(g, math.radians(90.0))
    # the mark crosses to larboard: round the shorter way, a minute for the half circle
    larboard = _target(-90.0)
    for _ in range(30):
        b._train_pivots(1.0, None, firer, larboard)
    assert g.train_deg == pytest.approx(0.0)  # half way, swinging across the deck
    for _ in range(30):
        b._train_pivots(1.0, None, firer, larboard)
    assert g.train_deg == pytest.approx(-90.0)
    # short-handed, half its crew: half the pace; nobody at it, not at all
    g.train_deg = 0.0
    for _ in range(10):
        b._train_pivots(1.0, _Quarters(4, 9), firer, starboard)
    assert g.train_deg == pytest.approx(10 * G.PIVOT_TRAIN_DEG_S * 4 / 9)
    before = g.train_deg
    b._train_pivots(10.0, _Quarters(0, 9), firer, starboard)
    assert g.train_deg == before


def test_a_secured_pivot_is_not_trained_and_the_pivot_serves_whichever_side_is_engaged(ship):
    b = G.Battery(ship)
    g = _pivot(ship)
    b._train_pivots(30.0, None, _firer(), _target(90.0))
    assert g.train_deg == 0.0  # still secured fore and aft
    for x in ship.guns.values():
        x.cast_loose = True
    b.engaged = "larboard"
    assert b.serving(g)
    starboard_carronade = ship.guns["gun.1.starboard"]
    assert not b.serving(starboard_carronade)
    assert b._side_fires(g)


def test_a_pivot_trained_to_leeward_is_on_the_lee_side(ship):
    g = _pivot(ship)
    g.train_deg = 90.0  # trained to starboard
    assert G._is_lee(g, heel_deg=8.0)  # heeled to starboard
    assert not G._is_lee(g, heel_deg=-8.0)


def test_the_orders_name_the_pivot_gun_and_the_long_tom(ship):
    assert guns_named(ship, "the pivot gun") == ["pivot"]
    assert guns_named(ship, "the long Tom") == ["pivot"]
    assert guns_named(load_ship(PRIVATEER, fit="letter of marque"), "the pivot gun") == []


def test_a_pivot_gun_with_a_side_is_refused_at_the_load():
    gun = {
        "id": "pivot",
        "kind": "long",
        "pounder": 12,
        "place": "pivot",
        "side": "starboard",
        "x_m": 0.0,
        "height_m": 1.7,
        "crew": 9,
        "weight_cwt": 34.0,
    }
    with pytest.raises(ShipFileError, match="no side"):
        _parse_gun(gun, 0, "the fit 'long tom'", "test")


def test_each_pivot_bears_through_its_own_arc_from_its_ship_file(ship):
    """Package 86 (the review of the owner's local work, section 3): the arc is the gun's,
    read from its ship file, so another ship's pivot need not inherit the schooner's sixty
    to a hundred and forty; a gun with none (or pickled before it) takes the default."""
    from freesail.orders.gunnery import _guns_bearing

    g = _pivot(ship)
    assert g.arc_deg == (60.0, 140.0) and G.pivot_arc(g) == (60.0, 140.0)
    b = G.Battery(ship)
    g.arc_deg = (40.0, 120.0)  # a pivot clear of the fore rigging further forward
    for deg, bears in ((45.0, True), (125.0, False)):
        g.train_deg = deg
        assert b.bears(g, math.radians(deg)) is bears, (deg, bears)
    assert [x.id for x in _guns_bearing(ship, 45.0) if x.place == "pivot"] == ["pivot"]
    assert not [x.id for x in _guns_bearing(ship, 125.0) if x.place == "pivot"]
    del g.arc_deg  # an old pickle's gun: the class's default, the default arc
    assert g.arc_deg is None and G.pivot_arc(g) == (G.ARC_PIVOT_FROM_DEG, G.ARC_PIVOT_TO_DEG)


def test_an_arc_is_refused_on_a_gun_that_is_no_pivot_and_out_of_its_bounds():
    gun = {
        "id": "gun.1.starboard",
        "kind": "long",
        "pounder": 6,
        "place": "broadside",
        "number": 1,
        "side": "starboard",
        "crew": 6,
        "weight_cwt": 20.0,
        "arc_deg": [60, 140],
    }
    with pytest.raises(ShipFileError, match="only a pivot gun"):
        _parse_gun(gun, 0, "the fit 'letter of marque'", "test")
    pivot = {"id": "pivot", "kind": "long", "pounder": 12, "place": "pivot", "crew": 9}
    for bad in ([140, 60], [60], [-5, 90], [60, 190], ["sixty", 140]):
        with pytest.raises(ShipFileError, match="arc_deg"):
            _parse_gun(dict(pivot, arc_deg=bad), 0, "the fit 'long tom'", "test")
    assert _parse_gun(dict(pivot, arc_deg=[50, 130]), 0, "f", "test").arc_deg == (50.0, 130.0)
