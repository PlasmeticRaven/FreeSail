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
    work my reckoning               the master's slate since the last fix, for a station's
                                    own reckoning; a reading in the reply, never a line
                                    of the log (package 40b; spec M6 §5)
    my reckoning is <lat> <long>    a station's own reckoning, kept beside the master's and
                                    said after the noon's line; it moves nothing
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
from dataclasses import dataclass
from typing import Any

from freesail import units
from freesail.orders import errors
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.world.geo import name_words, parse_position

__all__ = [
    "NO_RECKONING_WORDS",
    "OWN_RECKONING_VERBS",
    "OWN_REFUSED_WORDS",
    "SLATE_KIND",
    "check",
    "execute",
    "mark_in_sight",
    "own_station",
    "where_is",
]

NO_RECKONING_WORDS = (
    "No reckoning is kept in this ship: the scenario gives her no position, and there is "
    "no sea to be lost on."
)

# An officer's own reckoning (package 40b; spec M6 §5): the slate asked for and his own
# position given back, by the station that keeps it. A book gives neither: a reckoning
# is a man's working, and the standing dialect refuses both at entry
# (`standing.grammar`).
OWN_RECKONING_VERBS = ("work my reckoning", "my reckoning is")
# The slate's kind: a reading answered in the station's reply and never written in the
# log (`core.world.UNLOGGED_KINDS`), as the brief of package 40b has it.
SLATE_KIND = "query.slate"
OWN_REFUSED_WORDS = (
    "A reckoning of one's own is a man's working from the slate, never a book's: "
    "'work my reckoning' and 'my reckoning is' are given at a station, not by a standing "
    "order."
)


def own_station(ship: Any) -> str:
    """The station whose own reckoning an order works or gives, by the order's actor
    (`core.world.ORDER_ACTOR`): the officer of the watch's (a model's or the player's
    seat), or the captain's (the player at the prompt, or the captain's station).
    Refused in words for a standing order's firing and the rules-based captain's
    judgement, and for a station that keeps no reckoning."""
    from freesail.core.world import RULE_ACTOR_PREFIXES
    from freesail.world.reckoning import OWN_STATIONS

    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
    if actor.startswith(RULE_ACTOR_PREFIXES):
        raise OrderError(OWN_REFUSED_WORDS)
    station = actor.split(" (", 1)[0].removeprefix("the ").strip()
    if station in OWN_STATIONS:
        return station
    raise OrderError(f"The {station} keeps no reckoning of his own.")


def _position_or_refuse(rest: str, verb: str) -> Any:
    try:
        return parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", rest))
    except ValueError:
        raise OrderError(f"'{rest}' is not a position; say '{verb} 49 52 N 6 10 W'.") from None


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
# the bearing draws, together with his own way across it, which is his own run through
# the water between the two bearings by his course and his log (package 45c:
# `Lookout.own_run`, pegged each minute; it was the course she was on at the second
# bearing, so that a chase begun as she turned read her whole turn as the chase's drift
# and led her across the brig's bows at the cap); the lead off her bearing is the angle
# whose sine is that over his own speed. Everything in it is his (the bearing, the glass,
# the estimate, which is a third out at the worst, his log and his course). The lead is
# capped (judgement: short of the right angle, beyond which she would be running from
# the line of sight; 45 degrees before package 45c, which left a brig crossing at her own
# speed two miles off to cross ahead of her); a bearing that has swung more than
# `CHASE_CROSSED_DEG` since the last is a chase that has crossed her bows or passed close,
# and she is steered for her bearing again (the bearing's drift over the interval says
# nothing of the rate now); and the course is never nearer the wind than she lies
# close-hauled, when she is put close-hauled on the tack nearer the course (judgement).
CHASE_LEAD_MAX_DEG = 70.0
CHASE_CROSSED_DEG = 45.0
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
    peg = getattr(lookout, "peg_own_run", None)
    run = peg(world) if peg is not None else None
    last = chases.get(fid)
    chases[fid] = (tick, bearing) if run is None else (tick, bearing, run[0], run[1])
    words = ""
    course = bearing
    if last is not None and tick - last[0] >= CHASE_MIN_INTERVAL_S:
        drift = units.rad_to_deg(units.wrap_pi(math.radians(bearing - last[1])))
        way = (
            "aft"
            if (drift > 0) == (units.wrap_pi(math.radians(bearing - heading_deg)) < 0)
            else "forward"
        )
        if abs(drift) < CHASE_STEADY_DEG:
            words = ", the bearing steady"
        elif abs(drift) > CHASE_CROSSED_DEG:
            words = (
                f", drawing {way} {abs(drift):.0f} degrees since the last: she has crossed, "
                "and the course is laid for her bearing again"
            )
        else:
            words = f", drawing {way} {abs(drift):.0f} degrees since the last"
            lead = drift
            dyn = getattr(world.ship, "dyn", None)
            speed = float(dyn.speed) if dyn is not None else 0.0
            estimate = getattr(sighting, "estimate_m", None)
            if estimate and speed > 0.1:
                dt = float(tick - last[0])
                rate = math.radians(drift) / dt  # rad/s, clockwise
                if run is not None and len(last) >= 4:
                    # his own way across the line of sight, from his run between the
                    # bearings, across the mean of the two
                    mean = math.radians(last[1] + drift / 2.0)
                    de, dn = run[0] - float(last[2]), run[1] - float(last[3])
                    own_across = (de * math.cos(mean) - dn * math.sin(mean)) / dt
                else:
                    own_across = speed * math.sin(math.radians(heading_deg - bearing))
                across = (float(estimate) * rate + own_across) / speed
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


