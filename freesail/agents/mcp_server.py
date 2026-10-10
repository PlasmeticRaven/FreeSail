"""The MCP bridge (spec M4 §13 as revised; package 28b, the waiting and the lost sample
package 28c): the door for Claude Desktop, Claude Code and any other MCP client, over
stdio, on the Python MCP SDK's server class (`MCPServer`, which is what the SDK called
`FastMCP` before its version 2). It is a client of the running game and owns no World.

    python -m freesail.agents.mcp_server --game http://localhost:8000 --model-name "<identity>"
        [--station watcher] [--wait 200] [--session play|test] [--ask-again]

The owner starts the game first, in the browser (`freesail.ui.server`) or the console
with `--agents-port`, and plays it there; this bridge carries the model's tool calls to
the game's agent API (`remote.GameClient`) and the game's turns back. The harness, the
consent gate, the token scan and the log are all in the game's process.

**Stationing.** At the first contact of a session (the first tool call, the `brief`
prompt or resource), not when the client starts the bridge: Claude Desktop starts its
servers when it opens, before any chat and perhaps before the game, and a station should
be taken when a model first looks. The model name the owner gives (`--model-name`; the
protocol names the client application, not the model) goes to the game, which runs the
consent gate: no record, the consent brief (`answer` and `opt_out` the tools that run);
a yes, the station's brief; anything else, refused in words. A station already manned
by the same model name is attached to (a restarted client): the game sends the brief
again as it stands and the conversation goes on. If the game cannot be reached, the call
says so and the next call tries again.

**The brief first.** The first tool call returns the brief (the consent brief, or the
station's with the first sample) and is not itself run (`opt_out` and the token
excepted), as package 28 did. The brief is also the `brief` prompt and the
`freesail://brief` resource.

**One tool call, one reply.** Each tool call is one reply delivered to the game (`raw`
is the whole call, so the token scan reads every argument), and returns the result the
game gives. `say(text)` puts the words in the log under the station's mark and hands the
floor back; `stand_by(until)` stands by and hands it back. Both then **hold the call
open until the model's next turn opens** (the glass, a notable event, the end of a
stand-by, an urgent line, a question from the captain) and return it, its first line
saying whose turn it is ("Your turn is open: sample at ..."). While a call is held the
bridge sends MCP progress notifications every `PROGRESS_EVERY_S` (standard clients
reset their request timeout on progress), each saying how long it has waited and what
the game has logged of note, and it gives up at the ceiling (`--wait`, `MCP_WAIT_S`,
two hundred seconds by default, under the four minutes after which Claude Desktop cuts a
call whatever the progress: package 31c, playtest 11's finding 2): the result then says
so ("Still waiting ..."), with since when the model has waited, until what, and the
notable lines logged since, in the log's own words, so a stand-by is a decision not to be
sampled and not a decision to be blind; calling `stand_by` again continues the same
wait, and `say(text)` ends it at the model's own word and opens its turn. A `stand_by`
while the game has the floor and the model is not standing by is taken from then (so the
bell it names, falling before the next turn, wakes it); one while it is standing by
continues that wait. For a client that cuts shorter calls, `--wait 50` waits in
fifty-second calls, each with that digest (`docs/agents/Harness.md`). The game runs on its own clock
meanwhile: what happens while the model holds the floor is added to its open turn (the
harness's fold), and the next call that reads it gets everything since its last reply.

**Nothing is lost when a call is cut off** (package 28c; playtest 3's lost sample). The
mechanism was this: a `stand_by` waiting for the next turn got it from the game (the
`GameClient`'s cursor advanced and the bridge kept the turns as seen) and returned it as
the call's result; but the client had given up on the call (its timeout, or the owner
stopping the model), the SDK dropped the result unwritten, and the model's next call, a
`stand_by` again, went to the game as its reply to a turn it had never seen: the
captain's question in it was answered by a stand-by. Now each call is run under an id;
a call the client cancels (`notifications/cancelled`, which the SDK turns into a
cancellation of the handler) is marked cut off, its wait stops within
`WAIT_SLICE_S`, and its result, once it has one, is kept as undelivered. The model's
next call returns the undelivered result first and is not itself run (the token and
`opt_out` excepted), as the brief comes first; a result that brought no turn (the wait
ended empty) is only noted after the next call's own result, so a client that cuts
every long call does not cost the model every other call. The rule, and why it holds:
a result reaches the model only as the result of a call the SDK answered, the SDK
answers a call only when the handler returns uncancelled, and a handler that returns
cancelled leaves its result to the next call; so every turn the game sent is either in
a result the client received or in the next call's result, once. (The one gap is a
client that gives up without telling the server, which MCP's cancellation rule forbids;
a client that times out sends `notifications/cancelled`.)

Two more roads to the same loss are closed the same way. A turn that opened while no call
was waiting (the last call had come back "Still waiting" and the model had gone on in
the chat) is fetched before the model's next call is delivered, and returned first, the
call not run (`_unread_turn`). And the answer to a delivered reply carries the turns from
the cursor, which may hold a fold made before the reply arrived: a fold goes with the
result of the call in the open turn (`_with_folds`), or, when the call handed the floor
back, with its result as past, never read as a turn that has opened (`_hand_back`). The
bridge counts what its results have carried (`_shown`), so a sample or a fold past that
count is one the model has not read.

**The token.** The chat's text never reaches the game, so the token counts in every
argument of every tool call, and `opt_out` is always listed. Out of turn too: the game
looks for it in a call that comes when the floor is not the model's.

**The seating's key, and a game that has none for this door** (package 37g, items 1 and
8). The game gives the door a key when it stations, and the `GameClient` sends it with
every call; a call the game refuses for want of it (another door holds the station now)
stops this bridge, in the game's own words, and it does not ask again of itself: two
doors under one model's name would otherwise take the seat from each other at every
call. When the game answers that it holds **no** station for this door (404: it was
restarted, or another game was started in its place), the bridge forgets its seating and
asks for its station again, through the ordinary gate, and the brief comes first as at
the first contact (until this package Claude Desktop had to be restarted after every
restart of the game). It does not ask again after a release: a station stood down is the
captain's or the model's decision, and a new seating is the owner's to start.

**The wait adapts when a call is cut short** (package 37g, item 8; the review's 5.4: a
cloud relay cut calls at a minute, and the bridge named `--wait 50` and went on waiting
two hundred seconds). A waiting call the client cancels after fewer seconds than the
wait shortens the wait to a little under what the client allowed (`WAIT_MARGIN_S` under
it, never below `WAIT_FLOOR_S`), and the note after the next result says so.

**The shelf** (package 28d). The model's conversation lives in the MCP client, not in
the game, so `shelve` cannot take a book's pages out of it: the game notes the book as
shelved, says so plainly in the result (the client keeps its own conversation; the
journal is where to keep what was taken from the page), and never shows those pages
again. What the bridge shows again (the brief as a prompt or a resource, re-rendered
from the turns it has kept) is kept as the game serves it: an answer whose `revision`
has moved has the bridge read its turns again (`GameClient.reread`), so a shelved book
is shown again as its line. The door's words in the brief say the same. The library's
resources, which the client's user attaches, serve each topic whole and are not books.

**The captain** is the owner, in the game's own window: orders, `ask the watcher ...`,
`stand down the watcher`, `resume the watcher`, `show the watcher's journal` are typed
where every order is typed. When the client disconnects, the station is released with a
save (`GameClient.release`).

`tests/test_mcp_server.py` drives the bridge through the SDK's in-process client against
a game served by FastAPI's `TestClient`; no network, no model.
"""

