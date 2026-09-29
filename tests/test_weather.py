"""Package 30: weather systems, the glass and the sky (spec M5 §2, §3, §5; the study
docs/design/WeatherSystems.md).

The systems' arithmetic (a single low's wind against the gradient rule, the fronts'
geometry, the sector table); the seeding from the climatology (deterministic, drawing
only at a system's birth, nothing while a scripted system is present); the scenario's
`systems` beside `wind` (the pinned wind winning); the readings on both ships with their
absent patterns; the log's lines and the roll-up; the dialect reading the glass and the
sky for nothing. The behavioural truths 52 to 55 and 57 are in test_known_truths.py.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

import pytest

from freesail import units
from freesail.api import queries
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core import events
from freesail.core.events import Event, Severity
from freesail.core.rng import Rng
from freesail.core.world import Scenario, World
from freesail.standing.grammar import parse_condition
from freesail.world import weather as W
from freesail.world.scenarios import ScenarioError, load_scenario, make_scenario_world
from freesail.world.weather import Glass, Weather, load_climatology

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
GATE_DAY = "data/scenarios/gate-4c-day.yaml"
T0 = datetime(1805, 6, 1, 4, 0)


def low(
    name: str = "the low",
    x: float = 0.0,
    y: float = 500.0,
    hpa: float = 985.0,
    radius: float = 500.0,
    warm: float = 135.0,
    cold: float = 225.0,
    at: datetime = T0,
) -> dict:
    return {
        "name": name,
        "kind": "low",
        "radius_km": radius,
        "fronts": {"warm_deg": warm, "cold_deg": cold},
        "track": [{"at": at.isoformat(), "x_km": x, "y_km": y, "hpa": hpa}],
    }


def high(x: float = 0.0, y: float = 500.0, hpa: float = 1030.0, radius: float = 1000.0) -> dict:
    return {
        "name": "the high",
        "kind": "high",
        "radius_km": radius,
        "track": [{"at": T0.isoformat(), "x_km": x, "y_km": y, "hpa": hpa}],
    }


def weather_with(*systems: dict, **kw) -> Weather:
    return Weather(T0, None, seed=7, systems=list(systems), **kw)


def gate_systems() -> Scenario:
    """The gate's day's systems without its pinned wind: the day as a system."""
    sc = load_scenario(GATE_DAY).scenario
    return Scenario(
        name="the gate's day as a system",
        start_time=sc.start_time,
        gustiness=sc.gustiness,
        variability=sc.variability,
        latitude_deg=sc.latitude_deg,
        systems=sc.systems,
        background=sc.background,
        glass=True,
    )


# -- the systems' arithmetic ------------------------------------------------------------


def test_a_single_lows_wind_follows_the_gradient_rule():
    """A low of 985 hPa, 500 km to the north, 500 km across: at the ring (one radius from
    the centre, where a Gaussian bell's gradient is greatest) the gradient is |A| e^-1/2 / R,
    the geostrophic wind 7.2 m/s a hectopascal a hundred kilometres turned ninety degrees
    with low pressure on its left, capped by the cyclonic gradient-wind rule; the surface
    wind is that turned fifteen degrees toward the centre and scaled by 0.7."""
    w = weather_with(low(x=0, y=500, hpa=985, radius=500))
    anomaly, radius = 30.0, 500.0
    g = anomaly * math.exp(-0.5) / radius  # hPa/km at the ring
    vg = W.GEOSTROPHIC_MS_PER_HPA_PER_100KM * g * 100.0
    r = radius * 1000.0
    vgr = 2.0 * vg / (1.0 + math.sqrt(1.0 + 4.0 * vg / (W.CORIOLIS_50N * r)))
    vx, vy = w.geostrophic_at(0.0, 0.0)
    assert vy == pytest.approx(0.0, abs=1e-9)
    assert vx == pytest.approx(vgr)  # blowing east: a westerly south of a low
    assert vgr < vg, "the cap in curvature makes the flow subgeostrophic"
    direction, speed = w.surface_wind_at(0.0, 0.0)
    assert speed == pytest.approx(W.SURFACE_SCALE * vgr)
    assert units.rad_to_deg(direction) == pytest.approx(270.0 - W.SURFACE_TURN_DEG)
    # round the centre the geostrophic wind circles anticlockwise
    for (x, y), toward in (((500, 500), 0.0), ((0, 1000), 270.0), ((-500, 500), 180.0)):
        vx, vy = w.geostrophic_at(x, y)
        assert units.rad_to_deg(units.vector_heading(vx, vy)) == pytest.approx(toward, abs=1e-6)
    # the pressure: the anomaly at the centre, the bell at the ring, the background far off
    assert w.pressure_at(0.0, 500.0) == pytest.approx(985.0)
    assert w.pressure_at(0.0, 0.0) == pytest.approx(1015.0 - 30.0 * math.exp(-0.5))
    assert w.pressure_at(0.0, -4000.0) == pytest.approx(1015.0, abs=1e-6)


def test_a_high_turns_the_other_way_and_is_capped_near_its_centre():
    w = weather_with(high(x=0, y=500, hpa=1030, radius=1000))
    direction, speed = w.surface_wind_at(0.0, 0.0)
    # south of a high the geostrophic wind is from the east; turned toward low pressure
    # (away from the high, to the left of the flow) it is from east by north
    assert units.rad_to_deg(direction) == pytest.approx(90.0 - W.SURFACE_TURN_DEG)
    assert units.ms_to_knots(speed) == pytest.approx(6.5, abs=0.5)
    assert w.sector_at(0.0, 0.0).sector == "high"
    # a strong high a hundred kilometres off: the anticyclonic bound f r / 4
    near = weather_with(high(x=0, y=100, hpa=1055, radius=1000))
    cap = W.CORIOLIS_50N * 100_000.0 / 4.0
    assert math.hypot(*near.geostrophic_at(0.0, 0.0)) <= cap + 1e-9


def test_the_fronts_hinge_at_the_centre_and_turn_until_the_low_occludes():
    """The warm sector is the wedge from the warm front's bearing clockwise to the cold
    front's; the fronts turn cyclonically, the cold front faster, and the low occludes
    when it catches the warm front (W §1.3)."""
    w = weather_with(low(x=0, y=500, warm=135, cold=225))
    assert w.sector_at(0.0, 0.0).sector == "warm"  # due south
    assert w.sector_at(500.0, 500.0).sector == "ahead"  # due east
    assert w.sector_at(-500.0, 500.0).sector == "behind"  # due west
    assert w.sector_at(0.0, 1000.0).sector == "ahead"  # due north: the nearer front's side
    warm0, cold0, occluded = w.systems[0].fronts_at(T0)
    assert (warm0, cold0, occluded) == (135.0, 225.0, False)
    later = T0 + timedelta(hours=10)
    warm, cold, occluded = w.systems[0].fronts_at(later)
    assert warm == pytest.approx(135.0 - 10 * W.WARM_FRONT_TURN_DEG_PER_H)
    assert cold == pytest.approx(225.0 - 10 * W.COLD_FRONT_TURN_DEG_PER_H)
    assert not occluded
    closing = W.COLD_FRONT_TURN_DEG_PER_H - W.WARM_FRONT_TURN_DEG_PER_H
    when = T0 + timedelta(hours=90.0 / closing + 0.5)
    warm, cold, occluded = w.systems[0].fronts_at(when)
    assert occluded and cold == warm
    w.advance(when)
    assert w.sector_at(0.0, 0.0, when).sector != "warm"
    # a point a hundred kilometres ahead of the warm front, which runs south-east from the
    # centre: its distance to the front, and the backing it gets (two points at the front)
    along, across = 400.0, 100.0
    x = along * math.sin(math.radians(135)) + across * math.sin(math.radians(45))
    y = 500.0 + along * math.cos(math.radians(135)) + across * math.cos(math.radians(45))
    w = weather_with(low(x=0, y=500, warm=135, cold=225))
    sec = w.sector_at(x, y)
    assert sec.sector == "ahead" and sec.to_warm_km == pytest.approx(across, abs=1e-6)
    assert sec.veer_deg == pytest.approx(
        -W.WARM_FRONT_VEER_DEG * (1 - across / W.WARM_FRONT_APPROACH_KM)
    )
    # and thirty kilometres behind the cold front, which runs south-west: the veer, fading
    x = along * math.sin(math.radians(225)) + 30.0 * math.sin(math.radians(315))
    y = 500.0 + along * math.cos(math.radians(225)) + 30.0 * math.cos(math.radians(315))
    sec = w.sector_at(x, y)
    assert sec.sector == "behind" and sec.to_cold_km == pytest.approx(30.0, abs=1e-6)
    assert sec.veer_deg == pytest.approx(
        W.COLD_FRONT_VEER_DEG * (1 - 30.0 / W.COLD_FRONT_VEER_FADE_KM)
    )
    assert sec.air_mass == "unstable"


def test_the_sector_table_gives_the_sky_the_weather_the_visibility_and_the_air_mass():
    """W §1.3's sequence as the readings' words: ahead of the warm front the sky thickens
    and rain sets in; the warm sector is overcast or hazy with drizzle, stable air; behind
    the cold front squalls, then showers between hard-edged clouds in unstable air; under a
    high, clear; open sea between systems, fine."""
    w = weather_with(low(x=0, y=500, warm=135, cold=225))

    def point(bearing: float, along: float, side: float, across: float) -> tuple[float, float]:
        return (
            along * math.sin(math.radians(bearing)) + across * math.sin(math.radians(side)),
            500.0 + along * math.cos(math.radians(bearing)) + across * math.cos(math.radians(side)),
        )

    far = w.conditions_at(900.0, 700.0)
    assert far.sector == "ahead" and far.sky in ("clear", "detached clouds")
    assert (far.weather, far.visibility, far.air_mass) == ("fine", "the horizon", "neutral")
    near = w.conditions_at(*point(135, 400, 45, 100))
    assert near.sector == "ahead" and near.weather == "rain"
    assert near.sky in ("overcast", "dark and gloomy") and near.visibility in (
        "a few miles",
        "a mile",
    )
    warm = w.conditions_at(0.0, 0.0)
    assert warm.sector == "warm" and warm.air_mass == "warm"
    assert warm.sky in ("overcast", "hazy") and warm.weather in ("drizzle", "fine")
    squally = w.conditions_at(*point(225, 400, 315, 30))
    assert squally.sector == "behind" and squally.air_mass == "unstable"
    assert squally.sky == "dark and gloomy" and squally.weather in ("squally", "thunder")
    assert squally.visibility == "a mile" and squally.visibility_nm == 1.0
    showers = w.conditions_at(*point(225, 400, 315, 300))
    assert showers.air_mass == "unstable" and showers.sky == "detached clouds"
    assert showers.signs == W.SKY_SIGNS["hard edged"]
    assert showers.weather in ("passing showers", "fine")
    under = weather_with(high(x=0, y=300)).conditions_at(0.0, 0.0)
    assert under.sector == "high" and under.sky in ("clear", "hazy") and under.weather == "fine"
    open_sea = Weather(T0, None, seed=7).conditions_at(0.0, 0.0)
    assert (open_sea.sector, open_sea.weather, open_sea.visibility) == (
        "open",
        "fine",
        "the horizon",
    )
    assert open_sea.sky in ("clear", "detached clouds") and open_sea.air_mass == "neutral"
    assert open_sea.pressure_hpa == pytest.approx(W.BACKGROUND_HPA)
    for c in (far, near, warm, squally, showers, under, open_sea):
        assert c.sky in W.SKY_WORDS and c.weather in W.WEATHER_WORDS
        assert c.visibility in W.VISIBILITY_WORDS and c.air_mass in W.AIR_MASSES


def test_the_skys_noise_holds_for_a_watch_and_differs_between_watches():
    w = weather_with(low(x=0, y=500))
    words = {
        (
            w.conditions_at(0.0, 0.0, T0 + timedelta(hours=h)).sky,
            w.conditions_at(0.0, 0.0, T0 + timedelta(hours=h)).weather,
        )
        for h in range(0, 48)
    }
    assert len(words) > 1, "the noise makes two watches differ"
    block = [
        w.conditions_at(0.0, 0.0, T0 + timedelta(minutes=m)).sky
        for m in range(0, 60 * W.SKY_NOISE_HOURS, 15)
    ]
    assert len(set(block)) == 1, "and holds for a watch"


def test_the_hooks_for_the_coast_are_inert_until_5b():
    w = weather_with(low())
    assert w.coast_distance_km(0.0, 0.0) is None
    assert w.sea_breeze(0.0, 0.0, T0) == (0.0, 0.0)
    assert w.coastal_fog(0.0, 0.0, T0) is False


# -- seeding ------------------------------------------------------------------------------


def test_the_climatology_is_twelve_provisional_months_with_the_studys_check():
    clim = load_climatology()
    assert clim.provisional and sorted(clim.months) == list(range(1, 13))
    jan, jul = clim.month(1), clim.month(7)
    assert (jan.check["westerly_pct"], jan.check["easterly_pct"]) == (
        29.0,
        22.0,
    )  # W §1.1, 1750-1854
    assert (jul.check["westerly_pct"], jul.check["easterly_pct"]) == (44.0, 11.0)
    assert jan.check["ushant_gust31_days"] == 23.6  # W §1.2
    assert jan.speed_kn == (15.0, 35.0) and jan.central_hpa[2] >= 950.0  # W §1.3
    assert jan.lows_per_month > jul.lows_per_month


def test_seeded_systems_replay_tick_for_tick_and_draw_only_at_a_births():
    clim = load_climatology()
    start = datetime(1805, 1, 1)
    a = Weather(start, Rng(7).stream("weather"), seed=7, climatology=clim)
    b = Weather(start, Rng(7).stream("weather"), seed=7, climatology=clim)
    c = Weather(start, Rng(8).stream("weather"), seed=8, climatology=clim)
    differs = False
    for h in range(0, 30 * 24):
        t = start + timedelta(hours=h)
        for w in (a, b, c):
            w.advance(t)
        assert [(s.name, s.x_km, s.y_km, s.anomaly_hpa) for s in a.systems] == [
            (s.name, s.x_km, s.y_km, s.anomaly_hpa) for s in b.systems
        ]
        assert a.surface_wind_at(0.0, 0.0, t) == b.surface_wind_at(0.0, 0.0, t)
        differs = differs or a.surface_wind_at(0.0, 0.0, t) != c.surface_wind_at(0.0, 0.0, t)
    assert differs
    assert a.draws == b.draws and a.lows_drawn > a.LOW_SLOTS, (
        "lows were born as others left or died"
    )
    assert all(not s.gone for s in a.systems)


def test_nothing_is_drawn_while_a_scripted_system_is_present():
    clim = load_climatology()
    w = Weather(T0, Rng(7).stream("weather"), seed=7, systems=[low()], climatology=clim)
    for h in range(0, 10 * 24):
        w.advance(T0 + timedelta(hours=h))
    assert w.draws == 0 and w.scripted and len(w.systems) == 1


# -- the scenario's systems ------------------------------------------------------------------


def test_the_gate_day_file_carries_both_forms_and_the_pinned_wind_wins():
    """The gate's day with `wind` and `systems` (spec M5 §2): the frigate's base wind is
    the script's tick for tick and the systems give only the sky and the glass; the
    wind's gusts keep the M2 draws (no air mass), so truths 48 to 51 do not move."""
    sf = load_scenario(GATE_DAY)
    sc = sf.scenario
    assert (
        sc.glass
        and len(sc.weather) == 9
        and [s["name"] for s in sc.systems]
        == [
            "the low",
            "the old ridge",
            "the ridge",
        ]
    )
    assert sc.background["gradient_hpa_per_100km"] == 0.5
    assert any("the sky and the glass" in ln for ln in sf.lines())
    w = make_scenario_world(sf)
    assert w.systems is not None and w.weather is not None and w.glass is not None
    assert w.wind.air_mass is None
    for _ in range(4):
        w.run(900)
        d, s = w.weather.at(w.clock.ship_time)
        assert w.wind.base_direction == pytest.approx(d, abs=1e-9)
        assert w.wind.base_speed == pytest.approx(s, rel=1e-9)
        assert w.wind.air_mass is None
    r = w.readings
    assert 29.5 < r["glass"] < 30.5 and r["sky"]["words"] in W.SKY_WORDS
    assert r["tendency"]["words"] in W.TENDENCY_WORDS


def test_with_systems_alone_the_systems_wind_at_the_ship_is_the_base():
    sc = gate_systems()
    sc.gustiness, sc.variability = 0.0, 0.0
    w = World(seed=7, scenario=sc)
    assert w.weather is None and w.systems is not None
    for _ in range(6):
        w.run(600)
        d, s = w.systems.surface_wind_at(w.ship_x_km, w.ship_y_km, w.clock.ship_time)
        assert w.wind.direction_from == pytest.approx(d, abs=1e-9)
        assert w.wind.effective_speed == pytest.approx(s, rel=1e-9)
        assert w.wind.air_mass == w.conditions.air_mass
    assert units.point_name(w.wind.direction_from) == "W"


def test_a_scenario_file_with_both_forms_and_the_old_list_form(tmp_path):
    both = tmp_path / "both.yaml"
    both.write_text(
        "name: both\nstart: 1805-06-01T04:00\nship: {glass: true}\n"
        "weather:\n  wind:\n    - {at: 1805-06-01T04:00, from_deg: 270, knots: 17}\n"
        "  systems:\n    - name: a low\n      kind: low\n      radius_km: 450\n"
        "      track:\n        - {at: 1805-06-01T04:00, x_km: 0, y_km: 600, hpa: 990}\n",
        encoding="utf-8",
    )
    sf = load_scenario(both)
    assert sf.scenario.glass and len(sf.scenario.weather) == 1 and len(sf.scenario.systems) == 1
    assert sf.scenario.systems[0]["track"][0]["at"] == "1805-06-01T04:00:00"
    old = tmp_path / "old.yaml"
    old.write_text(
        "name: old\nweather:\n  - {at: 1805-06-01T04:00, from_deg: 270, knots: 17}\n",
        encoding="utf-8",
    )
    sf = load_scenario(old)
    assert len(sf.scenario.weather) == 1 and sf.scenario.systems == [] and not sf.scenario.glass
    seeded = tmp_path / "seeded.yaml"
    seeded.write_text("name: seeded\nweather: {climatology: true}\nglass: true\n", encoding="utf-8")
    sf = load_scenario(seeded)
    assert sf.scenario.climatology and sf.scenario.glass
    assert "climatology" in sf.lines()[1]
    w = World(seed=7, scenario=sf.scenario)
    assert w.systems is not None and w.systems.draws > 0 and w.glass is not None


@pytest.mark.parametrize(
    "systems,words",
    [
        ("  - {name: x, kind: middling, radius_km: 400}\n", "'low' or 'high'"),
        ("  - {name: x, kind: low, radius_km: 400}\n", "needs a track"),
        (
            "  - name: x\n    kind: low\n    track:\n"
            "      - {at: 1805-06-01T05:00, x_km: 0, y_km: 0, hpa: 990}\n"
            "      - {at: 1805-06-01T04:00, x_km: 0, y_km: 0, hpa: 990}\n",
            "not after",
        ),
        (
            "  - name: x\n    kind: low\n    track:\n      - {at: 1805-06-01T05:00, x_km: 0}\n",
            "'x_km', 'y_km' and 'hpa'",
        ),
        (
            "  - {name: x, kind: low, radius_km: -3, track: [{at: 1805-06-01T05:00, x_km: 0, y_km: 0, hpa: 990}]}\n",
            "no radius",
        ),
    ],
)
def test_a_scripted_system_that_cannot_be_followed_is_refused_in_words(tmp_path, systems, words):
    p = tmp_path / "bad.yaml"
    p.write_text(f"name: bad\nweather:\n  systems:\n{systems}", encoding="utf-8")
    with pytest.raises(ScenarioError, match=words):
        load_scenario(p)


def test_the_scenarios_systems_are_saved_and_a_replay_follows_them():
    from freesail.api.session import ship_factory
    from freesail.core import replay

    sc = gate_systems()
    w = World(seed=7, scenario=sc)
    w.run(3 * 3600)
    data = w.save()
    assert data["scenario"]["systems"] == sc.systems and data["scenario"]["glass"] is True
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.readings["glass"] == w.readings["glass"]


# -- the readings, the log and the roll-up -------------------------------------------------


def test_the_readings_on_a_ship_with_a_glass_and_on_one_without():
    sc = gate_systems()
    frigate = make_world(7, FRIGATE, sc)
    without = gate_systems()
    without.glass = False
    schooner = make_world(7, SCHOONER, without)
    for w in (frigate, schooner):
        w.run(2 * 3600 + 60)
    r = frigate.readings
    assert isinstance(r["glass"], float) and r.words("glass").endswith(" inches")
    assert r["tendency"]["words"] in W.TENDENCY_WORDS
    assert r.words("tendency").startswith(r["tendency"]["words"])
    assert r.words("sky").startswith(r["sky"]["words"]) and r["weather"] in W.WEATHER_WORDS
    assert r["visibility"]["words"] in W.VISIBILITY_WORDS
    s = schooner.readings
    assert s["glass"] is None and s["tendency"] is None
    assert s.words("glass") == R.NO_GLASS_WORDS and s.words("tendency") == R.NO_GLASS_WORDS
    assert s["sky"] is not None and s.words("weather") in W.WEATHER_WORDS
    bare = World(seed=1)  # no weather at all
    assert bare.readings.words("sky") == R.NO_WEATHER_WORDS
    assert bare.readings.words("visibility") == R.NO_WEATHER_WORDS
    # every reading's words, as an agent reads them
    from freesail.agents.tools import readings_words

    words = readings_words(frigate)
    assert {"glass", "tendency", "sky", "weather", "visibility"} <= set(words)


def test_the_glass_record_gives_the_tendency_in_the_periods_words():
    """The tendency is the ship's own record: the change over three hours in the words
    steady, rising, falling, rising fast, falling fast; nothing before an hour."""
    glass = Glass(seed=7)
    t = T0
    assert glass.tendency() is None
    for minute in range(0, 3 * 60 + 1):
        glass.read(1015.0 - 4.0 * minute / 180.0, t + timedelta(minutes=minute))  # 4 hPa in 3 h
    tendency = glass.tendency()
    assert tendency["words"] == "falling fast"  # 0.118 inches in three hours: the tenth
    assert tendency["three_hours_in"] == pytest.approx(-0.12, abs=0.015)
    assert tendency["one_hour_in"] == pytest.approx(-0.04, abs=0.015)
    steady = Glass(seed=7)
    for minute in range(0, 61):
        steady.read(1015.0, t + timedelta(minutes=minute))
    assert steady.tendency()["words"] == "steady"
    rising = Glass(seed=7)
    for minute in range(0, 181):
        rising.read(1010.0 + 2.0 * minute / 180.0, t + timedelta(minutes=minute))  # 0.06 in
    assert rising.tendency()["words"] == "rising"
    assert W.tendency_words(-0.02) == "steady" and W.tendency_words(0.11) == "rising fast"
    assert W.inches(1015.0) == pytest.approx(29.976, abs=0.001)


def test_the_log_says_the_weather_by_the_hour_the_glass_at_the_watch_and_the_sky_as_it_changes():
    sc = gate_systems()
    w = World(seed=7, scenario=sc)
    w.run(5 * 3600)
    hours = [e for e in w.log if e.kind == "weather.hour"]
    assert [e.ship_time.hour for e in hours] == [5, 6, 7, 8, 9]
    assert all("the glass" in e.text and e.data["glass_in"] > 29 for e in hours)
    eight = hours[3]
    assert "since the morning watch" in eight.text and eight.data["since_watch_in"] is not None
    assert all(e.severity is Severity.ROUTINE for e in hours)
    changes = [e for e in w.log if e.kind in ("weather.sky", "weather.change")]
    assert changes, "the sky or the weather changed in five hours of the warm sector"
    assert all(e.text[0].isupper() and e.text.endswith(".") for e in changes)
    # no glass: the hour's line says the sky and the weather only
    sc.glass = False
    w = World(seed=7, scenario=sc)
    w.run(3600)
    line = [e for e in w.log if e.kind == "weather.hour"][0]
    assert "glass" not in line.text and "glass_in" not in line.data


def test_the_rollup_sums_the_glass_and_the_rain_by_the_hour():
    t = datetime(1805, 6, 1, 10, 0)

    def ev(kind, text, data=None, minute=0):
        return Event(
            tick=minute * 60,
            ship_time=t + timedelta(minutes=minute),
            severity=Severity.ROUTINE,
            kind=kind,
            text=text,
            data=data or {},
        )

    hour = ev(
        "weather.hour",
        "Overcast, rain; the glass 29.72.",
        {"sky": "overcast", "weather": "rain", "glass_in": 29.72, "change_in": -0.02},
    )
    rain = ev("weather.change", "Rain set in.", {"weather": "rain"}, minute=20)
    sky = ev("weather.sky", "The sky dark and gloomy.", {"sky": "dark and gloomy"}, minute=40)
    text = events.summarise([hour, rain, sky]).text
    assert text.startswith("Overcast, rain; the glass 29.72, down 2 hundredths, ")
    assert "rain set in" in text and "the sky dark and gloomy" in text
    assert text.endswith("3 routine entries.")


def test_the_snapshot_and_the_console_carry_the_weather():
    w = make_world(7, FRIGATE, gate_systems())
    w.run(61)
    snap = queries.snapshot(w)
    wx = snap["weather"]
    assert isinstance(wx["glass_in"], float) and wx["sky"] in W.SKY_WORDS
    assert wx["weather"] in W.WEATHER_WORDS and wx["visibility"] in W.VISIBILITY_WORDS
    assert wx["tendency"] is None and wx["tendency_words"] == R.GLASS_UNWATCHED_WORDS
    assert snap["wind"]["squall"] is False
    lines = w.summary_lines()
    assert any(ln.startswith("The glass ") and ln.endswith(".") for ln in lines)
    bare = World(seed=1)
    assert queries.snapshot(bare)["weather"]["glass_in"] is None
    assert queries.snapshot(bare)["weather"]["sky_words"] == R.NO_WEATHER_WORDS
    assert not any("glass" in ln for ln in bare.summary_lines())


def test_the_dialect_reads_the_glass_the_sky_and_the_weather_for_nothing():
    """`when the glass is falling fast then shorten sail` is a book's line (spec M5 §5):
    the registry's rows are the grammar's words, on a ship with a glass or without."""
    from freesail.orders.errors import OrderError

    ship = make_world(7, SCHOONER).ship  # no glass aboard: the line still parses
    c = parse_condition("the glass is falling fast", ship)
    assert (c.clauses[0].reading, c.clauses[0].comparison.value) == ("tendency", "falling fast")
    c = parse_condition("the glass is under 29.5 inches", ship)
    assert (c.clauses[0].reading, c.clauses[0].comparison.op, c.clauses[0].comparison.value) == (
        "glass",
        "lt",
        29.5,
    )
    assert parse_condition("the glass is below 29.5", ship).clauses[0].reading == "glass"
    assert parse_condition("the barometer is rising", ship).clauses[0].reading == "tendency"
    assert parse_condition("the tendency is not steady", ship).clauses[0].comparison.op == "is_not"
    c = parse_condition("the sky is overcast and the weather is not rain", ship)
    assert [(x.reading, x.comparison.value) for x in c.clauses] == [
        ("sky", "overcast"),
        ("weather", "rain"),
    ]
    assert parse_condition("the sky is cloudy", ship).clauses[0].comparison.value == "overcast"
    assert parse_condition("the weather is raining", ship).clauses[0].comparison.value == "rain"
    assert parse_condition("the visibility is a mile", ship).clauses[0].reading == "visibility"
    for text, words in (
        ("the glass is shaking", "cannot be 'shaking'"),
        ("the sky exceeds 3", "cannot be"),
        ("the weather is blue", "cannot be 'blue'"),
        ("the glass is under 30 knots", "not knots"),
    ):
        with pytest.raises(OrderError, match=words):
            parse_condition(text, ship)
    # on a ship without a glass the condition reads false; with one it reads the record
    w = make_world(7, SCHOONER)
    assert not c.holds(w.readings)
    assert not parse_condition("the glass is falling", w.ship).holds(w.readings)
    from freesail.standing.rules import Clause, Comparison

    rich = Clause(
        "tendency", Comparison("is", "falling fast", "falling fast"), "x", (), "the glass"
    )
    glassed = World(seed=7, scenario=gate_systems())
    glassed.run(60)
    assert not rich.holds(glassed.readings), "not watched an hour yet"
    assert "watched an hour" in rich.describe(glassed.readings)


def test_a_standing_order_on_the_glass_fires_when_it_falls():
    """The frigate under the day's low from the evening: the glass falls a tenth and more
    between eight and midnight, and a rule on it fires (spec M5 §5)."""
    sc = gate_systems()
    sc.start_time = datetime(1805, 6, 1, 19, 0)
    w = make_world(7, FRIGATE, sc)
    w.submit('standing order "glass": when the glass is falling fast then steer 200')
    assert w.standing.book.get("glass") is not None
    w.run(4 * 3600)
    fired = [
        e for e in w.log if e.kind == "order.accepted" and "By standing order 'glass'" in e.text
    ]
    assert fired, [e.text for e in w.log if "glass" in e.text][-5:]
    assert w.readings["tendency"]["words"] == "falling fast"
