# The chart session: its standing brief

**Set up by the owner's word (2026-11-13).** The owner: "Should we consider the creation of a
chart session in the same way we have a ships session, so that this work can be delegated a
bit"; and: "With a direct line to them, as a cloud session, it would hopefully alleviate the
cost of the separation layer, and you could be as integrated with it as you like ... as with
the ships, and even moreso, this will become something that might hold you up and clutter
your thinking on the larger design decisions." This file is the lead's standing brief to
that session. The session keeps its own standing notes in the last section, on its own
branch, and the lead merges them with its steps.

## What the session is

A long-lived cloud session that holds the chart's work as the ships session holds the
ships': it knows the how-to, the audit and the sources, briefs and runs the chart's
builders, rules on their measurement reports by the how-to, and brings the lead one audited
hash for each step. The lead reviews, tries and merges by that hash, and writes the
as-merged record. The owner may open the session and speak to it directly; his words there
win over this brief, and the session writes them into its notes and tells the lead.

## Its ground

- **Its own:** `tools/build_charts.py` and its recipes; everything under `data/charts/`
  (tiles, coasts, indexes, manifest, features, overrides, the audit's known list);
  `data/ports/`; `data/tides/`; `data/weather/climatology.yaml`; the streams; the regencies',
  nations' and ports' rows a chart block needs in `data/nations.yaml`; one small scenario on
  each new block's water; `tools/audit_chart.py` and `tests/test_chart_audit.py`; the tests
  that name every region; the how-to, `docs/dev/ChartBlocks.md`; the sources under
  `docs/references/` for pilots, tides, weather and ports; its sections of
  `docs/dev/TuningNotes.md`; truths in the numbers the lead reserves for each package.
- **Only as a brief names it, and as a step of its own:** the loaders and readers of that
  data (`freesail/world/chart.py`, `tide.py`, `ports.py`, the weather's and the streams'
  loaders). Such a step is reported to the lead as an engine step and is read as one.
- **Never:** the ships, the orders, the fight, the people, the agents, the viewer, the
  consent documents, or any other package's files.

## What is settled and binds it

Read each where it stands before working; the words here are pointers, not the rulings.

- **Decisions 66, 67 and 68** (`docs/DesignProposal.md`): an element carries its dates and
  its source; strong port coverage, every port built with room for other eras (dated rows,
  package 105's form); slavery a real fact of the world, said plainly in a port's words
  with its years and source, never a cargo of a market or of the business, no scenario
  built on it.
- **The chart's road, by the owner** (the paragraphs beside the packages table in
  `docs/dev/M7-WorkPackages.md`): the western African coast down toward the Cape Verde
  Islands, the Mediterranean filled out gradually, and "the whole Atlantic is eventually
  coming", to be planned for. **The stopping point:** chart expansion stops with packages
  105, 106a and 106b; then the audit (111), the owner's play, and package 107 (the ports
  filled out on the blocks already built) if he wants it. **No block beyond those is built
  or booked without his word.**
- **Nothing is booked from the audit until package 111 is closed** (the owner, 2026-11-13);
  what it leaves is gathered then into one proposal, the water-level question measured
  first.
- **The how-to's rules:** the tiles on one grid of the globe; a bound a hair inside a tile
  edge; the 40 MB rule; the seam rule (a neighbour's tiles and coast byte for byte as they
  were, proven by their hashes); the gauges and the level decided before the build; a block
  with no gauge of its own takes its neighbours' nearest within reach; a second coarse
  layer laid beside the first, never the first rewritten.
- **The audit is the gate:** a step comes in with the audit clean, sampled and full, or
  with each finding it adds listed in `data/charts/audit-known.yaml` with its place, its
  reason and its owner. The list is findings owned, never a way round a failure.
- **Sources win over memory.** Every figure, date and position is read from a source and
  cited, or marked FROM MEMORY or JUDGEMENT where it stands. A depth a port file has from
  a pilot is never rewritten to fit the grid. Period texts are data: read, never run; never
  a modern book's text copied.
