"""Package 29: time compression and the roll-up (spec M4 §20), the roll-up in a model's
samples and auto-slow on alarm (spec M4 open item 8, the owner's rulings (a) and (b)).

The roll-up is one view (`events.RollupView`), over the store and never a change to it:
the console prints it, the server sends it (and the client shows what it is sent), and a
model's samples carry it, at the same threshold (`ROLLUP_FROM`).
"""

from __future__ import annotations

import io
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from freesail.agents import Fake, Harness, SamplingPolicy, Station
from freesail.agents.agent import WATCHER_BRIEF, Authority
from freesail.agents.model import DATA
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.events import (
    KEPT_ACTORS,
    ROLLUP_FROM,
    ROLLUP_KIND,
    ROLLUP_PERIOD_S,
    Event,
    Rollup,
    RollupView,
    Severity,
    rollup,
    summarise,
)
from freesail.core.world import Scenario, World
from freesail.ship.stub import PointShip
from freesail.ui.console import ALARM_SPEED, MAX_COMPRESSION, Console
from freesail.ui.server import Driver, create_app

T0 = datetime(1805, 6, 1, 4, 0)
FRIGATE = "data/ships/frigate-36.yaml"


def ev(minutes: float, kind: str, text: str, severity: str = "routine", actor: str = "sim"):
    t = T0 + timedelta(minutes=minutes)
    return Event(
        tick=int(minutes * 60),
        ship_time=t,
        severity=Severity(severity),
        kind=kind,
        text=text,
        actor=actor,
    )


def an_hour_and_a_bit() -> list[Event]:
    return [
        ev(0, "clock.bell", "8 bells."),
        ev(5, "yard.braced_round", "Braced round on the larboard tack."),
        ev(7, "wind.gust", "A gust: 24 knots."),
        ev(9, "sail.set", "Set the jib.", "notable"),
        ev(20, "wind.gust", "A gust: 31 knots."),
        ev(30, "clock.bell", "1 bell."),
        ev(31, "order.accepted", "Order: steer south.", actor="captain"),
        ev(40, "yard.braced_round", "Braced round on the starboard tack."),
        ev(45, "sail.blown_out", "Jib split and blew out of the bolt-ropes.", "urgent"),
        ev(59, "watch.relieved", "Eight bells. The larboard watch relieved the deck."),
        ev(60, "clock.bell", "2 bells."),
        ev(61, "wind.gust", "A gust: 20 knots."),
    ]


# -- the view -------------------------------------------------------------------------


def test_below_the_threshold_every_line_is_shown_as_it_is():
    events = an_hour_and_a_bit()
    assert rollup(events, ROLLUP_FROM - 1) == events
    assert ROLLUP_FROM == 60 and ROLLUP_PERIOD_S == 3600  # spec §20: sixty, hourly
    assert KEPT_ACTORS == {"captain", "driver"}


def test_at_the_threshold_the_hour_rolls_up_and_notable_urgent_and_the_captains_stay():
    events = an_hour_and_a_bit()
    shown = rollup(events, ROLLUP_FROM)
    kept = [x for x in shown if isinstance(x, Event)]
    assert [x.text for x in kept] == [
        "Set the jib.",
        "Order: steer south.",
        "Jib split and blew out of the bolt-ropes.",
    ]
    rolls = [x for x in shown if isinstance(x, Rollup)]
    assert len(rolls) == 1, "the hour still open (from 05:00) waits for its end"
    r = rolls[0]
    assert r.count == 7 and r.first_tick == 0 and r.last_tick == 59 * 60
    assert r.stamp == "Morning watch (04:00-05:00)"
    assert r.text == (
        "Braced round twice, the larboard watch relieved the deck, 2 gusts, the strongest "
        "31 knots; 7 routine entries."
    )
    assert shown.index(r) == len(shown) - 1, "shown where the hour ends"
    # nothing is dropped: every event is kept or counted
    closed = [e for e in events if e.ship_time < T0 + timedelta(hours=1)]
    assert len(kept) + r.count == len(closed)
    # with `so_far` a reader who will not see the hour close has it too
    last = rollup(events, ROLLUP_FROM, so_far=True)[-1]
    assert isinstance(last, Rollup) and last.so_far and last.count == 2
    assert last.stamp == "Morning watch (05:00-on)" and last.text.endswith("so far.")


