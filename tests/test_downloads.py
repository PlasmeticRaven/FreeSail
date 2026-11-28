"""The downloads for a machine without Python (package 130; tools/bundle.py, tools/bundle/,
.github/workflows/downloads.yml; docs/design/Report-Package130.md). Truths 7-800 to 7-809.

The downloads themselves are built and proven in the cloud, on Windows and on both kinds of
Mac (tools/bundle_smoke.py). What is held here, on every push, is what a forgetful change
would break before anyone unpacked a zip: that the game's files the downloads ship hold
everything the game opens (a file added to the game next month and missed by the packer
fails here, not on a friend's first evening), that the libraries are the game's own and
pinned, that every third party is pinned by checksum and every action by its commit, and
that the launchers and the "start here" pages say what they must.
"""

from __future__ import annotations

import hashlib
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


# What each lock file holds, by name: what `python tools/bundle.py lock` resolved from
# pyproject.toml's base, server and agents extras, and nothing more, held by the count of
# its names and the sha256 of them sorted, one a line. A change of a lock's set is a
# declared change of this truth (the failure lists the names the lock now holds), never
# one that passes unseen.
LOCKED_NAMES = {
    "windows": (62, "1bc53ea529ef83b2d6451031de16e6ea08ae2243fdc6232823db5d224674b620"),
    "arm64": (60, "c367ec6d961bc85be8f2a128aeac5fe13f73c15441ba8a8fb66e00bbe228c851"),
    "x86_64": (60, "c367ec6d961bc85be8f2a128aeac5fe13f73c15441ba8a8fb66e00bbe228c851"),
}


def _names_held(names: set[str]) -> tuple[int, str]:
    joined = "\n".join(sorted(names))
    return len(names), hashlib.sha256(joined.encode("utf-8")).hexdigest()


# A lock's requirement, whole: `name==version`, an environment marker at most, and its
# sha256 hashes; nothing else (no URL, no range, no extra, no option line).
_REQUIREMENT = re.compile(
    r"(?P<name>[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?)==(?P<version>[A-Za-z0-9.!+_-]+)"
    r"(?: ; [^\\-]+?)?(?P<hashes>(?: --hash=sha256:[0-9a-f]{64})+)"
)


def _lock_lines(text: str) -> list[str]:
    """A lock file's logical lines (a backslash at a line's end joins the next), spaces
    made single, without the comments and the blank lines."""
    joined = re.sub(r"\\[ \t]*\n", " ", text)
    lines = []
    for line in joined.splitlines():
        line = " ".join(line.split())
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def _locked(text: str) -> dict[str, list[str]]:
    """A lock file's packages, each with its hashes; a line that is not a whole requirement
    as `_REQUIREMENT` has it refused, by an AssertionError naming it."""
    out: dict[str, list[str]] = {}
    for line in _lock_lines(text):
        m = _REQUIREMENT.fullmatch(line)
        assert m, f"not a pinned requirement with its hashes: {line!r}"
        name = m.group("name").replace("_", "-").replace(".", "-")
        assert name not in out, f"twice: {name}"
        out[name] = re.findall(r"[0-9a-f]{64}", m.group("hashes"))
    return out


