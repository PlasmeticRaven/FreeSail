"""The player's seat at a lesser station (package 40; spec M6 §3, the owner's ruling 1 of
2026-10-09: the player and a model are at parity for the roles on ships).

The player is always the owner at the door: whatever station he holds or none, the stop,
the deck's sentences, the grants, `stand down` and `resume`, the save and the clock are
his, and his words reach a station as the owner's. Beside that, the console and the
browser can seat him at a named station below the captain's, with that station's
authority: an order he types is judged as a model's at the station would be
(`agents.tools.judge`: the domain, the captain's named grants and his general authority,
the way out of danger), refused in the same words, and given under the station's actor
when it passes. He may so hold a lesser role under a model captain (`--station captain`
at a door; `--seat officer` at the console or the browser), or under the rules-based
captain when nobody holds the captain's station.

The seat is not a harness: there is no model behind it, no sampling, no patience and no
welfare (a player is not watched for his welfare by his own game), and it is not in
`world.agents`, which is the harnesses'. It lives on the World as `player_seat` and on the
ship as `extra["player_seat"]`, and the three places that look a station up fall back to
it: the orders' station sentences (`orders.stations`: `you have the deck`, `you may`,
`tell`, `ask`, `stand down`), the authority filter (`agents.tools`) and the readings (`the
officer of the watch`). The harness's own methods for the deck and the grants are borrowed
whole, so that the player's seat is given the deck and allowed things by the same rules
and with the same lines.

**A replay rebuilds the seat.** The seating is a driver's line in the inputs
(`SEAT_KIND`), after which the replay seats the player again before the orders that
follow it; his orders are journaled under the seat's actor (`SEAT_ACTOR_SUFFIX` after the
station's), which the World journals as it does the captain's own; a refusal is a driver's
line, so that the log reads the same again. A checkpoint carries the seat as it carries
the rest of the World.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from freesail.agents.agent import (
    OFFICER,
    RELEASED,
    SESSION_PLAY,
    STOOD_DOWN,
    AgentState,
    domain_of,
    door_words,
    officer,
)
from freesail.agents.harness import Harness
from freesail.agents.journal import Journal
from freesail.core.events import Severity
from freesail.orders.errors import OrderError

if TYPE_CHECKING:
    from freesail.core.events import Event
    from freesail.core.world import World

__all__ = [
    "SEAT_ACTOR_SUFFIX",
    "SEAT_KIND",
    "SEAT_STATIONS",
    "PlayerSeat",
    "seat_actor",
    "seat_of",
    "seat_player",
    "seat_words",
]

# The stations the player may be seated at from a driver's flag: those with authority
# below the captain's (the captain's is the player's own surface at the prompt, and the
# watcher's has no orders to judge). The flag's word, to the station's name.
SEAT_STATIONS: dict[str, str] = {"officer": OFFICER, OFFICER: OFFICER}

# The driver's line that seats the player (an input: a replay seats him again at it).
SEAT_KIND = "seat.taken"

# The seat's actor is the station's with this after it, so that the World journals the
# player's orders (a station's own actor is a harness's, whose replies are its transcript
# and are not journaled) and the log says whose they were.
SEAT_ACTOR_SUFFIX = " (the player)"


def seat_actor(station: str) -> str:
    return f"the {station}{SEAT_ACTOR_SUFFIX}"


def seat_words(station: str, door: str) -> str:
    """The seating said in one line, for the driver and the log."""
    return f"the player, through {door_words(door)}, at the {station}'s station"


def seat_of(world: Any, station: str) -> PlayerSeat | None:
    """The player's seat at a station, held (not released); None otherwise."""
    seat = getattr(world, "player_seat", None)
    if seat is None or seat.station.name != station or seat.agent.released:
        return None
    return seat


