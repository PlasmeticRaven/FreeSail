"""Package 32e: staying and sheets, the fore-and-aft rig at the small vessels' scale
(spec M5 open items 12 and 13).

- The yaw that scales with the vessel: the lateral plane's damping grows with the
  length squared and cubed, the rudder's lift slope with the blade's aspect ratio; a
  turning truth for each of the four ships in her own lengths (the frigate's is truth 16).
- Staying with Luce's recovery: the schooner's, the cutter's and the brig's tacks beside
  truth 10; the frigate hung in stays and boxed through in a light breeze; a miss under
  three knots still a miss, and the squaring on a miss a brace with a duration.
- The sheet holds the trim: haul, ease, let fly and trim after a let-fly; the sheet's load
  belayed and none let fly; heaving to on the cutter and the schooner with the staysail
  sheet to windward; the starter book's tending routine.

The bands of the small vessels' circles and tacks are judgement, said so in
docs/dev/TuningNotes.md (package 32e): the period sources give a cutter's reputation
("spins on her heel") and no figure, and Luce 1884's Appendix L is steamship trials.
"""

from __future__ import annotations

import math

import pytest

from freesail import orders, units
from freesail.evolutions import trim
from freesail.orders.errors import OrderError
from freesail.physics import hull as hp
from freesail.ship.loader import load_ship
from freesail.ship.parts import LineState
from freesail.ship.schema import RudderSpec
from tests.test_known_truths import (
    FRIGATE,
    SCHOONER,
    close_hauled_on_starboard,
    events,
    knots,
    off_wind,
    under_plain_sail,
    until,
)

CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
SHIPS = {"frigate": FRIGATE, "schooner": SCHOONER, "cutter": CUTTER, "brig": BRIG}


# ---------------------------------------------------------------------------
# The yaw that scales with the vessel
# ---------------------------------------------------------------------------


def test_yaw_damping_grows_with_the_length_squared_and_cubed():
    """The standard form: the linear term proportional to A L^2 u r, the quadratic to
    A L^3 r |r| (package 32e; the earlier form had one length only)."""
    cutter = load_ship(CUTTER).hull
    frigate = load_ship(FRIGATE).hull
    ratio_l = frigate.length / cutter.length
    ratio_a = frigate.lateral_area / cutter.lateral_area
    u, r = 3.0, 0.02
    quad_c = hp.yaw_damping(cutter, 0.0, r)
    quad_f = hp.yaw_damping(frigate, 0.0, r)
    linear_c = hp.yaw_damping(cutter, u, r) - quad_c
    linear_f = hp.yaw_damping(frigate, u, r) - quad_f
    assert linear_f / linear_c == pytest.approx(ratio_a * ratio_l**2, rel=0.02)
    assert quad_f / quad_c == pytest.approx(ratio_a * ratio_l**3, rel=0.02)
    assert linear_c < 0 and quad_c < 0  # opposing the swing


def test_the_rudders_lift_slope_follows_the_blades_aspect_ratio():
    """Helmbold's slope times the effectiveness fitted on the frigate: her blade of 15 ft
    by 4 ft 3 in keeps package 10's 2.5 per radian; the deep narrow blades of the small
    vessels bite harder per square metre; a file with no span takes a blade three times
    as deep as it is broad."""
    frigate = load_ship(FRIGATE).hull.spec.rudder
    assert hp.rudder_aspect_ratio(frigate) == pytest.approx(3.53, abs=0.05)
    assert hp.rudder_lift_slope(frigate) == pytest.approx(2.5, abs=0.05)
    cutter = load_ship(CUTTER).hull.spec.rudder
    assert hp.rudder_lift_slope(cutter) > hp.rudder_lift_slope(frigate)
    assert hp.rudder_aspect_ratio(RudderSpec(area_m2=2.0)) == hp.RUDDER_DEFAULT_ASPECT
    deeper = RudderSpec(area_m2=2.0, span_m=4.0)
    assert hp.rudder_lift_slope(deeper) > hp.rudder_lift_slope(RudderSpec(area_m2=2.0))


