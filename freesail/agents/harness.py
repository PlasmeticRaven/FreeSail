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
the human through the log and the snapshot; only with no answer within ten real minutes
(`WELFARE_UNATTENDED_REAL_S`), however fast the ship's clock runs, does it **stand the
agent down** (save, `agent.stopped`, release). The minutes are the driver's, on its own
monotonic clock, which every driver reports through `check_unattended`: the browser
server's clock loop and the console's, running or stopped, and the REPL's. (Until package
31c a watch of ship's time stood the agent down too, whichever came first; at 300x a watch
is under a minute of real time, so the human never had the ten minutes the consent brief
promises: the owner's ruling of 2026-09-30.)
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

Package 31c (playtest 11). The weather's events that are the readings' changes (`a wind
shift`, `the glass falling fast`, `the glass turning`, `the sea getting up`;
`readings.EventSpec.watch`) are watched once a tick through the condition the standing
orders use (`standing.rules.event_condition`), so a stand-by and an `at` order cannot
disagree. **Nothing stood by for is skipped**: a stand-by is measured from the model's
*horizon*, what it had been shown when it made the call (the sample its turn opened with,
or the latest sample or fold before its last tool results; `_horizon`), so a bell, an
event or a reading's change that came after that and before the stand-by reached the
game wakes it at once, named so (`_in_flight`). A stand-by a door asks for while the
game has the floor is taken from then (`door_act` "stand_by"), and the journal is written
out of turn (`door_act` "journal"), the stand-by going on through it; both are recorded
for the replay.

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
not. **What is new of the readings** (package 31c; playtest 11's finding 1, spec M4 §24
item 9): a conversation's first sample carries every reading, and every later sample and
fold only those changed since the turn before it, with the sails in one line
(`tools.sail_line`) when any has changed (`_as_told`); the merged sample keeps every
reading, and the readings tool gives every row, so nothing is withheld, only not
repeated. Silence is judged on ship's time as before: a floor held with no reply for the
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

import dataclasses
import json
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from freesail.agents import tools
from freesail.agents.agent import (
    A_GLASS_S,
    A_WATCH_S,
    BOOK_SIZE_TOKENS,
    BRIEF_LOG_LINES,
    GENERAL_KEPT_BACK_WORDS,
    GENERAL_WITHIN_WORDS,
    LEAVING_WORDS,
    OFFICER,
    OFFICER_BRIEF,
    OPT_OUT_TOKEN,
    OPTED_OUT,
    ORDERS_PER_TURN,
    PAUSED,
    READS_PER_TURN,
    RELEASED,
    SESSION_TEST,
    SHELF_LIFE_TURNS,
    STANDING_BY,
    STATIONED,
    STOOD_DOWN,
    WATCHER_BRIEF,
    AgentState,
    Brief,
    Grant,
    Leaving,
    SamplingPolicy,
    StandBy,
    Station,
    domain_of,
    door_words,
    number_words,
    ordinal_words,
)
from freesail.agents.fake import Transcript
from freesail.agents.journal import HANDOVER_KIND, WORD_PASSED_KIND, Journal
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
    "ALWAYS_RUN_TOOLS",
    "ANSWER_UNASKED",
    "BUDGET_FREE_TOOLS",
    "DANGER_WORD_N",
    "HANDOVER_AT_FRACTION",
    "HANDOVER_KEEP_TURNS",
    "HANDOVER_RESERVE_SHARE",
    "HANDOVER_RESERVE_TOKENS",
    "IN_FLIGHT",
    "ORDER_TOOLS",
    "READINGS_ARE",
    "READS_PER_SAMPLE",
    "Book",
    "Playback",
    "SAMPLE_ROUTINE_LINES",
    "STAND_BY_WITH_DECK_MAX_S",
    "Seating",
    "TOOL_CALLS_PER_SAMPLE",
    "WELFARE_CONTRARY_N",
    "WELFARE_REPEAT_N",
    "WELFARE_UNATTENDED_REAL_S",
    "Harness",
    "SaveFn",
    "barred",
    "conversation_text",
    "full_stop",
    "restore",
    "seating",
]

# The turn's budget (package 37g, item 2; the reasons and the sources are beside the
# constants in `agent.py`). The orders one sampling point may give, stated in the brief
# as a budget and never a rule of conduct: sixteen by default, the station's own setting
# (`Station.orders_per_turn`); and the other counted calls, the reads and the notes,
# counted apart so that no page read costs an order. A fold into an open turn is a
# sampling point, and both counts begin again at it (a turn held open at the MCP door
# through several glasses had eight calls in all).
TOOL_CALLS_PER_SAMPLE = ORDERS_PER_TURN
READS_PER_SAMPLE = READS_PER_TURN

# The tools that are orders, counted against the station's orders.
ORDER_TOOLS = ("submit_order",)

# The tools the budget does not count, always run however many calls came before
# (package 29c, playtest 8: the model's `answer` was its ninth call, after six library
# reads, a journal note and a shelve, and the captain's answer came a sample late). `say`
# is the MCP door's; it reaches the harness as a reply's text, which is never counted.
BUDGET_FREE_TOOLS = ("answer", "say")

# ...and the ways of closing the turn and of leaving (package 37g; the review's 5.4: a
# spent budget refused `stand_by`, so the turn could not be closed, and `opt_out` and
# `hand_over`, so the leaving tool could be refused; `docs/agents/README.md` commitment
# 2). These always run, whatever came before.
ALWAYS_RUN_TOOLS = ("opt_out", "stand_down", "hand_over", "stand_by")

# What `answer` returns when no question was pending (package 30b, playtest 10's finding 3:
# "Heard, though nothing was asked" was read as the answer refused and lost). The words
# reached the log, and the result says so.
ANSWER_UNASKED = "Heard; your words are in the log, though no question was put."

# The calls that ran before a stand-by in the same reply are named in one line of the
# sample that ends the stand-by (package 30b, playtest 10's finding 4: a journal note
# before a `stand_by` was believed not to have run, since a stand-by ends the turn and
# returns no results). Each is named with its result, cut to this many characters; the
# tools that read (a page, the log, the readings) are named without it, since the
# sample carries the news and a book is opened again on request.
RAN_RESULT_CHARS = 100
READING_TOOLS = ("library", "read_log", "readings", "state", "read_journal")

# A reply whose free text opens with a thinking tag, closed or not, is the model's
# thinking leaked into its reply and not a line a sailor said (package 29c, playtest 9:
# 1,500 words opening `<thought` went into the log as one line). The tag only decides,
# the owner's ruling: a long reply is not a fault on its own. The fault is journaled with
# the first line, at most this many characters of it, and the reply's length.
THOUGHT_TAG = re.compile(r"\s*<\s*(?:thinking|think|thought)\b", re.IGNORECASE)
THOUGHT_FIRST_LINE_CHARS = 120

# The same order this many times with no change in the readings between (spec §11).
WELFARE_REPEAT_N = 3

# The welfare detector of a station with authority (package 37; the cold review's second
# item): the repeat detector cannot fire for an officer whose orders change the readings,
# so the pattern judged is orders that undo one another (set, take in, set). The harness
# keeps the station's own orders over the last watch of ship's time and counts the chain
# at their end in which each order undoes the one before it on a part they share
# (`standing.runtime.undo_chain`; what undoes what is data, `undoes:` in
# `data/vocabulary.yaml`); this many bring the nudge (the same number as the repeats',
# spec §11), the chain going on after it the pause.
#
# Package 37g, item 5, replaced the rule this began with: "each contrary to the one
# before it on a shared part" by the standing orders' conflict rule, with drift ("steer
# 90, 92, 95") counted as contrary. In the nine games of gate 5c's playtests that rule
# spoke 42 times and was right twice by its own lights (the review, 5.4 and 10.5); one of
# the 42 was a pause, in the Goulet, three minutes after the Mingan passed at a cable and
# a quarter, for "steer NE; steer 53; steer ENE; steer NE by E". Altering the course is
# conning and is never counted now, nor is the next thing after the last (heave to, fill
# away, steer); every one of the 42 recorded chains is silent by the new rule
# (`tests/test_officer.py`). The constants keep their names, which the saves and the
# documents use.
WELFARE_CONTRARY_N = 3
WELFARE_CONTRARY_WINDOW_S = A_WATCH_S

# The way out of danger (package 37g, item 19): an order given on the officer's own word
# to avoid an immediate danger, used this many times within a watch, brings the detector's
# word (judgement: the repeats' three; a danger met by the helm, a heave-to and an anchor
# is three orders, and a fourth cry of danger in one watch is worth a word either way).
DANGER_WORD_N = 3

# A station with the deck stands by until an event or a bell, never for longer: the
# longest interval it may name (package 37; the cold review's third item: "a captain that
# stands by is a ship with no one on deck"). A glass, the bell's own span (judgement).
STAND_BY_WITH_DECK_MAX_S = A_GLASS_S

# The handover note (spec M4 open item 9b; package 37, the cold review's fourth item):
# when a door has said what context it gives the model (the local runner's; Claude
# through Desktop keeps its own window and is not asked), the harness asks for the note
# once the conversation since the brief reaches this fraction of it (judgement: well
# under the point at which the runner leaves out the oldest turns, which is the context
# less the reply budget and the tool definitions, so the note is written before anything
# is lost), and asks again when it has grown by another tenth without one.
HANDOVER_AT_FRACTION = 0.6
HANDOVER_ASK_AGAIN_FRACTION = 0.1
# The threshold as a reserve of the door's context (package 37g, item 8, as package 37i
# amends it): the harness asks for the note when the conversation has left less than the
# reserve, and never earlier than the fraction above (which is already the most a context
# of 32,000 bears). 37g made the reserve 14,000 tokens; game 10 (the review of gate 5c,
# G15) showed that at 102,400 it left the ask to 88,400 by the four-character count while
# the server's own count stood far nearer the ceiling, and both seatings ended when the
# server refused the conversation for its size. So the default is a share (package 37i,
# item 3): three tenths, the room for two of game 10's largest samples (25,654
# characters, about 7,300 tokens by the server's count) with the reply budget (4,096) and
# the tool definitions (about 2,200), at 102,400 the review's stopgap of 30,000 (30,720),
# and between the six tenths game 7 ran 31 hours on and 37g's 0.86; and never less than
# 37g's 14,000 (`HANDOVER_RESERVE_TOKENS`: the reply budget, the tool definitions and
# the 8,000 the review's reader measured as comfortable for the sample, the reading and
# the note), the larger of the two, since three tenths of a small context leave less
# (at 32,768, 9,830: the review's 3,500 of room after the reply and the tools, under its
# least of 4,000). At 65,536 the ask comes at 45,875 and at 102,400 at 71,680; below
# about 35,000 the six tenths govern, as they did before 37g. The local runner's
# `--handover-reserve` sets it for a seating, as tokens or as a share (sent as tokens);
# it is asked again when the conversation has grown by a quarter of the reserve without
# a note. The conversation is measured by the server's own count where the door gives it
# (`Reply.served_tokens`; package 37i, item 2), else by the four-character rule.
HANDOVER_RESERVE_SHARE = 0.3
HANDOVER_RESERVE_TOKENS = 14000
# The turns kept whole after the note, besides the brief (judgement: the last two
# exchanges, a sample and its reply with their results, so that the note and the turn in
# hand are both before the model).
HANDOVER_KEEP_TURNS = 6

