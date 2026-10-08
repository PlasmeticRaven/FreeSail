"""Package 32: the lookout (spec M5 §12).

The lookout's words (by compass bearing and an estimated distance, never the truth to a
cable; a light is "a light"); the height of eye at the topmast head; a landfall notable
and a danger notable, the rest routine, a feature not hailed twice in half an hour, the
land lost said once; the reading `what is in sight` and `the land` through the registry
and the snapshot; nothing on the plane.
"""

from __future__ import annotations

import math
from datetime import datetime

from freesail import units
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario
from freesail.world import lookout as L
from freesail.world.chart import Feature, Sighting, load_chart
from freesail.world.geo import Position, destination

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
LIZARD = Position(49.9594, -5.2067)


def chart_world(
    pos: Position,
    ship: str = FRIGATE,
    heading: float = 0.0,
    start: datetime = datetime(1805, 6, 1, 10, 0),
):
    sc = Scenario(
        start_time=start,
        wind_from_deg=270.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position=pos.to_dict(),
        region="channel-west",
    )
    return make_world(7, ship, sc)


def test_the_lookouts_words_are_a_compass_bearing_and_an_estimate():
    lizard = Feature("lizard-point", "headland", "the Lizard", 49.9594, -5.2067, height_m=60)
    s = Sighting(lizard, bearing_deg=11.25, distance_m=12.3 * units.NAUTICAL_MILE, seen_as="land")
    assert L.Lookout.words(s, heading_rad=0.0) == "The Lizard bearing N by E, distant four leagues."
    light = Feature(
        "st-agnes-light", "light", "St Agnes light", 49.8933, -6.3453, lit={"from": 1680}
    )
    s = Sighting(light, bearing_deg=326.0, distance_m=14.0 * units.NAUTICAL_MILE, seen_as="light")
    assert L.Lookout.words(s, heading_rad=0.0) == "A light on the larboard bow, bearing NW by N."
    rock = Feature("the-manacles", "ledge", "the Manacles", 50.047, -5.044)
    s = Sighting(rock, bearing_deg=90.0, distance_m=0.3 * units.NAUTICAL_MILE, seen_as="danger")
    assert (
        L.Lookout.words(s, heading_rad=0.0)
        == "The Manacles bearing E, distant three cables: a danger."
    )


def test_where_a_thing_lies_from_the_ships_head():
    p = units.POINT
    assert L.relative_words(0.5 * p) == "right ahead"
    assert L.relative_words(3 * p) == "on the starboard bow"
    assert L.relative_words(-3 * p) == "on the larboard bow"
    assert L.relative_words(8 * p) == "abeam to starboard"
    assert L.relative_words(-12 * p) == "on the larboard quarter"
    assert L.relative_words(math.pi) == "right astern"


def test_the_height_of_eye_is_the_topmast_head_and_falls_with_the_topmast():
    w = chart_world(Position(49.80, -5.20))
    eye = L.height_of_eye(w.ship)
    assert 34.0 < eye < 38.0  # the frigate's deck, main mast and main topmast
    w.submit("send down the topgallant masts")
    assert L.height_of_eye(w.ship) == eye  # the topgallants are above the lookout
    w.ship.spars["main.topmast"].sent_down = True
    lower = L.height_of_eye(w.ship)
    assert 30.0 < lower < eye  # the fore topmast head now
    assert L.height_of_eye(object()) == L.DEFAULT_HEIGHT_OF_EYE_M
    schooner = chart_world(Position(49.80, -5.20), ship=SCHOONER)
    assert 25.0 < L.height_of_eye(schooner.ship) < 32.0


