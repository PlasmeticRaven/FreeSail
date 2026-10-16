"""Known truths 73 to 76 (package 32b): the four reference ships stand in a hierarchy.

The cutter Sherbourne and the brig Harpy beside the frigate and the schooner, measured
as the known truths are (tests/test_known_truths.py: a plain-sail polar in 15 knots and a
pointing sweep up the wind on the starboard tack), so that a change to the physics or to
a ship file shows as a change in the hierarchy. The bands are judgement, provisional:
the period sources give no polars, only the reputation of each rig (a cutter the closest-
winded of them, a brig a ship in little, a schooner between), and the figures measured
when the files were built are in docs/dev/TuningNotes.md, "Where the ships stand".

- 73: a cutter lies as close to the wind as a topsail schooner or closer (the owner's
  wording of 2026-09-30; the first asked for half a point closer, which the shared
  sail-class curves and trim floors cannot give: spec M5 open item 12).
- 74: a brig lies as a ship does, about six points, and less close than the schooner.
- 75: the cutter's beam reach in 15 knots of wind under plain sail is 6 to 8 knots.
- 76: the brig's beam reach is 7 to 9 knots, within a knot of the frigate's, and, as the
  frigate's, her fastest point of sailing.

Package 43b extends them to six vessels (spec M6 §19): the lugger Éclair (the chasse-marée
by Forfait's Table VII, dipping lugs) and the smack Culloden (cutter-rigged by Steel's
proportions, with a well). Their crews are small (thirty and eight), so their polars are
taken with all hands called before the sail is set, as a small craft makes sail; the
sweeps are the frigate's form. The figures and the bands' reasons are in
docs/dev/TuningNotes.md, package 43b.

- 73 extended: a lugger lies as close to the wind as the cutter or closer ("Luggers sail
  well close hauled, and very near the wind", Steel 1794 vol. I, LUGGER); the smack, on
  the cutter's rules, lies as the cutter does within a degree.
- 75 extended: the lugger's beam reach in 15 knots is 7 to 9.5 knots, faster than the
  cutter's ("construits pour la marche", Lescallier 1791 p. 408); the smack's is 5 to 7,
  slower than the cutter's on her forty feet of water-line.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.test_known_truths import (
    FRIGATE,
    POLAR_ANGLES,
    SCHOONER,
    argmax_speed,
    best_sustained_course,
    make,
    pointing_sweep,
    polar,
    reading,
    settle,
    tack_for,
)


def polar_all_hands(ship, angles=POLAR_ANGLES) -> dict[int, dict]:
    """The plain-sail polar in fifteen knots with all hands called first (package 43b):
    the smack's eight men, the watch alone, took eleven minutes to set her three sails and
    she lost her way and fell off before she had them."""
    out = {}
    for twa in angles:
        world = make(ship, float(twa))
        settle(
            world,
            ["call all hands", "set plain sail", f"brace sharp up on the {tack_for(twa)} tack"],
        )
        out[twa] = reading(world)
    return out


ROOT = Path(__file__).resolve().parents[1]
CUTTER = str(ROOT / "data" / "ships" / "cutter.yaml")
BRIG = str(ROOT / "data" / "ships" / "brig.yaml")
LUGGER = str(ROOT / "data" / "ships" / "lugger.yaml")
SMACK = str(ROOT / "data" / "ships" / "smack.yaml")

HALF_A_POINT = 5.625


@pytest.fixture(scope="module")
def cutter_sweep():
    return pointing_sweep(CUTTER)


@pytest.fixture(scope="module")
def brig_sweep():
    return pointing_sweep(BRIG)


@pytest.fixture(scope="module")
def schooner_sweep():
    return pointing_sweep(SCHOONER)


@pytest.fixture(scope="module")
def frigate_sweep():
    return pointing_sweep(FRIGATE)


@pytest.fixture(scope="module")
def cutter_polar():
    return polar(CUTTER)


@pytest.fixture(scope="module")
def brig_polar():
    return polar(BRIG)


@pytest.fixture(scope="module")
def frigate_polar():
    return polar(FRIGATE)


def test_truth_73_the_cutter_lies_as_close_as_the_schooner_or_closer(cutter_sweep, schooner_sweep):
    """Truth 73 as the owner amended it (2026-09-30): a cutter points much as a schooner
    does, so she lies as close or closer, and holds three knots inside five points, where
    the frigate cannot. The first wording asked for half a point closer and failed: how
    close a ship lies is set by the sail-class curves and trim floors the four ships share,
    not by the file (58.004 deg each when built); pointing from the file's own geometry is
    spec M5 open item 12's."""
    best_c, closest_c = best_sustained_course(cutter_sweep)
    best_s, _ = best_sustained_course(schooner_sweep)
    assert 50.0 <= best_c <= 62.0, f"cutter's best course {best_c} deg off"
    assert best_c <= best_s + 1.0  # the same to the degree (58.004 and 58.004 when built)
    assert closest_c < 54.0


