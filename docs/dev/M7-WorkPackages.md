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
that wave (**and granted for every builder, Fable or Opus, on 2026-10-27**, after package
73's first run was lost with the machine's rebuild: a builder pushes its worktree branch to
`claude/pkg-<n>` after each commit as a safety net, never force-pushed, nothing merging from
it without the lead's review); the lead fetching, reviewing and merging as now, and running one whole suite on
the merged tree). The lead's own work (the six-on-six measure, the gate document, the
merges, the records, the short plays) is no package. **The suites, from 2026-10-28:** a
builder runs the fast tier once on its final tree and the slow tier of the files it touched,
and after a mend reruns only the mended test's file (and the pace tests when the mend
touches a per-tick path), never a whole tier again; **the whole suite on the merged tree is
the lead's, run in the cloud by the whole-suite workflow** (`.github/workflows/
whole-suite.yml`: the slow tier in six shards, the pace tests alone after, some twenty
minutes) at every merge, so that no builder spends seventy minutes of the shared machine
watching dots (the owner's word). The usage may run to the week's limit
on these packages; that is the owner's choice.

## Waves

| # | Who | Package | Status |
|---|---|---|---|
| 70 | Fable | The combat core: the quarter bill and work in action, guns as parts, the gunnery's cycle, the hit model with heel, roll and the sea, damage as state, morale and the strike, the fighting book; the first armament and truths; the figures' sources (spec §7 to §10, §8a) | **merged 2026-10-24** (`80f64f7`); the record below |
| 71 | Fable | Signals and the voice between ships: colours, the private signal, the hail, the lights and the bell, the signal hoisted and read; the books' shape for any nation and the first books of Britain and France (spec §1 to §6) | **merged 2026-10-24** (`142b739`); the record below |
| 72 | Fable | The naval system: the squadron as a genuine set, the formations and station keeping, the squadron's book, the regimes and the nations' knobs, the business following the player's ship (spec §21 to §23) | **merged 2026-10-24** (`29b538b`); the record below |
| 73 | Fable | Water, damage control, health and the fight on deck: leaks and the pumps, the carpenter and the surgeon, the muster's states, the marines, the fight on deck, a station holder hurt at parity (spec §11, §13 to §17) | **merged 2026-10-28** (`ec56664`; the first run lost with the machine's rebuild of the 24th to 27th, relaunched off `7da0c0e`); the record below |
| 74 | Fable | Prizes, the strike and what follows, and the far fight; the consent revision for adversarial seats drafted with it (spec §11a, §18 to §20, §29) | briefed 2026-10-24 (below), for the owner's approval; **runs after 84 and 82** (decision 52) |
| 75 | Opus | The ships: the *Indefatigable*, the *Prince de Neufchatel*, the 74; every file's armament, quarter bill and marines from 70's shape; **the ship's sub-types as fits and roles the scenario editor selects and customises in their reasonable degrees** (armed and unarmed, by rig, hull and role: the armed Indiaman, the revenue cutter, the privateer; the owner, 2026-10-24) | briefed 2026-10-28 (below) for **the owner's own local session** on `claude/pkg-75`, from the head after 86 is merged |
| 76 | Opus | The signal books built out from 71's baseline | behind 71 |
| 77 | Opus | The gunnery's and the fight's evolutions from 70 and 73; the damage-control catalogue; the fillers as posts (from 75); Portsmouth's Ordnance block in the magazine's table (79b's finding: the Gun Wharf issuing at Spithead under the Regulations of 1806) | behind 70 and 73 |
| 78 | Opus | Sight across land; collision; fine control of the sails and the gybe as an evolution | where the sailing wants it |
| 79 | Opus | **Split 2026-10-29 (the owner):** 79a the regimes filled out and sourced; 79b the Channel's east block (`channel-east`, the Wight to Dunkirk); 79c the Mediterranean west (the Strait to Cartagena and the Balearics, with its research pass for the period's pilots); 79d the Gulf of Lion and the Tyrrhenian (Toulon, Corsica, Sardinia, Elba, Naples); Sicily and Malta, and the eastern basin, later blocks | **79a and 79b merged 2026-10-29** (the records below); **79c and 79d approved 2026-10-29 (the owner); 79c launched 2026-10-29** as an Opus sibling session on `claude/pkg-79c`; **its research pass (step 0) merged 2026-10-29** (`38b0145`: fifteen texts of both basins under `docs/references/pilots/`, the Admiralty's meteorological tables as page images, the pass's report in the tuning notes; Gallica, the BDH, HathiTrust and Europeana refusing with their own pages, the Archive answering everything); **79d launched 2026-10-29** from it as an Opus sibling session on `claude/pkg-79d` **and merged 2026-10-30** (the record below; the four packages of 79 done); **79c merged 2026-10-29** (the record below; its block ruled two regions at the builder's report of 57.5 MB in one: `mediterranean-west` the Alboran, Málaga to Cartagena and Barbary to Oran, 5 W to a tile column at 0.05 E, and `balearics`, the Balearics with Algiers, thence to 4.5 E; every tile written, the numbering one package's); **79d's Gulf ruled two regions the same day** (`gulf-of-lion` 3 to 7.73 E and `ligurian-sea` 7.73 to 11 E, with `tyrrhenian` within the rule: three regions in the package; the Gulf's south bound to 40.56 N to meet `balearics`, so no open water between the blocks answers nothing; a port's nation allowed a dated form, `{nation, since, until}` by 79a's form, read for the world's date, for Genoa's annexation of June 1805, the smallest change in the ports' readers, 84 told); none depends on 84 |
| 80 | Opus | Prizes and the continuation from 74; the consent revision's package if 55 has closed | behind 74 |
| 82 | Fable | **The boat as a vessel, and the player aboard another ship** (M7b's 63 and the heart of 51, brought forward by the owner, 2026-10-24): the followed ship in place of the given one and a world with no player's ship; the player and any person aboard another ship, moving between ships by the boat, by boarding or by capture, the seat following the person, 68's refusal lifted; the boat crewed and sailed, towing by an oar force; the replay of a station on another ship | briefed 2026-10-24 (below); **re-briefed after 83's design** (decision 52), runs after 84; Fable whole (the owner, 2026-10-29), **the re-brief carrying the ships session's principles for a hull and a ship** (`docs/design/Build-Ships.md` §5.0's twelve, the ladder of evidence with its marks, sourced points over the rule, the drawing never changing how a vessel sails, nothing invented; the boat a ship file written by a module of `tools/ships/` through `tools/gen_ships.py` with her shape keys and port triples as the ships are, never by hand), so that the boat is built to the new standard |
| 83 | Fable | **The one-world study** (decision 52): the design of a world the player is one part of, many crewed hulls in one World, the person's coarse acts anywhere, the leaders' roles left room for; the migration in steps that keep the suite green; the cost in pace and pins; a brief for 84; no code | **merged 2026-10-27** (`docs/design/Design-OneWorld.md`; road A recommended; 84's draft brief below) |
| 84 | Fable | **The one-world refactor**, on 83's design: the promotion builds a hull and not a World, the ports, people, things, markets, business, weather and the director's hand the world's once, every crewed ship with her own people, places and log; 82 folded into or behind it as 83 says | briefed by 83 (below); the eight decisions taken (decision 53); **steps 1 to 10 merged 2026-10-28/30** (steps 1 and 2 at `d9dba1f`, steps 3 to 10 from the sibling's `claude/pkg-84` after it; three pins moved at step 6 for the one clock, bugs of the two clocks; **the owner's acceptance test passes whole as truth 7-200 at step 4**); steps 5 onward continue in the sibling |
| 85 | Fable | **The orders, the primer and the library reviewed for a model reader** (the owner's notes 3 to 6 and the officer's five points): the primer and the library made general and in-world, every scenario-, book-, ship- or build-specific reference redacted and kept elsewhere, with a test that guards it; the date and the war's state readable; the voice's one grammar; the stand-by's words; the action's severities; **and the documentation whole** (the owner, 2026-10-29: "might as well go all the way": `docs/` read for completeness and refinement with the same pass, item 8 of the brief) | briefed 2026-10-27 (below), widened 2026-10-29; after 84's last step; 87 follows it |
| 86 | Opus | **The owner's local work folded in** by the review's plan (`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/review-of-the-local-work.md`): the practice-and-resupply package and the pivot gun with the listed edits, the free intents tightened, the hail fix with its pins proven, station keeping by name and kind limited to sails in sight, the records recast; the whole slow tier and the convoy's stall reproduced | **merged 2026-10-28** (`cd97ce7`); the record below |
| 87 | Opus (the owner, 2026-10-29; Fable before) | **The warrant officers' stations** (the owner, 2026-10-27): the gunner, the surgeon, the carpenter, the sailmaker and the boatswain as stations a person or a model may hold, each with a domain of orders and readings of its own and its peculiarities (the gunner's magazine, filling, practice and the batteries' service from 70 and 86; the surgeon's sick list, the wounded and the cockpit from 73; the carpenter's well, leaks, plugs and spars from 73 and 77; the boatswain's rigging, the spares, the hands' work and the bill from 77; the sailmaker's sails, the holes and the sailroom from 70's damage and 65's work in its place), a brief and a station line for each, a reason to be stationed by the milestone's end; the equal-reach rule and the handover as every station has them | to brief after 85's pass over the orders, the primer and the docs is merged (the owner, 2026-10-29), and after 77; the brief fixes the pattern on the gunner and the four follow it |
| 88 | Opus (the owner, 2026-10-29; Fable before) | **The captain's pass of M7**: the commodore's recovery when aback with no way and no tack while the hands are at a shortening (the convoy's stall, 86's finding; truths 7-152 and 7-153 move with it); 57's offing's tack among islands with no room to wear (the station-gale trial's expected failure lifted); 72's near station law read against 58b's; the colours held once shown before an enemy (71's flicker, if 85 has not taken it) | after 84; to brief, each item with the symptom, the rule as it stands, the rule as it should read and what proves it, the moved pins by bisection (the owner, 2026-10-29) |
| 89 | Opus | **The held gauges' water** (79b's finding): a held gauge enters the tide's blend for the positions within its own block's bounds alone, so that the Channel east's six, Biscay's, Portugal's and the islands' gauges give their water its own tide and no position west of 1 W reads anything new; the master's epitome's rises by the same water; the proof that no recorded passage's digest moves | briefed below (2026-10-29); **approved and launched 2026-10-30** (the owner) as an Opus sibling session on `claude/pkg-89`, with the Mediterranean's held gauges of 79c and 79d now among its cases; for the owner's approval; independent of 84 |
| 90 | Opus (the ships session) | **The tartane and the xebec** (the owner, 2026-10-29): the Mediterranean's two lateen hulls on 79c's water, the tartane the third reference vessel of decision 11 (one raking mast, the lateen mainsail, the jibs on the long bowsprit, the small mizen, the boat in tow), the xebec with the lateen on three masts and her sweeps, each as a trader or fisherman and as a corsair or the King's by fits and roles, built to Build-Ships.md §5.0's principles and the ladder of evidence from Roux's and Tofiño's plans and the pilots 79c lays down, with the lateen handling B3.1 gives (worn, not tacked; the yard dipped round the mast); the regency's cruisers as a role with their doctrine; inside milestone 7 | the ships session's next window after 75 closes, on 79c's block; to brief by the session in its plan's form, for the lead's gate |
| 81 | Opus | The viewer's action, **from the hull 75 draws**: the guns drawn in their ports with their movement, a muzzle flash and a smoke plume over a few seconds at each gun's firing, the smoke lingering to leeward; the damage as the viewer's present honesty draws it (the owner's first action, 2026-10-24); the ports drawn from the files' port triples and `port_size_m`, and a triple within `OVER_THE_RAIL_M` of the rail at its x a gun place over the rail, not a port (from 75's design of the 74, 2026-10-29) | after 71 and 75's hull; when the owner likes |
| 91 | Opus | **The viewer's light and air** (the owner's references of 2026-10-29, decision 57): the ship's own lights warm and distinct at night (the stern lantern, the top lights and the binnacle 71 already hoists, each a glow on the faces near it); the scene's light by the hour and the sky (the sun's altitude and azimuth from `core/moon.py`, the weather's cover and visibility: a gradient sky and sea, the faces tinted by their side to the light, dusk's warmth, night's dark with the lights alone, haze by the visibility); a lively telltale at the masthead and a waving ensign, canned but driven by the apparent wind the physics already gives (direction, a flutter whose rate and amplitude follow the speed), animated between snapshots; all in the present SVG viewer, stylesheet-driven, drawing only, nothing of the world read that the readings do not give | after 81 and 75's hull; when the owner likes; the two reference pictures stay with the owner (another game's work), described in the decision |
| 92 | Fable | **The career study** (decision 58): the design of a career the player takes up under the world's own rules, in 83's shape and no code: the state as the frame of the naval and the economic systems, tasks from the world's needs, the lead actor a station, standings as interest and character, progression in the period's currencies, the ellipsis between voyages, a closed economy, the decision chain's ceiling, every change an act; a design document and the first career package's brief for milestone 8 | after 85's review; the building in milestone 8 |

The M7b work wrapped up alongside: 58a, 58b and 67 merged (2026-10-23), the one whole suite
on the merged tree the lead's; the lead's playtest of 58b's gale book (its two trials
expected failures until it); the owner's decisions listed in 58a's, 58b's and 67's
as-merged records; 51, 60, 61, 63, 64, 65 and 69 on the books in `M7b-WorkPackages.md`; 55
deferred until testing begins in earnest.

**For package 77's brief, from package 86** (the review of the owner's local work, section
5; his debrief: practice a stopgap to rewrite or redesign as judged): `heave_mark`, dumb
show and the notional mark are the gunnery's evolutions in a first, stopgap form, which 77
takes over or redesigns; the gunner, his crew and the quarter gunners made posts that
compete for hands (86's filling party is read and never moved, the build's decision 5);
truths 7-162 to 7-166 kept or replaced by its own, each with the old figure beside the new.

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

### Package 72 as merged (2026-10-24)

Merged `--no-ff` from the builder's worktree (ten commits on `356e7ba`, the design note
first; 53 files, ~6,800 lines) with no conflict; ruff clean; the lead's sweeps clean (no
consent file, no ship file, no physics file touched; no model identifier). The builder ran
the fast tier whole (3,631 passed, two failed in the pictures' API-door test under four
workers, passing alone, not its own), the whole slow tier (3,964 passed, 11 expected
failures, three failed, all its own and mended after it, their three files rerun, 88
passed) and the pace tests alone (10 passed after truth 7-159 was put in truth 51's form);
**since three mends followed its whole slow tier, the lead ran the whole slow tier and the
pace tests on the merged tree after the merge: 3,973 passed, 11 expected failures, 2 skipped, none failed; the pace tests 10 passed**. Built as briefed,
generously: **the squadron's shape designed and written first** (`docs/design/
Design-Squadrons.md`); **the set** (`freesail/world/squadrons.py`: a commander, the members
in their order of sailing, a kind, a formation and interval, divisions, stragglers, a
rendezvous, a book, a regime; joined and left by the scenario's `squadrons:`, the director's
forms, the commander's signals and the world; writing 71's `under_orders_of` on every
member so that every reader 71 built works unchanged); **one brain at far detail** (each
member's far body on a station leg laid each minute in the commander's frame at the set's
pace, the slowest member's; a promoted member's captain `in company`, a state of the
machine with its doctrine in every role's file, keeping station by the near order; the line
kept through promotion); **station keeping** a held order of the navigation
(`freesail/orders/station.py`: `keep station two cables astern of the flagship` and its
kin, the flag's course and a lead point three cables ahead, shortened a step a glass) and
**succession by the wake** inside a set (71's three minutes kept outside one); **the
books** (`data/squadrons/convoy.yaml`, `squadron.yaml`, `blockade.yaml`: rules of signal,
order, formation, goal and rearm, run once a minute on whichever rules captain holds the
commodore's station and silent under a model, who commands by `make the signal`; the
escort's cover and the far cut-out at hailing distance; the commodore's chase and recall);
**the regimes in data** (`data/regimes.yaml`, eight regimes with knobs and sources; a
`naval:` block for every nation; `freesail/world/regimes.py`: in ordinary, commissioned
with a delay, the sortie when no enemy man-of-war has been in the offing for an hour and
the wind is under a fresh breeze; the intent `blockade <port>` keeping the port's new
`blockade_station`); **the business** drawing convoys, blockades and ships in ordinary by
the knobs and **following the player's ship across the regions' edge**, carrying a set over
whole; **the weather's seasonal bound** (R-39) built under a switch and off (`weather_bound:
seasonal` on the scenario; no recorded scenario sets it, truth 7-158); readings, events,
channels and the director's forms (`squadron:`, `squadron "X": ...`, `convoy:`, `ship "X":
in ordinary at`, `commissioned for`); three scenarios (the convoy of six with a privateer
schooner, the Brest blockade blown off to Torbay by a scripted gale and a French frigate
slipping out an hour after the wind fell, the Channel squadron promoting in line); **the
pace measured** (the convoy of six at far detail alone 544 to 551 ticks a second, under the
default cap 318 to 328; truth 7-159 at 581 against the build machine's floor of 500, truth
7-160 at 318 against the crewed floor of 60; the owner's baseline untouched); truths 7-152
to 7-160; spec §21 to §23 as built, Harness §21e, primer chapter 24, the tuning notes.

**Taken another way, accepted:** the far cut-out stops at hailing distance, not pistol shot
(74's far fight takes it on); the land-avoiding planner (61) left to 78 with the reason
(the convoys and the blockade work in open water; Plymouth's track to sea moved off the
land as data, by Cawsand Bay and the Rame, a frigate from the west having gone through the
Four onto the Plâtresses in 28 minutes under `blockade Brest` on the outer road: a test
case for 61); the bound taken only as far as the squadrons' gale wanted (a scripted low
wants no bound), Iberia's drift left to 79. **Pins:** none moved, no bisection needed (the
bound off, the planner's graph not built, Plymouth's track read by no recorded passage,
truth 7-145's 180 seconds kept). **Found on the way, fixed:** the near `keep station`
order's first form swung her across the line and crept without turning her; a promoted
ship's world rebuilt the scenario's sets for want of the ships; `blockade Brest` on the
outer road led through the Four (the chart has two Black Rocks); YAML reads a bare `on:`
as true; the business's hourly draw counted the sets against `most_ships` and stopped
drawing; a brainless member's row had no business; the director's `commissioned for`
example wanted the forms test's list. **Found, carried:** the rules captain on a station
under the land stands off forty miles in a rising onshore wind (his offing); the
gradient-wind rule flattens a scripted low's surface wind far from its centre; a brainless
member is never promoted under any cap (give her an intent to promote her); the pictures'
API-door test times out beside four workers running long truths (passes alone; not this
package's). **Decisions for the owner:** the seasonal bound stays under its switch until
judged on a passage of days; the regimes' knobs are judgement (a sortie when the offing is
clear fifteen miles or the blockade station, the wind under 22 knots, a commission in two
to five days); merchantmen stay brainless and far under every cap.

### Package 73 as merged (2026-10-28)

Merged `--no-ff` from the builder's worktree (twelve commits on `7da0c0e`, the design note
first, every commit pushed to `claude/pkg-73`; 96 files, ~10,600 lines) with no conflict;
ruff clean; the lead's sweeps clean (no consent file; the ship files regenerated
byte-identical; the four physics files touched only by state hooks rule 1 wants: the
metacentric height read as she floats, the held states of a foundered or grappled hull, a
preventer taking a parting line's strain). The first run of this package was lost with the
machine's rebuild of 2026-10-24 to 27; the second rode through a restart on the 27th with
its disk intact. The builder ran the fast tier whole on its last tree (3,689 passed, two
failed: the pictures test under load, passing alone, and its own stiffness line, mended and
its file rerun), the slow tier whole on that tree (334 passed, none failed, 11 expected
failures) and the pace tests alone (9 passed, truth 7-159 at 481 against 500 on this loaded
machine, as 72's own first run had it; not re-pinned); after them one line of `water.py`
and the notes changed. **The whole suite on the merged tree in the cloud (run 2 of the
whole-suite workflow, 40 minutes): every shard green but truth 7b-108's harbour line unseen
on the runner (an environment's failure, mended since by a flush), the pace job informative
with 7-159 at 491 on a shared runner.** Built as briefed, generously:
**the water in the ship** one quantity the keeper sums each tick (shot holes by the orifice
law, the ground, the seams working in a roll, the sea shipped unless battened, the
director's causes), the well's depth and the carpenter's feet, **the pumps** the ship
file's through the generator as the hands' work by spells, the weather's water pumped
every glass unasked, **the free surface** taking the metacentric height, **foundering**;
**damage control and jury work** as evolutions competing for hands (the plugs by the hole's
place, fothering, fishing, preventers and slings, the rigging set up, a mast cut away, a
jury mast, the owner's `reeve new lines`), the damage report naming everything; **the
muster's states** (hurt, wounded light, grave or invalid, sick, killed), the surgeon and his
mates as posts with their queue and courses, the sick list at eight, the needs' ends, the
burial, the morning report and the butcher's bill; **a station holder hurt at parity** (his
own urgent line, the deck kept or given, the grave wound's collapse into a carried-below
stand-by, the judgement that ends the station, the command passing by the bill); **the
marines' kit by nation as data** and their musketry within musket shot of a near deck;
**the fight on deck** (`lay her aboard`, `grapple her`, `boarders away`, `repel boarders`, a
round a minute by strengths, carried or repulsed); **the doctrine in data** read by the
captain's own minute; the readings, events, forms and samples; the leak scenario; truths
7-172 to 7-184; spec §9, §11, §11a, §13 to §17 as built, Harness §21f, primer chapter 25,
the tuning notes.

**Taken another way, accepted:** the marines stand at 70's carronades at quarters until
ordered to their muskets; the grapnels hold from the throw; the doctrine's standing orders
replaced by the captain's own minute; the wounds' draws on a health stream of their own so
70's and 71's gunnery runs as it did. **Pins:** the first action's strike 11:12 to 11:43,
the mover the small arms served out by both captains on entering the action (bisected,
kept for realism, `board_odds: 0` turns it off per role); the trade-stranger trial one line
(the butcher's bill's "nobody hurt"); the lee-shore trial and gate 5a's day moved under an
early keeper and are back to their pins exactly after two mends the trials themselves
found (the pumps' crews kept all day by the weather's water; a sound ship in a blow passing
the free surface's tenth). **Found on the way, fixed:** a man hit at tick 0 taken as hit
now; a person marked dead before the lookups never told and the command never passed;
`man the boats` hinting `man the pumps`; a foundered ship accepting orders of work; a
privateer whose boarding was refused standing off and never firing. **Found, carried:**
the pictures test and the fingerprint test under load; truth 7-159's pace on a loaded
machine. **For package 84:** the places the work assumes the player's ship the only crewed
one are listed in the builder's report (the small arms' and boarding's `_own_id`, the
founder's report to the parent, the keepers one per World), all of the kind step 1's
delegation handles.

### Practice and resupply as merged (the owner's local work, folded in by package 86, 2026-10-28)

**Built locally by the owner between packages 72 and 73** (on `main` of a local repository
taken from `2774be3`, nothing pushed; `docs/design/Build-PracticeAndResupply.md`, the
owner's two proposals of 2026-10-25 approved, and the pivot gun and the privateer schooner
before them), with six fixes after his playtests of 2026-10-26 and 27; reviewed for the lead
(`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/review-of-the-local-work.md`), the
door fixes merged as the plan's first step (`59c4ca4`), **the rest folded in by package 86
on top of 73** on its own branch: the ordnance package at `5b01fdf`, the free
intent, the hail and the station fixes taken as he made them at `33e852c` and tightened at
`35cf088` and `d479b4f`, the records after. Every shared file was merged hunk by hunk over
the line's, never copied over it; the new files whole; `tools/gen_ships.py` merged by hand
with 73's pumps, shot plugs, small-arms men and boarders, and the ship files regenerated by
running it (the regenerated files equal a text merge of his files over 73's but for two
comment placements the text merge could not settle). **Built as he designed it:** the
magazine by gun kind and calibre with the powder below in barrels and the gunner's filling;
powder and shot taken in at eleven ports by the hoy, issued free and vouched by the
Ordnance at Plymouth and Gibraltar to a King's ship of Britain and sold by the merchants to
the rest, the galley fire out as a state, the gunner's account a paper; practice at a cask,
at a notional mark and in dumb show, the drill and the allowance for exercise; the shot into
the sea; the scenario `exercising-the-great-guns.yaml`; the pivot gun and the privateer
schooner, PROVISIONAL. **His truths keep their numbers, 7-161 to 7-171** (73's are 7-172
to 7-184; nothing renumbered). **The review's edits:** the pivot gun's arc made per gun
(`arc_deg` in the ship file, `guns.pivot_arc`; the schooner's 60 to 140 written by the
generator, the old constants a default only); the stale `schooner_armament` docstring and
the stale comment at the filling's call in `action.py`; the fillers' stopgap named in 75's
and 77's briefs; the duplicated word helpers gone (`guns.count_words` and
`guns.seconds_words` for `_cardinal` and both `_seconds_words`, `parts.kind_rank` for
`gunnery._rank`); `Papers._merge` reading its own catalogue's path; the docstring slip in
7-164 (the chasers' 56 s their best); the tuning notes' line naming a model reworded; the
owner's local hashes recast (his commits are on no branch of the project: "the local
baseline" for the tree he measured before, the fold-in's `5b01fdf` for the work). **Taken
with a judgement of the fold-in's:** the privateer schooner's quarter bill given 73's
small-arms men and boarders (eight and twenty-six of her forty, after the cutter's six and
twenty of thirty, PROVISIONAL for 75) where the merged generator would have written none;
the readings registered after 73's damage readings. **The fixes tightened:** the crewed
captain lays no plan for a free intent and heaves her to once on his passage, the ship
keeps her service's role and doctrine under it, the warning says she is lain to; the hail's
`commands` branch the player's ship's alone; a station by kind only on a sail in sight, and
'brig' no brig-sloop. **Pins:** the unit counts on the merged tree, the old figure beside
each: 98 evolutions (97), 11 papers (10), the officer's handover budget 20,500 (20,000;
12,052 tokens at the seat); no recorded passage moved: the slow tier of the touched files and the captain's trials 155 run, 147 passed, 8 expected failures, and the hail fix bisected all the same (truths 7-140 to 7-158 the same lines and digests with the gating reverted but 7-143's hailed crewed ship, unasserted); two pace tests under the floor on this machine before and after alike. **The convoy's stall**
reproduced on the line since 72 (the same on `2774be3`, `e7a3ee8`, his tree and the fold-in) and left for the lead: not the near station order (the merchantmen are brainless and far) but the commodore's own brig, aback with no way from about 10:20 after a short-handed tack and nothing in her captain's rules to bear her away, the far convoy held to her pace; she pays off at 10:45 when the book takes in her after sail. A mend moves truths 7-152 and 7-153 (the tuning notes, package 86). **Records:** spec M7 §4, §7, §8 and §21, M7b
§4's ships, Harness §21d, §21e and §21g (his §21f, renumbered after 73's), primers 14, 20
and 22, the four design notes, the tuning notes (his sections and package 86's), the
briefs of 74, 75, 77 (below the waves) and 82. **Left out:** his four consent records, his
copy of this file, and nothing of `tests/test_pictures.py`. **The builder's suites:** ruff clean; the fast tier on the final tree 3,891 passed, 1 failed (the pictures test, this machine's Chromium, before and after alike); the slow tier of the touched files and the captain's trials 147 passed, 8 expected failures; the pace tests 8 passed, 2 under the floor before and after alike. **The whole suite on the merged
tree is the lead's in the cloud.**

### Package 86 as merged (2026-10-28)

Merged `--no-ff` from the builder's worktree (six commits on `e7a3ee8`, pushed to
`claude/pkg-86`; 92 files, ~15,600 lines) with no conflict; ruff clean; the lead's sweeps
clean (no consent file, no physics file, no model identifier; the ship files regenerated
byte-identical). The builder took the owner's tree as a commit over `2774be3` in a scratch
index and cherry-picked it onto the line without committing, so that every shared file was
merged hunk by hunk over 73's version and nothing copied; the review's edits made (the
pivot's arc per gun as an optional `arc_deg` of the ship file, the stale docstring and
comment, the duplicated helpers replaced by `guns.count_words`, `guns.seconds_words` and
`parts.kind_rank`, `Papers._merge` reading its own path, the 7-164 slip); the owner's
truths 7-161 to 7-171 placed before 73's with the build machine's figures beside his; the
unit counts recomputed with the old beside the new (evolutions 98, papers 11, the officer's
handover budget 20,500); the three fixes taken as he made them and then tightened as the
review asked (the crewed captain under a free intent lain to once and planning nothing,
the ship keeping her service role; the hail's `commands` branch the player's ship's only;
station keeping by kind among sails in sight, hyphen-aware); **no recorded passage moved**
(the hail's gating reverted in a copy and 37 logs compared: identical but for one unasserted
scene); the records recast into the line's files with the one model-naming line reworded;
the builder's fast tier 3,891 passed and one failed (the pictures test's threshold on this
machine), the touched files' slow tier 147 passed, 8 expected failures; **the whole suite on the
merged tree in the cloud (run 3 of the whole-suite workflow, 41 minutes): every shard green
but truth 7b-108's harbour line unseen on the runner (mended by the flush at `8db8b9a`),
the pace job informative with 7-159 and the gate day under the build machine's floor on a
shared runner, as before.**

**Judgements, the lead's:** the privateer schooner's eight small-arms men and twenty-six
boarders, scaled from the cutter's and marked provisional, accepted for 75 to source. **The
convoy's stall reproduced and named, not mended** (`convoy-six.yaml`, no orders; the same
on `2774be3`, the owner's tree and the line since 72): not the near `keep station` order
the study suspected (the merchantmen have no brain and are never crewed) but the
commodore's own brig-sloop, which starts a tack at 10:17 with thirty-one hands while her
book is shortening sail, spends eight minutes and a half in stays, comes out with no way,
is taken aback at 10:30 some forty degrees off the wind under the full-and-by helm, and
lies so until the book's second shortening at 10:45 lets her pay off; the far convoy capped
at her pace lies with her. The mend is the near captain's and the helm's (no tack while the
hands are at a shortening; a recovery when aback with no way, the counterpart of 58b's law)
and it moves truths 7-152 and 7-153: **booked as the captain's pass after 84** with 57's
offing's tack and 72's station law. **Found, carried:** a misspelt port is taken as a free
intent (85's hint); the pace tests on this machine spread 450 to 530 against the floor of
500 before and after the fold-in alike (the cloud's pace job is informative for the same
reason).

### Package 84, steps 1 and 2, as merged (2026-10-28)

Merged `--no-ff` from the sibling session's `claude/pkg-84` (three commits on `e7a3ee8`;
16 files, ~1,550 lines) over 86's merge, with two docs conflicts of the appended kind; ruff
clean; the sibling's fast tier whole on each step's tree and the touched files' slow tier
(its tuning notes, "Package 84, steps 1 and 2"); the lead's smoke of the files both merges
touched; **the whole suite on the merged tree is the lead's in the cloud (the figures below
when it ends).** **Step 1:** every per-ship field of the World (59 of them, `PER_SHIP_FIELDS`)
lives on `world.own`, a `freesail.world.hulls.Hull`, read and written under its old name
through properties, the World's tick, record and submit unchanged in text and order, so
nothing pinned could move and nothing did; the checkpoint's converter reads the old shape
(the three kept saves and a promoted brig's world round-trip to their digests); the
delegation's cost measured at two microseconds of a two-millisecond tick, under the pace
measure's noise (the base and the step alternated on a quiet container, 539 to 653 either
way). **Step 2:** one registry of persons and things on the World with a whereabouts and a
home hull (`Person.hull`, `Person.home`, `Thing.hull`), each company a view of it, hearing
and reach by the registry; a world in which nobody moves is line for line as it was; the
converter reads every older shape. **Found on the way:** `orders._doubt_thing_moved`
unpacking a thing's where into three. The builder's report reached the lead through its
pushed branch and notes, its scheduled-task message carrying only a preamble: sibling
sessions report by their branch, which the lead reads, and the message is a courtesy.

### Package 84, steps 3 and 4, as merged (2026-10-28)

Merged `--no-ff` from the sibling session's `claude/pkg-84` (two commits on the merged head
`8db8b9a`; 55 files, ~5,500 lines added and ~3,600 removed) with no conflict; ruff clean;
the lead's sweeps clean; the sibling's fast tier whole on each step (two explained failures:
the pictures' threshold under load, and the squadrons' succession test whose band was the
old route's phase and not the rule, recast to the rule it states with the old figure beside
the new), its touched files' slow tier running as it reported; **the whole suite on the
merged tree in the cloud (the figures below when it ends).** **Step 3:** the ports split
into `Ports`, the world's (the files, the markets, the stances, the tracks, who is at each
place ashore), and `Dealings`, a hull's (her pilot and his conn, her boat and its errands,
her price lists, her jobs). **Step 4:** the coarse acts on a sleeping hull and the far
brain's port acts: a station on a ship at far detail works every act that wants no
physics through her own grammar (the boat's errands as the port's jobs with the boat's
time, the captain landed at the quay and fetched, the places ashore, a word said and heard
by spot, the free lines, a signal and a hail); `shape a course for <port>` in the far
shape the planner's passage by the ports' tracks and the chart's common tracks, ending at
her anchor; a far body under a held station lying to at her plan's end instead of
vanishing; the far trader at her port selling, buying a return cargo and sailing again
(`transact: true`, decision 53's fifth); the director's `say as` for a person ashore heard
by whoever of any hull is at his place; a kept thing knowing its keeper's home hull.
**The owner's acceptance test is truth 7-200** on the new `data/scenarios/tender.yaml`: the
Amazon at anchor in Brixham road, the Raven her tender asleep the whole day with a fake at
her captain's station, ordered to Plymouth by signal, by the tracks, ashore to a person,
back with the packet, the lugger passed, home within hail. **Taken another way, with
reasons in the design note's postscript:** the Raven asleep from the start (the switch is
steps 5 and 6's), the pilot's track in as the plan's anchor leg (the pilot as a job is
step 5's). **Data:** a coasting track from Torbay to Plymouth in the Channel's features,
used only where a straight line is not clear. **Found on the way, fixed:** `station_world`
ignoring the scenario's crewed cap. **Open for the lead:** the director's lines for a
person land in the player's log as before (the director's-reach step's).

**The whole suite in the cloud on the merged head `5e3f7b5`** (run 5, 34 minutes): lint
clean; the slow tier's six shards 4,246 passed, 3 skipped, 11 xfailed and **2 failed**, both
pinned truths that passed on the previous head `3421829`: 7-154 (the blockade squadron
blown off for Torbay restored its station at 34200 for the pinned 37920) and 7-156 (the
convoy's tack-in-succession gaps `[300, 240]` for the band 300 to 420); truth 7b-108's
harbour line passed with the line buffering; the pace job (informative) missed two floors on
the runner as before (the gates' day 487, 7-159 476 for 500). **The cause, step 4's
coasting track**, which the planner took for every route whose ends reached it, bisected by
the sibling on its own tree the same hour (the known truths' slow tier run after all, on
the merged head) and by the lead on this one; the lead's recast of 7-156 to the rule it
states (`bd220cb`) reverted (`ad041ca`) when the sibling's mend came, since a data change
is no reason to re-pin three figures. **The mend merged `--no-ff` from `claude/pkg-84` at
`ef7b7fe`:** the track withdrawn, the squadrons' and the captains' tests' original
assertions restored, and the far course for a port taking the captain's marks (`shape a
course for Plymouth via the Start`, the intents' `via` of package 45, each headland given
its offing), the land guard's refusal naming the way by marks ("give the way by marks");
truth 7-200's fake reads the refusal in its order's result and gives the way (two refusals
in the day, out and home, each answered). **The lead's judgement:** right as the thing is:
a captain told that the straight course for Plymouth crosses the Start names the Start, in
the words the intents already take, and a model captain gets the same refusal naming what
to say; the record and the acceptance test say so. **The whole suite in the cloud on the
mended head `e38a3e2`** (run 6, 34 minutes): lint clean; the slow tier's six shards **4,248
passed, 3 skipped, 11 xfailed, none failed**, truths 7-154, 7-156 and 7-200 among them at
their pinned figures; the pace tests 10 of 10 on that runner. Steps 3 and 4 stand merged
green.

### Package 84, step 5, as merged (2026-10-28)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `2f81fc1` (one commit over
the lead's `e38a3e2`, brought in at the step's boundary; 8 files, 305 lines added and 45
removed); ruff clean; the sibling's fast tier whole (the pictures' threshold under load the
one failure, passing alone) and the known truths' slow tier with the trials, the crews, the
checkpoint, the business, the brains and the squadrons (the lee-shore trial's digest the
container's difference recorded at step 3, the same on the base); the lead's fast tier of
the touched files; **the whole suite on the merged tree `5949e18` in the cloud (run 7, 45
minutes, one shard's runner slow): lint clean; the slow tier's six shards 4,250 passed, 3
skipped, 11 xfailed, none failed; the pace tests 10 of 10.** Step 5 stands merged green.
**The step:** the ship persists. `demote` is a sleep: her truth and her captain's state into
the far body and the brain as before, her damage summed into the far body's record
(`write_damage`: the killed and the wounded by the muster's hurt, the guns dismounted, the
shot holes and those below the water, the spars wrecked, the sails blown out, the tick she
slept; the far fight's own counts kept, 74's ground), her World kept in the far shape with
the physics off, her company in the one registry, her stores, purse, parts and Rng hers.
`promote` of a ship with a World is a wake (`_to_full` without `make_ship`): the ship she
had, her body given the far body's mirrored truth, her sail set as the far body's word only
where the plan changed it asleep, the brain folded in, no reseat; the woken line urgent
only where a station is seated. A vessel gone from the sea gives up her World and her
people (`release_done`, first in the switch). `crewed_ids` counts the Worlds alive (the far
tick's gate), `crews.crewed` the awake against the cap; a vessel's dict says `crewed` for
awake only and `asleep` apart, so the glass's pinned data reads as before. **Taken another
way, with reasons in the design note's postscript:** the Rng made with her World and kept;
a sleeping company's needs not advanced (a knob for the owner: ticking them without the
routines that serve them would kill her company of thirst); the watch not changed at the
bells while she sleeps. **Measured** (TuningNotes "Step 5"): three sleeping brigs beside
the frigate cost the pace about a thirty-seventh each against a third awake (459 and 490
ticks a second for 530 with their Worlds dropped on the old road); the checkpoint with the
three asleep 704,775 bytes for 704,756 dropped, the growth the log's; the 2 MB bound stands.
**The lead's review, one finding for step 6:** a ship asleep keeps `detail == "crewed"`
(the sibling's tests assert it), so `_promote_and_hail` never gives her the near detail's
every-second tick when she comes within `NEAR_DETAIL_NM` over the cap; before the step an
unseated demote set her `far` and the near level served her. A seated ship was already so.
Nothing pinned shows it; step 6's two-phase tick (the Hull as the container) is where a
sleeping hull's cadence by distance is settled, and the sibling is told.

### Package 84, step 6, as merged (2026-10-29)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `fc43086` (the step `b33e164`
on the lead's `5949e18`, and a one-line correction of its record; 15 files, 1,026 lines added
and 283 removed); ruff clean; the sibling's fast tier whole 3,912 passed and none failed, its
pace tests all but the two container floors (the gates' day 495, 7-159 468, the same two 489
and 453 on a worktree at `5949e18`: the container's, the step costing nothing the measure
sees), its known truths' and touched files' slow tier run to 146 of 362 before the bell mend
with every failure mended or re-pinned and the whole set running again after the push; the
lead's fast tier of the touched files (six files, none failed); **the whole suite on the
merged tree `f99648d` in the cloud (run 8, 48 minutes): lint clean; the slow tier's six
shards 4,250 passed, 3 skipped, 11 xfailed, none failed, the three moved pins at their new
figures; the pace tests 10 of 10.** Step 6 stands merged green. The sibling's own slow set
on the step's tree, reported after (the known truths and the touched files, 148 tests):
146 passed and two failed, the lee-shore trial's digest (its container's known difference)
and truth 7-200 under three workers, which passes alone and passed in the cloud: a
load-sensitive test, the fake at the tender's station lost to the stand-in when its reply
is late under load, carried as a finding into step 7's notes and not mended in step 6.
**The step:** the Hull is the container. A crewed ship is a `Hull` of
the one World in `world.hulls`; the World's per-ship names read the current hull through a
thread-local stack (`World.as_hull`), the followed hull their default, so a door's thread
reads the player's ship while the driver ticks another; the Hull is the façade her systems
and stations hold as their world, every other name of the World's run with her current;
one clock from her making, her own log, Rng, seed, scenario, view of the sail and bell;
another hull's tick is the World's own with her current, a sleeping hull's second a
function over the hull; `CrewedWorld` the builder of a hull's fields and the unpickler's
name, the building World discarded after a rebinding walk; a checkpoint of before converted
at the load. **Found by the step and mended, seven of one class:** shared code that meant
the player's ship read the World while another hull was current (the shadow built as the
enemy's nation; the French frigate's battery with no mark; the colours struck written on
the wrong vessel so her guns fired on a struck ship; the boarding's round on the enemy's
log; a promoted captain judging at his first tick; the building World's sea its own view;
the converters walking a view), each probed against a worktree at `5949e18` and ending alike
once mended. **Three pins moved, for the one clock, old beside new** with the first
differing log line named in the tests and TuningNotes "Step 6": the station-stranger trial
(787 lines, `f8f4e544cc34b86e` to 788, `d56963daf49d566a`: the Palinure answers the private
signal at 9840 s), truth 7-152 (the Friendship in station 5280 to 6420 s after the
Vengeur's bluffed reply at 3480 s) and the trade-stranger trial (`11b8a45bdc8c935a` to
`02313d83240a11d5`: the butcher's bill 17520 to 20220 s). **The lead's judgement:** these
are bugs of the two clocks and the pins were wrong. A hoist is seen when it flies by the
reader's tick, and a crewed stranger's World, on a clock counted from her promotion, stood
hours behind the tick the King's private signal broke out at, so no crewed stranger ever
saw it; a hit's tick was written by the firer's clock, so the bill came early. The one clock
is the rule, the passages now run as the rules say, and the ships' sailing (the states, the
manoeuvres' ticks) stands in all three. **The step 5 finding settled:** a sleeping hull's
`detail` is the sea's word by her distance, far or near, and within the near range her far
body moves every second and her hull mirrors each move. **Noted for a later tidy, not a
mend:** the thread-local stacks are keyed by `id(world)` and never dropped, an empty list
per World made; and the façade's `__getattr__` wraps every World method in the swap, which
the pace figures show costing nothing the measure sees.

### Package 84, step 7, as merged (2026-10-29)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `d9ea717` (one commit over the
lead's `f99648d`, brought in at the boundary; 25 files, 534 lines added and 172 removed);
ruff clean; the sibling's fast tier whole on the final tree 3,917 passed and one failed, the
pictures' blank-image check, which that day failed alone on the step's tree and on a worktree
at `f99648d` alike with the same figure (the known flake); its slow tier of the known truths,
the trials and the touched files 151 of 161 passed with eight left out by their marks and two
failed, the lee-shore trial's container digest and truth 7-143 before the hail's mend (green
alone after it); its pace tests on a worktree at `f99648d` and on the step's tree in turn
under the container's floor on both, the step costing nothing the measure sees; the lead's
fast tier of the touched files (seven files, none failed); **the whole suite on the merged
tree `de36e0a` in the cloud (run 9, 39 minutes; 4,256 passed over the six shards, 3 skipped, 11 expected failures, none failed; the pace tests 10 of 10 in 155 seconds): green, every shard and the pace tests
passing; the shards' counts to be written in when read.** Step 7 stands merged green, the
cap's order's retirement of the not-crewed states moving no recorded passage. **The step:**
the player's ship is a vessel of the sea (`Vessels.own`,
under `ships.PLAYER_ID`, the one definition, which the brains, the squadrons and the action
import), made at the World's start after the scenario's and the business's ships and at an
old checkpoint's load, appended last and kept last, her hull the followed hull and the
followed hull's vessel she, brought up to her truth every tick; `player_shadow` keeps its
name and answers with her, so every reader of the shadow reads the vessel; a viewer's own
body is left out of `in_sight` and of the hail's addressees; the `PLAYER_ID` cases are one
rule through the vessel's hull (the squadrons' body, the action's, the boarding's, the hail's,
the captains'), the followed hull's way and frame her ship's own so the sets' stations
compute as before; `Vessels.active()` the other sail. **The cap's order** (decisions 3 and
6): the not-crewed states retired, so a hull at anchor or in port is awake under the cap and
a station may be seated on her in port; the order a ship in dealings, then a hull with a
stationed person, then the nearest, a higher rank within the range taking the farthest
lower-ranked crewed ship's place at a full cap; `crewed: {stationed: always}` keeps a
stationed hull awake whatever her distance. **Found on the way, both mended:** the business
could name a trader after the player's ship (her name was not among the sea's); and with her
on the sea the hail took the ship herself for "her" (truth 7-143 found it). **The lead's
review:** sound; two tidies for step 11's long tail, not mends: `combat/action.py`'s
`target_of` keeps an `if False:` arm where the shadow's branch was, and `world/ships.py`'s
`_lying_to` imports the readings' `_manoeuvre` from the api layer (lazily, so no cycle).

### Package 79a as merged (2026-10-29)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-79a` at `44fc890` (three
commits on the lead's `b3aff3a`; 10 files, 807 lines added and 34 removed), after the
period's books the ships session filed were brought forward from `claude/pkg-75` as data
(`docs/references/`, James, Nicolas, Niles, Jackson, Steel 1805 and the rest, with their
README rows), since the package's citations point at them; ruff clean; the builder's fast
tier whole 3,924 passed with the pictures' blank-image check the one failure (the known
flake, passing alone), its slow tier of the touched files and the squadrons' truths green;
the lead's run of the touched files and the new truths; **the whole suite on the merged tree
in the cloud (the figures below).** **The package:** every knob of `data/regimes.yaml` and
every key of the eight nations' `naval:` blocks (a `sources:` map each) cited by work,
volume and page, or said to be judgement with what was looked for; **no figure moved**; the
three a source gives differently written beside their knobs for the lead (below). The
commission drawn by the business: a ship in ordinary with no sortie is commissioned at the
region's peopling or the business's minute for an intent of her nation's (a doctrine station
within the region, else a passage to another of her ports), the delay from the regime's
knob drawn from the business's own stream, said in her story and the port's news (the
director's form writes the news too now), the line gone when she sails; a ship with a sortie
keeps the sortie rule; a ship with no intent of her nation's stays laid up and says so. The
blockades the sources give, dated: Rochefort to 12 July 1805 (off Chassiron, the rendezvous
Quiberon), Ferrol off Cape Prior, Cadiz under Orde to 9 April 1805 and from 31 May off
Cadiz at fifteen miles, Lorient from 1808; the ships in ordinary of Rochefort, Lorient,
Ferrol and Cadiz. The Channel's two regions draw nothing new (truth 7-267; the business's
record byte for byte the base's). Iberia's drift a note: Tofiño has no climatic table, the
weather untouched. Truths 7-260 to 7-269 (7-260 sets the clock forward over the 55-hour
delay, said in its docstring, the ship a brainless hull throughout). **The lead's rulings on
the figures that differ, all kept as the builder left them:** the commission's delay stays
two to five days (the record's eleven to thirteen weeks cut for play, the owner's earlier
judgement); the sortie's wind stays 22 knots from any quarter, with the sources' better rule
(a sortie on a strong fair wind off the land) booked for the regimes' next pass, since it
moves truth 7-154; the convoy's size stays four to eight under the cap; the blockade book's
Torbay stays, Plymouth and Cawsand being James's and Torbay the fleet's lee anchorage in
every account the game's earlier packages read. **Found and left, booked for 79c with the
Mediterranean's nations:** the blockade book's westerly sector is Brest's for every port
(Cadiz's danger was easterly), a per-port `blown_off` for the book; the business draws every
blockade as a frigate and a brig, the far body having no ship of the line until package 75's
74. The launch prompt named a CLAUDE.md the repository does not have; the briefs' heads and
the records served, and the next prompts will not name it.

### Package 84, step 8, as merged (2026-10-29)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `4b312fe` (three commits over
the lead's `de36e0a`: the step pushed in progress at the lead's word with the usage near its
limit, the fast tier's figure, the step green; 9 files, 416 lines added and 35 removed; the
tuning notes' conflict with 79a's section resolved by keeping both); ruff clean; the
sibling's fast tier whole 3,920 passed with the pictures' known flake the one failure, its
slow tier of the known truths, the trials and the touched files 169 of 178 passed with eight
left out by their marks and the lee-shore trial's container digest the one failure, its pace
read in a three-way A/B against the step 7 head on the same hour's machine and within the
head's own spread; the lead's run of the touched files (with 79b's, 279 passed, none failed); **the whole suite on the merged tree
in the cloud (run 11 on `76eb22c`, with 79b: lint green, 4,287 passed over the six shards, 3 skipped, 11 expected failures, none failed, 37 minutes; the pace job, informative, 7 of 10 with three under the floor at 452 to 491 ticks a second, read below).** **The step:** the save and the replay of many hulls. The
hull on each input and act of a station on another ship (`ship`: her id; the followed hull's
entries read as they did), given to her again by either road (the hull by id, or made in the
far shape by `station_world` as a seat made her in play); the save's `hulls` block with every
hull's stations, their journals, her book and her bindings; by the transcript a hull's block
seated when her first station is due, by the acts her `seated` act makes her; every hull's
stations in the replay's loop and taking up the game at its end; `transcripts_in` naming a
hull's station as "raven/captain". **Found and mended, two:** no act of a station on a hull
had been journaled since step 6, the façade answering a World class default over the
instance's value so the harness took it for no journaling; and a sleeping hull's station
order went by the far road before the acts' capture. Three tests new: a fake captain of a
promoted hull and of a far hull replayed by both roads to the same digests of both logs; the
owner's tender save loaded and replayed its first thousand ticks (another build's rules and
no station in it, replayed from its journal with the words that say so). **Taken another
way:** the doors untouched, the load's words already naming the stations a save holds; the
converter for a checkpoint with crewed Worlds as step 6 left it. Nothing pinned moved.

### Package 84, step 9, as merged (2026-10-29)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `6cf65f6` (one commit on the
trunk's `449a72a`, the lead's `76eb22c` brought in at the boundary before the step's final
fast tier and the records-only head under the step's changes before the commit; 13 files,
560 lines added and 42 removed, of them `world/orders.py` 215, `test_world_orders.py` 128);
ruff clean; the sibling's fast tier whole 3,944 passed and none failed, its slow tier of the
known truths, the trials and the touched files 182 of 191 passed with eight left out by
their marks and the lee-shore trial's container digest the one failure as at every step,
its pace within the spread step 8's A/B measured for the step 7 head on the same machine;
the lead's run of the touched files and the gate selection (202 passed, none failed);
**the whole suite on the merged tree in the cloud (run 12 on `6f8c708`: lint green, 4,293
passed over the six shards, 3 skipped, 11 expected failures, none failed, 34 minutes; the
pace tests 10 of 10 in 158 seconds, which closes 79b's note on runs 10 and 11).** **The
step:** the director's reach and the truth over the hulls. An `aboard` order names a hull at
its head and is carried out aboard her by her own names, her people's report in her log and
the order's own line in the player's log naming her; a person made aboard another hull is
of her company where package 68 refused the words, and `comes aboard the X [as <station>]`
moves a person of any company into her; a cutter's letter addressed to a hull steers for her
body and comes aboard her within hail; the rule of reach counts every hull's held stations;
the truth gives every hull's row awake or asleep with her purse, cargo and water and lists
the persons ashore at every port; `read_log(ship=)` reads a hull's log, the director's
alone; a seat may be at a person aboard any hull (67's refusal lifted); four hull examples
in the library performed by the forms test. **Found and mended:** the hearing's walk over
the stations counted the followed hull's twice since step 7; it walks the hulls each once.
**Taken another way:** a letter left at a port lies for whichever boat comes; no focus
tool; the hand's reach as 62 left it; 68's people test restated to the hull's refusal.
**Two tidies for the builder, booked to step 11 with the others:** the new reach test's
line `assert any(...) or True` asserts nothing and should assert the held station it names;
`_person_anywhere` matches a surname across the whole registry and takes the first, which
two Mr Popes on two hulls would confuse (the name whole first, the surname only when one
person bears it). Nothing pinned moved.

### Package 84, step 10, as merged (2026-10-30)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `5cc45f6` (one commit on the
trunk's `6f8c708`, brought in at the boundary before the step's final fast tier; merged here
over 79c's block, clean; 17 files, 422 lines added and 53 removed, of them `core/world.py`
100 and `test_crews.py` 87); ruff clean; the sibling's fast tier whole 3,946 passed with the
parity table's own entry mended after and the pictures' known flake the other failure, its
slow tier of the known truths, the trials and the touched files 185 of 194 passed with eight
left out by their marks and the lee-shore trial's container digest the one failure as at
every step, its pace within step 8's spread; the lead's run of the touched files and the
gate selection (202 passed, none failed); **the whole suite on the merged tree in the cloud
(run 14 on `90cef2c`: lint green, 4,312 passed over the six shards, 3 skipped, 11 expected
failures, none failed, 34 minutes; the pace tests 10 of 10 in 205 seconds).** **The step:** the drivers follow a hull. The World's default
hull is the followed one, the player's own until `follow "X"` names another, and with it
every per-ship name of the World's, the drivers' state, the browser's snapshot and chart,
the console's prompt and the log the drivers show; the player's hull stands apart as
`World.players`, the sea hers, her vessel on it brought up from her hull, the save the
game's with her current, and she is awake always and never counted against the cap; a
`follow` is a driver's line, journaled and replayed, refused in words for a ship not on the
sea or without a captain of her own; the walks over the hulls each once; `World.offices`
beside the hulls as the room for milestone 8's station of the world; a world order given
under a purview carries `by`, is checked by a hook the director and the bare order pass
whole, and is replayed with it. **Found and mended, two:** the pace rule's walk listed the
player's stations twice since step 7; and the first follow put the player's hull to sleep
and the save wrote the followed hull's seed, scenario and ship at its top, so a replay
rebuilt the brig's world. **Taken another way:** a world with no followed hull is 82's, its
words standing ready; whether the director's door follows the drivers or stays with the
player's ship is 82's question, noted; no office built. The parity table lists `follow` as
the owner's by design, as the clock's commands are. The step 9 tidies are booked in its
notes for step 11. Nothing pinned moved.

### Package 79d as merged (2026-10-30)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-79d` at `7ceaae7` (the trunk
merged into it at `9b3deb8` with 79c's block, the shared files kept both sides in order and
the counts summed; merged here over 84's step 10 with the tuning notes the one conflict,
both kept; 46 files beside the tiles, 12,843 lines added and 24 removed; 443 tile, coast and
index files, none of another region's touched); ruff clean; the builder's eleven recorded
passages by node id to their digests before and after its merge of the trunk, the touched
files' slow tests 14, truths 7-295 to 7-304 with 7-261 11, its fast tier on the final tree
with the pictures' known flake the one failure, the three regions rebuilt after the merge
with no tile of theirs or 79c's changed, the scenario sailed again to the same digest; the
lead's run of the touched files with five of its truths and the gate selection (268 passed,
none failed); **the whole suite on the merged tree in the cloud (run 15, the figures
below).** **The block, three regions by the lead's ruling at the builder's report of the
Gulf at 46.1 MB:** `gulf-of-lion`, 3 to 7.73 E, its south bound moved to the row edge
40.56 N where `balearics` ends so that the strip between the blocks answers, 120 level-2
tiles, the patches of Toulon, Marseille, the Hyères road and Villefranche, 28.1 MB;
`ligurian-sea`, 7.73 to 11 E, 72 level-2 tiles, the patches of Genoa, Leghorn, Porto
Ferrajo, Bastia, Ajaccio, San Fiorenzo and the Maddalena, 20.6 MB; `tyrrhenian`, 8 to
15.5 E and 38.5 to 42.5 N, its boundary with the Gulf at the row edge 40.99 N west of
11.15 E, the patches of Cagliari, Alghero, Civita Vecchia, Gaeta, Naples and Ponza,
37.8 MB; all after `balearics` in the chart. The marks from the research pass's texts
(the Derrotero of 1849, Lamberti, Michelot, Purdy, Norie, Smyth), seventeen islets the
grid lacks given as rocks of their height and extent, the lights dated from the earliest
text that has them (Porto Ferrajo's and Bastia's `from` 1826, the later ones unverified).
Sixteen port files (Toulon, Marseille, Hyères and Villefranche French and hostile; Genoa,
Leghorn, Porto Ferrajo, Bastia, Ajaccio, San Fiorenzo, the Maddalena, Cagliari, Alghero,
Civita Vecchia, Gaeta and Naples), and `sardinia`, `naples`, `etruria`, `liguria` and the
Papal state as data in Morocco's form, each relation sourced to James or said from memory;
**a port's nation by date** (Genoa the Ligurian Republic's until 3 June 1805 and France's
from the 4th), the smallest change in `world/ports.py`, the loader taking the scenario's
first day and `Ports.stance` the world's, the other readers named in the notes, a test of
the form and of Genoa's two dates, no recorded passage moved. The gauges held with
verified mean levels; the currents of the directions as `current:` with no tidal stream;
Norie's places; two weather boxes from the Admiralty's tables (Marseille's, Ajaccio's,
Genoa's, Leghorn's, Naples' and Cagliari's), the Gulf's taking the mistral's lows and saying
the easterlies it leaves short. `agincourt-sound.yaml` sailed at seed 7 from the Maddalena
to look into Toulon and back, not pinned. Truths 7-295 to 7-304 as behaviours. No gauge
of the eleven moved, no recorded passage's digest moved. **The lead's rulings on its
findings:** (1) the world's tide over the Mediterranean is Le Conquet's alone while the
gauges are held, two metres of M2 against the gauges' centimetres, and the master's account
allows a flood in a sea that has none: 89's case, now the strongest, its brief to say so;
(2) the lights of 1805 dated from the earliest text on file is the rule working, and Porto
Ferrajo's of 1788 from memory stays a note until a text dates it; (3) a `road` with a
bottom gives no note of it, the roads being anchorages: a chart tidy booked with the island
kind and the inland tiles; (4) each port's produce cheap and its wants dear by judgement,
so that the business draws a trader in the Mediterranean: accepted, said so in the files,
as 79c's grain was; (5) the weather's one track a month cannot carry two wind regimes in
one box: a finding for the weather's design, recorded for the lead, not this package's;
(6) Porto Santo Stefano, Giannutri, Monte Limbara and the Adriatic's shore not given, and
Sicily, the Lipari islands and Messina a later block, as the notes say.

