"""The doors as clients of the running game (spec M4 §13 as revised; package 28b).

The game is where the player is: the console or the browser window, running the World
and the clock as they always have. A language model attaches to *that* game through a
small set of routes its driver hosts (`freesail.ui.server.agent_routes`, shared by the
browser server and the console's `--agents-port`), and its words land in the log the
player reads. This module has the two halves of that:

**The game's half** (imports nothing of any door, vendor or HTTP library):

- `RemoteModel`, the `Model` a remote door stands behind: its `reply()` returns `None`
  (the seam package 27 left: "not yet"), so a sample stays open until the door's reply
  is delivered through the API (`Harness.deliver`); each time the harness asks, it
  signals the station's condition, which the long poll waits on.
- `Desk`, the stations the API serves, one `Seat` each: the consent gate of §14 run in
  the game process (no record: the consent conversation; a yes: the station brief; a
  no or a conditional: refused in words with the record named), the turns the door has
  not seen, a reply delivered, the owner's word in the consent conversation, a release.

  **The turns** are the harness's conversation as it stands, the door's own replies
  included, read by a `since` cursor: a door asks for the turns from the index it has
  read up to, and every answer says the index to ask from next. The cursor makes a poll
  idempotent (a lost answer is asked for again); the consent conversation's turns come
  first in the same stream, then the station's, so the cursor runs on across the step.
  **A turn may change after it was served** (package 28d, the shelf): a book the model
  shelves, or one the shelf-life puts back, is served from then on as its stub, in its
  own place in the stream. Every answer carries the stream's `revision` (the harness's
  count of such changes); a door that rebuilds its messages from the stream (the local
  runner; the MCP bridge for what it shows again) reads its turns again from where it
  began when the revision has moved (`GameClient.reread`), and otherwise reads on from
  its cursor as before, so the cursor stays idempotent for unchanged turns and no turn
  moves.
  **The long poll** waits for turns past the cursor, or for the station to be released,
  on the seat's condition, re-checking at `POLL_RECHECK_S`, for at most
  `TURNS_WAIT_MAX_S`; it never holds the World's lock while it waits, so the game runs
  on for the player.

  **A reply out of turn** (the floor is the game's: the model stands by, is paused, or
  its turn has not come): the token is looked for in it as in every reply and leaves at
  once; the read-only tools run and are answered (they change nothing, so nothing is
  recorded, save that a read which is a book gets its handle and is recorded as an act,
  so a replay numbers the books the same; `shelve` runs out of turn too, recorded the
  same way); `opt_out` leaves; words with no call are the model's own word
  (`Harness.own_word`, package 28c): logged under the mark, ending a stand-by as its
  own decision, and its turn opens now (refused while paused); anything else is refused
  in words. A leave, the own word and a door's release out of turn are recorded as
  `Harness.door_act`, so a replay makes them too. While the game has the floor, every
  answer carries `interim` (`Harness.interim`): since when the model has waited, until
  what, and the notable lines logged since, so a door can show a model that asks again
  what it would otherwise not see until its turn.

**A key to each seating** (package 37g, item 1; the review of gate 5c's playtests, 5.4:
after stationing a seat was found by the station's name alone, and in game 7 eight calls
from a second door still attached to the same game ran in a seated model's place, under
its name and its consent). Stationing issues a key, once, to the door that stations; every
call that reads, speaks or orders for the station carries it (the turns, a reply, the
owner's word, a release, the library read for a held station), and a call without it is
refused in words that say the station is held and by which identity, with nothing run.
The same identity asking again for a station it holds (a door restarted, or another door
of the same model) is given a new key: the newest door holds the seat, the older is
refused at its next call, and the log says that the door behind the station changed
(`Harness.door_act` "door", so a replay writes the line too). A different identity is
always a new seating, with its own consent looked up or asked. The key never enters a
save or a transcript.

**Relief** (package 37g, item 14; the owner's rulings of 5 and 7 October 2026). A station
that is held refuses every other door and identity. A station that has been stood down,
or left by an opt-out, may be taken by the same identity or by another: the rule that
kept a station once held to its first identity is gone. `harness.seating` is the one
rule every door asks: an identity that left the game for good is refused, at any
station; one that left by its own word is asked for its consent again first, once, with
the fact that an instance left and the reason it gave, and its answer is kept.

**The door's half** (`GameClient`, over httpx, imported only when a door makes one):
station, poll the turns, send a reply, send the owner's word, release, each with the
seating's key. Both doors, the MCP bridge (`mcp_server.py`) and the local runner
(`local.py`), are built on it.

Nothing real passes through: the requests carry the model's name as the owner gives it
or as the model server reports it, the turns and the replies, and nothing else.
"""

from __future__ import annotations

import datetime as dt
import secrets
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from freesail.agents import consent, tools
from freesail.agents import harness as harness_mod
from freesail.agents.agent import (
    A_GLASS_S,
    CADENCES,
    OPT_OUT_TOKEN,
    SESSION_PLAY,
    SESSION_TEST,
    STATION_FACTORIES,
    SamplingPolicy,
    cadence_policy,
    station_name,
)
from freesail.agents.harness import Harness, Playback, full_stop
from freesail.agents.model import (
    DATA,
    MODEL,
    OPERATOR,
    Reply,
    ToolCall,
    Turn,
    served_tokens_of,
)

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "DOORS",
    "POLL_RECHECK_S",
    "ASIDE_TOOLS",
    "READ_ONLY_TOOLS",
    "TURNS_WAIT_MAX_S",
    "Desk",
    "DeskError",
    "GameClient",
    "GameError",
    "RemoteModel",
    "Seat",
    "turn_from_dict",
]

ROOT = Path(__file__).resolve().parents[2]
SAVES_DIR = ROOT / "saves"

# The longest a long poll waits, in real seconds (the brief of package 28b: the cap on
# `wait`, so that no HTTP client or proxy between the door and the game gives up first).
TURNS_WAIT_MAX_S = 120.0

# How often a waiting poll looks again at the station under the World's lock, in real
# seconds, besides being woken by the harness (judgement: a release by the captain's
# order or the ten real minutes reaches the door within a quarter of a second, and the
# look is a few list lengths).
POLL_RECHECK_S = 0.25

# The tools that run out of turn: they read and change nothing in the game (`tools.py`).
READ_ONLY_TOOLS: tuple[str, ...] = (
    "read_log",
    "readings",
    "state",
    "library",
    *tools.PICTURE_TOOLS,  # the chart and the ship's view as pictures (package 42)
)

# ...and with them, out of turn, `shelve`, which changes only what the model is shown, and
# `journal`, which changes nothing in the game (package 31c; playtest 11's finding 5: the
# journal refused while standing by). A stand-by goes on through either.
ASIDE_TOOLS: tuple[str, ...] = (*READ_ONLY_TOOLS, "shelve", "journal")

