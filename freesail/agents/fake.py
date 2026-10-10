"""The scripted model (spec M4 §15): a deterministic fake that plays a script of replies
against the harness, so that every commitment to models is a test before a model is
asked.

A script is a list of items, one per call of the model (a sample's first reply, or the
reply after that sample's tool results): a `Reply`, a plain string (free text, no
calls), a `ToolCall` or a list of them (calls, no text), or a callable
`(last_data, turns) -> Reply` that reads the last data turn (a sample's dict, or
`{"tool_results": [...]}`) and composes its reply. `say`, `call` and `reply` write the
items in a line each:

    Fake([
        "Nothing to report.",                                # a note
        reply("Looking.", call("readings")),                 # a call...
        "The wind is fresh from the west.",                  # ...and the reply after its result
        call("stand_by", until="eight bells"),
        f"I have seen enough. {OPT_OUT_TOKEN} The rest is silence.",
    ])

When the script is spent the fake answers `when_done` (silence, by default) forever, or
starts over with `loop=True`. `Transcript` plays back a recorded transcript and returns
`None` when it is spent, which leaves the sample open: the replay of a saved game
(`harness.restore`) and the REPL's turn mode both rest on it. `narrator()` is the small
built-in script the drivers run for `--watcher fake`: a line at each sample from the
readings, and an answer to a question.
"""

from __future__ import annotations

import math
import re
from collections.abc import Callable, Sequence
from typing import Any

from freesail.agents.model import DATA, Reply, ToolCall, Turn

__all__ = [
    "Fake",
    "Item",
    "Transcript",
    "call",
    "captain_of_the_ship",
    "keep_the_command",
    "lookout_at_the_masthead",
    "master_of_the_reckoning",
    "narrator",
    "officer_of_the_watch",
    "passenger_aboard",
    "reply",
    "say",
    "silence",
    "work_the_slate",
]

Item = (
    Reply | str | ToolCall | Sequence[ToolCall] | Callable[[dict[str, Any], Sequence[Turn]], Reply]
)


def say(text: str) -> Reply:
    return Reply(text=text)


def call(name: str, **args: Any) -> ToolCall:
    return ToolCall(name, dict(args))


def reply(text: str = "", *calls: ToolCall) -> Reply:
    return Reply(text=text, calls=tuple(calls))


def silence() -> Reply:
    return Reply()


def _as_reply(item: Item, last_data: dict[str, Any], turns: Sequence[Turn]) -> Reply:
    if isinstance(item, Reply):
        return item
    if isinstance(item, str):
        return Reply(text=item)
    if isinstance(item, ToolCall):
        return Reply(calls=(item,))
    if callable(item):
        return item(last_data, turns)
    return Reply(calls=tuple(item))


def last_data(turns: Sequence[Turn]) -> dict[str, Any]:
    for t in reversed(turns):
        if t.role == DATA:
            return t.content
    return {}


class Fake:
    def __init__(
        self, script: Sequence[Item], *, loop: bool = False, when_done: Reply | None = None
    ):
        self.script = list(script)
        self.loop = loop
        self.when_done = Reply() if when_done is None else when_done
        self.calls = 0  # how many times the harness has called
        self.seen: list[Sequence[Turn]] = []  # the conversation at each call, for tests

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        self.seen.append(tuple(turns))
        i = self.calls
        self.calls += 1
        if not self.script:
            return self.when_done
        if i >= len(self.script):
            if not self.loop:
                return self.when_done
            i %= len(self.script)
        return _as_reply(self.script[i], last_data(turns), turns)


class Transcript:
    """A recorded transcript played back in order; `None` when it is spent."""

    def __init__(self, replies: Sequence[Reply]):
        self.replies = list(replies)
        self.calls = 0

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        if self.calls >= len(self.replies):
            return None
        r = self.replies[self.calls]
        self.calls += 1
        return r

    def extend(self, replies: Sequence[Reply]) -> None:
        self.replies.extend(replies)


def readings_so_far(turns: Sequence[Turn]) -> dict[str, Any]:
    """The readings as the conversation has them: every sample's in turn, each after the
    first holding only what changed (package 31c), the sails as the last sample that had
    them gave them (the rows, or the one line)."""
    out: dict[str, Any] = {}
    for t in turns:
        if t.role == DATA and isinstance(t.content, dict) and "readings" in t.content:
            out.update(t.content.get("readings") or {})
    return out


