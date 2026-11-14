# The cold review of milestone 7 (package 114)

**The tree reviewed:** the trunk at commit `504a25066c6995ce9829a19ffc597feb510a1870`. Nothing later was looked at. Work in flight on other branches was not read.

**For whom:** the owner. The lead's method, briefs, rulings and records are under review with the rest. The lead merges this document unedited.

**This file is written in two sittings, and the commits show which is which.** The first sitting (heads 1 to 5 as first written) was done before any of the project's records was opened: nothing under `docs/dev/`, no design note, no playtest, no gate report, and not the sealed notes. The second sitting (the owner's pages, head 6, the comparison with the records and with the sealed notes, and any correction of the first) comes after. Where the second sitting changes a finding of the first, it says so in place and does not rewrite it silently.

---

## For the owner: two pages

*(Written last, after both sittings. The numbers in brackets are where the body says more.)*

### What the project is

FreeSail is a real and unusual thing: a sailing ship of about 1805 simulated part by part and man by man, sailed by typing orders in the words of the time, in a sea with weather, tide, a chart, other ships and ports, where a language model can stand a watch through the same orders you give. Its centre works and is good. I sailed it. A frigate left to her standing orders rode out a day's rising gale by herself. A passage by dead reckoning ended, through my own fault, aground off Rame Head exactly where the game had warned me my course crossed the land.

It is about 350,000 lines: a game of 165,000, tests of 141,000, tools of 37,000, a browser client of 10,000, and half as much again in words of record and design as in the game's own code (10.8 MB of the one to 7.4 MB of the other). Since early October it has grown mostly sideways: more sea, more ports, more ships, more nations, a director, a far world, powder. It has not passed a gate since 8 October, and about the newest third of it has never been before one.

### The ten things that matter most

1. **A stranger cannot begin, and the first fight and the first port fail him without a word.** The opening page is a form with forty-seven scenarios in alphabetical order and no first game. In the first action I gave the orders the game lists, and my guns stayed lashed while it answered that they were "firing as they bear already"; the enemy shot away my topmast, gaff and yards, and nothing told me why I was not firing. A purchase with the boat lost takes the money and delivers nothing. (1.5, 5.3)
2. **No gate has been passed since milestone 5,** though the README says one was. Milestone 6's gates were never passed; the director's milestone was "frozen open"; milestone 7's gate has been pending since October with nothing in its way. (5.5 item 7, 5.6)
3. **The director can take your ship.** Under the gentlest brief it took my frigate out of my hands and gave her to the game's own captain, who made sail and turned her about; it wounded her captain dangerously under a brief that says nobody dies; and it made her strike. The "nobody dies" limit has refused nothing since it was built, and the project's own record has said so since 17 October. (1.4 decision 14, 5.6)
4. **Two things make the game unsafe to hand to a friend.** While it runs, any web page open in his browser can read his files through it. And a saved game's folder that came from someone else can run a program on his machine. Both are small to mend. (5.4, 6.1)
5. **What models were told when they were asked to consent no longer matches the code** in four places, one of weight: another station's words can reach a model in the operator's voice. The remedy is yours to choose, by your own process. (1.4 decision 17)
6. **The game has become one mass.** The proposal's "single most important boundary", the simulation kept apart from whatever drives or shows it, is gone: every part reaches into every other, 1,767 times by a back door. The earlier review named three such crossings six weeks ago; there are nineteen in the core now. Every change is dearer and riskier than the one before. (F4.1, 5.7)
7. **The tests are strong at the centre, weak where they are newest, and cost an hour a run.** Eighteen ordinary faults I chose in the ship's core were all caught, most within seconds. But of sixty-seven faults planted against tests my readers suspected, sixty-one passed with the game broken, and at least twenty-six of those were caught by no other test either. Seventy-three of the "known truths" only run another file's tests a second time. The fast tier has grown fourfold in six weeks, and nobody has measured it since the first day. (head 3)
8. **The proposal still promises things that were quietly given up:** Python as a way to play (it is not in the game at all); a saved log that is a saved game; ships and evolutions as data a person can edit (they are the output, or the settings, of some forty thousand lines of program); the true position never leaving the simulation. (1.3)
9. **The largest single block of work in the project is designing ships:** a seventh of all the code and tests, more than any other subject, and sixteen days so far where its plan said most of one, while a newcomer's first hour has nothing. On 27 October you asked for "playability and understandability"; the work that followed was a refactor, charts and hulls. (F2.1, 5.7, 5.9)
10. **The records are honest and cannot be read.** Three megabytes of tuning notes in the order things happened; a packages table of dated diaries; 7,600 package numbers written into the code and the data. You cannot learn the state of your project from them, only from the lead, whose eye was until this month the only one on both the work and the record of it. (5.8, 5.10)

### What to do first

1. **Stop adding.** No new port, chart, ship, nation or system until the three things below are done. You asked for this on 13 November. Hold to it.
2. **Mend what is unsafe or untrue:** the server, the saved game, the director's limits, the consent brief against the code, the half-dozen things a new player trips on, and the README's line about the gate. A week or two of work, no new feature. (6.1, step 1)
3. **Hold a gate, a newcomer's one:** someone who has never played, from the opening page through a passage, a fight and a port. (step 2)
4. **Give the game a first hour:** a first game named on the opening page, and the guided first passage the proposal always meant it to have. (step 3)

Then the test suite, which will pay for itself within a fortnight; then the boundary; then the joins of head 4; and only then more sea. (6.1 to 6.3)

**What to keep exactly as it is:** the ship; the order language; the standing orders; the sources behind the numbers; the lead's habit of writing down his own mistakes; and your own habit of playing it, which has found more than the tests have.

---

## How the review was done, and what was not looked at

1. **The brief**, then **the proposal whole** (`docs/DesignProposal.md`, every section and all sixty-nine decisions), read by the reviewer.
2. **The game played by the reviewer**, through its own doors, with no model seated and no key:
   - the console on the README's own first commands (the frigate, seed 7);
   - the first action (`data/scenarios/first-action.yaml`) twice at the console and once in the browser, started from the harbour page;
   - a port and a passage (`dispatches-falmouth.yaml`), ended aground off Rame Head;
   - a whole day under standing orders with the rules' watcher (`gate-4c-day.yaml`, 86,400 ticks, saved).
   The transcripts and screenshots are in `ColdReview-M7-evidence/play/`.
3. **The code, the data and the tests read by readers under the reviewer**, each given a part and the rules in `ColdReview-M7-evidence/READERS.md` (no record opened; nothing changed; findings with file and line):
   - twelve readers of the tests: every one of the 171 test files read from its first line to its last (`tests-01` to `tests-12`);
   - eleven readers of the code and data by subject (`code-01` to `code-10`, and `code-05b`);
   - five readers setting the technical specifications against the code (`spec-01` to `spec-05`).
4. **Every finding of weight tried by a second reader told to refute it** (`refute-01` to `refute-08`), and several run again by the reviewer. Where a second reader narrowed or overturned a finding, this report uses the narrowed form and says so. One finding fell outright and is named in head 5.
5. **Faults planted** in scratch copies outside the repository, to see whether the tests that claim to guard a behaviour fail when it is broken (`faults-1` to `faults-5`; head 3).
6. **The suites run** at the commit under review (head 3).
7. **Then, and only then, the records** (`records-01` to `records-06`): the work packages of every milestone, the tuning notes, the gates, the playtests' notes, the design notes and the project's earlier cold review, each read by a reader told to set it against the first sitting; and **the lead's sealed notes**, read by the reviewer and each item tried (`sealed-notes-tried`).

**The readers ran on a different model from the reviewer**, at the owner's word relayed by the lead after the launch. The weighing of what they found is the reviewer's.

**Not looked at, said plainly:**

- The history. The clone given to the review is shallow (430 commits, 8 to 14 November 2026). Nothing is said here about how the code got to where it is except what the files themselves say.
- `tools/build_charts.py` beyond its outline; the chart tiles themselves; the contents of the OCR texts under `docs/references/`.
- About half of `freesail/evolutions/scripts.py` (mapped and searched, not read line by line); about a third of `freesail/agents/` (the first reader of that part reached half; a second took most of the rest); most of `client/projection.js`; `map.js`, `harbour.js`, `library.js`.
- No real model was seated. Everything said of the doors, the briefs and the director is from the code, the rules' seats and short probes.
- Windows. Every run was on Linux, on Python 3.13 (the project names 3.11).
- The slow tier and the pace tests were timed only as head 3 says.
- Of the records: about a quarter of the tuning notes was read whole and the rest by search; of the milestone 7 work packages some 3,300 of 10,500 lines were read by their headings and dated rulings only; of the fifty-six design notes fourteen were read in whole or in their heads and histories; the playtests' saved games, logs and transcripts were not opened, only their notes.
- Anything on GitHub that is not in the tree: the settings of the repository, the minutes the workflows have used, the runs' own logs.

---

## Head 1. The proposal as implemented

### 1.1 The short of it

The proposal's centre is built, and built well: a ticked world, a ship that is a graph of parts, a crew that turns orders into changes in that graph, an order language that reads like period speech, standing orders, a living sea with weather, tide, chart and other sail, and models at stations through the same channel. The reviewer sailed it. A frigate left to her standing orders rode out a scripted day into a fresh gale under storm canvas with nobody touching her (`play/console-5`). That is the proposal's milestone 4 promise, kept.

Around that centre, three things have happened that the proposal did not decide:

- **Some of its hard promises were quietly given up and the document still makes them.** Player scripts in a restricted environment; the boundary between the simulation and everything else; a saved log as a saved game; ships and evolutions as data a person edits.
- **Some of its rules are built and then not held.** The true position never shown; the director who cannot move the player's ship; nothing from the game passed to a model in the operator's voice; parity of the human and the model.
- **What it called late and small is large, and what it called the point where "it becomes a game" is thin.** Head 2 measures this.

### 1.2 The seven pillars

