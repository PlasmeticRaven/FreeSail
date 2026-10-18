"""The player's settings (package 59; spec M7b §21d; `freesail/settings.py`): the file's
place by platform, the Windows pieces tested by path (the settings' folder under
%APPDATA%, the desktop client's configuration file, the shortcut), the defaults, the
refusal of a key in any shape (truth 7b-110's first half), and the desktop client's
entries, one per station, put into its file with every other server kept.

The model names here are placeholders; the credential store is the tests' own.
"""

from __future__ import annotations

import json
from pathlib import Path, PureWindowsPath

import pytest

from freesail import settings as S

ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "placeholder-model-name"  # no model is named here


# ---------------------------------------------------------------------------
# The places, by platform
# ---------------------------------------------------------------------------


def test_the_settings_live_in_appdata_on_windows_and_the_xdg_place_elsewhere():
    win = {"APPDATA": r"C:\Users\Owner\AppData\Roaming", "USERPROFILE": r"C:\Users\Owner"}
    home = Path("/home/owner")
    p = S.settings_path("win32", win, home)
    assert PureWindowsPath(str(p)).parts[-3:] == ("Roaming", "FreeSail", "settings.yaml")
    assert str(p).startswith(r"C:\Users\Owner\AppData\Roaming")
    # no APPDATA: the profile's own Roaming folder
    assert S.settings_path("win32", {}, home) == (
        home / "AppData" / "Roaming" / "FreeSail" / "settings.yaml"
    )
    assert S.settings_path("linux", {}, home) == home / ".config" / "freesail" / "settings.yaml"
    assert S.settings_path("linux", {"XDG_CONFIG_HOME": "/x"}, home) == Path(
        "/x/freesail/settings.yaml"
    )
    assert S.settings_path("darwin", {}, home) == (
        home / "Library" / "Application Support" / "FreeSail" / "settings.yaml"
    )
    # FREESAIL_SETTINGS names another file outright
    assert S.settings_path("win32", {**win, S.SETTINGS_ENV: "/elsewhere/s.yaml"}) == Path(
        "/elsewhere/s.yaml"
    )


def test_the_desktop_clients_file_and_the_python_command_by_platform():
    win = {"APPDATA": r"C:\Users\Owner\AppData\Roaming"}
    p = S.desktop_config_path("win32", win, Path("/h"))
    assert str(p).startswith(r"C:\Users\Owner\AppData\Roaming")
    assert PureWindowsPath(str(p)).parts[-2:] == ("Claude", "claude_desktop_config.json")
    assert S.desktop_config_path("darwin", {}, Path("/h")) == Path(
        "/h/Library/Application Support/Claude/claude_desktop_config.json"
    )
    assert S.desktop_config_path("linux", {}, Path("/h")) == Path(
        "/h/.config/Claude/claude_desktop_config.json"
    )
    assert S.python_command("win32") == "py" and S.python_command("linux") == "python3"


def test_the_shortcut_goes_to_the_game_folder_and_starts_the_harbour():
    win = {"USERPROFILE": r"C:\Users\Owner"}
    p = S.shortcut_path("win32", win, Path("/h"))
    assert str(p).startswith(r"C:\Users\Owner")
    assert PureWindowsPath(str(p)).parts[-2:] == ("Desktop", "FreeSail.cmd")
    text = S.shortcut_text("win32", Path(r"D:\Projects\FreeSail"))
    assert text == '@echo off\r\ncd /d "D:\\Projects\\FreeSail"\r\npy -m freesail\r\n'
    assert S.shortcut_path("linux", {}, Path("/h")) == Path(
        "/h/.local/share/applications/freesail.desktop"
    )
    assert "python3 -m freesail" in S.shortcut_text("linux", Path("/g"))
    assert S.shortcut_path("darwin", {}, Path("/h")) == Path("/h/Desktop/FreeSail.command")


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------


def test_no_file_gives_the_defaults_and_a_kept_file_reads_back(tmp_path):
    path = tmp_path / "s" / "settings.yaml"
    assert S.load_settings(path) == S.DEFAULTS
    s = S.load_settings(path)
    s["game"]["seat"] = "officer"
    s["game"]["pace"] = "lockstep"
    s["doors"]["api"]["model"] = PLACEHOLDER
    s["doors"]["local"]["flags"] = "--ctx 32768"  # words are split into the flags
    S.save_settings(s, path)
    back = S.load_settings(path)
    assert back["game"]["seat"] == "officer" and back["game"]["pace"] == "lockstep"
    assert back["doors"]["local"]["flags"] == ["--ctx", "32768"]
    assert back["doors"]["api"]["model"] == PLACEHOLDER
    text = path.read_text(encoding="utf-8")
    assert text.startswith("# FreeSail's settings") and "No key is kept here" in text
    # the places beside the file unless named
    assert S.place(back, "scenarios", path) == path.parent / "scenarios"


