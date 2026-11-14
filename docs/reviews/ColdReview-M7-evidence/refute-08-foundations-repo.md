# Refuter 08: the foundations (spec-01) and the repository (code-10)

Second reader under `REFUTERS.md`, against `spec-01-M0-M4.md` and `code-10-tools-data-repo.md`.
HEAD read at 64b09bd; `git diff --stat 504a250 HEAD -- freesail client tools data tests .github
pyproject.toml docs/primer docs/agents docs/Tech* docs/DesignProposal.md` is empty, so every
line cited below is the commit under review. Nothing under `docs/dev/` opened (one count
below matched paths beginning `docs/dev/` without printing them). No test suite run, no test
run; each probe below ran a few seconds with `-B`, in `.../scratchpad/r8/` (outside the
repository). Spec-01's checkpoint unpickler (its no. 2) and the sim/driver boundary (its no. 5)
were tried by another reader and are not repeated.

| Finding | First reader | Verdict | My weight |
|---|---|---|---|
| S1 No sandbox for player Python; nothing in play runs it | high | STANDS IN PART | medium-high, as a missing level of the ladder; low, as security |
| S2 A game with a Python standing order does not replay | medium | STANDS IN PART | medium |
| S3 Topmen found by the first word of the mast's id | medium | REFUTED in the main, a small part stands | low |
| S4 Seven foundation truths strict xfail, truth 51 asserted unmet | medium | STANDS (counts); "silently" falls | low-medium |
| S5 Four of twenty-four pointers stale | medium (in no. 9) | STANDS IN PART | low |
| S6 A saved log is not a saved game across builds (spec-01 no. 3) | high | STANDS IN PART | medium |
| S7 The evolution catalogue is mostly code (no. 7) | medium | STANDS | low-medium |
| S8 Specs no longer the truth; long tail of open items (nos. 9, 10) | medium; low-medium | NOT TRIED beyond S5 | - |
| C1 CI ignores `docs/**`, `**.md` that the game serves and tests read | high | STANDS, and worse | medium |
| C2 Chart tiles: 359 MB binary in plain git, every rebuild a copy | high | STANDS IN PART | medium |
| C3 No schema; a misspelt optional key is silent | medium | STANDS IN PART | medium |
| C4 Release gate's pace tests within a few per cent of a cloud runner | medium | STANDS | low-medium |
| C5 Six hull regression tests can never run in CI | medium | STANDS IN PART | low |
| C6 Chart audit re-implements the tide blend | medium | STANDS | low-medium |
| C7 A plain (non-editable) install cannot find its data | medium | STANDS | low-medium |
| C8 `.mcp.json` tracked, Windows-only, a placeholder | medium | STANDS IN PART | low |
| C9 No licence file though pyproject declares MIT | medium | STANDS | medium |
| C10 Hand-run tools, tools twice | low | STANDS | low |
| C11 63 per cent of visible commits touch only documents | (in §4) | STANDS as a count; the inference falls | low |

---

## Spec-01

### S1. No sandbox for player Python; nothing in the game as played runs player Python

First reader: no sandbox, a rule body reaches the World, disk and network with no time limit,
the promise dropped. High, sure.

**What I did.** Read `freesail/standing/python_api.py` whole (330 lines) and DesignProposal
§2.2 (lines 51-64) and §4.5 (288-297). Searched every driver for a road by which a player or a
model hands the game Python:

- `grep -rn "python_api\|exec(\|eval(\|builtins\|__import__\|importlib\|run_path"` over
  `freesail client tools`: the only importers of `bind/at/when/every/order` are
  `tools/python_twin.py:31` and `tests/test_python_api.py:20-31`. `freesail/ui/console.py:447`
  imports only `restore_absent` (the placeholder for a saved Python rule, below). The one
  `importlib.import_module` in the game (`core/acts.py:496`) decodes an act's dataclass and
  refuses any module not under `freesail.` and any class that is not a dataclass.
