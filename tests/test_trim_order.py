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
    ship, runner = frigate(41.0)
    handle(ship, "trim the yards")
    from freesail.physics.sails import SAIL_CLASSES

    cls = SAIL_CLASSES["square"]
    best = cls.alpha[max(range(len(cls.lift)), key=lambda i: cls.lift[i])]
    chord = units.deg_to_rad(41.0) - best
    yard = ship.spars["fore.topsail.yard"]
    expected = min(math.pi / 2 - max(chord, 0.0), yard.brace_limit)
    got = {s: p["target_angle"] for _, s, p in runner.started}["fore.topsail.yard"]
    assert got == pytest.approx(expected)


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
