"""Dumb show, the drill, and the shot at a mark (practice and resupply, between packages 72
and 73; docs/design/Build-PracticeAndResupply.md §1.6, §6, §8.1).

The guns exercised in dumb show are served through the exercise's phases at the action's
pace with nothing taken from the magazine and nothing fired but by name; a loaded gun is
exercised from the run out to the point and keeps its charge; each gun's drill is counted.
A shot at a mark is laid and drawn as at a ship, with the mark's own size term, and counted
as practice and never as firing on a sail; a shotted gun fired with no mark sends its shot
into the sea, and every minute without one keeps today's words.
"""

from __future__ import annotations

import copy
import math
import random
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.combat import shot as S
from freesail.combat.action import _firer
from freesail.combat.guns import Battery, FireMode, Target, Volley, battery_of
from freesail.core.world import Scenario
from freesail.crew.model import number_words
from freesail.crew.quarters import quarters_of
from freesail.ship.loader import load_ship
from freesail.ship.parts import Charge, magazine

SEED = 7
CUTTER = "data/ships/cutter.yaml"


def _world():
    """The action truths' scenario (tests/test_known_truths.py `_action_scenario`)."""
    return make_world(
        SEED,
        CUTTER,
        Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=270.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 49.8, "lon_deg": -5.3},
            region="channel-west",
            ports=["falmouth", "plymouth", "brest"],
            nation="britain",
            ship_heading_deg=180.0,
            ship_speed_kn=0.0,
        ),
    )


def _store(mag) -> tuple:
    return copy.deepcopy((mag.cartridges, mag.shot, mag.fired, mag.powder_lb))


def test_dumb_show_takes_nothing_fires_nothing_and_opens_no_stream():
    """Given at quarters before the guns are cast loose, so that every cycle starts empty:
    the starboard battery served round and round, the larboard guns left alone, the
    magazine as it was, no round fired, no `gunnery` stream, no `action.fired`, and the
    minute's line `practice.exercise`."""
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    battery = battery_of(w.ship)
    mag = magazine(w.ship)
    start = _store(mag)
    assert battery.begin_exercise("starboard") == []  # nothing loaded: the guns secured
    w.submit("cast loose the guns")
    w.run(10 * 60)
    assert _store(mag) == start and not mag.short
    assert battery.rounds_fired == 0 and "gunnery" not in w.rng.stream_names()
    assert not [e for e in w.log if e.kind == "action.fired"]
    drill = battery.drill or {}
    for g in w.ship.guns.values():
        assert not g.loaded
        if g.side == "starboard":
            assert drill[g.id].dumb >= 3 and drill[g.id].live == 0, g.id
            assert drill[g.id].cycles == drill[g.id].dumb
        else:
            assert g.id not in drill and not g.run_out and not g.primed
    lines = [e for e in w.log if e.kind == "practice.exercise"]
    assert lines and all(
        e.text.startswith("Exercising the starboard battery in dumb show: ") for e in lines
    )
    assert sum(e.data["rounds"] for e in lines) == sum(d.dumb for d in drill.values())
    quick = [e for e in lines if "quickest" in e.data]
    assert quick and quick[0].text.endswith(" from sponge to point.")
    assert all(e.data["exercise"] == "starboard" for e in lines)
    battery.end_exercise()
    assert battery.exercise is None
    for g in w.ship.guns.values():
        assert not g.run_out and not g.primed and battery.services[g.id].idle


