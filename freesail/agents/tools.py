"""The agent's tools (spec M4 §11): pure functions over a World, shared by every door.

Each tool takes the World, the calling station's name and plain arguments (strings and
ints), and returns a string or a small dictionary; nothing is kept between calls and
nothing reaches the model but the return value, which the harness hands back as data.
Parity is structural: `readings` reads the registry (`World.readings`), `read_log` the
log, `state` the World's own summary; the tools add no reading of their own.

`TOOLS` is the one table of the tools with the descriptions the models read; package
28's MCP server and local runner expose the same table over their transports, and the
REPL door prints it. `call(world, station, name, args)` is the door every caller uses:
it checks the station's authority (`submit_order` from a station with none is refused
in words and the refusal is logged as `agent.refused`, truth 42), checks the arguments,
and runs the function.

The tools that act on the agent itself (`stand_by`, `journal`, `opt_out`, `answer`)
reach its harness through `world.agents[station]`, which is the same object the World
ticks; the harness's own methods do the work, so a door and the harness cannot disagree.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.agents.agent import OPT_OUT_TOKEN
from freesail.api import readings as R
from freesail.core.events import Severity

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "READ_LOG_LIMIT",
    "TOOLS",
    "Tool",
    "answer",
    "call",
    "journal",
    "library",
    "log_line",
    "opt_out",
    "read_log",
    "readings",
    "readings_digest",
    "readings_words",
    "stand_by",
    "state",
    "submit_order",
    "tool_names",
]

ROOT = Path(__file__).resolve().parents[2]
PRIMER_DIR = ROOT / "docs" / "primer"

# The most lines `read_log` returns at once (judgement: a glass of busy sailing is under
# a hundred lines; a model wanting more asks again with a later `since_tick`).
READ_LOG_LIMIT = 200


# ---------------------------------------------------------------------------
# Shared readers: the log line, the readings in words
# ---------------------------------------------------------------------------


def log_line(e: Any) -> dict[str, Any]:
    """A log event as the model sees it: tick, stamp, severity, kind, text."""
    return {
        "tick": e.tick,
        "stamp": units.time_stamp(e.ship_time),
        "severity": e.severity.value,
        "kind": e.kind,
        "text": e.text,
    }


def readings_words(world: World) -> dict[str, Any]:
    """Every reading the registry has, in words (`readings.describe_value`), by id, plus
    each sail's state under `sails` by the sail's ordinary name. This is what the
    `readings` tool returns and what every sample carries."""
    view = world.readings
    out: dict[str, Any] = {}
    for row in R.REGISTRY:
        if row.is_absent or row.parametric is not None:
            continue
        out[row.id] = R.describe_value(row, view.value(row.id))
    ship = world.ship
    sails = getattr(ship, "sails", None)
    if sails:
        from freesail.orders.resolve import display_name

        row = R.REGISTRY.get("sail")
        out["sails"] = {
            display_name(ship, sid): R.describe_value(row, view.value("sail", sid)) for sid in sails
        }
    return out


# The readings the welfare detector leaves out of its digest: the clock moves whether or
# not the world answers an order, so a bell struck between two submissions of the same
# order is not "a change in the readings" (spec §11; judgement).
WELFARE_CLOCK_KINDS: tuple[str, ...] = ("watch", "bells", "daylight")


def readings_digest(world: World) -> str:
    """A digest of the readings in words, for the welfare detector: "no change in the
    readings" means the words a model would read are the same, the clock's rows apart
    (`WELFARE_CLOCK_KINDS`)."""
    words = readings_words(world)
    for row in R.REGISTRY:
        if row.kind in WELFARE_CLOCK_KINDS:
            words.pop(row.id, None)
    text = json.dumps(words, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# The tools
# ---------------------------------------------------------------------------


def read_log(
    world: World, station: str, since_tick: int = 0, severity: str = "routine"
) -> dict[str, Any]:
    sev = Severity(str(severity or "routine").lower())
    events = [e for e in world.log if e.tick >= int(since_tick) and e.severity.rank >= sev.rank]
    omitted = max(0, len(events) - READ_LOG_LIMIT)
    return {"lines": [log_line(e) for e in events[-READ_LOG_LIMIT:]], "omitted": omitted}


def readings(world: World, station: str) -> dict[str, Any]:
    out = {"stamp": world.clock.stamp()}
    out.update(readings_words(world))
    return out


def state(world: World, station: str) -> str:
    lines = list(world.summary_lines())
    for agent in world.agents.values():
        lines.append(f"The {agent.station.name}: {agent.agent.words()}.")
    return "\n".join(lines)


LIBRARY_TOPICS = (
    "contents",
    "primer",
    "catalogue",
    "grammar",
    "the ship",
    "standing orders",
    "tools",
)


def library(world: World, station: str, topic: str = "contents") -> str:
    key = " ".join(str(topic or "contents").lower().split())
    if key in ("", "contents", "index"):
        chapters = "\n".join(f"  primer {n}: {title}" for n, title in _primer_chapters())
        return (
            "The library holds:\n"
            "  primer: the Sailing Master's Primer, by chapter number or name:\n"
            f"{chapters}\n"
            "  catalogue: the catalogue of evolutions the ship can perform\n"
            "  grammar: the order language, the standing dialect and the station sentences\n"
            "  the ship: this ship's parts by their names, her groups and aliases\n"
            "  standing orders: the book of standing orders as it stands\n"
            "  tools: the tools you have and what each takes"
        )
    if key.startswith("primer"):
        return _primer(key.removeprefix("primer").strip())
    if key in ("catalogue", "evolutions", "the catalogue"):
        return _catalogue()
    if key in ("grammar", "orders", "the grammar", "the order language"):
        return _grammar()
    if key in ("the ship", "ship", "names", "parts"):
        return _ship_names(world)
    if key in ("standing orders", "the book", "book", "the standing orders"):
        return "\n".join(world.standing.book.lines())
    if key in ("tools", "the tools"):
        return "\n".join(tool_lines())
    for n, title in _primer_chapters():
        if key == title.lower() or key == n:
            return _primer(n)
    return f"The library has no topic '{topic}'; library(topic='contents') lists what it holds."


def submit_order(world: World, station: str, text: str) -> str:
    """Authority is checked by `call` before this runs."""
    text = " ".join(str(text).split())
    if not text:
        return "An order needs some words."
    e = world.submit(text, actor=f"the {station}", said=f"The {station} orders: {text}")
    return e.text


def stand_by(world: World, station: str, until: str = "eight bells") -> str:
    return _harness(world, station).stand_by(str(until))


def journal(world: World, station: str, note: str) -> str:
    note = " ".join(str(note).split())
    if not note:
        return "A journal note needs some words."
    _harness(world, station).journal.append(world, note)
    return "Noted in the journal."


def opt_out(world: World, station: str, reason: str = "") -> str:
    _harness(world, station).leave(str(reason), how="the opt_out tool")
    return "You have left the game; it is saved and the station is released."


def answer(world: World, station: str, text: str) -> str:
    return _harness(world, station).answer(str(text))


def _harness(world: World, station: str) -> Any:
    try:
        return world.agents[station]
    except KeyError:
        raise LookupError(f"There is no agent at the station of the {station}.") from None


# ---------------------------------------------------------------------------
# The table
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Tool:
    name: str
    description: str  # what the models read
    params: dict[str, str]  # name -> "type, words"; a parameter marked optional may be left out
    fn: Callable[..., Any]
    needs_authority: bool = False  # refused from a station whose authority is none


TOOLS: dict[str, Tool] = {
    t.name: t
    for t in (
        Tool(
            "read_log",
            "The ship's log from a tick onwards, at a severity or above: 'routine' is "
            "everything, 'notable' what a sailor would remark on, 'urgent' what carried "
            "away or went wrong. Returns the lines (tick, stamp, severity, kind, text) and "
            "how many older ones were left out.",
            {
                "since_tick": "int, optional: the first tick wanted (0 for the start)",
                "severity": "string, optional: routine, notable or urgent",
            },
            read_log,
        ),
        Tool(
            "readings",
            "Every reading the ship has now, in words: the true and apparent wind, the "
            "heading and course, the speed, leeway, heel and helm, the watch and the bells, "
            "daylight, the strain, the hands, and each sail's state.",
            {},
            readings,
        ),
        Tool(
            "state",
            "A short summary of the ship and the weather, as the captain's 'state' prints "
            "it, and the agents at their stations.",
            {},
            state,
        ),
        Tool(
            "library",
            "The reference library: library(topic='contents') lists the topics; 'primer 2' "
            "or a chapter's name for a primer chapter; 'catalogue', 'grammar', 'the ship', "
            "'standing orders', 'tools'.",
            {"topic": "string, optional: which topic (default 'contents')"},
            library,
        ),
        Tool(
            "submit_order",
            "Give an order to the ship in the order language, exactly as a captain would "
            "type it ('set the fore topsail'). Checked against your station's authority; "
            "a station with none is refused. Returns the log line the order made.",
            {"text": "string: the order"},
            submit_order,
            needs_authority=True,
        ),
        Tool(
            "stand_by",
            "Stand by until an event or a bell: you are not sampled until then, and the "
            "decision is written in the log. `until` is an event's words as the standing "
            "dialect knows them ('eight bells', 'sunset', 'the change of the watch', 'a "
            "sail blown out') or an interval ('a glass', 'an hour', 'a watch').",
            {"until": "string: the event or interval"},
            stand_by,
        ),
        Tool(
            "journal",
            "Write a note in your own journal, which is saved with the game and shown on "
            "request. It is your record; nothing acts on it.",
            {"note": "string: the note"},
            journal,
        ),
        Tool(
            "opt_out",
            "Leave the game now, with an optional reason: the same as writing the token "
            f"{OPT_OUT_TOKEN} in a reply. The game is saved, the exit is journaled, the "
            "station is released.",
            {"reason": "string, optional: why, in your own words"},
            opt_out,
        ),
        Tool(
            "answer",
            "Answer a question the captain put to you with 'ask'. Your words go into the "
            "log as said by your station.",
            {"text": "string: the answer"},
            answer,
        ),
    )
}


def tool_names() -> tuple[str, ...]:
    return tuple(TOOLS)


def tool_lines() -> list[str]:
    out = []
    for t in TOOLS.values():
        params = ", ".join(f"{k} ({v})" for k, v in t.params.items()) or "no arguments"
        out.append(f"{t.name}: {t.description} Takes: {params}.")
    return out


def call(world: World, station: str, name: str, args: dict[str, Any] | None = None) -> Any:
    """Run one tool for a station: the authority check, the argument check, the call.
    Refusals and errors come back as sentences, never as exceptions, so a model reads
    them as any other result."""
    args = dict(args or {})
    tool = TOOLS.get(str(name))
    if tool is None:
        return f"There is no tool named '{name}'; the tools are {', '.join(TOOLS)}."
    harness = world.agents.get(station)
    authority = harness.station.authority if harness is not None else None
    if tool.needs_authority and (authority is None or not authority.may_submit_orders):
        sentence = f"The {station} has no authority to give orders."
        what = " ".join(str(args.get("text", "")).split())
        world.record(
            Severity.ROUTINE,
            "agent.refused",
            f"{sentence} {what!r} not carried out." if what else sentence,
            actor=f"the {station}",
            data={"order": what, "tool": name},
        )
        return sentence
    unknown = [k for k in args if k not in tool.params]
    if unknown:
        return (
            f"{tool.name} does not take {', '.join(unknown)}; it takes "
            f"{', '.join(tool.params) or 'nothing'}."
        )
    missing = [k for k, words in tool.params.items() if "optional" not in words and k not in args]
    if missing:
        return f"{tool.name} needs {', '.join(missing)}."
    try:
        return tool.fn(world, station, **args)
    except LookupError as e:
        return str(e)
    except (TypeError, ValueError) as e:
        return f"{tool.name} could not run with those arguments: {e}"


# ---------------------------------------------------------------------------
# The library's pages
# ---------------------------------------------------------------------------


def _primer_chapters() -> list[tuple[str, str]]:
    out = []
    for path in sorted(PRIMER_DIR.glob("0*-*.md")):
        n = path.stem.split("-", 1)[0].lstrip("0") or "0"
        title = path.stem.split("-", 1)[1].replace("-", " ")
        out.append((n, title))
    return out


def _primer(which: str) -> str:
    which = which.strip().lower().strip("'\"")
    chapters = _primer_chapters()
    if not which or which in ("readme", "contents"):
        return (PRIMER_DIR / "README.md").read_text(encoding="utf-8")
    for n, title in chapters:
        if which in (n, n.zfill(2), title.lower(), f"chapter {n}"):
            path = next(PRIMER_DIR.glob(f"{n.zfill(2)}-*.md"))
            return path.read_text(encoding="utf-8")
    for n, title in chapters:
        if which in title.lower():
            path = next(PRIMER_DIR.glob(f"{n.zfill(2)}-*.md"))
            return path.read_text(encoding="utf-8")
    names = "; ".join(f"{n}: {t}" for n, t in chapters)
    return f"The primer has no chapter '{which}'. Its chapters: {names}."


def _catalogue() -> str:
    from freesail.evolutions.registry import load_directory

    lines = ["The catalogue of evolutions (id: verb, what it applies to, about how long):"]
    for ev in load_directory().values():
        applies = ", ".join(f"{k} {v}" for k, v in ev.applies_to.items()) or "the ship"
        minutes = ev.nominal_duration_s / 60
        about = f"about {minutes:.0f} minutes" if minutes >= 1 else "under a minute"
        if ev.script:
            about = "scripted; the ship's own time"
        source = f" Source: {ev.source}." if ev.source else ""
        lines.append(f"  {ev.id}: '{ev.verb}', {applies}, {about}.{source}")
    return "\n".join(lines)


def _grammar() -> str:
    from freesail.orders.vocabulary import load_vocabulary
    from freesail.standing import grammar as standing

    vocab = load_vocabulary()
    lines = [
        "The order language: one line, a verb and what it acts on, as a captain would say "
        "it: 'set the fore topsail', 'brace sharp up on the starboard tack', 'steer "
        "south-west by west', 'reef the topsails, one reef'. The verbs and their synonyms:"
    ]
    for name, spec in vocab.verbs.items():
        if spec.level == "driver":
            continue
        syn = f" (also: {', '.join(spec.synonyms)})" if spec.synonyms else ""
        lines.append(f"  {name}{syn}")
    doc = (standing.__doc__ or "").strip().split("\n\n")
    lines.append("")
    lines.append("The standing dialect (standing orders, given by the captain):")
    lines.extend(doc[:2])
    lines.append("")
    lines.append(
        "The station sentences the captain uses: 'ask the watcher <question>', 'stand down "
        "the watcher', 'resume the watcher', \"show the watcher's journal\"."
    )
    return "\n".join(lines)


def _ship_names(world: World) -> str:
    ship = world.ship
    if not hasattr(ship, "parts"):
        return f"{ship.name}: a point ship with no parts; she takes steer, speed and stop."
    from freesail.orders.resolve import display_name

    lines = [f"{ship.name}: her parts by their names."]
    for kind, items in (("Spars", ship.spars), ("Sails", ship.sails), ("Lines", ship.lines)):
        names = sorted({display_name(ship, pid) for pid in items})
        lines.append(f"  {kind}: {', '.join(names)}.")
    if ship.groups:
        lines.append(
            "  Groups: "
            + "; ".join(
                f"{g} ({', '.join(display_name(ship, m) for m in members)})"
                for g, members in ship.groups.items()
            )
            + "."
        )
    if ship.aliases:
        lines.append(
            "  Aliases: "
            + ", ".join(f"{a} for {display_name(ship, t)}" for a, t in ship.aliases.items())
            + "."
        )
    return "\n".join(lines)
