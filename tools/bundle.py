"""The downloads for a machine without Python (package 130): one zip for Windows and one for
the Mac, each carrying its own Python, the game's dependencies and the game, and ONE thing
to open at its top (`FreeSail.cmd`, `FreeSail.command`) beside a "start here" page.

    python tools/bundle.py windows --name NAME [--out DIR] [--cache DIR]
    python tools/bundle.py mac     --name NAME [--out DIR] [--cache DIR]
    python tools/bundle.py files                  # the game's files a download ships
    python tools/bundle.py lock                   # resolve the three lock files again

What each download holds, and why (docs/design/Report-Package130.md):

- **The game**, by a rule and not a list (`game_files`): every file git tracks under
  `freesail/`, `client/`, `data/` and `docs/primer/`, and `README.md` and
  `docs/agents/ConsentBrief.md`. That is what the game opens when it runs, measured by
  Python's audit hook (tests/test_downloads.py, truth 7-800, holds it so: a file the game
  opens that the rule leaves out fails that test). Not the owner's consent records
  (`docs/agents/consent/`), the tests, the tools or the rest of the documents.
- **A Python of its own**, every byte pinned by version and checksum (`INTERPRETERS`):
  python.org's embeddable CPython for Windows; for the Mac, python-build-standalone's
  relocatable CPython for Apple silicon and for Intel, both in one download (python.org
  builds no relocatable Python for macOS).
- **The dependencies**: the game's base, its `server` extra and its `agents` extra (never
  `dev`), from the lock files in `tools/bundle/locks/` (one per platform, every artifact's
  sha256 in it), installed with pip's `--require-hashes --no-deps --only-binary=:all:` for
  the download's platform, whatever machine builds it.
- **The licences** of everything third-party it carries, in `licences/`.

Nothing in a download reads the machine's own Python: on Windows the interpreter's
`python311._pth` names the only places it imports from (which also makes it ignore
`PYTHONPATH`, `PYTHONHOME` and the registry), and both launchers run it by its own path with
`-I` (no user site, no environment) and `-B` (nothing written beside the code).

The zip is deterministic in what it holds: its entries sorted, each dated by the commit
built, its mode kept (the Mac's launcher and interpreter executable), the tiles and other
compressed files stored and the rest deflated.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "tools" / "bundle"
LOCKS = HERE / "locks"

# ---------------------------------------------------------------------------
# What ships of the game
# ---------------------------------------------------------------------------

GAME_DIRS = ("freesail", "client", "data", "docs/primer")
GAME_FILES = ("README.md", "docs/agents/ConsentBrief.md")
# Never shipped, whatever git tracks under the folders above (none is today): the bytes a
# Python writes beside its code, and a Mac's folder notes.
NEVER = ("__pycache__", ".DS_Store")


def _shipped(rel: str) -> bool:
    parts = rel.split("/")
    if any(p in NEVER for p in parts) or rel.endswith((".pyc", ".pyo")):
        return False
    return rel in GAME_FILES or any(rel == d or rel.startswith(d + "/") for d in GAME_DIRS)


def game_files(root: Path = ROOT) -> list[str]:
    """The game's files a download ships, as paths relative to the repository with `/`,
    sorted: every file git tracks under `GAME_DIRS` and the files `GAME_FILES` name. From a
    copy that is not a git checkout (a gate's zip), every file under them."""
    root = Path(root)
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z", "--", *GAME_DIRS, *GAME_FILES],
            cwd=root,
            capture_output=True,
            check=True,
        ).stdout
        names = [n.decode("utf-8") for n in out.split(b"\0") if n]
    except (OSError, subprocess.CalledProcessError):
        names = [f for f in GAME_FILES if (root / f).is_file()]
        for d in GAME_DIRS:
            for p in (root / d).rglob("*"):
                if p.is_file():
                    names.append(p.relative_to(root).as_posix())
    return sorted({n for n in names if _shipped(n) and (root / n).is_file()})


