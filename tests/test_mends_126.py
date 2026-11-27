"""Package 126: the weather (the owner's note 3 of gate M7,
`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`). The harbour's part is in
`tests/test_harbour.py` (truths 7-770 to 7-773).

The fog comes on and goes by degrees (`world.weather.Weather.fog_degree`), the sight closing
and opening through the weather's own steps and the log saying each.
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from freesail.core import replay as replay_mod
from freesail.world import weather as W
from tests.test_chart import SCHOONER, chart_world, high_over_the_channel

# -- the fog by degrees ---------------------------------------------------------------------

# Off Falmouth under the June high of test_chart, seed 7: the morning of the 5th draws a fog
# that settles from 07:42 and clears to 11:45 (measured; the lines below are its log).
FOG_DAY = datetime(1805, 6, 5, 7, 0)
FOG_LINES_IN_ORDER = [
    "A fog is settling in.",
    "The fog is thickening.",
    "The fog has shut in thick.",
    "The fog seems to be clearing.",
    "The fog is thinning.",
    "The fog lifted.",
]


def _fog_world():
    start = datetime(1805, 6, 1, 0, 0)
    w = chart_world(
        50.12, -5.03, ship=SCHOONER, start=FOG_DAY, systems=high_over_the_channel(start)
    )
    return w


def _fog_lines(w) -> list:
    return [e for e in w.log if e.kind in ("weather.change", "weather.fog")]


def test_truth_7_774_the_fog_comes_on_and_clears_over_a_time_and_is_said_as_it_does():
    """The owner's note 3 of gate M7 ("fog clears instantaneously ... 'the fog seems to be
    clearing', or, 'a fog is settling in'"): a fog drawn for a sky block no longer falls at
    one minute from the horizon to a cable and lifts at another. Off Falmouth on a June
    morning under a high it settles in at a few miles' or a mile's sight, shuts in thick to a
    cable within the half hour it takes to settle, opens again a step at a time over the hour
    before it lifts, and the log says each: "A fog is settling in.", "The fog has shut in
    thick.", "The fog seems to be clearing.", "The fog lifted."; what the ship reads (her
    conditions, the reading of the weather, the lookout's limit by the weather) is the
    sight of that minute through it."""
    w = _fog_world()
    seen: list[tuple[int, str, float]] = []
    for _ in range(5 * 60):
        w.run(60)
        c = w.conditions
        if not seen or seen[-1][1] != c.visibility:
            seen.append((w.clock.tick, c.visibility, c.fog))
        # the reading a station is served is the minute's sight
        assert w.readings.words("visibility") == c.visibility
        # the lookout's limit by the shore is the weather's sight wherever that is the less
        limit, bound = w.lookout._shore_limit(c.visibility_nm, w.daylight)
        clear_limit, _ = w.lookout._shore_limit(None, w.daylight)
        if c.visibility_nm < clear_limit:
            assert (limit, bound) == (c.visibility_nm, "weather"), (c.visibility, limit, bound)
        else:
            assert limit == clear_limit, (c.visibility, limit, bound)
    lines = _fog_lines(w)
    said = [e.text for e in lines]
    fog_said = [t for t in said if "fog" in t.lower()]
    assert fog_said == FOG_LINES_IN_ORDER, said  # every line of the fog, in order
    at = {e.text: e.tick for e in lines}
    settle = at["The fog has shut in thick."] - at["A fog is settling in."]
    clear = at["The fog lifted."] - at["The fog seems to be clearing."]
    # the times as figures, not as the constants (the lead's list, B4): the settling half
    # an hour from its first line to a cable, a mile at its half; the clearing an hour from
    # its first opening to the fog lifted, a few miles at its half
    assert abs(settle - 1800) <= 120, settle
    assert abs(clear - 3600) <= 120, clear
    assert abs(at["The fog is thickening."] - at["A fog is settling in."] - 900) <= 120
    assert abs(at["The fog is thinning."] - at["The fog seems to be clearing."] - 1800) <= 120
    # the sight through the steps between: never from a cable to clear, or clear to a cable
    sights = [v for _, v, _ in seen]
    for a, b in zip(sights, sights[1:], strict=False):
        assert {a, b} != {"a cable", "the horizon"}, sights
    assert "a mile" in sights and "a cable" in sights
    # notable where the sight she is handled by has changed (settled in, shut in thick, first
    # opening), routine the steps between and its lifting, as the lead ruled
    severity = {
        "A fog is settling in.": "NOTABLE",
        "The fog has shut in thick.": "NOTABLE",
        "The fog seems to be clearing.": "NOTABLE",
        "The fog is thickening.": "ROUTINE",
        "The fog is thinning.": "ROUTINE",
        "The fog lifted.": "ROUTINE",
    }
    fogs = [e for e in lines if e.text in severity]
    assert fogs and all(e.severity.name == severity[e.text] for e in fogs), [
        (e.text, e.severity.name) for e in fogs
    ]


def test_truth_7_775_the_fog_is_the_same_after_a_save_and_a_plain_function_of_its_moment():
    """The fog's degree is a function of the seed, the place and the moment alone (no state
    to keep): a game saved while the fog settles and taken up from its checkpoint goes on to
    the same sights and the same lines as the game that was never saved, minute by minute;
    and the conditions of any minute asked twice, or out of order, are the same."""
    w = _fog_world()
    w.run(48 * 60)  # 07:48, in the settling, six minutes after its first line
    assert 0.0 < w.conditions.fog < 1.0 and w.conditions.visibility == "a few miles"
    # the quiet between two lines in force as it is saved, and kept by the checkpoint
    said = w._fog_said
    assert said is not None and said[2] == "settling" and w.clock.tick - said[0] < 600
    d = Path(tempfile.mkdtemp())
    path = replay_mod.save_to_file(w, d / "fog.json")
    copy, report = replay_mod.load_report(path, None)
    assert report.how == "checkpoint"
    assert copy._fog_said == said
    n0, n1 = len(w.log), len(copy.log)
    for _ in range(4 * 60):
        w.run(60)
        copy.run(60)
        assert (copy.conditions.visibility, copy.conditions.fog) == (
            w.conditions.visibility,
            w.conditions.fog,
        )
    assert [e.text for e in copy.log[n1:]] == [e.text for e in w.log[n0:]]
    sys = w.systems
    moments = [FOG_DAY + timedelta(minutes=m) for m in range(0, 300, 7)]
    first = [sys.conditions_at(0.0, 0.0, t) for t in moments]
    again = [sys.conditions_at(0.0, 0.0, t) for t in reversed(moments)][::-1]
    assert first == again


def test_truth_7_775_b_the_fog_thins_at_its_edges_and_its_sight_steps_one_at_a_time(
    monkeypatch,
):
    """The lead's list of 2026-11-24, B1 to B4, at the fog's own function: in the thick of a
    drawn fog (09:30 on the 5th off Falmouth, a cable's sight), it is thick under a wind of
    9 knots, half thinned at 10.5 and gone at 12.5; thick 20 km from the coast, half at 27.5
    and gone at 31; and where the air that holds it is to go in half an hour it is half
    cleared, a minute before only just there, and gone at the moment, as where it came half
    an hour ago and a quarter. Through a June of minutes its sight never jumps a step coming or
    going. And the log does not say a step one way within ten minutes of a step the other."""
    w = _fog_world()
    sys = w.systems
    noon = datetime(1805, 6, 5, 9, 30)
    assert sys.fog_degree(0.0, 0.0, noon) == 1.0
    real_geo, real_coast, real_air = sys.geostrophic_at, sys._coast, sys._fog_air

    def wind(kn: float):
        ms = kn / 1.943844 / W.SURFACE_SCALE
        monkeypatch.setattr(sys, "geostrophic_at", lambda x, y: (ms, 0.0))

    for kn, degree in ((9.0, 1.0), (10.5, 0.5), (12.5, 0.0)):
        wind(kn)
        assert abs(sys.fog_degree(0.0, 0.0, noon) - degree) < 0.02, (kn, degree)
    monkeypatch.setattr(sys, "geostrophic_at", real_geo)
    for km, degree in ((20.0, 1.0), (27.5, 0.5), (31.0, 0.0)):
        monkeypatch.setattr(sys, "_coast", lambda x, y, km=km: (km, 0.0))
        assert abs(sys.fog_degree(0.0, 0.0, noon) - degree) < 0.02, (km, degree)
    monkeypatch.setattr(sys, "_coast", real_coast)
    leaves = noon + timedelta(minutes=30)
    monkeypatch.setattr(sys, "_fog_air", lambda x, y, t: t < leaves)
    assert abs(sys.fog_degree(0.0, 0.0, noon) - 0.5) < 0.02
    assert 0.0 < sys.fog_degree(0.0, 0.0, leaves - timedelta(minutes=1)) < 0.05
    assert sys.fog_degree(0.0, 0.0, leaves) == 0.0
    came = noon - timedelta(minutes=15)
    monkeypatch.setattr(sys, "_fog_air", lambda x, y, t: t >= came)
    assert abs(sys.fog_degree(0.0, 0.0, noon) - 0.5) < 0.02
    assert sys.fog_degree(0.0, 0.0, came + timedelta(minutes=30)) == 1.0
    monkeypatch.setattr(sys, "_fog_air", real_air)
    # a June of minutes: every change of sight in or out of fog is one step
    steps = W.VISIBILITY_WORDS
    start = datetime(1805, 6, 1, 0, 0)
    was = sys.conditions_at(0.0, 0.0, start)
    jumps = []
    for m in range(1, 30 * 24 * 60):
        t = start + timedelta(minutes=m)
        now = sys.conditions_at(0.0, 0.0, t)
        if "fog" in (now.weather, was.weather) and now.visibility != was.visibility:
            if abs(steps.index(now.visibility) - steps.index(was.visibility)) > 1:
                jumps.append((t, was.visibility, now.visibility))
        was = now
    assert jumps == [], jumps[:5]
    # the quiet between two steps said: a flicker of the sight is read, and not said
    from freesail.world.weather import Conditions

    seq = ["a mile", "a few miles", "a mile", "a few miles", "a mile"]
    w2 = _fog_world()
    said_before = len(_fog_lines(w2))
    base = w2.conditions
    for vis in seq:
        c = Conditions(base.sector, base.air_mass, "thick", "", "fog", vis, base.pressure_hpa, 0.5)
        w2._last_conditions = w2.conditions if w2.conditions.weather == "fog" else c
        monkeypatch.setattr(
            w2, "_observe_weather", lambda first=False, c=c: setattr(w2, "conditions", c)
        )
        w2._tick_weather()
        w2.clock.tick += 60
    said = [e.text for e in _fog_lines(w2)[said_before:]]
    assert said == ["The fog is thinning."], said
    # put off, not lost: the sight holding at a mile past the quiet, it is said
    for _ in range(11):
        w2._tick_weather()
        w2.clock.tick += 60
    said = [e.text for e in _fog_lines(w2)[said_before:]]
    assert said == ["The fog is thinning.", "The fog is thickening."], said
    # a fog giving way to other weather is said to lift
    showers = Conditions(
        base.sector,
        base.air_mass,
        "detached clouds",
        "",
        "passing showers",
        "a few miles",
        base.pressure_hpa,
        0.0,
    )
    monkeypatch.setattr(
        w2, "_observe_weather", lambda first=False: setattr(w2, "conditions", showers)
    )
    w2._tick_weather()
    changed = [e.text for e in w2.log if e.kind == "weather.change"]
    assert changed[-1] == "The fog lifted. Passing showers.", changed[-3:]
    assert w2._fog_said is None
    # the air's edge in space: a ship sailing toward it has the fog thin over the last five km
    edge = 0.5
    monkeypatch.setattr(sys, "_fog_air", lambda x, y, t: x < edge)
    across = [sys.fog_degree(edge - km, 0.0, noon) for km in (6.0, 3.5, 1.5, 0.3)]
    assert across[0] == 1.0 and 0.0 < across[2] < across[1] < 1.0 and across[3] == 0.0, across
    monkeypatch.setattr(sys, "_fog_air", real_air)
