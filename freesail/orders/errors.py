"""The sentences an order is refused with.

Every refusal is an `OrderError` whose message is a plain sentence written
for the ship's log. The message is the player's main teacher, so each one
says three things where it can: what was understood, what was not, and the
nearest things that would have been. The helpers here build those sentences
so that every module refuses in the same voice.

`OrderError` itself is defined in `freesail.ship.stub` (the World catches
that class), and is re-exported here for convenience.
"""

from __future__ import annotations

import difflib
from collections.abc import Iterable

from freesail.ship.stub import OrderError


class UnknownNounError(OrderError):
    """The object phrase names nothing in this ship."""


class AmbiguousNounError(OrderError):
    """The object phrase could name several parts; the candidates are in the message."""


class UnknownVerbError(OrderError):
    """The words begin with no verb this ship knows (package 33c: the prompt then asks
    whether they name a reading or a part, `orders.prompt.answer_unparsed`)."""


class NothingToDoError(OrderError):
    """Every part the order named was already dealt with by an earlier order in the same group."""


__all__ = [
    "OrderError",
    "UnknownNounError",
    "UnknownVerbError",
    "AmbiguousNounError",
    "join_names",
    "nearest",
    "suggest",
    "ambiguous_noun",
    "unknown_noun",
    "unknown_verb",
    "unknown_words",
    "wrong_kind",
]

# How many candidates a message lists before saying "and N more".
MAX_LISTED = 6


def join_names(names: Iterable[str], conjunction: str = "or", limit: int = MAX_LISTED) -> str:
    """'a, b or c' from a list of names, with 'and N more' past `limit`."""
    names = list(names)
    if not names:
        return ""
    if len(names) > limit:
        shown = names[:limit]
        more = len(names) - limit
        return ", ".join(shown) + (" and one more" if more == 1 else f" and {more} more")
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + f" {conjunction} " + names[-1]


def nearest(word: str, known: Iterable[str], n: int = 3, cutoff: float = 0.6) -> list[str]:
    """The `n` known names closest in spelling to `word`, best first.

    Uses difflib, which is deterministic: the same inputs always give the
    same suggestions in the same order. Names that *contain* the word are
    put first, since "topsail" is a better hint for "tops" than "tops'l" is.
    """
    known = list(dict.fromkeys(known))  # unique, order kept
    word = word.strip().lower()
    if not word:
        return []
    containing = [k for k in known if word in k and k != word]
    containing.sort(key=lambda k: (len(k), k))
    close = difflib.get_close_matches(word, known, n=n, cutoff=cutoff)
    out: list[str] = []
    for k in containing[:n] + close:
        if k not in out and k != word:
            out.append(k)
    return out[:n]


def suggest(word: str, known: Iterable[str], article: str = "the ") -> str:
    """'; did you mean the X or the Y?' or '' when nothing is close."""
    hints = nearest(word, known)
    if not hints:
        return ""
    return "; did you mean " + join_names(f"{article}{h}" for h in hints) + "?"


def unknown_verb(text: str, verbs: Iterable[str]) -> UnknownVerbError:
    """'X is not an order this ship understands; did you mean 'set' or 'steer'?'"""
    verbs = list(verbs)
    words = text.split()
    # Try the first one or two words: most verbs are one word, some are two.
    # The closer spelling comes first, whichever length found it.
    scored: dict[str, float] = {}
    for n in (2, 1):
        if len(words) >= n:
            said = " ".join(words[:n])
            for h in nearest(said, verbs, n=2):
                ratio = difflib.SequenceMatcher(None, said, h).ratio()
                scored[h] = max(scored.get(h, 0.0), ratio)
    hints = sorted(scored, key=lambda h: -scored[h])
    hint = ("; did you mean " + join_names(f"'{h}'" for h in hints[:3]) + "?") if hints else "."
    return UnknownVerbError(
        f"'{text}' is not an order this ship understands{hint} "
        f"An order begins with a verb such as {join_names(verbs[:8], 'or', limit=8)}."
    )


def sentence_list(items: Iterable[str]) -> str:
    """'a; b; c' from sentences, each with its final full stop removed."""
    return "; ".join(s.strip().rstrip(".") for s in items if s.strip())


def unknown_noun(phrase: str, verb: str, known: Iterable[str]) -> OrderError:
    """'There is no such part as the X in this ship; did you mean the Y?'"""
    hint = suggest(phrase, known) or "."
    return UnknownNounError(
        f"There is no such part as the {phrase} in this ship{hint} ('{verb}' was understood.)"
    )


def ambiguous_noun(phrase: str, candidates: Iterable[str], verb: str) -> OrderError:
    """'The topsail could be the fore topsail, the main topsail or ...; say which.'"""
    return AmbiguousNounError(
        f"The {phrase} could be "
        + join_names(f"the {c}" for c in candidates)
        + f"; say which ('{verb}' was understood)."
    )


def unknown_words(words: Iterable[str], verb: str, known: Iterable[str]) -> OrderError:
    """After a verb and object were understood, some words remained that were not."""
    words = list(words)
    known = list(known)
    phrase = " ".join(words)
    hints = []
    for w in words:
        for h in nearest(w, known, n=1):
            if h not in hints:
                hints.append(h)
    hint = ("; did you mean " + join_names(f"'{h}'" for h in hints) + "?") if hints else ""
    return OrderError(
        f"'{verb}' was understood, but not '{phrase}'{hint} "
        f"(Punctuation and 'the' are ignored; the rest must be a part, a side, a heading or "
        f"a modifier such as 'sharp up', 'one reef' or 'a fathom'.)"
    )


def wrong_kind(verb: str, name: str, what_it_is: str, wanted: str, hint: str = "") -> OrderError:
    """'You set sails; the fore topsail sheet is a line. Did you mean ...?'"""
    tail = f" {hint}" if hint else ""
    return OrderError(f"You {verb} {wanted}; the {name} is {what_it_is}.{tail}")
