"""Package 22: canvas (spec 3b §6).

Canvas numbers and the cloth ratings derived from them (Luce 1884 App. E); condition and
wear, the effective rating and the baggy luff; the sail room and the sail scripts that draw
on it; storm canvas and the occasional sails on both ships; and the gale of gate M2 item 9
with a worn royal against a new one (the mechanism behind truth 27).

Sail work is run with the runner alone and no physics, as in tests/test_evolutions.py; the
gale and the sails set at sea run through the real world.
"""

from __future__ import annotations

import math
import random
from types import SimpleNamespace

import pytest
import yaml

from freesail import orders, units
from freesail.api.queries import muster_lines
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner
from freesail.physics import strain as S
from freesail.physics.sails import compute_sail_forces
from freesail.physics.strain import apply_strain, strain_state
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import (
    CANVAS_CROSSWISE_LB_PER_IN,
    CLOTH_KN_PER_M2_NO2,
    SailState,
    SpareSail,
    canvas_strength,
    cloth_rating_for,
    sail_room,
)
from freesail.ship.schema import ShipFileError
from freesail.ship.stub import OrderError

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SHIPS = [FRIGATE, SCHOONER]

# The cloth ratings milestone 2 gave the sails of No. 2 canvas (the committed files before
# package 22: CLOTH_KN_PER_M2 0.9 for courses and topsails). Spec 3b §6.1: No. 2 keeps them.
M2_NO2_RATINGS = {
    FRIGATE: {
        "fore.course": 162.9,
        "fore.topsail": 188.1,
        "main.course": 200.7,
        "main.topsail": 231.3,
    },
    SCHOONER: {"fore.topsail": 76.5},
}

# Crosswise strength relative to No. 2, as docs/references/Tables.md §2 derives it.
TABLES_RELATIVE = {1: 1.12, 2: 1.00, 3: 0.88, 4: 0.81, 5: 0.76, 6: 0.71, 7: 0.67, 8: 0.57, 9: 0.53}


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def make_wind(from_deg: float = 90.0, knots: float = 3.0) -> Wind:
    params = WindParams.from_nautical(from_deg, knots, gustiness=0.0, variability=0.0)
    return Wind(params, random.Random(0))


def bare(path: str):
    ship = load_ship(path)
    return ship, Runner(ship), make_wind()


def run(runner, ship, wind, max_ticks: int = 6000) -> list:
    """Tick the runner (no physics) until nothing is in progress; the notes."""
    notes = []
    ticks = 0
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return notes


def texts(notes) -> list[str]:
    return [n[2] for n in notes]


def kinds(notes) -> list[str]:
    return [n[1] for n in notes]


def work(runner, ship, wind, evolution: str, sail: str, **params) -> list:
    runner.start(ship, evolution, sail, {"sail": sail, **params})
    return run(runner, ship, wind)


def world(path: str, knots: float, heading: float, speed: float = 4.0, seed: int = 7):
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
    )
    return make_world(seed, path, scenario)


# ---------------------------------------------------------------------------
# canvas numbers and cloth ratings (spec 3b §6.1)
# ---------------------------------------------------------------------------


def test_luce_appendix_e_strengths_relative_to_no_2():
    assert CANVAS_CROSSWISE_LB_PER_IN[2] == 420.0
    assert CANVAS_CROSSWISE_LB_PER_IN[8] == pytest.approx(240.0)  # 300 lb on 1.25 in
    assert CANVAS_CROSSWISE_LB_PER_IN[9] == pytest.approx(224.0)  # 280 lb on 1.25 in
    for no, rel in TABLES_RELATIVE.items():
        assert canvas_strength(no) == pytest.approx(rel, abs=0.005), no
    assert [canvas_strength(n) for n in range(1, 10)] == sorted(
        (canvas_strength(n) for n in range(1, 10)), reverse=True
    )