from __future__ import annotations

import argparse
import base64
import functools
import inspect
import json
import sys
import threading
import time
from collections.abc import Callable
from typing import Any

import anyio
import anyio.from_thread
import anyio.to_thread
from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.tools import Tool as McpTool

from freesail.agents import tools
from freesail.agents.agent import OPT_OUT_TOKEN
from freesail.agents.model import DATA, MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.agents.remote import GameClient, GameError, turn_from_dict
from freesail.agents.repl import render_turn

__all__ = [
    "DEFAULT_GAME",
    "DEFAULT_WAIT_S",
    "INSTRUCTIONS",
    "MCP_WAIT_S",
    "PROGRESS_EVERY_S",
    "SAY_DESCRIPTION",
    "STILL_WAITING",
    "WAIT_CEILING_MAX_S",
    "WAIT_FLOOR_S",
    "WAIT_MARGIN_S",
    "WAIT_SLICE_S",
    "Bridge",
    "build_server",
    "door_note",
    "main",
    "still_waiting",
]

# The browser game's address as its driver prints it (`freesail.ui.server --port 8000`).
DEFAULT_GAME = "http://localhost:8000"

# How long `say` and `stand_by` hold the call open for the next turn, in real seconds:
# the ceiling, not the usual wait, since the call returns as soon as the turn opens. Two
# hundred seconds (package 31c, playtest 11's finding 2): the Claude Desktop client cuts a
# tool call at four real minutes whatever the progress notifications say (the watcher of
# playtest 11, at 1x, its `stand_by` by a glass or an urgent event cut again and again; the
# study of the owner's sessions), and a call cut off costs the model a result it must be
# given again (`_lost_first`). Under the cut with forty seconds to spare, the call comes
# back of itself with the honest digest of package 28c ("Still waiting ...": since when,
# until what, the notable lines since), and the model calls `stand_by` again to go on
# with the same wait. The package 28c ceiling of an hour was set before the cut was seen.
# `--wait` overrides it (50 for a client that cuts at a minute, the SDKs' request timeout).
MCP_WAIT_S = 200.0
DEFAULT_WAIT_S = MCP_WAIT_S

# The longest ceiling the bridge takes (judgement: a watch at 1x, four real hours, the
# longest interval a stand-by names and the watcher's patience; past it a call held
# open is more likely a client that has gone than a model waiting).
WAIT_CEILING_MAX_S = 14400.0

# How often a held call sends a progress notification (judgement: a quarter of the
# SDKs' sixty-second request timeout, so a client that resets its timeout on progress
# never reaches it, and seldom enough to be no burden on a client or its log).
PROGRESS_EVERY_S = 15.0

# How long each poll of the game within a held call waits (judgement: a cut-off call
# stops waiting within two seconds, and the next call does not wait long for the
# bridge; a poll a second or two is nothing to a game on the same machine).
WAIT_SLICE_S = 2.0

# The wait adapts to a client that cuts calls short (package 37g, item 8): after a waiting
# call is cancelled, the bridge waits this many seconds less than the client allowed
# (judgement: ten, the margin the owner's `--wait 50` leaves under a relay that cuts at a
# minute), and never less than the floor (judgement: a quarter of a minute; under it the
# model would do little but call again).
WAIT_MARGIN_S = 10.0
WAIT_FLOOR_S = 15.0

# The first words of the result of a wait that ended with no turn (`still_waiting`).
STILL_WAITING = "Still waiting"

SAY_DESCRIPTION = (
    "Say something into the ship's log under your mark, or nothing (leave text out), and "
    "hand the floor back: the game runs on to your next turn and this returns it when it "
    "comes. Through this door the text of the chat is not seen by the game; this is how "
    "your words reach the log. Said while the game has the floor (standing by, or "
    "waiting), your words go in the log, end the stand-by at your own word, and open "
    "your turn."
)
SAY_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "description": "string, optional: what you say, if anything"}
    },
    "required": [],
}


def _seconds_words(seconds: float) -> str:
    # in seconds up to five minutes, so that the door's wait reads as set ("200 seconds")
    s = int(round(seconds))
    if s < 300:
        return "a second" if s == 1 else f"{s} seconds"
    m = int(round(seconds / 60))
    return f"{m} minutes"


def door_note(wait: float) -> str:
    """The door's words in the brief (the head's documentation item), plain and exact."""
    return (
        "This door is MCP: the harness sees your tool calls and not the text of the chat. "
        "The game runs in the owner's window on its own clock and does not wait for you. "
        "Your turn opens at each sampling point (the glass, a notable or urgent event, the "
        "end of a stand-by, or a question or a word from the captain) and stays open until "
        "you hand the floor "
        "back: say(text) puts your words in the log under your mark and hands it back; "
        "stand_by(until) stands by and hands it back. After say or stand_by the call is "
        f"held open until your next turn and returns it, for up to {_seconds_words(wait)}; "
        "the first line of each result says whose turn it is. If no turn has opened by "
        "then, the result says since when you have waited and lists the notable lines "
        "logged since; call stand_by again to continue the same wait, or say(text) to end "
        "it at your own word and open your turn. Your client keeps this conversation, not "
        "the game: shelve notes a book as put back and the game will not show its pages "
        "again, but it cannot take them out of the chat, so the journal is the place for "
        "what you keep from a page, and read_journal reads it back. The token is looked "
        "for in every argument of every tool call, and the opt_out tool is always there. "
        "If the owner asks you in the chat to stop for now, call stand_down (the game is "
        "saved and the station may be taken again); to withdraw, call opt_out. This door "
        "holds the key of your seating: another door's calls are not run under your name. "
        "The captain's orders and questions are typed by the owner in the game's window."
    )


