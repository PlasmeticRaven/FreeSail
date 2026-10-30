"""The parity tests (spec M6 §22; the proposal's fourth principle; package 44, truth 91).

The captain's station's observation surface is the player's, and its action surface is the
player's: every reading the console answers, the station answers the same from the same
function; every verb the vocabulary has, the station may submit, filtered only by the
station's authority; and nothing is reachable by one that is not by the other. The first
tests enumerate both surfaces from the registries (the readings registry, the vocabulary,
the console's own commands, the browser's snapshot, the station's tools) and fail on any
entry of one that has no road on the other, the differences that are so by design listed
here with their reasons; the last seats a fake captain beside the console on one game and
has the console give the same orders to another game of the same seed, and the two logs
are the same log.

Found by the enumeration and closed (package 44): `muster`, the watch bill station by
station, which the console and the browser answered and the grammar refused to a station
as a console command; a station's `submit_order('muster')` is answered now from the same
function (`api.queries.muster_lines`), as the console prints it, logged by neither.
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import pytest

from freesail.agents import Harness, SamplingPolicy
from freesail.agents import tools as T
from freesail.agents.agent import CAPTAIN, CAPTAIN_DOMAIN, captain
from freesail.agents.fake import captain_of_the_ship
from freesail.api import queries
from freesail.api import readings as R
from freesail.orders.vocabulary import load_vocabulary
from freesail.ui import console as console_mod
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

ROOT = Path(__file__).resolve().parents[1]
PASSAGE = "data/scenarios/gate-5b-passage.yaml"

# A parametric reading asked with its parameter, as a player types it.
ASKED_WITH = {
    "sail": "the fore topsail",
    "strain": "the strain",
    "bearing_of": "the bearing of Ushant",
    "bearing_by_chart": "the bearing of Ushant by the chart",
    "distance_to": "the distance to Ushant",
    "where_is": "where is the master",
}

# The rows the `readings` tool does not carry, each with the road the station reads it by.
NOT_IN_THE_READINGS_TOOL = {
    "parametric": "asked by name with submit_order, as the console asks it ('the fore "
    "topsail', 'the bearing of Ushant'); the sails' states are the tool's `sails`",
    "absent": "refused in the same words at both (the world has none yet)",
    "driver": "the pace is the driver's (spec M6 §12): read with submit_order('the pace'), "
    "never carried in a sample",
}

# The console's own commands (the driver's, `freesail/ui/console.py`'s help and the
# browser's `Driver._console_query`), each with the station's road, or the reason it is
# the owner's alone by design.
CONSOLE_COMMANDS = {
    "hold": "by design: the clock is the owner's (spec M6 §12, the pace rule and lockstep)",
    "go": "by design: the clock is the owner's",
    "speed": "by design: the clock is the owner's",
    "time": "by design: the clock is the owner's",
    "tick": "by design: the clock is the owner's",
    "follow SHIP": "by design: the drivers' centre is the owner's (package 84, step 10; 82's "
    "§11): the hull the chart, the prompt and the snapshot follow, a driver's line; a "
    "station reads its own hull and no other",
    "state": "the station's `state` tool, from `World.summary_lines` as the console prints it",
    "muster": "submit_order('muster'), answered from `api.queries.muster_lines` (package 44)",
    "the sail room": "submit_order('the sail room'), the vocabulary's query",
    "the booms": "submit_order('the booms'), the vocabulary's query",
    "standing orders": "submit_order('standing orders'), the book's own listing",
    "read the standing orders from": "by design: the driver reads the disk (spec M4 §3); a "
    "station gives the book's lines one by one with submit_order",
    "ask the watcher": "submit_order, a station sentence (the captain's station addresses "
    "the stations as the player does)",
    "stand down the watcher": "submit_order, a station sentence",
    "resume the watcher": "submit_order, a station sentence",
    "show the watcher's journal": "submit_order, a station sentence",
    "log": "the station's `read_log` tool, the same log (a world order's own line is for the "
    "record only at both, decision 46)",
    "save": "by design: the save is the owner's",
    "replay": "by design: the load and the replay are the owner's",
    "help": "the station's `library` tool (the primer, the grammar, the tools)",
    "quit": "by design: the station's own leaving is `stand_down`; the game is the owner's",
    "world:": "by design: a world order is the scenario's, the director's and the owner's "
    "(spec M6 §23); refused to the captain at the prompt and at the station alike",
    # the director's (spec M7b §4 and §6; package 50): the owner's and the player's own
    "the director's log": "by design: the player's reveal of the director's log (spec M7b "
    "§6), which the director is told of; no station reads it",
    "two stories": "by design: the replay view, the player's",
    "director:": "by design: the player's brief for the director (spec M7b §4)",
}

# The browser's snapshot (`api.queries.snapshot`, the instruments and the chart's pane):
# each block, and the station's road to what it shows.
SNAPSHOT_BLOCKS = {
    "tick": "every sample's `tick`",
    "ship_time": "every sample's `stamp`",
    "stamp": "every sample's `stamp`",
    "bell": "the readings `watch`, `time`",
    "wind": "the readings `true_wind_*`, `apparent_wind_*`, `mean_true_wind_*`",
    "weather": "the readings `glass`, `tendency`, `sky`, `weather`, `visibility`, `sea`, `motion`",
    "lookout": "the readings `in_sight`, `land`",
    "strangers": "the readings `strangers`, `sail_in_sight`, `stranger_in_sight`",
    "reckoning": "the readings `reckoning`, `reckoning_uncertainty`, `run_since_noon`, "
    "`course_made_good`, `tide_by_almanac`, ...; the chart's track with the `chart` picture",
    "ship": "the readings `heading`, `course`, `speed`, `leeway`, `heel`, `helm`; the "
    "weather helm in the `state` tool",
    "sails": "the readings tool's `sails`",
    "spars": "the reading `strain` (the worst, and a part's by name)",
    "lines": "the reading `strain` (a line's by name)",
    "evolutions_in_progress": "the readings `work_in_hand`, `manoeuvre_in_hand`",
    "crew": "the readings `hands_on_deck`, `watch_below`; the muster",
    "agents": "the reading `stations` and the `state` tool",
    "driver": "the reading `pace`",
}

# The station's tools (`agents.tools.TOOLS`), each with the player's counterpart, or the
# reason it is the station's own by design.
TOOL_COUNTERPARTS = {
    "readings": "the instruments; a reading typed at the prompt",
    "read_log": "the log pane; `log N` at the console",
    "state": "`state`",
    "submit_order": "the order line",
    "library": "the primer and the references the player reads (docs/primer/)",
    "chart": "the browser's chart, drawn by the same page",
    "ship_view": "the browser's ship view, drawn by the same page",
    "answer": "`answer <words>` at the player's seat",
    "journal": "by design: a station's memory across its turns; the player keeps his own",
    "read_journal": "by design: the station's own; the owner reads it with 'show the "
    "<station>'s journal'",
    "stand_by": "by design: a station's cadence (spec M6 §12); the player holds the clock",
    "shelve": "by design: a model's context, which a player has not",
    "hand_over": "by design: the officer's deck given back; the player's seat says 'I have "
    "the deck' and 'you have the deck'",
    "handover_note": "by design: the station's relief",
    "stand_down": "by design: the station's leaving; the player's seat is stood down with "
    "'stand down the <station>'",
    "opt_out": "by design: the model's withdrawal (docs/agents/ConsentBrief.md)",
    # the director's (spec M7b §2; package 50): a station above the game, not on a ship;
    # offered at its station alone and refused in words at every other
    "world_order": "by design: the director's hand (spec M7b §3); the owner's is the `world:` "
    "prefix at the prompt; refused to the captain at the prompt and at the station alike",
    "truth": "by design: the director's reading surface (spec M7b §2; `readings."
    "director_readings`), which no station on a ship and no prompt reads (truth 81)",
}

# The vocabulary's verbs a station may not submit: the driver's, which the grammar refuses
# to the ship whoever says them (the console takes them first as its own commands).
DRIVER_VERBS_BY_DESIGN = {"hold", "go", "time", "read the standing orders from", "muster"}


@pytest.fixture(scope="module")
def seated_world():
    sf = load_scenario(ROOT / PASSAGE)
    world = make_scenario_world(sf)
    begin(world, sf)
    h = Harness(
        world,
        captain(SamplingPolicy.in_lockstep(600), 3600, world=world),
        captain_of_the_ship(),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake", "runner"
    h.start()
    world.run(1200)
    return world


def at_the_station(world, text: str) -> str:
    return T.call(world, CAPTAIN, "submit_order", {"text": text})


def test_every_reading_the_console_answers_the_station_answers_the_same(seated_world):
    """Every row of the readings registry, asked at the console's prompt and by the
    captain's station's `submit_order` at the same tick, gives the same words (the same
    function, `orders.prompt`); and every row the samples carry is in the `readings` tool
    with the registry's own words."""
    world = seated_world
    tool = T.readings(world, CAPTAIN)
    differ = []
    for row in R.REGISTRY:
        asked = ASKED_WITH.get(row.id, row.words[0])
        console = world.submit(asked).text
        station = at_the_station(world, asked)
        if console != station:
            differ.append((row.id, console, station))
        if row.is_absent or row.parametric is not None or row.kind in R.DRIVER_KINDS:
            why = (
                "absent"
                if row.is_absent
                else "parametric"
                if row.parametric is not None
                else "driver"
            )
            assert why in NOT_IN_THE_READINGS_TOOL and row.id not in tool, row.id
            continue
        assert tool.get(row.id) == world.readings.words(row.id), row.id
    assert not differ, differ
    assert set(tool["sails"]) and all(isinstance(v, str) for v in tool["sails"].values())


