"""The Sailing Master's Primer (docs/primer/) shows only orders that parse.

Every fenced code block in the primer whose info string begins with
``orders`` is a list of orders, one per line, run here through
``freesail.orders.handle`` against the ship the fence names. The info
string is::

    ```orders <ship> [<preset>] [<tack>]

- ``<ship>`` is ``frigate`` (data/ships/frigate-36.yaml), ``schooner``
  (data/ships/topsail-schooner.yaml), ``cutter`` (data/ships/cutter.yaml) or
  ``brig`` (data/ships/brig.yaml).
- ``<preset>`` is the state the ship starts the block in: ``furled`` (the
  default: nothing set, yards square), ``plain-sail`` (the ship file's
  ``plain sail`` group set, the yards braced sharp up and the fore-and-aft
  sheets trimmed to the wind at 40° apparent, as setting them does), ``all-sail``
  (the ``all sail`` group set, studding sails and all) or ``reefed``
  (plain sail with one reef in every sail that has reef bands).
- ``<tack>`` is ``starboard`` (the default) or ``larboard``: which side the
  wind is on, which is what ``weather`` and ``lee`` resolve against.

Inside a block:

- a blank line, or a line beginning ``#`` that is not one of the forms
  below, is a comment and is ignored;
- a line beginning ``# rejected:`` is an order the chapter says the ship
  refuses; the test asserts that it raises ``OrderError``;
- a line whose first word is a console driver command (``tick``,
  ``state``, ``muster``, ``hold``, ``go``, ``time``, ``log``, ``save``, ``replay``,
  ``help``, ``quit``) is skipped: it goes to the console, not the ship;
- any other line is an order the chapter says the ship accepts; the test
  asserts that ``handle`` returns without raising.

A block tagged ``orders-pending`` (same syntax) shows an order that a
package still in flight will add, such as ``trim`` (package 13). It is
run the same way, but if any accepted line is refused because its verb is
unknown, the block is skipped instead of failed; once the verb exists the
block is checked in full, and the fence should then be retagged ``orders``.

The evolution runner is stood in for by ``InstantRunner``, which records
each start and applies the evolution's end state at once (a set sail is
set, a braced yard is at its angle, a tack puts the wind on the other
side), so that the orders of one block can build on each other as they
would in the console. Runtime preconditions that only the real runner
checks (way enough to stay, already hove to) are described in the prose,
not asserted here.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest

from freesail import orders
from freesail.core.clock import Clock
from freesail.core.rng import Rng
from freesail.core.world import Scenario, World
from freesail.crew import muster
from freesail.crew.routine import Routine
from freesail.evolutions.trim import set_sheet_angle, wanted_sheet_angle
from freesail.orders.errors import OrderError
from freesail.ship.graph import Ship
from freesail.ship.loader import load_spec
from freesail.ship.parts import SailState

ROOT = Path(__file__).resolve().parents[1]
PRIMER = ROOT / "docs" / "primer"
SHIP_FILES = {
    "frigate": ROOT / "data" / "ships" / "frigate-36.yaml",
    "schooner": ROOT / "data" / "ships" / "topsail-schooner.yaml",
    "cutter": ROOT / "data" / "ships" / "cutter.yaml",
    "brig": ROOT / "data" / "ships" / "brig.yaml",
}
SPECS = {name: load_spec(path) for name, path in SHIP_FILES.items()}

CHAPTERS = [
    "README.md",
    "01-the-ship.md",
    "02-the-wind-and-the-points-of-sail.md",
    "03-making-and-shortening-sail.md",
    "04-trimming.md",
    "05-going-about.md",
    "06-the-watch-and-the-log.md",
    "07-a-first-passage.md",
    "08-where-to-read-more.md",
    "09-the-glass-and-the-sky.md",
    "10-the-reckoning.md",
    "11-the-starting-book.md",
    "12-the-longitude.md",  # package 33b
]

DRIVER_COMMANDS = frozenset(
    {"hold", "go", "time", "tick", "state", "muster", "log", "save", "replay", "help"}
    | {"quit", "exit"}
)
# The blocks' ships keep the forenoon watch: the idlers are up (package 20).
PRIMER_TIME = datetime(1805, 6, 1, 10, 0)
PRESETS = ("furled", "plain-sail", "all-sail", "reefed")
TACKS = ("starboard", "larboard")

FENCE = re.compile(r"^```(orders(?:-pending)?)\b([^\n]*)\n(.*?)^```", re.M | re.S)


# ---------------------------------------------------------------------------
# A runner that finishes every evolution the moment it starts
# ---------------------------------------------------------------------------


class InstantRunner:
    """Stands in for the evolution runner: records starts, applies end states."""

    def __init__(self) -> None:
        self.started: list[tuple[str, str, dict[str, Any]]] = []

    def start(self, ship: Ship, evolution_id: str, subject_id: str, params=None) -> str:
        p = dict(params or {})
        self.started.append((evolution_id, subject_id, p))
        self._apply(ship, evolution_id, subject_id, p)
        return f"Started {evolution_id} on {subject_id}."

    @staticmethod
    def _apply(ship: Ship, evo: str, subject: str, p: dict[str, Any]) -> None:
        if evo.startswith("set_"):
            ship.sails[subject].state = SailState.SET
        elif evo == "take_in_studding":
            ship.sails[subject].state = SailState.FURLED
        elif evo.startswith("take_in_"):
            ship.sails[subject].state = SailState.IN_THE_GEAR
        elif evo == "furl_all":
            for sail in ship.sails.values():
                if sail.state is not SailState.UNBENT:
                    sail.state = SailState.FURLED
        elif evo.startswith("furl_"):
            ship.sails[subject].state = SailState.FURLED
        elif evo in ("reef_bowsprit", "rig_out_bowsprit"):
            # the cutter's running bowsprit (package 32b): run in to its housed length
            # or out to its full one, as the evolutions' end states have it
            spar = ship.spars[subject]
            spar.rigged_out = evo == "rig_out_bowsprit"
            spar.length_m = spar.full_length_m if spar.rigged_out else spar.housed_length_m
        elif evo.startswith("reef_"):
            sail = ship.sails[subject]
            n = sail.reef_bands if p.get("close") else int(p.get("reefs", 1))
            sail.reefs = min(sail.reefs + n, sail.reef_bands)
        elif evo.startswith("shake_out_"):
            sail = ship.sails[subject]
            sail.reefs = max(sail.reefs - int(p.get("reefs", 1)), 0)
        elif evo == "brace":
            ship.spars[subject].brace_angle = float(p.get("target_angle", 0.0))
        elif evo in ("tack", "wear"):
            ship.dyn.apparent_wind_angle = -ship.dyn.apparent_wind_angle
            for yard in ship.spars.values():
                if yard.is_yard:
                    yard.brace_angle = -yard.brace_angle
        elif evo == "heave_to":
            # As the real script does: the courses hauled up and, on a ship
            # with yards on more than one mast, the driver brailed up.
            masts_with_yards = {
                ship.mast_of(y).id for y in ship.spars.values() if y.is_yard and ship.mast_of(y)
            }
            for sail in ship.sails.values():
                if not sail.is_set:
                    continue
                yard = ship.yard_of(sail)
                parent = ship.parent_of(yard) if yard is not None else None
                if sail.cls == "square" and parent is not None and parent.cls == "mast":
                    sail.state = SailState.IN_THE_GEAR
                elif sail.cls == "gaff" and len(masts_with_yards) > 1:
                    sail.state = SailState.IN_THE_GEAR
            ship.extra["hove_to"] = {"yards": [], "sign": 1.0}
        elif evo == "fill_away":
            ship.extra.pop("hove_to", None)


def make_ship(which: str, preset: str, tack: str) -> Ship:
    ship = Ship(SPECS[which])
    ship.extra["evolutions"] = InstantRunner()
    # a World around the ship, so that chapter 7's standing orders have a book to be
    # entered in (spec M4 §3: `standing order "x": ...` needs the runtime the World
    # attaches); the blocks never tick it
    # ...and on the sphere, ten miles south of the Lizard on the chart of the western
    # Channel, so that chapter 10's navigation orders have a reckoning to keep and a
    # mark in sight (package 33a; the reckoning refuses every order on the plane)
    World(
        seed=7,
        scenario=Scenario(
            start_time=PRIMER_TIME,
            position={"lat_deg": 49.80, "lon_deg": -5.20},
            region="channel-west",
        ),
        ship=ship,
    )
    if ship.spec.crew is not None:
        # the ship's company and the watch routine, as make_world attaches them, so that
        # chapter 6's crew orders have hands to call (package 20)
        ship.extra["crew"] = muster(ship.spec.crew, Rng(7).stream("muster"), ship_name=ship.name)
        ship.extra["routine"] = Routine(ship.extra["crew"], Clock(PRIMER_TIME))
    sign = 1.0 if tack == "starboard" else -1.0
    ship.dyn.apparent_wind_angle = sign * math.radians(40.0)
    ship.dyn.apparent_wind_speed = 8.0
    if preset == "furled":
        return ship
    group = "all sail" if preset == "all-sail" else "plain sail"
    for sail_id in ship.groups[group]:
        sail = ship.sails[sail_id]
        sail.state = SailState.SET
        if sail.is_fore_and_aft:
            # as setting the sail does: the sheet worked to the trim for the apparent wind
            # (package 32e: the sheet holds the trim)
            set_sheet_angle(ship, sail, wanted_sheet_angle(sail.cls, ship.dyn.apparent_wind_angle))
    for yard in ship.spars.values():
        if yard.is_yard:
            yard.brace_angle = sign * yard.brace_limit
    if preset == "reefed":
        for sail in ship.sails.values():
            if sail.is_set and sail.reef_bands:
                sail.reefs = 1
    return ship


# ---------------------------------------------------------------------------
# Extracting the blocks
# ---------------------------------------------------------------------------


@dataclass
class Block:
    chapter: str
    line: int
    pending: bool
    ship: str
    preset: str
    tack: str
    lines: list[str]

    @property
    def id(self) -> str:
        return f"{self.chapter}:{self.line}"


def parse_info(info: str, where: str) -> tuple[str, str, str]:
    words = info.split()
    if not words or words[0] not in SHIP_FILES:
        raise ValueError(f"{where}: an orders fence must name the ship: ```orders frigate")
    ship = words[0]
    preset, tack = "furled", "starboard"
    for w in words[1:]:
        if w in PRESETS:
            preset = w
        elif w in TACKS:
            tack = w
        else:
            raise ValueError(f"{where}: unknown word {w!r} in the fence (presets {PRESETS})")
    return ship, preset, tack


def blocks_of(path: Path) -> list[Block]:
    text = path.read_text(encoding="utf-8")
    out: list[Block] = []
    for m in FENCE.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        ship, preset, tack = parse_info(m.group(2), f"{path.name}:{line}")
        out.append(
            Block(
                chapter=path.name,
                line=line,
                pending=m.group(1) == "orders-pending",
                ship=ship,
                preset=preset,
                tack=tack,
                lines=m.group(3).splitlines(),
            )
        )
    return out


def all_blocks() -> list[Block]:
    out: list[Block] = []
    for name in CHAPTERS:
        path = PRIMER / name
        if path.exists():
            out.extend(blocks_of(path))
    return out


BLOCKS = all_blocks()


def classify(line: str) -> tuple[str, str]:
    """('accept' | 'reject' | 'skip', order text) for one line of a block."""
    s = line.strip()
    if not s:
        return "skip", ""
    if s.startswith("#"):
        body = s[1:].strip()
        if body.lower().startswith("rejected:"):
            return "reject", body[len("rejected:") :].strip()
        return "skip", ""
    if s.split()[0].lower() in DRIVER_COMMANDS:
        return "skip", ""
    return "accept", s


# ---------------------------------------------------------------------------
# The tests
# ---------------------------------------------------------------------------


def test_every_chapter_exists_and_is_listed_in_the_readme():
    readme = (PRIMER / "README.md").read_text(encoding="utf-8")
    for name in CHAPTERS:
        assert (PRIMER / name).exists(), f"missing chapter {name}"
        if name != "README.md":
            assert name in readme, f"README.md does not link {name}"


def test_the_primer_shows_enough_orders():
    accepted = sum(1 for b in BLOCKS for ln in b.lines if classify(ln)[0] == "accept")
    rejected = sum(1 for b in BLOCKS for ln in b.lines if classify(ln)[0] == "reject")
    assert len(BLOCKS) >= 25
    assert accepted >= 100
    assert rejected >= 10
    assert any(b.ship == "schooner" for b in BLOCKS)


@pytest.mark.parametrize("block", BLOCKS, ids=[b.id for b in BLOCKS])
def test_orders_block(block: Block):
    ship = make_ship(block.ship, block.preset, block.tack)
    runner: InstantRunner = ship.extra["evolutions"]
    for n, raw in enumerate(block.lines, start=block.line + 1):
        kind, text = classify(raw)
        where = f"{block.chapter}:{n} ({block.ship}, {block.preset}, {block.tack} tack)"
        if kind == "skip":
            continue
        if kind == "reject":
            before = len(runner.started)
            with pytest.raises(OrderError):
                orders.handle(ship, text)
            assert len(runner.started) == before, f"{where}: a refused order started something"
            continue
        try:
            result_kind, log, _data = orders.handle(ship, text)
        except OrderError as e:
            if block.pending and "is not an order this ship understands" in str(e):
                pytest.skip(f"{where}: {text!r} waits on a verb not yet in the vocabulary")
            raise AssertionError(f"{where}: {text!r} was refused: {e}") from None
        assert result_kind and log, where
        assert log[0].isupper() and log.endswith("."), f"{where}: log line {log!r}"


def test_a_rejected_line_that_parses_fails_the_test():
    """The convention has teeth: a '# rejected:' order that the ship accepts is an error."""
    ship = make_ship("frigate", "furled", "starboard")
    with pytest.raises(pytest.fail.Exception):
        with pytest.raises(OrderError):
            orders.handle(ship, "set the fore topsail")


def test_presets_put_the_ship_in_the_state_the_chapters_assume():
    plain = make_ship("frigate", "plain-sail", "starboard")
    assert plain.sails["fore.topsail"].is_set and not plain.sails["fore.royal"].is_set
    main_yard = plain.spars["main.yard"]
    assert main_yard.brace_angle == pytest.approx(main_yard.brace_limit)
    larboard = make_ship("frigate", "plain-sail", "larboard")
    assert larboard.dyn.tack == "larboard"
    assert larboard.spars["main.yard"].brace_angle < 0
    reefed = make_ship("schooner", "reefed", "starboard")
    assert reefed.sails["main.sail"].reefs == 1 and reefed.sails["fore.topsail"].reefs == 1
    everything = make_ship("frigate", "all-sail", "starboard")
    assert everything.sails["fore.topmast.studdingsail.larboard"].is_set


def test_instant_runner_applies_end_states():
    ship = make_ship("frigate", "furled", "starboard")
    orders.handle(ship, "set the fore topsail")
    assert ship.sails["fore.topsail"].is_set
    orders.handle(ship, "reef the fore topsail, two reefs")
    assert ship.sails["fore.topsail"].reefs == 2
    orders.handle(ship, "shake out a reef in the fore topsail")
    assert ship.sails["fore.topsail"].reefs == 1
    orders.handle(ship, "take in the fore topsail")
    assert ship.sails["fore.topsail"].state is SailState.IN_THE_GEAR
    orders.handle(ship, "furl the fore topsail")
    assert ship.sails["fore.topsail"].state is SailState.FURLED
    orders.handle(ship, "brace the main yard sharp up on the larboard tack")
    main_yard = ship.spars["main.yard"]
    assert main_yard.brace_angle == pytest.approx(-main_yard.brace_limit)
    orders.handle(ship, "tack ship")
    assert ship.dyn.tack == "larboard"


# ---------------------------------------------------------------------------
# Package 33c: every form in the forms tables of chapters 10 and 11 parses
# ---------------------------------------------------------------------------

# The tables of forms, by chapter and the heading they stand under.
FORM_TABLES = {
    "10-the-reckoning.md": "## Every form, in a table",
    "11-the-starting-book.md": "## The dialect's forms, in a table",
}
TICK = "`"


def table_forms(chapter: str, heading: str) -> list[str]:
    """Every form in the tables under `heading`: in a table of three columns the first two
    (the form, and the forms also taken), in one of two the first."""
    text = (PRIMER / chapter).read_text(encoding="utf-8")
    section = text.split(heading, 1)[1].split("\n## ", 1)[0]
    forms: list[str] = []
    for line in section.splitlines():
        if not line.startswith("|") or set(line) <= set("|- "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells[0].startswith(TICK):
            continue  # the header
        for cell in cells[: 2 if len(cells) == 3 else 1]:
            forms += [f for i, f in enumerate(cell.split(TICK)) if i % 2 == 1]
    return forms


STANDING_HEADS = ("when ", "at ", "every ", "if ")
FORMS = [(ch, f) for ch, heading in FORM_TABLES.items() for f in table_forms(ch, heading)]


def test_the_forms_tables_are_there_and_large_enough():
    by_chapter = {ch: [f for c, f in FORMS if c == ch] for ch in FORM_TABLES}
    assert len(by_chapter["10-the-reckoning.md"]) >= 90
    assert len(by_chapter["11-the-starting-book.md"]) >= 60
    assert sum(1 for _, f in FORMS if f.startswith(STANDING_HEADS)) >= 80


@pytest.mark.parametrize("chapter,form", FORMS, ids=[f"{c[:2]}: {f}" for c, f in FORMS])
def test_every_form_in_the_forms_tables_is_taken(chapter: str, form: str):
    """Package 33c (the owner's note at gate 5b: the reckoning's terms unclear with the
    primer beside him, many orders refused): every form of the master's orders and the
    reckoning's readings in chapter 10's table, and every form of the dialect in chapter
    11's, is understood by the frigate off the Lizard. An order may be refused for the
    ship's state (the sun not on the meridian, a mark not in sight), never for its words;
    a condition or an event is given as a standing order and must be entered."""
    from freesail.orders.errors import UnknownNounError, UnknownVerbError

    ship = make_ship("frigate", "plain-sail", "starboard")
    if form.startswith(STANDING_HEADS):
        head = f"every glass, {form}" if form.startswith("if ") else form
        kind, log, _ = orders.handle(ship, f'standing order "form": {head} then trim sails')
        assert kind == "standing.given", log
        return
    try:
        kind, log, _ = orders.handle(ship, form)
    except (UnknownVerbError, UnknownNounError) as e:
        raise AssertionError(f"{chapter}: {form!r} was not understood: {e}") from None
    except OrderError as e:
        words = str(e)
        assert "was understood, but not" not in words, f"{form!r}: {words}"
        assert "takes nothing after it" not in words, f"{form!r}: {words}"
        return
    assert kind and log and log[0].isupper(), (form, log)