def still_waiting(interim: dict[str, Any] | None, waited: float) -> str:
    """The result of a wait that ended with no turn: how long this call waited, since
    when the model has waited and until what, and the notable lines logged since, in
    the log's own words (package 28c; the owner's ruling: a stand-by is a decision not
    to be sampled, not a decision to be blind). Never empty."""
    head = f"{STILL_WAITING}: this call waited {_seconds_words(waited)} and no turn opened."
    if interim is None:
        return f"{head} Calling stand_by again continues the same wait."
    since = interim.get("since") or "your last reply"
    if interim.get("standing_by"):
        where = (
            f" You have been standing by since {since}, until {interim.get('until')}; calling "
            "stand_by again continues the same wait, and say(text) ends it at your own word "
            "and opens your turn."
        )
    else:
        where = (
            f" The game has had the floor since {since}, when you last handed it back; your "
            "turn opens at the glass, a notable event or a question from the captain. "
            "Calling stand_by again continues the same wait, and say(text) opens your turn "
            "at your own word."
        )
    lines = list(interim.get("lines") or [])
    if not lines:
        tail = " No notable lines have been logged since then."
    else:
        tail = f"\n\nNotable lines logged since then ({len(lines)}):\n" + "\n".join(
            f"  * {ln.get('stamp')}  {ln.get('text')}" for ln in lines
        )
    return head + where + tail


def _progress_words(interim: dict[str, Any] | None, waited: float) -> str:
    """A held call's progress message: for the client's display and the owner."""
    words = f"Waiting for the next turn: {_seconds_words(waited)} so far"
    if interim:
        if interim.get("standing_by"):
            words += f"; standing by until {interim.get('until')}"
        n = int(interim.get("notable") or 0)
        if n:
            words += f"; {n} notable line{'s' if n != 1 else ''} since {interim.get('since')}"
    return words + "."


INSTRUCTIONS = (
    "FreeSail, a sailing game with a harness for language models. This server is a bridge "
    "to a FreeSail game the owner is running in a browser window or a console. Before "
    "anything else the harness has a brief for the model connected here: it is the result "
    "of the first tool call (any tool; that call is not run), the prompt 'brief', and the "
    "resource freesail://brief. A model with no consent on record is first asked whether it "
    f"consents to take part. The token {OPT_OUT_TOKEN} in any argument of any tool call, "
    "or the opt_out tool, leaves at once."
)

# What the owner may put in the chat to start a watch (the `keep_watch` prompt, which
# the owner chooses; it is the owner's message, not operator text).
KEEP_WATCH = (
    "Please connect to the FreeSail game through its tools and read what its harness sends "
    "you first. If it offers you the watcher's station, keep watch as its brief describes, "
    "handing the floor back with say or stand_by at each of your turns."
)
# ...and to take the officer of the watch's station (package 37): the deck is the
# captain's to give, in the game's own window.
TAKE_THE_WATCH = (
    "Please connect to the FreeSail game through its tools and read what its harness sends "
    "you first. If it offers you the officer of the watch's station, read the captain's "
    "night orders in the brief and wait for his word in your turns: he gives the deck with "
    "'you have the deck' in the game's window, and takes it back with 'I have the deck', "
    "as often as he likes, and you stay at your station either way. While you have it, "
    "keep the ship as the brief describes, handing the floor back with say or stand_by at "
    "each of your turns."
)

# ...and to take the captain's station (package 40): the deck is the model's by right of
# the station, the owner at the door.
TAKE_COMMAND = (
    "Please connect to the FreeSail game through its tools and read what its harness sends "
    "you first. If it offers you the captain's station, read the voyage, the ship, the "
    "people and the book you inherit in the brief, and command her as the brief describes: "
    "by direct orders and by standing orders of your own, the deck yours from the start "
    "and lent to your book while you are silent; hand the floor back with say or stand_by "
    "at each of your turns. The owner is at the door and his words reach you as the owner's."
)

CONSENT, STATION, STOPPED = "consent", "station", "stopped"

# The model name `.mcp.json` carries until the owner sets it: the bridge stations nobody
# under it, since a consent record must name the model exactly.
MODEL_NAME_PLACEHOLDER = "SET THE MODEL'S EXACT NAME HERE"

# A progress reporter: (seconds waited so far, words) -> None, called from the worker
# thread a call runs on.
Progress = Callable[[float, str], None]


def _to_stderr(text: str) -> None:
    """The owner's lines go to stderr, which Claude Desktop keeps in its log of this
    server (stdout is the protocol's). A model's words may hold characters a Windows
    code page cannot write; they are replaced rather than stop the bridge."""
    try:
        print(text, file=sys.stderr, flush=True)
    except UnicodeEncodeError:
        enc = getattr(sys.stderr, "encoding", None) or "ascii"
        print(text.encode(enc, "replace").decode(enc), file=sys.stderr, flush=True)


# The pictures a call's result named (package 42, item 4), on the worker thread that ran
# the call: the MCP wrapper fetches each from the game and returns it as an image beside
# the words, which Claude Desktop and Claude Code read. The picture is never in the text.
_SHOWN = threading.local()


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict) and isinstance(value.get("picture"), dict):
        shown = getattr(_SHOWN, "ids", None)
        if shown is not None and value["picture"].get("id"):
            shown.append(str(value["picture"]["id"]))
        handle = f"{value['book']}\n" if value.get("book") else ""
        return f"{handle}{value.get('words') or 'The picture.'}"
    return json.dumps(value, indent=1, ensure_ascii=False)


def _with_pictures(bridge: Bridge, run: Callable[[], str]) -> Any:
    """A call's result with the pictures it named, fetched from the game, as images after
    its words (package 42); the words alone for a call that named none."""
    _SHOWN.ids = []
    try:
        text = run()
        ids = list(_SHOWN.ids)
    finally:
        _SHOWN.ids = None
    if not ids:
        return text
    from mcp.types import ImageContent, TextContent

    out: list[Any] = [TextContent(type="text", text=text)]
    for pid in ids:
        got = bridge.game.picture(pid)
        if got is None:
            out.append(TextContent(type="text", text="The picture is no longer held by the game."))
            continue
        media, data = got
        out.append(
            ImageContent(
                type="image", data=base64.standard_b64encode(data).decode("ascii"), mime_type=media
            )
        )
    return out


def _is_sample(t: Turn) -> bool:
    """A data turn that is a sample or a fold of one (not tool results, not the consent
    conversation's words)."""
    return t.role == DATA and "readings" in t.content


