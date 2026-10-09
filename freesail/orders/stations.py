"""The station sentences (spec M4 §11, §12): what the captain says to an agent's station.

    ask the watcher how the sails are drawing     an order, journaled: the watcher answers
    tell the watcher we make for Falmouth         an order, journaled: no answer is owed
                                                  (`say to the watcher ...` the same)
    stand down the watcher                        an order, journaled: released with a save
    resume the watcher                            an order, journaled: the answer to a pause
    show the watcher's journal                    a query, like `state`: never journaled

The deck (package 37; spec M5 §29; as package 37g has it): the officer of the watch's
deck is given and taken by the captain's word, as the period had it, and neither unseats
him.

    you have the deck                             an order, journaled: the officer takes the
    Mr Pearce, you have the deck                  deck, with the night orders said to him
    I have the deck                               the captain takes the deck and no more:
                                                  the officer stays at his station, off watch
    you may tack ship if the land closes          his word allows a named thing, his
                                                  condition kept as said
    you may shape a course for Brest              a grant means what it says: for Brest
    you may not tack ship                         and takes it back
    you may work the ship                         his general authority to work the ship
    you have general authority                    (`you have my authority`), which keeps back
                                                  the port's business (the pilot taken or
                                                  declined at his hail among it, package
                                                  37h), his standing orders, a new
                                                  destination and what cannot be undone
    you may not work the ship                     and takes it back
    the officer of the watch                      a reading: who has the deck, since when,
                                                  what his word allows (`api.readings`)

**A named grant means what it says** (package 37g, item 17; the review's 10.5: in game 9
`you may shape a course for Brest` allowed a course shaped for anywhere, since a grant
was matched by its order word alone and kept one to a word). `read_grant` reads the
captain's words: the order, the thing they name where the order's own reader knows it (a
place for a course shaped, an anchor by its name, a person sent for), which is checked
when the officer gives the order, and his other words, kept as said for the officer to
judge. Several grants of one order stand together. A grant that resolves by its first
word to an order the officer may give already is refused, with the longer orders that
begin with the same word named (`you may set the reckoning` granted the sail verb `set`),
and so are two orders joined in one sentence (`you may tack or wear`).

`the officer` says the officer of the watch in any of them (`agent.STATION_ALIASES`).
`hand over the deck` is the officer's own (the `hand_over` tool), and the captain is
told to say `I have the deck`.

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

from freesail.agents.agent import (
    OFFICER,
    STATION_ALIASES,
    STATION_NAMES,
    STATIONS_ABOARD,
    Grant,
)
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import normalise

__all__ = [
    "GENERAL_GRANT",
    "GENERAL_TAKEN",
    "STANDING_STATION_VERBS",
    "STATION_VERBS",
    "for_standing",
    "handle",
    "read_grant",
    "recognises",
    "thing_named",
]

# The canonical verbs, as `data/vocabulary.yaml` lists them with `object: station`.
STATION_VERBS: tuple[str, ...] = (
    "ask",
    "tell",
    "stand down",
    "resume",
    "show the journal of",
    "you have the deck",
    "i have the deck",
    "you may",
    "you may not",
    "you may work the ship",
    "you may not work the ship",
)

# The general grant's two sentences, by their verbs in the vocabulary (package 37g, item
# 18): the words a captain would type for each are its synonyms there.
GENERAL_GRANT = "you may work the ship"
GENERAL_TAKEN = "you may not work the ship"

# The deck's sentences (package 37): the captain's word that gives and takes it, and his
# word for the watch. The officer's name before the giving, as the period had it ("Mr
# Pearce, you have the deck"), is any words before the comma, or before the sentence
# with no comma at all ("Mr Pearce you have the deck"; package 37l, game 10, where it was
# answered "did you mean 'moor'?"); "the deck is yours" is the same word.
_GIVE_DECK = re.compile(
    r"^(?:(?P<who>[\w' ]+?)\s*(?:,\s*|\s+))?(?:you have the deck|the deck is yours)\s*$"
)
_TAKE_DECK = re.compile(r"^(?:i have the deck|i'll take the deck|the captain has the deck)\s*$")
_ALLOW = re.compile(r"^you may (?P<not>not )?(?P<rest>.+)$")
_HAND_OVER = re.compile(r"^hand over the deck\s*$")

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
    for alias, name in STATION_ALIASES.items():
        # 'the officer' for the officer of the watch (package 37); 'the deck' only in
        # the deck's own sentences, never 'ask the deck'
        if alias != "the deck" and (who == alias or who.startswith(alias + " ")):
            return name
    return None


def _alias_words(who: str) -> int:
    """How many words of `who` name the station: the station's own name or its alias."""
    who = " ".join(who.split())
    for name in sorted(STATION_NAMES, key=lambda n: -len(n)):
        if who == name or who.startswith(name + " "):
            return len(name.split())
    for alias in STATION_ALIASES:
        if who == alias or who.startswith(alias + " "):
            return len(alias.split())
    return 0


