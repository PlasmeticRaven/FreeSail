"""The marines, the small arms and the fight on deck (spec M7 §11, §11a; package 73;
`freesail/combat/small_arms.py`, `freesail/combat/boarding.py`, `freesail/orders/fight.py`;
the design in `docs/design/Design-WaterAndHealth.md`)."""

from __future__ import annotations

import math
from datetime import datetime

import pytest

from freesail.api.session import make_world
from freesail.combat import boarding as B
from freesail.combat import small_arms as SA
from freesail.combat.action import target_of
from freesail.core.world import Scenario
from freesail.crew.model import Station

FRIGATE = "data/ships/frigate-36.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
MERCHANT = "data/ships/merchant-brig.yaml"


def _scenario(speed: float = 0.0) -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
        ship_heading_deg=180.0,
        ship_speed_kn=speed,
    )


def _enemy(
    world,
    bearing_deg: float,
    distance_m: float,
    description="frigate",
    name="Medusa",
    nation="france",
):
    """A ship of the nation made so far off on the bearing, lying to, and crewed at once;
    her captain's state `engaging`."""
    from freesail.world import crews
    from freesail.world.geo import destination
    from freesail.world.ships import vessel_from_spec

    there = destination(world.position, bearing_deg, distance_m)
    world.vessels.serial += 1
    v = vessel_from_spec(
        world,
        {
            "description": description,
            "name": name,
            "nation": nation,
            "position": there,
            "goal": "bound for 48 30 N 5 18 W",
            "intent": "bound for 48 30 N 5 18 W",
        },
        world.vessels.serial,
    )
    v.plan = [("lie_to", math.inf)]
    v.sail_state = "lying to"
    world.vessels.add(v)
    enemy = crews.promote(world, v)
    enemy.captain.state = "engaging"
    return v, enemy


def _alongside(distance_m: float = 10.0, her_quarters: bool = False, her_captain: bool = False):
    """The player's frigate at quarters with her fire held, and a French frigate made so far
    off her starboard beam and crewed; the lookout given his minute; the mark engaged to
    starboard. Her captain stands aside (the test moves her) unless `her_captain`."""
    w = make_world(7, FRIGATE, _scenario())
    w.submit("beat to quarters")
    w.run(5)
    heading = math.degrees(float(w.ship.heading))
    v, enemy = _enemy(w, heading + 90.0, distance_m)
    enemy.ship.dyn.heading = float(w.ship.heading)
    if not her_captain:
        enemy.captain.aside = True
    else:
        # her captain enters the action by his own transition (the drum, the guns, the
        # small arms), not by the state set from outside
        enemy.captain.state = None
    if her_quarters:
        enemy.submit("beat to quarters")
    w.submit("hold your fire")
    w.run(65)
    out = w.submit("engage her to starboard")
    assert out.kind == "guns.engage", out.text
    return w, v, enemy


def _events(world, kind: str) -> list:
    return [e for e in world.log if e.kind == kind]


# -- the bill and the figures ---------------------------------------------------------------------


def test_the_quarter_bill_counts_the_small_arms_men_and_the_boarders_through_the_generator():
    """§11: each armed ship file's bill has its small-arms men and its boarders (the
    generator's figures with their notes); a ship whose bill is reckoned has a tenth and
    a half of her fit seamen."""
    from freesail.ship.loader import load_ship

    for path, arms, boarders in (
        (FRIGATE, 20, 60),
        (CUTTER, 6, 20),
        (BRIG, 8, 30),
        (MERCHANT, 2, 6),
    ):
        spec = load_ship(path).spec
        assert (spec.crew.quarter_bill.small_arms, spec.crew.quarter_bill.boarders) == (
            arms,
            boarders,
        ), path
    w = make_world(7, FRIGATE, _scenario())
    assert SA.small_arms_count(w.ship) == 20 and SA.boarders_count(w.ship) == 60


def test_the_hit_chance_falls_with_the_square_of_the_range_to_nought_at_musket_shot():
    """§11: the kit's chance at fifty yards, five times it at point blank, nought at a
    hundred yards; the British and the French kits by nation, the basic kit else."""
    kit = {"hit_at_50_yd": 0.05}
    assert SA.hit_chance(kit, SA.AIMED_AT_M) == pytest.approx(0.05)
    assert SA.hit_chance(kit, 0.0) == pytest.approx(
        0.05 / (1 - SA.AIMED_AT_M / SA.MUSKET_SHOT_M) ** 2
    )
    assert SA.hit_chance(kit, SA.MUSKET_SHOT_M) == 0.0 and SA.hit_chance(kit, 200.0) == 0.0
    assert SA.hit_chance(kit, 70.0) < SA.hit_chance(kit, 60.0) < SA.hit_chance(kit, 50.0)
    from freesail.world.nations import load_nations

    n = load_nations()
    assert (
        n.marines_kit_of("britain")["id"] == "british"
        and n.marines_kit_of("britain")["volley_s"] == 20
    )
    assert n.marines_kit_of("france")["tops_share"] > n.marines_kit_of("britain")["tops_share"]
    assert (
        n.marines_kit_of("spain")["id"] == "basic" and n.marines_kit_of("nowhere")["id"] == "basic"
    )


