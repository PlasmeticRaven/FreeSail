"""The watch bill: which watch has the deck, and who is on deck, at a given time.

Pure functions of the time and the crew's flags (spec M3 §2.2, §4.1). Nothing here
changes the crew; the routine (package 18) sets the flags and calls these.

The watches alternate through the day's seven watches, the dog watches included, so that
a watch that had the middle watch last night has the first watch tonight. Which watch
has which is fixed by the calendar: counting watches from the first day of the Christian
era, the starboard watch has the even-numbered ones. On the default scenario's first day
(1 June 1805) that gives the starboard watch the morning watch.

On deck at any moment (spec M3 §2.2):

- nobody of the quarterdeck: the officers give orders and are not in the hands' pool;
- no one unfit;
- every hand at work (`at` set): he is not relieved mid-evolution (spec M3 §4.1);
- everyone, when all hands are called;
- a hand turned up out of his watch (`turned_up`, set by the routine);
- the idlers between IDLERS_UP_HOUR and IDLERS_BELOW_HOUR;
- the watch on deck.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from freesail import units
from freesail.crew.model import WATCHES, Crew, Sailor, Station, Watch

# The idlers come up at the start of the morning watch's second half ("idlers, lay up
# rigging and sweep clean", Luce's routine) and go below after the second dog watch
# (spec M3 §4.1). Hours of ship's time.
IDLERS_UP_HOUR = 6
IDLERS_BELOW_HOUR = 20

_WATCH_INDEX = {name: i for i, (_, _, name) in enumerate(units.WATCHES)}
WATCHES_PER_DAY = len(units.WATCHES)  # seven: the dog watches make the rotation


def when_of(clock: Any) -> datetime:
    """A datetime from a Clock (its ship's time) or a datetime."""
    if isinstance(clock, datetime):
        return clock
    return clock.ship_time


def watch_on_duty(clock: Any) -> Watch:
    """The watch whose turn it is by the clock."""
    when = when_of(clock)
    _, name = units.watch_of(when)
    n = when.date().toordinal() * WATCHES_PER_DAY + _WATCH_INDEX[name]
    return WATCHES[n % 2]


def watch_below(watch: Watch) -> Watch:
    """The other watch."""
    return Watch.LARBOARD if watch is Watch.STARBOARD else Watch.STARBOARD


def watch_on_deck(crew: Crew, clock: Any) -> Watch:
    """The watch that has the deck: the routine's if it has set one, else the clock's."""
    return crew.watch_on_deck or watch_on_duty(clock)


def idlers_up(clock: Any) -> bool:
    """Whether the idlers are on deck: by day, from six until the dog watches are out."""
    return IDLERS_UP_HOUR <= when_of(clock).hour < IDLERS_BELOW_HOUR


def _on_deck(crew: Crew, s: Sailor, watch: Watch, up: bool) -> bool:
    if s.station is Station.QUARTERDECK or not s.fit:
        return False
    if s.at is not None or crew.all_hands_called or s.turned_up:
        return True
    if s.station is Station.IDLERS:
        return up
    return s.watch is watch


def is_on_deck(crew: Crew, sailor: Sailor, clock: Any) -> bool:
    when = when_of(clock)
    return _on_deck(crew, sailor, watch_on_deck(crew, when), idlers_up(when))


def on_deck(crew: Crew, clock: Any) -> list[Sailor]:
    """The hands on deck, in id order."""
    when = when_of(clock)
    watch = watch_on_deck(crew, when)
    up = idlers_up(when)
    return [s for s in crew.sailors if _on_deck(crew, s, watch, up)]


def below(crew: Crew, clock: Any) -> list[Sailor]:
    """The hands below (the quarterdeck is neither), in id order."""
    deck = {s.id for s in on_deck(crew, clock)}
    return [s for s in crew.sailors if s.station is not Station.QUARTERDECK and s.id not in deck]
