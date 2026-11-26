"""Package 126: the weather and the captain (the owner's notes 3 and 4 of gate M7,
`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`; the list carried forward,
`docs/dev/CarriedForward-M7.md`, section 4, item 12). The harbour's part is in
`tests/test_harbour.py` (truths 7-770 to 7-773).

The fog comes on and goes by degrees (`world.weather.Weather.fog_degree`), the sight closing
and opening through the weather's own steps and the log saying each; the game's own captain
clears a spar's wreck and shifts it for a spare where she carries one, out of action
(`world.captains.Captain._spar_work`); and a ship with no topsail set to lie a-try under
heaves to in the gale where the order would have been refused and left her sailing on.
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from freesail.core import replay as replay_mod
from freesail.physics import strain as ST
from freesail.ship import parts
from freesail.world import weather as W
from freesail.world.scenarios import begin, load_scenario, make_scenario_world
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
            assert (limit, bound) != (c.visibility_nm, "weather") or limit == clear_limit
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
    w.run(55 * 60)  # 07:55, in the settling
    assert 0.0 < w.conditions.fog < 1.0 and w.conditions.visibility == "a few miles"
    d = Path(tempfile.mkdtemp())
    path = replay_mod.save_to_file(w, d / "fog.json")
    copy, report = replay_mod.load_report(path, None)
    assert report.how == "checkpoint"
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


# -- the captain's spars --------------------------------------------------------------------

CRUISE = """
name: a spar carried away
seed: 7
start: 1805-06-12T10:00
position: {{lat_deg: 49.80, lon_deg: -5.30}}
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: 180
  speed_kn: 5
intent: cruise off the Lizard within 10 miles
wind: {{from_deg: 270, knots: 12, gustiness: 0.0, variability: 0.0}}
ports: [falmouth, plymouth, brest]
orders:
  - set plain sail
