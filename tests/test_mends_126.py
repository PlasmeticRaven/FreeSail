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
        by + "bending the gaff topsail (its spar shifted for a spare).",
    ], work  # her topsail loosed and her gaff topsail furled when it went: bent, not set
    ship = w.ship
    assert not ship.spars["main.topmast"].wrecked and not ship.spars["topsail.yard"].wrecked
    assert ship.spars["main.topgallant_mast"].wrecked and ship.spars["topgallant.yard"].wrecked
    assert parts.booms(ship).have("topmast") == 0 and parts.booms(ship).have("yard") == 0
    assert ship.sails["jib"].state is not parts.SailState.UNBENT
    assert [e.kind for e in w.log[n0:] if e.kind == "spar.shifted"] == ["spar.shifted"] * 2
    assert ship.sails["jib"].is_set and ship.sails["topsail"].state is not parts.SailState.UNBENT
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
    # an order of his or the watch's waiting for hands has them first (the lead's list of
    # 2026-11-27 for part two, item 1): her trims waiting, nothing; none waiting, the wreck
    assert any(i.waiting for i in runner.instances)
    assert asked() == []
    runner.instances[:] = [i for i in runner.instances if not i.waiting]
    assert asked() == [
        "By the captain, keeping station: clearing away the wreck of the main topmast (the main "
        "topmast carried away)."
    ]
    # not under command, nothing: in a manoeuvre, aback with no headway, or without steerage way
    import dataclasses

    from freesail.world.captains import Perception

    w = _cruising("brig")
    _carry_away(w, "main.topmast")
    cap, ship = w.captain, w.ship
    runner = ship.extra["evolutions"]
    runner.instances[:] = [i for i in runner.instances if not i.waiting]  # none waits for hands
    p = Perception.read(w)
    assert p.manoeuvre == "none" and p.headway and cap._spar_work(ship, p, set(), runner)
    for changed in ({"manoeuvre": "wearing"}, {"manoeuvre": "hove to"}, {"headway": False}):
        assert cap._spar_work(ship, dataclasses.replace(p, **changed), set(), runner) is None
    u = ship.dyn.u
    ship.dyn.u = 0.5  # a knot: no steerage way
    assert cap._spar_work(ship, p, set(), runner) is None
    ship.dyn.u = u
    # a light spar last, and only with nothing at all in hand: the brig's studding-sail boom
    # alone carried away and cleared, it waits while any work is in hand
    w = _cruising("brig")
    boom = "main.topmast.studdingsail_boom.starboard"
    _carry_away(w, boom)
    w.ship.spars[boom].sent_down = True
    cap, ship = w.captain, w.ship
    runner = ship.extra["evolutions"]
    p = Perception.read(w)
    assert runner.instances, "her trims in hand at the start"
    assert cap._spar_work(ship, p, set(), runner) is None
    runner.instances[:] = []
    got = cap._spar_work(ship, p, set(), runner)
    assert got is not None and got[0].startswith("shift the starboard main topmast studding"), got
    # the spares are read without writing into a ship with nothing carried away
    from freesail.world.captains import spares_of

    whole = _cruising("cutter").ship
    whole.extra.pop("booms", None)
    whole.extra.pop("spare_spars", None)
    assert spares_of(whole, "topmast") == 1 and spares_of(whole, "topgallant_mast") == 0
    assert "booms" not in whole.extra and "spare_spars" not in whole.extra
    # a manoeuvre begun while a spar is being shifted belays the shift and takes its hands; the
    # shift is taken up again after, and done
    from tests.test_damage_control import _world as harbour_world

    w = harbour_world()
    _carry_away(w, "main.topmast")
    assert w.submit("clear away the wreck of the main topmast").kind == "order.accepted"
    w.run(2400)
    assert w.ship.spars["main.topmast"].sent_down
    assert w.submit("shift the main topmast").kind == "order.accepted"
    w.run(120)
    n0 = len(w.log)
    assert w.submit("wear ship").kind == "order.accepted"
    w.run(3 * 3600)
    after = [(e.kind, e.text) for e in w.log[n0:]]
    belayed = [t for k, t in after if k == "evolution.belayed" and "shifting the main topmast" in t]
    assert belayed, after[:12]
    kinds = [k for k, _ in after]
    assert "spar.shifted" in kinds and kinds.index("spar.shifted") > kinds.index(
        "evolution.belayed"
    )
    assert not w.ship.spars["main.topmast"].wrecked