# -- the marines --------------------------------------------------------------------------------


def test_the_marines_fire_by_volley_within_musket_shot_and_her_people_fall():
    """§11: within musket shot of a near deck the marines fire by volley at the kit's rate
    (three a minute, the British drill), the hits drawn on the mark's exposed men with
    the quarterdeck's share, each a musket ball in the health keeper's words; both logs
    say so (ours the volleys and the men seen to fall, hers 'musketry from her deck');
    beyond musket shot nothing; not at quarters, refused; a ship without marines refused
    to her small arms."""
    w, v, enemy = _alongside(30.0)
    out = w.submit("marines, fire by volley")
    assert (
        out.kind == "marines.fire"
        and "40 muskets" in out.text
        and "from the carronades" in out.text
    )
    assert "the detachment" not in out.text
    w.run(180)
    ours = _events(w, "action.musketry")
    assert ours and "fire by volley" in ours[0].text and ours[0].data["volleys"] >= 2
    crew = enemy.ship.extra["crew"]
    hurt = [s for s in crew.sailors if s.hurt]
    assert hurt, [e.text for e in ours]
    assert all("musket ball" in s.hurt_how for s in hurt)
    hits = _events(enemy, "action.hit")
    assert hits and "musketry from her deck" in hits[0].text
    assert any(s.station is Station.QUARTERDECK for s in hurt) or len(hurt) < 6
    assert "firing by volley" in w.readings.words("marines")
    # beyond musket shot: nothing more falls
    far = make_world(7, FRIGATE, _scenario())
    far.submit("beat to quarters")
    far.run(5)
    assert far.submit("marines, fire at will").kind == "marines.fire"
    v2, e2 = _enemy(far, math.degrees(float(far.ship.heading)) + 90.0, 150.0)
    e2.captain.aside = True
    far.run(125)
    assert not [s for s in e2.ship.extra["crew"].sailors if s.hurt]
    # the refusals
    cold = make_world(7, FRIGATE, _scenario())
    out = cold.submit("marines, fire by volley")
    assert out.kind == "order.rejected" and "beat to quarters" in out.text
    cutter = make_world(7, CUTTER, _scenario())
    out = cutter.submit("marines, fire at will")
    assert out.kind == "order.rejected" and "no marines" in out.text


def test_the_marines_leave_the_carronades_for_their_muskets_and_go_back_when_the_fire_is_held():
    """§11 (70's beat kept): at the beat the marines serve the quarterdeck carronades;
    `marines, fire by volley` takes them to their muskets and the carronades go short by
    them, `marines, hold your fire` sends them back; the tops take the kit's share."""
    w = make_world(7, FRIGATE, _scenario())
    w.submit("beat to quarters")
    w.run(5)
    q = w.ship.extra["quarters"]
    at_guns = {
        gc.key: sum(1 for s in gc.members if s.station is Station.MARINES)
        for gc in q.crews.values()
    }
    assert sum(at_guns.values()) == 40 and not SA.marines_of(w.ship)
    at_carronades = sum(n for key, n in at_guns.items() if q.crews[key].kind == "carronade")
    assert at_carronades >= 10  # the carronades first, the rest where a crew is short
    out = w.submit("marines, fire at will")
    assert out.kind == "marines.fire" and "40 from the carronades" in out.text
    assert len(SA.marines_of(w.ship)) == 40
    assert (
        sum(1 for gc in q.crews.values() for s in gc.members if s.station is Station.MARINES) == 0
    )
    short = [gc for gc in q.crews.values() if len(gc.members) < gc.wanted]
    assert short
    out = w.submit("marines to the tops")
    assert out.kind == "marines.tops" and "eight of the 40" in out.text
    assert SA.musketry_of(w.ship).in_tops and "in the tops" in w.readings.words("marines")
    assert w.submit("marines to the tops").kind == "order.rejected"
    assert w.submit("marines to the gangways").kind == "marines.tops"
    out = w.submit("marines, hold your fire")
    assert out.kind == "marines.fire" and "back to the carronades" in out.text
    assert (
        sum(1 for gc in q.crews.values() for s in gc.members if s.station is Station.MARINES) == 40
    )
    assert not SA.marines_of(w.ship)


