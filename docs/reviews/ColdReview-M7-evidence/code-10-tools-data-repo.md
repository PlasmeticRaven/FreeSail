# Code reader 10: the repository as a thing, the tools, the data as a whole

Reader under the reviewer of package 114. Tree: `/home/user/FreeSail` at
504a25066c6995ce9829a19ffc597feb510a1870. **Note:** during this reading HEAD moved to
5d32478 by three commits that touch only `docs/reviews/ColdReview-M7-evidence/` (other
readers' evidence; `git diff --stat 504a250 HEAD -- freesail client tools data tests .github
pyproject.toml` is empty). Every count below is taken at 504a250 unless it says otherwise.

Rules kept: nothing under `docs/dev/` listed or opened (one file of it appeared in a
whole-tree `git ls-files | du` sort before I filtered it out; it is left out of every table
here); `docs/design`, `docs/playtests`, `docs/gates` listed by name and size only;
`docs/references/README.md` and `docs/references/images/README.md` read; no test suite run;
no `git log` subject or body read. The tools were run only for `--help` and for a few
seconds each where said.

---

## 1. The tools (tools/*.py, not gen_ships.py and not tools/ships/)

14 files, 7,719 lines (75% code, 8% comment, 8% docstring, measured with `ast`). There is no
`tools/__init__.py`, so tools are reached three ways: as scripts, as the namespace package
`tools.` (`from tools.check_signals import ...`, tests/test_signals.py:680, :691), and as
top-level modules after `sys.path.insert(0, ROOT / "tools")` (`import regatta as RG`,
tests/test_regatta.py:29; `import check_viewer_guns`, five test files) or by
`importlib.util.spec_from_file_location` (audit_chart, build_charts, chart_manifest). Every
tool's `--help` ran clean against the code as it is (exit 0, each under half a second; the
two without argparse were run outright, below). The package is installed editable here
(`import freesail` resolves to the checkout), which is why `measure_loads.py`, which does
not put the root on `sys.path`, works.

| Tool | Lines | For | Who runs it | Runs today | Duplicates |
|---|---|---|---|---|---|
| audit_chart.py | 1414 | sweeps the chart for water no region owns, seams, tide, weather boxes, streams, ports, marks, scenarios (checks a to h); a ratchet against `data/charts/audit-known.yaml` | tests/test_chart_audit.py (294 lines: sampled grid fast, full sweep slow), test_known_truths.py:16208; a person | yes: `--known` sampled ran in 38 s, 133 findings, 0 unlisted | re-implements the tide blend (below, 3.1); its own table of regions (`SEAS`, :106-134); `fmt` beside `geo.format_position`; tile span 1536/3600 written twice (:192, :272) |
| browser_probe.py | 622 | plays YAML plans at the real page in headless Chromium and marks each typed line ANSWERED/OTHER/UNSHOWN | tests/test_browser_probe.py (68 lines, slow); the `browser` job of whole-suite.yml:220-245 | `--help` yes (no browser run: long) | `chromium_path` copied in tests/test_pictures.py:139 and tests/test_harbour.py:468; `_free_port` in five places (tools/browser_probe.py:117, tests/test_pictures.py:72, test_harbour.py:334, test_mcp_server.py:991, test_known_truths.py:6603) |
| build_charts.py | 3099 | fetches GEBCO/EMODnet over the network, resamples with numpy, rasterises period overrides, writes `data/charts/` tiles, coast, index, manifest | a person with network (never CI); tests import its functions (test_chart.py:63, test_islands.py:41, test_tide.py:1210, test_known_truths.py:12419) | `--check channel-west` ran in 3 s and passed; no fetch tried (network forbidden) | `point_in_polygon` (:1858) beside `tide._point_in_polygon` (freesail/world/tide.py:254); `FATHOM_M`, `M_PER_SEC_LAT` (:95, :101) beside `freesail/units.py:28,30`; tile naming beside `chart.py:698`; the regions' bounds live here (`REGIONS`, :230) and again in the generated manifest, tied by tests for some regions only (test_chart.py:1500,1621,1772,1904; test_islands.py:86) |
| chart_manifest.py | 99 | prints the manifest's sources, licences, regions, attribution | tests/test_chart.py:657; a person | yes, 0.8 s, 62 lines | none of note |
| check_signals.py | 264 | checks every signal root: books, `does`, qualifiers, sources, flags drawn | tests/test_signals.py:680-691, test_flag_drawings.py:204, test_known_truths.py:14155 | yes, 2.7 s, all roots pass | hard-codes the engine's tables: `STATES`, `ANSWERS`, `QUALIFIERS` (:34-36, "what `signals._qualifiers` fills") and `declared_flags` (:155-188, a special case for `spain` at :180) |
| check_viewer_guns.py | 116 | checks each ship file's guns against the viewer's placing rule | tests/test_check_viewer_guns.py (70), test_neufchatel.py:700, test_bilander.py:972, test_bellerophon.py:638, test_viewer_action.py:141, test_known_truths.py:14229 | yes, 2.2 s, "clean" | none: it calls `freesail/api/viewer_guns.py` itself (sound) |
| climatology_check.py | 189 | runs N simulated months of weather and prints quarter shares against the study's table | test_known_truths.py:2324 (`run`, `table`); a person | yes (`--months 12`, 0.6 s) | `month_stream` (:337) copies `Rng.stream`'s hash (freesail/core/rng.py:23); the World seeds its weather from stream `"weather"` with `seed=self.seed` and a box (freesail/core/world.py:841-849), the tool from `"weather:{serial}"`, `seed*1000+serial`, no box: the "same named-stream rule" (docstring :265-271) is the hash only |
| context_budget.py | 352 | reads a local model file's header and prints the KV-cache bytes a token and the largest context that fits a graphics card | tests/test_context_budget.py (158); a person | `--help` yes | none in the game; it is not about the game at all (1.2) |
| day_log.py | 126 | runs a scenario and writes `tick kind text` and the digest, for diffing two machines | nobody automated (named only in a comment, test_known_truths.py:2815) | yes, 1.8 s for 3 minutes of game | nearly the same loop and print as lesson_run.py |
| lesson_run.py | 142 | runs a primer lesson with timed or triggered orders and prints the log and digest | nobody automated (no test names it) | yes, 5.8 s | nearly the same as day_log.py (scenario, `begin`, run, print, digest) |
| measure_loads.py | 137 | averages each part's load over rating at a set wind | nobody automated | yes, 1.2 s | `best_trim` (:271) is a second trim rule beside `freesail/evolutions/trim.py:254-271`; its `BEST_ALPHA_DEG = 35` "the square class's peak lift" (:268) is stale: `data/sail_classes.yaml:36-38` moved the square peak to 40 degrees in milestone 3b (and the same file's header, :28, still says 35) |
| pace.py | 225 | ticks a second in seven measures | nobody automated (named in comments, test_known_truths.py:9277, test_bellerophon.py:2198) | `--help` yes | the "best of three thousands" loop is copied 14 times in tests (`grep -c "best = max(best, 1000 / (time.perf_counter() - t0))"`: test_known_truths 11, test_bellerophon, test_crews, test_knowledge 1 each); `sys.path.insert(0, os.getcwd())` (:33) works only from the root or installed |
| python_twin.py | 78 | a demonstration that a standing order in the dialect and in Python give one log | nobody (no argparse; "a demonstration, not a test", :12) | yes, 7.6 s, "same log after the order: True" | duplicates test_python_api.py's truth 40 by its own account (:12-13); the demo's "make all sail" sets no studding sails, so the rule it shows fires on nothing ("already furled", its own output) |
| regatta.py | 856 | a course, an agent (rules, fake, local model, hosted model, replay), a judge and a score; writes rows and a table | tests/test_regatta.py (444); a person | `--help` yes | its own flat-plane geometry for rounding marks (`_local_nm`, :247) beside `freesail/world/geo.py`; its own run loop (`_sail`, :469) and a second one for doors (:571-587); hosts the game through `fastapi.testclient.TestClient` (:512), a test utility, in a shipped tool |

### 1.1 Findings on the tools

- **T1. Five tools (708 lines) are run by nothing but a person:** day_log, lesson_run,
  measure_loads, pace, python_twin. Grep of tests/, .github/ for their module names finds
  only comments. They run today, but nothing will tell anyone when one stops. Weight low;
  confidence sure.
- **T2. The chart audit re-implements the tide blend rather than asking for it, and leaves
  out the seam's taper.** tools/audit_chart.py:680-691 computes the gauges' weights itself
  (`1.0 / max(d, T.GAUGE_FLOOR_M) ** tide.power` over `tide.gauges_at(centre)` within
  `tide.reach_m`); the game's blend is `Tide._blend` (freesail/world/tide.py:508-535) and
  then, within a block's open edge, a taper toward the eleven gauges
  (tide.py:484-498). The audit's "other sea" share is therefore not the game's near a seam.
  The docstring claims the tool uses "the game's own readers ... and nothing of its own but
  the arithmetic" (audit_chart.py:7-10): this is more than arithmetic. Joining: expose the
  weights from `_blend` and read them. Weight medium (the ratchet can bless or miss a seam
  fault); confidence likely.
- **T3. The audit reaches into private game functions:** `T._point_in_polygon`
  (audit_chart.py:844), `freesail.world.brains._plan_of_legs` and `Planner._port_track`
  (:1105-1108). A rename in the game breaks the slow tier's audit, not the game. Weight low;
  sure.
- **T4. The audit's ratchet holds 142 accepted chart faults** (`grep -c "key:"
  data/charts/audit-known.yaml`); the sampled run found 133 of them, 59 of them against the
  ports (check f: a road or anchorage on dry ground, depths off, ways in crossing land). The
  ratchet stops new faults; nothing in the repository drives the known list down. Weight
  medium; sure (counts), likely (that they stand unaddressed).
- **T5. check_signals.py holds a copy of the engine's vocabularies** (`STATES`, `ANSWERS`,
  `QUALIFIERS`, `DESIGN_ORDERS`, :33-46) instead of importing them; a state added to the
  captain and not here is reported as a data fault. Weight low; likely.
- **T6. day_log.py and lesson_run.py are one tool twice.** Both: `load_scenario`,
  `make_scenario_world`, `begin`, tick, print each event, print the digest
  (day_log.py:517-555; lesson_run.py:377-431). They differ in the line format (`e.text` in
  day_log, `e.line()` in lesson_run), so their outputs cannot be diffed against each other.
  Weight low; sure.
- **T7. measure_loads' trim is not the game's.** `best_trim` (measure_loads.py:271-280)
  braces every yard to 35 degrees of attack, "which is what package 13's `trim` order does"
  (:249); the game's square peak is 40 degrees (data/sail_classes.yaml:36-38). The tool
  sized the spars' `SUSTAINED_FRACTION` (tools/gen_ships.py:96,149), so that number was
  measured against a trim the game no longer uses. Weight low to medium; likely.
- **T8. regatta.py writes into the project's records by default**: `RUNS_DIR =
  REPO_ROOT / "docs" / "playtests" / "regatta"` (:73) and `--out` defaults to it (:783). A
  casual run from a checkout dirties `docs/playtests/`. Weight low; sure.
- **T9. context_budget.py is outside the game.** 352 lines and a dependency (`gguf`, in the
  `agents` extra, pyproject.toml:29) to size a local model's context on a graphics card,
  defaulting to one model of card (context_budget.py:66, "a 4090"). It is tested (158 lines).
  It is scope grown at the edge, not a fault of the game. Weight low; sure.
- **T10. Docstrings tell a newcomer to run `py tools/X.py`** (the Windows launcher:
  day_log.py:7, lesson_run.py:5, pace.py:8, python_twin.py:4, regatta.py:4,
  context_budget.py:5); off Windows `py` does not exist (this machine: the MCP server below
  failed for exactly that). Comments in the tools cite `docs/dev/` and packages by number
  (`grep -c "package [0-9]"`: build_charts.py 107, pace.py 8); build_charts' recipe block
  (:182-399) is mostly history ("package 93 took it out"). Weight low; sure.

## 2. The data

### 2.1 Measured (tracked, at 504a250; `find`, `du -sb`, `git ls-files`)

| Directory | Files | Bytes | Kinds | Loaded by (game unless said) |
|---|---|---|---|---|
| data/charts | 2,398 | 370,775,753 | 2,325 npz, 33 yaml, 20 json, 20 geojson | freesail/world/chart.py:85 (tiles, coast, features, index, manifest), tide.py:133 (manifest again), client/map.js (coast); `audit-known.yaml` and `unverified-checks.yaml` by tools and tests only |
| data/ships | 18 | 1,358,011 | yaml | freesail/ship/loader.py via callers; ui/harbour.py:82 |
| data/ports | 121 | 800,429 | yaml | freesail/world/ports.py:131 |
| data/signals | 52 | 535,541 | yaml (6 roots) | freesail/world/signals.py:68, flags.py |
| data/scenarios | 73 | 296,122 | 52 yaml, 21 orders | freesail/world/scenarios.py; ui/harbour.py:80 |
| data/captains | 11 | 277,400 | yaml | freesail/world/captains.py:107, hail.py:52 |
| data/evolutions | 108 | 259,736 | yaml | freesail/evolutions/registry.py:78 |
| data/tides | 3 | 214,575 | yaml | freesail/world/tide.py:98 |
| data/weather | 1 | 201,919 | yaml | freesail/world/weather.py:410 |
| data/people | 12 | 86,588 | yaml | freesail/world/people.py:89 |
| data/director | 7 | 37,745 | yaml | freesail/agents/director.py:120, world/orders.py:2640 |
| data/fishing | 3 | 19,842 | yaml | freesail/world/fishing.py:64 |
| data/crew | 3 | 16,023 | yaml | freesail/crew/muster.py:46, crew/victuals.py:53, world/needs.py:63 |
| data/standing_orders | 2 | 11,952 | orders | ui/console.py:156, ui/harbour.py:81, agents/tools.py:3156; `fighting.orders` by two scenarios |
| data/squadrons | 3 | 11,259 | yaml | freesail/world/squadrons.py:60 |
| data/regatta | 3 | 6,299 | yaml | **tools/regatta.py and tests/test_regatta.py only; nothing in freesail/ or client/** |
| data/papers | 1 | 4,773 | yaml | freesail/world/places.py:63 |
| six files at data/ | 6 | (small) | yaml | business.py:57, nations.py:33,48, regimes.py:26, physics/sails.py:112, orders/vocabulary.py:20 |

Outside the charts the data is 78,847 lines of YAML and orders. A sweep of every scenario,
ship, people, regatta, brief and squadron file by its stem across code, tests, tools and data
found none referenced by nothing (each is named somewhere, or loaded by a directory glob).
Sound, one line: there is no dead data file I could find.

- **D1. The data root is computed 25 times.** `grep -rn '^[A-Z_]* *=.*"data"' freesail`
  gives 25 module constants of the form `Path(__file__).resolve().parents[2] / "data" / ...`
  (e.g. world/ports.py:131, world/chart.py:85, crew/muster.py:46), two of them relative to
  the working directory instead (`ui/console.py:156` `"data/standing_orders/starter.orders"`,
  `agents/model.py:41` `DATA = "data"`). pyproject.toml:35-36 packages only `freesail*`, so
  `data/` (and `docs/primer`, read by the game, below) is not package data: a plain
  `pip install .` (not `-e`) gives a game that cannot find its ships. Weight medium; sure
  (config), likely (effect; not tried, no install allowed).
- **D2. No schema for the YAML; a typo in an optional key is silent.** There is no
  jsonschema, pydantic or the like (grep of freesail/ and pyproject.toml). Loaders read with
  `doc.get(key, default)`. In a port file (freesail/world/ports.py:663-770): a misspelt
  `outer_road`, `anchorage`, `mooring` or `shore` raises a `ValueError` naming the file
  (:691-697), good; a misspelt `reach_nm` takes `IN_PORT_NM` (:738), `depth_fathoms` drops the
  file's depth (:701), `comes_off_by_night` becomes false (:785), `cutter` becomes the
  default cutter (:786), `tracks`, `places`, `blockade_station`, `tide` become empty, all
  without a word. The only unknown-key refusal I found is the ship profile's
  (tests/test_profile.py:244). The chart audit's check f catches a port whose spots are off
  the water, not one whose options are misspelt. Weight medium (121 port files, 108
  evolutions, hand-written); sure.
- **D3. data/charts: what it is and whether it can be rebuilt.**
  - Generated by tools/build_charts.py (reproducible given the network and the services):
    2,325 `.npz` tiles (`tiles/2` 288 MB in 1,587 files; `tiles/3` 53 MB in 684;
    `tiles/1` 11 MB in 54: the Atlantic corridor and its southern layer), 20 coast
    `.geojson` (5.9 MB), 20 feature `.index.json`, `manifest.yaml` (398 KB). A tile holds
    `elevation` int16 512x512, `dist` uint16, `overridden` bool, and scalars (checked on
    `tiles/2/101472_-48960.npz`). The manifest records each fetched source's URL, date,
    sha256 and bytes (40 EMODnet subsets, 23 GEBCO extracts); tiles are written with a fixed
    zip date (build_charts.py:1486) and tests check their sha256 against the manifest
    (tests/test_chart.py:1070). A rebuild depends on GEBCO's queue API, CEDA's archive and
    EMODnet's ERDDAP still serving the same bytes (build_charts.py:955-960); I could not
    test it.
  - Hand-made, irreplaceable if lost: `features/*.yaml` (20 files, 1,927 features; the
    index files agree with them today, checked), `overrides/**` (10 period sheets, 55 KB),
    `audit-known.yaml` (36 KB), `unverified-checks.yaml` (13 KB).
  - What it does to a clone: 91% of the tracked bytes of `data/` and 61% of the checkout's
    tracked bytes outside `docs/dev`; npz is already compressed, so git cannot shrink it.
    In the visible (shallow) history 9 commits touched `data/charts/tiles`, 2,333 file
    changes, some tiles three times (`git log --format= --name-only -- data/charts/tiles |
    sort | uniq -c`): every rebuild adds a new copy of each tile it touches to `.git`
    forever. No LFS (.gitattributes has none). Weight high for the repository's future (each
    region rebuilt is tens of MB of permanent history); sure.
- **D4. The regions' bounds and names are written in three places**: `REGIONS` in
  tools/build_charts.py:230 (the recipe), `regions:` in data/charts/manifest.yaml
  (generated), and `SEAS` in tools/audit_chart.py:106-134 (each region's sea, by hand; a
  missing one is reported, `c-no-sea`). Tests tie recipe to manifest for some regions only
  (above). Weight low; sure.
- **D5. A generated index is committed beside its source and the game reads the index**
  (freesail/world/chart.py:1090-1101). The audit's own comment says "an index not rebuilt
  from its file lacks some" (audit_chart.py:1138). They agree today; I found no test that
  rebuilds and compares. Weight low; likely.
- **D6. Stale numbers in data comments**: data/sail_classes.yaml:28 says the square sail
  peaks "at 35 degrees" and :36-38 says it was moved to 40. Weight low; sure.

## 3. The repository

### 3.1 Size

- This clone is **shallow** (`git rev-parse --is-shallow-repository` true); the oldest commit
  visible is 2026-11-08. `.git` is 429 MB (one pack, 427.44 MiB, 7,574 objects); the
  checkout (without `.git`) is 639 MB. The full history's size cannot be inferred from this
  and I do not.
- Tracked: 3,962 files. By top directory (tracked bytes; `docs` without `docs/dev`, which I
  did not measure): data 375.1 MB (2,825 files), docs 216.0 MB (685), tests 9.35 MB (203),
  freesail 7.43 MB (179), tools 1.81 MB (30), client 0.46 MB (13), .github 10.7 KB (3).
- `freesail.egg-info/` is **not tracked** (`git ls-files freesail.egg-info` empty;
  `.gitignore` has `*.egg-info/`): an artefact of the editable install, harmless.
- `CHANGES-m5c-c.md` (66.5 KB) **is tracked** at the root. Its first lines call it a working
  copy's note of gate m5c's follow-ups ("local work: no commits are made here"). It is cited
  by two tests' comments (tests/test_known_truths.py:4318, tests/test_checkpoint.py:157) as
  the source of facts, so a record has been left in the root and tests point at it. Weight
  low; sure.
- **No licence file.** pyproject.toml:7 declares `license = { text = "MIT" }`; `git
  ls-files | grep -i licen` finds only the chart sources' licences under
  `docs/references/licences/`. The gate zip (release.yml:132-135) therefore ships code that
  says MIT nowhere but in pyproject. Weight medium (for an owner who may publish); sure.

### 3.2 The largest 40 tracked files (outside docs/dev)

101.5 MB together, every one of them under `docs/`: 16 are game saves under
`docs/playtests/` (the largest 10.41 MB,
`docs/playtests/2026-10-18-to-22-owner-playtests-and-review/saves/2026-10-20-western-islands-run-H-final.json`;
others 3.47, 3.44, 3.34, 3.26, 3.26, 3.24, 2.89, 2.49, 2.47, 2.47, 2.42, 1.95, 1.75 MB), one
is a 2.01 MB extraction of a save as Markdown under `docs/playtests/.../work/`, and 23 are
OCR texts under `docs/references/` (the largest the three Niles registers, 5.54, 4.94,
3.76 MB; then pilots, James's naval history in five volumes, Roeding, Steel, Luce, Falconer).
No code, test or data file is in the top 40; the largest data file is a chart tile.

### 3.3 Binary files tracked

2,325 `.npz` (data/charts); 78 `.jpg` (docs/references: 56 signal-book pages, 16 pilot
pages, 6 images); 59 `.png` (56 under docs/playtests pictures, 3 under this review's
`play/`); 6 `.webp`; 25 `.gz` and 8 `.checkpoint` saves (docs/playtests and 5 test fixtures
under tests/fixtures/saves); 55 save `.json` under docs/playtests (52.5 MB). No zip, model
file, database or executable is tracked. `docs/playtests` holds 81.8 MB of the owner's runs:
the records of play, not needed to build or test (but see 3.6 for what is).

### 3.4 Secrets, keys, personal paths, names

Swept (git grep, restricted to freesail client tools data tests .github pyproject.toml
README.md .mcp.json CHANGES-m5c-c.md docs/references docs/agents docs/primer docs/reviews;
never docs/dev, design, playtests, gates): no `sk-` key, no `api_key = "..."` literal, no
GitHub/AWS/Slack token pattern, no private key block. E-mail-shaped strings: one in an OCR
text (OCR noise) and one `proxy.example` in a test (tests/test_api_door.py:129). Personal
paths: a Windows profile path in tests/test_settings.py:29-68 and tests/test_local_runner.py:121,
whose user name is a generic word (checked, not printed); a personal drive path
(`D:/Projects/...`) in docs/references/README.md:119, naming where the owner keeps a cache.
Not a secret, a record of the owner's machine. An unrestricted sweep, before I narrowed it,
returned the **names** (not the contents) of at least eighteen files under `docs/playtests/` that match
a personal-path pattern (saves and notes); I did not open them: the reviewer should check
whether saves carry the owner's profile path. Separately, 47 tracked paths under
docs/playtests and 20 under docs/agents carry a model's name in the path itself, against
tools/regatta.py:42-43's rule that "no model is named in the repository" (the consent records
under docs/agents are named so by design). Weight low to medium; sure for what is reported.

### 3.5 .gitignore, .gitattributes, .mcp.json

- `.gitignore` (29 lines) is sound: caches, venvs, egg-info, `saves/`, the chart fetch cache,
  untracked chart levels 0 and 1 with the two committed level-1 folders let back in, the test
  fixture saves let back in. It carries package history in its comments.
- `.gitattributes` forces LF on all text and keeps byte-exact the files whose digests tests
  pin (`docs/agents/ConsentBrief.md`, three brief fixtures, fixture saves) and the records
  under docs/agents/consent and docs/playtests. Sound; no LFS.
- `.mcp.json` starts `py -m freesail.agents.mcp_server --game http://localhost:8000
  --model-name "SET THE MODEL'S EXACT NAME HERE"`. `py` is the Windows launcher; it does not
  exist off Windows. **In this very session the configured MCP server "freesail" failed with
  "Executable not found in $PATH: py".** The model name is a placeholder that must be edited
  before use, in a file that is tracked. ci.yml ignores `.mcp.json` changes (:23, :29).
  Weight medium (any non-Windows checkout ships a broken tool configuration); sure.

### 3.6 The three workflows (read whole)

- **ci.yml "checks"**: on every push and PR that is not only `docs/**`, `**.md`,
  `.gitignore`, `.mcp.json` (:17-29), and by hand. Ubuntu-latest and Windows-latest,
  Python 3.11, `pip install -e ".[dev,server]"`, ruff check and format on Linux, then
  `pytest -n auto --dist loadgroup` (the fast tier; `--slow` when asked). Newer push cancels
  older. Cost: two jobs a push, the Windows one at the runner's higher rate.
- **release.yml "gate release"**: on a push to `gates/**` or by hand; Ubuntu-latest, 3.11;
  `ruff check .` (no format check), the whole suite `--slow -m "not pace"` on one runner, then
  the pace tests serially **as a gating step**, then `git archive` of the whole tree into a
  zip, a tag and a prerelease with `docs/gates/gate-<n>.md` as its notes. A red run stops the
  tag and the release (steps are sequential); it stops nothing else.
- **whole-suite.yml**: by hand only. Lint; the slow tier in six shards on ubuntu-24.04
  (Windows as well if ticked); the browser plans with Chromium installed, failing if a plan is
  skipped; the pace tests last, `continue-on-error: true` (informative).
- Checkout depth: all use `actions/checkout@v4` with no `fetch-depth`, so depth 1. **What
  skips because of it**: six hull tests that `git show` the base commit `f5be9110`
  (tests/test_hull_lugger.py:610, test_hull_schooner.py:470, test_hull_frigate.py:510,
  test_hull_smack.py:598, test_hull_brig.py:583, test_hull_cutter.py:430) skip in every CI
  run, and in this shallow clone too (`git cat-file -e f5be9110` fails here). They are
  checks that the hull work did not move a physics key; CI has never run them.
  tests/test_chart.py:1077 skips its `git ls-files` check only where `.git` is absent (the
  gate zip), and runs in CI.

Findings on CI:

- **W1. The fast tier ignores documents the game and the tests read.** ci.yml ignores
  `docs/**` and `**.md`, but the game reads `docs/primer/` (freesail/agents/tools.py:118,
  served to a model through `library`) and `docs/agents/ConsentBrief.md`, whose digest is
  pinned (freesail/agents/consent.py:141; .gitattributes says so), and writes consent records
  under `docs/agents/consent/` at run time (consent.py:142); tests read `docs/primer`
  (test_primer.py:74, test_grammar_book.py:27, test_in_world.py:36,
  test_known_truths.py:2783), `docs/design/Build-Ships.md` and six notes under
  `docs/design/ships-design/` (test_hull_*.py), `docs/references/Charts.md`
  (test_chart.py:643). An edit to any of these pushes green without a run. Weight high; sure.
- **W2. The gate gates on a measurement its own sibling calls a coin toss.** release.yml:131
  runs `pytest --slow -m pace` as a failing step on `ubuntu-latest`; whole-suite.yml:247-254
  says a shared cloud runner gives 480 to 520 ticks a second, made the pace job informative,
  and that its first run failed the floor; the floor is 500 (tests/test_known_truths.py:2157-2163,
  1000 x 0.5). Weight medium; likely.
- **W3. Runner images differ.** whole-suite.yml pins `ubuntu-24.04` because "the floating
  image moved ... and nine recorded passages moved with it" (:162-166); ci.yml:52 and
  release.yml:102 still use `ubuntu-latest`. The gate's own run is on the floating image.
  Weight medium; sure (config), likely (effect).
- **W4. Release lint is weaker than CI's**: release.yml:126 has `ruff check` and not
  `ruff format --check`. Weight low; sure.
- **W5. Nothing in CI runs a tool directly or the chart build**; tools are checked only
  through the tests that import them (section 1). The browser plans run only by hand
  (whole-suite). No workflow pins the browser version used by the probe. Weight low; sure.
- **W6. The gate zip carries everything**: `git archive` of the whole tree (release.yml:134),
  so each gate's download includes 359 MB of chart tiles, 82 MB of playtests and 128 MB of
  references. Weight low; sure.

### 3.7 pyproject.toml, Python, lint

- Pins: runtime `pyyaml>=6.0`, `numpy>=1.26`, `prompt_toolkit>=3.0`, all floors only; dev
  pins `ruff==0.15.8` exactly and the rest by floor; the agents extra caps two packages
  below a next major. No lock file. A new numpy or pyyaml major will arrive unasked in CI.
  The agents extra carries a vendor's SDK and a credential-store package (pyproject.toml:29);
  `dev` pulls `agents` in, so every test run installs them.
- Python: `requires-python = ">=3.11"`, ruff `target-version = "py311"`, all workflows 3.11.
  **This machine runs Python 3.13.18** (`python3 --version`), and the local ruff is 0.16.9,
  not the pinned 0.15.8: whatever is run on this machine is not what CI runs, and 3.12/3.13
  are exercised nowhere in CI. Weight low to medium; sure.
- Lint: `ruff check .` "All checks passed!"; `ruff format --check .` "390 files already
  formatted" (with ruff 0.16.9; `docs` excluded by pyproject.toml:52). Sound.

### 3.8 Licences and provenance under docs/references

217 tracked files, 127.9 MB: 125 OCR `.txt`, 78 `.jpg`, 11 `.md`, 3 `.webp`.
docs/references/README.md (85.8 KB) gives, per work, the edition, the archive URL and a
rights statement: "public domain" (51 mentions), "no rights stated; public domain by age"
(9), "Crown copyright, expired" (4 rows of Admiralty pilots, 1913 to 1917). Non-commercial
material is explicitly not committed (README.md:77: the Rumsey scans under CC BY-NC-SA are
"read and not committed"), and a museum-licensed image was taken out (images/README.md:23).
Chart source licences are kept as texts (`licences/`, five files) and named in the manifest.
Sound in method. Two gaps: 89 of the 216 files are named by neither their path nor their
basename in either README (they are covered by row-level descriptions such as "vol. 2 to 6",
or not at all; e.g. the 16 `pilots/pages/*.jpg` and 5 `signals/pages/*.jpg` are described by
group, `african-institution/*` eight reports by row); I did not check every row. And a file
taken out of the tree for its licence stays in git history (the shallow clone cannot show
whether the removed image is in earlier objects). Weight low (provenance), medium (history,
if the image is there); confidence sure / a suspicion.

## 4. The count of things

| | Lines | Bytes | Files |
|---|---|---|---|
| Game code, freesail/*.py | 164,607 (code 117,460 = 71%; comment 7%; docstring 11%; blank 10%) | 7.43 MB | 179 |
| Browser client | 9,870 | 0.46 MB | 13 (9 js, 3 html, 1 css) |
| Tools, all | 36,529 (gen_ships.py alone 10,381; tools/ships/ the rest beyond mine) | 1.81 MB | 30 |
| Tools, my 14 | 7,719 | | 14 |
| Tests, *.py | 141,396 | 6.85 MB | 176 (+27 fixtures and plans, 2.5 MB) |
| Data outside the charts | 78,847 (YAML and orders) | 4.4 MB | 427 |
| Chart text (yaml, json, geojson) | 42,460 | | 73 |
| Chart tiles | | 362.8 MB | 2,325 |
| Authored documents (root specs, agents, design, gates, primer, reviews) | | 7.71 MB, 1,221,923 words | |
| docs/references (OCR and pages) | | 127.9 MB | 217 |
| docs/playtests (saves, notes, pictures) | | 81.8 MB | 330 |
| docs/dev | not measured (rule) | | |

By directory under docs/ (tracked): agents 24 files 0.59 MB; design 56 files 3.74 MB;
gates 18 files 0.27 MB; playtests 330 files 81.81 MB; primer 28 files 0.73 MB; references
217 files 127.88 MB; reviews 35 files 1.46 MB; the root's ten specifications and proposal
0.93 MB (the two largest, TechnicalSpec-M6.md and -M7b.md, 0.18 MB each).

Ratios: tests to game code 0.86 by lines; game code to data (outside charts) 2.1 to 1;
authored prose to game code 1.04 by bytes and 1.29 by words (1.22 M words of documents
against 0.95 M words of code, docstrings and comments included). Comment and docstring are
18% of the game's lines.

Commits visible in the shallow clone at 504a250 (`git log --format=%ad --date=short`): 430
over seven days: 2026-11-08 4, 11-09 2, 11-10 107, 11-11 44, 11-12 59, 11-13 208,
11-14 6. Of these 92 are merges (no files by `--name-only`). Of the 338 others, **214 (63%)
touch only documents** (`docs/**` or `*.md`), 205 of them under docs/dev; 48 (14%) touch
`freesail/` or `client/`; 93 touch tests; 66 touch data. 2026-11-13 alone: 208 commits, 52
merges, 115 docs-only, 8 touching game code. (`--shortstat` totals are meaningless here: the
graft commit at the shallow boundary carries the whole tree as 32.6 M inserted lines.)

What the shape tells a newcomer: the repository is a document archive with a game inside
it. 94% of its tracked bytes (outside docs/dev) are chart tiles, OCR sources and recorded play; the authored prose
alone outweighs the game's code; nearly two commits in three in the last week changed only
the project's notes about itself, against one in seven that changed the game. The code is
large (165k lines) and nearly matched by tests (141k), and the tests lean on the documents
(W1). Most of a clone's 1 GB is not needed to build, test or play, but cannot be left out
without history surgery, since the tiles and the saves are in the history.

---

## The ten findings that matter

1. **CI ignores the documents the game serves and the tests read** (ci.yml:17-29 against
   freesail/agents/tools.py:118, agents/consent.py:141-142, tests reading docs/primer,
   docs/design, docs/references). A change to the primer or the consent brief merges green
   unchecked. High; sure.
2. **data/charts is 359 MB of compressed binary tiles in plain git**, rebuilt by region with
   every rebuild a permanent new copy (9 commits, 2,333 tile changes in the visible week
   alone; no LFS). The clone is 1 GB and can only grow. High; sure.
3. **No schema; typos in optional YAML keys are silent** (ports.py:701-786 and the other
   `get(key, default)` loaders; one unknown-key refusal in the whole tree, the hull profile).
   Medium; sure.
4. **The gate release gates on the pace tests on a floating cloud image** that the project's
   own manual workflow says gives 480 to 520 against a floor of 500 and moved nine pinned
   passages (release.yml:102,131; whole-suite.yml:162-166,247-254;
   tests/test_known_truths.py:2157-2163). Medium; likely.
5. **Six hull regression tests never run in CI or in a shallow clone** (depth 1; `git show
   f5be9110` absent; test_hull_*.py). Medium; sure.
6. **The chart audit re-implements the tide blend without the seam taper** and reaches
   private functions (audit_chart.py:680-691, 844, 1105-1108 against tide.py:484-535), while
   its docstring says it uses the game's readers only; and its ratchet holds 142 accepted
   faults, 59 of the sampled ones against ports. Medium; likely.
7. **The game cannot be installed except editable**: 25 separate `parents[2] / "data"`
   roots and two cwd-relative ones, and pyproject packages only `freesail*`
   (pyproject.toml:35-36). Medium; sure (config), likely (effect).
8. **.mcp.json is tracked, Windows-only and a placeholder**: `py` launcher, model name to be
   filled in; it failed to start in this session for want of `py`. Medium; sure.
9. **No licence file for the code** though pyproject says MIT and the gate zip publishes the
   tree. Medium; sure.
10. **Five hand-run tools and two tool pairs that are one tool twice** (day_log/lesson_run;
    pace's measure copied 14 times into tests), with stale constants (measure_loads' 35-degree
    peak against the data's 40). Low; sure.

## What I did not read

- `tools/gen_ships.py` and `tools/ships/` (another reader's), and `freesail/` beyond the
  loaders and lines cited (ports.py:663-802, tide.py:456-535, the data path constants).
- tools/build_charts.py read in full only to line 400 and by its outline (every `def`,
  `class`, constant and URL) beyond; the bodies of `Build` (:1988-2934) and the readers
  (:1116-1435) were not read line by line. Its fetch was not run (no network).
- tools/browser_probe.py was not run against a browser; regatta.py was not run on a course;
  pace.py and climatology_check.py at full length not run (long).
- `docs/dev/` (by rule; not listed, not measured: its size is missing from every docs total
  here), `docs/design`, `docs/gates`, `docs/playtests` (names and sizes only).
  `docs/references/README.md` read for provenance by grep and the rows quoted, not every
  row checked against every file.
- Branch protection and the Actions minutes actually spent are GitHub settings and history,
  not in the tree; what a red ci.yml run blocks depends on them and I could not see them.
- The full history's size and whether removed files remain in it (shallow clone).
