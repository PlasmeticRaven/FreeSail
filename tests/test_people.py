"""The people (spec M5 §22; package 35): the named few from the muster, each with a
name, a role, a skill, a place and a state; the orders that move them where the period's
orders did; a task that occupies a person; the message that reaches the captain where
he is; the readings and the standing dialect's words for them."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.orders.errors import OrderError
from freesail.world import people as PE

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}


def world_for(ship=FRIGATE, start=datetime(1805, 6, 10, 10, 0), **kw):
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=OFF_THE_LIZARD,
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


def test_the_named_few_come_from_the_muster_by_post_and_by_the_ship_files_roles():
    """The frigate's: the captain, three lieutenants, the master, the standing officers,
    two master's mates and a midshipman as the messenger; each a sailor of the muster,
    so the counts of spec M3 §2.3 are what they were and the names are the muster's."""
    w = world_for()
    people = w.people
    roles = [p.role for p in people.all]
    assert roles[:5] == [
        "captain",
        "first lieutenant",
        "second lieutenant",
        "third lieutenant",
        "master",
    ]
    assert roles.count("master's mate") == 2 and roles.count("midshipman") == 1
    for role in ("surgeon", "purser", "boatswain", "carpenter", "sailmaker"):
        assert role in roles
    crew = w.ship.extra["crew"]
    ids = {s.id for s in crew.sailors}
    assert all(p.sailor_id in ids for p in people.all)
    assert len({p.sailor_id for p in people.all}) == len(people.all)  # one sailor, one person
    assert crew.complement == 264
    assert people.captain.name.startswith("Captain ") and people.captain.role == "captain"
    assert people.messenger is not None and people.messenger.role == "midshipman"
    assert people.messenger.name.startswith("Mr ")
    mate = people.by_role("master's mate")[0]
    assert crew.by_id[mate.sailor_id].rating.value == "able"  # drawn from the forecastle's able
    # the master is package 33a's, now a person whole: one name, one place
    master = people.find("the master")
    assert master is not None and master.mirror is w.navigation.master
    assert master.name == w.navigation.master.name and master.skill == w.navigation.master.skill
    # the small vessels: the master and a mate (the schooner, the cutter), a boy to carry
    # the word; the brig a midshipman and a master's mate as the frigate in small
    for path, wanted in (
        (SCHOONER, ["master", "mate", "boatswain", "boy"]),
        (CUTTER, ["master", "mate", "boatswain", "boy"]),
    ):
        ws = world_for(path)
        assert [p.role for p in ws.people.all] == wanted, path
        assert ws.people.captain.role == "master" and ws.people.messenger.role == "boy"
    brig = world_for(BRIG).people
    assert brig.captain.role == "commander" and brig.messenger.role == "midshipman"
    assert [p.role for p in brig.all][-2:] == ["master's mate", "midshipman"]


def test_the_people_and_where_is_are_readings_in_the_registry_and_at_the_prompt():
    w = world_for()
    said = w.readings.words("people")
    assert said.startswith(f"{w.people.captain.name}: on the quarterdeck. ")
    assert "master: on the quarterdeck." in said and "sailmaker: in the sail room." in said
    e = w.submit("the people")
    assert e.kind == "query.reading" and e.text == f"The people: {said}"
    e = w.submit("where is the carpenter")
    assert e.kind == "query.reading" and e.text.endswith(", carpenter, on the deck.") is False
    carpenter = w.people.find("the carpenter")
    assert e.text == f"Where is the carpenter: {carpenter.name}, on the deck."
    e = w.submit(f"where is {carpenter.surname}")
    assert e.text == f"Where is {carpenter.surname}: {carpenter.name}, on the deck."
    assert w.readings.value("where_is", "the master")["place"] == "on deck"
    e = w.submit("where is the chaplain")
    assert e.kind == "order.rejected" and "Nobody aboard answers to 'the chaplain'" in e.text
    # the standing dialect reads a person by his place, as the master's row always did
    e = w.submit('standing order "x": when the master is below then heave to')
    assert e.kind == "standing.given"