def _general(text: str) -> tuple[str, str] | None:
    """The general grant's sentence in the text, if it is one: (its verb, `GENERAL_GRANT`
    or `GENERAL_TAKEN`; the captain's words after it, kept as said: 'in to Brest').
    The longest of the vocabulary's phrases for either that the text begins with, so
    that `you may not work the ship` is never `you may ...` and `you have not my
    authority` never `you have my authority`."""
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    said = normalise(text).replace(" , ", " ")
    words = said.split()
    for phrase in vocab.verb_phrases:  # longest first
        verb = vocab.phrase_to_verb[phrase]
        if verb not in (GENERAL_GRANT, GENERAL_TAKEN):
            continue
        pw = phrase.split()
        if words[: len(pw)] == pw:
            tail = " ".join(words[len(pw) :]).strip(" .")
            as_said = " ".join(text.split()).rstrip(" .")
            if tail and as_said.lower().endswith(tail):
                tail = as_said[len(as_said) - len(tail) :]  # his words as he said them
            return verb, tail
    return None


def recognises(text: str, ship: Any = None) -> str | None:
    """The station verb the text is, or None. The station's name must be one the game
    knows ("ask the watcher"), so an `ask` to nobody in particular is left to the
    imperative parser's refusal."""
    norm = normalise(text).replace(" , ", " ")
    deck = normalise(text).replace(" , ", ", ")
    if _GIVE_DECK.match(deck):
        return "you have the deck"
    if _TAKE_DECK.match(deck):
        return "i have the deck"
    if _HAND_OVER.match(deck):
        return "i have the deck"  # the captain's word for it, refused in words (handle)
    general = _general(text)
    if general is not None:
        return general[0]
    m = _ALLOW.match(deck)
    if m is not None:
        return "you may not" if m.group("not") else "you may"
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
    # the question is what follows the station's name (or its alias) in the text as said
    n = _alias_words(normalise(rest)) or len(station.split())
    words = rest.split()
    question = " ".join(words[n:]).lstrip(",:").strip()
    return station, question


def _aboard(ship: Any) -> tuple[str, ...]:
    """The stations a standing order may address: those the game can man now, and any
    this game has manned."""
    extra = getattr(ship, "extra", None) or {}
    # not the captain's station (package 40): a standing order speaks for the captain,
    # whoever holds his station, and never tells or asks him
    names = [n for n in STATIONS_ABOARD if n != "captain"]
    for name in list(extra.get("agents") or {}) + list(extra.get("agent_journals") or {}):
        if name not in names and name != "captain":
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
    seat = extra.get("player_seat")  # the player's seat at a station (package 40)
    journals = extra.get("agent_journals") or {}
    if agents is None:
        raise OrderError("This world has no stations for agents; it was made without them.")
    norm = normalise(text).replace(" , ", " ")
    by, officer = _speaker(ship)
    said_by = {"by": by} if by else {}
    if verb in (
        "you have the deck",
        "i have the deck",
        "you may",
        "you may not",
        GENERAL_GRANT,
        GENERAL_TAKEN,
    ):
        if by:
            raise OrderError(
                f"'{norm}' is the captain's own word to the {OFFICER}, not a standing order's."
            )
        return _deck(ship, agents, verb, text, seat)
    if verb == "ask":
        station, question = _split_ask(text, ship)
        agent = _manned(agents, station, seat)
        return (
            "agent.asked",
            agent.put_question(question, by=by, officer=officer),
            {"station": station, "question": question, **said_by},
        )
    if verb == "tell":
        station, words = _split_ask(text, ship, verb="tell")
        held = _held(agents, station, seat)
        if (held is None or not held.started or held.agent.released) and not by:
            # the captain's own word is kept (a station a replay has yet to seat is held by
            # nobody yet); a standing order's firing to nobody is refused as it always was,
            # or a book would fill the journal every glass
            return _keep_word(ship, station, words)
        agent = _manned(agents, station, seat)
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
    agent = _manned(agents, station, seat)
    if verb == "stand down":
        return (
            "agent.stand_down",
            agent.request_stand_down("the captain's order", by="the captain"),
            {"station": station},
        )
    return "agent.resume", agent.resume("the captain"), {"station": station}