- Console and server command lines (`console.py:1133-1188`, `server.py:1730-1791`): `--scenario`,
  `--standing-orders`, `--load` and the like; no script option. `--standing-orders` and the
  console's `read the standing orders from FILE` go to `read_standing_orders`
  (`console.py:140-151`), which reads text lines (`standing/book.py:306-319`) and submits each
  as an order through `world.submit`. A `.py` file named there would be read as order text and
  each line refused.
- Console commands: the parity list (`tests/test_parity.py:63-93`) has no Python command.
- Server and harbour routes (grep of `@app.`): `/api/order`, `/api/driver`, `/api/save`,
  `/api/harbour/scenario`, `/api/harbour/start` and the rest take words, settings or a scenario;
  none takes code. The scenario loader's `standing_orders:` is a list of `.orders` paths read by
  the same function (`world/scenarios.py:996-1002`).
- The agents' tools (`python3 -c "from freesail.agents import tools; print(sorted(tools.TOOLS))"`):
  answer, chart, hand_over, handover_note, journal, library, opt_out, read_journal, read_log,
  readings, shelve, ship_view, stand_by, stand_down, state, submit_order, truth, world_order.
  No code tool; the MCP server wraps these.

**Verdict: STANDS IN PART.** Confirmed plainly: **there is no road by which a player at the
console, the browser or the harbour, or a model through any door, gives the game Python.** The
fourth level of the ladder ("Scripts: Python against a documented API", proposal §2.2) exists
only as a library (`freesail.standing`) used by one demonstration tool and one test file. The
primer (`docs/primer/07-a-first-passage.md:406-423`) tells the player the rules "can be written
in Python, for a script", but the only way to run one is to write your own Python program that
builds and drives a World, i.e. to be the driver yourself. And even that library is not level 3
as the proposal means it: the body runs once at registration and only collects fixed order
texts (`python_api.py:36-46, 262-280`), so a Python rule is a level-2 rule written in Python
syntax; "computation on the readings at firing" is left to "milestone 6's sandbox"
(`python_api.py:44-45`), which no code builds (grep for `sandbox`: the two docstrings only).

What falls is the weight as a **security** finding. The proposal itself says the sandbox "is
not a security boundary against a hostile player on a shared server ... It is a boundary
against bugs and runaway loops" (DesignProposal.md:297). With no road for anyone's Python but
the programmer's own, an unrestricted body reaches nothing its author could not reach by
running Python on his own machine. The cost to the owner is a promised level of the game that
is not in the game, not an exposure. Weight medium-high as design (one of four ladder levels,
and the primer advertises it); low as security.

### S2. A game with a Python standing order does not replay

First reader: registration is never journaled, so the replay lacks the rule and its firings.
Medium, sure.

