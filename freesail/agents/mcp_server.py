"""The MCP bridge (spec M4 §13 as revised; package 28b): the door for Claude Desktop,
Claude Code and any other MCP client, over stdio, on the Python MCP SDK's server class
(`MCPServer`, which is what the SDK called `FastMCP` before its version 2). It is a
client of the running game and owns no World.

    python -m freesail.agents.mcp_server --game http://localhost:8000 --model-name "<identity>"
        [--station watcher] [--wait 50] [--session play|test] [--ask-again]

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
floor back; `stand_by(until)` stands by and hands it back. Both then wait for the
model's next turn (the glass, a notable event, the end of a stand-by, a question from
the captain), up to `--wait` real seconds, and return it; when it has not come, the call
says so ("Still waiting for the next sample; call stand_by again to keep waiting.") so
the client never hangs. The game runs on its own clock meanwhile: what happens while the
model holds the floor is added to its open turn (the harness's fold), and the next call
that reads it gets everything since the model's last reply.

**The token.** The chat's text never reaches the game, so the token counts in every
argument of every tool call, and `opt_out` is always listed. Out of turn too: the game
looks for it in a call that comes when the floor is not the model's.

**The captain** is the owner, in the game's own window: orders, `ask the watcher ...`,
`stand down the watcher`, `resume the watcher`, `show the watcher's journal` are typed
where every order is typed. When the client disconnects, the station is released with a
save (`GameClient.release`).

`tests/test_mcp_server.py` drives the bridge through the SDK's in-process client against
a game served by FastAPI's `TestClient`; no network, no model.
"""

from __future__ import annotations

import argparse
import inspect
import json
import sys
import threading
from collections.abc import Callable
from typing import Any

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
    "SAY_DESCRIPTION",
    "STILL_WAITING",
    "Bridge",
    "build_server",
    "door_note",
    "main",
]

# The browser game's address as its driver prints it (`freesail.ui.server --port 8000`).
DEFAULT_GAME = "http://localhost:8000"

# How long `say` and `stand_by` wait for the next turn, in real seconds (judgement: an
# MCP client gives up on a call it has waited too long for, and the SDKs' default for a
# request is sixty seconds; fifty leaves room. The owner checks Claude Desktop's own
# limit at the gate, and `--wait` changes it).
DEFAULT_WAIT_S = 50.0

STILL_WAITING = "Still waiting for the next sample; call stand_by again to keep waiting."

SAY_DESCRIPTION = (
    "Say something into the ship's log under your mark, or nothing (leave text out), and "
    "hand the floor back: the game runs on to your next turn and this returns it when it "
    "comes. Through this door the text of the chat is not seen by the game; this is how "
    "your words reach the log."
)
SAY_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string", "description": "string, optional: what you say, if anything"}
    },
    "required": [],
}


def door_note(wait: float) -> str:
    """The door's words in the brief (the head's documentation item), plain and exact."""
    return (
        "This door is MCP: the harness sees your tool calls and not the text of the chat. "
        "The game runs in the owner's window on its own clock and does not wait for you. "
        "Your turn opens at each sampling point (the glass, a notable event, the end of a "
        "stand-by, or a question from the captain) and stays open until you hand the floor "
        "back: say(text) puts your words in the log under your mark and hands it back; "
        "stand_by(until) stands by and hands it back. What happens while your turn is open "
        "is added to it, so your next look carries everything since your last reply. After "
        f"say or stand_by the call waits up to {wait:g} seconds for your next turn and "
        "returns it; if it has not come, call stand_by again to keep waiting. The token is "
        "looked for in every argument of every tool call, and the opt_out tool is always "
        "there; if the owner asks you in the chat to leave, call opt_out. The captain's "
        "orders and questions are typed by the owner in the game's window."
    )


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

CONSENT, STATION, STOPPED = "consent", "station", "stopped"

# The model name `.mcp.json` carries until the owner sets it: the bridge stations nobody
# under it, since a consent record must name the model exactly.
MODEL_NAME_PLACEHOLDER = "SET THE MODEL'S EXACT NAME HERE"


def _to_stderr(text: str) -> None:
    """The owner's lines go to stderr, which Claude Desktop keeps in its log of this
    server (stdout is the protocol's). A model's words may hold characters a Windows
    code page cannot write; they are replaced rather than stop the bridge."""
    try:
        print(text, file=sys.stderr, flush=True)
    except UnicodeEncodeError:
        enc = getattr(sys.stderr, "encoding", None) or "ascii"
        print(text.encode(enc, "replace").decode(enc), file=sys.stderr, flush=True)


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, indent=1, ensure_ascii=False)


