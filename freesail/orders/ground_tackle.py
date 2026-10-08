"""The ground tackle's orders (spec M5 §18; package 34; decision 30): what the captain
says to the forecastle about the anchors and the cable.

    come to an anchor [with the small bower] [in <n> fathoms]
                                    Luce's evolution whole: the sails in, head to wind or
                                    tide, let go with the way off her, the cable veered
                                    to the scope the depth wants, the sails furled
    let go the best bower           the anchor let go where she is, whatever her way
    let go the second anchor        the bower not yet down (when the first drags)
    let go the best bower and veer to <n> fathoms
                                    the same, the cable veered to that scope and no further
                                    (`with <n> fathoms`, `in <n> fathoms` likewise)
    veer cable [<n> fathoms]        more cable on the anchor she rides by
    veer to <n> fathoms             the scope veered to
    veer the small bower to <n> fathoms
                                    on the anchor named (package 37f)
    heave short                     the cable in to a short stay; no number
    heave in <n> fathoms            so much of the cable hove in at the capstan
    heave in to <n> fathoms         the cable hove in to that scope (package 37f)
    weigh                           the anchor hove up, catted and fished; the time by the
                                    scope; no sail set (the owner, 2026-10-02)
    weigh the small bower           the anchor named, the other cable veered as it comes
                                    in, or refused in words that name the anchor she rides
                                    by (package 37f)
    cat and fish the anchor         an anchor left aweigh secured
    back the anchor                 the stream anchor let go on the riding cable
    the ground tackle               the anchors and their cables (a query)

and the port's (spec M5 §23; package 35):

    get under way [on the <tack> tack] [and steer <course>]
                                    Luce's whole sequence: heave short, loose and sheet
                                    home the topsails, weigh, cast her on the tack the
                                    pilot wants, the anchor catted and fished as she pays
                                    off; the pilot's tack and course when he is aboard
    moor [with the small bower]     a second anchor laid, a cable each way, the hawse open
    unmoor                          the lee anchor hove up, to single anchor
    lay out a kedge [to the <point>] [<n> fathoms]
                                    the kedge carried out by the boat and let go there

Each is a verb of `data/vocabulary.yaml` with the object `anchor`: the grammar takes the
words after the verb as they are, and this module reads an anchor's name and a number of
fathoms from them and starts the evolution (`data/evolutions/*_anchor.yaml`,
`veer_cable.yaml`, `heave_short.yaml`) on the ship through the runner, as the manoeuvres
are started (`orders.verbs._ship_evolution`). A ship whose file lists no ground tackle
refuses them in words. `orders.handle` hands an order with this object here.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.api import readings as _readings
from freesail.orders import verbs
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.ship.parts import ground_tackle

__all__ = ["NO_TACKLE_WORDS", "execute"]

# one sentence with the registry's (`api.readings`), which an agent reads
NO_TACKLE_WORDS = _readings.NO_TACKLE_WORDS

Result = tuple[str, str, dict[str, Any]]

# The evolution each verb starts.
_EVOLUTIONS = {
    "come to an anchor": "come_to_anchor",
    "let go the anchor": "let_go_anchor",
    "veer cable": "veer_cable",
    "heave short": "heave_short",
    "heave in": "heave_in",
    "weigh": "weigh_anchor",
    "cat and fish the anchor": "cat_and_fish_anchor",
    "back the anchor": "back_anchor",
    # the port (package 35; spec M5 §23): Luce's whole getting under way, the moor and
    # the unmoor, and a kedge laid out by the boat
    "get under way": "get_under_way",
    "moor": "moor",
    "unmoor": "unmoor",
    "lay out a kedge": "lay_out_kedge",
}

_TACK_RE = re.compile(r"\b(?:on|to)?\s*(?:the\s+)?(starboard|larboard|port)\s+tack\b")
_COURSE_RE = re.compile(r"\b(?:and\s+)?(?:steer|steering|course)\s+(?P<course>[\w\s]+?)\s*$")

_FATHOMS_RE = re.compile(r"(?P<n>\d+(?:\.\d+)?|[a-z]+(?:\s+and\s+a\s+half)?)\s+fathoms?\b")
_NUMBER_WORDS = {
    "ten": 10,
    "twelve": 12,
    "fifteen": 15,
    "twenty": 20,
    "twenty five": 25,
    "thirty": 30,
    "forty": 40,
    "forty five": 45,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "seventy five": 75,
    "eighty": 80,
    "ninety": 90,
    "a hundred": 100,
    "hundred": 100,
    "a hundred and twenty": 120,
}


def _fathoms(text: str) -> tuple[float | None, str]:
    """A number of fathoms in the words, and the words without it."""
    low = text.lower()
    for words, n in sorted(_NUMBER_WORDS.items(), key=lambda kv: -len(kv[0])):
        if re.search(rf"\b{words}\s+fathoms?\b", low):
            return float(n), re.sub(rf"\b{words}\s+fathoms?\b", " ", low)
    m = _FATHOMS_RE.search(low)
    if m is None:
        return None, low
    try:
        n = float(m.group("n"))
    except ValueError:
        raise OrderError(
            f"'{m.group('n')} fathoms' is not a number of fathoms I can read."
        ) from None
    return n, low[: m.start()] + " " + low[m.end() :]


def _anchor_words(text: str) -> str | None:
    """The anchor named in the words after the verb, if any ('with the small bower',
    'the sheet anchor', 'second anchor'), else None (the best bower, or the one down)."""
    words = re.sub(r"\b(with|on|by|the|in|to|her)\b", " ", text.lower())
    words = " ".join(words.split())
    return words or None


# The words about a cable that name no anchor and no number: left out before an anchor's
# name is looked for in an order to veer, heave in or weigh (package 37f).
_CABLE_FILLERS = re.compile(
    r"\b(with|on|by|the|in|to|her|of|and|a|an|cable|cables|more|away|out|scope|veer|veering|"
    r"anchor|upon)\b"
)
# The orders that work a cable already out, each on the anchor named or the one she rides by.
_CABLE_VERBS = ("veer cable", "heave short", "heave in", "weigh")
# "in twelve fathoms", "in 12 fathoms of water": a depth, unless it is "of cable"
_DEPTH_RE = re.compile(
    r"\bin\s+(?P<n>\d+(?:\.\d+)?|[a-z]+(?:\s+[a-z]+)??(?:\s+and\s+a\s+half)?)\s+fathoms?"
    r"(?:\s+of\s+water|\s+water)?\b(?!\s+of\s+cable)"
)


def _depth_said(text: str) -> tuple[float | None, str]:
    """'in twelve fathoms' after `come to an anchor`: the depth to let go in, and the
    words without it; (None, the words) when none is said."""
    low = text.lower()
    m = _DEPTH_RE.search(low)
    if m is None:
        return None, text
    n, _ = _fathoms(m.group("n") + " fathoms")
    if n is None:
        return None, text
    return n, low[: m.start()] + " " + low[m.end() :]


def _named_anchor(ship: Any, phrase: str, remainder: str) -> tuple[str | None, str]:
    """The anchor an order to veer, heave in or weigh names, in the verb's own phrase
    ('weigh the small bower') or after it ('veer the best bower to 80 fathoms', 'veer to
    80 fathoms on the best bower'), as the words `GroundTackle.by_words` takes; None when
    it names none; and whatever words are left that are neither (the refusal names them)."""
    named = _anchor_in_phrase(phrase)
    left = " ".join(_CABLE_FILLERS.sub(" ", remainder.lower()).split())
    if not left:
        return named, ""
    tackle = ground_tackle(ship)
    found = _anchor_in_phrase(left)
    if found is not None and tackle is not None and tackle.by_words(found) is not None:
        rest = left
        for words, _name in _PHRASE_ANCHORS:
            rest = re.sub(rf"\b{words}\b", " ", rest)
        rest = " ".join(w for w in rest.split() if w not in ("bower", "anchor"))
        return found, rest
    if tackle is not None and tackle.by_words(left) is not None:
        return left, ""
    return named, left


def execute(ship: Any, order: Order) -> Result:
    """Carry out a ground-tackle order. The verb is the vocabulary's key."""
    verb = order.verb
    evo = _EVOLUTIONS.get(verb)
    if evo is None:
        raise OrderError(f"'{verb}' is not a ground-tackle order this ship knows.")
    if ground_tackle(ship) is None:
        raise OrderError(NO_TACKLE_WORDS)
    rest = (order.object or "").strip()
    phrase = order.verb_phrase
    params: dict[str, Any] = {}
    # the anchor named in the verb's own phrase ("let go the small bower") or after it
    named = _anchor_in_phrase(phrase) or None
    if verb == "come to an anchor":
        # "in twelve fathoms" is the depth to let go in, as the primer has it (package
        # 37f; the review of gate 5c's playtests, 5.8: it was taken for the scope)
        depth_said, rest = _depth_said(rest)
        if depth_said is not None:
            params["depth_fathoms"] = depth_said
    fathoms, remainder = _fathoms(rest)
    if fathoms is not None:
        params["fathoms"] = fathoms
    if verb in _CABLE_VERBS:
        # Package 37f (the review of gate 5c's playtests, 10.4): an anchor's name is
        # honoured by every order that works a cable, and "to" is kept wherever it is
        # said. Until now the name reached five verbs only, and "to" was looked for where
        # the number had been: `veer the best bower to 80 fathoms` veered eighty more, and
        # `weigh the small bower` weighed the best bower without a word.
        name, left = _named_anchor(ship, phrase, remainder)
        if name is not None:
            params["anchor"] = name
        said_to = phrase.endswith(" to") or bool(re.search(r"\bto\b", remainder.lower()))
        if verb == "veer cable":
            if fathoms is not None and said_to:
                params["to"] = True
            if left or (fathoms is None and said_to):
                if fathoms is None:
                    raise OrderError(
                        "Veer how much? Say 'veer twenty fathoms', 'veer to ninety fathoms' "
                        "or 'veer cable'."
                    )
                raise OrderError(
                    f"'{left}' was not understood after 'veer'. Say 'veer twenty fathoms', "
                    "'veer to ninety fathoms', 'veer the small bower to ninety fathoms' or "
                    "'veer cable'."
                )
        elif verb == "heave short":
            if fathoms is not None:
                # `heave short` takes no number (the review's 5.8: `heave in 70 fathoms`
                # ran as `heave short` and 163 fathoms came in)
                n = f"{fathoms:g}"
                raise OrderError(
                    f"'Heave short' takes no number: it heaves in to a short stay, a cable and "
                    f"a half the depth. To heave in to a scope say 'heave in to {n} fathoms'; "
                    f"to heave in so much, 'heave in {n} fathoms'."
                )
            if left:
                raise OrderError(
                    f"'{left}' was not understood after 'heave short'; say 'heave short' or "
                    "'heave short on the small bower'."
                )
        elif verb == "heave in":
            if left:
                raise OrderError(
                    f"'{left}' was not understood after 'heave in'; say 'heave in twenty "
                    "fathoms', 'heave in to eighty fathoms' or 'heave in the small bower to "
                    "eighty fathoms'."
                )
            if fathoms is None:
                # "heave in", "heave in the cable": to a short stay, as it always was
                evo = _EVOLUTIONS["heave short"]
                verb = "heave short"
            elif said_to:
                params["to"] = True
        else:
            if fathoms is not None:
                raise OrderError("'Weigh' takes no number: it heaves the anchor up to the bows.")
            if left:
                raise OrderError(
                    f"'{left}' was not understood after 'weigh'; say 'weigh' or 'weigh the "
                    "small bower'."
                )
    elif verb in (
        "come to an anchor",
        "let go the anchor",
        "cat and fish the anchor",
        "back the anchor",
        "moor",
    ):
        low = remainder.lower()
        if verb in ("come to an anchor", "let go the anchor"):
            # "... and veer to 45 fathoms", "... with 45 fathoms of cable": the scope to
            # veer, and no further (package 37f; the owner's ruling: `let go` keeps the
            # scope the depth wants, says it, and takes a number). After `let go`, which
            # lets go where she is, "in twenty fathoms" is the scope too, as it always was.
            if fathoms is None and re.search(r"\b(veer|veering|scope)\b", low):
                raise OrderError(
                    "Veer to how much? Say 'let go the best bower and veer to forty-five "
                    "fathoms', or 'let go the best bower' for five times the depth."
                )
            if fathoms is not None:
                low = re.sub(
                    r"\b(and|veer|veering|to|scope|of|cable|out|a|water|depth)\b", " ", low
                )
        words = _anchor_words(low)
        if words and named is None:
            named = words
        if named is not None:
            params["anchor"] = named
    elif verb == "get under way":
        # the tack to cast on and the course to steer once she has cast (package 35):
        # 'get under way on the larboard tack', '... and steer S by E'; the pilot's when
        # none is said and he is aboard
        low = remainder.lower()
        m = _TACK_RE.search(low)
        if m:
            params["tack"] = "larboard" if m.group(1) == "port" else m.group(1)
            low = low[: m.start()] + " " + low[m.end() :]
        c = _COURSE_RE.search(low)
        if c:
            from freesail import units

            heading = units.parse_compass_point(c.group("course").strip())
            if heading is None:
                try:
                    heading = units.deg_to_rad(float(c.group("course").strip()))
                except ValueError:
                    raise OrderError(
                        f"'{c.group('course').strip()}' is not a course to steer once she has cast."
                    ) from None
            params["course_deg"] = units.rad_to_deg(heading)
            low = low[: c.start()] + " " + low[c.end() :]
        left = " ".join(w for w in low.split() if w not in ("and", "the", "on", "to", "her"))
        if left:
            raise OrderError(
                f"'{left}' was not understood after 'get under way'; say 'get under way', "
                "'get under way on the larboard tack' or '... and steer S by E'."
            )
    elif verb == "lay out a kedge":
        # the bearing to lay it out on, and the fathoms of hawser (package 35)
        low = remainder.lower()
        low = re.sub(r"\b(to|toward|towards|the|of|hawser|with|out)\b", " ", low).strip()
        if low:
            from freesail import units

            toward = units.parse_compass_point(low)
            if toward is None:
                raise OrderError(
                    f"'{low}' is not a bearing to lay the kedge out on; say 'lay out a kedge to "
                    "the NE', with the fathoms of hawser if you like."
                )
            params["toward_deg"] = units.rad_to_deg(toward)
    elif remainder.strip():
        raise OrderError(
            f"'{verb}' takes nothing after it; '{remainder.strip()}' was not understood."
        )
    runner = verbs.runner_of(ship)
    text = runner.start(ship, evo, verbs.SHIP_SUBJECT, params)
    data = {
        "verb": verb,
        "level": 1,
        "subjects": [verbs.SHIP_SUBJECT],
        "evolutions": [{"evolution": evo, "subject": verbs.SHIP_SUBJECT, "params": params}],
        "failed": [],
    }
    return "evolution.started", text, data


_PHRASE_ANCHORS = (
    ("best bower", "best bower"),
    ("small bower", "small bower"),
    ("sheet", "sheet"),
    ("stream", "stream"),
    ("kedge", "kedge"),
    ("second", "second"),
    ("other", "second"),
    ("lee bower", "second"),
    ("weather bower", "best bower"),
    ("starboard", "best bower"),
    ("larboard", "small bower"),
    ("port", "small bower"),
)


def _anchor_in_phrase(phrase: str) -> str | None:
    low = phrase.lower()
    for words, name in _PHRASE_ANCHORS:
        if re.search(rf"\b{words}\b", low):
            return name
    return None