# ---------------------------------------------------------------------------
# The pinned third parties
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Pin:
    """A download from its maker's own published place, by version and sha256."""

    what: str
    version: str
    url: str
    sha256: str
    licence: str  # where its licence text lies in the download, said in licences/README.txt

    @property
    def filename(self) -> str:
        return self.url.rsplit("/", 1)[1].replace("%2B", "+")


PBS = "https://github.com/astral-sh/python-build-standalone/releases/download/20260718/"
INTERPRETERS = {
    # python.org's embeddable package: 3.11.9 is the last 3.11 python.org built for Windows
    "windows": Pin(
        "CPython, python.org's embeddable package for Windows (64-bit)",
        "3.11.9",
        "https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip",
        "009d6bf7e3b2ddca3d784fa09f90fe54336d5b60f0e0f305c37f400bf83cfd3b",
        "licences/python/LICENSE.txt",
    ),
    # python-build-standalone (the relocatable CPython builds that uv installs), release
    # 20260718, its sha256 from that release's SHA256SUMS
    "arm64": Pin(
        "CPython, python-build-standalone's relocatable build for macOS on Apple silicon",
        "3.11.15+20260718",
        PBS + "cpython-3.11.15%2B20260718-aarch64-apple-darwin-install_only_stripped.tar.gz",
        "b21dbc3f3e01932fcc3f0f4c51e5a7ef61888cb454d23eee6e8207c6f52d0b04",
        "licences/python/ (LICENSE.cpython.txt and the libraries it is built with)",
    ),
    "x86_64": Pin(
        "CPython, python-build-standalone's relocatable build for macOS on Intel",
        "3.11.15+20260718",
        PBS + "cpython-3.11.15%2B20260718-x86_64-apple-darwin-install_only_stripped.tar.gz",
        "8ca3906ed23f4a8ab4ff8f02d61b15ecf62e6fa8b312cd59d1692df34e834a65",
        "licences/python/ (LICENSE.cpython.txt and the libraries it is built with)",
    ),
}

# The lock file of each interpreter's dependencies, and the platform pip installs them for
# (pip widens a macOS tag to the older ones it accepts: 12 is the oldest macOS the download
# promises, and the arm64 wheels say 11).
LOCK_FILES = {
    "windows": "windows-x86_64.txt",
    "arm64": "macos-arm64.txt",
    "x86_64": "macos-x86_64.txt",
}
PIP_PLATFORMS = {
    "windows": "win_amd64",
    "arm64": "macosx_12_0_arm64",
    "x86_64": "macosx_12_0_x86_64",
}
# uv's names of the same platforms, for `lock`
UV_PLATFORMS = {
    "windows": "x86_64-pc-windows-msvc",
    "arm64": "aarch64-apple-darwin",
    "x86_64": "x86_64-apple-darwin",
}
# The extras a download carries beside the game's base (pyproject.toml): never `dev`.
EXTRAS = ("server", "agents")


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch(pin: Pin, cache: Path) -> Path:
    """The pinned file, from the cache when it is there with the right checksum, else from
    its maker's place; refused unless its sha256 is the pinned one."""
    cache.mkdir(parents=True, exist_ok=True)
    path = cache / pin.filename
    if path.is_file() and sha256_of(path) == pin.sha256:
        return path
    part = path.with_name(path.name + ".part")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(pin.url, timeout=120) as r, open(part, "wb") as f:
                shutil.copyfileobj(r, f)
            break
        except OSError:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))
    got = sha256_of(part)
    if got != pin.sha256:
        part.unlink()
        raise SystemExit(f"{pin.url}: sha256 {got}, pinned {pin.sha256}; refused.")
    part.replace(path)
    return path


