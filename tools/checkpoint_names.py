"""The names the game's own checkpoints hold (package 115, part B; the cold review's 5.4).

    python tools/checkpoint_names.py            # the census, compared with the list
    python tools/checkpoint_names.py --write    # the list written again from the census
    python tools/checkpoint_names.py --write --jobs 4   # the same, on four processes

A checkpoint (`freesail/core/replay.py`) is a pickle, and a pickle names the classes and
functions its loading calls. The loader admits an exact list of those names
(`freesail/core/checkpoint_names.py`, `ADMITTED`) and nothing else. This tool makes the
list from what the game's own checkpoints hold: every scenario under `data/scenarios/`
begun as the harbour begins it (the server's `prepare_game`), run and checkpointed; the
kept saves under `tests/fixtures/saves/`, and each played on with a station left in it
taken again; a fight; a port, a ship in it and her business; the far world; the wardroom
(`wardroom_world`: the stations seated as play seats them, the watcher, the player at a
seat, a captain and an officer at work); a practice at the great guns (`practice_world`: a
cask heaved over and engaged); and a boat away as a hull (`boat_world`: under oars, then
under her lug). The list is written from a long census (`LIST_RUN_S`, two hours of each
scenario, where the fishermen's gear is out and the people's needs have come due) and the
kin of every class it meets (`kin`); truth 7-606 (`tests/test_known_truths.py`) takes the
short one (`RUN_S`, ten minutes) and fails when any checkpoint of the game's own holds a
name the list lacks, so that a new class in a checkpoint is added to the list on purpose
and seen in the diff.

The census reads the game's own pickles with a recording loader; it never reads a
checkpoint from elsewhere.
"""

from __future__ import annotations

import argparse
import gzip
import pickle
import sys
from collections.abc import Iterator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENARIOS = ROOT / "data" / "scenarios"
FIXTURES = ROOT / "tests" / "fixtures" / "saves"
LIST_FILE = ROOT / "freesail" / "core" / "checkpoint_names.py"
RUN_S = 600  # ten minutes of each scenario: its routine, its runner and its book under way
LIST_RUN_S = 7200  # the list's census: two hours of each (JUDGEMENT: past the first watch)

# The game's own worlds beyond the scenarios' openings (name, scenario, seconds run, orders
# given first): a fight with the guns cast loose and fired, a port with the ship's business
# done in it, and the far world.
WORLDS: tuple[tuple[str, str, int, tuple[str, ...]], ...] = (
    (
        "a fight",
        "first-action.yaml",
        1800,
        ("beat to quarters", "cast loose the guns", "fire as they bear"),
    ),
    ("a port", "merchant-passage.yaml", 3600, ()),
    ("the far world", "madeira.yaml", 3600, ()),
)


class _Census(pickle.Unpickler):
    """The game's own pickle read with every name it calls recorded."""

    def __init__(self, f, seen: set[tuple[str, str]]):
        super().__init__(f)
        self.seen = seen

    def find_class(self, module: str, name: str):  # type: ignore[no-untyped-def]
        self.seen.add((module, name))
        return super().find_class(module, name)


def names_of_bytes(body: bytes) -> set[tuple[str, str]]:
    import io

    seen: set[tuple[str, str]] = set()
    _Census(io.BytesIO(body), seen).load()
    return seen


def names_of_file(path: Path) -> set[tuple[str, str]]:
    seen: set[tuple[str, str]] = set()
    with gzip.open(path, "rb") as f:
        f.readline()  # the header, JSON
        _Census(f, seen).load()
    return seen


def scenario_world(path: Path, run_s: int, orders: tuple[str, ...] = ()):
    """A scenario begun as the harbour begins it, run, its orders given first."""
    from freesail.ui.server import prepare_game, server_parser

    args = server_parser().parse_args(["--scenario", str(path)])
    world = prepare_game(args, say=lambda _line: None)
    for order in orders:
        world.submit(order)
    world.run(run_s)
    return world


def wardroom_world(run_s: int = 3600):
    """The stations seated, as play seats them: a scenario begun as the harbour begins it
    with the scripted watcher and the player at the master's seat, the fake captain and
    the fake officer each through a harness of his own, the captain giving the officer the
    deck and his word, the officer at work and standing by; run an hour."""
    from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call
    from freesail.agents.agent import captain, officer
    from freesail.agents.fake import captain_of_the_ship
    from freesail.ui.server import prepare_game, server_parser

    args = server_parser().parse_args(
        ["--scenario", str(SCENARIOS / "merchant-cutter.yaml"), "--watcher", "fake"]
        + ["--seat", "master"]
    )
    world = prepare_game(args, say=lambda _line: None)
    policy = SamplingPolicy.in_lockstep(600, "notable", "urgent")
    orders = ["trim sails", "heave the log"]

    def keep_her(last, turns):  # type: ignore[no-untyped-def]
        if "tool_results" in last:
            return Reply()
        if orders:
            return Reply(calls=(call("submit_order", text=orders.pop(0)),))
        return Reply(calls=(call("stand_by", until="eight bells"),))

    oh = Harness(world, officer(policy, world=world), Fake([keep_her], loop=True), save=None)
    oh.start()
    words = ["you have the deck", "you may work the ship", "ask the master for a course"]
    ch = Harness(world, captain(policy, world=world), captain_of_the_ship(words), save=None)
    ch.start()
    world.run(run_s)
    return world


