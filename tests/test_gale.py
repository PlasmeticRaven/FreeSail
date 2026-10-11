"""The yards and the helm by the wind, and the ship in a gale (package 37p).

The captain's trials (package 40c) found the frigate in a westerly gale lying aback for
hours with no way, driven up-Channel at four knots, her head sails blown out of their
bolt-ropes and nothing set forward. The package's brief (docs/dev/M6-WorkPackages.md):

- the period's trim by the wind, each level of yards braced in from the level below it,
  and the helmsman's mark the highest sail set, kept just lifting with the rest full;
- the lift of the lower sails his warning, and "Kept her away" when he acts on it;
- storm canvas: the jibs in by their ratings, the storm staysails set over the storm line
  and in place of the head sails and the spanker, `set the storm staysails`;
- heaving to with the way she has, the recovery from aback (the keel's grip astern, the
  helm shifted hard for sternway, `box her off`, and the helm's own box-off after two
  minutes aback);
- the yards by hand in points: in or up so many points, to so many points from the keel,
  braced about; and the log's word when a sail on them shivers or fills.
"""

from __future__ import annotations

import math
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import trim
from freesail.orders import storm
from freesail.physics import hull as hp
from freesail.ship.loader import load_ship
from freesail.ship.parts import HelmMode, SailState

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
BRIG = "data/ships/brig.yaml"
START = datetime(1805, 6, 1, 8, 0, 0)


def world_for(ship=FRIGATE, heading=300.0, knots=15.0, speed=4.0, seed=7):
    """The wind from north: 300 is close-hauled on the starboard tack."""
    scenario = Scenario(
        start_time=START,
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
    )
    return make_world(seed, ship, scenario)


def full_and_by(ship=FRIGATE, knots=15.0, extra=(), ticks=900):
    """Plain sail set, the yards trimmed by the period's trim, kept full and by."""
    world = world_for(ship, 300.0, knots)
    world.submit("set plain sail")
    for order in extra:
        world.submit(order)
    world.run(400)
    world.submit("keep her full and by")
    for i in range(ticks):
        if i % 120 == 0:
            world.submit("trim sails")
        world.tick()
    return world


def events(world, kind, after=0):
    return [e for e in world.log if e.kind == kind and e.tick > after]


def off_wind(world) -> float:
    return abs(math.degrees(units.wrap_pi(world.ship.dyn.heading - world.wind.direction_from)))


# -- 1: the three levels of bracing -------------------------------------------------


class FakeRunner:
    def __init__(self, ship):
        self.started = []
        ship.extra["evolutions"] = self

    def start(self, ship, evolution, subject, params=None):
        self.started.append((evolution, subject, params or {}))
        return f"started {evolution} on {subject}"

    def in_progress(self):
        return []


def frigate_on_a_wind(awa_deg=41.0):
    from freesail.orders import handle

    ship = load_ship(FRIGATE)
    runner = FakeRunner(ship)
    ship.dyn.apparent_wind_angle = units.deg_to_rad(awa_deg)
    ship.dyn.apparent_wind_speed = 8.0
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship, runner, handle


def targets(runner) -> dict[str, float]:
    return {s: math.degrees(abs(p["target_angle"])) for _, s, p in runner.started}


def test_trim_sails_on_a_wind_braces_each_level_in_from_the_one_below():
    """Luce 1884, p. 418: "the top-sail yard ... with the weather yard arm about a half
    point abaft the lower yard, and the top-gallant trimmed by the topsail yard in the
    same way, and so on"; the step the model's (`trim.UPPER_YARDS_IN_DEG`), the courses'
    yards the sharpest, and the after yards staggered sharper than the head yards of their
    level as before (spec 3b §2.2)."""
    ship, runner, handle = frigate_on_a_wind()
    handle(ship, "trim sails")
    t = targets(runner)
    step = trim.UPPER_YARDS_IN_DEG
    fore = ["fore.yard", "fore.topsail.yard", "fore.topgallant.yard", "fore.royal.yard"]
    assert t["fore.yard"] == pytest.approx(math.degrees(ship.spars["fore.yard"].brace_limit))
    for lower, upper in zip(fore, fore[1:], strict=False):
        assert t[upper] == pytest.approx(t[lower] - step)
    for level in ("topsail", "topgallant", "royal"):
        main, head = t[f"main.{level}.yard"], t[f"fore.{level}.yard"]
        assert main == pytest.approx(head + trim.AFTER_YARDS_SHARPER_DEG)


