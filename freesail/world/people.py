"""The people (spec M5 §22; package 35): the named few, each with a name, a role, a
skill where a system reads it, a place and a state.

The inward minimum of `docs/design/InwardAndOutward.md` and no more. The crew of
milestone 3 stays counts and ratings; these are the few the story names: the captain,
the master (package 33a's `Master`, now a person whole), the lieutenants or the mates,
the surgeon, the purser, the boatswain, the carpenter, the sailmaker, the master's
mates, and a midshipman or a boy as the messenger. Each is a sailor of the muster, found
by his post or drawn from his station by the ship file's `crew.people` list
(`tools/gen_ships.py` writes it; no ship is special-cased), so his name is the muster's
and the counts of spec M3 §2.3 are what they were. The pilot comes aboard as a person
too (`freesail.world.ports`), borne as a supernumerary as the Regulations have him.

A person's **place** is one of `freesail.world.places.PLACES`; his **state** is read
from it and from the watch bill: on deck, below, asleep (a watch-keeper in his watch
below at night), ashore, in the boat, sick, or occupied by a task until a tick. Orders
move people where the period's orders did: `send for the master` and `pass the word
for the carpenter` bring a man to where the captain is by the messenger, who takes
`PASS_THE_WORD_S` to find him; `go below` and `come on deck` move the captain between
the cabin and the quarterdeck; the boat's going and coming carry a person ashore and
back. A task that occupies a person (the lunar, the day's work, the boat) says so in the
log and refuses a second call on him in words (`People.occupy`, `People.free`).

A **message** reaches the captain where he is, through what the ship models (truth 68):
it comes aboard in the boat or with the pilot (`People.message_aboard`), the messenger
carries it to the cabin door or the quarterdeck (`PASS_THE_WORD_S` later), and the log
says each step in order; never a line from nowhere. The harness's stations may later
bind to a person (M6); here a person is data and a line.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world.places import PLACES, place_words

__all__ = [
    "PASS_THE_WORD_S",
    "ROLE_WORDS",
    "WATCH_KEEPERS",
    "Message",
    "People",
    "Person",
]

# The messenger's time to find a man about the ship and bring him aft, or to carry a
# letter from the gangway to the cabin door: a minute (judgement; a frigate is a hundred
# and forty feet long and the man may be below).
PASS_THE_WORD_S = 60

# Where the man in whose place the officer of the watch stands is, in the people's words
# (package 37g, item 10): with the watch while the station has the deck, and off watch
# while it is seated without it.
ON_DECK_WORDS = "on deck, with the watch"
OFF_WATCH_WORDS = "off watch"

# The roles that keep a watch and sleep in the other at night (Luce 1884 ch. XX: the
# lieutenants and the master's mates and midshipmen by watches; the first lieutenant,
# the master and the standing officers keep no watch), paired with the watch each keeps
# in turn: the second lieutenant the starboard, the third the larboard, and so down
# (judgement: the bill's custom, not a page).
WATCH_KEEPERS = (
    "second lieutenant",
    "third lieutenant",
    "lieutenant",
    "mate",
    "master's mate",
    "midshipman",
    "boy",
)

# The words a role is asked for by, each to the post or role as the ship file names it.
ROLE_WORDS: dict[str, str] = {
    "captain": "captain",
    "commander": "commander",
    "master": "master",
    "the master": "master",
    "first lieutenant": "first lieutenant",
    "first": "first lieutenant",
    "second lieutenant": "second lieutenant",
    "third lieutenant": "third lieutenant",
    "lieutenant": "lieutenant",
    "mate": "mate",
    "surgeon": "surgeon",
    "doctor": "surgeon",
    "purser": "purser",
    "boatswain": "boatswain",
    "bosun": "boatswain",
    "carpenter": "carpenter",
    "sailmaker": "sailmaker",
    "sail maker": "sailmaker",
    "gunner": "gunner",
    "master at arms": "master-at-arms",
    "masters mate": "master's mate",
    "master's mate": "master's mate",
    "midshipman": "midshipman",
    "mid": "midshipman",
    "boy": "boy",
    "messenger": "messenger",
    "pilot": "pilot",
}


@dataclass
class Person:
    """One of the named few. `mirror` is package 33a's `Master` for the master, whose
    place and occupation the reckoning keeps; this person reads and writes through it."""

    id: str
    name: str  # "Mr Harvey", "Captain Bowen", "the pilot, Mr Pascoe of Falmouth"
    role: str
    skill: float
    place: str = "quarterdeck"
    aboard: bool = True
    sick: bool = False
    messenger: bool = False
    watch: str | None = None  # "starboard" or "larboard" for a watch-keeper
    occupied_until: int | None = None
    occupied_with: str = ""
    # a move in hand: where he is going, when he gets there, and the line to say
    pending: tuple[str, int, str] | None = None
    mirror: Any = None
    sailor_id: str | None = None
    port: str | None = None  # the pilot's port
    up: bool = False  # called from his watch below: not asleep again until his watch

    @property
    def where(self) -> str:
        """His place now, the mirror's for the master ('on deck' is the quarterdeck,
        'below' the gunroom where he works his sights)."""
        if self.mirror is not None:
            if self.mirror.place == "on deck":
                return "quarterdeck"
            # below: the cabin when he went below as the captain, else the gunroom where
            # he works his sights
            return self.place if PLACES.get(self.place, PLACES["gunroom"]).below else "gunroom"
        return self.place

    @where.setter
    def where(self, place: str) -> None:
        if self.mirror is not None:
            self.mirror.place = "on deck" if place in ("quarterdeck", "deck", "tops") else "below"
        self.place = place

    @property
    def occupied(self) -> bool:
        if self.mirror is not None:
            return bool(self.mirror.occupied)
        return self.occupied_until is not None

    @property
    def task(self) -> str:
        return self.mirror.occupied_with if self.mirror is not None else self.occupied_with

    @property
    def surname(self) -> str:
        return self.name.split()[-1].rstrip(",")

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "skill": round(self.skill, 2),
            "place": self.where,
            "aboard": self.aboard,
            "occupied_with": self.task,
        }


@dataclass
class Message:
    """A letter or a word for someone aboard, carried by the boat or the pilot."""

    text: str
    origin: str  # "Brest", "the port admiral"
    to: str = "captain"
    carried_by: str = "the boat"


class People:
    """The people of one World, built from the muster at the first call (the composer
    musters the crew after the World is made, as the master is found: `reckoning`)."""

    def __init__(self, world: Any) -> None:
        self.world = world
        self.people: list[Person] = []
        self._built = False
        self.messages: list[tuple[Message, int]] = []  # letters in the messenger's hand (due tick)

    # -- building -------------------------------------------------------------------

    def _build(self) -> None:
        if self._built:
            return
        self._built = True
        world = self.world
        ship = world.ship
        crew = (getattr(ship, "extra", None) or {}).get("crew")
        spec = getattr(getattr(ship, "spec", None), "crew", None)
        nav = getattr(world, "navigation", None)
        if crew is None:
            # a point ship, or one with no company: the captain alone, and the master of
            # the reckoning if there is one
            self.people.append(Person("captain", "the captain", "captain", 0.9))
            if nav is not None:
                self.people.append(
                    Person("master", nav.master.name, "master", nav.master.skill, mirror=nav.master)
                )
            return
        used: set[str] = set()
        for post, sailor in crew.posts.items():
            name = _address(post, sailor.name)
            person = Person(
                post.replace(" ", "_").replace("'", ""),
                name,
                post,
                float(sailor.skill_deck),
                sailor_id=sailor.id,
            )
            if post == "master" and nav is not None:
                person.mirror = nav.master
            used.add(sailor.id)
            self.people.append(person)
        # the roles beyond the posts, each drawn from his station in id order
        counts: dict[str, int] = {}
        for role_spec in spec.people if spec is not None else []:
            from freesail.crew.model import Rating, Station

            station = Station(role_spec.station)
            wanted = Rating(role_spec.rating) if role_spec.rating else None
            pool = [
                s
                for s in crew.by_station.get(station, [])
                if s.id not in used and (wanted is None or s.rating is wanted)
            ]
            if not pool:
                pool = [s for s in crew.by_station.get(station, []) if s.id not in used]
            if not pool:
                continue
            sailor = pool[0]
            used.add(sailor.id)
            n = counts.get(role_spec.role, 0) + 1
            counts[role_spec.role] = n
            pid = role_spec.role.replace(" ", "_").replace("'", "") + (f"_{n}" if n > 1 else "")
            self.people.append(
                Person(
                    pid,
                    _address(role_spec.role, sailor.name),
                    role_spec.role,
                    float(sailor.skill_deck),
                    messenger=role_spec.messenger,
                    sailor_id=sailor.id,
                )
            )
        # the watch each watch-keeper keeps, in turn
        turn = 0
        for p in self.people:
            if p.role in WATCH_KEEPERS:
                p.watch = ("starboard", "larboard")[turn % 2]
                turn += 1
        # the officers start on the quarterdeck, the standing officers and the idlers'
        # chiefs at their stations below or on deck (judgement: where their work is)
        for p in self.people:
            if p.role == "sailmaker":
                p.where = "sail_room"
            elif p.role in ("purser", "surgeon"):
                p.where = "gunroom"
            elif p.role in ("carpenter", "boatswain", "gunner", "master-at-arms"):
                p.where = "deck"
        self._scenario_people()

    def _scenario_people(self) -> None:
        """The scenario's `people:` (spec M5 §27; package 36): a person beyond the muster
        ({role, name, skill, place, ashore}), or, named by a role the muster fills with
        no name given, that man's skill and place set (a lunarian master: `{role: master,
        skill: 0.95}`; the master's skill is the reckoning's, through his mirror)."""
        world = self.world
        for spec in getattr(world.scenario, "people", None) or []:
            role = str(spec.get("role") or "").strip().lower()
            name = str(spec.get("name") or "").strip()
            if not role:
                continue
            found = None if name else next((p for p in self.people if p.role == role), None)
            if found is not None:
                if spec.get("skill") is not None:
                    found.skill = float(spec["skill"])
                    if found.mirror is not None:
                        found.mirror.skill = found.skill
                if spec.get("place"):
                    found.where = str(spec["place"]).replace(" ", "_")
                continue
            pid = (role + ("_" + name if name else "")).lower()
            pid = "".join(c if c.isalnum() else "_" for c in pid).strip("_")
            ashore = bool(spec.get("ashore")) or str(spec.get("place") or "") == "shore"
            self.people.append(
                Person(
                    pid,
                    name or _address(role, role),
                    role,
                    float(spec.get("skill", 0.7) or 0.7),
                    place="shore"
                    if ashore
                    else str(spec.get("place") or "cabin").replace(" ", "_"),
                    aboard=not ashore,
                    port=str(spec.get("port")) if spec.get("port") else None,
                )
            )

    # -- finding ------------------------------------------------------------------

    @property
    def all(self) -> list[Person]:
        self._build()
        return self.people

    @property
    def captain(self) -> Person:
        self._build()
        for p in self.people:
            if p.role in ("captain", "commander"):
                return p
        # a vessel whose master commands (the schooner, the cutter): the master is the captain
        for p in self.people:
            if p.role == "master":
                return p
        return self.people[0]

    @property
    def messenger(self) -> Person | None:
        self._build()
        for p in self.people:
            if p.messenger and p.aboard and not p.sick:
                return p
        return None

    def by_role(self, role: str) -> list[Person]:
        self._build()
        return [p for p in self.people if p.role == role]

    def find(self, words: str) -> Person | None:
        """A person by his role ('the master', 'the first lieutenant', 'the carpenter',
        'the pilot') or by his surname ('Mr Harvey', 'Harvey'); the captain by 'the
        captain' whoever commands. None when nobody answers to the words."""
        self._build()
        key = _words(words)
        if not key:
            return None
        if key in ("captain", "commander", "me", "myself"):
            return self.captain
        role = ROLE_WORDS.get(key)
        if role == "messenger":
            return self.messenger
        if role is not None:
            found = [p for p in self.people if p.role == role]
            if found:
                return found[0]
        # 'master' is a role before it is a surname; a surname after 'mr'
        key = key.removeprefix("mr ").removeprefix("mister ")
        for p in self.people:
            if _words(p.surname) == key or _words(p.name) == key:
                return p
        return None

    def add(self, person: Person) -> Person:
        self._build()
        self.people.append(person)
        return person

    def remove(self, person: Person) -> None:
        self._build()
        self.people = [p for p in self.people if p is not person]

    # -- states -----------------------------------------------------------------------

    def state_words(self, p: Person) -> str:
        """'on the quarterdeck', 'below, asleep', 'ashore', 'in the boat', 'sick', 'at the
        lunar, below'."""
        if not p.aboard and p.where in ("shore", "boat", "cutter"):
            return place_words(p.where)
        if p.sick:
            return "sick, in the sick berth"
        deck = self._at_the_station(p)
        if deck is True:
            return ON_DECK_WORDS
        if p.occupied:
            return f"at the {p.task}, {place_words(p.where)}"
        if p.pending is not None:
            return f"sent for, on his way to {PLACES[p.pending[0]].name}"
        if p.role == "pilot" and getattr(
            getattr(self.world, "ports", None), "pilot_boat_asked", False
        ):
            # package 37h: his charge done, he waits for his boat to put him off
            return "at the gangway, waiting for his boat"
        if deck is False:
            return OFF_WATCH_WORDS
        if self._asleep(p):
            return "below, asleep"
        return place_words(p.where)

    def _at_the_station(self, p: Person) -> bool | None:
        """Whether this is the man in whose place the officer of the watch stands, and
        the station has the deck (package 37g, item 10; in game 9 the readings had him
        "below, asleep" through 78 hours of deck): True while the station has the deck,
        False while it is seated without it, None for anyone else, and for him when
        nobody holds the station. The deck is the harness's to keep (`World.agents`);
        this reads it and changes nothing. The officer as a person who moves about the
        ship is Milestone 6's."""
        agents = getattr(self.world, "agents", None) or {}
        harness = agents.get("officer of the watch")
        if harness is None or harness.agent.released:
            return None
        if harness.station.person != p.name:
            return None
        return bool(harness.agent.deck)

    def _asleep(self, p: Person) -> bool:
        """A watch-keeper in his watch below at night is asleep (Luce 1884 ch. XX: the
        watch below turns in), unless an order has him elsewhere: at a task, sent for,
        in the boat or ashore; or the deck is his (package 37g)."""
        if p.watch is None or p is self.captain or not p.aboard or p.sick:
            return False
        if self._at_the_station(p) is True:
            return False
        if (
            p.occupied
            or p.pending is not None
            or p.where not in ("gunroom", "cabin", "quarterdeck")
        ):
            return False
        if not self._watch_below_at_night(p):
            p.up = False  # his watch on deck, or the day: the call is spent
            return False
        return not p.up

    def _watch_below_at_night(self, p: Person) -> bool:
        from freesail.crew import bill
        from freesail.crew.routine import is_night

        when = self.world.clock.ship_time
        return is_night(when) and bill.watch_on_duty(when).value != p.watch

    def effective_place(self, p: Person) -> str:
        """Where he is now: his place, or the gunroom when the bill has him asleep below."""
        return "gunroom" if self._asleep(p) else p.where

    def describe(self) -> list[str]:
        """`the people`: each by name and role with his state, the captain first."""
        self._build()
        out = []
        for p in self.people:
            role = "" if p.role in ("captain", "commander") else f", {p.role}"
            if p.role == "pilot" and p.port:
                # package 37h: the pilot of his port, a supernumerary aboard
                port = (getattr(getattr(self.world, "ports", None), "ports", None) or {}).get(
                    p.port
                )
                role += f" of {port.name}" if port is not None else ""
            out.append(f"{p.name}{role}: {self.state_words(p)}.")
        return out

    def where_is(self, words: str) -> dict[str, Any] | None:
        p = self.find(words)
        if p is None:
            return None
        return p.to_dict() | {
            "place": self.effective_place(p),
            "words": f"{p.name}, {self.state_words(p)}",
            "state": self.state_words(p),
        }

    # -- occupying and moving ----------------------------------------------------------

    def occupy(self, p: Person, place: str, until: int, with_what: str) -> str | None:
        """Occupy a person with a task until a tick; the refusal in words when he is busy."""
        if p.occupied:
            return f"{p.name} is at the {p.task}; he will be free at {self._when(p)}"
        if p.mirror is not None:
            p.mirror.occupy(
                "on deck" if place in ("quarterdeck", "deck") else "below", until, with_what
            )
        else:
            p.where = place
            p.occupied_until = until
            p.occupied_with = with_what
        return None

    def _when(self, p: Person) -> str:
        until = p.mirror.occupied_until if p.mirror is not None else p.occupied_until
        if until is None:
            return "once"
        clock = self.world.clock
        then = clock.ship_time + timedelta(seconds=until - clock.tick)
        return units.time_stamp(then)

    def free(self, p: Person) -> None:
        if p.mirror is None:
            p.occupied_until = None
            p.occupied_with = ""

    def send_for(self, words: str) -> tuple[str, dict[str, Any]]:
        """`send for the master`, `pass the word for the carpenter`: the messenger goes for
        him and he comes to where the captain is a minute later; refused in words when he
        is occupied, ashore, in the boat or sick, or when nobody answers to the words."""
        from freesail.orders.errors import OrderError

        p = self.find(words)
        if p is None:
            names = ", ".join(x.name for x in self.all)
            raise OrderError(f"Nobody aboard answers to '{words}'; the people are {names}.")
        captain = self.captain
        if p is captain:
            raise OrderError("You are the captain; there is no sending for yourself.")
        if not p.aboard:
            raise OrderError(f"{p.name} is {place_words(p.where)}; he cannot be sent for.")
        if p.sick:
            raise OrderError(f"{p.name} is sick in the sick berth; the surgeon has him.")
        if p.occupied:
            raise OrderError(
                f"{p.name} is at the {p.task} and will be free at {self._when(p)}; "
                "he is not to be called from it."
            )
        if p.pending is not None:
            raise OrderError(f"{p.name} is sent for already.")
        where = captain.where
        asleep = self._asleep(p)
        if p.where == where and not asleep:
            return (
                f"{p.name} is {place_words(where)} already.",
                {"person": p.to_dict(), "place": where},
            )
        messenger = self.messenger
        who = messenger.name if messenger is not None else "the sentry"
        due = self.world.clock.tick + PASS_THE_WORD_S
        was = self.state_words(p)
        line = (
            f"{p.name} came {_to_words(where)}, called from his watch below."
            if asleep
            else f"{p.name} came {_to_words(where)}, sent for."
        )
        p.pending = (where, due, line)
        p.up = True  # the order outranks the bill: he is not asleep again this watch
        text = f"Passed the word for {p.name} by {who}; he is {was}."
        return text, {"person": p.to_dict(), "place": where, "due_tick": due}

    def captain_moves(self, below: bool) -> tuple[str, dict[str, Any]]:
        """`go below` and `come on deck`: the captain between the cabin and the quarterdeck."""
        from freesail.orders.errors import OrderError

        captain = self.captain
        want = "cabin" if below else "quarterdeck"
        if captain.where == want:
            raise OrderError(f"You are {place_words(want)} already.")
        captain.where = want
        text = (
            "The captain went below to his cabin; the deck is the officer of the watch's."
            if below
            else "The captain came on deck."
        )
        return text, {"person": captain.to_dict(), "place": want}

    # -- messages -----------------------------------------------------------------------

    def message_aboard(self, message: Message) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """A letter come aboard by the boat or the pilot: the line of its coming, and the
        messenger takes it to the captain where he is (`tick` says the door and the
        reading, a minute later). The chain is the carrier, the gangway, the messenger,
        the door: every link a thing the ship models."""
        captain = self.captain
        due = self.world.clock.tick + PASS_THE_WORD_S
        self.messages.append((message, due))
        messenger = self.messenger
        who = messenger.name if messenger is not None else "the sentry"
        if messenger is not None:
            messenger.occupied_until = due
            messenger.occupied_with = "message"
        text = (
            f"A letter from {message.origin} came aboard by {message.carried_by}; "
            f"{who} took it aft for the captain, who is {place_words(captain.where)}."
        )
        return [
            (
                Severity.ROUTINE,
                "message.aboard",
                text,
                {"origin": message.origin, "carried_by": message.carried_by, "due_tick": due},
            )
        ]

    # -- the tick -----------------------------------------------------------------------

    def tick(self, now: int) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """Every tick: the people whose tasks are done freed, the moves in hand finished,
        and the letters in the messenger's hand delivered through the door."""
        if not self._built:
            return []
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        for p in self.people:
            if p.mirror is None and p.occupied_until is not None and now >= p.occupied_until:
                was = p.occupied_with
                p.occupied_until = None
                p.occupied_with = ""
                if was and was != "message":
                    lines.append(
                        (
                            Severity.ROUTINE,
                            "person.free",
                            f"{p.name} is done with the {was}.",
                            p.to_dict(),
                        )
                    )
            if p.pending is not None and now >= p.pending[1]:
                where, _, line = p.pending
                p.pending = None
                p.where = where
                lines.append((Severity.ROUTINE, "person.came", line, p.to_dict()))
        if self.messages:
            left = []
            for message, due in self.messages:
                if now < due:
                    left.append((message, due))
                    continue
                captain = self.captain
                messenger = self.messenger
                who = messenger.name if messenger is not None else "the sentry"
                if captain.where == "cabin":
                    door = f"{who} knocked at the cabin door with a letter from {message.origin}."
                else:
                    door = (
                        f"{who} brought a letter from {message.origin} to the captain "
                        f"{place_words(captain.where)}."
                    )
                lines.append(
                    (
                        Severity.ROUTINE,
                        "message.door",
                        door,
                        {"origin": message.origin, "place": captain.where},
                    )
                )
                lines.append(
                    (
                        Severity.NOTABLE,
                        "message.received",
                        f"The captain read it: {message.text}",
                        {"origin": message.origin, "text": message.text, "place": captain.where},
                    )
                )
            self.messages = left
        return lines


def _address(role: str, name: str) -> str:
    """How the log addresses a person: the captain by his rank, a warrant officer by his
    surname as the reckoning addresses the master, a boy by his name whole."""
    surname = name.split()[-1]
    if role in ("captain", "commander"):
        return f"Captain {surname}"
    if role in ("boy", "midshipman"):
        return f"Mr {surname}" if role == "midshipman" else name
    return f"Mr {surname}"


def _to_words(place: str) -> str:
    if place == "cabin":
        return "to the cabin"
    if place in ("quarterdeck", "deck"):
        return "aft"
    return f"to {PLACES[place].name}"


def _words(text: str) -> str:
    t = str(text).lower().replace("’", "'").replace("-", " ")
    t = "".join(c if c.isalnum() or c in " '" else " " for c in t)
    t = " ".join(t.split())
    for lead in ("for the ", "for ", "the "):
        if t.startswith(lead):
            t = t[len(lead) :]
    return t
