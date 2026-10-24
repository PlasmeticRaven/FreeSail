# Milestone 7 work packages

The packages of `docs/TechnicalSpec-M7.md` (§31), briefed in turn for the owner's approval
and launched on his word. The head rules of `M7b-WorkPackages.md` hold (each item an intent
with the lead's reading of a way, the intent binding; the budget the owner's; nothing under
`docs/agents/consent/` or in `docs/agents/ConsentBrief.md` touched but by the package the
specification names; no model identifier in any file of the repository; a world order never
shown as sent; the recorded passages' pins re-measured only where a change moves them, with
the old figure beside the new and the reason in the tuning notes; never a test skipped,
disabled or quarantined; a section in the tuning notes and a report to the lead; the lead
plays each merged package briefly and files the notes), and this milestone adds its own
(spec M7's rules 1 to 7: damage is just state; a gun is served by the bill; recognition
before fire; rules first, models welcome; the far ships fight as the near do, coarsely;
realism, not pacing; nothing pre-defines a battle's timing).

**How the packages are run (the owner, 2026-10-23).** Milestone 7b is frozen open beside
this milestone (decision 51); its remaining work is wrapped up alongside. **The Fable
packages run one at a time**, so that the owner can meter the week's usage, and each is
**generously scoped and encouraged**: the brief binds the intent and names the ground, and
the builder is free to design and build to the intent as it judges best, taking an item
another way with its reason, growing a part where the work shows it should, and saying
plainly what it left and why; a Fable package is trusted with the design, not fenced to a
list. The Opus packages that build out behind a Fable baseline run as a wave when their
baseline is in, as **sibling cloud sessions** rather than subagents of the lead's machine
(each in its own container, so the suites do not share one machine's load; each pushing its
own branch named for its package, `claude/pkg-<n>`, with the owner's permission given at
that wave; the lead fetching, reviewing and merging as now, and running one whole suite on
the merged tree). The lead's own work (the six-on-six measure, the gate document, the
merges, the records, the short plays) is no package. The usage may run to the week's limit
on these packages; that is the owner's choice.

## Waves

| # | Who | Package | Status |
|---|---|---|---|
| 70 | Fable | The combat core: the quarter bill and work in action, guns as parts, the gunnery's cycle, the hit model with heel, roll and the sea, damage as state, morale and the strike, the fighting book; the first armament and truths; the figures' sources (spec §7 to §10, §8a) | **merged 2026-10-24** (`80f64f7`); the record below |
| 71 | Fable | Signals and the voice between ships: colours, the private signal, the hail, the lights and the bell, the signal hoisted and read; the books' shape for any nation and the first books of Britain and France (spec §1 to §6) | **merged 2026-10-24** (`142b739`); the record below |
| 72 | Fable | The naval system: the squadron as a genuine set, the formations and station keeping, the squadron's book, the regimes and the nations' knobs, the business following the player's ship (spec §21 to §23) | approved and launched 2026-10-24 (Fable, in a worktree off the head of that day) |
| 73 | Fable | Water, damage control, health and the fight on deck: leaks and the pumps, the carpenter and the surgeon, the muster's states, the marines, the fight on deck, a station holder hurt at parity (spec §11, §13 to §17) | briefed 2026-10-24 (below), for the owner's approval; runs after 72 |
| 74 | Fable | Prizes, the strike and what follows, and the far fight; the consent revision for adversarial seats drafted with it (spec §11a, §18 to §20, §29) | after 70 and 73 |
| 75 | Opus | The ships: the *Indefatigable*, the *Prince de Neufchatel*, the 74; every file's armament, quarter bill and marines from 70's shape; **the ship's sub-types as fits and roles the scenario editor selects and customises in their reasonable degrees** (armed and unarmed, by rig, hull and role: the armed Indiaman, the revenue cutter, the privateer; the owner, 2026-10-24) | behind 70 |
| 76 | Opus | The signal books built out from 71's baseline | behind 71 |
| 77 | Opus | The gunnery's and the fight's evolutions from 70 and 73; the damage-control catalogue | behind 70 and 73 |
| 78 | Opus | Sight across land; collision; fine control of the sails and the gybe as an evolution | where the sailing wants it |
| 79 | Opus | The regimes from 72; the chart's Mediterranean block | behind 72 |
| 80 | Opus | Prizes and the continuation from 74; the consent revision's package if 55 has closed | behind 74 |
| 81 | Opus | The viewer's action: the gun ports and the guns drawn with their movement, a muzzle flash and a smoke plume over a few seconds at each gun's firing, the smoke lingering to leeward; the damage as the viewer's present honesty draws it (the owner's first action, 2026-10-24) | after 71; when the owner likes |

The M7b work wrapped up alongside: 58a, 58b and 67 merged (2026-10-23), the one whole suite
on the merged tree the lead's; the lead's playtest of 58b's gale book (its two trials
expected failures until it); the owner's decisions listed in 58a's, 58b's and 67's
as-merged records; 51, 60, 61, 63, 64, 65 and 69 on the books in `M7b-WorkPackages.md`; 55
deferred until testing begins in earnest.

## As merged

### Package 70 as merged (2026-10-24)

