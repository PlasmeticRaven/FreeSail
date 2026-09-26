"""Hands: the pool of sailors an evolution draws on, and the crew factor (spec M3 §3).

Every evolution file carries a ``crew:`` line, and here it becomes a request::

    crew: {hands: 12, rating: ordinary, stations: [topmen, afterguard]}
    crew: {hands: all, rating: ordinary, stations: [all hands]}

`CrewRequest.from_mapping` reads it. `request` fills it from the hands that are on deck,
fit and idle, marks the sailors taken with the instance that holds them (`Sailor.at`), and
says how it went: enough, short but workable, or too few to begin (spec §3.2). `release`
gives them back. `crew_factor` says how much longer the work takes with the hands actually
assigned (spec §3.3); the runner multiplies it into every step's time and passes it to the
scripts with the weather factor.

The order hands are taken in (spec §3.1, with the judgement noted at `_tier`):

1. the rating wanted, from the preferred stations in the order the file gives them;
2. the rating wanted, from any other station;
3. a better rating, preferred stations first;
4. a lesser rating, preferred stations first.

Within a tier the preferred stations go in the file's order (``topmen`` is the subject's
own top, then the other tops, fore to mizzen), the rest in the order of the watch bill,
then the nearer rating, then the sailor's number on the books. Nothing here is random.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

from freesail.crew.model import RATING_SKILL, TOPS, Crew, Rating, Sailor, Station

# The crew factor (spec M3 §3.3). A hand done in (fatigue 1) works half again as slowly;
# soft, per the owner, and tuned from here.
FATIGUE_WEIGHT = 0.5
# Below this a hand is fresh and works at the file's pace: the watch on deck gathers a
# hundredth of fatigue an hour merely standing there, and without a dead band that would
# lengthen every job by a tick within the hour (the compatibility rule, spec M3 §1).
FATIGUE_FRESH = 0.05

# A hand whose table skill for the work is nought is never assigned to it (marines and
# idlers aloft); should one be, his skill is read as this, so that nothing divides by nought.
SKILL_FLOOR = 0.1

# Short-handed (spec M3 §3.2): with fewer than this share of the hands wanted the work
# does not begin; with this share or more it begins, slower in proportion.
SHORT_HANDED_SHARE = 0.5

# What the file may say.
ALL = "all"  # hands: all
TOPMEN = "topmen"  # the topmen of the subject's mast, then the other tops
ALL_HANDS = "all hands"  # everyone fit
DEFAULT_RATING = Rating.ORDINARY

# The top each mast's topmen work in; a mast not listed (the bowsprit) has none.
TOP_OF_MAST: dict[str, Station] = {
    "fore": Station.FORE_TOP,
    "main": Station.MAIN_TOP,
    "mizzen": Station.MIZZEN_TOP,
}

# Stations that are never in the hands' pool: the officers give orders and do not haul.
_NOT_HANDS = (Station.QUARTERDECK,)

# How a request came out (spec M3 §3.2).
ENOUGH = "enough"
SHORT = "short"
TOO_FEW = "too few"


class CrewRequestError(ValueError):
    """An evolution file's crew line that cannot be read. The message is a sentence."""


@dataclass(frozen=True)
class CrewRequest:
    """What an evolution asks for: so many hands (or all), of a rating, from stations."""

    hands: int | None = 0  # None: all hands
    rating: Rating = DEFAULT_RATING
    stations: tuple[str, ...] = ()

    @property
    def all_hands(self) -> bool:
        return self.hands is None

    @property
    def wants_none(self) -> bool:
        return self.hands == 0

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, Any] | None) -> CrewRequest:
        """Read an evolution file's ``crew:`` mapping. Missing, or ``{hands: 0}``: no hands."""
        if not mapping:
            return cls()
        if not isinstance(mapping, Mapping):
            raise CrewRequestError("The crew line must be a mapping of hands, rating and stations.")
        raw_hands = mapping.get("hands", 0)
        hands: int | None
        if isinstance(raw_hands, str) and raw_hands.strip().lower() == ALL:
            hands = None
        elif isinstance(raw_hands, int) and not isinstance(raw_hands, bool) and raw_hands >= 0:
            hands = raw_hands
        else:
            raise CrewRequestError(
                f"The crew line asks for {raw_hands!r} hands; say a number or 'all'."
            )
        raw_rating = str(mapping.get("rating") or DEFAULT_RATING.value)
        rating = _rating_named(raw_rating)
        raw_stations = mapping.get("stations") or []
        if isinstance(raw_stations, str):
            raw_stations = [raw_stations]
        stations = tuple(_station_word(str(s)) for s in raw_stations)
        return cls(hands=hands, rating=rating, stations=stations)