def test_send_for_brings_a_man_to_where_the_captain_is_by_the_messenger():
    w = world_for()
    carpenter = w.people.find("the carpenter")
    assert carpenter.where == "deck"
    e = w.submit("send for the carpenter")
    assert e.kind == "person.sent_for"
    assert e.text == (
        f"Passed the word for {carpenter.name} by {w.people.messenger.name}; he is on the deck."
    )
    assert carpenter.pending is not None and "sent for, on his way" in w.people.state_words(
        carpenter
    )
    again = w.submit("pass the word for the carpenter")
    assert again.kind == "order.rejected" and "sent for already" in again.text
    w.run(PE.PASS_THE_WORD_S - 1)
    assert not events(w, "person.came")
    w.run(1)
    came = events(w, "person.came")
    assert len(came) == 1 and came[0].text == f"{carpenter.name} came aft, sent for."
    assert carpenter.where == "quarterdeck" and carpenter.pending is None
    # the captain below: the man comes to the cabin
    w.submit("go below")
    assert w.people.captain.where == "cabin"
    surgeon = w.people.find("the doctor")
    assert surgeon.role == "surgeon"
    w.submit("send for the surgeon")
    w.run(PE.PASS_THE_WORD_S)
    assert (
        surgeon.where == "cabin"
        and events(w, "person.came")[-1].text == f"{surgeon.name} came to the cabin, sent for."
    )
    assert w.people.state_words(surgeon) == "in the cabin"
    w.submit("come on deck")
    assert w.people.captain.where == "quarterdeck"
    # refusals in words
    e = w.submit("send for the captain")
    assert e.kind == "order.rejected" and "no sending for yourself" in e.text
    e = w.submit("send for the chaplain")
    assert e.kind == "order.rejected" and "Nobody aboard answers to 'chaplain'" in e.text
    e = w.submit("send for the first lieutenant")
    assert "already" in e.text  # he is on the quarterdeck with the captain
    e = w.submit("come on deck")
    assert e.kind == "order.rejected" and "already" in e.text


def test_a_task_occupies_a_person_and_a_second_call_on_him_is_refused_in_words():
    """The master's day's work, the lunar and the boat occupy a person until a tick: the
    log says so, `where is` reads it, and `send for` is refused while he is at it."""
    w = world_for()
    master = w.people.find("the master")
    until = w.clock.tick + 600
    assert w.people.occupy(master, "gunroom", until, "day's work") is None
    assert master.occupied and w.navigation.master.occupied  # the one state, through the mirror
    assert w.people.state_words(master) == "at the day's work, in the gunroom"
    assert w.submit("where is the master").text.endswith("at the day's work, in the gunroom.")
    e = w.submit("send for the master")
    assert e.kind == "order.rejected" and "is at the day's work and will be free at" in e.text
    assert w.people.occupy(master, "gunroom", until, "lunar") is not None  # busy already
    w.run(600)
    assert not master.occupied and master.where == "quarterdeck"
    assert events(w, "master.place")[-1].text == f"{master.name} came on deck, the day's work done."
    # a person without the mirror: the messenger carrying a letter is occupied a minute
    boy = w.people.messenger
    assert w.people.occupy(boy, "deck", w.clock.tick + 60, "errand") is None
    assert w.people.state_words(boy) == "at the errand, on the deck"
    w.run(60)
    assert (
        not boy.occupied
        and events(w, "person.free")[-1].text == f"{boy.name} is done with the errand."
    )


def test_a_watch_keeper_in_his_watch_below_at_night_is_asleep_by_the_bill():
    w = world_for(start=datetime(1805, 6, 10, 2, 0))  # the middle watch
    second = w.people.find("the second lieutenant")
    third = w.people.find("the third lieutenant")
    assert {second.watch, third.watch} == {"starboard", "larboard"}
    from freesail.crew import bill

    on_duty = bill.watch_on_duty(w.clock.ship_time).value
    awake = second if second.watch == on_duty else third
    asleep = third if awake is second else second
    assert w.people.state_words(awake) == "on the quarterdeck"
    assert w.people.state_words(asleep) == "below, asleep"
    assert w.readings.value("where_is", asleep.role)["place"] == "below"
    # the first lieutenant and the master keep no watch; the captain is never asleep by the bill
    assert w.people.state_words(w.people.find("the first lieutenant")) == "on the quarterdeck"
    assert w.people.state_words(w.people.captain) == "on the quarterdeck"
    # sent for, he is up: the order outranks the bill
    e = w.submit(f"send for the {asleep.role}")
    assert e.kind == "person.sent_for" and e.text.endswith("; he is below, asleep.")
    assert "sent for, on his way" in w.people.state_words(asleep)
    w.run(PE.PASS_THE_WORD_S)
    assert w.people.state_words(asleep) == "on the quarterdeck"
    assert (
        events(w, "person.came")[-1].text == f"{asleep.name} came aft, called from his watch below."
    )
    w.run(600)
    assert w.people.state_words(asleep) == "on the quarterdeck"  # not asleep again this watch
    e = w.submit(f"send for the {asleep.role}")
    assert e.kind == "person.sent_for" and "already" in e.text


