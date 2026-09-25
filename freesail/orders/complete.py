"""Suggestions for a half-typed order (package 14).

The grammar is data, so completion is a lookup: which verb phrases could
start what was typed; then which of this ship's nouns could follow the verb;
then which modifiers the verb accepts. Every suggestion is a whole order the
parser would take, or a longer prefix of one. Nothing is invented: nouns come
from the ship's noun table and verbs and modifiers from the vocabulary.

`suggestions(ship, text)` returns full-line candidates that begin with `text`
(compared with the same normalisation the parser uses), most useful first,
at most `limit`. The console and the browser client show them as the player
types.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from freesail import units
from freesail.orders import resolve
from freesail.orders.vocabulary import Vocabulary, load_vocabulary, normalise

DRIVER_COMMANDS = (
    "hold",
    "go",
    "time ",
    "tick ",
    "state",
    "log",
    "save ",
    "replay ",
    "help",
    "quit",
)
POINT_SHIP_ORDERS = ("steer ", "speed ", "stop")


@lru_cache(maxsize=1)
def _vocab() -> Vocabulary:
    return load_vocabulary()


def _compass_names() -> list[str]:
    return [units.point_full_name(a) for a in units.COMPASS_ABBREVIATIONS]


def _modifiers_for(spec_object: str, verb: str, vocab: Vocabulary, sided: bool) -> list[str]:
    """Modifier phrases that may follow a complete noun for this verb."""
    out: list[str] = []
    if verb == "brace":
        # "square" and "back" say how in the verb itself, so they take no mode
        out += list(vocab.brace_modes)
        out += [f"{m} on the starboard tack" for m in ("sharp up", "up", "in", "square")]
        out += [f"{m} on the larboard tack" for m in ("sharp up", "up", "in", "square")]
    elif verb == "reef":
        out += ["one reef", "two reefs", "three reefs", "close"]
    elif verb == "shake out":
        out += ["one reef", "two reefs", "all reefs"]
    elif verb == "haul":
        out += ["home", "aft", "a fathom", "two fathoms", "a little", "handsomely", "roundly"]
    elif spec_object == "line":
        out += ["a fathom", "two fathoms", "a little", "handsomely", "roundly"]
    if sided:
        out += [", starboard", ", larboard", ", both sides"]
    return out


def _noun_candidates(ship: Any, spec_object: str, verb: str) -> list[tuple[str, bool]]:
    """(noun phrase, is_sided) pairs that make sense for the verb's object kind.

    Built from the parts themselves (display and family names, with the
    weather and lee forms the parser resolves at parse time), the ship's
    groups and its aliases, then filtered by what the verb takes.
    """
    wanted = {"sail": {"sail"}, "line": {"line"}, "yards": {"yard", "sail"}}.get(spec_object)
    if wanted is None:
        return []
    phrases: dict[str, list[str]] = {}

    def put(phrase: str, ids: list[str]) -> None:
        if phrase and phrase not in phrases:
            phrases[phrase] = ids

    kinds_of = {pid: resolve.kind_of(part) for pid, part in ship.parts.items()}
    families: dict[tuple[str, str], list[str]] = {}
    for pid, part in ship.parts.items():
        put(resolve.display_name(ship, pid), [pid])
        if getattr(part, "side", None):
            fam = resolve.family_name(ship, pid)
            families.setdefault((fam, kinds_of[pid]), []).append(pid)
    for (fam, kind), ids in families.items():
        put(fam, ids)
        put(f"weather {fam}", ids)
        put(f"lee {fam}", ids)
        if kind == "line":
            put(resolve.pluralise(fam), ids)  # "main braces": both sides
    for name, members in ship.groups.items():
        put(name, list(members))
    for alias, target in ship.aliases.items():
        put(alias, list(ship.groups.get(target, [target])))

    out: list[tuple[str, bool]] = []
    for phrase, ids in phrases.items():
        parts = [ship.parts[i] for i in ids if i in ship.parts]
        if not parts:
            continue
        kinds = {kinds_of[p.id] for p in parts}
        if not kinds <= wanted:
            continue
        if spec_object == "yards" and kinds == {"sail"}:
            if not all(p.cls == "square" for p in parts):
                continue
        sided = (
            spec_object == "sail"
            and len(parts) > 1
            and all(getattr(p, "side", None) for p in parts)
        )
        out.append((phrase, sided))
    return out


def _starts(candidate: str, typed: str) -> bool:
    return normalise(candidate).startswith(typed)


def suggestions(ship: Any, text: str, limit: int = 12) -> list[str]:
    """Whole-line completions for `text`, most useful first."""
    typed = normalise(text)
    trailing = text.endswith(" ") or text.endswith(",")
    vocab = _vocab()
    out: list[str] = []

    def offer(candidate: str) -> None:
        if _starts(candidate, typed) and normalise(candidate) != typed and candidate not in out:
            out.append(candidate)

    # driver commands and, for the M0 point ship, its three orders
    if not hasattr(ship, "parts"):
        for c in POINT_SHIP_ORDERS + DRIVER_COMMANDS:
            offer(c)
        if typed.startswith("steer "):
            for name in _compass_names():
                offer(f"steer {name}")
        return out[:limit]

    # which verb phrase, if any, has been typed in full?
    matched: str | None = None
    for phrase in vocab.verb_phrases:  # longest first
        p = normalise(phrase)
        if typed == p or typed.startswith(p + " "):
            matched = phrase
            break
    if matched is None:
        for phrase in vocab.verb_phrases:
            offer(
                phrase + " "
                if vocab.verbs[vocab.phrase_to_verb[normalise(phrase)]].object != "none"
                else phrase
            )
        for c in DRIVER_COMMANDS:
            offer(c)
        return sorted(out, key=lambda s: (len(s), s))[:limit]

    verb = vocab.phrase_to_verb[normalise(matched)]
    spec = vocab.verbs[verb]
    rest = typed[len(normalise(matched)) :].strip()
    prefix = matched + " "

    if spec.object in ("heading", "points"):
        for name in _compass_names():
            offer(prefix + name)
        for n in ("one point", "two points", "three points", "four points"):
            for side in ("to starboard", "to larboard"):
                offer(prefix + f"{n} {side}")
        return out[:limit]

    if spec.object == "none":
        return out[:limit]

    nouns = _noun_candidates(ship, spec.object, verb)
    if verb == "brace" and not rest and normalise(matched) != "lay":
        for m in _modifiers_for(spec.object, verb, vocab, False):
            offer(prefix + m)
    article_taken = normalise(matched).split()[-1] == "the"  # "take in the" is a verb phrase
    for phrase, sided in nouns:
        if article_taken or phrase.startswith("the "):
            forms: tuple[str, ...] = (phrase,)
        else:
            forms = (f"the {phrase}", phrase)
        for form in forms:
            offer(prefix + form)
            head = normalise(prefix + form)
            if (typed == head and trailing) or typed.startswith((head + " ", head + ",")):
                for m in _modifiers_for(spec.object, verb, vocab, sided):
                    joiner = "" if m.startswith(",") else " "
                    offer(prefix + form + joiner + m)
    # brace modes first, then the shorter, article-bearing forms
    modes = {prefix + m for m in _modifiers_for(spec.object, verb, vocab, False)}
    out.sort(key=lambda s: (s not in modes, not s.startswith(prefix + "the "), len(s), s))
    return out[:limit]
