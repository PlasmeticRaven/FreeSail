"""The ship's company: sailors, their ratings, stations and watches (spec M3 §2.1, §2.2).

Ordinary hands are numbers only (proposal §12 item 6): a name, a rating, two skills, a
fatigue and a flag for fitness. Station holders (the posts) have an `outline` that stays
empty in milestone 3, so that milestone 4's station briefs have somewhere to live.

Who is on deck is the watch bill's question (`crew/bill.py`); this module holds the
people and the flags the bill reads. Nothing here draws randomness: the muster
(`crew/muster.py`) does that once, from the stream it is handed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Rating(Enum):
    LANDSMAN = "landsman"
    ORDINARY = "ordinary"
    ABLE = "able"
    PETTY_OFFICER = "petty officer"
    MARINE = "marine"
    IDLER = "idler"
    OFFICER = "officer"


class Station(Enum):
    """The parts of the ship. Values are the ship file's station names."""

    FORECASTLE = "forecastle"
    FORE_TOP = "fore_top"
    MAIN_TOP = "main_top"
    MIZZEN_TOP = "mizzen_top"
    AFTERGUARD = "afterguard"
    WAISTERS = "waisters"
    MARINES = "marines"
    IDLERS = "idlers"
    QUARTERDECK = "quarterdeck"


class Watch(Enum):
    STARBOARD = "starboard"
    LARBOARD = "larboard"
    NONE = "none"  # idlers and officers keep no watch


# The stations aloft on their own mast, in the order of the masts.
TOPS = (Station.FORE_TOP, Station.MAIN_TOP, Station.MIZZEN_TOP)

# The seamen's stations: the ones the ratings line of the ship file shares out.
SEAMAN_STATIONS = (
    Station.FORECASTLE,
    Station.FORE_TOP,
    Station.MAIN_TOP,
    Station.MIZZEN_TOP,
    Station.AFTERGUARD,
    Station.WAISTERS,
)

# The seamen's ratings, best first, as the ship file shares them.
SEAMAN_RATINGS = (Rating.ABLE, Rating.ORDINARY, Rating.LANDSMAN)

# The two watches, starboard first: the odd hand of a station goes to the starboard watch.
WATCHES = (Watch.STARBOARD, Watch.LARBOARD)

# Skill of a fresh sailor of each rating, (deck, aloft), spec M3 §2.1. The ordinary seaman
# at 0.6 is the reference for the crew factor (package 17 reads this table). Marines and
# idlers never go aloft. Officers give orders and do not haul; they are given the petty
# officers' numbers only so that nothing divides by nought if a later milestone sets them
# to work. Provisional: package 17 tunes against the compatibility rule (spec M3 §1).
RATING_SKILL: dict[Rating, tuple[float, float]] = {
    Rating.LANDSMAN: (0.35, 0.35),
    Rating.ORDINARY: (0.6, 0.6),
    Rating.ABLE: (0.8, 0.8),
    Rating.PETTY_OFFICER: (0.9, 0.9),
    Rating.MARINE: (0.4, 0.0),
    Rating.IDLER: (0.3, 0.0),
    Rating.OFFICER: (0.9, 0.9),
}

# Mean fatigue in words for the muster (spec M3 §5.1): below the first bound "fresh", below
# the second "tired", else "worn out". Judgement: truth 20's watch at about 0.3 reads tired.
FATIGUE_FRESH_BELOW = 0.2
FATIGUE_TIRED_BELOW = 0.5

# How the muster names each station, singular and plural.
STATION_NAMES: dict[Station, tuple[str, str]] = {
    Station.FORECASTLE: ("forecastleman", "forecastlemen"),
    Station.FORE_TOP: ("fore topman", "fore topmen"),
    Station.MAIN_TOP: ("main topman", "main topmen"),
    Station.MIZZEN_TOP: ("mizzen topman", "mizzen topmen"),
    Station.AFTERGUARD: ("afterguard", "afterguard"),
    Station.WAISTERS: ("waister", "waisters"),
    Station.MARINES: ("marine", "marines"),
    Station.IDLERS: ("idler", "idlers"),
    Station.QUARTERDECK: ("officer", "officers"),
}