def test_a_landfall_is_notable_the_reading_carries_it_and_the_land_lost_is_said_once():
    ten_south = destination(LIZARD, 180.0, 10 * units.NAUTICAL_MILE)
    w = chart_world(ten_south, heading=0.0)
    w.submit("set plain sail")
    w.run(120)
    sightings = [e for e in w.log if e.kind == "lookout.sighting"]
    assert sightings, "nothing sighted ten miles south of the Lizard by day"
    first = sightings[0]
    assert first.severity is Severity.NOTABLE and first.data["landfall"] is True
    assert any(e.data["id"] == "lizard-point" for e in sightings)
    lizard = next(e for e in sightings if e.data["id"] == "lizard-point")
    # the distance by estimation is the lookout's eye, drawn once a sighting episode
    # (package 33b): at seed 7 he judges the Lizard, ten miles off, four leagues
    assert lizard.text.startswith("The Lizard bearing N") and "distant four leagues" in lizard.text
    assert lizard.data["estimate"] == "four leagues" and lizard.data["relative"] == "right ahead"
    assert abs(lizard.data["distance_m"] - 10 * units.NAUTICAL_MILE) < 300.0  # the truth kept
    r = w.readings
    assert r["land"]["in_sight"] is True and r["land"]["words"] == "in sight"
    assert r["in_sight"]["count"] == len(w.lookout.sightings) >= 1
    assert "the Lizard bearing N" in r["in_sight"]["words"]
    assert r.words("land") == "in sight"
    # the same feature is not hailed again within half an hour
    w.run(600)
    assert (
        len([e for e in w.log if e.kind == "lookout.sighting" and e.data["id"] == "lizard-point"])
        == 1
    )
    # the land lost: she is put far to sea and the next look says so once
    w._position = Position(49.0, -6.0)
    w._geo_last = (w.ship_x, w.ship_y)
    w.run(120)
    lost = [e for e in w.log if e.kind == "lookout.lost"]
    assert len(lost) == 1 and lost[0].text == "The land is out of sight."
    assert (
        w.readings["land"]["in_sight"] is False
        and w.readings.words("in_sight") == "nothing in sight"
    )
    assert "Nothing in sight." in w.summary_lines()


def test_at_night_a_light_is_a_light_and_the_lookout_does_not_name_it():
    ten_south = destination(LIZARD, 180.0, 10 * units.NAUTICAL_MILE)
    w = chart_world(ten_south, heading=0.0, start=datetime(1805, 6, 1, 23, 30))
    assert w.daylight == "night"
    w.run(60)
    sightings = [e for e in w.log if e.kind == "lookout.sighting"]
    assert sightings and all(e.data["seen_as"] == "light" for e in sightings)
    assert sightings[0].text.startswith("A light ") and "Lizard" not in sightings[0].text
    assert sightings[0].data["id"] == "lizard-lights" and sightings[0].data["landfall"] is True


def test_the_lookout_looks_at_the_start_then_once_a_minute_and_the_plane_has_no_lookout():
    w = chart_world(destination(LIZARD, 180.0, 10 * units.NAUTICAL_MILE))
    assert w.lookout is not None and w.lookout.sightings  # the first look, at the start
    hailed = [e for e in w.log if e.kind == "lookout.sighting"]
    assert hailed and hailed[0].tick == 0
    w._position = destination(LIZARD, 180.0, 9 * units.NAUTICAL_MILE)
    w._geo_last = (w.ship_x, w.ship_y)
    before = [s.distance_m for s in w.lookout.sightings]
    w.run(59)
    assert [s.distance_m for s in w.lookout.sightings] == before  # no look until the minute
    w.run(1)
    assert [s.distance_m for s in w.lookout.sightings] != before
    plain = make_world(7, SCHOONER, Scenario(gustiness=0.0, variability=0.0))
    assert plain.lookout is None and plain.readings["in_sight"] is None
    chart = load_chart("channel-west")
    assert L.Lookout(chart).look(plain) == []


# ---------------------------------------------------------------------------
# Package 37d: the distance judged afresh, the shore always a sighting, land ahead (the
# review of gate 5c's playtests, 5.1). The ship here is the point ship put where the test
# wants her a minute at a time, so each look's distance is exact and the stream sets
# nothing; the lookout reads her true motion from one look to the next.
# ---------------------------------------------------------------------------

PENLEE = Position(50.319, -4.1909)  # the chart's Penlee Point, some 300 metres inland
OFF_PENLEE = 200.0  # the bearing a ship stands in from here: SSW of the point


