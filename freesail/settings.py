"""The player's settings (package 59; spec M7b §21d): a file in his own place, outside the
repository, which the harbour (`py -m freesail`, `freesail/ui/harbour.py`) reads and
writes with a form.

    Windows   %APPDATA%\\FreeSail\\settings.yaml
    macOS     ~/Library/Application Support/FreeSail/settings.yaml
    elsewhere $XDG_CONFIG_HOME/freesail/settings.yaml (~/.config/freesail/settings.yaml)

`FREESAIL_SETTINGS` names another file (the tests', a second profile). The file holds the
model names the player uses at each door (a model's name may live here and nowhere in the
repository, a save or a log: truth 7b-110), the local runner's endpoint and its flags, the
API door's, the default seat, compression, pace and crewed budget, and where the saves, the
player's scenarios and the consent records go. **The key is never in it**: the API door
reads its key from the platform's credential store (`freesail.agents.api`, package 42;
`py -m freesail.agents.api --store-key` puts it there), and this module refuses a settings
file that holds a field named for a key or a value that is one (`SettingsError`). A flag
given on a command line wins over the file for that run.

The Windows pieces are small and tested by path (`tests/test_settings.py`): the settings'
place, the desktop client's configuration file (`desktop_config_path`, where the harbour
writes the MCP bridge's entries, one per station: `freesail-captain`, `freesail-director`,
...) and a shortcut that starts the harbour (`shortcut_path`, `shortcut_text`).
"""

from __future__ import annotations

import copy
import json
import os
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SETTINGS_ENV = "FREESAIL_SETTINGS"
SETTINGS_NAME = "settings.yaml"

# The doors the harbour knows (docs/agents/Harness.md): the desktop client's MCP bridge,
# the API door and the local runner.
DOORS = ("desktop", "api", "local")
PACES = ("rule", "lockstep", "free")

DEFAULTS: dict[str, Any] = {
    "server": {"host": "127.0.0.1", "port": 8000, "open_browser": True},
    "game": {
        "seat": "",  # '' the captain at the prompt; officer, master, lookout, director, ...
        "compression": 1.0,
        "pace": "rule",  # the pace rule; lockstep; free (free-running)
        "crewed": {"cap": None, "range_nm": None},  # None: the build machine's
    },
    "places": {
        "saves": "",  # '' the settings' own place, saves/
        "scenarios": "",  # '' the settings' own place, scenarios/
        "consent_records": "",  # '' the game's own (docs/agents/consent)
        "desktop_config": "",  # '' the platform's place for the desktop client's file
    },
    "doors": {
        "desktop": {"model_name": "", "command": "", "wait": None},
        "api": {"model": "", "dialect": "anthropic", "effort": "", "flags": []},
        "local": {"endpoint": "http://127.0.0.1:8080", "model": "", "flags": []},
    },
}

HEAD = """\
# FreeSail's settings (package 59), kept by the harbour (py -m freesail) and yours to edit.
# A flag given on a command line wins over this file for that run. No key is kept here:
# the API door reads its key from the credential store (py -m freesail.agents.api
# --store-key), and the game refuses a settings file that holds one. The model names
# below live here and nowhere in the repository, a save or a log.
"""

# A field named so is a key's, never a setting's.
KEY_FIELDS = ("key", "api_key", "apikey", "token", "secret", "password", "credential")
_KEYISH = re.compile(r"^(sk-|sk_|rk-|key-|AKIA)[A-Za-z0-9_\-]{12,}$")
_LONG_TOKEN = re.compile(r"^[A-Za-z0-9_\-]{40,}$")


class SettingsError(ValueError):
    """Settings that cannot be read or kept, in words."""


# ---------------------------------------------------------------------------
# Places
# ---------------------------------------------------------------------------


def _windows(platform: str) -> bool:
    return platform.startswith("win")


def _mac(platform: str) -> bool:
    return platform == "darwin"


def config_home(
    platform: str = sys.platform, environ: Mapping[str, str] | None = None, home: Path | None = None
) -> Path:
    """The folder the platform keeps an application's settings in: `%APPDATA%` on Windows,
    `~/Library/Application Support` on macOS, the XDG config place elsewhere."""
    environ = os.environ if environ is None else environ
    home = Path.home() if home is None else home
    if _windows(platform):
        appdata = environ.get("APPDATA")
        return Path(appdata) if appdata else home / "AppData" / "Roaming"
    if _mac(platform):
        return home / "Library" / "Application Support"
    xdg = environ.get("XDG_CONFIG_HOME")
    return Path(xdg) if xdg else home / ".config"


