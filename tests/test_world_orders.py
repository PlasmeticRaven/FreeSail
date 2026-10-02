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
        position=OPEN_WATER,
        region="channel-west",
        **kw,
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
