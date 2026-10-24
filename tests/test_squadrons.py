"""The squadron as a genuine set (spec M7 §21 to §23; package 72;
docs/design/Design-Squadrons.md): the set and its membership writing 71's relation, the
formations and the station leg at far detail, the set's pace the slowest member's, the
stragglers, the divisions, the state `in company`, the commander's book and his minute,
the succession by the wake, the near body's station keeping, the regimes and the business,
the director's forms."""

from __future__ import annotations

import pytest

from freesail import units
from freesail.world import squadrons as Q
from freesail.world.geo import bearing_and_distance, destination
from tests.test_brains import put, world_at

STATION_INTENT = "keep the station off the Lizard within 10 miles"


def convoy_world(brains=(True, False, True, False, True), cap=0, formation="order of sailing"):
    """A brig-sloop with the commodore's intent and five merchant brigs scattered a mile
    or two astern of her, six miles south-south-west of the player's frigate (whose rules
    captain answers the private signal), the set formed in the order of sailing; the cap
    nought so that the far bodies alone are measured."""
    w = world_at(49.5, -5.5, intent=STATION_INTENT)
    w.crewed_settings = {"cap": cap}
    w.run(60)
    start = destination(w.position, 200.0, 6.0 * units.NAUTICAL_MILE)
    harpy = put(
        w,
        "brig-sloop",
        "britain",
        {"lat_deg": start.lat_deg, "lon_deg": start.lon_deg},
        "bound for the Start",
        intent="convoy the trade from Falmouth to the Start",
        name="Harpy",
    )
    members = [harpy.id]
    for i, with_brain in enumerate(brains):
        p = destination(start, 180.0 + 20.0 * i, (0.3 + 0.2 * i) * units.NAUTICAL_MILE)
        v = put(
            w,
            "merchant brig",
            "britain",
            {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
            "bound for the Start",
            intent="bound for the Start" if with_brain else "",
            name=f"M{i}",
        )
        members.append(v.id)
    sq = Q.Squadron(
        id="convoy",
        name="the convoy",
        kind="convoy",
        commander=harpy.id,
        members=members,
        goal="convoy the trade from Falmouth to the Start",
        formation=formation,
        columns=2,
    )
    w.squadrons.add(sq, w)
    return w, sq, harpy


def off_station_m(w, sq) -> dict[str, float]:
    st = sq.stations(w)
    out = {}
    for m in sq.others():
        v = w.vessels.get(m)
        out[m] = bearing_and_distance(v.position, st[m])[1]
    return out


# -- the set and 71's relation ------------------------------------------------------------


def test_the_set_writes_the_relation_on_every_member_and_clears_it_when_she_leaves():
    w, sq, harpy = convoy_world()
    for m in sq.others():
        v = w.vessels.get(m)
        assert v.under_orders_of == harpy.id and v.squadron == "convoy"
    assert harpy.under_orders_of == "" and harpy.squadron == "convoy"
    # the commodore's brain is the commodore's (found on the way: a far brig-sloop with the
    # convoy intent sailed by the cruiser's doctrine)
    assert harpy.brain.role == "commodore"
    gone = sq.others()[1]
    sq.leave(w, gone, "parted company")
    v = w.vessels.get(gone)
    assert v.under_orders_of == "" and v.squadron == "" and gone not in sq.members
    assert w.squadrons.of(gone) is None and w.squadrons.of(harpy.id) is sq
    assert any("leaves the convoy" in words for _, words in sq.history)


def test_a_member_with_a_brain_and_one_without_are_both_in_company_on_the_station_leg():
    w, sq, harpy = convoy_world()
    w.run(120)
    for m in sq.others():
        v = w.vessels.get(m)
        assert v.state == "in company", (m, v.state)
        assert v.plan and v.plan[0] == ("station", "convoy")
        if v.brain is not None:
            assert v.brain.state == "in company" and v.brain.history[-1][1] == "in company"
    assert harpy.brain.state == "on passage" and harpy.plan[0][0] == "to"


# -- the formation at far detail ----------------------------------------------------------


def test_the_convoy_forms_in_the_order_of_sailing_and_keeps_it_at_the_slowest_ships_pace():
    """Five merchant brigs scattered a mile or two astern close their stations in the
    order of sailing (two columns to leeward of the escort, two cables apart) within three
    hours (the dullest, a mile astern, closes at half a knot under the capped convoy) and
    keep them within the tolerance; the commodore's far body sails at the set's pace, the
    slowest member's best times the book's factor, so the dull sailers keep up."""
    w, sq, harpy = convoy_world()
    w.run(10800)
    errs = off_station_m(w, sq)
    assert all(e <= Q.STATION_TOLERANCE_M for e in errs.values()), errs
    assert harpy.pace_cap_kn is not None
    wind_from, wind_ms = harpy._wind_at(w)
    own = harpy.polar.speed_kn(
        abs(((harpy.heading_deg - wind_from + 180) % 360) - 180), units.ms_to_knots(wind_ms)
    )
    assert harpy.speed_kn <= harpy.pace_cap_kn + 0.05 < own
    # the slots: the escort to windward of the body, the body in two columns
    slots = sq.slots(w)
    body = [m for m in sq.others()]
    assert slots[harpy.id][1] < 0 < min(slots[m][1] for m in body)
    alongs = sorted({round(slots[m][0]) for m in body})
    assert len(alongs) == 3 and alongs[0] < alongs[1] < alongs[2] == 0
    w.run(1800)
    errs = off_station_m(w, sq)
    assert all(e <= Q.STATION_TOLERANCE_M for e in errs.values()), errs
    assert not sq.stragglers


def test_the_stations_turn_with_the_commodores_course_and_the_leeward_side_with_the_wind():
    w, sq, harpy = convoy_world()
    w.run(60)
    before = sq.stations(w)
    # sixty degrees to larboard keeps the wind on the same side (a turn across it would
    # mirror the formation to the new leeward side, which is the rule and not the test)
    harpy.heading_deg = (harpy.heading_deg - 60.0) % 360.0
    harpy.speed_kn = 5.0
    sq._stations_tick = -1
    after = sq.stations(w)
    m = sq.others()[0]
    b0 = bearing_and_distance(harpy.position, before[m])[0]
    b1 = bearing_and_distance(harpy.position, after[m])[0]
    turned = ((b1 - b0 + 180.0) % 360.0) - 180.0
    assert 50.0 < abs(turned) < 70.0


def test_the_line_ahead_and_the_line_abreast_lay_the_members_by_the_interval():
    w, sq, harpy = convoy_world(formation="line ahead")
    slots = sq.slots(w)
    for i, m in enumerate(sq.members):
        assert slots[m] == pytest.approx((-i * sq.interval_m, 0.0))
    sq.formation = "line abreast"
    slots = sq.slots(w)
    assert slots[sq.members[0]] == pytest.approx((0.0, 0.0))
    assert slots[sq.members[1]][0] == 0.0 and abs(slots[sq.members[1]][1]) == pytest.approx(
        sq.interval_m
    )
    assert slots[sq.members[1]][1] == -slots[sq.members[2]][1]


# -- the divisions ------------------------------------------------------------------------


def test_a_division_detached_keeps_station_on_its_leader_and_reads_his_signals_until_recalled():
    w, sq, harpy = convoy_world()
    w.run(60)
    lead, other = sq.others()[0], sq.others()[1]
    d = sq.detach(w, "inshore", lead, [other])
    assert d.detached and d.leader == lead and d.members == [other]
    assert w.vessels.get(other).under_orders_of == lead
    assert w.vessels.get(lead).under_orders_of == harpy.id
    assert sq.under(harpy.id) == [m for m in sq.others() if m not in (lead, other)] + [lead] or (
        lead in sq.under(harpy.id) and other not in sq.under(harpy.id)
    )
    assert sq.under(lead) == [other]
    st = sq.stations(w)
    _, off_lead = bearing_and_distance(w.vessels.get(lead).position, st[other])
    assert abs(off_lead - sq.interval_m) < 1.0
    sq.recall(w, "inshore")
    assert not sq.divisions and w.vessels.get(other).under_orders_of == harpy.id


# -- the scenario's forms -----------------------------------------------------------------


def test_a_scenario_names_a_set_whole_or_by_a_ships_squadron_key(tmp_path):
    from freesail.world.scenarios import load_scenario, make_scenario_world

    text = """
name: a set
seed: 7
start: 1805-06-12T10:00
position: {lat_deg: 49.6, lon_deg: -5.4}
region: channel-west
nation: britain
ship: {file: data/ships/brig.yaml, heading_deg: 90, speed_kn: 5}
intent: convoy the trade from Falmouth to the Start
wind: {from_deg: 45, knots: 12, gustiness: 0.0, variability: 0.0}
ports: [falmouth, plymouth, brest]
ships:
  - id: a
    description: merchant brig
    name: A
    nation: britain
    position: 49 35.0 N 5 24.5 W
    goal: bound for the Start
    squadron: trade
  - id: b
    description: merchant brig
    name: B
    nation: britain
    position: 49 35.2 N 5 24.6 W
    goal: bound for the Start
    squadron: trade
  - id: c
    description: cutter
    name: C
    nation: britain
    position: 49 35.4 N 5 24.7 W
    goal: bound for the Start
    intent: bound for the Start
squadrons:
  - id: trade
    name: the Falmouth trade
    kind: convoy
    commander: the ship
    members: [c]
    formation: order of sailing
    columns: 2
    interval_cables: 2
"""
    path = tmp_path / "set.yaml"
    path.write_text(text, encoding="utf-8")
    sf = load_scenario(path)
    assert len(sf.scenario.squadrons) == 1
    w = make_scenario_world(sf)
    sq = w.squadrons.find("the Falmouth trade")
    assert (
        sq is not None and sq.commander == "the ship" and sq.members == ["the ship", "c", "a", "b"]
    )
    assert sq.goal == "convoy the trade from Falmouth to the Start"
    for vid in ("a", "b", "c"):
        assert w.vessels.get(vid).under_orders_of == "the ship"
    assert w.vessels.get("a").plan[0] == ("station", "trade")
    d = w.scenario.to_dict()
    assert d["squadrons"][0]["id"] == "trade"
    bad = text.replace("kind: convoy", "kind: fleet")
    path.write_text(bad, encoding="utf-8")
    with pytest.raises(Exception, match="no kind"):
        load_scenario(path)


# -- the commander's book and his minute -------------------------------------------------


def test_the_commodores_book_signals_a_straggler_and_she_makes_sail():
    """A merchantman a mile and a half astern is a straggler after ten minutes; the convoy book's
    rule makes the signal (No. 20, the ships astern to make more sail) on the far
    commodore's locker, and she reads and performs it; she regains her station under the
    capped convoy (at half a knot of closing) within four hours and the rule re-arms."""
    w, sq, harpy = convoy_world(brains=(False, False, False))
    p = destination(harpy.position, 235.0, 1.6 * units.NAUTICAL_MILE)
    nancy = put(
        w,
        "merchant brig",
        "britain",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "bound for the Start",
        name="Nancy",
    )
    sq.join(w, nancy.id)
    w.run(900)
    assert nancy.id in sq.stragglers
    assert "rule:straggler" in sq.made
    assert any("ships astern to make more sail" in words for _, words in harpy.story)
    w.run(600)
    assert any("made sail" in words for _, words in nancy.story), nancy.story
    w.run(11400)
    assert nancy.id not in sq.stragglers and "rule:straggler" not in sq.made
    assert off_station_m(w, sq)[nancy.id] <= Q.STATION_TOLERANCE_M


def test_a_crewed_commodore_shortens_sail_by_his_book_when_a_member_falls_astern():
    """The near body has no pace cap: the commodore promoted within the player's four
    miles runs away from his convoy at the physics' pace, and the book's near-only rule
    has him shorten sail (by steps, every twenty minutes while one is astern)."""
    w, sq, harpy = convoy_world(brains=(True, False, True, False), cap=3)
    # the player's frigate is six miles off: close the convoy to within the range
    here = w.position
    for v in w.vessels.vessels:
        b, d = bearing_and_distance(here, v.position)
        v.position = destination(
            here, b, max(d - 3.5 * units.NAUTICAL_MILE, 0.3 * units.NAUTICAL_MILE)
        )
    w.run(1500)
    assert harpy.crew is not None and harpy.crew.shape == "full"
    assert "rule:pace" in sq.made
    said = [e.text for e in harpy.crew.log if "shortening sail (the squadron's book)" in e.text]
    assert said, [e.text[:80] for e in harpy.crew.log if "captain" in e.kind][-5:]


def test_an_enemy_made_out_closes_the_convoy_round_the_commodore_with_no_model_seated():
    """A French privateer schooner under British colours within two miles of the convoy:
    the commodore challenges her with the private signal, her bluff is wrong, she is an
    enemy to him, and his book makes the convoy book's signal to close round the commodore
    (the set in close order), which the merchantmen read and answer; when she is lost the
    order of sailing is formed again."""
    w, sq, harpy = convoy_world(brains=(False, False, False, False))
    w.run(1200)
    p = destination(harpy.position, 150.0, 1.8 * units.NAUTICAL_MILE)
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="British",
        name="Vengeur",
    )
    pv.sailing_factor = 1.0
    for _ in range(70):
        w.run(60)
        if "rule:close" in sq.made:
            break
    assert "rule:close" in sq.made, (harpy.story, harpy.brain.recognised)
    assert sq.formation == "close order"
    assert any("close round the commodore" in words for _, words in harpy.story)
    w.run(600)
    gap = sq.interval_m * 0.5
    slots = sq.slots(w)
    body = [m for m in sq.others()]
    assert max(abs(slots[m][1]) for m in body) <= gap + 1.0
    # the merchantmen read it and answered with the pendant
    read = [
        m for m in sq.others() if any("close round" in words for _, words in w.vessels.get(m).story)
    ]
    assert len(read) >= 2, [w.vessels.get(m).story for m in sq.others()]


