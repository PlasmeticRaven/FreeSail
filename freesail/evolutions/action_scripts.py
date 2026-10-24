"""The evolutions that move the ship between the watch bill and the quarter bill (spec M7
§8, §8a; package 70; `docs/design/Design-WorkInAction.md`): clearing for action, casting
loose the guns and securing them (the beat itself is a crew order, `orders.crew`, for the
same reason `call all hands` is: the drum does not queue behind the work in hand). Each is
an all-hands evolution of M3's kind (hands, a duration and phases) whose last phase hands
the company to the quarter bill (`crew.quarters.Quarters.beat`) or back (`stand_down`);
the guns' service after the beat is no evolution's but the battery's own cycle
(`combat.guns`).

The times are the period's by the ship's size: a frigate cleared for action in a quarter
of an hour and a cutter in five minutes (spec M7 §8; the logs of 1805 say "cleared for
action" ten to twenty minutes after "beat to quarters" in a frigate, and a cutter's
company had little to clear), scaled by her length between the two (judgement); the drum
beat and the hands at their stations in a minute and a half; the guns cast loose and
provided in a minute (Douglas 1820, part II: "Cast loose your guns", the tackles cast off
and the tompions out); the guns secured in two (run in, housed, the breechings and the
tackles frapped). Every figure is the file's to tune.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.scripts import PhasedScript
from freesail.ship.graph import Ship

__all__ = [
    "ACTION_SCRIPTS",
    "CastLooseScript",
    "ClearForActionScript",
    "MakeSignalScript",
    "SecureGunsScript",
]

# The frigate's quarter of an hour at her length, the cutter's five minutes at hers
# (spec M7 §8): the clearing's time by length between the two (judgement).
FRIGATE_LENGTH_M = 44.0
FRIGATE_CLEAR_S = 900.0
CUTTER_LENGTH_M = 20.0
CUTTER_CLEAR_S = 300.0


def clear_seconds(ship: Ship) -> float:
    """The seconds to clear for action by her length, the quarters' beat not counted."""
    length = float(getattr(getattr(ship, "hull", None), "length", CUTTER_LENGTH_M) or 0.0)
    if length <= CUTTER_LENGTH_M:
        return CUTTER_CLEAR_S
    if length >= FRIGATE_LENGTH_M:
        return FRIGATE_CLEAR_S
    f = (length - CUTTER_LENGTH_M) / (FRIGATE_LENGTH_M - CUTTER_LENGTH_M)
    return CUTTER_CLEAR_S + f * (FRIGATE_CLEAR_S - CUTTER_CLEAR_S)


def _quarters(ship: Ship) -> Any:
    from freesail.crew.quarters import quarters_of

    return quarters_of(ship)


class _QuartersScript(PhasedScript):
    """The common ground: the quarters, the guns, and the beat as a phase."""

    def holds(self) -> set[str]:
        # no manoeuvre's hold: the drum beats through a tack or a heave-to in hand
        return set()

    def _beat(self) -> None:
        q = _quarters(self.ship)
        if q is None:
            return
        from freesail.orders.prompt import world_of

        world = world_of(self.ship)
        tick = int(world.clock.tick) if world is not None else 0
        for line in q.beat(tick):
            self.note(line, kind="quarters.beat")

    def _guns(self) -> list[Any]:
        return list(getattr(self.ship, "guns", {}).values())

    def _turn_up(self) -> None:
        """All hands turned up by the drum, as by the captain's own call (the runner does
        not pipe them down after)."""
        routine = self.ship.extra.get("routine")
        call = getattr(routine, "call_all_hands", None)
        if call is None:
            return
        note = call("to beat to quarters", by_order=True)
        if note is not None:
            severity, kind, text, subject, data = note
            self.ship.note(str(getattr(severity, "value", severity)), kind, text, subject, data)


class ClearForActionScript(_QuartersScript):
    """Clear for action: the cabin bulkheads down and the furniture struck below, the
    galley fire out, the decks wetted and sanded and the match tubs and shot garlands
    filled, the boats hoisted out to tow astern; then the drum beats to quarters. Phases
    `bulkheads`, `galley`, `decks`, `boats`, `quarters`, their seconds shares of the
    ship's clearing time (`clear_seconds`), the beat its own."""

    DEFAULTS = {"quarters": 90.0}
    SHARES = {"bulkheads": 0.35, "galley": 0.1, "decks": 0.35, "boats": 0.2}

    def check(self, words: dict[str, Any]) -> str | None:
        if self.ship.extra.get("cleared") and (_quarters(self.ship) or None) is not None:
            if _quarters(self.ship).at_quarters:
                return "She is cleared for action and the hands at quarters already."
        return None

    def phase_s(self, name: str) -> float:
        if name in self.SHARES:
            return self.timing_value(f"{name}_s", self.SHARES[name] * clear_seconds(self.ship))
        return super().phase_s(name)

    def begin(self, words: dict[str, Any]) -> None:
        phases = [] if self.ship.extra.get("cleared") else ["bulkheads", "galley", "decks", "boats"]
        self.start_phases([*phases, "quarters"])

    def end_phase(self, name: str) -> None:
        if name == "bulkheads":
            self.note("The bulkheads are down and the cabin furniture struck below.")
        elif name == "galley":
            self.note("The galley fire is out.")
        elif name == "decks":
            self.note("The decks wetted and sanded; the match tubs and the shot garlands filled.")
        elif name == "boats":
            self.ship.extra["cleared"] = True
            self.note("The boats are out and towing astern; the ship is clear.")
        elif name == "quarters":
            self._beat()

    def words(self) -> dict[str, Any]:
        q = _quarters(self.ship)
        return {"quarters": " ".join(q.describe()[:2]) if q is not None else ""}


