"""Practice at the great guns: the marks (practice and resupply, between packages 72 and
73; docs/design/Build-PracticeAndResupply.md §1.5, §1.7, §6, §8.1).

The cask and the notional mark as the action's targets (`action.target_of`, beam-on at any
bearing), the shot that strikes the cask (`hits.resolve_shot`'s first branch, once), a mark
fired on that is no sail (no `_fired_on`, no outlaw, no morale), the cask's drift, its loss
and its abandonment, the practice reading and the sample's idle rows on every path, the
magazine's row in port, and the allowance for exercise said once a month.

Builder 1's battery (the dumb show, the drill, the fire at a mark that sets
`last_practice_tick`) was not merged on the branch these tests were written on: where its
behaviour was wanted they stand a small fake in for it and rely only on the stage-0
signatures, and they hold as well with the battery merged. The reading's words for each
kind as she carries it (the swivels from the cartridge, the one pivot gun singular) and
for the hits at each mark ("struck" at the cask, "on the mark" at the notional), and the
allowance of one and its binding a King's ship of Britain only, are the review's findings.
"""

from __future__ import annotations

import copy
import math
from types import SimpleNamespace

import pytest

from freesail import units
from freesail.api import readings  # noqa: F401 - first: it imports the rows' modules
from freesail.api.action_readings import ACTION_ROWS, _guns, idle_rows
from freesail.api.practice_readings import practice_value
from freesail.combat import action, marks
from freesail.combat import hits as HITS
from freesail.combat import shot as S
from freesail.combat.guns import Battery, Drill, FireMode, Volley, battery_of
from freesail.ship.parts import Charge, Magazine, Wanting
from freesail.world.geo import bearing_and_distance, destination
from tests.test_brains import world_at

FRIGATE = "data/ships/frigate-36.yaml"
CUTTER = "data/ships/cutter.yaml"
SMACK = "data/ships/smack.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"


def frigate():
    """The frigate south of the Lizard at seed 7, the lookout given his first minute."""
    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    return w


def cask_in_sight(w, side="starboard"):
    """A cask over the side (`marks.drop_cask`, as the heave's end does) and the lookout's
    next look, so that the masthead has it."""
    cask = marks.drop_cask(w, side)
    w.run(60)
    assert marks.cask_in_sight(w, cask)
    return cask


def kinds(w, prefix):
    return [e for e in w.log if e.kind.startswith(prefix)]


class NoDraw:
    """A stream that must not be drawn from."""

    def random(self):
        raise AssertionError("a mark drew from the gunnery stream")

    gauss = uniform = random


# -- the targets --------------------------------------------------------------------------


def test_the_cask_is_a_target_by_the_truth_beam_on_and_small():
    w = frigate()
    cask = marks.drop_cask(w, "starboard")
    # not yet made out from the masthead: no target, so no gun lays for it
    assert action.target_of(w, cask.id) is None
    w.run(60)
    t = action.target_of(w, cask.id)
    assert t is not None
    bearing, distance = bearing_and_distance(w.position, cask.position)
    assert t.id == cask.id and t.mark == "cask" and t.words == "the cask"
    assert t.bearing_rad == pytest.approx(math.radians(bearing))
    assert t.range_m == pytest.approx(distance)
    assert t.length_m == marks.CASK_LENGTH_M and t.size == pytest.approx(marks.CASK_SIZE)
    assert t.size == pytest.approx(math.sqrt(1.0 / 40.0))
    assert t.body is cask and t.world is None and t.nation is None
    aspect = S.aspect_of(t.heading_rad, units.wrap_2pi(t.bearing_rad + math.pi))
    assert abs(math.sin(aspect)) == pytest.approx(1.0)
    # gone, it is no target
    cask.gone = "struck"
    assert action.target_of(w, cask.id) is None


