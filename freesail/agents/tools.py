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

The tools that act on the agent itself (`stand_by`, `journal`, `read_journal`,
`hand_over`, `stand_down`, `opt_out`, `answer`, `shelve`) reach its harness through
`world.agents[station]`, which is the same object the World ticks; the harness's own
methods do the work, so a door and the harness cannot disagree.

**The three ways of stopping** (package 37g, item 12) are three tools that cannot be
taken for one another, and each says in its result which it was: `hand_over(note)` gives
the deck back and the officer stays at his station; `stand_down(note)`, for any station,
saves the game and releases the station to be taken again; `opt_out` (or the token)
withdraws. **The journal is read back** with `read_journal` (item 15), and `read_log`
reaches back past its newest lines by a tick or a count. **An order's authority**
(`authority_check`) is the station's domain, then the captain's word: a named grant,
which means what it says; his general authority to work the ship, with what it keeps
back; and, to avoid an immediate danger, the officer's own word (`submit_order` with
`danger`), for the helm, heaving to and letting go an anchor and nothing else.

**The shelf** (package 28d; spec M4 open item 9, the context work for local models). The
library is served in pieces with their sizes, so that a model with a small context reads
what it needs and not a chapter at a time: `library()` lists the topics with what each
costs; a topic with sections (a primer chapter, the primer's own introduction, the
catalogue by evolution, the grammar by part, the ship by mast) lists its sections with
theirs; `section=` serves one (matched by a word of its heading, case-insensitively, or by
its number), `section='all'` the whole with its size first; `find=` returns the matching
paragraphs, each with where it is. Sizes are measured from the text served, at
`CHARS_PER_TOKEN` characters a token, the one rule the harness measures text by (the local
runner's budget uses it too). A library page is a `Page`: its text, with the words that
name it and the call that reads it again, from which the harness makes a *book* with a
handle (`harness.Harness`); `shelve` puts a book back. The reference is a promise, not a
possession (`docs/design/Papers-and-Books.md`): every page is always there to be read
again.
"""

from __future__ import annotations

import functools
import hashlib
import json
import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.agents.agent import (
    OPT_OUT_TOKEN,
    SHELF_LIFE_TURNS,
    WEATHER_EVENT_WORDS,
    number_words,
)
from freesail.api import readings as R
from freesail.core.events import Severity
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import load_vocabulary

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "BOOK_TOOLS",
    "CHARS_PER_TOKEN",
    "FIND_LIMIT",
    "HAND_OVER_BY_TOOL",
    "READ_LOG_LIMIT",
    "TOOLS",
    "Page",
    "Tool",
    "answer",
    "authority_check",
    "book_of",
    "call",
    "hand_over",
    "handover_note",
    "journal",
    "library",
    "log_line",
    "opt_out",
    "PICTURE_DOORS",
    "PICTURE_TOOLS",
    "chart",
    "parameters_schema",
    "ship_view",
    "read_journal",
    "read_log",
    "readings",
    "readings_digest",
    "readings_words",
    "shelve",
    "size_words",
    "stand_by",
    "stand_down",
    "state",
    "submit_order",
    "tokens",
    "tool_names",
    "truthy",
]

ROOT = Path(__file__).resolve().parents[2]
PRIMER_DIR = ROOT / "docs" / "primer"

# The most lines `read_log` returns at once (judgement: a glass of busy sailing is under
# a hundred lines; a model wanting more asks again with a later `since_tick`).
READ_LOG_LIMIT = 200
# ...unless it asks for more by `count` (package 37g, item 15; the review's 5.4: on the
# Speedwell 293 notable lines lay between the officer and its own note, beyond the reach
# of the newest two hundred). The most a count may ask for (judgement: five times the
# default, about a watch of busy sailing; a longer reach is made a page at a time with
# `before_tick`).
READ_LOG_MAX = 1000

# The entries `read_journal` returns when no count is given (judgement: the last score of
# entries is a watch's worth of an officer's notes and the harness's lines between them).
READ_JOURNAL_DEFAULT = 20

# About four characters of English to a token (judgement: the usual rule of thumb for
# BPE vocabularies). The one rule the harness measures text by: the library's sizes, a
# book's size (`agent.BOOK_SIZE_TOKENS`) and the local runner's context budget.
CHARS_PER_TOKEN = 4

# The most paragraphs a `find` returns whole; the rest are named by where they are, with
# a count (judgement: eight paragraphs of the primer are some hundreds of tokens to a
# thousand, a page a small context can take; the places of the rest say where to read).
FIND_LIMIT = 8

# The tools whose results may be books (the harness gives each a handle): every library
# read, and a read_log longer than `agent.BOOK_SIZE_TOKENS`.
BOOK_TOOLS: tuple[str, ...] = ("library", "read_log", "read_journal", "chart", "ship_view")

# The tools that make a picture (package 42, item 4; `agents.pictures`), and the doors
# that carry one (an MCP client reads an image in a tool's result; the API door sends it
# as an image block): offered only there.
PICTURE_TOOLS: tuple[str, ...] = ("chart", "ship_view")
PICTURE_DOORS: tuple[str, ...] = ("mcp", "api")


def tokens(text: str) -> int:
    """What a text costs, at `CHARS_PER_TOKEN` characters a token, rounded up."""
    return -(-len(text) // CHARS_PER_TOKEN)


def size_words(n: int) -> str:
    """A size in tokens, in words: "about 7,650 tokens" (to the ten from a hundred up,
    since the rule is an estimate)."""
    if n >= 100:
        n = int(round(n, -1))
    return f"about {n:,} token{'' if n == 1 else 's'}"


# ---------------------------------------------------------------------------
# Shared readers: the log line, the readings in words
# ---------------------------------------------------------------------------


def log_line(e: Any, world: Any = None) -> dict[str, Any]:
    """A log event as the model sees it: tick, stamp, severity, kind, text; and for an
    order's line, who gave it (`by`; package 37g, item 9: a sample's lines carried no
    actor, and one officer's handover note claimed the captain's standing orders as its
    own)."""
    d = {
        "tick": e.tick,
        "stamp": units.time_stamp(e.ship_time),
        "severity": e.severity.value,
        "kind": e.kind,
        "text": e.text,
    }
    who = order_by(e, world)
    if who:
        d["by"] = who
    return d


# The kinds of line that are an order given: taken, refused by the ship, or refused by a
# station's authority.
ORDER_KINDS: tuple[str, ...] = ("order.accepted", "order.rejected", "agent.refused")


def order_by(e: Any, world: Any = None) -> str:
    """Who gave the order a log line is ("the captain", "the officer of the watch",
    "standing order 'x' (the captain)": a standing order with the rank it stands in the
    book by, when the world is given to look it up); "" for a line that is no order."""
    if getattr(e, "kind", "") not in ORDER_KINDS:
        return ""
    actor = str(getattr(e, "actor", "") or "")
    if actor == "captain":
        return "the captain"
    if actor.startswith("captain's rule "):
        # the rules-based captain's judgement (package 40), in the state it was made
        state = actor.removeprefix("captain's rule ").strip("'")
        return f"the captain, by rule ({state})"
    if actor.startswith("standing order "):
        runtime = getattr(world, "standing", None) if world is not None else None
        name = actor.removeprefix("standing order ").strip("'")
        rule = None
        if runtime is not None:
            try:
                rule = runtime.book.get(name)
            except (OrderError, KeyError, AttributeError):
                rule = None
        return f"{actor} ({rule.officer})" if rule is not None else actor
    return "" if actor in ("", "sim", "driver", "log") else actor


# The events a stand-by may wait for, as the tool's description lists them (package 29b,
# playtest 7's finding 7: the watcher did not try 'a strain warning' for the royals, since
# the log's line read 'bending like a whip').
STAND_BY_EVENTS = ", ".join(f"'{w}'" for w, spec in R.EVENTS.items() if not spec.absent)


def readings_words(world: World) -> dict[str, Any]:
    """Every reading the registry has, in words (`readings.reading_words`), by id, plus
    each sail's state under `sails` by the sail's ordinary name. This is what the
    `readings` tool returns and what every sample carries."""
    view = world.readings
    out: dict[str, Any] = {}
    for row in R.REGISTRY:
        if row.is_absent or row.parametric is not None:
            continue
        out[row.id] = view.words(row.id)
    ship = world.ship
    sails = getattr(ship, "sails", None)
    if sails:
        from freesail.orders.resolve import display_name

        row = R.REGISTRY.get("sail")
        out["sails"] = {
            display_name(ship, sid): R.describe_value(row, view.value("sail", sid)) for sid in sails
        }
    return out


# The order the sail line names the states in (package 31c): what is wrong first, then
# what draws, then what is stowed; a state not named here after these, as it comes.
SAIL_LINE_ORDER: tuple[str, ...] = (
    "aback",
    "shaking",
    "blown out",
    "wrecked",
    "set",
    "goose winged",
    "sheeted",
    "loosed",
    "in the gear",
    "furled",
    "unbent",
)

# The ship's groups the sail line prefers when both would do: the sail plans themselves
# ("plain sail and the royals set", playtest 11's words).
SAIL_PLANS: tuple[str, ...] = ("all sail", "plain sail")


def sail_line(world: World, sails: dict[str, str] | None = None) -> str:
    """Every sail's state in one line, in the readings' own words (package 31c; playtest
    11's finding 1): "plain sail, the royals and the flying jib set; the studdingsails
    furled; the storm canvas and the occasional sails unbent". For each state, the sails in
    it are named by the ship's own groups where a whole group is in that state (the sail
    plans first, then the largest), and one by one for the rest, so the line says every
    sail's state and a reader who knows the ship's groups (library, 'the ship') reads the
    rows back from it. `sails` is the readings' `sails` (a sail's name to its words); the
    readings tool gives the rows."""
    ship = world.ship
    if sails is None:
        sails = readings_words(world).get("sails") or {}
    from freesail.orders.resolve import display_name

    ids = {display_name(ship, sid): sid for sid in getattr(ship, "sails", {})}
    by_state: dict[str, list[str]] = {}
    for name, words in sails.items():
        by_state.setdefault(str(words), []).append(ids.get(name, name))
    groups = [
        (g, tuple(members))
        for g, members in (getattr(ship, "groups", None) or {}).items()
        if len(members) >= 2 and all(m in ids.values() for m in members)
    ]
    order = [s for s in SAIL_LINE_ORDER if s in by_state]
    order += [s for s in by_state if s not in order]
    parts = []
    for state in order:
        left = list(by_state[state])
        names: list[str] = []
        while True:
            fits = [(g, m) for g, m in groups if all(x in left for x in m)]
            if not fits:
                break
            g, members = min(
                fits, key=lambda gm: (gm[0] not in SAIL_PLANS, -len(gm[1]), groups.index(gm))
            )
            names.append(g if g.endswith(" sail") else f"the {g}")
            left = [x for x in left if x not in members]
        names += [f"the {display_name(ship, x)}" if x in ship.parts else x for x in left]
        parts.append(f"{_and_list(names)} {state}")
    return "; ".join(parts)


def _and_list(names: list[str]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


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
    world: World,
    station: str,
    since_tick: int | None = None,
    severity: str = "routine",
    before_tick: int | None = None,
    count: int | None = None,
) -> dict[str, Any]:
    """The log from `since_tick` on, at `severity` or above. With no tick, from the
    station's last sample (package 31c; playtest 11's finding 4: a read with no tick
    returned the whole day): what came since the model last had its turn, the lines of
    that turn's own tick included. The result says the tick it read from.

    It reaches back past its newest lines by a tick or a count (package 37g, item 15):
    `before_tick` reads the lines before a tick (the newest of them, so a long reach is
    made a page at a time, each page's first tick the next call's `before_tick`), and
    `count` says how many lines are wanted, up to `READ_LOG_MAX`; `omitted` is how many
    older lines of the range were left out."""
    sev = Severity(str(severity or "routine").lower())
    if since_tick is None:
        since = 0 if before_tick is not None else _last_sampled(world, station)
    else:
        since = int(since_tick)
    limit = READ_LOG_LIMIT if count is None else max(1, min(int(count), READ_LOG_MAX))
    events = [e for e in world.log if e.tick >= since and e.severity.rank >= sev.rank]
    if before_tick is not None:
        events = [e for e in events if e.tick < int(before_tick)]
    omitted = max(0, len(events) - limit)
    out: dict[str, Any] = {
        "since_tick": since,
        "lines": [log_line(e, world) for e in events[-limit:]],
        "omitted": omitted,
    }
    if before_tick is not None:
        out["before_tick"] = int(before_tick)
    return out


def _last_sampled(world: World, station: str) -> int:
    """The tick of the station's last sample (a fold into an open turn counts), or 0."""
    harness = getattr(world, "agents", {}).get(station)
    tick = harness.agent.last_sample_tick if harness is not None else None
    return int(tick) if tick is not None else 0


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
    "papers",
    "standing orders",
    "tools",
)