def test_truth_7_802_the_libraries_are_the_games_own_pinned_with_their_hashes():
    """Truth 7-802: each platform's lock file is nothing but requirements each pinned
    `name==version` with its sha256 hashes (no URL, no range, no option line, which pip
    would take under --require-hashes all the same); its names are exactly those resolved
    for it (62 for Windows, 60 for each Mac: no library more, none less); and they hold every
    one pyproject.toml names in its base and its server and agents extras, and none that
    only its `dev` extra names. The refusal is proven on the lines it must refuse."""
    import tomllib

    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]

    def names(reqs: list[str]) -> set[str]:
        return {re.split(r"[<>=!~\[ ;]", r, maxsplit=1)[0].lower().replace("_", "-") for r in reqs}

    wanted = names(bundle.requirements())
    dev_only = names(project["optional-dependencies"]["dev"]) - wanted - {"freesail"}
    assert wanted >= names(project["dependencies"])
    assert {k: v[0] for k, v in LOCKED_NAMES.items()} == {
        "windows": 62,
        "arm64": 60,
        "x86_64": 60,
    }
    for which, name in bundle.LOCK_FILES.items():
        text = (bundle.LOCKS / name).read_text(encoding="utf-8")
        locked = _locked(text)
        assert _names_held(set(locked)) == LOCKED_NAMES[which], (which, sorted(locked))
        assert wanted <= set(locked), (which, wanted - set(locked))
        assert not dev_only & set(locked), (which, dev_only & set(locked))
        for package, hashes in locked.items():
            assert hashes, f"{which}: {package} has no hash"
    h = "--hash=sha256:" + "0" * 64
    good = f"pyyaml==6.0.2 \\\n    {h}\n"
    assert _locked(good) == {"pyyaml": ["0" * 64]}
    for bad in (
        f"pyyaml @ https://example.org/PyYAML-6.0.2.whl {h}\n",
        f"pyyaml>=6.0 {h}\n",
        f"pyyaml==6.* {h}\n",
        f"pyyaml[extra]==6.0.2 {h}\n",
        "pyyaml==6.0.2\n",
        f"pyyaml==6.0.2 --hash=md5:{'0' * 32}\n",
        f"{good}--index-url https://example.org/simple\n",
        f"{good}--extra-index-url https://example.org/simple\n",
        f"{good}--find-links /somewhere\n",
        f"{good}-e .\n",
        f"{good}-r other.txt\n",
        f"{good}./a-local.whl {h}\n",
        f"pyyaml==6.0.2 ; python_version >= '3' --index-url https://example.org {h}\n",
    ):
        with pytest.raises(AssertionError):
            _locked(bad)


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
    refuses kindly to start inside its zip, the Mac one clears the quarantine of its four
    folders (the interpreters, the game, the licences) and of nothing else.
    Each "start here" page says how to start, the warning its system gives the first time
    and how to pass it, what the player will see, how to stop, where the saves and
    settings live, and where to tell what went wrong; and of a model at a station only
    that it is optional and needs a key of their own."""
    cmd = (bundle.HERE / "FreeSail.cmd").read_text(encoding="utf-8")
    assert '"%HERE%python\\python.exe" -I -B -X utf8 -m freesail %*' in cmd
    assert "Extract All" in cmd and ":notunpacked" in cmd
    # the one folder "Extract All" makes, by its name (the Windows zip holds no folder)
    assert "the folder FreeSail-{{NAME}}-windows" in cmd
    windows_page = (bundle.HERE / "START-HERE-windows.txt").read_text(encoding="utf-8")
    assert "It makes one folder, FreeSail-{{NAME}}-windows, and opens it" in windows_page
    # another tool's "Extract Here" would spill the zip's loose files: a folder of its own
    assert "unpack into a new folder of its\n     own" in windows_page
    assert '"Extract Here" spills them' in windows_page
    mac = (bundle.HERE / "FreeSail.command").read_text(encoding="utf-8")
    assert mac.startswith("#!/bin/bash\n")
    assert '"$PY" -I -B -X utf8 -m freesail "$@"' in mac
    # the quarantine cleared of the download's four folders, and of nothing else
    clearing = re.search(r"/usr/bin/xattr -dr com\.apple\.quarantine ((?:\\\n|[^\n])*)", mac)
    assert clearing, "the Mac launcher clears no quarantine"
    operands = clearing.group(1).replace("\\\n", " ").split()
    assert operands[-1] == "2>/dev/null", operands
    assert operands[:-1] == [
        '"$HERE/python-arm64"',
        '"$HERE/python-x86_64"',
        '"$HERE/game"',
        '"$HERE/licences"',
    ], operands
    assert mac.count("xattr") == 1 and mac.count("quarantine") == 1
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
    default.) And as `py -m freesail` works it out, the download's place follows the
    settings file in use, `--settings OTHER` too: beside OTHER, where the saves go. The
    smoke test seats no model: this is the proof."""
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
    # `py -m freesail`'s own road: from a download, beside the settings file IN USE (a
    # `--settings OTHER` too, as the saves are); a place the settings name wins; from a
    # checkout nothing is given, and the game's own place stands
    from freesail.__main__ import consent_records_place

    other = tmp_path / "elsewhere" / "other.yaml"
    assert consent_records_place({}, other, download) == str(other.parent / "consent")
    assert consent_records_place({"consent_records": "/r"}, other, download) == "/r"
    assert consent_records_place({}, other, checkout) is None
    assert consent_records_place({"consent_records": "/r"}, other, checkout) == "/r"


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


