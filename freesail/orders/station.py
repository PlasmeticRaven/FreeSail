"""Station keeping on the near body (spec M7 §21; package 72; docs/design/Design-Squadrons.md):
`keep station` as a held order of the navigation, in the family of `keep her full and by`,
worked by the books every two minutes (the `in company` book of every role) and given by
the player in his own words.

    keep station                         her station in her set (refused in words in none)
    keep your station                    the same, or the station last ordered
    keep station two cables astern of the Harpy
    keep station on the larboard beam of the flagship
    keep station a cable to windward of the Harpy

What is read is the lookout's (`tests/test_captains.py`'s proof that the near captain reads
no truth holds): the flag's bearing and distance by estimation from the sails in sight, her
course by what the tops have made out of her heading (to the nearest point) or his own
heading when they have not, the wind at the ship; the set's offset for her slot from the
squadron's formation through the parent World (the set is the player's own, or the one his
ship is a member of). From these the station point is laid relative to the ship, and:

- within the tolerance (half a cable) she steers the flag's course, going with her;
- astern of her station she steers for it under the helm's law (never within the
  close-hauled angle: a station to windward is worked up to on the tack that points nearer)
  and makes sail when she is far astern;
- ahead of it (the station bears abaft her beam) she steers the flag's course and shortens
  sail, to drop back into it; sail is made again when she is in station.

One line a glass unless something changes (the course laid anew by more than a point, the
sail changed, in and out of station); `sail.out_of_station` and `sail.in_station` are the
events the books and a stand-by read. The period's station keeping was done by the
topgallants and the topsails' reefs and by the officer of the watch's eye on the ship
ahead (Falconer 1780, STATION; the Regulations 1806 on the order of sailing; judgement on
the steps).
"""

from __future__ import annotations

import math
import re
from typing import Any

from freesail import units
from freesail.orders.errors import OrderError

__all__ = ["STATION_TOLERANCE_M", "execute", "keep_station_minute", "station_reading"]

Result = tuple[str, str, dict[str, Any]]

# The tolerance of the near body's station: half a cable (the set's own figure).
STATION_TOLERANCE_M = 0.5 * units.CABLE
# Astern of her station by more than this she makes sail; ahead of it by more than this she
# shortens (judgement: a cable, the step the topgallants are worth in a glass).
SAIL_STEP_M = 1.0 * units.CABLE
# A new course is said and the helm put again when it differs from the last by a point.
RELAY_DEG = 11.25
# Out of station she steers for a point this far ahead of her station along the flag's
# course (judgement: three cables, so that a ship a cable off her station closes it at
# some twenty degrees to the line and not by chasing the point across it).
LEAD_M = 3.0 * units.CABLE
# Ahead of her station she shortens sail a step at a time, this often, up to so many steps
# (judgement: a glass between steps for the hands to finish the last; four steps take her
# from all plain sail to reefed topsails).
SHORT_STEPS = 4
SHORT_EVERY_S = 120

_BEARING_WORDS = {
    "astern": "astern",
    "ahead": "ahead",
    "to windward": "windward",
    "to weather": "windward",
    "to leeward": "leeward",
    "on the larboard beam": "larboard beam",
    "on the port beam": "larboard beam",
    "on the starboard beam": "starboard beam",
    "on the larboard quarter": "larboard quarter",
    "on the starboard quarter": "starboard quarter",
    "on the larboard bow": "larboard bow",
    "on the starboard bow": "starboard bow",
}
_SPEC = re.compile(
    r"^(?:(?P<n>[\w.]+)\s+cables?\s+)?(?P<where>astern|ahead|to windward|to weather|to leeward|"
    r"on the (?:larboard|port|starboard) (?:beam|quarter|bow))\s+of\s+(?P<flag>.+)$"
)


def _root(world: Any) -> Any:
    return getattr(world, "parent", None) or world


def _own_id(world: Any) -> str:
    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else "the ship"


