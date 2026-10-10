"""Milestone 3b, package 23: studding sails through the physics, and their booms.

Spec 3b §7 (docs/TechnicalSpec-M3b.md), from Luce 1866 ch. XXIII (line 26509) and 1884
ch. XXIII (line 28668): the weather topmast and topgallant studding sails may be set "with
the wind one point free, or forming an angle of seven points with the keel", the lower
"only ... with the wind abaft the beam". What is tested here:

- the stall: the studding class's lift falls to nothing a point forward of its level's
  angle, and the sail counts as flogging; nothing is refused for setting or carrying
  studding sails on a wind;
- the mechanism behind truths 29 and 30: set at nine points they draw; brought up to six
  they shake, their booms strain, and kept so a boom carries away; both ships;
- the booms: rigged in at the start, the `set` answer through `set_studding`'s own reason,
  and the two refusals of the lee rigging, each once;
- the tack and wear take the studding sails in and the booms in first, with Luce's words,
  and do nothing extra when none are out;
- a sideless studding sail (the ringtail, the water sail) lies in its gaff sail's plane;
- determinism.
"""

from __future__ import annotations

import math
import random

import pytest

from freesail import orders, units
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.evolutions.scripts import STUDDING_IN_S, studding_work
from freesail.evolutions.trim import set_sheet_angle
from freesail.orders.errors import OrderError
from freesail.orders.verbs import BOOM_FOUL_BRACE_DEG
from freesail.physics import sails as sails_mod
from freesail.physics.sails import (
    SAIL_CLASSES,
    STUDDING_MIN_WIND_DEG,
    STUDDING_STALL_BAND_DEG,
    compute_sail_forces,
    studding_level,
    studding_stall,
)
from freesail.physics.strain import (
    CLOTH_WEAR_FLOGGING_FACTOR,
    CLOTH_WEAR_PER_HOUR_SET,
    cloth_wear_per_hour,
)
from freesail.physics.wind import Wind, WindParams
from freesail.ship.parts import SailState

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SHIPS = [FRIGATE, SCHOONER]
SEED = 7
POINT = 11.25
SIX_POINTS = 6 * POINT
NINE_POINTS = 9 * POINT


def rad(deg: float) -> float:
    return units.deg_to_rad(deg)


def scenario_world(path, off_deg, knots, speed=5.0, seed=SEED):
    """Starboard tack (wind from north, on the starboard side), `off_deg` off the wind."""
    return make_world(
        seed,
        path,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=knots,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=360.0 - off_deg,
            ship_speed_kn=speed,
        ),
    )


def stuns(ship):
    return [s for s in ship.sails.values() if s.cls == "studding"]


def events(world, kind, after=0):
    return [e for e in world.log if e.kind == kind and e.tick > after]


# ---------------------------------------------------------------------------
# The stall: data and curve
# ---------------------------------------------------------------------------


def test_the_stall_angles_are_luces():
    # seven points for the topmast and topgallant, the beam for the lower (Luce ch. XXIII)
    assert STUDDING_MIN_WIND_DEG == pytest.approx({"lower": 90.0, "upper": 78.75})
    assert STUDDING_STALL_BAND_DEG == pytest.approx(POINT)
    # only the studding class stalls
    assert all(not c.stall_wind for n, c in SAIL_CLASSES.items() if n != "studding")


@pytest.mark.parametrize("path", SHIPS)
def test_each_studding_sail_has_its_level(path):
    ship = make_ship(path)
    levels = {s.id: studding_level(ship, s) for s in stuns(ship)}
    for sid, level in levels.items():
        if ".lower." in sid or "save_all" in sid or sid in ("ringtail", "water_sail"):
            assert level == "lower", sid
        else:
            assert level == "upper", sid