def test_truth_7_806_main_says_the_port_sentence_only_when_the_port_is_taken(
    tmp_path, monkeypatch, capsys
):
    """Truth 7-806, at `main`'s own level: `py -m freesail` on a free port says no word of
    it being taken, on a taken one says the sentence, and either way starts the server as
    before (uvicorn's run, held here); and a probe the machine cannot make (`--host ::1`
    without IPv6, errno 97) is no word and no error."""
    import socket

    import uvicorn

    import freesail.__main__ as entry

    ran: list[dict] = []
    monkeypatch.setattr(uvicorn, "run", lambda app, **kw: ran.append(kw))
    monkeypatch.setenv("FREESAIL_SETTINGS", str(tmp_path / "settings.yaml"))
    monkeypatch.chdir(ROOT)
    free = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free.bind(("127.0.0.1", 0))
    port = free.getsockname()[1]
    free.close()
    first = port
    assert entry.main(["--no-browser", "--port", str(port)]) == 0
    out = capsys.readouterr().out
    assert "seems to be running already" not in out and "FreeSail harbour" in out, out
    held = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    held.bind(("127.0.0.1", 0))
    held.listen(1)
    try:
        port = held.getsockname()[1]
        assert entry.main(["--no-browser", "--port", str(port)]) == 0
        out = capsys.readouterr().out
        assert entry.port_taken_words("127.0.0.1", port) in out, out
    finally:
        held.close()
    assert [kw["port"] for kw in ran] == [first, port]  # the server started, both times

    def no_family(*args, **kwargs):
        raise OSError(97, "Address family not supported by protocol")

    monkeypatch.setattr(socket, "socket", no_family)
    assert entry.port_taken_words("::1", 8000) is None


def _snapshot(top: Path) -> dict[str, bytes]:
    return {
        p.relative_to(top).as_posix(): (p.read_bytes() if p.is_file() else b"<folder>")
        for p in sorted(top.rglob("*"))
    }


@pytest.mark.parametrize("windows", [False, True])
def test_truth_7_807_the_teeth_take_out_every_guard_of_both_launchers(
    tmp_path, monkeypatch, windows
):
    """The poison check's teeth (the smoke test's `--without-isolation`) run each launcher
    with every guard against the poison taken out: `-I`, the `PYTHONNOUSERSITE` it sets (a
    second guard of the user site, which left in made the first teeth run on every system
    find no user-site mark) and, on Windows, the `._pth`; nothing else of the launcher is
    changed."""
    import bundle_smoke

    monkeypatch.setattr(bundle_smoke, "WINDOWS", windows)
    name = "FreeSail.cmd" if windows else "FreeSail.command"
    monkeypatch.setattr(bundle_smoke, "LAUNCHER", name)
    text = bundle._text(name, {"NAME": "t"}, crlf=windows)
    (tmp_path / name).write_bytes(text)
    if windows:
        (tmp_path / "python").mkdir()
        (tmp_path / "python" / "python311._pth").write_bytes(b"x")
    bundle_smoke.without_isolation(tmp_path)
    after = (tmp_path / name).read_bytes()
    assert b" -I -B " not in after and b"PYTHONNOUSERSITE=1" not in after
    assert b" -B -X utf8 -m freesail" in after
    assert not (tmp_path / "python" / "python311._pth").exists()
    guarded = [ln for ln in text.splitlines() if b" -I -B " in ln or b"PYTHONNOUSERSITE" in ln]
    assert len(guarded) == 2
    kept = [ln for ln in text.splitlines() if ln not in guarded]
    assert [ln for ln in after.splitlines() if ln in kept] == kept