def point_ship_world(pos: Position, heading: float = 20.0, start=datetime(1805, 6, 19, 10, 0)):
    from freesail.core.world import World

    sc = Scenario(
        start_time=start,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position=pos.to_dict(),
        region="channel-west",
    )
    return World(seed=7, scenario=sc)


def look_from(w, pos: Position, minutes: int = 1):
    """Put her at `pos` so many minutes on and have the lookout look: its lines."""
    for _ in range(60 * minutes):
        w.clock.advance()
    w._position = pos
    w._geo_last = (w.ship_x, w.ship_y)
    lines = w.lookout.look(w)
    for severity, kind, text, data in lines:
        w.record(severity, kind, text, data=data)
    return lines


def off_the_shore(metres: float, bearing: float = OFF_PENLEE) -> Position:
    """A place so far to seaward of the shore under Penlee Point, on `bearing` from it."""
    chart = load_chart("channel-west")
    foot = destination(PENLEE, bearing, 150.0)
    for _ in range(200):
        shore = chart.nearest_shore(foot)
        if shore is not None and shore.distance_m >= 30.0:
            break
        foot = destination(foot, bearing, 15.0)
    return destination(foot, bearing, metres - chart.nearest_shore(foot).distance_m)


def test_the_lookout_judges_a_distance_afresh_as_she_stands_in_from_a_league_to_two_cables():
    """Item 5: the Harpy was told "Penlee Point ... a mile" at under two cables, the
    estimate being held until the ship herself had run a mile. Standing in from a league
    the list, a bearing's words and the reading follow her in, each a figure within the
    eye's error of the truth; the eye's error is the sighting's own throughout."""
    nm = units.NAUTICAL_MILE
    w = point_ship_world(off_the_shore(3.0 * nm))
    first = w.lookout.find("Penlee Point")
    assert first is not None and "three miles" in L.Lookout.words(first, 0.0)
    factor = w.lookout._episodes["penlee-point"].factor
    said = []
    for cables in (25, 20, 15, 10, 8, 6, 5, 4, 3, 2):
        look_from(w, off_the_shore(cables * units.CABLE))
        s = w.lookout.find("Penlee Point")
        # judged afresh whenever the truth is a tenth off the last judging: never staler
        assert abs(s.estimate_m / (s.distance_m * factor) - 1.0) <= L.ESTIMATE_REFRESH_FRACTION
        assert w.lookout._episodes["penlee-point"].factor == factor  # the same eye
        listed = next(i for i in w.lookout.reading(0.0)["items"] if i["id"] == "penlee-point")
        bearing = w.navigation.bearing_reading("Penlee Point")
        assert listed["estimate"] == bearing["estimate"] == L.estimate_words(s.estimate_m)
        said.append(listed["estimate"])
    assert said[0] in ("two miles", "three miles") and said[-1].endswith("cables")
    assert len(set(said)) >= 6, said  # it follows her in
    text, data = w.navigation.take_bearing("Penlee Point")
    assert f", {said[-1]} by estimation" in text and data["estimate"] == said[-1]
    # one hail of the point for the whole approach, as before
    hails = [x for x in w.log if x.kind == "lookout.sighting" and x.data["id"] == "penlee-point"]
    assert len(hails) == 1


def test_an_hour_of_calm_leaves_the_figure_as_it_was():
    """Item 5: a calm re-draws nothing, since nothing has changed and the error is the
    sighting's (playtest 13: the Start at four miles, four leagues and three leagues in an
    hour of calm)."""
    where = off_the_shore(2.0 * units.NAUTICAL_MILE)
    w = point_ship_world(where)
    first = {s.feature.id: s.estimate_m for s in w.lookout.sightings}
    assert "penlee-point" in first and L.SHORE_ID in first
    draws = w.rng.stream("lookout").getstate()
    for minute in range(60):
        # she lies becalmed, swinging a few yards about her place
        look_from(w, destination(where, 90.0 * (minute % 4), 20.0))
    assert {s.feature.id: s.estimate_m for s in w.lookout.sightings} == first
    assert w.rng.stream("lookout").getstate() == draws  # nothing drawn again