# Ratings as a muster book counts them: (singular, plural).
RATING_NAMES: dict[Rating, tuple[str, str]] = {
    Rating.ABLE: ("able", "able"),
    Rating.ORDINARY: ("ordinary", "ordinary"),
    Rating.LANDSMAN: ("landsman", "landsmen"),
    Rating.PETTY_OFFICER: ("petty officer", "petty officers"),
    Rating.MARINE: ("marine", "marines"),
    Rating.IDLER: ("idler", "idlers"),
    Rating.OFFICER: ("officer", "officers"),
}

# Numbers in words, as a clerk writes them in the log (above this, figures).
_NUMBER_WORDS = (
    "no",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "eleven",
    "twelve",
)


@dataclass
class Sailor:
    id: str  # "s017", stable for the voyage
    name: str  # "Wm. Hoskins"
    rating: Rating
    station: Station
    watch: Watch
    skill_aloft: float  # 0..1: work on the yards and in the tops
    skill_deck: float  # 0..1: hauling, the capstan, the braces
    fatigue: float = 0.0  # 0..1: 0 fresh, 1 done in
    fit: bool = True  # False when sick or hurt; not built beyond the flag in milestone 3
    post: str | None = None  # a station holder's post: "captain", "master", "boatswain"...
    trade: str | None = None  # an idler's trade: "cook", "carpenter's crew"...; None for seamen
    at: str | None = None  # the evolution instance holding this sailor, else None
    outline: str = ""  # a station holder's character outline: empty in milestone 3
    # Called on deck out of his watch: by a call for his watch or for all hands while the
    # hands come up (the routine, package 18, sets and clears it). The bill reads it.
    turned_up: bool = False


def fatigue_words(fatigue: float) -> str:
    if fatigue < FATIGUE_FRESH_BELOW:
        return "fresh"
    if fatigue < FATIGUE_TIRED_BELOW:
        return "tired"
    return "worn out"


def number_words(n: int) -> str:
    return _NUMBER_WORDS[n] if 0 <= n < len(_NUMBER_WORDS) else str(n)


def _plural(n: int, pair: tuple[str, str]) -> str:
    return f"{number_words(n)} {pair[0] if n == 1 else pair[1]}"