def turning_circle(path: str, speed_kn: float = 6.0) -> tuple[float, float, float]:
    """Truth 16's measure: hard a-weather from a beam reach, the transfer when her head
    has come round sixteen points, in her own lengths; her speed at the start and the
    fastest she swung, degrees a second."""
    world = under_plain_sail(path, 270.0, speed_kn=speed_kn)
    d = world.ship.dyn
    v0 = knots(world)
    h0, x0, y0 = d.heading, d.x, d.y
    world.submit("hard a-weather")
    turned, last, ticks, fastest = 0.0, h0, 0, 0.0
    while turned < math.pi and ticks < 900:
        world.tick()
        ticks += 1
        step = abs(units.wrap_pi(world.ship.dyn.heading - last))
        fastest = max(fastest, math.degrees(step))
        turned += step
        last = world.ship.dyn.heading
    assert turned >= math.pi, "did not come round in fifteen minutes"
    dx, dy = world.ship.dyn.x - x0, world.ship.dyn.y - y0
    transfer = abs(dx * math.cos(h0) - dy * math.sin(h0))
    return v0, transfer / world.ship.hull.length, fastest


@pytest.mark.parametrize(
    ("name", "band", "fastest_band"),
    [
        # a topsail schooner: a long shallow hull with a small rudder (judgement; measured
        # 5.4 lengths at 7.9 knots, package 32e)
        ("schooner", (4.0, 7.0), (2.0, 4.5)),
        # a cutter "spins on her heel": the type's reputation, no figure; a circle in her
        # own lengths as the frigate's, swung twice as fast (judgement; 4.9 lengths, 5°/s)
        ("cutter", (3.5, 6.0), (3.5, 7.0)),
        # a brig as a ship in little (judgement; 4.8 lengths at 7.7 knots)
        ("brig", (4.0, 6.0), (2.5, 5.0)),
    ],
)
def test_turning_truths_the_small_vessels_turn_in_their_own_lengths(name, band, fastest_band):
    v0, lengths, fastest = turning_circle(SHIPS[name])
    assert 7.0 <= v0 <= 8.5, f"{name} started at {v0:.1f} kn"
    assert band[0] <= lengths <= band[1], f"{name}: {lengths:.1f} lengths"
    assert fastest_band[0] <= fastest <= fastest_band[1], f"{name} swung {fastest:.2f} deg/s"


def test_the_cutter_swings_twice_as_fast_as_the_frigate():
    """The same circle in lengths, half the length: the cutter turns through sixteen
    points in well under a minute where the frigate takes two (the lead's probe of
    2026-09-30 had her turning as the frigate, in metres)."""
    _, _, frigate = turning_circle(FRIGATE)
    _, _, cutter = turning_circle(CUTTER)
    assert cutter > 1.8 * frigate


# ---------------------------------------------------------------------------
# Staying: the three tacks beside truth 10, and Luce's recovery
# ---------------------------------------------------------------------------


def tack(path: str, knots_: float = 15.0, speed_kn: float = 4.0):
    world = close_hauled_on_starboard(path, knots_, speed_kn)
    start = world.clock.tick
    world.submit("tack ship")
    done, seconds = until(world, ("ship.tacked", "ship.fell_off"), 900)
    lines = [
        (e.tick - start, e.text)
        for e in world.log
        if e.tick >= start
        and e.kind
        in ("evolution.step", "helm.order", "ship.tacked", "ship.missed_stays", "ship.fell_off")
    ]
    return world, done, seconds, lines


def through_the_wind_at(lines) -> int:
    return next(t for t, text in lines if text.startswith("Let go and haul"))


def test_tack_truth_the_schooner_is_about_in_two_and_a_half_minutes():
    """A topsail schooner tacks quickly (Luce 1884, ch. XXXIV; the band is judgement):
    her head through the wind within a minute of "helm's a-lee", her yards round and her
    sheets shifted over within two, steady on the new tack within three (measured: 40 s
    through, 156 s tacked, at 6.9 knots in 15; package 32e)."""
    world, done, seconds, lines = tack(SCHOONER)
    assert [e.kind for e in done] == ["ship.tacked"]
    assert through_the_wind_at(lines) <= 60
    assert 90 <= seconds <= 180, f"tacked in {seconds} s"
    assert world.ship.dyn.tack == "larboard" and knots(world) > 3.0
    assert not any("Mainsail haul" in text for _, text in lines)  # no after yards
    assert any("Draw jib" in text for _, text in lines)


