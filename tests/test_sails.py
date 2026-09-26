"""Package 4: wind and sail physics (freesail/physics/sails.py)."""

from __future__ import annotations

import copy
import math
import random

import pytest

from freesail import units
from freesail.physics import sails as S
from freesail.physics.sails import SAIL_CLASSES, SailForces, compute_sail_forces
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import SailState
from tests.test_ship_loader import MINIMAL

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def make_wind(from_deg: float, knots: float) -> Wind:
    """A steady wind. The stream is never stepped, so nothing here is random."""
    return Wind(WindParams.from_nautical(from_deg, knots, 0.0, 0.0), random.Random(0))


def minimal_ship():
    return ship_from_dict(copy.deepcopy(MINIMAL), "minimal")


def set_sails(ship, ids, brace_deg=0.0, sheet_deg=None):
    for s in ship.sails.values():
        s.state = SailState.FURLED
    for sid in ids:
        ship.sails[sid].state = SailState.SET
    for sp in ship.spars.values():
        if sp.is_yard:
            limit = sp.brace_limit if sp.brace_limit > 0 else math.pi / 2
            sp.brace_angle = math.copysign(min(abs(math.radians(brace_deg)), limit), brace_deg)
    if sheet_deg is not None:
        for s in ship.sails.values():
            if s.is_fore_and_aft:
                s.sheet_angle = math.radians(sheet_deg)


def frigate_plain_sail(brace_deg=38.0, sheet_deg=25.0, speed_kn=0.0):
    ship = load_ship(FRIGATE)
    set_sails(ship, ship.groups["plain sail"], brace_deg=brace_deg, sheet_deg=sheet_deg)
    ship.dyn.u = units.knots_to_ms(speed_kn)
    return ship


# ---------------------------------------------------------------------------
# the class tables
# ---------------------------------------------------------------------------


def test_every_sail_class_has_a_curve():
    assert set(SAIL_CLASSES) == {
        "square",
        "gaff",
        "jibheaded",
        "lug",
        "lateen",
        "sprit",
        "studding",
    }
    for cls in SAIL_CLASSES.values():
        assert cls.alpha[0] == 0.0 and cls.alpha[-1] == pytest.approx(math.pi / 2)
        assert cls.lift[0] == 0.0 and cls.lift[-1] == 0.0
        assert max(cls.lift) >= 1.0 and 1.0 <= cls.drag[-1] <= 1.3
        assert 0 < cls.luff_angle < math.radians(20)
        assert 0 <= cls.reef_factor <= 0.5 and 0 <= cls.furled_windage <= 0.2
        assert cls.notes


def test_curves_interpolate_and_fold():
    # the values here are the package 10 tuning (docs/dev/TuningNotes.md): the
    # foot of every curve is dead below about ten degrees, and the peaks are
    # those of coarse flax sails, not aerofoils
    sq = SAIL_CLASSES["square"]
    assert sq.coefficients(0.0) == (0.0, pytest.approx(0.10))
    # milestone 3b moved the square curve five degrees up: the peak is at 40, the foot at 15
    cl, cd = sq.coefficients(math.radians(40))
    assert cl == pytest.approx(1.12) and 0.45 <= cd <= 0.55
    assert sq.coefficients(math.radians(15))[0] == 0.0  # a square sail shakes under fifteen degrees
    # halfway between two table points is the mean of their values
    cl_mid, _ = sq.coefficients(math.radians(22.5))
    assert cl_mid == pytest.approx((0.12 + 0.42) / 2)
    # negative and over-range angles are folded
    assert sq.coefficients(-math.radians(35)) == sq.coefficients(math.radians(35))
    assert sq.coefficients(math.radians(120))[0] == 0.0
    assert SAIL_CLASSES["gaff"].coefficients(math.radians(30))[0] == pytest.approx(1.25)


# ---------------------------------------------------------------------------
# apparent wind
# ---------------------------------------------------------------------------