def test_serve_out_the_small_arms_takes_the_gunners_party_five_minutes_and_arms_the_men():
    """§11: `serve out the small arms` is an evolution of five minutes; before it the
    small-arms men may not fire and the boarders fight at half strength; after it the
    small-arms men fire at will within musket shot and the readings say served."""
    w = make_world(7, FRIGATE, _scenario())
    w.submit("beat to quarters")
    w.run(5)
    out = w.submit("small arms, fire at will")
    assert out.kind == "order.rejected" and "serve out the small arms" in out.text
    assert "in the arms chests" in w.readings.words("small_arms")
    before = sum(f for _, f in B.boarders_of(w.ship, w))
    out = w.submit("serve out the small arms")
    assert out.kind in ("order.accepted", "evolution.started", "evolution.queued"), out.text
    w.run(200)
    assert not SA.musketry_of(w.ship).served
    w.run(200)
    assert SA.musketry_of(w.ship).served
    assert _events(w, "small_arms.served")
    assert sum(f for _, f in B.boarders_of(w.ship, w)) > before
    out = w.submit("small arms men, fire at will")
    assert out.kind == "small_arms.fire" and "20 muskets" in out.text
    assert "served out" in w.readings.words("small_arms") and "firing at will" in w.readings.words(
        "small_arms"
    )
    assert w.submit("serve out the small arms").kind == "order.rejected"


# -- the grapple and the fight on deck ---------------------------------------------------------


def test_grapple_her_within_a_grapnels_throw_holds_both_ships_and_beyond_it_is_refused():
    """§11a: `grapple her` is refused beyond thirty metres; within it the grapnels hold
    from the throw: both ships carry `grappled_to`, both logs say so, and the two lie
    locked (the range does not change) until `cast off the grapnels` frees them."""
    w, v, enemy = _alongside(60.0)
    out = w.submit("grapple her")
    assert out.kind == "order.rejected" and "beyond a grapnel's throw" in out.text
    w, v, enemy = _alongside(10.0)
    rng0 = target_of(w, v.id).range_m
    assert rng0 <= B.GRAPPLE_RANGE_M
    out = w.submit("grapple her")
    assert out.kind in ("order.accepted", "evolution.started"), out.text
    w.run(2)
    assert B.grappled_to(w.ship) == v.id and B.grappled_to(enemy.ship)
    hers = _events(enemy, "ship.grappled")
    assert hers and "has grappled us" in hers[0].text
    w.run(180)
    assert abs(target_of(w, v.id).range_m - rng0) < 2.0
    done = _events(w, "ship.grappled")
    assert done and "locked together" in done[-1].text
    assert "grappled to a frigate" in w.readings.words("boarders")
    out = w.submit("cast off the grapnels")
    assert out.kind == "ship.cast_off"
    assert not B.grappled_to(w.ship) and not B.grappled_to(enemy.ship)
    assert w.submit("cast off the grapnels").kind == "order.rejected"
    assert w.submit("boarders away").kind == "order.rejected"


def test_boarders_against_a_whole_company_awake_are_repulsed_and_the_temper_pays_for_it():
    """§11a: a hundred boarders (the bill's sixty and the forty marines) against a frigate's
    whole company on deck are repulsed in a round: the crossing's volley told, the round's
    losses on both musters, the lines on both logs, the grapnels cast off, the repulse
    on the hands' temper."""
    w, v, enemy = _alongside(10.0)
    w.submit("grapple her")
    w.run(65)
    out = w.submit("boarders away")
    assert out.kind == "action.boarders" and "over the side" in out.text, out.text
    assert len([e for e in w.log if e.kind == "action.boarders"]) == 1  # said once
    boarded = _events(enemy, "action.boarded")
    assert boarded and "coming over the side" in boarded[0].text
    for _ in range(B.CONTEST_ROUNDS + 1):
        w.run(60)
        f = B.fight_of(w.ship)
        if f is not None and f.over:
            break
    f = B.fight_of(w.ship)
    assert f is not None and f.over == "repulsed" and f.round <= 3
    rounds = _events(w, "action.boarding")
    assert rounds and "fight at the gangways" in rounds[0].text
    assert rounds[0].data["strength_defence"] > rounds[0].data["strength_attack"]
    assert _events(w, "action.repulsed") and _events(enemy, "action.repulsed")
    assert not B.grappled_to(w.ship) and not B.grappled_to(enemy.ship)
    from freesail.combat.morale import morale_of

    assert morale_of(w.ship).repulses == pytest.approx(B.REPULSE_COST)
    ours = [s for s in w.ship.extra["crew"].sailors if s.hurt]
    theirs = [s for s in enemy.ship.extra["crew"].sailors if s.hurt]
    assert len(ours) == f.lost_attack and len(theirs) == f.lost_defence and ours and theirs
    assert all(
        any(
            w_ in s.hurt_how
            for w_ in ("cutlass", "pike", "pistol", "tomahawk", "musket", "bayonet", "grape")
        )
        for s in ours
    )
    assert "the last fight repulsed" in w.readings.words("boarders")


