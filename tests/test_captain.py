"""The captain's station and the player's seat (package 40; spec M6 §3 and §7; truths 78,
79 and 81 in their fast forms, the passages whole in `tests/test_known_truths.py`),
proven against the scripted fake (`freesail/agents/fake.py`) and never a model.

The station with the player's whole surface: every order the player may give, judged by
the captain's domain and given under the station's actor, so that the log reads as a
captain's; the deck his by right of the station, lent to his book when his door is silent
or he hands it over, and his again at his next order; the officer under him given the
deck, allowed things and told, from this station, as the player does it; the brief head
saying the voyage; `the captain` and `the people` readings; `stand down the captain`; the
doors naming the station. The player's seat (`agents.seat`): the owner at the door, the
player at the officer's station under that station's authority, his orders journaled and
the game replaying with him seated."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call, reply
from freesail.agents import tools as tools_mod
from freesail.agents.agent import (
    CAPTAIN,
    CAPTAIN_DOMAIN,
    OFFICER,
    STOOD_DOWN,
    Authority,
    captain,
    officer,
    voyage_words,
)
from freesail.agents.fake import captain_of_the_ship, officer_of_the_watch
from freesail.agents.model import OPERATOR
from freesail.agents.seat import SEAT_KIND, PlayerSeat, seat_actor, seat_of, seat_player
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.orders.errors import OrderError
from freesail.world import captains as C
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = str(ROOT / "data/ships/frigate-36.yaml")
MERCHANT = "data/scenarios/merchant-passage.yaml"
INTENT = "data/scenarios/merchant-intent.yaml"
EVERY = 600  # sampled every ten minutes in lockstep, as the officer's tests
A_GLASS = 1800

# The fake captain's six harmless orders on the merchant passage (truth 78): three
# readings asked at the prompt, a question, `pipe down` with nobody turned up (accepted,
# and nothing to do), and the port; none moves the ship or draws the rng (heaving the log
# does, and moved the bearings' noise: TuningNotes, package 40).
SIX_ORDERS = [
    "what is the time",
    "the reckoning",
    "pipe down",
    "the tide",
    "the people",
    "the port",
]


def frigate_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, FRIGATE, scenario)


def scenario_world(path: str) -> World:
    sf = load_scenario(path)
    world = make_scenario_world(sf)
    begin(world, sf)
    return world


def station(world: World, every: int | None = EVERY, patience: int = 3600, events: bool = True):
    sevs = ("notable", "urgent") if events else ()
    return captain(SamplingPolicy.in_lockstep(every, *sevs), patience, world=world)


def seated(world: World, script: Any, *, patience: int = 3600, **kw) -> tuple[Harness, Any]:
    """The captain's station on `world`, held by a fake (a script, or a fake made)."""
    fake = script if hasattr(script, "reply") else Fake(script, **kw)
    h = Harness(world, station(world, patience=patience), fake, save=lambda w, why: None)
    h.model_name, h.door = "the fake", "runner"
    h.start()
    return h, fake


def order(text: str, **args: Any) -> Reply:
    return reply("", call("submit_order", text=text, **args))


def kinds(world: World, prefix: str = "agent.") -> list[str]:
    return [e.kind for e in world.log if e.kind.startswith(prefix)]


def lines(world: World, kind: str) -> list[str]:
    return [e.text for e in world.log if e.kind == kind]


def his(world: World) -> list[tuple[str, str]]:
    """The station's own order lines (not the harness's)."""
    return [
        (e.kind, e.text)
        for e in world.log
        if e.actor == "the captain" and not e.kind.startswith("agent.")
    ]


def others(world: World) -> list[tuple[str, str]]:
    """Every line that is not the station's nor the harness's about it."""
    return [
        (e.kind, e.text)
        for e in world.log
        if not e.kind.startswith("agent.") and e.actor != "the captain"
    ]


# ---------------------------------------------------------------------------
# The station: the whole surface, the deck by right, the log a captain's
# ---------------------------------------------------------------------------