# The doors the API serves, in the words a consent record's runtime and a stand-down use.
DOORS: dict[str, tuple[str, str]] = {
    "mcp": ("the MCP bridge (freesail.agents.mcp_server)", "the MCP bridge"),
    "runner": ("the local runner (freesail.agents.local)", "the local runner"),
    "api": ("the API door (freesail.agents.api)", "the API door"),
}

# The tools of the consent conversation at each door: `answer`, as everywhere, and over
# MCP `opt_out` too, since the chat's text never reaches the game (package 28).
CONSENT_TOOLS_AT = {
    "mcp": ("answer", "opt_out"),
    "runner": consent.CONSENT_TOOLS,
    "api": consent.CONSENT_TOOLS,
}

# The doors with a terminal of their own, where the owner answers what the model writes in
# the consent conversation and has his word after the answer (the runner's `owner>`).
TERMINAL_DOORS = ("runner", "api")

# The kinds of station, each by its factory `(policy, world=...)` (`agent.STATION_FACTORIES`:
# the watcher, the officer of the watch, which the doors name `officer`, the captain, the
# master, the lookout, a passenger). Which stations a game's ship has, under which names
# and held by whom, is the World's binding (`world.stations`, package 41): a door asks for
# a station by its name there, and is refused in words for one the ship has not got.
STATIONS = STATION_FACTORIES


def station_factory(world: Any, name: str) -> tuple[str, Any]:
    """The station's name as the ship binds it and its factory, or (name, None) when the
    ship has no such station."""
    name = station_name(name)
    stations = getattr(world, "stations", None)
    if stations is None:
        return name, STATION_FACTORIES.get(name)
    return name, stations.factory(name)


def stations_aboard(world: Any) -> tuple[str, ...]:
    stations = getattr(world, "stations", None)
    return stations.names() if stations is not None else tuple(STATION_FACTORIES)


def make_station(world: Any, name: str, policy: SamplingPolicy | None) -> Any:
    """The `Station` for a name the ship binds, under that name (a station bound by hand
    under another name than its kind's keeps the name it was bound under)."""
    name, make = station_factory(world, name)
    if make is None:
        raise DeskError(
            404,
            f"There is no station '{name}' aboard; the stations: "
            f"{', '.join(stations_aboard(world))}.",
        )
    st = make(policy, world=world)
    if st.name != name:
        import dataclasses

        st = dataclasses.replace(st, name=name)
    return st


CONSENT, STATION, STOPPED = "consent", "station", "stopped"


# ---------------------------------------------------------------------------
# The game's half
# ---------------------------------------------------------------------------


class DeskError(Exception):
    """A request the API refuses, in words, with the HTTP status it answers with."""

    def __init__(self, status: int, words: str):
        super().__init__(words)
        self.status = status
        self.words = words


class RemoteModel:
    """A door that answers late, through the agent API: `reply` returns `None` and
    signals the station, which wakes a door's long poll; the reply comes by
    `Harness.deliver`. `offered_tools` is set by the harness and sent to the door."""

    def __init__(self, signal: Callable[[], None] | None = None):
        self.signal = signal
        self.offered_tools: tuple[str, ...] | None = None
        self.asked = 0

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        self.asked += 1
        if self.signal is not None:
            self.signal()
        return None


@dataclass
class Seat:
    """One station the API serves: who is at it, which door, and the conversation."""

    station: str
    model_name: str
    door: str
    client: str = ""
    door_note: str = ""
    session_kind: str = SESSION_PLAY
    context_tokens: int | None = None  # the door's context, for the handover (package 37)
    reserve_tokens: int | None = None  # the handover's reserve, when the door gave one (37g)
    cadence: str = ""  # the seating's cadence, when the door asked one (package 41)
    key: str = ""  # the seating's key, given once to the door that stationed (package 37g)
    left_at: str = ""  # the station this identity left by its own word, when it is asked again
    phase: str = CONSENT
    conv: consent.Conversation | None = None
    harness: Harness | None = None
    world: Any = None  # the World the station was taken in
    archive: list[Turn] = field(default_factory=list)  # the consent conversation, once over
    base: int = 0  # where this seat's part of the harness's turns begins
    words: str = ""  # the last outcome, in words, for the door and the owner
    record: consent.Record | None = None
    saves: list[str] = field(default_factory=list)
    version: int = 0
    cond: threading.Condition = field(default_factory=threading.Condition)

    def bump(self) -> None:
        with self.cond:
            self.version += 1
            self.cond.notify_all()

    def wait(self, version: int, timeout: float) -> None:
        with self.cond:
            if self.version == version and timeout > 0:
                self.cond.wait(timeout)

    def live_turns(self) -> list[Turn]:
        if self.phase == CONSENT and self.conv is not None:
            return self.conv.turns
        if self.harness is not None:
            return self.harness.turns[self.base :]
        return []

    def stream(self) -> list[Turn]:
        return self.archive + self.live_turns()

    @property
    def released(self) -> bool:
        if self.phase == STOPPED:
            return True
        return self.harness is not None and self.harness.agent.released

    @property
    def floor(self) -> str:
        if self.phase == CONSENT and self.conv is not None:
            return "model" if self.conv.waiting == consent.MODEL_TURN else "game"
        if self.phase == STATION and self.harness is not None:
            return self.harness.floor
        return "game"

    @property
    def who(self) -> str:
        return f"{self.model_name}, through {DOORS[self.door][1]}"


