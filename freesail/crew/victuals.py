"""The ration and the stores' fall (spec M7b §19; package 54).

The company eat and drink at the meals the watch bill keeps (`data/crew/ration.yaml`:
breakfast, dinner and supper), and at each the ship's provisions and water fall by the
meal's share of the day's ration for the company mustered: the provisions by days at full
allowance (the stores count them so, `places.Stores`), the water by the gallons a man a day
the ship file gives (`crew.ration.water_gallons`) turned to tons of the ground tier. Short
allowance (the captain's order, the Regulations' Art. III) serves the table's share of the
whole, every man alike; the fall is the smaller and the days the longer, and the hands work
the harder for it.

**A reading and not a line.** The fall writes nothing in the log: it is the purser's
reading (`the stores`, the purser's books) that says what remains and for how long. The
log hears of the stores only when they run out (the last of the provisions served out, the
last of the water started), and of short allowance by the captain's order, with a line on
the people's temper.

**The hands.** What the company is served bears on the crew's fatigue
(`crew.routine.Routine.hardship`, the crew factor's input): short allowance a half, nothing
to serve the whole, the water found foul (package 50's `aboard:`) a quarter more, drunk at
a cost in the grog and the coppers. Nought, as it always is at whole allowance with sweet
water, leaves the routine as it was.

A ship whose file keeps neither water nor provisions is not victualled, and nothing here
touches her.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from freesail.core.events import Severity

__all__ = [
    "FOUL_WATER_HARDSHIP",
    "RATION_PATH",
    "Ration",
    "day_words",
    "hardship",
    "load_ration",
    "set_allowance",
    "tick",
    "victualled",
    "water_days",
]

RATION_PATH = Path(__file__).resolve().parents[2] / "data" / "crew" / "ration.yaml"

# The water found foul, drunk in the grog and the coppers: a quarter of the crew factor's
# hardship (judgement; health is M7's).
FOUL_WATER_HARDSHIP = 0.25

DAYS = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")

Line = tuple[Severity, str, str, dict[str, Any]]


@dataclass(frozen=True)
class Ration:
    tables: dict[str, dict[str, Any]]
    words: dict[str, tuple[str, str]]
    meals: tuple[tuple[int, str], ...]
    gallons_a_ton: float
    short_allowance: float


@functools.lru_cache(maxsize=4)
def load_ration(path: str | Path = RATION_PATH) -> Ration:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    meals = tuple((int(m["hour"]), str(m["name"])) for m in raw.get("meals") or ())
    if not meals:
        raise ValueError(f"{path}: the ration serves no meals.")
    return Ration(
        tables={str(k): dict(v) for k, v in (raw.get("tables") or {}).items()},
        words={str(k): (str(v[0]), str(v[1])) for k, v in (raw.get("words") or {}).items()},
        meals=meals,
        gallons_a_ton=float(raw.get("water_gallons_a_ton", 252)),
        short_allowance=float(raw.get("short_allowance", 0.5)),
    )


# -- what a ship is victualled by --------------------------------------------------------


def _crew(world: Any) -> Any:
    return (getattr(world.ship, "extra", None) or {}).get("crew")


def _crew_spec(world: Any) -> Any:
    return getattr(getattr(world.ship, "spec", None), "crew", None)


def victualled(world: Any) -> bool:
    """Whether the ship is victualled: a company mustered and stores in her file."""
    spec = _crew_spec(world)
    stores = getattr(spec, "stores", None)
    if _crew(world) is None or stores is None or getattr(world, "stores", None) is None:
        return False
    return float(stores.provisions_days or 0) > 0 or float(stores.water_tons or 0) > 0


def _ration_spec(world: Any) -> Any:
    from freesail.ship.schema import RationSpec

    return getattr(_crew_spec(world), "ration", None) or RationSpec()


def daily_water_tons(world: Any) -> float:
    """The water the company draws in a day at whole allowance, in tons."""
    crew = _crew(world)
    if crew is None:
        return 0.0
    gallons = float(_ration_spec(world).water_gallons) * crew.complement
    return gallons / load_ration().gallons_a_ton


def _days_basis(world: Any) -> float:
    """The company mustered over the complement the days are reckoned for (the file's):
    one, until hands are entered or lost."""
    crew, spec = _crew(world), _crew_spec(world)
    if crew is None or spec is None or not spec.complement:
        return 1.0
    return crew.complement / float(spec.complement)


def water_days(world: Any) -> float | None:
    """The days her water lasts at the allowance she is at; None where none is drawn."""
    stores = getattr(world, "stores", None)
    daily = daily_water_tons(world) * float(getattr(stores, "allowance", 1.0))
    if stores is None or daily <= 0:
        return None
    return stores.water_tons / daily


def provisions_days_left(world: Any) -> float | None:
    """The days her provisions last at the allowance she is at."""
    stores = getattr(world, "stores", None)
    if stores is None:
        return None
    rate = float(getattr(stores, "allowance", 1.0)) * _days_basis(world)
    return stores.provisions_days / rate if rate > 0 else None


def day_words(world: Any, when: datetime | None = None) -> str:
    """The day's proportion a man, from the ship's table: 'Tuesday: a pound of biscuit,
    a gallon of beer and two pounds of beef a man'."""
    ration = load_ration()
    table = ration.tables.get(str(_ration_spec(world).table)) or {}
    when = when or world.clock.ship_time
    day = DAYS[when.weekday()]
    issue = (table.get("days") or {}).get(day) or {}
    parts = []
    for key, qty in issue.items():
        one, many = ration.words.get(key, (key, key))
        parts.append(f"{_qty_words(float(qty))} {one if float(qty) <= 1 else many}")
    if not parts:
        return ""
    said = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]
    return f"{day.capitalize()}: {said} a man"


