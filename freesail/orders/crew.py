"""The crew orders (spec M3 §5.1): all hands, piping down, relieving the watch, and the
hands selector that gives a piece of work to one watch or one station.

- `call all hands` turns the hands up through the watch routine (`crew/routine.py`),
  with the captain's reason, so that the runner does not pipe down when its own
  all-hands work ends. A second call while they are up says so and changes nothing
  but that flag.
- `pipe down` sends the watch below below again; it is refused while an all-hands
  evolution is still at work, and answered in words when nobody is turned up.
- `relieve the watch` is the routine's early watch change.
- The hands selector ("send the larboard watch aloft to furl the main course", "set
  the fore topsail with the fore topmen") is carried by the grammar as the modifier
  `hands_from` and reaches the runner in the evolution's params, where it narrows the
  pool to that watch or station. A watch that is below is turned up for the work: a
  `WatchCall`, the same staged arrival as all hands for that watch alone (a third at
  once, the rest in id order over `routine.ALL_HANDS_DELAY_S`), which the runner
  advances once a tick.

`muster` is a query, not an order: the console answers it (`api/queries.muster_lines`),
as it answers `state`, and it is never journaled.

Replies are `(kind, log_text, data)` like every verb's. Nothing here draws randomness.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any

from freesail.crew import bill, hands
from freesail.crew.model import STATION_NAMES, Crew, Sailor, Station, Watch, number_words
from freesail.crew.routine import (
    ALL_HANDS_AT_ONCE_DIVISOR,
    ALL_HANDS_DELAY_S,
    FATIGUE_ALL_HANDS_AT_NIGHT,
    is_night,
)
from freesail.evolutions import registry
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.ship.graph import Ship

Result = tuple[str, str, dict[str, Any]]

# Where the watches being turned up are kept for the runner to advance each tick.
WATCH_CALLS = "watch_calls"

# When neither the routine nor the runner has a clock (a ship without a World), the watch
# bill is read at the default scenario's start, as the runner reads it.
DEFAULT_WATCH_TIME = datetime(1805, 6, 1, 4, 0, 0)

# The evolutions that are going about: piping down while one runs is refused with Luce's
# words for it rather than the general sentence.
ABOUT_SHIP = ("tack", "wear", "wear_short_round", "boxhaul")


# ---------------------------------------------------------------------------
# Finding the crew, the routine and the time
# ---------------------------------------------------------------------------


def crew_of(ship: Ship) -> Crew | None:
    crew = ship.extra.get("crew")
    return crew if isinstance(crew, Crew) else None


def _routine(ship: Ship, verb: str) -> Any:
    routine = ship.extra.get("routine")
    if crew_of(ship) is None or routine is None:
        raise OrderError(
            f"There is no ship's company mustered in this ship; '{verb}' has no one to call."
        )
    return routine


def now_of(ship: Ship) -> datetime:
    """The ship's time: the routine's clock, else the runner's, else the default start."""
    for holder in (ship.extra.get("routine"), ship.extra.get("evolutions")):
        clock = getattr(holder, "clock", None)
        if clock is not None:
            return bill.when_of(clock)
    return DEFAULT_WATCH_TIME


# ---------------------------------------------------------------------------
# All hands, piping down, relieving the watch
# ---------------------------------------------------------------------------


def whose_order(ship: Any) -> str:
    """Whose order is being carried out, as the log's lines say it: "the captain's",
    or a station's when one gives it ("the officer of the watch's"; package 37g, item 10:
    all hands called by the officer under the captain's grant were logged "by the
    captain's order", and so was a reckoning he set). The World keeps the order's actor
    on the ship while its handler runs (`core.world.ORDER_ACTOR`); a standing order's
    firing is the captain's book's, and reads as his, as it did."""
    from freesail.core.events import STATION_ACTORS

    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "")
    # the player's seat at a station gives orders under the station's actor with a word
    # after it (package 40; `agents.seat`): the lines say they were the station's
    station = actor.split(" (", 1)[0]
    return f"{station}'s" if station in STATION_ACTORS else "the captain's"


def call_all_hands(ship: Ship, order: Order) -> Result:
    routine = _routine(ship, order.verb)
    crew = crew_of(ship)
    assert crew is not None
    already = crew.all_hands_called or routine.calling
    whose = whose_order(ship)
    note = routine.call_all_hands(f"by {whose} order", by_order=True)
    crew.all_hands_called_by = whose
    data: dict[str, Any] = {"verb": order.verb, "level": 1, "all_hands": True}
    if note is None:
        if already and not crew.all_hands_called:
            text = "All hands are called already; the watch below is coming up."
        else:
            text = "All hands are on deck already; they stay up until piped down."
        return "crew.order", text, data
    severity, kind, text, subject, note_data = note
    ship.note(severity, kind, text, subject, note_data)
    coming = int(note_data.get("coming", 0))
    data.update(note_data)
    if coming:
        reply = (
            f"The boatswain's mates pipe all hands at the hatchways; "
            f"{_hands(coming)} turning out below."
        )
    else:
        reply = "The boatswain's mates pipe all hands; every hand is on deck already."
    return "crew.order", reply, data