class PlayerSeat:
    """The player at a station with authority below the captain's. Quacks as a harness
    does where the game looks a station up (`agent`, `station`, `domain`, `journal`,
    `model_name`, `door`, `started`), and borrows the harness's deck and grants."""

    _deck_was: Any = None  # the harness's field the borrowed methods write

    def __init__(self, world: World, station: str = OFFICER, door: str = "console"):
        name = SEAT_STATIONS.get(" ".join(str(station).lower().split()))
        if name is None:
            raise OrderError(
                f"The player is not seated at the {station}: a seat is a station with "
                f"authority below the captain's ({', '.join(sorted(set(SEAT_STATIONS.values())))})."
            )
        held = world.agents.get(name)
        if held is not None and not held.agent.released:
            raise OrderError(
                f"The station of the {name} is {held.agent.words()}; the player is not "
                "seated where a model is."
            )
        old = getattr(world, "player_seat", None)
        if old is not None and not old.agent.released:
            raise OrderError(f"The player is seated already, at the {old.station.name}'s station.")
        self.world = world
        self.station = officer(world=world)  # the one seat there is; a list grows here
        self.agent = AgentState(self.station, session_kind=SESSION_PLAY)
        self.agent.stationed_tick = world.clock.tick
        self.agent.last_heard_tick = world.clock.tick
        self.journal: Journal = world.agent_journals.setdefault(name, Journal(name))
        self.model_name = "the player"
        self.door = str(door or "console")
        world.player_seat = self  # type: ignore[attr-defined]
        extra = getattr(world.ship, "extra", None)
        if isinstance(extra, dict):
            extra["player_seat"] = self
        self.note(f"Seated as {seat_words(name, self.door)}.", kind="agent.stationed")

    # -- what the game looks up on a station -----------------------------------------

    @property
    def actor(self) -> str:
        return self.station.title

    @property
    def order_actor(self) -> str:
        return seat_actor(self.station.name)

    @property
    def domain(self) -> Any:
        return domain_of(self.station)

    @property
    def started(self) -> bool:
        return True

    @property
    def who(self) -> str:
        return f"{self.model_name}, through {door_words(self.door)}"

    @property
    def _is_captains(self) -> bool:
        return False

    def _sync_captain(self) -> None:
        return None

    def note(self, text: str, kind: str = "note") -> Any:
        return self.journal.append(self.world, text, kind=kind, by=self.model_name)

    # the harness's deck and grants, whole (package 37g): the same rules, the same lines
    give_deck = Harness.give_deck
    take_deck = Harness.take_deck
    allow = Harness.allow
    disallow = Harness.disallow
    allow_general = Harness.allow_general
    disallow_general = Harness.disallow_general
    grants = Harness.grants
    granted_words = Harness.granted_words
    journal_words = Harness.journal_words

    # -- the captain's word to the seat ------------------------------------------------

    def put_word(self, words: str, by: str = "", officer: str = "the captain") -> str:
        """`tell the officer ...`: the words are the player's to read in the log; kept
        with what he was told, as the reading says them."""
        a = self.agent
        words = " ".join(str(words).split())
        if not words:
            raise OrderError(f"Tell the {self.station.name} what? Say the words after the name.")
        if a.released:
            raise OrderError(
                f"There is no {self.station.name} at the station now; {a.released_reason}."
            )
        a.told.append(words)
        self.note(f"Told by {by or officer}: {words}", kind="agent.told")
        if by:
            return f"By {by}: {officer} to the {self.station.name}: {words}"
        return f"The captain to the {self.station.name}: {words}"

    def put_question(self, question: str, by: str = "", officer: str = "the captain") -> str:
        """`ask the officer ...`: the question stands at the prompt until the player
        answers it ('answer <words>')."""
        a = self.agent
        question = " ".join(question.split()).rstrip("?")
        if not question:
            raise OrderError(f"Ask the {self.station.name} what? Say the question after the name.")
        if a.released:
            raise OrderError(
                f"There is no {self.station.name} at the station now; {a.released_reason}."
            )
        a.question = question
        self.note(f"Asked by {by or officer}: {question}?", kind="agent.asked")
        tail = " (the player answers at the prompt: 'answer <words>')"
        if by:
            return f"By {by}: {officer} asks the {self.station.name}: {question}?{tail}"
        return f"Asked the {self.station.name}: {question}?{tail}"

    def answer(self, text: str) -> Event:
        """The player's answer to a question put to his seat: a driver's line, so that a
        replay says it again."""
        text = " ".join(str(text).split())
        a = self.agent
        if not text:
            raise OrderError("Answer what? Say the words after 'answer'.")
        asked = a.question
        head = f"The {self.station.name} answers"
        words = f"{head} ({asked}?): {text}" if asked else f"{head}: {text}"
        return self._driver_line(
            "agent.answered",
            words,
            {"station": self.station.name, "text": text, "question": asked or ""},
        )

    def _driver_line(self, kind: str, words: str, data: dict[str, Any]) -> Event:
        """A line of the seat's that is an input (a refusal, an answer): recorded as the
        driver's, so that a replay writes it again, and applied to the seat as the replay
        applies it (`replayed`)."""
        e = self.world.record_driver(Severity.ROUTINE, kind, words, data={**data, "seat": True})
        self.replayed(kind, words, data)
        return e

    def replayed(self, kind: str, words: str, data: dict[str, Any]) -> None:
        """What a driver's line of the seat's does to it beside the log: the journal's
        note, and a question answered. Called when the line is made and when a replay
        writes it again (`core.replay`), so that the seat is the same either way."""
        if kind == "agent.answered":
            self.agent.question = None
            self.note(words, kind=kind)
        elif kind == "agent.refused":
            self.note(f"Refused: {words}", kind=kind)

    # -- leaving -----------------------------------------------------------------------

    def request_stand_down(self, reason: str, by: str = "the captain") -> str:
        """`stand down the officer`: the seat is released now (there is no turn to end),
        and the station may be taken again, by the player or by a model's door."""
        a = self.agent
        if a.released:
            raise OrderError(
                f"The {self.station.name}'s station is released already; {a.released_reason}."
            )
        a.state = RELEASED
        a.left_by = STOOD_DOWN
        a.released_reason = f"stood down by {by}: {reason}"
        a.released_tick = self.world.clock.tick
        a.question = None
        a.deck, a.deck_tick, a.deck_stamp = False, None, ""
        a.deck_lost, self._deck_was = "", None
        a.grants, a.allowances = (), {}
        a.general, a.general_words = False, ""
        self.note(f"Stood down by {by}: {reason}.", kind="agent.stopped")
        extra = getattr(self.world.ship, "extra", None)
        if isinstance(extra, dict):
            extra.pop("player_seat", None)
        return (
            f"The player's seat at the {self.station.name}'s station is stood down by {by}; "
            "the station is released and may be taken again. The deck is the captain's."
        )

    def resume(self, by: str = "the captain") -> str:
        raise OrderError(
            f"The player's seat at the {self.station.name}'s station is not paused; there "
            "is nothing to resume."
        )

    # -- the player's line -------------------------------------------------------------

    def route(self, text: str) -> Event:
        """A line typed at the prompt while the player is seated: the owner's where it is
        his (the stations' sentences, a world order, 'answer ...'), the seat's otherwise,
        judged by the station's authority."""
        from freesail.orders import stations
        from freesail.world import orders as world_orders

        line = " ".join(str(text).split())
        low = line.lower()
        if low.startswith("answer ") or low == "answer":
            return self.answer(line[len("answer") :])
        if self.agent.released or world_orders.recognises(line):
            return self.world.submit(line)
        if stations.recognises(line, self.world.ship) is not None:
            return self.world.submit(line)
        return self.submit(line)

    def submit(self, text: str, danger: str = "") -> Event:
        """An order of the player's at his seat, judged as a model's at the station would
        be and given under the seat's actor, so that the ship and the log read it as the
        station's (`whose_order`), and the World journals it."""
        from freesail.agents import tools

        text = " ".join(str(text).split())
        a = self.agent
        st = self.station
        if a.released:
            return self.world.submit(text)
        if not a.deck:
            why = (
                f"The {st.name} has not the deck ({a.deck_lost or 'the captain has it'}); an "
                f"order waits for 'you have the deck'. {text!r} not carried out."
            )
            return self._refused(text, why)
        text, why, _how = tools.judge(self.world, st.name, text, danger)
        if why:
            return self._refused(text, f"{why} {text!r} not carried out.")
        return self.world.submit(text, actor=self.order_actor)

    def _refused(self, text: str, why: str) -> Event:
        data = {"order": text, "station": self.station.name}
        return self._driver_line("agent.refused", why, data)


def seat_player(
    world: World, station: str = OFFICER, door: str = "console", quiet: bool = False
) -> PlayerSeat:
    """Seat the player at a station from a driver (`--seat officer`): the driver's line
    that says so, then the seat; a replay that reaches the line seats him again
    (`core.replay`, `quiet`). The seat that stands at the station already is returned as
    it is."""
    name = SEAT_STATIONS.get(" ".join(str(station).lower().split()), station)
    old = seat_of(world, name)
    if old is not None:
        return old
    words = (
        f"The player takes the {name}'s station ({seat_words(name, door)}); his orders are "
        "judged by the station's authority and the captain's word, and the deck is the "
        "captain's until he gives it."
    )
    if not quiet:
        world.record_driver(
            Severity.NOTABLE, SEAT_KIND, words, data={"station": name, "door": str(door)}
        )
    return PlayerSeat(world, name, door)
