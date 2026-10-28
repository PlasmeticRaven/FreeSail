"""The supply's orders (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §3.2): powder and shot taken in at a port.

    take in powder and shot         the magazine completed: of the Ordnance's storekeeper,
                                    free and vouched, for a King's ship of the port's
                                    nation; of the merchants at a price for the rest
    take in powder | take in shot   the one or the other
    buy powder of necessity         a King's ship of the merchants, on the captain's word
    take in two barrels of powder   so many barrels
    take in 30 cartridges for the carronades
                                    powder for so many, at their charge, in whole barrels
    take in 100 round shot for the 12-pounders
    take in two tons of shot for the long 18s

The verb is the vocabulary's `take in powder and shot` with its synonyms; `buy ...` and
`demand ...` whose words name powder, shot, ball, cartridges or ammunition come here from
`orders.port` before the yard and the market (no market trades powder), and 'take in
forty barrels of powder' from `orders._stores_order`. The words are read in the build
design's order: "of necessity" struck out as a flag; the guns named ("for the
12-pounders", "for the long 12", "for the carronades", "for the pivot gun", "for the long
Tom", "for the swivels", "of 12 pounds") stripped before the number is read; then the
quantities. With no number the order completes to what the magazine wants
(`Magazine.wanting`), and any number is cut to it, with words. The World's side, the
refusals in their order and the hoy, is `world.ordnance`'s.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders import numbers
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of
from freesail.world import ordnance as supply

__all__ = ["TAKE_IN", "check", "execute", "names_powder", "read"]

TAKE_IN = "take in powder and shot"

Result = tuple[str, str, dict[str, Any]]

# The words that make a `buy` or a `demand` the supply's: whole words only.
_POWDER_WORDS = re.compile(r"\b(?:powder|shot|ball|balls|cartridge|cartridges|ammunition)\b")
# "of necessity", "of absolute necessity": the captain's word for a purchase (the
# Regulations of 1806, the Captain, Art. VII, l.6220-6252)
_NECESSITY = re.compile(r"\b(?:out\s+)?of\s+(?:an?\s+)?(?:absolute\s+)?necessity\b")
# who supplies it, said or not: the words carry no quantity
_FROM = re.compile(
    r"\b(?:from|of)\s+(?:the\s+)?(?:ordnance's\s+storekeeper|ordnance|storekeeper|"
    r"merchants?|yard|chandlers|town)\b"
)
_SAYS_POWDER = re.compile(r"\b(?:powder|cartridges?|barrels?)\b")
_SAYS_SHOT = re.compile(r"\b(?:shot|balls?|round|grape|chain|tons?)\b")
_ARTICLES = frozenset({"the", "her", "his", "our", "all", "of", "and"})
# The words of the guns as a whole, which name no kind or calibre.
_ALL_GUNS = frozenset({"great", "guns", "gun", "battery", "broadside", "cannon"})


def names_powder(words: str | None) -> bool:
    """Whether the words name powder, shot, ball, cartridges or ammunition (whole words)."""
    return bool(_POWDER_WORDS.search(str(words or "").lower()))


def _norm(text: str) -> str:
    return " ".join(str(text or "").lower().replace("-", " ").replace("’", "'").split())


def execute(ship: Any, order: Order) -> Result:
    """Carry out the supply's order: the words read, the World's refusals and the hoy."""
    from freesail.orders.port import NO_PORTS_WORDS

    if not getattr(ship, "guns", None):
        raise OrderError(supply.NO_GUNS_WORDS)
    world = world_of(ship)
    ports = getattr(world, "ports", None) if world is not None else None
    if ports is None or not ports.ports:
        raise OrderError(NO_PORTS_WORDS)
    ask = read(ship, order)
    text, data = supply.take_in(world, ask)
    return "ordnance.demanded", text, {"verb": order.verb, "level": 1} | data


def check(ship: Any, order: Order) -> None:
    """Read the order's words whole without carrying it out (a standing order's action,
    `orders.read_whole`): its quantities and its guns; whether she is in port, what the
    magazine wants and the purse are the order's own business when it fires."""
    ask = read(ship, order)
    if ask.error:
        raise OrderError(ask.error)


