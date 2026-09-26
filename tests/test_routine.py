"""The watch routine: watch changes, all hands and piping down, fatigue (spec M3 §4; package 18)."""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

import pytest

from freesail.api.session import make_world
from freesail.core.clock import Clock
from freesail.core.rng import Rng
from freesail.core.world import Scenario
from freesail.crew import bill
from freesail.crew import routine as routine_module
from freesail.crew.model import TOPS, Crew, Station, Watch
from freesail.crew.muster import muster
from freesail.crew.routine import (
    ALL_HANDS_DELAY_S,
    FATIGUE_ALL_HANDS_AT_NIGHT,
    FATIGUE_ASLEEP_BELOW,
    FATIGUE_AT_WORK_ALOFT,
    FATIGUE_AT_WORK_ON_DECK,
    FATIGUE_BELOW_BY_DAY,
    FATIGUE_ON_DECK_IDLE,
    Routine,
    is_night,
)
from freesail.ship.loader import load_ship

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = ROOT / "data" / "ships" / "frigate-36.yaml"
SCHOONER = ROOT / "data" / "ships" / "topsail-schooner.yaml"
DAY = datetime(1805, 6, 1)  # the default scenario's first day: larboard has the middle watch

# The crew factor's weight on fatigue (spec M3 §3.3; package 17 owns the constant).
FATIGUE_WEIGHT = 0.5


def _crew(path: Path = FRIGATE, seed: int = 7) -> Crew:
    ship = load_ship(path)
    return muster(ship.spec.crew, Rng(seed).stream("muster"), ship_name=ship.name)


def _at(when: datetime) -> tuple[Crew, Clock, Routine]:
    crew = _crew()
    clock = Clock(when)
    return crew, clock, Routine(crew, clock)


def _run(clock: Clock, routine: Routine, seconds: int) -> list[tuple[datetime, tuple]]:
    """Tick the clock and the routine as the World does; the notes with their times."""
    notes = []
    for _ in range(seconds):
        clock.advance()
        notes.extend((clock.ship_time, n) for n in routine.tick(None, 1.0))
    return notes


def _hands(crew: Crew) -> list:
    return [s for s in crew.sailors if s.station is not Station.QUARTERDECK]


# ---------------------------------------------------------------------------
# a day's watch changes and the idlers' hours
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def a_day():
    """The frigate's company through a whole day from midnight, and into the next."""
    crew, clock, routine = _at(DAY)
    deck = {}  # hands on deck a minute after each hour
    notes = []
    for hour in range(25):
        notes += _run(clock, routine, 60)
        deck[hour] = len(crew.on_deck(clock))
        notes += _run(clock, routine, 3540)
    return crew, notes, deck


EXPECTED_RELIEFS = [
    # (hour, bells, relief): the watches alternate through the day's seven watches, so the
    # dog watches turn the rotation over: larboard had last night's middle watch, starboard
    # has tonight's, as bill.py counts them.
    (4, "Eight", "starboard"),  # morning
    (8, "Eight", "larboard"),  # forenoon
    (12, "Eight", "starboard"),  # afternoon
    (16, "Eight", "larboard"),  # first dog
    (18, "Four", "starboard"),  # last dog: four bells at six in the evening
    (20, "Eight", "larboard"),  # first
    (24, "Eight", "starboard"),  # the next day's middle watch
]


def test_a_days_watch_changes_with_the_dog_watches(a_day):
    _, notes, _ = a_day
    reliefs = [(t, n) for t, n in notes if n[1] == "watch.relieved"]
    assert len(reliefs) == 7
    for (t, note), (hour, bells, relief) in zip(reliefs, EXPECTED_RELIEFS, strict=True):
        assert t == DAY + timedelta(hours=hour)
        severity, kind, text, subject, data = note
        assert severity == "routine" and subject is None
        assert text == f"{bells} bells. The {relief} watch relieved the deck."
        assert data["relief"] == relief == bill.watch_on_duty(t).value
        assert data["relieved"] == bill.watch_below(Watch(relief)).value
    names = [n[4]["watch"] for _, n in reliefs]
    assert names == [
        "Morning watch",
        "Forenoon watch",
        "Afternoon watch",
        "First dog watch",
        "Last dog watch",
        "First watch",
        "Middle watch",
    ]


