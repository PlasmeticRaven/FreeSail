"""The practice's reading and the events of practice and resupply (between packages 72 and
73; docs/design/Build-PracticeAndResupply.md §1.7, §8), registered in the readings registry
(`api.readings.REGISTRY`, `EVENTS`) from this module, which `readings` imports at its end
after the squadron's.

The row, a state in words the dialect compares by `is <words>` and `is not <words>`:

    the practice      the practice at the great guns: each gun's rounds in dumb show and
                      live, the mean and the best from sponge to point (a swivel's from
                      its cartridge); the falls of shot at the mark by cables; the mark, a
                      cask or a notional one, with its bearing and range and whether it is
                      in sight; the month's rounds against the allowance for exercise;
                      'none' when there has been none

The row rides a sample only while she is exercising, a mark is engaged or a cask is in the
water (`idle_practice_rows`).

The events, for `at` and a stand-by: `the gunner filling` (`guns.filling`), `the cartridges
filled` (`guns.filled`), `the powder all filled` (`guns.powder_out`), `the hoy alongside`
(`ordnance.alongside`), `the powder stowed` (`ordnance.stowed`), `the hoy turned back`
(`ordnance.missed`), `the mark over the side` (`practice.mark_over`), `the mark struck`
(`practice.mark_struck`), `the mark lost` (`practice.mark_lost`), `the mark lost to sight`
and `the mark in sight again` (`practice.mark_sight`, by its `seen`), `the exercise`
(`practice.exercise`), `beyond the allowance` (`practice.beyond_allowance`).

The drill's counts are the battery's (`guns.Drill`, kept per gun and never read for pace or
aim: the owner's ruling that practice improves no skill); the reading only says them.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.api import readings as R
from freesail.combat import marks
from freesail.combat.guns import seconds_words
from freesail.ship.parts import gun_words

__all__ = ["PRACTICE_ROWS", "idle_practice_rows", "practice_value", "register"]

PRACTICE_ROWS: tuple[str, ...] = ("practice",)


def idle_practice_rows(world: Any) -> set[str]:
    """The practice's rows to leave out of a sample now: every one, unless she is
    exercising in dumb show, a mark is engaged, or a cask is in the water."""
    ship = getattr(world, "ship", None)
    extra = getattr(ship, "extra", None) or {}
    battery = extra.get("battery")
    if battery is not None and (
        getattr(battery, "exercise", None) or marks.is_mark(getattr(battery, "target", None))
    ):
        return set()
    if ship is not None and marks.cask_in_water(ship) is not None:
        return set()
    return set(PRACTICE_ROWS)


def _no_guns_words(world: Any) -> str | None:
    ship = getattr(world, "ship", None)
    if ship is not None and not getattr(ship, "guns", None):
        return "she carries no guns"
    return None


def _side_words(side: str) -> str:
    return "both batteries" if side == "both" else f"the {side} battery"


def _guns_words(ship: Any, drill: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    """Each gun's drill as data, and the pace by the guns' kinds in words: the mean of
    their timed cycles and the best, from the sponge to the point (a swivel's from its
    cartridge, for it has no sponge: `guns.PHASES`), the kind named for the guns of it
    she carries ('the long 12-pounder' for the one pivot gun; the review's finding)."""
    guns: dict[str, Any] = {}
    by_kind: dict[tuple[str, float], list[Any]] = {}
    for gid in sorted(drill):
        d = drill[gid]
        cycles = int(getattr(d, "cycles", 0) or 0)
        total = float(getattr(d, "total_s", 0.0) or 0.0)
        best = getattr(d, "best_s", None)
        guns[gid] = {
            "dumb": int(getattr(d, "dumb", 0) or 0),
            "live": int(getattr(d, "live", 0) or 0),
            "cycles": cycles,
            "mean_s": round(total / cycles, 1) if cycles else None,
            "best_s": round(float(best), 1) if best is not None else None,
        }
        g = getattr(ship, "guns", {}).get(gid)
        if g is not None and cycles:
            by_kind.setdefault((str(g.kind), float(g.pounder)), []).append(d)
    words = []
    for (kind, pounder), ds in by_kind.items():
        cycles = sum(int(d.cycles) for d in ds)
        mean = sum(float(d.total_s) for d in ds) / cycles
        best = min(float(d.best_s) for d in ds if d.best_s is not None)
        n = sum(
            1
            for x in getattr(ship, "guns", {}).values()
            if x.kind == kind and float(x.pounder) == pounder
        )
        start = "cartridge" if kind == "swivel" else "sponge"
        words.append(
            f"the {gun_words(kind, pounder, n)} {seconds_words(mean)} from {start} to point "
            f"on the mean, the best {seconds_words(best)}"
        )
    return guns, words


def _falls(drill: dict[str, Any]) -> tuple[dict[str, dict[str, int]], list[str]]:
    """The falls of shot at the marks by cables (the drills' "2 struck", "4 short", and at
    the notional mark "4 struck notional"), summed over the guns and the marks:
    {"2": {"struck": 3, "short": 1}}; and in words, a hit at the cask "struck" and one at
    the notional mark "on the mark", as the minute's line says them (§6; the review's
    finding: the notional mark's hits were "struck" in the reading)."""
    falls: dict[str, dict[str, int]] = {}
    hits: dict[str, dict[str, int]] = {}  # cables -> {"cask": n, "notional": n}, the hits
    for d in drill.values():
        for key, n in (getattr(d, "falls", None) or {}).items():
            cables, _, rest = str(key).partition(" ")
            outcome, _, mark = rest.partition(" ")
            outcome = outcome or "fired"
            row = falls.setdefault(cables, {})
            row[outcome] = row.get(outcome, 0) + int(n)
            at = hits.setdefault(cables, {})
            which = "notional" if mark == "notional" else "cask"
            at[which] = at.get(which, 0) + (int(n) if outcome == "struck" else 0)

    def order(k: str) -> float:
        try:
            return float(k)
        except ValueError:
            return math.inf

    falls = {k: falls[k] for k in sorted(falls, key=order)}
    words = []
    for cables, row in falls.items():
        fired = sum(row.values())
        at = hits.get(cables, {})
        said = []
        if "cask" in at:
            said.append(f"{at['cask']} struck")
        if "notional" in at:
            said.append(f"{at['notional']} on the mark")
        unit = "cable" if cables == "1" else "cables"
        words.append(f"at {cables} {unit} {' and '.join(said)} of {fired}")
    return falls, words


def _mark(world: Any, battery: Any, p: Any) -> dict[str, Any] | None:
    """The mark engaged, else the cask the last hove over: its kind and words, its bearing
    by the point and its range in cables (the lookout's estimate for the cask, the stated
    range for the notional mark), whether it is in sight, and how it was given up."""
    ship = world.ship
    target = getattr(battery, "target", None) if battery is not None else None
    heading = float(ship.heading)
    if target == marks.NOTIONAL_ID and p is not None and p.notional is not None:
        relative_deg, range_m, words = p.notional
        bearing = units.wrap_2pi(heading + math.radians(relative_deg))
        return {
            "kind": "notional",
            "words": words,
            "bearing": units.point_name(bearing),
            "range_cables": round(range_m / units.CABLE, 1),
            "in_sight": False,
            "gone": "",
            "engaged": True,
        }
    cask = p.cask if p is not None else None
    if cask is None:
        return None
    from freesail.world.lookout import relative_words

    seen = None
    lookout = getattr(world, "lookout", None)
    for s in getattr(lookout, "sightings", ()) or ():
        if s.feature.id == cask.id:
            seen = s
    data: dict[str, Any] = {
        "kind": "cask",
        "words": "the cask",
        "bearing": None,
        "range_cables": None,
        "in_sight": seen is not None and not cask.gone,
        "gone": cask.gone,
        "engaged": target == cask.id,
    }
    if seen is not None and not cask.gone:
        b = math.radians(seen.bearing_deg)
        data["bearing"] = units.point_name(b)
        data["relative"] = relative_words(b - heading)
        data["range_cables"] = round(seen.judged_m / units.CABLE, 1)
    return data


def _mark_words(mark: dict[str, Any]) -> str:
    if mark["kind"] == "notional":
        return f"engaged at {mark['words']}"
    gone = {
        "struck": "the last cask knocked to staves",
        "lost": "the last cask lost",
        "abandoned": "the last cask given up",
    }.get(mark["gone"])
    if gone:
        return gone
    if not mark["in_sight"]:
        return "the cask in the water, not in sight from the masthead"
    cables = float(mark["range_cables"])
    if cables < 0.5:
        distance = "close aboard"
    else:
        distance = f"{cables:g} cable{'' if cables == 1 else 's'} by estimation"
    engaged = ", engaged" if mark["engaged"] else ""
    return f"the cask {mark['relative']}, bearing {mark['bearing']}, {distance}{engaged}"


def _month(world: Any, p: Any) -> dict[str, Any] | None:
    """The month's live rounds against the allowance for exercise, for a King's ship bound
    by the Regulations whose fit gives one (`marks.count_live` keeps the count)."""
    fit = getattr(world.ship, "fit_spec", None)
    allowance = int(getattr(fit, "exercise_charges", 0) or 0)
    if allowance <= 0:
        return None
    from freesail.world.service import under_the_regulations

    if not under_the_regulations(world):
        return None
    month = f"{world.clock.ship_time:%Y-%m}"
    rounds = p.month_rounds if p is not None and p.month == month else 0
    return {
        "month": month,
        "rounds": rounds,
        "allowance": allowance,
        "beyond": max(0, rounds - allowance),
    }


def practice_value(world: Any) -> dict[str, Any] | None:
    """The practice at the great guns, as data and in words (the module's head); None for
    a ship with no guns."""
    ship = getattr(world, "ship", None)
    if ship is None or not getattr(ship, "guns", None):
        return None
    extra = getattr(ship, "extra", None) or {}
    battery = extra.get("battery")
    p = marks.practice_of(ship)
    exercise = getattr(battery, "exercise", None) if battery is not None else None
    drill = dict(getattr(battery, "drill", None) or {}) if battery is not None else {}
    guns, pace = _guns_words(ship, drill)
    falls, fall_words = _falls(drill)
    mark = _mark(world, battery, p)
    month = _month(world, p)
    dumb = sum(g["dumb"] for g in guns.values())
    live = sum(g["live"] for g in guns.values())
    parts: list[str] = []
    if exercise:
        parts.append(f"exercising {_side_words(exercise)} in dumb show")
    rounds = []
    if dumb:
        rounds.append(f"{dumb} round{'' if dumb == 1 else 's'} in dumb show")
    if live:
        rounds.append(f"{live} live" if dumb else f"{live} live round{'' if live == 1 else 's'}")
    if rounds:
        parts.append(" and ".join(rounds))
    parts.extend(pace)
    if fall_words:
        parts.append("at the mark " + ", ".join(fall_words))
    if mark is not None:
        parts.append(_mark_words(mark))
    if month is not None and month["rounds"]:
        beyond = f", {month['beyond']} beyond it" if month["beyond"] else ""
        parts.append(
            f"this month {month['rounds']} live round{'' if month['rounds'] == 1 else 's'} of "
            f"an allowance of {month['allowance']}{beyond}"
        )
    return {
        "words": "; ".join(parts) if parts else "none",
        "exercise": exercise,
        "dumb": dumb,
        "live": live,
        "guns": guns,
        "falls": falls,
        "mark": mark,
        "month": month,
    }


def _practice(world: Any, _: str | None) -> dict[str, Any] | None:
    return practice_value(world)


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "practice",
            ("the practice", "the exercise", "the gun drill"),
            "state",
            "",
            _practice,
            description="the practice at the great guns: each gun's rounds in dumb show and "
            "live, the mean and the best from sponge to point, the falls of shot at the mark "
            "by cables, the mark with its bearing and range and whether it is in sight, the "
            "month's rounds against the allowance for exercise; 'none'",
            none_words=_no_guns_words,
        )
    )
    ev = R.EventSpec
    for spec in (
        ev("the gunner filling", "guns.filling"),
        ev("the cartridges filled", "guns.filled"),
        ev("the powder all filled", "guns.powder_out"),
        ev("the hoy alongside", "ordnance.alongside"),
        ev("the powder stowed", "ordnance.stowed"),
        ev("the hoy turned back", "ordnance.missed"),
        ev("the mark over the side", "practice.mark_over"),
        ev("the mark struck", "practice.mark_struck"),
        ev("the mark lost", "practice.mark_lost"),
        ev("the mark lost to sight", "practice.mark_sight", lambda d: not d.get("seen")),
        ev("the mark in sight again", "practice.mark_sight", lambda d: bool(d.get("seen"))),
        ev("the exercise", "practice.exercise"),
        ev("beyond the allowance", "practice.beyond_allowance"),
    ):
        R.EVENTS[spec.words] = spec
