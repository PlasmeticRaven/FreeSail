"""Run a lesson of the primer (docs/primer/18-lessons.md) once, at its scenario's seed, and
print its log: the tool package 40b measured the chapter's quotations with, so that the
lead or the owner can run a lesson again and read the same lines.

    py tools/lesson_run.py data/scenarios/lesson-landfall.yaml --until 05:30 \\
        --order "01:16 trim sails" \\
        --order "@sun.rise observe an amplitude" \\
        --order "@lookout.sighting~lizard take a bearing of the land"

The scenario is begun as a driver begins it (its standing orders and first orders at tick
0). Each `--order` is given at a time on the ship's clock ("HH:MM words", the first day or
the next; "+N words" for N seconds from the start), or on the tick after the first line of
the log of a kind ("@kind words"), or of a kind whose text holds a word ("@kind~word
words"; an underscore in the word stands for a space). Orders on one trigger are given in
the order they are listed. `--seat officer` seats the player at the officer of the
watch's station first (`--seat officer` at the console), and every order then goes
through the seat as a typed line does: the stations' sentences are the owner's, the rest
the officer's, judged by his authority.

The run ends at `--until` (a time on the clock) or after `--hours`. Every line of the log
is printed `tick  kind  line`, the line as the console prints it (its mark and its watch),
and an answer that is not a line of the log (the master's slate, `core.world.
UNLOGGED_KINDS`) is printed where it was given, its kind in brackets. `--quiet` leaves out
the bells, the gusts and the evolutions' steps. The digest of the log is the last line.

A lesson is tuned once and cheaply (the head rules of docs/dev/M6-WorkPackages.md): the
chapter quotes one run at its seed and says the seed; the orders and their times are in
docs/dev/TuningNotes.md under package 40b.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from freesail.core.world import UNLOGGED_KINDS  # noqa: E402
from freesail.world.scenarios import begin, load_scenario, make_scenario_world  # noqa: E402

# What `--quiet` leaves out: the bells, the gusts and the evolutions' small steps.
QUIET_KINDS = frozenset(
    {
        "clock.bell",
        "wind.gust",
        "evolution.step",
        "evolution.started",
        "evolution.short_handed",
        "sail.set",
        "sail.backed",
        "sail.filled",
        "ship.leeway",
        "weather.hour",
    }
)


def _at(start: datetime, words: str) -> int:
    """A tick from "HH:MM" (on the first day, or the next when it is before the start) or
    "+N" seconds."""
    if words.startswith("+"):
        return int(words[1:])
    hh, mm = (int(x) for x in words.split(":"))
    when = start.replace(hour=hh, minute=mm, second=0)
    if when < start:
        when += timedelta(days=1)
    return int((when - start).total_seconds())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("scenario")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--until", default=None, help="HH:MM on the clock")
    ap.add_argument("--hours", type=float, default=None)
    ap.add_argument("--order", action="append", default=[], help="'HH:MM words' or '@kind words'")
    ap.add_argument("--seat", default=None, help="'officer': the player seated at the station")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    sf = load_scenario(args.scenario)
    world = make_scenario_world(sf, seed=args.seed)
    start = world.clock.start
    timed: list[tuple[int, str]] = []
    on_kind: list[tuple[str, str, str]] = []
    for raw in args.order:
        head, _, words = raw.partition(" ")
        if head.startswith("@"):
            kind, _, match = head[1:].partition("~")
            on_kind.append((kind, match.replace("_", " "), words))
        else:
            timed.append((_at(start, head), words))
    timed.sort(key=lambda x: x[0])
    end = _at(start, args.until) if args.until else int((args.hours or 1.0) * 3600)
    begin(world, sf)
    seat = None
    if args.seat:
        from freesail.agents.seat import seat_player

        seat = seat_player(world, args.seat, door="console")
    replies: list[tuple[int, str]] = []

    def give(text: str) -> None:
        e = seat.route(text) if seat is not None else world.submit(text)
        if e is not None and e.kind in UNLOGGED_KINDS:
            replies.append((len(world.log), f"{e.tick}\t[{e.kind}]\t{e.line()}"))

    seen = 0
    due: list[str] = []
    while world.clock.tick < end:
        for text in due:
            give(text)
        due = []
        while timed and timed[0][0] <= world.clock.tick:
            give(timed.pop(0)[1])
        world.tick()
        events = world.log.all()
        for e in events[seen:]:
            for item in list(on_kind):
                kind, match, text = item
                if e.kind == kind and match.lower() in e.text.lower():
                    due.append(text)
                    on_kind.remove(item)
        seen = len(events)
    for i, e in enumerate(world.log):
        for at, line in replies:
            if at == i:
                print(line)
        if args.quiet and e.kind in QUIET_KINDS:
            continue
        print(f"{e.tick}\t{e.kind}\t{e.line()}")
    for at, line in replies:
        if at >= len(world.log):
            print(line)
    print(f"# seed {world.seed}; {len(world.log)} lines; digest {world.log.digest()[:16]}")


if __name__ == "__main__":
    main()