**What I did.** Probe `r1.py`: frigate, seed 7, 19:40 on 1 June 1805, `bind`, `make all sail`,
an `@at("sunset")` rule, 1,500 ticks; then `replay.replay(w.save(), ship_factory)`. Output:
journal `[[0, 'captain', 'make all sail']]`; original log has "Standing order 'night routine'
entered in the book" and "By standing order 'night routine': taking in the royals"; the replay
has neither; 81 events against 70. `replay()` raised nothing and the save carries no digest that
the replay road checks (`core/replay.py:504-523` puts a digest in the checkpoint's header only).

Probe `r2.py`: the same game, 300 ticks, `replay.save_to_file` (which writes a checkpoint by
default, `replay.py:68`), `unbind()`, then `replay.load`. Output: `how checkpoint`, book
`['night routine']`, and after 1,200 more ticks "By standing order 'night routine': taking in
the royals." The rule came back and fired, with no module imported.

**Verdict: STANDS IN PART.** On the replay road (no checkpoint, or `--until`, or an unreadable
checkpoint) the rule and every firing vanish and the log diverges without a word from
`replay()`; at the console and the agent REPL, `restore_python_rules` (`console.py:444-449`,
`agents/repl.py:379-384`) then lists the rule belayed with a notable "standing.absent" line, so
the player is told the rule is not loaded, but not that the replayed game differs from the one
he played. On the default road (save beside its checkpoint, same session's save) the game does
continue with the rule, firing. So "does not replay" is right for the replay and wrong for the
ordinary load. The same save therefore gives two different games depending on whether the
`.checkpoint` file is beside it (see "Found on the way", F1). Weight medium; as S1 says, only a
programmer driving the library can make such a save at all.

### S3. Topmen found by the first word of the mast's id; another rig "gets no topmen"

First reader: `crew/hands.py:104`, `runner.py:1110-1118`; a fourth mast or another id gets no
topmen of its own. Medium, sure.

**What I did.** Read `hands.py:96-115, 202-224, 263-290, 290-385`, `crew/model.py:25-50`,
`evolutions/runner.py:1105-1117`, `physics/strain.py:449`. Listed the masts and top stations of
all 18 ship files.

`preferred_stations` (`hands.py:203-222`): for `topmen`, it adds the mast's own top if
`TOP_OF_MAST` knows the word, **and then all three tops** (`for top in TOPS: add(top)`).
`request` and `_ranked` (`hands.py:304-336, 338-343`) **sort** the idle hands by `_tier`
(`:263-290`), they do not filter: a hand outside the preferred stations is tier 1, 3 or 5,
still taken. So a sail on a mast whose id begins with another word is worked by topmen from the
fore, main and mizzen tops in that order, and then by anyone fit. `strain.py:449` is the
wording of a warning only.

**Verdict: REFUTED in the main.** No rig "gets no topmen": it loses only the preference for its
own top. What stands, small: the three tops are fixed in the `Station` enum (`model.py:33-35`)
and the ship file's stations must be its values, so a fourth mast (a jigger) cannot have a top
of its own, and its work draws on the fore top first. Every ship file names its masts `fore`,
`main`, `mizzen` (the lugger's `mizen.mast` has no top station to miss). Weight low.

### S4. Seven foundation truths held as strict expected failures; one budget asserted unmet

First reader: truths 3, 11, 18, 24, 26, 28, 31 strict xfail, truth 51 asserted unmet; "the green
suite carries them silently". Medium, sure.

**What I did.** `grep -n xfail tests/test_known_truths.py`; read each mark and test at 283, 457,
719, 1054, 1132, 1251, 1374, and truth 51 at 2145-2183. (An eighth strict xfail, at 6036, is
truth 7b-100, a superseded M7b reading, outside the foundations.) Not run.

All seven are `xfail(strict=True)` as said. What each means for a player:

| Truth | What the game does instead | What a player meets |
|---|---|---|
| 3 (`:283`) | the schooner is fastest with the wind abeam, not on the broad reach | a schooner's best point of sailing is wrong; reaching pays too well |
| 11 (`:457`) | wearing loses about a tenth of a mile to leeward, not a quarter to a half | wearing is cheaper than at sea; clawing off a lee shore by wearing is too easy |
| 18 (`:719`) | the watch sets plain sail in 16.4 min (25-40 asked), all hands in 5.6 (12-20 asked) | sail is made two to three times faster than history; the ratio is right |
| 24 (`:1054`) | after yards braced sharper gain +0.17 kn / 0.9 deg, under the quarter knot or point | a fine trimming practice is barely rewarded |
| 26 (`:1132`) | bowlines gain about a third of a point, not half | the same, smaller |
| 28 (`:1251`) | lying a-try in 45 kn she drifts 1.6 kn on the hour's mean, 2.6 at most, not under 1.5 | in a gale she makes more leeway than she should; matters near a lee shore |
| 31 (`:1374`) | catharpins gain 0.7 deg, not a quarter point | barely felt |

Truth 51 (`:2147-2183`): the floor asserted is 500 ticks a second (`1000 x 0.5`), and
`assert TICKS_PER_SECOND_HEADLESS / OWNER_TO_BUILD_RATIO > BUILD_MACHINE_MEASURED` compares two
constants (1500 > 1000), so it states the budget is unmet and would fail only if someone wrote a
higher measurement in. For a player: fast time runs at well under the spec's 3,000 ticks a
second; at the owner's assumed 2,000 a week's passage (604,800 ticks) takes about five minutes
rather than three and a half, and at the build machine's 500 to 1,000, ten to twenty.

**Verdict: STANDS** for the counts and the meaning. "Silently" falls in part: each mark carries
its reason in words, pytest's summary line counts xfailed tests, and `strict=True` is there to
turn the suite red if the model is ever fixed, not to hold the code to failing. Four of the
seven (24, 26, 28, 31) are recorded in their marks as "Owner's ruling", accepted misses; the
three open model faults a player would notice are 3, 11 and 18. Weight low-medium.

### S5. Four of twenty-four pointers in the specifications name files that do not exist

**What I did.** `ls client/profile.js tests/test_loader.py tests/test_grammar.py`: all absent;
`client/shipview.js`, `tests/test_ship_loader.py`, `tests/test_orders.py` exist. Read
`TechnicalSpec-M0-M2.md:28-80, 105, 441, 517-521`. Spot-checked 14 of the names the reader says
hold (grep for each definition): all found.

**Verdict: STANDS IN PART.** The reviewer's wording ("four name files that do not exist") is not
what the first reader found: of the four that do not hold, two are files (one item naming
`profile.js`, one naming two test files: three files in all) and two are behaviours (the journal
keeps "weather" unresolved; the save keeps a path, not content hashes). The missing files are
renamed equivalents, not missing work. The first reader's own tally does not add up either: the
list of names said to hold (spec-01 §2) has about 29 entries, none of them the four that fail.
The layout also names `set_square_sail.yaml` and `take_in_square_sail.yaml`
(`M0-M2.md:69`), filed as `set_square.yaml` and `take_in_square.yaml`. Weight low.

### S6. A saved log is not a saved game across builds (spec-01 no. 3)

**What I did.** Read `core/world.py:30-83` (the fingerprint over every `freesail/**/*.py` and
every data file but the tiles) and `core/replay.py:28-41, 815-905` (`load_report`).

**Verdict: STANDS IN PART.** The log alone (the JSON save) is promised to replay only on the
build that wrote it, as said. But `load_report` reads **another build's checkpoint** and goes on
"under this build's rules" with a sentence saying so (`replay.py:866-875`), and
`tests/fixtures/saves/` keeps old builds' checkpoints as tests. So a save with its checkpoint is
a saved game across builds; what is lost across builds is the replay from the log, the
proposal's "a saved log is a saved game" (§3.2). That road is the pickle another reader has
already shown to run code. Weight medium.

### S7. The evolution catalogue is mostly code (spec-01 no. 7)

`ls data/evolutions | wc -l` 108; `grep -l "^script:"` 64; step lists 44; `wc -l
freesail/evolutions/*.py` 13,512. The 64 include every manoeuvre (tack, wear, boxhaul, heave to,
anchoring, mooring, fishing, damage repair). **STANDS.** The strongest defence holds in part:
M0-M2 §8.5 itself makes tack, wear and heave to scripts, since a manoeuvre steered by the ship's
state is not a fixed list of steps. But the proposal's "it is data, so it can be extended
without programming" (§2.2) is true only for routine sail work. Weight low-medium.

### S8. Specs not the truth; the open items (spec-01 nos. 9, 10)

NOT TRIED beyond S5: they are counts and judgements over four specifications, and the time went
to the findings named for the owner.

---

## Code-10

### C1. CI ignores `docs/**` and `**.md`, which the game serves and the tests read

**What I did.** Read `.github/workflows/ci.yml` whole (73 lines): `paths-ignore` `docs/**`,
`**.md`, `.gitignore`, `.mcp.json` on push and pull request (`:17-29`), with the comment giving
the reason: the first form spent "the account's free Actions minutes in a day" (`:3-6`).
Confirmed the game reads documents: `agents/tools.py:118` `PRIMER_DIR = ROOT / "docs" /
"primer"` (served to models by `library` and to the browser by `/api/library`,
`ui/server.py:41-44`); `agents/consent.py:141-142` the brief and the records directory, the
brief's sha256 written into every consent record (`consent.py:448-451, 566, 1277`) and pinned
for fixtures in tests (`tests/test_officer.py:1596, 1732`). `grep -rl` over `tests/*.py` for
`docs/primer|docs/design|docs/references|docs/agents|"docs"`: 78 test files.

**Verdict: STANDS, and it is worse than said.** Tests also read the project's working notes
under `docs/dev/`: `tests/test_practice.py:594-602` asserts headings and sentences in
`docs/dev/TuningNotes.md` and `docs/dev/M7-WorkPackages.md` (and in `docs/TechnicalSpec-M7.md`
and `docs/agents/Harness.md`). So the 195 visible commits that touch only `docs/dev/` (C11) can
break the suite with no run. One correction: a docs-only push does not "push green", it runs
nothing; whether a pull request with no run can merge depends on branch protection, which is
not in the tree. The defence (minutes are finite; the gate and the whole-suite run catch it
later) holds in part: a primer or brief edit that breaks a test is found at the next gate, not
when made. Weight medium.

### C2. The chart tiles: 359 MB of binary in plain git, every rebuild a permanent copy

**What I did.** `git ls-files -z data/charts/tiles | du -cb --files0-from=-`: 362,844,618
bytes in 2,325 files (all of `data/charts`: 370,775,753). `.gitattributes`: no LFS. `git
rev-list --objects --all -- data/charts/tiles | grep -c .npz`: 2,333 tile blobs reachable.
Per commit (`git show --name-only`, no messages read): the shallow root commit 8da908e carries
1,805 tiles; seven later commits 528 changes. `--name-status`: 2,325 A, 8 M; the rewritten
tiles are five (three of them three times), together about 1 MB.

**Verdict: STANDS IN PART.** The size and the absence of LFS stand: a clone carries some 360 MB
of tiles that git cannot compress. What falls is the churn: the "2,333 tile changes in the
visible week" are the shallow boundary's 1,805 plus 520 new tiles for new regions; only eight
rewrites of five tiles, about 1 MB, are true duplicates. Tiles are written with a fixed zip date
(build_charts.py, per the first reader) and checked against the manifest's sha256, so a rebuild
of an unchanged region writes identical bytes and adds nothing. Every new or changed region does
add permanently; the full history cannot be seen here. Weight medium.

### C3. No schema; a misspelt optional key in a port file silently takes its default

**What I did.** Read `world/ports.py:659-810`. Copied `data/ports/falmouth.yaml` to the
scratch directory, made `falmouth-typo.yaml` with `depth_fathoms:` misspelt `depth_fathom:` in
the mooring and `tracks:` misspelt `trakcs:`, and loaded both with the game's own
`load_port(path, load_chart("atlantic-east"))` (as `ui/harbour.py:438-445` does), under
`python3 -W error`:

```
tracks ['from_sea', 'in', 'to_sea'] -> []
outer_road depth 18.288 -> 18.288
anchorage depth 21.9456 -> 21.9456
mooring depth 5.4864 -> None
no warning raised
```

The port lost its three tracks (her ways in and out) and its mooring depth, with no word. Then
grepped the loaders for unknown-key refusals: `freesail/ship/schema.py` refuses unknown keys in
some eighteen places (the armament :1141, a fit :1169, a gun :1303, the quarter bill :1390, the
hold :1430, a boat :1455, gear :1515, ground tackle :1548, an anchor :1564, the profile :1667,
:1824, :1859, :2708, the crew section :2747, a role :2865, a flag post :2925, the ration :2942).
No other loader in `freesail/` does (grep for `which (it|a ...) does not take`); no test sweeps
the port files for unknown keys.

**Verdict: STANDS IN PART.** Confirmed by experiment for ports, and by reading for the other
`get(key, default)` loaders. The first reader's "the only unknown-key refusal ... is the ship
profile's" falls: ship files are refused on unknown keys in most of their sections (an unknown
hull key outside the profile is passed over, `schema.py:1658`). Ports, scenarios, captains,
people, evolutions: not refused (scenarios and evolutions not tried by experiment). Weight
medium: 121 hand-written port files, and a misspelt `tracks` breaks the pilot's way in without
a sign.

### C4. The release gate's pace tests sit within a few per cent of a cloud runner

**What I did.** Read `release.yml` (71 lines) and `whole-suite.yml` (128 lines) whole. Release:
`runs-on: ubuntu-latest` (`:29`), and in one step `pytest ... --slow -m "not pace"` then
`pytest --slow -m pace` (`:57-58`); a failure fails the step and nothing after it runs (zip,
tag, release). Whole-suite's pace job (`:103-110`): "informative, not gating ... a shared cloud
runner gives 480 to 520 where the build machine gives 580; the first run here failed the gate
day's floor by three ticks a second", `continue-on-error: true`. The pace tests
(`tests/conftest.py:648-657`, marks in four files) assert `BUILD_MACHINE_FLOOR` = 500
(`test_known_truths.py:2156-2163`).

**Verdict: STANDS.** A floor of 500 against a runner the project measured at 480 to 520 makes
the gate a toss on the pace step, and on a floating image (whole-suite pins `ubuntu-24.04` for
that reason, `:18-22`). The first reader's line numbers are wrong (`release.yml:102, 131` and
`whole-suite.yml:162-166, 247-254` do not exist; they are `:29, :58` and `:18-22, :103-106`:
the lines were counted down the three files run together). Cost to the owner: a re-run, or a
gate that will not tag. Weight low-medium.

### C5. Six hull regression tests can never run in the checks

**What I did.** Read `tests/test_hull_lugger.py:560-615`, `test_hull_frigate.py:474-520`; grep of
the six files for their skip and their pins. `git cat-file -e f5be9110`: "Not a valid object
name". `actions/checkout@v4` with no `fetch-depth` in all three workflows.

**Verdict: STANDS IN PART.** The six `git show f5be9110:...` comparisons skip in every CI run
and in this clone, as said. But each file keeps the hull's figures as filed in a constant that
always runs (`HULL_AS_FILED`, lugger :563-579, cutter :399-418; `FILED`, frigate :474, checked
before the skip at :500-503; `HULL_FIGURES`, schooner :446; smack and brig "the pins above hold
her figures", :598, :583). What is never checked in CI is the rest of the old document (spars,
sails, lines, groups, aliases) against the base commit; these are one-time step checks, and the
ships' polars and pinned passages would show a physics change. Weight low.

### C6. The chart audit re-implements the tide blend without the seam's taper

Read `tools/audit_chart.py:672-695` and `freesail/world/tide.py:480-500`. The audit weighs
`gauges_at(centre)` by inverse distance itself; the game, within a block's open edge, tapers
toward the eleven gauges (`taper_at`, `_taper`). **STANDS.** It is the audit's "other sea" share
that is off near a seam, not the game. Weight low-medium.

### C7. A plain (non-editable) install could not find its data

**What I did.** `pyproject.toml:35-36` packages `freesail*` only; no `package-data`, no
`MANIFEST.in`, no `setup.py`. Copied `freesail/` alone to `scratchpad/r8/site/` (as a wheel
would lay it out) and ran `python3 -I` against it: `freesail.__file__` the copy;
`port_files()` found 0 ports at `.../site/data/ports`; `make_world(1,
'data/ships/frigate-36.yaml')` raised `ShipFileError: no such ship file`. `ui/server.py:171`
finds the client at `parents[2] / "client"` in the same way.

**Verdict: STANDS.** The defence: every install line in `README.md` (`:12, :19, :25`) says
`pip install -e`, and the game is meant to run from a checkout, so the owner's road works.
It costs only if the game is ever published as a package. Weight low-medium.

### C8. `.mcp.json` tracked, Windows-only and a placeholder

Read it: `"command": "py"`, `--model-name "SET THE MODEL'S EXACT NAME HERE"`. In this session
the configured server failed for want of `py`. **STANDS IN PART:** the owner's platform is
Windows (README `:12`, "python3 in place of py off Windows"), and the harbour writes the clients'
entries itself (spec-01's M4 §24.6 row), so for the owner the file is redundant rather than
broken; off Windows it is a broken entry that loads itself in any code-client session opened
on the checkout. Weight low.

### C9. No licence file though the project declares one

`ls LICEN* COPYING*` at the root: none; `pyproject.toml:7` `license = { text = "MIT" }`;
`README.md` names no licence (grep). The gate zip is `git archive` of the tree
(`release.yml:59-62`). **STANDS.** MIT's one condition is that its notice, naming the holder,
goes with the code; there is no notice to go. Weight medium, for an owner who may publish.

### C10. Hand-run tools; tools twice

`grep` of `tests` and `.github` for `day_log`, `lesson_run`, `measure_loads`, `pace`,
`python_twin`: comments only (`test_known_truths.py:2815, 9277`, `test_bellerophon.py:2198`).
The pace loop: 11 + 1 + 1 + 1 copies in four test files. **STANDS.** Weight low.

### C11. 63 per cent of the commits visible touch only documents

**What I did.** `git log 504a250 --no-merges --format=@%H --name-only`, counted by path with no
message read: 338 non-merge commits (the shallow root among them), 214 touch only `docs/**` or
`*.md` (63%), 195 of those only `docs/dev/`; 48 touch `freesail/` or `client/`; 430 commits
with 92 merges. Then `git diff --numstat 8da908e 504a250` by area (lines added, the visible
week): `freesail` +5,816, `client` +203, `tests` +9,172, `data/ships` +5,721, `data/ports`
+6,074, `tools` +5,974; `docs/dev` +7,809, `docs/design` +1,358, `docs/primer` +108, the root
specifications +142.

**Verdict: STANDS as a count; the inference falls.** The first reader's "nearly two commits in
three ... changed only the project's notes about itself, against one in seven that changed the
game" is true by commit and misleading by work: by lines added over the same span the game's
code, tests, data and tools take some 33,000 against the notes' 9,400. The notes are many small
commits; the game is fewer large ones. Weight low.

---

## Found on the way

- **F1. One save, two games: a Python standing order survives a load from the checkpoint and
  is lost on a replay.** Probe `r2.py` (S2): saved with its checkpoint and loaded with no module
  bound, the rule is in the book, armed, and fires ("By standing order 'night routine': taking
  in the royals."). Probe `r1.py`: the same kind of save replayed from its log has no rule and
  no firing, and `restore_absent` lists it belayed. The module's docstring says a save loaded
  without the module "lists the rule in the book, belayed ... the rule runs again when its
  module is imported" (`python_api.py:47-53`): on the checkpoint road that is false, the rule
  runs with no module. Whether the player's game goes on as played thus turns on whether the
  `.checkpoint` file was copied with the save. Weight low-medium (only a programmer can make
  such a save); sure.
- **F2. The suite pins the project's working notes.** `tests/test_practice.py:591-602` reads
  `docs/dev/TuningNotes.md` and `docs/dev/M7-WorkPackages.md` and asserts their headings and
  sentences. A note edited, reworded or tidied breaks a test, and CI does not run on such an
  edit (C1). Weight low-medium; sure.
- **F3. The first reader's workflow line numbers are wrong** (C4): `release.yml` has 71 lines and
  `whole-suite.yml` 128; the cited `:102, :126, :131-135, :162-166, :220-245, :247-254` were
  counted down the three files run together. The facts cited are there; the lines are not.
  Weight low.

## What I did not do

- No test run, not even the seven xfails by node id: that they still fail is taken from
  `strict=True` and the reasons, not observed.
- Did not open later specifications (M5 onwards) to confirm the sandbox is dropped there; took
  the first reader's grep.
- Did not try scenarios, captains, people or evolutions with misspelt keys (ports only).
- Did not read `tools/build_charts.py` to confirm the fixed zip date (C2 takes the first
  reader's citation); did not see the full history (the clone is shallow).
- Branch protection and Actions history are not in the tree.
