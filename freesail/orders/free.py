"""The free lines (spec M7b §17a; package 53b): a short list of verbs that take any words
after them and do what the game can with them, no more, saying so in the log in the words
as used.

    give <thing> to <person>        the thing into his keeping (`hand ... to ...` the same;
                                    `give <person> <thing>` too)
    show <thing> to <person>        said, and nothing moves
    take <thing>                    a thing lying where he is into his own keeping
    stow <thing> in <place>         the thing put down: in a place aboard he is in or within
    hide <thing> in <place>         earshot of, or at the spot the words say in his own place
    put <thing> in/on <place>       ('on the table', 'in the bread locker'); ashore, at the
                                    place of the port he is at
    open <thing>, read <thing>      said, and nothing moves
    throw <thing> overboard         the thing over the side

beside the needs' `eat` and `drink` (package 54), which take any words after the verb and
are answered to the person alone as they always were (the vocabulary's `free_lines`).

**What the game does with them.** The giver is the order's person (`movement.
person_of_actor`: the captain at the prompt, a station's person at his station); a rule,
a standing order's firing and the director have no hands aboard and are refused in words.
Where the words name a thing known (`world.things`) within his reach (in his keeping, or
lying where he is) and, for a giving, a person within his reach (in his place or within
earshot of it aboard, at the same place of the same port ashore), the thing moves and the
log says where it is now ("By the captain, on the quarterdeck: gave the packet to Mr
Veale; the sealed packet is in Mr Veale's keeping."). Where they do not, or the verb moves
nothing (show, open, read), the line is accepted as said and nothing moves, the log saying
**"as said; nothing of the ship's changed"** in those words with the reason when a thing or
a person was named, so that the record and the replay stay honest and no model learns that
the ship did what it only said. A thing handed to a person a model or the player holds is
not put into his keeping without his own act: it lies before him, for his own hand to take.

**Heard where it is said.** A free line is a notable line of the log (`free.line`), heard
by the stations held within earshot of the giver as a word on deck (`Harness.hear`, the
stand-by's "a word on deck"), and read by the director in his sample as he reads the deck's
conversation. It is journaled as the order it is, so that a replay says it again and moves
the thing again.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.core.events import Severity
from freesail.orders.errors import OrderError
from freesail.orders.prompt import world_of

__all__ = ["AS_SAID", "FREE_KIND", "PAST", "Several", "execute", "hand_line", "not_found"]

Result = tuple[str, str, dict[str, Any]]

# The log's kind for a free line, and the words of a line accepted as said.
FREE_KIND = "free.line"
# A letter's words shown its reader, and its writer's own shown him (package 100): lines of
# the reach `reader` (`world.knowledge`), the person named and nobody else.
READ_KIND = "free.read"
WRITTEN_KIND = "free.written"
AS_SAID = "as said; nothing of the ship's changed"

# Each free verb phrase in the past, for the log's line in the words as used.
PAST: dict[str, str] = {
    "give": "gave",
    "hand": "handed",
    "show": "showed",
    "take": "took",
    "pick up": "picked up",
    "stow": "stowed",
    "hide": "hid",
    "conceal": "concealed",
    "put": "put",
    "open": "opened",
    "unseal": "unsealed",
    "break the seal of": "broke the seal of",
    "read": "read",
    "throw": "threw",
    "toss": "tossed",
    # package 100
    "write": "wrote",
    "write a letter": "wrote a letter",
    "pen": "penned",
    "seal": "sealed",
    "seal up": "sealed up",
    "examine": "examined",
    "look at": "looked at",
    "inspect": "inspected",
    "look over": "looked over",
    "burn": "burnt",
    "tear up": "tore up",
    "tear": "tore",
    "rip up": "ripped up",
    "destroy": "destroyed",
}

# The verbs of a thing with words (package 100), carried out by `_letter_act`.
LETTER_VERBS = frozenset({"write", "seal", "open", "read", "examine", "burn", "tear up"})
# How a thing destroyed went, by the verb as said.
_GONE_WORDS = {"burn": "burnt", "destroy": "destroyed"}

# Words of a free verb that are an order of the dialect said short (package 109), answered
# with the orders they may mean ('take a sight for the latitude' is the dialect's own).
_ANSWERED = {
    "take a sight": "Which sight? Say 'observe the sun' for the latitude at noon, or 'take a "
    "sight for the longitude' for the time sight.",
}

# The words a thing is put in, on or under something by (stow, hide, put).
_PUT_PREPS = ("in", "into", "on", "onto", "under", "inside", "behind", "beneath", "upon", "at")
_OVERBOARD = re.compile(
    r"^(?P<thing>.+?)\s+(?:overboard|over\s+board|over\s+the\s+side|into\s+the\s+sea)\.?$", re.I
)


def hand_line(text: str) -> bool:
    """Whether words the sail's `hand` could not read are a giving: `hand <thing> to
    <person>` (a bare `hand` is the sail's, `take in`; package 53b)."""
    low = " ".join(str(text).lower().split())
    return low.startswith("hand ") and " to " in low


def _said_words(text: str, phrase: str) -> tuple[str, str]:
    """(the words after the verb as said, the line's words in the past): 'give the packet
    to Mr Veale' -> ('the packet to Mr Veale', 'gave the packet to Mr Veale')."""
    raw = " ".join(str(text).split()).rstrip(".")
    n = len(phrase.split())
    rest = " ".join(raw.split(" ")[n:]).strip()
    past = PAST.get(phrase, phrase)
    return rest, f"{past} {rest}".strip()


def _who(world: Any, person: Any) -> str:
    return "the captain" if person is world.people.captain else person.name


def execute(ship: Any, text: str, verb: str, phrase: str) -> Result:
    """A free line given by the person of the order's actor: the thing moved where the words
    name one within reach, else the line as said; (the log's kind, its words, its data)."""
    from freesail.world import movement
    from freesail.world import things as TH

    world = world_of(ship)
    if world is None or getattr(world, "people", None) is None:
        raise OrderError("There is nobody here to do it: the ship is not in a world.")
    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
    person = movement.person_of_actor(world, actor)
    if person is None:
        raise OrderError(
            f"'{' '.join(str(text).split())}' is a person's own, said where he stands; a "
            "standing order, a rule and the director have no hands aboard."
        )
    rest, done = _said_words(text, phrase)
    answer = _ANSWERED.get(" ".join(str(text).lower().split()).rstrip("."))
    if answer is not None:
        raise OrderError(answer)
    if not rest:
        raise OrderError(f"{phrase.capitalize()} what? Say the words after '{phrase}'.")
    act = _letter_act(ship, world, person, verb, phrase, rest)
    said_as = " ".join(str(text).split())
    then: list[tuple[Any, ...]] = []
    if act is not None:
        moved, outcome, why, thing, to = (
            act["moved"],
            act["outcome"],
            act["why"],
            act["thing"],
            None,
        )
        done = act.get("done") or done
        said_as = act.get("said") or said_as
        then = act.get("then") or []
    else:
        moved, outcome, why, thing, to = _carry_out(world, person, verb, rest)
    if thing is None:
        # the words found nothing (package 109, the owner's note 9): refused, saying what
        # was not found and what the game does know by that name, never 'as said'
        raise OrderError(not_found(world, person, phrase, rest, text))
    where = movement.where_words(world, person)
    who = _who(world, person)
    if moved:
        line = f"By {who}, {where}: {done}; {outcome}."
    else:
        line = f"By {who}, {where}: {done}, {AS_SAID}" + (f" ({why})." if why else ".")
    heard = _hearers(world, person)
    for h in heard:
        h.hear(line)
    here = TH._where_of_person(world, person)
    data: dict[str, Any] = {
        "verb": verb,
        "said": said_as,
        "person": person.name,
        "place": here[0],
        "moved": moved,
        "heard_by": [h.station.name for h in heard],
        "notable": True,
    }
    if thing is not None:
        data["thing"] = thing.id
    if to is not None:
        data["to"] = to.name
    if said_as != " ".join(str(text).split()):
        from freesail.core.world import ORDER_AS_SAID

        data[ORDER_AS_SAID] = said_as  # the order said without the letter's words
    if then:
        from freesail.core.world import THEN_LINES

        data[THEN_LINES] = then
    return FREE_KIND, line, data


# The free verbs a person's words begin with when the director speaks as him (package 84,
# step 4; the design's §2.12, step 6): `say as Mr Gill: give the packet to Mr Pope`.
_SPOKEN = re.compile(
    r"^(?P<verb>give|gives|hand|hands|show|shows|take|takes|throw|throws|stow|stows|hide|hides"
    r"|put|puts)\s+(?P<rest>.+)$",
    re.I,
)


def spoken(world: Any, person: Any, words: str) -> tuple[str, str, dict[str, Any]] | None:
    """A free line in the words a person nobody holds is given to say (`say as <person>:
    give the packet to <person>`; package 84, step 4): performed as his own, by the rule of
    reach, where the words begin with a free verb; (the log's kind, the line, its data), or
    None when they are no free line. Heard by the stations held at his place on any hull,
    as a free line of his own would be."""
    from freesail.agents.agent import DIRECTOR
    from freesail.world import movement
    from freesail.world import things as TH
    from freesail.world.hearing import spot_of, station_spot, stations_everywhere, within_hearing

    low = " ".join(str(words).split()).rstrip(".")
    m = _SPOKEN.match(low)
    if m is None:
        return None
    verb = m.group("verb").lower().rstrip("s")
    verb = "give" if verb == "hand" else verb
    rest = m.group("rest")
    try:
        moved, outcome, why, thing, to = _carry_out(world, person, verb, rest)
    except Several:
        # the director's say-as is answered as it was (package 109 left it): said
        moved, outcome, why, thing, to = False, "", "", None, None
    where = movement.where_words(world, person)
    done = f"{PAST.get(verb, verb)} {rest}"
    if moved:
        line = f"{person.name}, {where}: {done}; {outcome}."
    else:
        line = f"{person.name}, {where}: {done}, {AS_SAID}" + (f" ({why})." if why else ".")
    here = spot_of(world, person)
    heard = [
        h
        for w, h in stations_everywhere(world)
        if h.station.name != DIRECTOR and within_hearing(here, station_spot(w, h.station.name))
    ]
    for h in heard:
        h.hear(line)
    place = TH._where_of_person(world, person)[0]
    data: dict[str, Any] = {
        "verb": verb,
        "said": low,
        "person": person.name,
        "place": place,
        "moved": moved,
        "heard_by": [h.station.name for h in heard],
        "notable": True,
        "spoken_as": True,
    }
    if thing is not None:
        data["thing"] = thing.id
    if to is not None:
        data["to"] = to.name
    return FREE_KIND, line, data


def _carry_out(world: Any, person: Any, verb: str, rest: str) -> tuple[bool, str, str, Any, Any]:
    """(moved, the outcome's words, the reason nothing moved or "", the thing, the person
    given to) for a free line's words."""
    from freesail.world import things as TH

    if verb in ("give", "show"):
        thing, to = _thing_and_person(world, rest, person)
        if thing is None:
            return False, "", "", None, to
        if to is None:
            return (
                False,
                "",
                f"nobody named is among the people; {thing.the} stays as it was",
                thing,
                None,
            )
        if verb == "show":
            return False, "", "", thing, to
        if to is person:
            return False, "", f"{thing.the} is yours to give, not to take", thing, to
        why = TH.reach_why(world, person, thing) or TH.person_reach_why(world, person, to)
        if why:
            return False, "", why, thing, to
        held = TH.held_by(world, to)
        if held:
            place, port, ashore_at, hull = TH._where_of_person(world, to)
            TH.put(
                thing,
                {
                    "place": place,
                    "spot": f"before {to.name}",
                    "port": port,
                    "ashore_at": ashore_at,
                    "hull": hull,
                },
            )
            return (
                True,
                f"{thing.the} lies before {to.name}, for his own hand to take ('take "
                f"{thing.the.removeprefix('the ')}')",
                "",
                thing,
                to,
            )
        TH.put(thing, {"keeper": to.id, "keeper_home": str(getattr(to, "home", "") or "")})
        return True, f"{thing.the} is in {_who(world, to)}'s keeping", "", thing, to
    if verb in ("open", "read"):
        thing = _one(world, person, rest)
        return False, "", "" if thing is not None else "", thing, None
    if verb == "take":
        words = re.split(r"\s+from\s+", rest, maxsplit=1, flags=re.I)[0]
        thing = _one(world, person, words) or _one(world, person, rest)
        if thing is None:
            return False, "", "", None, None
        if thing.keeper == person.id:
            return False, "", f"{thing.the} is in your keeping already", thing, None
        why = TH.reach_why(world, person, thing)
        if why:
            return False, "", why, thing, None
        TH.put(thing, {"keeper": person.id, "keeper_home": str(getattr(person, "home", "") or "")})
        return True, f"{thing.the} is in {_who(world, person)}'s keeping", "", thing, None
    if verb == "throw":
        m = _OVERBOARD.match(rest)
        thing = (
            _one(world, person, m.group("thing")) if m is not None else _one(world, person, rest)
        )
        if thing is None:
            return False, "", "", None, None
        if m is None:
            return (
                False,
                "",
                f"{thing.the} goes nowhere but over the side by these words",
                thing,
                None,
            )
        if not person.aboard and person.where != "boat":
            return False, "", "you are ashore, with no side to throw it over", thing, None
        why = TH.reach_why(world, person, thing)
        if why:
            return False, "", why, thing, None
        TH.put(thing, {"place": TH.OVERBOARD})
        return True, f"{thing.the} went over the side", "", thing, None
    # stow, hide, put
    thing, dest = _thing_and_dest(world, person, rest)
    if thing is None:
        return False, "", "", None, None
    if not dest:
        return False, "", f"say where: '{verb} {thing.the} in the hold'", thing, None
    why = TH.reach_why(world, person, thing)
    if why:
        return False, "", why, thing, None
    where, why = _destination(world, person, dest)
    if where is None:
        return False, "", why, thing, None
    TH.put(thing, where)
    return True, f"{thing.the} is {TH.where_words(world, thing)}", "", thing, None


# ---------------------------------------------------------------------------
# A thing with words (package 100)
# ---------------------------------------------------------------------------

_WRITE = re.compile(
    r"^(?:(?:a|the)\s+)?(?:letter\s+)?(?:to|for)\s+(?P<to>[^:]+?)\s*:\s*(?P<words>.+)$", re.I
)
_QUOTED = "\"'“”‘’"


def _letter_act(
    ship: Any, world: Any, person: Any, verb: str, phrase: str, rest: str
) -> dict[str, Any] | None:
    """A free line of a thing with words (package 100): written, sealed, opened, read,
    looked at, burnt or torn up; {moved, outcome, why, thing, done, said, then}, or None
    where the verb is no such (and `open` and `read` of a thing that is no letter, which
    move nothing and are said as they always were)."""
    from freesail.world import things as TH

    if verb not in LETTER_VERBS:
        return None
    if verb == "write":
        return _write(ship, world, person, phrase, rest)
    thing = _one(world, person, rest)
    out: dict[str, Any] = {"moved": False, "outcome": "", "why": "", "thing": thing}
    if thing is None:
        return out
    if verb in ("open", "read") and not thing.is_letter:
        return None
    why = TH.reach_why(world, person, thing)
    if why:
        out["why"] = why
        return out
    the = thing.the
    if verb == "examine":
        out["moved"] = True
        out["outcome"] = TH.seen_words(world, thing)
        return out
    if verb == "seal":
        if not thing.is_letter:
            out["why"] = f"{the} is no letter to seal"
        elif thing.broken:
            out["why"] = "its seal is broken, and it shows; no new seal hides it"
        elif thing.sealed:
            out["why"] = f"{the} is sealed already"
        else:
            thing.sealed = True
            out["moved"] = True
            out["outcome"] = f"{the} is sealed"
        return out
    if verb == "open":
        if thing.broken:
            out["why"] = f"its seal is broken already; 'read the {thing.head}'"
        elif not thing.sealed:
            out["why"] = f"{the} is not sealed; 'read the {thing.head}'"
        else:
            thing.broken = True
            out["moved"] = True
            out["outcome"] = f"the seal of {the} is broken, and it shows"
        return out
    if verb == "read":
        if thing.sealed and not thing.broken:
            out["why"] = (
                f"{the} is sealed; it is read only by breaking its seal ('open the "
                f"{thing.head}'), which shows"
            )
            return out
        out["moved"] = True
        out["outcome"] = f"{the} read"
        out["then"] = [
            (
                Severity.NOTABLE,
                READ_KIND,
                TH.letter_words(thing),
                {"to": person.name, "thing": thing.id, "place": "", "reader": person.name},
            )
        ]
        return out
    # burn, tear up
    if not thing.is_paper:
        out["why"] = f"{the} is no paper to {phrase}; throw it overboard"
        return out
    if verb == "burn" and person.where == "boat":
        out["why"] = "there is no fire in the boat to burn it; tear it up, or throw it overboard"
        return out
    gone = _GONE_WORDS.get(phrase, "burnt" if verb == "burn" else "torn up")
    TH.put(thing, {"place": TH.GONE})
    thing.gone = gone
    out["moved"] = True
    out["outcome"] = f"{the} is {gone}, and gone"
    return out


def _write(ship: Any, world: Any, person: Any, phrase: str, rest: str) -> dict[str, Any]:
    """`write a letter to <whom>: "<words>"` by the drafting's road (package 100; `books`):
    the writer's mark and the hour, the captain gone below to his table and at his writing;
    the letter in the writer's keeping, its words shown to him, the line heard without
    them."""
    from freesail.world import books
    from freesail.world import things as TH

    m = _WRITE.match(rest.strip())
    if m is None:
        raise OrderError(
            "Write what, and to whom? Say 'write a letter to <whom>: \"<its words>\"'."
        )
    to = " ".join(m.group("to").split()).strip(_QUOTED + " ")
    words = " ".join(m.group("words").split()).strip()
    if len(words) >= 2 and words[0] in _QUOTED and words[-1] in _QUOTED:
        words = words[1:-1].strip()
    if not to or not words:
        raise OrderError(
            "Write what, and to whom? Say 'write a letter to <whom>: \"<its words>\"'."
        )
    from freesail.world.captive import is_captive

    if not is_captive(person):
        books._in_the_cabin(ship, world)  # the captain's writing is done at his table
    name = f"a letter to {to}"
    thing = TH.Thing(TH._new_id(world, name), name)
    thing.words, thing.author, thing.to, thing.written = words, person.name, to, books._stamp(world)
    TH.addressed(world, thing)
    TH.put(thing, {"keeper": person.id, "keeper_home": str(getattr(person, "home", "") or "")})
    TH.things_of(world).append(thing)
    said = f"{phrase} {rest[: m.start('words')].rstrip().rstrip(':').strip()}"
    return {
        "moved": True,
        "outcome": f"the letter is in {_who(world, person)}'s keeping",
        "why": "",
        "thing": thing,
        "done": f"wrote a letter to {to}",
        "said": " ".join(said.split()),
        "then": [
            (
                Severity.NOTABLE,
                WRITTEN_KIND,
                f'Your letter to {to}, as written: "{words}"',
                {"to": person.name, "thing": thing.id, "place": "", "writer": person.name},
            )
        ],
    }


class Several(OrderError):
    """Words that name more than one thing within reach (package 109): refused naming
    them apart; `things` the things named."""

    def __init__(self, message: str, things: list[Any]) -> None:
        super().__init__(message)
        self.things = things
        self.data = {CHOICES: [t.id for t in things]}


# The rejected order's data that keeps the things a refusal named apart (package 109), so
# that 'the first', 'the second' and 'the other' said after it take one of them.
CHOICES = "choices"
_ORDINAL = re.compile(
    r"^(?:the\s+)?(?P<ord>first|second|third|fourth|last|other)\b\s*(?P<rest>.*)$", re.I
)
_ORDINALS = {"first": 0, "second": 1, "third": 2, "fourth": 3, "last": -1}
_COUNT = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def _in_reach(world: Any, person: Any, things: list[Any]) -> list[Any]:
    from freesail.world import things as TH

    return [t for t in things if TH.reach_why(world, person, t) is None]


def _pick(world: Any, person: Any, words: str) -> tuple[Any, list[Any]]:
    """(the one thing the words name, or None; the things they name apart where they name
    several within reach, or none of them in reach): 'the first letter', 'the other', 'the
    second' after a refusal that named two (package 109); else the one found, or the one
    of several within his reach."""
    from freesail.world import things as TH

    m = _ORDINAL.match(" ".join(str(words).split()))
    if m is not None and person is not None:
        noun = m.group("rest").strip()
        if noun:
            found = TH.find(world, noun)
            cands = _in_reach(world, person, found) or found
        else:
            cands = _last_choices(world, person)
        chosen = _by_ordinal(world, person, m.group("ord").lower(), cands)
        if chosen is not None:
            return chosen, []
    found = TH.find(world, words)
    if len(found) <= 1:
        return (found[0] if found else None), []
    if person is None:
        return None, found
    near = _in_reach(world, person, found)
    if len(near) == 1:
        return near[0], []
    return None, near or found


def _by_ordinal(world: Any, person: Any, word: str, cands: list[Any]) -> Any:
    if len(cands) < 2:
        return None
    if word == "other":
        last = _last_handled(world, person, cands)
        others = [t for t in cands if t.id != last]
        return others[0] if len(others) == 1 else None
    i = _ORDINALS[word]
    return cands[i] if -len(cands) <= i < len(cands) else None


def _recent(world: Any, n: int = 2000):
    log = getattr(world, "log", None)
    if log is None:
        return
    for i in range(len(log) - 1, max(-1, len(log) - 1 - n), -1):
        yield log[i]


def _last_handled(world: Any, person: Any, cands: list[Any]) -> str:
    """The id of the one of these things the person's last free line named."""
    ids = {t.id for t in cands}
    for e in _recent(world):
        if e.kind == FREE_KIND and e.data.get("person") == person.name:
            if e.data.get("thing") in ids:
                return str(e.data["thing"])
    return ""


def _last_choices(world: Any, person: Any) -> list[Any]:
    """The things the person's last refusal named apart, still known (package 109)."""
    from freesail.world import things as TH

    actor = _actor_of(world)
    for e in _recent(world):
        if e.kind == "order.rejected" and e.actor == actor and e.data.get(CHOICES):
            ids = list(e.data[CHOICES])
            known = {t.id: t for t in TH.things_of(world)}
            return [known[i] for i in ids if i in known]
    return []


def _actor_of(world: Any) -> str:
    extra = getattr(getattr(world, "ship", None), "extra", None)
    if not isinstance(extra, dict):
        return "captain"
    return str(extra.get("order_actor") or "captain")


def _one(world: Any, person: Any, words: str) -> Any:
    """The one thing the words name, the one within his reach where they name several;
    None when they name none; refused naming them apart (`Several`) where they name
    several within his reach (package 109)."""
    thing, several = _pick(world, person, words)
    if thing is None and several:
        raise Several(several_words(world, person, words, several), several)
    return thing


def _thing_and_person(world: Any, rest: str, giver: Any = None) -> tuple[Any, Any]:
    """(the thing, the person) of 'the packet to Mr Veale' or 'Mr Veale the packet'; either
    None where the words name none; refused naming them apart where the thing's words name
    several within the giver's reach (package 109)."""
    people = world.people
    words = rest.split()
    low = [w.lower() for w in words]
    thing = person = None
    several: list[Any] = []
    said = rest
    for i in range(len(words) - 1, 0, -1):
        if low[i] != "to":
            continue
        t, sev = _pick(world, giver, " ".join(words[:i]))
        p = people.find_anywhere(" ".join(words[i + 1 :]))
        if t or sev or p:
            thing = thing or t
            person = person or p
            if sev and not several:
                several, said = sev, " ".join(words[:i])
        if t is not None and p is not None:
            return t, p
    for i in range(1, len(words)):
        p = people.find_anywhere(" ".join(words[:i]))
        t, sev = _pick(world, giver, " ".join(words[i:]))
        if p is not None and t is not None:
            return t, p
        if p is not None and sev and not several:
            several, said = sev, " ".join(words[i:])
    if thing is None and not several:
        thing, several = _pick(world, giver, rest)
    if thing is None and several:
        raise Several(several_words(world, giver, said, several), several)
    return thing, person


def _thing_and_dest(world: Any, person: Any, rest: str) -> tuple[Any, str]:
    """(the thing, the words of where it goes) of 'the packet in the bread locker'."""
    words = rest.split()
    several: list[Any] = []
    said = rest
    for i in range(1, len(words)):
        if words[i].lower() not in _PUT_PREPS:
            continue
        thing, sev = _pick(world, person, " ".join(words[:i]))
        if thing is not None:
            return thing, " ".join(words[i:])
        if sev and not several:
            several, said = sev, " ".join(words[:i])
    if not several:
        return _one(world, person, rest), ""
    raise Several(several_words(world, person, said, several), several)


# ---------------------------------------------------------------------------
# The refusals in words (package 109)
# ---------------------------------------------------------------------------


def several_words(world: Any, person: Any, words: str, things: list[Any]) -> str:
    """Several things named by one name, told apart by what tells them apart: a letter's
    writer and its hour, whose keeping or where it lies, and the first words of one he may
    read; and how to say which."""
    from freesail.world import things as TH

    n = len(things)
    heads = {t.head for t in things}
    noun = (things[0].head + "s") if len(heads) == 1 and things[0].head else "things"
    parts = []
    for i, t in enumerate(things):
        bits = [TH.name_words(t)]
        if t.is_letter:
            if t.author and " from " not in t.name.lower():
                bits.append(f"in {t.author}'s hand")
            if t.written:
                bits.append(f"written {t.written}")
        bits.append(TH.where_words(world, t))
        if t.is_letter and t.words and (not t.sealed or t.broken):
            first = " ".join(t.words.split()[:6])
            more = "..." if len(t.words.split()) > 6 else ""
            bits.append(f'beginning "{first}{more}"')
        ordinal = ("the first", "the second", "the third", "the fourth")[i] if i < 4 else ""
        parts.append((f"{ordinal}, " if ordinal else "") + ", ".join(bits))
    said = " ".join(str(words).split())
    return (
        f"'{said}' names {_COUNT.get(n, str(n))} {noun}: "
        + "; ".join(parts)
        + ". Say which: by its writer or what it is ('the letter from ...'), or 'the first',"
        " 'the second'" + (", 'the other'" if n == 2 else "") + "."
    )


def _gone_words(world: Any, words: str) -> str:
    from freesail.world import things as TH

    gone = [t for t in TH.find(world, words, gone=True) if t.place in (TH.OVERBOARD, TH.GONE)]
    if not gone:
        return ""
    t = gone[-1]
    if t.place == TH.OVERBOARD:
        return f"{t.the} went over the side"
    return f"{t.the} is {t.gone or 'destroyed'}, and gone"


def _near_order(text: str) -> str:
    """An order of the dialect the words were near ('take posession of' for 'take
    possession of'), or ""."""
    import difflib

    from freesail.orders.vocabulary import key, load_vocabulary

    said = key(text).split()
    vocab = load_vocabulary()
    best, best_r = "", 0.0
    for phrase, verb in vocab.phrase_to_verb.items():
        spec = vocab.verbs.get(verb)
        if spec is None or spec.object == "free" or verb in vocab.readings:
            continue
        n = len(phrase.split())
        if n < 2 or len(said) < n:
            continue
        head = " ".join(said[:n])
        if head == phrase:
            continue
        r = difflib.SequenceMatcher(None, head, phrase).ratio()
        if r > best_r:
            best, best_r = phrase, r
    return best if best_r >= 0.88 else ""


def reach_words(world: Any, person: Any) -> str:
    """What is in the person's keeping and what lies where he stands, by their listed
    names: 'in your keeping: a purse; lying here: a sealed packet'; "" for nothing."""
    from freesail.world import things as TH

    kept = TH.kept_by(world, person)
    here = TH._where_of_person(world, person)
    lying = [
        t
        for t in TH.things_of(world)
        if not t.keeper
        and t.place not in (TH.OVERBOARD, TH.GONE)
        and TH.same_place(here, TH.place_of(world, t))
    ]
    parts = []
    if kept:
        parts.append("in your keeping: " + ", ".join(TH.name_words(t) for t in kept))
    if lying:
        parts.append("lying here: " + ", ".join(TH.lying_words(t) for t in lying))
    return "; ".join(parts)


def not_found(world: Any, person: Any, phrase: str, rest: str, text: str) -> str:
    """The refusal of a free order whose words found nothing (package 109): what was not
    found, and what the game does know by that name: a thing gone, a person, an order of
    the dialect the words were near, and the things in his reach."""
    words = " ".join(str(rest).split())
    m = _OVERBOARD.match(words)
    words = m.group("thing") if m is not None else words
    head = re.split(r"\s+(?:to|in|into|on|onto|under|from|overboard)\s+", words, maxsplit=1)[0]
    bare = re.sub(r"^(?:the|a|an|some|my|his|your)\s+", "", head, flags=re.I) or head
    out = f"Nothing of that name is known: there is no {bare} that you know of."
    more = []
    gone = _gone_words(world, head)
    if gone:
        more.append(f"{gone[:1].upper()}{gone[1:]}.")
    who = world.people.find_anywhere(head) if getattr(world, "people", None) else None
    if who is not None:
        more.append(f"{who.name} is one of the people, not a thing to {phrase}.")
    near = _near_order(text)
    if near:
        more.append(f"The ship's orders know '{near}'.")
    reach = reach_words(world, person)
    more.append(f"You have {reach}." if reach else "You keep nothing, and nothing lies here.")
    return " ".join([out, *more])


def _destination(world: Any, person: Any, dest: str) -> tuple[dict[str, Any] | None, str]:
    """Where the words put a thing down, within the giver's reach: a place aboard he is in
    or within earshot of, or a spot in his own place; ashore, his place of the port or a
    spot in it. (None, the reason) where the words name a place out of his reach."""
    from freesail.world import things as TH
    from freesail.world.places import PLACES, find_port_place

    here = TH._where_of_person(world, person)
    if here[0] == "shore":
        port = TH._port(world, here[1])
        pp = None
        m = re.match(r"^(?:in|into|on|at|inside)\s+(?:the\s+)?(?P<pp>.+)$", dest, re.I)
        if port is not None and m is not None:
            pp = find_port_place(port, m.group("pp"))
        if pp is not None and pp.id != (here[2] or "quay"):
            return None, f"{pp.name} is not where you are; go there first"
        return {
            "place": "shore",
            "port": here[1],
            "ashore_at": here[2] or "quay",
            "spot": "" if pp is not None else dest,
        }, ""
    found = TH._place_in(dest)
    if found is not None:
        place, spot = found
        if not TH.same_place(here, (place, None, "", here[3])):
            return None, f"{PLACES[place].name} is not where you are; go there first"
        return {"place": place, "spot": spot, "hull": here[3]}, ""
    return {"place": here[0], "spot": dest, "hull": here[3]}, ""


def _hearers(world: Any, person: Any) -> list[Any]:
    """The stations held within the giver's reach (his place or its earshot aboard, his
    place of the port ashore), not his own: a free line is heard where it is said."""
    from freesail.agents.agent import DIRECTOR
    from freesail.agents.harness import _stations_held
    from freesail.world import things as TH

    here = TH._where_of_person(world, person)
    out = []
    for h in _stations_held(world):
        name = getattr(h.station, "person", "") or ""
        if h.station.name == DIRECTOR or not name or name == person.name:
            continue
        other = world.people.find(name)
        if other is None or other is person:
            continue
        if TH.same_place(here, TH._where_of_person(world, other)):
            out.append(h)
    return out