@pytest.mark.parametrize(
    ("off_deg", "lower", "upper"),
    [
        (SIX_POINTS, 1.0, 1.0),  # close-hauled: all shake
        (7 * POINT, 1.0, 0.0),  # a point free: the upper ones draw (Luce), the lower shake
        (7.5 * POINT, 0.5, 0.0),  # half a point forward of the beam
        (8 * POINT, 0.0, 0.0),  # the beam
        (NINE_POINTS, 0.0, 0.0),
        (180.0, 0.0, 0.0),
    ],
)
def test_the_stall_by_the_wind(off_deg, lower, upper):
    ship = make_ship(FRIGATE)
    lo = ship.sails["fore.lower.studdingsail.starboard"]
    up = ship.sails["fore.topmast.studdingsail.starboard"]
    assert studding_stall(ship, lo, rad(off_deg)) == pytest.approx(lower)
    assert studding_stall(ship, up, rad(off_deg)) == pytest.approx(upper)
    assert studding_stall(ship, ship.sails["fore.course"], rad(off_deg)) == 0.0


def make_wind(from_deg=0.0, knots=12.0):
    return Wind(WindParams.from_nautical(from_deg, knots, 0.0, 0.0), random.Random(0))


def set_by_hand(ship, off_deg, ids, knots=12.0):
    """The ship on the starboard tack `off_deg` off a steady wind, the sails named set with
    their yards braced to the wind, standing still (no ship's motion), for one step."""
    ship.dyn.heading = rad(360.0 - off_deg)
    for spar in ship.spars.values():
        if spar.cls == "studdingsail_boom":
            spar.rigged_out = True
        if spar.is_yard:
            spar.brace_angle = min(spar.brace_limit, rad(max(90.0 - off_deg + 40.0, 0.0)))
    for sid in ids:
        ship.sails[sid].state = SailState.SET
    wind = make_wind(knots=knots)
    compute_sail_forces(ship, wind)
    return wind


@pytest.mark.parametrize("path", SHIPS)
def test_lift_falls_to_nothing_and_the_sail_flogs_forward_of_its_angle(path):
    ship = make_ship(path)
    upper = "fore.topmast.studdingsail.starboard"
    set_by_hand(ship, NINE_POINTS, ["fore.topsail", upper])
    sail = ship.sails[upper]
    drawing = sail.thrust_kn
    assert drawing > 0.0 and not sail.shivering
    assert cloth_wear_per_hour(ship, sail) == pytest.approx(CLOTH_WEAR_PER_HOUR_SET)
    set_by_hand(ship, SIX_POINTS, ["fore.topsail", upper])
    assert sail.shivering
    assert sail.thrust_kn < 0.0  # nothing but the drag of loose cloth
    assert cloth_wear_per_hour(ship, sail) == pytest.approx(
        CLOTH_WEAR_PER_HOUR_SET * CLOTH_WEAR_FLOGGING_FACTOR
    )
    # the snatching comes on the boom as the strain model's flogging does, with all the cloth
    boom = ship.spar_of_role(sail, "boom")
    assert boom.load_kn > sail.force_kn
    assert any(e[1] == "sail.shivering" for e in ship.drain_notes())


# ---------------------------------------------------------------------------
# Truths 29 and 30's mechanism: drawing at nine points, flogging at six, both ships
# ---------------------------------------------------------------------------


def weather_studding_sails_at_nine_points(path, knots):
    world = scenario_world(path, NINE_POINTS, knots)
    world.ship.extra["rng"] = world.rng  # the strain stream, as the session composer wires it
    world.submit("set plain sail")
    world.run(400)
    world.submit("trim sails")
    world.run(200)
    world.submit("rig out the studdingsails, weather")  # the weather booms go out braced up
    world.run(200)
    for _ in range(2):  # those that waited for the sail beside them
        world.submit("set the studdingsails, weather")
        world.run(600)
    world.submit("trim sails")
    world.run(120)
    return world