# ---------------------------------------------------------------------------
# The helm through the wind (package 37m; the owner's ruling 3 of 2026-10-09, spec M6 §31,
# decision 39): one judgement of a course against her head and the wind, shared by
# `steer <course>`, the points orders (`come up`, `bear away`, `steer two points to
# starboard`), `shape a course for` and `give chase`. She is steered, put about, worn,
# gybed or kept full and by as the ship and the course allow, and the line says which,
# so that a captain reading it may countermand.
# ---------------------------------------------------------------------------

# A course shaped nearer the wind than close-hauled and half a point is not laid
# (package 35's rule for the pilot's course, `evolutions.scripts`): she is kept full and
# by on the tack that points nearer the course. The helm's own orders (`steer`, the
# points orders) are laid at the close-hauled angle itself, and on the tack she is on
# they are carried out as given however near the wind: pinching her is the captain's to
# order (Fincham 1843, art. 99, the sails "just lifting"; truths 1, 2 and 25 steer her
# up so), and the line warns when the course lies in the wind's eye.
COURSE_NOT_LAID_MARGIN_POINTS = 0.5
# "The wind's eye": the point the wind blows from. A helm order within a point of it is a
# course in the wind's eye, steered as given and said to take her aback (the owner's
# ruling 3); judgement, a point either side, since the wind is named to the point and
# wanders about it.
EYE_POINTS = 1.0
# the point either side of it taken whole: N by W is in the eye of a northerly, though the
# wind's own figure wanders a degree from its point
EYE_ALLOWANCE = units.deg_to_rad(1.0)
# Way enough to stay: the tack's own precondition (`data/evolutions/tack.yaml`, two
# knots); under it a ship that must cross the wind's eye is worn, "when ... the vessel
# has not sufficient headway for tacking" (Luce 1866, ch. XXIV, 'Wearing').
STAY_MIN_KN = 2.0
# A vessel with a square sail set and this much way on is worn for a course through the
# wind's wake (a knot: under that she is drifting, and a wear would not come round); and
# a ship that must cross the wind's eye without way to stay is worn with no less.
WEAR_FOR_IT_MIN_MS = 0.5
# A turn by the stern of eight points or less keeps the wind abaft the beam at both ends,
# where a square sail fills however its yard is braced: running, the wind brought from one
# quarter to the other, it is the helm's, the trim following (the St Mary's pilot's
# approach in `tests/test_ports.py`, steered by the bearing a minute at a time, came 78
# degrees round from a run and was worn for it, and she struck the Nut Rock). A longer
# turn brings the wind forward of the beam on the new side with the yards still braced
# for the old: what laid every square sail aback in the cruise's chase (the fold-in of
# m5c-c, whose guard counted turns of more than six points). Judgement.
WAKE_HELM_POINTS = 8.0
# Under this she has no steerage way: the course is steered as given, as it always was,
# for there is no turn to judge (a ship gathering way from rest, a ship drifting).
STEERAGE_WAY_MS = 0.1
# The course given when she gathers way, not at the aweigh (package 58b, item 4; the lead's
# wave-2 playtest, finding 4: the standing order `at the anchor aweigh then steer E` put
# the Éclair's helm for E the moment the anchor broke out, before she had cast or had way,
# and her head fell off to the south with the land a cable on the bow, as in the owner's
# first cruise). After weighing, a course given her (a helm order, a course shaped, a
# chase's) is held while she casts and until she has this much way through the water with
# her sails drawing, and given then (`keep_course_pending`); the cast and the course the
# get-under-way ends on are the evolution's own. Judgement: a knot, the way at which a
# ship answers her helm, the period's "she gathers way".
GATHERED_WAY_KN = 1.0
# The weighing evolutions and their phases once the anchor is aweigh: casting and under
# way for `get under way`, the anchor hove up and catted for `weigh` alone.
WEIGHING_PHASES: dict[str, tuple[str, ...]] = {
    "get_under_way": ("cast", "under_way"),
    "weigh_anchor": ("hoist", "cat_and_fish"),
}


def _has_way(ship: Any) -> bool:
    """A knot of headway through the water (`GATHERED_WAY_KN`), a sail set and none of
    hers aback: she has gathered way."""
    from freesail.physics.hull import hull_state

    dyn = getattr(ship, "dyn", None)
    if dyn is None or float(dyn.u) < units.knots_to_ms(GATHERED_WAY_KN):
        return False
    if hull_state(ship).seconds_aback > 0.0:
        return False
    return any(sl.is_set for sl in ship.sails.values())


def gathering_way(ship: Any) -> bool:
    """Whether she has weighed and not yet gathered way (package 58b, item 4): a weighing
    in hand with the anchor aweigh, still casting, or cast (or hove up alone) and without
    a knot of way and her sails drawing (`_has_way`)."""
    runner = (getattr(ship, "extra", None) or {}).get("evolutions")
    for inst in getattr(runner, "instances", None) or []:
        phases = WEIGHING_PHASES.get(inst.evo.id)
        script = getattr(inst, "script", None)
        if phases is None or script is None or inst.waiting or script.status != "running":
            continue
        if getattr(script, "phase", "") not in phases:
            continue
        if script.phase == "cast":
            return True
        return not _has_way(ship)
    return False


# The manoeuvres a course is handed to while they are in hand (`give_course`).
COURSE_MANOEUVRES = ("tack", "wear")


