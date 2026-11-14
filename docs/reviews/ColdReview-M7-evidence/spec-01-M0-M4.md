# Spec reader 01: the foundations (M0 to M2, M3, M3b, M4) against the code

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read whole: `docs/TechnicalSpec-M0-M2.md`
(617 lines), `docs/TechnicalSpec-M3.md` (355), `docs/TechnicalSpec-M3b.md` (146),
`docs/TechnicalSpec-M4.md` (271), and the two rule files. Grepped `docs/DesignProposal.md`
for the replay and sandbox promises (lines 92 and 292). Code read in part (see the last
section). No test suite run; three short Python calls, each a few seconds, with bytecode
writing off; nothing written in the tree but this file (scratch files in the session's
scratchpad only).

Short calls used as evidence below:

- **P1 (the sandbox probe).** A frigate world, `bind(world)`, then an `@at("sunset")` rule
  whose body reads `r._world`, lists the working directory, writes `world.ship.extra["poked"]`
  and spins for 1.5 s. Output: `world reached: Hull files visible: 15`,
  `registered; poked: True`, `journal: []`.
- **P2 (replay and rate).** Seed 7, `make all sail`, 600 ticks, then `replay.replay(save)`.
  Lugger: 1,262 ticks/s, replay digest equal. Frigate: 482 ticks/s, replay digest equal,
  77 events. The machine had a load average of 3 to 4.5 from the timed suite, so the rate
  is low by an unknown factor.
- **P3 (the checkpoint unpickler).** A hand-built protocol-4 pickle naming
  `freesail.settings` / `os.getcwd` with STACK_GLOBAL and REDUCE, fed to
  `freesail.core.replay._Unpickler`: it returned `/home/user/FreeSail`. Same through
  `freesail.agents.api`. Python 3.13.18.
- **P4 (orders).** Frigate, `haul the weather main brace`, `set the topsail`,
  `set the fore topsail`, `brace the fore yard sharp up`; journal printed.
- **P5 (save size).** Frigate, 300 ticks: save 1,552 bytes, checkpoint 173,556 bytes;
  `ship_ref` is `{'type': 'file', 'path': 'data/ships/frigate-36.yaml'}`.

## 1. The commitments

### Spec M0 to M2