def _keep_word(ship: Any, station: str, words: str) -> tuple[str, str, dict[str, Any]]:
    """`tell the <station> <words>` to a station nobody holds (package 37l; the review of
    gate 5c's playtests, G17: the words were refused and lost): kept in the station's
    journal and passed to whoever takes it next, in its first sample; the log says so."""
    from freesail.agents.journal import WORD_KEPT_KIND, Journal
    from freesail.orders.prompt import world_of

    words = " ".join(str(words).split())
    if not words:
        raise OrderError(f"Tell the {station} what? Say the words after the name.")
    world = world_of(ship)
    journals = (getattr(ship, "extra", None) or {}).get("agent_journals")
    if world is None or journals is None:
        raise OrderError(f"There is no {station} at the station; nobody has been stationed there.")
    journal = journals.setdefault(station, Journal(station))
    journal.append(
        world, f"The captain's word, kept for whoever takes the station: {words}", WORD_KEPT_KIND
    )
    return (
        "agent.told",
        f"The captain to the {station}: {words} (nobody holds the station; the words are kept "
        "in its journal for whoever takes it)",
        {"station": station, "words": words, "kept": True},
    )


def _manned(agents: dict[str, Any], station: str, seat: Any = None) -> Any:
    agent = _held(agents, station, seat)
    if agent is None:
        raise OrderError(f"There is no {station} at the station; nobody has been stationed there.")
    return agent


def _held(agents: dict[str, Any], station: str, seat: Any = None) -> Any:
    """Who holds a station: its harness, or the player's seat at it (package 40;
    `agents.seat`), to which the captain's sentences go as to a harness."""
    agent = agents.get(station)
    if agent is None and seat is not None and seat.station.name == station:
        return None if seat.agent.released else seat
    return agent


def _deck(
    ship: Any, agents: dict[str, Any], verb: str, text: str, seat: Any = None
) -> tuple[str, str, dict[str, Any]]:
    """The deck's sentences (package 37), carried out by the officer's harness, or by
    the player's seat at the station (package 40)."""
    deck = normalise(text).replace(" , ", ", ")
    if _HAND_OVER.match(deck):
        raise OrderError(
            f"'hand over the deck' is the {OFFICER}'s own order, given with his note; the "
            "captain takes the deck with 'I have the deck'."
        )
    agent = _held(agents, OFFICER, seat)
    if agent is None:
        raise OrderError(
            f"There is no {OFFICER} at the station; a model's door seats one first "
            "(docs/agents/Harness.md), and then the captain gives the deck."
        )
    if verb == "you have the deck":
        m = _GIVE_DECK.match(deck)
        assert m is not None
        who = " ".join((m.group("who") or "").split())
        return (
            "agent.deck",
            agent.give_deck(by="the captain", name=who),
            {"station": OFFICER, "deck": "given", "name": who},
        )
    if verb == "i have the deck":
        return (
            "agent.deck",
            agent.take_deck(by="the captain"),
            {"station": OFFICER, "deck": "taken"},
        )
    if verb == GENERAL_GRANT:
        _, words = _general(text) or (verb, "")
        return (
            "agent.deck",
            agent.allow_general(words),
            {"station": OFFICER, "general": True, "words": words},
        )
    if verb == GENERAL_TAKEN:
        return (
            "agent.deck",
            agent.disallow_general(),
            {"station": OFFICER, "general": False},
        )
    m = _ALLOW.match(deck)
    assert m is not None
    rest = m.group("rest").strip(" .")
    grant = read_grant(ship, None, rest, said=True)
    if verb == "you may not":
        return (
            "agent.deck",
            agent.disallow(grant.verb, grant=grant),
            {"station": OFFICER, "disallowed": grant.verb, "thing": grant.thing},
        )
    _not_his_already(agent, grant, rest)
    return (
        "agent.deck",
        agent.allow(grant.verb, grant.words, grant=grant),
        {"station": OFFICER, "allowed": grant.verb, "words": grant.words, "thing": grant.thing},
    )