Merged `--no-ff` from the builder's worktree (sixteen commits on `5fb193e`, the design note
first; 78 files, ~9,200 lines) with no conflict, the merge's tree byte-identical to the
builder's tested head, so **the builder's suite on that tree is the suite on the merged
tree: the fast tier 3,596 passed; the slow tier of the twenty touched files 1,684 passed,
9 expected failures; the whole slow tier 3,918 passed, 12 expected failures, none failed;
the pace tests alone 7 passed**; ruff clean; the lead's sweeps clean (no consent file
touched, no model identifier, the ship files regenerated byte-identical, the physics
changed only by the state hooks rule 1 wants: the helm lost, the holed area, the parting's
cause said). The builder's session was cut three times by server overloads and once by the
machine's reboot; the worktree carried every commit through. Built as briefed, generously:
**the design of item 1 written before it was built** (`docs/design/Design-WorkInAction.md`:
the quarter bill a second assignment of the same men, beaten by `crew/quarters.py`; a gun's
service a cycle per gun stepped every tick beside the helm's `full and by`, never an
evolution, so no battle's timing is written anywhere but in the hands, the powder and the
sea; standing intentions the divisions keep and the few one-shot orders over them; sail
work the evolutions as they are, drawing on the trimmers and robbing the guns by the
fighting book's priority with the line saying from where); **guns as parts** with the
armament as one or several fits the scenario chooses (`ship: {fit: ...}`; the cutter's
12-pounder carronades the 1805 default and her long 3-pounders with eight swivels, the
Amazon class's 1795 establishment, the brig-sloop's and the merchant brig's, through the
generator with sources, the figures from memory marked unverified); **the gunnery's
orders** (clear for action, beat to quarters, cast loose, load with round, chain, grape,
double or a blank, run out and in, aim, fire as they bear, by divisions, on the up or down
roll, the broadside, a gun by its number or place, a shot across her bows, a gun to
leeward, cease firing, strike the colours, guns before sail and the reverse); **the hit
model** (point blank and random shot by calibre, the bands, heel on the quoin by the side,
the lee port shut within a foot of the water, the roll's doctrine, the sea's scatter; the
gunnery's own stream opened at the first shot); **damage as state** by the strain model's
own partings and wrecks with the cause said, sails holed, guns dismounted, boats stove,
the helm lost, shot holes written against the waterline for 73's well, men killed and
wounded off the bill; **the engaging doctrine as data** in every role file, the nations'
habits, a **privateer** role, the player's `fighting.orders`, **morale the ship's one
figure** and the strike by rule only when fired on and a shot has told; recognition's
least (an unrecognised target told once, the colours' state where 71 plugs in); **the
stations in action** (readings, events, the cables tripwire, the deltas carrying the
action's rows only while something is afoot, the director's `aboard:` causes and `say as`
for a gun captain); **the first action** (`first-action.yaml`: the King's cutter and a
French privateer cutter off the Lizard, two hours to the colours struck at seed 7); the
pace at 538 ticks a second with two crewed cutters engaged; **the far fight measured and
not wired** (`combat/far.py`, the same tables at three-minute rounds, for 74); truths
7-133 to 7-142; spec §7 to §12 as built, Harness §21c, primer chapter 22, the tuning notes.

**Taken another way, accepted:** `beat to quarters` a crew order beside `call all hands`
(the drum must not queue behind a heave-to); `cast loose` and `secure the guns` evolutions
whose hands are the gun crews' own; morale the ship's figure. **Measured:** the frigate's
broadside every 104 seconds with her full company and 159 with a quarter of each crew
down; her tack 447 seconds cleared, 436 at quarters under `sail before guns` with 84 hands
lent, 642 under `guns before sail`. **Pins:** no sailing passage moved; one captain's trial
moved as a finding (the trade trial with the stranger: the French brig, crewed while
chasing, now takes the cruiser's engaging within a mile and fires on the schooner at seven
cables; proven by the transition alone turned off; the old figures beside the new).
**Found on the way, fixed:** a promoted ship took her file's name; a merchantman is never an
overmatch; a ship with no guns never engages; the gunnery stream opened every tick on any
armed ship. **Found, carried:** the lookout calls a King's cutter and a trader both "a
cutter" (71 gives more); a crewed captain stays a minute in engaging after his mark strikes;
`say as` addresses a gun captain as "Mr". **Decisions (the owner, 2026-10-24):** the nations' gunnery
habits (French at twice the range, the rigging, the up-roll; British close, the hull, the
down-roll), a judgement kept in code, **move to the nations' data file** (71's, which is in
that file for the colours); the merchant's morale means one telling broadside brings her
colours down by the odds, and **the ship's sub-types** (the armed Indiaman and the rest,
selected and customised in the scenario editor) are 75's; the far fight waits for 74. **The
owner's first play** (`docs/playtests/2026-10-24-owner-first-action/`): the action holds,
the damage comes to the rigging, both sides hit and miss; the rules captain's engaging
helm turns a full circle through the wind's eye (for the next captain's pass, with 71);
two of the fighting book's orders were refused at the load (fixed by the lead the same day: the `at quarters` event registered by its words; the playtest's notes).

### Package 71 as merged (2026-10-24)

Merged `--no-ff` from the builder's worktree (ten commits on `bca885c`, the design note
first; 74 files, ~8,500 lines) with no conflict, the merge's tree byte-identical to the
builder's head; ruff clean; the lead's sweeps clean (no consent file, no ship file, no
physics file touched; no model identifier). The builder ran the fast tier whole on its
final tree (3,614 passed), the whole slow tier one mend earlier (3,941 passed, 11 expected
failures, one failed: its own forms test, mended and its four files rerun, 800 passed) and
the pace tests alone (8 passed); **the lead ran the whole slow tier and the pace tests on
the merged tree after the merge: 3,948 passed, 11 expected failures, 2 skipped, none failed; the pace tests 8 passed**. Built as briefed, generously: **the
signals' data shape designed and written first** (`docs/design/Design-Signals.md`: six files
under `data/signals/<root>/` in one shape for every nation, the declaration, the numerary
mapped to what a commanded captain does, the telegraphic dictionary, night and fog, the
convoy's, the private table's form; Britain's and France's books and the basic system every
other nation stands on, named from `data/nations.yaml`); **colours a state of both bodies**
(shown, none, false, struck, distress; a lookout gives the nation shown and never the true
one; the privateer closes under the enemy's colours and shows her own at four cables; a
shot under false or no colours told once as a pirate's act, the ports' stance turned and
every captain whose people saw it holding her a pirate; rule 3 completed); **the private
signal** made under the seed in the period's form, a paper of the King's ships, the King's
captain challenging every strange sail within the flags' range, the wrong answer the tell
and the chase by doctrine; **a signal hoisted** by three hands a phase a hoist, flying when
the hands have it up, read at the flags' range a minute later by whoever has the book, the
answering pendant; **the least relation** (`under the orders of`, by the scenario or the
director) with a commanded captain performing the entry's `does` and a brainless vessel
obeying by the least captain, the convoy of four tacking in succession on one hoist with no
model; **the hail in three bodies** by a table in `data/captains/hail.yaml`; **the lights,
the bell and the fog gun**; **the nations' habits in data** (70's `netherlands` key that
never matched found and fixed); **the captain's helm in action** (never within the
close-hauled angle plus half a point, never across the eye, the gage kept, `through_the_eye`
in every role file, the chase under the same law; the first action at seed 7 no longer
turns through the wind's eye and ends at 11:12 after 59 minutes of fire, 146 rounds); the
readings, events and director's forms; truths 7-143 to 7-151; two scenarios (the encounter
off the Lizard, the convoy of four); spec §1 to §6 as built, Harness §21d, primer chapter
23, the tuning notes.