# -- the straggler cut out at far detail -----------------------------------------------------


def test_a_merchantman_brought_to_by_a_privateer_with_no_cover_strikes_and_joins_his_company():
    """Rule 5's least (74's hook): a merchant brig alone, a French privateer schooner a mile
    off who chases her and comes up within hail with no man of war of hers within two
    miles: she strikes by rule, her colours struck, and joins the privateer's company as a
    prize, keeping station on him as he returns to his cruise."""
    w = world_at(49.5, -5.5, intent=STATION_INTENT)
    w.crewed_settings = {"cap": 0}
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    # a merchantman with her goal and no brain, as a convoy's are (one with a brain of her
    # own evades at seven knots, and a topsail schooner at seven and a fifth closes her at a
    # fifth of a knot: a stern chase of hours, which is the physics and honest)
    prey = put(
        w,
        "merchant brig",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for the Start",
        name="Nancy",
    )
    prey.sailing_factor = 0.85  # a dull sailer, as the record has the stragglers
    p = destination(far, 270.0, 1.2 * units.NAUTICAL_MILE)  # to windward, within the tops' range
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        colours="shown",
        name="Vengeur",
    )
    pv.sailing_factor = 1.0
    for _ in range(150):
        w.run(60)
        if prey.struck:
            break
    assert prey.struck and prey.state == "struck"
    assert prey.signals.colours.state == "struck"
    company = w.squadrons.commanded_by(pv.id)
    assert company is not None and prey.id in company.prizes and prey.squadron == company.id
    assert any("struck" in words for _, words in prey.story)
    assert any(e.kind == "squadron.cut_out" for e in w.log)