@dataclass(frozen=True)
class Judgement:
    """What the helm is to do for a course: `branch` is 'helm' (steered as given),
    'aback' (steered as given, in the wind's eye), 'full_and_by' (kept full and by on the
    tack she is on), 'tack' or 'wear' (the manoeuvre ordered for the course), 'gybe'
    (steered round by the stern, a fore-and-after's boom coming over), or 'in_hand' (a
    tack or a wear in hand takes the course as she comes round), or 'pending' (across the
    wind with too little way: kept full and by and the course held till she has way,
    `keep_course_pending`; since package 58b also a course given after weighing before she
    has gathered way, `gathering_way`). `course` is the heading
    she is to have at the end (radians true): the course, or the close-hauled course on
    the tack she is kept full and by on; `words` the clause the line says."""

    branch: str
    course: float
    words: str = ""
    full_and_by: bool = False
    tack: str = ""
    # 'eye' or 'wake', for a course held till she has way ('pending'); 'way' for one held
    # since the aweigh till she has gathered way (package 58b)
    crossing: str = ""
    helm_order: bool = False


def _side(x: float) -> str:
    """The tack of a heading `x` radians from the wind's eye: the wind over the starboard
    side when her head lies to the left of it."""
    return "starboard" if x < 0.0 else "larboard"


def _crosses(now: float, to: float, wind_from: float) -> str | None:
    """Which of the wind's eye ('eye') and its wake ('wake') the shorter turn from her
    head `now` to `to` passes through; None when it passes through neither, the course
    lying on the tack she is on. A turn through the wake of `WAKE_HELM_POINTS` or less is
    the helm's (`WAKE_HELM_POINTS`)."""
    turn = units.wrap_pi(to - now)
    for mark, name in ((wind_from, "eye"), (wind_from + math.pi, "wake")):
        to_mark = units.wrap_pi(mark - now)
        if to_mark != 0.0 and (turn > 0) == (to_mark > 0) and abs(to_mark) < abs(turn):
            if name == "wake" and abs(turn) <= WAKE_HELM_POINTS * units.POINT + 1e-9:
                return None
            return name
    return None


def _square_sail_set(ship: Any) -> bool:
    """A square sail set: a vessel whose long turn by the stern is a wear, her yards to be
    braced round as the wind comes over (the fold-in of m5c-c for a square-rigged ship;
    the lead's ruling on package 37m for a fore-and-after with a square sail set, the
    topsail schooner's fore topsail and topgallant, the cutter's square sail and topsail,
    whose yards gybed by the helm were still braced for the old tack and laid her aback).
    With none set, a fore-and-after gybes by the helm, her boom coming over."""
    return any(sl.is_set and sl.cls == "square" for sl in ship.sails.values())


def manoeuvre_in_hand(ship: Any) -> Any:
    """The tack or the wear in hand (begun and running), or None."""
    runner = (getattr(ship, "extra", None) or {}).get("evolutions")
    for inst in reversed(getattr(runner, "instances", None) or []):
        script = getattr(inst, "script", None)
        if (
            inst.evo.id in COURSE_MANOEUVRES
            and script is not None
            and not inst.waiting
            and script.status == "running"
            and script.phase != "ready"
        ):
            return inst
    return None


