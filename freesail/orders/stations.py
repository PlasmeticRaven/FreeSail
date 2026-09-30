"""The station sentences (spec M4 §11, §12): what the captain says to an agent's station.

    ask the watcher how the sails are drawing     an order, journaled: the watcher answers
    tell the watcher we make for Falmouth         an order, journaled: no answer is owed
                                                  (`say to the watcher ...` the same)
    stand down the watcher                        an order, journaled: released with a save
    resume the watcher                            an order, journaled: the answer to a pause
    show the watcher's journal                    a query, like `state`: never journaled

`orders.handle` hands a sentence that names a station to `handle` here before the
imperative parser sees it, as it hands the standing dialect to its grammar. The agents
are reached through `ship.extra["agents"]` (the World's `agents`, by station name) and
the journals through `ship.extra["agent_journals"]`, which outlive their agents. A
sentence to a station nobody mans is refused in words.

**In a standing order** (package 31c; the owner's finding at gate 5a, `standing order
"sea": when the sea is heavy then tell the watcher the sea is getting up`): `tell` and
`ask` may follow `then`. The standing grammar resolves each at give time
(`for_standing`) to a station aboard, or refuses it in words ("there is no lookout aboard
yet"); at a firing it is delivered as the captain's own word or question would be, and
the log names the standing order as the speaker: "By standing order 'sea': the captain to
the watcher: the sea is getting up". The runtime says which order is firing
(`standing.runtime.Runtime.firing`).
"""

from __future__ import annotations

import re
from typing import Any

from freesail.agents.agent import STATION_NAMES, STATIONS_ABOARD
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import normalise

__all__ = ["STANDING_STATION_VERBS", "STATION_VERBS", "for_standing", "handle", "recognises"]

# The canonical verbs, as `data/vocabulary.yaml` lists them with `object: station`.
STATION_VERBS: tuple[str, ...] = ("ask", "tell", "stand down", "resume", "show the journal of")

# The station verbs a standing order may give (package 31c): a word and a question. The
# rest are the captain's own acts on a station, never a routine's.
STANDING_STATION_VERBS: tuple[str, ...] = ("ask", "tell")

# A sentence addressed to someone by a station verb, whoever is named: the head noun after
# the article, for the refusal of a station the ship has not got
_ADDRESSED = re.compile(r"^(?:ask|tell|say to) (?:the |a |an )?(?P<who>[\w'-]+)")

_ASK = re.compile(r"^ask (?:the )?(?P<who>.+?)(?:(?:\s*[,:]\s*|\s+)(?P<q>.+))?$")
# `tell the watcher ...` and `say to the watcher ...` (package 29): words with no answer owed
_TELL = re.compile(r"^(?:tell|say to) (?:the )?(?P<who>.+?)(?:(?:\s*[,:]\s*|\s+)(?P<q>.+))?$")
_STAND_DOWN = re.compile(
    r"^(?:stand down (?:the )?(?P<who>.+?)|stand (?:the )?(?P<who2>.+?) down)\s*$"
)
_RESUME = re.compile(r"^(?:resume|continue) (?:the )?(?P<who>.+?)\s*$")
_JOURNAL = re.compile(
    r"^(?:show (?:me )?)?(?:the )?(?P<who>.+?)(?:'s| s)? journal\s*$"
    r"|^show (?:the )?journal of (?:the )?(?P<who2>.+?)\s*$"
)


def _known(ship: Any) -> tuple[str, ...]:
    extra = getattr(ship, "extra", None) or {}
    names = list(STATION_NAMES)
    for name in list(extra.get("agents") or {}) + list(extra.get("agent_journals") or {}):
        if name not in names:
            names.append(name)
    return tuple(sorted(names, key=lambda n: -len(n)))


def _station_in(who: str, ship: Any) -> str | None:
    who = " ".join(who.split())
    for name in _known(ship):
        if who == name or who.startswith(name + " "):
            return name
    return None


def recognises(text: str, ship: Any = None) -> str | None:
    """The station verb the text is, or None. The station's name must be one the game
    knows ("ask the watcher"), so an `ask` to nobody in particular is left to the
    imperative parser's refusal."""
    norm = normalise(text).replace(" , ", " ")
    for verb, pattern in (
        ("show the journal of", _JOURNAL),
        ("stand down", _STAND_DOWN),
        ("resume", _RESUME),
        ("ask", _ASK),
        ("tell", _TELL),
    ):
        m = pattern.match(norm)
        if m is None:
            continue
        who = m.group("who") or m.groupdict().get("who2") or ""
        if verb in ("ask", "tell"):
            # "ask the watcher how ..." : the station is the head of `who` + `q`
            whole = f"{who} {m.group('q') or ''}"
            if _station_in(whole, ship) is not None:
                return verb
            continue
        if _station_in(who, ship) is not None:
            return verb
    return None


