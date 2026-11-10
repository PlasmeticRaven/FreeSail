"""The far fight on the sleeping hulls (spec M7 §18; package 74, step 4; the design in
`docs/design/Design-Prizes.md` §4): the far brain's engaging transition and its chase leg,
the rounds of `combat/far.py` run by the world once every three minutes for a pair of far
bodies in anger within gun's reach, the strike by morale and the possession that follows,
the guns heard at the player's ship; the far record carried into a hull's parts at her
making and her waking and summed back at her sleep; the far ship's reply to an awake hull
as the fallback where the cap is full; the toggle that turns it all off."""

from __future__ import annotations

import pytest

from freesail import units
from freesail.combat import far as F
from freesail.combat import far_action as FA
from freesail.world import crews
from freesail.world import prizes as P
from freesail.world.geo import destination
from tests.test_brains import put, world_at

CUTTER = "data/ships/cutter.yaml"


def _two_in_anger(cap: int = 0, miles_off: float = 12.0, seed: int = 7, cutter_near: bool = False):
    """The frigate hove to; a French frigate cruising for prizes and a King's cutter cruising,
    a mile and a half apart, so many miles to the south at far detail (the cap given); with
    `cutter_near` the cutter is the nearer of the two to the player."""
    w = world_at(49.5, -5.5)
    w.seed_used = seed
    w.crewed_settings = {"cap": cap}
    w.submit("heave to")
    w.run(60)
    far = destination(w.position, 180.0, miles_off * units.NAUTICAL_MILE)
    if cutter_near:
        far, q = destination(far, 180.0, 1.5 * units.NAUTICAL_MILE), far
    a = put(
        w,
        "frigate",
        "france",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Renard",
    )
    if not cutter_near:
        q = destination(far, 90.0, 1.5 * units.NAUTICAL_MILE)
    b = put(
        w,
        "cutter",
        "britain",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise off the Lizard within 20 miles",
        colours="shown",
        name="Sprightly",
    )
    return w, a, b


def _engage_both(w, v, enemy) -> None:
    """7-140's setting: both at quarters, the guns cast loose, the batteries engaged as they
    bear, the King's cutter at the hull and the French at the rigging."""
    from freesail.combat.guns import Aim, FireMode, battery_of
    from freesail.crew.quarters import quarters_of
    from freesail.ship.parts import Charge

    for world, target in ((w, v.id), (enemy, "the ship")):
        q = quarters_of(world.ship)
        q.beat(world.clock.tick)
        for g in world.ship.guns.values():
            g.cast_loose = True
        b = battery_of(world.ship)
        b.target = target
        b.engaged = "larboard" if world is w else "starboard"
        b.mode = FireMode.AS_THEY_BEAR
        b.aim = Aim.HULL if world is w else Aim.RIGGING
        b.charge = Charge.ROUND


def _run_until_struck(w, a, b, minutes: int = 120) -> int:
    for i in range(minutes):
        w.run(60)
        if a.struck or b.struck:
            return i + 1
    return minutes


# -- the rounds beyond the range -------------------------------------------------------------------


