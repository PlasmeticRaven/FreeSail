"""The navigation orders (spec M5 §15; package 33a): what the captain says to the master.

    heave the log                   the log hove now (it is hove hourly of itself)
    heave the lead                  the hand lead, to twenty fathoms
    heave the deep-sea lead         the deep-sea lead, to a hundred and twenty (the key
                                    `heave the deep sea lead`, as the parser normalises it)
    take a bearing of <mark>        a mark in sight, or "the land", "the light"; a transit
    take a fix [by <mark> and <mark> [and <mark>]]
                                    cross bearings of two or three charted marks in sight,
                                    the account set at their crossing (package 37d)
    work up the reckoning           the day's work on demand
    observe the sun                 the noon sight by order, at noon
    set the reckoning to <lat> <long>   the captain overrides the master
    allow <n> knots of set to <direction>   the captain's own set in the traverse, in the
                                    place of the master's tide until it is handed back
    allow no set                    the captain's word that there is none
    allow the tide by the book      the tide handed back to the master (package 37e)
    shape a course for <place>      the course from the reckoning to a place of the chart,
                                    made good against the tide the master allows (package
                                    37e), with the charted dangers and the land its line
                                    passes (packages 33b and 37e)

and the longitude's (spec M5 §14; package 33b):

    take a sight for the longitude  the time sight against the chronometer
    take a lunar [of the sun | of <star>]   a set of distances; the result an hour later
    wind the chronometer            by order (daily of itself)
    compare the watches             the chronometer against the deck watch
    observe an amplitude            the variation by the sun's rising or setting
    observe an azimuth              the variation by the sun's bearing by day

Each is a verb of `data/vocabulary.yaml` with the object `navigation`: the imperative
grammar takes the words after the verb as they are (`grammar.parse`), and this module
carries the order out through the World's navigation (`ship.extra["navigation"]`,
`freesail.world.reckoning.Navigation`), which keeps the reckoning and writes the lines.
A ship on the endless plane, with no position, has no reckoning and every order here is
refused in words. `orders.handle` hands an order with this object here.
"""

from __future__ import annotations

import math
import re
from typing import Any

from freesail import units
from freesail.orders import errors
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.world.geo import name_words, parse_position

__all__ = ["NO_RECKONING_WORDS", "check", "execute", "mark_in_sight", "where_is"]

NO_RECKONING_WORDS = (
    "No reckoning is kept in this ship: the scenario gives her no position, and there is "
    "no sea to be lost on."
)

Result = tuple[str, str, dict[str, Any]]

_SET_RE = re.compile(
    r"^(?P<n>[\w\s./]+?)\s+(?:knots?|kn)\s+(?:of\s+)?set\s+(?:to(?:ward|wards)?\s+(?:the\s+)?)?"
    r"(?P<dir>.+)$"
)
_NO_SET = {"no set", "none", "nothing", "no", "no set at all"}
# `allow the tide by the book` (package 37e): the words after `allow` (or `allow for`)
# that hand the tide back to the master; `work the tide yourself` and its like are verbs
# of their own in the vocabulary and reach the same order.
_BY_THE_BOOK = {
    "the tide by the book",
    "the tide",
    "the tide by the directions",
    "the tide by the epitome",
    "the master's tide",
    "the masters tide",
    "the tide as the books give it",
    "the tide yourself",
    "by the book",
}


def _whose(ship: Any, text: str) -> str:
    """A line of the master's that says "the captain's order", said as the order's own
    giver's when a station gave it under the captain's word (package 37g, item 10: the
    officer of the watch's order is logged as his). The captain's own lines are as they
    were."""
    from freesail.orders.crew import whose_order

    whose = whose_order(ship)
    if whose == "the captain's":
        return text
    return text.replace("the captain's order", f"{whose} order")


def _navigation(ship: Any) -> Any:
    nav = (getattr(ship, "extra", None) or {}).get("navigation")
    if nav is None:
        raise OrderError(NO_RECKONING_WORDS)
    return nav


def _knots(text: str) -> float:
    """A number of knots of set ('one', 'half a', 'a knot and a half', '1.5', 'one and a
    quarter'), by the one reader for numbers (`orders.numbers`; package 37l); 'no' is
    none."""
    from freesail.orders import numbers

    t = " ".join(text.strip().lower().replace("-", " ").split())
    if t == "no":
        return 0.0
    t = t.replace(" knot and a half", " and a half").removesuffix(" knot")
    value = numbers.read_all(t)
    if value is None:
        raise OrderError(
            f"'{text}' is not a number of knots; say 'allow one knot of set to the east'."
        )
    return value


def _course(words: str) -> float | None:
    """A direction in words, with its half or quarter point (package 37l), in radians;
    None when the words are no direction; refused in words when a fraction in them cannot
    be read."""
    try:
        return units.parse_course(words)
    except units.CourseError as e:
        raise OrderError(str(e)) from None


