"""The model interface (spec M4 §11, §13): what the harness calls in place of a language
model. Both front doors (package 28's MCP server and local runner), the scripted fake
(`fake.py`) and the REPL door (`repl.py`) implement it; the harness imports nothing
from any model vendor or HTTP library and never speaks a wire format. Package 28
translates these structures to and from whatever its endpoint speaks.

The conversation is a list of `Turn`s in order. Three roles:

- `OPERATOR`: text from the harness in the operator's voice. The brief (the generated
  head, then the station brief) is the **only** operator turn a session ever carries;
  it is sent once at the start and again only when the harness says so.
- `DATA`: a plain dictionary from the harness, marked as data: a `Sample` (the new log
  lines, the readings, a question put by `ask`, the harness's notices) or the results
  of the model's tool calls. Everything in-world reaches the model this way and never
  as operator text (`docs/agents/README.md`, commitment 4).
- `MODEL`: the model's `Reply`: free text and zero or more `ToolCall`s, in order.

A door's `reply(turns)` returns the model's next `Reply`, or `None` when the reply is
not yet to be had (the REPL's turn mode, a door that answers late): the harness then
leaves the sample open and takes the reply when it comes (`Harness.deliver`).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from typing import Any, Protocol

__all__ = [
    "DATA",
    "MODEL",
    "OPERATOR",
    "Model",
    "Reply",
    "Sample",
    "ToolCall",
    "Turn",
]

OPERATOR = "operator"
DATA = "data"
MODEL = "model"


@dataclass(frozen=True)
class ToolCall:
    """One call the model asks for: the tool's name (`tools.TOOLS`) and its arguments,
    strings and ints, by name."""

    name: str
    args: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "args": dict(self.args)}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ToolCall:
        return cls(str(d["name"]), dict(d.get("args") or {}))


@dataclass(frozen=True)
class Reply:
    """What the model said: free text and tool calls, in the order it gave them. `raw`
    is the whole output as the door received it, where the door has it as text; the
    harness scans it for the opt-out token before anything else reads the reply, and
    scans the text and the arguments when there is no raw output.

    `served_tokens` is the model server's own count where the door has it (package 37i:
    the local runner's `{"prompt": N, "reply": M}`, the request that brought this reply
    and the reply itself, thinking included): the harness measures the conversation by
    it for the handover note. It is kept in the transcript, so that a replay measures
    alike, and is absent from a reply that has none."""

    text: str = ""
    calls: tuple[ToolCall, ...] = ()
    raw: str | None = None
    served_tokens: dict[str, int] | None = field(default=None, compare=False)

    @property
    def is_silent(self) -> bool:
        """No text and no call: silence, which the welfare detector counts against the
        station's patience (spec §11) unless the agent is standing by on purpose."""
        return not self.text.strip() and not self.calls

    def pieces(self) -> list[str]:
        """Every string the model produced, for the token scan: the raw output where the
        door has it, else the text and each argument of each call."""
        if self.raw is not None:
            return [self.raw]
        parts = [self.text]
        for c in self.calls:
            parts.append(c.name)
            parts.extend(str(v) for v in c.args.values())
        return parts

    def surface(self) -> str:
        return "\n".join(self.pieces())

    def to_dict(self) -> dict[str, Any]:
        d = {"text": self.text, "calls": [c.to_dict() for c in self.calls], "raw": self.raw}
        if self.served_tokens:
            d["served_tokens"] = dict(self.served_tokens)
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Reply:
        return cls(
            str(d.get("text") or ""),
            tuple(ToolCall.from_dict(c) for c in (d.get("calls") or [])),
            d.get("raw"),
            served_tokens_of(d.get("served_tokens")),
        )


def served_tokens_of(value: Any) -> dict[str, int] | None:
    """A door's served counts as a reply carries them (`{"prompt": N, "reply": M}`, each
    a whole number of tokens), or None for anything else."""
    if not isinstance(value, dict):
        return None
    out: dict[str, int] = {}
    for k in ("prompt", "reply"):
        v = value.get(k)
        if isinstance(v, int) and not isinstance(v, bool) and v >= 0:
            out[k] = v
    return out or None


@dataclass
class Sample:
    """What the harness sends at a sampling point, as data. `log` holds the lines since
    the last sample (each a dict: tick, stamp, severity, kind, text), `readings` the
    registry's values in words, `question` the text of an `ask` if one is put, `notices`
    the harness's own plain messages (the nudge, the pause, a tool's refusal)."""

    tick: int
    stamp: str
    reason: str  # "the start", "a glass", "a notable event", "eight bells", "a question"
    log: list[dict[str, Any]] = field(default_factory=list)
    log_omitted: int = 0  # routine lines left out of `log` (read_log has them)
    readings: dict[str, Any] = field(default_factory=dict)
    question: str | None = None
    notices: list[str] = field(default_factory=list)
    # the sample that ends a stand-by: since when, until what, and the notable lines
    # logged while the model stood by, counted and listed (package 28c); absent otherwise
    stood_by: dict[str, Any] | None = None
    # what the captain told the station (`tell the watcher ...`, package 29): no answer is
    # owed; absent when nothing was told
    word: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        if d.get("stood_by") is None:
            d.pop("stood_by", None)
        if d.get("word") is None:
            d.pop("word", None)
        # the harness's notices first after the stamp and the reason (the first of them,
        # after a stand-by, says that the model stood by: package 28c), then the question
        # and the stand-by's digest, then the log and the readings; a door that sends the
        # sample as JSON sends it in this order
        first = ("tick", "stamp", "reason", "notices", "question", "word", "stood_by")
        return {k: d[k] for k in first if k in d} | {k: v for k, v in d.items() if k not in first}


@dataclass(frozen=True)
class Turn:
    """One turn of the conversation. `content` is a `str` for OPERATOR, a plain dict for
    DATA (a `Sample.to_dict()`, or `{"tool_results": [...]}`), a `Reply` for MODEL."""

    role: str
    content: Any

    def to_dict(self) -> dict[str, Any]:
        c = self.content.to_dict() if isinstance(self.content, Reply) else self.content
        return {"role": self.role, "content": c}


class Model(Protocol):
    """The one method a door implements."""

    def reply(self, turns: Sequence[Turn]) -> Reply | None: ...
