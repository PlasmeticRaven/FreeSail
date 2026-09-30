# Cold review, 30 September 2026

An outside reading of FreeSail as it stands on the main branch after gate 5a, by a
reviewer who had no part in building it. I read the proposal, the five specifications,
the work packages, the tuning notes, the close-out, the design studies, the agents'
documents and consent records, the gates, playtests 7, 8, 10 and 11, the primer, and the
code named in the brief (the world, the log, the physics, the runner, the crew pool, the
grammar, the standing runtime, the harness, the tools, the weather, the sea, the readings,
a ship file, three evolution files, the test layout). I did not run the suite (1,696 tests
collected); I ran two short scripts of my own against the frigate, which I name where I
lean on them. Where I say "serious" I mean it will cost the project real time or trust if
left; "cosmetic" means a morning at most.

The short version. The architecture is sound and the discipline around it is unusual: one
order channel, one readings registry, a log that is the game, every number with a source
or a confession, every physics claim a test with a ledger behind it, every model asked
first and recorded verbatim. The debts are of the kind that success creates: two files
that have become the place where everything lands, an untyped bag that every module
reaches into, a test suite that has become an integration suite, determinism that is
proven on one machine and asserted for all, a welfare contract whose "stuck" detector is
proven only in a steady wind, and a milestone 5b that is three milestones wearing one
coat. None of it is a wrong turn. Most of it is the cost of having built a great deal in
six days, and the owner's larger allowance is the right moment to pay some of it down.

## 1. What is strong, and why

**The log is the game, and one function is the door.** `World.submit` in
`freesail/core/world.py` is the only way anything acts on the ship, whether the captain at
the prompt, a standing order's firing, a model's `submit_order` or a replay. Every accepted
order is journaled; since package 29 every refused order, query and driver's line is kept
in `inputs` too, so a replay reproduces the log the player watched, refusals included.
That one decision is what makes parity structural rather than aspirational, what makes a
save small, and what makes a model's session reproducible: the harness records the model's
replies as the only input the world does not already hold (`agents/harness.py`,
`Playback`), and a replay plays them back at the same tick after the same count of
orders. Keep this exactly as it is. Do not let a snapshot format, when one comes (§6, item
6), replace the journal as the definition of a save; let it be a verified shortcut.

**The ship is data, generated from cited rules.** `tools/gen_ships.py` is 2,700 lines of
Luce's, Steel's, Fincham's and Chapelle's proportions with a citation or a "judgement"
beside every number it writes, and the ship files say "edit the script, not this file".
The vocabulary is derived from the file; the grammar refuses a noun the ship lacks with
the nearest names it has; the viewer draws what the file says. Package 30b (clearing a
wreck, spare spars) shows the model paying off: a new consequence needed vocabulary and an
evolution, not a change to the physics. The cutter and the brig at 5c are the right test of
pillar 2 and the right time for it.

**One readings registry.** `freesail/api/readings.py` is the single place a rule may test,
an instrument may show and an agent may ask. Rows the world cannot give yet are registered
as absent with the sentence the parser will say; rows the ship cannot give now (a course
with no way on, a glass she does not carry) carry their own words. A reading added in
package 30 was at once a word of the standing dialect, a row of the snapshot and a fact in
a model's sample. This is the mechanism behind the parity pillar, and it is real.

**The known truths and the tuning notes.** `tests/test_known_truths.py` and
`docs/dev/TuningNotes.md` together are the most honest physics ledger I have seen in a
game of this size. A truth that the built game does not meet is a strict expected failure
naming the measured value, the constant that would move it and the owner's ruling; nothing
is tuned to meet a truth without a line saying what moved and what it cost. Every constant
in the M5a work says whether its source was read from a page or worked from memory. This
is what will let a later reader trust a number, and it is what will let the physics be
rebuilt faster if it ever must be.