# Package 37p, for the lead: the schooner set up from rest at nine points gripes up as she
# loses her way setting sail, to within two points, and lies in irons going astern, her helm
# hard over for a quarter of an hour, before the package as since (the model's ship gripes
# with no way, spec M5 §33 item 26). Before it the trims brought her back to nine points;
# with the keel's grip astern she comes out at five points and a half and three knots, her
# sheets trimmed for that wind, and does not bear away again, so the studding sail "at nine
# points" shakes. The frigate's case is as it was.
_SCHOONER_IN_IRONS = pytest.mark.xfail(
    strict=True, reason="the schooner's setup in irons (package 37p; see the comment above)"
)


@pytest.fixture(
    scope="module",
    params=[SHIPS[0], pytest.param(SHIPS[1], marks=_SCHOONER_IN_IRONS)],
    ids=["frigate", "schooner"],
)
def brought_up(request):
    """Set at nine points in 13 knots, then brought up to six and kept so half an hour."""
    world = weather_studding_sails_at_nine_points(request.param, 13.0)
    at_nine = {s.id: (s.is_set, s.shivering, s.thrust_kn) for s in stuns(world.ship)}
    start = world.clock.tick
    world.submit(f"steer {360.0 - SIX_POINTS}")
    for _ in range(30):
        world.submit("trim sails")
        world.run(60)
    return world, at_nine, start


def test_studding_sails_draw_at_nine_points(brought_up):
    world, at_nine, _ = brought_up
    weather = {sid: v for sid, v in at_nine.items() if v[0]}
    assert weather, "no studding sail set at nine points"
    assert all(sid.endswith(".starboard") for sid in weather)  # the weather side
    for sid, (_, shivering, thrust) in weather.items():
        assert not shivering and thrust > 0.0, sid


def test_brought_up_to_six_points_they_shake_strain_and_carry_away(brought_up):
    world, at_nine, start = brought_up
    shaking = {e.subject for e in events(world, "sail.shivering", start)}
    assert shaking == {sid for sid, v in at_nine.items() if v[0]}
    warned = [e for e in events(world, "strain.warning", start) if "studdingsail boom" in e.text]
    assert warned and all("whipping as the" in e.text for e in warned)
    lost = [e for e in events(world, "spar.carried_away", start) if "studdingsail boom" in e.text]
    assert lost, "kept at six points for half an hour, no boom went"
    assert events(world, "evolution.failed", start) == []  # nothing refused: physics only


def test_setting_studding_sails_on_a_wind_is_not_refused():
    ship = make_ship(FRIGATE)
    ship.dyn.heading = rad(360.0 - SIX_POINTS)
    for sid in ("fore.topsail", "fore.course"):
        ship.sails[sid].state = SailState.SET
    for spar in ship.spars.values():
        if spar.cls == "studdingsail_boom":
            spar.rigged_out = True
    orders.handle(ship, "set the fore topmast studdingsail, starboard")  # no refusal


# ---------------------------------------------------------------------------
# Booms: rigged in at the start, the set answer, the lee rigging
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", SHIPS)
def test_booms_start_rigged_in_and_a_gaff_sails_boom_is_not(path):
    ship = make_ship(path)
    booms = [s for s in ship.spars.values() if s.cls == "studdingsail_boom"]
    assert booms and not any(b.rigged_out for b in booms)
    assert "ringtail_boom" in {b.id for b in booms}
    assert all(s.rigged_out for s in ship.spars.values() if s.cls == "boom")
    sails, out = studding_work(ship)
    assert sails == [] and out == []


def test_set_answers_with_what_must_be_done_first():
    ship = make_ship(FRIGATE)
    ship.sails["fore.topsail"].state = SailState.SET
    with pytest.raises(OrderError, match="boom is rigged in; rig it out first"):
        orders.handle(ship, "set the fore topmast studdingsail, starboard")


def test_the_water_sail_needs_no_boom_rigged_out():
    ship = make_ship(SCHOONER)
    water = ship.sails["water_sail"]
    assert ship.spar_of_role(water, "boom").rigged_out  # the main boom