def _set_of(world: Any) -> Any:
    sets = getattr(_root(world), "squadrons", None)
    return sets.of(_own_id(world)) if sets is not None else None


def _parse(world: Any, rest: str) -> dict[str, Any]:
    """The station's spec from the words: the set's station (nothing said, or 'your
    station'), or so many cables in a direction of a ship named."""
    low = " ".join(str(rest or "").lower().split()).strip(" .")
    if low in ("", "your station", "her station", "the station", "station", "in the line"):
        sq = _set_of(world)
        if sq is None:
            held = (getattr(world.ship, "extra", None) or {}).get("station")
            if held and held.get("flag"):
                return dict(held)
            raise OrderError(
                "The ship is in no squadron and no station has been given her; say 'keep "
                "station two cables astern of the <ship>' to name one."
            )
        return {"flag": None, "set": sq.id}
    m = _SPEC.match(low)
    if m is None:
        raise OrderError(
            f"'{rest}' is no station: say 'keep station two cables astern of the Harpy', "
            "'keep station on the larboard beam of the flagship', or 'keep your station'."
        )
    from freesail.orders.numbers import read_all

    n = m.group("n")
    cables = 2.0
    if n is not None:
        got = read_all(n)
        if got is None:
            raise OrderError(f"'{n}' is no number of cables in '{rest}'.")
        cables = float(got)
    who = m.group("flag").strip()
    root = _root(world)
    flag: str | None = None
    if who in ("the flagship", "the flag", "the commodore", "the admiral"):
        sq = _set_of(world)
        if sq is None:
            raise OrderError("The ship is in no squadron: name the ship to keep station on.")
        flag = sq.leader_of(_own_id(world)) or sq.commander
    else:
        key = who.removeprefix("the ").strip()
        v = root.vessels.find(key)
        if v is None and key in ("ship", "player's ship", "us"):
            flag = "the ship"
        elif v is None:
            raise OrderError(f"No ship named {who!r} is on the sea to keep station on.")
        else:
            flag = str(v.id)
    return {"flag": flag, "where": _BEARING_WORDS[m.group("where")], "cables": cables}


def _sighting_of(world: Any, flag: str) -> Any:
    lookout = getattr(world, "lookout", None)
    if lookout is None:
        return None
    for s in lookout.sightings:
        if s.seen_as == "sail" and str(s.feature.modern) == flag:
            return s
    return None


def _flag_course_deg(world: Any, flag: str, sighting: Any) -> float | None:
    """The flag's course: the squadron's own, which the officer of the watch knows (the
    course the flag signalled, the order of sailing), when the flag is the leader of her
    set; else as the tops have made it out (her heading to the nearest point once her rig
    is made out), else None (her own heading is taken, and the station laid along it, which
    is the loop that swung her across the line until the set's course was read)."""
    lookout = world.lookout
    sq = _set_of(world)
    in_set = sq is not None and (flag == sq.commander or flag == sq.leader_of(_own_id(world)))
    level = int((getattr(lookout, "_sail_said", None) or {}).get(sighting.feature.id, 0))
    if level < 1 and not in_set:
        return None
    root = _root(world)
    body = root.vessels.get(flag) if flag != "the ship" else root.vessels.player_shadow(root)
    if body is None:
        return None
    heading = float(getattr(body, "heading_deg", 0.0)) % 360.0
    return round(heading / RELAY_DEG) * RELAY_DEG % 360.0


