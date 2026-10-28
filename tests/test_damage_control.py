"""Damage control and jury work (spec M7 §14; package 73; `freesail/evolutions/
repair_scripts.py`, `freesail/orders/damage.py`, the damage report of
`freesail/api/action_readings.py`; the design in `docs/design/Design-WaterAndHealth.md`)."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.api.session import make_world
from freesail.combat.hits import damage_of, shot_diameter_m
from freesail.core.world import Scenario
from freesail.evolutions import repair_scripts as RS
from freesail.physics import strain as ST
from freesail.ship import parts
from freesail.ship.parts import LineState

CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"


def _scenario(wind_kn: float = 10.0, speed: float = 4.0) -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=wind_kn,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth"],
        nation="britain",
        ship_heading_deg=180.0,
        ship_speed_kn=speed,
    )


def _world(ship: str = CUTTER, sail: bool = True):
    w = make_world(7, ship, _scenario())
    if sail:
        w.submit("set plain sail")
        w.run(900)
    else:
        w.run(5)
    return w


def _hole(world, z_m: float, side: str = "starboard", pounder: float = 12.0) -> dict:
    keeper = damage_of(world.ship)
    hole = {
        "tick": world.clock.tick,
        "side": side,
        "x_m": 1.0,
        "z_m": z_m,
        "diameter_m": round(shot_diameter_m(pounder), 3),
        "pounder": pounder,
    }
    keeper.holes.append(hole)
    return hole


def _shoot_away(world, line) -> None:
    ST._part_line(world.ship, ST.strain_state(world.ship), line, 1.2, how="shot away")


def _events(world, *kinds: str) -> list:
    return [e for e in world.log if e.kind in kinds]


def test_the_carpenter_plugs_the_holes_worst_first_in_the_time_the_bill_says():
    """Spec M7 §15: the carpenter plugs a hole in the time the bill says (twenty minutes
    for one at or just under the water, ten above), the worst leak first, a plug a hole
    from his store; a plugged hole flows no more and the report says it is plugged."""
    w = _world()
    under = _hole(w, -0.3, "starboard")
    above = _hole(w, 0.8, "larboard")
    assert w.water.gain_t_per_h() > 30.0
    assert RS.shot_plugs(w.ship).count == 8
    e = w.submit("plug the shot holes")
    assert e.kind == "order.accepted", e.text
    start = w.clock.tick
    for _ in range(60):
        w.run(60)
        if under.get("plugged") is not None:
            break
    took = under["plugged"] - start
    assert 1200 <= took <= 1500, took  # twenty minutes, the crew factor over it
    assert above.get("plugged") is None  # the dry hole after the wet one
    assert w.water.gain_t_per_h() == 0.0
    w.run(900)
    assert above.get("plugged") is not None
    assert RS.shot_plugs(w.ship).count == 6
    plugged = _events(w, "hole.plugged")
    assert len(plugged) == 3 and "a plug driven in" in plugged[0].text
    assert "plugged" in w.readings.words("damage")
    e = w.submit("plug the shot holes")
    assert e.kind == "order.rejected" and "no shot hole" in e.text


def test_reeve_new_lines_roves_every_parted_running_line_in_turn_and_the_report_names_them():
    """The owner's form (his first action, 2026-10-24): `reeve new lines` roves every
    parted running line in turn, the damage report naming each parted line and what to
    do with it, the standing rigging left to `set up the rigging`."""
    w = _world()
    ship = w.ship
    halyard = next(ln for ln in ship.lines.values() if ln.cls == "halyard")
    brace = next(ln for ln in ship.lines.values() if ln.cls == "brace")
    shroud = next(ln for ln in ship.lines.values() if ln.cls == "shroud")
    e = w.submit("reeve new lines")
    assert e.kind == "order.rejected" and "No running line is parted" in e.text
    for ln in (halyard, brace, shroud):
        _shoot_away(w, ln)
    report = w.readings.words("damage")
    for ln in (halyard, brace):
        assert w.readings.value("damage")["running_parted"].count(ln.id) == 1
    assert "to be rove: 'reeve new lines'" in report
    assert "standing rigging, to be set up" in report
    parted = w.readings.value("parted_lines")
    assert parted["running"] == [halyard.id, brace.id] and parted["standing"] == [shroud.id]
    e = w.submit("reeve new lines")
    assert e.kind == "order.accepted", e.text
    w.run(1)  # the runner's own line; the second reeve waits on the yard the first serves
    started = [x for x in w.log if x.kind == "evolution.started" and x.tick >= e.tick]
    assert len(started) >= 1 and "Reeve a new" in started[0].text, [x.text for x in started]
    w.run(1800)
    assert halyard.state is LineState.BELAYED and brace.state is LineState.BELAYED
    assert shroud.state is LineState.PARTED
    assert len(_events(w, "line.rove")) == 2
    assert w.readings.value("parted_lines")["running"] == []


def test_the_standing_rigging_shot_away_is_set_up_again_in_the_bills_time_from_the_cordage():
    """A shroud shot away is set up again with deadeyes and lanyards in three quarters of
    an hour by ten hands, a new rope from the boatswain's store; refused for a sound line
    and for running rigging."""
    w = _world(FRIGATE)
    ship = w.ship
    shrouds = [ln for ln in ship.lines.values() if ln.cls == "shroud"]
    backstay = next(ln for ln in ship.lines.values() if ln.cls == "backstay")
    e = w.submit("set up the rigging")
    assert e.kind == "order.rejected" and "nothing to set up" in e.text
    _shoot_away(w, shrouds[0])
    _shoot_away(w, backstay)
    fathoms = parts.cordage(ship).fathoms
    e = w.submit("set up the rigging")
    assert e.kind == "order.accepted", e.text
    start = w.clock.tick
    w.run(2 * 3600)
    assert shrouds[0].state is LineState.BELAYED and backstay.state is LineState.BELAYED
    done = _events(w, "rigging.set_up")
    assert len(done) == 3 and done[0].tick - start >= 2700
    assert parts.cordage(ship).fathoms < fathoms
    e = w.submit("set up the rigging")
    assert e.kind == "order.rejected"
    sheet = next(ln for ln in ship.lines.values() if ln.cls == "sheet")
    _shoot_away(w, sheet)
    e = w.submit(f"set up the {ship.lines[sheet.id].id.replace('.', ' ')}")
    assert e.kind == "order.rejected"


def test_a_sprung_spar_is_fished_and_stands_at_seventy_at_most():
    """A sprung topmast fished and woolded in three quarters of an hour aloft stands at
    seventy of a hundred; a sound spar and a wrecked one are refused in words."""
    w = _world()
    spar = w.ship.spars["main.topmast"]
    e = w.submit("fish the topmast")
    assert e.kind == "order.rejected" and "sound enough" in e.text
    spar.condition = 40.0
    assert "main topmast sprung" in w.readings.words("damage")
    e = w.submit("fish the topmast")
    assert e.kind == "order.accepted", e.text
    w.run(3600)
    assert spar.condition == pytest.approx(RS.FISHED_CONDITION)
    assert _events(w, "spar.fished")
    assert "sprung" not in w.readings.words("damage")


def test_the_preventers_hold_a_brace_shot_away_and_cost_the_cordage():
    """The preventer braces rove before an action: a brace shot away keeps its office (the
    preventer takes it, consumed, a line of its own), and the preventers take their
    fathoms from the boatswain's store; refused when the store has not the rope."""
    w = _world(FRIGATE)
    ship = w.ship
    braces = [ln for ln in ship.lines.values() if ln.cls == "brace"]
    fathoms = parts.cordage(ship).fathoms
    e = w.submit("rig preventer braces")
    assert e.kind == "order.accepted", e.text
    w.run(2400)
    lower = [
        ln
        for ln in braces
        if ship.parent_of(ship.parts[ln.of]) is not None
        and ship.parent_of(ship.parts[ln.of]).cls in ("mast", "topmast")
    ]
    assert lower and all(ln.preventer for ln in lower)
    assert not all(ln.preventer for ln in braces)  # the light yards aloft go without
    braces = lower
    assert parts.cordage(ship).fathoms < fathoms
    assert _events(w, "preventers.rigged")
    _shoot_away(w, braces[0])
    assert braces[0].state is not LineState.PARTED and not braces[0].preventer
    w.run(1)  # the ship's note reaches the log at the tick
    held = _events(w, "line.preventer_held")
    assert held and "the preventer holds" in held[0].text
    _shoot_away(w, braces[0])
    assert braces[0].state is LineState.PARTED
    e = w.submit("rig preventer braces")
    assert e.kind == "order.rejected"
    # a store without the rope is refused in words
    c = _world(CUTTER)
    parts.cordage(c.ship).fathoms = 2.0
    e = c.submit("rig preventer braces")
    assert e.kind == "order.rejected" and "fathoms" in e.text


