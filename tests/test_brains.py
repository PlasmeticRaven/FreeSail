"""The brain on the far body (package 43; spec M6 §4 "one brain, two bodies", §19): a
far-detail vessel given an intent carries a rules-based captain who perceives from her
own truth at the roll-up's cadence, runs the doctrine of her role and resolves every
state into a plan of the far body; the cruiser's doctrine; the far-detail guard; the
world order's intent clause; the hail between captains."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import brains as B
from freesail.world import captains as C
from freesail.world.geo import Position, bearing_and_distance, destination
from freesail.world.ships import Vessel, vessel_from_spec

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


def world_at(lat: float, lon: float, ship: str = FRIGATE, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        **kw,
    )
    return make_world(7, ship, sc)


def put(world, description, nation, position, goal, intent="", colours="shown", name="X"):
    world.vessels.serial += 1
    spec = {
        "description": description,
        "name": name,
        "nation": nation,
        "position": position,
        "goal": goal,
        "colours": colours,
    }
    if intent:
        spec["intent"] = intent
    v = vessel_from_spec(world, spec, world.vessels.serial)
    world.vessels.add(v)
    return v


# -- the doctrine by description, the perception from her truth ---------------------------


def test_the_role_is_by_her_description_and_her_intent():
    w = world_at(49.5, -5.5)
    v = Vessel("x", "X", "a brig", "data/ships/brig.yaml", "france", Position(49.4, -5.4))
    v.description = "brig-sloop"
    passage = C.read_intent(w, "bound for Brest")
    station = C.read_intent(w, "keep the station off Ushant within 15 miles")
    letter = C.read_intent(w, "carry this letter to Brest")
    assert B.role_of_vessel(v, passage) == "cruiser"
    assert B.role_of_vessel(v, letter) == "packet"
    v.description = "frigate"
    assert B.role_of_vessel(v, passage) == "kings-ship"
    v.description = "merchant brig"
    assert B.role_of_vessel(v, passage) == "merchant"
    assert B.role_of_vessel(v, station) == "kings-ship"
    v.description = "cutter"
    assert B.role_of_vessel(v, station) == "cruiser"
    assert B.role_of_vessel(v, passage) == "merchant"
    d = C.load_doctrine("cruiser")
    assert "cruiser" in C.ROLES and d.threshold("investigate_nm") == 10
    assert any(t.on == "overmatched" and t.to == "evading" for t in d.transitions)
    assert all(t.on in C.STIMULI for t in d.transitions)


def test_the_perception_is_from_her_own_truth_and_sees_the_player_by_the_horizon():
    """The ships in sight from her masthead by the horizon her rig's height and the
    other's give, within the player's visibility, by day; the player's ship among them
    under `PLAYER_ID`, her colours made out within two miles as any sail's; the land and
    the sea room by the chart from where she is; nothing of the player's account."""
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.run(120)
    near = put(w, "merchant brig", "france", "49 31 N 5 30 W", "bound for Brest", "bound for Brest")
    far = put(
        w,
        "merchant brig",
        "france",
        "48 40 N 5 30 W",
        "bound for Brest",
        "bound for Brest",
        name="Y",
    )
    w.run(60)
    p = B.perceive_vessel(w, near, near.brain)
    assert p.wind_kn == pytest.approx(14.0, abs=1.5)
    assert p.wind_from_deg == pytest.approx(270.0, abs=5)
    assert p.heading_deg == pytest.approx(near.heading_deg)
    ids = {s["id"] for s in p.strangers}
    assert B.PLAYER_ID in ids
    ship = next(s for s in p.strangers if s["id"] == B.PLAYER_ID)
    _, d = bearing_and_distance(near.position, w.position)
    assert ship["estimate_m"] == pytest.approx(d, abs=2)
    assert ship["made_out"] >= 2 and ship["nation"] == "britain" and ship["size"] == 3
    assert "frigate" in ship["known"] or "ship" in ship["known"]
    assert p.own_size == 2 and p.coast_by_account_nm is not None
    # fifty miles off, beyond any horizon: nothing in sight of the player, and the player
    # is nothing to her
    q = B.perceive_vessel(w, far, far.brain)
    assert B.PLAYER_ID not in {s["id"] for s in q.strangers}
    # a sail in sight of her is made out at the lookout's distances by eye: the brig
    # twenty miles from the frigate is a sail and no more
    assert "Y" not in ids or all(s["made_out"] == 0 for s in p.strangers if s["id"] == far.id)


# -- the states resolved into plans -----------------------------------------------------


