"""The smoke test of a built download (package 130), run in the cloud on Windows and on both
kinds of Mac against the zip itself, by the runner's own Python as the harness (the game
never sees that Python).

    python tools/bundle_smoke.py FreeSail-NAME-windows.zip
    python tools/bundle_smoke.py FreeSail-NAME-mac.zip

What it does, in order, as a friend's machine would:

1. Unpacks the zip with the system's own tool into a fresh folder whose path has a space
   and a letter outside English in it (`~/Free Sail Proof ä/`): Expand-Archive on
   Windows; on the Mac `ditto`, after giving the zip the quarantine mark a browser gives
   its downloads, so that every unpacked file carries it as a friend's do.
2. Takes a digest of every file in the unpacked folder.
3. Starts the game by the launcher's own road (`cmd /c FreeSail.cmd`, `bash
   FreeSail.command`; `--no-browser`, which the launcher passes on), with the runner's
   Python hidden from it: PATH cut to the system's own folders, and PYTHONPATH,
   PYTHONHOME and PYTHONSTARTUP set to a folder of poisoned modules (`yaml.py`,
   `sitecustomize.py`, ...) that leave a mark if anything imports them.
4. Waits for the server; asks the harbour's page (taking its mark as a browser does), its
   state and catalogue; begins the catalogue's first game (*A first passage*); asks the
   game's page, its state and ship; runs sixty ticks (a minute of the game's time); reads
   the primer's chapter 7 from the library; asks the harbour's chart; saves; and begins a
   second game on the Channel's chart (*The tender*), runs a minute of it (its depth
   tiles read) and asks its chart.
5. Reads the running interpreter's path from the system (it must lie in the unpacked
   folder), and looks for the poison's marks (there must be none).
6. Stops the game (Control-C on the Mac, as a player does; on Windows Ctrl+Break, which
   the server takes as Ctrl+C, a runner having no window to press Ctrl+C in), and reads
   the launcher's "FreeSail has stopped (exit code 0)" (on Windows 3, the code Windows
   ends a process with on a break the server has re-raised after its clean shutdown),
   and that the server no longer answers.
7. Checks that no file in the unpacked folder is new, changed or gone, that the Mac's
   quarantine marks are cleared, and that the save lies in the user's own data folder.

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
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

WINDOWS = sys.platform.startswith("win")
MAC = sys.platform == "darwin"
PORT = 8000
BASE = f"http://localhost:{PORT}"
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


def user_data() -> Path:
    if WINDOWS:
        return Path(os.environ["APPDATA"]) / "FreeSail"
    if MAC:
        return Path.home() / "Library" / "Application Support" / "FreeSail"
    return Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config") / "freesail"


def unpack(zip_path: Path, dest: Path, f: Findings) -> Path:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    if WINDOWS:
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                "Expand-Archive -LiteralPath $env:SMOKE_ZIP -DestinationPath $env:SMOKE_DEST",
            ],
            env={**os.environ, "SMOKE_ZIP": str(zip_path), "SMOKE_DEST": str(dest)},
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
    tops = [p for p in dest.iterdir() if p.is_dir()]
    f.check(len(tops) == 1, "the zip unpacks to one folder", tops[0].name if tops else "none")
    return tops[0]


def quarantined(top: Path, inside: tuple[str, ...] = ()) -> list[str]:
    places = [str(top / p) for p in inside] if inside else [str(top)]
    out = subprocess.run(
        ["xattr", "-r", "-l", *places], capture_output=True, text=True, errors="replace"
    ).stdout
    return [line.split(":")[0] for line in out.splitlines() if "com.apple.quarantine" in line]


def poison(root: Path) -> tuple[Path, Path]:
    """A folder of modules that leave a mark in `marks` if anything imports them."""
    folder = root / "poison"
    marks = root / "marks"
    folder.mkdir(parents=True)
    marks.mkdir()
    for name in ("yaml", "sitecustomize", "usercustomize", "numpy", "fastapi", "freesail"):
        (folder / f"{name}.py").write_text(
            f"open({str(marks / name)!r}, 'w').write('imported')\n"
            f"raise ImportError('the runner\\'s {name}, which the game must never see')\n",
            encoding="utf-8",
        )
    (folder / "startup.py").write_text(
        f"open({str(marks / 'startup')!r}, 'w').write('run')\n", encoding="utf-8"
    )
    return folder, marks


def hidden_env(poison_dir: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
    if WINDOWS:
        sysroot = os.environ.get("SystemRoot", r"C:\Windows")
        env["PATH"] = ";".join(
            [
                rf"{sysroot}\System32",
                sysroot,
                rf"{sysroot}\System32\Wbem",
                rf"{sysroot}\System32\WindowsPowerShell\v1.0",
            ]
        )
    else:
        env["PATH"] = "/usr/bin:/bin:/usr/sbin:/sbin"
    env["PYTHONPATH"] = str(poison_dir)
    env["PYTHONHOME"] = str(poison_dir)
    env["PYTHONSTARTUP"] = str(poison_dir / "startup.py")
    return env


def start(top: Path, env: dict[str, str], log: Path) -> subprocess.Popen:
    out = open(log, "wb")
    if WINDOWS:
        return subprocess.Popen(
            ["cmd.exe", "/c", str(top / "FreeSail.cmd"), "--no-browser"],
            cwd=top,
            env=env,
            stdin=subprocess.PIPE,
            stdout=out,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
        )
    return subprocess.Popen(
        ["/bin/bash", str(top / "FreeSail.command"), "--no-browser"],
        cwd=top,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=out,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )


class Page:
    """The harbour's page in a browser on the machine: its mark in every request."""

    def __init__(self) -> None:
        self.mark = ""

    def ask(self, method: str, path: str, body: dict | None = None, timeout: float = 120):
        headers = {"Origin": BASE}
        if self.mark:
            headers["x-freesail-page"] = self.mark
        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            kind = r.headers.get("content-type", "")
        return json.loads(raw) if "json" in kind else raw.decode("utf-8", "replace")