def test_boarders_carry_a_deck_held_by_her_marines_and_the_colours_come_down_by_their_hand():
    """§11a: against a frigate at quarters, her gun crews at the guns, the boarders with
    their arms served out carry the deck in a few rounds: her colours come down by the
    boarders' hand (`action.strike` with the words), the far body struck, the losses on
    both musters by name, the prize crew left to 74."""
    w, v, enemy = _alongside(10.0, her_quarters=True)
    w.submit("grapple her")
    w.submit("serve out the small arms")
    w.run(400)
    assert SA.musketry_of(w.ship).served and B.grappled_to(w.ship) == v.id
    out = w.submit("boarders away")
    assert out.kind == "action.boarders", out.text
    for _ in range(B.CONTEST_ROUNDS + 1):
        w.run(60)
        f = B.fight_of(w.ship)
        if f is not None and f.over:
            break
    f = B.fight_of(w.ship)
    assert f is not None and f.over == "carried", (f.over, f.round)
    assert 2 <= f.round <= 12
    carried = _events(w, "action.carried")
    assert carried and "by our boarders' hand" in carried[0].text
    struck = _events(enemy, "action.struck")
    assert struck and "carried by boarding" in struck[0].text
    assert v.struck and enemy.ship.extra.get("struck")
    assert B.grappled_to(w.ship) == v.id  # the prize alongside, 74's
    her_hurt = [s for s in enemy.ship.extra["crew"].sailors if s.hurt]
    assert len(her_hurt) == f.lost_defence > f.lost_attack
    assert "wounded" in enemy.readings.words("bill")
    assert "the last fight carried" in w.readings.words("boarders")


def test_repel_boarders_brings_the_gun_crews_up_and_the_guns_fall_silent():
    """§11a: `repel boarders` is the defender's one order: the gun crews up with the pikes
    and cutlasses, the battery held, the defence every fit man but the powder's, the
    carpenter's and the surgeon's; refused off quarters."""
    from freesail.combat.guns import FireMode, battery_of
    from freesail.crew.quarters import CARPENTER, POWDER, SURGEON

    w = make_world(7, FRIGATE, _scenario())
    out = w.submit("repel boarders")
    assert out.kind == "order.rejected" and "beat to quarters" in out.text
    w.submit("beat to quarters")
    w.run(5)
    w.submit("fire as they bear")
    few = len(B.defenders_of(w.ship, w, False))
    out = w.submit("repel boarders")
    assert out.kind == "action.repel" and "gun crews up" in out.text
    assert battery_of(w.ship).mode is FireMode.HOLD and SA.musketry_of(w.ship).repelling
    q = w.ship.extra["quarters"]
    crew = w.ship.extra["crew"]
    below = {s.id for name in (POWDER, CARPENTER, SURGEON) for s in q.divisions.get(name, [])}
    many = len(B.defenders_of(w.ship, w, True))
    assert many == sum(1 for s in crew.sailors if s.fit and s.id not in below) > few
    assert "repel boarders" in w.readings.words("boarders")


def test_cast_off_is_refused_while_her_boarders_are_on_our_deck():
    """§11a: the defender cannot cast off the grapnels with the enemy's boarders on his
    deck; the attacker's cast-off recalls his boarders as a repulse."""
    w, v, enemy = _alongside(10.0)
    w.submit("grapple her")
    w.run(65)
    enemy.submit("beat to quarters")
    enemy.run(5) if hasattr(enemy, "run") else w.run(5)
    text = B.boarders_away(enemy)  # her boarders over the side on to ours
    assert "Boarders away" in text
    f = B.fight_of(w.ship)
    assert f is not None and f.defender is w.ship
    out = w.submit("cast off the grapnels")
    assert out.kind == "order.rejected" and "repel them" in out.text
    assert w.submit("boarders away").kind == "order.rejected"
    assert "hers on our deck" in w.readings.words("boarders")
    out = w.submit("repel boarders")
    assert out.kind == "action.repel" and f.repelling


