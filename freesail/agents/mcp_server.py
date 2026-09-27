"""The MCP server (spec M4 §13): the door for Claude Desktop, over stdio, on the Python
MCP SDK's server class (`MCPServer`, which is what the SDK called `FastMCP` before its
version 2).

    python -m freesail.agents.mcp_server <ship or save> --model-name <identity>
        [--seed N] [--station watcher] [--standing-orders FILE] [--session play|test]
        [--wind FROM,KN] [--heading DEG] [--save PATH] [--records DIR] [--ask-again]

The World runs inside this process. The client (Claude Desktop) is the model's side: it
lists the tools and calls them; this server never calls it. So the harness's loop is
turned inside out: the model's **turn** is the harness's open sample, and each tool call
the client makes is one reply delivered into it (`Harness.deliver`), with the whole call
as the reply's `raw` so the token scan reads every argument.

**How the World advances.** Never on the clock of the wall. The station is in lockstep
(every glass and on notable and urgent events, the watcher's defaults): the World waits
at each sampling point for the model. The model hands the floor back with `say(text)`,
which puts its words in the log under its mark (the chat's text never reaches the game,
so this door adds this one tool), or with `stand_by(until)`; then the World runs on to
the model's next turn (the next glass, an event, the end of the stand-by, a question) and
the call returns that turn's sample. One call runs at most `ADVANCE_LIMIT_S` of ship's
time, so that a long stand-by returns before a client gives up on the call; calling
`stand_by` again goes on waiting.

**The brief first.** The first contact of a session (any tool call, the `brief` prompt)
settles what the model meets: with no consent on record for the identity the owner names
(`--model-name`; the protocol names the client application, not the weights) the consent
brief, run through `consent.Conversation` with `answer` and `opt_out` as the tools that
run; with a yes on record, the station's brief. The first tool call returns the brief and
is not itself run (`opt_out` and the token excepted). The brief is also the `brief`
prompt and the `freesail://brief` resource. A yes goes on to the station brief in the
answer's result; anything else leaves the server inert, every call answered with why.

**The token over MCP.** The client does not send its free text to the server, so the
scan runs over every argument of every tool call, and `opt_out` is always listed. The
brief says so; `docs/agents/Harness.md` says so to the owner: a token the owner types
into the chat reaches the game only when the model passes it on or calls `opt_out`.

**The captain.** The owner gives the captain's word through the `captain` prompt, which
MCP reserves for the user: an order, `ask the watcher ...`, `stand down the watcher`,
`resume the watcher`, `show the watcher's journal`, `state`, `log`. An order given while
the model has the floor waits until it hands the floor back, and is then given on that
tick before the World runs on, so a replay of the save (the orders journaled, the
model's replies played back at their samples) gives the same log; `stand down` is
carried out at once. When the client disconnects, a manned station is stood down with a
save.

The door (`Door`) is plain Python and holds the World; `build_server` wraps it in MCP.
`tests/test_mcp_server.py` drives it through the SDK's in-process client; no network.
"""

from __future__ import annotations

import argparse
import datetime as dt
import inspect
import json
import sys
import threading
from collections.abc import Callable
from pathlib import Path
from typing import Any

from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.tools import Tool as McpTool

from freesail.agents import consent, tools
from freesail.agents.agent import (
    A_GLASS_S,
    OPT_OUT_TOKEN,
    SESSION_PLAY,
    SESSION_TEST,
    STATIONED,
    SamplingPolicy,
    watcher,
)
from freesail.agents.harness import Harness
from freesail.agents.model import DATA, Reply, ToolCall, Turn
from freesail.agents.repl import open_world, render_turn

__all__ = [
    "ADVANCE_LIMIT_S",
    "INSTRUCTIONS",
    "MCP_CONSENT_TOOLS",
    "MCP_DOOR_NOTE",
    "SAY_DESCRIPTION",
    "Door",
    "build_server",
    "main",
]

ROOT = Path(__file__).resolve().parents[2]
SAVES_DIR = ROOT / "saves"

# The most ship's time one call runs (judgement: two hours is about 16 seconds of the
# frigate at the 457 ticks a second measured at gate 4a, well inside the minute an MCP
# client commonly waits for a call; the watcher is sampled every glass, so only a long
# stand-by reaches it).
ADVANCE_LIMIT_S = 2 * 3600