def test_truth_7_777_b_the_wreck_she_needs_to_work_her_is_cleared_before_a_light_one():
    """The order of the wreck's clearing (the lead's list of 2026-11-27 for package 126, part
    two, item 3; the reader's mutant M03, a light spar sorted first, survived): with a light
    spar's wreck hanging beside a working spar's, the working spar's is cleared first, with
    work in hand or with none; the light spar's is cleared after it, and only with nothing at
    all in hand."""
    from freesail.evolutions.scripts import wrecks
    from freesail.world.captains import Perception

    boom = "main.topmast.studdingsail_boom.starboard"
    for in_hand in (True, False):
        w = _cruising("brig")
        _carry_away(w, boom, "fore.topmast")
        cap, ship = w.captain, w.ship
        runner = ship.extra["evolutions"]
        # her trims going on, none waiting for hands (work waiting has the hands first)
        runner.instances[:] = [i for i in runner.instances if in_hand and not i.waiting]
        assert bool(runner.instances) is in_hand
        got = cap._spar_work(ship, Perception.read(w), set(), runner)
        assert got is not None and got[0] == "clear away the wreck of the fore topmast", got
    # the working spar's wreck cleared: the light spar's waits on work in hand, and is cleared
    # with none
    for sp in wrecks(ship):
        if getattr(sp, "id", None) != boom:
            sp.sent_down = True
    assert [x.id for x in wrecks(ship) if hasattr(x, "id")] == [boom]
    runner.instances[:] = [i for i in _cruising("brig").ship.extra["evolutions"].instances[:1]]
    assert cap._spar_work(ship, Perception.read(w), set(), runner) is None
    runner.instances[:] = []
    got = cap._spar_work(ship, Perception.read(w), set(), runner)
    assert got is not None and got[0].startswith("clear away the wreck of the starboard"), got


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