def test_the_words_come_from_the_kinds_and_counts():
    """No language model: each phrase is a kind and a count; what no rule names is
    counted at the end."""
    r = summarise(
        [
            ev(1, "sail.filled", "Fore course filled again."),
            ev(2, "sail.filled", "Main course filled again."),
            ev(3, "crew.all_hands_up", "All hands on deck."),
            ev(4, "crew.piped_down", "Piped down; the starboard watch has the deck."),
            ev(5, "evolution.step", "Laid aloft and loosed the main topsail."),
            ev(6, "evolution.started", "Hands aloft to loose the foresail."),
            ev(
                7,
                "order.rejected",
                "Standing order 'night routine': ...",
                actor="standing order 'night routine'",
            ),
            ev(8, "standing.held", "...", actor="standing order 'morning sail'"),
            ev(9, "agent.note", "[watcher] All quiet.", actor="the watcher"),
            ev(10, "ship.leeway", "Leeway 4° to larboard."),
            ev(11, "something.else", "A line no rule names."),
        ]
    )
    assert r.text == (
        "The fore course and the main course filled again, all hands up once, piped down "
        "once, the hands at their work (2 steps), standing order 'morning sail' held, its "
        "condition not met, standing order 'night routine' found nothing to do once, the "
        "watcher spoke once, "
        "leeway 4° to larboard, 1 other entry; 11 routine entries."
    )
    assert r.counts["sail.filled"] == 2


def test_the_live_view_lets_go_of_an_hour_at_its_end_and_when_the_speed_comes_down():
    events = an_hour_and_a_bit()
    view = RollupView()
    out = []
    for e in events[:10]:
        out += view.feed(e, 300)
    assert not any(isinstance(x, Rollup) for x in out) and view.holding == 7
    out = view.feed(events[10], 300)  # the 05:00 bell: the hour is over
    assert isinstance(out[0], Rollup) and not out[0].so_far and view.holding == 1
    out = view.feed(events[11], 10)  # the speed came down: the hour so far, then the line
    assert isinstance(out[0], Rollup) and out[0].so_far and out[0].count == 1
    assert out[1] is events[11] and view.holding == 0
    assert view.flush() == []


def test_a_rollup_goes_on_the_wire_like_an_event():
    r = rollup(an_hour_and_a_bit(), 60)[-1]
    d = r.to_dict()
    assert d["kind"] == ROLLUP_KIND == "log.rollup" and d["severity"] == "routine"
    assert d["stamp"] == "Morning watch (04:00-05:00)"
    assert d["data"]["first_tick"] == 0 and d["data"]["count"] == 7
    assert r.line() == "= Morning watch (04:00-05:00)  " + r.text


# -- the console ------------------------------------------------------------------------


def frigate(seed: int = 7) -> World:
    return make_world(
        seed,
        FRIGATE,
        Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=1.0, variability=0.3),
    )


def test_the_console_prints_the_rollup_at_sixty_and_every_line_below():
    out = io.StringIO()
    con = Console(frigate(), out=out)
    con.handle_line("set plain sail")
    con.handle_line("speed 30")
    con.world.run(600)
    below = out.getvalue()
    assert "Hands aloft" in below  # a routine line, printed at 30x
    con.handle_line("speed 60")
    start = len(out.getvalue())
    con.world.run(3600)
    text = out.getvalue()[start:]
    assert "Hands aloft" not in text and "= Morning watch (04:00-05:00)" in text
    notable = [e for e in con.world.log if e.tick > 600 and e.severity is not Severity.ROUTINE]
    for e in notable:
        assert e.line() in text


