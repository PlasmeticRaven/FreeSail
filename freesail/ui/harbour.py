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
                                           settings' place, the credential store's state
    GET  /api/harbour/catalogue            the scenarios, ships, seats, stations, briefs,
                                           books, ports, regions and nations
    POST /api/harbour/start                {scenario | ship | load, seed, seat, time, pace,
                                           crewed_cap, crewed_range, business,
                                           director_brief, standing_orders} -> the game
    GET  /api/harbour/settings             the settings and where they are kept
    POST /api/harbour/settings             {settings} -> kept (no key, truth 7b-110)
    POST /api/harbour/desktop              {stations: [...], ship?, write?} -> the entries
                                           and the client's file as it would be; written
                                           only with write: true
    POST /api/harbour/shortcut             {write?} -> the shortcut's path and text
    POST /api/harbour/doors                {door: api|local, station, ship?} -> started
    GET  /api/harbour/doors/{id}           ?since=N: its output from line N
    POST /api/harbour/doors/{id}/say       {text}: a line to its terminal (the owner's
                                           word in a consent conversation)
    POST /api/harbour/doors/{id}/stop      stopped, its station released
    GET  /api/harbour/scenario             ?path=: a scenario's text and fields
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
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

import yaml
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from freesail import settings as settings_mod
from freesail.settings import SettingsError

ROOT = Path(__file__).resolve().parents[2]
CLIENT_DIR = ROOT / "client"
GAME_SCENARIOS = ROOT / "data" / "scenarios"
GAME_BOOKS = ROOT / "data" / "standing_orders"
SHIPS_DIR = ROOT / "data" / "ships"

