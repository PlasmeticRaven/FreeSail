"""The wardroom (package 41; spec M6 §11, §12 and §16): the master's and the lookout's
stations, a passenger's, the stations as data bound on the World, the stand-by on
several conditions, the deck's conversation, who may give what, the player's seat at
the lesser stations, the doors and the pace rule; proven against the scripted fakes
(`freesail/agents/fake.py`) and never a model. Every world is the frigate or the cutter
in a steady wind, the stations sampled every ten minutes in lockstep, so that a script's
count of replies is exact. The identities are made up; the consent records go to a
temporary directory."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

import pytest

from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call, consent, reply
from freesail.agents import tools as tools_mod
from freesail.agents.agent import (
    A_GLASS_S,
    CAPTAIN,
    LOOKOUT,
    LOOKOUT_DOMAIN,
    LOOKOUT_KINDS,
    MASTER,
    MASTER_DOMAIN,
    MASTER_KINDS,
    OFFICER,
    PASSENGER,
    PASSENGER_DOMAIN,
    STATION_FACTORIES,
    cadence_policy,
    lookout,
    master,
    officer,
    passenger,
    place_of,
)
from freesail.agents.fake import (
    captain_of_the_ship,
    master_of_the_reckoning,
    officer_of_the_watch,
    passenger_aboard,
)
from freesail.agents.harness import open_samples
from freesail.agents.seat import seat_player
from freesail.api import readings as R
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.orders.errors import OrderError
from freesail.world import captains as C
from freesail.world.reckoning import MASTER_STOOD_KIND, MASTER_WORKING_KIND, MASTER_WORKING_S
from freesail.world.stations import BOUND_KIND, UNBOUND_KIND

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = str(ROOT / "data/ships/frigate-36.yaml")
CUTTER = str(ROOT / "data/ships/cutter.yaml")
EVERY = 600
WEIGHTS = "made-up-wardroom-model-9b.Q4_K_M.gguf"  # made up: no model is named here


def frigate_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, FRIGATE, scenario)


def cutter_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, CUTTER, scenario)


def off_the_lizard(seed: int = 7) -> World:
    """The frigate standing ESE off the Lizard at ten past eleven (truth 80's water):
    noon comes within the hour."""
    sc = Scenario(
        start_time=dt.datetime(1805, 6, 12, 11, 10),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=112.0,
        ship_speed_kn=6.0,
        position={"lat_deg": 49.75, "lon_deg": -5.45},
        region="channel-west",
    )
    world = make_world(seed, FRIGATE, sc)
    world.submit("set plain sail")
    world.submit("steer ESE")
    world.run(600)
    world.submit("trim sails")
    world.run(1800)
    return world


def seated(
    world: World, name: str, script: Any, every: int = EVERY, deck: bool = False, **kw
) -> Harness:
    """A station on `world` held by a fake (a script, or a fake made), in lockstep; with
    `deck`, the captain's word before the first sample, so the script's first reply has
    it (as `tests/test_officer.py` seats the officer)."""
    fake = script if hasattr(script, "reply") else Fake(script, **kw)
    make = STATION_FACTORIES[name]
    st = make(SamplingPolicy.in_lockstep(every, "notable", "urgent"), world=world)
    h = Harness(world, st, fake, save=lambda w, why: None)
    h.model_name, h.door = f"the fake {name}", "runner"
    if deck:
        assert world.submit("you have the deck").kind == "agent.deck"
    h.start()
    return h


def order(text: str, **args: Any) -> Reply:
    return reply("", call("submit_order", text=text, **args))


def lines(world: World, kind: str) -> list[str]:
    return [e.text for e in world.log if e.kind == kind]


def blow(world: World, knots_: float) -> None:
    """The steady wind's speed under way (as `tests/test_known_truths.py` sets it)."""
    from freesail import units

    world.wind.base_speed = world.wind.speed = units.knots_to_ms(knots_)


def samples(fake: Fake) -> list[dict[str, Any]]:
    seen: list[dict[str, Any]] = []
    for turns in fake.seen:
        for t in turns:
            if (
                t.role == "data"
                and "readings" in t.content
                and not any(t.content is s for s in seen)
            ):
                seen.append(t.content)
    return seen


# ---------------------------------------------------------------------------
# The stations as data, bound on the World
# ---------------------------------------------------------------------------


def test_the_stations_are_a_binding_on_the_world_whose_starting_state_is_the_wardroom_file():
    """The ship's stations and who holds each live on the World (`world.stations`): the
    wardroom file's `stations:` is the starting state (the cutter's mate holds the
    officer's and the master's), the kinds without a person are bound to nobody named,
    and the holder's outline builds the brief."""
    world = cutter_world()
    names = world.stations.names()
    assert ("watcher", OFFICER, CAPTAIN, MASTER, LOOKOUT, PASSENGER) == names
    mate = world.people.find("the mate")
    assert world.stations.holder(OFFICER) is mate and world.stations.holder(MASTER) is mate
    assert world.stations.holder(CAPTAIN) is world.people.captain
    assert world.stations.holder(LOOKOUT) is None and world.stations.holder(PASSENGER) is None
    st = master(world=world)
    assert st.person == mate.name and st.rank == "mate" and not st.domain.deck
    assert st.outline.startswith(mate.name) and "a good hand at the lead" in st.outline
    assert "There is no deck at this station" in MASTER_DOMAIN.words
    assert "there is no deck here to give back" in st.brief
    words = world.stations.words()
    assert f"the master ({mate.name})" in words and "the lookout (nobody named)" in words


def test_a_station_bound_to_a_new_person_at_run_time_is_taken_by_a_door_with_his_outline():
    """`bind` moves the binding: the master's station bound to the second lieutenant is
    the one a door takes, and the brief it is given names him and carries his outline;
    a station bound by hand under a new name of a kind is aboard for the sentences."""
    world = frigate_world()
    second = world.people.find("the second lieutenant")
    assert second is not None
    said = world.stations.bind(MASTER, second)
    assert said == f"The master's station is bound ({second.name})."
    assert lines(world, BOUND_KIND) == [said]
    assert world.stations.holder(MASTER) is second
    h = seated(world, MASTER, [Reply()])
    assert h.station.person == second.name
    assert f"You are the master, in the place of {second.name}" in h.brief.text()
    assert second.outline_words() in h.brief.text()
    assert world.stations.words()[3] == f"the master ({second.name})"
    # a second passenger's station under its own name, a kind's station by another name
    world.stations.bind("supercargo", None, kind=PASSENGER)
    assert "supercargo" in world.stations.names()
    assert world.stations.kind_of("supercargo") == PASSENGER
    assert world.submit("tell the supercargo we sail at dawn").kind == "agent.told"
    with pytest.raises(ValueError):
        world.stations.bind("purser's clerk", None, kind="no such kind")
    with pytest.raises(ValueError):
        world.stations.bind(MASTER, "Mr Nobody")


def test_a_station_unbound_under_a_seated_fake_releases_it_with_a_line_and_a_door_is_refused():
    """`unbind` while a model holds the station stands it down with a line saying why, as
    `stand down` does (the game saved), and a door asking for it afterwards is refused in
    words; the player's seat at it is stood down too."""
    world = frigate_world()
    saves: list[str] = []
    h = Harness(
        world,
        master(SamplingPolicy.in_lockstep(EVERY), world=world),
        Fake([Reply()]),
        save=lambda w, why: saves.append(why),
    )
    h.start()
    world.run(1)
    said = world.stations.unbind(MASTER, "the master is sent into the prize")
    assert "is unbound: the master is sent into the prize" in said
    assert h.agent.released and "unbound" in h.agent.released_reason
    assert saves and "stood down" in saves[0]
    stopped = lines(world, "agent.stopped")
    assert stopped and "the master's station is unbound" in stopped[0]
    assert lines(world, UNBOUND_KIND) == [said]
    assert MASTER not in world.stations.names() and world.stations.factory(MASTER) is None
    from freesail.agents.remote import DeskError, make_station

    with pytest.raises(DeskError) as e:
        make_station(world, MASTER, None)
    assert "There is no station 'master' aboard" in e.value.words
    # the sentences refuse it too
    with pytest.raises(OrderError):
        world.ship.handle_order("tell the master we sail at dawn")
    # and the player's seat
    world.stations.bind(MASTER, world.people.find("the master"))
    seat = seat_player(world, "master", door="console")
    world.stations.unbind(MASTER)
    assert seat.agent.released
    data = json.loads(json.dumps(world.save()))
    assert data["stations"]["unbound"] == [MASTER]


# ---------------------------------------------------------------------------
# The master's station
# ---------------------------------------------------------------------------


def test_the_masters_domain_is_the_reckoning_and_no_order_of_the_deck():
    world = frigate_world()
    h = seated(world, MASTER, [Reply()])
    allowed = ("heave the log", "heave the lead", "work up the reckoning", "take a bearing of")
    for text in ("heave the log", "work up the reckoning", "the depth of water by the chart"):
        _, why, how = tools_mod.judge(world, MASTER, text)
        assert not why, (text, why)
    for text in (
        "set the royals",
        "steer NW",
        "tack ship",
        "let go the anchor",
        "shape a course for Falmouth",
    ):
        _, why, _ = tools_mod.judge(world, MASTER, text)
        assert why and "master may not" in why, (text, why)
    _, why, _ = tools_mod.judge(world, MASTER, "shape a course for Falmouth")
    assert "the course is the captain's" in why
    _, why, _ = tools_mod.judge(world, MASTER, "set the reckoning to 49 N 5 W")
    assert "overruling of the master" in why
    # no deck: an order of his is judged by the domain alone, nothing gives him one
    result = tools_mod.call(world, MASTER, "submit_order", {"text": "heave the log"})
    assert "has not the deck" not in result
    with pytest.raises(OrderError):  # the deck's sentences are the officer's station's
        world.ship.handle_order("master, you have the deck")
    with pytest.raises(OrderError) as e:
        h.give_deck()
    assert "There is no deck at the master's station" in str(e.value)
    assert (
        not MASTER_DOMAIN.deck and MASTER_DOMAIN.why_not("heave the log", "navigation", "1") is None
    )
    assert allowed and h.agent.wants_deck is False


def test_the_master_works_the_reckoning_at_noon_and_his_figure_is_the_ships_account():
    """G19's third step: at noon the master's station is sampled with the slate in its
    notice; the fake works it by the traverse and gives his figure within the working's
    time, which is then the ship's account (the log says whose); the slate begins again
    at it."""
    world = off_the_lizard()
    fake = master_of_the_reckoning()
    h = seated(world, MASTER, fake, every=3600)
    assert MASTER_KINDS <= h.policy.kinds
    world.run(1800)
    noon = [e for e in world.log if e.kind == "reckoning.noon"]
    assert len(noon) == 1
    working = [e for e in world.log if e.kind == MASTER_WORKING_KIND]
    assert working and working[0].tick == noon[0].tick
    assert "has the slate to work the noon" in working[0].text
    told = [
        s
        for s in samples(fake)
        if any("The reckoning is to be worked" in n for n in s.get("notices", []))
    ]
    assert len(told) == 1 and "The master's slate since" in told[0]["notices"][0]
    own = [e for e in world.log if e.kind == "reckoning.own"]
    assert own and own[0].data.get("adopted") and own[0].severity is Severity.NOTABLE
    assert h.agent.samples >= 2
    assert f"worked at the master's station by {h.station.person} (the fake master" in own[0].text
    assert own[0].data["from_master_nm"] < 0.5
    assert not [e for e in world.log if e.kind == MASTER_STOOD_KIND]
    assert world.navigation.master_working is None
    assert world.navigation.reckoning.slate_from["what"] == "the master's station's figure"


def test_a_figure_that_comes_too_late_leaves_the_ships_masters_standing():
    """The other way: no figure within the working's time, and the ship's own master's
    figure stands, said in the log; the account is the same as with nobody seated."""
    base = off_the_lizard()
    base.run(1800 + MASTER_WORKING_S + 60)
    world = off_the_lizard()
    seated(world, MASTER, master_of_the_reckoning(answer_in_time=False), every=3600)
    world.run(1800 + MASTER_WORKING_S + 60)
    stood = [e for e in world.log if e.kind == MASTER_STOOD_KIND]
    assert len(stood) == 1 and "none came within 30 minutes" in stood[0].text
    assert not [e for e in world.log if e.kind == "reckoning.own"]
    assert world.navigation.reckoning.position == base.navigation.reckoning.position


def test_the_captains_word_and_a_fix_open_a_working_too():
    world = off_the_lizard()
    seated(world, MASTER, [Reply()] * 6, every=3600)
    assert world.submit("work up the reckoning").kind == "reckoning.worked"
    world.run(1)
    opened = [e for e in world.log if e.kind == MASTER_WORKING_KIND]
    assert opened and "at the captain's word" in opened[-1].text
    assert world.navigation.master_working["what"].startswith("the reckoning worked up")


# ---------------------------------------------------------------------------
# The lookout's station
# ---------------------------------------------------------------------------


def test_the_lookouts_station_hails_the_deck_and_gives_no_order():
    """The lookout's domain is the glass aloft and the hail; everything else is refused in
    words; his cadence is the masthead's lines, an urgent line and the glass, never the
    notable lines of the quarterdeck; a hail is a notable line from the masthead heard on
    deck and waking a station with the deck that stands by."""
    world = off_the_lizard()
    assert not LOOKOUT_DOMAIN.deck
    st = lookout(world=world)
    assert LOOKOUT_KINDS <= st.policy.kinds and "notable" not in st.policy.events
    assert "urgent" in st.policy.events and st.policy.every_s == A_GLASS_S
    assert st.person == "the lookout" and st.rank == ""
    oh = seated(world, OFFICER, [call("stand_by", until="eight bells")], deck=True)
    assert oh.agent.standing_by
    lh = seated(world, LOOKOUT, [order("hail sail ho, two points on the larboard bow"), Reply()])
    world.run(EVERY)
    hails = [e for e in world.log if e.kind == "agent.hail"]
    assert hails and hails[0].text == (
        "The lookout, from the masthead: sail ho, two points on the larboard bow"
    )
    assert hails[0].severity is Severity.NOTABLE and hails[0].data["hail"]
    assert "officer of the watch" in hails[0].data["heard_by"]
    assert not oh.agent.standing_by  # woken: a hail from the masthead speaks of danger
    assert lh.agent.heard == [] and oh.agent.heard == []  # the hearer was woken by it
    for text in ("set the royals", "steer NW", "heave the lead", "tell the officer keep her full"):
        _, why, _ = tools_mod.judge(world, LOOKOUT, text)
        if text.startswith("tell"):
            assert not why
        else:
            assert why and "lookout gives no order" in why, (text, why)
    _, why, _ = tools_mod.judge(world, LOOKOUT, "make her out")
    assert not why
    r = world.readings["lookout"]
    assert r["held"] and "the fake lookout" in r["who"] and "sail ho" in r["last_hail"]


# ---------------------------------------------------------------------------
# A passenger's station
# ---------------------------------------------------------------------------


def test_a_passenger_hears_a_say_on_the_quarterdeck_and_can_give_no_order():
    world = frigate_world()
    assert not PASSENGER_DOMAIN.deck and passenger(world=world).person == "a person aboard"
    ph = seated(world, PASSENGER, passenger_aboard(["a fine morning for it"]))
    oh = seated(world, OFFICER, [order("say the glass is falling"), Reply()])
    lh = seated(world, LOOKOUT, [Reply()] * 4)
    world.run(2 * EVERY + 1)
    heard = [s["heard"] for s in samples(ph.model) if s.get("heard")]
    assert heard and "on the quarterdeck: the glass is falling" in heard[0][0]
    assert heard[0][0].startswith("The officer of the watch (")
    assert not [s for s in samples(lh.model) if s.get("heard")]
    spoke = [e for e in world.log if e.kind == "agent.spoke" and e.data["station"] == OFFICER]
    assert (
        spoke
        and PASSENGER in spoke[0].data["heard_by"]
        and LOOKOUT not in spoke[0].data["heard_by"]
    )
    assert any("a fine morning for it" in t for t in lines(world, "agent.spoke"))
    for text in ("set the royals", "heave the lead", "steer NW"):
        _, why, _ = tools_mod.judge(world, PASSENGER, text)
        assert why and "a passenger gives no order" in why, (text, why)
    _, why, _ = tools_mod.judge(world, PASSENGER, "ask the master for a course")
    assert not why
    assert oh.agent.has_deck is False


# ---------------------------------------------------------------------------
# The stand-by on several conditions
# ---------------------------------------------------------------------------


def test_a_stand_by_on_several_conditions_wakes_on_any_and_names_which():
    world = frigate_world()
    world.submit("set plain sail")
    h = seated(
        world,
        OFFICER,
        [
            call(
                "stand_by",
                until="eight bells, or the true wind exceeds 20 knots, or a sail sighted",
            ),
            Reply(),
            Reply(),
        ],
        deck=True,
    )
    world.run(1)
    sb = h.agent.stand_by
    assert sb is not None and h.agent.standing_by
    assert sb.event == "eight bells" and sb.others[0].condition == "the true wind exceeds 20 knots"
    assert sb.others[1].event == "a sail sighted" and sb.bound is None
    assert sb.words == "eight bells, or the true wind exceeds 20 knots, or a sail sighted"
    world.run(EVERY)
    assert h.agent.standing_by
    blow(world, 24.0)
    world.run(2)
    resumed = [e for e in world.log if e.kind == "agent.resumed"]
    assert resumed and "the true wind exceeds 20 knots" in resumed[-1].text
    assert (
        "(one of: eight bells, or the true wind exceeds 20 knots, or a sail sighted)"
        in resumed[-1].text
    )


def test_a_condition_the_book_cannot_read_is_refused_in_the_dialects_words():
    world = frigate_world()
    h = seated(world, OFFICER, [Reply()], deck=True)
    world.run(1)
    said = h.stand_by("eight bells, or the moon is blue")
    assert "'the moon is blue' is not an event" in said and "standing dialect" in said
    assert not h.agent.standing_by
    # the dialect's own 'or' inside one condition reads as one
    said = h.stand_by("the true wind veers 1 point or backs 1 point")
    assert said.startswith("Standing by until the true wind veers 1 point or backs 1 point")
    assert h.agent.stand_by is not None and not h.agent.stand_by.others
    # a wait with the deck for an event still ends at eight bells
    h.agent.state = "stationed"
    h.agent.stand_by = None
    said = h.stand_by("a sail sighted, or the land is in sight")
    assert h.agent.stand_by.bound == "eight bells"


# ---------------------------------------------------------------------------
# The deck's conversation, and who may give what
# ---------------------------------------------------------------------------


def test_a_station_asks_another_and_the_answer_comes_back_or_the_asker_is_told():
    """`ask the master for a course` from the captain's station: the master's sample
    carries the question under the asker's name and place, his answer goes back as the
    captain's word, and when no answer comes by the master's patience the asker is
    told."""
    world = frigate_world()
    ch = seated(
        world,
        CAPTAIN,
        captain_of_the_ship(
            ["ask the master for a course", "tell the master to work up the reckoning"]
        ),
    )
    mh = seated(
        world,
        MASTER,
        [
            Reply(),
            reply("", call("answer", text="South-east by south, sir, for the Lizard.")),
            Reply(),
            Reply(),
            Reply(),
        ],
    )
    world.run(EVERY + 1)
    asked = [e for e in world.log if e.kind == "agent.asked"]
    assert asked and asked[0].text.startswith("The captain (")
    assert (
        "on the quarterdeck, asks the master: for a course?" in asked[0].text
        or "asks the master: a course?" in asked[0].text
    )
    q = [s["question"] for s in samples(mh.model) if s.get("question")]
    assert q and q[0].startswith("the captain (") and "asks: " in q[0]
    world.run(EVERY)
    said = [e for e in world.log if e.kind == "agent.said"]
    assert said and said[0].data["to"] == CAPTAIN
    words = [s["word"] for s in samples(ch.model) if s.get("word")]
    assert words and "answers your question" in words[-1] and "South-east by south" in words[-1]
    assert ch.agent.asked == []
    world.run(EVERY)
    told = [e for e in world.log if e.kind == "agent.told"]
    assert told and "to the master: work up the reckoning" in told[-1].text
    # unanswered by the patience: the asker told
    world2 = frigate_world()
    ch2 = seated(world2, CAPTAIN, captain_of_the_ship(["ask the lookout what she is"]))
    seated(world2, LOOKOUT, [Reply()] * 40)
    world2.run(EVERY + 1)
    assert ch2.agent.asked and ch2.agent.asked[0][0] == LOOKOUT
    world2.run(4 * 3600 + EVERY)
    notices = [n for s in samples(ch2.model) for n in s.get("notices", [])]
    notices += list(ch2.agent.notices)  # for his next sample, if none has come yet
    assert any("No answer has come from the lookout" in n for n in notices)
    assert ch2.agent.asked == []


def test_a_say_at_the_prompt_is_the_captains_and_a_station_may_not_give_the_owners_sentences():
    world = frigate_world()
    oh = seated(world, OFFICER, [Reply()] * 4)
    mh = seated(world, MASTER, [Reply()] * 4)
    e = world.submit("say we shall have a blow before night")
    assert e.kind == "agent.spoke" and e.text.startswith("The captain, on the quarterdeck: ")
    assert set(e.data["heard_by"]) == {OFFICER, MASTER}
    assert (
        oh.agent.heard and mh.agent.heard and "The captain, on the quarterdeck" in oh.agent.heard[0]
    )
    assert world.journal[-1][2] == "say we shall have a blow before night"  # an order, replayed
    for station in (OFFICER, MASTER):
        for text in (
            "you may heave to",
            "stand down the master",
            "resume the officer",
            "you have the deck",
        ):
            _, why, _ = tools_mod.judge(world, station, text)
            assert why and "may not" in why, (station, text)
    # the player's seat speaks as his station
    world.submit("stand down the master")
    world.run(1)
    seat = seat_player(world, "master", door="console")
    e = seat.route("say the lead gives twenty fathoms")
    assert e.kind == "agent.spoke" and e.text.startswith("The master (")
    assert ", the player, on the quarterdeck: the lead gives twenty fathoms" in e.text
    assert e.actor == "the master (the player)"


def test_you_may_flows_down_the_ranks_and_the_master_takes_a_named_thing():
    world = frigate_world()
    world.submit("set plain sail")
    world.run(900)
    mh = seated(world, MASTER, [Reply()] * 6)
    # the owner, by name
    e = world.submit("master, you may heave to")
    assert e.kind == "agent.deck" and e.data["station"] == MASTER
    assert [g.verb for g in mh.grants()] == ["heave to"]
    _, why, how = tools_mod.judge(world, MASTER, "heave to")
    assert not why and how == "a named grant"
    assert world.submit("master, you may not heave to").kind == "agent.deck"
    assert mh.grants() == ()
    e = world.submit("you may work the ship")  # the officer's: nobody holds that station
    assert e.kind == "order.rejected"
    # the captain's station, to the master's
    ch = seated(world, CAPTAIN, captain_of_the_ship(["master, you may wear ship"]))
    world.run(EVERY + 1)
    assert "By the captain: master, you may wear ship." in lines(world, "order.accepted")
    assert [g.verb for g in mh.grants()] == ["wear ship"]
    assert ch.agent.has_deck
    # the person's name does as well
    e = world.submit(f"{mh.station.person}, you may tack ship")
    assert e.kind == "agent.deck" and e.data["station"] == MASTER, e.text


def test_the_rules_based_captain_gives_a_seated_officer_the_deck_and_takes_it_back_to_evade():
    """On an intent scenario with nobody at the captain's station, the officer seated is
    given the deck by the captain's own words at his judgement, his book over it; a
    stranger to evade takes it back, saying so; the quiet state gives it again."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/trials/trial-trade-stranger.yaml")
    world = make_scenario_world(sf)
    begin(world, sf)
    cap = world.captain
    oh = seated(world, OFFICER, officer_of_the_watch())
    assert not oh.agent.deck
    world.run(C.JUDGE_FIRST_S + 1)
    assert cap.commands and cap.state == "on passage" and oh.agent.deck
    given = [e for e in world.log if e.kind == "agent.deck" and e.data.get("by") == "rule"]
    assert (
        given and given[0].data["deck"] == "given" and given[0].actor.startswith("captain's rule")
    )
    assert "by his rule, on passage; his standing orders stand over it" in given[0].text
    world.run(3700 - world.clock.tick)
    assert cap.state == "evading"
    taken = [e for e in world.log if e.kind == "agent.deck" and e.data.get("by") == "rule"]
    assert taken[-1].data["deck"] == "taken" and not oh.agent.deck
    assert "takes the deck for a judgement that needs it: evading" in taken[-1].text
    world.run(8100 - world.clock.tick)
    assert cap.state == "on passage" and oh.agent.deck


# ---------------------------------------------------------------------------
# The player's seat at the lesser stations
# ---------------------------------------------------------------------------


def test_the_player_is_seated_at_the_master_and_the_lookout_with_each_stations_authority():
    world = off_the_lizard()
    seat = seat_player(world, "master", door="console")
    assert seat.station.name == MASTER and not seat._wants_deck
    assert "there is no deck at it" in lines(world, "seat.taken")[0]
    e = seat.route("heave the lead")
    assert e.kind != "agent.refused", e.text
    e = seat.route("set the royals")
    assert e.kind == "agent.refused" and "master may not" in e.text
    assert world.readings["master"]["station"]["who"] == "the player, through the console"
    world.submit("stand down the master")
    seat = seat_player(world, "lookout", door="browser")
    e = seat.route("hail land ho, on the starboard bow")
    assert e.kind == "agent.hail" and e.actor == "the lookout (the player)"
    assert world.readings["lookout"]["who"] == "the player, through the browser"
    e = seat.route("steer NW")
    assert e.kind == "agent.refused" and "lookout gives no order" in e.text
    with pytest.raises(OrderError):
        seat_player(world, "captain")
    world.submit("stand down the lookout")
    seat = seat_player(world, "passenger", door="console")
    assert seat.station.name == PASSENGER
    assert seat.route("heave the lead").kind == "agent.refused"
    assert place_of(world, PASSENGER) == "quarterdeck"


# ---------------------------------------------------------------------------
# The doors, and the pace rule
# ---------------------------------------------------------------------------


def test_the_doors_ask_the_worlds_binding_and_a_held_station_is_refused_to_a_second_door(tmp_path):
    """Through the agent API: the master's station taken by a door, with the holder's
    name in the brief; the same station asked for by another identity refused in words;
    a station the ship has not got refused in words; the cadence a setting of the
    seating, said in the stationed line and in the brief."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    world = frigate_world()
    records = tmp_path / "consent"
    records.mkdir()
    for identity in (WEIGHTS, "another-made-up-model.gguf"):
        consent.Record(
            identity, "a test runtime", "2026-10-10", consent.YES, answer="Yes.", drill="passed"
        ).write(records)
    driver = Driver(world, compression=60.0)
    app = create_app(driver, game="a test", consent_records=records, saves_dir=tmp_path / "saves")
    with TestClient(app) as http:
        a = http.post(
            "/api/agents/master", json={"model_name": WEIGHTS, "door": "mcp", "cadence": "events"}
        ).json()
        assert a["phase"] == "station" and a["station"] == MASTER
        h = world.agents[MASTER]
        assert h.station.person == world.people.find("the master").name
        assert h.policy.every_s is None and MASTER_KINDS <= h.policy.kinds
        stationed = lines(world, "agent.stationed")
        assert "sampled on notable and urgent events and on the reckoning's lines" in stationed[0]
        assert "that is this seating's cadence" in h.brief.text()
        r = http.post(
            "/api/agents/master", json={"model_name": "another-made-up-model.gguf", "door": "mcp"}
        )
        assert r.status_code == 409 and "taken by nobody else" in r.json()["detail"]
        r = http.post("/api/agents/purser", json={"model_name": WEIGHTS, "door": "mcp"})
        assert r.status_code == 404 and "no station 'purser' aboard" in r.json()["detail"]
        r = http.post(
            "/api/agents/lookout", json={"model_name": WEIGHTS, "door": "mcp", "cadence": "hourly"}
        )
        assert r.status_code == 400 and "cadence" in r.json()["detail"]
        state = http.get("/api/state").json()["driver"]
        assert (
            state["pace"]["rule"] == "pace"
            and state["pace"]["held"]
            and state["pace"]["open"][0]["station"] == MASTER
        )


def test_the_pace_rule_holds_the_clock_at_1x_while_a_sample_is_open_and_a_stand_by_releases_it():
    from freesail.ui.console import PACE_HELD_SAID_S, Pace

    world = frigate_world()
    pace = Pace(world)

    class Late:
        def __init__(self) -> None:
            self.asked = 0

        def reply(self, turns):
            self.asked += 1
            return None

    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(EVERY), world=world),
        Late(),
        save=lambda w, why: None,
    )
    h.start()
    assert h.open_sample is not None
    assert open_samples(world) == [
        {"station": OFFICER, "since_tick": 0, "since": world.clock.stamp(), "reason": "the start"}
    ]
    assert pace.rate(60.0, now=10.0) == 1.0
    d = pace.state(60.0, now=20.0)
    assert d["held"] and d["rate"] == 1.0 and d["open"][0]["for_s"] == 10
    assert world.readings["pace"]["rate"] == 1.0 and "held at 1x" in world.readings["pace"]["words"]
    assert "pace" not in tools_mod.readings_words(world)
    # the long hold said once
    assert pace.rate(60.0, now=10.0 + PACE_HELD_SAID_S) == 1.0
    assert pace.rate(60.0, now=20.0 + PACE_HELD_SAID_S) == 1.0
    held = [e for e in world.log if e.kind == "driver.pace"]
    assert len(held) == 1 and "held at 1x for the officer of the watch" in held[0].text
    h.deliver(Reply(text="Nothing yet."))
    world.compression = 60.0
    assert h.open_sample is None and pace.rate(60.0, now=30.0) == 60.0
    assert world.readings["pace"]["words"].startswith("the clock runs at 60x; no sample is open")
    world.run(EVERY)
    assert h.open_sample is not None and pace.rate(60.0) == 1.0
    h.deliver(Reply(calls=(call("stand_by", until="eight bells"),)))
    assert h.agent.standing_by and pace.rate(60.0) == 60.0
    # lockstep and free-running are the other rules
    assert Pace(world, "free").rate(60.0) == 60.0 and Pace(world, "lockstep").rate(60.0) == 60.0
    assert world.pace_rule == "lockstep"
    # a replay's recorded station never holds the clock
    from freesail.agents.harness import Playback

    h2 = Harness(
        frigate_world(),
        officer(SamplingPolicy.in_lockstep(EVERY)),
        Playback(world, []),
        save=lambda w, why: None,
    )
    h2.start()
    assert h2.open_sample is not None and open_samples(h2.world) == []