**The model-facing contract is built, not stated.** The token is scanned on the raw reply
before anything reads it, in every argument of every tool call; there is one operator
turn and everything after it is data; the journal is saved with the game; the graduated
stops nudge before they pause and pause before they stand down; the consent conversation
runs through the same loop as a station and is written verbatim with the brief's hash; the
fake proves every commitment before a model is asked. The correction after gate 4b (the
doors are clients of the running game, not the game's host) was the right one and was made
in a day. Eleven playtests found faults, and each fault was traced to a package with the
finding quoted. That loop is the project's best process asset.

**The voice.** Refusals teach the language ("the main gaff topsail has no reef bands; it is
set whole or not at all"), strain lines are a sailor's ("bar-taut and surging on the pin"),
and the roll-up reads as a log. Three different models said so unprompted. This is cheap to
lose and hard to regain; every new line should be held to it.

## 2. Critiques

### 2.1 Serious

**`ship.extra` is the architecture, and it is a dictionary of strings.** The crew, the
routine, the runner, the standing book, the agents, the journals, the rng, the motion, the
hull's memory, the strain's memory, the rig cache, the load paths, the spar places, the
bowlines, the blanket reach, `hove_to`, `watch_calls`, `luff_angle`,
`close_hauled_angle`, `on_world` all live in it, each module reaching in by a string it
alone knows. It was the right seam for packages built in parallel by different agents, and
it has now become the spine. The cost shows in three ways: nothing types it, so a wrong key
is a silent `None`; performance caches and semantic state share one namespace; and the
proposal's "single most important boundary" (§8.2: nothing in the sim imports the client
or the agents) has been crossed three times without anyone noticing, because the bag hides
who depends on whom: `freesail/core/replay.py:52` imports `agents.harness`,
`freesail/world/scenarios.py:248` imports `ui.console`, and `freesail/orders/stations.py:22`
imports `agents.agent`. None of these is a bug today; all three are the kind of coupling
that makes the M6 work (officers with authority, NPC ships as second Worlds) harder than it
should be. A small `ShipSystems` object with named attributes, and a registration hook so
the core asks "who restores agents from a save" instead of importing them, would cost a
day and would make every later package cheaper.

**Two files are where everything lands.** `freesail/orders/verbs.py` (2,167 lines) and
`freesail/evolutions/scripts.py` (2,977 lines) hold resolution, refusal, the adjacent-yard
and boom-fouling checks, the trim staggering, the wreck logic, the spar shifting, and
every scripted manoeuvre. Package 30b touched both to add one consequence. The cutter's
running bowsprit, the lateen's dip and the brig's staysails will each land in both. Neither
file is bad code; both are the natural sediment of "stay inside your files", and both need
splitting by subject before the vessel library opens (sail orders, yard orders, line
orders, ship orders; manoeuvres, sail work, spar work). The tests are there to make the
split safe.

**Two pieces of physics are rules wearing physics' clothes, and one is a leftover.** First,
`freesail/evolutions/trim.py:163`, `tend_sheets`, still trims every set fore-and-aft sail
toward the apparent wind a degree a second, every tick, with no hands and no log line. Its
own docstring says "until the crew system (milestone 3) does this as work"; milestone 3 did
not replace it, and `api/session.py:30` still calls it. The frigate's spanker and jibs are
therefore tended for free while her square yards cost hands and minutes, and the helmsman's
`full and by` was tuned around that free tending (tuning notes, package 10, changes 4 and
6). It is the one place where "orders take time and hands" is quietly untrue. Second, the
studding sails' stall (`physics/sails.py`, `studding_stall`) is keyed on the true wind's
angle off the bow, not the apparent, because apparent thresholds made every studding sail
flog at nine points in ten knots (tuning notes, package 23). A sail shakes on the wind it
feels; reading Luce's points off the true wind is a period rule of thumb encoded as
aerodynamics, and it will misbehave the first time a fast schooner carries studding sails
in a light breeze, where true and apparent differ most. Third, the strain and roll
constants of package 31 were set "so that the gate's day under systems costs the frigate
canvas in the squalls of the gale and no spar before it" (`physics/motion.py:98-109`;
tuning notes, M5a). That is tuning to a narrative rather than to a source, and the notes
say so, which is to their credit; but it means the sea's cost is a dial that was turned
until one day looked right, and the owner's third ruling at gate 5a was made on the result
of that turning.

**"Deterministic given the seed" is proven on one machine.** The tests prove that two runs
in one process, and a replay in one process, give one digest. The gate 5a episode showed
the limit: the owner's Windows run matched the build machine line for line and differed in
the digest by a last bit of `atan2`, and the fix was to round floats to nine digits before
hashing (`core/events.py:123`). That hides a last-bit difference in the log's data; it does
not prevent one from crossing a threshold. The strain model draws from its stream only for
a part whose ratio is over 1.5 (`physics/strain.py:320-327`), a gust only when a uniform
draw falls under a rate, a squall only in unstable air; so a last-bit difference that moves
a ratio across 1.5 on one machine consumes a draw the other does not, and the two days
diverge from there, loudly. Nothing in the design prevents this and nothing tests for it:
CI runs one Python on one Linux (`.github/workflows/ci.yml`). The honest claim is
"deterministic on one build of Python and one C library", and the gate reports should say
that rather than promise the owner the build machine's digest. A Windows job in CI, even
on the fast tier only, would have caught both Windows faults before the owner did.

