"""The stand-by's tripwires (package 58a; the cold review of 2026-10-22, §7.2: the lugger
officer's own proposal, "making the right orders at the wrong time").

A model sees samples and never the curve between them: every order "feels finished when
it returns", and an oversleeping stand-by is no gap from the inside. "Whatever guards
against it has to live in the instruments." So a stand-by may wait for the ship's own
state as well as for the log's events and the bells: `stand_by("her way settled")`,
`"depth under 8 fathoms"`, `"speed under 2 knots"`, `"speed over 6 knots"`, `"the wind
over 25 knots"`, `"a point of interest within 3 miles"`, alone or joined with "or" to the
events of before. Each is judged by the game's readings, never by prose:

- **her way settled**: her speed through the water steady within a quarter of a knot and
  her head within a quarter of a point for two minutes (`SETTLED_S`, `SETTLED_KN`,
  `SETTLED_DEG`), measured from the stand-by and begun again at every order given since
  (a helm or a sail order, the book's among them): the lugger officer trimmed before she
  had settled, and the owner's method was "steer, settle, trim";
- **depth under n fathoms**: the chart's depth at her position by account, or the lead's
  last cast, under the figure (the dialect's `the depth of water` and `the depth`);
- **speed under / over n knots**: the log's speed (the dialect's `the speed`);
- **the wind over n knots**: the true wind (the dialect's `the true wind`);
- **a point of interest within n miles**: a charted headland, island, mark, light,
  danger or anchorage, or a point of interest the world has put on the sea (`mark:`),
  within the miles of her position by account that was not within them when the stand-by
  began; the wake names it.

The dialect's own conditions are read as the book's `when` is (`standing.grammar.
parse_condition`); the two of the ship's own way (settled, and a point of interest) are
this module's, watched once a tick through the same `holds(view, memory)`.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

from freesail import units

__all__ = [
    "POINT_OF_INTEREST_KINDS",
    "SETTLED_DEG",
    "SETTLED_KN",
    "SETTLED_S",
    "TRIPWIRE_WORDS",
    "Tripwire",
    "tripwire_of",
]

# Her way settled: her speed steady within a quarter of a knot and her head within a
# quarter of a point for two minutes (the brief's figures; judgement: a frigate's way
# settles in about a minute after a trim, a minute or two after a turn).
SETTLED_S = 120
SETTLED_KN = 0.25
SETTLED_DEG = 11.25 / 4.0

# The chart's kinds that are a point of interest to a stand-by: the land's and the sea's
# named places, the marks and lights, and the dangers (never the bottom's kinds).
POINT_OF_INTEREST_KINDS = frozenset(
    {
        "headland",
        "island",
        "town",
        "anchorage",
        "light",
        "mark",
        "beacon",
        "tower",
        "castle",
        "church",
        "rock",
        "ledge",
        "drying",
        "shoal",
        "bank",
    }
)

# The tripwires' words as the stand-by tool and the briefs give them.
TRIPWIRE_WORDS = (
    "her way settled",
    "depth under <n> fathoms",
    "speed under <n> knots",
    "speed over <n> knots",
    "the wind over <n> knots",
    "a point of interest within <n> miles",
    "a sail within <n> cables",
)

_NUMBERS = {
    "a": 1.0,
    "an": 1.0,
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0,
    "six": 6.0,
    "seven": 7.0,
    "eight": 8.0,
    "nine": 9.0,
    "ten": 10.0,
    "eleven": 11.0,
    "twelve": 12.0,
    "fifteen": 15.0,
    "twenty": 20.0,
    "thirty": 30.0,
    "half a": 0.5,
}
_N = (
    r"(?P<n>\d+(?:\.\d+)?|half a|an?|one|two|three|four|five|six|seven|eight|nine|ten|eleven"
    r"|twelve|fifteen|twenty|thirty)"
)
_UNDER = r"(?:is\s+)?(?:under|below|less\s+than|shoaler\s+than|falls?\s+(?:under|below))"
_OVER = r"(?:is\s+)?(?:over|above|more\s+than|exceeds?|rises?\s+(?:over|above))"
_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "settled",
        re.compile(
            r"^(?:her\s+|the\s+)?way\s+(?:is\s+|has\s+)?settled$|^she\s+(?:has\s+)?settled$"
        ),
    ),
    (
        "depth",
        re.compile(rf"^(?:the\s+)?(?:depth|water)(?:\s+of\s+water)?\s+{_UNDER}\s+{_N}\s+fathoms?$"),
    ),
    ("speed_under", re.compile(rf"^(?:the\s+|her\s+)?speed\s+{_UNDER}\s+{_N}\s+knots?$")),
    ("speed_over", re.compile(rf"^(?:the\s+|her\s+)?speed\s+{_OVER}\s+{_N}\s+knots?$")),
    ("wind", re.compile(rf"^(?:the\s+)?(?:true\s+)?wind\s+{_OVER}\s+{_N}\s+knots?$")),
    (
        "point",
        re.compile(
            rf"^(?:a\s+)?(?:point\s+of\s+interest|mark|danger|landmark)\s+within\s+{_N}\s+"
            r"(?:miles?|nautical\s+miles?)$"
        ),
    ),
    # package 70: a sail within so many cables (the gun's range is cables, not miles)
    (
        "sail",
        re.compile(
            rf"^(?:a\s+)?(?:sail|stranger|enemy|ship|the\s+enemy)\s+within\s+{_N}\s+"
            r"(?:cables?|cables?\s+length)$"
        ),
    ),
)


def _number(words: str) -> float:
    w = words.strip()
    if w in _NUMBERS:
        return _NUMBERS[w]
    return float(w)


def _figure(n: float) -> str:
    return f"{n:g}"


def tripwire_of(words: str) -> Tripwire | None:
    """The tripwire these words name, or None: lower-cased, an 'until' already off."""
    w = " ".join(str(words).lower().split()).strip(" .!?,")
    for kind, pattern in _PATTERNS:
        m = pattern.match(w)
        if m is None:
            continue
        if kind == "settled":
            return Tripwire("her way settled", kind, 0.0)
        n = _number(m.group("n"))
        if n <= 0.0:
            return None
        said = {
            "depth": f"depth under {_figure(n)} fathoms",
            "speed_under": f"speed under {_figure(n)} knots",
            "speed_over": f"speed over {_figure(n)} knots",
            "wind": f"the wind over {_figure(n)} knots",
            "point": f"a point of interest within {_figure(n)} miles",
            "sail": f"a sail within {_figure(n)} cables",
        }[kind]
        return Tripwire(said, kind, n)
    return None


@dataclass(frozen=True)
class Tripwire:
    """One tripwire, watched once a tick as a reading's condition is (`holds(view,
    memory)`, the stand-by's own memory kept between ticks)."""

    text: str
    kind: str
    n: float

    def _dialect(self, ship: Any) -> list[Any]:
        from freesail.standing.grammar import parse_condition

        n = _figure(self.n)
        words = {
            # "the depth by the chart": the dialect reads "the depth of water ..." as the
            # lead's `the depth` (found on the way, package 58a)
            "depth": (
                f"the depth by the chart is less than {n} fathoms",
                f"the depth is less than {n} fathoms",
            ),
            "speed_under": (f"the speed is less than {n} knots",),
            "speed_over": (f"the speed exceeds {n} knots",),
            "wind": (f"the true wind exceeds {n} knots",),
        }[self.kind]
        return [parse_condition(w, ship) for w in words]

    def holds(self, view: Any, memory: dict[str, Any] | None = None) -> bool:
        memory = memory if memory is not None else {}
        world = getattr(view, "_world", None)
        if world is None:
            return False
        if self.kind == "settled":
            return self._settled(view, world, memory)
        if self.kind == "point":
            return self._point(world, memory)
        if self.kind == "sail":
            return self._sail(world, memory)
        conds = memory.get("dialect")
        if conds is None:
            conds = memory["dialect"] = self._dialect(world.ship)
        held = False
        for i, cond in enumerate(conds):
            mem = memory.setdefault(f"m{i}", {})
            if cond.holds(view, mem):
                held = True
        return held

    @staticmethod
    def _settled(view: Any, world: Any, memory: dict[str, Any]) -> bool:
        """Her speed within a quarter knot and her head within a quarter point for two
        minutes, begun again at any order given since the look before."""
        tick = int(world.clock.tick)
        orders = len(getattr(world, "journal", ()) or ())
        try:
            kn = units.ms_to_knots(float(view.value("speed") or 0.0))
            head = math.degrees(float(view.value("heading") or 0.0)) % 360.0
        except (TypeError, ValueError):
            return False
        hist: list[tuple[int, float, float]] = memory.setdefault("hist", [])
        if memory.get("orders") != orders:
            memory["orders"] = orders
            hist.clear()
            memory["from"] = tick
        hist.append((tick, kn, head))
        while hist and tick - hist[0][0] > SETTLED_S:
            hist.pop(0)
        if tick - int(memory.get("from", tick)) < SETTLED_S:
            return False
        kns = [h[1] for h in hist]
        ref = hist[0][2]
        spread = max(abs((h[2] - ref + 180.0) % 360.0 - 180.0) for h in hist)
        if max(kns) - min(kns) <= SETTLED_KN and spread <= SETTLED_DEG:
            memory["said"] = f", at {kns[-1]:.1f} knots"
            return True
        return False

    def _point(self, world: Any, memory: dict[str, Any]) -> bool:
        """A point of interest within the miles of her position by account that was not
        within them at the first look."""
        nav = getattr(world, "navigation", None)
        pos = nav.account_now() if nav is not None else None
        if pos is None:
            return False
        near = points_within(world, pos, self.n)
        known = memory.get("known")
        if known is None:
            memory["known"] = {k for k, _w, _d in near}
            return False
        for key, words, nm in near:
            if key not in known:
                memory["said"] = f": {words}, {miles_words(nm)} by account"
                return True
        return False

    def _sail(self, world: Any, memory: dict[str, Any]) -> bool:
        """A sail within the cables by the lookout's estimate that was not within them at
        the first look (package 70): the gun's range is judged by eye, never by the truth."""
        lookout = getattr(world, "lookout", None)
        if lookout is None:
            return False
        items = lookout.strangers(world, float(world.ship.heading)).get("items") or []
        cable = units.NAUTICAL_MILE / 10.0
        near = {
            str(i.get("id")): (str(i.get("known") or "a sail"), float(i["estimate_m"]) / cable)
            for i in items
            if i.get("estimate_m") is not None and float(i["estimate_m"]) <= self.n * cable
        }
        known = memory.get("known")
        if known is None:
            memory["known"] = set(near)
            return False
        for key, (words, cables) in near.items():
            if key not in known:
                memory["said"] = f": {words}, {cables:.1f} cables by estimation"
                return True
        return False


def points_within(world: Any, pos: Any, miles: float) -> list[tuple[str, str, float]]:
    """The points of interest within `miles` of `pos`, nearest first: (a key, the name,
    the miles), the chart's (`POINT_OF_INTEREST_KINDS`) and the world's own (`mark:`)."""
    from freesail.world.geo import bearing_and_distance

    radius = miles * units.NAUTICAL_MILE
    out: list[tuple[str, str, float]] = []
    chart = getattr(world, "chart", None)
    if chart is not None:
        for f in chart.nearby(pos, radius, POINT_OF_INTEREST_KINDS):
            d = bearing_and_distance(pos, f.position)[1] / units.NAUTICAL_MILE
            out.append((f"chart:{f.id}", str(f.name), d))
    for m in getattr(world, "marks_of_interest", None) or []:
        # a point of interest the world put on the sea (`mark:`, a chart `Feature`)
        d = bearing_and_distance(pos, m.position)[1] / units.NAUTICAL_MILE
        if d <= miles:
            out.append((f"mark:{m.id}", str(m.name), d))
    out.sort(key=lambda t: t[2])
    return out


def miles_words(nm: float) -> str:
    if nm < 0.95:
        cables = max(1, round(nm * 10))
        return "a cable" if cables == 1 else f"{cables} cables"
    rounded = round(nm * 2) / 2
    if rounded == 1.0:
        return "a mile"
    return f"{rounded:g} miles"
