"""Package 20: the crew orders, the hands selector, the group line, close reef, and the
watch in `state`, the snapshot and the muster (spec M3 §5)."""

from __future__ import annotations

import io
from datetime import datetime

import pytest

from freesail import orders
from freesail.api import queries
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import bill
from freesail.crew.model import Watch
from freesail.crew.routine import ALL_HANDS_DELAY_S
from freesail.orders.errors import OrderError
from freesail.ship.parts import SailState
from freesail.ui.console import Console

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


def world(ship=FRIGATE, start=None, heading=293.0, speed=0.0):
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
    )
    if start is not None:
        scenario.start_time = start
    return make_world(7, ship, scenario)


def events(w, kind, after=-1):
    return [e for e in w.log if e.kind == kind and e.tick > after]


def rejected(w):
    return [e.text for e in events(w, "order.rejected")]


# ---------------------------------------------------------------------------
# The grammar: the hands selector is a modifier
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text, verb, obj, hands",
    [
        (
            "send the larboard watch aloft to furl the main course",
            "furl",
            "main course",
            "larboard",
        ),
        ("send the fore topmen to loose the fore topsail", "set", "fore topsail", "fore_top"),
        ("send the fore-topmen aloft to loose the fore topsail", "set", "fore topsail", "fore_top"),
        ("set the fore topsail with the starboard watch", "set", "fore topsail", "starboard"),
        ("set plain sail with the port watch", "set plain sail", None, "larboard"),
        ("brace sharp up with the afterguard", "brace", None, "afterguard"),
        ("take in the studdingsails, both sides, with the waisters", "take in", None, "waisters"),
    ],
)
def test_the_hands_selector_is_read_as_a_modifier(text, verb, obj, hands):
    w = world()
    order = orders.parse(w.ship, text)
    assert order.verb == verb
    if obj is not None:
        assert order.object == obj
    assert order.modifiers["hands_from"] == hands


def test_meet_her_with_the_helm_is_not_a_selector():
    w = world()
    order = orders.parse(w.ship, "meet her with the helm")
    assert order.verb == "meet her" and "hands_from" not in order.modifiers


@pytest.mark.parametrize(
    "text, words",
    [
        ("send the larboard watch aloft", "Send the larboard watch to do what?"),
        ("set the jib with the starboard watch with the fore topmen", "Two sets of hands"),
        ("haul the main brace with the starboard watch", "a watch or a station is sent"),
        ("tack ship with the larboard watch", "work for all hands"),
        ("send the marines aloft to loose the fore topsail", "The marines do not go aloft"),
        ("call all hands with the larboard watch", "a watch or a station is sent"),
    ],
)
def test_selector_errors_are_sentences(text, words):
    w = world()
    w.submit(text)
    assert any(words in r for r in rejected(w)), rejected(w)
    assert w.journal == []


def test_a_schooner_has_no_marines_or_main_topmen():
    w = world(SCHOONER, heading=300.0)
    w.submit("set the foresail with the marines")
    w.submit("send the main topmen to loose the fore topsail")
    assert rejected(w) == [
        "Order not carried out ('set the foresail with the marines'): "
        "There are no marines in this ship.",
        "Order not carried out ('send the main topmen to loose the fore topsail'): "
        "There are no main topmen in this ship.",
    ]


# ---------------------------------------------------------------------------
# A watch sent to work: turned up, staged, and the work drawn from it alone
# ---------------------------------------------------------------------------


