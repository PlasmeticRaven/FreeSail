"""The marks for practice at the great guns (practice and resupply, between packages 72 and
73; docs/design/Build-PracticeAndResupply.md §1.5, §6): an empty cask with a flag on a staff
hove over the side from the quarter, or a notional mark laid at a bearing and a range by
the captain's word.

A mark is never a ship: it is not in `world.vessels`, it has no colours and no people, and
the shot that strikes it changes nothing but the cask (`hits.resolve_shot` hands it here).
Its target id carries `PRACTICE_PREFIX`, so that nothing of the action's (the recognition,
the outlaw, the witnesses, morale) takes it for a sail. The cask is a lookout's sighting
with a stream of its own ("practice"), opened only when a cask is first seen, so that no
draw of an existing scenario moves.

**The cask** goes over the side from the quarter (`HeaveMarkScript`, a minute's work for
two hands) and floats where it fell, set by the tide's stream and blown to leeward a
little, once a minute (`tick`). The gun captains lay for it by the truth, as for a ship; it
is fired at only while the masthead has it in sight (`target_of_mark`), by day within a
mile and the weather's visibility, at twilight half that, never by night (`sightings`). It
is knocked to staves by the first shot that strikes it (`struck`), lost when she is three
miles from it, and given up when another is hove over. Each is said once.

**The notional mark** is the captain's word: "a mark four cables on the starboard beam", a
cutter's length beam-on at that bearing from her head and that range, wherever she heads,
by night and in fog alike; nothing is seen of it and nothing strikes it but in the minute's
line ("on the mark").

**The allowance.** A King's ship's live rounds at a mark are counted by the month against
the Regulations' allowance for exercise (the Gunner, Art. XXI, l.13122-13144: a fourth of
the upper deck's guns a month for the first six months; the ship file's
`exercise_charges`); the first round beyond it is said once a month and entered in the
gunner's account (`count_live`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.core.events import Severity

if TYPE_CHECKING:
    from freesail.combat.guns import Target
    from freesail.world.chart import Sighting
    from freesail.world.geo import Position

__all__ = [
    "CASK_HEIGHT_M",
    "CASK_LEEWAY_SHARE",
    "CASK_LENGTH_M",
    "CASK_LOST_NM",
    "CASK_SEEN_DAY_NM",
    "CASK_SIZE",
    "NOTIONAL_ID",
    "NOTIONAL_LENGTH_M",
    "PRACTICE_PREFIX",
    "Cask",
    "Practice",
    "abandon",
    "cask_in_sight",
    "cask_in_water",
    "count_live",
    "drop_cask",
    "is_mark",
    "lay_notional",
    "practice_of",
    "seen_range_nm",
    "sightings",
    "struck",
    "target_of_mark",
    "tick",
]

# The target id's prefix: never 'mark:' (the director's), nor truth 7-135's bare 'mark',
# nor a sighting's seen_as 'mark' (the lookout counts that as land).
PRACTICE_PREFIX = "practice:"
NOTIONAL_ID = f"{PRACTICE_PREFIX}notional"
# The cask's length (judgement), and the size term of the hit chance without the hull's
# floor, about 0.16: every hull under 10 m is given 0.5 today, and a cask would be hit as
# often as a cutter (decision 18).
CASK_LENGTH_M = 1.0
CASK_SIZE = math.sqrt(CASK_LENGTH_M / 40.0)
CASK_HEIGHT_M = 2.0  # the flag on its staff
# Made out from the masthead by day at a mile at most (judgement); at twilight that times
# `chart.TWILIGHT_FACTOR`; never by night.
CASK_SEEN_DAY_NM = 1.0
CASK_LEEWAY_SHARE = 0.02  # of the wind's base speed, to leeward (judgement)
CASK_LOST_NM = 3.0  # given up when she is three miles from it (judgement)
NOTIONAL_LENGTH_M = 20.0  # the notional mark: a cutter's length, beam-on (judgement)
# The cask goes over the side from the quarter: four points abaft the beam, and six
# tenths of her length from her centre (judgement on the quarter's place).
HEAVE_RELATIVE_DEG = 135.0
HEAVE_LENGTH_SHARE = 0.6


@dataclass
class Cask:
    """The cask in the water: its id (`practice:cask-N`), where it floats, the tick it went
    over, and how it was given up ("", "struck", "lost", "abandoned"). Every field after
    the first three takes a plain default, and so does any field added later."""

    id: str
    position: Position
    dropped_tick: int
    gone: str = ""
    gone_tick: int | None = None
    gone_said: bool = False
    struck_by: str = ""
    struck_at_m: float = 0.0


@dataclass
class Practice:
    """A ship's practice, kept in `ship.extra["practice"]`: the cask in the water, the
    notional mark laid (relative degrees, metres, the words), the casks' serial, the
    lookout's last say of the cask ("", "seen", "lost"), and the month's live rounds against
    the allowance ("1805-06"). Immutable defaults only."""

    cask: Cask | None = None
    notional: tuple[float, float, str] | None = None
    serial: int = 0
    sight: str = ""
    month: str = ""
    month_rounds: int = 0
    said_beyond: str = ""  # the month the allowance line was said


def is_mark(target_id: str | None) -> bool:
    """Whether a battery's target id is a mark for practice, and never a sail."""
    return bool(target_id) and str(target_id).startswith(PRACTICE_PREFIX)


