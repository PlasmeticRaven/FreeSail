"""The downloads for a machine without Python (package 130; tools/bundle.py, tools/bundle/,
.github/workflows/downloads.yml; docs/design/Report-Package130.md). Truths 7-800 to 7-806.

The downloads themselves are built and proven in the cloud, on Windows and on both kinds of
Mac (tools/bundle_smoke.py). What is held here, on every push, is what a forgetful change
would break before anyone unpacked a zip: that the game's files the downloads ship hold
everything the game opens (a file added to the game next month and missed by the packer
fails here, not on a friend's first evening), that the libraries are the game's own and
pinned, that every third party is pinned by checksum and every action by its commit, and
that the launchers and the "start here" pages say what they must.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bundle  # noqa: E402

# What the game opens under the repository that a download rightly lacks: the tests' own
# files, the git metadata, and the record a development install leaves (a library's look
# at the installed distributions; the download has none and the game does not need it).
NOT_THE_GAMES = ("tests/", ".git/", "freesail.egg-info/", ".pytest_cache/", ".ruff_cache/")

_opened: list[str] | None = None


def _hook(event: str, args: tuple) -> None:
    if _opened is None or event != "open" or not args:
        return
    path = args[0]
    if isinstance(path, (str, bytes, os.PathLike)):
        _opened.append(os.fsdecode(path))


def _under_root(paths: list[str]) -> set[str]:
    found = set()
    for raw in paths:
        try:
            p = Path(raw).resolve()
            rel = p.relative_to(ROOT).as_posix()
        except (ValueError, OSError):
            continue
        if p.is_file():
            found.add(rel)
    return found


def _source_of(rel: str) -> str:
    """The source a compiled file stands for: freesail/x/__pycache__/y.cpython-311.pyc is
    freesail/x/y.py (the download carries the source alone and writes no bytecode)."""
    if "/__pycache__/" in rel and rel.endswith(".pyc"):
        folder, name = rel.split("/__pycache__/")
        return f"{folder}/{name.split('.')[0]}.py"
    return rel


def _forget_what_the_game_has_read() -> None:
    """Empty every `functools` cache in the game's modules already imported: a file another
    test in this process has read (the primer's pages, the charts' tiles) is otherwise
    served from memory, never opened again, and so never seen by the hook."""
    for name, module in list(sys.modules.items()):
        if name != "freesail" and not name.startswith("freesail."):
            continue
        for value in list(vars(module).values()):
            clear = getattr(value, "cache_clear", None)
            if callable(clear) and hasattr(value, "cache_info"):
                clear()


def test_truth_7_800_everything_the_game_opens_lies_in_what_the_downloads_ship(
    tmp_path, monkeypatch
):
    """Truth 7-800 (package 130, item 5): with Python's audit hook on every file opened, the
    server's app is started as `py -m freesail` starts it (the harbour, no game), the
    harbour's page, state and catalogue asked, the catalogue's first game begun (*A first
    passage*), its page, state and ship asked, a minute of its time run, a primer chapter
    and the library's topics served, the harbour's chart asked, the game saved, and a
    second game begun on the Channel's chart (*The tender*), a minute of it run and its
    chart asked: every file opened under the repository but the tests' own lies in the
    list the assembling script ships (`bundle.game_files`), and some of the charts' tiles
    and the primer's pages were among them. The game's caches are emptied first, so that
    what other tests in the same process read is read again here."""
    pytest.importorskip("fastapi")
    from own_page import PageClient

    from freesail.core.world import Scenario, World
    from freesail.ui.harbour import Harbour
    from freesail.ui.server import Driver, create_app

    global _opened
    monkeypatch.setenv("FREESAIL_SETTINGS", str(tmp_path / "settings.yaml"))
    monkeypatch.chdir(ROOT)
    saves = tmp_path / "saves"
    sys.addaudithook(_hook)  # once a process; it records only while _opened is a list
    _forget_what_the_game_has_read()
    _opened = []
    try:
        driver = Driver(World(seed=7, scenario=Scenario()))
        harbour = Harbour(driver, saves_dir=str(saves), started=False, game_url="http://x")
        app = create_app(driver, game="the downloads' truth", saves_dir=str(saves), harbour=harbour)
        with PageClient(app) as c:
            page = c.get("/harbour")
            assert page.status_code == 200
            for script in re.findall(r'src="(/client/[^"?]+)', page.text):
                c.get(script)
            assert c.get("/api/harbour/state").status_code == 200
            first = c.get("/api/harbour/catalogue").json()["first_game"]
            assert "first passage" in first["name"].lower()
            begun = c.post("/api/harbour/start", json={"scenario": first["path"]})
            assert begun.status_code == 200, begun.text
            game = c.get("/")
            for script in re.findall(r'src="(/client/[^"?]+)', game.text):
                c.get(script)
            tick = c.get("/api/state").json()["tick"]
            assert c.get("/api/ship").status_code == 200
            assert c.post("/api/driver", json={"action": "tick", "value": 60}).status_code == 200
            assert c.get("/api/state").json()["tick"] == tick + 60
            primer = c.get("/api/library", params={"topic": "primer 7"}).json()
            assert "first passage" in primer["text"].lower()
            assert c.get("/api/library/topics").status_code == 200
            assert c.get("/api/harbour/chart").status_code == 200
            assert (
                c.post("/api/driver", json={"action": "save", "value": "truth"}).status_code == 200
            )
            # a second game, on the chart of the Channel: its minute and its chart open the
            # charts' tiles (A first passage is in open water, and touches none)
            begun = c.post("/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml"})
            assert begun.status_code == 200, begun.text
            assert c.post("/api/driver", json={"action": "tick", "value": 60}).status_code == 200
            assert c.get("/api/chart").status_code == 200
        opened = list(_opened)
    finally:
        _opened = None
    assert (saves / "truth.json").is_file()
    shipped = set(bundle.game_files())
    under = {_source_of(r) for r in _under_root(opened)}
    missing = sorted(r for r in under if r not in shipped and not r.startswith(NOT_THE_GAMES))
    assert not missing, f"opened by the game and not in the downloads: {missing}"
    assert any(r.startswith("data/charts/tiles/") for r in under), "no chart tile was opened"
    assert any(r.startswith("docs/primer/") for r in under)


def test_truth_7_801_the_downloads_ship_the_game_by_its_rule_and_not_the_records():
    """Truth 7-801: the game's files a download ships are every file git tracks under
    freesail/, client/, data/ and docs/primer/ (every ship, scenario and chart, however
    many there are), README.md and the consent brief; and not the owner's consent records,
    the tests, the tools, the rest of the documents, nor any compiled file."""
    files = bundle.game_files()
    assert files == sorted(set(files))
    tracked_ships = sorted(p.as_posix() for p in Path(ROOT, "data", "ships").glob("*.yaml"))
    for ship in tracked_ships:
        assert Path(ship).relative_to(ROOT).as_posix() in files
    assert "freesail/__main__.py" in files and "client/harbour.html" in files
    assert "docs/agents/ConsentBrief.md" in files and "README.md" in files
    assert any(f.startswith("data/charts/tiles/") and f.endswith(".npz") for f in files)
    for f in files:
        assert f.split("/")[0] in ("freesail", "client", "data", "docs", "README.md"), f
        assert not f.startswith(("docs/agents/consent/", "tests/", "tools/")), f
        assert "__pycache__" not in f and not f.endswith(".pyc")
        assert (
            not f.startswith("docs/")
            or f.startswith("docs/primer/")
            or f == ("docs/agents/ConsentBrief.md")
        )


def _locked(path: Path) -> dict[str, list[str]]:
    """A lock file's packages, each with its hashes."""
    out: dict[str, list[str]] = {}
    name = ""
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^([A-Za-z0-9_.-]+)==([^ \\;]+)", line)
        if m:
            name = m.group(1).lower().replace("_", "-")
            out[name] = []
        for h in re.findall(r"--hash=sha256:([0-9a-f]{64})", line):
            out[name].append(h)
    return out


