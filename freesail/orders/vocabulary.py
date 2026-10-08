"""Loads `data/vocabulary.yaml`: the words of Orders that are true of every ship.

The file holds the verbs and their synonyms, the modifier words, the number
words, the contraction rules that generate part names ("tops'l" for
"topsail"), and the group evolutions ("make all sail") as lists of orders.
It is read once and shared. Nothing here knows about a particular ship;
ship nouns come from the ship file and are built in `resolve.py`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "data" / "vocabulary.yaml"


@dataclass(frozen=True)
class VerbSpec:
    """One verb of the table: its canonical name, what it takes, and its level."""

    name: str
    synonyms: tuple[str, ...]
    object: str  # sail | yards | line | heading | points | none | work | driver
    level: str  # "0", "1" or "driver"


@dataclass
class Vocabulary:
    verbs: dict[str, VerbSpec]
    phrase_to_verb: dict[str, str]  # every verb phrase and synonym -> canonical name
    evolutions: dict[str, Any]  # verb -> {sail class -> evolution id} or verb -> id
    refusals: dict[str, str]
    brace_modes: dict[str, float | str]  # phrase -> degrees, or "limit" | "aback" | "wind"
    sides: dict[str, str]  # word -> starboard | larboard | weather | lee
    both_sides: tuple[str, ...]
    manner: tuple[str, ...]
    a_little: tuple[str, ...]
    reef_close: tuple[str, ...]
    tack_phrase: tuple[str, ...]
    point_directions: dict[str, str]
    numbers: dict[str, float]
    contractions: dict[str, tuple[str, ...]]
    droppable_inner_words: tuple[str, ...]
    group_evolutions: dict[str, list[str]]
    source: str = ""
    verb_phrases: list[str] = field(default_factory=list)  # longest first, for matching
    # modifiers a verb phrase carries in itself: "close reef" -> {close: True}
    phrase_modifiers: dict[str, dict[str, Any]] = field(default_factory=dict)
    # words after a line's name meaning "all the way in": "haul the jib sheet aft"
    haul_home: tuple[str, ...] = ()
    # the take-in phrases that suit each class of sail (the first is the proper word)
    take_in_words: dict[str, tuple[str, ...]] = field(default_factory=dict)
    # hands selectors: "larboard watch" -> "larboard", "fore topmen" -> "fore_top"
    hands_selectors: dict[str, str] = field(default_factory=dict)
    # the words between "send the larboard watch" and "to": "aloft", "forward"
    send_directions: tuple[str, ...] = ()
    # kinds of work by a noun, for `belay the reef` (package 29c): "reef" -> "reef"
    work_nouns: dict[str, str] = field(default_factory=dict)
    # words after a line's name meaning it is rove again: "reeve the sheet afresh" (31b)
    afresh: tuple[str, ...] = ()
    # words after a sheet's name saying which side it is hauled on: "haul the jib sheet to
    # windward" -> "weather", "... to leeward" -> "lee" (package 32e)
    sheet_to: dict[str, str] = field(default_factory=dict)
    # a reading asked at the prompt (package 33c): each query verb made of a registry
    # phrase -> that phrase as the registry has it ("the reckonings uncertainty" -> "the
    # reckoning's uncertainty"); `orders.prompt` answers them
    readings: dict[str, str] = field(default_factory=dict)
    # the words before a reading's that ask for it: "what is", "ask the master" (33c)
    asking: tuple[str, ...] = ()
    # the world-order channel's words (package 36; `freesail.world.orders`): the channels
    # a line may not open with at the captain's prompt, the words that name the channel,
    # and the sentence the captain's grammar refuses one with (truth 71)
    world_order_channels: tuple[str, ...] = ()
    world_order_words: tuple[str, ...] = ()
    world_order_refusal: str = ""
    # what undoes what (package 37g): the pairs of verbs of which the later undoes the
    # earlier on a shared part, each pair read both ways (`standing.runtime.undoes`, the
    # harness's detector for a station with authority)
    undoes: frozenset[frozenset[str]] = frozenset()
    # the orders that give up something of the ship's for good (package 37g): kept back
    # from the captain's general authority to work the ship (`agents.tools`)
    irrevocable: tuple[str, ...] = ()

    @property
    def class_bound_take_in_phrases(self) -> frozenset[str]:
        """The take-in synonyms that suit only some sails ('clew up', 'haul down')."""
        return frozenset(p for phrases in self.take_in_words.values() for p in phrases)

    @property
    def verb_names(self) -> list[str]:
        """Canonical verb names in file order (the order shown in error messages)."""
        return [v for v in self.verbs if self.verbs[v].level not in ("driver", READING_LEVEL)]


# ---------------------------------------------------------------------------
# Text normalisation, shared by the parser and the noun table
# ---------------------------------------------------------------------------

_PUNCT = re.compile(r"[^\w\s,'°]")
_DECIMAL = re.compile(r"(\d)\.(\d)")


def normalise(text: str) -> str:
    """Lower-case, curly apostrophes to straight, hyphens to spaces, other punctuation gone.

    Commas and apostrophes are kept: the comma separates the side of an
    order, and apostrophes are part of words such as "tops'l" and "nor'west".
    """
    t = text.lower().replace("’", "'").replace("‘", "'")
    t = t.replace("-", " ").replace("_", " ").replace("/", " ")
    # keep the point inside a number such as "280.5" through the punctuation sweep
    t = _DECIMAL.sub(lambda m: m.group(1) + "qdotq" + m.group(2), t)
    t = _PUNCT.sub(" ", t).replace("qdotq", ".")
    t = t.replace(",", " , ")
    return " ".join(t.split())


def key(phrase: str) -> str:
    """The form a phrase is matched in: normalised, with apostrophes removed."""
    return " ".join(normalise(phrase).replace("'", "").split())


def strip_article(words: list[str]) -> list[str]:
    """Drop a leading 'the' (or 'a', 'an' before a noun) from a word list."""
    if words and words[0] == "the":
        return words[1:]
    return words


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------


def _tuple(v: Any) -> tuple[str, ...]:
    return tuple(key(str(x)) for x in (v or []))


@lru_cache(maxsize=4)
def load_vocabulary(path: str | Path | None = None) -> Vocabulary:
    """Read the vocabulary file (once) into a `Vocabulary`."""
    p = Path(path) if path else DEFAULT_PATH
    data = yaml.safe_load(p.read_text(encoding="utf-8"))

    verbs: dict[str, VerbSpec] = {}
    phrase_to_verb: dict[str, str] = {}
    for name, spec in (data.get("verbs") or {}).items():
        name = key(name)
        syns = _tuple(spec.get("synonyms"))
        verbs[name] = VerbSpec(
            name=name,
            synonyms=syns,
            object=str(spec.get("object", "none")),
            level=str(spec.get("level", "1")),
        )
        phrase_to_verb[name] = name
        for s in syns:
            phrase_to_verb.setdefault(s, name)

    contractions: dict[str, tuple[str, ...]] = {}
    for word, alts in (data.get("contractions") or {}).items():
        contractions[key(word)] = tuple(key(a) for a in (alts or []) if key(a) != key(word))

    brace_modes: dict[str, float | str] = {}
    for phrase, target in (data.get("brace_modes") or {}).items():
        if isinstance(target, str):
            if target not in ("limit", "aback", "wind"):
                raise ValueError(
                    f"{p}: brace mode '{phrase}' is '{target}'; "
                    f"say degrees, 'limit', 'aback' or 'wind'."
                )
            brace_modes[key(phrase)] = target
        else:
            brace_modes[key(phrase)] = float(target)

    _aliases(data, verbs, phrase_to_verb, p)
    readings = _reading_verbs(data, verbs, phrase_to_verb)

    group_evolutions = {
        key(name): [str(o) for o in (orders or [])]
        for name, orders in (data.get("group_evolutions") or {}).items()
    }

    vocab = Vocabulary(
        verbs=verbs,
        phrase_to_verb=phrase_to_verb,
        evolutions={key(k): v for k, v in (data.get("evolutions") or {}).items()},
        refusals={key(k): str(v) for k, v in (data.get("refusals") or {}).items()},
        brace_modes=brace_modes,
        sides={key(k): str(v) for k, v in (data.get("sides") or {}).items()},
        both_sides=_tuple(data.get("both_sides")),
        manner=_tuple(data.get("manner")),
        a_little=_tuple(data.get("a_little")),
        reef_close=_tuple(data.get("reef_close")),
        tack_phrase=_tuple(data.get("tack_phrase")),
        point_directions={key(k): str(v) for k, v in (data.get("point_directions") or {}).items()},
        numbers={key(k): float(v) for k, v in (data.get("numbers") or {}).items()},
        contractions=contractions,
        droppable_inner_words=_tuple(data.get("droppable_inner_words")),
        group_evolutions=group_evolutions,
        source=str(p),
    )
    vocab.readings = readings
    vocab.asking = _tuple((data.get("reading_words") or {}).get("asking"))
    world_orders = data.get("world_orders") or {}
    vocab.world_order_channels = _tuple(world_orders.get("channels"))
    vocab.world_order_words = _tuple(world_orders.get("words"))
    vocab.world_order_refusal = str(world_orders.get("refusal") or "")
    vocab.verb_phrases = sorted(phrase_to_verb, key=lambda s: (-len(s.split()), -len(s), s))
    for phrase, mods in (data.get("phrase_modifiers") or {}).items():
        k = key(phrase)
        if k not in phrase_to_verb:
            raise ValueError(f"{p}: phrase_modifiers lists '{phrase}', which is not a verb phrase.")
        vocab.phrase_modifiers[k] = dict(mods or {})
    vocab.haul_home = _tuple(data.get("haul_home"))
    vocab.afresh = _tuple(data.get("afresh"))
    vocab.sheet_to = {
        key(phrase): str(value) for phrase, value in (data.get("sheet_to") or {}).items()
    }
    for cls, phrases in (data.get("take_in_words") or {}).items():
        vocab.take_in_words[str(cls)] = _tuple(phrases)
    vocab.hands_selectors = {
        key(phrase): str(value) for phrase, value in (data.get("hands_selectors") or {}).items()
    }
    vocab.send_directions = _tuple(data.get("send_directions"))
    for noun, verb in (data.get("work_nouns") or {}).items():
        if key(verb) not in verbs:
            raise ValueError(f"{p}: work_nouns gives '{noun}' the verb '{verb}', which is none.")
        vocab.work_nouns[key(noun)] = key(verb)
    for noun, verb in (data.get("more_work_nouns") or {}).items():
        if key(verb) not in verbs:
            raise ValueError(
                f"{p}: more_work_nouns gives '{noun}' the verb '{verb}', which is none."
            )
        vocab.work_nouns.setdefault(key(noun), key(verb))
    pairs: set[frozenset[str]] = set()
    for pair in data.get("undoes") or []:
        names = [key(str(v)) for v in pair or []]
        if len(names) != 2 or names[0] == names[1]:
            raise ValueError(f"{p}: undoes lists {pair!r}; a pair is two different verbs.")
        for name in names:
            if name not in verbs:
                raise ValueError(f"{p}: undoes names '{name}', which is no verb.")
        pairs.add(frozenset(names))
    vocab.undoes = frozenset(pairs)
    for verb in data.get("irrevocable") or []:
        if key(str(verb)) not in verbs:
            raise ValueError(f"{p}: irrevocable names '{verb}', which is no verb.")
    vocab.irrevocable = _tuple(data.get("irrevocable"))
    return vocab


# ---------------------------------------------------------------------------
# Package 33c: aliases, and the readings asked at the prompt
# ---------------------------------------------------------------------------

# The level of a reading's query verb: neither an order's nor the console's, and left out
# of `verb_names`, so that an order's refusal names the orders and not fifty readings.
READING_LEVEL = "reading"


def _aliases(
    data: dict[str, Any], verbs: dict[str, VerbSpec], phrase_to_verb: dict[str, str], p: Path
) -> None:
    """`aliases:` (package 33c): another phrase for an existing verb. A phrase some verb
    has already keeps it."""
    for phrase, verb in (data.get("aliases") or {}).items():
        if key(verb) not in verbs:
            raise ValueError(f"{p}: the alias '{phrase}' names '{verb}', which is no verb.")
        phrase_to_verb.setdefault(key(phrase), key(verb))


def _reading_verbs(
    data: dict[str, Any], verbs: dict[str, VerbSpec], phrase_to_verb: dict[str, str]
) -> dict[str, str]:
    """A query verb for each phrase of the readings registry (package 33c, a reading asked
    at the prompt), with the asking words before it as its synonyms: "the reckoning",
    "what is the reckoning", "ask the master the reckoning". The phrases are the
    registry's own (`freesail.api.readings.REGISTRY`), so a row registered there is a word
    here; a phrase without its article takes one too ("daylight", "the daylight"). The
    parametric phrase `the bearing of <mark>` is the verb "the bearing of", which takes the
    mark's words after it (object `reading`); a sail or a part by name is read by
    `orders.prompt` from the ship. A phrase an existing verb has stays that verb's.
    Returns each verb's registry phrase."""
    from freesail.api.readings import REGISTRY

    words = data.get("reading_words") or {}
    asking = [key(a) for a in words.get("asking") or []]
    named: dict[str, str] = {}  # the phrase as said -> the registry's phrase
    for row in REGISTRY:
        for phrase in row.words:
            if "<sail>" in phrase or "<part>" in phrase:
                continue
            said = phrase.split(" <")[0]
            named.setdefault(said, phrase)
            if not said.startswith(("the ", "what ", "a ")):
                named.setdefault(f"the {said}", phrase)
    for alias, phrase in (words.get("aliases") or {}).items():
        named.setdefault(str(alias), str(phrase))
    out: dict[str, str] = {}
    for said, phrase in named.items():
        verb = key(said)
        if verb in phrase_to_verb or verb in verbs:
            continue  # an order's words already
        bare = said.startswith(("what ", "a "))  # "what is in sight", "a sail in sight"
        forms = [said] if bare else [said] + [f"{a} {said}" for a in asking]
        synonyms = tuple(dict.fromkeys(key(f) for f in forms[1:]))
        verbs[verb] = VerbSpec(
            name=verb,
            synonyms=synonyms,
            object="reading" if "<" in phrase else "query",
            level=READING_LEVEL,
        )
        phrase_to_verb[verb] = verb
        for s in synonyms:
            phrase_to_verb.setdefault(s, verb)
        out[verb] = phrase
    return out