@pytest.mark.parametrize("relative_deg", [45.0, 90.0, 135.0, -45.0, -135.0])
def test_the_notional_mark_is_beam_on_at_the_bow_the_beam_and_the_quarter(relative_deg):
    w = frigate()
    w.ship.dyn.heading = math.radians(30.0)
    marks.lay_notional(w, relative_deg, 4 * units.CABLE, "the mark four cables")
    t = action.target_of(w, marks.NOTIONAL_ID)
    assert t is not None and t.mark == "notional" and t.size is None
    assert t.length_m == marks.NOTIONAL_LENGTH_M and t.body is None and t.world is None
    want = units.wrap_2pi(math.radians(30.0 + relative_deg))
    assert t.bearing_rad == pytest.approx(want)
    assert t.range_m == pytest.approx(4 * units.CABLE)
    aspect = S.aspect_of(t.heading_rad, units.wrap_2pi(t.bearing_rad + math.pi))
    assert abs(math.sin(aspect)) == pytest.approx(1.0)
    # the relative bearing the runner reads is the one laid
    assert math.degrees(units.wrap_pi(t.bearing_rad - float(w.ship.heading))) == pytest.approx(
        relative_deg
    )


def test_the_notional_mark_needs_no_position_and_none_is_laid_by_default():
    ship = SimpleNamespace(extra={}, heading=0.0, guns={"x": None})
    plane = SimpleNamespace(ship=ship, position=None)
    assert action.target_of(plane, marks.NOTIONAL_ID) is None  # no practice yet
    marks.lay_notional(plane, -90.0, 3 * units.CABLE, "the mark three cables")
    t = action.target_of(plane, marks.NOTIONAL_ID)
    assert t is not None and t.range_m == pytest.approx(3 * units.CABLE)
    assert t.bearing_rad == pytest.approx(math.radians(270.0))
    # a sail's id keeps today's path, and a bare 'mark' (truth 7-135's) is no mark
    assert not marks.is_mark("mark") and not marks.is_mark("renard") and not marks.is_mark(None)
    assert marks.is_mark("practice:cask-3")


# -- the shot -------------------------------------------------------------------------------


def test_the_first_shot_that_strikes_knocks_the_cask_to_staves_and_draws_nothing():
    w = frigate()
    cask = cask_in_sight(w)
    battery = battery_of(w.ship)
    battery.target, battery.target_words = cask.id, "the cask"
    t = action.target_of(w, cask.id)
    guns = list(w.ship.guns.values())
    tick = int(w.clock.tick)
    seen = HITS.resolve_shot(battery, guns[0], Charge.ROUND, t, high=False, rng=NoDraw(), tick=tick)
    assert seen == []
    assert cask.gone == "struck" and cask.gone_tick == tick
    assert cask.struck_by == guns[0].name and cask.struck_at_m == pytest.approx(t.range_m)
    # a second hit in the tick changes nothing
    again = HITS.resolve_shot(battery, guns[1], Charge.ROUND, t, high=True, rng=NoDraw(), tick=tick)
    assert again == [] and cask.struck_by == guns[0].name
    # the notional mark: nothing struck, nothing drawn
    marks.lay_notional(w, 90.0, 2 * units.CABLE, "the mark two cables")
    n = action.target_of(w, marks.NOTIONAL_ID)
    assert (
        HITS.resolve_shot(battery, guns[0], Charge.ROUND, n, high=False, rng=NoDraw(), tick=1) == []
    )
    # the minute says it once, and the guns have nothing to fire at
    marks.tick(w, battery, tick, minute=False)
    assert not kinds(w, "practice.mark_struck")
    marks.tick(w, battery, tick, minute=True)
    struck = kinds(w, "practice.mark_struck")
    assert [str(e.severity) for e in struck] == ["notable"]
    assert struck[0].text == (
        f"The mark struck by {guns[0].name} at {_cables(t.range_m)} and knocked to staves; "
        "the guns hold their fire for want of a mark."
    )
    assert battery.target is None and battery.target_words == ""
    marks.tick(w, battery, tick + 60, minute=True)
    assert len(kinds(w, "practice.mark_struck")) == 1
    assert "gunnery" not in w.rng.stream_names()


def _cables(m):
    from freesail.world.geo import estimate_words

    return estimate_words(m)