def wait_for_server(proc: subprocess.Popen, seconds: float) -> float:
    began = time.time()
    while time.time() - began < seconds:
        if proc.poll() is not None:
            return -1.0
        try:
            urllib.request.urlopen(BASE + "/harbour", timeout=2).read()
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("zip", help="the built download")
    ap.add_argument("--title", default="", help="the annotations' title")
    args = ap.parse_args(argv)
    zip_path = Path(args.zip).resolve()
    machine = platform.machine()
    f = Findings(args.title or f"smoke test, {zip_path.name} on {sys.platform} {machine}")
    window = ""
    work = Path(tempfile.mkdtemp(prefix="smoke-"))
    dest = Path.home() / "Free Sail Proof ä"
    saves = user_data() / "saves"
    if saves.exists():
        shutil.rmtree(saves)
    proc = None
    try:
        top = unpack(zip_path, dest, f)
        if MAC:
            marked = quarantined(top)
            f.check(
                len(marked) > 0,
                "the unpacked files carry the quarantine mark, as a browser's download's do",
                f"{len(marked)} files marked",
            )
        before = digests(top)
        f.ok("the unpacked folder", f"{top} ({len(before)} entries)")
        poison_dir, marks = poison(work)
        env = hidden_env(poison_dir)
        log = work / "window.txt"
        began = time.time()
        proc = start(top, env, log)
        up = wait_for_server(proc, 240)
        window = log.read_text("utf-8", "replace")
        if not f.check(up >= 0, "the server answers", f"after {up:.0f} s" if up >= 0 else ""):
            return 1
        page = Page()
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
        f.check(not left, "nothing of the runner's Python was read", ", ".join(left) or "no mark")
        road = stop(proc)
        try:
            proc.wait(timeout=90)
        except subprocess.TimeoutExpired:
            f.fail("the game stops when asked", "still running after 90 s")
            proc.kill()
        window = log.read_text("utf-8", "replace")
        try:
            urllib.request.urlopen(BASE + "/harbour", timeout=3).read()
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
            # the download's own folders, which the launcher clears; the launcher itself, the
            # pages beside it and the folder keep theirs (the player opened the launcher)
            marked = quarantined(top, ("python-arm64", "python-x86_64", "game", "licences"))
            kept = sorted({Path(m).name for m in quarantined(top)} - {Path(m).name for m in marked})
            f.check(
                not marked,
                "the launcher cleared the quarantine on the download's folders",
                f"{len(marked)} left in them; still marked at the top: {', '.join(kept) or 'none'}",
            )
        saved = saves / f"{SAVE_NAME}.json"
        f.check(saved.is_file(), "the save lies in the user's data folder", str(saved))
        settings = user_data() / "settings.yaml"
        f.ok("the user's data folder", f"{user_data()} (settings file there: {settings.is_file()})")
    except Exception as e:  # every failure said, never a bare traceback
        f.fail("the smoke test ran to its end", f"{type(e).__name__}: {e}")
        if proc is not None and proc.poll() is None:
            stop(proc)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                proc.kill()
        try:
            window = (work / "window.txt").read_text("utf-8", "replace")
        except OSError:
            pass
    finally:
        f.report(window)
    return 0 if f.passed else 1


if __name__ == "__main__":
    sys.exit(main())