| § | what the specification says is built | verdict | where it lives | how you know |
|---|---|---|---|---|
| 1.1 | The simulation is a library, `freesail.sim`, ignorant of who drives it | built otherwise | no `freesail/sim`; `freesail/core/world.py` | `ls freesail`. The World imports the agents' code: `core/world.py:1124,1296,2505,2653,2686` (`agents.director`, `agents.harness`, `agents.watches`); `core/replay.py` 16 imports from `freesail.agents`; `orders/` 14; `world/` 63 across 18 files (grep count). The sim knows its LLM drivers by name. |
| 1.2, 3.2 | Determinism: no wall clock, no unseeded randomness, named streams | built as specified (for the sim) | `core/rng.py:14-29` | grep for `time.time`/`monotonic`/`datetime.now`/`perf_counter`: only `agents/` and `ui/`. Bare `random.Random(0..3)` fallbacks in `world/lookout.py:427-496` and `world/ships.py:550`, and `world/hail.py:488` seeds from `crc32(vessel.id)`, not the master seed: deterministic, but outside the named-stream rule. P2 replays equal. |
| 1.2 | No iteration over unordered containers where order matters | cannot tell | | not audited; would need a read of every `set` loop. |
| 1.3 | Every noticeable change is an event | cannot tell in general | | every kind of §5.3 and the M3/M4 kinds found in code or data (grep of 35 kinds, none missing). |
| 1.4 | Rig-agnostic: no `"main"` in reference to masts | built in part | `crew/hands.py:104-108`, `crew/model.py:33-35`, `evolutions/runner.py:1110-1118`, `physics/strain.py:449` | The topmen of a sail are found by splitting the mast's id on its first dot and looking the word up in `{"fore","main","mizzen"}`; the station enum has exactly three tops. §6.2 says the dots "have no meaning to the engine". Every ship file happens to name its masts `fore/main/mizzen` (the lugger's `mizen.mast` has no tops, so it does not bite yet); a fourth mast, a jigger, or a mast filed under another id gets no topmen of its own. The spec M3 §2.1 enum itself writes the three tops in. `Ship.on_schooner_mast` (`ship/graph.py:207`) is derived from the graph, as it should be. |
| 1.5 | Data before code; validate loudly | built in part | `ship/schema.py:2402-2560` | loader raises sentences for cycles, chains, alias/group against part ids; no check that an alias or group collides with a verb (§6.4 asks for it): grep for verb collision in schema, loader, resolve found none. |
| 1.6, 4.1 | `units.py` the only place that converts | cannot tell | | not audited; `client/units.js` mirrors it as §9.4 allows. |
| 2 | Repository layout | built otherwise | | all named modules exist except `client/profile.js` (the view is `client/shipview.js`, `projection.js`), `tests/test_loader.py` (now `test_ship_loader.py`), `tests/test_grammar.py` (now `test_orders.py` and others). `evolutions/runner.py` "replaced in M3" was extended, not replaced. |
| 3.1 | 1 s tick, four 0.25 s substeps | built as specified | `physics/integrate.py:40`, `physics/strain.py:101` | constants read. |
| 3.3 | Journal of `(tick, actor, text)` | built as specified | `core/world.py:2080-2081` | standing-order and station firings are not journaled, as M4 §4 says. |
| 3.3 | Save = engine version, seed, scenario, **ship file content hashes**, journal | built otherwise | `core/world.py:2591-2645`, `ship/graph.py:421-422` | P5: `ship_ref` is a relative path only. Content hashing moved to a whole-tree fingerprint (`core/world.py:53-83`) over every `.py` and every data file, comments included. |
| 3.3 | Replay gives a byte-identical log; `tests/test_replay.py` asserts it | built as specified on the same build | `core/replay.py:155-220`, `core/events.py:108-120` | the test compares a SHA-256 over canonical JSON of events (`events.py:108`), not bytes; P2 equal on two ships. |
| 3.3 | "A full state snapshot is not the save format" | overtaken | `core/replay.py:14-27` | package 33a's checkpoint is a pickle of the whole World beside the save; `load` prefers it. The spec still says the opposite. |
| 3.3 + proposal §3.2 | "A saved log is a saved game" | built in part | `core/replay.py:30-41, 739-790` | A replay is "promised only on the build that wrote it"; the build is the fingerprint of every file of code and data, so a one-line comment edit makes every earlier save another build's. Such a save with a station's transcript is refused unless `replay_anyway`; one without is replayed with a warning and may silently diverge. A game with a Python standing order does not replay at all (row M4 §4 below). |
| 4.2 | `port` accepted, echoed larboard | cannot tell | | `port the helm` refused in P4 (it is not a period helm order, so no finding). |
| 5.1-5.3 | Event shape, severities, the 26 kinds | built as specified | `core/events.py` | grep of kinds. |
| 6.2-6.3 | Ship file format, part classes, role links | built as specified | `ship/schema.py`, `ship/loader.py` | 18 ship files load (the parity tests glob them, e.g. `tests/test_driver.py:298`). |
| 6.3 | Role queries `yard_of`, `sail_of`, `halyard_of`, `braces_of`, `sheets_of`, `spar_chain`, `dependents` | built as specified | `ship/graph.py:89,94,125,154,301,310,313` | `grep def`. |
| 6.5 | Derived vocabulary, sides, weather/lee at parse | built as specified | `orders/resolve.py` | P4: "Hauled the starboard (weather) main brace". |
| 7.1 | Wind with walk, gusts, shear | not read | `physics/wind.py` | not read. |
| 7.2-7.4 | Sail force, blanketing, hull, heel, helm | built otherwise (tuned) | `physics/hull.py:35`, `physics/sails.py` | `C_F = 0.008` against the spec's 0.004; the spec itself calls these starting values. Not read in full. |
| 7.5 | Strain rule: ratio bands, `0.002 (r-1.5)^2` per substep, blow-out at 1.8 | built as specified | `physics/strain.py:94-104` | constants read. |
| 7.6 | Fifteen known truths pass | built in part | `tests/test_known_truths.py:283, 457` | truth 3 (the schooner's best point) and truth 11 (wear's loss to leeward) are `xfail(strict=True)`: the code is held to failing them. |
| 8.1-8.3 | Imperative grammar, verbs, resolution | built as specified, then grown | `orders/`, `data/vocabulary.yaml` (2,494 lines) | §8.6 abdicates: "this section is not maintained verb by verb". Ambiguity refusal holds (P4: "could be the fore topsail, the main topsail or the mizzen topsail"). |
| 8.3 | weather/lee "recorded resolved in the journal" | built otherwise | `core/world.py:2081` | P4 journal: `(0, 'captain', 'haul the weather main brace')`, unresolved. Replay re-resolves it at the same tick, so it is harmless on one build, but the spec's reason (unambiguous replay) is not what the code relies on. |
| 8.4 | Evolutions as data files; M3 changes only durations | built in part | `data/evolutions/` (108 files) | 64 of 108 files say `script:` and carry only parameters; their behaviour is Python in `evolutions/scripts.py` (9,095 lines, 44 classes), `action_scripts.py`, `fight_scripts.py`, `repair_scripts.py`. 44 are step lists. The catalogue is data for routine sail work and code for every manoeuvre. |
| 8.5 | Tack, wear, heave to as scripts; truth 10, 11, 12 | built as specified, wear failing | `data/evolutions/tack.yaml`, `evolutions/scripts.py` | truth 11 xfail (above). |
| 9.1 | Console with driver commands | built as specified | `ui/console.py` | not run. |
| 9.2 | Server routes `/`, `/api/ship`, `/api/state`, `/api/order`, `/api/driver`, `/ws` | built as specified | `ui/server.py:1489,1498,1506,1565,1572,1613` | grep; binds 127.0.0.1 by default (`ui/server.py:1744`). |
| 9.3 | Client: log, instruments, profile, map; no framework | built otherwise | `client/` | no `profile.js`; 13 files incl. `harbour`, `library`. Not read. |
| 10 | Determinism and replay tests on every reference ship | built in part | `tests/test_determinism.py:12-30` | the determinism test drives the point stub, not a ship; replay tests use the stub and the frigate (`test_replay.py:171`), and a few ship-specific files. No test parametrised over `data/ships/*.yaml` for replay found by grep. |
| 10 | Suite under a minute | overtaken | | the spec's own aside: some 1,700 tests and eleven minutes at M5a; 177 test files now. |