def test_truth_74_a_brig_lies_as_a_ship_does(brig_sweep, frigate_sweep, schooner_sweep):
    best_b, closest_b = best_sustained_course(brig_sweep)
    best_f, _ = best_sustained_course(frigate_sweep)
    best_s, _ = best_sustained_course(schooner_sweep)
    assert 60.0 <= best_b <= 72.0, f"brig's best course {best_b} deg off"
    assert abs(best_b - best_f) <= HALF_A_POINT  # a ship in little
    assert best_b > best_s  # and less close-winded than the schooner
    assert closest_b >= 50.0


def test_truth_75_the_cutters_beam_reach(cutter_polar, frigate_polar):
    speed = cutter_polar[90]["speed"]
    assert 6.0 <= speed <= 8.0, f"cutter's beam reach {speed:.1f} kn"
    assert speed < frigate_polar[90]["speed"]  # fifteen metres of waterline, not forty
    # she is stiff for her size: under ten degrees of heel in fifteen knots
    assert cutter_polar[90]["heel"] < 10.0


def test_truth_76_the_brigs_beam_reach(brig_polar, frigate_polar):
    speed = brig_polar[90]["speed"]
    assert 7.0 <= speed <= 9.0, f"brig's beam reach {speed:.1f} kn"
    assert abs(speed - frigate_polar[90]["speed"]) <= 1.0
    fastest = argmax_speed(brig_polar)
    assert 75 <= fastest <= 105, f"fastest at {fastest} deg off the true wind"


def test_the_four_ships_stand_in_order_on_a_beam_reach(cutter_polar, brig_polar, frigate_polar):
    """The hull speeds order them: the cutter (9.5 kn) below the brig (11.5) and the
    frigate; every one under her hull speed with the wind abeam in fifteen knots."""
    assert cutter_polar[90]["speed"] < brig_polar[90]["speed"] < 9.5
    assert brig_polar[90]["speed"] <= frigate_polar[90]["speed"] + 0.5


# ---------------------------------------------------------------------------
# Package 43b: the lugger and the smack, six vessels
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def lugger_sweep():
    return pointing_sweep(LUGGER)


@pytest.fixture(scope="module")
def smack_sweep():
    return pointing_sweep(SMACK)


@pytest.fixture(scope="module")
def lugger_polar():
    return polar_all_hands(LUGGER)


@pytest.fixture(scope="module")
def smack_polar():
    return polar_all_hands(SMACK)


def test_truth_73_extended_the_lugger_lies_closer_than_the_cutter(lugger_sweep, cutter_sweep):
    """The lug is the weatherly sail of the period (Steel 1794, LUGGER: "Luggers sail well
    close hauled, and very near the wind"; Forfait 1788 p. 53): she lies as close as the
    cutter or closer (52 degrees against 58 when built), and holds way inside five points."""
    best_l, closest_l = best_sustained_course(lugger_sweep)
    best_c, _ = best_sustained_course(cutter_sweep)
    assert 46.0 <= best_l <= 60.0, f"lugger's best course {best_l} deg off"
    assert best_l <= best_c
    assert closest_l < 50.0


def test_truth_73_extended_the_smack_lies_as_the_cutter(smack_sweep, cutter_sweep):
    """Cutter-rigged on the cutter's rules (Lescallier 1791 p. 420: "le Gréement est
    semblable à celui des Sloops"), she lies as the cutter does (58 and 58 when built)."""
    best_s, closest_s = best_sustained_course(smack_sweep)
    best_c, _ = best_sustained_course(cutter_sweep)
    assert abs(best_s - best_c) <= 2.0, f"smack {best_s}, cutter {best_c}"
    assert closest_s < 54.0


def test_truth_75_extended_the_luggers_beam_reach(lugger_polar, cutter_polar):
    """Built for speed ("pour la marche", Lescallier 1791 p. 408) on 55 ft of water-line:
    7 to 9.5 knots on a beam reach in fifteen, faster than the cutter (8.2 when built),
    under her hull speed, and stiff for the sail she carries (Forfait p. 53)."""
    speed = lugger_polar[90]["speed"]
    assert 7.0 <= speed <= 9.5, f"lugger's beam reach {speed:.1f} kn"
    assert speed > cutter_polar[90]["speed"]
    assert lugger_polar[90]["heel"] < 15.0


def test_truth_75_extended_the_smacks_beam_reach(smack_polar, cutter_polar):
    """Forty feet of water-line: 5 to 7 knots on a beam reach in fifteen (6.2 when built),
    slower than the cutter, and stiff."""
    speed = smack_polar[90]["speed"]
    assert 5.0 <= speed <= 7.0, f"smack's beam reach {speed:.1f} kn"
    assert speed < cutter_polar[90]["speed"]
    assert smack_polar[90]["heel"] < 10.0


def test_the_six_vessels_stand_in_order_on_a_beam_reach(
    smack_polar, cutter_polar, lugger_polar, brig_polar, frigate_polar
):
    """By their length on the water and their canvas: the smack below the cutter below the
    lugger; the brig and the frigate within a knot and a half of the lugger, the larger
    hulls not slower by more."""
    smack, cutter = smack_polar[90]["speed"], cutter_polar[90]["speed"]
    lugger, brig = lugger_polar[90]["speed"], brig_polar[90]["speed"]
    assert smack < cutter < lugger
    assert abs(brig - lugger) <= 1.5
    assert frigate_polar[90]["speed"] >= lugger - 1.5