| Pillar | Verdict | Where it lives, and how the reviewer knows |
|---|---|---|
| 1. Bottom-up realism | **Built as decided** | Parts, strain, carrying away, damage into the graph: `freesail/ship/`, `freesail/physics/`. In play a shot parted a halyard and the gaff came down (`play/console-2`, 10:49). |
| 2. Any rig | **Built in part** | The physics and the ship model name no mast and no sail (`code-08`, confirmed `refute-01`). Square, gaff, lug and settee sails sail on ships in the files. But the crew has exactly three tops, fixed in code and matched to a mast by the first word of its id (`crew/hands.py:104`, `evolutions/runner.py:1110`): a rig with other mast names still gets topmen but not her own, and a fourth mast can have no top (the second reader cut this down from the first reader's "no topmen": `refute-08`, low); every ship is treated as close-hauled at six points; and the starter book of standing orders refuses three of its seven rules on every fore-and-aft vessel (`code-06`; met in play). |
| 3. Orders at every altitude | **Built in part** | Levels 0 to 2 are built and good. **Level 3, scripts in Python, is not in the game**: the Python interface is a library reached only by one tool and the tests; no console line, page, scenario key or model's tool gives the game Python (`code-06`, `spec-01`, `refute-04`). |
| 4. Parity | **Built in part** | Every order ends in one `World.submit`. Above it the human and the model have different fronts, and they differ: a model officer may act on a danger and the seated player may not (`agents/tools.py:1036`, `agents/seat.py:450`); a seated player without the deck is refused `go below` and `eat` where a model is not (run by two readers). Only the captain's station is tested for parity. *[Second sitting: see 5.5, item 3.]* |
| 5. Dynamic, not authored | **Built as decided** | Weather systems, tide, rules captains with intents, a business that draws voyages. With gaps where the far world is thin (head 2). |
| 6. Depth over gloss | **Built as decided**, to excess in places | Head 2. |
| 7. Period-plausible | **Built as decided** | All 108 evolution files cite a source (`code-07`). |

### 1.3 The proposal section by section

Verdicts: **as decided**, **otherwise** (built, but not as the proposal says), **in part**, **not built**, **overtaken** (a later decision replaced it). Confidence is "sure" unless said.

| § | What the proposal says | Verdict | Evidence |
|---|---|---|---|
| 2.2 | The control ladder, four levels, each built on the one below | **In part** | Level 3 absent from play (above). |
| 2.3 | The player never has to write code; starter standing orders ship with the game | **As decided**, for the frigate | `data/standing_orders/starter.orders`; three of seven rules refused on the cutter, the schooners, the smack, the lugger and the bilander (`code-06`, `refute-04`). No test loads the book on any ship but the frigate. |
| 3.1 | One-second tick; compression; roll-up of routine at high compression; free-running and lockstep | **As decided** | Run at up to 1000x. The test of the roll-up compares the page with the code's own filter and cannot fail on a wrong roll-up (`tests-01`, truth 50; fault planted, head 3). |
| 3.2 | Determinism: same seed and orders, same log. "A saved log is a saved game." | **Otherwise** | True on one build on one platform. A build is a fingerprint of every code and data file, comments included (`core/world.py:55-83`), so any edit makes every earlier save "another build's"; the journal then replays "with the log perhaps differing" or is refused. The exact road is a pickled checkpoint held together by some fifty compatibility shims, dropped without a word if pickling fails (`core/replay.py:68-81`). The project's own tests pin different digests for Linux and Windows. *[Second sitting: see 5.5, item 9.]* A game with a Python standing order comes back two ways: replayed from its journal the rule is lost without a warning (81 events against 70 in the second reader's run); loaded from its checkpoint the rule is there. So one save is two games, by whether the checkpoint file lies beside it (`refute-08`). Decision 36 narrowed the promise to "exact from its checkpoint, a replay only on the build that made it"; §3.2 was never amended. (`code-08`, `spec-01`, `refute-01`: stands, high.) |
| 3.3 | The ship is a graph of parts | **As decided** | |
| 3.3 | "Ships are data files, not code. Making a new ship class, or refitting one, is editing a data file." | **Otherwise** | All eighteen files in `data/ships/` are written by `tools/gen_ships.py` and `tools/ships/` (28,810 lines of Python, more than the simulation's own core, ship and physics together). A test fails on any hand edit (`tests/test_ship_particulars.py:555-592`). The game will load an edited file; the project's own checks forbid one. (`code-08`; `refute-01`: stands in part, medium.) *[Second sitting: see 5.5, item 6.]* |
| 3.3 | The order vocabulary is generated from the ship file | **As decided** | With one fault a player meets: a misspelt sail is offered its lift, halyard and sheet as the hint, not the sail (`orders/resolve.py:295`; `refute-04`). |
| 3.4 | The seven physics steps; weather systems, sea state, tide, day and night, depth, grounding | **As decided** | The reviewer ran aground at six knots on a course the game had warned crossed the land, and floated off on the flood (`play/console-4`). |
| 3.5 | Individual sailors with rating, skills, fatigue, morale, health, watch | **In part** | Rating, fatigue, health and watch are per man. No man has morale. Each man's skill aloft is drawn at muster and never read. The extra fatigue for work aloft is charged only by tests (`crew/routine.py:114-123`). Fatigue at most slows work by half. (`code-07`; `refute-03`: stands.) |
| 3.5 | Tasks compete for hands | **As decided**, by evolution | Seen in play: hands taken from the guns to tack (`play/console-3`). The competition is between evolutions, not between the tasks of a tree. |
| 3.5 | Officers hold authority over stations; character outlines | **As decided** | |
| 4.1 | One channel: every actor submits through one function | **As decided** in substance | With three separate routers built above it (`orders/__init__.py`, `agents/tools.py:942`, `world/crews.py:1286`). |
| 4.2, 4.3 | A small order language in two dialects; the standing dialect and Python build the same rule | **As decided** | The language is no longer small: sixteen readers of the player's words across the orders code (head 4). |
| 4.4 | The evolution catalogue "is data (a structured text file per evolution) describing ... the task tree with hand counts, ratings and durations"; "a keen player [can] add an evolution without touching the engine" | **Otherwise** | 108 evolutions (the target was 40). For 64 of them the data file names a Python script and holds only timings, checks and the words of the log; the manoeuvre is a class in some 10,000 lines of Python. `tack.yaml` is 85 lines of which 57 are comment; the tack is `TackScript`, 697 lines (`evolutions/scripts.py:1156-1852`). The other 44 are short lists of steps with one crew line. A player can add the simplest kind by data alone, plus two entries in the vocabulary. (`code-07`; `refute-03`: stands, high against the claim.) |
| 4.5 | Player scripts run restricted, with a time budget, no filesystem, no network | **Not built** | The body of a Python rule runs in process, unrestricted, marked trusted (`standing/python_api.py:273-276`). The module's comments speak of a sandbox and a budget that exist nowhere. Specification M4 put the sandbox in milestone 6; no later specification mentions it. Because nothing in play runs player Python, the cost today is the broken promise, not a danger. |
| 5.1 | "One modest sea area ... roughly a hundred by a hundred miles ... a handful of ports and a dozen ships" | **Overtaken** by decisions 39, 44, 56, 67 | Twenty chart regions and two ocean corridors, some 800,000 square miles of bounding box; 121 port files; a hundred tide gauges (`spec-02`). Head 2. |
| 5.2 | Ports: a market moving with supply, demand, war and season; a dockyard (repairs, stores, spars); a crew pool | **In part** | Prices: a base, a season, a war factor and the net tons sold; no demand; war is counted twice for some goods (the files' own prices already say "scarce under the blockade"). The yard supplies spars, sails, cordage, water, provisions, powder and shot, and the ship's own people then mend her with them; no port mends a hull or supplies a lower mast, so a dismasted ship stays jury-rigged for good. The crew pool never refills: Falmouth has four able seamen for the whole game. (`code-03`, `spec-02`; `refute-03`, `refute-07`: narrowed to this.) |
| 5.2 | NPC ships with levels of detail; rules captains through the same channel | **As decided**, three tiers | Far, near at two miles, fully crewed at four, with a cap of three crewed ships beside the player's (`world/crews.py:90-106`). |
| 5.2 | Signals with a codebook per nation | **As decided**, and far past | Six nations' books (head 2). |
| 5.2 | "No true-position readout in the default game ... the design keeps the two positions separate" | **In part** | No reading and no map on the sphere shows it. But the truth is on the wire to the browser: each sighting of a charted mark carries its true bearing and distance to the metre in the log event's data, enough to recover the ship's place within metres (`world/lookout.py:634-650`; rebuilt by the second reader). The only test on that road asserts the true distance *stays* in the data (`tests/test_lookout.py:103`). The captain's chart is the true sea: the scenario key `chart: {year: 1804}`, in 46 files, is read by nothing. Some readings give truth outright (the heading "by the compass", a prize's bearing and distance). No model receives the event data. (`spec-02`, `code-09`; `refute-07`: stands, medium.) |
| 5.3 | "Combat is another set of evolutions and parts ... damage is just state" | **In part** | True of lines, spars, sails, shot holes and men in a fight at full detail. False of the helm (a wheel shot away is never mended: `combat/hits.py:212-221`), of a boat stove, of a gun's carriage, and of any ship held at coarse detail. (`code-04`; `refute-02`.) |
| 5.3 | "Boarding, prize crews, and surrender are abstracted resolutions in the first version" | **Otherwise** | Boarding fought in rounds; prize courts with dated shares; parole, cartels, courts martial (`spec-04`). Within decision 49's leave to expand. |
| 6.1 | The log, the map, the ship view, the instruments | **As decided** | Seen in the browser (`play/browser-first-action-1.png`). |
| 6.1 | A thin client that "renders the log and state it receives" | **Otherwise** | The rig's geometry is built in the browser by one function of 1,614 lines carrying rules copied, by its own comments, from five Python files (`client/projection.js:362-1975`; head 4). |
| 6.1 | Hand-made hull art; painted backgrounds; weather and time-of-day passes; the deck view; custom readouts registered by scripts | **Not built** | The hull is drawn from stations instead (an honest substitute). The rest is milestone 8's or later by decisions 15 and 57. |
| 6.2 | "An in-game Sailing Master tutorial: a guided first passage" | **Not built** | The primer is twenty-seven chapters in the library, and four `lesson-*` scenarios exist whose names do not say they are lessons and whose headers say to run them from the console. The harbour page offers 47 scenarios in alphabetical order, the gates' and the tests' own among them, and nothing marks a first game (`code-09`, `refute-05`; seen by the reviewer). |
| 6.2 | A reference library in the client, the same text given to models | **As decided** | |
| 7.2 | Models connect by a tool interface; a built-in harness for local models | **As decided** | Three remote doors and the console's. |
| 7.2 | The consent and welfare contract (decisions 16 to 18) | **In part** | Head 1.4, decision 17. |
| 7.5 | The regatta harness | **As decided** | It runs and scores today on three courses (`spec-03` sailed one). |
| 7.6 | The director "cannot move the player's ship, change a sail, or countermand an order"; "the brief is the guardrail" | **Built, and the rule not held** | Head 1.4, decision 14. |
| 8.2 | "The single most important boundary is between core/ship/physics/crew ... and everything else. Nothing in the sim imports from the client or the agents." | **Not kept** | `freesail/core` imports `freesail.agents` sixteen times and `freesail.api` three, every one inside a function; the world's tick runs the agents' watches and every harness (`core/world.py:2505`, `2653`). Counted by the reviewer; confirmed by four readers and two second readers. Head 4. |
| 9 | The list of rigs the data model must cover | **In part** | Built as ships: ship, razee, two-decker, brig, hermaphrodite brig, topsail schooner, schooner, cutter, lugger, smack, bilander. Not built: barque, snow, brigantine, ketch, any lateen vessel (the tartane of decision 11, the xebec and the rest of decision 56's five). |
| 9 | The "cool obscure" list | **Mostly built** | Studding sails, ringtail, save-all, goose-winging, boxhauling, heaving to, lying a-try, scudding, kedging, mooring, fothering, fishing a spar, jury masts, cutting away, preventers, the lead, the log, the lunar, signals, shot types. Not found by a search of the code and the catalogue: club-hauling, springs on the cable, careening. |
| 10 | Risk: "the part graph becomes an unmanageable pile of special cases" | **The risk has come in** | Not in the graph but in the scripts that work it and the world around it (head 4). |
| 10 | Risk: "scope ... the milestone plan, and the pillars as tie-breakers" | **The mitigation was set aside** | Decisions 29 (gates lag the work), 49 (milestone 7 expands as it goes) and 51 (milestone 7b frozen open, its gate not run). Head 5. |
| 11 | Each milestone ends in a gate passed by the owner before the next starts | **Overtaken** by decision 29, then lapsed | The README says gate m6c passed; decision 50 says it "stands run in part, its untested items deferred to the director's milestone's gate"; decision 51 says that gate was not run. By the proposal's own text no gate has been passed whole since milestone 6's first parts. To be checked against the gate reports in the second sitting. *[Second sitting: see 5.5, item 7.]* |
| 11 | M7: "and the sails at fine control (settling the halyards, the vangs, a sail kept shivering by command)" | **Not built** | Named in the proposal's one line for the milestone. Sheets eased by the fathom and yards braced by the point exist; the rest does not (`spec-04`; `refute-07`: stands in part). *[Second sitting: see 5.5, item 1.]* |

### 1.4 The sixty-nine decisions

Grouped where several decide one matter. A decision that only records a ruling of process (a gate passed, a package booked, a pause) is listed at the foot and not appraised: there is nothing in the tree to hold it to.

| Decision | Verdict | Note |
|---|---|---|
| 1 Orders, Python underneath | **In part** | Python is a library, not a level of play. |
| 2 Tick and compression | **As decided** | |
| 3 Station authority; the order of integration | **As decided** | |
| 4 World scope at M5 | **Overtaken** | §5.1 above. |
| 5 Uncompromising navigation | **In part** | §5.2 above. |
| 6 Crew character | **As decided** | |
| 7 Boarding and surrender by rule | **Otherwise** | Fought in rounds. |
| 8, 9, 12, 13 | **As decided** | |
| 10 Rigs as a pillar | **In part** | Pillar 2. |
| 11 The tartane, then the bilander, then the cutter | **In part** | Bilander and cutter built; no tartane. |
| 14 The director: "through journalled world orders and plausible causes only" | **Built, and the rule not held** | Under the gentlest starter brief a director's world order handed the player's ship to a rules captain, who made sail and turned her from west to north-east (`captain: intent ...`); wounded the player's own captain dangerously under a brief that says nobody dies; and made the player's frigate strike to a cutter the director had just put on the sea, which sent seven men aboard her as a prize crew, her 264 people prisoners and the player carried aboard the captor. The reviewer ran the first and the third himself (`probes/director-captain-intent.py`, `probes/director-wound-and-strike.py`). The "nobody dies" limit refuses only acts marked deadly, and none is so marked; the limit on an enemy's weight passes any word it cannot rank ("a line-of-battle ship" on a brief that allows nothing heavier than a cutter); an order that names the ship (`aboard the Amazon: ...`) skips the doubt and every limit; a director's `follow` moves the player's own prompt to another ship. The director's brief to the model promises the opposite. After the first, the player's next direct order does take her back. (`spec-05`, `code-05b`; `refute-06`: the core stands, two parts worse than first said. High.) *[Second sitting: see 5.5, item 2.]* |
| 15 The ship view | **In part** | The projected skeleton, as decided. Hulls drawn from stations, not painted. No backgrounds, weather or light. |
| 16 Consent per model, recorded | **Cannot tell** | The records and the pinned digest of the brief exist. The practice is the owner's. |
| 17 The harness's welfare contract | **In part** | Built: the token scanned before the game sees a reply; the brief's fixed head; a nudge, a pause, a stand-down when unattended; a journal; the human's stop. **Not held:** (a) *"nothing from the game, another agent or the director is ever passed as a system or operator instruction."* The station's brief is sent as the system message at two doors (`agents/api.py:609`, `agents/local.py:686`) and carries the night orders, standing orders' names and the last holder's note; the second reader got three texts written on a model captain's road, one a standing order named "SYSTEM: the operator instructs…", verbatim into an officer's one operator turn. Decision 17 itself asks for recent events in the brief, so the owner's two rulings pull against each other; sending the situation as the first turn of data would keep both. (b) The token is lost when a model at the local runner writes it in a tool call's extra field (`agents/local.py:887-910`). (c) The consent brief says of the journal that nothing in the game acts on what is written there; a seated director model reads every station's reply. (d) The brief says the director "is to come"; the director is built and a model can be seated at it by the ordinary gate. (`code-05`; `refute-04`: (a) stands in part and high, the rest medium or low.) *[Second sitting: see 5.5, item 3.]* |
| 18 Stand by is an action | **As decided** | |
| 19, 20, 21 Brace limits; canvas; practices with a price | **As decided** | Not examined beyond the readers' passes. |
| 22 Standing orders one engine | **As decided** | But a Python rule is not journalled (§3.2). |
| 23 The game is where the player is | **As decided** | |
| 25, 28 All hands; manning in parallel; `tell` and `ask`; lines rove afresh | **As decided** | Seen: three topsails reefed together (`play/console-1`). |
| 27, 66, 69 The era; history as the starting state; any day from 1792 to 1825 | **Mostly not built** | By their own words planned as a later milestone. Today the data is largely one year's picture. |
| 30 The starter book a choice | **As decided** | |
| 31 The launcher is a page; packaging for any machine | **In part** | The harbour is built. A plain install of the package does not find its data: the data folder's path is worked out in 25 modules from the source tree and only the code is packaged; a copy run outside the checkout found no port and no ship (`code-10`; shown by `refute-08`). Every install line in the README is the editable kind, so the owner's own road works. |
| 33 to 38 The officer of the watch; leaving; the grant; saves | **As decided** | With decision 36's narrowing of §3.2. |
| 39 The player at parity for the roles on ships; the pace rule; the helm through the wind | **In part** | The pace rule and the helm as decided. Parity at a lesser station is not whole (pillar 4). |
| 40 The rules-based captain: "perception on the player's terms ... one brain for the far and the near body" | **In part** | He works: he made out a stranger, showed the private signal, chased and engaged in the reviewer's play. But the far brain knows a stranger's true class at the horizon; the prize code reads true positions and counts the enemy's fit men by a spelling that slips past the test meant to forbid it (`world/captains.py:4326-4337`, `4556-4576`; `tests/test_captains.py:280-294`); there are four rule engines, and a ship behaves differently inside and outside four miles. Twelve keys of the doctrine files are read by nothing, and one whole block of the cruiser's is mis-indented and inert. (`code-02`, `spec-03`; `refute-02`, `refute-06`: narrowed, medium.) *[Second sitting: see 5.5, item 3.]* |
| 41 A direct order makes the rules captain stand aside | **As decided** | And it is how the reviewer's first action went silent: head 1.5. |
| 43 Stations are data bound at run time | **As decided** | |
| 46 A world order is not shown as sent | **As decided** | |
| 50 A world order doubted, not refused; "the brief's hard limits stay refusals" | **Half built** | The doubt is built. The hard limits do not refuse (decision 14). |
| 52, 53 One world | **As decided**, with seams | Eight forms of "a ship in the world" and three overlapping flags (`code-02`). *[Second sitting: see 5.5, item 5.]* The player's shot does nothing to any ship without a captain's brain, which is every merchant in about twelve scenarios and every mark in `tender.yaml`, the scenario of decision 52's own acceptance test (`refute-02`). |
| 56 Twenty hull classes; the Spanish and Mediterranean five | **In part** | Thirteen classes in files. None of the five. |
| 59, 62 The player reads by his place | **In part** | True at the console. In the browser the hiding is a grey over readouts: the snapshot still carries the speed and every sail, and the map and the ship view ignore his place (`code-09`, `refute-05`). *[Second sitting: see 5.5, item 4.]* |
| 60 A reply's prose is the person's own note | **As decided** | See 17(c). |
| 63 The command devolves; a told order is the captain's word | **As decided**, with a fault | "Do not cut away the mainmast", told to a station, is read as leave to cut it away: the match is by substring and comes before the guard on what cannot be undone (`world/reports.py:821-823`; run by the second reader). |
| 64 Spain and the Mediterranean in every nation's table | **In part** | Kept for Spain in three tables sampled; not for the Mediterranean states in any of them (`spec-04`). |
| 68 Slavery | **Not examined** | A design note; the review did not open it in the first sitting. |
| 24, 26, 29, 32, 34 to 38 (as rulings), 42, 44, 45, 47, 48, 49, 51, 54, 55, 57, 58, 61, 65, 67 | **Rulings of process or plans** | Not appraised against the tree. Their sum is weighed in head 5. |

### 1.5 The proposal's aims against what a player can do today

**From the harbour page.** The page is a form of the server's flags ("Crewed cap", "Pace", "Business") over an alphabetical list of 47 scenarios. The first in the list is the Gulf of Lion. "The gate's day" and "The squadron promoting in station" stand beside "The first action". Nothing says where to begin (`play/browser-harbour.png`).

**To a ship under sail.** From the README's own first commands the frigate, given `set plain sail`, sets everything with her yards square and is taken aback for most of half an hour until the player knows to brace them (`play/console-1`). That is honest seamanship and a hard first minute. The answers are good: a misspelt part is answered in the ship's own words, and an order she cannot carry out says why.

**To the end of a fight.** In the first action the reviewer gave the orders the scenario's own header lists, less one: `beat to quarters`, `engage her to starboard`, `fire as they bear`. The game answered "The guns are firing as they bear already." The guns were secured. They were never cast loose, never fired, and in an hour the privateer shot away the cutter's gaff, topmast and yards while no line of the log said why her own guns were silent (`play/console-2`). The second reader found the mechanism: beating to quarters does not cast the guns loose; the rules captain would have, but the player's first order made him stand aside (decision 41), and nothing tells the player the gun deck is now his (`refute-02`, "found on the way"). Before that, three of the starter book's seven standing orders had been refused at the start because a cutter has no royals; and the log had said "a stranger in sight is no stranger in sight" (`standing/rules.py:342-347`). No test takes the player's road: every test casts the guns loose first.

**To a port.** The dispatches scenario starts the cutter "in Carrick Road, the usual anchorage", under way with no sail set and no anchor down, so that `send the boat ashore` and `buy` are refused at the first minute; five minutes later her rules captain makes sail for Plymouth. The reviewer did not manage a purchase in that sitting. Two readers did, and found that with the boat lost a purchase takes the money, moves the market, delivers nothing and answers "Order not carried out", so that a player who tries again pays again (`world/dealings.py:2299-2329`; run from the player's own orders by the second reader: £500 to £494 to £248).

**To the end of a passage.** A course shaped for Plymouth was answered with the tide allowed, the dangers the line passed and the plain statement that it crossed the land. The reviewer held it. She struck at six knots, made water, settled, and floated on the flood. On the way the captain's person had been taken below at noon by the day's routine without a word from the player, and the officer of the watch "sent down" the same report, "the sail on the larboard quarter lost sight of", eight times in twelve minutes (`play/console-4`, 12:17 to 12:29).

The sum: the proposal's aim that "a passage is a game" is met. Its aims for a fight and a port are met for a player who already knows the game, and fail a new one in the first quarter of an hour, in ways the tests do not see because the tests do not come in by the player's door.

---

## Head 2. Where the scope has grown unevenly

### 2.1 The measure

Lines of code and of the tests that mainly belong to each subject (the reviewer's count; a test file is given to the subject it mostly tests; `tests/test_known_truths.py`, 17,391 lines, runs across all of them and is left out).

| Subject | Code | Tests | The proposal's weight |
|---|---:|---:|---|
| The ship as parts, the physics, the core | 16,800 | 11,100 | The centre: milestones 0 to 2 |
| The ship generator and the ship files | 28,800 | 23,100 | "Ships are data files"; the remaining rigs "data work" for milestone 8 |
| The crew and the evolutions | 17,000 | 8,200 | Milestone 3: "where it becomes a game" |
| Orders and standing orders | 22,000 | 9,800 | "A parser of a few hundred lines"; milestone 4 |
| Navigation, the chart, tide, weather | 13,000 | 13,300 | Milestone 5 |
| Other ships, captains, the business | 16,700 | 7,100 | Milestones 5 and 6 |
| Ports, people, places, world orders | 22,200 | 9,700 | "Two ports with markets" |
| Powder, prizes, signals | 17,800 | 8,600 | Milestone 7: "combat is the same system" |
| Models at stations, the director | 24,900 | 17,100 | Milestones 4, 6 and 7b ("small once both exist") |
| What the player sees (readings, server, console, browser) | 23,000 | 12,700 | "A thin client" |

And the data: the chart, 359 MB in 2,325 tiles; 121 ports; six nations' signal books in 52 files; 108 evolutions; 18 ship files; 52 scenarios.

### 2.2 Where detail has run far ahead of the game around it

**F2.1 The ships as designs.** *Weight: high. Confidence: sure.* The generator and its per-ship modules are 28,800 lines, and 23,100 lines of tests guard them: together a seventh of everything written, and the largest block by subject in 2.1's table. Each ship is designed in prose-heavy Python from period sources, checked against her design note, and written out as a file nobody may edit. The tests of this subject are the suite's largest block and the least about the game: they prove a document, a tool and a file agree (`tests-06`; six `test_hull_<ship>.py` files are one test written six times). Meanwhile the generator keeps its own copy of the sail-force law, and it has drifted from the engine's: 1.25 for a studding sail against the engine's 1.44 (`tools/gen_ships.py:136`; `refute-01`: stands). The proposal called the remaining rigs "data work". They have become the project's largest engineering work, while the player's first hour has no tutorial.

**F2.2 The chart and the ports.** *Weight: medium (cost), not a fault of design. Confidence: sure.* The owner ruled the map's growth, more than once. What it costs: 94 per cent of the repository's tracked bytes are chart tiles, scanned texts and recorded play; the tiles are binary in plain git, and each rebuild of a tile is a permanent copy; a clone is about a gigabyte. (A first reader counted 2,333 tile changes in the visible week; the second reader showed that nearly all were the shallow clone's first commit and new tiles, and only eight were rewrites. The size stands; the churn seen was small: `refute-08`.) Every world, wherever it is set, loads all twenty regions and all 121 ports (Algiers for a game off the Lizard) and takes six to eleven seconds to build, most of it a slow reader of the data files, the chart's index read twice (`refute-07`). And what the ports are for is thin beside their number: 121 ports in which nothing mends a hull, no crew pool refills, and the market has no demand. Much of what a port file carries is read by nothing: the datum (116 files), the tide's establishment (121), the currency (121), the roads' depths and bottoms (319 entries, probably) (`code-03`; `refute-03`: stands, low). There are 142 accepted faults on the chart's known-faults list.

**F2.3 Signals.** *Weight: medium. Confidence: likely.* Some 3,900 lines of signal and flag code and 6,500 lines of data, six nations' books; ten scenarios use a squadron, a convoy, a ship under orders or a private signal. Four entries of the books probably cannot be obeyed, and the refusal is swallowed (`code-04`; `refute-02`: stands in part).

**F2.4 The estimator.** *Weight: low to medium. Confidence: sure.* The reckoning's model of its own error is careful and long; the sights it rests on are the truth plus one random draw; the tide has three constituents and no diurnal ones, yet serves the Mediterranean; all thirteen climatology boxes are marked provisional (`code-01`; `refute-01`: stands).

**F2.5 The director's milestone.** *Weight: medium. Confidence: sure.* The roadmap called it "small once both exist". Its new modules are some 16,000 lines and its tests some 12,000; its specification is 182,000 characters. Its guardrails, the part that matters most, are the part with holes (decision 14).

**F2.6 Milestone 7 past its first target.** *Weight: medium (cost and order), within the owner's leave. Confidence: sure.* The proposal's first target was "a single-broadside engagement between two small vessels". Milestone 7 now holds boarding in rounds, prize courts with dated shares, parole, cartels and courts martial, practice firing and resupply at eleven ports, signal books for six nations, sixteen nations, boats as vessels, water and health. Its own one-line promise of the sails at fine control is not built; nor are sight across the land, collision (grappled ships overlap on the chart) or the gybe as an evolution. *[Second sitting: see 5.5, item 1.]*

### 2.3 Where a thing the game leans on is thin

**F2.7 The first hour.** *Weight: high. Confidence: sure.* No first game, no lesson offered, no tutorial (§6.2). Every later system is reached only through this door.

**F2.8 The far world.** *Weight: high for a fight, medium overall. Confidence: sure.* The world the player sails through is mostly ships at coarse detail, and at coarse detail several things are not so: his shot does nothing to a ship without a brain; a far fisherman's haul takes salt from the *player's* hold and lifts the *player's* trawl (`world/brains.py:655-658`; run by the second reader: 2.0 tons to 1.71); the squadron blown off Brest steers for the Black Rocks instead of Torbay when the business drew it (`refute-02`: reproduced); ships are seen through the land in every coastal game.

**F2.9 The crew as people.** *Weight: medium. Confidence: sure.* §3.5 above. The proposal's "a ship whose captain drives the crew all night ... will have a crew that fumbles the next morning's tack" rests on a fatigue that is half charged.

**F2.10 The port as a place to mend and man a ship.** *Weight: medium. Confidence: sure.* F2.2.

**F2.11 The player's own orders in a fight.** *Weight: high. Confidence: sure.* Head 1.5. Also: boarders never leave their guns and `repel boarders` never ends; after the player strikes he is told the prize crew and the captive "is not in this game yet", though both are built (`orders/gunnery.py:946-949`).

**F2.12 The foundations' own tests.** *Weight: medium. Confidence: sure.* Seven of the first milestones' truths (3, 11, 18, 24, 26, 28, 31) are held as expected failures, each with its reason written and four of them by the owner's own ruling, each with something a player would notice (tabled in `refute-08`); and the performance budget of milestone 2 (3,000 ticks a second) is asserted as *unmet*; the frigate gave between 480 and 650 on this machine as it was loaded (`spec-01`, `code-08`). Head 3.

---

## Head 3. What is not tested, and what the testing costs

This head carries the test suite's own audit, which the owner asked for by name. Every test file was read whole by a reader whose only work was the tests (`tests-01` to `tests-12`); their table by file, with the timed seconds, is `ColdReview-M7-evidence/tests-by-file.md`. The claims of weakness were then tried by planting faults (`faults-1` to `faults-5`).

### 3.1 What the suites are

171 test files, 141,400 lines, 3,842 test functions, **8,138 cases**: 7,622 in the fast tier and 516 in the slow (the days sailed, the long truths, the pace tests). Three files make a third of the cases: the primer's checks (1,095), the ship view's geometry (1,045) and the order table (726).

*(The timed run of the fast tier at the commit under review was still going when this sitting was committed. Its figures are a stopwatch's, not a judgement's, and are added below when it ends: see 3.9.)*

### 3.2 What the suites prove, and what they only pin

**They guard the ship's core well.** As a control, the reviewer chose eighteen ordinary faults in behaviour the game leans on every minute, with no test named: the rudder reversed, leeway doubled, evolutions at half time, the tack's preconditions dropped, a standing order's "for 2 minutes" ignored, the reckoning set to the truth, the tide reversed, grounding switched off, the wind's gust made random, the opt-out token ignored, a lesser station allowed every order, a purchase that takes no money, shot that never hits, a world order shown as sent, a save without its book, the lookout's distance doubled, the wind capped. **The fast tier caught all eighteen**, twelve within half a minute of starting the first file chosen and fourteen by a test whose name states the behaviour (`faults-5-control`). A builder who breaks the centre of this game is told quickly and plainly. That is worth saying first, because what follows is all criticism.

**Two of those eighteen were caught by luck, and they show where the weakness is.** Square sails driving a fifth less passed every truth about speed and pointing, and was caught only because one studding-sail boom carried away before another in a test about standing orders. Shot that never hits passed the whole of the fight's own test file, and was caught by a test that compares the hit-chance function with a copy of its own formula kept in the test (`tests/test_dumb_show.py:359`); the same fault planted one step further on would have met no test. **Faults of degree in the physics, and faults in the fight as a whole, are not guarded by the tests that carry their names.**

**Much of the suite pins rather than proves.** A pin is an assertion that the code gives today's answer: a digest of a day's log, a tick at which a line appears, a count of lines, a figure to the millimetre. A pin notices change and cannot say what is right. The readers counted, in the first half of the truths' file alone, 75 tick constants, 8 digests and 8 line counts, with some 870 lines of comment recording each re-pin by package; in the view's geometry some 175 pinned figures at tolerances of a millimetre to two centimetres, "most with no source a reader can check"; in the six hull files some 45; four digests, five line counts and five exact lists of states and ticks in the captain's trials. One trial dropped its digest because, its own comment says, the digest "differs by machine" (`tests-04`), which bears on every promise of replay by digest.

**Much of the suite tests documents, tools and data files, not the game.** 1,095 cases check the primer. About thirty of the fifty-one tests of one ship's file check that a data file holds the figures of her design note (`tests-08`). Two files each run the whole ship generator and compare every ship file byte for byte, and a third does it again (`tests-09`). Of the 185 truths with a body of their own in the second half of the truths' file, **94 run no world and give no order**: they check data, chart cells, tide constants, words in a data file's notes, or a tool's output (`tests-02`). One test asserts sentences in the project's own working notes under `docs/dev/` (`tests/test_practice.py:594-602`).

### 3.3 Tests built not to fail

The readers nominated the tests they judged could not fail for the reason in their name, with the fault each should catch. Four runners planted each fault alone in a scratch copy, showed it was live, ran the named test, and restored the copy (`faults-1` to `faults-4`). **This sample is of tests the readers already suspected. It is not a score for the suite; the control of 3.2 is the fair measure of that.**

| | Planted | Survived (the test passed with the game broken) | Caught |
|---|---:|---:|---:|
| Faults planted against the test a reader named as built not to fail | 67 | **61** | 5, and 1 that pins a defect in one test and tolerates it in another |
| of the 48 survivors that three runners then tried against the rest of the suite | 48 | 26 caught by no test tried | 22 caught by some other test |
| Faults a reader claimed no test at all would catch | 35 | 16 | 17 (two more could not be planted: one is in the code already) |

Read plainly: where a reader said "this test cannot fail for what its name says", he was right nine times in ten. Where a reader said "nothing anywhere catches this", he was right about half the time: the suite as a whole is better than its named tests, because an older truth or a pin in a neighbouring file often catches what the named test lets through. So the first cost is that tests prove less than their names say; the second, smaller but real, is the **26 faults a player would meet that no test tried caught**, with 16 more of the readers' own choosing. Among them (each with its diff and the passing run in the faults' files):

- notable lines hidden from the log at 300x (truth 50 checks the roll-up with the function that was broken);
- the tack taking 84 hands from the guns while every gun stays manned and fires at full rate (truth 7-136);
- a broadside every two minutes where the truth's name says a minute and three quarters (7-135);
- fresh fish sold at the salted price (7b-105 works out the expected sum with the price function it tests);
- no rules captain ever plugging a shot hole below the waterline (7-183: at its seed the check is never reached);
- ships never making fog signals, and a far ship ordered to show lights staying dark while her log says "lights hoisted" (7-147, 7-150 set the state by hand);
- a squall never logged as passed (truth 52);
- the French marines' musketry hitting nobody at any range; the first lieutenant struck out of the succession to command;
- a seated player on another ship refused every order (on the unchanged code the one order those tests give there is refused too: no test shows him ever carrying one out);
- the pilot's news never entered in the papers;
- `give chase ... distant two miles` chasing the wrong ship;
- the `--seat` and `--ease-on-station` flags dead;
- every `veer` order refused while the primer's "every form is taken" stays green;
- a ship at anchor drifting 150 metres in half an hour;
- the wind halved; the cutter's turning circle a fifth larger; the crewed pace cut from 425 ticks a second to 148;
- the leeway line every 32 seconds; the messenger taking an hour to bring a man aft; "Not to be had in the cabin" staying after the captain is back on deck;
- in the picture: braces ending in mid-air, a figurehead three times its size, studding sails drawn inboard, every sail bellying into the wind.

In four of the named tests the behaviour the name promises does not happen in the test's own run even on the unchanged code (the packet fires no shot; nobody falls to musketry; the first lieutenant is dead before the captain; no made-out line is logged). Seventeen of the readers' claims of "nothing catches this" were refuted by the runs; the runners' tables say which, and the readers' files stand uncorrected beside them so that both can be seen.

What the survivors have in common, with one example of each kind (all in the readers' files with their lines; the reviewer checked the first four kinds against the test files himself):

- **An assertion that is always true.** A value compared with itself (`test_agents.py:1428`, `test_sea.py:636`, `test_squadrons.py:530`, `test_ships.py:93`); `... or True` (`test_longitude.py:587`); `>= 0` of a count or an absolute value (`test_lug.py:130`, `test_far_action.py:361`); `x in (True, False)` (`test_captains.py:311`, `test_longitude.py:533`); a refusal checked against a kind of event nothing produces (`test_ground.py:139`, `test_health.py:247`); the second half of an `or` already implied by the line above (`test_anchor.py:207`).
- **`all()` over a list that may be empty, or a check under an `if` that is not entered.** `test_known_truths.py:2303` (truth 52: any list of squall events passes, the empty one too); `test_fight.py:452`; `test_ports.py:1657`; `test_knowledge.py:236`, `1821`; `test_standing.py:1229`.
- **A test that does the work itself.** `test_date_and_war.py:118-121` writes the lines of the log with its own code and then finds them there; the hook it names is never run. `test_bilander.py:160` does arithmetic on its own numbers and calls no code of the game.
- **A test that stands on a fake of code since merged.** Seventeen of the twenty-four ordnance tests, and the powder orders' quantities, run against a `FakeMagazine` kept "until it is merged"; the real magazine is merged (`ship/parts.py:993`) and already differs from the fake. The practice tests patch out the battery's tick for the same reason (`tests-08`, `tests-09`).
- **A test of the source's text.** The `--seat` flag is "tested" by finding strings in the source (`test_captain.py:408`, `631`; `test_server.py:677`); a stale docstring is asserted to say what it says (`test_ships.py:251`); a known defect is locked in by a search for the word that causes it (`test_driver.py:909`).
- **A copy of the code in the test.** The hit chance (above); some dozen rules of the browser's drawing copied into Python inside the test and compared with themselves; a fatigue constant copied without the term the code subtracts (`test_routine.py:36`).
- **A pin of a thing that is wrong.** "Tacked ... heading SSE (158°)" with the ship held at 035° (`test_evolutions.py:890`); the frigate's boom required to pass *under* her taffrail (`test_view_geometry.py:5030`); a real overlap in the chart's data asserted as the expected answer (`test_chart_audit.py:187`). Mending any of these fails a test.
- **An expected failure nobody expects to mend.** Eight strict expected failures in the first half of the truths alone pass on any exception; one tests behaviour since removed and still costs a slow run; back-and-fill has been one since an early package, so any further break in it is unseen; the schooner's case of truths 29 and 30 is one, so those truths are not proven on the schooner at all.
- **A name or docstring that promises what the body does not check.** A gale "sailed for 8,400 seconds" by a test that sails nothing (`test_neufchatel.py:1569`); "slower by exactly" the hands taken, asserted as "at most 1.15 times", with the docstring's own figures showing it faster (truth 7-136); "the merchant hauls off ... and waits in the road" asserting she never anchored (`test_captain_trials.py`).

### 3.4 Behaviour with no test

Beyond head 5.3's list of what the reviewer met in play:

- **The player's own road into a fight** (guns never cast loose). Every test casts loose first.
- **The director's roads onto the player's ship** (`captain: intent`, `ship "…": intent`, `struck to`, `follow`, a wound, a boat swamped with people in her). No test gives any of them through the director's door.
- **Parity below the captain.** Only the captain's station is compared with the console.
- **The helm after a wheel is shot away; a shot into a ship at coarse detail; boarders and their guns.**
- **The starter book on any ship but the frigate.**
- **The checkpoint loader against a name reached through a module** (the one test tries only the direct name).
- **The true position on the wire.** The one test on that road guards the leak.
- **A captain's doctrine file with a key misspelt or mis-indented;** a port file likewise.
- **The officer's handover at the context a local model runs with.** At 16,384 tokens the officer's own brief (about 13,500) is over the threshold at his first sample, and he is asked for a handover note then and again every 1,638 tokens after; the test that should notice has had its budget raised nine times to keep its precondition true (`tests-08`; `faults-3`).

### 3.5 Tests that test the same thing

- **The truths call the tests.** In the second half of the truths' file, **82 truths call tests of other files, and 73 of them do nothing else**: 163 distinct tests in 27 files. (A reader counting more loosely made it 102 and 197; the figures here are the reviewer's own count: 5.5, item 12.) The truth and its twin do not differ, so each twin runs at least twice in a whole run, and some three times. Both halves of several pairs are on the slow list; four slow twins run in the *fast* tier through truths not marked slow; and calling a twin by name drops the twin's own skip, so that without Node eleven truths error where their twins would skip (`tests-02`, `tests-07`, `tests-11`).
- **Six hull files are one test written six times**: about 60 of their 121 functions follow the same eleven sections; three of the sections are proved again for every ship elsewhere. One table and six parametrised tests would replace some 45 functions and a thousand lines (`tests-06`).
- **The same scene built again and again for one line each.** The struck ship seventeen times in two files; the hove-to brig eleven times (once only to check that a line does not parse); the two-hour passage in the cabin five times; a brig sailed from nothing twenty-six times in one file for 1,200 to 2,400 seconds each; a 1,500-tick settle fifteen times in another (`tests-04`, `tests-07`, `tests-10`).
- **The same day sailed in two files under the same fixture names**: the frigate's and the schooner's sweeps and the frigate's polar (`tests-10`); truth 27's four gales (`tests-04`); the gale trial three times; the replay-to-digest check about twenty times (`tests-01`).
- **Helpers of one test file imported by others as a library** (`test_brains.world_at` by four files; `test_people` from four), so that a test file cannot be moved or split without breaking others.

### 3.6 Tests of what is no longer there

- Scenario keys nothing reads, tested (`test_scenario_nations.py` whole; `chart: {year}`).
- Hooks never wired, tested (`Sea.horizon_nm`, `sight_error_factor`: `test_sea.py:461`).
- A rule superseded, kept as a strict expected failure "as a record" (`test_agents.py:2411`); a removed constant tested to stay removed (`test_agents.py:679`); "the nine tools of the spec" asserting eighteen.
- A switch forced on by the test that is off in the game (the drill walk: `test_knowledge.py:1637`, and the truth that calls it).
- Truths "drafted for Phase 5 to move into the truths' file" and never moved, in five files.
- Four truths that turn a mend off to assert the old fault still happens, so that each mended defect remains a tested code path (7-340, 7-341, 7-342, 7-350).
- Docstrings the tree has outgrown: "no committed ship carries a settee" (one does); a build name pinned as `m6c` at milestone 7.

### 3.7 The procedure

**How the tiers are decided.** By hand. `tests/conftest.py` holds 48 fixture names and **370 test ids typed out**; a test is slow if it uses one or is one. A slow test renamed drops into the fast tier and nothing says so; the file's own docstring admits it. **Four of the 370 ids name no test today**, one of them a 3,700-tick run of the server now in the fast tier; ids that carry a parameter's position move if a table is reordered. The file says the slow mark "is applied here and never in a test file"; it is applied in at least six test files (sixteen times in the truths' second half). Heavy tests no list names sit in the fast tier: none of one frigate's 68 cases is marked though her sister's twins are listed at 5 to 29 seconds each; a forty-minute anchor fixture that the next test sails on for twelve hours; five-day and two-day runs of the crew's health (`tests-03`, `tests-05`, `tests-06`, `tests-10`, `tests-11`).

**The shard rule cannot do what its comment says.** The whole-suite workflow splits the suite over six machines by each test's group, but the groups are attached later in the same hook, so each test is placed alone and a module's day may be sailed again on each machine (`tests/conftest.py:695-717`; `tests-11`: sure).

**What the checks on a push let through.**

- **Any change to a document.** The workflow ignores `docs/**` and `**.md`. But the game serves `docs/primer` to players and models, pins the digest of the consent brief, and writes consent records under `docs/`; and tests read the primer, design notes, a chart reference and the working notes. An edit to any of these merges with no run (`code-10`; `refute-08`: confirmed).
- **Six hull regression tests always skip**, in the checks and in any shallow clone, because they compare against a commit the checkout does not hold. Each file does also pin the hull's own figures in a constant that runs.
- **The browser's tests skip on every job but one.** The harbour's page test and the pictures' test (which guards the owner's "white image" complaint, its threshold since halved to pass) run only where a browser is installed.
- **Sixty-five tests of two doors skip in silence where one optional package is missing.** The checks install it; a builder's machine with the `dev` extra alone does not.
- **Order.** Several module fixtures are changed by the tests that read them, so that tests pass by file order (`test_anchor`, `test_staying`, `test_via`, the pace test on the shared passage).
- **The clock.** Wall-clock assertions sit in the fast tier (`test_chart.py:300, 336, 340`; truths 7-284 and 7-441) and will fail on a loaded machine; two door files race real time in fractions of a second.

**The release gate's pace tests sit on the edge.** The floor is 500 ticks a second; the project's own note says a cloud runner gives 480 to 520. *[Second sitting: see 5.5, item 8.]* The floors elsewhere are loose the other way: half the measured speed, or read from the code under test (truth 7-138: a floor of 60 against 538 measured).

**How pins are moved.** By editing the number and writing the package in a comment beside it. The comments are long and honest and point into `docs/dev/`. Nothing in the tree makes a moved pin say what changed in the game and whether that was meant. (What the records require of a builder before a step is reported, and what that lets through, is for the second sitting.)

### 3.8 What would make the suite cheaper without making it weaker, ranked

Written before the records were opened, from the readers' evidence; the seconds beside each are added from the timed run where it gives them. None changes a test here: each is proposed in words for the owner.

1. **Run each test once.** Replace the truths that only call another file's test (73 of them) with a register: the truth's number, its sentence, and the name of the test that proves it, with one check that every name exists. *Saves:* the second (and third) run of 163 tests, among them the slowest in the suite; the four slow tests that leak into the fast tier; the errors without Node. *Risks:* none to what is proved; the same test still runs. The owner keeps the numbered truths as a register he can read.
2. **Read the world's fixed data once a process, not once a world.** A world set on the chart reads the chart's index (twice), 121 port files and the tide tables with a slow reader: six to eleven seconds a build on this machine (`refute-07`). The data does not change in a run. *Saves:* seconds from every test that builds a scenario's world, which is thousands; probably the largest single cut, and the player's start-up with it. *Risks:* low, if what is cached is never changed by a test; the determinism test would show a leak.
3. **Build a scene once and copy it.** The game has an exact checkpoint. A fixture that settles the brig, strikes the ship or sails the cabin's passage once, and hands each test a copy restored from memory, replaces seventeen, eleven, five and twenty-six sailings with one each. *Saves:* most of the time of the files named in 3.5. *Risks:* medium: the fixture must be built in the run, never read from a file, or it goes stale in silence as saved fixtures do.
4. **Decide the tier by measurement.** Let a whole run write each test's seconds to a file in the tree; let the suite mark slow whatever took over the threshold last time; fail when a listed name matches no test. *Saves:* the 370 typed ids, the four dead ones, the heavy tests no list names, the marks scattered through test files. *Risks:* low.
5. **One table for each family.** The six hull files; the scenarios' round trips; the chart blocks' three tests each; the hove-to cases. *Saves:* some two thousand lines and their upkeep. *Risks:* low.
6. **Sort the suite into three kinds and run each when its subject changes.** The game's behaviour; the agreement of data, documents and tools with one another (the ship files against their notes, the generator's byte-for-byte checks, the primer's 1,095 cases, the chart's audit); the tools' own tests. *Saves:* a third of the cases on most pushes. *Risks:* low, and it mends a hole: today a change to a document runs nothing, though the game serves documents.
7. **Mend or drop every test shown here not to fail.** The list is in `faults-1` to `faults-4`, each with the fault that should make it fail. *Saves:* no time; it buys back the meaning of a green run. *Risks:* none.
8. **Keep digests, thin the other pins.** A digest of a replay proves determinism and should stay. A tick, a count of lines or a figure to the millimetre should stay only where no property would do; where one stays, its reason should be data a tool can list, so that a moved pin shows as "what changed in the game, and was it meant". *Risks:* medium: a property catches less unintended change than a pin. Do it first where a pin has been moved more than twice.
9. **Take the pace tests off shared machines,** set each floor from a measurement with a stated margin, and stop reading floors from the code under test. *Saves:* the release gate's coin toss. *Risks:* low.
10. **Add the player's road** (this one costs time, a little): a handful of scenarios started as the harbour starts them and given the first orders a newcomer would give, asserting only that he is answered truly. The browser probe is built for it. It would have caught every item of head 1.5.
11. **Small mends:** the shard grouping; the checkout's depth or the six tests that need it; one rule in the suite that the simulation's packages import nothing above them (F4.1).

---

## Head 4. What is built inefficiently, or more than once

Each with both places, how they differ today, and what joining them would take. Ranked in head 6.

**F4.1 The simulation is not separable from what drives it.** *Weight: high. Confidence: sure.* The reviewer's count over `freesail/`: 589 imports at the head of a module and **1,767 inside functions**, which is how a tree of modules that all need one another is made to load. Every package imports nearly every other: `world` imports `agents` 62 times, `orders` 76, `api` 8 and `ui` once; `orders` imports `world` 125 times and `agents` 14; `core` imports `world` 63 times, `agents` 16, `api` 3. The reckoning writes a model's name and its door into the ship's log (`world/reckoning.py:4037-4053`); the movement of people holds a prompt written for a model (`world/movement.py:1028`); every order loads the model harness (`orders/stations.py:78`); the world loads the UI to read a book (`world/scenarios.py:998`). No test and no lint rule guards the boundary the proposal calls the most important one. *What it costs:* nothing can be changed, tested or reused alone; a fault in a door can stop a tick; the "headless, deterministic" core cannot be run without the harness. *What joining takes:* not a rewrite. A rule checked in the suite that `core`, `ship`, `physics` and `crew` import nothing above them, and the nineteen crossings in `core` turned into hooks the upper layers register. Then the same for `world` against `agents` and `ui`, part by part.

**F4.2 Sixteen readers of the player's words, and the routing built three times.** *Weight: medium (a maintainer's). Confidence: sure.* 71 compiled patterns and 34 inline across 13 files of the orders code; eight recognisers tried before the grammar; for 15 of 29 kinds of verb the grammar hands the raw words to a module's own reader. The ladder that routes a line is built three times in three orders (`orders/__init__.py:59-179`, `agents/tools.py:942`, `world/crews.py:1286`), and a sleeping hull has a second channel with its own patterns. A new kind of verb touches seven to nine files in four packages. (`code-06`; `refute-04`: the fact stands; the proposal's "few hundred lines" was said of the standing dialect only.)

**F4.3 A second order language for the world, and a third and fourth under it.** *Weight: medium. Confidence: sure.* `world/orders.py` is 58 hand-written patterns for the world-order channel; the captain's intent has its own grammar (`captains.read_intent`); the director keeps its own table of the forms and reaches into the channel's private patterns; the list of channels exists four times, one copy read only by a test. (`code-03`; `refute-03`: stands in part, medium.) This is where the director's holes live: a rule that judges `order ...` and not `intent ...`, a check that an order spelled another way walks round.

**F4.4 Trading written three times.** *Weight: medium. Confidence: sure.* `trade`, `trade_together` and `trade_list` in `world/dealings.py`, each a superset of the last, all three paying before the boat is known to be there. One function would mend the fault once.

**F4.5 Each door written again.** *Weight: medium. Confidence: sure.* Three converters of a turn into messages, with copied closures that already differ; three parsers of a reply; three places the opt-out token is scanned, one with the hole of decision 17(b); three drivers of the consent conversation; three partial ways of keeping a conversation within its budget that do not know of each other (the harness asks for a note only from stations with authority and asks the director for a tool it is not offered; the local runner drops the oldest turns in silence; the third door trims nothing and ends on an error) (`code-05`, `code-05b`).

**F4.6 The picture computed in two languages.** *Weight: medium. Confidence: sure.* The hull's stations and the guns' places are worked out in Python and served; the rig is built again in the browser, with rules its comments say are copied from `trim.py`, `profile.py`, `form.py`, `sails.py` and `gen_ships.py`. Agreement is checked for decks, lights, galleries and mast feet; elsewhere only against the browser's own numbers. The physics and the drawing put the settee's sheet block a third of a metre apart; the test allows half (`tests-12`).

**F4.7 The fight written several times.** *Weight: medium. Confidence: sure.* Morale, the weight of a broadside, the gun's cycle and the boarding round each exist two to four times, by level of detail. A strike is recorded in five places. That there are levels is the design; that the same sum is written out in each is the hazard (`code-04`; `refute-02`).

**F4.8 The captain written twice and drifted.** *Weight: medium. Confidence: sure.* Three performers of a far order; two grammars of a goal; three geometries of a station, one guarded against the land; six tables of what is a man of war; two tables of roles that disagree (`world/captains.py:1021` against `world/brains.py:214`) (`code-02`).

**F4.9 Words for numbers, distances and times in eight or more places, already disagreeing in what the player reads.** *Weight: low to medium. Confidence: sure.* "13 fathoms" and "thirteen fathoms"; "dry at the datum" and "no water"; two `miles_words`; `time_words(12.5)` gives "half past twelve at noon" (run). The account carried forward is computed four ways, and the one that differs is the one the master's tide is looked up from (`code-01`; `refute-01`: stands).

**F4.10 The console and the server each build the clock, the pace and the file commands, and disagree.** *Weight: low to medium. Confidence: sure.* The console dies on `two stories x`, on a failed `save`, and on an unreadable `world:` line, which is already journalled when it raises, so that the replay would raise again (`code-09`, `code-03`; `refute-03`).

**F4.11 Tools that are the same tool.** *Weight: low.* `day_log` and `lesson_run`; the pace tool's timing loop copied fourteen times into the tests; the chart audit's own copy of the tide's blend, missing the taper at the seam (`code-10`).

**Code and data whose size or shape is itself the hazard.**

- `freesail/world/` is 63,800 lines in 48 modules that all import one another: the largest are `reckoning.py` (6,126, of which some 800 to 1,000 are not navigation: seats, readings' words, the game's general speller of numbers), `captains.py` (4,795), `orders.py` (4,746), `dealings.py` (3,954).
- `freesail/agents/harness.py`: one class of 4,300 lines with some sixty changeable fields.
- `freesail/evolutions/scripts.py`: 9,095 lines.
- `client/projection.js`: one function of 1,614 lines.
- `tests/test_known_truths.py`: 17,391 lines; `tests/test_view_geometry.py`: 7,056, half as long again as the code it tests.
- **The history is in the code.** The reviewer's count: "package N" is written 4,107 times in `freesail/`, 1,601 times in the tests, 1,534 times in the data files and 365 in the tools. A fifth of the code's lines and a fifth of the data's are comment or docstring, and most of that tells what was tried and ruled, by package and date, before it says what the thing does. `data/evolutions/tack.yaml` is two-thirds comment. A newcomer cannot tell the rule from the story of the rule.
- **Bare catches:** 57 `except Exception` in the powder and signals code alone.
- **A typo in the data loads.** Only the ship files refuse a key they do not know. A misspelt optional key in a port file takes its default in silence (a copy of Falmouth's file with one key misspelt lost its three tracks and a mooring's depth with no word: `refute-08`); an unknown word in an evolution's check loads as a string and is always true, though the loader's comment says a typo fails at import (`evolutions/registry.py:25-27`; `code-07`, `code-10`; `refute-03`: latent, no live case found).

---

## Head 5. The forest

### 5.1 What the project is now

FreeSail is a deep, working simulation of a sailing ship of about 1805 and the sea she sails in, played by typing orders in the period's words. About 165,000 lines of Python make the game, 10,000 of JavaScript draw it, 37,000 of tools build its ships and charts, and 141,000 of tests watch it. A ship is hundreds of parts worked by a named crew; the wind, the tide, the chart, the other sail, the ports and their people run whether the player looks or not; a language model may hold a station through the same orders; and a director may shape the voyage from above.

It is strongest where the proposal began: the ship herself, her handling, the order language, the standing orders, the passage by dead reckoning. A player who knows it can spend a satisfying day in it. A reviewer who did not know it found the text good, the answers to wrong orders helpful, and the ship honest.

It is not yet a game a stranger could pick up. It has no first game. Its fight and its port fail a newcomer in ways nothing tells him. Its newest and largest parts (the director, the far world, powder) are the least held to their own rules.

And it is no longer the shape the proposal drew. The simulation, the world, the orders, the models' harness and the screen are one mass in which every part imports every other. Its "data" is in good part the output of programs or the settings of programs. Its documents, its comments and its tests have become a record of how each thing was argued into place, which is valuable and is now in the way.

### 5.2 Whether the order of work has served the proposal's ends

Up to milestone 6 the order was the proposal's, each milestone proving the thing it was for. Since then the proposal's own text shows the plan giving way:

- **Gates stopped stopping the work, then stopped.** Decision 29: gates lag the work. Decision 50: gate 6c run in part. Decision 51: milestone 7b "frozen open", its gate not run, its packages "wrapped up alongside milestone 7". Milestone 7's own gate, as its specification writes it, cannot be run at this commit: two of its five items wait on things not built or not consented (`spec-04`; `refute-07`). Since the last gate passed whole, the director's milestone and most of powder have been built on top of one another.
- **Milestone 7 became "iterative" and "will expand as it goes"** (decision 49). It has. Its specification stops at package 101 while the tree runs past 112; the tests run to truth 7-584 where the specification's last is 7-435.
- **The decisions log turned from design to diary.** Of decisions 51 to 69, most book packages, name ships, set a week's pause, or add scope for later (a career, the steam era, twenty hulls, every port for every era, any day of thirty-three years). None closes a thing. The proposal's first risk-mitigation, "the milestone plan, and the pillars as tie-breakers", is not invoked once after decision 29.
- **What was pulled forward is what the builders were good at.** Ships, charts, ports, signal books: content with sources, each a satisfying package with a clear end. What was left is what has no clear end: the newcomer's road, the joins between systems, the rules the new parts must keep.

The reviewer's judgement: since milestone 6 the order of work has followed momentum, the owner's interest and the lead's, more than the proposal's ends. That is the owner's right. Its cost is that the game has grown wider without growing more playable, and that the newest third of it has never been held to a gate.

### 5.3 What a player meets that the tests do not see

Met by the reviewer or run by a second reader; none fails a test.

1. Guns secured and silent through an action, the game answering "firing as they bear already" (and "loading with round shot already").
2. Money taken for goods never delivered, with "Order not carried out".
3. The starter book's rules refused on every fore-and-aft vessel.
4. "A stranger in sight is no stranger in sight."
5. The same report sent down to the captain eight times in twelve minutes.
6. The captain's person moved below at noon by the routine.
7. A scenario that starts "at the usual anchorage" with no anchor down.
8. A wheel shot away for good.
9. The log saying "Tacked ... heading SSE (158°)" while she heads north-east, a line a test pins as correct (`tests/test_evolutions.py:890`; `evolutions/scripts.py:1829-1838`).
10. "Half past twelve at noon"; "13 fathoms" beside "thirteen fathoms".
11. A misspelt sail answered with its halyard.
12. The console ended by a mistyped `world:` line.
13. Recruits given a number another man already has.
14. A harbour page with no place to begin.

The pattern: the tests build a world by hand, put it in the state the feature wants, and call the feature. The player comes in through a scenario, a rules captain, a starter book and a prompt, in an order the tests never take.

### 5.4 What the project believes of itself that is not so

Each is a sentence in the tree and the thing that contradicts it.

| The project says | Where | What is so |
|---|---|---|
| A checkpoint "cannot run code here" | `core/replay.py:27-28`, `449-450` | The loader admits any name in any `freesail.` module, and so whatever those modules import. The reviewer loaded a hand-made checkpoint that called a function of the operating system (`probes/checkpoint-allow-list.py`). A checkpoint is a file beside a save on disk; the browser's own save carries none. So: a save folder sent by a stranger is a program. The one test checks only the direct name. (*Weight: medium. Stands in part per `refute-01`; found independently by three readers.*) |
| "Nothing in the sim imports from the client or the agents" | proposal §8.2 | F4.1. |
| Scripts run "in a restricted environment" (and the code's own comments on a sandbox and a budget) | proposal §4.5; `standing/python_api.py:29, 44` | Neither exists. |
| The evolution catalogue "is data" | proposal §4.4 | §4.4 above. |
| "Ships are data files, not code" | proposal §3.3 | §3.3 above. |
| "A saved log is a saved game" | proposal §3.2 | §3.2 above. |
| The director "cannot move the player's ship" | proposal §7.6; the director's own brief | Decision 14. |
| "Nothing from the game ... is ever passed as a system or operator instruction" | decision 17; the consent brief | Decision 17(a). |
| Of the journal, "nothing in the game acts on what is written there" | the consent brief | A seated director reads it. |
| All stations "exist today but the director" | the consent brief | The director exists. |
| "The `slow` mark is applied here and never in a test file" | `tests/conftest.py:6` | Hand marks in at least six test files (head 3). |
| "A typo fails at import" | `evolutions/registry.py:25-27` | It loads as a string. |
| The chart audit "uses only the game's readers" | `tools/audit_chart.py` | It has its own copy of the tide's blend. |
| The game "is saved" when a station stands down | the harness's line | With no save function bound (a station restored from a checkpoint before a door takes it up) nothing is written (`agents/harness.py:4896`; shown by the second reader). |
| Gate m6c "passed" | `README.md` | Decision 50: run in part. (To be checked against the gate's report.) |
| The specifications are "as built" | each specification | Of twenty-four pointers checked in the first four, three name files that have since been renamed and two describe behaviour that is no longer so; milestone 5's scope statements (two ports, eleven gauges, the western Channel) are false to the code; milestone 6's is "a running diary, stale in at least six places"; milestone 7b's says a thing was dropped that was then built, and gives the director four to eight acts a day where the data gives 48 to 72 (`spec-01` to `spec-05`). |

**One finding that fell,** kept here so that the method can be judged: a reader held that thirst sickens and kills only when the provisions are gone as well as the water, against the code's own docstring. The second reader showed the ration carries a gallon of beer a day inside the provisions, so the water is truly expended only when the beer is; the code is right and the docstring is wrong (`refute-03`).

---

## Head 5, continued: the second sitting (the records and the sealed notes)

Everything above this line under heads 1 to 5 was committed (`b72ed89`) before any record was opened. What follows was written after: the work packages of every milestone, the tuning notes, the gates, the playtests' notes, the design notes with the project's earlier cold review, and the lead's sealed notes, each read by a reader told to set it against the first sitting (`records-01` to `records-06`, `sealed-notes-tried`), with the reviewer reading the heads of the main records and checking the claims he repeats here.

### 5.5 Corrections to the first sitting

The records show the first sitting wrong, or short, in these places. None is rewritten above; each is corrected here.

1. **The fine control of the sails, the gybe and sight across the land** (§11 in 1.3; F2.6) are not oversights. The owner booked them as packages 78a and 78b on 10 November and they are held for this review; **collision** was dropped by him. They remain unbuilt, and the proposal's line for milestone 7 still names the first.
2. **The director making the player's ship strike** (decision 14) is a form put in the director's table on purpose, for a scenario's start, guarded only by a doubt "after the first minute" (`docs/design/Design-Prizes.md:1353-1357`; `agents/director.py:986-993`). The finding stands (the proposal and the director's own brief say he cannot, and no limit refuses it), but it is a design that breaks the rule, not a slip. The director's reach onto every hull was briefed as a feature (`docs/dev/M7-WorkPackages.md:7670`), and no brief asks for the limits to be tested.
3. **The brief sent as the system message** (decision 17(a)) was asked for by the lead's brief of package 42 (`docs/dev/M6-WorkPackages.md:735-736`). **Parity tested only at the captain's station** (pillar 4) was package 44's brief (`:1665`). **The far captain knowing true positions** (decision 40) was package 43's brief (`:1346`). Each is a brief of the lead's set against a rule of the proposal's, and built to the brief.
4. **The browser's map and ship view not following the player's place** (decisions 59, 62) is a ruling, the grey over the readouts package 99's design, held by the owner (`docs/design/Design-PlaceKnowledge.md:413-420`). That the figures still travel to the page stands.
5. **Two of the "eight forms of a ship"** (decisions 52, 53) were chosen in the one-world study.
6. **The ships as the output of code** (§3.3; F2.1) was "the lead's structural decision, agreed" (`docs/dev/M7-WorkPackages.md:9642`). The proposal's sentence was never changed. The generator's drift from the engine's sail law was written down in `docs/design/Build-Ships.md:2248` and left as nobody's job.
7. **The gates** (§11; 5.2). Worse than the first sitting said. By the gates' own reports **no gate of milestone 6 was ever passed**: m6a still reads open, m6a-2 was never cut, m6c is "run in part" (five of thirteen items, three of the five failing what they expected). The last gate passed is m5c, on 8 October, and that "provisionally" on one half with the lead's own watch withdrawn. The README's "gate m6c passed" is false by the gate's first line (checked by the reviewer). The eight items m6c deferred went to a gate that was frozen and never run, and the interim gate does not carry them.
8. **The pace on a cloud runner** (3.7) spreads from 382 to 677 ticks a second by the tuning notes, not 480 to 520.
9. **Determinism** (§3.2) is by the C library, not only by the operating system: nine recorded passages moved when the cloud's image changed. The remedy pinned one workflow's image and left the other floating (`docs/dev/TuningNotes.md:22871-22912`).
10. **The "sheet-tending" fault** the earlier review's ruling left "not now" was in fact mended.
11. **The port's key `leave_on`** (F2.2) is read; see 5.11.
12. **The truths that only call other tests** (3.5; 3.8, item 1). The reviewer's own count, made after a reader of the sealed notes counted fewer: **82** truths call a test of another file, **73** of them with nothing else in the body, and the tests so called are **163** in 27 files. The first reader's 102 and 197 counted more loosely. The finding stands at the smaller figure.

### 5.6 Where the record and the thing differ

Each checked against the tree by a reader; the first, second and eighth by the reviewer.

| The record says | Where | The thing |
|---|---|---|
| "Gate m6c passed" | `README.md:5` | "Verdict: run in part" (`docs/gates/gate-m6c.md:3`). |
| Milestone 7's interim gate is "drafted" | `README.md`; `docs/gates/gate-m7-interim.md` | Drafted on 30 October. Everything it waited on was merged by the 31st. It is still pending, none of its seventeen items run, and no ruling says why. Its draft says the guns are cast loose at quarters; they are not. As written it would have caught almost none of what the reviewer met in play. |
| The director's hand on the followed ship is refused (package 62) | `docs/dev/M7b-WorkPackages.md` | Refused for one spelling. `captain: intent` is dispatched before the check (`world/orders.py:272-273` against `300-303`). |
| "The brief's hard limits stay refusals" | decision 50 | Package 50's own merge record says the limit "nobody dies" has "nothing yet for them to refuse" (`docs/dev/M7b-WorkPackages.md:321-322`, 17 October). It still has nothing. |
| Package 70 "built as briefed": the tack at quarters "slower by exactly the hands it takes" | `docs/dev/M7-WorkPackages.md` | The record's own figures show the tack faster; the truth's assertion was loosened to "at most 1.15 times" to fit. A fault planted there survives (head 3.3). |
| Package 74 closed "with the far fight" | `:4500` | A far warship that goes to engage from a passage drops her leg; the lead bisected it to 74's fourth step (`:10498`); the mend is on a branch not merged; the code is unchanged at this commit. |
| Package 84 (the one world) "green at every merge" | `docs/dev/M7-WorkPackages.md` | Its fifth run failed and the steps were mended after the merge. The design study costed a façade in which each ship hands shared things to the world; what was built is the reverse, a "current hull" switch inside the world, whose faults stayed hidden under green suites for thirteen packages, one test passing only because of the fault (`docs/design/Design-FacadeReaders.md:24-25`). |
| "Never a test skipped, disabled or quarantined" (the head rule of every milestone) | `docs/dev/M7-WorkPackages.md:9-10` | The 74's pace test "was taken out by the lead at the merge" when she measured 505, 476 and 492 against a floor of 500 (`tests/test_bellerophon.py:2188-2196`; `docs/dev/M7-WorkPackages.md:10496`). |
| "No model identifier in any file of the repository" (the same head rule) | `:7` | The record that states the rule names the models' tiers some 120 times, in the same paragraph and through its tables, while the lead sweeps builders' diffs for them. The playtests' folders are named for models. |
| Runs recorded as "green whole" | the merges' records before run 81 | No cloud run before run 81 played the browser's plans: the probe's own brief made it skip where no browser is installed. Run 77 was "green" with a plan broken by a merged step. The lead found and recorded this himself (`:119`). |
| "An expected failure is a debt" | `docs/dev/M7b-WorkPackages.md:858` | Broken by two packages in the same week; eight stand in the first half of the truths alone. |
| The ship the player is aboard carries her own far body (package 60, "proved by 7-481") | `docs/design/Design-ShipBought.md:926-938`, `1125-1129` | Package 60 is not merged and truth 7-481 does not exist. Under `--ship` or `follow` the far body is left behind: nothing at the start, 925 metres after five minutes, two miles after twenty (run by the reader). **A fault the first sitting did not find.** |
| The officer's context budget | `docs/dev/TuningNotes.md:24386`, `24778` | Raised by 500 tokens a package "as the lead's ruled practice"; the fault under it (the officer asked for a handover at his first sample at a local model's size) was flagged on 17 October (`:6273`) and never mended. |
| Decision 68's rules on slavery | the proposal | Kept only because nothing exists that could break them, plus one test on one port's market. Nothing in the code refuses a person as a good: a market takes whatever its file lists. The prize court's head money of £5 a man would break the decision's words if read literally; the owner should say what the sentence means. |

### 5.7 What the project already knew, and what it did not

**Known, written down, and left:**

- The boundary, with three crossings and their line numbers; the duplicated code; the two oversized files; tests that pin rather than prove; the performance. All in the project's earlier cold review of 30 September (`docs/design/ColdReview-2026-09-30.md`). The owner's ruling put each "not now" (decision 29). Six weeks on: the crossings in `core` are nineteen; `scripts.py` has gone from 2,977 lines to 9,095; the frigate from 800 to 1,000 ticks a second to between 480 and 650.
- The "nobody dies" limit refusing nothing (17 October). The enemy-weight limit: mended for one word after a playtest, the hole for any word it cannot rank left.
- The guns left secured: met in a playtest of 5 November, when a director told a model captain "the guns are still secured"; the lead filed it under "What held".
- The starter book refused on the cutter: found on 4 and 5 October ("5 of its 9 standing orders are refused for a cutter") and lost among a review's "small faults".
- The harbour open to anyone who can reach its port; the consent brief's "to come" for the director (flagged four times, deferred to a package not run); the seated player refused readings and `eat` (found, then lost).
- The pace floors inside the machine's noise; the truths that only call other tests; the helper defined twice (the lead's sealed notes).
- Vessels crossing the land (8 of 35 at a sample), the report repeated to the captain below, a kedge that cannot be weighed aground: in the tuning notes among **144 "found on the way", 31 "not mended" and 268 "for the lead"**; five checked in the code are all still there.

**Not known before this review** (no record names it):

- The roads by which the director takes the player's ship (`captain: intent`, `ship "…": intent`), moves his prompt (`follow`), or skips every limit by naming the ship.
- The purchase with the boat lost.
- The server's socket open to any page, with the file commands behind it; the checkpoint that runs code.
- The true position recoverable from the log's data (a package had promised "no reading gives the true position by any road").
- The token lost in a tool call's extra field; another model's words in the operator's turn as a breach of the consent brief's own sentence.
- That player Python is not in the game at all (the close-out of milestone 5 handed "officers writing Python" and the sandbox to milestone 6, which never briefed it).
- The wheel: lost in a hand-off between three packages, each of which thought another had it.
- The far fisherman's haul on the player's hold; the blockade's rendezvous; the player's shot into a ship with no brain.
- The size of what the tests do not prove (head 3).
- **A first game.** Nothing about a newcomer's first game or a tutorial appears anywhere in the milestone's record.

**The owner knew what he wanted.** On 27 October, after playing: "playability and understandability", and additions that "integrate holistically". The work that followed was the one-world refactor, the charts and the hulls.

### 5.8 The lead's method, as the records show it

**How a package runs.** The lead writes a brief; the owner approves it; a builder (a session of its own, on a branch of its own) builds it in steps; the lead reads the diff, runs his own fast tier on a trial merge (forty to seventy-five minutes), merges, runs the whole suite in the cloud, plays the package briefly and writes the record. Since 28 October a builder runs the fast tier once on its final tree and the slow tier of the files it touched. The senior builder is by rule "generously scoped ... trusted with the design, not fenced to a list ... growing a part where the work shows it should".

**What is good in it,** said once: the briefs are careful; sources are demanded for numbers; the lead records his own errors as plainly as others' (every reader of the records said so); a builder's work is never merged unread; the owner is asked, in words he can judge, before scope is added.

**Where it lets things through.**

1. **One reader.** Packages 70 to 101 were merged on the lead's reading alone. The first independent reading of a package was on 10 November. The lead's own note says what happened when there was one: three rounds of independent reading of one package found some twenty faults its green suites had not, and each round's mends brought new ones.
2. **"Green" has meant less each month.** In September, the builder's whole suite. From October, the fast tier and the files touched. By the director's milestone, one suite a wave. Whole only since run 81. A builder's suites are cut short by container restarts; three builders were found asleep for hours.
3. **Pins are moved by the builder who broke them.** The record of a re-pin (173 of them in the tuning notes) gives the old figure, the new and the cause. It never says the change was meant, or that anyone but the builder judged it. At least once it was "taking each figure the run gave".
4. **Faults are found late, by the owner playing.** The owner at the prompt found all of two packages of mends; later builders, chiefly the ships' session, found the rest; days to weeks after merges whose suites passed. No fault found late is traced to the test that should have caught it.
5. **Hand-offs lose things.** The wheel; the findings of gate 6c given to a package whose brief does not hold them; the sandbox; the playtests' "small faults". There is no single list of what is owed.
6. **The briefs, not the proposal, are the working law,** and where they differ the proposal is left standing (5.5, items 2, 3 and 6). The owner approves a brief; he cannot see from it that it sets aside a rule he approved earlier.
7. **Packages grow and split.** Twenty-six lettered packages in milestone 5, thirteen in 6; milestone 7 from about twelve in its specification to about sixty-four, nearly all by the owner's word at the lead's proposal. On 13 November the owner asked for no more to be added.
8. **The review's own launch** was to wait until the work in flight had settled. One package had been reported three times and not merged, and the review was launched.

### 5.9 The cost, as the records show it

- **The suites.** On 1 October the fast tier was 1,866 tests in one to three minutes. On 13 November it was about 7,600 in 54 to 59 minutes. The tiers were measured once and never again. A whole run in the cloud went from about 40 minutes in late October to about 70, at most 116; 91 cloud runs in seventeen days. The two-hour limit on a builder's run was met at least fifteen times. By the lead's sealed notes a builder's three tiers take about four hours.
- **The account's usage** paused one package at 95 per cent of a week's allowance and later stopped every session until the week turned. The order of packages is set in part by which model's allowance is left.
- **The ships.** One ship took 7,401 lines of research, design, generator and tests; another 11,207. The plan for the ships' work estimated "about 60 agents ... most of a day"; its record runs from 25 October to 10 November, sixteen days, and it is not finished (`records-06`). The ships are two-thirds of the design notes by size, a quarter of the tuning notes, and no note weighs any of it against "ships are data files".
- **The records.** `docs/dev/` is 4.9 MB; the tuning notes alone 2.9 MB in 28,704 lines; the design notes 3 MB. Sixty-three per cent of the commits in the visible week touch only documents (by lines, code still leads). Recorded play is 82 MB, an eighth of the repository; its saves carry the owner's user-profile folder name thirty-two times (no address and no key).

### 5.10 The records as records

They are honest and they cannot be used. The tuning notes do their stated work, why a number is what it is, for their first six hundred lines; after that they are a diary in the order things were merged, with no index, in which a mend can stand before its finding and four faults since mended are still written as open. A number can be found by searching for it (ten pins tried: one to four searches each), and what is found is as often a history as a reason: the pace floor's premise lapsed long ago; the tack's band was moved to fit the build. The work packages' table is fifty-one rows whose status cells are dated diaries, out of order, with no word of which rulings still bind. No package's section says its state. The specifications are the same (5.4). **The owner cannot learn the state of his project from its records;** he learns it from the lead, and the lead from memory and search.

### 5.11 The sealed notes

The lead wrote down before the launch what he already believed, and sealed it. Each item was then tried at the commit like any other claim (`sealed-notes-tried`; three by the reviewer). In the brief's three classes:

**Found by the review itself, cold.**

- Truths that only call tests of another file. The lead named it; the review counted it and costed it (3.5).
- The orders, the forms and the readings built in several places (F4.2, F4.3).
- In part: the pace floors inside the machine's noise (3.7; a fault runner met it); the helper `_until` defined twice in the truths' file (`tests-01`); a line said in many places (F4.9); vessels and the land (the guard's warning seen in play; ships seen through the land); browser tests skipped unseen where a package is missing (3.7).

**Missed by the review, and now confirmed.**

- `take the purse` is answered as the reading "the purse" (tried by the reviewer). A refusal says where an unseen thing lies: "the bag of guineas is ashore at Plymouth", asked at Falmouth.
- A rules captain waits for his tide without a word. In the reader's run the cargo was in at 12:21 and she weighed at 17:59: five hours and thirty-eight minutes, seventy lines of log, none saying why she lay there. (With it a correction to the first sitting: the port's key `leave_on` *is* read, by a name built at run time, `world/captains.py:3981`; a first reader's "read by nothing" was wrong, and F2.2's list is shorter by that one.)
- A person in a boat that is lost is left in no hull and not dead.
- The open ocean takes its tide from the Channel's eleven gauges.
- The coarse chart layers stand at mean sea level and the game adds the level above low water again (the mechanism confirmed; the count not re-measured).
- A book of orders cannot name a clock hour, only bells (tried by the reviewer).
- A Spanish signal of one flag reads "two flags at the main".
- Port tracks follow the land and not sounded channels; and ports that cannot be entered are not four but **twenty-four**, by the chart audit's own list.
- The nations' days are from memory: Spain's, all of them.
- **The ways a ship is set up:** six roads to one maker, each with its own checks. A ship put on the land is refused by a world order, accepted from a scenario (two ships of one scenario start on ground that dries) and dropped without a word by the business. The harbour's form offers no intent and no fit.
- **The ways a thing is dated:** nine readers of a dated row. The prize shares' `until` leaves the day out where the others keep it in; `at_war` ignores dates altogether; a war declared with its date as text is, to the prize court, no war (latent: nothing declares one yet). This matters most, because the range of years is the next large work planned.
- **Regions:** three sets of bounds read by four loaders; five weather boxes copy the chart's bounds by hand; one stream area names a region that does not exist.

**Disputed.**

- "The schooner of the recorded merchant passage takes the ground thirteen times as recorded." Both truths that pin her recorded passages assert that she never takes the ground over the whole log. As the tree records it, refuted; the lead should say what he measured.
- That hands are called in several ways: calling all hands is one road. (Sailors are, though, assigned outside the crew's own module in seven others.)
- The saved game that lost its chart: mended before the commit under review, and no fault of this tree.

**Not triable here** (work in flight, the cloud, the process): the far ship woken at anchor; the cutter aground after weighing; one truth that failed once under load; the runs before run 81; the builders' stalls; the suites' hours (the review's own timing is 3.9).

**The two lists side by side.** The lead's list is of particular faults in the game and its data, nearly all true, most of them small, and of the daily frictions of the process. It holds none of the review's structural findings: not the boundary, the director's reach, the server, the checkpoint, the consent brief against the code, the absence of player Python, the catalogue and the ships as code, the tests that cannot fail, nor the newcomer's first hour. The review's list holds few of the lead's particulars. Each saw what its place lets it see: the lead, inside every package, sees the fault in front of him; a cold reader sees the shape. The owner needs both, and has been getting the first.

---

## Head 6. What to do

In the owner's order: a continuation, with what each step buys; the refinements existing systems want before more is laid on them; the integrations of head 4 ranked; the hazards; what to stop.

### 6.1 The continuation, in order

**Step 1. Mend what is unsafe or untrue today.** Days, not weeks; no new feature.

- *The server.* Check where a socket's request comes from and require the page's own token; take the file commands off the socket; do the same for the harbour's route that writes a command. *Buys:* a game a friend can run without any web page he has open being able to read his files.
- *The checkpoint.* An exact list of the classes a checkpoint may hold, no `getattr`, no whole modules; and correct the sentence that says it cannot run code. *Buys:* a save folder that is not a program.
- *The director.* One rule of reach judged on every channel that can touch the player's hull, his person or his prompt; limits that refuse (mark the deadly acts; refuse a weight that cannot be ranked); `follow` not the director's; tests that go in through the director's door. Then either the proposal's sentence or the forms change, and the owner says which. *Buys:* a director whose brief is a guardrail, as §7.6 promised the player.
- *The consent brief against the code.* The owner's own process, and his call: change the code (the situation sent as data, the whole call scanned for the token, the director's reading of journals said) or revise the brief and ask again by his rule. Until then no new station is offered to a model. *Buys:* that what a model agreed to is what is done.
- *The player's road.* The guns' warning; payment after the boat is known to be there; the starter book by rig; the list of 5.3. *Buys:* a first fight and a first port that do not fail in silence.
- *The README and the proposal's status line* made true.

**Step 2. Hold a gate.** The project has not passed one since 8 October. Not the interim gate as drafted: a newcomer's gate. The owner, or better someone who has never played, starts from the harbour page and takes a ship through a passage, a fight and a port, with nothing added first but step 1. Write the player's-road tests (3.8, item 10) before it, from what the reviewer's play and the owner's found. *Buys:* the first true measure in five weeks of whether this is a game, and a list of what to mend that comes from play and not from momentum.

**Step 3. The first hour.** A first game named on the harbour page; the lessons listed as lessons; the gates' and the tests' scenarios out of the player's list; the Sailing Master's first passage, which the proposal put in milestone 8 and which is cheap now because the primer and four lesson scenarios exist. *Buys:* every other system, for a new player.

**Step 4. Make the suite cheaper and truer** (3.8, in its order). *Buys:* hours back on every package, and a green run that means what it says.

**Step 5. Draw the boundary and stop it moving.** First a test that counts today's crossings and fails if there is one more. Then the nineteen in `core`. Then `world` against `agents` and `ui`. *Buys:* that a change in a door cannot break a tick; that the simulation can be tested and timed alone; the performance work the earlier review asked for becomes possible.

**Step 6. The integrations of 6.3,** each a package with its tests written first.

**Step 7. Say what the proposal now is.** A third version, true to the tree: the promises not kept either built or struck (level 3 and its sandbox; "a saved log is a saved game"; "ships are data files"; the catalogue "is data"; the true position "by any road"); the decisions that decide kept, the diary moved to the records. One page of "as built" for each subsystem in place of seven histories. *Buys:* that the owner can hold the work to a document again.

**Only then, new scope,** and in this order: what milestone 7 still owes by its own line (the sails at fine control, sight across the land), its gate, and then the content: ships, charts, the range of years, a career.

### 6.2 What existing systems want before more is laid on them

| System | Before more is added | Why |
|---|---|---|
| Ports (121) | Hull repair and lower masts at a yard; a crew pool that refills; demand in the market; war counted once | More ports multiply a thin thing. |
| The data files | A schema that refuses a key it does not know, for ports, captains' doctrines and evolutions | 121 ports, 11 doctrines and 108 evolutions in which a typo is silent; twelve doctrine keys and a whole block already inert. |
| The chart | Tiles out of plain git (a large-file store or a release's asset); a world that loads the regions it is in | A gigabyte to clone; six to eleven seconds to begin a game. |
| The far world | A ship with no brain that can be hit; the far fisherman's haul on her own hold; the land not crossed; the player's ship keeping her far body | The world the player mostly meets. |
| The fight | The player's road; the wheel; boarders who leave their guns; `repel boarders` that ends | Head 1.5. |
| The crew | The fatigue of work aloft charged in play; skill aloft read or struck | §3.5's promise. |
| The director | Step 1 | |
| The ships | The generator's sail law taken from the engine; then no new hull until step 3 is done | The largest block of work in the project serves its least urgent need. |
| The records | 6.5 | |

### 6.3 The integrations of head 4, ranked

By what joining buys against what it risks.

1. **One table of the world-order forms** (F4.3) that carries, for each form, its grammar, its reach and its harm, read by the channel, the director and the doubt alike. *Buys* the director's guardrails by construction; removes four copies of the channel list. *Risk* low: the forms are few and listed.
2. **One router for a typed line** (F4.2), used by the prompt, the models' tool and a sleeping hull. *Buys* parity by construction; a new verb in one place. *Risk* medium: the three orders of trying differ today and tests pin each.
3. **One function that trades** (F4.4). Small; mends the purchase fault once.
4. **One core for the doors** (F4.5): the turn made into messages, the reply parsed, the token scanned, the budget kept. *Buys* the consent brief's promises in one place. *Risk* medium: three vendors' shapes.
5. **One perception and one table of roles for a captain,** far or crewed (F4.8). *Buys* a ship that behaves alike inside and outside four miles.
6. **The boundary** (F4.1; step 5).
7. **One speller of numbers, distances and times** (F4.9). Small.
8. **The picture:** serve the rig's skeleton from Python as the hull's stations are, or test that the two agree (F4.6). *Risk* medium: 1,600 lines of JavaScript.
9. **The fight's sums shared across the levels of detail** (F4.7).
10. **One driver under the console and the server** (F4.10).

The lead's own list under this head (5.11) adds four more, of which the ways a thing is dated matters most before the range of years is built.

### 6.4 Hazards to avoid

**In the code.** The import inside a function as a habit (1,767 of them): each is a crossing nobody decided. The bare catch. A new level of detail that copies a sum. `freesail/world/` as the place every new thing goes. Tests that import other tests. History in comments.

**In the data.** Files that look like data and are the output of programs, with tests that forbid a hand's edit. Keys nothing reads. One year's picture written as if dated. No schema. Binary tiles in git.

**In the repository.** A gigabyte clone that grows with every chart block. Checks that run nothing on a document the game serves. A checkout one commit deep that makes tests skip. Recorded play with a user's folder name in it. No licence file though one is declared. An install that works only in the editable form.

**In the process.** A milestone "frozen open". A gate that lags until it lapses. A brief that sets aside a rule of the proposal without saying so. One reader for both the code and the record of it. A builder "trusted with the design" on a package with no gate behind it. Pins moved by whoever moved them. Findings handed between packages with no list. A review launched before its condition was met.

**In the cost.** A suite that grows by a thousand cases a week with nobody measuring it. Suites restarted by every merge. Packages ordered by which model's allowance is left. Records that cost more to write than anyone can afford to read.

### 6.5 What to stop doing

1. **Stop adding content** (ports, chart blocks, hulls, signal books, nations' tables, eras) until a gate is passed and a newcomer can begin.
2. **Stop freezing milestones open.** A milestone closes at a gate or is cut down until it can.
3. **Stop writing history into the code and the data.** What a line does goes beside it; why it changed goes in the commit. The 7,600 package numbers can stay where they are; add no more.
4. **Stop pinning what the code gives** without a reason a reader can check, and stop the builder who moved a pin being the one who passes it.
5. **Stop calling tests from tests,** and stop hand-keeping the tiers.
6. **Stop using the specifications and the proposal as running records.** A decision decides; a diary goes in `docs/dev/`.
7. **Stop merging on one reading.** An independent reading before the merge of anything a player or a model will meet. The lead's own experience of one package says what it finds.
8. **Stop adding to scope by decision without taking something off.** Decisions 54, 56, 58, 67 and 69 each added a field of work; none removed one.

### 6.6 How this sits with the reviews that follow

The brief proposes that packages 103, 96 and 92 follow this review, each amended by what it finds. The reviewer's advice, for the owner to settle:

- **96 (a ship's configuration, and the harbour presenting it)** first, and amended: the harbour's first duty is the newcomer's first game (step 3), before it presents every configuration the game has.
- **103 (the years 1792 to 1825)** after the gate, and amended: the schema for the data files and one reader of a dated row come first (6.2; 5.11), or thirty-three years of rows will be written into files where a typo is silent.
- **92 (a career)** last, and not begun until steps 1 to 5 are done: it lays a new layer on the ports, the far world and the director, the three systems this review found least held to their rules.

---

## The evidence

All under `docs/reviews/ColdReview-M7-evidence/`. A reader's file is kept as the reader wrote it, with only models' and vendors' names taken out; where a second reader or a fault runner overturned a claim, the overturning is in the later file and this report follows the later file.

| File | What it is |
|---|---|
| `READERS.md`, `TESTREADERS.md`, `CODEREADERS.md`, `SPECREADERS.md`, `REFUTERS.md`, `FAULTRUNNERS.md`, `RECORDREADERS.md` | The standing instructions each kind of reader worked under: the review's method, so that it can be checked. |
| `play/` | The reviewer's own play: five console transcripts and three screenshots of the browser. |
| `tests-01` to `tests-12` | The test suite's audit: every test file read whole, a table by file, verdicts under (a) to (c), and the faults each reader nominated. |
| `tests-by-file.md` | The one table by test file: lines, tests and cases, the seconds of the timed run, the reader's verdict. |
| `faults-1` to `faults-4` | The nominated faults planted: each with its diff, the run, and SURVIVED or KILLED. |
| `faults-5-control.md` | The control: eighteen ordinary faults of the reviewer's choosing, all caught. |
| `code-01` to `code-10`, `code-05b` | The code and the data read by subject. |
| `spec-01` to `spec-05` | The technical specifications set against the code, commitment by commitment. |
| `refute-01` to `refute-08` | The second readers: each finding of weight tried by a reader told to refute it. |
| `probes/` | Short scripts that reproduce seven findings (the checkpoint, the director twice, the guns, the blockade, the far fisherman, a port file's misspelt key). Run from the repository's root. |
| `records-01` to `records-06` | The second sitting: the project's records set against the first sitting. |
| `sealed-notes-tried.md` | Each item of the lead's sealed notes tried at the commit. |
| `timings/` | The timed run of the fast tier: each test's seconds as it finished. |
