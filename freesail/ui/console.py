"""The console driver: runs a world, prints the log, reads orders from stdin.

    python -m freesail.ui.console [--seed N] [--time N] [--load SAVE]

Driver commands (not ship orders, not journaled):
    hold            pause the clock
    go              run the clock
    time N          set compression to N game seconds per real second
    tick N          advance N ticks, then hold
    state           print a summary of the ship and the weather
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
from freesail.core import replay as replay_mod
from freesail.core.events import Event, Severity
from freesail.core.world import Scenario, World

HELP = __doc__.split("Driver commands")[1] if __doc__ else ""


class Console:
    ROLLUP_ABOVE = 10  # compression above which routine entries are rolled up per bell

    def __init__(self, world: World, compression: float = 1.0, out=sys.stdout):
        self.world = world
        self.compression = compression
        self.running = False
        self.out = out
        self._rolled_up = 0
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

    def _replay(self, path: str) -> None:
        data = replay_mod.load_file(path)
        self.running = False
        self._detach()
        self._print(f"Replaying {path} to tick {data['end_tick']}...")
        self.world = replay_mod.replay(data)
        self._attach()
        self._print(f"Replayed. Log digest {self.world.log.digest()[:16]}. Clock held.")
        for s in self.world.summary_lines():
            self._print(s)

    # -- main loop -----------------------------------------------------------

    def loop(self, lines: queue.Queue[str]) -> None:
        period = 0.1
        owed = 0.0
        while True:
            try:
                while True:
                    if not self.handle_line(lines.get_nowait()):
                        return
            except queue.Empty:
                pass
            if self.running:
                owed += self.compression * period
                n = int(owed)
                owed -= n
                self.world.run(n)
            time.sleep(period)


def _stdin_reader(q: queue.Queue[str]) -> None:
    for line in sys.stdin:
        q.put(line)
    q.put("quit")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="FreeSail console")
    ap.add_argument("ship", nargs="?", help="ship file (ignored in M0; the ship is a point)")
    ap.add_argument("--seed", type=int, default=1805)
    ap.add_argument("--time", type=float, default=1.0, help="compression, game s per real s")
    ap.add_argument("--load", help="save file to replay and continue from")
    ap.add_argument("--wind", help="wind as 'FROM_DEG,KNOTS', e.g. 225,15")
    args = ap.parse_args(argv)

    if args.load:
        world = replay_mod.replay(replay_mod.load_file(args.load))
    else:
        scenario = Scenario()
        if args.wind:
            d, s = args.wind.split(",")
            scenario.wind_from_deg, scenario.wind_speed_kn = float(d), float(s)
        world = World(seed=args.seed, scenario=scenario)

    console = Console(world, compression=args.time)
    for e in world.log.all():
        console._print(e.line())
    console._print(
        f"FreeSail console. Seed {world.seed}. {units.time_stamp(world.clock.ship_time)}. "
        "Type 'help' for driver commands, 'go' to start the clock."
    )
    q: queue.Queue[str] = queue.Queue()
    threading.Thread(target=_stdin_reader, args=(q,), daemon=True).start()
    console.loop(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
