"""The door follows its harness (package 82b, item 1; `docs/design/Design-DoorAndVisitor.md` §2).

A seat of the agent API's desk is keyed to its harness's identity (`Harness.ident`, carried in
the save), never to a station's name and a ship: a station whose person goes aboard another
ship keeps its door, its model and its identity through the move, a stationing again by its own
name, and a save and a load; two "captain" stations of two hulls through one door each are each
answered by their own harness, and a stand-down of one leaves the other.

Driven on the desk itself (`remote.Desk`, the routes' half), with the door's replies as the
script; the identities are made up and the consent records go to a temporary directory.
"""

from __future__ import annotations

import json
import threading

from freesail.agents import consent
from freesail.agents.remote import Desk, home_harness
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.world.seats import _voice_name
from tests.test_between_hulls import _brig_alongside, _run_until

WEIGHTS = "made-up-model-Q4, for the door that follows"


def _desk(tmp_path, world):
    records = tmp_path / "consent"
    consent.Record(
        WEIGHTS,
        "a test runtime",
        "2026-09-26",
        consent.YES,
        answer="Yes.",
        drill=consent.DRILL_PASSED,
    ).write(records)
    return Desk(threading.RLock(), lambda: world, records_dir=records, saves_dir=tmp_path / "s")


def _order(desk, ship, answer, text):
    """The door's reply at its open turn: one order of its station's."""
    body = {
        "calls": [{"name": "submit_order", "args": {"text": text}}],
        "key": answer["key"],
        "ship": ship,
    }
    return desk.reply("captain", body)


def _two_captains_one_moved(tmp_path):
    """The frigate's captain and the brig X's captain, each through a door of the same model;
    the brig's captain sends himself aboard the frigate in his own boat (his station's order,
    an input), and is there as a visitor."""
    w, b, hull = _brig_alongside()
    desk = _desk(tmp_path, w)
    own = desk.station("captain", {"model_name": WEIGHTS, "door": "api"})
    far = desk.station("captain", {"model_name": WEIGHTS, "door": "api", "ship": "X"})
    h_own, h_far = w.own.agents["captain"], hull.agents["captain"]
    assert h_own.ident != h_far.ident
    _run_until(w, lambda: h_far.open_sample is not None, 0.5)
    _order(desk, "X", far, f"send the boat to the {w.ship.name} with the captain")
    captain = hull.people.captain
    _run_until(w, lambda: captain.hull == w.own.id, 1.5)
    assert h_far.visiting and h_far.world is w.own
    return w, b, hull, desk, own, far, h_own, h_far, captain


def test_the_moved_station_keeps_its_door_its_model_and_its_identity(tmp_path):
    w, b, hull, desk, own, far, h_own, h_far, captain = _two_captains_one_moved(tmp_path)
    ident = h_far.ident
    assert ident == f"{b.id}/captain"
    # the door's calls by its own address and key reach its harness where it is now
    seat = desk._seat("captain", far["key"], "X")
    assert seat.harness is h_far and seat.ident == ident and seat.hull is w.own
    assert desk.turns("captain", 0, 0, key=far["key"], ship="X")["model_name"] == WEIGHTS
    # the listing names him by his station, his ship and his host, with his identity
    rows = {d["ident"]: d for d in desk.stations() if "ident" in d}
    assert rows[ident]["station"] == f"captain, of the X, aboard the {w.ship.name}"
    assert rows[h_own.ident]["station"] == "captain"
    # a stationing again by its own name (a door restarted) attaches to the same harness,
    # and no fresh station is made on the brig
    again = desk.station("captain", {"model_name": WEIGHTS, "door": "api", "ship": "X"})
    assert again.get("attached") and desk._seat("captain", again["key"], "X").harness is h_far
    assert "captain" not in hull.agents and home_harness(hull, "captain") is h_far
    assert len([s for s in desk.seats.values() if s.harness is h_far]) == 1


def test_the_moved_station_keeps_its_identity_through_the_save_and_a_door_after_the_load(
    tmp_path,
):
    w, b, hull, desk, own, far, h_own, h_far, captain = _two_captains_one_moved(tmp_path)
    data = json.loads(json.dumps(w.save()))
    idents = sorted(a["ident"] for blk in data["hulls"] for a in blk.get("agents", [])) + sorted(
        a["ident"] for a in data["agents"]
    )
    assert set(idents) == {h_own.ident, h_far.ident}
    voice = _voice_name(captain)
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        moved = copy.agents.get(voice)
        assert moved is not None and moved.visiting and moved.ident == h_far.ident, road
        assert copy.agents["captain"].ident == h_own.ident, road
        # the door after the load stations by its own name and takes up its own harness,
        # visiting where its person is; nothing is made at the brig's captain's station
        d2 = _desk(tmp_path / road, copy)
        d2.station("captain", {"model_name": WEIGHTS, "door": "api", "ship": "X"})
        seat = d2.seat_at("captain", "X")
        assert seat is not None and seat.harness is moved, road
        assert "captain" not in copy.hulls[b.id].agents, road


def test_two_captains_through_one_door_each_answered_by_its_own_and_one_stood_down(tmp_path):
    w, b, hull, desk, own, far, h_own, h_far, captain = _two_captains_one_moved(tmp_path)
    assert desk._seat("captain", own["key"]).harness is h_own
    assert desk._seat("captain", far["key"], "X").harness is h_far
    # the stand-down by the visitor's name on the frigate stands down his harness alone
    w.submit(f"stand down the {_voice_name(captain)}")
    _run_until(w, lambda: h_far.agent.released, 0.25)
    assert h_far.agent.released and not h_own.agent.released
    assert desk.turns("captain", 0, 0, key=own["key"])["released"] is False
    assert desk.turns("captain", 0, 0, key=far["key"], ship="X")["released"] is True
    # and the other door's station is answered as before, its own turn its own
    rows = {d["ident"]: d for d in desk.stations() if "ident" in d}
    assert rows[h_own.ident]["state"] != "released" and rows[h_far.ident]["state"] == "released"