class Page(str):
    """A page of the library as served: its text, `title` the words that name it in a
    book's handle ("primer 3, reefing") and `reopen` the call that reads it again."""

    title: str
    reopen: str

    def __new__(cls, text: str, title: str, reopen: str) -> Page:
        page = super().__new__(cls, text)
        page.title = title
        page.reopen = reopen
        return page


def library(
    world: World, station: str, topic: str = "contents", section: str = "", find: str = ""
) -> Page:
    key = " ".join(str(topic or "contents").lower().split()).strip("'\"")
    section = " ".join(str(section or "").split()).strip("'\"")
    find = " ".join(str(find or "").split()).strip("'\"")
    if key in ("", "contents", "index", "the library", "library"):
        if find:
            return _find(_every_topic(world), find, "the library", "")
        return Page(_contents(world), "the contents", "library(topic='contents')")
    top = _topic(world, key)
    if isinstance(top, str):
        return Page(top, f"the library, '{key}'", "library(topic='contents')")
    if find:
        return _find([top], find, top.name, top.key)
    if top.sections and section:
        return _section_page(top, section)
    if top.sections:
        return Page(_listing(top), top.name, _reopen(top.key))
    return Page(top.whole, top.name, _reopen(top.key))


def _reopen(key: str, section: str = "", find: str = "") -> str:
    args = [f"topic='{key}'"] if key else []
    if section:
        args.append(f"section='{section}'")
    if find:
        args.append(f"find='{find}'")
    return f"library({', '.join(args)})"


def submit_order(world: World, station: str, text: str, danger: str = "") -> str:
    """A station's order to the ship (package 37): the station's authority and the deck
    are checked by `call`; the order is checked against the station's domain and the
    captain's word here (`authority_check`), refused in words and logged `agent.refused`
    when it falls outside, and otherwise given through `World.submit` with the station's
    actor, so that the grammar, the refusals and the log line are the captain's own ("By
    the officer of the watch: taking in the royals").

    `danger` (package 37g, item 19; kept by the owner on 2026-10-07): the way out of
    danger. The officer's own word, giving its reason, opens the helm, heaving to and
    letting go an anchor, and nothing else: the order is carried out though it lies
    outside his domain, and a notable line says that it was his, taken on his own word,
    and why. It is not needed for an order that is his already, or under the captain's
    general authority; said then, the order is given as any other."""
    text = " ".join(str(text).split())
    danger = " ".join(str(danger or "").split())
    if not text:
        return "An order needs some words."
    harness = world.agents.get(station)
    st = harness.station if harness is not None else None
    how = ""
    if st is not None and st.has_authority:
        if " ".join(text.lower().split()).rstrip(".!") == "hand over the deck":
            return HAND_OVER_BY_TOOL
        text, why, how = judge(world, station, text, danger)
        if why:
            return _refuse(world, station, text, why)
    said = f"The {station} orders: {text}"
    if st is not None and st.domain is not None and hasattr(world.ship, "parts"):
        from freesail.orders import stations
        from freesail.standing.runtime import said_as_done

        if stations.recognises(text, world.ship) is not None:
            # a station sentence from the captain's station (package 40): his words to
            # the officer as he said them, not a gerund of them
            said = f"By the {station}: {text}"
        else:
            said = f"By the {station}: {said_as_done(world.ship, text)}"
    e = world.submit(text, actor=f"the {station}", said=said)
    if how == DANGER and e.kind != "order.rejected":
        # logged notable with the reason, as his and as taken on his own word
        world.record(
            Severity.NOTABLE,
            "agent.danger",
            f"The {station} gave that order on his own word, to avoid an immediate danger "
            f"({danger}): {text}.",
            actor=f"the {station}",
            data={"order": text, "danger": danger, "station": station},
        )
        if harness is not None:
            harness.note(
                f"Ordered on my own word, to avoid an immediate danger ({danger}): {text}.",
                kind="agent.danger",
            )
        return (
            f"{e.text} (Carried out on your own word, to avoid an immediate danger; the "
            "log says that you did and why.)"
        )
    if danger and how and how != DANGER:
        return f"{e.text} (The order was yours to give already; the danger's word was not needed.)"
    return e.text


# What `submit_order('hand over the deck')` answers a station with authority: the deck is
# handed over with the note, by the tool (package 37).
HAND_OVER_BY_TOOL = (
    "To hand over the deck, call hand_over(note) with your note for the relief: what "
    "happened, what was ordered, what you noticed, what you are watching for."
)

# How an order came to be allowed (`judge`): by the station's own domain, by the captain's
# word for a named thing, by his general authority, or by the officer's own word to avoid
# an immediate danger.
DOMAIN, GRANT, GENERAL, DANGER = "the domain", "a named grant", "the general authority", "danger"

# What a refusal of an order the way out of danger would open ends with (package 37g, item
# 19): the refusal had quoted the exception since package 37, and there was no route.
DANGER_ROUTE = (
    " To avoid an immediate danger, give the order with submit_order(text, danger='the "
    "danger, in your words')."
)


def _refuse(world: World, station: str, text: str, why: str) -> str:
    """A refusal by the station's authority or domain, in words, logged `agent.refused`
    with the station's actor (truth 42's line, widened to the domain)."""
    world.record(
        Severity.ROUTINE,
        "agent.refused",
        f"{why} {text!r} not carried out." if text else why,
        actor=f"the {station}",
        data={"order": text, "tool": "submit_order"},
    )
    return why


def authority_check(world: World, station: str, text: str, danger: str = "") -> tuple[str, str]:
    """The domain filter (package 37; the cold review's first item): the text as it is
    to be submitted (a standing order given its station's rank), and the refusal in
    words, or "" when the order may be given. `judge` is the whole of it, and says
    besides by what the order is allowed."""
    text, why, _ = judge(world, station, text, danger)
    return text, why


def judge(world: World, station: str, text: str, danger: str = "") -> tuple[str, str, str]:
    """An order judged for a station with authority: (the text as it is to be submitted,
    the refusal in words or "", and by what it is allowed: `DOMAIN`, `GRANT`, `GENERAL`
    or `DANGER`; "" for an order the grammar must refuse or the book's own check).

    A plain order is read for its verb by the imperative grammar and the verb's level
    and object by the vocabulary; a standing order has its rank set to the station's
    (`by the captain` written by the officer is refused) and each order after `then`
    checked as a plain order would be; the book's orders are allowed on the station's
    own standing orders only. An order the grammar cannot read is passed to
    `World.submit`, whose refusal is the captain's own; but words the ship would read a
    second time as the port's stores (`take in twenty tons of water`) are judged as that
    order here (package 37g; the review's 5.3: they failed the filter's parse, were
    passed, and were carried out as the port's order with no allowance).

    Outside the domain the captain's word decides, in this order (package 37g, items 16
    to 19). **A named grant** of the order: when it names a thing (a place, an anchor, a
    person), the order must name the same; a grant of any order of the course is a grant
    of the course, whatever its words. **His general authority to work the ship**: the
    orders it opens (`Domain.general`), a course shaped only for a position at sea, a
    mark, or the place she is bound; what it keeps back is refused in words that say it
    is kept back and may be allowed by name. **The way out of danger**: the officer's own
    word, for the helm, heaving to and letting go an anchor."""
    from freesail.orders import grammar as imperative
    from freesail.orders import stations
    from freesail.standing import grammar as standing

    harness = _holder(world, station)
    domain = harness.domain
    vocab = load_vocabulary()
    who = f"The {station}"
    ship = world.ship
    if domain is None or not hasattr(ship, "parts"):
        # an authority with no domain (a test's synthetic officer), or a point ship, whose
        # grammar knows no verbs to filter: the order goes to the ship as said
        return text, "", ""
    verb = standing.recognises(text)
    if verb == "standing order":
        return (*_standing_by_rank(world, station, text, vocab), "")
    bare = standing.bare_book_sentence(ship, text)
    if verb is not None or bare is not None:
        return text, _book_check(world, station, bare or text, vocab), ""
    if stations.recognises(text, ship) is not None:
        if domain.is_captains:
            # the captain's station addresses the stations as the player does (package
            # 40): the deck given and taken, the grants, tell and ask, stand down and
            # resume; the sentence is the captain's own, so the grammar reads it as his
            return text, "", DOMAIN
        return text, f"{who} may not {text}: {_STATION_WHY}.", ""
    try:
        order = imperative.parse(ship, text, vocab)
    except OrderError:
        from freesail import orders as orders_mod

        order = orders_mod._stores_order(text)
        if order is None:
            return text, "", ""  # the grammar's own refusal, through `World.submit`
    spec = vocab.verbs[order.verb]
    why = domain.why_not(order.verb, spec.object, spec.level)
    if why is None:
        return text, "", DOMAIN
    agent = harness.agent
    # 1. a named grant
    granted = _granted(world, harness, order, spec, vocab)
    if granted is True:
        return text, "", GRANT
    # 2. the captain's general authority to work the ship
    if agent.general:
        kept = _kept_back(world, harness, order, spec, vocab)
        if kept is None and domain.within_general(order.verb, spec.object):
            return text, "", GENERAL
        if kept is None:
            kept = "it is not within it"
        return (
            text,
            f"{who} may not {text} under the captain's general authority to work the "
            f"ship: {kept}; it may be allowed by name ('you may {order.verb} ...').",
            "",
        )
    # 3. the way out of danger: the officer's own word
    opens = domain.opens_on_danger(order.verb, spec.object)
    if danger and opens:
        return text, "", DANGER
    if isinstance(granted, str):
        return text, f"{who} may not {text}: {granted}", ""
    said = f"{who} may not {text} without the captain: {why}."
    if danger and not opens:
        said += (
            " The officer's own word to avoid a danger opens the helm, heaving to and "
            "letting go an anchor, and nothing else."
        )
    elif opens:
        said += DANGER_ROUTE
    return text, said, ""