def test_the_captains_station_has_the_players_whole_surface_and_the_deck_by_right():
    """Spec M6 §3: the station's domain is every verb at every level; the deck is his
    from the seating, said in the log; an order of his goes through `World.submit` under
    the station's actor, logged as a captain's ('By the captain: ...') and not journaled;
    the grammar refuses him as it refuses the player."""
    assert CAPTAIN_DOMAIN.is_captains and CAPTAIN_DOMAIN.why_not("tack ship", "ship", "3") is None
    assert CAPTAIN_DOMAIN.why_not("let go", "anchor", "3") is None
    assert Authority.CAPTAIN.may_submit_orders
    world = frigate_world()
    h, fake = seated(
        world,
        [
            order("set plain sail"),
            "Done.",
            order("shape a course for the moon"),
            "Done.",
            "Nothing more.",
        ],
    )
    assert h.agent.has_deck and h.station.person and h.station.rank == "captain"
    deck = lines(world, "agent.deck")
    assert deck and deck[0].startswith("The captain's station has the deck (")
    world.run(2 * EVERY + 1)
    accepted = [t for k, t in his(world) if k == "order.accepted"]
    assert accepted[0] == "By the captain: setting plain sail."
    rejected = [t for k, t in his(world) if k == "order.rejected"]
    assert rejected and "the moon" in rejected[0]
    # the journal holds the player's alone: his orders are the harness's transcript
    assert {actor for _, actor, _ in world.journal} <= {"captain"}
    reading = world.readings["captain"]
    assert reading["held"] and reading["deck"] and reading["model"] == "the fake"
    assert "the captain's station held by the fake, through the local runner" in reading["words"]


def test_the_captains_brief_head_says_the_voyage_the_ship_the_people_and_the_book():
    """Spec M6 §3 (M4 §11 extended): the head's five items in order, and the situation
    item opening with the voyage: the scenario's name, the intent or the book, the ship
    and her nation, the people with their outlines; the authority item saying he has the
    deck and carrying the book he inherits (the rules-based captain's state book)."""
    world = scenario_world(INTENT)
    world.run(C.JUDGE_FIRST_S + 1)  # the rules-based captain enters his first state
    words = voyage_words(world)
    assert words.startswith("The voyage: ")
    assert "The intent the scenario gives the ship: trade tin from Falmouth to Brest" in words
    assert "The ship: " in words and "topsail schooner" in words and "united states" in words
    assert "in command" in words or "master" in words
    h, _ = seated(world, [Reply()])
    brief = h.brief
    assert brief is not None
    text = brief.text()
    assert text.index("This is a message from the harness") < text.index("The voyage: ")
    assert "You have the deck, since" in text
    assert "The captain's night orders" in text
    # the in-port state's book is empty (the buying and the sailing are judgements): the
    # situation says the state through `the captain`, and the intent is in the voyage
    assert "trade tin from Falmouth to Brest" in text
    assert "  captain: " in text and "in port" in text
    assert h.turns[0].role == OPERATOR and h.turns[0].content == text
    assert "primer 17" in text and "primer 16" in text