def test_a_message_reaches_the_captain_where_he_is_through_the_messenger_and_the_door():
    w = world_for()
    w.submit("go below")
    lines = w.people.message_aboard(
        PE.Message(
            "The admiral desires a return of defaulters.", "Plymouth", carried_by="the pilot cutter"
        )
    )
    assert [kind for _, kind, _, _ in lines] == ["message.aboard"]
    assert (
        "came aboard by the pilot cutter" in lines[0][2] and w.people.messenger.name in lines[0][2]
    )
    for severity, kind, text, data in lines:
        w.record(severity, kind, text, data=data)
    w.run(PE.PASS_THE_WORD_S)
    door = events(w, "message.door")
    got = events(w, "message.received")
    assert len(door) == 1 and len(got) == 1 and door[0].tick == got[0].tick
    assert (
        door[0].text
        == f"{w.people.messenger.name} knocked at the cabin door with a letter from Plymouth."
    )
    assert got[0].text == "The captain read it: The admiral desires a return of defaulters."
    assert w.log._events.index(door[0]) < w.log._events.index(got[0])


def test_the_people_are_a_function_of_the_seed_and_the_journal_and_a_checkpoint_holds_them(
    tmp_path,
):
    from freesail.core import replay

    a, b = world_for(), world_for()
    for w in (a, b):
        w.submit("send for the carpenter")
        w.submit("go below")
        w.run(120)
    assert a.log.digest() == b.log.digest()
    assert [p.to_dict() for p in a.people.all] == [p.to_dict() for p in b.people.all]
    path = replay.write_checkpoint(a, tmp_path / "people.ckpt")
    _, c = replay.read_checkpoint(path)
    assert [p.to_dict() for p in c.people.all] == [p.to_dict() for p in a.people.all]
    a.run(300)
    c.run(300)
    assert a.log.digest() == c.log.digest()
    # a world on the endless plane keeps the captain and nobody else to send for
    from freesail.core.world import World

    bare = World(seed=1)
    assert [p.role for p in bare.people.all] == ["captain"]
    with pytest.raises(OrderError):
        bare.people.send_for("the master")


def test_the_pilot_is_a_person_aboard_of_his_port_and_waits_for_his_boat():
    """Package 37h: the pilot aboard is one of the people, said as the pilot of his port
    (a supernumerary, the Regulations' Pilot's art. I), found by 'the pilot' and by his
    surname, and at the gangway once he has asked for his boat."""
    w = world_for()
    pilot = w.people.add(PE.Person("pilot-falmouth-1", "Mr Hocking", "pilot", 0.9, port="falmouth"))
    w.ports.pilot, w.ports.pilot_port = pilot, "falmouth"
    assert w.people.find("the pilot") is pilot and w.people.find("Hocking") is pilot
    said = w.readings.words("people")
    assert "Mr Hocking, pilot of Falmouth: on the quarterdeck." in said
    w.ports.pilot_boat_asked = True
    w.run(1)  # the readings are the tick's
    assert "Mr Hocking, pilot of Falmouth: at the gangway, waiting for his boat." in (
        w.readings.words("people")
    )
    assert w.people.where_is("the pilot")["state"] == "at the gangway, waiting for his boat"


# ---------------------------------------------------------------------------
# Package 52 (spec M7b §8, §9): people made from words, the company's people by trade, the
# galley and earshot
# ---------------------------------------------------------------------------