def test_a_sail_whose_distance_halves_is_said_nearer_and_the_closing_hail_is_fresh():
    """Item 5, for a sail and for the closing hail: a cutter stood at "two miles" for 37
    minutes while her bearing swung from S to NW by N; "steady and closing" carried the
    distance of the first look."""
    from freesail.world.chart import Feature, Sighting

    w = point_ship_world(off_the_shore(3.0 * units.NAUTICAL_MILE))
    look = w.lookout
    cutter = Feature("sail:cutter", "sail", "a sail", 50.2, -4.2)

    def judged(distance_m: float, minute: int):
        s = Sighting(cutter, 180.0, distance_m, "sail")
        return look._judge(s, w.position, minute, new_episode=minute == 0).estimate_m

    far = judged(4000.0, 0)
    assert judged(3800.0, 1) == far  # within a tenth: held
    near = judged(2000.0, 2)
    assert near == far / 2.0 and L.estimate_words(near) != L.estimate_words(far)
    # the closing hail: Penlee Point steady on the bow, the distance a fifth less and more
    look_from(w, off_the_shore(2.9 * units.NAUTICAL_MILE))
    for step in range(1, 12):
        lines = look_from(w, off_the_shore((2.9 - 0.08 * step) * units.NAUTICAL_MILE))
    closing = [e for e in w.log if e.kind == "lookout.closing" and e.data["id"] == "penlee-point"]
    assert len(closing) == 1
    s = look.find("Penlee Point")
    truth_then = closing[0].data["distance_m"]
    factor = look._episodes["penlee-point"].factor
    assert abs(closing[0].data["estimate_m"] / (truth_then * factor) - 1.0) <= 0.1
    assert closing[0].data["estimate"] in closing[0].text and s is not None
    assert lines is not None


def test_the_shore_is_a_sighting_at_every_look_within_its_limits_and_hailed_once():
    """Item 9: off any named coast the nearest land was never spoken of, the shore being
    looked for only when no headland of the chart was in sight. It is a sighting at every
    look within a league, the visibility and the night's mile; hailed once a sighting;
    and no mark to take a bearing of."""
    from types import SimpleNamespace

    nm = units.NAUTICAL_MILE
    w = point_ship_world(off_the_shore(2.0 * nm))
    ids = {s.feature.id for s in w.lookout.sightings}
    assert {"penlee-point", "rame-head", L.SHORE_ID} <= ids
    shore = next(s for s in w.lookout.sightings if s.feature.id == L.SHORE_ID)
    truth = load_chart("channel-west").nearest_shore(w.position)
    assert shore.distance_m == truth.distance_m and shore.bearing_deg == truth.bearing_deg
    assert shore.feature.name.startswith("the land about ")
    hail = [e for e in w.log if e.kind == "lookout.sighting" and e.data["id"] == L.SHORE_ID]
    assert len(hail) == 1 and hail[0].text.startswith("The land about ")
    assert "close aboard" not in hail[0].text and hail[0].data["estimate_m"] >= nm
    assert f"distant {hail[0].data['estimate']}." in hail[0].text
    for cables in (15, 10, 5, 3):
        look_from(w, off_the_shore(cables * units.CABLE))
    hail = [e for e in w.log if e.kind == "lookout.sighting" and e.data["id"] == L.SHORE_ID]
    assert len(hail) == 1  # hailed once
    shore = next(s for s in w.lookout.sightings if s.feature.id == L.SHORE_ID)
    assert "close aboard" in L.Lookout.words(shore, 0.0)
    # `take a bearing of the land` still means the nearest mark, and the shore is refused
    assert w.lookout.find("the land").feature.id != L.SHORE_ID
    assert w.lookout.find("the land about Penlee Point") is None
    # beyond a league there is none; in fog it shows within the visibility alone; at
    # night within a mile
    look_from(w, destination(PENLEE, 180.0, 5.0 * nm), minutes=40)
    assert L.SHORE_ID not in {s.feature.id for s in w.lookout.sightings}
    w.conditions = SimpleNamespace(visibility_nm=0.1)
    look_from(w, off_the_shore(3.0 * units.CABLE), minutes=40)
    assert L.SHORE_ID not in {s.feature.id for s in w.lookout.sightings}
    look_from(w, off_the_shore(0.8 * units.CABLE))
    assert [s.feature.id for s in w.lookout.sightings] == [L.SHORE_ID]
    night = point_ship_world(off_the_shore(1.5 * nm), start=datetime(1805, 6, 26, 1, 0))
    assert night.daylight == "night" and not night.lookout.moonlit
    assert L.SHORE_ID not in {s.feature.id for s in night.lookout.sightings}
    look_from(night, off_the_shore(0.8 * nm))
    assert L.SHORE_ID in {s.feature.id for s in night.lookout.sightings}