@dataclass
class Crew:
    """A mustered company. `sailors` is in id order; the indexes are built from it.

    The flags are the routine's (package 18) to set; the bill (`crew/bill.py`) reads them:

    - `all_hands_called`: everyone fit is on deck, and watch changes send nobody below.
    - `all_hands_called_by_order`: the captain called all hands himself, so the runner does
      not pipe down when its all-hands evolution ends (spec M3 §3.2).
    - `watch_on_deck`: the watch that has the deck when it is not the one the clock names
      (after `relieve the watch`, or a pipe-down that left the other watch up); None means
      the clock's watch.
    """

    ship_name: str
    sailors: list[Sailor]
    all_hands_called: bool = False
    all_hands_called_by_order: bool = False
    watch_on_deck: Watch | None = None
    by_station: dict[Station, list[Sailor]] = field(init=False, repr=False)
    by_watch: dict[Watch, list[Sailor]] = field(init=False, repr=False)
    by_id: dict[str, Sailor] = field(init=False, repr=False)
    posts: dict[str, Sailor] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.reindex()

    def reindex(self) -> None:
        """Rebuild the indexes from `sailors` (call after changing a station or watch)."""
        self.sailors.sort(key=lambda s: s.id)
        self.by_station = {st: [] for st in Station}
        self.by_watch = {w: [] for w in Watch}
        self.by_id = {}
        self.posts = {}
        for s in self.sailors:
            self.by_station[s.station].append(s)
            self.by_watch[s.watch].append(s)
            self.by_id[s.id] = s
            if s.post:
                self.posts[s.post] = s

    @property
    def complement(self) -> int:
        return len(self.sailors)

    def on_deck(self, clock: Any) -> list[Sailor]:
        """The hands on deck at this clock (or datetime), in id order. See `crew/bill.py`."""
        from freesail.crew import bill

        return bill.on_deck(self, clock)

    def describe(self, clock: Any) -> list[str]:
        """The muster (spec M3 §5.1): the watch bill, station by station, and the posts."""
        from freesail.crew import bill

        when = bill.when_of(clock)
        deck = {s.id for s in bill.on_deck(self, when)}
        watch = bill.watch_on_deck(self, when)
        officers = self.by_station[Station.QUARTERDECK]
        seamen = [s for s in self.sailors if s.station in SEAMAN_STATIONS]
        marines = self.by_station[Station.MARINES]
        idlers = self.by_station[Station.IDLERS]

        parts = [_plural(len(officers), ("officer", "officers"))]
        parts.append(_plural(len(seamen), ("seaman", "seamen")))
        if marines:
            parts.append(_plural(len(marines), ("marine", "marines")))
        if idlers:
            parts.append(_plural(len(idlers), ("idler", "idlers")))
        company = f"the {self.ship_name}'s company" if self.ship_name else "the ship's company"
        listed = ", ".join(parts[:-1]) + f" and {parts[-1]}" if len(parts) > 1 else parts[0]
        lines = [f"Mustered {company}, {self.complement} souls: {listed}."]
        if self.all_hands_called:
            state = "All hands are called"
        else:
            state = f"The {watch.value} watch has the deck"
            if idlers:
                state += ", the idlers " + ("up" if bill.idlers_up(when) else "below")
        lines.append(f"{state}: {len(deck)} hands on deck.")

        for station in Station:
            if station is Station.QUARTERDECK:
                continue
            men = self.by_station[station]
            if not men:
                continue
            lines.append(self._station_line(station, men, deck))

        ratings = SEAMAN_RATINGS
        counts = [sum(1 for s in seamen if s.rating is r) for r in ratings]
        if seamen:
            lines.append(
                "Seamen by rating: "
                + ", ".join(
                    f"{n} {RATING_NAMES[r][0 if n == 1 else 1]}"
                    for r, n in zip(ratings, counts, strict=True)
                )
                + "."
            )
        if idlers:
            trades: dict[str, int] = {}
            for s in idlers:
                trades[s.trade or "idler"] = trades.get(s.trade or "idler", 0) + 1
            lines.append(
                "Idlers by trade: " + ", ".join(f"{t} {n}" for t, n in trades.items()) + "."
            )
        for s in officers:
            lines.append(_post_line(s))
        room = getattr(self, "sail_room", None)  # spec 3b §6.3: given by parts.sail_room(ship)
        if room is not None:
            lines.append(room.muster_line())
        return lines

    def _station_line(self, station: Station, men: list[Sailor], deck: set[str]) -> str:
        n = len(men)
        name = STATION_NAMES[station][0 if n == 1 else 1]
        name = name[0].upper() + name[1:]
        head = f"{name}, {n}"
        if station in SEAMAN_STATIONS:
            mix = [(r, sum(1 for s in men if s.rating is r)) for r in SEAMAN_RATINGS]
            head += (
                " ("
                + ", ".join(f"{c} {RATING_NAMES[r][0 if c == 1 else 1]}" for r, c in mix if c)
                + ")"
            )
        on = sum(1 for s in men if s.id in deck)
        work = sum(1 for s in men if s.at is not None)
        below = n - on
        fatigue = sum(s.fatigue for s in men) / n
        return (
            f"{head}: {_figure(on)} on deck, {_figure(below)} below, "
            f"{_figure(work)} at work; {fatigue_words(fatigue)}."
        )


def _figure(n: int) -> str:
    return "none" if n == 0 else str(n)


def _post_line(s: Sailor) -> str:
    if s.post == "captain":
        return f"Captain {s.name}."
    return f"Mr. {s.name}, {s.post}."
