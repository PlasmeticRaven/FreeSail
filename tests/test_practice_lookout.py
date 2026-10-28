"""Practice at the great guns: the cask as the lookout has it (practice and resupply,
between packages 72 and 73; docs/design/Build-PracticeAndResupply.md §6, §8.1).

The cask is a sighting of its own kind ("cask", named "the mark"): made out by day within a
mile and the visibility, at twilight within half that, never by night; never hailed; told
once when it is lost to sight and once when it is made out again; judged from a stream of
its own ("practice"), opened at its first sighting so that no other draw moves; never
among the strangers, the land or the marks of a fix; answered by `find("the mark")`; and
named in the words of `what is in sight` beside a sail, never cut off by the land and the
chart's marks off a coast (the review's finding, in the owner's practice scenario).
"""

from __future__ import annotations

import re

from freesail import units
from freesail.combat import marks
from freesail.world.geo import destination
from tests.test_brains import world_at

FRIGATE = "data/ships/frigate-36.yaml"
NM = units.NAUTICAL_MILE


def frigate():
    w = world_at(49.5, -5.5, FRIGATE)
    w.run(60)
    return w


def kinds(w, kind):
    return [e for e in w.log if e.kind == kind]


def test_the_cask_is_made_out_within_a_mile_by_day_half_at_twilight_and_never_by_night():
    assert marks.seen_range_nm(None, "day") == marks.CASK_SEEN_DAY_NM == 1.0
    assert marks.seen_range_nm(5.0, "day") == 1.0
    assert marks.seen_range_nm(0.4, "day") == 0.4  # the haze
    assert marks.seen_range_nm(None, "twilight") == 0.5
    assert marks.seen_range_nm(0.4, "twilight") == 0.2
    assert marks.seen_range_nm(None, "night") == 0.0
    w = frigate()
    cask = marks.drop_cask(w, "starboard")
    cask.position = destination(w.position, 90.0, 0.8 * NM)
    seen = marks.sightings(w, w.position, None, "day")
    assert len(seen) == 1
    s = seen[0]
    assert s.seen_as == "cask" and s.feature.id == cask.id and s.feature.modern == cask.id
    assert s.feature.name == "the mark" and s.feature.height_m == marks.CASK_HEIGHT_M
    assert abs(s.distance_m - 0.8 * NM) < 1.0 and abs(s.bearing_deg - 90.0) < 0.5
    assert marks.sightings(w, w.position, 0.9, "day")
    assert marks.sightings(w, w.position, 0.5, "day") == []  # in the haze
    assert marks.sightings(w, w.position, None, "twilight") == []
    assert marks.sightings(w, w.position, None, "night") == []
    cask.position = destination(w.position, 90.0, 0.3 * NM)
    assert marks.sightings(w, w.position, None, "twilight")
    assert marks.sightings(w, w.position, None, "night") == []
    cask.gone = "lost"
    assert marks.sightings(w, w.position, None, "day") == []


def test_the_cask_is_never_hailed_and_the_sight_lines_are_said_once_each_way():
    w = frigate()
    n0 = len(w.log)
    cask = marks.drop_cask(w, "starboard")
    w.run(120)
    p = marks.practice_of(w.ship)
    assert marks.cask_in_sight(w, cask) and p.sight == "seen"
    hails = [e for e in w.log[n0:] if e.kind.startswith("lookout.")]
    assert not [e for e in hails if e.data.get("id") == cask.id or "mark" in e.text.lower()]
    assert not kinds(w, "practice.mark_sight")  # the first sighting says nothing
    # beyond the mile: lost to sight, once
    cask.position = destination(w.position, 200.0, 1.4 * NM)
    w.run(180)
    lost = kinds(w, "practice.mark_sight")
    assert [e.data["seen"] for e in lost] == [False]
    assert str(lost[0].severity) == "routine"
    assert lost[0].text == (
        "The mark is lost to sight, too far off to be made out from the masthead."
    )
    assert p.sight == "lost" and not marks.cask_in_sight(w, cask)
    # no gun lays for it while it is unseen
    from freesail.combat.action import target_of

    assert target_of(w, cask.id) is None
    # within it again: made out again, once
    cask.position = destination(w.position, 200.0, 0.3 * NM)
    w.run(180)
    sight = kinds(w, "practice.mark_sight")
    assert [e.data["seen"] for e in sight] == [False, True]
    # the distance as the lookout judges it, with the eye's error of the sighting
    assert re.fullmatch(
        r"The mark is made out again, bearing [NSEW by]+, about (?:a|one|two|three|four) "
        r"cables?\.",
        sight[1].text,
    ), sight[1].text
    assert target_of(w, cask.id) is not None
    # still no hail of it
    hails = [e for e in w.log[n0:] if e.kind == "lookout.sighting"]
    assert not [e for e in hails if e.data.get("id") == cask.id]