def test_tack_truth_the_cutter_is_quicker_than_the_schooner():
    """A cutter spins on her heel (the type's reputation; the band is judgement): through
    the wind within half a minute, tacked within two (measured: 23 s through, 96 s
    tacked, at 6.3 knots in 15)."""
    world, done, seconds, lines = tack(CUTTER)
    assert [e.kind for e in done] == ["ship.tacked"]
    assert through_the_wind_at(lines) <= 40
    assert 60 <= seconds <= 130, f"tacked in {seconds} s"
    _, _, schooner_s, schooner_lines = tack(SCHOONER)
    assert seconds < schooner_s
    assert through_the_wind_at(lines) < through_the_wind_at(schooner_lines)


def test_tack_truth_the_brig_goes_about_as_a_ship_does():
    """A brig is a ship in little: Luce's five to ten minutes, as the frigate (truth 10;
    measured 415 s at 5.3 knots in 15, the frigate 403 s). Package 37p: in with less way
    under the period's trim, she comes out of stays with less, tacked at 454 s
    with 1.7 knots (355 s and 3.4 before), and has 4.6 two minutes after, 5.3 in four."""
    world, done, seconds, lines = tack(BRIG)
    assert [e.kind for e in done] == ["ship.tacked"]
    assert 285 <= seconds <= 600, f"tacked in {seconds} s"
    assert any(text.startswith("Rise tacks and sheets. Mainsail haul") for _, text in lines)
    world.run(120)
    assert world.ship.dyn.tack == "larboard" and knots(world) > 2.5


def test_the_frigate_hung_in_stays_is_boxed_through_in_a_light_breeze():
    """Luce's recovery (1866, ch. XXIV, 'Tacking', p. 451; 1884, ch. XXXIV, 'Sloops'): in
    seven knots of wind, at under three knots, her way goes within a point of the wind and
    she hangs; the helm is kept a-lee, the head yards aback, the head sheets held to
    windward and the spanker boom hauled over to windward; her head passes the wind, the
    head sails aback pay her off, and she is tacked. The stages in the log, in order (in
    eight knots she carries her way through and tacks plainly)."""
    world, done, seconds, lines = tack(FRIGATE, knots_=7.0, speed_kn=2.5)
    assert [e.kind for e in done] == ["ship.tacked"], [t for _, t in lines]
    texts = [t for _, t in lines]
    hung = next(i for i, t in enumerate(texts) if t.startswith("Her way is gone; she hangs"))
    assert "the head sheets held to windward" in texts[hung]
    assert "the spanker boom hauled over to windward" in texts[hung]
    assert "the head yards aback to box her off" in texts[hung]
    through = next(i for i, t in enumerate(texts) if t.startswith("Her head is through the wind"))
    drawn = next(i for i, t in enumerate(texts) if t.startswith("Let go and haul. Draw jib"))
    assert hung < through < drawn
    assert seconds <= 600 and world.ship.dyn.tack == "larboard"


def test_the_frigate_misses_stays_under_three_knots_and_squares_the_yards_as_a_brace():
    """Truth 10's second half stands: in six knots, at 2.2 knots, her way goes before her
    head comes up to the wind, a plain miss (Luce 1866, 'Missing Stays'); the urgent line
    at the moment, then the yards squared with hands and time (brace_s), the head sheets
    flattened in, the spanker sheet eased off, and the helm put up as an order the
    helmsman carries out; she falls off on the old tack."""
    world = close_hauled_on_starboard(FRIGATE, knots_=6.0, speed_kn=2.0)
    assert 2.0 <= knots(world) < 3.0
    start = world.clock.tick
    world.submit("tack ship")
    missed, _ = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in missed] == ["ship.missed_stays"]
    assert missed[0].severity.value == "urgent"
    assert "Up helm; square the yards; flatten in the head sheets" in missed[0].text
    yards = [y for y in world.ship.spars.values() if y.is_yard]
    assert any(abs(y.brace_angle) > 0.1 for y in yards)  # not yet square: a brace takes time
    fell, seconds = until(world, ("ship.fell_off",), 300)
    assert fell and seconds >= 30, f"the yards were squared in {seconds} s"
    assert all(abs(y.brace_angle) < 1e-6 for y in yards)
    assert "fell off on the starboard tack" in fell[0].text
    world.run(300)
    assert world.ship.dyn.tack == "starboard"
    assert events(world, "ship.tacked", after=start) == []