def _position_in(words: str) -> Any:
    """A position in the words ('48 20 N 4 36 W'), or None for a place's name."""
    try:
        return parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", words))
    except ValueError:
        return None


# A chaser keeps the chase on a steady compass bearing (Luce 1884 p. 553: "by constantly
# keeping the chase on the same compass bearing, the chaser will attain the chase in the
# shortest time possible"; Luce 1866 ch. XXXIII, 'Chasing': the officers "should
# constantly take the bearings"). The first order steers her bearing. Each order after
# it, for the same sail, reads how the bearing has drawn since the last and works the
# lead that brings the drift to nothing, as the master would on the slate: the chase's
# way across the line of sight is the lookout's estimate of her distance times the rate
# the bearing draws, together with his own way across it on the course he has been
# steering; the lead off her bearing is the angle whose sine is that over his own speed.
# Everything in it is his (the bearing, the glass, the estimate, which is a third out at
# the worst, his log and his course); the lead is capped (judgement: a bearing that
# swings fast is a close pass, and the lead would otherwise put her head anywhere), and
# the course is never nearer the wind than she lies close-hauled, when she is put
# close-hauled on the tack nearer the course (judgement).
CHASE_LEAD_MAX_DEG = 45.0
CHASE_STEADY_DEG = 0.5  # a drift below this is 'the bearing steady'
CHASE_MIN_INTERVAL_S = 60.0  # two orders within a minute read no drift


def _chase_course(world: Any, sighting: Any) -> tuple[float, str]:
    """The course to steer for a chase, and the words of the bearing's drift and the lead;
    the courses are degrees true."""
    from freesail.evolutions.scripts import close_hauled_true_angle

    lookout = world.lookout
    chases = getattr(lookout, "_chases", None)
    if chases is None:
        chases = lookout._chases = {}
    fid = sighting.feature.id
    bearing = float(sighting.bearing_deg)
    tick = int(world.clock.tick)
    heading_deg = units.rad_to_deg(float(world.ship.heading)) % 360.0
    last = chases.get(fid)
    chases[fid] = (tick, bearing)
    words = ""
    course = bearing
    if last is not None and tick - last[0] >= CHASE_MIN_INTERVAL_S:
        drift = units.rad_to_deg(units.wrap_pi(math.radians(bearing - last[1])))
        if abs(drift) < CHASE_STEADY_DEG:
            words = ", the bearing steady"
        else:
            way = (
                "aft"
                if (drift > 0) == (units.wrap_pi(math.radians(bearing - heading_deg)) < 0)
                else "forward"
            )
            words = f", drawing {way} {abs(drift):.0f} degrees since the last"
            lead = drift
            dyn = getattr(world.ship, "dyn", None)
            speed = float(dyn.speed) if dyn is not None else 0.0
            estimate = getattr(sighting, "estimate_m", None)
            if estimate and speed > 0.1:
                rate = math.radians(drift) / float(tick - last[0])  # rad/s, clockwise
                across = float(estimate) * rate / speed + math.sin(
                    math.radians(heading_deg - bearing)
                )
                lead = units.rad_to_deg(math.asin(max(-0.95, min(0.95, across))))
            lead = max(-CHASE_LEAD_MAX_DEG, min(CHASE_LEAD_MAX_DEG, lead))
            course = (bearing + lead) % 360.0
            side = "starboard" if lead > 0 else "larboard"
            words += f", the course led {abs(lead):.0f} degrees to {side} of her"
    # never nearer the wind than she lies close-hauled
    wind_from = units.rad_to_deg(float(world.wind.direction_from)) % 360.0
    closest = units.rad_to_deg(close_hauled_true_angle(world.ship))
    off = units.rad_to_deg(units.wrap_pi(math.radians(course - wind_from)))
    if abs(off) < closest:
        # on the tack she is on: her head's side of the wind's eye (a chase dead to
        # windward is not a reason to put her about every glass)
        side = 1.0 if units.wrap_pi(math.radians(heading_deg - wind_from)) >= 0 else -1.0
        course = (wind_from + side * closest) % 360.0
        words += ", as near the wind as she will lie"
    return course, words


# A course shaped nearer the wind than close-hauled and half a point is not laid
# (package 35's rule for the pilot's course, `evolutions.scripts`): she is kept full and
# by on the tack that points nearer the course, put about for it when it is the other,
# and the line says so; a course laid but reached by a turn through the wind's eye is
# worn round for (the book gives the course again after, as the cruise's does).
COURSE_NOT_LAID_MARGIN_POINTS = 0.5
# a square-rigged ship with this much way on is worn for a course through the wind's wake
# (a knot: under that she is drifting, and a wear would not come round)
WEAR_FOR_IT_MIN_MS = 0.5