def test_the_chain_slings_and_the_preventer_backstays_are_rigged():
    w = _world(FRIGATE)
    ship = w.ship
    e = w.submit("sling the yards")
    assert e.kind == "order.accepted", e.text
    e = w.submit("rig preventer backstays")
    assert e.kind == "order.accepted", e.text
    w.run(3600)
    backstays = [ln for ln in ship.lines.values() if ln.cls == "backstay"]
    assert all(ln.preventer for ln in backstays)
    slung = [
        ln
        for ln in ship.lines.values()
        if ln.cls in ("halyard", "tye", "lift") and getattr(ln, "preventer", False)
    ]
    assert slung


def test_a_mast_cut_away_goes_over_the_side_and_a_jury_mast_stands_in_its_stump():
    """A standing lower mast cut away by the axes is wrecked and cleared with all it
    carried; a jury mast from the spare topmast stands in its stump in four hours at two
    fifths of the mast's strength, its course to be bent; refused without a spare."""
    w = _world()
    ship = w.ship
    mast = ship.spars["main.mast"]
    e = w.submit("rig a jury mast")
    assert e.kind == "order.rejected" and "no lower mast is carried away" in e.text
    e = w.submit("cut away the mainmast")
    assert e.kind == "order.accepted", e.text
    w.run(1500)
    assert mast.wrecked and mast.sent_down
    assert _events(w, "mast.cut_away")
    assert "carried away" in w.readings.words("damage")
    rating = mast.rating_kn
    assert parts.booms(ship).have("topmast") == 1
    e = w.submit("rig a jury mast")
    assert e.kind == "order.accepted", e.text
    w.run(7 * 3600)
    assert not mast.wrecked and mast.jury
    assert mast.rating_kn == pytest.approx(rating * RS.JURY_RATING_SHARE)
    assert mast.condition == RS.JURY_CONDITION
    assert parts.booms(ship).have("topmast") == 0
    assert ship.spars["main.topmast"].wrecked  # still down
    assert "a jury mast" in w.readings.words("damage")
    done = _events(w, "mast.jury")
    assert done and any("stepped in the stump" in x.text for x in done)
    e = w.submit("rig a jury mast")
    assert e.kind == "order.rejected"