"""


def _cruising(ship: str):
    path = Path(tempfile.mkdtemp()) / "cruise.yaml"
    path.write_text(CRUISE.format(ship=ship), encoding="utf-8")
    sf = load_scenario(str(path))
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(600)
    return w


def _carry_away(w, *spars: str) -> None:
    for sid in spars:
        ST._wreck_spar(w.ship, ST.strain_state(w.ship), w.ship.spars[sid], 2.0)


def _captains(w, n0: int) -> list[str]:
    return [e.text for e in w.log[n0:] if str(e.actor).startswith("captain")]


def test_truth_7_776_the_captain_clears_the_wreck_and_shifts_the_spar_for_a_spare():
    """The owner's note 4 of gate M7: the game's own captain, out of action and with
    nothing else in hand, clears away the wreck of a spar carried away, shifts it for a spare
    of its class from the booms, bends again the head sail it took as soon as it stands, then
    shifts the next spar that stands on it, and bends the rest; each order says why in his
    words. The cutter's main topmast carried away: the wreck (with the topgallant mast and
    both yards on it), the topmast from her one spare, the jib, the topsail yard from her one
    spare yard, the topsail and the gaff topsail; the topgallant mast, for which she carries
    no spare, and its yard are left as they are."""
    w = _cruising("cutter")
    _carry_away(w, "main.topmast")
    n0 = len(w.log)
    w.run(5 * 3600)
    said = _captains(w, n0)
    keys = ("wreck", "shifting", "bending", "jury", "(bent again to its spar)")
    work = [x for x in said if any(k in x for k in keys)]
    by = "By the captain, keeping station: "
    assert work == [
        by + "clearing away the wreck of the main topmast (the main topmast carried away).",
        by + "shifting the main topmast (the main topmast carried away).",
        by + "bending the jib (its spar shifted for a spare).",
        by + "setting the jib (bent again to its spar).",
        by + "shifting the topsail yard (the topsail yard carried away).",
        by + "bending the topsail (its spar shifted for a spare).",
        by + "setting the topsail (bent again to its spar).",
        by + "bending the gaff topsail (its spar shifted for a spare).",
        by + "setting the gaff topsail (bent again to its spar).",
    ], work
    ship = w.ship
    assert not ship.spars["main.topmast"].wrecked and not ship.spars["topsail.yard"].wrecked
    assert ship.spars["main.topgallant_mast"].wrecked and ship.spars["topgallant.yard"].wrecked
    assert parts.booms(ship).have("topmast") == 0 and parts.booms(ship).have("yard") == 0
    assert ship.sails["jib"].state is not parts.SailState.UNBENT
    assert [e.kind for e in w.log[n0:] if e.kind == "spar.shifted"] == ["spar.shifted"] * 2
    assert ship.sails["jib"].is_set and ship.sails["topsail"].is_set
    # two spars down, of two classes: the one that keeps her manageable first (the brig's
    # main topmast before her fore topgallant mast, the wreck and the shift alike), and her
    # one spare yard to her topsail yard, never to a lower yard
    w = _cruising("brig")
    _carry_away(w, "fore.topgallant_mast", "main.topmast", "main.yard")
    n0 = len(w.log)
    w.run(4 * 3600)
    order = [
        x.split(": ", 1)[1].split(" (")[0]
        for x in _captains(w, n0)
        if "wreck of" in x or "shifting" in x
    ]
    assert order[:4] == [
        "clearing away the wreck of the main topmast",
        "clearing away the wreck of the main yard",
        "clearing away the wreck of the fore topgallant mast",
        "shifting the main topmast",
    ], order
    assert order.index("shifting the main topsail yard") < order.index(
        "shifting the fore topgallant mast"
    ), order
    assert "shifting the main yard" not in order and w.ship.spars["main.yard"].wrecked


def test_truth_7_777_none_where_she_has_no_spare_none_under_fire_and_none_with_hands_busy():
    """The Renard's own case (the cutter's main topgallant mast shot away): the wreck is
    cleared, and the line says there is no spare topgallant mast aboard; nothing is shifted,
    the topgallant yard waiting on its mast. No spar work is ordered within ten minutes of a
    shot come aboard, nor while other repair work is in hand; and none in action."""
    w = _cruising("cutter")
    _carry_away(w, "main.topgallant_mast")
    n0 = len(w.log)
    w.run(3 * 3600)
    said = [x for x in _captains(w, n0) if "wreck" in x or "shifting" in x or "bending" in x]
    assert said == [
        "By the captain, keeping station: clearing away the wreck of the main topgallant mast "
        "(the main topgallant mast carried away)."
    ]
    # and nothing asked that she cannot do: no shift given and refused for want of a spare
    refused = [e.text for e in w.log[n0:] if e.kind == "order.rejected" and "spare" in e.text]
    assert refused == [], refused
    cleared = [e.text for e in w.log[n0:] if e.kind == "wreck.cleared"]
    assert len(cleared) == 1 and cleared[0].endswith("There is no spare topgallant mast aboard.")
    ship = w.ship
    assert ship.spars["main.topgallant_mast"].sent_down and ship.spars["topgallant.yard"].sent_down
    # under fire, with other repair work in hand, in action: nothing; then the wreck
    from freesail.combat.hits import damage_of
    from tests.test_damage_control import _hole

    w = _cruising("brig")
    _carry_away(w, "main.topmast")
    cap, ship = w.captain, w.ship

    def asked() -> list[str]:
        n0 = len(w.log)
        cap._business.pop("repairs_tick", None)
        from freesail.world.captains import Perception

        cap._repairs(Perception.read(w))
        return [x for x in _captains(w, n0) if "wreck" in x]

    damage_of(ship).struck_by["a stranger"] = w.clock.tick - 60
    assert asked() == []
    damage_of(ship).struck_by["a stranger"] = w.clock.tick - 601
    _hole(w, 0.8)  # above the water: the captain's own repairs leave it, the order given here
    assert w.submit("plug the shot holes").kind == "order.accepted"
    assert "plug_shot_hole" in {i.evo.id for i in ship.extra["evolutions"].instances}
    assert asked() == []
    runner = ship.extra["evolutions"]
    runner.instances[:] = [i for i in runner.instances if i.evo.id != "plug_shot_hole"]
    cap.state = "engaging"
    assert asked() == []
    cap.state = "struck"  # a prize's spars are her captor's to order, not her own captain's
    assert asked() == []
    cap.state = "keeping station"
    assert asked() == [
        "By the captain, keeping station: clearing away the wreck of the main topmast (the main "
        "topmast carried away)."
    ]


# -- lying to with no topsail set -----------------------------------------------------------

GALE = """
name: a gale abeam
seed: 7
start: 1805-06-14T04:00
position: 48 40 N 5 05 W
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: 0
  speed_kn: 6
  glass: true
intent: bound for Falmouth
ports: [falmouth, plymouth, brest]
weather:
  wind:
    - {{at: 1805-06-14T00:00, from_deg: {wind}, knots: 20, air_mass: neutral}}
    - {{at: 1805-06-14T04:30, from_deg: {wind}, knots: 20}}
    - {{at: 1805-06-14T05:30, from_deg: {wind}, knots: 35}}
    - {{at: 1805-06-14T08:00, from_deg: {wind}, knots: 35}}
  background:
    {{hpa: 1004, gradient_hpa_per_100km: 1.2, high_toward_deg: 200}}
  sea: true
orders:
  - set plain sail
