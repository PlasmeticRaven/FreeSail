"""The REPL door: a model that prints each sample to a stream and reads the reply from a
stream, and a command that runs a World in lockstep with it. A door, not a client: the
owner at a terminal can be the watcher, and the lead (a language model working through
a terminal, one reply a turn) can play a passage through it, one process invocation a
turn, once package 28 has put the consent step in front.

    python -m freesail.agents.repl <ship> --seed N --station watcher [--load SAVE]
                                   [--every SECONDS] [--wind FROM,KN] [--heading DEG]
                                   [--replay-anyway]

prints the brief once, then at each sampling point prints the sample and waits for a
reply on stdin. **The reply syntax**: free text on any line; a tool call on its own
line beginning with `>`, the tool's name and then its arguments as `name=value`, a
value with spaces in quotes:

    The wind is freshening from the west and she is heeling more than she was.
    > read_log since_tick=1800 severity=notable
    > submit_order text="set the jib"
    > stand_by until="eight bells"

A blank line ends the reply (a blank line at once is an empty reply, which the harness
counts as silence); end of input stands the agent down. A reply with tool calls is
followed by their results and another prompt, until a reply without calls ends the
sample. `FREESAIL-OPT-OUT` anywhere in a reply ends the session as the brief says.

**Turn mode**, for a step driven by separate process invocations:

    python -m freesail.agents.repl <ship> --seed N --station watcher --turn \\
        --save STATE.json --sample NEXT.txt [--load STATE.json --reply REPLY.txt]

The first call (no `--load`) makes the World, stations the agent, runs to the first
sampling point, and writes the save to `--save` and the brief with the first sample to
`--sample`. Each later call loads the save, replays it (the recorded replies are played
back so the log is the same), applies the one reply read from `--reply` to the open
sample, advances the World to the next sampling point (or `--max-ticks`), and writes
the save and the next sample to the files. The exit code is 0 while the station is
manned and 3 once it is released (the token, a stand-down), so a driving script knows
when to stop. Nothing here talks to a model; the text on the streams is the whole door.

**Who is at the terminal** (package 28). Every run says: `--model-name <identity>` for a
language model (the lead playing through the door is one), or `--human` for a person.
The owner's rule is that the consent step exempts no model, so a named model meets the
consent brief (`consent.py`) before any station brief, unless a yes is on record for
exactly that identity; the record names the runtime as this door. In turn mode the
consent conversation runs a turn a call like the station: the first call writes the
brief and the question to `--sample`; each later call takes the model's reply from
`--reply`. When the model writes something without answering, it is for the owner: the
call exits 4 with the words in `--sample`, and the owner's reply comes in the next call
with `--owner-reply FILE`. After the answer the developer has a turn before the record
closes (package 28c): the call exits 4, and the next call's `--owner-reply FILE` is put
to the model (which may reply once, by `--reply`), or, empty, closes the record. The
record written, a yes goes straight on to the station's brief and first sample in the
same call, anything else exits 5 with the reason. A game saved under a named model is
continued only while a yes is on record for that name.

**A released station taken again** (package 37g, items 13 and 14; the review's section 6:
"the REPL door cannot seat again at all"). A save whose station was stood down, or left,
is loaded, and the game's one rule decides as it does at every door
(`harness.seating`): an identity that left for good is refused, at any station; one that
left by its own word is asked for its consent again first, with the fact that an
instance left and the reason it gave, and its answer is kept; every other takes the
station, its own or another's (a relief), with the last handover note in its brief. In
turn mode a station is taken again when no question is owed; where one is, the call says
so in words and the question is put at the interactive door.
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any, TextIO

from freesail.agents import consent
from freesail.agents import harness as harness_mod
from freesail.agents.agent import (
    A_GLASS_S,
    TURN_ENDS_WORDS,
    SamplingPolicy,
    Station,
    captain,
    officer,
    station_name,
    watcher,
)
from freesail.agents.fake import Transcript
from freesail.agents.model import MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.api import readings as R
from freesail.core import replay as replay_mod
from freesail.core.world import Scenario, World

__all__ = [
    "REPL_RUNTIME",
    "REPLY_HINT",
    "Repl",
    "REPLY_SYNTAX",
    "parse_reply",
    "render_turn",
    "main",
]

# The runtime a consent record names for this door.
REPL_RUNTIME = "the REPL door of FreeSail's harness (text at a terminal, one reply a turn)"

# Exit codes of turn mode beyond 0 (manned) and 3 (released).
EXIT_OWNER = 4  # the consent conversation waits for the owner's reply
EXIT_NO_CONSENT = 5  # no yes on record: the run stops

REPLY_SYNTAX = (
    "Replies are typed as text; a tool call goes on its own line beginning with '>' "
    "and the tool's name, then its arguments as name=value with a value in quotes when "
    'it has spaces: > submit_order text="set the jib" (a line that begins with a tool\'s '
    "name and carries only name=value words is taken as the call even without the '>'). "
    "Nothing is sent until a blank line: type the reply, then press return on an empty "
    f"line to send it. {TURN_ENDS_WORDS}"
)

# Printed before every reply is read, so that a person at the terminal is never left to
# guess the two rules (the owner's first practice run, 2026-09-27, stumbled on both).
REPLY_HINT = (
    "Type your reply, then a blank line to send it. A tool call is a line beginning "
    'with >, such as > answer text="yes" or > readings.'
)

# The stations this door seats, by their factories: the watcher, the officer of the
# watch (`--station officer`; package 37) and the captain (`--station captain`; package 40).
STATIONS = {"watcher": watcher, "officer of the watch": officer, "captain": captain}


# ---------------------------------------------------------------------------
# Rendering and parsing
# ---------------------------------------------------------------------------


def render_turn(turn: Turn) -> str:
    """One turn as text for the stream. The operator brief is marked as such; a data
    turn is marked as data from the game; a model turn as the reply given."""
    if turn.role == OPERATOR:
        return "== The brief (operator text; the only operator message) ==\n" + str(turn.content)
    if turn.role == MODEL:
        r: Reply = turn.content
        lines = [r.text] if r.text else []
        lines += [
            f"> {c.name} " + " ".join(f"{k}={_quote(v)}" for k, v in c.args.items())
            for c in r.calls
        ]
        return "== Your reply ==\n" + ("\n".join(lines) or "(nothing)")
    d = turn.content
    words = harness_mod.conversation_text(d)
    if words is not None:
        return f"== From the developer ({d.get('reason', '')}) ==\n{words}"
    if "tool_results" in d:
        out = ["== Tool results (data) =="]
        for res in d["tool_results"]:
            value = res.get("result")
            text = value if isinstance(value, str) else json.dumps(value, indent=1)
            out.append(f"{res['name']}: {text}")
        return "\n".join(out)
    out = [f"== Sample at {d.get('stamp')} (data from the game; reason: {d.get('reason')}) =="]
    for n in d.get("notices") or []:
        out.append(f"Notice from the harness: {n}")
    if d.get("question"):
        out.append(f"The captain asks: {d['question']}?")
    if d.get("word"):
        out.append(f"The captain tells you: {d['word']}")
    sb = d.get("stood_by")
    if sb:
        # the stand-by's digest (package 28c): the notable lines while it lasted
        n = int(sb.get("notable") or 0)
        lines = "no notable lines" if n == 0 else f"{n} notable line{'s' if n != 1 else ''}"
        out.append(
            f"While you stood by (since {sb.get('since')}, until {sb.get('until')}): {lines} "
            "logged" + (":" if n else ".")
        )
        out += [f"  * {ln['stamp']}  {ln['text']}" for ln in sb.get("lines") or []]
    log = d.get("log") or []
    if log:
        out.append(
            f"New log lines ({len(log)}"
            + (f", {d['log_omitted']} routine ones left out" if d.get("log_omitted") else "")
            + "):"
        )
        marks = {"routine": " ", "notable": "*", "urgent": "!"}
        out += [
            f"  {marks.get(e['severity'], ' ')} {e['stamp']}  {e['text']}{_by_words(e)}"
            for e in log
        ]
    else:
        out.append("No new log lines.")
    r = d.get("readings") or {}
    if d.get("readings_are"):
        # a sample after the first: the readings changed since the last (package 31c)
        out.append(f"Readings, {d['readings_are']}:" if r else "Readings: none has changed.")
    else:
        out.append("Readings:")
    for k, v in r.items():
        if isinstance(v, dict):
            out.append(f"  {k}: " + "; ".join(f"{a} {b}" for a, b in v.items()))
        else:
            out.append(f"  {k}: {v}")
    return "\n".join(out)


def _by_words(line: dict[str, Any]) -> str:
    """Who gave the order a log line is, where the line's own words do not say (package
    37g, item 9): the captain's "Order: steer east." is marked his, and a standing
    order's firing with whose book it stands in."""
    by = str(line.get("by") or "")
    text = str(line.get("text") or "")
    if not by:
        return ""
    if by.startswith("standing order ") and by.endswith(")") and "(" in by:
        return f"  [{by[by.rindex('(') + 1 : -1]}'s standing order]"
    if by in text:
        return ""
    return f"  [{by}]"


