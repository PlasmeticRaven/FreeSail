"""Water in the ship, the pumps and foundering (spec M7 §13; package 73;
`freesail/world/water.py`; the design in `docs/design/Design-WaterAndHealth.md`)."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import water as W

CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"


def _scenario(wind_kn: float = 12.0, speed: float = 5.0, sea: bool | None = None) -> Scenario:
    return Scenario(
        sea=sea,
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


def _hole(world, z_m: float, pounder: float = 12.0, side: str = "starboard") -> dict:
    """A shot hole written as 70's state (`combat.hits`), at so much against the upright
    waterline (negative below)."""
    from freesail.combat.hits import damage_of, shot_diameter_m

    keeper = damage_of(world.ship)
    hole = {
        "tick": world.clock.tick,
        "side": side,
        "x_m": 0.0,
        "z_m": z_m,
        "diameter_m": round(shot_diameter_m(pounder), 3),
        "pounder": pounder,
    }
    keeper.holes.append(hole)
    return hole


def test_the_orifice_law_gives_the_periods_figures():
    """An 18-pounder's hole half a metre under takes in some eighty-five tons an hour, a
    12-pounder carronade's a third of a metre under some fifty; nothing above the water."""
    from freesail.combat.hits import shot_diameter_m

    eighteen = W.orifice_t_per_h(shot_diameter_m(18.0), 0.5)
    twelve = W.orifice_t_per_h(shot_diameter_m(12.0), 0.33)
    assert 75.0 < eighteen < 95.0, eighteen
    assert 40.0 < twelve < 60.0, twelve
    assert W.orifice_t_per_h(0.13, 0.0) == 0.0


def test_a_shot_hole_below_the_waterline_fills_the_well_at_the_rate_the_hole_and_the_heel_give():
    """Spec M7 §15: a hole below the waterline fills the well by the orifice law; the
    carpenter reports the feet; the heel that lifts the hole's side out of the water slows
    it and the heel that buries it quickens it."""
    w = make_world(7, CUTTER, _scenario(wind_kn=0.1, speed=0.0))
    w.run(5)
    hole = _hole(w, z_m=-0.4, pounder=12.0, side="starboard")
    leaks = w.water.leaks()
    assert len(leaks) == 1 and leaks[0].kind == "shot hole"
    upright = leaks[0].t_per_h
    assert 40.0 < upright < 70.0, upright
    w.run(600)
    tons = w.water.state.tons
    assert 7.0 < tons < 12.0, tons  # ten minutes of it
    assert w.ship.hull.water_in_well_m == pytest.approx(tons / w.water.floor_m2())
    # the heel: buried on the starboard side the hole takes in more, lifted it takes less
    w.ship.dyn.heel = 0.087  # five degrees to starboard
    buried = w.water.leaks()[0].t_per_h
    w.ship.dyn.heel = -0.087
    lifted = w.water.leaks()[0].t_per_h
    assert buried > upright > lifted, (buried, upright, lifted)
    w.ship.dyn.heel = 0.0
    # the carpenter's report comes by the foot
    w.run(3600)
    rising = [e for e in w.log if e.kind == "well.rising"]
    assert rising and "a foot of water in the well" in rising[0].text
    assert hole.get("plugged") is None
    assert "shot hole between wind and water" in w.readings.words("leaks")


def test_the_pumps_hold_a_leak_with_hands_enough_and_not_with_fewer():
    """Spec M7 §15: the frigate's two chain pumps and two hand pumps (Falconer's figures)
    gain on an 18-pounder's hole with their full crews and lose with a quarter of them."""
    w = make_world(7, FRIGATE, _scenario(wind_kn=0.1, speed=0.0))
    w.run(5)
    _hole(w, z_m=-0.5, pounder=18.0)
    w.run(1800)
    gain = w.water.gain_t_per_h()
    assert 70.0 < gain < 100.0, gain
    e = w.submit("man the pumps")
    assert e.kind == "pumps.manned", e.text
    assert "Twelve hands" in e.text or "twelve hands" in e.text.lower()
    w.run(120)
    full = w.water.pumps.rate_t_per_h(w.water.pumps.hands())
    assert full > gain, (full, gain)
    assert any(e.kind == "pumps.gaining" for e in w.log)
    assert w.readings.value("pumps")["manned"]
    before = w.water.state.tons
    w.run(600)
    assert w.water.state.tons < before
    # three of the twelve: the chain pumps short, the lift under the leak
    men = w.water.pumps.hands()
    few = w.water.pumps.rate_t_per_h(men[:3])
    assert few < gain < full, (few, gain, full)
    assert w.submit("secure the pumps").kind == "pumps.secured"
    assert not w.water.pumps.manned
    assert all(s.at != W.PUMPS_ID for s in w.ship.extra["crew"].sailors)