def _course_not_laid(ship: Any, heading: float) -> tuple[str, str] | None:
    """When a course shaped lies too near the wind to be laid: (the words, the helm order
    that stands in for it: 'keep her full and by' on the tack that points nearer the
    course, 'tack' when that is the other tack); None when the course is laid."""
    from freesail.evolutions.scripts import close_hauled_true_angle
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    wind = getattr(world, "wind", None)
    if wind is None:
        return None
    wind_from = float(wind.direction_from)
    closest = close_hauled_true_angle(ship)
    off = abs(units.wrap_pi(heading - wind_from))
    dyn = getattr(ship, "dyn", None)
    if off >= closest + COURSE_NOT_LAID_MARGIN_POINTS * units.POINT:
        # laid; but a helm put over for it turns her the shorter way, and when the wind's
        # eye lies in that arc she is taken aback and lies in irons (a frigate chasing a
        # cutter down wind and shaping back for her station, found on the way): she is
        # worn round instead (Luce 1866 ch. XXIV), and the course is given again after.
        # The same for a square-rigged ship under sail whose arc passes through the
        # wind's wake, dead to leeward: the helm alone turns her by the stern with the
        # yards still braced for the old tack, and as the wind comes over the other
        # quarter every square sail is laid aback (the cruise's frigate at 07:30 on the
        # 13th, chasing the Palinure 175 degrees round, and again shaping for her station
        # from the cutter's hail: the fold-in of m5c-c, the audit's C1 and C2). That turn
        # is a wear, and wearing her works the yards round with her head. A fore-and-after
        # (one mast with yards) gybes by the helm, her booms swinging over, as she always
        # has; a ship with no square sail set, or drifting with no way, has nothing to be
        # worn for
        if dyn is not None and float(getattr(dyn, "speed", 0.0)) > 0.1:
            from freesail.evolutions.scripts import _masts_with_yards

            now = float(dyn.heading)
            turn = units.wrap_pi(heading - now)
            marks = [(wind_from, "lying across the wind's eye from her head")]
            square_set = any(sl.is_set and sl.cls == "square" for sl in ship.sails.values())
            if (
                len(_masts_with_yards(ship)) >= 2
                and square_set
                and float(dyn.speed) > WEAR_FOR_IT_MIN_MS
            ):
                marks.append(
                    (wind_from + math.pi, "lying across the wind from her head, by the stern")
                )
            for mark, words in marks:
                to_mark = units.wrap_pi(mark - now)
                if abs(turn) > closest and (turn > 0) == (to_mark > 0) and abs(to_mark) < abs(turn):
                    return (
                        f"{units.format_heading(heading)} {words}, she is worn round for it",
                        "wear ship",
                    )
        return None
    # the wind over the starboard side: her head lies the closest angle to the left of
    # the wind's eye; over the larboard side, to the right
    starboard = units.wrap_2pi(wind_from - closest)
    larboard = units.wrap_2pi(wind_from + closest)
    nearer = (
        "starboard"
        if abs(units.wrap_pi(heading - starboard)) <= abs(units.wrap_pi(heading - larboard))
        else "larboard"
    )
    said = f"{units.format_heading(heading)} lying too near the wind to be laid"
    if dyn is not None and getattr(dyn, "tack", None) == nearer:
        return f"{said}, she is kept full and by on the {nearer} tack", "keep her full and by"
    return f"{said}, she is put about for the {nearer} tack", "tack"


def _helm_for(ship: Any, not_laid: tuple[str, str]) -> tuple[str, str, dict[str, Any]]:
    """The helm order that stands in for a course not laid or across the eye, given; a
    tack refused because she is not by the wind brings her by the wind instead (the book
    gives the course again at its next glass, and the tack is accepted then)."""
    from freesail.orders import handle

    words, order = not_laid
    try:
        _, helm_text, helm_data = handle(ship, order)
    except OrderError as exc:
        if order != "tack" or "close-hauled" not in str(exc):
            raise
        _, helm_text, helm_data = handle(ship, "keep her full and by")
        words = words.replace("she is put about for", "she is brought by the wind to go about for")
    return words, helm_text, helm_data


def _world_with_lookout(ship: Any) -> Any:
    """The World with a lookout at the masthead (a chart), for the other sail's orders;
    refused in words on the plane."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    if world is None or getattr(world, "lookout", None) is None:
        raise OrderError(
            "No lookout is kept: the scenario gives her no chart, and there is no sea for "
            "another sail to be on."
        )
    return world


def _sail_named(verb_phrase: str) -> str | None:
    """Which sail a phrase names of itself: 'make out the brig' names the brig; 'make her
    out' names none (the nearest)."""
    words = verb_phrase.split()
    for word in ("brig", "cutter", "ship", "schooner", "frigate", "stranger", "sail"):
        if word in words:
            return word
    return None


