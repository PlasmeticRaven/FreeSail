"""Package 82, item 4 (the design's §5): the boat as a hull of the one world.

A ship's boat with a file of her own is manned as a vessel of the sea with a hull of her own
when she is commanded (`go to the boat`), pulls at three to four knots light under her oars
and slower as the men tire (`physics/oars.py`), steps her mast and sails under her lug,
comes alongside and is hoisted in with her log folded into the ship's; her errands run as
before with nobody in her, and the hoy comes off as a vessel of the sea; a boat lost is sent
on no errand and manned by nobody until the yard replaces her. Truths 7-327, 7-328, 7-329
and 7b-114 are in tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

import json

from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.physics.oars import oars_of
from freesail.world import boats as B
from freesail.world.geo import bearing_and_distance
from tests.test_crews import hove_to_world
from tests.test_ports import CARRICK_ROAD, at_anchor_in

CUTTER = "data/ships/cutter.yaml"


def _run_until(w, cond, minutes: int) -> int:
    for i in range(minutes):
        w.run(60)
        if cond():
            return i + 1
    return minutes


def _kn(w) -> float:
    return float(w.readings["speed"]) / 0.5144


# ---------------------------------------------------------------------------
# the boat manned and away (truth 7-327)
# ---------------------------------------------------------------------------


def test_go_to_the_boat_mans_her_as_a_hull_and_the_drivers_follow_the_player():
    w = hove_to_world()
    frigate = w.players
    assert "the launch (31 ft, 10 oars, 11 hands)" in w.readings.words("boats")
    assert w.readings.words("boat") == "the launch at the booms"
    e = w.submit("go to the launch")
    assert e.kind == "person.aboard" and "hoisted out and manned" in e.text
    assert "went down into the Amazon's launch" in e.text
    boat = w.own
    assert B.is_boat(boat) and w.followed == boat.id and boat.id == f"{frigate.id}:launch"
    assert boat.ship.name == "the Amazon's launch" and B.ship_of(w, boat) is frigate
    assert w.hulls[boat.id] is boat and boat.awake
    vessel = w.vessels.find("the Amazon's launch")
    assert vessel is not None and vessel.boat and vessel.crew is boat
    assert frigate.dealings.boat.hull == boat.id and frigate.dealings.boat.away
    assert frigate.dealings.boat.words() == "the launch manned and away as a hull of her own"
    with w.as_hull(frigate):
        assert frigate.dealings.boat_reading()["manned"] is True
    people = [p.name for p in w.registry.aboard(boat.id)]
    assert frigate.people.captain.name in people and len(people) == 2  # and her coxswain
    assert w.submit("where am i").text.endswith("in the Amazon's launch, the oars in.")
    assert any(e.kind == "hull.followed" for e in boat.log)
    # the mast is down and the lug cannot be set until it is stepped
    e = w.submit("set the lug")
    assert e.kind == "order.rejected" and "'step the mast' first" in e.text
    # the ship's grammar in the boat is refused naming what she has not
    e = w.submit("set the royals")
    assert e.kind == "order.rejected" and "no such part as the royals" in e.text
    # a second boat: the barge has no file of her own
    e = w.submit("go to the barge")
    assert e.kind == "order.rejected" and "already" in e.text
    w.submit("come alongside")
    _run_until(w, lambda: not B.is_boat(w.own), 10)
    e = w.submit("go to the barge")
    assert e.kind == "order.rejected" and "has no file of her own to be a vessel by" in e.text
    # the ship's orders are refused in words at the ship
    e = w.submit("give way")
    assert e.kind == "order.rejected" and "this hull has no oars" in e.text


def test_the_boat_pulls_at_three_to_four_knots_fresh_and_slower_as_the_men_tire():
    w = hove_to_world()
    w.submit("go to the launch")
    boat = w.own
    oars = oars_of(boat.ship)
    assert oars is not None and oars.number == 10 and not oars.out
    e = w.submit("give way")
    assert e.kind == "boat.oars" and "give way together" in e.text
    assert oars.out and oars.manned == 10 and oars.stroke == 1.0
    w.run(240)
    fresh = _kn(w)
    assert 3.0 <= fresh <= 4.0, fresh
    assert 0.06 <= oars.hours <= 0.07  # four minutes at the oars
    oars.hours = 4.0  # the men four hours at the oars: half their strength
    w.run(240)
    tired = _kn(w)
    assert 2.5 <= tired < fresh - 0.3, (fresh, tired)
    assert "the men 4." in w.submit("where am i").text
    e = w.submit("easy all")
    assert "a light stroke" in e.text and oars.stroke == 0.5
    w.run(180)
    assert _kn(w) < tired
    e = w.submit("lie on your oars")
    assert oars.stroke == 0.0 and oars.out
    rested_from = oars.hours
    w.run(120)
    assert oars.hours < rested_from  # resting
    e = w.submit("pull for NE")
    assert "Pulling NE" in e.text and oars.stroke == 1.0
    w.run(180)
    assert abs(float(w.readings["heading"]) - 0.785) < 0.2
    e = w.submit("boat your oars")
    assert not oars.out and oars.manned == 0
    coasting = _kn(w)
    assert coasting > 0.5
    w.run(300)
    assert _kn(w) < coasting - 0.5  # her way coming off her with the oars in


def test_the_boat_steps_her_mast_sails_under_her_lug_and_comes_alongside_with_her_log_folded():
    w = hove_to_world()
    frigate = w.players
    w.submit("go to the launch")
    boat = w.own
    w.submit("give way")
    w.run(300)
    e = w.submit("step the mast")
    assert e.kind == "boat.mast" and "stepped" in e.text
    e = w.submit("set the lug")
    assert e.kind == "order.accepted"
    w.run(120)
    e = w.submit("give way")
    assert e.kind == "order.rejected" and "The lug is drawing" in e.text
    sailing = _kn(w)
    assert sailing > 2.0
    e = w.submit("unstep the mast")
    assert e.kind == "order.rejected" and "take it in" in e.text
    w.submit("take in the lug")
    w.run(120)
    assert w.submit("unstep the mast").kind == "boat.mast"
    before = len(frigate.log)
    e = w.submit("come alongside")
    assert e.kind == "boat.alongside" and "Pulling for the Amazon" in e.text
    minutes = _run_until(w, lambda: not B.is_boat(w.own), 40)
    assert minutes < 40
    assert w.own is frigate and w.followed == frigate.id
    assert boat.id not in w.hulls
    gone = w.vessels.find("the Amazon's launch")
    assert gone is None or gone.done
    assert frigate.dealings.boat.words() == "the launch at the booms"
    assert w.readings.words("boat") == "the launch at the booms"
    assert w.submit("where am i").text.endswith("aboard the Amazon, on the deck.")
    since = list(frigate.log)[before:]
    assert any(e.kind == "boat.hoisted_in" and "Captain" in e.text for e in since)
    folded = [e for e in since if e.kind == "boat.log"]
    assert folded and all(e.text.startswith("The Amazon's launch, ") for e in folded)
    assert any("Order: give way" in e.text for e in folded)
    assert any(e.kind == "hull.followed" and "back aboard" in e.text for e in since)
    # the people are hers again: the captain on deck, the coxswain gone with her
    assert frigate.people.captain.hull == frigate.id
    assert not [p for p in w.registry.aboard(boat.id)]


def test_the_boats_voyage_replays_to_the_same_digests():
    w = hove_to_world()
    frigate = w.players
    w.submit("go to the launch")
    w.submit("give way")
    w.run(300)
    w.submit("pull for NE")
    w.run(300)
    w.submit("step the mast")
    w.submit("set the lug")
    w.run(300)
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.followed == w.followed and B.is_boat(copy.own)
    assert copy.log.digest() == w.log.digest()
    assert copy.players.log.digest() == frigate.log.digest()
    w.submit("take in the lug")
    w.run(120)
    w.submit("come alongside")
    _run_until(w, lambda: not B.is_boat(w.own), 60)
    assert w.own is frigate
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.own is copy.players and copy.log.digest() == w.log.digest()
    assert copy.players.dealings.boat.words() == "the launch at the booms"


# ---------------------------------------------------------------------------
# the errands as before, and the hoy a vessel (truth 7-328)
# ---------------------------------------------------------------------------


def test_the_boats_errands_run_as_before_with_nobody_in_her():
    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER)
    hulls = set(w.hulls)
    e = w.submit("send the boat ashore for the prices")
    assert e.kind != "order.rejected", e.text
    assert w.dealings.boat.away and not w.dealings.boat.hull
    assert set(w.hulls) == hulls  # no hull made for the script's errand
    e = w.submit("go to the boat")
    assert e.kind == "order.rejected" and "is away already" in e.text
    _run_until(w, lambda: not w.dealings.boat.away, 180)
    assert not w.dealings.boat.away
    # `go ashore` lands him by the script, in no hull
    captain = w.people.captain
    e = w.submit("go ashore")
    assert e.kind != "order.rejected", e.text
    assert not captain.aboard and captain.where == "boat" and captain.hull is None
    assert set(w.hulls) == hulls


def test_the_hoy_comes_off_as_a_vessel_of_the_sea_and_the_lookout_sees_her():
    from tests.test_ordnance import THE_SOUND, after_the_action, events, hurry
    from tests.test_ordnance import at_anchor_in as anchored

    w = anchored(THE_SOUND, papers={"service": "kings"}, cargo={"purse_pounds": 100.0})
    after_the_action(w.ship)
    e = w.submit("buy powder and shot of necessity")
    assert e.kind == "ordnance.demanded", e.text
    hoy = next((v for v in w.vessels.vessels if "hoy" in v.name and not v.done), None)
    assert hoy is not None and hoy.boat and hoy.kind == "a hoy"
    assert hoy.plan and hoy.plan[0][0] == "to_ship"
    job = next(j for j in w.dealings.jobs if j.kind == "ordnance")
    assert job.payload["hoy"] == hoy.id
    w.run(1800)
    assert (
        bearing_and_distance(w.position, hoy.position)[1]
        < bearing_and_distance(w.position, w.dealings.ports["plymouth"].shore.position)[1]
    )
    hurry(w)
    assert events(w, "ordnance.alongside")
    hurry(w)
    assert events(w, "ordnance.stowed")
    assert hoy.plan and hoy.plan[0][0] == "to"  # home to the shore


# ---------------------------------------------------------------------------
# the boat lost (truth 7-329)
# ---------------------------------------------------------------------------


def test_the_boat_cut_adrift_is_lost_until_the_yard_replaces_her():
    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER, cargo={"purse_pounds": 100.0})
    e = w.submit("cut the boat adrift")
    assert e.kind == "boat.lost" and "cut adrift by order" in e.text
    state = w.dealings.boat
    assert state.lost == "cut adrift" and state.lost_tick == w.clock.tick
    assert w.readings.words("boat").startswith("the boat lost: cut adrift on the ")
    e = w.submit("send the boat ashore for the prices")
    assert e.kind == "order.rejected" and "is lost" in e.text
    e = w.submit("go to the boat")
    assert e.kind == "order.rejected" and "is lost" in e.text
    e = w.submit("cut the boat adrift")
    assert e.kind == "order.rejected" and "lost already" in e.text
    from freesail.api.readings import director_readings

    assert "lost" in director_readings(w)["words"]
    e = w.submit("demand a boat of the yard")
    assert e.kind != "order.rejected", e.text
    assert "Demanded a boat" in e.text and "48 hours" in e.text
    w.run(int(B.NEW_BOAT_HOURS * 3600) + 120)
    assert not w.dealings.boat.lost and w.readings.words("boat") == "the boat at the booms"
    assert any("a new boat came off from the yard" in e.text for e in w.log)
    assert w.submit("demand a boat of the yard").kind == "order.rejected"


def test_the_boat_swamped_loses_her_people_and_the_ship_says_so():
    w = hove_to_world()
    frigate = w.players
    w.submit("go to the launch")
    boat = w.own
    captain = frigate.people.captain
    assert captain.hull == boat.id
    text = B.lose_boat(w, frigate, "swamped", "swamped in a heavy sea")
    assert "swamped in a heavy sea" in text and captain.name in text
    assert captain.dead and not captain.aboard and captain.hull is None
    assert w.followed == frigate.id and w.own is frigate and boat.id not in w.hulls
    lost = [e for e in frigate.log if e.kind == "boat.lost"]
    assert lost and lost[-1].severity.value == "urgent"
    assert frigate.dealings.boat.lost == "swamped"
    assert w.readings.words("boat").startswith("the launch lost: swamped on the ")
    assert B.manned_hull(w, frigate) is None


def test_a_sea_above_her_weather_swamps_her_by_the_sea_states():
    assert "short" in B.SWAMP_STATES_SMALL and "short" not in B.SWAMP_STATES_LARGE
    assert "heavy" in B.SWAMP_STATES_LARGE and "moderate" not in B.SWAMP_STATES_SMALL


# ---------------------------------------------------------------------------
# the cutter's boat ashore at Falmouth and back under her lug (truth 7b-114)
# ---------------------------------------------------------------------------


def the_cutters_boat_ashore_and_back():
    """The player in the cutter's boat pulls ashore at Falmouth from Carrick Road under
    oars, steps the mast and sails her back under her lug, the readings his in the boat
    and the ship's again aboard."""
    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER)
    cutter = w.players
    assert w.dealings.in_port().name == "Falmouth"
    ship_speed = w.readings["speed"]
    e = w.submit("go to the boat")
    assert e.kind == "person.aboard" and B.is_boat(w.own)
    boat = w.own
    e = w.submit("pull for the quay")
    assert "Pull for the quay at Falmouth" in e.text
    minutes = _run_until(w, lambda: any(x.kind == "boat.at_quay" for x in boat.log), 60)
    assert minutes < 60, minutes
    assert (
        "Alongside the quay at Falmouth"
        in [x for x in boat.log if x.kind == "boat.at_quay"][0].text
    )
    quay = w.dealings.ports["falmouth"].shore.position
    assert bearing_and_distance(w.position, quay)[1] <= B.QUAY_M
    # the readings are his in the boat: her way, the wind at her, the ship a sail in sight
    assert w.readings["speed"] is not None and w.readings["speed"] != ship_speed
    sight = str(w.readings["in_sight"]["words"])
    assert "cutter" in sight.lower() or "sail" in sight.lower()
    assert "in the Sherbourne's boat" in w.submit("where am i").text
    w.submit("step the mast")
    assert w.submit("set the lug").kind == "order.accepted"
    from freesail.ship.parts import SailState

    lug = boat.ship.sails["lug"]
    assert _run_until(w, lambda: lug.state == SailState.SET, 10) < 10
    w.run(60)
    assert _kn(w) > 0.5
    e = w.submit("come alongside")
    assert e.kind == "boat.alongside" and "under the lug" in e.text
    minutes = _run_until(w, lambda: not B.is_boat(w.own), 90)
    assert minutes < 90 and w.own is cutter
    assert w.readings["speed"] == cutter.readings["speed"]
    assert w.submit("where am i").text.endswith("aboard the Sherbourne, on the quarterdeck.")
    assert w.readings.words("boat") == "the boat at the booms"
    return w


def test_the_cutters_boat_pulls_ashore_at_falmouth_and_sails_back_under_her_lug():
    the_cutters_boat_ashore_and_back()
