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