@pytest.mark.parametrize("path", SHIPS)
def test_no_2_canvas_keeps_the_milestone_2_ratings_exactly(path):
    """The derivation's identity: CLOTH_KN_PER_M2_NO2 is milestone 2's rating for courses
    and topsails, so every sail of No. 2 keeps its rating to the decimal."""
    assert CLOTH_KN_PER_M2_NO2 == 0.9
    ship = load_ship(path)
    for sid, rating in M2_NO2_RATINGS[path].items():
        sail = ship.sails[sid]
        assert sail.canvas_no == 2, sid
        assert sail.cloth_rating_kn == rating, sid
        assert cloth_rating_for(sail.area_m2, 2) == round(0.9 * sail.area_m2, 1) == rating


@pytest.mark.parametrize("path", SHIPS)
def test_every_sail_has_a_canvas_number_and_its_rating_follows_luce(path):
    ship = load_ship(path)
    for sail in ship.sails.values():
        assert sail.canvas_no in range(1, 10), sail.id
        expected = round(0.9 * canvas_strength(sail.canvas_no) * sail.area_m2, 1)
        assert sail.cloth_rating_kn == expected == sail.rating_kn, sail.id


def test_the_frigates_canvas_by_the_period_rule():
    ship = load_ship(FRIGATE)
    no = {sid: s.canvas_no for sid, s in ship.sails.items()}
    # courses and topsails 2 (Steel, Luce), the mizzen topsail 4 (Steel)
    assert {no[s] for s in ship.groups["courses"]} == {2}
    assert [no[f"{m}.topsail"] for m in ("fore", "main", "mizzen")] == [2, 2, 4]
    # topgallants 6 and 7 (Steel; Kipping: "in the royal navy ... No. 6"), royals 8 (Steel)
    assert [no[f"{m}.topgallant"] for m in ("fore", "main", "mizzen")] == [6, 6, 7]
    assert {no[s] for s in ship.groups["royals"]} == {8}
    assert no["mizzen.spanker"] == 2 and no["jib"] == 6 and no["flying_jib"] == 7
    # studding sails: Kipping's frigates, lower and topmast 6, topgallant 7
    assert no["fore.lower.studdingsail.starboard"] == 6
    assert no["main.topmast.studdingsail.larboard"] == 6
    assert no["fore.topgallant.studdingsail.starboard"] == 7
    # storm canvas 1 (Luce p. 171); the ringtail 5 (Kipping), the save-alls 7
    assert {no[s] for s in ship.groups["storm canvas"]} == {1}
    assert no["mizzen.ringtail"] == 5 and no["fore.save_all.larboard"] == 7


def test_the_schooners_canvas_by_the_same_heights():
    ship = load_ship(SCHOONER)
    no = {sid: s.canvas_no for sid, s in ship.sails.items()}
    assert no["fore.topsail"] == 2 and no["fore.topgallant"] == 6
    assert no["fore.sail"] == no["main.sail"] == no["jib"] == no["fore.staysail"] == 2
    assert no["flying_jib"] == 6 and no["main.gaff_topsail"] == 8
    assert no["main.storm_trysail"] == no["storm_jib"] == 1
    assert no["main.ringtail"] == 5 and no["main.water_sail"] == 7


# ---------------------------------------------------------------------------
# condition and wear (spec 3b §6.2)
# ---------------------------------------------------------------------------


def one_hour(ship) -> None:
    for _ in range(3600):
        apply_strain(ship, 1.0)


def test_canvas_wears_by_use_set_aback_flogging_and_not_furled():
    ship = load_ship(FRIGATE)
    set_, aback, flogging, furled = (ship.sails[s] for s in S_WEAR)
    set_.state = aback.state = SailState.SET
    aback.backed = True
    flogging.state = SailState.LOOSED
    strain_state(ship).flogging.add(flogging.id)
    one_hour(ship)
    assert S.CLOTH_WEAR_PER_HOUR_SET == 0.05
    assert set_.condition == pytest.approx(100.0 - 0.05)
    assert aback.condition == pytest.approx(100.0 - 0.15)
    assert flogging.condition == pytest.approx(100.0 - 0.15)
    assert furled.condition == 100.0
    assert ship.sails["fore.storm_staysail"].condition == 100.0  # in the sail room


S_WEAR = ("fore.topsail", "main.topsail", "mizzen.topsail", "fore.course")