def test_a_side_dropped_from_the_exercise_is_left_as_cease_exercising_leaves_its_guns():
    """`exercise both batteries`, then the starboard battery alone, then the larboard: each
    side dropped is left as `end_exercise` leaves its guns, the empty ones run in, unprimed
    and their dumb rounds given up, so that once the exercise is over every gun's first
    cycle takes its cartridge and no gun is run out or primed with no charge in it (the
    review's finding: an empty larboard gun was left run out and primed, worked its
    half-done round on with no charge after `cease exercising`, and loaded only at its
    second cycle)."""
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    battery = battery_of(w.ship)
    battery.begin_exercise("both")
    w.submit("cast loose the guns")
    w.run(150)

    def side(name):
        return [g for g in w.ship.guns.values() if g.side == name]

    def left_as_ceased(guns):
        for g in guns:
            assert not g.loaded and not g.run_out and not g.primed, g.id
            assert battery.services[g.id].idle and battery.services[g.id].began_tick is None

    assert [g.id for g in side("larboard") if not battery.services[g.id].idle]  # mid-round
    battery.begin_exercise("starboard")
    left_as_ceased(side("larboard"))
    w.run(150)
    assert [g.id for g in side("starboard") if not battery.services[g.id].idle]
    battery.begin_exercise("larboard")
    left_as_ceased(side("starboard"))
    w.run(150)
    battery.end_exercise()
    left_as_ceased(w.ship.guns.values())
    taken = {}
    for _ in range(400):
        w.run(1)
        for g in w.ship.guns.values():
            if g.loaded:
                taken.setdefault(g.id, w.clock.tick)
            else:
                assert not g.run_out and not g.primed, g.id  # never worked empty
    assert set(taken) == set(w.ship.guns)


def test_a_loaded_gun_is_exercised_from_the_run_out_to_the_point_and_keeps_its_charge():
    """Shotted and run out (the usual state at sea): exercised, each starboard gun is run
    in and out and pointed with its charge in it, untimed; the magazine untouched. A gun
    fired by name still fires, and with no mark its shot goes into the sea."""
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(400)
    battery = battery_of(w.ship)
    mag = magazine(w.ship)
    assert all(battery.ready(g) and g.loaded is Charge.ROUND for g in w.ship.guns.values())
    start = _store(mag)
    filled = mag.filled_by_gunner
    named = battery.begin_exercise("starboard")
    assert sorted(named) == ["No. 1 starboard gun", "No. 2 starboard gun", "No. 3 starboard gun"]
    timed_before = {gid: d.cycles for gid, d in (battery.drill or {}).items()}
    w.run(5 * 60)
    # nothing taken: the gunner's filling of the six cartridges loaded before is all
    by_gunner = mag.filled_by_gunner - filled
    cartridges, shot, fired, powder = start
    assert mag.shot == shot and mag.fired == fired and battery.rounds_fired == 0
    assert mag.cartridges == {k: n + by_gunner for k, n in cartridges.items()}
    assert mag.powder_lb == powder - by_gunner * 1.0
    for g in w.ship.guns.values():
        assert g.loaded is Charge.ROUND and g.primed, g.id
        if g.side == "starboard":
            d = battery.drill[g.id]
            assert d.dumb >= 3 and d.cycles == timed_before.get(g.id, 0), g.id
    assert not [e for e in w.log if e.kind == "action.fired"]
    # fired by name while exercising: the one gun fires, into the sea, drawing nothing
    battery.single = ["gun.1.starboard"]
    w.run(120)
    assert battery.rounds_fired == 1 and w.ship.guns["gun.1.starboard"].fired == 1
    fired = [e for e in w.log if e.kind == "action.fired"]
    assert [e.text for e in fired] == ["Fired one gun, the shot into the sea."]
    assert fired[0].data["sea"] == 1 and fired[0].data["fired"] == 1
    assert "gunnery" not in w.rng.stream_names()
    assert battery.drill["gun.1.starboard"].live == 1


def _first_cycles(exercise: bool) -> dict[str, float]:
    """Each gun's first full cycle from the sponge to the point, in seconds, as the guns
    are cast loose at quarters: loaded live, or in dumb show on both sides (so that each
    pair's crew serves both its guns either way)."""
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    battery = battery_of(w.ship)
    if exercise:
        battery.begin_exercise("both")
    w.submit("cast loose the guns")
    first: dict[str, float] = {}
    for _ in range(400):
        w.run(1)
        for gid, d in (battery.drill or {}).items():
            if d.cycles and gid not in first:
                first[gid] = d.total_s
        if len(first) == len(w.ship.guns):
            break
    return first


def test_dumb_show_serves_the_guns_at_the_actions_pace_and_the_drill_is_timed():
    """The same crews at the same guns: the first cycle from the sponge to the point takes
    the same seconds in dumb show as loading live (the live gun is ready, and fires as it
    bears, at the point)."""
    live, dumb = _first_cycles(False), _first_cycles(True)
    assert set(live) == set(dumb) and len(live) == 6
    assert live == dumb
    for s in live.values():
        assert 30.0 <= s <= 300.0