def scenario_files() -> list[Path]:
    return sorted(SCENARIOS.glob("*.yaml"))


def census_of_scenario(path: Path, run_s: int = RUN_S, orders: tuple[str, ...] = ()):
    from freesail.core import replay

    return names_of_bytes(replay.checkpoint_bytes(scenario_world(path, run_s, orders)))


def jobs(run_s: int = LIST_RUN_S) -> list[tuple]:
    """The census's checkpoints, each a job a worker can take."""
    out: list[tuple] = [("fixture", p.name) for p in sorted(FIXTURES.glob("*.checkpoint"))]
    out += [("kept", p.name) for p in sorted(FIXTURES.glob("*.json"))]
    for path in scenario_files():
        # ten minutes (an evolution under way) and the long run (what the hours bring)
        out += [("scenario", path.name, seconds) for seconds in sorted({RUN_S, run_s})]
    out += [("world", i) for i in range(len(WORLDS))]
    out += [("wardroom",), ("practice",), ("boat",)]
    return out


def run_job(job: tuple) -> tuple[str, set[tuple[str, str]]]:
    kind = job[0]
    if kind == "fixture":
        return f"the kept save {job[1]}", names_of_file(FIXTURES / job[1])
    if kind == "kept":
        return f"the kept save {job[1]}, played on", census_of_kept_save(FIXTURES / job[1])
    if kind == "scenario":
        return f"the scenario {job[1]} at {job[2]} s", census_of_scenario(
            SCENARIOS / job[1], job[2]
        )
    if kind == "world":
        what, name, run_s, orders = WORLDS[job[1]]
        return what, census_of_scenario(SCENARIOS / name, run_s, orders)
    what, make = {
        "wardroom": ("the wardroom", census_of_wardroom),
        "practice": ("a practice at the great guns", census_of_practice),
        "boat": ("a boat away", census_of_boat),
    }[kind]
    return what, make()


def census(
    say=print, run_s: int = LIST_RUN_S, workers: int = 1
) -> Iterator[tuple[str, set[tuple[str, str]]]]:
    """(where, names) for every checkpoint of the game's own the census takes, on
    `workers` processes (each checkpoint its own world)."""
    todo = jobs(run_s)
    if workers <= 1:
        for job in todo:
            say(f"  {job}")
            yield run_job(job)
        return
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(workers) as pool:
        for where, names in pool.map(run_job, todo):
            say(f"  {where}")
            yield where, names


def census_of_kept_save(path: Path, run_s: int = 3600):
    """A kept save taken up as a player takes one up (from its checkpoint), a station left
    in it taken again by a model, played on for an hour and checkpointed again: a station's
    sample open, a model's transcript under way."""
    from freesail.agents import Fake
    from freesail.core import replay

    world, _ = replay.load(path, replay_anyway=True)
    for h in list((getattr(world, "agents", None) or {}).values()):
        # a station left in the save taken again by a model, as a player's door takes it
        if getattr(h.agent, "released", False) and hasattr(h, "reseat"):
            h.reseat(Fake(["Aye."], loop=True), identity="the census", door="mcp", save=None)
    world.run(run_s)
    return names_of_bytes(replay.checkpoint_bytes(world))