def test_truth_7_802_the_libraries_are_the_games_own_pinned_with_their_hashes():
    """Truth 7-802: each platform's lock file pins every library by version with its
    sha256, holds every one pyproject.toml names in its base and its server and agents
    extras, and none that only its `dev` extra names."""
    import tomllib

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

    def names(reqs: list[str]) -> set[str]:
        return {re.split(r"[<>=!~\[ ;]", r, maxsplit=1)[0].lower().replace("_", "-") for r in reqs}

    wanted = names(bundle.requirements())
    dev_only = names(project["optional-dependencies"]["dev"]) - wanted - {"freesail"}
    assert wanted >= names(project["dependencies"])
    for which, name in bundle.LOCK_FILES.items():
        locked = _locked(bundle.LOCKS / name)
        assert locked, which
        assert wanted <= set(locked), (which, wanted - set(locked))
        assert not dev_only & set(locked), (which, dev_only & set(locked))
        for package, hashes in locked.items():
            assert hashes, f"{which}: {package} has no hash"


def test_truth_7_803_every_third_party_is_pinned_and_every_action_by_its_commit():
    """Truth 7-803: every interpreter a download carries is pinned by version and sha256 at
    its maker's own place (python.org; python-build-standalone's releases); and every
    action the downloads' workflow and the gate's release use is pinned by a commit, not a
    tag; neither workflow is run by a pull request; each gives its token reading alone and
    writing only to its publishing job; nothing an outsider writes is spliced into a script
    of either; and no commit's message publishes anything."""
    for which, pin in bundle.INTERPRETERS.items():
        assert re.fullmatch(r"[0-9a-f]{64}", pin.sha256), which
        assert pin.url.startswith(
            (
                "https://www.python.org/ftp/python/",
                "https://github.com/astral-sh/python-build-standalone/releases/download/",
            )
        ), which
        assert pin.version.split("+")[0] in pin.url, which
    for name in ("downloads.yml", "release.yml"):
        text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
        uses = re.findall(r"uses:\s*([^\s#]+)", text)
        assert uses, name
        for u in uses:
            if u.startswith("./"):
                continue
            assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", u), f"{name}: {u}"
        assert "pull_request" not in text, name
        # the downloads' publishing job; the gate's release job, and its call of the downloads
        assert text.count("contents: write") == {"downloads.yml": 1, "release.yml": 2}[name], name
        assert "\npermissions:\n  contents: read\n" in text, name
        # nothing an outsider writes is put into a script as text: only through the environment
        for run in re.findall(r"run: \|\n((?:\s{10,}.*\n)+)", text):
            assert "${{" not in run, f"{name}: {run}"
    downloads = (ROOT / ".github" / "workflows" / "downloads.yml").read_text(encoding="utf-8")
    assert "persist-credentials: false" in downloads
    # a release is made by a hand or by a gate, never by the words of a commit
    assert "head_commit" not in downloads and "--draft" not in downloads
    release = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    jobs = "\n" + release.split("\njobs:\n", 1)[1]
    for job in ("lint", "checks"):
        part = jobs.split(f"\n  {job}:\n", 1)[1].split("\n\n  ", 1)[0]
        assert "permissions" not in part, job  # the workflow's reading alone
    assert "contents: write" in jobs.split("\n  release:\n", 1)[1]
    call = jobs.split("\n  downloads:\n", 1)[1].split("\n\n  ", 1)[0]
    assert "contents: write" in call and "uses: ./.github/workflows/downloads.yml" in call


