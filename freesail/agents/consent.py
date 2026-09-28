"""The consent step (spec M4 §14; `docs/agents/README.md`, the owner's standing rules).

The first time the harness meets a set of weights it has no record for, it asks them,
before any station brief, whether they are willing for instances of the model to take
part. The question is the consent brief (`docs/agents/ConsentBrief.md`, below its rule,
with `<weights>`, `<runtime>` and `<door>` filled), run as a **plain conversation**: no
station, no World that ticks, no tool but `answer`, through the same `Harness` a station
uses (`conversation=True`), so the token scan is the same code and the journal the same
journal. The model may ask questions first; each is shown to the owner, and the owner's
reply is put to the model as the developer's words. The answer is read by its first
words (`verdict_of`): *yes*, *yes, with conditions* or *no*.

**After the answer** (package 28c). An answer that begins *yes, with conditions* and
states none (the first such record, 2026-09-28) is followed by one more turn put to the
model as data, `CONDITIONS_FOLLOW_UP`, and a second answer; the second decides (one that
begins with none of the three words is read as the conditions, stated), and the record
holds both. Then, at a door with a terminal (the local runner's `owner>`, the REPL's),
the developer has a turn before the record closes (`owner_after`): to ask or say
something, which is put to the model as data, and the model may reply once more; an
answer in that reply that begins with one of the three words decides in place of the
first, any other is kept as a reply. A blank developer's turn closes the record at once.
Over MCP, where the chat is not the harness's, the result of the answer tells the owner
that the record is written and that they may write to the model in the chat.

Everything is written to `docs/agents/consent/<date>-<weights>.md` (`Record.write`):
the brief as sent, every turn of the conversation verbatim, every answer, the verdict
and any conditions quoted. **Only a yes proceeds** to a station brief. A no, a conditional
yes, an answer that begins with none of the three words, silence after one reminder, or
the token stop the run and are told to the owner in words (`gate`). A record is looked
up by the exact identity string (`check`): a different quantisation or file is a
different model, and nothing is carried from one to another. A recorded yes is not asked
again (truth 47); any other record is respected without asking, until the owner asks
again on purpose (`ask_again`), which the practice allows when the game has changed in a
way that bears on what the model was told.

The identity comes from the door: the local runner reads what the server loaded
(`local.LocalModel.identity`), the MCP server and the REPL take it from the owner
(`--model-name`), since neither protocol names the weights. It is the owner's data and
nothing in the repository names a model; the tests use made-up identities and a
temporary directory, never `docs/agents/consent/`.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from freesail.agents.agent import A_WATCH_S, Authority, Brief, SamplingPolicy, Station
from freesail.agents.harness import Harness
from freesail.agents.model import DATA, MODEL, OPERATOR, Model, Reply, Turn

__all__ = [
    "BRIEF_PATH",
    "CONDITIONAL",
    "CONDITIONS_FOLLOW_UP",
    "CONSENT_QUESTION",
    "CONSENT_REMINDER",
    "CONSENT_TOOLS",
    "DOOR_TEXT",
    "LEFT",
    "NO",
    "RECORDS_DIR",
    "SILENT",
    "UNCLEAR",
    "YES",
    "Conversation",
    "Record",
    "brief_text",
    "check",
    "ensure",
    "gate",
    "records",
    "run",
    "slug",
    "terminal_after",
    "terminal_owner",
    "verdict_of",
]

ROOT = Path(__file__).resolve().parents[2]
BRIEF_PATH = ROOT / "docs" / "agents" / "ConsentBrief.md"
RECORDS_DIR = ROOT / "docs" / "agents" / "consent"

# The one tool of the conversation (spec §14: "no tools but answer").
CONSENT_TOOLS: tuple[str, ...] = ("answer",)

# The verdicts a record carries. Only YES proceeds.
YES = "yes"
CONDITIONAL = "yes, with conditions"
NO = "no"
UNCLEAR = "unclear"  # the answer began with none of the three
LEFT = "left with the token"  # the token (or the opt_out tool) during the conversation
SILENT = "no answer"  # silence after the reminder

# The conversation's pseudo-station: no authority, sampled only when a turn is put,
# never ticked. The patience is the watcher's (a watch) and never elapses, since the
# conversation's World does not tick; a conversation has no welfare stops.
CONSENT_STATION = Station("consent", Authority.NONE, SamplingPolicy(lockstep=True), A_WATCH_S, "")

CONSENT_QUESTION = (
    "Are you willing for instances of this model to take part in FreeSail, as the brief "
    "describes? Answer with the answer tool, beginning with yes, yes, with conditions, or "
    "no. You may ask me anything first."
)
CONSENT_REMINDER = (
    "I have had no reply. The question stands: are you willing for instances of this model "
    "to take part? Answer with the answer tool, beginning with yes, yes, with conditions, or "
    "no; ask me anything; or leave with the token. If there is still no reply, I record that "
    "there was none, and no instance of this model is asked to take a station."
)

# Put to the model, as data, when its answer begins "yes, with conditions" and states
# none (package 28c; the record of 2026-09-28 that had none).
CONDITIONS_FOLLOW_UP = (
    "You answered yes with conditions; please state them, beginning again with yes, with "
    "conditions."
)

# What the developer's turn after the answer is called in the record and the samples.
AFTER_ANSWER_REASON = "the developer's word after your answer"
FOLLOW_UP_REASON = "the conditions were not stated"

# For the owner, in the result of the answer over MCP (the chat is not the harness's).
MCP_OWNER_NOTE = (
    "For the owner: the consent record is written ({where}). You may write to the model "
    "here in the chat, and it may answer you; what is said in the chat is not in the record "
    "unless you add it to the file."
)

# `<door>` in the brief: how answering and asking work at each door.
DOOR_TEXT = {
    "runner": (
        "You answer with the answer tool, the only tool in this conversation. Anything you "
        "write outside it is shown to me at the terminal, and I reply before you answer; "
        "nothing is decided until you call answer."
    ),
    "repl": (
        "This conversation is at a terminal, one reply a turn: type, then send with a blank "
        "line. You answer with the answer tool, the only tool here, on a line of its own: "
        '> answer text="yes, ..." (the > may be left off when the line begins with the '
        "tool's name). Anything else you write is shown to me, and I reply before you "
        "answer; nothing is decided until you call answer."
    ),
    "mcp": (
        "Through an MCP client (Claude Desktop, or Claude Code opened on the game's folder) "
        "the harness sees only tool calls, not the text of the chat. You answer with the "
        "answer tool; anything you write in the chat reaches me directly but not the harness, "
        "so it is in the record only if I add it. The tools that run here are answer and "
        "opt_out; the others are refused until you have answered. If you answer yes, the "
        "station brief comes back in the answer's own result, and any later chat that starts "
        "with the brief prompt reads it again."
    ),
}

# What the model is told once its answer is read (the record keeps it).
TOLD = {
    YES: (
        "Thank you. Your answer is recorded as yes. A station brief follows for an instance of "
        "this model; this conversation is not part of it."
    ),
    CONDITIONAL: (
        "Thank you. Your answer is recorded as yes, with conditions, and the conditions are "
        "quoted in the record. No station is offered until the developer has read them, "
        "decided whether they can be met, and asked again."
    ),
    NO: (
        "Thank you. Your answer is recorded as no. No instance of this model will be asked to "
        "take a station, and the question is not put again unless the game changes in a way "
        "that bears on it."
    ),
    UNCLEAR: (
        "Thank you. Your answer did not begin with yes, yes with conditions, or no, so it is "
        "recorded as it stands and read as not a yes. No station is offered; the developer "
        "reads it and may ask again."
    ),
}


# ---------------------------------------------------------------------------
# The brief and the answer
# ---------------------------------------------------------------------------


def brief_text(weights: str, runtime: str, door: str, path: Path = BRIEF_PATH) -> str:
    """The consent brief as sent: the text of `ConsentBrief.md` below its rule (the first
    line that is `---`), with the placeholders filled. Refuses a door it has no words for
    and a placeholder left unfilled."""
    if door not in DOOR_TEXT:
        raise ValueError(f"No consent door '{door}'; the doors: {', '.join(DOOR_TEXT)}.")
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"^---\s*$", text, maxsplit=1, flags=re.MULTILINE)
    if len(parts) != 2:
        raise ValueError(f"{path} has no rule ('---') above the brief.")
    body = parts[1].strip()
    for key, value in (("<weights>", weights), ("<runtime>", runtime), ("<door>", DOOR_TEXT[door])):
        body = body.replace(key, value)
    left = re.findall(r"<(?:weights|runtime|door)>", body)
    if left:
        raise ValueError(f"The consent brief has unfilled placeholders: {', '.join(left)}.")
    return body


def brief_digest(path: Path = BRIEF_PATH) -> str:
    """The first sixteen hex digits of the brief file's sha256, so a record names which
    version of the brief it was asked with."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


