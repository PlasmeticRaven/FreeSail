"""Courses and intents by way of marks (package 45, Part A item 5; spec M6 §4 and §26).

`shape a course for Lisbon via Ushant and Finisterre` and `bound for Lisbon via Ushant,
Finisterre`: the marks are sailed in order, a mark that is land or a danger passed a berth
off to seaward and left on the hand the straight line puts it, a mark that is water sailed
to; the master keeps the way and shapes each next course as a mark is reached or passed
abeam; the rules-based captain's plan carries the legs. No routing between the marks: a
captain or a player with no `via` sails the straight line as before.
"""

from __future__ import annotations

import pytest

from freesail.core.world import World
from freesail.world.captains import Planner, read_intent, split_via, way_marks
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

FALMOUTH_LESSON = "data/scenarios/lesson-falmouth.yaml"


@pytest.fixture(scope="module")
def off_falmouth() -> World:
    sf = load_scenario(FALMOUTH_LESSON)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(120)
    return w


def test_via_is_parted_at_commas_and_then_and_where_the_grammar_dropped_them(off_falmouth):
    assert split_via("Lisbon via Ushant, Finisterre") == ("Lisbon", ["Ushant", "Finisterre"])
    both = ("Lisbon", ["Ushant", "Finisterre"])
    assert split_via("Lisbon via Ushant and then Finisterre") == both
    assert split_via("Lisbon") == ("Lisbon", [])
    # an order's grammar drops the commas: the words are parted into the chart's marks
    assert split_via("lisbon via ushant finisterre", off_falmouth) == (
        "lisbon",
        ["ushant", "finisterre"],
    )
    assert split_via("lisbon via the lizard 48 20 N 4 36 W", off_falmouth)[1] == [
        "the lizard",
        "48 20 N 4 36 W",
    ]


def test_a_land_mark_is_passed_to_seaward_on_the_hand_the_line_puts_it(off_falmouth):
    """Ushant between Falmouth and Finisterre is left to larboard, the point five miles to
    the northward and westward of it; Finisterre between Ushant and Lisbon is left to
    larboard too, to seaward (the straight line from Ushant to Lisbon runs across Galicia,
    so the hand is the sea room's and not that line's); a pricked position and a sounding
    are sailed to themselves."""
    w = off_falmouth
    lisbon = w.chart.find_feature("Lisbon").position
    pts = way_marks(w, w.navigation.account_now(), ["Ushant", "Finisterre"], lisbon)
    assert [p[0] for p in pts] == [
        "5 miles north-west of Ushant",
        "5 miles south-west of Cape Finisterre",
    ]
    ushant, finisterre = pts
    assert "leaving Ushant to larboard" in ushant[2] and ushant[1].lon_deg < -5.14
    assert "leaving Cape Finisterre to larboard" in finisterre[2]
    assert finisterre[1].lon_deg < -9.27 and finisterre[1].lat_deg < 42.88
    sea = way_marks(
        w,
        w.navigation.account_now(),
        ["48 20 N 5 30 W", "the soundings seven leagues south-west of Ushant"],
        lisbon,
    )
    assert all(p[2] == "" for p in sea)
    assert abs(sea[0][1].lat_deg - 48.3333) < 0.01 and abs(sea[0][1].lon_deg + 5.5) < 0.01
    with pytest.raises(ValueError, match="names no mark of the chart"):
        way_marks(w, w.navigation.account_now(), ["the moon"], lisbon)


