"""The crewed promotion (package 43; spec M6 §19, §20; truths 87 and 88): within the
range of the player's ship a far-detail vessel with a brain becomes a full part-and-crew
ship from her file, her captain's orders through the same channel, her lookout, her
account and her book; beyond it she is demoted with her state folded back; the cap with
the nearest first and a ship in dealings before a nearer one that is not; the
hysteresis; the pace with the cap full; a checkpoint with a crewed ship."""

from __future__ import annotations

import time

import pytest

from freesail import units
from freesail.core import replay as replay_mod
from freesail.world import crews as K
from freesail.world.geo import bearing_and_distance
from tests.test_brains import put, world_at


def nm_between(a, b) -> float:
    return bearing_and_distance(a, b)[1] / units.NAUTICAL_MILE


def hove_to_world():
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    return w


def test_a_vessel_with_a_brain_within_the_range_is_promoted_and_demoted_beyond_it():
    """Truth 87 in part: the brig three miles off is promoted at the first switch; her
    own World has her hull from her file, her company, her stations, her captain with
    the brain's intent and state and his book loaded, her account within half a mile of
    her truth; the far body mirrors her every tick, so the player's lookout hails one
    sail; nothing of the promotion is a line of the player's log; sailed beyond six miles
    she is demoted, her state folded back into the brain and her World dropped."""
    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    assert b.crew is not None and b.detail == "crewed" and w.vessels.crewed_ids == (b.id,)
    crew = b.crew
    assert isinstance(crew, K.CrewedWorld) and crew.shape == "full"
    assert crew.ship.name and crew.ship.spec.source.endswith("brig.yaml")
    assert crew.people.captain.name and crew.stations.aboard("captain")
    cap = crew.captain
    assert cap.intent is not None and cap.intent.words == "bound for Falmouth"
    assert cap.role == "merchant" and cap.state == "on passage" and cap.commands
    assert crew.standing.books_loaded() == ["on passage"]
    assert nm_between(crew.navigation.account_now(), crew.position) < 1.0
    assert crew.ports.ports == {} and crew.systems is None and crew.chart is w.chart
    # the body mirrored, and the player's lookout sees one sail, hailed once
    w.run(600)
    assert b.position == crew.position
    assert b.heading_deg == pytest.approx(units.rad_to_deg(crew.ship.heading) % 360.0, abs=0.01)
    hails = [e for e in w.log if e.kind == "lookout.sighting" and "brig" in e.text]
    assert len(hails) == 1
    assert not [e for e in w.log if e.kind.startswith("crew.")]
    assert [e for e in crew.log if e.kind == "crew.promoted"]
    # her captain's orders go through her own channel, under the rules actor, in her log
    assert any(str(e.actor).startswith("captain's rule") for e in crew.log)
    assert not any(str(e.actor).startswith("captain's rule") for e in w.log)
    # her lookout sees the player's ship as a sail and makes out her colours
    seen = [e for e in crew.log if e.kind in ("lookout.sighting", "lookout.made_out")]
    assert any("ship" in e.text.lower() for e in seen)
    # sailed away westward she is demoted beyond six miles, the state folded back
    w.world_order('ship "X": intent bound for 49 30 N 6 30 W')
    for _ in range(400):
        w.run(60)
        if b.crew is None:
            break
    d = nm_between(w.position, b.position)
    assert b.crew is None and b.detail == "far" and d >= K.CREWED_DEMOTE_NM - 0.2
    assert b.brain.state == "on passage" and b.plan and b.plan[0][0] == "to"
    assert w.vessels.crewed_ids == ()
    assert not w.vessels.to_dict()[0]["crewed"]


