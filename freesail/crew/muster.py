"""Muster a ship's company from the ship file's `crew:` section (spec M3 §2.3).

`muster(spec, stream)` is the only place in `crew/` that draws randomness, and it draws
only from the stream it is handed (the World's "muster" stream): names from
`data/crew/names.yaml` and the small spread of skills about each rating's figure. The same
stream state gives the same crew, to the letter.

How the company is made up, all of it deterministic:

1. The posts come first on the books (s001 onwards): the quarterdeck, rating officer,
   keeping no watch here.
2. The seamen are counted by rating from the file's shares (largest remainder, the better
   rating taking a tie), then shared among the stations in FILL_ORDER: the topmen from the
   able and ordinary seamen first, in proportion to what is left of each, so that the
   three tops are alike; the forecastle from the able; the waisters from the landsmen; the
   afterguard from what is left (spec M3 §2.3; Luce 1884 ch. XX).
3. Each station is entered on the books best rating first, and its hands are watched
   alternately starboard and larboard, so that each watch has an equal share of its
   strength (Luce: "giving to each watch an equal share of the strength and intelligence of
   the crew"); an odd hand goes to the starboard watch.
4. The marines are watched the same way; the idlers are entered by trade in the file's
   order and keep no watch.
"""

from __future__ import annotations

import functools
import random
from fractions import Fraction
from pathlib import Path

import yaml

from freesail.crew.model import (
    RATING_SKILL,
    SEAMAN_RATINGS,
    WATCHES,
    Crew,
    Rating,
    Sailor,
    Station,
    Watch,
)
from freesail.ship.schema import CrewSpec, ShipFileError

NAMES_PATH = Path(__file__).resolve().parents[2] / "data" / "crew" / "names.yaml"

# Skills are the rating's figure (model.RATING_SKILL) plus a seeded spread of this much
# either way (spec M3 §2.1), clamped to 0..1 and kept to this many decimals. A skill of
# nought stays nought: a marine or an idler is never given any skill aloft.
SKILL_SPREAD = 0.05
SKILL_DECIMALS = 3

# A name already on the books is drawn again, up to this many times, so that two hands
# seldom share one; after that a second John Smith is entered, as muster books show.
NAME_REDRAWS = 12

# The order the seamen's stations are filled, and each one's preference: tiers of ratings,
# the ratings within a tier drawn together in proportion to what remains of each.
_TOPMEN_TIERS = ((Rating.ABLE, Rating.ORDINARY), (Rating.LANDSMAN,))
FILL_ORDER: tuple[tuple[Station, tuple[tuple[Rating, ...], ...]], ...] = (
    (Station.FORE_TOP, _TOPMEN_TIERS),
    (Station.MAIN_TOP, _TOPMEN_TIERS),
    (Station.MIZZEN_TOP, _TOPMEN_TIERS),
    (Station.FORECASTLE, ((Rating.ABLE,), (Rating.ORDINARY,), (Rating.LANDSMAN,))),
    (Station.WAISTERS, ((Rating.LANDSMAN,), (Rating.ORDINARY,), (Rating.ABLE,))),
    (Station.AFTERGUARD, ((Rating.ABLE, Rating.ORDINARY, Rating.LANDSMAN),)),
)

# A muster book's abbreviations of the common given names.
GIVEN_ABBREVIATIONS = {
    "Abraham": "Abm.",
    "Alexander": "Alexr.",
    "Andrew": "Andw.",
    "Archibald": "Archd.",
    "Bartholomew": "Barthw.",
    "Benjamin": "Benjn.",
    "Charles": "Chas.",
    "Christopher": "Christr.",
    "Daniel": "Danl.",
    "Ebenezer": "Ebenr.",
    "Edward": "Edwd.",
    "Frederick": "Fredk.",
    "George": "Geo.",
    "Hezekiah": "Hezh.",
    "James": "Jas.",
    "Jeremiah": "Jerh.",
    "John": "Jno.",
    "Jonathan": "Jona.",
    "Joseph": "Jos.",
    "Matthew": "Matthw.",
    "Nathaniel": "Nathl.",
    "Nicholas": "Nichs.",
    "Richard": "Richd.",
    "Robert": "Robt.",
    "Samuel": "Saml.",
    "Thomas": "Thos.",
    "William": "Wm.",
    "Zachariah": "Zachh.",
}


@functools.lru_cache(maxsize=4)
def _name_lists(path: str) -> dict[str, tuple[tuple[str, ...], tuple[str, ...]]]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {
        str(k): (tuple(str(x) for x in v["given"]), tuple(str(x) for x in v["surnames"]))
        for k, v in data.items()
    }


def name_lists(path: str | Path = NAMES_PATH) -> dict[str, tuple[tuple[str, ...], ...]]:
    """The name lists: {list: (given names, surnames)}."""
    return _name_lists(str(path))