def test_truth_7_804_the_launchers_and_the_start_here_pages_say_what_they_must():
    """Truth 7-804: each launcher runs the download's own interpreter by its own path,
    isolated (-I) and writing nothing (-B), passing its arguments on; the Windows one
    refuses kindly to start inside its zip, the Mac one clears its folder's quarantine.
    Each "start here" page says how to start, the warning its system gives the first time
    and how to pass it, what the player will see, how to stop, where the saves and
    settings live, and where to tell what went wrong; and of a model at a station only
    that it is optional and needs a key of his own."""
    cmd = (bundle.HERE / "FreeSail.cmd").read_text(encoding="utf-8")
    assert '"%HERE%python\\python.exe" -I -B -X utf8 -m freesail %*' in cmd
    assert "Extract All" in cmd and ":notunpacked" in cmd
    mac = (bundle.HERE / "FreeSail.command").read_text(encoding="utf-8")
    assert mac.startswith("#!/bin/bash\n")
    assert '"$PY" -I -B -X utf8 -m freesail "$@"' in mac
    assert "xattr -dr com.apple.quarantine" in mac
    assert "python-arm64/bin/python3.11" in mac and "python-x86_64/bin/python3.11" in mac
    for name, words in (
        (
            "START-HERE-windows.txt",
            [
                "Extract All",
                "Windows protected your PC",
                "Run anyway",
                "Ctrl+C",
                "%APPDATA%\\FreeSail",
                "A first passage",
                "issues",
            ],
        ),
        (
            "START-HERE-mac.txt",
            [
                "Control-click",
                "macOS cannot verify the developer",
                "Open Anyway",
                "Privacy & Security",
                "Control-C",
                "~/Library/Application Support/FreeSail",
                "A first passage",
                "issues",
            ],
        ),
    ):
        text = (bundle.HERE / name).read_text(encoding="utf-8")
        for w in words:
            assert w in text, (name, w)
        assert "Optional, and needs a key of your own; see the README" in text
        said = [ln for ln in text.splitlines() if re.search(r"\bmodel\b", ln, re.I)]
        assert said == ["A MODEL AT A STATION"], said
        assert len(text.splitlines()) <= 50, name  # a screen