def test_brace_sharp_up_braces_every_yard_to_its_limit_as_before():
    ship, runner, handle = frigate_on_a_wind()
    handle(ship, "brace sharp up")
    for _, sid, params in runner.started:
        limit = math.degrees(ship.spars[sid].brace_limit)
        assert math.degrees(abs(params["target_angle"])) == pytest.approx(limit, abs=0.01)


def test_in_heavy_weather_the_trim_eases_the_lowest_yards_a_point():
    """Luce 1884, ch. XXIX, p. 478, at the third reef: "observing not to brace the topsail
    or lower yards too sharp"; the levels above braced in from them by the trim's step."""
    ship, runner, handle = frigate_on_a_wind()
    for sid in ("fore.topsail", "main.topsail", "mizzen.topsail"):
        ship.sails[sid].reefs = 3
    handle(ship, "trim sails")
    t = targets(runner)
    limit = math.degrees(ship.spars["fore.yard"].brace_limit)
    eased = limit - trim.HEAVY_WEATHER_EASE_DEG
    assert t["fore.yard"] == pytest.approx(eased)
    assert t["fore.topsail.yard"] == pytest.approx(eased - trim.UPPER_YARDS_IN_DEG)


@pytest.mark.parametrize(
    "order, expected",
    [
        ("brace the fore yards in a point", "fore yards in a point"),
        ("brace the main yards up half a point", "main yards up half a point"),
        ("brace the yards to four points", "yards to four points from the keel (45°)"),
    ],
)
def test_the_yards_by_hand_in_points(order, expected):
    """The deck's measure is the point: in or up so many points from where the yards
    stand, to so many points from the keel; the log may say the angle in brackets."""
    world = world_for()
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    world.run(300)
    before = {y.id: y.brace_angle for y in world.ship.spars.values() if y.is_yard}
    e = world.submit(order)
    assert e.kind != "order.rejected", e.text
    world.run(120)
    said = events(world, "yard.braced_by_hand")
    assert said and expected in said[-1].text
    point = units.deg_to_rad(11.25)
    yard = world.ship.spars["fore.yard" if "main" not in order else "main.yard"]
    if "in a point" in order:
        assert yard.brace_angle == pytest.approx(before[yard.id] - point, abs=1e-3)
    elif "up half a point" in order:
        limit = yard.brace_limit
        assert yard.brace_angle == pytest.approx(min(limit, before[yard.id] + point / 2), abs=1e-3)
    else:
        assert yard.brace_angle == pytest.approx(math.pi / 4, abs=1e-3)
    assert yard.id in world.ship.extra["yards_by_hand"]


def test_the_yards_braced_about_go_to_the_other_side_and_a_trim_takes_them_back():
    world = world_for()
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    world.run(300)
    angle = world.ship.spars["mizzen.topsail.yard"].brace_angle
    world.submit("brace the mizzen yards about")
    world.run(120)
    assert world.ship.spars["mizzen.topsail.yard"].brace_angle == pytest.approx(-angle, abs=1e-3)
    assert "for the larboard tack" in events(world, "yard.braced_by_hand")[-1].text
    world.submit("trim sails")
    assert "mizzen.topsail.yard" not in (world.ship.extra.get("yards_by_hand") or ())