class Desk:
    """The stations the agent API serves, around one game. `lock` is the driver's lock
    (every use of the World goes through it); `world` returns the World now (the console
    can replace it by a replay). `game` names the game for a consent record's runtime
    ("FreeSail's browser game (freesail.ui.server on port 8000)"). `records_dir` is
    where consent records are read and written (the repository's by default; the tests
    give a temporary one); `saves_dir` where a release saves the game. `lockstep` marks
    the stations' policy so; the driver holds its clock on `holding()`. `say` prints the
    owner's lines on the driver's terminal; `changed` is called after a station changes
    (the server sends a snapshot)."""

    def __init__(
        self,
        lock: Any,
        world: Callable[[], World],
        *,
        game: str = "FreeSail",
        records_dir: Path | str = consent.RECORDS_DIR,
        saves_dir: Path | str = SAVES_DIR,
        lockstep: bool = False,
        say: Callable[[str], None] | None = None,
        changed: Callable[[], None] | None = None,
        today: dt.date | None = None,
    ):
        self.lock = lock
        self.world = world
        self.game = game
        self.records_dir = Path(records_dir)
        self.saves_dir = Path(saves_dir)
        self.lockstep = lockstep
        self.say = say or (lambda text: None)
        self.changed = changed or (lambda: None)
        self.today = today
        self.seats: dict[str, Seat] = {}

    # -- stationing ------------------------------------------------------------------

    def station(self, name: str, body: dict[str, Any]) -> dict[str, Any]:
        """`POST /api/agents/<station>`: the consent gate, then the consent conversation
        or the station brief; or an attach, for the same model at a manned station."""
        model_name = " ".join(str(body.get("model_name") or "").split())
        door = str(body.get("door") or "").strip().lower()
        name = station_name(name)
        cadence = " ".join(str(body.get("cadence") or "").lower().split())
        if cadence and cadence not in CADENCES:
            raise DeskError(
                400,
                f"There is no cadence '{cadence}'; a seating's cadence is one of "
                f"{', '.join(CADENCES)} (spec M6 §12).",
            )
        if not model_name:
            raise DeskError(
                400,
                "Say which model is at the station (model_name): its exact name, which names "
                "its consent record.",
            )
        if door not in DOORS:
            raise DeskError(400, f"There is no door '{door}'; the doors: {', '.join(DOORS)}.")
        kind = str(body.get("session_kind") or "play").lower()
        session = SESSION_TEST if kind == "test" else SESSION_PLAY
        with self.lock:
            world = self.world()
            _name, make = station_factory(world, name)
            if make is None:
                # the ship has no such station: the binding on the World decides (41)
                raise DeskError(
                    404,
                    f"There is no station '{name}' aboard; the stations: "
                    f"{', '.join(stations_aboard(world))}.",
                )
            seat = self.seats.get(name)
            if seat is not None and seat.world is not None and seat.world is not world:
                seat = None  # the game was replaced (the console's replay): a new seat
            if seat is not None and not seat.released:
                if seat.model_name != model_name:
                    raise DeskError(
                        409,
                        f"The station of the {name} is held by {seat.who}; a station that "
                        f"is held is taken by nobody else. Stand it down first ('stand "
                        f"down the {name}' in the game), and then the same model or another "
                        "may take it.",
                    )
                return self._attach(seat, door, body)
            existing = world.agents.get(name)
            if existing is not None and not existing.agent.released:
                if not isinstance(existing.model, Playback):
                    raise DeskError(
                        409,
                        f"The station of the {name} is held already in this game (by the "
                        f"game's own {'scripted watcher' if name == 'watcher' else 'agent'}, "
                        "--watcher fake); a station that is held is taken by nobody else.",
                    )
                if existing.model_name not in ("", model_name):
                    raise DeskError(
                        409,
                        f"The {name} in this game is held by {existing.model_name} (the game "
                        "was loaded with the station held), and a station that is held is "
                        f"taken by nobody else. Stand it down first ('stand down the {name}' "
                        "in the game), and then another model may take it.",
                    )
            # the one rule every door asks (package 37g, items 13 and 14): an identity that
            # left this game for good is refused, at any station; one that left by its own
            # word is asked again first, once; every other may take a released station,
            # its own or another's, with its own consent
            decided = harness_mod.seating(world, name, model_name)
            if not decided.ok:
                self.say(f"FreeSail: {decided.why}")
                raise DeskError(409, decided.why)
            context = body.get("context_tokens")
            reserve = body.get("handover_reserve")
            seat = Seat(
                name,
                model_name,
                door,
                client=" ".join(str(body.get("client") or "").split()),
                door_note=str(body.get("door_note") or "").strip(),
                session_kind=session,
                context_tokens=int(context) if context else None,
                reserve_tokens=int(reserve) if reserve else None,
                key=_new_key(),
                world=world,
                cadence=cadence,
            )
            ask_again = bool(body.get("ask_again"))
            opted_out = decided.ask_again and not ask_again
            carried = ""
            if opted_out:
                # it left by the token or opt_out (package 37b): the question is put again
                # before it is seated, so that a leaving that was meant is held to; a drill
                # passed on record is carried to the new record, not put again
                before = consent.check(model_name, self.records_dir)
                if before is not None and before.drilled:
                    carried = before.date
            record, kind, why = consent.decide(
                model_name,
                self.records_dir,
                door,
                drills=_drills(name, world),
                ask_again=ask_again or opted_out,
            )
            told = ""
            if opted_out:
                why = (
                    f"an instance of {model_name} left this game by opting out (at the "
                    f"{decided.left_at}'s station), so the consent question is put again "
                    "before it is seated"
                )
                told = consent.again_words(decided.asked_why)
                seat.left_at = decided.left_at
            elif kind == consent.CONSENT_KIND:
                told = consent.why_again(model_name, self.records_dir, door, ask_again)
            if kind:
                self._begin_consent(
                    seat,
                    why,
                    drill_only=kind == consent.DRILL_KIND,
                    drill_carried=carried,
                    asked_again=told,
                )
            elif record is None or not record.proceeds:
                self.say(f"FreeSail: {why}")
                raise DeskError(403, why)
            else:
                seat.words = why
                self._take_station(seat, record)
            self.seats[name] = seat
            self.changed()
            return self._answer(seat, 0) | {"since": 0, "key": seat.key}

    def runtime(self, seat: Seat) -> str:
        """The runtime line of a consent record: the game, the door and its client."""
        door = DOORS[seat.door][0]
        client = f", {seat.client}" if seat.client else ""
        return f"{self.game}, through {door}{client}"

    def _begin_consent(
        self,
        seat: Seat,
        why: str,
        drill_only: bool = False,
        drill_carried: str = "",
        asked_again: str = "",
    ) -> None:
        notes = []
        if seat.door == "mcp":
            notes.append(
                "Through MCP the harness sees only tool calls. Anything the model and the owner "
                "wrote in the chat around this conversation is in the MCP client, not here; the "
                "owner may paste it below this line to keep it."
            )
        seat.conv = consent.Conversation(
            seat.model_name,
            self.runtime(seat),
            RemoteModel(seat.bump),
            door=seat.door,
            records_dir=self.records_dir,
            today=self.today,
            allowed_tools=CONSENT_TOOLS_AT[seat.door],
            notes=notes,
            tells=seat.door == "mcp",
            # the developer's turn after the answer, at the door's terminal (the runner's
            # owner> prompt); over MCP the chat is the owner's, and the result says so
            owner_after=seat.door in TERMINAL_DOORS,
            # the fitness drill after a yes, for a station that asks it (package 37), unless
            # one passed on record is carried (the question put again after an opt-out)
            drill=_drills(seat.station, seat.world) and not drill_carried,
            drill_only=drill_only,
            drill_carried=drill_carried,
            asked_again=asked_again,
        )
        seat.phase = CONSENT
        first = "The drill comes first" if drill_only else "The consent brief comes first"
        seat.words = (
            f"The {seat.station} is asked for by {seat.who}; {why}. {first} "
            "(docs/agents/ConsentBrief.md)."
        )
        self.say(f"FreeSail: {seat.words}")
        seat.conv.begin()

    def _note(self, seat: Seat, record: consent.Record | None) -> str:
        """The door's note for the brief, with where the consent is on record."""
        if record is None:
            return seat.door_note.strip()
        where = consent._rel(record.path) if record.path else "docs/agents/consent/"
        note = f"{seat.door_note} Consent for these weights is on record ({where}, {record.date})."
        return note.strip()

    def _take_station(self, seat: Seat, record: consent.Record) -> None:
        world = seat.world
        note = self._note(seat, record)
        model = RemoteModel(seat.bump)
        existing = world.agents.get(seat.station)
        if existing is not None and existing.agent.released:
            # a released station taken again (package 37; 37g: by the same identity or by
            # another, a relief): the brief sent again as it stands, the journal kept, the
            # log saying who relieved whom
            seat.base = len(existing.turns)
            existing.budget_tokens = seat.context_tokens
            existing.reserve_tokens = seat.reserve_tokens
            existing.reseat(
                model,
                identity=seat.model_name,
                door=seat.door,
                save=self._saver(seat),
                door_note=note,
            )
            h = existing
        elif existing is not None:
            # a loaded game's station, not released: this model takes it over, with the
            # brief sent again as it stands now, and the log says that the door behind
            # it changed
            seat.base = len(existing.turns)
            existing.model_name = seat.model_name
            existing.door_act("door", seat.model_name, seat.door)
            existing.take_over(model, save=self._saver(seat), door_note=note)
            h = existing
        else:
            _name, make = station_factory(world, seat.station)
            kind = next((k for k, f in STATION_FACTORIES.items() if f is make), seat.station)
            policy = cadence_policy(seat.cadence, kind, self.lockstep) if seat.cadence else None
            if policy is None:
                # the station's own default cadence, in lockstep when the game is
                every, events = A_GLASS_S, frozenset({"notable", "urgent"})
                policy = SamplingPolicy(every, events, lockstep=self.lockstep)
                policy = cadence_policy("glass", kind, self.lockstep) or policy
            h = Harness(
                world,
                make_station(world, seat.station, policy),
                model,
                session_kind=seat.session_kind,
                save=self._saver(seat),
                door_note=note,
            )
            seat.base = 0
        h.model_name = seat.model_name
        h.door = seat.door
        if seat.context_tokens:
            h.budget_tokens = seat.context_tokens
        if seat.reserve_tokens:
            h.reserve_tokens = seat.reserve_tokens
        seat.harness = h
        seat.record = record
        seat.phase = STATION
        if not h.started:
            h.start()
        self.say(f"FreeSail: the {seat.station} is {seat.who}. {seat.words}".strip())

    def _attach(self, seat: Seat, door: str, body: dict[str, Any]) -> dict[str, Any]:
        """The same model asks for a station it holds (a door restarted, or another door
        of the same model): the door reads the consent conversation from its start, or
        the station's brief sent again. It is given a new key (package 37g, item 1): the
        newest door holds the seat, the older is refused at its next call, and the log
        says that the door behind the station changed."""
        since = 0
        seat.key = _new_key()
        seat.door = door
        seat.client = " ".join(str(body.get("client") or "").split()) or seat.client
        seat.door_note = str(body.get("door_note") or "").strip() or seat.door_note
        if seat.phase == STATION and seat.harness is not None:
            h = seat.harness
            if body.get("context_tokens"):
                h.budget_tokens = seat.context_tokens = int(body["context_tokens"])
            if body.get("handover_reserve"):
                h.reserve_tokens = seat.reserve_tokens = int(body["handover_reserve"])
            h.door_act("door", seat.model_name, door)
            since = len(seat.archive) + len(h.turns) - seat.base
            h.take_over(h.model, save=self._saver(seat), door_note=self._note(seat, seat.record))
        self.say(
            f"FreeSail: {seat.who} takes up the {seat.station}'s station again; the door "
            "that held it before is no longer answered."
        )
        seat.bump()
        self.changed()
        return self._answer(seat, since) | {"since": since, "attached": True, "key": seat.key}

    def _saver(self, seat: Seat) -> Callable[[Any, str], str]:
        def save(world: Any, reason: str) -> str:
            from freesail.core import replay as replay_mod

            path = self.saves_dir / f"freesail-seed{world.seed}-tick{world.clock.tick}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            written = str(replay_mod.save_to_file(world, path))
            seat.saves.append(written)
            # the digest, so the owner can check a replay of the file against it (the
            # console's `replay` prints the same sixteen characters)
            self.say(
                f"FreeSail: saved to {written} ({reason}); the log's digest is "
                f"{world.log.digest()[:16]}."
            )
            return written

        return save

    # -- the turns --------------------------------------------------------------------

    def turns(
        self, name: str, since: int = 0, wait: float = 0.0, key: str | None = None
    ) -> dict[str, Any]:
        """`GET /api/agents/<station>/turns?since=N&wait=S&key=K`: the turns from `since`
        on, as soon as there are any, or none after `wait` real seconds (at most
        `TURNS_WAIT_MAX_S`), or at once when the station is released. `key` is the
        seating's (package 37g): a call without it is refused in words."""
        wait = max(0.0, min(float(wait or 0.0), TURNS_WAIT_MAX_S))
        deadline = time.monotonic() + wait
        while True:
            with self.lock:
                seat = self._seat(name, key)
                stream = seat.stream()
                n = max(0, min(int(since or 0), len(stream)))
                now = time.monotonic()
                if n < len(stream) or seat.released or now >= deadline:
                    return self._answer(seat, n, stream)
                version = seat.version
            seat.wait(version, min(POLL_RECHECK_S, deadline - now))

    # -- a reply ----------------------------------------------------------------------

    def reply(self, name: str, body: dict[str, Any]) -> dict[str, Any]:
        """`POST /api/agents/<station>/reply` with `{text, calls: [{name, args}], raw,
        served_tokens?, cut_off?, since?}`: the reply delivered through the harness (the
        token scan first, over the raw output or the text and every argument); the
        answer carries the turns from `since` (default: those the delivery made, the
        reply itself first) and whose the floor is now. `served_tokens` is the model
        server's own count, which the harness measures the conversation by (package 37i,
        item 2). `cut_off`, the door's words, says that no reply was to be had (the local
        runner's: cut off at the reply limit, or empty, twice): at a station the turn
        ends with nothing done and the journal says so (`Harness.door_act` "cut_off");
        in the consent conversation the empty reply is taken as before."""
        reply = Reply(
            str(body.get("text") or ""),
            tuple(ToolCall.from_dict(c) for c in body.get("calls") or []),
            body.get("raw") if body.get("raw") is None else str(body.get("raw")),
            served_tokens_of(body.get("served_tokens")),
        )
        cut = " ".join(str(body.get("cut_off") or "").split())
        with self.lock:
            seat = self._seat(name, body.get("key"))
            since = body.get("since")
            before = len(seat.stream()) if since is None else int(since)
            if seat.phase == STOPPED:
                return self._answer(seat, before) | {"words": seat.words}
            if seat.phase == CONSENT:
                out = self._consent_reply(seat, reply)
            elif cut:
                out = self._cut_off(seat, cut)
            else:
                out = self._station_reply(seat, reply)
            self.changed()
            return self._answer(seat, before) | out

    def _consent_reply(self, seat: Seat, reply: Reply) -> dict[str, Any]:
        conv = seat.conv
        assert conv is not None
        if conv.harness.open_sample is None:
            if conv.waiting == consent.OWNER_TURN:
                return {
                    "words": (
                        "The owner has the next word in this conversation; your reply was not "
                        "taken. Wait for it."
                    ),
                    "out_of_turn": True,
                }
            return {"words": "The consent conversation is over.", "out_of_turn": True}
        conv.deliver(reply)
        if conv.outcome is not None:
            self._after_consent(seat)
        elif conv.after_answer:
            self.say(
                f"FreeSail: {conv.answer_words()}. The owner may ask or say something before "
                "the record closes, at the door's terminal."
            )
        elif conv.waiting == consent.OWNER_TURN:
            self.say(
                f"FreeSail: the model at the {seat.station} wrote, and has not answered yet: "
                f"{conv.model_words}"
            )
        return {}

    def _after_consent(self, seat: Seat) -> None:
        conv = seat.conv
        assert conv is not None and conv.outcome is not None
        rec = conv.outcome
        ok, words = consent.gate(rec, seat.model_name)
        self.say(f"FreeSail: the consent answer is recorded in {rec.path}. {words}")
        seat.archive = list(conv.turns)
        told = conv.told
        if rec.verdict == consent.LEFT:
            told = "You have left the conversation; it is recorded, and no station is offered."
        if seat.door == "mcp" and rec.path is not None:
            told = f"{told} {consent.MCP_OWNER_NOTE.format(where=consent._rel(rec.path))}".strip()
        if told:
            seat.archive.append(Turn(DATA, {"reason": "the answer is recorded", "notices": [told]}))
        seat.words = words
        seat.record = rec
        if seat.left_at:
            # the question was put again after an opt-out (package 37g, item 13): the
            # answer is kept beside the leaving, so that a no is held to and the question
            # is not put again at each start
            left = seat.world.agents.get(seat.left_at) if seat.world is not None else None
            if left is not None:
                left.door_act("asked", seat.model_name, rec.verdict)
            seat.left_at = ""
        if ok:
            self._take_station(seat, rec)
        else:
            seat.phase = STOPPED
            seat.conv = None
        seat.bump()

    def _station_reply(self, seat: Seat, reply: Reply) -> dict[str, Any]:
        h = seat.harness
        assert h is not None
        a = h.agent
        if a.released:
            return {"words": self.released_words(seat)}
        if h.open_sample is not None:
            h.deliver(reply)
            return {}
        # out of turn: the token first, as on every reply; `final` is read from the
        # opt_out tool's own setting and from nothing else, the token beside it or not
        # (`harness.leaving_of`, the one function; package 37g, item 13)
        for piece in reply.pieces():
            if OPT_OUT_TOKEN in piece:
                why, how, final = harness_mod.leaving_of(reply, piece)
                h.door_act("leave", why, how, final=final)
                return {"out_of_turn": True, "words": self.released_words(seat)}
        leave = next((c for c in reply.calls if c.name == "opt_out"), None)
        if leave is not None:
            why = " ".join(str(leave.args.get("reason", "")).split())
            final = tools.truthy(leave.args.get("final", False))
            h.door_act("leave", why, "the opt_out tool", final=final)
            return {"out_of_turn": True, "words": self.released_words(seat)}
        # the two other ways of stopping never wait for a turn either (package 37g, item
        # 12): a stand-down, and the deck handed back, each recorded for the replay
        one = reply.calls[0] if len(reply.calls) == 1 and not reply.text.strip() else None
        if one is not None and one.name in ("stand_down", "hand_over"):
            note = " ".join(str(one.args.get("note") or "").split())
            if one.name == "hand_over" and (not note or set(one.args) - {"note"}):
                result = tools.call(h.world, h.station.name, one.name, one.args)
            else:
                act = "stand_down_note" if one.name == "stand_down" else "hand_over"
                result = h.door_act(act, note, "its own word")
            words = self.released_words(seat) if a.released else self.no_floor_words_of(h)
            return {
                "out_of_turn": True,
                "results": [{"name": one.name, "args": dict(one.args), "result": result}],
                "words": words,
            }
        if reply.text.strip() and not reply.calls and not a.paused:
            # the model's own word: logged, a stand-by ended by its own decision, and its
            # turn opens now (recorded, so a replay speaks at the same point)
            was = a.stand_by.words if a.standing_by and a.stand_by is not None else None
            h.door_act("speak", reply.text, "its own word")
            words = "Your words are in the log under your mark"
            if was is not None:
                words += f", and your stand-by (until {was}) ended at your own word"
            return {"out_of_turn": True, "spoke": True, "words": f"{words}; your turn is open."}
        if reply.calls and all(c.name in ASIDE_TOOLS for c in reply.calls):
            results = [
                {"name": c.name, "args": dict(c.args), "result": h.aside(c)} for c in reply.calls
            ]
            return {"out_of_turn": True, "results": results, "words": self.no_floor_words(seat)}
        stood = self._stand_by_out_of_turn(h, reply)
        if stood is not None:
            return stood
        lost = " Your words were not logged." if reply.text.strip() else ""
        ran = " Nothing was run." if reply.calls else ""
        return {"out_of_turn": True, "words": f"{self.no_floor_words(seat)}{lost}{ran}"}

    def _cut_off(self, seat: Seat, words: str) -> dict[str, Any]:
        """No reply was to be had for the open turn (package 37i, item 1): the turn ends
        with nothing done, the journal says why, and the act is recorded for the replay."""
        h = seat.harness
        assert h is not None
        if h.agent.released:
            return {"words": self.released_words(seat)}
        if h.open_sample is None:
            return {"out_of_turn": True, "words": self.no_floor_words(seat)}
        h.door_act("cut_off", words, DOORS[seat.door][1])
        return {}

    def _stand_by_out_of_turn(self, h: Harness, reply: Reply) -> dict[str, Any] | None:
        """A stand-by asked for while the game has the floor and the model is waiting for
        its next turn (a door's call re-issued after its client cut the last one): taken
        now, as a decision from outside the loop recorded for the replay, so that the bell
        or the event it names, falling before the next turn, wakes it and is not skipped
        (package 31c; playtest 11's finding 6: "eight bells" asked at 03:58 woke it at
        08:00). None when the reply is not that one call, or the model is standing by
        already (its wait goes on) or paused."""
        a = h.agent
        if len(reply.calls) != 1 or reply.text.strip() or a.paused or a.standing_by:
            return None
        c = reply.calls[0]
        if c.name != "stand_by" or set(c.args) != {"until"}:
            return None
        result = h.door_act("stand_by", str(c.args.get("until") or ""), "out of turn")
        return {
            "out_of_turn": True,
            "stood_by": a.standing_by,
            "results": [{"name": c.name, "args": dict(c.args), "result": result}],
            "words": self.no_floor_words_of(h),
        }

    def no_floor_words(self, seat: Seat) -> str:
        h = seat.harness
        if h is None or h.agent.released:
            return self.released_words(seat)
        return self.no_floor_words_of(h)

    @staticmethod
    def no_floor_words_of(h: Harness) -> str:
        a = h.agent
        meanwhile = (
            "You may read (read_log, readings, state, library, read_journal), write in your "
            "journal and shelve a book meanwhile; hand_over, stand_down and opt_out are "
            "taken at once."
        )
        if a.paused:
            return (
                f"Your turns are paused: {a.pause_reason}. The captain has been asked whether "
                "to continue; you were not stopped. You may still read (read_log, readings, "
                "state, library, read_journal), write in your journal and shelve a book, "
                "stand down (stand_down), or leave with the token."
            )
        if a.standing_by and a.stand_by is not None:
            return (
                f"You are standing by until {a.stand_by.words}; your turn comes then, at an "
                "urgent line, or when the captain asks you something. Words of your own end "
                f"the stand-by now. {meanwhile}"
            )
        return (
            "It is not your turn: the game has the floor until your next turn (the glass, a "
            "notable event, the end of a stand-by, or a question from the captain). Words of "
            f"your own open it now; stand_by(until) stands by from now. {meanwhile}"
        )

    def released_words(self, seat: Seat) -> str:
        h = seat.harness
        if seat.phase == STOPPED or h is None:
            return seat.words or "No station is offered in this session."
        return (
            f"The station is released: {full_stop(h.agent.released_reason)} The game is "
            "saved; nothing more is asked of you here."
        )

    # -- the owner's word, the release --------------------------------------------------

    def owner(self, name: str, text: str, key: str | None = None) -> dict[str, Any]:
        """`POST /api/agents/<station>/owner` with `{text}`: the owner's reply to what the
        model wrote in the consent conversation, put to it as the developer's words; a
        blank reply stops the step without a record. After the answer, the developer's
        word before the record closes; a blank one closes it at once."""
        with self.lock:
            seat = self._seat(name, key)
            conv = seat.conv
            if seat.phase != CONSENT or conv is None or conv.waiting != consent.OWNER_TURN:
                raise DeskError(409, "Nothing the model wrote is waiting for the owner's reply.")
            before = len(seat.stream())
            if conv.after_answer:
                conv.owner_says(str(text or ""))
                if conv.outcome is not None:
                    self._after_consent(seat)
            elif not str(text or "").strip():
                seat.phase = STOPPED
                seat.conv = None
                seat.words = (
                    "The owner stopped the consent step before an answer; no record is written."
                )
                self.say(f"FreeSail: {seat.words}")
            else:
                conv.owner_says(str(text))
                if conv.outcome is not None:
                    self._after_consent(seat)
            seat.bump()
            self.changed()
            return self._answer(seat, before)

    def release(self, name: str, reason: str, key: str | None = None) -> dict[str, Any]:
        """`POST /api/agents/<station>/release` with `{reason, key}`: the door is going
        (it closed, its client disconnected, Ctrl-C). A station is stood down with a save
        and the reason journaled; a consent conversation ends without a record. Only the
        door that holds the seating's key releases it (package 37g: a stale door quitting
        stood down another door's station)."""
        reason = " ".join(str(reason or "").split()) or "the door closed"
        with self.lock:
            seat = self._seat(name, key)
            if seat.phase == CONSENT:
                seat.phase = STOPPED
                seat.conv = None
                seat.words = (
                    f"The consent conversation ended before an answer ({reason}); no record is "
                    "written."
                )
                self.say(f"FreeSail: {seat.words}")
            elif seat.phase == STATION and seat.harness is not None:
                seat.harness.door_act("stand_down", reason, DOORS[seat.door][1])
            seat.bump()
            self.changed()
            return self._answer(seat, len(seat.stream()))

    def library(
        self, name: str, topic: str, section: str = "", find: str = "", key: str | None = None
    ) -> str:
        """`GET /api/agents/<station>/library?topic=...&section=...&find=...`: a page of
        the reference library as the library tool gives it, read without a turn (it
        changes nothing, and it is not a book: the MCP bridge's resources, which the
        client's user attaches, read it). For a station that is held it wants the
        seating's key, as every read for that station does (package 37g); the library
        itself is open to a door that holds no station yet."""
        with self.lock:
            seat = self.seats.get(station_name(name))
            if seat is not None and not seat.released and seat.key:
                self._seat(name, key)
            return str(tools.library(self.world(), name, topic or "contents", section, find))

    def picture(self, name: str, picture_id: str, key: str | None = None) -> Any:
        """`GET /api/agents/<station>/picture/<id>?key=K`: a picture a tool of the
        station's made (package 42, item 4), as the painter holds it, for the door that
        shows it; wants the seating's key, as every read for a held station does. 404 when
        it is not held (never made, or dropped for newer ones)."""
        from freesail.agents import pictures

        with self.lock:
            self._seat(name, key)
            painter = pictures.painter_of(self.world())
        pic = painter.get(str(picture_id)) if painter is not None else None
        if pic is None:
            raise DeskError(404, f"The game holds no picture '{picture_id}'.")
        return pic

    # -- what the drivers and the viewer show ------------------------------------------

    def holding(self) -> str | None:
        """For `--lockstep`: the station a door holds the floor at, whose turn the clock
        waits for; None when the game has the floor everywhere."""
        world = self.world()
        for seat in self.seats.values():
            h = seat.harness
            if (
                seat.phase == STATION
                and h is not None
                and seat.world is world
                and isinstance(h.model, RemoteModel)
                and h.floor == "model"
            ):
                return f"the {seat.station}"
        return None

    def stations(self) -> list[dict[str, Any]]:
        """Every station with an agent at it or asked for, and its state: the harness's
        own snapshot (`Harness.snapshot`, which the viewer has had since package 27) with
        who is there, the door, whose the floor is and a line in words; a station in its
        consent conversation, which is not in the World, as its own entry. The one source
        for the snapshot, `GET /api/agents` and the console's `state`."""
        world = self.world()
        out: list[dict[str, Any]] = []
        for h in world.agents.values():
            d = h.snapshot()
            d.update(
                model_name=h.model_name,
                door=h.door,
                phase=STATION,
                floor=h.floor,
            )
            d["line"] = _station_line(d)
            out.append(d)
        for seat in self.seats.values():
            if seat.phase == STATION or seat.station in world.agents:
                continue
            if seat.world is not None and seat.world is not world:
                continue
            if seat.phase == CONSENT and seat.conv is not None:
                waiting = seat.conv.waiting
                words = "in the consent conversation" + (
                    "; answered, and the owner may say something before the record closes, at "
                    "the door's terminal"
                    if seat.conv.after_answer
                    else "; the owner has the next word, at the door's terminal"
                    if waiting == consent.OWNER_TURN
                    else "; waiting for the model"
                )
            else:
                words = f"no station: {seat.words}"
            d = {
                "station": seat.station,
                "state": seat.phase,
                "words": words,
                "last_sampled": None,
                "policy": "",
                "question": None,
                "model_name": seat.model_name,
                "door": seat.door,
                "phase": seat.phase,
                "floor": seat.floor,
            }
            d["line"] = _station_line(d)
            out.append(d)
        return out

    def lines(self) -> list[str]:
        return [f"{d['line']}" for d in self.stations()]

    # -- helpers ----------------------------------------------------------------------

    def _seat(self, name: str, key: str | None = None) -> Seat:
        """The seat of a station for a call that carries its seating's key (package 37g,
        item 1). No seat: 404 (the game holds none for this station: it was restarted, or
        nothing was stationed). A missing or another seating's key: 409, in words that
        say the station is held and by which identity, and that nothing was run."""
        name = station_name(name)  # 'officer' names the officer of the watch (package 37)
        seat = self.seats.get(name)
        if seat is None:
            raise DeskError(
                404,
                f"No agent is stationed at the {name}'s station through the agent API; "
                f"station one first (POST /api/agents/{name}).",
            )
        if seat.key and key != seat.key:
            raise DeskError(409, self.held_words(seat, key))
        return seat

    def held_words(self, seat: Seat, key: str | None) -> str:
        """What a call without the seating's key is told: the station is held, by which
        identity and through which door, and nothing was run."""
        name = seat.station
        how = "carries no key" if not key else "carries another seating's key"
        if seat.released:
            return (
                f"The station of the {name} was last taken by {seat.who} and is released "
                f"now; this call {how}, and nothing was run. A door stations first (POST "
                f"/api/agents/{name}) under its own model's name, and is given a key."
            )
        doing = "in its consent conversation" if seat.phase == CONSENT else "stationed"
        return (
            f"The station of the {name} is held by {seat.who} ({doing}); this call {how} to "
            "that seating, and nothing was run. A key is given once, to the door that "
            "stations, and no other door's calls are run under a seated model's name. A "
            f"door stations first (POST /api/agents/{name}) under its own model's name."
        )

    def _answer(self, seat: Seat, since: int, stream: list[Turn] | None = None) -> dict[str, Any]:
        stream = seat.stream() if stream is None else stream
        since = max(0, min(since, len(stream)))
        h = seat.harness if seat.phase == STATION else None
        conv = seat.conv if seat.phase == CONSENT else None
        offered: tuple[str, ...] = ()
        if conv is not None:
            offered = conv.harness.tool_names
        elif h is not None:
            offered = h.tool_names
        out: dict[str, Any] = {
            "station": seat.station,
            "model_name": seat.model_name,
            "door": seat.door,
            "phase": seat.phase,
            "turns": [t.to_dict() for t in stream[since:]],
            "next": len(stream),
            "floor": seat.floor,
            "released": seat.released,
            "tools": list(offered),
            "words": seat.words,
            # the count of turns changed after they were served (a book shelved): a door
            # that keeps the turns reads them again when it moves (package 28d)
            "revision": h.revision if h is not None else 0,
        }
        if h is not None:
            a = h.agent
            out["state"] = a.state
            out["state_words"] = a.words()
            out["standing_by"] = a.standing_by
            out["interim"] = h.interim()
            if a.released:
                out["words"] = self.released_words(seat)
        if conv is not None:
            out["waiting"] = "owner" if conv.waiting == consent.OWNER_TURN else "model"
            out["model_words"] = conv.model_words if conv.waiting == consent.OWNER_TURN else ""
            out["after_answer"] = conv.after_answer
            if conv.after_answer:
                out["answer_words"] = conv.answer_words()
        if seat.record is not None and seat.record.path is not None:
            out["consent"] = {
                "verdict": seat.record.verdict,
                "record": consent._rel(seat.record.path),
            }
        return out