class Bridge:
    """One MCP session's side of the game: stationing at first contact, one reply per
    tool call, the wait for the next turn, the release. Plain Python over a
    `GameClient`; `build_server` wraps it in MCP. Every entry point takes the lock, since
    the SDK runs a plain function on a worker thread."""

    def __init__(
        self,
        game: GameClient,
        identity: str,
        *,
        wait: float = DEFAULT_WAIT_S,
        session_kind: str = "play",
        ask_again: bool = False,
        tell_owner: Callable[[str], None] | None = None,
    ):
        self.game = game
        self.identity = identity
        self.wait = float(wait)
        self.session_kind = session_kind
        self.ask_again = ask_again
        self.tell_owner = tell_owner or _to_stderr
        self.lock = threading.RLock()
        self.phase: str | None = None
        self.client: tuple[str, str] | None = None
        self.briefed = False
        self.seen: list[Turn] = []  # every turn the game has sent, in order
        self.stopped_words = ""

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
            return self.brief_text()

    def brief_resource(self) -> str:
        with self.lock:
            words = self.contact(self.client)
            return words or self.brief_text()

    def library(self, topic: str) -> str:
        with self.lock:
            try:
                return self.game.library(topic)
            except GameError as e:
                return f"The library could not be read: {e.words}"

    # -- a tool call ------------------------------------------------------------------

    def call(self, name: str, args: dict[str, Any], client: tuple[str, str] | None = None) -> str:
        """One tool call from the client, as one reply to the game."""
        with self.lock:
            words = self.contact(client)
            if words:
                return words
            args = {k: v for k, v in (args or {}).items() if v is not None}
            raw = json.dumps({"tool": name, "arguments": args}, ensure_ascii=False, sort_keys=True)
            token = OPT_OUT_TOKEN in raw
            first = self._brief_first(name, token)
            if first is not None:
                return first
            try:
                if self.phase == STATION and name in ("say", "stand_by") and not token:
                    return self._hand_back(name, args, raw)
                return self._one(Reply(calls=(ToolCall(name, args),), raw=raw))
            except GameError as e:
                self.tell_owner(f"FreeSail: {e.words}")
                return f"The game did not take the call: {e.words}"

    def _brief_first(self, name: str, token: bool) -> str | None:
        if self.briefed or name == "opt_out" or token:
            self.briefed = True
            return None
        self.briefed = True
        return (
            f"Your call to {name} was not run: the harness's brief comes first. Read it, then "
            f"call again.\n\n{self.brief_text()}"
        )

    def _send(self, reply: Reply) -> dict[str, Any]:
        a = self.game.reply(reply)
        self._take(a)
        return a

    def _one(self, reply: Reply) -> str:
        """A tool call as a reply: its result, and whatever the game sent with it (the
        consent answer's outcome and the station's brief after a yes)."""
        before = self.phase
        a = self._send(reply)
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
        return self._result(a)

    def _result(self, a: dict[str, Any]) -> str:
        for t in reversed([turn_from_dict(x) for x in a.get("turns") or []]):
            if t.role == DATA and "tool_results" in t.content:
                results = t.content["tool_results"]
                return _text(results[-1].get("result")) if results else ""
        return str(a.get("words") or "")

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
                parts += [str(n) for n in t.content.get("notices") or []]
        if brief_at is not None:
            parts.append(self._render(turns[brief_at:]))
        elif self.phase == STOPPED:
            parts.append(
                "No station is offered in this session: the consent record for these weights "
                "is not a yes, and the owner has been told."
            )
        return "\n\n".join(p for p in parts if p)

    def _hand_back(self, name: str, args: dict[str, Any], raw: str) -> str:
        """`say` and `stand_by`: the reply that hands the floor back, then the wait."""
        if name == "say":
            text = " ".join(str(args.get("text") or "").split())
            a = self._send(Reply(text=text, raw=raw))
            if a.get("released"):
                return str(a.get("words") or "")
            if a.get("out_of_turn"):
                prefix = str(a.get("words") or "")
            else:
                prefix = "Said, under your mark." if text else "Nothing said."
        else:
            a = self._send(Reply(calls=(ToolCall(name, args),), raw=raw))
            if a.get("released"):
                return str(a.get("words") or "")
            if a.get("out_of_turn"):
                prefix = str(a.get("words") or "")
            else:
                prefix = self._result(a)
                if not a.get("standing_by"):
                    return prefix  # not a stand-by the game knows: the turn stays open
                a = self._send(Reply())  # the turn ends with the decision
        return f"{prefix}\n\n{self._wait()}"

    def _wait(self) -> str:
        a = self.game.turns(wait=self.wait)
        new = self._take(a)
        if a.get("released"):
            shown = self._render(new)
            words = str(a.get("words") or "")
            return f"{shown}\n\n{words}".strip()
        if not any(t.role == DATA for t in new):
            return STILL_WAITING
        return self._render(new)

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


def _tool(bridge: Bridge, name: str, description: str, schema: dict[str, Any], params: list[str]):
    def fn(ctx: Context, **kwargs: Any) -> str:
        args = _raw_arguments(ctx)
        if args is None:
            args = {k: v for k, v in kwargs.items() if v is not None}
        return bridge.call(name, args, _client(ctx))

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
            return bridge.library(topic)

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
        return bridge.library(f"primer {chapter}")

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
    ap.add_argument("--station", default="watcher", choices=["watcher"])
    ap.add_argument(
        "--wait",
        type=float,
        default=DEFAULT_WAIT_S,
        help="real seconds say and stand_by wait for the next turn before returning",
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