# The tools that run in the consent conversation over MCP: `answer`, as everywhere, and
# `opt_out`, which this door always lists because the chat's text is not scanned.
MCP_CONSENT_TOOLS: tuple[str, ...] = ("answer", "opt_out")

# Read-only tools, which run whether or not the model has the floor: they change nothing.
READ_ONLY: tuple[str, ...] = ("read_log", "readings", "state", "library")

STATIONS = {"watcher": watcher}

SAY_DESCRIPTION = (
    "Say something into the ship's log under your mark, or nothing (leave text out), and "
    "hand the floor back: the game runs on to your next turn and this returns its sample. "
    "Through this door the text of the chat is not seen by the game; this is how your words "
    "reach the log."
)
SAY_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "description": "string, optional: what you say, if anything"}
    },
    "required": [],
}

MCP_DOOR_NOTE = (
    "This door is MCP (Claude Desktop): the harness sees your tool calls and not the text of "
    "the chat. Your turn is open until you hand the floor back: say(text) puts your words in "
    "the log under your mark and hands it back; stand_by(until) stands by and hands it back. "
    "Then the game runs on to your next turn (the next glass, a notable event, the end of a "
    "stand-by, or a question from the captain) and the call returns that turn's sample; the "
    "game never runs on the clock of the wall. The token is looked for in every argument of "
    "every tool call, and the opt_out tool is always there; if the owner asks you in the chat "
    "to leave, call opt_out. The captain's orders come through the owner's captain prompt "
    "and wait until you hand the floor back."
)

INSTRUCTIONS = (
    "FreeSail, a sailing game with a harness for language models. Before anything else the "
    "harness has a brief for the model connected here: it is the result of the first tool "
    "call (any tool; that call is not run), the prompt 'brief', and the resource "
    "freesail://brief. A model with no consent on record is first asked whether it consents "
    f"to take part. The token {OPT_OUT_TOKEN} in any argument of any tool call, or the "
    "opt_out tool, leaves at once. The owner gives the captain's orders with the prompt "
    "'captain'."
)

CONSENT, STATION, STOPPED = "consent", "station", "stopped"


class Pending:
    """The door's model: a client that speaks only when spoken to never answers the
    harness's call. Its replies arrive by `deliver`, one tool call at a time."""

    def reply(self, turns: Any) -> None:
        return None


