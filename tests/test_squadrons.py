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