def test_the_drill_keeps_its_best_and_its_mean():
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    battery = battery_of(w.ship)
    battery.begin_exercise("starboard")
    w.submit("cast loose the guns")
    w.run(15 * 60)
    for gid, d in battery.drill.items():
        assert d.cycles >= 3 and d.best_s is not None
        assert d.best_s <= d.total_s / d.cycles, gid
        assert d.falls == {} and d.live == 0
    assert battery.drill_of("gun.1.starboard") is battery.drill["gun.1.starboard"]


# -- the minute's words -------------------------------------------------------------------


def _old_minute_line(volleys: list[Volley], target_words: str, target: str | None):
    """Today's `Battery.minute_line` (combat/guns.py at 4a12e97), for the minutes with no
    shot into the sea and none at a mark."""
    n = len(volleys)
    struck = sum(1 for v in volleys if v.outcome == "struck")
    short = sum(1 for v in volleys if v.outcome == "short")
    over = sum(1 for v in volleys if v.outcome == "over")
    wide = sum(1 for v in volleys if v.outcome == "wide")
    blank = sum(1 for v in volleys if v.outcome in ("blank", "across her bows"))
    seen = [w for v in volleys for w in v.seen]
    at = f" at {target_words}" if target_words else ""
    if n == blank:
        across = any(v.outcome == "across her bows" for v in volleys)
        text = (
            f"Fired {number_words(n)} gun{'s' if n != 1 else ''}"
            + (" across her bows" if across else "")
            + ", a blank charge."
        )
    else:
        fell = []
        if struck:
            fell.append(f"{number_words(struck)} struck her")
        if short:
            fell.append(f"{number_words(short)} fell short")
        if over:
            fell.append(f"{number_words(over)} over")
        if wide:
            fell.append(f"{number_words(wide)} wide")
        across = sum(1 for v in volleys if v.outcome == "across her bows")
        if across:
            fell.append(f"{number_words(across)} across her bows")
        if blank - across:
            fell.append(f"{number_words(blank - across)} a blank charge")
        said = ", ".join(fell[:-1]) + " and " + fell[-1] if len(fell) > 1 else "".join(fell)
        text = f"{number_words(n).capitalize()} shot{at}: {said}."
        if seen:
            text += " " + " ".join(seen)
    data = {
        "fired": n,
        "struck": struck,
        "short": short,
        "over": over,
        "wide": wide,
        "target": target,
        "guns": [v.gun_id for v in volleys],
    }
    return text, data


def _volleys(*outcomes: str, mark: str = "") -> list[Volley]:
    return [
        Volley(f"gun.{i + 1}.starboard", Charge.ROUND, o, mark=mark) for i, o in enumerate(outcomes)
    ]


@pytest.mark.parametrize(
    "outcomes",
    [
        ("struck",),
        ("struck", "short", "over", "wide"),
        ("over", "over", "wide"),
        ("blank",),
        ("across her bows",),
        ("blank", "blank", "across her bows"),
        ("struck", "blank"),
        ("short", "across her bows", "blank"),
    ],
)
def test_a_minute_with_no_shot_into_the_sea_keeps_todays_words_and_data(outcomes):
    battery = Battery(load_ship(CUTTER))
    battery.target, battery.target_words = "v7", "a brig"
    battery.volleys = _volleys(*outcomes)
    if "struck" in outcomes:
        battery.volleys[0].seen = ["Her main topmast comes down."]
    expected = _old_minute_line(copy.deepcopy(battery.volleys), "a brig", "v7")
    assert battery.minute_line(60) == expected