def test_a_silent_captains_door_passes_the_deck_to_the_book_and_the_rules_stand_in():
    """Truth 79, the fast form: on the intent scenario a captain who takes the station
    and says nothing more has the deck lent to his book at the patience, an urgent line
    saying so and that the rules-based captain's judgements stand in; the rules then
    sail her (his judgements under the rule's actor, not journaled); the captain's next
    order takes the deck back and the rules stand aside."""
    world = scenario_world(INTENT)
    cap = world.captain
    assert cap.intent is not None
    h, fake = seated(world, captain_of_the_ship(then_silent=True), patience=A_GLASS)
    assert cap.seated and not cap.stand_in and cap.active and not cap.commands
    world.run(A_GLASS + 1)
    assert not h.agent.deck and h.agent.deck_lost == "silent"
    urgent = [e for e in world.log if e.kind == "agent.deck" and e.severity is Severity.URGENT]
    assert urgent and urgent[0].text.startswith("The captain's door has given no reply for a glass")
    assert "the rules-based captain's judgements stand in" in urgent[0].text
    assert cap.stand_in and cap.commands
    world.run(A_GLASS - 60)  # short of the pause at twice the patience
    by_rule = [e for e in world.log if e.actor.startswith("captain's rule ")]
    assert by_rule, "the rules-based captain gave no judgement while standing in"
    assert all(a.startswith("captain") for _, a, _ in world.journal)  # nothing of his journaled
    assert world.readings["captain"]["words"].count("stand in") == 1
    # the captain's door answers: an order takes the deck back and the rules stand aside
    result = tools_mod.call(world, CAPTAIN, "submit_order", {"text": "what is the time"})
    assert "The time" in result
    assert h.agent.deck and not cap.stand_in and not cap.commands
    back = [t for t in lines(world, "agent.deck") if "answers again (an order given)" in t]
    assert back


def test_a_silent_captain_on_a_book_scenario_leaves_the_book_the_deck_and_the_passage_as_it_was():
    """Truth 79 on the merchant passage (its book, no intent): the deck passes to the
    book at the patience, the book carries on (every line but the harness's as with
    nobody seated), and the line says the standing orders hold the deck."""
    base = scenario_world(MERCHANT)
    base.run(2 * 3600)
    world = scenario_world(MERCHANT)
    h, _ = seated(world, captain_of_the_ship(then_silent=True), patience=A_GLASS)
    world.run(2 * 3600)
    assert not h.agent.deck and h.agent.deck_lost in ("silent", "paused")
    urgent = [e for e in world.log if e.kind == "agent.deck" and e.severity is Severity.URGENT]
    assert urgent and "the standing orders hold the deck" in urgent[0].text
    assert not world.captain.active and not world.captain.commands
    assert others(world) == [(e.kind, e.text) for e in base.log]


def test_the_fake_captain_gives_six_orders_and_the_log_is_the_same_but_for_his_lines():
    """Truth 78, the fast form: the fake captain commands the merchant passage by its
    book and six direct orders (one a sample); every line of the passage is there as
    with nobody seated, and his six under his mark beside them."""
    base = scenario_world(MERCHANT)
    base.run(90 * 60)
    world = scenario_world(MERCHANT)
    h, _ = seated(world, captain_of_the_ship(SIX_ORDERS))
    world.run(90 * 60)
    mine = his(world)
    assert [k for k, _ in mine].count("order.accepted") == 1  # pipe down
    assert len(mine) >= 6 and "The time:" in mine[0][1]
    assert others(world) == [(e.kind, e.text) for e in base.log]
    assert h.agent.has_deck and h.agent.standing_by


def test_hand_over_lends_the_deck_to_the_book_and_the_next_order_takes_it_back():
    """Spec M6 §3: hand_over(note) at this station lends the deck to the book with the
    note, the captain staying seated; the next order takes it back; both said."""
    world = frigate_world()
    h, _ = seated(
        world,
        [
            reply("", call("hand_over", note="The ship is yours, book; I am at my desk.")),
            "Done.",
            order("set plain sail"),
            "Done.",
        ],
    )
    world.run(1)
    assert not h.agent.deck and h.agent.deck_lost == "handed over" and not h.agent.released
    lent = [t for t in lines(world, "agent.deck") if t.startswith("The captain lends the deck")]
    assert lent
    assert "lending the deck to the book" in " ".join(lines(world, "agent.handover"))
    world.run(EVERY)
    assert h.agent.deck and not h.agent.deck_lost
    assert any("answers again (an order given)" in t for t in lines(world, "agent.deck"))
    assert "By the captain: setting plain sail." in lines(world, "order.accepted")


