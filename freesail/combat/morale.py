"""Morale, the one new quantity, and the strike by rule (spec M7 §10; decision 7;
package 70).

**The ship's one figure, not each division's** (§34's open question, decided here): the
colours are one decision of the captain's for the whole company, and a division's temper
has nothing to act on until 73's fight on deck (a gun's crew that will not stand to its
gun is 73's and 77's); one figure keeps the rule legible in the log, which is where the
owner reads it.

The company's readiness to fight on, 0 to 1, read once a minute while she is under fire
or engaging: the captain's doctrine gives where it starts (`morale_start`: a King's ship's
company high, a merchant crew's low, the nation's habit in the doctrine's figure) and
where the colours come down (`strike_below`); the losses (the killed and wounded as a
share of her complement, the heaviest weight), the guns dismounted, the masts gone, and
the odds (the enemy's weight of broadside against her own, while his shot strikes) each
take from it; nothing restores it in an action (a company that has stood an hour under
fire is not fresher for it). A King's ship's doctrine sets `strike_below` low enough that
she fights to a wreck, which is the period's record; a merchantman's high enough that a
privateer's first broadside into her brings her colours down, which is also the record.

**Striking by rule**: when the figure falls under the doctrine's line while she is under
fire (fired on within `UNDER_FIRE_S`) and a shot has told (a company does not haul down to
shot that missed, whatever the odds), the colours are struck, said in the log with the
reasons in figures; the battery holds, the state `struck` is written for the captain's
machine (he lies to) and the colours as a state the lookout reads (71's hook). The
player's own `strike the colours` is never refused: the same state, its consequence told.
What follows (the prize crew, the prisoners) is 74's: this package ends at the colours
down and the firing ceased.

Every weight is a judgement, named in the tuning notes, tuned in play (rule 6).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from freesail.crew.model import number_words

__all__ = [
    "GUNS_WEIGHT",
    "LOSSES_WEIGHT",
    "MASTS_WEIGHT",
    "ODDS_WEIGHT",
    "UNDER_FIRE_S",
    "Morale",
    "morale_of",
]

# The weights (judgement): a fifth of the company hurt takes two fifths of the figure, which
# with a merchant's start of a half brings her to the line at once; the guns dismounted
# their share of a quarter; a lower mast gone three tenths; the odds up to a quarter while
# his shot strikes, by the log of his broadside weight over hers (twice her weight a
# twelfth... four times a sixth, eight times a quarter).
LOSSES_WEIGHT = 2.0
GUNS_WEIGHT = 0.25
MASTS_WEIGHT = 0.3
ODDS_WEIGHT = 0.08
ODDS_MOST = 0.25
# Under fire: struck by a shot within this long (ten minutes; judgement).
UNDER_FIRE_S = 600
# The defaults where a doctrine gives none (a ship without a captain's file).
DEFAULT_START = 0.7
DEFAULT_STRIKE_BELOW = 0.3


@dataclass
class Morale:
    """The company's figure and what made it, kept in `ship.extra["morale"]`."""

    start: float = DEFAULT_START
    strike_below: float = DEFAULT_STRIKE_BELOW
    value: float = DEFAULT_START
    losses: float = 0.0
    guns_lost: float = 0.0
    masts_lost: float = 0.0
    odds: float = 0.0
    reasons: str = ""

    def judge(
        self,
        ship: Any,
        complement: int,
        enemy_weight_lb: float,
        under_fire: bool,
    ) -> float:
        """The figure now, from the ship's state."""
        import math

        crew = ship.extra.get("crew")
        # the losses (package 73): the killed, the wounded and the hurt at light duty, and
        # the dead buried and struck from the books; the sick list is not the action's
        hurt = (
            sum(1 for s in crew.sailors if s.hurt in ("killed", "wounded", "hurt"))
            + len(getattr(crew, "dead", []) or [])
            if crew is not None
            else 0
        )
        self.losses = hurt / max(complement, 1)
        guns = list(getattr(ship, "guns", {}).values())
        self.guns_lost = sum(1 for g in guns if g.dismounted) / len(guns) if guns else 0.0
        lower = [s for s in ship.spars.values() if s.cls in ("mast", "bowsprit")]
        self.masts_lost = sum(1 for s in lower if s.wrecked) / len(lower) if lower else 0.0
        own = sum(g.pounder for g in guns if g.side == "starboard" or g.place != "broadside")
        if under_fire and enemy_weight_lb > 0.0 and own >= 0.0:
            ratio = enemy_weight_lb / max(own, 1.0)
            self.odds = min(ODDS_MOST, ODDS_WEIGHT * max(0.0, math.log2(max(ratio, 1.0))))
        else:
            self.odds = 0.0
        value = (
            self.start
            - LOSSES_WEIGHT * self.losses
            - GUNS_WEIGHT * self.guns_lost
            - MASTS_WEIGHT * self.masts_lost
            - self.odds
        )
        self.value = max(0.0, min(1.0, value))
        self.reasons = self._reasons(hurt, complement, guns, lower, enemy_weight_lb, own)
        return self.value

    def _reasons(self, hurt, complement, guns, lower, enemy_lb, own_lb) -> str:
        parts = [f"{number_words(hurt)} of {complement} hurt"]
        lost = sum(1 for g in guns if g.dismounted)
        if lost:
            parts.append(f"{number_words(lost)} gun{'s' if lost != 1 else ''} dismounted")
        gone = sum(1 for s in lower if s.wrecked)
        if gone:
            parts.append(f"{number_words(gone)} lower mast{'s' if gone != 1 else ''} gone")
        if self.odds > 0.0 and own_lb > 0.0:
            parts.append(f"against a broadside of {enemy_lb:g} pounds to our {own_lb:g}")
        elif self.odds > 0.0:
            parts.append(f"against a broadside of {enemy_lb:g} pounds and no guns of our own")
        return ", ".join(parts)

    @property
    def words(self) -> str:
        """The hands' temper in words, for `the bill`."""
        if self.value >= 0.7:
            return "steady"
        if self.value >= 0.5:
            return "firm"
        if self.value >= self.strike_below + 0.1:
            return "shaken"
        return "wavering"


def morale_of(ship: Any, doctrine: Any = None) -> Morale:
    """The ship's morale, made at the first call from her captain's doctrine (its
    `morale_start` and `strike_below`), else the defaults."""
    extra = ship.extra
    m = extra.get("morale")
    if isinstance(m, Morale):
        return m
    start = DEFAULT_START
    below = DEFAULT_STRIKE_BELOW
    if doctrine is not None:
        start = float(doctrine.threshold("morale_start", start))
        below = float(doctrine.threshold("strike_below", below))
    m = Morale(start=start, strike_below=below, value=start)
    extra["morale"] = m
    return m