def _quote(v: Any) -> str:
    s = str(v)
    return shlex.quote(s) if (" " in s or not s) else s


def _looks_like_a_call(line: str) -> bool:
    """A line that names a tool and carries only name=value words after it is a tool
    call without the '>' (a person's slip the door forgives; `answer text="Yes."`)."""
    from freesail.agents.tools import TOOLS

    try:
        words = shlex.split(line)
    except ValueError:
        words = line.split()
    if not words or words[0] not in TOOLS:
        return False
    return all("=" in w for w in words[1:])


def parse_reply(text: str) -> Reply:
    """The reply syntax of the module docstring: text lines, and `> tool k=v` lines."""
    lines: list[str] = []
    calls: list[ToolCall] = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if line.lstrip().startswith(">") or _looks_like_a_call(line.strip()):
            body = line.lstrip().lstrip(">").strip()
            if not body:
                continue
            try:
                words = shlex.split(body)
            except ValueError:
                words = body.split()
            name, args = words[0], {}
            for w in words[1:]:
                k, _, v = w.partition("=")
                args[k] = int(v) if v.lstrip("-").isdigit() else v
            calls.append(ToolCall(name, args))
        else:
            lines.append(line)
    return Reply(text="\n".join(lines).strip(), calls=tuple(calls), raw=text)