def test_the_captains_own_reckoning_neither_wants_the_deck_nor_takes_it_back_from_the_book():
    """Package 40b (spec M6 §5): the captain's station has the officer's two orders of his
    own reckoning, as it has the player's whole surface, kept under the captain's name;
    they move nothing, so with the deck lent to his book they are given and the deck
    stays lent until an order that is the ship's takes it back."""
    from datetime import datetime

    scenario = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.2},
        region="channel-west",
    )
    world = make_world(7, FRIGATE, scenario)
    h, fake = seated(
        world,
        [
            reply("", call("hand_over", note="The ship is yours, book; I am at my slate.")),
            "Done.",
            order("work my reckoning"),
            order("my reckoning is 49 47 N 5 13 W"),
            "Done.",
            order("set plain sail"),
            "Done.",
        ],
    )
    world.run(1)
    assert not h.agent.deck and h.agent.deck_lost == "handed over"
    world.run(EVERY)
    assert not h.agent.deck and h.agent.deck_lost == "handed over"
    own = world.navigation.own["captain"]
    assert own["who"] == h.station.person and own["lat_deg"] == pytest.approx(49 + 47 / 60)
    assert [t for k, t in his(world) if k == "reckoning.own"]
    world.run(EVERY)
    assert h.agent.deck and not h.agent.deck_lost


def test_stand_down_the_captain_releases_the_station_and_the_rules_hold_her():
    """`stand down the captain` is the owner's: the station released and said, the game
    saved, the rules-based captain told nobody holds his station."""
    world = scenario_world(INTENT)
    cap = world.captain
    saves: list[str] = []
    h = Harness(world, station(world), captain_of_the_ship(), save=lambda w, why: saves.append(why))
    h.start()
    assert cap.seated and not cap.commands
    e = world.submit("stand down the captain")
    assert e.kind == "agent.stand_down", e.text
    world.run(1)
    assert h.agent.released and h.agent.left_by == STOOD_DOWN
    assert saves and "captain stood down" in saves[0]
    assert not cap.seated and cap.commands
    r = world.readings["captain"]
    assert not r["held"] and "nobody at the captain's station" in r["words"]
    assert "the deck the captain's own, by his rules" in r["words"]
    # the owner's resume is refused for a released station as it is for any
    with pytest.raises(OrderError):
        world.ship.handle_order("resume the captain")


def test_the_captains_station_gives_the_deck_allows_and_tells_the_officer_as_the_player_does():
    """Spec M6 §3: from the captain's station the officer under him is given the deck,
    allowed a thing by name, told, and asked, by the same sentences the player types; the
    sentences are the captain's own and the grammar reads them so."""
    world = frigate_world()
    oh = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(EVERY), world=world),
        officer_of_the_watch(),
        save=lambda w, why: None,
    )
    oh.start()
    ch, _ = seated(
        world,
        [
            order("you have the deck"),
            "Done.",
            order("you may tack ship if the land closes within two miles"),
            "Done.",
            order("tell the officer keep her full and by"),
            "Done.",
            order("I have the deck"),
            "Done.",
            "Nothing more.",
        ],
    )
    world.run(1)
    assert oh.agent.has_deck
    assert "you have the deck" in " ".join(lines(world, "agent.deck")).lower()
    assert "By the captain: you have the deck." in lines(world, "order.accepted")
    world.run(EVERY)
    assert [g.verb for g in oh.grants()] == ["tack ship"]
    world.run(EVERY)
    assert "The captain to the officer of the watch: keep her full and by" in lines(
        world, "agent.told"
    )
    world.run(EVERY)
    assert not oh.agent.has_deck and not oh.agent.released
    assert ch.agent.has_deck
    # the officer's own station may not say them
    text, why, _ = tools_mod.judge(world, OFFICER, "you have the deck")
    assert why and "may not" in why