_FIX_LEAD = re.compile(r"^(?:by|on|of|from|with|upon)\s+", re.IGNORECASE)
_FIX_SPLIT = re.compile(r"\s*,\s*(?:and\s+)?|\s+and\s+", re.IGNORECASE)


def _fix_names(nav: Any, rest: str) -> list[str]:
    """The marks a fix is to be taken by, as the words after `take a fix` name them
    ('by the Lizard and the Manacles', 'by the Lizard, Black Head and St Anthony's
    light'): each the name of a mark in sight by any of its words (`mark_in_sight`, with
    its refusals); none for a bare `take a fix`. The grammar hands the words on without
    their commas, so a run of words between two 'and's that is no one mark is divided
    where each part is a mark in sight ('Black Head St Anthony's Head and the Deadman');
    a name that holds an 'and' of its own ('the Penwin and the Vaze') is one mark."""
    words = _FIX_LEAD.sub("", rest.strip().rstrip("."))
    if not words:
        return []
    lookout = getattr(nav.world, "lookout", None)

    def known(text: str) -> str | None:
        """The name in sight a run of words means, or None."""
        if lookout is None or not text:
            return None
        seen = lookout.find(text)
        if seen is not None:
            return str(seen.feature.name)  # by the name the lookout says
        try:
            return mark_in_sight(nav, text, refuse=False)
        except OrderError:
            return None

    def divided(text: str) -> list[str] | None:
        """A run of words as two or three marks in sight, said one after another."""
        tokens = text.split()
        n = len(tokens)
        for i in range(1, n):
            head, tail = known(" ".join(tokens[:i])), known(" ".join(tokens[i:]))
            if head and tail:
                return [head, tail]
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                three = [
                    known(" ".join(tokens[:i])),
                    known(" ".join(tokens[i:j])),
                    known(" ".join(tokens[j:])),
                ]
                if all(three):
                    return [name for name in three if name]
        return None

    whole = known(words)
    if whole is not None and " and " not in f" {words.lower()} ".replace(",", " "):
        return [whole]
    names: list[str] = []
    for part in (w.strip() for w in _FIX_SPLIT.split(words)):
        if not part:
            continue
        one = known(part)
        if one is not None:
            names.append(one)
            continue
        several = divided(part)
        # not in sight by any division: left as said, for the refusal that names it
        names.extend(several if several else [mark_in_sight(nav, part) or part])
    if whole is not None and len(set(names)) < 2:
        return [whole]  # 'the Penwin and the Vaze': one mark with an 'and' of its own
    return list(dict.fromkeys(names))


# ---------------------------------------------------------------------------
# A point off a place of the chart (package 37l): `shape a course for a mile west of
# Ushant`, `... for two miles south of the Lizard`, `... for half a league NW of Bas`
# ---------------------------------------------------------------------------

_OFF_UNITS_M = {
    "cable": units.CABLE,
    "cables": units.CABLE,
    "mile": units.NAUTICAL_MILE,
    "miles": units.NAUTICAL_MILE,
    "league": 3.0 * units.NAUTICAL_MILE,
    "leagues": 3.0 * units.NAUTICAL_MILE,
}


def _off_a_place(world: Any, said: str) -> tuple[Any, str] | None:
    """A point laid off from a place of the chart by a distance and a point of the
    compass ('a mile west of ushant'): (the position, the words for the log); None when
    the words are not of that form; refused in words when they are and the place is not
    the chart's or the point is no point."""
    from freesail.orders import numbers
    from freesail.world.geo import destination

    words = said.lower().replace("-", " ").split()
    got = numbers.read(words, 0)
    if got is None:
        return None
    value, used = got
    unit = words[used] if used < len(words) else ""
    if unit not in _OFF_UNITS_M:
        return None
    rest = words[used + 1 :]
    if rest[:2] == ["to", "the"]:
        rest = rest[2:]
    elif rest[:1] == ["to"]:
        rest = rest[1:]
    if "of" not in rest and "off" not in rest:
        return None
    k = next(i for i, w in enumerate(rest) if w in ("of", "off"))
    point_words, place = rest[:k], " ".join(rest[k + 1 :])
    if not point_words or not place:
        return None
    toward = _course(" ".join(point_words))
    if toward is None:
        raise OrderError(
            f"'{' '.join(point_words)}' is not a point of the compass; say 'shape a course "
            f"for a mile west of {place}'."
        )
    chart = getattr(world, "chart", None)
    feature = chart.find_feature(place) if chart is not None else None
    if feature is None:
        raise OrderError(_no_place_words(chart, place))
    target = destination(feature.position, units.rad_to_deg(toward), value * _OFF_UNITS_M[unit])
    distance = " ".join(words[: used + 1])
    return target, f"{distance} {units.point_name(toward, full=True)} of {feature.name}"


