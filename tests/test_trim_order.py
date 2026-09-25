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


def test_trim_the_sheets_sets_fore_and_aft_sails_at_once():
    ship, runner = frigate(60.0)
    for s in ship.sails.values():
        s.sheet_angle = 0.0
    kind, text, data = handle(ship, "trim the sheets")
    assert runner.started == []
    assert kind == "sail.trimmed"
    assert set(data["trimmed_sheets"]) >= {"the mizzen spanker", "the jib"}
    assert ship.sails["mizzen.spanker"].sheet_angle == pytest.approx(units.deg_to_rad(35))
    assert ship.sails["jib"].sheet_angle == pytest.approx(units.deg_to_rad(32))
    assert "trimmed the sheets of the mizzen spanker" in text.lower()


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
