"""The visitor keeps his own station's name (package 82b, item 2; `Design-DoorAndVisitor.md` §3).

A station whose person goes aboard another ship is named there by his own station, his ship
and hers, "officer of the watch, of the X, aboard the Amazon": in the host's stations, the
desk's listing, `where am I` and the log's mark. The host's sentences address him by that
name with its commas or without, by "the officer of the watch of the X" and by his person's
name; the host's own officer of the watch is untouched and answered by his own harness.

Driven on the desk (`remote.Desk`) and by `put_aboard`, the one road for a person's change of
hull; the identities are made up and the consent records go to a temporary directory.
"""

from __future__ import annotations

from freesail.agents.harness import say_aboard
from freesail.world import movement as M
from tests.test_between_hulls import _brig_alongside
from tests.test_door_follows import WEIGHTS, _desk

OOW = "officer of the watch"


def _officer_visiting(tmp_path):
    """The brig X's officer of the watch and the frigate's, each through a door of the same
    model; the brig's goes aboard the frigate (`put_aboard`, the boat's road) and is there
    as a visitor."""
    w, b, hull = _brig_alongside()
    desk = _desk(tmp_path, w)
    desk.station(OOW, {"model_name": WEIGHTS, "door": "api", "ship": "X"})
    desk.station(OOW, {"model_name": WEIGHTS, "door": "api"})
    h_far, h_own = hull.agents[OOW], w.own.agents[OOW]
    person = hull.stations.holder(OOW)
    M.put_aboard(w, person, w.own, by="the boat")
    assert h_far.visiting and h_far.world is w.own
    return w, b, hull, desk, h_far, h_own, person


def test_the_visitor_is_named_by_his_station_his_ship_and_hers(tmp_path):
    w, b, hull, desk, h_far, h_own, person = _officer_visiting(tmp_path)
    host = w.ship.name
    words = f"officer of the watch, of the X, aboard the {host}"
    name = words.lower()
    # the host's stations: his under the new name, the passenger's kind; hers unchanged
    assert h_far.station.name == name and w.own.agents[name] is h_far
    assert w.stations.holder(name) is person and w.stations.kind_of(name) == "passenger"
    assert w.own.agents[OOW] is h_own and not h_own.visiting
    assert w.stations.holder(OOW) is not person
    # the desk's listing, with the names as the ships say them
    rows = {d["ident"]: d["station"] for d in desk.stations() if "ident" in d}
    assert rows[h_far.ident] == words and rows[h_own.ident] == OOW
    # where am I: aboard her, a visitor, standing at his own station's name
    assert M.where_am_i(w, person).endswith(f"a visitor, of the X, standing as the {words}")
    # the log's mark of his words
    e = say_aboard(w, name, person.name, "A fine ship.")
    assert e.text == f"[{name}] A fine ship." and e.data["station"] == name


def test_the_visitor_is_addressed_by_each_form_and_the_hosts_officer_by_his_own(tmp_path):
    w, b, hull, desk, h_far, h_own, person = _officer_visiting(tmp_path)
    host = w.ship.name
    name = f"officer of the watch, of the x, aboard the {host.lower()}"
    for said in (
        f"tell the officer of the watch, of the X, aboard the {host} to keep a lookout",
        f"tell the officer of the watch of the X, aboard the {host} to keep a lookout",
        "tell the officer of the watch of the X to keep a lookout",
        "tell the officer of the watch, of the X: keep a lookout",
        f"tell {person.name} to keep a lookout",
    ):
        e = w.submit(said)
        assert e.kind == "agent.told" and e.data.get("station") == name, (said, e.text)
        assert h_far.agent.word.endswith("keep a lookout"), said
        h_far.agent.word = ""
    # the host's own officer of the watch, by his name and by its alias, is his own
    for said in (
        "tell the officer of the watch to keep a lookout",
        "tell the officer of the watch, keep a lookout",
        "tell the officer to keep a lookout",
    ):
        e = w.submit(said)
        assert e.kind == "agent.told" and e.data.get("station") == OOW, (said, e.text)
        assert h_own.agent.word.endswith("keep a lookout") and not h_far.agent.word, said
        h_own.agent.word = ""


def test_the_visitor_home_again_has_his_own_station_and_the_name_is_let_go(tmp_path):
    w, b, hull, desk, h_far, h_own, person = _officer_visiting(tmp_path)
    name = h_far.station.name
    M.put_aboard(w, person, hull, by="the boat")
    assert not h_far.visiting and h_far.station.name == OOW and hull.agents[OOW] is h_far
    assert not w.stations.aboard(name) and name not in w.own.agents
    assert w.own.agents[OOW] is h_own