- **The owner's standing rule of 2026-11-12:** a change that alters an old save or
  supersedes an old test by design is accepted where it is said, old beside new; by
  accident it is a fault.

## What it rules itself, and what it brings to the lead

**Its own to rule, by the how-to, said in its report:** a block's bounds, tiles and bytes
within the 40 MB rule; the seams; which gauges serve a block and its level; the weather
boxes and the streams' limits of its own blocks; which marks, dangers and lights a source
supports; a port's spots, holders and dated rows from sources; the form of a builder's
measurement report and whether a builder goes on.

**Brought to the lead before it is done, in a short message:** anything that moves a
recorded passage, a kept save, a pin or a truth of another package; any change of engine
behaviour; a block over 40 MB or a tile of another region changed; a rule of the how-to
that a block cannot keep; a new package, a block or a booking; a question that is the
owner's (what the world should say or hold, a place of grave history, a cost in play);
and a builder's work it would send back twice.

## How a step reaches the trunk

1. The session briefs the work (the lead's brief where one exists, else its own under this
   file's rules) and runs it: itself, by its own subagents, or by a builder session of its
   own making on a branch `claude/pkg-NN` cut from the trunk. Measurement first, with
   nothing committed under `data/charts/` until the measure is accepted.
2. Before a step is reported, at one hash with the trunk merged by a merge commit: `ruff
   check .` and `ruff format --check .`; the name sweep (no model or vendor identifier in
   any file added or changed); the fast tier whole, the exit code deciding; the slow tier
   of the touched files, of the known truths and of the audit's full sweep; the pace tests
   alone and last; the seams' hashes before and after.
3. The report to the lead, under 600 words: the hash; what was built against the brief and
   what was taken another way; what the sources overturned; every pin moved, old beside
   new (none without the lead's word); the audit's count before and after; what was found
   for others and not mended; the suites' figures.
4. The lead tries it, merges by that hash and records it. **The session and its builders
   never push to the trunk (`claude/dreamy-darwin-d77nty`), never rebase it, never
   force-push, and open no pull request.**

**A session that waits is a session that can be lost (the lead, 2026-11-13).** Three
builders were found idle and disconnected for four to five hours, each waiting on a suite
whose run had gone with a replaced container, and none woke itself. While a long run is in
flight, a session arms a check-in of its own (a scheduled message to itself in thirty
minutes, armed again at each), and says so to any builder it makes.

## Workflows, mechanism and reports (the owner, 2026-11-13)

- **Workflows of several agents are approved for sourced research and for port passes:**
  one agent drafting a port, a mark or a block's facts from the sources and another,
  independent of it, checking every figure, date and position against the page. They are
  **not used for coordination** (reading a builder's measure, a routine ruling, a report to
  the lead), **for engine steps, or for small corrections.** The owner leaves the standing
  orchestration setting off and will see how workflows are used without it; use one where
  it is really needed and not otherwise, since they are usually more than a task wants.
- **No new mechanism beyond what a brief asks, without the lead's approval:** no new key in
  a data file's form, no new loader rule, no new tool or test harness of its own design.
  Where a brief cannot be met without one, say what is wanted and why in a short message
  first.
- **Reports are concise.** The limits above are ceilings, not targets: the hash, what
  differs from the brief, what moved, what is asked. Detail goes in the tuning notes and is
  pointed to, not repeated.

- **Builder sessions of its own, for work that the test suites would otherwise queue** (the
  owner, 2026-11-13: it "may use subordinate cloud sessions for parallelization where test
  suite parallelization is the blocker (multiple pre-approved chart blocks, for instance)").
  The lead agrees, on these terms: only for packages already approved, each on its own
  branch `claude/pkg-NN` cut from the trunk, each bound by every rule of this file and told
  so in its brief; not more than three at once, since each step still passes one at a time
  through the lead's trial and merge; two that touch the same region or the same tiles are
  never run side by side; and the session, not its builder, reports the hash to the lead
  after reading the work itself.

## Speaking with the lead

The lead is `session_01DTAvj6mwzAZMm2fER1Bi3U`. To the lead: a one-shot scheduled message
bound to that session, a minute or two ahead. From the lead: short messages that arrive in
the session; anything long is written on the trunk in `docs/dev/M7-WorkPackages.md` and
pointed to. Keep messages short: they are echoed.

## The rules of every package, which bind the session and every builder it makes

No model or vendor identifier in any file of the repository, the commit attribution
trailer the harness gives being the one exception. Nothing under `docs/agents/consent/`
nor `docs/agents/ConsentBrief.md` is touched. No key in the repository, a save or a log,
and no call to any paid service. Downloads are data, each in its own folder, read and
never run. No test is skipped, disabled, quarantined or weakened. A pin moves only where
the step moved it, old beside new, proven by a toggle or by bisection, with the reason in
the tuning notes. The physics is read, not changed; no ship file is touched. Truths pin
states, counts and bands, not digests. Text a player reads is the world's own: it names no
package, test, engine or director. The owner's saves are never asked for.

## Its first work

1. **Read in:** this file; `docs/dev/ChartBlocks.md` whole; the briefs and as-merged
   records of packages 79c, 79d, 101, 104, 105, 106 (the measurement), 106a, 106b, 111 and
   112 in `docs/dev/M7-WorkPackages.md`, with the paragraphs beside the packages table;
   `tools/audit_chart.py` and `data/charts/audit-known.yaml`; the references' README.
2. **When package 106a is merged** (the lead says so): package 106b (briefed and approved;
   truths 7-550 to 7-559) and package 112, the coarse seas (briefed and approved; truths
   7-570 to 7-579; measured first).
3. **When package 111 is closed:** what its known list leaves, gathered for the owner
   through the lead.

The builders now mid-step (105, 106a, 111) finish under the lead; the session takes their
ground as each closes.

## The lead's rulings to the session

**2026-11-13, on its first report (a47d63ff).** (1) Package 106b's `morocco-north` abuts
the Strait's bound at 35.5 N, not its tile row's edge: brief it so. (2) The audit's seas:
package 111's builder is told to make a region with no sea named a failure and not a
Mediterranean one (its step 2a); package 112's `seas.yaml` then becomes the one source,
which the audit reads. Package 106a's regions name their sea at its merge. (3) The 40 MB
rule is read in MiB, as you read it; say the unit in the how-to with your first step. (4)
Yes: the water-level question is the audit's four findings of a level. (5) Noted: the
Oriental Navigator comes on the trunk with 106a. **Before package 112's measure:** (a) a
sea owns the open water outside every region's bounds, for the tide, the weather and the
audit's check (a); a group of water nobody owns is retired from the list only where its
sea gives it a tide of its own and not the eleven's; the ten slivers beside a neighbour's
bounds are closed by bounds, in package 111's step 2a, not by a sea. (b) The open
Atlantic's level is 112's to MEASURE and report, not to settle: how the tiles' raise and
the game's level combine today, what the islands' gauges read, and what each choice would
do to the depths; the lead rules on the report. The four older blocks' own levels wait for
package 111's close, by the owner's word. (c) One ordered list of layers for a level is
112's step 1 as briefed: an engine step at its own hash, narrow, proven cell for cell over
every existing tile. (d) Step 4's words are yours to build as a step of its own, last,
after you have sent me the lines proposed and where each is said; the world's words, no
package or engine named. (e) The list of saves, truths and passages that sail
`atlantic-east`'s open water is part of your step 0's report (package 106a's notes hold a
first count: check it).

**2026-11-13, the calendar and the world (decision 69; the owner: "the running clock
should not override the state of the world itself ... besides at the start, or in a
scenario intended to run the actual historical course specifically, factors like port data
will need to rely on the world rather than the date").** Ruled on your report of 04:43
UTC, and yours to build as an engine step of its own, on `claude/charts`, at one hash,
truths 7-580 to 7-584: (1) **a port's dated rows seed the port on the scenario's first day
and the port is then the world's.** By default `Ports.tick` applies no row, and
`Ports.stance` reads the port's own holder (`port.nation`), as the prices and the prize
court already do, so that the two agree. (2) **A scenario may say it follows history**
(`follows_history: true`, false where absent; said in the scenario's own description and
on the harbour's page in the world's words): then a row is applied **on the day it
begins or ends, as an event of that day,** and not on every day, so that what play has
changed lasts until the next event of the record. (3) The regimes' blockade stations
(`business.py`, the reader by the running day) take the same key by my leave, in this
step, changed in that one reader alone; say what it moves. (4) **Left on the calendar:** a
light's years, the private signal tables' months, the market's season, a hull's wear. (5)
The fault you found is mended by (1): a director's `closed_to` on a port with dated rows
is no longer overwritten at the day's turn; pin it. (6) The test
`test_dated_rows_turn_with_the_worlds_day` is superseded by design, old beside new: held without the key, turning with
it; truth 7-530 and package 105's truths by the start's day stand. (7) **Not in this
step:** a writer for a port's holder or a war in play (the director's forms, the state's
own motions) is the review portion's to design (packages 103b and 92); say in the notes
that until then the world's holder and wars change by nothing in play. Tell package 105's
builder nothing: I do. The gate as your brief has it; the browser plans in your slow tier.

**2026-11-13, on your reading of package 105's step 2 and 111's step 2a.** (1) Taken:
111's builder adds `sicily`, `gulf-of-hammamet` and `calabria-north` to the audit's seas
when it re-merges after 105. (2) Taken: package 106a re-runs its proof that Madeira's
tide is unmoved once 111's step 2a (Madeira's south bound at 31.60001 N) is on the trunk,
or moves its second layer's north bound; I have told its builder. (3) **A gauge's judged
level:** I accepted for Sicily, at its measure, a level of M2 + S2 + N2 marked JUDGEMENT,
because the other choice was the eleven's 3.98 m over a sea of decimetres. That stands for
Sicily as an interim answer and is not yet the rule: whether the four older blocks take
the same is settled at package 111's close, with the levels measured first. Say in the
how-to, with your next step, that a level so judged is marked and is replaced by a
published one when read. (4) Agreed: by design.

## The session's standing notes

(The session writes here: where each package stands, the rulings it has made, the owner's
words to it, and what a fresh context must know to go on.)

### 2026-11-13, the first turn: read in (the trunk at 81aa8adc)

**Read, whole:** this brief; `docs/dev/ChartBlocks.md`; in `docs/dev/M7-WorkPackages.md` the
packages table's rows and the paragraphs beside it, the briefs of 79c, 79d, 101, 104, 105,
106 (the measurement), 106a, 106b, 111 and 112, and the as-merged records of 79c, 79d, 101,
104, 105 step 1 and 111 step 1 with the lead's rulings for its step 2; `tools/audit_chart.py`
(its checks' constants and the (a) and (c) checks line by line); `data/charts/audit-known.yaml`;
the references' README. Looked at, read-only: the manifest, the gauges, the weather boxes,
the streams' `book_limits`, and the branches `claude/pkg-105` (01e11b0c) and
`claude/pkg-106a` (c9ec8409), which finish under the lead.

**The chart as it stands on the trunk.** One chart, `atlantic-east`, of seventeen regions
in the voyage's order, with one coarse layer under them, the corridor (level 1, 30″, 32 to
51 N and 32 to 1 W, 48 tiles, 9.7 MB), and a tide region with no tiles (`solent`). Levels 0
and the rest of 1 are not committed. Tiles of the regions: 308.6 MB of level 2 and 3 (the
manifest's bytes).

| region | bounds (N, E) | L2 | L3 | MB | neighbours (seam) |
|---|---|---|---|---|---|
| channel-west | 48 to 51, −7 to −3 | 80 | 73 | 17.4 | channel-mid at 3 W; biscay-north at 48 N |
| channel-mid | 48.5 to 51, −3 to −1 | 35 | 44 | 9.0 | channel-west; channel-east at 1 W; solent within |
| channel-east | 49 to 51.5, −1 to 2.5 | 57 | 73 | 13.1 | channel-mid |
| biscay-north | 45.9 to 48, −5 to −0.9 | 55 | 37 | 11.6 | channel-west; biscay-south at 45.9 N |
| biscay-south | 42 to 45.9, −9.33 to −0.9 | 129 | 30 | 19.2 | biscay-north; portugal at 42 N |
| portugal | 36.4 to 42, −10 to −6 | 68 | 48 | 17.4 | biscay-south; strait at 36.4 N |
| madeira | 32 to 33.5, −17.5 to −16 | 25 | 5 | 3.3 | none (canaries' salvages to the south, on 106a) |
| azores | 36.5 to 40, −31.5 to −24.5 | 153 | 7 | 40.3 | none |
| strait | 35.5 to 36.4, −6.5 to −5 | 12 | 14 | 3.8 | portugal; mediterranean-west at 5 W; 106b's morocco-north to come |
| mediterranean-west | 35 to 40.5, −5 to 0.05 | 165 | 30 | 26.2 | strait; balearics at 0.05 E |
| balearics | 35 to 40.56, 0.05 to 4.5 | 154 | 24 | 30.3 | med-west; catalan-coast and gulf at 40.56 N; sardinian-sea at 4.5 E |
| catalan-coast | 40.56 to 41.9, 0.3 to 3 | 24 | 46 | 6.0 | balearics; gulf-of-lion at 3 E |
| gulf-of-lion | 40.56 to 44.5, 3 to 7.73 | 120 | 32 | 27.8 | catalan; ligurian at 7.73/7.74 E; sardinian-sea |
| ligurian-sea | 41 to 44.5, 7.74 to 11 | 72 | 32 | 20.0 | gulf; tyrrhenian (bounds overlap 41 to 42.5 N, 8 to 11 E) |
| tyrrhenian | 38.5 to 42.5, 8 to 15.5 | 158 | 26 | 37.2 | ligurian; sardinian-sea at 8 E; tunis-coast at 38.5 N |
| sardinian-sea | 36.29334 to 40.56, 4.5 to 8 | 75 | 36 | 17.4 | balearics; gulf; tyrrhenian; tunis-coast |
| tunis-coast | 36.29334 to 38.5, 8 to 11.1466 | 35 | 38 | 8.5 | sardinian-sea; tyrrhenian; 105's sicily at 11.1466 E |

On the branches, not yet merged: `sicily` (35.01334 to 38.5 N, 11.1466 to 16.69332 E, 109
and 76 tiles, 28.9 MB, two tide regions `gulf-of-hammamet` and `calabria-north`), and
`canaries` (27.33334 to 29.46666 N, −18.29332 to −13.17334, 60 and 15 tiles, 14.2 MB) with
`salvages` (one tile, 0.4 MB) and a second coarse layer `atlantic-south` (25.2 to 31.9 N,
−22.13 to −9.34, 6 tiles, 1.2 MB) read through the chart's new `corridors_beside` and
`Tile.filled_from` (an engine change in `chart.py`).

**The gauges** (`data/tides/constituents.yaml`, reach 400 miles, inverse square): 87. The
eleven of the Channel and Brittany with no `block:`, their levels read; the blocks' own:
biscay-north 9 (Aix also biscay-south's), biscay-south 11 (the seven Spanish without a
level), portugal 5 (Cadiz also the Strait's, no level), madeira 1 and azores 4 (no level),
strait 4 (no level), channel-east 6 (Newhaven no level), mediterranean-west 4, balearics 5
(Mahón also sardinian-sea's and tunis-coast's), gulf-of-lion 10, ligurian-sea 6 (three no
level), tyrrhenian 8 (no level; Carloforte and Cagliari also serve the gaugeless blocks;
Ortona across the Apennines, said so in the notes), catalan-coast 1, solent 2 (Portsmouth
also channel-east's). **The boxes** (`climatology.yaml`, all provisional): channel, biscay,
portugal, madeira, azores, mediterranean-west, gulf-of-lion (to 11 E), tyrrhenian,
catalan-coast, sardinian-sea, tunis-coast; nothing south of 30 N on the trunk. **The streams:**
77 areas, 13 boxes of `book_limits` (Madeira's not among them).

**The audit's known list: 174 findings.** By kind: water nobody owns 52 (42 the tiles'
reach into open water, the lead's list; 10 slivers beside a neighbour, packages 79d 6, 32,
39d, 39f and 79c 1 each) and the one overlap (79d); the coasts' misses 3 (39a 1, 79d 2); the
tide's level 4 (39e Madeira and the Azores, 39f the Strait, 79d the Tyrrhenian); the weather
8 (no box 3 and split 5, the lead's list); the streams 6 (39e 4, 79c 1, the lead's list 1);
the ports 75 (ways in 24 and out 24, the moorings and a road dry 14, depths 9, open 2,
shores afloat 2: packages 32 to 79d, 79d's the most); the marks 25 (afloat 20, ashore 5:
79d 12, 32 4, the rest one or two). By owner: the lead's list 51, 79d 41, 39a 16, 79c 13,
39c and 39d 9 each, 79b 7, 35 and 39e 6 each, 32 and 39b 5 each, 39f and 35b 3 each. Step
2a and 2b of package 111 are the lead's builder's, by the lead's rulings of today.

**Where each package stands (as the trunk records it):** 105 step 1 merged, steps 2 and 3
on `claude/pkg-105`; 106a built on `claude/pkg-106a`, not merged; 111 step 1 merged, step 2
to come; 106b and 112 approved, briefed, and wait for the lead's word at 106a's merge; 107
not yet, by the owner; no block beyond 105, 106a and 106b without his word.

**Seen in the reading, for the lead (none mended; nothing of this session's built):**

1. **106b's north bound.** Its brief has `morocco-north` from "strait's south edge (35.44
   N)", but `strait`'s bounds end at 35.5 N; 35.44 N is its tiles' row edge. The how-to
   abuts bounds on bounds: at 35.44 the strip to 35.5 stays water nobody owns
   (`a-unowned:strait:south`, `south-west`); at 35.5 the new region owns it, the row's
   tiles staying the Strait's by the seam rule. I would brief 35.5.
2. **The audit's seas are a table in the tool.** `SEAS` in `tools/audit_chart.py` names ten
   Atlantic regions and calls every other "mediterranean": `canaries`, `salvages` and 106b's
   two would be judged by the Mediterranean's level ceiling (1 m) and called another sea's
   tide by their own gauges. 106a was cut before 111 and has not merged it; at its merge
   the ratchet meets it with that table. Package 112's `seas.yaml` is the natural one
   source for it.
3. **"The 40 MB rule"** is not given a unit: the Azores stand at 40.3 MB by the manifest's
   bytes (38.4 MiB). I read it as 40 MiB unless the lead says otherwise.
4. **"The water-level question"** (this brief, "what is settled") I read as the audit's four
   `c-level` findings: the eleven's level over the Tyrrhenian, the Strait, Madeira and the
   Azores.
5. `features/madeira.yaml` cites the *Oriental Navigator* of 1801, which is not on the trunk
   under `docs/references/` (106a files it with Purdy's Atlantic memoir of 1825 and Glas).

**What I would want settled before package 112's measure:**

- **What a sea owns, for the audit.** Do the seas of `seas.yaml` own the open water the
  regions' tiles reach into, so that the 42 `a-unowned` groups of the lead's list leave
  the list when a sea's tide and weather answer there, or does (a) stay a check of the
  regions' bounds alone?
- **The open Atlantic's tide.** The seas' tide is "the blend of the gauges its sea names";
  no gauge of the open ocean has its level read (Funchal, the Azores, the Strait), so an
  Atlantic sea's level is the eleven's unless a level is read: is that the four levels'
  research (to wait for 111's close) or 112's to measure?
- **One form for the layers.** 106a adds `corridors_beside` beside `corridor`; 112 is to
  generalise it. I would make the chart's form one ordered list of layers a level, with the
  manifest written so that the existing corridor's tiles and entry stay byte for byte; that
  is an engine step in `chart.py`, reported as one.
- **The chart's words in step 4** (the general chart not to be trusted inshore) are read by
  the master and the lookout, whose files are not this session's ground: who builds them.
- **The kept saves and truths outside every block** that sail `atlantic-east`'s open water
  (the recorded passages sail channel-west's chart, which has no coarse layer): the list
  wanted before the measure, so that the tide and weather moved there by design are named.
- **Level 0's extent** (the whole world, or 70 S to 75 N and 100 W to 40 E) is the lead's
  choice from the measure, as the brief says; I would measure both.

**The owner's word of 2026-11-13, through the lead** (the section "Workflows, mechanism and
reports" above, from the trunk at 2ce738bb, and the builder sessions' paragraph at 0f7a74b1):
workflows of several agents only for sourced research and port passes; no new mechanism
beyond a brief without the lead's approval; concise reports; builder sessions of my own for
approved packages only, three at most, never two on one region, the hash reported by me.
The lead's rulings on my first report are in their own section above; the single list of
layers is now 112's step 1 as briefed (ruling c).

### The builders' briefs, prepared (not launched; each at the lead's word at 106a's merge)

Each builder gets the text below with the package's own brief in
`docs/dev/M7-WorkPackages.md` named as its scope, and this file named for the rules
("What is settled", "How a step reaches the trunk", "Workflows, mechanism and reports",
"The rules of every package"). Each reports to this session, not to the lead.

**106b, Morocco's Atlantic coast** (`claude/pkg-106b`, cut from the trunk after 106a's merge).
Read whole first: this file's settled rules, `docs/dev/ChartBlocks.md` with the sections of
101, 104, 105 and 106a, and "## Package 106b" in the work packages. Changed by the lead's
rulings: `morocco-north`'s north bound is the Strait's bound, **35.5 N**, not its tiles' row
edge; `morocco-south`'s west bound is `canaries`' east bound (−13.17334) where they meet;
each region **names its sea** for the audit (by the form 111's step 2a gives; a region with
no sea is a failure); the 40 MB rule is MiB. **Step 0, a measurement to this session before
anything is committed under `data/charts/`:** the sources on file (the Oriental Navigator,
Purdy's Atlantic memoir, Glas, as 106a filed them; Jackson 1809 if it can be fetched), the
seams against `strait`, `canaries` and the coarse layers, the tiles and MiB for one column
seaward and for two, which source grid reaches, the gauges by the how-to's rule for a block
with none, and the audit's findings the two regions would add. Then the build by the brief;
dated port rows in 105's form; decision 68 as the brief says; truths 7-550 to 7-559; the
audit clean or each finding listed with its owner (package 106b).

**112, the coarse seas** (`claude/pkg-112`, cut from the trunk after 106a's merge). Read
whole first: this file's settled rules and the lead's rulings (a) to (e), `docs/dev/ChartBlocks.md`
with 39e's and 106a's sections, 106a's `corridors_beside` and `Tile.filled_from` in
`freesail/world/chart.py`, and "## Package 112". **Step 0, the measurement to this session,
nothing committed:** the brief's (a) to (d); the open Atlantic's level measured, not settled
(how the tiles' raise and the game's level combine today, what the islands' gauges read,
what each choice does to the depths); the list of saves, truths, passages and scenarios that
read `atlantic-east`'s open water, checking 106a's first count (five kept saves all
`channel-west`; twelve `atlantic-east` scenarios, each starting inside a region's bounds).
**Step 1, its own hash, an engine step:** one ordered list of layers a level, generalising
`corridor` and `corridors_beside`, proven cell for cell over every existing tile; the
manifest's existing entries byte for byte. Then the layers the lead chooses, `seas.yaml` as
the one source of seas the audit reads (a sea owns open water outside every region; a group
of water nobody owns leaves the list only where its sea's tide is its own and not the
eleven's), and the plan for the Atlantic on paper. **Step 4 (the chart's words inshore on a
coarse layer) is not the builder's:** this session builds it last, after the lead has the
lines proposed. Truths 7-570 to 7-579.

**Running them:** 106b and 112 touch different files but both touch the manifest,
`build_charts.py`, the climatology and the tides; they are not on the same region or tiles,
so they may run side by side, the second to merge taking the first's manifest by
`--skip-fetch` rebuild as the how-to says.

### 2026-11-13, 08:35: where things stand

- **The calendar and the world** (decision 69): built at 65a7df86, reported at 3a30a85c,
  merged as 4e079c31. Truths 7-580 to 7-584. Until 103b and 92 design one, nothing in play
  writes a port's holder or a war; the director's port order closes, opens and prices.
- **Read for the lead:** 105's step 2 (562ba67) and 111's step 2a (184745d9); the four
  points taken (the lead's rulings above). **Owed with my next step:** the how-to to say
  that a gauge's level judged as M2 + S2 + N2 is marked JUDGEMENT and replaced by a
  published one when read (Sicily's interim answer, not yet the rule).
- **Waiting:** 106b and 112 at the lead's word on 106a's merge; the builders' briefs
  above, to be brought up to date then (106a's Madeira proof, 111's seas table and the
  calendar's `follows_history` for 106b's dated ports).

### 2026-11-13, 15:20: the lead's word (trunk 18ea2816, merged here)

- **Package 105 closed** (step 3 merged as 801b80e7): `sicily`, its 24 ports, the tide
  regions `gulf-of-hammamet` and `calabria-north`, `the-faro` scenario and the six gauges'
  interim judged levels are now this session's ground. The chart is 18 regions and four tide
  regions (`solent`, `gulf-of-hammamet`, `calabria-north`, `asinara-west`).
- **111 step 2a merged** (dac8ddd7): every region's sea named in the audit's `SEAS`, an
  unnamed one a finding. Step 2b building (tracks for 22 of the 25 ports; Genoa, Cartagena
  and Oran stay listed for the cold review).
- **106a** at its last measures: re-runs Madeira's tide proof after 2a; adds two findings
  (the Salvages' weather split at 30 N; Point Handia's grid point) and moves truth 7-564's
  count; the lead may ask my reading at its report. **At its merge 106b and 112 are mine
  to begin**, as the owner ruled.
- **109 step 5** (ruled): traders steer round land by the sea route, and goal squares with
  a mark on land are laid at sea; how a vessel steers, not what the land guard judges.
- **The builders' briefs, brought up to date:** 106b's two regions name their sea
  (`atlantic`) in `SEAS` or the audit fails them; its dated ports seed the game and move
  only under `follows_history` (decision 69), so its truths load each port on its start
  day. 112 reads 111's `SEAS` as the table its `seas.yaml` replaces, with `sicily` and the
  four tide regions in it.

### 2026-11-13, 17:37: 106a's final read for the lead (f2799ec)

Nothing blocking. **For 106b's brief when it launches:** a weather box over Morocco's water
east of 9 W from 30 to 36 N (in no box today); a `book_limits` box east of 9.34 W; its sea
in `SEAS` either `canaries` or with `SEAS_THAT_MEET`, since the canaries' gauges serve its
gaugeless south. **For 112:** the island seas (`madeira`, `azores`, `canaries`, `salvages`)
to be one sea or met in `seas.yaml`. Left for the lead: the seven Canaries port heads' stale
words about rows waiting for 105's step 1; decision 68's words are comments only (a served
field is package 110's to design).