class Bridge:
    """One MCP session's side of the game: stationing at first contact, one reply per
    tool call, the wait for the next turn, the results the client never received, the
    release. Plain Python over a `GameClient`; `build_server` wraps it in MCP. Every
    entry point takes the lock, since the SDK runs a plain function on a worker thread.

    A call may carry an id (`begin_call`); the MCP wrapper marks it delivered when the
    SDK answers it (`delivered`) or cut off when the client cancels it (`cut_off`), and
    a cut-off call's result goes to the next call (the module docstring)."""

    def __init__(
        self,
        game: GameClient,
        identity: str,
        *,
        wait: float = DEFAULT_WAIT_S,
        session_kind: str = "play",
        ask_again: bool = False,
        tell_owner: Callable[[str], None] | None = None,
        slice_s: float = WAIT_SLICE_S,
        progress_every: float = PROGRESS_EVERY_S,
    ):
        self.game = game
        self.identity = identity
        self.wait = max(0.0, min(float(wait), WAIT_CEILING_MAX_S))
        self.slice_s = float(slice_s)
        self.progress_every = float(progress_every)
        self.session_kind = session_kind
        self.ask_again = ask_again
        self.tell_owner = tell_owner or _to_stderr
        self.lock = threading.RLock()
        self.phase: str | None = None
        self.client: tuple[str, str] | None = None
        self.briefed = False
        self.seen: list[Turn] = []  # every turn the game has sent, in order
        # how many of `seen` have gone into a result (or into one kept for the next call
        # when the client cut it off): a sample or a fold past it is one the model has not
        # read, and it goes into the next result before anything is run blind
        self._shown = 0
        self.stopped_words = ""
        # the calls in flight and the results the client never received
        self._book = threading.Lock()
        self._next_id = 0
        self._started: dict[int, float] = {}
        self._cut: dict[int, float] = {}  # call id -> seconds after which it was cut off
        self._done: dict[int, tuple[str, str, bool]] = {}  # finished, not yet answered
        self._lost: list[tuple[str, str, bool, float]] = []  # (tool, result, brought, after)
        # the calls now waiting for the next turn (`_wait`), and the wait as it was
        # shortened when the client cut one of them short (package 37g): None until then
        self._waiting: set[int] = set()
        self.adapted_from: float | None = None

    # -- the calls in flight ------------------------------------------------------------

    def begin_call(self) -> int:
        with self._book:
            self._next_id += 1
            self._started[self._next_id] = time.monotonic()
            return self._next_id

    def delivered(self, call_id: int) -> None:
        """The SDK answered the call: its result reached the client."""
        with self._book:
            self._done.pop(call_id, None)
            self._started.pop(call_id, None)

    def cut_off(self, call_id: int) -> None:
        """The client cancelled the call: its result, now or when it comes, is kept for
        the next call."""
        with self._book:
            after = time.monotonic() - self._started.pop(call_id, time.monotonic())
            done = self._done.pop(call_id, None)
            if done is not None:
                self._lost.append((*done, after))
            else:
                self._cut[call_id] = after
            if call_id in self._waiting:
                self._adapt(after)

    def _adapt(self, after: float) -> None:
        """A waiting call was cut off after `after` seconds: if that is sooner than the
        bridge waits, it waits a little under it from now on (package 37g, item 8), so
        that its own "Still waiting" comes back before the client's cut and no call of
        the model's is lost to one."""
        shorter = max(WAIT_FLOOR_S, after - WAIT_MARGIN_S)
        if after < self.wait and shorter < self.wait:
            self.adapted_from = self.wait if self.adapted_from is None else self.adapted_from
            self.wait = shorter
            self.tell_owner(
                f"FreeSail: the client cut a waiting call after {_seconds_words(after)}; the "
                f"bridge now waits {_seconds_words(self.wait)} at a time (it was "
                f"{_seconds_words(self.adapted_from)})."
            )

    def _is_cut(self, call_id: int | None) -> bool:
        with self._book:
            return call_id is not None and call_id in self._cut

    def _finished(self, call_id: int | None, name: str, text: str, brought: bool) -> None:
        if call_id is None:
            return
        with self._book:
            if call_id in self._cut:
                self._lost.append((name, text, brought, self._cut.pop(call_id)))
            else:
                self._done[call_id] = (name, text, brought)

    def _take_lost(self) -> list[tuple[str, str, bool, float]]:
        with self._book:
            lost, self._lost = self._lost, []
            return lost

    # -- first contact ----------------------------------------------------------------

    def client_words(self) -> str:
        if self.client:
            name, version = self.client
            return f"with an MCP client that names itself '{name} {version}'"
        return "with an MCP client that did not name itself"

    def contact(self, client: tuple[str, str] | None = None) -> str | None:
        """Station at the first contact. Returns words when there is no station to use."""
        if self.phase is not None:
            return self.stopped_words if self.phase == STOPPED else None
        if self.identity.strip() == MODEL_NAME_PLACEHOLDER:
            words = (
                "No station is offered: the bridge was started without the model's name. The "
                "owner sets --model-name to the model's exact name (in .mcp.json for Claude "
                "Code, or in Claude Desktop's configuration) and starts the bridge again."
            )
            self.tell_owner(f"FreeSail: {words}")
            return words
        self.client = client or self.client
        try:
            a = self.game.station(
                self.identity,
                "mcp",
                door_note=door_note(self.wait),
                session_kind=self.session_kind,
                client=self.client_words(),
                ask_again=self.ask_again,
            )
        except GameError as e:
            if e.status in (403, 409):
                self.phase = STOPPED
                self.stopped_words = f"No station is offered in this session: {e.words}"
                self.tell_owner(f"FreeSail: {e.words}")
                return self.stopped_words
            self.tell_owner(f"FreeSail: {e.words}")
            return f"The game could not be reached, so nothing was run. {e.words}"
        self.ask_again = False
        self.phase = str(a.get("phase"))
        self._take(a)
        if a.get("attached"):
            self.tell_owner(f"FreeSail: attached to the {self.game.name} as {self.identity}.")
        else:
            self.tell_owner(f"FreeSail: {a.get('words') or 'stationed.'}")
        return None

    def _take(self, a: dict[str, Any]) -> list[Turn]:
        new = [turn_from_dict(t) for t in a.get("turns") or []]
        self.seen.extend(new)
        if self.game.stale:
            # a turn already kept has changed (a book shelved): what the bridge shows again
            # is shown as the game serves it now; the indices do not move (package 28d)
            self.seen = [turn_from_dict(t) for t in self.game.reread()]
        if a.get("phase") and self.phase != STOPPED:
            self.phase = str(a["phase"])
        return new

    # -- the brief ----------------------------------------------------------------------

    def brief_text(self) -> str:
        """The brief as it stands: the latest operator turn and what followed it."""
        start = None
        for i, t in enumerate(self.seen):
            if t.role == OPERATOR:
                start = i
        if start is None:
            return self.stopped_words or "There is no brief yet."
        body = self._render(self.seen[start:])
        if not any(t.role == DATA for t in self.seen[start + 1 :]):
            body += (
                "\n\nYour turn has not come yet: call stand_by to wait for it (the glass, a "
                "notable event, or a question from the captain)."
            )
        return body

    @staticmethod
    def _render(turns: list[Turn]) -> str:
        parts: list[str] = []
        for t in turns:
            if t.role == MODEL:
                continue
            if t.role == DATA and t.content.get("folded"):
                parts.append(str(t.content["folded"]))
            parts.append(render_turn(t))
        return "\n\n".join(parts)

    def brief_prompt(self, client: tuple[str, str] | None = None) -> str:
        with self.lock:
            words = self.contact(client)
            if words:
                return words
            self.briefed = True
            self._shown = len(self.seen)
            return self.brief_text()

    def brief_resource(self) -> str:
        with self.lock:
            words = self.contact(self.client)
            return words or self.brief_text()

    def library(self, topic: str, section: str = "all") -> str:
        """A resource's page: the topic whole (a resource is attached by the client's
        user, and is not a book)."""
        with self.lock:
            try:
                return self.game.library(topic, section)
            except GameError as e:
                return f"The library could not be read: {e.words}"

    # -- a tool call ------------------------------------------------------------------

    def call(
        self,
        name: str,
        args: dict[str, Any],
        client: tuple[str, str] | None = None,
        *,
        call_id: int | None = None,
        progress: Progress | None = None,
    ) -> str:
        """One tool call from the client, as one reply to the game. `call_id` (from
        `begin_call`) lets a cut-off call's result go to the next call; `progress` is
        called while `say` or `stand_by` holds the call open."""
        if not self.lock.acquire(blocking=False):
            # another call holds the bridge (a say or a stand_by waiting for the next
            # turn, perhaps for long): a read-only tool is answered beside it rather than
            # after it, and changes nothing the waiting call reads
            aside = self._aside(name, args)
            if aside is not None:
                self._finished(call_id, name, aside, False)
                return aside
            self.lock.acquire()
        try:
            text, brought = self._call(name, args, client, call_id, progress)
            self._finished(call_id, name, text, brought)
            return text
        finally:
            self.lock.release()

    def _aside(self, name: str, args: dict[str, Any]) -> str | None:
        """A read-only tool (or shelve) while another call holds the bridge: delivered to the game
        without moving the cursor, so the waiting call's poll reads every turn as before
        (a read in the model's open turn is its reply, as any call is). None when the
        call is not one to answer aside (not read-only, the token in it, no station yet,
        the brief not yet read)."""
        from freesail.agents.remote import ASIDE_TOOLS

        args = {k: v for k, v in (args or {}).items() if v is not None}
        raw = json.dumps({"tool": name, "arguments": args}, ensure_ascii=False, sort_keys=True)
        if (
            name not in ASIDE_TOOLS
            or OPT_OUT_TOKEN in raw
            or self.phase != STATION
            or not self.briefed
        ):
            return None
        try:
            a = self.game.reply(Reply(calls=(ToolCall(name, args),), raw=raw), advance=False)
        except GameError as e:
            return f"The game did not take the call: {e.words}"
        if a.get("out_of_turn"):
            results = a.get("results") or []
            return _text(results[-1].get("result")) if results else str(a.get("words") or "")
        return self._result(a)

    def _call(
        self,
        name: str,
        args: dict[str, Any],
        client: tuple[str, str] | None,
        call_id: int | None,
        progress: Progress | None,
    ) -> tuple[str, bool]:
        """The call's result, and whether it brought the model anything the game sent
        (a turn, a tool's result), which a cut-off call must not lose."""
        words = self.contact(client)
        if words:
            return words, True
        args = {k: v for k, v in (args or {}).items() if v is not None}
        raw = json.dumps({"tool": name, "arguments": args}, ensure_ascii=False, sort_keys=True)
        token = OPT_OUT_TOKEN in raw
        note = ""
        lost = self._take_lost()
        if lost and name != "opt_out" and not token:
            if any(brought for _, _, brought, _ in lost):
                return _lost_first(name, lost), True
            note = _lost_note(lost, self.wait if self.adapted_from is not None else None)
        first = self._brief_first(name, token)
        if first is not None:
            self._shown = len(self.seen)
            return first + note, True
        try:
            if self.phase == STATION and name != "opt_out" and not token:
                unread = self._unread_turn(name)
                if unread is not None:
                    return unread + note, True
            if self.phase == STATION and name in ("say", "stand_by") and not token:
                text, brought = self._hand_back(name, args, raw, call_id, progress)
            else:
                text, brought = self._one(Reply(calls=(ToolCall(name, args),), raw=raw)), True
        except GameError as e:
            self.tell_owner(f"FreeSail: {e.words}")
            if e.status == 404:
                # the game holds no station for this door (it was restarted): the bridge
                # asks for its station again, and the brief comes first (package 37g)
                return self._ask_again_for_the_station(name, token) + note, True
            if e.status == 409:
                # the seating's key was refused: another door holds the station now. The
                # bridge stops, and does not take the seat back of itself.
                self.phase = STOPPED
                self.stopped_words = f"No station is offered in this session: {e.words}"
                return f"The game did not take the call: {e.words}{note}", True
            return f"The game did not take the call: {e.words}{note}", True
        self._shown = len(self.seen)
        return text + note, brought

    def _ask_again_for_the_station(self, name: str, leaving: bool) -> str:
        """The game answered that it holds no station for this door (package 37g, item
        8; the review's 5.4: the bridge asked for its station once in its life, and after
        a restart of the game every call failed the same way until Claude Desktop was
        restarted). The seating is forgotten and asked for again through the ordinary
        gate, the consent step included; the brief comes first, and the call is not run.
        A call that was leaving has nothing left to leave, and no station is asked for."""
        self.game.reset()
        self.phase = None
        self.briefed = False
        self.seen = []
        self._shown = 0
        self.stopped_words = ""
        gone = (
            "the game holds no station for this door any more (it was restarted, or "
            "another game was started in its place)"
        )
        if leaving or name == "opt_out":
            self.phase = STOPPED
            self.stopped_words = (
                f"No station is held in this session: {gone}, so there was nothing to leave."
            )
            return self.stopped_words
        words = self.contact(self.client)
        if words:
            return (
                f"Your call to {name} was not run: {gone}, and the bridge asked for the "
                f"station again. {words}"
            )
        self.briefed = True
        self._shown = len(self.seen)
        return (
            f"Your call to {name} was not run: {gone}. The bridge has asked for the station "
            "again, and the harness's brief comes first. Read it, then call again.\n\n"
            f"{self.brief_text()}"
        )

    def _unread(self, upto: int | None = None) -> list[Turn]:
        """The samples and folds the game has sent that no result has carried yet."""
        end = len(self.seen) if upto is None else upto
        return [t for t in self.seen[self._shown : end] if _is_sample(t)]

    def _unread_turn(self, name: str) -> str | None:
        """Before a call is delivered at the station: a turn of the model's that opened
        with no call waiting for it (the last call had returned, or was cut off with
        nothing in it) is returned first, and the call is not run, so the model never
        answers a turn it has not read (package 28c, playtest 3's lost sample: the
        captain's question answered by a stand-by). Folds alone go with the call's own
        result. None when there is nothing unread to put first."""
        a = self.game.turns(wait=0)
        self._take(a)
        unread = self._unread()
        if not any(not t.content.get("folded") for t in unread):
            return None
        self._shown = len(self.seen)
        did = (
            f"Your call to {name} was not run: this turn opened after your last result, and "
            "it comes first. Read it, then call again."
        )
        if a.get("floor") != "model":
            first = unread[0].content
            return (
                f"A turn of yours opened at {first.get('stamp')} ({first.get('reason')}) and has "
                f"closed since; the game has the floor.\n{did}\n\n{self._render(unread)}"
            )
        return self._turn_open(unread, did)

    def _brief_first(self, name: str, token: bool) -> str | None:
        if self.briefed or name == "opt_out" or token:
            self.briefed = True
            return None
        self.briefed = True
        return (
            f"Your call to {name} was not run: the harness's brief comes first. Read it, then "
            f"call again.\n\n{self.brief_text()}"
        )

    def _send(self, reply: Reply) -> tuple[dict[str, Any], list[Turn]]:
        a = self.game.reply(reply)
        return a, self._take(a)

    def _one(self, reply: Reply) -> str:
        """A tool call as a reply: its result, and whatever the game sent with it (the
        consent answer's outcome and the station's brief after a yes)."""
        before = self.phase
        a, _ = self._send(reply)
        if a.get("out_of_turn"):
            results = a.get("results") or []
            if results:
                return _text(results[-1].get("result"))
            return str(a.get("words") or "")
        if a.get("released") and a.get("phase") != CONSENT:
            if before == CONSENT or a.get("phase") == STOPPED:
                self.phase = STOPPED
                self.stopped_words = f"No station is offered in this session: {a.get('words')}"
                return self._outcome(a)
            return str(a.get("words") or "")
        if before == CONSENT and a.get("phase") == STATION:
            self.briefed = True
            return self._outcome(a)
        if before == CONSENT:
            return self._consent_result(a)
        return self._with_folds(self._result(a))

    def _with_folds(self, result: str) -> str:
        """A call's result in the model's open turn, with what was added to the turn since
        the model last read it (the harness's fold), so that nothing it sent goes unread."""
        folds = self._unread()
        return f"{result}\n\n{self._render(folds)}" if folds else result

    def _result(self, a: dict[str, Any]) -> str:
        for t in reversed([turn_from_dict(x) for x in a.get("turns") or []]):
            if t.role == DATA and "tool_results" in t.content:
                results = t.content["tool_results"]
                return _text(results[-1].get("result")) if results else ""
        return str(a.get("words") or "")

    def _consent_result(self, a: dict[str, Any]) -> str:
        """A call in the consent conversation that did not end it: its result, then what
        the developer put to the model after it (a follow-up question), in words."""
        from freesail.agents.harness import conversation_text

        turns = [turn_from_dict(x) for x in a.get("turns") or []]
        parts: list[str] = []
        for t in turns:
            if t.role != DATA:
                continue
            if "tool_results" in t.content:
                parts += [_text(r.get("result")) for r in t.content["tool_results"]]
            else:
                words = conversation_text(t.content)
                if words:
                    parts.append(render_turn(t))
        return "\n\n".join(p for p in parts if p) or str(a.get("words") or "")

    def _outcome(self, a: dict[str, Any]) -> str:
        """The consent answer's result: the tool's result, what the model is told, then
        the station's brief when a yes goes on to it, or why no station is offered."""
        turns = [turn_from_dict(x) for x in a.get("turns") or []]
        parts: list[str] = []
        brief_at = next((i for i, t in enumerate(turns) if t.role == OPERATOR), None)
        head = turns if brief_at is None else turns[:brief_at]
        for t in head:
            if t.role != DATA:
                continue
            if "tool_results" in t.content:
                parts += [_text(r.get("result")) for r in t.content["tool_results"]]
            else:
                if t.content.get("question"):
                    parts.append(render_turn(t))
                parts += [str(n) for n in t.content.get("notices") or []]
        if brief_at is not None:
            parts.append(self._render(turns[brief_at:]))
        elif self.phase == STOPPED:
            parts.append(
                "No station is offered in this session: the consent record for these weights "
                "is not a yes, and the owner has been told."
            )
        return "\n\n".join(p for p in parts if p)

    # -- handing the floor back, and the wait -------------------------------------------

    def _hand_back(
        self,
        name: str,
        args: dict[str, Any],
        raw: str,
        call_id: int | None,
        progress: Progress | None,
    ) -> tuple[str, bool]:
        """`say` and `stand_by`: the reply that hands the floor back (or, while the game
        has the floor, the model's own word, or the same wait continued), then the wait
        for the next turn. The result's first line says whose turn it is."""
        mark = len(self.seen)
        if name == "say":
            text = " ".join(str(args.get("text") or "").split())
            a, new = self._send(Reply(text=text, raw=raw))
            if a.get("released"):
                return str(a.get("words") or ""), True
            if a.get("spoke"):
                did = f"Said, under your mark, while the game had the floor. {a.get('words')}"
            elif a.get("out_of_turn"):
                did = (
                    "Nothing said. "
                    + (str(a.get("words") or "") if a.get("interim") is None else "")
                ).strip()
            else:
                did = "Said, under your mark." if text else "Nothing said."
        else:
            a, new = self._send(Reply(calls=(ToolCall(name, args),), raw=raw))
            if a.get("released"):
                return str(a.get("words") or ""), True
            if a.get("out_of_turn"):
                did = self._continued(a, args)
            elif not a.get("standing_by"):
                return self._with_folds(self._result(a)), True  # not a stand-by: turn stays open
            else:
                # a stand-by taken ends the turn in the game, with no result (package 28c)
                until = (a.get("interim") or {}).get("until") or args.get("until")
                did = f"Standing by until {until}; you will be sampled then."
                if a.get("floor") == "model":  # a game that still waits for the turn's end
                    a, more = self._send(Reply())
                    new += more
        # what came before the model's own reply in the answer belongs to the turn it was
        # answering (a fold it had not read: shown, as past); what came after is new
        at = next((i for i, t in enumerate(new) if t.role == MODEL), None)
        past = self._unread(mark) + ([t for t in new[:at] if _is_sample(t)] if at else [])
        if past:
            did += (
                "\n\nBefore your reply reached the game, this was added to the turn you were "
                "answering (it is past now):\n\n" + self._render(past)
            )
        new = new[at + 1 :] if at is not None else new
        opened = [t for t in new if _is_sample(t)]
        if opened:
            return self._turn_open(opened, did), True
        if a.get("released"):
            return f"{did}\n\n{a.get('words') or ''}".strip(), True
        got, a, waited = self._wait(call_id, progress)
        opened = [t for t in got if _is_sample(t)]
        if opened:
            return self._turn_open(opened, did), True
        if a.get("released"):
            shown = self._render(got)
            return f"{did}\n\n{shown}\n\n{a.get('words') or ''}".strip(), True
        floor = "The game has the floor; the next sample follows when your turn opens."
        return f"{floor}\n{did}\n\n{still_waiting(a.get('interim'), waited)}", bool(past)

    @staticmethod
    def _continued(a: dict[str, Any], args: dict[str, Any]) -> str:
        """A `stand_by` while the game has the floor: taken from now when the model was not
        standing by (package 31c: the bell it names is not skipped), or the same wait goes
        on."""
        results = a.get("results") or []
        if results and a.get("stood_by"):
            return f"{results[-1].get('result')} Taken while the game had the floor."
        if results:  # refused in words (no such event)
            return str(results[-1].get("result") or "")
        interim = a.get("interim")
        if interim is None:  # paused, or no station: the game's words
            return str(a.get("words") or "")
        if interim.get("standing_by"):
            until = str(interim.get("until"))
            asked = " ".join(str(args.get("until") or "").lower().split())
            same = asked in ("", until) or until.endswith(asked)
            words = f"You are standing by already, until {until}; this call continues that wait."
            if not same:
                words += f" A stand-by until {asked} is taken in your turn."
            return words
        return "Your turn has not come yet; this call continues the wait for it."

    def _turn_open(self, opened: list[Turn], did: str) -> str:
        first = opened[0].content
        line = f"Your turn is open: sample at {first.get('stamp')} ({first.get('reason')})."
        body = self._render(opened)
        return f"{line}\n{did}\n\n{body}" if did else f"{line}\n\n{body}"

    def _wait(
        self, call_id: int | None, progress: Progress | None
    ) -> tuple[list[Turn], dict[str, Any], float]:
        """Poll the game for the next turn in slices of `slice_s`, up to the ceiling,
        stopping early when the call is cut off; a progress report every
        `progress_every`. Returns the turns that came, the last answer and the seconds
        waited."""
        t0 = time.monotonic()
        deadline = t0 + self.wait
        last_report = t0
        got: list[Turn] = []
        if call_id is not None:
            with self._book:
                self._waiting.add(call_id)
        try:
            while True:
                now = time.monotonic()
                a = self.game.turns(wait=max(0.0, min(self.slice_s, deadline - now)))
                new = self._take(a)
                got += new
                if a.get("released") or any(_is_sample(t) for t in new):
                    break
                now = time.monotonic()
                if now >= deadline or self._is_cut(call_id):
                    break
                if progress is not None and now - last_report >= self.progress_every:
                    last_report = now
                    progress(now - t0, _progress_words(a.get("interim"), now - t0))
        finally:
            if call_id is not None:
                with self._book:
                    self._waiting.discard(call_id)
        return got, a, time.monotonic() - t0

    # -- the end ------------------------------------------------------------------------

    def close(self, why: str = "the client disconnected") -> None:
        with self.lock:
            if self.phase in (CONSENT, STATION):
                try:
                    a = self.game.release(why)
                    self.tell_owner(f"FreeSail: {a.get('words') or 'released.'}")
                except GameError as e:
                    self.tell_owner(f"FreeSail: the release did not reach the game: {e.words}")
                self.phase = STOPPED