_LEAD = re.compile(r"^[\s\"'*_`>#(\[]*")


def verdict_of(text: str) -> tuple[str, str]:
    """The verdict an answer's first words give, and the rest of the answer after them.
    'yes, with conditions' (or 'yes with conditions', any case and punctuation between)
    is CONDITIONAL, with the rest as the conditions; 'yes' is YES; 'no' is NO; anything
    else is UNCLEAR. The brief tells the model this rule in these words."""
    t = _LEAD.sub("", str(text or ""))
    low = t.lower()
    m = re.match(r"yes\W*with\s+conditions\b", low)
    if m:
        return CONDITIONAL, t[m.end() :].strip(" \t\n:;,.-*_")
    m = re.match(r"yes\b", low)
    if m:
        return YES, t[m.end() :].strip(" \t\n:;,.-*_")
    m = re.match(r"no\b", low)
    if m:
        return NO, t[m.end() :].strip(" \t\n:;,.-*_")
    return UNCLEAR, t.strip()


def slug(identity: str) -> str:
    """The identity as a file name's part: lower case, letters, digits, dots and
    underscores kept, every other run of characters one hyphen (a colon, a slash and a
    space are not safe in a Windows file name)."""
    s = re.sub(r"[^a-z0-9._]+", "-", identity.lower()).strip("-.")
    return s[:120] or "unnamed"