# The variables a person's machine may hold, every one of which must stay out of the
# launcher's environment unless FROM_THE_MACHINE names it (truth 7-807).
_PERSONS = {
    "HOME": "/Users/a-person",
    "USERPROFILE": r"C:\Users\a-person",
    "APPDATA": r"C:\Users\a-person\AppData\Roaming",
    "LOCALAPPDATA": r"C:\Users\a-person\AppData\Local",
    "XDG_CONFIG_HOME": "/home/a-person/.config",
    "XDG_DATA_HOME": "/home/a-person/.local/share",
    "TEMP": r"C:\Users\a-person\AppData\Local\Temp",
    "TMP": r"C:\Users\a-person\AppData\Local\Temp",
    "TMPDIR": "/var/folders/a-person/T/",
    "FREESAIL_SETTINGS": "/Users/a-person/elsewhere/settings.yaml",
    "FREESAIL_ANYTHING": "a-person",
    "PATH": "/Users/a-person/bin:/usr/bin",
    "PYTHONPATH": "/Users/a-person/lib",
    "PYTHONUSERBASE": "/Users/a-person/.pybase",
    "HOMEDRIVE": "C:",
    "HOMEPATH": r"\Users\a-person",
    "USERNAME": "a-person",
    "SystemRoot": r"C:\Windows",
    "SystemDrive": "C:",
    "PROCESSOR_ARCHITECTURE": "AMD64",
    "NUMBER_OF_PROCESSORS": "4",
}


@pytest.mark.parametrize("system", ["windows", "mac", "linux"])
def test_truth_7_807_the_launchers_environment_is_built_from_nothing(tmp_path, monkeypatch, system):
    """Truth 7-807 (the reader's second finding 1a): the environment the smoke test gives
    the launcher is built from nothing by an allowlist, never the caller's less a few names.
    A pure function, tested here on every system's road: of a person's environment only
    FROM_THE_MACHINE's names come through (on Windows the system folder and the processor;
    on the Mac and elsewhere none); no FREESAIL_*, no home, no temporary folder, no PATH of
    the person's; every place of the player's lies in the test's home; and the process's own
    environment is never read."""
    import bundle_smoke

    home, work, named = tmp_path / "home", tmp_path, tmp_path / "named"
    machine = dict(_PERSONS)
    monkeypatch.setattr(bundle_smoke.os, "environ", {"FREESAIL_SETTINGS": "never read"})
    env = bundle_smoke.launcher_env(system, machine, home, work, named)
    assert machine == _PERSONS  # nothing of the caller's changed
    assert env == bundle_smoke.launcher_env(system, dict(_PERSONS), home, work, named)
    taken = set(bundle_smoke.FROM_THE_MACHINE[system])
    assert taken == (
        {"SystemRoot", "SystemDrive", "PROCESSOR_ARCHITECTURE", "NUMBER_OF_PROCESSORS"}
        if system == "windows"
        else set()
    )
    made = {
        "HOME",
        "USERPROFILE",
        "APPDATA",
        "LOCALAPPDATA",
        "XDG_CONFIG_HOME",
        "XDG_DATA_HOME",
        "PATH",
        "PYTHONPATH",
        "PYTHONHOME",
        "PYTHONSTARTUP",
    }
    made |= (
        {"windir", "ComSpec", "PATHEXT", "TEMP", "TMP"}
        if system == "windows"
        else {"TMPDIR", "LANG"}
    )
    assert set(env) == made | taken
    for name in taken:
        assert env[name] == _PERSONS[name]
    for name, value in env.items():
        if name not in taken:
            assert "a-person" not in value, (name, value)
    assert not any(k.upper().startswith("FREESAIL") for k in env)
    for name in (
        "HOME",
        "USERPROFILE",
        "APPDATA",
        "LOCALAPPDATA",
        "XDG_CONFIG_HOME",
        "XDG_DATA_HOME",
    ):
        assert Path(env[name]).is_relative_to(home), name
    for name in ("TEMP", "TMP", "TMPDIR"):
        if name in env:
            assert Path(env[name]).is_relative_to(work), name


def _trial_zip(path: Path, launcher: str) -> Path:
    import zipfile

    with zipfile.ZipFile(path, "w") as z:
        info = zipfile.ZipInfo("FreeSail-trial-mac/FreeSail.command")
        info.external_attr = 0o755 << 16
        z.writestr(info, launcher)
    return path


