"""The 'trim' order (package 13): yards to the wind, sheets tended."""

import math

import pytest

from freesail import units
from freesail.orders import handle
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from freesail.ship.stub import OrderError


class FakeRunner:
    def __init__(self, ship):
        self.started = []
        ship.extra["evolutions"] = self

    def start(self, ship, evolution, subject, params=None):
        self.started.append((evolution, subject, params or {}))
        return f"started {evolution} on {subject}"

    def step(self, ship, dt, wind):
        pass

    def in_progress(self):
        return []


def frigate(awa_deg=41.0):
    ship = load_ship("data/ships/frigate-36.yaml")
    runner = FakeRunner(ship)
    ship.dyn.apparent_wind_angle = units.deg_to_rad(awa_deg)
    ship.dyn.apparent_wind_speed = 8.0
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship, runner


def test_trim_the_yards_braces_every_yard_for_the_tack():
    ship, runner = frigate(41.0)  # wind on the starboard bow
    kind, text, data = handle(ship, "trim the yards")
    yards = [y for y in ship.spars.values() if y.is_yard]
    assert {s for _, s, _ in runner.started} == {y.id for y in yards}
    for _, sid, params in runner.started:
        assert params["target_angle"] > 0  # starboard tack: positive
        assert params["target_angle"] <= ship.spars[sid].brace_limit + 1e-9
    assert kind == "evolution.started"
    assert data["trimmed_sheets"] == []


def test_trim_on_the_larboard_tack_is_negative_and_wider_wind_braces_less():
    ship, runner = frigate(-41.0)
    handle(ship, "trim the yards")
    close = {s: p["target_angle"] for _, s, p in runner.started}
    assert all(v < 0 for v in close.values())
    ship2, runner2 = frigate(-110.0)  # a broad reach
    handle(ship2, "trim the yards")
    broad = {s: p["target_angle"] for _, s, p in runner2.started}
    for sid in close:
        assert abs(broad[sid]) < abs(close[sid])


def test_trim_the_sheets_works_each_sheet_by_an_evolution():
    """Package 32e (spec M5 open item 13): the sheet holds the trim, so 'trim the sheets'
    starts a sheet evolution with hands and time for each set fore-and-aft sail whose
    sheet is off its trim, and sets nothing at once; a sheet at its trim stands."""
    ship, runner = frigate(60.0)  # the sheets flat aft at the sails' floors
    kind, text, data = handle(ship, "trim the sheets")
    assert [(e, s) for e, s, _ in runner.started] == [
        ("trim_gaff_sheet", "mizzen.spanker"),
        ("trim_jib_sheet", "fore.topmast_staysail"),
        ("trim_jib_sheet", "jib"),
    ]
    assert all(p["angle_deg"] is None and "sail" in p for _, _, p in runner.started)
    assert kind == "sail.trimmed"
    assert set(data["trimmed_sheets"]) >= {"the mizzen spanker", "the jib"}
    from freesail.evolutions import trim

    spanker = trim.read_sheet(ship, ship.sails["mizzen.spanker"])
    assert spanker.angle == pytest.approx(units.deg_to_rad(18)) and not spanker.free
    assert "trimming the sheets of the mizzen spanker" in text.lower()
    # at their trim already, the sheets stand and the line says so
    from freesail.evolutions import trim

    for sid in ("mizzen.spanker", "fore.topmast_staysail", "jib"):
        sail = ship.sails[sid]
        trim.set_sheet_angle(
            ship, sail, trim.wanted_sheet_angle(sail.cls, ship.dyn.apparent_wind_angle)
        )
    runner.started.clear()
    kind, text, data = handle(ship, "trim the sheets")
    assert runner.started == [] and data["trimmed_sheets"] == []
    assert len(data["standing_sheets"]) == 3 and "stand as trimmed" in text


def test_trim_sails_does_both_and_logs_a_sentence():
    ship, runner = frigate(50.0)
    kind, text, data = handle(ship, "trim sails")
    assert runner.started and data["trimmed_sheets"]
    assert kind == "sail.trimmed"
    assert text.startswith("Braced ") and "to the wind" in text


def test_trim_without_wind_is_refused():
    ship, _ = frigate(41.0)
    ship.dyn.apparent_wind_speed = 0.0
    with pytest.raises(OrderError, match="no wind"):
        handle(ship, "trim sails")


def test_wrecked_yards_are_reported_not_trimmed():
    ship, runner = frigate(41.0)
    ship.spars["fore.royal.yard"].wrecked = True
    _, text, data = handle(ship, "trim the yards")
    assert "fore.royal.yard" not in {s for _, s, _ in runner.started}
    assert "fore.royal.yard" in data["failed_subjects"]
    assert "carried away" in text