def test_the_captain_and_the_people_readings_give_who_commands_and_no_truth():
    """Truth 81 and spec M6 §7: `the captain` says who holds the station, the book and
    whose the deck is; `the people` says who is in command; the readings tool at the
    captain's station is the registry's words and nothing else (no true position, no
    key the watcher's station lacks)."""
    world = scenario_world(INTENT)
    world.run(C.JUDGE_FIRST_S + 1)
    people = world.readings.words("people")
    assert "in command" in people
    r = world.readings["captain"]
    assert r["name"] and r["intent"] == "trade tin from Falmouth to Brest"
    assert r["state"] == "in port" and not r["held"]
    h, _ = seated(world, [Reply()])
    at_captain = tools_mod.readings(world, CAPTAIN)
    at_watcher = tools_mod.readings(world, "watcher")
    assert set(at_captain) == set(at_watcher)
    assert "captain" in at_captain and "the fake" in at_captain["captain"]
    truth = world.position
    for key, words in at_captain.items():
        text = json.dumps(words)
        assert f"{truth.lat_deg:.4f}" not in text and f"{truth.lon_deg:.4f}" not in text, key
    assert not any(k in at_captain for k in ("position", "truth", "true_position", "lat_deg"))


def test_the_doors_name_the_captains_station():
    """`--station captain` at the MCP bridge and the local runner; the REPL's table; the
    bridge's prompt for taking the command; the fake captain in `fake.py`."""
    from freesail.agents import local, mcp_server, repl
    from freesail.agents.remote import STATIONS

    assert CAPTAIN in STATIONS and CAPTAIN in repl.STATIONS
    for module in (mcp_server, local):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert 'choices=["watcher", "officer", "captain"]' in src, module.__name__
    assert "take_command" in Path(mcp_server.__file__).read_text(encoding="utf-8")
    assert STATIONS[CAPTAIN]().name == CAPTAIN


def test_a_game_with_the_captain_seated_saves_and_replays_to_the_same_digest(tmp_path):
    """The station's transcript in the save: the game replays with the captain seated,
    his orders given again from his transcript at their ticks, the digest the same."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    h, _ = seated(world, [order("set the royals"), order("take in the royals"), "Done."])
    world.run(3 * EVERY)
    world.submit("stand down the captain")
    world.run(EVERY)
    assert h.agent.released
    data = json.loads(json.dumps(world.save()))
    path = tmp_path / "captain.json"
    path.write_text(json.dumps(data))
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert copy.agents[CAPTAIN].agent.words() == h.agent.words()
    assert copy.captain.to_dict() == world.captain.to_dict()


# ---------------------------------------------------------------------------
# The player's seat (the owner's ruling 1)
# ---------------------------------------------------------------------------


def test_the_players_seat_is_judged_by_the_officers_authority_and_the_owner_keeps_his_words():
    """The player at the officer's station: an order of his is refused without the deck,
    judged by the domain and the captain's word with it, and given under the seat's actor
    and journaled when it passes; the stations' sentences typed at the same prompt are
    the owner's; the reading names him; the harness's own deck and grant lines serve."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(900)  # way enough on her to stay
    seat = seat_player(world, "officer", door="console")
    assert isinstance(seat, PlayerSeat) and seat_of(world, OFFICER) is seat
    assert world.player_seat is seat and world.ship.extra["player_seat"] is seat
    assert [e.kind for e in world.log if e.kind == SEAT_KIND] == [SEAT_KIND]
    assert seat_player(world, "officer", door="console") is seat  # idempotent
    with pytest.raises(OrderError):
        PlayerSeat(world, "watcher")
    e = seat.route("set the royals")
    assert e.kind == "agent.refused" and "has not the deck" in e.text and e.actor == "driver"
    e = seat.route("you have the deck")  # the owner's sentence, at the same prompt
    assert e.kind == "agent.deck" and seat.agent.has_deck
    e = seat.route("set the royals")
    assert e.kind == "order.accepted" and e.actor == seat_actor(OFFICER), e.text
    assert world.journal[-1][1] == seat_actor(OFFICER) and world.journal[-1][2] == "set the royals"
    e = seat.route("wear ship")
    assert e.kind == "agent.refused" and "may not wear ship" in e.text
    assert seat.route("you may wear ship").kind == "agent.deck"
    assert [g.verb for g in seat.grants()] == ["wear ship"]
    e = seat.route("wear ship")
    assert e.kind == "order.accepted", e.text
    r = world.readings["officer_of_the_watch"]
    assert r["deck"] and "the player, through the console" in r["words"]
    assert "may also wear ship" in r["words"]
    # a question and its answer; the word kept
    assert world.submit("ask the officer how she lies").kind == "agent.asked"
    assert seat.agent.question == "how she lies"
    e = seat.route("answer close hauled on the starboard tack")
    assert e.kind == "agent.answered" and seat.agent.question is None
    assert world.submit("tell the officer keep her full").kind == "agent.told"
    assert seat.agent.told == ["keep her full"]
    # the owner's `I have the deck` and `stand down`
    assert world.submit("I have the deck").kind == "agent.deck" and not seat.agent.has_deck
    e = seat.route("take in the royals")
    assert e.kind == "agent.refused" and "has not the deck" in e.text
    assert world.submit("stand down the officer").kind == "agent.stand_down"
    assert seat.agent.released and seat_of(world, OFFICER) is None
    assert world.ship.extra.get("player_seat") is None
    # released, his line is the owner's again
    assert seat.route("set the royals").actor == "captain"