def pipe_down(ship: Ship, order: Order) -> Result:
    routine = _routine(ship, order.verb)
    busy = all_hands_work(ship)
    if busy:
        raise OrderError(busy)
    note = routine.pipe_down()
    ship.extra.pop(WATCH_CALLS, None)  # a watch still coming up goes below with the rest
    data: dict[str, Any] = {"verb": order.verb, "level": 1}
    if note is None:
        watch = bill.watch_on_deck(routine.crew, now_of(ship))
        return (
            "crew.order",
            f"Nobody is turned up; the {watch.value} watch has the deck.",
            data,
        )
    _severity, kind, text, _subject, note_data = note
    data.update(note_data)
    return kind, text, data


def relieve_watch(ship: Ship, order: Order) -> Result:
    routine = _routine(ship, order.verb)
    _severity, kind, text, _subject, note_data = routine.relieve_watch()
    data: dict[str, Any] = {"verb": order.verb, "level": 1}
    data.update(note_data)
    return kind, text, data


def _watch_said(phrase: str) -> Watch | None:
    """The watch a phrase names by its side ('call the starboard watch'), or None."""
    words = phrase.split()
    if "starboard" in words:
        return Watch.STARBOARD
    if "larboard" in words or "port" in words:
        return Watch.LARBOARD
    return None


def call_watch(ship: Ship, order: Order) -> Result:
    """`call the starboard watch`, `call the watch below` (package 37l; game 10): the
    watch below turned up by itself, as a watch sent to a piece of work is (`WatchCall`:
    a third at once, the rest over the minutes), up until piped down. A watch that has the
    deck, or all hands up already, is answered so and nothing changes."""
    _routine(ship, order.verb)
    crew = crew_of(ship)
    assert crew is not None
    when = now_of(ship)
    deck = bill.watch_on_deck(crew, when)
    named = _watch_said(order.verb_phrase) or bill.watch_below(deck)
    data: dict[str, Any] = {"verb": order.verb, "level": 1, "watch": named.value}
    if crew.all_hands_called:
        return "crew.order", "All hands are on deck already; they stay up until piped down.", data
    if named is deck:
        return "crew.order", f"The {named.value} watch has the deck already.", data
    if any(c.watch is named for c in ship.extra.get(WATCH_CALLS, [])):
        return "crew.order", f"The {named.value} watch is coming up already.", data
    call = WatchCall(crew, named, when)
    if not call.coming:
        return "crew.order", f"Every hand of the {named.value} watch is on deck already.", data
    call.note_at = len(getattr(ship, "notes", []))
    commit(ship, call)
    data["coming"] = len(call.coming)
    return (
        "crew.order",
        f"The boatswain's mates call the {named.value} watch at the hatchways; "
        f"{_hands(len(call.coming))} turning out below. They stay up until piped down.",
        data,
    )


CREW_VERBS: dict[str, Callable[[Ship, Order], Result]] = {
    "call all hands": call_all_hands,
    "call the watch": call_watch,
    "pipe down": pipe_down,
    "relieve the watch": relieve_watch,
}


def all_hands_work(ship: Ship) -> str | None:
    """A sentence if an all-hands evolution is still at work, else None."""
    runner = ship.extra.get("evolutions")
    if runner is None or not hasattr(runner, "in_progress"):
        return None
    for entry in runner.in_progress():
        if entry.get("waiting") or entry.get("paused"):
            continue
        evo = registry.get(entry["id"])
        if evo is None or not _is_all_hands(evo):
            continue
        if evo.id in ABOUT_SHIP:
            return "The hands are still about ship; wait for her to come round."
        return (
            f"All hands are still at work ({_doing(ship, evo, entry['subject'])}); "
            f"pipe down when it is done."
        )
    return None


def _doing(ship: Ship, evo: registry.Evolution, subject: str) -> str:
    from freesail.evolutions.runner import gerund, part_name

    verb = evo.verb.replace("_", " ")
    first, _, rest = verb.partition(" ")
    doing = f"{gerund(first)} {rest}".strip()
    if subject in ship.parts:
        return f"{doing} the {part_name(ship, subject)}"
    return doing


def _is_all_hands(evo: registry.Evolution) -> bool:
    return str((evo.crew or {}).get("hands", "")).strip().lower() == hands.ALL


def _hands(n: int) -> str:
    return f"{number_words(n)} {'hand' if n == 1 else 'hands'}"


# ---------------------------------------------------------------------------
# The hands selector
# ---------------------------------------------------------------------------


def selection_name(selector: str) -> str:
    """'larboard' -> 'larboard watch', 'fore_top' -> 'fore topmen'."""
    if selector in (w.value for w in Watch):
        return f"{selector} watch"
    try:
        return STATION_NAMES[Station(selector)][1]
    except ValueError:
        return selector.replace("_", " ")


def _selected(crew: Crew, selector: str) -> list[Sailor]:
    if selector in (Watch.STARBOARD.value, Watch.LARBOARD.value):
        return [s for s in crew.by_watch[Watch(selector)] if s.station is not Station.QUARTERDECK]
    return list(crew.by_station.get(Station(selector), []))