def _split_ask(text: str, ship: Any, verb: str = "ask") -> tuple[str, str]:
    norm = " ".join(text.split())
    head = r"(?:tell|say\s+to)" if verb == "tell" else "ask"
    m = re.match(rf"^{head}\s+(?:the\s+)?(?P<rest>.+)$", norm, re.I)
    rest = m.group("rest") if m else norm
    station = _station_in(normalise(rest), ship)
    if station is None:
        if verb == "tell":
            raise OrderError("Tell whom? Say 'tell the watcher <words>'.")
        raise OrderError("Ask whom? Say 'ask the watcher <question>'.")
    # the question is what follows the station's name in the text as said
    n = len(station.split())
    words = rest.split()
    question = " ".join(words[n:]).lstrip(",:").strip()
    return station, question


def _aboard(ship: Any) -> tuple[str, ...]:
    """The stations a standing order may address: those the game can man now, and any
    this game has manned."""
    extra = getattr(ship, "extra", None) or {}
    names = list(STATIONS_ABOARD)
    for name in list(extra.get("agents") or {}) + list(extra.get("agent_journals") or {}):
        if name not in names:
            names.append(name)
    return tuple(names)


def _not_aboard(who: str, ship: Any) -> str:
    aboard = " or the ".join(_aboard(ship))
    if who == "captain":
        return f"a standing order speaks for the captain; it may tell or ask the {aboard}."
    return f"there is no {who} aboard yet; a standing order may tell or ask the {aboard}."


def for_standing(ship: Any, text: str) -> tuple[str, str, str] | None:
    """A station sentence after 'then' in a standing order (package 31c), resolved when the
    order is given: (the verb, the station, the words or the question) for `tell` or
    `ask` to a station aboard, whether or not it is manned at that moment (a book read
    before the watcher takes the station; a firing to a station nobody mans is refused in
    words when it fires, as the captain's own would be). None when the text addresses no
    station (an order of the ship). OrderError in words for a station not aboard, a
    station verb a standing order does not give, or nothing to say."""
    norm = normalise(text).replace(" , ", " ")
    verb = recognises(text, ship)
    if verb is None:
        m = _ADDRESSED.match(norm)
        if m is None:
            return None
        raise OrderError(_not_aboard(m.group("who"), ship))
    if verb not in STANDING_STATION_VERBS:
        raise OrderError(
            f"'{norm}' is the captain's own to say to a station, not a standing order's; a "
            "standing order may tell or ask one."
        )
    station, words = _split_ask(text, ship, verb=verb)
    if station not in _aboard(ship):
        raise OrderError(_not_aboard(station, ship))
    if not words:
        what = "the words" if verb == "tell" else "the question"
        raise OrderError(f"{verb.capitalize()} the {station} what? Say {what} after the name.")
    return verb, station, words


def _speaker(ship: Any) -> tuple[str, str]:
    """Who speaks a station sentence now: ("", "the captain") for the captain's own, or
    ("standing order 'x'", its officer) while a standing order fires (package 31c)."""
    runtime = (getattr(ship, "extra", None) or {}).get("standing")
    firing = getattr(runtime, "firing", None)
    if firing is None:
        return "", "the captain"
    return f"standing order '{firing.name}'", firing.officer


def handle(ship: Any, text: str) -> tuple[str, str, dict[str, Any]]:
    verb = recognises(text, ship)
    extra = getattr(ship, "extra", None) or {}
    agents = extra.get("agents")
    journals = extra.get("agent_journals") or {}
    if agents is None:
        raise OrderError("This world has no stations for agents; it was made without them.")
    norm = normalise(text).replace(" , ", " ")
    by, officer = _speaker(ship)
    said_by = {"by": by} if by else {}
    if verb == "ask":
        station, question = _split_ask(text, ship)
        agent = _manned(agents, station)
        return (
            "agent.asked",
            agent.put_question(question, by=by, officer=officer),
            {"station": station, "question": question, **said_by},
        )
    if verb == "tell":
        station, words = _split_ask(text, ship, verb="tell")
        agent = _manned(agents, station)
        return (
            "agent.told",
            agent.put_word(words, by=by, officer=officer),
            {"station": station, "words": words, **said_by},
        )
    if verb == "show the journal of":
        m = _JOURNAL.match(norm)
        assert m is not None
        station = _station_in(m.group("who") or m.group("who2") or "", ship) or ""
        journal = journals.get(station)
        if journal is None:
            raise OrderError(f"There is no {station}'s journal; no {station} has been stationed.")
        # a query, like `state` and the book's listing: answered in the log, not journaled
        return "query.journal", "\n".join(journal.lines()), {"station": station}
    m = (_STAND_DOWN if verb == "stand down" else _RESUME).match(norm)
    assert m is not None
    station = _station_in(m.group("who") or m.groupdict().get("who2") or "", ship) or ""
    agent = _manned(agents, station)
    if verb == "stand down":
        return (
            "agent.stand_down",
            agent.request_stand_down("the captain's order", by="the captain"),
            {"station": station},
        )
    return "agent.resume", agent.resume("the captain"), {"station": station}


def _manned(agents: dict[str, Any], station: str) -> Any:
    agent = agents.get(station)
    if agent is None:
        raise OrderError(f"There is no {station} at the station; nobody has been stationed there.")
    return agent
