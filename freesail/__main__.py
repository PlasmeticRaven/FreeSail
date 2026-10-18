"""`py -m freesail`: the harbour (package 59; spec M7b §21d).

    py -m freesail [--no-browser] [--settings FILE] [the server's flags]

Starts the game's server (`freesail.ui.server`) and opens the browser on the harbour,
`http://localhost:8000/harbour`: the page that lists the scenarios, the ships, the seats and
the doors, starts a game with the choices made, writes the desktop client's entries, starts
the API door and the local runner, holds the settings and carries the scenario maker
(`freesail/ui/harbour.py`). With no scenario, ship or save on the command line no game is in
play until the harbour starts one (the game's page leads to the harbour meanwhile); with
one, that game is started at once as the server would start it, and the harbour is beside it.

The settings (`freesail/settings.py`: `%APPDATA%\\FreeSail\\settings.yaml` on Windows) give
the defaults of the host and port, the compression, the seat, the pace, the crewed budget
and the places of the saves and the consent records; a flag on this command line wins over
them for the run. The clock is held at the start, as at every driver: `go` (the game page's
button, or the order line) runs it.
"""

from __future__ import annotations

import copy
import os
import sys
import threading
import webbrowser
from pathlib import Path

from freesail import settings as settings_mod

ROOT = Path(__file__).resolve().parents[1]

# The flags whose values are paths, made absolute before the server goes to the game's
# folder (where every scenario names its files from).
PATH_FLAGS = ("ship", "scenario", "load", "standing_orders", "consent_records", "saves")


def main(argv: list[str] | None = None) -> int:
    from freesail.ui import server

    ap = server.server_parser("FreeSail: the harbour, the game's launcher (package 59)")
    ap.add_argument("--no-browser", action="store_true", help="do not open the browser")
    ap.add_argument(
        "--settings",
        help=f"the settings file (default {settings_mod.settings_path()}; also "
        f"{settings_mod.SETTINGS_ENV})",
    )
    first, _ = ap.parse_known_args(argv)
    settings_path = Path(first.settings).expanduser() if first.settings else None
    try:
        settings = settings_mod.load_settings(settings_path)
        error = ""
    except settings_mod.SettingsError as e:
        settings, error = copy.deepcopy(settings_mod.DEFAULTS), str(e)
    path = settings_path or settings_mod.settings_path()
    game, places, srv = settings["game"], settings["places"], settings["server"]
    crewed = game.get("crewed") or {}
    ap.set_defaults(
        host=srv.get("host") or "127.0.0.1",
        port=int(srv.get("port") or 8000),
        time=float(game.get("compression") or 1.0),
        seat=game.get("seat") or None,
        lockstep=game.get("pace") == "lockstep",
        free_running=game.get("pace") == "free",
        crewed_cap=crewed.get("cap"),
        crewed_range=crewed.get("range_nm"),
        saves=str(settings_mod.place(settings, "saves", path)),
        consent_records=places.get("consent_records") or None,
    )
    args = ap.parse_args(argv)
    for name in PATH_FLAGS:
        value = getattr(args, name, None)
        if value:
            setattr(args, name, str(Path(value).expanduser().resolve()))
    os.chdir(ROOT)

    import uvicorn

    from freesail.core.world import Scenario, World
    from freesail.ui.console import DEFAULT_SEED
    from freesail.ui.harbour import Harbour

    given = bool(args.scenario or args.ship or args.load)
    if given:
        world = server.prepare_game(args)
    else:
        # no game yet: a World held at its first tick, which the harbour's start replaces
        world = World(
            seed=args.seed if args.seed is not None else DEFAULT_SEED, scenario=Scenario()
        )
    driver = server.Driver(
        world,
        compression=args.time,
        lockstep=args.lockstep,
        ease_on_station=args.ease_on_station,
        free_running=args.free_running,
    )
    url = f"http://localhost:{args.port}"
    harbour = Harbour(
        driver,
        settings_path=settings_path,
        consent_records=args.consent_records,
        saves_dir=args.saves,
        started=given,
        game_url=url,
    )
    app = server.create_app(
        driver,
        game=f"FreeSail's browser game (freesail.ui.server on port {args.port}, from the harbour)",
        consent_records=args.consent_records,
        saves_dir=args.saves,
        say=server.say_to_terminal,
        harbour=harbour,
    )
    host = "localhost" if args.host in ("127.0.0.1", "0.0.0.0") else args.host
    page = f"http://{host}:{args.port}/harbour"
    print(f"FreeSail harbour. Open {page}")
    print(f"The settings: {path}" + (f" (not read: {error})" if error else ""))
    print(
        "The clock is held until the driver says go (the game page's button, or 'go' at "
        "its order line)."
    )
    if not args.no_browser and srv.get("open_browser", True):
        threading.Timer(1.5, webbrowser.open, args=(page,)).start()
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