def judge_course(
    ship: Any,
    course: float,
    helm_order: bool,
    points: bool = False,
    stay_kn: float = STAY_MIN_KN,
) -> Judgement:
    """The one judgement of a course (radians true) against her head and the wind.

    `helm_order` is true for the helm's own orders (`steer`, the points orders), false for
    a course shaped or a chase's; `points` for an order reckoned from her course in points
    (`come up`, `bear away`, `steer two points off`). Laid and on the tack she is on, the
    helm; across the wind's eye, put about when she has way enough to stay, else worn
    (Luce 1866, ch. XXIV, 'Wearing': "when ... the vessel has not sufficient headway for
    tacking"); through the wind's wake, worn if she has a square sail set (a square-rigged
    ship, or a fore-and-after with her topsail set), gybed by the helm if a fore-and-after
    with none; nearer the wind than she will lie, kept full and by on the
    tack that points nearer it, put about or worn for that tack when it is the other; a
    helm order in the wind's eye is steered as given, and the line says she will be taken
    aback. A tack or a wear in hand takes a course on the tack she is going to (an order
    reckoned in points is left to the helm there, as it always was)."""
    from freesail.evolutions.scripts import close_hauled_true_angle
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    wind = getattr(world, "wind", None)
    dyn = getattr(ship, "dyn", None)
    if wind is None or dyn is None:
        return Judgement("helm", course)
    wind_from = float(wind.direction_from)
    closest = close_hauled_true_angle(ship)
    shown = units.format_heading(course)
    x = units.wrap_pi(course - wind_from)
    off = abs(x)
    said_tack = _side(x)
    speed = float(getattr(dyn, "speed", 0.0))
    now = float(dyn.heading)
    margin = 0.0 if helm_order else COURSE_NOT_LAID_MARGIN_POINTS * units.POINT
    laid = off >= closest + margin

    in_hand = manoeuvre_in_hand(ship)
    if in_hand is not None:
        if points:
            return Judgement("helm", course)
        going_to = "larboard" if in_hand.script.sign > 0 else "starboard"
        if said_tack == going_to:
            doing = "going about" if in_hand.evo.id == "tack" else "wearing"
            words = (
                f"{shown}: she is {doing}, and the course is given her as she comes round"
                if laid
                else f"{shown} lies too near the wind to be laid; she is {doing}, and is kept "
                f"full and by on the {going_to} tack as she comes round"
            )
            if laid:
                return Judgement("in_hand", course, words, tack=going_to)
            sign = 1.0 if going_to == "larboard" else -1.0
            by_the_wind = units.wrap_2pi(wind_from + sign * closest)
            return Judgement("in_hand", by_the_wind, words, full_and_by=True, tack=going_to)

    if gathering_way(ship):
        # weighed and not yet under way (package 58b, item 4): the course is held while she
        # casts and given when she has gathered way, as `keep_course_pending` gives a course
        # held for way across the wind
        words = (
            f"{shown} is held till she has gathered way: the anchor is aweigh and she has not "
            f"a knot of way on her yet; it is given when she has, her sails drawing"
        )
        return Judgement("pending", course, words, helm_order=helm_order, crossing="way")
    if helm_order and off <= EYE_POINTS * units.POINT + EYE_ALLOWANCE:
        # the owner's ruling: a course given directly into the wind's eye is steered
        aback = f"{shown} lies in the wind's eye from her head; she will be taken aback"
        return Judgement("aback", course, aback)
    own = _side(units.wrap_pi(now - wind_from))
    crossing = _crosses(now, course, wind_from)
    if crossing is None:
        if laid or helm_order:
            return Judgement("helm", course)
        # a course too near the wind on the tack she is on: kept full and by on her tack
        words = (
            f"{shown} lies too near the wind to be laid; she is kept full and by on the {own} tack"
        )
        return Judgement("full_and_by", course, words, full_and_by=True, tack=own)
    # through the wind: the course, or the close-hauled course on the tack nearer it
    if laid:
        target, full_and_by = course, False
        what = f"{shown} lies across the wind's eye from her head"
    else:
        sign = 1.0 if said_tack == "larboard" else -1.0
        target, full_and_by = units.wrap_2pi(wind_from + sign * closest), True
        what = f"{shown} lies too near the wind to be laid"
    crossing = _crosses(now, target, wind_from) or crossing
    if laid and crossing == "wake":
        what = f"{shown} lies across the wind from her head, by the stern"
    tail = f" and kept full and by on the {said_tack} tack" if full_and_by else ""
    square = _square_sail_set(ship)
    if crossing == "eye":
        if speed >= units.knots_to_ms(stay_kn):
            way = "she is put about for it" if laid else "she is put about"
            return Judgement("tack", target, f"{what}; {way}{tail}", full_and_by, said_tack)
        if speed > WEAR_FOR_IT_MIN_MS:
            way = "worn round for it" if laid else "worn round"
            return Judgement(
                "wear",
                target,
                f"{what}; she has not way enough to stay, and is {way}{tail}",
                full_and_by,
                said_tack,
            )
    elif square:
        if speed > WEAR_FOR_IT_MIN_MS:
            way = "she is worn round for it" if laid else "she is worn round"
            return Judgement("wear", target, f"{what}; {way}{tail}", full_and_by, said_tack)
    elif speed > STEERAGE_WAY_MS:
        way = (
            "she gybes for it by the helm"
            if laid
            else f"she gybes by the helm and is steered close-hauled on the {said_tack} tack"
        )
        return Judgement("gybe", target, f"{what}; {way}", full_and_by, said_tack)
    # too little way to go about, to wear or to gybe (package 37m, the lead's last round):
    # not left to the helm, which would turn her across the wind with her yards and sheets
    # for the old tack and lay her aback (the merchant passage filling away after the
    # Iroise's cast), but kept full and by on her tack, the course held as the helm's
    # intention and judged again when she has the way (`keep_course_pending`)
    then = (
        "put about"
        if crossing == "eye" and laid
        else "worn"
        if square or crossing == "eye"
        else "gybed"
    )
    then += " for it" if laid else f" for the {said_tack} tack and kept full and by"
    lacking = "has no way on her" if speed <= STEERAGE_WAY_MS else "has not way enough on her"
    return Judgement(
        "pending",
        course,
        f"{what}, and she {lacking}; she is kept full and by on the {own} tack until she has, "
        f"then {then}",
        full_and_by,
        own,
        crossing=crossing or "",
        helm_order=helm_order,
    )


def carry_out(ship: Any, judged: Judgement) -> tuple[str, dict[str, Any]]:
    """Put a judgement other than the plain helm's into effect: (the helm's or the
    manoeuvre's own words, its data). A tack or a wear is ordered with the course it is
    for and ends by steering it (`evolutions.scripts.CourseToSteer`); refused, the order
    is refused with the judgement's words and the reason."""
    from freesail.orders import handle, verbs

    if judged.branch == "in_hand":
        inst = manoeuvre_in_hand(ship)
        inst.script.give_course(units.rad_to_deg(judged.course), judged.full_and_by)
        return "", {"verb": inst.evo.id, "in_hand": True}
    if judged.branch == "full_and_by":
        _, text, data = handle(ship, "keep her full and by")
        return text, data
    if judged.branch == "pending" and judged.crossing == "way":
        # weighed and casting (package 58b, item 4): the helm is the evolution's while she
        # casts, and the course is held for her, nothing ordered now
        ship.extra[COURSE_PENDING] = {
            "course_deg": round(units.rad_to_deg(judged.course), 3),
            "helm_order": judged.helm_order,
            "crossing": "way",
            "waited_s": 0.0,
        }
        return "", {"course_pending": ship.extra[COURSE_PENDING]["course_deg"], "held_for": "way"}
    if judged.branch == "pending":
        # kept full and by on her tack, the course held till she has way (the helm's order
        # clears any intention held before it, and this one is held after it)
        _, text, data = handle(ship, "keep her full and by")
        ship.extra[COURSE_PENDING] = {
            "course_deg": round(units.rad_to_deg(judged.course), 3),
            "helm_order": judged.helm_order,
            "crossing": judged.crossing,
            "waited_s": 0.0,
        }
        return text, data | {"course_pending": ship.extra[COURSE_PENDING]["course_deg"]}
    if judged.branch in COURSE_MANOEUVRES:
        params: dict[str, Any] = {"course_deg": round(units.rad_to_deg(judged.course), 3)}
        if judged.full_and_by:
            params["full_and_by"] = True
        try:
            _, text, data = verbs.manoeuvre_for_course(ship, judged.branch, params)
        except OrderError as exc:
            said = judged.words[:1].upper() + judged.words[1:]
            raise OrderError(f"{said}; that could not be done: {exc}") from None
        return text, data
    # the helm: steered as given, or round by the stern for a fore-and-after
    _, text, data = steer_degrees(ship, units.rad_to_deg(judged.course))
    return text, data