def test_a_sail_set_on_a_spar_sent_down_does_not_wear():
    ship = load_ship(FRIGATE)
    ship.sails["main.royal"].state = SailState.SET
    ship.spars["main.royal_mast"].sent_down = True
    one_hour(ship)
    assert ship.sails["main.royal"].condition == 100.0


def test_the_effective_rating_and_blowing_out_of_a_worn_sail():
    ship = load_ship(FRIGATE)
    worn, new = ship.sails["fore.royal"], ship.sails["main.royal"]
    for sail in (worn, new):
        sail.state = SailState.SET
    worn.condition = 50.0
    assert worn.effective_cloth_rating_kn == pytest.approx(0.7 * worn.cloth_rating_kn)
    assert new.effective_cloth_rating_kn == new.cloth_rating_kn
    # the same pressure on both: 1.3 of each one's new rating
    worn.load_kn = 1.3 * worn.cloth_rating_kn
    new.load_kn = 1.3 * new.cloth_rating_kn
    assert worn.strain_ratio == pytest.approx(1.3 / 0.7)  # above BLOW_OUT_RATIO
    apply_strain(ship, 1.0)
    assert worn.state is SailState.BLOWN_OUT  # out of the bolt-ropes
    assert new.state is SailState.SET  # the new one rides it out, straining
    assert strain_state(ship).blown_out == ["fore.royal"]


def test_a_worn_sail_is_baggier_and_lies_less_close():
    ship = load_ship(FRIGATE)
    ship.dyn.heading = 0.0
    sail = ship.sails["jib"]
    sail.state = SailState.SET
    sail.sheet_angle = units.deg_to_rad(20.0)
    wind = Wind(WindParams.from_nautical(60.0, 12.0, gustiness=0.0, variability=0.0), None)
    compute_sail_forces(ship, wind)
    new_luff = ship.extra["luff_angle"]
    sail.condition = 25.0
    compute_sail_forces(ship, wind)
    worn_luff = ship.extra["luff_angle"]
    assert S.BAGGY_LUFF_DEG == 6.0
    assert math.degrees(worn_luff - new_luff) == pytest.approx(6.0 * 0.75)
    assert S.baggy_luff(ship.sails["main.course"]) == 0.0  # a new sail is not baggy


# ---------------------------------------------------------------------------
# the gale of gate M2 item 9, a worn royal against a new one (truth 27's mechanism)
# ---------------------------------------------------------------------------

ROYALS = ("fore.royal", "main.royal", "mizzen.royal")
# The No. 2 rating at which truth 27 holds, measured (docs in the package 22 report): the
# worn royals blow out and the new ones keep their cloth with CLOTH_KN_PER_M2_NO2 between
# about 0.30 and 0.36 kN/m2. The ship files keep spec 3b §6.1's 0.9; see the xfail below.
TRUTH_27_NO2_KN_PER_M2 = 0.36