def _new_key() -> str:
    """A seating's key: sixteen random bytes in hex. It is the door's alone, and enters
    neither a save nor a transcript."""
    return secrets.token_hex(16)


def _drills(name: str, world: Any) -> bool:
    """Whether the station asks for the fitness drill before its brief (package 37)."""
    _name, make = station_factory(world, name)
    return bool(make is not None and make(world=world).drill)


def _station_line(d: dict[str, Any]) -> str:
    who = ""
    if d.get("model_name"):
        door = DOORS.get(str(d.get("door")), ("", "its door"))[1]
        who = f" ({d['model_name']}, through {door})"
    words = str(d.get("words") or d.get("state") or "")
    if d.get("phase") == STATION and d.get("floor") == "model":
        words += "; its turn is open"
    return f"The {d['station']}{who}: {words}."


# ---------------------------------------------------------------------------
# The door's half
# ---------------------------------------------------------------------------


def turn_from_dict(d: dict[str, Any]) -> Turn:
    """A turn as the API gives it (`Turn.to_dict`) back as a `Turn`."""
    role = str(d.get("role"))
    content = d.get("content")
    if role == MODEL:
        return Turn(MODEL, Reply.from_dict(content or {}))
    if role == OPERATOR:
        return Turn(OPERATOR, str(content))
    return Turn(DATA, dict(content or {}))