def _ahead(w):
    return [e for e in w.log if e.kind == "lookout.land_ahead"]


def stand_in(w, from_m: float, to_m: float, knots: float = 4.0, bearing: float = OFF_PENLEE):
    """Stand in for the shore under Penlee Point at `knots`, a look a minute, from so far
    off to so far off; the minutes run."""
    step = units.knots_to_ms(knots) * 60.0
    d = from_m
    n = 0
    while d > to_m:
        d -= step
        look_from(w, off_the_shore(d, bearing))
        n += 1
    return n


def test_land_ahead_is_notable_under_ten_minutes_and_urgent_under_four_each_once():
    """Item 10: steered at Penlee Point at four knots from a mile, the notable line comes
    about two thirds of a mile off and the urgent one under three cables, each once; the
    words say where it lies from her head, its distance by estimation and the time."""
    nm = units.NAUTICAL_MILE
    w = point_ship_world(off_the_shore(1.05 * nm), heading=OFF_PENLEE - 180.0)
    stand_in(w, 1.05 * nm, 0.6 * units.CABLE)
    lines = _ahead(w)
    assert [e.severity for e in lines] == [Severity.NOTABLE, Severity.URGENT]
    notable, urgent = lines
    factor = w.lookout._episodes[L.SHORE_ID].factor
    # ten minutes at four knots is two thirds of a mile, four is under three cables
    assert 9.0 <= notable.data["minutes"] < 10.0 and 3.0 <= urgent.data["minutes"] < 4.0
    assert 0.55 * nm < notable.data["estimate_m"] / factor < 0.67 * nm
    assert urgent.data["estimate_m"] / factor < 3.0 * units.CABLE
    where = {"right ahead": "right ahead"}.get(
        notable.data["relative"], f"ahead, {notable.data['relative']}"
    )
    assert notable.text == f"Land {where}, {notable.data['estimate']}: she is standing into it."
    close = {"right ahead": "close ahead"}.get(
        urgent.data["relative"], f"close ahead, {urgent.data['relative']}"
    )
    assert urgent.text == (
        f"Land {close}, {urgent.data['estimate']}! She will be on it in three minutes."
    )
    assert notable.data["relative"] in (
        "right ahead",
        "fine on the larboard bow",
        "fine on the starboard bow",
    )
    assert notable.data["what"] == "land" and not notable.data["urgent"] and urgent.data["urgent"]
    assert "distance_m" not in notable.data  # by estimation: the truth is in no line
    # the events for a stand-by and a book
    from freesail.api import readings as R

    kinds = [
        [
            name
            for name in ("land ahead", "land close ahead")
            if R.event_matches(R.EVENTS[name], e.kind, e.data)
        ]
        for e in lines
    ]
    assert kinds == [["land ahead"], ["land close ahead"]]