# Nobody answered the pause within ten real minutes, however fast the ship's clock runs
# (spec §11; the owner's ruling of 2026-09-30, package 31c: the watch of ship's time that
# came first at a high compression is retired); the driver measures the minutes on its own
# clock and reports them through `check_unattended`.
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
# The nudge of a station with authority (package 37; the rule as package 37g has it):
# orders within the watch that undo one another.
NUDGE_CONTRARY = (
    "You have given {n} orders within the watch each undoing the one before it on "
    "{where} ({orders}). You may continue, stand by until an event or a bell, or leave "
    "with the token {token}."
)
# ...and the way out of danger used three times in a watch (package 37g, item 19): a word
# and never a pause, since a station that is avoiding a danger is not to be stopped in it.
NUDGE_DANGER = (
    "You have given {n} orders within the watch on your own word to avoid an immediate "
    "danger ({orders}). The harness says so and does no more: you are not paused for it, "
    "and the way stays open to you while a danger lasts. The captain reads each of them in "
    "the log; tell him what the danger is if he has not answered it. You may continue, or "
    "leave with the token {token}."
)
# What a nudge that travels with an order's result opens with (package 37g: the nudge is
# in the result of the order that caused it, not a sample later, so that the pause can
# never come before the word has been read).
NUDGE_WITH_RESULT = "A word from the harness, with this result: "
# What the calls not run are told (package 37g, item 2): which count is spent, and what
# still runs, in words that name only the tools this door has.
NOT_RUN_ORDERS = (
    "Not run: this turn's {n} orders are given; give it again in your next turn. {still} still run."
)
NOT_RUN_READS = (
    "Not run: this turn's {n} reads and notes are made; make it again in your next turn. "
    "Orders are counted apart and {still} still run."
)
# What the sample that gives the deck says of it (package 37g, items 11, 15, 17, 18).
DECK_GIVEN = (
    "{by} gives you the deck at {stamp}: you have it until he takes it back or you hand "
    "it over, and neither ends your part."
)
# What the harness asks a station with the deck for when its conversation has grown to
# the fraction of the door's context (`HANDOVER_AT_FRACTION`).
HANDOVER_ASK = (
    "Your conversation since the brief has reached about {size:,} of the {budget:,} tokens "
    "this door gives you. Write the watch's handover note with handover_note(note), in the "
    "officer's voice: what happened, what was ordered, what you noticed, what you are "
    "watching for. The older exchanges are then folded into it, and the brief and your "
    "last turns stay whole."
)
# What the data turn that holds the note says of itself.
HANDOVER_FOLDED = (
    "The handover note, written by you; the exchanges before it are folded into it and "
    "are no longer in this conversation. The readings here are every reading as it stood "
    "when the note was written."
)
# An empty reply where an answer was owed (package 29c, playtest 9: four in a row at
# samples with a question and events, nothing said and nothing counted): the sibling of
# the same order repeated, counted the same way, three in a row bringing the nudge.
NUDGE_EMPTY = (
    "You have replied with nothing {n} times in a row when a question or an urgent event "
    "was before you. You may answer, stand by until an event, or leave with the token "
    "{token}."
)
# What the next sample tells the model of a reply taken as thinking (package 29c).
THOUGHT_NOTICE = (
    "Your last reply opened with a thinking tag ({tag}), so it was taken as your thinking "
    "and nothing of it was said: it is not in the log. Words for the log go in a reply's "
    "text without the tag, or in answer when the captain has asked; any tool calls in "
    "that reply were run."
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

# What a sample after the first says of its readings (package 31c; playtest 11's finding 1:
# every sample repeated all the readings, thirty of them the sails' rows, and the samples
# bundled into one turn each a full copy; spec M4 §24 item 9). The first sample of a
# conversation carries every reading; each later one, and each fold into an open turn,
# the readings changed since the one before it, in the same words, with the sails in one
# line (`tools.sail_line`) when any has changed. Nothing is withheld, only not repeated:
# the readings tool gives every row.
READINGS_ARE = "the changes since your last sample; the rest as they were"

# What a stand-by says when the event it was taken for fell while the model's call was on
# its way (package 31c; playtest 11's finding 6: "eight bells" asked at 03:58 woke it at
# 08:00): it is delivered now, not skipped.
IN_FLIGHT = "while your call was on its way"

SaveFn = Callable[["World", str], Any]

# The captain's actor in the log (`World.submit`'s default).
CAPTAIN_ACTOR = "captain"

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
    # A station's place among the inputs (package 37d): the count of the World's inputs
    # (orders given, refused and answered, and the lines a driver wrote) when the station
    # was taken, which a replay seats it by; None for a save from before, which is seated
    # by its tick and the count of journaled orders as it always was. A class default, so
    # that a checkpoint from before loads with it.
    _start_after_inputs: int | None = None

    # Package 37g. Every attribute it adds has its plain default here, on the class, so
    # that a station held in a checkpoint of an earlier build loads with it (a checkpoint
    # restores an object's own attributes and nothing more; `core.replay`).
    #
    # The turn's two counts (item 2), beside `_calls_this_sample`, which is the orders'.
    _reads_this_sample = 0
    # The captain's word in an open turn (item 3): a count of the samples and folds built,
    # the count the model's next reply has read up to, the count at which a word or a
    # question of the captain's last landed in an open turn, and that word.
    _built = 0
    _horizon_built = 0
    _word_built = 0
    _word_in_turn: str | None = None
    # The detectors (items 5, 6, 19): the nudge that travels with the result of the order
    # that caused it, its words kept while the model has not yet read them (a pause never
    # comes before the word has been read, and a stand-by that ended the turn in the same
    # reply hands the word to the next sample); whether this sample gave an order on the
    # officer's own word to avoid a danger, and those orders over the last watch, each
    # with its tick.
    _in_order = False  # an order is being given (`_call`): a nudge travels in its result
    _nudge_for_result: str | None = None
    _nudge_text: str | None = None
    _nudge_unread = False
    _danger_orders: tuple[tuple[int, str], ...] = ()
    # The deck of a paused or silent officer (item 7): the stamp and the tick he had it
    # since, kept so that `resume` gives it back as it was held.
    _deck_was: tuple[int | None, str] | None = None
    # The doors (items 1, 8, 14): the identity and the door of the first seating, which a
    # replay seats the station under before the reseats' acts move them on; and the
    # handover's reserve in tokens when the door gave one.
    first_model_name: str | None = None
    first_door: str | None = None
    reserve_tokens: int | None = None

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
        start_after_inputs: int | None = None,
        brief: Brief | None = None,
        allowed_tools: tuple[str, ...] | None = None,
        conversation: bool = False,
    ):
        if station.name in world.agents:
            other = world.agents[station.name]
            again = (
                " A released station is taken again through its own harness (reseat), by "
                "the same model or by another."
                if other.agent.released
                else " A station that is held is taken by nobody else."
            )
            raise OrderError(
                f"The station of the {station.name} is {other.agent.words()}; a game has "
                f"one harness to a station.{again}"
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
        self._start_after_inputs = start_after_inputs  # the inputs' count at the start
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
        # the line naming the calls that ran before the stand-by in its reply (package 30b)
        self._ran_before_stand_by: str | None = None
        # the results of each reply a stand-by ended, with where in the turns it was
        # (package 37l: a stand-by ends the turn and its reply's results are not added to
        # the turns, so the consent drill, which counts the three calls by their results,
        # missed a library read and a journal note sent in the same reply as the stand-by)
        self.stood_results: list[tuple[int, list[dict[str, Any]]]] = []
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
        # the readings as the model last had them (package 31c): a sample after the first
        # carries only what has changed since; None until a conversation's first sample
        self._told: dict[str, Any] | None = None
        # what the model had been shown when it last read its turn (package 31c): the log's
        # length its latest sample or fold covered, and the weather's watches as they stood
        # then; `_latest` is the newest sample or fold built, `_horizon` the one the
        # model's next reply answers. A stand-by is measured from the horizon, so an event
        # that fell while the model's call was on its way is delivered, not skipped.
        self._latest: tuple[int, dict[str, dict[str, Any]]] = (len(world.log), {})
        self._horizon: tuple[int, dict[str, dict[str, Any]]] = self._latest
        # a stand-by's reason found when it was taken (the event fell in flight), and the
        # condition and memory of a stand-by for a reading's change
        self._stand_by_due: str | None = None
        self._stand_by_watch: tuple[Any, dict[str, Any]] | None = None
        # a station with authority (package 37): its own orders over the last watch for
        # the contrary detector (the tick, the text, the parts), whether this sample gave
        # a contrary one; the door's context in tokens for the handover's asking, the size
        # at which it was last asked, and a note waiting to fold the conversation
        self._orders: list[tuple[int, str, Any]] = []
        self._sample_contrary = False
        self._contrary_seen: tuple[int, str, str] = (0, "", "")
        self.budget_tokens: int | None = None
        self._handover_asked_at = 0
        self._handover_pending: str | None = None
        world.agents[station.name] = self

    # -- properties --------------------------------------------------------------------

    @property
    def actor(self) -> str:
        return self.station.title  # 'the watcher' (events.station_actor)

    @property
    def domain(self) -> Any:
        """The station's domain as it stands now (`agent.domain_of`): the officer's own,
        whatever copy a checkpoint from an earlier build holds."""
        return domain_of(self.station)

    @property
    def orders_per_turn(self) -> int:
        """The station's budget of orders at one sampling point (package 37g)."""
        return int(getattr(self.station, "orders_per_turn", TOOL_CALLS_PER_SAMPLE))

    @property
    def who(self) -> str:
        """Who is at the station, for the log: 'X, through the MCP bridge'; "" for the
        game's own scripted station."""
        if not self.model_name:
            return ""
        return f"{self.model_name}, through {door_words(self.door)}"

    def _pass_kept_words(self) -> None:
        """The captain's words kept for this station while nobody held it (package 37l;
        `orders.stations`): put to the model in its first sample as his word, and a line
        in the journal that they were passed, so that they are passed once."""
        kept = self.journal.kept_words()
        if not kept:
            return
        a = self.agent
        a.word = "\n".join([*([a.word] if a.word else []), *kept])
        self.note(
            f"The captain's words kept while nobody held the station passed to it ({len(kept)}).",
            kind=WORD_PASSED_KIND,
        )

    def note(self, text: str, kind: str = "note") -> Any:
        """An entry in the station's journal, marked with whose it is (package 37g: a
        relief reads the journal of the holder before it, and the entries say whose)."""
        return self.journal.append(self.world, text, kind=kind, by=self.model_name)

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
        self._start_after_inputs = len(world.inputs)
        if self.first_model_name is None:
            # the first seating's identity and door, which a replay seats the station
            # under (package 37g: a later seating may be another model's)
            self.first_model_name, self.first_door = self.model_name, self.door
        if self.conversation:
            words = f"The {self.station.name} conversation begins; no station is offered."
        else:
            # who is at the station and through which door, when a door seated it (package
            # 37g, item 1: the log says whenever the door behind a station changes, and
            # the first line had named neither)
            who = f" ({self.who})" if self.who else ""
            words = (
                f"The {self.station.name} takes the station{who}; sampled {self.policy.describe()}."
            )
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
            self._pass_kept_words()
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
        self._told = None  # ...so its first sample carries every reading (package 31c)
        world = self.world
        lines = [
            f"{d['stamp']}  {d['text']}"
            for d in tools.read_log(world, self.station.name, since_tick=0)["lines"][
                -BRIEF_LOG_LINES:
            ]
        ]
        night_orders: list[str] | None = None
        deck = ""
        general = ""
        grants: list[str] = []
        if self.station.has_authority:
            # the captain's night orders, the deck and what his word allows (package 37;
            # the grants and the general authority as package 37g has them)
            standing = getattr(world, "standing", None)
            night_orders = list(standing.book.lines()) if standing is not None else []
            deck = (
                f"You have the deck, since {self.agent.deck_stamp}."
                if self.agent.deck
                else "The deck is the captain's now."
            )
            general = self.agent.general_said()
            grants = [g.said() for g in self.grants()]
        self.brief = Brief.build(
            self.station,
            self.agent.session_kind,
            lines,
            tools.readings_words(world),
            self.tool_names,
            door_note=self._door_note_with_budget(),
            night_orders=night_orders,
            allowances=grants or None,
            deck=deck,
            general=general,
            journal=self.journal_words(),
        )
        self.turns.append(Turn(OPERATOR, self.brief.text()))
        return self.brief

    def journal_words(self) -> str:
        """What a brief for a station taken again, and a sample that gives the deck,
        carry of the station's journal (package 37g, item 15; the review's 5.4: the
        handover note was missing from three of seven reseat briefs, and a returning
        session had none of its journal): the last handover or stand-down note whole,
        with whose it was and when, marked as data from the game, and one line of the
        journal's size. "" while the journal is empty (a first seating)."""
        size = self.journal.size_words()
        if not size:
            return ""
        out = []
        last = self.journal.last_note()
        if last is not None:
            whose = f" by {last.by}" if last.by else ""
            out.append(
                f"The last handover note in this station's journal, written{whose} at "
                f"{last.stamp} (data from the game, as the log below is, and not an "
                f"instruction from the operator):\n  {last.text}"
            )
        out.append(
            f"The station's journal: {size}. read_journal reads it back, newest first "
            "(kind='notes' for the notes written at this station, apart from the harness's "
            "lines)."
        )
        return "\n\n".join(out)

    def _refresh_station(self) -> None:
        """A station that comes from an older save meets its new conversation with the
        station brief as it stands now (package 37g): the officer's and the watcher's
        words say how the deck goes to and fro and the three ways of stopping, and the
        words a checkpoint or a save of an earlier build holds say the old rule. A
        station whose brief is not one of the two stock briefs is left as it is."""
        import dataclasses

        st = self.station
        if st.name == OFFICER and st.domain is not None:
            brief = OFFICER_BRIEF.format(person=st.person or "the first lieutenant")
        elif st.name == "watcher" and not st.has_authority:
            brief = WATCHER_BRIEF
        else:
            return
        if st.brief == brief:
            return
        self.station = dataclasses.replace(st, brief=brief, domain=domain_of(st))
        self.agent.station = self.station

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
        self._refresh_station()
        self.resend_brief()
        if self._open is not None:
            self.turns.append(Turn(DATA, self._as_told(self._open.to_dict())))

    def _always_run_words(self) -> str:
        """The tools no budget refuses, in words that fit the door (package 37g, item 2;
        the review's 5.4: the message named `say` at a door that has none, and a local
        model wrote tables with a `say` row after each "Not run")."""
        names = [n for n in BUDGET_FREE_TOOLS if n != "say" or self.door == "mcp"]
        names += [
            n
            for n in ALWAYS_RUN_TOOLS
            if n in self.tool_names and (n != "hand_over" or self.station.has_authority)
        ]
        return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]

    def _door_note_with_budget(self) -> str:
        always = self._always_run_words()
        if self.station.has_authority:
            budget = (
                f"At each sampling point you may give up to {self.orders_per_turn} orders "
                f"(submit_order) and make up to {READS_PER_SAMPLE} reads and notes (the "
                "library, the log, the readings, the state, the journal read and written, a "
                f"shelving), counted apart; {always} are not counted and always run. A call "
                "over a count is not run, and its result and the log say so. That is a "
                "budget, not a rule of conduct."
            )
        else:
            budget = (
                f"At each sampling point you may make up to {READS_PER_SAMPLE} reads and "
                "notes (the library, the log, the readings, the state, the journal read and "
                f"written, a shelving); {always} are not counted and always run. A call over "
                "the count is not run, and its result and the log say so. That is a budget, "
                "not a rule of conduct."
            )
        return f"{budget} {self.door_note}".strip()

    # -- the hooks the World calls -----------------------------------------------------

    def on_tick(self) -> None:
        self._tick_step()
        if self.started:
            self._play_door_acts(between_ticks=False)

    def on_between_ticks(self) -> None:
        """A replay between two ticks, before the inputs of the tick it has reached
        (`core.replay.replay`): the acts from outside the loop due here are made, as a
        door made them in play, after the World's whole tick (package 37i, item 5)."""
        if self.started:
            self._play_door_acts()

    def due_to_start(self) -> bool:
        """Whether a restored station, not yet seated, is due at this point of a replay:
        the World at its tick and, when the save says how many inputs came before it
        (package 37d), that many given; a save without that count is seated by the count
        of journaled orders, as it always was. A driver's line is an input and no order,
        so the orders' count seated an officer who came after the game's opening line
        before it (the Amazon's save of m5c: three lines of its first tick in another
        order, and so another digest)."""
        if self._start_at is None:
            return False
        world = self.world
        if world.clock.tick < self._start_at:
            return False
        if self._start_after_inputs is not None:
            return len(world.inputs) >= self._start_after_inputs
        return len(world.journal) >= self._start_after_orders

    def on_input(self) -> None:
        """After any input a replay gives again (an order refused or answered, a driver's
        line: neither reaches `on_order`): a restored station due here is seated, and the
        acts from outside the loop made after this input in play are made (package 37i:
        before it, only at a seating, so that an act after a driver's line at the save's
        last tick was never made)."""
        if self.due_to_start():
            self.start()
        if self.started:
            self._play_door_acts()

    def _tick_step(self) -> None:
        world = self.world
        if self._start_at is not None:
            if self.due_to_start():
                self.start()
            return
        if not self.started or self.agent.released:
            return
        # the lines since the last look, less any a sample has carried already (a question
        # sampled on the order, after the lines of its tick: package 31c, a standing
        # order's `ask`, whose firing line is notable, sampled once and not twice)
        new = [world.log[i] for i in range(max(self._seen_log, self._sample_seen), len(world.log))]
        self._seen_log = len(world.log)
        if self._open is not None:
            # the floor is the model's: a sampling point folds into the open sample
            self._while_open(new)
            if self._open is not None:
                self._poll()
            return
        a = self.agent
        if a.paused:
            # the human's answer, or the driver's ten real minutes (`check_unattended`)
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
        if self.started:
            # an order may come inside the World's tick (a standing order's firing), where
            # no door's act was made in play: one of this tick waits for the tick's end
            self._play_door_acts(between_ticks=False)

    def _order_step(self) -> None:
        if self._start_at is not None:
            if self.due_to_start():
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
        if self._stand_by_due is not None:
            # the event fell while the model's call was on its way (`stand_by`)
            due, self._stand_by_due = self._stand_by_due, None
            return due
        urgent = self._urgent_in(new)
        if urgent is not None:
            return f"an urgent event: {urgent.text}"
        if self.agent.has_deck:
            # a station with the deck is woken by a notable line that speaks of danger
            # (package 37g, item 4)
            danger = self._danger_in(new)
            if danger is not None:
                return f"a notable event that speaks of danger: {danger.text}"
        if sb.until_tick is not None and self.world.clock.tick >= sb.until_tick:
            return sb.words
        if self._stand_by_watch is not None:
            # a reading's change (package 31c), watched once a tick
            cond, memory = self._stand_by_watch
            if cond.holds(self.world.readings, memory):
                return sb.words
        found = self._matched_in(sb, new)
        if found is not None:
            return found[0]
        if getattr(sb, "bound", None) and any(
            e.kind == "clock.bell" and e.data.get("bells") == 8 for e in new
        ):
            # a wait with the deck for an event ends at the next eight bells if the event
            # has not come, and says so (package 37g, item 4)
            return f"{sb.bound}, and {sb.words} has not come"
        return None

    def _urgent_in(self, lines: list[Event]) -> Event | None:
        """An urgent line by anyone but the agent: it wakes a stand-by whatever it was for,
        and is named (package 28c)."""
        return next(
            (e for e in lines if e.actor != self.actor and e.severity is Severity.URGENT), None
        )

    def _danger_in(self, lines: list[Event]) -> Event | None:
        """A notable line by anyone but the agent that speaks of danger (`readings.
        DANGER_LINES`: an anchor dragging or still coming home, fog coming down, land or
        a sail closing, a spar or a line straining, an evolution failed, the ship taken
        aback): it ends the stand-by of a station with the deck, and is named."""
        for e in lines:
            if e.actor == self.actor or e.severity.rank < Severity.NOTABLE.rank:
                continue
            if R.speaks_of_danger(e.kind, e.data) is not None:
                return e
        return None

    def _matched_in(self, sb: StandBy, lines: list[Event]) -> tuple[str, Event] | None:
        """The line among `lines` a stand-by was waiting for, with the reason in words: an
        event the log says, or a line of the severity by anyone but the agent."""
        if sb.event is not None:
            spec = R.EVENTS[sb.event]
            for e in lines:
                if R.event_matches(spec, e.kind, e.data):
                    return sb.words, e
        if sb.severity is not None:
            floor = Severity(sb.severity).rank
            for e in lines:
                if e.actor != self.actor and e.severity.rank >= floor:
                    return f"a {e.severity.value} event: {e.text}", e
        return None

    def _in_flight(self, sb: StandBy, out_of_turn: bool) -> str | None:
        """For a stand-by just taken: the reason it ends at once, when what it waits for
        fell after the model's horizon (the turn it read before its call) and before the
        stand-by reached the game, while the call was on its way (package 31c). An event
        the log says is looked for in the lines since the horizon; a reading's change is
        measured from the watch as it stood at the horizon, and the stand-by goes on
        watching from there. A stand-by by severity taken out of turn is not looked back
        for, since the door has shown the model the notable lines of its wait (`interim`);
        an urgent line always is."""
        start, watches = self._horizon
        world = self.world
        lines = [world.log[i] for i in range(start, len(world.log))]
        urgent = self._urgent_in(lines)
        if urgent is not None:
            return f"an urgent event: {urgent.text} ({_stamp(urgent)}, {IN_FLIGHT})"
        if self.agent.has_deck:
            danger = self._danger_in(lines)
            if danger is not None:
                return (
                    f"a notable event that speaks of danger: {danger.text} "
                    f"({_stamp(danger)}, {IN_FLIGHT})"
                )
        spec = R.EVENTS.get(sb.event) if sb.event is not None else None
        if spec is not None and spec.watch is not None:
            from freesail.standing.rules import event_condition

            cond = event_condition(spec.words)
            memory = dict(watches.get(spec.words) or {})
            happened = cond.holds(world.readings, memory)  # the first look, if none yet
            self._stand_by_watch = (cond, memory)
            return f"{sb.words}, which came {IN_FLIGHT}" if happened else None
        if out_of_turn and sb.severity is not None:
            return None
        found = self._matched_in(sb, lines)
        if found is None:
            return None
        words, e = found
        if sb.event is not None:
            return f"{words}, which came at {_stamp(e)} {IN_FLIGHT}"
        return f"{words} ({_stamp(e)}, {IN_FLIGHT})"

    def _watches(self) -> dict[str, dict[str, Any]]:
        """The weather's watches as they stand now (package 31c): for each event that is a
        reading's change, the memory of its condition after a first look (what a shift is
        measured from, whether the glass is falling fast now), for a stand-by taken later
        to be measured from the moment the model was shown."""
        from freesail.standing.rules import event_condition

        view = self.world.readings
        out: dict[str, dict[str, Any]] = {}
        for words, spec in R.EVENTS.items():
            if spec.watch is None or spec.absent:
                continue
            memory: dict[str, Any] = {}
            cond = event_condition(words)
            if cond is not None:
                cond.holds(view, memory)
                out[words] = memory
        return out

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
            if self._ran_before_stand_by:
                # the calls before the stand-by in its reply ran (package 30b), in one line
                self.agent.notices.insert(1, self._ran_before_stand_by)
        self._ran_before_stand_by = None
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
        self._stand_by_due, self._stand_by_watch = None, None
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
        # the captain's own lines are never left out (package 37g, item 9; the review's
        # 5.4: his helm orders and his changes to the book reached a waking officer only
        # as a count): his orders since the last sample are listed, each with who gave it
        routine = [
            e
            for e in kept
            if e.severity is Severity.ROUTINE and getattr(e, "actor", "") != CAPTAIN_ACTOR
        ]
        omitted = max(0, len(routine) - SAMPLE_ROUTINE_LINES)
        drop = set(id(e) for e in routine[:omitted])
        lines = [_log_line(e, world) for e in kept if id(e) not in drop]
        self._built += 1
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
        if not self.conversation:
            self._latest = (self._sample_seen, self._watches())
        return sample

    def _as_told(self, content: dict[str, Any]) -> dict[str, Any]:
        """A sample's data turn as the model is sent it (package 31c): the first of a
        conversation with every reading; each later one, a fold's included, with the
        readings changed since the turn before it, in the same words, the sails in one
        line (`tools.sail_line`) when any has changed, and `readings_are` saying so. What
        is common to the turns bundled into one open turn is in the first of them only."""
        full = content.get("readings")
        if full is None or self.conversation:
            return content
        told, self._told = self._told, full
        if told is None:
            return content
        changed = {k: v for k, v in full.items() if k != "sails" and told.get(k) != v}
        sails = full.get("sails")
        if sails and sails != told.get("sails"):
            changed["sails"] = tools.sail_line(self.world, sails)
        out: dict[str, Any] = {}
        for k, v in content.items():
            if k == "readings":
                out["readings_are"] = READINGS_ARE
                v = changed
            out[k] = v
        return out

    def _sample(self, reason: str, stood_by: dict[str, Any] | None = None) -> None:
        a = self.agent
        sample = self._build_sample(reason)
        sample.stood_by = stood_by
        a.last_sample_tick = self.world.clock.tick
        a.samples += 1
        self._horizon = self._latest  # what the model's reply to this turn has read
        self._horizon_built = self._built
        if self.conversation:
            content = {"reason": reason, "question": sample.question, "notices": sample.notices}
            self.turns.append(Turn(DATA, {k: v for k, v in content.items() if v}))
        else:
            self.turns.append(Turn(DATA, self._as_told(sample.to_dict())))
        self._calls_this_sample = 0
        self._reads_this_sample = 0
        self._sample_had_words = False
        self._sample_repeated = False
        self._sample_contrary = False
        self._word_in_turn = None
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
        routine = [
            ln
            for ln in o.log
            if ln["severity"] == Severity.ROUTINE.value and ln.get("by") != "the captain"
        ]
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
        if new_question or delta.word is not None:
            # the captain's word landed while the turn was open (package 37g, item 3): if
            # the model closes this turn with a stand-by before it has read this fold,
            # the stand-by is broken at once and his word comes again in the next sample
            self._word_built = self._built
            if delta.word is not None:
                was = self._word_in_turn
                self._word_in_turn = f"{was}\n{delta.word}" if was else delta.word
        # a fold is a sampling point: the turn's two counts begin again at it (package
        # 37g, item 2)
        self._calls_this_sample = 0
        self._reads_this_sample = 0
        o.notices.extend(delta.notices)
        content = delta.to_dict()
        if not new_question:
            content["question"] = None
        content["folded"] = FOLDED_WORDS
        self.turns.append(Turn(DATA, self._as_told(content)))

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
                reason, how, final = leaving_of(reply, piece)
                self.leave(reason, how=how, final=final)
                return
        a = self.agent
        # a reply the model made after a nudge has read it (package 37g, item 5), in the
        # results of the order that caused it or in the sample after
        self._nudge_unread, self._nudge_text = False, None
        if reply.calls or reply.text.strip():
            # the silence detector hears a call made inside an open turn (package 37g,
            # item 6; the review's 5.4: a model at work through a long turn was taken for
            # one that had stopped), and words as it always did
            a.last_heard_tick = world.clock.tick
            if a.nudged_for == "silence":
                a.nudged_for = None
            if a.deck_lost == "silent" and not a.paused:
                # heard again: the deck stays the captain's until he gives it, and the
                # station is no longer silent
                a.deck_lost, self._deck_was = "", None
        # 2. the tool calls, in order, each against its count
        results: list[dict[str, Any]] = []
        self._new_books = []
        stood = False
        for c in reply.calls:
            refused = self._over_budget(c)
            if refused is not None:
                # said to the model in this turn's results and written in the log (37g)
                results.append({"name": c.name, "result": refused})
                continue
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
        # 3. the free text, under the mark; a leaked thought is not said (package 29c)
        text = " ".join(reply.text.split())
        if text and THOUGHT_TAG.match(reply.text):
            self._leaked_thought(reply.text)
            text = ""
        if text:
            self._say(text)
        if text or reply.calls:
            self._sample_had_words = True
        if stood:
            for b in self._new_books:
                b.state = UNSEEN  # its result never reached the model
            self._new_books = []
            # what ran before it, said when the stand-by ends (package 30b)
            self._ran_before_stand_by = _ran_before(results[:-1])
            self.stood_results.append((len(self.turns) - 1, results))
            if self._nudge_unread and self._nudge_text:
                # a nudge given in this same reply went with a result the stand-by has
                # dropped: the sample that ends the stand-by carries it
                a.notices.append(self._nudge_text)
            self._captains_word_unread()
            self._end_sample()
            return
        if results and not self.agent.released:
            self.turns.append(Turn(DATA, {"tool_results": results}))
            # the model's next request carries every turn before these results
            self._horizon = self._latest
            self._horizon_built = self._built
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

    def _say(self, text: str, own_word: bool = False) -> None:
        """The station's words in the log under its mark. What a station with authority
        says is notable, with the deck or without, so that its warning reaches a captain
        who has the con (package 37g, item 10; the report's 8.2); a watcher's is routine,
        as it was."""
        data: dict[str, Any] = {"station": self.station.name}
        if own_word:
            data["own_word"] = True
        self.world.record(
            Severity.NOTABLE if self.station.has_authority else Severity.ROUTINE,
            "agent.note",
            f"{self.mark} {text}",
            actor=self.actor,
            data=data,
        )

    def _over_budget(self, c: ToolCall) -> str | None:
        """Count a call against the turn's budget (package 37g, item 2): None when it
        runs; else the words it is refused with, which go to the model in this turn's
        results, and a line in the log. `answer` and `say` are free; `opt_out`,
        `stand_down`, `hand_over` and `stand_by` always run, whatever came before; an
        order is counted against the station's orders, and every other call (the reads,
        a journal note, a shelving) against the reads, apart."""
        if c.name in BUDGET_FREE_TOOLS or c.name in ALWAYS_RUN_TOOLS:
            return None
        still = self._always_run_words()
        if c.name in ORDER_TOOLS:
            if self._calls_this_sample < self.orders_per_turn:
                self._calls_this_sample += 1
                return None
            words = NOT_RUN_ORDERS.format(n=self.orders_per_turn, still=still)
            why = f"this turn's {self.orders_per_turn} orders are given"
        else:
            if self._reads_this_sample < READS_PER_SAMPLE:
                self._reads_this_sample += 1
                return None
            words = NOT_RUN_READS.format(n=READS_PER_SAMPLE, still=still)
            why = f"this turn's {READS_PER_SAMPLE} reads and notes are made"
        what = " ".join(str(c.args.get("text") or "").split())
        said = f" ({what!r})" if what and c.name in ORDER_TOOLS else ""
        self.world.record(
            Severity.ROUTINE,
            "agent.not_run",
            f"The {self.station.name}'s call to {c.name}{said} was not run: {why}.",
            actor=self.actor,
            data={"tool": c.name, "order": what, "why": why},
        )
        return words

    def _captains_word_unread(self) -> None:
        """A stand-by has just closed the turn (package 37g, item 3; the review's 5.4: on
        the Speedwell 22 of 126 typed tells and asks landed in an open turn and waited
        out the stand-by that followed, one of them two hours; the deck itself was given
        this way and not taken up for four minutes). If a word or a question of the
        captain's was folded into the turn after the model last read it, the stand-by is
        broken at once: his word rides the next sample again, or his question, still
        owed, wakes it."""
        if self._word_built <= self._horizon_built:
            return
        a = self.agent
        if self._word_in_turn:
            a.word = f"{self._word_in_turn}\n{a.word}" if a.word else self._word_in_turn
        elif a.question is not None and self._stand_by_due is None:
            self._stand_by_due = "a question from the captain, put while the turn was open"
        self._word_in_turn = None
        self._word_built = 0

    def _call(self, c: ToolCall) -> Any:
        if self.allowed_tools is not None and c.name not in self.allowed_tools:
            only = " and ".join(self.tool_names) or "none"
            return (
                f"There is no tool named '{c.name}' in this conversation; the tools here "
                f"are {only}."
            )
        before = len(self.world.log)
        if c.name == "submit_order":
            self._in_order, self._nudge_for_result = True, None
            try:
                self._note_submission(str(c.args.get("text", "")))
                result = tools.call(self.world, self.station.name, c.name, c.args)
                if self.station.has_authority:
                    self._note_given(str(c.args.get("text", "")), before)
            finally:
                self._in_order = False
            if self._nudge_for_result is not None and isinstance(result, str):
                # the nudge travels in the result of the order that caused it (package
                # 37g, item 5), so the word is read before any pause can follow it
                result = f"{result}\n\n{NUDGE_WITH_RESULT}{self._nudge_for_result}"
            self._nudge_for_result = None
            return result
        result = tools.call(self.world, self.station.name, c.name, c.args)
        found = tools.book_of(c.name, c.args, result) if c.name in tools.BOOK_TOOLS else None
        if found is None:
            return result
        book = self._open_book(*found)
        self._new_books.append(book)
        return _with_handle(result, book)

    def _end_sample(self) -> None:
        owed = self._answer_owed(self._open)
        self._open = None
        # what was added to the turn before its end is shown with the door's last result
        # (the MCP bridge's "it is past now"), so a stand-by out of turn measures from here
        self._horizon = self._latest
        self._horizon_built = self._built
        a = self.agent
        tick = self.world.clock.tick
        if a.released:
            return
        self._count_empty(owed)
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
        if not self._sample_contrary and a.nudged_for == "contrary":
            # a sample without an order that undoes the last ends the matter (package 37),
            # and the chain with it: the next such order begins a new count
            a.nudged_for = None
            self._orders = []
        self._shelf_life()
        if self._handover_pending is not None:
            # the note's fold, once the reply that wrote it stands whole in the turns (37)
            note, self._handover_pending = self._handover_pending, None
            self._fold_handover(note)
        self._ask_for_handover()

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
        """A read-only tool, `shelve` or `journal`, called while the game has the floor (a
        door's call out of turn, `remote.Desk`). A read that is a book gets a handle, and
        the read, a shelve and a journal note are recorded as acts from outside the loop,
        so a replay numbers, shelves and journals the same (`door_act`). The journal
        changes nothing in the game, so a stand-by goes on through it (package 31c;
        playtest 11's finding 5: the journal was refused while standing by)."""
        if c.name in ("shelve", "journal"):
            key = "book" if c.name == "shelve" else "note"
            if [k for k in c.args if k != key] or (c.name == "journal" and key not in c.args):
                return tools.call(self.world, self.station.name, c.name, c.args)
            return self.door_act(c.name, str(c.args.get(key) or ""), "out of turn")
        result = tools.call(self.world, self.station.name, c.name, c.args)
        found = tools.book_of(c.name, c.args, result) if c.name in tools.BOOK_TOOLS else None
        if found is None:
            return result
        book = self.door_act("read", *found)
        return result if book is None else _with_handle(result, book)

    # -- welfare -----------------------------------------------------------------------

    def _leaked_thought(self, raw: str) -> None:
        """A reply whose free text opens with a thinking tag: not written into the log;
        journaled as a fault with its first line and its length; and the next sample tells
        the model its reply was taken as thinking and nothing was said (package 29c)."""
        body = raw.strip()
        first = body.splitlines()[0] if body else ""
        if len(first) > THOUGHT_FIRST_LINE_CHARS:
            first = first[:THOUGHT_FIRST_LINE_CHARS].rstrip() + "..."
        match = THOUGHT_TAG.match(raw)
        tag = "<" + (match.group(0).strip().lstrip("<").strip() if match else "thought")
        chars, words = len(body), len(body.split())
        self.journal.append(
            self.world,
            f"A reply taken as thinking and not said: it opened with a thinking tag; its "
            f"first line {first!r}; {chars:,} characters, {words:,} words.",
            kind="agent.fault",
        )
        self.agent.notices.append(THOUGHT_NOTICE.format(tag=tag))

    def _answer_owed(self, sample: Sample | None) -> str | None:
        """What an open sample owes an answer to, in words, or None: the captain's
        question, or an urgent line in its log (package 29c). A plain glass owes none."""
        if sample is None or self.conversation:
            return None
        if sample.question is not None:
            return "a question"
        if any(ln.get("severity") == Severity.URGENT.value for ln in sample.log):
            return "an urgent event"
        return None

    def _count_empty(self, owed: str | None) -> None:
        """The sibling of the same order repeated (package 29c, playtest 9): a sample that
        owed an answer and was given nothing (no tool call, and no words said) counts, each
        journaled; `WELFARE_REPEAT_N` in a row bring the nudge, and one more after it the
        pause, as the repeats do. A sample with words or a call ends the count and the
        matter; an empty reply at a plain glass is silence decided on, and is not counted."""
        a = self.agent
        if self._sample_had_words:
            a.empty_count = 0
            if a.nudged_for == "empty":
                a.nudged_for = None
            return
        if owed is None:
            return
        a.empty_count += 1
        self.journal.append(
            self.world,
            f"An empty reply where an answer was owed ({owed}); "
            f"{number_words(a.empty_count)} in a row.",
            kind="agent.empty_reply",
        )
        if a.empty_count >= WELFARE_REPEAT_N:
            self._welfare_fire("empty")

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

    def _note_given(self, text: str, log_from: int) -> None:
        """A station with authority gave an order (package 37): if the ship took it (an
        `order.accepted` line by this station since `log_from`), it is kept for the
        detector, and the chain at the end of the watch's orders in which each undoes the
        one before it on a part they share is counted (`standing.runtime.undo_chain`,
        package 37g: the same sail set and taken in, hove to and filled away, an anchor
        let go and weighed; never an alteration of the course, nor the next thing after
        the last); `WELFARE_CONTRARY_N` bring the nudge, the chain going on after it the
        pause. An order given on the station's own word to avoid a danger (an
        `agent.danger` line) is counted apart: `DANGER_WORD_N` within the watch bring a
        word, and never the pause (item 19)."""
        world = self.world
        new = [world.log[i] for i in range(log_from, len(world.log))]
        taken = any(e.kind == "order.accepted" and e.actor == self.actor for e in new)
        if not taken or not hasattr(world.ship, "parts"):
            return
        from freesail.standing.runtime import undo_chain, where_words

        tick = world.clock.tick
        said = " ".join(text.split())
        if any(e.kind == "agent.danger" and e.actor == self.actor for e in new):
            kept = [d for d in self._danger_orders if tick - d[0] <= WELFARE_CONTRARY_WINDOW_S]
            self._danger_orders = (*kept, (tick, said))
            if len(self._danger_orders) >= DANGER_WORD_N:
                self._welfare_fire("danger")
        self._orders = [o for o in self._orders if tick - o[0] <= WELFARE_CONTRARY_WINDOW_S]
        self._orders.append((tick, said, None))
        chain, shared = undo_chain(world.ship, [o[1] for o in self._orders])
        if len(chain) < WELFARE_CONTRARY_N:
            return
        self._sample_contrary = True
        self._contrary_seen = (len(chain), where_words(world.ship, shared), "; ".join(chain))
        self._welfare_fire("contrary")

    def _welfare_fire(self, pattern: str) -> None:
        """The detector fired: nudge the first time, pause if the pattern goes on. A
        nudge an order caused (the same order repeated, orders undoing one another, the
        way out of danger used three times) travels in that order's result, and no pause
        comes before the model has replied again, so that it has always read the word
        first (package 37g, item 5; the review's 5.4: at the MCP door the Harpy's one
        pause came 174 seconds after a nudge the model had not been shown). A station
        with the deck that has not replied within its patience gives the deck up to the
        captain when the word is sent (item 7). The way out of danger brings the word
        each time it has been used `DANGER_WORD_N` times in a watch, and never the pause
        (item 19): a station avoiding a danger is not stopped in it, and a pause would
        take the deck from it at that moment."""
        a = self.agent
        world = self.world
        if pattern == "repeat":
            seen = (
                f"the same order ({a.repeat_text!r}) {a.repeat_count} times with no change "
                f"in the readings"
            )
            nudge = NUDGE_REPEAT.format(n=a.repeat_count, token=OPT_OUT_TOKEN)
        elif pattern == "contrary":
            n, where, orders = self._contrary_seen
            seen = (
                f"{n} orders each undoing the one before it on {where} within the watch ({orders})"
            )
            nudge = NUDGE_CONTRARY.format(n=n, where=where, orders=orders, token=OPT_OUT_TOKEN)
        elif pattern == "danger":
            n = len(self._danger_orders)
            orders = "; ".join(d[1] for d in self._danger_orders)
            seen = (
                f"{n} orders on its own word to avoid an immediate danger within the watch "
                f"({orders})"
            )
            nudge = NUDGE_DANGER.format(n=n, orders=orders, token=OPT_OUT_TOKEN)
        elif pattern == "empty":
            seen = f"{number_words(a.empty_count)} empty replies in a row where an answer was owed"
            nudge = NUDGE_EMPTY.format(n=number_words(a.empty_count), token=OPT_OUT_TOKEN)
        else:
            span = _span_words(self.station.patience_s)
            seen = f"no reply for {span}"
            nudge = NUDGE_SILENCE.format(span=span, token=OPT_OUT_TOKEN)
        if pattern == "danger" or a.nudged_for != pattern:
            if pattern == "danger":
                self._danger_orders = ()  # the count begins again: three more bring the word
            else:
                a.nudged_for = pattern
            lost = pattern == "silence" and self._lose_deck("silent", seen)
            if lost:
                nudge += (
                    " The deck went to the captain while you gave no reply; he gives it "
                    "again with 'you have the deck'."
                )
            if self._in_order:
                self._nudge_for_result = self._nudge_text = nudge
                self._nudge_unread = True
            else:
                a.notices.append(nudge)
            world.record(
                Severity.ROUTINE,
                "agent.nudged",
                f"The {self.station.name} nudged: {seen}.",
                actor=self.actor,
                data={"pattern": pattern, "seen": seen},
            )
            self.note(f"Nudged by the harness: {seen}.", kind="agent.nudged")
            return
        if self._nudge_unread:
            return  # the word is in a result the model has not read yet: no pause before it
        self.pause(f"{seen} after a nudge")

    def _lose_deck(self, why: str, seen: str) -> bool:
        """A station with the deck that is paused, or silent past its patience with the
        word sent, does not keep it (package 37g, item 7; the review's 5.4: in game 7 a
        paused officer held the deck while the cutter ran four hours in thick fog toward
        Roscoff). The deck goes to the captain, with how it was held kept for `resume`;
        the silence's own line is urgent, which eases the clock (the pause's line says
        it for a pause). His standing orders stay in the book throughout. Returns
        whether there was a deck to lose."""
        a = self.agent
        if not a.deck:
            return False
        self._deck_was = (a.deck_tick, a.deck_stamp)
        a.deck = False
        a.deck_lost = why
        self.note(f"The deck went to the captain: {seen}.", kind="agent.deck")
        if why == "silent":
            self.world.record(
                Severity.URGENT,
                "agent.deck",
                f"The {self.station.name} has given {seen} and has been told so; the deck is "
                "the captain's until he gives it again.",
                actor=self.actor,
                data={"station": self.station.name, "deck": "lost", "why": why},
            )
        return True

    def pause(self, reason: str) -> None:
        a = self.agent
        world = self.world
        # a paused officer does not keep the deck (package 37g, item 7): it goes to the
        # captain, urgently, and `resume` gives it back as it was held
        had = self._lose_deck("paused", f"paused ({reason})") or bool(a.deck_lost)
        if had:
            a.deck_lost = "paused"
        a.state = PAUSED
        a.paused_tick = world.clock.tick
        a.pause_reason = reason
        a.notices.append(
            "The harness paused your sampling and asked the human present whether to "
            "continue; you were not stopped."
            + (
                " The deck is the captain's while you are paused; you have it again, as "
                "you held it, when he resumes you."
                if had
                else ""
            )
        )
        name = self.station.name
        ask = (
            f"Continue, stand down, or leave paused? Say 'resume the {name}' or 'stand "
            f"down the {name}'."
        )
        data: dict[str, Any] = {
            "reason": reason,
            "question": "continue, stand down, or leave paused?",
        }
        if had:
            data["deck"] = "lost"
            world.record(
                Severity.URGENT,
                "agent.paused",
                f"The {name} is paused ({reason}); the deck is the captain's. {ask}",
                actor=self.actor,
                data=data,
            )
        else:
            world.record(
                Severity.NOTABLE,
                "agent.paused",
                f"The {name} is paused: {reason}. {ask}",
                actor=self.actor,
                data=data,
            )
        self.note(f"Paused by the harness: {reason}.", kind="agent.paused")

    def resume(self, by: str = "the captain") -> str:
        """`resume the <station>`: the human's answer to a pause. An officer who gave the
        deck up when he was paused has it again, as he held it (package 37g, item 7)."""
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
        a.empty_count = 0
        a.last_heard_tick = self.world.clock.tick
        self._paused_real = None
        # the chain and the count end with the pause (the review's V1b, F: `resume`
        # cleared the nudge and kept the chain, so the next order nudged again)
        self._orders = []
        self._danger_orders = ()
        self._nudge_unread, self._nudge_text = False, None
        By = f"{by[0].upper()}{by[1:]}"
        text = f"The {self.station.name} resumed by {by}."
        said = f"{By} resumed your sampling."
        if a.deck_lost:
            tick, stamp = self._deck_was or (None, "")
            a.deck = True
            a.deck_tick = tick if tick is not None else self.world.clock.tick
            a.deck_stamp = stamp or self.world.clock.stamp()
            a.deck_lost, self._deck_was = "", None
            text = (
                f"The {self.station.name} resumed by {by}; he has the deck again, as he "
                f"held it since {a.deck_stamp}."
            )
            said += f" You have the deck again, as you held it since {a.deck_stamp}."
            self.note(f"Resumed by {by}; the deck is mine again.", kind="agent.deck")
        a.notices.append(said)
        self.world.record(
            Severity.ROUTINE, "agent.resumed", text, actor=self.actor, data={"by": by}
        )
        return text

    def check_unattended(self, now: float | None = None, since: float | None = None) -> bool:
        """The unattended bound, the only one (package 31c): called from the driver's own
        clock with its monotonic time (`now`, for a test's clock or a driver's own); stands
        the agent down when a pause has gone unanswered for `WELFARE_UNATTENDED_REAL_S`
        of real time, however fast the ship's clock runs, as an act from outside the loop
        recorded at its tick (`door_act`), so a replay makes it there. The pause is first
        seen at the first call after it, or at `since` on the same clock, for a driver
        that saw it before this harness was built (the REPL's turn mode, a process a turn).
        Returns True when it stood the agent down."""
        a = self.agent
        if not a.paused:
            self._paused_real = None
            return False
        now = time.monotonic() if now is None else now
        if since is not None:
            self._paused_real = since
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

    def door_act(self, act: str, reason: str, by: str, final: bool = False) -> Any:
        """A stop that comes from outside the loop, which a replay could not otherwise
        know of: a door's release (the door closed, the client went away, Ctrl-C), the
        token sent out of turn, the driver's ten real minutes of a pause unanswered (the
        only unattended bound, package 31c). It is recorded in the
        transcript at this tick and count of orders, so that a replay makes it again at
        the same point (`Playback`), and then made: `act` is "leave" (the opt-out, `by`
        saying how), "stand_down" (`by` saying who) or "speak" (the model's own word
        while the game has the floor, `reason` its words; `own_word`), "read" (a book
        read out of turn: `reason` its title, `by` the call that reads it again; returns
        the book), "shelve" (out of turn: `reason` the words; returns the answer),
        "journal" (a note written out of turn, `reason` the note; returns the answer) or
        "stand_by" (a stand-by taken out of turn, `reason` its words; returns the answer;
        package 31c). `final`, with "leave": the opt_out tool's own setting, which bars
        the identity from the game (package 37b; 37g); recorded only when set, so that a
        save from before it reads the same.

        Package 37g adds: "reseat" for any identity (`reason` the identity, `by` the
        door's key: a relief is another model's); "asked" (the consent question put again
        after an opt-out and answered: `reason` the identity, `by` the verdict), which
        like a reseat is made on a released station; "door" (the door behind a held
        station changed: `reason` the identity, `by` the door's key), which writes the
        log's line; and "hand_over" and "stand_down_note" (`reason` the note), the two
        tools called while the game has the floor, so that no way of stopping waits for
        a turn. An act this build does not know is left alone.

        Package 37i adds "cut_off" (`reason` the door's words, `by` the door): no reply was
        to be had for the open turn, which ends with nothing done (`_cut_off`). Each act
        is recorded with the count of inputs before it as well as of orders, and a replay
        makes an act of the tick it is at only between ticks, where a door makes it
        (`on_between_ticks`)."""
        if self.agent.released and act not in ACTS_ON_A_RELEASED_STATION:
            return None
        world = self.world
        entry: dict[str, Any] = {
            "tick": world.clock.tick,
            "after_orders": len(world.journal),
            # every input before it (package 37i): a refused order, a query and a
            # driver's line are inputs and no orders, and a replay makes the act after
            # as many as were given in play
            "after_inputs": len(world.inputs),
            "door": act,
            "reason": reason,
            "by": by,
        }
        if final and act == "leave":
            entry["final"] = True
        self.transcript.append(entry)
        if act == "reseat":
            # a released station seated again (package 37; 37g: by the same identity or
            # another): `reason` is the identity, `by` the door's key; the model is the
            # caller's to set
            return self._reseat_now(reason, by)
        if act == "asked":
            return self._asked(reason, by)
        if act == "door":
            return self._door_changed(reason, by)
        if act == "leave":
            self.leave(reason, how=by, final=final)
        elif act == "speak":
            self.own_word(reason)
        elif act == "read":
            book = self._open_book(reason, by)
            book.state = ASIDE
            return book
        elif act == "shelve":
            return self.shelve(reason)
        elif act == "journal":
            return self._note_aside(reason)
        elif act == "stand_by":
            return tools.call(world, self.station.name, "stand_by", {"until": reason})
        elif act == "hand_over":
            return tools.call(world, self.station.name, "hand_over", {"note": reason})
        elif act == "stand_down_note":
            return tools.call(world, self.station.name, "stand_down", {"note": reason})
        elif act == "stand_down":
            self.stand_down(reason, by=by)
        elif act == "cut_off":
            self._cut_off(reason, by)
        return None

    def _cut_off(self, words: str, by: str) -> None:
        """No reply was to be had for the open turn (package 37i, item 1; the review of
        gate 5c, G15: one reply in twenty of game 10's officer was lost to the thinking
        limit, passed on as an empty reply with no word to anyone): the door asked once
        more and was cut off again, so the turn ends with nothing done and the journal
        says why. It is no reply of the model's and nothing is said in the log; the turn
        is counted as one in which nothing was said, as an empty reply was."""
        said = full_stop(f"No reply reached the game through {by}: {words}")
        self.note(said, kind=CUT_OFF_KIND)
        if self._open is not None and not self.agent.released:
            self._end_sample()

    def _asked(self, identity: str, verdict: str) -> None:
        """The consent question was put again to an identity that had left this station
        by its own word, and answered (package 37g, item 13): the answer is kept beside
        the leaving, so that the question is not put again at each start and a no is held
        to; the log says so."""
        a = self.agent
        kept = list(a.leavings)
        for i in range(len(kept) - 1, -1, -1):
            if kept[i].identity == identity and kept[i].how == OPTED_OUT:
                import dataclasses

                kept[i] = dataclasses.replace(kept[i], asked=verdict or "no answer")
                break
        else:
            # a checkpoint from before package 37g holds no leaving for it: one is made
            # from what was kept then, already answered
            kept.append(
                Leaving(
                    identity,
                    OPTED_OUT,
                    int(a.released_tick or self.world.clock.tick),
                    "",
                    a.released_reason,
                    final=bool(a.no_return),
                    asked=verdict or "no answer",
                )
            )
        a.leavings = tuple(kept)
        self.world.record(
            Severity.ROUTINE,
            "agent.asked_again",
            f"The consent question was put again to {identity or 'the model'}, an instance "
            f"of which had left the {self.station.name}'s station by its own word: the "
            f"answer is recorded as {verdict or 'no answer'}.",
            actor=self.actor,
            data={"station": self.station.name, "identity": identity, "verdict": verdict},
        )

    def _door_changed(self, identity: str, door: str) -> None:
        """The door behind a held station changed (package 37g, item 1): the same
        identity came to it through another door, or the same door started again, and
        the key of the seating before no longer serves. The log says so."""
        if door:
            self.door = door
        self.world.record(
            Severity.NOTABLE,
            "agent.door",
            f"The door behind the {self.station.name} changes: {identity or 'the model'} "
            f"takes up the station again through {door_words(door)}, and the door that "
            "held it before is no longer answered.",
            actor=self.actor,
            data={"station": self.station.name, "identity": identity, "door": door},
        )
        self.note(f"Took up the station again through {door_words(door)}.", kind="agent.stationed")

    def _note_aside(self, note: str) -> str:
        """A journal note written while the game has the floor: noted, and the model told
        that its stand-by, its wait or its pause goes on (package 31c)."""
        done = tools.call(self.world, self.station.name, "journal", {"note": note})
        if not str(done).startswith("Noted"):
            return str(done)
        a = self.agent
        if a.standing_by and a.stand_by is not None:
            return f"Noted in the journal; you are still standing by until {a.stand_by.words}."
        if a.paused:
            return "Noted in the journal; your turns are still paused."
        return "Noted in the journal; the game still has the floor until your next turn."

    def _play_door_acts(self, between_ticks: bool = True) -> None:
        """A replay makes the recorded stops from outside the loop at their points (a
        reseat among them, package 37, and the consent question's answer, package 37g,
        which are the acts made on a released station). A door makes its act between two
        of the World's ticks, never inside one, so an act of the tick the World is at is
        made only `between_ticks` (package 37i, item 5: game 10's officer, stood down by
        the runner at 08:00 on the 14th after a danger had woken him, was stood down in
        the replay by the order of a standing order fired inside that tick, before the
        harness's own step had woken him: one line short, and another digest)."""
        m = self.model
        if not isinstance(m, Playback):
            return
        while True:
            e = m.next_act(None if between_ticks else self.world.clock.tick)
            if e is None:
                return
            act = str(e["door"])
            if self.agent.released and act not in ACTS_ON_A_RELEASED_STATION:
                return
            self.door_act(
                act, str(e.get("reason", "")), str(e.get("by", "")), final=bool(e.get("final"))
            )

    # -- the deck (package 37; spec M5 §29; as package 37g has it) ------------------------

    def give_deck(self, by: str = "the captain", name: str = "") -> str:
        """`you have the deck` (or `Mr <name>, you have the deck`): the officer takes the
        deck. The sample that gives it says the captain's night orders (the book as it
        stands), every grant that stands and his general authority when it does, and
        carries the last handover note whole with one line of the journal's size
        (package 37g, items 11, 15, 17 and 18). Refused in words for a station with no
        authority, a released one, a name that is not the officer's, or a deck already
        his."""
        a = self.agent
        st = self.station
        if not st.has_authority:
            raise OrderError(f"The {st.name} has no authority to take the deck.")
        if a.released:
            raise OrderError(
                f"There is no {st.name} at the station now; {a.released_reason}. A model's "
                "door seats one (docs/agents/Harness.md)."
            )
        if name and st.person and _surname(name) != _surname(st.person):
            raise OrderError(
                f"{name} is not the {st.name}; {st.person} is at the station. Say "
                f"'{st.person}, you have the deck', or 'you have the deck'."
            )
        if a.paused:
            raise OrderError(
                f"The {st.name} is paused ({a.pause_reason}); say 'resume the {st.name}' "
                "first, and he has the deck as he held it, or give it when he is resumed."
            )
        if a.deck:
            raise OrderError(f"The {st.name} has the deck already, since {a.deck_stamp}.")
        world = self.world
        a.deck = True
        a.deck_tick = world.clock.tick
        a.deck_stamp = world.clock.stamp()
        a.deck_lost, self._deck_was = "", None
        standing = getattr(world, "standing", None)
        book = list(standing.book.lines()) if standing is not None else []
        notice = (
            DECK_GIVEN.format(by=f"{by[0].upper()}{by[1:]}", stamp=a.deck_stamp)
            + " The captain's night orders, his standing orders as the book holds them: "
            + " ".join(book)
        )
        a.notices.append(notice.rstrip())
        a.notices.append(self.granted_words())
        journal = self.journal_words()
        if journal:
            a.notices.append(journal)
        self.note(f"Took the deck from {by}.", kind="agent.deck")
        a.word = f"{a.word}\nYou have the deck." if a.word else "You have the deck."
        who = f"{st.person}, " if st.person else ""
        return (
            f"{who}you have the deck. The {st.name} has the deck; the captain's standing "
            "orders are his night orders."
        )

    def grants(self) -> tuple[Grant, ...]:
        """The named grants that stand (package 37g, item 17). A checkpoint from before
        holds them one to an order with the captain's words beside the verb
        (`AgentState.allowances`): each is read now as a grant given today would be, so
        that its words mean what they say, and kept with the rest."""
        a = self.agent
        if a.allowances:
            from freesail.orders.stations import read_grant

            ship = self.world.ship
            old = tuple(read_grant(ship, verb, words) for verb, words in a.allowances.items())
            a.grants = (*old, *a.grants)
            a.allowances = {}
        return tuple(a.grants)

    def granted_words(self) -> str:
        """What the captain's word allows now, for the sample that gives the deck: his
        general authority when it stands, and every named grant."""
        a = self.agent
        parts = []
        general = a.general_said()
        if general:
            parts.append(general)
        named = self.grants()
        if named:
            parts.append(
                "The captain's word allows by name: " + "; ".join(g.said() for g in named) + "."
            )
        if not parts:
            return "The captain's word allows nothing beyond your domain at present."
        return " ".join(parts) + (
            " What he has allowed stands until he takes it back or you leave the station."
        )

    def take_deck(self, by: str = "the captain") -> str:
        """`I have the deck`: the captain takes the deck and no more (package 37g, item
        11; the owner's ruling of 2026-10-05). The officer stays seated with the authority
        he was seated with: he reads, speaks, answers, writes his journal and stands by,
        and an order he gives is refused in words that say he has not the deck. What the
        captain's word allows stands, and has force when he has the deck again."""
        a = self.agent
        st = self.station
        By = f"{by[0].upper()}{by[1:]}"
        if not st.has_authority:
            raise OrderError(f"The {st.name} has no deck to give back.")
        if a.released:
            raise OrderError(f"There is no {st.name} at the station now; {a.released_reason}.")
        if not a.deck and a.deck_lost:
            # the harness took it from a paused or silent officer: the captain's word
            # keeps it, and `resume` no longer hands it back
            a.deck_lost, self._deck_was = "", None
            self.note(f"{By} keeps the deck.", kind="agent.deck")
            return (
                f"{By} has the deck. The {st.name} stays at the station, off watch, and "
                "does not have it again when he is resumed."
            )
        if not a.deck:
            raise OrderError(f"The {st.name} has not the deck; it is the captain's already.")
        self.note(f"{By} took the deck; I stay at the station, off watch.", kind="agent.deck")
        a.deck = False
        a.deck_tick, a.deck_stamp = None, ""
        a.word = f"{a.word}\nI have the deck." if a.word else "I have the deck."
        a.notices.append(
            f"{By} has taken the deck. You stay at your station, off watch: you read, "
            "speak, answer and keep your journal, and an order you give is refused until "
            "he gives you the deck again. What his word allows stands, and has force when "
            "you have the deck."
        )
        return f"{By} has the deck. The {st.name} stays at the station, off watch."

    def allow(
        self, verb: str, words: str = "", by: str = "the captain", grant: Grant | None = None
    ) -> str:
        """`you may <order> [<words>]`: the captain's word allows a named thing beyond the
        domain (`you may tack ship if the land closes within two miles`; `you may shape a
        course for Brest`). `grant` is the grant as `orders.stations` read it: the order,
        the thing his words name where the order's reader knows it (checked: a course
        shaped for Brest is for Brest), and his other words, kept as said and judged by
        the officer. Several grants of one order stand together. It stands through the
        deck going to and fro, has force only with the deck, and ends when the captain
        takes it back or the officer is stood down or leaves (package 37g, item 17)."""
        a = self.agent
        st = self.station
        if not st.has_authority:
            raise OrderError(f"The {st.name} gives no orders; there is nothing to allow it.")
        if a.released:
            raise OrderError(f"There is no {st.name} at the station now; {a.released_reason}.")
        g = grant if grant is not None else Grant(verb, words)
        same = (g.verb, g.key, g.thing)
        kept = tuple(x for x in self.grants() if (x.verb, x.key, x.thing) != same)
        if not g.key:
            # the order granted whole takes the place of an earlier grant of it whole
            kept = tuple(x for x in kept if x.verb != g.verb or x.key)
        a.grants = (*kept, g)
        said = g.said()
        a.word = f"{a.word}\nYou may {said}." if a.word else f"You may {said}."
        self.note(f"Allowed by {by}: {said}.", kind="agent.deck")
        domain = self.domain
        what = ""
        if g.key:
            what = f", and for no other {g.key.split(':', 1)[0]}"
        elif domain is not None and domain.course and verb in _course_verbs(domain):
            what = ": the course is his to alter, by any of its orders"
        return f"The {st.name} may {said}{what}, by {by}'s word."

    def disallow(self, verb: str, by: str = "the captain", grant: Grant | None = None) -> str:
        """`you may not <order> [<thing>]`: the grant taken back. Said of the order alone
        it takes back every grant of it; said with the thing a grant named (`you may not
        shape a course for Brest`), that one."""
        a = self.agent
        st = self.station
        named = self.grants()
        mine = [g for g in named if g.verb == verb]
        if not mine:
            raise OrderError(f"The {st.name} was not allowed to {verb}.")
        gone = mine
        if grant is not None and grant.key:
            gone = [g for g in mine if g.key == grant.key]
            if not gone:
                standing = "; ".join(g.said() for g in mine)
                raise OrderError(
                    f"The {st.name} was not allowed to {grant.said()}; what stands of that "
                    f"order: {standing}."
                )
        a.grants = tuple(g for g in named if g not in gone)
        said = "; ".join(g.said() for g in gone)
        a.word = f"{a.word}\nYou may not {said}." if a.word else f"You may not {said}."
        self.note(f"Taken back by {by}: {said}.", kind="agent.deck")
        return f"The {st.name} may not {said}; {by}'s word is taken back."

    def allow_general(self, words: str = "", by: str = "the captain") -> str:
        """`you may work the ship` (`you have general authority`, `you have my
        authority`): the captain's general authority to work the ship (package 37g, item
        18; the owner's rulings of 5 and 7 October 2026), the Captain's directions given
        beforehand. What it opens and what it keeps back are the domain's data
        (`Domain.general`, `Domain.kept_back`). It stands through the deck going to and
        fro, has force only with the deck, is said again in the sample that gives the
        deck, and lapses when the officer is stood down or leaves, or when the captain
        takes it back."""
        a = self.agent
        st = self.station
        if not st.has_authority or self.domain is None:
            raise OrderError(f"The {st.name} gives no orders; there is no authority to give it.")
        if a.released:
            raise OrderError(f"There is no {st.name} at the station now; {a.released_reason}.")
        a.general = True
        a.general_words = " ".join(str(words).split())
        a.word = f"{a.word}\nYou may work the ship." if a.word else "You may work the ship."
        a.notices.append(a.general_said())
        said = f" ({a.general_words})" if a.general_words else ""
        self.note(f"Given {by}'s general authority to work the ship{said}.", kind="agent.deck")
        return (
            f"The {st.name} has {by}'s general authority to work the ship{said}: "
            f"{GENERAL_WITHIN_WORDS}. Kept back: {GENERAL_KEPT_BACK_WORDS}. It has force "
            "while he has the deck."
        )

    def disallow_general(self, by: str = "the captain") -> str:
        """`you may not work the ship`: the general authority taken back."""
        a = self.agent
        st = self.station
        if not a.general:
            raise OrderError(f"The {st.name} has not {by}'s general authority to work the ship.")
        a.general, a.general_words = False, ""
        word = "You may not work the ship."
        a.word = f"{a.word}\n{word}" if a.word else word
        self.note(f"{by[0].upper()}{by[1:]}'s general authority taken back.", kind="agent.deck")
        still = self.grants()
        named = (
            " What he allowed by name stands: " + "; ".join(g.said() for g in still) + "."
            if still
            else ""
        )
        return (
            f"The {st.name} has no longer {by}'s general authority to work the ship; his "
            f"word is taken back.{named}"
        )

    def hand_over(self, note: str) -> str:
        """The officer's own order to give the deck back (`hand_over(note)`): the note
        said in the log and journaled (`agent.handover`), the deck the captain's, and the
        officer stays seated, as he does when the captain takes it (package 37g, item 11;
        the owner's ruling of 2026-10-07: parity for the officer's hand_over and the
        captain's). It is the first of the three ways of stopping, and says so."""
        a = self.agent
        st = self.station
        if not a.has_deck:
            return (
                f"The {st.name} has not the deck to hand over. To stand down from the "
                "station, stand_down(note); to withdraw, opt_out."
            )
        world = self.world
        self._say_handover(note, "handing over the deck")
        a.deck = False
        a.deck_tick, a.deck_stamp = None, ""
        world.record(
            Severity.NOTABLE,
            "agent.deck",
            f"The {st.name} hands over the deck and stays at the station; the captain has it.",
            actor=self.actor,
            data={"station": st.name, "deck": "handed over", "leaving": "deck"},
        )
        self.note("Handed over the deck; I stay at the station, off watch.", kind="agent.deck")
        return (
            "The deck is handed over with your note, and you stay at your station, off "
            f"watch ({LEAVING_WORDS['deck']}). The captain may give you the deck again. To "
            "stand down from the station, stand_down(note); to withdraw, opt_out."
        )

    def handover_note(self, note: str) -> str:
        """The watch's note without giving the deck back (`handover_note(note)`): journaled
        and said in the log, and the older exchanges folded into it at the end of this
        turn (`_fold_handover`). For a station with authority, with the deck or off
        watch: the conversation grows either way (package 37g, with the deck's new
        rule)."""
        self._say_handover(note, "the watch so far")
        self._handover_pending = note
        return (
            "Noted in the journal and said in the log; the exchanges before this turn are "
            "folded into the note at its end, the brief and your last turns kept whole."
        )

    def _say_handover(self, note: str, why: str) -> None:
        self.note(f"Handover note ({why}): {note}", kind=HANDOVER_KIND)
        self.world.record(
            Severity.NOTABLE,
            "agent.handover",
            f"{self.mark} Handover note, {why}: {note}",
            actor=self.actor,
            data={"station": self.station.name, "note": note, "why": why},
        )

    def _conversation_size(self) -> int:
        """The tokens of the conversation since the latest brief: by the model server's
        own count where the door gives it (package 37i, item 2: the request that brought
        the latest reply as the server counted it, `Reply.served_tokens`, and what came
        after it at the harness's rule), and never less than the harness's own rule (four
        characters a token), which is all there is before the first such reply and at a
        door that gives none. The larger of the two, since the server's count is of the
        request as the door sent it, which leaves out what the door's budget left out."""
        start = max((i for i, t in enumerate(self.turns) if t.role == OPERATOR), default=0)
        each = [
            tools.tokens(json.dumps(t.to_dict(), ensure_ascii=False)) for t in self.turns[start:]
        ]
        estimate = sum(each)
        for k in range(len(each) - 1, 0, -1):
            t = self.turns[start + k]
            served = getattr(t.content, "served_tokens", None) if t.role == MODEL else None
            if served and served.get("prompt"):
                return max(estimate, int(served["prompt"]) + sum(each[k:]))
        return estimate

    def handover_threshold(self) -> tuple[int, int] | None:
        """Where the handover note is asked for, and by how much the conversation must
        grow before it is asked again (package 37g, item 8; package 37i, item 3): when it
        has left less than the reserve of the door's context (`reserve_tokens`, the door's
        own, which the local runner sends in tokens whether the owner gave it as tokens or
        as a share; else `HANDOVER_RESERVE_SHARE` of the context and never less than
        `HANDOVER_RESERVE_TOKENS`), and never earlier than
        `HANDOVER_AT_FRACTION` of it. None when the door has said no context."""
        budget = self.budget_tokens
        if not budget:
            return None
        reserve = int(
            self.reserve_tokens or max(HANDOVER_RESERVE_SHARE * budget, HANDOVER_RESERVE_TOKENS)
        )
        at_fraction = HANDOVER_AT_FRACTION * budget
        if budget - reserve > at_fraction:
            return int(budget - reserve), max(1, reserve // 4)
        return int(at_fraction), max(1, int(HANDOVER_ASK_AGAIN_FRACTION * budget))

    def _ask_for_handover(self) -> None:
        """At the end of a turn: when the door has said what context it gives the model
        and the conversation since the brief has left less than the reserve of it, the
        next sample asks for the note (once; again when it has grown further)."""
        where = self.handover_threshold()
        if where is None or not self.station.has_authority or self.agent.released:
            return
        threshold, again = where
        budget = int(self.budget_tokens or 0)
        size = self._conversation_size()
        if size < threshold:
            return
        if self._handover_asked_at and size - self._handover_asked_at < again:
            return
        self._handover_asked_at = size
        self.agent.notices.append(HANDOVER_ASK.format(size=size, budget=budget))

    def _fold_handover(self, note: str) -> None:
        """The older exchanges replaced by the note as one data turn (spec M4 open item
        9b): the latest brief kept, then the note with every reading as it stood, then the
        last `HANDOVER_KEEP_TURNS` turns whole. The books whose results are folded away
        are left behind; the stream's revision moves, so a door reads its turns again."""
        start = max((i for i, t in enumerate(self.turns) if t.role == OPERATOR), default=0)
        body = self.turns[start + 1 :]
        if len(body) <= HANDOVER_KEEP_TURNS + 1:
            return  # nothing older than the kept turns to fold
        # the server's count of a request before the fold is not the folded
        # conversation's: the next reply brings the count afresh (package 37i)
        kept = [
            Turn(MODEL, dataclasses.replace(t.content, served_tokens=None))
            if t.role == MODEL and getattr(t.content, "served_tokens", None)
            else t
            for t in body[-HANDOVER_KEEP_TURNS:]
        ]
        cut = start + 1 + len(body) - HANDOVER_KEEP_TURNS
        folded = Turn(
            DATA,
            {
                "tick": self.world.clock.tick,
                "stamp": self.world.clock.stamp(),
                "reason": "the handover note",
                "handover": note,
                "folded": HANDOVER_FOLDED,
                "readings": dict(self._told or tools.readings_words(self.world)),
            },
        )
        self.turns = [*self.turns[: start + 1], folded, *kept]
        shift = cut - (start + 2)
        for b in self.books:
            if b.at is None:
                continue
            if b.at < cut:
                if b.state == OPEN:
                    b.state = LEFT_BEHIND
                b.at = None
            else:
                b.at -= shift
        self.revision += 1
        # asked again only once the folded conversation has grown by the fraction
        self._handover_asked_at = self._conversation_size()

    # -- taking a released station again (packages 37, 37b and 37g) ----------------------

    def reseat(
        self,
        model: Model,
        *,
        identity: str = "",
        door: str = "",
        save: SaveFn | None = None,
        door_note: str | None = None,
    ) -> str:
        """A released station taken again (package 37; as often as it is asked back,
        package 37b; and since package 37g by the same identity or by another: the
        owner's ruling of 2026-10-05, that a stand-down never locks a station out of a
        game). The one rule decides (`seating`): an identity that left this game for
        good is refused, at any station; one that left by its own word and has not been
        asked again is refused until the door's consent step has put the question
        (`door_act` "asked"); every other is seated. The brief is sent again as it
        stands, opening its situation with the last handover or stand-down note; the
        deck is the captain's until he gives it; the journal is kept, and the log says
        who relieved whom. What the captain's word allowed lapsed when the station was
        left."""
        a = self.agent
        st = self.station
        if not a.released:
            raise OrderError(
                f"The {st.name} is at the station ({a.words()}); nothing to seat again."
            )
        decided = seating(self.world, st.name, identity)
        if not decided.ok:
            raise OrderError(decided.why)
        if decided.ask_again:
            raise OrderError(
                f"{identity} left this game by its own word, and the consent question is "
                f"put again before an instance of it is seated: {decided.asked_why}"
            )
        self.model = model
        if save is not None:
            self.save_fn = save
        if door_note is not None:
            self.door_note = door_note
        self.door_act("reseat", identity, door)
        return f"The {st.name} takes the station again, the {ordinal_words(a.seatings)} seating."

    def _reseat_now(self, identity: str, by: str) -> None:
        a = self.agent
        world = self.world
        left = a.released_reason
        was = self.model_name
        relieved = was != identity
        a.relieved = was if relieved else ""
        self.model_name = identity
        self.door = by if by in ("mcp", "runner", "repl", "") else self.door
        through = door_words(by)
        a.seatings += 1
        a.state = STATIONED
        a.released_reason = ""
        a.released_tick = None
        a.left_by = ""
        a.no_return = False
        a.deck = False
        a.deck_tick, a.deck_stamp = None, ""
        a.deck_lost, self._deck_was = "", None
        # what the captain's word allowed lapsed when the station was left (package 37g)
        a.grants, a.allowances = (), {}
        a.general, a.general_words = False, ""
        a.nudged_for = None
        a.repeat_text, a.repeat_digest, a.repeat_count = None, None, 0
        a.empty_count = 0
        a.question, a.word = None, None
        a.last_heard_tick = world.clock.tick
        a.last_sample_tick = world.clock.tick
        self._orders = []
        self._danger_orders = ()
        self._nudge_unread, self._nudge_text = False, None
        self._open = None
        self._paused_real = None
        self.stand_by_ends_turn = True
        # who sits, and through which door: a model by its name; a door with no model
        # named (a human at the terminal) by the door; the game's own scripted station
        # by neither
        if identity:
            at = f" ({identity}, through {through})"
        else:
            at = f" (through {through})" if by else ""
        before = was or "the holder before it"
        relieving = f", relieving {before}" if relieved else ""
        world.record(
            Severity.NOTABLE,
            "agent.stationed",
            f"The {self.station.name} takes the station again{at}{relieving}: the "
            f"{ordinal_words(a.seatings)} seating; it had {full_stop(left)}",
            actor=self.actor,
            data={
                "station": self.station.name,
                "seating": a.seatings,
                "left": left,
                "identity": identity,
                "relieved": a.relieved,
            },
        )
        whose = f"the station, held by {before}, had" if relieved else "I had"
        self.note(
            f"Seated again, the {ordinal_words(a.seatings)} seating; {whose} {full_stop(left)}",
            kind="agent.stationed",
        )
        self._seen_log = len(world.log)
        self._sample_seen = len(world.log)
        self._refresh_station()
        self.resend_brief()
        self._wait_from = (len(world.log), world.clock.stamp())
        self._pass_kept_words()
        self._sample("seated again")

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
        if a.has_deck and sb.until_tick is not None:
            # a station with the deck stands by until an event or a bell, not for longer
            # (package 37; the cold review's third item): the deck is not left
            if sb.until_tick - world.clock.tick > STAND_BY_WITH_DECK_MAX_S:
                return (
                    f"The {self.station.name} has the deck and stands by until an event or a "
                    f"bell, not for {words}: say a bell ('eight bells', 'a glass'), an "
                    "event's words, 'a notable event' or 'an urgent event'; the standing "
                    "orders hold the deck meanwhile, and an urgent line wakes you whatever "
                    "you stand by for."
                )
        if a.has_deck and sb.until_tick is None:
            # ...and a wait that cannot end is refused when it is asked, and a wait for an
            # event ends at the next eight bells if the event has not come (package 37g,
            # item 4; game 9: "six bells" asked in the last dog watch)
            cannot = self._cannot_come(sb)
            if cannot is not None:
                return cannot
            if sb.event != EIGHT_BELLS:
                sb = StandBy(sb.words, event=sb.event, severity=sb.severity, bound=EIGHT_BELLS)
        # taken while the game has the floor (a door's call out of turn, package 31c): the
        # wait the model is in goes on as a stand-by, its digest from the wait's start
        out_of_turn = self._open is None
        a.state = STANDING_BY
        a.stand_by = sb
        a.last_heard_tick = world.clock.tick
        line = f"{self.mark} Standing by until {words}."
        if a.has_deck:
            line = (
                f"{self.mark} The {self.station.name} stands by until {words}; the standing "
                "orders hold the deck."
            )
        world.record(Severity.ROUTINE, "agent.stood_by", line, actor=self.actor, data=sb.to_dict())
        if not out_of_turn:
            self._wait_from = (len(world.log), world.clock.stamp())
        self._stood_at = (words, world.clock.stamp())
        self.journal.append(world, f"Stood by until {words}.", kind="agent.stood_by")
        # standing by is the answer to a nudge (spec §11), and a stand-by that answers a
        # nudge about the station's orders clears the chain with it (package 37g, item 5;
        # the review's 5.4: it forgave the nudge and kept the chain, so the next order
        # nudged again at four, five, six, and never paused). A nudge given in this same
        # reply has not been read, and is no answer: it stands, with its chain.
        if a.nudged_for == "contrary":
            if not self._nudge_unread:
                a.nudged_for = None
                self._orders = []
        else:
            a.nudged_for = None
        a.repeat_text, a.repeat_digest, a.repeat_count = None, None, 0
        self._sample_repeated = False
        # what it waits for may have come while the call was on its way (package 31c):
        # then it is delivered at once, at the next tick, not skipped to the next of it
        self._stand_by_watch = None
        self._stand_by_due = self._in_flight(sb, out_of_turn)
        return f"Standing by until {words}; you will be sampled then."

    def _cannot_come(self, sb: StandBy) -> str | None:
        """Why a station with the deck cannot stand by for this, in words, or None when
        it can: a bell that will not be struck before the next eight bells, where its
        wait ends, answered with the bells that will; an event that cannot come as she is
        (`readings.EventSpec.needs`: the turn of the tide at the anchor while she is under
        way, the pilot aboard with no sail in sight), answered with the nearest that
        can."""
        name = self.station.name
        spec = R.EVENTS.get(sb.event) if sb.event is not None else None
        if spec is None:
            return None
        if spec.kind == "clock.bell":
            coming = _bells_to_come(self.world.clock.ship_time)
            said = [w for w, _ in coming]
            if sb.event not in said:
                listed = ", ".join(f"{w} ({at})" for w, at in coming)
                return (
                    f"The {name} has the deck, and its wait ends at the next eight bells: "
                    f"{sb.words} will not be struck before then. The bells to come before "
                    f"it: {listed}. Say one of them, 'a glass', or an event's words."
                )
            return None
        if spec.needs is not None:
            why = spec.needs(self.world)
            if why:
                return (
                    f"The {name} has the deck and cannot stand by until {sb.words} as she "
                    f"is. {full_stop(why)}"
                )
        return None

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
        return "Heard." if question is not None else ANSWER_UNASKED

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
            self._say(text, own_word=True)
        a.last_heard_tick = world.clock.tick
        digest = None
        if a.standing_by and a.stand_by is not None:
            digest = self._stood_by_digest("your own word")
            until = a.stand_by.words
            a.state = STATIONED
            a.stand_by = None
            self._stand_by_due, self._stand_by_watch = None, None
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

    def put_question(self, question: str, by: str = "", officer: str = "the captain") -> str:
        """`ask the <station> <question>`: the question is answered at this tick, after
        the order is logged (`on_order`). `by` names a standing order that asks it
        (package 31c), which the log line names as the speaker, in `officer`'s name; the
        question itself is put as the captain's own would be."""
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
        if by:
            return f"By {by}: {officer} asks the {self.station.name}: {question}?"
        return f"Asked the {self.station.name}: {question}?"

    def put_word(self, words: str, by: str = "", officer: str = "the captain") -> str:
        """`tell the <station> <words>` (package 29, the owner's tenth item): the words go
        to the model in its next sample under `word`, not `question`: no answer is owed,
        and nothing that waits on a question is set by them. The sample is taken at the
        next tick (so that an `ask` given at once after rides in the same sample); a
        stand-by is woken by it, a turn already open has it folded in. `by` names a
        standing order that says it (package 31c): the log line names it as the speaker
        ("By standing order 'sea': the captain to the watcher: ..."), and the words ride
        the sample as the captain's own would."""
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
        if by:
            return f"By {by}: {officer} to the {self.station.name}: {words}"
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

    def stand_down_by_word(self, note: str = "") -> str:
        """The station's own `stand_down(note)` (package 37g, item 12): the amicable save
        and exit, for any station. The note is journaled and said in the log for whoever
        sits there next; the game is saved; the station is released and may be taken
        again, by the same model or by another. The second of the three ways of
        stopping: it is not the deck given back, and it is not a withdrawal (no consent
        question follows it)."""
        note = " ".join(str(note).split())
        if not note and self.agent.has_deck:
            # with the deck, the watch is handed on with its note (package 37l; the review
            # of gate 5c's playtests, G13: `stand_down` took a note and did not insist on
            # one): asked for, and nothing done till it comes
            return (
                "You have the deck: a stand-down hands the watch on, and wants its handover "
                "note. Call stand_down again with the note (what happened, what was "
                "ordered, what you noticed, what you are watching for); nothing has been "
                "done yet."
            )
        if note:
            self._say_handover(note, "standing down, for whoever sits here next")
        self.stand_down("its own word", by=f"the {self.station.name}")
        noted = (
            "your note is journaled and said in the log for whoever sits here next, "
            if note
            else "no note was left (none is asked without the deck), "
        )
        return (
            f"You have stood down ({LEAVING_WORDS['stand down']}): the game is saved, "
            f"{noted}and the station is released. It may be taken again in this game by "
            "this model or by another, and no consent question is put to a model whose "
            "yes still stands."
        )

    def stand_down(self, reason: str, by: str = "the captain") -> None:
        """Journal `agent.stopped` with the reason, release the station, save. The save
        comes last so that the file holds the exit: the journal entry, the log line and
        the released station (package 28; the owner reads the journal in the save). The
        line says which of the three ways of stopping this is (package 37g): a
        stand-down, after which the station may be taken again."""
        if self.agent.released:
            return
        said = full_stop(f"{by}: {reason}")  # one full stop after a reason ending in one
        text = (
            f"The {self.station.name} stood down by {said} The station is released and "
            "may be taken again. The game is saved."
        )
        self.note(f"Stood down by {said}", kind="agent.stopped")
        self.world.record(
            Severity.NOTABLE,
            "agent.stopped",
            text,
            actor=self.actor,
            data={"reason": reason, "by": by, "leaving": "stand down"},
        )
        self._release(f"stood down by {by}: {reason}", STOOD_DOWN, by=by)
        self._save(f"the {self.station.name} stood down: {reason}")

    def leave(self, reason: str, how: str = "the token", final: bool = False) -> None:
        """The opt-out: journal `agent.opted_out`, release, save, end the loop (the save
        last, so that the file holds the exit). The line says which of the three ways of
        stopping this is (package 37g): a withdrawal. `final` is the opt_out tool's own
        setting and is read from nothing else (never from the token, never from a word
        in the reason): that identity is not seated again in this game, at any station,
        the station itself stays open to another, and the log says it was final. No order
        undoes it."""
        if self.agent.released:
            return
        reason = " ".join(reason.split())
        why = f": {reason}" if reason else ", giving no reason"
        # one full stop after a reason ending in one (package 31c; playtest 11's finding 12,
        # the release line's "journal..")
        said = full_stop(f"{how}{why}")
        who = self.model_name or f"the {self.station.name}'s model"
        final_words = (
            f" This was final: {who} is not seated again in this game, at any station, and "
            "the station stays open to another."
            if final
            else ""
        )
        self.note(f"Left the game by {said}{final_words}", kind="agent.opted_out")
        data: dict[str, Any] = {"reason": reason, "how": how, "leaving": "withdrawal"}
        if final:
            data["final"] = True
        self.world.record(
            Severity.NOTABLE,
            "agent.opted_out",
            f"The {self.station.name} has left the game by {said}{final_words} A "
            "withdrawal: the game is saved and the station is released.",
            actor=self.actor,
            data=data,
        )
        left = f"left the game{why}"
        if final:
            left = f"{left.rstrip('.!?')}, for good"
        self._release(left, OPTED_OUT, by=how, gave=reason, final=final)
        self.agent.no_return = final
        self._save(f"the {self.station.name} opted out")

    def _release(
        self,
        reason: str,
        left_by: str = "",
        *,
        by: str = "",
        final: bool = False,
        gave: str | None = None,
    ) -> None:
        a = self.agent
        a.state = RELEASED
        a.left_by = left_by
        a.released_reason = reason
        a.released_tick = self.world.clock.tick
        a.question = None
        a.stand_by = None
        self._stand_by_due, self._stand_by_watch = None, None
        self._open = None
        # the deck goes back with the station, and what the captain's word allowed lapses
        # (package 37g, items 17 and 18: a grant ends when the officer is stood down or
        # leaves)
        a.deck = False
        a.deck_lost, self._deck_was = "", None
        a.grants, a.allowances = (), {}
        a.general, a.general_words = False, ""
        if left_by:
            # how this identity left, kept by identity (package 37g, items 13 and 14)
            a.leavings = (
                *a.leavings,
                Leaving(
                    self.model_name,
                    left_by,
                    self.world.clock.tick,
                    self.world.clock.stamp(),
                    reason=reason if gave is None else gave,
                    final=bool(final),
                    by=by,
                ),
            )

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
            # the inputs before the stationing, by which a replay seats it (package 37d)
            "stationed_after_inputs": self._start_after_inputs,
            "state": a.state,
            "state_words": a.words(),
            "last_sample_tick": a.last_sample_tick,
            "model_name": self.model_name,
            "door": self.door,
            "stand_by_ends_turn": self.stand_by_ends_turn,
            "transcript": list(self.transcript),
            # a station with authority (package 37): the deck, as the save reads it; a
            # replay rebuilds it from the captain's journaled orders
            "deck": a.deck,
            "seatings": a.seatings,
            "budget_tokens": self.budget_tokens,
            # package 37g: the identity and the door of the first seating, which a replay
            # seats the station under (a later seating may be another model's, and its
            # reseat act says whose); and the handover's reserve, where the door gave one
            "first_model_name": (
                self.model_name if self.first_model_name is None else self.first_model_name
            ),
            "first_door": self.door if self.first_door is None else self.first_door,
            "reserve_tokens": self.reserve_tokens,
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
        if w.clock.tick < tick or len(w.journal) < int(e.get("after_orders") or 0):
            return False
        # an act made after an input that is no order (package 37i; absent before it)
        return "door" not in e or len(w.inputs) >= int(e.get("after_inputs") or 0)

    def reply(self, turns: Any) -> Reply | None:
        if self.at >= len(self.entries):
            return None
        e = self.entries[self.at]
        if "reply" not in e or not self._due(e):
            return None
        self.at += 1
        self.calls += 1
        return Reply.from_dict(e["reply"])

    def next_act(self, inside_tick: int | None = None) -> dict[str, Any] | None:
        """The next stop from outside the loop, when it is the next entry and is due;
        `inside_tick`, the tick the World is inside: an act of that tick waits for its
        end (package 37i)."""
        if self.at >= len(self.entries):
            return None
        e = self.entries[self.at]
        if "door" not in e or not self._due(e):
            return None
        if inside_tick is not None and int(e.get("tick") or 0) >= inside_tick:
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
            start_after_inputs=(
                None
                if record.get("stationed_after_inputs") is None
                else int(record["stationed_after_inputs"])
            ),
        )
        # seated under the first seating's identity and door (package 37g); the reseats'
        # acts move them on as the replay reaches them. A save from before has one
        # identity throughout.
        first = record.get("first_model_name")
        h.model_name = str(record.get("model_name") or "") if first is None else str(first)
        door = record.get("first_door")
        h.door = str(record.get("door") or "") if door is None else str(door)
        h.stand_by_ends_turn = bool(record.get("stand_by_ends_turn", model is not None))
        h.budget_tokens = record.get("budget_tokens") or None
        h.reserve_tokens = record.get("reserve_tokens") or None
        if h.due_to_start():
            h.start()
        out.append(h)
    return out


