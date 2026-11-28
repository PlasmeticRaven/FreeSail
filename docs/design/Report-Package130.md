# Package 130: the game on a machine without Python (Windows and Mac)

*The builder's design and report. The brief: `docs/dev/briefs/Brief-Package130.md`. The owner's word of 2026-11-27: "let's build it for Windows and Mac. I won't be able to test the Mac version myself, but that is alright."*

## What was wanted, and what there is

A player who has never heard of Python downloads one file, unpacks it, opens one thing, and the harbour is in his browser. There are now two downloads, built from any commit by the repository's own workflow:

- **`FreeSail-NAME-windows.zip`** (about 430 MB): Windows 10 and 11, 64-bit.
- **`FreeSail-NAME-mac.zip`** (about 505 MB): macOS 12 and later, Apple silicon and Intel in the one download.

Each unpacks to one folder holding, at its top, **one thing to open** (`FreeSail.cmd`, which Windows shows as "FreeSail", a Windows Command Script; `FreeSail.command` on the Mac, which Terminal runs on a double-click), the **"start here" page** (`START HERE.txt`), and beside them the game (`game/`), its own Python (`python/`; on the Mac `python-arm64/` and `python-x86_64/`) and the licences (`licences/`). Nothing of the game changed: the launcher runs `python -m freesail` with the folder's own interpreter, which opens the harbour as it always has.

The pieces in the repository:

| piece | what it is |
|---|---|
| `tools/bundle.py` | assembles each download from a checkout (`windows`, `mac`), lists the game's files it ships (`files`), and resolves the lock files again (`lock`) |
| `tools/bundle/` | the launchers, the two "start here" pages, the three lock files, and python-build-standalone's licence texts |
| `tools/bundle_smoke.py` | the smoke test of a built zip, on the system it is for |
| `.github/workflows/downloads.yml` | builds both, smoke-tests them on Windows and both Macs, and publishes a pre-release when asked |
| `.github/workflows/release.yml` | the gate's release, which now calls the above and attaches both downloads beside the project's zip |
| `tests/test_downloads.py` | truths 7-800 to 7-806, in the ordinary suite; a change to it runs the downloads workflow again |

## What the game opens, and so what ships

Measured with Python's audit hook on every file opened (the `open` event), in process: the server's app as `py -m freesail` makes it, the harbour's page, state and catalogue, *A first passage* begun from the catalogue's first game, the game's page, state and ship, sixty ticks, the primer's chapter 7 and the library's topics, the harbour's chart, a save, and a second game on the Channel's chart (*The tender*) with its minute and its chart (the first passage is in open water and opens none of the depth tiles; the tender opens them).

| under the repository | files opened | size |
|---|---|---|
| `freesail/` | 494 (its modules) | 17 MB with their bytecode |
| `data/` | about 660 (every scenario, ship, port, evolution and signal book the catalogue and a game read; the coast, features and overrides of the charts; nine depth tiles for the tender) | 15 MB |
| `docs/primer/` | 29 (the README and every chapter: the library lists them all) | 0.8 MB |
| `client/` | 15 | 0.6 MB |

Read as well, by the code's own paths: `docs/agents/ConsentBrief.md` when a model is seated, and `docs/agents/consent/` (the records). Nothing is written under the repository in that run; the save and its checkpoint go to the saves place.