def test_the_pumps_are_spelled_every_glass_and_suck_when_the_well_is_dry():
    """The men at the brakes are relieved every glass of themselves (the keeper's spell);
    with the leak stopped the pumps suck and the crews stand down with the line."""
    w = make_world(7, CUTTER, _scenario(wind_kn=0.1, speed=0.0))
    w.run(5)
    seam = w.water.start_seam(4.0, "a seam started")
    w.run(1800)
    w.submit("man the pumps")
    first = set(w.water.state.pumps_hands)
    w.run(W.SPELL_S + 30)
    second = set(w.water.state.pumps_hands)
    assert w.water.pumps.manned and second and second != first
    assert any(e.kind == "pumps.spelled" for e in w.log)
    assert w.submit("spell the pumps").kind == "pumps.spelled"
    seam["stopped"] = w.clock.tick
    w.run(900)
    sucked = [e for e in w.log if e.kind == "pumps.sucked"]
    assert sucked and "the pumps' crews stand down" in sucked[-1].text
    assert not w.water.pumps.manned and w.water.state.tons == 0.0


def test_a_sound_ship_in_a_breeze_makes_no_water_worth_a_line_and_the_watch_pumps_her_dry():
    """The seams in a seaway: a cutter under plain sail in twenty knots for a watch makes
    inches, never a foot, no line is written, and at the change of the watch the water is
    pumped unasked; the free surface takes nothing under four inches."""
    w = make_world(7, CUTTER, _scenario(wind_kn=22.0, speed=5.0, sea=True))
    w.submit("set plain sail")
    w.run(2 * 3600 - 300)  # the sea built and the ship rolling: the seams working
    st = w.water.state
    assert w.motion is not None and w.motion.roll_deg > W.SEAMS_ROLL_FREE_DEG
    assert any(lk.kind == "the seams" for lk in w.water.leaks())
    assert 0.0 < st.tons < 1.0  # a few hundredweight in two hours
    w.run(2 * 3600 + 420)  # the afternoon watch relieves the deck at noon
    assert w.ship.hull.water_in_well_m < W.FOOT_M / 3.0
    assert not [e for e in w.log if e.kind in ("well.rising", "pumps.gaining", "pumps.losing")]
    assert st.routine_pumped_tick is not None and st.tons < 0.5
    assert w.ship.hull.free_surface_m == 0.0 and w.ship.hull.gm_m == w.ship.hull.spec.gm_m


def test_the_free_surface_takes_from_the_metacentric_height_and_the_roll_reads_it():
    """A foot and a half of water in the cutter costs her metacentric height by the
    free-surface formula; the heel's balance and the motion's roll period read the lesser
    figure, and a dry well gives the file's."""
    from freesail.physics import hull as HP

    w = make_world(7, CUTTER, _scenario(wind_kn=12.0, speed=5.0, sea=True))
    w.run(5)
    gm_dry = w.ship.hull.gm_m
    assert gm_dry == w.ship.hull.spec.gm_m
    period_dry = w.motion.roll_period_s
    heel_dry = HP.equilibrium_heel(w.ship.hull, 2.0e5, 1.0e4)
    w.water.state.tons = 0.45 * w.water.floor_m2()  # 0.45 m in the well
    w.run(2)
    assert w.ship.hull.free_surface_m > 0.02
    assert w.ship.hull.gm_m < gm_dry
    assert w.motion.roll_period_s > period_dry
    assert HP.equilibrium_heel(w.ship.hull, 2.0e5, 1.0e4) > heel_dry
    w.water.pump_out()
    w.run(2)
    assert w.ship.hull.gm_m == gm_dry and w.motion.roll_period_s == pytest.approx(period_dry)


def test_a_ship_that_founders_does_so_with_the_log_saying_when_the_pumps_lost():
    """Spec M7 §15: the cutter with two carronade holes under water and her two hand pumps
    manned founders at half her displacement; the pumps' losing line gives the time the
    foundering line names; she lies awash with no way, her sails taken in, and the world
    flags the ship lost."""
    w = make_world(7, CUTTER, _scenario(wind_kn=12.0, speed=5.0))
    w.submit("set plain sail")
    w.run(900)  # the sail made, the hands free for the pumps
    _hole(w, z_m=-0.6, pounder=12.0, side="starboard")
    _hole(w, z_m=-0.5, pounder=12.0, side="larboard")
    assert w.submit("man the pumps").kind == "pumps.manned"
    for _ in range(6 * 60):
        w.run(60)
        if w.ship.extra.get("foundered"):
            break
    lost = [e for e in w.log if e.kind == "pumps.losing"]
    founder = [e for e in w.log if e.kind == "ship.foundered"]
    settling = [e for e in w.log if e.kind == "ship.settling"]
    assert lost and settling and founder, [
        e.kind for e in w.log if e.kind.startswith(("pumps", "ship"))
    ]
    assert "the pumps lost her at" in founder[0].text
    assert lost[0].ship_time.strftime("%H:%M") in founder[0].text
    assert w.water.state.tons >= W.FOUNDER_SHARE * w.water.displacement_t() - 1.0
    assert w.ship_lost
    w.run(120)
    assert w.ship.dyn.speed < 0.2
    assert all(not s.is_set for s in w.ship.sails.values())
    assert w.readings.words("water") == "foundered"
    e = w.submit("man the pumps")
    assert e.kind == "order.rejected" and "foundered" in e.text