def test_a_sail_fothered_over_the_leak_slows_it_and_goes_when_she_makes_way():
    """A spare sail thrummed and hauled under the bottom lets through three tenths of
    the leak while the sail holds, and goes when she makes more than six knots."""
    w = _world(sail=False)
    hole = _hole(w, -0.6, pounder=3.0)  # a 3-pounder's hole, which her two hand pumps hold
    assert 15.0 < w.water.gain_t_per_h() < 30.0
    assert w.submit("man the pumps").kind == "pumps.manned"
    spares = len(parts.sail_room(w.ship))
    e = w.submit("fother a sail over the leak")
    assert e.kind == "order.accepted", e.text
    w.run(3 * 3600)
    st = w.water.state
    assert st.fothered and len(parts.sail_room(w.ship)) == spares - 1
    fothered = w.water.gain_t_per_h()
    st.fothered = False
    bare = w.water.gain_t_per_h()
    st.fothered = True
    assert bare > 0.0 and fothered == pytest.approx(bare * 0.3)
    assert _events(w, "leak.fothered")
    w.ship.dyn.u = 4.0  # her surge, metres a second: near eight knots
    w.run(2)
    assert not w.water.state.fothered and _events(w, "leak.fother_gone")
    assert hole.get("plugged") is None


def test_the_ground_leak_is_caulked_by_the_carpenter_in_his_hours():
    """`stop the leak` with no hole: the ground's leak and a started seam found and
    caulked in three hours, the keeper's leak stopped and the line said."""
    w = _world()
    w.water.start_seam(3.0, "a seam started")
    w.ship.extra["leak_m_per_h"] = 0.05
    assert w.water.gain_t_per_h() > 3.0
    e = w.submit("stop the leak")
    assert e.kind == "order.accepted", e.text
    w.run(4 * 3600)
    assert w.water.gain_t_per_h() == 0.0 or all(lk.kind == "the seams" for lk in w.water.leaks())
    assert w.ship.extra["leak_m_per_h"] == 0.0
    stopped = _events(w, "leak.stopped")
    assert stopped and "found and stopped" in stopped[0].text


def test_every_repair_is_an_evolution_with_hands_and_competes_for_them():
    """The repairs are the runner's evolutions: each takes its hands from the pool and a
    second piece of work on the same hold waits its turn; the catalogue's files load with
    their scripts."""
    from freesail.evolutions import registry
    from freesail.evolutions.scripts import SCRIPTS

    for evo_id in RS.REPAIR_SCRIPTS:
        evo = registry.get(evo_id)
        assert evo is not None and evo.script in SCRIPTS, evo_id
        assert evo.crew.get("hands"), evo_id
        assert evo.source
    w = _world()
    _hole(w, -0.3)
    _hole(w, -0.2, "larboard")
    w.submit("plug the shot holes")
    w.run(5)
    at = [s for s in w.ship.extra["crew"].sailors if s.at and "plug" in s.at]
    assert len(at) >= 2
    e = w.submit("stop the leak")
    assert e.kind == "evolution.queued" and "will follow" in e.text