def test_a_sail_on_yards_braced_by_hand_is_said_to_shiver_and_to_fill():
    world = world_for()
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    world.submit("steer 295")
    world.run(400)
    world.submit("brace the fore yards in two points")
    world.run(150)
    shivers = events(world, "sail.shivers")
    assert any(e.text == "The fore topsail shivers in the wind." for e in shivers)
    world.submit("steer 250")
    world.run(240)
    assert any(e.text == "The fore topsail fills." for e in events(world, "sail.fills"))


def test_counts_with_the_wrong_brace_words_are_refused():
    world = world_for()
    for order in ("brace the yards sharp up a point", "brace the yards to four points in"):
        assert world.submit(order).kind == "order.rejected"


# -- 2: the helm in full and by --------------------------------------------------------


@pytest.fixture(scope="module")
def frigate_by_the_wind():
    return full_and_by()


def test_full_and_by_the_highest_sail_lifts_first_and_the_rest_stand_a_clean_full(
    frigate_by_the_wind,
):
    """Luce 1884, p. 418n: "when the main royal is just lifting all the other sails are a
    'clean full and by'". Close-hauled under plain sail, trimmed by the period's trim and
    kept full and by, the mark is a topgallant, the highest level set, and lifts more than
    a degree before any other sail; the helmsman keeps her about `MARK_MARGIN` fuller than
    it, and every other square sail stands at least twice that beyond its luff (measured:
    the fore topgallant lifting at 46.5°, the fore topsail first of the rest at 45.0°, she
    at 49.5° apparent, 67.5° from the true wind at 5.1 knots in 15)."""
    ship = frigate_by_the_wind.ship
    mark, rest = ship.extra["helm_mark"], ship.extra["helm_rest"]
    assert ship.extra["helm_mark_sail"].endswith("topgallant")
    assert mark - rest > math.radians(1.0)
    awa = abs(ship.dyn.apparent_wind_angle)
    assert awa - rest >= 2.0 * hp.MARK_MARGIN
    assert abs(awa - mark - hp.MARK_MARGIN) <= math.radians(1.5)


def test_after_a_change_of_sail_the_mark_is_the_new_highest_sail():
    world = full_and_by(ticks=600)
    world.submit("take in the topgallants")
    world.run(300)
    ship = world.ship
    assert ship.extra["helm_mark_sail"].endswith("topsail")


def test_under_reefed_topsails_the_mark_is_the_topsail_and_the_angle_wider():
    """The brief: "Under reefed topsails with the light sails in, the mark is the topsail
    and the angle wider: she is never brought up to the old angle." The light sails in,
    the topsails at the third reef and trimmed, she is kept fuller than under plain sail,
    and never nearer than the old rule (the mean of her sails' luffs and eight degrees;
    measured in 26 knots: the reefed fore topsail lifting 56.3° apparent, the old rule's
    58.5°, which then holds)."""
    plain = full_and_by(ticks=600)
    plain_angle = hp.full_and_by_angle(plain.ship)
    world = full_and_by(knots=26.0, ticks=600)
    world.submit("take in the topgallants")
    world.run(300)
    world.submit("close reef the topsails")
    world.run(1200)
    world.submit("trim sails")
    world.run(600)
    ship = world.ship
    assert ship.extra["helm_mark_sail"].endswith("topsail")
    reefed_angle = hp.full_and_by_angle(ship) - hp.full_for_way(ship)
    assert reefed_angle > plain_angle
    old = ship.extra["luff_angle"] + hp.FULL_AND_BY_MARGIN
    assert reefed_angle >= old - 1e-9


