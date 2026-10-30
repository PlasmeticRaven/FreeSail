"""Package 82, step 1: the person's movement between hulls (`docs/design/
Design-BoatAndPersonAboard.md` §2; the re-brief's item 3).

Proven here: a person put aboard another hull by his ship's boat (`send the boat to the
<ship> with <person>`) is a visitor there, his station going with him as his voice (a
passenger's station under his name) and his own station standing bound to him at home; a
visitor reads the hull he is in (`where am I`, the station line), gives none of her deck's
orders and comes home by `come aboard` in her boat, his own station his again; the moves
replay by both roads to the same digests of both logs, the harness grouped in the save by
the hull of its seating; the boarders' officer stands on the deck won, his station
following; a captive put aboard the captor with his station standing down by the handover's
rule (the hook package 74 calls); the director's `person: "X" goes aboard the <ship> by the
boat`.
"""

from __future__ import annotations

import json

from freesail.agents import Fake, Harness, SamplingPolicy, call
from freesail.agents.agent import captain as captain_station
from freesail.agents.model import Reply
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.world import movement as M
from freesail.world.seats import VOICE_KIND, _voice_name
from tests.test_crews import hove_to_world


def _brig_alongside(hold: str = 'ship "X": order heave to for a watch'):
    """The frigate hove to with a merchant brig put on the sea six cables off and promoted
    at the first switch, her captain held hove to by the director's hand so that the two lie
    within a boat's pull (`movement.BOAT_BETWEEN_NM`)."""
    w = hove_to_world()
    w.record_driver("routine", "driver.book", "The book of standing orders begins empty.")
    e = w.world_order('ship: a merchant brig "X" of Britain at 49 30 N 5 29 W, bound for Falmouth')
    assert e.data.get("result") == "done", e.text
    assert w.world_order('ship "X": intent bound for Falmouth').data.get("result") == "done"
    w.run(61)
    b = w.vessels.find("X")
    hull = b.crew
    assert hull is not None and hull.shape == "full"
    e = w.world_order(hold)
    assert e.data.get("result") == "done", e.text
    return w, b, hull


def _stages(frigate: str):
    """The fake at the brig's captain's station: sent aboard the frigate in his own boat,
    reads where he is and tries her helm, then comes home."""
    stage = {"n": 0, "results": []}

    def act(last, turns):
        if "tool_results" in last:
            stage["results"].append(str(last["tool_results"]))
            return Reply()
        log = last.get("log") or []
        kinds = {str(e.get("kind")) for e in log}
        text = " ".join(str(e.get("text", "")) for e in log).lower()
        s, orders = stage["n"], []
        if s == 0:
            orders, s = [f"send the boat to the {frigate} with the captain"], 1
        elif s == 1 and "person.aboard" in kinds and "came aboard" in text:
            orders, s = ["where am i", "steer west", "the ship"], 2
        elif s == 2:
            orders, s = ["come aboard"], 3
        elif s == 3 and "person.aboard" in kinds:
            orders, s = ["where am i"], 4
        stage["n"] = s
        if not orders:
            return Reply(text="Nothing to add; carrying on.")
        return Reply(calls=tuple(call("submit_order", text=o) for o in orders))

    return stage, act


def _seat(hull, act):
    policy = SamplingPolicy.in_lockstep(300, "notable", "urgent")
    h = Harness(hull, captain_station(policy, 3600, world=hull), Fake([act], loop=True))
    h.model_name, h.door = "the fake", "runner"
    h.start()
    return h


def _run_until(w, cond, hours: float, step: int = 60) -> None:
    for _ in range(int(hours * 3600 / step)):
        w.run(step)
        if cond():
            return
    raise AssertionError(f"not reached in {hours} h")


def _round_trip():
    """The brig's captain sent aboard the frigate in his own boat and home again in hers,
    every assertion of the first test on the way."""
    w, b, hull = _brig_alongside()
    frigate = w.ship.name
    stage, act = _stages(frigate)
    h = _seat(hull, act)
    captain = hull.people.captain
    voice = _voice_name(captain)
    assert h.seated_on == b.id and not h.visiting
    # the boat away for the frigate with him: a job of the port's kind at the boat's pace
    _run_until(w, lambda: hull.dealings.boat.away, 0.5)
    assert stage["n"] >= 1 and hull.dealings.boat.errand == "to_ship"
    assert captain.where == "boat" and captain.hull is None
    # alongside her: he is aboard the frigate, his harness with him as his voice
    _run_until(w, lambda: captain.hull == w.own.id, 1.0)
    assert captain.home == b.id and captain.aboard
    assert h.visiting and h.world is w.own and w.agents[voice] is h
    assert "captain" not in hull.agents
    assert hull.stations.holder("captain") is captain  # his own station stands bound to him
    assert w.stations.kind_of(voice) == VOICE_KIND and w.stations.holder(voice) is captain
    came = [e for e in w.log if e.kind == "person.aboard" and captain.name in e.text]
    assert came and "from the X's boat" in came[0].text
    assert any(e.kind == "person.moved" and "went aboard" in e.text for e in hull.log)
    assert h.line() is not None and "as a visitor" in h.line()
    # he reads where he is, and her deck is not his
    _run_until(w, lambda: stage["n"] >= 3, 0.5)
    results = " ".join(stage["results"]).lower()
    assert f"aboard the {frigate.lower()}" in results and "a visitor" in results
    assert "steer west" in results and "a visitor aboard another ship gives no order" in results
    # his acts there carry the frigate's hull (none for the player's own: the id rule)
    assert any(a["station"] == voice and "ship" not in a for a in w.station_acts)
    # home again by the frigate's boat: his own station his, the voice unbound
    _run_until(w, lambda: captain.hull == b.id, 1.5)
    assert captain.where == "quarterdeck"  # landed by the frigate's boat, as a visitor is
    assert not h.visiting and h.world is hull and hull.agents["captain"] is h
    assert voice not in w.agents and not w.stations.aboard(voice)
    _run_until(w, lambda: stage["n"] >= 4 and not w.dealings.boat.away, 0.5)
    assert "aboard the x" in " ".join(stage["results"][-2:]).lower()
    assert not hull.dealings.boat.away
    return w, b, hull, h