class Door:
    """One MCP session's state: the World, the consent conversation or the station, the
    captain's waiting orders. Every entry point takes the lock, since the SDK runs a
    plain function on a worker thread."""

    def __init__(
        self,
        world: Any,
        identity: str,
        *,
        station: str = "watcher",
        records_dir: Path = consent.RECORDS_DIR,
        save_path: Path | None = None,
        saves_dir: Path = SAVES_DIR,
        session_kind: str = SESSION_PLAY,
        ask_again: bool = False,
        today: dt.date | None = None,
        advance_limit: int = ADVANCE_LIMIT_S,
        tell_owner: Callable[[str], None] | None = None,
    ):
        if station not in STATIONS:
            raise ValueError(f"No station '{station}'; the stations: {', '.join(STATIONS)}.")
        self.world = world
        self.identity = identity
        self.station_name = station
        self.records_dir = Path(records_dir)
        self.save_path = Path(save_path) if save_path else None
        self.saves_dir = Path(saves_dir)
        self.session_kind = session_kind
        self.ask_again = ask_again
        self.today = today
        self.advance_limit = advance_limit
        self.tell_owner = tell_owner or _to_stderr
        self.lock = threading.RLock()
        self.phase: str | None = None
        self.client: tuple[str, str] | None = None
        self.conv: consent.Conversation | None = None
        self.harness: Harness | None = None
        self.briefed = False
        self.pending_orders: list[str] = []
        self.stopped_words = ""
        self.saves: list[str] = []

    # -- first contact ----------------------------------------------------------------

    def runtime(self) -> str:
        if self.client:
            name, version = self.client
            who = f"an MCP client that names itself '{name} {version}'"
        else:
            who = "an MCP client that did not name itself"
        return f"FreeSail's MCP server over stdio, with {who} (Claude Desktop is the one expected)"

    def contact(self, client: tuple[str, str] | None = None) -> None:
        """The first contact of the session decides what the model meets."""
        if self.phase is not None:
            return
        self.client = client
        record = None if self.ask_again else consent.check(self.identity, self.records_dir)
        if record is None:
            self.conv = consent.Conversation(
                self.identity,
                self.runtime(),
                Pending(),
                door="mcp",
                records_dir=self.records_dir,
                today=self.today,
                allowed_tools=MCP_CONSENT_TOOLS,
                notes=[
                    "Through MCP the harness sees only tool calls. Anything the model and the "
                    "owner wrote in the chat around this conversation is in Claude Desktop, "
                    "not here; the owner may paste it below this line to keep it."
                ],
                tells=True,
            )
            self.conv.begin()
            self.phase = CONSENT
            self.tell_owner(
                f"FreeSail: no consent is on record for {self.identity}; the consent brief "
                "comes first."
            )
            return
        ok, words = consent.gate(record, self.identity)
        self.tell_owner(f"FreeSail: {words}")
        if ok:
            self._take_station(record)
        else:
            self._stop(words)

    def _stop(self, words: str) -> None:
        self.phase = STOPPED
        self.stopped_words = (
            "No station is offered in this session: the consent record for these weights is "
            "not a yes, and the owner has been told."
        )
        self.tell_owner(f"FreeSail: the run stops. {words}")

    def _take_station(self, record: consent.Record) -> None:
        where = consent._rel(record.path) if record.path else "docs/agents/consent/"
        note = f"{MCP_DOOR_NOTE} Consent for these weights is on record ({where}, {record.date})."
        existing = self.world.agents.get(self.station_name)
        if existing is not None:
            if existing.agent.released:
                self._stop(
                    f"The save's {self.station_name} was released "
                    f"({existing.agent.released_reason}); a station is taken once in a game."
                )
                return
            existing.take_over(Pending(), save=self._save, door_note=note)
            self.harness = existing
        else:
            policy = SamplingPolicy.in_lockstep(A_GLASS_S, "notable", "urgent")
            self.harness = Harness(
                self.world,
                STATIONS[self.station_name](policy),
                Pending(),
                session_kind=self.session_kind,
                save=self._save,
                door_note=note,
            )
            self.harness.start()
        self.phase = STATION
        self.briefed = False

    def _save(self, world: Any, reason: str) -> str:
        path = self.save_path or (
            self.saves_dir / f"freesail-seed{world.seed}-tick{world.clock.tick}.json"
        )
        from freesail.core import replay as replay_mod

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        written = str(replay_mod.save_to_file(world, path))
        self.saves.append(written)
        self.tell_owner(f"FreeSail: saved to {written} ({reason}).")
        return written

    # -- the brief ----------------------------------------------------------------------

    def brief_text(self) -> str:
        """What the model meets first, whatever the phase."""
        if self.phase == CONSENT and self.conv is not None:
            h = self.conv.harness
            return f"{h.brief.text()}\n\n{render_turn(self._last_data(h))}"
        if self.phase == STATION and self.harness is not None:
            return self._station_brief()
        return self.stopped_words

    def _station_brief(self) -> str:
        h = self.harness
        assert h is not None and h.brief is not None
        parts = [h.brief.text()]
        if h.open_sample is not None:
            parts.append(render_turn(self._last_data(h)))
        else:
            parts.append(self._no_floor_words())
        return "\n\n".join(parts)

    def brief_prompt(self, client: tuple[str, str] | None = None) -> str:
        with self.lock:
            self.contact(client)
            self.briefed = True
            return self.brief_text()

    def brief_resource(self) -> str:
        with self.lock:
            self.contact(self.client)
            return self.brief_text()

    # -- a tool call ------------------------------------------------------------------

    def call(
        self,
        name: str,
        args: dict[str, Any],
        client: tuple[str, str] | None = None,
    ) -> str:
        """One tool call from the client, as one reply to the harness."""
        with self.lock:
            self.contact(client)
            args = {k: v for k, v in (args or {}).items() if v is not None}
            raw = json.dumps({"tool": name, "arguments": args}, ensure_ascii=False, sort_keys=True)
            token = OPT_OUT_TOKEN in raw
            if self.phase == STOPPED:
                return self.stopped_words
            if self.phase == CONSENT:
                return self._consent_call(name, args, raw, token)
            return self._station_call(name, args, raw, token)

    def _brief_first(self, name: str, token: bool) -> str | None:
        if self.briefed or name == "opt_out" or token:
            self.briefed = True
            return None
        self.briefed = True
        return (
            f"Your call to {name} was not run: the harness's brief comes first. Read it, then "
            f"call again.\n\n{self.brief_text()}"
        )

    def _consent_call(self, name: str, args: dict[str, Any], raw: str, token: bool) -> str:
        first = self._brief_first(name, token)
        if first is not None:
            return first
        conv = self.conv
        assert conv is not None
        h = conv.harness
        conv.deliver(Reply(calls=(ToolCall(name, args),), raw=raw))
        result = self._last_result(h)
        if conv.outcome is None:
            return result
        rec = conv.outcome
        ok, words = consent.gate(rec, self.identity)
        self.tell_owner(f"FreeSail: the consent answer is recorded in {rec.path}. {words}")
        told = conv.told
        if rec.verdict == consent.LEFT:
            result = "You have left the conversation; it is recorded, and no station is offered."
        if ok:
            self._take_station(rec)
            if self.phase != STATION:
                return "\n\n".join(p for p in (result, told, self.stopped_words) if p)
            self.briefed = True
            return "\n\n".join(p for p in (result, told, self._station_brief()) if p)
        self._stop(words)
        return "\n\n".join(p for p in (result, told) if p)

    def _station_call(self, name: str, args: dict[str, Any], raw: str, token: bool) -> str:
        h = self.harness
        assert h is not None
        a = h.agent
        if a.paused:
            h.check_unattended()
        if a.released:
            return self._released_words()
        first = self._brief_first(name, token)
        if first is not None:
            return first
        if h.open_sample is None:
            return self._out_of_turn(name, args, raw, token)
        if name == "say":
            text = " ".join(str(args.get("text") or "").split())
            h.deliver(Reply(text=text, raw=raw))
            if a.released:
                return self._released_words()
            return self._hand_back("Said, under your mark." if text else "Nothing said.")
        if name == "stand_by":
            h.deliver(Reply(calls=(ToolCall(name, args),), raw=raw))
            if a.released:
                return self._released_words()
            result = self._last_result(h)
            if a.standing_by:
                h.deliver(Reply())  # the turn ends with the decision
                return self._hand_back(result)
            return result
        h.deliver(Reply(calls=(ToolCall(name, args),), raw=raw))
        if a.released:
            return self._released_words()
        return self._last_result(h)

    def _out_of_turn(self, name: str, args: dict[str, Any], raw: str, token: bool) -> str:
        """A call when the model does not have the floor (it stands by, it is paused, or a
        call ran out of ship's time before its next turn)."""
        h = self.harness
        assert h is not None
        a = h.agent
        if token:  # the scan the harness makes on a reply, made here on a call out of turn
            piece = next((str(v) for v in args.values() if OPT_OUT_TOKEN in str(v)), "")
            after = piece.split(OPT_OUT_TOKEN, 1)[1] if piece else ""
            h.leave(after.strip(" .:;,-\n"), how="the token")
            return self._released_words()
        if name == "opt_out":
            tools.call(self.world, h.station.name, name, args)
            return self._released_words()
        if name in READ_ONLY:
            return _text(tools.call(self.world, h.station.name, name, args))
        if a.paused:
            return self._no_floor_words()
        if name in ("say", "stand_by"):
            lost = (
                " Your words were not logged, since it was not your turn."
                if (name == "say" and str(args.get("text") or "").strip())
                else ""
            )
            return (
                f"{self._no_floor_words()}{lost} The game runs on to your next turn.\n\n"
                f"{self._advance()}"
            )
        return f"{self._no_floor_words()} {name} was not run."

    def _no_floor_words(self) -> str:
        h = self.harness
        assert h is not None
        a = h.agent
        if a.released:
            return self._released_words()
        if a.paused:
            return (
                f"Your turns are paused: {a.pause_reason}. The captain has been asked whether "
                "to continue; you were not stopped. You may still read, or leave with the token."
            )
        if a.standing_by and a.stand_by is not None:
            return (
                f"You are standing by until {a.stand_by.words}. Call stand_by again to go on "
                "waiting."
            )
        return "It is not your turn. Call stand_by or say to let the game run on to it."

    def _released_words(self) -> str:
        h = self.harness
        reason = h.agent.released_reason if h is not None else ""
        return (
            f"The station is released: {reason}. The game is saved; nothing more is asked of "
            "you here."
        )

    def _hand_back(self, prefix: str) -> str:
        """The model has handed the floor back: the captain's waiting orders are given on
        this tick, then the World runs on to the model's next turn."""
        given = self._give_waiting_orders()
        body = self._advance()
        return "\n\n".join(p for p in (prefix, given, body) if p)

    def _advance(self) -> str:
        h = self.harness
        assert h is not None
        a = h.agent
        world = self.world
        n = 0
        while h.open_sample is None and not a.released and not a.paused and n < self.advance_limit:
            world.tick()
            n += 1
        if a.released:
            return self._released_words()
        if h.open_sample is not None:
            return render_turn(self._last_data(h))
        if a.paused:
            return self._no_floor_words()
        span = f"{n // 60} minutes" if n % 3600 else f"{n // 3600} hours"
        return (
            f"The game ran {span} of ship's time to {world.clock.stamp()} and your turn has not "
            f"come. {self._no_floor_words()}"
        )

    @staticmethod
    def _last_data(h: Harness) -> Turn:
        for t in reversed(h.turns):
            if t.role == DATA and "tool_results" not in t.content:
                return t
        return Turn(DATA, {})

    @staticmethod
    def _last_result(h: Harness) -> str:
        for t in reversed(h.turns):
            if t.role == DATA and "tool_results" in t.content:
                results = t.content["tool_results"]
                return _text(results[-1].get("result")) if results else ""
            if t.role == DATA:
                break
        return ""

    # -- the captain ------------------------------------------------------------------

    def captain(self, order: str, client: tuple[str, str] | None = None) -> str:
        """The owner's word as the captain, through the `captain` prompt."""
        with self.lock:
            self.contact(client)
            order = " ".join(str(order or "").split())
            world = self.world
            if not order:
                return (
                    "Say an order, or 'ask the watcher ...', 'stand down the watcher', 'resume "
                    "the watcher', \"show the watcher's journal\", 'state', 'log 20'."
                )
            low = order.lower()
            if low == "state":
                lines = list(world.summary_lines())
                lines += [
                    f"The {h.station.name}: {h.agent.words()}." for h in world.agents.values()
                ]
                return "\n".join(lines)
            if low == "log" or low.startswith("log "):
                n = int(low.split()[1]) if len(low.split()) > 1 and low.split()[1].isdigit() else 20
                return "\n".join(e.line() for e in world.log.tail(n))
            h = self.harness
            if (
                h is not None
                and h.open_sample is not None
                and not h.agent.released
                and not low.startswith("stand down")
            ):
                self.pending_orders.append(order)
                who = h.station.name
                return (
                    f"The captain's order waits until the {who} hands the floor back, so that a "
                    f"replay gives the same log: {order!r}. ({who.capitalize()}: call say or "
                    "stand_by to hand the floor back; what the order brings comes to you then.)"
                )
            lines = self._give(order)
            if h is not None and h.agent.state == STATIONED and h.open_sample is None:
                lines.append(self._advance())  # resumed: the World runs on to its next turn
            elif h is not None and h.open_sample is not None and not h.agent.released:
                lines.append(render_turn(self._last_data(h)))
            return "\n\n".join(p for p in lines if p)

    def _give(self, order: str) -> list[str]:
        world = self.world
        n = len(world.log)
        world.submit(order, actor="captain")
        return ["\n".join(world.log[i].line() for i in range(n, len(world.log)))]

    def _give_waiting_orders(self) -> str:
        out: list[str] = []
        while self.pending_orders:
            out += self._give(self.pending_orders.pop(0))
        return "\n".join(p for p in out if p)

    # -- the library ------------------------------------------------------------------

    def library(self, topic: str) -> str:
        with self.lock:
            return tools.library(self.world, self.station_name, topic)

    # -- the end ------------------------------------------------------------------------

    def close(self, why: str = "the client disconnected") -> None:
        with self.lock:
            h = self.harness
            if h is not None and h.started and not h.agent.released:
                h.stand_down(why, by="the MCP server")
            elif self.phase == CONSENT and self.conv is not None and self.conv.outcome is None:
                self.tell_owner(
                    "FreeSail: the consent conversation ended before an answer; no record is "
                    "written."
                )