def test_a_mark_fired_on_is_no_sail_no_recognition_no_outlaw_no_morale(monkeypatch):
    """The battery's fire at a mark stood in by a fake of Builder 1's (`last_practice_tick`
    set and not `last_fired_tick`, the volley's `mark` kept, the struck shot resolved): the
    action calls `marks.count_live` and never `_fired_on`, so there is no recognition, no
    outlaw, no witness and no morale."""
    w = frigate()
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    cask = cask_in_sight(w)
    battery = battery_of(w.ship)
    battery.target, battery.target_words = cask.id, "the cask"
    battery.engaged, battery.mode = "starboard", FireMode.AS_THEY_BEAR

    def fake_tick(self, dt, quarters, firer, target, rng, tick, resolve):
        if target is None or tick % 20:
            return
        gun = next(iter(self.ship.guns.values()))
        self.rounds_fired += 1
        gun.fired += 1
        self.last_practice_tick = tick
        outcome = "struck" if self.rounds_fired >= 3 else "over"
        self.volleys.append(Volley(gun.id, Charge.ROUND, outcome, mark=target.mark))
        if outcome == "struck":
            resolve(self, gun, Charge.ROUND, target, high=False, rng=rng, tick=tick)

    fired_on: list = []
    counted: list = []
    monkeypatch.setattr(Battery, "tick", fake_tick)
    monkeypatch.setattr(action, "_fired_on", lambda *a, **k: fired_on.append(a))
    real = marks.count_live
    monkeypatch.setattr(marks, "count_live", lambda world, n: (counted.append(n), real(world, n)))
    w.run(180)
    assert battery.rounds_fired >= 3 and counted and sum(counted) == battery.rounds_fired
    assert fired_on == []
    assert cask.gone == "struck" and len(kinds(w, "practice.mark_struck")) == 1
    assert "outlaw" not in w.ship.extra and "morale" not in w.ship.extra
    for kind in ("action.unrecognised", "action.false_colours", "action.enemy_struck"):
        assert not kinds(w, kind), kind
    assert battery.last_fired_tick is None and battery.target is None


def test_the_battery_at_a_notional_mark_never_calls_fired_on(monkeypatch):
    """Today's battery (stage 0) fires live at the notional mark as at any target: the
    action still keeps the shot from the recognition and the outlaw."""
    w = frigate()
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    fired_on: list = []
    monkeypatch.setattr(action, "_fired_on", lambda *a, **k: fired_on.append(a))
    battery = battery_of(w.ship)
    marks.lay_notional(w, 90.0, 2 * units.CABLE, "the mark two cables on the starboard beam")
    battery.target = marks.NOTIONAL_ID
    battery.engaged, battery.mode = "starboard", FireMode.AS_THEY_BEAR
    w.run(240)
    assert battery.rounds_fired > 0
    assert fired_on == [] and "outlaw" not in w.ship.extra
    assert not kinds(w, "action.unrecognised") and not kinds(w, "action.fired_at")
    assert battery.target_words == "the mark two cables on the starboard beam"


# -- the cask's life ------------------------------------------------------------------------


def test_the_cask_drifts_with_the_stream_and_to_leeward_once_a_minute_and_draws_nothing():
    w = frigate()
    cask = marks.drop_cask(w, "larboard")
    names = w.rng.stream_names()
    before = cask.position
    battery = battery_of(w.ship)
    marks.tick(w, battery, int(w.clock.tick), minute=False)
    assert cask.position == before  # nothing between the minutes
    from freesail.world.sights import greenwich_time

    east, north = w.tide.stream_at(before, greenwich_time(w))
    leeway = marks.CASK_LEEWAY_SHARE * w.wind.base_speed
    toward = w.wind.direction_from + math.pi
    east += leeway * math.sin(toward)
    north += leeway * math.cos(toward)
    marks.tick(w, battery, int(w.clock.tick), minute=True)
    dx, dy = before.offset_to(cask.position)
    assert dx == pytest.approx(east * 60.0, abs=0.05)
    assert dy == pytest.approx(north * 60.0, abs=0.05)
    # with no stream, the westerly alone sets it to the eastward, a fiftieth of its speed
    w.tide = None
    before = cask.position
    marks.tick(w, battery, int(w.clock.tick) + 60, minute=True)
    dx, dy = before.offset_to(cask.position)
    assert dx == pytest.approx(leeway * 60.0 * math.sin(toward), abs=0.05) and dx > 0.0
    assert w.rng.stream_names() == names