def test_every_verb_the_vocabulary_has_the_captains_station_may_submit(seated_world):
    """The action surface: every verb of the vocabulary passes the captain's station's
    domain (the player's whole surface), but the driver's, which the grammar refuses to
    the ship from either; at the officer's station the same verbs are filtered by his
    domain alone, never by the door."""
    vocab = load_vocabulary()
    refused = {
        verb
        for verb, spec in vocab.verbs.items()
        if CAPTAIN_DOMAIN.why_not(verb, spec.object, spec.level) is not None
    }
    driver = {verb for verb, spec in vocab.verbs.items() if spec.level == "driver"}
    assert refused <= driver, refused - driver
    assert driver == DRIVER_VERBS_BY_DESIGN, driver ^ DRIVER_VERBS_BY_DESIGN
    world = seated_world
    for verb in sorted(driver - {"muster", "read the standing orders from"}):
        said = verb if verb != "time" else "time 30"
        assert "console command" in world.submit(said).text
        assert "console command" in at_the_station(world, said)


def _console_commands() -> set[str]:
    """The console's own commands from its help, and the browser's queries."""
    help_text = console_mod.__doc__.split("Driver commands")[1].split("Anything else")[0]
    known = sorted(CONSOLE_COMMANDS, key=len, reverse=True)
    words = set()
    for line in help_text.splitlines():
        if not re.match(r"^ {4}\S", line):
            continue  # a description's continuation, indented further
        said = re.split(r"\s{2,}", line.strip())[0]
        for i, part in enumerate(said.split(", ")):
            cmd = next((k for k in known if part.startswith(k)), None)
            if cmd is not None:
                words.add(cmd)
            elif i == 0:
                words.add(part)  # a command the list has not got: the test fails on it
    return words | {"world:"}