def _kept_full_and_by(trim: str, knots: float = 15.0, ticks: int = 900):
    """The frigate under plain sail, the yards as `trim` leaves them, kept full and by:
    (her mean speed after five minutes, her least, her mean angle off the true wind, the
    ticks she was aback)."""
    world = world_for(FRIGATE, 300.0, knots)
    world.submit("set plain sail")
    world.run(400)
    world.submit(trim)
    world.run(120)
    world.submit("keep her full and by")
    speeds, offs, aback = [], [], 0
    for i in range(ticks):
        if trim == "trim sails" and i % 120 == 0:
            world.submit("trim sails")
        world.tick()
        speeds.append(units.ms_to_knots(world.ship.dyn.u))
        offs.append(off_wind(world))
        if any(s.backed for s in world.ship.sails.values() if s.is_set):
            aback += 1
    tail = slice(300, None)
    mean = sum(speeds[tail]) / len(speeds[tail])
    return mean, min(speeds[tail]), sum(offs[tail]) / len(offs[tail]), aback, world


def test_full_and_by_with_the_yards_braced_sharp_up_keeps_her_way_and_is_never_aback():
    """Package 45 (the owner's notes 1 and 1b of gate m6a: braced sharp up and kept full
    and by she pinched until she was aback, boxed off and repeated; right after `trim
    sails` she steered well). The helmsman's mark is the highest sail only under the
    period's trim by level, where it lifts first; with every yard at its limit the
    courses lift first (`hull.helm_mark_staggered` False) and he keeps her by the old
    rule, the mean luff and its margin: four knots and more, never aback. After `trim
    sails` she lies as 37p measured her, about 67.5 degrees from the wind at five knots."""
    mean, least, off, aback, world = _kept_full_and_by("brace sharp up")
    assert not hp.helm_mark_staggered(world.ship)
    assert mean >= 4.0 and least >= 4.0, (mean, least)
    assert aback == 0
    assert 78.0 < off < 92.0, off  # the old rule's angle, as before package 37p and wider
    mean, least, off, aback, world = _kept_full_and_by("trim sails")
    assert hp.helm_mark_staggered(world.ship)
    assert 4.5 < mean < 5.5 and 64.0 < off < 71.0, (mean, off)
    assert aback == 0


def test_a_schooner_keeps_the_mean_of_her_sails():
    """A fore-and-after sails by her fore-and-aft canvas with the topsail shaking."""
    world = full_and_by(SCHOONER, ticks=300)
    assert "helm_mark" not in world.ship.extra


def test_headed_full_and_by_the_helm_keeps_her_away_and_says_so_once(frigate_by_the_wind):
    world = full_and_by(ticks=600)
    start = world.clock.tick
    world.wind.direction_from = units.wrap_2pi(world.wind.direction_from - math.radians(14))
    world.wind.base_direction = world.wind.direction_from
    world.run(60)
    kept = events(world, "helm.kept_away", start)
    assert len(kept) <= 1
    assert not events(world, "ship.lifting", start)


# -- 3: storm canvas --------------------------------------------------------------------


def test_set_the_storm_staysails_bends_them_sets_them_and_takes_in_what_they_replace():
    """Luce 1884, ch. XXIX, p. 477: "To set fore-storm staysail, and haul down fore topmast
    staysail"; the mizzen's takes the spanker's place as the after sail."""
    world = world_for(knots=20.0)
    world.submit("set plain sail")
    world.run(600)
    e = world.submit("set the storm staysails")
    assert e.kind != "order.rejected", e.text
    world.run(1200)
    sails = world.ship.sails
    assert sails["fore.storm_staysail"].is_set and sails["mizzen.storm_staysail"].is_set
    assert not sails["fore.topmast_staysail"].is_set and not sails["jib"].is_set
    assert not sails["mizzen.spanker"].is_set
    said = [x.text for x in events(world, "sail.storm_canvas")]
    assert any("in place of the fore topmast staysail and the jib" in t for t in said)
    assert world.submit("set the storm staysails").kind == "order.rejected"