def test_the_minutes_words_at_a_mark_and_into_the_sea():
    battery = Battery(load_ship(CUTTER))
    battery.target, battery.target_words = "practice:cask-1", "the cask"
    battery.volleys = _volleys("struck", "over", mark="cask")
    text, data = battery.minute_line(60)
    assert text == "Two shot at the cask: one struck the mark and one over."
    assert data["mark"] == "cask" and data["struck"] == 1 and "sea" not in data
    battery.target = "practice:notional"
    battery.target_words = "the mark four cables on the starboard beam"
    battery.volleys = _volleys("struck", "struck", "short", mark="notional")
    text, data = battery.minute_line(120)
    assert text == (
        "Three shot at the mark four cables on the starboard beam: two on the mark and one "
        "fell short."
    )
    assert data["mark"] == "notional" and data["struck"] == 2
    battery.target, battery.target_words = None, ""
    battery.volleys = _volleys("into the sea")
    text, data = battery.minute_line(180)
    assert text == "Fired one gun, the shot into the sea."
    assert data == {
        "fired": 1,
        "struck": 0,
        "short": 0,
        "over": 0,
        "wide": 0,
        "target": None,
        "guns": ["gun.1.starboard"],
        "sea": 1,
    }
    battery.volleys = _volleys("into the sea", "into the sea")
    assert battery.minute_line(240)[0] == "Fired two guns, the shot into the sea."
    battery.volleys = _volleys("blank", "into the sea")
    assert battery.minute_line(300)[0] == "Two shot: one a blank charge and one into the sea."
    battery.target, battery.target_words = "v7", "a brig"
    battery.volleys = _volleys("struck", "into the sea")
    text, data = battery.minute_line(360)
    assert text == "Two shot at a brig: one struck her and one into the sea."
    assert data["sea"] == 1 and "mark" not in data


# -- the hit chance's size, and the shot at a mark ------------------------------------------


def _old_hit_chance(range_m, b, reach_m, *, target_length_m, aspect_rad, aim, scatter_deg):
    """Today's `shot.hit_chance` (combat/shot.py at 4a12e97)."""
    if range_m <= 0.0 or reach_m <= 0.0:
        return 0.0
    if range_m > reach_m * 1.05 or range_m > b.random_m:
        return 0.0
    r = range_m / b.point_blank_m
    if r <= 0.25:
        base = 0.9
    elif r <= 1.0:
        base = 0.9 - 0.4 * (r - 0.25) / 0.75
    elif r <= 2.0:
        base = 0.5 - 0.3 * (r - 1.0)
    else:
        rmax = max(b.random_m / b.point_blank_m, 2.5)
        base = max(0.03, 0.2 * (1.0 - (r - 2.0) / (rmax - 2.0)))
    size = min(1.3, max(0.5, math.sqrt(max(target_length_m, 5.0) / 40.0)))
    aspect = 0.6 + 0.4 * abs(math.sin(aspect_rad))
    quality = min(1.2, max(0.6, aim))
    steady = 1.0 / (1.0 + 0.05 * max(0.0, scatter_deg) * max(r, 0.5))
    return min(0.98, base * size * aspect * quality * steady)


def test_the_hit_chance_with_no_size_is_todays_and_a_size_replaces_the_hulls():
    cases = 0
    for kind, pounder in (("long", 18), ("long", 3), ("carronade", 32), ("carronade", 12)):
        b = S.ballistics_of(kind, pounder)
        for range_m in (20.0, 60.0, 150.0, 300.0, 600.0, 1200.0, 1900.0):
            for length in (1.0, 8.0, 20.0, 45.0, 70.0):
                for aspect in (0.0, 0.7, math.pi / 2):
                    for aim, scatter in ((0.8, 0.0), (1.1, 3.5)):
                        reach = range_m * 1.02
                        kw = dict(
                            target_length_m=length,
                            aspect_rad=aspect,
                            aim=aim,
                            scatter_deg=scatter,
                        )
                        today = _old_hit_chance(range_m, b, reach, **kw)
                        assert S.hit_chance(range_m, b, reach, **kw) == today
                        assert S.hit_chance(range_m, b, reach, size=None, **kw) == today
                        cases += 1
    assert cases == 4 * 7 * 5 * 3 * 2
    b = S.ballistics_of("long", 18)
    kw = dict(target_length_m=1.0, aspect_rad=math.pi / 2, aim=1.0, scatter_deg=0.0)
    hull = S.hit_chance(300.0, b, 310.0, **kw)  # the hull's floor: 0.5
    cask = S.hit_chance(300.0, b, 310.0, size=math.sqrt(1.0 / 40.0), **kw)
    assert cask == pytest.approx(hull * math.sqrt(1.0 / 40.0) / 0.5)