def test_the_order_shapes_the_first_mark_and_the_master_keeps_the_way(off_falmouth):
    w = off_falmouth
    nav = w.navigation
    e = w.submit("shape a course for Lisbon via Ushant and Finisterre")
    assert e.kind == "helm.set", e.text
    assert "Shaped a course for 5 miles north-west of Ushant" in e.text
    assert "then 5 miles south-west of Cape Finisterre, then Lisbon" in e.text
    assert "leaving Ushant to larboard" in e.text
    assert e.data["via"] == ["5 miles south-west of Cape Finisterre", "Lisbon"]
    assert nav.way_mark == "5 miles north-west of Ushant"
    assert [x["said"] for x in nav.way] == ["5 miles south-west of Cape Finisterre", "Lisbon"]
    assert nav.way_words().startswith("for 5 miles north-west of Ushant, then ")
    # the mark reached by account: the next course shaped by the master, said in the log
    nav.way_target = nav.account_now()
    w.run(60)
    said = [x for x in w.log if x.text.startswith("By the way shaped")]
    assert said, [x.text for x in w.log[-20:]]
    assert "5 miles north-west of Ushant reached, leaving Ushant to larboard" in said[-1].text
    assert "the course shaped for 5 miles south-west of Cape Finisterre" in said[-1].text
    assert nav.way_mark == "5 miles south-west of Cape Finisterre"
    assert [x["said"] for x in nav.way] == ["Lisbon"]
    assert said[-1].actor.startswith("standing order")  # a rule's order: never journaled
    assert not any(o[2].startswith("shape a course for 5 miles south-west") for o in w.journal)
    # a helm order of the officer's drops the way, said once
    w.submit("steer S")
    w.run(60)
    assert nav.way_mark == "" and not nav.way
    dropped = [x for x in w.log if x.kind == "navigation.way"]
    assert len(dropped) == 1 and "the helm was given another course" in dropped[0].text
    # a plain course drops any way; a mark the chart has not got is refused
    w.submit("shape a course for Lisbon via Ushant")
    assert nav.way_mark
    w.submit("shape a course for the Lizard")
    assert not nav.way_mark
    refused = w.submit("shape a course for Lisbon via the moon")
    assert refused.kind == "order.rejected" and "names no mark of the chart" in refused.text


def test_an_intent_by_way_of_marks_gives_the_captain_the_legs(off_falmouth):
    w = off_falmouth
    intent = read_intent(w, "bound for Lisbon via Ushant, Finisterre")
    assert intent.kind == "passage" and intent.destination == "lisbon"
    assert intent.via == ("Ushant", "Finisterre")
    trade = read_intent(w, "trade tin from Falmouth to Lisbon via Ushant and Finisterre")
    assert trade.kind == "trade" and trade.via == ("Ushant", "Finisterre")
    assert trade.to_dict()["via"] == ["Ushant", "Finisterre"]
    legs = Planner(w).legs_for(intent, w.navigation.account_now(), "")
    via = [lg for lg in legs if lg.kind == "via"]
    assert [lg.words for lg in via] == [
        "5 miles north-west of Ushant",
        "5 miles south-west of Cape Finisterre",
    ]
    assert "leaving Ushant to larboard" in via[0].said
    assert legs[-1].words == "Lisbon" and legs[0].kind == "via"
    # with no via, the straight line as before: no routing
    plain = Planner(w).legs_for(read_intent(w, "bound for Lisbon"), w.navigation.account_now(), "")
    assert [lg.kind for lg in plain] == ["to"] or all(lg.kind != "via" for lg in plain)
    with pytest.raises(ValueError, match="names no mark of the chart"):
        read_intent(w, "bound for Lisbon via the moon")


# -- the frigate, Falmouth to Lisbon via Ushant and Finisterre, on the whole chart -----------

VIA_FRIGATE = {
    "name": "The frigate for Lisbon by way of Ushant and Finisterre",
    "seed": 7,
    "start": "1805-06-12T06:00",
    "position": "49 56 N 5 00 W",  # off Falmouth, clear of the Manacles' berth
    "region": "channel-west",
    "ship": {
        "file": "data/ships/frigate-36.yaml",
        "heading_deg": 190,
        "speed_kn": 4,
        "glass": True,
    },
    "wind": {"gustiness": 0.3, "variability": 0.3},
    "intent": "bound for Lisbon via Ushant, Finisterre",
    "orders": ["set plain sail"],
    "papers": {"chart": {"year": 1804}, "epitome": "norie", "almanac": 1805},
    "ports": ["falmouth", "brest", "corunna", "lisbon"],
    "weather": {
        "wind": [
            {"at": "1805-06-12T04:00", "from_deg": 300, "knots": 14, "air_mass": "neutral"},
            {"at": "1805-06-13T06:00", "from_deg": 330, "knots": 13},
            {"at": "1805-06-14T06:00", "from_deg": 10, "knots": 12},
        ],
        "background": {"hpa": 1020, "gradient_hpa_per_100km": 0.3, "high_toward_deg": 220},
        "systems": [
            {
                "name": "the old high over Biscay",
                "kind": "high",
                "radius_km": 900,
                "track": [
                    {"at": "1805-06-11T12:00", "x_km": 300, "y_km": -500, "hpa": 1024},
                    {"at": "1805-06-15T12:00", "x_km": 500, "y_km": -600, "hpa": 1022},
                ],
            }
        ],
        "sky": {"sky": "clear", "weather": "fine", "visibility": "the horizon"},
        "sea": True,
    },
}