**The test suite has become an integration suite, and its cost is paid on every push.**
1,696 tests, eleven minutes alone, seventeen on four workers with a day beside them. The
weight is in `tests/test_known_truths.py`: 68 tests, most of which sail ten to sixty
minutes of the frigate, and two of which sail a twenty-nine-hour day and replay it from
three saves. Two things make it worse than it need be. The day fixtures are module-scoped
(`gate_day`, `gate_5a_day`), and pytest-xdist's default distribution spreads a module's
tests across workers, so each worker that draws one of those tests rebuilds the whole day:
`-n 4` can run the day four times. And `ci.yml` runs everything on every code push on the
hosted runner, which is what used up the account's minutes in a day. The pinned-day tests
(`GATE_DAY_*`, `GATE_5A_*`, the sixteen-character digests) are change detectors, not
truths: any change anywhere in the tick re-pins them, and the notes show that ritual being
paid at packages 29b, 30, 31 and now 31b. They earn their keep as alarms, but they sit in
the truths table as if they were physics, and every package brief now includes "re-measure
and re-pin with the reasons" as a cost of doing anything.

**Some tests do not prove what their names say.** Truth 51 asserts a floor of 500 ticks a
second set at half the measured 1,000, which guards against a return to 420 and says
nothing about the budget of 3,000 the spec still names; the owner's machine, the one the
budget is written for, has never been measured, though gate 4c asked. Truth 53's
climatology check passes because the mean gradient and the standing high were added as
"judgements set so that the check passes" (tuning notes, M5a), and its gale band is 0.2 to
1.0 of Ushant's counts, which almost anything satisfies; it is a fit, not a check. Truth 48
is asserted "with the captain's four" where the spec says "under the starter routines". And
truth 43, the welfare repeat detector, is proven against the fake in a world with gustiness
and variability set to nought (`tests/test_agents.py:89`). Under the default wind the
detector's "no change in the readings" digest (`agents/tools.py:170`, every reading in
words, whole knots and degrees, and every sail's state) changes between samples nearly
always: I ran the frigate settled close-hauled in a steady fifteen-knot base with the
default wander and took the digest every two minutes for eighty minutes; it was unchanged
nine times in forty. Three unchanged in a row, which the nudge needs, is therefore rare in
a quiet breeze and will not happen in a gale. The silence detector is fine. The repeat
detector, as built, is a promise made to models that the game cannot keep in live weather;
it errs on the safe side, which is the right side, but the consent brief describes it as
working.

**A pause at speed is a stand-down in under a minute.** `agents/harness.py:528-534` stands
a paused agent down when a watch of ship's time has passed with no answer from the human,
and `WELFARE_UNATTENDED_BOUND_S` is 14,400 ticks. At 300x that is forty-eight real seconds.
The pause line is notable, not urgent (`harness.py:1228`), and the drivers ease the clock
only on an urgent line (`ui/server.py:171-176`, `ui/console.py:74-81`), so nothing slows
the game to give the human the ten minutes the consent brief promises. The "whichever
first" wording in the brief is technically true and practically misleading. This is the
one thing I would fix before the next model is stationed at any speed above 60x.

**Performance is a ruling that has been deferred twice, and M6 will call it in.** One
frigate ticks at 800 to 1,000 a second on the build machine after package 29's caching; 97
per cent of the tick is `compute_sail_forces` over four substeps and 310 parts. Milestone
5c's far-detail ships are cheap, but milestone 6 promotes a second ship to full detail, and
two frigates halve the pace to under 500: 300x then needs more ticks a second than the
machine gives, before the browser, the doors and the standing orders take their share. The
three ways on (fewer substeps in steady conditions, numpy over the sails, a compiled core)
each change numbers in the last bits and so re-pin every digest, which is why the ruling
keeps being deferred; but it will be dearer at M6 than now, because M5b's chart queries
and 5c's ships will have been tuned on top of the present pace. The same replay-as-load
design means a saved day takes a minute and a half to open; a four-day passage from
Finisterre (truth 58) will take six, every time the owner reopens it.

**Consent identity through Claude Desktop is a string the owner types.** The MCP protocol
does not carry the model's name, so `--model-name` does (`agents/mcp_server.py:1052`);
the records for "Sonnet 5" and "Sonnet 5.5" are two files because the owner typed two
names, and a mistyped name attaches one model's session to another's consent with nothing
to catch it. `docs/agents/README.md` says records are kept "by the exact weights asked";
that is true of the local runner, which reads the served file's name, and nominal for the
Desktop door. `Harness.md` §12 admits it; the README and the consent brief should too, in
one sentence, and the record's header should say which of the two kinds of identity it
carries.