def read(ship: Any, order: Order) -> supply.Ask:
    """The order's words as the World's side takes them (`world.ordnance.Ask`)."""
    phrase = _norm(order.verb_phrase or "")
    rest = _norm(order.object or "")
    article = phrase.rsplit(" ", 1)[-1] if " " in phrase else ""
    if article in ("a", "an"):
        # the vocabulary's 'demand a' and 'demand an' (data/vocabulary.yaml, the port's
        # `demand`) take the article into the verb's words: it is the quantity's, and 'demand
        # a barrel of powder' is one barrel, not the whole of what the magazine wants
        rest = f"{article} {rest}".strip()
    necessity = bool(_NECESSITY.search(rest))
    rest = _norm(_FROM.sub(" ", _NECESSITY.sub(" ", rest)))
    whole = f"{phrase} {rest}"
    powder = bool(_SAYS_POWDER.search(whole))
    shot = bool(_SAYS_SHOT.search(whole))
    if not powder and not shot:
        powder = shot = True  # 'complete the magazine', 'take in ammunition'
    parts: list[supply.Part] = []
    keys: list[tuple[str, float]] = []
    error = ""
    for chunk in _chunks(rest):
        part, named, why = _read_chunk(ship, chunk)
        if why and not error:
            error = why
        if part is not None:
            parts.append(part)
        else:
            keys.extend(k for k in named if k not in keys)
    return supply.Ask(
        powder=powder,
        shot=shot,
        necessity=necessity,
        parts=tuple(parts),
        keys=tuple(keys),
        error=error,
    )


# The words a quantity counts by (`_unit`): a fraction said after 'and' with one of these
# after it begins a quantity of its own ('and half a ton of shot'); with none, it is the
# last quantity's ('two barrels and a half of powder').
_UNIT_WORDS = frozenset(
    {"barrel", "barrels", "cartridge", "cartridges", "ton", "tons"}
    | {"round", "grape", "chain", "shot", "ball", "balls"}
)


def _chunks(rest: str) -> list[str]:
    """The words as one quantity or several ('2 barrels of powder and 100 round shot for
    the 12-pounders': two), split at each 'and' that a number follows. A number is read
    whole first (`numbers.read`), so that the 'and' inside 'a hundred and fifty' or 'two
    and a half' splits nothing; and an 'and' before a half or a quarter said after its unit
    ('two barrels and a half of powder', 'two tons and a half of shot') is the quantity's
    own."""
    words = rest.split()
    parts: list[list[str]] = [[]]
    k = 0
    while k < len(words):
        w = words[k]
        if w == "and" and parts[-1]:
            got = numbers.read(words, k + 1)
            if got is not None and not _a_fraction_of_the_last(words, k + 1, got):
                parts.append([])
                k += 1
                continue
        got = numbers.read(words, k) if w != "and" else None
        used = got[1] if got is not None else 1
        parts[-1].extend(words[k : k + used])
        k += used
    return [" ".join(p) for p in parts if p]


def _a_fraction_of_the_last(words: list[str], i: int, got: tuple[float, int]) -> bool:
    """Whether the number at words[i], said after an 'and', is a half or a quarter of the
    quantity before it: under one, and no unit after it ('and a half of powder'; not 'and
    half a ton of shot')."""
    value, used = got
    after = words[i + used] if i + used < len(words) else ""
    return value < 1.0 and after not in _UNIT_WORDS


# a calibre said with its weight: 'of 12 pounds', 'of half a pound'
_OF_POUNDS = re.compile(r"\bof\s+(?:a\s+)?(?P<n>[a-z0-9.]+(?:\s+a)?)\s+pounds?\b")
# a calibre said as the guns' own: '12 pounder', '12 pounders', 'half pounder'
_POUNDER = re.compile(r"\b(?P<n>\d+(?:\.\d+)?|[a-z]+)\s+pounders?\b")