@pytest.fixture(scope="module")
def frigate_via(tmp_path_factory) -> World:
    """Run until the Finisterre mark is passed, or four days."""
    import yaml

    p = tmp_path_factory.mktemp("via") / "via.yaml"
    p.write_text(yaml.safe_dump(VIA_FRIGATE), encoding="utf-8")
    sf = load_scenario(p)
    w = make_scenario_world(sf)
    begin(w, sf)
    for _ in range(4 * 24):
        w.run(3600)
        if any("Cape Finisterre passed" in e.text for e in w.log if e.kind == "captain.plan"):
            break
    return w


def test_the_frigate_passes_ushant_and_finisterre_on_their_hands_on_the_whole_chart(frigate_via):
    """Slow (tests/conftest.py): the captain's plan carries the two via legs; Ushant is
    passed to larboard five miles off, then Finisterre, each said in the log, the frigate
    never aground and the course between them the straight line (no routing)."""
    w = frigate_via
    assert w.chart.name == "atlantic-east"
    plans = [e for e in w.log if e.kind == "captain.plan"]
    assert any("5 miles north-west of Ushant" in e.text and "plan for" in e.text for e in plans)
    passed = [e.text for e in plans if " passed, leaving " in e.text]
    assert any("Ushant passed, leaving Ushant to larboard" in t for t in passed), passed
    finisterre = "Cape Finisterre passed, leaving Cape Finisterre to larboard"
    assert any(finisterre in t for t in passed), passed
    assert not [e for e in w.log if e.kind == "ship.aground"]
    assert w.position.lat_deg < 42.9
    assert w.captain.intent is not None and w.captain.intent.via == ("Ushant", "Finisterre")


def test_a_mark_is_passed_abeam_only_within_two_miles_of_it_or_of_its_line():
    """Package 43b, from package 44's regatta: a water mark far to windward was taken as
    passed abeam while she was miles from it, the bearing alone abaft the line's beam. A
    mark is passed only within two miles of it or of the line to it
    (`reckoning.WAY_PASSED_WITHIN_NM`)."""
    from freesail import units
    from freesail.world.geo import destination, off_the_line_m

    sf = load_scenario(FALMOUTH_LESSON)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(120)
    nav = w.navigation
    assert w.submit("shape a course for Lisbon via Ushant and Finisterre").kind == "helm.set"
    here = nav.account_now()
    nm = units.NAUTICAL_MILE
    # the mark ten miles south and ten east of her, its line running north from twenty
    # miles south of it: she lies ten miles off the line, the mark abaft its beam
    mark = destination(destination(here, 180.0, 10 * nm), 90.0, 10 * nm)
    nav.way_target = mark
    nav.way_from = destination(mark, 180.0, 20 * nm)
    assert off_the_line_m(nav.way_from, mark, here) > 9 * nm
    w.run(60)
    assert not [x for x in w.log if x.text.startswith("By the way shaped")]
    assert nav.way_mark == "5 miles north-west of Ushant"
    # within two miles of the line, the same mark abaft the beam is passed
    here = nav.account_now()
    mark = destination(here, 180.0, 10 * nm)
    nav.way_target = destination(mark, 90.0, 1 * nm)
    nav.way_from = destination(nav.way_target, 0.0, -20 * nm)
    w.run(60)
    said = [x for x in w.log if x.text.startswith("By the way shaped")]
    assert said and "5 miles north-west of Ushant passed abeam" in said[-1].text