# The player's seats at the start (the server's `--seat`): '' as the scenario says; the
# captain at the prompt; the stations below and above (`agents.seat.SEAT_STATIONS`).
SEATS = ("", "captain", "officer", "master", "lookout", "passenger", "director")
# The stations a door asks for (the doors' `--station`).
STATIONS = ("captain", "officer", "master", "lookout", "director", "watcher", "passenger")
DOOR_KINDS = ("api", "local")
DOOR_LINES_KEPT = 4000
STOP_WAIT_S = 6.0
COAST_STEP_DEG = 0.01  # the harbour's chart keeps a point about every half mile


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
        self.doors: dict[str, Door] = {}
        self._ids = itertools.count(1)
        self.game: dict[str, Any] = {}  # what the harbour started, in words
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
            "ships": [_rel(p) for p in sorted(SHIPS_DIR.glob("*.yaml"))],
            "seats": list(SEATS),
            "stations": list(STATIONS),
            "holders": list(STATION_HOLDERS),
            "doors": list(DOOR_KINDS),
            "paces": list(settings_mod.PACES),
            "briefs": briefs,
            "books": books,
            "descriptions": list(DESCRIPTIONS),
            "nations": list(load_nations().nations),
            "regions": self.regions(),
            "ports": self.ports(),
            "scenarios_place": str(own),
        }

    _names: dict[str, tuple[float, str]] = {}

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
            with contextlib.suppress(OSError, yaml.YAMLError, AttributeError):
                doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                name = str(doc.get("name") or path.stem)
            Harbour._names[key] = (mtime, name)
            cached = Harbour._names[key]
        return {"path": _rel(path) if not own else str(path), "name": cached[1], "own": own}

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
        args.scenario = scenario or None
        args.ship = ship or None
        args.load = load or None

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
        args.director_brief = str(choices.get("director_brief") or "").strip() or None
        args.standing_orders = str(choices.get("standing_orders") or "").strip() or None
        args.ease_on_station = bool(choices.get("ease_on_station"))
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
        with self._lock:
            self.driver.replace_world(
                world, compression=args.time, pace=rule, ease_on_station=args.ease_on_station
            )
            self.started = True
            self.game = {
                "scenario": scenario,
                "ship": ship,
                "load": load,
                "seat": args.seat or "",
                "pace": pace,
                "director_brief": args.director_brief or "",
                "lines": lines,
            }
        return {"lines": lines, "game": self.game_state()}

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
            }
        return out

    def stations(self) -> list[dict[str, Any]]:
        """The stations held and by whom: the agent API's (a model's, through a door) and
        the player's seat."""
        d = self.driver
        out: list[dict[str, Any]] = []
        with d.lock:
            if d.desk is not None:
                for st in d.desk.stations():
                    out.append(
                        {
                            "station": st.get("station"),
                            "ship": st.get("ship", ""),
                            "holder": st.get("model_name") or "",
                            "door": st.get("door") or "",
                            "line": st.get("line") or "",
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

    def door_argv(self, kind: str, station: str, ship: str = "", seat_model: str = "") -> list[str]:
        """A door's command line from the settings: the module's own flags, nothing more.
        `seat_model` is a director's seat's model (package 67): one of the models the
        settings can call, with its dialect, and the seated door's fold where the settings
        name one (`--budget-tokens`)."""
        s, error = self.settings_or_defaults()
        if error:
            raise HarbourError(error)
        doors = s.get("doors") or {}
        station = " ".join(str(station).lower().split())
        if not station:
            raise HarbourError("Name the station the door asks for.")
        if kind == "api":
            d = doors.get("api") or {}
            if seat_model:
                known = settings_mod.callable_models(s)
                if seat_model not in known:
                    raise HarbourError(
                        "The settings call no model by that name (the API door's model and "
                        "the models beside it, doors.api.models)."
                    )
                model, dialect = seat_model, known[seat_model]
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
    ) -> dict[str, Any]:
        """A door started as the server's subprocess: the owner's from the page, or a
        director's seat's (package 67: `seat` its key, `seat_model` its model, `by` "the
        director"), shown in the doors tab beside the owner's and marked so."""
        argv = self.door_argv(kind, station, ship, seat_model=seat_model)
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
                threading.Thread(target=door.stop, daemon=True).start()

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
        from freesail.agents.remote import DeskError, seat_key

        seat = desk.seats.get(seat_key(door.station, door.ship))
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
        }

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
        original, _ = self._original(source)
        try:
            text = scenario_text(fields, original)
        except ScenarioError as e:
            raise HarbourError(f"The scenario was not written: {e}") from None
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "scenario.yaml"
            p.write_text(text, encoding="utf-8")
            try:
                sf = load_scenario(p)
                world = make_scenario_world(sf)
                begin(world, sf)
            except (ScenarioError, OSError, ValueError, KeyError) as e:
                raise HarbourError(_scenario_words(str(e), p)) from None
            refused = [e for e in world.log if e.kind == "order.rejected"]
            if refused:
                raise HarbourError(
                    "A first order or standing order was refused: "
                    + "; ".join(e.text for e in refused[:3])
                )
            seat = sf.player_seat
            if seat:
                from freesail.agents.seat import seat_station

                try:
                    seat_station(world, seat)
                except Exception as e:  # noqa: BLE001  (OrderError, in words)
                    raise HarbourError(f"stations: {e}") from None
            lines = [ln.replace(str(p), "this scenario") for ln in sf.lines() + guard_lines(world)]
        return {"text": text, "lines": lines}

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

    @router.get("/harbour")
    def harbour_page() -> FileResponse:
        return FileResponse(h.client_dir / "harbour.html", media_type="text/html")

    @router.get("/api/harbour/state")
    def api_state() -> JSONResponse:
        return call(h.state)

    @router.get("/api/harbour/catalogue")
    def api_catalogue() -> JSONResponse:
        return call(h.catalogue)

    @router.post("/api/harbour/start")
    def api_start(body: dict[str, Any]) -> JSONResponse:
        return call(h.start, body)

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
        return call(h.prove, body.get("fields") or {}, str(body.get("source") or ""))

    @router.post("/api/harbour/scenario")
    def api_scenario_save(body: dict[str, Any]) -> JSONResponse:
        return call(
            h.save_scenario,
            body.get("fields") or {},
            str(body.get("name") or ""),
            str(body.get("source") or ""),
            str(body.get("book") or ""),
            bool(body.get("overwrite")),
        )

    @router.get("/api/harbour/chart")
    def api_chart(region: str = "channel-west") -> JSONResponse:
        return call(h.chart, region)

    return router