def test_trim_targets_follow_the_lift_peak():
    """The lowest yard follows the lift peak to its limit; since package 37p the yard
    above it is braced in from it by the trim's step (`trim.UPPER_YARDS_IN_DEG`, the
    period's trim by the wind, tests/test_gale.py)."""
    ship, runner = frigate(41.0)
    handle(ship, "trim the yards")
    from freesail.evolutions.trim import UPPER_YARDS_IN_DEG
    from freesail.physics.sails import SAIL_CLASSES

    cls = SAIL_CLASSES["square"]
    best = cls.alpha[max(range(len(cls.lift)), key=lambda i: cls.lift[i])]
    chord = units.deg_to_rad(41.0) - best
    course = ship.spars["fore.yard"]
    expected = min(math.pi / 2 - max(chord, 0.0), course.brace_limit)
    got = {s: p["target_angle"] for _, s, p in runner.started}
    assert got["fore.yard"] == pytest.approx(expected)
    topsail = ship.spars["fore.topsail.yard"]
    step = units.deg_to_rad(UPPER_YARDS_IN_DEG)
    assert got["fore.topsail.yard"] == pytest.approx(min(expected - step, topsail.brace_limit))


def test_backing_a_topsail_lays_the_whole_masts_yards_aback():
    """'Back the main topsail' braces every yard on the main mast the other way:
    one yard braced against the yards above and below would foul their sails."""
    ship, runner = frigate(41.0)  # starboard tack
    handle(ship, "back the main topsail")
    subjects = {s for _, s, _ in runner.started}
    main_yards = {
        y.id for y in ship.spars.values() if y.is_yard and ship.mast_of(y).id == "main.mast"
    }
    assert subjects == main_yards
    assert all(
        p["tack"] == "larboard" for _, _, p in runner.started
    )  # aback from the starboard tack
    assert not any(s.startswith("fore.") for s in subjects)


def test_a_trims_braces_log_one_line_when_the_last_is_done():
    """Playtest 7, finding 6 (package 29b): a trim logged twelve lines as its braces began
    and twelve as they ended. Now the order's own line says what was ordered, the braces
    begin without a line each, and one notable line says they are done, its data naming
    every yard and its angle; a yard trimmed alone still has its own line."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    w = make_world(
        7,
        "data/ships/frigate-36.yaml",
        Scenario(wind_from_deg=0, ship_heading_deg=180, gustiness=0, variability=0),
    )
    w.submit("set plain sail")
    w.run(2400)
    w.wind.direction_from += 0.4
    w.wind.base_direction += 0.4
    w.run(5)
    n0 = len(w.log)
    w.submit("trim the yards")
    w.run(900)
    after = w.log.all()[n0:]
    said = [e for e in after if e.kind == "sail.trimmed"]
    assert said and said[0].text.startswith("Braced twelve yards to the wind,")
    assert not [e for e in after if e.text.startswith("Man the") and "braces" in e.text]
    (braced,) = [e for e in after if e.kind == "yard.braced"]
    assert braced.severity.value == "notable"
    assert braced.text.startswith("Braced twelve yards to the wind; ")
    assert braced.text.endswith(" from square.")
    yards = [y.id for y in w.ship.spars.values() if y.is_yard]
    assert sorted(braced.data["subjects"]) == sorted(yards)
    assert set(braced.data["brace_deg"]) == set(yards)
    n1 = len(w.log)
    w.submit("trim the fore yard")
    w.run(300)
    alone = [e for e in w.log.all()[n1:] if e.kind == "yard.braced"]
    assert [e.text.split(";")[0] for e in alone] == ["Braced the fore yard"]


def test_the_trim_line_says_the_yards_on_deck_as_a_clause_and_not_as_a_refusal():
    """Playtest 11's finding 8 (package 31b): with the topgallant masts sent down, "trim
    sails" braced the six yards aloft and then said "Not the fore topgallant yard is sent
    down; the fore royal yard is sent down; ...". The line now reads "Braced six yards to
    the wind, ...; the topgallant and royal yards are on deck." and names a single yard
    on deck or carried away by itself."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    w = make_world(
        7,
        "data/ships/frigate-36.yaml",
        Scenario(wind_from_deg=0, ship_heading_deg=180, gustiness=0, variability=0),
    )
    w.submit("set plain sail")
    w.run(2400)
    w.submit("send down the topgallant masts")
    w.run(2400)
    assert all(w.ship.spars[m].sent_down for m in w.ship.groups["topgallant masts"])
    e = w.submit("trim sails")
    assert e.kind == "sail.trimmed"
    assert e.text.startswith("Braced six yards to the wind, ")
    assert "; the topgallant and royal yards are on deck." in e.text
    assert "Not " not in e.text and "sent down" not in e.text
    yards_started = [s for s in e.data["subjects"] if s in w.ship.spars]
    assert len(yards_started) == 6 and len(e.data["failed_subjects"]) == 6
    w.run(600)
    # one yard carried away and one royal yard on deck, the rest aloft: each by name
    w.submit("sway up the topgallant masts")
    w.run(3000)
    assert not any(w.ship.spars[m].sent_down for m in w.ship.groups["topgallant masts"])
    w.ship.spars["fore.royal.yard"].sent_down = True
    w.ship.spars["main.topgallant.yard"].wrecked = True
    e = w.submit("trim the yards")
    assert e.text.startswith("Braced ten yards to the wind, ")
    assert e.text.endswith(
        "; the fore royal yard is on deck and the main topgallant yard is carried away."
    )


