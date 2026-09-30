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
    assert lizard.text.startswith("The Lizard bearing N") and "distant three leagues" in lizard.text
    assert lizard.data["estimate"] == "three leagues" and lizard.data["relative"] == "right ahead"
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