def _rating_named(name: str) -> Rating:
    word = name.strip().lower().replace("_", " ")
    for r in Rating:
        if r.value == word or r.name.lower().replace("_", " ") == word:
            return r
    options = ", ".join(r.value for r in Rating)
    raise CrewRequestError(f"There is no rating called '{name}'; say one of: {options}.")


def _station_word(name: str) -> str:
    word = name.strip().lower()
    if word in (TOPMEN, ALL_HANDS):
        return word
    word = word.replace(" ", "_")
    if any(st.value == word for st in Station):
        return word
    options = ", ".join([TOPMEN, ALL_HANDS, *(st.value for st in Station)])
    raise CrewRequestError(f"There is no station called '{name}'; say one of: {options}.")


def preferred_stations(want: CrewRequest, subject_mast: str | None) -> list[Station]:
    """The stations a request names, in order of preference, resolved for the subject."""
    out: list[Station] = []

    def add(st: Station) -> None:
        if st not in out and st not in _NOT_HANDS:
            out.append(st)

    for word in want.stations:
        if word == TOPMEN:
            own = TOP_OF_MAST.get(subject_mast or "")
            if own is not None:
                add(own)
            for top in TOPS:
                add(top)
        elif word == ALL_HANDS:
            for st in Station:
                add(st)
        else:
            add(Station(word))
    return out


def rating_skill(rating: Rating, aloft: bool) -> float:
    """A fresh sailor's skill for the work by his rating (`model.RATING_SKILL`)."""
    deck, up = RATING_SKILL[rating]
    return up if aloft else deck


def can_work(sailor: Sailor, aloft: bool) -> bool:
    """Whether a sailor can be put to this work at all: fit, not an officer, and, aloft,
    of a rating that goes aloft (never a marine or an idler)."""
    if not sailor.fit or sailor.station in _NOT_HANDS:
        return False
    return rating_skill(sailor.rating, aloft) > 0.0 if aloft else True


def company_can_give(crew: Crew, aloft: bool) -> int:
    """How many hands the whole ship's company could ever put to this work."""
    return sum(1 for s in crew.sailors if can_work(s, aloft))


@dataclass
class Assignment:
    """The hands an instance holds and how the request came out."""

    inst_id: str
    wanted: int  # hands wanted, after clamping to the company; for all hands, those taken
    hands: list[Sailor] = field(default_factory=list)
    outcome: str = ENOUGH  # ENOUGH, SHORT or TOO_FEW
    available: int = 0  # idle hands on deck that could have been taken, when TOO_FEW
    all_hands: bool = False

    @property
    def got(self) -> int:
        return len(self.hands)


def _tier(sailor: Sailor, preferred: list[Station], want_skill: float, aloft: bool) -> tuple:
    """The sort key that fills a request (see the module docstring).

    Judgement against spec §3.1, which reads "preferred stations by rating wanted, then
    higher ratings, then other stations, then lower ratings": the rating wanted is taken
    from any station before a better rating is taken from a preferred one. Taken literally
    the spec would put the forecastle's able seamen on the jib before the ordinary seamen
    the file asks for, the work would go a quarter faster, and the compatibility rule
    (spec §1: one evolution at a time with the watch on deck reproduces milestone 2 to the
    tick) could not hold for the jib.
    """
    skill = rating_skill(sailor.rating, aloft)
    in_pref = sailor.station in preferred
    if skill == want_skill:
        tier = 0 if in_pref else 1
    elif skill > want_skill:
        tier = 2 if in_pref else 3
    else:
        tier = 4 if in_pref else 5
    station_rank = preferred.index(sailor.station) if in_pref else len(preferred)
    return (
        tier,
        station_rank,
        list(Station).index(sailor.station),
        abs(skill - want_skill),
        sailor.id,
    )