def _aloft(evo: registry.Evolution) -> bool:
    """Whether any of the work is aloft, as the runner reads it."""
    if evo.script is not None:
        return bool(evo.params.get("aloft"))
    return any(step.aloft for step in evo.steps)


class WatchCall:
    """A watch turned up out of its turn for a piece of work (spec M3 §5.1).

    The same staged arrival as all hands (`crew/routine.py`), for that watch alone: a
    third of the hands below at once, the rest in id order over `ALL_HANDS_DELAY_S`,
    each marked `turned_up` as he comes; turned up at night, each pays the broken
    sleep of a call. The hands stay up until piped down, as all hands do. `tick`
    advances it; `cancel` undoes it if the order that made it is refused.
    """

    def __init__(self, crew: Crew, watch: Watch, when: datetime):
        self.watch = watch
        deck = {s.id for s in bill.on_deck(crew, when)}
        self.coming = [
            s
            for s in crew.by_watch[watch]
            if s.fit and s.station is not Station.QUARTERDECK and s.id not in deck
        ]
        self.first = -(-len(self.coming) // ALL_HANDS_AT_ONCE_DIVISOR)
        self.arrived = 0
        self.called_at = when
        self.night = is_night(when)
        self.note_at = 0  # where in the ship's notes its "Turned up" line goes
        self._arrive(self.first)

    def _arrive(self, upto: int) -> None:
        for s in self.coming[self.arrived : upto]:
            s.turned_up = True
            if self.night:
                s.fatigue = min(1.0, s.fatigue + FATIGUE_ALL_HANDS_AT_NIGHT)
        self.arrived = max(self.arrived, upto)

    def tick(self, clock: Any) -> bool:
        """Bring up the hands due by now. True while some are still to come."""
        if any(not s.turned_up for s in self.coming[: self.arrived]):
            return False  # piped down meanwhile: the rest stay below
        elapsed = (bill.when_of(clock) - self.called_at).total_seconds()
        n = len(self.coming)
        if elapsed >= ALL_HANDS_DELAY_S:
            upto = n
        else:
            upto = self.first + int((n - self.first) * max(elapsed, 0.0) // ALL_HANDS_DELAY_S)
        self._arrive(upto)
        return self.arrived < n

    def cancel(self) -> None:
        for s in self.coming[: self.arrived]:
            s.turned_up = False
            if self.night:
                s.fatigue = max(0.0, s.fatigue - FATIGUE_ALL_HANDS_AT_NIGHT)
        self.arrived = 0


def take_hands_from(
    ship: Ship, order: Order, evolution_ids: list[str]
) -> tuple[dict[str, Any], WatchCall | None]:
    """Check a hands selector against the work and the crew, and turn the watch up if it
    is below. Returns the params to add to each evolution (``{"hands_from": ...}``, or
    nothing when no selector was said) and the watch call, if one was made, for the
    caller to `commit` once an evolution has started, or to `cancel` if none has.
    """
    selector = order.modifiers.get("hands_from")
    if selector is None:
        return {}, None
    name = selection_name(selector)
    crew = crew_of(ship)
    if crew is None:
        raise OrderError(
            f"There is no ship's company mustered in this ship to send the {name} to it."
        )
    men = _selected(crew, selector)
    if not men:
        raise OrderError(f"There are no {name} in this ship.")
    for evo_id in dict.fromkeys(evolution_ids):
        evo = registry.get(evo_id)
        if evo is None:
            continue
        if _is_all_hands(evo):
            raise OrderError(
                f"'{order.verb}' is work for all hands; a watch or a station is not sent to it."
            )
        aloft = _aloft(evo)
        if not any(hands.can_work(s, aloft) for s in men):
            raise OrderError(f"The {name} do not go aloft; send topmen, or a watch, to work aloft.")
    when = now_of(ship)
    call: WatchCall | None = None
    if selector in (Watch.STARBOARD.value, Watch.LARBOARD.value):
        watch = Watch(selector)
        up = crew.all_hands_called or bill.watch_on_deck(crew, when) is watch
        coming = any(c.watch is watch for c in ship.extra.get(WATCH_CALLS, []))
        if not up and not coming:
            call = WatchCall(crew, watch, when)
            call.note_at = len(getattr(ship, "notes", []))  # its line goes before the work's
            if not call.coming:
                call = None
    elif not any(bill.is_on_deck(crew, s, when) for s in men):
        raise OrderError(
            f"None of the {name} are on deck at this hour; send their watch, or call all hands."
        )
    return {"hands_from": selector}, call


def commit(ship: Ship, call: WatchCall | None) -> None:
    """The order stands: the watch keeps coming up, and the log says it was turned up."""
    if call is None:
        return
    ship.extra.setdefault(WATCH_CALLS, []).append(call)
    note = (
        "routine",
        "crew.watch_turned_up",
        f"Turned up the {call.watch.value} watch.",
        None,
        {"watch": call.watch.value, "coming": len(call.coming), "at_once": call.first},
    )
    notes = getattr(ship, "notes", None)
    if isinstance(notes, list):
        notes.insert(min(call.note_at, len(notes)), note)
    else:
        ship.note(*note)