**Taken another way, accepted:** a trader's rig that makes no answer to the private signal
is a stranger to be spoken, not an enemy (only a man-of-war's rig makes the silence a
tell); a single ship keeps fog signals only while a sail has been about within the hour
(so the thick-weather passages did not move); the offing's tack among the Molène islands
read against item 8 and left as the beating book's sea-room judgement, the station gale an
expected failure still. **Pins:** truths 7-133, 7-144 and 7-145 by the builder's own
mendings (the hoist flying when the hands have it up, the helm's law), the old beside the
new; two captain's trials moved as findings (the station stranger, the King's brig's private
signal to the Palinure, 756 to 787 lines; the trade stranger, the French brig's signal and
her going about for the schooner, 1248 to 1246), each proven by its switch alone; no
sailing passage with no other ship in it moved. **Found on the way, fixed:** the hoist flew
from the book's minute before the hands had it up; a telegraphic sentence was hauled down
before it could be read; `give chase` went after the wrong sail (the captain now names his
stranger's rig, a judged enemy is a stranger to the order, and `cutter`, `lugger` and
`sloop` are rig words); the chase held the tack that opened her (45c's law: a chase more
than a point on the other side of the eye is now gone about for, under a switch, which the
lead accepts for every chase). **Found, carried:** the planner lays no way into Plymouth
from the south-west (61); the frigate close-hauled makes four knots to the cutter's seven in
fourteen knots of wind (the hull's); a commodore stopped leaves `_keep_company` to 72.
**Decisions (the owner, 2026-10-24):** whether a stranger of any rig that will not answer the
private signal should be closed and hailed by doctrine **stays open**, the owner weighing
the investigation of every stranger against the time it costs and its edge cases (as built:
only a man-of-war's rig makes the silence a tell); the fog signals **only while a sail has
been about**, as built, "that keeps it interesting"; `through_the_eye` `shift` for every role
and the chase's new tack rule for every chase **stand as built**, the owner seeing no
problem and asking their implications be shown in play; the succession's three minutes
become the wake with 72; the French and basic books' numbers are all made, for 76 to
correct.

## Package 70: the combat core (`freesail/combat/` new: `shot.py`, `hits.py`, `morale.py` or as the design finds; `freesail/crew/bill.py` the quarter bill beside the watch bill, `crew/model.py`, `muster.py` the casualties' states; `freesail/ship/schema.py`, `parts.py`, `graph.py` the gun as a part, the magazine and the shot as stores; `tools/gen_ships.py` and `data/ships/cutter.yaml`, `frigate-36.yaml` first, the others as reached; `freesail/evolutions/` the gunnery's evolutions and the work in action, `data/evolutions/*.yaml`; `freesail/world/captains.py`, `brains.py`, `data/captains/*.yaml` the engaging state filled, `data/standing_orders/fighting.orders` new; `freesail/world/orders.py`, `data/vocabulary.yaml`, `freesail/orders/` the orders of the gun deck; `freesail/api/readings.py` the guns, the damage and the bill as readings; `freesail/agents/harness.py`, `director.py`, `data/director/` the stations in action and the director's forms; `freesail/world/scenarios.py`, `data/scenarios/` the first action; `docs/TechnicalSpec-M7.md` §7 to §12 as built; `docs/agents/Harness.md`; the primer's new chapter; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-133 onward)

Fable; the first package of the milestone, and the one that sets the shape every later
combat package builds behind (75 the ships, 77 the evolutions filled out, 73 water, health
and the fight on deck, 74 the strike's consequences and the far fight). Spec M7 Part 7-ii
(§7 to §12) and its seven rules, rule 1 (damage is just state), rule 2 (a gun is served by
the bill), rule 6 (realism, not pacing) and rule 7 (nothing pre-defines a battle's timing)
first among them; the owner's frame (single-ship actions first, the framework open to more
ships); the striking-colours study (`docs/design/Scenario-StrikingColours.md`) and the
owner's combat brainstorm in `docs/design/NotesForM7.md`; §33a for what the last M7b
packages taught. **This is a generously scoped package by the owner's method of 2026-10-23:
the brief binds the intent and names the ground, and the builder designs.** Each item below
is an intent with the lead's reading of a way; the intent binds, the reading is advice. The
builder may take an item another way with its reason, may grow a part where the work shows
it should (the marines' place in the bill, the shot hole's first water, the gun captain's
words, a thing the first action wants), and says plainly in its report what it left and
why. There is no day count; the owner's usage is the budget, and he has said it may run to
the week's limit. **The design of item 1 comes first and is written down before it is
built** (a page in the tuning notes or a design note under `docs/design/`), because every
other item hangs from it.

1. **The quarter bill, and work in action (§8a; rule 7).** At quarters every man has a
   station by a quarter bill the ship's file carries beside her watch bill (through the
   generator, each figure with its source: the period's quarter bills, Falconer, the
   Establishments, the frigate's own books where found, judgement where not), and the
   work of an action is **continuous and concurrent, never a queue**: a gun's service is
   a cycle that runs by itself while hands and powder last; `engage her to starboard`,
   `fire as they bear`, `aim at her rigging` are standing intentions the divisions keep,
   logged when they change something; a broadside at the word, a single gun, `cease
   firing` and `boarders away` ride over them; sail orders in action draw on the sail
   trimmers first and then on the guns by the fighting book's priority, so a tack with
   the guns served is slower by exactly the hands it takes, said from where, and the
   player never wonders how his orders will queue. A ship with hands to spare fights
   better because every order in hand gets done; a short-handed one suffers by the same.
   *The lead's reading:* the standing-intention form the helm's `full and by` already has
   is the shape; the quarter bill is the scheduler and the evolutions (M3's, with hands, a
   duration and steps) are its leaves; clearing for action and beating to quarters move
   the ship from the watch bill's rule to the quarter bill's and `secure the guns` and
   `pipe down` move her back; the bill says where hands came from when it robs a
   division. The builder's design may find a better shape; what binds is the intent.
2. **Guns as parts (§7).** Each gun and carronade a part of the graph by its position (the
   broadside by number and side, the bow and stern chasers, the swivels) with its carriage,
   tackles and breeching, a load state (empty; loaded with round, chain, grape or double;
   run in or out; primed), elevation and train; the magazine and the shot lockers as stores
   the gunner and the purser count (powder in cartridges by calibre, shot by kind); the
   gunner, the quarter gunners and the gun crews from the muster's posts and item 1's bill.
   **Through the generator with the source beside each figure, never by hand**: the cutter
   first, **with two fits the scenario chooses between (the owner, 2026-10-23)**: the
   12-pounder carronades the Admiralty gave its cutters from the 1790s, the default of 1805,
   and the long 3-pounders with eight swivels her file names in words, the hired and
   revenue cutters' fit; each with its source; and the frigate
   (the Amazon class's 18-pounders, her carronades and her chasers by Winfield and the
   Establishments); the brig, the schooner, the lugger, the merchant brig and the smack as
   the builder reaches them or left to 75 with their shape settled. A gun dismounted is a
   part out of the bill, as a sprung spar is out of the sail plan.
3. **The gunnery's cycle as evolutions (§8; rule 2).** `clear for action`, `beat to
   quarters`, `cast loose the guns`, `load with round shot` (chain, grape, double), `run
   out`, `fire` (by broadside at the word, by division, **as they bear** (the period's
   independent fire, the first broadside together and then each gun as it is loaded and
   bears), a rolling broadside), **a single gun by its number or place** (`fire the bow
   chaser`, `fire No. 3 gun`, `fire a shot across her bows`: the ranging shot, the gun to
   leeward, the signal gun, the one shot of a roleplay), `cease firing`, `secure the guns`;
   each with hands, ratings, fatigue and time from the bill as sail work has them. **The
   rates of fire fall out of the muster**: a full and drilled frigate's broadside every
   minute and a half to two minutes at the start of an action, falling with fatigue and
   casualties; a merchantman's few guns served by few untrained hands at a fraction; the
   figures are judgements with Douglas (*A Treatise on Naval Gunnery*, 1820), Lavery
   (*Arming and Fitting*), and the period's captains' logs as the sources, named beside
   each, pinned by the truths and tuned in play. The dialect gains the orders (the
   vocabulary, the library's grammar, the standing orders' forms), and a rules captain
   gives them by his book.
4. **Shot and the hit model (§9).** A fired gun produces shot with a simple ballistic by
   calibre, charge and elevation (point-blank a few hundred yards, random shot to a mile,
   the carronade short and heavy) and a hit chance by range band, the roll and the aim,
   resolved against the target's **part graph by the aim's doctrine** (the rigging, the
   hull, or between); **heel and the sea**: the lee battery fires lower and shorter and the
   weather battery higher and longer by the heel, the gun's elevation answering only so
   far; a lee port whose sill is within a foot of the water is shut and its gun silent;
   the roll's timing is the gunner's doctrine (the up-roll for the rigging, the down-roll
   for the hull) and the sea state scatters the shot by its height; deterministic under
   the seed. The fired-at ship perceives the fall of shot (short, over, a hit, in her own
   log by what her people can see) and the firing ship her own; the truth sees both. The
   bands and figures are 70's to set with their sources, as §34 leaves them.
5. **Damage as state (rule 1; §9).** No second model of the ship exists for the fight. A
   hit is a change of state the game already has or this package adds, by the cause the
   director's hand uses today (`aboard: the fore topmast is found sprung` and a shot that
   springs it end in the same state): a line parted (the sail comes down as it does now),
   a spar sprung or carried away (clearing the wreck as it is), a sail holed (its area
   cut), a gun dismounted, a boat stove, the wheel or the tiller ropes shot away (the helm
   lost until repaired), **a shot hole at or below the waterline written as state for 73's
   well to read** (the hole, its place against the waterline, its size; no water flows
   from it until 73, unless the builder finds the first water cheap and says so), and **men
   killed and wounded written to the muster as states that take a man off the bill** (the
   surgeon's work, the sick list's course and a man's return are 73's; the count, the
   names where the muster has them and the loss of hands are this package's). The
   carpenter's report and the readings (`the guns`, `the damage`, `the bill`, `state`) show
   it all; the viewer draws what is there at its present honesty.
6. **The fighting instructions, the captain's engaging, and morale (§10; decision 7).** The
   rules captain's engaging state (present and empty since M6) filled by **doctrine as
   data** in the captains' files: whether he engages at all (the merchantman runs or
   strikes by the odds, the privateer takes what pays and runs from a King's ship, the
   King's ship engages her class and shadows a heavier), from which side (the weather gage
   to engage, the lee to escape), at what range (the British close, the French at long
   shot), his aim, when he boards and when he breaks off; a **fighting book** of standing
   orders in the dialect (`engage from to windward`, `aim at her rigging`, `hold your fire
   until she bears`, `when she strikes, cease firing`) that the player reads and rewrites
   as the starter book is the sailing's, and that yields to the sailing's book what the
   other hand holds (58b's rule, §33a); and **morale, the one new quantity**: the company's
   readiness to fight on, from the captain's doctrine, the losses, the odds, the nation's
   habit and the hands' temper, giving **striking by rule** (the colours struck when morale
   fails, said in the log with its reason), the struck ship ceasing fire and lying to, her
   state `struck`, the victor's `cease firing` by his book; the player's own `strike the
   colours` never refused, its consequence told. *Whether morale is the ship's figure or
   each division's is 70's to decide, with the reason written.* What follows the strike
   (the prize crew, the prisoners, the captive's channel) is 74's; this package ends at the
   colours down and the firing ceased.
7. **Recognition before fire (rule 3), the least of it.** A ship fires on a ship her people
   have made out as an enemy by the nations table as it stands and by what the lookout has
   made out of her; firing on a ship not made out, or on one not at war, is not refused
   but its consequence told (the stance of every port and ship that hears of it, by the
   table's own means). The true colours, the private signal and the hail are 71's: this
   package leaves the hook (a ship's colours shown as a state the lookout reads, the
   nation's by default) where 71 plugs in, and says in its report what 71 will find.
8. **The stations in action (the harness; §33a).** What a station reads: the guns and the
   damage in one line when they change (58a's deltas), the fall of shot and the hits as
   notable lines, the casualties as lines, the bill's word when hands are robbed; the
   tripwires gain the action's events (`she opens fire`, `a shot strikes her`, `her
   colours come down`, `a sail within <n> cables`), judged by the readings; the samples
   kept small enough that a model's thinking does not cost it a broadside (the "n minutes
   since your last reply" line read against the cycle's figures and the measure recorded).
   The director's forms for action follow `WORLD_ORDER_FORMS` (every example performed by a
   test): his hand reaches the new state by the table's plausible causes (a gun found
   dismounted, a cartridge found damp), his truth shows both ships' guns and damage, and
   his `say as` speaks for a gun captain or the gunner. A station holder hurt is 73's
   (§16a); this package writes the hit to his person's line and nothing more.
9. **The first action, the pace, and the far fight's measure (§12; rule 5).** A scenario
   under `data/scenarios/` for the first single-ship action (the study's shape: two ships
   that can make each other out, one that will fight and one that may strike), played by
   the rules captains with no model seated and by the player at one station; the truths
   of §12 (two cutters at pistol shot and the damage in the part graph; the frigate's
   broadside in a minute and three quarters with her full company and in three with a
   quarter of them casualties; a tack with the guns run out slower than cleared; the
   merchant brig fired into strikes by morale, the log saying why; an action that runs
   for hours as a legitimate outcome, and one of a quarter of an hour the same) numbered
   7-133 onward; **the pace measured** with two crewed ships in action against the baseline
   (the owner's 95 ticks a second with twelve crewed ships; the pace floors of the
   conftest not lowered: if an action breaks them the tables are made cheaper, not the
   floors), and **the far fight measured once**: the near action against the same tables
   run at coarse steps with no crewed ship (a round of broadsides a few minutes long),
   recorded for 74 to build from, not built here beyond what the measure needs.
10. **Truths and records.** The truths above; spec §7 to §12 "as built" with what was
    taken another way; `docs/agents/Harness.md`'s section on the stations in action; a
    new chapter of the primer (an action, from clearing for action to the colours struck,
    in the player's words); the director's library; the tuning notes (item 1's design, the
    figures and their sources, the rates measured, what moved and its proof by bisection,
    the pins with the old beside the new, the pace and the far fight's measures, found on
    the way, the decisions for the lead and the owner); the suite as run (the fast tier,
    the slow tier of the touched files, the whole suite if the machine is the builder's
    alone, the pace tests alone and last) and a report to the lead.

**Not built here:** colours, the private signal and the hail (71); water from the hole,
the surgeon, the marines' fire and the fight on deck (73; the marines keep their place in
the bill from item 1); the prize and the captive (74); the far fight beyond its measure
(74); the new ships (75); boarding (§11a, with 73 and 74). **The head rules bind:** no
model identifier in any file; nothing under `docs/agents/consent/` touched; a world order
never shown as sent; the ship files through the generator with the source beside each
figure; the recorded passages' pins re-measured only where a change moves them, with the
old figure beside the new and the proof by bisection (an action's package should move no
sailing passage: if one moves, that is a finding); never a test skipped, disabled or
quarantined; **realism, not pacing** (rule 6: nothing made deadlier or quicker for the
game's sake); **nothing pre-defines a battle's timing** (rule 7). The physics of the hull,
the sails and the sea is read by the hit model and not changed by it.

## Package 71: signals and the voice between ships (`freesail/world/signals.py` new; `data/signals/<nation>/` new; `freesail/world/ships.py`, `nations.py`, `data/nations.yaml` the colours and the nations' habits; `freesail/world/lookout.py` the colours and the flags made out, the lights; `freesail/world/hearing.py`, `orders.py`, `crews.py` the hail's three bodies; `freesail/world/captains.py`, `brains.py`, `data/captains/*.yaml` the challenge, the false colours, the chase by doctrine and the helm in action; `freesail/combat/action.py` the recognition completed and the habits read from data; `freesail/evolutions/` the hoist; `freesail/orders/`, `data/vocabulary.yaml` the orders; `freesail/api/readings.py` the colours and the signals as readings; `freesail/agents/harness.py`, `director.py`, `data/director/` the stations and the director's forms; the papers (`data/papers/`); `data/scenarios/` an encounter and a convoy; `docs/TechnicalSpec-M7.md` §1 to §6 as built; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-143 onward)

Fable; the second package of the milestone, run alone after 70 by the owner's rule. Spec M7
Part 7-i (§1 to §6) whole, with rule 3 (recognition before fire) and rule 4 (rules first,
models welcome); the owner's note 1 (any nation a combatant, the books built out
progressively from one foundation); M7b's play (R-17 the voice between ships, R-54 a chase
with no good options); the striking-colours study; §33a. **Generously scoped as 70 was:**
the brief binds the intent and names the ground, the builder designs, takes an item another
way with its reason, grows a part where the work shows it should, and says what it left and
why; no day count. **The data shape of the signals is this package's first design, written
down before it is built** (a design note under `docs/design/`), because 76 builds the books
out from it and every nation's book must fit it. Each item an intent with the lead's
reading; the intent binds.

1. **Colours as state (§1).** A ship's colours are shown (which ensign), none, false
   (another nation's, the ruse the law allowed until the first shot), struck, or the
   signals of distress; the orders `hoist the colours`, `hoist French colours`, `haul down
   the colours`, `strike the colours` (70's, kept), `fire a gun to leeward`; the lookout
   makes colours out at the glass's range by their size and the light; a privateer of the
   business sails under false colours by her doctrine and shows her own at the range the
   doctrine says; **firing under false colours is not refused but logged, and every
   nation's stance turns** (the business's stances, R-54's bluff made real); the
   vocabulary's `hoist our colours` refusal goes. 70 left the hooks (`extra["colours"]`,
   the lookout's `shows_colours`, `action._recognition`): this item completes rule 3, so
   that a ship fires on what her people have made out by colours, by the private signal
   or by the hail, and 70's `action.unrecognised` becomes the exception it was meant to be.
2. **The private signal (§2).** The challenge and its reply as a small table per nation
   per month, made under the seed in the period's form (flags by day, lights or false
   fires by night), carried as a paper of the ship's library (`papers: private_signals`);
   `show the private signal`, `answer the private signal`; the rules captain of a King's
   ship challenges a stranger within the glass's range and reads the answer, right, wrong
   or none, **the wrong or missing answer the tell that makes her a stranger and starts the
   chase by his doctrine**; a privateer or a merchant has no table; a captured table is a
   paper 74's prize carries, good until the month turns.
3. **The signal books (§3): the shape for any nation, and the first books.** The data
   shape (`data/signals/<nation>/`) the same for every nation of the table: a numerary book
   (number to meaning, each entry mapped to an intent or an order the rules captain
   understands, with its qualifiers: the compass, numbers, a ship by her pennants), the
   telegraphic dictionary, the night and fog signals, the convoy's instructions, the
   private tables' form. **The British books first** (Howe's 1790 and the Admiralty's 1799
   numerary, some two hundred entries chosen for what a squadron, a chase and a convoy
   need; Popham's telegraphic of 1803 for the free sentence; the night and fog book; the
   *Signals and Instructions for Ships under Convoy*), **the French book smaller and marked
   where made** (du Pavillon's tables and the numerary that followed), and **the basic
   system every nation has from the foundation** (a numerary of a few dozen entries in the
   period's common form, a private table under the seed, night and fog, the convoy's), so
   that the Spanish, the Dutch, the Danes or the Americans may be combatants in a
   fictional scenario; the sources named in each file, and the hoists that are the
   builder's own invention marked so. 76 builds the books out from this shape and never
   before it.
4. **A signal is a thing hoisted and read.** The hoist an evolution (the hands at the
   halyards, a minute a hoist, the substitute and the preparative, a telegraphic sentence
   as many hoists as it needs and daylight only); the signal read by the lookout at the
   range the flags' size and the light allow ("she makes a signal we cannot read" without
   the book, a minute to look it up, the answering pennant), and in the dark or in fog the
   night book's lights, false fires, rockets and guns; the orders by meaning (`make the
   signal to chase`, `make the signal: enemy in sight bearing NW`, `make the telegraphic
   signal: ...`, `answer the signal`, `repeat it`, `haul it down`), the number in the log
   beside the meaning. The receiving rules captain acts by doctrine when the sender
   commands him and logs it otherwise: **the least relation** (a scenario names whose
   signals a ship obeys, `under the orders of`, enough for a convoy of four to tack in
   succession on one hoist with no model seated) is this package's; **the squadron as a
   genuine set, the formations and station keeping are 72's** and not built here. A model
   at a flagship gives a signal by the order, by the equal-reach rule (§34), unless the
   work shows a better way.
5. **The hail, and the voice between ships (§4; R-17).** Within hail a ship is spoken by the
   speaking trumpet (`hail her`, `say to the <description or name>: <words>`) and the
   answer comes as a line heard on deck, by the three bodies: the rules captain by table
   (what ship, whence, whither, cargo, the news, by his nation and his stance; a privateer
   under false colours lying; a King's ship demanding to know who she is and bidding her
   heave to), a model at the other captain's station given the words in his sample and
   answering freely, the player typing the hail and hearing the answer; between two rules
   captains the standard exchange written to both logs once and the stances read ("spoken",
   as the lookout keeps it); **the hail as the first order of a search** ("heave to, I am
   sending a boat", the boat as 63 and 53b have it, the search itself a scene of the
   director's or the doctrine's, not built here beyond the heave-to demanded and
   answered); the director's `say as` across the water and 67's seat at a person as they
   stand. 65's reading of who perceives what (the place's knowledge, on the books) is read
   and not built: a hail is heard by the deck.
6. **The lights and the bell (§5).** A stern lantern, top lights for ships in company, the
   fishing boat's lantern on her nets, merchantmen often none, by order and by the standing
   orders (`hoist the lights`, `show no lights`); the bell at anchor in fog and the gun or
   the drum under way as the Regulations and the custom have them; the lookout sees a
   light at night as it sees a sail by day, at the range a light carries, and hears the
   bell and the gun in fog. **Sight across land is 78's**, not here.
7. **The nations' habits to data (the owner, 2026-10-24).** 70's `NATION_HABITS` (the range
   a nation engages at, its aim, its roll) move from code into `data/nations.yaml` beside
   each nation's colours, read by 70's doctrine; the same entry names the nation's signals
   root (`data/signals/<nation>/`) and whether it is a well-built book or the basic
   system, so that a nation is built out in one place.
8. **The captain's helm in action (carried from the owner's first action, 2026-10-24).**
   70's engaging law steered by the enemy's bearing alone and turned the King's cutter a
   full circle through the wind's eye, aback with the carronades silent for half an hour
   (`docs/playtests/2026-10-24-owner-first-action/notes.md`). The engaging captain never
   orders a course within the close-hauled angle; when the enemy passes through the eye he
   shifts the engaged battery or tacks or wears by his doctrine; he keeps or takes the gage
   the doctrine names; the chase by doctrine (item 2's tell, 70's `give chase` renewed)
   works the same law; and 57's offing's tack among islands with no room to wear (the
   station gale's grounding, the trial an expected failure with its reason) is the same sea
   sense, taken with it or left with its reason. 70's first-action truths may move by it,
   with the reasons and the bisection the head rules ask.
9. **The stations, the director and the readings.** `the colours`, `the signals` (the
   hoists seen and made, with their meanings where the book is ours), `the private signal`
   as readings; the events and tripwires (`she hoists her colours`, `a signal made`, `the
   private signal answered`, `hailed`); the director's forms after `WORLD_ORDER_FORMS`
   (`ship "X": hoist false colours`, `ship "X": make the signal ...`, his truth showing
   every ship's true colours and her signals), and the director's brief saying whether his
   ships may fight under false colours; the harness's samples carrying a hail and a signal
   as words a model answers.
10. **Truths and records.** §6's truths but sight across land (a cutter under false colours
    spoken by a King's frigate answers the hail by the table and is made out at the right
    range; the private signal answered wrong makes her a stranger and the frigate gives
    chase by doctrine; a convoy of four under a commodore tacks in succession on one hoist
    with no model seated; a telegraphic sentence takes the hoists and the minutes the book
    says; a signal made in fog is a gun and not a flag; and item 8's: the King's cutter
    engaging to leeward of a privateer never puts her head in the wind), numbered 7-143
    onward; a scenario or two under `data/scenarios/` (the encounter of the study's shape;
    the convoy of four); spec §1 to §6 "as built"; the Harness; a chapter of the primer
    (colours, the private signal, a hail, a signal made and read); the director's library;
    the tuning notes (the data shape's design, the books' sources and what was made, the
    hail's tables, the habits moved, what moved and its proof, found on the way, decisions,
    the suite as run with its counts); the fast tier, the slow tier of the touched files,
    the whole slow tier when the machine is quiet, the pace tests alone and last.

**Not built here:** sight across land (78); the squadron as a set, formations and station
keeping (72); the full books (76); the search's scene and the boat's work (the director's,
63); prizes and the captured papers' use (74); marines (73). **The head rules bind** as 70's
brief has them: no model identifier; nothing under `docs/agents/consent/` touched; a world
order never shown as sent; the pins re-measured only where a change moves them, old beside
new, proven by bisection; never a test skipped, disabled or quarantined; realism, not
pacing; the physics read and not changed.

## Package 72: the naval system (`freesail/world/squadrons.py` new; `freesail/world/crews.py`, `brains.py`, `ships.py` the set, the offsets and the promotion; `freesail/world/signals.py` the least relation given to the set; `freesail/world/captains.py`, `data/captains/*.yaml` station keeping, the escort's and the commodore's doctrine; `freesail/standing/` station keeping as a standing-order kind; `freesail/world/business.py`, `data/business.yaml`, `data/nations.yaml` the regimes and the nations' knobs, the business following the player's ship; `freesail/world/weather.py` R-39's bound; `freesail/world/orders.py`, `freesail/agents/director.py`, `data/director/` the squadron's forms; `freesail/api/readings.py`; `freesail/agents/harness.py` the commodore's station; `data/scenarios/` the convoy of six, the blockade; `docs/TechnicalSpec-M7.md` §21 to §23 as built; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-152 onward)

Fable; the third package of the milestone, run alone after 71 by the owner's rule. Spec M7
Part 7-vi (§21 to §23) whole, with rule 4 (rules first, models welcome) and rule 5 (the far
ships fight as the near do, coarsely); the owner's note 8 (a genuine set, split and joined
freely); the owner's frame (the command system and the signals to make more ships sane, six
on six the ideal and never rushed); the owner's requirement that the business follows the
player's ship across regions; 71's as-merged record (the least relation, the convoy of four,
the succession's three minutes to become the wake) and its design note; §33 for what is
carried in. **Generously scoped as 70 and 71 were:** the brief binds the intent and names
the ground, the builder designs, takes an item another way with its reason, grows a part
where the work shows it should, and says what it left and why; no day count. **The
squadron's shape is designed first and written down before it is built** (a design note
under `docs/design/`), because 79 builds the regimes out from it and the gate's six on six
is measured on it. Each item an intent with the lead's reading; the intent binds.

1. **The squadron as a genuine set (§21).** One new object: a set of vessels with one
   commander and one goal, and nothing more fixed. Ships join it and leave it freely: by
   the scenario file, by the director (`squadron "Channel": detach the Medusa`, `... join
   the Harpy`), by the world (a ship separated in a gale sails alone until she rejoins by
   signal; a prize joins her captor's company, 74's; a straggler is lost to the convoy),
   and by the commander's own signal (a division detached in chase and recalled); a
   squadron splits into divisions with their own leaders and merges again; a ship alone is
   a squadron of one for the brain and no object at all for the player. 71's `under the
   orders of` becomes what the set reads, kept as the field for a ship under orders
   outside any set.
2. **One brain at far detail, and the promotion in station.** The set is moved as one
   brain at far detail with the members at formation offsets (the line ahead, the line
   abreast, the order of sailing, the convoy's columns), re-formed whenever the set
   changes, so that a convoy, a blockading squadron and a line of battle are one cheap
   thing until the player is near; under the cap the members promote one by one, each in
   her station, and a promoted member keeps her station by her own captain's book. **The
   pace is a figure of this item**: the owner's baseline is 95 ticks a second with twelve
   crewed ships; six on six at far detail must be cheap and measured, and the conftest's
   floors are not lowered.
3. **Formations and station keeping.** Station keeping as a standing-order kind the
   captain's and the squadron's books use (`keep station two cables astern of the
   flagship`, `keep your station in the line`), the helm's law and the sails' trim serving
   it (71's `helm_in_action` and the sea sense of 58b as they are); in succession by the
   wake, the leader's going about the mark (71's three minutes replaced); the order of
   sailing by the wind; a straggler, a ship out of her station and the signal that calls
   her in.
4. **The squadron's book, the commodore and the escort.** The commander's standing orders
   as a book like the captain's (the signals of the day, the night and fog signals, the
   order of sailing, the rendezvous), his signals the command by 71's books; the
   subordinate rules captains obeying the book and their doctrine; **a model at the
   flagship as the orchestrator** the owner saw in play, given the squadron's state in his
   sample and commanding by `make the signal`; the escort's doctrine (a stranger answered
   by doctrine, the convoy closed round the commodore, a straggler covered, a privateer
   driven off by the odds or the straggler cut out by hers), the commodore's (the
   rendezvous kept, a division detached and recalled).
5. **The regimes (§22).** A ship of a nation in port, in ordinary, on station, on passage,
   in convoy or escorting, on blockade, in chase, each a doctrine of a few rules in data:
   the blockade's inshore and offshore squadrons blown off by a westerly gale; the convoy
   at the slowest ship's pace; a ship in ordinary a hull in port commissioned with a delay
   by the business or the director; the nations' knobs in `data/nations.yaml` beside 71's
   habits (the British keep the sea and engage, the French keep port, the privateers of any
   flag chase what pays, the Americans of 1812 fight single actions). The shape and the
   first of each regime are this package's; 79 fills them out.
6. **The business draws them, and follows the player's ship.** The business draws
   convoys, escorts and squadrons under the seed as it draws traders and fishermen (M6
   §19), and **follows the player's ship across regions** (the owner's requirement of
   2026-10-17): the convoys and the long chases crossing the chart's blocks, a ship under
   way at a block's edge carried over with her state and her set.
7. **The weather's bound (R-39, carried in).** The summed field's seasonal bound and the
   climatology's drift onto Iberia, kept out by 58a and placed here because a squadron at
   sea for days and a blockade blown off by a gale want honest weather over a week; the
   small part (an appended system's ramp, a high doubted) is 58a's and stands. Taken only as
   far as the squadrons want it, with the reason written.
8. **The planner across the land (61, carried in).** A convoy's route and a blockade's
   station want a plan that does not cross the land (71 found the planner lays no way into
   Plymouth from the south-west; 58b found the Roscoff plan crossing the Isle Verte). Built
   here if the convoys want it, else left to 78 with the reason.
9. **The stations, the director and the readings.** `the squadron`, `the station`, `the
   convoy`, `the order of sailing` as readings; the events and tripwires (`a ship out of
   her station`, `the commodore makes a signal`, `a straggler`); the director's forms after
   `WORLD_ORDER_FORMS` (the set joined and detached, a squadron's goal, a convoy drawn),
   his truth showing every set and its stations; the harness's samples at a commodore's or
   a subordinate's station; a squadron never shown as a thing to the player but by its
   ships and its signals.
10. **Truths and records.** §23's truths (a convoy of six under a brig-sloop meets a
    privateer schooner, the escort makes the signal to close round the commodore, the
    convoy obeys with no model seated, the privateer cuts out the straggler by doctrine or
    is driven off by the odds; a blockading squadron off Brest blown off by a gale and the
    business's frigate slipping out on it; the squadron keeping its line at far detail and
    promoting member by member as the player closes, each in her station; the pace of six
    on six at far detail and under the cap), numbered 7-152 onward; the scenarios under
    `data/scenarios/`; spec §21 to §23 "as built"; the Harness; a chapter of the primer (in
    company: the convoy, the station, the commodore's signals); the director's library;
    the tuning notes (the set's design, each item, the pace measured, what moved and its
    proof, the pins old beside new, found on the way, decisions, the suite as run with its
    counts); the fast tier, the slow tier of the touched files, the whole slow tier when
    the machine is quiet, the pace tests alone and last.

**Not built here:** fleet actions beyond six on six (§32); prizes joining a company beyond
the hook (74); the marines (73); the regimes filled out and the Mediterranean block (79);
sight across land (78); the full signal books (76). **The head rules bind** as 70's and
71's briefs have them: no model identifier; nothing under `docs/agents/consent/` touched; a
world order never shown as sent; the pins re-measured only where a change moves them, old
beside new, proven by bisection; never a test skipped, disabled or quarantined; realism,
not pacing; the physics read and not changed; the ship files through the generator.

## Package 73: water, damage control, health and the fight on deck (`freesail/world/hull.py` or `ground.py` the water in the ship, `physics/hull.py` read for the free surface; `freesail/evolutions/` and `data/evolutions/` the pumps, the plugs, the fothering, the jury work, the small arms and the boarding's fight; `freesail/ship/schema.py`, `parts.py` the pumps, the spares and the stores, `tools/gen_ships.py` and `data/ships/*.yaml`; `freesail/crew/model.py`, `muster.py`, `quarters.py`, `hands.py` the muster's states, the surgeon's and the carpenter's posts, the marines' division and kit; `freesail/world/needs.py` the needs' ends; `freesail/combat/hits.py`, `action.py` the shot hole's water, the musketry and the grape on the men, the fight on deck; `freesail/world/captains.py`, `data/captains/*.yaml` the doctrine of boarding and of the pumps; `freesail/orders/`, `data/vocabulary.yaml` the orders and the pumps' refusal retired; `freesail/api/readings.py` the well, the damage report, the sick list, the butcher's bill; `freesail/agents/harness.py`, `director.py`, `data/director/` a station holder hurt and the director's causes; `data/scenarios/`; `docs/TechnicalSpec-M7.md` §11, §13 to §17 as built; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths from the number after 72's)

Fable; the fourth package of the milestone, run alone after 72 by the owner's rule. Spec M7
§11 (the marines, the small arms and the fight on deck), Part 7-iii (§13 to §15) and Part
7-iv (§16, §16a, §17) whole, with rule 1 (damage is just state), rule 2 (served by the bill),
rule 6 (realism, not pacing) and rule 7; the owner's notes 3 (the marines, their kit by
nation and period, firing from the deck and the tops, their duties) and 7 (a station holder
hurt at parity); 70's as-merged record and tuning notes (what 70 left you: the shot hole
written as state with its place against the waterline and no water flowing, men killed and
wounded off the bill with no surgeon, `boarders away` refused in words, the marines in the
quarter bill with no fire); the owner's first action (`docs/playtests/2026-10-24-owner-
first-action/notes.md`: the repairs he tried and what was refused, the damage report that
should name the parted lines, `reeve new lines`, the standing rigging that cannot be set up,
`the surgeon`); the hotfix's stopgaps of M7b (`aboard: the leak stopped`, `the well pumped
out`, the Horta grounding) and 68's pumps refusal, retired here. **Generously scoped as 70,
71 and 72 were:** the brief binds the intent and names the ground, the builder designs,
takes an item another way with its reason, grows a part where the work shows it should,
and says what it left and why; no day count. **The water in the ship and the muster's
states are designed first and written down before they are built** (a design note under
`docs/design/`), because 74's strike and 77's catalogue build on them. Each item an intent
with the lead's reading; the intent binds.

1. **Water in the ship (§13).** Leaks from shot holes (70's state, now flowing by the
   hole's size, its place against the waterline and the heel), from the ground (the Horta
   grounding's stopgap replaced), from working seams in a seaway, from heavy seas shipped
   and rain with the hatches open; the water in the well a quantity the carpenter sounds
   (the hotfix's reading kept) and a stability penalty as the free surface grows (the
   physics read, not changed); **the pumps** an evolution with hands and a rate by the pump
   and the men (`man the pumps`, `spell the pumps`, the chain pump and the hand pumps by
   the ship's file through the generator with sources), gaining on the leak or losing;
   **foundering** when the water wins (the hands to the boats, the ship lost, the
   scenario's end or the director's continuation); `batten down the hatches` and the hands
   kept below in a gale. 68's refusal line for the pumps retired; the director's `aboard:
   the well pumped out` and `the leak stopped` kept as his causes with a doubt.
2. **Damage control and jury work (§14).** Plugging a shot hole (the carpenter and his
   crew, shot plugs and oakum, the time by the hole's place), fothering a sail over a leak,
   fishing a sprung spar (in the kit since M3b, taken up), preventer braces and backstays
   and chain slings before an action, cutting away a mast over the side, a jury mast from
   the spare spars, **knotting and splicing the running rigging and setting up the standing
   rigging shot away** (the owner's `reeve new lines` as an evolution that roves every
   parted running line in turn, the shrouds and backstays set up again with deadeyes and
   lanyards in the time the bill says); each an evolution competing for hands with the
   guns and the sails by the fighting book's priority, which is where the fight's
   decisions live; **the spares as the boatswain's and the carpenter's stores, counted**,
   through the generator with sources (the cutter with no spare topgallant mast stays so);
   **the damage report naming every parted line, sprung spar, holed sail, dismounted gun
   and shot hole**, so that a player finds what to mend. The first of each; 77 fills the
   catalogue out.
3. **The muster's states, the surgeon and the needs' ends (§16).** Beyond fresh and tired:
   hurt (fit for light duty), wounded (below, the surgeon's), sick (the sick list, by the
   needs' ends and the ship's condition: foul water, short allowance, cold and wet), dead
   (struck from the muster, buried at sea with a line of the log); the surgeon and his
   mates as posts with a place (the cockpit at quarters, the sick berth), their work an
   evolution on each man by his hurt, the lightly hurt back on the bill in days and the
   badly not; **the needs of M7b meet their ends** (hunger and thirst to sickness and
   death, fatigue to collapse) as M7b's §20 left them; the butcher's bill in the log after
   an action, the sick list in the morning report; `the surgeon`, `the sick list`, `the
   wounded` as readings and `where is the surgeon` answered. Disease as a thing of its own
   is M8's, the hooks left.
4. **A station holder hurt, at parity (§16a; the owner's note 7).** A person at a station
   is hit as the men at his part are (the quarterdeck the most exposed place); his hurt
   comes to the station as an urgent line of his own; what he may do is the same for a
   model and a human: keep the deck (his words carry, his orders go, every sample saying
   his state), give the deck and go below to the surgeon (the officer or the next in the
   bill taking it as the handover has it), or carry on hurt until he collapses by the
   needs' rule; a holder killed ends his person's station as a death does (the harness
   tells the model in words, writes it in the journal and stands the station down with the
   reason; no model moved to another person by the game; the player at the prompt likewise
   loses his person and the scenario continues by 74's roads or ends; the deck passes by
   the bill). 67's seats and 58a's deltas as they stand; the fairness is the rules'.
5. **The marines and the small arms (§11; the owner's note 3).** The marines a division of
   the muster with their own officer and sergeant, **their kit by nation and period as
   data** (the musket and bayonet, the sergeant's halberd or pike, the officer's sword; the
   French with more soldiers and sharpshooters in the tops; the weapon's kind at least, not
   intensely detailed; in `data/nations.yaml` beside 71's habits or a file of their own,
   the ship files naming the detachment through the generator), their duties in the day
   (the sentries at the cabin door, the spirit room and the gangway; the guard; the drill)
   and at quarters by 70's bill (the poop and the gangways, the tops as marksmen by the
   captain's book, the boarders' backbone, the guard on the prisoners); within musket shot
   they **fire at the men on a near deck** by volley or at will, the hits on the men at
   the parts exposed (the quarterdeck's officers and helmsmen first), and are fired at in
   turn; the ship's company's small arms (cutlasses, pikes, pistols, tomahawks) served out
   to the boarders by the bill; the orders in the dialect (`marines to the tops`, `marines,
   fire by volley`, `serve out the small arms`).
6. **The fight on deck (§11).** A boarding won or repulsed, a deck contested, resolved in a
   few steps with cover, numbers, arms and temper on each side, the marines' volleys and
   the guns' grape counted into it, the losses written to the muster; `boarders away`
   (refused by 70) and `repel boarders` as the orders; the ships brought together (the
   helm, the grapnels, the yards locked) as §11a's evolution so that the fight has a
   ground, **the capture that follows a deck won left to 74** (the state `struck` by the
   boarders' hand, as a strike by morale, is this package's; the prize crew and the
   prisoners are 74's); 70's morale read and written by the fight.
7. **The doctrine of it, in data.** The rules captain's boarding (when he boards and when
   he repels, by the odds and his role), his pumps (when he mans and spells them, when he
   lightens the ship, when he gives her up), his damage control's priority (the leak
   before the rigging, the rigging before the guns, by his state); the captain's books
   written again at the transitions as 58b's rule has it.
8. **The stations, the director and the readings.** `the well`, `the damage report`, `the
   pumps`, `the sick list`, `the butcher's bill`, `the marines` as readings; the events and
   tripwires (`the well rising`, `the pumps gaining`, `a man killed`, `boarders`); the
   director's forms after `WORLD_ORDER_FORMS` (a leak found, a man taken ill, the marines'
   officer down) with their doubts; the harness's samples at a hurt holder's station; the
   truth showing every ship's water and her muster.
9. **Truths and records.** §15's and §17's truths (a shot hole below the waterline fills
   the well at the rate the hole and the heel give and the pumps hold it with so many hands
   and not with fewer; the carpenter plugs it in the time the bill says; a ship that
   founders does so with the log saying when the pumps lost; the Horta grounding replayed
   with the pumps and the carpenter instead of the stopgap gives the same tide and a repair
   that takes hands and hours; a broadside's casualties are men of the muster, named where
   named, and the gun's crew short by them works the gun slower; the surgeon returns the
   lightly hurt in days and not the badly; a hand dead of thirst with the water foul and no
   port, the log explaining it from the needs' lines; a marine's volley at pistol shot
   fells men on the quarterdeck; a boarding against the odds repulsed and one with the odds
   carried, the losses in both musters; a holder hit at the captain's station told so and
   keeping the deck or going below at parity, by the test's two roads), numbered from the
   first after 72's; the first action replayed with the marines and the surgeon in it and
   what changes said; a scenario of a leak and the pumps; spec §11, §13 to §17 "as built";
   the Harness (a holder hurt); a chapter of the primer (the well, the pumps, the carpenter,
   the surgeon, the marines); the director's library; the tuning notes (the design or its
   pointer, each item, the figures and sources, what moved and its proof, the pins old
   beside new, found on the way, decisions, the suite as run); the fast tier, the slow tier
   of the touched files, the whole slow tier when the machine is quiet, the pace tests
   alone and last.

**Not built here:** the prize, the prisoners and the captive (74); the far fight (74); the
damage-control catalogue filled out and the boarders' drill (77); disease as its own system
(M8); the cold (§26, deferred). **The head rules bind** as the briefs before have them: no
model identifier; nothing under `docs/agents/consent/` touched; a world order never shown as
sent; the ship files through the generator with sources; the pins re-measured only where a
change moves them, old beside new, proven by bisection (the Horta grounding's replay and
the gale trials may move by the water's rule: say which and why); never a test skipped,
disabled or quarantined; realism, not pacing (a man's wound and a ship's leak take the time
they took); the physics read and not changed.