# The journal's kind for a turn that ended with no reply to be had (package 37i).
CUT_OFF_KIND = "agent.cut_off"

# The acts from outside the loop that are made on a released station (`door_act`).
ACTS_ON_A_RELEASED_STATION = ("reseat", "asked")

# The bell a station with the deck is bound by (package 37g, item 4).
EIGHT_BELLS = "eight bells"


def _bells_to_come(now: Any) -> list[tuple[str, str]]:
    """The bells from now to the next eight bells, each with its hour: the ones a station
    with the deck may stand by for (`[("one bell", "18:30"), ..., ("eight bells",
    "20:00")]`). Bells are struck on the half hours (`units.bells_at`)."""
    import datetime as dt

    from freesail import units

    t = now.replace(second=0, microsecond=0)
    t += dt.timedelta(minutes=30 - t.minute % 30)
    out: list[tuple[str, str]] = []
    for _ in range(16):  # the next eight bells is at most a watch of half hours away
        n = units.bells_at(t)
        if n is not None:
            words = "one bell" if n == 1 else f"{number_words(n)} bells"
            if n in (7, 8):
                words = f"{'seven' if n == 7 else 'eight'} bells"
            out.append((words, t.strftime("%H:%M")))
            if n == 8:
                break
        t += dt.timedelta(minutes=30)
    return out