"""


def _gale(ship: str, wind: int):
    path = Path(tempfile.mkdtemp()) / "gale.yaml"
    path.write_text(GALE.format(ship=ship, wind=wind), encoding="utf-8")
    sf = load_scenario(str(path))
    w = make_scenario_world(sf)
    begin(w, sf)
    return w


def test_truth_7_778_with_no_topsail_set_to_lie_a_try_under_she_heaves_to_in_the_gale():
    """The list carried forward from milestone 7, section 4, item 12 (`lie a-try` ordered by
    the game's own captain with the wind abeam and not taken), as it is on a ship in the game:
    the smack, her topsail furled under her plain sail, bound for Falmouth with the wind
    rising from twenty knots to thirty-five over an hour, abeam (from the west) and nearer
    the wind (from the north-east): at the gale's line the captain's `lie a-try` was refused
    ("The topsail is not set; set it to lie a-try under it.") and she sailed on at seven to
    nine knots for the two hours of the gale. She heaves to under her fore-and-aft canvas,
    the order said with its reason, and drifts at under two and a half knots; a ship with
    her topsail set lies a-try as before (the cutter)."""
    for wind in (270, 55):
        w = _gale("smack", wind)
        w.run(int(1.5 * 3600))
        said = _captains(w, 0)
        refused = [e for e in w.log if e.kind == "order.rejected" and "lie a-try" in e.text]
        assert refused == [], [e.text for e in refused]
        assert (
            "By the captain, hove to for weather: heaving to (no topsail set to lie a-try under)."
            in said
        ), said
        hove = [e for e in w.log if e.kind == "ship.hove_to"]
        assert hove and "under her fore-and-aft canvas" in hove[0].text, (wind, hove)
        assert 3540 <= hove[0].tick <= 3540 + 900
        speeds = []
        for _ in range(30):
            w.run(60)
            speeds.append(float(w.readings.value("speed")) * 1.943844)
        assert max(speeds) < 2.5 and w.captain.state == "hove to for weather", (wind, speeds)
    w = _gale("cutter", 270)
    w.run(int(1.5 * 3600))
    assert any(e.text.startswith("Lying a-try under the topsail") for e in w.log)
    assert "By the captain, hove to for weather: lying a try." in _captains(w, 0)
    # her topsail unbent is as her topsail furled: she heaves to
    w = _gale("smack", 270)
    w.ship.sails["topsail"].state = parts.SailState.UNBENT
    w.run(int(1.5 * 3600))
    said = _captains(w, 0)
    assert (
        "By the captain, hove to for weather: heaving to (no topsail set to lie a-try under)."
        in said
    ), said
    # a topsail in hand, lowered for its reefs at the gale's line, is not a topsail stowed: the
    # bilander lies a-try under it, as she did
    w = _gale("bilander", 270)
    w.run(int(2.5 * 3600))
    said = _captains(w, 0)
    assert "By the captain, hove to for weather: lying a try." in said, said
    assert not any("no topsail set to lie a-try under" in x for x in said)
    assert any(e.text.startswith("Lying a-try under the main topsail") for e in w.log)


# -- the spar's work leaves her no worse off --------------------------------------------------


def _three_hours_on(ship: str, spar: str, spar_work: bool, monkeypatch) -> dict:
    """Her way through the third hour after a spar carried away out of action, how often she
    was taken aback, and what the captain said, with his spar work or without it (the trunk's
    captain, who left the spar as it fell)."""
    from freesail.world import captains as C

    if not spar_work:
        monkeypatch.setattr(C.Captain, "_spar_work", lambda self, *a: None)
    w = _cruising(ship)
    _carry_away(w, spar)
    n0 = len(w.log)
    way: list[float] = []
    for minute in range(180):
        w.run(60)
        if minute >= 120:
            way.append(float(w.ship.dyn.u) * 1.943844)
    monkeypatch.undo()
    return {
        "world": w,
        "mean": sum(way) / len(way),
        "least": min(way),
        "aback": sum(1 for e in w.log[n0:] if e.kind == "ship.aback"),
        "said": _captains(w, n0),
    }


@pytest.mark.slow
@pytest.mark.parametrize(
    ("ship", "spar", "sail"),
    [
        ("cutter", "main.topmast", "jib"),  # a fore-and-after
        ("brig", "main.topmast", "main.topsail"),  # a small square-rigger
        ("seventy-four", "fore.topmast", "fore.topsail"),  # a ship of the line
    ],
)
def test_truth_7_779_her_spar_shifted_she_makes_no_less_way_and_is_no_more_often_aback(
    ship, spar, sail, monkeypatch
):
    """The lead's list of 2026-11-24 for package 126, A3: the spar's work must not leave her
    worse off than the trunk's captain, who left the spar as it fell. A spar carried away out
    of action, cruising off the Lizard in twelve knots: three hours on she makes no less way
    through the third hour, and is taken aback no more often, than the same ship with the
    same loss and no spar work; the sail that stood on the spar is bent again, set by him,
    and drawing; he gave no spar's order while she was in a manoeuvre, and every order of the
    work (the wreck, the shift, the bend, the set) said why."""
    on = _three_hours_on(ship, spar, True, monkeypatch)
    off = _three_hours_on(ship, spar, False, monkeypatch)
    assert on["mean"] >= off["mean"], (on["mean"], off["mean"])
    assert on["least"] > 0.0, on["least"]  # never going astern in the third hour
    assert on["aback"] <= off["aback"], (on["aback"], off["aback"])
    w = on["world"]
    name = w.captain._sail_name(sail)
    said = on["said"]
    assert any(f"setting the {name} (bent again to its spar)" in x for x in said), said
    assert any(f"bending the {name} (its spar shifted for a spare)" in x for x in said), said
    assert not w.ship.spars[spar].wrecked
    assert w.ship.sails[sail].is_set
    assert not [x for x in off["said"] if "shifting" in x or "wreck" in x]
