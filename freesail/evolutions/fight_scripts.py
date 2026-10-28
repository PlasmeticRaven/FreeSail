"""The fight's evolutions (spec M7 §11, §11a; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): the grapnels thrown and the small arms served
out. Each is an evolution of M3's kind (a file in `data/evolutions/` with its crew line,
its timing and its source), competing for hands as every evolution does; the effects are
states the game has: `extra["grappled_to"]` on both ships (`combat/boarding.py`), the
musketry's `served` (`combat/small_arms.py`).
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.scripts import PhasedScript
from freesail.ship.graph import Ship

__all__ = ["FIGHT_SCRIPTS", "GrappleScript", "ServeSmallArmsScript"]


def _world(ship: Ship) -> Any:
    from freesail.orders.prompt import world_of

    return world_of(ship)


class GrappleScript(PhasedScript):
    """The grapnels thrown into the enemy's chains and rigging: one phase, `grapnels`;
    refused beyond `GRAPPLE_RANGE_M`; at its end both ships grappled, if she has not
    drawn off meanwhile."""

    holds_subject = False
    DEFAULTS = {"grapnels": 120.0}

    def holds(self) -> set[str]:
        return {"grapnels"}

    def _target(self) -> Any:
        from freesail.combat.action import target_of
        from freesail.combat.guns import battery_of

        world = _world(self.ship)
        if world is None:
            return None
        tid = self.params.get("target")
        if not tid:
            battery = battery_of(self.ship)
            tid = getattr(battery, "target", None) if battery is not None else None
        if not tid:
            return None
        return target_of(world, str(tid))

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.combat.boarding import GRAPPLE_RANGE_M, grappled_to

        if grappled_to(self.ship):
            return "she is grappled already"
        target = self._target()
        if target is None:
            return "no enemy is engaged to grapple ('engage her to starboard' names her)"
        body = target.body
        if getattr(body, "extra", None) is None or body.extra.get("crew") is None:
            return "she is a far sail with no company modelled to fight"
        if target.range_m > GRAPPLE_RANGE_M:
            return (
                f"she is {target.range_m:.0f} metres off, beyond a grapnel's throw (thirty): "
                "'lay her aboard' first"
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        # the grapnels hold from the throw (the hands then haul the ships together for the
        # phase's minutes): both ships held from here, unless she has drawn off while the
        # hands were found
        from freesail.combat.boarding import GRAPPLE_RANGE_M, grapple

        self.start_phases(["grapnels"])
        world = _world(self.ship)
        target = self._target()
        if world is None or target is None:
            self._short = True
            return
        if target.range_m > GRAPPLE_RANGE_M * 1.5:
            from freesail.core.events import Severity

            self._short = True
            world.record(
                Severity.NOTABLE,
                "ship.grapnels_short",
                f"The grapnels fall short: {target.words} has drawn off to "
                f"{target.range_m:.0f} metres.",
            )
            return
        self._done_words = grapple(world, target, say=False)

    def end_phase(self, name: str) -> None:
        return

    def words(self) -> dict[str, Any]:
        target = self._target()
        who = target.words if target is not None else "the enemy"
        done = getattr(self, "_done_words", None) or (
            f"The grapnels fell short of {who}; she is not held."
            if getattr(self, "_short", False)
            else f"The grapnels are thrown at {who}."
        )
        return {
            "begin": (
                "Stand by the grapnels! The grapnels on their chains to the fore chains and "
                f"the gangway, to throw into {who}."
            ),
            "done": done,
            "verb_word": "grapple",
        }


class ServeSmallArmsScript(PhasedScript):
    """The small arms served out to the boarders from the arms chests: one phase, `arms`;
    at its end the musketry's `served`."""

    holds_subject = False
    DEFAULTS = {"arms": 300.0}

    def holds(self) -> set[str]:
        return {"small_arms"}

    def check(self, words: dict[str, Any]) -> str | None:
        from freesail.combat.small_arms import musketry_of

        if musketry_of(self.ship).served:
            return "the small arms are served out already"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["arms"])

    def end_phase(self, name: str) -> None:
        from freesail.combat.small_arms import musketry_of

        musketry_of(self.ship).served = True

    def words(self) -> dict[str, Any]:
        from freesail.combat.small_arms import small_arms_of

        world = _world(self.ship)
        arms = small_arms_of(world) if world is not None else {}
        what = str(arms.get("words") or "cutlasses, pikes, pistols and tomahawks")
        return {
            "begin": f"Serve out the small arms! The gunner's party at the arms chests: {what}.",
            "done": (
                "The small arms are served out: the boarders with their cutlasses and pistols, "
                "the pikes in the racks along the gangways, the muskets of the stand of arms to "
                "the small-arms men."
            ),
            "verb_word": "serve out",
        }


FIGHT_SCRIPTS: dict[str, type[PhasedScript]] = {
    "grapple": GrappleScript,
    "serve_small_arms": ServeSmallArmsScript,
}