def test_every_state_resolves_into_a_plan_with_a_brain_and_two_without():
    w = world_at(49.5, -5.5)
    v = put(w, "merchant brig", "britain", "49 30 N 5 40 W", "bound for the Lizard")
    plan = list(v.plan)
    for state in ("chasing", "evading", "keeping station", "investigating a stranger"):
        assert B.resolve_state(v, state) is False and v.state == "on passage"
    assert B.resolve_state(v, "hove to for weather") is True and v.plan[0][0] == "lie_to"
    assert B.resolve_state(v, "on passage") is True and v.plan == plan
    b = put(w, "brig-sloop", "france", "49 40 N 5 40 W", "bound for Brest", "bound for Brest")
    brain = b.brain
    assert brain is not None and brain.role == "cruiser" and b.plan and b.plan[0][0] == "to"
    first = list(b.plan)
    brain._stranger = B.PLAYER_ID
    assert B.resolve_state(b, "investigating a stranger", brain) and b.plan == [
        ("chase", B.PLAYER_ID, B.HAIL_REACH_M)
    ]
    assert b.saved_plan == first
    assert B.resolve_state(b, "chasing", brain) and b.plan[0][0] == "chase"
    assert B.resolve_state(b, "evading", brain) and b.plan == [("away", B.PLAYER_ID)]
    assert B.resolve_state(b, "hove to for weather", brain) and b.plan[0][0] == "lie_to"
    assert B.resolve_state(b, "at anchor", brain) and b.plan == [("anchor", "")]
    # no open road within the doctrine's reach of her: she lies to; a merchant brig off
    # the Lizard runs for Falmouth's outer road and the anchor
    assert B.resolve_state(b, "running for shelter", brain) and b.plan[0][0] == "lie_to"
    m = put(
        w,
        "merchant brig",
        "britain",
        "49 50 N 5 10 W",
        "bound for Brest",
        "bound for Brest",
        name="M",
    )
    assert B.resolve_state(m, "running for shelter", m.brain)
    assert m.plan[0][0] == "to" and m.plan[-1] == ("anchor", "falmouth")
    assert B.resolve_state(b, "on passage", brain) and b.plan == first and b.saved_plan is None
    k = put(
        w,
        "frigate",
        "britain",
        "48 40 N 5 40 W",
        "patrolling off Ushant within 15 miles",
        "keep the station off Ushant within 15 miles",
        name="K",
    )
    assert k.brain.role == "kings-ship"
    assert B.resolve_state(k, "keeping station", k.brain) and len(k.plan) == 4 and k.cycle
    with pytest.raises(ValueError):
        B.resolve_state(b, "fishing", brain)


def test_the_body_moves_by_the_brains_plan_a_chase_closes_and_a_flight_opens(far_only):
    """A chase leg steers to intercept the stranger and stops within hail; an away leg
    steers the reciprocal of her bearing; at anchor she rides head to wind with no way."""
    w = world_at(49.5, -5.5)
    b = put(w, "brig-sloop", "france", "49 30 N 5 40 W", "bound for Brest", "bound for Brest")
    _, d0 = bearing_and_distance(b.position, w.position)
    b.brain._stranger = B.PLAYER_ID
    B.resolve_state(b, "chasing", b.brain)
    for _ in range(30):
        b.tick(w, 60.0)
    _, d1 = bearing_and_distance(b.position, w.position)
    assert d1 < d0 - 2 * units.NAUTICAL_MILE
    B.resolve_state(b, "evading", b.brain)
    for _ in range(30):
        b.tick(w, 60.0)
    _, d2 = bearing_and_distance(b.position, w.position)
    assert d2 > d1 + units.NAUTICAL_MILE
    B.resolve_state(b, "at anchor", b.brain)
    p = b.position
    b.tick(w, 60.0)
    assert b.position == p and b.speed_kn == 0.0 and b.sail_state == "at anchor"
    assert b.course_words() == "at anchor"


# -- the two captains judge one another --------------------------------------------------


@pytest.fixture
def far_only(monkeypatch):
    """The far brain alone: no crewed promotion within the range (package 43, `crews`),
    so that the brain's own judgement is what the test reads."""
    from freesail.world import crews

    monkeypatch.setattr(crews, "CREWED_CAP", 0)


def test_a_cruiser_makes_out_the_frigate_an_enemy_of_a_bigger_class_and_hauls_off(far_only):
    """The cruiser's doctrine: a stranger within ten miles is closed (investigating); the
    frigate's colours made out, an enemy of a bigger class within two leagues, she is
    `overmatched` and evades; lost to sight she goes on passage. Her history is the
    record; the player's log has only what the lookout sees of her."""
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    b = put(
        w,
        "brig-sloop",
        "france",
        "49 36 N 5 30 W",
        "bound for Brest",
        "bound for Brest",
        colours="none",
        name="Palinure",
    )
    w.run(600)
    states = [s for _, s in b.brain.history]
    assert states[:2] == ["on passage", "investigating a stranger"]
    for _ in range(60):
        w.run(60)
        if "evading" in states:
            break
        states = [s for _, s in b.brain.history]
    assert "evading" in states and b.plan[0] == ("away", B.PLAYER_ID)
    assert not [e for e in w.log if "evading" in e.text and e.kind == "captain.state"]
    assert w.vessels.to_dict()[0]["brain"]["state"] == "evading"