def test_the_cask_is_lost_at_three_miles_once_and_the_mark_cleared():
    w = frigate()
    cask = cask_in_sight(w)
    battery = battery_of(w.ship)
    battery.target, battery.target_words = cask.id, "the cask"
    cask.position = destination(w.position, 180.0, 3.1 * units.NAUTICAL_MILE)
    marks.tick(w, battery, int(w.clock.tick), minute=True)
    lost = kinds(w, "practice.mark_lost")
    assert len(lost) == 1 and str(lost[0].severity) == "routine"
    assert lost[0].text == "The mark is lost astern, three miles off."
    assert lost[0].data["gone"] == "lost" and cask.gone == "lost" and cask.gone_said
    assert battery.target is None and battery.target_words == ""
    marks.tick(w, battery, int(w.clock.tick) + 60, minute=True)
    assert len(kinds(w, "practice.mark_lost")) == 1
    assert marks.cask_in_water(w.ship) is None


def test_a_fresh_cask_gives_up_the_one_in_the_water_once():
    w = frigate()
    first = cask_in_sight(w)
    battery = battery_of(w.ship)
    battery.target = first.id
    second = marks.drop_cask(w, "larboard")
    given_up = kinds(w, "practice.mark_lost")
    assert len(given_up) == 1 and given_up[0].data == {"id": first.id, "gone": "abandoned"}
    assert (
        given_up[0].text == "The old mark is given up: a fresh cask goes over the side for another."
    )
    assert first.gone == "abandoned" and battery.target is None
    assert second.id == "practice:cask-2" and marks.practice_of(w.ship).serial == 2
    assert marks.cask_in_water(w.ship) is second
    # from her larboard quarter, six tenths of her length off
    bearing, distance = bearing_and_distance(w.position, second.position)
    relative = units.wrap_pi(math.radians(bearing) - float(w.ship.heading))
    assert math.degrees(relative) == pytest.approx(-135.0, abs=1.0)
    assert distance == pytest.approx(0.6 * w.ship.hull.length, rel=0.05)
    # the cask given up says nothing more
    marks.tick(w, battery, int(w.clock.tick), minute=True)
    assert len(kinds(w, "practice.mark_lost")) == 1


def test_a_world_with_no_practice_does_nothing_in_the_marks_tick():
    w = frigate()
    n = len(w.log)
    marks.tick(w, battery_of(w.ship), int(w.clock.tick), minute=True)
    assert len(w.log) == n and marks.practice_of(w.ship) is None
    assert marks.sightings(w, w.position, None, "day") == []


# -- the readings ---------------------------------------------------------------------------


def test_the_practice_reading_says_none_then_the_drill_the_falls_and_the_mark():
    w = frigate()
    assert practice_value(w)["words"] == "none"
    battery = battery_of(w.ship)
    gid = next(g.id for g in w.ship.guns.values() if g.kind == "long" and g.pounder == 18)
    battery.drill = {
        gid: Drill(
            dumb=3,
            live=2,
            cycles=2,
            total_s=200.0,
            best_s=95.0,
            falls={"2 struck": 1, "2 over": 1, "4 short": 2},
        )
    }
    battery.exercise = "starboard"
    value = practice_value(w)
    assert value["guns"][gid] == {
        "dumb": 3,
        "live": 2,
        "cycles": 2,
        "mean_s": 100.0,
        "best_s": 95.0,
    }
    assert value["falls"] == {"2": {"struck": 1, "over": 1}, "4": {"short": 2}}
    assert value["dumb"] == 3 and value["live"] == 2 and value["exercise"] == "starboard"
    words = value["words"]
    assert words.startswith("exercising the starboard battery in dumb show; 3 rounds in dumb ")
    assert (
        "the long 18-pounders a minute and forty seconds from sponge to point on the mean" in words
    )
    assert "the best a minute and thirty-five seconds" in words
    assert "at the mark at 2 cables 1 struck of 2, at 4 cables 0 struck of 2" in words
    # the guns' row says the dumb show, and its data has `exercise` only while it is set
    guns = _guns(w, None)
    assert "exercising the starboard battery in dumb show" in guns["words"]
    assert guns["exercise"] == "starboard"
    battery.exercise = None
    assert "exercise" not in _guns(w, None)
    # the notional mark engaged
    marks.lay_notional(w, 90.0, 4 * units.CABLE, "the mark four cables on the starboard beam")
    battery.target = marks.NOTIONAL_ID
    mark = practice_value(w)["mark"]
    assert mark["kind"] == "notional" and mark["range_cables"] == 4.0 and mark["engaged"]
    assert "engaged at the mark four cables on the starboard beam" in practice_value(w)["words"]


