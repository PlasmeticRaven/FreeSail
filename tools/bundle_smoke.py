"""The smoke test of a built download (package 130), run in the cloud on Windows and on both
kinds of Mac against the zip itself, by the runner's own Python as the harness (the game
never sees that Python).

    python tools/bundle_smoke.py FreeSail-NAME-windows.zip
    python tools/bundle_smoke.py FreeSail-NAME-mac.zip
    python tools/bundle_smoke.py FreeSail-NAME-mac.zip --without-isolation   # its teeth

It touches nothing of the machine's own people: everything it writes, and the only places
the game is let see as the player's, lie in ONE fresh temporary folder of its own (made by
the system's `mkdtemp`, its name with a space and a letter outside English in it): a home
of its own (HOME, APPDATA, LOCALAPPDATA, USERPROFILE and XDG_CONFIG_HOME are pointed into
it, so the game's settings, saves and consent records, and Python's user site, are there),
the unpacked folder, and the folder the launcher is started from. Nothing outside it is
removed or written, and it is removed at the end.

What it does, in order, as a friend's machine would:

1. Unpacks the zip with the system's own tool, as its own user would: on Windows
   Expand-Archive into a folder named for the zip (what "Extract All" does); on the Mac
   `ditto`, after giving the zip the quarantine mark a browser gives its downloads, so that
   every unpacked file carries it as a friend's do. Either must make ONE folder, the
   launcher at its top.
2. Takes a digest of every file in the unpacked folder.
3. Plants poison where the download must never look, each a module named as one the game
   imports (`freesail`, `yaml`, `numpy`, `fastapi`, `uvicorn`) or one Python runs by itself
   (`sitecustomize`, `usercustomize`, and a `.pth` file), which leaves a mark if run:
   (a) in a folder named by PYTHONPATH, PYTHONHOME and PYTHONSTARTUP, which the launchers
   clear; (b) in the user's site-packages for that system (Windows'
   `%APPDATA%\\Python\\Python311\\site-packages`; the Mac's `~/.local/lib/python3.11/...` and
   `~/Library/Python/3.11/lib/python/...`), which the launchers do NOT clear and the
   download must ignore by `-I`; (c) in the folder the launcher is started from, which
   Python puts first on its path for `-m` unless `-I` (and on Windows the `._pth` file).
4. Starts the game by the launcher's own road (`cmd /c FreeSail.cmd`, `bash
   FreeSail.command`; `--no-browser`, which the launcher passes on), from (c), with the
   runner's Python off the PATH.
5. Waits for the server, and reads that a first start says nothing of its port being taken;
   asks the harbour's page (taking its mark as a browser does), its state and catalogue;
   begins the catalogue's first game (*A first passage*); asks the game's page, its state
   and ship; runs sixty ticks (a minute of the game's time); reads the primer's chapter 7
   from the library; asks the harbour's chart; saves; and begins a second game on the
   Channel's chart (*The tender*), runs a minute of it (its depth tiles read) and asks its
   chart.
6. Reads the running interpreter's path from the system (it must lie in the unpacked
   folder), and looks for the poison's marks (there must be none).
7. Stops the game (Control-C on the Mac, as a player does; on Windows Ctrl+Break, which
   the server takes as Ctrl+C, a runner having no window to press Ctrl+C in), and reads
   the launcher's "FreeSail has stopped (exit code 0)" (on Windows 3, the code Windows
   ends a process with on a break the server has re-raised after its clean shutdown),
   and that the server no longer answers.
8. Checks that no file in the unpacked folder is new, changed or gone; on the Mac that the
   launcher cleared the quarantine of exactly its four folders and that the folder, the
   launcher and the two pages beside it keep theirs; and that the save lies in the
   player's own data folder.

`--without-isolation` proves step 6 has teeth: it takes `-I` out of the unpacked launcher
(and on Windows the interpreter's `python311._pth`), starts it, and passes only if the
poison in (b) and (c) is run. (A Windows registry's Python paths are not poisoned: a
runner's registry is the machine's own, and is not this test's to write.)

Each finding is said as a GitHub annotation (`::notice::`, `::error::`) and in the job's
summary, so that it is read without the log. Exit status 1 if anything failed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from collections.abc import Mapping
from pathlib import Path

WINDOWS = sys.platform.startswith("win")
MAC = sys.platform == "darwin"
SAVE_NAME = "smoke-proof"


class Findings:
    def __init__(self, title: str):
        self.title = title
        self.rows: list[tuple[bool, str, str]] = []

    def ok(self, what: str, detail: str = "") -> None:
        self.rows.append((True, what, detail))
        print(f"  ok   {what}" + (f": {detail}" if detail else ""), flush=True)

    def fail(self, what: str, detail: str = "") -> None:
        self.rows.append((False, what, detail))
        print(f"  FAIL {what}" + (f": {detail}" if detail else ""), flush=True)

    def check(self, cond: bool, what: str, detail: str = "") -> bool:
        (self.ok if cond else self.fail)(what, detail)
        return cond

    @property
    def passed(self) -> bool:
        return all(r[0] for r in self.rows)

    def report(self, window: str) -> None:
        def esc(s: str) -> str:
            return s.replace("%", "%25").replace("\r", "").replace("\n", "%0A")

        good = [f"{w}" + (f": {d}" if d else "") for ok, w, d in self.rows if ok]
        bad = [(w, d) for ok, w, d in self.rows if not ok]
        verdict = "passed" if not bad else f"FAILED ({len(bad)} of {len(self.rows)})"
        print(
            f"::notice title={self.title}: {verdict}::"
            + esc(f"{len(good)} of {len(self.rows)} checks passed:\n" + "\n".join(good))
        )
        for w, d in bad[:9]:
            print(f"::error title={self.title}: {w}::" + esc(d or w))
        if bad:
            tail = "\n".join(window.splitlines()[-40:])
            print(f"::error title={self.title}: the game's window, its last lines::" + esc(tail))
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as f:
                f.write(f"### {self.title}: {verdict}\n\n| | check | detail |\n|---|---|---|\n")
                for ok, w, d in self.rows:
                    d = d.replace("|", "\\|").replace("\n", " ")
                    f.write(f"| {'✅' if ok else '❌'} | {w} | {d} |\n")
                f.write("\n<details><summary>The game's window</summary>\n\n```\n")
                f.write(window[-6000:])
                f.write("\n```\n</details>\n\n")


def digests(top: Path) -> dict[str, str]:
    out = {}
    for p in sorted(top.rglob("*")):
        if p.is_symlink():
            out[p.relative_to(top).as_posix()] = "link:" + os.readlink(p)
        elif p.is_file():
            out[p.relative_to(top).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
        elif p.is_dir():
            out[p.relative_to(top).as_posix() + "/"] = "dir"
    return out


LAUNCHER = "FreeSail.cmd" if WINDOWS else "FreeSail.command"
# The poison's modules: those the game imports, and those Python runs by itself at its start.
POISONED = ("freesail", "yaml", "numpy", "fastapi", "uvicorn", "sitecustomize", "usercustomize")
# What a player's unpacking leaves marked on the Mac, the launcher having cleared its four
# folders (python-arm64, python-x86_64, game, licences): the folder, and the three beside them.
KEPT_MARKED = ("FreeSail.command", "LICENCES.txt", "START HERE.txt")


def player_env(home: Path) -> dict[str, str]:
    """The variables by which the game, Python and the system find the player's own
    places, every one pointed into `home` (the test's, never a person's)."""
    return {
        "HOME": str(home),
        "USERPROFILE": str(home),
        "APPDATA": str(home / "AppData" / "Roaming"),
        "LOCALAPPDATA": str(home / "AppData" / "Local"),
        "XDG_CONFIG_HOME": str(home / ".config"),
        "XDG_DATA_HOME": str(home / ".local" / "share"),
    }


def user_data(home: Path) -> Path:
    """The game's own folder in the player's place (freesail/settings.py), under `home`."""
    if WINDOWS:
        return home / "AppData" / "Roaming" / "FreeSail"
    if MAC:
        return home / "Library" / "Application Support" / "FreeSail"
    return home / ".config" / "freesail"


def user_sites(home: Path) -> list[Path]:
    """The user's site-packages a Python 3.11 of that system reads unless told not to (-s,
    -I): site.getusersitepackages() for the home `home`."""
    if WINDOWS:
        return [home / "AppData" / "Roaming" / "Python" / "Python311" / "site-packages"]
    sites = [home / ".local" / "lib" / "python3.11" / "site-packages"]
    if MAC:  # a framework build's
        sites.append(home / "Library" / "Python" / "3.11" / "lib" / "python" / "site-packages")
    return sites


def unpack(zip_path: Path, dest: Path, f: Findings) -> Path:
    dest.mkdir(parents=True)
    if WINDOWS:
        # "Extract All": a folder named for the zip, in which the zip's entries are laid
        into = dest / zip_path.stem
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Expand-Archive -LiteralPath $env:SMOKE_ZIP -DestinationPath $env:SMOKE_DEST",
            ],
            env={**os.environ, "SMOKE_ZIP": str(zip_path), "SMOKE_DEST": str(into)},
            check=True,
        )
    elif MAC:
        # the mark Safari gives a download; ditto, as Archive Utility, passes it to every
        # file it unpacks
        mark = f"0083;{int(time.time()):08x};Safari;{uuid.uuid4()}".upper()
        subprocess.run(["xattr", "-w", "com.apple.quarantine", mark, str(zip_path)], check=True)
        subprocess.run(["ditto", "-x", "-k", str(zip_path), str(dest)], check=True)
    else:  # elsewhere (the harness's own trial): Info-ZIP keeps the modes
        subprocess.run(["unzip", "-q", str(zip_path), "-d", str(dest)], check=True)
    made = sorted(dest.iterdir())
    top = made[0] if len(made) == 1 and made[0].is_dir() else None
    f.check(
        top is not None and (top / LAUNCHER).is_file(),
        "the unpacking makes one folder, the launcher at its top",
        f"{top.name}/{LAUNCHER}" if top is not None else ", ".join(p.name for p in made),
    )
    if top is None:
        raise RuntimeError("the zip did not unpack to one folder")
    return top


def quarantined(top: Path, inside: tuple[str, ...] = ()) -> list[str]:
    places = [str(top / p) for p in inside] if inside else [str(top)]
    out = subprocess.run(
        ["xattr", "-r", "-l", *places], capture_output=True, text=True, errors="replace"
    ).stdout
    return [line.split(":")[0] for line in out.splitlines() if "com.apple.quarantine" in line]


def plant(folder: Path, marks: Path, place: str) -> None:
    """The poison's modules in `folder`, each leaving the mark `place-name` in `marks` if
    it is run, and a `.pth` file that leaves `place-pth` if a site reads it."""
    folder.mkdir(parents=True, exist_ok=True)
    for name in POISONED:
        mark = str(marks / f"{place}-{name}")
        (folder / f"{name}.py").write_text(
            f"open({mark!r}, 'w').write('run')\n"
            f"raise ImportError('the {place} {name}, which the game must never see')\n",
            encoding="utf-8",
        )
    pth = str(marks / f"{place}-pth")
    (folder / "zz-poison.pth").write_text(
        f"import os; open({pth!r}, 'w').write('run')\n", encoding="utf-8"
    )


def poison(work: Path, home: Path, started_from: Path) -> tuple[Path, Path]:
    """The poison planted in its three places (the docstring's step 3); its marks' folder
    and the folder PYTHONPATH names returned."""
    marks = work / "marks"
    marks.mkdir()
    named = work / "named by PYTHONPATH"
    plant(named, marks, "environment")
    (named / "startup.py").write_text(
        f"open({str(marks / 'environment-startup')!r}, 'w').write('run')\n", encoding="utf-8"
    )
    for site in user_sites(home):
        plant(site, marks, "user-site")
    plant(started_from, marks, "started-from")
    return marks, named


# What the launcher is given of the machine's own environment: these names and no other,
# read from the machine only on Windows, where Python and the system cannot start without
# them (the Windows folder; the processor, which Python's `platform` reads). Everything else
# the launcher sees is made here, pointed into the test's own folder: no FREESAIL_* (the
# settings file a person names), no home, no temporary folder of a person's gets through.
FROM_THE_MACHINE = {
    "windows": ("SystemRoot", "SystemDrive", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS"),
    "mac": (),
    "linux": (),
}


def launcher_env(
    system: str, machine: Mapping[str, str], home: Path, work: Path, named: Path
) -> dict[str, str]:
    """The whole environment the launcher is started with, built from nothing (a pure
    function of its arguments: `machine` is the caller's environment, of which only
    FROM_THE_MACHINE[system] is taken). The player's places (`player_env`) and the
    temporary folder lie in the test's folder; the PATH is the system's own; and the three
    PYTHON* variables name the poison's folder, which the launchers must clear."""
    env = {k: machine[k] for k in FROM_THE_MACHINE[system] if machine.get(k)}
    env.update(player_env(home))
    temp = str(work / "temp")
    if system == "windows":
        root = env.setdefault("SystemRoot", r"C:\Windows")
        env["PATH"] = ";".join(
            [
                rf"{root}\System32",
                root,
                rf"{root}\System32\Wbem",
                rf"{root}\System32\WindowsPowerShell\v1.0",
            ]
        )
        env["windir"] = root
        env["ComSpec"] = rf"{root}\System32\cmd.exe"
        env["PATHEXT"] = ".COM;.EXE;.BAT;.CMD"
        env["TEMP"] = env["TMP"] = temp
    else:
        env["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin"
        env["TMPDIR"] = temp
        env["LANG"] = "en_US.UTF-8" if system == "mac" else "C.UTF-8"
    env["PYTHONPATH"] = str(named)
    env["PYTHONHOME"] = str(named)
    env["PYTHONSTARTUP"] = str(named / "startup.py")
    return env


def this_system() -> str:
    return "windows" if WINDOWS else "mac" if MAC else "linux"


def free_port() -> int:
    """A port no one listens on now, the system's choice: the test's game runs there, never
    on the 8000 a person's own game is on."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def answers(port: int) -> bool:
    """Whether anything at all listens on the port, by IPv4 or IPv6 (localhost is either)."""
    for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
        try:
            with socket.socket(family, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex((host, port)) == 0:
                    return True
        except OSError:
            pass
    return False


def inside(path: str, home: Path) -> bool:
    return os.path.normcase(path).startswith(os.path.normcase(str(home)) + os.sep)


def its_own_game(window: str, home: Path, proc: subprocess.Popen, page: Page) -> str:
    """Why what answers is not the test's own game, or "" when it is. Asked before a
    single order, by reads alone: the launcher still running, no word of its port being
    taken, the game's window naming its settings file inside the test's home, and the
    server itself saying so (the harbour's state names the settings file it holds, which
    no other game would have inside the test's folder)."""
    if proc.poll() is not None:
        return f"the test's launcher has ended (code {proc.returncode}), yet a server answers"
    if PORT_WORDS in window:
        return "the game said its port is taken"
    line = next((ln.strip() for ln in window.splitlines() if "The settings: " in ln), "")
    named = line.partition("The settings: ")[2].split(" (not read")[0]
    if not named:
        return "the game's window names no settings file"
    if not inside(named, home):
        return f"the game's settings are not the test's: {named}"
    try:
        harbour = page.ask("GET", "/harbour", timeout=30)
        m = re.search(r'<meta name="freesail-page" content="([^"]+)"', str(harbour))
        if not m:
            return "what answers has no harbour page of the game's"
        page.mark = m.group(1)
        state = page.ask("GET", "/api/harbour/state", timeout=30)
        held = str(((state or {}).get("settings") or {}).get("path", ""))
    except Exception as e:  # noqa: BLE001 - any answer but the game's own is not it
        return f"what answers is not the game's harbour: {type(e).__name__}: {e}"
    if not inside(held, home):
        return f"the server holds settings that are not the test's: {held or 'none'}"
    return ""


def without_isolation(top: Path) -> str:
    """Every guard of the unpacked launcher against the poison taken out: its `-I`, the
    `PYTHONNOUSERSITE` it sets (a second guard of the user site: with it left in, the
    user site's poison is not run even without `-I`), and on Windows the interpreter's
    `._pth`. What the proof of the poison's teeth runs; what was taken out said."""
    launcher = top / LAUNCHER
    text = launcher.read_bytes()
    nousersite = b'set "PYTHONNOUSERSITE=1"\r\n' if WINDOWS else b" PYTHONNOUSERSITE=1"
    for guard in (b" -I -B ", nousersite):
        if text.count(guard) != 1:
            raise RuntimeError(f"{LAUNCHER} has not one {guard!r} to take out")
    text = text.replace(b" -I -B ", b" -B ").replace(nousersite, b"")
    launcher.write_bytes(text)
    taken = [f"-I and PYTHONNOUSERSITE from {LAUNCHER}"]
    if WINDOWS:
        (top / "python" / "python311._pth").unlink()
        taken.append("python\\python311._pth")
    return " and ".join(taken)


def start(top: Path, env: dict[str, str], log: Path, cwd: Path, port: int) -> subprocess.Popen:
    """The launcher run as a player runs it, on the test's own port (the launchers pass
    their arguments on to the game)."""
    out = open(log, "wb")
    flags = ["--no-browser", "--port", str(port)]
    if WINDOWS:
        return subprocess.Popen(
            ["cmd.exe", "/c", str(top / LAUNCHER), *flags],
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE,
            stdout=out,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    return subprocess.Popen(
        ["/bin/bash", str(top / LAUNCHER), *flags],
        cwd=cwd,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


class Page:
    """The harbour's page in a browser on the machine: its mark in every request."""

    def __init__(self, base: str) -> None:
        self.base = base
        self.mark = ""

    def ask(self, method: str, path: str, body: dict | None = None, timeout: float = 120):
        headers = {"Origin": self.base}
        if self.mark:
            headers["x-freesail-page"] = self.mark
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(self.base + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            kind = r.headers.get("content-type", "")
        return json.loads(raw) if "json" in kind else raw.decode("utf-8", "replace")


def wait_for_server(proc: subprocess.Popen, seconds: float, base: str) -> float:
    began = time.time()
    while time.time() - began < seconds:
        if proc.poll() is not None:
            return -1.0
        try:
            urllib.request.urlopen(base + "/harbour", timeout=2).read()
            return time.time() - began
        except (urllib.error.URLError, OSError):
            time.sleep(1)
    return -1.0


def interpreters() -> list[tuple[str, str]]:
    """The running Pythons that run the game: (their executable's path, their command)."""
    if WINDOWS:
        ps = (
            "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*-m freesail*' }"
            " | Select-Object ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        )
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True
        ).stdout.strip()
        if not out:
            return []
        rows = json.loads(out)
        rows = rows if isinstance(rows, list) else [rows]
        return [
            (r.get("ExecutablePath") or "", r.get("CommandLine") or "")
            for r in rows
            if "python" in (r.get("ExecutablePath") or "").lower()
        ]
    out = subprocess.run(
        ["ps", "-axww", "-o", "pid=,command="], capture_output=True, text=True
    ).stdout
    found = []
    for line in out.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if "-m freesail" in cmd and "bash" not in cmd.split()[0]:
            if Path(f"/proc/{pid}/exe").exists():  # elsewhere than the Mac
                exe = os.readlink(f"/proc/{pid}/exe")
            else:  # the Mac's ps says the whole path the interpreter was started by
                exe = subprocess.run(
                    ["ps", "-p", pid, "-o", "comm="], capture_output=True, text=True
                ).stdout.strip()
            found.append((exe, cmd))
    return found


def stop(proc: subprocess.Popen) -> str:
    """The game stopped as a player stops it; the road said."""
    if WINDOWS:
        # Ctrl+Break: a runner has no window to press Ctrl+C in, and Ctrl+C cannot be sent to
        # a process group of its own. The server takes the break as it takes Ctrl+C (uvicorn
        # handles both and shuts down cleanly), then raises it again once it has shut down,
        # and Windows ends a process on a break with code 3: so 3 is this road's clean stop.
        proc.send_signal(signal.CTRL_BREAK_EVENT)
        road = "Ctrl+Break in its window"
        try:
            # cmd's "Terminate batch job (Y/N)?" answered N, and its pause answered: the
            # launcher goes on to say the game has stopped, as it does in a player's window
            proc.stdin.write(b"N\r\n\r\n")
            proc.stdin.close()
        except OSError:
            pass
        return road
    os.killpg(proc.pid, signal.SIGINT)
    return "Control-C in its window"


PORT_WORDS = "FreeSail seems to be running already"


def the_game(page: Page, f: Findings) -> None:
    """The game played as a friend would, from the harbour (the docstring's step 5)."""
    harbour = page.ask("GET", "/harbour")
    m = re.search(r'<meta name="freesail-page" content="([^"]+)"', harbour)
    f.check(bool(m), "the harbour's page, with the game's mark in it", f"{len(harbour)} bytes")
    page.mark = m.group(1) if m else ""
    state = page.ask("GET", "/api/harbour/state")
    f.check(isinstance(state, dict), "the harbour's state")
    cat = page.ask("GET", "/api/harbour/catalogue")
    first = (cat or {}).get("first_game") or {}
    f.check(
        "first passage" in str(first.get("name", "")).lower(),
        "the harbour's first game",
        f"{first.get('name')} ({first.get('path')})",
    )
    begun = page.ask("POST", "/api/harbour/start", {"scenario": first.get("path", "")})
    f.check(
        isinstance(begun, dict) and "error" not in begun,
        "A first passage begun from the harbour",
        " / ".join((begun or {}).get("lines", [])[:1]) if isinstance(begun, dict) else "",
    )
    game = page.ask("GET", "/")
    f.check("<html" in game.lower(), "the game's page", f"{len(game)} bytes")
    for script in sorted(set(re.findall(r'src="(/client/[^"?]+)', game)))[:20]:
        page.ask("GET", script)
    tick0 = page.ask("GET", "/api/state").get("tick")
    ship = page.ask("GET", "/api/ship")
    f.check(isinstance(ship, dict) and bool(ship), "the ship's drawing")
    page.ask("POST", "/api/driver", {"action": "tick", "value": 60})
    tick1 = page.ask("GET", "/api/state").get("tick")
    f.check(
        isinstance(tick0, int) and tick1 == tick0 + 60,
        "a minute of the game's time run",
        f"tick {tick0} to {tick1}",
    )
    primer = page.ask("GET", "/api/library?topic=primer%207")
    f.check(
        "first passage" in (primer.get("title", "") + primer.get("text", "")).lower(),
        "the primer's chapter 7 read",
        primer.get("title", ""),
    )
    chart = page.ask("GET", "/api/harbour/chart")
    f.check(
        isinstance(chart, dict) and bool(chart),
        "the harbour's chart",
        f"{len(str(chart))} chars",
    )
    page.ask("POST", "/api/driver", {"action": "save", "value": SAVE_NAME})
    # a second game, on the Channel's chart, whose minute opens the charts' depth tiles
    # (A first passage is in open water and touches none)
    begun = page.ask("POST", "/api/harbour/start", {"scenario": "data/scenarios/tender.yaml"})
    t0 = page.ask("GET", "/api/state").get("tick")
    page.ask("POST", "/api/driver", {"action": "tick", "value": 60})
    t1 = page.ask("GET", "/api/state").get("tick")
    sea = page.ask("GET", "/api/chart")
    f.check(
        isinstance(t0, int) and t1 == t0 + 60 and isinstance(sea, dict) and bool(sea),
        "a second game on the Channel's chart: a minute run and its chart drawn",
        " / ".join((begun or {}).get("lines", [])[:2]) if isinstance(begun, dict) else "",
    )


def stopped(proc: subprocess.Popen, f: Findings, seconds: float = 90) -> str:
    road = stop(proc)
    try:
        proc.wait(timeout=seconds)
    except subprocess.TimeoutExpired:
        f.fail("the game stops when asked", f"still running after {seconds:.0f} s")
        proc.kill()
    return road


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("zip", help="the built download")
    ap.add_argument("--title", default="", help="the annotations' title")
    ap.add_argument(
        "--without-isolation",
        action="store_true",
        help="the proof of the poison check's teeth: -I (and Windows' ._pth) taken out of "
        "the unpacked download, which must then read the poison",
    )
    args = ap.parse_args(argv)
    zip_path = Path(args.zip).resolve()
    machine = platform.machine()
    teeth = args.without_isolation
    f = Findings(
        args.title
        or f"smoke test{' without isolation' if teeth else ''}, {zip_path.name} on "
        f"{sys.platform} {machine}"
    )
    window = ""
    # the test's one folder, and nothing of anyone's outside it
    work = Path(tempfile.mkdtemp(prefix="FreeSail smoke ä "))
    home = work / "home"
    home.mkdir()
    started_from = work / "started from here"
    log = work / "window.txt"
    proc = None
    try:
        top = unpack(zip_path, work / "Free Sail Proof ä", f)
        if MAC:
            marked = quarantined(top)
            f.check(
                len(marked) > 0,
                "the unpacked files carry the quarantine mark, as a browser's download's do",
                f"{len(marked)} files marked",
            )
        if teeth:
            f.ok("isolation taken out of the unpacked download", without_isolation(top))
        before = digests(top)
        f.ok("the unpacked folder", f"{top} ({len(before)} entries)")
        marks, named = poison(work, home, started_from)
        f.ok(
            "poison planted where the launchers clear nothing",
            "; ".join(str(p) for p in [*user_sites(home), started_from]),
        )
        env = launcher_env(this_system(), os.environ, home, work, named)
        (work / "temp").mkdir()
        port = free_port()
        base = f"http://localhost:{port}"
        # nothing of anyone's is ever spoken to: if anything answers on the test's own port
        # before its launcher runs (a person's game, another program), the test stops here
        if not f.check(
            not answers(port),
            "nothing answers on the test's own port before its launcher runs",
            f"port {port}",
        ):
            return 1
        began = time.time()
        proc = start(top, env, log, started_from, port)
        if teeth:
            places = (
                ("started-from", "the folder it is started from"),
                ("user-site", "the user's site-packages"),
            )
            up = -1.0
            while time.time() - began < 120 and proc.poll() is None:
                left = [p.name for p in marks.iterdir()]
                if all(any(m.startswith(k + "-") for m in left) for k, _ in places):
                    break
                if up < 0 and wait_for_server(proc, 1, base) >= 0:
                    up = time.time() - began
                time.sleep(1)
            if proc.poll() is None:
                stopped(proc, f, 30)
            window = log.read_text("utf-8", "replace")
            left = sorted(p.name for p in marks.iterdir())
            for place, what in places:
                got = [m for m in left if m.startswith(place + "-")]
                f.check(
                    bool(got),
                    f"without isolation, the poison in {what} is run (the check has teeth)",
                    ", ".join(got) or "no mark",
                )
            f.ok("the server", f"answered after {up:.0f} s" if up >= 0 else "did not answer")
            return 0 if f.passed else 1
        up = wait_for_server(proc, 240, base)
        window = log.read_text("utf-8", "replace")
        if not f.check(up >= 0, "the server answers", f"after {up:.0f} s" if up >= 0 else ""):
            return 1
        # before a single order: what answers is the test's own game, or the run ends here
        if not f.check(
            PORT_WORDS not in window,
            "a first start says nothing of its port being taken",
            next((ln.strip() for ln in window.splitlines() if PORT_WORDS in ln), "no such word"),
        ):
            return 1
        page = Page(base)
        why = its_own_game(window, home, proc, page)
        if not f.check(not why, "what answers is the test's own game", why or f"port {port}"):
            return 1
        the_game(page, f)
        time.sleep(1)
        running = interpreters()
        here = os.path.normcase(str(top.resolve()))
        inside = [
            exe for exe, _ in running if os.path.normcase(str(Path(exe).resolve())).startswith(here)
        ]
        f.check(
            bool(running) and len(inside) == len(running),
            "the game runs on the download's own Python",
            "; ".join(exe for exe, _ in running) or "no interpreter found",
        )
        left = sorted(p.name for p in marks.iterdir())
        f.check(
            not left,
            "none of the poison was run (the environment's, the user's site's, the folder "
            "it is started from)",
            ", ".join(left) or "no mark",
        )
        road = stopped(proc, f)
        window = log.read_text("utf-8", "replace")
        try:
            urllib.request.urlopen(base + "/harbour", timeout=3).read()
            gone = False
        except (urllib.error.URLError, OSError):
            gone = True
        f.check(gone, "the server no longer answers once stopped")
        clean = ("FreeSail has stopped (exit code 0)",) + (
            ("FreeSail has stopped (exit code 3)",) if WINDOWS else ()
        )
        f.check(
            any(c in window for c in clean),
            f"the game stops cleanly when asked ({road})",
            next((ln.strip() for ln in window.splitlines() if "has stopped" in ln), "no word"),
        )
        f.check("Traceback" not in window, "no traceback in the game's window")
        f.ok("the whole run", f"{time.time() - began:.0f} s from the launcher to the stop")
        after = digests(top)
        new = sorted(set(after) - set(before))
        gone = sorted(set(before) - set(after))
        changed = sorted(k for k in before.keys() & after.keys() if before[k] != after[k])
        f.check(
            not (new or gone or changed),
            "nothing written inside the unpacked folder",
            "; ".join(
                f"{what}: {', '.join(items[:8])}"
                for what, items in (("new", new), ("gone", gone), ("changed", changed))
                if items
            )
            or f"{len(after)} entries as unpacked",
        )
        if MAC:
            # the download's own folders, which the launcher clears; the folder, the launcher
            # and the pages beside it keep theirs (the player opened the launcher, no more)
            marked = quarantined(top, ("python-arm64", "python-x86_64", "game", "licences"))
            f.check(
                not marked,
                "the launcher cleared the quarantine on its four folders",
                f"{len(marked)} left in them",
            )
            kept = sorted({Path(m).name for m in quarantined(top)})
            f.check(
                kept == sorted((top.name, *KEPT_MARKED)),
                "the folder, the launcher and the pages beside it keep their mark",
                ", ".join(kept) or "none",
            )
        data = user_data(home)
        saved = data / "saves" / f"{SAVE_NAME}.json"
        f.check(saved.is_file(), "the save lies in the player's own data folder", str(saved))
        f.ok(
            "the player's data folder",
            f"{data} (settings file there: {(data / 'settings.yaml').is_file()})",
        )
    except Exception as e:  # every failure said, never a bare traceback
        f.fail("the smoke test ran to its end", f"{type(e).__name__}: {e}")
        if proc is not None and proc.poll() is None:
            stopped(proc, f, 30)
        try:
            window = log.read_text("utf-8", "replace")
        except OSError:
            pass
    finally:
        if proc is not None and proc.poll() is None:
            # the game stopped as asked, then the whole of it ended (its window's process
            # group, not the launcher alone), on every road out, a refusal's too
            stop(proc)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                if WINDOWS:
                    subprocess.run(
                        ["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True
                    )
                else:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                    except OSError:
                        pass
                proc.kill()
        f.report(window)
        shutil.rmtree(work, ignore_errors=True)
    return 0 if f.passed else 1


if __name__ == "__main__":
    sys.exit(main())