def install_dependencies(which: str, target: Path) -> None:
    """The lock file's dependencies into `target`, for the download's platform, each wheel
    checked against its hash; no build from a source, no script, nothing compiled."""
    lock = LOCKS / LOCK_FILES[which]
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--disable-pip-version-check",
            "--no-input",
            "--isolated",
            "--target",
            str(target),
            "--no-deps",
            "--require-hashes",
            "--only-binary=:all:",
            "--no-compile",
            "--platform",
            PIP_PLATFORMS[which],
            "--python-version",
            "3.11",
            "--implementation",
            "cp",
            "-r",
            str(lock),
        ],
        check=True,
    )
    # pip's console scripts name the build machine's Python; the download runs none of them
    shutil.rmtree(target / "bin", ignore_errors=True)


def dependency_licences(site: Path, into: Path) -> list[str]:
    """Every installed distribution's licence files (its dist-info's `licenses/`, or the
    LICENSE, COPYING and NOTICE files beside its METADATA), copied to `into/<name>/`; the
    distributions' names and versions returned."""
    found: list[str] = []
    for info in sorted(site.glob("*.dist-info")):
        name = info.name[: -len(".dist-info")]
        dest = into / name
        files = (
            [p for p in (info / "licenses").rglob("*") if p.is_file()]
            if (info / "licenses").is_dir()
            else []
        )
        files += [
            p
            for p in info.iterdir()
            if p.is_file() and p.name.upper().startswith(("LICEN", "COPYING", "NOTICE", "AUTHORS"))
        ]
        for p in files:
            rel = p.relative_to(info / "licenses") if (info / "licenses") in p.parents else p.name
            out = dest / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, out)
        if not files:
            # the licence is named in the METADATA alone: that is kept
            dest.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(info / "METADATA", dest / "METADATA")
        found.append(name)
    return found


# ---------------------------------------------------------------------------
# Assembling a download
# ---------------------------------------------------------------------------