def _no_place_words(chart: Any, place: str) -> str:
    """The refusal for a place the chart has not got, with the nearest names it has."""
    if chart is None:
        return "No chart of these waters: there is no place to shape a course for."
    names = sorted({f.name for f in chart.features.values() if f.kind != "transit"})
    near = errors.nearest(
        " ".join(name_words(place)), [" ".join(name_words(n)) for n in names], n=2, cutoff=0.75
    )
    hint = [n for n in names if " ".join(name_words(n)) in near]
    if hint:
        return f"The chart has no place named {place!r}; did you mean {errors.join_names(hint)}?"
    return f"The chart has no place named {place!r}."


# ---------------------------------------------------------------------------
# Where a mark is (package 37l; game 10, `where is ushant`: "Nobody aboard answers to
# 'ushant'"): in sight, the lookout's bearing and estimate; else by account, from the
# master's position (never the truth's) to the chart's place
# ---------------------------------------------------------------------------


def where_is(world: Any, said: str) -> str | None:
    """`where is <mark>`: the words for a mark of the chart, or None when the chart has
    no such name. In sight, its bearing by the master's compass and the lookout's
    estimate; not in sight, its bearing and distance from the account, said as the
    account's."""
    from freesail.world.reckoning import miles_words

    chart = getattr(world, "chart", None)
    nav = getattr(world, "navigation", None)
    if chart is None or nav is None:
        return None
    feature = chart.find_feature(said)
    if feature is None:
        words = name_words(said)
        if words and words[0] == "the":
            words = words[1:]
        found = [
            f
            for f in chart.features.values()
            if f.kind != "transit" and words and set(words) <= set(name_words(f.name))
        ]
        if len({f.id for f in found}) != 1:
            return None
        feature = found[0]
    seen = nav.bearing_reading(feature.name)
    if seen is not None:
        return f"{_head(feature.name)}: in sight, bearing {seen['words']}"
    from freesail.world.geo import bearing_and_distance

    here = nav.account_now()
    bearing, metres = bearing_and_distance(here, feature.position)
    point = units.point_name(math.radians(bearing))
    miles = miles_words(metres / units.NAUTICAL_MILE)
    return f"{_head(feature.name)}: not in sight; by account it bears {point}, {miles}"


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


# ---------------------------------------------------------------------------
# A navigation order read whole without carrying it out (package 37l): a standing order's
# action is read when it is given, so that a mark the chart has not got or a place it
# does not name is refused at the giving and not met at sea
# ---------------------------------------------------------------------------

# The words for a mark that are the lookout's own, or a sail's, never a name of the chart
_MARK_WORDS = frozenset(
    {
        "land",
        "the land",
        "shore",
        "the shore",
        "coast",
        "the coast",
        "headland",
        "nearest land",
        "the nearest land",
        "light",
        "the light",
        "nearest light",
        "the nearest light",
        "sail",
        "the sail",
        "stranger",
        "the stranger",
        "brig",
        "the brig",
        "cutter",
        "the cutter",
        "schooner",
        "the schooner",
        "ship",
        "the ship",
        "frigate",
        "the frigate",
        "pilot cutter",
        "the pilot cutter",
    }
)


def _chart_mark(chart: Any, said: str) -> bool:
    """Whether the words name a mark of the chart: by its name whole, or by words that
    are all among one feature's name's words ('manacle' for Manacle Point)."""
    if chart.find_feature(said) is not None:
        return True
    words = [w for w in name_words(said) if w not in ("the", "of", "and")]
    if not words:
        return False
    return any(set(words) <= set(_name_words(f.name)) for f in chart.features.values())