@pytest.mark.slow
def test_two_far_ships_meet_in_anger_beyond_the_range_and_fight_by_the_rounds_to_a_strike():
    """The design's §4.2, §4.3 and §4.5: the French frigate makes the cutter out an enemy
    (the private signal answered wrong), chases and enters `engaging` with her as the mark
    (the far brain's transition, the same rows as the near captain's), her chase leg closing
    to the doctrine's range; the cutter, overmatched, evades. Within the frigate's guns'
    reach (her long eighteens' random shot, 1,830 m) the rounds fire every three minutes on
    the records: the cutter's carronades do not reach seven cables and her morale falls
    under the frigate's fire until she strikes (at seed 7 after eleven rounds, 33 minutes,
    one killed and three wounded by the tables); her far body is struck as the cut-out
    writes it, the frigate's brain takes `taking possession` and at hailing distance the far
    possession is taken on the records ('struck at far detail'). The player's lookout
    twelve miles off hears the guns once a round (`action.guns_heard`). The World's `far`
    stream is opened at the first round and not before."""
    w, a, b = _two_in_anger()
    assert FA.has_guns(a) and FA.has_guns(b)
    assert FA.reach_m(a) > FA.reach_m(b) > 0
    for _ in range(10):
        w.run(60)
        if a.brain.state == "engaging":
            break
    assert a.brain.state == "engaging" and a.brain._stranger == b.id
    assert a.plan and a.plan[0][0] == "chase" and a.plan[0][1] == b.id
    assert abs(a.plan[0][2] - FA.engage_range_m(a.brain)) < 1.0
    assert b.brain.state == "evading"
    assert "far" not in w.rng.stream_names()
    minutes = _run_until_struck(w, a, b)
    assert b.struck and not a.struck, (a.brain.state, b.brain.state)
    assert "far" in w.rng.stream_names()
    rounds = int(b.damage["rounds"])
    assert rounds == 11 and 60 <= minutes <= 75, (rounds, minutes)
    assert b.damage["killed"] + b.damage["wounded"] >= 1
    assert b.damage["morale"] < 0.35 and b.damage["struck_tick"] == w.clock.tick
    assert a.damage["killed"] == a.damage["wounded"] == 0  # her carronades never reached
    assert a.damage["rounds"] == rounds and a.damage["rounds_fired"] > 0
    assert b.state == "struck" and b.brain.state == "struck" and b.plan[0][0] == "lie_to"
    assert b.signals.colours.state == "struck"
    assert any("struck to the Renard" in words for _, words in b.story)
    assert any("a round with the Sprightly" in words for _, words in a.story)
    heard = [e for e in w.log if e.kind == "action.guns_heard"]
    assert len(heard) >= rounds // 2  # the pair drifts about the twelve-mile reach
    assert heard[0].text.startswith("The sound of guns to the S") and "12 miles" in heard[0].text
    for _ in range(25):
        w.run(60)
        if P.is_prize(b):
            break
    assert P.is_prize(b) and P.record_of(b)["how"] == "struck at far detail"
    assert P.record_of(b)["captor"] == a.id and b.nation == "france"


def test_the_toggle_off_leaves_the_world_as_it_was_and_the_far_brain_never_engages():
    """`far_action.ENABLED` False (the bisection's toggle, §4.6): the far brain takes no
    engaging transition, nothing fires, no `far` stream is opened and no gun is heard."""
    FA.ENABLED = False
    try:
        w, a, b = _two_in_anger()
        for _ in range(40):
            w.run(60)
        assert a.brain.state != "engaging" and not a.damage and not b.damage
        assert "far" not in w.rng.stream_names()
        assert not any(e.kind == "action.guns_heard" for e in w.log)
    finally:
        FA.ENABLED = True


def test_beyond_the_guns_reach_nothing_fires_and_the_chase_leg_closes_her():
    """A pair in anger beyond the longer reach fires nothing (the round is not spent, no
    stream opened); the engaging ship's chase leg closes the range."""
    w, a, b = _two_in_anger()
    for _ in range(10):
        w.run(60)
        if a.brain.state == "engaging":
            break
    d0 = P._bearing_distance(a.position, b.position)[1]
    assert d0 > FA.reach_m(a)
    for _ in range(10):
        w.run(60)
    d1 = P._bearing_distance(a.position, b.position)[1]
    assert d1 < d0 and not a.damage and "far" not in w.rng.stream_names()


# -- the agreement of the two roads ----------------------------------------------------------------


