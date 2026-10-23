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
| 70 | Fable | The combat core: the quarter bill and work in action, guns as parts, the gunnery's cycle, the hit model with heel, roll and the sea, damage as state, morale and the strike, the fighting book; the first armament and truths; the figures' sources (spec §7 to §10, §8a) | approved and launched 2026-10-23 (Fable, in a worktree off `b4f91ef`), after the one whole suite on the merged tree of 68, 58a, 67 and 58b |
| 71 | Fable | Signals and the voice between ships: colours, the private signal, the hail, the lights and the bell, the signal hoisted and read; the books' shape for any nation and the first books of Britain and France (spec §1 to §6) | after 70, or beside it if the owner's usage allows |
| 72 | Fable | The naval system: the squadron as a genuine set, the formations and station keeping, the squadron's book, the regimes and the nations' knobs, the business following the player's ship (spec §21 to §23) | after 71 |
| 73 | Fable | Water, damage control, health and the fight on deck: leaks and the pumps, the carpenter and the surgeon, the muster's states, the marines, the fight on deck, a station holder hurt at parity (spec §11, §13 to §17) | after 70 |
| 74 | Fable | Prizes, the strike and what follows, and the far fight; the consent revision for adversarial seats drafted with it (spec §11a, §18 to §20, §29) | after 70 and 73 |
| 75 | Opus | The ships: the *Indefatigable*, the *Prince de Neufchatel*, the 74; every file's armament, quarter bill and marines from 70's shape | behind 70 |
| 76 | Opus | The signal books built out from 71's baseline | behind 71 |
| 77 | Opus | The gunnery's and the fight's evolutions from 70 and 73; the damage-control catalogue | behind 70 and 73 |
| 78 | Opus | Sight across land; collision; fine control of the sails and the gybe as an evolution | where the sailing wants it |
| 79 | Opus | The regimes from 72; the chart's Mediterranean block | behind 72 |
| 80 | Opus | Prizes and the continuation from 74; the consent revision's package if 55 has closed | behind 74 |

The M7b work wrapped up alongside: 58a, 58b and 67 merged (2026-10-23), the one whole suite
on the merged tree the lead's; the lead's playtest of 58b's gale book (its two trials
expected failures until it); the owner's decisions listed in 58a's, 58b's and 67's
as-merged records; 51, 60, 61, 63, 64, 65 and 69 on the books in `M7b-WorkPackages.md`; 55
deferred until testing begins in earnest.

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