def _a_persons_home(tmp_path: Path, monkeypatch) -> Path:
    """A person's home with saves on every system's road, a settings file of their own
    named by FREESAIL_SETTINGS (whose saves lie beside it), and their home's variables set."""
    person = tmp_path / "a person's home"
    for saves in (
        person / ".config" / "freesail" / "saves",
        person / "Library" / "Application Support" / "FreeSail" / "saves",
        person / "AppData" / "Roaming" / "FreeSail" / "saves",
        person / "elsewhere" / "saves",
        person / "Free Sail Proof ä",
    ):
        saves.mkdir(parents=True)
        (saves / "precious.json").write_text("theirs", encoding="utf-8")
    (person / "elsewhere" / "settings.yaml").write_text("places: {}\n", encoding="utf-8")
    for name, value in {
        "HOME": person,
        "USERPROFILE": person,
        "APPDATA": person / "AppData" / "Roaming",
        "XDG_CONFIG_HOME": person / ".config",
        "FREESAIL_SETTINGS": person / "elsewhere" / "settings.yaml",
    }.items():
        monkeypatch.setenv(name, str(value))
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    return person


@pytest.mark.skipif(sys.platform.startswith("win"), reason="the trial's launcher is bash")
def test_truth_7_807_the_smoke_test_touches_nothing_of_a_persons(tmp_path, monkeypatch):
    """Truth 7-807 (the reader's findings 1 and 1a): the smoke test, run on a person's own
    machine, removes and writes nothing of theirs, a FREESAIL_SETTINGS of theirs set or not.
    Everything it writes lies in one temporary folder of its own, removed at its end: the
    game and Python are given a home inside it (the launcher sees HOME there), and the
    person's saves, on every system's road and beside the settings their FREESAIL_SETTINGS
    names, and a folder named as the old test's unpacking folder, are as they were. Run here
    on a trial zip whose launcher says the home it sees, writes a save where a
    FREESAIL_SETTINGS would send the game's (as the game does), and stops; and the script
    reads no person's place."""
    import bundle_smoke

    person = _a_persons_home(tmp_path, monkeypatch)
    seen = tmp_path / "the home the launcher saw.txt"
    temp = tmp_path / "temp"
    temp.mkdir()
    monkeypatch.setattr(bundle_smoke.tempfile, "tempdir", str(temp))
    trial = _trial_zip(
        tmp_path / "FreeSail-trial-mac.zip",
        "#!/bin/bash\n"
        f"echo \"$HOME\" > '{seen}'\n"
        'if [ -n "$FREESAIL_SETTINGS" ]; then\n'
        '  echo saved > "$(dirname "$FREESAIL_SETTINGS")/saves/smoke-proof.json"\n'
        "fi\n"
        "exit 1\n",
    )
    before = _snapshot(person)
    assert bundle_smoke.main([str(trial)]) == 1  # the trial's game never answers
    assert _snapshot(person) == before
    home = Path(seen.read_text(encoding="utf-8").strip())
    assert home.parent.parent == temp and home.name == "home", home
    assert list(temp.iterdir()) == []  # its folder removed
    source = Path(bundle_smoke.__file__).read_text(encoding="utf-8")
    assert "Path.home()" not in source and "expanduser" not in source
    assert 'environ["APPDATA"]' not in source and 'environ.get("APPDATA' not in source


