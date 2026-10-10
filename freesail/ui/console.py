"""The console driver: runs a world, prints the log, reads orders from stdin.

    python -m freesail.ui.console [ship] [--seed N] [--time N] [--load SAVE]
                                  [--scenario FILE] [--standing-orders FILE]
                                  [--watcher fake] [--agents-port N] [--lockstep]
                                  [--consent-records DIR] [--saves DIR] [--seat officer]

`--scenario FILE` starts from a scenario file (`freesail.world.scenarios`,
`data/scenarios/gate-4c-day.yaml`): its ship, start, latitude and weather script, its
seed unless `--seed` is given, its standing orders and first orders.

Compression runs to `MAX_COMPRESSION` (300, spec M4 §20). At `events.ROLLUP_FROM` (60)
and above the log is rolled up: notable and urgent lines and the captain's own as they
are, each hour's routine lines in one line marked `=` (`events.RollupView`, the same view
the server and a model's samples use). An urgent line while the clock runs faster than
`ALARM_SPEED` eases it to that speed and says so in the log (spec M4 open item 8).

`--agents-port N` hosts the agent API (the routes of `freesail.ui.server.agent_routes`,
spec M4 §13 as revised) on that port, in a thread on the console's own lock, so that a
model's door (the MCP bridge, the local runner) attaches to this game as it does to the
browser's. `--lockstep` holds the clock while a door has the floor.

Driver commands (not ship orders, not journaled):
    hold            pause the clock
    go              run the clock
    speed N         set compression to N game seconds per real second, up to 300
    time N          the same as speed N
    tick N          advance N ticks, then hold
    state           print a summary of the ship and the weather
    muster          muster the crew: the watch bill, station by station
    the sail room   what the sail room holds: each sail, its canvas and condition
    the booms       the spare spars aboard, by class (also `the spare spars`)
    standing orders the book of standing orders, each with its state
    read the standing orders from FILE
                    give every standing order in the file (each is journaled)
    ask the watcher QUESTION, stand down the watcher, resume the watcher,
    show the watcher's journal
                    orders to the watcher's station, when one is stationed
                    (--watcher fake stations a scripted one; spec M4 §12)
    log [N]         print the last N log entries (default 20)
    save PATH       write a save file
    replay PATH     rebuild a world from a save and continue from it; a save of another
                    build that holds a station's transcript is refused in words unless
                    `replay PATH --replay-anyway` (package 37d)
    help            this text
    quit            leave

Anything else is submitted to the ship as an order.
"""

from __future__ import annotations

import argparse
import queue
import sys
import threading
import time
from typing import Any

from freesail import units
from freesail.agents.seat import seat_player
from freesail.api import queries
from freesail.core import replay as replay_mod
from freesail.core.events import Event, RollupView, Severity, Shown
from freesail.core.world import UNLOGGED_KINDS, Scenario, World
from freesail.ship.stub import OrderError

HELP = __doc__.split("Driver commands")[1] if __doc__ else ""

READ_STANDING_ORDERS = ("read the standing orders from", "load the standing orders from")

# The fastest the clock runs, game seconds a real second (spec M4 §20: "The server and
# console take `speed N` up to 300"): a day in under five minutes.
MAX_COMPRESSION = 300.0
# The slowest, so that `speed 0` still moves.
MIN_COMPRESSION = 0.1
# Auto-slow on alarm (spec M4 open item 8, the owner's ruling (b)): an urgent line while the
# clock runs faster than this eases it to this, and the log says so; the player speeds up
# again when ready. One, not ten (judgement, named in docs/dev/TuningNotes.md, M4c): an
# urgent line is a sail blown out, a spar carried away, a line parted, and the next one often
# follows within seconds of ship's time (package 29's first run of the gate's day: two
# topgallants blew out and the fore topgallant yard carried away eleven seconds later), so
# the player needs the ship's own pace to see it and answer; at ten that is one real second.
ALARM_SPEED = 1.0

# The words for the driver's speed, the console's `time` and the owner's `speed`.
SPEED_WORDS = ("speed", "time")


