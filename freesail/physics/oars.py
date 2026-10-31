"""The oar force on a hull (package 82, item 4; docs/design/Design-BoatAndPersonAboard.md
§5.2).

The oars are a thrust along the hull's axis, added to the sails' in the integrator's substep
(`integrate._substep`, beside the cable's pull and the trawl's drag, the two outside forces it
has), read from `ship.extra["oars"]`, an `Oars` state the boat's orders set: the hands at the
oars (`manned`, up to the file's number), whether the oars are out, the stroke (`give way` the
full stroke, `easy all` half, `lie on your oars` none) and the men's fatigue, the hours pulled
since fresh. The thrust of one oar is

    F_oar(u) = min(F_0, P / max(u, u_min)) x stroke x f(hours)

with `F_0` the pull a man sustains on the blade at no way (the file's `thrust_n`), `P` the
power a man delivers to the water at the oar over hours (`power_w`), `u` the boat's way
through the water, `u_min` a floor so the thrust is finite at rest (the stroke's own speed at
the catch; judgement) and `f(hours)` the men's tiring, 1 fresh and 1 / (1 + hours / T) after
hours at the oars, T the file's `tiring_h` (half strength at T hours, two thirds at T / 2, a
third at 2 T: the period's practice of towing watch and watch, "the boat's crew tiring by
the hour"; judgement).

The source of the model's form: the oar as a lever of the second class that strikes the
water, its fulcrum the thole on the gunwale (Falconer 1780, OAR), the thrust the water's
reaction to the blade; a man's sustained output bounded in force at low way and in power at
speed is the ordinary model of a rower and is the design's, not the period's, which gives no
figure for a man's power at an oar (Falconer, OAR; Steel 1805 p. 181 on the boats' purposes).
The figures (F_0 50 N, P 60 W an oar) are fitted to the behaviours the brief and the sources
give (three to four knots light under four oars, a knot and a half towing, the men tiring by
the hour) and written in each boat's file as judgement. Nothing else of the physics changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__all__ = ["EASY", "FULL", "LYING_ON", "U_MIN_MS", "Oars", "oar_thrust", "oars_of", "stroke_words"]

# The stroke as a fraction of the full stroke: `give way`, `easy all`, `lie on your oars`.
FULL = 1.0
EASY = 0.5
LYING_ON = 0.0
# The floor on the way the power is divided by, so that the thrust at rest is finite: the
# stroke's own speed through the water at the catch (judgement), 0.3 m/s.
U_MIN_MS = 0.3


@dataclass
class Oars:
    """The oars' state on a boat's hull (`ship.extra["oars"]`), set by her orders and read by
    the integrator; saved in the checkpoint with the ship, as the ground tackle is."""

    number: int  # the file's oars
    thrust_n: float  # F_0, a man's pull on the blade at no way
    power_w: float  # P, a man's power at the oar over hours
    tiring_h: float  # T, the hours at the oars that halve his strength
    manned: int = 0  # the hands at the oars now (0: the oars in, or nobody at them)
    out: bool = False  # the oars out (shipped in the rowlocks) or boated
    stroke: float = LYING_ON  # the stroke pulled: FULL, EASY or LYING_ON
    hours: float = 0.0  # the hours pulled since the men were fresh
    pulling_for: dict[str, Any] = field(default_factory=dict)  # the coxswain's mark (`pull for`)

    @property
    def pulling(self) -> bool:
        return self.out and self.manned > 0 and self.stroke > 0.0

    def fatigue(self) -> float:
        """f(hours): 1 fresh, 1 / (1 + hours / T) after `hours` at the oars."""
        return 1.0 / (1.0 + max(0.0, self.hours) / self.tiring_h) if self.tiring_h > 0 else 1.0

    def tick(self, dt_s: float) -> None:
        """The men tire while they pull (the hours at the oars grow by the stroke's share
        of the time) and rest when they lie on their oars or the oars are in (the hours
        fall back at half the rate they grew, judgement: a spell at rest recovers them
        slowly)."""
        if self.pulling:
            self.hours += dt_s / 3600.0 * self.stroke
        elif self.hours > 0.0:
            self.hours = max(0.0, self.hours - dt_s / 3600.0 * 0.5)

    def words(self) -> str:
        if not self.out:
            return "the oars in"
        if self.manned <= 0:
            return "the oars out and nobody at them"
        how = stroke_words(self.stroke)
        tired = ""
        if self.hours >= 0.5:
            tired = f", the men {self.hours:.1f} hours at the oars"
        return f"{self.manned} oars out, {how}{tired}"


def stroke_words(stroke: float) -> str:
    if stroke >= FULL:
        return "giving way together"
    if stroke > LYING_ON:
        return "pulling easy"
    return "lying on their oars"


def oars_of(ship: Any) -> Oars | None:
    """The boat's oars, kept in `ship.extra["oars"]`: made on first use from the ship file's
    `oars:` section, as the ground tackle is made from its own; None for a ship whose file
    has none (every ship's but a boat's; the oars' orders are then refused in words). A
    function of the file and the orders given, so a replay rebuilds it."""
    extra = getattr(ship, "extra", None)
    if not isinstance(extra, dict):
        return None
    oars = extra.get("oars")
    if isinstance(oars, Oars):
        return oars
    spec = getattr(getattr(ship, "spec", None), "oars", None)
    if spec is None:
        return None
    oars = Oars(
        number=int(spec.number),
        thrust_n=float(spec.thrust_n),
        power_w=float(spec.power_w),
        tiring_h=float(spec.tiring_h),
    )
    extra["oars"] = oars
    return oars


def oar_thrust(oars: Oars | None, u: float) -> float:
    """The oars' thrust along the hull's axis at a way of `u` m/s through the water, newtons;
    nought with no oars, the oars in, nobody at them or the men lying on them."""
    if oars is None or not oars.pulling:
        return 0.0
    per_oar = min(oars.thrust_n, oars.power_w / max(abs(u), U_MIN_MS))
    return per_oar * oars.manned * oars.stroke * oars.fatigue()
