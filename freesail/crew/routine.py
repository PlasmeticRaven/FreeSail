"""The watch routine: watch changes, all hands and piping down, fatigue and rest (spec M3 §4).

The routine is the one thing in `crew/` that changes the crew's flags as time passes. The
watch bill (`crew/bill.py`) says who is on deck from those flags and the clock; the routine
sets the flags, writes the log lines for them, and keeps each sailor's fatigue.

- **Watch changes** (§4.1). When the clock's watch changes, the relief comes up and the
  relieved watch goes below; a hand at work (`at` set) stays until his evolution lets him go
  and goes below then (the bill keeps him on deck while `at` is set). An early relief
  (`relieve the watch`) holds until the clock's next watch change, which gives the deck back
  to the watch the bill names.
- **Idlers** come up at six and are piped down at eight in the evening (`bill.py`'s hours).
- **All hands** (§4.2). `call_all_hands` turns up everyone fit: a third of the hands below
  at once, the rest over `ALL_HANDS_DELAY_S`, in id order, each marked `turned_up` as he
  arrives; `Crew.all_hands_called` is set when the last is up, so that the bill shows the
  pool growing tick by tick. The hands already on deck at the call are marked `turned_up`
  too, so that no watch change or idlers' hour sends them below while all hands are up.
  `pipe_down` sends the watch below below again.
- **Fatigue and rest** (§4.3), per sailor per tick, as `rate * dt / 3600`, clamped to 0..1.

Nothing here draws randomness: the same crew, clock and calls give the same notes and the
same fatigues. Notes have the shape `Ship.step` yields, `(severity, kind, text, subject,
data)`; `tick` returns the ones the World records, and `call_all_hands`, `pipe_down` and
`relieve_watch` return theirs to the caller to record (the runner through `ship.note`, an
order through the World).
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.crew import bill
from freesail.crew.model import Crew, Sailor, Station, number_words

Note = tuple[str, str, str, str | None, dict[str, Any]]

# -- all hands (spec M3 §4.2) -----------------------------------------------------------

# Seconds from the call until the last hand is on deck: hammocks, ladders.
ALL_HANDS_DELAY_S = 90.0
# The hands below who come up at once, as a divisor: a third at the call, the rest in id
# order, evenly, over ALL_HANDS_DELAY_S.
ALL_HANDS_AT_ONCE_DIVISOR = 3

# -- fatigue and rest, per hour (spec M3 §4.3; provisional and soft, per the owner) ------

FATIGUE_ASLEEP_BELOW = -0.12  # below at night: the watch below asleep
FATIGUE_BELOW_BY_DAY = -0.08  # below by day
FATIGUE_ON_DECK_IDLE = 0.01  # on deck, not at work
FATIGUE_AT_WORK_ON_DECK = 0.06  # at work on deck: hauling, the capstan, the braces
FATIGUE_AT_WORK_ALOFT = 0.10  # at work aloft: loosing, furling, reefing
# Once, for a hand turned up out of his sleep by a call for all hands at night.
FATIGUE_ALL_HANDS_AT_NIGHT = 0.03

# Night, for sleep and for the cost of a call: from the end of the second dog watch to the
# start of the morning watch. Hours of ship's time.
NIGHT_BEGINS_HOUR = 20
NIGHT_ENDS_HOUR = 4

SECONDS_PER_HOUR = 3600.0


def is_night(when: datetime) -> bool:
    return when.hour >= NIGHT_BEGINS_HOUR or when.hour < NIGHT_ENDS_HOUR


def _note(severity: Severity, kind: str, text: str, data: dict[str, Any]) -> Note:
    return (severity.value, kind, text, None, data)


def _bells_words(bells: int) -> str:
    return f"{number_words(bells).capitalize()} {'bell' if bells == 1 else 'bells'}"


class Routine:
    """The watch routine of one ship's company, driven by the World once a tick."""

    def __init__(self, crew: Crew, clock: Any):
        self.crew = crew
        self.clock = clock
        self._watch_name = clock.watch()
        self._deck_watch = bill.watch_on_deck(crew, clock)
        self._idlers_up = bill.idlers_up(clock)
        # An all-hands call under way: the hands still to come, in id order, how many came
        # at once, when the call was made and whether it was made at night.
        self._coming: list[Sailor] = []
        self._first: int = 0
        self._arrived: int = 0
        self._called_at: datetime | None = None
        self._called_at_night = False
        # Who is at work aloft rather than on deck (package 17 knows the step): sailor ids,
        # and evolution instances whose every hand is aloft.
        self._aloft_ids: frozenset[str] = frozenset()
        self._aloft_instances: set[str] = set()

    # -- the seam for the hands' pool (package 17) ------------------------------------

    def set_aloft(self, sailor_ids: Iterable[str]) -> None:
        """Name the sailors at work aloft now, replacing the last set. Default: on deck."""
        self._aloft_ids = frozenset(sailor_ids)

    def set_instance_aloft(self, inst_id: str, aloft: bool) -> None:
        """Mark every hand held by an evolution instance as aloft (or not) from now on."""
        if aloft:
            self._aloft_instances.add(inst_id)
        else:
            self._aloft_instances.discard(inst_id)

    def is_aloft(self, sailor: Sailor) -> bool:
        return sailor.at is not None and (
            sailor.id in self._aloft_ids or sailor.at in self._aloft_instances
        )

    @property
    def calling(self) -> bool:
        """True while a call for all hands is under way and not all are up yet."""
        return self._called_at is not None

    # -- the tick -------------------------------------------------------------------

    def tick(self, ship: Any, dt: float) -> list[Note]:
        """One tick of the routine at the clock's present time. Returns log notes."""
        notes: list[Note] = []
        if self._called_at is not None:
            notes.extend(self._arrivals())
        name = self.clock.watch()
        if name != self._watch_name:
            notes.append(self._watch_change(name))
        up = bill.idlers_up(self.clock)
        if up != self._idlers_up:
            self._idlers_up = up
            note = self._idlers(up)
            if note is not None:
                notes.append(note)
        self._fatigue(dt)
        self._deck_watch = bill.watch_on_deck(self.crew, self.clock)
        return notes

    def _watch_change(self, name: str) -> Note:
        relieved = self._deck_watch
        self._watch_name = name
        self.crew.watch_on_deck = None  # an early relief lasts until the clock's next watch
        relief = bill.watch_on_duty(self.clock)
        bells = units.bells_at(self.clock.ship_time)
        head = f"{_bells_words(bells)}. " if bells is not None else ""
        at_work = sum(1 for s in self.crew.by_watch[relieved] if s.at is not None)
        if self.crew.all_hands_called or self._called_at is not None:
            text = f"{head}All hands on deck; the {relief.value} watch has the deck."
        elif relief is relieved:
            text = f"{head}The {relief.value} watch kept the deck."
        else:
            text = f"{head}The {relief.value} watch relieved the deck."
        data = {
            "watch": name,
            "relief": relief.value,
            "relieved": relieved.value,
            "bells": bells,
            "at_work": at_work if relief is not relieved else 0,
        }
        return _note(Severity.ROUTINE, "watch.relieved", text, data)

    def _idlers(self, up: bool) -> Note | None:
        if not self.crew.by_station[Station.IDLERS]:
            return None
        if self.crew.all_hands_called or self._called_at is not None:
            return None  # they are on deck with all hands, and go below when piped down
        if up:
            return _note(Severity.ROUTINE, "crew.idlers_up", "Idlers up.", {})
        return _note(Severity.ROUTINE, "crew.idlers_down", "Piped the idlers down.", {})

    def _fatigue(self, dt: float) -> None:
        scale = dt / SECONDS_PER_HOUR
        aloft = FATIGUE_AT_WORK_ALOFT * scale
        work = FATIGUE_AT_WORK_ON_DECK * scale
        idle = FATIGUE_ON_DECK_IDLE * scale
        rest = FATIGUE_ASLEEP_BELOW if is_night(self.clock.ship_time) else FATIGUE_BELOW_BY_DAY
        rest *= scale
        crew = self.crew
        watch = bill.watch_on_deck(crew, self.clock)
        up = bill.idlers_up(self.clock)
        everyone = crew.all_hands_called
        aloft_ids, aloft_insts = self._aloft_ids, self._aloft_instances
        quarterdeck, idlers = Station.QUARTERDECK, Station.IDLERS
        for s in crew.sailors:
            station = s.station
            if station is quarterdeck:
                continue  # the officers are not in the hands' pool; their rest is not kept
            if s.at is not None:
                d = aloft if (s.id in aloft_ids or s.at in aloft_insts) else work
            # on deck and idle: the rule of `bill.on_deck`, written out here because this
            # loop runs for every sailor every tick (tests/test_routine.py holds them equal)
            elif s.fit and (
                everyone or s.turned_up or (up if station is idlers else s.watch is watch)
            ):
                d = idle
            else:
                d = rest
            f = s.fatigue + d
            s.fatigue = 0.0 if f < 0.0 else (1.0 if f > 1.0 else f)

    # -- all hands and piping down (spec M3 §4.2) ----------------------------------------

    def call_all_hands(self, reason: str, by_order: bool = False) -> Note | None:
        """Turn the hands up. Returns the notable line, or None if all hands are up already.

        `by_order` is for the captain's own call (package 20's order): it sets
        `all_hands_called_by_order`, so that the runner does not pipe down when its
        all-hands evolution ends. A call by order while all hands are up already sets the
        flag and writes no line.
        """
        crew = self.crew
        if by_order:
            crew.all_hands_called_by_order = True
        if crew.all_hands_called or self._called_at is not None:
            return None
        now = self.clock.ship_time
        deck = {s.id for s in bill.on_deck(crew, now)}
        coming: list[Sailor] = []
        for s in crew.sailors:
            if s.station is Station.QUARTERDECK or not s.fit:
                continue
            if s.id in deck:
                s.turned_up = True  # up already: stays up whatever the bells say
            else:
                coming.append(s)
        self._coming = coming
        self._first = -(-len(coming) // ALL_HANDS_AT_ONCE_DIVISOR)
        self._arrived = 0
        self._called_at = now
        self._called_at_night = is_night(now)
        self._arrive(self._first)
        if self._arrived >= len(coming):
            self._all_up()
        text = f"All hands! ({reason})"
        data = {
            "reason": reason,
            "by_order": by_order,
            "on_deck": len(deck),
            "coming": len(coming),
            "at_once": self._first,
        }
        return _note(Severity.NOTABLE, "crew.all_hands", text, data)

    def _arrive(self, upto: int) -> None:
        for s in self._coming[self._arrived : upto]:
            s.turned_up = True
            if self._called_at_night:
                s.fatigue = min(1.0, s.fatigue + FATIGUE_ALL_HANDS_AT_NIGHT)
        self._arrived = max(self._arrived, upto)

    def _arrivals(self) -> list[Note]:
        assert self._called_at is not None
        elapsed = (self.clock.ship_time - self._called_at).total_seconds()
        n = len(self._coming)
        rest = n - self._first
        if elapsed >= ALL_HANDS_DELAY_S:
            upto = n
        else:
            upto = self._first + int(rest * max(elapsed, 0.0) // ALL_HANDS_DELAY_S)
        self._arrive(upto)
        if self._arrived < n:
            return []
        self._all_up()
        up = len(bill.on_deck(self.crew, self.clock))
        return [_note(Severity.ROUTINE, "crew.all_hands_up", "All hands on deck.", {"hands": up})]

    def _all_up(self) -> None:
        self.crew.all_hands_called = True
        self._coming = []
        self._called_at = None

    def pipe_down(self) -> Note | None:
        """Pipe down: the watch below goes below. None, and no line, if nobody was up."""
        crew = self.crew
        turned = [s for s in crew.sailors if s.turned_up]
        if not (crew.all_hands_called or self._called_at is not None or turned):
            return None
        for s in turned:
            s.turned_up = False
        crew.all_hands_called = False
        crew.all_hands_called_by_order = False
        self._coming = []
        self._called_at = None
        watch = bill.watch_on_deck(crew, self.clock)
        self._deck_watch = watch
        text = f"Piped down; the {watch.value} watch has the deck."
        data = {"watch": watch.value, "on_deck": len(bill.on_deck(crew, self.clock))}
        return _note(Severity.ROUTINE, "crew.piped_down", text, data)

    # -- relieve the watch (spec M3 §5.1) -----------------------------------------------

    def relieve_watch(self) -> Note:
        """An early watch change: the other watch takes the deck until the next bells' change.

        Hands of the relieved watch at work stay until their evolution lets them go.
        """
        crew = self.crew
        relieved = bill.watch_on_deck(crew, self.clock)
        relief = bill.watch_below(relieved)
        crew.watch_on_deck = None if relief is bill.watch_on_duty(self.clock) else relief
        self._deck_watch = relief
        at_work = sum(1 for s in crew.by_watch[relieved] if s.at is not None)
        text = f"The {relief.value} watch relieved the deck."
        data = {"relief": relief.value, "relieved": relieved.value, "early": True}
        data["at_work"] = at_work
        return _note(Severity.ROUTINE, "watch.relieved", text, data)