def gale_royals(condition: float, no2_kn_per_m2: float = CLOTH_KN_PER_M2_NO2):
    """Gate M2 item 9 (35 knots, all sail made and braced up, the yards trimmed), with the
    royals at a condition and, optionally, rated as if No. 2 canvas bore `no2_kn_per_m2`.
    What happened to each royal first: 'blown_out' or 'yard' (its yard or mast went)."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=35.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=270.0,
        ship_speed_kn=0.0,
    )
    w = make_world(7, FRIGATE, scenario)
    for sid in ROYALS:
        sail = w.ship.sails[sid]
        sail.condition = condition
        sail.cloth_rating_kn *= no2_kn_per_m2 / CLOTH_KN_PER_M2_NO2
        sail.rating_kn = sail.cloth_rating_kn
    w.submit("make all sail")
    w.submit("brace up on the starboard tack")
    for i in range(2400):
        if i == 600:
            w.submit("make all sail")
            w.submit("trim sails")
        elif i in (1200, 1800):
            w.submit("trim sails")
        w.tick()
    first: dict[str, str] = {}
    for e in w.log:
        if e.kind == "sail.blown_out" and e.subject in ROYALS:
            first.setdefault(e.subject, "blown_out")
        elif e.kind == "spar.carried_away":
            for sid in ROYALS:
                if sid in e.data.get("wrecked", []):
                    first.setdefault(sid, "yard")
    return first


def test_worn_canvas_goes_before_its_spar_and_new_canvas_holds_until_the_spar_goes():
    """Spec 3b §6.5, truth 27's mechanism, through the physics alone: the effective rating,
    the strain decay and BLOW_OUT_RATIO. With the No. 2 rating at the measured value a royal
    of condition 50 blows out of its bolt-ropes before its yard goes, and a new royal holds
    until the yard goes, as at milestone 2."""
    assert gale_royals(100.0, TRUTH_27_NO2_KN_PER_M2) == {r: "yard" for r in ROYALS}
    assert gale_royals(50.0, TRUTH_27_NO2_KN_PER_M2) == {r: "blown_out" for r in ROYALS}


@pytest.mark.xfail(
    strict=True,
    reason="Truth 27 with the ship files' ratings: CLOTH_KN_PER_M2_NO2 = 0.9 (spec 3b §6.1's "
    "identity with milestone 2's untuned course and topsail rating) makes a No. 8 royal bear "
    "0.514 kN/m2; at condition 50 its cloth peaks at 0.84 of its effective rating in the gale "
    "and its yard goes first. The constant near 0.36 brings the truth; the owner's ruling.",
)
def test_truth_27_with_the_ship_files_ratings():
    assert gale_royals(100.0) == {r: "yard" for r in ROYALS}
    assert gale_royals(50.0) == {r: "blown_out" for r in ROYALS}


# ---------------------------------------------------------------------------
# the sail room (spec 3b §6.3)
# ---------------------------------------------------------------------------


def test_the_frigates_sail_room_is_luces_allowance():
    ship = load_ship(FRIGATE)
    room = sail_room(ship)
    kinds_in = [s.kind for s in room.sails]
    assert len(room) == 21 == ship.spec.crew.stores.spare_sails
    assert len(set(kinds_in)) == 21  # one spare of each kind
    heavy = {s.kind for s in room.sails if s.canvas_no == 1 and ship.sails[s.kind].canvas_no == 2}
    assert heavy == {"fore.course", "fore.topsail", "main.topsail"}  # Luce p. 171's note
    assert set(ship.groups["storm canvas"]) <= set(kinds_in)
    assert set(ship.groups["occasional sails"]) <= set(kinds_in)
    for s in room.sails:
        assert s.condition == 100.0
        if s.kind not in heavy:
            assert s.canvas_no == ship.sails[s.kind].canvas_no  # the working number
    # the studding sails and the main topmast staysail are not in the allowance
    assert "main.topmast_staysail" not in kinds_in
    assert not [k for k in kinds_in if k in ship.groups["studdingsails"]]


def test_the_schooners_sail_room():
    ship = load_ship(SCHOONER)
    kinds_in = [s.kind for s in sail_room(ship).sails]
    assert kinds_in[:3] == ["fore.sail", "fore.topsail", "jib"]
    assert set(kinds_in[3:]) == {"main.storm_trysail", "storm_jib", "main.ringtail"} | {
        "main.water_sail"
    }


def test_a_ship_file_with_only_a_count_has_made_up_sails():
    ship = load_ship(FRIGATE)
    ship.spec = SimpleNamespace(crew=SimpleNamespace(stores={"spare_sails": 2}))
    room = sail_room(ship)
    assert len(room) == 2 and all(s.kind is None for s in room.sails)
    assert room.choose("fore.royal") is room.sails[0]  # a made-up sail fits any yard


def test_shift_chooses_the_best_of_the_working_number_and_returns_the_old_sail():
    ship, runner, wind = bare(FRIGATE)
    room = sail_room(ship)
    room.stow(SpareSail(kind="main.course", canvas_no=2, condition=60.0))
    course = ship.sails["main.course"]
    course.condition = 72.5
    notes = work(runner, ship, wind, "shift_sail", "main.course")
    assert course.state is SailState.FURLED and course.condition == 100.0
    worn = [s for s in room.sails if s.kind == "main.course"]
    assert sorted(s.condition for s in worn) == [60.0, 72.5]  # the old one went below
    assert any("Swayed aloft the mainsail (No. 2 canvas, new)" in t for t in texts(notes))
    assert any(
        "Shifted the mainsail; the mainsail bent (No. 2 canvas, new)" in t for t in texts(notes)
    )


def test_shift_the_fore_topsail_for_the_heavy_one_and_back():
    ship, runner, wind = bare(FRIGATE)
    topsail = ship.sails["fore.topsail"]
    working_rating = topsail.cloth_rating_kn
    work(runner, ship, wind, "shift_sail", "fore.topsail", heavy=True)
    assert topsail.canvas_no == 1
    assert topsail.cloth_rating_kn == pytest.approx(working_rating * 470.0 / 420.0)
    below = [s for s in sail_room(ship).sails if s.kind == "fore.topsail"]
    assert [(s.canvas_no, s.condition) for s in below] == [(2, 100.0)]
    # the No. 2 back again: named by its number, as "bend the No. 2 fore topsail"
    work(runner, ship, wind, "shift_sail", "fore.topsail", canvas_no=2)
    assert topsail.canvas_no == 2 and topsail.cloth_rating_kn == pytest.approx(working_rating)


def test_bend_the_one_named_and_refuse_a_number_not_in_the_room():
    ship, runner, wind = bare(FRIGATE)
    work(runner, ship, wind, "unbend_sail", "main.topsail")
    with pytest.raises(OrderError, match="There is no main topsail of No. 3 canvas"):
        runner.start(ship, "bend_sail", "main.topsail", {"sail": "main.topsail", "canvas_no": 3})
    work(runner, ship, wind, "bend_sail", "main.topsail", canvas_no=1)
    assert ship.sails["main.topsail"].canvas_no == 1
    with pytest.raises(OrderError, match="no heavy-weather fore royal"):
        runner.start(ship, "shift_sail", "fore.royal", {"sail": "fore.royal", "heavy": True})


def test_the_unbent_sail_goes_below_with_its_condition():
    ship, runner, wind = bare(FRIGATE)
    ship.sails["fore.royal"].condition = 41.0
    notes = work(runner, ship, wind, "unbend_sail", "fore.royal")
    assert "Lowered the fore royal on deck and stowed it in the sail room." in texts(notes)
    royals = [s for s in sail_room(ship).sails if s.kind == "fore.royal"]
    assert sorted(s.condition for s in royals) == [41.0, 100.0]
    # bending again draws the better of the two
    work(runner, ship, wind, "bend_sail", "fore.royal")
    assert ship.sails["fore.royal"].condition == 100.0
    # a blown-out sail's rags are condemned, not stowed
    ship.sails["main.royal"].state = SailState.BLOWN_OUT
    before = len(sail_room(ship))
    work(runner, ship, wind, "unbend_sail", "main.royal")
    assert len(sail_room(ship)) == before


def test_the_muster_and_the_sail_room_query_lines():
    w = world(FRIGATE, 10.0, 90.0)
    room = sail_room(w.ship)  # the lead wires this into the session (package 22 report)
    lines = muster_lines(w)
    assert lines[-1] == room.muster_line()
    assert lines[-1].startswith("Sail room: 21 sails, 12 spares of the working canvas; ")
    assert "for heavy weather the foresail, fore topsail and main topsail" in lines[-1]
    assert (
        "the storm canvas (fore storm staysail, mizzen storm staysail and storm mizzen)"
        in (lines[-1])
    )
    inventory = room.inventory_lines()
    assert inventory[0] == "The sail room holds 21 sails."
    assert any(
        line.startswith("Storm canvas: fore storm staysail, No. 1 canvas") for line in inventory
    )
    w.ship.sails["jib"].condition = 30.0
    w.ship.sails["jib"].state = SailState.FURLED
    room.stow(SpareSail(kind="jib", canvas_no=6, condition=30.0))
    assert "the most worn, the jib, much worn" in room.muster_line()


# ---------------------------------------------------------------------------
# storm canvas and the occasional sails (spec 3b §6.4)
# ---------------------------------------------------------------------------


def test_the_storm_mizzen_needs_the_spanker_unbent():
    ship, runner, wind = bare(FRIGATE)
    with pytest.raises(
        OrderError, match=r"The spanker is bent in the storm mizzen's place; unbend"
    ):
        runner.start(ship, "bend_sail", "mizzen.storm_mizzen", {"sail": "mizzen.storm_mizzen"})
    notes = work(runner, ship, wind, "shift_sail", "mizzen.spanker", **{"for": "storm mizzen"})
    assert ship.sails["mizzen.spanker"].state is SailState.UNBENT
    assert ship.sails["mizzen.storm_mizzen"].state is SailState.FURLED
    assert ship.sails["mizzen.storm_mizzen"].canvas_no == 1
    assert "mizzen.spanker" in [s.kind for s in sail_room(ship).sails]
    assert any("the storm mizzen bent (No. 1 canvas, new)" in t for t in texts(notes))
    with pytest.raises(OrderError, match="The storm mizzen is bent in the spanker's place"):
        runner.start(ship, "bend_sail", "mizzen.spanker", {"sail": "mizzen.spanker"})
    with pytest.raises(OrderError, match="not bent in the jib's place"):
        runner.start(ship, "shift_sail", "jib", {"sail": "jib", "for": "mizzen.storm_mizzen"})
    work(runner, ship, wind, "shift_sail", "mizzen.storm_mizzen", **{"for": "mizzen.spanker"})
    assert ship.sails["mizzen.spanker"].state is SailState.FURLED


def runner_name(ship, sid: str) -> str:
    from freesail.evolutions import part_name

    return part_name(ship, sid)


def bend_in_place(runner, ship, wind, sid: str) -> None:
    """Bend a sail from the sail room, shifting the one it goes in place of if need be."""
    sail = ship.sails[sid]
    if sail.in_place_of and ship.sails[sail.in_place_of].state is not SailState.UNBENT:
        work(runner, ship, wind, "shift_sail", sail.in_place_of, **{"for": sid})
    else:
        work(runner, ship, wind, "bend_sail", sid)
    assert sail.state is SailState.FURLED


@pytest.mark.parametrize("path", SHIPS)
def test_every_new_sail_loads_bends_sets_and_takes_in(path):
    from freesail.api.session import make_ship

    ship = make_ship(path)  # with the orders, which refuse to set a sail still below
    runner, wind = ship.extra["evolutions"], make_wind()
    new = ship.groups["storm canvas"] + ship.groups["occasional sails"]
    assert new
    for sid in new:
        sail = ship.sails[sid]
        assert sail.state is SailState.UNBENT and sail.canvas_no is not None
        with pytest.raises(OrderError, match="is unbent; there is no sail on the yard"):
            orders.handle(ship, f"set the {runner_name(ship, sid)}")
        bend_in_place(runner, ship, wind, sid)
        if sail.cls == "studding":
            # it extends a sail: the course on its yard, or the gaff sail its boom rigs on
            with pytest.raises(OrderError, match="cannot be set until the sail"):
                runner.start(ship, "set_studding", sid)
            boom = ship.spar_of_role(sail, "boom")
            if sail.roles.get("yard"):
                beside = ship.sail_of(ship.yard_of(sail))  # a save-all: the foresail
            elif boom.cls == "boom":
                beside = ship.sail_of(boom)  # the water sail: the mainsail over it
            else:
                beside = ship.sail_of(ship.parent_of(boom))  # a ringtail: the gaff sail
            assert beside.state is not SailState.UNBENT
            work(runner, ship, wind, f"set_{beside.cls}", beside.id)
        work(runner, ship, wind, f"set_{sail.cls}", sid)
        assert sail.is_set, sid
        work(runner, ship, wind, f"take_in_{sail.cls}", sid)
        assert sail.state is not SailState.SET, sid
        if sail.cls == "studding":
            work(runner, ship, wind, f"take_in_{beside.cls}", beside.id)
        if sail.in_place_of:  # and the working sail bent again in its place
            work(runner, ship, wind, "shift_sail", sid, **{"for": sail.in_place_of})
            assert ship.sails[sail.in_place_of].state is SailState.FURLED
            assert sail.state is SailState.UNBENT


def test_the_ringtail_and_water_sail_draw_running():
    """The schooner running before 12 knots under her mainsail: the ringtail on its boom
    abaft the mainsail's leech and the water sail under the boom both draw."""
    w = world(SCHOONER, 12.0, 180.0, speed=5.0)
    runner = w.ship.extra["evolutions"]
    w.submit("set the mainsail")
    w.run(400)
    for sid in ("main.ringtail", "main.water_sail"):
        runner.start(w.ship, "bend_sail", sid, {"sail": sid})
    w.run(900)
    w.submit("set the ringtail")
    w.submit("set the water sail")
    w.run(900)
    for sid in ("main.ringtail", "main.water_sail"):
        sail = w.ship.sails[sid]
        assert sail.is_set, sid
        assert sail.thrust_kn > 0.0, sid


