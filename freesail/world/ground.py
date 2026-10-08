"""Grounding (spec M5 §18; package 34): touching is an event with speed, heel, tide and
bottom, and its consequences are the hull's and the log's.

Each tick the World asks whether the keel touches: the chart's cells against her draught,
heel and the tide's height (`chart.Chart.aground`, package 32's test, which the tide now
enters), and the charted dangers by name (`chart.Chart.danger_under`: the Manacles are a
dozen fathoms deep in the tiles and a mile of ledges in the pilot). When she strikes:

- **a stop**: the ground holds her (`ship.extra["aground"]`, which `physics/integrate.py`
  reads: no way through the water but the stream's past her, no swing) until the tide
  floats her off;
- **the masts**: the shock of her way checked carries the topmasts away as a squall does
  (Luce 1884, ch. XXXVI, 'Getting on Shore': "When a vessel strikes, the first step is to
  brace aback ... send down the upper yards and top-gallant masts"): the strain model's
  rule on a blow proportional to the square of her speed (`strain.shock_spars`,
  `SHOCK_SPEED_KN`: judgement, at six knots the topmasts go);
- **a leak**, by the bottom's kind and her speed: on rock her planks are stove and the
  well rises fast, on sand or mud it is a trickle (judgement in the rates; the pumps are
  milestone 8's with the well's reading, so the carpenter reports each foot and at two
  metres she is waterlogged and nothing more is modelled, which the tuning notes say);
- **the log**: the urgent line with her speed, heel, the tide rising or falling and the
  ground, then the master's word on when she should float, which is *his* tide (the
  epitome's next high water, `tide.Epitome`), never the world's; and the world's own line
  when she floats ("She is off, and afloat again").

Getting off is the tide's business, or the anchor's: a kedge laid out by the boat is
package 35's (the boat); what the hands can do here is lighten nothing and wait for the
flood, as Luce's first case has it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.physics import strain

__all__ = [
    "LEAK_ROCK_M_PER_H",
    "LEAK_SOFT_M_PER_H",
    "LEAK_REFERENCE_KN",
    "SHOCK_SPEED_KN",
    "WATERLOGGED_M",
    "Ground",
    "Grounded",
]

# The speed at which the blow of striking carries the topmasts away: judgement (a ship
# striking a rock at six knots is brought up all standing; Luce 1884 ch. XXXVI sends the
# upper masts down after a strike for what the shock has done to them).
SHOCK_SPEED_KN = 6.0
# The leak: metres of water in the well an hour at `LEAK_REFERENCE_KN`, growing with the
# square of the speed; on rock, and on sand or mud (judgement: a rock stoves her planks, a
# bank she sits on).
LEAK_ROCK_M_PER_H = 0.6
LEAK_SOFT_M_PER_H = 0.05
LEAK_REFERENCE_KN = 4.0
# Past this in the well she is waterlogged and nothing more is modelled (the pumps and
# the well's reading are milestone 8's).
WATERLOGGED_M = 2.0
FOOT_M = 0.3048

# The dangers about her are read from the chart's index once a minute and tested every
# tick (the tiles' test is every tick as it was).
DANGERS_REFRESH_S = 60
# She is said to be off only with this much water under her keel beyond her draught
# (judgement: a foot; without it a ship on the edge of a bank floats and strikes again
# every minute as the tide makes, which the log would say each time).
AFLOAT_MARGIN_M = 0.3


@dataclass
class Grounded:
    """The strike, for the log and the state."""

    tick: int
    speed_kn: float
    heel_deg: float
    tide_m: float
    rising: bool
    bottom: str
    where: str
    depth_m: float
    rock: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "speed_kn": round(self.speed_kn, 1),
            "heel_deg": round(self.heel_deg, 1),
            "tide_m": round(self.tide_m, 2),
            "rising": self.rising,
            "bottom": self.bottom,
            "where": self.where,
            "depth_m": round(self.depth_m, 2),
            "rock": self.rock,
        }


class Ground:
    """The World's grounding check and its consequences."""

    def __init__(self, world: Any):
        self.world = world
        self.grounded: Grounded | None = None
        self._dangers: list[Any] = []
        self._dangers_tick = -DANGERS_REFRESH_S
        self._feet_said = 0
        self._waterlogged_said = False

    @property
    def aground(self) -> bool:
        return self.grounded is not None

    def tick(self) -> None:
        world = self.world
        pos = world.position
        chart = world.chart
        if pos is None or chart is None:
            return
        ship = world.ship
        tide_m = world.tide_height_m
        length, draught = _length(ship), _draught(ship)
        if world.clock.tick - self._dangers_tick >= DANGERS_REFRESH_S:
            self._dangers = chart.dangers_about(pos, length)
            self._dangers_tick = world.clock.tick
        touched = chart.aground(pos, ship.heading, length, draught, _heel(ship), tide_m=tide_m)
        rock = False
        if touched is None and self._dangers:
            touched = chart.danger_under(
                pos, ship.heading, length, draught, tide_m, dangers=self._dangers
            )
            rock = touched is not None
        if touched is None and self.grounded is not None:
            # off only with a foot under her: the test again at the deeper draught
            touched = chart.aground(
                pos, ship.heading, length, draught + AFLOAT_MARGIN_M, _heel(ship), tide_m=tide_m
            )
            if touched is None and self._dangers:
                touched = chart.danger_under(
                    pos,
                    ship.heading,
                    length,
                    draught + AFLOAT_MARGIN_M,
                    tide_m,
                    dangers=self._dangers,
                )
        if touched is not None and self.grounded is None:
            self._strike(touched, rock)
        elif touched is None and self.grounded is not None:
            self._afloat()
        if self.grounded is not None:
            self._leak()

    # -- the strike -----------------------------------------------------------------------

    def _strike(self, touched: Any, rock: bool) -> None:
        world = self.world
        ship = world.ship
        state = world.tide_state
        speed_kn = units.ms_to_knots(_speed(ship))
        heel_deg = abs(math.degrees(_heel(ship)))
        tide_m = world.tide_height_m
        rising = bool(state.rising) if state is not None else False
        bottom = touched.bottom or ""
        rock = rock or "rock" in bottom.lower()
        self.grounded = Grounded(
            world.clock.tick,
            speed_kn,
            heel_deg,
            tide_m,
            rising,
            bottom,
            touched.where,
            touched.depth_m,
            rock,
        )
        extra = getattr(ship, "extra", None)
        if extra is not None:
            extra["aground"] = self.grounded.to_dict()
            if "hove_to" in extra:
                # a ship that has taken the ground is hove to no longer (package 37f)
                from freesail.evolutions.scripts import end_lying_to

                end_lying_to(ship)
            # the way through the water is checked at once; the ground holds her
            dyn = getattr(ship, "dyn", None)
            if dyn is not None:
                dyn.u = dyn.v = dyn.r = 0.0
                dyn.speed = 0.0
        tide_words = "the tide rising" if rising else "the tide falling"
        if state is not None and state.slack:
            tide_words = "at the turn of the tide"
        words = touched.words.rstrip(".")
        head = (
            f"{words}; she struck at {_knots_words(speed_kn)}, "
            f"heeling {heel_deg:.0f} degrees, {tide_words}."
        )
        world.record(
            Severity.URGENT,
            "ship.aground",
            head,
            data=touched.to_dict() | self.grounded.to_dict(),
        )
        # the masts: the blow of her way checked (strain.shock_spars)
        ratio = (speed_kn / SHOCK_SPEED_KN) ** 2
        if extra is not None and hasattr(ship, "spars"):
            strain.shock_spars(ship, ratio)
        # the leak by the bottom's kind and the speed
        rate = LEAK_ROCK_M_PER_H if rock else LEAK_SOFT_M_PER_H
        rate *= (speed_kn / LEAK_REFERENCE_KN) ** 2
        if extra is not None:
            extra["leak_m_per_h"] = rate
        if rate > 0.02:
            how = "stove on the rock" if rock else "strained on the ground"
            world.record(
                Severity.NOTABLE,
                "ship.leak",
                f"The carpenter reports her {how} and making water.",
                data={"leak_m_per_h": round(rate, 3), "rock": rock},
            )
        # the master's word: when she should float, by his tide (never the world's)
        self._masters_word(rising)

    def _masters_word(self, rising: bool) -> None:
        world = self.world
        nav = getattr(world, "navigation", None)
        if nav is None or getattr(nav, "epitome", None) is None:
            return
        if rising:
            text = "She took the ground on the flood; the master thinks she will float as it makes."
            world.record(Severity.NOTABLE, "ground.master", text, data={"rising": True})
            return
        said = nav.tide_by_almanac()
        text = (
            "She took the ground on the ebb: she will not float before the flood, and the "
            f"master makes it {said['next_words']} by the epitome."
        )
        world.record(Severity.NOTABLE, "ground.master", text, data={"rising": False} | said)

    # -- the leak and floating off ---------------------------------------------------------

    def _leak(self) -> None:
        world = self.world
        ship = world.ship
        extra = getattr(ship, "extra", None)
        hull = getattr(ship, "hull", None)
        if extra is None or hull is None:
            return
        rate = float(extra.get("leak_m_per_h", 0.0))
        if rate <= 0.0:
            return
        hull.water_in_well_m = min(WATERLOGGED_M, hull.water_in_well_m + rate / 3600.0)
        feet = int(hull.water_in_well_m / FOOT_M)
        if feet > self._feet_said:
            self._feet_said = feet
            n = "a foot" if feet == 1 else f"{feet} feet"
            world.record(
                Severity.NOTABLE,
                "well.rising",
                f"The carpenter reports {n} of water in the well, and gaining.",
                data={"well_m": round(hull.water_in_well_m, 2), "feet": feet},
            )
        if hull.water_in_well_m >= WATERLOGGED_M and not self._waterlogged_said:
            self._waterlogged_said = True
            world.record(
                Severity.URGENT,
                "ship.waterlogged",
                "She is waterlogged; the water has beaten the carpenter's crew.",
                data={"well_m": round(hull.water_in_well_m, 2)},
            )

    def _afloat(self) -> None:
        world = self.world
        state = world.tide_state
        self.grounded = None
        extra = getattr(world.ship, "extra", None)
        if extra is not None:
            extra.pop("aground", None)
        how = " on the flood" if state is not None and state.rising else ""
        world.record(Severity.NOTABLE, "ship.afloat", f"She is off, and afloat again{how}.")


def _length(ship: Any) -> float:
    hull = getattr(ship, "hull", None)
    return float(hull.spec.length_waterline_m) if hull is not None else 0.0


def _draught(ship: Any) -> float:
    hull = getattr(ship, "hull", None)
    return float(hull.spec.draught_m) if hull is not None else 0.0


def _heel(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    return float(dyn.heel) if dyn is not None else 0.0


def _speed(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    return float(dyn.speed) if dyn is not None else float(getattr(ship, "speed", 0.0))


def _knots_words(kn: float) -> str:
    from freesail.world.reckoning import knots_words

    return knots_words(round(kn * 2.0) / 2.0) if kn >= 0.25 else "no way"