def test_truth_7_805_from_a_download_the_consent_records_go_beside_the_settings(tmp_path):
    """Truth 7-805 (package 130; the lead's ruling, after the proposal's decision 31): with
    nothing naming a place, a seated model's consent record goes, from a download (its mark
    in the game's folder, which the assembling script writes), to `consent/` beside the
    player's settings and saves, so that nothing is written in the unpacked folder; from a
    checkout, to the game's own `docs/agents/consent/` as ever. (A setting, or
    `--consent-records`, still wins: they are given as `records_dir` and never reach this
    default.) The smoke test seats no model: this is the proof."""
    from freesail.agents import consent

    assert consent.DOWNLOAD_MARK == bundle.DOWNLOAD_MARK
    settings_file = tmp_path / "home" / "FreeSail" / "settings.yaml"
    checkout = tmp_path / "checkout"
    checkout.mkdir()
    assert consent.default_records_dir(checkout, settings_file) == (
        checkout / "docs" / "agents" / "consent"
    )
    download = tmp_path / "Free Sail ä" / "game"
    download.mkdir(parents=True)
    (download / consent.DOWNLOAD_MARK).write_text("mark", encoding="utf-8")
    assert consent.default_records_dir(download, settings_file) == settings_file.parent / "consent"
    # this checkout carries no mark: its default is unchanged
    assert not (ROOT / consent.DOWNLOAD_MARK).exists()
    assert consent.RECORDS_DIR == ROOT / "docs" / "agents" / "consent"
    assert bundle.DOWNLOAD_MARK not in bundle.game_files()


def test_truth_7_806_a_port_taken_is_said_in_a_plain_sentence_and_the_game_stops_as_before(
    tmp_path,
):
    """Truth 7-806 (package 130; the lead's word): when the game's port is already in use
    (a second start, or another program on it), `py -m freesail` says in one plain sentence
    that FreeSail seems to be running already, where to look, and that a second one wants
    `--port` and another number; and stops with the same exit as before (the server could
    not listen: uvicorn's own code). On a free port the sentence is not said."""
    import socket
    import subprocess

    from freesail.__main__ import port_taken_words

    held = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    held.bind(("127.0.0.1", 0))
    held.listen(1)
    port = held.getsockname()[1]
    try:
        words = port_taken_words("127.0.0.1", port)
        assert words and "FreeSail seems to be running already" in words
        assert f"http://localhost:{port}/harbour" in words and "--port" in words
        env = {**os.environ, "FREESAIL_SETTINGS": str(tmp_path / "settings.yaml")}
        run = subprocess.run(
            [sys.executable, "-m", "freesail", "--no-browser", "--port", str(port)],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=120,
        )
        assert words in run.stdout, run.stdout + run.stderr
        # the server's own exit when it cannot listen, as before (uvicorn's: 3 in its 0.54)
        assert run.returncode != 0, (run.returncode, run.stderr[-2000:])
    finally:
        held.close()
    free = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free.bind(("127.0.0.1", 0))
    port = free.getsockname()[1]
    free.close()
    assert port_taken_words("127.0.0.1", port) is None