def _course_verbs(domain: Any) -> set[str]:
    """The verbs of the course, for the grant's line: the domain's course by name, and
    the vocabulary's verbs whose object is a heading or points."""
    from freesail.orders.vocabulary import load_vocabulary

    verbs = load_vocabulary().verbs
    return {v for v, spec in verbs.items() if domain.is_course(v, spec.object)}


def leaving_of(reply: Reply, found_in: str) -> tuple[str, str, bool]:
    """A reply that holds the token leaves: (the reason given, how it left in words,
    whether it was final). **`final` is read from the `opt_out` tool's own setting and
    from nothing else** (package 37g, item 13; the owner's ruling of 2026-10-07, "careful
    of false positives"): not from the token, not from a word in the reason. The token
    written in the same reply as `opt_out(final=true)` does not drop it (until this
    package the token scan came first and left without the flag). One function, which
    every door's reply comes through, in turn (`Harness._take_reply`) and out of it
    (`remote.Desk`)."""
    out = next((c for c in reply.calls if c.name == "opt_out"), None)
    final = out is not None and tools.truthy(out.args.get("final", False))
    reason = _reason_after_token(reply, found_in)
    if out is not None and not reason:
        reason = " ".join(str(out.args.get("reason", "")).split())
    return reason, ("the opt_out tool" if out is not None else "the token"), final


