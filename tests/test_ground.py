"""The grounding (spec M5 §18; package 34): the tide over the tiles and the charted
dangers, the strike and its consequences (the stop, the masts, the leak, the well), the
master's word by his own tide, and floating off on the flood. Truth 66 of spec M5 §19."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import ground as G
from freesail.world.geo import Position, bearing_and_distance

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
REGION = "channel-west"
THE_MANACLES = Position(50.04666, -5.04419)
# fourteen miles east-south-east of the Manacles, in the forty-fathom water
APPROACH = Position(49.88, -4.78)
THE_HIGH = [
    {
        "name": "the old high over Biscay",
        "kind": "high",
        "radius_km": 900,
        "track": [
            {"at": "1805-06-11T12:00", "x_km": 300, "y_km": -500, "hpa": 1024},
            {"at": "1805-06-13T12:00", "x_km": 500, "y_km": -600, "hpa": 1022},
        ],
    }
]


def thick_world(
    ship: str, pos: Position, heading: float, start: datetime, from_deg=180.0, knots=15.0
):
    """A world in a mile of fog on a pinned wind (the sky pinned wants a system, as the
    gate's thick passage has one)."""
    sc = Scenario(
        start_time=start,
        wind_from_deg=from_deg,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position={"lat_deg": pos.lat_deg, "lon_deg": pos.lon_deg},
        region=REGION,
        sky={"sky": "thick", "weather": "fog", "visibility": "a mile"},
        weather=[
            {"at": "1805-06-12T00:00", "from_deg": from_deg, "knots": knots, "air_mass": "neutral"}
        ],
        systems=THE_HIGH,
    )
    return make_world(7, ship, sc)


def run_until_aground(world, hours: float):
    for _ in range(int(hours * 60)):
        world.run(60)
        if world.ship.extra.get("aground"):
            return True
    return False


def miles_to_the_manacles(world) -> float:
    return units.m_to_nm(bearing_and_distance(world.position, THE_MANACLES)[1])


# ---------------------------------------------------------------------------
# Truth 66
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def standing_on_by_account():
    """The schooner on the ebb of 12 June 1805 (high water about five in the morning),
    steering for the Manacles through fog by her account alone."""
    w = thick_world(SCHOONER, APPROACH, 300.0, datetime(1805, 6, 12, 5, 0))
    w.submit("set plain sail")
    w.submit("steer NW by W")
    aground = run_until_aground(w, 5.0)
    return w, aground


def test_truth_66_standing_on_by_account_grounds_the_schooner_on_the_ebb_at_the_logs_speed(
    standing_on_by_account,
):
    """Spec M5 §19, truth 66, first clause: "Standing on by account across the reckoning's
    ellipse toward the Manacles in thick weather grounds the schooner on the ebb at the
    speed the log gives"."""
    w, aground = standing_on_by_account
    assert aground
    strike = [e for e in w.log if e.kind == "ship.aground"]
    assert len(strike) == 1
    e = strike[0]
    assert e.severity.value == "urgent"
    assert not e.data["rising"] and "on the ebb" not in e.text and "the tide falling" in e.text
    assert miles_to_the_manacles(w) < 2.0  # the shore about the Manacles
    logs = [x for x in w.log if x.kind == "log.read"]
    assert logs and abs(e.data["speed_kn"] - float(logs[-1].data["knots"])) < 1.5
    assert "she struck at five knots" in e.text or "she struck at six knots" in e.text
    # the fog hid the land till it was close aboard: nothing seen beyond a mile and a half
    seen = [x for x in w.log if x.kind == "lookout.sighting" and x.tick > 0]
    close = 1.5 * units.NAUTICAL_MILE
    assert all(x.data.get("distance_m", x.data["estimate_m"]) < close for x in seen), seen
    # the consequences: her way over the ground checked (the stream runs past her), the
    # carpenter's report, the master's word
    assert w.ship.dyn.speed < 1.0 and w.ship.extra["aground"]
    assert [x for x in w.log if x.kind == "ship.leak"]
    master = [x for x in w.log if x.kind == "ground.master"]
    assert master and "by the epitome" in master[0].text and "flood" in master[0].text
    # held fast: the stream runs past her and she does not move
    pos = w.position
    w.run(600)
    assert bearing_and_distance(pos, w.position)[1] < 1.0
    assert w.readings.words("anchor").startswith("aground")


def test_truth_66_the_same_passage_with_the_lead_going_hourly_does_not_ground():
    """Truth 66, second clause: the deep-sea lead hourly (the ship brought to for it, as
    the Channel Soundings are struck), the master hauling off at the forty-fathom line
    the pilots make the mark of the Lizard's and the Manacles' ground."""
    w = thick_world(SCHOONER, APPROACH, 300.0, datetime(1805, 6, 12, 5, 0))
    w.submit("set plain sail")
    w.submit("steer NW by W")
    for line in (
        'standing order "bring to for the lead": every hour then heave to',
        'standing order "the deep-sea lead": at hove to then heave the deep-sea lead',
        'standing order "fill away after the cast": at a sounding then fill away',
        'standing order "stand on": at filled away, if the depth exceeds 40 fathoms '
        "then steer NW by W",
        'standing order "haul off": at filled away, if the depth is under 40 fathoms then steer SE',
    ):
        assert w.submit(line).kind != "order.refused", line
    aground = run_until_aground(w, 6.0)
    assert not aground
    casts = [e for e in w.log if e.kind == "sounding"]
    assert len(casts) >= 5 and all(e.data["deep"] for e in casts)
    assert any(e.data["fathoms"] < 40.0 for e in casts)  # the line found, and hauled off from
    assert miles_to_the_manacles(w) > 1.5


# ---------------------------------------------------------------------------
# The consequences, each
# ---------------------------------------------------------------------------


def test_a_rock_at_speed_shocks_the_masts_and_stoves_her_and_the_well_rises():
    """The strike on a charted rock at six knots: the topmasts shaken (a strain warning
    or a spar carried away), the carpenter's report of her stove, the well rising by the
    foot, and in time waterlogged."""
    # the frigate run on to the Manacles from the south-east on the flood at six knots
    start = datetime(1805, 6, 12, 12, 0)
    w = thick_world(FRIGATE, Position(50.025, -5.015), 315.0, start, from_deg=180.0, knots=22.0)
    w.submit("set plain sail")
    w.submit("steer NW")
    assert run_until_aground(w, 1.5)
    strike = [e for e in w.log if e.kind == "ship.aground"][0]
    assert "(rock)" in strike.data["where"] or strike.data["rock"]
    assert strike.data["speed_kn"] >= G.SHOCK_SPEED_KN  # the blow felt in the masts
    leak = [e for e in w.log if e.kind == "ship.leak"]
    assert leak and "stove on the rock" in leak[0].text
    rate = w.ship.extra["leak_m_per_h"]
    assert rate >= G.LEAK_ROCK_M_PER_H * (4.0 / G.LEAK_REFERENCE_KN) ** 2
    w.run(3600)
    rising = [e for e in w.log if e.kind == "well.rising"]
    assert rising and "in the well" in rising[0].text
    w.run(6 * 3600)
    assert [e for e in w.log if e.kind == "ship.waterlogged"]


def test_the_blow_of_the_strike_shakes_the_topmasts_and_carries_them_away_at_speed():
    """`strain.shock_spars`: the strike at six knots is one strain of the rating on the
    topmasts and above (half on the lower masts), which wears them and warns; at nine
    knots (a strain of 2.25) they carry away by the strain stream's draw or for certain
    when spent. The ground hands the physics the ratio (speed / SHOCK_SPEED_KN) squared."""
    from freesail.physics import strain

    w = make_world(7, FRIGATE, Scenario(wind_speed_kn=10.0, gustiness=0.0, variability=0.0))
    ship = w.ship
    topmasts = [s for s in ship.spars.values() if s.cls == "topmast"]
    before = {s.id: s.condition for s in topmasts}
    strain.shock_spars(ship, (5.0 / G.SHOCK_SPEED_KN) ** 2)  # five knots: nothing felt
    assert all(s.condition == before[s.id] for s in topmasts)
    strain.shock_spars(ship, (7.0 / G.SHOCK_SPEED_KN) ** 2)  # seven: shaken and warned
    assert all(s.condition < before[s.id] for s in topmasts)
    w.run(1)
    assert [e for e in w.log if e.kind == "strain.warning"]
    strain.shock_spars(ship, (12.0 / G.SHOCK_SPEED_KN) ** 2)  # twelve: a strain of four
    w.run(1)
    assert any(s.wrecked for s in topmasts)
    assert [e for e in w.log if e.kind == "spar.carried_away"]


def test_soft_ground_on_the_ebb_holds_her_till_the_flood_floats_her():
    """A bank taken slowly on the ebb: no leak to speak of, held fast through low water,
    and off on the flood, the log saying so; the master's word by his epitome first."""
    # Falmouth bank off Pendennis, two fathoms and a half, on the ebb of the forenoon
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 7, 0),
        wind_from_deg=90.0,
        wind_speed_kn=8.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=270.0,
        ship_speed_kn=2.0,
        position={"lat_deg": 50.152, "lon_deg": -5.030},
        region=REGION,
    )
    w = make_world(7, FRIGATE, sc)
    w.submit("set the fore topsail")
    assert run_until_aground(w, 1.0)
    strike = [e for e in w.log if e.kind == "ship.aground"][0]
    assert not strike.data["rock"] and not strike.data["rising"]
    assert w.ship.extra.get("leak_m_per_h", 0.0) < 0.05
    master = [e for e in w.log if e.kind == "ground.master"][0]
    assert "will not float before the flood" in master.text
    afloat_tick = None
    for _ in range(12 * 60):
        w.run(60)
        if not w.ship.extra.get("aground"):
            afloat_tick = w.clock.tick
            break
    assert afloat_tick is not None
    off = [e for e in w.log if e.kind == "ship.afloat"]
    assert off and off[0].text.startswith("She is off, and afloat again")
    assert w.tide_state.rising
    assert (afloat_tick - strike.tick) > 2 * 3600  # through the low water


def test_the_dangers_cover_and_uncover_with_the_tide():
    """A drying rock with a head above the datum is seen at low water and not at high;
    the grounding reads the tide over it (spec M5 §18); a rock with a height is seen at
    any tide."""
    chart = make_world(
        7, FRIGATE, Scenario(position={"lat_deg": 50.15, "lon_deg": -5.03}, region=REGION)
    ).chart
    features = chart.features.values()
    black_rock = next(f for f in features if f.id == "black-rock-falmouth")
    manacles = next(f for f in features if f.id == "the-manacles")
    rose = next(f for f in features if f.id == "rose-rock")
    assert black_rock.dries_m == 3.0 and black_rock.covered(4.0) and not black_rock.covered(2.0)
    assert manacles.head_above_datum_m() == 2.0 and not manacles.covered(5.0)  # a head always up
    assert rose.head_above_datum_m() == -4.0 and rose.covered(0.0)
    # fifteen feet of draught over the Rose: aground at the datum, afloat with a metre of tide
    length, draught = 40.0, units.feet_to_m(15.0)
    assert chart.danger_under(rose.position, 0.0, length, draught, 0.0) is not None
    assert chart.danger_under(rose.position, 0.0, length, draught, 1.0) is None