def _player_bilander(all_hands: bool):
    """The bilander under the player's orders alone, 18 knots from the west: plain sail set,
    her fore topmast carried away at a quarter of an hour, its wreck ordered cleared, and three
    minutes after (all hands called by his order first, or not) the mainsail ordered taken in,
    which her watch, setting her main topsail and topgallant, is short of hands for."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    w = make_world(
        7,
        "data/ships/bilander.yaml",
        Scenario(
            wind_from_deg=270,
            wind_speed_kn=18,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=0,
            ship_speed_kn=5,
        ),
    )
    w.submit("set plain sail")
    w.run(900)
    _carry_away(w, "fore.topmast")
    n0 = len(w.log)
    assert w.submit("clear away the wreck of the fore topmast").kind == "order.accepted"
    w.run(180)
    if all_hands:
        w.submit("call all hands")
        w.run(60)
        assert w.ship.extra["crew"].all_hands_called_by_order
    assert w.submit("take in the mainsail").kind == "order.accepted"
    return w, n0


def _clearing(w):
    return next(
        (i for i in w.ship.extra["evolutions"].instances if i.evo.id == "clear_wreck"), None
    )


def test_truth_7_777_c_work_short_of_hands_belays_the_spars_work_and_has_its_hands():
    """The spar's work is the last claimant of her hands (the lead's list of 2026-11-27 for
    package 126, part two, items 1 and 3; the reader's mutant N01, the giving-way removed,
    survived every tier): work short of hands or too few to begin holds the wreck's clearing in
    hand and has its hands, said, with all hands called by order or without; and no work goes
    on short with the wreck named as what the rest are at."""
    for all_hands in (False, True):
        w, n0 = _player_bilander(all_hands)
        w.run(5400)
        after = [(e.kind, e.text) for e in w.log[n0:]]
        belayed = [
            t
            for k, t in after
            if k == "evolution.belayed"
            and t
            == "Belayed clearing away the wreck of the fore topmast: hands to take in the mainsail."
        ]
        assert belayed, (all_hands, after)
        named = [t for k, t in after if k == "evolution.short_handed" and "wreck" in t]
        assert named == [], (all_hands, named)
        kinds = [k for k, _ in after]
        assert "wreck.cleared" in kinds, (all_hands, after[-6:])


def test_truth_7_777_d_a_spars_work_held_is_taken_up_only_when_nothing_has_wanted_hands():
    """A spar's work held for her working is not taken up again while other work waits for
    hands or goes on short, nor until nothing has wanted them for five minutes (`runner.
    SPAR_WORK_RESUME_QUIET_S`; the lead's list of 2026-11-27, item 4: twelve belays in one
    passage is a thrash; the reader's mutant N02, the resume not waiting, survived)."""
    from freesail.crew import hands
    from freesail.evolutions.runner import SPAR_WORK_RESUME_QUIET_S

    assert SPAR_WORK_RESUME_QUIET_S == 300
    w, _n0 = _player_bilander(False)
    runner = w.ship.extra["evolutions"]
    last_want = None
    resumed_at = None
    was_paused = False
    for _ in range(240):
        w.run(15)
        clearing = _clearing(w)
        if clearing is None:
            break
        others = [i for i in runner.instances if i.evo.id != "clear_wreck" and not i.paused]
        wanting = [
            i
            for i in others
            if (i.waiting and i.waiting_for == "hands")
            or (i.assignment is not None and i.assignment.outcome == hands.SHORT)
        ]
        if clearing.paused:
            was_paused = True
            if wanting:
                last_want = w.clock.tick
        elif was_paused and resumed_at is None:
            resumed_at = w.clock.tick
            assert not wanting, [i.evo.id for i in wanting]
    assert was_paused and resumed_at is not None and last_want is not None
    assert resumed_at - last_want >= SPAR_WORK_RESUME_QUIET_S, (last_want, resumed_at)
    # at the function: held, nothing wanting hands, it waits out the five minutes and no more
    w, _n0 = _player_bilander(False)
    w.run(1200)
    runner = w.ship.extra["evolutions"]
    clearing = _clearing(w)
    crew = w.ship.extra["crew"]
    runner.instances[:] = [clearing]
    now = w.clock.tick
    clearing.wanted_at = now - SPAR_WORK_RESUME_QUIET_S + 1
    assert runner._spar_work_waits(w.ship, clearing, crew)
    clearing.wanted_at = now - SPAR_WORK_RESUME_QUIET_S
    assert not runner._spar_work_waits(w.ship, clearing, crew)


def _wrecked_cruising(
    spar: str = "main.topmast", keep_waiting: bool = False, ship_file: str = "brig"
):
    from freesail.world.captains import Perception

    w = _cruising(ship_file)
    _carry_away(w, spar)
    runner = w.ship.extra["evolutions"]
    if not keep_waiting:
        runner.instances[:] = [i for i in runner.instances if not i.waiting]
    return w, w.captain, w.ship, runner, Perception.read(w)


def test_truth_7_777_e_no_spars_work_in_heavy_weather_unless_she_lies_to():
    """At his shortening line or over it, or with the weather worsening (the glass falling
    fast or the wind risen by a force within the hour), no spar's work is begun, the wreck's
    clearing with it, unless she lies to for the weather; and work in hand is held for the
    weather and not taken up again until she lies to or the weather settles (the lead's list
    of 2026-11-27, item 4; the reader's mutants N03, the worsening gate dropped, and N04, the
    weather blind to the trend, survived)."""
    import dataclasses

    from freesail.evolutions.runner import SPAR_WORK_WEATHER_HELD

    w, cap, ship, runner, p = _wrecked_cruising()
    line = float(cap._th("shorten_sail_kn", 30.0))
    cap.trend = "steady"
    settled = dataclasses.replace(p, wind_kn=line - 1.0)
    assert not cap._weather_against_spar_work(settled)
    got = cap._spar_work(ship, settled, set(), runner)
    assert got is not None and got[0] == "clear away the wreck of the main topmast", got
    over = dataclasses.replace(p, wind_kn=line)
    assert cap._weather_against_spar_work(over)
    assert cap._spar_work(ship, over, set(), runner) is None
    cap.trend = "worsening"
    assert cap._weather_against_spar_work(settled)
    assert cap._spar_work(ship, settled, set(), runner) is None
    # lying to for the weather, the wreck is cleared whatever the wind
    cap.state = "hove to for weather"
    lying = dataclasses.replace(p, wind_kn=line + 10.0, manoeuvre="hove to")
    got = cap._spar_work(ship, lying, set(), runner)
    assert got is not None and got[0] == "clear away the wreck of the main topmast", got
    # the clearing in hand, the weather turning: held, said, and kept held
    w, cap, ship, runner, p = _wrecked_cruising()
    cap.trend = "steady"
    assert w.submit("clear away the wreck of the main topmast").kind == "order.accepted"
    w.run(120)
    clearing = _clearing(w)
    assert clearing is not None and not clearing.paused and not clearing.waiting
    n0 = len(w.log)
    cap._hold_spar_work_for_weather(dataclasses.replace(_perceive(w), wind_kn=line + 5.0))
    assert clearing.paused and ship.extra.get(SPAR_WORK_WEATHER_HELD)
    crew = ship.extra["crew"]
    assert runner._spar_work_waits(ship, clearing, crew)
    w.run(1)
    assert "Belayed clearing away the wreck of the main topmast: hands kept for the weather." in [
        e.text for e in w.log[n0:]
    ]
    cap._hold_spar_work_for_weather(dataclasses.replace(_perceive(w), wind_kn=line - 5.0))
    assert SPAR_WORK_WEATHER_HELD not in ship.extra
    # held, it stands in no one's way: a lie a-try given after, sharing its main topsail, begins
    # (the brig of the rising wind waited behind it and was never brought to); and it is not
    # taken up again while that work is in hand
    cap._hold_spar_work_for_weather(dataclasses.replace(_perceive(w), wind_kn=line + 5.0))
    assert w.submit("lie a-try").kind == "order.accepted"
    lie = next(i for i in runner.instances if i.evo.id == "lie_a_try")
    assert lie.holds & clearing.holds
    runner.instances[:] = [clearing, lie]
    w.run(5)
    assert not lie.waiting, [e.text for e in w.log[-4:]]
    ship.extra.pop(SPAR_WORK_WEATHER_HELD, None)
    clearing.wanted_at = None
    assert runner._spar_work_waits(ship, clearing, crew)


def _perceive(w):
    from freesail.world.captains import Perception

    return Perception.read(w)


def test_truth_7_777_f_all_hands_for_a_wreck_at_the_hour_in_settled_weather_and_piped_down():
    """A wreck that has hung an hour with her watch never free has all hands turned up for it,
    at the hour and not before, in settled weather only and never as she is brought to; and
    the hands are piped down when it is cleared (the lead's list of 2026-11-27, items 1, 3 and
    4; the reader's mutants N05, the call at once, N06, never, and N12, no pipe-down)."""
    import dataclasses

    from freesail.world.captains import WRECK_HANDS_UP_S

    assert WRECK_HANDS_UP_S == 3600
    w, cap, ship, runner, p = _wrecked_cruising(keep_waiting=True)
    assert any(i.waiting for i in runner.instances), "her trims wait for hands"
    cap.trend = "steady"
    line = float(cap._th("shorten_sail_kn", 30.0))
    settled = dataclasses.replace(p, wind_kn=line - 5.0)
    cap._business["wreck_since"] = p.tick - WRECK_HANDS_UP_S + 1
    assert cap._spar_work(ship, settled, set(), runner) is None
    cap._business["wreck_since"] = p.tick - WRECK_HANDS_UP_S
    for heavy in (
        dataclasses.replace(settled, wind_kn=line),
        settled,  # the weather worsening, below
    ):
        if heavy is settled:
            cap.trend = "worsening"
        assert cap._spar_work(ship, heavy, set(), runner) is None
        assert not cap._business.get("hands_up_for_wreck")
    cap.trend = "steady"
    cap._business["brought_to_at"] = p.tick
    assert cap._spar_work(ship, settled, set(), runner) is None
    assert cap._spar_work(ship, settled, {"lie_a_try"}, runner) is None
    cap._business.pop("brought_to_at")
    got = cap._spar_work(ship, settled, set(), runner)
    assert got == ("call all hands", "to clear away the wreck of the main topmast"), got
    assert cap._business.get("hands_up_called")
    # called, and the wreck cleared: piped down
    w.submit("call all hands")
    for _ in range(20):
        w.run(30)
        if ship.extra["crew"].all_hands_called:
            break
    assert ship.extra["crew"].all_hands_called
    for sp in ship.spars.values():
        if sp.wrecked:
            sp.sent_down = True
    got = cap._spar_work(ship, dataclasses.replace(_perceive(w), wind_kn=line - 5.0), set(), runner)
    assert got == ("pipe down", "the wreck cleared away"), got


def test_truth_7_777_g_the_wreck_cleared_that_took_her_head_sails_a_head_sail_is_set():
    """The wreck cleared that took the head sails she had set, a head sail still standing is
    set once, the order said with its reason, in settled weather (the reader's mutant N13, the
    head sail after the clearing dropped, survived)."""
    from freesail.ship.parts import SailState

    w, cap, ship, runner, p = _wrecked_cruising("fore.topmast", ship_file="seventy-four")
    cap.trend = "steady"
    heads = list(ship.groups.get("headsails", []))
    from freesail.evolutions.scripts import gone_spar

    lost = [sid for sid in heads if gone_spar(ship, ship.sails[sid]) is not None]
    standing = [sid for sid in heads if sid not in lost]
    assert lost and standing, (lost, standing)
    for sid in standing:
        ship.sails[sid].state = SailState.FURLED
    for sp in ship.spars.values():
        if sp.wrecked:
            sp.sent_down = True
    cap._business["was_set"] = lost
    runner.instances[:] = []
    import dataclasses

    settled = dataclasses.replace(p, wind_kn=float(cap._th("shorten_sail_kn", 30.0)) - 5.0)
    got = cap._spar_work(ship, settled, set(), runner)
    assert got is not None and got[1] == "to keep her head off, her head sails gone", got
    assert got[0] == f"set the {cap._sail_name(standing[0])}", got
    # once for each clearing
    assert cap._spar_work(ship, settled, set(), runner) != got


def test_truth_7_778_b_a_refused_bringing_to_is_given_again_at_ten_minutes_and_then_rests():
    """Lying to for the weather and not brought to, his refused order to bring her to is given
    again ten minutes after the last and not sooner (`BRING_TO_AGAIN_S`); refused again in the
    same words with her sail as it was, it is not given a third time while her sail is
    unchanged; her sail changed, it is given again (the lead's list of 2026-11-27, item 1; the
    reader's mutants N07, never again, and N08, for ever, survived)."""
    import dataclasses
    import types

    from freesail.world.captains import BRING_TO_AGAIN_S

    assert BRING_TO_AGAIN_S == 600
    w = _gale("cutter", 270)
    w.run(60)
    cap = w.captain
    given: list[tuple[int, str]] = []

    def refuse(text, why=""):
        given.append((w.clock.tick, text))
        return types.SimpleNamespace(kind="order.rejected", text="She will not lie to.")

    cap.give = refuse
    cap.state = "hove to for weather"
    runner = w.ship.extra["evolutions"]
    runner.instances[:] = []
    w.ship.extra.pop("hove_to", None)
    t0 = w.clock.tick
    cap._bring_to_for_weather()
    p = dataclasses.replace(_perceive(w), manoeuvre="none")
    for dt in range(60, 3601, 60):
        w.clock.tick = t0 + dt
        cap._bring_to_again(dataclasses.replace(p, tick=t0 + dt))
    ticks = [t - t0 for t, _ in given]
    assert ticks == [0, BRING_TO_AGAIN_S], ticks
    # her sail changed: given again
    sail = next(
        s for s in w.ship.sails.values() if not s.is_set and s.state is parts.SailState.FURLED
    )
    sail.state = parts.SailState.SET
    w.clock.tick = t0 + 3660
    cap._bring_to_again(dataclasses.replace(p, tick=t0 + 3660))
    assert [t - t0 for t, _ in given] == [0, BRING_TO_AGAIN_S, 3660]


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
    the order said with its reason, and drifts at under two and a half knots. What she can lie
    a-try under is a fact of the sail, not of the moment (the lead's list of 2026-11-27, item
    2): a topsail of the mast she lies to with, standing, bent, of working canvas, with reef
    bands or in her plain sail; the brig's, the frigate's and the bilander's are, the
    cutter's of light canvas is not, and she heaves to, her topsail taken in first and kept."""
    heaving = "By the captain, hove to for weather: heaving to (no topsail to lie a-try under)."
    for wind in (270, 55):
        w = _gale("smack", wind)
        w.run(int(1.5 * 3600))
        said = _captains(w, 0)
        refused = [e for e in w.log if e.kind == "order.rejected" and "lie a-try" in e.text]
        assert refused == [], [e.text for e in refused]
        assert heaving in said, said
        assert not any("lying a try" in x for x in said), said
        hove = [e for e in w.log if e.kind == "ship.hove_to"]
        assert hove and "under her fore-and-aft canvas" in hove[0].text, (wind, hove)
        assert 3540 <= hove[0].tick <= 3540 + 900
        speeds = []
        for _ in range(30):
            w.run(60)
            speeds.append(float(w.readings.value("speed")) * 1.943844)
        assert max(speeds) < 2.5 and w.captain.state == "hove to for weather", (wind, speeds)
    # the cutter's topsail is of light canvas (No. 6, `LIE_A_TRY_CANVAS_NO`): laid to under it
    # in forty knots it blew out; she takes it in and heaves to under her fore-and-aft canvas,
    # and keeps it
    w = _gale("cutter", 270)
    w.run(int(2.5 * 3600))
    said = _captains(w, 0)
    assert not any("lying a try" in x for x in said), said
    assert (
        "By the captain, hove to for weather: taking in the topsail (to heave to under her "
        "fore-and-aft canvas)." in said
    ), said
    assert any(x.startswith(heaving[:-2]) for x in said), said
    hove = [e for e in w.log if e.kind == "ship.hove_to"]
    assert hove and "under her fore-and-aft canvas" in hove[0].text, hove
    assert not any(e.kind == "sail.blown_out" for e in w.log)
    # her topsail unbent is as her topsail furled: she heaves to
    w = _gale("smack", 270)
    w.ship.sails["topsail"].state = parts.SailState.UNBENT
    w.run(int(1.5 * 3600))
    assert heaving in _captains(w, 0), _captains(w, 0)
    # a fact of the sail: the smack's light topsail (no reef band, outside her plain sail) is
    # never one to lie under, furled, loosed or set; nor the cutter's, of No. 6; the brig's and the
    # bilander's (in her plain sail and reefed, of No. 2) always are, furled or set
    w = _gale("smack", 270)
    for state in (parts.SailState.FURLED, parts.SailState.LOOSED, parts.SailState.SET):
        w.ship.sails["topsail"].state = state
        assert not w.captain._topsail_to_lie_under(), state
    for ship in ("bilander", "brig", "frigate-36"):
        w = _gale(ship, 270)
        assert w.captain._topsail_to_lie_under(), ship
    w = _gale("cutter", 270)
    assert not w.captain._topsail_to_lie_under()
    # a boat has none; nor has a ship whose topmast is gone with its yard: the privateer with her
    # fore topmast carried away is given `heave to`, not `lie a-try` refused over and over
    w = _gale("boat-cutter-28", 270)
    assert not w.captain._topsail_to_lie_under()
    w = _gale("privateer-schooner", 270)
    assert w.captain._topsail_to_lie_under()
    _carry_away(w, "fore.topmast")
    assert not w.captain._topsail_to_lie_under()
    # a topsail in hand, lowered for its reefs at the gale's line, is not a topsail stowed: the
    # bilander lies a-try under it, as she did
    w = _gale("bilander", 270)
    w.run(int(2.5 * 3600))
    said = _captains(w, 0)
    assert "By the captain, hove to for weather: lying a try." in said, said
    assert not any("no topsail to lie a-try under" in x for x in said)
    assert any(e.text.startswith("Lying a-try under the main topsail") for e in w.log)


# -- the spar's work leaves her no worse off --------------------------------------------------


def _three_hours_on(ship: str, spar: str, spar_work: bool, monkeypatch) -> dict:
    """Her way through the third hour after a spar carried away out of action, how often she
    was taken aback, and what the captain said, with his spar work or without it (the trunk's
    captain, who left the spar as it fell)."""
    from freesail.world import captains as C

    given: list[dict] = []
    if not spar_work:
        monkeypatch.setattr(C.Captain, "_spar_work", lambda self, *a, **k: None)
    else:
        real = C.Captain._spar_work

        def watched(self, ship_, p, in_hand, runner):
            got = real(self, ship_, p, in_hand, runner)
            if got is not None:
                given.append(
                    {
                        "order": got[0],
                        "manoeuvre": p.manoeuvre,
                        "headway": p.headway,
                        "u": float(ship_.dyn.u),
                        "in_hand": len(getattr(runner, "instances", []) or []),
                    }
                )
            return got

        monkeypatch.setattr(C.Captain, "_spar_work", watched)
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
        "given": given,
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
    # every order of the spar's work given with her under command, a light spar's with
    # nothing at all in hand
    from freesail.physics.hull import HELM_STEERAGE_SPEED
    from freesail.world.captains import light_spar

    assert on["given"], on["given"]
    for g in on["given"]:
        assert g["manoeuvre"] == "none" and g["headway"], g
        assert g["u"] >= HELM_STEERAGE_SPEED, g
        named = g["order"].removeprefix("shift the ")
        light = [
            sp
            for sp in w.ship.spars.values()
            if light_spar(w.ship, sp) and w.captain._sail_name(sp.id) == named
        ]
        if g["order"].startswith("shift the ") and light:
            assert g["in_hand"] == 0, g


# -- the spar's work against the trunk, in four winds (the lead's probe) ----------------------

PASSAGE = """
name: a spar carried away on passage
seed: {seed}
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
{wind}
  background:
    {{hpa: 1012, gradient_hpa_per_100km: 1.2, high_toward_deg: 200}}
  sea: true
orders:
  - set plain sail
"""
# The lead's four winds (from the west, she bound north): twelve knots; twenty-five; twelve with
# the wind heading her four points at forty minutes (half an hour after the spar went); twenty
# rising to thirty-eight from forty to seventy minutes.
PASSAGE_WINDS: dict[str, list[tuple[str, int, int]]] = {
    "12": [("04:00", 270, 12), ("04:50", 270, 12), ("09:00", 270, 12)],
    "25": [("04:00", 270, 25), ("09:00", 270, 25)],
    "12-heading": [("04:00", 270, 12), ("04:40", 270, 12), ("04:45", 330, 12), ("09:00", 330, 12)],
    "20-38": [("04:00", 270, 20), ("04:40", 270, 20), ("05:10", 270, 38), ("09:00", 270, 38)],
}
# The spar carried away at minute ten, by ship: the lead's four and the three of truth 7-779.
PASSAGE_SPARS = {
    "bilander": "fore.topmast",
    "merchant-brig": "main.topmast",
    "topsail-schooner": "fore.topmast",
    "frigate-36": "main.topmast",
    "cutter": "main.topmast",
    "brig": "main.topmast",
    "seventy-four": "fore.topmast",
}
# The reader's five seeds of the third read (the lead's list of 2026-11-27, item 4).
PASSAGE_SEEDS = (3, 7, 8, 9, 11)
FALMOUTH = (50.15, -5.07)


def _from_falmouth_nm(lat: float, lon: float) -> float:
    import math

    dlat = math.radians(FALMOUTH[0] - lat)
    dlon = math.radians(FALMOUTH[1] - lon) * math.cos(math.radians((lat + FALMOUTH[0]) / 2))
    return math.hypot(dlat, dlon) * 3437.75


def _spar_passage(ship: str, wind: str, seed: int, how: str) -> dict:
    """Three hours bound for Falmouth after `PASSAGE_SPARS[ship]` carried away at minute ten:
    her way made good toward Falmouth (nm), the minutes she went astern, how often she was
    taken aback, and the tick she was brought to (lying a-try or hove to) or None. `how`:
    "mine" this tree's captain; "trunk" the trunk's captain (the spar's work, the bring-to
    given again and the narrowed `lie a-try` patched out: shown equal to the trunk in every
    line and position on every cell, the report's section 8); "instant" the trunk's captain
    with the wreck cleared the moment it fell, no hands spent and no time (its sails to the
    sail room, its spars sent down)."""
    from freesail.evolutions.scripts import wreck_root
    from freesail.world import captains as C

    names = (
        "_spar_work",
        "_bring_to_again",
        "_topsail_to_lie_under",
        "_hold_spar_work_for_weather",
    )
    saved = {n: getattr(C.Captain, n) for n in names}
    if how in ("trunk", "instant"):
        C.Captain._spar_work = lambda self, *a, **k: None
        C.Captain._bring_to_again = lambda self, p: None
        C.Captain._topsail_to_lie_under = lambda self: True
        C.Captain._hold_spar_work_for_weather = lambda self, p: None
    try:
        lines = "\n".join(
            f"    - {{at: 1805-06-14T{at}, from_deg: {d}, knots: {k}"
            f"{', air_mass: neutral' if i == 0 else ''}}}"
            for i, (at, d, k) in enumerate(PASSAGE_WINDS[wind])
        )
        path = Path(tempfile.mkdtemp()) / "passage.yaml"
        path.write_text(PASSAGE.format(ship=ship, wind=lines, seed=seed), encoding="utf-8")
        sf = load_scenario(str(path))
        w = make_scenario_world(sf)
        begin(w, sf)
        w.run(600)
        s = w.ship
        ST._wreck_spar(s, ST.strain_state(s), s.spars[PASSAGE_SPARS[ship]], 2.0)
        if how == "instant":
            for sail in s.sails.values():
                if wreck_root(s, sail) is not None and sail.state is not parts.SailState.BLOWN_OUT:
                    sail.state = parts.SailState.UNBENT
            for sp in s.spars.values():
                if sp.wrecked:
                    sp.sent_down = True
        n0 = len(w.log)
        start = _from_falmouth_nm(w._position.lat_deg, w._position.lon_deg)
        astern = 0
        for _ in range(180):
            w.run(60)
            if float(s.dyn.u) < -0.05:
                astern += 1
        log = w.log[n0:]
        return {
            "made_good": start - _from_falmouth_nm(w._position.lat_deg, w._position.lon_deg),
            "astern": astern,
            "aback": sum(1 for e in log if e.kind == "ship.aback"),
            "brought_to": next((e.tick for e in log if e.kind == "ship.hove_to"), None),
            "world": w,
        }
    finally:
        for n, f in saved.items():
            setattr(C.Captain, n, f)


# "Not worse", judged seed by seed (the lead's list of 2026-11-27 for part two, item 4 (a), and
# his ruling of the same afternoon on the rule's own fault): on each cell-seed against the trunk,
# or against its yardstick where that is the wreck cleared at once: minutes astern not more than
# five beyond, times aback not more than one beyond (JUDGEMENT: the least counts of each, as
# before), brought to not later than five minutes after (the lead's figure), and way made good
# not less by more than the price of the hands' work, `PASSAGE_WAY_SHARE` of the yardstick's way
# and never under
# `PASSAGE_WAY_FLOOR_NM` (JUDGEMENT: the lead's "a captain who cuts a wreck away and is a mile or
# two behind for it is a seaman", taken at its lower bound, a mile; and over a longer run a
# tenth, the wreck's clearing, an hour of her watch's work, costing her a third of her way for
# that hour of the three).
PASSAGE_ASTERN_MIN = 5
PASSAGE_ABACK = 1
PASSAGE_BROUGHT_S = 300
PASSAGE_WAY_SHARE = 0.10
PASSAGE_WAY_FLOOR_NM = 1.0
PASSAGE_CELLS = [(ship, wind) for ship in PASSAGE_SPARS for wind in PASSAGE_WINDS]
# The cell-seeds outside the rule, each with its cause (the report's section 9 says each in a
# sentence); the truth holds the set exactly, so that one more outside, or one of these come
# inside, fails it.
PASSAGE_DECLARED: dict[tuple[str, str, int], str] = {
    ("topsail-schooner", "20-38", 3): (
        "her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, "
        "which fails in thirty-eight knots or takes late, where the trunk's captain, refused "
        "`lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did "
        "not, and could not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("topsail-schooner", "20-38", 7): (
        "her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, "
        "which fails in thirty-eight knots or takes late, where the trunk's captain, refused "
        "`lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did "
        "not, and could not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("topsail-schooner", "20-38", 8): (
        "her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, "
        "which fails in thirty-eight knots or takes late, where the trunk's captain, refused "
        "`lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did "
        "not, and could not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("topsail-schooner", "20-38", 9): (
        "her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, "
        "which fails in thirty-eight knots or takes late, where the trunk's captain, refused "
        "`lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did "
        "not, and could not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("topsail-schooner", "20-38", 11): (
        "her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, "
        "which fails in thirty-eight knots or takes late, where the trunk's captain, refused "
        "`lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did "
        "not, and could not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("cutter", "20-38", 3): (
        "her topsail of light canvas, she is hove to under her fore-and-aft canvas where the "
        "trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's "
        "captain was not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("cutter", "20-38", 7): (
        "her topsail of light canvas, she is hove to under her fore-and-aft canvas where the "
        "trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's "
        "captain was not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("cutter", "20-38", 8): (
        "her topsail of light canvas, she is hove to under her fore-and-aft canvas where the "
        "trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's "
        "captain was not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("cutter", "20-38", 9): (
        "her topsail of light canvas, she is hove to under her fore-and-aft canvas where the "
        "trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's "
        "captain was not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("cutter", "20-38", 11): (
        "her topsail of light canvas, she is hove to under her fore-and-aft canvas where the "
        "trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's "
        "captain was not (the lead's ruling of 2026-11-27, (a))"
    ),
    ("frigate-36", "25", 7): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): "
        "aback eleven times against eight in her wears; 4.65 nm against 4.23, 15 minutes astern "
        "against 19"
    ),
    ("frigate-36", "20-38", 3): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) "
        "before the rise: given `lie a-try` at the trunk's tick, she lies a-try 545 s after it; "
        "13.29 nm against 12.34"
    ),
    ("brig", "20-38", 3): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) "
        "just before the rise: given `lie a-try` at the trunk's tick, she comes round through "
        "the wind as she is brought up and lies a-try 689 s after it; 10.61 nm against 2.70, 18 "
        "minutes astern against 44"
    ),
    ("seventy-four", "25", 7): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): "
        "117 minutes astern against the wreck cleared at once's 111 and the trunk's 96"
    ),
    ("seventy-four", "20-38", 3): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) "
        "before the rise: 7.30 nm against the trunk's 8.58 and the wreck cleared at once's "
        "11.17, 97 minutes astern as the latter's"
    ),
    ("topsail-schooner", "12-heading", 11): (
        "the clearing in hand through her wear and her tack, the hands turned up for it at the "
        "hour: 21 minutes astern against 15, and 8.98 nm made good against 6.64"
    ),
    ("cutter", "12-heading", 7): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) "
        "before the wind headed her: 175 minutes astern against 165 (astern most of the three "
        "hours whatever is done), aback once against three, -0.87 nm against -1.37"
    ),
    ("cutter", "12-heading", 9): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): "
        "178 minutes astern against 172, the wreck cleared at once's 177"
    ),
    ("seventy-four", "12-heading", 8): (
        "the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): "
        "144 minutes astern against 138, the wreck cleared at once's 143"
    ),
}