def request(
    crew: Crew,
    on_deck: Iterable[Sailor],
    inst_id: str,
    want: CrewRequest,
    subject_mast: str | None,
    aloft: bool = False,
) -> Assignment:
    """Fill a request from the hands on deck, fit and idle (spec M3 §3.1, §3.2).

    `aloft` is true when any of the evolution's steps is aloft: then only hands who go
    aloft can be taken. Enough or short but workable: the hands taken are marked
    ``at = inst_id``. Too few: nobody is taken, and the assignment says how many there were.
    """
    idle = [s for s in on_deck if s.at is None and can_work(s, aloft)]
    if want.all_hands:
        for s in idle:
            s.at = inst_id
        outcome = ENOUGH if idle else TOO_FEW
        return Assignment(inst_id, len(idle), list(idle), outcome, len(idle), all_hands=True)
    wanted = min(int(want.hands or 0), company_can_give(crew, aloft))
    if wanted <= 0:
        return Assignment(inst_id, 0)
    preferred = preferred_stations(want, subject_mast)
    want_skill = rating_skill(want.rating, aloft)
    ranked = sorted(idle, key=lambda s: _tier(s, preferred, want_skill, aloft))
    taken = ranked[:wanted]
    if len(taken) < wanted * SHORT_HANDED_SHARE:
        return Assignment(inst_id, wanted, [], TOO_FEW, len(taken))
    for s in taken:
        s.at = inst_id
    outcome = ENOUGH if len(taken) >= wanted else SHORT
    return Assignment(inst_id, wanted, taken, outcome, len(taken))


def top_up(assignment: Assignment, on_deck: Iterable[Sailor], aloft: bool = False) -> int:
    """An all-hands assignment takes every hand who has come on deck since (the watch
    below comes up over a minute and a half, spec M3 §4.2). Returns how many joined."""
    if not assignment.all_hands:
        return 0
    joined = [s for s in on_deck if s.at is None and can_work(s, aloft)]
    for s in joined:
        s.at = assignment.inst_id
    assignment.hands.extend(joined)
    assignment.hands.sort(key=lambda s: s.id)
    assignment.wanted = len(assignment.hands)
    if assignment.hands:
        assignment.outcome = ENOUGH
    return len(joined)


def release(crew: Crew, inst_id: str) -> list[Sailor]:
    """Give back every hand an instance holds. Returns them, in id order."""
    freed = [s for s in crew.sailors if s.at == inst_id]
    for s in freed:
        s.at = None
    return freed


def crew_factor(assignment: Assignment, want: CrewRequest, aloft: bool) -> float:
    """How much longer the work takes with these hands (spec M3 §3.3)::

        numbers  = max(1, wanted / got)             # never faster for extra hands
        skill    = mean of reference_skill(rating wanted) / reference_skill(hand's rating)
        fatigue  = 1 + FATIGUE_WEIGHT * max(0, mean fatigue - FATIGUE_FRESH)
        factor   = numbers * skill * fatigue

    The skill term reads each hand's rating through `RATING_SKILL`, not his own skill with
    its seeded spread, so a request filled at its own rating gives exactly 1.0 (spec §3.3).

    An all-hands evolution (``hands: all``) takes the ship's company as it is: its file's
    durations are the whole company's pace, so its numbers and skill terms are 1.0 and only
    fatigue slows it (judgement; the spec's mean over a company of marines, idlers and
    landsmen against the ordinary seaman would make every tack half again as long).
    """
    hands = assignment.hands
    if not hands:
        return 1.0
    mean_fatigue = sum(s.fatigue for s in hands) / len(hands)
    fatigue = 1.0 + FATIGUE_WEIGHT * max(0.0, mean_fatigue - FATIGUE_FRESH)
    if want.all_hands or assignment.all_hands:
        return fatigue
    numbers = max(1.0, assignment.wanted / len(hands))
    reference = rating_skill(want.rating, aloft)
    if reference <= 0.0:
        reference = SKILL_FLOOR
    ratios = [reference / max(rating_skill(s.rating, aloft), SKILL_FLOOR) for s in hands]
    skill = sum(ratios) / len(ratios)
    return numbers * skill * fatigue