def clamp_compression(value: float) -> float:
    """A compression the drivers run at: between MIN_COMPRESSION and MAX_COMPRESSION."""
    return min(MAX_COMPRESSION, max(MIN_COMPRESSION, float(value)))


def eased_words(e: Event) -> str:
    """The log's line for auto-slow: 'Compression eased to 1x: <the urgent line's words>'."""
    return f"Compression eased to {ALARM_SPEED:g}x: {e.text}"


def read_standing_orders_path(line: str) -> str | None:
    """The file named by `read the standing orders from <file>`, or None."""
    lower = " ".join(line.lower().split())
    for head in READ_STANDING_ORDERS:
        if lower.startswith(head + " "):
            return " ".join(line.split())[len(head) + 1 :].strip().strip("\"'")
        if lower == head:
            return ""
    return None


def read_standing_orders(world: World, path: str) -> int:
    """Give every standing order in a file to the world (spec M4 §3, §6). Each line is
    submitted as the captain's order, so each is journaled and replays; the log says what
    became of it. Returns how many were given. Shared by the console and the server."""
    from freesail.standing.book import read_orders_file

    if not path:
        raise OSError(2, "Say which file", path)
    lines = read_orders_file(path)
    for text in lines:
        world.submit(text)
    return len(lines)


# The starter book (package 33c, decision 30): a choice, never a requirement for
# beginning; the opening words of the console and the browser say how to load it.
STARTER_BOOK = "data/standing_orders/starter.orders"


def book_words(world: World) -> str:
    """The opening words about the book of standing orders (package 33c, decision 30):
    how to load the starter book or begin with none, or what the book holds."""
    n = len(world.standing.book)
    if n == 0:
        return (
            "The book of standing orders is empty. Begin with none, give your own, or load "
            f"the starter book: read the standing orders from {STARTER_BOOK} (the primer's "
            "chapter 11, 'The starting book', gives each routine with its reason)."
        )
    held = "one standing order" if n == 1 else f"{n} standing orders"
    return f"The book holds {held}; 'standing orders' lists them."


def agent_save_path(world: World) -> str:
    """Where an agent's harness saves the game on an opt-out or a stand-down (spec M4
    §11): the same name the server offers a download under, in the working directory."""
    return f"freesail-seed{world.seed}-tick{world.clock.tick}.json"


def station_watcher(world: World, kind: str, out=None) -> Any:
    """`--watcher fake`: station the scripted watcher (spec M4 §12, §15) with the
    built-in narration script, sampled every glass and on notable events, saving through
    the console's own save path. The two real doors are package 28's. Returns the
    harness. A loaded game that already has a watcher keeps it and gives it the live
    model in place of the recorded replies."""
    from freesail.agents import fake as fake_mod
    from freesail.agents.agent import SESSION_PLAY, watcher
    from freesail.agents.harness import Harness

    if kind != "fake":
        raise SystemExit(
            f"--watcher takes 'fake' in this build (the doors are package 28's), not '{kind}'."
        )
    model = fake_mod.narrator()

    def save(w: World, reason: str) -> str:
        p = replay_mod.save_to_file(w, agent_save_path(w))
        if out is not None:
            # the digest, so a replay of the file can be checked against it (`replay`)
            print(
                f"Saved to {p} ({reason}); the log's digest is {w.log.digest()[:16]}.",
                file=out,
                flush=True,
            )
        return str(p)

    existing = world.agents.get("watcher")
    if existing is not None:
        existing.model = model
        existing.save_fn = save
        return existing
    h = Harness(world, watcher(), model, session_kind=SESSION_PLAY, save=save)
    h.start()
    return h


def check_agents_unattended(world: World) -> None:
    """The driver's half of the unattended bound (spec M4 §11): ten real minutes of a
    pause with no answer stands the agent down. Called from the drivers' clock loops."""
    for agent in list(world.agents.values()):
        agent.check_unattended()