def _offset(world: Any, spec: dict[str, Any], flag: str, flag_course: float) -> tuple[float, float]:
    """The station's offset from the flag in east and north metres."""
    wind_from = units.rad_to_deg(float(world.wind.direction_from)) % 360.0
    rel = units.rad_to_deg(units.wrap_pi(math.radians(wind_from - flag_course)))
    lee_sign = 1.0 if rel <= 0.0 else -1.0  # the wind from larboard: leeward to starboard
    where = spec.get("where")
    if where is None:
        sq = _set_of(world)
        own = _own_id(world)
        if sq is None:
            return 0.0, 0.0
        from freesail.world.squadrons import _rotate

        slots = sq.slots(_root(world))
        mine = slots.get(own)
        d = sq.division_of(own)
        if d is not None and d.detached and d.leader == flag:
            i = d.members.index(own) + 1 if own in d.members else 1
            return _rotate(-i * sq.interval_m, 0.0, flag_course, lee_sign)
        theirs = slots.get(flag, (0.0, 0.0))
        if mine is None:
            return 0.0, 0.0
        return _rotate(mine[0] - theirs[0], mine[1] - theirs[1], flag_course, lee_sign)
    d_m = float(spec.get("cables", 2.0)) * units.CABLE
    c = math.radians(flag_course)
    ahead = (math.sin(c), math.cos(c))
    starboard = (math.cos(c), -math.sin(c))
    if where == "astern":
        return -d_m * ahead[0], -d_m * ahead[1]
    if where == "ahead":
        return d_m * ahead[0], d_m * ahead[1]
    if where in ("windward", "leeward"):
        sign = -lee_sign if where == "windward" else lee_sign
        return sign * d_m * starboard[0], sign * d_m * starboard[1]
    side = 1.0 if where.startswith("starboard") else -1.0
    along = 0.0
    if where.endswith("quarter"):
        along = -d_m * math.cos(math.radians(45.0))
        d_side = d_m * math.sin(math.radians(45.0))
    elif where.endswith("bow"):
        along = d_m * math.cos(math.radians(45.0))
        d_side = d_m * math.sin(math.radians(45.0))
    else:
        d_side = d_m
    return (
        along * ahead[0] + side * d_side * starboard[0],
        along * ahead[1] + side * d_side * starboard[1],
    )


def _course_clamped(world: Any, course_deg: float) -> tuple[float, str]:
    """Never nearer the wind than she lies close-hauled, on the tack that points nearer."""
    from freesail.evolutions.scripts import close_hauled_true_angle

    wind_from = units.rad_to_deg(float(world.wind.direction_from)) % 360.0
    closest = units.rad_to_deg(close_hauled_true_angle(world.ship))
    off = units.rad_to_deg(units.wrap_pi(math.radians(course_deg - wind_from)))
    if abs(off) >= closest:
        return course_deg % 360.0, ""
    side = 1.0 if off >= 0 else -1.0
    return (wind_from + side * closest) % 360.0, ", as near the wind as she will lie"