def brace_all(ship, deg):
    for spar in ship.spars.values():
        if spar.is_yard:
            spar.brace_angle = rad(deg)


def test_rig_out_is_refused_for_the_lee_boom_braced_sharp():
    ship = make_ship(FRIGATE)
    brace_all(ship, 60.0)  # braced up for the starboard tack: the larboard yardarms aft
    with pytest.raises(OrderError) as e:
        orders.handle(ship, "rig out the larboard fore lower studdingsail boom")
    assert str(e.value) == "The fore yard is braced too sharp for the boom to go out."
    orders.handle(ship, "rig out the starboard fore lower studdingsail boom")  # to weather
    brace_all(ship, BOOM_FOUL_BRACE_DEG)  # at the angle, not beyond it
    orders.handle(ship, "rig out the larboard fore topmast studdingsail boom")


def test_bracing_sharper_with_the_lee_boom_out_is_refused_once():
    ship = make_ship(FRIGATE)
    ship.spars["fore.topmast.studdingsail_boom.larboard"].rigged_out = True
    with pytest.raises(OrderError) as e:
        orders.handle(ship, "brace the fore topsail yard sharp up on the starboard tack")
    assert (
        str(e.value) == "Rig in the studdingsail boom before bracing the fore topsail yard sharper."
    )
    # the whole mast with the topsail and topgallant set: the boom's yard is refused for the
    # boom alone, and the yards either side of it, which cannot go so far from it while it
    # stays, for the adjacent yards; every yard once, and the boom's reason first
    ship.sails["fore.topsail"].state = SailState.SET
    ship.sails["fore.topgallant"].state = SailState.SET
    _, text, data = orders.handle(ship, "brace the fore yards sharp up on the starboard tack")
    assert len(data["failed_subjects"]) == len(set(data["failed_subjects"]))
    reasons = dict(zip(data["failed_subjects"], data["failed"], strict=True))
    assert reasons["fore.topsail.yard"] == (
        "Rig in the studdingsail boom before bracing the fore topsail yard sharper."
    )
    for yid in ("fore.yard", "fore.topgallant.yard"):
        assert reasons[yid].startswith(f"The {yid.replace('.', ' ')} cannot be braced so far")
    assert text.count("Rig in the studdingsail boom") == 1
    # to the other tack the boom is to weather: not refused
    ship.extra["evolutions"].instances.clear()
    for sid in ("fore.topsail", "fore.topgallant"):
        ship.sails[sid].state = SailState.FURLED  # nothing between the yards to foul
    orders.handle(ship, "brace the fore topsail yard sharp up on the larboard tack")


def test_hauling_a_brace_stops_at_the_lee_rigging():
    ship = make_ship(FRIGATE)
    ship.spars["fore.topmast.studdingsail_boom.larboard"].rigged_out = True
    yard = ship.spars["fore.topsail.yard"]
    for _ in range(9):
        orders.handle(ship, "haul the larboard fore topsail brace")
    assert units.rad_to_deg(yard.brace_angle) == pytest.approx(45.0)
    with pytest.raises(OrderError, match="^Rig in the studdingsail boom before bracing"):
        orders.handle(ship, "haul the larboard fore topsail brace")
    orders.handle(ship, "haul the starboard fore topsail brace")  # coming in is not refused


def test_the_ringtail_boom_is_never_fouled_by_a_brace():
    ship = make_ship(FRIGATE)
    brace_all(ship, 68.0)
    orders.handle(ship, "rig out the ringtail boom")


# ---------------------------------------------------------------------------
# Tack and wear: in studding-sails first
# ---------------------------------------------------------------------------


def close_hauled(path, knots=10.0):
    world = scenario_world(path, SIX_POINTS, knots, speed=4.0)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    world.run(400)
    for _ in range(4):
        world.submit("trim sails")
        world.run(120)
    return world