def test_a_stationed_person_sent_aboard_another_hull_is_a_visitor_there_and_home_again():
    _round_trip()


def test_the_moves_replay_by_both_roads_to_the_same_digests_with_the_harness_seated_at_home():
    w, b, hull, h = _round_trip()
    data = json.loads(json.dumps(w.save()))
    # the save groups the harness by the hull of its seating, wherever it was
    assert data["agents"] == [] and [blk["id"] for blk in data["hulls"]] == [b.id]
    assert data["hulls"][0]["agents"][0]["seated_on"] == b.id
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == w.log.digest(), road
        ch = copy.hulls[b.id]
        assert ch.log.digest() == hull.log.digest(), road
        assert "captain" in ch.agents and ch.agents["captain"].world is ch, road
        assert not ch.agents["captain"].visiting, road


def test_a_captive_put_aboard_the_captor_stands_his_station_down_by_the_handovers_rule():
    """The hook package 74 calls: `seat="stands down"`."""
    w, b, hull = _brig_alongside()
    h = _seat(hull, lambda last, turns: Reply(text="Carrying on."))
    captain = hull.people.captain
    w.run(300)
    kind, text, data = M.put_aboard(
        w,
        captain,
        w.own,
        "quarterdeck",
        seat="stands down",
        why="taken in the prize",
        by="the captor",
    )
    assert kind == "person.aboard" and captain.hull == w.own.id
    assert h.agent.released and hull.agents["captain"] is h  # released, kept for a reseat
    assert any(e.kind == "agent.stopped" and "stood down by the captor" in e.text for e in hull.log)
    assert hull.stations.holder("captain") is captain  # the binding stands; the deck the book's


def test_the_boarders_officer_stands_on_the_deck_won_and_his_station_follows_him():
    from freesail.agents.agent import officer as officer_station
    from freesail.combat import boarding as B
    from tests.test_fight import _alongside

    w, v, enemy = _alongside(10.0, her_quarters=True)
    lieutenant = B.boarders_officer(w)
    assert lieutenant is not None and lieutenant.role == "first lieutenant"
    policy = SamplingPolicy.in_lockstep(300, "notable", "urgent")
    h = Harness(
        w,
        officer_station(policy, world=w),
        Fake([lambda last, turns: Reply(text="Aye.")], loop=True),
    )
    h.start()
    assert w.stations.holder("officer of the watch") is lieutenant
    w.submit("grapple her")
    w.submit("serve out the small arms")
    w.run(400)
    assert w.submit("boarders away").kind == "action.boarders"
    for _ in range(B.CONTEST_ROUNDS + 1):
        w.run(60)
        f = B.fight_of(w.ship)
        if f is not None and f.over:
            break
    assert f is not None and f.over == "carried"
    assert lieutenant.hull == v.id and lieutenant.home == w.own.id
    assert h.visiting and h.world is enemy and enemy.agents[_voice_name(lieutenant)] is h
    assert any(e.kind == "person.moved" and "leads the boarders" in e.text for e in w.log)
    assert any(e.kind == "person.aboard" and "with the boarders" in e.text for e in enemy.log)
    assert "a visitor" in M.where_am_i(w, lieutenant)


def test_the_director_sends_a_person_aboard_another_ship_by_the_boat_and_doubts_it_far_off():
    from freesail.world import orders as WO

    w, b, hull = _brig_alongside()
    assert (
        w.world_order('person: make "Mr Veale", a clerk, aboard in the cabin', "the test").data[
            "result"
        ]
        == "done"
    )
    veale = w.people.find("Mr Veale")
    assert WO.doubt(w, WO.parse('person: "Mr Veale" goes aboard the X by the boat')) is None
    e = w.world_order('person: "Mr Veale" goes aboard the X by the boat', "the test")
    assert e.data.get("result") == "done", e.text
    assert veale.where == "boat" and w.dealings.boat.away
    w.run(1500)
    assert veale.hull == b.id and veale.home == w.own.id
    assert "aboard the X" in M.where_am_i(w, veale) and "a visitor" in M.where_am_i(w, veale)
    assert hull.people.find_aboard("Mr Veale") is veale and hull.people.find("Mr Veale") is None
    # far off, the move is doubted and not refused
    far = hove_to_world()
    far.world_order('ship: a merchant brig "Far" of Britain at 49 45 N 5 30 W, bound for Falmouth')
    far.world_order('ship "Far": intent bound for Falmouth')
    far.world_order('person: make "Mr Veale", a clerk, aboard in the cabin', "the test")
    far.run(60)
    doubt = WO.doubt(far, WO.parse('person: "Mr Veale" goes aboard the Far by the boat'))
    assert doubt is not None and "not sent so far" in doubt
