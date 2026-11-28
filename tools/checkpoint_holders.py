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
`'path'`), and by the objects it is part of, outermost first: those on the loader's stack
when it is named whose state is given them after it (their BUILD comes later), so that an
object already made, waiting beside it to be put in a dict, is not counted (the stack is
followed by each opcode's own account of what it takes and gives, `pickletools`). What it
is, by the strings it is called with: for a path, its words (a later Python pickles a path
as its words whole, 3.11 as its parts).

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

BEFORE = 4  # the strings told before a name: its holder (JUDGEMENT: enough)


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
_TUPLES = {"TUPLE1": 1, "TUPLE2": 2, "TUPLE3": 3}
# the functions that make an object of the class they are given (the game's own, `replay._new`,
# and the standard library's): the object is told by that class
_MAKERS = {
    "freesail.core.replay._new",
    "copyreg.__newobj__",
    "copyreg.__newobj_ex__",
    "copyreg._reconstructor",
}


@dataclass
class _Item:
    """A value on the loader's stack, as far as this reader keeps it: a string (`words`, one),
    a name the pickle calls (`held`), an object made by calling one (`made`), a tuple (the
    strings in it, `words`), a mark, or anything else."""

    kind: str  # "str", "name", "obj", "tuple", "mark", "other"
    words: list[str] = field(default_factory=list)
    held: Held | None = None
    made: str = ""
    built_at: int = -1  # the byte of the BUILD that gave the object its state
    names: list[Held] = field(default_factory=list)  # a tuple's: the names in it


_OTHER = _Item("other")


def pickle_of(path: Path) -> bytes:
    """A checkpoint's pickle, its header line passed over."""
    with gzip.open(path, "rb") as f:
        f.readline()
        return f.read()


def holders(body: bytes) -> list[Held]:
    """Every name the pickle calls, in order, with the strings pushed before it, the objects
    being built about it and the strings it is called with.

    Walks the opcodes only, keeping the loader's stack as `pickletools` gives each opcode's
    taking and giving; a value is kept as a string, a name, an object of a named class, a
    tuple of strings, or nothing, and the memo keeps the same, so that a value fetched again
    from it is read as itself. Nothing is looked up or called."""
    memo: dict[int, _Item] = {}
    stack: list[_Item] = []
    recent: list[str] = []  # the strings pushed, newest last
    around: list[tuple[Held, list[_Item]]] = []  # each name and the objects on the stack at it

    def pop(n: int) -> list[_Item]:
        took = stack[len(stack) - n :] if n else []
        del stack[len(stack) - n :]
        return [x for x in took]

    def to_mark() -> list[_Item]:
        for i in range(len(stack) - 1, -1, -1):
            if stack[i].kind == "mark":
                took = stack[i + 1 :]
                del stack[i:]
                return took
        took = stack[:]
        stack.clear()
        return took

    def made_by(called: _Item, args: _Item | None = None) -> _Item:
        held = called.held if called.kind == "name" else None
        if held is None:
            return _Item("obj")
        if args is not None and not held.words:
            held.words = list(args.words)
        made = held.dotted
        if made in _MAKERS and args is not None and args.names:
            made = args.names[0].dotted
        return _Item("obj", made=made)

    for op, arg, pos in pickletools.genops(body):
        name = op.name
        if name in ("FRAME", "PROTO", "STOP"):
            continue
        if name == "MARK":
            stack.append(_Item("mark"))
        elif name == "MEMOIZE":
            memo[len(memo)] = stack[-1] if stack else _OTHER
        elif name in _PUTS:
            memo[int(arg)] = stack[-1] if stack else _OTHER
        elif name in _GETS:
            got = memo.get(int(arg), _OTHER)
            if got.held is not None:
                # a name fetched again from the memo: another place it is held, told as its own
                again = _held(got.held.module, got.held.name, pos, recent, stack, around)
                got = _Item("name", held=again)
            stack.append(got)
        elif name in _STRINGS:
            stack.append(_Item("str", [arg if isinstance(arg, str) else str(arg)]))
        elif name == "GLOBAL":
            module, _, called = str(arg).partition(" ")
            stack.append(_Item("name", held=_held(module, called, pos, recent, stack, around)))
        elif name == "STACK_GLOBAL":
            module, called = pop(2)
            words = (" ".join(module.words), " ".join(called.words))
            if recent[-2:] == list(words):
                del recent[-2:]  # its own two words, not a holder's
            stack.append(_Item("name", held=_held(*words, pos, recent, stack, around)))
        elif name == "INST":
            module, _, called = str(arg).partition(" ")
            held = _held(module, called, pos, recent, stack, around)
            args = to_mark()
            held.words = [w for x in args if x.kind == "str" for w in x.words]
            stack.append(_Item("obj", made=held.dotted))
        elif name == "OBJ":
            took = to_mark()
            stack.append(made_by(took[0], _Item("tuple", [w for x in took[1:] for w in x.words])))
        elif name in ("REDUCE", "NEWOBJ"):
            called, args = pop(2)
            stack.append(made_by(called, args))
        elif name == "NEWOBJ_EX":
            called, args, _kw = pop(3)
            stack.append(made_by(called, args))
        elif name == "BUILD":
            pop(1)  # the state is taken into the object, which stays
            if stack:
                stack[-1].built_at = pos
        elif name == "EMPTY_TUPLE":
            stack.append(_Item("tuple"))
        elif name in _TUPLES or name == "TUPLE":
            took = pop(_TUPLES[name]) if name in _TUPLES else to_mark()
            words = [w for x in took if x.kind == "str" for w in x.words]
            names = [x.held for x in took if x.held is not None]
            stack.append(_Item("tuple", words, names=names))
        else:
            before = op.stack_before
            if pickletools.markobject in before:
                to_mark()
                pop(before.index(pickletools.markobject))
            else:
                pop(len(before))
            stack.extend(_OTHER for _ in op.stack_after)
        if (name in _STRINGS or name in _GETS) and stack[-1].kind == "str":
            recent.append(stack[-1].words[0])
            del recent[:-64]
    for held, about in around:
        held.within = [x.made for x in about if x.made and x.built_at > held.at]
    return [h for h, _ in around]


def _held(
    module: str,
    called: str,
    at: int,
    recent: list[str],
    stack: list[_Item],
    around: list[tuple[Held, list[_Item]]],
) -> Held:
    held = Held(module, called, at, keys=recent[-BEFORE:])
    around.append((held, [x for x in stack if x.kind == "obj"]))
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