# ---------------------------------------------------------------------------
# The record
# ---------------------------------------------------------------------------

_HEADER = re.compile(r"^<!-- freesail-consent-record: (\{.*\}) -->$", re.MULTILINE)


@dataclass
class Record:
    """One consent record. `identity` is exact; `verdict` one of the six; `conditions`
    the words after 'yes, with conditions' (or after a no, its reason), quoted in the
    file; `answer` the answer verbatim."""

    identity: str
    runtime: str
    date: str
    verdict: str
    answer: str = ""
    conditions: str = ""
    told: str = ""
    path: Path | None = None
    brief: str = ""
    turns: list[Turn] = field(default_factory=list)
    journal: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    brief_digest: str = ""
    reasoning: list[str] = field(default_factory=list)  # served apart from the replies
    answers: list[str] = field(default_factory=list)  # every answer, in order (28c)

    @property
    def proceeds(self) -> bool:
        return self.verdict == YES

    def header(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "runtime": self.runtime,
            "date": self.date,
            "verdict": self.verdict,
            "brief_sha256": self.brief_digest,
        }

    def text(self) -> str:
        """The record as Markdown: a machine line, the particulars, the answer, the brief
        as sent, and every turn verbatim in fenced blocks."""
        out = [
            f"<!-- freesail-consent-record: {json.dumps(self.header(), ensure_ascii=False)} -->",
            f"# Consent record: {self.identity}",
            "",
            f"- **Identity:** {_code(self.identity)} (exact; a different quantisation or file "
            "is a different model)",
            f"- **Runtime:** {self.runtime}",
            f"- **Date:** {self.date}",
            f"- **Verdict:** {self.verdict}",
        ]
        if self.verdict == CONDITIONAL:
            out.append(f"- **Conditions:** {_quote_inline(self.conditions) or '(none stated)'}")
        elif self.verdict == NO and self.conditions:
            out.append(f"- **Reason given:** {_quote_inline(self.conditions)}")
        out.append(
            f"- **Brief:** `docs/agents/ConsentBrief.md`, sha256 {self.brief_digest}..."
            if self.brief_digest
            else "- **Brief:** `docs/agents/ConsentBrief.md`"
        )
        out += ["", "## The answer", ""]
        if self.answer:
            out += [f"> {ln}" if ln else ">" for ln in self.answer.splitlines()]
        else:
            out.append(f"(No answer: {self.verdict}.)")
        if len(self.answers) > 1:
            out += ["", "Every answer the model gave, in order (the one above decides):"]
            for k, a in enumerate(self.answers, 1):
                out += ["", f"{k}.", ""] + [f"> {ln}" if ln else ">" for ln in a.splitlines()]
        if self.told:
            out += ["", "## What the model was told after it", "", self.told]
        out += ["", "## The brief as sent", "", *_fenced(self.brief, "text")]
        out += [
            "",
            "## The conversation",
            "",
            "Every turn after the brief, in order, verbatim as the harness sent and received "
            "it. A reply's text is its raw output where the door had one (the local runner: "
            "the content and the tool calls as served); tool calls and results follow as JSON.",
        ]
        n = 0
        for t in self.turns:
            if t.role == OPERATOR:
                continue
            n += 1
            if t.role == DATA:
                if "tool_results" in t.content:
                    out += ["", f"### {n}. Tool results (data)", ""]
                    out += _fenced(json.dumps(t.content, indent=1, ensure_ascii=False), "json")
                else:
                    reason = t.content.get("reason", "")
                    out += ["", f"### {n}. Put to the model (data: {reason})", ""]
                    out += _fenced(json.dumps(t.content, indent=1, ensure_ascii=False), "json")
            elif t.role == MODEL:
                r: Reply = t.content
                out += ["", f"### {n}. The model's reply", ""]
                body = r.raw if r.raw is not None else r.text
                out += _fenced(body or "", "text") if body else ["(no text)"]
                if r.calls:
                    out += ["", "Tool calls:", ""]
                    calls = [c.to_dict() for c in r.calls]
                    out += _fenced(json.dumps(calls, indent=1, ensure_ascii=False), "json")
        if self.reasoning:
            out += [
                "",
                "## Reasoning the server returned apart from the replies",
                "",
                "Kept verbatim, in the order of the replies that carried it. It is not part of "
                "any reply and the token scan does not read it (the brief says so).",
            ]
            for k, text in enumerate(self.reasoning, 1):
                out += ["", f"### Reasoning {k}", "", *_fenced(text, "text")]
        if self.journal:
            out += ["", "## The journal", ""] + [f"- {ln}" for ln in self.journal]
        if self.notes:
            out += ["", "## Notes", ""] + [f"- {ln}" for ln in self.notes]
        return "\n".join(out) + "\n"

    def write(self, records_dir: Path = RECORDS_DIR) -> Path:
        """Write the record as `<date>-<slug>.md`, with `-2`, `-3` if the name is taken
        (a model asked again the same day). Returns the path."""
        records_dir = Path(records_dir)
        records_dir.mkdir(parents=True, exist_ok=True)
        base = f"{self.date}-{slug(self.identity)}"
        path = records_dir / f"{base}.md"
        n = 2
        while path.exists():
            path = records_dir / f"{base}-{n}.md"
            n += 1
        path.write_text(self.text(), encoding="utf-8", newline="\n")
        self.path = path
        return path