# ---------------------------------------------------------------------------
# The model
# ---------------------------------------------------------------------------


class Repl:
    """Prints the turns it has not shown yet, then reads one reply: lines until a blank
    line or the end of input. At the end of input `reply` returns None and `closed` is
    set, and the driver stands the agent down."""

    def __init__(self, inp: TextIO, out: TextIO, prompt: str = "reply> "):
        self.inp = inp
        self.out = out
        self.prompt = prompt
        self.shown = 0
        self.closed = False

    def show_new(self, turns: Sequence[Turn]) -> None:
        for t in turns[self.shown :]:
            print(render_turn(t), file=self.out, flush=True)
            print(file=self.out, flush=True)
        self.shown = len(turns)

    def reply(self, turns: Sequence[Turn]) -> Reply | None:
        self.show_new(turns)
        if self.closed:
            return None
        print(REPLY_HINT, file=self.out, flush=True)
        print(self.prompt, end="", file=self.out, flush=True)
        lines: list[str] = []
        while True:
            line = self.inp.readline()
            if line == "":
                self.closed = True
                break
            if line.strip() == "":
                break
            lines.append(line.rstrip("\n"))
        if self.closed and not lines:
            return None
        return parse_reply("\n".join(lines))


# ---------------------------------------------------------------------------
# The command
# ---------------------------------------------------------------------------


def _scenario(args: argparse.Namespace) -> Scenario:
    scenario = Scenario()
    if args.wind:
        d, s = args.wind.split(",")
        scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
    if args.heading is not None:
        scenario.ship_heading_deg = args.heading
    return scenario


def _new_world(args: argparse.Namespace) -> World:
    from freesail.api.session import make_world

    scenario = _scenario(args)
    if args.ship:
        return make_world(args.seed, args.ship, scenario)
    return World(seed=args.seed, scenario=scenario)


def replay_save(
    data: dict[str, Any], path: str, replay_anyway: bool = False, out: TextIO | None = None
) -> World:
    """A save replayed at this door, which always replays (the recorded replies are
    played back and the terminal goes on), by the load's rule (package 37d;
    `core.replay.check_replay`): a save of another build, or unstamped, that holds a
    station's transcript is refused in words (the run stops with them) unless
    `--replay-anyway`; one without a transcript is replayed and `out` is told that its
    log may differ from the one that was watched. A save of this build replays as it
    always did, with a line to `out` when one is given."""
    from freesail.api.session import ship_factory

    try:
        report = replay_mod.check_replay(data, path, replay_anyway)
    except replay_mod.ReplayRefused as refused:
        raise SystemExit("\n".join(refused.report.words)) from None
    world = replay_mod.replay(data, ship_factory)
    if out is not None:
        for line in report.words:
            print(line, file=out, flush=True)
    return world