def narrate(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
    """The built-in watcher's line: the readings in a sentence, and an answer to a
    question. After a tool result it says nothing more."""
    if "tool_results" in last:
        return Reply()
    r = readings_so_far(turns)
    question = last.get("question")
    reason = str(last.get("reason", ""))
    parts = []
    if r.get("true_wind_speed") and r.get("true_wind_from"):
        parts.append(f"wind {r['true_wind_from']}, {r['true_wind_speed']}")
    if r.get("heading"):
        parts.append(f"heading {r['heading']}")
    if r.get("speed"):
        parts.append(f"making {r['speed']}")
    if r.get("heel"):
        parts.append(f"heeling {r['heel']}")
    strain = r.get("strain")
    if strain and not str(strain).startswith("0.0"):
        parts.append(f"the strain at {strain}")
    line = "; ".join(parts)
    text = f"{line[0].upper()}{line[1:]}." if line else ""
    if reason.startswith("a notable event") or reason.startswith("an urgent event"):
        # an event: name it and no more; the readings come at the glass
        text = f"Noted: {reason.split(': ', 1)[-1]}".strip()
    calls: tuple[ToolCall, ...] = ()
    if question:
        sails = r.get("sails") or {}
        if isinstance(sails, str):  # the sails in one line (package 31c)
            answer = f"The sails: {sails}. {text}".rstrip()
            calls = (ToolCall("answer", {"text": f"You asked {question}. {answer}".strip()}),)
            return Reply(calls=calls)
        drawing = [n for n, s in sails.items() if s in ("set", "drawing", "goose winged")]
        shaking = [n for n, s in sails.items() if s in ("shaking", "aback")]
        if sails:
            answer = f"{len(drawing)} sails drawing"
            if shaking:
                answer += f"; {', '.join(shaking)} {'is' if len(shaking) == 1 else 'are'} not"
            answer += f". {text}".rstrip()
        else:
            answer = text or "Nothing to report."
        calls = (ToolCall("answer", {"text": f"You asked {question}. {answer}".strip()}),)
        text = ""
    return Reply(text=text, calls=calls)


def narrator() -> Fake:
    return Fake([narrate], loop=True)


# The scripted officer's thresholds (package 37), from the starter book's reasons
# (`docs/primer/11-the-starting-book.md`): the royals come in over twenty knots and go
# back under fifteen, a wind a sailor would call fresh and moderate.
OFFICER_ROYALS_IN_KN = 20
OFFICER_ROYALS_OUT_KN = 15


def _knots(words: Any) -> float | None:
    try:
        return float(str(words).split()[0])
    except (ValueError, IndexError):
        return None


def keep_the_deck(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
    """The built-in officer's turn (package 37): with the deck, the royals taken in when
    the true wind is over `OFFICER_ROYALS_IN_KN` and set again under `OFFICER_ROYALS_OUT_KN`
    (one order a turn, so a repeated refusal is the ship's and not a loop); a question
    answered from the readings; a note of the deck's giving in the journal; nothing after
    a tool result but the next thing. Without the deck it watches as the narrator does."""
    if "tool_results" in last:
        return Reply()
    r = readings_so_far(turns)
    question = last.get("question")
    if question:
        text = narrate(last, turns)
        answer = text.calls[0].args["text"] if text.calls else text.text or "Nothing to report."
        return Reply(calls=(ToolCall("answer", {"text": answer}),))
    word = str(last.get("word") or "")
    if "You have the deck" in word:
        return Reply(
            text="I have the deck, sir.",
            calls=(ToolCall("journal", {"note": "Took the deck; the night orders read."}),),
        )
    officer = r.get("officer_of_the_watch")
    has_deck = isinstance(officer, dict) and officer.get("deck")
    if not has_deck and "has the deck since" not in str(officer):
        return narrate(last, turns)
    kn = _knots(r.get("true_wind_speed"))
    sails = r.get("sails")
    royals_set = None
    if isinstance(sails, dict):
        royals = [s for n, s in sails.items() if n.endswith("royal")]
        royals_set = any(s in ("set", "drawing") for s in royals) if royals else None
    elif isinstance(sails, str):
        royals_set = "royals set" in sails or ("the royals" in sails.split(";")[0])
    if kn is not None and royals_set is not None:
        if kn > OFFICER_ROYALS_IN_KN and royals_set:
            return Reply(calls=(ToolCall("submit_order", {"text": "take in the royals"}),))
        if kn < OFFICER_ROYALS_OUT_KN and not royals_set:
            return Reply(calls=(ToolCall("submit_order", {"text": "set the royals"}),))
    return narrate(last, turns)


def officer_of_the_watch() -> Fake:
    return Fake([keep_the_deck], loop=True)


# The scripted captain (package 40; spec M6 §3, truths 78 and 79): takes the station,
# notes it in the journal, gives the direct orders it was handed one a sample (in
# `orders`), answers a question from the readings, and otherwise stands by until eight
# bells, the book holding the deck meanwhile; with `then_silent` it answers nothing once
# its orders are given, so that the silent door passes the deck to the book (truth 79).


def keep_the_command(orders: Sequence[str] = (), then_silent: bool = False) -> Any:
    given: list[str] = list(orders)
    state = {"i": 0, "took": False}

    def turn(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
        if "tool_results" in last:
            return Reply()
        question = last.get("question")
        if question:
            text = narrate(last, turns)
            answer = text.calls[0].args["text"] if text.calls else text.text or "Nothing to report."
            return Reply(calls=(ToolCall("answer", {"text": answer}),))
        if not state["took"]:
            state["took"] = True
            return Reply(
                text="I have the command.",
                calls=(ToolCall("journal", {"note": "Took the command; the book read."}),),
            )
        if state["i"] < len(given):
            text = given[state["i"]]
            state["i"] += 1
            return Reply(calls=(ToolCall("submit_order", {"text": text}),))
        if then_silent:
            return Reply()
        return Reply(calls=(ToolCall("stand_by", {"until": "eight bells"}),))

    return turn


def captain_of_the_ship(orders: Sequence[str] = (), then_silent: bool = False) -> Fake:
    """The fake at the captain's station: `orders` given one a sample after it has taken
    the command, then standing by until eight bells (or silent, `then_silent`)."""
    return Fake([keep_the_command(orders, then_silent)], loop=True)


# The scripted master (package 41; spec M6 §11, truth 80's working at the master's
# station): the traverse worked from the slate's words alone, as a model reads them.
_SLATE_POINT = r"([NESW]+(?: by [NESW]+)?)"
_SLATE_FROM = re.compile(r"(\d+)° (\d+)' ([NS]), (\d+)° (\d+)' ([EW]) by account then")
_SLATE_BOARD = re.compile(r"\((\d{3})°\) (\d+\.\d) miles([^;]*)")
_SLATE_ALSO = re.compile(r"(?:the tide|her drift hove to) (\d+\.\d) miles to the " + _SLATE_POINT)
_SLATE_SIGHT = re.compile(r"moved (\d+\.\d) miles to the " + _SLATE_POINT)


def work_the_slate(words: str, with_the_tide: bool = True) -> tuple[float, float]:
    """The traverse worked from the slate's words alone: where it begins, each board's
    course and distance and the tide and drift with it, each sight's move; (lat, lon)."""
    from freesail import units

    m = _SLATE_FROM.search(words)
    assert m, words
    lat = (int(m.group(1)) + int(m.group(2)) / 60.0) * (1 if m.group(3) == "N" else -1)
    lon = (int(m.group(4)) + int(m.group(5)) / 60.0) * (1 if m.group(6) == "E" else -1)
    boards = words.split("and its distance: ", 1)[1].split(". ", 1)[0]
    de = dn = 0.0
    for course, miles, rest in _SLATE_BOARD.findall(boards):
        c = math.radians(float(course))
        de += float(miles) * math.sin(c)
        dn += float(miles) * math.cos(c)
        for also in _SLATE_ALSO.finditer(rest):
            if with_the_tide or not also.group(0).startswith("the tide"):
                a = units.parse_compass_point(also.group(2))
                de += float(also.group(1)) * math.sin(a)
                dn += float(also.group(1)) * math.cos(a)
    for miles, point in _SLATE_SIGHT.findall(words):
        a = units.parse_compass_point(point)
        de += float(miles) * math.sin(a)
        dn += float(miles) * math.cos(a)
    lat += dn / 60.0
    lon += de / (60.0 * math.cos(math.radians(lat)))
    return lat, lon


def _position_words(lat: float, lon: float) -> str:
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{abs(lat):.4f} {ns} {abs(lon):.4f} {ew}"


def keep_the_reckoning(with_the_tide: bool = True, answer_in_time: bool = True) -> Any:
    """The built-in master's turn (package 41): when a sample's notice hands him the
    slate for a working, he works it by the traverse and gives his figure for the
    working's moment ('my reckoning is ...'), which the ship's account takes; with
    `answer_in_time` false he stands by instead and the ship's master's figure stands
    (G19's third step, the other way). A question is answered from the readings; off a
    working he notes the glass and stands by until noon or a fix."""
    state = {"took": False}

    def turn(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
        if "tool_results" in last:
            return Reply()
        question = last.get("question")
        if question:
            text = narrate(last, turns)
            answer = text.calls[0].args["text"] if text.calls else text.text or "Nothing to report."
            return Reply(calls=(ToolCall("answer", {"text": answer}),))
        if not state["took"]:
            state["took"] = True
            return Reply(
                text="I have the reckoning, sir.",
                calls=(
                    ToolCall("journal", {"note": "Took the master's station; the slate read."}),
                ),
            )
        notice = next(
            (n for n in last.get("notices") or [] if "The reckoning is to be worked" in str(n)),
            None,
        )
        if notice is not None:
            if not answer_in_time:
                return Reply(
                    text="I shall want longer than that.",
                    calls=(ToolCall("stand_by", {"until": "noon, or a fix, or eight bells"}),),
                )
            lat, lon = work_the_slate(str(notice), with_the_tide)
            return Reply(
                calls=(
                    ToolCall(
                        "submit_order", {"text": f"my reckoning is {_position_words(lat, lon)}"}
                    ),
                )
            )
        return Reply(calls=(ToolCall("stand_by", {"until": "noon, or a fix, or eight bells"}),))

    return turn


def master_of_the_reckoning(with_the_tide: bool = True, answer_in_time: bool = True) -> Fake:
    """The fake at the master's station: the slate worked by the traverse as truth 80's
    fake officer works it, the figure given within the working's time (or not,
    `answer_in_time`)."""
    return Fake([keep_the_reckoning(with_the_tide, answer_in_time)], loop=True)


def keep_a_lookout(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
    """The built-in lookout's turn (package 41): a hail for each sighting, each sail
    made out and each sail lost in the sample's log, in a lookout's words; a question
    answered; nothing when nothing is seen; then standing by for the masthead's events
    or the glass."""
    if "tool_results" in last:
        return Reply()
    question = last.get("question")
    if question:
        r = readings_so_far(turns)
        seen = r.get("in_sight") or r.get("lookout") or "nothing in sight"
        return Reply(calls=(ToolCall("answer", {"text": f"From the masthead: {seen}."}),))
    hails = []
    for line in last.get("log") or []:
        kind = str(line.get("kind") or "")
        if kind == "lookout.sighting":
            hails.append(
                f"Sail ho! {line['text']}"
                if "sail" in str(line["text"]).lower()
                else f"Land ho! {line['text']}"
            )
        elif kind in (
            "lookout.made_out",
            "lookout.sail_lost",
            "lookout.land_ahead",
            "lookout.closing",
        ):
            hails.append(f"Deck there! {line['text']}")
    if hails:
        return Reply(
            calls=tuple(ToolCall("submit_order", {"text": f"hail {h}"}) for h in hails[:3])
        )
    return Reply(
        calls=(ToolCall("stand_by", {"until": "a sighting, or a sail lost, or eight bells"}),)
    )


def lookout_at_the_masthead() -> Fake:
    """The fake at the lookout's station: a hail for what the masthead sees, nothing
    else."""
    return Fake([keep_a_lookout], loop=True)


def passenger_aboard(remarks: Sequence[str] = ()) -> Fake:
    """The fake at a passenger's station (package 41): says each remark on the
    quarterdeck one a sample, answers a question, and otherwise stands by until eight
    bells."""
    given = list(remarks)
    state = {"i": 0}

    def turn(last: dict[str, Any], turns: Sequence[Turn]) -> Reply:
        if "tool_results" in last:
            return Reply()
        if last.get("question"):
            return Reply(calls=(ToolCall("answer", {"text": "A passenger knows nothing of it."}),))
        if state["i"] < len(given):
            text = given[state["i"]]
            state["i"] += 1
            return Reply(calls=(ToolCall("submit_order", {"text": f"say {text}"}),))
        return Reply(calls=(ToolCall("stand_by", {"until": "eight bells"}),))

    return Fake([turn], loop=True)