def test_the_relief_is_on_deck_and_the_relieved_below(a_day):
    crew, _, deck = a_day
    idlers = len(crew.by_station[Station.IDLERS])
    for hour in range(25):
        t = DAY + timedelta(hours=hour, minutes=1)
        watch = len(crew.by_watch[bill.watch_on_duty(t)])
        assert deck[hour] == watch + (idlers if 6 <= t.hour < 20 else 0), hour


def test_the_idlers_are_up_at_six_and_piped_down_at_eight(a_day):
    crew, notes, _ = a_day
    lines = [(t, n[1], n[2]) for t, n in notes if n[1].startswith("crew.idlers")]
    assert lines == [
        (DAY.replace(hour=6), "crew.idlers_up", "Idlers up."),
        (DAY.replace(hour=20), "crew.idlers_down", "Piped the idlers down."),
    ]
    assert len(crew.by_station[Station.IDLERS]) == 30


def test_nothing_else_in_a_quiet_day(a_day):
    _, notes, _ = a_day
    kinds = sorted({n[1] for _, n in notes})
    assert kinds == ["crew.idlers_down", "crew.idlers_up", "watch.relieved"]


def test_hands_at_work_finish_before_they_go_below():
    crew, clock, routine = _at(DAY.replace(hour=3, minute=58))
    larboard = crew.by_watch[Watch.LARBOARD]
    workers = [s for s in larboard if s.station is Station.FORE_TOP][:5]
    for s in workers:
        s.at = "reef_square#1"
    notes = _run(clock, routine, 120)  # to 04:00
    (_, relief) = notes[0]
    assert relief[2] == "Eight bells. The starboard watch relieved the deck."
    assert relief[4]["at_work"] == 5
    deck = crew.on_deck(clock)
    assert all(s in deck for s in workers)
    assert sum(1 for s in deck if s.watch is Watch.LARBOARD) == 5
    for s in workers:
        s.at = None  # the reef is tied: they go below
    _run(clock, routine, 1)
    assert not any(s.watch is Watch.LARBOARD for s in crew.on_deck(clock))


# ---------------------------------------------------------------------------
# all hands and piping down
# ---------------------------------------------------------------------------


def test_all_hands_come_up_over_ninety_seconds():
    crew, clock, routine = _at(DAY.replace(hour=2))  # middle watch: larboard on deck
    watch = len(crew.by_watch[Watch.LARBOARD])
    below = bill.below(crew, clock)
    assert watch == 111 and len(below) == 141  # the starboard watch and the idlers

    note = routine.call_all_hands("to shorten sail")
    assert note == (
        "notable",
        "crew.all_hands",
        "All hands! (to shorten sail)",
        None,
        {
            "reason": "to shorten sail",
            "by_order": False,
            "on_deck": 111,
            "coming": 141,
            "at_once": 47,
        },
    )
    curve = {0: len(crew.on_deck(clock))}
    assert not crew.all_hands_called  # set when the last hand is up
    up_line = []
    for second in range(1, 91):
        up_line += _run(clock, routine, 1)
        if second in (30, 60, 89, 90):
            curve[second] = len(crew.on_deck(clock))
    # a third at once, the rest evenly over the delay
    assert curve == {0: 111 + 47, 30: 111 + 47 + 31, 60: 111 + 47 + 62, 89: 250, 90: 252}
    assert crew.all_hands_called
    assert len(crew.on_deck(clock)) == len(_hands(crew)) == 252
    assert [n[2] for _, n in up_line] == ["All hands on deck."]
    assert up_line[0][0] == DAY.replace(hour=2) + timedelta(seconds=ALL_HANDS_DELAY_S)
    # deterministically by id: the first to come are the lowest ids below
    first = [s.id for s in below[:47]]
    assert all(crew.by_id[i].turned_up for i in first)


def test_the_first_third_are_up_before_the_rest():
    crew, clock, routine = _at(DAY.replace(hour=2))
    below = bill.below(crew, clock)
    routine.call_all_hands("to shorten sail")
    deck = {s.id for s in crew.on_deck(clock)}
    assert [s.id in deck for s in below] == [True] * 47 + [False] * 94
    _run(clock, routine, 30)
    deck = {s.id for s in crew.on_deck(clock)}
    assert [s.id in deck for s in below] == [True] * 78 + [False] * 63


