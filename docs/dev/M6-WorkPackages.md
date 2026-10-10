# Milestone 6 work packages

The packages of `docs/TechnicalSpec-M6.md` (§28), briefed in turn for the owner's approval
and launched on his word. The head rules of `M5-WorkPackages.md` hold: the heavy design to
Fable and the standard work to Opus; a scenario's book tuned once and cheaply; the budget
the owner's; nothing under `docs/agents/consent/` or in `docs/agents/ConsentBrief.md`
touched but by the package the specification names for it (42); no model identifier in
any file of the repository; the recorded passages' constants re-pinned only where a change
moves them, with the old figure beside the new and the reason in the tuning notes, and a
passage that moves for a reason the package cannot give a finding, not a pin; the fast
tier run before the report and the slow tests of the passages touched; a section in the
tuning notes and a report to the lead at the end.

## Waves

| Package | Builder | What | State |
|---|---|---|---|
| 38 | Fable | The chart stitched: many regions over the corridor, the queries across edges, the climatology's boxes, the tide's gauges, the recipe form for the blocks | launched 2026-10-09 |
| 39a to 39f | Opus | The six blocks of the voyage to Madeira and the Strait (39c to 39f briefed 2026-10-10; decision 44) | 39a (channel-mid) merged 2026-10-09, bounds 48.5 N to 51 N and 3 W to 1 W, Morlaix's patch left; 39b (biscay-north) merged 2026-10-10; 39c (biscay-south), 39d (portugal), 39e (madeira and azores, the corridor widened) and 39f (strait) launched together 2026-10-10 after gate 6a's cut, in four worktrees |
| 40 | Fable | The ship's company and the rules-based captain in three layers; the captain's station; the player's seat | merged 2026-10-09 (the officer's reckoning moved to 40b; the consent brief's revision drafted for the owner, `docs/playtests/drafts/consent-brief-m6-draft.md`, held for 42) |
| 40b | Opus | The lessons in the primer; the officer's own reckoning (spec M6 §5, truth 80; moved from 40 at the owner's word) | merged 2026-10-09 (an own reckoning carried on past noon, the lead's ruling; chapter 13 stays out of the primer test) |
| 40c | the lead | The captain's trials: the gate's pinned scenarios of the rules-based captain under weather scripts and world orders; the player's hand on an intent scenario (the captain stands aside until `captain: carry on`) | merged 2026-10-10; gate 6a opened (`docs/gates/gate-m6a.md`); the fast tier on the merged tree 3093 passed, none failed |
| 42a | Opus | The consent brief revised once from 40's draft, describing in kind all of 6b and 6c that the rule watches; the watched sections pinned; the re-asks the owner's | merged 2026-10-10 (decision 42: the added sentences approved; the re-asks the owner's) |
| 41 | Fable | The wardroom: several doors, the pace rule, the deck's conversation, the master's and the lookout's stations, the stand-by on several conditions | merged 2026-10-10 (stations bound at run time, a passenger station, the pace rule as one object the drivers share; no pin moved) |
| 42 | Opus | The API door and its security pass; the transcript-driven replay; the chart and the ship's view as images through the doors that carry one (the consent revision moved to 42a) | merged 2026-10-10 (the key from the credential store first; the acts beside the log; the pictures from the open page; OpenRouter on a mock only; thinking cannot be switched off on the current models, so no-effort is the model's default) |
| 43 | Fable | The crewed promotion, a model captain of another ship, the far-detail guard, the director's seat hook | brief to write |
| 37p | Opus | The yards and the helm by the wind, and the ship in a gale: three levels of bracing, the helm's mark the highest sail set, storm canvas, the recovery from aback; every passage re-pinned once | merged 2026-10-10, with 41 and 42 merged in its worktree; gate 6a cut after it |
| 43b | Opus | The lugger and the smack; the world's business | brief to write |
| 44 | Opus | The regatta harness and the parity tests | brief to write |

Package 37m (the helm through the wind) is milestone 5's last, briefed in
`M5-WorkPackages.md`, launched beside 38 on 2026-10-09 and merged after it: 38 moves no
recorded passage, 37m moves several.

## Package 38: the chart stitched (`freesail/world/chart.py` for the chart as the whole manifest, the finest tile under a point across every region and the fall back to the corridor and the world, the features of every region indexed together; `freesail/world/geo.py` if a function needs the sphere beyond one region; `freesail/world/scenarios.py` and `freesail/core/world.py` for `chart:` beside `region:`; `freesail/world/lookout.py`, `ground.py`, `reckoning.py`, `orders/navigation.py`, `api/queries.py` only where a caller assumed one region; `freesail/world/tide.py` and `data/tides/*.yaml` for gauges and streams over a larger table; `freesail/world/weather.py`, `weather_script.py` and `data/weather/climatology.yaml` for the boxes; `tools/build_charts.py` for the corridor, the recipe form and the blocks' checks; `data/charts/` for the corridor's tiles and the manifest; `docs/TechnicalSpec-M6.md` §26 as built; `docs/design/ChartData.md` a note; `docs/references/Charts.md`; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_geo.py`, `test_lookout.py`, `test_tide.py`, `test_weather.py`, `test_scenarios.py`, `tests/test_known_truths.py` only to prove nothing moved)

Spec M6 §26 whole, with the study `docs/design/ChartData.md` §5 and §6 (the levels, the
files, the disk, the build, the queries per tick) and spec M5 §9 to §12 and §16 for what
the chart, the lookout and the tide are today; the owner's chart goal of 2026-10-09
(decision 39, ruling 4 and 5: the Strait as a sixth block, the regions committed whatever
their size). On Fable, since the runtime's one-region assumption runs through the world's
code and the weather's seeding must not move a recorded passage. Launched 2026-10-09
beside 37m; merged first.

What to build:

1. **The chart is the whole manifest.** `load_chart` takes a chart name (`atlantic-east`,
   the manifest's new top-level `charts:` naming the regions it holds and the corridor
   under them) or, as now, a region's name, which is a chart of that one region (every
   scenario and test today keeps working unchanged). A query asks the finest level that has
   a tile under the point across every region of the chart, falls back to the corridor at
   level 1 and the world at level 0 where either is built, and answers None beyond them as
   now. The features of every region are loaded and indexed together, their names unique
   across regions (a clash is an error at load, said in words). `Chart.contains` and
   `bounds_words` speak of the whole. The queries' names and signatures do not change:
   37m's branch, built beside this one, calls them.