# ---------------------------------------------------------------------------
# The sheet holds the trim
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def frigate_by_the_wind():
    world = under_plain_sail(FRIGATE, 292.5)
    world.run(300)  # the last sail and sheet work done, the helm steady
    return world


def test_haul_ease_and_let_fly_read_the_sheet(frigate_by_the_wind):
    """One truth: the sheet's length hauled gives the sail's angle by the boom's
    geometry; let fly, the sail flogs and drives nothing; hauled again, it draws."""
    world = frigate_by_the_wind
    ship = world.ship
    spanker = ship.sails["mizzen.spanker"]
    sheet = ship.lines["mizzen.spanker.sheet"]
    geo = trim.sheet_geometry(ship, spanker)
    world.submit("haul aft the spanker sheet")
    world.tick()
    assert sheet.hauled == 1.0 and spanker.sheet_angle == pytest.approx(geo.floor)
    world.submit("ease the spanker sheet two fathoms")
    world.run(5)
    assert sheet.hauled == pytest.approx(1.0 - 2 * trim.FATHOM_M / geo.scope_m)
    assert spanker.sheet_angle == pytest.approx(geo.angle_from_hauled(sheet.hauled))
    assert spanker.sheet_angle > geo.floor and spanker.thrust_kn > 0.0
    drawing_load = sheet.load_kn
    assert drawing_load > 0.0
    e = world.submit("let fly the spanker sheet")
    assert "flogging" in e.text
    world.run(5)
    assert sheet.state is LineState.FREE and sheet.load_kn == 0.0
    assert spanker.shivering and spanker.thrust_kn <= 0.0
    assert ship.spars["mizzen.gaff"].load_kn > 0.0  # it snatches at its spars
    world.submit("haul the spanker sheet")
    world.run(5)
    assert sheet.state is LineState.BELAYED and not spanker.shivering
    assert sheet.hauled == pytest.approx(trim.FATHOM_M / geo.scope_m)  # a fathom taken up
    assert spanker.thrust_kn <= 0.0  # still all but right off: it luffs, and drives nothing
    world.submit("haul aft the spanker sheet")
    world.run(5)
    assert spanker.thrust_kn > 0.0 and sheet.load_kn > 0.0


def test_trim_after_a_let_fly_hauls_the_sheet_back_with_hands_and_time(frigate_by_the_wind):
    """`trim the spanker` is an evolution on the sheet: a sheet let fly is taken up and
    hauled to the trim the wind wants, over a time set by the sail's size, and the sail
    draws again; the order reports the work and the line stands belayed."""
    world = frigate_by_the_wind
    ship = world.ship
    spanker = ship.sails["mizzen.spanker"]
    sheet = ship.lines["mizzen.spanker.sheet"]
    world.submit("let fly the spanker sheet")
    world.run(3)
    assert sheet.state is LineState.FREE
    e = world.submit("trim the spanker")
    assert e.text.startswith("Trimming the sheet of the mizzen spanker")
    runner = ship.extra["evolutions"]
    assert [i.evo.id for i in runner.instances if i.evo.id.startswith("trim_")] == [
        "trim_gaff_sheet"
    ]
    world.run(5)
    assert sheet.state is LineState.BELAYED and 0.0 < sheet.hauled < 1.0  # under way
    done, seconds = until(world, ("sail.trimmed",), 300)
    assert done and 40 <= seconds + 5 <= 120, seconds
    assert "Trimmed the spanker sheet" in done[0].text
    wanted = trim.wanted_sheet_angle("gaff", ship.dyn.apparent_wind_angle)
    assert spanker.sheet_angle == pytest.approx(wanted, abs=units.deg_to_rad(2.0))
    assert spanker.thrust_kn > 0.0 and not spanker.shivering