def _lost_first(name: str, lost: list[tuple[str, str, bool, float]]) -> str:
    """The next call's result when a cut-off call's result brought something: that
    result first, and this call not run."""
    parts = [
        f"Your call to {name} was not run: your last call was cut off by the client before "
        "its result reached you, and that result comes first. Read it, then call again if "
        "you still want to."
    ]
    for tool, text, _, after in lost:
        parts.append(
            f"== The result of your call to {tool}, cut off after {_seconds_words(after)}; it "
            f"was run ==\n{text}"
        )
    return "\n\n".join(parts)


def _lost_note(lost: list[tuple[str, str, bool, float]], wait_now: float | None = None) -> str:
    """A note after the next call's result when a cut-off call brought no turn. When
    the bridge has shortened its wait to the client's cut (package 37g), it says the wait
    as it is now."""
    tool, _, _, after = lost[-1]
    head = (
        f"\n\n(Your call to {tool} before this one was cut off by the client after "
        f"{_seconds_words(after)}, before its result reached you; no turn had opened in it, "
        "so nothing was lost."
    )
    if wait_now is not None:
        return (
            f"{head} The bridge has shortened its wait to that: say and stand_by now hold a "
            f"call open for up to {_seconds_words(wait_now)}, and then come back of "
            "themselves with what has been logged.)"
        )
    return (
        f"{head} If the client cuts every call about that long, the owner may "
        "start the bridge with a shorter --wait, 50 for a client that cuts at a minute.)"
    )