@pytest.mark.parametrize("knots", [55.0, 70.0])
def test_the_storm_staysails_stand_a_whole_gale_and_a_storm(knots):
    """Package 45, Part B item 7 (the owner's notes 3 and 5: the mizzen storm staysail
    split and blew out of the bolt-ropes at 10:01 in both gale trials, in a gust of the
    whole gale). Rated by the square metre as the working canvas, a storm staysail bore
    its rating at forty knots apparent and blew out at sixty: the cloth's rating, not the
    sheet's nor the stay's (the probe in docs/dev/TuningNotes.md, package 45). Storm
    canvas is rated for the wind it is cut for (`parts.storm_cloth_rating_for`, seventy
    knots apparent at a strain of 1.35): set in fifty-five and in seventy knots of true
    wind for a quarter of an hour, each storm staysail stands, loaded under its rating,
    and nothing blows out; the fore topmast staysail keeps its rating and 37p's rule."""
    from freesail.ship.parts import storm_cloth_rating_for

    world = world_for(FRIGATE, 300.0, knots, speed=3.0)
    world.submit("set the storm staysails")
    world.run(900)
    ship = world.ship
    for sid in ("fore.storm_staysail", "mizzen.storm_staysail"):
        sail = ship.sails[sid]
        assert sail.state is SailState.SET, (sid, sail.state)
        assert sail.rating_kn == storm_cloth_rating_for(sail.area_m2)
        assert sail.strain_ratio < 1.0, (sid, sail.strain_ratio)
    fore_jib, fore_storm = ship.sails["fore.topmast_staysail"], ship.sails["fore.storm_staysail"]
    assert fore_jib.rating_kn < fore_storm.rating_kn
    assert not [e for e in world.log if "blew out" in e.text], [
        e.text for e in world.log if "blew out" in e.text
    ]
    assert units.ms_to_knots(ship.dyn.apparent_wind_speed) > 40.0


def test_a_schooner_sets_her_storm_jib():
    world = world_for(SCHOONER, knots=20.0)
    world.submit("set plain sail")
    world.run(400)
    world.submit("set the storm staysails")
    world.run(1500)  # the storm jib bent from the sail room in the jib's place, then set
    assert world.ship.sails["storm_jib"].is_set