def settings_dir(
    platform: str = sys.platform, environ: Mapping[str, str] | None = None, home: Path | None = None
) -> Path:
    """FreeSail's own folder in the player's place (`%APPDATA%\\FreeSail` on Windows)."""
    name = "freesail" if not (_windows(platform) or _mac(platform)) else "FreeSail"
    return config_home(platform, environ, home) / name


def settings_path(
    platform: str = sys.platform, environ: Mapping[str, str] | None = None, home: Path | None = None
) -> Path:
    """The settings file: `FREESAIL_SETTINGS` when it is set, else `settings.yaml` in
    FreeSail's folder of the player's place."""
    environ = os.environ if environ is None else environ
    named = environ.get(SETTINGS_ENV)
    if named:
        return Path(named).expanduser()
    return settings_dir(platform, environ, home) / SETTINGS_NAME


def desktop_config_path(
    platform: str = sys.platform, environ: Mapping[str, str] | None = None, home: Path | None = None
) -> Path:
    """The desktop client's configuration file, where its MCP servers are listed
    (docs/agents/Harness.md, section 3): `%APPDATA%\\Claude\\claude_desktop_config.json`
    on Windows, the same name under the platform's place elsewhere."""
    return config_home(platform, environ, home) / "Claude" / "claude_desktop_config.json"


def python_command(platform: str = sys.platform) -> str:
    """The command that starts Python in an entry another program runs: the launcher `py`
    on Windows, `python3` elsewhere."""
    return "py" if _windows(platform) else "python3"


def shortcut_path(
    platform: str = sys.platform, environ: Mapping[str, str] | None = None, home: Path | None = None
) -> Path:
    """Where the harbour's shortcut goes: a command file on the desktop on Windows
    (`%USERPROFILE%\\Desktop\\FreeSail.cmd`) and macOS (`FreeSail.command`), a desktop
    entry among the applications elsewhere."""
    environ = os.environ if environ is None else environ
    home = Path.home() if home is None else home
    if _windows(platform):
        profile = environ.get("USERPROFILE")
        return (Path(profile) if profile else home) / "Desktop" / "FreeSail.cmd"
    if _mac(platform):
        return home / "Desktop" / "FreeSail.command"
    data = environ.get("XDG_DATA_HOME")
    return (Path(data) if data else home / ".local" / "share") / "applications" / "freesail.desktop"


def shortcut_text(platform: str = sys.platform, root: Path = ROOT) -> str:
    """The shortcut's text: go to the game's folder and start the harbour."""
    if _windows(platform):
        return f'@echo off\r\ncd /d "{root}"\r\npy -m freesail\r\n'
    if _mac(platform):
        return f'#!/bin/sh\ncd "{root}" && exec python3 -m freesail\n'
    return (
        "[Desktop Entry]\nType=Application\nName=FreeSail\n"
        "Comment=The harbour: start a game, make a scenario, open the doors\n"
        f"Exec=sh -c 'cd \"{root}\" && exec python3 -m freesail'\nTerminal=true\n"
    )


def inside_repository(path: str | Path, root: Path = ROOT) -> bool:
    try:
        Path(path).expanduser().resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------