def until(world, kinds, limit):
    start = world.clock.tick
    for _ in range(limit):
        world.tick()
        done = [e for e in world.log if e.kind in kinds and e.tick > start]
        if done:
            return done
    return []


@pytest.mark.parametrize("path", SHIPS)
def test_the_tack_takes_the_studding_sails_in_first(path):
    world = close_hauled(path)
    ship = world.ship
    weather = [s for s in stuns(ship) if s.side == "starboard" and s.state is SailState.FURLED]
    for s in weather:  # set by hand: the order would have them shake, which is not the point
        ship.spar_of_role(s, "boom").rigged_out = True
        s.state = SailState.SET
    start = world.clock.tick
    world.submit("tack ship")
    done = until(world, ("ship.tacked", "ship.missed_stays"), 1200)
    assert [e.kind for e in done] == ["ship.tacked"]
    steps = [
        e.text for e in world.log if e.tick > start and e.kind in ("evolution.step", "helm.order")
    ]
    assert steps[0] == "Stand by to take in the studding-sails. Haul taut! In studding-sails!"
    assert steps[1] == "In studding-sails; rigged in and got alongside the booms."
    assert steps[2].startswith("Ready about.")
    first = next(e for e in world.log if e.tick > start and e.text == steps[0]).tick
    ready = next(e for e in world.log if e.tick > start and e.text == steps[2]).tick
    assert ready - first >= STUDDING_IN_S - 1
    assert all(s.state is SailState.FURLED for s in stuns(ship) if s.state is not SailState.UNBENT)
    assert studding_work(ship) == ([], [])


@pytest.mark.parametrize("path", SHIPS)
def test_the_tack_without_studding_sails_is_as_it_was(path):
    world = close_hauled(path)
    start = world.clock.tick
    world.submit("tack ship")
    done = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert done
    steps = [
        e.text for e in world.log if e.tick > start and e.kind in ("evolution.step", "helm.order")
    ]
    assert steps[0].startswith("Ready about.")
    assert not any("studding" in t for t in steps)


def test_the_wear_takes_the_studding_sails_in_first():
    world = scenario_world(FRIGATE, 135.0, 10.0)
    world.submit("set plain sail")
    world.run(500)
    ship = world.ship
    for s in stuns(ship):
        if s.state is SailState.FURLED and s.side:
            ship.spar_of_role(s, "boom").rigged_out = True
            s.state = SailState.SET
    ship.spars["ringtail_boom"].rigged_out = True  # a boom out with no sail on it
    start = world.clock.tick
    world.submit("wear ship")
    done = until(world, ("ship.wore", "evolution.failed"), 1500)
    steps = [
        e.text for e in world.log if e.tick > start and e.kind in ("evolution.step", "helm.order")
    ]
    assert steps[0] == "Stand by to take in the studding-sails. Haul taut! In studding-sails!"
    assert steps[1] == "In studding-sails; rigged in and got alongside the booms."
    assert steps[2].startswith("Stand by to wear ship.")
    assert studding_work(ship) == ([], [])
    assert done and done[0].kind == "ship.wore"


def test_booms_alone_are_rigged_in_first():
    world = close_hauled(FRIGATE)
    world.ship.spars["fore.topmast.studdingsail_boom.starboard"].rigged_out = True
    start = world.clock.tick
    world.submit("tack ship")
    world.run(60)
    steps = [
        e.text for e in world.log if e.tick > start and e.kind in ("evolution.step", "helm.order")
    ]
    assert steps[:2] == [
        "Rig in and get alongside the studding-sail booms.",
        "Rigged in the studding-sail booms.",
    ]