def test_the_unfit_stay_below_and_a_second_call_is_nothing():
    crew, clock, routine = _at(DAY.replace(hour=2))
    sick = bill.below(crew, clock)[-1]
    sick.fit = False
    assert routine.call_all_hands("to shorten sail") is not None
    assert routine.call_all_hands("to tack") is None  # coming up already
    _run(clock, routine, 90)
    assert routine.call_all_hands("to reef topsails") is None  # all up
    assert sick not in crew.on_deck(clock)
    assert len(crew.on_deck(clock)) == 251


def test_pipe_down_after_the_runners_call_and_after_the_captains():
    # the runner's call for an all-hands evolution: piped down when it ends
    crew, clock, routine = _at(DAY.replace(hour=2))
    routine.call_all_hands("to tack")
    _run(clock, routine, 90)
    assert crew.all_hands_called and not crew.all_hands_called_by_order
    tacking = [s for s in crew.on_deck(clock) if s.watch is Watch.STARBOARD][:3]
    for s in tacking:
        s.at = "tack#1"  # still at the braces when the others are piped down
    note = routine.pipe_down()
    assert note == (
        "routine",
        "crew.piped_down",
        "Piped down; the larboard watch has the deck.",
        None,
        {"watch": "larboard", "on_deck": 111 + 3},
    )
    assert not crew.all_hands_called and not any(s.turned_up for s in crew.sailors)
    for s in tacking:
        s.at = None
    assert len(crew.on_deck(clock)) == 111
    assert routine.pipe_down() is None  # nobody up: no line

    # the captain's call: the runner reads the flag and leaves them up
    crew, clock, routine = _at(DAY.replace(hour=2))
    routine.call_all_hands("by the captain's order", by_order=True)
    assert crew.all_hands_called_by_order
    _run(clock, routine, 90)
    if not crew.all_hands_called_by_order:  # the runner's rule when its evolution ends
        routine.pipe_down()
    assert crew.all_hands_called and len(crew.on_deck(clock)) == 252
    assert routine.pipe_down()[2] == "Piped down; the larboard watch has the deck."
    assert not crew.all_hands_called and not crew.all_hands_called_by_order


def test_the_captains_call_while_all_hands_are_up_keeps_them_up():
    crew, clock, routine = _at(DAY.replace(hour=2))
    routine.call_all_hands("to tack")
    _run(clock, routine, 90)
    assert routine.call_all_hands("by the captain's order", by_order=True) is None
    assert crew.all_hands_called_by_order


def test_watch_changes_and_the_idlers_hour_send_nobody_below_while_all_hands_are_up():
    crew, clock, routine = _at(DAY.replace(hour=19, minute=59))  # last dog: starboard
    routine.call_all_hands("to shorten sail")
    notes = _run(clock, routine, 120)  # through 20:00
    texts = [n[2] for _, n in notes]
    assert texts == [  # at 20:00 they are still coming; all up at 20:00:30
        "Eight bells. All hands on deck; the larboard watch has the deck.",
        "All hands on deck.",
    ]
    assert len(crew.on_deck(clock)) == 252
    assert routine.pipe_down()[2] == "Piped down; the larboard watch has the deck."
    deck = crew.on_deck(clock)
    assert len(deck) == len(crew.by_watch[Watch.LARBOARD])  # the idlers below: it is night


def test_a_watch_change_while_the_hands_are_coming_up():
    crew, clock, routine = _at(DAY.replace(hour=3, minute=59, second=30))
    routine.call_all_hands("to wear")
    notes = _run(clock, routine, 30)  # 04:00: the starboard watch's turn, while they come
    assert notes[-1][1][2] == "Eight bells. All hands on deck; the starboard watch has the deck."
    assert all(s in crew.on_deck(clock) for s in crew.by_watch[Watch.LARBOARD])


def test_relieve_the_watch_early():
    crew, clock, routine = _at(DAY.replace(hour=3))  # middle watch: larboard
    note = routine.relieve_watch()
    assert note[1:3] == ("watch.relieved", "The starboard watch relieved the deck.")
    assert crew.watch_on_deck is Watch.STARBOARD
    assert {s.watch for s in crew.on_deck(clock)} == {Watch.STARBOARD}
    notes = _run(clock, routine, 3600)  # to 04:00, the starboard watch's by the bill
    assert [n[2] for _, n in notes] == ["Eight bells. The starboard watch kept the deck."]
    assert crew.watch_on_deck is None
    notes = _run(clock, routine, 4 * 3600)  # the next change is the ordinary one
    reliefs = [n[2] for _, n in notes if n[1] == "watch.relieved"]
    assert reliefs == ["Eight bells. The larboard watch relieved the deck."]