def test_the_practice_reading_names_each_kind_as_she_carries_it_and_each_mark_its_hits():
    """The pace by the kinds she carries: the privateer's one pivot gun "the long
    12-pounder", her swivels timed "from cartridge to point" (a swivel has no sponge:
    `guns.PHASES`), as the minute's line says them; and the falls by cables summed over
    the marks in the data, a hit at the cask "struck" and one at the notional mark "on
    the mark" in the words, as the minute's line says them (the review's findings: "the
    long 12-pounders", "the half-pounder swivels ... from sponge to point", "3 struck of
    60" at a notional mark)."""
    w = world_at(49.5, -5.5, PRIVATEER)
    w.run(60)
    battery = battery_of(w.ship)
    guns = list(w.ship.guns.values())
    pivot = next(g.id for g in guns if g.place == "pivot")
    swivel = next(g.id for g in guns if g.kind == "swivel")
    carronade = next(g.id for g in guns if g.kind == "carronade")
    battery.drill = {
        pivot: Drill(live=4, cycles=2, total_s=192.0, best_s=96.0, falls={"3 struck notional": 1}),
        swivel: Drill(dumb=2, cycles=2, total_s=62.0, best_s=31.0),
        carronade: Drill(
            live=4,
            cycles=1,
            total_s=52.0,
            best_s=52.0,
            falls={"2 struck": 1, "2 wide": 1, "2 struck notional": 2, "3 over notional": 3},
        ),
    }
    value = practice_value(w)
    words = value["words"]
    assert (
        "the long 12-pounder a minute and thirty-six seconds from sponge to point on the mean, "
        "the best a minute and thirty-six seconds" in words
    ), words
    assert (
        "the half-pounder swivels thirty-one seconds from cartridge to point on the mean, the "
        "best thirty-one seconds" in words
    ), words
    assert "the 12-pounder carronades fifty-two seconds from sponge to point" in words
    assert "long 12-pounders" not in words and "swivels thirty-one seconds from sponge" not in words
    assert value["falls"] == {"2": {"struck": 3, "wide": 1}, "3": {"struck": 1, "over": 3}}
    assert (
        "at the mark at 2 cables 1 struck and 2 on the mark of 4, at 3 cables 1 on the mark "
        "of 4" in words
    ), words


def test_the_practice_reading_names_the_cask_in_sight_and_gone():
    w = frigate()
    cask = cask_in_sight(w)
    mark = practice_value(w)["mark"]
    assert mark["kind"] == "cask" and mark["in_sight"] and mark["gone"] == ""
    assert mark["bearing"] and mark["range_cables"] is not None
    assert practice_value(w)["words"].startswith("the cask ")
    cask.gone = "struck"
    assert practice_value(w)["words"] == "the last cask knocked to staves"


def test_a_ship_without_guns_has_no_practice():
    w = world_at(50.0, -5.0, SMACK)
    assert practice_value(w) is None
    assert w.readings.words("practice") == "she carries no guns"


def _sampled(w) -> set[str]:
    return set(idle_rows(w))


