"""People in places (spec M7b §14, §16 and §17; package 53): a person's place as an aspect
of his state tied to what he can do; the port's places ashore; books drafted, posted and
given to the boat; the equal reach, and several stations of the officer's kind with the
deck passing among them by the watch bill. Truths 7b-100 to 7b-102 are in
`tests/test_known_truths.py`."""

from __future__ import annotations

import io
from datetime import datetime

import pytest

from freesail.agents import Fake, Harness, SamplingPolicy, call, reply, tools
from freesail.agents.agent import officers_words
from freesail.agents.remote import make_station
from freesail.agents.seat import seat_player
from freesail.api import queries
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.world import movement
from freesail.world import places as P
from freesail.world.books import MANIFEST, NOTE, SHEET, books_of

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}
OFFICER = "officer of the watch"


def world_at(where=OFF_THE_LIZARD, ship=FRIGATE, start=datetime(1805, 6, 10, 10, 0), **kw):
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=250.0,
        position=where,
        chart="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def in_falmouth(**kw):
    w = world_at(CARRICK_ROAD, ship=SCHOONER, cargo={"purse_pounds": 2000.0}, **kw)
    w.run(60)
    w.submit("let go the best bower")
    w.run(300)
    assert w.at_anchor and w.ports.in_port().id == "falmouth"
    return w


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


def until(world, done, minutes=240):
    for _ in range(minutes):
        if done():
            return
        world.run(60)
    raise AssertionError("not done in time")


def seat(world, name, script=None, every=600):
    st = make_station(world, name, SamplingPolicy.in_lockstep(every, "notable", "urgent"))
    stand = reply("", call("stand_by", until="a glass"))
    h = Harness(world, st, Fake(script or [stand] * 60, when_done=stand), save=lambda w, r: None)
    h.model_name, h.door = f"the fake {name}", "runner"
    h.start()
    return h


# ---------------------------------------------------------------------------
# The port's places
# ---------------------------------------------------------------------------


def test_every_port_has_the_five_places_and_a_ports_file_adds_its_own():
    w = in_falmouth()
    falmouth = w.ports.ports["falmouth"]
    ids = list(P.port_places(falmouth))
    assert ids[:5] == ["quay", "market", "counting_house", "tavern", "pilots_office"]
    assert "packet_office" in ids
    assert P.find_port_place(falmouth, "the pilots' office").id == "pilots_office"
    assert P.find_port_place(falmouth, "Counting House").id == "counting_house"
    assert P.find_port_place(falmouth, "the ropewalk") is None
    assert P.ashore_place_of(falmouth, "Guernsey pilot") == "pilots_office"
    assert P.ashore_place_of(falmouth, "merchant") == "counting_house"
    assert P.ashore_place_of(falmouth, "") == "quay"
    assert "dockyard" in P.port_places(w.ports.ports["plymouth"])


def test_the_port_in_port_says_its_places_and_who_is_found_there():
    """`the port` at anchor in a port reads its places as words, each with what is done
    there and who is found there, the world's people ashore by name; at sea it is as it
    was."""
    w = in_falmouth()
    w.world_order('person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth', "t")
    fox = w.people.find("Mr Fox")
    assert w.people.state_words(fox) == "ashore at Falmouth, at the pilots' office"
    said = w.submit("the port").text
    assert "ashore: The quay: the boats land" in said
    assert "The pilots' office: a pilot is engaged" in said and "and Mr Fox." in said
    assert "The packet office:" in said
    at_sea = world_at().submit("the port").text
    assert "ashore:" not in at_sea
    # the words that make a person may put him at a place ashore
    e = w.world_order('person: make "Mr Gill", a merchant, ashore at Falmouth, in the tavern', "t")
    assert e.data["result"] == "done" and "ashore at Falmouth, in the tavern" in e.text
    gill = w.people.find("Mr Gill")
    assert gill.ashore_at == "tavern" and gill.outline.history == ""


# ---------------------------------------------------------------------------
# Movement and what a person can do where he is
# ---------------------------------------------------------------------------