def test_the_cut_out_is_withheld_while_a_man_of_war_of_hers_is_within_the_cover_distance():
    from freesail.world import squadrons as Q2

    w = world_at(49.5, -5.5, intent=STATION_INTENT)
    w.crewed_settings = {"cap": 0}
    w.run(60)
    far = destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE)
    prey = put(
        w,
        "merchant brig",
        "britain",
        {"lat_deg": far.lat_deg, "lon_deg": far.lon_deg},
        "bound for the Start",
        name="Nancy",
    )
    p = destination(far, 200.0, 0.05 * units.NAUTICAL_MILE)
    pv = put(
        w,
        "schooner",
        "france",
        {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg},
        "cruising off the Lizard within 20 miles",
        intent="cruise for prizes off the Lizard within 20 miles",
        name="Vengeur",
    )
    pv.brain.state = "chasing"
    pv.brain._stranger = prey.id
    q = destination(far, 90.0, 1.0 * units.NAUTICAL_MILE)
    put(
        w,
        "brig-sloop",
        "britain",
        {"lat_deg": q.lat_deg, "lon_deg": q.lon_deg},
        "bound for the Start",
        intent="bound for the Start",
        name="Harpy",
    )
    assert Q2._armed_enemy_alongside(w, prey) is pv and Q2._covered(w, prey)
    assert Q2.far_captures(w) == [] and not prey.struck


