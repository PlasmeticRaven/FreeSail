"""Package 90, item 37 (step A0): the generator's copy of the sail-force law held to the engine's.

The rating pass (`tools/gen_ships.py`, `static_kn` and `Builder.rate_spars`) rates every spar by
the static force of its sails at each class's peak coefficient. Package 10 raised the studding
curve's peak to 1.35 (1.44 at its best angle) for truth 14 and left the generator's table at
1.25, so that every studding-sail boom was rated a seventh below the rule (the cold review's
`code-08-core-ship-physics.md` l. 329: no test held the two together). The table is now read
from the engine's curves, rounded to two places; these tests hold it there, with the other
copies of the law the generator keeps (the air's density, the knot, the shear).
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

from freesail import units
from freesail.physics.sails import SAIL_CLASSES
from freesail.physics.wind import Wind

ROOT = Path(__file__).resolve().parents[1]


def _gen():
    spec = importlib.util.spec_from_file_location(
        "gen_ships_for_peaks", ROOT / "tools" / "gen_ships.py"
    )
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    return gen


def _sampled_peak(cls) -> float:
    """The greatest |(C_L, C_D)| the engine gives for the class, every 0.01 degree from 0 to 90."""
    return max(math.hypot(*cls.coefficients(units.deg_to_rad(k / 100.0))) for k in range(0, 9001))


def test_every_class_of_the_engine_has_its_peak_in_the_generators_table_to_two_places():
    gen = _gen()
    assert set(gen.PEAK_COEFF) == set(SAIL_CLASSES)
    for name, cls in SAIL_CLASSES.items():
        peak = _sampled_peak(cls)
        assert gen.PEAK_COEFF[name] == round(peak, 2), (name, gen.PEAK_COEFF[name], peak)
        assert abs(gen.PEAK_COEFF[name] - peak) <= 0.005 + 1e-9, name


def test_the_studding_peak_is_the_engines_1_44_and_the_others_as_they_were():
    """The one figure that moved, and the five that agreed already; the sprit class gains its
    drag alone at 90 degrees (a KeyError at the rating pass before, `map-engine.md` §4)."""
    gen = _gen()
    assert gen.PEAK_COEFF == {
        "square": 1.23,
        "studding": 1.44,
        "gaff": 1.29,
        "jibheaded": 1.32,
        "lug": 1.29,
        "lateen": 1.25,
        "sprit": 1.20,
    }


def test_the_generators_air_knot_and_shear_are_the_engines():
    gen = _gen()
    assert gen.RHO_AIR == units.RHO_AIR
    assert gen.KNOT == units.KNOT
    # `static_kn`'s shear, (h / 10) ** 0.11, is the wind's (`Wind.SHEAR_EXPONENT` at
    # `Wind.REFERENCE_HEIGHT`): one square metre of square sail at 25 m in 20 kn
    v = 20.0 * units.KNOT * (25.0 / Wind.REFERENCE_HEIGHT) ** Wind.SHEAR_EXPONENT
    want = 0.5 * units.RHO_AIR * v * v * gen.PEAK_COEFF["square"] / 1000.0
    assert math.isclose(gen.static_kn([(1.0, 25.0, "square")], 20.0), want, rel_tol=1e-12)