def test_the_captain_goes_where_he_will_aboard_and_the_deck_is_given_from_the_deck():
    w = world_at()
    w.submit("set the jib")
    e = w.submit("go to the gunroom")
    assert e.kind == "person.moved" and e.text == "Captain Bowen went below to the gunroom."
    assert w.submit("set the main topsail").text.endswith(
        "You are in the gunroom; go on deck to make or take in sail."
    )
    assert w.submit("let go the best bower").text.endswith(
        "You are in the gunroom; go on deck to work the ground tackle."
    )
    # the reckoning, the book, the people, the readings are given from anywhere
    assert w.submit("send for the master").kind == "person.sent_for"
    assert w.submit('standing order "q": every glass then heave the lead').kind == "standing.given"
    assert w.submit("where is the captain").text.endswith("Captain Bowen, in the gunroom.")
    assert w.submit("go aloft").text == "Captain Bowen went aloft into the tops."
    assert w.submit("set the main topsail").kind == "order.rejected"
    assert w.submit("come on deck").kind == "captain.on_deck"
    assert w.submit("set the main topsail").kind != "order.rejected"
    for words, why in (
        ("go to the stables", "'stables' is no place aboard"),
        ("go to the boat", "is not a place to walk to"),
        ("go to the shore", "Say 'go ashore'"),
        ("go to", "Go where?"),
        ("come on deck", "already"),
        ("go ashore", "She is not in port"),
        ("come aboard", "You are aboard already"),
    ):
        assert why in w.submit(words).text, words


def test_a_place_ashore_named_aboard_says_go_ashore_first_and_go_alone_runs_the_clock():
    from freesail.ui.console import Console

    w = in_falmouth()
    assert "'go ashore' first" in w.submit("go to the market").text
    out = io.StringIO()
    con = Console(World(seed=3), out=out)
    con.handle_line("go")
    assert con.running
    con.running = False
    con.handle_line("go below")
    assert not con.running  # an order to the ship, not the clock


def test_an_officer_goes_below_at_his_station_and_the_cabin_is_the_captains():
    """The equal reach (spec M7b §17): a station's own move is his whatever his domain,
    with the deck or without; his duty keeps him out of the captain's cabin; the people and
    the muster say where he is."""
    w = world_at()
    seat(w, OFFICER)
    pearce = w.stations.holder(OFFICER)
    said = tools.call(w, OFFICER, "submit_order", {"text": "go below"})
    assert said == f"{pearce.name} went below to the gunroom."
    assert w.people.state_words(pearce) == "off watch, in the gunroom"
    assert f"{pearce.name}, off watch, in the gunroom" in queries.muster_lines(w)[-1]
    said = tools.call(w, OFFICER, "submit_order", {"text": "go to the cabin"})
    assert "The cabin is the captain's" in said
    said = tools.call(w, OFFICER, "submit_order", {"text": "come on deck"})
    assert said == f"{pearce.name} came on deck, to the quarterdeck."
    assert w.people.state_words(pearce) == "off watch"


def test_the_player_ashore_is_out_of_hail_of_the_ship_and_cannot_send_her_boat():
    w = in_falmouth()
    master = w.people.captain
    w.submit("go ashore")
    until(w, lambda: master.where == "shore" and not w.ports.boat.away)
    assert w.submit("send the boat ashore").text.endswith("'come aboard' sends the boat for you.")
    e = w.submit("tell the mate we sail on the morning tide")
    assert e.kind == "order.rejected" and "he is out of hail" in e.text
    assert w.submit("go to the tavern").text.startswith(f"{master.name} went to the tavern")
    assert "in the tavern already" in w.submit("go to the tavern").text
    assert w.people.state_words(master) == "ashore at Falmouth, in the tavern"
    assert "The tavern:" in w.submit("the port").text and master.name in w.submit("the port").text


def test_the_master_who_keeps_the_reckoning_does_not_leave_the_ship_but_the_commanding_one_may():
    w = world_at()
    harvey = w.people.find("the master")
    assert movement.person_of_actor(w, "captain") is w.people.captain
    seat_player(w, "master")
    e = w.submit("go ashore", actor="the master (the player)")
    assert e.kind == "order.rejected" and "does not leave the ship" in e.text
    assert harvey.aboard