# The pace rule (spec M6 §12; decision 39, ruling 2; package 41). The owner's testing
# setting, built as the default: the clock slows to 1x while any model's sample is open,
# whoever holds it, at whatever station, and returns to the set compression when every
# open sample has been answered or has stood by. Not lockstep: the ship sails on at her
# own second while the model thinks, and a slow answer lands late; `--lockstep` holds
# the clock for a door with the floor and stays the separate option; `--free-running`
# runs at the set compression with no slowing, the flag for the solo player who wants a
# model to think while he sails at sixty times. The rule is the driver's: it moves no
# tick of the world, only how many of them a real second brings.
PACE_RULE, PACE_LOCKSTEP, PACE_FREE = "pace", "lockstep", "free"

# The log says once when the clock has been held at 1x for a station this long, in real
# seconds, so that a slow door is seen and not suffered (judgement: the MCP bridge holds
# a call open 200 s by default under the Desktop client's four-minute cut, and a reply
# through it in gate 5c's games came within a minute as a rule; two minutes of the ship
# at her own second is when the player at sixty times notices his evening has stopped,
# and is still under the bridge's own wait, so the line comes before the door's).
PACE_HELD_SAID_S = 120.0


class Pace:
    """A driver's pace: which rule it runs under, the samples it holds the clock for and
    since when on the driver's own clock, and the line said once for a long hold."""

    def __init__(self, world: World, rule: str = PACE_RULE):
        self.world = world
        self.rule = rule
        world.pace_rule = rule  # type: ignore[attr-defined]
        self.since: dict[str, float] = {}
        self.said: set[str] = set()

    def open(self) -> list[dict[str, Any]]:
        from freesail.agents.harness import open_samples

        return open_samples(self.world)

    def rate(self, compression: float, now: float | None = None) -> float:
        """The compression the clock runs at now: 1x while a sample is open under the
        pace rule, the set compression otherwise. Keeps the hold's start per station
        and says the long hold once (`PACE_HELD_SAID_S`)."""
        if self.rule != PACE_RULE:
            self.since.clear()
            self.said.clear()
            return compression
        now = time.monotonic() if now is None else now
        held = self.open()
        names = {o["station"] for o in held}
        for o in held:
            self.since.setdefault(o["station"], now)
        for name in list(self.since):
            if name not in names:
                del self.since[name]
                self.said.discard(name)
        for o in held:
            name = o["station"]
            for_s = now - self.since[name]
            if for_s >= PACE_HELD_SAID_S and name not in self.said:
                self.said.add(name)
                self.world.record_driver(
                    "routine",
                    "driver.pace",
                    f"The clock has been held at 1x for the {name} for {int(for_s)} real "
                    f"seconds; its sample has been open since {o['since']} ({o['reason']}).",
                    data={"station": name, "for_s": int(for_s), "since": o["since"]},
                )
        return 1.0 if names else compression

    def state(self, compression: float, now: float | None = None) -> dict[str, Any]:
        """For the snapshot and `state`: the rule, the set compression, the rate now, and
        each open sample with since when and for how many real seconds."""
        now = time.monotonic() if now is None else now
        held = self.open() if self.rule == PACE_RULE else []
        return {
            "rule": self.rule,
            "compression": compression,
            "rate": 1.0 if held else compression,
            "held": bool(held),
            "open": [dict(o, for_s=int(now - self.since.get(o["station"], now))) for o in held],
        }

    def words(self, compression: float) -> str:
        """One line for the owner: 'The clock runs at 60x; held at 1x while the captain's
        sample is open (since 04:10, the glass).'"""
        d = self.state(compression)
        if d["rule"] == PACE_LOCKSTEP:
            return (
                f"The clock runs at {compression:g}x, in lockstep (it waits for a door with "
                "the floor)."
            )
        if d["rule"] == PACE_FREE:
            return f"The clock runs free at {compression:g}x: no model's sample slows it."
        if not d["open"]:
            return f"The clock runs at {compression:g}x; no sample is open."
        held = "; ".join(
            f"the {o['station']}'s since {o['since']} ({o['reason']}, {o['for_s']} s)"
            for o in d["open"]
        )
        return f"The clock is held at 1x (set {compression:g}x) while a sample is open: {held}."


def pace_rule_of(args: Any) -> str:
    """The pace rule a driver's flags ask for: `--lockstep`, `--free-running`, else the
    pace rule (the default)."""
    if getattr(args, "lockstep", False):
        return PACE_LOCKSTEP
    if getattr(args, "free_running", False):
        return PACE_FREE
    return PACE_RULE