def _way_margin(way: float) -> float:
    return max(PASSAGE_WAY_FLOOR_NM, PASSAGE_WAY_SHARE * abs(way))


def _worse(a: dict, b: dict) -> list[str]:
    """How `a` is worse than `b` beyond the rule's allowances, by measure."""
    out = []
    if a["made_good"] < b["made_good"] - _way_margin(b["made_good"]):
        out.append("way")
    if a["astern"] > b["astern"] + PASSAGE_ASTERN_MIN:
        out.append("astern")
    if a["aback"] > b["aback"] + PASSAGE_ABACK:
        out.append("aback")
    return out


def _short_of(mine: dict, y: dict) -> list[str]:
    """How this tree's captain falls short of a yardstick: worse beyond the allowances, or
    brought to more than five minutes after it."""
    why = _worse(mine, y)
    if y["brought_to"] is not None and (
        mine["brought_to"] is None or mine["brought_to"] > y["brought_to"] + PASSAGE_BROUGHT_S
    ):
        why.append("brought to late")
    return why


def _seed_verdict(trunk: dict, instant: dict, mine: dict) -> dict:
    """One cell-seed judged by the lead's rulings of 2026-11-27: she passes where she is not
    worse than the trunk; or, where the wreck cleared at once is the yardstick (itself worse
    than the trunk beyond the allowances: a wreck hanging pays some hulls off like a head sail,
    the carried list, fault 22), where she is not worse than that. And wherever the trunk's
    captain brings her to, so does this one, without exception."""
    by = "instant" if _worse(instant, trunk) else "trunk"
    why = _short_of(mine, trunk)
    if why and by == "instant" and not _short_of(mine, instant):
        why = []
    if trunk["brought_to"] is not None and mine["brought_to"] is None:
        why.append("not brought to")
    return {"by": by, "why": why}