# ---------------------------------------------------------------------------
# fatigue and rest
# ---------------------------------------------------------------------------


def _fatigue_after_an_hour(when: datetime, set_up) -> Crew:
    crew, clock, routine = _at(when)
    for s in crew.sailors:
        s.fatigue = 0.5
    set_up(crew, clock, routine)
    _run(clock, routine, 3600)
    return crew


def test_the_rates_of_the_table():
    # 01:00 to 02:00, night: larboard on deck, starboard and idlers asleep
    def work(crew, clock, routine):
        larboard = crew.by_watch[Watch.LARBOARD]
        larboard[0].at = "haul#1"
        larboard[1].at = "furl#1"
        larboard[2].at = "loose#1"
        routine.set_aloft([larboard[1].id])
        routine.set_instance_aloft("loose#1", True)

    crew = _fatigue_after_an_hour(DAY.replace(hour=1), work)
    larboard = crew.by_watch[Watch.LARBOARD]
    assert larboard[0].fatigue == pytest.approx(0.5 + FATIGUE_AT_WORK_ON_DECK)
    assert larboard[1].fatigue == pytest.approx(0.5 + FATIGUE_AT_WORK_ALOFT)
    assert larboard[2].fatigue == pytest.approx(0.5 + FATIGUE_AT_WORK_ALOFT)
    assert larboard[3].fatigue == pytest.approx(0.5 + FATIGUE_ON_DECK_IDLE)
    assert crew.by_watch[Watch.STARBOARD][0].fatigue == pytest.approx(0.5 + FATIGUE_ASLEEP_BELOW)
    assert crew.by_station[Station.IDLERS][0].fatigue == pytest.approx(0.5 + FATIGUE_ASLEEP_BELOW)
    assert crew.posts["captain"].fatigue == 0.5  # the quarterdeck is not kept

    # 13:00 to 14:00, day: starboard on deck, larboard below, idlers up
    crew = _fatigue_after_an_hour(DAY.replace(hour=13), lambda *_: None)
    assert crew.by_watch[Watch.LARBOARD][0].fatigue == pytest.approx(0.5 + FATIGUE_BELOW_BY_DAY)
    assert crew.by_station[Station.IDLERS][0].fatigue == pytest.approx(0.5 + FATIGUE_ON_DECK_IDLE)
    assert [FATIGUE_ASLEEP_BELOW, FATIGUE_BELOW_BY_DAY] == [-0.12, -0.08]
    assert [FATIGUE_ON_DECK_IDLE, FATIGUE_AT_WORK_ON_DECK, FATIGUE_AT_WORK_ALOFT] == [
        0.01,
        0.06,
        0.10,
    ]


def test_fatigue_is_clamped():
    crew, clock, routine = _at(DAY.replace(hour=1))
    below = crew.by_watch[Watch.STARBOARD][0]
    worker = crew.by_watch[Watch.LARBOARD][0]
    below.fatigue, worker.fatigue, worker.at = 0.01, 0.999, "furl#1"
    routine.set_aloft({worker.id})
    _run(clock, routine, 3600)
    assert below.fatigue == 0.0 and worker.fatigue == 1.0


def test_night_is_from_the_second_dog_watch_to_the_morning_watch():
    assert is_night(DAY.replace(hour=20)) and is_night(DAY.replace(hour=3, minute=59))
    assert not is_night(DAY.replace(hour=4)) and not is_night(DAY.replace(hour=19, minute=59))


def test_the_night_call_costs_those_turned_out_of_their_sleep_once():
    crew, clock, routine = _at(DAY.replace(hour=2))
    below = bill.below(crew, clock)
    watch = crew.on_deck(clock)
    routine.call_all_hands("to shorten sail")
    assert all(s.fatigue == FATIGUE_ALL_HANDS_AT_NIGHT for s in below[:47])
    assert all(s.fatigue == 0.0 for s in below[47:]) and all(s.fatigue == 0 for s in watch)
    _run(clock, routine, 300)
    up = FATIGUE_ALL_HANDS_AT_NIGHT + 300 * FATIGUE_ON_DECK_IDLE / 3600  # up from the call
    assert below[0].fatigue == pytest.approx(up)
    # by day there is no cost for the call itself
    crew, clock, routine = _at(DAY.replace(hour=14))
    below = bill.below(crew, clock)
    routine.call_all_hands("to shorten sail")
    assert all(s.fatigue == 0.0 for s in below)