def test_speed_and_time_are_one_word_and_run_to_three_hundred():
    out = io.StringIO()
    con = Console(World(seed=3), out=out)
    con.handle_line("speed 120")
    assert con.compression == 120 and con.world.compression == 120
    con.handle_line("time 600")
    assert con.compression == MAX_COMPRESSION == 300
    assert "Compression 300x (the most there is)." in out.getvalue()
    con.handle_line("speed 5")
    assert con.compression == 5


def test_coming_down_from_three_hundred_lets_go_of_the_hour_held():
    out = io.StringIO()
    con = Console(World(seed=3, scenario=Scenario(gustiness=1.0)), out=out)
    con.handle_line("speed 300")
    con.world.run(900)
    assert "= Morning watch" not in out.getvalue()
    con.handle_line("speed 10")
    assert "= Morning watch (04:00-on)" in out.getvalue()


# -- the server ----------------------------------------------------------------------------


def test_the_server_sends_rollups_at_sixty_and_events_below():
    d = Driver(frigate())
    got: list[dict] = []
    d.add_listener(got.append)
    d.set_compression(300)
    d.submit("set plain sail")
    d._run_ticks(3700)
    kinds = [m["type"] for m in got]
    assert "rollup" in kinds
    rolls = [m["rollup"] for m in got if m["type"] == "rollup"]
    assert rolls[0]["stamp"] == "Morning watch (04:00-05:00)"
    sent = [m["event"] for m in got if m["type"] == "event"]
    assert all(e["severity"] != "routine" or e["actor"] in KEPT_ACTORS for e in sent)
    # the same lines the console's view gives
    shown = rollup(d.world.log.all(), 300)
    assert [r.text for r in shown if isinstance(r, Rollup)] == [r["text"] for r in rolls]


def test_the_server_takes_speed_to_three_hundred_and_serves_the_store_by_ticks():
    driver = Driver(frigate())
    app = create_app(driver)
    with TestClient(app) as client:
        r = client.post("/api/driver", json={"action": "speed", "value": 1000})
        assert r.json()["compression"] == 300.0
        client.post("/api/order", json={"text": "set plain sail"})
        client.post("/api/driver", json={"action": "tick", "value": 3700})
        with client.websocket_connect("/ws") as ws:
            hello = ws.receive_json()
            log = hello["log"]
            rolled = [x for x in log if x["kind"] == ROLLUP_KIND]
            assert rolled and rolled[0]["stamp"] == "Morning watch (04:00-05:00)"
        first, last = rolled[0]["data"]["first_tick"], rolled[0]["data"]["last_tick"]
        lines = client.get(
            "/api/log", params={"since": first - 1, "until": last, "limit": 5000}
        ).json()
        assert lines and all(first <= e["tick"] <= last for e in lines)
        routine = [e for e in lines if e["severity"] == "routine" and e["actor"] not in KEPT_ACTORS]
        assert len(routine) == rolled[0]["data"]["count"], "the roll-up's lines, from the store"


# -- the model's samples (open item 8, ruling (a)) ----------------------------------------


def stationed(world: World, every: int = 1800) -> tuple[Harness, Fake]:
    st = Station(
        "watcher",
        Authority.NONE,
        SamplingPolicy.in_lockstep(every, "notable", "urgent"),
        7200,
        WATCHER_BRIEF,
    )
    fake = Fake(["Aye."], loop=True)
    h = Harness(world, st, fake, save=lambda w, why: None)
    h.start()
    return h, fake


def sample_lines(fake: Fake) -> list[dict]:
    seen, out = [], []
    for turns in fake.seen:
        for t in turns:
            if t.role == DATA and "log" in t.content and not any(t.content is s for s in seen):
                seen.append(t.content)
                out += t.content["log"]
    return out