def practice_world():
    """A forenoon's practice at the great guns, as the owner's scenario sails it
    (`exercising-the-great-guns`): quarters beaten, a battery exercised with the guns cast
    loose, a cask heaved overboard and engaged."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(SCENARIOS / "exercising-the-great-guns.yaml")
    world = make_scenario_world(sf)
    begin(world, sf)
    for order, then in (
        ("beat to quarters", 5),
        ("exercise the starboard battery", 0),
        ("cast loose the guns", 20 * 60),
        ("cease exercising", 60),
        ("heave a cask overboard from the starboard quarter", 120),
        ("engage the cask to starboard", 600),
    ):
        world.submit(order)
        world.run(then)
    return world


def boat_world():
    """A boat away as a hull of the one world (package 82), as the game sends her: the
    frigate of the naval cruise at anchor, `go to the launch` (her coxswain and oarsmen in
    her, the player with them), `give way` under oars, `step the mast`, `set the lug`, and
    sailed so a quarter of an hour."""
    from freesail.ui.server import prepare_game, server_parser

    args = server_parser().parse_args(["--scenario", str(SCENARIOS / "naval-cruise.yaml")])
    world = prepare_game(args, say=lambda _line: None)
    world.run(60)
    for order, then in (
        ("go to the launch", 30),
        ("give way", 600),
        ("step the mast", 300),
        ("set the lug", 900),
    ):
        world.submit(order)
        world.run(then)
    return world


def census_of_boat():
    from freesail.core import replay

    return names_of_bytes(replay.checkpoint_bytes(boat_world()))


def census_of_practice():
    from freesail.core import replay

    return names_of_bytes(replay.checkpoint_bytes(practice_world()))


def census_of_wardroom():
    from freesail.core import replay

    return names_of_bytes(replay.checkpoint_bytes(wardroom_world()))


def kin(names: set[tuple[str, str]]) -> set[tuple[str, str]]:
    """The classes of the game's kin to the census's: for each class the census met, every
    class of the game that shares a class of the game with it (its subclasses, and its
    base's other subclasses: every evolution's script beside the scripts met, `CrewedWorld`
    beside `World`), and every record (a dataclass or an enum) of a module the census met a
    class of, by its exact name. JUDGEMENT: play reaches a script, a world or a record of a
    family by roads no census of scenarios walks whole (a boom shifted, a ship crewed close
    by, the captain's grant to his officer), and a class of the family, or a record of the
    same module, is the same kind of state; a function, a name of another library, and a
    class of a module no checkpoint holds are admitted only as met."""
    import importlib
    import pkgutil

    import freesail

    for m in pkgutil.walk_packages(freesail.__path__, "freesail."):
        if not m.name.endswith("__main__"):
            importlib.import_module(m.name)

    def below(c: type):  # type: ignore[no-untyped-def]
        for s in c.__subclasses__():
            yield s
            yield from below(s)

    import dataclasses
    import enum
    import inspect

    out: set[tuple[str, str]] = set()
    for module in {m for m, _ in names if m.startswith("freesail.")}:
        # the module's other records: its dataclasses and its enums, data made from their
        # fields alone (the captain's grant beside the stand-by, a fishing ground's lot)
        mod = importlib.import_module(module)
        for _, c in inspect.getmembers(mod, inspect.isclass):
            if c.__module__ == module and (dataclasses.is_dataclass(c) or issubclass(c, enum.Enum)):
                out.add((module, c.__qualname__))
    for module, name in names:
        if not module.startswith("freesail."):
            continue
        obj: object = importlib.import_module(module)
        for part in name.split("."):
            obj = getattr(obj, part, None)
        if not isinstance(obj, type):
            continue
        for family in obj.__mro__:
            if not family.__module__.startswith("freesail."):
                continue
            for s in below(family):
                if s.__module__.startswith("freesail.") and "<locals>" not in s.__qualname__:
                    out.add((s.__module__, s.__qualname__))
    return out


def write_list(names: set[tuple[str, str]]) -> str:
    lines = [
        '"""The names a checkpoint may hold, exactly (package 115, part B): written by',
        "`tools/checkpoint_names.py --write` from the census of the game's own checkpoints,",
        "and checked against it by `tests/test_known_truths.py` (truth 7-606). A name is added",
        "here on purpose, by the tool, and is seen in the diff; nothing is admitted by its module.",
        '"""',
        "",
        "ADMITTED: frozenset[tuple[str, str]] = frozenset(",
        "    {",
    ]
    lines += [f'        ("{m}", "{n}"),' for m, n in sorted(names)]
    lines += ["    }", ")", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true", help="write the list from the census")
    ap.add_argument("--jobs", type=int, default=1, help="the census on this many processes")
    args = ap.parse_args(argv)
    from freesail.core.checkpoint_names import ADMITTED
    from freesail.core.replay import BOUND_METHODS

    found: set[tuple[str, str]] = set()
    for where, names in census(workers=args.jobs):
        lacking = names - ADMITTED - {("builtins", "getattr")}
        if lacking:
            print(f"{where}: not in the list: {sorted(lacking)}")
        found |= names
    found.discard(("builtins", "getattr"))  # admitted by BOUND_METHODS alone, never by name
    while not kin(found) <= found:  # the kin of the kin, until nothing more comes
        found |= kin(found)
    print(f"{len(found)} names in the census; {len(ADMITTED)} in the list.")
    print(f"bound methods admitted: {sorted(BOUND_METHODS)}")
    unused = ADMITTED - found
    if unused:
        print(f"in the list and in no checkpoint of the census: {sorted(unused)}")
    if args.write:
        LIST_FILE.write_text(write_list(found), encoding="utf-8")
        print(f"written: {LIST_FILE.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