def _work(world: Any, spec: dict[str, Any], by_order: bool) -> Result:
    ship = world.ship
    extra = ship.extra
    tick = int(world.clock.tick)
    held = extra.get("station") or {}
    flag = spec.get("flag")
    sq = _set_of(world)
    if flag is None:
        if sq is None:
            raise OrderError("The ship is in no squadron now; name the ship to keep station on.")
        flag = sq.leader_of(_own_id(world)) or sq.commander
    root = _root(world)
    flag_name = (
        getattr(root.ship, "name", "the ship")
        if flag == "the ship"
        else getattr(root.vessels.get(flag), "name", flag)
    )
    sighting = _sighting_of(world, flag)
    if sighting is None or sighting.estimate_m is None:
        words = f"Keeping station on {flag_name}: she is not in sight from the masthead."
        if by_order or held.get("said") != "lost":
            extra["station"] = dict(spec, flag=flag, since=held.get("since", tick), said="lost")
            return "station.lost", words, {"verb": "keep station", "level": 1, "flag": flag}
        return (
            "station.kept",
            words,
            {"verb": "keep station", "level": 1, "flag": flag, "routine": True},
        )
    own_heading = units.rad_to_deg(float(ship.heading)) % 360.0
    flag_course = _flag_course_deg(world, flag, sighting)
    course_known = flag_course is not None
    if flag_course is None:
        flag_course = own_heading
    b = math.radians(float(sighting.bearing_deg))
    est = float(sighting.estimate_m)
    fx, fy = est * math.sin(b), est * math.cos(b)
    ox, oy = _offset(world, spec, flag, flag_course)
    sx, sy = fx + ox, fy + oy
    distance = math.hypot(sx, sy)
    bearing = math.degrees(math.atan2(sx, sy)) % 360.0
    c = math.radians(flag_course)
    ux, uy = math.sin(c), math.cos(c)
    along = sx * ux + sy * uy  # the station ahead of her (+) or astern (-) by the flag's course
    tolerance = STATION_TOLERANCE_M
    straggle_m = (sq.straggler_nm if sq is not None else 1.0) * units.NAUTICAL_MILE
    out = distance > straggle_m
    was_out = bool(held.get("out"))
    lines: list[str] = []
    data: dict[str, Any] = {
        "verb": "keep station",
        "level": 1,
        "flag": flag,
        "distance_m": round(distance),
        "bearing_deg": round(bearing, 1),
        "in_station": distance <= tolerance,
    }
    # the helm: in station the flag's course; out of it the bearing of a point LEAD_M ahead
    # of the station along the flag's course, which near the station is the flag's course
    # with a small correction and far astern of it the station's own bearing (steering
    # for the station point itself chases a point moving at the flag's speed and swings
    # her across the line); ahead of her station the same aim, with sail shortened below
    if distance <= tolerance:
        course, clamp = flag_course, ""
        why = "in station, her course"
    else:
        # ahead of her station the lead grows by how far ahead, so that she edges back onto
        # the line while her sail drops her back and never crosses the flag's bows
        lead = LEAD_M + max(0.0, -along)
        ax, ay = sx + lead * ux, sy + lead * uy
        aim = math.degrees(math.atan2(ax, ay)) % 360.0
        course, clamp = _course_clamped(world, aim)
        why = "for the station" if along >= -SAIL_STEP_M else "ahead of her station, dropping back"
    # the helm is put again when the course differs by a point from the one last ORDERED
    # (not the one last computed, which creeps a few degrees a glass and would never turn
    # her), or when her head has strayed two points from it (an evolution or another
    # order has moved the helm)
    ordered = held.get("ordered")
    strayed = abs(units.rad_to_deg(units.wrap_pi(math.radians(course - own_heading))))
    turned = (
        ordered is None
        or abs(units.rad_to_deg(units.wrap_pi(math.radians(course - ordered)))) >= RELAY_DEG
        or strayed >= 2.0 * RELAY_DEG
    )
    helm_words = ""
    if turned:
        from freesail.orders.navigation import carry_out, judge_course, steer_degrees

        judged = judge_course(ship, math.radians(course), helm_order=False)
        if judged.branch == "helm":
            _, helm_words, _ = steer_degrees(ship, course)
        else:
            helm_words, _ = carry_out(ship, judged)
            helm_words += f" ({judged.words})"
    # the sail: ahead of her station she shortens a step at a time, a step a glass while she
    # is still ahead (the topgallants, then the courses, then the reefs: the sail order's
    # own ladder), up to SHORT_STEPS; back within half a step she sets plain sail again
    sail_words = ""
    short = int(held.get("short") or 0)
    last_sail = int(held.get("sail_tick", -(10**9)))
    if along < -SAIL_STEP_M and short < SHORT_STEPS and tick - last_sail >= SHORT_EVERY_S:
        from freesail.orders import handle

        try:
            _, sail_words, _ = handle(ship, "shorten sail")
            short += 1
            last_sail = tick
        except OrderError:
            pass
    elif short and along >= -SAIL_STEP_M / 2.0:
        from freesail.orders import handle

        try:
            _, sail_words, _ = handle(ship, "set plain sail")
            short = 0
            last_sail = tick
        except OrderError:
            pass
    elif along > 3.0 * SAIL_STEP_M and not held.get("pressed"):
        from freesail.orders import handle

        try:
            _, sail_words, _ = handle(ship, "make all sail")
            data["pressed"] = True
        except OrderError:
            pass
    pressed = bool(data.get("pressed") or (held.get("pressed") and distance > tolerance))
    extra["station"] = dict(
        spec,
        flag=flag,
        since=held.get("since", tick),
        course=course,
        ordered=course if turned else ordered,
        short=short,
        sail_tick=last_sail,
        pressed=pressed,
        out=out,
        said="kept",
        last=tick,
    )
    where = spec.get("where")
    station_words = (
        f"{_cables(float(spec.get('cables', 2.0)) * units.CABLE)} {where} of {flag_name}"
        if where
        else f"her station on {flag_name} in {sq.name if sq is not None else 'the line'}"
    )
    place = (
        "in station"
        if distance <= tolerance
        else f"{_cables(distance)} {'astern of' if along >= 0.0 else 'ahead of'} her station"
    )
    head = f"Keeping {station_words}: {flag_name} bears {units.point_name(b)} {_cables(est)}" + (
        f", steering {units.point_name(math.radians(flag_course))}" if course_known else ""
    )
    lines.append(f"{head}; {place}.")
    if turned:
        lines.append(
            f"The course {units.point_name(math.radians(course))} {why}{clamp}."
            + (f" {helm_words}" if helm_words else "")
        )
    if sail_words:
        lines.append(sail_words)
    kind = "station.kept"
    notable = by_order or turned or bool(sail_words)
    if out and not was_out:
        kind, notable = "sail.out_of_station", True
        lines.append("She is out of her station.")
    elif was_out and not out:
        kind, notable = "sail.in_station", True
        lines.append("She has regained her station.")
    if not notable:
        data["routine"] = True
    return kind, " ".join(lines), data