# The course held as the helm's intention while she has not the way to go about, wear or
# gybe for it (`ship.extra`, a plain dict, so that a checkpoint carries it).
COURSE_PENDING = "course_pending"
# Held for a turn across the wind's eye, she waits this long, seconds, with way enough to
# wear and not to stay, for the way to stay, and is then worn (judgement: a frigate
# gathers her two knots from rest in two or three minutes under plain sail).
STAY_WAIT_S = 180.0
# Held for a turn across the eye, she is put about when she has gathered this much way,
# a knot more than the tack's least: at the tack's own two knots, just gathered from rest,
# the frigate missed stays in the test of it (`tests/test_ships.py`), her way not yet her
# own. Under it after `STAY_WAIT_S`, she is worn. Judgement.
PENDING_STAY_KN = 3.0


def keep_course_pending(ship: Any, dt: float) -> None:
    """Each tick (`evolutions.runner.Runner.step`): a course held for want of way is judged
    again once she has it: `PENDING_STAY_KN` to tack for a turn across the eye (or, after
    `STAY_WAIT_S` with the way to wear, to wear); the way to wear for a turn by the stern
    with a square sail set; steerage way to gybe without. The manoeuvre then comes, and
    she ends on the course. At anchor or aground the intention is let go."""
    pending = (getattr(ship, "extra", None) or {}).get(COURSE_PENDING)
    if not pending:
        return
    extra = ship.extra
    tackle = extra.get("ground_tackle")
    if extra.get("aground") or (tackle is not None and tackle.at_anchor()):
        extra.pop(COURSE_PENDING, None)
        return
    speed = float(ship.dyn.speed)
    held_for_way = pending.get("crossing") == "way"
    if held_for_way:
        # held since the aweigh (package 58b, item 4): given when she has gathered way
        ready = not gathering_way(ship)
    elif pending["crossing"] == "eye":
        if speed > WEAR_FOR_IT_MIN_MS:
            pending["waited_s"] = float(pending.get("waited_s", 0.0)) + dt
        ready = speed >= units.knots_to_ms(PENDING_STAY_KN) or (
            speed > WEAR_FOR_IT_MIN_MS and pending["waited_s"] >= STAY_WAIT_S
        )
    elif _square_sail_set(ship):
        ready = speed > WEAR_FOR_IT_MIN_MS
    else:
        ready = speed > STEERAGE_WAY_MS
    if not ready:
        return
    extra.pop(COURSE_PENDING, None)
    course = math.radians(float(pending["course_deg"]))
    judged = judge_course(
        ship, course, helm_order=bool(pending["helm_order"]), stay_kn=PENDING_STAY_KN
    )
    try:
        if judged.branch == "helm":
            _, text, data = steer_degrees(ship, units.rad_to_deg(course))
        else:
            text, data = carry_out(ship, judged)
    except OrderError as exc:
        ship.note(
            "notable",
            "helm.course_given",
            f"She has way on her, but the course held for her could not be given: {exc}",
            ship.name,
        )
        return
    said = judged.words or f"{units.format_heading(course)} is steered"
    head = "She has way on her now"
    if held_for_way:
        knots = units.ms_to_knots(float(ship.dyn.u))
        head = f"She has gathered way, {knots:.1f} knots, her sails drawing"
    ship.note(
        "notable",
        "helm.course_given",
        f"{head}: {said}. {text}".rstrip(),
        ship.name,
        # the held-for key only for a course held for way, so that the eye's and the
        # wake's lines are as they were
        {"judged": judged.branch, "course_deg": pending["course_deg"], "helm": data}
        | ({"held_for": "way"} if held_for_way else {}),
    )


# The wind across the stern (package 58b, item 3; the owner's ruling of 2026-10-23: nothing
# is ordered by the helm). A turn by the stern of `WAKE_HELM_POINTS` or less is the helm's,
# and a fore-and-after's long one a gybe by the helm; the sails answer it as 43b and 37m
# built them, and that is not changed: a boom comes over by itself (its strain line), a
# dipping lug left on the old side is pressed against its mast and draws at
# `physics.sails.LUG_AGAINST_MAST_AREA` until it is dipped, square yards left braced for the
# old tack are by the lee. What the deck adds is one line when the wind has come across
# the stern and left a lug against its mast or the yards by the lee ("dip them when you
# will"), once a crossing, and nothing done: the sail work is the captain's next order (the
# rules captain gives it, `captains.Captain._across_the_stern`). The crossing is counted
# when the wind is this far past dead astern on the new quarter, so that a ship running
# with the wind yawing about her stern is not told of it at every yaw (judgement: a point,
# more than a helmsman's yaw before it).
STERN_CROSSED_DEG = 11.25
STERN_WATCH = "stern_watch"  # `ship.extra`: the side the wind was last on, a plain dict