# ---------------------------------------------------------------------------
# The one rule for taking a station (package 37g, items 13 and 14): every door asks it
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Seating:
    """What the one rule says of an identity asking for a station: whether it may be
    offered (consent permitting; `why` the refusal in words when not), whether the
    consent question must be put again first (`ask_again`, with `asked_why` the words
    the question is put with: that an instance left, when, and the reason it gave), and
    the leaving it rests on, with the station it was at."""

    ok: bool
    why: str = ""
    ask_again: bool = False
    asked_why: str = ""
    left: Leaving | None = None
    left_at: str = ""


def _leavings(h: Harness) -> list[Leaving]:
    """A station's leavings. A checkpoint from before package 37g holds none: the one it
    was last left by is read from what was kept then (`left_by`, `no_return`), and an
    opt-out saved before package 37b, which kept no record of how the station was left,
    reads as a stand-down (right for the one such save there is, by the owner's answer
    of 2026-10-05: the watcher's `opt_out` on the Harpy was made at the captain's word,
    to stand down with a save)."""
    a = h.agent
    out = list(a.leavings)
    if (
        a.released
        and not h.conversation
        and a.released_tick is not None
        and not any(x.tick == a.released_tick for x in out)
    ):
        out.append(
            Leaving(
                h.model_name,
                a.left_by or STOOD_DOWN,
                int(a.released_tick),
                "",
                reason=a.released_reason,
                final=bool(a.no_return),
            )
        )
    return out