def check(ship: Any, order: Order) -> None:
    """Read a navigation order whole, without carrying it out: a mark, the marks of a
    fix, a place, a position or an allowance in its words that cannot be read, refused
    in words now. Nothing that depends on the moment (what is in sight, the sky, the
    hour) is judged here: that is the order's own business when it is carried out. On a
    ship with no chart nothing is read (the order is refused in words when it fires, as
    it always was)."""
    from freesail.orders.prompt import world_of

    verb = order.verb
    rest = (order.object or "").strip()
    world = world_of(ship)
    chart = getattr(world, "chart", None) if world is not None else None
    if verb == "set the reckoning to":
        try:
            parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", rest))
        except ValueError:
            raise OrderError(
                f"'{rest}' is not a position; say 'set the reckoning to 49 52 N 6 10 W'."
            ) from None
        return
    if verb == "allow":
        low = " ".join(rest.lower().rstrip(".").split())
        if not rest or low in _BY_THE_BOOK or low in _NO_SET or low.startswith("no set"):
            return
        m = _SET_RE.match(low)
        if m is None:
            raise OrderError(
                "Say how much set and which way: 'allow one knot of set to the east'; or "
                "'allow no set'; or 'allow the tide by the book'."
            )
        _knots(m.group("n"))
        if _course(m.group("dir")) is None:
            raise OrderError(f"'{m.group('dir')}' is not a compass point to allow the set toward.")
        return
    if chart is None:
        return
    if verb == "take a bearing of":
        if not rest:
            raise OrderError(
                "Take a bearing of what? Name a mark of the chart, or say 'the land' or "
                "'the light'."
            )
        key = " ".join(name_words(rest))
        if key in _MARK_WORDS or _chart_mark(chart, rest):
            return
        raise OrderError(
            _no_place_words(chart, rest).replace("no place named", "no mark named")
            + " A bearing is taken of a mark of the chart by its name, of the land or of "
            "the light."
        )
    if verb == "take a fix":
        words = _FIX_LEAD.sub("", rest.strip().rstrip("."))
        if not words:
            return
        for part in (w.strip() for w in _FIX_SPLIT.split(words)):
            if part and not _chart_mark(chart, part) and not _chart_mark(chart, words):
                raise OrderError(
                    f"'{part}' names no mark of the chart. Say 'take a fix', and the master "
                    "takes the marks in sight that cut best, or 'take a fix by the Lizard "
                    "and the Manacles'."
                )
        return
    if verb == "shape a course for":
        if not rest:
            raise OrderError("Shape a course for where? Name a place of the chart.")
        if _position_in(rest) is not None or _off_a_place(world, rest) is not None:
            return
        if chart.find_feature(rest) is None:
            raise OrderError(_no_place_words(chart, rest))
        return


