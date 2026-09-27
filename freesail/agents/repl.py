"""The REPL door: a model that prints each sample to a stream and reads the reply from a
stream, and a command that runs a World in lockstep with it. A door, not a client: the
owner at a terminal can be the watcher, and the lead (a language model working through
a terminal, one reply a turn) can play a passage through it, one process invocation a
turn, once package 28 has put the consent step in front.

    python -m freesail.agents.repl <ship> --seed N --station watcher [--load SAVE]
                                   [--every SECONDS] [--wind FROM,KN] [--heading DEG]

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
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, TextIO

from freesail.agents import harness as harness_mod
from freesail.agents.agent import A_GLASS_S, SamplingPolicy, Station, watcher
from freesail.agents.fake import Transcript
from freesail.agents.model import MODEL, OPERATOR, Reply, ToolCall, Turn
from freesail.core import replay as replay_mod
from freesail.core.world import Scenario, World

__all__ = ["Repl", "REPLY_SYNTAX", "parse_reply", "render_turn", "main"]

REPLY_SYNTAX = (
    "Replies are typed as text; a tool call goes on its own line beginning with '>' "
    "and the tool's name, then its arguments as name=value with a value in quotes when "
    'it has spaces: > submit_order text="set the jib". A blank line ends the reply.'
)

STATIONS = {"watcher": watcher}


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
    log = d.get("log") or []
    if log:
        out.append(
            f"New log lines ({len(log)}"
            + (f", {d['log_omitted']} routine ones left out" if d.get("log_omitted") else "")
            + "):"
        )
        marks = {"routine": " ", "notable": "*", "urgent": "!"}
        out += [f"  {marks.get(e['severity'], ' ')} {e['stamp']}  {e['text']}" for e in log]
    else:
        out.append("No new log lines.")
    r = d.get("readings") or {}
    out.append("Readings:")
    for k, v in r.items():
        if isinstance(v, dict):
            out.append(f"  {k}: " + "; ".join(f"{a} {b}" for a, b in v.items()))
        else:
            out.append(f"  {k}: {v}")
    return "\n".join(out)


def _quote(v: Any) -> str:
    s = str(v)
    return shlex.quote(s) if (" " in s or not s) else s


def parse_reply(text: str) -> Reply:
    """The reply syntax of the module docstring: text lines, and `> tool k=v` lines."""
    lines: list[str] = []
    calls: list[ToolCall] = []
    for raw in text.splitlines():
        line = raw.rstrip("\n")
        if line.lstrip().startswith(">"):
            body = line.lstrip()[1:].strip()
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


def _station(args: argparse.Namespace) -> Station:
    try:
        make = STATIONS[args.station]
    except KeyError:
        raise SystemExit(
            f"No station '{args.station}'; the stations: {', '.join(STATIONS)}."
        ) from None
    return make(SamplingPolicy.in_lockstep(int(args.every), "notable", "urgent"))


def _save_fn(path: str):
    def save(world: World, reason: str) -> str:
        p = replay_mod.save_to_file(world, path)
        return str(p)

    return save


def run_interactive(args: argparse.Namespace, inp: TextIO, out: TextIO) -> int:
    from freesail.api.session import ship_factory

    model = Repl(inp, out)
    if args.load:
        data = replay_mod.load_file(args.load)
        world = replay_mod.replay(data, ship_factory)
        h = world.agents.get(args.station)
        if h is not None:
            h.model = model  # the recorded replies are played; the terminal continues
            h.save_fn = _save_fn(args.save)
    else:
        world = _new_world(args)
        h = None
    if h is None:
        h = harness_mod.Harness(
            world, _station(args), model, save=_save_fn(args.save), door_note=REPLY_SYNTAX
        )
        h.start()
    while not h.agent.released and not model.closed:
        world.tick()
    if model.closed and not h.agent.released:
        h.stand_down("the terminal closed", by="the terminal")
    model.show_new(h.turns)
    return 3 if h.agent.released else 0


def run_turn(args: argparse.Namespace) -> int:
    from freesail.api.session import ship_factory

    if not args.save or not args.sample:
        raise SystemExit("Turn mode needs --save STATE.json and --sample NEXT.txt.")
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
        world = replay_mod.replay(data, ship_factory)
        h = world.agents.get(args.station)
        if h is None:
            raise SystemExit(f"The save has no {args.station}.")
        h.save_fn = _save_fn(args.save)
    else:
        world = _new_world(args)
        h = harness_mod.Harness(
            world, _station(args), Transcript([]), save=_save_fn(args.save), door_note=REPLY_SYNTAX
        )
        h.start()
    ticks = 0
    while h.open_sample is None and not h.agent.released and ticks < args.max_ticks:
        world.tick()
        ticks += 1
    replay_mod.save_to_file(world, args.save)
    shown = 0
    for i in range(len(h.turns) - 1, -1, -1):
        if h.turns[i].role == MODEL:
            shown = i + 1
            break
    text = "\n\n".join(render_turn(t) for t in h.turns[shown:])
    if h.agent.released:
        text += f"\n\n== The station is released: {h.agent.released_reason}. =="
    elif h.open_sample is None:
        text += f"\n\n== No sampling point within {args.max_ticks} ticks; call again to go on. =="
    Path(args.sample).write_text(text + "\n", encoding="utf-8", newline="\n")
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
    ap.add_argument("--save", default="freesail-agent-save.json", help="where the game is saved")
    ap.add_argument("--turn", action="store_true", help="one turn from files, then exit")
    ap.add_argument("--reply", help="turn mode: the file holding this turn's reply")
    ap.add_argument("--sample", help="turn mode: where to write the next sample")
    ap.add_argument("--max-ticks", type=int, default=harness_mod.WELFARE_UNATTENDED_BOUND_S)
    args = ap.parse_args(argv)
    if args.turn:
        return run_turn(args)
    return run_interactive(args, sys.stdin, sys.stdout)


if __name__ == "__main__":
    sys.exit(main())