def test_a_watch_below_is_turned_up_for_the_work_and_does_it():
    w = world()  # four in the morning: the starboard watch has the deck
    crew = w.ship.extra["crew"]
    assert bill.watch_on_deck(crew, w.clock) is Watch.STARBOARD
    larboard = [s for s in crew.by_watch[Watch.LARBOARD]]
    w.submit("send the larboard watch aloft to loose the fore topsail")
    first = sum(1 for s in larboard if s.turned_up)
    assert first == -(-len(larboard) // 3)  # a third at once, as all hands come
    w.tick()
    assert [e.text for e in events(w, "crew.watch_turned_up")] == ["Turned up the larboard watch."]
    runner = w.ship.extra["evolutions"]
    held = [s for s in crew.sailors if s.at == runner.instances[0].inst_id]
    assert held and all(s.watch is Watch.LARBOARD for s in held)
    w.run(int(ALL_HANDS_DELAY_S) // 2)
    assert first < sum(1 for s in larboard if s.turned_up) < len(larboard)
    w.run(int(ALL_HANDS_DELAY_S))
    assert all(s.turned_up for s in larboard)
    assert "the larboard watch turned up" in w.summary_lines()[-1]
    w.run(600)
    assert w.ship.sails["fore.topsail"].is_set
    w.submit("pipe down")
    assert not any(s.turned_up for s in larboard)
    assert events(w, "crew.piped_down")[-1].text == "Piped down; the starboard watch has the deck."


def test_a_refused_order_leaves_the_watch_below():
    w = world()
    crew = w.ship.extra["crew"]
    w.submit("send the larboard watch to goose wing the fore topgallant")  # runner refuses
    assert rejected(w)
    assert not any(s.turned_up for s in crew.sailors)
    assert w.ship.extra.get("watch_calls", []) == []
    w.tick()
    assert events(w, "crew.watch_turned_up") == []


def test_a_station_is_sent_from_the_deck_only():
    w = world(start=datetime(1805, 6, 1, 2, 0))  # the idlers are below at night
    w.submit("set the jib with the idlers")
    assert "None of the idlers are on deck" in rejected(w)[0]
    w.submit("set the fore topsail with the fore topmen")
    runner = w.ship.extra["evolutions"]
    crew = w.ship.extra["crew"]
    held = [s for s in crew.sailors if s.at == runner.instances[0].inst_id]
    assert held and all(s.station.value == "fore_top" for s in held)


# ---------------------------------------------------------------------------
# All hands, piping down, relieving the watch
# ---------------------------------------------------------------------------


def test_call_all_hands_by_order_and_a_second_call_says_so():
    w = world()
    crew = w.ship.extra["crew"]
    w.submit("call all hands")
    reply = w.log.tail(1)[0].text
    assert reply.startswith("The boatswain's mates pipe all hands at the hatchways;")
    assert crew.all_hands_called_by_order
    w.tick()
    notable = events(w, "crew.all_hands")
    assert [e.text for e in notable] == ["All hands! (by the captain's order)"]
    assert notable[0].severity.value == "notable"
    w.run(int(ALL_HANDS_DELAY_S))
    assert crew.all_hands_called
    assert "All hands called by the captain's order." in w.summary_lines()
    w.submit("turn the hands up")
    assert w.log.tail(1)[0].text == "All hands are on deck already; they stay up until piped down."
    w.tick()
    assert len(events(w, "crew.all_hands")) == 1


def test_pipe_down_is_refused_while_the_hands_are_about_ship():
    w = world(heading=292.5, speed=5.0)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    w.run(600)
    w.submit("trim sails")
    w.run(120)
    w.submit("tack ship")
    w.run(100)
    w.submit("pipe the watch below")
    assert rejected(w)[-1].endswith("The hands are still about ship; wait for her to come round.")
    assert w.ship.extra["crew"].all_hands_called


def test_pipe_down_with_nobody_up_is_answered_in_words():
    w = world()
    w.submit("pipe down")
    assert w.log.tail(1)[0].text == "Nobody is turned up; the starboard watch has the deck."
    assert rejected(w) == []


def test_relieve_the_watch():
    w = world()
    w.submit("relieve the watch")
    assert w.log.tail(1)[0].text == "The larboard watch relieved the deck."
    assert bill.watch_on_deck(w.ship.extra["crew"], w.clock) is Watch.LARBOARD


def test_crew_orders_without_a_crew_are_refused_in_words():
    from freesail.ship.loader import load_ship

    ship = load_ship(FRIGATE)
    from freesail.api.session import attach_systems

    attach_systems(ship)
    with pytest.raises(OrderError, match="no ship's company"):
        orders.handle(ship, "call all hands")
    with pytest.raises(OrderError, match="no ship's company"):
        orders.handle(ship, "set the jib with the starboard watch")


# ---------------------------------------------------------------------------
# The group line
# ---------------------------------------------------------------------------


def test_a_group_order_says_once_that_it_must_wait_for_hands():
    w = world(SCHOONER, heading=300.0)
    w.submit("set plain sail")
    w.tick()
    waits = events(w, "evolution.waiting")
    notable = [e for e in waits if e.severity.value == "notable"]
    assert [e.text for e in notable] == [
        "Setting plain sail: not hands enough for all at once; the watch takes the sails in turn."
    ]
    assert len(waits) > 1 and all(
        e.severity.value == "routine" for e in waits if e is not notable[0]
    )


def test_an_order_given_singly_keeps_its_notable_line():
    w = world(SCHOONER, heading=300.0)
    for text in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(text)
    w.tick()
    waits = events(w, "evolution.waiting")
    assert [e.severity.value for e in waits] == ["notable"]
    assert waits[0].text.startswith("Not hands enough on deck to set the mainsail")


# ---------------------------------------------------------------------------
# Close reef
# ---------------------------------------------------------------------------


def test_close_reef_takes_every_reef_band():
    w = world(heading=292.5, speed=4.0)
    w.submit("set the topsails")
    w.run(600)
    w.submit("close reef the topsails")
    w.run(1500)
    for sid in ("fore.topsail", "main.topsail", "mizzen.topsail"):
        sail = w.ship.sails[sid]
        assert sail.reef_bands > 1
        assert sail.reefs == sail.reef_bands, sid


def test_close_reef_after_one_reef_takes_the_rest():
    from test_primer import make_ship

    ship = make_ship("frigate", "plain-sail", "starboard")
    orders.handle(ship, "reef the fore topsail, one reef")
    runner = ship.extra["evolutions"]
    orders.handle(ship, "close reef the fore topsail")
    evo, subject, params = runner.started[-1]
    sail = ship.sails["fore.topsail"]
    assert (evo, subject) == ("reef_square", "fore.topsail")
    assert sail.reefs == sail.reef_bands
    assert params["reefs"] == sail.reef_bands - 1


# ---------------------------------------------------------------------------
# state, the snapshot and the muster
# ---------------------------------------------------------------------------


def test_state_shows_the_watch_and_the_work():
    w = world()
    w.submit("set the fore topsail")
    w.submit("set the main topsail")
    w.tick()
    lines = w.summary_lines()
    watch = [ln for ln in lines if ln.startswith("Watch on deck:")]
    assert watch == [
        "Watch on deck: starboard, 111 hands, 24 at work "
        "(12 at the fore topsail, 12 at the main topsail); idlers below."
    ]
    assert not any(ln.startswith("All hands called") for ln in lines)


def test_the_sail_set_line_shows_goose_winged_unbent_and_sent_down():
    w = world()
    ship = w.ship
    ship.sails["fore.course"].state = SailState.GOOSE_WINGED
    ship.sails["main.topsail"].state = SailState.SET
    ship.sails["fore.royal"].state = SailState.UNBENT
    for spar in ship.spars.values():
        if spar.id.startswith("main.topgallant_mast") or spar.id.startswith("main.royal"):
            spar.sent_down = True
    line = next(ln for ln in w.summary_lines() if ln.startswith("Sail set:"))
    assert line.startswith("Sail set: fore.course (goose-winged), main.topsail")
    assert "; unbent: fore.royal" in line
    assert line.endswith("; sent down: main.topgallant_mast")


def test_the_snapshot_carries_the_crew():
    w = world()
    w.submit("set the fore topsail")
    w.tick()
    crew = queries.snapshot(w)["crew"]
    assert set(crew) >= {
        "watch_on_deck",
        "on_deck",
        "idle",
        "at_work",
        "all_hands",
        "fatigue_mean_on_deck",
        "fatigue_mean_below",
    }
    assert crew["watch_on_deck"] == "starboard"
    assert crew["on_deck"] == 111 and crew["idle"] == 99
    assert crew["at_work"] == [
        {
            "evolution": "set_square",
            "subject": "fore.topsail",
            "hands": 12,
            "words": "at the fore topsail",
        }
    ]
    assert crew["all_hands"] is False
    from freesail.core.world import World

    assert queries.snapshot(World(seed=1))["crew"] is None


def test_muster_is_a_console_query_and_not_journaled():
    w = world()
    out = io.StringIO()
    con = Console(w, out=out)
    con.handle_line("muster the crew")
    con.handle_line("muster")
    text = out.getvalue()
    assert text.count("Mustered the Amazon's company") == 2
    assert "Fore topmen, 24" in text
    assert w.journal == []
    w.submit("muster")
    assert "is a console command" in rejected(w)[-1]


# ---------------------------------------------------------------------------
# Completion
# ---------------------------------------------------------------------------


def test_completion_offers_the_crew_orders_and_the_hands():
    from freesail.orders.complete import suggestions

    w = world()
    assert "call all hands" in suggestions(w.ship, "call")
    assert "pipe down" in suggestions(w.ship, "pip")
    assert "relieve the watch" in suggestions(w.ship, "reli")
    assert "muster the crew" in suggestions(w.ship, "mus")
    assert "send the larboard watch aloft to " in suggestions(w.ship, "send the l")
    inner = suggestions(w.ship, "send the larboard watch aloft to furl the main c")
    assert "send the larboard watch aloft to furl the main course" in inner
    after = suggestions(w.ship, "set the fore topsail ")
    assert "set the fore topsail with the starboard watch" in after
    assert "set the fore topsail with the fore topmen" in after
    assert "set plain sail with the larboard watch" in suggestions(w.ship, "set plain sail ")
    schooner = world(SCHOONER, heading=300.0)
    assert not any("marines" in s for s in suggestions(schooner.ship, "set the foresail "))