def test_a_person_made_from_words_has_his_outline_from_them():
    """`person: make "<name>", ...`: who he is, his age, where he is and his history from
    the words in any order, kept as his outline; a role or none; among the people from
    then on, by his name and by his role."""
    w = world_for(ports=["falmouth", "brest"])
    for text in (
        'person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Brest, who knew the '
        "captain's father",
        'person: make "Mrs Tregarthen", aboard in the cabin, a widow, aged forty, going home',
        'person: make "Jenkins", in the gunroom',
        'person: make "Mr Gill", a merchant of Brest, 45 years old',
    ):
        e = w.world_order(text, "the test")
        assert e.data["result"] == "done", e.text
    fox = w.people.find("Mr Fox")
    assert fox.role == "pilot" and not fox.aboard and fox.port == "brest"
    assert fox.outline.age == 60 and fox.outline.rank == "Guernsey pilot"
    assert fox.outline_words() == (
        "Mr Fox, Guernsey pilot, sixty years of age, who knew the captain's father."
    )
    widow = w.people.find("Mrs Tregarthen")
    assert widow.aboard and widow.where == "cabin" and widow.outline.age == 40
    assert widow.outline.history == "going home" and w.people.find("the widow") is widow
    jenkins = w.people.find("Jenkins")
    assert jenkins.role == "" and jenkins.where == "gunroom"
    gill = w.people.find("Mr Gill")
    assert gill.role == "merchant" and gill.outline.rank == "merchant of Brest"
    assert gill.outline.age == 45 and gill.aboard and gill.where == "cabin"
    said = " ".join(w.people.describe())
    # ashore at his port, where his role is found (package 53: the pilots' office)
    assert "Mr Fox, pilot of Brest: ashore at Brest, at the pilots' office." in said
    assert "Jenkins: in the gunroom." in said
    # refused in words: a name taken, a place that is none, a port that is none
    for text, words in (
        ('person: make "Mr Fox", a cooper', "among the people already"),
        ('person: make "Mr Hale", aboard in the crow\'s nest', "no place aboard"),
        ('person: make "Mr Hale", ashore at Atlantis', "no port of the world"),
    ):
        e = w.world_order(text, "the test")
        assert e.data["result"] == "refused" and words in e.text, e.text


def test_a_man_of_the_muster_by_his_trade_is_drawn_only_when_the_voice_reaches_him():
    """The cook is an idler of the muster, not one of the named few: nobody finds him and
    `the people` does not list him until the director's voice reaches for him
    (`of_the_company`), when he is drawn under his own name at the galley, and is the
    same man after."""
    w = world_for()
    before = w.people.describe()
    assert w.people.find("the cook") is None
    look = w.people.of_the_company("the cook", draw=False)
    assert look is not None and look.where == "galley" and w.people.find("the cook") is None
    assert w.people.describe() == before  # a look draws nobody
    cook = w.people.of_the_company("the cook")
    sailor = w.ship.extra["crew"].by_id[cook.sailor_id]
    assert sailor.trade == "cook" and cook.name.endswith(sailor.name.split()[-1])
    assert w.people.find("the cook") is cook and w.people.of_the_company("cook") is cook
    assert w.people.describe()[-1] == f"{cook.name}, cook: in the galley."
    assert w.people.of_the_company("the cooper").where == "hold"
    assert w.people.of_the_company("the ship's astrologer") is None


def test_the_galley_is_a_place_and_the_open_deck_is_within_earshot():
    from freesail.world import places as PL

    assert PL.PLACES["galley"].name == "the galley" and not PL.PLACES["galley"].below
    assert PL.place_words("galley") == "in the galley"
    assert PL.earshot("galley") == PL.earshot("quarterdeck") == {"quarterdeck", "deck", "galley"}
    assert PL.earshot("cabin") == {"cabin"} and PL.earshot("tops") == {"tops"}
    w = world_for()
    assert "the galley" in w.readings["places"]["words"]


# ---------------------------------------------------------------------------
# The needs (spec M7b §20; package 54): hunger, thirst and fatigue in steps, by hand at a
# filled station, told to the person stationed alone and never to the log
# ---------------------------------------------------------------------------


