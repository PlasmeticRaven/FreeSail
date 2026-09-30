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

import re
from typing import Any

from freesail import units
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.world.geo import parse_position

__all__ = ["NO_RECKONING_WORDS", "execute"]

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
        text, data = nav.take_bearing(rest)
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