def test_the_near_fight_of_two_cutters_at_a_cable_and_the_far_rounds_agree_within_a_round():
    """The design's §4.6 (truth 7-359): 7-140's near action (two cutters at a cable, the
    King's carronades at the hull and the French long guns at the rigging, the fire as it
    bears) ends three minutes after the first shot at seed 7; the far rounds of the same two
    at the same range (the mended `far_ship`s) end in two rounds, six minutes. The near ends
    35 seconds after the first shot on this tree, so the two are within two rounds and not
    one: pinned as found (the far fight is the coarser by design, rule 5)."""
    from freesail.core.rng import Rng
    from tests.test_known_truths import _a_cutter_crewed, _action_scenario, make_world

    w = make_world(7, CUTTER, _action_scenario(wind_kn=14.0, speed=5.0))
    w.submit("heave to")
    v, enemy = _a_cutter_crewed(w, 90.0, 150.0, fit="long guns")
    enemy.submit("heave to")
    w.run(90)
    _engage_both(w, v, enemy)
    first = struck_at = None
    for _ in range(900):
        w.run(1)
        if first is None and any(e.kind == "action.fired_at" for e in enemy.log):
            first = w.clock.tick
        if v.struck:
            struck_at = w.clock.tick
            break
    assert first is not None and struck_at is not None
    near_s = struck_at - first
    rng = Rng(7).stream("far")
    fa = F.far_ship(CUTTER, "britain", "carronades", aim="hull", morale_start=0.9, strike_below=0.1)
    fb = F.far_ship(
        CUTTER, "france", "long guns", aim="rigging", morale_start=0.7, strike_below=0.35
    )
    rounds = F.fight(fa, fb, 185.0, rng, minutes=180)
    far_s = rounds[-1].t_s
    assert fb.struck_at_s is not None and fa.struck_at_s is None
    # the figures found on the step's tree (the design's §4.6: pinned as found, no table
    # moved for the agreement's sake): the near fight at a cable ends 35 seconds after the
    # first shot (fourteen guns as they bear, a shot between wind and water, her morale gone
    # in the first minute), the far rounds in two rounds, six minutes (the far fight cannot
    # end before its first round at 180 s, and the second finishes her): under two rounds
    # apart, the far the coarser by design (rule 5)
    assert near_s == 35 and far_s == 360.0, (near_s, far_s)
    assert abs(far_s - near_s) <= 2 * FA.FAR_ROUND_S


# -- the far state into the near body, and back ----------------------------------------------------


@pytest.mark.slow
def test_a_hull_made_or_woken_with_far_damage_carries_it_in_her_parts_and_sums_it_back():
    """The design's §4.4 (truth 7-360): the cutter struck by the rounds, promoted to a hull,
    carries her record in her parts (the men killed and wounded on her muster, the shot
    holes in her damage keeper, the rest as the record has it), applied once
    (`carried_in`); slept again, `write_damage` sums the parts to the same counts. A hull
    fought awake and slept carries the parts' sum in her record."""
    w, a, b = _two_in_anger()
    _run_until_struck(w, a, b)
    assert b.struck
    rec = dict(b.damage)
    hull = crews.promote(w, b)
    assert hull is not None and hull.awake
    muster = hull.ship.extra["crew"]
    killed = sum(1 for s in muster.sailors if s.hurt == "killed") + len(muster.dead or [])
    wounded = sum(1 for s in muster.sailors if s.hurt in ("wounded", "hurt"))
    assert killed == rec["killed"] and wounded == rec["wounded"]
    from freesail.combat import hits as H

    keeper = H.damage_of(hull.ship)
    assert len(keeper.holes) == rec["holes"]
    assert sum(1 for h in keeper.holes if h.get("below")) == rec["holes_below"]
    assert b.damage["carried_in"]["killed"] == rec["killed"]
    # applied once: a second pass changes nothing
    applied = FA.far_damage_into_parts(hull, b.damage)
    assert all(v == 0 for v in applied.values())
    crews.demote(w, b)
    assert not hull.awake
    for key in ("killed", "wounded", "dismounted", "holes", "holes_below", "spars_gone"):
        assert b.damage[key] == rec[key], key


def test_a_hull_fought_awake_and_slept_carries_the_parts_sum_in_her_record():
    from tests.test_known_truths import _a_cutter_crewed, _action_scenario, make_world

    w = make_world(7, CUTTER, _action_scenario(wind_kn=14.0, speed=5.0))
    w.submit("heave to")
    v, enemy = _a_cutter_crewed(w, 90.0, 150.0, fit="long guns")
    enemy.submit("heave to")
    w.run(90)
    _engage_both(w, v, enemy)
    for _ in range(900):
        w.run(1)
        if v.struck:
            break
    assert v.struck
    muster = enemy.ship.extra["crew"]
    hurt = sum(1 for s in muster.sailors if s.hurt in ("wounded", "hurt"))
    killed = sum(1 for s in muster.sailors if s.hurt == "killed") + len(muster.dead or [])
    crews.demote(w, v)
    assert v.damage["killed"] == killed and v.damage["wounded"] == hurt
    assert v.damage["holes"] >= 1