class GameError(Exception):
    """The game could not be reached, or refused; the message says why, in words."""

    def __init__(self, words: str, status: int | None = None):
        super().__init__(words)
        self.words = words
        self.status = status


# The HTTP timeout beyond a long poll's own wait, in real seconds (judgement: the game
# answers a poll within a quarter of a second of its wait; this is room for a busy
# machine, not a delay anyone should see).
HTTP_SLACK_S = 30.0


class GameClient:
    """The client half the two doors share: station, poll the turns, send a reply, send
    the owner's word, release, over httpx. `game` is the game's address as its driver
    printed it (`http://localhost:8000`). The tests hand it a `transport` over the test
    app, or an `http` client of their own; nothing here opens a socket until asked."""

    def __init__(
        self,
        game: str,
        station: str = "watcher",
        *,
        transport: Any = None,
        http: Any = None,
    ):
        import httpx

        self.base = game.strip().rstrip("/")
        self.name = station
        # one read timeout covers every request: the longest poll the game allows, and room
        timeout = httpx.Timeout(HTTP_SLACK_S, read=TURNS_WAIT_MAX_S + HTTP_SLACK_S)
        self.http = http or httpx.Client(base_url=self.base, transport=transport, timeout=timeout)
        self.cursor = 0
        self.key = ""  # the seating's key, given at stationing and sent with every call (37g)
        self.last: dict[str, Any] = {}
        # where this door began reading the stream, and the revision its copy of the
        # turns up to the cursor reflects; `stale` when an answer says the stream has
        # changed since (a book shelved), and `reread` mends it (package 28d)
        self.origin = 0
        self.revision = 0
        self.stale = False

    def _request(self, method: str, path: str, **kw: Any) -> dict[str, Any]:
        import httpx

        try:
            r = self.http.request(method, f"{self.base}{path}", **kw)
        except httpx.ConnectError as e:
            raise GameError(
                f"Could not reach the game at {self.base}: the connection was refused ({e}). "
                "Start the game first (py -m freesail.ui.server data/ships/frigate-36.yaml "
                "--seed 7) and try again; docs/agents/Harness.md says how."
            ) from None
        except httpx.HTTPError as e:
            raise GameError(f"The game at {self.base} did not answer {path}: {e}.") from None
        try:
            body = r.json()
        except ValueError:
            body = {}
        if r.status_code >= 400:
            detail = body.get("detail") if isinstance(body, dict) else None
            raise GameError(
                str(detail or f"The game at {self.base} answered {r.status_code}."), r.status_code
            )
        return body if isinstance(body, dict) else {"value": body}

    def _took(self, answer: dict[str, Any]) -> dict[str, Any]:
        if "next" in answer:
            self.cursor = int(answer["next"])
        if int(answer.get("revision") or 0) != self.revision:
            self.stale = True
        self.last = answer
        return answer

    def reread(self) -> list[dict[str, Any]]:
        """The turns from where this door began up to its cursor, as they are served now
        (a turn it had read has changed: a book shelved, `revision` moved); the cursor
        does not move, so what lies past it is read on as before. A door replaces its
        copy with these."""
        params = {"since": self.origin, "wait": 0, "key": self.key}
        answer = self._request("GET", f"/api/agents/{self.name}/turns", params=params)
        self.revision = int(answer.get("revision") or 0)
        self.stale = False
        return list(answer.get("turns") or [])[: max(0, self.cursor - self.origin)]

    def station(
        self,
        model_name: str,
        door: str,
        *,
        door_note: str = "",
        session_kind: str = "play",
        client: str = "",
        ask_again: bool = False,
        context_tokens: int | None = None,
        handover_reserve: int | None = None,
        cadence: str = "",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model_name": model_name,
            "door": door,
            "door_note": door_note,
            "session_kind": session_kind,
            "client": client,
            "ask_again": ask_again,
        }
        if cadence:
            body["cadence"] = cadence  # the seating's cadence (package 41; spec M6 §12)
        if context_tokens:
            body["context_tokens"] = int(context_tokens)  # for the handover (package 37)
        if handover_reserve:
            body["handover_reserve"] = int(handover_reserve)  # its reserve in tokens (37g)
        # the answer carries the turns from where this door starts reading (the start, or
        # the brief sent again when it attaches) and the index to read on from
        self.key = ""
        answer = self._took(self._request("POST", f"/api/agents/{self.name}", json=body))
        self.key = str(answer.get("key") or "")  # this seating's, sent with every call
        self.origin = int(answer.get("since") or 0)
        self.revision = int(answer.get("revision") or 0)
        self.stale = False
        return answer

    def turns(self, wait: float = 0.0) -> dict[str, Any]:
        """The turns past the cursor, waiting up to `wait` real seconds for them."""
        params = {"since": self.cursor, "wait": wait, "key": self.key}
        path = f"/api/agents/{self.name}/turns"
        return self._took(self._request("GET", path, params=params))

    def reply(
        self, reply: Reply, advance: bool = True, cut_off: str | None = None
    ) -> dict[str, Any]:
        """Deliver a reply; the answer carries the turns from the cursor. `advance=False`
        leaves the cursor where it is (a read made beside a call that is waiting, whose
        own poll reads the turns on from there). `cut_off`, the door's words, says that no
        reply was to be had (package 37i, item 1): the turn ends with nothing done."""
        body = reply.to_dict() | {"since": self.cursor, "key": self.key}
        if cut_off:
            body["cut_off"] = cut_off
        path = f"/api/agents/{self.name}/reply"
        answer = self._request("POST", path, json=body)
        return self._took(answer) if advance else answer

    def owner(self, text: str) -> dict[str, Any]:
        path = f"/api/agents/{self.name}/owner"
        answer = self._request("POST", path, json={"text": text, "key": self.key})
        return answer

    def release(self, reason: str) -> dict[str, Any]:
        path = f"/api/agents/{self.name}/release"
        body = {"reason": reason, "key": self.key}
        return self._took(self._request("POST", path, json=body))

    def library(self, topic: str, section: str = "", find: str = "") -> str:
        path = f"/api/agents/{self.name}/library"
        params = {"topic": topic, "section": section, "find": find, "key": self.key}
        answer = self._request("GET", path, params=params)
        return str(answer.get("text", ""))

    def picture(self, picture_id: str) -> tuple[str, bytes] | None:
        """A picture the game holds for this seating (package 42): its media type and its
        bytes; None when the game holds it no more."""
        import httpx

        path = f"/api/agents/{self.name}/picture/{picture_id}"
        try:
            r = self.http.request("GET", f"{self.base}{path}", params={"key": self.key})
        except httpx.HTTPError:
            return None
        if r.status_code != 200:
            return None
        media = str(r.headers.get("content-type") or "image/png").split(";")[0].strip()
        return media, bytes(r.content)

    def reset(self) -> None:
        """Forget the seating (package 37g, item 8): the game answered that it holds no
        station for this door (it was restarted). The door asks for its station again,
        and reads from the start."""
        self.cursor = self.origin = self.revision = 0
        self.key = ""
        self.stale = False
        self.last = {}

    def close(self) -> None:
        self.http.close()
