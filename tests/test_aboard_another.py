"""Package 82, item 2 (the design's §4): the player's own seat on another ship, and the
director's door with another hull followed.

`--seat captain --ship <name>` at a driver (`console.aboard_ship`) sets the drivers to
follow her hull after a line in his own ship's log saying how she is left; his prompt is
hers (his orders go to the followed hull, her rules captain stands aside at his hand), his
`--seat` at a lesser station of hers is a `PlayerSeat` on her hull, which stays hers when
the drivers move on and goes with its person between hulls as a harness does (a visitor's
voice on another hull, his own station again at home). The director's door reads the
followed hull by the one rule (84's): `read_log` without a ship, `aboard:` without a
name, `captain:` and `captain: carry on` are hers; named, another's. 86's three seams by
the hull. Truths 7-322, 7-323 and 7-326 are in tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

import json

import pytest

from freesail.agents import tools
from freesail.agents.seat import seat_player
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.orders import station as station_mod
from freesail.ui.console import aboard_ship
from freesail.world import hail
from tests.test_crews import _frigate_and_the_brig_x_on_the_sea, hove_to_world, put


def aboard_x():
    """The frigate hove to with the brig X promoted beside her (84's helper, her captain
    bound for Falmouth under no hold), the player put aboard the X by the driver's flag."""
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    said: list[str] = []
    aboard_ship(w, "X", said.append)
    assert said == ["Following the X."]
    return w, b, hull


def _run_until(w, cond, ticks: int, step: int = 60) -> bool:
    for _ in range(0, ticks, step):
        if cond():
            return True
        w.run(step)
    return cond()


# ---------------------------------------------------------------------------
# the player aboard another ship (truth 7-322)
# ---------------------------------------------------------------------------


def test_the_player_aboard_another_ship_has_her_prompt_and_his_own_is_left_as_she_lies():
    w, b, hull = aboard_x()
    frigate = w.players
    assert w.followed == b.id and w.own is hull and not w.is_observer
    left = [e for e in frigate.log if e.kind == "driver.left"]
    assert len(left) == 1 and "is left as she lies, her watch kept" in left[0].text
    assert "no captain's hand on her" in left[0].text and "aboard the X" in left[0].text
    assert any(e.kind == "driver.follow" for e in hull.log)
    # her rules captain commands her until the player's hand
    assert hull.captain.commands and hull.captain.intent.words == "bound for Falmouth"
    e = w.submit("set the royals")
    assert e.kind == "order.accepted"
    assert any(x.text == "Order: set the royals." for x in hull.log)
    assert not any(x.text == "Order: set the royals." for x in frigate.log)
    assert hull.captain.aside and not hull.captain.commands
    assert any(x.kind == "captain.aside" for x in hull.log)
    # his own ship sails on as another hull, untouched by his orders, her captain quiet
    before = frigate.position
    w.run(120)
    assert frigate.position != before and frigate.captain.intent is None
    assert not any(x.kind == "order.accepted" and x.tick > 61 for x in frigate.log)
    # the seat flag's words at a driver with an observed world, and for a ship not there
    with pytest.raises(SystemExit, match="No ship named"):
        aboard_ship(w, "Nobody Known", lambda s: None)
    # back home: his own prompt again, the X's captain hers
    w.follow("the ship")
    assert w.own is frigate
    e = w.world_order("captain: carry on")
    assert "not carried out" in e.text  # the frigate's captain has no intent
    w.follow("X")
    assert "commands again" in w.world_order("captain: carry on").text or hull.captain.commands


def test_the_player_aboard_another_ship_replays_by_his_acts_to_the_same_digests():
    w, b, hull = aboard_x()
    w.submit("set the royals")
    w.run(300)
    w.submit("ease the sheets")
    w.run(300)
    data = json.loads(json.dumps(w.save()))
    kinds = [i["line"]["kind"] for i in data["inputs"] if "line" in i]
    assert "driver.left" in kinds and "driver.follow" in kinds
    copy = replay.replay(data, ship_factory)
    assert copy.followed == b.id
    assert copy.log.digest() == w.log.digest()
    assert copy.players.log.digest() == w.players.log.digest()
    assert copy.hulls[b.id].captain.aside