### Package 79c as merged (2026-10-29)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-79c` at `e17dad4` (the trunk
merged into it at `fafee99` with the tuning notes the one conflict, both kept; 31 files
beside the tiles and the pilots' texts, 2,635 lines added and 12 removed; 375 tile, coast and
index files, none of another region's touched); ruff clean; the builder's eleven recorded
passages by node id to their digests, the touched files' slow tests 14, truths 7-285 to
7-294 10, its fast tier on the final tree with two lists of its own extended (the chart's
regions in `test_geo.py`, truth 7-261's count of the nations now nine) and the pictures'
known flake the rest; the lead's run of the touched files with the short truths and the gate
selection (267 passed, none failed); **the whole suite on the merged tree in the cloud
(run 13 on `159df45`: lint green, 4,308 passed over the six shards, 3 skipped, 11 expected
failures, none failed, 39 minutes; the pace job, informative, 8 of 10 with the gates' day at
472 and 7-159's convoy at 456 against the floor of 500, the job 281 seconds against run 12's
158 on the same ten tests an hour before: the runner's day as runs 10 and 11 were, read in
79b's record; nothing re-pinned).** **The block, two regions by the lead's ruling at the
builder's report of 57.5 MB in one:** `mediterranean-west`, 35 to 40.5 N and 5 W to 0.05 E,
165 level-2 tiles and the patches of Málaga, Almería, Cartagena and Oran with Mers-el-Kebir,
26.5 MB, three seam tiles the Strait's; `balearics`, 0.05 to 4.5 E, 154 level-2 tiles and
the patches of Palma, Port Mahon, Ivica and Algiers, 30.9 MB, the fourteen-tile seam column
`mediterranean-west`'s, its north edge at the row 40.56 N where 79d's Gulf begins; both after
`strait` in the chart, whose title now names them. 182 marks from Tofiño 1787 and the
research pass's texts, the lights of 1805 three (Málaga's mole, Porto Pí's, Algiers'; none
at Mahon by Purdy 1840, the brief's "Mahon's light" withdrawn), the isles the grid lacks as
rocks, Mahon placed by hand by Tofiño's plan. Eight port files (six Spanish and hostile,
Cartagena's and Mahon's yards; Oran's and Algiers' the regency's, neutral) and `algiers` in
Morocco's form, its relations from James where he speaks and from memory where said so.
Nine TICON gauges held with REDMAR's mean levels verified; seven stream areas, no tidal
stream, the period's currents (east along Granada and Barbary, west inshore from Oran);
Norie's table with the pilots' foot of rise. The weather box `mediterranean-west` from the
Admiralty's tables, every month within five points. `mahon.yaml` sailed at seed 7 from
Gibraltar road to the mouth of Port Mahon through a northerly, 98 hours, not pinned. Truths
7-285 to 7-294 as behaviours, five of them in the long list of `conftest.py`. No gauge of
the eleven moved, no recorded passage's digest moved. **The lead's rulings on its findings:**
(1) the world's tide over the Balearics is Saint-Malo's while the gauges are held: 89's
brief now carries the figure, the sharpest case yet; (2) the regency's war with Portugal is
from memory and rightly not in `wars:`, their ships neutral to each other until a work on
file gives it; (3) an isle the grid lacks is a rock so that nothing sails through it, and
the lookout calls it "a danger": **a feature kind for an island with an extent is booked as
a chart tidy** with the Alboran's inland tiles (`skip_dry_tiles`, on file since 39d, not
taken) for the next block package or a small one of its own; (4) the apostrophe refusal is
85's, written into its brief; (5) the Barbary grain (Oran's and Algiers' wheat in the
Spanish ports' markets, from memory, said so) stands as the judgement that gave the business
its routes, a source to be cited when one on file speaks; (6) Mahon's harbour patch read
from Tofiño's plan with its datum, and the modern ports in the grid's land, are the later
package's with Bellin's plans, as 79b's are. Both regions went into one commit rather than
two, said in the notes: accepted.

### Package 79b as merged (2026-10-29)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-79b` at `174d002` (six commits
on the lead's `de36e0a`, five steps; 42 files beside the tiles, 132 tile, coast and index
files all new and none of another region's touched; the tuning notes', the known truths' and
the references README's conflicts with 79a's additions resolved by keeping both, the
README's count of works recounted to thirty-two); ruff clean; the builder's gate selection
and the eleven recorded passages passing to their digests, its slow tests of the chart, the
ports, the tide and the scenarios and truths 7-270 to 7-279 green, its fast tier on the
final tree with the pictures' known flake the one failure; the lead's run of the touched
files (with step 8's, 279 passed, none failed); **the whole suite on the merged tree in the cloud (run 11 on
`76eb22c`: green, the figures in step 8's record above).** **The pace job of runs 10 and 11, read:**
run 9 on `de36e0a` passed its ten pace tests in 155 seconds; run 10 on `995d515` (79a alone)
failed two at 458 and 478 in 279 seconds, and run 11 failed three at 452, 463 and 491 in 290
seconds, the job as a whole near twice as long on the same tests, which is the runner's day
and not the tree's: an A/B on the lead's machine, the three tests on `de36e0a`, `995d515` and
`76eb22c` in turn, twice, had `de36e0a` and `76eb22c` pass both rounds and `995d515` fail once
at 498 and 500 and pass once, every head at the floor's edge with the machine's noise and no
head below another; the step 8 sibling's own three-way A/B against the step 7 head was within
the head's spread. The pace job is informative by the workflow's design for this reason;
nothing is re-pinned, and the next green pace job on a quiet runner closes the note.
**The block:**
the region `channel-east` from the Wight to Dunkirk, 49 to 51.5 N and 1 W to 2.5 E,
abutting `channel-mid` at 1 W exactly; 57 level-2 and 73 level-3 tiles (13 MB: shallow
water compresses well), six seam tiles kept `channel-mid`'s; eight harbour patches; 137
marks from Faden 1793, Moore 1799, Norie 1805, White 1835 and Imray 1874, the lights dated
so that 1805 sees what 1805 had, the Goodwin's five drying heads; eight port files
(Portsmouth with the King's yard, Poole, the Downs with the Deal boatmen, Dover without the
Admiralty harbour; the Havre, Boulogne, Calais and Dunkirk, French and hostile, the
invasion flotilla and its batteries noted in their heads and not modelled), every one
`datum: unverified` with no sheet read; the six TICON gauges read and **held**, the French
mean levels SHOM's; eight stream areas by the directions and the block's box in the
directions' limits; Norie 1805's Table XLI read from the page images for 27 places; the
Channel's weather box to 2.5 E, the same rows; `data/scenarios/spithead.yaml` sailed at seed
7 from the Downs through the Strait to St Helens for the night and Spithead at daylight, 28
hours, with the book's lessons recorded; truths 7-270 to 7-279 as behaviours; the pilots'
texts under `docs/references/pilots/` with their rows. No gauge of the eleven moved, no
recorded passage's digest moved. **The lead's rulings on its findings:** (1) the world's tide
over the block is the eleven's blend and wrong in its range (Newhaven's spring range 3.9 feet
for the gauge's 19.5), the block's gauges held as every block's are: **the gauges' water is
now the most pressing of the held decisions, since this block is the Channel itself, and is
booked as package 89** (below), the rule that a held gauge serves the positions within its
own block's bounds alone, so that no position west of 1 W reads anything new; (2) the spec's
pointer under §28, the chart's section, is right (the brief's §26 was the lead's slip);
(3) Portsmouth without an Ordnance block, the table being the practice-and-resupply
design's eleven: a finding for the magazine's table, booked to 77 with its source (the Gun
Wharf issuing at Spithead under the Regulations of 1806); (4) the modern ports land in the
grid where 1805 had water or sand, no sheet read: a later package with Bellin's plans of
the Havre and Dunkirk; (5) and (6) as the builder has them.

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

## Package 74: prizes, the strike and what follows, and the far fight (`freesail/world/prizes.py` new; `freesail/world/crews.py`, `ships.py`, `brains.py` the prize as a vessel with a new nation and goal, the far fight wired; `freesail/combat/far.py`, `action.py`, `morale.py`; `freesail/world/business.py`, `ports.py`, `data/business.yaml`, `data/ports/*.yaml` the prize court and the head money; `freesail/world/people.py`, `places.py`, `hearing.py`, `stations.py`, `seats.py` the captive's place and voice; `freesail/world/captains.py`, `data/captains/*.yaml` the captor's and the prize master's doctrine, the parole; `freesail/agents/harness.py`, `director.py`, `data/director/` the captive's channel, the court martial as the director's proceeding, a new command; `freesail/world/scenarios.py`, `data/scenarios/`; `freesail/api/readings.py`; `docs/design/` the consent revision's draft; `docs/TechnicalSpec-M7.md` §11a, §18 to §20, §29 as built; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths from the number after 73's)

Fable; the fifth and last of the front-loaded Fable packages, run alone after 73 by the
owner's rule. Spec M7 §11a (the far fight), Part 7-v (§18 to §20) and §29 whole, with rule
4 (rules first, models welcome) and rule 5 (the far ships fight as the near do, coarsely);
decision 7 (the colours struck by rule, the captain's own word too); the striking-colours
study whole (its gaps 1 and 6 are this package's); the owner's note on the court martial
and the continuation (`docs/design/NotesForM7.md`); 70's far fight measured and not wired
(`combat/far.py`, truth 7-139), 72's cut-out stopping at hailing distance and its prize hook
on the set, 73's fight on deck ending at `struck` by the boarders' hand, 71's captured
private table as a paper, 53b's things and transactions, 66's line and 67's seat at a
person (the shape of the captive's voice). **Generously scoped as the four before it:** the
brief binds the intent and names the ground, the builder designs, takes an item another
way with its reason, grows a part where the work shows it should, and says what it left
and why; no day count. **The prize and the captive are designed first and written down
before they are built** (a design note under `docs/design/`), because 80 fills them out and
M8's career remembers what they record. Each item an intent with the lead's reading; the
intent binds.

1. **The prize (§18).** A ship struck is possessed: her colours the captor's; a prize crew
   out of the captor's muster put aboard with a prize master (a person bound to her
   captain's station under the rules, or a model's seat by 67's door); her people prisoners
   confined below or divided between the ships, counted as numbers but for the named; a
   goal that is a friendly port, the two sailing in company (72's set: a prize joins her
   captor's company) or parting; a prize retaken by her prisoners rising when the prize crew
   is thin and tired, or by a cruiser coming up (the retaking by boats waits for 63's boat
   and 77's cutting out); a captured signal book or private table a paper of the prize
   (71's); burning or scuttling a prize not worth manning; the far body carrying a prize as
   a vessel with a new nation and goal. The doctrine of it in the captor's role file (what
   he mans, what he burns, how he divides his people).
2. **The prize court and the money.** The prize condemned and paid at the port by the
   business's purse: the hull's valuation (60's mechanics from the other side: 60 is not
   built, so the least valuation from the ship file's tonnage, age and fit with its source,
   left in a shape 60 takes up for buying and selling), the cargo at the market (53b's
   transactions), the head money for a privateer or a man-of-war, the agent's commission,
   shared by the period's eighths (the 1808 proclamation's shares, or the 1805 ones, named)
   between the captain, the officers and the people, the purse's line saying so; a prize
   lost on the way home nothing; a neutral taken wrongly the court's refusal and the costs.
3. **The player struck: the captive's channel (§19; the study's gap 1).** The player who
   strikes has not lost the game: he is a person aboard the captor with the place and the
   voice M7b gave every person (where he is: the great cabin, the gunroom, the hold; what he
   can see from there; what he can say and to whom, `say to the captain: ...`; his journal
   kept); the parole given or refused by the period's custom (an officer's parole, a
   passenger's, a seaman confined); the captor's captain a rules captain by doctrine (the
   sword returned, the parole accepted, the course for his port, the prisoners landed or
   exchanged by cartel) or a model's seat or the director's voice; the director shaping
   what follows through plausible causes as always (a gale that night, a cartel in the
   offing, a friendly cruiser at dawn); a holder at the captor's stations seeing him as a
   person aboard. The same channel serves a prisoner of the player's own prize, by parity.
4. **The court martial and a new command (§19; the owner's note).** The court martial as
   the director's proceeding: its questions in-world through the director's channel (67's)
   and the captive's, the verdict a world order journaled (acquitted with honour, reprimanded,
   dismissed the ship, dismissed the service), nothing shown as sent; a new command as a
   scenario's start that carries what the records keep (his name, his people who followed
   him, the verdict); **a career that remembers is M8's**, the hooks named in the records.
5. **The far fight, wired (§11a; rule 5).** 70's `combat/far.py` (the same tables at
   three-minute rounds) given to the far brains: two far ships that meet in anger resolve
   their action at coarse steps by their doctrine (the engaging transition for the far
   bodies with the doctrine's range under the nation's habit), the damage summed into the
   far state (`Vessel.damage`), the striking by morale, the prize as item 1 has it at far
   detail; 72's cut-out carried from hailing distance to its end by the same rounds; within
   the promotion's range the engaged ships crewed under the cap's order, **an engagement
   first among the cap's reasons**, the far state carried into the near body and back; the
   near action and the far one measured to agree within a round (70's truth 7-139 extended);
   the pace measured with the far fights running (the floors not lowered).
6. **The consent revision for adversarial seats (§29; the study's gap 6), drafted and not
   applied.** No model is seated as the captain of a ship that fires into a human's ship or
   takes him prisoner until the consent brief has been revised and the question put again;
   package 55 (deferred by the owner until testing begins in earnest) carries the revision
   and the re-brief. This package **drafts the revision's text** under `docs/design/` (what
   the brief would say: the roles of an enemy captain, a prize master over prisoners, a
   captor's captain to a human captive; what an instance would see and do; the leaving
   words), **edits no file under `docs/agents/consent/` or `docs/agents/ConsentBrief.md`**,
   and makes the game refuse such a seat in words until the revised brief is in force (a
   flag the revision's package turns), the refusal saying why; the rules captain and the
   director's voice serve every adversarial role meanwhile (rule 4).
7. **The stations, the director and the readings.** `the prize`, `the prisoners`, `the
   prize crew`, `the parole` as readings; the events and tripwires (`she is taken`, `the
   prisoners rising`, `a cartel`); the director's forms after `WORLD_ORDER_FORMS` (a prize
   condemned or restored, a cartel sent, the court's verdict, a new command) with their
   doubts; the harness's samples at the captive's channel and at a prize master's station;
   the truth showing every prize, her crew and her prisoners.
8. **Truths and records.** §20's truths (a merchant brig taken by a privateer schooner sails
   for Bayonne under a prize crew of eight with her master a prisoner in the cabin and is
   retaken by a cruiser coming up when the prize crew is thin and tired, the boats' retaking
   left to 63 and 77 with the truth's words amended and the reason; the prize money paid at
   Falmouth by the eighths, the purse's line saying so; the player struck to a model's ship
   asked for his parole in the model's words and answering in his own, the exchange in both
   logs and nowhere in the operator's voice, by the test's fake door; the far fight of a
   privateer and a merchantman off the horizon ending as the near fight would within a
   round, and the prize carried; a court martial's verdict journaled as a world order and a
   new command started from it), numbered from the first after 73's; scenarios (the prize's
   passage home; the captive aboard the captor); spec §11a, §18 to §20 and §29 "as built";
   the Harness (the captive's channel, a prize master's station); a chapter of the primer
   (a prize taken, a prize crew, the court; striking and what follows); the director's
   library; the tuning notes (the design or its pointer, each item, the figures and sources,
   the far fight's agreement, what moved and its proof, the pins old beside new, found on
   the way, decisions, the suite as run); the fast tier, the slow tier of the touched files,
   the whole slow tier when the machine is quiet, the pace tests alone and last.

**Not built here:** the career (M8); a ship bought and sold (60) beyond the valuation's
shape; the boats' cutting out and retaking (63, 77); the cartel's and the captive's places
and words filled out (80); the consent revision applied (55). **The head rules bind** as the
briefs before have them: no model identifier; **nothing under `docs/agents/consent/` or in
`docs/agents/ConsentBrief.md` touched, this package's item 6 included**; a world order never
shown as sent; the ship files through the generator with sources; the pins re-measured only
where a change moves them, old beside new, proven by bisection (the far fight wired can
move passages with two far ships in anger: say which and why); never a test skipped,
disabled or quarantined; realism, not pacing; the physics read and not changed.

**From the owner's local work, folded in by package 86** (the review of it, section 5):
the port files now carry an `ordnance:` block (who issues and sells powder and shot, at
what price, from the road or the harbour), the hoy is a port job (`world/ordnance.py`, the
galley fire out while she is alongside), and `world/service.py` says whose service a ship
is in (the papers, the captain's role, the wardroom) and who may buy of whom. 74 builds
the prize court, the prize's stores and captured powder as prize goods (the owner's ruling)
on these, not beside them.

**Found by package 75 (2026-10-29), for this package:** `combat/far.py:111` reads
`spec.hull.length_m`, a key `HullSpec` has not (`length_waterline_m` is its), so every far
ship's length is 0.0 and `combat/shot.py:167` floors her size at 0.5 whatever she is. The
mend is one read, and it moves the far fight's pins: re-measure them where moved, old
beside new, the cause this line.

## Package 79a: the regimes filled out and sourced (`data/regimes.yaml`, `data/nations.yaml` `naval:`; `freesail/world/regimes.py`, `freesail/world/business.py` the commission drawn; `data/weather/` only if Iberia's drift is taken; `docs/TechnicalSpec-M7.md` §22 as built; `docs/dev/TuningNotes.md`; `tests/test_business.py`, `test_nations.py`, `test_known_truths.py` truths 7-260 to 7-269)

Opus. The first of 79's four packages (the owner's split of 2026-10-29), none of which waits
on 84: it touches the business, the regimes and their data, which 84's remaining steps
(the player's ship a hull, the save, the director's reach, the drivers) do not. It builds on
package 72's shape (spec §22 "as built"; `docs/design/Design-Squadrons.md`; 72's record and
its "left to 79" lines above) and **changes no rule a recorded passage runs**: the truths
7-152 to 7-160 and the trials stand, and the scenarios that name no business draw nothing
new. Read 72's record, the regimes file's head and `regimes.py`'s head before anything.

1. **Every knob sourced, or said to be judgement.** Each figure in `data/regimes.yaml` and
   each nation's `naval:` block is marked "from memory" today. The repository now holds
   the period's own books under `docs/references/` (James's six volumes of the *Naval
   History*, Nicolas's *Dispatches and Letters of Nelson*, Niles' *Register* for 1812 to
   1815, the *Regulations and Instructions* of 1806, Jackson's *Logs of the Great Sea
   Fights*, Falconer, Steel): read each knob against them and write the source by volume and
   page where one is found (the blockade of Brest's inshore and offshore squadrons and its
   being blown off, the convoy acts and the convoys' sizes, a commission's weeks, the
   French keeping port and the sorties when the blockaders were blown off, the Dutch at
   the Texel, Ferrol and Cadiz under blockade); where none is found, the figure stays and
   its `source:` says "judgement" plainly, with what was looked for. Mahan is not in the
   repository: a figure that rests on him alone is said so and left. **No figure moves in
   this item**: a source that gives a different figure is written beside the knob as "the
   source gives N; kept at M until re-measured", and the lead rules. (The pins: a knob that
   a recorded passage reads, the sortie's fifteen miles, hour and 22 knots among them,
   moves no digest only if it does not move.)