def _at_the_prompt(start=datetime(1805, 6, 10, 11, 58)):
    """A frigate with the player at the prompt (a driver listening for his lines), taken
    in hand at the first minute; the lines he is told, as the console would print them."""
    w = world_for(start=start)
    told = []
    w.needs.listen(told.append)
    w.run(60)
    cap = w.people.captain
    assert cap.needs is not None and cap.needs.by_hand
    return w, cap, told


def _behind(w, n, hours_ate=0.0, hours_drank=0.0, awake=None):
    now = w.clock.tick
    n.ate = now - int(hours_ate * 3600)
    n.drank = now - int(hours_drank * 3600)
    if awake is not None:
        n.awake_h, n.at = awake, now


def test_the_player_at_the_prompt_is_told_his_needs_at_the_change_of_the_watch_and_nobody_else():
    """No line until the second step; a notable line waits for the change of the watch and
    names together every need that has risen; nothing of it is in the log, and nobody
    unseated is told anything or has needs by hand."""
    w, cap, told = _at_the_prompt()
    lines = len(w.log)
    _behind(w, cap.needs, hours_ate=31, hours_drank=29, awake=21)  # at 11:59
    w.run(30)  # not yet the change of the watch
    assert told == []
    w.run(31)  # 12:00, eight bells: the afternoon watch
    assert [(e.severity.value, e.text) for e in told] == [
        ("notable", "You are quite thirsty and quite hungry. ('drink' and 'eat')")
    ]
    assert told[0].kind == "needs.felt" and told[0].data["person"] == cap.name
    # tired (the first step) is never said; and nothing in the log
    assert w.needs.words(cap) == "quite thirsty, quite hungry and tired"
    assert not [e for e in w.log.all()[lines:] if e.kind.startswith("needs.")]
    first = w.people.find("first lieutenant")
    assert first.needs is None or not first.needs.by_hand
    assert w.needs.showing(first) == ""


def test_an_urgent_need_is_said_at_once_and_a_notable_one_once_a_watch():
    w, cap, told = _at_the_prompt(start=datetime(1805, 6, 10, 12, 30))
    _behind(w, cap.needs, hours_drank=37.99)
    w.run(120)  # parched at 38 hours: notable, which waits for the watch
    assert told == []
    _behind(w, cap.needs, hours_drank=46, hours_ate=1)
    w.run(60)
    assert [e.text for e in told] == ["You are desperately thirsty. ('drink')"]
    assert told[0].severity.value == "urgent"
    w.run(3600)
    assert len(told) == 1  # told once a step


def test_eat_and_drink_are_the_persons_own_answered_to_him_and_never_logged():
    w, cap, told = _at_the_prompt()
    _behind(w, cap.needs, hours_ate=31, hours_drank=29)
    lines = len(w.log)
    e = w.submit("eat")
    assert e.kind == "needs.answer" and e.text.startswith(
        "A biscuit and a piece of cheese are brought up from the stores; you eat on the "
        "quarterdeck, the first since"
    )
    assert w.submit("drink").text.startswith("You drink at the scuttle-butt, the first since")
    assert len(w.log) == lines  # answered to him, never a line of the log
    assert ("captain", "eat") not in [(a, t) for _, a, t in w.journal]
    assert {"tick": w.clock.tick, "actor": "captain", "order": "eat"} in w.inputs
    assert w.needs.words(cap) == ""
    w.submit("go below")
    assert w.submit("eat").text.startswith("You eat in the cabin")
    # the water found foul: his beer, or the foul water at a cost
    w.stores.foul = True
    assert w.submit("drink").text.startswith("The water being foul, you drink your beer")
    awake = cap.needs.awake_h
    assert w.submit("drink the foul water").text.startswith("You drink the foul water")
    assert cap.needs.awake_h == pytest.approx(awake + 6)
    # on short allowance a meal is half a meal
    w.submit("short allowance")
    assert "half meal" in w.submit("eat").text
    assert cap.needs.ate == w.clock.tick - 8 * 3600
    said = w.submit("how am i").text  # the station's line first (package 66), then the needs
    assert said.startswith("You: the captain, ") and "\nYou are " in said


