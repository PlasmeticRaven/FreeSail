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
"""

from __future__ import annotations

import re
from typing import Any

from freesail.agents.agent import STATION_NAMES
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import normalise

__all__ = ["STATION_VERBS", "handle", "recognises"]

# The canonical verbs, as `data/vocabulary.yaml` lists them with `object: station`.
STATION_VERBS: tuple[str, ...] = ("ask", "tell", "stand down", "resume", "show the journal of")

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


def handle(ship: Any, text: str) -> tuple[str, str, dict[str, Any]]:
    verb = recognises(text, ship)
    extra = getattr(ship, "extra", None) or {}
    agents = extra.get("agents")
    journals = extra.get("agent_journals") or {}
    if agents is None:
        raise OrderError("This world has no stations for agents; it was made without them.")
    norm = normalise(text).replace(" , ", " ")
    if verb == "ask":
        station, question = _split_ask(text, ship)
        agent = _manned(agents, station)
        return (
            "agent.asked",
            agent.put_question(question),
            {"station": station, "question": question},
        )
    if verb == "tell":
        station, words = _split_ask(text, ship, verb="tell")
        agent = _manned(agents, station)
        return "agent.told", agent.put_word(words), {"station": station, "words": words}
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