def practice_of(ship: Any) -> Practice | None:
    """The ship's practice, or None when there has been none."""
    extra = getattr(ship, "extra", None)
    if not extra:
        return None
    p = extra.get("practice")
    return p if isinstance(p, Practice) else None


def _practice_for(ship: Any) -> Practice:
    """The ship's practice, made at the first heave or the first mark laid."""
    p = practice_of(ship)
    if p is None:
        p = Practice()
        ship.extra["practice"] = p
    return p


def cask_in_water(ship: Any) -> Cask | None:
    """The cask in the water now, neither struck, lost nor given up; None when there is
    none."""
    p = practice_of(ship)
    cask = p.cask if p is not None else None
    return cask if cask is not None and not cask.gone else None


def cask_in_sight(world: Any, cask: Cask) -> bool:
    """Whether the masthead has the cask among its last look's sightings."""
    lookout = getattr(world, "lookout", None)
    if lookout is None:
        return False
    return any(s.feature.id == cask.id for s in getattr(lookout, "sightings", ()) or ())


# -- the cask over the side, and the notional mark ----------------------------------------


def drop_cask(world: Any, side: str) -> Cask:
    """A cask hove over the side from the quarter on `side` ("starboard" or "larboard"):
    four points abaft the beam and six tenths of her length from her centre. A cask still
    in the water is given up first (`abandon`). Nothing is drawn."""
    from freesail.world.geo import destination

    ship = world.ship
    pos = getattr(world, "position", None)
    if pos is None:
        raise ValueError("a cask over the side needs the ship's position on the sphere")
    battery = (getattr(ship, "extra", None) or {}).get("battery")
    abandon(world, battery)
    p = _practice_for(ship)
    sign = 1.0 if side == "starboard" else -1.0
    heading = math.degrees(float(ship.heading))
    length = float(getattr(getattr(ship, "hull", None), "length", 0.0) or 20.0)
    where = destination(
        pos, (heading + sign * HEAVE_RELATIVE_DEG) % 360.0, HEAVE_LENGTH_SHARE * length
    )
    p.serial += 1
    cask = Cask(f"{PRACTICE_PREFIX}cask-{p.serial}", where, int(world.clock.tick))
    p.cask = cask
    p.sight = ""
    return cask


def abandon(world: Any, battery: Any = None) -> bool:
    """The cask in the water given up at a fresh heave: said once (ROUTINE
    `practice.mark_lost`), and the battery's mark cleared when it was the cask. False when
    none was in the water."""
    cask = cask_in_water(world.ship)
    if cask is None:
        return False
    cask.gone, cask.gone_tick, cask.gone_said = "abandoned", int(world.clock.tick), True
    _clear(battery, cask.id)
    world.record(
        Severity.ROUTINE,
        "practice.mark_lost",
        "The old mark is given up: a fresh cask goes over the side for another.",
        data={"id": cask.id, "gone": "abandoned"},
    )
    return True