def test_the_practice_row_is_idle_on_every_path_of_the_actions_rows():
    w = frigate()
    battery = battery_of(w.ship)
    # nothing afoot: every action row idle, and the practice's
    assert set(ACTION_ROWS) | {"practice"} <= _sampled(w)
    # at quarters: the action's rows ride, the practice's does not
    w.submit("beat to quarters")
    w.run(2)
    assert "practice" in _sampled(w) and "damage" not in _sampled(w)
    # a sail engaged, the colours struck, damage, men hurt: each the action's early return
    w.ship.extra["quarters"].stand_down()
    battery.target = "some-sail"
    assert "practice" in _sampled(w) and "enemy" not in _sampled(w)
    battery.target = None
    w.ship.extra["struck"] = 1
    assert "practice" in _sampled(w)
    del w.ship.extra["struck"]
    HITS.damage_of(w.ship).hits = 1
    assert "practice" in _sampled(w)
    HITS.damage_of(w.ship).hits = 0
    w.ship.extra["crew"].sailors[0].hurt = "wounded"
    assert "practice" in _sampled(w)
    w.ship.extra["crew"].sailors[0].hurt = None
    assert "practice" in _sampled(w)
    # exercising, a mark engaged, a cask in the water: the practice rides
    battery.exercise = "both"
    assert "practice" not in _sampled(w)
    battery.exercise = None
    battery.target = marks.NOTIONAL_ID
    assert "practice" not in _sampled(w)
    battery.target = None
    assert "practice" in _sampled(w)
    marks.drop_cask(w, "starboard")
    assert "practice" not in _sampled(w)


class ShortMagazine(Magazine):
    """A magazine short of its establishment (Builder 1's `wanting` stood in for)."""

    def wanting(self) -> Wanting:
        return Wanting(200.0, 2, {18.0: {"round": 40}})


def test_the_magazine_row_rides_in_port_while_she_wants_powder_or_shot(monkeypatch):
    w = frigate()
    assert "magazine" in _sampled(w)
    # not in port: idle, whatever she wants
    w.ship.extra["magazine"] = ShortMagazine(layout=2)
    assert w.ports.in_port() is None and "magazine" in _sampled(w)
    # in port and short: it rides; in port and complete: idle
    monkeypatch.setattr(w.ports, "in_port", lambda: object())
    assert "magazine" not in _sampled(w)
    w.ship.extra["magazine"] = Magazine(layout=2)
    assert "magazine" in _sampled(w)
    # in port with no magazine made yet: hers is the fit's, complete, and none is made here
    del w.ship.extra["magazine"]
    assert "magazine" in _sampled(w) and "magazine" not in w.ship.extra


# -- the allowance --------------------------------------------------------------------------


def _with_allowance(w, n):
    fit = copy.copy(w.ship.fit_spec)
    fit.exercise_charges = n  # Builder 1's FitSpec field, stood in on a copy
    w.ship.fit_spec = fit


def test_the_allowance_for_exercise_is_said_once_a_month_beyond_it():
    w = frigate()
    _with_allowance(w, 6)
    w.scenario.papers = {"service": "kings"}
    mag = Magazine(layout=2)
    w.ship.extra["magazine"] = mag
    marks.count_live(w, 6)
    assert not kinds(w, "practice.beyond_allowance")
    marks.count_live(w, 1)
    marks.count_live(w, 3)
    beyond = kinds(w, "practice.beyond_allowance")
    assert len(beyond) == 1 and str(beyond[0].severity) == "notable"
    assert beyond[0].text == (
        "Beyond the allowance for exercise this month (six charges by the Regulations, the "
        "Gunner, Art. XXI): the powder past it is spent on the captain's word, and the "
        "gunner's account keeps it."
    )
    assert beyond[0].data == {"month": "1805-06", "rounds": 7, "allowance": 6}
    p = marks.practice_of(w.ship)
    assert p.month == "1805-06" and p.month_rounds == 10 and p.said_beyond == "1805-06"
    assert len(mag.account) == 1 and "beyond the allowance of six charges" in mag.account[0][1]
    # the reading counts the month
    month = practice_value(w)["month"]
    assert month == {"month": "1805-06", "rounds": 10, "allowance": 6, "beyond": 4}
    # a month past: the count begins again, and the line is said again once
    p.month, p.said_beyond = "1805-05", "1805-05"
    marks.count_live(w, 7)
    assert len(kinds(w, "practice.beyond_allowance")) == 2 and p.month_rounds == 7