FREE_RUNNING_HELP = (
    "run at the set compression with no slowing while a model's sample is open (the solo "
    "player's flag; the default is the pace rule of spec M6 §12, 1x while a sample is open)"
)


def restore_python_rules(world: World, data: dict) -> None:
    """A save's standing orders written in Python (spec M4 §4) have no journal line to
    replay them by; list them in the loaded book, belayed, with the sentence."""
    from freesail.standing import restore_absent

    restore_absent(world, data.get("standing_orders", []))


class Console:
    def __init__(
        self,
        world: World,
        compression: float = 1.0,
        out=sys.stdout,
        lockstep: bool = False,
        replay_anyway: bool = False,
        free_running: bool = False,
    ):
        self.world = world
        self.replay_anyway = replay_anyway  # `--replay-anyway` given at the start
        self.compression = clamp_compression(compression)
        self.world.compression = self.compression
        self.lockstep = lockstep
        # the pace rule (package 41): 1x while a sample is open, unless in lockstep or
        # free-running
        self.pace = Pace(
            world, PACE_LOCKSTEP if lockstep else PACE_FREE if free_running else PACE_RULE
        )
        self.desk: Any = None  # the agent API's stations, with --agents-port
        self.running = False
        self.out = out
        self._view = RollupView()  # the roll-up (spec M4 §20)
        self._alarm: Event | None = None  # an urgent line seen while running fast
        self.lock = threading.RLock()  # the clock thread and the prompt share the world
        self._stop = threading.Event()
        self._attach()

    # -- log printing --------------------------------------------------------

    def _attach(self) -> None:
        self.world.log.subscribe(self._on_event)
        self.world.compression = self.compression

    def _detach(self) -> None:
        self.world.log.unsubscribe(self._on_event)

    def _on_event(self, e: Event) -> None:
        if (
            e.severity is Severity.URGENT
            and self.running
            and self.compression > ALARM_SPEED
            and self._alarm is None
        ):
            self._alarm = e  # eased once the tick is over (`_run`)
        for x in self._view.feed(e, self.compression):
            self._show(x)

    def _show(self, x: Shown) -> None:
        self._print(x.line())

    def set_compression(self, value: float) -> None:
        """`speed N` (or `time N`): the roll-up lets go of an hour it holds when the speed
        comes down below its threshold, so nothing held is left unsaid."""
        self.compression = clamp_compression(value)
        self.world.compression = self.compression
        if self._view.holding and not _rolls_up(self.compression):
            for x in self._view.flush():
                self._show(x)

    def _ease(self) -> None:
        """Auto-slow (spec M4 open item 8): the compression eased to ALARM_SPEED, and the
        log says so, as a driver's line a replay writes again (`World.record_driver`)."""
        e, self._alarm = self._alarm, None
        if e is None or self.compression <= ALARM_SPEED:
            return
        was = self.compression
        self.set_compression(ALARM_SPEED)
        self.world.record_driver(
            Severity.NOTABLE,
            "driver.eased",
            eased_words(e),
            data={"from": was, "to": ALARM_SPEED, "tick": e.tick, "kind": e.kind},
        )

    def _print(self, text: str) -> None:
        print(text, file=self.out, flush=True)

    # -- commands ------------------------------------------------------------

    def handle_line(self, line: str) -> bool:
        """Handle one line of input. Returns False when the console should exit."""
        line = line.strip()
        if not line:
            return True
        words = line.split()
        cmd, args = words[0].lower(), words[1:]
        if cmd == "quit" or cmd == "exit":
            return False
        if cmd == "help":
            self._print(HELP)
        elif cmd == "hold":
            self.running = False
            self._print("Clock held.")
        elif cmd == "go":
            self.running = True
            self._print(f"Clock running at {self.compression:g}x.")
        elif cmd in SPEED_WORDS:
            try:
                wanted = float(args[0])
                self.set_compression(wanted)
                most = " (the most there is)" if wanted > MAX_COMPRESSION else ""
                self._print(f"Compression {self.compression:g}x{most}.")
            except (IndexError, ValueError):
                self._print(f"Say '{cmd} 30' for thirty game seconds per real second.")
        elif cmd == "tick":
            n = int(args[0]) if args else 1
            self.running = False
            done = self._run(n)
            if done < n:
                self._print(
                    f"Advanced {done} ticks to {self.world.clock.stamp()}; the clock waits for "
                    f"{self.held_for()} (--lockstep)."
                )
            else:
                self._print(f"Advanced {n} ticks to {self.world.clock.stamp()}.")
        elif cmd == "state":
            for s in self.world.summary_lines():
                self._print(s)
            if self.desk is not None:
                for s in self.desk.lines():
                    self._print(s)
            else:
                for agent in self.world.agents.values():
                    self._print(f"The {agent.station.name}: {agent.agent.words()}.")
            held = self.held_for()
            if held is not None:
                self._print(f"The clock waits for {held} (--lockstep).")
            elif self.world.agents:
                self._print(self.pace.words(self.compression))
        elif self._is_muster(line):
            # a query, like `state`: printed, never journaled (spec M3 §5.1)
            for s in queries.muster_lines(self.world):
                self._print(s)
        elif " ".join(line.lower().split()) in ("the sail room", "sail room"):
            # a query too (spec 3b §6.3): what is in the sail room, never journaled
            for s in queries.sail_room_lines(self.world):
                self._print(s)
        elif " ".join(line.lower().split()) in queries.BOOMS_QUERIES:
            # and the spare spars (package 30b), in the same form
            for s in queries.booms_lines(self.world):
                self._print(s)
        elif self._is_read_standing_orders(line):
            # the driver's business, since it reads the disk (spec M4 §3): each line of
            # the file is given as an order, journaled, and printed by the log
            self._read_standing_orders(line)
        elif self._is_book_query(line):
            # the book (spec M4 §3): a query like `state`, printed, never journaled
            for s in self._book_lines(line):
                self._print(s)
        elif cmd == "log":
            n = int(args[0]) if args else 20
            for e in self.world.log.tail(n):
                self._print(e.line())
        elif cmd == "save":
            if not args:
                self._print("Say 'save somewhere.json'.")
            else:
                p = replay_mod.save_to_file(self.world, args[0])
                self._print(f"Saved to {p} at tick {self.world.clock.tick}.")
        elif cmd == "replay":
            anyway = REPLAY_ANYWAY_FLAG in args
            paths = [a for a in args if a != REPLAY_ANYWAY_FLAG]
            if not paths:
                self._print("Say 'replay somewhere.json'.")
            else:
                self._replay(paths[0], replay_anyway=anyway or self.replay_anyway)
        else:
            seat = getattr(self.world, "player_seat", None)
            if seat is not None and not seat.agent.released:
                # the player's seat at a station (package 40): the line is the owner's
                # where it is his, the seat's otherwise, judged by its authority
                e = seat.route(line)
            else:
                e = self.world.submit(line)
            if e is not None and e.kind in UNLOGGED_KINDS:
                # an answer for the one who asked and not a line of the log (package 40b:
                # the master's slate), printed here as a station reads it in its reply
                self._print(e.line())
        return True

    @staticmethod
    def _is_muster(line: str) -> bool:
        """'muster', 'muster the crew' and the vocabulary's other words for it."""
        from freesail.orders.vocabulary import key, load_vocabulary

        vocab = load_vocabulary()
        return vocab.phrase_to_verb.get(key(line)) == "muster"

    @staticmethod
    def _is_read_standing_orders(line: str) -> bool:
        return read_standing_orders_path(line) is not None

    def _read_standing_orders(self, line: str) -> None:
        path = read_standing_orders_path(line) or ""
        try:
            n = read_standing_orders(self.world, path)
        except OSError as e:
            self._print(f"Could not read {path}: {e.strerror or e}.")
            return
        self._print(f"Read {n} standing order{'s' if n != 1 else ''} from {path}.")

    @staticmethod
    def _is_book_query(line: str) -> bool:
        from freesail.standing.grammar import recognises

        return recognises(line) in ("standing orders", "show standing order")

    def _book_lines(self, line: str) -> list[str]:
        from freesail.standing.grammar import parse_book_command

        try:
            command = parse_book_command(line)
            _, text, _ = self.world.standing.book.carry_out(command)
        except OrderError as e:
            return [str(e)]
        return text.split("\n")

    def _replay(self, path: str, replay_anyway: bool = False) -> None:
        data = replay_mod.load_file(path)
        # the load's rule (package 37d): another build's game with a station's transcript
        # in it is not replayed unless asked for, and the words say why
        try:
            report = replay_mod.check_replay(data, path, replay_anyway)
        except replay_mod.ReplayRefused as refused:
            for line in refused.report.words:
                self._print(line)
            return
        self.running = False
        self._detach()
        self._view = RollupView()
        self._print(f"Replaying {path} to tick {data['end_tick']}...")
        from freesail.api.session import ship_factory

        self.world = replay_mod.replay(data, ship_factory, road=report.road)
        self._attach()
        self.pace = Pace(self.world, self.pace.rule)
        restore_python_rules(self.world, data)  # attached, so its lines are printed
        self._print(f"Replayed. Log digest {self.world.log.digest()[:16]}. Clock held.")
        for line in report.words:
            self._print(line)
        for s in self.world.summary_lines():
            self._print(s)

    # -- main loop -----------------------------------------------------------

    def loop(self, lines: queue.Queue[str]) -> None:
        """Piped or scripted input: one thread, lines from a queue, ticks between."""
        period = 0.1
        owed = 0.0
        while True:
            try:
                while True:
                    line = lines.get_nowait()
                    with self.lock:  # the agent API's thread shares the world
                        if not self.handle_line(line):
                            return
            except queue.Empty:
                pass
            owed = self._tick_owed(owed, period)
            time.sleep(period)

    def held_for(self) -> str | None:
        """In lockstep, the station whose door has the floor, which the clock waits for."""
        if not self.lockstep or self.desk is None:
            return None
        with self.lock:
            return self.desk.holding()

    def _run(self, n: int) -> int:
        """Run up to n ticks; in lockstep, stop where a door has the floor; on an alarm,
        stop and ease the compression. Returns how many ran."""
        for k in range(n):
            if self.held_for() is not None:
                return k
            self.world.tick()
            if self._alarm is not None:
                self._ease()
                return k + 1
        return n

    def _tick_owed(self, owed: float, period: float) -> float:
        if self.running:
            with self.lock:
                # the pace rule (package 41): 1x while a model's sample is open
                rate = self.pace.rate(self.compression)
            owed += rate * period
            n = int(owed)
            owed -= n
            with self.lock:
                self._run(n)
        with self.lock:
            # the unattended bound on this driver's clock, running or not: ten real minutes
            # of a pause unanswered, however fast the ship's clock runs (package 31c)
            check_agents_unattended(self.world)
        return owed

    def serve_agents(
        self,
        port: int,
        host: str = "127.0.0.1",
        records_dir: str | None = None,
        saves_dir: str | None = None,
    ) -> Any:
        """Host the agent API on `port` in a thread, on this console's lock (spec M4 §13
        as revised). Returns the uvicorn server (its `should_exit` stops it)."""
        import uvicorn
        from fastapi import FastAPI

        from freesail.ui.server import agent_routes

        options: dict[str, Any] = {
            "game": f"FreeSail's console (freesail.ui.console, agents on port {port})",
            "lockstep": self.lockstep,
            "say": self._print,
        }
        if records_dir:
            options["records_dir"] = records_dir
        if saves_dir:
            options["saves_dir"] = saves_dir
        router = agent_routes(self.lock, lambda: self.world, **options)
        self.desk = router.desk  # type: ignore[attr-defined]
        app = FastAPI(title="FreeSail agents")
        app.include_router(router)
        server = uvicorn.Server(uvicorn.Config(app, host=host, port=port, log_level="warning"))
        threading.Thread(target=server.run, daemon=True).start()
        return server

    def _clock_thread(self) -> None:
        period = 0.1
        owed = 0.0
        while not self._stop.is_set():
            owed = self._tick_owed(owed, period)
            time.sleep(period)

    def run_interactive(self) -> None:
        """A real terminal: the clock runs in a thread; the prompt owns the screen.

        prompt_toolkit's patch_stdout redraws the half-typed order underneath
        every log line that arrives, so nothing you are typing is swallowed.
        """
        from prompt_toolkit import PromptSession
        from prompt_toolkit.completion import Completer, Completion
        from prompt_toolkit.patch_stdout import patch_stdout

        from freesail.orders.complete import suggestions

        console = self

        class OrdersCompleter(Completer):
            """Offers whole orders the parser would accept, as the player types."""

            def get_completions(self, document, complete_event):
                text = document.text_before_cursor
                with console.lock:
                    cands = suggestions(console.world.ship, text)
                for c in cands:
                    yield Completion(c, start_position=-len(text))

        session: PromptSession[str] = PromptSession(
            completer=OrdersCompleter(), complete_while_typing=True
        )
        ticker = threading.Thread(target=self._clock_thread, daemon=True)
        with patch_stdout(raw=True):
            ticker.start()
            try:
                while True:
                    try:
                        line = session.prompt("> ")
                    except (EOFError, KeyboardInterrupt):
                        break
                    with self.lock:
                        if not self.handle_line(line):
                            break
            finally:
                self._stop.set()