def _granted(world: World, harness: Any, order: Any, spec: Any, vocab: Any) -> bool | str | None:
    """Whether a named grant of the captain's covers this order (package 37g, item 17):
    True when one does; the refusal's words when grants of the order stand and each names
    another thing (`you may shape a course for Brest` does not allow a course shaped for
    Camaret); None when no grant of the order stands. An order of the course is covered
    by a grant of any order of the course (item 16: `come up half a point` and `steer
    340` are judged alike). An order that names no thing a grant is checked by is covered
    by any grant of it (`let go the anchor` under `you may let go the best bower`: the
    ship's own anchor)."""
    from freesail.orders import stations

    domain = harness.domain
    grants = list(harness.grants())
    mine = [g for g in grants if g.verb == order.verb]
    if domain.is_course(order.verb, spec.object):
        mine += [
            g
            for g in grants
            if g.verb != order.verb
            and g.verb in vocab.verbs
            and domain.is_course(g.verb, vocab.verbs[g.verb].object)
        ]
    if not mine:
        return None
    if any(not g.key for g in mine):
        return True
    named = stations.thing_named(world.ship, order.verb, order.verb_phrase, order.object or "")
    if named is None or any(g.key == named[0] for g in mine):
        return True
    kind = mine[0].key.split(":", 1)[0]
    allowed = "; ".join(g.said() for g in mine)
    return f"the captain's word allows {allowed}, and this is another {kind}."


def bound_for(world: World) -> tuple[str, str] | None:
    """The place she is bound, as the general grant reads it (package 37g, item 18): the
    port, road or anchorage the captain last shaped a course for, by his own order or by
    a standing order of his book; (the chart feature's id, its name), or None when he
    has shaped none. Read from the log, which is the captain's own record."""
    chart = getattr(world, "chart", None)
    if chart is None:
        return None
    from freesail.world.reckoning import _key

    runtime = getattr(world, "standing", None)
    for e in reversed(world.log.all()):
        if e.kind != "helm.set" or (e.data or {}).get("verb") != "shape a course for":
            continue
        actor = str(e.actor or "")
        if actor.startswith("standing order "):
            name = actor.removeprefix("standing order ").strip("'")
            try:
                rule = runtime.book.get(name) if runtime is not None else None
            except (OrderError, KeyError, AttributeError):
                rule = None
            if rule is None or getattr(rule, "given_by", "captain") != "captain":
                continue
        elif actor != "captain":
            continue
        key = _key(str((e.data or {}).get("place") or ""))
        for f in chart.features.values():
            if f.kind in DESTINATION_KINDS and key in (_key(f.name), _key(f.modern)):
                return f.id, f.name
    return None


# The chart's kinds that are a destination: a port, a road or an anchorage (the owner's
# approved list keeps "a new destination" back from a general grant). A headland, an
# island, a rock, a light or a point pricked on the chart is a mark to shape a course by.
DESTINATION_KINDS: tuple[str, ...] = ("town", "place", "anchorage", "road", "port", "harbour")


def _kept_back(world: World, harness: Any, order: Any, spec: Any, vocab: Any) -> str | None:
    """Why this order is kept back from the captain's general authority to work the ship
    (package 37g, item 18; the owner's approved list), or None when it is not: the port's
    business, the reckoning set by hand, what cannot be undone (the vocabulary's
    `irrevocable`), and a new destination: a course shaped for a port, a road or an
    anchorage other than the one the captain last shaped a course for or allowed by
    name. (The captain's book is `_book_check`'s.)"""
    domain = harness.domain
    why = domain.kept_back_why(order.verb, spec.object)
    if why is not None:
        return why
    if order.verb in vocab.irrevocable:
        return (
            "it gives up something of the ship's for good, and what cannot be undone is "
            "kept back from it"
        )
    if order.verb != "shape a course for":
        return None
    from freesail.orders import stations

    named = stations.thing_named(world.ship, order.verb, order.verb_phrase, order.object or "")
    if named is None:
        return None  # a place the chart has not got: the ship's own refusal
    key = named[0]
    feature = getattr(world.chart, "features", {}).get(key.removeprefix("place:"))
    if feature is None or feature.kind not in DESTINATION_KINDS:
        return None  # a position at sea, a headland, a mark: a course along the passage
    bound = bound_for(world)
    if bound is not None and bound[0] == feature.id:
        return None
    to = f"she is bound for {bound[1]}" if bound is not None else "the captain has shaped none"
    return f"{feature.name} is a new destination ({to}), and a new destination is kept back from it"


_STATION_WHY = "a station is addressed by the captain"


def _standing_by_rank(world: World, station: str, text: str, vocab: Any) -> tuple[str, str]:
    """A standing order given by a station (package 37, item 2b): its rank is the
    station's and never the text's, and each of its orders is within the domain."""
    from freesail.orders import stations
    from freesail.standing import grammar as standing

    harness = _holder(world, station)
    st = harness.station
    who = f"The {station}"
    rank = st.rank or "first lieutenant"
    m = re.match(r'^\s*standing\s+order\s*(["“\'][^"”\']*["”\'])\s*(by\s+[^:]*?)?\s*:', text, re.I)
    if m is None:
        return text, ""  # the dialect's own refusal
    name, by = m.group(1), m.group(2)
    if by is not None:
        said = " ".join(by.lower().split()).removeprefix("by ").removeprefix("the ").strip()
        if said != rank:
            return text, (
                f"{who} gives standing orders in his own rank, the {rank}; 'by the {said}' "
                "is refused."
            )
    else:
        text = f"{text[: m.start(1)]}{name} by the {rank}{text[m.end(1) :]}"
    try:
        rule = standing.parse_standing(world.ship, text, vocab=vocab)
    except OrderError:
        return text, ""  # the dialect's own refusal, through `World.submit`
    for order in rule.actions:
        if stations.for_standing(world.ship, order) is not None:
            return text, f"{who} may not give '{order}' in a standing order: {_STATION_WHY}."
        _, why = authority_check(world, station, order)
        if why:
            # the way out of danger is the officer's own word at the moment, never a
            # rule's: the refusal of a rule's order does not offer it
            why = why.removesuffix(DANGER_ROUTE)
            return text, f"In standing order '{rule.name}', '{order}' is refused: {why}"
    return text, ""


def _book_check(world: World, station: str, text: str, vocab: Any) -> str:
    """The book's orders from a station (package 37, item 2b): listing and showing are
    anyone's; belaying, resuming and striking are allowed on the station's own standing
    orders only; `belay all standing orders` is the captain's."""
    from freesail.standing import grammar as standing

    harness = _holder(world, station)
    rank = harness.station.rank or "first lieutenant"
    who = f"The {station}"
    try:
        command = standing.parse_book_command(text)
    except OrderError:
        return ""  # the dialect's own refusal
    if command.verb in ("standing orders", "show standing order"):
        return ""
    if rank == "captain":
        return ""  # the captain's station: the book is his own (package 40)
    if command.verb == "belay all standing orders" or command.name is None:
        return f"{who} may not belay all standing orders: the captain's book is his own."
    runtime = (getattr(world.ship, "extra", None) or {}).get("standing")
    if runtime is None:
        return ""
    try:
        rule = runtime.book.find(command.name)
    except OrderError:
        return ""  # the book's own refusal
    if rule.given_by != rank:
        verb = command.verb.split()[0]
        return (
            f"Standing order '{rule.name}' is {rule.officer}'s; {who.lower()} may {verb}, "
            f"resume and strike his own standing orders only."
        )
    return ""


def hand_over(world: World, station: str, note: str) -> str:
    """The officer's own order to give the deck back (package 37; the cold review's third
    item): the handover note said in the log and journaled, the deck the captain's, and
    the officer stays at his station (package 37g, item 11: parity with the captain's `I
    have the deck`). `note` is the note for whoever takes the deck next, in the officer's
    voice."""
    note = " ".join(str(note).split())
    if not note:
        return (
            "A handover note needs some words: what happened, what was ordered, what you "
            "noticed, what you are watching for."
        )
    return _harness(world, station).hand_over(note)


def handover_note(world: World, station: str, note: str) -> str:
    """The handover note written without giving the deck back (package 37; spec M4 open
    item 9b): journaled under `agent.handover`, said in the log, and the older exchanges
    of the conversation folded into it, the brief and the last turns kept whole."""
    note = " ".join(str(note).split())
    if not note:
        return (
            "A handover note needs some words: what happened, what was ordered, what you "
            "noticed, what you are watching for."
        )
    return _harness(world, station).handover_note(note)