def test_shorten_sail_takes_in_a_loaded_jib_and_over_the_storm_line_sets_storm_canvas():
    ship = load_ship(FRIGATE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    jib = ship.sails["jib"]
    jib.load_kn = storm.HEAD_SAIL_IN_RATIO * jib.effective_cloth_rating_kn
    lines = storm.shorten_sail_lines(ship, 30.0)
    assert "take in the jib" in lines
    assert "set the storm staysails" not in lines
    assert "set the storm staysails" in storm.shorten_sail_lines(ship, storm.STORM_CANVAS_KN)
    jib.load_kn = 0.5 * storm.HEAD_SAIL_IN_RATIO * jib.effective_cloth_rating_kn
    assert "take in the jib" not in storm.shorten_sail_lines(ship, 30.0)


def test_shorten_sail_reduces_the_after_sail_with_the_reefs():
    """Luce 1884, p. 476: the courses reefed with the second reef in the topsails, the
    mainsail hauled up with the third; the spanker in."""
    ship = load_ship(FRIGATE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    assert storm.shorten_sail_lines(ship, 25.0) == []
    for sid in ship.groups["topsails"]:
        ship.sails[sid].reefs = 1
    lines = storm.shorten_sail_lines(ship, 25.0)
    assert "reef the fore course, one reef" in lines and "take in the mizzen spanker" not in lines
    for sid in ship.groups["topsails"]:
        ship.sails[sid].reefs = 2
    lines = storm.shorten_sail_lines(ship, 25.0)
    assert "take in the main course" in lines and "take in the mizzen spanker" in lines


def test_trim_the_sheets_with_only_square_sail_set_says_so():
    world = world_for(knots=20.0)
    world.submit("set the topsails")
    world.run(400)
    e = world.submit("trim the sheets")
    assert e.kind == "order.rejected"
    assert "no fore-and-aft sail is set" in e.text


# -- 4: aback, sternway and the recovery ------------------------------------------------


def test_the_keels_grip_astern_turns_her_head_off_to_leeward():
    """With sternway the keel's lift acts near the stern: drifting to larboard, her head
    swings to larboard (falls off from a wind on the starboard bow); nothing going ahead."""
    ship = load_ship(FRIGATE)
    h = ship.hull
    assert hp.sternway_yaw(h, 2.0, -0.5) == 0.0
    assert hp.sternway_yaw(h, -1.0, -0.5) < 0.0
    assert hp.sternway_yaw(h, -1.0, 0.5) > 0.0


def test_taken_aback_head_to_wind_she_pays_off_and_fills():
    """The trials' fault: aback with her head in the wind's eye, going astern for an hour
    and a half. Full and by, the helm shifted hard for the sternway and the keel's grip
    astern pay her off: within five minutes she is full and has way on again. (She comes
    back to the wind with too little way and is aback again within the next two minutes,
    under her topsails alone in thirty knots: the model's ship gripes with no way on her,
    which the rudder cannot answer; see the package's tuning notes.)"""
    world = world_for(heading=345.0, knots=30.0, speed=0.0)
    for order in ("set the topsails", "brace sharp up on the starboard tack"):
        world.submit(order)
    world.run(5)
    world.ship.dyn.heading = math.radians(358.0)
    world.ship.dyn.u = -units.knots_to_ms(1.0)
    world.submit("keep her full and by")
    filled = False
    for _ in range(300):
        world.tick()
        filled = filled or (off_wind(world) > 60.0 and world.ship.dyn.u > units.knots_to_ms(1.0))
    assert filled


def test_box_her_off_recovers_her_on_her_tack():
    world = world_for(heading=300.0, knots=18.0)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    world.run(400)
    e = world.submit("box her off")
    assert e.kind != "order.rejected", e.text
    world.run(900)
    done = events(world, "ship.boxed_off")
    assert done and "starboard tack, full and by" in done[0].text
    assert world.ship.dyn.helm_mode is HelmMode.FULL_AND_BY


def test_full_and_by_two_minutes_in_irons_going_astern_the_helm_boxes_her_off():
    """In irons, her sails shaking and not pressed, so not counted aback, and going astern:
    the lee-shore trial's last hours before it, an hour at a knot and a half astern."""
    from freesail.evolutions import scripts

    ship = load_ship(FRIGATE)
    runner = FakeRunner(ship)
    runner.instances = []
    hp.hull_state(ship)
    ship.dyn.helm_mode = HelmMode.FULL_AND_BY
    ship.dyn.u = -units.knots_to_ms(1.5)
    for _ in range(int(scripts.BOX_OFF_AFTER_S) - 1):
        scripts.keep_full_and_by(ship, runner, 1.0)
    assert runner.started == []
    for _ in range(300):
        scripts.keep_full_and_by(ship, runner, 1.0)
    assert [(e, s) for e, s, _ in runner.started] == [("box_off", "ship")]  # once
    ship.dyn.u = units.knots_to_ms(0.5)  # way on again: the next episode may box her off
    scripts.keep_full_and_by(ship, runner, 1.0)
    assert "boxed_off" not in ship.extra["hull"].extra


def test_heave_to_with_sternway_lies_to_drifting_and_says_so():
    """`heave to` completes with the way she has: with sternway steady she is hove to and
    the line says she drifts, where before the evolution waited for her way to come off
    and failed at the end of ten minutes."""
    from freesail.evolutions import scripts

    world = world_for(heading=300.0, knots=20.0)
    world.submit("set the topsails")
    world.run(400)
    world.submit("heave to")
    world.tick()
    inst = next(i for i in world.ship.extra["evolutions"].instances if i.evo.id == "heave_to")
    world.ship.dyn.u = -units.knots_to_ms(3.0)
    words = inst.script.words()
    assert "knots of sternway, and drifts" in words["drifting"]
    assert isinstance(inst.script, scripts.HeaveToScript)