def _read_chunk(
    ship: Any, chunk: str
) -> tuple[supply.Part | None, tuple[tuple[str, float], ...], str]:
    """One quantity's words: the part (None with no number), the guns named, and the
    words' refusal ("" when they read)."""
    words = chunk.split()
    while words and words[0] in ("and", "some", "more"):
        words = words[1:]
    text = " ".join(words)
    named: tuple[tuple[str, float], ...] = ()
    why = ""
    guns_words = ""
    m = re.search(r"\bfor\s+(?P<guns>.+)$", text)
    if m:
        guns_words = m.group("guns")
        text = text[: m.start()].strip()
    calibre: float | None = None
    m = _OF_POUNDS.search(text)
    if m:
        got = numbers.read_all(m.group("n"))
        if got is not None:
            calibre = float(got)
            text = (text[: m.start()] + " " + text[m.end() :]).strip()
    m = _POUNDER.search(text)
    if m and calibre is None:
        got = numbers.read_all(m.group("n"))
        if got is not None:
            calibre = float(got)
            text = (text[: m.start()] + " " + text[m.end() :]).strip()
    if guns_words or calibre is not None:
        named, why = _guns_named(ship, guns_words, calibre)
    n, left = numbers.number_in(text)
    if n is None:
        return None, named, why
    unit = [w for w in left.split() if w not in _ARTICLES]
    what = _unit(unit)
    if what is None and _bare_article(text) and (not unit or unit[0] not in _UNIT_WORDS):
        # 'a' or 'an' before no unit is no number ('demand a supply of powder', the article
        # given back to the words by `read`): the words are read as if it were not said
        n, left = numbers.number_in(text, skip_a=True)
        if n is None:
            return None, named, why
        unit = [w for w in left.split() if w not in _ARTICLES]
        what = _unit(unit)
    if what is not None:
        # a half or a quarter said after the unit: 'two barrels and a half of powder', 'two
        # tons and a half of shot' (`numbers.read` leaves it to the caller, the unit coming
        # between)
        n += _fraction_after_unit(left.split())
    if what is None:
        return (
            None,
            named,
            why
            or (
                f"'{chunk}' is not a quantity of powder or shot: say 'take in two barrels of "
                f"powder', 'take in 100 round shot for the {_example(ship)}' or 'take in 20 "
                f"cartridges for the {_cartridges_example(ship)}'."
            ),
        )
    if n <= 0:
        return None, named, why or f"'{chunk}' asks for nothing: say how many."
    kind = "round"
    if what in ("grape", "chain", "round"):
        kind, what = what, "shot"
    if what == "barrels":
        return supply.Part("barrels", float(n)), named, why
    if why:
        return None, named, why
    keys = named or _all_keys(ship)
    if what == "cartridges":
        if len(keys) != 1:
            return None, named, _which(ship, "Cartridges", "20 cartridges", _cartridges_example)
        return supply.Part("cartridges", float(n), keys), named, ""
    calibres = sorted({p for _k, p in keys}, key=lambda p: -p)
    if len(calibres) != 1:
        return None, named, _which(ship, "Shot", "100 round shot", _example)
    key = next(k for k in keys if k[1] == calibres[0])
    return supply.Part(what, float(n), (key,), kind), named, ""


def _bare_article(text: str) -> bool:
    """Whether the first number in the words is a bare 'a' or 'an' (one), not 'a hundred'
    or 'a half'."""
    words = text.split()
    for i in range(len(words)):
        got = numbers.read(words, i)
        if got is not None:
            return got[1] == 1 and words[i] in ("a", "an")
    return False


def _fraction_after_unit(words: list[str]) -> float:
    """The half or quarter said after a quantity's unit: 'barrels and a half of powder',
    'tons and three quarters'; nought when none is said. `words` begin at the unit, the
    articles before it allowed."""
    j = 0
    while j < len(words) and words[j] in _ARTICLES and words[j] != "and":
        j += 1
    j += 1  # the unit
    if words[j : j + 1] != ["and"]:
        return 0.0
    got = numbers.read(words, j + 1)
    if got is None or got[0] >= 1.0:
        return 0.0
    return got[0]


def _unit(words: list[str]) -> str | None:
    """What the number counts: 'barrels', 'cartridges', 'tons' (of shot), or the shot's
    kind ('round', 'grape', 'chain'; 'shot' or 'ball' alone are round)."""
    if not words:
        return None
    first = words[0]
    if first in ("barrel", "barrels"):
        return "barrels"
    if first in ("cartridge", "cartridges"):
        return "cartridges"
    if first in ("ton", "tons"):
        if "powder" in words and not any(w in ("shot", "ball", "balls") for w in words):
            return None  # powder by the ton is no quantity the storekeeper issues
        return "tons"
    if first in ("round", "grape", "chain"):
        return first
    if first in ("shot", "ball", "balls"):
        return "round"
    return None


def _all_keys(ship: Any) -> tuple[tuple[str, float], ...]:
    out: list[tuple[str, float]] = []
    for g in getattr(ship, "guns", {}).values():
        key = (str(g.kind), float(g.pounder))
        if key not in out:
            out.append(key)
    return tuple(out)