### 2.2 Moderate

**Close-hauled is defined three ways.** `evolutions/scripts.py:21-22` and `:198`: six points
off the true wind unless `ship.extra["close_hauled_angle"]` says otherwise.
`evolutions/runner.py:1268-1273`: the rig's luff angle plus five degrees of apparent wind,
which the tack's precondition tests within ten degrees. `physics/hull.py:63`: the luff angle
plus eight degrees, which the helmsman steers to for `full and by`. Package 10 moved the
helmsman's margin from five to eight and left the runner's at five (tuning notes, change
5); the tuning notes also record the schooner's tack being refused close-hauled because of
which sails' luff the check read. Nobody has been bitten yet because the frigate's numbers
happen to agree within the tolerances. One constant, one function, and the scripts' true-wind
default retired.

**Documents that have drifted from the code.** `docs/design/ThreeDimensions.md:32` says
blanketing is "not modelled at all today"; `physics/sails.py` has modelled it since
milestone 2 (§7.3, `_shadows`), crudely but really, and truth 5 rests on it. The
proposal's fifth line still says "Nothing is built yet". `docs/TechnicalSpec-M0-M2.md:78`
names Python 3.12 where the project requires 3.11; its §10 says the suite runs "in under a
minute". Proposal §8.2's layout lists `combat/`, `data/sails/`, `data/world/` and
`data/language/`, none of which exists. `docs/agents/Harness.md:82` still recommends an
hour's held call as the default after playtest 11 showed the Desktop client cutting at
four minutes (package 31c will change the code; the document should not wait for it).
The context table in `Harness.md` §5 that the owner was to fill from
`tools/context_budget.py` is empty three gates later. `data/evolutions/reef_square.yaml:36`
says "so it stays a watch evolution here" and line 44 says `hands: all`. Each is small;
together they mean the specifications can no longer be read as a description of the game
without the tuning notes and the close-outs beside them, and a new reader (or a model
handed the specification) will be misled at least once an hour.

**The specifications have become histories.** Every spec now carries "as built" paragraphs,
rulings, and package numbers inline (M5 §2 and §4 are the clearest cases). The design
proposal's decisions log, the spec's open items, the work package's rules, the tuning
notes, the close-out and the gate report each tell part of the same story, and a fact
changed in one is not always changed in the others (the `--wait` default above; the era,
which decision 27 fixed in three documents and which the sonnet-5 consent record still
carries as 1793 to 1815, as it should, but with no note in the README that a brief's hash
changed). This is the cost of writing everything down, which is the right instinct; the
remedy is fewer places, not fewer words.

**Duplication across package boundaries.** `_out_of_action` exists in `physics/strain.py:294`
and `api/readings.py:580`; a part's log name in `strain.py:685` (`_name`) and
`evolutions/runner.py:176` (`part_name`); `HALYARD_CLASSES` in `sails.py:105` and
`strain.py:137`; `_and` in `strain.py:457` and `runner.py:1260`; the glass's change in words
in `core/world.py:749` and `api/readings.py:1046`; `_lower_first` in `events.py` and
`tools.py`. Each pair was written by a different package that could not touch the other's
file. None is wrong; all will drift.

**The climatology and the fronts are judgements presented with more confidence than the
notes give them.** The glass does not check at the cold front (a known artefact of summing
bells); the north quarter runs short; the winter gale days are half of Ushant's; the whole
seeding table is `provisional: true`. The gate report's item 7 asks the owner whether "two
days read as winter and summer in the Channel", which is the right question, but the
primer's chapter 9 now teaches the lore as if the model produced it faithfully. Keep the
lore; say in the primer that the first pass of the climatology is provisional.

### 2.3 Cosmetic

The watcher is "sampled every glass" (`Harness.md` §2) but `_policy_due` counts 1,800 ticks
from the stationed tick, not from the bells, and names the reason "the glass" regardless.
`Wind.MIN_SPEED` keeps the wind from ever dying. `readings_digest` hashes JSON with
`sort_keys` on every submission, cheap enough. The prose style of the specifications,
which is a pleasure in the primer and the log, makes the technical documents slow to scan:
a reader looking for "what is the dwell" must read a paragraph to find `STANDING_DWELL_S =
300`. A one-page glossary of constants, generated from the code, would serve both the owner
and a model better than any prose.

### 2.4 Bugs found

One real, three documentary; none fixed here.