def _guns_ready_at_a_notional_mark():
    w = _world()
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    ship = w.ship
    battery = battery_of(ship)
    battery.engaged = "starboard"
    battery.mode = FireMode.AS_THEY_BEAR
    battery.target = "practice:notional"
    battery.target_words = "the mark two cables on the starboard beam"
    bearing = units.wrap_2pi(float(ship.heading) + math.pi / 2.0)
    mark = Target(
        id="practice:notional",
        words="the mark two cables on the starboard beam",
        bearing_rad=bearing,
        range_m=2.0 * units.CABLE,
        heading_rad=units.wrap_2pi(bearing + math.pi / 2.0),
        length_m=20.0,
        heel_deg=0.0,
        nation=None,
        body=None,
        world=None,
        mark="notional",
    )
    return w, battery, mark


def test_a_shot_at_a_mark_is_practice_and_never_firing_on_a_sail():
    """The battery's own cycle at a notional mark two cables abeam: the guns fire as they
    bear, the hits are handed to `resolve` as at a ship, and the minute's line says 'on the
    mark'; `last_fired_tick` (morale's engagement) and `opened_fire_at` are untouched, and
    the falls are counted by cables in each gun's drill."""
    w, battery, mark = _guns_ready_at_a_notional_mark()
    assert battery.last_fired_tick is None and battery.opened_fire_at == {}
    q = quarters_of(w.ship)
    rng = random.Random(7)
    resolved: list[str] = []

    def resolve(b, gun, charge, target, high, rng, tick):
        resolved.append(target.id)
        return []

    lines = []
    for tick in range(1, 6 * 60 + 1):
        battery.tick(1.0, q, _firer(w, w.ship), mark, rng, tick, resolve)
        if tick % 60 == 0:
            line = battery.minute_line(tick)
            if line is not None:
                lines.append(line)
    assert battery.rounds_fired >= 3
    assert battery.last_fired_tick is None and battery.last_practice_tick is not None
    assert battery.opened_fire_at == {}
    assert lines and all(data["mark"] == "notional" for _, data in lines)
    struck = sum(data["struck"] for _, data in lines)
    assert struck == len(resolved) and set(resolved) <= {"practice:notional"}
    if struck:
        assert any(" on the mark" in text for text, _ in lines)
    assert not any("struck her" in text for text, _ in lines)
    falls = {}
    for d in battery.drill.values():
        for k, n in d.falls.items():
            falls[k] = falls.get(k, 0) + n
            assert k.split()[0] == "2" and k.endswith(" notional"), k
    assert sum(falls.values()) == battery.rounds_fired
    assert sum(d.live for d in battery.drill.values()) == battery.rounds_fired


def test_a_fall_at_the_cask_within_half_a_cable_is_at_a_cable():
    """The falls are by whole cables and a cable at the least, as the deck estimates a
    range (`geo.estimate_words`): a cask at 23 m, struck or missed, is "at a cable" in the
    struck line and in the drill alike (the review's finding: its falls were filed at "0"
    cables and the reading said "at 0 cables"); a fall at the cask is unmarked."""
    from freesail.combat.marks import CASK_LENGTH_M, CASK_SIZE

    w, battery, notional = _guns_ready_at_a_notional_mark()
    battery.target, battery.target_words = "practice:cask-1", "the cask"
    cask = Target(
        id="practice:cask-1",
        words="the cask",
        bearing_rad=notional.bearing_rad,
        range_m=23.0,
        heading_rad=notional.heading_rad,
        length_m=CASK_LENGTH_M,
        heel_deg=0.0,
        nation=None,
        body=None,
        world=None,
        mark="cask",
        size=CASK_SIZE,
    )
    q = quarters_of(w.ship)
    rng = random.Random(7)
    for tick in range(1, 3 * 60 + 1):
        battery.tick(1.0, q, _firer(w, w.ship), cask, rng, tick, lambda *a, **k: [])
    keys = {k for d in battery.drill.values() for k in d.falls}
    assert keys and all(k.split()[0] == "1" and len(k.split()) == 2 for k in keys), keys
