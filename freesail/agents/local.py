"""The local runner (spec M4 §13 as revised; package 28b): a door for a model served on
this machine through an OpenAI-compatible chat-completions endpoint with tool calling,
which is what llama.cpp's `llama-server` serves (and Ollama, on its own port). It is a
client of the running game and of the endpoint, and builds no World.

    python -m freesail.agents.local --game http://localhost:8000 --endpoint http://localhost:8080
        [--model NAME] [--seed N] [--temperature T] [--ctx N] [--station watcher]
        [--session play|test] [--ask-again]

It reads the served model's identity (`LocalModel.identity`), stations it through the
game's agent API with that identity (`remote.GameClient`; the game runs the consent gate:
the consent conversation for weights with no record, the station brief after a yes,
refused in words otherwise), then loops: poll the game for turns, send the endpoint the
conversation when the floor is the model's, deliver its reply to the game, until the
station is released or Ctrl-C, which releases it. What the model writes without
answering in the consent conversation is shown at this terminal and the owner's reply
typed here goes back to it (`owner>`), as with package 28's runner. The owner plays the
game in its own window meanwhile; the watcher's lines are in its log.

**The wire.** `LocalModel.reply(turns)` translates package 27's turns into the messages
array: the latest operator turn (the brief) is the `system` message; a data turn that
is a sample is a `user` message carrying its JSON; a data turn of tool results is one
`tool` message per call, answering the assistant message's `tool_calls` by id (the ids
are made here, by position, since the harness's calls carry none); a plain
conversation's turn (the consent step's) is a `user` message in words; a model turn is
an `assistant` message with its text and its calls. `tools.TOOLS` (or the harness's
allow-list, `offered_tools`) becomes the `tools` array with `tools.parameters_schema`.
The response's content and tool calls come back as a `Reply` whose `raw` is the content
and the tool calls serialised, so the token scan reads everything the model *said*. A
thinking model's reasoning, where the server returns it apart (`reasoning_content`), is
not in `raw`: thinking about the token does not use it, writing it does (the consent
brief says so). The response messages are kept whole in `exchanges`, reasoning and all.

**The budget.** The conversation grows a sample at a time. When the context size is
known (`--ctx-size`, else the server's `n_ctx` from `/props`), the oldest turns are left
out of the request, whole exchanges at a time, so that the system message and the latest
turns fit with `REPLY_RESERVE_TOKENS` to spare; a brief that alone does not fit stops the
run with the numbers. Tokens are estimated at `CHARS_PER_TOKEN` characters each.

**Nothing real passes through.** The request carries the brief, the samples and the tool
results, the model's own earlier replies, the sampling settings and nothing else: no
credential, no header of the owner's, no telemetry. The identity is the served file's
*name*, never its path, so the owner's folders (a Windows path holds the user's name) do
not reach a consent record.

Tested against `httpx.MockTransport` only (`tests/test_local_runner.py`), never a server.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from typing import Any

import httpx

from freesail.agents import consent
from freesail.agents.harness import conversation_text
from freesail.agents.model import DATA, MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.agents.remote import GameClient, GameError, turn_from_dict
from freesail.agents.tools import TOOLS, parameters_schema, tool_names

__all__ = [
    "CHARS_PER_TOKEN",
    "DEFAULT_ENDPOINT",
    "IDENTITY_HASH_KEYS",
    "REPLY_RESERVE_TOKENS",
    "DoorError",
    "LocalModel",
    "main",
]

# llama-server's default address (its --host 127.0.0.1 and --port 8080, per its README).
DEFAULT_ENDPOINT = "http://127.0.0.1:8080"

# About four characters of English to a token (judgement: the usual rule of thumb for
# BPE vocabularies; the budget errs early rather than late by keeping a reserve).
CHARS_PER_TOKEN = 4

# Tokens kept free for the reply (judgement: a watcher's turn is a line or two and a few
# tool calls, a few hundred tokens; a thinking model's reasoning takes more).
REPLY_RESERVE_TOKENS = 2048

# How long one request may take (judgement: a large model on a 4090 reading a long brief
# for the first time can take a minute or more; ten minutes is the unattended bound).
REQUEST_TIMEOUT_S = 600.0

# Keys a server might give the loaded file's hash under. llama-server's /props gives the
# path and not a hash, as far as its README says; these are read if a server gives one.
IDENTITY_HASH_KEYS: tuple[str, ...] = ("model_sha256", "model_hash")


class DoorError(Exception):
    """The endpoint could not be used; the message says why, in words for the owner."""


def _basename(path: str) -> str:
    return str(path).replace("\\", "/").rstrip("/").rsplit("/", 1)[-1]


class LocalModel:
    """A `Model` for an OpenAI-compatible chat-completions endpoint."""

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        *,
        model: str = "",
        seed: int | None = None,
        temperature: float | None = None,
        ctx_size: int | None = None,
        transport: httpx.BaseTransport | None = None,
        timeout: float = REQUEST_TIMEOUT_S,
        on_reply: Callable[[Reply], None] | None = None,
    ):
        base = endpoint.strip().rstrip("/")
        base = base.removesuffix("/v1")
        self.base = base
        self.model = model
        self.seed = seed
        self.temperature = temperature
        self.ctx_size = ctx_size
        self.on_reply = on_reply
        self.client = httpx.Client(base_url=base, transport=transport, timeout=timeout)
        self.offered_tools: tuple[str, ...] | None = None  # set by the harness
        self.failed: str | None = None  # words for the owner once the endpoint fails
        self.exchanges: list[dict[str, Any]] = []  # each response message as served
        self.dropped_turns = 0  # turns left out of the last request for the budget
        self._props: dict[str, Any] | None = None
        self._props_read = False

    # -- the server ------------------------------------------------------------------

    def _get(self, path: str) -> httpx.Response:
        try:
            return self.client.get(path)
        except httpx.ConnectError as e:
            raise DoorError(self._refused(e)) from None
        except httpx.HTTPError as e:
            raise DoorError(
                f"The model server at {self.base} did not answer {path}: {e}."
            ) from None

    def _refused(self, e: Exception) -> str:
        return (
            f"Could not reach the model server at {self.base}: the connection was refused "
            f"({e}). Is llama-server (or Ollama) running on that address? The command to "
            "start it is in docs/agents/Harness.md."
        )

    def props(self) -> dict[str, Any] | None:
        """llama-server's `/props`, or None where the server has none (Ollama)."""
        if not self._props_read:
            self._props_read = True
            r = self._get("/props")
            if r.status_code == 200:
                try:
                    body = r.json()
                except ValueError:
                    body = None
                self._props = body if isinstance(body, dict) else None
        return self._props

    def server_words(self) -> str:
        """What is serving, for the consent record's runtime."""
        p = self.props()
        if p is not None:
            build = p.get("build_info")
            return f"llama-server{f' ({build})' if build else ''} at {self.base}"
        return f"an OpenAI-compatible server at {self.base}"

    def identity(self) -> str:
        """The served weights' identity, exact, which names the consent record: the
        file's name from llama-server's `/props` (`model_path`, or the older
        `default_generation_settings.model`) with its hash where the server gives one;
        else the models list (`/v1/models`): the `--model` name if the server lists it,
        or the one model it lists, with Ollama's digest for it where `/api/tags` gives
        one. Refuses in words when it cannot say which weights answer."""
        p = self.props()
        if p is not None:
            path = p.get("model_path") or (p.get("default_generation_settings") or {}).get("model")
            if path:
                name = _basename(str(path))
                digest = next((str(p[k]) for k in IDENTITY_HASH_KEYS if p.get(k)), "")
                return f"{name} (sha256 {digest})" if digest else name
        r = self._get("/v1/models")
        if r.status_code != 200:
            raise DoorError(
                f"The model server at {self.base} gave no /props and its models list "
                f"answered {r.status_code}; the harness cannot say which weights it serves."
            )
        try:
            ids = [str(m.get("id", "")) for m in r.json().get("data") or []]
        except (ValueError, AttributeError):
            ids = []
        ids = [i for i in ids if i]
        if self.model and self.model in ids:
            name = self.model
        elif self.model and not ids:
            raise DoorError(f"The model server at {self.base} lists no models.")
        elif self.model:
            raise DoorError(
                f"The model server at {self.base} does not list '{self.model}'; it lists "
                f"{', '.join(ids)}."
            )
        elif len(ids) == 1:
            name = ids[0]
        else:
            raise DoorError(
                f"The model server at {self.base} lists {len(ids)} models "
                f"({', '.join(ids) or 'none'}) and says none is loaded; name one with --model."
            )
        name = _basename(name) if ("/" in name or "\\" in name) else name
        digest = self._ollama_digest(name)
        return f"{name} (digest {digest})" if digest else name

    def _ollama_digest(self, name: str) -> str:
        try:
            r = self.client.get("/api/tags")
        except httpx.HTTPError:
            return ""
        if r.status_code != 200:
            return ""
        try:
            models = r.json().get("models") or []
        except (ValueError, AttributeError):
            return ""
        for m in models:
            if name in (m.get("name"), m.get("model")) and m.get("digest"):
                return str(m["digest"]).removeprefix("sha256:")
        return ""

    def context_size(self) -> int | None:
        if self.ctx_size:
            return self.ctx_size
        try:
            p = self.props()
        except DoorError:
            return None
        n = ((p or {}).get("default_generation_settings") or {}).get("n_ctx")
        return int(n) if n else None

    # -- the request -----------------------------------------------------------------

    def tools_schema(self) -> list[dict[str, Any]]:
        names = self.offered_tools if self.offered_tools is not None else tool_names()
        return [
            {
                "type": "function",
                "function": {
                    "name": n,
                    "description": TOOLS[n].description,
                    "parameters": parameters_schema(n),
                },
            }
            for n in names
        ]

    def messages(self, turns: Sequence[Turn]) -> list[dict[str, Any]]:
        """The turns as chat messages, from the latest operator turn on (a door taking
        over a restored station sends the brief again, `Harness.take_over`)."""
        start = 0
        for i, t in enumerate(turns):
            if t.role == OPERATOR:
                start = i
        out: list[dict[str, Any]] = []
        last_ids: list[str] = []
        for i, t in enumerate(turns[start:], start):
            if t.role == OPERATOR:
                out.append({"role": "system", "content": str(t.content)})
            elif t.role == MODEL:
                r: Reply = t.content
                last_ids = [f"call_{i}_{k}" for k in range(len(r.calls))]
                msg: dict[str, Any] = {"role": "assistant", "content": r.text or ""}
                if r.calls:
                    msg["tool_calls"] = [
                        {
                            "id": cid,
                            "type": "function",
                            "function": {
                                "name": c.name,
                                "arguments": json.dumps(c.args, ensure_ascii=False),
                            },
                        }
                        for cid, c in zip(last_ids, r.calls, strict=True)
                    ]
                out.append(msg)
            elif t.role == DATA:
                d = t.content
                if "tool_results" in d:
                    results = list(d["tool_results"])
                    for k, cid in enumerate(last_ids):
                        res = results[k] if k < len(results) else None
                        if res is None:
                            content = "Not run: this sample's tool-call budget was spent."
                        else:
                            value = res.get("result")
                            content = (
                                value
                                if isinstance(value, str)
                                else json.dumps(value, ensure_ascii=False)
                            )
                        out.append({"role": "tool", "tool_call_id": cid, "content": content})
                    last_ids = []
                    continue
                words = conversation_text(d)
                if words is not None:
                    out.append({"role": "user", "content": words})
                else:
                    out.append({"role": "user", "content": json.dumps(d, ensure_ascii=False)})
        return self._budget(out)

    def _budget(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self.dropped_turns = 0
        ctx = self.context_size()
        if not ctx or not messages:
            return messages
        cost = [len(json.dumps(m, ensure_ascii=False)) // CHARS_PER_TOKEN + 1 for m in messages]
        tools_cost = len(json.dumps(self.tools_schema())) // CHARS_PER_TOKEN
        room = ctx - REPLY_RESERVE_TOKENS - tools_cost
        head = messages[0] if messages[0]["role"] == "system" else None
        head_cost = cost[0] if head is not None else 0
        if head_cost > room:
            raise DoorError(
                f"The brief is about {head_cost} tokens and the context is {ctx} tokens, of "
                f"which {REPLY_RESERVE_TOKENS} are kept for the reply and {tools_cost} for the "
                "tool definitions; start the server with a larger --ctx-size "
                "(docs/agents/Harness.md)."
            )
        body = messages[1:] if head is not None else messages
        body_cost = cost[1:] if head is not None else cost
        total = head_cost + sum(body_cost)
        first = 0
        while total > room and first < len(body):
            # leave out the oldest whole exchange: up to the next user message
            total -= body_cost[first]
            first += 1
            while first < len(body) and body[first]["role"] != "user":
                total -= body_cost[first]
                first += 1
        if first >= len(body):
            raise DoorError(
                f"The brief and the latest sample do not fit a context of {ctx} tokens with "
                f"{REPLY_RESERVE_TOKENS} kept for the reply; start the server with a larger "
                "--ctx-size (docs/agents/Harness.md)."
            )
        self.dropped_turns = first
        return ([head] if head is not None else []) + body[first:]

    def request_body(self, turns: Sequence[Turn]) -> dict[str, Any]:
        body: dict[str, Any] = {"messages": self.messages(turns), "stream": False}
        if self.model:
            body["model"] = self.model
        tools = self.tools_schema()
        if tools:
            body["tools"] = tools
        if self.seed is not None:
            body["seed"] = int(self.seed)
        if self.temperature is not None:
            body["temperature"] = float(self.temperature)
        return body

    # -- the reply -------------------------------------------------------------------

    @staticmethod
    def parse(message: dict[str, Any]) -> Reply:
        """A response message as a `Reply`: the content as text; each tool call with its
        arguments (a JSON string, or an object where a server sends one; an argument
        string that is not JSON gives no arguments, and the tool says what it needs);
        `raw` the content and then the calls as served, so the scan sees every word."""
        content = message.get("content") or ""
        if isinstance(content, list):  # content parts
            content = "".join(str(p.get("text", "")) for p in content if isinstance(p, dict))
        content = str(content)
        calls: list[ToolCall] = []
        served: list[dict[str, Any]] = []
        for tc in message.get("tool_calls") or []:
            fn = tc.get("function") or {}
            name = str(fn.get("name", ""))
            raw_args = fn.get("arguments")
            if isinstance(raw_args, dict):
                args = raw_args
            else:
                try:
                    args = json.loads(raw_args) if raw_args else {}
                except (TypeError, ValueError):
                    args = {}
                if not isinstance(args, dict):
                    args = {}
            calls.append(ToolCall(name, dict(args)))
            served.append({"name": name, "arguments": raw_args})
        raw = content
        if served:
            raw += ("\n" if raw else "") + json.dumps(served, ensure_ascii=False)
        return Reply(text=content.strip(), calls=tuple(calls), raw=raw)

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        """One request, one reply. A failure sets `failed` with the words and returns
        None (the sample stays open), and every later call returns None at once, so the
        World never waits on a dead server; the drivers stand the station down on it."""
        if self.failed is not None:
            return None
        try:
            body = self.request_body(turns)
            r = self.client.post("/v1/chat/completions", json=body)
        except DoorError as e:
            self.failed = str(e)
            return None
        except httpx.ConnectError as e:
            self.failed = self._refused(e)
            return None
        except httpx.HTTPError as e:
            self.failed = f"The model server at {self.base} did not answer: {e}."
            return None
        if r.status_code != 200:
            self.failed = (
                f"The model server at {self.base} answered {r.status_code}: {_error_words(r)}"
            )
            return None
        try:
            message = r.json()["choices"][0]["message"]
        except (ValueError, KeyError, IndexError, TypeError):
            self.failed = f"The model server at {self.base} sent a reply the runner cannot read."
            return None
        self.exchanges.append(message)
        reply = self.parse(message)
        if self.on_reply is not None:
            self.on_reply(reply)
        return reply

    def close(self) -> None:
        self.client.close()


def _error_words(r: httpx.Response) -> str:
    try:
        err = r.json().get("error")
        if isinstance(err, dict):
            return str(err.get("message") or err)
        if err:
            return str(err)
    except (ValueError, AttributeError):
        pass
    return (r.text or "no reason given").strip()[:300]


# ---------------------------------------------------------------------------
# The command: a client of the game and of the endpoint
# ---------------------------------------------------------------------------

# The browser game's address as its driver prints it (`freesail.ui.server --port 8000`).
DEFAULT_GAME = "http://localhost:8000"

# How long one poll of the game waits for the model's next turn, in real seconds
# (judgement: long enough that an idle runner asks the game a few times a minute, short
# enough that Ctrl-C between polls is prompt; the game answers at once when a turn opens).
POLL_WAIT_S = 30.0

# The door's words in the brief (the head's documentation item), plain and exact.
RUNNER_NOTE = (
    "This door is a model server on the owner's machine. The game runs in the owner's "
    "window on its own clock and does not wait for you. Your turn opens at each sampling "
    "point (the glass, a notable event, the end of a stand-by, or a question from the "
    "captain) and ends when you reply without a tool call; what happens while it is open "
    "is added to it, so your next turn carries everything since your last reply. The "
    "captain's orders and questions are typed by the owner in the game's window."
)

# Exit codes: 0 is not used by a run that was stationed (it ends released); 2 the game or
# the model server could not be used; 3 the station was released; 5 no station, because
# consent is not a yes on record (as the REPL and package 28's runner).
EXIT_UNREACHABLE = 2
EXIT_RELEASED = 3
EXIT_NO_CONSENT = 5


def echo_reply(out) -> Callable[[Reply], None]:
    def show(r: Reply) -> None:
        if r.text:
            print(f"  model> {r.text}", file=out, flush=True)
        for c in r.calls:
            args = ", ".join(f"{k}={v!r}" for k, v in c.args.items())
            print(f"  model> ({c.name}: {args})", file=out, flush=True)

    return show


def main(
    argv: list[str] | None = None,
    *,
    inp=None,
    out=None,
    transport=None,
    game_transport=None,
    game_http=None,
    poll_wait: float = POLL_WAIT_S,
) -> int:
    """The runner's command. `transport` is the model server's (tests: a fake
    `llama-server`), `game_transport` or `game_http` the game's (tests: the game's app)."""
    inp = inp or sys.stdin
    out = out or sys.stdout
    ap = argparse.ArgumentParser(description="FreeSail: the local runner, a client of the game")
    ap.add_argument(
        "--game",
        default=DEFAULT_GAME,
        help=f"the running game's address (default {DEFAULT_GAME}, the browser game)",
    )
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="the model server's address")
    ap.add_argument("--model", default="", help="the model's name, where the server serves several")
    ap.add_argument("--seed", type=int, help="the model's sampling seed (default: the server's)")
    ap.add_argument(
        "--temperature", type=float, help="the model's temperature (default: the server's)"
    )
    ap.add_argument(
        "--ctx",
        "--ctx-size",
        dest="ctx",
        type=int,
        help="the context to budget against (default: the server's)",
    )
    ap.add_argument("--station", default="watcher", choices=["watcher"])
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    args = ap.parse_args(argv)

    model = LocalModel(
        args.endpoint,
        model=args.model,
        seed=args.seed,
        temperature=args.temperature,
        ctx_size=args.ctx,
        transport=transport,
        on_reply=echo_reply(out),
    )
    try:
        identity = model.identity()
        server = model.server_words()
    except DoorError as e:
        print(str(e), file=out, flush=True)
        return EXIT_UNREACHABLE
    print(f"The model server serves {identity}.", file=out, flush=True)
    game = GameClient(args.game, args.station, transport=game_transport, http=game_http)
    try:
        first = game.station(
            identity,
            "runner",
            door_note=RUNNER_NOTE,
            session_kind=args.session,
            client=server,
            ask_again=args.ask_again,
        )
    except GameError as e:
        print(e.words, file=out, flush=True)
        return EXIT_NO_CONSENT if e.status == 403 else EXIT_UNREACHABLE
    print(first.get("words") or f"The {args.station} is stationed.", file=out, flush=True)
    return run(game, model, first, inp=inp, out=out, poll_wait=poll_wait)


def run(
    game: GameClient,
    model: LocalModel,
    first: dict[str, Any],
    *,
    inp: Any,
    out: Any,
    poll_wait: float = POLL_WAIT_S,
) -> int:
    """The loop: poll the game for turns, send the endpoint the conversation when the
    floor is the model's, deliver its reply, until the station is released or Ctrl-C
    (which releases it). The owner answers what the model writes in the consent
    conversation at this terminal, as with package 28's runner."""
    owner = consent.terminal_owner(inp, out)
    turns: list[Turn] = []
    a = first

    def took(answer: dict[str, Any]) -> dict[str, Any]:
        new = [turn_from_dict(t) for t in answer.get("turns") or []]
        for t in new:
            if t.role == DATA and "readings" in t.content:
                how = "added to the open turn" if t.content.get("folded") else "a turn"
                print(
                    f"== {t.content.get('stamp')}: {how}, {t.content.get('reason')} ==",
                    file=out,
                    flush=True,
                )
        turns.extend(new)
        return answer

    took(a)
    try:
        while True:
            if a.get("released"):
                print(a.get("words") or "The station is released.", file=out, flush=True)
                return EXIT_NO_CONSENT if a.get("phase") == "stopped" else EXIT_RELEASED
            if a.get("waiting") == "owner":
                words = owner(str(a.get("model_words") or ""))
                if not words or not words.strip():
                    a = game.owner("")
                    continue
                game.owner(words)
                a = took(game.turns(wait=0))
                continue
            if a.get("floor") == "model":
                offered = tuple(a.get("tools") or ())
                model.offered_tools = offered or None
                r = model.reply(turns)
                if r is None:
                    why = model.failed or "the model server gave no reply"
                    print(why, file=out, flush=True)
                    a = game.release(f"the model server could not be used: {why}")
                    print(a.get("words") or "", file=out, flush=True)
                    return EXIT_RELEASED
                a = took(game.reply(r))
                continue
            a = took(game.turns(wait=poll_wait))
    except KeyboardInterrupt:
        print("Stopped at the owner's word (Ctrl-C).", file=out, flush=True)
        try:
            a = game.release("Ctrl-C at the local runner")
            print(a.get("words") or "", file=out, flush=True)
        except GameError as e:
            print(e.words, file=out, flush=True)
        return EXIT_RELEASED
    except GameError as e:
        print(e.words, file=out, flush=True)
        return EXIT_UNREACHABLE


if __name__ == "__main__":
    sys.exit(main())
