"""The names the game's own checkpoints hold (package 115, part B; the cold review's 5.4).

    python tools/checkpoint_names.py            # the census, compared with the list
    python tools/checkpoint_names.py --write    # the list written again from the census

A checkpoint (`freesail/core/replay.py`) is a pickle, and a pickle names the classes and
functions its loading calls. The loader admits an exact list of those names
(`freesail/core/checkpoint_names.py`, `ADMITTED`) and nothing else. This tool makes the list
from what the game's own checkpoints hold: every scenario under `data/scenarios/` begun as
the harbour begins it (the server's `prepare_game`) and run `RUN_S` seconds of the game and
checkpointed; the kept saves under `tests/fixtures/saves/`; a fight; a port, a ship in it
and her business; the far world. Truth 7-606 (`tests/test_known_truths.py`) takes the
same census and fails when any checkpoint of the game's own holds a name the list lacks,
so that a new class in a checkpoint is added to the list on purpose and seen in the diff.

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


def scenario_files() -> list[Path]:
    return sorted(SCENARIOS.glob("*.yaml"))


def census_of_scenario(path: Path, run_s: int = RUN_S, orders: tuple[str, ...] = ()):
    from freesail.core import replay

    return names_of_bytes(replay.checkpoint_bytes(scenario_world(path, run_s, orders)))


def census(say=print) -> Iterator[tuple[str, set[tuple[str, str]]]]:
    """(where, names) for every checkpoint of the game's own the census takes."""
    for path in sorted(FIXTURES.glob("*.checkpoint")):
        yield f"the kept save {path.name}", names_of_file(path)
    for path in scenario_files():
        say(f"  {path.name}")
        yield f"the scenario {path.name}", census_of_scenario(path)
    for what, name, run_s, orders in WORLDS:
        say(f"  {what}")
        yield what, census_of_scenario(SCENARIOS / name, run_s, orders)


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
    args = ap.parse_args(argv)
    from freesail.core.checkpoint_names import ADMITTED
    from freesail.core.replay import BOUND_METHODS

    found: set[tuple[str, str]] = set()
    for where, names in census():
        lacking = names - ADMITTED - {("builtins", "getattr")}
        if lacking:
            print(f"{where}: not in the list: {sorted(lacking)}")
        found |= names
    found.discard(("builtins", "getattr"))  # admitted by BOUND_METHODS alone, never by name
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