def test_new_parts_do_not_change_the_ratings_of_the_old_spars():
    """The rating pass leaves the sail room's canvas out: every spar the files had keeps
    its rating (the ringtail booms are rated for their ringtails, as studding sail booms)."""
    for path in SHIPS:
        doc = yaml.safe_load(open(path, encoding="utf-8"))
        ratings = {s["id"]: s["rating_kn"] for s in doc["spars"]}
        booms = [sid for sid in ratings if sid.endswith("ringtail_boom")]
        assert len(booms) == 1
        assert ratings[booms[0]] >= 1.0


# ---------------------------------------------------------------------------
# the ship file format
# ---------------------------------------------------------------------------


def frigate_doc() -> dict:
    return yaml.safe_load(open(FRIGATE, encoding="utf-8"))


def test_the_loader_refuses_bad_canvas_in_words():
    doc = frigate_doc()
    doc["sails"][0]["canvas_no"] = 12
    with pytest.raises(ShipFileError, match=r"canvas is numbered 1 \(the heaviest\) to 9"):
        ship_from_dict(doc)
    doc = frigate_doc()
    doc["crew"]["stores"]["sails"].append({"kind": "main.skysail", "canvas_no": 8})
    with pytest.raises(ShipFileError, match="made for 'main.skysail', which is not a sail"):
        ship_from_dict(doc)
    doc = frigate_doc()
    doc["crew"]["stores"]["spare_sails"] = 3
    with pytest.raises(ShipFileError, match="give the list alone"):
        ship_from_dict(doc)
    doc = frigate_doc()
    storm = next(s for s in doc["sails"] if s["id"] == "mizzen.storm_mizzen")
    storm["in_place_of"] = "mizzen.spinnaker"
    with pytest.raises(ShipFileError, match="in place of 'mizzen.spinnaker'"):
        ship_from_dict(doc)
    doc = frigate_doc()
    doc["crew"]["stores"]["sails"][0]["condition"] = 140
    with pytest.raises(ShipFileError, match="condition runs from 0"):
        ship_from_dict(doc)