def _whole_ship_work(ship: Any) -> bool:
    """A whole-ship evolution in hand (a tack, a wear, heaving to, getting under way, coming
    to an anchor) or her lying to: the manoeuvre does its own sail work."""
    extra = getattr(ship, "extra", None) or {}
    if "hove_to" in extra:
        return True
    runner = extra.get("evolutions")
    for inst in getattr(runner, "instances", None) or []:
        if getattr(inst, "subject_id", None) not in ("ship", getattr(ship, "name", None)):
            continue
        script = getattr(inst, "script", None)
        if inst.evo.id == "get_under_way" and getattr(script, "cast_done", False):
            continue  # cast and under way, the anchor at the cathead: her sails are set
        return True
    return False


def watch_the_stern(ship: Any) -> None:
    """Each tick (`evolutions.runner.Runner.step`): when the wind has come across her stern
    (abaft the beam on both sides, past dead astern by `STERN_CROSSED_DEG`) and a dipping
    lug lies against its mast or a square yard is braced for the old tack, one line says so,
    once for the crossing (package 58b, item 3). Nothing is ordered; a crossing in a
    manoeuvre is the manoeuvre's."""
    dyn = getattr(ship, "dyn", None)
    extra = getattr(ship, "extra", None)
    if dyn is None or not isinstance(extra, dict):
        return
    awa = float(dyn.apparent_wind_angle)
    side = "starboard" if awa >= 0.0 else "larboard"  # the side the wind is on
    watch = extra.get(STERN_WATCH)
    if not isinstance(watch, dict):
        extra[STERN_WATCH] = {"side": side}
        return
    if side == watch.get("side"):
        return
    if abs(awa) < math.pi / 2.0:
        # through the eye or before the beam: a tack's, or the wind's shift ahead
        watch["side"] = side
        return
    if math.pi - abs(awa) < math.radians(STERN_CROSSED_DEG):
        return  # not yet a point past dead astern on the new quarter
    old = watch.get("side")
    watch["side"] = side
    if _whole_ship_work(ship) or extra.get("aground"):
        return
    from freesail.evolutions.scripts import (
        _yards_aback_for,
        boom_sails,
        dipping_lugs,
        names_of_sails,
    )

    lee = "larboard" if side == "starboard" else "starboard"
    lugs = [sl for sl in dipping_lugs(ship) if sl.lug_side is not None and sl.lug_side != lee]
    sign = 1.0 if side == "starboard" else -1.0
    yards = _yards_aback_for(ship, sign)
    if not lugs and not yards:
        return
    said = []
    if lugs:
        one = len(lugs) == 1
        names = names_of_sails(ship, lugs)
        said.append(
            f"{names} {'is' if one else 'are'} against {'its mast' if one else 'their masts'}; "
            f"dip {'it' if one else 'them'} when you will"
        )
    if yards:
        said.append(
            f"the yards are braced for the {old} tack, by the lee; brace them round when you will"
        )
    booms = [sl.id for sl in boom_sails(ship)]
    ship.note(
        "notable",
        "sail.across_the_stern",
        f"The wind has come across the stern to the {side} quarter: " + "; and ".join(said) + ".",
        ship.name,
        {
            "side": side,
            "lugs": [sl.id for sl in lugs],
            "yards": [y.id for y in yards],
            "booms": booms,
        },
    )


def steer_degrees(ship: Any, degrees: float) -> Result:
    """The helm put for a course in whole degrees, as `steer <degrees>` puts it, with no
    judgement of it (the judgement has been made)."""
    from freesail.orders import verbs

    return verbs.steer_as_given(ship, f"steer {degrees:.0f}")


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


# `put her about` (package 45, Part B item 4; the owner's notes 4 and 7 of gate m6a: missed
# stays under a reefed main topsail and staysails, and after the headsails blew out). She
# wears when her sail is short or she has lately missed stays, and tacks regardless with
# the land close to leeward, since wearing loses the ground. The figures are the
# doctrine's where a captain gives the order (`data/captains/*.yaml`: `wear_wind_kn`,
# `tack_regardless_nm`) and these by default: thirty knots is the starter book's shorten-
# sail line and Luce's "To wear ship ... in a gale"; two miles is the planner's danger
# berth doubled (judgement); an hour is a watch's half.
WEAR_WIND_KN = 30.0
TACK_REGARDLESS_NM = 2.0
MISSED_STAYS_WITHIN_S = 3600
CLOSE_REEF = 3