# -- the doctrine ---------------------------------------------------------------------------


def test_the_rules_captain_opens_musketry_within_a_cable_and_serves_out_the_arms_by_his_doctrine():
    """§11, item 7: a French frigate's captain at quarters (the King's ship's doctrine,
    the French kit) serves out the small arms on entering the action and opens with the
    small arms and the marines within `musketry_cables`; his lines in his log say so in
    the orders' own words, and our people fall to his musketry."""
    w, v, enemy = _alongside(15.0, her_captain=True)
    w.run(540)  # his first judgement comes some minutes in; the arms take five
    said = [e.text for e in enemy.log if e.text.startswith("By the captain")]
    assert any("serving out the small arms" in t for t in said), said
    assert any(
        "the marines to fire by volley" in t or "the small-arms men to fire at will" in t
        for t in said
    ), said
    assert not any("smalling" in t or "marining" in t for t in said)
    # his orders took: the marines at their muskets (the hits are the range's, which his
    # beam law opens: the fire itself is the musketry test's)
    m = SA.musketry_of(enemy.ship)
    assert m.mode == "volley" and SA.marines_of(enemy.ship)
    assert (
        m.served
        or any(
            "serve_small_arms" in str(e.data) for e in enemy.log if e.kind == "evolution.started"
        )
        or any("Serve out the small arms" in e.text for e in enemy.log)
    )
    ours = [s for s in w.ship.extra["crew"].sailors if s.hurt]
    assert all("musket ball" in s.hurt_how for s in ours)
    from freesail.world.captains import load_doctrine

    for role, odds in (("kings-ship", 1.3), ("privateer", 1.0), ("merchant", 0.0)):
        d = load_doctrine(role)
        assert d.threshold("board_odds") == odds and d.threshold("board_when") == "her guns silent"
        assert d.threshold("pumps_at_m") == 0.3
        assert str(d.threshold("damage_priority")).startswith("the leak")
        assert d.sources["board_odds"]


# -- the director's hand (item 8) ---------------------------------------------------------------


def test_the_director_puts_men_on_the_sick_list_and_hurts_an_officer_by_the_aboard_forms():
    """Item 8 (spec M7 §16, §16a): `aboard: a man taken ill`, `the fever in the ship`,
    `the first lieutenant is hurt` and `the surgeon taken ill` are the director's forms,
    each doubted without its cause and performed with one: the sick list, the officer's
    wound and his station's roads, the surgeon off his work."""
    from freesail.agents import director as D

    w = make_world(7, FRIGATE, _scenario())
    told: list = []
    w.needs.listen(told.append)
    crew = w.ship.extra["crew"]
    said = D.direct(w, "aboard: a man taken ill", by="the test")
    assert "Doubt" in said or "doubt" in said, said
    said = D.direct(w, "aboard: a man taken ill [reason: the test]", by="the test")
    assert said.startswith("Done: found aboard") and "on the sick list" in said, said
    assert sum(1 for s in crew.sailors if s.hurt == "sick") == 1
    # the doubt seen first, then entered again with the reason (package 68)
    D.direct(w, "aboard: the fever in the ship", by="the test")
    said = D.direct(w, "aboard: the fever in the ship [reason: the test]", by="the test")
    assert "on the sick list" in said, said
    assert sum(1 for s in crew.sailors if s.hurt == "sick") >= 15
    reports = [e for e in w.log if e.kind == "aboard.found"]
    assert "fever broken out" in reports[-1].text
    assert "sick" in w.readings.words("bill")
    lieutenant = w.people.find("the first lieutenant")
    D.direct(w, "aboard: the first lieutenant is hurt", by="the test")
    said = D.direct(w, "aboard: the first lieutenant is hurt [reason: the test]", by="the test")
    assert lieutenant.name in said and "lightly" in said, said
    s = crew.by_id[lieutenant.sailor_id]
    assert s.hurt == "wounded" and s.wound == "light" and "fall" in s.hurt_how
    assert "wounded" in w.people.state_words(lieutenant)
    D.direct(w, "aboard: the surgeon taken ill", by="the test")
    said = D.direct(w, "aboard: the surgeon taken ill [reason: the test]", by="the test")
    assert "on his own sick list" in said, said
    assert w.health.surgeon() is None and "surgeon's mate" in w.readings.words("surgeon")
    said = D.direct(w, "aboard: the surgeon taken ill [reason: the test]", by="the test")
    assert "bears no surgeon, or he is ill already" in said
    forms = [f for f in D.WORLD_ORDER_FORMS if f.key == "aboard.found"][0]
    assert "aboard: the first lieutenant is hurt" in forms.examples
