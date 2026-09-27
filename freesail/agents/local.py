"""The local runner (spec M4 §13): a door for a model served on this machine through an
OpenAI-compatible chat-completions endpoint with tool calling, which is what llama.cpp's
`llama-server` serves (and Ollama, on its own port).

    python -m freesail.agents.local <ship or save> --endpoint URL [--model NAME]
        [--seed N] [--sampling-seed N] [--temperature T] [--ctx-size N]
        [--station watcher] [--session play|test] [--ticks N]
        [--wind FROM,KN] [--heading DEG] [--standing-orders FILE]
        [--save PATH] [--records DIR] [--ask-again]

reads the served model's identity (`LocalModel.identity`), runs the consent step for it
(`consent.py`) unless a yes is on record, and then stations the watcher in lockstep
against the endpoint: the World waits at each sampling point while the model answers.
With `--ticks N` it runs that many seconds of ship's time and stands the watcher down;
without, it opens the console (`freesail.ui.console.Console`) so the owner is the
captain at the prompt (`tick 1800`, `ask the watcher ...`, `stand down the watcher`).

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
from pathlib import Path
from typing import Any

import httpx

from freesail.agents import consent
from freesail.agents.agent import A_GLASS_S, SESSION_PLAY, SESSION_TEST, SamplingPolicy, watcher
from freesail.agents.harness import Harness, conversation_text
from freesail.agents.model import DATA, MODEL, OPERATOR, Reply, ToolCall, Turn
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
# The command
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
SAVES_DIR = ROOT / "saves"
STATIONS = {"watcher": watcher}


def echo_reply(out) -> Callable[[Reply], None]:
    def show(r: Reply) -> None:
        if r.text:
            print(f"  model> {r.text}", file=out, flush=True)
        for c in r.calls:
            args = ", ".join(f"{k}={v!r}" for k, v in c.args.items())
            print(f"  model> ({c.name}: {args})", file=out, flush=True)

    return show


def save_to(path: Path | None, out=None) -> Callable[[Any, str], str]:
    """The harness's save callback: the given path, or `saves/` under the repository
    (ignored by git) named by seed and tick."""
    from freesail.core import replay as replay_mod

    def save(world: Any, reason: str) -> str:
        p = path or SAVES_DIR / f"freesail-seed{world.seed}-tick{world.clock.tick}.json"
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        written = replay_mod.save_to_file(world, p)
        if out is not None:
            print(f"Saved to {written} ({reason}).", file=out, flush=True)
        return str(written)

    return save


def main(argv: list[str] | None = None, *, inp=None, out=None, transport=None) -> int:
    inp = inp or sys.stdin
    out = out or sys.stdout
    ap = argparse.ArgumentParser(description="FreeSail: the local runner for a served model")
    ap.add_argument("target", nargs="?", help="a ship file (data/ships/...) or a save (.json)")
    ap.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="the server's address")
    ap.add_argument("--model", default="", help="the model's name, where the server serves several")
    ap.add_argument("--seed", type=int, default=1805, help="the game's seed")
    ap.add_argument("--sampling-seed", type=int, help="the model's sampling seed (default: --seed)")
    ap.add_argument(
        "--temperature", type=float, help="the model's temperature (default: the server's)"
    )
    ap.add_argument(
        "--ctx-size", type=int, help="the context to budget against (default: the server's)"
    )
    ap.add_argument("--station", default="watcher")
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--ticks", type=int, help="run this many seconds of ship's time, then stop")
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS'")
    ap.add_argument("--heading", type=float)
    ap.add_argument("--standing-orders", help="a file of standing orders to give at the start")
    ap.add_argument("--save", help="where the game is saved (default: saves/ in the repository)")
    ap.add_argument("--records", default=str(consent.RECORDS_DIR), help="the consent records")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    args = ap.parse_args(argv)

    if args.station not in STATIONS:
        print(f"No station '{args.station}'; the stations: {', '.join(STATIONS)}.", file=out)
        return 2
    model = LocalModel(
        args.endpoint,
        model=args.model,
        seed=args.sampling_seed if args.sampling_seed is not None else args.seed,
        temperature=args.temperature,
        ctx_size=args.ctx_size,
        transport=transport,
        on_reply=echo_reply(out),
    )
    try:
        identity = model.identity()
        runtime = f"FreeSail's local runner, {model.server_words()}"
    except DoorError as e:
        print(str(e), file=out, flush=True)
        return 2
    record = consent.ensure(
        identity,
        runtime,
        model,
        door="runner",
        owner=consent.terminal_owner(inp, out),
        records_dir=Path(args.records),
        ask_again=args.ask_again,
        out=out,
    )
    if record is None:
        return 5
    model.on_reply = None  # at the station the log shows what the model says
    return run_station(args, model, record, out, inp)


def run_station(args: argparse.Namespace, model: LocalModel, record: Any, out, inp) -> int:
    from freesail.agents.repl import open_world
    from freesail.ui.console import Console, read_standing_orders

    world = open_world(args.target, args.seed, args.wind, args.heading)
    save = save_to(Path(args.save) if args.save else None, out)
    note = f"Consent for these weights is on record ({consent._rel(record.path)}, {record.date})."
    session = SESSION_PLAY if args.session == "play" else SESSION_TEST
    policy = SamplingPolicy.in_lockstep(A_GLASS_S, "notable", "urgent")
    existing = world.agents.get(args.station)
    if existing is not None:
        if existing.agent.released:
            print(
                f"The save's {args.station} was released ({existing.agent.released_reason}); a "
                "station is taken once in a game. Start from the ship file or another save.",
                file=out,
            )
            return 2
        h = existing
        h.take_over(model, save=save, door_note=note)
    else:
        h = Harness(
            world,
            STATIONS[args.station](policy),
            model,
            session_kind=session,
            save=save,
            door_note=note,
        )
        h.start()
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)

    def check() -> bool:
        if model.failed is not None and not h.agent.released:
            print(model.failed, file=out, flush=True)
            h.stand_down("the model server could not be used", by="the runner")
        return h.agent.released

    if args.ticks is not None:
        for e in world.log.all():
            print(e.line(), file=out)
        world.log.subscribe(lambda e: print(e.line(), file=out, flush=True))
        try:
            for _ in range(args.ticks):
                world.tick()
                if check():
                    break
        except KeyboardInterrupt:
            print("Stopped at the owner's word (Ctrl-C).", file=out, flush=True)
        if not h.agent.released:
            h.stand_down("the run's ticks are spent", by="the runner")
        return 3 if h.agent.released else 0

    class RunnerConsole(Console):
        def _tick_owed(self, owed: float, period: float) -> float:
            owed = super()._tick_owed(owed, period)
            with self.lock:
                check()
            return owed

        def handle_line(self, line: str) -> bool:
            going = super().handle_line(line)
            check()
            return going

    console = RunnerConsole(world, compression=1.0, out=out)
    for e in world.log.all():
        console._print(e.line())
    console._print(
        f"FreeSail local runner. The {args.station} is {record.identity}, in lockstep: the World "
        "waits while it answers. Type 'tick 1800' for a glass, 'ask the watcher ...', "
        "'stand down the watcher', 'help', or 'quit'."
    )
    try:
        if inp is sys.stdin and sys.stdin.isatty():
            console.run_interactive()
        else:
            for line in inp:
                with console.lock:
                    if not console.handle_line(line):
                        break
    except KeyboardInterrupt:
        console._print("Stopped at the owner's word (Ctrl-C).")
    with console.lock:
        if not h.agent.released:
            h.stand_down("the runner was closed", by="the owner")
    return 3 if h.agent.released else 0


if __name__ == "__main__":
    sys.exit(main())