def put_about_choice(ship: Any) -> tuple[str, str]:
    from freesail.world.reckoning import miles_words

    """('tack ship' | 'wear ship', why): the rule above, read from the ship and the
    readings (her sails, the wind, the nearest land to leeward, the log's missed stays)."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    readings = getattr(world, "readings", None)
    reasons: list[str] = []
    # the land to leeward: tack regardless within TACK_REGARDLESS_NM
    close = None
    wind_from = None
    if readings is not None:
        near = readings.value("nearest_land")
        frm = readings.value("mean_true_wind_from")
        if frm is None:
            frm = readings.value("true_wind_from")
        wind_from = float(frm) if frm is not None else None
        if isinstance(near, dict) and near.get("metres") is not None and wind_from is not None:
            brg = near.get("bearing_deg")
            if brg is None and near.get("bearing"):
                try:
                    brg = units.rad_to_deg(units.parse_course(str(near["bearing"])))
                except (ValueError, units.CourseError):
                    brg = None
            if brg is not None:
                toward = (units.rad_to_deg(wind_from) + 180.0) % 360.0
                to_lee = abs(units.wrap_pi(math.radians(float(brg) - toward))) < math.radians(67.5)
                if to_lee:
                    close = float(near["metres"]) / units.NAUTICAL_MILE
    if close is not None and close < TACK_REGARDLESS_NM:
        return "tack ship", (
            f"the land {miles_words(close)} to leeward, where wearing would lose the ground"
        )
    sails = getattr(ship, "sails", {}) or {}
    groups = getattr(ship, "groups", {}) or {}
    head = [
        sails[sid]
        for g in ("jibs", "staysails", "head sails")
        for sid in groups.get(g, [])
        if sid in sails
    ]
    if not head:
        head = [sl for sl in sails.values() if sl.cls == "jibheaded" and sl.x_m > 0]
    if head and not any(sl.is_set for sl in head):
        reasons.append("no head sail set")
    topsails = [sails[sid] for sid in groups.get("topsails", []) if sid in sails]
    if (
        topsails
        and all(sl.reefs >= CLOSE_REEF for sl in topsails if sl.is_set)
        and any(sl.is_set for sl in topsails)
    ):
        reasons.append("the topsails close-reefed")
    wind_kn = None
    if readings is not None:
        w = readings.value("mean_true_wind_speed")
        if w is None:
            w = readings.value("true_wind_speed")
        wind_kn = units.ms_to_knots(float(w)) if w is not None else None
    if wind_kn is not None and wind_kn > WEAR_WIND_KN:
        reasons.append(f"the wind {wind_kn:.0f} knots")
    log = getattr(world, "log", None)
    tick = world.clock.tick
    if log is not None:
        since = log.since(max(0, tick - MISSED_STAYS_WITHIN_S))
        missed = [e for e in since if e.kind == "ship.missed_stays"]
        if missed:
            reasons.append("she missed stays within the hour")
    if reasons:
        return "wear ship", ", ".join(reasons)
    return "tack ship", "her sail is whole and the wind moderate"


def put_about(ship: Any) -> Result:
    """`put her about`: tacks or wears by `put_about_choice`, the choice and its reason
    said before the manoeuvre's own line."""
    from freesail import orders

    verb, why = put_about_choice(ship)
    choice = "wearing" if verb == "wear ship" else "tacking"
    # the choice said as a note of the ship's (the World drops an evolution order's own
    # text when the runner has logged its start), before the manoeuvre's own line
    note = getattr(ship, "note", None)
    if callable(note):
        note(
            "notable",
            "ship.put_about",
            f"Put about: {choice}, {why}.",
            data={"put_about": verb, "why": why},
        )
    kind, text, data = orders.handle(ship, verb)
    data = dict(data or {})
    data["put_about"] = verb
    data["why"] = why
    return kind, f"{choice.capitalize()}, {why}. {text}".strip(), data


def _target_of(world: Any, nav: Any, place: str) -> tuple[Any, str, Any]:
    """A place's position, its words and its feature (None for a point): a pricked
    position, a point off a place, or a feature of the chart; refused in words."""
    pricked = _position_in(place)
    if pricked is not None:
        from freesail.world.geo import format_position

        return pricked, format_position(pricked), None
    off = _off_a_place(world, place)
    if off is not None:
        return off[0], off[1], None
    found = nav.place_of(place)  # a feature, or a port by its name (its road)
    if found is None:
        raise OrderError(_no_place_words(world.chart, place))
    return found


