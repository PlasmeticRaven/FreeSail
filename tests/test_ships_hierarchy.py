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
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.test_known_truths import (
    FRIGATE,
    SCHOONER,
    argmax_speed,
    best_sustained_course,
    pointing_sweep,
    polar,
)

ROOT = Path(__file__).resolve().parents[1]
CUTTER = str(ROOT / "data" / "ships" / "cutter.yaml")
BRIG = str(ROOT / "data" / "ships" / "brig.yaml")

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
