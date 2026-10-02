"""The navigation orders (spec M5 §15; package 33a): what the captain says to the master.

    heave the log                   the log hove now (it is hove hourly of itself)
    heave the lead                  the hand lead, to twenty fathoms
    heave the deep-sea lead         the deep-sea lead, to a hundred and twenty (the key
                                    `heave the deep sea lead`, as the parser normalises it)
    take a bearing of <mark>        a mark in sight, or "the land", "the light"; a transit
    work up the reckoning           the day's work on demand
    observe the sun                 the noon sight by order, at noon
    set the reckoning to <lat> <long>   the captain overrides the master
    allow <n> knots of set to <direction>   the master's allowance in the traverse
    shape a course for <place>      the course from the reckoning to a place of the chart,
                                    with the charted dangers its line passes (package 33b)

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
from freesail.world.geo import parse_position

__all__ = ["NO_RECKONING_WORDS", "execute", "mark_in_sight"]

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
_NUMBER_WORDS = {
    "no": 0.0,
    "half": 0.5,
    "half a": 0.5,
    "a": 1.0,
    "one": 1.0,
    "a knot": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "a quarter": 0.25,
    "quarter": 0.25,
}


def _navigation(ship: Any) -> Any:
    nav = (getattr(ship, "extra", None) or {}).get("navigation")
    if nav is None:
        raise OrderError(NO_RECKONING_WORDS)
    return nav


def _knots(text: str) -> float:
    t = text.strip().lower()
    if t in _NUMBER_WORDS:
        return _NUMBER_WORDS[t]
    m = re.match(r"^(\d+(?:\.\d+)?)(?:\s+and\s+a\s+half)?$", t)
    if m:
        return float(m.group(1)) + (0.5 if "half" in t else 0.0)
    for words, value in _NUMBER_WORDS.items():
        if t.startswith(words + " and a half"):
            return value + 0.5
    raise OrderError(f"'{text}' is not a number of knots; say 'allow one knot of set to the east'.")


def _position_in(words: str) -> Any:
    """A position in the words ('48 20 N 4 36 W'), or None for a place's name."""
    try:
        return parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", words))
    except ValueError:
        return None


def _shape_for_position(nav: Any, pricked: Any) -> tuple[float, str]:
    """`shape a course for <position>`: the course from the account brought up to now to
    a point pricked on the chart, with the charted dangers its line passes, as
    `Navigation.shape_course` gives it for a named place (never from the truth)."""
    from freesail.world.chart import DANGER_PASS_NM
    from freesail.world.geo import bearing_and_distance, format_position
    from freesail.world.reckoning import miles_words

    world = nav.world
    now = nav.account_now()
    bearing, dist = bearing_and_distance(now, pricked)
    heading = math.radians(bearing)
    words = (
        f"Shaped a course for {format_position(pricked)}: {units.point_name(heading)} by "
        f"account, {miles_words(dist / units.NAUTICAL_MILE)}"
    )
    chart = getattr(world, "chart", None)
    if chart is not None:
        passes = chart.line_passes(now, pricked, DANGER_PASS_NM * units.NAUTICAL_MILE)
        crossed = [f.name for f, _off, crosses in passes if crosses]
        near = [f.name for f, _off, crosses in passes if not crosses]
        said = []
        if crossed:
            said.append(f"the line crosses {errors.join_names(crossed, 'and')}")
        if near:
            said.append(f"the line passes {errors.join_names(near, 'and')} within a mile")
        if said:
            words += "; " + " and ".join(said)
    return heading, words + "."


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
        side = 1.0 if off >= 0 else -1.0
        if abs(off) < 1e-6:
            side = 1.0 if units.wrap_pi(math.radians(bearing - heading_deg)) >= 0 else -1.0
        course = (wind_from + side * closest) % 360.0
        words += ", as near the wind as she will lie"
    return course, words


# A course shaped nearer the wind than close-hauled and half a point is not laid
# (package 35's rule for the pilot's course, `evolutions.scripts`): she is kept full and
# by on the tack that points nearer the course, put about for it when it is the other,
# and the line says so; a course laid but reached by a turn through the wind's eye is
# worn round for (the book gives the course again after, as the cruise's does).
COURSE_NOT_LAID_MARGIN_POINTS = 0.5


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
        # worn round instead (Luce 1866 ch. XXIV), and the course is given again after
        if dyn is not None and float(getattr(dyn, "speed", 0.0)) > 0.1:
            now = float(dyn.heading)
            turn = units.wrap_pi(heading - now)
            to_eye = units.wrap_pi(wind_from - now)
            if abs(turn) > closest and (turn > 0) == (to_eye > 0) and abs(to_eye) < abs(turn):
                return (
                    f"{units.format_heading(heading)} lying across the wind's eye from her "
                    "head, she is worn round for it",
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
        return "reckoning.set", text, {"verb": verb, "level": 1} | data
    if verb == "allow":
        nav = _navigation(ship)
        low = rest.lower()
        if not rest or low in _NO_SET or low.startswith("no set"):
            text, data = nav.allow_set(0.0, None)
            return "reckoning.set_allowance", text, {"verb": verb, "level": 1} | data
        m = _SET_RE.match(low)
        if m is None:
            raise OrderError(
                "Say how much set and which way: 'allow one knot of set to the east', or "
                "'allow no set'."
            )
        knots = _knots(m.group("n"))
        toward = units.parse_compass_point(m.group("dir"))
        if toward is None:
            raise OrderError(f"'{m.group('dir')}' is not a compass point to allow the set toward.")
        text, data = nav.allow_set(knots, toward)
        return "reckoning.set_allowance", text, {"verb": verb, "level": 1} | data
    if verb == "shape a course for":
        if not rest:
            raise OrderError("Shape a course for where? Name a place of the chart.")
        nav = _navigation(ship)
        pricked = _position_in(rest)
        if pricked is not None:
            # a point pricked on the chart (package 36: the books' waypoints through the
            # Goulet and out of Falmouth), the course from the account as for a place
            heading, words = _shape_for_position(nav, pricked)
        else:
            heading, words = nav.shape_course(rest)
        from freesail.orders import handle

        not_laid = _course_not_laid(ship, heading)
        if not_laid:
            # the course lies nearer the wind than she will sail: said, not steered, and
            # she is kept full and by on the tack that points nearer it, put about for it
            # when that is the other tack (as the pilot's course is said and not steered,
            # package 35; the book's helm rules have no other guard)
            _, helm_text, helm_data = handle(ship, not_laid[1])
            words = words.rstrip(".") + f"; {not_laid[0]}."
        else:
            _, helm_text, helm_data = handle(ship, f"steer {units.rad_to_deg(heading):.0f}")
        data = {"verb": verb, "level": 1, "place": rest, "heading": heading} | {"helm": helm_data}
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
            sighting = min(sails, key=lambda s: s.distance_m)
        from freesail.world.lookout import relative_words

        heading = float(world.ship.heading)
        relative = relative_words(math.radians(sighting.bearing_deg) - heading)
        point = units.point_name(math.radians(sighting.bearing_deg))
        who = lookout.sail_name(sighting.feature.id, sighting.feature.name)
        course, drift_words = _chase_course(world, sighting)
        from freesail.orders import handle

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
    words = "".join(c if c.isalnum() or c.isspace() else " " for c in name.lower()).split()
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