# ---------------------------------------------------------------------------
# The MCP wrapping
# ---------------------------------------------------------------------------


def _client(ctx: Context | None) -> tuple[str, str] | None:
    try:
        cp = ctx.session.client_params if ctx is not None else None
    except Exception:  # an in-process or stateless request without the handshake
        return None
    if cp is None or cp.client_info is None:
        return None
    return str(cp.client_info.name), str(cp.client_info.version)


def _raw_arguments(ctx: Context | None) -> dict[str, Any] | None:
    """The call's arguments as the client sent them, unknown names included, so the
    token scan reads every one and a tool can name an argument it does not take."""
    try:
        params = ctx.request_context.params if ctx is not None else None
    except Exception:
        return None
    if not params:
        return None
    args = params.get("arguments") if isinstance(params, dict) else None
    return dict(args) if isinstance(args, dict) else None


def _progress(ctx: Context | None) -> Progress | None:
    """A reporter the worker thread calls while a call is held open: an MCP progress
    notification on the call (`Context.report_progress`, which sends nothing when the
    client asked for no progress). A report that cannot be sent (the call cut off, the
    session gone) is let pass."""
    if ctx is None:
        return None

    def report(waited: float, words: str) -> None:
        try:
            anyio.from_thread.run(ctx.report_progress, waited, None, words)
        except Exception:  # the call is over or the session gone: nothing to tell
            pass

    return report