def _verb_in(rest: str) -> tuple[str | None, str]:
    """The vocabulary's verb the captain's allowance names, longest first, and his words
    after it (his condition, kept as said)."""
    verb, _, words = _verb_and_phrase(rest)
    return verb, words


def _verb_and_phrase(rest: str) -> tuple[str | None, str, str]:
    """(the verb, the phrase of it the words began with, the words after it); (None, "",
    "") when the words begin with no order the officer could be allowed."""
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    words = rest.split()
    # an order whose phrase ends in a word that wants a thing after it, granted whole:
    # 'you may shape a course' is `shape a course for`, for any place
    if " ".join(words) in _WHOLE:
        verb = _WHOLE[" ".join(words)]
        return verb, verb, ""
    for phrase in vocab.verb_phrases:  # longest first
        pw = phrase.split()
        if words[: len(pw)] == pw:
            verb = vocab.phrase_to_verb[phrase]
            spec = vocab.verbs[verb]
            if spec.level in ("driver", "reading") or spec.object in ("standing", "station"):
                return None, "", ""
            return verb, phrase, " ".join(words[len(pw) :])
    return None, "", ""


_WHOLE = {
    "shape a course": "shape a course for",
    "shape courses": "shape a course for",
}


# The words that begin the captain's condition after the thing a grant names: 'you may
# shape a course for Brest if the wind serves'.
_CONDITION = re.compile(
    r"\s+(?=(?:if|when|whenever|unless|until|till|while|once|after|before|as|should|"
    r"provided|so long as|but only|only)\b)"
)


def thing_named(ship: Any, verb: str, phrase: str, said: str) -> tuple[str, str] | None:
    """The thing an order names, where the order's own reader knows it (package 37g, item
    17): (what it is checked by, the order with it in words), or None when the order
    names nothing a grant is checked by. A place for `shape a course for` (a feature of
    the chart by its name, or a position pricked on it), an anchor by its name for the
    ground tackle's orders, a person for `send for`. `phrase` is the verb's words as
    said (an anchor or a person may be named in them: `weigh the small bower`, `call
    the carpenter`), `said` the words after them."""
    from freesail.orders.vocabulary import load_vocabulary

    spec = load_vocabulary().verbs.get(verb)
    if spec is None:
        return None
    said = " ".join(str(said or "").split())
    if verb == "shape a course for":
        if not said:
            return None
        from freesail.orders.navigation import _position_in

        pricked = _position_in(said)
        if pricked is not None:
            from freesail.world.geo import format_position

            where = format_position(pricked)
            return f"place:{where}", f"{verb} {where}"
        nav = (getattr(ship, "extra", None) or {}).get("navigation")
        chart = getattr(getattr(nav, "world", None), "chart", None)
        if chart is None:
            return None
        from freesail.world.reckoning import _key

        key = _key(said)
        for f in chart.features.values():
            if _key(f.name) == key or _key(f.modern) == key:
                return f"place:{f.id}", f"{verb} {f.name}"
        return None
    if spec.object == "anchor":
        from freesail.orders.ground_tackle import _anchor_in_phrase

        name = _anchor_in_phrase(f"{phrase} {said}")
        if name is None:
            return None
        head = phrase if _anchor_in_phrase(phrase) else f"{verb}, the {name}"
        return f"anchor:{name}", head
    if verb == "send for":
        who = said
        if phrase.startswith("call the "):
            who = f"{phrase.removeprefix('call the ')} {said}".strip()
        nav = (getattr(ship, "extra", None) or {}).get("navigation")
        people = getattr(getattr(nav, "world", None), "people", None)
        person = people.find(who) if people is not None and who else None
        if person is None:
            return None
        return f"person:{person.name}", f"send for {person.name}"
    return None


