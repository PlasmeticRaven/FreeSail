"""The ground tackle's orders (spec M5 §18; package 34; decision 30): what the captain
says to the forecastle about the anchors and the cable.

    come to an anchor [with the small bower] [in <n> fathoms]
                                    Luce's evolution whole: the sails in, head to wind or
                                    tide, let go with the way off her, the cable veered
                                    to the scope the depth wants, the sails furled
    let go the best bower           the anchor let go where she is, whatever her way
    let go the second anchor        the bower not yet down (when the first drags)
    veer cable [<n> fathoms]        more cable on the anchor she rides by
    veer to <n> fathoms             the scope veered to
    heave short                     the cable in to a short stay
    weigh                           the anchor hove up, catted and fished; the time by the
                                    scope
    cat and fish the anchor         an anchor left aweigh secured
    back the anchor                 the stream anchor let go on the riding cable
    the ground tackle               the anchors and their cables (a query)

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
    "weigh": "weigh_anchor",
    "cat and fish the anchor": "cat_and_fish_anchor",
    "back the anchor": "back_anchor",
}

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
    fathoms, remainder = _fathoms(rest)
    if fathoms is not None:
        params["fathoms"] = fathoms
    if verb == "veer cable":
        if phrase.endswith(" to") or remainder.strip().startswith("to "):
            params["to"] = True
        rest_words = remainder.strip()
        if fathoms is None and rest_words and rest_words not in ("away", "to"):
            raise OrderError(
                "Veer how much? Say 'veer twenty fathoms', 'veer to ninety fathoms' or "
                "'veer cable'."
            )
    elif verb in (
        "come to an anchor",
        "let go the anchor",
        "cat and fish the anchor",
        "back the anchor",
    ):
        words = _anchor_words(remainder)
        if words and named is None:
            named = words
        if named is not None:
            params["anchor"] = named
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