def test_the_kings_cutters_allowance_of_one_is_one_charge():
    """The King's cutter's carronades fit allows one charge a month (decision 23): the
    line, the gunner's account and its paper say "one charge" (the review's finding: "one
    charges")."""
    w = world_at(49.5, -5.5, CUTTER)
    w.run(60)
    w.scenario.papers = {"service": "kings"}
    assert w.ship.fit_spec.exercise_charges == 1
    marks.count_live(w, 2)
    (beyond,) = kinds(w, "practice.beyond_allowance")
    assert beyond.text == (
        "Beyond the allowance for exercise this month (one charge by the Regulations, the "
        "Gunner, Art. XXI): the powder past it is spent on the captain's word, and the "
        "gunner's account keeps it."
    )
    from freesail.ship.parts import magazine

    words = (
        "powder for exercise beyond the allowance of one charge this month, on the captain's word"
    )
    assert magazine(w.ship).account[-1][1] == words
    (written,) = kinds(w, "paper.written")
    assert words in written.text and "charges" not in written.text


def test_the_allowance_binds_a_kings_ship_of_britain_alone():
    """The allowance is the Admiralty's Regulations' (the Gunner, Art. XXI): a man of war
    of another nation, a King's ship by her papers or her wardroom, keeps none, and the
    reading has no month (the review's finding: an American frigate said "beyond the
    allowance ... six charges by the Regulations")."""
    w = frigate()
    _with_allowance(w, 6)
    w.scenario.papers = {"service": "kings"}
    w.scenario.nation = "united-states"
    marks.count_live(w, 20)
    assert marks.practice_of(w.ship) is None and not kinds(w, "practice.beyond_allowance")
    assert practice_value(w)["month"] is None
    w.scenario.nation = "britain"
    marks.count_live(w, 20)
    assert len(kinds(w, "practice.beyond_allowance")) == 1
    assert practice_value(w)["month"]["rounds"] == 20


def test_the_documents_say_what_practice_and_resupply_built():
    """The lead's documents of the build design's §7.2, which the merge had left undone (the
    review's finding): the tuning notes' entry with an old game's two caveats (§1.1 step 3
    and §9: no powder reserve; a once-said magazine line said once more), the spec's "as
    built", the work packages' entry, Harness.md's `practice` row with every event word of
    this work, and the squadrons design's pace floors at truths 7-159 and 7-160 (7-161 and
    7-162 are this work's)."""
    from pathlib import Path

    from freesail.api.readings import EVENTS

    root = Path(__file__).resolve().parents[1]

    def read(path: str) -> str:
        return (root / path).read_text(encoding="utf-8")

    tuning = read("docs/dev/TuningNotes.md")
    heading = (
        "## Between packages 72 and 73: practice at the great guns, and powder and shot taken in"
    )
    entry = tuning[tuning.index(heading) :]
    assert "**It has no powder reserve.**" in entry
    assert "**It may say a once-said magazine line once more.**" in entry
    spec = read("docs/TechnicalSpec-M7.md")
    assert "**As built (practice and resupply, between packages 72 and 73).**" in spec
    assert "### Practice and resupply as merged" in read("docs/dev/M7-WorkPackages.md")
    harness = read("docs/agents/Harness.md")
    start = harness.index("## 21g. Practice at the great guns")  # 21f before 73 (86)
    section = " ".join(harness[start : harness.index("\n## 22.", start)].split())
    assert "`practice`" in section and "`magazine`" in section
    ours = ("guns.filling", "guns.filled", "guns.powder_out", "ordnance.", "practice.")
    words = [w for w, spec in EVENTS.items() if spec.kind.startswith(ours)]
    assert len(words) == 13, words
    assert not [w for w in words if f"`{w}`" not in section]
    squadrons = read("docs/design/Design-Squadrons.md")
    assert "truths 7-161 and 7-162" not in squadrons
    assert "truths 7-159 and 7-160" in squadrons


def test_the_allowance_is_a_kings_ships_and_counts_nothing_without_one():
    w = frigate()
    w.scenario.papers = {"service": "merchant"}
    _with_allowance(w, 6)
    marks.count_live(w, 20)
    assert marks.practice_of(w.ship) is None and not kinds(w, "practice.beyond_allowance")
    w.scenario.papers = {"service": "kings"}
    _with_allowance(w, 0)
    marks.count_live(w, 20)
    assert marks.practice_of(w.ship) is None
    assert practice_value(w)["month"] is None
