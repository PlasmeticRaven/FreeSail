"""The lug sail and its dip (package 43b; spec M6 §19; the proposal's §4.4).

The lugger Éclair (`data/ships/lugger.yaml`, Forfait 1788's Table VII) carries dipping lugs
on her fore and main masts and a standing lug for a mizen. A dipping lug is slung at a
third of its yard on one side of the mast with two thirds of its cloth to leeward; its tack
and sheet cannot change roles, so in going about it is lowered, its yard passed round the
mast and its tack shifted, and hoisted again on the new lee side (Forfait pp. 5 to 6;
Lescallier 1791 pp. 391 to 392; Steel 1794 vol. I, LUGGER). Left on the weather side it lies
against the mast and draws badly (`physics.sails.LUG_AGAINST_MAST_AREA`). The tack and the
wear dip the lugs as part of the manoeuvre, not at once; `dip the <lug>` is the order by
itself. A lug's yard has no braces: it is no yard of `brace` or `trim the yards`.
"""

from __future__ import annotations

import math

import pytest

from freesail.physics.sails import LUG_AGAINST_MAST_AREA, compute_sail_forces
from freesail.ship.loader import load_ship
from freesail.ship.parts import SailState
from tests.test_known_truths import make, run, settle

LUGGER = "data/ships/lugger.yaml"


@pytest.fixture(scope="module")
def by_the_wind():
    """The lugger under plain sail on the starboard tack, sixty degrees off a fifteen-knot
    northerly, settled (the module's one sailing; each test takes a copy of its state by
    sailing on from a fresh world where it must)."""
    world = make(LUGGER, 300.0)
    settle(world, ["set plain sail", "brace sharp up on the starboard tack"])
    return world


def test_the_lugs_are_hoisted_to_leeward_and_their_yards_are_not_braced():
    ship = load_ship(LUGGER)
    assert not any(sp.is_yard for sp in ship.spars.values() if sp.cls == "lug_yard")
    world = make(LUGGER, 300.0)  # starboard tack: the lee side is larboard
    settle(world, ["set plain sail", "brace sharp up on the starboard tack"], ticks=200)
    lugs = {s.id: s for s in world.ship.sails.values() if s.cls == "lug"}
    assert lugs["fore.lug"].is_set and lugs["main.lug"].is_set and lugs["mizen.lug"].is_set
    assert lugs["fore.lug"].lug_side == "larboard" and lugs["main.lug"].lug_side == "larboard"
    for e in world.log:
        assert "lug yard" not in e.text, e.text  # no brace order reaches a lug's yard


def test_a_dipping_lug_against_the_mast_draws_two_thirds(by_the_wind):
    ship = by_the_wind.ship
    main = ship.sails["main.lug"]
    compute_sail_forces(ship, by_the_wind.wind)
    clear = main.area_effective_m2
    main.lug_side = "starboard"  # the weather side on the starboard tack
    try:
        compute_sail_forces(ship, by_the_wind.wind)
        against = main.area_effective_m2
    finally:
        main.lug_side = "larboard"
    assert against == pytest.approx(LUG_AGAINST_MAST_AREA * clear, rel=0.02)
    # the standing mizen is not dipped and loses nothing on either side
    mizen = ship.sails["mizen.lug"]
    compute_sail_forces(ship, by_the_wind.wind)
    before = mizen.area_effective_m2
    mizen.lug_side = "starboard"
    compute_sail_forces(ship, by_the_wind.wind)
    assert mizen.area_effective_m2 == pytest.approx(before)
    mizen.lug_side = "larboard"


def test_a_tack_lowers_the_lugs_and_dips_them_and_takes_time():
    world = make(LUGGER, 300.0)
    settle(world, ["set plain sail", "brace sharp up on the starboard tack"])
    start = world.clock.tick
    world.submit("tack ship")
    lowered_at = hoisted_at = None
    for _ in range(600):
        world.tick()
        main = world.ship.sails["main.lug"]
        if lowered_at is None and main.state is SailState.IN_THE_GEAR:
            lowered_at = world.clock.tick
        if lowered_at is not None and hoisted_at is None and main.is_set:
            hoisted_at = world.clock.tick
    texts = [e.text for e in world.log if e.tick > start]
    assert any("lower the foresail and the mainsail" in t for t in texts), texts
    assert any(t.startswith("Dipped the foresail and the mainsail") for t in texts)
    tacked = [e for e in world.log if e.tick > start and e.kind == "ship.tacked"]
    assert tacked, texts
    assert lowered_at is not None and hoisted_at is not None
    assert hoisted_at - lowered_at >= 90  # not instant: down while she goes about, then dipped
    assert tacked[0].tick >= hoisted_at  # the tack is done when the lugs are up again
    for sid in ("fore.lug", "main.lug"):
        assert world.ship.sails[sid].lug_side == "starboard"  # the larboard tack's lee side
    assert world.ship.dyn.tack == "larboard"


def test_the_dip_by_itself_shifts_a_lug_left_against_the_mast():
    world = make(LUGGER, 300.0)
    settle(world, ["set plain sail", "brace sharp up on the starboard tack"])
    fore = world.ship.sails["fore.lug"]
    world.submit("dip the foresail")  # on the lee side already
    run(world, 200)
    refused = [e.text for e in world.log if "lies to leeward of its mast already" in e.text]
    assert refused
    fore.lug_side = "starboard"  # as if she had come round with no dip
    start = world.clock.tick
    world.submit("dip the foresail")
    run(world, 400)
    done = [e for e in world.log if e.tick > start and e.kind == "sail.dipped"]
    assert done, [e.text for e in world.log if e.tick > start]
    assert 120 <= done[0].tick - start <= 360  # lowered, shifted, hoisted: minutes, not a tick
    assert fore.lug_side == "larboard" and fore.is_set
    world.submit("dip the mizen")
    run(world, 200)
    assert any("standing lug" in e.text for e in world.log if e.tick > start)


def test_she_heaves_to_with_her_lugs_lowered():
    world = make(LUGGER, 300.0)
    settle(world, ["set plain sail", "brace sharp up on the starboard tack"])
    start = world.clock.tick
    world.submit("heave to")
    run(world, 600)
    assert any(e.kind == "ship.hove_to" for e in world.log if e.tick > start), [
        e.text for e in world.log if e.tick > start and e.severity != "routine"
    ]
    assert world.ship.sails["fore.lug"].state is SailState.IN_THE_GEAR
    assert world.ship.sails["main.lug"].state is SailState.IN_THE_GEAR
    assert math.degrees(abs(world.ship.dyn.u)) >= 0.0