def read_grant(ship: Any, verb: str | None, rest: str, said: bool = False) -> Grant:
    """The captain's grant from his words (package 37g, item 17). With `verb` None, `rest`
    is everything after `you may`: the order is the vocabulary's verb they begin with,
    longest first (refused in words when they begin with none, or when two orders are
    joined in one sentence); with a verb given, `rest` is his words after it (a grant a
    checkpoint from before this package holds, read as one given today). The thing the
    words name, where the order's own reader knows it, is what the grant is checked by;
    the words after it, or all of them when they name no such thing, are his condition,
    kept as said. A place the chart has not got is refused when the grant is said
    (`said`), as the order itself would be."""
    phrase = verb or ""
    if verb is None:
        verb, phrase, words = _verb_and_phrase(rest)
        if verb is None:
            raise OrderError(
                f"'{rest}' names no order the {OFFICER} could be allowed; say the order's "
                "words first ('you may tack ship if the land closes within two miles'), or "
                "'you may work the ship' for his general authority."
            )
        first = words.split()[0] if words.split() else ""
        if first in ("and", "or"):
            raise OrderError(
                f"'{rest}' joins two orders, and a grant names one: say each in its own "
                f"sentence ('you may {phrase}', and then the other)."
            )
    else:
        words = rest
    words = " ".join(str(words).split())
    head, tail = words, ""
    found = thing_named(ship, verb, phrase, head)
    if found is None and words:
        # his condition after the thing: tried at each place a condition's word begins
        for m in _CONDITION.finditer(words):
            head, tail = words[: m.start()], words[m.end() :]
            found = thing_named(ship, verb, phrase, head)
            if found is not None:
                break
    if found is None:
        if said and verb == "shape a course for" and words:
            # a place the chart has not got, refused now in the order's own words
            nav = (getattr(ship, "extra", None) or {}).get("navigation")
            if nav is not None and getattr(nav.world, "chart", None) is not None:
                place = _CONDITION.split(words)[0]
                raise OrderError(
                    f"The chart has no place named '{place}', so no course for it can be "
                    "allowed; name a place of the chart, or say 'you may shape a course' "
                    "for any."
                )
        return Grant(verb, words)
    key, thing = found
    return Grant(verb, tail, thing=thing, key=key)


def _not_his_already(agent: Any, grant: Grant, rest: str) -> None:
    """A grant that resolves to an order the officer may give already grants nothing, and
    is refused with the longer orders that begin with the same word named (package 37g,
    item 17; the report's 8.2, item 13: `You may set the reckoning` was logged "may set
    (the reckoning)", the sail verb, and the order was refused three seconds later;
    `You may let go` granted nothing for the anchor)."""
    from freesail.orders.vocabulary import load_vocabulary

    domain = getattr(agent, "domain", None)
    if domain is None:
        return
    vocab = load_vocabulary()
    spec = vocab.verbs[grant.verb]
    if domain.why_not(grant.verb, spec.object, spec.level) is not None:
        return
    first = rest.split()[0] if rest.split() else ""
    longer: list[str] = []
    for phrase in vocab.verb_phrases:
        if not phrase.startswith(first + " "):
            continue
        verb = vocab.phrase_to_verb[phrase]
        vs = vocab.verbs[verb]
        if vs.level in ("driver", "reading") or vs.object in ("standing", "station"):
            continue
        if domain.why_not(verb, vs.object, vs.level) is None:
            continue
        if phrase == verb and verb not in longer:
            longer.append(verb)
    named = (
        " The longer orders that begin with the same word: "
        + ", ".join(f"'you may {v}'" for v in longer)
        + "."
        if longer
        else " No longer order begins with that word; say the order as the officer would "
        "give it ('you may steer', 'you may tack ship')."
    )
    raise OrderError(
        f"'{rest}' reads as the order '{grant.verb}', which the {OFFICER} may give "
        f"already, so it would allow nothing.{named}"
    )