def test_every_console_command_has_its_road_at_the_station_or_is_the_owners():
    """Every command the console's help lists (and the browser's order line takes) has a
    road at the captain's station, or is listed here as the owner's by design."""
    found = _console_commands()
    assert found <= set(CONSOLE_COMMANDS), found - set(CONSOLE_COMMANDS)
    assert {"muster", "state", "the sail room", "the booms", "hold", "save"} <= found


def test_the_console_queries_answer_the_station_from_the_same_functions(seated_world):
    """`muster` (the gap closed), `state`, `the sail room` and `the booms`: the station's
    answer is the console's own lines."""
    world = seated_world
    n = len(world.log)
    assert at_the_station(world, "muster") == "\n".join(queries.muster_lines(world))
    assert at_the_station(world, "muster the crew") == "\n".join(queries.muster_lines(world))
    assert len(world.log) == n  # never logged, as the console's muster is not
    state = T.state(world, CAPTAIN)
    assert all(line in state for line in world.summary_lines())
    assert at_the_station(world, "the sail room") == "\n".join(queries.sail_room_lines(world))
    assert at_the_station(world, "the booms") == "\n".join(queries.booms_lines(world))
    # the world order, refused at both in the vocabulary's words
    said = 'world: message: at Brest from the agent: "Come."'
    assert world.submit(said).text == at_the_station(world, said)