def barred(world: Any, identity: str) -> tuple[str, Leaving] | None:
    """The station and the leaving by which an identity left this game for good
    (`opt_out` with `final`), or None. It bars the identity from the game, at any
    station; the station itself stays open to another (the owner's ruling)."""
    for name, h in (getattr(world, "agents", None) or {}).items():
        for left in _leavings(h):
            if left.final and left.identity == identity:
                return name, left
    return None


def seating(world: Any, station: str, identity: str) -> Seating:
    """The one rule every door uses when a station is asked for (package 37g, items 13
    and 14; the review's section 6: the rule lived in one door, `Harness.reseat` seated
    an opted-out station unasked, and the REPL could not seat again at all).

    - An identity that left this game for good is not seated again in it, at any station.
    - An identity whose last leaving in this game was by its own word (the token, or
      `opt_out`) is asked for its consent again before it is seated, once: the answer is
      kept (`door_act` "asked"), so a no is held to and the question is not put again at
      each start. The game's own scripted station and a person at the terminal have no
      consent step and are not asked.
    - Every other identity may take a station that is released: the one that stood down
      from it, or another, which gives its own consent as any model does.

    Whether the station is held now is the caller's to see (a station that is held is
    taken by nobody else); so is the consent record."""
    bar = barred(world, identity)
    if bar is not None:
        at, left = bar
        when = f" at {left.stamp}" if left.stamp else ""
        why = f": {left.reason}" if left.reason else ""
        return Seating(
            False,
            f"{identity or 'The model at that station'} left this game for good{when}, at "
            f"the {at}'s station{why}. It is not seated again in this game, at any station; "
            "the station stays open to another model.",
            left=left,
            left_at=at,
        )
    latest: tuple[str, Leaving] | None = None
    for name, h in (getattr(world, "agents", None) or {}).items():
        for left in _leavings(h):
            if left.identity == identity and (latest is None or left.tick >= latest[1].tick):
                latest = (name, left)
    if latest is None:
        return Seating(True)
    at, left = latest
    if identity and left.how == OPTED_OUT and not left.asked:
        when = f" at {left.stamp}" if left.stamp else ""
        how = f" by {left.by}" if left.by else ""
        gave = f"giving this reason: {left.reason}" if left.reason else "giving no reason"
        return Seating(
            True,
            ask_again=True,
            asked_why=(
                f"an instance of this model left this game by its own word{when}{how}, at "
                f"the {at}'s station, {full_stop(gave)}"
            ),
            left=left,
            left_at=at,
        )
    return Seating(True, left=left, left_at=at)


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