def test_deck_apparent_wind_is_written():
    ship = minimal_ship()
    ship.dyn.heading = math.radians(30)
    wind = make_wind(75, 12)  # 45° on the starboard bow
    compute_sail_forces(ship, wind)
    assert ship.dyn.apparent_wind_angle == pytest.approx(math.radians(45))
    deck = ship.hull.spec.deck_height_m + S.WIND_EYE_HEIGHT_M
    assert ship.dyn.apparent_wind_speed == pytest.approx(wind.speed_at_height(deck))
    assert ship.dyn.tack == "starboard"
    # ship's own speed draws the apparent wind ahead and larboard is negative
    ship.dyn.heading = 0.0
    ship.dyn.u = units.knots_to_ms(6)
    compute_sail_forces(ship, make_wind(270, 12))
    assert -math.radians(90) < ship.dyn.apparent_wind_angle < -math.radians(45)
    assert ship.dyn.tack == "larboard"


# ---------------------------------------------------------------------------
# contract cases
# ---------------------------------------------------------------------------


def mirror(f: SailForces) -> tuple[float, ...]:
    return (f.thrust_n, -f.side_n, -f.heel_moment_nm, -f.yaw_moment_nm, f.windage_drag_n)


def as_tuple(f: SailForces) -> tuple[float, ...]:
    return (f.thrust_n, f.side_n, f.heel_moment_nm, f.yaw_moment_nm, f.windage_drag_n)


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_symmetric_on_either_tack(path):
    ship = load_ship(path)
    plain = list(ship.groups["plain sail"])
    set_sails(ship, plain, brace_deg=38, sheet_deg=20)
    ship.dyn.u = units.knots_to_ms(4)
    starboard = compute_sail_forces(ship, make_wind(80, 15))
    per_sail_stb = {s.id: (s.thrust_kn, s.side_force_kn) for s in ship.sails.values()}
    set_sails(ship, plain, brace_deg=-38, sheet_deg=20)
    larboard = compute_sail_forces(ship, make_wind(280, 15))
    assert as_tuple(larboard) == pytest.approx(mirror(starboard), rel=1e-9, abs=1e-6)
    assert starboard.thrust_n > 0
    for s in ship.sails.values():
        assert s.thrust_kn == pytest.approx(per_sail_stb[s.id][0], abs=1e-9)
        assert s.side_force_kn == pytest.approx(-per_sail_stb[s.id][1], abs=1e-9)


def test_backed_square_sail_gives_negative_thrust_and_is_logged_once():
    ship = minimal_ship()
    set_sails(ship, ["topsail"], brace_deg=0)
    wind = make_wind(0, 15)  # dead ahead, yard square: the wind is on the fore face
    f = compute_sail_forces(ship, wind)
    sail = ship.sails["topsail"]
    assert f.thrust_n < 0 and sail.thrust_kn < 0
    assert sail.backed is True
    assert f.side_n == pytest.approx(0.0, abs=1e-6)
    notes = ship.drain_notes()
    assert [(n[1], n[3]) for n in notes] == [("sail.backed", "topsail")]
    assert notes[0][2] == "Topsail taken aback."
    compute_sail_forces(ship, wind)
    assert ship.drain_notes() == []  # no repeat while it stays aback
    # wind from astern fills it again
    compute_sail_forces(ship, make_wind(180, 15))
    assert sail.backed is False and sail.thrust_kn > 0
    assert [n[1] for n in ship.drain_notes()] == ["sail.filled"]


def test_braced_yard_is_backed_when_wind_is_forward_of_it():
    ship = minimal_ship()
    set_sails(ship, ["topsail"], brace_deg=40)  # starboard tack trim: chord 50° from the bow
    compute_sail_forces(ship, make_wind(70, 15))  # wind abaft the yard: drawing
    assert ship.sails["topsail"].backed is False and ship.sails["topsail"].thrust_kn > 0
    compute_sail_forces(ship, make_wind(30, 15))  # wind forward of the yard: aback
    assert ship.sails["topsail"].backed is True and ship.sails["topsail"].thrust_kn < 0