def _merge(base: dict[str, Any], over: Mapping[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, Mapping) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _walk(value: Any, where: str = "") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(value, Mapping):
        for k, v in value.items():
            out += [(f"{where}.{k}" if where else str(k), None)]
            out += _walk(v, f"{where}.{k}" if where else str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            out += _walk(v, f"{where}[{i}]")
    else:
        out.append((where, value))
    return out


def looks_like_a_key(value: Any) -> bool:
    """Whether a value has a credential's shape: a provider's prefix (sk-, ...) or a long
    unbroken token of the kind keys are and a model's name is not."""
    if not isinstance(value, str):
        return False
    v = value.strip()
    if " " in v or "/" in v or "." in v:
        return False
    if _KEYISH.match(v):
        return True
    return (
        bool(_LONG_TOKEN.match(v)) and any(c.isdigit() for c in v) and any(c.isupper() for c in v)
    )


def stored_keys() -> list[str]:
    """The keys the credential store holds for the doors (read only to refuse a settings
    file that holds one, never shown or sent); none where the store cannot be read."""
    try:
        from freesail.agents.api import KEYRING_ACCOUNT, KEYRING_SERVICE, OPENROUTER_ACCOUNT
    except ImportError:  # the agents' extra not installed
        return []
    try:
        import keyring
    except ImportError:
        return []
    out = []
    for account in (KEYRING_ACCOUNT, OPENROUTER_ACCOUNT):
        try:
            key = keyring.get_password(KEYRING_SERVICE, account)
        except Exception:  # noqa: BLE001  (a store that is locked, absent or refuses)
            key = None
        if key and key.strip():
            out.append(key.strip())
    return out


def credential_words() -> list[str]:
    """Whether the credential store holds the doors' keys, in words, never the key."""
    try:
        from freesail.agents.api import KEYRING_ACCOUNT, KEYRING_SERVICE, OPENROUTER_ACCOUNT
    except ImportError:
        return ['The agents\' extra is not installed (py -m pip install -e ".[agents]").']
    try:
        import keyring
    except ImportError:
        return [
            "The keyring package is not installed; the API door reads its key from the "
            "environment instead (docs/agents/Harness.md)."
        ]
    out = []
    for account in (KEYRING_ACCOUNT, OPENROUTER_ACCOUNT):
        try:
            held = bool((keyring.get_password(KEYRING_SERVICE, account) or "").strip())
        except Exception as e:  # noqa: BLE001
            out.append(
                f"The credential store could not be read for {account} ({type(e).__name__})."
            )
            continue
        out.append(
            f"A key for {account} is in the credential store (service {KEYRING_SERVICE})."
            if held
            else f"No key for {account} is in the credential store; put it there once with "
            f"py -m freesail.agents.api --store-key"
            + (" --dialect openrouter." if account == OPENROUTER_ACCOUNT else ".")
        )
    return out


def check_settings(data: Mapping[str, Any], keys: list[str] | None = None) -> dict[str, Any]:
    """The settings as kept: the defaults under what was given, every field checked. A
    field named for a key, a value with a key's shape, or a value holding a key the
    credential store has (`keys`), is refused in words (truth 7b-110); so is an unknown
    pace or door, a compression that is no number, or a place inside the repository for
    the player's scenarios or the settings' own folders."""
    if not isinstance(data, Mapping):
        raise SettingsError("The settings are a mapping of server, game, places and doors.")
    for where, value in _walk(data):
        leaf = re.split(r"[.\[]", where)[-1].rstrip("]").lower()
        if leaf in KEY_FIELDS:
            raise SettingsError(
                f"The settings hold no key ('{where}'): the key stays in the credential store "
                "(py -m freesail.agents.api --store-key)."
            )
        if looks_like_a_key(value):
            raise SettingsError(
                f"'{where}' has the shape of a key, and the settings hold no key: it stays in "
                "the credential store (py -m freesail.agents.api --store-key)."
            )
        if isinstance(value, str) and any(k and k in value for k in (keys or [])):
            raise SettingsError(
                f"'{where}' holds the key the credential store has; the settings hold no key."
            )
    unknown = [k for k in data if k not in DEFAULTS]
    if unknown:
        raise SettingsError(
            f"The settings have no section {', '.join(map(str, unknown))}; they are "
            f"{', '.join(DEFAULTS)}."
        )
    out = _merge(DEFAULTS, data)
    game = out["game"]
    if game.get("pace") not in PACES:
        raise SettingsError(f"The pace is one of {', '.join(PACES)}, not '{game.get('pace')}'.")
    try:
        game["compression"] = float(game.get("compression") or 1.0)
        port = int(out["server"].get("port") or 8000)
    except (TypeError, ValueError):
        raise SettingsError("The compression and the port are numbers.") from None
    out["server"]["port"] = port
    game["seat"] = " ".join(str(game.get("seat") or "").split())
    crewed = game.get("crewed") or {}
    try:
        game["crewed"] = {
            "cap": None if crewed.get("cap") in (None, "") else int(crewed["cap"]),
            "range_nm": None if crewed.get("range_nm") in (None, "") else float(crewed["range_nm"]),
        }
    except (TypeError, ValueError):
        raise SettingsError("The crewed budget's cap and range are numbers.") from None
    for door in out["doors"]:
        if door not in DOORS:
            raise SettingsError(f"There is no door '{door}'; the doors: {', '.join(DOORS)}.")
        flags = out["doors"][door].get("flags", [])
        if isinstance(flags, str):
            flags = flags.split()
        if not isinstance(flags, list):
            raise SettingsError(f"The {door} door's flags are a list of words.")
        if "flags" in out["doors"][door]:
            out["doors"][door]["flags"] = [str(f) for f in flags]
    for name in ("saves", "scenarios"):
        place = str(out["places"].get(name) or "")
        if place and inside_repository(place):
            raise SettingsError(
                f"The {name} place {place} is inside the game's folder; name one outside it, "
                "where the repository never holds what you make."
            )
    return out


def load_settings(path: str | Path | None = None) -> dict[str, Any]:
    """The settings at `path` (`settings_path()` by default), the defaults where the file
    is silent or absent. `SettingsError` in words for a file that cannot be read or kept."""
    p = Path(path) if path is not None else settings_path()
    if not p.exists():
        return copy.deepcopy(DEFAULTS)
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as e:
        raise SettingsError(f"The settings file {p} could not be read ({e}).") from None
    return check_settings(data)


def save_settings(data: Mapping[str, Any], path: str | Path | None = None) -> Path:
    """Write the settings (checked first, the credential store's keys among what is
    refused), outside the repository only, with the file's head saying what it holds."""
    p = Path(path) if path is not None else settings_path()
    if inside_repository(p):
        raise SettingsError(
            f"The settings file {p} would be inside the game's folder; the settings live in "
            "the player's own place, outside the repository."
        )
    kept = check_settings(data, keys=stored_keys())
    p.parent.mkdir(parents=True, exist_ok=True)
    body = yaml.safe_dump(kept, sort_keys=False, allow_unicode=True, default_flow_style=False)
    p.write_text(HEAD + body, encoding="utf-8")
    return p


def place(settings: Mapping[str, Any], name: str, path: Path | None = None) -> Path:
    """A place the settings name (`saves`, `scenarios`), else its folder beside the
    settings file."""
    given = str((settings.get("places") or {}).get(name) or "")
    if given:
        return Path(given).expanduser()
    return (Path(path) if path is not None else settings_path()).parent / name


# ---------------------------------------------------------------------------
# The desktop client's entries (package 59, item 3)
# ---------------------------------------------------------------------------

ENTRY_PREFIX = "freesail-"
MODEL_NAME_PLACEHOLDER = "SET THE MODEL'S EXACT NAME HERE"


def entry_name(station: str, ship: str = "") -> str:
    """The desktop client's name for a station's bridge: `freesail-captain`, and on another
    ship `freesail-captain-<her>`."""
    words = [station] + ([ship] if ship else [])
    slug = "-".join(re.sub(r"[^a-z0-9]+", "-", w.lower()).strip("-") for w in words)
    return ENTRY_PREFIX + slug


def desktop_entry(
    station: str,
    settings: Mapping[str, Any],
    game: str,
    *,
    ship: str = "",
    platform: str = sys.platform,
    root: Path = ROOT,
) -> dict[str, Any]:
    """The MCP bridge's entry for one station, in `.mcp.json`'s form: the command (`py` on
    Windows, `python3` elsewhere, or the settings' own), the game's address, the station,
    the model's name from the settings, and the game's folder on `PYTHONPATH`."""
    door = (settings.get("doors") or {}).get("desktop") or {}
    args = ["-m", "freesail.agents.mcp_server", "--game", game, "--station", station]
    if ship:
        args += ["--ship", ship]
    args += ["--model-name", str(door.get("model_name") or MODEL_NAME_PLACEHOLDER)]
    if door.get("wait"):
        args += ["--wait", f"{float(door['wait']):g}"]
    return {
        "command": str(door.get("command") or python_command(platform)),
        "args": args,
        "env": {"PYTHONPATH": str(root), "PYTHONUTF8": "1"},
    }


def merged_desktop_config(
    existing: str | None, entries: Mapping[str, dict[str, Any]]
) -> dict[str, Any]:
    """The desktop client's configuration with these entries put in: every other server and
    setting the file holds kept as it was, an entry of the same name replaced."""
    try:
        doc = json.loads(existing) if existing and existing.strip() else {}
    except json.JSONDecodeError as e:
        raise SettingsError(
            f"The desktop client's configuration is not JSON ({e.msg} at line {e.lineno}); "
            "mend it or move it aside, and write the entries again."
        ) from None
    if not isinstance(doc, dict):
        raise SettingsError("The desktop client's configuration is not a JSON object.")
    servers = doc.get("mcpServers")
    if servers is None:
        servers = {}
    if not isinstance(servers, dict):
        raise SettingsError("The desktop client's configuration's mcpServers is not an object.")
    doc["mcpServers"] = {**servers, **{k: dict(v) for k, v in entries.items()}}
    return doc


def write_desktop_config(path: str | Path, entries: Mapping[str, dict[str, Any]]) -> Path | None:
    """Put the entries in the desktop client's configuration file, keeping the file as it
    was beside it (`.bak`) first. Returns the copy's path, or None for a new file. Refused
    inside the repository (an entry holds a model's name)."""
    p = Path(path)
    if inside_repository(p):
        raise SettingsError(f"{p} is inside the game's folder; the client's file is not.")
    existing = p.read_text(encoding="utf-8") if p.exists() else None
    doc = merged_desktop_config(existing, entries)
    backup = None
    if existing is not None:
        backup = p.with_name(p.name + ".bak")
        backup.write_text(existing, encoding="utf-8")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return backup