def _cables(m: float) -> str:
    from freesail.world.geo import distance_words

    return distance_words(m)


def execute(ship: Any, order: Any) -> Result:
    """`keep station ...` from the ship's grammar (`navigation.execute` hands it here)."""
    from freesail.orders.navigation import _world_with_lookout

    world = _world_with_lookout(ship)
    spec = _parse(world, order.object or "")
    return _work(world, spec, by_order=True)


def keep_station_minute(world: Any) -> None:
    """Nothing: the books give `keep your station` every two minutes (the `in company`
    book of every role), and the order does the work; kept as the seam for a runner that
    would work it of itself."""
    return None


def station_reading(world: Any) -> dict[str, Any] | None:
    """`the station` reading: her station as last kept (the flag, the offset, the last
    distance and bearing), or the set's slot with no order yet given; None in no set and
    with no station ordered."""
    extra = getattr(getattr(world, "ship", None), "extra", None) or {}
    held = extra.get("station")
    sq = _set_of(world)
    if not held and sq is None:
        return None
    root = _root(world)
    out: dict[str, Any] = {}
    if held:
        flag = held.get("flag")
        name = (
            getattr(root.ship, "name", "the ship")
            if flag == "the ship"
            else getattr(root.vessels.get(flag), "name", flag)
        )
        where = held.get("where")
        out["flag"] = name
        out["station"] = (
            f"{_cables(float(held.get('cables', 2.0)) * units.CABLE)} {where} of {name}"
            if where
            else f"her station on {name} in the set"
        )
        if held.get("said") == "lost":
            out["words"] = f"{out['station']}; the flag not in sight"
            out["in_station"] = False
        elif held.get("distance_m") is not None or held.get("course") is not None:
            out["in_station"] = not held.get("out")
            out["words"] = out["station"] + ("; out of station" if held.get("out") else "; kept")
        else:
            out["words"] = out["station"]
    else:
        own = _own_id(world)
        flag = sq.leader_of(own) or sq.commander
        name = (
            getattr(root.ship, "name", "the ship")
            if flag == "the ship"
            else getattr(root.vessels.get(flag), "name", flag)
        )
        out["flag"] = name
        out["station"] = f"her station on {name} in {sq.name}, not yet taken up"
        out["words"] = out["station"]
        out["in_station"] = False
    return out
