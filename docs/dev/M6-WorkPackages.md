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
| 39a to 39f | Opus | The six blocks of the voyage to Madeira and the Strait | 39a (channel-mid) merged 2026-10-09, bounds 48.5 N to 51 N and 3 W to 1 W, Morlaix's patch left; 39b (biscay-north) building; the rest after them |
| 40 | Fable | The ship's company and the rules-based captain in three layers; the captain's station; the player's seat | merged 2026-10-09 (the officer's reckoning moved to 40b; the consent brief's revision drafted for the owner, `docs/playtests/drafts/consent-brief-m6-draft.md`, held for 42) |
| 40b | Opus | The lessons in the primer; the officer's own reckoning (spec M6 §5, truth 80; moved from 40 at the owner's word) | merged 2026-10-09 (an own reckoning carried on past noon, the lead's ruling; chapter 13 stays out of the primer test) |
| 40c | the lead | The captain's trials: the gate's pinned scenarios of the rules-based captain under weather scripts and world orders; the player's hand on an intent scenario (the captain stands aside until `captain: carry on`) | merged 2026-10-10; gate 6a opened (`docs/gates/gate-m6a.md`) |
| 42a | Opus | The consent brief revised once from 40's draft, describing in kind all of 6b and 6c that the rule watches; the watched sections pinned; the re-asks the owner's | merged 2026-10-10 (decision 42: the added sentences approved; the re-asks the owner's) |
| 41 | Fable | The wardroom: several doors, the pace rule, the deck's conversation, the master's and the lookout's stations, the stand-by on several conditions | brief to write |
| 42 | Opus | The API door and its security pass; the transcript-driven replay (the consent revision moved to 42a) | brief to write |
| 43 | Fable | The crewed promotion, a model captain of another ship, the far-detail guard, the director's seat hook | brief to write |
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