# -- the succession by the wake --------------------------------------------------------------


def test_the_convoy_tacks_in_succession_by_the_wake_each_at_the_ship_aheads_turning_point():
    """In line ahead four cables apart, the far commodore's hoist of the convoy book's No. 5
    is read by each merchantman and performed in succession by the wake: each puts about
    when her own run since the ship ahead went about reaches the distance she was astern
    of her, so the second is four cables of run after the first (five or six minutes at the
    convoy's pace, the run counted by the minute), not 71's three minutes; at two cables
    and this pace the two coincide, which is why the test opens the line. The ships under
    orders outside a set keep the three minutes (truth 7-145)."""
    from freesail.world import signals as S

    w, sq, harpy = convoy_world(brains=(False, False, False), formation="line ahead")
    sq.interval_m = 4.0 * units.CABLE
    w.run(7200)
    assert all(e <= Q.STATION_TOLERANCE_M for e in off_station_m(w, sq).values())
    books = S.books_for_nation(w.nations, "britain")
    entry, q = books.find("tack in succession", "convoy")
    S.make_hoist(S.vessel_locker(harpy), books, entry, q, harpy.id, int(w.clock.tick))
    about: dict[str, int] = {}
    where: dict[str, object] = {}
    for _ in range(40):
        w.run(60)
        for m in sq.others():
            v = w.vessels.get(m)
            if m not in about and any("went about" in words for _, words in (v.story or ())):
                about[m] = next(t for t, words in v.story if "went about" in words)
                where[m] = v.position
    assert set(about) == set(sq.others()), about
    ticks = [about[m] for m in sq.others()]
    gaps = [b - a for a, b in zip(ticks, ticks[1:], strict=False)]
    assert ticks == sorted(ticks) and all(300 <= g <= 420 for g in gaps), gaps
    others = sq.others()
    for a, b in zip(others, others[1:], strict=False):
        _, d = bearing_and_distance(where[a], where[b])
        assert d <= 1.5 * units.CABLE, (a, b, d)