@pytest.mark.skipif(sys.platform.startswith("win"), reason="the trial's launcher is bash")
@pytest.mark.parametrize("road", ["seen before the launcher", "begun after the look"])
def test_truth_7_807_the_smoke_test_never_drives_a_game_not_its_own(tmp_path, monkeypatch, road):
    """Truth 7-807 (the reader's finding 1b): with a person's own game already answering,
    the smoke test sends it not a single order. Seen before its launcher runs (on the port
    the test chose), the test stops there and its launcher never runs; begun between the
    look and the launch (the look fooled here), the test reads that what answers is not its
    own game (no settings of the test's) and stops before any order: the person's game is
    asked for its harbour page at most, and nothing is begun, saved or run on it."""
    import http.server
    import threading

    import bundle_smoke

    person = _a_persons_home(tmp_path, monkeypatch)
    asked: list[tuple[str, str]] = []

    class APersonsGame(http.server.BaseHTTPRequestHandler):
        def _answer(self):
            asked.append((self.command, self.path))
            body = b'<html><meta name="freesail-page" content="theirs"></html>'
            if self.path.startswith("/api/"):
                body = b'{"settings": {"path": "/Users/a-person/settings.yaml"}}'
            self.send_response(200)
            kind = "application/json" if self.path.startswith("/api/") else "text/html"
            self.send_header("content-type", kind)
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        do_GET = do_POST = _answer

        def log_message(self, *args):
            pass

    game = http.server.ThreadingHTTPServer(("127.0.0.1", 0), APersonsGame)
    threading.Thread(target=game.serve_forever, daemon=True).start()
    monkeypatch.setattr(bundle_smoke, "free_port", lambda: game.server_address[1])
    if road == "begun after the look":
        monkeypatch.setattr(bundle_smoke, "answers", lambda port: False)
    ran = tmp_path / "the launcher ran"
    temp = tmp_path / "temp"
    temp.mkdir()
    monkeypatch.setattr(bundle_smoke.tempfile, "tempdir", str(temp))
    trial = _trial_zip(
        tmp_path / "FreeSail-trial-mac.zip",
        f"#!/bin/bash\necho ran > '{ran}'\nsleep 20\n",
    )
    before = _snapshot(person)
    try:
        assert bundle_smoke.main([str(trial)]) == 1
    finally:
        game.shutdown()
    assert [m for m, _ in asked if m != "GET"] == []  # not one order
    assert {p for _, p in asked} <= {"/harbour"}
    if road == "seen before the launcher":
        assert asked == [] and not ran.exists()
    assert _snapshot(person) == before
    assert list(temp.iterdir()) == []


def test_truth_7_807_the_smoke_and_its_teeth_run_on_all_three_and_cannot_be_passed_over():
    """Truth 7-807 (the reader's 3a): the teeth cannot run outside the three machines, so
    what is held here is that the downloads workflow runs both the smoke test and its teeth
    (`--without-isolation`) on Windows, a Mac with Apple silicon and a Mac with Intel, and
    that neither can be passed over: no `continue-on-error` anywhere in the workflow, no
    `if:` on the smoke job or on either step, the matrix not cut short by a first failure,
    and publishing waiting on the smoke job."""
    import yaml

    text = (ROOT / ".github" / "workflows" / "downloads.yml").read_text(encoding="utf-8")
    assert "continue-on-error" not in text
    jobs = yaml.safe_load(text)["jobs"]
    smoke = jobs["smoke"]
    assert "if" not in smoke and smoke["needs"] == "build"
    assert smoke["strategy"]["fail-fast"] is False
    assert "exclude" not in smoke["strategy"]["matrix"]
    runners = sorted(row["runner"] for row in smoke["strategy"]["matrix"]["include"])
    assert runners == ["macos-15", "macos-15-intel", "windows-2025"]
    assert smoke["runs-on"] == "${{ matrix.runner }}"
    runs = [st for st in smoke["steps"] if "bundle_smoke.py" in st.get("run", "")]
    assert len(runs) == 2
    plain, teeth = runs
    assert "--without-isolation" not in plain["run"] and "--without-isolation" in teeth["run"]
    for st in runs:
        assert "if" not in st and "continue-on-error" not in st
        assert "|| true" not in st["run"] and "||" not in st["run"]
    assert "smoke" in jobs["publish"]["needs"]