def open_world(
    target: str | None,
    seed: int,
    wind: str | None = None,
    heading: float | None = None,
    replay_anyway: bool = False,
) -> World:
    """A ship file or a save (a `.json`, replayed by the load's rule, `replay_save`), as
    the console opens them; the doors of package 28 share it. `wind` is
    'FROM_DEG,KNOTS'."""
    from freesail.api.session import make_world
    from freesail.ui.console import restore_python_rules

    if target and target.lower().endswith(".json"):
        data = replay_mod.load_file(target)
        world = replay_save(data, target, replay_anyway, out=sys.stderr)
        restore_python_rules(world, data)
        return world
    scenario = Scenario()
    if wind:
        d, s = wind.split(",")
        scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
    if heading is not None:
        scenario.ship_heading_deg = heading
    if target:
        return make_world(seed, target, scenario)
    return World(seed=seed, scenario=scenario)


def _station(args: argparse.Namespace, world: World | None = None) -> Station:
    try:
        make = STATIONS[station_name(args.station)]
    except KeyError:
        raise SystemExit(
            f"No station '{args.station}'; the stations: {', '.join(STATIONS)}."
        ) from None
    return make(SamplingPolicy.in_lockstep(int(args.every), "notable", "urgent"), world=world)


def _save_fn(path: str):
    def save(world: World, reason: str) -> str:
        p = replay_mod.save_to_file(world, path)
        return str(p)

    return save


# The shelf at this door (package 28d): each turn is printed once and stays with the
# reader, so shelving cannot take pages back; the brief says so plainly.
SHELF_NOTE = (
    "This door prints each turn once, and what it has printed stays with you: shelve notes "
    "a book as put back and the game will not show its pages again, but it cannot take "
    "them back from you."
)


def _consent_note(record: consent.Record | None) -> str:
    if record is None:
        return f"{REPLY_SYNTAX} {SHELF_NOTE}"
    where = consent._rel(record.path) if record.path else "docs/agents/consent/"
    return (
        f"{REPLY_SYNTAX} {SHELF_NOTE} Consent for this model is on record ({where}, {record.date})."
    )


# How often the interactive REPL looks at a paused station's ten real minutes, in real
# seconds (judgement: the clock holds meanwhile; a second is nothing to wait at a pause).
PAUSE_POLL_S = 1.0

# A paused station at this door, in words (package 31c): the terminal is the station's and
# not the captain's, so nobody here answers a pause, and the ten real minutes decide.
PAUSED_HERE = (
    "== The {station} is paused: {reason}. Nobody at this door answers a pause (the "
    "terminal is the station's, not the captain's); the clock holds, and the {station} is "
    "stood down after ten real minutes unless it leaves first. =="
)


