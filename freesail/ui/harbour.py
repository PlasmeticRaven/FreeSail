"""The harbour: a launcher in the browser, served by the game's own server (package 59; spec
M7b §21d and §21e; the owner, 2026-10-17: the terminals, the flags, the desktop client's
configuration and the scenarios by hand had become tedious).

`py -m freesail` (`freesail/__main__.py`) starts the server and opens the harbour at
`/harbour` (`client/harbour.html`, `harbour.js`). The page lists the scenarios (the game's
under `data/scenarios/` and the player's own under his scenarios place), the ships, the
seats and the doors; starts a game with the choices made, the server's flags as its
controls (`Harbour.start`, which builds the flags' namespace and calls the server's own
`prepare_game`, so that a game started here is the server's game as from the command line,
and takes it up in place with `Driver.replace_world`: one server process, the harbour
reachable while the game runs); shows which doors are up and which stations are held by
whom; writes the desktop client's MCP entries, one per station ticked
(`freesail-<station>`), the entry shown first and the player confirming; starts the API
door and the local runner as the server's subprocesses with their flags from the settings
(`Door`: the modules' own command lines, nothing re-implemented), their output in a pane,
each stoppable, a door that dies said so; holds the settings (`freesail.settings`); and
carries the scenario maker (spec M7b §21e): a scenario read into the form, proved by
loading it as the console would (`prove`), and written in the file's own form
(`scenarios.write_scenario`), unchanged where nothing was changed (truth 7b-109).

Routes (`harbour_routes`):

    GET  /harbour                          the page
    GET  /api/harbour/state                the game, the stations held, the doors, the
                                           saves in the saves place by name, the settings'
                                           place, the credential store's state
    GET  /api/harbour/catalogue            the scenarios (each with its shelf and its
                                           sentence, in the shelves' order), the shelves,
                                           the first game the page names,
                                           the ships, seats, stations, briefs, books, ports,
                                           regions and nations
    POST /api/harbour/start                {scenario | ship | load, seed, seat, aboard,
                                           time, pace, crewed_cap, crewed_range, business,
                                           director_brief, standing_orders, wind, heading}
                                           -> the game
    GET  /api/harbour/settings             the settings and where they are kept
    POST /api/harbour/settings             {settings} -> kept (no key, truth 7b-110)
    POST /api/harbour/desktop              {stations: [...], ship?, write?} -> the entries
                                           and the client's file as it would be; written
                                           only with write: true
    POST /api/harbour/shortcut             {write?} -> the shortcut's path and text
    POST /api/harbour/doors                {door: api|local, station, ship?, model?} ->
                                           started (model: one the settings can call, for
                                           the API door)
    GET  /api/harbour/doors/{id}           ?since=N: its output from line N
    POST /api/harbour/doors/{id}/say       {text}: a line to its terminal (the owner's
                                           word in a consent conversation)
    POST /api/harbour/doors/{id}/stop      stopped, its station released
    GET  /api/harbour/scenario             ?path=: a scenario's text and fields, its lines
                                           as a driver says them, the ships to be aboard
    POST /api/harbour/scenario/prove       {fields, source?} -> the scenario's lines, or
                                           its refusal in words
    POST /api/harbour/scenario             {fields, source?, name, book?, overwrite?} ->
                                           proved and written in the player's place
    GET  /api/harbour/chart                ?region=: the coast simplified and the ports,
                                           for pricking a start on the chart

Nothing here writes the World's log but what the server's own start writes; a model's name
from the settings goes to the doors' command lines and the desktop client's file, never to
the repository, a save or a log (truth 7b-110).
"""

from __future__ import annotations

import collections
import contextlib
import itertools
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse, Response

from freesail import settings as settings_mod
from freesail.settings import SettingsError
from freesail.ui.places import PlaceRefused, Places

ROOT = Path(__file__).resolve().parents[2]
CLIENT_DIR = ROOT / "client"
GAME_SCENARIOS = ROOT / "data" / "scenarios"
GAME_BOOKS = ROOT / "data" / "standing_orders"
SHIPS_DIR = ROOT / "data" / "ships"
# The page's shelves (package 96b, step 1; docs/design/Design-Harbour.md §3.2): which shelf
# each of the game's scenarios stands on, read by the page alone. With the page's own files
# and not under `data/`: that folder is the game's data, every dated key of which the
# range's audit classes (`tools/audit_range.py`) and every file of which is hashed into the
# rules' stamp a save carries (`core.world.fingerprint_of`), and a re-sorting of the page's
# list is no change of the rules.
SHELVES_FILE = CLIENT_DIR / "harbour-shelves.yaml"
# The two shelves the file never names: the player's own scenarios, first; and the game's
# scenarios no shelf names, last, so that none is hidden by being forgotten.
SHELF_OWN = {"id": "yours", "title": "Yours", "says": "Scenarios of your own.", "hidden": False}
SHELF_UNSORTED = {
    "id": "unsorted",
    "title": "Not yet sorted",
    "says": "Scenarios of the game that no shelf names yet.",
    "hidden": False,
}

# The player's seats at the start (the server's `--seat`): '' as the scenario says; the
# captain at the prompt; the stations below and above (`agents.seat.SEAT_STATIONS`).
SEATS = ("", "captain", "officer", "master", "lookout", "passenger", "director")
# The stations a door asks for (the doors' `--station`).
STATIONS = ("captain", "officer", "master", "lookout", "director", "watcher", "passenger")
DOOR_KINDS = ("api", "local")
DOOR_LINES_KEPT = 4000
STOP_WAIT_S = 6.0
# A seat's door whose station the game released is given this long to end of itself before
# it is stopped (package 67; judgement: the door's poll returns within its wait, half a
# second in the doors' loop, and its last words take a moment more).
SEAT_DOOR_GRACE_S = 20.0
COAST_STEP_DEG = 0.01  # the harbour's chart keeps a point about every half mile
SAVES_LISTED = 30  # the page lists this many saves, the newest first


class HarbourError(Exception):
    """A choice the harbour refuses, in words, with the status it answers with."""

    def __init__(self, words: str, status: int = 400):
        super().__init__(words)
        self.words = words
        self.status = status


def _rel(path: Path) -> str:
    """A path in the game's folder as the scenarios name one (`data/ships/smack.yaml`);
    another as it is."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


# The keys of a scenario file the loader reads (`world.scenarios.load_scenario`, by its
# own reading: every `raw.get` and `raw[...]` of it): a key outside these is passed over by
# the game in silence, and the maker's proof says so (package 96b, step 8).
LOADER_KEYS = frozenset(
    """name start latitude_deg position region chart follows_history ship director knowledge
    wind glass papers epitome instrument chronometer nation nations people cargo ports ships
    things crewed squadrons weather_bound business world_orders current weather seed
    standing_orders intent orders stations""".split()
)


def year_words(year: int) -> str:
    """What the page says of a scenario that begins in another year than 1805 (the
    design's trap 3; the owner's answer to its question 5: said on the page)."""
    return (
        f"she begins in {year}. The ports are as they stood on that day; the wars are those "
        "of June 1805, whatever the year."
    )


# The most a box of the file's own words takes (the longest block of the game's scenarios,
# a day of systems, is under four thousand characters).
BLOCK_MAX_CHARS = 20_000


def _has_anchor_or_alias(text: str) -> bool:
    """Whether YAML text carries an anchor (`&name`) or an alias (`*name`), by its tokens
    alone: nothing is loaded, so a text of nested aliases costs its own length to refuse.
    Text that cannot be scanned raises the scanner's error, which the caller says."""
    return any(
        isinstance(token, yaml.tokens.AnchorToken | yaml.tokens.AliasToken)
        for token in yaml.scan(text)
    )


def _plain(value: Any) -> Any:
    """A value read from YAML as the scenario's fields carry one: a day or a time as its
    words (the fields are JSON, and the loader reads the words)."""
    import datetime as dt

    if isinstance(value, dict):
        return {str(k): _plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_plain(v) for v in value]
    if isinstance(value, dt.datetime):
        return value.isoformat(timespec="minutes")
    if isinstance(value, dt.date):
        return value.isoformat()
    return value


_boats: dict[str, tuple[float, bool]] = {}


def _is_boat(path: Path) -> bool:
    """Whether a ship's file is a ship's boat (its `ship: rig: boat`): the boats are carried
    by the ships and are no ship to start a game in, so the page's list leaves them out
    (package 96b, step 1). A file that cannot be read is listed, as before."""
    key = str(path)
    try:
        mtime = path.stat().st_mtime
    except OSError:
        return False
    cached = _boats.get(key)
    if cached is None or cached[0] != mtime:
        boat = False
        with contextlib.suppress(OSError):
            # her file's head alone (the ships' files are long, and the catalogue is asked
            # for at every opening of the page): the line `  rig: boat` under `ship:`
            with path.open(encoding="utf-8") as f:
                head = f.read(8000)
            boat = re.search(r"^  rig:[ \t]*boat[ \t]*$", head, re.M) is not None
        _boats[key] = (mtime, boat)
        cached = _boats[key]
    return cached[1]


# ---------------------------------------------------------------------------
# A door as the server's subprocess
# ---------------------------------------------------------------------------


def _exit_words() -> dict[int, str]:
    """The doors' exit codes in words (`agents.local`'s, which the API door shares)."""
    from freesail.agents import local

    return {
        0: "it ended of itself",
        1: "it failed (its last lines say why)",
        local.EXIT_UNREACHABLE: "it could not reach the game or its model, or would not "
        "start (its last lines say why)",
        local.EXIT_RELEASED: "its station was released",
        local.EXIT_NO_CONSENT: "no consent: the model did not consent, or the owner stopped "
        "the step",
    }