def test_a_ship_given_on_the_flag_with_an_observed_world_is_refused_in_words():
    from tests.test_observer import observed_world

    w, _ = observed_world()
    with pytest.raises(SystemExit, match="no ship of the player's to leave"):
        aboard_ship(w, "Medusa", lambda s: None)
    aboard_ship(w, None, lambda s: None)  # nothing for no name
    assert w.followed is None


# ---------------------------------------------------------------------------
# the director's door with another hull followed (truth 7-323)
# ---------------------------------------------------------------------------


def test_the_directors_door_reads_the_followed_hull_and_the_other_by_name():
    w, b, hull = aboard_x()
    frigate = w.players
    # the log the director reads with no ship named is the followed hull's
    lines = tools.read_log(w, 5)["lines"]
    assert any("X at full detail" in ln["text"] for ln in lines)
    assert not any("left as she lies" in ln["text"] for ln in lines)  # the frigate's line
    # `aboard:` with no name is aboard her
    n_x, n_f = len(hull.log), len(frigate.log)
    e = w.world_order("aboard: a cask found stove")
    assert "found aboard" in e.text
    assert any("found aboard" in x.text for x in list(hull.log)[n_x:])
    assert not any("found aboard" in x.text for x in list(frigate.log)[n_f:])
    # named, the other hull's
    e = w.world_order(f"aboard the {frigate.ship.name}: a cask found stove")
    assert f"aboard the {frigate.ship.name}: found aboard" in e.text
    assert any("cask" in x.text or "water" in x.text for x in list(frigate.log)[n_f:])
    # `captain:` is her rules captain's: the player's hand, then `carry on` gives her back
    w.submit("set the royals")
    assert hull.captain.aside
    e = w.world_order("captain: carry on")
    assert e.data.get("result") != "refused" and not hull.captain.aside
    assert hull.captain.commands
    # the director's hand on the followed ship is refused with her named as followed
    e = w.world_order('ship "X": order make sail')
    assert "X is the followed ship, and her captain is held by the player" in e.text
    # the truth is read from her
    from freesail.api.readings import director_readings

    truth = director_readings(w)
    assert truth["ships"][0]["name"] == "X"
    assert any(s["name"] == frigate.ship.name for s in truth["ships"][1:])


# ---------------------------------------------------------------------------
# 86's three seams by the hull (truth 7-326)
# ---------------------------------------------------------------------------


def test_a_free_intent_ship_lies_to_until_the_player_follows_her_and_gives_an_order():
    from freesail.world.captains import FREE

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    assert crew is not None and crew.shape == "full"
    w.world_order('ship "X": intent wait here for the Amazon\'s boat')
    assert crew.captain.intent.kind == FREE
    w.run(20 * 60)
    assert crew.readings.value("manoeuvre_in_hand") == "hove to" and crew.captain.commands
    assert not hail.model_holds_her(crew)  # nobody holds her: her table answers a hail
    # the player follows her and gives an order: her captain stands aside, she is held
    w.follow("X")
    e = w.submit("fill the main topsail")
    assert e.kind in ("order.accepted", "order.rejected")
    w.submit("set the royals")
    assert crew.captain.aside and not crew.captain.commands
    assert hail.model_holds_her(crew)
    n = len(list(crew.log))
    w.run(10 * 60)
    assert not [e for e in list(crew.log)[n:] if "free intent" in e.text]  # he lies her to no more
    # the player's own ship, left behind, is answered by her table (nobody holds her)
    assert not hail.model_holds_her(w.players)
    w.follow("the ship")
    assert hail.model_holds_her(w.players)  # his own prompt again


