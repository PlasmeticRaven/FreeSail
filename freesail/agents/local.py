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
typed here goes back to it (`owner>`), as with package 28's runner; after the model
answers, the owner has a turn here too before the record closes (package 28c): anything
typed goes to the model, which may reply once, and a blank line closes the record. The
owner plays the game in its own window meanwhile; the watcher's lines are in its log.

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

**The reply budget and the timeout** (package 28c, playtest 4: one request ran away to
76,674 tokens and never returned, and the runner, waiting in it, fetched neither the
captain's question nor the glass). Every request carries `max_tokens` (`--max-reply`,
`REPLY_MAX_TOKENS` by default), so a model that falls into a loop stops within the
budget; every request has `REQUEST_TIMEOUT_S`. A request that fails (a timeout, an
error) leaves the sample open: the runner says so, reads the game's turns again (what
happened meanwhile is folded into the open turn) and asks again; only
`FAILURES_TO_STAND_DOWN` failures in a row stand the station down, with the reason.

**The context guard.** Before stationing, the runner asks the server what context it
gives the model (llama-server's `/props` `n_ctx`; Ollama's `/api/ps` `context_length`
for a loaded model, else the `num_ctx` of `/api/show`), falling back to `--ctx`, and
refuses in words, with what it measured, when that is smaller than the consent brief
(measured as this door sends it; it is the longer of the two briefs: about 6,000
characters against the watcher's 5,200 on the frigate at seed 7, measured for package
28c), the tool definitions (measured), one turn (`TURN_ALLOWANCE_TOKENS`) and the reply
budget; and says so when it cannot learn it.

**The budget.** The conversation grows a sample at a time. When the context size is
known (`--ctx-size`, else the server's `n_ctx` from `/props`), the oldest turns are left
out of the request, whole exchanges at a time, so that the system message and the latest
turns fit with `REPLY_RESERVE_TOKENS` to spare; a brief that alone does not fit stops the
run with the numbers. Tokens are estimated at `CHARS_PER_TOKEN` characters each (the
harness's one rule, `tools.CHARS_PER_TOKEN`, which the library's sizes use too).

**The shelf** (package 28d). The runner keeps the game's turns as the game serves them
and builds each request's messages from them afresh, so a book the model shelved (or
the shelf-life put back) goes out as its line and not its pages from the next request
on: an answer whose `revision` has moved since the runner's copy was read has the
runner read its turns again from where it began (`GameClient.reread`) before it asks
the model; otherwise it reads on from its cursor. The pages are really gone from what
the model is sent.

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
from freesail.agents.agent import TURN_ENDS_WORDS
from freesail.agents.harness import conversation_text
from freesail.agents.model import DATA, MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.agents.remote import GameClient, GameError, turn_from_dict
from freesail.agents.tools import CHARS_PER_TOKEN, TOOLS, parameters_schema, tool_names

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

# `CHARS_PER_TOKEN` (four characters to a token) is the harness's one rule for measuring
# text, named in `tools.py`; the budget errs early rather than late by keeping a reserve.

# The most tokens one reply may run to, sent as `max_tokens` with every request (the
# owner's ruling, 2026-09-28: generous on purpose, so that a long answer, a journal note
# or a thinking model's reasoning is never cut, while a runaway generation is bounded
# within about a minute and a half on a 4090). `--max-reply` changes it.
REPLY_MAX_TOKENS = 4096

# Tokens kept free for the reply in the context budget: the reply budget itself.
REPLY_RESERVE_TOKENS = REPLY_MAX_TOKENS

# How long one request may take, in real seconds. The reply budget, not the clock, is
# what bounds a reply; the timeout is for a server that has hung. Playtest 6 (Qwen3.8
# 27B through Ollama, 2026-09-28) showed 180 s cutting off honest replies: a thinking
# model composing a long note runs to the 4,096-token budget, which a 27B model at four
# bits on a 4090 generates at some twenty to thirty tokens a second, three minutes or
# more, after reading a prompt of some fifteen thousand tokens. Ten minutes leaves room
# for that and still ends a hung server well inside the watcher's patience (a watch of
# ship's time). `--request-timeout` changes it.
REQUEST_TIMEOUT_S = 600.0