def lay_notional(world: Any, relative_deg: float, range_m: float, words: str) -> None:
    """A notional mark laid at a bearing from her head (degrees, starboard positive) and a
    range in metres, with its words ("the mark four cables on the starboard beam"); the
    battery's target is then `NOTIONAL_ID`, set by the caller."""
    p = _practice_for(world.ship)
    p.notional = (float(relative_deg), float(range_m), str(words))


def target_of_mark(world: Any, target_id: str) -> Target | None:
    """The `Target` for a mark's id, as `action.target_of` gives one for a sail: the cask by
    the truth of its bearing and range while it is in the water and the masthead has it in
    sight, or the notional mark at its bearing from her head and its range. Either is
    beam-on at any bearing (its heading the bearing and a right angle), so the aspect term
    is whole."""
    from freesail.combat.guns import Target

    ship = getattr(world, "ship", None)
    p = practice_of(ship)
    if p is None:
        return None
    if target_id == NOTIONAL_ID:
        if p.notional is None:
            return None
        relative_deg, range_m, words = p.notional
        bearing = units.wrap_2pi(float(ship.heading) + math.radians(relative_deg))
        return Target(
            id=NOTIONAL_ID,
            words=words,
            bearing_rad=bearing,
            range_m=float(range_m),
            heading_rad=units.wrap_2pi(bearing + math.pi / 2.0),
            length_m=NOTIONAL_LENGTH_M,
            heel_deg=0.0,
            nation=None,
            body=None,
            world=None,
            mark="notional",
            size=None,
        )
    cask = p.cask
    if cask is None or cask.id != target_id or cask.gone:
        return None
    here = getattr(world, "position", None)
    if here is None or not cask_in_sight(world, cask):
        return None
    from freesail.world.geo import bearing_and_distance

    bearing_deg, distance = bearing_and_distance(here, cask.position)
    bearing = math.radians(bearing_deg)
    return Target(
        id=cask.id,
        words="the cask",
        bearing_rad=bearing,
        range_m=float(distance),
        heading_rad=units.wrap_2pi(bearing + math.pi / 2.0),
        length_m=CASK_LENGTH_M,
        heel_deg=0.0,
        nation=None,
        body=cask,
        world=None,
        mark="cask",
        size=CASK_SIZE,
    )


# -- the lookout ---------------------------------------------------------------------------


def seen_range_nm(visibility_nm: float | None, daylight: str) -> float:
    """How far the masthead makes the cask out, in miles: `CASK_SEEN_DAY_NM` by day within
    the visibility, half that at twilight (`chart.TWILIGHT_FACTOR`), nothing by night."""
    from freesail.world.chart import TWILIGHT_FACTOR

    if str(daylight) == "night":
        return 0.0
    reach = CASK_SEEN_DAY_NM
    if visibility_nm is not None:
        reach = min(reach, float(visibility_nm))
    if str(daylight) != "day":
        reach *= TWILIGHT_FACTOR
    return reach


def sightings(
    world: Any, pos: Position, visibility_nm: float | None, daylight: str
) -> list[Sighting]:
    """The cask as the masthead makes it out, for the lookout's `look`: a sighting seen as
    "cask", named "the mark", within `seen_range_nm`; none when no cask is in the water."""
    cask = cask_in_water(getattr(world, "ship", None))
    if cask is None or pos is None:
        return []
    reach = seen_range_nm(visibility_nm, daylight)
    if reach <= 0.0:
        return []
    from freesail.world.chart import Feature, Sighting
    from freesail.world.geo import bearing_and_distance

    bearing, distance = bearing_and_distance(pos, cask.position)
    if distance > reach * units.NAUTICAL_MILE:
        return []
    feature = Feature(
        cask.id,
        "cask",
        "the mark",
        cask.position.lat_deg,
        cask.position.lon_deg,
        modern=cask.id,
        height_m=CASK_HEIGHT_M,
    )
    return [Sighting(feature, bearing, distance, "cask")]