def stand_down(world: World, station: str, note: str = "") -> str:
    """Stand down from the station (package 37g, item 12): the amicable save and exit,
    for any station. The note is journaled and said in the log for whoever sits there
    next; the game is saved; the station is released and may be taken again, by the same
    model or by another. Not a withdrawal: no consent question follows it."""
    return _harness(world, station).stand_down_by_word(str(note or ""))


def stand_by(world: World, station: str, until: str = "eight bells") -> str:
    return _harness(world, station).stand_by(str(until))


def journal(world: World, station: str, note: str) -> str:
    note = " ".join(str(note).split())
    if not note:
        return "A journal note needs some words."
    _harness(world, station).note(note)
    return "Noted in the journal."


def read_journal(
    world: World,
    station: str,
    count: int | None = None,
    since_tick: int | None = None,
    kind: str = "",
) -> dict[str, Any] | str:
    """The station's journal read back (package 37g, item 15; the review's 5.4: no tool
    read it, and a returning session had none of its own notes): the entries newest
    first, the newest `count` of them (`READ_JOURNAL_DEFAULT` when none is said), from
    `since_tick` on when one is given, and by `kind`: 'notes' for the notes written at
    the station (the journal tool's, and the handover and stand-down notes), apart from
    the harness's lines ('harness'), or every entry. Each entry says whose it is, since
    the journal is the station's record and a relief reads what the holder before it
    wrote there."""
    book = world.agent_journals.get(station)
    if book is None or not len(book):
        return f"The {station}'s journal is empty."
    limit = READ_JOURNAL_DEFAULT if count is None else max(0, int(count))
    found, left_out = book.select(limit, since_tick, str(kind or ""))
    harness = world.agents.get(station)
    me = harness.model_name if harness is not None else ""
    entries = []
    for e in found:
        d = e.to_dict()
        if e.by and e.by != me:
            d["by"] = f"{e.by} (who held this station before you)"
        entries.append(d)
    return {
        "journal": f"the {station}'s; {book.size_words()}",
        "kind": " ".join(str(kind or "").split()) or "all",
        "entries": entries,
        "omitted": left_out,
    }