2. **The commission's delay drawn by the business** (72's first left item). A hull in
   ordinary is commissioned today by the director's form (`ship "X": commissioned for
   <intent> [at once | in <n> hours | in <n> days]`) or at once by the business. Give the
   business the regime's delay: a nation's ship in ordinary with no sortie is commissioned
   by the business for an intent of her nation's (a cruise on one of her doctrine's
   stations, a passage between her ports) after `commission_delay_h` drawn under the
   seed, said in her story and the port's news as the director's commission is; a ship
   with a `sortie` keeps the sortie rule as it is. The draw is from the business's own
   stream so that no other draw moves (`test_the_draw_is_the_seeds_and_moves_no_other_draw`
   says how). Off unless the business is on; every recorded passage leaves it off.
3. **The nations' doctrines as data, for the waters the chart has.** The `naval:` blocks
   of Britain, France, Spain, the Batavian Republic, the United States, Portugal, Denmark
   and Morocco filled where 72 left them thin: who blockades whom and where (Britain's
   `blockades:` names Brest alone; Ferrol, Rochefort, Cadiz and the Texel belong there
   with the dates the sources give), who convoys and with what escort, who keeps ships in
   ordinary at which ports with what sortie (France's one frigate at Brest is the whole
   list today), the privateers' prey. Each entry with its source as item 1 has it. **No
   new nation in this package**: the Mediterranean's (the Ligurian and Italian republics,
   Naples, the Barbary regencies, the Ottomans) come with their blocks, 79c and 79d.
4. **Iberia's drift** (72's second left item): the seasonal bound of the weather 72 took only
   as far as the squadrons' gale wanted, and the Portuguese coast's drift and northerlies
   of summer that the climatology's PROVISIONAL rows stand in for. Read what the pilots on
   file say (Tofiño's directions for the summer northerlies, the references' index); if a
   printed climatic table is found it replaces a PROVISIONAL row as `ChartBlocks.md` item
   7 says; if not, the item is a note in the tuning notes and nothing changes. Truth
   7-158 (the bound off in every recorded scenario) stands either way.
5. **Not this package's**: the nations' fighting habits (firing high, the single actions),
   which are the far fight's and the action's and go with package 74; the regimes' words
   in the primer (85's); any new regime (the eight stand).
6. **Truths 7-260 to 7-269** in `tests/test_known_truths.py`: a ship in ordinary at Brest
   with no sortie commissioned by the business after the regime's delay under seed 7, her
   intent her nation's and her commission in her story and the port's news; the knobs'
   table read whole with every source in the references' form or "judgement"; and what the
   items above earn, each a behaviour and not a digest. The fast tier whole on the final
   tree; `test_business.py`, `test_nations.py` and the squadrons' truths 7-152 to 7-160 in
   the slow tier; the whole suite is the lead's in the cloud at the merge.
7. **The records**: spec §22 as built (the list of what is still judgement, by knob); the
   tuning notes' section (the sources read, the figures found that differ and kept, the
   commission's draw and its first run, the suite as run).

The hard rules as every brief has them: no model identifier in any file or commit message's
body; the two attribution lines; nothing under `docs/agents/consent/` touched; no pin moved
without the old beside the new and the proof; the physics not changed; the references
read as data and never run. Work in a worktree on a branch `claude/pkg-79a`, pushed after
each commit; the lead merges.

## Package 79b: the Channel's east block (`channel-east`; `tools/build_charts.py` `REGIONS` and `CHARTS`; `data/charts/` the region's tiles, coast, index and manifest entry, `features/channel-east.yaml`, `overrides/channel-east/`; `data/ports/*.yaml` new per port; `data/nations.yaml` the ports' index; `data/tides/constituents.yaml` `held_gauges:`, `streams.yaml`, `establishments.yaml`; `data/weather/climatology.yaml` only the Channel box's east bound; `data/scenarios/spithead.yaml` new; `docs/references/README.md` the pilots fetched; `docs/dev/ChartBlocks.md` where the how-to proves wrong; `docs/TechnicalSpec-M7.md` §26's pointer as built; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_ports.py`, `test_tide.py`, `test_scenarios.py`, `test_known_truths.py` truths 7-270 to 7-279)

Opus. The second of 79's four packages: the Channel one block to the eastward (the owner,
2026-10-29), built as `docs/dev/ChartBlocks.md` says (read it whole first, with the recipe
form over `REGIONS` in `tools/build_charts.py`, package 38's and the six blocks' sections
of the tuning notes, and 39a's brief in `docs/dev/M6-WorkPackages.md`, whose region
`channel-mid` this one abuts). It touches nothing of any other region's tiles, coast or
index, and nothing 84 reworks.

1. **The region** `channel-east`: the Wight and the Solent, Spithead and St Helens road,
   Portsmouth; Poole; Beachy Head; the Downs and Deal, the Goodwin Sands, the South and
   North Forelands, Dover; Dungeness and Rye bay; on the French side the Seine's mouth and
   Le Havre, Fécamp, Dieppe, Boulogne, Calais and the Flemish banks to Dunkirk. **Bounds
   49.0 N to 51.5 N and 1.0 W to 2.5 E, abutting `channel-mid` at 1 W exactly** (its east
   bound), the fetch box widened as the form says; a bound moved to a tile column's or
   row's edge where a mark asks it, at no cost in tiles, as Biscay south's was. The Thames
   above the North Foreland and the Nore, and the Flemish coast east of Dunkirk (Ostend,
   Flushing), are later blocks and are said so. Cherbourg (1.6 W) lies in `channel-mid`'s
   bounds: not this block's (a left item there, as Morlaix was for 39a).
2. **The harbour patches** (level 3, about 15′ by 15′ each): Spithead with Portsmouth
   harbour's mouth and St Helens road; Poole; the Downs with Deal and the Gull Stream;
   Dover; Le Havre and the Seine's mouth; Boulogne; Calais; Dunkirk. Dieppe, Newhaven,
   Shoreham and Rye are roads and marks without a patch unless a sheet is read for them.
   The seam rule for the tiles `channel-mid` lists, as the how-to has it.
3. **The period data.** The English side from the Hurd and Mackenzie sheets where they can
   be fetched, and the Channel pilots on file (White 1835, Imray 1874, Moore 1799's
   catechism) for the directions and the marks; the French side from Bellin and the
   *Neptune François* where fetched, and the pilots for the rest. The period shoreline
   where it differs from the modern: **Dover without the Admiralty harbour** (built from
   1847) and Portsmouth without the later dockyard basins and Haslar's reclamation, as
   Plymouth is drawn without the breakwater; the Goodwins as the sheets of the day have
   them, with `dries_m` and an `extent_m` under a kilometre a head. The lights of 1805 dated
   (the South Foreland's two, Dungeness, the Nab's floating light, the Owers, Calais,
   Gris-Nez, Dunkirk, and the rest the directions give), so that 1805 sees what 1805 had.
   Every source fetched goes under `docs/references/` with its README row, read as data
   and never run; where a sheet cannot be fetched or its datum read, the port file says
   `datum: unverified` and no figure is invented.
4. **The ports** on package 35's machinery, each a file: Portsmouth (Spithead the outer
   road, St Helens, the harbour; the King's dockyard: the yard's goods and the Ordnance's,
   as Plymouth has them), Poole, the Downs (Deal, the anchorage and its boatmen), Dover,
   Le Havre, Boulogne, Calais, Dunkirk; each with its nation, its state (Le Havre,
   Boulogne, Calais and Dunkirk French and hostile to a King's ship; the invasion flotilla's
   ports of 1803 to 1805 and their batteries noted in the file's head, not modelled),
   its road, pilot's station, market, yard, pool and the pilot's four words, and every
   `feature:` spot with its position beside it; entered in the nations' index and
   `test_ports.py`'s list. No new nation.
5. **The tide.** TICON's gauges of the block read as package 34 read the file (Portsmouth is
   held already from 39a and Dover is among the eleven: which others it has, Newhaven, Le
   Havre, Dieppe, Boulogne, Calais, Dunkirk, is unverified until read), **held** under
   `held_gauges:` after the last, as every block's are until the lead rules on the gauges'
   water; the eleven and their figures do not move. The stream areas by the directions: the
   Solent and Spithead, the Looe and the Owers, Beachy Head, the Downs and the Gull Stream,
   the Strait of Dover, the Seine's mouth; an area over the block's whole box after them,
   and the block's box appended to `book_limits`. The master's epitome places with the
   period's rise where a pilot gives one (Portsmouth's, Dover's, the Downs', Le Havre's).
   The polygons kept off the water the recorded passages' other sail use.
6. **The weather.** The Channel box reaches 2 E; the block's water to 2.5 E would take the
   nearest box by `Climatology.box_at`. Extend the Channel box's east bound to 2.5 E
   (the same rows: judgement, said in the row's note), unless a printed table is read.
7. **A scenario** `spithead.yaml`: a free passage of the block's stretch (the frigate from
   St Helens road down Channel through the Needles, or from the Downs through the Strait
   to Spithead against the stream: the package's choice), `chart: atlantic-east`, sailed
   once at seed 7 to the anchor by a short book, its figures in the notes; not pinned.
   (39a's scenario `channel-east.yaml` sails `channel-mid` and keeps its name.)
8. **The build**: `python tools/build_charts.py --region channel-east` through the proxy,
   the checks printed and passing, the tiles committed (expect 20 to 30 MB: the block is
   mostly coast and shoal water), the manifest with every other entry carried over, the
   region appended to `CHARTS["atlantic-east"]["regions"]` after `channel-mid`, and after
   the build `git status` showing no change to any tile, coast or index another region
   lists. Build early, to fetch; rebuild with `--skip-fetch` after the marks are written so
   that the index holds them.
9. **Truths 7-270 to 7-279**: the frigate's lookout from Spithead sees the Nab's light at
   its range by night and the Wight's marks by day; a ship through the Strait of Dover at
   springs is set by the stream as the directions say (the master's account against the
   world's water); the Goodwins ground a ship that stands on across them with less water
   than she draws; the Downs' anchorage holds her in a south-westerly with the sands to
   leeward; the ports' files load and the passages of 7-157's kind cross the seam at 1 W
   with the business carried; and what the build earns, each a behaviour.
10. **The records**: the tuning notes' section (the sources with their licences, the
    patches' datums and residuals, the checks as printed, the scenario's run, what was found
    on the way, the suite as run: the fast tier whole on the final tree, the chart's, the
    ports', the tide's and the scenarios' slow tests; the recorded passages of the Channel
    west, `gate_5b` and `gate_5c` once, which must pass to the digest); `ChartBlocks.md`
    corrected where the how-to proved wrong; spec M6 §26's as-built list extended by the
    block and M7 §26's pointer.

The hard rules as every brief has them; `claude/pkg-79b`, pushed after each commit; the
lead merges, rebuilding `channel-mid`'s index by hand only if a mark of this block lies in
its bounds, as 39a's were. Runs after 79a or beside it (the two share no file but the
nations' ports index, which the lead merges).

## Package 79c: the Mediterranean's west block (`mediterranean-west`; `docs/references/pilots/` the research pass, both basins; `tools/build_charts.py` `REGIONS` and `CHARTS`; `data/charts/` the region's tiles, coast, index and manifest entry, `features/mediterranean-west.yaml`, `overrides/mediterranean-west/`; `data/ports/*.yaml` new per port; `data/nations.yaml` the ports' index and the regency of Algiers; `data/tides/constituents.yaml`, `streams.yaml`, `establishments.yaml`; `data/weather/climatology.yaml` a box of its own; `data/scenarios/mahon.yaml` new; `docs/references/README.md`; `docs/dev/ChartBlocks.md`; `docs/TechnicalSpec-M7.md` §28's pointer; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_ports.py`, `test_tide.py`, `test_weather.py`, `test_nations.py`, `test_scenarios.py`, `test_known_truths.py` truths 7-285 to 7-294)

Opus. The third of 79's four packages: the Mediterranean's west, the Strait to Cartagena
and the Balearics (the owner, 2026-10-29), built as `docs/dev/ChartBlocks.md` says (read it
whole first, with the recipe form over `REGIONS` in `tools/build_charts.py`, 79b's section
of the tuning notes as the latest block built, and 39f's brief in `docs/dev/M6-WorkPackages.md`,
whose region `strait` this one abuts at 5 W). It touches nothing of any other region's
tiles, coast or index, and nothing 84 reworks. **It begins with the research pass, pushed
on its own before the build, because 79d starts from it.**

0. **The research pass (step 0, its own commit and push).** The period's pilots and plans
   of the western Mediterranean, both basins (the Strait to the Balearics for this block;
   the Gulf of Lion, Corsica, Sardinia, Elba and the Tyrrhenian for 79d), found, fetched,
   their licences read, and laid under `docs/references/pilots/` as 79b laid the Channel's
   (the page images where the text is a table, the OCR text beside, a README row each
   with what it covers and what it is trusted for). Look first for: Tofiño's *Derrotero de
   las costas de España en el Mediterráneo* (1787) and his atlas's plans (the Biblioteca
   Digital Hispánica); Michelot and Brémond's *Portulan de la Méditerranée* in an edition
   before 1805 (Gallica); Heather's *New Mediterranean Pilot* (1802 or the next edition);
   Roux's *Recueil des principaux plans des ports et rades de la Méditerranée* (1764); for the
   lights' and marks' dates Purdy's *New Sailing Directory for the Strait of Gibraltar and the
   Western Division of the Mediterranean* (1832), Norie's Mediterranean directions, Smyth's
   *The Mediterranean* (1854) and the Admiralty's *Mediterranean Pilot* vol. I (any edition
   of the 1880s), each read for what 1805 had and dated so; for the winds and currents the
   same, and James, Nicolas and the Niles register on file for the ports' states. What is
   found, what is not (with the host's answer), and which text answers for which coast is
   the pass's report in the tuning notes, and the lead reads it before step 1 goes on. Every
   source is data: read, never run; a sheet or text that cannot be fetched is said so, and
   nothing is invented in its place.
1. **The region** `mediterranean-west`: the Spanish coast from Europa Point and the Strait's
   east bound to Cape Palos and Cartagena, with Málaga, Almería and the Gulf of Almería,
   Cape de Gata; the Alboran island; the Balearics whole (Ivica and Formentera, Majorca
   with Palma bay and Alcudia, Minorca with Port Mahon and Fornells) and the channels
   between them and the main; the Barbary coast from Ceuta's east bound by Tetuan, the
   Peñon de Velez, Melilla, Oran and Mers-el-Kebir to Algiers. **Bounds 35.0 N to 40.5 N
   and 5.0 W to 4.5 E, abutting `strait` at 5 W exactly** (its east bound), the fetch box
   widened as the form says; a bound moved to a tile column's or row's edge where a mark
   asks it. The coast north of Cape Palos (Alicante, Valencia, Barcelona) and the
   Algerian coast east of Algiers are later blocks and are said so. The block is the
   largest yet (about fifty square degrees, two thirds open water): the level-2 tiles go
   where the how-to puts them, and **before the tiles are committed the package reports
   their count and bytes; past 40 MB it stops at the report and the lead rules** (a tile
   column of deep water dropped, or a second region) rather than committing the lot.
2. **The harbour patches** (level 3, about 15′ by 15′ each): Málaga; Almería; Cartagena;
   Palma; Port Mahon; Ivica town; Oran with Mers-el-Kebir; Algiers. Tetuan, Melilla and
   Alcudia are roads and marks without a patch unless a sheet is read for them. The seam
   rule for the tiles `strait` lists, as the how-to has it.
3. **The period data.** The Spanish coast from Tofiño's plans and derrotero where fetched,
   the Balearics the same with Heather's and Michelot's directions, the Barbary coast from
   Roux's plans and the directions (Algiers' mole and the Peñon; Oran's two harbours);
   the period shoreline where it differs from the modern (Málaga's and Algiers' later
   moles, Cartagena's arsenal as 1805 had it, Mahon's lazaretto and the island hospital);
   the lights of 1805 dated (few: the directions name Málaga's and Mahon's; the rest are
   towers, which are marks by day), so that 1805 sees what 1805 had. Every source fetched
   goes under `docs/references/` with its README row, read as data and never run; where
   a sheet cannot be fetched or its datum read, the port file says `datum: unverified`
   and no figure is invented.
4. **The ports** on package 35's machinery, each a file: Málaga, Almería, Cartagena (the
   King of Spain's arsenal: a yard as Ferrol's), Palma, Port Mahon (British until Amiens
   gave it back in 1802, Spanish in 1805, the yard and the hospital island noted), Ivica,
   Oran (Spanish until 1792, the regency's in 1805), Algiers; each with its nation, its
   state (the Spanish ports hostile to a King's ship from December 1804, by 79a's dated
   form; the regency's ports at peace with Britain by treaty, their cruisers noted in the
   file's head and not modelled), its road, pilot's station, market, yard, pool and the
   pilot's four words, every `feature:` spot with its position beside it; entered in the
   nations' index and `test_ports.py`'s list. **One new nation, data alone**: `algiers`,
   the regency, in `data/nations.yaml` in Morocco's form (its colours, its regime's rows,
   its dated dealings with Britain, France and Spain from the sources on file, and no code
   of its own); 79a left the Mediterranean's nations to this block and 79d, by name.
5. **The tide.** The Mediterranean's is small (a foot or two at Málaga, inches at Mahon)
   and the directions say so: TICON's gauges of the block read as every block's are
   (Málaga, Almería, Alicante if within the box, Palma, Mahon, Algiers: unverified until
   read), **held** under `held_gauges:` unless package 89 is merged before this step, in
   which case they go in by 89's form with their `block:`; the eleven do not move either
   way. The streams by the directions: the Strait's inset current already in 39f's area
   is not this block's; the block's own areas are the surface set along the Spanish coast
   and the Barbary coast as the pilots give it (the current running east along Barbary,
   a knot or less), with `current:` where the period gives a set and no tide, an area over
   the block's whole box after them, and the box appended to `book_limits`. The master's
   epitome places with the period's rise where a pilot gives one (Norie's and Heather's
   few), else the world's. The polygons kept off the water the recorded passages' sail use
   (none reaches the block; say so in the notes).
6. **The weather.** No box of `climatology.yaml` covers the Mediterranean; `box_at` would
   answer with the nearest Atlantic box, which is wrong (the Levanter and the Poniente in
   the Strait's approaches, the Alboran's easterlies, the Balearics' winter northerlies).
   **A new box** `mediterranean-west` over the block's bounds, its twelve rows from a
   printed table where one is read (the *Mediterranean Pilot*'s wind tables for Gibraltar,
   Málaga, Mahon and Algiers; modern normals from a public source named in the row's note
   otherwise), each row's source said, judgement said as judgement. `test_weather.py` holds
   the box's rows to the file's form as the Channel's are held.
7. **A scenario** `mahon.yaml`: the frigate from Gibraltar bay to Port Mahon by the Spanish
   coast and the Balearic channels in 1805, the Spanish ports hostile, `chart:
   atlantic-east`, sailed once at seed 7 to the anchor by a short book, its figures in the
   notes; not pinned.
8. **The build**: `python tools/build_charts.py --region mediterranean-west` through the
   proxy, the checks printed and passing, the tiles committed within item 1's rule, the
   manifest with every other entry carried over, the region appended to
   `CHARTS["atlantic-east"]["regions"]` after `strait` and the chart's title amended to
   name the Mediterranean's west (the level-1 Atlantic reaches 20 E, so no new chart is
   needed; say so in the notes), and after the build `git status` showing no change to
   any tile, coast or index another region lists. Build early, to fetch; rebuild with
   `--skip-fetch` after the marks are written.
9. **Truths 7-285 to 7-294**: the lookout off Europa Point sees the Sierra's marks and the
   Barbary coast's as the directions give their ranges; a ship bound east from the Strait
   is set by the surface current as the pilots say (the master's account against the
   world's water); the Balearic channels are entered on their marks; Port Mahon's
   entrance holds a frigate at the anchor in a northerly; the Spanish ports refuse a
   King's ship in 1805 and the regency's receive her; the seam at 5 W is crossed with the
   business carried; and what the build earns, each a behaviour.
10. **The records**: the tuning notes' section (the research pass's report; the sources
    with their licences; the patches' datums and residuals; the checks as printed; the
    scenario's run; what was found on the way; the suite as run: the fast tier whole on
    the final tree, the chart's, the ports', the tide's, the weather's, the nations' and the
    scenarios' slow tests, the recorded passages of the Channel west, `gate_5b` and
    `gate_5c` once by name, which must pass to the digest); `ChartBlocks.md` corrected
    where the how-to proved wrong; spec M6 §26's as-built list extended by the block and
    M7 §28's pointer.

The hard rules as every brief has them; `claude/pkg-79c`, pushed after each commit, the
research pass first on its own; the lead merges. No CLAUDE.md is in the repository: the
briefs' heads and the records serve.

## Package 79d: the Gulf of Lion and the Tyrrhenian (`gulf-of-lion` and `tyrrhenian`, two regions in one package; `tools/build_charts.py` `REGIONS` and `CHARTS`; `data/charts/` each region's tiles, coast, index and manifest entry, `features/<region>.yaml`, `overrides/<region>/`; `data/ports/*.yaml` new per port; `data/nations.yaml` the ports' index and the Italian states; `data/tides/constituents.yaml`, `streams.yaml`, `establishments.yaml`; `data/weather/climatology.yaml` two boxes; `data/scenarios/agincourt-sound.yaml` new; `docs/references/README.md`; `docs/dev/ChartBlocks.md`; `docs/TechnicalSpec-M7.md` §28's pointer; `docs/dev/TuningNotes.md`; the same tests, `test_known_truths.py` truths 7-295 to 7-304)

Opus. The fourth of 79's four packages: Toulon, Corsica, Sardinia, Elba and Naples (the
owner, 2026-10-29), **launched once 79c's research pass is pushed** and built from its
texts; otherwise beside 79c, sharing no file but the chart builder's tables, the
manifest, the nations' index, the tide's and the weather's files, which the lead merges
(79a and 79b were merged so). Read what 79c's brief says to read, and 79c's pass's report.
Because the water is wide, **two regions**, each built, checked and committed in turn with
its own patches, ports, tide, weather box and truths, the first whole before the second
begins:

1. **`gulf-of-lion`**: from the Spanish border by Cape Creus to the Rhône, Marseille, Toulon
   and the Hyères islands, Fréjus, Antibes, Nice, Villefranche and Genoa, Leghorn and the
   Tuscan coast to Piombino, Elba and the Tuscan islands, Corsica whole (Cape Corse, San
   Fiorenzo bay, Bastia, Calvi, Ajaccio, Bonifacio), and the Maddalena islands with
   Agincourt Sound, which Nelson's fleet used against Toulon in 1803 to 1805. **Bounds 41.0 N
   to 44.5 N and 3.0 E to 11.0 E**, the west bound 1.5° inside 79c's east bound so that the
   two overlap nowhere a mark lies (79c reaches Minorca; the open water between is
   either's by the how-to's seam rule, said in both notes); a bound moved to a tile edge
   where a mark asks it. The harbour patches: Toulon with its roads; Marseille; the Hyères
   road; Villefranche; Genoa; Leghorn; Porto Ferrajo; San Fiorenzo; Ajaccio; Agincourt
   Sound. The ports: Toulon (French, the fleet's port, hostile: the watch off it the
   period's whole business), Marseille, Hyères, Villefranche, Genoa (the Ligurian Republic
   until its annexation to France in June 1805, dated by 79a's form), Leghorn (the Kingdom
   of Etruria, neutral and French-leaning), Porto Ferrajo (French from 1802), Bastia,
   Ajaccio, San Fiorenzo, and the Maddalena (the King of Sardinia's, Nelson's watering).
2. **`tyrrhenian`**: Sardinia whole (Cagliari, the Gulf of Palmas, Alghero, the strait of
   Bonifacio from the south), the Italian coast from Piombino by Civita Vecchia and the Tiber
   to Gaeta, the bay of Naples with Ischia, Procida and Capri, and south to the Gulf of
   Salerno and Cape Palinuro; Ponza. **Bounds 38.5 N to 42.5 N and 8.0 E to 15.5 E**, sharing
   its north-west with `gulf-of-lion` by the seam rule (the boundary between them drawn at
   a tile row's edge and said in both notes, so no tile is built twice). Sicily, the
   Lipari islands and the Strait of Messina are a later block and are said so. The harbour
   patches: Cagliari; Alghero; Civita Vecchia; Gaeta; Naples; Ponza. The ports: Cagliari
   (the King of Sardinia's, at peace with Britain), Alghero, Civita Vecchia (the Papal
   state's), Gaeta and Naples (the Kingdom of Naples, neutral under a treaty with France
   until the French occupation of 1806, dated).
3. **The period data, the ports, the tide, the weather, the scenario, the build and the
   records as 79c's brief has them, region by region**, with these particulars: **the
   nations, data alone**, as 79c adds Algiers: `sardinia` (the King of Sardinia, at Cagliari
   since 1799), `naples` (the Two Sicilies' crown of 1805), `etruria`, `liguria` (annexed
   June 1805, after which Genoa is France's by the dated form) and the Papal state, each in
   Morocco's form with its dated dealings from the sources on file, none with code of its
   own; the French ports hostile; **the weather** two new boxes, `gulf-of-lion` (the
   Mistral and the Tramontane, the Gulf's winter gales, from a printed table where one is
   read) and `tyrrhenian`; **the tide** the basins' small water, the gauges held or by 89's
   form as 79c's rule has it, the currents of the directions (the set along the Riviera and
   through Bonifacio) as `current:`; **the scenario** `agincourt-sound.yaml`: the frigate
   from the Maddalena to look into Toulon and back in 1805, the French fleet in port noted
   and not modelled, `chart: atlantic-east`, sailed once at seed 7; **the tiles** within
   79c's 40 MB rule for each region, the count and bytes reported before each commit;
   **the truths** 7-295 to 7-299 the Gulf's (the Mistral's gale from the north-west in the
   Gulf's winter row; Toulon's roads seen from the Hyères islands; Agincourt Sound holding
   a fleet; the Bonifacio strait entered on its marks; Genoa's state before and after June
   1805) and 7-300 to 7-304 the Tyrrhenian's (the bay of Naples' marks; Cagliari's
   reception; the seam between the two regions crossed with the business carried; and what
   the build earns), each a behaviour.

The hard rules as every brief has them; `claude/pkg-79d`, pushed after each commit, the
first region's commits before the second's; the lead merges. No CLAUDE.md is in the
repository: the briefs' heads and the records serve. **For the owner:** this is the larger
of the two by water and by ports, and if its first region fills the package's time the
second may be split off as 79e by the owner's word, nothing of the first redone.

## Package 89: the held gauges' water (`freesail/world/tide.py` the blend; `data/tides/constituents.yaml` the held gauges given their water; `data/tides/establishments.yaml` the rises by the same water; `docs/references/Tides.md`; `docs/dev/ChartBlocks.md` item 6 rewritten; `docs/TechnicalSpec-M7.md` §28 as built; `docs/dev/TuningNotes.md`; `tests/test_tide.py`, `test_known_truths.py` truths 7-280 to 7-284)

Opus. Independent of 84 and of 75. The finding every chart block since 39a has carried and
79b made pressing: the world's tide blends every gauge within `reach_nm` (400 miles) of a
position, so a gauge added to `gauges:` enters the blend at Falmouth and moves every
recorded passage's digest, and the blocks' gauges (Bournemouth and Portsmouth, Biscay
north's nine, Vigo, Portugal's five, the islands' five, the Channel east's six) have been
read, verified and **held** under `held_gauges:`, the world's tide over their water the
eleven's blend and wrong: at Newhaven the world's spring range is 3.9 feet for the gauge's
19.5, at Dieppe 5.3 for 27, at Beachy Head 4.8 for Norie's 20 (79b's tuning notes), over
Biscay the Channel's tide (39b's), at Cape Trafalgar Le Conquet's eighteen feet (39f's), **and over the Balearics Saint-Malo's, a mean level of 6.83 m and an M2 of 3.7 m where Mahón's is five centimetres (79c's), the block's nine gauges held with their mean levels verified from REDMAR so that the blend gives the Mediterranean its own foot of tide at once; and over the Gulf of Lion and the Tyrrhenian Le Conquet's alone, two metres of M2 against the gauges' five to twelve centimetres, the master's account allowing a flood in a sea that has none to speak of (79d's)**. Read
`docs/dev/ChartBlocks.md` item 6, `docs/references/Tides.md`, the tide module's head and the
blocks' tuning notes on their gauges before anything.

1. **The rule.** A held gauge serves the positions within its own block's bounds (the region
   of `data/charts/manifest.yaml` its block names) and no position outside them; the eleven
   serve as they do today everywhere. Within a block the blend is the eleven within reach
   **and** the block's gauges, by the present weighting; outside it the eleven alone. So no
   position in `channel-west` or west of 1 W in `channel-mid` reads anything new, and every
   recorded passage's digest stands: that is the test, run first and last (the eleven
   passage tests by name, `gate_5b` and `gate_5c`, the trials' digests, as 79b's notes list
   them). Where the lead's rule would move a Channel-west or Channel-mid passage all the
   same (a passage that reaches into a block), the package stops and says which and why,
   with the old figure beside the new, and the lead rules; it does not re-pin.
2. **The data.** `held_gauges:` becomes `gauges:` entries each with its `block:` (the region
   id), the eleven with none; the loader refuses a held gauge without a block and a block
   the manifest does not name; the form is otherwise the eleven's. Newhaven's mean level
   stays null and is said unverified; nothing of the figures moves.
3. **The epitome.** The master's table's `rise_judgement` places (the 37j rule: the world's
   spring range at the place to the foot) read the same water, so a rise over a block is the
   block's own; Norie's and Moore's given rises do not move. The tuning notes list each
   place whose judged rise changes, old beside new.
4. **The words.** `ChartBlocks.md` item 6 rewritten for the rule (a block's gauges go in
   `gauges:` with their `block:`, verified, and the test that no recorded passage moves is
   the block's); `Tides.md`; spec §28 as built. Nothing a reading says changes in its form.
5. **Truths 7-280 to 7-284:** the world's spring range at Newhaven, Dieppe and Beachy Head
   within a foot of the gauge's and Norie's; at Vigo and Cadiz within a foot of their
   gauges'; a position a mile west of 1 W in `channel-mid` reading the same tide to the
   centimetre as before the package, and one a mile east reading the block's; every
   recorded passage's digest unchanged (the eleven and the gate's two, by name); the pace of
   the tide's blend unchanged within the measure (the blend adds a membership, not a gauge).
6. **The suites:** the fast tier whole on the final tree; `test_tide.py`, `test_chart.py`,
   `test_scenarios.py` and the recorded passages in the slow tier; the whole suite is the
   lead's in the cloud at the merge.

The hard rules as every brief has them; `claude/pkg-89`, pushed after each commit; the lead
merges. No CLAUDE.md is in the repository: the briefs' heads and the records serve.

## Package 82: the boat as a vessel, and the player aboard another ship (`freesail/core/world.py`, `ui/console.py`, `ui/server.py`, the drivers: the followed ship; `freesail/world/crews.py`, `ships.py`, `people.py`, `places.py`, `stations.py`, `seats.py`, `orders.py` a person aboard another ship and the seat that follows him; `freesail/core/replay.py` the station on another ship replayed; `freesail/physics/` an oar force on a hull (new, by the brief's leave); `freesail/evolutions/` the boat's orders and the tow; `data/ships/boat-*.yaml` through `tools/gen_ships.py`; `freesail/world/movement.py`, `ports.py` the boat's errands as they are; `freesail/api/readings.py` the readings following the person; `freesail/agents/harness.py`, `director.py`, `data/director/`; the viewer (`client/`) drawing the boat; `docs/TechnicalSpec-M7b.md` §11, §12, §21k as built; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7b-113, 7b-114 and the M7 numbers after 73's)

Fable; brought forward by the owner on 2026-10-24 to run after 73 and before 74, because
74's captive is a person aboard another ship and its prize crew goes aboard by boat. Spec
M7b §11 (a world with no player's ship: the followed ship in place of the given one), §12
(the player on another ship and the replay of a station there) and §21k (towing by the
boat, and the boat as a vessel), with their truths 7b-113 and 7b-114; M7b's packages 51 and
63 on the books (this package takes the heart of 51 and all of 63; 51 keeps the director's
chart and focus, §12a and §12b, for a later brief); 68's refusal of a person made aboard
another ship (R-15) and 67's seat (every station of the player's ship seatable, a seat at a
person as a voice, one aboard another ship refused for want of a World of people); 53's
places and 66's line; the owner's own tests of the kedge and the boat (M7b spec §21k's
head). **Generously scoped as the M7 packages are:** the brief binds the intent and names
the ground, the builder designs, takes an item another way with its reason, grows a part
where the work shows it should, and says what it left and why; no day count. **The followed
ship and the person's movement between ships are designed first and written down before
they are built** (a design note under `docs/design/`), because 74 builds the captive on
them. Each item an intent with the lead's reading; the intent binds.

1. **The followed ship in place of the given one (§11).** The game's centre (the
   promotion's, the chart's, the pace rule's, the readings', the lookout's, the reckoning's,
   the drivers') follows a ship rather than being the one ship given at the start: the
   player's ship the followed ship by default, so nothing recorded moves; a scenario with
   no player's ship (`ship: none`, `director: observe`) running its business and its ships
   under their captains with the centre wherever the observer looks (`follow "Palinure"`,
   the chart's view), the readings that assume a ship answering "no ship followed" in words,
   the ship's orders refused in words, the world orders standing, the console and the
   browser opening at the director's station. *The lead's reading of the cost* stands as the
   spec has it: the World's construction assumes a ship in several places, and the package
   measures what moved (nothing pinned should).
2. **The player on another ship, and the seat that follows the person (§12; 67 and 68).**
   `--seat captain --ship <id>` for the player, seated under the same contract as a model
   there, the drivers' centre following the ship he is aboard; **a person aboard another
   ship made real**: the player and any person may be aboard a ship not the given one, that
   ship given her World of people as the cap promotes her (68's refusal lifted and 67's
   "one aboard another ship" seatable), his place and his voice there as 53's places and
   66's line have them, the readings his ship's while he is in her; **the person moving
   between ships** by the boat (item 4), by boarding (73's deck won) and by capture (74's
   captive, the hook left: a person put aboard the captor with his station's seat following
   him or standing down by the handover's rule); the director's `aboard:` and `ship "X":`
   forms reaching a person on any ship. The design question is the seat: a station is a
   person aboard, so a person who changes ships keeps his station and the ship under it
   changes, or the station ends and a new one begins on the other ship with the same holder;
   the builder decides and writes why (the replay and the consent's record must both hold).
3. **The replay of a station on another ship (§12).** A save with a station on another
   ship replays that station's acts as it replays the player's (the checkpoint carries the
   other ship whole; the acts keyed by ship), and a person who moved between ships in play
   moves the same in the replay to the same digest.
4. **The boat as a vessel (§21k).** Each ship's boat a ship file through the generator (a
   16-ft boat with four oars and a sprit or lug stepped at will; the frigate's launch and
   cutter larger; with sources or the word judgement), a vessel of the world when manned
   and away from the ship (crewed by the promotion's machinery, her own World, small), **an
   oar force on a hull** as her propulsion by the hands at the oars and their fatigue (the
   one physics addition this brief allows, with its source) and the sail when stepped; the
   sweeps' orders (`give way`, `lie on your oars`, `step the mast`, `set the lug`, `pull
   for <the point>`); **the player aboard her** by `go to the boat` and item 2's seat, her
   readings his while he is in her and the ship's again when he comes aboard; the errands
   (ashore, the kedge, the tow, the pilot, the prices) done by her as before when nobody is
   in her; the viewer drawing her under oars or sail; the account following the boat as a
   vessel's; the boat lost (stove, swamped, cut adrift) as a state the ship's file knows.
5. **Towing by the boat, and the kedge's false denial (§21k).** `tow her with the boat [to
   <the point or bearing>]`: the boat ahead on a tow-line with her oars, the ship's head
   brought round or the ship moved at the boat's pace against her resistance and the tide
   (a quarter of a knot to a knot for a cutter or a lugger by the boat's size and hands;
   little or nothing for the frigate, whose boats towed her head round in a calm and no
   more: the period's practice, a judgement in the notes), the boat's crew tiring by the
   hour, `the boat alongside` ending it, refused in a sea the boat cannot work in; the same
   oar force for the tow and for the boat herself; the kedge's false denial ("the boat was
   not sent away" while the lay-out went on) mended, kedging itself left to the anchor
   physics it is in.
6. **The stations, the director and the readings.** `the boat`, `the boats`, `where am I`
   answering the ship or the boat the person is in, `the followed ship`; the events and
   tripwires (`the boat away`, `the boat alongside`, `aboard the <ship>`); the director's
   forms after `WORLD_ORDER_FORMS` (`follow "X"`, a person put aboard another ship, the
   boat sent); the harness's samples following the person's ship; the truth showing every
   boat as a vessel when she is one.
7. **Truths and records.** Truths 7b-113 (the lugger becalmed with the ebb setting her
   toward the Lavandière towed clear by her boat at half a knot; the frigate's boats bring
   her head round in a calm and move her no distance worth the account's notice) and 7b-114
   (the player in the cutter's boat pulls ashore at Falmouth from Carrick Road under oars,
   steps the mast and sails her back under her lug, the readings his in the boat and the
   ship's again aboard; the boat's errands run as before with nobody in her), and M7 truths
   numbered from the first after 73's (a world with no player's ship runs a day with its
   business and the centre on the followed ship, nothing pinned moved; the player seated as
   captain of another ship with the player's ship brainless and far; a person moved from
   one ship to another by the boat in play and in the replay to the same digest; the
   director's `follow`); spec M7b §11, §12 and §21k "as built"; the Harness (the seat on
   another ship, the readings following the person); a chapter of the primer (the boat; going
   aboard another ship); the director's library; the tuning notes (the design or its
   pointer, each item, what moved and its proof by bisection, the pins old beside new,
   found on the way, decisions, the suite as run); the fast tier, the slow tier of the
   touched files, the whole slow tier when the machine is quiet, the pace tests alone and
   last.

**Not built here:** the director's chart and focus (§12a, §12b; 51's remainder); the boats
as fighting vessels and cutting out (77); the captive's channel itself (74, on item 2's
hook); the prize crew (74). **The head rules bind** as the briefs before have them: no model
identifier; nothing under `docs/agents/consent/` touched (a seat on another ship is read
from the consent record as 67 reads it; if the brief's words do not cover it, the seat is
refused in words and the gap named for 55); a world order never shown as sent; the ship
files through the generator with sources; the pins re-measured only where a change moves
them, old beside new, proven by bisection (the followed ship should move nothing pinned:
if it does, that is a finding); never a test skipped, disabled or quarantined; realism,
not pacing; the physics read and not changed but for the oar force this brief names.

**From the owner's local work, folded in by package 86** (the review of it, section 5):
three of the fixes lean on today's player-centric seam and are 82's to rework with the
person aboard another ship: the free intent (`ship "X": intent <words>` taking unreadable
words as the goal told to a model at her captain's station, the scenario's `free_intent:`,
the rules captain lying her to; `captains.FREE`), the hail's rule that the player's ship
with nobody's rules captain commanding waits for `say to her` (`hail.model_holds_her`, the
player's ship only, by `parent is None`), and keeping station on the player's ship by her
name (`orders/station._named_or_kind`, by `player_shadow` and the id 'the ship'). The hoy
as a vessel was deferred to 82 as well.

## Package 83: the one-world study (`docs/design/Design-OneWorld.md` new; a draft brief for package 84 in this file; throwaway measurements in the scratchpad only; no code in the repository)

Fable; a design study and no code, launched 2026-10-27 beside 73 on the owner's word that
the usage is to be spent now and the refactor planned smartly before more is built on the
old seam. Decision 52 (`docs/DesignProposal.md`) is the frame; the owner's debrief
(`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/debrief.md`) and his twelve notes
(`owner-notes-2026-10-27.txt` beside it, notes 2, 9, 11 and 12) are the evidence; his
acceptance test is in the decision. The study reads the world as it is and designs the world
as it should be, costs the road between, and writes both down. Each item an intent with the
lead's reading; the intent binds; the study may take an item another way with its reason.

1. **The world as it is: the seam named.** How the game's one World holds the player's ship,
   her people, places and things, the ports and their people, the business, the weather,
   the sets, the director; how a far body lives in it (`ships.py`, `brains.py`, 72's sets);
   what the promotion under the cap builds for a crewed ship today (`crews.py`'s
   CrewedWorld, `_crew_scenario`, the mirror between the far state and the near body, what
   is copied and what is cut: no ports, no people ashore, no things, no market, the
   director's hand only by the forms that name a ship); how a station's harness, the doors
   and the seats (67) bind to a World; how the replay and the save (`core/replay.py`, the
   checkpoint keyed by ship) rebuild it; how the pace rule and the cap centre on the player's
   ship. Written as a map with the files and the objects named, the player-centric
   assumptions listed one by one (the lead's count of them is the study's first finding).
2. **The world as it should be: one world, many crewed hulls.** The design: one World that
   the player is in and so is everyone else; a crewed ship a hull in it with her own
   people, places aboard, bill, log and stations, the player's ship one such hull; the
   ports, the people ashore, the things, the markets, the business, the weather, the sets,
   the chart and the director's hand the world's once; a person a person of the world who
   may be aboard any hull or ashore, moved between them (82's boat, 73's boarding, 74's
   capture) with his station following him; **the person's coarse acts possible anywhere**
   at far detail (go ashore, trade, speak to a person, take a thing, anchor, sail for a
   port, chase, report) by the far brain's and the business's own means, the full-detail
   hull only where the cap gives it, nothing coded out (the owner's bound); the station's
   readings, samples and deltas (58a) per hull; the director's reach the world's (his forms,
   his truth, his `say as`); the replay and the save of a world with several crewed hulls
   and persons who moved. The leaders of nations and companies as **abstract stationed
   roles** (M8's; rules or model, biased and competitive, perhaps never seen as a person)
   left room for in the design: a role that holds reins of the naval system (72's regimes)
   and the business, with a station's contract and a sample of its own. Say what a model at
   another ship's captain's station sees and may do under this design, and what the owner's
   acceptance test looks like step by step in it.
3. **The two roads costed, honestly.** One World with many hulls (the lead's instinct)
   against many Worlds sharing the world's state (the cheaper reach); for each: what moves
   in the code (files, objects, the count of player-centric assumptions it removes or keeps),
   what it costs in pace (the baseline 95 ticks a second with twelve crewed ships and the
   conftest's floors; measure what you can on the present code with throwaway scripts in
   the scratchpad), what the recorded passages lose (which pins move and why; the aim is
   none), what the consent brief's words assume (a station on "the ship"; read
   `docs/agents/ConsentBrief.md` and say where its wording would no longer be true, without
   editing it: that is 55's), what 82, 74, 75 and 77 gain or must wait for. Recommend one
   road, with the reason.
4. **The migration in steps that keep the suite green.** The refactor (84) as an ordered
   list of steps, each a mergeable state with the whole suite passing and the pins standing
   (or the few that must move, named with why), so that the work can be built by one Fable
   package in stages or by sibling builders in parallel where the steps are independent;
   each step with its files, its tests, its risk and its rollback; the step at which the
   owner's acceptance test first passes whole; the step at which 82's boat and 74's captive
   become simple. The steps are the brief of 84, drafted in this file as "## Package 84"
   for the lead and the owner.
5. **Found on the way, and the open decisions.** Everything the reading shows that is wrong
   today and not the seam's (the convoy's stall, the colours flickering, the tender's "no
   port in the world", whatever else), listed for the lead; the decisions only the owner can
   take (how far a far person's acts go in the first step; whether a far hull's log is kept
   for every ship or only for ships with a stationed person; the pace bound he accepts;
   whether the leaders' roles come in M8 or earlier), each with the study's recommendation.

**Not done here:** no code change in the repository; no edit to the consent files; no pin
moved. **The head rules bind:** no model identifier in any file; the design note and the
draft brief are the deliverables, committed on the study's branch and pushed to
`claude/pkg-83` after each commit (the owner's permission of 2026-10-27).

## Package 85: the orders, the primer and the library for a model reader (`docs/primer/*`, `docs/agents/Harness.md`, the library's topics (`freesail/agents/tools.py`, `data/director/` and the stations' briefs), `data/vocabulary.yaml` and `freesail/orders/` the grammar, `freesail/api/readings.py` the date and the war, `freesail/world/papers` and `data/papers/papers.yaml` the news of the war, `freesail/agents/harness.py` the stand-by's words and the action's severities; a new test over the primer and the library; `docs/dev/` a record of what was redacted and where it went; `docs/dev/TuningNotes.md`; tests beside each)

Fable; a review that mends what it finds, by the owner's word of 2026-10-27, to run after
83's design is read and beside or after 84 as the usage allows. The evidence: the owner's
notes 3 to 6 (`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/owner-notes-2026-10-27.txt`),
the model officer's five friction points (`model-officer-review.md` beside it), the
dispatches test's and the Roscoff station's findings in the tuning notes, and the owner's
reading of the door logs (a model reasoning the war's state from the primer's pilot example;
a model taking a primer's pilot's news as its own voyage's; a model calling out the wrong
flag numbers from a generic signal page). Each item an intent with the lead's reading; the
intent binds.

1. **The rule, stated once and enforced.** The primer and the library are in-world documents
   for whoever reads them, human or model, at any station, in any scenario, on any ship.
   Nothing in them may be true only for one scenario, one signal book, one ship, one voyage
   or one stage of the build: no particular signal book presented as the reader's (a general
   page on signals says how a book is read and that the ship's papers hold hers); no pilot's
   news, price or stranger given as if of the reader's own voyage unless marked as an example
   and set apart; no reference to milestones, packages, gates, builders, the owner, the lead,
   a model, an instance, a playtest or the development at all. **Redact aggressively**; what
   is cut and still worth keeping (the examples from real voyages, the figures' provenance,
   the history of a page) goes to a record under `docs/dev/` (for instance
   `docs/dev/PrimerRedactions.md`) with the page it came from. A test over `docs/primer/` and
   the library's rendered topics guards the rule by a list of forbidden words and patterns
   (the milestone and package numbers, "the owner", "the lead", "builder", "playtest",
   "gate", model and vendor names, the scenarios' names where not the primer's own worked
   example) with an allow-list for the few words that are in-world too, and fails when one
   returns.
2. **Categorised, complete, correct.** The primer's chapters and the library's topics read
   as one book: what a station may do, where to find each thing, the grammar in one place
   with every order form the game accepts (the dialect's forms generated or checked against
   the vocabulary by a test, so that no order the game takes is missing from the book and no
   form the book gives is refused), the readings listed with what each answers, the events
   and tripwires, the director's forms where the director's library is concerned; the voice
   in one grammar (`hail the <sail> <words>` with the colon optional, `say to`, the lookout's
   `hail`), and the briefs and tool descriptions telling a model that it may move about the
   ship, eat, drink, read, say and say to, go ashore (the owner's note 3).
3. **The date, and the war, as readings.** The date and the ship's time as a reading in
   words (`the date`, in every sample's first line or on request; the owner's note 4); the
   war's state as the ship knows it: the knowledge she sailed with (the nations' table as
   of the scenario's start, in her papers) and every change the news brought in from a port
   or a pilot logged in the papers as the prices are, readable as `the war` (note 5), never
   deduced from a primer's example.
4. **The stand-by's words, and the action's severities.** A reply that batches orders before
   a `stand_by` says "not run" only of the calls after it, and names the ones that ran; in
   action at 1x the discharges and the trim steps carry the severity that lets a stand-by on
   "a notable event" wake for what matters (a hit, a strike, a change of state) and not for
   every shot, with the owner's "the flow of the game through the log" as the measure, and
   the same read for the human's log; the two signal books in the papers made one (the
   ship's own; the generic page says whose it is not).
5. **The ship herself, said plainly (the owner, 2026-10-27).** Models at a station have
   almost never been told what ship they are on, and sometimes not her name; they reason it
   out or guess, usually right, and learn it over time. Every station's brief says, at the
   seating and after a fold, her name, her rig and class (a 36-gun frigate, a cutter, a
   topsail schooner), her service (a King's ship, a merchantman, a privateer, a packet, a
   fisherman) and nation, her fit of guns, her port and her people's number, and who
   commands; and a reading `the ship` (or `what ship`, `my ship`) answers the same at any
   time, from the ship's own papers and muster, so that no model has to deduce where it
   stands.
6. **Found on the way, and the records.** Everything else the reading shows (79c's finding: a standing order's name with an apostrophe is refused with "After the name say a colon", the grammar's; the hail
   resolving to a far lugger over the wreck in sight, the `captain: carry on` collision with
   the director's form, `gybe the mainsail`'s answer); the record of redactions; the tuning
   notes; the Harness; the suite as run (the fast tier, the slow tier of the touched files,
   the whole slow tier when quiet, the pace tests alone and last).
7. **The interim gate's draft (the owner, 2026-10-29).** The last gate document is M6c's
   (`docs/gates/gate-m6c.md`); the owner's next playtests are after package 84 completes and
   after package 75's *Indefatigable* is in, and the documentation is to be brought up to date
   before them. This package's reviewer, primed by the reading above, drafts
   `docs/gates/gate-m7-interim.md` as its last deliverable: not a full gate, but **where M7
   stands since M6c** from the player's and the reader's side (what a captain, an officer and
   a model at a station can now do and read, package by package 70 to 86 and 84's steps, as
   the records have them), **the open items** it finds in the records (the playtests of
   70 to 72 and their debrief, the model officer's points, the tuning notes' "open" and
   "noted" lines, the pins moved and why, the container floors and the pictures' threshold),
   and **suggested tests for the two playtests**: after 84 (the one world: a station on a far
   ship, the tender's day, two crewed strangers signalling and fighting on one clock, a save
   with many hulls replayed, the pace with hulls asleep) and after the first new ship (the
   64 and the razee: her fits, her mizen course and driver, her gun decks and the lee ports,
   the pictures, a scenario of 1796). The lead adds the engine's and the world's half from
   the as-merged records (84's eleven steps, 86, 73, the suites' figures, what 88 is booked to
   mend) and anything the draft missed, and the owner reads the whole before the playtest.
   Runs after 84's last step is merged; the draft's engine half may be begun by the lead
   before that.
8. **The documentation whole (the owner, 2026-10-29: "might as well go all the way").** The
   same pass over `docs/` as items 1 and 2 make over the primer and the library: every
   document read for completeness and refinement against the code as it stands after 84
   (the specs' as-built pointers, the agents' documents but for the consent's, the
   references' READMEs, the dev notes' how-tos), a stale line mended or marked as history
   where the record wants it kept, a missing document named for the lead rather than
   written on a guess, and the record of what moved in `docs/dev/` beside item 6's. The
   interim gate's draft (item 7) comes last, after this pass, so that it reads the
   documents as mended. 87's brief waits for this item's merge.

**Not done here:** the one-world refactor (84), the boat (82); any change to
`docs/agents/consent/` or `docs/agents/ConsentBrief.md` (if the brief's wording offends the
rule, say so for 55). **The head rules bind** as the briefs before have them.

## Package 84: the one-world refactor (`freesail/world/hulls.py` new, the Hull; `freesail/core/world.py` the World split and the two-phase tick; `freesail/world/crews.py` the switch alone, `CrewedWorld` retired; `freesail/world/people.py`, `hearing.py`, `movement.py`, `things.py`, `stations.py` one registry of persons and things with the whereabouts; `freesail/world/ports.py` and `dealings.py` new, the ports' half and the hull's half; `freesail/world/ships.py`, `brains.py`, `squadrons.py`, `signals.py`, `signalling.py`, `hail.py`, `combat/action.py` the player's vessel of the sea and `PLAYER_ID` one rule; `freesail/world/business.py`, `data/business.yaml` the far trader's transaction; `freesail/world/orders.py`, `agents/director.py`, `data/director/` the forms with a hull and the truth over the hulls; `freesail/api/readings.py` the station line and the truth; `freesail/agents/harness.py`, `remote.py`, `tools.py`, `seats.py` the hull in the World's place; `freesail/core/replay.py`, `acts.py` the hull on the inputs, the save's hulls block, the checkpoint's converter; `freesail/ui/server.py`, `console.py`, `harbour.py` the followed hull; `docs/TechnicalSpec-M6.md` §19 and §20, `docs/TechnicalSpec-M7b.md` §11, §12 and §12b "as built" pointers; `docs/agents/Harness.md`; the primer; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` the acceptance test as a truth; **84's truths are numbered 7-200 onward**, 75's 7-185 to 7-199, 85's 7-240 onward, so that packages built apart do not collide)

**The suites (2026-10-28):** the fast tier once on the final tree and the slow tier of the touched files; after a mend only the mended test's file; the whole suite is the lead's in the cloud at the merge.

**The owner's eight decisions were taken as the study proposed on 2026-10-27 (decision 53 in `docs/DesignProposal.md`); where an item below says it waits on one, it no longer does, and the log's holding in decision 2 is to be measured for storage before any hull's log is dropped.**

Fable; the refactor of decision 52 on package 83's design (`docs/design/Design-OneWorld.md`:
the world as it is in its part 1, the design in its part 2, the roads costed in its part 3,
the steps in its part 4, the findings and the owner's decisions in its part 5), run after
73 and the owner's local work are merged and after the owner has read the study and taken
its part 5's decisions (each item below says which it waits on). The intent: **one World
that the player is in and so is everyone else**; a ship at full detail a `Hull` of that
World with her own people, places, bill, log and stations, the player's ship one such
hull, the ports, the persons ashore, the things, the markets, the business, the weather,
the sets, the chart and the director's hand the world's once; a hull awake under the
physics or asleep under the plan with her state kept, the cap deciding which wake and
nothing dropped at the switch; a person's coarse acts possible anywhere; the leaders'
offices left room for. **Generously scoped as 70 to 73 were:** the brief binds the intent
and names the ground, the builder designs within the study's design, takes a step another
way with its reason (the study's "what was rejected" read first), grows a part where the
work shows it should, and says what it left and why; no day count. **Each item is a step
of the study's part 4: a mergeable state with the whole suite passing and the pins
standing**, one commit on the branch that reverts whole, pushed to `claude/pkg-84` after
each, so that the lead may merge in parts; the pace truths alone and last at every step,
`tools/pace.py` at steps 5, 6 and 7 with the figures beside the study's 3.2. The study's
three rules for the pins (the followed hull's streams unprefixed and the other hulls seeded
as today, the tick's two phases, the player's vessel last) bind; a pin that moves is proven
by bisection and restored by the order, never re-pinned for the order's sake; the few that
may move as findings (a ship woken twice; a crewed log's ticks) are named with why. Each
item an intent with the lead's reading; the intent binds.

1. **The Hull extracted behind the World's names (step 1).** `hulls.Hull` with every
   per-ship field and method the study's 1.1 lists; `World` keeping the shared fields and
   `world.own`, every per-ship attribute of `World` a property to it; the tick's order
   untouched; `CrewedWorld` untouched; 73's water and muster's states per hull by the
   rename; the checkpoint's converter (`World.__setstate__`) so that the three fixture
   saves and the owner's load by the checkpoint road. *The lead's reading:* pure
   delegation, no pin moves, the proof the slow tier whole; the ground of everything, done
   alone and first.
2. **One registry of persons and things, the whereabouts, hearing by spot (step 2).**
   `People` on the World; `Person.aboard` the hull's id, `Person.home`; the company and the
   aboard as views; the things on the registry; `hearing.spot_of` with the hull; the moves
   writing the whereabouts; the crewed World's `people` the parent's registry filtered to
   her. *Reading:* the acceptance test's step 5 and 6 ground; a world in which nobody
   moves is as it was (53's rule); `People.find` scoped to the hull then the world.
   *Parallel with item 3.*
3. **The ports split: `Ports` the world's, `Dealings` the hull's (step 3).** The port
   files, markets, stances (`stance(port, nation)`), blockades, tracks, yards, pools and
   the jobs of every hull in `Ports`; the pilot and his conn, the cutter, the boat and its
   errands, the price lists, `lay_in`, `trade`, `trade_list`, `enter_hands` in a hull's
   `Dealings`; the crewed World given the parent's `Ports` and her own `Dealings`, so that
   the tender goes ashore at full detail. *Reading:* the largest file; the player's dealings
   the same state in another class; the passages' pilot lines at their ticks the proof.
   *Parallel with item 2.*
4. **The coarse acts on a sleeping ship, and the far brain's port acts (step 4).**
   `submit_far` routing by "needs no physics" (the person's acts, the port's acts, the free
   lines, the conversation, the signals through the grammar; the plan's words to
   `far_order`); `far_order`'s course by the port's track and under the land guard; the far
   brain transacting at her port under `data/business.yaml`'s `transact:` knob (the owner's
   decision 5); `shape_words` naming the coarse forms. **The owner's acceptance test as a
   truth here**: a fake captain of the tender ordered from Torbay to Plymouth by signal,
   by the track, ashore to a person made there, back with a thing, home within hail, the
   lugger passed and not fought until 74. *Reading:* how far the acts go is the owner's
   decision 1, recommended whole; the business off in every recorded scenario, so no pin.
5. **The ship persists: sleep and wake in place of drop and remake (step 5).** The
   demotion a sleep with the physics off, the promotion a wake without remaking her ship,
   a hull made once and her `Rng` made once; `Vessel.damage` from the parts at sleep; the
   checkpoint's bound stated per hull (the owner's decision 2 on which logs are kept).
   *Reading:* a ship woken twice may move as a finding; truth 88's pace with the sleeping
   Worlds beside.
6. **The Hull the container; `CrewedWorld` retired; the two-phase tick (step 6).** One
   clock; her own log; `World.tick` over `world.hulls` in the study's two phases (the
   bodies move, the other hulls see and act, the far minute, the followed hull last);
   `tick_hulls`, `all_agents`, `Harness(hull)`, `hull_for`, `hand` one road, `hull.vessels`;
   the hull's own sea, motion and conditions at her place (the study's findings 5 and 6).
   *Reading:* the one step where a pin can move for the order's sake, and the order is
   the mend; `CrewedWorld` kept as a name for the unpickler alone.
7. **The player's ship a hull among the hulls; the shadow retired (step 7).**
   `world.followed`; the player's `Vessel` of the sea appended last; `strangers_of(viewer)`;
   the sixty-six `PLAYER_ID` cases one rule and `PLAYER_ID` defined once; a hull at anchor
   or in port awake under the cap's order with the stationed hull first (the owner's
   decisions 3 and 6). *Reading:* 82's followed ship and 74's captive become simple here;
   the nearest-first orders by the study's rule 3.
8. **The save and the replay of many hulls (step 8).** The hull on each input, the save's
   `hulls` block, `_give` and `acts.give` to the hull, a hull made in play re-made in the
   replay at its tick, the converter completed for a checkpoint with `CrewedWorld`s (the
   owner's eleven saves of 70 to 72). *Reading:* 43's left-undone closed (a save with a
   model captain of another ship replays her orders); parallel with item 7.
9. **The director's reach and the truth over the hulls (step 9).** The forms with a hull
   (`aboard the Raven: ...`, the followed when none is named; `person: ... aboard the
   Raven`; `say as` anywhere by spot; `message: ... to the Raven`); the truth walking the
   hulls, their people, purses, cargoes, guns, damage and water, and the persons ashore;
   `read_log ship=` of a hull's log (§12b's ground); the seat at a person aboard any hull;
   the director's library and `WORLD_ORDER_FORMS` with every example performed. *Reading:*
   parallel with item 10.
10. **The drivers follow a hull; the offices' room (step 10).** `state()`, the chart and
    the prompt reading `world.followed`; `follow "X"` as a driver's line and `followed`
    None answered "no ship followed" (82's §11 words; the rest of §11 82's); the stations'
    registry and the harness taking a domain, an office's shape as a stub and no office
    built (the owner's decision 4: M8's); the world orders' purview hook. *Reading:*
    parallel with item 9.
11. **The long tail, the words and the records (step 11).** `shape_words`, `seats.py`'s
    and `agent.py`'s "the player's ship"; the Harness doc; the primer's chapters on the
    promotion and the other ship's captain; spec M6 §19 and §20 and M7b §11, §12 and
    §12b "as built" pointing to the study; `crews.py`'s head; the tuning notes (the design's
    pointer, each step, the pace figures beside the study's, what moved and its proof by
    bisection, the pins old beside new, found on the way, decisions, the suite as run);
    the `world` to `hull` rename only where a step touched a consumer.

**Not built here:** the boat as a vessel, the oar force, the tow and the seat's words for a
person who moves between ships (82, re-briefed on this ground); the prize, the captive's
channel and the far fight wired (74); any office of the leaders (M8; the domain, the
whereabouts and the purview hook are this package's); the business peopling a region
where a stationed hull goes (the owner's decision 7, a later knob); a vectorised many-hull
physics (not wanted). **The head rules bind** as the briefs before have them: no model
identifier; nothing under `docs/agents/consent/` or in `docs/agents/ConsentBrief.md`
touched (the study's 3.4 is 55's); a world order never shown as sent; the ship files
untouched; the pins re-measured only where a change moves them, old beside new, proven by
bisection; never a test skipped, disabled or quarantined; realism, not pacing; the physics
read and not changed; each step a green mergeable state pushed to `claude/pkg-84`.

## Package 86: the owner's local work folded in (every file the review's plan names: the ordnance package's new files whole, the shared files hunk by hunk on top of 73, `tools/gen_ships.py` merged by hand and the ship files regenerated; the fixes with their tightening; the records recast into the line's current files; `docs/dev/TuningNotes.md`; the tests)

**The suites (2026-10-28):** the fast tier once on the final tree and the slow tier of the touched files; after a mend only the mended test's file; the whole suite is the lead's in the cloud at the merge.

Opus (the owner, 2026-10-27: the fold-in is mechanical work under a precise plan; the two judgements, the hail fix's pins proven by bisection and the convoy's stall's cause, are the lead's at the merge); launched the moment 73 is merged, the one package between 73 and 84. The ground is
**the review of the owner's local work**, `docs/playtests/2026-10-25-to-27-owner-playtests-
70-72/review-of-the-local-work.md`, whose section 3 gives every change and its
recommendation, section 5 the collisions, and **section 7 the merge plan, which is this
brief's order of work**; the owner's own weighting in `debrief.md` beside it (the door fixes
key, already merged as the plan's step 1 at `59c4ca4`; the free intent wanted in substance
and provisional in form; resupply and practice as stopgaps for 75 and 77 to redesign as
judged); his tree extracted at `/tmp/claude-0/-home-user-FreeSail/e2d459f1-79d4-50d6-9285-0413fe7ccd0b/scratchpad/owner-local-2026-10-27/m7localchanges` (read as data; run nothing from inside it) and his unified diff against `2774be3` beside it (`owner-local.diff`). Each item an intent with the lead's reading; the intent binds; the review's reasons are the reading.

1. **The ordnance package on top of 73 (the plan's step 3).** The new files whole; the
   shared files hunk by hunk over 73's versions of the same files; `tools/gen_ships.py`
   merged by hand with 73's changes and the ship files regenerated, never taken as text;
   the review's edits made (the global pivot arc made per gun or named for 75; the fillers
   noted for 75 or 77 as real posts; the stale docstring and comment; the duplicated word
   helpers removed; `Papers._merge` reading its own path; the `practice` stream and the
   `hit_chance` size keyword as they are). The owner's truths keep their numbers 7-161 to
   7-171 (73's begin at 7-172, so no renumbering: the plan's step 4 is reduced to the unit
   pins and the counts, each with the old figure beside the new).
2. **The fixes (the plan's step 2), tightened.** The free intents (the crewed captain
   short-circuiting a free intent as the far one does, the ship keeping her service role,
   the warning's words), the hail fix (its `commands` branch limited to the player's ship,
   the heave-to on a demand only as the spec has it), station keeping by name and by kind
   limited to sails in sight with the word match tightened; the tests the review asks for
   each.
3. **The pins proven.** The whole slow tier and the pace tests on the merged tree; every pin
   the hail fix or the rest moves bisected (the gating reverted, the old figure back), moved
   with the old beside the new and the reason, and the convoy and blockade scenarios and
   truths 7-143 to 7-160 checked in particular. **The convoy's stall reproduced**
   (`convoy-six.yaml` run with no orders, as the owner played it: stalled early south-east
   of the Lizard with no way on) and the cause named: the study's reading is the near
   `keep station` order shaping a course inside the close-hauled angle with no bear-away to
   fill (58b's law for the far body's `_course_for`); mended if it is that and small, else
   reported for 72's captain pass.
4. **The records recast (the plan's step 5).** The owner's design notes whole with their
   local hashes replaced by the fold-in's commits; his sections of the spec, the Harness,
   the tuning notes and the primers into the line's current files; the one line that names
   a model reworded; the "Practice and resupply as merged" record written by hand into the
   line's `docs/dev/M7-WorkPackages.md` (never his file whole); 74's, 75's, 77's and 82's
   briefs given the lines the review's section 5 names; the six slow truths' build-machine
   digests recorded beside the owner's.
5. **Left out.** The four consent records; the owner's `docs/dev/M7-WorkPackages.md` as a
   file; nothing of `tests/test_pictures.py` (its two tests fail on this machine's newer
   Chromium by a hair under the blank threshold, before and after every change: the
   machine's, noted, not mended here).

**The head rules bind** as the briefs before have them; the builder pushes its branch to
`claude/pkg-86` after each commit.

## Package 75: the ships (`tools/gen_ships.py` and `data/ships/*.yaml` through it, new files for the *Indefatigable*, the *Prince de Neufchatel* and a 74; `freesail/world/ships.py` the vessel types and their far descriptions, `captains.py` `SIZE_RANK`; `freesail/ship/schema.py` only where a new figure needs a key; `data/nations.yaml` the marines' detachments by nation if 73 left them there; `data/scenarios/` a scenario for each ship; `docs/TechnicalSpec-M7.md` §27 as built; the primer's chapter on the ships; `docs/dev/TuningNotes.md`; `tests/test_ships.py`, `test_ship_particulars.py`, `test_known_truths.py` truths 7-185 to 7-199)

**Built by the owner's own local session by its workflow method** (his word of 2026-10-28;
its plan `Plan-ShipsWorkflow.md` of 2026-10-25, research, the owner's decisions, design,
a behaviour-free stage 0, builders in worktrees, review by lenses, truths, the comparison
with the ships built by single agents; the per-ship generator modules under `tools/ships/`
imported by `tools/gen_ships.py`, the lead's structural decision, agreed), on a branch
`claude/pkg-75` pushed to the origin: **the research and the preparation may begin now from
the head of `claude/dreamy-darwin-d77nty` as it stands (docs and references only); before
any code or ship file is built, the session brings in the head after package 86 is merged,
which the lead names, with `git fetch origin && git merge origin/claude/dreamy-darwin-d77nty`
on `claude/pkg-75`** (a merge into its own branch, never a rebase); the lead reviews and merges, and runs the suite
on the build machine. The session works in a fresh clone that keeps the remote (never a
copied folder made into its own repository), commits on `claude/pkg-75` only, pushes that
branch only, never pushes to or rebases `claude/dreamy-darwin-d77nty`, never force-pushes,
and does not merge; the research notes and the sources filed in the session's earlier
`ships/research` worktree come over by copying the files into the fresh clone, never by its
history; the owner's machine gives different digests from the build machine's (decision
26), so its truths pin states, counts, ticks and bands, never digests. **Each ship file
gains a hull profile through the generator** (a dozen sourced points for the sheer, the
stem, the stern, the wales and the port sills, beside the guns' `x_m` and `height_m` of 70),
the existing seven ships included, so that package 81 draws real ports from data; the
viewer draws each hull from it, toward hulls distinguishable and as near the sources as
they allow (the lead's ruling of 2026-10-29 in the notes below; the owner's end goal,
`docs/design/Build-Ships.md` §5.0); the ports, the guns, the flash and the smoke are
package 81's. Spec M7 §27
and §28 (the Bermuda sloop's description for later), §7 as built by 70 and extended by 86
(the magazine by kind, the fits, the pivot gun with its arc to be made per gun), §8a's
quarter bill, 73's marines' detachment and kit, 72's naval knobs, 71's colours and signals
root; the owner's note of 2026-10-24 (the ship's sub-types as fits and roles the scenario
editor selects and customises in their reasonable degrees) and decision 53's note on 75.
Each item an intent with the lead's reading; the intent binds; the session designs within
them and says what it took another way.

1. **The *Indefatigable*** (the razee of 1795, 44 guns, 24-pounders on the gun deck, her
   carronades, her people some 330): the file through the generator from her draughts and
   Winfield, the Establishments and Lavery, every figure with its source or marked
   judgement; her sail plan and spars as the frigate's are drawn, her polar measured and
   recorded; her quarter bill and her marines' detachment; her fits (as razeed 1795; later
   armaments as data for the scenario editor); a far description and a vessel type.
2. **The *Prince de Neufchatel*** (the privateer of 1812, the hermaphrodite brig or
   schooner rig as the sources have her, her long guns and carronades, her large crew for
   prizes): the same, with the rig's peculiarities recorded for the physics' reading (the
   physics is not changed; where her rig needs a sail class the engine lacks, say so for the
   lead rather than approximate silently); her privateer's fits; an American vessel of
   1812 under 71's basic signals system.
3. **The British bilander with a settee main** (the owner's ruling of 2026-10-25 in his
   session's plan, Gwyn's drawing of c. 1780; unarmed by default with an armed merchant fit;
   the settee a four-cornered lateen on a long oblique yard built on the lug's yard and
   dipping machinery of 43b, set and clewed up as Lescallier gives it): **the one piece of
   this package that extends the engine**, a sail type with its yard, physics, evolutions
   and stations, so the lead's gate applies: the session's design document for the settee
   (its Phase 3) comes to the lead before it is built, and the settee follows the lug's
   class as 43b built it. **And a 74, or a ship of the line of a like class** (the owner,
   2026-10-28: the session runs its research workflow on the class starting from the
   *Bellona* or the *Bellerophon*, and may propose a similar class it finds more
   interesting, with its reason; the owner decides from the research): the two-decker's file through the generator, her lower deck's
   32-pounders and their ports' sills against the heel (70's lee ports shut within a foot of
   the water, the famous reason), her upper deck and quarterdeck, her people some 590, her
   quarter bill by deck, her marines; her sail plan and spars; her polar; the pace of a
   74 crewed measured against the floors and recorded (the muster is three times the
   frigate's); a scenario that puts her on the sea.
4. **The sub-types as fits and roles.** Each file's fits named and described so that the
   scenario editor may select and customise them in their reasonable degrees: the armed
   Indiaman as a role of the merchant ship with her guns and morale (74's and 70's
   decisions: an Indiaman is not a merchantman who strikes at the first telling broadside),
   the revenue cutter, the hired armed cutter, the privateer, the packet; the roles'
   doctrine files where a role is new (`data/captains/`); the generator the one place a
   fit is written.
5. **Every file's armament, quarter bill and marines from 70's and 73's shape.** The
   schooner, the lugger and the smack given their fits and quarter bills (left to 75 by
   70); the pivot gun's arc made per gun in the generator (86's global constant retired)
   with the Dolphin's and the schooner's arcs sourced; the fillers as posts where 73 or 86
   left them as a judgement; the marines' kit by nation from 73's data.
6. **Truths and records.** Truths 7-185 to 7-199 (each ship's particulars against her
   sources within the test's bands; the generator byte-identical for every file; the
   Indefatigable's broadside rate and weight against the frigate's by 70's rule; the 74's
   lower ports shut at the heel the sources give; the 74's pace; the Prince de Neufchatel's
   polar's best point); a scenario per ship; spec §27 as built; the primer's ships chapter;
   the tuning notes (each figure's source, the polars, what was taken another way, found on
   the way, the suite as run on the owner's machine: the fast tier and the touched files'
   slow tier; the whole slow tier and the pace tests the lead's on the build machine).

**The session's five extensions, ruled on by the lead (2026-10-28)** after the owner's
answers to its decision sheet: the hull profile **drawn** in the viewer for every ship is in
this package (the owner's word that the viewer is in scope), the pictures' tests kept
passing and any threshold that moves re-pinned with the old beside the new, 81 starting
from the drawn hull; the lateen class finished and the yards under the bowsprit are
accepted **under the lead's gate with the settee** (one design document for the three
engine extensions reaches the lead before Phase 4; the physics' equations are not changed);
the lee ports wired with sourced sill heights for every ship is accepted as data honesty,
built only after 86's head is in, every combat pin it moves with the old figure beside the
new, the reason and the proof by bisection; the settee tacking as a ship's mizen is within
the settee's design.

**Not built here:** the physics' equations (read, not changed); the boats as files (82's);
the Bermuda sloop (the Caribbean's block, 79 or later). **The head rules bind** as the briefs before have them: no model
identifier in any file or commit; nothing under `docs/agents/consent/` touched; the ship
files never edited by hand; the pins re-measured only where a change moves them, old
beside new, proven; never a test skipped, disabled or quarantined; realism, not pacing.

**From the owner's local work, folded in by package 86** (the review of it, section 5;
the owner's debrief: resupply and practice stopgaps to rewrite or redesign as judged): the
provisional `privateer-schooner.yaml` (the "privateer schooner" description, the "a letter
of marque" alias, the "long tom" and "letter of marque" fits) sits where the *Prince de
Neufchatel* and the sub-types as fits and roles go: 75 says whether it replaces the file or
builds beside it, with the owner's answer on file against fit (his trade trial found that
arming `topsail-schooner.yaml` made the merchant schooner engage). The pivot gun's arc is
the gun's own since 86 (`arc_deg` in the ship file, written by `pivot_gun`; the old
constants a default only): 75 gives each pivot its arc from its own rig. The magazine's
charges by kind are UNVERIFIED shares until Table No. 29 is read, through the generator.
The frigate's quarterdeck is marked INCORRECT against Winfield: correcting it moves the
quarter bill, the magazine, the filling party and the allowance, and with them truths 7-133
onward and 86's 7-161 to 7-171, each with the old figure beside the new. The gunner's
filling party is read and never moved (the build's decision 5): the gunner, his crew and
the quarter gunners as real posts that compete for hands are 77's unless 75 takes them
first.

### Notes from the lead to the ships session (the written channel: the session fetches this branch before each stage; its reports are its branch and `docs/design/`)

**2026-10-28, on the session's first message.** The channel works from the session to the
lead and not back (a cloud session's credential does not deliver to another session), so
these notes are the lead's side of it. The session's reading of the go-ahead is right on
all three points: Phase 3 approved and then the build one ship at a time, the
*Indefatigable* first, the generator modules, the hull profiles and the ship files going
from design to build without a gate; the gate on the engine extensions only, one design
document read once by the lead before their builders start, and **the mizen course cut at
the mast** (laced to it, its head on the lateen yard abaft the mast, the owner's choice of
the 28th for the 74 and the 64) belongs in that same document, between the lateen and the
gaff; the lead's head merged before stage 0 and the builders reaching `world.ship` and the
crewed world only through the names the Hull keeps. One addition: after the merge before
stage 0, bring the lead's branch in again **only at stage boundaries**, so the builders are
not chasing the one-world refactor mid-stage. When the engine document is ready, name its
path in a message if the session can, or the lead reads it on the branch.

**2026-10-28, the gate: `Design-ShipsEngineExtensions.md` at bee6e96 on `claude/pkg-75`,
read with `Build-Ships.md` §19.2 and §20.** The engine extensions are **approved as
designed**, and the session may lay stage 0 and stage 0E and start its builders.

The gate's two items:
1. *The mizen course* as class lateen cut at the mast (`cut_at_mast`), reading the gaff's
   curve through `curve_class`, is right: the physics sees the curve the sail's cut earns and
   the rig sees a yard, which is what the thing is. The measurements of §3.2 settle it (the
   frigate's polar within 0.2 kn at every point with the gaff's curve; the yard out of the
   braced yards; her classing as filed).
2. *"The physics' equations are not changed"* is met by what §1 lists: a `curve_class` lookup
   where a class lookup already stood, a membership test that leaves the yards under the
   bowsprit out of `_square_rigged`, the helm's mark and `_spar_x`, and nothing else in
   `physics/`. The proof the lead reads at the merge: `_plate_force`, `compute_sail_forces`'s
   sums, `_lateral_offset`, the load fractions and `data/sail_classes.yaml` byte-identical
   to the head merged before stage 0 (a diff of those ranges shows nothing), and the row "the
   spanker as filed" of §3.2 re-measured on the final tree equal to the figures printed there.
   Nothing pinned on the existing ships moves; where a pin moves it is re-measured where moved,
   old beside new, with the cause bisected to one change (the standing rule).

Build §19.2, in its order:
- *2, stage 0E after this approval*, the four `curve_class` lookups in stage 0: as settled.
- *3, D48 against a named fit*: **the third way.** A command-line ship that lacks the
  scenario's fit takes her own default, with one line in the log, and a test of it in
  `tests/test_scenarios_75.py`. B6 builds it, the smallest change in `make_scenario_world`'s
  reach and nothing else in `world/scenarios.py`; package 84 may touch that file later and the
  lead resolves the merge.
- *4, the fillers as posts*: to 77, as proposed.
- *5, the merchant brig's and the packet's descriptions* moved to their files: yes. The convoy
  and trade pins it moves are listed in the record with old beside new and the move proved by
  bisection; a description is a description and no behaviour may move with it.
- *6, the scenario's `nations:` block*: **ruled in**, laid in stage 0b as §12.1 says, inert
  while no scenario carries it. The wars' dates land with their citation by page; a row the
  builder cannot check against James says so in its comment, and the *Neufchatel*'s scenario
  notes name it open, rather than carrying a date from memory as if checked.
- *7, D10(a)'s key* for the *Neufchatel*'s main topgallant: yes, built by B3 as its fourth
  step beside `under_bowsprit` at places 1 and 3 of §4.2, inert until her file uses it.
- *8, the order and the merges*: the *Indefatigable*, the *Prince de Neufchatel*, the bilander,
  the 74, as the owner asked and §2.3 has it. **The lead merges after each ship**: the session
  reports a ship done on its branch, the lead reviews and merges `--no-ff`, runs the whole suite
  in the cloud, and the session brings the lead's head in at the next stage boundary. The
  window closes with the merge; nothing waits for the end of the package.
- *9, the names and the fits*: accepted as written (`sixty-four.yaml`, `razee-44.yaml`,
  `hermaphrodite-brig.yaml`, `seventy-four.yaml`, `bilander.yaml`; the fits "ardent class
  1784", "ardent class 1794", "as razeed 1795", "as carried 1796"; the description keys).
- *10, the workflow's shape*: accepted, the two-way byte test included.
- *11, the head*: the lead's branch now stands at 5e3f7b5 (package 84's steps 3 and 4
  merged). Merge the lead's head as it stands when stage 0 begins, then at stage boundaries
  only; the ancestor check of §2.1 before stage 0.
- *12, the frigate's draught and the 36's trimmers*: recorded for the frigate's own file, not
  this package's.
- `ARC_PIVOT_*` kept for the old pickles, with a comment saying why: yes.

Ext §14, the rest: *3*, the engine's driver rule holds for the settee hove to unless the
measured figures say otherwise, and then D4(a) with the figures in TuningNotes; *4*, as
designed, the case that holds pinned and named, and if neither holds D44(c)'s `settee` row is
accepted in advance (no equation changes; `test_sails.py`'s curve set old beside new); *5*,
yes, furled aloft; *6* and *7*, the session's judgement, the times and hands recorded in
TuningNotes with the sources; *8* and *9*, yes; *10*, the 74 without the driver of 1773, the
want recorded in her design as open, not asked for now; *11*, the truths' numbers as Build §20
has them within 7-185 to 7-199, the spare block 7-230 to 7-239 for more; *12*, (a), above;
*13*, a later package; *14*, open.

The suites as the brief has them: the fast tier once on the final tree and the touched files'
slow tier on the owner's machine; the whole suite is the lead's, in the cloud, at each merge.

**2026-10-28, later: the owner's answers read** (`9710fad` on `claude/pkg-75`, recorded in
`Decisions-ShipsRound2-2026-10.md`, `Build-Ships.md` and the *Indefatigable*'s design). They
sit with the rulings above and change none of them: the razee's default fit "as carried
1796" serves her without a scenario naming a fit, and **D48's third way stands as ruled** for
the files with named fits that are not hers (the 74, the 64's two fits) and for a command-line
ship meeting any scenario's fit; the engine's judgement figures the owner accepted are the
ones ruled in (the mizen furled aloft, the settee dipped when the head yards' swing ends, the
spritsails out of plain sail). **The lifts drawn on every yard**, faint at the braces'
opacity, in the profile's step: accepted; the pictures' figures measured with and without,
old beside new, and the change kept to the viewer's rig drawing so that package 81's hull
work, which draws from this package's profiles later, does not meet it in the same lines.
The 74's driver stays left out unless the owner asks. Nothing further is owed from the lead
before stage 0's first commits.

**2026-10-28, stage 0 read** (`fd5bb95`, with `c514048` the pages and `b562bae` the driver,
on `claude/pkg-75`; the session's message of the evening). **Accepted as laid.** Read against
the gate: nothing under `freesail/physics/` or in `data/sail_classes.yaml` is touched; no
ship file moves; the `curve_class` lookups are where the ruling put them and return the
sail's own class; the hooks are inert as said (`combat/ports.update` returns two empty sets,
`CHARGE_TABLE_LB` is empty, the four ship modules write nothing, the profile is read by
nothing a file carries). The known word changes are accepted: the director's brief-limit
refusal naming the ships of the line by their rank, and the two lee-port events registered
absent so the brief and the stand-by are as before. The checkpoint's forms leave the new
fields out at their defaults, which is the right way to keep every pin. Four things to carry:
1. **`charge_lb` now reads the Regulations' table first.** When SW-1 fills
   `CHARGE_TABLE_LB`, the eight files' magazines (`fit_magazine`) read it too. The rule: the
   two-way byte test is the gate on that commit; if a figure of the eight would move, the
   table serves the new ships alone (keyed so, or read only where a file asks), and the
   eight's charges stay as filed until a package of their own re-measures them old beside
   new. The design's "no figure of the eight moves" is the rule, not a hope.
2. **Package 84 and the shared files.** Stage 0 touches `world/ships.py`, `captains.py`,
   `brains.py` and `squadrons.py`, which 84's step 6 (the Hull as the container, under test
   now) reworks. So, beside "the lead's head at every stage boundary": **bring the lead's
   head in again before reporting a ship done**, and resolve what meets on the session's
   branch, where the ships' changes are small and local and the engine's are to be re-read
   as they land; the lead merges a branch that already carries the lead's head. The merge
   cadence stands: after each ship.
3. **The references** (twenty-seven OCR texts now, 53 MB where there were 15): accepted, all
   period and public domain, each with its README row and source; the page images stay
   outside the repository as the README says; nothing further is filed without its row. The
   size is told to the owner as a fact, not a complaint.
4. **The lifts on every yard**: confirmed (the entry above). **The driver of the 64 and the
   74** (Ext §14 item 10 reopened by the owner): proceed to the addendum; the lead reads it
   with the same lens as the gate, the physics' ranges byte-identical, the sail's curve an
   existing class's, `_gaff_host`'s new host a membership and not an equation, and the
   frigate's polar re-measured equal. Stage 0E and B1 do not wait on it.
The 64's exercise allowance by `decks=2`, Adye's and Falconer's tables in `tools/ships/period.py`
with their pages, and the pivot's arc required at the load (the old pickles keeping the
default, as ruled) are all as they should be. Go on to stage 0E.

**2026-10-29, stage 0E read and the driver's addendum ruled** (`2ead5f0` and `0dbde00` on
`claude/pkg-75`). **Stage 0E accepted as laid:** the three keys refused in words where they
cannot stand (`settee` a dipping lug naming its mast with four corners, never flying nor
sheeted to another sail; `cut_at_mast` a lateen naming its mast with four corners;
`heave_to_aback` a lower mast's and one mast's at most), the runtime fields class defaults
left out of the pickle while false, `curve_class` the gaff's for a sail cut at the mast,
`Ship.under_bowsprit` defined and called by nothing, the runner's `class: settee` and
`wanted_sheet`, the served keys only where true; nothing under `freesail/physics/` or
`data/`; the eight files byte for byte and every pickle byte-identical to `5326e24`'s. One
thing seen and accepted for the interval: between 0E and B3.1 the rating, the polar's sheets
and the readings take the gaff's curve for a sail cut at the mast while the physics' own
lookups still take the lateen's; no file carries the key, so nothing differs, and B3.1
closes it, in that order and not the other.

**The driver (Ext §17): approved.** The lens is met in full: nothing in the physics or the
class table changes, not even a lookup; the curve is the gaff's through `curve_class`; no new
host, since the sail is Steel's driver boomsail and not the 1773 ringtail; and the frigate's
spanker re-filed as the driver's model (row 3′) gives her polar and her yaw equal to the
filed spanker at every angle, in speed and in moment. The two changes are what they say:
a schema allowance (a boom on a lateen cut at the mast, refused on a whole lateen) and a
handling membership (two sails bent in one place are rivals, so the storm mizzen and the
driver are never bent together), the second reaching `orders/storm.py`'s own copy of the
rule, so the storm's slow tier runs on that commit. The model's departure from the owner's
item, the course unbent while the driver is bent in place of brailed beside it, is the
engine's one-place rule keeping one after sail bent on every path that sets sail unasked;
the owner chose Steel's sail for both ships with that explained, and §17.9 keeps the brailed
way open should they want it later. The 64's low confidence is recorded as it should be: the
owner's choice, not the evidence's. **Truth 7-230 is allotted to the driver** from the spare
block: row 3′'s equality (the model is the spanker to the physics) and the shift's thirteen
minutes, in `tests/test_driver.py` as proposed. B1 and B7 measure their own polars and
balance at the flip, old beside new, as the addendum says. Go on: the stage-0 allowance,
B3.5 after B3.1, B5's drawing, B1's flip at the 64's stage B.

**2026-10-29, the hull's principles, design and order approved** (`85b5a2a` on
`claude/pkg-75`: `Build-Ships.md` §5.0, §5.7, §3.5, §5.1 to §5.3, §5.6, §6, §2.6 and §19.2
items 13 to 21; read whole). **1. The hull (item 13): approved.** The twelve principles are
right, and the two that carry the weight are the ones the lead would have written: the
drawing never changes how a ship sails or fights, and nothing is invented. The design holds
to them in the code's shape, which is what the gate reads: eight optional shape keys after
`port_size_m`, drawn only; `freesail/ship/form.py` pure, computing the drawn stations when
`/api/ship` is served so that a rule's change moves no file; the guard that nothing under
`physics/`, `combat/`, `crew/` or `world/` reads a shape key; no port triple ever written
from the drawing and the lee port reading only stored triples; the two-way byte test at 0H;
`HullProfile.__getstate__` leaving the new fields out while empty. The ladder of evidence
with its one-word marks on every line, sourced points winning over the rule, a stand-in's
departures recorded beside the file's figures and never moved, and the pair check that no
two files draw alike unless listed as one class in two roles: all accepted as the method.
It goes beyond the brief's dozen points, and the brief is amended (above) to say what it
now says. **2. The owner's answers (items 14 to 18): recorded** as the design has them;
the hull below the water and the close-up stay open for the owner's sheets. **3. The order
(§2.6): approved.** B1's window stays open until the *Indefatigable* is whole, with the
hull's form built and drawn first on her two files, held for the owner's first test; no
later ship's window opens before it; the session brings the lead's head in before reporting
her, and the lead merges her whole as each ship is merged. One leave the lead adds, for the
drift's sake while 84's later steps rework `world/ships.py` and its kin: **the inert engine
steps may be reported at their boundaries for merge before her** (0H with SW-2b.1, B3.1,
B3.2, B3.5), each green on the fast tier and the touched files' slow tier with its byte
test, so that the ships' branch and the lead's do not diverge for the length of her window;
the lead merges them as the inert steps they are, and the pilot's test is of the whole
tree. The session may take that leave or not. **4. Beside the pilot (item 20):** SW-1 runs
beside the pilot under the stage 0 rule (the charge table serves the new ships alone if a
figure of the eight would move; the two-way byte test the gate on its commit). SW-4 runs
beside the pilot but for its rows in `world/ships.py`, which wait for B1's window to close
and for 84's step 7, which reworks that file. **5. Package 81's boundary (item 19):**
accepted as read: 75 draws no port, lid or opening, its stern lights plain marks; the
ports, the guns, the flash and the smoke are 81's; the brief's stale line is replaced.
**6. The far ship's length (item 21): confirmed and not 75's.** `combat/far.py:111` reads
`spec.hull.length_m`, a key `HullSpec` has not (it has `length_waterline_m`), so every far
ship's length is 0.0 and `shot.py:167` floors her size at 0.5 whatever she is; the mend
moves the far fight's pins and belongs to package 74, the far fight's package, where it is
booked with the old figures to be shown beside the new. **7. Stage A's two points** (the
rail ending 0.8 m abaft the stem; the knee of the head carried in `stem_m` where the design
gives it `head_m`): the session's refinement, checked against §5.1's form, as it says.
Go on: stage 0H.

**2026-10-29, after the usage reset: the three designs read, the stage B items, the merge of
the pilot** (`claude/pkg-75` at `164027c`: `Design-Ship-PrinceDeNeufchatel.md`,
`Design-Ship-Bilander.md`, `Design-Ship-Bellerophon.md` whole, each one's list for the lead;
`Build-Ships.md` §2.6 as the owner's direction of 2026-10-29 rewrote it; the owner's answers of
`8f30be9` and `164027c`). The lead's head is `76eb22c`: 84's step 8 (the save and the replay of
many hulls) and 79b (the Channel's east block, `channel-east`, 1 W to 2.5 E, its own tiles and
truths, nothing of the Channel west's moved) are merged; bring it in before stage B as §2.6
says. **1. The merge of the pilot.** The leave of the last note (the inert steps merged at their
boundaries) cannot be taken as the branch stands: 0H, SW-2b.1 and the viewer's steps sit on
stage A's ship files in the history, so no inert step can come over without her. The lead takes
her whole at her report, as §2.6 step 7 has it, with the testing report in place of the
owner's test; the leave stands only for an inert step the session carves onto a branch from the
lead's head, which it is not asked to do. **2. Stage B, settled:** the topgallants and royals
by Steel p. 42's pole-heads for the 64 and the 74 (the owner's "Agreed"), the 64's at her stage
B, her file regenerated, the polar and the light-air figures old beside new (Bel §17.2 item 8:
yes, in her window); the viewer roots the bowsprit from the profile's stem head in the same
step as the yards under the bowsprit are drawn, so that the spritsail yards hang from a
bowsprit that stands where the file has it and the 2.3 m stand-in goes with them; the clew
check of Bel §1.5 runs at B1's stage B on both her files (Bel item 13's last question: yes),
and where the 64's course clew ends under her roundhouse deck at the side the head room goes
first, as the 74's pick has it, to 5 ft, past that a report with the figures; the razee's
driver boom's jaws under her roundhouse (Indf, open at her stage B) the same: raised clear by
the least that clears, her spanker kept within 8 % of Steel's driver for a 38 as the owner
settled it, the figures old beside new in the testing report. The files' notes carry sources,
departures and judgements, not figures a rule computes from the file's own keys (an area from
a cut, a heel from a sill): those live in the generator's report and the tests, where they
cannot go stale. **3. The order (Bel item 6): confirmed.** B1 merged on her testing report;
SW-2 with SW-2b.2 as one step after her merge, SW-5 L2 and L3 behind them; then B2, B4, B7 in
that order, each on a testing report of her own and merged as each ship is; the session records
it in §2.6 at her window's opening by a design-record commit, as 8f30be9 was made, and the
same commit writes the direction into §2.2's B2 row. **4. The *Neufchatel* (her §17).** (1)
D10(a)'s key in the proposed form: `schooner_mast` on the mast, `Spar.schooner_mast` and
`Ship.on_schooner_mast`, read at Ext §4.2's places 1 and 3 only, place 2 left as it is; the
schema key by a stage-0 commit at B3.4's boundary, the field and the predicate B3.4's; B3.4
right after B3.5 and before B3.3, so her file takes the key from its first commit; the two
findings of §12.2 item 8 reported before any further place. (2) Yes. (3) Yes: 84's step 7 is
merged, so SW-4's rows in `world/ships.py` wait on B1's merge alone now; if they are not in when
she is otherwise done, hers go first in her window and SW-4's follow. (4) Yes, the direction
holds for her, a testing report and the lead's merge on it. The scenario's `nations:` block
(§19.2 item 6, open since the gate) is **ruled in**: laid at her stage 0b as a parsed and kept
block that nothing reads until her scenario, the stage 0b commit made on the lead's head of
the day; B6's D48 change to `world/scenarios.py` merges onto it. (5) Yes, that meets the
brief: her best speed in 25 kn within her accounts' band pinned, the best point's angle
reported, the pointing clause reported and not forced if her file misses it. (6) As the design
has it. (7) Recorded for a later package of the rigging's evolutions. (8) Yes, at her merge, old
beside new, by the session's design-record commit. (9) Accepted. **5. The bilander (her §17).**
(1) Her window after B2's merge, her file on the package's branch only after B3.3 is merged
there, held unmerged if B3.3 lags, the 74 waiting as §2.2 has it. (2) Yes. (3) Yes. (4) **The
design's block:** the reserve branch from the start, keyed on `settee`, the foot from the
corners with the block a fathom abaft the clew and abreast of it, the trim reading no part of
the profile; Ext §5.9's taffrail block is the one approved and this is the departure from it,
so Ext §5.9 gains the line (one block for a settee's cut, the other for every other), by the
session, and the lateral offset's understatement goes in TuningNotes as said. (5) Noted against
the plan hull by hull: S† for her body and for Gwyn's heights, the marks as the ladder has
them; the plan's §5.7 row amended at her merge, old beside new. (6) Unscaled, as picked;
"about 130" holds 128. (7) Yes: report first, no curve moved for rule 1 alone. (8) Yes: B4 runs
them; a follow-up B3 step keyed on `settee` alone before her merge if one is needed, her polar
and 7-197's rule-1 clause measured again on it, old beside new. (9) Accepted. **6. The 74 (her
§17.2).** (1) One `marines` key, the same on her bill, the 64's and the razee's, laid inert in
stage 0c; whether a division forms at the beat is B7's to measure on all three. (2) Keyed on
two gun decks and a `lower` deck, the two two-deckers alike, the 64's beat lines and robbing
order old beside new. (3) B7.d at the end of her window, both two-deckers together, on the
lead's allotment of `parts.py` and `graph.py` after B3's merge, checked as Build §3.4. (4)
B7.c, its own commit, bisected, old beside new for 7-136 and every file's tack at quarters;
the lead reads the moved pins before the merge. (5) Agreed. (6) Confirmed (item 3 above). (7)
Hold her window for SW-5 L3. (8) B1's stage B (item 2 above). (9) Accepted. (10) If the owner
takes the rank-4 rule, B7.e owns `world/captains.py` and the two doctrine books for that step
alone, and the 64's scenario tests are re-run. (11) Accepted. (12) A later package of the
physics; a line in TuningNotes with the *Bellona*'s figures beside the engine's, for both files.
(13) The pick: head room first, to 5 ft; past that, a report with the figures and `DRIVER =
False` until the lead rules; the 64's clew check at B1's stage B (item 2 above). (14) Yes: the
line is passed to 81's row (above): a triple within `OVER_THE_RAIL_M` of the rail at its x is a
gun place over the rail and is not drawn as a port. (15) The key laid inert in stage 0c is
75's; the world code that brings the flag's people aboard with their stations is a package of
its own after 84, beside 87, booked when the owner asks for a scenario that hoists a flag; 75
does not build it. Named for the lead (§12.3): `freesail/orders/gunnery.py` is B7's for the
whole package; `evolutions/runner.py`, `ship/graph.py`, `ship/parts.py` and
`tools/ships/indefatigable.py` B7's for B7.c and B7.d alone, each returned at that step's
merge; `tools/ships/mizen_yard.py` B7's for the driver's jaws. **7. Also:** the far ship's
length is booked to 74 as the last note said; §19.2 item 5 (the merchant brig's description
to `merchant-brig.yaml`, the packet's description) is ruled as §8.4 proposes, built by its
owner before the brig's phrases are next touched. Go on: stage 0H's merge wait is lifted (item
1), so stage B when B3.5 and its drawing are in.

**2026-10-29, the owner's six sheets of the pilot seen by the lead** (the viewer's sheets of
the 64 and the razee at the head after `09dde99`: abeam and on the quarter at 135 degrees,
old beside new, furled and under plain sail; the hull alone beside the frigate-36, one scale
and normalised; the hull below the water three ways at 10 degrees of heel; astern with the
razee's short roundhouse under D18 (c); sent to the lead by the owner, not in the branch).
**The read:** the hull is a two-decker at a glance where the old viewer had a slab, the rig
the same in old and new and the masts' feet and the bowsprit's heel on the drawn hull, which
is the principles kept; the quarter view holds, the run aft narrowing as it should; the
razee one tier fewer with the same lower wales, her short roundhouse the stepped block,
her stern one row of lights under the roundhouse where the 64 has two and two tiers of
galleries; the frigate-36 normalised, a box 2.69 times too high with no sheer, the plainest
case yet for SW-2 directly after the pilot, which is the order. **Rulings:** (1) §19.1 item
16: **hidden by the sea is the default**, as proposed; *faint* is kept as the viewer's toggle
for sheets like these, since it shows the body against its waterline when the lines are
judged; *solid* goes with the shared hull when SW-2 lands. (2) §19.1 item 19 is closed by the
owner's word in `164027c` (the browser's look decides); at 7.9 px a metre the tumblehome
reads plainly. (3) The tan strips at the deck levels read as planking bands until 81 draws
the ports over them: as designed, and the sheets say so; nothing to change. (4) One question
for the Vanguard photographs, not a fault: the razee's roundhouse is drawn as a plain block
with no lights in its after bulkhead; whether the model shows lights there is the owner's to
read, and the file's note should say which way it was judged. (5) **The sheets go into the
record** with B1's testing report, under `docs/playtests/<date>-pilot-indefatigable/pictures/`
in the form the playtests' pictures take (the six as PNG, a README naming each by its head
and what it shows), since they are the sheets §2.6 step 7 promised and the record of the
hull's first drawing; the Vanguard photographs stay private as the design has them.

**2026-10-29, the next window after 75: the tartane and the xebec (package 90).** The owner's
word, with the Mediterranean's west block (79c) now building: after the 74 closes 75, the
session's next ships are the tartane of decision 11 (the third reference vessel, chosen in
September for how differently she handles) and the xebec, each as a trader or fisherman and
as a corsair or the King's by fits and roles, on 79c's water, with the regency's cruisers as
a role; inside milestone 7. The design is the session's, in its plan's form (a design
document each, the ladder of evidence, the lead's gate before a file), drawn from Roux's and
Tofiño's plans and the pilots 79c lays under `docs/references/pilots/`; the lateen's
handling is B3.1's. Nothing of it opens before 75's last window closes. The count the owner
is aiming at, loosely: **twenty hulls**, fits not counted (eight today, thirteen after 75,
fifteen after these two); more fits on a hull are welcome, at the cost of research and
tuning only; the number grows in the content phase as it likes. **After 90, the choosing
(the owner, 2026-10-29; decision 56):** the armed Indiaman first; then rigs and variations
the game has not got before another of a rig it has (a snow, a brigantine, a polacre, a
ship-sloop, the small unrated vessels such as gunboats), with exceptions as the fancy
strikes; Winfield's lists are now on the owner's shelf as a source, with plans scattered
through most sections, to be cited by page as James and Steel are. Nothing of this is
booked yet; the session may name candidates with their sources in its plan when 90's
design is written, for the owner's choosing.