def test_hail_holds_the_players_own_hull_with_no_rules_captain_and_a_model_held_hull():
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import captain as captain_station
    from freesail.agents.model import Reply

    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    assert not hail.model_holds_her(hull)
    policy = SamplingPolicy.in_lockstep(300, "notable", "urgent")
    fake = Fake([Reply(text="Carrying on.")], loop=True)
    h = Harness(hull, captain_station(policy, 3600, world=hull), fake)
    h.model_name, h.door = "the fake", "runner"
    h.start()
    assert hail.model_holds_her(hull)  # a model at her captain's station
    # the player's own hull with no rules captain at all (the design's third case)
    players = w.players
    was = players.__dict__.get("captain")
    players.captain = None
    try:
        w.follow("X")
        assert players.parent is not None and hail.model_holds_her(players)
    finally:
        players.captain = was


def test_the_station_kept_on_the_players_ship_by_her_name_reads_the_players_vessel():
    w, b, hull = _frigate_and_the_brig_x_on_the_sea()
    name = w.players.ship.name
    own = w.vessels.own
    assert own is not None and own.crew is w.players
    found = station_mod._named_or_kind(hull, w, name.lower())
    assert found is own
    w.follow("X")
    assert station_mod._named_or_kind(hull, w, name.lower()) is own  # whichever is followed


# ---------------------------------------------------------------------------
# the seat on another ship, and with its person
# ---------------------------------------------------------------------------


def test_the_players_seat_on_another_ship_is_hers_and_stays_when_the_drivers_move_on():
    w, b, hull = aboard_x()
    seat = seat_player(w, "officer", door="console")
    assert seat.world is hull and hull.player_seat is seat and w.player_seat is seat
    assert w.players.player_seat is None
    e = seat.route("set the royals")
    assert e.kind in ("order.accepted", "agent.refused")  # judged by her station's authority
    w.follow("the ship")
    assert w.player_seat is None and hull.player_seat is seat and seat.world is hull
    # a second seat on his own ship is his own ship's (the X's stays hers)
    own_seat = seat_player(w, "officer", door="console")
    assert own_seat is not seat and own_seat.world is w and w.players.player_seat is own_seat


def test_the_seat_goes_with_its_person_by_the_boat_and_replays():
    """The seat's person sent to the player's own ship by her boat is a visitor there, his
    seat his voice (a visitor's orders refused in words); fetched home, his station his
    again; the whole by orders, so that a save replays it to the same digests."""
    from tests.test_between_hulls import _brig_alongside

    w, b, hull = _brig_alongside()  # six cables off, within a boat's pull
    aboard_ship(w, "X", lambda s: None)
    frigate = w.players
    seat = seat_player(w, "officer", door="console")
    person = hull.stations.holder(seat.station.name)
    assert person is not None and person.hull == b.id
    # the frigate's boat fetches him: given from her prompt
    w.follow("the ship")
    e = w.submit(f"send the boat to the X for {person.name}")
    assert e.kind != "order.rejected", e.text
    assert _run_until(w, lambda: person.hull == frigate.id, 3600)
    assert seat.visiting and seat.world is frigate and frigate.player_seat is seat
    assert hull.player_seat is None
    e = seat.route("set the royals")
    assert "a visitor aboard another ship gives no order" in e.text
    # and home again by her boat
    e = w.submit(f"send the boat to the X with {person.name}")
    assert e.kind != "order.rejected", e.text
    assert _run_until(w, lambda: person.hull == b.id, 3600)
    assert not seat.visiting and seat.world is hull and hull.player_seat is seat
    assert frigate.player_seat is None and seat.station.name == "officer of the watch"
    w.run(60)
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.hulls[b.id].log.digest() == hull.log.digest()
    cs = copy.hulls[b.id].player_seat
    assert cs is not None and not cs.visiting and cs.station.name == "officer of the watch"
