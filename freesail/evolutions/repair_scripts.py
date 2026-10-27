"""The damage control's evolutions (spec M7 §13, §14; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): the hatches battened, the shot holes plugged and
the leaks caulked, a sail fothered over the leak, a sprung spar fished, the preventers and
the chain slings before an action, the standing rigging set up again, a mast cut away, a
jury mast from the booms. Each is an evolution of M3's kind (a file in `data/evolutions/`
with its crew line, its timing and its source; the script where a step list cannot decide
what the work finds), competing for hands with the guns and the sails by the fighting
book's priority as every evolution does, and consuming a counted store (the carpenter's
shot plugs, the boatswain's cordage, the sail room, the booms). The effects are states the
game has (rule 1): a hole `plugged`, the ground's leak nought, a line's `preventer`, a
spar's condition, a lower mast standing again as a jury mast.

The times are judgement with their sources in the files; nothing here draws randomness.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.scripts import PhasedScript
from freesail.ship.graph import Ship

__all__ = ["REPAIR_SCRIPTS", "BattenDownScript"]


def _world(ship: Ship) -> Any:
    from freesail.orders.prompt import world_of

    return world_of(ship)


def _water_state(ship: Ship) -> Any:
    from freesail.world.water import water_of

    return water_of(ship)


class BattenDownScript(PhasedScript):
    """Batten down the hatches, or take the battens off (`params.open`): one phase,
    `battens`; at its end the water's state has the hatches battened or open."""

    DEFAULTS = {"battens": 600.0}

    def holds(self) -> set[str]:
        return {"hatches"}

    @property
    def opening(self) -> bool:
        return bool(self.params.get("open"))

    def check(self, words: dict[str, Any]) -> str | None:
        st = _water_state(self.ship)
        if st is None:
            return "she has no hatches to speak of"
        if self.opening and not st.hatches_battened:
            return "the hatches are open already"
        if not self.opening and st.hatches_battened:
            return "the hatches are battened down already"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["battens"])

    def end_phase(self, name: str) -> None:
        st = _water_state(self.ship)
        if st is not None:
            st.hatches_battened = not self.opening

    def words(self) -> dict[str, Any]:
        if self.opening:
            return {
                "begin": "Take the battens off the hatches!",
                "done": "The hatches are open again, the tarpaulins off and stowed.",
                "verb_word": "open",
            }
        return {
            "begin": "Batten down the hatches! The tarpaulins on and the battens nailed down.",
            "done": "The hatches are battened down: the tarpaulins on and the battens wedged; "
            "the sea she ships comes no further than the deck.",
            "verb_word": "batten down",
        }


REPAIR_SCRIPTS: dict[str, type[PhasedScript]] = {
    "batten_down": BattenDownScript,
}
