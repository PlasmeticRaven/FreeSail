"""The places aboard and the ship's papers (spec M5 §22; package 35): a place is a name
and a description; the hold, the purse and the stores are ledgers; a paper is a thing
with a keeper and a place, served by handle through the library to every station the
same, and only as current as its last entry."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.agents import tools
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.ship.parts import booms, cordage, ground_tackle, sail_room
from freesail.world import places as P

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}


def world_for(ship=FRIGATE, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=OFF_THE_LIZARD,
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def test_the_places_are_a_name_and_a_description_and_no_more():
    """The inward minimum (InwardAndOutward.md): the quarterdeck, the deck, the cabin, the
    gunroom, the tops, the sail room, the hold, the boat, the shore; a place has no layout
    and nothing moves in it."""
    ids = list(P.PLACES)
    for wanted in (
        "quarterdeck",
        "deck",
        "cabin",
        "gunroom",
        "tops",
        "sail_room",
        "hold",
        "boat",
        "shore",
    ):
        assert wanted in ids
    for p in P.PLACES.values():
        assert (
            p.name.startswith("the ")
            and p.description
            and set(vars(p))
            == {
                "id",
                "name",
                "description",
                "below",
                "aboard",
            }
        )
    assert P.PLACES["cabin"].below and not P.PLACES["quarterdeck"].below
    assert not P.PLACES["shore"].aboard and not P.PLACES["boat"].aboard
    assert P.place_words("quarterdeck") == "on the quarterdeck"
    assert P.place_words("cabin") == "in the cabin"
    assert P.place_words("shore") == "ashore"
    places = P.Places("Amazon")
    assert places.find("the sail room").id == "sail_room"
    assert places.find("below").id == "cabin" and places.find("the moon") is None
    assert places.describe()[0].startswith("The quarterdeck: the after part of the upper deck")
    # the reading at the prompt is the same words
    w = world_for()
    e = w.submit("the places")
    assert e.kind == "query.reading" and e.text.startswith("The places: the quarterdeck, the deck")
    assert w.readings["places"]["items"]["hold"]["description"].startswith(
        "the whole interior cavity"
    )
    assert "The hold: the whole interior cavity" in " ".join(w.readings["places"]["described"])


def test_the_hold_the_purse_and_the_stores_are_ledgers():
    hold = P.Hold(112.0)
    hold.stow("tin", 40.0)
    assert hold.stowed_tons == 40.0 and hold.room_tons == 72.0
    with pytest.raises(ValueError, match="room in the hold for 72 tons"):
        hold.stow("salt", 80.0)
    with pytest.raises(ValueError, match="has 40 tons of tin"):
        hold.break_out("tin", 41.0)
    hold.break_out("tin", 40.0)
    assert hold.goods == {} and hold.words() == "empty, room for 112 tons"
    assert hold.lines()[1] == "No cargo aboard."
    purse = P.Purse(100.0)
    purse.pay(12.5, "the pilot", 10)
    assert purse.pounds == 87.5 and purse.words() == "£87 10s"
    with pytest.raises(ValueError, match="holds £87 10s"):
        purse.pay(1000.0, "a ship", 11)
    purse.take(0.5, "a sale", 12)
    assert purse.entries[-1] == (12, 0.5, "a sale") and P.pounds_words(0.0) == "nothing"
    assert P.pounds_words(5.0) == "£5" and P.pounds_words(2.25) == "£2 5s"
    stores = P.Stores(100.0, 120.0)
    assert stores.words() == "water 100 tons, provisions for 120 days"
    assert "Nothing is yet expended" in stores.lines(264)[-1]


def test_the_ship_file_gives_the_hold_and_the_boats_through_the_generator():
    """No ship is special-cased: the hold's room and the boats come from each ship's
    file, written by tools/gen_ships.py from Luce's rules of size and the allowance by
    the ship's size."""
    for path, boats_wanted, hold_wanted in (
        (FRIGATE, 6, 93),
        (SCHOONER, 2, 112),
        ("data/ships/cutter.yaml", 2, 42),
        ("data/ships/brig.yaml", 3, 32),
    ):
        w = world_for(path)
        spec = w.ship.spec
        assert spec.hold is not None and spec.hold.capacity_tons == hold_wanted, path
        assert len(spec.boats) == boats_wanted, path
        assert w.hold.capacity_tons == hold_wanted
        largest = max(spec.boats, key=lambda b: (b.tons, b.length_ft))
        assert largest.kind in ("launch", "long-boat", "yawl") and largest.crew == largest.oars + 1
        for b in spec.boats:
            assert b.length_ft > 0 and b.oars >= 2 and b.tons > 0
    frigate = world_for(FRIGATE).ship.spec
    launch = next(b for b in frigate.boats if b.id == "launch")
    assert launch.length_ft == 31.0  # 2.6 root(143.2 ft), Luce 1866 'Boats'
    assert [b.kind for b in frigate.boats] == [
        "launch",
        "barge",
        "pinnace",
        "cutter",
        "cutter",
        "jolly boat",
    ]
    assert (
        world_for(FRIGATE)
        .readings.words("boats")
        .startswith("the launch (31 ft, 10 oars, 11 hands)")
    )