def test_fore_and_aft_sail_at_zero_angle_of_attack_gives_no_lift():
    ship = minimal_ship()
    set_sails(ship, ["mainsail"], sheet_deg=30)
    wind = make_wind(30, 15)  # wind along the chord
    f = compute_sail_forces(ship, wind)
    sail = ship.sails["mainsail"]
    q = 0.5 * units.RHO_AIR * wind.speed_at_height(sail.centre_height_m) ** 2
    drag_only = q * sail.area_m2 * SAIL_CLASSES["gaff"].drag[0]
    # nothing across the wind: the whole (small) force is drag along the wind
    assert sail.force_kn * 1000 == pytest.approx(drag_only, rel=1e-6)
    assert sail.thrust_kn * 1000 == pytest.approx(-drag_only * math.cos(math.radians(30)), rel=1e-6)
    assert f.thrust_n < 0  # that drag, plus windage, all pushes her astern
    # pinched further, with the wind on the lee face, the cloth collapses: still no lift
    compute_sail_forces(ship, make_wind(15, 15))
    assert sail.force_kn * 1000 == pytest.approx(drag_only, rel=1e-6)
    assert sail.backed is False


def test_fore_and_aft_sail_drawing_pulls_forward():
    ship = minimal_ship()
    set_sails(ship, ["mainsail", "jib"], sheet_deg=15)
    f = compute_sail_forces(ship, make_wind(50, 15))
    assert f.thrust_n > 0
    assert f.side_n < 0  # pushed to leeward (larboard) on the starboard tack
    assert f.heel_moment_nm < 0  # heels to larboard
    assert ship.sails["jib"].thrust_kn > 0 and ship.sails["mainsail"].thrust_kn > 0


def test_running_blanketed_sail_gives_less():
    ship = load_ship(FRIGATE)
    wind = make_wind(180, 15)  # dead astern, heading north
    set_sails(ship, ["fore.topsail"], brace_deg=0)
    fore = ship.sails["fore.topsail"]
    compute_sail_forces(ship, wind)
    alone = fore.thrust_kn * 1000
    assert fore.area_effective_m2 == pytest.approx(fore.area_m2)
    set_sails(ship, ["fore.topsail", "main.topsail"], brace_deg=0)
    both = compute_sail_forces(ship, wind)
    assert fore.area_effective_m2 == pytest.approx(fore.area_m2 * (1 - S.BLANKET_RUNNING))
    assert fore.thrust_kn * 1000 < alone
    assert fore.thrust_kn * 1000 == pytest.approx(alone * (1 - S.BLANKET_RUNNING), rel=1e-6)
    main = ship.sails["main.topsail"]
    assert main.area_effective_m2 == pytest.approx(main.area_m2)  # nothing to windward of it
    assert both.thrust_n > alone + main.thrust_kn * 1000 * 0.9  # two sails still beat one
    # with the wind four points on the quarter the fore topsail is clear of the main
    ship.dyn.heading = math.radians(45)
    compute_sail_forces(ship, wind)
    assert fore.area_effective_m2 == pytest.approx(fore.area_m2)


def test_dead_before_the_wind_is_slower_than_four_points_off():
    """Truth 5 at the force level: courses and topsails, same wind, same speed."""
    ship = load_ship(FRIGATE)
    sails = ship.groups["courses"] + ship.groups["topsails"]
    ship.dyn.u = units.knots_to_ms(6)
    set_sails(ship, sails, brace_deg=0)
    dead = compute_sail_forces(ship, make_wind(180, 15)).thrust_n
    set_sails(ship, sails, brace_deg=15)
    quartering = compute_sail_forces(ship, make_wind(135, 15)).thrust_n
    assert 0 < dead < quartering


def test_force_scales_with_wind_speed_squared():
    ship = frigate_plain_sail(brace_deg=30, sheet_deg=25)
    ten = compute_sail_forces(ship, make_wind(100, 10))
    twenty = compute_sail_forces(ship, make_wind(100, 20))
    assert as_tuple(twenty) == pytest.approx(tuple(4 * x for x in as_tuple(ten)), rel=1e-9)
    for s in ship.sails.values():
        assert s.area_effective_m2 >= 0