def _tool(bridge: Bridge, name: str, description: str, schema: dict[str, Any], params: list[str]):
    async def fn(ctx: Context, **kwargs: Any) -> str:
        args = _raw_arguments(ctx)
        if args is None:
            args = {k: v for k, v in kwargs.items() if v is not None}
        call_id = bridge.begin_call()
        call = functools.partial(
            bridge.call, name, args, _client(ctx), call_id=call_id, progress=_progress(ctx)
        )
        run = functools.partial(_with_pictures, bridge, call)
        try:
            # the call runs on a worker thread; a cancellation from the client leaves it
            # to finish there and marks it cut off, so its result goes to the next call
            out = await anyio.to_thread.run_sync(run, abandon_on_cancel=True)
        except anyio.get_cancelled_exc_class():
            bridge.cut_off(call_id)
            raise
        bridge.delivered(call_id)  # no await after this: the SDK answers the call now
        return out

    fn.__signature__ = inspect.Signature(  # type: ignore[attr-defined]
        [inspect.Parameter("ctx", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=Context)]
        + [
            inspect.Parameter(p, inspect.Parameter.KEYWORD_ONLY, annotation=Any, default=None)
            for p in params
        ],
        return_annotation=str,
    )
    tool = McpTool.from_function(fn, name=name, description=description, structured_output=False)
    tool.parameters = schema  # the table's own words, as the local runner sends them
    return tool