def _rolls_up(compression: float) -> bool:
    from freesail.core.events import rolls_up

    return rolls_up(compression)


def start_world(args: argparse.Namespace) -> tuple[World, Any]:
    """The World a driver starts with, from its command line (shared with the server):
    `--load SAVE` takes a save up at its last tick, from its checkpoint or by a replay
    (`core.replay.load_report`, whose report is left on the World as `load_report` for
    `loaded_words`; a replay refused stops the driver with the words); `--scenario FILE`
    builds the scenario's
    world (the orders it names are given by the caller, after the watcher is stationed);
    otherwise the ship, the seed, `--wind` and `--heading`. Returns the World and the
    scenario file read, if any."""
    from freesail.api.session import make_world, ship_factory

    if getattr(args, "load", None):
        # from the checkpoint beside the save when it belongs to it (package 33a: seconds
        # for a day's save), else by replaying the journal; another build's game with a
        # station's transcript in it is not replayed unless asked for (package 37d)
        try:
            world, report = replay_mod.load_report(
                args.load, ship_factory, replay_anyway=bool(getattr(args, "replay_anyway", False))
            )
        except replay_mod.ReplayRefused as refused:
            raise SystemExit("\n".join(refused.report.words)) from None
        if report.how == "replay":
            restore_python_rules(world, replay_mod.load_file(args.load))
        world.loaded_from = report.how  # type: ignore[attr-defined]
        world.load_report = report  # type: ignore[attr-defined]
        return world, None
    if getattr(args, "scenario", None):
        from freesail.world.scenarios import load_scenario, make_scenario_world

        sf = load_scenario(args.scenario)
        if args.wind:
            raise SystemExit("--wind and --scenario: the scenario's weather script is the wind.")
        if args.heading is not None:
            sf.scenario.ship_heading_deg = args.heading
        return make_scenario_world(sf, seed=args.seed, ship=args.ship), sf
    seed = args.seed if args.seed is not None else DEFAULT_SEED
    scenario = Scenario()
    if args.wind:
        d, s = args.wind.split(",")
        scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
    if args.heading is not None:
        scenario.ship_heading_deg = args.heading
    if args.ship:
        return make_world(seed, args.ship, scenario), None
    return World(seed=seed, scenario=scenario), None


