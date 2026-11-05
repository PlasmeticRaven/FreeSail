"""Package 82, item 6 (the design's §7): the stations, the director and the readings with
the boat a hull and the person aboard another ship. The reading `the followed ship`; the
events `the boat manned`, `the boat lost`, `the tow begun`, `the tow ended` and `aboard
another ship`; the director's `follow "X"` as a driver's line through the channel, and the
boat lost by the `aboard:` table (stove, swamped, gone adrift); the truth showing a manned
boat as a vessel with her ship, who is in her and what she is under; the harness's words
for a station in a boat. Truth 7-332 is in tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

from freesail.agents import director as D
from freesail.api import readings as R
from freesail.api.readings import director_readings
from freesail.world import boats as B
from freesail.world import orders as WO
from tests.test_crews import hove_to_world, put
from tests.test_observer import observed_world
from tests.test_ports import CARRICK_ROAD, at_anchor_in

CUTTER = "data/ships/cutter.yaml"


def _events(w, kind):
    return [e for e in w.log if e.kind == kind]


def test_the_followed_ship_reading_names_the_drivers_centre_the_boat_and_the_view():
    w = hove_to_world()
    r = w.readings["followed"]
    assert r["words"].endswith(", the player's ship") and not r["observer"]
    assert w.readings.words("followed") == r["words"]
    w.submit("go to the launch")
    r = w.readings["followed"]
    assert "launch, a boat of the " in r["words"] and "manned as a hull" in r["words"]
    w.submit("come alongside")
    for _ in range(30):
        w.run(60)
        if not B.is_boat(w.own):
            break
    assert w.readings["followed"]["words"].endswith(", the player's ship")
    ob, _sf = observed_world()
    r = ob.readings["followed"]
    assert r["observer"] and r["words"].startswith("no ship followed; the observer's view at")


def test_the_events_registry_has_the_boats_events_and_a_standing_order_takes_them():
    for words in (
        "the boat manned",
        "the boat lost",
        "the tow begun",
        "the tow ended",
        "aboard another ship",
    ):
        assert words in R.EVENTS and not R.EVENTS[words].absent, words
    assert R.EVENTS["the boat manned"].kind == "boat.manned"
    assert R.EVENTS["the tow begun"].kind == "boat.towing"
    w = hove_to_world()
    for words in ("the boat manned", "the tow ended", "aboard another ship"):
        e = w.submit(f'standing order "{words[:6]}": at {words} then trim sails')
        assert e.kind == "standing.given", e.text
    spec = R.EVENTS["aboard another ship"]
    assert spec.test({"ship": "the ship:x", "by": "the boat"})
    assert not spec.test({"ship": "the ship", "by": ""})


def test_the_director_follows_a_ship_as_a_drivers_line_and_the_dry_run_says_so():
    assert WO.parse('follow "the ship"').channel == "follow" and "follow" in WO.CHANNELS
    assert D.form_of("follow").examples == ('follow "the ship"',)
    w = hove_to_world()
    frigate = w.players
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    assert b.crew is not None
    said = D.dry_run(w, f'follow "{b.name}"')
    assert "it would be performed as a driver's line, no act spent" in said and b.name in said
    assert w.own is frigate  # the dry run moved nothing
    before = D.budget_of(w).acts
    said = D.direct(w, f'follow "{b.name}"', by="the test")
    assert said.startswith(f"Following the {b.name}"), said
    assert w.own is b.crew and D.budget_of(w).acts == before  # no act spent
    assert _events(frigate, "driver.follow") or _events(w, "driver.follow")
    said = D.direct(w, 'follow "the ship"', by="the test")
    assert said.startswith("Following the") and w.own is frigate
    said = D.direct(w, "follow nobody", by="the test")
    assert said.startswith("Refused:") and "observed world alone" in said
    # through the channel as a world order (a scenario's line), the same driver's line
    e = w.world_order(f'follow "{b.name}"', source="the scenario")
    assert e.kind == "world.order" and "Following the" in e.text and w.own is b.crew
    w.world_order('follow "the ship"', source="the scenario")
    assert w.own is frigate
    ob, _sf = observed_world()
    said = D.direct(ob, "follow nobody", by="the test")
    assert said.startswith("Following no ship:")


def test_the_boat_lost_by_the_directors_word_and_doubted_on_a_smooth_sea():
    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER)
    said = D.dry_run(w, "aboard: the boat stove")
    assert "it would be" in said and not w.dealings.boat.lost  # nothing moved on the world
    said = D.direct(w, "aboard: the boat gone adrift", by="the test")
    assert "painter parted" in said or "gone adrift" in said, said
    assert w.dealings.boat.lost == "cut adrift"
    assert _events(w, "aboard.found") and _events(w, "boat.lost")
    e = w.submit("send the boat ashore for the prices")
    assert e.kind == "order.rejected" and "is lost" in e.text
    # a second loss: doubted once on the record (a smooth sea), then with its reason the
    # game says it has no way to lose a boat lost already
    said = D.direct(w, "aboard: the boat stove", by="the test")
    assert said.startswith("Doubted"), said
    said = D.direct(w, "aboard: the boat stove [reason: a sea in the night]", by="the test")
    assert "lost already" in said, said
    # swamped: doubted on a smooth sea, performed with a reason
    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER)
    said = D.direct(w, "aboard: the boat swamped", by="the test")
    if said.startswith("Doubted"):
        said = D.direct(w, "aboard: the boat swamped [reason: a squall]", by="the test")
    assert w.dealings.boat.lost == "swamped", said


def test_the_truth_shows_a_manned_boat_as_a_vessel_and_the_harness_names_her():
    from freesail.world.crews import shape_words

    w = hove_to_world()
    frigate = w.players
    w.submit("go to the launch")
    boat = w.own
    w.submit("give way")
    w.run(2)
    with w.as_hull(frigate):
        t = director_readings(w)
    rows = [s for s in t["ships"] if s.get("boat_of")]
    assert rows and rows[0]["boat_of"] == "Amazon" and rows[0]["under"] == "oars"
    assert "Captain" in rows[0]["in_her"]
    assert "'s boat, a hull of the world, under oars" in t["words"] and "in her:" in t["words"]
    assert "a hull of the one world under your oars" in shape_words(boat)
    words = R.ship_words(w)
    assert "a ship's boat of the Amazon's" in words and "10 oars" in words