def test_land_ahead_comes_again_after_the_quiet_and_not_at_anchor_without_way_or_in_fog():
    """Item 10: turned away and brought back after the quiet, the lines come again; at
    anchor, hove to without way and in fog, nothing; at night only within the mile."""
    from types import SimpleNamespace

    nm = units.NAUTICAL_MILE
    w = point_ship_world(off_the_shore(1.0 * nm), heading=OFF_PENLEE - 180.0)
    stand_in(w, 1.0 * nm, 2.0 * units.CABLE)
    assert len(_ahead(w)) == 2
    # turned away: four looks standing off are not yet the quiet, the fifth is
    d = 2.0 * units.CABLE
    for look in range(L.LAND_AHEAD_CLEAR_LOOKS):
        d += units.knots_to_ms(4.0) * 60.0
        look_from(w, off_the_shore(d))
        assert w.lookout._ahead_notable is (look < L.LAND_AHEAD_CLEAR_LOOKS - 1)
    stand_in(w, d + 0.6 * nm, 2.0 * units.CABLE)
    assert [e.severity for e in _ahead(w)] == [Severity.NOTABLE, Severity.URGENT] * 2
    # at anchor or aground she is standing into nothing
    riding = point_ship_world(off_the_shore(1.0 * nm), heading=OFF_PENLEE - 180.0)
    riding.ship.extra = {"aground": True}
    stand_in(riding, 1.0 * nm, 2.0 * units.CABLE)
    assert _ahead(riding) == []
    # hove to without way: a quarter of a knot of drift is no way on
    drifting = point_ship_world(off_the_shore(3.0 * units.CABLE), heading=OFF_PENLEE - 180.0)
    stand_in(drifting, 3.0 * units.CABLE, 2.0 * units.CABLE, knots=0.25)
    assert _ahead(drifting) == []
    # in fog the lookout is silent and the lead is the guard: nothing beyond a cable
    fog = point_ship_world(off_the_shore(1.0 * nm), heading=OFF_PENLEE - 180.0)
    fog.conditions = SimpleNamespace(visibility_nm=0.1)
    stand_in(fog, 1.0 * nm, 2.0 * units.CABLE)
    assert _ahead(fog) == []
    # at night only within the mile: at eight knots from a league the land is under ten
    # minutes off at a mile and a third, and nothing is said until the mile
    night = point_ship_world(
        off_the_shore(3.0 * nm), heading=OFF_PENLEE - 180.0, start=datetime(1805, 6, 26, 1, 0)
    )
    assert night.daylight == "night" and not night.lookout.moonlit
    stand_in(night, 3.0 * nm, 0.9 * nm, knots=8.0)
    said = _ahead(night)
    assert len(said) == 1 and said[0].severity is Severity.NOTABLE
    assert said[0].data["estimate_m"] / night.lookout._episodes[L.SHORE_ID].factor <= 1.0 * nm
    day = point_ship_world(off_the_shore(3.0 * nm), heading=OFF_PENLEE - 180.0)
    stand_in(day, 3.0 * nm, 1.2 * nm, knots=8.0)
    assert len(_ahead(day)) == 1  # by day at a mile and a third, as soon as it is ten minutes


def test_a_danger_ahead_is_named_and_where_it_lies_is_said_from_her_head():
    """Item 10's words: a danger by its name; fine on the bow when her head is off her
    course made good."""
    assert L.ahead_words(0.0) == "right ahead"
    assert L.ahead_words(units.POINT) == "fine on the starboard bow"
    assert L.ahead_words(-1.5 * units.POINT) == "fine on the larboard bow"
    assert L.ahead_words(3 * units.POINT) == "on the starboard bow"
    chart = load_chart("channel-west")
    rock = chart.find_feature("the Black Rock")  # in Falmouth's mouth: it dries ten feet
    assert rock is not None and rock.kind == "drying"
    start = destination(rock.position, 180.0, 0.85 * units.NAUTICAL_MILE)
    w = point_ship_world(start, heading=10.0)  # her head a point off her course made good
    w.tide_state = None  # the water at the chart's datum: the rock shows
    for step in range(1, 9):
        look_from(w, destination(start, 0.0, step * units.knots_to_ms(4.0) * 60.0))
        if _ahead(w):
            break
    first = _ahead(w)[0]
    assert first.data["what"] == "danger" and first.data["id"] == rock.id
    assert first.text.startswith("The Black Rock ahead, fine on the larboard bow, ")
    assert first.text.endswith(": she is standing into danger.")