# The seed without a scenario or `--seed` (the drivers' default since M0).
DEFAULT_SEED = 1805

# Every door that loads or replays a save takes this flag (package 37d): a save of another
# build that holds a station's transcript is replayed only when it is given.
REPLAY_ANYWAY_FLAG = "--replay-anyway"
SEAT_HELP = (
    "seat the player at a station below the captain's ('officer'): his orders are judged "
    "by that station's authority and the captain's word (package 40; spec M6 §3)"
)

REPLAY_ANYWAY_HELP = (
    "replay a save all the same when it was written by another build and holds a "
    "station's transcript (the replay is then not the game that was played); without it "
    "such a save is loaded from its checkpoint or refused in words"
)


def loaded_words(world: World, path: str) -> list[str]:
    """What a door prints for a game loaded with `--load`: the road taken, the tick and
    the log's digest, then the load's own words (which build wrote the save or the
    checkpoint, why a checkpoint was not used, that a replay's log may differ)."""
    report = getattr(world, "load_report", None)
    how = report.how if report is not None else getattr(world, "loaded_from", "replay")
    way = "from its checkpoint at" if how == "checkpoint" else "replayed to"
    lines = [
        f"Loaded {path}: {way} tick {world.clock.tick}, {world.clock.stamp()}; the log's "
        f"digest is {world.log.digest()[:16]}."
    ]
    if report is not None:
        lines += list(report.words)
    return lines


