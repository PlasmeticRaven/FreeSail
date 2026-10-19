"""Package 36: the world-order channel (spec M5 §26; the proposal's §7.6; truth 71).

Orders to the world, not to the ship: the weather, a ship with a goal, a message, a port,
a person; given by a scenario file at a time or by the harness, journaled at the tick
with the source and logged at the driver's mark, saved and replayed; refused in words at
the captain's prompt; and what each causes reaches the ship through what she models.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.events import for_the_record
from freesail.core.world import Scenario
from freesail.orders.vocabulary import load_vocabulary
from freesail.world import orders as WO

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
OPEN_WATER = {"lat_deg": 49.60, "lon_deg": -5.40}
HIGH = {
    "name": "the old high",
    "kind": "high",
    "radius_km": 900,
    "track": [
        {"at": "1805-06-11T12:00", "x_km": 300, "y_km": -500, "hpa": 1024},
        {"at": "1805-06-13T12:00", "x_km": 500, "y_km": -600, "hpa": 1022},
    ],
}


def world_for(ship: str = FRIGATE, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        region="channel-west",
        **({"position": OPEN_WATER} | kw),
    )
    return make_world(7, ship, sc)


def events(world, kind: str):
    return [e for e in world.log if e.kind == kind]


def test_each_channel_is_carried_out_in_words_and_a_bad_one_refused_in_words():
    w = world_for(systems=[HIGH])
    said = {}
    for text in (
        'weather: waypoint for "the old high" at 1805-06-14T12:00 600 -700 1020',
        'weather: low "the low" radius 450 km fronts 140 300 at 1805-06-12T10:00 -300 500 990',
        'ship: a merchant brig "Two Brothers" of Britain at 49 50 N 5 30 W, '
        "trading Falmouth to Ushant",
        'ship: a brig-sloop "Palinure" of France at the Iroise, running home to Brest, no colours',
        'ship "Two Brothers": running home to Falmouth',
        'message: at Brest from the Prefect maritime: "The captain is begged to dine."',
        "port brest: closed to the United States",
        "port falmouth: price of tin 130",
        'person: supercargo "Mr Pentreath" aboard in the cabin',
        'person: agent "Mr Fox" ashore at Brest',
    ):
        e = w.world_order(text, "the test")
        assert e.kind == "world.order" and e.actor == "driver" and e.data["result"] == "done"
        assert e.text.startswith("World order (the test): ")
        said[WO.parse(text).channel] = said.get(WO.parse(text).channel, 0) + 1
    assert said == {"weather": 2, "ship": 3, "message": 1, "port": 2, "person": 2}
    # what each did
    high = w.systems.find("the old high")
    assert high is not None and high.track[-1].at == datetime(1805, 6, 14, 12, 0)
    low = w.systems.find("the low")
    assert low is not None and low.scripted and low.kind == "low"
    brig = w.vessels.find("Two Brothers")
    assert (
        brig is not None
        and brig.goal == "running home to Falmouth"
        and brig.description == "merchant brig"
    )
    pal = w.vessels.find("Palinure")
    assert pal is not None and not pal.shows_colours and pal.nation == "france"
    assert w.ports.ports["brest"].letters[0].origin == "the Prefect maritime"
    assert "united-states" in w.ports.ports["brest"].closed_to
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 130.0
    assert w.people.find("Mr Pentreath").where == "cabin"
    fox = w.people.find("Mr Fox")
    assert fox is not None and not fox.aboard and fox.port == "brest"
    # refused in words, journaled as refused, and nothing changed
    for text, words in (
        ("port nowhere: closed to France", "no port of the world"),
        (
            'ship: a ship of the line "Victory" of Britain at the Iroise, bound for Brest',
            "no description",
        ),
        ('ship "Nobody": running home to Brest', "No ship named"),
        (
            'weather: waypoint for "the old high" at 1805-06-13T00:00 0 0 1000',
            "appended comes after",
        ),
        ('person: cook "Mr Fox" aboard in the galley', "among the people already"),
        ("message: at Brest: hello", "A message order is"),
        ("weather: a gale tonight", "A weather order is"),
    ):
        e = w.world_order(text, "the test")
        assert e.data["result"] == "refused" and words in e.text, e.text
    assert w.world_orders[-1]["result"] == "refused"
    with pytest.raises(WO.WorldOrderError):
        WO.parse("set the topsails")


def test_truth_71_the_prompt_refuses_a_world_order_in_words_and_the_channels_are_one_list():
    """Truth 71's second half: the same order typed at the captain's prompt is refused;
    the refusal is the vocabulary's, and its channels are the channel's own."""
    w = world_for()
    vocab = load_vocabulary()
    assert tuple(vocab.world_order_channels) == WO.CHANNELS
    for text in (
        'ship: a brig "X" of France at the Iroise, running home to Brest',
        "port brest: closed to the United States",
        'weather: low "the low" radius 450 km at 1805-06-12T10:00 -300 500 990',
        'message: at Brest from the Prefect: "dine"',
        'person: agent "Mr Fox" ashore at Brest',
        "world order: a gale tonight",
    ):
        e = w.submit(text)
        assert e.kind == "order.rejected" and vocab.world_order_refusal in e.text, text
        assert WO.recognises(text)
    assert not WO.recognises("set the topsails") and not WO.recognises("the port")
    assert w.journal == [] and all("world_order" not in i for i in w.inputs)
    # an order of the ship's that happens to begin with a channel's word is not refused
    e = w.submit("the port")
    assert e.kind == "query.reading"


def test_a_world_order_is_journaled_at_its_tick_with_its_source_and_replayed_at_its_tick():
    """Truth 72's mechanism for the harness's orders: in `inputs` at the tick with the
    source, applied again by a replay at the same tick, the digests one; a save holds
    the record for the reader."""
    w = world_for(systems=[HIGH])
    w.run(600)
    w.world_order(
        'ship: a cutter "Lark" of Britain at 49 40 N 5 20 W, bound for Falmouth', "the lead"
    )
    w.run(1800)
    w.world_order("port falmouth: price of tin 130", "the lead")
    w.run(1800)
    saved = w.save()
    entries = [i for i in saved["inputs"] if "world_order" in i]
    assert [(i["tick"], i["source"]) for i in entries] == [(600, "the lead"), (2400, "the lead")]
    assert [(o["tick"], o["source"], o["result"]) for o in saved["world_orders"]] == [
        (600, "the lead", "done"),
        (2400, "the lead", "done"),
    ]
    lines = events(w, "world.order")
    assert [e.tick for e in lines] == [600, 2400] and all(e.actor == "driver" for e in lines)
    copy = replay.replay(saved, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert [v.to_dict() for v in copy.vessels.vessels] == [v.to_dict() for v in w.vessels.vessels]
    assert copy.ports.ports["falmouth"].market.goods["tin"].price == 130.0


def test_the_scenarios_orders_by_time_are_applied_at_their_ticks_as_the_scenario_and_replayed():
    """Truth 71's first half and truth 72's: a world order given by the scenario at a
    time is journaled at that tick with the source "the scenario", is not an input (a
    replay from the saved scenario applies it again), and the replay's digest is the
    same."""
    sc_orders = [
        {"at": "1805-06-12T10:10", "order": "port falmouth: price of tin 140"},
        {
            "at": "1805-06-12T10:30",
            "order": 'ship: a merchant brig "Nancy" of Britain at 49 40 N 5 10 W, '
            "bound for the Eddystone",
        },
    ]
    w = world_for(systems=[HIGH], world_orders=sc_orders)
    w.run(1500)
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 140.0
    assert w.vessels.find("Nancy") is None
    w.run(300)
    assert w.vessels.find("Nancy") is not None
    lines = events(w, "world.order")
    assert [(e.tick, e.data["source"]) for e in lines] == [
        (600, "the scenario"),
        (1800, "the scenario"),
    ]
    w.run(1200)
    saved = w.save()
    assert not [i for i in saved["inputs"] if "world_order" in i]
    assert [o["tick"] for o in saved["world_orders"]] == [600, 1800]
    copy = replay.replay(saved, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.vessels.find("Nancy").position == w.vessels.find("Nancy").position


def test_a_message_by_the_cutter_reaches_the_captain_through_the_lookout_the_hail_and_the_door():
    """The principle's carrier rule (`InwardAndOutward.md`; truth 68): a world order
    sends the cutter with the letter; the lookout sights her, she comes within hail, the
    letter comes aboard by her, the messenger carries it to the captain where he is, and
    each is a line in order; nothing from nowhere."""
    w = world_for()
    w.submit("go below")
    before = len(w.log)
    e = w.world_order(
        'ship: a cutter "Nimble" of Britain at 49 38 N 5 10 W, carrying a letter from the port '
        'admiral to the ship: "Proceed with all dispatch to the station off Ushant."',
        "the scenario",
    )
    assert e.data["result"] == "done"
    for _ in range(240):
        w.run(60)
        if events(w, "message.received"):
            break
    kinds = [x.kind for x in list(w.log)[before:]]
    chain = [
        "lookout.sighting",
        "sail.within_hail",
        "message.aboard",
        "message.door",
        "message.received",
    ]
    found = [k for k in kinds if k in chain]
    for a, b in zip(chain, chain[1:], strict=False):
        assert found.index(a) < found.index(b), found
    aboard = events(w, "message.aboard")[0]
    assert aboard.data["carried_by"] == "the cutter Nimble" and "the port admiral" in aboard.text
    door = events(w, "message.door")[0]
    assert "knocked at the cabin door with a letter from the port admiral" in door.text
    received = events(w, "message.received")[0]
    assert (
        received.text == "The captain read it: Proceed with all dispatch to the station off Ushant."
    )
    hail = events(w, "sail.within_hail")[0]
    assert hail.text.startswith("A cutter is within hail") and hail.data["letter"]
    # the same by the port's cutter from the quay, and the letter left at a port comes
    # by the pilot (35's chain), never by a line of its own
    e = w.world_order(
        'message: by a cutter from Falmouth from the collector: "The packet is in."', "the test"
    )
    assert e.data["result"] == "done" and w.vessels.find("the Falmouth cutter") is not None
    assert len(events(w, "message.received")) == 1


def test_an_appended_system_lives_among_the_climatologys_and_a_scenario_file_is_checked(tmp_path):
    """A scripted system appended to a seeded (climatology) world follows its track and
    is not killed by the seeded systems' life curve; a scenario file's `world_orders` and
    `ships` are refused in words at the load when they cannot be read."""
    from freesail.world.scenarios import ScenarioError, load_scenario

    w = world_for(climatology=True)
    e = w.world_order(
        'weather: low "the low" radius 450 km at 1805-06-12T10:00 -300 500 990', "the test"
    )
    assert e.data["result"] == "done"
    w.run(3600)
    low = w.systems.find("the low")
    assert low is not None and low.scripted and not low.gone
    # the scenario file's checks
    base = (
        "name: x\nseed: 7\nstart: 1805-06-12T05:00\nposition: {lat_deg: 49.6, lon_deg: -5.4}\n"
        "region: channel-west\nship: {file: data/ships/topsail-schooner.yaml}\n"
    )
    bad_order = tmp_path / "a.yaml"
    bad_order.write_text(base + "world_orders:\n  - {at: 1805-06-12T06:00, order: 'make a gale'}\n")
    with pytest.raises(ScenarioError, match="world_orders 1"):
        load_scenario(bad_order)
    bad_ship = tmp_path / "b.yaml"
    bad_ship.write_text(
        base + "ships:\n  - {description: galleon, position: 49 N 5 W, goal: bound for Brest}\n"
    )
    with pytest.raises(ScenarioError, match="no description"):
        load_scenario(bad_ship)
    good = tmp_path / "c.yaml"
    good.write_text(
        base + "ships:\n  - {id: a, description: merchant brig, name: A, nation: britain, "
        "position: 49 50 N 5 30 W, goal: bound for Falmouth}\n"
        + "world_orders:\n  - {at: 1805-06-12T06:00, order: 'port falmouth: price of tin 130'}\n"
        + "papers: {chart: {year: 1804}, epitome: moore, almanac: 1805, price_lists: [falmouth]}\n"
    )
    sf = load_scenario(good)
    assert sf.scenario.ships[0]["id"] == "a"
    assert sf.scenario.world_orders[0]["at"].startswith("1805-06-12T06:00")
    assert sf.scenario.epitome == "moore" and sf.scenario.papers["chart"] == {"year": 1804}
    assert any("Other sail on the sea" in ln for ln in sf.lines())
    assert any("World orders by time" in ln for ln in sf.lines())


def test_a_point_of_interest_by_world_order_is_seen_as_a_mark_with_its_description():
    """Package 45c, item 13 (the owner's note 23 of gate m6a-2): `mark: <description> at
    <place>` puts a point of interest in the world, the scenario's at its time or the
    harness's; the lookout sees it as a mark when it is in sight (a mark beyond the horizon
    is not seen), the log's line its description, where it lies from her head, its bearing
    and its distance; the order itself is the record's, refused at the captain's prompt;
    saved and replayed, the digests one."""
    wreck = "a wreck, her masts showing above the water"
    sc_orders = [{"at": "1805-06-12T10:01", "order": f"mark: {wreck} at 49 36 N 5 20 W"}]
    w = world_for(world_orders=sc_orders)
    w.world_order("mark: a cask adrift at 49 36 N 4 40 W", "the test")  # 26 miles east
    w.run(300)
    seen = [
        e for e in events(w, "lookout.sighting") if e.data.get("id", "").startswith("interest-")
    ]
    assert [e.data["description"] for e in seen] == [wreck]
    line = seen[0].text
    assert line.startswith(
        "A wreck, her masts showing above the water abeam to larboard, bearing E, distant "
    )
    assert [o["result"] for o in w.save()["world_orders"]] == ["done", "done"]
    refused = w.submit(f"mark: {wreck} at 49 36 N 5 20 W")
    assert refused.kind == "order.rejected"
    assert w.world_order("mark: a wreck at nowhere at all", "the test").data["result"] == "refused"
    saved = w.save()
    copy = replay.replay(saved, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert [f.name for f in copy.marks_of_interest] == ["a cask adrift", wreck]


# ---------------------------------------------------------------------------
# Package 52 (spec M7b §8, §9): people made from words and moved, `say as`, the rule of
# reach, and the movements' doubt
# ---------------------------------------------------------------------------

OFF_FALMOUTH = {"lat_deg": 50.10, "lon_deg": -5.00}  # some two miles off Falmouth's roads


def _fake_officer(w):
    from freesail.agents import Fake, Harness, SamplingPolicy
    from freesail.agents.agent import officer

    h = Harness(
        w,
        officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=w),
        Fake(["Noted."], loop=True),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake officer", "mcp"
    h.start()
    return h


def test_a_person_made_from_words_comes_aboard_is_bound_and_goes_ashore():
    """`person: "Mr Fox" comes aboard as master`: aboard from his port, the master's station
    bound to him (its own line), his journal the station's; `leaves the ship at <port>` and
    `goes ashore`: ashore at the port, his station unbound; each a line of the play log,
    the order the record's. The master who keeps the reckoning and the captain cannot be
    put ashore; a person never made is refused, with how to make him."""
    from freesail.agents.agent import master
    from freesail.agents.journal import journal_of, person_journal

    w = world_for(position=OFF_FALMOUTH, ports=["falmouth", "brest"])
    for text in (
        'person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth',
        'person: "Mr Fox" comes aboard as master',
    ):
        assert w.world_order(text, "the test").data["result"] == "done"
    fox = w.people.find("Mr Fox")
    assert fox.aboard and fox.where == "quarterdeck" and w.stations.holder("master") is fox
    assert events(w, "person.aboard")[-1].text == "Mr Fox came aboard from Falmouth."
    assert events(w, "station.bound")[-1].text == "The master's station is bound (Mr Fox)."
    assert journal_of(w, "master") is person_journal(w, fox)
    assert master(world=w).person == "Mr Fox"  # a model seated there is in his place
    e = w.world_order('person: "Mr Fox" leaves the ship at Falmouth', "the test")
    assert e.data["result"] == "done" and not fox.aboard and fox.port == "falmouth"
    assert events(w, "person.ashore")[-1].text == "Mr Fox left the ship at Falmouth."
    assert w.stations.holder("master").name == "Mr Harvey"  # the file's again
    assert events(w, "station.bound")[-1].text == "The master's station is bound (Mr Harvey)."
    e = w.world_order('person: "Mr Pascoe" goes ashore', "the test")
    assert e.data["result"] == "done" and not w.stations.aboard("second officer")
    for text, words in (
        ('person: "Mr Harvey" goes ashore', "keeps the reckoning"),
        ('person: "Captain Bowen" goes ashore', "held by the player at the prompt"),
        ('person: "Mr Nobody" comes aboard', "make him first"),
        ('person: "Mr Fox" goes ashore', "ashore already"),
        ('person: "Mr Pearce" comes aboard', "aboard already"),
    ):
        e = w.world_order(text, "the test")
        assert e.data["result"] == "refused" and words in e.text, e.text


def test_the_movements_are_doubted_beyond_a_boats_reach_and_a_person_made_or_a_word_never():
    w = world_for(ports=["falmouth", "brest"])  # 35 miles off Falmouth
    w.world_order('person: make "Mr Fox", a pilot, ashore at Brest', "the test")
    doubt = WO.doubt(w, WO.parse('person: "Mr Fox" comes aboard as master'))
    assert "no boat brings a man off so far" in doubt and "Brest" in doubt
    assert "no boat puts a man ashore" in WO.doubt(w, WO.parse('person: "Mr Pearce" goes ashore'))
    left = WO.doubt(w, WO.parse('person: "Mr Pearce" leaves the ship at Falmouth'))
    assert "35 miles from Falmouth" in left
    for text in (
        'person: make "Mr Gill", a merchant, aboard in the cabin',
        'say as the carpenter: "She is making a little water, sir."',
    ):
        assert WO.doubt(w, WO.parse(text)) is None
    near = world_for(position=OFF_FALMOUTH, ports=["falmouth", "brest"])
    near.world_order('person: make "Mr Fox", a pilot, ashore at Falmouth', "the test")
    assert WO.doubt(near, WO.parse('person: "Mr Fox" comes aboard')) is None
    assert WO.doubt(near, WO.parse('person: "Mr Pearce" goes ashore')) is None


def test_say_as_puts_words_in_a_mouth_heard_within_earshot_and_journaled_as_his():
    """`say as <person>: <words>`: his words a notable line of the play log where he is
    (never the order), heard by the stations within earshot (the officer on the
    quarterdeck hears the cook in the galley, open to the waist; nobody hears the purser
    in the gunroom), and in his journal as his. A man of the muster by his trade is drawn
    when he is spoken for; a person ashore is heard only within a boat's reach of his
    port; a stranger never made is nobody."""
    from freesail.agents.journal import SAID_KIND, person_journal
    from freesail.core.events import for_the_record

    w = world_for(position=OFF_FALMOUTH, ports=["falmouth", "brest"])
    officer_h = _fake_officer(w)
    w.run(1)
    for text in (
        'say as the cook: "Pease and pork, sir."',
        "say as the purser: The slops are short of shoes.",
    ):
        assert w.world_order(text, "the test").data["result"] == "done"
    cook = w.people.find("the cook")
    spoke = events(w, "person.spoke")
    assert spoke[0].text == f"{cook.name}, the cook, in the galley: Pease and pork, sir."
    assert spoke[0].severity.value == "notable" and not for_the_record(spoke[0])
    assert spoke[0].data["heard_by"] == ["officer of the watch"]
    assert spoke[1].data["heard_by"] == [] and spoke[1].data["where"] == "in the gunroom"
    assert officer_h.agent.heard[-1] == spoke[0].text
    entries = person_journal(w, cook).entries
    assert entries[-1].kind == SAID_KIND and "Pease and pork, sir." in entries[-1].text
    w.world_order('person: make "Mr Fox", an agent, ashore at Falmouth', "the test")
    w.world_order('person: make "Mr Roy", an agent, ashore at Brest', "the test")
    assert w.world_order('say as Mr Fox: "The packet is in."', "t").data["result"] == "done"
    said = events(w, "person.spoke")[-1].text
    assert said == "Mr Fox, the agent, ashore at Falmouth: The packet is in."
    far = w.world_order('say as Mr Roy: "Bonjour."', "t")
    assert far.data["result"] == "refused" and "nobody aboard can hear Mr Roy" in far.text
    none = w.world_order('say as the harbourmaster: "Welcome."', "t")
    assert none.data["result"] == "refused" and "make" in none.text
    assert w.submit('say as the cook: "Aye."').kind == "order.rejected"  # the captain's prompt
    assert WO.recognises('say as the cook: "Aye."') and not WO.recognises("say all is well")


def test_the_rule_of_reach_refuses_a_held_station_and_names_the_stations_held():
    """Nobody speaks as, moves or binds a station to a person a model or the player holds,
    whoever gives the order: the captain (the player at the prompt), the officer (a model);
    the refusal names the stations held. Unheld, the same person is spoken for."""
    from freesail.agents.seat import seat_player

    w = world_for(position=OFF_FALMOUTH, ports=["falmouth"])
    assert WO.held_words(w) == "the captain (Captain Bowen, the player at the prompt)"
    w.world_order('say as Mr Pearce: "All well forward, sir."', "the test")
    assert events(w, "person.spoke")[-1].text.startswith("Mr Pearce, the first lieutenant")
    _fake_officer(w)
    w.run(1)
    assert WO.held_words(w) == (
        "the officer of the watch (Mr Pearce, a model); the captain (Captain Bowen, the "
        "player at the prompt)"
    )
    w.world_order('person: make "Mr Fox", a pilot, aboard', "the test")
    for text, words in (
        ('say as Mr Pearce: "Aye."', "Mr Pearce is the officer of the watch's, held by a model"),
        ('say as the captain: "Make it so."', "held by the player at the prompt"),
        ('person: "Mr Pearce" goes ashore', "nobody moves or binds a person"),
        ('person: "Mr Fox" comes aboard as officer of the watch', "nobody binds another"),
    ):
        e = w.world_order(text, "the test")
        assert e.data["result"] == "refused" and words in e.text, e.text
        assert "the stations held now: the officer of the watch (Mr Pearce, a model)" in e.text
    # the player seated at the master's: the captain is nobody's at the prompt, the master his
    seat_player(w, "master")
    held = WO.held_words(w)
    assert "the master (Mr Harvey, the player at his seat)" in held and "captain" not in held


# ---------------------------------------------------------------------------
# The director's hand (spec M7b §3; package 62)
# ---------------------------------------------------------------------------


def test_the_hand_gives_a_far_ship_her_captains_order_and_he_takes_up_his_plan_after_a_glass():
    """`ship "X": order <words>`: at far detail through the far shape's orders, her log (the
    far body's story) saying it as her captain's, never a line of the player's log; he holds
    by it a glass, then his plan again; `carry on` sooner; what the far shape cannot carry
    answered in words naming what it can; a world order is no order of hers; the player's
    own ship is never the hand's."""
    from tests.test_brains import put

    w = world_for(ports=["falmouth", "plymouth"])
    v = put(
        w, "merchant brig", "britain", "49 40 N 4 55 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(60)
    assert v.detail == "far" and v.plan and v.plan[0][0] == "to"
    before = list(v.plan)
    e = w.world_order('ship "X": order heave to', "the test")
    assert e.data["result"] == "done" and e.data["hand"] == "heave to", e.text
    assert "her captain holds by it until 10:31" in e.text
    assert v.plan == [("lie_to", float("inf"))] and v.story[-1][1] == "By the captain: heaving to."
    assert v.brain.over_head["until"] == w.clock.tick + 1800
    assert not [x for x in w.log if "By the captain" in x.text and not for_the_record(x)]
    assert v.to_dict()["story"] == [[w.clock.tick, "By the captain: heaving to."]]
    # his judgement held: a glass lying to, then his plan again, said in her story
    w.run(1200)
    assert v.plan[0][0] == "lie_to" and v.sail_state == "lying to"
    w.run(660)
    assert v.brain.over_head is None and v.plan[0][0] == "to" and v.plan[0][1:] == before[0][1:]
    assert v.story[-1][1] == "The captain takes up his plan again (bound for Falmouth)."
    # 'carry on' gives her back before the glass is out
    w.world_order('ship "X": order heave to', "the test")
    e = w.world_order('ship "X": order carry on', "the test")
    assert e.data["result"] == "done" and "carries on" in e.text
    assert v.plan[0][0] == "to" and v.brain.over_head is None
    e = w.world_order('ship "X": order carry on', "the test")
    assert e.data["result"] == "refused" and "under no order of yours" in e.text
    # what the far shape cannot carry, and a world order, in words
    e = w.world_order('ship "X": order set the fore royal', "the test")
    assert e.data["result"] == "refused" and "the orders the far shape carries are" in e.text
    assert "crewed first" not in e.text  # she is far beyond the range of the ship
    e = w.world_order('ship "X": order port falmouth: price of tin 130', "the test")
    assert e.data["result"] == "refused" and "an order to the world, not to her" in e.text
    e = w.world_order('ship "X": crewed', "the test")
    assert e.data["result"] == "refused" and "beyond the promotion's range" in e.text
    e = w.world_order('ship "Amazon": order heave to', "the test")
    assert e.data["result"] == "refused" and "the player's own ship" in e.text
    assert "held by the player at the prompt" in e.text
    # a World kept in the far shape (a station on her): through `submit_far`, her log
    from freesail.world import crews as K

    _v, crew = K.station_world(w, "X")
    assert crew.shape == "far"
    e = w.world_order('ship "X": order heave to', "the test")
    assert e.data["result"] == "done" and v.plan[0][0] == "lie_to", e.text
    said = [x for x in crew.log if x.text == "By the captain: heaving to."]
    assert said and str(said[0].actor).startswith("captain's rule")


def test_the_hand_is_doubted_only_where_her_captains_order_is_implausible_for_her():
    """A captain's order is a plausible cause: never doubted but an anchor let go too deep
    for her cables, plain sail in a gale, a chase by a merchantman; the scenario's and the
    owner's never at all (the doubt is the director's door's)."""
    from tests.test_brains import put

    w = world_for(ports=["falmouth"])
    put(w, "merchant brig", "britain", "49 40 N 4 55 W", "bound for Falmouth", "bound for Falmouth")
    put(
        w,
        "brig-sloop",
        "britain",
        "49 30 N 5 50 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    w.run(60)

    def doubt(text):
        return WO.doubt(w, WO.parse(text))

    assert doubt('ship "X": order heave to') is None
    assert doubt('ship "X": order shape a course for Plymouth') is None
    deep = doubt('ship "X": order come to an anchor')
    assert deep and "fathoms by the chart" in deep and "no master lets go beyond 30" in deep
    chase = doubt('ship "X": order give chase')
    assert chase and "the merchant's doctrine" in chase
    assert doubt('ship "Hazard": order give chase') is None  # a cruiser chases
    assert doubt('ship "X": order make sail') is None  # fourteen knots: no gale
    assert WO.reach(w, WO.parse('ship "X": order heave to')) is None


def test_the_hand_on_a_crewed_ship_is_her_captains_order_held_a_glass_and_refused_when_held():
    """Within the range a far ship may be asked for crewed first (the cap and its order
    stand); crewed, the order is her World's as her captain's, under his rules' actor and his
    domain, her log saying it as his; his book struck and his judgement held a glass, then
    his intent again, filling away; refused in words, naming who holds him, where a fake
    captain holds her captain's station."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import captain
    from freesail.agents.fake import captain_of_the_ship
    from freesail.world import crews as K
    from tests.test_brains import put

    w = world_for(ports=["falmouth"])
    w.submit("heave to")
    v = put(
        w,
        "brig-sloop",
        "britain",
        "49 38 N 5 22 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    e = w.world_order('ship "Hazard": crewed', "the test")
    assert e.data["result"] == "done" and "Hazard at full detail" in e.text, e.text
    crew = v.crew
    assert crew is not None and crew.shape == "full" and K.crewed(w) == [v]
    e = w.world_order('ship "Hazard": crewed', "the test")
    assert e.data["result"] == "refused" and "at full detail already" in e.text
    w.run(600)
    assert crew.captain.commands
    e = w.world_order('ship "Hazard": order heave to', "the test")
    assert e.data["result"] == "done" and "at full detail" in e.text, e.text
    said = [x for x in crew.log if x.text == "By the captain: heaving to."]
    assert said and str(said[-1].actor).startswith("captain's rule")
    assert not [x for x in w.log if "By the captain" in x.text and not for_the_record(x)]
    cap = crew.captain
    assert cap.over_head_until == crew.clock.tick + 1800 and not cap.commands
    assert cap.state is None and cap.to_dict()["over_head"] == "heave to"
    assert crew.standing.books_loaded() == []
    w.run(900)
    assert crew.readings.value("manoeuvre_in_hand") == "hove to"
    # her grammar is the domain: what she cannot do is refused in her words
    e = w.world_order('ship "Hazard": order sell the tin', "the test")
    assert e.data["result"] == "refused" and "Hazard's captain could not give it" in e.text
    # the glass out: his intent again, filling away
    w.run(1000)
    assert cap.over_head_until is None and cap.commands and cap.state is not None
    assert any("filling away" in x.text for x in crew.log if x.tick > said[-1].tick + 1700)
    # a fake captain at her captain's station: refused in words, naming who holds him
    h = Harness(
        crew,
        captain(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=crew),
        captain_of_the_ship([]),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake captain", "mcp"
    h.start()
    e = w.world_order('ship "Hazard": order heave to', "the test")
    assert e.data["result"] == "refused", e.text
    assert "Hazard's captain (" in e.text and "is held by a model" in e.text
    assert "write to him instead ('message: ...')" in e.text
    assert WO.reach(w, WO.parse('ship "Hazard": order heave to'))


def test_the_hold_crosses_the_promotion_both_ways():
    """A far ship hove to by the hand and promoted inside the glass heaves to at full detail
    by her captain's words, the first of her new log's, and he holds by it the rest of the
    glass; demoted while held, the far body lies to and her far captain keeps the hold."""
    from freesail import units
    from freesail.world import crews as K
    from tests.test_brains import put

    w = world_for(ports=["falmouth"])
    w.submit("heave to")
    v = put(
        w,
        "brig-sloop",
        "britain",
        "49 38 N 5 10 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    w.run(60)
    assert v.crew is None
    w.world_order('ship "Hazard": order heave to', "the test")
    until = v.brain.over_head["until"]
    v.position = w.position.advanced(0.0, 3.0 * units.NAUTICAL_MILE)
    w.run(61)
    crew = v.crew
    assert crew is not None and crew.shape == "full" and v.brain.over_head is None
    left = until - w.clock.tick
    assert crew.captain.over_head_until == crew.clock.tick + left and crew.captain.state is None
    assert [e.text for e in crew.log if e.text.startswith("By the captain")] == [
        "By the captain: heaving to."
    ]
    w.run(600)
    assert crew.readings.value("manoeuvre_in_hand") == "hove to" and not crew.captain.commands
    w.run(until - w.clock.tick + 60)
    assert crew.captain.over_head_until is None and crew.captain.commands
    w.world_order('ship "Hazard": order heave to', "the test")
    w.run(300)
    K.demote(w, v)
    assert v.crew is None and v.plan[0][0] == "lie_to"
    assert v.brain.over_head is not None and v.brain.over_head["order"] == "heave to"


# ---------------------------------------------------------------------------
# Package 53b: things made and moved by the aboard channel (spec M7b §17a)
# ---------------------------------------------------------------------------


def test_the_aboard_channel_makes_and_moves_a_thing_never_doubted_made_and_keeps_the_reach():
    """`aboard: <a thing>, <where>` makes a thing (a thing made wants no cause of the
    sea's, and is never doubted), and `aboard: the <thing>, <where>` moves one known; no
    thing is put into or taken out of the keeping of a person the player or a model holds
    (the player at the prompt holds the captain), the refusal saying to leave it where he
    can take it; the table's things and the old refusal's forms stand."""
    from freesail.world import things as TH

    w = world_for()
    for text in (
        "aboard: a sealed packet, on the cabin table, from the Custom House",
        "aboard: a cask of brandy, in the hold",
    ):
        o = WO.parse(text)
        assert WO.doubt(w, o) is None and WO.reach(w, o) is None
        assert w.world_order(text, "the test").data["result"] == "done"
    packet, cask = TH.things_of(w)
    assert (cask.name, cask.place) == ("a cask of brandy", "hold")
    master = w.people.find("the master")
    e = w.world_order("aboard: the packet, in the keeping of the master", "the test")
    assert e.data["result"] == "done" and packet.keeper == master.id
    assert e.text.endswith(f"it was on the table in the cabin, and is in {master.name}'s keeping.")
    e = w.world_order("aboard: the cask, in the captain's keeping", "the test")
    assert e.data["result"] == "refused" and "leave it where he can take it" in e.text
    assert "the stations held now: the captain" in e.text and not cask.keeper
    TH.put(packet, {"keeper": w.people.captain.id})
    e = w.world_order("aboard: the packet, in the hold", "the test")
    assert e.data["result"] == "refused" and "nothing is taken out of a held person's" in e.text
    # the scenario and the table's things as they were
    assert (
        w.world_order("aboard: a cask found stove [reason: x]", "the test").data["result"] == "done"
    )
    e = w.world_order("aboard: the cook reports the beef cask found rotten", "the test")
    assert e.data["result"] == "refused" and "a thing made or moved" in e.text


def test_a_thing_moved_by_no_hand_that_could_carry_it_is_doubted_and_a_replay_keeps_it():
    """A thing moved between the ship and a port beyond a boat's reach, or from one port to
    another, is doubted; a thing made is not. Made and moved by orders, the things are
    the same after a replay and a checkpoint, as the people are."""
    from freesail.core.events import for_the_record
    from freesail.world import things as TH

    w = world_for(ports=["falmouth", "brest"])
    w.world_order('person: make "Mr Veale", a clerk, ashore at Falmouth', "the test")
    w.world_order("aboard: a sealed packet, on the cabin table", "the test")
    o = WO.parse("aboard: the packet, in the keeping of Mr Veale")
    assert "no boat carries it so far" in WO.doubt(w, o)
    o = WO.parse("aboard: a sealed letter, ashore at Brest")
    assert WO.doubt(w, o) is None  # made, never doubted
    w.world_order("aboard: the packet, ashore at Falmouth", "the test")
    o = WO.parse("aboard: the packet, ashore at Brest, at the market")
    assert "from one port to another" in WO.doubt(w, o)
    w.world_order("aboard: a cask of brandy, in the hold", "the test")
    w.run(120)
    back = replay.replay_world(w, ship_factory)
    assert [t.to_dict() for t in TH.things_of(back)] == [t.to_dict() for t in TH.things_of(w)]
    assert back.log.digest() == w.log.digest()
    assert not [e for e in w.log.all() if "brandy" in e.text and not for_the_record(e)]


# Package 66: the hand's hold named, `say as` by station or trade, who heard
# ---------------------------------------------------------------------------


def test_the_hands_hold_is_named_for_a_time_or_until_her_own_event():
    """`... for a watch`, `... for two glasses`, `... until a sail within hail`: the hold so
    named in place of the glass, the default still a glass; an event she is held until ends
    it when it comes to her (a day at most), and an event she cannot be held until is
    refused in words naming those she can."""
    from freesail import units
    from freesail.world import crews as K
    from tests.test_brains import put

    assert K.hold_of("heave to for a watch") == ("heave to", 4 * 3600, "")
    assert K.hold_of("give chase for two glasses") == ("give chase", 3600, "")
    assert K.hold_of("heave to for an hour") == ("heave to", 3600, "")
    assert K.hold_of("shape a course for Falmouth") == ("shape a course for Falmouth", None, "")
    assert K.hold_of("give chase until a sail within hail") == ("give chase", None, "hail")
    assert K.hold_of("heave to until a landfall")[2] == "land"
    w = world_for(ports=["falmouth"])
    w.submit("heave to")
    v = put(
        w,
        "brig-sloop",
        "britain",
        "49 30 N 5 50 W",
        "bound for Falmouth",
        "keep the station off the Lizard within 10 miles",
        name="Hazard",
    )
    w.run(60)
    e = w.world_order('ship "Hazard": order heave to for two glasses', "the test")
    assert e.data["result"] == "done" and "holds by it until 11:01" in e.text, e.text
    assert v.brain.over_head["until"] == w.clock.tick + 3600
    e = w.world_order('ship "Hazard": order heave to until a mermaid', "the test")
    assert e.data["result"] == "refused" and "a sail within hail" in e.text
    e = w.world_order('ship "Hazard": order heave to until a sail within hail', "the test")
    assert e.data["result"] == "done", e.text
    assert "until a sail within hail comes to her (a day at most, 10:01 tomorrow)" in e.text
    assert v.brain.over_head["event"] == "hail"
    w.run(2 * 1800)  # past the glass, and past two
    assert v.brain.over_head is not None and v.plan[0][0] == "lie_to"
    nancy = put(w, "merchant brig", "britain", "49 30 N 5 50 W", "bound for Falmouth", name="N")
    nancy.position = v.position.advanced(0.0, 0.25 * units.NAUTICAL_MILE)
    w.run(180)
    assert v.brain.over_head is None and v.plan[0][0] != "lie_to"
    assert v.story[-1][1].startswith("The captain takes up his plan again")


def test_say_as_the_lookout_the_hands_and_a_station_and_who_heard_in_the_result():
    """`say as the lookout`: the ship's own lookout at the masthead, his hail heard on deck;
    `say as the hands`: the hands on deck; `say as the officer of the watch`: the station's
    person; the result names who heard it. The rule of reach holds: a held lookout is
    refused as any held station."""
    from freesail.agents.seat import seat_player

    w = world_for(position=OFF_FALMOUTH, ports=["falmouth"])
    officer_h = _fake_officer(w)
    w.run(1)
    e = w.world_order('say as the lookout: "Sail ho! Two points on the lee bow!"', "the test")
    assert e.data["result"] == "done", e.text
    hail = events(w, "person.spoke")[-1]
    assert hail.text == "The lookout, from the masthead: Sail ho! Two points on the lee bow!"
    assert hail.data["heard_by"] == ["officer of the watch"] and hail.data["place"] == "masthead"
    assert officer_h.agent.heard[-1] == hail.text
    assert "heard by Mr Pearce, the captain" in e.text
    e = w.world_order('say as the hands: "Huzzah!"', "the test")
    assert events(w, "person.spoke")[-1].text == "The hands, on the deck: Huzzah!"
    e = w.world_order('say as the second officer: "My watch, sir."', "the test")
    assert events(w, "person.spoke")[-1].text.startswith("Mr Pascoe, the second lieutenant")
    e = w.world_order('say as the purser: "The slops are short."', "the test")
    assert e.text.endswith("Mr Gardner spoke in the gunroom, heard by Mr Bailey, in the gunroom.")
    w.world_order('person: supercargo "Mr Pentreath" aboard in the hold', "the test")
    e = w.world_order('say as Mr Pentreath: "Dry as a bone."', "the test")
    assert e.text.endswith("heard by nobody: the captain is on the quarterdeck."), e.text
    seat_player(w, "lookout")
    e = w.world_order('say as the lookout: "Deck there!"', "the test")
    assert e.data["result"] == "refused" and "held by" in e.text