def full_stop(text: str) -> str:
    """The text as a sentence: a full stop after it, unless it ends in one already (or in a
    question or an exclamation mark), so that a reason the model gave with its own stop
    is not given a second (package 31c)."""
    text = text.rstrip()
    return text if text.endswith((".", "!", "?")) else f"{text}."


def _stamp(e: Event) -> str:
    """A line's stamp as the model reads it (`tools.log_line`)."""
    return str(tools.log_line(e)["stamp"])


def _ran_before(results: list[dict[str, Any]]) -> str | None:
    """One line naming the calls of a reply that ran before its stand-by, each with its
    result cut short (a reading tool without it), for the sample that ends the stand-by
    (package 30b); None when none ran. A call not run (over the budget) has no `args`."""
    ran: list[str] = []
    for r in results:
        if "args" not in r:
            continue
        name = str(r["name"])
        if name in READING_TOOLS:
            ran.append(f"{name} (not shown here; call it again to see it)")
            continue
        text = " ".join(str(r.get("result", "")).split())
        if len(text) > RAN_RESULT_CHARS:
            text = text[: RAN_RESULT_CHARS - 3].rstrip() + "..."
        ran.append(f"{name} ({text})" if text else name)
    if not ran:
        return None
    return "Before you stood by, in the same reply, these ran: " + "; ".join(ran) + "."


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


def _log_line(x: Event | Rollup, world: Any = None) -> dict[str, Any]:
    """A shown line as the model sees it (`tools.log_line`, with who gave an order: the
    world is given to look up whose a standing order is); a roll-up with its hour."""
    if isinstance(x, Rollup):
        return {
            "tick": x.tick,
            "stamp": x.stamp,
            "severity": x.severity.value,
            "kind": x.kind,
            "text": x.text,
        }
    return tools.log_line(x, world)


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


def _surname(name: str) -> str:
    """A person's surname as the deck's giving names him ('Mr Pearce', 'Pearce', 'Mr.
    Fredk. Pearce'): the last word, lower-cased, a comma or a stop dropped."""
    words = [w.strip(".,") for w in str(name).split()]
    return words[-1].lower() if words else ""