### Spec M3

| § | what the specification says is built | verdict | where it lives | how you know |
|---|---|---|---|---|
| 1 | Compatibility rule: rested frigate crew, one evolution, factor 1.0 to the tick | built as specified | `tests/test_hands.py:621` | test exists; `crew/hands.py:415-440` gives 1.0 for a request filled at its rating. |
| 2.1 | `Sailor` fields, seeded skill spread | built in part | `crew/model.py` | the spread is drawn but never read by the crew factor (`hands.py:427-436` reads the rating table); `skill_deck` is read only by later combat and people code (`combat/boarding.py:273`, `combat/shot.py:216`). |
| 2.1 | `RATING_SKILL` 0.35/0.6/0.8/0.9, marine 0.4 deck 0 aloft, idler 0.3/0 | built as specified | `crew/model.py:73-81` | read. |
| 2.2 | Stations, watch bill, idlers by day | built as specified | `crew/bill.py`, `crew/routine.py` | not traced tick by tick. |
| 2.3 | `crew:` section, stations plus posts must equal complement | built as specified | `ship/schema.py:2750-2812` | the sentence "must make up the complement". |
| 2.3 | Three name lists | built otherwise | `data/crew/names.yaml:17,55,94` | english, american and french (the lugger's). |
| 2.4 | Muster from the named stream, replayed | built as specified | `api/session.py` (`stream("muster")`, `extra["crew"]`) | grep; truth 22 test. |
| 3.1 | Request order: on deck, fit, idle; by preference; by id | built as specified | `crew/hands.py:202-222, 297-380` | read. |
| 3.2 | Short-handed: half rule, waits, named party refused | built as specified | `crew/hands.py:95` (`SHORT_HANDED_SHARE = 0.5`) | read in part. |
| 3.2 | All-hands `party: N` | built as specified | `crew/hands.py:126-135, 319` | read. |
| 3.3 | Crew factor = numbers x skill x fatigue; 0.5 and 0.05 | built otherwise | `crew/hands.py:50,54,398-440` | as spec, plus a `seaway` term (M5) and a skill of 1.0 for all-hands work, a judgement the docstring owns. |
| 3.4 | All hands a pool action; manoeuvres `belays: true` pause | built as specified | `evolutions/runner.py` (`_top_up_all_hands`, `paused`, `in_progress`) | grep; truth 19 tested. |
| 4.1-4.3 | Watch changes, call all hands (90 s, a third at once), fatigue table | built as specified | `crew/routine.py:44-72` | every constant matches the §4.3 table. |
| 5.1 | `call all hands`, `pipe down`, `muster`, hands selectors | built as specified | `orders/crew.py` | not read whole. |
| 5.3 | Level-0 line orders free of hands | not checked | | |
| 5.4 | `belay <work>`, `belay that`, `belay all work` | built as specified | `orders/work.py`, `evolutions/runner.py` (`def belay`) | grep. |
| 6 | Catalogue to at least forty | built as specified | `data/evolutions/` | 108 files. |
| 7 | Truths 18 to 23 | built in part | `tests/test_known_truths.py:719` | truth 18's absolute times strict xfail (16.4 and 5.6 min against 25-40 and 12-20). |

### Spec M3b

| § | what the specification says is built | verdict | where it lives | how you know |
|---|---|---|---|---|
| 2.2 | After yards 3 degrees sharper | built as specified | `evolutions/trim.py:43` | constant read; truth 24 strict xfail (`test_known_truths.py:1054`). |
| 3 | Catharpins +4 degrees, rating x0.85 | built as specified | `ship/parts.py:1205`, `physics/strain.py:135` | constants; truth 31 strict xfail (`:1374`). |
| 4 | Bowlines, luff gain 4, slack at 40 | built as specified | `physics/sails.py:161,168` | truth 26 strict xfail (`:1132`). |
| 5 | Adjacent-yard limit from geometry, floor 10 | built as specified | `orders/verbs.py:185,1416-1427` | read. |
| 6.1-6.2 | Canvas number, cloth rating, wear 0.05/h, baggy luff | built as specified | `ship/parts.py:76-96`, `physics/strain.py:99-125` | constants. |
| 6.3-6.4 | Sail room as a list, storm canvas, ringtails | built as specified | `ship/schema.py:689`, ship files | schema read in part. |
| 6.5 | Truths 27, 28 | built in part | `test_known_truths.py:1251` | truth 28 strict xfail: she goes astern. |
| 7 | Studding stall, boom foul at 45, booms start rigged in | built as specified | `data/sail_classes.yaml:116-132`, `orders/verbs.py:193`, `ship/parts.py:187` | `rigged_out: bool = False`. |
| 8 | View fixes | cannot tell | `client/` | not read. |

### Spec M4

| § | what the specification says is built | verdict | where it lives | how you know |
|---|---|---|---|---|
| 2 | One readings registry for rules, instruments and agents | built as specified | `api/readings.py` (4,865 lines), `core/world.py:1947` | read the view. |
| 3 | Standing dialect, book, authority, dwell 300 s | built as specified | `standing/`, `standing/rules.py:44` | grep; truths 34 to 38 named in tests. |
| 4 | Firings not journaled, replay gives the same firings | built as specified (dialect) | `core/world.py:2080` | truth 39 test (`tests/test_replay.py:126`). |
| 4 | Python API builds the same rules, one engine | built as specified | `standing/python_api.py:224-260` | read: decorators make `Rule` objects in the same book. |
| 4 | A Python rule "may only call `order(...)` and read the readings object ... never the World" | built otherwise | `standing/python_api.py:270-287`, `api/readings.py:334-337` | P1: the body ran unrestricted, read `r._world`, listed the disk, wrote the ship's state, and spun 1.5 s. The rule is a convention. |
| 4 + proposal §4.5 | Python rule "saves as its name and source text"; a save of it replays | built in part | `standing/python_api.py:294-330`, `tests/test_python_api.py:340-380` | P1: `journal: []`. Registration goes through `book.enter`, not `World.submit`, so it is never journaled; the replay omits the rule and every firing (the project's own test asserts `copy.standing.book.names == ["morning sail"]` after replaying a world that had both). A game with a Python rule is not reproduced by its save. |
| 4, 24.1 + proposal §4.5 (line 292) | Sandbox: restricted environment, time budget per tick, no filesystem or network; overrun suspended and logged | not built, and dropped | `standing/python_api.py:28-44`, `rules.py:493` | grep of `freesail/` for `sandbox`: only the two docstrings saying milestone 6 will do it. grep of `docs/TechnicalSpec-M6.md`, `-M7.md`, `-M7b.md` for sandbox, "python rule", "time budget": nothing. The body runs once at registration, so a time budget per tick has nothing to apply to. |
| 5 | Sun: rise, set, twilight; latitude default 50 N | built as specified | `core/sun.py`, `core/world.py:118` | grep. |
| 6 | Six starter routines | built otherwise | `data/standing_orders/starter.orders` | seven orders; "heavy weather" now `close reef the topsails; send down the topgallant masts; set the storm staysails` (lines 122-125), not the four-step order truth 37 describes. |
| 11 | Station and authority; watcher has none | built as specified | `agents/agent.py`, `agents/tools.py` | not traced. |
| 11 | Token scanned on the raw output before anything | built as specified | `agents/harness.py:2530-2535`, `agents/model.py:90-99`, `agent.py:146` | read. Case-sensitive exact match. |
| 11 | Welfare: repeat N=3, nudge, pause, stand down after 600 real s | built as specified | `agents/harness.py:299,375,3084-3095,3375-3381` | constants; the stand-down reads `time.monotonic()`, so a logged line depends on the wall clock (recorded as a door act and replayed, per `test_replay.py:624`). |
| 11 | Budgets 16 orders, 32 reads | built as specified | `agents/agent.py:268-269` | read. |
| 11 | Named pointers (`TURN_ENDS_WORDS`, `DANGER_LINES`, `StandBy.bound`, `undoes`, `LEAVING_WORDS`, `seating`, `JournalEntry.by`, `Seat.key`, `why_again`, `RE_ASK_SECTIONS`, `again_words`, `asked_why`, `STATION_ACTORS`) | built as named | see §2 | grep. Behaviour not traced. |
| 13 | Doors as clients; MCP bridge; local runner | built as specified in shape | `agents/mcp_server.py`, `agents/local.py`, `ui/server.py` | not run. |
| 14 | Consent records per weights | built as specified | `docs/agents/consent/` (21 records) | listed. Identity is the string the door passes (`--model-name`), which the spec intends. |
| 15-16 | Scripted fake; truths 41 to 47 | built as specified | `agents/fake.py`; `tests/test_agents.py` | grep found each truth number. |
| 19 | Weather script | built as specified | `world/weather_script.py` | exists. |
| 20 | Roll-up at 60x and above; up to 300x | built otherwise | `core/events.py:156`, `ui/console.py:95` | `ROLLUP_FROM = 60`; `MAX_COMPRESSION = 1000`. |
| 20, 23 | 3,000 ticks/s headless on the owner's machine (truth 51) | not met, and the test says so | `tests/test_known_truths.py:2147-2183` | the test asserts a floor of 500 here and then `3000 / 2.0 > 1000`, a constant comparison that passes only because the budget is not met. P2: 482 ticks/s for the frigate on a loaded machine. |
| 24.8 | Auto-slow on alarm | built as specified | `ui/console.py:98-125, 576`, `ui/server.py:259` | grep. |
| 24.9 | Context budget tool, handover | built as specified | `tools/context_budget.py`, `agents/harness.py:364-365` | grep. |
| 24.6 | One `freesail` command with two `setup <client>` subcommands (for the desktop client and the code client) | built otherwise | `freesail/__main__.py:1-38` | a harbour web page that writes the client configurations; no subcommands. |

## 2. The pointers

Twenty-four checked by name (grep for the definition): `units.watch_of`, `core/rng.py` streams,
`ship/graph.py` role queries (7 functions counted as one), `Ship.mast_of`, `hands.request`,
`hands.release`, `Runner._begin`, `_tick_steps`, `_start_waiting`, `_top_up_all_hands`,
`Instance.paused`/`in_progress`, `Script.clears`, `crew.model.RATING_SKILL`,
`stream("muster")` and `ship.extra["crew"]` in `api/session.py`, `Runner.belay`,
`World.summary_lines`, `queries.snapshot` crew key, the `standing order '` actor,
`tools.TOOLS` (at `agents/tools.py:1601`), the eight tool functions, `agent.TURN_ENDS_WORDS`,
`readings.DANGER_LINES`, `harness.seating`, `consent.RE_ASK_SECTIONS`,
`events.STATION_ACTORS`, `tools/context_budget.py`, `tests/test_staying.py`,
`tests/test_primer.py`, `tests/test_evolutions.py`.

**Hold: 20 of 24. Do not hold:**

1. `client/profile.js` (M0-M2 §2, §9.3): absent; `client/shipview.js` and `projection.js`.
2. `tests/test_loader.py` and `tests/test_grammar.py` (M0-M2 §2, §10): absent under those
   names.
3. "recorded resolved in the journal" (M0-M2 §8.3): the journal keeps the unresolved words (P4).
4. "ship file content hashes" in the save (M0-M2 §3.3): a path only (P5).

Behaviour behind the names that hold was traced only for the crew factor, the token scan,
the Python API and the replay roads.

## 3. The numbers

| Number | Held by a test? | Checked here |
|---|---|---|
| Truths 1 to 15 (M0-M2 §7.6) | yes; 3 and 11 strict xfail | no |
| Turning circle 4 to 6 lengths (truth 16) | yes, `tests/test_staying.py` | no |
| Truth 18: watch 25-40 min, all hands 12-20 | strict xfail; measured 16.4 and 5.6 | no |
| Truth 20: factor 1.10-1.25 | yes | no |
| Truths 24, 26, 28, 31 (3b) | all four strict xfail | no |
| Truth 51: 3,000 ticks/s owner's machine | no; floor 500 asserted, budget asserted unmet | P2: 482/s frigate, 1,262/s lugger, loaded machine |
| Save "a small JSON file" | no size test found | P5: 1.5 kB save, 174 kB checkpoint at 300 ticks |
| Replay digest equal | yes | P2: equal on frigate and lugger |
| ALL_HANDS_DELAY_S 90, fatigue table, dwell 300, repeat 3, 600 real s | constants as specified | read |

Seven of the foundations' truths (3, 11, 18, 24, 26, 28, 31) are held by tests to *fail*,
and an eighth (51) is asserted unmet; the green suite carries them silently.

## 4. The open items

**M0-M2 §12 (11 items, numbered 1, 2, 3, 4, 6, 8, 7, 5, 9, 10, 11):** 1 curves: open by
nature. 2 turning truth: closed (package 32e). 3 reef factors: open (not checked). 4
blanketing: open. 5 frigate particulars: built (Amazon class in the crew comments). 6 mast
rake: closed. 7 schooner's bare fore yard: **still open** (no `fore.yard` in
`data/ships/topsail-schooner.yaml`). 8 adjacent yards: built in 3b. 9 draw order: claimed
by 3b §8, not checked. 10 backed sail drawn: cannot tell (the client marks `backed`;
`shipview.js:93`). 11 pointing geometry: built in part by 3b (brace limits still a file
number; 3b open item 1).

**M3 §9 (14 items, 1 to 6 before §10 and 7 to 14 after its table):** 1 `max_hands`:
**still open** (no `max_hands` in code); `party` covers all-hands only. 2 helmsman and
lookout as sailors: not checked. 3 officer of the watch: built later (M6, not my reading).
4 meals, sickness: partly built later (`crew/health.py`, `crew/victuals.py`). 5 line
orders costing hands: still open (not checked). 6 boys: not checked. 7 per-ship scaling of
requests: **still open** (no scaling in `crew/hands.py`). 8 booms rigged in: built (3b).
9 box-haul after trim: not checked. 10 truth 18 times: **still open**, strict xfail. 11
suits: built (3b). 12 studding wind: built (3b). 13, 14 view: not checked.

**M3b §11 (15 items):** 1 geometric brace limits: open. 2 Bouguer/Euler tables: not
checked. 3 Steel's spar tables: not checked. 4 mending: M8. 5 Hardy's other measures:
open. 6 and 9 sternway a-try: **still open**; `physics/hull.py:246-257` resists astern as
ahead, and a yaw fade brought her to 1.6 kn astern, truth 28 still xfail. 7 storm canvas in
gusts: owner's judgement, open. 8 after-yards ruling: held, truth 24 xfail. 10 `trim
<sail>`: built (M4 §7). 11 mast trimmed upper yards in: not checked. 12 schooner bowlines
truth: open. 13 telltales: not built (no match in `client/*.js`). 14 skysails: not built
(no `skysail` in code or ship data). 15 ringtail head: not checked.

**M4 §24 (11 items):** 1 sandbox: **quietly dropped** (milestone 6 named; nothing in
code; no later spec mentions it). 2 officers: built later. 3 director's channel: built
later (M7b). 4 well, glass, depth: built (M5, not traced). 5 library book: not checked. 6
install: built otherwise (the harbour). 7 bare-poles windage: not checked. 8 roll-up to
models and auto-slow: auto-slow built. 9 context budget and handover: built. 10, 11:
principles, no build.

Count: 51 open, deferred or "to do" items across the four chapters (11, 14, 15, 11). By my
placing above: 17 still open (four in M0-M2, four in M3, nine in M3b), one dropped (the
sandbox), about 18 built or closed (some by later milestones), and about 15 not checked.

## 5. The document as a document

- A newcomer could build the M0 core from §3 to §8 of M0-M2, and the crew from M3 §2 to §4.
  Past that, the documents are a ledger. M0-M2 §8.5 "as built (package 37f ...)" and M4
  §11's twelve sub-bullets of package 37g are dated rulings, package numbers, playtest
  references and accounts of what was tried; I would put a third of M4 and a sixth of M0-M2
  as history rather than specification.
- They refer constantly into `docs/dev/TuningNotes.md` and `docs/playtests/` for the
  numbers that justify them, which a reader under these rules may not open.
- They contradict themselves and each other: M0-M2 §11.1 "all fifteen truths pass" against
  M3 §1 "the seventeen truths"; M0-M2 §3.3 "a snapshot is not the save format" against the
  checkpoint; M0-M2 §6.2 "dots have no meaning" against M3 §2.1's three named tops and
  `hands.py:104`; M4 §6 "six orders" against §3's eight examples and the file's seven; M4
  §20 "up to 300" against `MAX_COMPRESSION = 1000`; M3 §9's list split in two by §10's table
  (items 7 to 14 sit after it); M0-M2 §12 numbered 1, 2, 3, 4, 6, 8, 7, 5.
- M0-M2 §8.6 says plainly that the grammar section is no longer maintained, and hands
  authority to the vocabulary file and the primer. That is honest, and it means the spec is
  no longer the truth about the orders.
- The sandbox promise appears in M4 §4 and §24 and in the proposal, and nowhere after.
  The spec still reads as though it is coming.

## 6. What the specifications never asked for

- **The checkpoint** (pickle of the whole World, `core/replay.py:14-27, 451-530`), grown
  to answer slow replays. Its unpickler admits any name reached through a `freesail.*` or
  `numpy*` module; P3 called `os.getcwd` through `freesail.settings`, so the same route
  reaches `os.system`. The docstring's "a checkpoint from elsewhere cannot run code here"
  (line 27) is false. A shared save with its `.checkpoint` beside it is code execution on
  load.
- **The build fingerprint** over every file (`core/world.py:33-83`) and the two replay
  roads by transcript or by acts (`core/replay.py:93-117`, `core/acts.py`): an elaborate
  apparatus, about 900 lines in `replay.py` alone, built to manage the consequence that
  replay is not stable across builds.
- What the specs' logic needed and nobody wrote down: a Python rule's registration in the
  journal (or the save) so that the "one engine" survives a replay; and a station for mast
  identity in the crew model that does not read the part id.

## The ten findings that matter

1. **No sandbox for player Python, and the promise has been dropped.** A rule body runs
   in-process with the whole interpreter, reaches the World through `readings._world`, the
   disk and the network, and has no time limit (P1; `standing/python_api.py:270-287`,
   `api/readings.py:334-337`); no later spec carries the M4 §24.1 promise. Weight high (the
   proposal's §4.5 security line), confidence sure.
2. **The checkpoint loader executes code.** `_Unpickler` admits `os.*` through any
   `freesail.*` module (P3; `core/replay.py:451-501`), against its own docstring. Weight
   high, confidence sure.
3. **A saved log is not a saved game across builds.** Replay is promised only on the build
   whose fingerprint covers every code and data file, comments included
   (`core/world.py:33-83`, `core/replay.py:30-41`); the save carries no ship content hash
   (P5). Weight high, confidence sure.
4. **A game with a Python standing order does not replay.** Its registration is never
   journaled (P1 `journal: []`); the project's own test shows the replayed book without it
   (`tests/test_python_api.py:360`). Weight medium, confidence sure.
5. **The simulation is not a library ignorant of its drivers.** `core/world.py` and
   `core/replay.py` import the agents' harness and director; `world/` imports `agents`/`ui`
   63 times. Weight medium, confidence sure.
6. **Rig-agnosticism leaks through the crew.** Topmen are found by the first word of the
   mast's id against `fore/main/mizzen` (`crew/hands.py:104`, `runner.py:1110-1118`), with
   three tops fixed in the enum. Weight medium (any new rig), confidence sure.
7. **The evolution catalogue is mostly code.** 64 of 108 files are `script:` stubs whose
   behaviour lives in some 10,000 lines of Python. Weight medium, confidence sure.
8. **Seven foundation truths are held to fail** (3, 11, 18, 24, 26, 28, 31, all strict
   xfail) and truth 51's speed budget is asserted unmet (`test_known_truths.py:2147-2183`;
   P2 482 ticks/s). Weight medium, confidence sure.
9. **The specifications are no longer the truth about the code**: history-heavy, mutually
   contradictory (fifteen or seventeen truths, snapshot not the save, dots meaningless), the
   grammar section abandoned, four of twenty-four pointers stale. Weight medium, confidence
   sure.
10. **The long tail of open items**: 51 across the four chapters, at least 17 still open
    (schooner's fore yard, `max_hands`, per-ship crew scaling, sternway a-try with astern
    resistance equal to ahead, skysails, telltales among them). Weight low to medium,
    confidence likely.

## What I did not read

- The physics in full (`physics/wind.py`, `sails.py`, `hull.py`, `integrate.py` read only at
  constants); `evolutions/scripts.py` (9,095 lines) beyond grep; `standing/grammar.py`,
  `runtime.py` beyond grep; `agents/harness.py` (5,571 lines) beyond the token scan and the
  welfare constants; `agents/mcp_server.py`, `local.py`, `remote.py`, `consent.py`; the
  client; `ui/console.py` and `ui/server.py` beyond grep.
- No test file read whole; tests located by grep only. No test run.
- No audit of unordered iteration; no check of truths 1 to 17 by running them.
- `docs/agents/*.md` and the consent records listed, not read. Later specs (M5 to M7b)
  grepped for the sandbox only.