def execute(ship: Any, order: Order) -> Result:
    """Carry out a navigation order. The verb is the vocabulary's key."""
    verb = order.verb
    rest = (order.object or "").strip()
    if verb == "heave the log":
        nav = _navigation(ship)
        line = nav.heave_log(automatic=False) or "The log hove."
        return "evolution.started", line, {"verb": verb, "level": 1, "subjects": ["her"]}
    if verb in ("heave the lead", "heave the deep sea lead"):
        nav = _navigation(ship)
        deep = verb == "heave the deep sea lead"
        line = nav.heave_lead(deep=deep)
        return "evolution.started", line, {"verb": verb, "level": 1, "subjects": ["her"]}
    if verb == "take a bearing of":
        if not rest:
            raise OrderError(
                "Take a bearing of what? Name a mark in sight, or say 'the land' or 'the light'."
            )
        nav = _navigation(ship)
        text, data = nav.take_bearing(mark_in_sight(nav, rest) or rest)
        return "bearing.taken", text, {"verb": verb, "level": 1, "mark": rest} | data
    if verb == "take a fix":
        # cross bearings of two or three charted marks in sight, and the account set at
        # their crossing (package 37d); unnamed, the master takes those that cut best
        nav = _navigation(ship)
        names = _fix_names(nav, rest)
        text, data = nav.take_fix(names or None)
        return "reckoning.fix", text, {"verb": verb, "level": 1, "by": names} | data
    if verb == "work up the reckoning":
        nav = _navigation(ship)
        text, data = nav.work_up()
        return "reckoning.worked", text, {"verb": verb, "level": 1} | data
    if verb == "observe the sun":
        nav = _navigation(ship)
        text, data = nav.observe_sun()
        kind = "reckoning.noon" if "noon" in data else "reckoning.sight"
        return kind, text, {"verb": verb, "level": 1} | data
    if verb == "set the reckoning to":
        nav = _navigation(ship)
        try:
            pos = parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", rest))
        except ValueError:
            raise OrderError(
                f"'{rest}' is not a position; say 'set the reckoning to 49 52 N 6 10 W'."
            ) from None
        text, data = nav.set_reckoning(pos)
        return "reckoning.set", _whose(ship, text), {"verb": verb, "level": 1} | data
    if verb == "allow the tide by the book":
        # the tide handed back to the master (package 37e)
        nav = _navigation(ship)
        text, data = nav.allow_tide_by_book()
        return "reckoning.set_allowance", text, {"verb": verb, "level": 1} | data
    if verb == "allow":
        nav = _navigation(ship)
        low = " ".join(rest.lower().rstrip(".").split())
        if low in _BY_THE_BOOK:
            text, data = nav.allow_tide_by_book()
            return "reckoning.set_allowance", text, {"verb": verb, "level": 1} | data
        if not rest or low in _NO_SET or low.startswith("no set"):
            text, data = nav.allow_set(0.0, None)
            return "reckoning.set_allowance", _whose(ship, text), {"verb": verb, "level": 1} | data
        m = _SET_RE.match(low)
        if m is None:
            raise OrderError(
                "Say how much set and which way: 'allow one knot of set to the east'; or "
                "'allow no set'; or 'allow the tide by the book', to hand the tide back to "
                "the master."
            )
        knots = _knots(m.group("n"))
        toward = _course(m.group("dir"))
        if toward is None:
            raise OrderError(f"'{m.group('dir')}' is not a compass point to allow the set toward.")
        text, data = nav.allow_set(knots, toward)
        return "reckoning.set_allowance", _whose(ship, text), {"verb": verb, "level": 1} | data
    if verb == "shape a course for":
        if not rest:
            raise OrderError("Shape a course for where? Name a place of the chart.")
        nav = _navigation(ship)
        pricked = _position_in(rest)
        off = _off_a_place(nav.world, rest) if pricked is None else None
        if pricked is not None:
            # a point pricked on the chart (package 36: the books' waypoints through the
            # Goulet and out of Falmouth), the course from the account as for a place
            from freesail.world.geo import format_position

            heading, words, shaped = nav.shape_for(pricked, format_position(pricked))
        elif off is not None:
            # a point off a place of the chart (package 37l; game 10, `shape a course for
            # a mile west of ushant`): laid off from the chart's place, and the course
            # shaped for it from the account as for any point on the chart
            target, said = off
            heading, words, shaped = nav.shape_for(target, said)
        else:
            heading, words, shaped = nav.shape_course(rest)
        from freesail.orders import handle

        not_laid = _course_not_laid(ship, heading)
        if not_laid:
            # the course lies nearer the wind than she will sail: said, not steered, and
            # she is kept full and by on the tack that points nearer it, put about for it
            # when that is the other tack (as the pilot's course is said and not steered,
            # package 35; the book's helm rules have no other guard)
            said, helm_text, helm_data = _helm_for(ship, not_laid)
            words = words.rstrip(".") + f"; {said}."
        else:
            _, helm_text, helm_data = handle(ship, f"steer {units.rad_to_deg(heading):.0f}")
        data = {"verb": verb, "level": 1, "place": rest, "heading": heading} | shaped
        data["helm"] = helm_data
        if not_laid:
            data["course_not_laid"] = True
        return "helm.set", f"{words} {helm_text}", data
    # other sail (spec M5 §25; package 36): the glass aloft, and the chase
    if verb == "make her out":
        world = _world_with_lookout(ship)
        which = rest or _sail_named(order.verb_phrase)
        text, data = world.lookout.make_out(world, which)
        return "lookout.made_out", text, {"verb": verb, "level": 1} | data
    if verb == "give chase":
        world = _world_with_lookout(ship)
        which = rest or _sail_named(order.verb_phrase)
        lookout = world.lookout
        sails = [s for s in lookout.sightings if s.seen_as == "sail"]
        if not sails:
            raise OrderError("No sail in sight to chase.")
        sighting = lookout.find(which) if which else None
        if which and sighting is None:
            raise OrderError(f"Nothing in sight answers to {which!r}; the strangers are listed.")
        if sighting is None:
            # the chase in hand is kept while she is in sight (a second sail nearer does
            # not take the helm from her); else the nearest sail
            chases = getattr(lookout, "_chases", None) or {}
            in_hand = [s for s in sails if s.feature.id in chases]
            sighting = min(in_hand or sails, key=lambda s: s.distance_m)
        from freesail.world.lookout import relative_words

        heading = float(world.ship.heading)
        relative = relative_words(math.radians(sighting.bearing_deg) - heading)
        point = units.point_name(math.radians(sighting.bearing_deg))
        who = lookout.sail_name(sighting.feature.id, sighting.feature.name)
        course, drift_words = _chase_course(world, sighting)
        from freesail.orders import handle

        across = _course_not_laid(ship, math.radians(course))
        if across:
            # the course lies across the wind's eye from her head: worn round for it
            said, helm_text, helm_data = _helm_for(ship, across)
            drift_words += f"; {said}"
        else:
            _, helm_text, helm_data = handle(ship, f"steer {course:.0f}")
        words = f"Gave chase to {who} {relative}, bearing {point}{drift_words}. {helm_text}"
        data = {
            "verb": verb,
            "level": 1,
            "id": sighting.feature.modern,
            "bearing_deg": round(sighting.bearing_deg, 1),
            "course_deg": round(course, 1),
            "relative": relative,
            "helm": helm_data,
        }
        return "helm.set", words, data
    # the longitude's orders (package 33b)
    if verb == "take a sight for the longitude":
        nav = _navigation(ship)
        text, data = nav.take_time_sight()
        return "reckoning.time_sight", text, {"verb": verb, "level": 1} | data
    if verb == "take a lunar":
        nav = _navigation(ship)
        line = nav.take_lunar(rest or None)
        return "evolution.started", line, {"verb": verb, "level": 1, "subjects": ["her"]}
    if verb == "wind the chronometer":
        nav = _navigation(ship)
        text, data = nav.wind_chronometer()
        return "chronometer.wound", text, {"verb": verb, "level": 1} | data
    if verb == "compare the watches":
        nav = _navigation(ship)
        text, data = nav.compare_watches()
        return "chronometer.compared", text, {"verb": verb, "level": 1} | data
    if verb in ("observe an amplitude", "observe an azimuth"):
        nav = _navigation(ship)
        text, data = nav.observe_variation(amplitude=verb == "observe an amplitude")
        return "reckoning.variation", text, {"verb": verb, "level": 1} | data
    raise OrderError(f"'{verb}' is not a navigation order this ship knows.")