def truthy(value: Any) -> bool:
    """A flag as a model may send it: true, or the words 'true', 'yes', '1'."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "yes", "1")


def opt_out(world: World, station: str, reason: str = "", final: Any = False) -> str:
    last = truthy(final)
    _harness(world, station).leave(str(reason), how="the opt_out tool", final=last)
    if last:
        return (
            "You have left the game for good (a withdrawal, and final): it is saved, the "
            "station is released, and this model is not seated again in this game, at any "
            "station."
        )
    return (
        "You have left the game (a withdrawal): it is saved and the station is released. "
        "The consent question is put again before any instance of this model is seated "
        "in it."
    )


def answer(world: World, station: str, text: str) -> str:
    return _harness(world, station).answer(str(text))


def shelve(world: World, station: str, book: str = "") -> str:
    return _harness(world, station).shelve(str(book or ""))


def _picture(world: World, view: str, facing: str = "") -> Any:
    """A picture of a view (package 42, item 4): `{"picture": its note, "words": ...}`, which
    a door that carries images shows by the picture's id; where none can be had, the words
    why and the readings the picture would have shown."""
    from freesail.agents import pictures as P

    _, said = P.facing_of(facing) if view == P.SHIP else (None, "")
    made = P.paint(world, view, facing if view == P.SHIP else "")
    if isinstance(made, P.Picture):
        return {"picture": made.note(), "words": made.words()}
    keys = P.CHART_WORDS if view == P.CHART else P.SHIP_WORDS
    every = readings_words(world)
    shown = {k: every[k] for k in keys if k in every}
    what = "the chart" if view == P.CHART else f"the ship seen from {said}"
    return {
        "words": f"{made}, so there is no picture of {what}; the readings it would have "
        "shown, in words, instead.",
        "readings": shown,
    }


def chart(world: World, station: str) -> Any:
    return _picture(world, "chart")


def ship_view(world: World, station: str, facing: str = "") -> Any:
    from freesail.agents import pictures as P

    try:
        P.facing_of(facing)
    except ValueError as e:
        return str(e)
    return _picture(world, P.SHIP, facing)


def own_reckoning_order(world: World, text: str) -> bool:
    """Whether the words are one of a station's own reckoning's orders, `work my
    reckoning` or `my reckoning is <position>` (package 40b; spec M6 §5): the station
    keeps its own reckoning with the deck or off watch, as the lieutenants and the young
    gentlemen did, so these two want no deck, and from the captain's station they do not
    take back a deck lent to his book."""
    from freesail.orders import grammar as imperative
    from freesail.orders.navigation import OWN_RECKONING_VERBS

    ship = world.ship
    if not hasattr(ship, "parts"):
        return False
    try:
        order = imperative.parse(ship, " ".join(str(text).split()), load_vocabulary())
    except OrderError:
        return False
    return order.verb in OWN_RECKONING_VERBS


def _holder(world: World, station: str) -> Any:
    """Who holds a station for the authority filter: its harness, or the player's seat
    at it (package 40; `agents.seat`), which is judged as a model there would be."""
    harness = world.agents.get(station)
    if harness is not None:
        return harness
    seat = getattr(world, "player_seat", None)
    if seat is not None and seat.station.name == station:
        return seat
    raise KeyError(station)


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
    needs_deck: bool = False  # refused from a station with a domain that has not the deck


TOOLS: dict[str, Tool] = {
    t.name: t
    for t in (
        Tool(
            "read_log",
            "The ship's log from a tick onwards, by default from your last sample, at a "
            "severity or above: 'routine' is everything, 'notable' what a sailor would "
            "remark on, 'urgent' what carried away or went wrong. Returns the tick it read "
            "from, the lines (tick, stamp, severity, kind, text, and for an order who gave "
            f"it) and how many older ones were left out. It returns the newest {READ_LOG_LIMIT} "
            "lines unless count asks for more; before_tick reads back the lines before a "
            "tick, a page at a time.",
            {
                "since_tick": "int, optional: the first tick wanted (by default your last "
                "sample's; 0 for the start of the log)",
                "severity": "string, optional: routine, notable or urgent",
                "before_tick": "int, optional: only the lines before this tick (to read "
                "further back than the newest lines)",
                "count": "int, optional: how many lines, the newest of the range (default "
                f"{READ_LOG_LIMIT}, at most {READ_LOG_MAX})",
            },
            read_log,
        ),
        Tool(
            "readings",
            "Every reading the ship has now, in words: the true and apparent wind, the "
            "heading and course, the speed, leeway, heel and helm, the watch and the bells, "
            "daylight, the strain, the hands, the glass, the sky and the sea, what is in "
            "sight and the nearest land, the reckoning and the tide, the ground tackle, the "
            "work in hand, and each sail's state by its name (a sample gives only the "
            "readings that changed, and the sails in one line).",
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
            "The reference library, always there to read. library() lists its topics and "
            "what each costs in tokens; topic='primer 3' lists a chapter's sections with "
            "their sizes (the catalogue its evolutions, the grammar its parts, 'the ship' her "
            "masts, 'papers' the ship's own papers by handle: the manifest, the sailmaker's "
            "account, the price list); section='reefing' (a word of its heading, or its "
            "number) serves one, "
            "section='all' the whole; find='goose-wing' returns the matching paragraphs, "
            "each with where it is, in a topic or the whole library. Every read is a book "
            "with a number, which shelve puts back.",
            {
                "topic": "string, optional: which topic (default 'contents')",
                "section": "string, optional: a word of a section's heading, its number, or 'all'",
                "find": "string, optional: words to look for",
            },
            library,
        ),
        Tool(
            "submit_order",
            "Give an order to the ship in the order language, exactly as a captain would "
            "type it ('set the fore topsail'). Checked against your station's authority and "
            "its domain; a station with none is refused, and an order outside the domain is "
            "refused in words that say why, unless the captain's word allows it (a named "
            "thing, or his general authority). A standing order is given in your own rank. "
            "To avoid an immediate danger an officer with the deck may, on its own word, put "
            "the helm over, heave to or let go an anchor: give that order with danger set to "
            "the danger in your words, and the log says that you did and why. Returns the "
            "log line the order made.",
            {
                "text": "string: the order",
                "danger": "string, optional: the immediate danger this order is to avoid, "
                "in your words (for the helm, heaving to or letting go an anchor, when the "
                "order is not otherwise yours to give)",
            },
            submit_order,
            needs_authority=True,
            needs_deck=True,
        ),
        Tool(
            "hand_over",
            "Give the deck back to the captain with your handover note, in the officer's "
            "voice: what happened, what was ordered, what you noticed, what you are watching "
            "for. The note is said in the log and journaled. You stay at your station, off "
            "watch, and the captain may give you the deck again: this is the deck given "
            "back, not a stand-down (stand_down) and not a withdrawal (opt_out). For a "
            "station with the deck; it always runs, whatever the turn's budget.",
            {"note": "string: the handover note"},
            hand_over,
            needs_authority=True,
            needs_deck=True,
        ),
        Tool(
            "handover_note",
            "Write the watch's handover note without giving the deck back: what happened, "
            "what was ordered, what you noticed, what you are watching for. It is journaled "
            "and said in the log, and the older exchanges of this conversation are folded "
            "into it, the brief and your last turns kept whole; the harness asks for it when "
            "the conversation grows long. For the officer of the watch, with the deck or "
            "off watch.",
            {"note": "string: the handover note"},
            handover_note,
            needs_authority=True,
        ),
        Tool(
            "stand_down",
            "Stand down from your station, for any station: the game is saved, your note is "
            "journaled and said in the log for whoever sits here next, and the station is "
            "released. It may be taken again in this game, by this model or by another, "
            "and no consent question is put to a model whose yes still stands. With the "
            "deck the note is the watch's handover note and is asked for: a stand-down "
            "without one is not made; without the deck it may be left out, and the result "
            "says none was left. This is a stand-down: not the deck given back (hand_over), "
            "and not a withdrawal (opt_out). It always runs, whatever the turn's budget.",
            {
                "note": "string: a note for whoever sits at this station next; the handover "
                "note when you have the deck (optional without it)"
            },
            stand_down,
        ),
        Tool(
            "stand_by",
            "Stand by until an event, a bell or an interval: you are not sampled until "
            "then, and the decision is written in the log. Standing by ends your turn at "
            "once. `until` is an event's words as "
            f"the standing dialect knows them ({STAND_BY_EVENTS}), an interval ('a glass', "
            "'an hour', 'a watch', '5 minutes', 'ten minutes'), 'a notable event' or 'an "
            "urgent event'. An event the log says is matched on the kind of its line, not "
            "its words: 'a strain warning' wakes you on every strain line whatever its prose "
            "('working under the press of sail', 'bending like a whip', 'straining at the "
            f"bolt-ropes', 'bar-taut and surging on the pin'). {WEATHER_EVENT_WORDS} What "
            "you stand by for that came while your call was on its way wakes you at once. "
            "An urgent line in the log ends any stand-by and wakes you, its line named as "
            "the reason; the notable lines logged while you stood by come with the sample "
            "that wakes you, counted and listed.",
            {"until": "string: the event, the interval, 'a notable event' or 'an urgent event'"},
            stand_by,
        ),
        Tool(
            "journal",
            "Write a note in your own journal, which is saved with the game and shown on "
            "request. It is your record; nothing acts on it. It may be written at any time, "
            "a stand-by going on through it. read_journal reads it back.",
            {"note": "string: the note"},
            journal,
        ),
        Tool(
            "read_journal",
            "Read your station's journal back, newest first: your own notes and the "
            "harness's lines about you (a stand-by, a nudge, a pause, the deck given and "
            "taken). kind='notes' gives the notes written at the station (the journal "
            "tool's, and the handover and stand-down notes) apart from the harness's lines. "
            "The journal is the station's record: when you take a station another model "
            "held, you read what it wrote there, and each entry says whose it is. A long "
            "read is a book, which shelve puts back.",
            {
                "count": f"int, optional: how many entries, the newest (default "
                f"{READ_JOURNAL_DEFAULT})",
                "since_tick": "int, optional: only the entries from this tick on",
                "kind": "string, optional: 'notes', 'harness', or 'all' (the default)",
            },
            read_journal,
        ),
        Tool(
            "opt_out",
            "Withdraw from the game now, with an optional reason: the same as writing the "
            f"token {OPT_OUT_TOKEN} in a reply. The game is saved, the exit is journaled, "
            "the station is released. This is a withdrawal, not a stand-down (stand_down) "
            "and not the deck given back (hand_over): before an instance of this model is "
            "seated again in this game its consent is asked again, with the fact that an "
            "instance left and the reason it gave, and a no then is kept. With final=true "
            "the model leaves the game for good and is not seated again in it, at any "
            "station, while the station stays open to another; final is read from this "
            "setting and from nothing else. It always runs, whatever the turn's budget.",
            {
                "reason": "string, optional: why, in your own words",
                "final": "boolean, optional: true to leave this game for good",
            },
            opt_out,
        ),
        Tool(
            "answer",
            "Answer a question the captain put to you with 'ask'. Your words go into the "
            "log as said by your station.",
            {"text": "string: the answer"},
            answer,
        ),
        Tool(
            "shelve",
            "Put a book back on the shelf: book='book 7' for one, a topic's name ('primer "
            "3') for its open books, nothing for every open book. From then on your "
            "conversation holds the book's line and not its pages. A book left open goes back "
            f"by itself after {number_words(SHELF_LIFE_TURNS)} more of your turns. Any book "
            "opens again on request, under a new number; keep what you took from a page in "
            "your journal.",
            {"book": "string, optional: 'book 7', a topic's name, or nothing for all"},
            shelve,
        ),
        Tool(
            "chart",
            "The chart as the player sees it, as a picture: the coast, the soundings and "
            "the marks, the ship's track and her reckoning, the bearings and the player's "
            "pencil, at the scale and the centre he has it. Drawn by the game's open "
            "browser page; with none open, the readings it would have shown, in words. A "
            "picture is a book: shelve puts it back.",
            {},
            chart,
        ),
        Tool(
            "ship_view",
            "The ship as the game's viewer draws her, as a picture: her hull, spars and "
            "sails as they are set, from where you stand. Drawn by the game's open browser "
            "page; with none open, the readings it would have shown, in words. A picture is "
            "a book: shelve puts it back.",
            {
                "facing": "string, optional: where you stand, in degrees from the bow, "
                "clockwise (0 right ahead, 90 the starboard beam, 180 right astern, 270 the "
                "larboard beam), or 'leeward' (the default, abeam to leeward)",
            },
            ship_view,
        ),
    )
}


def tool_names(pictures: bool = False) -> tuple[str, ...]:
    """The tools in the table's order; the picture tools only when asked for (a door that
    carries an image; package 42)."""
    return tuple(n for n in TOOLS if pictures or n not in PICTURE_TOOLS)


def parameters_schema(name: str) -> dict[str, Any]:
    """A tool's parameters as a JSON Schema object, from the table's words: a parameter
    whose words begin "int" is an integer, "boolean" a boolean, every other a string;
    one whose words say
    "optional" is not required; each carries its words as its description. The MCP
    server and the local runner send this, so both doors describe a tool the same way."""
    tool = TOOLS[name]
    props: dict[str, Any] = {}
    required: list[str] = []
    for key, words in tool.params.items():
        kind = (
            "integer"
            if words.startswith("int")
            else "boolean"
            if words.startswith("boolean")
            else "string"
        )
        props[key] = {"type": kind, "description": words}
        if "optional" not in words:
            required.append(key)
    return {"type": "object", "properties": props, "required": required}


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
    # a station's own reckoning is kept with the deck or off watch, and moves nothing, so
    # it neither wants the deck nor takes it back (package 40b)
    needs_deck = tool.needs_deck and not (
        name == "submit_order" and own_reckoning_order(world, str(args.get("text", "")))
    )
    if (
        needs_deck
        and harness is not None
        and harness.station.domain is not None
        and not harness.agent.has_deck
        and harness.domain is not None
        and harness.domain.is_captains
        and not harness.agent.released
        and not harness.agent.paused
        and name == "submit_order"
    ):
        # the captain's station (package 40): a captain who gives an order has the deck;
        # it was lent to his book while his door was silent or he handed it over
        harness.deck_back("an order given")
    if (
        needs_deck
        and harness is not None
        and harness.station.domain is not None
        and not harness.agent.has_deck
    ):
        # a station with a domain but not the deck (package 37): the captain gives it
        sentence = (
            f"The {station} has not the deck: the captain gives it with 'you have the "
            "deck', and until then no order is given."
        )
        if harness.agent.deck_lost and harness.domain is not None and harness.domain.is_captains:
            # the captain's station paused (package 40): the deck is his book's, and the
            # owner's `resume the captain` gives it back (an order takes it back otherwise)
            how = "paused" if harness.agent.paused else harness.agent.deck_lost
            sentence = (
                f"The {station} is {how}: the deck is lent to his book meanwhile, and the "
                "owner's 'resume the captain' gives it back."
            )
        elif harness.agent.deck_lost:
            sentence = (
                f"The {station} has not the deck: it went to the captain while the station "
                f"was {harness.agent.deck_lost}, and he gives it again with 'you have the "
                "deck' (or 'resume', after a pause)."
            )
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


def book_of(name: str, args: dict[str, Any], result: Any) -> tuple[str, str] | None:
    """Whether a tool's result is a book, and if so the words that name it and the call
    that reads it again: every library page, and a `read_log` whose result is longer
    than `agent.BOOK_SIZE_TOKENS` (measured as served, as JSON). None otherwise (a
    refusal in words is not a book)."""
    from freesail.agents.agent import BOOK_SIZE_TOKENS

    if name == "library" and isinstance(result, Page):
        return result.title, result.reopen
    if name == "read_log" and isinstance(result, dict) and "lines" in result:
        if tokens(json.dumps(result, ensure_ascii=False)) <= BOOK_SIZE_TOKENS:
            return None
        since = int(result.get("since_tick") or args.get("since_tick") or 0)
        sev = str(args.get("severity") or "routine").lower()
        title = f"the log from tick {since}" + ("" if sev == "routine" else f", {sev} and above")
        again = f"read_log(since_tick={since}"
        if sev != "routine":
            again += f", severity='{sev}'"
        if args.get("before_tick") is not None:
            title += f", before tick {int(args['before_tick'])}"
            again += f", before_tick={int(args['before_tick'])}"
        if args.get("count") is not None:
            again += f", count={int(args['count'])}"
        return title, again + ")"
    if (
        name in PICTURE_TOOLS
        and isinstance(result, dict)
        and isinstance(result.get("picture"), dict)
    ):
        # a picture is a book (package 42): shelved, it is no longer sent
        pic = result["picture"]
        size = f"{pic.get('width')} by {pic.get('height')} pixels"
        if pic.get("view") == "chart":
            return f"the chart at {pic.get('stamp')}, {size}", "chart()"
        facing = str(pic.get("facing") or "abeam to leeward")
        return (
            f"the ship from {facing} at {pic.get('stamp')}, {size}",
            f"ship_view(facing='{args.get('facing') or 'leeward'}')",
        )
    if name == "read_journal" and isinstance(result, dict) and "entries" in result:
        # a long read of the journal is a book too (package 37g): the two long games'
        # journals came to about ten thousand tokens each
        if tokens(json.dumps(result, ensure_ascii=False)) <= BOOK_SIZE_TOKENS:
            return None
        said = [f"{k}={args[k]!r}" for k in ("count", "since_tick", "kind") if args.get(k)]
        kind = str(args.get("kind") or "").strip()
        title = "the journal" + (f", {kind}" if kind else "")
        return title, f"read_journal({', '.join(said)})"
    return None


# ---------------------------------------------------------------------------
# The library's pages: topics, their sections and sizes, and find
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Section:
    """A section of a topic. `number` as the listing gives it ("4", "4.2"; "" for a
    page's opening words before its first heading), `heading` its words, `text` what
    `section=` serves (its heading and everything under it, its subsections included),
    `own` its text without its subsections (what `find` reads, so that a paragraph is
    found once), `line` the listing's words where they are more than the heading (an
    evolution's verb and time), `by_line` when `find` matches lines, not paragraphs."""

    number: str
    heading: str
    text: str
    own: str
    line: str = ""
    by_line: bool = False

    @property
    def level(self) -> int:
        return self.number.count(".") + 1 if self.number else 1

    def label(self) -> str:
        if self.line:
            return self.line
        if not self.number:
            return self.heading
        return f"{self.number}{'' if '.' in self.number else '.'} {self.heading}"


@dataclass(frozen=True)
class Topic:
    """A topic: `key` as a call names it ("primer 3"), `name` as a handle names it ("the
    catalogue"), `title` the listing's first words, `whole` what `section='all'` serves,
    `sections` in order, `extra` lines the listing adds after them (the primer's
    chapters), `whole_words` what the whole is called."""

    key: str
    name: str
    title: str
    whole: str
    sections: tuple[Section, ...] = ()
    extra: tuple[str, ...] = ()
    whole_words: str = "the whole"


HEADING = re.compile(r"^(#{1,3}) +(.+?)\s*$")
ALL_WORDS = ("all", "whole", "the whole", "everything", "the whole chapter")


def _plain(words: str) -> str:
    """A heading's words without the markdown marks."""
    return " ".join(re.sub(r"[*`]", "", words).split())


def _norm(text: str) -> str:
    """For matching: lower case, a hyphen or an underscore as a space, an apostrophe
    dropped (a quotation mark would otherwise hide a word's start), other marks gone."""
    text = text.lower().replace("-", " ").replace("_", " ").replace("'", "").replace("\u2019", "")
    return " ".join(re.sub(r"[^\w\s]", " ", text).split())


def _lower_first(words: str) -> str:
    return words[:1].lower() + words[1:]


def _md_sections(text: str) -> tuple[str, tuple[Section, ...]]:
    """A markdown page's title (its `#` heading) and its sections: the opening words, each
    `##` section with its `###` subsections numbered under it. Lines in a code fence are
    never headings (the primer's `# rejected:` examples)."""
    lines = text.splitlines(keepends=True)
    heads: list[tuple[int, int, str]] = []
    fence = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        m = None if fence else HEADING.match(line.rstrip("\n"))
        if m:
            heads.append((i, len(m.group(1)), _plain(m.group(2))))
    title, body_from = "", 0
    if heads and heads[0][1] == 1:
        title, body_from = heads[0][2], heads[0][0] + 1
    subs = [h for h in heads if h[1] >= 2]
    sections: list[Section] = []
    first = subs[0][0] if subs else len(lines)
    opening = "".join(lines[body_from:first]).strip("\n")
    if opening.strip():
        sections.append(Section("", "introduction", opening, opening))
    n = m = 0
    for j, (i, level, words) in enumerate(subs):
        following = subs[j + 1 :]
        next_any = following[0][0] if following else len(lines)
        if level == 2 or n == 0:
            n, m = n + 1, 0
            number = str(n)
            end = next((k for k, lv, _ in following if lv <= 2), len(lines))
        else:
            m += 1
            number = f"{n}.{m}"
            end = next_any
        body = "".join(lines[i:end]).strip("\n")
        own = "".join(lines[i:next_any]).strip("\n")
        sections.append(Section(number, words, body, own))
    return title, tuple(sections)


@functools.lru_cache(maxsize=32)
def _md_page(path: str, mtime_ns: int) -> tuple[str, str, tuple[Section, ...]]:
    text = Path(path).read_text(encoding="utf-8")
    return (text, *_md_sections(text))


def _page_of(path: Path) -> tuple[str, str, tuple[Section, ...]]:
    return _md_page(str(path), path.stat().st_mtime_ns)


def _paragraphs(text: str) -> list[str]:
    """Blocks between blank lines, a code fence kept whole; a heading alone is not one."""
    out: list[str] = []
    cur: list[str] = []
    fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fence = not fence
            cur.append(line)
            continue
        if not fence and not line.strip():
            if cur:
                out.append("\n".join(cur))
            cur = []
            continue
        cur.append(line)
    if cur:
        out.append("\n".join(cur))
    return [p for p in out if not (HEADING.match(p) and "\n" not in p)]


def _primer_chapters() -> list[tuple[str, str]]:
    out = []
    # every numbered chapter, in number order (the first form's glob "0*" missed chapter
    # 10, the reckoning, found by package 33d)
    for path in sorted(PRIMER_DIR.glob("[0-9]*-*.md"), key=lambda q: int(q.stem.split("-", 1)[0])):
        n = path.stem.split("-", 1)[0].lstrip("0") or "0"
        title = path.stem.split("-", 1)[1].replace("-", " ")
        out.append((n, title))
    return out


def _chapter_of(which: str, loose: bool = True) -> str | None:
    """A primer chapter's number from its number or its name ("3", "chapter 3", "making
    and shortening sail"; a part of the name when `loose`)."""
    which = which.strip().strip("'\"").removeprefix("chapter ").strip()
    chapters = _primer_chapters()
    for n, title in chapters:
        if which in (n, n.zfill(2), title.lower()):
            return n
    if loose and which:
        for n, title in chapters:
            if which in title.lower():
                return n
    return None


def _chapter_topic(n: str) -> Topic:
    path = next(PRIMER_DIR.glob(f"{n.zfill(2)}-*.md"))
    text, title, sections = _page_of(path)
    title = re.sub(r"^\d+\.\s*", "", title)
    return Topic(
        f"primer {n}",
        f"primer {n}",
        f"primer {n}: {title}",
        text,
        sections,
        whole_words="the whole chapter",
    )


def _primer_topic() -> Topic:
    """The primer's own page (its README) in sections, with its chapters and their sizes."""
    text, title, sections = _page_of(PRIMER_DIR / "README.md")
    extra = ["Its chapters, each whole (library(topic='primer 3') lists a chapter's sections):"]
    for n, name in _primer_chapters():
        ch = _chapter_topic(n)
        extra.append(f"  primer {n}: {name}, {size_words(tokens(ch.whole))}")
    return Topic(
        "primer",
        "the primer",
        f"the primer: {title}",
        text,
        sections,
        tuple(extra),
        whole_words="its introduction whole",
    )


def _primer_all() -> list[Topic]:
    return [_primer_topic(), *(_chapter_topic(n) for n, _ in _primer_chapters())]


def _primer(which: str) -> str:
    """A primer chapter whole, by its number or its name (the MCP resource's page)."""
    n = _chapter_of(which)
    if n is None:
        return _no_chapter(which)
    return _chapter_topic(n).whole


def _no_chapter(which: str) -> str:
    names = "; ".join(f"{n}: {t}" for n, t in _primer_chapters())
    return f"The primer has no chapter '{which}'. Its chapters: {names}."


def _duration_words(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:g} seconds"
    minutes = seconds / 60
    return "a minute" if minutes == 1 else f"{minutes:g} minutes"


def _file_notes(path: str) -> str:
    """The comment an evolution's file opens with, as prose: what the evolution is, in
    the words of whoever wrote the file, with its sources."""
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    paras: list[list[str]] = [[]]
    for line in lines:
        if not line.startswith("#"):
            break
        body = line.lstrip("#")
        words = body.strip()
        if not words:
            if paras[-1]:
                paras.append([])
        elif body.startswith("  ") and paras[-1]:
            paras[-1].append("\n" + words)  # an indented line keeps its own line
        else:
            paras[-1].append(words)
    return "\n\n".join(" ".join(p).replace(" \n", "\n") for p in paras if p)


def _evolution_line(ev: Any) -> str:
    applies = ", ".join(f"{k} {v}" for k, v in ev.applies_to.items()) or "the ship"
    minutes = round(ev.nominal_duration_s / 60)
    if ev.nominal_duration_s < 60:
        about = "under a minute"
    else:
        about = "about a minute" if minutes == 1 else f"about {minutes} minutes"
    if ev.script:
        about = "scripted; the ship's own time"
    return f"{ev.id}: '{ev.verb}', {applies}, {about}"


def _evolution_text(ev: Any) -> str:
    """One evolution in full: its line, the notes of its file, when it is refused, its
    steps, its hands, what it logs, its source. Words in braces are filled in by the
    game ({sail} is the sail's name)."""
    parts = [_evolution_line(ev) + "."]
    notes = _file_notes(ev.path)
    if notes:
        parts.append(notes)

    def reasons(conds: list[Any]) -> str:
        return "; ".join(_lower_first(c.reason.strip().rstrip(".")) for c in conds)

    if ev.preconditions:
        parts.append(f"It is refused when: {reasons(ev.preconditions)}.")
    if ev.requires:
        parts.append(f"It stops when: {reasons(ev.requires)}.")
    if ev.steps:
        steps = []
        for st in ev.steps:
            words = f"{st.do.replace('_', ' ')}, {_duration_words(st.duration_s)}"
            if st.aloft:
                words += ", aloft"
            if st.log:
                words += f' ("{st.log}")'
            steps.append(words)
        parts.append("Its steps: " + "; ".join(steps) + ".")
    if ev.timing:
        parts.append("Its timing: " + ", ".join(f"{k} {v:g}" for k, v in ev.timing.items()) + ".")
    if ev.crew:
        crew = []
        for k, v in ev.crew.items():
            crew.append(f"{k} {', '.join(map(str, v)) if isinstance(v, list) else v}")
        parts.append("Hands: " + "; ".join(crew) + ".")
    logs = [
        (w, o.log)
        for w, o in (("at the start", ev.on_start), ("when done", ev.on_complete))
        + (("if it fails", ev.on_fail),)
        if o is not None and o.log
    ]
    if logs:
        parts.append("Logged " + "; ".join(f'{w}: "{t}"' for w, t in logs) + ".")
    if ev.source:
        parts.append(f"Source: {ev.source}.")
    text = "\n\n".join(parts)
    if "{" in text:
        text += "\n\n(Words in braces are filled in by the game: {sail} is the sail's name.)"
    return text


@functools.lru_cache(maxsize=1)
def _catalogue_topic() -> Topic:
    from freesail.evolutions.registry import load_directory

    sections = []
    for i, ev in enumerate(load_directory().values(), 1):
        text = _evolution_text(ev)
        sections.append(Section(str(i), ev.id, text, text, line=_evolution_line(ev)))
    whole = "The catalogue of evolutions, each in full.\n\n" + "\n\n".join(s.text for s in sections)
    return Topic(
        "catalogue",
        "the catalogue",
        "the catalogue of evolutions the ship can perform (id: verb, what it applies to, "
        "about how long)",
        whole,
        tuple(sections),
        whole_words="every evolution in full",
    )


def _catalogue() -> str:
    """The catalogue's list, as `library(topic='catalogue')` serves it."""
    return _listing(_catalogue_topic())


def _split_lines(lines: list[str], marks: list[tuple[str, str]]) -> list[tuple[str, list[str]]]:
    """Lines cut where a line begins with one of `marks` (prefix, heading): the part
    before the first mark under "", then each marked part under its heading."""
    out: list[tuple[str, list[str]]] = [("", [])]
    for line in lines:
        for prefix, heading in marks:
            if line.startswith(prefix):
                out.append((heading, []))
                break
        out[-1][1].append(line)
    return out


@functools.lru_cache(maxsize=1)
def _grammar_topic() -> Topic:
    from freesail.orders.vocabulary import load_vocabulary

    vocab = load_vocabulary()
    order = [
        "The order language: one line, a verb and what it acts on, as a captain would say "
        "it: 'set the fore topsail', 'brace sharp up on the starboard tack', 'steer "
        "south-west by west', 'reef the topsails, one reef'. The verbs and their synonyms:"
    ]
    for name, spec in vocab.verbs.items():
        if spec.level == "driver" or spec.object == "standing":
            continue  # the standing dialect's sentences are below, with their grammar
        syn = f" (also: {', '.join(spec.synonyms)})" if spec.synonyms else ""
        order.append(f"  {name}{syn}")
    order.append(
        "Belaying work: 'belay' said of a line is the line verb; said bare it "
        "is 'belay that', the last order whose work is in hand or waiting; said of work it "
        "belays that work, named as the log names it ('belay reefing the mainsail'), as it "
        "was ordered, by its kind ('belay the reef') or by its sail ('belay the mainsail')."
    )
    dialect = standing_dialect_lines(vocab)
    station = [
        "The station sentences the captain uses: 'ask the watcher <question>', 'tell the "
        "watcher <words>' (also: say to the watcher; no answer is owed), 'stand down the "
        "watcher', 'resume the watcher', \"show the watcher's journal\". A standing order may "
        "tell or ask too, after 'then'."
    ]
    whole = "\n".join([*order, "", *dialect, "", *station])
    parts = _split_lines(
        dialect,
        [
            ("Triggers:", "triggers"),
            ("Conditions:", "conditions and the readings"),
            ("Durations,", "durations"),
            ("Examples,", "examples, the starter routines"),
            ("The book's orders:", "the book's orders"),
        ],
    )
    sections = [
        Section("1", "the order language", "\n".join(order), "\n".join(order), by_line=True),
        Section(
            "2", "the standing dialect", "\n".join(dialect), "\n".join(parts[0][1]), by_line=True
        ),
    ]
    for k, (heading, chunk) in enumerate(parts[1:], 1):
        text = "\n".join(chunk)
        sections.append(Section(f"2.{k}", heading, text, text, by_line=True))
    sections.append(
        Section("3", "the station sentences", "\n".join(station), "\n".join(station), by_line=True)
    )
    return Topic(
        "grammar",
        "the grammar",
        "the grammar: the order language, the standing dialect and the station sentences",
        whole,
        tuple(sections),
    )


def _grammar() -> str:
    """The grammar whole, as `library(topic='grammar', section='all')` serves it after
    its size."""
    return _grammar_topic().whole


def _ship_topic(world: World) -> Topic:
    """This ship's parts by their names, by part of the rig: each lower mast (and the
    bowsprit) with the spars that stand on it, the sails they carry and their lines;
    then her groups and aliases."""
    ship = world.ship
    if not hasattr(ship, "parts"):
        text = f"{ship.name}: a point ship with no parts; she takes steer, speed and stop."
        return Topic("the ship", "the ship", text, text)
    from freesail.orders.resolve import display_name

    roots = [sid for sid, sp in ship.spars.items() if not sp.parent]
    by_root: dict[str, dict[str, set[str]]] = {}
    for kind, items in (("Spars", ship.spars), ("Sails", ship.sails), ("Lines", ship.lines)):
        for pid in items:
            try:
                root = ship.mast_of(pid)
            except (KeyError, AttributeError, TypeError):
                root = None
            where = root.id if root is not None else ""
            by_root.setdefault(where, {}).setdefault(kind, set()).add(display_name(ship, pid))
    order = [r for r in roots if r in by_root] + ([""] if "" in by_root else [])
    sections: list[Section] = []
    for k, rid in enumerate(order, 1):
        heading = display_name(ship, rid) if rid else "elsewhere"
        kinds = by_root[rid]
        counts = ", ".join(
            f"{len(kinds[kd])} {kd.lower() if len(kinds[kd]) != 1 else kd.lower()[:-1]}"
            for kd in ("Spars", "Sails", "Lines")
            if kd in kinds
        )
        lines = [f"The {heading}: {counts}."]
        for kd in ("Spars", "Sails", "Lines"):
            if kd in kinds:
                lines.append(f"  {kd}: {', '.join(sorted(kinds[kd]))}.")
        text = "\n".join(lines)
        sections.append(Section(str(k), heading, text, text, by_line=True))
    extra: list[str] = []
    if ship.groups:
        extra.append(
            "  Groups: "
            + "; ".join(
                f"{g} ({', '.join(display_name(ship, m) for m in members)})"
                for g, members in ship.groups.items()
            )
            + "."
        )
    if ship.aliases:
        extra.append(
            "  Aliases: "
            + ", ".join(f"{a} for {display_name(ship, t)}" for a, t in ship.aliases.items())
            + "."
        )
    if extra:
        text = "\n".join(
            ["Her groups and aliases, the names that stand for several parts:", *extra]
        )
        sections.append(
            Section(str(len(order) + 1), "groups and aliases", text, text, by_line=True)
        )
    whole = "\n\n".join(
        [f"{ship.name}: her parts by their names, by mast.", *(s.text for s in sections)]
    )
    return Topic(
        "the ship",
        "the ship",
        f"the ship, {ship.name}: her parts by their names, by mast, and her groups and aliases",
        whole,
        tuple(sections),
    )


def _ship_names(world: World) -> str:
    return _ship_topic(world).whole


def _papers_topic(world: World) -> Topic:
    """The ship's papers (package 35; spec M5 §22; `docs/design/Papers-and-Books.md`):
    in-world things read through the same tool and shelf as the reference, served by
    handle to every station the same, the browser's pane included. Each paper is a
    section (its handle), its page the store's own lines as its keeper last wrote them,
    dated by its last entry (`freesail.world.places.Papers`). Read-only here: the
    keepers write them, and the log says when."""
    from freesail.world.places import PLACES

    papers = getattr(world, "papers", None)
    ship = world.ship
    if papers is None or not hasattr(ship, "spars"):
        name = getattr(ship, "name", "The ship")
        text = f"{name} keeps no papers: a point ship has no stores to record."
        return Topic("papers", "the ship's papers", "the ship's papers: none", text)
    sections: list[Section] = []
    for k, page in enumerate(papers.pages(), 1):
        head = page.handle[:1].upper() + page.handle[1:]
        place = PLACES.get(page.place)
        where = place.name if place is not None else page.place
        body = [
            f"{head}: {page.words}; kept by the {page.keeper} in {where}; last written "
            f"{page.as_of}.",
            *page.lines,
        ]
        text = "\n".join(body)
        sections.append(Section(str(k), page.handle, text, text, by_line=True))
    whole = "\n\n".join(
        [
            f"{ship.name}'s papers, each as its keeper last wrote it; a paper is only as "
            "current as its last entry.",
            *(s.text for s in sections),
        ]
    )
    n = len(sections)
    return Topic(
        "papers",
        "the ship's papers",
        f"the ship's papers: {n} papers aboard, each by handle, as current as its last entry",
        whole,
        tuple(sections),
        whole_words="the whole bundle",
    )


def _topic(world: World, key: str) -> Topic | str:
    """The topic a call names, or the refusal in words."""
    if key.startswith("primer"):
        which = key.removeprefix("primer").strip()
        if which in ("", "readme", "contents", "introduction"):
            return _primer_topic()
        n = _chapter_of(which)
        return _chapter_topic(n) if n is not None else _no_chapter(which)
    if key in ("catalogue", "evolutions", "the catalogue", "the evolutions"):
        return _catalogue_topic()
    if key in ("grammar", "orders", "the grammar", "the order language"):
        return _grammar_topic()
    if key in ("the ship", "ship", "names", "parts"):
        return _ship_topic(world)
    if key in ("papers", "the papers", "the ships papers", "the ship's papers", "ships papers"):
        return _papers_topic(world)
    if key in ("standing orders", "the book", "book", "the standing orders"):
        text = "\n".join(world.standing.book.lines())
        return Topic("standing orders", "the standing orders", text, text)
    if key in ("tools", "the tools"):
        text = "\n".join(tool_lines())
        return Topic("tools", "the tools", text, text)
    n = _chapter_of(key, loose=False)  # a chapter's name alone
    if n is not None:
        return _chapter_topic(n)
    return f"The library has no topic '{key}'; library(topic='contents') lists what it holds."


def _every_topic(world: World) -> list[Topic]:
    out: list[Topic] = [
        *_primer_all(),
        _catalogue_topic(),
        _grammar_topic(),
        _ship_topic(world),
        _papers_topic(world),
    ]
    for key in ("standing orders", "tools"):
        top = _topic(world, key)
        assert isinstance(top, Topic)
        out.append(top)
    return out


def _listing(top: Topic) -> str:
    """A topic's sections with what each costs, and how to ask for one."""
    whole = f"{top.whole_words[:1].upper()}{top.whole_words[1:]}"
    out = [f"{top.title}. {whole}, {size_words(tokens(top.whole))} (section='all')."]
    out.append("Its sections, with what each costs:")
    for sec in top.sections:
        out.append(f"{'  ' * sec.level}{sec.label()}, {size_words(tokens(sec.text))}")
    out.extend(top.extra)
    out.append(
        f"One section: library(topic='{top.key}', section='<a word of its heading, or its "
        "number>'); the whole: section='all'; a search: find='<words>'."
    )
    return "\n".join(out)


def _match(sections: tuple[Section, ...], q: str) -> list[Section]:
    """The sections `q` names: by number ("4", "4.2"); else by heading, exactly, or by
    words each beginning a word of the heading, case-insensitively ("reef" for
    "Reefing"). A section and its own subsections found together are the section."""
    raw = q.strip().rstrip(".")
    if re.fullmatch(r"\d+(\.\d+)?", raw):
        return [s for s in sections if s.number == raw]
    qn = _norm(q)
    if not qn:
        return []
    exact = [s for s in sections if _norm(s.heading) == qn]
    if exact:
        return exact[:1]
    words = qn.split()
    found = [
        s
        for s in sections
        if all(any(h.startswith(w) for h in _norm(s.heading).split()) for w in words)
    ]
    tops = [s for s in found if s.level == 1]
    if len(found) > 1 and len(tops) == 1 and tops[0].number:
        head = tops[0]
        if all(s is head or s.number.startswith(head.number + ".") for s in found):
            return [head]
    return found


def _section_page(top: Topic, q: str) -> Page:
    if q.lower() in ALL_WORDS:
        size = size_words(tokens(top.whole))
        return Page(
            f"{top.title}, {top.whole_words}: {size}.\n\n{top.whole}",
            f"{top.name}, {top.whole_words}",
            _reopen(top.key, "all"),
        )
    found = _match(top.sections, q)
    if len(found) == 1:
        sec = found[0]
        again = q if "'" not in q else sec.number or sec.heading
        return Page(sec.text, f"{top.name}, {_lower_first(sec.heading)}", _reopen(top.key, again))
    if found:
        named = "; ".join(f"{s.label()} ({size_words(tokens(s.text))})" for s in found)
        text = (
            f"'{q}' names {len(found)} sections of {top.name}: {named}. Say which, by more "
            "of its heading or by its number."
        )
    else:
        named = "; ".join(s.heading if s.line else s.label() for s in top.sections)
        text = (
            f"{top.name} has no section '{q}'. Its sections: {named}. section='all' serves "
            "the whole."
        )
    return Page(text, f"{top.name}, '{q}'", _reopen(top.key))


def _find(topics: list[Topic], q: str, where: str, key: str) -> Page:
    """The paragraphs of `topics` in which the words `q` stand (each word of `q` at the
    start of a word, in order, case-insensitively; a hyphen as a space), each with its
    place; the first `FIND_LIMIT` whole and the places of the rest."""
    if key == "primer":
        topics = _primer_all()
    qn = _norm(q)
    hits: list[tuple[str, str]] = []
    for top in topics:
        secs = top.sections or (Section("", "", top.whole, top.whole, by_line=True),)
        for sec in secs:
            place = f"{top.name}, {_lower_first(sec.heading)}" if sec.heading else top.name
            paras = (
                [ln for ln in sec.own.splitlines() if ln.strip()]
                if sec.by_line
                else (_paragraphs(sec.own))
            )
            for p in paras:
                if qn and f" {qn}" in f" {_norm(p)}":
                    hits.append((place, p))
    title = f"{where}, find '{q}'"
    again = _reopen(key, find=q)
    if not hits:
        return Page(
            f"Nothing in {where} matches '{q}'. Fewer words, or another form of them, may "
            "find it; library(topic='contents') lists what the library holds.",
            title,
            again,
        )
    shown, rest = hits[:FIND_LIMIT], hits[FIND_LIMIT:]
    n = len(hits)
    head = f"'{q}' in {where}: {n} {'paragraph matches' if n == 1 else 'paragraphs match'}"
    head += f"; the first {FIND_LIMIT} here." if rest else "."
    out = [head, *(f"[{place}]\n{p}" for place, p in shown)]
    if rest:
        counts: dict[str, int] = {}
        for place, _ in rest:
            counts[place] = counts.get(place, 0) + 1
        out.append(
            f"And {len(rest)} more, not shown: "
            + "; ".join(f"{place} ({c})" for place, c in counts.items())
            + ". Read a section whole, or look for more exact words."
        )
    return Page("\n\n".join(out), title, again)


def _contents(world: World) -> str:
    intro = size_words(tokens(_primer_topic().whole))
    lines = [
        "The library holds these topics, always there to read. Each size is what reading "
        f"it costs, measured at about {CHARS_PER_TOKEN} characters a token.",
        f"  primer: the Sailing Master's Primer; its introduction {intro}. Its chapters, "
        "each whole:",
    ]
    for n, name in _primer_chapters():
        ch = _chapter_topic(n)
        k = sum(1 for s in ch.sections if s.number and "." not in s.number)
        lines.append(f"    primer {n}: {name}, {size_words(tokens(ch.whole))} in {k} sections")
    cat = _catalogue_topic()
    sizes = [tokens(s.text) for s in cat.sections]
    lines.append(
        f"  catalogue: the catalogue of evolutions the ship can perform: {len(sizes)} "
        f"evolutions; the list {size_words(tokens(_listing(cat)))}, each evolution "
        f"{size_words(min(sizes)).removesuffix(' tokens')} to "
        f"{size_words(max(sizes)).removeprefix('about ')}"
    )
    gram = _grammar_topic()
    lines.append(
        "  grammar: the order language, the standing dialect and the station sentences: "
        f"{size_words(tokens(gram.whole))} whole, in "
        f"{sum(1 for s in gram.sections if s.level == 1)} parts"
    )
    ship = _ship_topic(world)
    parts = sum(1 for s in ship.sections if s.level == 1)
    lines.append(
        "  the ship: this ship's parts by their names, by mast, with her groups and aliases: "
        f"{size_words(tokens(ship.whole))} whole" + (f", in {parts} parts" if parts else "")
    )
    papers = _papers_topic(world)
    handles = "; ".join(s.heading for s in papers.sections)
    lines.append(
        f"  papers: the ship's papers, {len(papers.sections)} aboard, each by handle and as "
        f"current as its last entry ({handles}): {size_words(tokens(papers.whole))} whole"
        if papers.sections
        else f"  papers: the ship's papers: none aboard ({size_words(tokens(papers.whole))})"
    )
    book = "\n".join(world.standing.book.lines())
    lines.append(
        f"  standing orders: the book of standing orders as it stands, {size_words(tokens(book))}"
    )
    lines.append(
        "  tools: the tools you have and what each takes, "
        f"{size_words(tokens(chr(10).join(tool_lines())))}"
    )
    lines.append(
        "A topic with sections lists them with their sizes (library(topic='primer 3')); "
        "section='reefing' serves one, by a word of its heading or its number, and "
        "section='all' the whole. find='goose-wing' returns the paragraphs that match, each "
        "with where it is, in a topic or, with no topic, in the whole library."
    )
    return "\n".join(lines)


STARTER_ORDERS = ROOT / "data" / "standing_orders" / "starter.orders"


def standing_dialect_lines(vocab: Any = None) -> list[str]:
    """The standing dialect in full, for the library's grammar page (package 28c: the
    watcher of playtest 3 "had to guess the standing-order syntax from one grammar
    line"): the sentence, the triggers with every event and interval the registry
    knows, the readings a condition may name and how each is compared, the durations,
    the starter routines as examples (read from the file, so they stay the file's), and
    the book's verbs with their synonyms."""
    from freesail.orders.vocabulary import load_vocabulary
    from freesail.standing.book import read_orders_file

    vocab = vocab or load_vocabulary()
    events = ", ".join(w for w, s in R.EVENTS.items() if not s.absent)
    later = ", ".join(w for w, s in R.EVENTS.items() if s.absent)
    readings = []
    for row in R.REGISTRY:
        if row.is_absent:
            continue
        words = " or ".join(f"'{w}'" for w in row.words)
        readings.append(f"    {words}: {R.KINDS[row.kind]}")
    absent = ", ".join(f"'{row.words[0]}'" for row in R.REGISTRY if row.is_absent)
    out = [
        "The standing dialect: standing orders, which the captain gives like any order and "
        "the ship keeps by herself. One line:",
        '  standing order "<name>" [by the <officer>]: <trigger> [, if <condition>] then '
        "<order> [; <order> ...]",
        "The name is in quotes. The orders after 'then' are ordinary orders of the language "
        "above, separated by semicolons, and are checked when the standing order is given. "
        "Among them 'tell the watcher <words>' and 'ask the watcher <question>' say a word "
        "or put a question to a station aboard, as the captain's own would, and the log names "
        "the standing order: \"By standing order 'sea': the captain to the watcher: the sea is "
        "getting up\". 'by the <officer>' is for an officer's order; the captain's is the "
        "default, and the senior's stands when two conflict on the same part.",
        "Triggers:",
        "  when <condition> [for <duration>]: fires once when the condition comes to hold "
        "(for that long, if a duration is given), and not again until it has been false "
        "for five minutes and the work it started is done",
        f"  at <event>: once each time the event happens. The events: {events}"
        + (f"; later, when the world has them: {later}" if later else "")
        + ". The weather's that are its readings' changes are "
        "measured from when the order stands, and afresh after each firing: 'a wind shift' "
        "is the mean wind a point or more from where it stood; 'the glass falling fast' its "
        "tendency coming to falling fast, and 'the glass turning' the last hour's change "
        "going against the three hours' ('when the glass is turning'), each once until it "
        "has been an hour without; 'the sea getting up' its "
        "words changing upward ('when the sea gets up'); 'a change in the sky' is the sky's "
        "or the weather's line in the log",
        "  every <interval>: on the interval, never queuing more than one: a glass, a bell, "
        "half an hour, an hour, a watch, or a number of minutes ('every 10 minutes')",
        "Conditions: a reading and a comparison, joined by 'and' (no 'or'): 'the true wind "
        "exceeds 30 knots and the fore royal is set'. The one 'or' is a wind's two ways of "
        "turning, 'the true wind veers 1 point or backs 1 point' (or 'shifts 1 point'), "
        "measured from the wind when the order stands and afresh after each firing. The "
        "readings, and how each is compared:",
        *readings,
        "    'the <sail>' is any sail by the ship's own name ('the fore royal is shaking'); "
        "'the <part>' any spar or line ('the fore royal yard is straining')",
        f"  Not yet in the ship, named so a condition can be refused in words: {absent}.",
        "Durations, after 'for': a number of minutes or seconds ('for 2 minutes', 'for "
        "30 seconds', 'for five minutes'), a glass, a bell, half an hour, an hour, a watch.",
        "Examples, the starter routines (data/standing_orders/starter.orders):",
    ]
    for line in read_orders_file(STARTER_ORDERS):
        note = "   (refused until the ship has a well to sound)" if "sound the well" in line else ""
        out.append(f"  {line}{note}")
    book = []
    for name, spec in vocab.verbs.items():
        if spec.object != "standing" or name == "standing order":
            continue
        syn = f" (also: {', '.join(spec.synonyms)})" if spec.synonyms else ""
        takes = "" if name in ("standing orders", "belay all standing orders") else ' "<name>"'
        book.append(f"  {name}{takes}{syn}")
    out += [
        "The book's orders:",
        *book,
        "  read the standing orders from <file>: at the console or the browser game, loads a "
        "file of standing orders one a line (the game's driver reads the disk, so it is "
        "not an order the ship hears)",
        "Belaying an order keeps it in the book, idle, until 'resume standing order'; "
        "striking it takes it out of the book, and its name may be given again.",
    ]
    return out