So what ships is **a rule, not a list** (`bundle.game_files`): every file git tracks under `freesail/`, `client/`, `data/` and `docs/primer/`, and `README.md` and `docs/agents/ConsentBrief.md`. That is 3,307 files and 420 MB, of which the charts' tiles are 393 MB: a game in another region opens other tiles, so all of them ship. **Not shipped**: the owner's consent records (`docs/agents/consent/`, which carry the names of the models he has seated: a friend's model is asked its own consent), the tests, the tools and the rest of the documents. Truth 7-800 repeats the measurement on every push and fails if any file the game opened lies outside the rule, whatever `data/` holds; a ship, scenario or chart added to `data/` is inside the rule without anyone remembering it.

## The Windows road

- **The interpreter**: python.org's embeddable package, CPython **3.11.9** for amd64 (`python-3.11.9-embed-amd64.zip`, sha256 `009d6bf7e3b2ddca3d784fa09f90fe54336d5b60f0e0f305c37f400bf83cfd3b`). 3.11.9 is the last 3.11 python.org built for Windows; the line has been source-only since. It is the version the game is developed on (3.11), and the embeddable package is made to be carried inside another program's folder.
- **Nothing outside the folder is read.** The interpreter's `python311._pth` is rewritten to name the only places it imports from: `python311.zip`, its own folder, `Lib\site-packages` and `..\game`, and `import site` (so that the libraries' `.pth` files run: pywin32's, which the agents' extra brings on Windows, needs it). The presence of a `._pth` file makes Python ignore `PYTHONPATH`, `PYTHONHOME` and the registry; the launcher also passes `-I` (no user site-packages, no `PYTHON*` variables at all), `-B` (no `__pycache__` written beside the code) and `-X utf8`, and runs `python\python.exe` by its absolute path, never by the PATH. It clears the `PYTHON*` variables for anything the game starts (a door at a station) and sets `PYTHONDONTWRITEBYTECODE`, `PYTHONNOUSERSITE` and `PYTHONUTF8` for them.
- **The dependencies** are installed at the build, on Linux, for Windows: `pip install --target python\Lib\site-packages --platform win_amd64 --python-version 3.11 --implementation cp --only-binary=:all: --no-deps --require-hashes --no-compile -r tools/bundle/locks/windows-x86_64.txt`. Wheels only, each checked against the lock's sha256, no dependency resolved at the build, nothing compiled; pip's console scripts (which name the build machine's Python) are removed.
- **No precompiled bytecode** is shipped: compiling the game and its libraries in memory at each start costs about 1.5 s (measured), and shipping bytecode would double the file count of a zip a player unpacks with Explorer. `-B` keeps the folder unwritten.
- **The launcher, `FreeSail.cmd`**, titles its window "FreeSail", says in plain words that this window is the game's server and to keep it open, that the browser opens the harbour at `http://localhost:8000/harbour`, to begin with *A first passage*, how to stop (close the window, or Ctrl+C and Y to cmd's "Terminate batch job (Y/N)?"), and that the saves and settings are in `%APPDATA%\FreeSail` and survive a newer download. When the game stops it says so with its exit code, and waits for a key. Opened from inside the zip without unpacking (Explorer lets a zip be opened like a folder), it says to "Extract All" first instead of failing in Python's words. It passes its arguments on (`FreeSail.cmd --no-browser`, used by the smoke test).
- **What Windows says the first time.** Files unpacked by Explorer from a downloaded zip carry the "mark of the web", and a script with it from no known publisher meets one of two warnings, which the "start here" page names both of: Microsoft Defender SmartScreen's "Windows protected your PC" (*More info*, then *Run anyway*), or the older "Open File - Security Warning ... The publisher could not be verified. Are you sure you want to run this software?" (*Run*). **This part is from Microsoft's documented behaviour, not measured**: a cloud runner has no desktop to show a dialog in, and Expand-Archive does not pass the mark on. One risk is named and not built for: on a Windows 11 machine where **Smart App Control** is switched on (new installations, in its evaluation mode), unsigned DLLs (the libraries' `.pyd` files) can be refused; signing (below) is what removes it, and switching Smart App Control off is the player's only other road.

## The Mac road, and the two not taken

**Chosen: a relocatable Python carried in the download, the launcher clearing the quarantine on its own folder.**

- **The interpreters**: python.org builds no relocatable Python for macOS (only its `.pkg` installer, which installs into `/Library/Frameworks`), so they are python-build-standalone's CPython **3.11.15** (release 20260718), `aarch64-apple-darwin` and `x86_64-apple-darwin`, `install_only_stripped`, from the project's own GitHub releases (sha256 `b21dbc3f3e01932fcc3f0f4c51e5a7ef61888cb454d23eee6e8207c6f52d0b04` and `8ca3906ed23f4a8ab4ff8f02d61b15ecf62e6fa8b312cd59d1692df34e834a65`, as that release's SHA256SUMS gives them). They are the builds uv installs, made to be moved. Both go in the one download, about 40 MB each with their libraries, so that a friend need not know which Mac he has; the launcher picks by `uname -m`. The game is put on each interpreter's path by a one-line `.pth` file in its site-packages (`../../../../game`), which `-I` leaves working (it turns off the user's site, not the interpreter's own).
- **The libraries** come in as on Windows, for `macosx_12_0_arm64` and `macosx_12_0_x86_64` (pip accepts the older macOS tags under them; the arm64 wheels say 11.0), from a lock file per architecture. The Intel lock differs in one place: cryptography's wheels for Intel Macs stop at 48.0.1, so the lock is resolved wheels-only for each platform (`uv pip compile --only-binary :all: --python-platform ...`) and takes 48.0.1 there.
- **Gatekeeper.** A browser marks what it downloads with the `com.apple.quarantine` attribute, and the Mac's unpacker (Archive Utility, and Safari's own unzipping) passes the mark to every file it unpacks. A marked program from no identified developer is refused when it is first opened: on macOS 12 to 14 "“FreeSail.command” cannot be opened because it is from an unidentified developer" (or "... the developer cannot be verified"), passed by Control-click, *Open*, and *Open* in the box "macOS cannot verify the developer of “FreeSail.command”. Are you sure you want to open it?"; on macOS 15 and later "“FreeSail.command” Not Opened" ("Apple could not verify ... is free of malware"), passed by *Done*, then System Settings, Privacy & Security, *Open Anyway*, the password, and *Open Anyway* again. That is the one step, and it is the player's own decision. If nothing else were done, every marked executable and library the interpreter then loaded (the interpreter, and hundreds of `.so` files) would each meet Gatekeeper in turn. So the launcher's first act, once the player has let it run, is `xattr -dr com.apple.quarantine` on its own folder: the files are his, it needs no password, and it touches nothing outside the folder. The smoke test gives the zip the mark a browser gives, unpacks it with `ditto` (which passes the mark on as Archive Utility does), checks the files carry it, and checks the launcher cleared it.
- **The other prompt** a friend may meet: Terminal asking once whether it may access files in his Downloads (or Desktop, or Documents) folder, macOS's privacy rule for those folders. The page says to click OK.
- **Not taken, (b): the interpreter fetched at first start** by the launcher (curl, then the sha256 checked). curl's downloads carry no quarantine mark, so the clearing would not be needed, but the launcher itself is refused once all the same (it came by a browser), so the player's steps are no fewer; and it needs the network at the first start, and the one place the interpreter comes from to be up that evening. It saves 80 MB of download and costs a second way to fail.
- **Not taken, (c): the player's own Python 3.11 or later**, with a clear word if he has none. Most Macs have none (the `python3` Apple ships is a stub that offers to install the developer tools, and is 3.9). Installing python.org's is a second program to install, and the game's libraries would then need pip and the network: two obstacles, which the brief rules out.
- **A Linux download does not fall out for nothing**: it would want another interpreter, another lock file, and another runner in the smoke test. None is built; the README's two lines serve.

## Where the saves and settings live

The game already keeps them in the player's own folder (`freesail/settings.py`), outside the unpacked one, and the smoke test confirms the save lands there on each system:

- **Windows**: `%APPDATA%\FreeSail\settings.yaml`, the saves in `%APPDATA%\FreeSail\saves\` (on the runner `C:\Users\runneradmin\AppData\Roaming\FreeSail\saves\smoke-proof.json`).
- **macOS**: `~/Library/Application Support/FreeSail/settings.yaml`, the saves in `~/Library/Application Support/FreeSail/saves/`.

So a newer download is unpacked beside the old one and the old folder deleted, and nothing of his is lost. The **consent records** go there too (the lead's ruling, below): from a download, a seated model's record goes by default to `.../FreeSail/consent/`, beside the settings and the saves.

## The two changes to the game's behaviour

The package's only changes to the game's own code, each at the lead's word (2026-11-27):

1. **The consent records' default place, from a download** (`freesail/agents/consent.py`, `default_records_dir`; a comment in `freesail/settings.py`). The assembling script writes a mark into the download's game folder (`game/FROM-A-DOWNLOAD.txt`). Where the mark lies and nothing names a place, a seated model's consent record goes to `consent/` beside the player's settings file (`%APPDATA%\FreeSail\consent\`, `~/Library/Application Support/FreeSail/consent/`), after the proposal's decision 31 ("consent records belong to whoever runs the game"), so that nothing is written in the unpacked folder and a newer download loses no record. A setting of the player's, or `--consent-records`, still wins as before; from a checkout (no mark) the default stays `docs/agents/consent/`, where the owner's own records live; what is asked of a model, what is recorded and the brief's text are untouched; the launcher passes no flag. **The smoke test seats no model**, so its "nothing written in the unpacked folder" does not reach this road: truth 7-805 is the proof, of both cases.
2. **A port already taken** (`freesail/__main__.py`, `port_taken_words`): before the server starts, the port is tried as the server will bind it; if it is in use, one sentence is said, "FreeSail seems to be running already (or another program has port 8000): look for its other window, or open http://localhost:8000/harbour in your browser. To run a second one, start it with --port and another number." Then the server is started as before and stops as before when it cannot listen (uvicorn's own words and exit status, 3 in its 0.54). Words alone. Truth 7-806.

## The smoke test

`tools/bundle_smoke.py`, run by the runner's own Python as the harness, on Windows (`windows-2025`), a Mac with Apple silicon (`macos-15`) and a Mac with Intel (`macos-15-intel`), against the built zip downloaded from the build job:

1. The zip unpacked by the system's own tool (Expand-Archive; on the Mac `ditto`, after the zip is given a browser's quarantine mark) into a fresh folder named `Free Sail Proof ä` in the runner's home: a space and a letter outside English.
2. A digest of every file in it.
3. The game started by the launcher's own road (`cmd /c FreeSail.cmd --no-browser`; `/bin/bash FreeSail.command --no-browser`), with **the runner's Python hidden**: PATH cut to the system's own folders, and `PYTHONPATH`, `PYTHONHOME` and `PYTHONSTARTUP` pointed at a folder of poisoned modules (`yaml`, `numpy`, `fastapi`, `freesail`, `sitecustomize`, `usercustomize`, a startup file) each of which leaves a mark if anything imports it. A `PYTHONHOME` that was obeyed would also break the interpreter outright.
4. The server waited for; the harbour's page asked and its mark taken as a browser does; its state and catalogue; the catalogue's first game (*A first passage*) begun; the game's page and its scripts, its state and its ship; sixty ticks, a minute of the game's time; the primer's chapter 7; the harbour's chart; a save; then *The tender*, its minute (the depth tiles read) and its chart.
5. The running interpreter's path read from the system (Windows' process table; the Mac's `ps`): it must lie inside the unpacked folder. No poison's mark.
6. The game stopped as a player stops it (Ctrl+Break on Windows, which the server takes as Ctrl+C; Control-C on the Mac), and the launcher's own "FreeSail has stopped (exit code 0)" read; no traceback in the window.
7. No file in the unpacked folder new, changed or gone; the Mac's quarantine marks cleared; the save in the user's data folder.

Each finding is said in one `::notice::` annotation listing every check that passed, an `::error::` for each that failed with the game window's last lines, and a table in the job summary. The build job also builds both downloads twice and compares their bytes, and says each zip's size and sha256 in a notice.

## The workflows

`.github/workflows/downloads.yml` runs in three ways. **By hand**, "Run workflow" on any branch with a name typed: builds, smoke-tests, and publishes the pre-release `preview-NAME` (an earlier one of that name replaced), for handing to friends between gates. (GitHub offers "Run workflow" only for a workflow on the default branch, so this appears once the file is on the trunk.) **Called by the gate's release**, which attaches both downloads beside the project's zip once their smoke tests have passed. **On a push that changes the downloads' own files** (`tools/bundle.py`, `tools/bundle/**`, `tools/bundle_smoke.py`, the workflow): builds and smoke-tests, so that the macOS runners run when a download has changed and not on every push; a push whose head commit carries `[preview NAME]` also publishes, which is how the publishing was proven on this branch.

The build job's Python is setup-python's CPython 3.11.14 exactly (the harness's too): it runs pip and writes the zip, so it is pinned to a patch release rather than "3.11"; its download is setup-python's own (not checksummed by us), and every byte it puts in a zip is checked against a pin. The build refuses to start if the game's files in the checkout differ from the commit, and refuses a copy that is not a git checkout, so that a download said to be of a commit is that commit.

What a stranger's machine runs is pinned: each interpreter by version and sha256 (`bundle.INTERPRETERS`), each library by version and sha256 in its lock file and installed with `--require-hashes --no-deps --only-binary=:all:`, the locks resolved with nothing newer than two weeks before (`--exclude-newer 2026-11-13`); every action by its commit, with the tag beside it, in both workflows (release.yml's own `checkout@v4`, `setup-python@v5` and `action-gh-release@v2` are now pinned to those majors' present commits). No pull request runs either workflow, so no code of one runs with the token; the token is `contents: read` everywhere but the one publishing job, and checkouts keep no credentials. Text an outsider could write (a commit message, a typed name) reaches the scripts through the environment, never spliced into them, and a name is refused unless it is letters, figures, dots and dashes. The publish uses the `gh` command on the runner, deletes nothing but a `preview-` release (and its tag) of the same name, and two runs of one name publish one after the other. A typed run publishes a **pre-release** (public, for friends); a `[preview NAME]` push publishes a **draft** (not public), whose notes say it is a builder's proof and not a build for players.

**`release.yml`, line by line.** Nothing changed in it but the call to the downloads' workflow (a job `downloads`, the `release` job's `needs` and its attached files, one download step, a paragraph of its opening comment) and these pins, each the same major's commit as the tag resolved to on 2026-11-27:

| was | now |
|---|---|
| `actions/checkout@v4` (three times) | `actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4.4.0` |
| `actions/setup-python@v5` (twice) | `actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065 # v5.6.0` |
| `softprops/action-gh-release@v2` | `softprops/action-gh-release@3bb12739c298aeb8a4eeaf626c5b8d85266b0e65 # v2.6.2` |
| (new) | `actions/download-artifact@9000827ccba6bdab643e8b6fd33ac0654aef8333 # v8.0.2` |

The reader of the workflows found, in `release.yml` as it was before this package and left as it is (the lead's word: change nothing else in it), three things for whoever next touches it: the gate's name (typed, or the branch's) is spliced into its shell scripts as `${{ ... }}` rather than passed through the environment, so a branch named `gates/$(...)` would run a command; its `contents: write` is given to the whole workflow, so the lint and the suite's six shards (which install from PyPI unpinned) run with a token that can write, and their checkouts keep it; and a second run for a gate whose tag already exists updates that release in place.

## The licences

At the top of each download, `LICENCES.txt` says what it carries and where each licence lies, all under `licences/`: Python's (`licences/python/`: python.org's `LICENSE.txt` on Windows; on the Mac python-build-standalone's notices, those of CPython and of every library it is built with, taken from the full archive of the same release and kept in `tools/bundle/licences/python-build-standalone/`), and each library's, copied from its `.dist-info` (where pip keeps it, and where it stays too).

## The `agents` extra

It adds the MCP SDK (the desktop client's bridge), httpx (the local runner), gguf (a model file's header, for the context budget), the API door's SDK and keyring (its key from the system's credential store), and with them pydantic-settings, cryptography, pywin32 on Windows and their kin: about 35 MB unpacked. **It ships**, so that a friend who later wants a model at a station is not stopped by a Python he cannot add to. `dev` never ships.

## Signing and notarising: what each would cost, and remove

Nothing is built for either. **Windows**: an Authenticode code-signing certificate from a public authority costs roughly US$200 to $500 a year (since 2023 its key must live on a hardware token or a cloud signing service, which a workflow can use); Microsoft's own cloud signing service is cheaper (about $10 a month) where its eligibility rules admit an individual. A signed launcher and signed libraries replace "unknown publisher" by the owner's name, and satisfy Smart App Control; SmartScreen's "Windows protected your PC" still appears for a new publisher until enough downloads have built a reputation (an EV certificate no longer skips that). The launcher would need to become a small signed `.exe`, as a `.cmd` file cannot carry a signature. **Mac**: the Apple Developer Program costs US$99 a year; with a Developer ID certificate every executable and library in the download is signed and the zip notarised by Apple, and Gatekeeper then opens the download with only its ordinary "downloaded from the internet, are you sure?" box, with no Control-click, no System Settings and no clearing of the quarantine. It wants the launcher made into an `.app` (a `.command` cannot be notarised as an app) and a Mac in the workflow, which the cloud's runners are. Both are the owner's money and decisions; the figures are as of this writing and his to check.

## Truths 7-800 to 7-806

- **7-800** everything the game opens lies in what the downloads ship (the audit-hook measurement above, in process, about 14 s). It first empties the game's `functools` caches, so that a file another test in the same worker has read (the primer's pages, the charts' tiles) is opened again and seen: without that, the whole fast tier once found the primer unread.
- **7-801** the game's files ship by their rule (every ship, scenario and chart; the consent brief and the README), and not the owner's consent records, the tests, the tools, the other documents or any compiled file.
- **7-802** the libraries are the game's own (its base, `server` and `agents`, none of `dev`'s alone), each lock pinning every library by version with its sha256.
- **7-803** every interpreter pinned by version and sha256 at its maker's place; every action in both workflows by its commit; no pull request trigger; one job that may write; no outsider's text spliced into a script.
- **7-805** from a download the consent records' default place is beside the settings; from a checkout it is as before.
- **7-806** a port already taken is said in a plain sentence, and the game stops as before; a free port says nothing.
- **7-804** the launchers run the folder's own interpreter isolated and writing nothing, and the "start here" pages say each thing the brief asks, and of a model only that it is optional and needs a key of one's own.

## The cloud's runs

Read through the public API (`/actions/runs/<id>/jobs` and each job's annotations). The run that proved the downloads as they now are, at `14192b3` (the downloads' own files have not changed since; the hash reported carries the trunk merged in and this report, and its own run is named in the report to the lead):

**Run 46079578966**, all green:

- **build both downloads** (job 140775176775): `FreeSail-preview-pkg-130-windows.zip` 428 MB, sha256 `c606ea2c...d9773f`; `FreeSail-preview-pkg-130-mac.zip` 503 MB, sha256 `f4256b86...c09a5`; each built twice, the same bytes.
- **smoke test on Windows** (`windows-2025`, job 140775863655): 22 of 22. Unpacked to `C:\Users\runneradmin\Free Sail Proof ä\...` (10,294 entries); the server answered after 7 s; the harbour's page and its mark, its state, its first game *A first passage* begun, the game's page and ship, tick 0 to 60, the primer's chapter 7, the harbour's chart, *The tender*'s minute and chart; the game on `...\python\python.exe` inside the folder; no poison's mark; stopped (Ctrl+Break) with "FreeSail has stopped (exit code 3)", the server silent after, no traceback; nothing in the folder new, changed or gone; the save at `C:\Users\runneradmin\AppData\Roaming\FreeSail\saves\smoke-proof.json`. 79 s from the launcher to the stop.
- **smoke test on a Mac with Apple silicon** (`macos-15`, job 140775863564): 24 of 24. The unpacked files carried the quarantine mark (20,424 files); the game on `.../python-arm64/bin/python3.11`; stopped (Control-C) with "FreeSail has stopped (exit code 0)"; the quarantine cleared in the download's folders (the launcher, the two pages and the folder itself keep theirs); the save at `/Users/runner/Library/Application Support/FreeSail/saves/smoke-proof.json`. 21 s.
- **smoke test on a Mac with Intel** (`macos-15-intel`, job 140775863547): 24 of 24, as the other Mac, on `.../python-x86_64/bin/python3.11`. 51 s.
- **publish** (job 140777531662): the draft `preview-pkg-130`, "a builder's proof ... not a build for players".

**What the earlier runs found and mended**: the first (46072756789) was cancelled in the queue, superseded. The second (46073511628): setup-python has no 3.11.14 for Windows or the Mac (the harness now takes 3.11.9 there), and the publishing word matched the commit's own prose (now a line of its own, in small letters). The third (46075728015): on Windows the break ended the process with code 3 after the server's clean shutdown; on the Macs four files at the top kept their quarantine, as the launcher now means them to. The fourth (46078457483): the Macs green; on Windows Ctrl+C pressed in a console of the game's own lost the window's text and cmd's question to that console, and the game was not seen to stop.

**What is not proven in the cloud**, so that it is not taken as proven: the warnings each system gives a person on the first opening (a runner has no desktop; Windows' Expand-Archive passes no mark of the web), Smart App Control, Terminal's question about the Downloads folder, and on Windows the stop by Ctrl+C itself (the stop proven is the break, which the server takes the same way; the Mac's Control-C is proven). No person has yet tried the Mac download, which its page says.

## What is put to the lead, and to the owner

1. **Where a friend is told to report a fault**: the pages say "tell the person who sent you this download", or open an issue on the repository with a GitHub account. That is the owner's to word.
2. **The draft `preview-pkg-130`**, made on this branch to prove the publishing (not public): to be removed when the lead or the owner wishes.
3. **The lock files name the API door's library by its package name**, as `pyproject.toml` does: they cannot ship that door without it. No model's name is in them.
4. **`release.yml`'s three older faults** (above), for whoever next touches it.