@pytest.mark.slow
@pytest.mark.parametrize(("ship", "wind"), PASSAGE_CELLS)
def test_truth_7_779_b_her_spar_carried_away_she_does_no_worse_than_the_trunk_on_passage(
    ship, wind
):
    """The lead's list of 2026-11-27 for package 126, part two, items 1 and 4, and his ruling
    of the same day: bound for Falmouth from 48 40 N 5 05 W, a spar carried away at minute ten,
    three hours, in twelve knots, twenty-five, twelve with the wind heading her and twenty
    rising to thirty-eight, on the bilander, the merchant brig, a topsail schooner, the
    frigate, the cutter, the brig and the seventy-four, on five seeds: on every seed this
    tree's captain makes no less way (by more than the price of the hands' work), goes astern
    no longer and is taken aback no more often than the trunk's captain, or, where the wreck
    cleared at once is itself worse than the trunk, than that (`_seed_verdict`); is brought to
    not later than five minutes after it, and wherever the trunk's captain is. The cell-seeds
    outside are `PASSAGE_DECLARED`'s, exactly."""
    outside = {}
    for seed in PASSAGE_SEEDS:
        t, i, m = (_spar_passage(ship, wind, seed, how) for how in ("trunk", "instant", "mine"))
        v = _seed_verdict(t, i, m)
        if v["why"]:
            outside[seed] = (v, {k: (t[k], i[k], m[k]) for k in ("made_good", "astern", "aback")})
    declared = {sd for (sh, wd, sd) in PASSAGE_DECLARED if (sh, wd) == (ship, wind)}
    assert set(outside) == declared, outside


def test_truth_7_779_b_the_trunk_in_this_tree_is_the_trunk():
    """The stand-in `_spar_passage` runs for the trunk's captain (his spar work, the bring-to
    given again and the narrowed `lie a-try` patched out) is the trunk's own on a cell that
    carries a spar's work: these figures were the trunk's at f09fe283 (and the stand-in's, on
    all 84 cell-seeds, in every line and position: the report's section 8)."""
    got = _spar_passage("bilander", "20-38", 7, "trunk")
    assert (round(got["made_good"], 2), got["astern"], got["aback"], got["brought_to"]) == (
        8.9,
        21,
        1,
        6123,
    )