# ---------------------------------------------------------------------------
# Books drafted
# ---------------------------------------------------------------------------


def test_a_book_is_a_sheet_a_manifest_or_a_note_by_its_lines_and_refused_whole_in_words():
    w = world_at()
    e = w.submit(
        'draft a book "night orders": standing order "lead": every glass then heave the lead; '
        '"dusk": at sunset then take in the royals; take in the topgallant sails'
    )
    assert e.kind == "book.drafted" and e.data["kind"] == SHEET
    assert e.data["lines"][1] == (
        'standing order "dusk": at sunset then take in the royals; take in the topgallant sails'
    )
    e = w.submit('draft a book "cargo": buy 20 tons of tin and 5 tons of salt; sell 3 tons of tin')
    assert e.data["kind"] == MANIFEST
    assert e.data["lines"] == ["buy 20 tons of tin", "buy 5 tons of salt", "sell 3 tons of tin"]
    e = w.submit('draft a book "the passage": We made the Lizard at noon; all well.')
    assert e.data["kind"] == NOTE and e.data["lines"] == ["We made the Lizard at noon", "all well."]
    for words, why in (
        ('draft a book "bad": standing order "x": then', "is not a standing order the ship reads"),
        ('draft a book "worse": buy tin', "How many tons?"),
        ('draft a book "cargo": a second', "already"),
        ('draft a book "empty":', "wants some lines"),
        ("draft a book", "Draft what?"),
        ('post the book "the passage"', "only a sheet is posted"),
        ('post the book "logbook"', "There is no book 'logbook'"),
        ('give the book "night orders" to the boat', "only a manifest is given"),
    ):
        got = w.submit(words)
        assert got.kind == "order.rejected" and why in got.text, (words, got.text)
    listed = w.submit("the books").text
    assert listed.startswith("The books drafted (3):") and "drafted by Captain Bowen" in listed
    page = w.submit('show the book "the passage"').text
    assert page.splitlines()[1] == "  We made the Lizard at noon"
    # the library serves them from anywhere, and lists them once there are any
    assert "books: the books drafted aboard, 3" in tools.library(w, OFFICER)
    got = tools.library(w, OFFICER, "books", "cargo")
    assert "buy 20 tons of tin" in got and "drafted by Captain Bowen" in got
    assert "books:" not in tools.library(world_at(), OFFICER)


def test_a_sheet_posted_by_an_officer_is_in_his_rank_and_one_naming_another_is_refused():
    w = world_at()
    seat(w, OFFICER)
    w.submit("you have the deck")
    pearce = w.stations.holder(OFFICER)
    said = tools.call(
        w,
        OFFICER,
        "submit_order",
        {"text": 'draft a book "my orders": "reefs": every glass then heave the lead'},
    )
    assert said.startswith(f"{pearce.name} drafted a book, 'my orders'")
    assert books_of(w).find("my orders").mark == pearce.name
    said = tools.call(w, OFFICER, "submit_order", {"text": 'post the book "my orders"'})
    assert "posted the sheet 'my orders'" in said, said
    rule = w.standing.book.get("reefs")
    assert rule is not None and rule.given_by == "first lieutenant"
    tools.call(
        w,
        OFFICER,
        "submit_order",
        {
            "text": 'draft a book "his": standing order "cap" by the captain: at sunset '
            "then heave the lead"
        },
    )
    said = tools.call(w, OFFICER, "submit_order", {"text": 'post the book "his"'})
    assert said.startswith("The officer of the watch may not post the sheet 'his'")
    assert w.standing.book.get("cap") is None
    # a manifest given to the boat is the port's business, kept back from him
    tools.call(w, OFFICER, "submit_order", {"text": 'draft a book "goods": buy 5 tons of tin'})
    said = tools.call(w, OFFICER, "submit_order", {"text": 'give the book "goods" to the boat'})
    assert said.startswith("The officer of the watch may not give the manifest 'goods'")