# -- the shot, and the rounds -------------------------------------------------------------


def struck(battery: Any, gun: Any, target: Target, tick: int) -> list[str]:
    """A shot that struck a mark: the cask knocked to staves at the first (who struck it,
    and at what range, kept for `tick`'s line), nothing at a second in the same tick, and
    nothing at the notional mark; what her people saw of it is the minute's line alone.
    Nothing is drawn."""
    cask = getattr(target, "body", None)
    if isinstance(cask, Cask) and not cask.gone:
        cask.gone = "struck"
        cask.gone_tick = int(tick)
        cask.struck_by = str(getattr(gun, "name", "") or "")
        cask.struck_at_m = float(target.range_m)
    return []


def count_live(world: Any, rounds: int) -> None:
    """Live rounds fired at a mark, counted against the month's allowance for exercise: a
    King's ship's bound by the Regulations (`service.under_the_regulations`) whose fit gives
    `exercise_charges`. The first round beyond it in a month is said once (NOTABLE
    `practice.beyond_allowance`) and entered in the gunner's account and its paper; the
    King's cutter's allowance of one is "one charge" (the review's finding)."""
    if rounds <= 0:
        return
    ship = world.ship
    fit = getattr(ship, "fit_spec", None)
    allowance = int(getattr(fit, "exercise_charges", 0) or 0)
    if allowance <= 0:
        return
    from freesail.world.service import under_the_regulations

    if not under_the_regulations(world):
        return
    p = _practice_for(ship)
    now = world.clock.ship_time
    month = f"{now:%Y-%m}"
    if p.month != month:
        p.month, p.month_rounds = month, 0
    p.month_rounds += int(rounds)
    if p.month_rounds <= allowance or p.said_beyond == month:
        return
    p.said_beyond = month
    from freesail.crew.model import number_words

    charges = f"{number_words(allowance)} charge{'' if allowance == 1 else 's'}"
    world.record(
        Severity.NOTABLE,
        "practice.beyond_allowance",
        f"Beyond the allowance for exercise this month ({charges} by the Regulations, the "
        "Gunner, Art. XXI): the powder past it is spent on the captain's word, and the "
        "gunner's account keeps it.",
        data={"month": month, "rounds": p.month_rounds, "allowance": allowance},
    )
    from freesail.ship.parts import magazine

    when = f"{now:%d %B}, {units.time_stamp(now)}"
    words = (
        f"powder for exercise beyond the allowance of {charges} this month, on the captain's word"
    )
    magazine(ship).enter(when, words)
    papers = getattr(world, "papers", None)
    if papers is None:
        return
    try:
        line = papers.write("the gunner's account", words)
    except KeyError:
        return  # the paper is Builder 2's (practice and resupply): none aboard before it
    world.record(Severity.ROUTINE, "paper.written", line, data={"paper": "the gunner's account"})


# -- the minute ----------------------------------------------------------------------------