def test_frigate_beam_reach_in_15_knots_gives_kilonewtons_of_thrust():
    # Milestone 3b: the square curve's peak moved five degrees later, and at this fixed brace
    # the drive fell from tens of kilonewtons to about six; the beam-reach truths (3, 4), which
    # trim the yards to the wind, still make eight knots, so the floor here is the sanity band.
    ship = frigate_plain_sail(brace_deg=38, sheet_deg=25, speed_kn=7)
    f = compute_sail_forces(ship, make_wind(90, 15))
    assert 4_000 < f.thrust_n < 100_000
    assert f.side_n < 0  # to leeward, larboard
    assert f.heel_moment_nm < 0


# ---------------------------------------------------------------------------
# area: reefs, heel, sail state, wrecks
# ---------------------------------------------------------------------------


def test_reefs_and_heel_reduce_the_working_area():
    ship = minimal_ship()
    set_sails(ship, ["mainsail"], sheet_deg=20)
    wind = make_wind(80, 15)
    sail = ship.sails["mainsail"]
    compute_sail_forces(ship, wind)
    full = sail.thrust_kn
    assert full > 0
    assert sail.area_effective_m2 == pytest.approx(sail.area_m2)
    sail.reefs = 1
    compute_sail_forces(ship, wind)
    one = sail.thrust_kn
    assert sail.area_effective_m2 == pytest.approx(sail.area_m2 * 0.75)
    assert one == pytest.approx(full * 0.75, rel=1e-9)
    sail.reefs = 5  # more than it has bands: clamped
    compute_sail_forces(ship, wind)
    assert sail.area_effective_m2 == pytest.approx(sail.area_m2 * 0.5)
    sail.reefs = 0
    ship.dyn.heel = math.radians(30)
    compute_sail_forces(ship, wind)
    assert sail.area_effective_m2 == pytest.approx(sail.area_m2 * math.cos(math.radians(30)))


def test_only_set_sails_drive():
    ship = minimal_ship()
    wind = make_wind(120, 15)
    for state in SailState:
        ship.sails["topsail"].state = state
        compute_sail_forces(ship, wind)
        driving = ship.sails["topsail"].thrust_kn > 0
        # a goose-winged sail draws with half its cloth (spec M3 §6, package 19)
        assert driving == (state in (SailState.SET, SailState.GOOSE_WINGED)), state


def test_wrecked_or_sent_down_spar_stops_its_sail():
    ship = minimal_ship()
    set_sails(ship, ["topsail"], brace_deg=0)
    wind = make_wind(180, 15)
    assert compute_sail_forces(ship, wind).thrust_n > 0
    ship.spars["topmast"].sent_down = True
    f = compute_sail_forces(ship, wind)
    assert ship.sails["topsail"].thrust_kn == 0 and ship.sails["topsail"].area_effective_m2 == 0
    ship.spars["topmast"].sent_down = False
    ship.spars["topmast"].wrecked = True
    g = compute_sail_forces(ship, wind)
    assert ship.sails["topsail"].thrust_kn == 0
    assert g.windage_drag_n > f.windage_drag_n  # a wreck catches more wind than a sent-down mast


def test_windage_opposes_the_wind_and_bare_poles_push_astern():
    ship = load_ship(FRIGATE)  # everything furled
    f = compute_sail_forces(ship, make_wind(0, 30))
    assert f.windage_drag_n > 0
    assert f.thrust_n == pytest.approx(-f.windage_drag_n, rel=1e-9)  # all of it dead aft
    assert f.side_n == pytest.approx(0.0, abs=1e-6)
    # from astern the same drag pushes her ahead; from abeam it heels and pushes sideways
    aft = compute_sail_forces(ship, make_wind(180, 30))
    assert aft.thrust_n == pytest.approx(f.windage_drag_n, rel=1e-9)
    beam = compute_sail_forces(ship, make_wind(90, 30))
    assert beam.side_n < 0 and beam.heel_moment_nm < 0
    # sending down the topgallant masts reduces the windage
    for sp in ship.spars.values():
        if sp.cls in {"topgallant_mast", "royal_mast"}:
            sp.sent_down = True
    assert compute_sail_forces(ship, make_wind(0, 30)).windage_drag_n < f.windage_drag_n