def test_the_snapshot_and_the_tools_each_have_their_road_on_the_other_side(seated_world):
    """Every block of the browser's snapshot names the station's road to it, and every tool
    of the station names the player's counterpart or why it is the station's own; a block
    or a tool added without its road fails here until it is given one."""
    snap = queries.snapshot(seated_world)
    assert set(snap) <= set(SNAPSHOT_BLOCKS), set(snap) - set(SNAPSHOT_BLOCKS)
    assert set(T.TOOLS) == set(TOOL_COUNTERPARTS), set(T.TOOLS) ^ set(TOOL_COUNTERPARTS)
    for block, road in SNAPSHOT_BLOCKS.items():
        for rid in re.findall(r"`([a-z_]+)`", road):
            if rid.endswith("_"):
                continue
            assert rid in R.REGISTRY or rid in T.TOOLS or rid in ("tick", "stamp", "sails"), (
                block,
                rid,
            )


# The orders the fake captain gives one a sample (every ten minutes in lockstep) and the
# console gives at the same ticks in the other game: a sail order, a reading, the helm, the
# trim, the muster, a store's query, an order refused, a standing order, the log, a sail.
SAME_ORDERS = [
    "set plain sail",
    "the tide",
    "steer N by E",
    "trim sails",
    "muster",
    "the sail room",
    "take in the royals",
    'standing order "glass": every glass then trim the sheets',
    "heave the log",
    "set the royals",
]
SAME_EVERY = 600


def _the_passage():
    sf = load_scenario(ROOT / PASSAGE)
    sf.standing_orders = []
    sf.orders = []
    world = make_scenario_world(sf)
    begin(world, sf)
    return world


# By design: the console prints the answer to a question of the ship's stores (`the sail
# room`, `the booms`, ...) for the one who asked, and the browser's order line shows it in
# its pane; a station's answer is the tool's result and the log's line, as a reading's is
# at both (the console's own words for it, `Console.handle_line`, never reach the World).
FOR_THE_ONE_WHO_ASKED = ("query.sail_room", "query.booms", "query.cordage")


def _lines(world, actors: tuple[str, ...]):
    """The log as the two games share it: the station's own lines (`agent.`) left out, an
    order's own line by its kind (the station's 'By the captain: setting ...' is the
    console's 'Order: set ...'), everything else by its words."""
    out = []
    for e in world.log:
        if e.kind.startswith("agent.") or e.kind in FOR_THE_ONE_WHO_ASKED:
            continue
        if e.actor in actors and e.kind in ("order.accepted", "order.rejected"):
            out.append((e.tick, e.kind))
        else:
            out.append((e.tick, e.kind, e.text))
    return out


def test_truth_91_a_fake_captain_and_the_console_give_the_same_orders_to_the_same_log():
    """Spec M6 §22 and truth 91: a fake captain seated at the captain's station beside
    the console gives ten orders, one a sample; the console gives the same ten at the same
    ticks to a second game of the same seed and scenario; the two logs are the same log,
    line for line, but for whose each order's own line says it was."""
    a = _the_passage()
    console_a = console_mod.Console(a, out=io.StringIO())
    h = Harness(
        a,
        captain(SamplingPolicy.in_lockstep(SAME_EVERY), 3600, world=a),
        captain_of_the_ship(SAME_ORDERS),
        save=lambda w, why: None,
    )
    h.model_name, h.door = "the fake", "runner"
    h.start()
    end = SAME_EVERY * (len(SAME_ORDERS) + 2)
    a.run(end)
    console_a.handle_line("the tide")  # the console on the same game, answered the same
    given = [
        e.tick
        for e in a.log
        if e.actor == "the captain" and e.kind.startswith(("order.", "query."))
    ]
    assert given[:2] == [SAME_EVERY, 2 * SAME_EVERY]

    b = _the_passage()
    out = io.StringIO()
    console_b = console_mod.Console(b, out=out)
    for i, text in enumerate(SAME_ORDERS):
        b.run(SAME_EVERY * (i + 1) - b.clock.tick)
        console_b.handle_line(text)
    b.run(end - b.clock.tick)
    console_b.handle_line("the tide")
    assert "Mustered the" in out.getvalue()
    assert _lines(a, ("the captain",)) == _lines(b, ("captain",))
    assert len([e for e in a.log if e.actor == "the captain"]) >= len(SAME_ORDERS) - 1