def _to_stderr(text: str) -> None:
    """The owner's lines go to stderr, which Claude Desktop keeps in its log of this
    server (stdout is the protocol's). A model's words may hold characters a Windows
    code page cannot write; they are replaced rather than stop the server."""
    try:
        print(text, file=sys.stderr, flush=True)
    except UnicodeEncodeError:
        enc = getattr(sys.stderr, "encoding", None) or "ascii"
        print(text.encode(enc, "replace").decode(enc), file=sys.stderr, flush=True)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=1, ensure_ascii=False)


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


def _tool(door: Door, name: str, description: str, schema: dict[str, Any], params: list[str]):
    def fn(ctx: Context, **kwargs: Any) -> str:
        args = _raw_arguments(ctx)
        if args is None:
            args = {k: v for k, v in kwargs.items() if v is not None}
        return door.call(name, args, _client(ctx))

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


def build_server(door: Door) -> MCPServer:
    """The MCP server over a door: package 27's tools with their own names and words,
    `say`, the library as resources, the brief as a prompt and a resource, and the
    captain's prompt."""
    mcp_tools = [
        _tool(door, name, t.description, tools.parameters_schema(name), list(t.params))
        for name, t in tools.TOOLS.items()
    ]
    mcp_tools.append(_tool(door, "say", SAY_DESCRIPTION, SAY_SCHEMA, ["text"]))
    srv = MCPServer("freesail", instructions=INSTRUCTIONS, tools=mcp_tools)

    @srv.resource(
        "freesail://brief",
        name="brief",
        description="The harness's brief: what the model connected here meets first.",
        mime_type="text/plain",
    )
    def brief_resource() -> str:
        return door.brief_resource()

    def page_of(topic: str) -> Callable[[], str]:
        def page() -> str:
            return door.library(topic)

        return page

    for slug, topic in RESOURCE_TOPICS.items():
        page = page_of(topic)
        srv.resource(
            f"freesail://library/{slug}",
            name=f"library: {topic}",
            description=f"The reference library: {topic}.",
            mime_type="text/plain",
        )(page)

    @srv.resource(
        "freesail://library/primer/{chapter}",
        name="library: a primer chapter",
        description="A chapter of the Sailing Master's Primer, by number or name.",
        mime_type="text/plain",
    )
    def primer_chapter(chapter: str) -> str:
        return door.library(f"primer {chapter}")

    @srv.prompt(
        name="brief",
        description="The harness's brief for the model: the consent brief, or the station's.",
    )
    def brief_prompt(ctx: Context) -> str:
        return door.brief_prompt(_client(ctx))

    @srv.prompt(
        name="captain",
        description=(
            "The captain's word, from the owner: an order to the ship, 'ask the watcher ...', "
            "'stand down the watcher', 'resume the watcher', \"show the watcher's journal\", "
            "'state' or 'log 20'."
        ),
    )
    def captain_prompt(order: str, ctx: Context) -> str:
        return door.captain(order, _client(ctx))

    return srv


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail: the MCP server for Claude Desktop")
    ap.add_argument("target", nargs="?", help="a ship file (data/ships/...) or a save (.json)")
    ap.add_argument(
        "--model-name",
        required=True,
        help="the exact name of the model behind the client, which names its consent record",
    )
    ap.add_argument("--seed", type=int, default=1805)
    ap.add_argument("--station", default="watcher", choices=sorted(STATIONS))
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--standing-orders", help="a file of standing orders to give at the start")
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS'")
    ap.add_argument("--heading", type=float)
    ap.add_argument("--save", help="where the game is saved (default: saves/ in the repository)")
    ap.add_argument("--records", default=str(consent.RECORDS_DIR), help="the consent records")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    args = ap.parse_args(argv)

    from freesail.ui.console import read_standing_orders

    world = open_world(args.target, args.seed, args.wind, args.heading)
    door = Door(
        world,
        args.model_name,
        station=args.station,
        records_dir=Path(args.records),
        save_path=Path(args.save) if args.save else None,
        session_kind=SESSION_PLAY if args.session == "play" else SESSION_TEST,
        ask_again=args.ask_again,
    )
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)
    server = build_server(door)
    _to_stderr(
        f"FreeSail MCP server: {args.target or 'the point ship'}, seed {args.seed}, for "
        f"{args.model_name}. Waiting for the client on stdio."
    )
    try:
        server.run("stdio")
    except KeyboardInterrupt:
        pass
    finally:
        door.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
