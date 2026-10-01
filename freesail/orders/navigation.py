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
    shape a course for <place>      the course from the reckoning to a place of the chart

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
        heading, words = nav.shape_course(rest)
        from freesail.orders import handle

        _, helm_text, helm_data = handle(ship, f"steer {units.rad_to_deg(heading):.0f}")
        data = {"verb": verb, "level": 1, "place": rest, "heading": heading} | {"helm": helm_data}
        return "helm.set", f"{words} {helm_text}", data
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
