"""One reader for numbers, in figures or in words (package 37l; the review of gate 5c's
playtests, G17: five readers had five word lists between them, none read thirteen,
fourteen or seventeen to nineteen, `veer five fathoms` was refused while the log wrote "a
hundred and eighty-five fathoms", and `take in provisions for sixteen days` silently took
thirty).

Every order that takes a number reads it here: the grammar's counts (points, reefs,
fathoms of a line, the standing dialect's knots and minutes), the ground tackle's
fathoms, the port's tons, days and hands, the master's knots of set, the canvas's number.

    16, 16.5                        figures
    one ... nineteen                the units and the teens
    twenty ... ninety               the tens, and "twenty five" or "twenty-five" (the
                                    grammar's normalising has made the hyphen a space)
    a hundred, two hundred and five, a hundred and eighty-five, one hundred eighty five
    a thousand, two thousand three hundred
    a, an                           one ("a fathom", "an hour"); "a hundred" is a hundred
    half, half a, a half            a half ("half a fathom", "a point and a half")
    quarter, a quarter, a quarter of a, three quarters
    <n> and a half, <n> and a quarter, <n> and three quarters

`read(words, i)` reads one number at `words[i]` and says how many words it took; it
takes the longest number there ("a hundred and eighty-five", not "a"). `number_in(text)`
finds the first number in a run of words and hands back the words without it.
`WORDS` is every word a number may be made of, for the grammar's sets of modifier
words. Nothing here draws randomness or reads the ship.
"""

from __future__ import annotations

import re

__all__ = ["WORDS", "number_in", "read", "read_all"]

UNITS: dict[str, int] = {
    "zero": 0,
    "nought": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}
TENS: dict[str, int] = {
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fourty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
}
SCALES: dict[str, int] = {"hundred": 100, "thousand": 1000}
# "a score" and "a dozen" are numbers a seaman says of men and of days
OTHERS: dict[str, int] = {"dozen": 12, "score": 20}
FRACTIONS: dict[str, float] = {"half": 0.5, "quarter": 0.25, "quarters": 0.25}

WORDS: frozenset[str] = frozenset(
    {*UNITS, *TENS, *SCALES, *OTHERS, *FRACTIONS, "a", "an", "and", "of"}
)

_FIGURES = re.compile(r"^\d+(?:\.\d+)?$")


def _figure(word: str) -> float | None:
    return float(word) if _FIGURES.match(word) else None


def _fraction(words: list[str], i: int) -> tuple[float, int] | None:
    """A fraction alone at words[i]: 'half', 'half a', 'a half', 'quarter', 'a quarter',
    'a quarter of a', 'three quarters', 'three quarters of a'."""
    n = len(words)
    w = words[i] if i < n else ""
    j = i
    value: float | None = None
    if w in ("a", "an", "one") and i + 1 < n and words[i + 1] in ("half", "quarter"):
        value, j = FRACTIONS[words[i + 1]], i + 2
    elif w in ("half", "quarter"):
        value, j = FRACTIONS[w], i + 1
    elif w in ("three", "3") and i + 1 < n and words[i + 1] in ("quarters", "quarter"):
        value, j = 0.75, i + 2
    if value is None:
        return None
    # "half a fathom", "a quarter of a fathom", "three quarters of a mile"
    if words[j : j + 2] in (["of", "a"], ["of", "an"]):
        j += 2
    elif words[j : j + 1] in (["a"], ["an"]) and words[i] in ("half", "quarter"):
        j += 1
    return value, j - i


def _whole(words: list[str], i: int) -> tuple[int, int] | None:
    """A whole number in words at words[i] (not figures): 'sixteen', 'twenty five', 'a
    hundred and eighty five', 'two thousand three hundred', 'a dozen'; (value, words
    used), or None."""
    n = len(words)
    total = current = 0
    j = i
    last: str | None = None  # the kind of the last word read: unit, teen, ten, hundred...
    while j < n:
        w = words[j]
        nxt = words[j + 1] if j + 1 < n else ""
        if w in ("a", "an") and last is None and (nxt in SCALES or nxt in OTHERS):
            current, last, j = 1, "unit", j + 1  # "a hundred", "a thousand", "a dozen"
            continue
        if w == "and" and last in ("hundred", "thousand") and (nxt in UNITS or nxt in TENS):
            j += 1  # "a hundred and eighty-five"
            continue
        if w in UNITS:
            v = UNITS[w]
            if last in (None, "hundred", "thousand") or (last == "ten" and v < 10):
                current += v
                last = "teen" if v >= 10 else "unit"
                j += 1
                continue
            break
        if w in TENS:
            if last in (None, "hundred", "thousand"):
                current += TENS[w]
                last, j = "ten", j + 1
                continue
            break
        if w == "hundred":
            if last in ("unit", "teen") and current < 100:
                current *= 100
                last, j = "hundred", j + 1
                continue
            break
        if w == "thousand":
            if last not in (None, "thousand"):
                total += current * 1000
                current, last, j = 0, "thousand", j + 1
                continue
            break
        if w in OTHERS:
            if last is None:
                current, last, j = OTHERS[w], "other", j + 1
            elif last == "unit" and current < 10:
                current, last, j = current * OTHERS[w], "other", j + 1  # "two dozen"
        break
    if last is None:
        return None
    return total + current, j - i


def read(words: list[str], i: int = 0) -> tuple[float, int] | None:
    """The number at words[i], in figures or in words, with its halves and quarters:
    (its value, how many words it took), or None when there is none there. "a" or "an"
    alone is one, as in "a fathom" and "an hour"."""
    if i >= len(words):
        return None
    w = words[i]
    frac = _fraction(words, i)
    if frac is not None:
        return frac
    figure = _figure(w)
    if figure is not None:
        value, used = figure, 1
    else:
        whole = _whole(words, i)
        if whole is not None:
            value, used = float(whole[0]), whole[1]
        elif w in ("a", "an"):
            value, used = 1.0, 1
        else:
            return None
    # "two and a half", "a point and a half" is the caller's (the unit comes between)
    j = i + used
    if words[j : j + 3] in (["and", "a", "half"], ["and", "an", "half"]):
        return value + 0.5, used + 3
    if words[j : j + 3] == ["and", "a", "quarter"]:
        return value + 0.25, used + 3
    if words[j : j + 3] in (["and", "three", "quarters"], ["and", "three", "quarter"]):
        return value + 0.75, used + 3
    if words[j : j + 2] == ["and", "half"]:
        return value + 0.5, used + 2
    return value, used


def read_all(text: str | list[str]) -> float | None:
    """The words whole as one number ('sixteen', 'a hundred and eighty five', '1.5',
    'half a'), or None when they are not one number and nothing more."""
    words = text.split() if isinstance(text, str) else list(text)
    words = [w for w in words if w]
    if not words:
        return None
    got = read(words, 0)
    if got is None or got[1] != len(words):
        return None
    return got[0]


def number_in(text: str, skip_a: bool = False) -> tuple[float | None, str]:
    """The first number in the words (in figures or in words), and the words without it;
    (None, the words) when there is none. With `skip_a`, a bare 'a' or 'an' is not taken
    for one ('a month' is no number of days)."""
    words = " ".join(text.lower().replace("-", " ").split()).split()
    for i in range(len(words)):
        got = read(words, i)
        if got is None:
            continue
        if skip_a and got[1] == 1 and words[i] in ("a", "an"):
            continue
        value, used = got
        rest = words[:i] + words[i + used :]
        return value, " ".join(rest)
    return None, " ".join(words)