def test_every_paper_is_a_thing_with_a_keeper_and_a_place_and_the_stores_own_words():
    w = world_for()
    pages = w.papers.pages()
    assert [p.handle for p in pages] == [
        "the sailmaker's account",
        "the manifest",
        "the purser's books",
        "the boatswain's store book",
        "the booms' list",
        "the establishment of ground tackle",
        "the epitome's table of the establishments",
        "the price list",
    ]
    by = {p.handle: p for p in pages}
    assert by["the sailmaker's account"].keeper == "sailmaker"
    assert by["the sailmaker's account"].place == "sail_room"
    assert by["the sailmaker's account"].lines == sail_room(w.ship).inventory_lines()
    assert by["the booms' list"].lines == booms(w.ship).inventory_lines()
    assert by["the boatswain's store book"].lines == cordage(w.ship).inventory_lines()
    assert by["the establishment of ground tackle"].lines == ground_tackle(w.ship).describe()
    assert by["the manifest"].lines[0].startswith("The hold stows 93 tons of cargo")
    assert by["the purser's books"].lines[0] == "Water: 100 tons in the ground tier."
    epitome = by["the epitome's table of the establishments"]
    assert epitome.keeper == "master" and epitome.place == "cabin"
    assert "Falmouth: 5h 15m at full and change; springs rise 15 feet." in epitome.lines
    assert by["the price list"].lines == [
        "No price list aboard: the boat has not been ashore in any port."
    ]
    # dated by the last entry: the muster at the start, until a keeper writes it
    assert all(p.as_of == "10 June, Forenoon watch, 4 bells (10:00)" for p in pages)
    w.run(90)
    line = w.papers.write("the manifest", "twenty tons of tin stowed")
    assert line == "The manifest written up by the purser: twenty tons of tin stowed."
    assert w.papers.page("manifest").as_of == "10 June, Forenoon watch (10:01)"
    assert w.papers.page("sailmaker").as_of_tick == 0
    with pytest.raises(KeyError):
        w.papers.page("the signal book")


def test_the_mate_keeps_the_pursers_papers_in_a_merchantman():
    w = world_for(SCHOONER)
    assert w.papers.page("the manifest").keeper == "mate"
    assert w.papers.write("the price list", "the prices at Falmouth").startswith(
        "The price list written up by the mate"
    )


def test_the_papers_are_served_by_handle_through_the_library_to_every_station_the_same():
    """Papers-and-Books.md: in-world things read through the same tool and shelf as the
    reference; the parity gap 33d found (a paper reachable only through submit_order)
    closes here: the watcher, the captain and the browser's pane read one page."""
    w = world_for()
    listing = tools.library(w, "watcher", "papers")
    assert listing.startswith("the ship's papers: 8 papers aboard, each by handle")
    assert "  2. the manifest, about" in listing
    page = tools.library(w, "watcher", "papers", section="manifest")
    assert page.title == "the ship's papers, the manifest"
    assert page.reopen == "library(topic='papers', section='manifest')"
    assert page.splitlines()[0].startswith(
        "The manifest: the hold's capacity and the cargo in it by tons, with the purse; kept by "
        "the purser in the hold; last written 10 June"
    )
    assert page.splitlines()[1:] == w.papers.page("manifest").lines
    # the same page whatever the station; a station with no authority reads it too
    assert str(tools.call(w, "lookout", "library", {"topic": "papers", "section": "2"})) == str(
        page
    )
    assert str(tools.library(w, "captain", "the ship's papers", "manifest")) == str(page)
    whole = tools.library(w, "watcher", "papers", section="all")
    assert "The epitome's table of the establishments:" in whole
    found = tools.library(w, "watcher", "papers", find="Falmouth")
    assert "[the ship's papers, the epitome" in found
    # listed in the contents beside the ship, with its handles
    contents = tools.library(w, "watcher", "contents")
    assert "  papers: the ship's papers, 8 aboard" in contents
    # the pane's route serves the same lines (tests/test_server.py has the route itself)
    from freesail.ui.server import ship_papers

    pane = ship_papers(w)
    assert pane["waiting"] == [] and [p["handle"] for p in pane["papers"]][1] == "the manifest"
    assert pane["papers"][1]["lines"] == w.papers.page("manifest").lines
    # a point ship keeps none, and the library says so rather than failing
    from freesail.core.world import World

    bare = World(seed=1)
    assert "keeps no papers" in tools.library(bare, "watcher", "papers")