def test_at_sixty_and_above_the_samples_carry_the_same_rollup_the_captain_reads():
    """Parity (spec M4 open item 8 (a)): the watcher's samples carry the hour's roll-up
    exactly as the console shows it, and the notable lines as they are; the station's own
    lines are left out of its samples, as they always have been."""
    world = frigate()
    out = io.StringIO()
    con = Console(world, out=out)
    con.handle_line("speed 300")
    h, fake = stationed(world)
    world.submit("set plain sail")
    world.run(2 * 3600 + 60)
    lines = sample_lines(fake)
    rolled = [ln for ln in lines if ln["kind"] == ROLLUP_KIND]
    assert [ln["stamp"] for ln in rolled] == [
        "Morning watch (04:00-05:00)",
        "Morning watch (05:00-06:00)",
    ]
    others = [e for e in world.log if e.actor != "the watcher"]
    expected = [x for x in rollup(others, 300) if isinstance(x, Rollup)]
    assert [ln["text"] for ln in rolled] == [r.text for r in expected]
    assert all(
        ln["severity"] != "routine" or ln["kind"] == ROLLUP_KIND
        for ln in lines
        if ln["kind"] != "order.accepted"
    )
    printed = out.getvalue()
    for r in expected:  # the console printed the same hour, its count with the watcher's
        assert r.stamp in printed


def test_below_sixty_the_samples_are_as_they_were():
    world = frigate()
    world.compression = 10
    h, fake = stationed(world, every=600)
    world.submit("set plain sail")
    world.run(1200)
    lines = sample_lines(fake)
    assert not any(ln["kind"] == ROLLUP_KIND for ln in lines)
    assert any(ln["kind"].startswith("evolution.") for ln in lines), "routine lines as ever"


# -- auto-slow on alarm (open item 8, ruling (b)) ----------------------------------------


class AlarmShip(PointShip):
    """A point ship whose topgallant blows out at its fiftieth step: an urgent line from
    the ship's own step, as a real one comes, on the same tick in a replay."""

    def __init__(self) -> None:
        super().__init__()
        self.steps = 0

    def save_ref(self):
        return {"type": "alarm"}

    def step(self, dt, wind):
        notes = list(super().step(dt, wind))
        self.steps += 1
        if self.steps == 50:
            notes.append(("urgent", "sail.blown_out", "Main topgallant split and blew out."))
        return notes


def alarm_world() -> World:
    return World(seed=7, ship=AlarmShip())


def alarm_factory(ref, scenario):
    return AlarmShip() if ref.get("type") == "alarm" else None


def test_an_urgent_line_eases_the_console_to_one_and_says_so():
    out = io.StringIO()
    con = Console(alarm_world(), out=out)
    con.handle_line("speed 300")
    con.running = True
    ran = con._run(200)
    assert ran == 50 and con.world.clock.tick == 50
    assert con.compression == ALARM_SPEED == 1
    eased = [e for e in con.world.log if e.kind == "driver.eased"]
    assert [e.text for e in eased] == [
        "Compression eased to 1x: Main topgallant split and blew out."
    ]
    assert eased[0].actor == "driver" and eased[0].severity is Severity.NOTABLE
    assert "Compression eased to 1x" in out.getvalue()
    # the player chooses when to speed up again; at one, the next alarm eases nothing
    con.running = True
    con._run(100)
    assert con.compression == 1


def test_auto_slow_changes_the_drivers_speed_and_a_replay_writes_its_line_again(tmp_path):
    """The eased line is a driver's line in `World.inputs`: a replay of the save writes it
    at the same point, and the digests agree."""
    out = io.StringIO()
    con = Console(alarm_world(), out=out)
    con.handle_line("speed 300")
    con.running = True
    con._run(200)
    con.running = False
    con._run(30)
    data = replay.load_file(replay.save_to_file(con.world, tmp_path / "alarm.json"))
    assert any("line" in x and x["line"]["kind"] == "driver.eased" for x in data["inputs"])
    copy = replay.replay(data, alarm_factory)
    assert copy.log.digest() == con.world.log.digest()
    assert [e.tick for e in copy.log if e.kind == "driver.eased"] == [50]