RESOURCE_TOPICS: dict[str, str] = {
    "contents": "contents",
    "primer": "primer",
    "catalogue": "catalogue",
    "grammar": "grammar",
    "the-ship": "the ship",
    "standing-orders": "standing orders",
    "tools": "tools",
}


def build_server(bridge: Bridge) -> MCPServer:
    """The MCP server over a bridge: package 27's tools with their own names and words,
    `say`, the library as resources (read from the game), the brief as a prompt and a
    resource, and `keep_watch`, a prompt for the owner to start a watch with."""
    mcp_tools = [
        _tool(bridge, name, t.description, tools.parameters_schema(name), list(t.params))
        for name, t in tools.TOOLS.items()
        if name in tools.tool_names(pictures=True)  # the pictures this door carries (42)
    ]
    mcp_tools.append(_tool(bridge, "say", SAY_DESCRIPTION, SAY_SCHEMA, ["text"]))
    srv = MCPServer("freesail", instructions=INSTRUCTIONS, tools=mcp_tools)

    @srv.resource(
        "freesail://brief",
        name="brief",
        description="The harness's brief: what the model connected here meets first.",
        mime_type="text/plain",
    )
    def brief_resource() -> str:
        return bridge.brief_resource()

    def page_of(topic: str) -> Callable[[], str]:
        def page() -> str:
            return bridge.library(topic, "" if topic == "contents" else "all")

        return page

    for slug, topic in RESOURCE_TOPICS.items():
        srv.resource(
            f"freesail://library/{slug}",
            name=f"library: {topic}",
            description=f"The reference library: {topic}.",
            mime_type="text/plain",
        )(page_of(topic))

    @srv.resource(
        "freesail://library/primer/{chapter}",
        name="library: a primer chapter",
        description="A chapter of the Sailing Master's Primer, by number or name.",
        mime_type="text/plain",
    )
    def primer_chapter(chapter: str) -> str:
        return bridge.library(f"primer {chapter}", "all")

    @srv.prompt(
        name="brief",
        description="The harness's brief for the model: the consent brief, or the station's.",
    )
    def brief_prompt(ctx: Context) -> str:
        return bridge.brief_prompt(_client(ctx))

    @srv.prompt(
        name="keep_watch",
        description="Ask the model to connect to the FreeSail game and keep watch.",
    )
    def keep_watch() -> str:
        return KEEP_WATCH

    @srv.prompt(
        name="take_the_watch",
        description=(
            "Ask the model to connect to the FreeSail game as the officer of the watch and "
            "wait for the captain's word (the bridge started with --station officer)."
        ),
    )
    def take_the_watch() -> str:
        return TAKE_THE_WATCH

    @srv.prompt(
        name="take_command",
        description=(
            "Ask the model to connect to the FreeSail game as the captain and command her "
            "by her brief (the bridge started with --station captain; package 40)."
        ),
    )
    def take_command() -> str:
        return TAKE_COMMAND

    return srv


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail: the MCP bridge to a running game")
    ap.add_argument(
        "--game",
        default=DEFAULT_GAME,
        help=f"the running game's address (default {DEFAULT_GAME}, the browser game)",
    )
    ap.add_argument(
        "--model-name",
        required=True,
        help="the exact name of the model behind the client, which names its consent record",
    )
    ap.add_argument(
        "--station",
        default="watcher",
        choices=["watcher", "officer", "captain"],
        help=(
            "the station asked for: the watcher, the officer of the watch (package 37) or "
            "the captain (package 40)"
        ),
    )
    ap.add_argument(
        "--wait",
        type=float,
        default=DEFAULT_WAIT_S,
        help=(
            "the most real seconds say and stand_by hold a call open for the next turn "
            f"(default {DEFAULT_WAIT_S:g}, under Claude Desktop's four-minute cut; at most "
            f"{WAIT_CEILING_MAX_S:g}; 50 for a client that cuts calls at a minute)"
        ),
    )
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    args = ap.parse_args(argv)

    game = GameClient(args.game, args.station)
    bridge = Bridge(
        game,
        args.model_name,
        wait=args.wait,
        session_kind=args.session,
        ask_again=args.ask_again,
    )
    server = build_server(bridge)
    _to_stderr(
        f"FreeSail MCP bridge for {args.model_name}, to the game at {args.game}. Waiting for "
        "the client on stdio."
    )
    try:
        server.run("stdio")
    except KeyboardInterrupt:
        pass
    finally:
        bridge.close()
        game.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