def abbreviate(given: str) -> str:
    return GIVEN_ABBREVIATIONS.get(given, given)


def apportion(n: int, weights: list[Fraction]) -> list[int]:
    """Share n among weights by largest remainder; a tie goes to the earlier weight."""
    total = sum(weights, Fraction(0))
    if n <= 0 or total <= 0:
        return [0] * len(weights)
    exact = [n * w / total for w in weights]
    base = [int(x) for x in exact]
    order = sorted(range(len(weights)), key=lambda i: (-(exact[i] - base[i]), i))
    for i in order[: n - sum(base)]:
        base[i] += 1
    return base


def rating_counts(spec: CrewSpec) -> dict[Rating, int]:
    """How many seamen of each rating the file's shares give."""
    shares = [Fraction(str(spec.ratings.get(r.value, 0.0))) for r in SEAMAN_RATINGS]
    return dict(zip(SEAMAN_RATINGS, apportion(spec.seamen, shares), strict=True))


def station_ratings(spec: CrewSpec) -> dict[Station, dict[Rating, int]]:
    """Each seaman station's hands by rating, filled in FILL_ORDER."""
    left = rating_counts(spec)
    out: dict[Station, dict[Rating, int]] = {}
    for station, tiers in FILL_ORDER:
        need = spec.stations[station.value]
        got = {r: 0 for r in SEAMAN_RATINGS}
        for tier in tiers:
            if need <= 0:
                break
            avail = [left[r] for r in tier]
            take = apportion(min(need, sum(avail)), [Fraction(a) for a in avail])
            for r, t in zip(tier, take, strict=True):
                got[r] += t
                left[r] -= t
                need -= t
        out[station] = got
    return out


def muster(
    spec: CrewSpec,
    stream: random.Random,
    ship_name: str = "",
    names_path: str | Path = NAMES_PATH,
) -> Crew:
    """The ship's company from its crew section, drawing names and skills from `stream`."""
    lists = name_lists(names_path)
    if spec.names not in lists:
        raise ShipFileError(
            f"The ship's crew is to be drawn from the '{spec.names}' names, but "
            f"{Path(names_path).name} has only {' and '.join(sorted(lists))}."
        )
    given, surnames = lists[spec.names]

    # (rating, station, watch, post, trade, name) in the order of the books
    entries: list[tuple[Rating, Station, Watch, str | None, str | None, str | None]] = []
    for p in spec.posts:
        entries.append((Rating.OFFICER, Station.QUARTERDECK, Watch.NONE, p.post, None, p.name))
    by_rating = station_ratings(spec)
    for station in Station:
        n = spec.stations.get(station.value, 0) if station is not Station.QUARTERDECK else 0
        if n == 0:
            continue
        if station is Station.IDLERS:
            for trade, count in spec.idlers_by_trade.items():
                for _ in range(count):
                    entries.append((Rating.IDLER, station, Watch.NONE, None, trade, None))
            continue
        if station is Station.MARINES:
            ratings = [Rating.MARINE] * n
        else:
            ratings = [r for r in SEAMAN_RATINGS for _ in range(by_rating[station][r])]
        for i, rating in enumerate(ratings):
            entries.append((rating, station, WATCHES[i % 2], None, None, None))

    used: set[str] = {e[5] for e in entries if e[5]}
    sailors: list[Sailor] = []
    width = max(3, len(str(len(entries))))
    for i, (rating, station, watch, post, trade, name) in enumerate(entries):
        if name is None:
            name = _draw_name(stream, given, surnames, used)
        used.add(name)
        deck, aloft = RATING_SKILL[rating]
        deck = _spread(deck, stream.uniform(-SKILL_SPREAD, SKILL_SPREAD))
        aloft = _spread(aloft, stream.uniform(-SKILL_SPREAD, SKILL_SPREAD))
        sailors.append(
            Sailor(
                id=f"s{i + 1:0{width}d}",
                name=name,
                rating=rating,
                station=station,
                watch=watch,
                skill_aloft=aloft,
                skill_deck=deck,
                post=post,
                trade=trade,
            )
        )
    return Crew(ship_name=ship_name, sailors=sailors)


def _draw_name(
    stream: random.Random, given: tuple[str, ...], surnames: tuple[str, ...], used: set[str]
) -> str:
    name = ""
    for _ in range(NAME_REDRAWS):
        name = f"{abbreviate(stream.choice(given))} {stream.choice(surnames)}"
        if name not in used:
            break
    return name


def _spread(base: float, delta: float) -> float:
    if base <= 0.0:
        return 0.0
    return round(min(1.0, max(0.0, base + delta)), SKILL_DECIMALS)