@pytest.mark.parametrize(
    "field,value",
    [
        (("doors", "api", "key"), "anything"),
        (("doors", "api", "api_key"), "anything"),
        (("doors", "local", "token"), "x"),
        # put together here, so that no file of the repository holds a key's shape
        (("doors", "api", "model"), "sk" + "-ant-abcdefghijklmnopqrstuvwxyz0123"),
        (("doors", "api", "flags"), ["--key-file", "sk" + "-or-v1-0123456789abcdefABCDEF"]),
        (("doors", "desktop", "model_name"), "Ab3" * 20),
    ],
)
def test_a_key_in_any_shape_is_refused_and_nothing_is_written(tmp_path, field, value):
    path = tmp_path / "settings.yaml"
    s = S.load_settings(path)
    node = s
    for k in field[:-1]:
        node = node[k]
    node[field[-1]] = value
    with pytest.raises(S.SettingsError, match="key"):
        S.save_settings(s, path)
    assert not path.exists()


def test_the_key_the_credential_store_holds_is_refused_anywhere_in_the_file(tmp_path, monkeypatch):
    from messages_api import fake_store

    from freesail.agents.api import KEYRING_ACCOUNT, KEYRING_SERVICE

    store = fake_store(monkeypatch)
    key = "plain-words-key"  # not of a key's shape: found by the store's own copy
    store.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, key)
    s = S.load_settings(tmp_path / "x.yaml")
    s["doors"]["api"]["effort"] = key
    with pytest.raises(S.SettingsError, match="credential store has"):
        S.save_settings(s, tmp_path / "x.yaml")
    words = S.credential_words()
    assert any("is in the credential store" in w for w in words)
    assert not any(key in w for w in words)


def test_the_settings_and_the_players_places_are_never_inside_the_repository(tmp_path):
    with pytest.raises(S.SettingsError, match="outside the repository"):
        S.save_settings(S.DEFAULTS, ROOT / "settings.yaml")
    s = S.load_settings(tmp_path / "s.yaml")
    s["places"]["scenarios"] = str(ROOT / "data" / "scenarios")
    with pytest.raises(S.SettingsError, match="inside the game's folder"):
        S.save_settings(s, tmp_path / "s.yaml")
    with pytest.raises(S.SettingsError, match="pace"):
        S.check_settings({"game": {"pace": "fast"}})
    with pytest.raises(S.SettingsError, match="no section"):
        S.check_settings({"keys": {}})


# ---------------------------------------------------------------------------
# The desktop client's entries
# ---------------------------------------------------------------------------


def test_one_entry_per_station_in_the_mcp_json_form():
    s = S.load_settings(Path("/nonexistent/settings.yaml"))
    assert S.entry_name("captain") == "freesail-captain"
    assert S.entry_name("officer of the watch") == "freesail-officer-of-the-watch"
    assert S.entry_name("captain", "Palinure") == "freesail-captain-palinure"
    e = S.desktop_entry("director", s, "http://localhost:8000", platform="win32", root=ROOT)
    assert e["command"] == "py"
    assert e["args"][:2] == ["-m", "freesail.agents.mcp_server"]
    assert e["args"][e["args"].index("--station") + 1] == "director"
    assert e["args"][e["args"].index("--game") + 1] == "http://localhost:8000"
    assert e["args"][e["args"].index("--model-name") + 1] == S.MODEL_NAME_PLACEHOLDER
    assert e["env"] == {"PYTHONPATH": str(ROOT), "PYTHONUTF8": "1"}
    # the repository's own .mcp.json is of the same form
    mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))["mcpServers"]["freesail"]
    assert set(mcp) <= set(e) and mcp["args"][:2] == e["args"][:2]
    s["doors"]["desktop"]["model_name"] = PLACEHOLDER
    e = S.desktop_entry("captain", s, "http://localhost:8001", ship="Palinure", platform="linux")
    assert e["command"] == "python3"
    assert e["args"][e["args"].index("--ship") + 1] == "Palinure"
    assert e["args"][-1] == PLACEHOLDER


def test_the_entries_go_into_the_clients_file_beside_its_other_servers(tmp_path):
    path = tmp_path / "Claude" / "claude_desktop_config.json"
    s = S.load_settings(tmp_path / "none.yaml")
    entries = {
        S.entry_name(st): S.desktop_entry(st, s, "http://localhost:8000")
        for st in ("captain", "director")
    }
    assert S.write_desktop_config(path, entries) is None  # a new file: no copy kept
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(doc["mcpServers"]) == ["freesail-captain", "freesail-director"]
    other = {
        "mcpServers": {"other": {"command": "x"}, "freesail-captain": {"command": "old"}},
        "theme": "dark",
    }
    path.write_text(json.dumps(other), encoding="utf-8")
    backup = S.write_desktop_config(path, entries)
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert doc["theme"] == "dark" and doc["mcpServers"]["other"] == {"command": "x"}
    assert doc["mcpServers"]["freesail-captain"]["args"][1] == "freesail.agents.mcp_server"
    assert backup is not None and json.loads(backup.read_text(encoding="utf-8")) == other
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(S.SettingsError, match="not JSON"):
        S.write_desktop_config(path, entries)
    with pytest.raises(S.SettingsError, match="inside the game's folder"):
        S.write_desktop_config(ROOT / "claude_desktop_config.json", entries)