# ---------------------------------------------------------------------------
# determinism
# ---------------------------------------------------------------------------


def test_the_same_seed_gives_the_same_log_with_canvas_work():
    def voyage():
        w = world(FRIGATE, 22.0, 90.0, seed=11)
        w.submit("set plain sail")
        w.run(600)
        w.submit("take in the spanker")
        w.run(300)
        w.ship.extra["evolutions"].start(
            w.ship,
            "shift_sail",
            "mizzen.spanker",
            {"sail": "mizzen.spanker", "for": "storm mizzen"},
        )
        w.run(1500)
        w.submit("set the storm mizzen")
        w.run(900)
        conditions = {sid: s.condition for sid, s in w.ship.sails.items()}
        return w.log.digest(), conditions, [(s.kind, s.condition) for s in sail_room(w.ship).sails]

    a, b = voyage(), voyage()
    assert a == b
    assert a[1]["main.topsail"] < 100.0  # worn by use
    assert a[1]["mizzen.storm_mizzen"] < 100.0
    assert ("mizzen.spanker", pytest.approx(a[1]["mizzen.spanker"])) in [
        (k, pytest.approx(c)) for k, c in a[2]
    ]


def test_orders_still_reach_the_square_sail_scripts():
    ship = load_ship(FRIGATE)
    from freesail.api.session import make_ship

    ship = make_ship(FRIGATE)
    ship.sails["fore.royal"].state = SailState.BLOWN_OUT
    orders.handle(ship, "shift the fore royal")
    assert [i.evo.id for i in ship.extra["evolutions"].instances] == ["shift_sail"]
