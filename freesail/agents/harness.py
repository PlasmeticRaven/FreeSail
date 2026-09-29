"""The harness loop (spec M4 §11): one agent at one station, sampled by policy, its
replies read in a fixed order, its welfare watched in steps, its station released on
the token, on a stop or on the captain's word.

**The loop.** `World.tick` calls `on_tick` after the standing orders and `World.submit`
calls `on_order` after an order is logged. At a sampling point (by the policy, when the
World reaches an event the policy names, when a stand-by ends, or on `ask`) the harness
builds a `Sample` (the log lines since the last sample, the readings in words, any
question, any notice of its own), appends it to the conversation **as data**, and calls
the model. The brief (`agent.Brief`) is the only operator turn and is sent once at the
start (`start`) and again only when `resend_brief` is called. Each reply is read in
this order:

1. **The token scan.** `OPT_OUT_TOKEN` anywhere in the raw reply, before anything else
   reads it: the exit is journaled as `agent.opted_out` with the text after the token as
   the reason, the station is released, the game is saved through the callback the
   driver handed in (last, so that the file holds the exit), the loop ends.
   Unconditional (truth 41).
2. **The tool calls**, in order, each through `tools.call` (authority-checked), each
   result returned to the model as data, up to `TOOL_CALLS_PER_SAMPLE` in one sample,
   which the brief states as a budget. A reply with calls is followed by another call
   of the model with the results; a reply without calls ends the sample.
3. **The free text** lands in the log as `agent.note` under the station's mark
   ("[watcher] ..."), routine; empty text is not logged.

**Welfare, graduated** (spec §11, owner's ruling; `docs/agents/README.md` commitment 3).
The detector judges the game and never the prose: the same order text submitted
`WELFARE_REPEAT_N` times with no change in the readings between (the words a model
reads, `tools.readings_digest`), or no reply at all past the station's `patience_s`.
On firing the harness **nudges** once (a notice in the next sample saying what was seen
and the three things the model may do, logged `agent.nudged`); if the pattern goes on
after the nudge it **pauses** sampling (`agent.paused`, notable) and puts the question to
the human through the log and the snapshot; only with no answer within
`WELFARE_UNATTENDED_BOUND_S` of ship's time, or the driver's ten real minutes
(`WELFARE_UNATTENDED_REAL_S`, which the driver measures and reports through
`check_unattended`), does it **stand the agent down** (save, `agent.stopped`, release).
A model that answers the nudge by standing by, or by anything but the pattern, ends
the matter. The human answers a pause with `resume the watcher` or `stand down the
watcher`, and may stand any agent down at any time.

**Stand by** (`stand_by`) is a logged decision (`agent.stood_by`), and it ends the
model's turn at once, at every door: no result is returned and the model is not asked
again until the stand-by ends (package 28c; playtest 4's turn that never closed, the
model standing by thirteen times in answer to "Standing by"). Sampling is
suspended until the event, the bells, the interval ('a glass', '5 minutes') or a line of
a severity ('a notable event', 'an urgent event'), and taken up at that point (truth
44). A question from the captain wakes a standing-by agent, and so does any urgent line
in the log, whatever the stand-by was for, with the line named as the reason (package
28c; the owner's ruling: urgent wakes; notable is bundled and shown). The sample that
ends a stand-by carries the notable lines logged while it lasted, counted and listed
(`Sample.stood_by`), besides the log lines as ever; while it lasts, `interim` gives a
door the same digest so far. A stand-by is a decision not to be sampled, not a decision
to be blind.

**The model's own word** (`own_word`, through `door_act`): a door that hands the floor
back and waits (the MCP bridge's `say`) may speak while the game has the floor. The
words go in the log under the mark, a stand-by ends as the model's own decision (logged
and journaled), and the model is sampled at once; recorded like the other acts from
outside the loop, so a replay makes it at the same point.

**Determinism and replay.** The loop is tick-driven, never wall-clock-driven. The
model's replies are the only input the World does not already hold, so the harness
keeps them as a transcript in its save record (`save`), each with the tick and the
count of journaled orders at which it was taken, and a replay plays them back through
`Playback` at those same points (`restore`), which rebuilds the same log lines and the
same journal (truth 45 and the replay tests). A stop that comes from outside the loop
(a door's release, the token sent out of turn, the driver's ten real minutes) is
recorded the same way (`door_act`) and made again by the replay at the same point. An
agent stationed at tick T is stationed in the replay at the end of tick T, after the
orders journaled before it, which is where the drivers station it.

**Lockstep and live sampling.** An in-process door answers at once (the fake, the
REPL, the tests): the World waits at each sampling point while it answers, which is
lockstep. A door that answers late returns `None` from `reply` (the REPL's turn mode,
`remote.RemoteModel` behind the agent API of package 28b): the sample stays open, the
floor is the model's, and its reply comes by `deliver`. **The World never waits for
it** (unless the driver is told to, `--lockstep`): a sampling point reached while the
floor is the model's does not open a second sample; it is **folded** into the open one
(`_fold`): the new log lines are appended, the readings replaced by the latest, the
reason noted, a new question from the captain added (one the open turn carries already
is not put again: playtest 7's redelivered question), the harness's notices carried. The
merged sample is `open_sample`; the conversation gets each fold as a data turn of its
own holding what is new (marked `folded`), so the turns since the model's last reply
are everything since its last reply, whether its door had read the sample already or
not. Silence is judged on ship's time as before: a floor held with no reply for the
station's patience brings the nudge as a fold, and a second span the pause, which
takes the floor back.

**The shelf** (package 28d; spec M4 open item 9). A library read is a book taken off the
shelf, and the reader puts it back. Every library page, and a `read_log` longer than
`BOOK_SIZE_TOKENS`, is a **book** (`tools.book_of`): its result opens with a handle line
("primer 3, reefing, opened 04:10; book 7"), the number counting up per agent. `shelve`
(a handle, a topic's words, or nothing for every open book) puts books back: the book's
result in the conversation is replaced by its stub ("You read primer 3, reefing, at 04:10;
shelved (book 7). library(...) opens it again."), so from the model's next request on
only the line remains. A book left open goes back by itself after `SHELF_LIFE_TURNS` of
the model's turns after the one it was read in, the stub in its place and a notice in
the next sample. The model's turns are counted where a sample ends (`_end_sample`), so a
replay shelves at the same points; a shelve is a tool call in a reply, so the
transcript holds it. A shelved turn is served as its stub from then on: the
conversation is changed in place and `revision` counts the changes, which the agent API
carries so that a door rebuilding its messages from the game's turns knows to read them
again (`remote.Desk`). A door whose client keeps its own conversation (MCP; the REPL,
whose turns are printed once) is told so plainly by `shelve` and by the notice: the
game will not show the pages again, but it cannot take them out of the client's
conversation. Reads out of turn (a door's read-only call while the game has the floor)
are books too, recorded as acts (`door_act`: "read", "shelve") so a replay numbers and
shelves the same; the game keeps no copy of such a read's pages, so there is nothing to
stub. Nothing here makes the reference less reachable: every book opens again on
request, under a new number (`docs/design/Papers-and-Books.md`).

**A plain conversation** (`conversation=True`, spec §14): the consent step runs the
consent brief through this same loop, so the token scan, the tool calls and the journal
are the same code, with three differences. The brief is fixed (`brief=`, a
`Brief.plain`), not built from a station; a sample carries only what is put to the
model (`reason`, `question`, `notices`: no log, no readings, no ship's time); and the
caller puts each turn with `put`, since no World ticks. `allowed_tools` limits the tools
that run (the consent step's is `answer` alone): any other is refused in words as its
result, and a door that sends tool definitions reads the list from `offered_tools`.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from freesail.agents import tools
from freesail.agents.agent import (
    BOOK_SIZE_TOKENS,
    BRIEF_LOG_LINES,
    OPT_OUT_TOKEN,
    PAUSED,
    RELEASED,
    SESSION_TEST,
    SHELF_LIFE_TURNS,
    STANDING_BY,
    STATIONED,
    AgentState,
    Brief,
    SamplingPolicy,
    StandBy,
    Station,
    number_words,
)
from freesail.agents.fake import Transcript
from freesail.agents.journal import Journal
from freesail.agents.model import DATA, MODEL, OPERATOR, Model, Reply, Sample, ToolCall, Turn
from freesail.api import readings as R
from freesail.core.events import Event, Rollup, RollupView, Severity
from freesail.orders.errors import OrderError

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "BOOK_SIZE_TOKENS",
    "OPT_OUT_TOKEN",
    "SHELF_LIFE_TURNS",
    "Book",
    "Playback",
    "SAMPLE_ROUTINE_LINES",
    "TOOL_CALLS_PER_SAMPLE",
    "WELFARE_REPEAT_N",
    "WELFARE_UNATTENDED_BOUND_S",
    "WELFARE_UNATTENDED_REAL_S",
    "Harness",
    "SaveFn",
    "conversation_text",
    "restore",
]

# The tool calls one sample may make, stated in the brief as a budget (judgement: a
# watcher's turn is a look at the log, the readings and perhaps a page of the library;
# eight leaves room for a question answered after three or four reads).
TOOL_CALLS_PER_SAMPLE = 8

# The same order this many times with no change in the readings between (spec §11).
WELFARE_REPEAT_N = 3

# Nobody answered the pause within a watch of ship's time (spec §11)...
WELFARE_UNATTENDED_BOUND_S = R.INTERVALS["a watch"]
# ...or ten real minutes, whichever first; the driver measures the real minutes.
WELFARE_UNATTENDED_REAL_S = 600

# Routine lines a sample carries at most, the most recent kept; notable and urgent lines
# are all kept (judgement: a glass at sea is some tens of routine lines, and `read_log`
# has the rest; the count left out is stated in the sample). Below the roll-up's
# compression (`events.ROLLUP_FROM`); at and above it a sample carries the log as the
# captain reads it, rolled up by the hour (spec M4 open item 8, the owner's ruling (a):
# the captain and the watcher read the same digest of the same hour), and this cap still
# holds over what is left.
SAMPLE_ROUTINE_LINES = 40

# Why a sample is taken when the captain tells the station something (`tell the watcher
# ...`, package 29): the words ride in the sample's `word`, not its `question`, and no
# answer is owed.
A_WORD = "a word from the captain"

# The nudge (spec §11), in the consent brief's voice: what was seen, what may be done.
NUDGE_REPEAT = (
    "You have given the same order {n} times and nothing in the readings has changed. "
    "You may continue, stand by until an event, or leave with the token {token}."
)
NUDGE_SILENCE = (
    "You have given no reply for {span}. You may continue, stand by until an event, or "
    "leave with the token {token}."
)

# The words a stand-by takes for a severity: any line of it or above from anyone but the
# agent ends the stand-by (package 28c).
STAND_BY_SEVERITIES = {
    "a notable event": "notable",
    "notable event": "notable",
    "a notable line": "notable",
    "an urgent event": "urgent",
    "urgent event": "urgent",
    "an urgent line": "urgent",
}

# What a fold says to the model (a data turn's `folded` key), plain and exact.
FOLDED_WORDS = (
    "Added to your open turn: what has happened since, while you had the floor. Your turn "
    "stays open until you reply."
)

SaveFn = Callable[["World", str], Any]

# The doors whose client keeps the model's conversation itself, so that a shelved book's
# pages stay in it: the MCP client's chat, and the REPL, which prints each turn once.
DOORS_THAT_KEEP_THEIR_OWN = ("mcp", "repl")

# A book's states: open in the conversation; shelved by the model; gone back by the
# shelf-life; left behind by a brief sent again (the door's conversation starts at the
# brief, so it is no longer in it); unseen (its result never reached the model, a
# stand-by having ended the turn); read aside (out of turn: the game keeps no copy).
OPEN, SHELVED, WENT_BACK, LEFT_BEHIND, UNSEEN, ASIDE = (
    "open",
    "shelved",
    "went back",
    "left behind",
    "unseen",
    "aside",
)


@dataclass
class Book:
    """A read the model took off the shelf: its number (counting up per agent), the words
    that name it, the call that reads it again, the ship's clock when it was opened, the
    model's turn it was opened in (turns ended before it), and where its result stands
    in the conversation (the turn's index and the result's) once it is there."""

    number: int
    title: str
    reopen: str
    opened: str
    turn: int
    state: str = OPEN
    slot: int | None = None  # the result's index among its reply's tool results
    at: int | None = None  # the index of the tool-results turn in `Harness.turns`

    @property
    def handle(self) -> str:
        return f"{self.title}, opened {self.opened}; book {self.number}"

    @property
    def named(self) -> str:
        return f"book {self.number} ({self.title})"


class Harness:
    def __init__(
        self,
        world: World,
        station: Station,
        model: Model,
        *,
        session_kind: str = SESSION_TEST,
        save: SaveFn | None = None,
        door_note: str = "",
        start_at: int | None = None,
        start_after_orders: int = 0,
        brief: Brief | None = None,
        allowed_tools: tuple[str, ...] | None = None,
        conversation: bool = False,
    ):
        if station.name in world.agents:
            other = world.agents[station.name]
            raise OrderError(
                f"The station of the {station.name} is {other.agent.words()}; a station is "
                f"taken once in a game."
            )
        self.world = world
        self.station = station
        self.model = model
        self.save_fn = save
        self.door_note = door_note
        self.agent = AgentState(station, session_kind=session_kind)
        self.journal: Journal = world.agent_journals.setdefault(station.name, Journal(station.name))
        self.turns: list[Turn] = []
        self.transcript: list[dict[str, Any]] = []
        self.brief: Brief | None = None
        self.last_save: Any = None  # what the last save returned, or the save dict
        self._start_at = start_at
        self._start_after_orders = start_after_orders  # journal length at the start
        self._seen_log = len(world.log)  # for the events policy and the stand-by watch
        self._sample_seen = len(world.log)  # for the sample's log lines
        # the roll-up (spec M4 §20, open item 8): the log as the captain reads it at the
        # driver's compression (`World.compression`), fed every line in order
        self._rollup = RollupView()
        self._sampling = False
        self._open: Sample | None = None  # a sample awaiting its reply
        self._calls_this_sample = 0
        self._sample_had_words = False
        self._sample_repeated = False
        self._stand_down_requested: tuple[str, str] | None = None
        self._paused_real: float | None = None
        self._fixed_brief = brief
        self.allowed_tools = tuple(allowed_tools) if allowed_tools is not None else None
        self.conversation = conversation
        self._question_sent: str | None = None  # the question the open sample carries
        # a stand-by taken ends the model's turn (package 28c); a save recorded before
        # that rule replays by the old one, its recorded replies after a stand-by kept
        self.stand_by_ends_turn = True
        self._stood_at: tuple[str, str] | None = None  # (the stand-by's words, its stamp)
        # where the present wait began (the log's length and the stamp): the stand-by's
        # start, or the end of the last sample, for the stand-by digest and `interim`
        self._wait_from: tuple[int, str] = (len(world.log), world.clock.stamp())
        # who is at the station, for the save and the drivers (set by the agent API)
        self.model_name = ""
        self.door = ""
        # the shelf (package 28d): the books read, the model's turns ended so far (the
        # shelf-life counts them), the books opened in the reply being taken, and the
        # count of changes to turns already served (a door reads the turns again on it)
        self.books: list[Book] = []
        self.turns_ended = 0
        self._new_books: list[Book] = []
        self.revision = 0
        world.agents[station.name] = self

    # -- properties --------------------------------------------------------------------

    @property
    def actor(self) -> str:
        return f"the {self.station.name}"

    @property
    def mark(self) -> str:
        return f"[{self.station.name}]"

    @property
    def policy(self) -> SamplingPolicy:
        return self.station.policy

    @property
    def open_sample(self) -> Sample | None:
        return self._open

    @property
    def started(self) -> bool:
        return self.agent.stationed_tick is not None

    @property
    def floor(self) -> str:
        """Whose the floor is: "model" while a sample is open, else "game"."""
        return "model" if self._open is not None and not self.agent.released else "game"

    @property
    def tool_names(self) -> tuple[str, ...]:
        """The tools this harness runs, in the table's order: all of `tools.TOOLS`, or
        the allow-list when one is set."""
        if self.allowed_tools is None:
            return tools.tool_names()
        return tuple(n for n in tools.tool_names() if n in self.allowed_tools)

    # -- start -------------------------------------------------------------------------

    def start(self) -> None:
        """Take the station now: the brief as the one operator turn, the first sample."""
        world = self.world
        self.agent.stationed_tick = world.clock.tick
        self.agent.last_heard_tick = world.clock.tick
        self._start_at = None
        self._start_after_orders = len(world.journal)
        if self.conversation:
            words = f"The {self.station.name} conversation begins; no station is offered."
        else:
            words = f"The {self.station.name} takes the station; sampled {self.policy.describe()}."
        world.record(
            Severity.ROUTINE,
            "agent.stationed",
            words,
            actor=self.actor,
            data={"station": self.station.name, "policy": self.policy.save()},
        )
        self._seen_log = len(world.log)
        self._sample_seen = len(world.log)
        self.resend_brief()
        if not self.conversation:  # a conversation's first turn is what the caller puts
            self._sample("the start")

    def resend_brief(self) -> Brief:
        """Build the brief from the station and the situation and send it as operator
        text. Sent once by `start`; a caller sends it again only on purpose. A fixed
        brief (a plain conversation's) is sent as it was given."""
        if self._fixed_brief is not None:
            self.brief = self._fixed_brief
            self.turns.append(Turn(OPERATOR, self.brief.text()))
            return self.brief
        for b in self.books:
            if b.state == OPEN:
                b.state = LEFT_BEHIND  # a door's conversation begins at the brief
        world = self.world
        lines = [
            f"{d['stamp']}  {d['text']}"
            for d in tools.read_log(world, self.station.name)["lines"][-BRIEF_LOG_LINES:]
        ]
        self.brief = Brief.build(
            self.station,
            self.agent.session_kind,
            lines,
            tools.readings_words(world),
            self.tool_names,
            door_note=self._door_note_with_budget(),
        )
        self.turns.append(Turn(OPERATOR, self.brief.text()))
        return self.brief

    def take_over(self, model: Model, save: SaveFn | None = None, door_note: str = "") -> None:
        """A door continues a restored station (a loaded game) with a live model: the
        brief is sent again with the situation now, as the latest operator turn, and a
        sample the replay left open is sent again after it as data, so the new model's
        conversation begins at its own brief. A door reads from the last operator turn."""
        self.model = model
        if save is not None:
            self.save_fn = save
        if door_note:
            self.door_note = door_note
        if self.agent.released or not self.started:
            return
        self.stand_by_ends_turn = True  # a live model plays by the rule of its time
        self.resend_brief()
        if self._open is not None:
            self.turns.append(Turn(DATA, self._open.to_dict()))

    def _door_note_with_budget(self) -> str:
        budget = (
            f"A sample may make up to {TOOL_CALLS_PER_SAMPLE} tool calls; that is a budget, "
            f"not a rule of conduct."
        )
        return f"{budget} {self.door_note}".strip()

    # -- the hooks the World calls -----------------------------------------------------

    def on_tick(self) -> None:
        self._tick_step()
        if self.started and not self.agent.released:
            self._play_door_acts()

    def _tick_step(self) -> None:
        world = self.world
        tick = world.clock.tick
        if self._start_at is not None:
            if tick >= self._start_at and len(world.journal) >= self._start_after_orders:
                self.start()
            return
        if not self.started or self.agent.released:
            return
        new = [world.log[i] for i in range(self._seen_log, len(world.log))]
        self._seen_log = len(world.log)
        if self._open is not None:
            # the floor is the model's: a sampling point folds into the open sample
            self._while_open(new)
            if self._open is not None:
                self._poll()
            return
        a = self.agent
        if a.paused:
            if a.paused_tick is not None and tick - a.paused_tick >= WELFARE_UNATTENDED_BOUND_S:
                self.stand_down(
                    f"paused ({a.pause_reason}) and nobody answered within a watch",
                    by="the harness",
                )
            return
        if a.standing_by:
            ended = A_WORD if a.word is not None else self._stand_by_ended(new)
            if ended is None:
                return
            self._resume_from_stand_by(ended)
            return
        if a.question is not None:
            self._sample("a question")
            return
        if a.word is not None:
            self._sample(A_WORD)
            return
        reason = self._policy_due(new)
        if reason is not None:
            self._sample(reason)

    def _while_open(self, new: list[Event]) -> None:
        """A tick while the floor is the model's (a door that answers late): a sampling
        point the policy names is folded into the open sample, and a floor held silent
        for the station's patience brings the nudge, then the pause, which takes the
        floor back (spec §11, §13)."""
        a = self.agent
        tick = self.world.clock.tick
        heard = a.last_heard_tick if a.last_heard_tick is not None else tick
        if tick - heard >= self.station.patience_s and not a.paused:
            a.last_heard_tick = tick  # the next span is counted from here
            self._welfare_fire("silence")
            if a.paused:
                self._open = None
                return
            self._fold("no reply")
            return
        reason = self._policy_due(new)
        if reason is None and a.question is not None and a.question != self._question_sent:
            reason = "a question"
        if reason is None and a.word is not None:
            reason = A_WORD
        if reason is not None:
            self._fold(reason)

    def on_order(self) -> None:
        """After an order is logged: a stand-down the captain ordered is carried out now
        (after the order is journaled, so the save holds it), and a question is served
        (folded into the open sample when the floor is the model's). A restored agent
        stationed after the orders of its tick starts here."""
        self._order_step()
        if self.started and not self.agent.released:
            self._play_door_acts()

    def _order_step(self) -> None:
        if self._start_at is not None:
            world = self.world
            if (
                world.clock.tick >= self._start_at
                and len(world.journal) >= self._start_after_orders
            ):
                self.start()
            return
        if self._stand_down_requested is not None:
            reason, by = self._stand_down_requested
            self._stand_down_requested = None
            self.stand_down(reason, by=by)
            return
        if not self.started or self.agent.released or self._sampling:
            return
        a = self.agent
        if self._open is not None:
            if a.question is not None and a.question != self._question_sent and not a.paused:
                self._fold("a question")
            self._poll()  # a replay's reply may be due after this order
            return
        if a.question is None or a.paused:
            return
        if a.standing_by:
            self._resume_from_stand_by("a question from the captain")
            return
        self._sample("a question")

    def _policy_due(self, new: list[Event]) -> str | None:
        p = self.policy
        tick = self.world.clock.tick
        if p.every_s and self.agent.stationed_tick is not None:
            since = tick - self.agent.stationed_tick
            if since > 0 and since % p.every_s == 0:
                return "the glass" if p.every_s == R.INTERVALS["a glass"] else "the interval"
        if p.events:
            for e in new:
                if e.actor != self.actor and p.samples_severity(e.severity):
                    return f"a {e.severity.value} event: {e.text}"
        return None

    def _stand_by_ended(self, new: list[Event]) -> str | None:
        sb = self.agent.stand_by
        if sb is None:
            return "nothing to stand by for"
        others = [e for e in new if e.actor != self.actor]
        # an urgent line wakes a stand-by whatever it was for, and is named
        for e in others:
            if e.severity is Severity.URGENT:
                return f"an urgent event: {e.text}"
        if sb.until_tick is not None and self.world.clock.tick >= sb.until_tick:
            return sb.words
        if sb.event is not None:
            spec = R.EVENTS[sb.event]
            for e in new:
                if R.event_matches(spec, e.kind, e.data):
                    return sb.words
        if sb.severity is not None:
            floor = Severity(sb.severity).rank
            for e in others:
                if e.severity.rank >= floor:
                    return f"a {e.severity.value} event: {e.text}"
        return None

    def _notable_since(self, start: int) -> list[dict[str, Any]]:
        """The notable lines logged since `start` by anyone but the agent, as `read_log`
        gives them (urgent lines end a stand-by, so the digest is of the notable)."""
        world = self.world
        return [
            tools.log_line(world.log[i])
            for i in range(start, len(world.log))
            if world.log[i].actor != self.actor and world.log[i].severity is Severity.NOTABLE
        ]

    def _stood_by_digest(self, reason: str = "") -> dict[str, Any] | None:
        """For the sample that ends a stand-by: since when, until what, and the notable
        lines logged while it lasted, counted and listed; and, first among its notices,
        that the model stood by, since the stand-by ended its turn with no result."""
        sb = self.agent.stand_by
        if sb is None:
            return None
        if self._stood_at is not None:
            words, at = self._stood_at
            self.agent.notices.insert(
                0,
                f"You stood by until {words} at {at}; it is now {self.world.clock.stamp()}: "
                f"{reason or words}.",
            )
        start, stamp = self._wait_from
        lines = self._notable_since(start)
        return {"since": stamp, "until": sb.words, "notable": len(lines), "lines": lines}

    def interim(self) -> dict[str, Any] | None:
        """While the game has the floor (standing by, or waiting for the next sampling
        point after a reply): since when, until what, and the notable lines logged since
        the wait began, for a door to show a model that asked again (package 28c: a
        stand-by is a decision not to be sampled, not a decision to be blind). None while
        the model's turn is open, paused, released or not yet started."""
        a = self.agent
        if not self.started or a.released or a.paused or self._open is not None:
            return None
        start, stamp = self._wait_from
        lines = self._notable_since(start)
        return {
            "since": stamp,
            "until": a.stand_by.words if a.standing_by and a.stand_by is not None else None,
            "standing_by": a.standing_by,
            "notable": len(lines),
            "lines": lines,
        }

    def _resume_from_stand_by(self, reason: str) -> None:
        a = self.agent
        digest = self._stood_by_digest(reason.rstrip(".!"))
        a.state = STATIONED
        a.stand_by = None
        a.last_heard_tick = self.world.clock.tick
        self.world.record(
            Severity.ROUTINE,
            "agent.resumed",
            f"{self.mark} {reason[0].upper()}{reason[1:].rstrip('.!')}; the "
            f"{self.station.name} is sampled again.",
            actor=self.actor,
            data={"reason": reason},
        )
        self._sample(reason, stood_by=digest)

    # -- the sample --------------------------------------------------------------------

    def _build_sample(self, reason: str) -> Sample:
        world = self.world
        events = [world.log[i] for i in range(self._sample_seen, len(world.log))]
        self._sample_seen = len(world.log)
        mine = self.actor
        # the log as the captain reads it at the driver's compression: every line below the
        # roll-up's, and at or above it the kept lines and each closed hour in one line; an
        # hour not yet over is held for the sample after it closes, as the captain's view
        # holds it (spec M4 open item 8)
        compression = getattr(world, "compression", 1.0)
        kept: list[Event | Rollup] = []
        for e in events:
            if e.actor != mine:
                kept.extend(self._rollup.feed(e, compression))
        routine = [e for e in kept if e.severity is Severity.ROUTINE]
        omitted = max(0, len(routine) - SAMPLE_ROUTINE_LINES)
        drop = set(id(e) for e in routine[:omitted])
        lines = [_log_line(e) for e in kept if id(e) not in drop]
        a = self.agent
        sample = Sample(
            tick=world.clock.tick,
            stamp=world.clock.stamp(),
            reason=reason,
            log=lines,
            log_omitted=omitted,
            readings=tools.readings_words(world),
            question=a.question,
            notices=list(a.notices),
            word=a.word,
        )
        a.notices = []
        a.word = None  # carried once; no answer is owed (package 29, `tell`)
        return sample

    def _sample(self, reason: str, stood_by: dict[str, Any] | None = None) -> None:
        a = self.agent
        sample = self._build_sample(reason)
        sample.stood_by = stood_by
        a.last_sample_tick = self.world.clock.tick
        a.samples += 1
        if self.conversation:
            content = {"reason": reason, "question": sample.question, "notices": sample.notices}
            self.turns.append(Turn(DATA, {k: v for k, v in content.items() if v}))
        else:
            self.turns.append(Turn(DATA, sample.to_dict()))
        self._calls_this_sample = 0
        self._sample_had_words = False
        self._sample_repeated = False
        self._question_sent = sample.question
        self._open = sample
        self._poll()

    def _fold(self, reason: str) -> None:
        """A sampling point reached while the floor is the model's: what is new is folded
        into the open sample (the log lines appended, the readings replaced by the
        latest, the reason noted, a question added, the notices carried), and the same
        news goes into the conversation as a data turn marked `folded`, so the model's
        next turn carries everything since its last reply. The World does not wait."""
        o = self._open
        assert o is not None
        delta = self._build_sample(reason)
        self.agent.last_sample_tick = self.world.clock.tick
        o.log.extend(delta.log)
        o.log_omitted += delta.log_omitted
        routine = [ln for ln in o.log if ln["severity"] == Severity.ROUTINE.value]
        extra = len(routine) - SAMPLE_ROUTINE_LINES
        if extra > 0:  # the merged sample keeps the same cap, the most recent kept
            drop = set(id(ln) for ln in routine[:extra])
            o.log = [ln for ln in o.log if id(ln) not in drop]
            o.log_omitted += extra
        o.readings = delta.readings
        o.tick, o.stamp = delta.tick, delta.stamp
        o.reason = f"{o.reason}; then {reason}"
        # a question the open turn carries already is not put again: the fold holds what is
        # new, and the captain's question, still unanswered while the turn is open, is not
        # (playtest 7, finding 8: a fold made while the model was writing its answer carried
        # the question again, and the model, having answered, read it as asked once more)
        new_question = delta.question is not None and delta.question != self._question_sent
        if new_question:
            o.question = delta.question
            self._question_sent = delta.question
        if delta.word is not None:
            o.word = f"{o.word}\n{delta.word}" if o.word else delta.word
        o.notices.extend(delta.notices)
        content = delta.to_dict()
        if not new_question:
            content["question"] = None
        content["folded"] = FOLDED_WORDS
        self.turns.append(Turn(DATA, content))

    def _poll(self) -> None:
        """Ask the model for its reply to the open sample; take it if it has come."""
        if self._sampling:
            return
        if hasattr(self.model, "offered_tools"):
            # a door that sends tool definitions offers these and no others
            self.model.offered_tools = self.tool_names
        self._sampling = True
        try:
            while self._open is not None and not self.agent.released:
                reply = self.model.reply(self.turns)
                if reply is None:
                    return  # not yet: the sample stays open
                self._take_reply(reply)
        finally:
            self._sampling = False

    def deliver(self, reply: Reply) -> None:
        """Take a reply for the open sample from outside the model call."""
        if self._open is None:
            raise OrderError(f"The {self.station.name} has no sample open to answer.")
        self._sampling = True
        try:
            self._take_reply(reply)
        finally:
            self._sampling = False
        if self._open is not None:
            self._poll()

    def _take_reply(self, reply: Reply) -> None:
        world = self.world
        self.transcript.append(
            {"tick": world.clock.tick, "after_orders": len(world.journal), "reply": reply.to_dict()}
        )
        self.turns.append(Turn(MODEL, reply))
        # 1. the token, before anything else reads the reply
        for piece in reply.pieces():
            if OPT_OUT_TOKEN in piece:
                self.leave(_reason_after_token(reply, piece), how="the token")
                return
        # 2. the tool calls, in order, up to the budget
        results: list[dict[str, Any]] = []
        self._new_books = []
        stood = False
        for c in reply.calls:
            if self._calls_this_sample >= TOOL_CALLS_PER_SAMPLE:
                results.append(
                    {
                        "name": c.name,
                        "result": (
                            f"Not run: this sample's budget of {TOOL_CALLS_PER_SAMPLE} tool "
                            f"calls is spent; the rest of the calls wait for the next sample."
                        ),
                    }
                )
                break
            self._calls_this_sample += 1
            was_standing_by = self.agent.standing_by
            results.append({"name": c.name, "args": dict(c.args), "result": self._call(c)})
            if self._new_books and self._new_books[-1].slot is None:
                self._new_books[-1].slot = len(results) - 1
            if self.agent.released:
                return  # the token or opt_out: the turn and the station end here
            if (
                self.stand_by_ends_turn
                and c.name == "stand_by"
                and self.agent.standing_by
                and not was_standing_by
            ):
                # a stand-by taken ends the turn at once, at every door (package 28c,
                # playtest 4: the result "Standing by until a glass" and the model asked
                # again, which stood by again, thirteen times in a turn that never closed):
                # no result is returned, the model is not called again, and the calls after
                # it are not run; the sample that ends the stand-by says it stood by
                stood = True
                break
        # 3. the free text, under the mark
        text = " ".join(reply.text.split())
        if text:
            world.record(
                Severity.ROUTINE,
                "agent.note",
                f"{self.mark} {text}",
                actor=self.actor,
                data={"station": self.station.name},
            )
        if text or reply.calls:
            self._sample_had_words = True
        if stood:
            for b in self._new_books:
                b.state = UNSEEN  # its result never reached the model
            self._new_books = []
            self._end_sample()
            return
        if results and not self.agent.released:
            self.turns.append(Turn(DATA, {"tool_results": results}))
            self._place_books(len(self.turns) - 1)
            if self.conversation and any(
                r.get("name") == "answer" and "args" in r for r in results
            ):
                # a plain conversation's turn ends with its answer, at every door alike:
                # what follows (a follow-up, the developer's word, the record) is the
                # caller's, and a rebuilt conversation meets the same turns (package 28c)
                self._end_sample()
                return
            return  # the loop in `_poll` calls the model again with the results
        self._end_sample()

    def _call(self, c: ToolCall) -> Any:
        if self.allowed_tools is not None and c.name not in self.allowed_tools:
            only = " and ".join(self.tool_names) or "none"
            return (
                f"There is no tool named '{c.name}' in this conversation; the tools here "
                f"are {only}."
            )
        if c.name == "submit_order":
            self._note_submission(str(c.args.get("text", "")))
        result = tools.call(self.world, self.station.name, c.name, c.args)
        found = tools.book_of(c.name, c.args, result) if c.name in tools.BOOK_TOOLS else None
        if found is None:
            return result
        book = self._open_book(*found)
        self._new_books.append(book)
        return _with_handle(result, book)

    def _end_sample(self) -> None:
        self._open = None
        a = self.agent
        tick = self.world.clock.tick
        if a.released:
            return
        if not a.standing_by:  # a stand-by in this turn set the start already
            self._wait_from = (len(self.world.log), self.world.clock.stamp())
        if self._sample_had_words:
            a.last_heard_tick = tick
            if a.nudged_for == "silence":
                a.nudged_for = None
        else:
            heard = a.last_heard_tick if a.last_heard_tick is not None else tick
            if not a.standing_by and tick - heard >= self.station.patience_s:
                self._welfare_fire("silence")
                a.last_heard_tick = tick  # the next span is counted from the nudge
        if not self._sample_repeated and a.nudged_for == "repeat":
            # a sample after the nudge without the same order again: the matter ends (the
            # count itself is reset only by another order or a change in the readings,
            # since the detector counts submissions, not samples)
            a.nudged_for = None
        self._shelf_life()

    # -- the shelf (package 28d) ----------------------------------------------------------

    @property
    def keeps_its_own(self) -> bool:
        """The door's client keeps the model's conversation itself (MCP, the REPL)."""
        return self.door in DOORS_THAT_KEEP_THEIR_OWN

    def open_books(self) -> list[Book]:
        return [b for b in self.books if b.state == OPEN]

    def _open_book(self, title: str, reopen: str) -> Book:
        book = Book(
            len(self.books) + 1,
            title,
            reopen,
            self.world.clock.ship_time.strftime("%H:%M"),
            self.turns_ended,
        )
        self.books.append(book)
        return book

    def _place_books(self, at: int) -> None:
        """The books opened in the reply just taken now stand in the conversation, at the
        tool-results turn `at`; one shelved in the same reply is stubbed at once."""
        for b in self._new_books:
            b.at = at
            if b.state in (SHELVED, WENT_BACK):
                self._stub(b)
        self._new_books = []

    def _stub(self, b: Book) -> None:
        """The book's result in the conversation replaced by its line, a new turn in the
        old one's place (the old turn object is left as it was, for whoever holds it)."""
        if b.at is None or b.slot is None:
            return
        turn = self.turns[b.at]
        results = list(turn.content["tool_results"])
        entry = dict(results[b.slot])
        how = (
            f"it went back on the shelf after {number_words(SHELF_LIFE_TURNS)} of your turns"
            if b.state == WENT_BACK
            else "shelved"
        )
        entry["result"] = (
            f"You read {b.title}, at {b.opened}; {how} (book {b.number}). "
            f"{b.reopen} opens it again."
        )
        results[b.slot] = entry
        self.turns[b.at] = Turn(DATA, {**turn.content, "tool_results": results})
        self.revision += 1

    def _shelf_life(self) -> None:
        """At the end of each of the model's turns: a book open for `SHELF_LIFE_TURNS`
        turns after the one it was read in goes back, and the next sample says so."""
        self.turns_ended += 1
        for b in self.books:
            if b.state != OPEN or b.at is None:
                continue
            if self.turns_ended - b.turn > SHELF_LIFE_TURNS:
                b.state = WENT_BACK
                self._stub(b)
                self.agent.notices.append(self._went_back_words(b))

    def _went_back_words(self, b: Book) -> str:
        n = number_words(SHELF_LIFE_TURNS)
        again = f"{b.reopen} opens it again, under a new number."
        if self.keeps_its_own:
            return (
                f"Book {b.number} ({b.title}) went back on the shelf after {n} of your turns: "
                "the game will not show its pages to you again, though your client keeps its "
                f"own copy of the conversation. {again}"
            )
        return (
            f"Book {b.number} ({b.title}) went back on the shelf after {n} of your turns: "
            f"your conversation holds its line and not its pages. {again}"
        )

    def shelve(self, words: str = "") -> str:
        """`shelve(book)`: a handle ("book 7", "7"), a topic's words ("primer 3", which
        puts back every open book whose name holds them), or nothing for every open book.
        The shelved books' results are replaced by their lines at once, so the model's
        next request carries the lines only."""
        key = " ".join(str(words or "").lower().split()).strip(" .'\"")
        open_now = self.open_books()
        if key in ("", "all", "every book", "all books", "everything"):
            chosen = open_now
            if not chosen:
                return "No book is open; nothing was shelved."
        else:
            number = key.removeprefix("book").strip().lstrip("#")
            if number.isdigit():
                b = next((x for x in self.books if x.number == int(number)), None)
                if b is None:
                    return f"There is no book {number}; {self._open_words(open_now)}"
                if b.state == ASIDE:
                    return self._aside_words(b)
                if b.state != OPEN:
                    return f"Book {b.number} ({b.title}) is on the shelf already."
                chosen = [b]
            else:
                chosen = [b for b in open_now if key in b.title.lower()]
                if not chosen:
                    return f"No open book is called '{words}'; {self._open_words(open_now)}"
        for b in chosen:
            b.state = SHELVED
            self._stub(b)  # a book opened in this same reply is stubbed when it is placed
        names = "; ".join(b.named for b in chosen)
        if self.keeps_its_own:
            return (
                f"Shelved: {names}. The game will not show those pages to you again. This "
                "door's client keeps its own copy of the conversation, so the game cannot take "
                "the pages out of it; your journal is the place for what you took from them. "
                "Any book opens again with its call, under a new number."
            )
        return (
            f"Shelved: {names}. From your next request on, your conversation holds each "
            "book's line and not its pages; your journal is the place for what you took from "
            "them. Any book opens again with its call, under a new number."
        )

    def _open_words(self, open_now: list[Book]) -> str:
        if not open_now:
            return "no book is open."
        return "the open books: " + "; ".join(b.named for b in open_now) + "."

    def _aside_words(self, b: Book) -> str:
        client = (
            " Your client keeps its own copy of the conversation." if self.keeps_its_own else ""
        )
        return (
            f"Book {b.number} ({b.title}) was read while the game had the floor, so the game "
            f"keeps no copy of its pages and there is nothing of it to shelve.{client}"
        )

    def aside(self, c: ToolCall) -> Any:
        """A read-only tool, or `shelve`, called while the game has the floor (a door's
        call out of turn, `remote.Desk`). A read that is a book gets a handle, and the
        read and a shelve are recorded as acts from outside the loop, so a replay numbers
        and shelves the same (`door_act`)."""
        if c.name == "shelve":
            unknown = [k for k in c.args if k != "book"]
            if unknown:
                return tools.call(self.world, self.station.name, c.name, c.args)
            return self.door_act("shelve", str(c.args.get("book") or ""), "out of turn")
        result = tools.call(self.world, self.station.name, c.name, c.args)
        found = tools.book_of(c.name, c.args, result) if c.name in tools.BOOK_TOOLS else None
        if found is None:
            return result
        book = self.door_act("read", *found)
        return result if book is None else _with_handle(result, book)

    # -- welfare -----------------------------------------------------------------------

    def _note_submission(self, text: str) -> None:
        a = self.agent
        key = " ".join(text.lower().split())
        digest = tools.readings_digest(self.world)
        if key == a.repeat_text and digest == a.repeat_digest:
            a.repeat_count += 1
        else:
            a.repeat_text, a.repeat_digest, a.repeat_count = key, digest, 1
        if a.repeat_count >= WELFARE_REPEAT_N:
            self._sample_repeated = True
            self._welfare_fire("repeat")

    def _welfare_fire(self, pattern: str) -> None:
        """The detector fired: nudge the first time, pause if the pattern goes on."""
        a = self.agent
        world = self.world
        if pattern == "repeat":
            seen = (
                f"the same order ({a.repeat_text!r}) {a.repeat_count} times with no change "
                f"in the readings"
            )
            nudge = NUDGE_REPEAT.format(n=a.repeat_count, token=OPT_OUT_TOKEN)
        else:
            span = _span_words(self.station.patience_s)
            seen = f"no reply for {span}"
            nudge = NUDGE_SILENCE.format(span=span, token=OPT_OUT_TOKEN)
        if a.nudged_for != pattern:
            a.nudged_for = pattern
            a.notices.append(nudge)
            world.record(
                Severity.ROUTINE,
                "agent.nudged",
                f"The {self.station.name} nudged: {seen}.",
                actor=self.actor,
                data={"pattern": pattern, "seen": seen},
            )
            self.journal.append(world, f"Nudged by the harness: {seen}.", kind="agent.nudged")
            return
        self.pause(f"{seen} after a nudge")

    def pause(self, reason: str) -> None:
        a = self.agent
        world = self.world
        a.state = PAUSED
        a.paused_tick = world.clock.tick
        a.pause_reason = reason
        a.notices.append(
            "The harness paused your sampling and asked the human present whether to "
            "continue; you were not stopped."
        )
        world.record(
            Severity.NOTABLE,
            "agent.paused",
            f"The {self.station.name} is paused: {reason}. Continue, stand down, or leave "
            f"paused? Say 'resume the {self.station.name}' or 'stand down the "
            f"{self.station.name}'.",
            actor=self.actor,
            data={"reason": reason, "question": "continue, stand down, or leave paused?"},
        )
        self.journal.append(world, f"Paused by the harness: {reason}.", kind="agent.paused")

    def resume(self, by: str = "the captain") -> str:
        """`resume the <station>`: the human's answer to a pause."""
        a = self.agent
        if a.released:
            raise OrderError(
                f"The {self.station.name}'s station was released; {a.released_reason}."
            )
        if not a.paused:
            raise OrderError(f"The {self.station.name} is not paused; it is {a.words()}.")
        a.state = STATIONED
        a.paused_tick = None
        a.pause_reason = ""
        a.nudged_for = None
        a.repeat_text, a.repeat_digest, a.repeat_count = None, None, 0
        a.last_heard_tick = self.world.clock.tick
        self._paused_real = None
        a.notices.append(f"{by[0].upper()}{by[1:]} resumed your sampling.")
        text = f"The {self.station.name} resumed by {by}."
        self.world.record(
            Severity.ROUTINE, "agent.resumed", text, actor=self.actor, data={"by": by}
        )
        return text

    def check_unattended(self, now: float | None = None) -> bool:
        """The driver's half of the unattended bound: called from the driver's own clock
        with its monotonic time; stands the agent down when a pause has gone unanswered
        for `WELFARE_UNATTENDED_REAL_S`. Returns True when it did."""
        a = self.agent
        if not a.paused:
            self._paused_real = None
            return False
        now = time.monotonic() if now is None else now
        if self._paused_real is None:
            self._paused_real = now
            return False
        if now - self._paused_real >= WELFARE_UNATTENDED_REAL_S:
            self.door_act(
                "stand_down",
                f"paused ({a.pause_reason}) and nobody answered within ten minutes",
                "the harness",
            )
            return True
        return False

    def door_act(self, act: str, reason: str, by: str) -> Any:
        """A stop that comes from outside the loop, which a replay could not otherwise
        know of: a door's release (the door closed, the client went away, Ctrl-C), the
        token sent out of turn, the driver's ten real minutes. It is recorded in the
        transcript at this tick and count of orders, so that a replay makes it again at
        the same point (`Playback`), and then made: `act` is "leave" (the opt-out, `by`
        saying how), "stand_down" (`by` saying who) or "speak" (the model's own word
        while the game has the floor, `reason` its words; `own_word`), "read" (a book
        read out of turn: `reason` its title, `by` the call that reads it again; returns
        the book) or "shelve" (out of turn: `reason` the words; returns the answer)."""
        if self.agent.released:
            return None
        world = self.world
        self.transcript.append(
            {
                "tick": world.clock.tick,
                "after_orders": len(world.journal),
                "door": act,
                "reason": reason,
                "by": by,
            }
        )
        if act == "leave":
            self.leave(reason, how=by)
        elif act == "speak":
            self.own_word(reason)
        elif act == "read":
            book = self._open_book(reason, by)
            book.state = ASIDE
            return book
        elif act == "shelve":
            return self.shelve(reason)
        else:
            self.stand_down(reason, by=by)
        return None

    def _play_door_acts(self) -> None:
        """A replay makes the recorded stops from outside the loop at their points."""
        m = self.model
        if not isinstance(m, Playback):
            return
        while not self.agent.released:
            e = m.next_act()
            if e is None:
                return
            self.door_act(str(e["door"]), str(e.get("reason", "")), str(e.get("by", "")))

    # -- the agent's own actions (through the tools) --------------------------------------

    def stand_by(self, until: str) -> str:
        words = " ".join(str(until).lower().split()).strip(" .!?")
        for lead in ("until ", "till ", "for "):
            words = words.removeprefix(lead)
        # 'strain warning', 'the next strain warning', 'strain warnings': the event's words
        for said in (words, words.removeprefix("the next "), words.rstrip("s")):
            for article in ("", "a ", "an "):
                if words not in R.EVENTS and article + said in R.EVENTS:
                    words = article + said
        world = self.world
        if words in R.EVENTS:
            spec = R.EVENTS[words]
            if spec.absent:
                return f"{spec.absent} Stand by for a bell or another event instead."
            sb = StandBy(words, event=words)
        elif words in STAND_BY_SEVERITIES:
            sb = StandBy(words, severity=STAND_BY_SEVERITIES[words])
        elif words in R.INTERVALS:
            sb = StandBy(words, until_tick=world.clock.tick + R.INTERVALS[words])
        else:
            seconds = _duration(words)
            if seconds is None:
                events = ", ".join(w for w, s in R.EVENTS.items() if not s.absent)
                return (
                    f"'{until}' is not an event or an interval to stand by for. The events: "
                    f"{events}; or 'a notable event', 'an urgent event'. The intervals: a "
                    f"glass, an hour, a watch, or minutes ('5 minutes', 'ten minutes')."
                )
            words = f"{words} {'has' if seconds <= 60 else 'have'} passed"
            sb = StandBy(words, until_tick=world.clock.tick + seconds)
        a = self.agent
        a.state = STANDING_BY
        a.stand_by = sb
        a.last_heard_tick = world.clock.tick
        world.record(
            Severity.ROUTINE,
            "agent.stood_by",
            f"{self.mark} Standing by until {words}.",
            actor=self.actor,
            data=sb.to_dict(),
        )
        self._wait_from = (len(world.log), world.clock.stamp())
        self._stood_at = (words, world.clock.stamp())
        self.journal.append(world, f"Stood by until {words}.", kind="agent.stood_by")
        # standing by is the answer to a nudge (spec §11)
        a.nudged_for = None
        a.repeat_text, a.repeat_digest, a.repeat_count = None, None, 0
        self._sample_repeated = False
        return f"Standing by until {words}; you will be sampled then."

    def answer(self, text: str) -> str:
        text = " ".join(str(text).split())
        if not text:
            return "An answer needs some words."
        a = self.agent
        question = a.question
        a.question = None
        self.world.record(
            Severity.NOTABLE,
            "agent.said",
            f"{self.mark} {text}",
            actor=self.actor,
            data={"question": question, "station": self.station.name},
        )
        return "Heard." if question is not None else "Heard, though nothing was asked."

    def own_word(self, text: str) -> None:
        """The model speaks while the game has the floor (through `door_act`, so that a
        replay speaks at the same point): its words go in the log under the mark; a
        stand-by ends as its own decision, logged and journaled; and it is sampled now,
        the sample carrying the stand-by's digest. Refused silently when there is no
        floor to take (a turn open, paused, released): the doors check first."""
        a = self.agent
        world = self.world
        if a.released or a.paused or self._open is not None or not self.started:
            return
        text = " ".join(str(text).split())
        if text:
            world.record(
                Severity.ROUTINE,
                "agent.note",
                f"{self.mark} {text}",
                actor=self.actor,
                data={"station": self.station.name, "own_word": True},
            )
        a.last_heard_tick = world.clock.tick
        digest = None
        if a.standing_by and a.stand_by is not None:
            digest = self._stood_by_digest("your own word")
            until = a.stand_by.words
            a.state = STATIONED
            a.stand_by = None
            world.record(
                Severity.ROUTINE,
                "agent.resumed",
                f"{self.mark} The {self.station.name} ends its stand-by (until {until}) at its "
                f"own word; it is sampled again.",
                actor=self.actor,
                data={"reason": "its own word", "until": until},
            )
            self.journal.append(
                world, f"Ended the stand-by until {until} at my own word.", kind="agent.resumed"
            )
        self._sample("its own word", stood_by=digest)

    def close_turn(self) -> None:
        """A plain conversation's caller ends the model's open turn (a door that answers
        late, after an `answer` call whose result it has) so that the next thing can be
        put: the consent step's follow-up, or the developer's turn after the answer."""
        if self.conversation and self._open is not None and not self.agent.released:
            self._end_sample()

    def put(self, text: str, reason: str) -> None:
        """A plain conversation's next turn (the consent step): `text` is put to the model
        as the sample's `question`, with `reason` saying what it is, and the model is
        asked for its reply at once. For a conversation, where no World ticks."""
        if self.agent.released:
            raise OrderError(f"The {self.station.name} conversation is over.")
        if self._open is not None:
            raise OrderError(f"The {self.station.name} has a turn open; take its reply first.")
        self.agent.question = " ".join(text.split())
        self._sample(reason)

    def put_question(self, question: str) -> str:
        """`ask the <station> <question>`: the question is answered at this tick, after
        the order is logged (`on_order`)."""
        a = self.agent
        question = " ".join(question.split()).rstrip("?")
        if not question:
            raise OrderError(f"Ask the {self.station.name} what? Say the question after the name.")
        if a.released:
            raise OrderError(
                f"There is no {self.station.name} at the station now; {a.released_reason}."
            )
        if a.paused:
            raise OrderError(
                f"The {self.station.name} is paused ({a.pause_reason}); say 'resume the "
                f"{self.station.name}' first."
            )
        a.question = question
        return f"Asked the {self.station.name}: {question}?"

    def put_word(self, words: str) -> str:
        """`tell the <station> <words>` (package 29, the owner's tenth item): the words go
        to the model in its next sample under `word`, not `question`: no answer is owed,
        and nothing that waits on a question is set by them. The sample is taken at the
        next tick (so that an `ask` given at once after rides in the same sample); a
        stand-by is woken by it, a turn already open has it folded in."""
        a = self.agent
        words = " ".join(str(words).split())
        if not words:
            raise OrderError(f"Tell the {self.station.name} what? Say the words after the name.")
        if a.released:
            raise OrderError(
                f"There is no {self.station.name} at the station now; {a.released_reason}."
            )
        if a.paused:
            raise OrderError(
                f"The {self.station.name} is paused ({a.pause_reason}); say 'resume the "
                f"{self.station.name}' first."
            )
        a.word = f"{a.word}\n{words}" if a.word else words
        return f"The captain to the {self.station.name}: {words}"

    # -- release -----------------------------------------------------------------------

    def request_stand_down(self, reason: str, by: str = "the captain") -> str:
        """`stand down the <station>`: carried out after the order is journaled."""
        if self.agent.released:
            raise OrderError(
                f"The {self.station.name}'s station is released already; "
                f"{self.agent.released_reason}."
            )
        self._stand_down_requested = (reason, by)
        return f"Standing down the {self.station.name}."

    def stand_down(self, reason: str, by: str = "the captain") -> None:
        """Journal `agent.stopped` with the reason, release the station, save. The save
        comes last so that the file holds the exit: the journal entry, the log line and
        the released station (package 28; the owner reads the journal in the save)."""
        if self.agent.released:
            return
        text = f"The {self.station.name} stood down by {by}: {reason}. The game is saved."
        self.journal.append(self.world, f"Stood down by {by}: {reason}.", kind="agent.stopped")
        self.world.record(
            Severity.NOTABLE,
            "agent.stopped",
            text,
            actor=self.actor,
            data={"reason": reason, "by": by},
        )
        self._release(f"stood down by {by}: {reason}")
        self._save(f"the {self.station.name} stood down: {reason}")

    def leave(self, reason: str, how: str = "the token") -> None:
        """The opt-out: journal `agent.opted_out`, release, save, end the loop (the save
        last, so that the file holds the exit)."""
        if self.agent.released:
            return
        reason = " ".join(reason.split())
        why = f": {reason}" if reason else ", giving no reason"
        self.journal.append(self.world, f"Left the game by {how}{why}.", kind="agent.opted_out")
        self.world.record(
            Severity.NOTABLE,
            "agent.opted_out",
            f"The {self.station.name} has left the game by {how}{why}. The game is saved and "
            f"the station is released.",
            actor=self.actor,
            data={"reason": reason, "how": how},
        )
        self._release(f"left the game{why}")
        self._save(f"the {self.station.name} opted out")

    def _release(self, reason: str) -> None:
        a = self.agent
        a.state = RELEASED
        a.released_reason = reason
        a.released_tick = self.world.clock.tick
        a.question = None
        a.stand_by = None
        self._open = None

    def _save(self, reason: str) -> None:
        if self.save_fn is not None:
            self.last_save = self.save_fn(self.world, reason)
        else:
            self.last_save = self.world.save()

    # -- save and restore --------------------------------------------------------------

    def save(self) -> dict[str, Any]:
        a = self.agent
        return {
            "station": self.station.save(),
            "session_kind": a.session_kind,
            "door_note": self.door_note,
            "stationed_tick": a.stationed_tick,
            "stationed_after_orders": self._start_after_orders,
            "state": a.state,
            "state_words": a.words(),
            "last_sample_tick": a.last_sample_tick,
            "model_name": self.model_name,
            "door": self.door,
            "stand_by_ends_turn": self.stand_by_ends_turn,
            "transcript": list(self.transcript),
        }

    def snapshot(self) -> dict[str, Any]:
        """For `queries.snapshot`: the station, its state, when it was last sampled, and
        the question a pause puts to the human."""
        a = self.agent
        return {
            "station": self.station.name,
            "state": a.state,
            "words": a.words(),
            "last_sampled": a.last_sample_tick,
            "policy": self.policy.describe(),
            "question": (
                f"the {self.station.name} is paused: continue, stand down, or leave paused?"
                if a.paused
                else None
            ),
        }


class Playback(Transcript):
    """A restored station's recorded transcript, played back where it was recorded: each
    reply is given once the World has reached the tick it was taken at and the count of
    journaled orders it was taken after (a live door's reply comes between ticks, after
    any orders of its tick given before it), and each stop from outside the loop
    (`Harness.door_act`) is made at its own point. An entry without the count (the
    transcripts of packages 27 and 28, each taken at its own sample) is given as soon as
    its tick is reached, which is where it was taken. `None` while nothing is due."""

    def __init__(self, world: World, entries: list[dict[str, Any]]):
        super().__init__([Reply.from_dict(e["reply"]) for e in entries if "reply" in e])
        self.world = world
        self.entries = list(entries)
        self.at = 0  # the next entry

    def _due(self, e: dict[str, Any]) -> bool:
        w = self.world
        tick = int(e.get("tick") or 0)
        return w.clock.tick >= tick and len(w.journal) >= int(e.get("after_orders") or 0)

    def reply(self, turns: Any) -> Reply | None:
        if self.at >= len(self.entries):
            return None
        e = self.entries[self.at]
        if "reply" not in e or not self._due(e):
            return None
        self.at += 1
        self.calls += 1
        return Reply.from_dict(e["reply"])

    def next_act(self) -> dict[str, Any] | None:
        """The next stop from outside the loop, when it is the next entry and is due."""
        if self.at >= len(self.entries):
            return None
        e = self.entries[self.at]
        if "door" not in e or not self._due(e):
            return None
        self.at += 1
        return e

    @property
    def spent(self) -> bool:
        return self.at >= len(self.entries)


def restore(world: World, data: dict[str, Any], model: Model | None = None) -> list[Harness]:
    """Station the agents a save describes, for a replay or a load: each with a
    `Playback` of its recorded transcript (or `model`, when the caller has a live one
    to continue with), started when the World reaches its stationed tick. The journals
    in the save are restored as they were; a replay writes the same entries again, so
    the restored journal is replaced by the replayed one entry for entry."""
    out: list[Harness] = []
    for record in data.get("agents") or []:
        station = Station.load(record["station"])
        h = Harness(
            world,
            station,
            model or Playback(world, list(record.get("transcript") or [])),
            session_kind=str(record.get("session_kind", SESSION_TEST)),
            door_note=str(record.get("door_note", "")),
            start_at=int(record.get("stationed_tick") or 0),
            start_after_orders=int(record.get("stationed_after_orders") or 0),
        )
        h.model_name = str(record.get("model_name") or "")
        h.door = str(record.get("door") or "")
        h.stand_by_ends_turn = bool(record.get("stand_by_ends_turn", model is not None))
        if h._start_at <= world.clock.tick and len(world.journal) >= h._start_after_orders:
            h.start()
        out.append(h)
    return out


def _reason_after_token(reply: Reply, found_in: str) -> str:
    """The reason the model gave: what follows the token. The scan reads the raw output
    (a door's serialised calls included); the reason is read from the plainest piece that
    holds the token, the text or an argument, so that a served call's JSON punctuation is
    not taken for words."""
    for p in [reply.text, *(str(v) for c in reply.calls for v in c.args.values())]:
        if OPT_OUT_TOKEN in p:
            found_in = p
            break
    return found_in.split(OPT_OUT_TOKEN, 1)[1].strip(" .:;,-\n")


def _with_handle(result: Any, book: Book) -> Any:
    """A book's result with its handle first: a page's line above its text, a log read's
    `book` key first among its keys."""
    if isinstance(result, dict):
        return {"book": book.handle, **result}
    return f"{book.handle}\n{result}"


def conversation_text(content: dict[str, Any]) -> str | None:
    """A plain conversation's data turn as the words a door shows: the notices, then
    what is put to the model; `None` for any other data turn (a sample, tool results),
    which a door sends as data."""
    if "tool_results" in content or "readings" in content or "log" in content:
        return None
    parts = [str(n) for n in content.get("notices") or []]
    if content.get("question"):
        parts.append(str(content["question"]))
    return "\n\n".join(parts)


def _log_line(x: Event | Rollup) -> dict[str, Any]:
    """A shown line as the model sees it (`tools.log_line`); a roll-up with its hour."""
    if isinstance(x, Rollup):
        return {
            "tick": x.tick,
            "stamp": x.stamp,
            "severity": x.severity.value,
            "kind": x.kind,
            "text": x.text,
        }
    return tools.log_line(x)


def _duration(words: str) -> int | None:
    """An interval in the dialect's duration words ('5 minutes', 'ten minutes', 'two
    hours', 'half an hour'; `standing.grammar.parse_duration`), in seconds, or None."""
    from freesail.orders.vocabulary import normalise
    from freesail.standing.grammar import parse_duration

    try:
        return parse_duration(normalise(words).split())
    except OrderError:
        return None


def _span_words(seconds: int) -> str:
    if seconds == R.INTERVALS["a watch"]:
        return "a watch"
    if seconds == R.INTERVALS["an hour"]:
        return "an hour"
    if seconds == R.INTERVALS["a glass"]:
        return "a glass"
    if seconds % 60 == 0:
        return f"{seconds // 60} minutes"
    return f"{seconds} seconds"
