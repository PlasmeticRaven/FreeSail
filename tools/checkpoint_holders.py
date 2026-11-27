"""The names a checkpoint holds, read from its bytes without loading it, and where each is held.

    python -I tools/checkpoint_holders.py <save>.checkpoint            # the names not admitted
    python -I tools/checkpoint_holders.py <save>.checkpoint --all      # every name, counted
    python -I tools/checkpoint_holders.py <save>.checkpoint --name pathlib

A checkpoint (`freesail/core/replay.py`) is a line of JSON, its header, and a pickle. The
loader admits an exact list of the names a pickle calls (`freesail/core/checkpoint_names.py`,
`ADMITTED`), and refuses a checkpoint that names another ("the checkpoint names ..., which a
checkpoint may not hold"). This tool says which names those are, and where in the world each
is held, without loading the pickle: it walks the pickle's opcodes (`pickletools.genops`),
following the memo as the loader would, and calls nothing in it. So it may be run on a save
from anywhere: no class of the file is looked up, nothing of it is built, nothing it names is
imported.

Where a name is held is told by the strings pushed nearest before it, which in a pickle of
the game's world are the names of the attributes and keys that hold it (`saves_dir`,
`'path'`), and the classes last named before it, which are the objects being built about
it; and what it is, by the strings that follow it, which for a path are its parts.

The census of the game's own checkpoints (`tools/checkpoint_names.py`) loads them, being
the game's own; this reads any.
"""

from __future__ import annotations

import argparse
import gzip
import pickletools
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BEFORE = 4  # the strings and the classes told before a name: its holder (JUDGEMENT: enough)
AFTER = 4  # the strings told after it: its words


@dataclass
class Held:
    """A name the pickle calls, at its opcode's place, with what was pushed about it."""

    module: str
    name: str
    at: int
    keys: list[str] = field(default_factory=list)
    within: list[str] = field(default_factory=list)
    words: list[str] = field(default_factory=list)

    @property
    def dotted(self) -> str:
        return f"{self.module}.{self.name}"

    def line(self) -> str:
        return (
            f"{self.dotted} at byte {self.at}: held by {' / '.join(self.keys) or '?'}"
            f"; within {' < '.join(reversed(self.within)) or 'the world'}"
            f"; its words {self.words}"
        )


_STRINGS = {
    "SHORT_BINUNICODE",
    "BINUNICODE",
    "BINUNICODE8",
    "UNICODE",
    "SHORT_BINSTRING",
    "BINSTRING",
    "STRING",
}
_GETS = {"GET", "BINGET", "LONG_BINGET"}
_PUTS = {"PUT", "BINPUT", "LONG_BINPUT"}


def pickle_of(path: Path) -> bytes:
    """A checkpoint's pickle, its header line passed over."""
    with gzip.open(path, "rb") as f:
        f.readline()
        return f.read()


def holders(body: bytes) -> list[Held]:
    """Every name the pickle calls, in order, with the strings and classes pushed about it.

    Walks the opcodes only. A pushed value is kept as a string, as a name the pickle calls,
    or as nothing (any other object); the memo keeps the same, so that a string or a name
    fetched again from it is read as itself."""
    memo: dict[int, object] = {}
    pushed: list[object] = []  # the values pushed, newest last (strings, Held, or None)
    found: list[Held] = []
    open_words: list[Held] = []  # names still taking the strings that follow them
    for op, arg, pos in pickletools.genops(body):
        name = op.name
        value: object = None
        if name in ("FRAME", "PROTO", "STOP", "MARK", "POP", "POP_MARK"):
            continue
        if name == "MEMOIZE":
            memo[len(memo)] = pushed[-1] if pushed else None
            continue
        if name in _PUTS:
            memo[int(arg)] = pushed[-1] if pushed else None
            continue
        if name in _GETS:
            value = memo.get(int(arg))
        elif name in _STRINGS:
            value = arg if isinstance(arg, str) else str(arg)
        elif name in ("GLOBAL", "INST"):
            module, _, called = str(arg).partition(" ")
            value = _held(module, called, pos, pushed, found)
        elif name == "STACK_GLOBAL":
            called, module = (
                (pushed[-1] if pushed else None),
                (pushed[-2] if len(pushed) > 1 else None),
            )
            del pushed[-2:]  # the module and the name are taken by it
            value = _held(str(module), str(called), pos, pushed, found)
        if isinstance(value, str):
            for held in open_words:
                held.words.append(value)
            open_words = [h for h in open_words if len(h.words) < AFTER]
        if isinstance(value, Held) and name not in _GETS:
            open_words.append(value)
        pushed.append(value)
        if len(pushed) > 64:
            del pushed[:-64]
    return found


def _held(module: str, called: str, at: int, before: list[object], found: list[Held]) -> Held:
    keys = [v for v in before if isinstance(v, str)][-BEFORE:]
    within = [v.dotted for v in found[-BEFORE:]]
    held = Held(module, called, at, keys=keys, within=within)
    found.append(held)
    return held


def admitted() -> set[tuple[str, str]]:
    """The loader's list, read from its own file (a module of names, imported alone)."""
    sys.path.insert(0, str(ROOT))
    from freesail.core.checkpoint_names import ADMITTED

    return set(ADMITTED) | {("builtins", "getattr")}


def not_admitted(body: bytes) -> list[Held]:
    allowed = admitted()
    return [h for h in holders(body) if (h.module, h.name) not in allowed]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("checkpoint", type=Path)
    ap.add_argument("--all", action="store_true", help="every name the pickle calls, counted")
    ap.add_argument("--name", help="every place a name beginning so is held, admitted or not")
    a = ap.parse_args(argv)
    body = pickle_of(a.checkpoint)
    if a.all:
        for (module, called), n in sorted(
            Counter((h.module, h.name) for h in holders(body)).items()
        ):
            print(f"{n:6d}  {module}.{called}")
        return 0
    if a.name:
        held = [h for h in holders(body) if h.dotted.startswith(a.name)]
    else:
        held = not_admitted(body)
    for h in held:
        print(h.line())
    print(f"{len(held)} held" if held else "none held")
    return 1 if held and not a.name else 0


if __name__ == "__main__":
    raise SystemExit(main())