# ---------------------------------------------------------------------------
# Package 44: the trims by a point of sail (the owner's note 25, kept at the regatta)
# ---------------------------------------------------------------------------


def _targets(runner) -> dict[str, float]:
    return {s: p["target_angle"] for e, s, p in runner.started if e == "brace"}


def test_a_point_of_sail_is_trimmed_for_the_wind_it_will_give_not_the_wind_she_has():
    """`trim for the wind large`, `trim to run` and `trim for close hauled` trim every
    yard for the point named, from the true wind and her way now: on a reach the large
    trim braces the yards in from where `trim sails` puts them, the run squares them, and
    close-hauled is the period's trim by level whatever her way (each level in from the
    one below, the after yards sharper)."""
    from freesail.orders.verbs import POINT_TRUE_WIND_DEG

    assert set(POINT_TRUE_WIND_DEG) == {"close hauled", "the wind abeam", "the wind large", "a run"}
    now, now_runner = frigate(70.0)  # a reach on the starboard tack
    handle(now, "trim the yards")
    reach = _targets(now_runner)
    ship, runner = frigate(70.0)
    ship.dyn.u = 3.0
    kind, text, data = handle(ship, "trim for the wind large")
    large = _targets(runner)
    assert data["point"] == "the wind large" and data["awa_deg"] > 90.0
    assert text.startswith("Braced twelve yards for the wind large, the wind to come, ")
    assert all(0.0 <= large[y] < reach[y] for y in reach)
    ship, runner = frigate(70.0)
    handle(ship, "trim to run")
    assert all(abs(v) < 1e-9 for v in _targets(runner).values())
    ship, runner = frigate(110.0)  # well free, and still: close-hauled is braced up by level
    ship.dyn.u = 0.0
    handle(ship, "trim for close hauled")
    close = _targets(runner)
    fore, topsail = close["fore.yard"], close["fore.topsail.yard"]
    assert fore == pytest.approx(ship.spars["fore.yard"].brace_limit)
    assert topsail == pytest.approx(fore - math.radians(2.0))
    assert close["main.yard"] > fore  # the after yards sharper (spec 3b §2.2)


def test_the_point_is_trimmed_on_the_side_of_the_course_the_helm_steers_for():
    """Before the wind (the tack a toss-up) and the helm ordered to bring her to the wind
    abeam: the yards are braced for the side the wind will be on when she is round, not
    the tack she happened to be on."""
    from freesail.ship.parts import HelmMode

    for course, sign in ((90.0, -1.0), (270.0, 1.0)):
        ship, runner = frigate(179.0)  # running, the wind from the north, heading south
        ship.dyn.heading = math.radians(180.0)
        ship.dyn.helm_mode = HelmMode.HEADING
        ship.dyn.target_heading = math.radians(course)
        ship.dyn.u = 3.0
        _kind, _text, data = handle(ship, "trim for the wind abeam")
        assert math.copysign(1.0, data["awa_deg"]) == sign, course
        assert all(math.copysign(1.0, v) == sign for v in _targets(runner).values() if v)


@pytest.mark.parametrize(
    "said",
    ["trim for close-hauled", "trim sails for the wind abeam", "trim for the wind on the quarter"],
)
def test_the_points_other_words_are_taken(said):
    ship, runner = frigate(70.0)
    kind, text, data = handle(ship, said)
    assert data["point"] in ("close hauled", "the wind abeam", "the wind large")


def test_trimmed_for_the_point_in_the_same_breath_she_makes_more_than_by_trim_sails():
    """The regatta's measure in small (TuningNotes, package 44): the frigate in fifteen
    knots from the north, on the wind abeam, ordered to bear away to SE with the trim in
    the same breath; trimmed for the wind large she runs further in the half hour after
    than trimmed for the wind she had, whose yards stay braced for the beam."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    made = {}
    for trim in ("trim sails", "trim for the wind large"):
        w = make_world(
            7,
            "data/ships/frigate-36.yaml",
            Scenario(wind_from_deg=0.0, ship_heading_deg=90.0, gustiness=0.0, variability=0.0),
        )
        w.submit("set plain sail")
        w.run(900)
        w.submit("trim sails")
        w.run(900)
        w.submit("steer SE")
        w.submit(trim)
        x0, y0 = w.ship.dyn.x, w.ship.dyn.y
        w.run(1800)
        se = math.radians(135.0)
        dx, dy = w.ship.dyn.x - x0, w.ship.dyn.y - y0
        made[trim] = (dx * math.sin(se) + dy * math.cos(se)) / units.NAUTICAL_MILE
    assert made["trim for the wind large"] > made["trim sails"] + 0.3, made