def _rates_agree_with_the_bill(crew: Crew, clock: Clock, routine: Routine) -> None:
    for s in crew.sailors:
        s.fatigue = 0.5
    routine._fatigue(1.0)  # the fast rule, one second
    deck = {s.id for s in bill.on_deck(crew, clock)}
    for s in _hands(crew):
        if s.at is not None:
            continue
        rose = s.fatigue > 0.5
        assert rose == (s.id in deck), (s.id, clock.stamp())


def test_the_routines_rule_for_on_deck_is_the_bills():
    crew, clock, routine = _at(DAY.replace(hour=2))
    _rates_agree_with_the_bill(crew, clock, routine)
    crew.sailors[40].fit = False
    crew.sailors[41].at = "tack#1"
    crew.sailors[200].turned_up = True
    _rates_agree_with_the_bill(crew, clock, routine)
    routine.relieve_watch()
    _rates_agree_with_the_bill(crew, clock, routine)
    clock.tick = 10 * 3600  # 12:00, idlers up
    _rates_agree_with_the_bill(crew, clock, routine)
    crew.all_hands_called = True
    _rates_agree_with_the_bill(crew, clock, routine)


# ---------------------------------------------------------------------------
# a quiet night against three all-hands calls in the middle watch (truth 20's numbers)
# ---------------------------------------------------------------------------

EVENING = datetime(1805, 5, 31, 20)  # the starboard watch has the first watch, then sleeps
CALLS = ((1, 0), (2, 0), (3, 0))  # three all-hands calls in the middle watch
WORK_S = 600  # each evolution holds every hand ten minutes once they are up
ALOFT_FROM_S, ALOFT_S = 200, 200  # the topmen aloft for the middle third of it


def _night(calls, capture=None) -> tuple[Crew, list]:
    """The frigate from 20:00 to the morning watch; the calls made as the runner would."""
    crew = _crew()
    clock = Clock(EVENING)
    routine = Routine(crew, clock)
    plan = {}
    for k, (h, m) in enumerate(calls):
        t0 = int((DAY.replace(hour=h, minute=m) - EVENING).total_seconds())
        up = t0 + int(ALL_HANDS_DELAY_S)
        plan[t0] = ("call", k)
        plan[up] = ("work", k)
        plan[up + ALOFT_FROM_S] = ("aloft", k)
        plan[up + ALOFT_FROM_S + ALOFT_S] = ("deck", k)
        plan[up + WORK_S] = ("done", k)
    notes = []
    while clock.ship_time < DAY.replace(hour=4):
        what, k = plan.get(clock.tick, (None, None))
        if what == "call":
            notes.append((clock.ship_time, routine.call_all_hands("to shorten sail")))
        elif what == "work":
            for s in crew.on_deck(clock):
                s.at = f"all_hands#{k}"
        elif what == "aloft":
            routine.set_aloft(s.id for s in crew.sailors if s.at and s.station in TOPS)
        elif what == "deck":
            routine.set_aloft(())
        elif what == "done":
            for s in crew.sailors:
                s.at = None
            if not crew.all_hands_called_by_order:
                notes.append((clock.ship_time, routine.pipe_down()))
            if capture is not None:
                capture.append(_mean(crew.by_watch[Watch.STARBOARD]))
        notes += _run(clock, routine, 1)
    return crew, notes


def _mean(sailors) -> float:
    return sum(s.fatigue for s in sailors) / len(sailors)


def test_a_quiet_night_leaves_the_watch_below_fresh():
    crew, notes = _night(())
    # asleep since midnight; one second on deck at 04:00 itself
    assert _mean(crew.by_watch[Watch.STARBOARD]) == pytest.approx(0.0, abs=1e-5)
    assert [n[2] for _, n in notes if n[1] == "watch.relieved"] == [
        "Eight bells. The larboard watch relieved the deck.",
        "Eight bells. The starboard watch relieved the deck.",
    ]