def test_sleep_turns_the_player_in_below_and_his_next_order_or_his_rest_wakes_him():
    w, cap, told = _at_the_prompt()
    _behind(w, cap.needs, awake=40)
    e = w.submit("sleep")
    assert e.kind == "needs.answer" and e.text.startswith("You turn in below, in the cabin.")
    assert cap.where == "cabin" and w.people.state_words(cap) == "asleep, in the cabin"
    w.run(3600)
    assert cap.needs.awake_h == pytest.approx(32, abs=0.1)  # eight hours made up an hour
    w.submit("how am i")  # his next order wakes him, back where he turned in from
    assert not cap.needs.asleep and cap.where == "quarterdeck"
    assert told[-1].text == "You wake, on the quarterdeck."
    w.submit("sleep")
    w.run(4 * 3600 + 60)
    assert not cap.needs.asleep and cap.needs.awake_h == 0.0
    assert told[-1].text == "You wake, rested, on the quarterdeck."


def test_at_the_last_step_he_falls_asleep_where_he_stood_and_his_next_order_wakes_him():
    w, cap, told = _at_the_prompt()
    _behind(w, cap.needs, awake=55.99)
    w.run(120)
    assert cap.needs.asleep == "where he is" and cap.where == "quarterdeck"
    assert told[-1].severity.value == "urgent" and told[-1].text.startswith(
        "You have fallen asleep where you stood, on the quarterdeck. Your next order wakes you."
    )
    assert w.people.state_words(cap) == "asleep where he stood, on the quarterdeck"
    w.submit("eat")
    assert not cap.needs.asleep


def test_a_models_station_reads_its_needs_in_its_sample_and_turns_in_with_a_stand_by():
    """The officer of the watch held by a fake: his needs ride his samples (`needs` and a
    notice), never the log; `stand by, asleep below until called` is refused with the deck
    and turns him in without it; a word wakes him, back where he was. The captain, with
    nobody at the prompt, is the routine's."""
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer
    from freesail.agents.model import DATA

    w = world_for(start=datetime(1805, 6, 10, 11, 58))
    st = officer(SamplingPolicy.in_lockstep(600), world=w)
    script = [
        reply("", call("stand_by", until="asleep below until called")),
        "Aye.",
        "Off watch, sir.",
        reply("", call("stand_by", until="asleep below until called")),
        "Awake, sir.",
    ]
    fake = Fake(script, loop=False)
    h = Harness(w, st, fake, save=lambda w_, why: None)
    w.submit("you have the deck")
    h.start()
    pearce = w.stations.holder("officer of the watch")
    w.run(60)
    assert pearce.needs.by_hand and not getattr(w.people.captain.needs, "by_hand", False)
    data = [t.content for t in h.turns if t.role == DATA and "tool_results" in t.content]
    assert "has the deck: a man does not turn in on watch" in str(data[0])
    w.submit("I have the deck")  # a word: sampled, off watch
    _behind(w, pearce.needs, hours_drank=29, awake=30)
    w.run(600)  # the change of the watch at 12:00, and the glass at 12:08: he turns in
    samples = [t.content for t in h.turns if t.role == DATA and "reason" in t.content]
    last = samples[-1]
    assert last["reason"] == "the interval" and last["needs"] == "quite thirsty"
    assert "You are quite thirsty. (submit_order('drink'))" in last["notices"]
    assert not [e for e in w.log if e.kind.startswith("needs.")]
    assert pearce.needs.asleep == "below" and pearce.where == "gunroom"
    assert w.log.of_kind("agent.stood_by")[-1].text == (
        "[officer of the watch] Turned in below, in the gunroom, asleep until called."
    )
    assert w.people.state_words(pearce) == "asleep, in the gunroom"
    w.submit("tell the officer the wind is backing")
    w.tick()
    assert not pearce.needs.asleep and pearce.where == "quarterdeck"
    woke = [t.content for t in h.turns if t.role == DATA and "reason" in t.content][-1]
    assert woke["notices"][0].startswith("You stood by until asleep below until called")
    assert "You wake, on the quarterdeck." in woke["notices"]


def test_at_the_prompt_the_owner_has_no_needs_while_a_model_holds_the_captain():
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import captain

    w = world_for()
    h = Harness(
        w,
        captain(SamplingPolicy.in_lockstep(600), world=w),
        Fake(["Aye."]),
        save=lambda w_, why: None,
    )
    h.start()
    e = w.submit("eat")
    assert e.kind == "order.rejected" and "you are the owner, not the captain" in e.text
