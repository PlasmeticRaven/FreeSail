"""The API door (spec M6 §13; package 42): a model seated through its maker's own API,
with no chat client between, the Anthropic Messages API with tool use first. A runner on
the same harness as the local runner (`local.py` is its pattern): a client of the running
game and of the API, no World of its own, the consent gate run by the game.

    python -m freesail.agents.api --game http://localhost:8000 --model NAME
        [--station watcher|officer|captain] [--effort low|medium|high|xhigh|max]
        [--max-reply N] [--request-timeout S] [--base-url URL] [--key-file FILE]
        [--session play|test] [--ask-again] [--handover-reserve N|SHARE]
        [--exchanges FILE]
    python -m freesail.agents.api --store-key

**The model is the owner's** (`--model`, which has no default: no model's name is written
in this repository). Before stationing, the door asks the API what that name is
(`models.retrieve`): the name the server reports is the identity the consent record is
kept under (the record's form for a served identity, `consent.IDENTITY_KINDS["api"]`),
and the context it gives, which goes to the game for the handover note. Every reply is
checked to come from that model: a reply the server says another model wrote is not
passed on, and the station is stood down with the reason (consent is per model, and a
server-side fallback, which this door never asks for, would put another model's words at
the station under this one's consent).

**The wire** (`ApiModel.request`): package 27's turns as the Messages API has them, as the
local runner translates them for chat-completions. The latest operator turn (the brief)
is the system prompt; a sample is a user message carrying its JSON; tool results are
`tool_result` blocks answering the assistant's `tool_use` blocks by id; a plain
conversation's turn (the consent step's) is a user message in words; a model turn is an
assistant message, sent back as the API returned it (its thinking blocks with their
signatures, its text, its tool calls with the API's own ids) where the door has it, and
rebuilt from the reply otherwise (a brief sent again, a reread after a shelving). The tool
definitions are the harness's (`tools.parameters_schema`), the ones it offers. **Every
request is streamed** and the final message is taken whole from the stream
(`get_final_message`), so a long reply never meets an HTTP timeout. **The brief and the
library are cached**: the system block carries a cache breakpoint (the tools and the
brief, sent every turn), and the request's own breakpoint caches the conversation up to
its last block, so what was read last turn is read from the cache this one. **Thinking**
is the model's own (adaptive); `--effort` sets its effort (`output_config.effort`), and
without it the model's default stands. Thinking cannot be switched off on the current
models (a request that asks it is refused), so "off" is not offered; the brief of package
42 asked for it, and the API's shapes as they stand decided. The harness's conversation is
not append-only (a book shelved is served as its stub, the handover note folds the
conversation), and the API binds a thinking block to the conversation before it; so every
request sets `prefix_mismatch_behavior: drop_block` (the `thinking-binding-controls`
beta): a block whose conversation changed is dropped by the API rather than the request
refused.

**The server's own count.** Every reply's usage (in, out, read from the cache and written
to it) is kept, sent to the game with the reply (`Reply.served_tokens`, which the harness
measures the conversation by for the handover note), and said at this terminal at each
handover and at the end: what the server reported it used. Cost is the owner's.

**A reply cut off** at the reply limit (`stop_reason: max_tokens`) with a tool call in it
or no words is asked for once more in the same request, with the reason said at its end
in the door's own words (37i's rule); cut off again, the turn ends with nothing done and
the station's journal says why. A **refusal** by the API's safeguards (`stop_reason:
refusal`) is not asked again: the turn ends with nothing done, the journal saying so with
the category the server gave.

**The key** (the security pass, §13 and the owner's note of 2026-10-10) is read first from
the platform's credential store through `keyring` (the Windows Credential Manager, the
macOS Keychain, the Secret Service on Linux), under the service `freesail` and the account
`anthropic-api`, put there once by `--store-key`, which prompts without echo and writes
nothing else; second from the environment (`FREESAIL_API_KEY`, then the SDK's own
`ANTHROPIC_API_KEY`); third from a file named with `--key-file`, outside the repository.
Never from a setting file the game writes. It goes to the SDK and from there into the
request's header and nowhere else: it is never printed, logged, saved, journaled, in a
transcript or in a sample. The door refuses to start when the key would be written
anywhere the game keeps (`refusal_to_start`): a key file inside the repository (which
holds the records, the saves and the journals), the key in any word the door sends the
game (the model's name, the client's words), a base URL carrying a credential, or the
SDK's debug logging switched on. What the door keeps of an exchange (`exchanges`, and the
file `--exchanges` names) is the request's body and the reply's, never a header, and is
scanned for the key before it is written.

The **OpenRouter dialect** (decision 31): `--dialect openrouter` speaks the
chat-completions shape the local runner speaks (`OpenRouterModel`, a `LocalModel` with
the key in its header), with its own key (the account `openrouter`, `FREESAIL_OPENROUTER_KEY`,
`OPENROUTER_API_KEY`) and base URL.

Tested against a local HTTP server speaking the Messages API's shape
(`tests/test_api_door.py`), never the API itself.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from freesail.agents import local
from freesail.agents.agent import CAPTAIN, OFFICER, TURN_ENDS_WORDS, station_name
from freesail.agents.harness import conversation_text
from freesail.agents.model import MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.agents.remote import GameClient, GameError
from freesail.agents.tools import TOOLS, parameters_schema, tool_names

__all__ = [
    "DOOR_WORDS",
    "KEY_ENV",
    "KEY_SHAPES",
    "KEYRING_ACCOUNT",
    "KEYRING_SERVICE",
    "ApiModel",
    "KeyError_",
    "Usage",
    "main",
    "read_key",
    "refusal_to_start",
]

ROOT = Path(__file__).resolve().parents[2]

# The credential store's names for the key (the owner's note of 2026-10-10): a service and
# an account of the game's own, one account a dialect.
KEYRING_SERVICE = "freesail"
KEYRING_ACCOUNT = "anthropic-api"
OPENROUTER_ACCOUNT = "openrouter"

# The environment's names for the key, in the order they are read: the game's own, then
# the SDK's (which the SDK would read of itself; the door reads it and hands it over, so
# that where the key came from is said).
KEY_ENV: tuple[str, ...] = ("FREESAIL_API_KEY", "ANTHROPIC_API_KEY")
OPENROUTER_KEY_ENV: tuple[str, ...] = ("FREESAIL_OPENROUTER_KEY", "OPENROUTER_API_KEY")

# The shapes of a key, for the scans (the door's own before it writes an exchange, and the
# test that greps the repository and the records): the SDK's prefix, OpenRouter's, and a
# bearer header with a token. Written in pieces, so that this file is no match of its own.
KEY_SHAPES: tuple[re.Pattern[str], ...] = (
    re.compile("sk" + r"-ant-[A-Za-z0-9_\-]{8,}"),
    re.compile("sk" + r"-or-[A-Za-z0-9_\-]{8,}"),
    re.compile(r"(?i)\bbear" + r"er\s+[A-Za-z0-9._~+/=\-]{16,}"),
    re.compile(r"(?i)x-api-" + r"key\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
)

# The most tokens one reply may run to, thinking included (`max_tokens`; `--max-reply`).
# Judgement: a station's reply is a few lines and a few calls, and a thinking model at a
# high effort thinks some thousands of tokens first; sixteen thousand leaves it room and
# bounds a runaway. The request is streamed, so a large budget meets no HTTP timeout.
REPLY_MAX_TOKENS = 16000

# One request's real seconds (`--request-timeout`): the SDK's own default, ten minutes.
REQUEST_TIMEOUT_S = 600.0

# The effort levels the API offers (`output_config.effort`).
EFFORTS: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")

# The beta that lets a request say what the API does with a thinking block whose
# conversation changed: dropped, not refused (the harness's shelf and handover edit the
# conversation; module docstring).
THINKING_BINDING_BETA = "thinking-binding-controls-2026-08-01"

# The exchanges the door keeps in memory, the latest (judgement: a request is some forty
# kilobytes and grows with the watch; the `--exchanges` file keeps every one).
EXCHANGES_KEPT = 20

# Failures in a row after which the station is stood down (the local runner's figure).
FAILURES_TO_STAND_DOWN = local.FAILURES_TO_STAND_DOWN

# What the door says to the model when it asks once more for a reply cut off (37i's rule).
CUT_WORDS = (
    "From the API door, not the game: your last reply was cut off at the reply limit "
    "({limit:,} tokens) before it was whole, and nothing of it reached the game. This is "
    "the same turn, asked once more; think more briefly, and answer with a call or with "
    "words."
)
EMPTY_WORDS = (
    "From the API door, not the game: your last reply came with no words and no call, so "
    "nothing reached the game. This is the same turn, asked once more; answer with a call "
    "or with words."
)

# The door in a consent record's runtime line and the log's words (`remote.DOORS`).
DOOR_WORDS = "the API door (freesail.agents.api)"

# The door's words in the brief (the head's documentation item).
API_NOTE = (
    "This door is the model's own API, called by the game on the owner's machine with no "
    "chat client between; the owner is at the door and in the game's window. The game runs "
    "on its own clock and does not wait for you. Your turn opens at each sampling point "
    "(the glass, a notable or urgent event, the end of a stand-by, or a question or a word "
    f"from the captain). {TURN_ENDS_WORDS} What happens while it is open is added to it, so "
    "your next turn carries everything since your last reply. The captain's orders and "
    "questions are typed by the owner in the game's window."
)

# The SDK's headers that describe the machine it runs on (its operating system, processor,
# Python and the SDK's own version), which the door leaves out of every request.
PLATFORM_HEADERS: tuple[str, ...] = (
    "X-Stainless-OS",
    "X-Stainless-Arch",
    "X-Stainless-Runtime",
    "X-Stainless-Runtime-Version",
    "X-Stainless-Lang",
    "X-Stainless-Package-Version",
    "X-Stainless-Async",
)

# A picture's words in a tool result when it cannot be shown (the door cannot fetch it).
PICTURE_GONE = "The picture is no longer held by the game; ask for it again."


class KeyError_(Exception):  # noqa: N801  (not the builtin: a key the door cannot use)
    """No key to be had, or one the door will not use; the message says why, in words
    for the owner, and never holds the key."""


# ---------------------------------------------------------------------------
# The key's road
# ---------------------------------------------------------------------------


def _keyring() -> Any:
    try:
        import keyring
    except ImportError:
        return None
    return keyring


def read_key(
    *,
    account: str = KEYRING_ACCOUNT,
    env_names: Sequence[str] = KEY_ENV,
    key_file: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> tuple[str, str]:
    """The key and where it was found, in words: the credential store first (through
    `keyring`, under `KEYRING_SERVICE` and `account`), the environment second, the file
    named at the command line third. `KeyError_` when none has it."""
    environ = os.environ if environ is None else environ
    kr = _keyring()
    tried: list[str] = []
    if kr is not None:
        try:
            key = kr.get_password(KEYRING_SERVICE, account)
        except Exception as e:  # noqa: BLE001  (a store that is locked, absent or refuses)
            key = None
            tried.append(f"the credential store could not be read ({type(e).__name__})")
        else:
            tried.append("the credential store has none")
        if key:
            return key.strip(), f"the credential store (service {KEYRING_SERVICE}, {account})"
    else:
        tried.append("the keyring package is not installed")
    for name in env_names:
        value = (environ.get(name) or "").strip()
        if value:
            return value, f"the environment ({name})"
    tried.append(f"the environment has none of {', '.join(env_names)}")
    if key_file:
        path = Path(key_file).expanduser()
        try:
            value = path.read_text(encoding="utf-8").strip()
        except OSError as e:
            raise KeyError_(f"The key file {path} could not be read ({e.strerror}).") from None
        if value:
            return value, f"the file {path}"
        tried.append(f"the file {path} is empty")
    raise KeyError_(
        "No key for the API: "
        + "; ".join(tried)
        + ". Put it in the credential store once with --store-key (docs/agents/Harness.md)."
    )


def store_key(
    *,
    account: str = KEYRING_ACCOUNT,
    prompt: Callable[[str], str] = getpass.getpass,
    out: Any = None,
) -> int:
    """`--store-key`: the key asked for without echo and put in the credential store, and
    nothing else written anywhere."""
    out = out or sys.stdout
    kr = _keyring()
    if kr is None:
        print(
            "The keyring package is not installed (py -m pip install keyring); the key "
            "can be given in the environment instead (docs/agents/Harness.md).",
            file=out,
        )
        return local.EXIT_UNREACHABLE
    key = (prompt(f"The API key for {account} (not shown as you type): ") or "").strip()
    if not key:
        print("Nothing was typed; nothing is stored.", file=out)
        return local.EXIT_UNREACHABLE
    try:
        kr.set_password(KEYRING_SERVICE, account, key)
    except Exception as e:  # noqa: BLE001
        print(f"The credential store refused it ({type(e).__name__}).", file=out)
        return local.EXIT_UNREACHABLE
    print(
        f"The key is in the credential store (service {KEYRING_SERVICE}, account {account}). "
        "Nothing else was written.",
        file=out,
    )
    return 0


def _inside(path: Path, folder: Path) -> bool:
    try:
        path.resolve().relative_to(folder.resolve())
    except ValueError:
        return False
    return True


def refusal_to_start(
    key: str,
    *,
    key_file: str | None = None,
    sent: Sequence[str] = (),
    base_url: str | None = None,
    environ: Mapping[str, str] | None = None,
    keeps: Sequence[Path] = (),
) -> str | None:
    """Why the door will not start with this key, in words that never hold it; None when
    it may. The key would be written where the game keeps things: a key file inside the
    repository (the records, the saves and the journals are kept there) or inside a folder
    the game keeps (`keeps`); the key inside any word the door sends the game (`sent`: the
    model's name, the client's words, the door's note), which a consent record, a log line
    or a save would hold; a base URL carrying a credential (user and password, or a token
    in its query); the SDK's debug logging, which writes a request's particulars."""
    environ = os.environ if environ is None else environ
    if len(key) < 8:
        return "The key is too short to be one (fewer than eight characters)."
    if key_file:
        path = Path(key_file).expanduser()
        for folder in (ROOT, *keeps):
            if _inside(path, folder):
                return (
                    f"The key file {path} is inside {folder}, where the game keeps its records, "
                    "saves and journals; keep it outside, or in the credential store "
                    "(--store-key)."
                )
    for words in sent:
        if key in str(words):
            return (
                "The key is in words the door would send the game (the model's name or the "
                "client's words), where a consent record, a log line or a save would keep it."
            )
    if base_url:
        if re.search(r"//[^/@]+@", base_url) or re.search(
            r"(?i)[?&](key|token|api[-_]?key|auth)[=]", base_url
        ):
            return "The base URL carries a credential; give the key by its own road."
        if key in base_url:
            return "The base URL holds the key; give the key by its own road."
    if str(environ.get("ANTHROPIC_LOG") or "").strip().lower() in ("debug", "info"):
        return (
            "The SDK's logging is switched on (ANTHROPIC_LOG); it writes a request's "
            "particulars to the terminal. Unset it for a game."
        )
    return None


def scrub(text: str, key: str) -> str:
    """Text with the key and the shapes of a key taken out, for anything the door writes."""
    if key:
        text = text.replace(key, "[the key]")
    for shape in KEY_SHAPES:
        text = shape.sub("[a key's shape]", text)
    return text


# ---------------------------------------------------------------------------
# The server's own count
# ---------------------------------------------------------------------------


@dataclass
class Usage:
    """What the server reported it used, summed over the requests: tokens in (read from
    the cache, written to it, and neither), and out."""

    requests: int = 0
    uncached: int = 0
    cache_read: int = 0
    cache_written: int = 0
    out: int = 0
    by_request: list[dict[str, int]] = field(default_factory=list)

    @property
    def tokens_in(self) -> int:
        return self.uncached + self.cache_read + self.cache_written

    def add(self, usage: Any) -> dict[str, int]:
        def n(name: str) -> int:
            v = getattr(usage, name, None) if not isinstance(usage, dict) else usage.get(name)
            return int(v) if isinstance(v, int) and not isinstance(v, bool) else 0

        one = {
            "uncached": n("input_tokens"),
            "cache_read": n("cache_read_input_tokens"),
            "cache_written": n("cache_creation_input_tokens"),
            "out": n("output_tokens"),
        }
        self.requests += 1
        self.uncached += one["uncached"]
        self.cache_read += one["cache_read"]
        self.cache_written += one["cache_written"]
        self.out += one["out"]
        self.by_request.append(one)
        return one

    def words(self, when: str = "so far") -> str:
        if not self.requests:
            return f"The API has reported no use {when}: no request was answered."
        reqs = f"{self.requests} request{'s' if self.requests != 1 else ''}"
        return (
            f"The API reported, {when}, for {reqs}: {self.tokens_in:,} tokens in "
            f"({self.cache_read:,} read from the cache, {self.cache_written:,} written to it, "
            f"{self.uncached:,} not cached) and {self.out:,} tokens out."
        )


# ---------------------------------------------------------------------------
# The door's model
# ---------------------------------------------------------------------------


def _key_of(reply: Reply) -> str:
    """A reply's fingerprint, by which the door finds the content the API returned for it
    (its thinking blocks and its own tool ids) when the turn comes back from the game."""
    return json.dumps(
        {"text": reply.text, "calls": [[c.name, c.args] for c in reply.calls]},
        sort_keys=True,
        ensure_ascii=False,
    )


def _block_param(block: Any) -> dict[str, Any] | None:
    """A content block of the API's reply as a block to send back: thinking with its
    signature, redacted thinking, text, a tool call with its id; None for any other."""
    d = block if isinstance(block, dict) else block.to_dict()
    kind = d.get("type")
    if kind == "thinking":
        return {
            "type": "thinking",
            "thinking": d.get("thinking") or "",
            "signature": d["signature"],
        }
    if kind == "redacted_thinking":
        return {"type": "redacted_thinking", "data": d["data"]}
    if kind == "text":
        return {"type": "text", "text": d.get("text") or ""} if d.get("text") else None
    if kind == "tool_use":
        return {"type": "tool_use", "id": d["id"], "name": d["name"], "input": d.get("input") or {}}
    return None


class ApiModel:
    """A `Model` for the Messages API, with the local runner's door contract: `reply`
    returns a `Reply`, or None with `last_error` (the sample stays open and the door asks
    again) or `failed` (the station is stood down); `cut_off` holds the words when no
    reply was to be had for the turn."""

    def __init__(
        self,
        model: str,
        key: str,
        *,
        base_url: str | None = None,
        effort: str | None = None,
        max_reply: int = REPLY_MAX_TOKENS,
        timeout: float = REQUEST_TIMEOUT_S,
        say: Callable[[str], None] | None = None,
        on_reply: Callable[[Reply], None] | None = None,
        fetch_picture: Callable[[str], tuple[str, bytes] | None] | None = None,
        exchanges_file: str | None = None,
        client: Any = None,
    ):
        if effort is not None and effort not in EFFORTS:
            raise ValueError(f"No effort '{effort}'; the levels: {', '.join(EFFORTS)}.")
        self.model = model
        self._key = key  # handed to the SDK and kept for the scans, never written
        self.base_url = base_url
        self.effort = effort
        self.max_reply = int(max_reply)
        self.timeout = float(timeout)
        self.say = say
        self.on_reply = on_reply
        self.fetch_picture = fetch_picture
        self.exchanges_file = exchanges_file
        self.offered_tools: tuple[str, ...] | None = None  # set by the door's loop
        self.failures = 0
        self.last_error: str | None = None
        self.failed: str | None = None
        self.cut_off: str | None = None
        self.finish = ""
        self.identity_name = ""  # the model's name as the server reports it
        self.context: int | None = None  # the context the server gives it, when it says
        self.usage = Usage()
        self.exchanges: list[dict[str, Any]] = []  # bodies, never headers
        self._sent: dict[str, list[dict[str, Any]]] = {}  # a reply's content as the API gave it
        if client is None:
            import anthropic

            client = anthropic.Anthropic(
                api_key=key,
                base_url=base_url,
                timeout=self.timeout,
                max_retries=2,
                # the SDK's headers that describe the owner's machine, left out: nothing of
                # his goes with a request but the key (the request's own particulars stay)
                default_headers={name: anthropic.omit for name in PLATFORM_HEADERS},
            )
        self.client = client

    # -- the identity --------------------------------------------------------------------

    def identity(self) -> str:
        """The model's name as the server reports it (the Models API), and the context it
        gives, read once before stationing. Raises `local.DoorError` in words."""
        anthropic = _sdk()
        try:
            info = self.client.models.retrieve(self.model)
        except anthropic.AuthenticationError:
            raise local.DoorError(
                "The API refused the key (401). Check it, or put the right one in the "
                "credential store with --store-key."
            ) from None
        except anthropic.NotFoundError:
            raise local.DoorError(
                f"The API knows no model '{self.model}' (404); --model names it exactly."
            ) from None
        except anthropic.APIConnectionError as e:
            raise local.DoorError(f"Could not reach the API: {type(e).__name__}.") from None
        except anthropic.APIStatusError as e:
            raise local.DoorError(
                f"The API answered {e.status_code} when asked for the model: {_said(e)}"
            ) from None
        name = str(getattr(info, "id", "") or "").strip()
        if not name:
            raise local.DoorError("The API did not say which model answers to that name.")
        self.identity_name = name
        ctx = getattr(info, "max_input_tokens", None)
        self.context = int(ctx) if isinstance(ctx, int) and ctx > 0 else None
        return name

    def server_words(self) -> str:
        where = "a base URL of the owner's" if self.base_url else "the API's own address"
        return f"the Anthropic Messages API, at {where}"

    def context_size(self) -> int | None:
        return self.context

    # -- the request ---------------------------------------------------------------------

    def tools_schema(self) -> list[dict[str, Any]]:
        names = self.offered_tools if self.offered_tools is not None else tool_names()
        return [
            {
                "name": n,
                "description": TOOLS[n].description,
                "input_schema": parameters_schema(n),
            }
            for n in names
            if n in TOOLS
        ]

    def messages(self, turns: Sequence[Turn], notice: str = "") -> tuple[str, list[dict]]:
        """The system prompt and the messages, from the latest operator turn on."""
        start = 0
        for i, t in enumerate(turns):
            if t.role == OPERATOR:
                start = i
        system = ""
        out: list[dict[str, Any]] = []
        ids: list[str] = []
        calls: tuple[ToolCall, ...] = ()

        def user(*blocks: dict[str, Any]) -> None:
            if out and out[-1]["role"] == "user":
                out[-1]["content"].extend(blocks)
            else:
                out.append({"role": "user", "content": list(blocks)})

        def answer_the_ids() -> None:
            # a turn that ended on a stand-by has no results; every call is answered
            nonlocal ids
            for cid, c in zip(ids, calls, strict=False):
                words = (
                    f"Standing by: this ended your turn ({TURN_ENDS_WORDS[0].lower()}"
                    f"{TURN_ENDS_WORDS[1:-1]}), and what follows is the sample that ended "
                    "the stand-by."
                    if c.name == "stand_by"
                    else "Not run: a stand-by earlier in the reply ended your turn."
                )
                user({"type": "tool_result", "tool_use_id": cid, "content": words})
            ids = []

        for i, t in enumerate(turns[start:], start):
            if t.role == OPERATOR:
                answer_the_ids()
                system = str(t.content)
                continue
            if t.role == MODEL:
                answer_the_ids()
                r: Reply = t.content
                blocks = self._content_of(r, i)
                calls = r.calls
                ids = [b["id"] for b in blocks if b["type"] == "tool_use"]
                if not out or out[-1]["role"] != "user":
                    # the API's turns alternate from a user's (a model turn after the brief
                    # alone: the brief sent again over an open turn)
                    user({"type": "text", "text": "(Your turn.)"})
                out.append({"role": "assistant", "content": blocks})
                continue
            d = t.content
            if "tool_results" in d:
                results = list(d["tool_results"])
                for k, cid in enumerate(ids):
                    res = results[k] if k < len(results) else None
                    user(self._result_block(cid, res))
                ids = []
                continue
            answer_the_ids()
            words = conversation_text(d)
            if words is not None:
                user({"type": "text", "text": words or "(nothing said)"})
            else:
                user({"type": "text", "text": json.dumps(d, ensure_ascii=False)})
        answer_the_ids()
        if notice:
            user({"type": "text", "text": notice})
        if not out:
            user({"type": "text", "text": "(Your turn.)"})
        return system, out

    def _content_of(self, r: Reply, at: int) -> list[dict[str, Any]]:
        """The assistant turn as the API gave it, where the door has it; else built from
        the reply, with ids of the door's own making."""
        kept = self._sent.get(_key_of(r))
        if kept is not None:
            return [dict(b) for b in kept]
        blocks: list[dict[str, Any]] = []
        if r.text:
            blocks.append({"type": "text", "text": r.text})
        for k, c in enumerate(r.calls):
            blocks.append(
                {"type": "tool_use", "id": f"toolu_fs_{at}_{k}", "name": c.name, "input": c.args}
            )
        if not blocks:
            blocks.append({"type": "text", "text": "(no words)"})
        return blocks

    def _result_block(self, cid: str, res: dict[str, Any] | None) -> dict[str, Any]:
        if res is None:
            return {
                "type": "tool_result",
                "tool_use_id": cid,
                "content": "Not run: this turn's budget for it was spent.",
            }
        value = res.get("result")
        if isinstance(value, dict) and isinstance(value.get("picture"), dict):
            return {"type": "tool_result", "tool_use_id": cid, "content": self._picture(value)}
        text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        return {"type": "tool_result", "tool_use_id": cid, "content": text or "(empty)"}

    def _picture(self, value: dict[str, Any]) -> list[dict[str, Any]]:
        """A picture's tool result (package 42, item 4): the image block, fetched from the
        game by its id, and its words; the words alone when it cannot be had."""
        pic = value["picture"]
        words = str(value.get("words") or pic.get("words") or "")
        got = None
        if self.fetch_picture is not None and pic.get("id"):
            try:
                got = self.fetch_picture(str(pic["id"]))
            except Exception:  # noqa: BLE001  (a game gone, a picture dropped)
                got = None
        if got is None:
            return [{"type": "text", "text": f"{words} {PICTURE_GONE}".strip()}]
        media, data = got
        image = {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media,
                "data": base64.standard_b64encode(data).decode("ascii"),
            },
        }
        return [image, {"type": "text", "text": words or "The picture."}]

    def request(self, turns: Sequence[Turn], notice: str = "") -> dict[str, Any]:
        """The request's body as the SDK takes it (`messages.stream`'s arguments)."""
        system, messages = self.messages(turns, notice)
        body: dict[str, Any] = {
            "model": self.identity_name or self.model,
            "max_tokens": self.max_reply,
            "messages": messages,
            # the conversation cached up to its last block: what was sent last turn, the
            # library read in it among it, is read from the cache this turn
            "cache_control": {"type": "ephemeral"},
            "thinking": {
                "type": "adaptive",
                "block_binding": {"prefix_mismatch_behavior": "drop_block"},
            },
            "betas": [THINKING_BINDING_BETA],
        }
        if system:
            # the tools and the brief, the same every turn of a seating, cached
            body["system"] = [
                {"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}
            ]
        tools = self.tools_schema()
        if tools:
            body["tools"] = tools
        if self.effort:
            body["output_config"] = {"effort": self.effort}
        return body

    # -- the reply -----------------------------------------------------------------------

    def _tell(self, words: str) -> None:
        if self.say is not None:
            self.say(scrub(words.strip(), self._key))

    def _failure(self, words: str, final: bool = False) -> None:
        self.failures += 1
        self.last_error = words
        if final or self.failures >= FAILURES_TO_STAND_DOWN:
            self.failed = words if final else f"{words} ({self.failures} failed requests in a row)"

    def _keep(self, body: dict[str, Any], reply: dict[str, Any] | None) -> None:
        """An exchange kept: the request's body and the reply's, never a header; written to
        the owner's file when one is named, scanned for the key first."""
        entry = {"request": body, "reply": reply}
        self.exchanges.append(entry)
        del self.exchanges[:-EXCHANGES_KEPT]  # the latest in memory; the file has them all
        if self.exchanges_file:
            line = scrub(json.dumps(entry, ensure_ascii=False, default=str), self._key)
            with open(self.exchanges_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        if self.failed is not None:
            return None
        anthropic = _sdk()
        self.cut_off = None
        notice = ""
        first_cut = ""
        while True:
            body = self.request(turns, notice)
            try:
                with self.client.beta.messages.stream(**body) as stream:
                    message = stream.get_final_message()
            except anthropic.APITimeoutError:
                self._failure(
                    f"The API did not answer within {self.timeout:g} s; the sample is left open."
                )
                self._keep(body, None)
                return None
            except anthropic.APIConnectionError as e:
                self._failure(f"Could not reach the API ({type(e).__name__}).")
                self._keep(body, None)
                return None
            except anthropic.AuthenticationError:
                self._failure("The API refused the key (401).", final=True)
                return None
            except (anthropic.PermissionDeniedError, anthropic.NotFoundError) as e:
                self._failure(f"The API answered {e.status_code}: {_said(e)}", final=True)
                return None
            except anthropic.RateLimitError as e:
                self._failure(f"The API's rate limit was reached (429): {_said(e)}")
                return None
            except anthropic.BadRequestError as e:
                self._failure(f"The API refused the request (400): {_said(e)}", final=True)
                self._keep(body, None)
                return None
            except anthropic.APIStatusError as e:
                self._failure(f"The API answered {e.status_code}: {_said(e)}")
                return None
            self.failures = 0
            self.last_error = None
            got = message.to_dict()
            self._keep(body, got)
            counted = self.usage.add(message.usage)
            reported = str(getattr(message, "model", "") or "")
            if self.identity_name and reported and reported != self.identity_name:
                self._failure(
                    f"The API answered with another model ({reported}) than the one seated "
                    f"({self.identity_name}); its reply is not passed on, since consent is "
                    "per model.",
                    final=True,
                )
                return None
            self.finish = str(message.stop_reason or "")
            if self.finish == "refusal":
                details = getattr(message, "stop_details", None)
                category = getattr(details, "category", None) if details is not None else None
                self.cut_off = (
                    "the API's safeguards declined the reply"
                    + (f" (the category the server gave: {category})" if category else "")
                    + "; the turn ended with nothing done, and it is not asked again"
                )
                self._tell(f"{self.cut_off[0].upper()}{self.cut_off[1:]}.")
                return Reply()
            reply = self.parse(message)
            served = {
                "prompt": counted["uncached"] + counted["cache_read"] + counted["cache_written"],
                "reply": counted["out"],
            }
            why = self._no_reply(reply)
            if why is None:
                blocks = [b for b in (_block_param(x) for x in message.content) if b]
                self._sent[_key_of(reply)] = blocks
                reply = Reply(reply.text, reply.calls, reply.raw, served)
                if self.on_reply is not None:
                    self.on_reply(reply)
                if any(c.name in ("hand_over", "handover_note", "stand_down") for c in reply.calls):
                    self._tell(self.usage.words("to this handover"))
                return reply
            if not first_cut:
                first_cut = why
                notice = CUT_WORDS.format(limit=self.max_reply) if why == "cut" else EMPTY_WORDS
                self._tell(f"{self._cut_words(why)}; it is asked once more, with the reason.")
                continue
            self.cut_off = (
                f"{self._cut_words(first_cut)}, and {self._cut_words(why, again=True)} when "
                "asked once more; the turn ended with nothing done"
            )
            self._tell(f"{self.cut_off}, and the station's journal says so.")
            return Reply()

    def parse(self, message: Any) -> Reply:
        """The API's reply as a `Reply`: the text blocks as its words, the tool calls with
        their arguments, `raw` the words and then the calls as given, so that the token
        scan reads everything the model said (its thinking is not scanned: thinking about
        the token does not use it, as at the local runner)."""
        texts: list[str] = []
        calls: list[ToolCall] = []
        served: list[dict[str, Any]] = []
        for b in message.content:
            kind = getattr(b, "type", None)
            if kind == "text":
                texts.append(str(b.text or ""))
            elif kind == "tool_use":
                args = b.input if isinstance(b.input, dict) else {}
                calls.append(ToolCall(str(b.name), dict(args)))
                served.append({"name": str(b.name), "arguments": args})
        text = "\n".join(t for t in texts if t)
        raw = text
        if served:
            raw += ("\n" if raw else "") + json.dumps(served, ensure_ascii=False)
        return Reply(text=text.strip(), calls=tuple(calls), raw=raw)

    def _no_reply(self, reply: Reply) -> str | None:
        """ "cut" when the reply was cut at the limit with a call in it (whose arguments may
        be short) or no words; "empty" when it has neither words nor a call; None to pass
        it on (a reply cut at the limit with words and no call is a reply)."""
        if self.finish == "max_tokens" and (reply.calls or not reply.text):
            return "cut"
        if not reply.text and not reply.calls:
            return "empty"
        return None

    def _cut_words(self, why: str, again: bool = False) -> str:
        if why == "cut":
            if again:
                return "was cut off again"
            return f"The model's reply was cut off at the reply limit ({self.max_reply:,} tokens)"
        if again:
            return "came empty again"
        return "The model's reply came with no words and no call"

    def close(self) -> None:
        close = getattr(self.client, "close", None)
        if callable(close):
            close()


def _sdk() -> Any:
    import anthropic

    return anthropic


def _said(e: Any) -> str:
    """An API error's own words, short."""
    words = getattr(e, "message", None) or str(e)
    return " ".join(str(words).split())[:300]


# ---------------------------------------------------------------------------
# The OpenRouter dialect (decision 31)
# ---------------------------------------------------------------------------

OPENROUTER_BASE = "https://openrouter.ai/api"


class OpenRouterModel(local.LocalModel):
    """The OpenRouter dialect: the local runner's chat-completions on OpenRouter's base
    URL, the key in the request's header (set on the HTTP client, never in a body), the
    identity the `--model` name as the models list has it, and a reply the server says
    another model wrote not passed on."""

    def __init__(self, endpoint: str, key: str, **kw: Any):
        super().__init__(endpoint, **kw)
        self._key = key
        self.client.headers["Authorization"] = "Bear" + "er " + key

    def server_words(self) -> str:
        return f"OpenRouter's chat completions at {self.base}"

    def identity(self) -> str:
        """The `--model` name as OpenRouter's models list has it, whole (a vendor's name
        and the model's, with the slash between: not a file's path)."""
        r = self._get("/v1/models")
        if r.status_code == 401:
            raise local.DoorError("OpenRouter refused the key (401).")
        if r.status_code != 200:
            raise local.DoorError(f"OpenRouter's models list answered {r.status_code}.")
        try:
            ids = {str(m.get("id", "")) for m in r.json().get("data") or []}
        except (ValueError, AttributeError):
            ids = set()
        if self.model not in ids:
            raise local.DoorError(f"OpenRouter lists no model '{self.model}'.")
        self._served_name = self.model
        return self.model

    def _read(self, r: Any) -> Any:  # type: ignore[override]
        got = local.LocalModel._read(r)
        try:
            reported = str(r.json().get("model") or "")
        except (ValueError, AttributeError):
            reported = ""
        if got is not None and reported and self.model and reported != self.model:
            self.failed = (
                f"OpenRouter answered with another model ({reported}) than the one seated "
                f"({self.model}); its reply is not passed on, since consent is per model."
            )
            return None
        return got


# ---------------------------------------------------------------------------
# The command
# ---------------------------------------------------------------------------


def main(
    argv: list[str] | None = None,
    *,
    inp: Any = None,
    out: Any = None,
    game_transport: Any = None,
    game_http: Any = None,
    poll_wait: float = local.POLL_WAIT_S,
    environ: Mapping[str, str] | None = None,
    client: Any = None,
    transport: Any = None,
    prompt: Callable[[str], str] = getpass.getpass,
) -> int:
    """The door's command. `client` stands for the SDK's client (tests: none; the door
    makes the SDK's own against `--base-url`, the tests' local server); `transport` is the
    OpenRouter dialect's HTTP transport for a test."""
    inp = inp or sys.stdin
    out = out or sys.stdout
    ap = argparse.ArgumentParser(description="FreeSail: the API door, a client of the game")
    ap.add_argument("--game", default=local.DEFAULT_GAME, help="the running game's address")
    ap.add_argument(
        "--model",
        default="",
        help="the model's name as the API knows it (no default: the owner's choice)",
    )
    ap.add_argument("--dialect", choices=("anthropic", "openrouter"), default="anthropic")
    ap.add_argument("--base-url", default=None, help="the API's address (a proxy, a test server)")
    ap.add_argument("--key-file", default=None, help="a file holding the key, outside the game")
    ap.add_argument("--store-key", action="store_true", help="put the key in the credential store")
    ap.add_argument("--effort", choices=EFFORTS, default=None, help="the model's effort")
    ap.add_argument("--max-reply", type=int, default=REPLY_MAX_TOKENS)
    ap.add_argument("--request-timeout", type=float, default=REQUEST_TIMEOUT_S)
    ap.add_argument("--ctx", type=int, default=None, help="the context (OpenRouter's dialect)")
    ap.add_argument("--station", default="watcher", choices=["watcher", "officer", "captain"])
    ap.add_argument("--session", choices=("play", "test"), default="play")
    ap.add_argument("--ask-again", action="store_true")
    ap.add_argument("--handover-reserve", type=local.reserve_form, action="append")
    ap.add_argument("--exchanges", default=None, help="a file the request and reply bodies go to")
    args = ap.parse_args(argv)
    openrouter = args.dialect == "openrouter"
    account = OPENROUTER_ACCOUNT if openrouter else KEYRING_ACCOUNT
    if args.store_key:
        return store_key(account=account, prompt=prompt, out=out)
    if not args.model:
        print(
            "Name the model with --model, exactly as the API knows it: the door has no "
            "default, and the consent record is kept under the name the API reports.",
            file=out,
        )
        return local.EXIT_UNREACHABLE
    environ = os.environ if environ is None else environ
    try:
        key, where = read_key(
            account=account,
            env_names=OPENROUTER_KEY_ENV if openrouter else KEY_ENV,
            key_file=args.key_file,
            environ=environ,
        )
    except KeyError_ as e:
        print(str(e), file=out, flush=True)
        return local.EXIT_UNREACHABLE
    why = refusal_to_start(
        key,
        key_file=args.key_file,
        sent=(args.model, args.game, args.exchanges or ""),
        base_url=args.base_url,
        environ=environ,
    )
    if args.exchanges and _inside(Path(args.exchanges).expanduser(), ROOT):
        why = why or (
            f"The exchanges file {args.exchanges} is inside the repository; name one outside it."
        )
    if why:
        print(f"The API door does not start: {why}", file=out, flush=True)
        return local.EXIT_UNREACHABLE
    print(f"The key is read from {where}; it is sent in the request's header only.", file=out)
    game = GameClient(args.game, args.station, transport=game_transport, http=game_http)

    def fetch(pid: str) -> tuple[str, bytes] | None:
        return game.picture(pid)

    def show(words: str) -> None:
        print(scrub(words, key), file=out, flush=True)

    if openrouter:
        model: Any = OpenRouterModel(
            args.base_url or OPENROUTER_BASE,
            key,
            model=args.model,
            ctx_size=args.ctx,
            transport=transport,
            on_reply=local.echo_reply(out),
            max_reply=args.max_reply,
            timeout=args.request_timeout,
            say=show,
        )
    else:
        model = ApiModel(
            args.model,
            key,
            base_url=args.base_url,
            effort=args.effort,
            max_reply=args.max_reply,
            timeout=args.request_timeout,
            say=show,
            on_reply=local.echo_reply(out),
            fetch_picture=fetch,
            exchanges_file=args.exchanges,
            client=client,
        )
    try:
        identity = model.identity()
        server = model.server_words()
        print(f"The API serves {identity}.", file=out, flush=True)
        if openrouter:
            runtime = f"FreeSail's game at {args.game}, through {DOOR_WORDS}, {server}"
            print(model.check_context(identity, runtime, args.station), file=out, flush=True)
    except local.DoorError as e:
        show(str(e))
        return local.EXIT_UNREACHABLE
    if key in identity:
        show("The API door does not start: the model's name the API gave holds the key.")
        return local.EXIT_UNREACHABLE
    context = model.context_size()
    reserve = local.handover_reserve_tokens(args.handover_reserve, context)
    if context and station_name(args.station) in (OFFICER, CAPTAIN):
        show(local.handover_words(args.handover_reserve, context, reserve))
    try:
        first = game.station(
            identity,
            "api",
            door_note=API_NOTE,
            session_kind=args.session,
            client=server,
            ask_again=args.ask_again,
            context_tokens=context,
            handover_reserve=reserve,
        )
    except GameError as e:
        show(e.words)
        return local.EXIT_NO_CONSENT if e.status == 403 else local.EXIT_UNREACHABLE
    show(first.get("words") or f"The {args.station} is stationed.")
    try:
        code = local.run(game, model, first, inp=inp, out=out, poll_wait=poll_wait)
    finally:
        usage = getattr(model, "usage", None)
        if usage is not None:
            show(usage.words("in all"))
        model.close()
    return code


if __name__ == "__main__":
    sys.exit(main())