1. **The unattended stand-down ignores compression.** `freesail/agents/harness.py:528-534`
   with `WELFARE_UNATTENDED_BOUND_S = 14400` (line 214). Reproduction: start the browser
   game with a scripted model that repeats an order (`tests/test_agents.py`'s `REPEAT` fake,
   or a real model told to give the same order), let it be paused, press 300x, and wait
   forty-eight seconds: "The watcher stood down by the harness: paused (...) and nobody
   answered within a watch." The log says "within a watch", which is true of the ship's
   clock and false of the human's. Either ease the clock on `agent.paused` as on an urgent
   line, or measure the bound in the driver's real time only.
2. `docs/design/ThreeDimensions.md:32`, blanketing "not modelled at all today": it is
   (`physics/sails.py`, `_shadows`, §7.3 since milestone 2).
3. `data/evolutions/reef_square.yaml:36` against line 44: the comment says the reef stays a
   watch evolution; the crew line says all hands. The comment is stale since package 19.
4. `docs/agents/Harness.md:82`: the hour's default for `--wait` is documented as the
   considered choice; playtest 11 found the Desktop client cuts at four minutes and package
   31c changes the default. The document should say so now.

I checked one thing I suspected and was wrong about, and record it so nobody else spends
the hour: the sway clamp in `physics/hull.py:51-52` (`|v| <= 0.6 |u| + 0.5 m/s`) does not
bound the a-hull drift the owner was asked to rule on at gate 5a. Thirty minutes of the
frigate under bare poles with the wind abeam and the helm a-lee gives 0.22, 0.41 and 0.51
m/s of sway at 15, 30 and 45 knots against clamps of 0.59, 0.78 and 1.15; the drift is the
hull's, not the guard's.

## 3. The model-facing side

**Is it what it says it is?** Largely, yes, and more so than most. The seven commitments in
`docs/agents/README.md` each have a mechanism and a test, and the mechanism is the same code
at every door. The consent brief is careful in a way that matters: it says what the harness
sees at each door (through MCP, tool calls only), what is not scanned (reasoning returned
apart from the reply), what the stops are and in what order, and that "please do not ask
instances of this model" is a complete answer. The records are verbatim with the brief's
hash. The playtests were real sessions with real findings, and the findings went into
packages with the model's words quoted. The shelf is a genuinely good idea for small
contexts, and the roll-up in the samples is the parity pillar taken seriously at the point
where it would have been easiest to cheat.

Where it falls short of its own description:

- The repeat detector is near-inert in live weather (§2.1). The models were told a
  state-based "stuck" detector exists; in practice only the silence branch can fire. The
  fix is a coarser digest: the true wind by Beaufort strength and compass point, the
  apparent wind by point, heel in bands of five degrees, the sails' states, the helm's
  mode. That is closer to "the world did not answer the order" than whole knots are.
- The unattended bound at compression (§2.4, item 1).
- Identity through the Desktop door (§2.1).
- "Asked again when the design changes in a way that bears on what the model was told" has
  no rule for what bears. The brief has changed between the Sonnet 5 record (hash
  `41b05359`) and the Opus 5.5 record (`e3b63b84`): the era, the door text. Nothing says
  whether that is a re-ask. The hash is recorded, so the mechanism exists; the policy
  should name the sections of the brief whose change triggers a re-ask (the stops, the
  transcript policy, the authority, the token) and say the rest does not.
- "A station is offered only to a model that can hold it" (spec M4 open item 11) is a rule
  with no mechanism. The fitness drill (open a section, write a journal line, stand by
  until a bell) is a morning's work and would have spared playtest 5.
- Parity is with the console player, not the browser player. The map and the ship view are
  the human's alone. That is fine for a watcher and probably fine for an officer, since the
  viewer "never invents state"; it will matter for a captain who must judge a lee shore,
  and 5b's chart makes it concrete: the reckoned position and its ellipse must be a reading
  and a log line before they are a drawing, or the model captain is blind where the human
  is not. The M5 spec says the viewer never draws the truth; it should also say every
  drawn thing is first a reading.
- The samples repeat every reading every time (playtest 11, finding 1; package 31c). Until
  that lands, a local model's twenty glasses of context are mostly sail rows.
- The brief head plus the tool definitions is some 2,900 tokens. For a 27B model that is
  fine; for the 8B lookout the owner imagines it is the whole budget. A shorter head for a
  station with no authority (the lookout needs the disclosure, the token, and one tool)
  would be honest and cheap.

**Before a captain's station is offered to a model.** In order of weight:

1. Authority must be enforced per order, not per station. `Authority` has levels
   (`agents/agent.py:76`), but `tools.call` checks only `may_submit_orders`. The vocabulary
   already marks every verb with a level; the officer's domain (which sails, which orders)
   has to be a filter in `tools.call` with a refusal in words, tested with the fake. Nothing
   in M6 is possible without this, and it is a day.