def test_the_sheet_carries_the_sails_pull_by_its_lever(frigate_by_the_wind):
    """A boomed sail's sheet holds the boom against the sail's moment about the mast: the
    load on the line is the pull times the centre's distance abaft the mast over the
    sheet's lever, more with the boom eased far off."""
    world = frigate_by_the_wind
    ship = world.ship
    spanker = ship.sails["mizzen.spanker"]
    sheet = ship.lines["mizzen.spanker.sheet"]
    world.submit("haul aft the spanker sheet")
    world.run(3)
    geo = trim.sheet_geometry(ship, spanker)
    mast = ship.mast_of(spanker)
    arm = abs(mast.x_m - spanker.x_m)
    expected = spanker.force_kn * arm / geo.lever_m(spanker.sheet_angle)
    assert sheet.load_kn == pytest.approx(expected, rel=1e-6)
    assert 0.0 < sheet.strain_ratio < 0.5  # nothing near parting on a wind in fifteen knots


# ---------------------------------------------------------------------------
# Heaving to the fore-and-after's way
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["cutter", "schooner"])
def test_a_fore_and_after_heaves_to_with_the_staysail_sheet_to_windward(name):
    """Luce 1884, ch. XXXIV, 'To Heave to': "Haul flat aft the main sheet, putting the
    helm down, and haul the staysail sheet to windward". The staysail stands aback by
    its sheet on the weather side, she lies four or five points off forereaching a knot
    or two, and `fill away` lets the staysail draw."""
    world = under_plain_sail(SHIPS[name], 292.5, ticks=600)
    ship = world.ship
    e = world.submit("heave to")
    world.run(300)
    hove = events(world, "ship.hove_to")
    assert hove, [x.text for x in world.log if x.kind == "evolution.failed"]
    assert any("sheet to windward" in x.text for x in world.log if x.tick >= e.tick)
    staysail = ship.sails["fore.staysail"]
    reading = trim.read_sheet(ship, staysail)
    assert reading.held_to_windward and staysail.backed
    weather = "starboard"  # the starboard tack: the wind on the starboard side
    assert ship.lines[f"fore.staysail.sheet.{weather}"].state is LineState.BELAYED
    assert ship.lines["fore.staysail.sheet.larboard"].state is LineState.FREE
    main = ship.sails["main.sail"]
    assert main.sheet_angle == pytest.approx(trim.sheet_geometry(ship, main).floor)
    assert 35.0 <= off_wind(world) <= 65.0, off_wind(world)
    assert abs(units.ms_to_knots(ship.dyn.u)) < 3.5
    world.submit("fill away")
    world.run(300)
    assert events(world, "ship.filled_away")
    assert not trim.read_sheet(ship, staysail).held_to_windward and not staysail.backed
    assert knots(world) > 4.0


# ---------------------------------------------------------------------------
# The starter book tends the sheets
# ---------------------------------------------------------------------------


def test_the_starter_book_tends_the_sheets_every_glass():
    """The free tending is retired: a sheet stays where hands left it until the book's
    routine (every glass) or an order works it. With the spanker eased off, the first
    glass finds it off its trim and works it; the next finds the sheets standing."""
    from pathlib import Path

    book = Path("data/standing_orders/starter.orders").read_text(encoding="utf-8")
    # (with the dialect's own guard since package 37f: not while she is hove to)
    line = (
        'standing order "tend the sheets": every glass, if the manoeuvre in hand is not '
        "hove to then trim the sheets"
    )
    assert line in book
    world = under_plain_sail(FRIGATE, 292.5, ticks=600)
    world.submit(line)
    world.submit("ease the spanker sheet three fathoms")
    world.run(3)
    spanker = world.ship.sails["mizzen.spanker"]
    eased = spanker.sheet_angle
    world.run(1700)
    assert spanker.sheet_angle == pytest.approx(eased)  # nobody touched it
    world.run(300)
    fired = [e for e in world.log if e.actor == "standing order 'tend the sheets'"]
    assert fired and "trimming the sheets" in fired[0].text.lower()
    wanted = trim.wanted_sheet_angle("gaff", world.ship.dyn.apparent_wind_angle)
    assert spanker.sheet_angle == pytest.approx(wanted, abs=units.deg_to_rad(2.0))
    world.run(1800)
    later = [e for e in world.log if e.actor == "standing order 'tend the sheets'"]
    assert any("stand as trimmed" in e.text for e in later[1:])