def tick(world: Any, battery: Any, tick: int, minute: bool) -> None:
    """The marks' minute, after the battery's tick and its line: the cask struck said once
    and the mark cleared; else the cask set by the stream and the wind, given up at three
    miles, and the lookout's word when it is lost to sight and when it is made out again.
    Nothing between the minutes, nothing with no practice, and nothing drawn."""
    if not minute:
        return
    ship = getattr(world, "ship", None)
    p = practice_of(ship)
    if p is None:
        return
    cask = p.cask
    if cask is None or cask.gone_said:
        return
    from freesail.world.geo import bearing_and_distance, estimate_words

    if cask.gone == "struck":
        cask.gone_said = True
        _clear(battery, cask.id)
        who = cask.struck_by or "a gun"
        world.record(
            Severity.NOTABLE,
            "practice.mark_struck",
            f"The mark struck by {who} at {estimate_words(cask.struck_at_m)} and knocked to "
            "staves; the guns hold their fire for want of a mark.",
            data={"id": cask.id, "by": cask.struck_by, "range_m": round(cask.struck_at_m)},
        )
        return
    if cask.gone:
        cask.gone_said = True
        return
    _drift(world, cask)
    here = getattr(world, "position", None)
    if here is None:
        return
    bearing_deg, distance = bearing_and_distance(here, cask.position)
    if distance > CASK_LOST_NM * units.NAUTICAL_MILE:
        cask.gone, cask.gone_tick, cask.gone_said = "lost", int(tick), True
        _clear(battery, cask.id)
        relative = units.wrap_pi(math.radians(bearing_deg) - float(ship.heading))
        where = "astern" if abs(relative) > math.pi / 2.0 else _relative(relative)
        world.record(
            Severity.ROUTINE,
            "practice.mark_lost",
            f"The mark is lost {where}, {estimate_words(distance)} off.",
            data={"id": cask.id, "gone": "lost", "range_m": round(distance)},
        )
        return
    seen = cask_in_sight(world, cask)
    if seen and p.sight == "lost":
        p.sight = "seen"
        point = units.point_name(math.radians(bearing_deg))
        world.record(
            Severity.ROUTINE,
            "practice.mark_sight",
            f"The mark is made out again, bearing {point}, about {_judged(world, cask, distance)}.",
            data={"id": cask.id, "seen": True},
        )
    elif seen:
        p.sight = "seen"  # the first sighting says nothing: the heave said it
    elif p.sight == "seen":
        p.sight = "lost"
        world.record(
            Severity.ROUTINE,
            "practice.mark_sight",
            f"The mark is lost to sight{_lost_why(world, distance)}.",
            data={"id": cask.id, "seen": False},
        )


def _drift(world: Any, cask: Cask) -> None:
    """A minute's set: the tide's stream where the cask floats (as `Vessel._stream` reads
    it, ships.py:843-850) and a share of the wind's base speed to leeward."""
    dt = 60.0
    east = north = 0.0
    tide = getattr(world, "tide", None)
    if tide is not None:
        from freesail.world.sights import greenwich_time

        east, north = tide.stream_at(cask.position, greenwich_time(world))
    wind = getattr(world, "wind", None)
    if wind is not None:
        leeway = CASK_LEEWAY_SHARE * float(wind.base_speed)
        toward = float(wind.direction_from) + math.pi
        east += leeway * math.sin(toward)
        north += leeway * math.cos(toward)
    if east or north:
        cask.position = cask.position.advanced(east * dt, north * dt)


def _judged(world: Any, cask: Cask, distance: float) -> str:
    """The cask's distance as the lookout judges it (his estimate), else the truth."""
    from freesail.world.geo import estimate_words

    lookout = getattr(world, "lookout", None)
    for s in getattr(lookout, "sightings", ()) or ():
        if s.feature.id == cask.id:
            return estimate_words(s.judged_m)
    return estimate_words(distance)


def _lost_why(world: Any, distance: float) -> str:
    """Why the masthead has lost the cask, as the line's tail: in the dark, in the failing
    light, in the haze, or too far off."""
    daylight = str(getattr(world, "daylight", "day"))
    if daylight == "night":
        return " in the dark"
    conditions = getattr(world, "conditions", None)
    vis = getattr(conditions, "visibility_nm", None) if conditions is not None else None
    if vis is not None and float(vis) * units.NAUTICAL_MILE < distance:
        return " in the haze"
    if daylight != "day":
        return " in the failing light"
    return ", too far off to be made out from the masthead"


def _relative(relative_rad: float) -> str:
    from freesail.world.lookout import relative_words

    return relative_words(relative_rad)


def _clear(battery: Any, cask_id: str) -> None:
    """The battery's mark dropped when it was this cask: nothing to fire at."""
    if battery is not None and getattr(battery, "target", None) == cask_id:
        battery.target = None
        battery.target_words = ""