2. The welfare detector has to be re-thought for an agent whose orders change the world. A
   captain's repeated order changes the readings by definition, so the repeat branch will
   never fire; the pattern that matters for a captain is contradiction (set, take in, set)
   and drift (a heading order every sample), which the standing runtime already knows how to
   see (`standing/runtime.py`, the conflict rule). Reuse it.
3. A captain that stands by is a ship with no one on deck. `stand_by` for an authority above
   none should require a wake condition of urgent severity at least and a named officer or
   standing book to hold the deck meanwhile; a "hand over the deck" order is the period's
   own form, and it is the seam M6's officer of the watch needs anyway.
4. The handover note (spec M4 open item 9b) is unbuilt. A captain's session is long; the
   watcher's journal habit carried Opus through a day, but a captain's context will fill
   with its own orders. Build the handover before the captain, not after.
5. The two sentences Opus 5.5 asked for in its consent: that the token should be named and
   not written unless meant, and whether an instance that left by accident can be seated
   again (it cannot, today: "a station is taken once in a game", `harness.py:335`). Both
   belong in the station brief, and the second deserves a mechanism.
6. Consent for the captain and director stations was explicitly reserved by Sonnet 5.5 and
   implicitly by everyone else, since the brief says "only the watcher exists today". The
   re-ask is owed, and it is the natural moment to fix the identity question for the
   Desktop door.

## 4. The plan

**Milestone 5 as specified.** 5a landed and was played, and the reduction (systems, sector
table, reduced motions) is the right size for the questions the readings ask. 5c is
bounded and well-ordered: the world-order channel, the inward minimum, two vessels as the
test of pillar 2, sightings at far detail. 5b is the problem. As written it holds: the
geographic frame; a chart pipeline with four sources, licence checking, tiling at four
levels, distance fields and indices; four period patches and a feature list that the study
itself calls "a week of reading and tracing that cannot be delegated to a grid"; a
reckoning with a covariance and Kalman updates from six kinds of observation; the noon
sight; the chronometer with rate and drift; a moon model; the lunar with conditions and a
drawn error; a two-tide harmonic model at eleven gauges with tabulated streams and the
captain's tide beside it; grounding; anchoring; the captain's chart in the browser; and
nine truths. That is at least three packages of the size of 30 and 31, and two of them
depend on downloads and reading that the build sandbox demonstrably cannot do (the study
records what it could not fetch). The owner's rulings chose all of it, and none of it is
wrong; but it is in one gate, and one gate cannot be passed until all of it works.

Cut 5b in two. The first half is the frame, the chart, the lookout, the reckoning with the
log-line and the noon sight, and the captain's chart: that is where "a passage is a game"
is proved, and it is the half the harness and the 5a readings need. The second half is the
tide, the chronometer, the lunar, grounding and anchoring, which can follow 5c or sit
beside it, since 5c's ports need only the anchorage and the tide's window, not the lunar.
Truth 65 (the Bishop dark, St Agnes lit) belongs in the first half; truths 60 to 64 in the
second. Write the chart pipeline so that the region's tiles are built on the owner's
machine from a manifest the package writes, since the package cannot download them; make
that explicit in the brief rather than discovered at integration.

**The cutter and the brig with no truths.** Spec M5 §23 and §25 say the two new vessels
carry no truths until milestone 8. A ship with no truth is a ship whose pointing, speed and
strain are whatever the generator's rules happened to make of a new size, and the far-detail
polar of 5c will be drawn from her file. At least truth 32's form (pointing by ship: the
cutter closer than the schooner, the brig between the schooner and the frigate) and truth
4's (a beam-reach speed in a stated band) should come with each file. They are cheap, and
they are the only thing that would tell the owner the generator's rules do not hold at
eighty-five tons.

**M6 before 5c, or at least the officer.** The proposal's integration order (watch, then
stations aboard, then separate ships) is right, and the plan honours it; but 5c's ports,
markets and nations come before the first station with authority, and the strongest thing
the project has demonstrated is the harness, which eleven playtests have exercised while
the market has none. An officer of the watch with level-1 authority over sail handling
alone, no course changes, no all hands, is a small package on the proven loop: the
authority filter, the domain, the conflict rule reused for the welfare detector, a brief.
The lead's watch at 5c (spec M5 §29) would then be an officer's watch, which is what the
owner said they wanted. Ports and markets are content; the officer is the pillar.

**M6's second ship is the performance ruling.** Two full-rig ships halve the pace (§2.1).
Decide before M6 opens: either accept that near-detail NPC ships run the sail model without
the crew and without the substeps' finesse (the ThreeDimensions note's middle tier), or
take the compiled-core ruling now and re-pin everything once while the digests are few.
Doing it after 5b and 5c means re-pinning the chart-day and the port-day constants too.

