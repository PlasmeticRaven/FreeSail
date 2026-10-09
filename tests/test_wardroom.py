"""The wardroom (spec M6 §2; package 40): the ship's company as people with outlines,
the stations bound to a person by data, the ship files and the wardroom files agreeing,
and a scenario free to name any of them."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import yaml

from freesail.agents.agent import OFFICER, officer_rank, station_holder
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.ship.loader import load_spec
from freesail.world import people as PE

ROOT = Path(__file__).resolve().parents[1]
SHIPS = {
    "frigate-36": "data/ships/frigate-36.yaml",
    "topsail-schooner": "data/ships/topsail-schooner.yaml",
    "cutter": "data/ships/cutter.yaml",
    "brig": "data/ships/brig.yaml",
}
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}


def world_for(ship: str, **kw):
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


def test_the_ship_files_posts_and_people_agree_with_the_wardroom_files():
    """The generator draws the posts and the drawn roles from `data/people/<ship>.yaml`
    (spec M6 §2): the ship file's `crew.posts` are the file's posts in its order, and its
    `crew.people` the file's drawn roles with their stations, ratings and the messenger."""
    for stem, path in SHIPS.items():
        wardroom = PE.load_wardroom(path)
        assert wardroom is not None, stem
        spec = load_spec(ROOT / path)
        assert [p.post for p in spec.crew.posts] == wardroom.posts, stem
        drawn = [
            (o.role, o.drawn["station"], o.drawn.get("rating"), o.messenger) for o in wardroom.drawn
        ]
        assert [(p.role, p.station, p.rating, p.messenger) for p in spec.crew.people] == drawn
        raw = yaml.safe_load((ROOT / "data" / "people" / f"{stem}.yaml").read_text("utf-8"))
        assert raw["ship"] == path
        assert wardroom.role_of("captain") and wardroom.role_of("officer of the watch")


def test_every_station_holder_has_his_outline_his_rank_and_his_place_from_the_file():
    """Each person of the muster is given the file's outline by his role, in the file's
    order where a role is held twice; the outline is a few traits, a line of history and
    a station brief, said in a sentence or two; his place at the start is the file's."""
    w = world_for(SHIPS["frigate-36"])
    people = w.people
    assert people.wardroom is not None
    for p in people.all:
        assert p.outline is not None, p.role
        assert p.outline.traits and p.outline.history and p.outline.brief, p.role
        assert p.rank == p.outline.rank and p.to_dict()["rank"] == p.rank
    captain = people.captain
    assert captain.rank == "post-captain"
    words = captain.outline_words()
    assert words.startswith(f"{captain.name}, post-captain: exact, sparing of words")
    assert "His station, the command:" in words and "Regulations of 1806" in words
    mates = people.by_role("master's mate")
    assert [m.outline.traits[0] for m in mates] == ["handy", "older"]
    assert people.find("the purser").where == "gunroom"
    assert people.find("the sailmaker").where == "sail_room"
    assert people.find("the carpenter").where == "deck"
    assert w.readings.value("where_is", "the surgeon")["outline"].startswith(
        f"{people.find('the surgeon').name}, warrant officer:"
    )
    # the small vessels: the master is the captain and the mate his officer
    for ship in ("topsail-schooner", "cutter"):
        ws = world_for(SHIPS[ship])
        assert ws.people.captain.role == "master" and ws.people.captain.outline is not None
        assert ws.people.find("the boy").outline.station == "the master's messenger"
    lines = w.people.wardroom_lines()
    assert lines[0] == words and len(lines) == len(people.all)


def test_the_harness_stations_bind_to_a_person_by_the_files_data():
    """`stations:` in the wardroom file binds the captain's station and the officer of
    the watch's to a role; `People.holder` reads it, and `officer_rank` through it, so
    that the binding is data and never a name in code (spec M6 §2)."""
    for stem, wanted in (
        ("frigate-36", ("captain", "first lieutenant")),
        ("topsail-schooner", ("master", "mate")),
        ("cutter", ("master", "mate")),
        ("brig", ("commander", "lieutenant")),
    ):
        w = world_for(SHIPS[stem])
        captain, officer = w.people.holder("captain"), w.people.holder(OFFICER)
        assert (captain.role, officer.role) == wanted, stem
        assert captain.station == "captain" and officer.station == OFFICER
        assert officer_rank(w) == (officer.name, officer.role)
        assert station_holder(w, "captain", ("x", "y")) == (captain.name, captain.role)
        assert w.people.holder("director") is None
    # a point world keeps the old rule by name alone
    from freesail.core.world import World

    bare = World(seed=1)
    assert bare.people.holder("captain").role == "captain"
    assert officer_rank(bare) == ("the first lieutenant", "first lieutenant")


def test_a_scenario_may_name_any_person_of_the_muster_and_still_add_one():
    """`people: [{role: master, name: Pentreath}]` renames the master, his sailor on the
    books and the reckoning's master with him; a role the muster has not got is a person
    added, as package 35 had it; the names of the rest stay the muster's under the seed."""
    plain = world_for(SHIPS["topsail-schooner"])
    named = world_for(
        SHIPS["topsail-schooner"],
        people=[
            {"role": "master", "name": "Captain Pentreath", "skill": 0.9},
            {"role": "mate", "name": "Mr Tozer"},
            {"role": "supercargo", "name": "Mr Fox", "place": "cabin"},
        ],
    )
    master, mate = named.people.find("the master"), named.people.find("the mate")
    assert master.name == "Mr Pentreath" and master.skill == 0.9
    assert named.navigation.master.name == "Mr Pentreath"
    assert named.people.find("Pentreath") is master and named.people.captain is master
    assert mate.name == "Mr Tozer"
    crew = named.ship.extra["crew"]
    assert crew.by_id[master.sailor_id].name == "Pentreath"
    assert crew.by_id[mate.sailor_id].name == "Tozer"
    fox = named.people.find("Fox")
    assert fox is not None and fox.role == "supercargo" and fox.where == "cabin"
    assert fox.outline is None and fox.outline_words() == "Mr Fox, supercargo."
    assert len(named.people.all) == len(plain.people.all) + 1
    boatswain = [p for p in named.people.all if p.role == "boatswain"][0]
    assert boatswain.name == plain.people.find("the boatswain").name
    assert mate.outline is not None and mate.station == OFFICER