def test_the_cap_holds_the_nearest_first_and_a_ship_in_dealings_before_a_nearer_one():
    w = hove_to_world()
    ships = []
    for i, (lat, lon) in enumerate(
        [
            ("49 31 N", "5 30 W"),
            ("49 32 N", "5 30 W"),
            ("49 33 N", "5 30 W"),
            ("49 33.5 N", "5 30 W"),
        ]
    ):
        ships.append(
            put(
                w,
                "merchant brig",
                "britain",
                f"{lat} {lon}",
                "bound for Falmouth",
                "bound for Falmouth",
                name=f"B{i}",
            )
        )
    w.run(61)
    crewed = [v.id for v in ships if v.crew is not None]
    assert len(crewed) == K.CREWED_CAP and crewed == [v.id for v in ships[:3]]
    assert ships[3].crew is None
    # the farthest within the range is in dealings with the player: she takes the place
    # of the farthest crewed ship that is not
    ships[3].dealing_tick = w.clock.tick
    w.run(60)
    assert ships[3].crew is not None and ships[2].crew is None
    assert len(w.vessels.crewed_ids) == K.CREWED_CAP
    # a vessel at anchor or in port is not promoted, and a crewed one that anchors is demoted
    from freesail.world import brains as B

    B.resolve_state(ships[2], "at anchor", ships[2].brain)
    ships[2].brain.state = "at anchor"
    B.resolve_state(ships[0], "at anchor", ships[0].brain)
    ships[0].crew.captain._enter("at anchor")
    w.run(60)
    assert ships[0].crew is None and ships[2].crew is None


def test_a_checkpoint_carries_a_crewed_ship_and_ticks_on_alike(tmp_path):
    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(300)
    assert b.crew is not None
    path = replay_mod.write_checkpoint(w, tmp_path / "crewed.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    cb = c.vessels.get(b.id)
    assert cb.crew is not None and isinstance(cb.crew, K.CrewedWorld)
    assert cb.crew.chart is c.chart and cb.crew.parent is c
    c.run(300)
    w.run(300)
    assert c.log.digest() == w.log.digest()
    assert cb.crew.log.digest() == b.crew.log.digest()
    assert cb.position == b.position


def test_truth_87_the_brig_promoted_sails_near_the_track_her_polar_gave_her():
    """Truth 87: a brig promoted within the range sails the same track at full detail as
    her polar gave her at far detail, within the stated tolerance (a mile over an hour on
    a reach: the polar is her file's own physics balanced at each point, within half a
    knot of the ship sailed), and demotes to the same plan."""
    w = hove_to_world()
    far = put(
        w,
        "merchant brig",
        "britain",
        "49 10 N 5 30 W",
        "bound for 49 10 N 4 30 W",
        "bound for 49 10 N 4 30 W",
        name="Far",
    )
    near = put(
        w,
        "merchant brig",
        "britain",
        "49 33 N 5 30 W",
        "bound for 49 33 N 4 30 W",
        "bound for 49 33 N 4 30 W",
        name="Near",
    )
    plan_before = list(near.plan)
    w.run(3600 + 61)
    assert near.crew is not None and far.crew is None
    east_far = far.position.lon_deg - (-5.5)
    east_near = near.position.lon_deg - (-5.5)
    # both stood east on a westerly: the crewed brig's easting over the hour within a
    # mile of the far body's
    miles_far = east_far * 60.0 * 0.65
    miles_near = east_near * 60.0 * 0.65
    assert abs(miles_near - miles_far) <= 1.5, (miles_near, miles_far)
    K.demote(w, near)
    assert near.crew is None and [leg[0] for leg in near.plan] == [leg[0] for leg in plan_before]


@pytest.mark.pace
def test_truth_88_with_the_cap_full_the_pace_holds():
    """Truth 88: the frigate with the cap full (three crewed ships beside her) ticks at
    not less than `CREWED_FLOOR_TICKS_S` a second on the build machine, the sixty times
    the owner plays at (measured about 140 quiet; docs/dev/TuningNotes.md, package 43)."""
    w = hove_to_world()
    for i, lat in enumerate(("49 31 N", "49 32 N", "49 33 N")):
        put(
            w,
            "merchant brig",
            "britain",
            f"{lat} 5 30 W",
            "bound for Falmouth",
            "bound for Falmouth",
            name=f"B{i}",
        )
    w.run(1000)
    assert len(w.vessels.crewed_ids) == K.CREWED_CAP
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"
