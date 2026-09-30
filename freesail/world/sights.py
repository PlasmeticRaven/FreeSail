"""The noon sight (spec M5 §14's first sentence; N §1, §3; package 33a): the latitude by
the sun's meridian altitude, taken at the sun's noon if the sky allows and refused in
cloud, with the instrument's error and the horizon's.

The sun model (`freesail.core.sun`) has the declination and the moment of the meridian
passage; the master's arithmetic (the altitude corrected for dip, refraction and the
semi-diameter, the declination from the Almanac, Falconer 1780, 'Quadrant') is his, and
the game models its outcome: the true latitude plus an error drawn from the seed. The
sextant reads to a minute, the octant to two or three (N §3, from Falconer's 'Quadrant'
and the Oxford History of Science Museum's note that the octant stayed the cheap
everyday instrument for latitude); the horizon in haze or swell two to five minutes; "call
it 2 to 5 miles with a good horizon, none in cloud" (N §3). The scenario says which
instrument the ship carries (`Scenario.instrument`: the frigate a sextant, the schooner
an octant); the sea's motion of 5a widens the horizon's error, the hook package 31 left
inert now read. Double altitudes when noon is clouded are not built (spec §32).

The chronometer's time sight and the lunar are package 33b's.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any

from freesail.world.geo import Position, format_position

__all__ = [
    "HAZE_HORIZON_NM",
    "HORIZON_SEA_NM_PER_M",
    "HORIZON_SIGMA_NM",
    "INSTRUMENTS",
    "OCTANT_SIGMA_NM",
    "SEXTANT_SIGMA_NM",
    "SIGHT_ON_DECK_MINUTES",
    "SKY_HIDES_THE_SUN",
    "WEATHER_HIDES_THE_SUN",
    "NoonResult",
    "Sight",
    "instrument_sigma_nm",
    "noon_sight",
    "sky_allows",
]

# The instrument's error, one sigma, in minutes of altitude which are miles of latitude:
# "sextant to a minute, octant to two or three" (N §3).
SEXTANT_SIGMA_NM = 1.0
OCTANT_SIGMA_NM = 2.5
INSTRUMENTS: tuple[str, ...] = ("sextant", "octant")
# The horizon's error with a good horizon, one sigma (judgement: N §3's "2 to 5 miles
# with a good horizon" taken as the whole error with a sextant, so the horizon's part is
# what makes two miles with the sextant's one); a hazy sky adds a mile (judgement); and
# the sea's motion widens it by half a mile for every metre of sea (judgement: N §3's
# "the horizon in haze or swell two to five minutes", the five with an octant in a
# three-metre sea).
HORIZON_SIGMA_NM = 1.7
HAZE_HORIZON_NM = 1.0
HORIZON_SEA_NM_PER_M = 0.5
# The master is on deck with his instrument for the last quarter of an hour before the
# sun's noon, watching the altitude rise to its greatest (judgement: the practice of
# "waiting for the sun to dip"); the day's work follows below (`reckoning.DAYS_WORK_MINUTES`).
SIGHT_ON_DECK_MINUTES = 15
# The sky that hides the sun at noon (Beaufort's words as the readings give them, spec M5
# §5): overcast, dark and gloomy, threatening and thick hide it; hazy lets it through with
# a worse horizon; and rain, drizzle, fog and thunder hide it whatever the sky says.
SKY_HIDES_THE_SUN = frozenset({"overcast", "dark and gloomy", "threatening", "thick"})
WEATHER_HIDES_THE_SUN = frozenset({"rain", "drizzle", "fog", "thunder"})
# The master's skill scales the instrument's error: a skilled master (0.9) reads his
# instrument at three fifths of its error, a poor one (0.5) at the whole (judgement).
SKILL_REFERENCE = 0.5


def instrument_sigma_nm(instrument: str) -> float:
    if instrument == "sextant":
        return SEXTANT_SIGMA_NM
    if instrument == "octant":
        return OCTANT_SIGMA_NM
    raise ValueError(f"no such instrument as {instrument!r}; say sextant or octant")


def sky_allows(conditions: Any) -> tuple[bool, str]:
    """Whether the sun can be observed under these conditions (None: no weather is kept,
    and the sun of the plane always shows), and the refusal's words when not."""
    if conditions is None:
        return True, ""
    if conditions.weather in WEATHER_HIDES_THE_SUN:
        return False, f"the sun was hid at noon in {conditions.weather}"
    if conditions.sky in SKY_HIDES_THE_SUN:
        return False, "the sun was hid at noon"
    return True, ""


@dataclass(frozen=True)
class Sight:
    """A noon latitude as the master reports it: the latitude, the instrument, and the
    doubt he puts on it (one sigma, miles)."""

    latitude_deg: float
    instrument: str
    sigma_nm: float
    tick: int

    @property
    def words(self) -> str:
        return format_position(Position(self.latitude_deg, 0.0)).split(",")[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude_deg": round(self.latitude_deg, 5),
            "instrument": self.instrument,
            "sigma_nm": round(self.sigma_nm, 2),
            "tick": self.tick,
        }


@dataclass(frozen=True)
class NoonResult:
    sight: Sight | None
    refusal: str  # "" when the sight was had


def noon_sight(world: Any, master: Any, stream: random.Random) -> NoonResult:
    """The sight at the sun's noon: the true latitude plus the seeded error of the
    instrument, the master's skill, the horizon and the sea; or the refusal."""
    conditions = getattr(world, "conditions", None)
    allowed, why = sky_allows(conditions)
    if not allowed:
        return NoonResult(None, why)
    pos = world.position
    if pos is None:
        return NoonResult(None, "no sea to take a sight on")
    instrument = str(getattr(world.scenario, "instrument", "octant") or "octant")
    skill = float(getattr(master, "skill", 0.7))
    factor = max(0.5, 1.0 - (skill - SKILL_REFERENCE))
    s_instrument = instrument_sigma_nm(instrument) * factor
    s_horizon = HORIZON_SIGMA_NM
    if conditions is not None and conditions.sky == "hazy":
        s_horizon += HAZE_HORIZON_NM
    sea = getattr(world, "sea", None)
    if sea is not None:
        s_horizon += HORIZON_SEA_NM_PER_M * float(sea.reading().height_m)
    sigma = math.hypot(s_instrument, s_horizon)
    error_nm = stream.gauss(0.0, sigma)
    lat = pos.lat_deg + error_nm / 60.0
    return NoonResult(Sight(lat, instrument, sigma, world.clock.tick), "")