def test_the_hatches_battened_stop_the_sea_shipped(monkeypatch):
    """The sea over open hatches is a source in a heavy sea and none when they are
    battened down; the evolution takes its hands and its ten minutes."""
    w = make_world(7, CUTTER, _scenario(wind_kn=12.0, speed=5.0))
    w.run(5)
    monkeypatch.setattr(w.water, "_sea_height_m", lambda: 4.5)
    assert any(lk.kind == "the sea" for lk in w.water.leaks())
    assert w.readings.words("hatches") == "open"
    e = w.submit("batten down the hatches")
    assert e.kind == "order.accepted", e.text
    w.run(60)
    assert any(lk.kind == "the sea" for lk in w.water.leaks())  # not yet
    w.run(700)
    assert w.readings.words("hatches") == "battened down"
    assert not any(lk.kind == "the sea" for lk in w.water.leaks())
    assert any(e.kind == "hatches.battened" for e in w.log)
    assert w.submit("batten down the hatches").kind == "order.rejected"
    assert w.submit("open the hatches").kind == "order.accepted"
    w.run(700)
    assert w.readings.words("hatches") == "open"


def test_the_directors_causes_act_through_the_keeper_and_the_pumped_out_form_is_doubted():
    """`aboard: a seam found working` starts a leak of two tons an hour (modelled now, not
    report-only); `aboard: the leak stopped` stops it; `aboard: the well pumped out` is
    doubted while the ship has pumps and hands to pump her out herself, and done with a
    reason; the pumps' refusal line of 68 is gone."""
    from freesail.world import orders as WO

    w = make_world(7, CUTTER, _scenario(wind_kn=12.0, speed=5.0))
    w.submit("set plain sail")
    w.run(5)
    e = w.world_order("aboard: a seam found working", "the test")
    assert "two tons an hour" in e.text or "2 tons an hour" in e.text
    assert any(lk.kind == "a seam" for lk in w.water.leaks())
    w.run(1800)
    assert w.water.state.tons > 0.5
    d = WO.doubt(w, WO.parse("aboard: the well pumped out"))
    assert d is not None and "man the pumps" in d
    e = w.world_order(
        "aboard: the well pumped out [reason: the watch has been at it all night]", "the test"
    )
    assert e.data["result"] == "done" and w.water.state.tons == 0.0
    assert WO.doubt(w, WO.parse("aboard: the leak stopped")) is None
    e = w.world_order("aboard: the leak stopped", "the test")
    assert e.data["result"] == "done"
    assert not any(lk.kind == "a seam" for lk in w.water.leaks())
    assert "no leak to stop" in WO.doubt(w, WO.parse("aboard: the leak stopped"))
    # the pumps' refusal of 68 retired: the order is the ship's own now, and pumps a dry
    # well until it sucks
    e = w.submit("pump ship")
    assert e.kind == "pumps.manned" and "not worked in this game" not in e.text


def test_the_well_and_the_water_replay_to_the_same_digest():
    """A game with a leak, the pumps manned and the hatches battened replays from its
    inputs to the same log and the same water."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    w = make_world(7, CUTTER, _scenario(wind_kn=14.0, speed=5.0))
    w.submit("set plain sail")
    w.run(60)
    w.world_order("aboard: a seam found working", "the test")
    w.run(1200)
    w.submit("man the pumps")
    w.submit("batten down the hatches")
    w.run(2400)
    back = replay.replay_world(w, ship_factory)
    assert back.log.digest() == w.log.digest()
    assert back.water.state.tons == pytest.approx(w.water.state.tons)
    assert back.water.pumps.manned == w.water.pumps.manned


def test_the_ship_files_carry_their_pumps_and_plugs_through_the_generator():
    """Every ship file names her pumps and her shot plugs with Falconer's figures: the
    frigate two chain pumps and two hand pumps, the brig one and two, the small craft hand
    pumps alone."""
    from freesail.ship.loader import load_spec

    counts = {}
    for stem in (
        "frigate-36",
        "brig",
        "cutter",
        "topsail-schooner",
        "merchant-brig",
        "lugger",
        "smack",
    ):
        spec = load_spec(f"data/ships/{stem}.yaml")
        kinds = [p.kind for p in spec.pumps]
        counts[stem] = (kinds.count("chain"), kinds.count("hand"), spec.crew.stores.shot_plugs)
        for p in spec.pumps:
            assert (p.tons_per_hour, p.hands) == ((80.0, 4) if p.kind == "chain" else (15.0, 2))
    assert counts["frigate-36"] == (2, 2, 40)
    assert counts["brig"] == (1, 2, 20)
    assert counts["cutter"] == (0, 2, 8)
    assert counts["smack"] == (0, 1, 2)