def _stdin_reader(q: queue.Queue[str]) -> None:
    for line in sys.stdin:
        q.put(line)
    q.put("quit")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail console")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, help="the seed (default a scenario's, else 1805)")
    ap.add_argument(
        "--time", "--speed", type=float, default=1.0, help="compression, game s per real s"
    )
    ap.add_argument("--load", help="save file to replay and continue from")
    ap.add_argument(REPLAY_ANYWAY_FLAG, action="store_true", help=REPLAY_ANYWAY_HELP)
    ap.add_argument(
        "--scenario",
        help="a scenario file: ship, start, weather script, orders (spec M4 §19)",
    )
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS', e.g. 225,15")
    ap.add_argument("--heading", type=float, help="starting heading in degrees")
    ap.add_argument(
        "--standing-orders",
        help="a file of standing orders to give at the start (spec M4 §6); the starter "
        f"book is {STARTER_BOOK}, a choice: without it the book begins empty",
    )
    ap.add_argument(
        "--watcher", help="station a watcher: 'fake' for the scripted narrator (spec M4 §12)"
    )
    ap.add_argument(
        "--agents-port",
        type=int,
        help="host the agent API on this port, so a model's door can attach (spec M4 §13)",
    )
    ap.add_argument(
        "--lockstep",
        action="store_true",
        help="hold the clock while a model's door has the floor (spec M4 §13)",
    )
    ap.add_argument(
        "--consent-records",
        help="where the consent records are read and written (default docs/agents/consent)",
    )
    ap.add_argument("--saves", help="where a released station saves the game (default saves/)")
    ap.add_argument("--seat", help=SEAT_HELP)
    ap.add_argument("--free-running", action="store_true", help=FREE_RUNNING_HELP)
    args = ap.parse_args(argv)

    world, scenario_file = start_world(args)
    if args.watcher:
        # stationed before any order of this tick, which is where a replay stations it
        station_watcher(world, args.watcher, out=sys.stdout)
    if scenario_file is not None:
        from freesail.world.scenarios import begin

        begin(world, scenario_file)
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)
    if args.seat:
        seat_player(world, args.seat, door="console")

    console = Console(
        world,
        compression=args.time,
        lockstep=args.lockstep,
        replay_anyway=args.replay_anyway,
        free_running=args.free_running,
    )
    if scenario_file is not None:
        for line in scenario_file.lines():
            console._print(line)
    for e in world.log.all():
        console._print(e.line())
    console._print(
        f"FreeSail console. Seed {world.seed}. {units.time_stamp(world.clock.ship_time)}. "
        "Type 'help' for driver commands, 'go' to start the clock."
    )
    console._print(book_words(world))  # the starter book a choice (package 33c)
    if args.load:
        for line in loaded_words(world, args.load):  # the road taken, and why (package 37d)
            console._print(line)
    if args.agents_port:
        console.serve_agents(
            args.agents_port, records_dir=args.consent_records, saves_dir=args.saves
        )
        console._print(
            f"A model's door connects to http://localhost:{args.agents_port} "
            "(docs/agents/Harness.md)"
            + ("; the clock waits for it (--lockstep)." if args.lockstep else ".")
        )
    if sys.stdin.isatty():
        console.run_interactive()
    else:
        q: queue.Queue[str] = queue.Queue()
        threading.Thread(target=_stdin_reader, args=(q,), daemon=True).start()
        console.loop(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