def commit_of(root: Path = ROOT) -> tuple[str, int]:
    """The commit built and its time (the zip's entries are dated by it), or none."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H %ct"], cwd=root, capture_output=True, check=True
        ).stdout.decode()
        sha, ts = out.split()
        return sha, int(ts)
    except (OSError, subprocess.CalledProcessError, ValueError):
        return "unknown", int(os.environ.get("SOURCE_DATE_EPOCH", "315532800"))


def _text(name: str, fill: dict[str, str], crlf: bool) -> bytes:
    text = (HERE / name).read_text(encoding="utf-8")
    for k, v in fill.items():
        text = text.replace("{{" + k + "}}", v)
    if "{{" in text:
        raise SystemExit(f"{name}: a placeholder is left unfilled.")
    if crlf:
        text = text.replace("\r\n", "\n").replace("\n", "\r\n")
    return text.encode("utf-8")


def copy_game(top: Path, root: Path = ROOT) -> int:
    names = game_files(root)
    for rel in names:
        dest = top / "game" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / rel, dest)
    return len(names)


def licences_readme(top: Path, pins: list[Pin], dists: list[str], platform: str) -> None:
    lines = [
        "The licences of what this download carries (FreeSail's package 130).",
        "",
        "FreeSail itself: the game in game/, under the MIT licence its pyproject.toml names.",
        "",
        "The Python it runs on:",
    ]
    for p in pins:
        lines += [f"  {p.what}, {p.version}", f"    from {p.url}", f"    sha256 {p.sha256}"]
        lines += [f"    licence: {p.licence}"]
    lines += [
        "",
        f"The libraries the game uses, for {platform}, each from the Python Package Index by",
        "version and sha256 (tools/bundle/locks/ in the game's repository); each one's",
        "licence files are in the folder of its name here:",
    ]
    lines += [f"  {d}" for d in dists]
    (top / "licences" / "README.txt").write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))


def build_windows(name: str, out: Path, cache: Path, root: Path = ROOT) -> Path:
    pin = INTERPRETERS["windows"]
    sha, ts = commit_of(root)
    with tempfile.TemporaryDirectory() as tmp:
        top = Path(tmp) / f"FreeSail-{name}-windows"
        py = top / "python"
        py.mkdir(parents=True)
        with zipfile.ZipFile(fetch(pin, cache)) as z:
            z.extractall(py)
        # the only places the interpreter imports from: its own, the libraries and the game;
        # a ._pth also makes it ignore PYTHONPATH, PYTHONHOME and the registry. `import site`
        # runs the libraries' .pth files (pywin32's), the user's site being off by -I.
        (py / "python311._pth").write_bytes(
            b"python311.zip\r\n.\r\nLib\\site-packages\r\n..\\game\r\nimport site\r\n"
        )
        site = py / "Lib" / "site-packages"
        install_dependencies("windows", site)
        n = copy_game(top, root)
        fill = {"NAME": name, "COMMIT": sha[:12]}
        (top / "FreeSail.cmd").write_bytes(_text("FreeSail.cmd", fill, crlf=True))
        (top / "START HERE.txt").write_bytes(_text("START-HERE-windows.txt", fill, crlf=True))
        lic = top / "licences"
        (lic / "python").mkdir(parents=True)
        shutil.copyfile(py / "LICENSE.txt", lic / "python" / "LICENSE.txt")
        dists = dependency_licences(site, lic)
        licences_readme(top, [pin], dists, "Windows (64-bit)")
        path = write_zip(top, out / f"FreeSail-{name}-windows.zip", ts)
    print(f"{path}: the game's {n} files, Python {pin.version}, {len(dists)} libraries")
    return path


def build_mac(name: str, out: Path, cache: Path, root: Path = ROOT) -> Path:
    sha, ts = commit_of(root)
    pins = [INTERPRETERS["arm64"], INTERPRETERS["x86_64"]]
    with tempfile.TemporaryDirectory() as tmp:
        top = Path(tmp) / f"FreeSail-{name}-mac"
        top.mkdir(parents=True)
        dists: list[str] = []
        for arch in ("arm64", "x86_64"):
            pin = INTERPRETERS[arch]
            py = top / f"python-{arch}"
            with tarfile.open(fetch(pin, cache)) as t:
                staging = Path(tmp) / f"x-{arch}"
                t.extractall(staging, filter="tar")
            (staging / "python").rename(py)
            site = py / "lib" / "python3.11" / "site-packages"
            install_dependencies(arch, site)
            # the game, two folders up from the interpreter's own: site joins a relative
            # line of a .pth file to the site-packages folder it lies in
            (site / "freesail-game.pth").write_text("../../../../game\n", encoding="utf-8")
            lic = top / "licences" / f"libraries-{arch}"
            dists += [f"{d} ({arch})" for d in dependency_licences(site, lic)]
        n = copy_game(top, root)
        fill = {"NAME": name, "COMMIT": sha[:12]}
        launcher = top / "FreeSail.command"
        launcher.write_bytes(_text("FreeSail.command", fill, crlf=False))
        launcher.chmod(0o755)
        (top / "START HERE.txt").write_bytes(_text("START-HERE-mac.txt", fill, crlf=False))
        # python-build-standalone's own licence texts (those of CPython and every library it
        # is built with), from its full archive of the same release (tools/bundle/licences/)
        lic = top / "licences" / "python"
        lic.mkdir(parents=True)
        for p in sorted((HERE / "licences" / "python-build-standalone").iterdir()):
            shutil.copyfile(p, lic / p.name)
        licences_readme(top, pins, dists, "macOS (Apple silicon and Intel)")
        path = write_zip(top, out / f"FreeSail-{name}-mac.zip", ts)
    print(f"{path}: the game's {n} files, Python {pins[0].version} twice, {len(dists)} libraries")
    return path


STORED = (".npz", ".zip", ".gz", ".png", ".jpg", ".whl")


def write_zip(top: Path, path: Path, ts: int) -> Path:
    """The folder `top` as one zip with `top`'s name as its first folder: entries sorted,
    dated by `ts`, modes kept, symbolic links kept as links (a Mac's unzip makes them)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = time.gmtime(max(ts, 315532800))[:6]
    entries = sorted(p for p in top.rglob("*") if p.is_file() or p.is_symlink())
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in entries:
            arc = f"{top.name}/{p.relative_to(top).as_posix()}"
            info = zipfile.ZipInfo(arc, date_time=stamp)
            info.create_system = 3  # unix, so that the modes are read
            st = p.lstat()
            if stat.S_ISLNK(st.st_mode):
                info.external_attr = (stat.S_IFLNK | 0o755) << 16
                info.compress_type = zipfile.ZIP_STORED
                z.writestr(info, os.readlink(p))
                continue
            mode = 0o755 if st.st_mode & 0o111 else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = (
                zipfile.ZIP_STORED if p.suffix.lower() in STORED else zipfile.ZIP_DEFLATED
            )
            with open(p, "rb") as f, z.open(info, "w") as w:
                shutil.copyfileobj(f, w, 1 << 20)
    return path


# ---------------------------------------------------------------------------
# The lock files
# ---------------------------------------------------------------------------


def requirements(root: Path = ROOT) -> list[str]:
    """The game's base dependencies and its `EXTRAS`, as pyproject.toml says them."""
    import tomllib

    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    reqs = list(project["dependencies"])
    for extra in EXTRAS:
        reqs += project["optional-dependencies"][extra]
    return reqs


def lock(exclude_newer: str) -> None:
    """The three lock files resolved again by uv from pyproject.toml's base and extras, for
    each platform, with every artifact's sha256 and nothing newer than `exclude_newer`."""
    with tempfile.TemporaryDirectory() as tmp:
        given = Path(tmp) / "requirements.in"
        given.write_text("\n".join(requirements()) + "\n", encoding="utf-8")
        for which, name in LOCK_FILES.items():
            subprocess.run(
                [
                    "uv",
                    "pip",
                    "compile",
                    "--quiet",
                    str(given),
                    "--python-version",
                    "3.11",
                    "--python-platform",
                    UV_PLATFORMS[which],
                    "--generate-hashes",
                    # wheels alone, and those the platform takes: cryptography's Intel Mac
                    # wheels stop at 48, which uv would otherwise not notice
                    "--only-binary",
                    ":all:",
                    "--no-header",
                    "--no-annotate",
                    "--exclude-newer",
                    exclude_newer,
                    "-o",
                    str(LOCKS / name),
                ],
                check=True,
            )
            body = (LOCKS / name).read_text(encoding="utf-8")
            head = (
                f"# The libraries of FreeSail's download for {UV_PLATFORMS[which]} (package 130),\n"
                f"# resolved by `python tools/bundle.py lock --exclude-newer {exclude_newer}`\n"
                "# from pyproject.toml's base, server and agents; installed --require-hashes.\n"
            )
            (LOCKS / name).write_text(head + body, encoding="utf-8")


# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for which in ("windows", "mac"):
        p = sub.add_parser(which, help=f"build the {which} download")
        p.add_argument("--name", required=True, help="the download's name, e.g. gate-m7")
        p.add_argument("--out", default="dist", help="the folder the zip is written in")
        p.add_argument("--cache", default=str(Path(tempfile.gettempdir()) / "freesail-pins"))
    sub.add_parser("files", help="list the game's files a download ships")
    lk = sub.add_parser("lock", help="resolve the lock files again (needs uv)")
    lk.add_argument("--exclude-newer", required=True, help="a date, e.g. 2026-11-13")
    args = ap.parse_args(argv)
    if args.cmd == "files":
        out = io.StringIO()
        for n in game_files():
            out.write(n + "\n")
        sys.stdout.write(out.getvalue())
        return 0
    if args.cmd == "lock":
        lock(args.exclude_newer)
        return 0
    name = args.name
    if not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789.-" for c in name.lower()):
        raise SystemExit("A download's name is letters, figures, dots and dashes.")
    build = build_windows if args.cmd == "windows" else build_mac
    build(name, Path(args.out).resolve(), Path(args.cache))
    return 0


if __name__ == "__main__":
    sys.exit(main())