def test_the_cadence_policies_and_the_doors_flags():
    assert cadence_policy("glass", OFFICER).every_s == A_GLASS_S
    assert cadence_policy("watch", MASTER).every_s == 4 * 3600
    p = cadence_policy("events", LOOKOUT)
    assert (
        p is not None and p.every_s is None and p.kinds == LOOKOUT_KINDS and p.events == {"urgent"}
    )
    assert cadence_policy("hourly", OFFICER) is None
    assert p.describe() == "on urgent events and on the masthead's lines"
    from freesail.agents import local, mcp_server, repl

    for module in (mcp_server, local):
        src = Path(module.__file__).read_text(encoding="utf-8")
        assert '"--cadence"' in src and 'choices=["watcher", "officer", "captain"]' not in src
    world = cutter_world()
    import argparse

    st = repl._station(argparse.Namespace(station="master", every=EVERY), world)
    assert st.name == MASTER and st.person == world.people.find("the mate").name
    with pytest.raises(SystemExit):
        repl._station(argparse.Namespace(station="purser", every=EVERY), world)
    assert R.REGISTRY.get("pace").kind in R.DRIVER_KINDS


def test_a_game_with_three_seated_checkpoints_and_each_reseated_station_reads_its_own_journal(
    tmp_path,
):
    world = cutter_world()
    world.submit("set plain sail")
    ch = seated(world, CAPTAIN, captain_of_the_ship(["you have the deck"]))
    oh = seated(world, OFFICER, officer_of_the_watch())
    seat = seat_player(world, "master", door="console")
    world.run(2 * EVERY + 1)
    ch.note("The captain's own note.")
    oh.note("The officer's own note.")
    seat.note("The master's own note, by the player.")
    replay.write_checkpoint(world, tmp_path / "three.ckpt")
    _header, back = replay.read_checkpoint(tmp_path / "three.ckpt")
    assert set(back.agents) == {CAPTAIN, OFFICER} and back.player_seat.station.name == MASTER
    assert back.agents[OFFICER].agent.has_deck and back.agents[CAPTAIN].agent.has_deck
    for name, note in ((CAPTAIN, "The captain's own note."), (OFFICER, "The officer's own note.")):
        h = back.agents[name]
        h.take_over(Fake([reply("", call("read_journal", kind="notes"))]))
        read = tools_mod.call(back, name, "read_journal", {"kind": "notes"})
        assert any(e["text"] == note for e in read["entries"]), name
        assert note in h.brief.text() or "The station's journal" in h.brief.text()
    read = tools_mod.read_journal(back, MASTER, kind="notes")
    assert any(e["text"] == "The master's own note, by the player." for e in read["entries"])
    assert (
        "stations" in json.loads(json.dumps(back.save()))
    ) and back.stations.names() == world.stations.names()
    copy = replay.replay(replay.load_file(_save(world, tmp_path)), ship_factory)
    assert copy.log.digest() == world.log.digest()


def _save(world: World, tmp_path: Path) -> Path:
    path = tmp_path / "three.json"
    path.write_text(json.dumps(json.loads(json.dumps(world.save()))))
    return path