2. **No seam.** The lookout, the dangers on a shaped course, the nearest land, the
   grounding, the depth under the keel and the anchor's ground work across a region's edge
   and over the corridor without a seam: a test sails a fake across an edge and over the
   corridor's water and finds no step in the depth, no danger lost and no landfall said
   twice. Where the corridor's 30" cells are the finest, the lookout's words are honest
   about it ("the land" at a headland's scale, no rock by name), by the level's `use`.
3. **The corridor.** Level 1 from GEBCO over 32°N to 51°N and 20°W to 1°W, built by the
   tool (`--corridor`, a region-like recipe with the fetch bounds and the datum, mean sea
   level as the level has it) and **committed** (about 2,300 by 2,300 cells, some 11 MB
   raw; the owner's ruling 5), with the manifest's record of the source, the licence and
   the checksum as for every tile; `.gitignore`'s rule for `tiles/1/` gives way for the
   corridor's tiles alone (name them or move them), the Atlantic beyond it still fetched
   and not committed. The fingerprint of the rules takes the new files as it takes the
   rest.
4. **The weather's boxes.** `data/weather/climatology.yaml` gains boxes: the Channel's as
   it is, unchanged in every figure and in its name, and three more, PROVISIONAL from the
   same kinds of source and marked so (Biscay; the Portuguese coast with the summer
   northerlies, the Portuguese trades; the sea off Madeira with the north-east trade), with
   the sources named or "judgement" per row as the Channel's rows are; a scenario's weather
   is seeded from the box she starts in, and the systems in play blend at a box's edge by
   the study's rule (W §5) or a stated simple one. **Nothing in the Channel moves**: the
   recorded passages and the gate's day replay to their digests, which is the package's
   first test and the merge's condition.
5. **The tide's table over a larger sea.** `constituents.yaml` and `establishments.yaml`
   take gauges and places beyond the Channel as the blocks will add them, the interpolation
   between gauges honest about distance (a position far from every gauge gets the nearest
   with its doubt said in the master's words, not a blend across a coast), and `streams.yaml`
   takes areas by chart; the eleven gauges and their figures unchanged.
6. **The recipe form and the blocks' checks.** `REGIONS` in `tools/build_charts.py` as the
   form each block fills (bounds, fetch, harbours, the sources' names), a `--region` build
   that leaves every other region's tiles untouched, and the checks a block must pass,
   printed by the tool: the allowed-licence test, the shore swept for GEBCO's fill (M5 §33
   item 16), features within the region's bounds and unique across the manifest, every
   feature's source in the references' form, the harbour patches' datum stated. A short
   `docs/dev/ChartBlocks.md` says how a block is built, for the six Opus packages to follow
   (39a to 39f), with the Channel east block's bounds and sources as the worked example.
7. **The ships' plans and the pilots' stations** need nothing new; say so after checking,
   or say what did.

Tests for each; the whole suite's passages unchanged to the digest. Where the corridor's
build cannot be fetched from this machine, say so and leave the recipe and its tests on
a small synthetic corridor, the fetch for the lead or the owner to run; do not commit a
corridor that was not built from the source named in the manifest.

## Package 40: the ship's company, the rules-based captain in three layers, the captain's station (`freesail/world/people.py` and `data/people/<ship>.yaml` new for the wardroom as people with stations; `tools/gen_ships.py` for the complement's officers drawn into the ship file; `freesail/world/captains.py` new for intent, plan and behaviour; `data/captains/<role>.yaml` new for the doctrine; `freesail/standing/runtime.py` for a book loaded and unloaded by a state; `freesail/world/scenarios.py` for `intent:` beside `standing_orders:`; `freesail/world/ships.py` for the state machine's far-detail body as an interface (filled by 43); `freesail/orders/navigation.py` only for the planner's use of `shape a course for` and the beating rule; `freesail/orders/stations.py`, `freesail/agents/agent.py`, `tools.py`, `harness.py`, `remote.py`, `mcp_server.py`, `local.py`, `repl.py` for the captain's station and the player's seat; `freesail/agents/fake.py` for the fake captain; `freesail/api/readings.py` for `the captain` and `the people`; `freesail/ui/console.py` and `ui/server.py` for the player's seat; `docs/agents/Harness.md` a section, `docs/agents/README.md` where the stations are listed; `docs/primer/16-the-officer-of-the-watch.md` and a new `17-the-captain.md`; `docs/TechnicalSpec-M6.md` §2 to §8 as built; `docs/dev/TuningNotes.md`; `tests/test_people.py`, `test_captains.py` new, `test_standing.py`, `test_scenarios.py`, `test_officer.py`, `test_captain.py` new, `test_agents.py`, `test_known_truths.py` truths 77 to 79 and 81 and the passages re-measured only where the people's lines move them)

**Approved by the owner, 2026-10-09**, to run when the lead deems it the moment (after
37m lands), with this added in his words: the builder is to work this one like a senior
engineer and not be afraid to go beyond the letter of the brief where that fits the intent
and it feels it can do so, since it is a considerably important design package. Where the
builder goes beyond the letter, the report says where and why. Spec M6 §1 to §9 whole, with
decisions 39 and 40; the proposal's §3.5 (station holders and their outlines), §7.1 (the
roles as authority levels) and §7.4; M4 §11 (the harness's contract) and M5 §22 (people
as data and a line) and §29 (the officer's station as it stands); the review's G19 (the
officer's own reckoning, the wardroom); Luce 1884 and the Regulations of 1808 on the
duties of the captain, the lieutenants and the master
(`docs/references/admiralty/`, `docs/references/luce/`). On Fable: the three layers are
design, and the captain's station is the first with the player's whole surface. Built on
38 and 37m as they land; launched on the owner's word.

What to build:

1. **The ship's company as people.** Each of the four ships (and the two to come, 43b)
   gains its wardroom in `data/people/<ship>.yaml`: the captain (the master in trade),
   the lieutenants (three on the frigate, one on the brig-sloop), the master and his mates,
   the boatswain, the gunner, the carpenter, the purser and the surgeon on the frigate; the
   mate on the small vessels. Each a person as M5 §22 has it, with a rank, a station, a
   place aboard, a state (on deck, below, asleep, at a task, sick), a skill as M3 has it,
   and a short outline (a few traits, a line of history, a station brief) as data; the
   names drawn from the period's lists under the seed, a scenario free to name any. The
   generator draws the complement's officers into the ship file so that the muster and the
   people agree. The harness's stations bind to a person by data (`station: first
   lieutenant`), the officer of the watch to the first lieutenant or the mate as now, and
   the binding is read, never a name in code. `the people` lists them with places and
   states; `send for`, `pass the word for`, `go below`, `come on deck` move them as M5's
   orders do; a person at a task is occupied until it ends. The crew of M3 stay counts.
2. **The rules-based captain in three layers** (`captains.py`; spec M6 §4; decision 40).
   - *Intent*: the goal and its parameters, read from the scenario (`intent: trade tin from
     Falmouth to Brest`, `intent: keep the station off Ushant between ... and ...`,
     `intent: carry this letter to ...`, `intent: run home to ...`) or from a world order
     (`npc <id>: goal ...`, which M5 §26 has), with the port's and the nation's part.
   - *The plan*: legs derived at sea from the intent over the chart: the port's pilot
     station, the common tracks the features file names, the headlands cleared with an
     offing, the dangers on a shaped course; each leg shaped with `shape a course for`; a
     course the wind will not allow beaten by a rule (stand on the tack that makes the most
     good, go about when the other tack makes better or when the offing closes, as a
     standing order the captain writes for the leg); the plan worked again on an event (the
     wind shifted past a point, a danger ahead, the glass falling, a stranger). Written as
     orders and standing orders the captain gives, so the log reads as a captain's.
   - *Behaviour*: a state machine whose states are books in the dialect, loaded on entering
     and unloaded on leaving (the runtime gains a book's name and a load and unload by
     name): on passage, beating, hove to for weather, running for shelter, at anchor, in
     port, investigating a stranger, chasing, evading, keeping station, in distress, and
     engaging, present and empty until M7. A transition is an event the ship perceives
     (the lookout's, the glass's, the depth's, a signal's), judged by the doctrine.
   - *Doctrine as data*: `data/captains/<role>.yaml` for the King's ship on station, the
     merchant, the packet, the convoy's commodore (the fisherman is 43b's): the stimulus
     against the role giving the transition and its thresholds, with the source or
     "judgement" beside each figure, in the form the port files use.
   - *Perception on the player's terms*: a captain sees through the lookout and reads the
     glass and the sky as readings; nothing in `captains.py` reads the world's truth, and a
     test proves it as 37j's does for the readings.
   - *The rule of the road as 1805 had it*, at near detail: the ship close-hauled on the
     starboard tack stands on, the larboard-tack ship gives way, a ship running keeps
     clear of one by the wind; a reflex at a few cables, said in the log.
   - *The far-detail body as an interface*: the state machine's states resolve into a
     far-detail plan (hove to is no way; beating the made-good speed; investigating a plan
     toward the stranger); 40 writes the interface and resolves two states (on passage,
     hove to) on the far-detail vessels of the recorded passages without moving a pin; 43
     fills the rest with the crewed promotion.
   - *The floor*: the captain holds the player's ship when the player and every model are
     absent and the scenario gives an intent instead of a book; a scenario with a book is
     sailed by its book as now, so the recorded passages do not move. A new test scenario
     with an intent and no book, the schooner trading tin Falmouth to Brest, comes through
     to the sale under the captain alone, and is pinned (truth 77 as amended below).
3. **The captain's station** (spec M6 §3): the third station, with the player's whole
   surface (every reading, every order at every level, the standing orders as his book,
   the port's business, the people, the papers, the deck to give and take); its brief says
   the voyage, the ship, the people, the book he inherits, and the contract as the
   officer's (the token, the three ways of leaving, the journal, the turn's budget, the
   conflict-rule detector over his own orders, the stand-by naming an event or a bell
   while his book holds the deck); his door silent past the station's patience, the deck
   passes to his book and the rules-based captain's judgements stand in, said in the log,
   as the officer's does. `--station captain` at every door; the fake captain in `fake.py`
   proving each commitment of `docs/agents/README.md` at this station. **The owner's place
   and the player's seat** (decision 39, ruling 1): the owner is always at the door with
   the stop, the grants, the save and the clock, and his words reach a station as the
   owner's; the console and the browser can seat the player at a named station below the
   captain's with that station's authority (the authority filter the officer's station
   has, applied to the player's orders; the primer his brief), so that he may hold a lesser
   role under a model captain; the captain's station gives `you may` to the officer's as
   the player does now.
4. **The officer's own reckoning** is 40b's (the owner, 2026-10-09, to lessen 40's
   load): spec M6 §5 and truth 80 go with it.
5. **Orders and readings**: `the captain` (who holds the station, the book's name, the
   deck); `the people` extended; `stand down the captain`; `you may` from the captain's
   station; the captain's station brief head (M4 §11) saying the voyage.
6. **The consent brief's revision, drafted and held.** The captain's station is a kind of
   thing the brief does not describe (decision 37): the package drafts the revised brief
   as `docs/playtests/drafts/consent-brief-m6-draft.md` with the sections that change
   marked, and the station briefs that go with it, for the owner's approval; it does not
   change `docs/agents/ConsentBrief.md`, which 42 revises once with 41's changes, and no
   model is seated at the captain's station before the re-asks.
7. **Truths** (spec M6 §8, numbered on from 76): 77 the merchant passage and the naval
   cruise under their books with no model seated replay to their digests; 78 a fake
   captain commands the merchant passage by its book and six direct orders, the log the
   same with his six orders under his mark; 79 a silent captain's door passes the deck to
   his book within the station's patience and the book brings her to the anchor; 80 is
   40b's with the officer's reckoning; 81 no reading at the captain's station gives the
   truth by any road; and the new scenario of item 2, the schooner trading on an intent alone,
   pinned.

What 40 does not do: the crewed promotion and a model captain of another ship (43); the
fisherman's doctrine, the lugger and the smack (43b); the master's and the lookout's
stations, the deck's conversation, the pace rule (41); the API door and the brief revised
in the repository (42); the lessons and the officer's own reckoning (40b); engaging (M7). Tests for each item on the fake
world and the fake doors; the passages re-measured only where the people's lines move
them, with the reasons.


### Package 40, as merged (2026-10-09): what the lead found and the owner's decisions

Merged `--no-ff` at `49d09b7` after the K batch, 37m and 38. No pin of the recorded
passages moved; the schooner on an intent alone (`data/scenarios/merchant-intent.yaml`,
36 hours, Falmouth to Brest and the tin sold by rules alone) and the merchant passage
under the fake captain are pinned as truths 77 to 79 and 81 (`tests/test_known_truths.py`,
the two new day fixtures in the slow tier). The officer's own reckoning is 40b's. The
package's findings are in the tuning notes; the lead's probe of the station's bounds: a
world order from the captain's station is refused by the grammar as it is to the player,
`resume the captain` from the station is refused, and `stand down the captain` from the
station itself is accepted (the station released, the rules holding her), which is a
model leaving by another road than the token and is left as it is.

For the owner:

1. **The consent brief's revision**, drafted as
   `docs/playtests/drafts/consent-brief-m6-draft.md` with the changed sections marked and
   their reasons: approve as drafted, or fold the two one-clause changes (*Leaving*, *The
   journal*) into their neighbours so the re-ask names three sections rather than five.
   The lead's recommendation: approve as drafted; the re-ask names what changed and a
   clause is a change. Package 42 puts it in the repository and the owner runs the
   re-asks through the game's own consent step. No model is seated at the captain's
   station before then.
2. **A standing order may not tell or ask the captain's station** (kept refused, as the
   book speaks for the captain). The lead's recommendation: keep.
3. **The log's heave and the bearings' errors draw one stream**, so a captain's `heave
   the log` moves the next bearing's words (a finding, unchanged). The lead's
   recommendation: leave it; it is true of any order that draws, and splitting the
   streams would move every pin for no gain in play.

## Package 40b: the lessons in the primer, and the officer's own reckoning (`docs/primer/18-lessons.md` new, the README's row and chapters 10 and 16 where the forms tables and the pointers go; `freesail/orders/navigation.py` and `freesail/world/reckoning.py` for the officer's reckoning; `freesail/agents/agent.py` for the captain's and the officer's briefs pointing at the chapter; `freesail/agents/tools.py` only if the station needs a word the order language does not give; `docs/TechnicalSpec-M6.md` §5 and §6 as built; `docs/dev/TuningNotes.md`; `tests/test_primer.py` as it stands, `tests/test_reckoning.py`, `tests/test_officer.py`, `tests/test_known_truths.py` truth 80)

Opus. Two things, a writing package and a small step in the reckoning, from spec M6 §5
and §6 and the review's G19 (`docs/playtests/2026-10-05-gate-5c-review/report-2.md`,
§G19, which the package reads first, with the officer's own words of game 9 that it
quotes). Package 40 built the captain's station and the player's seat beside it; this
package writes for both.

1. **The lessons** (§6), a new primer chapter `docs/primer/18-lessons.md` (17 is the
   captain's since package 40; the spec's `17-lessons.md` becomes 18, said in §6 as
   built), the README's chapters table and its "where to start" line. Worked passages,
   each a duty an officer must be able to do alone: a landfall on one headland; a pilotage
   by cross bearings; heaving to for a pilot; coming to in a tideway; a night standing off
   a lee shore; and, from what neither the officer nor the owner knew the ship could do, the
   allowance for a set (`allow ... knots of set`), the amplitude (`observe an amplitude`),
   what `let go` veers by itself, what `veer to` and `weigh` act on, and when a bearing's
   distance is laid down. Each lesson gives the period's rule with its source in the
   references' form (`docs/references/README.md`; Luce, Norie, Moore, Falconer, Bowditch
   and the pilots the primer already cites), the orders in the game's language as a fenced
   block that `tests/test_primer.py` checks as it checks every chapter's (the presets and
   the instant runner are there to be used; a lesson's orders are played, not imagined),
   what the log says when it goes right, quoted from a run of the lesson on the game at a
   named seed and scenario (the quotation measured once, and the seed said), and the usual
   mistake with what the log says then. The officer's two conditions of game 9 ("a few
   more landfalls on my own reckoning", "taken her in and out of a road or two without
   your hand on the con") are written down at the chapter's end as the path to a command,
   in those words. The primer is the same book for the player and the model (parity): the
   chapter reads to both, and says so once. `CAPTAIN_BRIEF` and `OFFICER_BRIEF` in
   `freesail/agents/agent.py` gain one sentence each pointing at the chapter (the
   station briefs are not part of the consent question, and the consent files are not
   touched). The forms tables of chapters 10 and 16 gain the new orders of item 2.
2. **The officer's own reckoning** (§5; truth 80). An officer may keep a reckoning of his
   own from the same log board, tide table and sights, as lieutenants and the young
   gentlemen did. Two orders in the order language, so that the player at the officer's
   station (package 40's seat) and a model at it have them by the same words: `work my
   reckoning` gives the master's slate since the last fix (the courses steered and the
   distances by the log, the set allowed, the sights taken, the last fix and its doubt), as
   a reading in the station's reply and not a line the whole log keeps; `my reckoning is
   <position>` (a position in the form `set the reckoning to` takes) gives his own back,
   kept beside the master's and moving nothing: it is a figure of the station's, carried
   in the save, and at noon the log's reckoning line is followed by one line saying the
   officer's position and its distance and bearing from the master's, only when an
   officer's reckoning is held (so no recorded passage's digest moves: none has an
   officer). The captain adopts it, if he will, with `set the reckoning to ...`, which he
   has; the captain's station has both orders too, since it has the player's whole surface,
   and a standing order may not give either. Truth 80, in `tests/test_known_truths.py`:
   an officer's reckoning worked from the slate by the slate's own figures agrees with the
   master's within the master's doubt when both are right, and the log shows both at
   noon; a test in `tests/test_officer.py` that the fake officer and the player's seat can
   give both orders and are refused a position that is not one. The master's station a
   model could hold (6b's wardroom) takes the same slate; say in §5 as built what the
   slate is, as data, so that 41 reads it.
3. **The spec and the notes**: §5 and §6 as built; the tuning notes' section with the
   lessons' seeds and runs, what was found, and the suite as run.

Not this package's: the gate (the lead cuts 6a after this package); a model reading the
lessons (the gate's); the master's station (41). Tuned once and cheaply: a lesson's run is
made once at its seed and quoted, not iterated to a prettier log. The fast tier before
the report and the officer's and the reckoning's test files; the recorded passages do not
move, and the package says it checked (`tests/test_known_truths.py --slow -k "gate_5b or
gate_5c"` once, or the lead runs it at the merge).

## Package 39a: the Channel east block (`channel-mid`; `tools/build_charts.py` `REGIONS` and `CHARTS`; `data/charts/` the region's tiles, coast, index and manifest entry, `features/channel-mid.yaml`, `overrides/channel-mid/`; `data/ports/*.yaml` new per port; `data/nations.yaml` if a nation is new; `data/tides/constituents.yaml`, `streams.yaml`, `establishments.yaml`; `data/scenarios/channel-east.yaml` new; `docs/references/Charts.md`, `docs/dev/ChartBlocks.md` where the how-to proves wrong; `docs/TechnicalSpec-M6.md` §26 as built; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_ports.py`, `test_tide.py`, `test_scenarios.py`)

Opus. The first of the six blocks of spec M6 §26, built as `docs/dev/ChartBlocks.md` says
(read it whole first, and the recipe form over `REGIONS` in `tools/build_charts.py`, and
package 38's section of the tuning notes for what it found). Package 38 made the chart the
whole manifest; this block adds a region beside `channel-west` and touches nothing of it.

1. **The region** `channel-mid`: Dartmouth and Torbay, Portland and Weymouth; Guernsey and
   St Peter Port, Jersey and St Aubin's, Alderney and the Race; St Malo. Bounds 49°N to
   51°N and **3°W to 1°W, abutting `channel-west` at 3°W exactly** (its east bound), the
   fetch box widened as the form says. Morlaix (3.83°W) lies in `channel-west`'s bounds:
   it gets its port file and its marks in `features/channel-west.yaml` (the features file
   is data and no tile), and no harbour patch in this package; say so as a left item (a
   patch at Morlaix is a rebuild of `channel-west`'s harbours, for a later package).
2. **The seam.** The level-2 tiles are on one grid for every region, and `channel-west`'s
   easternmost column reaches past 3°W; a tile `channel-west` lists in the manifest is
   `channel-west`'s: the build does not write it again and does not list it under
   `channel-mid` (a rule to add to the tool, small and in the build's own code, printed
   as a check: `tiles another region lists: n kept`). After the build `git status` shows
   no change under `data/charts/tiles/` or `coast/` for any tile or file `channel-west`
   listed before, and the report says so. The datum finding of 38 (EMODnet's LAT against
   the corridor's mean sea level at a region's edge): fetch the region whole, as 38 says.
3. **The period data** for the harbour patches and the marks: Mackenzie's Hurd sheets for
   the English side, Bellin's Petit Atlas for the French and the islands, Faden 1793 and
   the Channel pilots for the directions; the lights of 1805 dated (the Casquets, Portland,
   and any other the directions give), so that 1805 sees what 1805 had. Where a sheet
   cannot be fetched or read from this machine the patch is left and the port file says
   `datum: unverified` as 35b did; never a figure invented.
4. **The nations**: the islands British; St Malo and Morlaix hostile to a King's ship, open
   to a neutral. **The tide**: TICON's gauges of the block read as package 34 read the
   file (St Helier, St Peter Port, Weymouth or Portland, Dartmouth, St Malo: which it has
   is unverified until read); the Race of Alderney, the Swinge, the Little Russel and the
   stream between the islands and the Cotentin as stream areas by the directions, the
   Portland Race as an area; the master's epitome places. The eleven gauges and their
   figures do not move. **The weather**: the Channel's box covers it; nothing.
5. **A scenario** `channel-east.yaml`: a free passage of the block's stretch (the frigate
   from Torbay to St Peter Port through the Race, or the schooner Weymouth to St Malo:
   the package's choice), `chart: atlantic-east`, sailed once at seed 7 to the anchor by a
   short book, its figures in the notes; not a gate's, not pinned.
6. **The build**: `python tools/build_charts.py --region channel-mid` through the proxy,
   the checks printed and passing, the tiles committed (about 18 MB), the manifest with
   every other entry carried over. The lead merges this block's manifest entry with 39b's
   by hand: keep the region's entry self-contained and say in the report the exact lines
   added to `charts.atlantic-east.regions` and to `sources`.
7. **The notes and the spec**: §26 as built for this block; the tuning notes' section
   (the sources with their licences, the patches' datums and residuals, the checks as
   printed, the scenario's run, what was found on the way, the suite as run).

The fast tier before the report; `tests/test_known_truths.py --slow -k "gate_5b or
gate_5c"` once, which must pass to the digest, `channel-west` being untouched. No model
identifier in any file; nothing under `docs/agents/consent/` touched.

## Package 39b: the Biscay north block (`biscay-north`; the same files as 39a under its own names; `data/scenarios/biscay-north.yaml` new)

Opus. The second block of spec M6 §26, built as `docs/dev/ChartBlocks.md` says (read it
whole first, with the recipe form over `REGIONS` in `tools/build_charts.py` and package
38's section of the tuning notes). Package 39a builds the Channel east at the same time
in its own worktree: this block touches nothing of `channel-west`'s nor of 39a's.

1. **The region** `biscay-north`: the Raz de Sein and the Penmarks, Lorient and Port
   Louis, Belle Île and Quiberon, the Loire's mouth to Paimboeuf, the Pertuis, La
   Rochelle and Rochefort with the Basque Roads (where the cruise's enemy is "reported out
   of Rochefort"). Bounds 46°N to **48°N, abutting `channel-west` at 48°N exactly** (its
   south bound), 5°W to 1°W, the fetch box widened as the form says. The Raz de Sein
   (48.03°N) and the Chaussée de Sein lie in `channel-west`'s bounds: their marks go in
   `features/channel-west.yaml` (data, no tile) if they are not there, and the Raz's
   stream area is this block's with `chart: atlantic-east`.
2. **The seam**, as 39a's item 2: a tile `channel-west` lists is `channel-west`'s, not
   written again nor listed twice (a rule to add to the tool, printed as a check; 39a adds
   the same rule, and the lead keeps one at the merge: write it small and in one place,
   where the region's tile list is made). After the build `git status` shows no change to
   any tile or coast file `channel-west` listed before, and the report says so. Fetch the
   region whole, for 38's datum finding.
3. **The period data**: the Neptune François and Bellin for the sheets, the French pilots
   for the directions; the lights of 1805 dated (Penmarch, Belle Île's Goulphar, the tower
   of Cordouan is 39c's, Chassiron and the Baleines on the Pertuis). Where a sheet cannot
   be fetched or read, the patch is left and the port file says `datum: unverified`; never
   a figure invented.
4. **The nations**: hostile throughout to a King's ship, open to a neutral. **The tide**:
   TICON's gauges of the block as package 34 read the file (Brest is the eleven's; Le
   Conquet too; Concarneau, Port-Tudy, Saint-Nazaire, La Rochelle-Pallice: unverified
   until read); the streams of the Raz, the Four is `channel-west`'s, the Pertuis
   d'Antioche and Breton, the Loire's mouth by the directions; the epitome's places. **The
   weather**: Biscay's box is PROVISIONAL; a printed climatic table read for the block
   replaces its row and says so in the row's `note`, else nothing.
5. **A scenario** `biscay-north.yaml`: a free passage of the block's stretch (the frigate
   from the Iroise round the Penmarks to the Basque Roads, or the cutter Lorient to
   Quiberon: the package's choice), `chart: atlantic-east`, sailed once at seed 7 to the
   anchor by a short book; its figures in the notes; not a gate's, not pinned.
6. **The build** and 7. **the notes and the spec**, as 39a's items 6 and 7 under this
   block's name.

The fast tier before the report; `tests/test_known_truths.py --slow -k "gate_5b or
gate_5c"` once, which must pass to the digest. No model identifier in any file; nothing
under `docs/agents/consent/` touched.

## Package 42a: the consent brief revised once (`docs/agents/ConsentBrief.md`; `docs/agents/README.md` where the revision is recorded; `freesail/agents/consent.py` only if the re-ask's words need it; `tests/test_officer.py` and a fixture of the brief as it stood; `docs/TechnicalSpec-M6.md` §15 as built; `docs/dev/TuningNotes.md`)

Opus. The one package of milestone 6 allowed to touch `docs/agents/ConsentBrief.md`
(decision 41; spec M6 §15, "Brought forward"). Nothing under `docs/agents/consent/` is
touched: the records are the models' answers and stand as given.

1. **The brief revised** from package 40's draft, `docs/playtests/drafts/consent-brief-m6-draft.md`,
   approved by the owner as drafted (its five marked sections, the two one-clause changes
   kept as clauses), and extended, in the same sections and the same voice, to describe in
   kind what 6b and 6c add (spec §15 lists it: the stations below the officer's, the
   master's and the lookout's; several models at once on one ship, each other's words
   in-world; the API door with the owner at the door; the game replayed from its
   transcript, never as instruction; a model at the captain's station of another ship).
   Each addition is a kind of thing, never a particular (decision 37: the particulars are
   the stations' briefs); where a kind is not yet built, the brief says so in a clause
   ("the game has, or will have before this answer is used again, ..."), so that the
   answer is honest. The brief's own paragraph *The record* says the rule as the owner
   approved it on 2026-10-07 and is not changed. Keep the brief lean: the owner made it
   leaner once by hand, and every sentence added is one a model must read.
2. **The mechanics**: the brief as it stood before this package kept as a fixture
   (`tests/fixtures/ConsentBrief-before-42a.md`, `-text` in `.gitattributes` as the
   earlier fixture is) and the test that a yes on record against it is asked again with
   the changed sections named (`consent.changed_sections`, `consent.why_again`); the
   sha256 pins in the tests and docs brought to the new text; **a test that pins the
   watched sections' text** (the opening, *What an instance would see and do*, *Leaving*,
   *Being stopped*, *The journal*, *What is not done*) by digest, so that a later package
   cannot change one without changing the test and saying why. `docs/agents/README.md`'s
   paragraph on the revisions gains this one. A model is not seated at any station by
   this package, and no re-ask is run: the re-asks are the owner's, through the game's
   own consent step.
3. **The notes and the spec**: §15 as built; the tuning notes' section short (what
   changed, section by section, and why; the suite as run).

Rules: no model identifier in any file; the brief's text is the owner's to approve and
the package's to draft, so the report quotes every added or changed sentence in full.
The fast tier and `tests/test_officer.py` before the report.

## Package 40c: the captain's trials (the lead; `data/scenarios/trials/*.yaml`, `freesail/world/captains.py` for the player's hand, `tests/test_known_truths.py` the trials pinned)

The gate's evidence for the rules-based captain (spec M6 §9 item 1), built by the lead
after 40b: scenarios of the frigate on a station intent off Ushant (the King's ship's
doctrine) and the schooner on her trade (the merchant's), each with a weather script and
world orders at ticks: a stranger of a nation at war sighted (investigating, chasing; the
merchant evading), a gale with the land under her lee (hove to with sea room, clawing off
without), thick weather near the land (running for shelter and the anchor); the states
entered and the books loaded by name proved against the doctrine's table, the rule of the
road at a few cables, the log reading as a captain's. **The player's hand** (decision 41):
a direct order of the ship's given at the prompt on an intent scenario makes the captain
stand aside, said in the log, until `captain: carry on`; a world order does not; the
player's seat under him is given the deck by his book's own words. Pinned; the tuning
notes' section; a short gate document `docs/gates/gate-m6a.md` opened with the owner's
runs.

## Package 37p: the yards and the helm by the wind, and the ship in a gale (`freesail/evolutions/trim.py` for the yards' stagger by level; `freesail/orders/verbs.py`, `grammar.py` and `data/vocabulary.yaml` for the bracing orders; `freesail/physics/integrate.py` for the helm in full and by, the lift as its cue and the recovery from aback; `freesail/evolutions/scripts.py` for `shorten sail`'s headsails and storm canvas, heaving to without way, boxing off; `data/standing_orders/starter.orders` and `data/captains/*.yaml` for the gale's book lines; the primer's chapters 2, 4, 9 and 11; `docs/TechnicalSpec-M5.md` §33 an item; `docs/dev/TuningNotes.md`; `tests/test_trim.py`, `test_physics.py` or their kin, `test_captain_trials.py`, `test_known_truths.py` re-pinned once)

Opus, from the lead's rules below; the gale trials of package 40c are the measure (decision
42's conversation of 2026-10-10 is the ground: the owner's reading of Luce against the
helm's fault). Run before gate 6a's runs, so that the owner can judge whether its changes
want a re-cut of the gate or a version on the same gate. Every recorded passage will move,
since the trim of every ship moves: re-pinned once, at the end, with the reasons.

**The sources, held.** Luce 1884 *Text-Book of Seamanship*, "Working to windward", p. 414
(the quartermaster's words: "Nothing off!", "Very well thus!", "No higher!", "Keep her a
good full and by! or simply Full and by! meaning close by the wind with the sails full", a
small helm) and the footnote on p. 418 ("The upper yards should be braced in more than the
lower, first, because the larger sail having greater curvature than the smaller must have
its yard braced up to a sharper angle, that the plane of both may have the same angle with
the keel; second, because the upper portion of the sail being attached to the yard
approaches nearer to a plane than the lower part which bellies out, hence the upper part
need not be so sharp; and thirdly, the lighter yards and braces require a greater angle for
their support. Further, the upper yards being in, when the main royal is just lifting all
the other sails are a 'clean full and by', which makes it a good sail to steer by"), with
Fincham's 19¼° for the main yard beside it. Luce 1866 *Seamanship*: ch. XXIV, the footnote
on conning ("As the leech of the mainsail reaches farthest to windward, it will be the
first to lift in coming to the wind"); ch. XXV, wind baffling (coming to against the helm,
boxing off, chapelling, taken aback: with headway the helm a-lee, "haul up the mainsail
and spanker, and square the after yards; the moment she gets sternboard, shift the helm,
and she will fall off briskly"); ch. XXVI, heaving to; ch. XXVII, reefing; ch. XXIII,
taking in sail in a gale; ch. XXVIII, storms. Fincham 1843 §94 to §96 (the sails "so
trimmed as just to touch at the same time", the after yards commonly sharper than the
fore, the head yards less sharp with a sea on the weather bow) and his table of angles
(p. 42). Steel 1794 vol. II §25 (the sails 40° with the keel close-hauled, better 30 in
great ships) and its FULL-AND-BY ("neither too nigh the direction nor to deviate to
leeward"); Lever 1808 (the yards sharp up, the weather leeches hauled forward by the
bowlines, "so suited with sail as nearly to steer herself ... with a small helm"). **Said
in the spec**: the steering mark by the royal is Luce 1884's wording; its reasons and
Fincham's "touch together" are the period's, and the game takes the rule as 1805's on
them.

1. **Three levels of bracing.** (a) `brace sharp up` as it is: every yard as sharp as its
   rigging allows, for the evolutions and for pointing. (b) `trim sails` becomes the
   period's trim and the default the books use: each level of yards braced to the wind
   with the level above it braced in more than the level below (the courses' yards
   sharpest, the topsail yards in by a step, the topgallant and royal yards by another),
   the after yards' stagger kept as it is (`AFTER_YARDS_SHARPER_DEG`), the steps as
   constants with Luce's three reasons as their source and the figures judgement, tuned
   once so that with the ship close-hauled under all plain sail the highest sail set lifts
   first and the rest stand "a clean full" (the test). (c) The yards by hand, in the deck's
   words: `brace the fore yards in a point`, `brace the main yards up half a point`, `brace
   the yards to four points` (from the keel, the weather yardarms forward), `square the
   fore yards`, `brace the mizzen yards about`; a mast's yards or all; points and halves,
   never degrees at the prompt (the log may say the angle in brackets as the helm's lines
   do). Given, the yards stay as given until the next trim or brace: in a fluky wind the
   captain sets them and lets them take the wind as they may, and the log says what shivers
   or fills. The forms in the primer's chapter 4 and the forms table.
2. **The helm in full and by.** The helmsman's mark is the highest sail set: he keeps her
   so that it is just lifting and the rest full (Luce's "clean full and by"); after any
   change of sail (a sail taken in, reefed, set) the mark is the new highest sail and the
   angle is found again from it, within a minute. The lift of the lower sails (the
   mainsail's weather leech first, Luce 1866) is the warning that she is too near: the helm
   bears away itself, with a small helm, and the log says "kept her away" once; the line
   "her sails lifting ... keep her away, or she will be taken aback" stays as the warning
   to a captain steering a course by compass, where the helm does not act. Under reefed
   topsails with the light sails in, the mark is the topsail and the angle wider: she is
   never brought up to the old angle. The quartermaster's words `nothing off`, `no higher`
   and `very well thus` as helm orders, if they fall out of the work cheaply (they are
   Luce's; optional).
3. **Storm canvas.** `shorten sail` takes in the headsails as the wind rises (the jib
   first, before it blows out of the bolt-ropes: the sail's own rating is the rule), and
   sets the storm staysails that the ship files already carry in the sail room (the fore
   storm staysail; the mizzen's) when the wind is over the storm-sail line, so that she
   keeps steerage way and a sail to lie to under; the order `set the storm staysails` for
   the captain, and the gale lines of the starter book and the captains' "hove to for
   weather" books saying it (close-reefed topsails, the storm staysails, lying to under
   the main staysail or the close-reefed main topsail as Luce ch. XXVI has it). A ship with
   nothing set at all in a gale is the fault the trials found; after this package the log
   never says "no sail is set" with the wind over thirty knots unless the captain ordered
   it so.
4. **Heaving to without way, and the recovery from aback.** `heave to` must complete with
   the way she has: with sternway or none, the yards are braced for lying to as Luce has
   it and she lies to, drifting, with the log saying so, rather than the evolution waiting
   for a way that never comes. Taken aback with no way (the trials' "her sails aback; she
   had no way on to lose", once a minute for an hour), she pays off: the wind on the backed
   sails and the helm shifted with the sternway bring her head off (`integrate.py`, the
   aback state yawing to leeward and gathering sternway until the sails fill), and the
   order `box her off` (Luce ch. XXV, boxing off) does it by the script that already
   exists for box-hauling where the helm's own paying off is too slow; the helm in full and
   by orders it itself after two minutes aback, and the books have the line. The measure:
   in the gale trials she is never aback longer than a glass, and the frigate's drift
   lying to under storm canvas is a knot to a knot and a half through the water (truth 28,
   a night's drift hove to) and not four knots over the ground.
5. **Re-measured once**: the six recorded passages, the gate's day, the two intent
   fixtures and the five trials, re-pinned at the end with the old figure beside each and
   the reason in the tuning notes (the trim moves every tick's drive; where a passage's
   outcome changes, say what changed in play and not only the digest). The pace floors
   not re-run under load.
6. **The notes and the spec**: §33 an item (the trim by level with its sources, the helm's
   mark, the gale); the primer's chapters 2 (the mark the helmsman steers by), 4 (the
   three levels of bracing and the forms), 9 (the gale: storm canvas, lying to, boxing
   off) and 11 (the starter book's gale lines); the tuning notes' section with the
   constants and their sources, the trials before and after, and the suite.

Not this package's: a gale's damage beyond what the sails' ratings already do; the hull's
behaviour in a sea beyond truth 28's drift; the lugger's lugs (43b). Tuned once and
cheaply: the trim's steps and the storm line are set from the sources and the trials, not
iterated for a prettier passage. The fast tier before the report, and the whole slow tier
once at the end, since every pin moves.

## Package 37p, as merged (2026-10-10)

Merged with 41 and 42 resolved in its worktree; the lead's ruling that a say heard by
nobody carries its place and hearers like any other (the log is the ear) folded in and
truth 78 re-pinned for it. The tuning notes' section (`docs/dev/TuningNotes.md`, "the yards
and the helm by the wind, and the ship in a gale") carries the constants and their sources,
the step and the mark tuned once, the gale trials before and after, what was found on the
way and every pin moved with its reason; spec M5 §33 item 26 is its record. The measure:
the station and the lee-shore trials aback 11 and 70 minutes in twenty hours where they
were aback 290 and 412, the longest stretch under three minutes where it was an hour and
more; lying a-try under the close-reefed main topsail and the storm staysails at 1.3 to
1.4 knots over the ground; nothing aground, no sail lost but the mizzen storm staysail in
a gust of the whole gale.

**Open for the owner**, none of them blocking the gate:

1. **Two strict expected failures** left for the lead in the slow tier: `back and fill`
   shoots through the wind under the keel's grip astern, and the schooner's studding-sail
   set-up is caught in irons. Both are evolutions the gate's runs do not touch; a short
   package or 43's physics work takes them.
2. **The drift lying to** is 1.6 knots on the mean through the water in forty-five knots
   (truth 28), the brief's measure a knot to a knot and a half; the hull's resistance
   astern is still its resistance ahead (spec 3b §9, the owner's ruling) and the builder
   did not tune further. Left as it stands unless the owner's runs find her driven too
   fast.
3. **The trade-off of the period's trim**: full and by the frigate now lies 67.5° from
   the true wind at 5.1 knots where she lay 76° at 6.8, a quarter slower through the water
   and a sixth more made good to windward; every passage by the wind took longer and was
   re-pinned. Luce's own half point a level put her at 93°, so the step is two degrees.
   The owner may want a feel for it at the helm before it is called settled.
4. **The starter book's heavy weather** sets the storm staysails by one order,
   `set the storm staysails`, folded into the routine (three orders where there were four);
   truth 37 keeps the old copies of the book as they were.
5. **The captain after the gale** (40c's ground, not this package's): the station trial
   beats for the station under the main topsail and two staysails to the end, the
   captain's state flipping to hove to for a minute and back, the beating book not making
   sail again. The gate's item 2 says so; 43 or a small captain's patch takes it.
6. **The sternway yaw's fade-in** (none under a knot astern, whole from two) is
   judgement, taken so that truth 17's frigate getting under way from rest is not thrown
   about by the first inch of sternway; the full-and-by helm still over-swings in light
   airs after a box-off (the gripe with no way on, which predates the package).

## Package 41: the wardroom (`freesail/agents/agent.py` for the master's and the lookout's stations, their domains and briefs, the cadence; `harness.py` for the conversation, the stand-by on several conditions, `you may` down the ranks; `tools.py` for the new tools and the authority filter at the new stations; `remote.py`, `mcp_server.py`, `local.py`, `repl.py` for the doors; `seat.py` for the player at the master's and the lookout's; `fake.py` for the fake master and lookout; `freesail/core/world.py` and `freesail/ui/server.py` for the pace rule and the `pace` reading; `freesail/api/readings.py`; `freesail/world/reckoning.py` only where the master's figure replaces the ship's; `freesail/world/captains.py` where the rules-based captain is the captain over a seated officer; `freesail/standing/grammar.py` only if the stand-by's conditions need a form the dialect lacks; `docs/agents/Harness.md`, `docs/agents/README.md`; the primer's chapter 16 and a chapter for the wardroom's stations; `docs/TechnicalSpec-M6.md` §11, §12, §16 as built; `docs/dev/TuningNotes.md`; `tests/test_wardroom_doors.py` new, `test_agents.py`, `test_officer.py`, `test_captain.py`, `test_mcp_server.py`, `test_known_truths.py` truths 82 to 85)

Fable: the harness's second large design, the stations and doors of spec M6 §11 and the
pace rule of §12 (decision 39's ruling 2), on the ground of 40 (the captain's station, the
player's seat), 40b (the slate as data) and 42a (the consent brief, which describes the
master's and the lookout's stations already and is not touched: `docs/agents/ConsentBrief.md`
and `docs/agents/consent/` are 42a's and the owner's; `tests/test_officer.py` pins the
brief's digest). No model is seated by this package; the fake stations prove it, and the
owner's wardroom game is gate 6b's.

1. **The master's station.** A model at the master's place (the frigate's master, the
   schooner's and the cutter's mate stand as the file binds them: `stations: master:` in
   the wardroom files, added by this package) works the ship's reckoning when the master
   would: at noon, at a fix, at the captain's word (`work up the reckoning`), and is given
   the slate of 40b as the officer is (`work my reckoning`'s data) with the sights as the
   ship takes them; his figure becomes the ship's account when it comes in time, and the
   simulated master's stands when it does not (G19's third step; the brief says so and the
   log says whose figure it was). His domain is the reckoning, the sights, the lead and the
   chart's queries; no order of the deck (the consent brief's sentence); `you may` from the
   owner or the captain's station may widen it as the officer's. The fake master works the
   slate's words by the traverse as truth 80's fake officer does.
2. **The lookout's station**, for a small model (M5 open item 6): the masthead's sightings
   put into his words (`the lookout` reading and the sightings as they come), `make her
   out` on a sail, the warning of a danger ahead; no order but `hail`. His cadence is on
   events (a sighting, a loss, a change in what is seen) and the glass, never the sample's
   every minute; his brief says what he counts and the three ways of stopping, in the
   officer's form.
3. **The stand-by on several conditions** (the owner's note 3 of 2026-10-09; the review's
   I7 item 3): `stand by until <x>, or <y>, or <z>` takes a list of conditions in the
   standing dialect's own words (an event, a bell, a reading's threshold, a sail sighted,
   the land in sight), any of which wakes the station, each named in the wake's line; the
   conditions at parity with the book's, so that a condition the book can read the stand-by
   can wait for; refused in the dialect's own words when one cannot be read. A wait for an
   event still ends at eight bells, as the officer's does.
4. **The deck's conversation.** A station addresses another by its person's name or its
   station: `ask the master for a course`, `tell the first lieutenant to shorten sail`,
   `say <words>`; the words are a log line with a place aboard (the quarterdeck, the
   cabin, the masthead) and a hearer, carried in the hearer's next sample as the
   captain's `tell` is now; `say` is heard by whoever is in the same place, the player at
   the prompt included (he is where the captain is). Nothing a station says is ever an
   operator instruction to another (the fourth commitment): the harness keeps the
   speaker's name on every line and sends it as a line of the game. A question put to a
   station is answered on its next sample, and the asker told when no answer comes by the
   patience. The player at his seat speaks the same way.
5. **Who may give what.** `you may` flows down the ranks: the owner to any station, the
   captain's station to the officer's and the master's, nobody upward; a station's `stand
   down` is its own, `stand down the <station>` the owner's and the captain's. **The
   rules-based captain over a seated officer**: on an intent scenario with nobody at the
   captain's station, a model or the player at the officer's is given the deck by the
   captain's book's own words with his standing orders in force over it (40c's gate item
   6 has the owner typing `you have the deck` as the owner; here the captain gives it, and
   takes it back for a judgement that needs the deck, saying so). **The player's seat** at
   the master's and the lookout's stations beside the officer's (`SEAT_STATIONS`), with
   each station's authority, so that the owner may hold a lowly station in his wardroom
   game (gate 6b).
6. **The doors.** Each client its own bridge asking for one station, as now, with
   `--station master` and `--station lookout` at the MCP bridge, the local runner and the
   REPL; a second door asking for a held station refused in words; a station found by its
   name and its key; three stations through three in-process doors in the tests (two
   fakes and the player's seat; truth 82), and a game with three seated saved and loaded
   from its checkpoint with three, each re-seated station reading its own journal (truth
   85's first half; its second half, the replay on a build whose sampling differs, is
   42's transcript-driven replay).
7. **The pace rule** (§12; decision 39, ruling 2). The clock slows to 1x while any model's
   sample is open, whoever holds it, at whatever station, and returns to the set
   compression when every open sample has been answered or has stood by; not lockstep (the
   ship sails on at her own second while the model thinks, a slow answer lands late);
   `--lockstep` stays as the separate option; free-running at the set compression stays as
   the flag for the solo player. Each station's **cadence** (every glass, every watch, on
   events only) is a setting of the seating, said in its brief. A `pace` reading says the
   compression, which samples are open and since when; the log says once when the clock
   has been held for a station longer than a stated time (a constant with its reasoning).
   The owner's testing setting is the default; the pace truth of M5 §30 is measured again
   with three stations sampled at a glass each at 60x, on the build machine (§27).
8. **Truths 82 to 85** in `tests/test_known_truths.py`, on the cutter's free passage with
   fakes: the captain's `you may` to the officer and each order under its own mark (82);
   the clock at 1x while a sample is open and back at the set compression when it is
   answered, a stand-by releasing it (83); a `say` on the quarterdeck heard by the station
   there and not by one below (84); the save with three seated (85). No recorded passage's
   pin moves: none has a station seated, and the pace rule changes no tick of the world
   (the clock's compression is the driver's, not the simulation's).
9. **The docs**: `Harness.md` a section for the wardroom (the stations, the conversation,
   the stand-by's conditions, the pace rule and the cadence, the doors' flags),
   `docs/agents/README.md` where the stations are listed; the primer's chapter 16 amended
   and a chapter for the master's and the lookout's stations in its form; spec §11, §12
   and §16 as built; the tuning notes with the constants, the pace measured, what was
   found and the suite as run.

**Added at launch (the owner, 2026-10-10).** Stations are data on the ship, bound at run
time, never a table in code: the set of stations and the person holding each live on the
world as a binding (the wardroom file's `stations:` its starting state), with bind and
unbind as the two operations the harness uses and a world order will drive later (M7b's
director: `person: "Mr Fox" comes aboard as master`, on the `person:` channel; the road
aboard the boat we have); a station unbound under a seated model releases it with a line;
a person's brief is built from the person's outline, so a person made from words later
carries what a brief needs. And a generic **passenger** station ("a person aboard", the
owner's word): no domain of orders, the readings and the journal, `say`, `ask` and
leaving; held by a person of the muster or one who comes aboard, so that a model or the
player may be aboard with no duty and a person brought aboard later has a station to
stand in; the consent brief covers it in kind already. Tests: a station bound to a new
person at run time taken by a door; one unbound under a seated fake released with its
line; a passenger hearing a `say` on the quarterdeck and giving no order.

Not this package's: the API door and its security pass, and the transcript-driven replay
(42); the consent brief and the re-asks (42a, the owner's); a model captain of another
ship (43); making a person from words and the story's reasons (the director's, M7b). Work
it like a senior engineer and go beyond the letter where it fits the
intent (the owner's standing word for the Fable packages), saying where. The fast tier
before the report; the slow tests of the files touched; the pace truth measured on the
build machine with the load said.

## Package 42: the API door and its security pass, the replay driven by the transcript, the chart as an image (`freesail/agents/api.py` new; `freesail/agents/harness.py`, `journal.py`, `remote.py`, `tools.py`, `mcp_server.py`; `freesail/core/replay.py` and `core/world.py` for the station's acts as inputs; `freesail/ui/server.py` and `client/map.js` for the chart's picture; `pyproject.toml` for the SDK in the `agents` extra; `docs/agents/Harness.md` a section, `docs/agents/README.md`; `docs/TechnicalSpec-M5.md` §33 item 11 closed; `docs/TechnicalSpec-M6.md` §13 and §14 as built; `docs/dev/TuningNotes.md`; `tests/test_api_door.py` new, `test_replay.py`, `test_agent_api.py`, `test_mcp_server.py`, `test_known_truths.py` truths 85 (its second half) and 86)

Opus. Spec M6 §13 and §14, on the harness as 37g, 40 and 42a left it; it runs beside 37p
(the trim and the helm; no file in common) and 41 (the wardroom: the stations and the pace
rule; the two meet in `harness.py`, `remote.py` and `mcp_server.py`, so keep each change
small and local, and the lead resolves the merge). The consent brief already names a
session through an API door (42a); `docs/agents/ConsentBrief.md` and `docs/agents/consent/`
are not touched, and no model is seated by this package: a test server standing for the
API is the whole proof.

1. **The API door** (`freesail/agents/api.py`): a runner on the same harness as the local
   runner (`local.py` is the pattern: a client of the running game and of the model, no
   World of its own; `remote.GameClient`; the consent gate run by the game), speaking to a
   hosted model through its own API, the Anthropic Messages API with tool use first, by
   the official Python SDK (`anthropic`, added to the `agents` extra; imported inside the
   door, so that the game runs without it). The same turn, tools, brief, budget, handover
   and three ways of leaving as every other door, built on `local.py`'s translation of
   package 27's turns (the brief as the system prompt; a sample as a user message; tool
   results answering the tool calls by id; the opt-out token looked for in every reply and
   every tool argument before anything else reads them). The settings: `--model` (no
   default in the repository: the model is the owner's choice at the command line or in
   the environment, and no model identifier is written in any file), `--effort` (the SDK's
   adaptive thinking, with the effort levels the API offers; off when not asked),
   `--max-reply`, `--request-timeout`; streaming for every request, the final message
   taken whole from the stream (long replies would otherwise time out); the brief and the
   library marked for prompt caching, since they are sent every turn and the cost is the
   owner's; the server's own token counts kept and said at each handover and at the end
   (what the server reported it used, in and out, cached and not); a reply cut off at the
   limit asked once more (37i's rule), then the stand-by. The identity for the consent
   record is the model name the server reports, in the record's form for a served
   identity. The OpenRouter dialect (decision 31): the same door on the OpenAI-shaped
   chat-completions with tools that `local.py` already speaks, with its own key name and
   base URL, if it falls out of the shared shape cheaply; else say what it would take.
2. **The security pass**, the package's other half. The key is read first from the
   platform's credential store through the `keyring` package (the Windows Credential
   Manager, the macOS Keychain, the Secret Service on Linux; the owner's note of
   2026-10-10, from another project's practice), under a service and account name of the
   game's, put there once by `--store-key`, which prompts without echo and writes nothing
   else; second from the environment (`FREESAIL_API_KEY`, and the SDK's own variable as a
   second name); third from a file named at the command line outside the repository, for
   a machine with no store; never from a setting file the game writes. The tests use a
   fake keyring backend and never touch the real store;
   it is never logged, saved, journaled, in a transcript or in a sample; request and reply
   bodies are journaled without their headers; the door refuses to start when the key
   would be written anywhere the game keeps (the records folder, the saves, the journal);
   no key, URL token or account detail is ever in the repository, and a test greps the
   repository and the records the tests write for the shapes of a key (the SDK's prefix,
   OpenRouter's, a bearer header) and fails on any. The base URL is a setting so that the
   tests point the door at a local test server and the owner may point it at a proxy.
   `docs/agents/Harness.md`'s section says all of it to the owner, with the setup in his
   words (where the key lives on his machine, what the door sends, what it costs and how
   it says so).
3. **The replay driven by the transcript** (§14; decision 36's promise of a replay on any
   build). A station's acts (an order given, a `say`, a stand-by, a `you may` from the
   captain's station, the leaving) are journaled at their ticks as inputs, as the driver's
   lines are, so that a replay applies them at their ticks whatever the build's sampling
   would have asked, and the transcript becomes the record and not the replay's source;
   the acts of 40's player's seat already go this road (`seat.taken` and the seat's
   refusals), and the station's follow the same form. A save of this build with a station
   seated replays on a later build whose sampling differs to the same log (truth 85's
   second half, with a test that changes the sampling and replays); a save from before
   replays as it does now, from its checkpoint, and says so. M5 §33 item 11 (a door act at
   the stationing tick, before any tick has run, not made by a replay) closes with it: say
   in §33 how.
4. **The chart and the ship's view as images, through the doors that carry one** (the
   owner's note 7 of 2026-10-09; spec §13's second paragraph). The lead's design decision:
   the open browser renders the picture as the player sees it and posts it to the server
   on the tool's request, since the chart's drawing lives in `client/map.js` and the
   ship's in the viewer, and a second renderer in Python would be a second picture to keep
   true; where no browser is open the tool says so in words and gives the reading instead.
   Two tools: `the chart` as the player sees it, and `the ship's view` from any angle the
   viewer offers (the owner, 2026-10-10: the viewer serves well already, sessions he has
   sent its pictures to have used them, and the view at the moment the request comes
   through is what they get; the words of the view are the ship's state readings, which
   they have), at the MCP door (a tool result may carry an image, and Claude Desktop and
   Claude Code read it) and at the API door (an image block in the tool result), the
   picture shelved as the library is, never in the journal or the transcript (a note that
   it was shown, with its size and the angle asked, is). The browser's part is one request
   from the server to the open page for a rendering at an angle and one post back, with a
   bound on the picture's size.
5. **Truths 85 and 86** in `tests/test_known_truths.py`: the replay on a build whose
   sampling differs (85) and the API door's test server receiving no key in any body,
   with the journal, the transcript and the save holding none (86), the test server a
   small local HTTP server in the tests speaking the Messages API's shape (a tool call
   and a text reply, a cut-off reply, a refusal), no network.
6. **The docs and the notes**: `Harness.md` (the API door's section, the chart's picture,
   the replay's rule), `docs/agents/README.md` (the doors listed), spec §13 and §14 as
   built, M5 §33 item 11, the tuning notes' section (what the door sends per turn and
   what the test server saw, the replay's test, what was found, the suite).

No recorded passage's pin moves (nothing here touches a tick of the world; a pin that
moves is a finding). Not this package's: the wardroom's stations and the pace rule (41);
the re-asks (the owner's). The fast tier before the
report and the slow tests of the files touched.

## Packages 39c to 39f: the last four blocks of the chart line (the same files as 39a and 39b under each block's names; `data/scenarios/<block>.yaml` and `.orders` new per block; `docs/TechnicalSpec-M6.md` §26 as built; `docs/dev/TuningNotes.md`)

The rules of 39a and 39b hold for each of the four blocks below, and `docs/dev/ChartBlocks.md`
as the first two corrected it is the how-to (read it whole; the seam rule, the fetch box
covering the tiles whole, GEBCO's fill raised to the chart's datum where the recipe asks,
the sources' earlier fetches kept, `held_gauges:` for a block's gauges held unblended, the
`book_limits` box widened, the ports' spots with their own positions, a neighbour's marks in
a neighbour's file and the lead rebuilding that neighbour's index at the merge). Each block
abuts its neighbours exactly at the bounds given; a tile another region lists is that
region's. The four run at once in four worktrees and touch the same shared files (the tool's
recipes and `CHARTS`, the manifest, the tide files, `nations.yaml`, the tests' port lists
and counts): keep every addition self-contained and in its own named place, and when the
lead asks, merge the branch head into your worktree and resolve against it as 39b did. The
recorded passages and the trials replay to their digests, which the slow tier proves once
(`tests/test_known_truths.py --slow` whole, not a `-k` selection). No model identifier in any
file; nothing under `docs/agents/consent/` touched; downloaded data in its own fresh
directory under `.cache/`, never run or imported, read with `-I`.

### Package 39c: Biscay south and Galicia (`biscay-south`)

Opus. Spec M6 §26 item 3. Bounds **42.0 N to 45.9 N, abutting `biscay-north` at 45.9 N**,
9.0 W to 0.9 W (the Galician coast to the Minho taken into this block, so that Vigo and
the Spanish shore north of 42 are one region's). The Gironde to Bordeaux's river mouth
(the river itself M8's), Arcachon's entrance as the directions have it, Santander, the
Asturian ports the pilots name, Ferrol and Corunna, Cape Finisterre, Vigo and Bayona. The
period data: Tofiño's *Atlas Marítimo de España* (1789; the scans at the national libraries,
unverified at full resolution; public domain) for the Spanish sheets, the *Derrotero* for
the directions; the Neptune François and Bellin for the French corner where 39b left them
unread; the lights of 1805 dated (Cordouan is this block's; the Spanish lights the
Derrotero gives). Nations: Spain at war with Britain in June 1805, hostile to a King's
ship and open to a neutral; the French ports as 39b has them. The tide: TICON's gauges of
the block held unblended (Bordeaux, Santander, Gijón, Corunna, Vigo: which it has is
unverified until read), the Gironde's stream and the Spanish ports' by the directions, the
epitome's places. The weather: Biscay's box stays PROVISIONAL unless a printed table is
read. A scenario: the schooner from the Basque Roads to Corunna across the bay, or the
cutter Vigo to Corunna round Finisterre; sailed once at seed 7; not a gate's.

### Package 39d: Portugal and Cadiz (`portugal`)

Opus. Spec M6 §26 item 4. Bounds **36.4 N to 42.0 N, abutting `biscay-south` at 42.0 N and
the Strait's block at 36.4 N** (so that Cadiz and its bay, at 36.5 N, are this block's and
Trafalgar the Strait's), 10.0 W to 6.0 W. Oporto's bar and the Douro's mouth, Aveiro,
Figueira, the Berlings, Peniche, Cascais road, Lisbon and the Tagus to the town (the river
above it M8's), Setúbal, Cape St Vincent, Lagos bay, Faro, Cadiz and its bay with Rota. The
period data: Tofiño for the Spanish sheets and Cadiz; the Portuguese coast from the period's
English directions (Norie, Faden, the *Oriental Navigator*'s Lisbon) and Tofiño's
Portuguese sheets; the lights of 1805 dated (the Berlings, Cape St Vincent's convent light,
Cadiz's San Sebastián, and whichever the directions give). Nations: Portugal neutral in
1805, open to all; Cadiz blockaded, which the port files gain as a state of a port (`state:
blockaded`, with what it means to a stance: closed to the blockaders' enemies and watched
by their ships, a thing for 6c's world's business to read; say in §26 what you built and
what you left). The tide: TICON's gauges held (Leixões, Cascais, Lagos, Cadiz: unverified
until read), the Tagus's stream by the directions, the bar of Oporto's by its pilots. The
weather: the Portuguese coast's box with its summer northerlies, PROVISIONAL unless a
printed table (the *Oriental Navigator* or Purdy has them) is read. A scenario: the frigate
from Lisbon's road to Cadiz bay, or the schooner Oporto to Lisbon; sailed once at seed 7;
not a gate's.

### Package 39e: Madeira and the Western Islands (`madeira` and `azores`; the corridor widened)

Opus. Spec M6 §26 item 5, widened by the owner's word of 2026-10-10 (decision 44) to the
Western Islands, the period's name for the Azores. Two regions in one package: **`madeira`**,
32.0 N to 33.5 N, 17.5 W to 16.0 W (Funchal and its open road, Porto Santo, the Desertas; the
island's lights and marks as 1805 had them; the voyage's end as an anchorage in a road with
a swell), and **`azores`**, 36.5 N to 40.0 N, 31.5 W to 24.5 W (Angra do Heroísmo on
Terceira, the main port and road; Ponta Delgada on São Miguel; Horta on Faial, the road
between Faial and Pico; the other islands as marks and dangers, the Formigas among them).
**The corridor widened**: the Western Islands lie west of the corridor's 20 W, so the
corridor is rebuilt by `--corridor` with its west bound moved to 32.0 W (the recipe's
`bounds` and `fetch`; GEBCO's extract fetched again over the wider box), its existing
tiles byte-identical after the rebuild (the tiles are whole on a fixed grid and the source
the same: prove it by `git diff --stat` over `data/charts/tiles/1/` showing only tiles
added, and say so in the report; if any existing tile changes, stop and report before
committing); the chart's envelope in `CHARTS` and the weather's and tide's tables reaching
the islands (a weather box for the Azores' high, PROVISIONAL and judgement, said so in the
row's note; the tide's gauges held unblended: Funchal, Ponta Delgada, Horta, Angra:
unverified until read). The period data: the English pilots of the 1790s and Norie for
Funchal road and the islands (the Admiralty's surveys are later; the block says what it
rests on, as 35b did); Tofiño's or the Portuguese sheets where any exist; the lights
dated. Nations: Portuguese, neutral, open to all. Scenarios: the schooner from Funchal
road to Porto Santo and back; and the frigate from Funchal to Angra's road, a free passage
of three or four days across the widened corridor, the reckoning by the log and the noon
sight alone, the landfall on Pico's peak (which stands 2,350 m and is seen from thirty
leagues in clear weather by the directions: the lookout's horizon rule tested at that
height); sailed once each at seed 7; not a gate's.

### Package 39f: the Strait (`strait`)

Opus. Spec M6 §26 item 6 (the owner's ruling 4 of decision 39, the Mediterranean to come
on its own chart line after this). Bounds **35.5 N to 36.4 N, abutting `portugal` at 36.4 N**,
6.5 W to 5.0 W. Cape Trafalgar, Tarifa and the Strait's streams, Gibraltar and its bay
with Algeciras, Ceuta, Tangier and the African shore between, Cape Spartel; the Pearl Rock
and the Strait's dangers. The period data: Tofiño for the Spanish side and the Strait; the
period's English directions for the Strait's currents (the constant inset from the Atlantic
and the tides over it, which the tide model takes as a stream by area: an area with a
constant set added to the tidal stream, which the stream model may need a field for; say
what you built); the lights of 1805 dated (Europa Point's, Tarifa's, Spartel's if any).
Nations: Gibraltar British; Ceuta and Algeciras Spanish, hostile to a King's ship; Tangier
Moorish, the nations table gaining Morocco (neutral, open to all, its stance toward each
nation as the period had it, with the source or judgement said). The tide: TICON's gauges
held (Gibraltar, Tarifa, Ceuta, Tangier: unverified until read), the Strait's streams by
area from the directions, the epitome's places. A scenario: the frigate from Cadiz bay
through the Strait to Gibraltar's bay against the inset, with the land of both shores in
sight; sailed once at seed 7; not a gate's. Built last in the voyage's order but launched
with the others; its seam with `portugal` is its only neighbour.