# ---------------------------------------------------------------------------
# loads (§7.5)
# ---------------------------------------------------------------------------


def test_loads_go_on_cloth_spars_and_lines():
    ship = minimal_ship()
    set_sails(ship, ["topsail", "mainsail", "jib"], brace_deg=20, sheet_deg=20)
    compute_sail_forces(ship, make_wind(100, 20))
    top, main, jib = ship.sails["topsail"], ship.sails["mainsail"], ship.sails["jib"]
    assert top.force_kn > 0 and main.force_kn > 0 and jib.force_kn > 0
    assert top.load_kn == top.force_kn
    assert ship.spars["topsail.yard"].load_kn == pytest.approx(top.force_kn)
    # the topmast carries the topsail and the jib (hanked to a stay of the topmast)
    assert ship.spars["topmast"].load_kn == pytest.approx(top.force_kn + jib.force_kn)
    # the lower mast carries everything
    assert ship.spars["mast"].load_kn == pytest.approx(top.force_kn + jib.force_kn + main.force_kn)
    assert ship.lines["topsail.sheet.starboard"].load_kn == pytest.approx(0.6 * top.force_kn)
    assert ship.lines["topsail.yard.halyard"].load_kn == pytest.approx(0.5 * top.force_kn)
    assert ship.lines["topsail.yard.brace.larboard"].load_kn == pytest.approx(0.3 * top.force_kn)
    assert ship.lines["mainsail.sheet"].load_kn == pytest.approx(0.6 * main.force_kn)
    assert ship.lines["gaff.peak_halyard"].load_kn == pytest.approx(0.5 * main.force_kn)
    assert ship.lines["gaff.throat_halyard"].load_kn == pytest.approx(0.5 * main.force_kn)
    assert ship.spars["gaff"].load_kn == pytest.approx(main.force_kn)
    assert ship.lines["jib.stay"].load_kn == pytest.approx(jib.force_kn)
    assert ship.lines["jib.halyard"].load_kn == pytest.approx(0.5 * jib.force_kn)
    assert ship.spars["bowsprit"].load_kn == 0.0
    # loads are refreshed, not accumulated, from one call to the next
    compute_sail_forces(ship, make_wind(100, 20))
    assert ship.spars["mast"].load_kn == pytest.approx(top.force_kn + jib.force_kn + main.force_kn)
    set_sails(ship, [])
    compute_sail_forces(ship, make_wind(100, 20))
    assert all(p.load_kn == 0.0 for p in ship.parts.values())


def test_strain_grows_aloft_in_a_gale():
    """Truth 8's setting: the light spars aloft are the ones a gale finds out."""
    ship = load_ship(FRIGATE)
    set_sails(ship, ship.groups["plain sail"], brace_deg=38, sheet_deg=25)
    ship.dyn.u = units.knots_to_ms(6)
    compute_sail_forces(ship, make_wind(90, 15))
    tg = ship.spars["main.topgallant_mast"]
    lower = ship.spars["main.mast"]
    moderate = tg.strain_ratio
    compute_sail_forces(ship, make_wind(90, 30))
    assert lower.load_kn > tg.load_kn  # the lower mast carries everything above it
    assert tg.strain_ratio > lower.strain_ratio  # but is nowhere near as close to its rating
    assert tg.strain_ratio > 2.5 * moderate  # the strain grows faster than the wind


# ---------------------------------------------------------------------------
# trims: luffing angle, gaff sheet on a run, studding sails
# ---------------------------------------------------------------------------


