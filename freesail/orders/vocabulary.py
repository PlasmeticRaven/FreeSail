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
    object: str  # sail | yards | line | heading | points | none | driver
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

    @property
    def class_bound_take_in_phrases(self) -> frozenset[str]:
        """The take-in synonyms that suit only some sails ('clew up', 'haul down')."""
        return frozenset(p for phrases in self.take_in_words.values() for p in phrases)

    @property
    def verb_names(self) -> list[str]:
        """Canonical verb names in file order (the order shown in error messages)."""
        return [v for v in self.verbs if self.verbs[v].level != "driver"]


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
    vocab.verb_phrases = sorted(phrase_to_verb, key=lambda s: (-len(s.split()), -len(s), s))
    for phrase, mods in (data.get("phrase_modifiers") or {}).items():
        k = key(phrase)
        if k not in phrase_to_verb:
            raise ValueError(f"{p}: phrase_modifiers lists '{phrase}', which is not a verb phrase.")
        vocab.phrase_modifiers[k] = dict(mods or {})
    vocab.haul_home = _tuple(data.get("haul_home"))
    for cls, phrases in (data.get("take_in_words") or {}).items():
        vocab.take_in_words[str(cls)] = _tuple(phrases)
    return vocab
