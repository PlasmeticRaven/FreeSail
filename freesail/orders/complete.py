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
    "muster",
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


def _hands_phrases(ship: Any, vocab: Vocabulary) -> list[str]:
    """The hands this ship can name: the two watches, then her company's stations."""
    crew = ship.extra.get("crew") if hasattr(ship, "extra") else None
    stations = set()
    if crew is not None:
        stations = {s.station.value for s in crew.sailors}
    out: list[str] = []
    seen: set[str] = set()
    for phrase, value in vocab.hands_selectors.items():
        if value in seen or phrase == "port watch":
            continue
        if value in ("starboard", "larboard") or value in stations:
            out.append(phrase)
            seen.add(value)
    return out


def _with_hands(ship: Any, vocab: Vocabulary) -> list[str]:
    """'with the starboard watch', 'with the fore topmen' ..."""
    return [f"with the {h}" for h in _hands_phrases(ship, vocab)]


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

    # "send the larboard watch aloft to ...": the hands, then any order after them
    if typed.startswith("send") and not typed.startswith("send down"):
        return _send(ship, text, typed, limit)

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
                if vocab.verbs[vocab.phrase_to_verb[normalise(phrase)]].object
                not in ("none", "driver")
                else phrase
            )
        offer("send the ")
        for c in DRIVER_COMMANDS:
            offer(c)
        # the verbs' own names before their synonyms, then the shortest first
        return sorted(out, key=lambda s: (normalise(s) not in vocab.verbs, len(s), s))[:limit]

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
        if verb in vocab.group_evolutions:
            for m in _with_hands(ship, vocab):
                offer(prefix + m)
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
                mods = _modifiers_for(spec.object, verb, vocab, sided)
                if spec.object in ("sail", "yards"):
                    mods += _with_hands(ship, vocab)
                for m in mods:
                    joiner = "" if m.startswith(",") else " "
                    offer(prefix + form + joiner + m)
    # brace modes first, then the shorter, article-bearing forms
    modes = {prefix + m for m in _modifiers_for(spec.object, verb, vocab, False)}
    out.sort(key=lambda s: (s not in modes, not s.startswith(prefix + "the "), len(s), s))
    return out[:limit]


def _sets_hands_to_work(order: str) -> bool:
    """Whether an order is work a watch or a station can be sent to: a sail, a yard, a
    group evolution or a ship evolution, not a line, the helm or the console."""
    vocab = _vocab()
    typed = normalise(order)
    for phrase in vocab.verb_phrases:  # longest first
        p = normalise(phrase)
        if typed == p or typed.startswith(p + " "):
            verb = vocab.phrase_to_verb[p]
            spec = vocab.verbs[verb]
            if spec.object in ("sail", "yards"):
                return True
            return spec.object == "none" and (
                verb in vocab.group_evolutions or isinstance(vocab.evolutions.get(verb), str)
            )
    return False


def _send(ship: Any, text: str, typed: str, limit: int) -> list[str]:
    """Completions for 'send the larboard watch aloft to loose the fore topsail'."""
    vocab = _vocab()
    words = typed.split()
    i = 2 if len(words) > 1 and words[1] == "the" else 1
    for phrase in _hands_phrases(ship, vocab):
        head = ["send", "the", *phrase.split()] if i == 2 else ["send", *phrase.split()]
        if words[: len(head)] != head:
            continue
        rest = words[len(head) :]
        for direction in ("", *vocab.send_directions):
            lead = direction.split() + ["to"]
            if rest[: len(lead)] == lead and (len(rest) > len(lead) or text.endswith(" ")):
                said = " ".join(head + lead) + " "
                inner = typed[len(said) :]
                if inner and text.endswith(" "):
                    inner += " "
                orders = [s for s in suggestions(ship, inner, limit * 3) if _sets_hands_to_work(s)]
                return [said + s for s in orders][:limit]
    out: list[str] = []
    for phrase in _hands_phrases(ship, vocab):
        for c in (f"send the {phrase} aloft to ", f"send the {phrase} to "):
            if normalise(c).startswith(typed) and normalise(c) != typed and c not in out:
                out.append(c)
    return out[:limit]