def run_interactive(
    args: argparse.Namespace,
    inp: TextIO,
    out: TextIO,
    *,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> int:
    """The REPL at a terminal, in lockstep. A pause holds the clock and the ten real
    minutes of the unattended bound run on `clock` (package 31c: the one bound, however
    fast the ship's clock would run); `clock` and `sleep` are the test's to give."""
    identity = args.model_name or ""
    station = station_name(args.station)
    world = None
    again = None  # the game's one rule, when the save's station is released
    if args.load:
        data = replay_mod.load_file(args.load)
        world = replay_save(data, args.load, getattr(args, "replay_anyway", False), out=out)
        held = world.agents.get(station)
        if held is not None and held.agent.released:
            again = harness_mod.seating(world, station, identity)
            if not again.ok:
                print(f"== {again.why} ==", file=out, flush=True)
                return EXIT_NO_CONSENT
    record = None
    if args.model_name:
        record = consent.ensure(
            args.model_name,
            REPL_RUNTIME,
            Repl(inp, out),
            door="repl",
            owner=consent.terminal_owner(inp, out),
            records_dir=Path(args.records),
            ask_again=args.ask_again,
            out=out,
            after=consent.terminal_after(inp, out),
            drills=_station(args).drill,
            # the question put again after an opt-out says why (package 37g, item 13)
            asked_why=again.asked_why if again is not None and again.ask_again else "",
        )
        if again is not None and again.ask_again:
            # the answer is kept beside the leaving, whatever it was: a no is held to,
            # and the question is not put again at each start
            asked = consent.check(args.model_name, Path(args.records))
            left = world.agents.get(again.left_at) if world is not None else None
            if left is not None:
                left.door_act("asked", identity, asked.verdict if asked is not None else "")
        if record is None:
            return EXIT_NO_CONSENT
    else:
        print(
            "A human at the terminal (--human): no consent step. A language model at this door "
            "is named with --model-name and meets the consent brief first.",
            file=out,
            flush=True,
        )
    model = Repl(inp, out)
    h = None
    if world is not None:
        h = world.agents.get(station)
        if h is not None and h.agent.released:
            # a released station taken again, by the same identity or another (37g)
            h.reseat(
                model,
                identity=identity,
                door="repl",
                save=_save_fn(args.save),
                door_note=_consent_note(record),
            )
        elif h is not None:
            h.model = model  # the recorded replies are played; the terminal continues
            h.save_fn = _save_fn(args.save)
    else:
        world = _new_world(args)
    if h is None:
        h = harness_mod.Harness(
            world,
            _station(args, world),
            model,
            save=_save_fn(args.save),
            door_note=_consent_note(record),
        )
        h.door = "repl"  # the terminal keeps what it printed (the shelf's words)
        h.model_name = identity
        h.start()
    told_paused = False
    while not h.agent.released and not model.closed:
        if h.agent.paused:
            if not told_paused:
                words = PAUSED_HERE.format(station=h.station.name, reason=h.agent.pause_reason)
                print(words, file=out, flush=True)
                told_paused = True
            if not h.check_unattended(now=clock()):
                sleep(PAUSE_POLL_S)
            continue
        told_paused = False
        world.tick()
    if model.closed and not h.agent.released:
        h.stand_down("the terminal closed", by="the terminal")
    model.show_new(h.turns)
    if h.agent.released:
        print(f"== The station is released: {h.agent.released_reason}. ==", file=out, flush=True)
    return 3 if h.agent.released else 0


def _write_sample(args: argparse.Namespace, text: str) -> None:
    Path(args.sample).write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def _since_last_reply(turns: list[Turn]) -> str:
    shown = 0
    for i in range(len(turns) - 1, -1, -1):
        if turns[i].role == MODEL:
            shown = i + 1
            break
    return "\n\n".join(render_turn(t) for t in turns[shown:])


def _consent_turn(args: argparse.Namespace) -> tuple[int | None, str, consent.Record | None]:
    """Turn mode's consent step for a named model. Returns (an exit code when the step
    holds the run, else None), words to put before the station's first sample, and the
    record when it is a yes."""
    identity = args.model_name
    records_dir = Path(args.records)
    drills = _station(args).drill
    state = None
    if args.load:
        loaded = json.loads(Path(args.load).read_text(encoding="utf-8"))
        state = loaded.get("consent") if isinstance(loaded, dict) else None
    if state is None:
        if args.load:
            record = consent.check(identity, records_dir)
            ok, words = consent.gate(record, identity)
            if ok:
                return None, "", record
            _write_sample(args, f"== {words} ==")
            return EXIT_NO_CONSENT, "", None
        record, kind, words = consent.decide(
            identity, records_dir, "repl", drills=drills, ask_again=args.ask_again
        )
        if not kind:
            if record is not None and record.proceeds:
                return None, "", record
            _write_sample(args, f"== {words} ==")
            return EXIT_NO_CONSENT, "", None
        state = {
            "identity": identity,
            "replies": [],
            "owner_replies": [],
            "drill_only": kind == consent.DRILL_KIND,
        }
    if state.get("identity") != identity:
        raise SystemExit(
            f"The save holds the consent conversation with {state.get('identity')}, not "
            f"{identity}; consent is never carried from one model to another."
        )
    if state.get("done"):
        _write_sample(args, f"== {state['done']} ==")
        return EXIT_NO_CONSENT, "", None
    replies = [Reply.from_dict(r) for r in state["replies"]]
    owner_replies = list(state["owner_replies"])
    conv = consent.Conversation(
        identity,
        REPL_RUNTIME,
        Transcript(replies),
        door="repl",
        records_dir=records_dir,
        owner_after=True,
        drill=drills,
        drill_only=bool(state.get("drill_only")),
    )
    conv.begin()
    queue = list(owner_replies)
    while conv.outcome is None and conv.waiting == consent.OWNER_TURN and queue:
        conv.owner_says(queue.pop(0))
    note = ""
    if conv.outcome is None and conv.waiting == consent.MODEL_TURN and args.reply:
        new = parse_reply(Path(args.reply).read_text(encoding="utf-8"))
        replies.append(new)
        conv.deliver(new)
    elif conv.outcome is None and conv.waiting == consent.OWNER_TURN and args.owner_reply:
        text = Path(args.owner_reply).read_text(encoding="utf-8").strip()
        owner_replies.append(text)
        conv.owner_says(text)
    elif args.load and (args.reply or args.owner_reply):
        whose = (
            "the owner's (--owner-reply)"
            if conv.waiting == consent.OWNER_TURN
            else ("the model's (--reply)")
        )
        note = f"\n\n== That reply was not taken: the turn is {whose}. =="
    state = {
        "identity": identity,
        "replies": [r.to_dict() for r in replies],
        "owner_replies": owner_replies,
        "drill_only": conv.drill_only,
    }
    if conv.outcome is not None:
        ok, words = consent.gate(conv.outcome, identity)
        if ok:
            return None, f"== {words} ==", conv.outcome
        state["done"] = words
        Path(args.save).write_text(
            json.dumps({"consent": state}, indent=1) + "\n", encoding="utf-8", newline="\n"
        )
        _write_sample(args, f"{_since_last_reply(conv.turns)}\n\n== {words} ==")
        return EXIT_NO_CONSENT, "", None
    Path(args.save).write_text(
        json.dumps({"consent": state}, indent=1) + "\n", encoding="utf-8", newline="\n"
    )
    if conv.after_answer:
        _write_sample(
            args,
            f"{_since_last_reply(conv.turns)}\n\n== {conv.answer_words()} ==\n\n== Before the "
            "record closes the developer may ask or say something, which the model may answer "
            "once: call again with --owner-reply FILE (an empty file closes the record) ==" + note,
        )
        return EXIT_OWNER, "", None
    if conv.waiting == consent.OWNER_TURN:
        _write_sample(
            args,
            "== The model has written this and has not answered; it is for the owner ==\n"
            f"{conv.model_words}\n\n== The run waits for the owner's reply: call again with "
            f"--owner-reply FILE ==" + note,
        )
        return EXIT_OWNER, "", None
    _write_sample(args, _since_last_reply(conv.turns) + note)
    return 0, "", None


def run_turn(args: argparse.Namespace, wall: Callable[[], float] | None = None) -> int:
    """One turn from files. A pause holds the clock; the ten real minutes of the
    unattended bound are measured across the calls on `wall` (the wall clock, since each
    call is a process of its own), from when a call first found the station paused, kept
    in the save beside the game (`repl.paused_since`; package 31c)."""
    if not args.save or not args.sample:
        raise SystemExit("Turn mode needs --save STATE.json and --sample NEXT.txt.")
    before, record = "", None
    paused_since: float | None = None
    if args.model_name:
        code, before, record = _consent_turn(args)
        if code is not None:
            return code
        if before:  # the yes came in this call: the station starts afresh
            args.load, args.reply = None, None
    if args.load:
        data = replay_mod.load_file(args.load)
        new_reply = None
        if args.reply:
            new_reply = parse_reply(Path(args.reply).read_text(encoding="utf-8"))
        # the new reply is appended to the recorded transcript before the replay, so the
        # open sample at the end tick takes it as the replay reaches it
        for record in data.get("agents") or []:
            if record["station"]["name"] == args.station and new_reply is not None:
                record["transcript"].append(
                    {"tick": data["end_tick"], "reply": new_reply.to_dict()}
                )
        # each call replays the state the call before wrote: this build's, and silent as
        # it always was; another build's is refused or warned of by the load's rule
        # (package 37d), the words to the terminal's error stream
        world = replay_save(
            data,
            args.load,
            getattr(args, "replay_anyway", False),
            out=None if replay_mod.same_build(replay_mod.stamp_of(data)) else sys.stderr,
        )
        h = world.agents.get(station_name(args.station))
        if h is None:
            raise SystemExit(f"The save has no {args.station}.")
        h.save_fn = _save_fn(args.save)
        paused_since = (data.get("repl") or {}).get("paused_since")
        if h.agent.released and new_reply is None:
            # a released station taken again by the game's one rule (package 37g): at
            # once when no question is owed; where one is, in words, for the interactive
            # door to put it
            again = harness_mod.seating(world, h.station.name, args.model_name or "")
            # (a human at this door meets no consent step, so none is owed again)
            if not again.ok or (again.ask_again and args.model_name):
                words = again.why or (
                    f"{args.model_name} left this game by its own word, and the consent "
                    "question is put again before it is seated: start this door without "
                    "--turn for the question, and then call again."
                )
                _write_sample(args, f"== {words} ==")
                return 3
            h.reseat(
                Transcript([]),
                identity=args.model_name or "",
                door="repl",
                save=_save_fn(args.save),
            )
    else:
        world = _new_world(args)
        h = harness_mod.Harness(
            world,
            _station(args, world),
            Transcript([]),
            save=_save_fn(args.save),
            door_note=_consent_note(record),
        )
        h.door = "repl"  # the reader keeps what each call wrote (the shelf's words)
        h.model_name = args.model_name or ""
        h.start()
    ticks = 0
    while (
        h.open_sample is None
        and not h.agent.released
        and not h.agent.paused
        and ticks < args.max_ticks
    ):
        world.tick()
        ticks += 1
    if h.agent.paused:
        now = (wall or time.time)()
        paused_since = now if paused_since is None else float(paused_since)
        h.check_unattended(now=now, since=paused_since)
    replay_mod.save_to_file(world, args.save)
    if h.agent.paused:
        kept = json.loads(Path(args.save).read_text(encoding="utf-8"))
        kept["repl"] = {"paused_since": paused_since}
        Path(args.save).write_text(json.dumps(kept, indent=2), encoding="utf-8")
    text = _since_last_reply(h.turns)
    if before:
        text = f"{before}\n\n{text}"
    if h.agent.released:
        text += f"\n\n== The station is released: {h.agent.released_reason}. =="
    elif h.agent.paused:
        text += "\n\n" + PAUSED_HERE.format(station=h.station.name, reason=h.agent.pause_reason)
    elif h.open_sample is None:
        text += f"\n\n== No sampling point within {args.max_ticks} ticks; call again to go on. =="
    _write_sample(args, text)
    return 3 if h.agent.released else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail: the REPL door for an agent's station")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, default=1805)
    ap.add_argument("--station", default="watcher")
    ap.add_argument("--every", type=int, default=A_GLASS_S, help="sampling period, ship's seconds")
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS'")
    ap.add_argument("--heading", type=float)
    ap.add_argument("--load", help="a save to replay and continue from")
    ap.add_argument(
        "--replay-anyway",
        action="store_true",
        help="replay a save all the same when it was written by another build and holds a "
        "station's transcript (the replay is then not the game that was played); without "
        "it such a save is refused in words",
    )
    ap.add_argument("--save", default="freesail-agent-save.json", help="where the game is saved")
    ap.add_argument("--turn", action="store_true", help="one turn from files, then exit")
    ap.add_argument("--reply", help="turn mode: the file holding this turn's reply")
    ap.add_argument("--sample", help="turn mode: where to write the next sample")
    # a watch of ship's time a call at most (a length for a turn, not a stand-down)
    ap.add_argument("--max-ticks", type=int, default=R.INTERVALS["a watch"])
    who = ap.add_mutually_exclusive_group()
    who.add_argument(
        "--model-name", help="the exact identity of the model at the terminal (consent first)"
    )
    who.add_argument("--human", action="store_true", help="a person at the terminal")
    ap.add_argument("--records", default=str(consent.RECORDS_DIR), help="the consent records")
    ap.add_argument("--ask-again", action="store_true", help="put the consent question again")
    ap.add_argument("--owner-reply", help="turn mode: the owner's reply to the model's question")
    args = ap.parse_args(argv)
    if not args.model_name and not args.human:
        ap.error(
            "say who is at the terminal: --model-name <identity> for a language model (the "
            "consent step comes first) or --human for a person"
        )
    if args.turn:
        return run_turn(args)
    return run_interactive(args, sys.stdin, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