def _shape_the_way(ship: Any, nav: Any, dest: str, via: list[str]) -> Result:
    """`shape a course for <place> via <mark>, <mark>` (package 45): the way's points
    worked by `captains.way_marks` (a mark that is land or a danger passed a league off,
    on the hand the straight line puts it; a mark that is water sailed to), the course
    shaped for the first, the rest kept by the master (`Navigation.way`). No routing
    between the marks: the straight line between one and the next, as the plan's."""
    from freesail.world.captains import way_marks

    world = nav.world
    end, end_words, _ = _target_of(world, nav, dest)
    try:
        points = way_marks(world, nav.account_now(), via, end)
    except ValueError as e:
        raise OrderError(str(e)) from None
    first = points[0]
    heading, words, shaped = nav.shape_for(first[1], first[0])
    rest = [
        {"words": w, "said": w, "lat_deg": p.lat_deg, "lon_deg": p.lon_deg, "hand": h}
        for w, p, h in points[1:]
    ]
    # the destination by the words given (a port's name, a place, a point): what the
    # master shapes for when the way comes to it; its full name (`said`) in the lines
    rest.append(
        {
            "words": dest,
            "said": end_words,
            "lat_deg": end.lat_deg,
            "lon_deg": end.lon_deg,
            "hand": "",
        }
    )
    then = "; then " + ", then ".join(x["said"] for x in rest)
    hands = "; ".join(h for _, _, h in points if h)
    words = words.rstrip(".") + then + (f" ({hands})" if hands else "") + "."
    nav.set_way(first[0], first[1], first[2], heading, rest)
    judged = judge_course(ship, heading, helm_order=False)
    if judged.branch == "helm":
        _, helm_text, helm_data = steer_degrees(ship, units.rad_to_deg(heading))
    else:
        helm_text, helm_data = carry_out(ship, judged)
        words = words.rstrip(".") + f". {judged.words}."
    data = {"verb": "shape a course for", "level": 1, "place": first[0], "heading": heading}
    data |= shaped
    data["helm"] = helm_data
    data["via"] = [x["said"] for x in rest]
    if judged.branch != "helm":
        data["judged"] = judged.branch
    if judged.full_and_by:
        data["course_not_laid"] = True
    return "helm.set", f"{words} {helm_text}".rstrip(), data


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
    if verb == "my reckoning is":
        _position_or_refuse(rest, verb)
        return
    if verb == "work my reckoning":
        if rest:
            raise OrderError("'work my reckoning' takes nothing after it.")
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
        from freesail.world.captains import split_via

        dest, via = split_via(rest, world)
        if not dest:
            raise OrderError("Shape a course for where? Name the place before 'via'.")
        for place in [dest, *via]:
            if _position_in(place) is not None or _off_a_place(world, place) is not None:
                continue
            if chart.find_feature(place) is None and _navigation(ship).place_of(place) is None:
                raise OrderError(_no_place_words(chart, place))
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
    if verb == "work my reckoning":
        # the master's slate (package 40b): a reading in the reply, never in the log
        station = own_station(ship)
        if rest:
            raise OrderError("'work my reckoning' takes nothing after it.")
        nav = _navigation(ship)
        text, data = nav.slate()
        return SLATE_KIND, text, {"verb": verb, "level": 1, "station": station} | data
    if verb == "my reckoning is":
        # the station's own reckoning beside the master's, moving nothing (package 40b)
        station = own_station(ship)
        pos = _position_or_refuse(rest, verb)
        nav = _navigation(ship)
        actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
        text, data = nav.own_reckoning(station, pos, actor)
        return "reckoning.own", text, {"verb": verb, "level": 1, "station": station} | data
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
    if verb == "put her about":
        return put_about(ship)
    if verb == "shape a course for":
        if not rest:
            raise OrderError("Shape a course for where? Name a place of the chart.")
        nav = _navigation(ship)
        from freesail.world.captains import split_via

        rest, via = split_via(rest, nav.world)
        if via:
            # a course by way of marks (package 45): the first mark shaped for now, the
            # rest kept by the master, who shapes each next course as a mark is reached or
            # passed abeam, said in the log; a helm order of the officer's drops the way
            return _shape_the_way(ship, nav, rest, via)
        nav.drop_way()
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
        # the one judgement of the course against her head and the wind (package 37m):
        # steered when it is laid on her tack; put about, worn or gybed for it across the
        # wind, the manoeuvre ending on it; kept full and by when it lies nearer the wind
        # than she will sail (as the pilot's course is said and not steered, package 35),
        # put about or worn for the tack that points nearer it when that is the other
        judged = judge_course(ship, heading, helm_order=False)
        if judged.branch == "helm":
            _, helm_text, helm_data = steer_degrees(ship, units.rad_to_deg(heading))
        else:
            helm_text, helm_data = carry_out(ship, judged)
            # the judgement as a sentence of its own after the course's, so that the
            # allowance's sentence keeps its full stop (package 37m's held course)
            words = words.rstrip(".") + f". {judged.words}."
        data = {"verb": verb, "level": 1, "place": rest, "heading": heading} | shaped
        data["helm"] = helm_data
        if judged.branch != "helm":
            data["judged"] = judged.branch
        if judged.full_and_by:
            data["course_not_laid"] = True
        return "helm.set", f"{words} {helm_text}".rstrip(), data
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
            # the chase in hand is kept while she is in sight and a stranger (a second sail
            # nearer does not take the helm from her); else the nearest stranger; else the
            # nearest sail. Package 45c: a sail spoken, or whose colours are made out for
            # the ship's own nation's, is no stranger and is not kept as the chase (the
            # naval cruise chased the admiral's cutter for two hours after her letter was
            # aboard, the French brig in sight on her quarter)
            chases = getattr(lookout, "_chases", None) or {}
            ports = getattr(world, "ports", None)
            own = ports.ship_nation if ports is not None else None
            known = lookout.stranger(world, float(world.ship.heading), own)
            ids = {i["id"] for i in known["items"]}
            strangers = [s for s in sails if s.feature.modern in ids]
            pool = strangers or sails
            in_hand = [s for s in pool if s.feature.id in chases]
            sighting = min(in_hand or pool, key=lambda s: s.distance_m)
        from freesail.world.lookout import relative_words

        heading = float(world.ship.heading)
        relative = relative_words(math.radians(sighting.bearing_deg) - heading)
        point = units.point_name(math.radians(sighting.bearing_deg))
        who = lookout.sail_name(sighting.feature.id, sighting.feature.name)
        course, drift_words = _chase_course(world, sighting)
        judged = judge_course(ship, math.radians(course), helm_order=False)
        if judged.branch == "helm":
            _, helm_text, helm_data = steer_degrees(ship, course)
        else:
            # the course lies across the wind from her head: put about, worn or gybed for
            # it, the manoeuvre ending on it (package 37m)
            helm_text, helm_data = carry_out(ship, judged)
            drift_words += f"; {judged.words}"
        words = f"Gave chase to {who} {relative}, bearing {point}{drift_words}. {helm_text}"
        words = words.rstrip()
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