def test_a_cruiser_chases_a_merchant_she_can_fight_and_speaks_her_within_hail(far_only):
    """Two vessels: the French brig-sloop closes the British schooner (a smaller class,
    an enemy once her colours are made out), chases her to hailing distance and speaks
    her; the merchant hauls off meanwhile; spoken, both go on their way, and the line
    says so when the player's lookout has them in sight."""
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    s = put(
        w,
        "schooner",
        "britain",
        "49 45 N 5 35 W",
        "bound for Falmouth",
        "bound for Falmouth",
        name="Betsey",
    )
    b = put(
        w,
        "brig-sloop",
        "france",
        "49 43 N 5 39 W",
        "bound for Brest",
        "bound for Brest",
        name="Renard",
    )
    # the schooner stripped of her way, so that the brig comes up with her
    s.sailing_factor = 0.1
    spoken = False
    for _ in range(14 * 6):
        w.run(600)
        if b.id in s.brain._spoken and s.id in b.brain._spoken:
            spoken = True
            break
    assert spoken
    bs = [st for _, st in b.brain.history]
    ss = [st for _, st in s.brain.history]
    assert "chasing" in bs and bs[-1] == "on passage"
    assert "evading" in ss
    assert [e for e in w.log if e.kind == "sail.spoke"] or not any(
        f"sail:{x}" in getattr(w.lookout, "_sails_seen", {}) for x in (b.id, s.id)
    )


# -- the far-detail guard, the scenario and the world order ------------------------------


def test_the_guard_refuses_a_captains_plan_across_the_land_and_warns_of_a_goals_leg():
    w = world_at(49.5, -5.5)
    # a goal's straight leg across the Lizard: a warning on the vessel, no refusal, no line
    v = put(w, "merchant brig", "britain", "49 55 N 5 20 W", "bound for Falmouth")
    assert "crosses the land" in v.warning
    assert not [e for e in w.log if "crosses the land" in e.text]
    from freesail.world.scenarios import guard_lines

    assert any("crosses the land" in ln for ln in guard_lines(w))
    # a captain's plan is the planner's, round the headlands: no warning, no refusal
    c = put(
        w, "merchant brig", "britain", "49 55 N 5 20 W", "bound for Falmouth", "bound for Falmouth"
    )
    assert not c.warning and c.brain is not None and len(c.plan) >= 2
    # an intent no captain knows is refused in words
    with pytest.raises(ValueError, match="no intent a captain knows"):
        put(w, "merchant brig", "britain", "49 20 N 5 20 W", "bound for Falmouth", "fish the Wolf")


def test_the_ship_world_order_takes_an_intent_and_gives_a_brain_to_a_ship_on_the_sea():
    w = world_at(49.5, -5.5)
    e = w.world_order(
        'ship: a brig-sloop "Palinure" of France at 49 20 N 5 40 W, bound for Brest, no '
        "colours, intent: run home to Brest"
    )
    assert e.data["result"] == "done" and "her captain's intent run home to Brest" in e.text
    v = w.vessels.find("Palinure")
    assert v is not None and v.brain is not None and v.brain.role == "cruiser"
    assert not v.shows_colours and v.intent_words == "run home to Brest"
    e2 = w.world_order(
        'ship: a merchant brig "Nancy" of Britain at 49 25 N 5 40 W, bound for Falmouth, '
        "intent bound for Falmouth, no colours"
    )
    assert e2.data["result"] == "done" and w.vessels.find("Nancy").brain is not None
    e3 = w.world_order('ship: a cutter "Lark" of Britain at 49 28 N 5 40 W, bound for Falmouth')
    assert e3.data["result"] == "done" and w.vessels.find("Lark").brain is None
    e4 = w.world_order('ship "Lark": intent carry this letter to Plymouth')
    assert e4.data["result"] == "done" and w.vessels.find("Lark").brain.role == "packet"
    e5 = w.world_order('ship "Lark": intent fish the Wolf')
    assert e5.data["result"] == "refused"
    # the save carries the brains' intents, and a replay gives them again
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    w.run(600)
    copy = replay_mod.replay(w.save(), ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.vessels.find("Lark").brain.to_dict() == w.vessels.find("Lark").brain.to_dict()


def test_a_station_intent_at_far_detail_keeps_the_station_off_the_place_to_seaward(far_only):
    w = world_at(49.5, -5.5)
    k = put(
        w,
        "frigate",
        "britain",
        "48 33 N 5 27 W",
        "patrolling off Ushant within 15 miles",
        "keep the station off Ushant within 15 miles",
        name="Diamond",
    )
    w.run(600)
    assert [s for _, s in k.brain.history] == ["keeping station"]
    mark = C.station_off(w, w.chart.find_feature("Ushant").position, 15.0)
    assert all(
        bearing_and_distance(mark, leg[1])[1] <= 15.0 * units.NAUTICAL_MILE + 1.0 for leg in k.plan
    )
    _ = destination