def test_a_game_with_the_player_seated_saves_and_replays_with_him_seated(tmp_path):
    """The seating is a driver's line in the inputs and the seat's orders are journaled:
    a replay seats the player again and gives his orders, to the same digest, his journal
    the same."""
    world = frigate_world()
    world.submit("set plain sail")
    world.run(60)
    seat = seat_player(world, "officer", door="browser")
    world.submit("you have the deck")
    seat.route("set the royals")
    world.run(EVERY)
    seat.route("take in the royals")
    seat.route("wear ship")  # refused: a driver's line
    world.submit("ask the officer how she lies")
    seat.route("answer under plain sail, the royals in")
    world.run(EVERY)
    data = json.loads(json.dumps(world.save()))
    path = tmp_path / "seat.json"
    path.write_text(json.dumps(data))
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.log.digest() == world.log.digest()
    again = copy.player_seat
    assert again is not None and again.door == "browser" and again.agent.has_deck
    assert [x.to_dict() for x in copy.agent_journals[OFFICER].entries] == [
        x.to_dict() for x in seat.journal.entries
    ]
    # a checkpoint holds him too
    replay.write_checkpoint(world, tmp_path / "seat.ckpt")
    _header, back = replay.read_checkpoint(tmp_path / "seat.ckpt")
    assert back.player_seat is not None and back.player_seat.agent.has_deck
    assert back.ship.extra["player_seat"] is back.player_seat


def test_the_player_seated_under_the_fake_captain_is_given_the_deck_from_the_station():
    """Parity (the owner's ruling 1): the player holds the officer's station under a
    model captain; the captain's station gives him the deck and allows him a thing by
    the sentences the player types; his words reach the player as the captain's."""
    world = frigate_world()
    seat = seat_player(world, "officer", door="console")
    ch, _ = seated(
        world,
        [
            order("you have the deck"),
            "Done.",
            order("you may wear ship"),
            "Done.",
            order("tell the officer keep her full"),
            "Done.",
            "Nothing more.",
        ],
    )
    world.run(1)
    assert seat.agent.has_deck
    world.run(EVERY)
    assert [g.verb for g in seat.grants()] == ["wear ship"]
    world.run(EVERY)
    assert seat.agent.told == ["keep her full"]
    assert ch.agent.has_deck  # the captain's deck is his by right, the officer's his own
    world.submit("set plain sail")
    world.run(900)
    e = seat.route("wear ship")
    assert e.kind == "order.accepted", e.text
    r = world.readings["captain"]
    assert r["held"] and r["deck"]


def test_the_console_and_the_server_take_the_seat_flag():
    """`--seat officer` at both drivers, wired to the seat; the line at the prompt goes
    through the seat while it is held."""
    from freesail.ui import console, server

    for module in (console, server):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert '"--seat"' in src and "seat.route(" in src, module.__name__
    assert "officer" in console.SEAT_HELP
