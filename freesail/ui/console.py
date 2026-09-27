"""The console driver: runs a world, prints the log, reads orders from stdin.

    python -m freesail.ui.console [--seed N] [--time N] [--load SAVE] [--standing-orders FILE]

Driver commands (not ship orders, not journaled):
    hold            pause the clock
    go              run the clock
    time N          set compression to N game seconds per real second
    tick N          advance N ticks, then hold
    state           print a summary of the ship and the weather
    muster          muster the crew: the watch bill, station by station
    the sail room   what the sail room holds: each sail, its canvas and condition
    standing orders the book of standing orders, each with its state
    read the standing orders from FILE
                    give every standing order in the file (each is journaled)
    log [N]         print the last N log entries (default 20)
    save PATH       write a save file
    replay PATH     rebuild a world from a save and continue from it
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

from freesail import units
from freesail.api import queries
from freesail.core import replay as replay_mod
from freesail.core.events import Event, Severity
from freesail.core.world import Scenario, World
from freesail.ship.stub import OrderError

HELP = __doc__.split("Driver commands")[1] if __doc__ else ""

READ_STANDING_ORDERS = ("read the standing orders from", "load the standing orders from")


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


class Console:
    ROLLUP_ABOVE = 10  # compression above which routine entries are rolled up per bell

    def __init__(self, world: World, compression: float = 1.0, out=sys.stdout):
        self.world = world
        self.compression = compression
        self.running = False
        self.out = out
        self._rolled_up = 0
        self.lock = threading.RLock()  # the clock thread and the prompt share the world
        self._stop = threading.Event()
        self._attach()

    # -- log printing --------------------------------------------------------

    def _attach(self) -> None:
        self.world.log.subscribe(self._on_event)

    def _detach(self) -> None:
        self.world.log.unsubscribe(self._on_event)

    def _on_event(self, e: Event) -> None:
        rolling = self.running and self.compression > self.ROLLUP_ABOVE
        if rolling and e.severity is Severity.ROUTINE and e.kind != "clock.bell":
            self._rolled_up += 1
            return
        if e.kind == "clock.bell" and self._rolled_up:
            self._print(f"  ({self._rolled_up} routine entries)")
            self._rolled_up = 0
        self._print(e.line())

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
        elif cmd == "time":
            try:
                self.compression = max(0.1, float(args[0]))
                self._print(f"Compression {self.compression:g}x.")
            except (IndexError, ValueError):
                self._print("Say 'time 30' for thirty game seconds per real second.")
        elif cmd == "tick":
            n = int(args[0]) if args else 1
            self.running = False
            self.world.run(n)
            self._print(f"Advanced {n} ticks to {self.world.clock.stamp()}.")
        elif cmd == "state":
            for s in self.world.summary_lines():
                self._print(s)
        elif self._is_muster(line):
            # a query, like `state`: printed, never journaled (spec M3 §5.1)
            for s in queries.muster_lines(self.world):
                self._print(s)
        elif " ".join(line.lower().split()) in ("the sail room", "sail room"):
            # a query too (spec 3b §6.3): what is in the sail room, never journaled
            for s in queries.sail_room_lines(self.world):
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
            if not args:
                self._print("Say 'replay somewhere.json'.")
            else:
                self._replay(args[0])
        else:
            self.world.submit(line)
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

    def _replay(self, path: str) -> None:
        data = replay_mod.load_file(path)
        self.running = False
        self._detach()
        self._print(f"Replaying {path} to tick {data['end_tick']}...")
        from freesail.api.session import ship_factory

        self.world = replay_mod.replay(data, ship_factory)
        self._attach()
        self._print(f"Replayed. Log digest {self.world.log.digest()[:16]}. Clock held.")
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
                    if not self.handle_line(lines.get_nowait()):
                        return
            except queue.Empty:
                pass
            owed = self._tick_owed(owed, period)
            time.sleep(period)

    def _tick_owed(self, owed: float, period: float) -> float:
        if self.running:
            owed += self.compression * period
            n = int(owed)
            owed -= n
            with self.lock:
                self.world.run(n)
        return owed

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


def _stdin_reader(q: queue.Queue[str]) -> None:
    for line in sys.stdin:
        q.put(line)
    q.put("quit")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail console")
    ap.add_argument("ship", nargs="?", help="ship file, e.g. data/ships/frigate-36.yaml")
    ap.add_argument("--seed", type=int, default=1805)
    ap.add_argument("--time", type=float, default=1.0, help="compression, game s per real s")
    ap.add_argument("--load", help="save file to replay and continue from")
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS', e.g. 225,15")
    ap.add_argument("--heading", type=float, help="starting heading in degrees")
    ap.add_argument(
        "--standing-orders", help="a file of standing orders to give at the start (spec M4 §6)"
    )
    args = ap.parse_args(argv)

    from freesail.api.session import make_world, ship_factory

    if args.load:
        world = replay_mod.replay(replay_mod.load_file(args.load), ship_factory)
    else:
        scenario = Scenario()
        if args.wind:
            d, s = args.wind.split(",")
            scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
        if args.heading is not None:
            scenario.ship_heading_deg = args.heading
        if args.ship:
            world = make_world(args.seed, args.ship, scenario)
        else:
            world = World(seed=args.seed, scenario=scenario)
    if args.standing_orders:
        read_standing_orders(world, args.standing_orders)

    console = Console(world, compression=args.time)
    for e in world.log.all():
        console._print(e.line())
    console._print(
        f"FreeSail console. Seed {world.seed}. {units.time_stamp(world.clock.ship_time)}. "
        "Type 'help' for driver commands, 'go' to start the clock."
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