# Failures in a row after which the runner stands the station down (judgement: one
# failure is a slow or runaway request, which the budget and the timeout end; three in a
# row, half an hour at most, is a server that cannot serve).
FAILURES_TO_STAND_DOWN = 3

# Tokens allowed for one turn in the context guard (judgement: a glass's turn on the
# frigate at seed 7 measured about 450 tokens, docs/agents/Harness.md §5; a turn that
# grew while the model thought is longer).
TURN_ALLOWANCE_TOKENS = 600

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
        max_reply: int = REPLY_MAX_TOKENS,
    ):
        base = endpoint.strip().rstrip("/")
        base = base.removesuffix("/v1")
        self.base = base
        self.model = model
        self.seed = seed
        self.temperature = temperature
        self.ctx_size = ctx_size
        self.max_reply = int(max_reply)
        self.timeout = float(timeout)
        self.failures = 0  # failed requests in a row
        self.last_error: str | None = None  # the last failure, in words
        self.served_ctx: int | None = None  # the context the server gives, when learned
        self._served_name = ""  # the name the server knows the model by
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
                self._served_name = name
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
        self._served_name = name
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

    def served_context(self) -> tuple[int, str] | None:
        """The context the server gives this model, and where that was read: llama-
        server's `/props` (`n_ctx`), or Ollama's `/api/ps` (`context_length`, for a model
        it has loaded) or `/api/show` (the model's `num_ctx` parameter). None when the
        server does not say (an Ollama model not yet loaded, with no `num_ctx` of its own,
        runs with Ollama's default)."""
        try:
            p = self.props()
        except DoorError:
            p = None
        n = ((p or {}).get("default_generation_settings") or {}).get("n_ctx")
        if n:
            return int(n), "llama-server's /props (n_ctx)"
        name = self._served_name or self.model
        if not name:
            return None
        try:
            r = self.client.get("/api/ps")
            if r.status_code == 200:
                for m in r.json().get("models") or []:
                    if name in (m.get("name"), m.get("model")) and m.get("context_length"):
                        return int(m["context_length"]), "Ollama's /api/ps (context_length)"
            r = self.client.post("/api/show", json={"model": name})
            if r.status_code == 200:
                params = str(r.json().get("parameters") or "")
                for line in params.splitlines():
                    words = line.split()
                    if len(words) == 2 and words[0] == "num_ctx" and words[1].isdigit():
                        return int(words[1]), "Ollama's /api/show (the model's num_ctx)"
        except (httpx.HTTPError, ValueError, AttributeError):
            return None
        return None

    def check_context(self, identity: str, runtime: str) -> str:
        """The context guard, before stationing (package 28c): what the watcher needs,
        measured at `CHARS_PER_TOKEN`: the consent brief as this door sends it (the
        longer of the two briefs; the module docstring), the tool definitions, one turn
        (`TURN_ALLOWANCE_TOKENS`) and the reply budget. Raises `DoorError` in words, with
        the numbers, when the context the server gives (or `--ctx`) is smaller; returns a
        line for the owner otherwise, saying what it measured or that it could not ask."""
        brief = consent.brief_text(identity, runtime, "runner")
        brief_cost = len(json.dumps({"role": "system", "content": brief})) // CHARS_PER_TOKEN + 1
        tools_cost = len(json.dumps(self.tools_schema())) // CHARS_PER_TOKEN
        need = brief_cost + tools_cost + TURN_ALLOWANCE_TOKENS + self.max_reply
        served = self.served_context()
        if served is not None:
            self.served_ctx = served[0]
            got, where = served
        elif self.ctx_size:
            got, where = int(self.ctx_size), "--ctx, as the owner gave it"
        else:
            return (
                f"The model server did not say what context it gives {identity}, and no --ctx "
                f"was given; the watcher needs about {need} tokens (the brief {brief_cost}, "
                f"the tool definitions {tools_cost}, a turn {TURN_ALLOWANCE_TOKENS}, the reply "
                f"budget {self.max_reply}). Ollama's own default is small unless "
                "OLLAMA_CONTEXT_LENGTH or the Modelfile's num_ctx says more: check with "
                "`ollama ps` once the model is loaded, and state it with --ctx."
            )
        words = (
            f"the model server gives {identity} a context of {got} tokens ({where}); the "
            f"watcher needs about {need}: the brief {brief_cost} tokens and the tool "
            f"definitions {tools_cost} (measured, at {CHARS_PER_TOKEN} characters a token), "
            f"a turn {TURN_ALLOWANCE_TOKENS} and the reply budget {self.max_reply}"
        )
        if got < need:
            raise DoorError(
                f"The context is too small: {words}. Raise it: for Ollama, set "
                "OLLAMA_CONTEXT_LENGTH (for example 16384) before `ollama serve`, or a "
                "`PARAMETER num_ctx 16384` line in the model's Modelfile; for llama-server, "
                "--ctx-size 16384; or lower the reply budget with --max-reply "
                "(docs/agents/Harness.md)."
            )
        return f"The context is enough: {words}."

    def context_size(self) -> int | None:
        if self.ctx_size and self.served_ctx:
            return min(int(self.ctx_size), self.served_ctx)
        if self.served_ctx:
            return self.served_ctx
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
        last_calls: tuple[ToolCall, ...] = ()

        def answer_the_ids() -> None:
            # a turn that ended on a stand-by has no results (package 28c); the protocol
            # wants every call answered, so the ids are answered in words
            nonlocal last_ids
            for cid, c in zip(last_ids, last_calls, strict=False):
                content = (
                    f"Standing by: this ended your turn ({TURN_ENDS_WORDS[0].lower()}"
                    f"{TURN_ENDS_WORDS[1:-1]}), and the next message is the sample that "
                    "ended the stand-by."
                    if c.name == "stand_by"
                    else "Not run: a stand-by earlier in the reply ended your turn."
                )
                out.append({"role": "tool", "tool_call_id": cid, "content": content})
            last_ids = []

        for i, t in enumerate(turns[start:], start):
            if t.role == OPERATOR:
                answer_the_ids()
                out.append({"role": "system", "content": str(t.content)})
            elif t.role == MODEL:
                answer_the_ids()
                r: Reply = t.content
                last_calls = r.calls
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
                answer_the_ids()
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
        room = ctx - self.max_reply - tools_cost
        head = messages[0] if messages[0]["role"] == "system" else None
        head_cost = cost[0] if head is not None else 0
        if head_cost > room:
            raise DoorError(
                f"The brief is about {head_cost} tokens and the context is {ctx} tokens, of "
                f"which {self.max_reply} are kept for the reply and {tools_cost} for the "
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
                f"{self.max_reply} kept for the reply; start the server with a larger "
                "--ctx-size (docs/agents/Harness.md)."
            )
        self.dropped_turns = first
        return ([head] if head is not None else []) + body[first:]

    def request_body(self, turns: Sequence[Turn]) -> dict[str, Any]:
        body: dict[str, Any] = {
            "messages": self.messages(turns),
            "stream": False,
            "max_tokens": self.max_reply,  # the reply budget: a runaway stops here
        }
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

    def _failure(self, words: str, final: bool = False) -> None:
        """A request failed: the sample stays open. `failed` is set, which stands the
        station down, only after `FAILURES_TO_STAND_DOWN` in a row, or at once for a
        failure no retry mends (`final`: the conversation does not fit the context)."""
        self.failures += 1
        self.last_error = words
        if final or self.failures >= FAILURES_TO_STAND_DOWN:
            n = self.failures
            self.failed = words if final else f"{words} ({n} failed requests in a row)"

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        """One request, one reply. A failure returns None (the sample stays open) with
        the words in `last_error`, and the caller asks again; `failed` is set after
        `FAILURES_TO_STAND_DOWN` failures in a row, and then every later call returns None
        at once, so the World never waits on a dead server; the drivers stand the station
        down on it."""
        if self.failed is not None:
            return None
        try:
            body = self.request_body(turns)
            r = self.client.post("/v1/chat/completions", json=body)
        except DoorError as e:
            self._failure(str(e), final=True)
            return None
        except httpx.TimeoutException:
            self._failure(
                f"The model server did not answer within {self.timeout:g} s; the sample is "
                "left open."
            )
            return None
        except httpx.ConnectError as e:
            self._failure(self._refused(e))
            return None
        except httpx.HTTPError as e:
            self._failure(f"The model server at {self.base} did not answer: {e}.")
            return None
        if r.status_code != 200:
            self._failure(
                f"The model server at {self.base} answered {r.status_code}: {_error_words(r)}"
            )
            return None
        try:
            message = r.json()["choices"][0]["message"]
        except (ValueError, KeyError, IndexError, TypeError):
            self._failure(f"The model server at {self.base} sent a reply the runner cannot read.")
            return None
        self.failures = 0
        self.last_error = None
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