def test_luff_angle_is_exposed_for_the_helm():
    ship = minimal_ship()
    compute_sail_forces(ship, make_wind(90, 10))
    assert "luff_angle" not in ship.extra  # nothing set, nothing to luff
    set_sails(ship, ["jib"], sheet_deg=15)
    compute_sail_forces(ship, make_wind(90, 10))
    jib_luff = math.radians(15) + SAIL_CLASSES["jibheaded"].luff_angle
    assert ship.extra["luff_angle"] == pytest.approx(jib_luff)
    set_sails(ship, ["jib", "topsail"], brace_deg=40, sheet_deg=15)
    compute_sail_forces(ship, make_wind(90, 10))
    yard_luff = math.radians(90 - 40) + SAIL_CLASSES["square"].luff_angle
    # the ship's luff angle is the area-weighted mean of her driving sails' (a
    # schooner sails by her fore-and-aft canvas with the topsail shaking), so it
    # lies between the jib's and the topsail's, nearer the larger sail's
    lo, hi = sorted((jib_luff, yard_luff))
    assert lo < ship.extra["luff_angle"] < hi
    set_sails(ship, [])
    compute_sail_forces(ship, make_wind(90, 10))
    assert "luff_angle" not in ship.extra


def test_gaff_sail_on_a_run_wants_squaring_off():
    """Truth 13: sheet eased to 45° on a run gives less thrust than at 70°."""
    ship = minimal_ship()
    wind = make_wind(180, 15)
    set_sails(ship, ["mainsail"], sheet_deg=45)
    at_45 = compute_sail_forces(ship, wind).thrust_n
    set_sails(ship, ["mainsail"], sheet_deg=70)
    at_70 = compute_sail_forces(ship, wind).thrust_n
    assert 0 < at_45 < at_70


def test_studding_sails_follow_their_yard_and_yaw_the_ship():
    ship = load_ship(SCHOONER)
    wind = make_wind(150, 12)  # broad reach on the starboard quarter
    set_sails(ship, ["fore.topsail"], brace_deg=20)
    plain = compute_sail_forces(ship, wind)
    set_sails(ship, ["fore.topsail", "fore.topmast.studdingsail.larboard"], brace_deg=20)
    with_stuns = compute_sail_forces(ship, wind)
    stun = ship.sails["fore.topmast.studdingsail.larboard"]
    assert stun.thrust_kn > 0
    assert with_stuns.thrust_n > plain.thrust_n
    # a sail boomed out to larboard pulls the bow to starboard
    assert with_stuns.yaw_moment_nm - plain.yaw_moment_nm > 0
    # the stuns'l hangs at its yard's angle: it is pushed the same way as the topsail
    top = ship.sails["fore.topsail"]
    assert math.copysign(1, stun.side_force_kn) == math.copysign(1, top.side_force_kn)
    assert stun.backed is False
    # the boom and the yard it stands on carry the stuns'l
    assert ship.spars["fore.topmast.studdingsail_boom.larboard"].load_kn == pytest.approx(
        stun.force_kn
    )
    assert ship.spars["fore.topsail.yard"].load_kn == pytest.approx(stun.force_kn + top.force_kn)


def test_schooner_points_higher_than_the_frigate():
    """Truth 2 at the force level: at 50° apparent the schooner drives, the frigate cannot."""
    wind = make_wind(50, 15)
    frigate = load_ship(FRIGATE)
    set_sails(frigate, frigate.groups["plain sail"], brace_deg=45, sheet_deg=15)
    schooner = load_ship(SCHOONER)
    fore_and_aft = [s.id for s in schooner.sails.values() if s.is_fore_and_aft]
    set_sails(schooner, fore_and_aft, sheet_deg=15)
    f = compute_sail_forces(frigate, wind)
    s = compute_sail_forces(schooner, wind)
    assert s.thrust_n > 0
    assert s.thrust_n / sum(
        x.area_m2 for x in schooner.sails.values() if x.is_set
    ) > f.thrust_n / sum(x.area_m2 for x in frigate.sails.values() if x.is_set)


def test_deterministic():
    ship = frigate_plain_sail(brace_deg=30, sheet_deg=25, speed_kn=5)
    a = compute_sail_forces(ship, make_wind(80, 15))
    b = compute_sail_forces(ship, make_wind(80, 15))
    assert as_tuple(a) == as_tuple(b)
