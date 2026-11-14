"""The folders the server reads and writes files in (package 115, part A, item 2; the cold
review of milestone 7, 5.7 and 6.1).

The cause it mends: a path that came in a request was opened as it was given. The order
line's `save PATH` wrote a save and its checkpoint at any path, and `read the standing
orders from FILE` read any file and gave each line back in a refusal; the harbour's start
and its scenario maker opened the scenario, ship, book, brief and save they were named, from
anywhere. Over the server a file is now named, not pathed, and lies in the folders the
server was started with, and a path that leaves them is refused in words before anything is
opened, so its text is never given back. The console keeps its paths, and so does the
command line (`--load`, `--scenario`, `--standing-orders`): the person typing there owns
the machine.

The folders (`Places`):

- **the saves place**: the `--saves` the server was started with. `py -m freesail` gives it
  the settings' saves place when no `--saves` is given (`saves` beside the settings file,
  unless the settings name another); `python -m freesail.ui.server` without `--saves` uses
  `saves/` in the game's folder. Where `save NAME` writes `NAME.json` and its checkpoint,
  and where a save is taken up from. It is fixed for the run: a change of the setting while
  the game runs takes effect when the game is started again;
- **the game's data** (`data/` in the game's folder): the game's ships, scenarios, books and
  the director's briefs, read by name or by the path the primer gives
  (`data/standing_orders/starter.orders`);
- **the player's scenarios place** (the settings' `places: scenarios`): his own scenarios
  and books, read;
- **the game's folder** itself and its `saves/`, for a save alone (a `.json` file lying
  directly in either): the browser's saves once landed in the game's folder (a `save
  foo.json` at the order line of `py -m freesail` wrote it there), and they stay loadable.

Every file a save writes (the save and the checkpoint beside it) and every file a load
reads is checked by its final path, resolved, so that a link in a folder that leads out of
it is neither written through nor read; words that no path can be made of (a NUL, a name
too long for the system) are refused in words like any other.

A path given relative is read from the folder its kind lives in (a save from the saves
place, then the game's folder; anything else from the game's folder), so the primer's own
line works as it always did. Paths are compared as paths, resolved, on whatever system the
game runs on: a Windows drive (`C:\\...`) or a share (`\\\\host\\share`) is refused on
Windows as anywhere else unless it lies in the folders, and `..` cannot climb out.
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from pathlib import Path, PureWindowsPath

from freesail.core.names import is_name, named_file

ROOT = Path(__file__).resolve().parents[2]
GAME_DATA = ROOT / "data"
DEFAULT_SAVES = ROOT / "saves"
SAVE_SUFFIX = ".json"
BOOK_SUFFIX = ".orders"
BOOK_FOLDERS = (GAME_DATA / "standing_orders", GAME_DATA / "scenarios")


class PlaceRefused(ValueError):
    """A file the server will not open, in words for the player."""


def shown(p: Path) -> str:
    """A path as the player is told it: under the game's folder as the primer names one
    (`saves/foo.json`), else whole."""
    try:
        return p.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(p)


def resolve(given: str, base: Path) -> Path | None:
    """The path the words name, from `base` when relative, resolved; None for a path of
    another system's (a Windows drive or share named on a system that has neither), which
    lies in no folder of this one. A backslash is a separator on every system (a player on
    Windows types one; elsewhere it would be part of a file's name, which no folder of the
    game holds)."""
    text = given.strip().strip("\"'")
    if os.name != "nt" and PureWindowsPath(text).drive:
        return None
    if "\0" in text:
        return None
    if os.sep != "\\":
        text = text.replace("\\", "/")
    p = Path(text)
    if not p.is_absolute():
        p = base / p
    try:
        return p.resolve()
    except (OSError, ValueError, RuntimeError):  # too long, a loop of links: no path here
        return None


def _there(p: Path, file: bool = False) -> bool:
    """Whether the path is there (a file, with `file`); a path this system cannot ask
    about (a name too long for it) is not there."""
    try:
        return p.is_file() if file else p.exists()
    except (OSError, ValueError):
        return False


def final(p: Path | None, suffix: str) -> Path | None:
    """`p` with `suffix` when it lacks it, resolved again: the path that is opened, which a
    link named without its suffix may lead out of the folder from."""
    if p is None:
        return None
    if p.suffix.lower() != suffix:
        p = p.with_name(p.name + suffix)
    try:
        return p.resolve()
    except (OSError, ValueError, RuntimeError):
        return None


def inside(p: Path | None, folders: Iterable[Path]) -> bool:
    if p is None:
        return False
    for f in folders:
        f = f.resolve()
        if p == f or f in p.parents:
            return True
    return False


class Places:
    """The server's folders. `scenarios` is called each time (the harbour's settings can
    change it while the server runs)."""

    def __init__(
        self,
        saves: Path | str | None = None,
        scenarios: Callable[[], Path | None] | None = None,
    ):
        self.saves = Path(saves).resolve() if saves else DEFAULT_SAVES.resolve()
        self._scenarios = scenarios or (lambda: None)

    @property
    def scenarios(self) -> Path | None:
        try:
            p = self._scenarios()
        except Exception:  # noqa: BLE001  (unreadable settings: no place of the player's)
            return None
        return Path(p).resolve() if p else None

    def reading_folders(self) -> list[Path]:
        out = [GAME_DATA.resolve(), self.saves]
        if self.scenarios is not None:
            out.append(self.scenarios)
        return out

    def _where_words(self) -> str:
        own = f", your scenarios place ({self.scenarios})" if self.scenarios else ""
        return f"the game's data folder (data/){own} and the saves place ({shown(self.saves)})"

    # -- a save --------------------------------------------------------------------

    def save_target(self, given: str) -> Path:
        """Where `save NAME` writes: `NAME.json` in the saves place; a path only if it lies
        there. The save and the checkpoint beside it are each checked by their final path."""
        from freesail.core.replay import CHECKPOINT_SUFFIX, checkpoint_path

        text = given.strip().strip("\"'")
        if not text:
            raise PlaceRefused(
                f"Say 'save NAME', and the game is saved as NAME.json in the saves place "
                f"({shown(self.saves)})."
            )
        p = final(resolve(text, self.saves), SAVE_SUFFIX)
        beside = final(checkpoint_path(p), CHECKPOINT_SUFFIX) if p else None
        if (
            p is None
            or beside is None
            or not inside(p, [self.saves])
            or not inside(beside, [self.saves])
        ):
            raise PlaceRefused(
                f"The game is saved in the saves place ({shown(self.saves)}), not elsewhere: "
                f"say 'save NAME' and it is written there as NAME.json. To keep a copy "
                f"elsewhere, copy the file from the saves place."
            )
        return p

    def load_folders(self) -> list[Path]:
        return [self.saves, ROOT.resolve(), DEFAULT_SAVES.resolve()]

    def save_to_load(self, given: str) -> Path:
        """A save the harbour takes up: a `.json` save by its name in the saves place, or by
        a path to one in the saves place, or lying directly in the game's folder or its
        `saves/` (the game's own older saves). The save's file and the checkpoint beside it
        are each checked by their final path, before anything is opened."""
        from freesail.core.replay import CHECKPOINT_SUFFIX, checkpoint_path

        text = given.strip().strip("\"'")
        found = None
        for base in (self.saves, ROOT.resolve()):
            p = resolve(text, base)
            p = final(p, SAVE_SUFFIX) if is_name(text) else p
            if p is not None and self._loadable(p) and _there(p, file=True):
                found = p
                break
        if found is not None:
            beside = final(checkpoint_path(found), CHECKPOINT_SUFFIX)
            if beside is not None and (not _there(beside) or self._loadable_beside(beside)):
                return found
        p = resolve(text, self.saves)
        plain = Path(text).suffix.lower() in ("", SAVE_SUFFIX)
        if plain and p is not None and self._loadable(final(p, SAVE_SUFFIX) or p):
            raise PlaceRefused(f"There is no save {text} in the saves place ({shown(self.saves)}).")
        raise PlaceRefused(
            f"The harbour takes up a save (a .json file) from the saves place "
            f"({shown(self.saves)}) or the game's folder, and {text} is none. It still loads: "
            f"move it into the saves place, or start the game with "
            f"'py -m freesail --load PATH' at the command line."
        )

    def _loadable(self, p: Path | None) -> bool:
        """A save's file where a load may read one: a `.json` in the saves place, or lying
        directly in the game's folder or its `saves/`."""
        if p is None or p.suffix.lower() != SAVE_SUFFIX:
            return False
        if inside(p, [self.saves]):
            return True
        return p.parent in (ROOT.resolve(), DEFAULT_SAVES.resolve())

    def _loadable_beside(self, p: Path) -> bool:
        if inside(p, [self.saves]):
            return True
        return p.parent in (ROOT.resolve(), DEFAULT_SAVES.resolve())

    # -- a file to read ------------------------------------------------------------

    def readable(self, given: str, what: str = "file") -> Path:
        """A file of the game's or the player's to read (a ship, a scenario, a brief): a
        path in the reading folders, read from the game's folder when relative."""
        text = given.strip().strip("\"'")
        p = resolve(text, ROOT)
        if p is not None and inside(p, self.reading_folders()):
            return p
        raise PlaceRefused(
            f"The game reads a {what} from {self._where_words()}; {text} is in none of them, "
            "and it was not opened."
        )

    def book(self, given: str) -> Path:
        """A book of standing orders: by its name in the game's books, its scenarios' books
        or the player's place (`starter`, `starter.orders`), else by a path in the reading
        folders (the primer's `data/standing_orders/starter.orders`)."""
        text = given.strip().strip("\"'")
        if is_name(text):
            folders = list(BOOK_FOLDERS) + ([self.scenarios] if self.scenarios else [])
            for f in folders:
                found = named_file(f, text, BOOK_SUFFIX)
                if found is not None:
                    return found
        return self.readable(text, "book of standing orders")

    def brief(self, words: str) -> str:
        """A director's brief as the player gives it (a starter's name, a file or words):
        a file is one in the reading folders, given as its resolved path; any other words
        are passed as they are (the director reads them as the brief's own words)."""
        text = " ".join(str(words).split())
        if Path(text.strip("\"'")).suffix.lower() in (".yaml", ".yml"):
            # a file: in the reading folders, by its path (a starter named with its
            # suffix, `quiet-passage.yaml`, is read from the starters' folder by its name)
            from freesail.agents import director as director_mod

            if is_name(text) and director_mod._starter(text) is not None:
                return text
            return str(self.readable(text, "director's brief"))
        # a starter's name or the brief's own words: the director's reader takes a starter
        # by its name alone (`core.names`), and words are words, never a file; one word that
        # is no name (a path without its suffix) is neither, and is refused as a path is
        if text and " " not in text and not is_name(text):
            raise PlaceRefused(
                f"A director's brief is a starter's name, a file in {self._where_words()}, or "
                f"words; {text} is none of them, and nothing was opened."
            )
        return text