# This door in a consent record's runtime line (`remote.DOORS`), for the context guard.
DOOR_WORDS = "the local runner (freesail.agents.local)"

# How long one poll of the game waits for the model's next turn, in real seconds
# (judgement: long enough that an idle runner asks the game a few times a minute, short
# enough that Ctrl-C between polls is prompt; the game answers at once when a turn opens).
POLL_WAIT_S = 30.0

# The door's words in the brief (the head's documentation item), plain and exact.
RUNNER_NOTE = (
    "This door is a model server on the owner's machine. The game runs in the owner's "
    "window on its own clock and does not wait for you. Your turn opens at each sampling "
    "point (the glass, a notable event, the end of a stand-by, or a question from the "
    f"captain). {TURN_ENDS_WORDS} What happens while it is open is added to it, so your "
    "next turn carries everything since your last reply. The captain's orders and "
    "questions are typed by the owner in the game's window."
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
    ap.add_argument(
        "--max-reply",
        type=int,
        default=REPLY_MAX_TOKENS,
        help=f"the most tokens one reply may run to (default {REPLY_MAX_TOKENS})",
    )
    ap.add_argument(
        "--request-timeout",
        type=float,
        default=REQUEST_TIMEOUT_S,
        help=f"real seconds one request may take (default {REQUEST_TIMEOUT_S:g})",
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
        max_reply=args.max_reply,
        timeout=args.request_timeout,
    )
    try:
        identity = model.identity()
        server = model.server_words()
        print(f"The model server serves {identity}.", file=out, flush=True)
        runtime = f"FreeSail's game at {args.game}, through {DOOR_WORDS}, {server}"
        print(model.check_context(identity, runtime), file=out, flush=True)
    except DoorError as e:
        print(str(e), file=out, flush=True)
        return EXIT_UNREACHABLE
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
    after = consent.terminal_after(inp, out)
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
        if game.stale:
            # a turn already read has changed (a book shelved): the copy is read again,
            # and the next request is built from the turns as the game serves them now
            turns[:] = [turn_from_dict(t) for t in game.reread()]
        return answer

    took(a)
    try:
        while True:
            if a.get("released"):
                print(a.get("words") or "The station is released.", file=out, flush=True)
                return EXIT_NO_CONSENT if a.get("phase") == "stopped" else EXIT_RELEASED
            if a.get("waiting") == "owner" and a.get("after_answer"):
                # the developer's turn after the answer: a word to the model, or blank to
                # close the record
                words = after(str(a.get("answer_words") or ""))
                game.owner(words or "")
                a = took(game.turns(wait=0))
                continue
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
                if r is None and model.failed is None and model.last_error:
                    # the sample stays open: read the game again (what happened meanwhile
                    # is folded into the turn) and ask again (package 28c)
                    n = f"{model.failures} of {FAILURES_TO_STAND_DOWN}"
                    print(f"{model.last_error} ({n}; asking again)", file=out, flush=True)
                    a = took(game.turns(wait=0))
                    continue
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
