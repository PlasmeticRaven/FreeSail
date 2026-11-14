"""The far fight on the sleeping hulls (spec M7 §18; package 74, step 4; the design in
`docs/design/Design-Prizes.md` §4): the far brain's engaging transition and its chase leg,
the rounds of `combat/far.py` run by the world once every three minutes for a pair of far
bodies in anger within gun's reach, the strike by morale and the possession that follows,
the guns heard at the player's ship; the far record carried into a hull's parts at her
making and her waking and summed back at her sleep; the far ship's reply to an awake hull
as the fallback where the cap is full; the toggle that turns it all off."""

from __future__ import annotations

import math

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


# -- a far ship of war engaging from her passage (package 75, truth 7-231) -------------------------


def _two_on_passage():
    """Two far King's ships of war on their passages, neither chasing first (package 75, the
    lead's ruling (2) of 2026-11-13): tests/test_brains.py's world at seed 7, the frigate hove
    to and the cap nought, and twelve miles south of her a French 74 bound for Brest and a
    British 74 bound for Falmouth a mile apart, each within the other's `engage_nm` (a mile)
    at her first judgement, so that each goes `engaging` from `on passage` with no mark in
    hand (the King's ship's row `{from: on passage, on: enemy in range, to: engaging}`)."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    q = destination(far, 90.0, 1.0 * units.NAUTICAL_MILE)
    a = put(
        w,
        "seventy-four",
        "france",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for Brest",
        intent="bound for Brest",
        colours="shown",
        name="Foudroyant",
    )
    b = put(
        w,
        "seventy-four",
        "britain",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        colours="shown",
        name="Hero",
    )
    return w, a, b


@pytest.mark.slow
def test_a_far_ship_of_war_engaging_from_her_passage_keeps_the_sea_and_closes_her_enemy():
    """Truth 7-231 (package 75; the lead's ruling (2) of 2026-11-13): a far ship of war that
    goes engaging from her passage takes the mark the stimulus read (`FarCaptain._engaging_mark`,
    as the near captain's `_mark`), keeps the sea and closes her enemy. Before the mend (package
    74's a4944b87) each of the two 74s, with no mark in hand, was given a chase of nobody, which
    the body dropped, and both were gone from the sea the next minute (tick 180) without a round.
    Now, at seed 7: both go `engaging` from `on passage` at their first judgement (tick 120), each
    with the other as her mark and a chase leg to her at her doctrine's engaging range (the
    French 4 cables, the British 2 by the nations' habits); both keep the sea every minute; the
    range closes every minute from 0.89 miles to under a fifth of a mile by tick 900 and is
    never opened; the far rounds fire every three minutes from the first judgement (both
    within the French long guns' reach) until the Hero strikes, at tick 1200 after seven rounds;
    the Foudroyant takes possession at hailing distance at the next judgement (tick 1260, "struck
    at far detail"), and both are on the sea at its end. **After the action** (the review's mends
    of the lead's notes of 12 and 13 November): each held her passage when she went engaging
    (`brains.PASSAGE_HELD`, the plan saved as a detour's is), and the Foudroyant, the prize taken,
    is on passage at the next judgement (tick 1320) with that plan again, and closes its first mark
    every minute of the half hour after, her prize in company. OLD BESIDE NEW: at f5102fae her
    passage was not taken up (`engaging` saved nothing, and `taking possession` saved the action's
    chase leg), and she was "on passage" chasing her prize at the engaging range for good."""
    from freesail.world import brains as B

    w, a, b = _two_on_passage()
    w.run(60)
    assert w.clock.tick == 120
    for v, other in ((a, b), (b, a)):
        assert v.brain.role == "kings-ship"
        assert v.brain.history == [(120, "on passage"), (120, "engaging")]
        assert v.brain._stranger == other.id
        assert v.plan == [("chase", other.id, FA.engage_range_m(v.brain))]
        assert v.brain._business.get(B.PASSAGE_HELD) is True
        assert v.saved_plan and all(leg[0] in ("to", "anchor") for leg in v.saved_plan)
    held = list(a.saved_plan)
    assert round(FA.engage_range_m(a.brain)) == 741 and round(FA.engage_range_m(b.brain)) == 370
    ranges: list[tuple[int, float]] = []
    while not b.struck and w.clock.tick < 3600:
        assert all(w.vessels.get(v.id) is v and not v.done for v in (a, b)), w.clock.tick
        nm = P._bearing_distance(a.position, b.position)[1] / units.NAUTICAL_MILE
        ranges.append((w.clock.tick, nm))
        w.run(60)
    assert 0.85 <= ranges[0][1] <= 0.9, ranges[0]
    closing = zip(ranges, ranges[1:], strict=False)
    assert all(later <= sooner for (_, sooner), (_, later) in closing), ranges
    assert max(nm for t, nm in ranges if t >= 900) < 0.2, ranges
    assert b.struck and not a.struck and w.clock.tick == 1200
    assert a.damage["rounds"] == b.damage["rounds"] == 7 and b.damage["struck_tick"] == 1200
    for _ in range(5):
        w.run(60)
        if P.is_prize(b):
            break
    assert P.is_prize(b) and w.clock.tick == 1260
    assert P.record_of(b)["captor"] == a.id and P.record_of(b)["how"] == "struck at far detail"
    assert a.brain.history[-1] == (1260, "taking possession")
    assert all(w.vessels.get(v.id) is v and not v.done for v in (a, b))
    assert a.saved_plan == held  # `taking possession` saved nothing over her passage
    w.run(60)
    assert a.brain.history[-1] == (1320, "on passage") and a.plan == held
    assert a.saved_plan is None and B.PASSAGE_HELD not in a.brain._business
    miles = []
    for _ in range(30):
        assert a.brain.state == "on passage" and a.plan[0] == held[0], w.clock.tick
        miles.append(P._bearing_distance(a.position, held[0][1])[1])
        w.run(60)
    assert all(later < sooner for sooner, later in zip(miles, miles[1:], strict=False)), miles
    assert P.is_prize(b) and b.brain.state == "in company"


@pytest.mark.parametrize("case", ["another-in-sight", "none-in-sight", "none-on-the-sea"])
def test_engaging_she_keeps_a_mark_in_hand_as_chasing_does_and_never_chases_nobody(case):
    """Truth 7-231's second half (the lead's ruling (2) of 2026-11-13: "keeps one in hand as
    chasing does when the mark is lost from sight"; `FarCaptain._take_mark`): the two 74s of
    `_two_on_passage` engaged (tick 180), the Hero is then hidden from every masthead
    (`seen_within_nm` nought) or gone from the sea. With a British frigate put a mile and a half
    from the Foudroyant, within her breaking-off distance, she takes the frigate for her mark at
    the next judgement and chases her, as chasing takes the nearest stranger; with none in
    sight she keeps the Hero in hand while the Hero is on the sea, her leg following her; with
    the Hero gone from the sea and none other, she lies to where she is (no chase of nobody,
    which the body would drop and take her from the sea with it), and `resolve_state` laying
    `engaging` with no mark and no enemy in sight lies her to as well. Hidden or gone, the
    action ends by `enemy out of range` ten minutes after the last judgement that saw an
    enemy (tick 840) and she is on passage, on the sea, with the passage she held when she went
    engaging (the review's mends of the lead's notes of 12 and 13 November; OLD BESIDE NEW: at
    f5102fae she was "on passage" lying to, or chasing the hidden Hero, for good)."""
    from freesail.world import brains as B

    w, a, b = _two_on_passage()
    w.run(120)
    assert a.brain.state == "engaging" and a.brain._stranger == b.id
    held = list(a.saved_plan)
    assert held and held[0][0] == "to" and a.brain._business.get(B.PASSAGE_HELD) is True
    engage = FA.engage_range_m(a.brain)
    c = None
    if case == "another-in-sight":
        b.seen_within_nm = 0.0
        r = destination(a.position, 0.0, 1.5 * units.NAUTICAL_MILE)
        c = put(
            w,
            "frigate",
            "britain",
            {"lat_deg": r.lat_deg, "lon_deg": r.lon_deg},
            "bound for Falmouth",
            intent="bound for Falmouth",
            colours="shown",
            name="Amethyst",
        )
    elif case == "none-in-sight":
        b.seen_within_nm = 0.0
    else:
        b.done = True
    w.run(60)
    assert a.brain.state == "engaging" and not a.done
    if case == "another-in-sight":
        assert a.brain._stranger == c.id and a.plan == [("chase", c.id, engage)]
    elif case == "none-in-sight":
        assert a.brain._stranger == b.id and a.plan == [("chase", b.id, engage)]
    else:
        assert a.brain._stranger is None and a.plan == [("lie_to", math.inf)]
        a.plan = [("to", a.position, "nowhere")]
        assert B.resolve_state(a, "engaging", a.brain)
        assert a.brain._stranger is None and a.plan == [("lie_to", math.inf)]
    for _ in range(10):
        w.run(60)
        assert w.vessels.get(a.id) is a and not a.done, w.clock.tick
    if case == "another-in-sight":
        assert a.brain.state == "engaging" and a.brain._stranger == c.id
        assert a.saved_plan == held
    else:
        assert a.brain.history[-1] == (840, "on passage"), a.brain.history
        assert a.plan == held and a.saved_plan is None
        assert B.PASSAGE_HELD not in a.brain._business


def test_package_74s_road_from_a_chase_keeps_the_mark_it_entered_with_as_it_did():
    """The review's mends of the lead's notes of 12 and 13 November: the mark kept in hand each
    minute and the passage held are the plan-state road's alone (`brains.PASSAGE_HELD`); package
    74's own road into an action, engaging from a detour with her mark in hand, is as it was at
    94bfac27. The two 74s of `_two_on_passage` each put chasing the other at tick 60, both engaging
    at 120 from `chasing` with the other in hand; the Hero then hidden from every masthead and a
    British frigate put a mile and a half from the Foudroyant, within her breaking-off distance:
    she keeps the Hero and the chase leg she entered with, minute after minute, and holds no
    passage. OLD BESIDE NEW: at f5102fae she took the frigate for her mark at tick 240."""
    from freesail.world import brains as B

    w, a, b = _two_on_passage()
    for v, other in ((a, b), (b, a)):
        v.brain._stranger = other.id
        v.brain._enter("chasing")
    w.run(120)
    assert a.brain.history[-2:] == [(60, "chasing"), (120, "engaging")]
    engage = FA.engage_range_m(a.brain)
    assert a.brain._stranger == b.id and a.plan == [("chase", b.id, engage)]
    assert B.PASSAGE_HELD not in a.brain._business
    b.seen_within_nm = 0.0
    r = destination(a.position, 0.0, 1.5 * units.NAUTICAL_MILE)
    put(
        w,
        "frigate",
        "britain",
        {"lat_deg": r.lat_deg, "lon_deg": r.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        colours="shown",
        name="Amethyst",
    )
    for _ in range(4):
        w.run(60)
        assert a.brain.state == "engaging", w.clock.tick
        assert a.brain._stranger == b.id and a.plan == [("chase", b.id, engage)], w.clock.tick
        assert B.PASSAGE_HELD not in a.brain._business


@pytest.mark.slow
def test_at_a_cap_of_nought_a_far_ship_engaging_the_players_ship_does_not_reply():
    """The lead's ruling of 2026-11-14, (F1): the reply at a cap of nought comes out of this hash
    (`far_action._fallback_reply` as it was before 2d2bbd8b). There it put her broadside into the
    player's parts every three minutes while his shot reached only `hits._far_hit`'s count, which
    nothing reads, so that the fight was one-sided and endless; a far body that fires on the
    player and one that can be hurt by him are one mend, package 77's, and go in together or not
    at all. The 64's case of `tests/test_bellerophon.py` (the player's 64 on her station off the
    Lizard, a French 74 bound for Brest a mile and a half north of her), the cap nought, at seed
    7: the 74 goes engaging from her passage at tick 360 with the 64 her mark, and in the half
    hour after no broadside of hers is said in the 64's log and none is counted. OLD BESIDE NEW:
    at 53c14457 her first broadside came at 360 ("The Foe fires her broadside at us from 9
    cables: none of her 63 shot strike us.") and again at 540; under a full cap the fallback is
    as it was (`test_a_far_ship_replies_to_an_awake_hull_only_where_the_cap_has_no_room`)."""
    from tests.test_brains import world_at

    FA.FALLBACK_COUNT["rounds"] = 0
    w = world_at(
        49.5,
        -5.5,
        "data/ships/sixty-four.yaml",
        intent="keep the station off the Lizard within 10 miles",
    )
    w.crewed_settings = {"cap": 0}
    w.run(60)
    foe = put(
        w,
        "seventy-four",
        "france",
        "49 31.5 N 5 30 W",
        "bound for Brest",
        "bound for Brest",
        "shown",
        "Foe",
    )
    for _ in range(8):
        w.run(60)
    assert foe.brain.history[-1] == (360, "engaging") and foe.brain._stranger == "the ship"
    for _ in range(30):
        w.run(60)
    assert not foe.done and foe.crew is None and foe.brain.state == "engaging"
    assert not [e for e in w.log if e.kind == "action.far_reply"]
    assert FA.FALLBACK_COUNT["rounds"] == 0


# -- a relation kept after the thing it stood on is gone (the lead's readings of cda12ec9) --------


def _three_on_passage():
    """Truth 7-231's world (`_two_on_passage`) with a second French 74 bound for Brest a third of
    a mile south of the first: two 74s on passage and one enemy (the lead's readings of cda12ec9,
    (F2))."""
    w, a, b = _two_on_passage()
    r = destination(a.position, 180.0, 0.33 * units.NAUTICAL_MILE)
    c = put(
        w,
        "seventy-four",
        "france",
        {"lat_deg": r.lat_deg, "lon_deg": r.lon_deg},
        "bound for Brest",
        intent="bound for Brest",
        colours="shown",
        name="Tonnant",
    )
    return w, a, c, b


def _until(w, stop, minutes):
    for _ in range(minutes):
        w.run(60)
        if stop():
            return True
    return False


@pytest.mark.slow
@pytest.mark.parametrize(
    "road", ["struck-to-the-other", "struck-to-nobody-known", "taken-and-gone"]
)
def test_the_second_of_two_ships_on_one_mark_gives_it_up_and_takes_her_passage_again(
    road, monkeypatch
):
    """The lead's readings of cda12ec9, (F2): "a ship whose mark is taken by another, struck to
    another or gone gives it up and takes her passage again (two 74s on passage and one enemy:
    the second must not stay 'taking possession' or chasing the other's prize)". The one answer
    (`relations.STRUCK`, asked by `_enemy_struck`, by `Judgement._prize_taken` for the books' row
    out of `taking possession`, and by `prizes.far_minute`). Two French 74s and the British Hero
    (`_three_on_passage`), seed 7: both French go engaging from their passages (the Foudroyant at
    120, the Tonnant at 300); the Hero strikes in the Tonnant's round at 840.

    - `struck-to-the-other`: the Hero struck to the Tonnant (`damage["struck_to"]`), the
      Foudroyant never goes taking possession; her action over (`enemy out of range`, ten minutes
      after her mark struck), she takes up the passage she held; the Tonnant possesses her.
    - `struck-to-nobody-known` (a strike with no taker named, as the near action's): both go
      taking possession; the first at hailing distance possesses; the other gives her up at her
      next judgement and takes her passage again.
    - `taken-and-gone`: the same, the prize then gone from the sea before the second reaches her.

    Each French ship is on passage with the plan she held at the end, and neither is in `taking
    possession`, nor chasing the prize, at any minute of the forty after the possession. OLD
    BESIDE NEW: at 53c14457 the second stayed `taking possession` of the other's prize for good,
    chasing her six thousand ticks later, her passage held."""
    from freesail.world import brains as B

    w, a, c, b = _three_on_passage()
    if road != "struck-to-the-other":
        strike = FA._strike

        def strike_unnamed(root, loser, winner, tick):
            strike(root, loser, winner, tick)
            loser.damage.pop("struck_to", None)

        monkeypatch.setattr(FA, "_strike", strike_unnamed)
    assert _until(w, lambda: b.struck, 40), (a.brain.state, c.brain.state)
    # to whom she struck, read at the strike: the strike's record ends with her colours given her
    # captor's (`prizes._set_colours`; the whole-change review of 80e703c7, engine-2), so that it
    # is read here and no longer after the possession, as it was at 80e703c7
    struck_to = b.damage.get("struck_to")
    held = {v.id: list(v.saved_plan or []) for v in (a, c)}
    assert all(held.values()) and all(v.brain._business.get(B.PASSAGE_HELD) for v in (a, c))
    assert _until(w, lambda: P.is_prize(b), 10)
    captor = w.vessels.get(P.record_of(b)["captor"])
    other = a if captor is c else c
    if road == "struck-to-the-other":
        assert struck_to and captor is w.vessels.get(struck_to)
        assert "struck_to" not in b.damage  # ended with the strike
        assert "taking possession" not in [s for _, s in other.brain.history]
    else:
        assert other.brain.state == "taking possession" and other.brain._stranger == b.id
        if road == "taken-and-gone":
            b.done = True
    for _ in range(40):
        w.run(60)
        for v in (a, c):
            assert v.brain.state != "taking possession", (w.clock.tick, v.name)
            assert not (v.plan and v.plan[0][0] == "chase" and v.plan[0][1] == b.id), v.name
    for v in (a, c):
        assert v.brain.state == "on passage" and v.plan == held[v.id], (v.name, v.plan[:1])
        assert v.saved_plan is None and B.PASSAGE_HELD not in v.brain._business


def _a_brig_cut_out():
    """A British frigate bound for Falmouth and a French merchant brig bound for Brest a third of
    a mile east of her, twelve miles south of the player's frigate hove to, the cap nought, seed 7:
    the frigate goes engaging from her passage at tick 120 with the brig her mark, and the brig,
    brought to with no help near, is cut out the same minute (`squadrons.far_captures`) and joins
    her captor's company as a prize."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    q = destination(far, 90.0, 0.3 * units.NAUTICAL_MILE)
    f = put(
        w,
        "frigate",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        colours="shown",
        name="Amethyst",
    )
    g = put(
        w,
        "merchant brig",
        "france",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "bound for Brest",
        intent="bound for Brest",
        colours="shown",
        name="Jeune Emilie",
    )
    return w, f, g


@pytest.mark.slow
def test_no_round_at_a_prize_and_the_captor_and_her_prize_keep_company():
    """The lead's readings of cda12ec9, (F3): "no round at a prize, a struck ship or her own side
    (`_pairs` and wherever a far round chooses its mark), and the captor and her prize keep
    company as the records say". The brig cut out at tick 120 (`_a_brig_cut_out`): the captor
    still `engaging` her that minute fires no round into her (`far_action._pairs` asks the one
    answer, `relations.MARK`), so that her prize is never struck again; her action over, the
    frigate takes her passage again (at 780), and her prize keeps her station in the captor's
    company (the set's pace counting its prize, `Squadron.pace_cap_kn`), within half a mile of
    her every minute of the four hours after the cut-out. OLD BESIDE NEW: at 53c14457 `_pairs`
    fired into the prize the minute she was made (five killed, eleven wounded), she "struck"
    again and lay to, and the frigate was on passage at 240 with her prize 1.9 miles astern by
    1200 and 6.4 by 3600; with the round alone mended, the prize kept her station leg but fell
    astern half a mile an hour (3.1 miles at 21,600), the set's pace leaving its prizes out."""
    w, f, g = _a_brig_cut_out()
    w.run(60)
    assert f.brain.history[-1] == (120, "engaging") and P.is_prize(g)
    assert P.record_of(g)["captor"] == f.id and P.record_of(g)["how"] == "cut out"
    assert not g.damage and not f.damage and "far" not in w.rng.stream_names()
    worst = 0.0
    for _ in range(240):
        w.run(60)
        assert not g.struck and g.brain.state == "in company", w.clock.tick
        assert g.plan[:1] == [("station", f"{f.id}-company")]
        worst = max(worst, P._bearing_distance(f.position, g.position)[1] / units.NAUTICAL_MILE)
    assert worst < 0.5, worst
    assert f.brain.state == "on passage"
    assert not g.damage and "far" not in w.rng.stream_names()


def test_the_rounds_choose_no_prize_no_struck_ship_and_none_of_her_own_side():
    """(F3) at `_pairs`' own level: a far ship engaging a mark makes a pair while the mark is an
    enemy on the sea, her colours up and nobody's prize; struck, a prize, showing her own colours,
    a friend by the hail, or gone, no round."""
    from freesail.world import signalling
    from freesail.world import signals as S

    w, f, g = _a_brig_cut_out()
    g.brain.state = "on passage"
    f.brain._stranger = g.id
    f.brain.state = "engaging"
    assert FA._pairs(w) == [(f, g)]
    g.struck = True
    assert FA._pairs(w) == []
    g.struck = False
    S.set_colours(S.vessel_locker(g).colours, w.nations, "false", "britain", 0)
    assert FA._pairs(w) == []
    S.set_colours(S.vessel_locker(g).colours, w.nations, "shown", "france", 0)
    signalling.recognise(f.brain, g.id, "france", "the hail", False)
    assert FA._pairs(w) == []
    f.brain.recognised.clear()
    assert FA._pairs(w) == [(f, g)]
    g.struck = True
    P.possess(w, f, g, by="a test", said=False)
    assert FA._pairs(w) == []
    g.done = True
    assert FA._pairs(w) == []


@pytest.mark.slow
def test_a_captor_is_alone_after_her_prize_and_hauls_off_from_a_ship_of_the_line():
    """The lead's readings of cda12ec9, (F4), the captor's case: the brig cut out
    (`_a_brig_cut_out`), the frigate commands "her company" of her prize (`prizes.possess`'s
    set), which supports nobody (`Judgement._alone`, the one answer `relations.SUPPORT`): a French
    74 put three miles north of her after the possession, she is alone and the rank-4 rule is
    hers: she evades, and is never engaging the 74 nor struck in the half hour. OLD BESIDE NEW: at
    53c14457 she was never alone again after her first prize: she engaged the 74, struck to her
    and was taken."""
    w, f, g = _a_brig_cut_out()
    w.run(240)
    assert P.is_prize(g) and w.squadrons.of(f.id).id == f"{f.id}-company"
    assert f.brain._alone()
    r = destination(f.position, 0.0, 3.0 * units.NAUTICAL_MILE)
    foe = put(
        w,
        "seventy-four",
        "france",
        {"lat_deg": r.lat_deg, "lon_deg": r.lon_deg},
        "bound for Brest",
        intent="bound for Brest",
        colours="shown",
        name="Foe",
    )
    seen = []
    for _ in range(30):
        w.run(60)
        seen.append(f.brain.state)
        assert not (f.brain.state == "engaging" and f.brain._stranger == foe.id), w.clock.tick
    assert "evading" in seen and not f.struck, seen


def _under_orders(enemy_miles: float | None):
    """Two British frigates bound for Falmouth half a mile apart twelve miles south of the
    player's frigate hove to, the cap nought, seed 7, the second under the first's orders; with
    `enemy_miles` a French frigate bound for Brest so many miles east of them."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.submit("heave to")
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    q = destination(far, 0.0, 0.5 * units.NAUTICAL_MILE)
    boss = put(
        w,
        "frigate",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        colours="shown",
        name="Amethyst",
    )
    mate = put(
        w,
        "frigate",
        "britain",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "bound for Falmouth",
        intent="bound for Falmouth",
        colours="shown",
        name="Arethusa",
    )
    mate.under_orders_of = boss.id
    foe = None
    if enemy_miles is not None:
        e = destination(far, 90.0, enemy_miles * units.NAUTICAL_MILE)
        foe = put(
            w,
            "frigate",
            "france",
            {"lat_deg": e.lat_deg, "lon_deg": e.lon_deg},
            "bound for Brest",
            intent="bound for Brest",
            colours="shown",
            name="Renard",
        )
    w.run(120)
    return w, boss, mate, foe


@pytest.mark.parametrize("signal", ["engage the enemy", "general chase"])
def test_a_signal_to_engage_or_chase_with_nobody_for_it_leaves_her_as_she_was_said(signal):
    """The lead's readings of cda12ec9, (F5): "'engage the enemy' by signal to a far ship with no
    enemy within breaking off ... She does not go engaging with nobody to engage." A signalled
    state that holds a mark is entered only with one for it (`signalling._obey`): an enemy within
    her breaking-off distance by her own judgement for the action, a sail in sight for a chase;
    with none she holds on as she was, and her story says so (for the chase, her commander and
    the player's ship spoken, so that no stranger is in sight). OLD BESIDE NEW: at 53c14457, to
    engage, she went engaging at the signal's minute (tick 300) with no mark, lay to ten minutes
    and was on passage at 960; to chase, she went chasing nobody."""
    from freesail.world import signals as S

    w, boss, mate, _foe = _under_orders(None)
    if signal == "general chase":
        mate.brain.spoken_ids |= {boss.id, "the ship"}
    kind, _text, _ = S.far_order_words(w, boss, f"make the signal: {signal}")
    assert kind == "signal.made"
    for _ in range(20):
        w.run(60)
        assert mate.brain.state == "on passage", (w.clock.tick, mate.brain.history)
    assert [s for _, s in mate.brain.history] == ["on passage"]
    said = [words for _, words in mate.story if "holds on as she was" in words]
    nobody = "no enemy within reach" if signal == "engage the enemy" else "no sail in sight"
    assert len(said) == 1 and nobody in said[0], mate.story[-3:]


def test_a_signal_to_engage_with_an_enemy_within_reach_takes_her_into_the_action():
    """The same signal with a French frigate a mile and a half east of them (within her
    breaking-off distance, beyond her engaging one): she goes engaging at the signal's minute
    with the Frenchman her mark, as before."""
    from freesail.world import signals as S

    w, boss, mate, foe = _under_orders(1.5)
    S.far_order_words(w, boss, "make the signal: engage the enemy")
    assert _until(w, lambda: mate.brain.state == "engaging", 10), mate.brain.history
    assert mate.brain._stranger == foe.id


@pytest.mark.slow
def test_a_save_in_mid_engagement_loads_and_the_action_finishes_as_it_would_have():
    """(C7, the far fight's part): truth 7-231's two 74s saved at tick 600, mid-engagement (both
    `engaging`, rounds fought, the passage held), by the checkpoint's own road
    (`replay.checkpoint_bytes`, its `_Unpickler`); the loaded world run on to tick 1500 finishes
    the action as the world never saved does, minute for minute: the Hero struck at 1200,
    possessed at 1260, the Foudroyant on passage at 1320 with the plan she held, the same far
    records."""
    import io

    from freesail.core import replay

    w, a, b = _two_on_passage()
    w.run(540)
    assert w.clock.tick == 600
    assert a.brain.state == b.brain.state == "engaging" and a.damage.get("rounds", 0) >= 1
    w2 = replay._Unpickler(io.BytesIO(replay.checkpoint_bytes(w))).load()
    a2, b2 = w2.vessels.get(a.id), w2.vessels.get(b.id)

    def row(world, x, y):
        return (
            world.clock.tick,
            x.brain.state,
            y.brain.state,
            x.plan[:1],
            x.struck,
            y.struck,
            P.is_prize(y),
            dict(x.damage),
            dict(y.damage),
        )

    for _ in range(15):
        w.run(60)
        w2.run(60)
        assert row(w2, a2, b2) == row(w, a, b), w.clock.tick
    assert w2.clock.tick == 1500 and P.is_prize(b2) and P.record_of(b2)["captor"] == a2.id
    assert a2.brain.history[-1] == (1320, "on passage") and a2.brain.history == a.brain.history


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
    assert not (a.crew is not None and a.crew.awake), "the cap holds the cutter alone"
    assert FA.FALLBACK_COUNT["rounds"] >= 1
    replies = [e for e in b.crew.log if e.kind == "action.far_reply"]
    assert replies and replies[0].data.get("fallback") is True
    # the line is the ship's words (85's rule): her broadside and the counts in words, with
    # nothing of the cap or the tables in it; the data keeps the fallback for the record
    text = replies[0].text
    assert text.startswith(f"The {a.name} fires her broadside at us from ")
    assert text.endswith(" us.") and " of her " in text
    assert "cap" not in text and "reply" not in text and "(" not in text


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
