"""A file of the game's found by its name, and only by its name (package 115, part A, the
reader's finding 1).

The cause it mends: a lookup said to take a name joined the words it was given to a folder
(`folder / f"{words}.yaml"`), so that `..` climbed out of the folder and an absolute path
replaced it, and the lookup read whatever file the words named. One rule, in one place:

- a **name** is a name: not empty, no separator of either system (`/`, `\\`), no drive, not
  absolute, not `.` or `..`, no character a file's name cannot hold on Windows;
- whatever a name resolves to is checked, by its resolved path, to lie inside the folder it
  was looked up in.

`named_file` is the one road from words to a file by name; the server's folders
(`freesail.ui.places`) and the director's starter briefs (`agents.director._starter`) go by
it.
"""

from __future__ import annotations

from pathlib import Path, PurePosixPath, PureWindowsPath

# Characters no file's name holds on Windows (and the separators of both systems).
_NOT_IN_A_NAME = set('/\\:*?"<>|\0')


def is_name(text: str) -> bool:
    """Whether the words are a file's name and nothing more."""
    t = str(text)
    if not t.strip() or t.strip() in (".", ".."):
        return False
    if any(c in _NOT_IN_A_NAME or ord(c) < 32 for c in t):
        return False
    if PureWindowsPath(t).drive or PureWindowsPath(t).is_absolute():
        return False
    return not PurePosixPath(t).is_absolute()


def inside(p: Path, folder: Path) -> bool:
    f = folder.resolve()
    return p == f or f in p.parents


def named_file(folder: Path, name: str, suffix: str = "") -> Path | None:
    """The file `name` (with `suffix` when it lacks it) in `folder`, resolved, when the words
    are a name, the file is there and it lies in the folder; else None."""
    if not is_name(name):
        return None
    leaf = name if not suffix or name.lower().endswith(suffix) else name + suffix
    p = (folder / leaf).resolve()
    if not inside(p, folder) or not p.is_file():
        return None
    return p