def test_the_server_eases_too_and_the_client_is_told():
    d = Driver(alarm_world())
    got: list[dict] = []
    d.add_listener(got.append)
    d.set_compression(300)
    d.running = True
    d._run_ticks(200)
    assert d.world.clock.tick == 50 and d.compression == 1
    state = d.state()
    assert state["eased"] == {
        "from": 300.0,
        "to": 1.0,
        "line": "Main topgallant split and blew out.",
        "tick": 50,
    }
    assert any(m["type"] == "event" and m["event"]["kind"] == "driver.eased" for m in got)
    d.set_compression(60)  # the player's choice clears the notice
    assert "eased" not in d.state()


def test_a_tick_command_is_not_eased():
    """Auto-slow is for the running clock; `tick N` is the player's own count."""
    out = io.StringIO()
    con = Console(alarm_world(), out=out)
    con.handle_line("speed 300")
    con.handle_line("tick 100")
    assert con.world.clock.tick == 100 and con.compression == 300


@pytest.mark.parametrize("value", [0, 0.01])
def test_the_slowest_speed_still_moves(value):
    con = Console(World(seed=3), out=io.StringIO())
    con.handle_line(f"speed {value}")
    assert con.compression == 0.1


def test_the_strongest_gust_names_the_mean_it_blew_over():
    """Package 29b: a gust line carries the ten-minute mean it blew over, and the hour's
    roll-up names it beside the strongest."""
    from freesail.core.events import summarise

    gusts = [
        ev(7, "wind.gust", "A gust: 24 knots, the mean 19."),
        ev(9, "wind.gust", "A gust: 31 knots, the mean 22."),
    ]
    gusts[0].data["mean_kn"] = 19.0
    gusts[1].data["mean_kn"] = 22.0
    assert "2 gusts, the strongest 31 knots on a mean of 22" in summarise(gusts).text


def test_a_stations_own_words_are_never_rolled_up():
    """The owner, package 29b (playtest 7): at speed a watcher's `say` went into the hour's
    roll-up instead of showing at once. A line whose actor is a station is kept as it is,
    like the captain's own, whatever the station (taken from the stations as they are
    defined, not a list here). At 300x, a fake watcher speaks in an otherwise routine hour:
    its line is shown at once, in its place, and the hour's count leaves it out."""
    from freesail.core.events import STATION_ACTORS, kept

    world = World(seed=7, scenario=Scenario(gustiness=0.0, variability=0.0))
    world.compression = 300
    st = Station(
        "watcher",
        Authority.NONE,
        SamplingPolicy.in_lockstep(1800, "urgent"),
        14400,
        WATCHER_BRIEF,
    )
    h = Harness(world, st, Fake(["The wind holds steady from the west."] * 4), save=None)
    h.start()
    world.run(3 * 3600)
    said = [e for e in world.log if e.kind == "agent.note"]
    assert said and all(e.severity is Severity.ROUTINE and e.actor == "the watcher" for e in said)
    assert "the watcher" in STATION_ACTORS and all(kept(e) for e in said)
    shown = rollup(world.log.all(), 300, so_far=True)
    lines = [x for x in shown if isinstance(x, Event)]
    rolls = [x for x in shown if isinstance(x, Rollup)]
    assert all(e in lines for e in said)
    assert rolls and sum(r.count for r in rolls) + len(lines) == len(world.log)
    assert not any("spoke" in r.text for r in rolls)
    # a station defined later (an officer) is kept the same way, with nothing added here
    Station("second lieutenant", Authority.NONE, SamplingPolicy.periodic(1800), 14400, "x")
    assert "the second lieutenant" in STATION_ACTORS