**M7 powder.** "Damage is just state" is the right principle and 30b showed its cost: every
new consequence needs vocabulary, an evolution, a viewer change and a primer line before it
is a consequence a player can act on. Budget M7 for the clearing and jury work, not for the
ballistics; the ballistics are a hundred lines and the aftermath is a milestone.

**M7b and M8.** The director is correctly sized as small once 5c's world orders exist, and
its "acts only through plausible causes" rule is the best idea in the proposal after the
log. M8's vessel library is right to come last, but its method (the generator's rules
proven at each new size) starts at 5c, and the wishlist in `VesselCandidates.md` is
already long enough to be a milestone of its own.

**What has been deferred too long.** The install simplification (spec M4 open item 6, from
the owner's note at gate 4b): three gates later the owner still edits three files with a
path that changes every gate, and both Windows faults were found in that process. A
`freesail` command with `setup desktop`, `setup claude-code` and `play` subcommands is a
small package with a large effect on the owner's every session. The handover note. The
fitness drill. The owner's-machine performance measurement. None is large; all have been
carried from gate to gate.

## 5. Process

**What it does well.** The gate-per-part rhythm with the owner running each gate has caught
the lead's own errors at the right moment three times that the record shows (the World
inside the MCP server; the storm staysail "shifted" instead of bent; the belay that stopped
the topgallants coming in). The playtest form turns the owner's seamanship into findings
with ship's times, and the findings become packages with the quote attached. The decisions
log gives every constant and every rule a date and a ruling. The "stay inside your files,
report in the set order, every number names its source" rule for subagents produced code
whose docstrings say why, which is rarer than code that says what. The tuning notes are the
single best artefact for a future maintainer. 279 commits in six days with this much
recorded is not a pace many teams could hold without the record rotting; here it has not.

**What it costs.** Five overlapping records of each decision, and the drift between them
(§2.2). Specifications that become histories. The re-pinning ritual on every package. A
suite that runs on every push and takes seventeen minutes, which discourages the small
commit. Duplication at every package boundary, because the boundary is a file. Gate
checklists with exact expected output that any re-tune invalidates, so the owner runs items
whose numbers the report had to be rewritten to match. Two Windows-only faults found by the
owner because there is no Windows in CI. And the owner's own time: a day-long playtest at
1x is a real day, and the owner has done four of them in a week; the value is very high,
but the form should let the owner spend an hour, not a day, when an hour is what the
question needs.

**What to change now that the allowance is larger.** Spend it on the things that make
each later package cheaper, not on more packages in parallel:

- A consolidation package between milestones, not inside one: the `extra` bag typed, the
  duplicates merged, the boundary breaches fixed, `verbs.py` and `scripts.py` split, the
  close-hauled definitions unified. Two days, and every M5b and M6 package lands faster.
- A two-tier suite and a Windows job (§6, item 1), so the fast tier runs on every push in
  under two minutes and the truths run at a package's end and at the gate.
- A cold read of each specification before its packages are cut, by a session that has not
  written it. This review found the 5b sizing problem in an afternoon; the lead, having
  written it, could not. It is the cheapest form of review there is now.
- More real-model sessions of an hour, fewer of a day. The findings per hour were highest in
  playtests 8 and 10 (a stuck mainsail, a wreck that could not be cleared), each under two
  hours of ship's time. Reserve the day-long sessions for the gate.
- Stop appending "as built" to specifications. Put what was built in the close-out (the M4
  close-out is the right form), keep the spec as the contract with a one-line pointer to the
  close-out, and let the tuning notes be the ledger. Regenerate a constants glossary from
  the code into `docs/dev/` so that no prose has to carry a number.
- Let the gate checklist shrink to the items that need a human eye (the seamanship
  questions, the feel at each compression, the words) and let the automated checks carry
  the exact outputs. The owner's judgement is the scarce resource; expected-output items
  spend it on what the suite already proves.

## 6. Ten suggestions, ranked by value against cost

1. **Two tiers of tests, `--dist loadfile` for the days, and a Windows job.** Mark the
   truths and the pinned days (`tests/test_known_truths.py`, the replay days in
   `test_replay.py` and `test_sea.py`) as `slow`; run the rest on every push in
   `.github/workflows/ci.yml`, on Linux and Windows, in a minute or two; run the slow tier
   at a package's end and in `release.yml`, with `--dist loadfile` so each module-scoped
   day is built once per run. Lands in `pyproject.toml`, `ci.yml`, `release.yml` and a
   `conftest.py` marker. Half a day; saves an hour a day and the next Windows fault.