def test_the_cask_lost_in_the_haze_says_so():
    w = frigate()
    cask = marks.drop_cask(w, "starboard")
    w.run(120)
    cask.position = destination(w.position, 200.0, 0.6 * NM)
    w.conditions = _Haze(0.4)
    try:
        w.run(120)
    finally:
        w.conditions = None
    assert [e.text for e in kinds(w, "practice.mark_sight")] == [
        "The mark is lost to sight in the haze."
    ]


class _Haze:
    """The weather's visibility alone, for the lookout (`World.conditions` is None under a
    pinned wind; the look reads `visibility_nm` and nothing else of it here)."""

    def __init__(self, nm: float) -> None:
        self.visibility_nm = nm

    def __getattr__(self, name):
        raise AttributeError(name)


def test_the_practice_stream_opens_only_with_a_cask_and_moves_no_other_draw():
    a = frigate()
    b = frigate()
    a.run(300)
    assert "practice" not in a.rng.stream_names()
    marks.drop_cask(b, "starboard")
    assert "practice" not in b.rng.stream_names()  # nothing drawn at the drop
    b.run(300)
    assert "practice" in b.rng.stream_names()
    assert b.lookout._practice_stream is not None and a.lookout._practice_stream is None
    for name in a.rng.stream_names():
        assert a.rng.stream(name).getstate() == b.rng.stream(name).getstate(), name
    assert [e.text for e in a.log if e.kind.startswith("lookout.")] == [
        e.text for e in b.log if e.kind.startswith("lookout.")
    ]


def test_the_cask_is_no_stranger_no_land_no_mark_of_a_fix_and_is_found_as_the_mark():
    w = frigate()
    lookout = w.lookout
    assert lookout.find("the mark") is None  # no cask: the words keep their meaning
    cask = marks.drop_cask(w, "larboard")
    w.run(120)
    heading = float(w.ship.heading)
    assert not [i for i in lookout.strangers(w, heading)["items"] if i["id"] == cask.id]
    assert lookout.sail(heading)["count"] == 0
    land = lookout.land(heading)
    assert land["nearest"] is None or land["nearest"]["id"] != cask.id
    for words in ("the mark", "the cask", "the target", "mark"):
        found = lookout.find(words)
        assert found is not None and found.feature.id == cask.id, words
    items = [i for i in lookout.reading(heading)["items"] if i["id"] == cask.id]
    assert len(items) == 1 and items[0]["seen_as"] == "cask"
    # where it lies from her head (she swings as she lies), its bearing and its distance
    assert re.fullmatch(r"The mark [a-z ]+, bearing [NSEW by]+, distant [a-z ]+", items[0]["words"])
    # the marks a fix may be taken by are the chart's alone
    assert not [s for s in w.navigation._fix_marks() if s.feature.id == cask.id]
    cask.gone = "struck"
    w.run(60)
    assert lookout.find("the mark") is None


def test_what_is_in_sight_names_the_mark_off_the_lizard_in_the_practice_scenario():
    """The owner's scenario (data/scenarios/exercising-the-great-guns.yaml), five miles south
    of the Lizard on a clear forenoon, with some thirty-six things in sight: the cask hove
    over is named "the mark" among the eight the words name, beside a sail, ahead of the
    land and the chart's marks (the review's finding: it sorted last and fell into "and 28
    more in sight"); and it is still never hailed."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/exercising-the-great-guns.yaml")
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(120)
    hails = len(kinds(w, "lookout.sighting"))
    assert w.submit("heave a cask overboard").kind == "order.accepted"
    w.run(210)
    cask = marks.cask_in_water(w.ship)
    assert cask is not None and marks.cask_in_sight(w, cask)
    v = w.readings.value("in_sight")
    assert v["count"] > 8 + 1, v["count"]  # more in sight than the words name
    assert v["words"].startswith("the mark "), v["words"]
    assert re.search(r"; and \d+ more in sight$", v["words"]), v["words"]
    assert not [e for e in kinds(w, "lookout.sighting")[hails:] if e.data.get("id") == cask.id]


def test_a_bearing_of_the_cask_is_said_and_moves_nothing_of_the_reckoning():
    # the review's finding, mended by the lead at the merge: `Navigation.take_bearing`
    # (world/reckoning.py) spares the cask from moving the account, as it spares a sail
    w = frigate()
    cask = marks.drop_cask(w, "starboard")
    w.run(120)
    assert marks.cask_in_sight(w, cask)
    r = w.navigation.reckoning
    before = (r.lat_deg, r.lon_deg, len(r.bearings))
    answer = w.submit("take a bearing of the mark")
    assert answer.kind == "bearing.taken" and answer.text.startswith("The mark bore ")
    taken = kinds(w, "bearing.taken")[-1]
    assert taken.data["moved_nm"] == 0.0
    assert (r.lat_deg, r.lon_deg, len(r.bearings)) == before