# ---------------------------------------------------------------------------
# The ringtail and the water sail: in the gaff sail's plane, on the lee side
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("path", "gaff_sail"), [(FRIGATE, "mizzen.spanker"), (SCHOONER, "main.sail")]
)
@pytest.mark.parametrize("wind_from", [170.0, 190.0])
def test_the_ringtail_lies_in_its_gaff_sails_plane_to_leeward(path, gaff_sail, wind_from):
    ship = make_ship(path)
    ship.dyn.heading = 0.0
    host = ship.sails[gaff_sail]
    host.state = SailState.SET
    set_sheet_angle(ship, host, rad(70.0))  # through the sheet (package 32e)
    ringtail = ship.sails["ringtail"]
    ringtail.state = SailState.SET
    ship.spars["ringtail_boom"].rigged_out = True
    wind = make_wind(from_deg=wind_from, knots=10.0)  # nearly aft, on one quarter or the other
    compute_sail_forces(ship, wind)
    awa = ship.dyn.apparent_wind_angle
    assert sails_mod._chord_angle(ship, ringtail) == pytest.approx(host.sheet_angle)
    y_ring = sails_mod._lateral_offset(ship, ringtail, awa)
    y_host = sails_mod._lateral_offset(ship, host, awa)
    assert y_ring * y_host > 0.0  # the same side, the lee side
    assert (y_ring < 0.0) == (awa > 0.0)
    assert abs(y_ring) > abs(y_host)  # further out: abaft the gaff sail's leech
    assert ringtail.thrust_kn > 0.0


def test_the_water_sail_lies_under_the_main_boom_to_leeward():
    ship = make_ship(SCHOONER)
    ship.dyn.heading = 0.0
    ship.sails["main.sail"].state = SailState.SET
    set_sheet_angle(ship, ship.sails["main.sail"], rad(80.0))
    water = ship.sails["water_sail"]
    water.state = SailState.SET
    compute_sail_forces(ship, make_wind(from_deg=175.0, knots=10.0))
    awa = ship.dyn.apparent_wind_angle
    assert sails_mod._chord_angle(ship, water) == pytest.approx(rad(80.0))
    assert (sails_mod._lateral_offset(ship, water, awa) < 0.0) == (awa > 0.0)


# ---------------------------------------------------------------------------
# Determinism
# ---------------------------------------------------------------------------


def test_studding_sails_brought_up_are_deterministic():
    def run():
        world = scenario_world(FRIGATE, NINE_POINTS, 13.0)
        world.ship.extra["rng"] = world.rng
        ship = world.ship
        for sid in ("fore.course", "fore.topsail", "main.topsail"):
            ship.sails[sid].state = SailState.SET
        for s in stuns(ship):
            if (
                s.side == "starboard"
                and ".lower." not in s.id
                and s.id.split(".")[0] in ("fore", "main")
            ):
                ship.spar_of_role(s, "boom").rigged_out = True
                s.state = SailState.SET
        world.submit("brace the yards to the wind")
        world.run(120)
        world.submit(f"steer {360.0 - SIX_POINTS}")
        world.run(900)
        loads = [(p.id, round(p.load_kn, 9), round(p.condition, 9)) for p in ship.parts.values()]
        return [(e.tick, e.kind, e.text) for e in world.log], loads

    assert run() == run()


def test_the_limit_does_not_flicker():
    ship = make_ship(FRIGATE)
    upper = "fore.topmast.studdingsail.starboard"
    limit = STUDDING_MIN_WIND_DEG["upper"]
    set_by_hand(ship, limit - 0.2, ["fore.topsail", upper])
    assert ship.sails[upper].shivering
    ship.drain_notes()
    set_by_hand(ship, limit + 0.5, ["fore.topsail", upper])  # abaft it, within the margin
    assert ship.sails[upper].shivering and ship.drain_notes() == []
    set_by_hand(ship, limit + 2.0, ["fore.topsail", upper])
    assert not ship.sails[upper].shivering
    assert [n[1] for n in ship.drain_notes()] == ["sail.drawing"]
    assert math.isclose(studding_stall(ship, ship.sails[upper], rad(limit + 2.0)), 0.0)