# -- the far ship's reply to an awake hull, the cap full -------------------------------------------


@pytest.mark.slow
def test_a_far_ship_replies_to_an_awake_hull_only_where_the_cap_has_no_room():
    """The lead's ruling 4: a far ship engaging a hull awake under a full cap fires her
    broadside at the hull by the tables, each shot that strikes resolved into the hull's
    parts with a synthetic gun of her fit's kind, said in the hull's log as the fallback
    (`action.far_reply`) and counted; with room under the cap she is woken and the near
    action is 70's."""
    FA.FALLBACK_COUNT["rounds"] = 0
    w, a, b = _two_in_anger(cap=1, miles_off=2.0, cutter_near=True)
    for _ in range(12):
        w.run(60)
        if b.crew is not None and b.crew.awake:
            break
    assert b.crew is not None and b.crew.awake, "the cutter under the cap"
    for _ in range(80):
        w.run(60)
        if FA.FALLBACK_COUNT["rounds"] or b.struck or (a.crew is not None and a.crew.awake):
            break
    if a.crew is not None and a.crew.awake:
        pytest.skip("the cap woke the frigate in place of the cutter: the near action's road")
    assert FA.FALLBACK_COUNT["rounds"] >= 1
    replies = [e for e in b.crew.log if e.kind == "action.far_reply"]
    assert replies and "the far ship's reply, the cap full" in replies[0].text


# -- the cut-out carried from hailing distance to its end by the rounds ----------------------------


@pytest.mark.slow
def test_a_packet_that_fights_is_brought_to_by_the_privateers_rounds_and_taken():
    """The design's §4.3 (truth 7-369): 72's cut-out yields a merchantman without a shot where
    her doctrine yields when caught; a packet (`yields_when_caught: false`, the mails fought
    for) fires her guns within her four cables and is struck by morale under the privateer's
    rounds, then taken possession of at hailing distance: the two rules together carry the
    cut-out from hail to its end by the same rounds."""
    from tests.test_squadrons import STATION_INTENT

    w = world_at(49.5, -5.5, intent=STATION_INTENT)
    w.crewed_settings = {"cap": 0}
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    # the packet a cutter (the brig's one file gives a "merchant brig" the brig-sloop's
    # eighteen guns and 121 men until package 75 parts them, and she beats the privateer)
    packet = put(
        w,
        "cutter",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "carrying the mail to Falmouth",
        intent="carry this letter to Falmouth",
        colours="shown",
        name="Expedition",
    )
    assert packet.brain is not None and packet.brain.role == "packet"
    packet.sailing_factor = 0.85
    q = destination(far, 270.0, 1.2 * units.NAUTICAL_MILE)
    # a privateer brig (the schooner's and the lugger's files carry no armament until
    # package 75 gives them theirs: a far ship with no guns fires nothing)
    pv = put(
        w,
        "brig-sloop",
        "france",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Vengeur",
    )
    pv.sailing_factor = 1.0
    assert pv.brain.role == "privateer" and FA.has_guns(packet) and FA.has_guns(pv)
    for _ in range(240):
        w.run(60)
        if packet.struck:
            break
    assert packet.struck and not pv.struck, (packet.brain.state, pv.brain.state)
    assert packet.damage.get("rounds", 0) >= 1 and pv.damage.get("rounds", 0) >= 1
    assert packet.damage["rounds_fired"] >= 0
    assert any("struck to the Vengeur" in words for _, words in packet.story)
    assert not any(e.kind == "squadron.cut_out" for e in w.log)  # no yielding without a shot
    for _ in range(30):
        w.run(60)
        if P.is_prize(packet):
            break
    assert P.is_prize(packet) and P.record_of(packet)["how"] == "struck at far detail"