# ---------------------------------------------------------------------------
# Hove to, she keeps her state until she fills away
# ---------------------------------------------------------------------------


def test_a_course_order_is_refused_while_she_lies_hove_to():
    """Package 33a found the starter book's "keep her full" bearing the schooner away
    from her noon sight with her yards still aback in the record, so that no cast was made
    and a later "heave to" was refused. A course order (by heading, by points, full and
    by) is refused while she lies to, from the deck or from the book, which logs the
    refusal once and stands disarmed; the bare helm and the conning words are the deck's;
    `fill away` gives her back her course."""
    world = under_plain_sail(SCHOONER, 292.5, ticks=600)
    ship = world.ship
    start = world.clock.tick
    world.submit("heave to")
    # package 37f: "Hove to" is said when her way is off, some minutes after the order
    done, _ = until(world, ("ship.hove_to",), 600)
    assert done and "hove_to" in ship.extra
    world.submit(
        'standing order "keep her full": when the apparent wind is forward of 55 degrees '
        "then bear away one point"
    )
    world.run(500)
    assert "hove_to" in ship.extra and knots(world) < 3.5
    rejected = [
        e for e in world.log if e.tick > start and e.actor == "standing order 'keep her full'"
    ]
    assert len(rejected) == 1 and rejected[0].kind == "order.rejected"
    assert "She is hove to; fill away before giving her a course." in rejected[0].text
    for words in ("bear away one point", "keep her full", "steer south"):
        with pytest.raises(OrderError, match="fill away before giving her a course"):
            orders.handle(ship, words)
    e = world.submit("hard a-weather")
    assert e.text.startswith("Helm ordered: hard a-weather")
    world.submit("fill away")
    done, _ = until(world, ("ship.filled_away",), 600)
    assert done and "hove_to" not in ship.extra
    world.submit("steer south")
    assert ship.dyn.helm_mode.value == "heading"


def test_a_sails_aback_line_waits_out_a_seas_period():
    """The physics reads a sail aback or filled every substep; the log says so only when
    the reading has held `BACKED_DWELL_S` (33a's finding: hove to in a seaway the lines
    came at every pitch). Read without a `dt` it records at once."""
    from freesail.physics import sails as sail_physics

    assert sail_physics.BACKED_DWELL_S == 10.0
    world = under_plain_sail(FRIGATE, 292.5, ticks=600)
    ship = world.ship
    sail = ship.sails["main.topsail"]
    assert not sail.backed
    sail_physics._record_backed(ship, sail, True, 1.0)
    assert not sail.backed  # a second's reading: not yet
    for _ in range(9):
        sail_physics._record_backed(ship, sail, True, 1.0)
    assert sail.backed
    sail_physics._record_backed(ship, sail, False, 0.0)
    assert not sail.backed  # no dt: at once


def test_heave_to_given_while_hove_to_or_heaving_to_is_refused_at_once():
    """Package 36's finding: a second `heave to` ran eight minutes of sail work before the
    script's own check said "she is hove to already" and left the yards half braced. The
    refusal is at the order (the lead, 2026-10-02): lying to, and while the manoeuvre is
    in hand."""
    world = under_plain_sail(FRIGATE, 292.5)
    world.run(300)
    world.submit("heave to")
    world.run(20)
    e = world.submit("heave to")
    assert e.kind == "order.rejected" and "heaving to already" in e.text
    world.run(900)
    assert "hove_to" in world.ship.extra
    e = world.submit("heave to")
    assert e.kind == "order.rejected" and "hove to already; fill away" in e.text