def _guns_named(
    ship: Any, words: str, calibre: float | None
) -> tuple[tuple[tuple[str, float], ...], str]:
    """The guns the words name, by kind and calibre in her own order, and the refusal
    when she has none such ("" when she has)."""
    guns = list(getattr(ship, "guns", {}).values())
    if not guns:
        return (), ""  # no guns at all: the order's first refusal says so
    tokens = [w for w in words.split() if w not in _ARTICLES and w not in ("a", "an")]
    # '12s', 'long 18s': the calibre's plural
    tokens = [re.sub(r"^(\d+(?:\.\d+)?)s$", r"\1", w) for w in tokens]
    kind: str | None = None
    pivot = False
    if "tom" in tokens or "pivot" in tokens:
        pivot = True
    elif any(w.startswith("carronade") for w in tokens):
        kind = "carronade"
    elif any(w.startswith("swivel") for w in tokens):
        kind = "swivel"
    elif "long" in tokens:
        kind = "long"
    rest = [
        w
        for w in tokens
        if w not in ("long", "tom", "pivot", "pounder", "pounders")
        and not w.startswith(("carronade", "swivel"))
    ]
    if calibre is None and rest:
        got = numbers.read(rest, 0)
        if got is not None:
            calibre = float(got[0])
            rest = rest[got[1] :]
    if rest and not set(rest) <= _ALL_GUNS:
        return (), (
            f"'for {words}' names none of her guns: she carries {_guns_words(ship)}; say "
            f"'take in 100 round shot for the {_example(ship)}'."
        )
    if pivot:
        sel = [g for g in guns if g.place == "pivot"]
        if not sel:
            return (), f"She carries no pivot gun; her guns are {_guns_words(ship)}."
    else:
        sel = [
            g
            for g in guns
            if (kind is None or g.kind == kind) and (calibre is None or float(g.pounder) == calibre)
        ]
    if calibre is not None:
        sel = [g for g in sel if float(g.pounder) == calibre]
    if not sel:
        if calibre is not None and not any(float(g.pounder) == calibre for g in guns):
            return (), (
                f"She carries no {_calibre_words(calibre)}-pounders; her calibres are "
                f"{_and([_calibre_figure(p) for p in _calibres(ship)])}."
            )
        what = {"long": "long guns", "carronade": "carronades", "swivel": "swivels"}
        named = (
            f"{kind_words(kind, calibre)}s"
            if kind is not None and calibre is not None
            else what.get(kind or "", "such guns")
        )
        return (), f"She carries no {named}; her guns are {_guns_words(ship)}."
    out: list[tuple[str, float]] = []
    for g in sel:
        key = (str(g.kind), float(g.pounder))
        if key not in out:
            out.append(key)
    return tuple(out), ""


def kind_words(kind: str, pounder: float) -> str:
    """'long 12-pounder', '12-pounder carronade', 'half-pounder swivel'."""
    calibre = _calibre_words(pounder)
    if kind == "long":
        return f"long {calibre}-pounder"
    return f"{calibre}-pounder {kind}"


def _calibre_words(pounder: float) -> str:
    return "half" if float(pounder) == 0.5 else f"{float(pounder):g}"


def _calibre_figure(pounder: float) -> str:
    return "the half-pounder" if float(pounder) == 0.5 else f"{float(pounder):g}"


def _calibres(ship: Any) -> list[float]:
    out: list[float] = []
    for g in getattr(ship, "guns", {}).values():
        if float(g.pounder) not in out:
            out.append(float(g.pounder))
    return out


def _guns_words(ship: Any) -> str:
    """Her guns by kind and calibre: 'a long 12-pounder, 12-pounder carronades and
    half-pounder swivels'."""
    counts: dict[tuple[str, float], int] = {}
    for g in getattr(ship, "guns", {}).values():
        key = (str(g.kind), float(g.pounder))
        counts[key] = counts.get(key, 0) + 1
    return _and(
        [
            f"a {kind_words(k, p)}" if n == 1 else f"{kind_words(k, p)}s"
            for (k, p), n in counts.items()
        ]
    )


def _example(ship: Any) -> str:
    calibres = _calibres(ship)
    return f"{_calibre_words(calibres[0])}-pounders" if calibres else "guns"


def _cartridges_example(ship: Any) -> str:
    """Her first guns by kind and calibre, as a cartridge's charge is theirs: 'long
    18-pounders', '12-pounder carronades', 'long 12-pounder' for the one gun (the review's
    finding: the privateer's pivot gun was 'the long 12-pounders' in the example)."""
    keys = _all_keys(ship)
    if not keys:
        return "guns"
    kind, pounder = keys[0]
    n = sum(
        1
        for g in getattr(ship, "guns", {}).values()
        if str(g.kind) == kind and float(g.pounder) == pounder
    )
    return kind_words(kind, pounder) + ("" if n == 1 else "s")


def _which(ship: Any, what: str, example: str, guns: Any) -> str:
    return (
        f"{what} for which guns? She carries {_guns_words(ship)}: say 'take in {example} for "
        f"the {guns(ship)}'."
    )


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