def test_a_manifest_that_cannot_be_struck_whole_is_refused_and_nothing_paid():
    w = in_falmouth(papers={"price_lists": ["falmouth"]})
    purse = w.purse.pounds
    w.submit('draft a book "dear": buy 10 tons of tin; buy 2000 tons of salt')
    e = w.submit('give the book "dear" to the boat')
    assert e.kind == "order.rejected" and "will not stow" in e.text
    w.submit('draft a book "short": sell 5 tons of tin')
    e = w.submit('give the book "short" to the boat')
    assert e.kind == "order.rejected" and "The hold has 0 tons of tin" in e.text
    assert w.purse.pounds == purse and not w.ports.boat.away


# ---------------------------------------------------------------------------
# Several stations of one kind, and the deck by the watch bill
# ---------------------------------------------------------------------------


def test_the_frigates_officers_are_named_by_number_or_person_and_each_brief_says_who_is_first():
    w = world_at()
    stations = w.stations
    assert stations.kind_of("third officer") == OFFICER
    assert stations.resolve("officer 2") == "second officer"
    assert stations.resolve("officer 3") == "third officer"
    assert stations.resolve("Mr Russell") == "third officer"
    assert stations.resolve("the second lieutenant") == "second officer"
    assert stations.resolve("officer 1") == OFFICER
    st = make_station(w, "officer 2", None)
    assert st.name == "second officer" and st.person == "Mr Pascoe" and st.rank == "lieutenant"
    assert "in the place of Mr Pascoe" in st.brief
    words = officers_words(w, "second officer")
    assert words.startswith("The officers of the watch: the officer of the watch (Mr Pearce")
    assert "the second officer (Mr Pascoe, second lieutenant, the starboard watch)" in words
    assert "the third officer (Mr Russell, third lieutenant, the larboard watch)" in words
    assert "You are the second officer." in st.brief
    seat = seat_player(w, "Mr Russell")
    assert seat.station.name == "third officer" and seat.station.person == "Mr Russell"
    # a ship with one officer's station: no such words
    brig = world_at(ship="data/ships/brig.yaml")
    assert officers_words(brig, OFFICER) == ""


def test_the_deck_passes_among_the_officers_at_the_change_of_the_watch_by_the_bill():
    """The captain gives the deck to the second lieutenant (the starboard watch) in the
    forenoon; at noon the larboard watch comes on deck and the deck passes to the third
    lieutenant at his station, and back at the first dog watch; the first lieutenant keeps
    no watch and is never given it by the bill."""
    w = world_at(start=datetime(1805, 6, 12, 11, 10))
    officers = {name: seat(w, name) for name in (OFFICER, "second officer", "third officer")}
    e = w.submit("Mr Pascoe, you have the deck")
    assert e.kind == "agent.deck" and e.data["station"] == "second officer"
    assert officers["second officer"].agent.deck
    w.run(3600)
    passed = events(w, "watch.deck_passed")
    assert [x.text for x in passed] == [
        "At the change of the watch the deck passed from the second officer (Mr Pascoe) to the "
        "third officer (Mr Russell), by the watch bill."
    ]
    assert officers["third officer"].agent.deck and not officers["second officer"].agent.deck
    assert w.stations.holder("third officer").where == "quarterdeck"
    w.run(4 * 3600)
    assert officers["second officer"].agent.deck and len(events(w, "watch.deck_passed")) == 2
    e = w.submit("I have the deck")
    assert e.kind == "agent.deck" and e.data["station"] == "second officer"
    assert not any(h.agent.deck for h in officers.values())
    # the first lieutenant keeps it through a change of the watch
    w.submit("you have the deck")
    w.run(2 * 3600)
    assert officers[OFFICER].agent.deck and len(events(w, "watch.deck_passed")) == 2


@pytest.mark.parametrize("words", ["officer 2", "Mr Pascoe"])
def test_a_seat_is_taken_by_the_officers_number_or_his_person(words):
    w = world_at()
    seat = seat_player(w, words)
    assert seat.station.name == "second officer"
    assert seat.station.person == "Mr Pascoe"