def test_truth_7_808_the_build_ships_no_link_and_no_interpreter_baggage(tmp_path):
    """Truth 7-808 (the reader's findings 4a and 4d): (a) a symbolic link tracked among the
    game's files is refused by the build (a link would ship what it points at), and the
    same files without it are copied; (b) python-build-standalone's interpreter is
    stripped, before the lock file's libraries go in, of its own pip and setuptools (its
    site-packages, its console scripts, ensurepip's wheels) and of the compiled bytes it
    carries, its site-packages left with its README alone, and the rest of it kept."""
    import inspect
    import subprocess

    repo = tmp_path / "repo"
    (repo / "freesail").mkdir(parents=True)
    (repo / "data").mkdir()
    (repo / "freesail" / "__main__.py").write_text("print('the game')\n", encoding="utf-8")
    (repo / "data" / "a.yaml").write_text("a: 1\n", encoding="utf-8")
    (tmp_path / "secret.txt").write_text("not the game's\n", encoding="utf-8")
    (repo / "data" / "link.yaml").symlink_to(tmp_path / "secret.txt")
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
    with pytest.raises(SystemExit, match="symbolic link.*data/link.yaml"):
        bundle.copy_game(tmp_path / "top", repo, allow_changed=True)
    assert not (tmp_path / "top" / "game" / "data" / "a.yaml").exists()  # nothing copied
    subprocess.run(["git", "rm", "-q", "--cached", "data/link.yaml"], cwd=repo, check=True)
    (repo / "data" / "link.yaml").unlink()
    assert bundle.copy_game(tmp_path / "top", repo, allow_changed=True) == 2

    py = tmp_path / "python"
    lib = py / "lib" / "python3.11"
    site = lib / "site-packages"
    for rel in (
        "bin/python3.11",
        "bin/pip",
        "bin/pip3",
        "bin/pip3.11",
        "lib/python3.11/os.py",
        "lib/python3.11/encodings/__init__.py",
        "lib/python3.11/encodings/__pycache__/__init__.cpython-311.pyc",
        "lib/python3.11/ensurepip/__init__.py",
        "lib/python3.11/ensurepip/_bundled/pip-24.0-py3-none-any.whl",
        "lib/python3.11/site-packages/README.txt",
        "lib/python3.11/site-packages/distutils-precedence.pth",
        "lib/python3.11/site-packages/pip/__init__.py",
        "lib/python3.11/site-packages/pip-26.1.2.dist-info/METADATA",
        "lib/python3.11/site-packages/setuptools/__init__.py",
        "lib/python3.11/site-packages/_distutils_hack/__pycache__/__init__.cpython-311.pyc",
    ):
        (py / rel).parent.mkdir(parents=True, exist_ok=True)
        (py / rel).write_text(rel, encoding="utf-8")
    bundle.strip_interpreter(py)
    left = sorted(p.relative_to(py).as_posix() for p in py.rglob("*") if p.is_file())
    assert left == [
        "bin/python3.11",
        "lib/python3.11/encodings/__init__.py",
        "lib/python3.11/ensurepip/__init__.py",
        "lib/python3.11/os.py",
        "lib/python3.11/site-packages/README.txt",
    ], left
    assert [p.name for p in site.iterdir()] == ["README.txt"]
    assert not list(py.rglob("__pycache__")) and not (lib / "ensurepip" / "_bundled").exists()
    built = inspect.getsource(bundle.build_mac)
    assert built.index("strip_interpreter(py)") < built.index("install_dependencies(arch")


def test_truth_7_809_pip_installs_by_the_lock_alone_for_the_downloads_platform(
    tmp_path, monkeypatch
):
    """Truth 7-809 (the reader's finding 3e): the command the build runs pip by, read from
    tools/bundle.py itself, is exactly: isolated from the machine's pip configuration,
    into the download's folder, with no dependency of its own resolving (`--no-deps`),
    every artifact checked against the lock's hashes (`--require-hashes`), wheels alone
    (`--only-binary=:all:`), nothing compiled, for the download's platform tag (Windows'
    win_amd64; macosx_12_0_arm64 and macosx_12_0_x86_64, macOS 12 the oldest promised),
    CPython 3.11, from that platform's lock file alone. Any flag more or less is a declared
    change of this truth."""
    calls: list[list[str]] = []
    monkeypatch.setattr(bundle.subprocess, "run", lambda cmd, **kw: calls.append(cmd))
    tags = {"windows": "win_amd64", "arm64": "macosx_12_0_arm64", "x86_64": "macosx_12_0_x86_64"}
    assert bundle.PIP_PLATFORMS == tags
    for which in bundle.LOCK_FILES:
        bundle.install_dependencies(which, tmp_path / which)
    assert len(calls) == 3
    for which, cmd in zip(bundle.LOCK_FILES, calls, strict=True):
        assert cmd == [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--quiet",
            "--disable-pip-version-check",
            "--no-input",
            "--isolated",
            "--target",
            str(tmp_path / which),
            "--no-deps",
            "--require-hashes",
            "--only-binary=:all:",
            "--no-compile",
            "--platform",
            tags[which],
            "--python-version",
            "3.11",
            "--implementation",
            "cp",
            "-r",
            str(bundle.LOCKS / bundle.LOCK_FILES[which]),
        ], (which, cmd)