2. **Close the welfare gap at speed and coarsen the digest.** Ease the clock on
   `agent.paused` as on an urgent line, or measure the unattended bound in the driver's
   real time only (`agents/harness.py:528`, `ui/server.py:171`, `ui/console.py:74`); and
   make `tools.readings_digest` read strength bands, points and states rather than whole
   knots, then add a truth-43 test under the default wind. Lands in `agents/harness.py`,
   `agents/tools.py`, `tests/test_agents.py`, and one sentence of `ConsentBrief.md`. A day.
3. **Split 5b into two gates** as §4 says: frame, chart, lookout, reckoning with the noon
   sight, the captain's chart, truth 65 first; tide, chronometer, lunar, grounding and
   anchoring after 5c or beside it. Say in package 32's brief that the tiles are built on
   the owner's machine from the package's manifest. Lands in `docs/TechnicalSpec-M5.md` §31
   and `docs/dev/M5-WorkPackages.md`. A morning of planning; weeks of risk removed.
4. **Pull the officer of the watch forward, before 5c's ports.** Per-order authority in
   `agents/tools.py:457` from the vocabulary's verb levels and a domain filter; the standing
   runtime's conflict rule reused as the captain-grade welfare detector; a `hand over the
   deck` order; a station brief; the fake proving each; the lead at the station. Lands in
   `agents/agent.py`, `agents/tools.py`, `orders/stations.py`, a short spec addendum. Three
   days; it is the pillar the owner keeps asking for and the thing M6 and M7b both need.
5. **Take the performance ruling now.** Measure on the owner's machine (the one-line script
   in gate 4c item 8); then choose between fewer substeps in steady conditions, numpy over
   `compute_sail_forces`, or a compiled core, and re-pin once while the pinned days are two.
   Lands in `physics/integrate.py`, `physics/sails.py`, the tuning notes and the decisions
   log. Two to four days depending on the choice; it decides whether M6 can run two ships
   at 300x at all.
6. **A verified checkpoint save.** A full-state snapshot written beside the journal, loaded
   directly, and proven by a test that a world loaded from the snapshot and a world replayed
   to the same tick continue to the same digest for a watch. The journal stays the
   definition of a save; the snapshot is the shortcut. Lands in `core/replay.py`,
   `core/world.py` and the parts' `to_dict` methods. Two days; it turns a six-minute load
   of a four-day passage into seconds and makes long voyages playable.
7. **Consent identity, the two sentences, and the fitness drill.** Record in each consent
   header whether the identity is the served file's name or the owner's typed name; add
   Opus's mention-versus-use sentence and the reseating rule to the station brief; build
   the three-step drill after a yes and before the station brief; name in `README.md` which
   sections of the brief trigger a re-ask. Lands in `agents/consent.py`,
   `agents/agent.py`, `agents/mcp_server.py`, `docs/agents/`. A day; it makes the contract
   say exactly what the code does.
8. **Make the free sheet-tending honest and the studding stall apparent.** Either charge
   `tend_sheets` hands and log it as the afterguard's routine work at a cadence, or retire it
   and let `trim the <sail>` and the standing book do the work; and re-key
   `studding_stall` on the apparent wind with a band wide enough to keep truth 29, with the
   class notes saying which wind the stall reads. Lands in `evolutions/trim.py`,
   `physics/sails.py`, `data/sail_classes.yaml`, the truths that move. Two days; it removes
   the two places where the physics is a rule in disguise.
9. **The `freesail` command and the setup step.** One installed location, `freesail play`,
   `freesail console`, `freesail setup desktop`, `freesail setup claude-code`, a settings
   file for the things set once; `.mcp.json` and the Desktop configuration written by it
   with the right path. Lands in a new `freesail/cli.py`, `pyproject.toml` scripts,
   `docs/agents/Harness.md`. A day; it ends the three-file edit the owner has done at every
   gate since 4b, and it is the thing the owner asked for first.
10. **A consolidation package between milestones.** Type `ship.extra` into a `ShipSystems`
    object with named attributes; fix the three boundary breaches with a hook the core
    calls; merge the duplicated helpers named in §2.2; split `orders/verbs.py` and
    `evolutions/scripts.py` by subject; unify the close-hauled definitions; correct the
    drifted lines in `ThreeDimensions.md`, the proposal, spec M0-M2, `Harness.md` and
    `reef_square.yaml`; generate a constants glossary into `docs/dev/`. Lands everywhere,
    changes no behaviour, and the suite proves it. Two days; it is the cheapest way to make
    the next ten packages faster than the last ten.