def test_three_calls_in_the_middle_watch_with_the_specs_table():
    peaks = []
    crew, notes = _night(CALLS, peaks)
    kinds = [n[1] for _, n in notes]
    assert kinds.count("crew.all_hands") == 3 and kinds.count("crew.piped_down") == 3
    # after each evolution the watch that should have slept is tired by a few hundredths...
    assert peaks == pytest.approx([0.0409, 0.0409, 0.0409], abs=5e-4)
    # ...and has slept it off by the morning watch: the fatigue term of the crew factor is
    # 1.0, not truth 20's 1.10 to 1.25 (the gate report carries this; see the next test)
    morning = _mean(crew.by_watch[Watch.STARBOARD])
    assert morning == pytest.approx(0.0, abs=1e-5)
    assert 1 + FATIGUE_WEIGHT * morning == pytest.approx(1.0, abs=1e-5)


def test_which_constant_would_bring_truth_20_in(monkeypatch):
    # Not a change: a measurement. The one-off cost of a night call at about 0.2 instead of
    # the spec's 0.03 gives the tired watch 0.34 and a fatigue term of 1.17 at 04:00.
    monkeypatch.setattr(routine_module, "FATIGUE_ALL_HANDS_AT_NIGHT", 0.2)
    crew, _ = _night(CALLS)
    morning = _mean(crew.by_watch[Watch.STARBOARD])
    assert morning == pytest.approx(0.3405, abs=5e-4)
    assert 1.10 <= 1 + FATIGUE_WEIGHT * morning <= 1.25


# ---------------------------------------------------------------------------
# determinism
# ---------------------------------------------------------------------------


def test_same_crew_same_clock_same_calls_same_notes_and_fatigues():
    a, notes_a = _night(CALLS)
    b, notes_b = _night(CALLS)
    assert notes_a == notes_b
    assert [s.fatigue for s in a.sailors] == [s.fatigue for s in b.sailors]


# ---------------------------------------------------------------------------
# the World: the routine's hook in the tick
# ---------------------------------------------------------------------------


def _crewed_world(path: Path, start: datetime):
    world = make_world(7, path, Scenario(start_time=start))
    crew = world.ship.extra["crew"]
    # the lead's line in session.py (make_world), made here by hand
    world.ship.extra["routine"] = Routine(crew, world.clock)
    return world


def test_a_crewed_world_logs_the_relief_before_the_bell():
    world = _crewed_world(FRIGATE, DAY.replace(hour=7, minute=59))
    world.run(90)
    kinds = ("watch.relieved", "clock.bell")
    lines = [e.line() for e in world.log if e.tick > 0 and e.kind in kinds]
    assert lines == [
        "  Forenoon watch, 8 bells (08:00)  Eight bells. The larboard watch relieved the deck.",
        "  Forenoon watch, 8 bells (08:00)  8 bells.",
    ]


def test_a_crewed_world_through_a_day():
    world = _crewed_world(SCHOONER, DAY)
    world.ship.stepper = None  # the physics has nothing to say to the routine: a day is quick
    world.run(24 * 3600)
    reliefs = world.log.of_kind("watch.relieved")
    assert [(e.ship_time.hour, e.text) for e in reliefs] == [
        (4, "Eight bells. The starboard watch relieved the deck."),
        (8, "Eight bells. The larboard watch relieved the deck."),
        (12, "Eight bells. The starboard watch relieved the deck."),
        (16, "Eight bells. The larboard watch relieved the deck."),
        (18, "Four bells. The starboard watch relieved the deck."),
        (20, "Eight bells. The larboard watch relieved the deck."),
        (0, "Eight bells. The starboard watch relieved the deck."),
    ]
    assert [e.text for e in world.log.of_kind("crew.idlers_up")] == ["Idlers up."]
    assert [e.text for e in world.log.of_kind("crew.idlers_down")] == ["Piped the idlers down."]
    assert all(e.actor == "sim" and e.severity == "routine" for e in reliefs)


def test_the_routine_touches_nothing_the_physics_reads():
    start = DAY.replace(hour=7, minute=55)
    worlds = [make_world(7, FRIGATE, Scenario(start_time=start)), _crewed_world(FRIGATE, start)]
    for w in worlds:
        w.submit("set the fore topsail")
        w.run(600)
    plain, crewed = worlds
    assert crewed.ship.state() == plain.ship.state()
    ours = {"watch.relieved", "crew.idlers_up", "crew.idlers_down"}
    others = [e.to_dict() for e in crewed.log if e.kind not in ours]
    assert others == [e.to_dict() for e in plain.log]
    assert len(crewed.log.of_kind("watch.relieved")) == 1