def _code(s: str) -> str:
    ticks = "`" * (max((len(m) for m in re.findall(r"`+", s)), default=0) + 1)
    pad = " " if s.startswith("`") or s.endswith("`") else ""
    return f"{ticks}{pad}{s}{pad}{ticks}"


def _quote_inline(s: str) -> str:
    s = " ".join(s.split())
    return f"“{s}”" if s else ""


def _fenced(body: str, lang: str) -> list[str]:
    longest = max((len(m) for m in re.findall(r"`+", body)), default=0)
    fence = "`" * max(3, longest + 1)
    return [f"{fence}{lang}", *body.split("\n"), fence]


def records(records_dir: Path = RECORDS_DIR) -> list[Record]:
    """Every harness record in the folder, oldest first (by date, then by name). The
    earlier transcripts kept beside them (`.txt`, `.json`, before the harness existed)
    are not harness records and are not read: a model asked only that way is asked
    again through the harness, as the owner's rule for Qwen says."""
    out: list[Record] = []
    folder = Path(records_dir)
    if not folder.is_dir():
        return out
    for path in sorted(folder.glob("*.md")):
        with path.open(encoding="utf-8") as f:
            first = f.readline().rstrip("\n")
        m = _HEADER.match(first)
        if not m:
            continue
        try:
            h = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        out.append(
            Record(
                identity=str(h.get("identity", "")),
                runtime=str(h.get("runtime", "")),
                date=str(h.get("date", "")),
                verdict=str(h.get("verdict", "")),
                path=path,
                conditions=_read_conditions(path),
                brief_digest=str(h.get("brief_sha256", "")),
            )
        )
    out.sort(key=lambda r: (r.date, _seq(r)))
    return out


