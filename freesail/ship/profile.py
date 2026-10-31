"""Reading the hull's profile (package 75; docs/design/Build-Ships.md §3.1 item 16, §5).

A ship file's `hull.profile` (`schema.HullProfile`) gives the top of the side, the decks and
the ports in the fore-and-aft plane as lines of points, x forward of midships and z above the
file's waterline, in metres. These functions read it, and they are pure: the schema's
refusals, the generator's helpers (a port gun's height from its sill, a swivel's from the
rail), the lee ports' rule (the side's half-breadth at a port's sill, §7.1) and the tests
read the profile through them and never by hand. Between two points a line is straight;
beyond its first and last it is held at their values.
"""

from __future__ import annotations

from bisect import bisect_right
from collections.abc import Sequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from freesail.ship.schema import HullProfile


def interp(points: Sequence[Sequence[float]], x: float) -> float:
    """The value at `x` of a line of [x, value] points, x increasing (a point's further
    numbers, a triple's third, are not read): straight between two points, a point's own
    value at its x, held at the first and the last beyond them."""
    if not points:
        raise ValueError("a line of no points has no value at any x")
    x = float(x)
    if x <= points[0][0]:
        return float(points[0][1])
    if x >= points[-1][0]:
        return float(points[-1][1])
    i = bisect_right([p[0] for p in points], x) - 1
    x0, v0 = float(points[i][0]), float(points[i][1])
    if x == x0:
        return v0
    x1, v1 = float(points[i + 1][0]), float(points[i + 1][1])
    return v0 + (v1 - v0) * (x - x0) / (x1 - x0)


def rail_at(profile: HullProfile, x: float) -> float:
    """The top of the side at `x`, metres above the waterline."""
    return interp(profile.rail_m, x)


def deck_at(profile: HullProfile, x: float) -> float | None:
    """The uppermost deck at side at `x`, metres above the waterline: of the decks whose
    extent holds x, the highest there (the razee's quarterdeck abaft her open waist, her gun
    deck in it). Beyond every deck's extent, the nearest deck's end, held (judgement: a
    mast's foot or the stem head may stand a little beyond a deck's last point); None, a
    profile that gives no decks."""
    if not profile.decks_m:
        return None
    x = float(x)
    over = [interp(pts, x) for _word, pts in profile.decks_m if pts[0][0] <= x <= pts[-1][0]]
    if over:
        return max(over)

    def gap(pts: Sequence[Sequence[float]]) -> float:
        return pts[0][0] - x if x < pts[0][0] else x - pts[-1][0]

    nearest = min(gap(pts) for _word, pts in profile.decks_m)
    return max(interp(pts, x) for _word, pts in profile.decks_m if gap(pts) == nearest)


def ports_of(profile: HullProfile, deck: str) -> tuple[tuple[float, float, float], ...]:
    """The deck's ports on one side, as [x, sill, half-breadth] triples from aft forward;
    none, a deck the profile gives no ports."""
    for word, triples in profile.ports_m:
        if word == deck:
            return triples
    return ()


def sill_at(profile: HullProfile, deck: str, x: float) -> float | None:
    """The deck's port sill at `x`, metres above the waterline: straight between its ports'
    sills, held beyond the end ports; None, a deck with no ports in the profile."""
    triples = ports_of(profile, deck)
    if not triples:
        return None
    return interp([(p[0], p[1]) for p in triples], x)


def half_breadth_at_sill(profile: HullProfile, deck: str, x: float) -> float | None:
    """The side's half-breadth at the deck's port sill at `x`, metres: straight between its
    ports' triples, held beyond the end ports; None, a deck with no ports in the profile,
    where the lee ports' rule takes half the beam (Build-Ships.md §7.1)."""
    triples = ports_of(profile, deck)
    if not triples:
        return None
    return interp([(p[0], p[2]) for p in triples], x)