def _qty_words(q: float) -> str:
    if q == 0.5:
        return "half a"
    if q == 1:
        return "a"
    whole = {2: "two", 3: "three", 4: "four", 6: "six", 8: "eight", 12: "twelve"}
    return whole.get(int(q), f"{q:g}") if q == int(q) else f"{q:g}"


# -- the hands ---------------------------------------------------------------------------


def hardship(world: Any) -> float:
    """What the company's victualling costs the hands, 0 to 1 (the routine's
    `hardship`): short allowance its shortfall, nothing to serve the whole, the water
    found foul a quarter more."""
    stores = getattr(world, "stores", None)
    if stores is None or not victualled(world):
        return 0.0
    allowance = float(getattr(stores, "allowance", 1.0))
    h = 1.0 - allowance
    if stores.provisions_days <= 0 or stores.water_tons <= 0:
        h = 1.0
    elif getattr(stores, "foul", False):
        h += FOUL_WATER_HARDSHIP
    return min(1.0, max(0.0, h))


def _set_hardship(world: Any) -> None:
    routine = (getattr(world.ship, "extra", None) or {}).get("routine")
    if routine is not None:
        routine.hardship = hardship(world)


# -- the meal ----------------------------------------------------------------------------


def tick(world: Any) -> list[Line]:
    """Once a minute from the World: at a meal's hour the stores fall by its share, and
    the hands' hardship is set from what they are served. Returns the log's lines, which
    are none but a store run out."""
    if not victualled(world):
        return []
    _set_hardship(world)
    now = world.clock.ship_time
    if now.minute or now.second:
        return []
    meal = next((name for hour, name in load_ration().meals if hour == now.hour), None)
    if meal is None or world.clock.tick == 0:
        return []
    return serve(world, meal)


def serve(world: Any, meal: str) -> list[Line]:
    """A meal served: the provisions and the water fall by its share of the day's ration
    at the allowance she is at, never below nothing; the line when one runs out."""
    stores = world.stores
    share = 1.0 / len(load_ration().meals)
    allowance = float(getattr(stores, "allowance", 1.0))
    days = share * allowance * _days_basis(world)
    tons = share * allowance * daily_water_tons(world)
    lines: list[Line] = []
    had_provisions, had_water = stores.provisions_days > 0, stores.water_tons > 0
    take_days = min(days, max(0.0, stores.provisions_days))
    take_tons = min(tons, max(0.0, stores.water_tons))
    stores.provisions_days = max(0.0, stores.provisions_days - days)
    stores.water_tons = max(0.0, stores.water_tons - tons)
    stores.expended_days = float(getattr(stores, "expended_days", 0.0)) + take_days
    stores.expended_tons = float(getattr(stores, "expended_tons", 0.0)) + take_tons
    if had_provisions and stores.provisions_days <= 1e-9:
        stores.provisions_days = 0.0
        lines.append(
            (
                Severity.NOTABLE,
                "stores.out",
                f"The last of the provisions served out at {meal}: the bread room and the "
                "steward's room are empty.",
                {"store": "provisions", "meal": meal},
            )
        )
    if had_water and stores.water_tons <= 1e-9:
        stores.water_tons = 0.0
        lines.append(
            (
                Severity.NOTABLE,
                "stores.out",
                f"The last of the water started at {meal}: the ground tier is dry.",
                {"store": "water", "meal": meal},
            )
        )
    _set_hardship(world)
    return lines


# -- short allowance ---------------------------------------------------------------------


def set_allowance(world: Any, short: bool) -> tuple[str, dict[str, Any]]:
    """`short allowance` and `whole allowance`: the captain's order (the Regulations, Art.
    III), every man alike; the line says it and the people's temper. Refused in words
    where there is nothing to change."""
    from freesail.orders.errors import OrderError

    stores = getattr(world, "stores", None)
    if stores is None or not victualled(world):
        raise OrderError("She keeps no stores to put the people to an allowance of.")
    was = float(getattr(stores, "allowance", 1.0))
    want = load_ration().short_allowance if short else 1.0
    if abs(was - want) < 1e-9:
        raise OrderError(
            "The people are at short allowance already."
            if short
            else "The people are at whole allowance already."
        )
    stores.allowance = want
    _set_hardship(world)
    left = provisions_days_left(world)
    water = water_days(world)
    lasts = []
    if left is not None:
        lasts.append(f"the provisions for {left:.0f} days")
    if water is not None:
        lasts.append(f"the water for {water:.0f}")
    lasting = f" At this allowance {' and '.join(lasts)}." if lasts else ""
    if short:
        text = (
            f"The ship's company put to short allowance, {_share_words(want)} the whole, "
            "every man aboard alike and the officers with them; the purser keeps the "
            f"savings to be paid them. The people take it sullenly.{lasting}"
        )
    else:
        text = (
            f"The ship's company back to whole allowance; the people take it cheerfully.{lasting}"
        )
    return text, {"allowance": want, "was": was, "notable": True}


def _share_words(share: float) -> str:
    for value, words in ((0.5, "half"), (2 / 3, "two thirds"), (0.75, "three quarters")):
        if abs(share - value) < 1e-6:
            return words
    return f"{share:g} of"