class Door:
    """The API door or the local runner, started with its own command line as a subprocess
    of the server (package 59, item 3): its output kept for the harbour's pane, a line
    given to its terminal when the owner has the word, stopped at the owner's word."""

    def __init__(
        self,
        ident: str,
        kind: str,
        station: str,
        argv: list[str],
        ship: str = "",
        env: dict[str, str] | None = None,
        cwd: Path = ROOT,
        by: str = "",
        seat: str = "",
    ):
        self.id = ident
        self.kind = kind
        self.station = station
        self.ship = ship
        # whose door: "" the owner's, started from the page; "the director" for a seat's
        # (package 67), with the seat's key on the World
        self.by = by
        self.seat = seat
        self.argv = list(argv)
        self.lines: collections.deque[str] = collections.deque(maxlen=DOOR_LINES_KEPT)
        self.count = 0  # lines ever written, so that a pane asks from where it left off
        self.code: int | None = None
        self.stopped = False
        self.started = time.time()
        self._lock = threading.Lock()
        kw: dict[str, Any] = {}
        if sys.platform.startswith("win"):
            kw["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        self.proc = subprocess.Popen(
            self.argv,
            cwd=str(cwd),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
            env=env,
            **kw,
        )
        self._reader = threading.Thread(target=self._read, daemon=True)
        self._reader.start()

    def _add(self, line: str) -> None:
        with self._lock:
            self.lines.append(line)
            self.count += 1

    def _read(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            self._add(line.rstrip("\n"))
        code = self.proc.wait()
        self.code = code
        why = _exit_words().get(code, "it died")
        self._add(
            f"== The {self.words()} has ended (exit code {code}): "
            f"{'stopped from the harbour' if self.stopped else why}. =="
        )

    @property
    def running(self) -> bool:
        return self.proc.poll() is None

    def words(self) -> str:
        door = "API door" if self.kind == "api" else "local runner"
        aboard = f" of {self.ship}" if self.ship else ""
        whose = "director's seat's " if self.by else ""
        return f"{whose}{door} at the {self.station}{aboard}"

    def output(self, since: int = 0) -> tuple[list[str], int]:
        """The lines from the `since`-th on (those still kept), and the count now."""
        with self._lock:
            first = self.count - len(self.lines)
            start = max(0, since - first)
            return list(self.lines)[start:], self.count

    def say(self, text: str) -> None:
        if not self.running or self.proc.stdin is None:
            raise HarbourError(f"The {self.words()} is not running.", 409)
        self._add(f"owner> {text}")
        try:
            self.proc.stdin.write(text + "\n")
            self.proc.stdin.flush()
        except OSError as e:
            raise HarbourError(f"The {self.words()} took no line ({e}).", 409) from None

    def stop(self) -> None:
        """The door's own Ctrl-C where the platform has one (it releases its station and
        says so), else ended; either way within `STOP_WAIT_S`."""
        if not self.running:
            return
        self.stopped = True
        with contextlib.suppress(OSError, ValueError):
            if sys.platform.startswith("win"):
                self.proc.terminate()
            else:
                self.proc.send_signal(signal.SIGINT)
        try:
            self.proc.wait(timeout=STOP_WAIT_S)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait(timeout=STOP_WAIT_S)
        self._reader.join(timeout=STOP_WAIT_S)

    def state(self) -> dict[str, Any]:
        state = "running" if self.running else ("stopped" if self.stopped else "ended")
        out = {
            "id": self.id,
            "door": self.kind,
            "station": self.station,
            "ship": self.ship,
            "state": state,
            "code": self.code,
            "words": f"The {self.words()}: {state}"
            + ("" if self.code is None else f" (exit code {self.code})")
            + ".",
            "lines": self.count,
            "by": self.by,
        }
        return out


# ---------------------------------------------------------------------------
# The harbour
# ---------------------------------------------------------------------------


class Harbour:
    """The launcher around one server's driver (`ui.server.Driver`). `started` is whether a
    game is in play (False for `py -m freesail` with no game asked for, when `/` leads to
    the harbour); `game_url` the address the doors reach the game at."""

    def __init__(
        self,
        driver: Any,
        *,
        settings_path: Path | str | None = None,
        consent_records: Path | str | None = None,
        saves_dir: Path | str | None = None,
        started: bool = False,
        game_url: str = "http://localhost:8000",
    ):
        self.driver = driver
        self.settings_path = Path(settings_path) if settings_path else None
        self.consent_records = consent_records
        self.saves_dir = saves_dir
        self.started = started
        self.game_url = game_url
        self.client_dir = CLIENT_DIR
        # the page as served: the server's guard puts the game's mark in it (package 115)
        self.page: Any = lambda path, host="": FileResponse(path, media_type="text/html")
        # the server's folders (package 115, part A): the app gives the driver's
        self.places = Places(saves_dir, self.scenarios_place)
        self.doors: dict[str, Door] = {}
        self._ids = itertools.count(1)
        self.game: dict[str, Any] = {}  # what the harbour started, in words
        # the games begun and ended from this harbour, counted: a page tells one game from
        # the next by it (the stations' table keeps a row's choice of door within a game)
        self.games = 0
        self._ports: list[dict[str, Any]] | None = None
        self._charts: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()
        # the director's seats' doors (package 67): the seat's key to its door's id (None
        # where no door could be started: the settings call no such model), for the World
        # they were started in
        self.seat_doors: dict[str, str | None] = {}
        self._seat_world: Any = None
        from freesail.agents import director as director_mod

        director_mod.set_seat_doors(driver.world, self)
        on_replace = getattr(driver, "on_replace", None)
        if callable(on_replace):
            on_replace(self._taken_up)
        on_tend = getattr(driver, "on_tend", None)
        if callable(on_tend):
            on_tend(self.tend_seats)
        # the ships' fits are read from their files, two seconds of reading for the
        # seventeen: begun here, so that the page's first catalogue seldom waits for it
        threading.Thread(target=self.fits, daemon=True).start()

    def _taken_up(self, old: Any, new: Any) -> None:
        """A new game in place: the seats' doors are the new World's to ask for."""
        from freesail.agents import director as director_mod

        director_mod.set_seat_doors(old, None)
        director_mod.set_seat_doors(new, self)

    # -- settings ------------------------------------------------------------------

    @property
    def path(self) -> Path:
        return self.settings_path or settings_mod.settings_path()

    def settings(self) -> dict[str, Any]:
        return settings_mod.load_settings(self.path)

    def settings_or_defaults(self) -> tuple[dict[str, Any], str]:
        try:
            return self.settings(), ""
        except SettingsError as e:
            import copy

            return copy.deepcopy(settings_mod.DEFAULTS), str(e)

    def scenarios_place(self) -> Path:
        s, _ = self.settings_or_defaults()
        return settings_mod.place(s, "scenarios", self.path)

    def callable_models(self) -> dict[str, str]:
        """The models the settings can call through the API door, by name to the dialect
        (package 67: the director's seats are for these); none where the settings cannot
        be read."""
        try:
            return settings_mod.callable_models(self.settings())
        except SettingsError:
            return {}

    def api_model(self) -> str:
        s, _ = self.settings_or_defaults()
        return str(((s.get("doors") or {}).get("api") or {}).get("model") or "")

    # -- what there is -------------------------------------------------------------

    def catalogue(self) -> dict[str, Any]:
        from freesail.agents import director as director_mod
        from freesail.world.nations import load_nations
        from freesail.world.scenarios import STATION_HOLDERS
        from freesail.world.ships import DESCRIPTIONS

        scenarios = [
            self._scenario_entry(p, own=False) for p in sorted(GAME_SCENARIOS.glob("*.yaml"))
        ]
        own = self.scenarios_place()
        if own.is_dir():
            scenarios += [self._scenario_entry(p, own=True) for p in sorted(own.glob("*.yaml"))]
        shelves = self._shelve(scenarios)
        books = [_rel(p) for p in sorted(GAME_BOOKS.glob("*.orders"))]
        if own.is_dir():
            books += [str(p) for p in sorted(own.glob("*.orders"))]
        briefs = {}
        for name in director_mod.starter_briefs():
            with contextlib.suppress(OSError, yaml.YAMLError):
                briefs[name] = yaml.safe_load(
                    (director_mod.BRIEFS_DIR / f"{name}.yaml").read_text(encoding="utf-8")
                )
        return {
            "scenarios": scenarios,
            "shelves": shelves,
            "first_game": self.first_game(scenarios),
            "ships": [_rel(p) for p in sorted(SHIPS_DIR.glob("*.yaml")) if not _is_boat(p)],
            "seats": list(SEATS),
            "stations": list(STATIONS),
            "holders": list(STATION_HOLDERS),
            "doors": list(DOOR_KINDS),
            "paces": list(settings_mod.PACES),
            "briefs": briefs,
            "books": books,
            "descriptions": list(DESCRIPTIONS),
            "kinds": self.kinds(),
            "squadrons": self.squadron_words(),
            "posts": self.posts(),
            # the signal books a ship may hold beside her own: a nation's root. `basic`, the
            # foundation every nation's books stand on, is left out: it is not shown to be a
            # book a ship holds apart (the lead's ruling: not guessed)
            "signal_books": sorted(
                p.name
                for p in (ROOT / "data" / "signals").iterdir()
                if p.is_dir() and p.name != "basic"
            ),
            "fits": self.fits(),
            "nations": list(load_nations().nations),
            "regions": self.regions(),
            "ports": self.ports(),
            "scenarios_place": str(own),
        }

    _names: dict[str, tuple[float, str, int | None]] = {}

    def _scenario_entry(self, path: Path, own: bool) -> dict[str, Any]:
        """A scenario for the lists: its path as a driver takes it and its name (read once
        a change of the file)."""
        key = str(path)
        try:
            mtime = path.stat().st_mtime
        except OSError:
            mtime = 0.0
        cached = Harbour._names.get(key)
        if cached is None or cached[0] != mtime:
            name = path.stem
            year: int | None = None
            with contextlib.suppress(OSError, yaml.YAMLError, AttributeError):
                doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                name = str(doc.get("name") or path.stem)
                with contextlib.suppress(ValueError, TypeError):
                    year = int(str(doc.get("start"))[:4]) if doc.get("start") else None
                if doc.get("follows_history") is True:
                    # decision 69: said on the harbour's page in the world's words
                    name += ", keeping to the course of history"
            Harbour._names[key] = (mtime, name, year)
            cached = Harbour._names[key]
        return {
            "path": _rel(path) if not own else str(path),
            "name": cached[1],
            "own": own,
            # the year she begins in (package 96b, step 8), where the file says a day
            "year": cached[2],
        }

    def shelves(self) -> list[dict[str, Any]]:
        """The shelves as the file has them (`client/harbour-shelves.yaml`): each its id, its
        title, its line, whether it is shown only when asked for, and its scenarios in
        order, each `{file, says}`. A file that is missing or cannot be read gives no
        shelves, and every scenario then stands unsorted: the list is never lost to it."""
        try:
            mtime = SHELVES_FILE.stat().st_mtime
        except OSError:
            return []
        cached = Harbour._shelves
        if cached is None or cached[0] != mtime:
            out: list[dict[str, Any]] = []
            with contextlib.suppress(OSError, yaml.YAMLError, AttributeError, TypeError):
                doc = yaml.safe_load(SHELVES_FILE.read_text(encoding="utf-8")) or {}
                for shelf in doc.get("shelves") or []:
                    if not isinstance(shelf, dict) or not str(shelf.get("id") or "").strip():
                        continue
                    out.append(
                        {
                            "id": str(shelf["id"]).strip(),
                            "title": str(shelf.get("title") or shelf["id"]).strip(),
                            "says": " ".join(str(shelf.get("says") or "").split()),
                            "hidden": shelf.get("hidden") is True,
                            "scenarios": [
                                {
                                    "file": str(s.get("file") or "").strip(),
                                    "says": " ".join(str(s.get("says") or "").split()),
                                    "seat": " ".join(str(s.get("seat") or "").lower().split()),
                                }
                                for s in shelf.get("scenarios") or []
                                if isinstance(s, dict)
                            ],
                        }
                    )
                first = doc.get("first_game")
                if isinstance(first, dict) and str(first.get("file") or "").strip():
                    says = first.get("says") or []
                    says = [says] if isinstance(says, str) else list(says)
                    Harbour._first = {
                        "file": str(first["file"]).strip(),
                        "says": [" ".join(str(x).split()) for x in says if str(x).strip()],
                    }
                else:
                    Harbour._first = None
            Harbour._shelves = (mtime, out)
            cached = Harbour._shelves
        return cached[1]

    _shelves: tuple[float, list[dict[str, Any]]] | None = None
    _first: dict[str, Any] | None = None

    def first_game(self, scenarios: list[dict[str, Any]]) -> dict[str, Any] | None:
        """The game the first panel names (package 96b, step 2): the shelves' file's
        `first_game`, as `{path, name, says: [lines]}`; None where the file names none or
        names a scenario that is not there (the panel then offers the lessons alone)."""
        self.shelves()
        first = Harbour._first
        if first is None:
            return None
        for entry in scenarios:
            if not entry["own"] and Path(entry["path"]).stem == first["file"]:
                return {"path": entry["path"], "name": entry["name"], "says": first["says"]}
        return None

    def saves(self) -> dict[str, Any]:
        """The saves in the saves place, newest first (package 96b, step 2: the first
        panel's "take up a saved game"): each by its name as `save NAME` wrote it and the
        time its file was written. Their names alone: no save is opened."""
        place = self.places.saves
        found: list[tuple[float, str]] = []
        with contextlib.suppress(OSError):
            for p in place.glob("*.json"):
                with contextlib.suppress(OSError):
                    if p.is_file():
                        found.append((p.stat().st_mtime, p.stem))
        found.sort(reverse=True)
        return {
            "place": str(place),
            "saves": [
                {"name": name, "written": time.strftime("%Y-%m-%d %H:%M", time.localtime(at))}
                for at, name in found[:SAVES_LISTED]
            ],
        }

    def _shelve(self, scenarios: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Each scenario of the list given its shelf, its place on it and its sentence
        (`shelf`, `order`, `says`), and the list put in the shelves' order: the player's
        own first, then the file's shelves, then the game's scenarios no shelf names.
        Returns the shelves that hold a scenario, in that order, each `{id, title, says,
        hidden}`."""
        named: dict[str, tuple[int, int, str, str, str]] = {}
        file_shelves = self.shelves()
        for i, shelf in enumerate(file_shelves, start=1):
            for j, s in enumerate(shelf["scenarios"]):
                named.setdefault(s["file"], (i, j, shelf["id"], s["says"], s["seat"]))
        last = len(file_shelves) + 1
        for n, entry in enumerate(scenarios):
            entry["seat"] = ""
            if entry["own"]:
                at, entry["shelf"], entry["says"] = (0, n), SHELF_OWN["id"], ""
            else:
                stem = Path(entry["path"]).stem
                i, j, shelf_id, says, seat = named.get(
                    stem, (last, n, SHELF_UNSORTED["id"], "", "")
                )
                at, entry["shelf"], entry["says"], entry["seat"] = (i, j), shelf_id, says, seat
            entry["order"] = at
        scenarios.sort(key=lambda e: e["order"])
        for n, entry in enumerate(scenarios):
            entry["order"] = n
        used = {e["shelf"] for e in scenarios}
        every = [SHELF_OWN, *file_shelves, SHELF_UNSORTED]
        return [
            {k: shelf[k] for k in ("id", "title", "says", "hidden")}
            for shelf in every
            if shelf["id"] in used
        ]

    # -- the ships' kinds, fits and roles (package 96b, step 5) -------------------------

    _kinds: list[dict[str, Any]] | None = None
    _fits: dict[str, dict[str, Any]] | None = None
    _fits_lock = threading.Lock()

    def kinds(self) -> list[dict[str, Any]]:
        """What another ship may be (`world.ships.DESCRIPTIONS`), each with her ship file,
        her rig and what she is in the file's words, the fit she carries as that kind and
        the roles her file gives her (package 75; "" and [] where the file gives none): the
        ship's card fills its blanks from these and invents nothing."""
        if Harbour._kinds is None:
            from freesail.world.ships import DESCRIPTIONS, description

            out = []
            for key in DESCRIPTIONS:
                d = description(key)
                out.append(
                    {
                        "id": key,
                        "file": str(d.get("file") or ""),
                        "rig": str(d.get("rig") or ""),
                        "what": str(d.get("what") or ""),
                        "fit": str(d.get("fit") or ""),
                        "roles": [str(r) for r in d.get("roles") or []],
                    }
                )
            Harbour._kinds = out
        return Harbour._kinds

    _posts: dict[str, list[str]] | None = None

    def posts(self) -> dict[str, list[str]]:
        """The posts of each ship file's wardroom (package 96b, step 7): the roles of
        `data/people/<her file's name>.yaml`, by her ship file, in the file's order; none
        for a ship with no wardroom file. A person the scenario names by one of these is
        the officer of her muster at that post; by any other role, a person added."""
        if Harbour._posts is None:
            out: dict[str, list[str]] = {}
            for p in sorted(SHIPS_DIR.glob("*.yaml")):
                if _is_boat(p):
                    continue
                roles: list[str] = []
                with contextlib.suppress(OSError, yaml.YAMLError, AttributeError, TypeError):
                    doc = yaml.safe_load(
                        (ROOT / "data" / "people" / p.name).read_text(encoding="utf-8")
                    )
                    for entry in (doc or {}).get("wardroom") or []:
                        role = " ".join(str(entry.get("role") or "").lower().split())
                        if role and role not in roles:
                            roles.append(role)
                out[_rel(p)] = roles
            Harbour._posts = out
        return Harbour._posts

    @staticmethod
    def squadron_words() -> dict[str, Any]:
        """What a squadron's card chooses from (package 96b, step 6): the game's own kinds
        and formations (`world.squadrons.KINDS`, `FORMATIONS`), the books a set may sail by
        (`data/squadrons/`), and the words that name the player's ship among the members."""
        from freesail.world.squadrons import FORMATIONS, KINDS, PLAYER_ID

        books = sorted(p.stem for p in (ROOT / "data" / "squadrons").glob("*.yaml"))
        return {
            "kinds": list(KINDS),
            "formations": list(FORMATIONS),
            "books": books,
            "player": PLAYER_ID,
        }

    def fits(self) -> dict[str, dict[str, Any]]:
        """Each ship file's fits of guns by name and the one she carries when none is said
        (`armament.fits`, `armament.default`; a file with no armament has none): what the
        player's `ship.fit` and another ship's `fit` may be. Read once (the ships' files
        are long)."""
        with Harbour._fits_lock:
            if Harbour._fits is not None:
                return Harbour._fits
            from freesail.ship.loader import load_spec

            out: dict[str, dict[str, Any]] = {}
            for p in sorted(SHIPS_DIR.glob("*.yaml")):
                if _is_boat(p):
                    continue
                names: list[str] = []
                default = ""
                with contextlib.suppress(Exception):  # a file that does not load has none
                    armament = load_spec(_rel(p)).armament
                    if armament is not None:
                        names = [str(n) for n in armament.fits]
                        default = str(armament.default or "")
                out[_rel(p)] = {"fits": names, "default": default}
            Harbour._fits = out
        return Harbour._fits

    def ship_warnings(self, fields: dict[str, Any]) -> list[str]:
        """What the loader takes of the other ships and the game would refuse or pass over
        later, said at the proof (the design's traps 4 and 5): a fit her kind's file has
        not (refused only when she is promoted to a full crew), and a heading (read by
        nothing: she heads for her first mark)."""
        from freesail.ship.schema import UNARMED
        from freesail.world.ships import description, description_key

        out: list[str] = []
        fits = self.fits()
        ships = fields.get("ships") if isinstance(fields.get("ships"), list) else []
        for s in ships:
            if not isinstance(s, dict):
                continue
            name = str(s.get("name") or s.get("id") or s.get("description") or "a ship")
            key = description_key(str(s.get("description") or s.get("kind") or ""))
            fit = " ".join(str(s.get("fit") or "").split())
            if key is not None and fit and fit != UNARMED:
                known = fits.get(str(description(key).get("file") or ""), {}).get("fits") or []
                if fit not in known:
                    has = ", ".join(known) if known else "none"
                    out.append(
                        f"  To know: {name}'s fit '{fit}' is none of her file's ({has}, or "
                        f"{UNARMED}); the game takes it now and refuses her when she comes "
                        "close and is given her full crew."
                    )
            if s.get("heading_deg") is not None:
                out.append(
                    f"  To know: {name}'s heading is read by nothing; another ship heads along "
                    "the first leg of her goal."
                )
        return out

    def regions(self) -> list[dict[str, Any]]:
        from freesail.world.chart import load_manifest

        manifest = load_manifest()
        return [
            {"id": rid, "title": str(spec.get("title") or rid), "bounds": spec.get("bounds")}
            for rid, spec in (manifest.get("regions") or {}).items()
        ]

    def ports(self) -> list[dict[str, Any]]:
        """Every port with its road (the anchorage the port's file names, placed by the
        chart's feature) and the region it lies in: a start the maker offers."""
        if self._ports is not None:
            return self._ports
        from freesail.world.chart import ChartError, load_chart
        from freesail.world.ports import load_port, port_files

        try:
            chart = load_chart("atlantic-east")
        except ChartError:
            chart = None
        regions = self.regions()
        out = []
        for pid, path in port_files().items():
            try:
                port = load_port(path, chart)
                spot = port.anchorage
            except Exception:  # noqa: BLE001  (a port the chart cannot place is left out)
                continue
            lat, lon = spot.position.lat_deg, spot.position.lon_deg
            region = next(
                (
                    r["id"]
                    for r in regions
                    if r.get("bounds")
                    and r["bounds"]["south"] <= lat <= r["bounds"]["north"]
                    and r["bounds"]["west"] <= lon <= r["bounds"]["east"]
                ),
                "",
            )
            out.append(
                {
                    "id": pid,
                    "name": port.name,
                    "road": spot.name,
                    "lat_deg": round(lat, 4),
                    "lon_deg": round(lon, 4),
                    "region": region,
                    "nation": port.nation,
                }
            )
        self._ports = out
        return out

    def chart(self, region: str) -> dict[str, Any]:
        """A region's coast, simplified, its bounds and the ports in it: the maker's chart,
        for pricking a start (no truth's depth, nothing a player would not see on the
        game's own chart)."""
        if region in self._charts:
            return self._charts[region]
        from freesail.world.chart import ChartError, load_chart

        try:
            chart = load_chart(region)
        except (ChartError, KeyError) as e:
            raise HarbourError(f"There is no chart of '{region}' ({e}).", 404) from None
        south, north, west, east = chart.bounds
        coast = []
        for line in chart.coast_lines():
            kept: list[list[float]] = []
            for lon, lat in line:
                if (
                    kept
                    and abs(lon - kept[-1][0]) < COAST_STEP_DEG
                    and abs(lat - kept[-1][1]) < COAST_STEP_DEG
                ):
                    continue
                kept.append([round(lon, 4), round(lat, 4)])
            if len(kept) >= 2:
                coast.append(kept)
        out = {
            "region": region,
            "title": chart.spec.get("title", region) if hasattr(chart, "spec") else region,
            "bounds": {"south": south, "north": north, "west": west, "east": east},
            "coast": coast,
            "ports": [p for p in self.ports() if p["region"] == region],
        }
        self._charts[region] = out
        return out

    # -- the game ------------------------------------------------------------------

    def start(self, choices: dict[str, Any]) -> dict[str, Any]:
        """A new game from the page's choices, made by the server's own `prepare_game` and
        taken up in place of the one in play (the clock held, as at every start: the
        driver's `go` runs it). Refused in words."""
        from freesail.ui import server

        s, _ = self.settings_or_defaults()
        args = server.server_parser().parse_args([])
        scenario = str(choices.get("scenario") or "").strip()
        ship = str(choices.get("ship") or "").strip()
        load = str(choices.get("load") or "").strip()
        if not (scenario or ship or load):
            raise HarbourError("Choose a scenario, a ship or a save to load.")
        # every file the start names lies in the server's folders (package 115, part A),
        # a save in the saves place or the game's folder; refused in words, unopened
        try:
            args.scenario = str(self.places.readable(scenario, "scenario")) if scenario else None
            args.ship = str(self.places.readable(ship, "ship's file")) if ship else None
            args.load = str(self.places.save_to_load(load)) if load else None
            book = str(choices.get("standing_orders") or "").strip()
            args.standing_orders = str(self.places.book(book)) if book else None
            brief = str(choices.get("director_brief") or "").strip()
            args.director_brief = self.places.brief(brief) if brief else None
        except PlaceRefused as e:
            raise HarbourError(str(e), 403) from None

        def number(name: str, kind: type, default: Any = None) -> Any:
            value = choices.get(name)
            if value in (None, ""):
                return default
            try:
                return kind(value)
            except (TypeError, ValueError):
                raise HarbourError(
                    f"The {name.replace('_', ' ')} is a number, not '{value}'."
                ) from None

        args.seed = number("seed", int)
        game = s.get("game") or {}
        args.time = number("time", float, float(game.get("compression") or 1.0))
        seat = str(
            choices.get("seat") if choices.get("seat") is not None else game.get("seat") or ""
        )
        args.seat = seat.strip() or None
        pace = str(choices.get("pace") or game.get("pace") or "rule")
        if pace not in settings_mod.PACES:
            raise HarbourError(f"The pace is one of {', '.join(settings_mod.PACES)}.")
        args.lockstep = pace == "lockstep"
        args.free_running = pace == "free"
        crewed = game.get("crewed") or {}
        args.crewed_cap = number("crewed_cap", int, crewed.get("cap"))
        args.crewed_range = number("crewed_range", float, crewed.get("range_nm"))
        business = str(choices.get("business") or "").strip().lower()
        if business not in ("", "on", "off"):
            raise HarbourError("The business is on, off, or as the scenario says.")
        args.business = business or None
        args.ease_on_station = bool(choices.get("ease_on_station"))
        # package 96b, step 3: the ship the player is aboard (the server's `--ship`), and
        # the wind and the heading of a bare ship (`--wind`, `--heading`), as the command
        # line has always taken them
        args.aboard = " ".join(str(choices.get("aboard") or "").split()) or None
        wind = str(choices.get("wind") or "").replace(" ", "")
        if wind:
            parts = wind.split(",")
            try:
                if len(parts) != 2:
                    raise ValueError
                from_deg, knots = float(parts[0]), float(parts[1])
            except ValueError:
                raise HarbourError(
                    "The wind is where it blows from in degrees and its knots, as '225,15'."
                ) from None
            if not (0.0 <= from_deg <= 360.0 and 0.0 <= knots <= 100.0):
                raise HarbourError(
                    "The wind is from 0 to 360 degrees and of 0 to 100 knots, as '225,15'."
                )
            args.wind = f"{from_deg:g},{knots:g}"
        args.heading = number("heading", float)
        if args.heading is not None and not 0.0 <= args.heading <= 360.0:
            raise HarbourError("The heading is from 0 to 360 degrees.")
        lines: list[str] = []
        try:
            world = server.prepare_game(args, say=lines.append)
        except SystemExit as e:
            raise HarbourError(str(e) or "The game could not be started.") from None
        except (OSError, ValueError, KeyError) as e:
            raise HarbourError(f"The game could not be started: {e}") from None
        except Exception as e:  # noqa: BLE001  (an OrderError of the seat, and the like)
            raise HarbourError(f"The game could not be started: {e}") from None
        from freesail.ui.console import PACE_FREE, PACE_LOCKSTEP, PACE_RULE

        rule = {"rule": PACE_RULE, "lockstep": PACE_LOCKSTEP, "free": PACE_FREE}[pace]
        # who the scenario says holds each station (step 9: the page offers the doors of those
        # it gives to a model), read before the game is taken up
        plan = self.plan(scenario)
        # the driver's lock held from the world's replacing to the game's words: `game_state`
        # reads under it, not under the harbour's, and a page that asks between must find one
        # whole game. Without it a first start could be found started with its plan not yet
        # said (the stations' table then showed the officer with no model asked for, and the
        # browser's test of it failed once in many runs beside other workers; found by package
        # 90's engine builder at A1d's tiers), and a second start the new world beside the
        # last game's words and plan (the lead's checker). The harbour's lock first, then the
        # driver's, as everywhere; nothing takes them the other way round.
        with self._lock, self.driver.lock:
            self.driver.replace_world(
                world, compression=args.time, pace=rule, ease_on_station=args.ease_on_station
            )
            self.game = {
                "scenario": scenario,
                "ship": ship,
                "load": load,
                "seat": args.seat or "",
                "aboard": args.aboard or "",
                "pace": pace,
                "director_brief": args.director_brief or "",
                "lines": lines,
                "plan": plan,
            }
            self.started = True
            self.games += 1
        return {"lines": lines, "game": self.game_state()}

    def end(self, lose_unsaved: bool = False) -> dict[str, Any]:
        """The game in play ended, the harbour kept (the owner's note 2 of gate M7): the
        doors of the models' stations closed as the harbour closes one (`stop_door`), the
        clock stopped and the World let go for one with no game in it, as the harbour
        begins with none; nothing saved is touched. Refused in words while what was played
        since the last save would be lost, until the player says so (`lose_unsaved`)."""
        from freesail.core.world import Scenario, World
        from freesail.ui.console import DEFAULT_SEED

        # the harbour's lock held throughout, so that no start or door begun from another
        # page comes between the asking and the end; the driver's only for the World's
        # replacing (the start's order: the harbour's first, then the driver's), so that a
        # page that asks while a game ends finds the whole game or none
        with self._lock:
            if not self.started:
                raise HarbourError("No game is in play to end.", 409)
            lost = self.driver.unsaved()
            if lost and not lose_unsaved:
                raise HarbourError(lost + " End it all the same, or save it first.", 409)
            # the doors first, the driver's lock not held: a door stopping asks the game to
            # release its station, and the release saves the station's record as it always has
            for door in list(self.doors.values()):
                if door.running:
                    with contextlib.suppress(Exception):
                        self.stop_door(door.id)
            with self.driver.lock:
                self.driver.replace_world(
                    World(seed=DEFAULT_SEED, scenario=Scenario()),
                    compression=self.driver.compression,
                    pace=self.driver.pace.rule,
                )
                self.game = {}
                self.started = False
                self.games += 1
                self.seat_doors, self._seat_world = {}, None
            # a door begun from a page while the doors stopped (`start_door` takes no lock:
            # the clock's tending starts the director's under the driver's) is stopped too;
            # with no game in play none can begin after
            for door in list(self.doors.values()):
                if door.running:
                    with contextlib.suppress(Exception):
                        self.stop_door(door.id)
        return {"lines": ["The game is ended."], "game": self.game_state()}

    def game_state(self) -> dict[str, Any]:
        from freesail.agents import director as director_mod

        d = self.driver
        with d.lock:
            w = d.world
            seat = getattr(w, "player_seat", None)
            brief = director_mod.brief_of(w)
            ship = getattr(w, "ship", None)
            name = getattr(ship, "name", "") or getattr(getattr(ship, "spec", None), "name", "")
            out = {
                "started": self.started,
                "title": getattr(getattr(w, "scenario", None), "name", "") or "",
                "seed": w.seed,
                "tick": w.clock.tick,
                "stamp": w.clock.stamp(),
                "running": d.running,
                "compression": d.compression,
                "pace": d.pace.rule,
                "ship": str(name or ""),
                "seat": (
                    f"the player at the {seat.station.name}'s station"
                    if seat is not None and not seat.agent.released
                    else "the player at the captain's prompt"
                ),
                "director": brief.name if brief is not None else "",
                "chosen": dict(self.game),
                "games": self.games,
                # the stations' table (package 96b, step 9): the other ships with a captain
                # of their own, whose captain's station a door may ask for
                "captains": self._captains(w) if self.started else [],
            }
        return out

    @staticmethod
    def _captains(world: Any) -> list[str]:
        """The other ships on the sea with a captain of their own (an intent or a free
        intent: a brain), by name: those whose captain's station a model's door may ask for
        (the doors' `--ship`)."""
        out: list[str] = []
        vessels = getattr(getattr(world, "vessels", None), "vessels", None) or []
        own = getattr(getattr(world, "vessel", None), "id", None)
        for v in vessels:
            if getattr(v, "brain", None) is None or getattr(v, "done", False):
                continue
            if own is not None and getattr(v, "id", None) == own:
                continue
            name = str(getattr(v, "name", "") or "")
            if name and name not in out:
                out.append(name)
        return out

    def plan(self, scenario: str) -> dict[str, str]:
        """Who the scenario says holds each station of the player's ship (its `stations:`;
        package 59, read by the page from step 9 of package 96b: the game itself reads only
        the player's seat): the station's name to player, model or rules; {} where the
        scenario says none or cannot be read."""
        if not scenario:
            return {}
        from freesail.world.scenarios import ScenarioError, read_scenario_text

        try:
            _text, fields = read_scenario_text(self.scenario_path(scenario))
        except (HarbourError, OSError, ScenarioError):
            return {}
        stations = fields.get("stations")
        if not isinstance(stations, dict):
            return {}
        return {
            " ".join(str(k).lower().split()): " ".join(str(v).lower().split())
            for k, v in stations.items()
        }

    def stations(self) -> list[dict[str, Any]]:
        """The stations held and by whom: the agent API's (a model's, through a door) and
        the player's seat."""
        d = self.driver
        out: list[dict[str, Any]] = []
        with d.lock:
            if d.desk is not None:
                # the desk lists, beside the stations held, the seats still in their consent
                # conversation and the seats stopped (a consent declined, a door stopped
                # before an answer), and those without their ship: each is passed on with
                # its phase ("station": seated; "consent": asked, not yet answered;
                # "stopped": nobody's), and an unseated seat's ship is had from the desk's
                # own seat (package 96b, step 9's mend: the table counts only a seated
                # station as held)
                unseated = [s for s in d.desk.seats.values() if s.phase != "station"]
                for st in d.desk.stations():
                    phase = str(st.get("phase") or "station")
                    ship = str(st.get("ship") or "")
                    if phase != "station" and not ship:
                        seat = next(
                            (
                                s
                                for s in unseated
                                if s.station == st.get("station")
                                and s.model_name == st.get("model_name")
                                and s.phase == phase
                            ),
                            None,
                        )
                        if seat is not None:
                            unseated.remove(seat)
                            ship = str(seat.ship or "")
                    out.append(
                        {
                            "station": st.get("station"),
                            "ship": ship,
                            "holder": st.get("model_name") or "",
                            "door": st.get("door") or "",
                            "line": st.get("line") or "",
                            "phase": phase,
                        }
                    )
            seat = getattr(d.world, "player_seat", None)
            if seat is not None and not seat.agent.released:
                name = seat.station.name
                out = [x for x in out if x["station"] != name or x["ship"]]
                out.append(
                    {
                        "station": name,
                        "ship": "",
                        "holder": "the player",
                        "door": "the browser",
                        "line": f"The {name}: the player, at the browser.",
                        "phase": "station",
                    }
                )
        return out

    def state(self) -> dict[str, Any]:
        s, error = self.settings_or_defaults()
        desktop = self.desktop_path(s)
        present: list[str] = []
        with contextlib.suppress(OSError, ValueError):
            import json

            doc = json.loads(desktop.read_text(encoding="utf-8"))
            present = sorted(
                k for k in (doc.get("mcpServers") or {}) if k.startswith(settings_mod.ENTRY_PREFIX)
            )
        return {
            "game": self.game_state(),
            "stations": self.stations(),
            "doors": [door.state() for door in self.doors.values()],
            "saves": self.saves(),
            "settings": {"path": str(self.path), "error": error},
            "credential": settings_mod.credential_words(),
            "desktop": {"path": str(desktop), "entries": present},
            "url": self.game_url,
        }

    # -- the doors -----------------------------------------------------------------

    def desktop_path(self, s: dict[str, Any] | None = None) -> Path:
        s = s if s is not None else self.settings_or_defaults()[0]
        given = str((s.get("places") or {}).get("desktop_config") or "")
        return Path(given).expanduser() if given else settings_mod.desktop_config_path()

    def desktop(self, stations: list[str], ship: str = "", write: bool = False) -> dict[str, Any]:
        """The desktop client's entries for the stations ticked, one each, and the client's
        file as it would read with them (shown first); written, with the old file kept
        beside it, only when `write` (the player's confirmation)."""
        s, error = self.settings_or_defaults()
        if error:
            raise HarbourError(error)
        chosen = [" ".join(str(x).lower().split()) for x in stations if str(x).strip()]
        if not chosen:
            raise HarbourError("Tick a station or more for the desktop client's entries.")
        entries = {
            settings_mod.entry_name(st, ship): settings_mod.desktop_entry(
                st, s, self.game_url, ship=ship
            )
            for st in chosen
        }
        path = self.desktop_path(s)
        existing = path.read_text(encoding="utf-8") if path.exists() else None
        try:
            doc = settings_mod.merged_desktop_config(existing, entries)
        except SettingsError as e:
            raise HarbourError(str(e)) from None
        import json

        out: dict[str, Any] = {
            "path": str(path),
            "entries": entries,
            "text": json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
            "written": False,
            "named": bool(((s.get("doors") or {}).get("desktop") or {}).get("model_name")),
        }
        if write:
            try:
                backup = settings_mod.write_desktop_config(path, entries)
            except (SettingsError, OSError) as e:
                raise HarbourError(f"The client's file was not written: {e}") from None
            out["written"] = True
            out["backup"] = str(backup) if backup else ""
        return out

    def shortcut(self, write: bool = False) -> dict[str, Any]:
        path = settings_mod.shortcut_path()
        text = settings_mod.shortcut_text(root=ROOT)
        out = {"path": str(path), "text": text, "written": False}
        if write:
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8", newline="")
                if not sys.platform.startswith("win"):
                    path.chmod(0o755)
            except OSError as e:
                raise HarbourError(f"The shortcut was not written: {e}") from None
            out["written"] = True
        return out

    def door_argv(
        self, kind: str, station: str, ship: str = "", seat_model: str = "", model: str = ""
    ) -> list[str]:
        """A door's command line from the settings: the module's own flags, nothing more.
        `seat_model` is a director's seat's model (package 67): one of the models the
        settings can call, with its dialect, and the seated door's fold where the settings
        name one (`--budget-tokens`). `model` is the owner's own choice for a door he starts
        from the stations' table (package 96b, step 9): one of the same models the settings
        can call, with its dialect, and nothing more (no seat's fold: it is no seat of the
        director's); "" is the API door's own model, as before."""
        chosen = seat_model or model
        s, error = self.settings_or_defaults()
        if error:
            raise HarbourError(error)
        doors = s.get("doors") or {}
        station = " ".join(str(station).lower().split())
        if not station:
            raise HarbourError("Name the station the door asks for.")
        if kind == "api":
            d = doors.get("api") or {}
            if chosen:
                known = settings_mod.callable_models(s)
                if chosen not in known:
                    raise HarbourError(
                        "The settings call no model by that name (the API door's model and "
                        "the models beside it, doors.api.models)."
                    )
                model, dialect = chosen, known[chosen]
            else:
                model, dialect = str(d.get("model") or ""), str(d.get("dialect") or "")
            if not model:
                raise HarbourError(
                    "Name the API door's model in the settings (doors, the API door's model), "
                    "exactly as the API knows it: it has no default."
                )
            argv = [sys.executable, "-m", "freesail.agents.api", "--game", self.game_url]
            argv += ["--model", model, "--station", station]
            if dialect:
                argv += ["--dialect", dialect]
            if d.get("effort"):
                argv += ["--effort", str(d["effort"])]
            if seat_model and d.get("seat_budget_tokens") not in (None, ""):
                argv += ["--budget-tokens", str(d["seat_budget_tokens"])]
        elif kind == "local":
            if model:
                raise HarbourError(
                    "The local runner serves the one model its settings name; a model is "
                    "chosen for the API door alone."
                )
            d = doors.get("local") or {}
            argv = [sys.executable, "-m", "freesail.agents.local", "--game", self.game_url]
            argv += ["--endpoint", str(d.get("endpoint") or "http://127.0.0.1:8080")]
            if d.get("model"):
                argv += ["--model", str(d["model"])]
            argv += ["--station", station]
        else:
            raise HarbourError(f"There is no door '{kind}'; the harbour starts api and local.")
        if ship:
            argv += ["--ship", ship]
        return argv + [str(f) for f in d.get("flags") or []]

    def start_door(
        self,
        kind: str,
        station: str,
        ship: str = "",
        *,
        seat: str = "",
        seat_model: str = "",
        by: str = "",
        model: str = "",
    ) -> dict[str, Any]:
        """A door started as the server's subprocess: the owner's from the page, or a
        director's seat's (package 67: `seat` its key, `seat_model` its model, `by` "the
        director"), shown in the doors tab beside the owner's and marked so."""
        argv = self.door_argv(kind, station, ship, seat_model=seat_model, model=model)
        if not self.started:
            raise HarbourError("Start a game first: a door is a client of the game in play.")
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        env["PYTHONPATH"] = os.pathsep.join(
            [str(ROOT)] + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else [])
        )
        ident = f"d{next(self._ids)}"
        try:
            door = Door(
                ident,
                kind,
                " ".join(station.lower().split()),
                argv,
                ship=ship,
                env=env,
                by=by,
                seat=seat,
            )
        except OSError as e:
            raise HarbourError(f"The door could not be started: {e}") from None
        self.doors[ident] = door
        return door.state()

    # -- the director's seats' doors (package 67; spec M7b §2a) ---------------------------

    def tend_seats(self) -> None:
        """The game starts the director's door (package 67): every seat held on the World
        in play and not yet served has the API door started for it as the harbour starts
        one from its page (its model one the settings can call, its key from the credential
        store in the door's own process, never the game's), marked the director's; a door
        whose seat is gone (unseat:, the spent budget, a lapse, a new game) is stopped if it
        still runs. Called by the driver's clock every tenth of a second, running or not;
        the stops are made off the clock's thread, since a stopping door asks the game to
        release its station."""
        if not self.started:
            return
        from freesail.world.orders import director_seats

        d = self.driver
        with d.lock:
            world = d.world
            if world is not self._seat_world:
                stale = [i for i in self.seat_doors.values() if i]
                self.seat_doors, self._seat_world = {}, world
            else:
                stale = []
            seats = {k: dict(v) for k, v in director_seats(world).items()}
            for key in [k for k in self.seat_doors if k not in seats]:
                ident = self.seat_doors.pop(key)
                if ident:
                    stale.append(ident)
            for key, seat in seats.items():
                if key in self.seat_doors:
                    continue
                station, ship = self._seat_station(world, key, seat)
                try:
                    started = self.start_door(
                        "api",
                        station,
                        ship,
                        seat=key,
                        seat_model=str(seat.get("model") or ""),
                        by="the director",
                    )
                except HarbourError as e:
                    self.seat_doors[key] = None
                    self._tell_director(
                        world,
                        f"No door was started for your seat ({seat.get('model')} at {station}"
                        f"{' of ' + ship if ship else ''}): {e.words} The seat is held as a "
                        "record; a door started by hand for it is admitted under its budget.",
                    )
                    continue
                self.seat_doors[key] = started["id"]
                self._tell_director(
                    world,
                    f"The harbour has started the API door for your seat ({seat.get('model')} "
                    f"at {station}{' of ' + ship if ship else ''}); it is admitted under the "
                    "seat's budget when it comes.",
                )
        for ident in stale:
            door = self.doors.get(ident or "")
            if door is not None and door.running:
                threading.Thread(target=self._stop_seat_door, args=(door,), daemon=True).start()

    def _stop_seat_door(self, door: Door) -> None:
        """A seat's door whose seat is gone: one whose station the game has released ends
        of itself (the door says its station was released) and is given the time to; one
        still waiting (no admission yet, a consent conversation) is stopped."""
        desk = self.driver.desk
        with self.driver.lock:
            seat = desk.seat_at(door.station, door.ship) if desk is not None else None
            released = bool(seat is not None and seat.released)
        if released:
            with contextlib.suppress(subprocess.TimeoutExpired):
                door.proc.wait(timeout=SEAT_DOOR_GRACE_S)
        door.stop()

    @staticmethod
    def _seat_station(world: Any, key: str, seat: dict[str, Any]) -> tuple[str, str]:
        """The station and the ship (her name; "" for the player's own) a seat's door asks
        for."""
        from freesail.agents.agent import CAPTAIN

        ship_id = str(seat.get("ship") or "") if "station" in seat else key
        station = str(seat.get("station") or CAPTAIN)
        if not ship_id:
            return station, ""
        vessel = world.vessels.find(ship_id)
        return station, (vessel.name if vessel is not None else ship_id)

    @staticmethod
    def _tell_director(world: Any, text: str) -> None:
        """A notice for the director's next sample (never a line of any log)."""
        from freesail.agents import director as director_mod

        held = director_mod.seated(world)
        notices = getattr(getattr(held, "agent", None), "notices", None)
        if isinstance(notices, list):
            notices.append(text)

    def door(self, ident: str) -> Door:
        door = self.doors.get(ident)
        if door is None:
            raise HarbourError(f"There is no door {ident} started from the harbour.", 404)
        return door

    def stop_door(self, ident: str) -> dict[str, Any]:
        door = self.door(ident)
        door.stop()
        self._release(door)
        return door.state()

    def _release(self, door: Door) -> None:
        """A station its stopped door held is released at the game, as the door's own
        Ctrl-C releases it (Windows has none to send: the door is ended there)."""
        desk = self.driver.desk
        if desk is None:
            return
        from freesail.agents.remote import DeskError

        seat = desk.seat_at(door.station, door.ship)
        if seat is None or seat.released:
            return
        with contextlib.suppress(DeskError):
            desk.release(door.station, "its door was stopped from the harbour", seat.key, door.ship)

    def close(self) -> None:
        for door in list(self.doors.values()):
            with contextlib.suppress(Exception):
                door.stop()

    # -- the scenario maker ----------------------------------------------------------

    def scenario_path(self, path: str) -> Path:
        """A scenario the harbour may read: the game's or the player's own, by the path the
        lists give."""
        p = Path(path)
        if not p.is_absolute():
            p = ROOT / p
        p = p.resolve()
        allowed = [GAME_SCENARIOS.resolve(), self.scenarios_place().resolve()]
        if not any(p == a or a in p.parents for a in allowed):
            raise HarbourError(
                f"{path} is neither the game's scenario nor one of yours; the harbour reads "
                "those under data/scenarios and your scenarios place.",
                403,
            )
        if p.suffix not in (".yaml", ".yml"):
            raise HarbourError(f"{path} is not a scenario file (.yaml).")
        return p

    def read_scenario(self, path: str) -> dict[str, Any]:
        from freesail.world.scenarios import ScenarioError, read_scenario_text

        p = self.scenario_path(path)
        try:
            text, fields = read_scenario_text(p)
        except (OSError, ScenarioError) as e:
            raise HarbourError(str(e), 404 if isinstance(e, OSError) else 400) from None
        own = self.scenarios_place().resolve() in p.parents
        where = None
        if fields.get("position") is not None:
            from freesail.world.geo import Position

            with contextlib.suppress(TypeError, ValueError):
                pos = Position.from_dict(fields["position"])
                where = [round(pos.lat_deg, 4), round(pos.lon_deg, 4)]
        return {
            "path": _rel(p) if not own else str(p),
            "own": own,
            "name": p.stem,
            "text": text,
            "fields": fields,
            "position_deg": where,  # for the form's latitude and longitude
            **self._said(p, fields),
            "blocks": self.blocks_of(fields),
        }

    # -- what is offered as the file's own words (package 96b, step 8; the design's §2.5) --

    BLOCKS = ("systems", "ports")

    @staticmethod
    def blocks_of(fields: dict[str, Any]) -> dict[str, str]:
        """The two blocks of a scenario the sheet shows as the file's own words and not as
        fields: the weather's systems (`weather: systems`: a low, its fronts and its track
        by the hour) and the ports' state (`ports` as a mapping: a port closed, blockaded,
        its letters and its news). Each as YAML text, "" where the scenario has none."""
        weather = fields.get("weather")
        systems = weather.get("systems") if isinstance(weather, dict) else None
        ports = fields.get("ports")

        def text(value: Any) -> str:
            return yaml.safe_dump(
                value, sort_keys=False, allow_unicode=True, default_flow_style=None, width=92
            )

        if isinstance(ports, list):
            # a list of ports is each of them with nothing said of it: the box comes up
            # holding that, so that a port's state added there keeps the other ports
            ports = {str(p): {} for p in ports}
        return {
            "systems": text(systems) if systems else "",
            "ports": text(ports) if isinstance(ports, dict) and ports else "",
        }

    def with_blocks(self, fields: Any, blocks: Any) -> Any:
        """The fields with the blocks the page sent as words read into them (only the
        blocks it sent: an untouched block is not sent, and the scenario's own is kept).
        The systems' words are a list of systems, laid under `weather: systems` ("" takes
        them out); the ports' words a mapping of each port to its state, which becomes
        `ports` whole ("" leaves `ports` as the fields have it). Refused in words when the
        text is no YAML or not of that shape; what each system and each port's state may
        say is the loader's to refuse, at the proof."""
        if not isinstance(blocks, dict) or not isinstance(fields, dict):
            return fields
        import copy

        out = copy.deepcopy(fields)
        for name, words in blocks.items():
            if name not in self.BLOCKS:
                raise HarbourError(f"There is no block '{name}'; the sheet has systems and ports.")
            text = str(words or "")
            # refused before any load: a box's words longer than a scenario's block ever is,
            # and any anchor or alias (a few hundred bytes of nested aliases load as
            # gigabytes: the tokens are scanned, which builds nothing)
            if len(text) > BLOCK_MAX_CHARS:
                raise HarbourError(
                    f"The {name}' words are {len(text)} characters; the box takes "
                    f"{BLOCK_MAX_CHARS} at most."
                )
            try:
                if _has_anchor_or_alias(text):
                    raise HarbourError(
                        "The box's words use an anchor or an alias (& or *), which the sheet "
                        "does not take: write each thing out where it is said."
                    )
                value = yaml.safe_load(text) if text.strip() else None
            except yaml.YAMLError as e:
                where = getattr(e, "problem_mark", None)
                at = f", line {where.line + 1}" if where is not None else ""
                raise HarbourError(
                    f"The {name}' words could not be read{at}: {getattr(e, 'problem', e)}."
                ) from None
            value = _plain(value)
            if name == "systems":
                weather = out.get("weather")
                if isinstance(weather, list):  # the old form, the pinned wind alone
                    weather = {"wind": weather}
                weather = dict(weather) if isinstance(weather, dict) else {}
                if value is None:
                    weather.pop("systems", None)
                elif isinstance(value, list):
                    weather["systems"] = value
                else:
                    raise HarbourError(
                        "The weather's systems are a list, each beginning '- name:' with its "
                        "kind, radius_km, fronts and track."
                    )
                if weather:
                    out["weather"] = weather
                else:
                    out.pop("weather", None)
            elif value is not None:
                if not isinstance(value, dict):
                    raise HarbourError(
                        "The ports' state is each port's id and under it what is said of it "
                        "(closed_to, state, blockade, letters, news), as 'brest: {closed_to: "
                        "[britain]}'."
                    )
                out["ports"] = value
        return out

    def unread_warnings(self, fields: dict[str, Any]) -> list[str]:
        """What a scenario says that the game reads nowhere, said at the proof (the
        design's traps 1, 2, 3 and 6): a key the loader does not know; the chart's year
        and the almanac; the `nations:` block; a station held by "model" or "rules"; and,
        of a scenario that begins in another year than 1805, that its ports are that day's
        and its wars June 1805's."""
        out: list[str] = []
        for key in fields:
            if str(key) not in LOADER_KEYS:
                out.append(
                    f"  To know: '{key}' is no key the game reads; it is kept in the file and "
                    "does nothing (a key misspelt is passed over in silence)."
                )
        papers = fields.get("papers") if isinstance(fields.get("papers"), dict) else {}
        unread = [
            w for k, w in (("chart", "the chart's year"), ("almanac", "the almanac")) if k in papers
        ]
        if unread:
            out.append(
                f"  To know: {' and '.join(unread)} in her papers "
                f"{'are' if len(unread) > 1 else 'is'} read by nothing in the game."
            )
        if fields.get("nations") is not None:
            out.append(
                "  To know: the nations' block (the wars and the letters of marque of this "
                "scenario's day) is checked and kept, and read by nothing yet: the wars in "
                "play are those of June 1805."
            )
        stations = fields.get("stations") if isinstance(fields.get("stations"), dict) else {}
        idle = [str(k) for k, v in stations.items() if str(v).lower().strip() in ("model", "rules")]
        if idle:
            out.append(
                f"  To know: the game itself reads only the station you hold; 'model' and "
                f"'rules' ({', '.join(idle)}) seat nobody when the game starts. The harbour's "
                "stations tab offers the door of each station given to a model."
            )
        ports = fields.get("ports")
        if isinstance(ports, list | dict):
            # the ports in play named, and a port the scenario leans on left out of them:
            # the port a ship is leaving, and a price list aboard (the two that name a port
            # by its id; the start is a place and a goal is words, neither a plain read)
            play = {str(p) for p in ports}
            ships = fields.get("ships") if isinstance(fields.get("ships"), list) else []
            for s in ships:
                port = str(s.get("departing") or "") if isinstance(s, dict) else ""
                if port and port not in play:
                    out.append(
                        f"  To know: {s.get('name') or s.get('id') or 'a ship'} is leaving "
                        f"{port}, which is not among the ports in play ({', '.join(sorted(play))})."
                    )
            lists = papers.get("price_lists") if isinstance(papers.get("price_lists"), list) else []
            for port in [str(p) for p in lists if str(p) not in play]:
                out.append(
                    f"  To know: the price list of {port} is aboard, and {port} is not among "
                    "the ports in play: a list counts only for a port in play."
                )
        with contextlib.suppress(ValueError, TypeError):
            year = int(str(fields.get("start"))[:4]) if fields.get("start") else 1805
            if year != 1805:
                out.append("  To know: " + year_words(year))
        return out

    @staticmethod
    def _said(p: Path, fields: dict[str, Any]) -> dict[str, Any]:
        """What a scenario is, for the page to say before it is started (package 96b, step
        3): the scenario's own lines as a driver prints them at the load (`lines`: the
        author's view, the file's path left out), or the loader's refusal in words
        (`refusal`); and the other ships the player may be aboard at the start (`aboard`:
        those with a captain of their own, an intent or a free intent, by name), which is
        what the server's `--ship` takes."""
        from freesail.world.scenarios import ScenarioError, load_scenario

        lines: list[str] = []
        refusal = ""
        try:
            lines = [ln.replace(f" ({p})", "") for ln in load_scenario(p).lines()]
        except (ScenarioError, OSError, ValueError, KeyError, yaml.YAMLError) as e:
            refusal = _scenario_words(str(e), p)
        ships = fields.get("ships") if isinstance(fields.get("ships"), list) else []
        aboard = [
            str(s.get("name") or s.get("id"))
            for s in ships
            if isinstance(s, dict)
            and (s.get("intent") or s.get("free_intent"))
            and (s.get("name") or s.get("id"))
        ]
        return {"lines": lines, "refusal": refusal, "aboard": aboard}

    def _original(self, source: str) -> tuple[str | None, str]:
        if not source:
            return None, "\n"
        from freesail.world.scenarios import newline_of

        p = self.scenario_path(source)
        try:
            return p.read_text(encoding="utf-8"), newline_of(p)
        except OSError as e:
            raise HarbourError(f"{source} could not be read ({e.strerror}).") from None

    def prove(self, fields: dict[str, Any], source: str = "") -> dict[str, Any]:
        """The scenario's text, proved by loading it as the console would: read by the
        loader, its World made, its standing orders and first orders given (an order refused
        is a refusal), the player's seat taken. The scenario's lines, or `HarbourError` in
        the loader's words."""
        from freesail.world.scenarios import (
            ScenarioError,
            begin,
            guard_lines,
            load_scenario,
            make_scenario_world,
            scenario_text,
        )

        if not isinstance(fields, dict):
            raise HarbourError("A scenario is a mapping of fields.")
        found, said = self._fields_in_places(fields)
        original, _ = self._original(source)
        try:
            text = scenario_text(fields, original)  # the player's own words, as written
            proved_text = scenario_text(found, original)  # each file as it was found
        except ScenarioError as e:
            raise HarbourError(f"The scenario was not written: {e}") from None
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "scenario.yaml"
            p.write_text(proved_text, encoding="utf-8")
            try:
                sf = load_scenario(p)
                world = make_scenario_world(sf)
                begin(world, sf)
            except (ScenarioError, OSError, ValueError, KeyError) as e:
                raise HarbourError(self._in_their_words(_scenario_words(str(e), p), said)) from None
            refused = [e for e in world.log if e.kind == "order.rejected"]
            if refused:
                raise HarbourError(
                    self._in_their_words(
                        "A first order or standing order was refused: "
                        + "; ".join(e.text for e in refused[:3]),
                        said,
                    )
                )
            seat = sf.player_seat
            if seat:
                from freesail.agents.seat import seat_station

                try:
                    seat_station(world, seat)
                except Exception as e:  # noqa: BLE001  (OrderError, in words)
                    raise HarbourError(f"stations: {e}") from None
            lines = [
                self._in_their_words(ln.replace(str(p), "this scenario"), said)
                for ln in sf.lines() + guard_lines(world)
            ]
            lines += self.ship_warnings(fields) + self.unread_warnings(fields)
        return {"text": text, "lines": lines}

    def _fields_in_places(self, fields: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
        """The files a scenario's fields name (her ship's file, the books, a director's
        brief) lie in the server's folders (package 115, part A), or the maker refuses them
        in words before the scenario is loaded and any of them opened. The fields to prove,
        each such file given by the path it was found at (the path checked is the path
        opened, whatever folder the server was started from); the fields written are the
        player's own words, unchanged."""
        import copy

        out = copy.deepcopy(fields)
        said: dict[str, str] = {}  # each path as found -> the player's own words for it

        def found(given: str, path: Any) -> str:
            said[str(path)] = given
            return str(path)

        try:
            ship = out.get("ship")
            if isinstance(ship, dict) and ship.get("file"):
                given = str(ship["file"])
                ship["file"] = found(given, self.places.readable(given, "ship's file"))
            if out.get("standing_orders"):
                out["standing_orders"] = [
                    found(str(b), self.places.book(str(b)))
                    for b in out.get("standing_orders") or []
                ]
            director = out.get("director")
            if isinstance(director, dict) and isinstance(director.get("brief"), str):
                given = director["brief"]
                director["brief"] = found(given, self.places.brief(given))
        except PlaceRefused as e:
            raise HarbourError(str(e), 403) from None
        return out, said

    @staticmethod
    def _in_their_words(text: str, said: dict[str, str]) -> str:
        """The proof's words with each file named as the player named it, not as it was
        found (its whole path)."""
        for path, given in sorted(said.items(), key=lambda kv: -len(kv[0])):
            if path != given:
                text = text.replace(path, given)
        return text

    def save_scenario(
        self,
        fields: dict[str, Any],
        name: str,
        source: str = "",
        book: str = "",
        overwrite: bool = False,
    ) -> dict[str, Any]:
        """Proved, then written under the player's scenarios place as `<name>.yaml` (with a
        drafted book beside it as `<name>.orders`, named in its standing orders), in the
        file's own form; the text it was read from kept where nothing changed."""
        from freesail.world.scenarios import write_scenario

        stem = "".join(c if c.isalnum() or c in "-_" else "-" for c in str(name).strip()).strip("-")
        if not stem:
            raise HarbourError("Name the scenario's file (letters, figures and dashes).")
        place = self.scenarios_place()
        if settings_mod.inside_repository(place):
            raise HarbourError(
                f"The scenarios place {place} is inside the game's folder; the maker writes "
                "your scenarios in your own place (the settings name it)."
            )
        target = place / f"{stem}.yaml"
        src = self.scenario_path(source) if source else None
        if target.exists() and not overwrite and (src is None or src != target.resolve()):
            raise HarbourError(
                f"{target} is there already; say to write over it, or give another name.", 409
            )
        fields = dict(fields)
        made_book = None
        if book.strip():
            made_book = place / f"{stem}.orders"
            place.mkdir(parents=True, exist_ok=True)
            made_book.write_text(book.strip() + "\n", encoding="utf-8")
            books = [str(x) for x in fields.get("standing_orders") or []]
            if str(made_book) not in books:
                fields["standing_orders"] = books + [str(made_book)]
        proved = self.prove(fields, source)
        original, newline = self._original(source)
        try:
            write_scenario(fields, target, original, newline=newline)
        except OSError as e:
            raise HarbourError(f"{target} was not written ({e.strerror}).") from None
        Harbour._names.pop(str(target), None)
        return {
            "path": str(target),
            "text": target.read_text(encoding="utf-8"),
            "lines": proved["lines"],
            "book": str(made_book) if made_book else "",
        }


def _scenario_words(words: str, tmp: Path) -> str:
    """The loader's refusal in the form's words: the temporary file's name left out."""
    return words.replace(f"{tmp}, ", "").replace(f"{tmp}: ", "").replace(str(tmp), "the scenario")


# ---------------------------------------------------------------------------
# The routes
# ---------------------------------------------------------------------------


def harbour_routes(h: Harbour) -> APIRouter:
    router = APIRouter()

    def call(fn: Any, *args: Any, **kw: Any) -> JSONResponse:
        try:
            return JSONResponse(fn(*args, **kw))
        except HarbourError as e:
            raise HTTPException(status_code=e.status, detail=e.words) from None
        except SettingsError as e:
            raise HTTPException(status_code=400, detail=str(e)) from None

    @router.get("/harbour", response_model=None)
    def harbour_page(request: Request) -> Response:
        return h.page(h.client_dir / "harbour.html", request.headers.get("host", ""))

    @router.get("/api/harbour/state")
    def api_state() -> JSONResponse:
        return call(h.state)

    @router.get("/api/harbour/catalogue")
    def api_catalogue() -> JSONResponse:
        return call(h.catalogue)

    @router.post("/api/harbour/start")
    def api_start(body: dict[str, Any]) -> JSONResponse:
        return call(h.start, body)

    @router.post("/api/harbour/end")
    def api_end(body: dict[str, Any]) -> JSONResponse:
        return call(h.end, bool(body.get("lose_unsaved")))

    @router.get("/api/harbour/settings")
    def api_settings() -> JSONResponse:
        s, error = h.settings_or_defaults()
        return JSONResponse(
            {
                "path": str(h.path),
                "settings": s,
                "error": error,
                "credential": settings_mod.credential_words(),
                "defaults": {
                    "scenarios": str(settings_mod.place(s, "scenarios", h.path)),
                    "saves": str(settings_mod.place(s, "saves", h.path)),
                    "desktop_config": str(settings_mod.desktop_config_path()),
                },
            }
        )

    @router.post("/api/harbour/settings")
    def api_settings_save(body: dict[str, Any]) -> JSONResponse:
        def save() -> dict[str, Any]:
            path = settings_mod.save_settings(body.get("settings") or {}, h.path)
            return {"path": str(path), "settings": h.settings()}

        return call(save)

    @router.post("/api/harbour/desktop")
    def api_desktop(body: dict[str, Any]) -> JSONResponse:
        return call(
            h.desktop,
            list(body.get("stations") or []),
            str(body.get("ship") or ""),
            bool(body.get("write")),
        )

    @router.post("/api/harbour/shortcut")
    def api_shortcut(body: dict[str, Any]) -> JSONResponse:
        return call(h.shortcut, bool(body.get("write")))

    @router.post("/api/harbour/doors")
    def api_door_start(body: dict[str, Any]) -> JSONResponse:
        return call(
            h.start_door,
            str(body.get("door") or ""),
            str(body.get("station") or ""),
            str(body.get("ship") or ""),
            # a model's name as the settings have it: its ends stripped, nothing within
            model=str(body.get("model") or "").strip(),
        )

    @router.get("/api/harbour/doors/{ident}")
    def api_door(ident: str, since: int = 0) -> JSONResponse:
        def read() -> dict[str, Any]:
            door = h.door(ident)
            lines, count = door.output(since)
            return {**door.state(), "output": lines, "count": count}

        return call(read)

    @router.post("/api/harbour/doors/{ident}/say")
    def api_door_say(ident: str, body: dict[str, Any]) -> JSONResponse:
        def say() -> dict[str, Any]:
            h.door(ident).say(str(body.get("text") or ""))
            return h.door(ident).state()

        return call(say)

    @router.post("/api/harbour/doors/{ident}/stop")
    def api_door_stop(ident: str) -> JSONResponse:
        return call(h.stop_door, ident)

    @router.get("/api/harbour/scenario")
    def api_scenario(path: str) -> JSONResponse:
        return call(h.read_scenario, path)

    @router.post("/api/harbour/scenario/prove")
    def api_scenario_prove(body: dict[str, Any]) -> JSONResponse:
        def prove() -> dict[str, Any]:
            fields = h.with_blocks(body.get("fields") or {}, body.get("blocks"))
            return h.prove(fields, str(body.get("source") or ""))

        return call(prove)

    @router.post("/api/harbour/scenario")
    def api_scenario_save(body: dict[str, Any]) -> JSONResponse:
        def save() -> dict[str, Any]:
            return h.save_scenario(
                h.with_blocks(body.get("fields") or {}, body.get("blocks")),
                str(body.get("name") or ""),
                str(body.get("source") or ""),
                str(body.get("book") or ""),
                bool(body.get("overwrite")),
            )

        return call(save)

    @router.get("/api/harbour/chart")
    def api_chart(region: str = "channel-west") -> JSONResponse:
        return call(h.chart, region)

    return router