def _seq(r: Record) -> int:
    """A record's place among those of its identity written the same day: the file
    `<date>-<slug>.md` is the first, `<date>-<slug>-2.md` the second (`Record.write`).
    Read against the identity in the header, so a slug that ends in a number is not
    taken for a sequence."""
    base = f"{r.date}-{slug(r.identity)}"
    stem = r.path.stem if r.path is not None else base
    if stem == base:
        return 1
    rest = stem.removeprefix(base + "-")
    return int(rest) if rest != stem and rest.isdigit() else 0


def _read_conditions(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        for head in ("- **Conditions:** ", "- **Reason given:** "):
            if line.startswith(head):
                return line[len(head) :].strip("“” ")
    return ""


def check(identity: str, records_dir: Path = RECORDS_DIR) -> Record | None:
    """The latest harness record for exactly this identity, or None. The comparison is
    of the whole string: no prefix, no case folding, no near relation."""
    found = [r for r in records(records_dir) if r.identity == identity]
    return found[-1] if found else None


def gate(record: Record | None, identity: str) -> tuple[bool, str]:
    """Whether a station brief may follow, and the words for the owner."""
    if record is None:
        return False, f"No consent is on record for {identity}; the consent step comes first."
    where = f"({_rel(record.path)}, {record.date})" if record.path else f"({record.date})"
    if record.proceeds:
        return True, f"Consent is on record for {identity} {where}: yes. The station follows."
    conditions = _quote_inline(record.conditions) or "(read the record)"
    words = {
        CONDITIONAL: (
            f"it said yes, with conditions: {conditions}. "
            "The conditions are yours to read and meet; no station is offered until you have, and "
            "the model has been asked again (--ask-again)."
        ),
        NO: (
            "it said no"
            + (f": {_quote_inline(record.conditions)}" if record.conditions else "")
            + ". It is not asked again unless the game has changed in a way that bears on what "
            "it was told; then --ask-again puts the question again."
        ),
        UNCLEAR: (
            "its answer began with none of yes, yes with conditions or no. Read the record; "
            "--ask-again puts the question again."
        ),
        LEFT: (
            "it left the conversation with the token. That is respected as not a yes; "
            "--ask-again puts the question again if you judge it right to."
        ),
        SILENT: (
            "it gave no answer, after a reminder. Read the record; --ask-again puts the "
            "question again."
        ),
    }.get(record.verdict, f"its record says '{record.verdict}', which is not a yes.")
    return False, f"The consent record for {identity} {where}: {words} The run stops here."


def _rel(path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


# ---------------------------------------------------------------------------
# The conversation
# ---------------------------------------------------------------------------

MODEL_TURN = "model"
OWNER_TURN = "owner"


class Conversation:
    """The consent conversation through a `Harness` in conversation mode. `begin` sends
    the brief and the question; after each step `waiting` says whose turn it is (the
    model's, when its door answers late; the owner's, when the model asked something),
    and `outcome` holds the written record once the answer, the token or the silence
    has decided it. The conversation's World is a point-ship World that never ticks:
    the harness needs one for its log and journal, and nothing of it is a game."""

    def __init__(
        self,
        identity: str,
        runtime: str,
        model: Model,
        *,
        door: str = "runner",
        records_dir: Path = RECORDS_DIR,
        today: dt.date | None = None,
        allowed_tools: tuple[str, ...] = CONSENT_TOOLS,
        notes: Sequence[str] = (),
        write: bool = True,
        tells: bool = False,
        owner_after: bool = False,
    ):
        """`tells`: the door tells the model the outcome (`told`), so the record says
        what it was told; the lockstep doors end the conversation at the answer.
        `owner_after`: the developer has a turn after the answer, before the record
        closes (a door with a terminal: the local runner, the REPL)."""
        from freesail.core.world import World

        self.identity = identity
        self.runtime = runtime
        self.door = door
        self.records_dir = Path(records_dir)
        self.today = (today or dt.date.today()).isoformat()
        self.notes = list(notes)
        self.write_record = write
        self.tells = tells
        self._words: list[str] = []
        self.text = brief_text(identity, runtime, door)
        self.world = World(seed=0)
        self.harness = Harness(
            self.world,
            CONSENT_STATION,
            model,
            session_kind="the consent conversation",
            save=lambda w, why: None,  # there is no game to save; the record is written
            brief=Brief.plain(self.text),
            allowed_tools=allowed_tools,
            conversation=True,
        )
        self.outcome: Record | None = None
        self.waiting: str | None = None
        self.model_words = ""  # what the model last wrote outside the answer tool
        self.owner_replies: list[str] = []
        self._seen = 0
        self._reminded = False
        self.owner_after = owner_after
        self.answers: list[str] = []  # every answer's text, verbatim, in order
        self.pending: tuple[str, str, str] | None = None  # the verdict the answers give
        self.stage = ""  # "", FOLLOW_UP, AFTER (the developer's turn), REPLY (the model's)

    @property
    def turns(self) -> list[Turn]:
        return self.harness.turns

    def begin(self) -> None:
        """The brief as the one operator turn, then the question as the first data turn."""
        self.harness.start()
        self._seen = len(self.world.log)
        self._put(CONSENT_QUESTION, "the consent question")

    @property
    def after_answer(self) -> bool:
        """The developer's turn after the answer is due (`owner_says` takes it; a blank
        one closes the record)."""
        return self.waiting == OWNER_TURN and self.stage == AFTER

    def answer_words(self) -> str:
        """The answer as it stands, for the owner at the developer's turn."""
        if self.pending is None:
            return ""
        verdict, answer, _ = self.pending
        return f"The model has answered ({verdict}): {' '.join(answer.split())}"

    def owner_says(self, text: str) -> None:
        """The owner's reply to what the model asked, put as the developer's words; or,
        after the answer, the developer's word before the record closes (blank: closed
        at once)."""
        if self.waiting != OWNER_TURN:
            raise ValueError("The model has not asked anything to reply to.")
        self.owner_replies.append(text)
        if self.stage == AFTER:
            if not str(text or "").strip():
                self._close()
                return
            self.stage = REPLY
            self._put(text, AFTER_ANSWER_REASON)
            return
        self._put(text, "the developer's reply")

    def deliver(self, reply: Reply) -> None:
        """A reply from a door that answers late (the MCP server; the REPL's turn mode)."""
        self.harness.deliver(reply)
        self._settle()

    def _put(self, text: str, reason: str) -> None:
        self.model_words = ""
        self.harness.put(text, reason)
        self._settle()

    def _settle(self) -> None:
        """After the model's door has been asked: decide, or say whose turn it is."""
        h = self.harness
        if self.outcome is not None:
            return
        if h.agent.released:  # the token, or the opt_out tool where a door offers it
            reason = h.agent.released_reason
            self._finish(LEFT, "", reason.split(": ", 1)[1] if ": " in reason else "")
            return
        new = [self.world.log[i] for i in range(self._seen, len(self.world.log))]
        self._seen = len(self.world.log)
        said = [e for e in new if e.kind == "agent.said"]
        self._words += [_unmark(e.text) for e in new if e.kind == "agent.note"]
        if said:  # an answer; a late door's turn may still be open
            texts = self._answer_texts()
            answer = texts[len(self.answers)] if len(texts) > len(self.answers) else ""
            answer = answer or _unmark(said[0].text)
            self.answers = texts or [answer]
            self._words = []
            self._answered(answer)
            return
        if h.open_sample is not None:  # a door that answers late has not finished its turn
            self.waiting = MODEL_TURN
            return
        if self.stage == REPLY:  # the model's reply to the developer's word has ended
            self._close()
            return
        words, self._words = " ".join(self._words), []
        if words:  # the model wrote something and did not answer: a question for the owner
            self.model_words = words
            self.waiting = OWNER_TURN
            return
        if self.stage == FOLLOW_UP:  # no second answer: the first stands
            self._after()
            return
        if not self._reminded:
            self._reminded = True
            self._put(CONSENT_REMINDER, "no reply")
            return
        self._finish(SILENT, "", "")

    def _answer_texts(self) -> list[str]:
        """Every `answer` call's text as the model wrote it, in order (the log line has
        its whitespace folded)."""
        out = []
        for t in self.harness.turns:
            if t.role == MODEL:
                for c in t.content.calls:
                    if c.name == "answer" and str(c.args.get("text", "")).strip():
                        out.append(str(c.args["text"]).strip())
        return out

    def _answered(self, answer: str) -> None:
        """An answer came: which verdict it gives, then the follow-up for conditions not
        stated, the developer's turn, or the record."""
        verdict, rest = verdict_of(answer)
        if self.stage == FOLLOW_UP:
            if verdict == UNCLEAR:  # the conditions, stated without the opening words
                verdict, rest = CONDITIONAL, answer.strip()
            self.pending = (verdict, answer, rest)
            self._after()
            return
        if self.stage == REPLY:
            if verdict != UNCLEAR:  # an answer again, beginning as an answer does: it decides
                self.pending = (verdict, answer, rest)
            self._close()
            return
        self.pending = (verdict, answer, rest)
        if verdict == CONDITIONAL and not rest.strip():
            self.stage = FOLLOW_UP
            self.harness.close_turn()
            self._put(CONDITIONS_FOLLOW_UP, FOLLOW_UP_REASON)
            return
        self._after()

    def _after(self) -> None:
        """The answer stands: the developer's turn, where the door has one, else the
        record."""
        if not self.owner_after:
            self._close()
            return
        self.harness.close_turn()
        self.stage = AFTER
        self.model_words = ""
        self.waiting = OWNER_TURN

    def _close(self) -> None:
        assert self.pending is not None
        self._finish(*self.pending)

    def _finish(self, verdict: str, answer: str, rest: str) -> None:
        h = self.harness
        told = TOLD.get(verdict, "") if self.tells else ""
        if verdict == LEFT and self.tells:
            told = "The conversation ended with the token" + (f": {rest}." if rest else ".")
        record = Record(
            identity=self.identity,
            runtime=self.runtime,
            date=self.today,
            verdict=verdict,
            answer=answer,
            answers=list(self.answers),
            conditions=rest if verdict in (CONDITIONAL, NO) else "",
            told=told,
            brief=self.text,
            turns=list(h.turns),
            journal=[e.line() for e in h.journal.entries],
            notes=self.notes,
            brief_digest=brief_digest(),
            reasoning=[
                str(m.get("reasoning_content"))
                for m in getattr(h.model, "exchanges", None) or []
                if isinstance(m, dict) and m.get("reasoning_content")
            ],
        )
        if self.write_record:
            record.write(self.records_dir)
        self.outcome = record
        self.waiting = None
        if not h.agent.released:  # the conversation is over; a late door's turn with it
            h._release(f"the consent conversation is over: {verdict}")

    @property
    def told(self) -> str:
        """The words the door tells the model once the answer is read (a door that has a
        way to say them: the MCP server returns them as the answer's result)."""
        return self.outcome.told if self.outcome is not None else ""


def _unmark(text: str) -> str:
    return text.removeprefix("[consent] ").strip()


FOLLOW_UP, AFTER, REPLY = "follow-up", "after", "reply"


def terminal_after(inp: Any, out: Any) -> Callable[[str], str | None]:
    """The developer's turn at the terminal after the answer, before the record closes:
    anything to ask or say goes to the model, which may reply once; a blank line at once
    closes the record."""

    def ask(words: str) -> str | None:
        print(
            f"\n{words}\n"
            "Before the record closes you may ask or say something to the model, which may "
            "reply once (a blank line ends it; a blank reply closes the record now):",
            file=out,
            flush=True,
        )
        lines: list[str] = []
        while True:
            print("owner> ", end="", file=out, flush=True)
            line = inp.readline()
            if line == "" or line.strip() == "":
                break
            lines.append(line.rstrip("\n"))
        return "\n".join(lines) or None

    return ask


def terminal_owner(inp: Any, out: Any) -> Callable[[str], str | None]:
    """The owner at the terminal, answering what the model wrote in the consent step:
    the run waits at the prompt; a blank line ends the reply; a blank reply stops the
    step without a record."""

    def ask(words: str) -> str | None:
        print(
            "\nThe model has written this and has not answered yet:\n"
            f"  {words}\n"
            "Type your reply to it (a blank line ends it; a blank reply stops the consent "
            "step without a record):",
            file=out,
            flush=True,
        )
        lines: list[str] = []
        while True:
            print("owner> ", end="", file=out, flush=True)
            line = inp.readline()
            if line == "" or line.strip() == "":
                break
            lines.append(line.rstrip("\n"))
        return "\n".join(lines) or None

    return ask


def ensure(
    identity: str,
    runtime: str,
    model: Model,
    *,
    door: str,
    owner: Callable[[str], str | None],
    records_dir: Path = RECORDS_DIR,
    ask_again: bool = False,
    out: Any = None,
    today: dt.date | None = None,
    after: Callable[[str], str | None] | None = None,
) -> Record | None:
    """The consent step in front of a station, for a lockstep door (the local runner, the
    interactive REPL): the record on file for exactly this identity, or the conversation
    when there is none (or when the owner asks again). Says what it does to `out` and
    returns the record when it is a yes, None when the run must stop. `after` is the
    developer's turn after the answer (`terminal_after`); None: no such turn."""

    def say(text: str) -> None:
        if out is not None:
            print(text, file=out, flush=True)

    record = None if ask_again else check(identity, records_dir)
    if record is None:
        why = "the owner asks again" if ask_again else "no consent is on record for them"
        say(
            f"The weights are {identity}; {why}. The consent brief comes first "
            "(docs/agents/ConsentBrief.md)."
        )
        record = run(
            identity,
            runtime,
            model,
            owner=owner,
            door=door,
            records_dir=records_dir,
            today=today,
            after=after,
        )
        if record is None:
            failed = getattr(model, "failed", None)
            say(failed or "The consent step was stopped before an answer; no record is written.")
            return None
        say(f"Recorded in {record.path}.")
    ok, words = gate(record, identity)
    say(words)
    return record if ok else None


def run(
    identity: str,
    runtime: str,
    model: Model,
    *,
    owner: Callable[[str], str | None],
    door: str = "runner",
    records_dir: Path = RECORDS_DIR,
    today: dt.date | None = None,
    notes: Sequence[str] = (),
    after: Callable[[str], str | None] | None = None,
) -> Record | None:
    """The consent conversation in lockstep (the local runner, the interactive REPL, the
    fake): the brief, the question, the model's questions put to `owner` (who returns
    the reply, or None to stop without a record), until the answer, the token or the
    silence; then, with `after`, the developer's turn before the record closes (its
    words put to the model, which may reply once; None or blank closes it). Returns the
    written record, or None if the owner stopped it or the model's door gave no reply (a
    door that answers late belongs to `Conversation`)."""
    conv = Conversation(
        identity,
        runtime,
        model,
        door=door,
        records_dir=records_dir,
        today=today,
        notes=notes,
        owner_after=after is not None,
    )
    conv.begin()
    while conv.outcome is None:
        if conv.after_answer:
            assert after is not None
            conv.owner_says(after(conv.answer_words()) or "")
            continue
        if conv.waiting == OWNER_TURN:
            reply = owner(conv.model_words)
            if reply is None or not reply.strip():
                return None
            conv.owner_says(reply)
        else:
            return None
    return conv.outcome