def _crews_present_share(ship: Ship) -> float:
    """The share of the gun crews' hands at their guns now (the men still coming up, or
    at sail work, are not): the time the crews' work takes stretches by its inverse, a
    quarter of them at the least."""
    q = _quarters(ship)
    if q is None or not q.at_quarters:
        return 1.0
    wanted = sum(gc.wanted for gc in q.crews.values())
    at = sum(len(gc.hands) for gc in q.crews.values())
    if wanted <= 0:
        return 1.0
    return max(0.25, min(1.0, at / wanted))


class CastLooseScript(_QuartersScript):
    """Cast loose the guns: the crews cast off the tackles and the breechings' lashings,
    take out the tompions and provide the guns (Douglas 1820, part II); one phase,
    `cast_loose`. Wanted at quarters; refused in words before the beat."""

    DEFAULTS = {"cast_loose": 60.0}

    def check(self, words: dict[str, Any]) -> str | None:
        q = _quarters(self.ship)
        if q is None or not q.at_quarters:
            return "the hands are not at quarters; beat to quarters first"
        if all(g.cast_loose or not g.serves for g in self._guns()):
            return "the guns are cast loose already"
        return None

    def phase_s(self, name: str) -> float:
        return super().phase_s(name) / _crews_present_share(self.ship)

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["cast_loose"])

    def end_phase(self, name: str) -> None:
        n = 0
        for g in self._guns():
            if g.serves and not g.cast_loose:
                g.cast_loose = True
                n += 1
        self.count = n

    def words(self) -> dict[str, Any]:
        return {"count": getattr(self, "count", 0)}


class SecureGunsScript(_QuartersScript):
    """Secure the guns: run in, housed and the tackles frapped, the tompions in; one
    phase, `secure`; at its end the company goes back under the watch bill (the quarters
    stood down), and the runner pipes the hands down as after any all-hands work."""

    DEFAULTS = {"secure": 120.0}

    def check(self, words: dict[str, Any]) -> str | None:
        q = _quarters(self.ship)
        at_quarters = q is not None and q.at_quarters
        if not at_quarters and all(not g.cast_loose for g in self._guns()):
            return "the guns are secured already and the hands under the watch bill"
        return None

    def phase_s(self, name: str) -> float:
        return super().phase_s(name) / _crews_present_share(self.ship)

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["secure"])

    def end_phase(self, name: str) -> None:
        for g in self._guns():
            g.cast_loose = False
            g.run_out = False
            g.primed = False
        battery = self.ship.extra.get("battery")
        if battery is not None:
            from freesail.combat.guns import FireMode

            battery.mode = FireMode.HOLD
            battery.word = None
            battery.single = []
        q = _quarters(self.ship)
        if q is not None and q.at_quarters:
            q.stand_down()

    def words(self) -> dict[str, Any]:
        loaded = sum(1 for g in self._guns() if g.loaded)
        return {"loaded": loaded}


class MakeSignalScript(PhasedScript):
    """Make a signal (spec M7 §3; package 71): the flags bent on and run up, a phase a
    hoist of `hoist_s` (a telegraphic sentence a phase a word), the hoist breaking out on
    the ship's body at the end of its first minute and complete at the end of its last
    (`signals.Hoist.breaks_out`, `complete_at`, set when the work begins and not when it
    was ordered, so a hoist queued behind other work waits its hands). Fails with the
    hoist hauled down when the hands cannot be had."""

    DEFAULTS = {"hoist": 60.0}

    def holds(self) -> set[str]:
        return set()  # the halyards are nobody's hold: a signal is made through any work

    def _tick(self) -> int:
        from freesail.orders.prompt import world_of

        world = world_of(self.ship)
        return int(world.clock.tick) if world is not None else 0

    def _hoist(self) -> Any:
        from freesail.world.signals import locker_of

        key = str(self.params.get("hoist_key") or "")
        locker = locker_of(self.ship)
        for h in [*locker.flying, *reversed(locker.made)]:
            if h.key == key:
                return h
        return None

    def check(self, words: dict[str, Any]) -> str | None:
        return None if self._hoist() is not None else "no signal is bent on"

    def phase_s(self, name: str) -> float:
        return self.timing_value("hoist_s", 60.0)

    def begin(self, words: dict[str, Any]) -> None:
        n = max(1, int(self.params.get("hoists") or 1))
        h = self._hoist()
        tick = self._tick()
        hoist_s = int(self.phase_s("hoist"))
        if h is not None:
            h.breaks_out = tick + hoist_s
            h.complete_at = tick + hoist_s * n if n > 1 else None
        self.start_phases([f"hoist_{i + 1}" for i in range(n)])

    def end_phase(self, name: str) -> None:
        h = self._hoist()
        if h is None or h.book != "telegraphic":
            return
        i = int(name.rsplit("_", 1)[-1]) - 1
        if 0 <= i < len(h.words_made):
            self.note(
                f"The telegraph: hoist {i + 1} of {len(h.words_made)}, '{h.words_made[i]}' "
                f"({h.numbers[i]}).",
                kind="signal.hoist",
            )

    def fail(self, reason: str) -> None:
        super().fail(reason)
        h = self._hoist()
        if h is not None and h.down is None:
            h.down = self._tick()

    def words(self) -> dict[str, Any]:
        return {"words": str(self.params.get("words") or "the signal")}


ACTION_SCRIPTS: dict[str, type[PhasedScript]] = {
    "clear_for_action": ClearForActionScript,
    "cast_loose_guns": CastLooseScript,
    "secure_guns": SecureGunsScript,
    "make_signal": MakeSignalScript,
}
