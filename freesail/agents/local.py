"""The local runner (spec M4 §13 as revised; package 28b): a door for a model served on
this machine through an OpenAI-compatible chat-completions endpoint with tool calling,
which is what llama.cpp's `llama-server` serves (and Ollama, on its own port). It is a
client of the running game and of the endpoint, and builds no World.

    python -m freesail.agents.local --game http://localhost:8000 --endpoint http://localhost:8080
        [--model NAME] [--seed N] [--temperature T] [--ctx N] [--station watcher]
        [--session play|test] [--ask-again] [--handover-reserve N|SHARE]
        [--max-reply N] [--request-timeout S]

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
refuses in words, with what it measured, when that is smaller than the longer of the
two briefs the model will meet (the consent brief, measured as this door sends it; and
the station's own brief, measured from its own words with an allowance for what the
ship adds, `station_brief_tokens`: package 37g, item 8, since the officer's brief is
about twice the consent brief and the guard had passed a context the officer's station
could not use), the tool definitions (measured), one turn (`TURN_ALLOWANCE_TOKENS`) and
the reply budget; and says so when it cannot learn it. **No officer is seated when
neither the server nor `--ctx` gives a context size** (the gate's ruling 2, the report's
8.7): without one nothing is asked for and nothing is trimmed, and the server cuts the
conversation unseen (the two Ollama officers of gate 5c's playtests).

**The handover's reserve** (package 37g, item 8; package 37i, item 3): the part of the
context kept free when the harness asks for the handover note. `--handover-reserve`
takes tokens (`30000`) or a share of the context (`0.3`, or `30%`), and may be given
twice, once in each form, when the larger counts; the runner sends it in tokens with the
station request. Unset, the harness's own: three tenths of the context
(`harness.HANDOVER_RESERVE_SHARE`) and never less than 14,000 tokens
(`HANDOVER_RESERVE_TOKENS`), the larger; and never earlier than six tenths of it.

**The budget, by the server's count** (package 37i, item 2). The conversation grows a
sample at a time. When the context size is known (`--ctx-size`, else the server's), the
oldest turns are left out of the request, whole exchanges at a time, so that the system
message, the handover note folded in after it and the latest turns fit with the reply
budget to spare; a brief that alone does not fit stops the run with the numbers. A
sample after the first carries only the readings that changed (package 31c), so the
first sample kept when older ones are left out is sent with every reading as the samples
before it made them (`READINGS_WHOLE`): nothing is withheld. Each message is measured at
`CHARS_PER_TOKEN` characters a token (the harness's one rule) and then scaled by the
server's own figure: every reply carries the tokens the server counted for the request
and the reply (`usage`'s `prompt_tokens` and `completion_tokens` at llama-server and at
Ollama's OpenAI-compatible endpoint; `prompt_eval_count` and `eval_count` in Ollama's
own form), and the runner keeps the ratio of the server's count to its own measure of
what it sent. So the four-character rule stands alone only until the first reply, and in
the context guard before stationing. Game 10 (the review of gate 5c, G15) had the rule
12 to 17 per cent short for its model and samples. The server's count also goes to the
game with the reply (`Reply.served_tokens`), where the harness measures the conversation
by it for the handover note. A count under half the runner's own measure is taken for a
partial one (a server that counts only what it did not have cached) and not used.

**A reply cut off is not a turn** (package 37i, item 1). The runner reads why each reply
ended (`finish_reason`, or Ollama's `done_reason`). A reply cut at the reply limit while
the model was still thinking (no words and no call, its reasoning apart or in an
unclosed `<think>`), or any reply with no words and no call, is asked for once more in
the same request with the reason said at its end, in the runner's own words; the owner is
told at this terminal. If that one is cut off or empty too, the owner is told, the turn
ends with nothing done and the station's journal says why (`GameClient.reply`'s
`cut_off`; the harness's "cut_off" act): no empty reply is passed on as the model's.

**A request refused for its size** (package 37i, item 4). When the server refuses a
request because it does not fit the context (llama-server's `exceed_context_size_error`,
or words to that effect), the runner takes the server's own count of it from the refusal
where it is given, measures by it, leaves out the oldest exchanges that are not the
brief, the handover note or the latest sample, says so once at this terminal, and asks
again at once. It never sends the same request again: each retry is smaller, and when
nothing more can be left out, or the server has refused `OVERSIZE_TRIES` requests in
one turn, the station is stood down with the numbers. Game 10's two seatings both ended
on the same request sent three times.

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
import dataclasses
import json
import math
import re
import sys
from collections.abc import Callable, Sequence
from typing import Any

import httpx

from freesail.agents import consent
from freesail.agents.agent import CAPTAIN, OFFICER, TURN_ENDS_WORDS, station_name
from freesail.agents.harness import (
    HANDOVER_RESERVE_SHARE,
    HANDOVER_RESERVE_TOKENS,
    conversation_text,
)
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

# What the first sample kept says of its readings when the budget has left the samples
# before it out (package 31c): it carries every reading, as those samples had them.
READINGS_WHOLE = (
    "every reading as it stands: the samples before this one are left out for the context"
)

# Tokens kept free for the reply in the context budget: the reply budget itself.
REPLY_RESERVE_TOKENS = REPLY_MAX_TOKENS

# Why a reply ended, as the servers say it when it was cut at the reply limit:
# llama-server's and the OpenAI form's `finish_reason`, Ollama's `done_reason`.
CUT_AT_THE_LIMIT = ("length", "max_tokens")

# A count from the server under this share of the runner's own measure of the same
# request is taken for a partial count (a server that counts only the part of the prompt
# it did not have cached) and not used (judgement: the four-character rule ran 12 to 17
# per cent short in game 10, never by half; a count that low is not of the whole).
PARTIAL_COUNT_SHARE = 0.5

# How much more the runner measures by when the server refuses a request for its size and
# gives no count of its own in the refusal (judgement: game 10's short count, 12 to 17
# per cent, rounded up). With the server's count in the refusal, that count is used.
OVERSIZE_STEP = 1.15

# The most requests the server may refuse for their size in one turn before the station is
# stood down (judgement: the first refusal is answered by the server's own count and one
# smaller request ordinarily fits; a third smaller still that is refused says the context
# the runner was told of is not the one the server has).
OVERSIZE_TRIES = 3

# What the runner says to the model when it asks once more for a reply that was cut off
# or empty (package 37i, item 1): its own words, at the end of the same request.
CUT_WORDS = (
    "From the local runner, not the game: your last reply was cut off at the reply limit "
    "({limit:,} tokens) while you were still thinking, and nothing of it reached the game: "
    "no words and no call. This is the same turn, asked once more; think more briefly, and "
    "answer with a call or with words."
)
EMPTY_WORDS = (
    "From the local runner, not the game: your last reply came with no words and no call, "
    "so nothing reached the game. This is the same turn, asked once more; answer with a "
    "call or with words."
)

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

# What the ship adds to a station's brief beyond its own words, allowed for in the
# context guard (package 37g; measured by the review's reader V1a, K: every reading at
# once is about 1,150 tokens, a first brief's twenty log lines some hundreds, and a
# reseat's brief ran to 6,500 tokens against 4,000 to 4,400 for a first; the captain's
# night orders are the book's lines, a score of them in the starter book). Judgement:
# two thousand five hundred, so that the guard errs toward refusing a context too small.
SITUATION_ALLOWANCE_TOKENS = 2500

# Keys a server might give the loaded file's hash under. llama-server's /props gives the
# path and not a hash, as far as its README says; these are read if a server gives one.
IDENTITY_HASH_KEYS: tuple[str, ...] = ("model_sha256", "model_hash")


# An unclosed or closed `<think>` block at the head of the content, where a server does
# not give the reasoning apart: what is left is what the model said.
THINKING = re.compile(r"(?s)^\s*<think>.*?(?:</think>|$)")

# A refusal's words, read for its size: "the request exceeds the available context size",
# "the input length exceeds the context length"; and the counts in them, "(103679 tokens)".
OVERSIZE_WORDS = ("exceed", "too long", "too large", "longer than", "larger than")
TOKENS_IN_WORDS = re.compile(r"(\d[\d,]*)\s*tokens")


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
        say: Callable[[str], None] | None = None,
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
        # the server's own count (package 37i): the ratio of its count of a request to
        # the runner's four-character measure of it, None until the first reply; the
        # last request's measure; the last reply's counts as the server gave them
        self.ratio: float | None = None
        self._sent_measure = 0
        self.served: dict[str, int] | None = None
        # why the last reply ended as the server said it, and the words when no reply was
        # to be had for the turn (cut off or empty twice; the runner tells the game)
        self.finish: str = ""
        self.cut_off: str | None = None
        self.say = say  # words for the owner at the runner's terminal

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

    def check_context(self, identity: str, runtime: str, station: str = "watcher") -> str:
        """The context guard, before stationing (package 28c): what the station needs,
        measured at `CHARS_PER_TOKEN`: the longer of the two briefs the model will meet
        (the consent brief as this door sends it, and the station's own brief,
        `station_brief_tokens`; package 37g), the tool definitions, one turn
        (`TURN_ALLOWANCE_TOKENS`) and the reply budget. Raises `DoorError` in words, with
        the numbers, when the context the server gives (or `--ctx`) is smaller, and for
        the officer's station when no context size is to be had at all; returns a line
        for the owner otherwise, saying what it measured or that it could not ask."""
        brief = consent.brief_text(identity, runtime, "runner")
        consent_cost = len(json.dumps({"role": "system", "content": brief})) // CHARS_PER_TOKEN + 1
        # the watcher's own brief is shorter than the consent brief, as it was when the
        # guard was written; the officer's is measured (package 37g)
        is_officer = station_name(station) in (OFFICER, CAPTAIN)  # a station with authority
        station_cost = station_brief_tokens(station) if is_officer else 0
        brief_cost = max(consent_cost, station_cost)
        tools_cost = len(json.dumps(self.tools_schema())) // CHARS_PER_TOKEN
        need = brief_cost + tools_cost + TURN_ALLOWANCE_TOKENS + self.max_reply
        served = self.served_context()
        if served is not None:
            self.served_ctx = served[0]
            got, where = served
        elif self.ctx_size:
            got, where = int(self.ctx_size), "--ctx, as the owner gave it"
        elif station_name(station) in (OFFICER, CAPTAIN):
            raise DoorError(
                f"The model server did not say what context it gives {identity}, and no "
                f"--ctx was given: the {station_name(station)} is not seated without a context "
                "size. With none, the harness can neither ask for the handover note in time "
                "nor leave out old turns, and the server cuts the conversation unseen. The "
                f"station needs about {need} tokens (the brief {brief_cost}, the tool "
                f"definitions {tools_cost}, a turn {TURN_ALLOWANCE_TOKENS}, the reply budget "
                f"{self.max_reply}). For Ollama, check with `ollama ps` once the model is "
                "loaded (OLLAMA_CONTEXT_LENGTH or the Modelfile's num_ctx sets it), and state "
                "it with --ctx; llama-server reports its own (docs/agents/Harness.md)."
            )
        else:
            return (
                f"The model server did not say what context it gives {identity}, and no --ctx "
                f"was given; the station needs about {need} tokens (the brief {brief_cost}, "
                f"the tool definitions {tools_cost}, a turn {TURN_ALLOWANCE_TOKENS}, the reply "
                f"budget {self.max_reply}). Ollama's own default is small unless "
                "OLLAMA_CONTEXT_LENGTH or the Modelfile's num_ctx says more: check with "
                "`ollama ps` once the model is loaded, and state it with --ctx."
            )
        which = (
            f"the {station_name(station)}'s own brief"
            if station_cost >= consent_cost
            else "the consent brief, the longer of the two"
        )
        words = (
            f"the model server gives {identity} a context of {got} tokens ({where}); the "
            f"station needs about {need}: the brief {brief_cost} tokens ({which}) and the "
            f"tool definitions {tools_cost} (measured, at {CHARS_PER_TOKEN} characters a "
            f"token), a turn {TURN_ALLOWANCE_TOKENS} and the reply budget {self.max_reply}"
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

    def messages(self, turns: Sequence[Turn], notice: str = "") -> list[dict[str, Any]]:
        """The turns as chat messages, from the latest operator turn on (a door taking
        over a restored station sends the brief again, `Harness.take_over`); `notice`, the
        runner's own words at the end (a reply asked for once more, package 37i)."""
        start = 0
        for i, t in enumerate(turns):
            if t.role == OPERATOR:
                start = i
        out: list[dict[str, Any]] = []
        last_ids: list[str] = []
        last_calls: tuple[ToolCall, ...] = ()
        # the readings as the samples so far make them, and for each message of a sample
        # that carries only the changes, the same sample with every reading (package 31c)
        picture: dict[str, Any] = {}
        whole: dict[int, dict[str, Any]] = {}
        pinned: set[int] = set()  # the handover note folded in after the brief

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
                            content = "Not run: this turn's budget for it was spent."
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
                    if "readings" in d:
                        picture.update(d.get("readings") or {})
                        if d.get("readings_are"):
                            all_of = {**d, "readings_are": READINGS_WHOLE}
                            whole[len(out)] = all_of | {"readings": dict(picture)}
                    if d.get("handover") and d.get("folded"):
                        pinned.add(len(out))
                    out.append({"role": "user", "content": json.dumps(d, ensure_ascii=False)})
        if notice:
            answer_the_ids()
            if out and out[-1]["role"] == "user":
                # one user message, not two in a row, which some chat templates refuse
                out[-1] = {"role": "user", "content": f"{out[-1]['content']}\n\n{notice}"}
            else:
                out.append({"role": "user", "content": notice})
        return self._budget(out, whole, pinned)

    def measure(self, thing: Any) -> int:
        """The runner's own measure of a message or of the tool definitions: four
        characters a token (`CHARS_PER_TOKEN`), before the server's figure scales it."""
        return len(json.dumps(thing, ensure_ascii=False)) // CHARS_PER_TOKEN + 1

    def scaled(self, measure: int) -> int:
        """A measure in the server's tokens: by the ratio of its count to the runner's
        measure of the last request (package 37i, item 2), and as it is until the first
        reply."""
        return measure if self.ratio is None else int(math.ceil(measure * self.ratio))

    def _budget(
        self,
        messages: list[dict[str, Any]],
        whole: dict[int, dict[str, Any]] | None = None,
        pinned: set[int] | None = None,
    ) -> list[dict[str, Any]]:
        self.dropped_turns = 0
        ctx = self.context_size()
        tools_measure = self.measure(self.tools_schema())
        if not ctx or not messages:
            self._sent_measure = sum(self.measure(m) for m in messages) + tools_measure
            return messages
        measures = [self.measure(m) for m in messages]
        cost = [self.scaled(m) for m in measures]
        tools_cost = self.scaled(tools_measure)
        room = ctx - self.max_reply - tools_cost
        # the brief, and the handover note folded in after it, are never left out
        lead = 0
        if messages[0]["role"] == "system":
            lead = 1
            while lead < len(messages) - 1 and lead in (pinned or set()):
                lead += 1
        head = messages[:lead]
        head_cost = sum(cost[:lead])
        if head_cost > room:
            raise DoorError(
                f"The brief is about {head_cost} tokens and the context is {ctx} tokens, of "
                f"which {self.max_reply} are kept for the reply and {tools_cost} for the "
                "tool definitions; start the server with a larger --ctx-size "
                "(docs/agents/Harness.md)."
            )
        body = messages[lead:]
        body_cost = cost[lead:]
        offset = lead
        whole = dict(whole or {})
        total = head_cost + sum(body_cost)
        first = 0
        while True:
            while total > room and first < len(body):
                # leave out the oldest whole exchange: up to the next user message
                total -= body_cost[first]
                first += 1
                while first < len(body) and body[first]["role"] != "user":
                    total -= body_cost[first]
                    first += 1
            if first >= len(body):
                raise DoorError(
                    f"The brief and the latest sample do not fit a context of {ctx} tokens "
                    f"with {self.max_reply} kept for the reply; start the server with a "
                    "larger --ctx-size (docs/agents/Harness.md)."
                )
            at = offset + first
            if first == 0 or at not in whole:
                break
            # the samples before the first kept are left out: it carries every reading as
            # they made them (package 31c), and if that does not fit, more goes
            msg = {"role": "user", "content": json.dumps(whole.pop(at), ensure_ascii=False)}
            c = self.scaled(self.measure(msg))
            total += c - body_cost[first]
            body = [*body[:first], msg, *body[first + 1 :]]
            body_cost = [*body_cost[:first], c, *body_cost[first + 1 :]]
        self.dropped_turns = first
        sent = head + body[first:]
        self._sent_measure = sum(self.measure(m) for m in sent) + tools_measure
        return sent

    def request_body(self, turns: Sequence[Turn], notice: str = "") -> dict[str, Any]:
        body: dict[str, Any] = {
            "messages": self.messages(turns, notice),
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
        """One turn's reply. A failure returns None (the sample stays open) with the words
        in `last_error`, and the caller asks again; `failed` is set after
        `FAILURES_TO_STAND_DOWN` failures in a row, and then every later call returns None
        at once, so the World never waits on a dead server; the drivers stand the station
        down on it. Package 37i: a reply cut off while the model thought, or empty, is
        asked for once more with the reason said; cut off or empty again, `cut_off` holds
        the words and an empty reply is returned, which the runner does not pass on as the
        model's (the game ends the turn with nothing done). A request the server refuses
        for its size is asked again at once, smaller, by the server's own count."""
        if self.failed is not None:
            return None
        self.cut_off = None
        notice = ""
        first_cut = ""
        refused = 0
        last_messages: list[dict[str, Any]] | None = None
        while True:
            try:
                body = self.request_body(turns, notice)
                if body["messages"] == last_messages:
                    # the same request is never sent again after a refusal for its size:
                    # measure by more until another exchange is left out
                    self.ratio = (self.ratio or 1.0) * OVERSIZE_STEP
                    continue
                r = self.client.post("/v1/chat/completions", json=body)
            except DoorError as e:
                self._failure(str(e), final=True)
                return None
            except httpx.TimeoutException:
                self._failure(
                    f"The model server did not answer within {self.timeout:g} s; the sample "
                    "is left open."
                )
                return None
            except httpx.ConnectError as e:
                self._failure(self._refused(e))
                return None
            except httpx.HTTPError as e:
                self._failure(f"The model server at {self.base} did not answer: {e}.")
                return None
            if r.status_code != 200:
                size = self._refused_for_size(r)
                if size is None:
                    self._failure(
                        f"The model server at {self.base} answered {r.status_code}: "
                        f"{_error_words(r)}"
                    )
                    return None
                refused += 1
                words = self._oversize_words(size)
                if not self.context_size():
                    self._failure(
                        f"{words} The runner knows no context size to leave old exchanges "
                        "out against; state it with --ctx (docs/agents/Harness.md).",
                        final=True,
                    )
                    return None
                if refused >= OVERSIZE_TRIES:
                    self._failure(
                        f"{words} The server refused {refused} requests for their size in one "
                        "turn, each smaller than the last; the context it has is not the one "
                        "the runner was told of.",
                        final=True,
                    )
                    return None
                if refused == 1:
                    self._tell(
                        f"{words} The oldest exchanges are left out (never the brief, the "
                        "handover note or the latest sample) and it is asked again; from now "
                        "on the runner measures by the server's count."
                    )
                last_messages = body["messages"]
                continue
            read = self._read(r)
            if read is None:
                self._failure(
                    f"The model server at {self.base} sent a reply the runner cannot read."
                )
                return None
            message, finish, counts = read
            self.failures = 0
            self.last_error = None
            self.finish = finish
            self._take_count(counts)
            self.exchanges.append(message)
            reply = self.parse(message)
            why = self._no_reply(reply, message, finish)
            if why is None:
                if self.served:
                    reply = dataclasses.replace(reply, served_tokens=dict(self.served))
                if self.on_reply is not None:
                    self.on_reply(reply)
                return reply
            if not first_cut:
                first_cut = why
                notice = CUT_WORDS.format(limit=self.max_reply) if why == "cut" else EMPTY_WORDS
                self._tell(f"{self._cut_words(why)}; it is asked once more, with the reason.")
                last_messages = None
                continue
            # cut off or empty again: the turn ends with nothing done
            self.cut_off = (
                f"{self._cut_words(first_cut)}, and {self._cut_words(why, again=True)} when "
                "asked once more; the turn ended with nothing done"
            )
            self._tell(
                f"{self.cut_off}, and the station's journal says so. "
                + (
                    f"A larger --max-reply (now {self.max_reply:,}) gives it more room."
                    if "cut off" in self.cut_off
                    else ""
                )
            )
            return Reply(text="", calls=(), raw=reply.raw)

    # -- the reply's end, the server's count, a refusal for size (package 37i) ----------

    def _tell(self, words: str) -> None:
        if self.say is not None:
            self.say(words.strip())

    @staticmethod
    def _read(r: httpx.Response) -> tuple[dict[str, Any], str, tuple[int, int] | None] | None:
        """The response message, why it ended and the server's counts (prompt, reply),
        from the OpenAI form (`choices[0].message`, `finish_reason`, `usage`: llama-server,
        and Ollama's OpenAI-compatible endpoint) or Ollama's own (`message`, `done_reason`,
        `prompt_eval_count` and `eval_count`). None when it is neither."""
        try:
            data = r.json()
        except ValueError:
            return None
        if not isinstance(data, dict):
            return None
        choices = data.get("choices")
        if isinstance(choices, list) and choices and isinstance(choices[0], dict):
            message = choices[0].get("message")
            finish = choices[0].get("finish_reason")
        else:
            message = data.get("message")
            finish = data.get("done_reason")
        if not isinstance(message, dict):
            return None
        counts: tuple[int, int] | None = None
        usage = data.get("usage")
        prompt = (usage or {}).get("prompt_tokens") if isinstance(usage, dict) else None
        reply = (usage or {}).get("completion_tokens") if isinstance(usage, dict) else None
        if prompt is None:
            prompt, reply = data.get("prompt_eval_count"), data.get("eval_count")
        if isinstance(prompt, int) and not isinstance(prompt, bool) and prompt > 0:
            counts = (prompt, reply if isinstance(reply, int) and reply >= 0 else 0)
        return message, str(finish or ""), counts

    def _take_count(self, counts: tuple[int, int] | None) -> None:
        """The server's count of the request just answered: the ratio to the runner's own
        measure of it is what the budget measures by from now on (package 37i, item 2),
        unless the count is so far under the measure that it cannot be of the whole."""
        self.served = None
        if counts is None or not self._sent_measure:
            return
        prompt, reply = counts
        if prompt < PARTIAL_COUNT_SHARE * self._sent_measure:
            return
        self.ratio = prompt / self._sent_measure
        self.served = {"prompt": prompt, "reply": reply}

    @staticmethod
    def _no_reply(reply: Reply, message: dict[str, Any], finish: str) -> str | None:
        """Why a reply is none (package 37i, item 1): "cut" when it was cut at the reply
        limit while the model was thinking (no words and no call; its reasoning apart, or
        an unclosed `<think>`), "empty" when it has no words and no call however it
        ended; None for a reply to pass on."""
        said = THINKING.sub("", str(reply.text or "")).strip()
        if said or reply.calls:
            return None
        thinking = bool(
            message.get("reasoning_content")
            or message.get("reasoning")
            or message.get("thinking")
            or "<think>" in str(reply.text or "")
        )
        return "cut" if finish in CUT_AT_THE_LIMIT and thinking else "empty"

    def _cut_words(self, why: str, again: bool = False) -> str:
        if why == "cut":
            if again:
                return "was cut off again"
            return (
                f"The model's reply was cut off at the reply limit ({self.max_reply:,} tokens) "
                "while it was still thinking"
            )
        if again:
            return "came empty again"
        return "The model's reply came with no words and no call"

    def _refused_for_size(self, r: httpx.Response) -> tuple[int | None, int | None] | None:
        """A refusal because the request does not fit the context: the server's count of
        the request and the context it has, each where the refusal gives it; None for any
        other answer (llama-server: 400 with `exceed_context_size_error`, its message "the
        request exceeds the available context size", and `n_prompt_tokens` and `n_ctx`)."""
        if r.status_code < 400:
            return None
        try:
            err = r.json().get("error")
        except (ValueError, AttributeError):
            err = None
        info = err if isinstance(err, dict) else {}
        words = str(info.get("message") or err or r.text or "").lower()
        kind = str(info.get("type") or "").lower()
        if "exceed_context" not in kind and not (
            "context" in words and any(w in words for w in OVERSIZE_WORDS)
        ):
            return None

        def number(v: Any) -> int | None:
            return v if isinstance(v, int) and not isinstance(v, bool) and v > 0 else None

        asked = number(info.get("n_prompt_tokens"))
        ctx = number(info.get("n_ctx"))
        if asked is None:
            found = [int(n.replace(",", "")) for n in TOKENS_IN_WORDS.findall(words)]
            if found:
                asked = found[0]
                if ctx is None and len(found) > 1:
                    ctx = found[1]
        return asked, ctx

    def _oversize_words(self, size: tuple[int | None, int | None]) -> str:
        """Measure by the server's count of the refused request (or `OVERSIZE_STEP` more
        when it gave none), take the context it names, and say what was refused."""
        asked, ctx = size
        if ctx and (self.served_ctx is None or ctx < self.served_ctx):
            self.served_ctx = ctx
        before = self.ratio or 1.0
        if asked and self._sent_measure:
            self.ratio = max(asked / self._sent_measure, before)
        else:
            self.ratio = before * OVERSIZE_STEP
        counted = f" ({asked:,} tokens by its count" if asked else " (no count given"
        held = f"; the context is {ctx:,})" if ctx else ")"
        return f"The model server refused the request for its size{counted}{held}."

    def close(self) -> None:
        self.client.close()


def station_brief_tokens(station: str) -> int:
    """What a station's own brief costs, for the context guard (package 37g, item 8; the
    report's 8.2, item 14): the brief built from the station's own words as the harness
    builds it (the generated head, the domain, the station brief, this door's note),
    measured at `CHARS_PER_TOKEN`, with `SITUATION_ALLOWANCE_TOKENS` for what the ship
    adds (the log's last lines, every reading, the captain's night orders). No World is
    built for it: the runner is a client."""
    from freesail.agents.agent import CAPTAIN, SESSION_PLAY, Brief, captain, officer, watcher

    name = station_name(station)
    is_officer = name in (OFFICER, CAPTAIN)
    st = officer() if name == OFFICER else captain() if name == CAPTAIN else watcher()
    brief = Brief.build(
        st,
        SESSION_PLAY,
        [],
        {},
        tool_names(),
        door_note=RUNNER_NOTE,
        night_orders=[] if is_officer else None,
        deck="The deck is the captain's now." if is_officer else "",
    )
    cost = len(json.dumps({"role": "system", "content": brief.text()})) // CHARS_PER_TOKEN + 1
    return cost + SITUATION_ALLOWANCE_TOKENS


def reserve_form(text: str) -> tuple[str, float]:
    """One `--handover-reserve`: tokens (`30000`) or a share of the context (`0.3`,
    `30%`), as ("tokens", n) or ("share", s); refused in words otherwise."""
    t = str(text).strip().replace(",", "").replace("_", "")
    try:
        if t.endswith("%"):
            share = float(t[:-1]) / 100.0
            if 0.0 < share < 1.0:
                return "share", share
        else:
            value = float(t)
            if 0.0 < value < 1.0:
                return "share", value
            if value >= 1.0 and value == int(value):
                return "tokens", float(int(value))
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(
        f"{text!r} is neither a number of tokens (30000) nor a share of the context "
        "between 0 and 1 (0.3, or 30%)"
    )


def handover_reserve_tokens(
    forms: Sequence[tuple[str, float]] | None, context: int | None
) -> int | None:
    """The reserve to send with the station request, in tokens (package 37i, item 3): the
    larger of the forms the owner gave, a share taken of the context; None when none was
    given (the harness's own share then), or when only a share was and no context is
    known."""
    if not forms:
        return None
    values = [
        int(v) if kind == "tokens" else int(v * context)
        for kind, v in forms
        if kind == "tokens" or context
    ]
    return max(values) if values else None


def handover_words(
    forms: Sequence[tuple[str, float]] | None, context: int, reserve: int | None
) -> str:
    """One line for the owner: where the handover note will be asked for."""
    from freesail.agents.harness import HANDOVER_AT_FRACTION

    if reserve is None:
        reserve = int(max(HANDOVER_RESERVE_SHARE * context, HANDOVER_RESERVE_TOKENS))
        how = (
            f"the harness's own share, {HANDOVER_RESERVE_SHARE:g} of the context and never "
            f"less than {HANDOVER_RESERVE_TOKENS:,} tokens"
        )
    else:
        given = " and ".join(
            f"{int(v):,} tokens" if kind == "tokens" else f"{v:g} of the context"
            for kind, v in forms or ()
        )
        how = f"--handover-reserve {given}" + (", the larger" if len(forms or ()) > 1 else "")
    at = max(context - reserve, int(HANDOVER_AT_FRACTION * context))
    return (
        f"The handover note is asked for when the conversation, by the server's own count, "
        f"has left less than {reserve:,} of the {context:,} tokens ({how}), and never "
        f"before {HANDOVER_AT_FRACTION:g} of them: at about {at:,}."
    )


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
    "point (the glass, a notable or urgent event, the end of a stand-by, or a question or "
    f"a word from the captain). {TURN_ENDS_WORDS} What happens while it is open is added to "
    "it, so your "
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
    ap.add_argument(
        "--station",
        default="watcher",
        choices=["watcher", "officer", "captain"],
        help="the station asked for: the watcher, the officer of the watch (package 37), "
        "or the captain's station (package 40)",
    )
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    ap.add_argument(
        "--handover-reserve",
        type=reserve_form,
        action="append",
        metavar="N|SHARE",
        help=(
            "the part of the context kept free when the harness asks the officer for the "
            "handover note, in tokens (30000) or as a share of the context (0.3, or 30%%); "
            "given twice, once in each form, the larger counts (default: the harness's own "
            f"share, {HANDOVER_RESERVE_SHARE:g}, and never less than "
            f"{HANDOVER_RESERVE_TOKENS} tokens; the note is asked for when the conversation, "
            "by the server's own count, has left less than this, and never before six "
            "tenths of the context)"
        ),
    )
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
        say=lambda words: print(words, file=out, flush=True),
    )
    try:
        identity = model.identity()
        server = model.server_words()
        print(f"The model server serves {identity}.", file=out, flush=True)
        runtime = f"FreeSail's game at {args.game}, through {DOOR_WORDS}, {server}"
        print(model.check_context(identity, runtime, args.station), file=out, flush=True)
    except DoorError as e:
        print(str(e), file=out, flush=True)
        return EXIT_UNREACHABLE
    context = model.context_size()
    reserve = handover_reserve_tokens(args.handover_reserve, context)
    if context and station_name(args.station) in (OFFICER, CAPTAIN):
        print(handover_words(args.handover_reserve, context, reserve), file=out, flush=True)
    game = GameClient(args.game, args.station, transport=game_transport, http=game_http)
    try:
        first = game.station(
            identity,
            "runner",
            door_note=RUNNER_NOTE,
            session_kind=args.session,
            client=server,
            ask_again=args.ask_again,
            # the context this door gives the model, for the handover note (package 37;
            # spec M4 open item 9b): the harness asks for the note when the conversation
            # has left less than a reserve of it (`--handover-reserve`; package 37g)
            context_tokens=context,
            handover_reserve=reserve,
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
                if model.cut_off:
                    # no reply to be had for the turn (package 37i, item 1): the game ends
                    # it with nothing done and the journal says why; no empty reply is
                    # passed on as the model's
                    a = took(game.reply(Reply(), cut_off=model.cut_off))
                    continue
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