# ---------------------------------------------------------------------------
# A mark in sight by any of its words (package 33c; playtest 13's cutter: "take a bearing
# of manacle" refused with Manacle Point in the list)
# ---------------------------------------------------------------------------

# The chart's kinds that are dangers, for the words of one not in sight.
_DANGER_KINDS = frozenset({"ledge", "rock", "drying", "shoal", "bank"})
# The lookout's own words for the nearest land or light (`Lookout.find`), never read as a
# mark's word ('land' is not Land's End).
_LOOKOUT_WORDS = frozenset(
    {"land", "shore", "coast", "headland", "nearest land", "light", "nearest light"}
)


def _name_words(name: str) -> list[str]:
    """A name's words as they are matched: lower case, no article, no punctuation."""
    words = name_words(name)
    return [w for w in words if w not in ("the", "of", "and")]


def mark_in_sight(nav: Any, said: str, refuse: bool = True) -> str | None:
    """The name of the mark in sight the words mean, for `take a bearing of <words>` and
    the reading `the bearing of <words>`: the words as said when the lookout knows them
    whole (`Lookout.find`: a name, 'the land', 'the light') or a transit of the chart
    names them; else the one mark in sight that has every word said among its name's
    words ('manacle' for Manacle Point). When two or more answer, or none does, refused
    in words that name them, or say that the feature the words name is the chart's and
    not in sight (the Manacles, the danger, are not Manacle Point), or the nearest name
    in sight; with `refuse` False, None instead of a refusal."""
    world = nav.world
    lookout = getattr(world, "lookout", None)
    if lookout is None or lookout.find(said) is not None:
        return said
    words = _name_words(said)
    if " ".join(words) in _LOOKOUT_WORDS:
        return said  # the lookout's own words ('the land', 'the light'): its refusal stands
    chart = getattr(world, "chart", None)
    features = list(chart.features.values()) if chart is not None else []
    if any(f.kind == "transit" and _name_words(f.name) == words for f in features):
        return said
    if not words:
        return said
    from freesail.world.lookout import SHORE_ID

    seen = [s for s in lookout.sightings if s.feature.id != SHORE_ID]
    # by the period's name the lookout says (the modern one is taken whole by `find`: the
    # Manacles' modern "Manacle Rocks" would make 'manacle' name two marks)
    matches = [s for s in seen if set(words) <= set(_name_words(s.feature.name))]
    if len({s.feature.id for s in matches}) == 1:
        return matches[0].feature.name
    if not refuse:
        return None
    heading = float(world.ship.heading)
    if matches:
        which = errors.join_names(
            [
                f"{s.feature.name} bearing {units.point_name(math.radians(s.bearing_deg))}"
                for s in matches
            ],
            "and",
        )
        raise OrderError(f"{len(matches)} marks in sight answer to '{said}': {which}; say which.")
    if not seen:
        return said  # the lookout's own refusal: nothing in sight, or the shore alone
    in_sight = lookout.reading(heading)["words"]
    named = [f for f in features if f.kind != "transit" and _name_words(f.name) == words]
    if named:
        f = named[0]
        verb = "are" if f.name.endswith("s") and not f.name.endswith("ss") else "is"
        what = "a danger of the chart" if f.kind in _DANGER_KINDS else "a mark of the chart"
        head = f"{f.name[:1].upper()}{f.name[1:]} {verb} not in sight ({what})"
        # a mark in sight whose words begin as these do is another feature: the Manacles
        # are not Manacle Point
        near = [
            s.feature.name
            for s in seen
            if any(w[:5] == x[:5] for w in _name_words(s.feature.name) for x in words)
        ]
        if near:
            be = "is" if len(near) == 1 else "are"
            head += f"; {errors.join_names(near, 'and')}, in sight, {be} another feature"
        raise OrderError(f"{head}; in sight: {in_sight}.")
    near = errors.nearest(
        " ".join(words), [" ".join(_name_words(s.feature.name)) for s in seen], n=2
    )
    names = [s.feature.name for s in seen if " ".join(_name_words(s.feature.name)) in near]
    if not names:
        return said  # the lookout's own refusal, with what is in sight
    head = said[:1].upper() + said[1:]
    raise OrderError(
        f"{head} is not in sight; did you mean {errors.join_names(names)}? In sight: {in_sight}."
    )
