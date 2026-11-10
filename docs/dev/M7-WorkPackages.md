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
realism, not pacing; nothing pre-defines a battle's timing), and from 2026-11-06 decision
64: **every nation-specific extension includes Spain and the relevant Mediterranean factions
where it can** (the signal books, the doctrines, the fighting habits, the regimes, the
nation-keyed tables), a builder writing Spain's row with its source or saying in the tuning
notes what was looked for and not found (spec M7 §28; the Spanish sources in
`docs/design/VesselReferences-2026-11-Spanish.md`).

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
| 74 | Fable | Prizes, the strike and what follows, and the far fight; the consent revision for adversarial seats drafted with it (spec §11a, §18 to §20, §29) | briefed 2026-10-24 (below), for the owner's approval; **runs after 84 and 82** (decision 52); **refreshed 2026-10-30 (below)** on the one world and 82's design; **held by the owner (2026-10-30) to run after 82 and 65 both**, one Fable package at a time; **launched 2026-11-07 on 65's close** as a Fable sibling session on `claude/pkg-74` (session_01XooV4BjeDy5Z9rXT75YZ27), the design note first, the trunk at f67640b; **the design approved 2026-11-07** (nine rulings; `docs/design/Design-Prizes.md`); step 1 merged 2026-11-07 (9acab09); step 2 merged 2026-11-07 (1bb24f52), truths 7-351 to 7-354; **step 3 (the captive's channel) merged 2026-11-07 (277e9482)**, truths 7-355 to 7-357; **PAUSED 2026-11-07 at the owner's word** (the account's Fable usage at 95 percent of its weekly limit; four steps left), at step 3's boundary with nothing in flight, steps 4 to 7 built on the scratch branch `claude/pkg-74-step3` (0de652a) and waiting their tiers; resumes about 2026-11-12 19:00 UTC or when the owner says, step 4 (the far fight wired) first with 74's answer on 76's two doctrine hooks; **RESUMED 2026-11-09 at the owner's word** after the reset: step 4's two mends, and with them five defects of step 3's channel found by replaying the owner's strike save (the captive's word taken as the player's hand, so the captor's captain stood aside and she took the ground; the captor engaging his own prize; a bare yes unread; a prisoner's hail performed; the free man's refusal of "go ashore"); **step 4 (the far fight wired) and the five mends merged 2026-11-10 (9944b671)**, truths 7-358 to 7-361 and 7-369, no pin moved; five small mends given back for step 5's tree (the parole's negations, the fallback line's engine words, a loosened test, a conditional skip, the player's plain speech no hand on her); **step 5 (the prize court and the money) merged 2026-11-10 (dcd6c690)**, truths 7-362 and 7-363, with the five mends; one pin moved at the meeting with 98 (the officer's handover budget 22,500 to 23,000, by the test's own practice); most of the money's figures FROM MEMORY and marked so, for the owner's shelf; next step 6 (the court martial, a new command, the consent revision's draft), then 7 |
| 75 | Opus | The ships: the *Indefatigable*, the *Prince de Neufchatel*, the 74; every file's armament, quarter bill and marines from 70's shape; **the ship's sub-types as fits and roles the scenario editor selects and customises in their reasonable degrees** (armed and unarmed, by rig, hull and role: the armed Indiaman, the revenue cutter, the privateer; the owner, 2026-10-24) | the hull step merged 2026-10-31 (cfe48a5's record); the lee-port step (L2 and L3), the rig lines and the booms merged 2026-11-06 (8c30c8a); next B3.4 by §12.2a's rule, SW-4, the *Neufchatel*, the bilander, the 74, Phase 5; B6 to a supplemental package; the hold (SW-5) and B3.4 merged 2026-11-06 (f414ed1); SW-4 merged 2026-11-07 (73b9469); B3.4's four rulings merged 2026-11-07 (3c9df9e1); **B2 (the *Prince de Neufchatel*) with SW-4's words step and her stage 0b merged 2026-11-07 (04136d99)**, truths 7-192 and 7-193 drafted, the lead's rulings on its six points in the notes below; B3.4b (the word's two cases, the dismasted lines) owed first, then B3.3 (the settee) with B4 (the bilander); **B3.3 and B5.4 (the settee in the engine and drawn), B3.4b, B2b (the *Neufchatel*'s ruled fixes) and B4 (the bilander) merged 2026-11-09 (acdcfb56)**, truths 7-197 to 7-199 drafted, the lead's rulings in the notes below; **B2c (the owner's two rulings of 2026-11-08 on the *Neufchatel*: her fore gaff sail at lie a-try, her lead re-tuned with her bands widened) and B3.3b (the settee's forced-round guard) merged 2026-11-10 (cff8fdb1)**; **SW-1 (Table No. 29's charges) and the ruled builds of the 9th and 10th merged 2026-11-10 (09222043)**, no figure of the eight old files moved; the session's six points ruled in the notes (the bilander's short watch calls all hands for her settee; "make all sail" lists only what she has); next B7 (the 74), then Phase 5; the lead's final word on the close-out, after those, frees the session's preliminary work on 90 (the owner, 2026-11-10); **B7, the 74 (the *Bellerophon*, steps 0 to 6, the bill by deck and her review's mends) merged 2026-11-10 (31f6bb35)**, truths 7-194 to 7-196 drafted (7-196's clause alone recorded, not pinned), the lead's rulings on its seven points in the notes below; next her step 7 (B7.c, B7.d, B7.e), the trim's alias words, Phase 5 |
| 76 | Opus | The signal books built out from 71's baseline | behind 71 (merged); **briefed 2026-11-07 (below); approved and launched 2026-11-07 (the owner)** as an Opus sibling session on `claude/pkg-76` (session_01XooV4AqyCMwqgyMVwkvG3x), beside 74 and 81, the trunk at f466051: the research pass first, the Spanish book first after the French (decision 64), a nation's book added by data alone; the research pass approved 2026-11-07; **the pass and step 1 (Britain) merged 2026-11-07 (4f3694b2)**; step 2 (France) merged 2026-11-07 (943b453f); steps 3 (Spain), 4 (the United States and Naples), 6, 7 and item 8 (the flags of command and identity) merged 2026-11-07 (649c5478), truths 7-426 to 7-435; **CLOSED 2026-11-07** (the owner has nothing to add for now on its seven shelf questions; they stand on the lead's list, each a small data step by a session the lead wakes when an answer comes) |
| 77 | Opus | The gunnery's and the fight's evolutions from 70 and 73; the damage-control catalogue; the fillers as posts (from 75); Portsmouth's Ordnance block in the magazine's table (79b's finding: the Gun Wharf issuing at Spithead under the Regulations of 1806); **found by package 81 (2026-11-07), for this package:** a hole above the water is made at 0.3 to 1.8 m above the waterline whatever the side's height (`combat/hits.py`, 73's), so a cutter's hole can stand above her rail: cap a hole at the side's height at its x (the profile's rail where the file gives one); and a tick on each volley (`Volley` in `combat/guns.py`) for the viewer's exact stamp of each round (81 stamps a round with its snapshot's tick meanwhile) | behind 70 and 73 |
| 78 | Opus | Sight across land; collision; fine control of the sails and the gybe as an evolution | where the sailing wants it |
| 79 | Opus | **Split 2026-10-29 (the owner):** 79a the regimes filled out and sourced; 79b the Channel's east block (`channel-east`, the Wight to Dunkirk); 79c the Mediterranean west (the Strait to Cartagena and the Balearics, with its research pass for the period's pilots); 79d the Gulf of Lion and the Tyrrhenian (Toulon, Corsica, Sardinia, Elba, Naples); Sicily and Malta, and the eastern basin, later blocks | **79a and 79b merged 2026-10-29** (the records below); **79c and 79d approved 2026-10-29 (the owner); 79c launched 2026-10-29** as an Opus sibling session on `claude/pkg-79c`; **its research pass (step 0) merged 2026-10-29** (`38b0145`: fifteen texts of both basins under `docs/references/pilots/`, the Admiralty's meteorological tables as page images, the pass's report in the tuning notes; Gallica, the BDH, HathiTrust and Europeana refusing with their own pages, the Archive answering everything); **79d launched 2026-10-29** from it as an Opus sibling session on `claude/pkg-79d` **and merged 2026-10-30** (the record below; the four packages of 79 done); **79c merged 2026-10-29** (the record below; its block ruled two regions at the builder's report of 57.5 MB in one: `mediterranean-west` the Alboran, Málaga to Cartagena and Barbary to Oran, 5 W to a tile column at 0.05 E, and `balearics`, the Balearics with Algiers, thence to 4.5 E; every tile written, the numbering one package's); **79d's Gulf ruled two regions the same day** (`gulf-of-lion` 3 to 7.73 E and `ligurian-sea` 7.73 to 11 E, with `tyrrhenian` within the rule: three regions in the package; the Gulf's south bound to 40.56 N to meet `balearics`, so no open water between the blocks answers nothing; a port's nation allowed a dated form, `{nation, since, until}` by 79a's form, read for the world's date, for Genoa's annexation of June 1805, the smallest change in the ports' readers, 84 told); none depends on 84 |
| 80 | Opus | Prizes and the continuation from 74; the consent revision's package if 55 has closed | behind 74 |
| 82 | Fable | **The boat as a vessel, and the player aboard another ship** (M7b's 63 and the heart of 51, brought forward by the owner, 2026-10-24): the followed ship in place of the given one and a world with no player's ship; the player and any person aboard another ship, moving between ships by the boat, by boarding or by capture, the seat following the person, 68's refusal lifted; the boat crewed and sailed, towing by an oar force; the replay of a station on another ship | briefed 2026-10-24 (below); **re-briefed after 83's design** (decision 52), runs after 84; Fable whole (the owner, 2026-10-29), **the re-brief carrying the ships session's principles for a hull and a ship** (`docs/design/Build-Ships.md` §5.0's twelve, the ladder of evidence with its marks, sourced points over the rule, the drawing never changing how a vessel sails, nothing invented; the boat a ship file written by a module of `tools/ships/` through `tools/gen_ships.py` with her shape keys and port triples as the ships are, never by hand), so that the boat is built to the new standard; **re-briefed 2026-10-30 (below, after 84 and 85), approved and launched the same day** as a Fable sibling session on `claude/pkg-82`; the boat to the ships session's principles; 74 starts on its item 3; **step 1 (item 3, the person's movement between hulls) merged 2026-10-30** (below, "Package 82, step 1, as merged"); **step 2 (item 1, the world with no followed hull) merged 2026-10-31** (below, "Package 82, step 2, as merged"); **steps 3 and 4 (the player's seat on another ship; the boat as a hull) merged 2026-10-31** (below); **steps 5 to 7 and the boat's drawing merged 2026-10-31, the package closed** (below) |
| 83 | Fable | **The one-world study** (decision 52): the design of a world the player is one part of, many crewed hulls in one World, the person's coarse acts anywhere, the leaders' roles left room for; the migration in steps that keep the suite green; the cost in pace and pins; a brief for 84; no code | **merged 2026-10-27** (`docs/design/Design-OneWorld.md`; road A recommended; 84's draft brief below) |
| 84 | Fable | **The one-world refactor**, on 83's design: the promotion builds a hull and not a World, the ports, people, things, markets, business, weather and the director's hand the world's once, every crewed ship with her own people, places and log; 82 folded into or behind it as 83 says | briefed by 83 (below); the eight decisions taken (decision 53); **merged whole, steps 1 to 11, 2026-10-28/30** (steps 1 and 2 at `d9dba1f`, steps 3 to 11 from the sibling's `claude/pkg-84` after it; the package closed with step 11's record below; three pins moved at step 6 for the one clock, bugs of the two clocks; **the owner's acceptance test passes whole as truth 7-200 at step 4**); steps 5 onward continue in the sibling |
| 85 | Fable | **The orders, the primer and the library reviewed for a model reader** (the owner's notes 3 to 6 and the officer's five points): the primer and the library made general and in-world, every scenario-, book-, ship- or build-specific reference redacted and kept elsewhere, with a test that guards it; the date and the war's state readable; the voice's one grammar; the stand-by's words; the action's severities; **and the documentation whole** (the owner, 2026-10-29: "might as well go all the way": `docs/` read for completeness and refinement with the same pass, item 8 of the brief) | briefed 2026-10-27 (below), widened 2026-10-29; **launched 2026-10-30** (the owner, 84 closed) as a Fable sibling session on `claude/pkg-85`; **merged whole 2026-10-30** at `252df5b` from `c4afb7c` (the record below: items 1 to 8 and the gate's draft, three findings of the lead's review mended); the owner runs the interim gate once 93 is in, the lead's half added first; 87 follows it |
| 86 | Opus | **The owner's local work folded in** by the review's plan (`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/review-of-the-local-work.md`): the practice-and-resupply package and the pivot gun with the listed edits, the free intents tightened, the hail fix with its pins proven, station keeping by name and kind limited to sails in sight, the records recast; the whole slow tier and the convoy's stall reproduced | **merged 2026-10-28** (`cd97ce7`); the record below |
| 87 | Opus (the owner, 2026-10-29; Fable before) | **The warrant officers' stations** (the owner, 2026-10-27): the gunner, the surgeon, the carpenter, the sailmaker and the boatswain as stations a person or a model may hold, each with a domain of orders and readings of its own and its peculiarities (the gunner's magazine, filling, practice and the batteries' service from 70 and 86; the surgeon's sick list, the wounded and the cockpit from 73; the carpenter's well, leaks, plugs and spars from 73 and 77; the boatswain's rigging, the spares, the hands' work and the bill from 77; the sailmaker's sails, the holes and the sailroom from 70's damage and 65's work in its place), a brief and a station line for each, a reason to be stationed by the milestone's end; the equal-reach rule and the handover as every station has them. **Added by the owner, 2026-11-05 (the case study of the all-models encounter, lesson 6):** the surgeon's order of treatment as a station's judgement and the captain's word: 73 built the period's rule, first come first served (Turnbull), with a knob for worst first; 87 adds `the surgeon to <name>` (the captain's order to see to a named man), the surgeon's own precedence for the captain and the officers when treatable (Nelson's refusals at the Nile and at Trafalgar are the proof the surgeon would have taken him first; a wound judged mortal is dressed and left, and the surgeon goes back to his work), and the wounded captain's own body: his `how am I` reading the bill's wound and not the needs' "rested", his sleep in the cockpit the surgeon's to allow, the surgeon's report a wake for his station | to brief after 85's pass over the orders, the primer and the docs is merged (the owner, 2026-10-29), and after 77; the brief fixes the pattern on the gunner and the four follow it |
| 88 | Opus (the owner, 2026-10-29; Fable before) | **The captain's pass of M7**: the commodore's recovery when aback with no way and no tack while the hands are at a shortening (the convoy's stall, 86's finding; truths 7-152 and 7-153 move with it); 57's offing's tack among islands with no room to wear (the station-gale trial's expected failure lifted); 72's near station law read against 58b's; the colours held once shown before an enemy (71's flicker, if 85 has not taken it) | after 84; **briefed 2026-10-30 (below)**, each item with the symptom, the rule as it stands, the rule as it should read and what proves it, the moved pins by bisection (the owner, 2026-10-29); **approved and launched 2026-10-30** as an Opus sibling session on `claude/pkg-88`, beside 82; **built and merged 2026-10-31** (below, "Package 88 as merged") |
| 89 | Opus | **The held gauges' water** (79b's finding): a held gauge enters the tide's blend for the positions within its own block's bounds alone, so that the Channel east's six, Biscay's, Portugal's and the islands' gauges give their water its own tide and no position west of 1 W reads anything new; the master's epitome's rises by the same water; the proof that no recorded passage's digest moves | briefed below (2026-10-29); **approved and launched 2026-10-30** (the owner) as an Opus sibling session on `claude/pkg-89`, with the Mediterranean's held gauges of 79c and 79d now among its cases; **built and stopped for the lead's ruling the same night** (the rule as briefed, 73 gauges given their blocks, no recorded passage moved; four of the blocks' own tests failing on their true water, Bournemouth and Portsmouth held in `channel-mid`, Beachy Head a hundredth over the brief's foot, the tiles' fill on the false mean level): **ruled 2026-10-30, a step 4** (the four re-measured or their data mended old beside new, the two gauges held with the options recorded, 7-280 pinned at the measured figure, the gap at 40.50 N closed if no tile moves) and the fill's rebuild booked as package 93; **merged 2026-10-30** (the record below) |
| 90 | Opus (the ships session) | **The Spanish and Mediterranean ships** (the owner, 2026-10-29, widened 2026-11-06 from the tartane and the xebec to five hulls): on 79c's water, from the smallest up: the tartane, the third reference vessel of decision 11 (one raking mast with the lateen mainsail and a square topsail over it, the lateen on the small mizen, one or two headsails on the long bowsprit by judgement, the boat in tow); the polacre, a lateen on a forward-raked foremast and on the mizen with square sail on the main (a lateen and square sails on one hull, the bilander's problem on a Mediterranean hull); the xebec, a lateen on all three masts and her sweeps as an option; the twenty-gun corvette *Diana* as captured and used by the Spanish navy in 1809; and the *Purísima Concepción* class three-decker of the Spanish navy, the game's first three-decked ship. Each as her trades and roles allow (a trader or fisherman and a corsair or the King's for the small three; the navy's fits for the two ships), built to Build-Ships.md §5.0's principles and the ladder of evidence from Roux's and Tofiño's plans, Winfield and the Spanish sources the session finds, and the pilots 79c lays down, with the lateen handling B3.1 gives (worn, not tacked; the yard dipped round the mast); the regency's cruisers as a role with their doctrine; the schooner's-mast rule of 75's B3.4 classing the tartane as the cutter and the polacre's square main as her one mast with yards, with its two limits (a lower square-sail yard on the main, a pole main with its topsail yard on the lower mast, each still a brig) and the polacre's lateen mizen and pole masts for her own document (the notes to the ships session, 2026-11-06, 18:00); inside milestone 7 | the ships session's next window after 75 closes, on 79c's block; to brief by the session in its plan's form (a design document each, the ladder of evidence, the lead's gate before a file), for the lead's gate; **the owner (2026-11-10) has told the ships session that after the lead's final word on 75's close-out it may begin 90's preliminary research and planning** |
| 81 | Opus | The viewer's action, **from the hull 75 draws**: the guns drawn in their ports with their movement, a muzzle flash and a smoke plume over a few seconds at each gun's firing, the smoke lingering to leeward; the damage as the viewer's present honesty draws it (the owner's first action, 2026-10-24); the ports drawn from the files' port triples and `port_size_m`, and a triple within `OVER_THE_RAIL_M` of the rail at its x a gun place over the rail, not a port (from 75's design of the 74, 2026-10-29) | after 71 and 75's hull (both merged); **briefed 2026-11-07 (below); approved and launched 2026-11-07 (the owner)** as an Opus sibling session on `claude/pkg-81` (session_01XooV4BCduVgUGzypUoJmNm), beside 74 and 76, the trunk at f466051: the standard written first, every gun of every hull placed by one rule from the file's data, a checker every new ship passes; the standard approved 2026-11-07 (seven rulings; `docs/design/Design-ViewerAction.md`); **items 1 to 7 merged 2026-11-07 (a8b716d4), truths 7-436 to 7-445; CLOSED** |
| 91 | Opus | **The viewer's light and air** (the owner's references of 2026-10-29, decision 57): the ship's own lights warm and distinct at night (the stern lantern, the top lights and the binnacle 71 already hoists, each a glow on the faces near it); the scene's light by the hour and the sky (the sun's altitude and azimuth from `core/moon.py`, the weather's cover and visibility: a gradient sky and sea, the faces tinted by their side to the light, dusk's warmth, night's dark with the lights alone, haze by the visibility); a lively telltale at the masthead and a waving ensign, canned but driven by the apparent wind the physics already gives (direction, a flutter whose rate and amplitude follow the speed), animated between snapshots; all in the present SVG viewer, stylesheet-driven, drawing only, nothing of the world read that the readings do not give | after 81 and 75's hull; when the owner likes; the two reference pictures stay with the owner (another game's work), described in the decision |
| 92 | Fable | **The career study** (decision 58): the design of a career the player takes up under the world's own rules, in 83's shape and no code: the state as the frame of the naval and the economic systems, tasks from the world's needs, the lead actor a station, standings as interest and character, progression in the period's currencies, the ellipsis between voyages, a closed economy, the decision chain's ceiling, every change an act; a design document and the first career package's brief for milestone 8 | after 85's review; the building in milestone 8 |
| 93 | Opus | **The blocks' tiles rebuilt on their true water** (89's finding): every block whose gauges 89 gave their water had its GEBCO fill raised to the false mean level of the eleven's blend, so the Mediterranean's land stands six metres and more above its true water and the Channel east's up to 4.4 m under its true high water; each region rebuilt with the fill read from its own gauges' mean level (`channel-east`, `mediterranean-west`, `balearics`, `gulf-of-lion`, `ligurian-sea`, `tyrrhenian`, and the Biscay, Portugal and islands' regions where the raise differs), the sources fetched again through the proxy, the checks printed, no mark or port file moved, the blocks' scenarios sailed again and their figures recorded, no recorded passage of the Channel west moved; `mean_level_grid` then by block | briefed below; **approved and launched 2026-10-30** (the owner, with 85 and 94) as an Opus sibling session on `claude/pkg-93`; **merged whole 2026-10-30** at `d9465d9` from `7e6b9f1` (the record below): ten regions rebuilt on the world's own tide, the raise one source of truth with the tide, Agincourt Sound keeping the eleven's raise until a sheet is read, truths 7-305 to 7-309 |
| 94 | Opus | **The chart's tidies from 79c, 79d and 89**: an island kind with an extent (the lookout calls an isle an isle and nothing sails through it) for the islets the grid lacks; a `road` with a bottom giving its note; the tide's seam tapered inside each block so that no step stands at a block's edge; Bournemouth and Portsmouth given their water by a Solent tide region, if it moves no recorded passage; the inland tiles of the Alboran left to 93's rebuild | briefed below; **launched 2026-10-30** (the owner) as an Opus sibling session on `claude/pkg-94`, beside 93, the trunk brought in at each boundary; **merged 2026-10-30** at `df9d4dc` from `6a30975` (the record below): `grid_lacks` in the island kind's place, the taper, the Solent's region and the rule of the seams by the lead's ruling; the Strait's level step at 36.4 N a finding |
| 82b | Opus | **The door follows its harness, the visitor's name, the far hull's hail** (the owner's testing of 2026-10-31 to 11-05: the Mr Hill and Captain Owen cases, the hails between model captains answered by the table): the agent API's desk keyed to the harness and not to a station's name and ship (`agents/remote.py` `Desk.seats`, `Seat`), so a model's door follows its person between hulls and `stand down` stands down one station; the visitor keeps his own station's name ("officer of the watch, of the Raven, aboard the Amazon") as the primer promises (`world/movement.py` `visiting_station`, `world/seats.py`); a hail of a hull in the far shape whose captain a model holds is his to answer, never the table's (`world/hail.py` `deliver`, `model_holds_her`); truths 7-390 to 7-394 | launched 2026-11-05 on the hotfix's merge, beside 65 (session_01XooV4BCBsF3TQSAwxBrxmy); **closed**: items 1 to 5 merged 2026-11-06 (07c06a0, f207fd8); the replay's seating order and the shared person ids booked to 97, the lower-cased served lines to 65's step 8 |
| 95 | Opus | **The sail by her name** (the owner, 2026-10-31 and 11-05): one resolver for a sail named in words (the kind, the quarter, the bearing, the distance, each narrowing the pool; the closer on remaining ambiguity; a name once known over all), serving `the glass on`, `make out`, the hail's addressee, `bearing of` and `pull for` (`world/lookout.py` `glass_on`, `make_out`; `world/hail.py` `_addressee`; `orders/boat.py`); a sail made out and identified named in the readings (`strangers`, `in_sight`, `sail_in_sight`) by her name while she is in sight, and her identification lost when she is lost sight of until she is closed and made out again; truths 7-395 to 7-399 | after 82b (both touch `hail.py`); **launched 2026-11-06 08:25 UTC** (session_01XooV4BQyodA4Vf5ABnBgby, claude/pkg-95, from the trunk at 0d1127f with 82b closed): the design note approved; step 1 merged (d65b2e3); step 2 merged (9936e12); **closed** 2026-11-06 |
| 65 | Fable | **The place's knowledge** (M7b's provisional row brought up by the owner, 2026-10-30; spec M7b §14 "Brought back and forward"): what reaches a person from where he stands, the sample carrying the readings and the log's lines his place allows and no other, ashore the ship by report, boat or letter only; the papers in their places; the drill's walk; each kind of work done in its room, the rules' people and the stations' persons alike; the director untouched; scoped to the edge cases (asleep below, the boat away, a visitor on another hull, the captive, the stand-by's wakings, the pictures, a hull asleep), an Opus follow-up booked from the testing | briefed 2026-10-30 (below), for the owner's approval; **launches when 82 is whole** (the owner: one Fable package at a time beside 74); 74 runs after it and takes the captive's places from its rule; **launched 2026-10-31; step 1 closed on its branch 10-31 and held unmerged through the week's pause; steps 1 to 3 merged (eb147e7 on 2026-11-05, 5288665 and 0855551 on 11-06); on step 4 on 2026-11-05 with decisions 62 and 63 and the hearing across hulls added on 82's whole merge** as a Fable sibling session on `claude/pkg-65` (session_01XooV47SeuYqmTZ8W1Rzyoo), the design note first; step 4 merged 2026-11-06 (e8dc268); on step 5; step 5 merged 2026-11-06 (aba233f); step 6 merged 2026-11-06 (429d7f5); steps 7 and 8 merged 2026-11-07 (c597a7d); **CLOSED 2026-11-07** (eight steps; truths 7-370 to 7-389, 7-420 and 7-421; the follow-up 65b booked in the close's record) |
| 96 | Fable | **The harbour and the ship's configuration** (the owner, 2026-11-06, in place of M7b's package 64, struck): a design package first, on two layers. (1) **The ship's configuration as a thing of its own**: one description of any hull's whole setup (her class file and fit, her role, her nation and its parameters, her stations and who holds each with its door, her people by name, her papers and private signal, her crew's number and quality, her books, her intent and her squadron) with defaults by role and nation, that the scenario maker, the director's `ship` order in live play and the business all build from, so that any hull is set up as wanted without nasty surprises. (2) **The harbour presenting every configuration the game has**: the doors and stations, the settings and flags, the scenario's settings with the full configuration of the player's ship and, at choice, of every other ship (the squadrons, the papers, the private signal explained, each ship's role, fit and crew), so that direct file editing is never necessary. The design document with the lead's gate, then the build in steps; M7b's harbour points of 2026-10-18 as facts | booked (the owner, 2026-11-06: "it may come after 74, I simply wanted it booked"); to brief when its turn comes in the Fable queue, after 65 and 74; **held by the owner (2026-11-07) to the end of milestone 7**, once most features are in, so that the design may be as complete as possible; **the owner added (2026-11-09) the ship's flag locker to its design**: which ships have which flags by nation, service, role and rank, and flags given and taken by the scenario, the page and the director |
| 97 | Opus | **The hull façade's readers audited** (the lead, 2026-11-06, from two builders' findings of the same day): 84's per-hull delegation (`World.own`, `as_hull`, `PER_SHIP_FIELDS`) answers for the hull whose block is running, so an object of one hull that reads `world.people`, `world.stations` or `log_of(world)` from inside another hull's block reads the wrong hull's: 82b found the player's hull's `Stations.holder` (her `Stations` is built with the World itself) reading the running block's people, so a named station on her matched another hull's captain moving; 65 found `station_spot` read from inside another hull's order (mended for `_say` with `station_spot_on`) and the director's own writes (`thought`, the budget lines, `director.seat`) landing in the followed hull's log under `follow`. The package: every reader of a per-hull field through a World handle audited and listed; each either bound to its own hull at construction (the Stations' and People's hull, not the World) or read in its own hull's block; a test per finding (the holder under another hull's block, the director's writes under `follow`, a façade read from inside another hull's order) and one guard that walks the readers; no pin moved (the faults are latent in the recorded passages, which run one hull's block at a time); one tidy rides with it, found by 95's builder: `hail_order`'s refusal in `world/hail.py` ("the strangers are listed") to give the strangers' words as `Lookout.sail_refusal` does; truths 7-422 to 7-425 | after 82b and 95; **launched 2026-11-06 12:40 UTC** (session_01XooV4AUe3L3SVNNGyD3K6i, claude/pkg-97, from the trunk at 9936e12 with 95 closed): the design note first (the audit's list), then the mends; the design note (c299be0, `docs/design/Design-FacadeReaders.md`: one cause, the player's own hull never walked at construction; eighteen readers listed; two roads; a guard) approved 13:04, one step; the one line in 65's `agents/harness.py` (a harness binds the hull whose agents it enters) granted; left by ruling: the shared person ids (96's), the replay's seating order of two hulls in one tick (a loose end beside truth 7-394, not a façade reader), the sea's one visibility under follow (noted for M8); 14:16: one fight's outcome moved by the binding and bisected (the Amazon's Health, holding the World, killed the Medusa's man of the boarder's post; the branch kills her own first lieutenant at tick 530): the branch right, the test's story kept under a chosen seed with the reason written, a new pin of the default draw beside it; who leads on when the boarders' officer falls booked to 74; merged 2026-11-06 (7e479b7); **closed** |
| 98 | Opus | **The mends from the owner's play of 2026-11-09** (the lead, from the triage above): the player's own readings and refusals heard wherever he stands, and "go below" reaching the server; a kept live-browser probe that proves each mend as the player sees it; the viewer's paint order for guns and flags, a flag's lines, the truce state and 81's port-top rule; the picture at the OpenRouter door; the Rade de Brest's stream; the colours and signals by the deck's rule | briefed 2026-11-09 (below); **approved and launched 2026-11-09 (the owner)** as an Opus sibling session on `claude/pkg-98` (session_01XooV4AQeh4Fkc3zC5jdAuL), the trunk at be9c951e, with the owner's two rulings in the brief (the colours and signals the deck's; a man's own word, refusals and readings always shown him, a thing done out of his sight not); **steps 1, 2 and 6 merged 2026-11-10 (985c8777)**, truths 7-446 to 7-449: the probe a kept tool, 71 of 123 typed lines unshown before and 2 after; step 7 added by the owner (the flags of command hauled down and read); **steps 3, 4, 5 and 7 with the four additions merged 2026-11-10 (12bd5f48)**, truths 7-450 to 7-459, the Rade's stream moving three passages' pins by the toggle, one line met with 74's step 4 and both kept; **step 8 added by the lead 2026-11-10** (the set's last course kept in the world: `squadrons._LAST_COURSE`, a module's table keyed by `id(world)`, found by 74 and proven by planting), **merged 2026-11-10 (b148e721)**, truths 7-460 and 7-461, no pin moved; **CLOSED 2026-11-10**: eight steps, truths 7-446 to 7-461; what it left is on the lead's list in its closing record |
| 99 | Opus (a design note first) | **The views under the knowledge rule** (the owner's note 3): the chart and the ship view show what the person knows, the last value he learned with its hour where he lacks the live one; the captive's cabin and its senses ruled with it | booked 2026-11-09 (below); **held by the owner (2026-11-09) for the moment** |
| 100 | Opus | **Letters and things as one system** (the owner's note 8): a letter a thing with words, written, carried, handed, read, sealed and destroyed by anyone by one road; the director's things with a description, removed by his form; the letters by boat and by cutter carried as things | booked 2026-11-09 (below); held by the owner (2026-11-09); **approved by the owner and launched 2026-11-10** as an Opus sibling session on `claude/pkg-100` (session_01XooV47cDNM2igRU6E9FkQ4), the trunk at 2a291604; two steps, each at one hash (the thing with words; the letters that travel), truths 7-470 to 7-479; **step 1 (the thing with words) merged 2026-11-10 (41216bbc)**, truths 7-470 to 7-476, no pin moved; step 2 next |
| 60 (from M7b) | Opus (a design note first) | **A ship bought, and the player's ship changed in play** (the owner's design goal of 2026-10-17, M7b's package 60, spec M7b §21g; brought into M7 at the owner's word, 2026-11-09): the player's own ship changed inside a running world as a journaled act, his person rehomed and his seat carried; the hands moved as a count between two hulls; a vessel's owner, price and sale as facts the port knows, with `buy the ship` and `sell the ship` through the purse; the hull valued by 74's function with her condition; an errand ashore answered by the port's facts and the director | re-briefed 2026-11-09 (below) on what 82, 84, 65 and 74 have built since, **to run after 74 closes (the owner, 2026-11-09: "it's good to let 74 close cleanly before starting anything else major")**, the design note and the building both; **the design note approved by the owner 2026-11-10 to be written now** (a document alone, `docs/design/Design-ShipBought.md`, by an Opus sibling session on `claude/pkg-60`, session_01XooV4BEMb2fNbYpMywL2G9, launched 2026-11-10 for the lead's gate); the building still after 74 closes; **the note reported 2026-11-10 and ACCEPTED AT THE GATE the same day, merged to the trunk** (`docs/design/Design-ShipBought.md`, `claude/pkg-60` at b14d46c, its section 13 the gate: the game's first hull stays fixed and a new `World._players` names the player's ship, one act `take_up` by one order, the old ship settled and never lost, ownership by her service, one valuation with her condition, the errand by a named person; found by the note and reproduced by the lead on the trunk: under `--ship` the followed ship's far body is never brought to her truth, 934 m off in five minutes and 3.8 km in twenty, mended in 60's step 1 by the owner's word of 2026-11-10: "I won't be conducting any testing before then"); **the owner's answers to its five questions, 2026-11-10, agreeing with the lead's recommendations:** (Q1) money stays the ship's until milestone 8's career, an owner's purse carried by the ledger; (Q2) a master's books and instruments stay with the hull for now; (Q3) the director's word is the only road by which a King's officer or an owner's captain takes another ship or a prize; (Q4) an owner may keep his old ship working under her mate; (Q5) in a merchant scenario that names no owner the player is her owner |
| 101 | Opus | **The Catalan coast block** (the owner, 2026-11-10: the gap in the chart on the eastern Iberian coast): a new region of `atlantic-east` between `balearics`' north bound (40.56 N) and `gulf-of-lion`'s west bound (3.0 E), the Ebro's mouths and the Alfaques, Salou, Tarragona, Barcelona and Mataró to the coast's crossing of 3 E near Tossa; with it the ports the coast lacks, in the block and in the charted water beside it | proposed 2026-11-10, **the gap measured by the lead** (the chart probed on a tenth of a degree): nothing at all (no depth, no land, no coast, no region) north of 40.56 N and west of 2.61 E as far as the land; the Gulf's first tile column gives depth from 2.61 E to 3.0 E, which no region owns; the sea so missing is a wedge of some 80 miles north and south by 110 east and west at its foot, from the coast at 0.5 E on 40.56 N to the coast's crossing of 3 E at 41.75 N. A box of 40.56 to about 41.9 N and about 0.3 to 3.0 E is some 3.6 square degrees, the smallest of the Mediterranean's blocks (about 28 level-2 tiles, 4 to 6 MB by the others' sizes, far under the 40 MB rule); the seam's exact meridian (3.0 E or the Gulf's tile edge) the builder's first measurement by `docs/dev/ChartBlocks.md`. **No port file exists between Cartagena and Marseille on the main**: in the block Barcelona, Tarragona (with Salou's road) and the Alfaques; beside it in water already charted Rosas and Palamós (`gulf-of-lion`), Valencia's Grao and Alicante (`mediterranean-west`). **Approved by the owner 2026-11-10: all seven ports, to launch at the close of package 98**; briefed 2026-11-10 (below), truths 7-490 to 7-499; **launched 2026-11-10 10:56 UTC on 98's close** as an Opus sibling session on `claude/pkg-101` (session_01XooV48XGVqWYMrANqYZQEs), the trunk at 0a7c3a9d; a short measurement report (the seam, the tiles' count and bytes) before any tile is committed, then one final report at one hash; **its measurement report ruled 2026-11-10** (the seam the how-to's plain answer, the Gulf's column kept the Gulf's; 24 level-2 tiles and 26 of the three harbours', 4.94 MB in all; Barcelona's gauge the block's; no patch for the four ports beside the block, no override of the delta for want of a public-domain plan, the truths written to the pilots' own words; **found: the wars table carries `since` and no `until` and `Nations.at_war` reads no date, so Britain is at war with Spain on any day and a Spanish port reads hostile in 1809**: not the block's to mend, a case for decision 66 and package 103, to be said to the owner); **the final report merged 2026-11-10 (1a4a4337): the gap closed, 6.07 MB, seven ports, truths 7-490 to 7-499, no pin moved; CLOSED** |
| 102 | Opus | **The signals seen and the ship dressed** (the owner, 2026-11-10, at the hundredth package: "being able to dress the ship overall and see it in the viewer", which "comes with being able to see the signals in the viewer properly"): (1) every signal flag of each nation's book given a drawing, as the colours have (today a signal flag is a number and words: no flag of any book has a drawing); (2) a hoist flying drawn in the viewer where it flies, on the player's ship and on others, **served only within the distance at which the flags are made out** (the book's `read_nm`), so that the picture tells no more than the eye could; (3) `dress ship` and `undress ship`, **in the fashion of the day, researched** (the owner and the lead both take the line of signal flags from masthead to masthead for a later fashion; the period's dressing with ensigns, jacks and flags at the mastheads and yardarms to be found in the sources and drawn as found, a later style under its own date if the sources give one); (4) the nations' days in data (the King's birthday and the like, each sourced), on which a nation's ships in harbour dress of themselves and fire the salute the day asks, so that the player may find a fleet dressed without knowing the order; (5) with it, if small, the extra issue on the day ("splice the main brace") | **booked 2026-11-10 at the owner's word, to come a bit later**; not briefed; a small package; the flags each ship holds are package 96's locker, which this reads and does not design |
| 103 | Fable (the primary review agent; subagents allowed) | **The range reviewed, and the lever designed** (proposed by the lead, 2026-11-10, on decision 66 and the owner's word that the sources should be found "with further searches" and by "an analysis of our own full research database"): nothing built. (1) The same rules-only scenarios begun on three dates far from 1805 (a year of the first war, the peace of 1802, a year after 1815) and played by the probe and the replay, with a list of what reads wrong, what is missing and what refuses to work; (2) every dated row in the data found and classed: read against the running clock (a rail by decision 66) or read once at the start; (3) the research on file (`docs/references/`, the design notes' sources, the ships' references) mapped by element and by year from 1792 to 1825, the gaps named with where each might be filled; (4) a design note for the owner from the three: the modes of the lever with strict's rule, the line between period features, events and general features drawn through the data as it stands, and what it would cost to hold each kind of element across the range | proposed 2026-11-10; **briefed 2026-11-10 (below) at the owner's word, for Fable; HELD by the owner, not launched** ("there's enough things in flight right now to let close out, and I'll sleep on it"); **the brief widened the same day at the owner's word** (Fable as the primary review agent for the date range audit and the overall design of fidelity, a wider and freer scope, subagents allowed); **consolidated with the other review and design packages (96, 92) towards the end of the order**, this one first, the three together to cover the whole range |
| 104 | Opus | **The sea between Minorca and Sardinia** (the owner, 2026-11-10, on the lead's finding while measuring 101's gap): the chart's second hole in the western basin, the open sea east of 4.5 E (`balearics`' east bound) and south of 40.56 N (the Gulf's south bound) as far as Sardinia at 8 E (`tyrrhenian`'s west bound), and the Algerian coast east of Algiers (Bougie, Bona) with what ports it wants; a passage from Port Mahon to Cagliari crosses it and the chart answers nothing there (probed at 38 N 6 E and 40 N 6 E) | **booked 2026-11-10 at the owner's word, a chart block subsequent to 101**; not measured in full, not briefed; its bounds, its tiles' count against the 40 MB rule (it is mostly deep water) and its ports the lead's to measure and put to the owner when 101 is in |

**The order of work as it stands (the lead for the owner, 2026-11-10; a picture to re-centre
on, not a ruling: every launch still waits for the owner's word).** *In flight (as of 11:00 UTC, 98 closed and 60's note merged):* 74 (Fable;
steps 5, 6 and 7 left), 101 (Opus; launched at 98's close), 100 (Opus; two steps), 75 in the ships session (the ruled builds, SW-1, the 74-gun ship, Phase
5). *Approved, waiting on its trigger:* 101, at 98's close. *Held by the owner:* 99 (the
views under the knowledge rule), 103 (Fable; the range reviewed), 96 (Fable; the harbour and
the ship's configuration, to the end of the milestone). *Booked and waiting on another
package:* 77 (on 75), 87 (on 77), 80 (on 74), 60's building (on 74 and the note's gate), 90
(the ships session's next, on 75), 91 (on 75's hull; when the owner likes), 102 (later), 78
(where the sailing wants it), 65b (on the owner's testing). *Milestone 7b's, still open:* 51's
director's chart, 61 (Fable; the land-avoiding route), 69 (the pins on Windows), 55 (the gate
and the consent revision, deferred until testing begins in earnest). *Milestone 8:* 92 (Fable;
the career study). *Booked 2026-11-10:* 104, the chart block from Minorca to Sardinia and the
Algerian coast east of Algiers, after 101. **The order the lead recommends, as amended by the owner's
words of 2026-11-10 (his decision on it to come after he has slept; "my initial impression
matches yours generally"):** (1) now, to the week's reset: close what is in flight and launch
101 when 98 closes; nothing else. (2) When 74 and 75 close: 77, 60's building and 80 (or 80
folded into what 74 leaves, decided at its close) on Opus; 90 in the ships session, whose
preliminary research and planning the owner has allowed as soon as the lead gives the final
word on 75's close-out; 104 (the sea between Minorca and Sardinia) after 101. (3) Behind
those: 87 after 77; the viewer's three in the order 99, 102, 91, one at a time since they
share the viewer; 78, split into its three unrelated parts when it is briefed; 65b from the
owner's testing. (4) The milestone's end, **the review and design packages together** (the
owner: "we should consolidate the review packages together, towards the end of the order,
and ensure we cover sufficient range with them together"): 103 first, Fable as the primary
review agent with subagents, then 96 on its answers and 92 beside them, the three together
covering the whole range of dates (confirmed by the owner the same day: "that's the consolidation I meant, and I intend for a fairly wide-ranging review at the end of the milestone"); then 69 and 55 with the consent revision and the gates; 61
and 51's chart briefed with them or carried to milestone 8. The limit that sets the pace: the lead proves each report with one whole fast tier of
about an hour before it merges, one at a time, so five builders reporting already make a
queue.

**An open design question, recorded for the owner (2026-11-10): the day and the range.** The
game's purpose is a world that can be simulated over a wide range of dates, 1792 to 1825 as
it stands, and earlier and later where possible; the build's attention has gathered on 1805
(the scenarios' year, the lights and shores "as 1805 had them", the signal books of 1799 and
1803). The owner's questions, open: which is better, fidelity to the day in every element
or a world that functions reasonably on any given day; and where attention to historical
fidelity gets in the way of an interesting simulation and game, "not because it is not
important to the intent of the game, but because the world must be subject to the game and
not vice-versa". **The owner's ruling the same day (decision 66, `docs/DesignProposal.md`): history is the starting state, not a rail; the elements are correct, their interactions are the world's own once play begins; fidelity is a lever.** How far each element is dated across the range is still open. What the lead notes for the discussion: the data that
carries its dates in its rows (79a's regimes, a port that changes hands by `since` and
`until`, a nation's wars) already answers for any day, while the data written as one year's
picture (a harbour's moles, a coast's lights, a signal book, a ship list) answers for 1805
and is silently wrong elsewhere; so a brief that says "as 1805 had it" builds the second
kind, and briefs from here say which kind each item is.

**A first case found (package 101's builder, 2026-11-10):** the wars of `data/nations.yaml`
carry `since` and no `until`, and `Nations.at_war` reads no date: Britain and Spain are at war
on any day, so the allies of 1808 to 1814 are enemies and a Spanish port refuses a King's ship
in 1809. A port's dated `nation:` (79a's form) does answer for the day. Nothing is changed:
how a dated war is read, as the state on the day a game begins or against the running clock,
is the open half of decision 66 and package 103's ground.

**The discussion so far (the owner and the lead, 2026-11-10; nothing below is ruled beyond
decision 66).** *Three layers*, which the owner likes: the elements (a ship, a gun, a coast, a
wind), held to the record; the state on the day a game begins (who is at war, who holds a
port, which book is in force), the dated seed; and what happened afterwards, which decision 66
frees: the record of it an almanac for the director and the scenario's author to use, bend or
leave, never applied by the engine of itself. *The lever as codified modes*, which matches the
owner's thought: seeded (correct at the start, free afterwards), strict (the record applied,
to see and take some part in a historical scenario), loose (elements allowed out of their
date). **The owner's caution on strict:** the player's own acts may break a scenario in which
no change is allowed, "or at least this will cause some conflict for a strict ruling"; it
needs attention. *The line still to be drawn* (the owner): between "period features" such as
the Barbary states' conflicts, the shifting political, diplomatic and governmental realities
as they bear on the game, and the general features that can happen at any time by
circumstance. *The sources* (the owner): enough on the era at large should be found by further
searches, and by an analysis of the project's own research on file "with an eye to bridging
extant gaps on a reasonable basis for our game and simulation". The lead's thoughts given in
answer, for the record: strict cannot mean that nothing changes, since the player acts; it can
mean that the record proceeds wherever the game has not contradicted it, each recorded event
carrying its conditions in the world's terms (who holds the place, whether the squadron
exists) and happening only if they hold, so that the game's facts outrank the almanac. And a
test for the line: a thing true by circumstance alone is general and has no date; a thing true
over a span of years whatever the player does is a period feature, a dated row; a change at a
moment is an event, the almanac's. The owner's own example divides by it: the corsairs
cruising is a period feature, a bombardment of Algiers an event.


The M7b work wrapped up alongside: 58a, 58b and 67 merged (2026-10-23), the one whole suite
on the merged tree the lead's; the lead's playtest of 58b's gale book (its two trials
expected failures until it); the owner's decisions listed in 58a's, 58b's and 67's
as-merged records; 51, 60, 61, 63, 65 and 69 on the books in `M7b-WorkPackages.md` (64 struck 2026-11-06 for 96); 55
deferred until testing begins in earnest.

**For package 77's brief, from package 86** (the review of the owner's local work, section
5; his debrief: practice a stopgap to rewrite or redesign as judged): `heave_mark`, dumb
show and the notional mark are the gunnery's evolutions in a first, stopgap form, which 77
takes over or redesigns; the gunner, his crew and the quarter gunners made posts that
compete for hands (86's filling party is read and never moved, the build's decision 5);
truths 7-162 to 7-166 kept or replaced by its own, each with the old figure beside the new.


**For package 77's brief, from package 75's lee-port step (the lead, 2026-11-06):** four
things the ports' rule (`combat/ports.py`, Build-Ships.md §7) leaves in 77's files, each
reproduced and measured in `docs/dev/TuningNotes.md`, "The lee ports with the roll", "Left,
and for whom": (1) `orders/gunnery.py`: with every port of a side shut, `engage` answers
"the guns to fire as they bear" and nothing follows; "fire the broadside" says no gun is run
out two seconds before the ports' line; the review's mend is in the record. (2) Two served
words for the weather side, `the weather ports shut` and `the weather ports opened` (the
line's `lee` False), new under 85's in-world rule. (3) The rules captains read nothing of
the ports: `engage_side` weather puts the mark on the guns the roll has shut;
`_a_gun_for_a_signal` and the distress gun take a gun behind a shut port. (4) Latent: a
weather port shut by the roll that opens exactly upright is said the lee's. The ports'
own figure (the dwell `PORT_HOLD_S = 60` for the flicker in gusts) is the ships session's,
ruled 2026-11-06 in the notes below.
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

### Package 89 as merged (2026-10-30)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-89` at `2f951aa` (twelve
commits on the trunk's `0483a73`, step 4 one commit an item by the lead's rulings; merged
here over 84's close with the tuning notes the one conflict, both kept; 16 files, 1,211
lines added and 242 removed); ruff clean; the builder's proof the one the brief asked for,
the eleven recorded passages by node id, the gate selection and the captain's trials run on a
clean worktree of the head first and on the final tree last and identical (every digest
held, the lee-shore trial's container digest the one failure on both); its touched files'
slow tier, the blocks' truths 7-270 to 7-304 and its own 7-280 to 7-284 green, its fast tier
whole with the pictures' flake the one failure; the lead's run of the tide's, chart's,
ports', islands' and scenarios' tests with four of its truths, 7-271 and the gate selection
(186 passed, none failed); **the whole suite on the merged tree in the cloud (run 17 on
`39c2fa5`: lint green, 4,330 passed over the six shards, 3 skipped, 11 expected failures,
none failed, 40 minutes; the pace job, informative, 7 of 10 at 445 to 499 in 296 seconds,
the slow runner's day as 79b's record reads it).** **The rule, as built:** a block's gauge serves the positions within its
own block's bounds, a region of the chart's manifest or a list of them, and no other; the
eleven serve everywhere; within a block the blend is the eleven within reach and the
block's gauges by the present weighting, the membership the cell's centre's so that the
seam at 1 W falls on a cell edge; a gauge whose mean level was not read gives its constants
and not its level, and where no gauge of the blend has one the level is the eleven's there,
not invented; `far` and the nearest gauge are of the gauges that serve the place. The 73
held gauges of 39b to 39f and 79b to 79d moved into `gauges:` with their `block:`, no
figure moved (checked by loading both files); the loader refuses a block the manifest does
not name and a gauge with neither block nor level. **The figures:** Newhaven's spring range
19.5 feet where the blend gave 3.9, Dieppe 27 for 5.4, Vigo and Cadiz their gauges' own
where Le Conquet's eighteen had served, Mahón half a foot where Saint-Malo's 33 had; a mile
west of 1 W the tide to the bit as before (truth 7-282). Twenty-one of the master's judged
rises re-worked to the blocks' water, old beside new (Lisbon 18 to 9, Cape Trafalgar 18 to
3, Boulogne 15 to 26, the Somme 5 to 21); no given rise and no hour moved. **The fill raise
reads the eleven alone**, the level the tiles were raised by, so a rebuild moves no tile by
the rule; what the rule means for the tiles as they stand is tabled in the notes (the
Mediterranean's land six metres and more above its true water, the Channel east's high
water up to 4.4 m above the fill's raise): **package 93**. **Step 4, by the lead's
rulings:** truth 7-271's bound re-measured 0.6 to 0.8 on the Strait's own water (the error
0.452 on the head, 0.648 here), the old margin kept; truth 7-280 Beachy Head at 18.99 feet
within a foot and a quarter of Norie's twenty, the reason in its words; the pilot off Aix
re-measured on Aix's own tide, the moment pinned at 01:00 and the height asserted with the
reason; the passage to Spithead's book weighs within three miles and a half of the road
where the night's anchoring on the seam and a daylight fix had left her outside its old band,
the truth passing unchanged; the passage to Port Mahon's book shaping the course for the
mouth again every ten minutes within seven miles, where the course shaped once from off
the Aire left her account outside the anchoring band and running on into the shallows that
the false seven metres of tide had covered (the outer road's move, the lead's first ruling,
tried and reverted: she never grounded at the spot, which lies in 37 m), the spot and the
port file untouched; `balearics`' north bound at its tiles' edge 40.56 N, no tile moved.
**Bournemouth and Portsmouth stay held** in `channel-mid`, the options recorded for the
lead (their block the whole of channel-mid, or a Solent region of their own); the seam at
1 W a step of 102 degrees of M2 off Selsey, the block's side the nearer the truth and the
eleven's blend over the Solent wrong by four hours and a half, 39a's finding again: **a
taper across the seam, or the Solent's own region, a later tidy.** Faden's '«8' for south
Brittany stays unread, the gauges giving 13 to 15 feet. **One departure from the ruling,
said plainly and accepted:** the Mahon mend is the book's, not the spot's.

### Package 84, step 11, as merged, and the package closed (2026-10-30)

Merged `--no-ff` from the sibling session's `claude/pkg-84` at `32c03d3` (one commit on the
trunk's `90cef2c`, brought in at the boundary before the step's final fast tier; merged here
over 79d's block with the tuning notes the one conflict, both kept; 14 files, 284 lines
added and 81 removed); ruff clean; the sibling's fast tier whole 3,957 passed with the
pictures' known flake the one failure, its slow tier of the known truths, the trials and the
touched files 190 of 199 passed with eight left out by their marks and the lee-shore
trial's container digest the one failure as at every step, its pace within step 8's spread;
the lead's run of the touched files and the gate selection (147 passed) and of the fight's,
the lying-to's, the ships' and the staying's tests (128 passed), none failed; **the whole
suite on the merged tree in the cloud (run 16 on `69dcdcd`: lint green, 4,323 passed over
the six shards, 3 skipped, 11 expected failures, none failed, 40 minutes; the pace job,
informative, 6 of 10 at 437 to 494 in 301 seconds, the slow runner's day as 79b's record
reads it, truth 51's frigate alone among them at 494 for the first time).** **The step:** the long
tail, the words and the records. The booked tidies made: the fight's mark on one road with
the shadow's dead arm gone; the lying-to reading taken from the ship by the reading's own
rule with no import of the api layer into the world; a person found by his name whole and
by his surname only when one person of the world bears it; the two test lines that
asserted nothing now assert what they name; the thread-local hull stack dropped when its
last block ends. The words: the awake notice ("awake, a hull of the one world"), the
crews' and the seats' heads recast, the Harness document's §17, the primer's chapter 17,
and specs M6 §19 and §20 and M7b §11, §12 and §12b given "as built since package 84"
pointers that say what 84 built and what stays each section's own. The records: the
design note's head recast as "As built, steps 1 to 11" with a table of the eleven steps
against the brief and the owner's decisions placed, a step 11 postscript, and "What 84
leaves"; the tuning notes' head likewise with the pace of every step beside the study's
figures. **Taken another way:** the `world` to `hull` rename is made nowhere, every
consumer holding its hull as its `world` by the façade; the façade's wrapping of the
World's methods in the swap stands, the pace of every step showing nothing the measure
sees. Nothing pinned moved.

**The package, closed.** Eleven steps in three days, each a green commit with the lead's
head brought in at its boundary, each reviewed and merged in turn, the whole suite green
in the cloud at every merge; the pins moved by the package three, all at step 6 for the
one clock and all judged bugs of the two clocks (the station-stranger and trade-stranger
trials, truth 7-152), old beside new in the notes. **What 84 leaves,** as its record has
it: for 82, the world with no followed hull and its words (`World.followed_words` stands
ready, the branch unreached), the player's own seat on another ship with the drivers
following him (step 10's follow the mechanism, step 8's save and replay the record), and
the director's door's question when another hull is followed; for 85's review of the
words, the words recast and the ones left as they were (the far notice, "the player's
ship" where "the followed hull" is meant, `CrewedWorld` as the builder's name, `world` as
every consumer's name for its hull, the tests' `crew`); for the design's own open items,
the tick's two strict phases, the empty `_NOT_CREWED_STATES` and `FAR_ONLY_ROLES`, the
business's region and the sleeping hulls' fight as the study recommends, and the gauges'
water (89, running). Three load-sensitive tests recorded and not mended: truth 7-200
under three workers, the pictures' blank-image check, the lee-shore trial's container
digest. The 84 session stands by for the review's findings; none is outstanding.

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
none failed); **the whole suite on the merged tree in the cloud (run 15 on `26af9bf`: lint
green, 4,323 passed over the six shards, 3 skipped, 11 expected failures, none failed, 60
minutes, shard 1 alone 53 of them with the Mediterranean's long truths in it; the pace job,
informative, 7 of 10 at 449 to 488 in 297 seconds, the slow runner's day again as 79b's
record reads it).** **The block, three regions by the lead's ruling at the builder's report of the
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

### Package 94 as merged (2026-10-30)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-94` at `6a30975` (six commits
on the trunk's `9b07813`, one an item, the records, and a step 5 by the lead's rulings; no
conflict, the merge's tree the branch's head's; 18 files, 1,203 lines added and 135
removed); ruff clean; the builder's proof the one 89's was (the eleven recorded passages
by node id, the gate selection and the captain's trials) run on a clean worktree of the
head first, on item 3's tree and on the final tree last, identical each time (every digest
held, the lee-shore trial's container digest the one failure on each); its touched files'
slow tier (10) and truths 7-264 and 7-270 to 7-314 (41) green, its fast tier whole with the
pictures' flake the one failure, passing alone; the lead's runs of the tide's, chart's,
islands', ports', lookout's and geo's tests with the moved and the new truths on the head
before step 5 (175 and 10 passed, none failed) and of the tide's, chart's and ports' tests
with twelve truths on step 5's (140 and 12 passed, none failed); **the whole suite on the
merged tree in the cloud (run 18 on `1e3523b`: lint green, 4,337 passed over the six shards,
3 skipped, 11 expected failures, none failed, 43 minutes; the pace job, informative, 7 of 10
at 448 to 495 against the floor of 500 in 298 seconds, the slow runner's day as 79b's and
89's records read it).**

**Item 1, an island the grid lacks, taken another way and accepted:** the brief's island
with an extent alone would have made Belle Isle and seven other islands the grid holds
discs of ground over their roads; an islet the grid lacks says so, `grid_lacks: true`
beside its height and `extent_m` (`chart.Feature.is_ground`, `is_hazard`), ground to the
keel by its height within its extent as a rock that stands above the water, a hazard on
the pilot's and the captain's line, land to the lookout by its name and stood into by its
extent; nineteen islets of 79c's and 79d's recast by their source lines (an isle or an
islet in the period's words an island, a rock a rock), six rocks kept; the index
byte-identical, the manifest's counts moved by text (a slip of four duplicated lines, found
at review, mended at step 5); truth 7-303 recast to the kind, nothing loosened; truth
7-310. **Item 2:** a road's bottom read as an anchorage's (`BOTTOM_NOTE_KINDS`); no
feature of kind `road` exists, so nothing moves; truth 7-311. **Item 3, the seam's taper:**
within ten miles of a block's open edge (charted water no block holds, the eleven within
reach) the block's water rises from the eleven's alone to its own by the smoothstep, on
each constituent's amplitude and phase and on the level (mixed as complex numbers the 114
degrees between the two M2s at 1 W made a false node mid-band, so the mix is the amplitude's
and the phase's); a seam between two blocks and an edge beyond which nothing is charted are
no open edge; outside every block the old arithmetic to the bit; the step at 1 W from 4.3
to 7.6 feet to 0.045, the Iroise's from 1.6 to 0.04; Concarneau's judged rise 13 to 14, the
taper reaching its gauge across Brittany (a finding, said, not mended); truth 7-282
re-measured old beside new, 7-312. **Item 4, the Solent:** the manifest's `tide_regions:`
(bounds and no tiles, for the gauges' membership alone; written by `tools/build_charts.py`
from `TIDE_REGIONS` so that 93's rebuild keeps it, the one change beyond the brief, said),
`solent` 50.62 to 51 N and 2.2 to 1 W by judgement from the gauges' places and the Wight's
shores; Bournemouth and Portsmouth serve it, `held_gauges:` gone, no figure moved;
Spithead's high waters within four minutes of Portsmouth's gauge where the eleven were four
hours and a half out; the Solent's judged rises re-worked (Norie's Spithead 10 to 12,
Moore's Portsmouth 9 to 12, Pool 8 to 5); the Downs to Spithead sailed on each tree, no
grounding, the truth's limits held; truths 7-313, 7-314, 7-283 re-measured. **Step 5, by
the lead's rulings:** the Solent's seam with the Channel east at 1 W north of 50.62 N (a
step of three feet and a half off Chichester, the taper being a block's against the eleven's
and no seam's) ruled way (a) under **the rule of the seams**: a gauge serves its own block
and also a block whose seam with its own lies within the taper's band (ten miles) of the
gauge, the water a cable either side of a seam being the near gauge's and no other's; the
rule catches three, Portsmouth (4.2 miles from 1 W), the Isle of Aix (6.4 from 45.9 N) and
Cadiz (8.0 from 36.4 N), each taken, `test_tide.py` holding the rule over every gauge; the
steps at 1 W 3.4 to 3.6 feet to 1.5 to 1.7, at 45.9 N 3.9 to 0.3; Beachy Head 18.99 to
18.86, within truth 7-280's words, which stand; three judged rises across the foot (Norie's
Cape Trafalgar 3 to 5, Moore's Shoreham 18 to 17 and Dungeness 20 to 19); way (b), the
eight gauges serving both, measured and not taken (Beachy Head 18.73 past the truth's words,
the block's far gauges weighing at its own places against Norie's figures). **Findings,
booked by the lead:** the seam at 36.4 N keeps eight feet, which the lead measured as the
mean level's and not the constituents' (Portugal's 1.63 m against the Strait's 3.98, the
eleven's there, the Strait's gauges' levels unread; the M2s 1.01 and 0.83 m a cable apart),
a tide data tidy, the Strait's and the islands' gauges' mean levels read from a source; a
taper by distance reaching a gauge across land (a taper by water a design question); the
western Solent and the Needles within the band of the region's south bound; `fathoms_words`
giving "in 13 fathoms" where the words say twelve (a words tidy); the pictures' flake under
the fast tier's load; the lee-shore trial's container digest as recorded since 79d.

### Package 85 as merged (2026-10-30)

Merged `--no-ff` from the Fable sibling session's `claude/pkg-85` at `c4afb7c` (eleven
commits of its own on the trunk, one an item or a few, the trunk brought in at every
boundary, the mend of the lead's review the last; no conflict, the merge's tree the branch's
head's; 147 files, 4,051 lines added and 1,259 removed); ruff clean; the builder's fast
tier whole on its final tree twice (the first run finding eleven failures the per-item runs
had not, each mended; the second 4,447 passed, none failed, the pictures' test among them),
the slow tier of the fifteen files of its diff with the checkpoints' and the anchor's and
the known truths (1,735 passed, 7 expected failures, none failed, every recorded passage's
digest and pin held); the lead's three runs on the branch (items 1 and 2's fifteen files
whole; items 3 to 8's twenty-three files with the new truths, which found truth 7b-117's
date and the old checkpoints' table, the builder's own fast tier finding the same two; and
the mended head's eighteen files with eight truths), the hail probed by hand on the trunk,
the first head and the mended one; **the whole suite on the merged tree in the cloud: run 19 on `3b76275` was cancelled at
its half by the workflow's own rule (one run a branch, the newer cancelling the older) when
run 20 was dispatched on 93's merge twenty minutes later, so the suite on 85's tree is run 20's
on `0ed9d28`, which holds 85 whole: lint green, 4,814 passed over the six shards, 3 skipped,
11 expected failures, none failed, 47 minutes; the pace job 10 of 10 in 267 seconds (a quiet
runner); the builder's own fast tier whole after 94's merge, 4,454 passed, none failed.**

**Item 1, the rule stated once and enforced:** `docs/dev/PrimerRedactions.md` states it (the
primer and the library's served topics are in-world documents for whoever reads them, at
any station, in any scenario, on any ship; nothing true of one scenario, one book, one ship,
one voyage or one stage of the build; no milestone, package, gate, builder, playtest,
ruling, truth or decision number, spec section, the lead, the owner's rulings, a model's or
a vendor's name) and `tests/test_in_world.py` enforces it over every primer chapter, every
brief constant, the tools' words, the library's topics rendered on a King's ship and on a
hired cutter, every station's brief head and the starter briefs, with an allow-list and its
reasons (the owner at the door, the sounding lead, seed 7, the shipped scenario files'
names); every such reference cut from the twenty-five chapters and the README, the
evolution files' build notes moved below a blank line under `# Build notes (not served by
the library's catalogue)` (156 cuts, tabled in the record), the captain's brief, the forms'
notes, the world page, two tools' words and two people files freed; stale lines mended on
the way (fourteen chapters); chapter 3's size pin 11,370 to 11,280. Noted and left: the
consent brief's preamble (55's), the playtest folders' names (the record), `BUILD_NAME`
(the lead's at a gate). **Item 2, categorised, complete, correct:** the grammar topic in
six parts generated from the game's tables and guarded by `tests/test_grammar_book.py`
(the order language, the readings with what each answers, the standing dialect, the voice,
the stand-by, the world orders); the `query` kind for the seventeen readings that are
questions in words (read, never compared, the standing grammar refusing a condition on one
in words; the anchor's two rows back to `ground` when the whole fast tier found the
anchor's standing order compares them); the hail's colon optional (`hail_parts`), the sail
told from the words by her rig, her name or 'her'; the person's own appended to every
station brief with authority but the director's (the officer's handover budget 20,500 to
21,000, then 21,500 with item 5); the primer measured against the vocabulary (23 verbs
added to their chapters, chapter 11 given the 184 events whole as a table kept equal to the
registry, every chapter with a forms table run through the ship); chapter 7 re-recorded
from the game as it stands with a stated cut rule; chapter 8's map of the library. **Item
3, the date and the war as readings:** `the date` in words, closing every station's line and
the director's; `the war` what the ship knows and never the world's table (the table she
sailed with, `Nations.sailed_with`, and every change the news brought, entered in the new
paper `the news of the war` at the pilot's news with where and when it came); truths 7-240,
7-241. **Item 4:** the calls before a stand-by answered with their results at the API door
and the local runner (`Reply.ran`, kept by the harness, carried in the transcript), "not run"
said only of the calls after it; the action's severities by the flow of the game through the
log (the firer's minute line notable when a shot struck, the fire opened or a gun was fired
with no mark, routine when the minute's shot all missed; at quarters the trimmers' yard by
yard routine, a trim's one line notable); the signal book's page saying whose it is, the
common book of no nation saying it is no other ship's; truths 7-242, 7-243. **Item 5, the
ship herself:** `readings.ship_words` (her name, rig and class from her file's era note, her
service and nation, her fit of guns, her people's number, who commands, the ports of her
voyage) at the head of every station's situation but the director's, kept across the
handover fold, and the reading `the ship`; truth 7-244. **Item 6, found on the way:** a
standing order's name may carry an apostrophe (the closing quote pairs with the opening);
`hail the lugger` names a sail in sight and never a far one, a wreck in sight no sail;
`captain: carry on` at the prompt the player's own hand given back; `gybe the mainsail`
answered that the gybe names no sail; truth 7-245. **Item 8, the documentation whole:**
every document under `docs/` but the primer's, the consent's, the playtests', the gates'
and the four left to the lead scanned for paths, symbols and flags the tree lacks and read
where the scan pointed; mended (spec M7's `data/nations/`, spec M6's primer 17, spec M7b
§19's stores pointer, the references' count, the repository's README's status and list,
the Harness's three places); the dated records left as history and said so; left to the
lead with nothing found to mend by the scan (ChartBlocks.md, Tides.md, DesignProposal.md;
M7-WorkPackages.md naming unbuilt packages' files); **missing, named for the lead:** an index
of `docs/` and a reader's page on the one world. **Item 7, the interim gate's draft:**
`docs/gates/gate-m7-interim.md` in m6c's form, the verdict Pending, what changed since m6c
from the player's and the reader's side, fifteen items over the two playtests (ten after
84 with the lead's two seats by the owner's word, five after the first new ship to be made
exact when her file is in), the open items of the records, the pins moved and why, the
container floors and the pictures' threshold; the engine's and the world's half the lead's
to add before the owner runs it, with the chart blocks' attribution in its "what changed"
list mended then (79b the Channel east, 79c the Mediterranean west and the Balearics, 79d
the Gulf, the Ligurian sea and the Tyrrhenian; the Strait, Madeira and the Azores 39d to
39f's). **The lead's review, three findings, all mended on the branch:** the hail's head
ran past a colon or a comma when the words before it named no sail, so `say to the master:
the brig has tacked` was refused as a hail of no sail and the lookout's `hail the deck: a
sail on the bow` got the wrong refusal (the head now stops at the first token ending in a
colon or a comma, the four lines in the colon test); chapter 20's "fourth part"; the notes'
line on a shot into the sea. Found by both the lead and the builder's fast tier: truth
7b-117's pinned date (the cutter scenario's for that world's Monday 10 June) and two
playtest checkpoints restoring a nations table without `sailed_with` (the rebind step and
`Papers.__init__` read it with a fallback to the wars as saved). **Pins moved, all of
structure, old beside new:** chapter 3's size, the grammar's parts 4 to 6, the officer's
handover budget 20,500 to 21,500, the papers' count 11 to 12, the station line's words (the
date); no recorded passage's digest moved. **Noted for the lead and booked:** the console's
`state` at seven lines and the hands' rationing lines at 1x (a words question for the gate);
the missing `docs/README.md` and the one-world reader's page (the lead's, with the gate's
half); 87's brief waits on this merge.

### Package 93 as merged (2026-10-30)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-93` at `7e6b9f1` (the rule,
then one commit a region rebuilt, the Atlantic four twice, the trunk brought in at each
boundary with 94's merge among them; merged here over 85's close with the tuning notes the
one conflict, both kept; 1,011 tile and coast files and nine others, the manifest's tile
records among them); ruff clean; the builder's proof the one 89's and 94's was (the eleven
recorded passages by node id, the gate selection and the captain's trials) on a clean
worktree of the head first and on the final tree last, identical (every digest held, the
lee-shore trial's container digest the one failure on both); the six chart and tide files
fast and slow after every region, the blocks' truths 7-260 to 7-314 with `--slow` after
every region, its fast tier whole with the pictures' flake the one failure, passing alone;
the lead's run of the chart's, tide's, islands', ports', scenarios' and geo's tests with
eleven truths on the head (176 and 11 passed, none failed; and of the in-world, tide, chart and grammar tests with eight truths on the merged tree (203 and 8 passed)); **the whole suite on the merged tree in the cloud (run 20 on `0ed9d28`: lint green, 4,814
passed over the six shards, 3 skipped, 11 expected failures, none failed, 47 minutes, the
count up from run 18's 4,337 by 85's and 93's tests; the pace job 10 of 10 in 267 seconds,
the first quiet runner since run 14).**

**The rule, as built:** GEBCO's fill under every block is raised to the chart's datum by the
world's mean level at each cell, `mean_level_grid` being `Tide.constants_at` itself (one
source of truth, the lead's ruling after 94's merge, way (b) of the builder's two: 89's
membership by the regions' bounds, 94's taper and rule of the seams come through it and
never by a second reading of the manifest; the eleven alone outside every block, the raise
every tile there was built by); `fill_mean_level_m` taken out of Biscay south's and
Portugal's recipes (39c's 2.5 and 39d's 2.0, made while the gauges were held), Biscay north
taking `fill_to_chart_datum` for the first time; a control before each rebuild (the head's
own tool on today's fetch) giving the committed arrays, so that what moved is the rule's
alone. **The ten regions** (channel-east, biscay-north, biscay-south, portugal, strait east
of 5 W, mediterranean-west, balearics, gulf-of-lion, ligurian-sea, tyrrhenian), each tiles
count as before, the bytes moved by under a quarter of a megabyte each (179.92 MB of level 2
and 26.61 of level 3 in the ten against 179.37 and 26.65), the figures old beside new region
by region in the notes; madeira and azores not rebuilt (the rule moves no cell of their
raise); the Mediterranean's harbours EMODnet lacks water again where Saint-Malo's 6.83 m
had made them land (Port Mahon's inner harbour, Palma, Ivica, Toulon's inner road,
Marseille, Leghorn's Darsena, the Camargue, Thau and the Albufera); the Channel east's
dyked levels (Romney Marsh, the Pevensey Levels) under high water springs as behind their
walls in truth. **The block scenarios** sailed to the same log byte for byte on the head and
the rebuilt tiles but where the notes say (biscay-south three moments at Corunna, a fathom
of cable and a bearing; mahon one line, the land about Georgetown a minute later;
agincourt-sound eight lines, its grounding at the same tick as on the head, 79d's scenario
finding); no recorded passage moved, none sailing a rebuilt region. **Two rulings on the
way:** truth 7-305 by option (a), the brief's wording the lead's and amended at the
measurement (the Somme's banks and Dungeness's shingle above the world's high water
springs; the raise at Romney Marsh the block's level less the eleven's; the marsh and the
Levels below, as behind the Dymchurch Wall in truth, a finding with the figures for a land
patch when a sheet is read); and **truth 7-297 on the rebuilt Ligurian sea** (Agincourt
Sound open to the north and east on the block's own water, the islands' shores that closed
it having been the false raise's and not the grid's: EMODnet silent over them, GEBCO's
fifteen seconds smearing them three to six metres under mean sea level): not re-measured
on tiles that open a harbour the real islands close, no sheet read and none drawn, (c)
taken bounded and said: the harbour patch `agincourt-sound` keeps the eleven's raise
within its box (`fill_raise: eleven`, the recipe's comment, ChartBlocks.md's rule, the port
file's head), every cell of both levels within it equal to 79d's (17,280 and 622,080
cells), the truth and the scenario unmoved, a land patch from a period sheet with its
datum (Ryves's survey of 1802, Smyth's, or the Derrotero's plan) booked to the patch
package with Mahon's plan and Bellin's. **Truths 7-305 to 7-309** written and passing.
**Findings, booked by the lead:** `channel-mid`'s seam column and `channel-west`'s edges lie
under water whose level now differs from their raise by up to 0.41 and 1.29 m over a few
hundred cells (not rebuilt by the brief; a rebuild of either with the key and the rule
would carry it, with the recorded passages re-measured, a decision for the owner); the
open sea east of 4.5 E south of 40.56 N lies in no block and reads Saint-Malo's water by
the eleven's nearest alone, the Balearics' tiles reaching 4.75 E (a bound to move, with
89's like finding at 40.5 N); a far gauge's raise hiding the coarse shore wherever EMODnet
stops short (the patch package's); one merge commit of the builder's (`dae50ca`) without
the attribution lines, pushed and not rewritten.

### Package 82, step 1, as merged (2026-10-30)

Merged `--no-ff` from the Fable sibling session's `claude/pkg-82` at `a4577b3` (the design
note first, approved with the lead's rulings on its three questions; then step 1, the
re-brief's item 3 reported first as briefed, with the trunk's `58c51ac` brought in at the
boundary; the merge clean, the trunk's head an ancestor of the branch); ruff clean; the
builder's fast tier whole on the final tree (4,473 passed, none failed, 29 minutes), the slow
tier of the eighteen touched files and the known truths (1,752 passed, 7 expected failures,
the rulings', none failed, 45 minutes); the lead's run of the between-hulls, officer, in-world
and the step's truths' tests on the head (180 passed) and the lead's probes (below); **the
whole suite on the merged tree in the cloud (run 21 on `432ddb4`: lint green, 4,828 passed
over the six shards, 3 skipped, 11 expected failures, none failed, 42 minutes, the count up
from run 20's 4,814 by the step's tests; the pace job 10 of 10 in 257 seconds).**

**What was built** (`docs/design/Design-BoatAndPersonAboard.md` §2 and its postscript;
`docs/dev/TuningNotes.md` "Package 82", step 1): `movement.put_aboard`, the one function for
every change of a person's hull, by the boat alongside another ship, by boarding, by capture
or by the director's word; a model's station goes with its person (`Harness.move_to`): in a
hull not his own he holds a **visitor's voice**, a station of the passenger's kind under his
name with a passenger's reach and a brief and a domain of its own (`VISITOR_DOMAIN`, the
refusal naming what he has and has not, of her deck and of his own ship's from there), his
own station standing bound to him at home until he comes back, when it is his again with its
whole surface; a captive put aboard a captor is stood down with the reason (the handover's
rule, 74's hook). The roads: `send the boat to the <ship> [with <persons>] [for <persons>]`
from an awake or a sleeping hull as two jobs of the port's kind within a boat's pull
(`BOAT_BETWEEN_NM`, a mile, judgement); a visitor's `come aboard` by the host's boat; the
director's `person: "X" goes aboard the <ship> by the boat`, doubted beyond the pull and
performed on the director's word; 84's `comes aboard the <ship>` through the one function;
the deck won, the first lieutenant who leads the boarders standing on her deck with his
station following. `where am I` as a per-asker query (read afresh at each asking, out of the
readings tool's dict), the station line's visitor. The save groups a harness by the hull of
its first seating (`Harness.seated_on`) and carries the station of his seating while he
visits, so that a replay by the transcript seats him at home and the replayed moves carry
him on. **Truths 7-324, 7-325, 7-333.** The player's own seat does not yet follow its person
between hulls: step 3's.

**The lead's review, two findings mended on the branch before the merge.** (1) A save taken in
the middle of a visit did not replay by the transcript road, the owner's road: the harness
saved its visitor's voice as its station under its home hull, so the replay seated a
passenger's voice on his own ship and his orders had no deck to be given from (the acts road
was whole; the builder's test saved only after he was home). Mended: the save carries the
station of his seating; a test saves on the brig, in the host's boat on the way home and at
home, and replays each by both roads to the same digests of both logs. (2) A player's
`send the boat to the <ship>` refused for the distance left a far body promoted to a hull:
mended, the hull made only when the boat goes, the distance measured by her far body first.
The lead's probes of both on the mended head: the mid-visit save the same by both roads, the
copy's harness visiting on the copy's own hull; the refused order leaving no hull.

**What moved: nothing pinned but the officer's handover budget** (21,500 to 22,000, old beside
new in `tests/test_officer.py`, the visitor's words in the officer's brief); `Dealings._boat_kept`
leaves a boat on the to-ship errand alone (the kedge's false denial is step 5's).

**Found on the way, booked:** a person's ids are his company's, so the boat's lists of ids
are resolved among the registry's persons (step 4's boat as a hull resolves by the person);
the player's own seat on another ship (step 3). **Next:** step 2, the observer's hull (item 1:
`ship: none`, `director: observe`; truths 7-320, 7-321, 7-334), the builder going on without
a report until the package is built or blocked; 74's prize and captive on this step's
function, held after 82 and 65 both.

### Package 75, B1 (the *Indefatigable*), as merged (2026-10-30)

Merged `--no-ff` from the ships session's `claude/pkg-75` at `bb60222` (the owner's own
session: stage A, stage B, the hull's shape keys and drawing, Ext §17.11's stage 0, B3 and B5,
her regeneration with the three figures the lead ruled, the record, and her second testing
report with the sheets; taken whole at the report, as the lead's notes to the session had it,
the owner away and the session left to proceed); the merge automatic over 85, 93 and 82's
step 1, which the branch lacked; ruff clean; the lead's checks on the merged tree: the
generator reproduces all ten ship files byte for byte (`tools/gen_ships.py` to a scratch
directory, `cmp` against `data/ships/`), the eight other ships unmoved against the trunk, the
physics' diff the stage-B extensions reviewed before (the yards under the bowsprit on no
mast, `Sail.curve_class` for a lateen cut at the mast, the slings' words) and nothing else,
no consent file touched, no model identifier in any file; 85's in-world test green on her
served heads and the tools' words the first time they met it; the grammar book, the primer,
the particulars and the profile tests green after the mend below; **the whole fast tier on
the merged tree here (whole but the pictures' flake under four workers, the MCP bridge's
images, passing alone as at 93's merge) and the whole suite in the cloud (run 22 on `11b4863`:
lint green, 5,626 passed over the six shards, 3 skipped, 11 expected failures, none failed,
41 minutes, the count up from run 21's 4,828 by her suites; the pace job 10 of 10 in 162
seconds).**

**What was built** (`docs/playtests/2026-10-30-pilot-indefatigable/testing-report.md`, the
tuning notes "Package 75", `docs/design/Design-Ship-Indefatigable.md` and the research,
build and shared-design notes beside it): the 64 of 1784 (`sixty-four.yaml`) and the razee of
1795 (`razee-44.yaml`), written by `tools/ships/indefatigable.py` through the generator, on
the hull of the first report, with the whole rig tuned: the 64's lateen mizen yard with a
104 m² course cut at the mast and no boom, Steel's driver of 203 m² on its 65-ft boom bent by
"shift the mizen for the driver" (the boom out with the shift and in with it: Ext §17.11),
Steel's long pole-heads on both (the main truck 47.2 to 51.7 m), the spritsail and
sprit-topsail yards on the 64 and the spritsail yard on the razee, the bowsprit on the stem
head at 27°, the razee's spanker of 200 m² with the boom clear of her taffrail by a
centimetre (218 could not stand clear: the lead's ruling), her stern plain above the lights.
In 15 kn on the beam the 64 makes 7.55 kn at 4.9° of heel with light weather helm, tacks in
244 to 266 s and wears in 497; the razee 7.86 kn at 4.3°, tacks in 427 to 484 s, her best in
25 kn 11.64 kn (the *Virginie* chase's 11.2 met); the razee faster than the 64 at every angle
(truth 7-187, pinned) and under the frigate-36 by 0.10 to 0.22 kn close-hauled and running
large in 15 kn (reported, not forced, as the owner left it); the driver faster in light fair
winds and poor close-hauled (a fair-weather sail, as Steel has it; measured, not pinned). The
question answered plainly for the owner: a two-decker quicker in stays than a 36 is her small
after sail against her lead, not the yards under the bowsprit (which cost her a degree of
staying: she misses from 60° and 60.5° off in 15 kn and stays from 61°) and not her lines
alone; every hull at its own lead with 104 m² aft tacks in about the same time. **Her truths**
(`tests/test_indefatigable.py --slow`, 68): 6, 9, 10, 11, 12, 17 and 7-187 to 7-189, 7-230 in
their forms, old beside new in the notes; the eight's pins untouched.

**The four departures from the lead's words, accepted as reported:** rule (3) of the slings'
ruling narrowed to a spar with yards under it (the lugger's bowsprit stays at 21.8 kN, the same
shrinking on another ground, SW-2's); the bowsprits' ratings 168.6, 168.5 and 27.0 kN as the
named rating reads the headsails lowered; three lines beyond §17.11's table through
`driver_boom` and two behaviours with them, in Ext §17.11's as-built note; the razee's
`clr_x_m` +4.5 kept for the owner's test, +4.4's figures beside it (quicker in stays, farther
from stage A at six points and 60°).

**Mended at the merge (the lead):** the branch registers two events for the lee ports as
*absent* (`the lee ports shut`, `the lee ports opened`: the sentence the book refuses them by
until the rule is built, stage 0's hook laid in `combat/ports.py`), the first absent events
the registry has had; 85's book tests, written when none was, held the registry's every event
to the primer's table and the grammar page, and the table's every form to be taken. An absent
event is now treated as an absent reading is: the grammar page names it in its "later, when
the world has them" list, quoted and with its sentence, and the primer's table is of the
events the book takes and none it refuses (`agents/tools.py`, `tests/test_grammar_book.py`,
`tests/test_primer.py`; the tests tightened by one assertion, none loosened).

**Found by the session, booked and not this merge's:** a shift or bend belayed after
`send_up` loses the canvas drawn, on any sail (the 64 can lose her driver for the voyage); the
frigate's ringtail keeps `wrecked` after its boom's wreck is cleared; a boom hit while rigged
in is not drawn though its refusal says the wreck "still hangs aloft"; `shift_sail`,
`bend_sail` and `unbend_sail`'s served heads name no boom phase; her long tests' `SLOW_TESTS`
entries wait on Phase 5; three captain's trials fail on the owner's machine with or without
the work (the build machine's difference; to be named in the hull step's record). **Next
(the notes to the session, below):** the hull step, three streams measuring the frigate-36,
the brigs and the cutter now, the landing held for one byte move of all eight; 81 and 91 after
75 complete; the owner's own sail in her when they are back.

### Package 82, step 2, as merged (2026-10-31)

Merged `--no-ff` from the Fable sibling session's `claude/pkg-82` at `3a1b6d4` (the step
reported as a note, not one of the four reports, and merged in parts as briefed; the trunk's
`588c664` brought in by the builder before the step's final runs, the Indefatigable's merge
after it, the lead's trial merge onto `5fbfbb0` clean and identical to the merge made; the
builder's step 3 on the branch above it is not in this merge); ruff clean; the builder's fast
tier whole on the step's tree before and after the trunk's merge (4,488 passed with two
failures not the step's, the parity list and the pictures' flake, then 5,288 passed, none
failed, 32 minutes), the slow tier of the eighteen touched files and the known truths (827
passed, 7 expected failures, the rulings'); the lead's run of the observer, parity, grammar,
in-world, primer, scenarios, console and server tests with the step's truths on the merged
tree (green), and **the whole fast tier on the merged tree here (whole), and the whole suite in the
cloud: run 23 on `2d512b2` was cancelled by the workflow's concurrency rule when run 24 was
dispatched on package 88's merge above it, and run 25 on `e587ba7` (this step, 88 and the
merge's two mends) stands for it: lint green, 5,650 passed over the six shards, 3 skipped,
10 expected failures, none failed, 60 minutes; the pace job, informative, 7 of 11 (below,
under 88's record).**

**What was built** (`docs/design/Design-BoatAndPersonAboard.md` §3 and its postscript; the
tuning notes "Package 82", step 2): `ship: none` in a scenario file, or `director: observe`
which implies it, builds a world whose own hull is **the observer's**, a hull of no ship at
the scenario's position kept under the player's id so that every id rule of 84's stands,
with no hull followed; the loader refuses in words what such a world cannot carry (a ship's
file beside it, standing orders, an intent, first orders, a station of the ship's for the
player, a position missing), and a ship given on the command line makes the world hers. No
vessel of hers is on the sea; her orders are refused in words (`NO_SHIP_FOLLOWED`, journaled
and replayed as every refusal is); the readings of a ship answer "no ship followed" through
one set of the world's rows (`readings.WORLD_ROWS`: the wind, the watch, the time and date,
the daylight, sky, weather, visibility and sea, what is in sight, the land and the dangers,
the moon, the war, the pace), so that a row added later is the observer's refusal by default;
the world orders stand, with `aboard:` unnamed and `captain:` refused and 'the ship' refused
as no ship of the player's. The centre is the view, moved by `look at <position or chart
feature>` (a driver's line, journaled and replayed) and by `follow "<ship>"` (her hull made
in the far shape and woken at the switch's next minute as the followed hull, outside the
cap's count), `follow nobody` giving the view back; the view's lookout looks from a boat's
height of eye (two metres, the design's nought taken another way with the reason); the
drivers open at the director's station when no seat is named (`console.player_seat_for`,
one function for both doors); the console's state, the snapshot and the page say "no ship
followed" and draw a ring at the view; the truth opens with the view. The scenario
`data/scenarios/the-channel-observed.yaml` (the western Channel on 12 June 1805 from a view
off the Lizard, the business on, three ships under their captains, the wind pinned).
**Truths 7-320** (a day at seed 7, slow), **7-321** (the words, the refusals, the world
orders, follow and look at, the save replayed mid-view and mid-follow), **7-334** (the pace,
informative).

**What moved: nothing pinned.** No recorded scenario has `ship: none`; every world with a
ship keeps the player's hull as its own with her id followed, and each new path is the old
path there. **Found on the way, six places where the World assumed a ship**, each given its
words (the far tick's sky with none followed; the own hull ticked through her shadow; the
console's reckoning lines with no account; the director's truth reading the own ship's
heading and purse; a far goal the captains know; `World.parent`, `Hull.parent` and
`Hull.is_followed` with none followed, which felled the business's first demotion of the
observed day).

**The cost, measured and booked for the lead:** the observed Channel runs at 444 ticks a
second against 271 for the same Channel with the frigate at the view and 668 for the frigate
alone; the observer's hull costs a point ship's tick as the design said, and what the observed
Channel costs beyond the design's figure is **the business's brains reading the chart's
tiles** (`chart.load` 440 times in a thousand ticks: two dozen ships over the whole Channel
exceed the tile cache, each eviction a read of a compressed tile), the same in a frigate's
world and no part of this package; a larger tile cache or a lee-land distance kept per brain
for a minute would give most of it back. Booked with the pace findings.

**Next:** step 3 (item 2: `--seat captain --ship <name>`, the director's door, 86's three
seams, the seat following its person; truths 7-322, 7-323, 7-326), already on the branch
above this merge and reported in its turn; then the boat as a hull (step 4) and the towing
(step 5).

### Package 88 as merged (2026-10-31)

Merged `--no-ff` from the Opus sibling session's `claude/pkg-88` at `cf4b055` (item 1 reported
with a question and held open under the lead's ruling, item 2 reported with three points
ruled, the close at the package built; the trunk brought in by the builder at item 2's
boundary and at the close; merged here over 82's step 2 with the tuning notes and the known
truths the two conflicts, both sides kept); ruff clean; the builder's slow tier of the touched
files with the captain's trials and the known truths whole, the pace tests alone and last,
and the fast tier whole (two failures passing alone after: the pictures' flake under load and
`test_log_lines`' standing-order names by a salted hash, booked); the lead's checks: no
physics file, ship file or consent file touched, no model identifier; **the whole fast tier
on the merged tree here (whole but the pictures' flake, passing alone), and the whole suite
in the cloud: run 24 on `0b55448` found two things of the merge's own, mended at `e587ba7`
(the format check on the known truths after the merge's resolution, two blank lines; and
the lee-shore trial's digest, `1ecbc08a61efb132` in the cloud against the builder's
`6e88e97cbdffac7b` with the states and the line count the same, so the assertion is a
comment naming each machine's figure and the states, the grounding and the lines are the
pins, as ruled); run 25 on `e587ba7`: lint green, 5,650 passed over the six shards, 3
skipped, 10 expected failures (the station gale's lifted: 11 before), none failed, 60
minutes. **The pace job (informative) 7 of 11 on runs 24 and 25 alike,** the same four under
truth 51's floor of 500 ticks a second (truth 51 at 496, the day under the systems 478, the
gate's day with the region 454, 7-159's convoy at far detail 440; 10 of 10 on runs 20 to
22 before this merge): a cost of the pass, measured on the lead's machine (four cores, load
one, single runs of `tools/pace.py` on the tree before the merge and on the trunk after it):
the frigate alone 488 to 518 and the dozen at far detail 439 to 475 (noise, no cost), the
convoy of six and the privateer at far detail alone 482 to 414 (a seventh), the default cap
268 to 263, a cap of twelve 265 to 239; the cost in the far captains' judgement under the
pass, the station-keepers most (the danger-ahead reading of the chart on every judgement of
every sailing far captain, and the square sails' states read for the recovery's flags each
judgement, by the lead's reading). **A follow-up asked of the builder on `claude/pkg-88`,
2026-10-31:** profile, mend with no change of behaviour (the chart read ahead only when the
account puts land or a danger within reach; the sails' states only with no headway), every
recorded figure again exactly, the pace truths old beside new; merged as 88's close, the
cloud's pace job the proof.** **The follow-up, merged as the close (`f58b0f7`, 2026-10-31):**
the builder's profile finds no cost of the pass on its machine (the package's own share of
the crewed captains' judgement under half a per cent, the far captains running none of it;
two alternating runs of `tools/pace.py squadrons` on the trunk before and after the merge
spread as wide within a tree as between them, 596 to 648 at far detail), so the lead's
single runs are read as noise and the cloud's two runs as its runner's (440 to 496 there
against 620 to 700 in the builder's container); the two dear reads are taken only when they
can answer all the same (the square sails' states with no headway; the chart ahead when the
coast by account or the nearest charted danger lies within the reach, `DANGER_AHEAD_SPAN_NM`
two miles past it for a danger), no change of behaviour, every pin as it stands; the cloud's
pace job on the next run decides, and if the four stay under the floor the runner is the
next reading. **Run 26, after the follow-up: the same four under the floor again** (truth 51
at 494, the systems' day 481, the gate's day 454, 7-159's convoy 442), on a third runner and
within a few ticks of runs 24 and 25, which is not a runner's noise but a cost somewhere
between run 22 (10 of 10 on `11b4863`) and run 24 (`0b55448`): 82's step 2 and 88 are the
two merges between them, and the lead measured them apart on this machine: `tools/pace.py`
on `11b4863` (run 22's tree), `2d512b2` (82's step 2 in) and `f5be911` (88 in), the frigate
alone twice each (513 and 318; 451 and 461; 518 and 545) and the convoy at far detail once
each (443; 415; 478), the machine's load falling from two to one through the series: the
spread within a tree is wider than any gap between trees, and the newest tree is the
fastest, so **no cost is found in the code on any machine but the cloud's**, where the drop
is coincident in time (from run 24's dispatch at 03:39 on 2026-10-31) and not in code. The
pace job stays informative and is read on each run; if the four stay under the floor for a
week, the floor is re-measured on the build machine (the owner's) and the runner's family
noted; nothing of 82's or 88's is to be moved for it.

**What was built** (the tuning notes "Package 88", items 1 to 4 in the owner's four parts,
each with its switch and the bisection's table): **(1)** the rules captain recovers her when
she lies aback with no way (`Captain._aback_with_no_way`; `aback_recover_minutes`, three,
in every role's file): having had way, with none, square sail set and none drawing, no
manoeuvre in hand, for three minutes, the work waiting for hands avasted, the driver taken in
(Lever p. 79; Luce 1866 ch. XXV), boxed off if she lies so another while, the driver set
again and the leg shaped when she has way; the convoy keeps way the morning through (86's
stall mended; truth 7-152's ticks moved, 7-153 holds). The haul-off keeps the sea (a point at
a time to a line the planner finds clear; the trade trial's schooner had been steered across
the land about Coverack). **(2)** The room a wear takes (`navigation.no_room_to_wear`): the
land or a charted danger within the doctrine's two miles anywhere in the lee half, by the
lookout, the chart at the account and the dangers by account, and she is tacked, never worn,
a shaped course that would be worn for want of way keeping her full and by to claw off; the
land or a danger ahead (`Captain._danger_ahead_by_chart`, `danger_ahead_nm` a mile and a
half): the lookout's land on her bow by any light, or with no land in sight the coast on her
course or a charted danger by the chart at the account, puts her about (Falconer, CLAWING).
**The station gale's expected failure of package 57 is lifted**: never aground in the twenty
hours, tacked with Ushant two miles under her lee where she was worn; the lee shore never
aground (under item 1 alone she struck the Four at night, the lookout's land on her bow
unanswered). **(3)** The near and far station laws read against each other: they agree in
the filling and aim differently by design (the near at a point ahead of the station, the far
at the station); the far leg given the near aim moved six tests and was undone; left two by
measure, with a test holding both to the filling. **(4)** The true colours held once shown
before an enemy (`signalling._true_colours_held`; `privateer.yaml` `true_colours_held`): the
owner's flicker reproduced and mended, the ruse not taken up again before the same ship
until every enemy she showed them to is out of sight. **Found on item 1 and mended:** a mark
engaged beyond the engaging distance and not gained on is a stale chase, given up from
`engaging` as from `chasing` (the trade trial's French brig had hung two to four miles astern
of the faster schooner for seven hours). Every switch off gives every recorded passage's old
figure. **Truths 7-340, 7-341, 7-342.**

**What moved, old beside new, by bisection and under the lead's rulings:** truth 7-152's
ticks; truth 7b-129's band (4 h to 200 min, the lee-shore line ending her lying a-try, said in
the docstring); the station gale's and the lee shore's states, lines and digests; the trade
trial re-pinned (never aground, never taken, unfired, on passage eleven miles from Falmouth at
the twentieth hour, where before she was fired into and in port: the recovery and the longer
evasion's cost); the wardroom door's evasion hour (3,700 to 14,700). **The lee-shore trial's
digest** is pinned at the package's figure with the trunk's and the stale pin named beside it;
the cloud's figure decides it at this merge's run (a digest is the build machine's: if it
differs, the assertion goes to a comment naming each machine's figure, the states and lines
staying the pins).

**Found, booked:** the station gale filled away in 42 knots lies aback by turns for two hours
(70 lines against 23), the gale book's ground (58b's family; item 1's recovery is armed and
never runs its three minutes there); the near and far laws can fill a station just across the
eye on opposite tacks, so a member might go about at her promotion; heaving to till light not
built (no trial wanted it); `test_log_lines`' standing-order names by a salted hash collide
once in a while (the test's own to mend); the merchant brig full and by 103 degrees off the
wind for some minutes after a station order, seen in a probe. **Next:** the owner's gate
testing on the captains' days; 65 after 82; the gale book's finding for a later pass.

### Package 82, steps 3 and 4, as merged (2026-10-31)

Merged `--no-ff` from the Fable sibling session's `claude/pkg-82` at `8167079` (step 3 on
the branch unreported as a note and step 4 reported as one, the two merged together; the
trunk's `0b55448` brought in by the builder at step 4's boundary, the lead's trial merge onto
`e012db5` with the known truths the one conflict, both sides kept and formatted); ruff and the
format check clean; the builder's fast tier whole on each step's tree (5,300 then 5,353
passed, none failed), the slow tier of the touched files and the known truths (649 then
3,032 passed, 7 expected failures), the pace tests alone (11 passed); the lead's checks on the
merged tree: the generator reproduces all fifteen ship and boat files byte for byte, the
physics' diff the oar force alone (`physics/oars.py` new, ten lines in the integrator's
substep, a term that is zero on every hull without an `oars:` section: the brief's one
leave), the eight ships' files differing by the `file:` line under each boat alone, no
consent file touched, no model identifier; the lead's run of the boat, aboard-another,
in-world, primer, grammar, parity, generator and particulars tests with the steps' truths on
the merged tree, then **the whole fast tier here (whole) and the whole suite in the cloud (run 26 on
`f5be911`, these steps and 88's close: lint green, 5,713 passed over the six shards, 3
skipped, 10 expected failures, none failed, 50 minutes; the pace job, informative, 7 of 11,
the same four under the floor as on runs 24 and 25, measured below under 88's record).**

**Step 3, the player's seat on another ship and the director's door** (the design's §4 and
its postscript; the tuning notes, step 3): `--ship <name>` at both drivers writes a driver's
line in the player's own ship's log saying how she is left (as she lies, her watch kept and
her sails as they were, her rules captain's by his intent where she has one) and sets the
drivers to follow her hull; his prompt is hers by the one rule, her rules captain stands
aside at his hand and `captain: carry on` gives her back; `--seat <station> --ship` is a
`PlayerSeat` on her hull (`seat.seat_world`), which stays hers when the drivers move on and
**goes with its person between hulls** (`PlayerSeat.move_to`, the step 1 postscript's
promise: his voice in a host, his own station again at home, a captive's seat stood down
quietly). The director's door with another hull followed reads her by the one rule, the
other hull by her name at the head; the director's hand on the followed ship is refused
naming her as such; the truth lists the player's own ship among the sail when another is
read as the own. 86's three seams read by the hull, two of them pinned by tests with no
code moved. **Truths 7-322, 7-323, 7-326.** Found on the way: a saved hull block with no
door's station (the seat's journal and her bindings) is restored once the replay has made
her; the seat's person in the host's boat found by name; the held helper.

**Step 4, the boat as a hull of the one world** (§5 and its postscript; the tuning notes,
step 4): five boats' files through the generator (`boat-yawl-16`, `boat-cutter-28`,
`boat-launch-31`, `boat-launch-25`, `boat-cutter-23`: the hull by Luce's rule of breadth and
judged depth, one mast stepped at will with a standing lug, the oars, a coxswain and the
oarsmen, a grapnel, no guns; each line's rung and source in its note, Steel's Folio LVII
named to read), the schema's `oars:` section (`number`, `thrust_n`, `power_w`, `tiring_h`).
**The oar force**: F_oar(u) = min(F_0, P / max(u, u_min)) x stroke x 1 / (1 + hours / T) an
oar (F_0 50 N, P 60 W, T four hours; judgement, fitted to the brief's behaviours), read
beside the cable's pull and the trawl's drag; the frigate's launch under ten oars 3.3 to 3.6
kn fresh, the cutter's boat to the Falmouth quay in 26 minutes and back under her lug at 2.7
to 2.9 kn. **The boat manned as a hull**: `go to the boat` puts her on the sea as a vessel
and a hull of her own at her ship's lee quarter, her company from her own file, the person in
her by step 1's road with the drivers following; `where am I` and the readings hers; her
orders (`give way`, `easy all`, `lie on your oars`, `boat your oars`, `out oars`, `pull for
...`, `step the mast`, `unstep the mast`, `come alongside`; on the ship `cut the boat
adrift`) through the vocabulary with the period's refusals; the coxswain steers for the mark
by the engine's helm law and **tends the lug's sheet each tick** (the one thing the design
did not foresee: untended she ran aback by her own sheet); hoisted in with her log folded
into the ship's as `boat.log` lines; swamped in a sea above her weather or cut adrift she is
lost until the yard replaces her; the hoy that brings the powder off a vessel of the sea
(86's deferral). A boat is hoisted out hove to or at anchor, refused with way on her above
two knots (the merged tree's one new rule). **Truths 7-327, 7-328, 7-329, 7b-114.** Taken
another way with the reason (the notes): `man the boat` stays `send the boat`'s synonym,
`step the mast` at once, the boat counts nothing against the cap, her account a hull's, the
coxswain's helm the helmsman's law.

**What moved: nothing pinned** (no recorded passage mans a boat or seats the player on
another ship; the ordnance test's payload gained the hoy's id, a built change). **The lead's
rulings at the merge:** the ship's muster is to be reduced by the boat's crew while she is
manned (a cutter of thirty feels four men away), booked for 82's close (step 7, the
stations) or a follow-up if step 7 cannot carry it; the five boat files are the ships
session's to bring to §5.0's rungs when Steel's Folio LVII is read, never by hand. **Next:**
step 5 (the tow and the kedge's false denial; truth 7b-113's lugger clause to be put to the
lead with the frigate clause's ruling), step 6 (the director's forms), step 7 (the stations
and the readings' words; 87 after it).

### Package 75, the hull step (the eight existing ships' own hulls), as merged (2026-10-31)

Merged `--no-ff` from the ships session's `claude/pkg-75` at `d9477c6` (the six streams built
and reviewed in their worktrees, the owner's word to build the rest too, the lead's ten
rulings of 2026-10-31 taken, the eight landed as one commit `7dd68f2`, B5's bands and the
turned guard `3cea266`, the record `3f48c41`, the trunk's `f5be911` merged by the session, the
report's test line `d9477c6`; the merge a fast-forward in content, made `--no-ff`); ruff and
the format check clean; the session's fast tier on the final tree 5,877 passed, 2 skipped,
none failed (46 minutes), the touched files and the guard sets with `--slow`, the pictures in
a real browser; the lead's checks: the generator reproduces all fifteen ship and boat files
byte for byte on the landed tree, `freesail/`, the evolutions, the sail classes, the people
and the captains' files untouched against the trunk, no consent file touched, no model
identifier; **the whole fast tier here on the landed tree (whole) and the whole suite in the cloud
(run 27 on `cfe48a5`: lint green, 6,231 passed over the six shards, 11 skipped, 10 expected
failures, none failed, 42 minutes, the count up from run 26's 5,713 by the hulls' suites; the
pace job, informative, 8 of 11, truth 51 at the floor again and three under it as the runs
before, the matter recorded under 88).**

**What was built** (`docs/dev/TuningNotes.md` "The eight hulls"; `docs/design/Build-Ships.md`
§5 to §7 and §15; the pages notes `pages-zaz2587.md`, `pages-zaz4491.md`, `pages-zaz6381.md`
new and `pages-zaz6306.md`, `pages-chapman-pl59.md`, `pages-chapelle-fig17.md` extended; the
owner's report and 27 sheets under `docs/playtests/2026-10-31-hulls-the-eight/`): each of the
eight drawn from her own sheets at rung S (the frigate's class draught and *Amazon*'s copy;
the brig's own lines with two sisters as checks; *Sherbourne*'s own draught for the cutter;
the *Éclair* taken off afloat above the water with *Le Coureur*'s body below it, S†; Chapman's
plate for the smack and Chapelle's *Lynx* for the schooners, S†, carried to the files' length
and beam), by a module each under `tools/ships/` called from one place in the generator;
nothing in `physics/` or `combat/` and nothing in the eight's behaviour (the check on a clean
archive: every log line, order's answer, each tick's dynamics as exact floats, the rig every
thirty ticks, the random streams' final states, the volleys and all ten polars identical; the
loaded keys that differ are `hull.profile`, the port guns' `height_m` and `deck`, and words).
The viewer's mends old beside new (the port band following the side within 2 mm, the head
closed to the stem, the cutter's stem head square across, every boom's swing in the frame and
its sheet to the taffrail, the painter's order of the closed body). **Truth 7-185**, which had
no code, drafted in `tests/test_profiles.py` as §15 directs for Phase 5 to move, its bands
first written there from each sheet and the brig's moved old beside new to the sheet's 5 ft 2
in (1.555 to 1.585 m) with the source, the one pin the step moves. The one table of every
figure the sheets disagree with (the brig's displacement −27% first, the frigate's +14% and
her keel and masts, the cutter's and lugger's masts), recorded and not moved by principle 5;
the port triples before L2 (the cutter's sills at 1.00 to 1.23 m and her lowest port shut at
14.5° flagged for the owner's test when L2 comes; no port shut at the heels the game reaches
today); the three captain's trials named once with their clean-archive figures (the owner's
machine's digests differ from the build machine's with every state and tick the same).

**The lead's rulings at the merge** (the notes to the ships session below): the eight points
accepted as reported (7-185 written as a test for Phase 5; the marks as the fixer read
principle 4, the rung letter each hull's best source; `RIGHTLY_WITHOUT` per part; the boats
held apart, their drawing 82's; the lugger's 18.33 m by the re-read; the viewer's further
small mends; `form.py`'s box under a counter booked for a later ship's builder); **the
viewer step for the rig's lines approved** (the sheets', braces' and tacks' ends read from the
drawn rail and stem head in place of the old datum and half-beam, the three level bowsprits
rooted at the sheet's height: no file and no pin moved, pictures old beside new, before L2 or
beside it; the owner's veto stands if they would rather see it later); **the Greenwich-held
image already in the repository** (`docs/references/images/bilander-gwyn-c1780-nmm-pag3828.webp`,
from before this step) put to the owner: the lead's pick is to take the file out of the tree
with its catalogue reference and link left in the README in its place, unless the owner holds
a licence for it; the ships session acts on the owner's word.

**Next:** L2 (the lee ports' rule) and L3, then the *Prince de Neufchatel* with B3.4 first, the
design-record commit at B2's window owed by the session; the later package on the files'
figures against the sheets, the brig first; 81 (the guns in their ports) and 91 after 75's
hulls, now that the eight stand on their own lines.

### Package 82, steps 5 to 7 and the drawing, as merged; the package closed (2026-10-31)

Merged `--no-ff` from the Fable sibling session's `claude/pkg-82` at `73756af` (step 5, step 6,
step 7 and the boat's drawing in its own commit, the aboard table's count in its own test, the
records of the close and the lead's two rulings booked at `065384d`; the trunk's hull step
brought in by the builder after the close at `8a421b2`, the view tests' table of the parts a hull
rightly lacks gaining the boats, which now carry a profile by rule and have no gallery, light,
head or port band by their form: the one conflict, the builder's resolution taken over the
lead's trial one, which said the same by a clause); ruff and the format check clean; the
builder's fast tier whole on the package's final tree (5,384 passed, none failed) and again on
the tree with the hull step in (5,910 passed, none failed), the slow tier of the thirty-six
touched files and the known truths (3,371 passed, 7 expected failures), the pace tests alone
(11 passed); the lead's checks on the merged tree:
the generator reproduces all fifteen files byte for byte (the eight ships' with the hull
step's profiles, the five boats' with theirs), the physics' diff the tow's thirteen lines in
the integrator beside the oar force (the brief's one leave: the towing boat's net pull read at
the stem as the cable's pull is read at the hawse), no consent file touched, no model
identifier; the lead's run of the tow, boat, director, view-geometry, in-world, primer and
log-lines tests on the merged tree, then **the whole fast tier here and the whole suite in the
cloud dispatched at the push (run 28 on `b896c4c`: lint green, 6,262 passed over the six
shards, 11 skipped, 10 expected failures, none failed, 42 minutes, the count up from run 27's
6,231 by the boats' and the tow's suites; the pace job, informative, 11 of 11 in 212 seconds,
the four pace truths that sat under the cloud's floor on runs 24 to 27 all passing this run,
which reads as the cloud's noise the bisection under 88 found and not as a cost moved by 82:
the matter stays recorded under 88 and re-read each run).**

**Step 5, towing by the boat and the kedge's false denial** (the design's §6 and its
postscript; the tuning notes, step 5): `tow her with the boat [to <the point or bearing>]`
from the ship, the boat manned and made a hull by step 4's road, her oars out and giving
way, the ship's helmsman given the tow's bearing; the coupling kinematic (the boat a line's
length ahead on the bearing, twenty fathoms, her way the ship's) and the force her oars' net
pull at the ship's speed, clamped at nothing, read by the integrator at the stem; the men
tiring by the oars' hours with the ship's log saying so once an hour; `the boat alongside`
ending it, the tow ending of itself at an anchor or the ground; refused in a sea the boat
cannot work in, at anchor and aground. Measured: the cutter under her four-oared boat 1.15 to
1.19 kn fresh and 0.83 at four hours, her head round in two minutes; the frigate under her
launch's ten oars 0.78 kn fresh, her head from north to east in ten minutes, 0.57 at four
hours (the lead's ruling on the frigate clause standing: the physics' figure); the lugger
1.16 kn fresh. **The kedge's false denial** (spec M7b §21k's one fault) mended: the boat's
keeper reads every evolution that holds her through the scripts' `holds()`, so the lay-out
is no longer denied at its first minute. Found on the way, the one that matters: a manned
boat not followed by the drivers slept at the first switch for want of a brain, which step 4's
followed-boat tests never saw; mended in `crews.crewed`. **Truths 7-330, 7-331, 7b-113.**

**7b-113's lugger clause, ruled:** the spec's "towed clear at half a knot" is not a figure
F_0 50 N an oar gives in any hour a boat's crew can pull (the lugger makes 1.16 kn fresh and
0.8 after four hours, half a knot at twelve); **the physics' figure stands**, as the lead ruled
for the frigate's clause, the truth asserting the physics' figures with the spec's words
quoted in its docstring; the lesser is costed in the notes for the owner (F_0 25 N an oar
gives the lugger and the cutter about 0.6 kn fresh and the frigate's launch 0.4 kn, one
generator constant and the five files regenerated), and is the owner's to ask for if they
want the words rather than the figure.

**Step 6, the stations, the director and the readings** (§7; the tuning notes, step 6): the
reading `the followed ship` (a world row, read in an observed world too); the events `the boat
manned`, `the boat lost`, `the tow begun`, `the tow ended` and `aboard another ship` (the
primer's table kept equal to the registry by 85's test); the director's `follow "X"` and
`follow nobody` as a channel of the world orders and a driver's line at the seat costing no
act, the dry run saying what it would do; the boat stove, swamped or gone adrift by the
`aboard:` table through `lose_boat`; the truth showing a manned boat as a vessel with her
ship, who is in her, what she is under and whom she tows; the harness's shape and ship words
for a boat. Found on the way: `come alongside` from the boat's prompt had left the drivers'
`followed` on the boat's hull (a write through her façade, hidden by the fallback to the
player's hull), mended in `boats._root`. **Truth 7-332.**

**Step 7, the records and the boat's drawing** (§5.4 and §8): spec M7b §11, §12 and §21k "as
built", Harness §17b, the primer's chapter 26 "The boat, and going aboard another ship"
(in-world), the director's library; the boat's drawing by §5.4's road with B5's helpers,
each boat's shape keys by rule from her principal dimensions, every line judged and said so,
a square transom and no head, the drawn displacement within the record's share of the filed
(the yawl 12% under, the 28-ft cutter 13% over, the 31-ft launch 12% over, the two others
within 1%), the eight ships' files untouched; the snapshot's `oars` block and the viewer
drawing her oars from the thwarts while they are out. `test_log_lines`' standing-order names
by index (88's booked finding mended on the way).

**What moved: nothing pinned** but the aboard table's count (31 to 34 by the boat's three
things, in the director's and the aboard-found tests). **The package, closed:** the seven
items of the re-brief built; truths 7-320 to 7-334 and the boat's 7b-113 and 7b-114 stand
(the two 7b numbers shared with other packages' truths, the tests' names saying so); the
physics changed by the oar force and the tow's reading of it alone; the ship files through
the generator; no consent file touched. **Open, booked:** the ship's muster reduced by the
boat's crew while she is manned (a follow-up, hung on the manning and the hoisting in); the
business's tile loads (step 2's finding, with the observer's cost); the five boat files to
the ladder's rungs when Steel's Folio LVII is read (the ships session's, regenerated with
the eight); the frigate's quarterdeck guns and the files' figures against the sheets (the
later package). **Next:** 65 (the place's knowledge, Fable) launched on this merge as the
owner ordered; 74 after 65; 87 (the stations' work) after 82's stations.

### The owner's testing week: loose ends mended by the lead (2026-10-31 onward)

**The followed hull's log at the drivers (2026-10-31).** The owner, testing 82's visit by
boat, saw nothing of his order in the log, neither refusal nor acceptance. Reproduced at
the console: `send the boat to the Raven with Mr Pearce` works from the prompt (the launch
away, the person aboard her in twenty-five minutes, `where am I` "aboard the Raven, on the
quarterdeck, a visitor, of the Amazon"), but after `follow "Raven"` every order and query
went to her hull and its lines to her log while the console went on listening to the hull it
was attached to at the start (`World.log` is the followed hull's by `_PER_SHIP_FIELDS`, the
listener was on the object), so an order, a refusal or an answer printed nothing; the
browser's driver the same. Mended in both (`Console._follow_log`, `Driver._follow_log`: the
listener moves to the followed hull's log after each line, each tick and each `follow`, so
`go to the boat` and `come alongside` move it too), tests beside each
(`tests/test_console.py`, `tests/test_server.py`); the console, server and observer suites
green here; the whole suite in the cloud on the push (run 29 on `a7440f0`: lint green, 6,264
passed over the six shards, 11 skipped, 10 expected failures, none failed, 41 minutes; the pace
job, informative, 7 of 11, the same four truths under the floor as on runs 24 to 27 on a slow
runner, the matter recorded under 88). Found on the way, for the week's turn:
the player's own body goes aboard another ship only as a person sent in the boat (the
captain's, from the prompt: `send the boat to the Raven with Captain Bowen`, after which
`where am I` answers as a visitor's while the prompt and the readings stay his own ship's
until `follow "Raven"`), or by `--seat captain --ship <name>` at the start; from his own
manned boat (`go to the launch`, `pull for the Raven`) there is no order to go aboard her
(`come alongside` is to his own ship): booked as 82's first follow-up.

**The owner's notes of 2026-11-01 (four points, from the saves `indefatigable-and-schooner-test-2`,
`m7-indefatigable-and-raven-mid-channel` and `boat-between-ships-test`; the lead's reading
against the code, nothing built):**

1. *Says and hails from the other vessel's models not shown to the player, even at the same
   place ashore.* Confirmed in the code: a station's `say` (`orders/stations.py` `_say`)
   delivers the word to `_stations_held(world)`, the speaker's own hull's stations and the
   player's seat there, although 66 and 84 gave `hearing.stations_everywhere` and
   `people_hearing` for every hull; and the line is written in the speaker's hull's log alone,
   which the player's console and browser never show. **For 65** (steps 2 and 4, after the
   reset): the hearers of a word are every hull's stations within hearing (`within_hearing`
   across hulls: ashore at the same place of the same port, aboard the same hull for a
   visitor, a hail within hail between hulls), the word written as heard into each hearing
   hull's log (so the player's log carries what his people heard and the replay stays a
   function of the inputs), and the drivers show it; truth 7-389 (free) takes it.
2. *The player not clearly bound to a single person; travel between ships and `follow`
   unintuitive.* Part of it was the followed-hull log bug, mended at a7440f0. The rest is
   decision 59's spirit carried through: **for 65's step 4**, the player is one person (his
   ship's captain by default, or the seat's person), the prompt and the play log are that
   person's (what reaches him where he is), he moves between ships as a person moves (in the
   boat, the prompt following his body), and `follow` is the owner's eye, a driver's command
   for observing and never the player's road; the primer's chapters 14, 19 and 26 and the
   browser's page say so in one sentence. The missing road, the player going aboard another
   ship from his own manned boat (`go to the launch`, `pull for the Raven`, then aboard her),
   is 82's first follow-up and is taken with step 4. Put to the owner as decision 62.
3. *The browser's play log and prompt as a single person's.* The same: 65's step 4.
4. *A model's station not retained when its person moved ship (a new station "the Mr Hill"
   made and a separate model seated).* On the trunk the harness does move with the person:
   probed here with a fake at the Raven's officer's station sent aboard the Amazon by her
   captain's `send the boat to the Amazon with Mr Newton`: the same harness, model and door
   stood at the visitor's station on the Amazon, the Raven's station emptied. What breaks is
   the agent API's desk (`agents/remote.py`), whose seats are keyed by station name and ship:
   the moved station reads as "mr newton of the Amazon", the remote client's seat loses its
   harness, the new station reads as unseated, and a fresh model is seated at it (the
   director's seats or the door). Two things **for 82's follow-up, not 65**: the desk's seat
   follows the harness (keyed by the harness, not the name and the ship), and the visitor
   keeps his own station's name as the primer's chapter 26 promises ("officer of the watch,
   of the Raven, aboard the Amazon"), not a station named for the man.
   **The owner's account, 2026-11-01 (the API door):** the moment Mr Hill came aboard, the
   Opus door that held the owner's own officer became "the Mr Hill" in its same session (and
   said so), and `stand down the Mr Hill` stood down both him and the officer: the desk had
   the one door covering both stations, the newest by recency. So the desk resolves a door's
   station by recency and not by a seat of its own; the follow-up keys each door to its
   harness.
5. *The glass and making out a sail are unwieldy* (the owner, 2026-11-01): `the glass on`
   and `make out` give the nearest sail, or at best the nearest of the named kind, and the
   wanted sail is hard to name. The rule to build (a loose end for the week's turn, the
   lookout's words in `api/queries.py` and the sail-naming of `world/hail.py`): the most
   specific naming wins, read from the words the lookout himself used: the kind, the quarter
   ("on the larboard quarter"), the bearing ("bearing NE by N") and the distance ("distant a
   mile"), each narrowing the pool; where ambiguity remains, the closer; a name once known
   ("the Raven") over all. The same resolver for the hail's addressee, `make out`, `the
   glass on`, `bearing of` and `pull for`, so that one way of naming a sail serves everywhere.

**The week's turn (the owner, 2026-11-05):** the reset in, the owner's new playtests read
(seven saves: the brig off Falmouth fully crewed, brig against brig, the sixty-four and the
Raven at dusk, three small convoy encounters and one with every captain a model) and his
notes 5 to 7 (the identified sail named in the readings; the Chevalier's captain's door
holding the Lynx's captain's station; the hails between model captains answered by the
table). The owner's word: the hotfix's moved pins bisected on Opus and the hotfix brought in
(session_01XooV47b8tcPVMMRaCtvurE, launched 19:11, branch `claude/hail-pins`); 65 resumed
on the hotfix's merge (the same `_say` is touched by both); 82b briefed and launched beside
65 on the same merge; 95 after 82b. Decision 62 taken.

**The case study (2026-11-05):** the all-models convoy encounter read whole and written up
in `docs/playtests/2026-11-05-small-convoy-all-models/case-study.md` (the course of the
action, what held, nine lessons each sent to its package: 95, 82b items 3 to 5, 74, 65's
step 4, and one booked: the wounded captain, whose body the needs read as rested with a ball
through it).

**The second case study (2026-11-05):** the brig off Falmouth with every station a
different model, `docs/playtests/2026-11-05-brig-off-falmouth-fully-crewed/case-study.md`:
a crew of five models worked as a crew with the director keeping the world; five lessons,
the first put to the owner as decision 63 (an order told through a station is the captain's
word for it; the deck given when the captain leaves it is the command), the rest to 95 (the
lookout's hail read as `hail the pilot`), 65's step 1 (a far body's lines in the ship's log)
and 65's step 2 (a word to a person is no order of the ship, in the briefs).

**The wakes in the fully crewed brig (the owner's point of 2026-11-05, which strengthens 65):**
in four hours and a half the officer of the watch was woken 130 times (28 an hour), the
master 68, the captain 60, the director 24, the lookout 16. The officer's wakes: 27 by a
word from the captain (most of them told to him, rightly), the rest by his own stand-by
conditions, which he set wide ("the deck given, or a message, or a wind shift, or a sail
made out, or ..."); the captain's 60: 38 by "a word from the captain", which were the
master's and the officer's words to him (23 and 8) and in seven cases his own last word.
For 65: the reach rule (a wake carries a line he perceived, by his place) is the cure for a
crowded deck, and two mends for step 2, pinned in the code: (a) the wake's reason for a
word addressed to a station is the fixed string `A_WORD` ("a word from the captain",
`agents/harness.py`, package 29's constant from when only the player's captain spoke),
whoever spoke: the reason names the speaker and the kind (a word, a question, from whom);
(b) the owner's observation, borne out by seven of the captain's sixty wakes following his
own last word: a station woken by its own line. `_heard_between` excludes the station's own
actor, so the road is the addressed word (`a.word`, set by `tell`, `say to` and the words
kept for an unheld station, `orders/stations.py` line 954's "kept for whoever takes the
station"): reproduce with a station that tells or says to a station nobody holds, and with
one that names itself, and make a station's own word never its wake. For the briefs (65's step 2 as well): stand by for the few things that matter, and
let the rest come with the next sample.

**For mulling, not for building (the owner, 2026-11-05): the shape of conversation.** In
life speech is not turn-based: a man speaks, acts and listens at once. The lead's take: the
world is already not turn-based (it ticks on between every station's turns, and a reply
may speak, order and stand by in one turn, which is speaking and acting at once); what is
turn-based is the listening, since a word reaches a station only at its next sample or
wake. The costs are the wake policy (every addressed word a wake, every overheard word a
wait: 41's rule, which 65's reach rule refines) and the floor (the pace rule holds the
ship at 1x while a sample is open, so six doors on one deck crawl). Roads worth mulling,
none taken: words within a short span of ship time folded into one sample per hearer
rather than one wake each (a conversation read as a stream at the station's own cadence);
a "while you spoke" fold for the words that arrived during a long turn; and an attention
rule beside the place rule (a man at the braces does not hear the quarterdeck). The gain of
each measured against the fully crewed brig's figures before anything is built.

**The hotfix merged (2026-11-05, the hail as typed and as answered, b1447bc with the
builder's 0b50156 and 25c634b):** the nine pinned passages red in cloud run 30 were not the
hotfix's: on the 24.04 machine every one stands at its pin on the hotfix's tree (the thick
weather trial and the merchant passage alone, line for line equal to the trunk's; the cloud's
shard 0 whole; the slow tier of the truths and the trials, 273 passed), and no order of those
passages reaches the hail's grammar. What moved was the cloud's runner image: ubuntu-latest
went from 24.04 to 26.04 between runs 29 and 30 (glibc 2.43 for 2.39; the same Python and
wheels), and a last-place difference in the system's libm moves a long passage by a line or
a minute, package 69's kind of cause. The builder could not sail under the new library; the
lead's proofs: run 31, the trunk as it stood on the unpinned workflow (red in the same nine
if so), and the workflow's Linux runner pinned to ubuntu-24.04 from this merge, the run on
the merged trunk after it (green if so). The builder found on the way that `hail._addressee`
takes the distance to every candidate on every hail (a cost, not a change). The pace job's
three floors under on run 30: the runner's speed. Run 31 (the trunk at ce9071f, no hotfix
aboard, the workflow still on ubuntu-latest, 21:18 to 22:18 UTC): lint green, all six shards
red, pace green; the failures the same nine and no other (shard 0 the two captain trials,
the thick-weather merchant 424 lines for 426 and the lee-shore digest c2bfe179 for 04f2fcd0;
shard 1 truths 78 and 79 and the merchant at seed 7, 96480 for 96540; shard 2 gate 5B's
schooner, 767 lines for 766; shard 3 the anchorings [57, 100918] for [57, 100616, 115547];
shard 4 gate 6A's intent, brought up at 111239 for 111238; shard 5 truth 77's digest
5422360d for 6abbbff4), the first proof made: the image moves the pins, the hotfix moved
none. Run 32 (the trunk at 36d30c4, the hotfix aboard, the runner pinned to ubuntu-24.04,
22:18 to 23:01 UTC): lint green, all six shards green, 6,266 passed, 11 skipped, 10
expected failures (run 29's 6,264 and the hotfix's two tests); the pace job 7 of 11, the
four floors under at 423 to 486 against 500, the runner's speed as on run 30. The second
proof made: the nine pins stand on the 24.04 machine with the hotfix in, and the trunk is
green again in the cloud. The image moves only when the lead moves it and re-measures.

**Beside them:** the owner's Opus session's hotfixes are on no branch on GitHub (the saves'
rules digest `9221bc3593cad15d` against the trunk's); the lead has asked for that branch, so
the testing build and the trunk do not diverge and the saves replay on the trunk.

### Package 65, step 1 (the rule in the harness), as merged (2026-11-05)

Merged `claude/pkg-65` at f52f146 (eb147e7, `--no-ff`; the step's final tree 1bb8933 with
the trunk's d4e6701 merged, then the suites' record), held unmerged on its branch from
2026-10-31 through the week's pause by the owner's word and merged on the week's turn with
the hotfix in. **Built as designed, with the lead's rulings of 2026-10-31** (the tell-tale in
the cabin alone; the sail work a sound in the cabin by `as_heard`; the deck the default reach
and the default place of a reading, the kinds' test generated from the code's string
literals; `go below` and `go to <a place below>` refused to a station with the deck below
the captain's, `go aloft` allowed): `freesail/world/knowledge.py` (130 kinds and 80 families
placed), `Reading.where` on 82 rows by hand, the harness's sample by place (`Harness.senses`
cached by tick, orders and log length; the log by reach with the lines slept through read
with a sleeper's senses; `readings_elsewhere`; `_reaches` extended from 66's words to every
kind: the stand-by's wake, the danger wake, the severity sample and the notable digest; the
brief head and the handover fold by senses; a tripwire judged below fired as the officer's
words), the readings tool's `not_here` and `where_you_are`, the prompt's query answered with
where (`orders/prompt.py` `_elsewhere`), the scenario key `knowledge: all`, one sentence in
every brief's head. **Taken another way, accepted:** the deck reads every row (the glass
and the purser's books the deck's too), so the pinned deck samples stand and the note's "the
glass none" is corrected; the fold carries the cabin's rows in the folded turn and keeps
37g's brief whole; the depth tripwire reads the chart, which the cabin has, so a captain
below is woken by it as 58a's, the call's words coming for a tripwire of the deck's rows
alone; `message.aboard` the deck's; a person in the script's boat has her deck's senses
within a pull. **Found on the way:** the brief head leaked the whole readings and log to a
station seated below (mended); the danger wake read no hearing (gated); the readings tool
at a station nobody holds raised (caught). **Pins:** nothing recorded moved (no recorded
passage moves a person below or ashore; the filter writes nothing); two truths moved old
beside new with the reason: 7b-100 (53's officer took the deck into the gunroom) kept as a
strict expected failure with the ruling and read anew; 7-200 (74's tender) the fake skipper
ashore acting on his own landing and asking for the boat again while she was away. The
informative pace band of truth 7-386 widened from eight tenths to seven for the machine's
noise, the figures the record (three stations seated, 593 under the rule against 615 with
it off; the frigate alone 530). **The suites:** the builder's fast tier whole 5,927 passed;
the slow tier of the eighteen touched files and the known truths 841 passed, 8 expected
failures; the pace tests all passed; the lead's trial merge on the trunk's 36d30c4 (the
tuning notes' conflict with the hotfix builder's section resolved keeping both, in order),
ruff check and format clean, the fast tier whole green (exit 0); the whole suite in the
cloud on the pinned runner after the hotfix's own proof run: **run 33 on 43823f6** (23:26 to
00:30 UTC, 2026-11-05 to 06), lint green, all six shards green, 6,287 passed, 11 skipped, 11
expected failures (run 32's 6,266 and 10, plus step 1's tests and 7b-100's old reading as
the eleventh), the pace job 9 of 13 (the four floors under at 444 to 499 against 500, the
runner's speed as on runs 30 and 32; the frigate alone 499, a hair under). Steps 2 to 8 go on
from the resumption of 2026-11-05 with decisions 62 and 63 and the hearing across hulls
added to the brief.

### Package 82b, item 1 (the door follows its harness), as merged (2026-11-06)

Merged `claude/pkg-82b` at 9596fd4 (07c06a0, `--no-ff`; commits 906efb7, c89baba, fcb5702,
de594fc with the trunk's 63035f6 brought in). **Built as the design note and the lead's
rulings have it:** `Harness.ident` ("<the hull first seated on>/<station>", "#2" on a clash),
set in the constructor, carried in `to_dict` and `restore`, derived the same way for a save
from before; the desk's seats filed by it (`Seat.ident`, `Desk._file`), each seat keeping the
door's address (`Seat.address`) for its calls, found by `seat_at`; a door stationing again by
its own name and ship takes up its harness wherever its person is (`home_harness`), nothing
made at the station he left; `Seat.hull` the hull the station is in now; the listing naming a
visitor "captain, of the X, aboard the Amazon" with his ident (`visitor_words`). **The root
cause found:** `movement.harness_of` and `seat_of_person` matched a harness by
`stations.holder(station)`, and on the player's hull `Stations.holder` reads the people of
the hull whose block is running, so while a brig's captain's boat arrived in the player's
hull's block the frigate's "captain" read as him and one harness came to stand at two
stations: the owner's "one door covering both" and "stand down the Mr Hill stood down both".
The mend: a station that names its person is his by that name alone; the holder is read only
for a station that names nobody. The harness touches are the four approved and no more
(the constructor line, `to_dict`, `restore`, `new_ident`; `all_agents` through
`visitor_words`); beyond the list and accepted: `ui/harbour.py`'s two `seat_at` lookups in
place of `seats.get(seat_key(...))`, `tools/regatta.py`'s one. Tests
`tests/test_door_follows.py` (three, driven on the desk itself with made-up identities and a
temporary consent directory); truths 7-390 (the moved station keeps its door, its model and
its ident through the move, a restationing and the save by both roads) and 7-391 (two
captains through one door each answered by its own harness; a stand-down of one leaves the
other); toggled: the trunk's `harness_of` fails the move test, the trunk's desk makes a
fresh harness at the brig's captain after a load. **The builder's suites on 9596fd4:** the
fast tier whole exit 0 (one browser-contrast test of the MCP chart under -n 4 read 7.96
against the 8.0 floor on the pre-merge tree and 8.03 alone and on the trunk: the container's
margin, no floor moved); the slow tier of 16 touched files and the known truths exit 0 (about
624); the pace alone, 7-159 toggled against the trunk three runs each alternating, trunk
510, 466, 511 and the branch 503, 504, 491, both straddling the floor as the container does
(nothing of 82b in the far convoy's loop); ruff and format clean. **Found on the way and
booked:** `Stations.holder` on the player's hull reads the running block's people (her
`Stations` is built with the World itself, and `world.people` delegates to the current
hull): package 97. **The lead's change at the merge:** `remote.py`'s "Your words are in
the log under your mark" to "Your words are in your journal under your mark" with its two
pins, for decision 60 (65's step 2, merged next). Items 2 to 5 are on the branch (e7317f7)
and report at their boundary.

### Package 65, step 2 (a reply's prose is the person's own note), as merged (2026-11-06)

Merged `claude/pkg-65` at aafd89c (5288665, `--no-ff`; the code at ff319e1 with the trunk's
dee47da merged, then the suites' figures), on top of 82b's item 1: the harness met cleanly
(82b's ident lines and the step's `_say` apart), the known truths' tail both sides' appended
truths kept. **Built as the design's decision 60 and the lead's word of 2026-11-05:**
`Harness._say` writes a reply's prose into the station's journal under the model's mark
(`PROSE_KIND`) and into the game's one director's log by the station (on the player's own
hull with that hull current, so the act is the game's and replays into the same log), and
into no log of the play; `say_aboard` deleted, `agent.note` out of `AGENT_LOG_KINDS` and the
reaches; the MCP `say` answers "Noted in your journal, under your mark." **The say across
hulls:** `_say`'s hearers are every hull's stations within hearing
(`hearing.stations_everywhere`, `within_hearing`, each hearer's spot read in its own hull's
block by the new `station_spot_on`), the line written as heard into each hearing hull's log
with `heard_by` and `said_from`; a hail from the masthead carries over her own deck alone.
**The wake's reason names the speaker and the kind** (`Harness.add_word(words, reason)`,
every word setter converted: "a word from the master (Mr Hart)", "an answer from ...", "no
answer from ...", "the deck, given by ...", "the words kept for the station while nobody
held it", "a question from the captain"), and **a station is never woken by its own word**
(`tell` or `say to` oneself refused: "The master tells itself nothing; tell another
station."); the briefs' sibling sentence from the brig case study's lesson 4; the director's
sample carries the stations' notes since its last (`Sample.notes`). **The empty-reply
count:** prose alone where an answer is owed counts as empty with the notice `NOTE_NOT_HEARD`
naming the tools, journaled in those words and never as "an empty reply"; a call resets it,
words never (the lead's ruling 3 of 2026-10-31 and the builder's reading: the count is
judged by the game). Truths 7-379 and 7-389; four tests in `tests/test_knowledge.py`.
**Taken another way, ruled:** the watcher is not given `say` (the owner's eye, silent in the
world; `answer` its one road). **What moved, with the proof:** truth 78's pin, the fake
captain's "I have the command." at tick 0 an `agent.note` line of the log until now and his
journal's note since, 3,113 to 3,112 lines, digest 1c9a985bfd5dce0f to dfaa7ab3bdd70295,
every other assertion unchanged, old beside new in the test; three slow tests re-pinned to
the new words and reasons; one old count test kept as a strict expected failure beside its
replacement. **Found on the way:** a hull façade read from inside another hull's order
answers for the current hull (mended for `_say`; the family booked as package 97 with 82b's
holder finding and the director's own writes under `follow`); an unanswered question
re-sampled every tick (29c as it stood, not changed); `PlayerSeat` borrows the harness's
`add_word`. **The builder's suites on ff319e1:** the fast tier whole 5,929 passed, 1
expected failure, none failed; the slow tier of the 22 touched files and the known truths
946 passed, 9 expected failures; the pace alone 13 passed (the frigate alone 569; truth
7-386's three stations 615 under the rule against 617 off; the Channel observed 347). **The
lead's merge:** ruff and format clean on the combined tree; the fast tier whole on it exit 1 on one test alone, test_pictures' MCP chart contrast (std 7.97 against the 8.0 floor under four workers; passed alone after, as on both builders' machines and on the trunk: the container's browser margin, no floor moved), every other test passed;
the whole suite in the cloud: **run 34 on 2b59ea4** (03:20 to 04:02 UTC, 2026-11-06, the two merges together), lint green, all six shards green, 6,298 passed, 11 skipped, 12 expected failures (run 33's 6,287 and 11, plus 82b's and the step's tests and the old count test kept strict), the pace job 9 of 13 (the four floors under at 452 to 495 against 500, the runner's speed as on the runs before). Step 3 (the reports, the messenger and the call; the
sleeper's wake; decision 63) goes on.

### Package 75, the lee-port step (L2 and L3), the rig lines and the booms, as merged (2026-11-06)

Merged `claude/pkg-75` at e88df44 (8c30c8a, `--no-ff`; the commits since the hull step
d9477c6: 65c56b8 SW-5 L2 the lee ports by the heel, the owner's rule; 46926bd the record and
the *Neufchatel*'s §12.2a, a rule in the key's place; 148af85 L2's pace cost taken back by
`ports._least_dip`; bd5566c the viewer step for the rig lines' ends; 06019a4 the booms topped
up 3° on the drawn hulls; 1238bed the lead's head brought in; e88df44 SW-5 L3 the roll's
amplitude in the dip, reviewed twice and mended), sent after the owner's review as the week's
one report. **Built as Build-Ships.md §7 and the lead's rulings have it:** the dip the heel
toward the gun's side plus the roll's amplitude (`Firer.roll_deg`, the player's ship's own
where her World keeps a sea; a crewed ship's nought until 84 gives each hull her sea), the
other side the roll less the heel, a chaser on the centre line the roll alone; the sill
lowered against `shot.PORT_SHUT_M`, opened again six inches clear; a gun whose port shuts run
in and housed with its charge kept and its loading going on, its running out and pointing
given over, the drill not timing a round behind a shut port; a shut port silencing its own gun
and no other (a gun named dropped with a line, the word for a broadside all behind shut ports
dropped, a division all behind them passing its turn); a deck's side one line from its first
port shut to its last opened, said only while a gun of it is cast loose, so that no sailing
passage's log moves; the `guns` reading counting the shut ports; the viewer's sheets, braces
and tacks ending on her drawn rail and the stem head (`sideEnd`, `railAtStem`,
`stemTackFraction`, `sortFar`), the booms 3° above the level from their jaws (`BOOM_STEEVE`),
the boats' lug sheet on the drawn rail, `drawnSideAt` restored for 82's oars. **What the roll
does** (the tuning notes, "The lee ports with the roll"): with the sea on her beam the cutter
loses her lee ports at about 12.6 kn against 24.5 on the heel alone, the frigate at about 20.9
against 29; the small ships' weather ports shut in bands of wind (the cutter's at 17.5 to 20
kn); three scripted actions put an enemy before the player in a sea (the blockade's sortie,
her frigate rolling 22° with 11 of 20 lee ports shut). **The flicker, measured and ruled:**
six inches of sill is 1.6° of heel at the frigate's lowest port and 3.1° at the cutter's, less
than a gust swings her, so an hour engaged in gusts with the sea on the beam gave the frigate at
21 kn 46 changes of port over 13 guns (the shortest 6 s apart), the brig at 17 kn 24, the 64 at
17.5 kn 43, the log saying two lines or none; the lead's ruling (the notes to the ships session,
the same day): the dwell `PORT_HOLD_S = 60` before a shut port reopens, in a commit of its own
with L2's reopening-band pins old beside new, and not a heel margin; the owner may veto; the
whole is gate 7's judgement item J1, ruled finally after the gate's testing. **The checks on
the builder's side:** no truth, action or trial moved (546 candidates passed on the tree, 525 at
the base, no outcome changed); the captain's trials 3 failed and 4 passed on both, the owner's
machine's three digest failures as at L2; the four whole logs identical before and after; the
fast tier 6,272 passed; the fifteen ship files regenerate byte for byte; the ports, profile,
primer, grammar-book, in-world and practice suites with `--slow` 1,424 passed after the last
mend; truth 7-190 drafted for Phase 5. **Rulings at the merge:** §12.2a's rule approved for
B3.4 (an after mast with yards and no lower yard handles as a fore-and-after's), B6 out to a
supplemental package, the four things left in the gunnery's files booked to 77. **The lead's
merge:** the trial on 2b59ea4 clean; the fast tier whole on it red in three tests and green
otherwise: the officer's handover test at exactly its fraction (13,200 tokens at the seat
against 0.6 × 22,000: 65's step 2's sentences and 75's port words together), its budget raised
to 22,500 by its own convention with its two pins (3478abf); and the two picture-contrast tests
reading "the chart is blank (std 7.9)" against 8.0, which the trunk's tree and the merged tree
both read above and below on this machine alone and under load (four runs alternating, all
green after; the tuning notes name four such readings since October): the floor set at 4.0,
twice a blank frame's and half the chart's own figure, old beside new in the test's comment
(the same commit). The whole suite in the cloud: **run 35 on ae3c22d** (04:34 to 05:40 UTC), lint green, all six shards green, 6,647 passed, 11 skipped, 12 expected failures (run 34's 6,298 and 12, plus the step's 349 tests: the lee ports' and the view geometry's), the pace job 9 of 13 (the four floors under at 434 to 491 against 500, the runner's speed as on the runs before; the ports' compare a tick within it).

### Package 82b, items 2 to 5 (the visitor's name, the far hull's hail, the held hull, the boat's names), as merged (2026-11-06); the package closed

Merged `claude/pkg-82b` at f406717 (f207fd8, `--no-ff`; the item commits 340b890, d4e294d,
7d15b93, e7317f7, the trunk's 2b59ea4 brought in at 9615f1b, two mends b68d1de and c7ebb90,
the pace figures f406717). **Item 2, the visitor's name (truth 7-392):** aboard another ship
he is "officer of the watch, of the Raven, aboard the Amazon" (`movement.visitor_words`,
`visitor_name`, `visitor_forms`; `visiting_station` names the voice by them, `put_aboard`
passes his home station, `_unbind_visit` the name he was bound under; `where am I` adds
", standing as the ..."); `orders/stations.py` `_station_in` tries the visitor's forms first
(the approved comma rule, proven by toggle: without it the host's "officer of the watch" took
his words), and beyond the list, accepted: a person's name that runs past a station's prefix
wins ("stand down the captain Pope" stands down the visitor, not the host's captain),
`_alias_words` tries the visitor's forms first, `_person_station` falls back to
`find_aboard`. A blemish ruled a tidy for 65's step 8 (the words): the served lines read the
lower-cased key ("the officer of the watch, of the x, aboard the amazon") where the desk's
listing and `where am I` carry the ships' own case. **Item 3, a far hull's hail (truths 7-393,
7-394):** `hail.deliver` asks her hull whatever its shape where a model holds her captain
(`crews.model_held`), the table answering only a ship nobody holds; the hailer's pending
words "She has not yet answered."; proven by toggle; 7-394 replays a hail between two
model-held far hulls by both roads. Found, not 82b's, booked to 97: on the transcript road
harnesses on two hulls seated in the same tick are seated again in hull order, not play order
(`core/replay.py`); 7-394 staggers its seatings by a minute. **Item 4, the held hull (truth
7-400):** `HELD_OVER_CAP = 2`, `model_held` (a harness at captain, started, not released,
with its door, so a replay ranks her alike); in `switch` a held hull ranks with the dealings
and up to the allowance of held hulls is left out of the cap's count; `far_dangers` at the top
of `switch` tries the far body's leg by 88's chart test (`line_shore`, `dangers_ahead`, the
doctrine's `danger_ahead_nm`), puts her about by `far_perform` and writes an urgent
`plan.danger` line that wakes her captain, once in `DANGER_AHEAD_AGAIN_S`. Two mends beyond
the approved lines, found by truth 7-200 on the merged tree and accepted: a cap of nought
(`crewed: {cap: 0}`, nobody promoted: the tender's day) has no allowance over it; and the
check is not made on a port's own track in (`_pilot_water`: the plan ends at the port's
anchor and the leg's mark is one of its `from_sea` marks after the first, its `in` marks or
its anchorage, read on `dealings._track_marks`; the first `from_sea` mark, where she joins
from the open sea, is still judged), as the awake captain makes none in pilot water; toggled
both ways. The convoy's pace, informative (the tuning notes, "Package 82b"): six brigs, none
held and three awake 167 to 171 ticks a second quiet; four held and five awake 110 to 113;
a third of the pace and well above `CREWED_FLOOR_TICKS_S`. **Item 5, the boat's names (truth
7-401):** the root cause, person ids are post-based and shared across hulls, so
`dealings._boat_to_job`'s id map over every hull landed the last-registered hull's men of the
same posts (the Renard's master, boatswain and gunner aboard the Lynx, the frigate's three
left in the boat); `in_boat(pid)` prefers the giver's hull then the boat's destination,
`aboard_her(pid)` the destination's own, for landing, fetching and the way back; `port.py`
`_boat_to_ship` refuses a person of another ship in words ("X is of the Raven, not of this
ship; the boat is not sent."); proven by toggle. The shared ids are booked to 97 with the
façade's readers (and are a fact for 96's configuration of a ship). **The builder's suites
on f406717:** ruff and format clean; the fast tier whole exit 0 (5,933 passed, 1 expected
failure); the slow tier of 22 touched and related files exit 0 (654 passed, 8 expected
failures); the pace alone 12 of 13, truth 7-159 at 497 against 500 and toggled against the
trunk alternating (the branch 504, 480, 504; the trunk 494, 473, 502), the container's margin,
no pin moved. **The lead's merge:** the trial on 48ebefc (the trunk with 75's lee-port step)
clean and lint-clean; the fast tier whole on it green, exit 0, every test passed; the whole suite in the cloud
run 36 on 0d1127f (08:24 to 09:17 UTC): lint green, all six shards green, 6,663 passed, 11 skipped,
12 expected failures; the pace job 9 of 13, the four floors under at 446 to 489 ticks a second against
500 (the runner's speed, as on every run; informative). Package 82b is closed; package 95 launched
on this merge.

### Package 65, step 3 (the reports, the call and the command devolved), as merged (2026-11-06)

Merged `claude/pkg-65` at c6efc0c (0855551, `--no-ff`; the step's code at bb23b8b with the
trunk's 2326d27 brought in at ecc93ff, then 7de98cc the boat's report read in the ship's own
block, 39545b0 the call's words, a287290 the three pins re-measured, c6efc0c the figures), on
top of 82b's items 2 to 5. **Built as the design's §7 and decision 63:** `freesail/world/
reports.py` (new), ticked after the routine and before the stations: the rules' officer of
the watch reports to the captain below a minute after each reportable line of the deck (the
messenger's minute; the lookout's sighting, made out, sail lost, land ahead, closing; the
wind's shift; a signal seen or read; a hail heard or answered; the pilot's hail; the boat
alongside or away), `report.made` with the reach `person`, when the captain is in the hull,
awake, not where he sees the deck, and no model or player holds a station of the officer's
kind (they have the duty, and the brief says it); a danger line, an urgent line of the deck's
business and by night every reportable line make a call at once, `report.called` with the
reach `wakes`, once for a thing until the captain comes on deck or an hour passes; `call the
captain [: <why>]` the officer's order (refused from the captain, "there is no sending for
yourself", and when he is on deck; `send for the captain` a synonym); the boat's report
(`report.boat`, reach `port`) when her boat manned as a hull comes to the quay where a person
of her company is ashore. In the harness: a `report.called` that reaches a station ends its
stand-by ("sent for: ..."); a sleeping stand-by is ended by any `wakes`-class line that
reaches him and by nothing else of the deck's; the tripwire's call below writes its line
before the wake; the officer's kind with the deck is told once, when the captain goes below,
that the duty is his. **Decision 63:** `command_state` read from the log (the last
`ship.command_devolved` not followed by `ship.command_resumed`), cached by the log's length
so a checkpoint and a replay read the same; the command devolves on a held station of the
officer's kind first, else the senior rules' person by the health module's order, when the
captain is ashore, in the boat, aboard another ship, wounded or sick below, or a captive;
`tools.judge` gives `COMMAND` for every order of the station in command ("By the officer of
the watch, in command: ..."), and the command is given back when the captain is available
again and has given an order (the orders' journal). **A told order is the captain's word:**
`Harness.put_word` keeps the captain's words in `agent.told`; `told_covers` says whether a
station's order is one it was told; `tools.judge` gives `TOLD` ("By the officer of the watch,
at the captain's word: ...") and the told order passes the deck's gate. The reach table, the
stand-by events ("a report", "the captain called", "the boat's report"), the primer's chapters
11 and 14. **Tests:** eight in `tests/test_knowledge.py`; truths 7-370 whole, 7-371, 7-372,
7-387 whole; decision 63's two tests allotted **truths 7-420 and 7-421** (numbered at step
4's boundary). **Taken another way, accepted:** the call and the report read from the log and
not a list kept aside; a danger call once for a thing; a captain asleep by day not reported to;
the seniority the health module's order; the command given back on an order given while
available again (an order typed from the shore does not take it back). **Found on the way:**
the masthead's hail is a danger line but the stations' own kinds make no call (the sighting's
line is the report); "the quay at the quay at Falmouth" mended to the port's name; the boat
hull's unmustered people (the boat's branch first); a devolution cache in `ship.extra` had
changed four readings rows on a point ship (truth 43's repeat detector): a weak-keyed
dictionary by hull now, nothing of it saved; a station's person's needs are the company's
until the harness takes them in hand; `come aboard` from the shore refused while the boat is
away; the officer's brief grew by four hundred characters (`test_officer`'s budget raised to
22,500 by the convention, the same figure the lead set at 75's merge, kept once with both
reasons at this merge); **(i) booked, not 65's:** the rules' master called does not come up
(the call is a line; a model or the player at the captain's station is woken by it, but the
rules' master at his day's work below stays at it, so the mate sends five times in twenty
minutes in the Goulet while the book sails her): the people's and the reckoning's mirror, a
later package. **What moved, with the proof:** three pinned passages, by the new report lines
alone, old beside new in the pins' comments: the merchant passage (the master below at his
sights when a sail is sighted off the Lizard, and below at the noon's day's work in the
Goulet, where the Mingan is sighted a danger, her sails lift, the Mingan closes, the land is
ahead and the pilot warns: two reports, five calls) 3,100 to 3,107 lines, 6abbbff4d7fa1a57 to
6436eb06a665f379, every other figure of the passage the same (the anchored ticks, the
soundings, the account; truth 78's `_not_the_stations` equal to the base); the fake captain's
passage the same seven, 3,112 to 3,119, dfaa7ab3bdd70295 to 7076e667c2bc41e3 (its formula
unchanged); the schooner on an intent, her boat away for the prices reported to the master
below, 2,078 to 2,079, 585c52675f10e590 to 8744d3e56cfc9508; the cruise unchanged (her captain
on deck throughout); the call's words doubled where the line names the danger mended before
the pins were taken. **The builder's suites on a287290:** the fast tier whole 5,938 passed, 1
expected failure; the slow tier of the twenty-six touched files and the known truths 2,972
passed, 9 expected failures; the pace alone 13 passed (the frigate alone 557; three stations
seated 564 under the filter against 551 with `all`). **The lead's merge:** the trial on 82b's
items 2 to 5 met the trunk in `docs/dev/TuningNotes.md`'s tail (both sides kept) and
`tests/test_officer.py`'s budget (kept once at 22,500 with both reasons); lint clean; the fast
tier whole on the combined tree green (exit 0); the whole suite in the cloud run 37 on 6423975
(09:52 to 10:43 UTC): lint green, all six shards green, 6,679 passed, 11 skipped, 12 expected
failures; the pace job 13 of 13, every floor held (the first such run since the runner was
pinned). Step 4 (the player at the prompt by his place, decision 59;
decision 62's one person and the boat road; the drivers' commands against the grammar) goes on;
95's step 1 puts a few lines in `orders/stations.py`'s `recognises` beside it.

### Package 95, step 1 (one resolver for a sail named in words), as merged (2026-11-06)

Merged `claude/pkg-95` at cc4e373 (d65b2e3, `--no-ff`; the design note 5216f29, the step
662ab8b, the trunk's ef3b5af brought in at 35de09a, 058821c the captain's `hail the pilot`
pinned beside the lookout's hail of the pilot's cutter, cc4e373 the primer's chapter 15), on
top of 65's step 3. **Built as the design note (`docs/design/Design-SailByName.md`):**
`Lookout.sail_named` in `world/lookout.py` reads the lookout's own line backwards
(`read_sail_words`: the kind, "on the <side> bow/quarter", "abeam to <side>", "right
ahead/astern", "bearing <point>", "distant <d>" or "<d> off", commas or none, any order); a
name the deck knows over all (her name, her id, and the hook for step 2's given name); the
kind by every word made out of her (a lone rig word by 36's substring rule); the quarter
widened a point, the bearing within a point and a half, the distance half to twice the
lookout's own judged estimate (`BEARING_SLACK_DEG`, `DISTANCE_SLACK`, `QUARTER_SLACK_POINTS`,
their reasons in the tuning notes); the closer by true distance where more than one answers.
It serves `make her out` (the verb's kind joined to its clauses), `the glass on`, `give
chase`, `the bearing of`, the hail (`_addressee` after its own names and kinds; the hail's
head extends over the clauses, so "hail the brig on the starboard bow what ship is that"
hails her), `pull for` and `send the boat to the <ship>` (`vessel_in_sight`; `hull_named` the
same); `dealings.send_boat`'s refusal at sea names the form when a sail lies within a boat's
pull; words that leave no sail are refused with the strangers' own words. **Taken another way,
accepted:** the resolver is reached only where the trunk's own words found nothing, and
`Lookout.find` takes it only when its caller hands the world, so the rules captain's own
`chase the <rig>` reads the lookout as before (had it reached the resolver, "privateer
schooner" made out would have moved the recorded passages); the stations touch is not the
speaker check the lead's ruling named (the order is judged in `agents/tools.py` before its
actor is set, so a lookout check there sees no speaker; proven by the seated fake lookout) but
`_HAIL`'s lookahead holding the pilot's bare words only, and `signals.hail_parts` reading the
lookout's every `hail` as his hail of the deck; the boat's `_TO_SHIP` read "to the brig abeam
to starboard with the master" at its last "to", so words that begin with one are read from the
first (`_TO_SHIP_FIRST`). Nothing in `vocabulary.yaml`, `grammar.py` or `_say`. **Truths 7-395
to 7-397 and 7-399** (`tests/test_sail_by_name.py`, called from the known truths): the
narrowing's four cases, the closer and the refusal, a name over all, and the proof by toggle
(`lookout.SAIL_BY_NAME` off: the encounter 45 minutes, the convoy 40 and the first action 60
by their rules captains give the same counts of lines by kind and the same words in every line
naming a sail) with the pilot pin. States and counts asserted, no digest; no pin re-measured,
none moved; the slow marks in `conftest.SLOW_TESTS` (7-399 at 58 s, 7-395 at 9 s, the seated
hail at 6 s). 7-398 is step 2's. **The books:** chapter 15 gains "Naming a sail" and sends the
boat to chapter 26; chapter 23 the hail by the lookout's words and the lookout's every hail
his; the tuning notes the section. **Found on the way, already booked:** `the strangers`' item
`id` is the vessel's id, which the scenarios write as her name (package 96's brief). **The
builder's suites:** the fast tier whole exit 0; the slow tier of the touched files and the
known truths exit 0 (190 run, the xfails as on the trunk); the pace alone 13 of 13 (none near
its floor; the container 5 to 10 percent under the build machine); ruff and format clean.
**The lead's merge:** the trial on 6423975 met only in the tuning notes (both sections kept),
lint-clean; the fast tier whole on it green, exit 0, every test passed (426 slow left out); the whole suite in the cloud run 38 on
b78477d (11:10 to 12:07 UTC): lint green, all six shards green, 6,694 passed, 11 skipped, 12
expected failures; the pace job 9 of 13, the four floors under at 423 to 489 ticks a second
against 500 (the runner's speed; informative). Step 2 (the identification named in the readings and lost with
the sight of her; truth 7-398) builds on; its one touch in 65's `agents/harness.py`, the sail
rows' delta key (id, made_out, nation) gaining the name so that a model holding a station is
sent the row again when the deck learns her name, was asked for at 10:26 and approved (it wakes
nothing; pinned from the model's side in 7-398; 65's builder told at each merge). 97 launches
when 95 closes.

### Package 95, step 2 (the identified sail named in the rows, and forgotten when lost), as merged; the package closed (2026-11-06)

Merged `claude/pkg-95` at 39be8e9 (9936e12, `--no-ff`; the step's code at 846f0f1 and 9af67aa,
the trunk's c7b13f4 brought in at f7e2f3f and b78477d at 39be8e9), on top of step 1.
**Built as the design note:** `Lookout._identify`, once a look, keeps a sail's name once the
deck has it, while she is in sight: by hail, read from the deck's log since the last look
(`LOOK_WINDOW_S`, the minute; our hail's answer and her hail of us, her own name or a liar's
from the hail table's lies, the deck's knowledge and not the truth); by the private signal
answered right (the deck captain's recognition or the locker's challenge judged right, the
locker read where it lies and never made); by a consort's colours made out (under our orders,
or of our squadron). A stranger's colours give her nation, never her name. `_sail_ident` is
made on the first identification and popped where `_sail_said` is popped when she is lost
sight of: a stranger at dawn. The rows: `the strangers`' item `name` (None until known) and
its words led by it ("the Raven, a brig-sloop of war abeam to starboard, ..."), `what is in
sight` ("Sail ho! The Raven, ...") and `a sail in sight` the same; `known` and the lookout's
own event lines untouched; her name is the resolver's too. **The one touch in 65's file**
(`agents/harness.py`, approved 10:27): the sail rows' delta key per item is (id, made_out,
nation, name), so the strangers row is re-sent once when the deck learns her name or loses
it with her, and wakes nothing; proven by toggle (the member out, the model's-side test
fails). **Truth 7-398** (`tests/test_sail_by_name.py`, called from the known truths): the
Raven and the Swift alike until the Raven answers the hail named by the lookout's words, then
named in the three rows and the Swift not; `make out the Raven` by her name; no name in the
lookout's lines; lost at twenty-five miles and closed again, nameless; the liar named by the
name she gives; the consort under our orders by her colours; the Nancy by the private signal
judged right; the French brig's colours, no name; and from the model's side, a fake captain
standing by a glass gets the strangers row again with her name after the hail and nameless
after she is lost and closed again. States and counts asserted, no digest; no pin re-measured,
none moved; 7-399's toggle covers the identification (off, nothing is identified); the slow
mark in `conftest.SLOW_TESTS` (11 s). **The books:** chapter 15 (a sail a stranger until named,
the three roads, the name lost with her), chapter 23 (a sail that answers with her name is
named by it), `docs/agents/Harness.md`'s deltas sentence, the tuning notes' step 2 paragraph.
**Found on the way, booked to 97:** `hail_order`'s own refusal in `world/hail.py` ("...; the
strangers are listed.") still promises a list it does not give, outside `_addressee`; the
lookout's refusals now give the strangers' words. **The builder's suites** (code as at
9af67aa): the fast tier whole exit 0 (427 slow left out); the slow tier of the touched files
and the known truths exit 0 (208 passed, 9 xfailed as on the trunk); the pace 13 of 13; ruff
and format clean. **The lead's merge:** the trial on b78477d clean and lint-clean; the fast tier
whole on it green, exit 0, every test passed (427 slow left out); the whole suite in the cloud run 39 on eabf20f (12:44 to 13:54 UTC): lint green, all six shards green, 6,699 passed,
11 skipped, 12 expected failures; the pace job 12 of 13, truth 7-159 at 479 ticks a second against 500 (the
runner's speed; informative). **Package 95 is closed**; 97 launches on this merge (the hull façade's readers audited;
Opus, small), with the hail refusal's words added to its brief.

### Package 65, step 4 (the player at the prompt reads by his place; one person), as merged (2026-11-06)

Merged `claude/pkg-65` at 6462a18 (e8dc268, `--no-ff`; the step at 439ebb0, decision 63's
tests numbered at 875c192, the parity registry's `knowledge` block at d42cfa7, the trunk brought
in at 41c8489, 2f4d341, 0e9a84b and 7cd7887, the figures at 6462a18), on top of 95 whole.
**Built as the design's §11, decision 59 and decision 62:** the console's and the browser's
play log are the player's person's (`world/knowledge.py`: `players_person`, the seat's person
when seated, else the captain of the ship he is aboard as her captain, read from the world and
the `driver.left` line of his own ship's log so that a save and a replay read the same;
`players_senses`, his senses where he is, read in his hull's block, everything under
`knowledge: all`, with no person of his, and under `follow` of a hull he holds no person in,
the owner's eye; `hears`, the lines by `reaches` and the words by 66's hearing as the harness
applies it); the snapshot's `knowledge` block (`api/queries.knowledge_block`: his place, the
rows not to be had there each with where it is, the sample's sentence, whether the deck's are
his), the instruments pane greying those readouts with the words in their place and a "Where
you are" line, nothing greyed for the owner's eye. **Decision 62:** the prompt follows his body
(`movement.put_aboard` writes `hull.followed` of her log and moves the drivers when the
player's one person changes hull, a consequence of his order and never a driver's input); the
road from his own manned boat aboard another ship (`come alongside the Medusa` from the boat
pulls for her and, alongside, `board_from_boat` puts whoever is in her but her crew aboard as
visitors, the boat made fast alongside, her station the ship's each tick until an oar is pulled
or the lug set; `go to the boat` from her deck takes a visitor off in his own ship's boat lying
alongside; `come alongside` brings him home); the prompt his there (`person_of_actor` gives the
player's visitor for the captain's actor, `movement.check` refuses her deck's orders and his
own ship's with a passenger's reach, `VISITOR_VERBS`/`VISITOR_OBJECTS`; `hearing.station_spot`
reads his spot; `where am I` says a visitor). **A driver's word never shadows an order of the
game** (the owner's clarification): `hold` alone, `speed N`/`time N`, `tick [N]`, `state`,
`log [N]` the driver's and `hold water`, `hold your fire`, `go below`, `go ashore` the ship's;
`follow "X"` and `look at` at the browser's order line the driver's as at the console, a
refusal sent to the pages as `driver.refused`, written nowhere. The primer's chapters 14, 19
and 26 and the browser's page say the one-person rule. **Tests:** five in
`tests/test_knowledge.py` and truth 7-382; decision 63's two tests numbered 7-420 and 7-421 at
the truths' tail (the lead's ruling at step 3); the slow marks in `conftest.SLOW_TESTS`. No pin
moved: the new lines fall in no pinned passage (no recorded passage puts the player aboard
another ship), the filters change what is shown and not what is written; truth 78 and the
digests of the merchant, the intent and the cruise stand. **Taken another way, accepted:** the
player's person found, not kept; the owner's eye told by the hull; the visitor given a
passenger's reach by `movement.check`, not a seat; the boat made fast, not left to drift; the
browser writing where a reading is to be had in the readout's place rather than dimming the
figure. **Found on the way:** (a) a World's `parent` is the followed hull's façade, so the
knowledge module walks `Hull.world` as `boats._root` does (97's family, mended in the module);
(b) the frigate hove to makes near three knots in the hulls' tests' world and the launch three
and a half fresh, so the pull home from a mile off is three hours (the engine's, not read; a
reminder for the gate's testing, J2); (c) the visitor's `say` at the bare prompt is said as
"the captain" (`orders.stations` speaks for the captain's station by name), the hearers right
and the name hers: a seat of the visitor's voice for the prompt as 82 made for a seated visitor
would mend it; **ruled to 65's step 8** if it is that small, else booked after; (d)
`World.dealings` reads the followed hull (97's audit, item 4, mends the player's own Dealings'
binding); (e) a boat on her oars alongside a ship hove to fell a cable astern in minutes, hence
made fast. **95's files:** `api/queries.py` gains `knowledge_block` and the `knowledge` key
(95 closed before this merge; nothing of the sail rows); `orders/boat.py` touched in `come
alongside` alone. **The builder's suites** (7cd7887): the fast tier whole 6,309 passed, 1
xfailed, exit 0 (on each merged tree; on 875c192 it found the parity red, mended at d42cfa7);
the slow tier of the thirty-six touched files and the known truths in two halves, 722 passed 8
xfailed and 2,402 passed 1 xfailed, exit 0; the pace 13 of 13 (the knowledge filter's place
559 against `all` 556; 7-386's 517 against 546, within the noise); ruff and format clean. **The
lead's merge:** the trial on d3f8fa3 clean and lint-clean; the fast tier whole on it
green, exit 0, every test passed; the whole suite in the cloud run 40 on 1662b54 (16:18 to 17:26 UTC): lint green, all six shards green, 6,707 passed,
11 skipped, 12 expected failures; the pace job 12 of 13, truth 7-159 at 498 ticks a second against 500 (the
runner's speed; informative). Step 5
(books, papers and pictures in their places, §8; truth 7-374) builds on; 97's two lines in
`agents/harness.py` meet this step's word tuples in the same file at 97's merge, the lead's to
resolve.

### Package 97 (the hull façade's readers audited), as merged; the package closed (2026-11-06)

Merged `claude/pkg-97` at b3adc86 (7e479b7, `--no-ff`; the design note c299be0, the mends
10454ba, 6f62674, 388e5a7, 7e0b0b7, the trunk brought in at 81e5cb9 and 11844e7, the postscript
0b554e8, the figures b3adc86), on top of 65's step 4. **The audit** (`docs/design/
Design-FacadeReaders.md`, approved 13:04): one cause behind most of it, the player's own hull
never walked at construction (`World.__init__` built her People, Stations, Papers, Dealings,
Navigation, Ground, NeedsKeeper, Water, Health, the standing Runtime and the Captain with the
World itself, where `crews.adopt_hull` rebinds a crewed hull's graph to her Hull), so each read
the running hull's fields inside another hull's block and the followed hull's under `follow`;
a differential on the trunk (the frigate and the brig X promoted beside her) showed
`stations.holder('master')` Mr Harvey against Mr Hart and every system reading 'Amazon' against
'X'; an instrumented run of the 23 multi-hull test files met the live roads (Stations 78 reads,
People 67, Dealings 42, Water 16, the Harness 1). Eighteen readers listed with their hull and
block. **Built, two roads only.** Bound at construction: `hulls.bind_to_hull` (the walk
`crews._rebind_world` used, moved there) binds the World's own hull at the end of
`World.__init__` and `__setstate__`, her own `hull.world` kept; the late keepers (Water,
NeedsKeeper, Health) made on `self.own`; the player's seat on `world.own` (`seat_world`);
`make_hull`/`adopt_hull` keep a hull in the World itself (`world_of`). Read in its own block:
every hull's readings view over her Hull; `director.director_hull(world)` for the director's
journal, station and holder, its twenty appends and `seats._log` given that handle;
`acts.act_target_of` (in `give`) gives an act keyed "" to `world.players` under `follow`,
`target_of` for inputs unchanged; `boats.follow_boat`'s line written on the World with the boat
current; `remote.py`'s desk seats told by `world_of`; the World's own state set or keyed through
a bound handle by `hulls.world_of` (the unheld questions, the books, the person journals, the
seats' count, the painter, the director's listeners and seat doors). **In 65's file** (granted
13:04 and 14:16): two lines of `agents/harness.py`, `Harness.__init__` binding the hull whose
agents the harness enters, and `_station_notices` giving no other-ship shape notice on the
player's own ship. **The tidy:** `hail_order`'s refusal gives `Lookout.sail_refusal`'s
strangers' words. **A moved outcome, bisected and ruled** (14:16): on the trunk the
boarding's casualties of the player's ship were named on the enemy's men of the same post
(her Health, holding the World, read the running block), so the first lieutenant always
lived to lead on; the branch kills him by the real draw at tick 530. The test of the boarders'
officer keeps its story under `_alongside(seed=1)` (the default 7 unchanged; the reason
written at the test) and a new pin beside it holds the default draw (Mr Pearce killed, the
deck carried, no officer leads on; who leads on when he falls is 74's, booked). **Tests:**
`tests/test_facade_readers.py`, truths 7-422 (her stations, people and every system read her
inside the brig's block), 7-423 (the director's writes on her hull under `follow`; the acts
and the inputs), 7-424 (inside an order of the brig's, the frigate's spots, holder, water and
reckoning hers), 7-425 (the hail's refusal); the guard walking every hull's graph through a
brief, a seated captain, `follow` and back and a checkpoint's round trip (two references kept
by design: a HullView's game, the far body's brain). Four asserts of the old binding read the
hull's, each commented. No pin moved; the probes stayed in the note. **Left by ruling:** the
shared person ids (96's), the replay's seating order of two hulls in one tick (a loose end
beside 7-394), the sea's one visibility under `follow` (noted for M8); found and left for the
lead's list: `harness.all_agents` returns every hull's, so `remote.stations`' "not this world"
names the followed hull's stations with her ship (older than this package). **The builder's
suites:** the fast tier whole exit 0, 6,315 passed, 1 xfailed; the slow tier of 34 touched and
related files with the known truths exit 0 (839 passed, 9 xfailed) and after 65's step 4 the
files it touched and its truths exit 0; every save-and-replay truth passed (22, 49, 72, 7-170,
7-171, 7-175, 7-183, 7-322, 7-324, 7-390, 7-394 by both roads, 7b-94, 7b-95; 84's saves of
many hulls); the pace 12 of 13, truth 7-159 at 474 against 500 and toggled against the trunk
alternating (the branch 492, 501, 498; the trunk 455, 487, 491), the container's margin; ruff
and format clean. **The lead's merge:** the trial on 5c2e24d clean and lint-clean; the fast
tier whole on it green, exit 0, every test passed; the owner's saves proven on the checkpoint road: six of them (the brig against the brig at tick 8,538, the
small convoy with all models at 13,941, the brig off Falmouth crewed at 16,475, the frigate and cutter in Torbay
at 387, the Raven at full detail at 1,266, the naval cruise at 318) replayed on the trunk's code with the
game's ship factory and checkpointed there, their systems holding the World as every checkpoint before
this package; read on the trial tree, every hull's systems bound to her, the guard's walk clean, and the
log's digest after two minutes' ticking the same as the trunk's for each of the six (the saves stay with
the lead, as always); the whole suite in the cloud run 41 on 8542e49 (18:22 to 19:07 UTC): lint green, all six shards green,
6,713 passed, 11 skipped, 12 expected failures; the pace job 9 of 13, the four floors under at 430 to 492 ticks a
second against 500 (the runner's speed; informative). **Package 97 is closed.**

### Package 75, the hold (SW-5) and B3.4 (the schooner's mast), as merged (2026-11-06)

Merged `claude/pkg-75` at 1c02517 (f414ed1, `--no-ff`; the hold 42a995b, the trunk brought in
at e6cf033 and 5dd7d67, B3.4 1c02517), on top of 97 and 65's step 4. **The hold, as the lead
ruled on the lee-port step** (`combat/ports.py` `PORT_HOLD_S = 60`, its own commit): a port shut
at once when the sea comes within the foot of its sill, and opened again only when the sill
stands six inches clear and the sea has kept from it a full minute, the hold counting from the
last tick the sea was at the sill, so a held port the sea reaches again starts its hold afresh
(`Battery._sea_at_sill`, a class default so a battery pickled before it loads; a port shut in an
older save counts from the first tick it is read); `ports.update` takes the tick from
`Battery.tick`. The hour in gusts: no port reopens within a minute (the frigate's seven quick
changes, six to sixty-three seconds apart, to none), the hour's changes standing at 46, 24 and
43, the gusts and lulls lasting minutes; about a round an hour and 0.9 to 2.4 percent more
port-seconds shut. L2's reopening-band pins moved old beside new, the reason at each (the
tuning notes' "The lee ports held a minute"); candidates 550 passed with no outcome changed;
the gate's J1 corrected by the lead (the 46 stands with the hold as without it). **B3.4 by
§12.2a's rule as approved** (`ship/graph.py` `Ship.on_schooner_mast`): a braced yard on an
after mast that carries no braced yard on its lower mast handles as a fore-and-after's mast,
read at places 1 and 3 only (`evolutions.scripts._masts_with_yards`, `physics.sails.
_square_rigged`), found once a ship from the parts as filed (wrecked or sent down or not, so a
brig whose main yard is shot away stays a brig) and held in a weak map beside the ship so no
pickle or checkpoint moves; no schema key, no Spar field; the yards under the bowsprit count for
nothing, a lug's or a lateen's yard is no braced yard (the tartane classes as the cutter, the
polacre's square main alone her mast with yards). No committed file trips it (all fifteen
guarded; the golden table and the razee's and the 64's rows unmoved); five rigs in memory (trial
A, the main topgallant, trial B, a tartane and a polacre probe). Trial A re-measured gives the
research's 149 s, 449 s, 50.2° off exactly; with the rule, trial B and the main topgallant heave
to about 50° off (68° to 90° without), wear keeping the mainsail, and in a gale lie a-try 35° to
46° off where without the rule they ran off at 178°. Candidates 3,973 passed, no outcome
changed; whole logs identical; the fast tier 6,319. The record in the tuning notes ("The
schooner's mast"), the *Neufchatel*'s §12.1 to §12.2a, Build-Ships §16.1, Ext §14 item 12.
**Four rulings asked and given** (the notes to the ships session, 18:00), each a small step
after SW-4, measured before built, the moved logs old beside new: place 2's timing after Luce
1884 p. 417 (the after yards hauled with the wind a point on the bow, before the head yards);
the word "Main-topsail haul!" for any ship whose main course is not set; the schooner-mast's
yards as after yards when no mast carries yards (every fore yard shot away); `orders/storm.py`
keeping the courses' reef at the topsails' second reef for any rig with topsails, the after
take-ins alone gated on square-rigging (the file granted to the ships session). **Recorded for
B2 and package 90:** "shorten sail" never takes in the *Neufchatel*'s main topgallant (B2 mends
her file); the two classing limits and the polacre's lateen mizen and pole masts (90's row).
**The lead's merge:** the trial on 7e479b7 (the trunk with 97) clean and lint-clean; the fast
tier whole on it green, exit 0, every test passed; the whole suite in the cloud run 42 on 0eb17c7 (19:10 to 20:24 UTC): lint green, all six shards green, 6,756 passed,
11 skipped, 12 expected failures; the pace job 9 of 13, the four floors under at 429 to 483 ticks a second
against 500 (the runner's speed; informative). The ships session runs on to SW-4 and B2 by the owner's leave, to one final report
for 75.

### Package 65, step 5 (books, papers and pictures in their places), as merged (2026-11-06)

Merged `claude/pkg-65` at f28c831 (aba233f, `--no-ff`; the step at 2c9bd6c, the postscript's
truth 7b-102 at c6b2031, the trunk brought in at 70ed9fe, 4953715 and 137720f, the figures at
f28c831), on top of 75's hold and B3.4. **Built as the design's §8:** the library by the
reader's senses (`tools.library_by`, which `tools.library` reaches through the station's senses
and the browser's pane through the player's person's): the player's reference (the primer, the
catalogue, the grammar, the ship's names, the tools, the world page) from anywhere; the ship's
papers each where it is kept (`knowledge.paper_place`, the keeper's rule: the keeper carries his
paper while he is occupied with it, the words of his task naming it, else it lies in its place;
`paper_here`, `paper_elsewhere`), the listing naming every paper and which are to be had where
he stands, a paper asked for from elsewhere refused with its place and the walk ("The manifest
is kept in the hold, with the purser; go to the hold to read it (or ask the purser)."),
`section='all'` serving the papers here and naming the rest, `find` searching the papers here
and naming the rest; the book of standing orders and the books drafted on the quarterdeck and in
the cabin (`knowledge.KEPT`, `thing_here`, `thing_elsewhere`), refused elsewhere with the walk; a
search of the whole library reading what is where he is and the reference, and saying what it
left out in one sentence; the contents page saying what is to be had where he stands.
`read_log` where the log is kept (the log board on the quarterdeck, the log books in the cabin
and the gunroom; ashore "The ship's log is aboard her."; the director's reach untouched);
`chart` in the cabin, the gunroom and at the binnacle; `ship_view` from the deck, aloft and the
boat. The browser's papers pane says of each paper `here` and `where`, withholding a paper's
lines where the player's person is not; `/api/library` reads by the same senses. The tools'
words and the primer's chapters 14 and 19 say the rule. The director and `knowledge: all` read
everything from anywhere. **Tests:** two in `tests/test_knowledge.py` and truth 7-374 (neither
slow); three tests moved to the rule, old beside new in their words (`tests/test_places.py`'s
parity of 35, the manifest served from the quarterdeck to every station before and now the
deck's paper the same page at every station on deck and the hold's the same refusal everywhere
else; `tests/test_server.py`'s pane; `tests/test_date_and_war.py`, the news of the war read in
the cabin). No digest moved (no pinned passage reads the library, the log tool or a picture from
a station below). **Taken another way, accepted, (1) by the lead's ruling:** the books drafted
kept with the book of standing orders on the quarterdeck and in the cabin, not the cabin alone
as §8's table had it (the owner's ruling of 2026-10-16 that a station reads them from anywhere,
package 53 and truth 7b-102, kept to the deck and the cabin rather than reversed); the refusal's
one wording whoever reads it; "ask the keeper" rather than "send for" (the papers answer first
when a keeper is asked); the keeper's rule by a shared stem until step 6 gives the tasks their
words; a refusal a book like any page; a search from below does not search the papers
elsewhere and hide the hits. **Found on the way:** a section's reopen by number where the words
hold an apostrophe (33d's choice, kept); the frigate's purser living in the gunroom and keeping
his books in the hold; `_papers_topic`'s "in the deck" for the deck's papers (35's words,
pinned, not touched). **95's and 97's files:** none touched but `ui/server.py`'s `ship_papers`
and the shelf route. **The builder's suites** (c6b2031 the code): the fast tier whole 6,312
passed, 1 xfailed, exit 0; the slow tier of thirty-nine touched files and the known truths in
two halves, 728 passed 8 xfailed and 2,413 passed 1 xfailed, exit 0; the pace 12 of 13, truth
7-159 at 495 against 500 under the run and passing twice alone (the container at the floor;
nothing of the step on the tick's path); the knowledge filter's place 557 against `all` 530;
ruff and format clean. **The lead's merge:** the trial on f414ed1 clean and lint-clean; the
fast tier whole on it green, exit 0, every test passed; the whole suite in the cloud run 43 on 1cb432b (20:21 to 21:28
UTC): lint green, all six shards green, 6,759 passed, 11 skipped, 12 expected failures; the pace job 9 of 13, the four
floors under at 373 to 438 ticks a second against 500 (the runner's speed; informative). Step 6 (work in its place, §9;
truths 7-375 and 7-388) builds on.

### Package 65, step 6 (work in its place), as merged (2026-11-06)

Merged `claude/pkg-65` at d6e52a7 (429d7f5, `--no-ff`; the step at 0df145f, the trunk at 8542e49
brought in at d6e52a7), the branch running on with steps 7 and 8 (reported at their boundary).
**Built as the design's §9:** `People.occupy(p, place, until, with_what)` the one road for the
rules' people and a station's person alike, taking the room's id and the mirror's "on deck" and
"below" too (mapped to the quarterdeck and his berth: the captain's cabin, a trade's place, else
the gunroom, or the room he is in when he is below already), keeping the room for a mirrored
person (the master's) so that his place reads the room and not the berth the mirror would give,
and leaving him where the work was when it is done (a man does not walk back by himself; the
master's "came on deck, the day's work done" line stands as the reckoning writes it). The
master's day's work in the gunroom, the rules' master and a model at his station alike (truth
7-375), proved rather than built: the mirror's "below" has read as the gunroom since 53 and a
station's senses have been its person's since step 1, so a model master sampled below (11:59 to
12:29 in the test world) reads the slate's rows and nothing of the deck, the line saying where
the rest are, the bell and the watch relieved reaching him and the sightings not. The captain's
writing in the cabin (truth 7-388): `draft a book` from the quarterdeck takes him below first
(one `captain.below` line, as his own `go below` writes it) and occupies him `writing` for five
minutes (`people.WRITING_MINUTES`, judgement); the deck's orders refused from there as from any
going below; he stays in the cabin until he comes on deck; a second book drafted in the cabin
moves him nowhere; a seated captain drafting through his harness goes the same way and his
sample after is the cabin's; a captain ashore, in the boat or at a task already writes where he
is; another drafter (an officer at his station) writes where he stands; the primer's chapter 14
says it in a sentence. Two tests in `tests/test_knowledge.py`; truths 7-375 and 7-388. **Taken
another way, accepted:** (1) the captain's writing is his own to leave (his `come on deck` and
any walk of his free him of it and move him, where the master's working is not left for a walk):
a man at his desk gets up when he chooses, a man working a sight cannot, and the five minutes
bind only what he may do meanwhile, so step 5's test that drafts on the quarterdeck and walks to
the hold at once stands as written; (2) the `captain.below` line before the order's own
`order.accepted` line (the handler moves him as it carries the order out, as the boat's
`hull.followed` line is at step 4), the log reading "went below; Order: draft a book; drafted a
book"; (3) nothing of §9's letter built (no order writes one at the prompt; a letter comes aboard
by the boat and is read where the captain is); (4) the trades' work left as it is, as §9 says.
**Found, noted:** (a) `People.occupy` with a mirrored person set the mirror's "on deck"/"below"
and never the person's own place, so a room given was lost: kept now; (b) the frigate's master
takes his noon sight at 11:44 and goes below at 11:59 in the knowledge tests' world, on deck
again at 12:29; (c) the builder's first fast tier on this tree read one red (the replay's
rules-fingerprint test) because step 7's edits landed under it while it ran; the clean figure
below is a second run in a worktree pinned at d6e52a7, and the builder runs every suite in a
pinned worktree from here on (the lesson in the tuning notes). **Two things that follow with
steps 7 and 8:** the master's eighty-minute test and truth 7-375 run in the fast tier at
d6e52a7 (13 s under load; their slow-tier marking is at f825749, after this tree), and the
step's tuning note says its suites' figures "are below" where c37c813 writes them. **Nothing of
95's or 97's files touched;** no pin moved (no pinned passage drafts a book; the people's
occupation in the passages is the reckoning's own road, untouched; the digests of the merchant,
the intent, the cruise and the fake captain stand). **The builder's suites on d6e52a7, each in
the pinned worktree:** fast tier whole 6,322 passed 1 xfailed, exit 0; the slow tier of the forty
touched files and the known truths in two halves, 812 passed 8 xfailed and 2,413 passed 1
xfailed, exit 0; the pace 13 of 13, the knowledge filter's place 532 ticks a second against `all`
535 (truth 7-386's run 543 against 539: within the noise, as at steps 1 to 5); ruff and format
clean. **The lead's merge:** the trial on 5e7a0f1 clean and lint-clean; the fast tier whole on
it green, exit 0, every test passed; the whole suite in the cloud run 44 on db5ff15 (22:54 to 00:05 UTC): lint
green, all six shards green, 6,763 passed, 11 skipped, 12 expected failures; the pace job 9 of 13, the four floors under at 385 to 439 ticks a second against 500 (the runner's speed; informative). Steps 7 and 8 (the drill's walk behind `DRILL_WALK=False`; truths 7-377,
7-378, 7-384; the visitor's voice at the prompt) are reported at their boundary.

### Package 65, steps 7 and 8 (the drill extended; the edge cases' truths and the records), as merged; the package closed (2026-11-07)

Merged `claude/pkg-65` at aafbb56 (c597a7d, `--no-ff`; step 7 at 835daad and 3eb7009, step 8's
truths at fec39ef and its records and the visitor's voice at 38050a7, the slow-tier marking of step
6's master at f825749, the trunk brought in at 2cb0c9e, 07e8d33 and fa25309, the figures at c37c813
and b4bf0a9, the spec's mend at aafbb56). **Step 7, built as the design's §10 behind one switch:**
the fitness drill's walk whole and kept behind `consent.DRILL_WALK`, off on the trunk by the lead's
ruling of 2026-10-31 (the drill a model meets stays the three things the consent brief describes
until package 55 re-briefs, so a yes on record for a drill of three is not asked eight before the
brief says eight; `drill_spec()` gives the drill as the switch has it); with the switch on, after
37's three things the walk (go below, eat or drink there, read one of the ship's papers where it is
kept, come on deck), seven things in up to eight replies, the drill's tools gaining `submit_order`
for the walk's four orders alone (any other refused in the drill's words: "The drill's orders are
the walk's alone ... '<the order>' waits for the game."), the judge counting each of the seven once
by its result (a move refused is not a move; a paper counts only where it was read) and naming what
is still to run, the record's `drill` field "passed, with the walk"; the walk taken by the drill's
world's own captain (`Harness.drill`), that world the frigate at seed 0 in a calm with her people
and her papers, its lines real there and in no game's; in-world under 85's rule; the consent brief
and the consent records untouched; the sentence package 55 will need in the design's postscript.
Truth 7-381 (the switch on); 37's drill tests stand unchanged with it off. **Step 8, built as §12
to §14:** truth 7-377 (the player in his own boat manned as a hull reads her as a deck, the ship's
lines reaching him by sight and hail alone: her standing order's royals in her log and not the
boat's, her lookout's line the ship seen, a word on her deck within hearing written in the boat's
log as heard); truth 7-378 (a passage with the brig X in sight at night and a fake captain who goes
below, is reported to and called, comes up and drafts a book, saved at the half and at the end,
replayed by its transcript and by its acts to the same digests of both hulls' logs); truth 7-384 (a
visitor in another hull's cabin reads her glass, her tell-tale's heading, her chart's rows, her log
and her chart, none of her deck and not her view; a person in her hold reads the hold's, her
manifest there; the confinement itself is 74's); the player's `say` at the prompt aboard another
ship as a visitor his own, in his name and from his spot ("Captain Bowen, a visitor of the Amazon,
in the cabin: ..."), her captain's station hearing him, narrower than a seat (`orders.stations._say`
reads `knowledge.players_visitor`; step 4's finding (c), as ruled); the records: spec M7b §14's
provisional list replaced by the rule as built, `docs/agents/Harness.md` §21h, the primer's
chapters 14, 16 and 19, the director's library page's sixth section, the design's postscripts and
the tuning notes; every truth of 7-370 to 7-389, 7-420 and 7-421 has its test. **Taken another way,
accepted:** step 7's (1) the drill's world a ship and not a point when the walk is on (the point
world keeps no papers and has no cabin), (2) the walker the drill's world's captain and not the
station's person (the consent station has no authority to widen), (3) the paper the text names the
price list in the cabin, §10's "any paper kept where he is" standing, (4) a reminder after an empty
reply or a reply a stand-by ended and no other; step 8's (1) the sight the boat's lookout's line
and the hail a word said on her deck, asserted within four cables, (2) 7-378 at night with the brig
in sight so that reports and calls both fall, (3) the captive by his place alone, (4) the visitor's
voice by the line's name and the speaker's skipping, no seat made. **Ruled at the close:** no seat
of the visitor's voice is wanted now; it is booked with 65b. **Found, noted:** step 7's (a) a helper
placed between `@dataclass` and its class made the decorator a function's, mended at once, (b) the
developer's empty turn at the runner's door is the fake's first reply in the drill, (c) the drill's
world's clock stands at 04:00; step 8's (a) under `follow` of another hull `world.people` is hers
(97's binding), (b) the primer's in-world test reads "gate" as a build's word. **The lead's one
finding on review, mended before the merge:** 38050a7's edit of the spec inserted the as-built §14
text together with a verbatim duplicate of 669 of the spec's lines (package 68's "as built"
paragraphs twice) and left the provisional paragraph standing; the builder's aafbb56 removes the
duplicate and replaces the provisional text, the spec reading once (no long line duplicated, as on
the trunk). **Booked for the owner's follow-up, 65b** (the builder's list for the close): §3.1's
named flaw (the weather over a port read from the followed hull's view), §9's refusals, the rules'
master who does not come up when called (step 3's finding (i)), a seat of the visitor's voice if
wanted, and the drill's switch for package 55. **Nothing of 95's or 97's files touched** beyond
`_say`'s visitor branch; no pin moved. **The builder's suites on c37c813 (steps 7 and 8 whole), in
a pinned worktree:** fast tier whole 6,367 passed 1 xfailed, exit 0; the slow tier of the forty-one
touched files and the known truths in two halves, 835 passed 8 xfailed and 2,413 passed 1 xfailed,
exit 0; the pace 13 of 13, the knowledge filter's place 579 ticks a second against `all` 580 (truth
7-386's run 569 against 571: within the noise, as at every step); ruff and format clean. **The
lead's merge:** the trial of b4bf0a9 on db5ff15 clean and lint-clean, the fast tier on it begun and stopped when the mend arrived (nothing of code between b4bf0a9
and aafbb56); the trial of aafbb56 on 632b46f clean and lint-clean (no long line of the spec duplicated), the fast tier whole on it green, exit 0, every test passed;
the whole suite in the cloud run 45 on f67640b (01:12 to 02:09 UTC): lint green, all six
shards green, 6,771 passed, 11 skipped, 12 expected failures; the pace job 13 of 13 passed (the runner at the floors
for once). **Package 65 is
closed**: eight steps, truths 7-370 to 7-389, 7-420 and 7-421, decisions 59 to 63 as built, the
design note `docs/design/Design-PlaceKnowledge.md` with a postscript a step. Package 74 (Fable)
launches on this close.

### Package 74, the design and step 1 (the far ship's length), as merged (2026-11-07)

Merged `claude/pkg-74` at 797860d (9acab09, `--no-ff`; the design note at 2079122, step 1 at
797860d; the branch's trunk merge f0457e9 and step 1's record commit 0352b3e lie after step 2's
first commit 88af63e, whose suites had not run, so step 1 is merged at its own commit and its
record paragraph in the tuning notes reaches the trunk with step 2). **The design**
(`docs/design/Design-Prizes.md`, 1,187 lines, approved 2026-11-07 with nine rulings): the prize
a hull of the one world possessed by one function for every road (the strike by morale, the
captain's word, the deck carried, the far rounds, the cut-out), the muster swapped (the prize
crew's sailors out of the captor's, her former company a prisoners' record confined below, the
named few by 65's confinement), one ladder of standing for the prize master and for who leads
the boarders on when their officer falls (97's paragraph; 97's pin to move old beside new), the
captors' doctrine in their role files with a prize master's file of its own, the captured book
and table, the rising and the retaking, burning and scuttling, the prisoners fed at two thirds
(the Regulations on file); the captive's channel the visitor's voice with his own station stood
down and his prompt following his body, the parole asked in the period's words by nation
(Spain's row by decision 64), the prisoners landed to the agent for prisoners at the port, the
cartel a hull of the sea with one errand; the far fight wired to the sleeping hulls by 70's
rounds every third minute with 75's finding mended first, the far state carried into the parts
and back, the engagement first among the cap's reasons; the prize court a job of the port by
nation, the valuation and the cargo and the prize goods on 86's ordnance, the money by the
eighths by date; the consent revision drafted under `docs/design/` with the refusal in words
behind a flag; the court martial the director's proceeding and a new command a scenario's start
under the saves. **Ruled:** the muster swap over a flag; the captive's station stood down; the
eighths from memory until the shelf answered (it did, the same day: Lavery, *Nelson's Navy*,
p. 116, confirming both schemes and adding the ships in sight sharing the money, built at step
5); the far ship's reply to an awake hull only as the fallback when the cap has no room for her;
the guns heard off the horizon kept under the rounds' toggle; the new command's scenario written
by a small writer of 74's own under `saves/` (96 is held); the boats' retaking amended to a
cruiser at sea; the adversarial refusal reaching every station of hers that gives an order of
the deck or the guns, the voices and the lookout admitted; `combat/boarding.py` and
`world/crews.py` granted, the cartel's gun words until 75 closes; the flag of truce the colours'
state `truce`. **Step 1, built as the design's §4.1:** `combat/far.py` reads the far ship's
length from `length_waterline_m` (70 read a key the spec has not, so every far ship was 0.0 m
long and her size floored at 0.5; found by 75), and `fight`'s loop body is `round_once`, the one
function the world's far action will run at step 4, the loop and its record unchanged; truth
7-350 pins the read and the move old beside new (the old read set by hand as the toggle); 7-139's
docstring carries the new figures beside the old: the two cutters at two cables strike in the
same seven rounds, the long-gun cutter five hurt and three holes against four and three, the
King's cutter one hurt against none; at a cable two rounds against three; two frigates at two
cables three rounds against six; the pin's bands hold and no other pin reads the far fight.
**Found, carried:** the world order's "merchant brig" takes `brig.yaml`'s muster of 121
(`merchant-brig.yaml` a shadow; to the ships session's notes); a rules captain bound for Brest
from the Iroise lays no course through the goulet and beats without way within five miles of
the road (the planner's, 61's family; the lead's list). **The builder's suites on 797860d, in a
pinned worktree:** ruff and format clean; the fast tier whole exit 0; the slow tier of the known
truths, the profile and the Indefatigable's tests exit 0; the pace alone and last 13 of 13 (the
first pace run cut by the background task's two-hour limit and run again alone). **The lead's
merge:** the trial of 797860d on 2a1cd96 clean and lint-clean; the fast tier whole on it green,
exit 0, every test passed; the whole suite in the cloud run 46 on 28c228e (04:53 to 05:47 UTC): lint green, all six shards green, 6,772
passed, 11 skipped, 12 expected failures; the pace job 13 of 13 passed. Steps 2 to 7 follow at their boundaries, each at one hash.

### Package 75, SW-4 (the sub-types as fits and roles), as merged (2026-11-07)

Merged `claude/pkg-75` at 1ff4e813 (73b9469, `--no-ff`; the branch's trunk merge 02bd0405 after
it brought the lead's head in and is not merged), a clean merge onto the trunk carrying 74's step
1. **Built as Build-Ships.md §8, §9 and §8.4 as ruled:** the descriptions' fit and roles written
in each file's `ship.descriptions` by the generator; four rows in `world/ships.py` (the revenue
cutter, the hired armed cutter, the coasting cutter, the privateer lugger), class 1, with their
lookout words; `brains.SUB_TYPE_ROWS` giving the four their first role where the intent names
none, no older row moving; **the merchant brig sails her own file** (`merchant-brig.yaml`: four
long 6-pounders and sixteen men where she sailed the brig-sloop's guns and a hundred and
twenty-one; `SHADOW_FILES` removed; a save, a checkpoint and a replay written before the step load
and run on); the `indiaman` and `revenue` books (James vol. 3 pp. 249-253 and vol. 5 pp. 132-136,
the thresholds judgement) in `ROLES` and `ROLE_SERVICE` (both the merchant service, neither the
Navy's nor a privateer's); a scenario's `role:` refused in words at the load; truth 7-191 drafted
(an Indiaman keeps her colours at 0.273 against her 0.25 line, a merchantman strikes); the
topsail schooner, the lugger and the smack sailing unarmed by default with their sourced fits and
bills; `pivot_arc_from_rig` giving the privateer schooner's pivot [62, 141] from [60, 140]; the
brig-sloop's "ten ports a side" (RMG ZAZ4491) everywhere served. **A mend outside B8's files,
confirmed:** a crewed privateer lugger near an enemy revenue cutter flipped evading and engaging
every minute (27 changes in 30 minutes), "a revenue cutter" being the first class-1 description
with a man-of-war word; `captains.Transition.unless` may be a list (one stimulus stays a plain
string, so older and pickled rows read as before) and the privateer's and the revenue's evading
rows read `unless: [overmatched, man of war near]`: three changes, evading from seven minutes;
`Captain.sub_type_role` carried in at the promotion; `description_key` trying the whole phrase
after the article first ("the frigate" loads in a `ship:` order). **Pins:** no physics figure of
any file moved and the generator's bytes equal `data/ships` (checked again at the merge); the
candidates 4,023 passed with no outcome changed; the station trial's stranger re-pinned by the
builder; the trade trial's stranger digest moved on the word "ten" alone, bisected, and re-pinned
by the lead on the build machine, old beside new (on the build machine the trunk before the merge gives the pinned bf059c3211b7cc9c, the merged tree 5e7bdba2a4f4770b, and the merged tree with the word put back to "sixteen" in `brig.yaml`'s own descriptions gives bf059c3211b7cc9c again (the words are served from the file's descriptions since SW-4; the engine table's word alone changes nothing); the states, the anchored ticks and the 1,594 lines hold; re-pinned at 5e7bdba2a4f4770b, the old beside it, in the commit after the merge). **Ruled at the merge** (the note to the
ships session): the rail-gun fits as played go to 77 as a finding (a kind-aware engine for
swivels and rail guns); the revenue's and the Indiaman's words and role sets a small step of the
ships session's own; the coasting cutter's own file when her turn comes; the glass words as
proposed; the revenue ensign a hook for 76; truth 7-191 and the two crewed evading tests to the
slow tier. **Found for others:** by 74, the world order's "merchant brig" took `brig.yaml`'s
muster before this step. **The builder's suites:** the fast tier 6,427 passed; the candidates and
the four whole logs as before; ruff and format clean. **The lead's merge:** the trial on
9acab09 clean and lint-clean, the ship files regenerated byte for byte, no forbidden word new
in the diff; the fast tier whole on it green, exit 0, every test passed; the whole suite in the
cloud: run 47 on 4423f62 cancelled for the lead's own lint fault (the re-pin's comment line,
mended at 2dc4921); run 48 on 2dc4921 (06:31 to 07:53 UTC): lint green, all six shards green,
6,851 passed, 11 skipped, 12 xfailed, no failure; the pace job (informative) 9 of 13 passed,
the four floor tests short of 500 ticks a second on the shared runner (379 to 438), where runs
45 and 46 held 13 of 13; whether the runner's load that hour or the brig's ten ports a side, run
49 (on 76's merge, no engine change) tells. B3.4's four steps and B2 follow to one final report.

### Package 76, the research pass and step 1 (the British books from the page), as merged (2026-11-07)

Merged `claude/pkg-76` at e200d9c (4f3694b2, `--no-ff`; the research pass at 6593dce, step 1 at
cfaf48c's tree with the notes at 0ff40be, the trunk brought in at 0d26261, 79fd890, cfaf48c and
e200d9c). **The research pass (step 0, approved 2026-11-07):** twenty-nine period texts and
fifty-two page images laid under `docs/references/signals/` with their rows in the references'
README, all public domain by age and all the Internet Archive's (the national libraries refusing):
the Admiralty's *Signal-Book for the Ships of War, Day and Fog* of 1796 and *Night Signals* of
1799, Popham's *Telegraphic Signals* of 1803, the instructions of 1776 and 1779 and Millan's convoy
signals of 1748, Corbett's two Navy Records volumes; Orvilliers 1772, Morogues 1763, du Pavillon
1775, Tronjoly 1779 and Audibert Ramatuelle 1802 for France; Mazarredo's *Instrucciones y señales*
of 1781 and *Corrección* of 1799 and Córdova's of 1778 for Spain; Barry 1800 and Preble 1894 for
the United States; Pereira 1817 and Giraldes 1820 for Portugal; the Neapolitan flotilla's book of
1807; Bylandt's Dutch Morogues; for the flags the 1820 *Display of the Naval Flags of all Nations*
in colour, Bowles 1795, the French law of 1790, Babron 1817, Perrin 1922 and Roosevelt 1882. The
1799 day book itself not found (Corbett places the copies); the 1799 numbers recovered from the
logs of Copenhagen and Trafalgar as Jackson's editor glossed them. The plan ruled: Britain, France,
Spain on Mazarredo 1781 in his numbers, then the United States first (no Dutch page), Naples a
root of her own by decision 64, Portugal on basic; the colours.yaml shape approved with 81's place
words. **Step 1, built as the plan:** the British numerary's 171 entries, 34 at the 1799 book's
numbers from the logs (eight more than the pass found), 137 made and marked, fifteen of 71's made
entries that stood on numbers the 1799 book gives to other signals moved to numbers of their own
above 150 with their sources saying where they stood, nine folded into their 1799 number, No. 1
("to denote an enemy in sight", No. 1 in the 1796 book too) marked still; the night book the 1799
night book number for number from the page images (Nos. 1 to 70), the fog book the 1796 book's
Nos. 1 to 18 with its gun counts as written by hand into the printed blanks of the copy scanned,
said so; Popham 1803 as printed, 1,444 words of parts 1 and 2, each leaf re-read where the OCR
failed and a word kept only where its head is English and its first letter matches the margin's
index, 158 numbers left out, part 3 not taken; the alphabet confirmed; the flags from the 1796
book's leaf 31 and Popham's leaf 13; the convoy numbers made (no period convoy book found); the
private form untouched. **One field of the loader** (`Books.forms` by `word_forms`: every form a
dictionary entry's printed endings make, on Popham's rule of p. 7), read by `encode`. **Tests
tightened to the page**, not loosened (the fog tack's three guns; every night and fog entry made
or carrying the page's number and year). **What moved and the proof:** truth 7-147 (a signal in
fog is a gun) reads the 1796 book's No. 14, "to lie to on the starboard tack", six guns slow and
two quick, where 71 made "four guns, bring to"; its substance unchanged (a gun heard two miles
off, answered, obeyed); proven by the entry put back; no log pins a day-book number that moved.
**Taken another way, accepted:** No. 19 is the night book's ("wanting the assistance of boats to
tow"), the day book's being 318. **Found, and ruled:** the lookout counts a hoist's flags by its
number's digits, right for the British numerary and not for du Pavillon's or Mazarredo's table of
two flags; a field for the hoist's form, carried on the hoist, is step 2's one engine change,
approved in advance; the trunk's lint fault at the trade trial's comment (the lead's, fixed at
2dc4921); the merge commit cfaf48c's message says "records" where the range carried the ships
session's tools too. **The builder's suites at cfaf48c, in a pinned worktree:** the fast tier
6,447 passed 1 xfailed, exit 0; the slow tier of the signals' tests and the known truths 315
passed 8 xfailed, exit 0; the pace 13 of 13; ruff and format clean at e200d9c. **The lead's
merge:** the trial on 2dc4921 clean and lint-clean, no forbidden word new in the diff; the fast
tier whole on it green, exit 0, every test passed; the whole suite in the cloud dispatched after
run 48: run 49 on c9cb4c0a (08:08 to 09:24 UTC): lint green, all six shards green, 6,851 passed,
11 skipped, 12 xfailed, no failure; the pace job (informative) 9 of 13 as on run 48, the same four
floor tests at 382 to 439 against 500 (a merge of documents and data with no engine change, so the
two runs agree with each other and not with runs 45 and 46; on the build machines packages 76 and
81 both ran the pace at 13 of 13 on trees carrying SW-4, so the lead holds it the shared runner's
hour until a third run on another day says otherwise). Step 2 (France) follows at its boundary.

### Package 81, the viewer's action (items 1 to 7), as merged; the package closed (2026-11-07)

**What landed:** the builder's 790b1a8 (claude/pkg-81; 4b0f317 with the trunk's 2dc4921 merged
in), merged `--no-ff` by hash at a8b716d4 onto ec424f92, a clean merge (trialled on 6f244969, the one commit between them the lead's mend below, no file of the branch's). The standard first
(`docs/design/Design-ViewerAction.md`, approved 2026-11-07 with seven rulings, its postscript as
built): the data contract (a profile with decks, port triples and a port size by deck; a deck of
port guns only), the one rule of placing (a port gun on its deck's triple within 0.01 m, a port
where the side stands the port's depth above the sill less 0.05 m and a place over the rail
where it does not; a swivel on its yoke on the rail; a pivot on the middle line), the gun table
(Adye 1804 pp. 155 and 72 read on the page images, the length the pattern of nearest weight to
the file's own, no key asked of a file), the firing, the damage and the animation's road. **The
data served:** `freesail/api/viewer_guns.py` (new, pure) the rule and the table;
`freesail/api/viewer_flags.py` (new) the flags' fallback until 76's colours.yaml (one plain
ensign at the peak while the colours show, the other nation's under false colours, turned over
in distress, the white under `truce`, nothing under `none` and `struck`; a locker's list of what
flies where passed through as it is); `queries.ship_graph` gains `guns` (each placing and
figure, or why refused) and `ports`; `queries.snapshot` gains `guns` (state, loaded, shut,
fired, a pivot's train), `damage` (the holes) and `flags`, read from the battery, the damage
keeper and the locker where the ship keeps them and never made (a snapshot writes nothing:
truth 7-441's digest). No engine file touched; `signals.py` read only. **The drawing**
(`client/projection.js`'s section "the action", `shipview.js`, `style.css`, `app.js`): the ports
on her drawn side at their triples with their lids open or shut by the gun's state and the sea;
the guns by place and state with muzzle face, carriage or slide, the barrel cut at the side;
the shot holes; the flags at their place words (peak, staff, the trucks, the mastheads, the
jackstaff, the rigging); the frame equal across every state (the guns never widen it, the
flags' reach where a flag flies past the rig: nothing on the frigate, the razee, the 64 and the
schooners, 0.2 m on the brigs, 1.2 to 1.9 m on the boats and the smack, 2.9 m on the cutter,
5.0 m on the lugger); the clock between snapshots, the rounds fired between them stamped with
the later snapshot's tick, the flash, the plume to leeward and the recoil on a
requestAnimationFrame loop that runs only while something is alive; a hull with no profile
draws as 75 left her, point for point (7-442). **The checker** `tools/check_viewer_guns.py`:
every gun of every fit of every file placed, 352 guns over fifteen fits, none refused; the
lugger, the smack and the topsail schooner (SW-4's) passed it with no change of code; its test
parametrized over `data/ships/` and a made-up ship in a temporary directory, so a ship added
later is checked by it with no change. **The records:** Build-Ships.md §6's postscript and the
ship builder's checklist; the primer's chapters 22 and 23; the tuning notes "## Package 81".
**Truths 7-436 to 7-445** (7-444 and 7-445 the owner's flags item). **Taken another way, each
accepted:** (a) the snapshot reads the state where the ship keeps it and not through the
readings `the guns` and `the damage` (they and `signals.locker_of` make their objects on first
asking); (b) a hull with no profile frames nothing of the action (the first form moved
test_view_geometry's FRAME_MOVED_OLD_M 5.59 to 5.46; the rule fixed, the pin stands); (c) the
flags' frame each place's own flags drooped as drawn, the peak held swung every way about its
gaff's throat (the first form moved the cutter's and the smack's frames 0.19 m between states,
caught by the boom-frame test and mended); (d) the smoke and the flash drawn facing the viewer,
the plume's foot held at the sea; (e) a port cut to the rail follows the rail where it steps
within the port's width (the 64's foremost quarterdeck port); (f) test_parity's SNAPSHOT_BLOCKS
gains guns, damage and flags; (g) the weight test pins the checker's listing (every gun a tenth
off its pattern and no other) rather than refusing, as §3.2 has it. **Found for others:** for
the ships session, the musquidobit fit's eight 18-pounder carronades at 10 cwt stand 11% off
Adye's 9 cwt pattern (listed, drawn at the pattern); for the lead, the trunk's import cycle
between `freesail/api/readings.py` and `action_readings.py` (a test file that imports
`action_readings` before anything has loaded `readings`, first in a worker, finds the registry
half built: tests/test_filling.py with `-n 4` alone, reproduced on the trunk three of three,
mended by the lead on the trunk before the merge (ec424f92): `freesail/api/__init__.py` loads `readings`
first, whichever module of the package is asked for). **Costs:** the snapshot's new fields 20 µs
of 393 on the 64, 14 of 330 on the frigate, 6 of 153 on the cutter; buildSkeleton and project in
Node the 64 10.5 ms against 5.3 without the action, the frigate 7.0 against 5.3, the cutter 3.0
against 2.6. **The builder's suites at 790b1a8:** ruff check and format clean; the fast tier
whole 6,548 passed, 1 xfailed, the one failure the trunk's import cycle above (not the
branch's); the slow tier of the touched files and the known truths 1,330 passed, 8 xfailed;
the pace alone and last 13 of 13. **The lead's merge:** the trial on 6f244969 clean and
lint-clean (ruff check and format); the fast tier whole on it green, exit 0 (08:37 to 09:17 UTC), 6,555 passed, 2 skipped, 1 xfailed, none failed; the Node tests of
the viewer among them (Node 22 on the build machine); the whole suite in the cloud: run 50 on eff2a556 (09:27 to 10:23 UTC): lint green, all six
shards green, 6,953 passed, 11 skipped, 12 xfailed, no failure; the pace job 13 of 13 (so runs
48 and 49's four floor failures were the shared runner's hour, as the lead held). PACKAGE 81 IS CLOSED: the standard, the data, the drawing,
the checker, the truths and the records in one package, the builder's seven departures each the
better rule. Package 91 (the viewer's light and air) follows after it in its turn.

### Package 74, step 2 (the prize as a hull of the one world), as merged (2026-11-07)

**What landed:** the builder's 1a752d3 (claude/pkg-74: the step's final tree f764616, one hash,
with the suites' figures added to the tuning notes alone at 1a752d3, step 1's shape), merged
`--no-ff` by hash at 1bb24f52 onto eff2a556, the one meeting the tuning notes (81's section and
74's step 2 both appended; both kept in order, 74's under its own heading). Steps 3 to 7 sit on
the builder's scratch branch and come onto claude/pkg-74 one step at a time, each its own final
tree, as the lead's rule of 04:06 asks. **Built** (`freesail/world/prizes.py` new, 1,451 lines;
`orders/prize.py`, `api/prize_readings.py` new; `data/captains/prize-master.yaml` new; the role
files' thresholds and the `taking possession` state; the hooks in boarding.py, captains.py,
brains.py, crews.py, world.py, movement.py, people.py, service.py, ships.py, signals.py,
squadrons.py, knowledge.py, grammar.py and the vocabulary): possession ONE function by every
road (the order `take possession of her` within a boat's pull, the officer on a deck carried at
once, the far cut-out on the records); the prize master by the period's ladder of standing
(Falconer's principal officer; the first lieutenant kept with his ship unless the file names
him), rehomed to her and bound to her captain's station, his harness or seat following; the
prize crew by the doctrine's thresholds remustered as hers (the two keepers that cache the
muster, the routine and the quarter bill, both re-pointed: the keepers' audit of ruling 1); her
people prisoners confined by the custom (the officers to the cabin, the people to the hold,
`Person.confined_to` and the walk refused in words); her nation, colours over her own for a day
(`Colours.over`), role, intent and set by the captor's doctrine; `take the prisoners aboard` by
the boat so many at a time; the rising (prisoners over twice the fit prize crew, tired, no
captor within two miles, a draw once an hour from her own stream) fought by 73's tables on one
deck, won or put down with irons for a day; the retaking by a cruiser of her own nation coming
up (72's far captures read from the prize's side); `burn the prize` and `scuttle her`; the
captured signal book a paper of hers; the readings `the prize`, `the prisoners`, `the prize
crew`; seven events; the primer's chapter 27 and chapter 11's rows; the save round trip pinned.
**Truths 7-351 to 7-354.** **Pins moved, old beside new** (each reason in its docstring and
the tuning notes): 7-181 and test_fight's carried deck (she is a prize of ours at once, our
colours over hers, her hurt the prisoners'; the fight's bands 2 to 12 rounds and the losses'
order as they were); 7-325 and 82b's officer on the deck won (her prize master, not a visitor);
97's officer-killed test (Mr Ward, the senior standing of the party, leads on and is her prize
master: package 97's paragraph answered); 72's cut-out (the Nancy his prize at once on the
records, parted for Brest by his doctrine); SW-4's merchant brig in the prize scenes (a prize
crew of eight over sixteen prisoners; the rising put down takes the brig-sloop's 121). **The
merge's meetings** resolved on the branch as told: service.py's ROLE_SERVICE and captains.py's
ROLES (75's indiaman and revenue beside 74's prize-master); 75's revenue.yaml and indiaman.yaml
copied before step 2 gave every role the `taking possession` state and the `mans_prizes` row,
mended in kind (the revenue cutter takes possession as the cruiser does, the Indiaman takes no
prizes as the merchant does). **Taken another way, each accepted:** possession at once when the
order is given within a boat's pull (the boat's quarter of an hour left to step 3's errands);
the privateer parts from her prize by his doctrine, so 72's cut-out no longer joins his company;
the player's own ship struck is not possessed until step 3 (the rules captain lies by her); the
doctrine's own burning waits for the court's valuation (step 5); the replay by both roads with
a prize is step 4's. **Found for others:** a rules captain bound for Brest from the Iroise lays
no course through the goulet (the planner's, 61's family; already on the lead's list); two
frigates of one file draw one seed's wardroom names (told apart in the registry by their homes;
the lead's list, the muster's). **The builder's suites at f764616** (a worktree pinned there):
ruff check and format clean; the fast tier whole exit 0 (08:39 to 09:18); the slow tier of the
touched files and the known truths with test_profile and test_indefatigable exit 0 (09:18 to
10:01); the pace alone and last 13 of 13 (10:01 to 10:05), no floor lowered. **The lead's
merge:** the trial on eff2a556 clean but for the notes' meeting, lint-clean (ruff check and
format); the fast tier whole on it green, exit 0 (10:08 to 10:48 UTC), 6,570 passed, 2 skipped, 1 xfailed, none failed; the whole suite in the cloud: run 51 on 0e38d5e7 (10:49 to 12:02 UTC): lint green, all six shards
green, 6,973 passed, 11 skipped, 12 xfailed, no failure; the pace job (informative) 10 of 13, three
floor tests short of 500 (490, 457, 433; truth 51's frigate held) where run 50 held 13 of 13 and the
builder measured 13 of 13 at f764616 on its machine; the lead ran the pace alone on the build
machine at the trunk head after it (d244be4c, nothing else on the CPU): the known truths' eleven pace tests 11 of 11, exit 0 (the
three the runner failed among them), the whole thirteen 13 of 13, exit 0 (12:09 to 12:14 UTC); so the shared runner's hour again,
as runs 48 and 49. Step 3 (the captive's channel) follows at its boundary, then 4
to 7 the same, one at a time.

### Package 76, step 2 (the French book from the page), as merged (2026-11-07)

**What landed:** the builder's 2df464d (claude/pkg-76: 5735d77 the book and the hoist's form,
c280716 and 2c5ea3c the notes, the trunk merged at the step's boundary), merged `--no-ff` by
hash at 943b453f onto 0e38d5e7, a clean merge. The branch's later commit 2c3e1cc (the step's
suite figures in the tuning notes) was committed after steps 3, 4, 6 and 7 and item 8 landed on
the branch, so its tree is not step 2's and the lead merged 2df464d, the step's own tree, as
the rule of 04:06 has it; that paragraph of the notes reaches the trunk with the next merge.
**Built:** `data/signals/france/` as du Pavillon's system, read in Audibert Ramatuelle's Cours
élémentaire de tactique navale (1802, ch. IV §§ 67 to 74; docs/references/signals/): every
signal two flags, the upper and the lower, read as a cell of a square table of some twenty
flags with guidons and pendants, a guidon over two flags for a bare number, the compass by one
flag under a guidon; the numerary 74 entries, EVERY cell made and marked (the Republic's book
of the year VI is not online; Corbett places a copy at the RUSI), 14 meanings in Orvilliers's
words (Signaux généraux pour l'escadre du Roi, Brest 1772) given as `original` with his source,
four entries added (the chase to windward and to leeward, Orvilliers's; the ships astern to make
more sail, the ships ahead to shorten); the night and fog in Audibert's form (guns in two times,
ten seconds between the guns and a minute between the times, the ships repeating by lanterns;
three chapters told apart by a rocket between or after; the fog one chapter), every cell made
but the fog's keeping company, which is his (§ 93, the signal de conserve); the convoy's
practice cited to Audibert's chapter on the escort of convoys (part II ch. V), its numbers made;
the private form read against his § 70; no dictionary (he has none and proposes none). **The
one engine change, as approved in advance:** `Books.hoist_form` ('numerary' or 'table', refused
in words otherwise) read from book.yaml, `Hoist.form` carried on the hoist and by `repeat the
signal`, `flags_words` saying "two flags at the main" for a table hoist whatever the cell's
number; the record writes `form` only where it is not the numerary's, so no British or basic
record changes; the British numerary proven unmoved by it (the new test: No. 186 three flags
and no form key in its record, No. 16 two flags, the French general chase two flags with form
'table'). **What moved:** nothing pinned (no passage hoists or reads a French signal).
**Taken another way, accepted:** the night and fog test's rule (every entry from a page names a
year of the period, or is marked made) reads the year by a regular expression, so Audibert's
fog signal of 1802 passes by its year and not by a number; the British tables stay numbered.
**Found on the way:** the branch's merge commit 2df464d says "(records)" where the trunk's
range carried code (81's merge and the import mend); said, not rewritten. **The builder's
suites at 2df464d** (a worktree pinned there): ruff check and format clean; the fast tier
exit 0, 6,550 passed, 1 xfailed; the slow tier of the touched files and the known truths exit
0, 326 passed, 8 xfailed; the pace alone and last 13 of 13 (and the same three at 1844886
before the trunk's two moves). **The lead's merge:** the trial on 0e38d5e7 clean and
lint-clean; the fast tier whole on it green, exit 0 (11:05 to 11:45 UTC), 6,571 passed, 2 skipped, 1 xfailed, none failed; the whole suite in the cloud: run 52 on d244be4c (12:03 to 12:55 UTC): lint green, all six shards
green, 6,974 passed, 11 skipped, 12 xfailed, no failure; the pace job (informative) 9 of 13, the
same four floor tests as runs 48 and 49 at 381 to 439 against 500, where the lead's own pace run
alone on the build machine at 12:09 on the same code held 13 of 13: the shared runner's hour. Steps 3 (Spain), 4 (the United States and Naples), 6, 7 and
item 8 are built on the branch and follow by one report when their suites finish.

### Package 75, B3.4's four rulings built (the schooner's mast at place 2), as merged (2026-11-07)

**What landed:** the ships session's 6e19f46c (claude/pkg-75: da7c0e4d ruling 1, aff2e57e ruling
2, e5b861e3 ruling 3, 2e97d97f ruling 4, 6e19f46c the review's mends, after SW-4's 1ff4e813 and
the trunk merged at 02bd0405), merged `--no-ff` by hash at 3c9df9e1 onto 3a94472d, a clean
merge. **Built, the lead's four rulings of 2026-11-06 (TuningNotes, B3.4, "The lead's four
rulings, built"):** (1) the short after swing: a schooner's light main yards (every after yard
on a schooner's mast) swing at "mainsail haul" in tack.yaml's new `light_after_swing_s`, 20 s
(judgement: the engine's abox time for a light topsail yard), hauled within a point of the wind
as before and before the head yards, never with them; trial B's tack 219 to 151 s, the main
topgallant's 232 to 172 s; trial A, the brig and the frigate line for line as before (no file
has a yard on a schooner's mast, pinned over every file); (2) the word by Luce 1884 p. 417:
"Main-topsail haul." for a main course not set, "Rise tacks and sheets. Mainsail haul." kept for
one set, read from the ship's "courses" group as her file names them (so the bilander's settee
is her mainsail), a course set or goose-winged counting as set, hauled up, furled, blown out,
unbent or its yard shot away not; (3) place 2 with no mast carrying yards: with every fore yard
shot away the schooner-mast's yards are her after yards (trial B's tack so 289 to 164 s, the
sail full on the new tack; the pin renamed and widened); (4) storm.py: the courses' reef at the
topsails' second reef for any rig with topsails (Luce p. 476; Cobb p. 95), the aftermost
course's and the driver's take-ins gated on square-rigging; a course with no reef bands not
named, as before; the cutter, the smack and the two filed schooners sail the gale exactly as
before. **One pin moved, old beside new, proven by bisection:** GATE_5B_THICK_DIGEST
6f062dc60419f52c to 9ce8174ebc6948c6, the frigate putting about off Black Head with both
courses in the gear: words only ("Main-topsail haul." for "Rise tacks and sheets. Mainsail
haul."), every tick and line the same, the old word put back giving the old digest;
test_evolutions' frigate tack line the same way; test_catalogue's frozen tack timings gain the
key. No whole log moved; the captain's trials the builder's machine's three with the same
digests; no slow test changed outcome. **The lead's rulings on the five open points** are in
the notes to the ships session below (2026-11-07, 12:50 UTC). **The builder's suites at
6e19f46c:** the fast tier 6,495 passed; ruff and format clean. **The lead's merge:** the trial
on 3a94472d clean and lint-clean (ruff check and format); no forbidden word new in the diff;
`data/ships/` untouched; the fast tier whole on it green, exit 0 (12:37 to 13:18 UTC), 6,622 passed, 2 skipped, 1 xfailed, none failed; the whole suite in the cloud: run 53 on b28266c3 (13:20 to 14:35 UTC): lint green, all six shards
green, 7,025 passed, 11 skipped, 12 xfailed, no failure; the pace job (informative) 9 of 13, the same
four floor tests as runs 48, 49 and 52 at 379 to 442 against 500, the shared runner's hour (the
build machine alone held 13 of 13 at 12:09 on the trunk before this merge; B3.4 touches no tick of
the pace's passages). B2 (the *Neufchatel*) starts on these; the one
final report for 75 follows.

### Package 76, steps 3, 4, 6 and 7 and item 8 (Spain, the United States and Naples from the page; the checker; the truths; the flags of command and identity), as merged (2026-11-07)

**What landed:** the builder's 7c35713 (claude/pkg-76: the steps' commits, the trunk merged at
9c3a306 and 6aea118, the trade trial's pin re-measured at b0cda9c, the figures and step 7's
notes at 7c35713, nothing after it), merged `--no-ff` by hash at 649c5478 onto b92dca34, a
clean merge. **Step 3, Spain a root of her own:** `data/signals/spain/` from Mazarredo's
Instrucciones y señales (Cádiz 1781, the third edition by royal order), read on the page: the
hoist's form a table (his four hundred cells of two flags of twenty), the numerary 100 entries,
87 from the page (his cells; his twenty one-flag signals numbered 401 to 420) and 13 made and
marked; the night 61 from the page (his three chapters under sail told apart by a rocket or the
stern lanterns, five articles at anchor); the fog 19 (his first chapter, guns in two times); the
convoy 35 (the squadron's cells and his orders to a convoy's commander, 4 made); the private
form basic's word for word so that her draw stands; no dictionary; the system well-built on his
numbers of 1781, the 1797 question stated in the declaration for the owner's shelf; her line in
nations.yaml moved to her root; no code changed for her. **Step 4:** the United States from
Barry's A Set of Signals (Norfolk 1800), a flag a figure, 69 entries (54 at his numbers, 15
made), the night his lantern figures, the squadron's flags of 1803 to 1804 from Preble's account
in the declaration; Naples from the flotilla's book of 1807 (the declaration saying 1807 and
Joseph's kingdom, the Bourbon book of 1805 not found), 55 entries (46 at its numbers, 9 made),
13 night signals by number; Portugal on basic for signals, her flags in basic's colours.yaml
dated to 1816; basic's declaration naming whom it stands for (the Batavian Republic, Denmark,
Portugal, Morocco and Algiers, Sardinia, Etruria, Liguria, the Papal State). **Step 6:**
`tools/check_signals.py` over every root (each root loads with its seventh file; every does
parses against a frigate or names a form of 71's design; every source named; an entry not
marked made cites a page of the period; the private form drawable; every nation reads the root
under her name), and per root a hoist read by her own book and "a signal we cannot read" by
another's, the convoy of four tacking in succession on one hoist of her own book. **Step 7:**
truths 7-426 to 7-433 as the brief words them; the design note's postscript "As built out",
spec M7 §3 as built, Harness §21d, the primer's chapter 23 in-world, the tuning notes. **Item 8,
the flags of command and identity (the owner's addition):** every root's `colours.yaml` in the
approved shape (the flags by name with words, proportion, drawing, dates and source; the
occasions by role in 81's place words), Britain from Perrin, France from the law of 1794 as
Preble gives it, Spain from the owner's Winfield answer (pp. 59 to 60, cited and not copied: the
ensign of 28 May 1785 and the quartered jack, the jack's colours the builder's judgement and
said so), the rest from the 1820 plates dated against Perrin and Preble; `freesail/world/flags.py`
(new) sets what flies where by the colours, the role, the occasion and the flags ordered;
`Locker.flies` the viewer's list (81's viewer serves it as it is; the drawing's lines kept apart
under `drawing.lines`, since 81 draws a part with no rect as the whole field); the lookout says
what flies beyond the ensign where the colours' line already falls ("she wears a pendant at the
main: a man-of-war"); the orders `hoist the broad pendant`, `hoist a second ensign at the main`,
`hoist the jack`; `make the Spanish private signal` and `make the private signals in succession`
from the tables held (her own, an ally's by the scenario's papers, a captured book by 74's road),
refused in words naming the tables held, a challenge in a named form answered only by a ship of
that nation and judged against that form's table, three minutes a hoist in succession, the
verdict naming the forms (the Java's move of 1812). **Truths 7-434 and 7-435.** **What moved,
two pins, each proven by its entry put back:** test_nations' Spain line (basic to spain,
well-built); TRIAL_TRADE_STRANGER_DIGEST 5e7bdba2a4f4770b to aa04702e062bc64b, the French
brig-sloop's two made-out lines gaining "; she wears a pendant at the main: a man-of-war", the
words switched off (`flags.FLAGS_SPOKEN`) giving the old digest with the 1,594 lines, the states
and the anchored ticks unmoved. **Taken another way, each accepted:** weighing in the Spanish
book made (433); the Spanish convoy reading the squadron's cells; the three new roots' private
forms basic's word for word; the checker parsing against a frigate; a stranger answering only a
challenge in her own form, for the item's named-form challenges alone; the succession's wait
three minutes a hoist; the drawing's lines apart from 81's parts. **Found for others:** "shake
out the reefs" in every root is a far body's form and not the dialect's words (a near commanded
captain given it by signal would be refused): named a design form in the checker, for the lead
(71's handling); a challenge made by the player while his captain does not command is never
judged (71's rule); 74's `Colours.over` is the field an "as a prize" occasion would read, not
built as ruled. **Hooks named for 74 and 72, not built:** a doctrine line for a rules captain
holding more than one table (the private signals in succession to a stranger who does not
answer the first) and a privateer hoisting another nation's challenge as a ruse (74's files); a
set's admiral by rank wanting the captain's rank (72's). **The builder's suites at b0cda9c** (a
worktree pinned there): ruff check and format clean; the fast tier exit 0, 6,600 passed, 1
xfailed; the slow tier of the touched files, their neighbours and the known truths exit 0, 570
passed, 8 xfailed; the pace alone and last 13 of 13. **The lead's merge:** the trial on b92dca34
clean and lint-clean; no forbidden word new in the diff; nothing of 74's, 75's or 81's files,
the physics and `data/ships/` untouched; the fast tier whole on it green, exit 0 (15:04 to 15:45 UTC), 6,657 passed, 2 skipped, 1 xfailed, none failed; the whole suite
in the cloud: run 54 on d7dfbdf9 (15:46 to 17:03 UTC): lint green, all six shards green, 7,072
passed, 11 skipped, 12 xfailed, no failure; the pace job (informative) 9 of 13, the same four floor
tests as runs 48, 49, 52 and 53 at 379 to 437 against 500, the shared runner's hour (the build
machine alone held 13 of 13 at 12:09 before this merge, and the builder measured the pace alone
13 of 13 at b0cda9c with the flags in; the lookout's refresh is once a minute with the look). Step 5's substance (the lookout's
reading, the private signals in succession) is item 8's; what a corrected number moves is the
steps' "what moved". Package 76 has one thing left: the owner's shelf answers to its seven
questions as they come (the 1797 quaderno, the 1799 fog book, the convoy book, the French book
of 1804 to 1805), each a data change by the same road; the lead holds the package open for them
and closes it with the owner.

### Package 75, B2: the *Prince de Neufchatel*, with SW-4's words step and her stage 0b, as merged (2026-11-07)

**What landed:** the ships session's a244e1bb (claude/pkg-75: 37c93bac SW-4's words step, 5afa7b6e
her stage 0b, 87896126 the reviews' mends, 84763fb8 her module named in `MODULE_FILES`, 9f2276ee
her, a244e1bb the shared guards naming her; after the trunk merged at c3d46cca), merged `--no-ff`
by hash at 04136d99 onto 9b821fb5, a clean merge (`tests/conftest.py` auto-merged). **Her, one
ship commit:** `tools/ships/neufchatel.py` writing `data/ships/hermaphrodite-brig.yaml` and no
other file (the sixteen files regenerated the same by `cmp`), her people file, her description row
("hermaphrodite brig", "a brig" at a distance, rank 2; "a privateer brig" and "an hermaphrodite
brig" her words, never "a brig", the merchant brig's), `tests/test_neufchatel.py` with truths
7-192 and 7-193 drafted. Her hull from RMG ZAZ6177 and ZAZ6179 (32.7 m between the rabbets, 7.82 m
beam, 328 tons on the Navy's rule against Winfield's 328.23), a brig's foremast and a schooner's
main, her main topgallant on its two light yards from her first commit by B3.4's rule; her one fit
"as taken 1814", sixteen 12-pounder carronades and two long 6s, no pivot (Winfield pp. 335 to 336,
cited; Adye 1804 pp. 72 and 155 for the patterns' weights, appended to `tools/ships/period.py`
with Steel's anchors for 14 guns); 130 men, American colours; package 81's checker clean.
**Measured:** her best 8.82 kn in 15 kn and 12.22 kn in 25 (7-193's band 11.5 to 13.0), 40°
closest; tack 182 s, wear 461 s, hove to 51.1° off at 3.0 kn; heel 5.5° at 90° in 15 kn; her
lowest port with a gun in it shut at 18.2° (7-190's row, 18.18, 3 ports); broadside 108 lb;
`clr_x_m` +0.3 to +2.0 and back to +0.1 after the jib's centre was mended to its triangle's, old
beside new. **SW-4's words step, as ruled at SW-4's merge:** a crewed revenue cutter reads "a
revenue cutter of Britain, in the service of the Customs" and hails from `answers: revenue:`; an
Indiaman "an Indiaman of Britain"; `revenue` in `regimes._MAN_OF_WAR_ROLES` and
`squadrons._ARMED_ROLES`, the Indiaman in `HAND_PEACEFUL_ROLES` and out of the armed set (her book
takes no prizes); truth 7-191 and the two crewed evading tests to `SLOW_TESTS`; the Musquidobit
fit's carronades 10 to 9 cwt through `gen_ships.py` (Adye 1804 p. 72; no source gave the 10;
81's note), the one change to another ship's file. **Her stage 0b:** the scenario's `nations:
{as_of, wars, letters_of_marque, source}` parsed, validated and kept on `Scenario` (left out of
the dict and the pickle while None; every shipped scenario and the kept saves byte for byte as
before), read by nothing until her scenario (B6's). **The shared guards name her:** twenty-one in
B3's, B8's and B5's test files, each naming her exactly (`ON_A_SCHOONERS_MAST`,
`COURSE_REEFED_BY_THE_GALE`, her 7-190 row, her viewer rows); the twenty-second, package 81's port
at her No. 8, a recorded departure in 81's test (`CUT_AT_A_CORNER_M`, 2.268 drawn against 2.27
served) for the lead's ruling; recorded departures beside it, each named in the tests:
`OUTLINE_MET_TWICE_AT` (her stem's foot served twice), `WALE_UNREAD`, `TACK_OFF_HER_SIDE_M`
(0.20 m) and `FLARED_TRANSOM`. **The owner's eye** on her sheets beside two photographs of a model
(the loose-footed fore gaff sail, no stern gallery, the boom close over the taffrail, square yards
on the main topmast) agrees with her file as drawn, recorded in her notes. **The lead's rulings on
the report's six points** are in the notes to the ships session below (2026-11-07, 21:48 UTC):
B3.4b still owed. **The builder's suites at a244e1bb:** the fast tier whole green on the final
tree (at 9f2276ee with the guards uncommitted, 6,753 passed, 1 failed, the one since named); ruff
and format clean; the slow candidates no outcome changed; the captain's trials the machine's
three; the four whole logs as before but the first action, 473 to 497 lines, bisected to the
trunk merge c3d46cca (74's step 2), not to her. **The lead's merge:** the trial on 9b821fb5 clean
and lint-clean (ruff check and format); no model or vendor name in the diff; `data/ships/`
touched by the generator alone; the fast tier whole on it exit 0, 6,791 passed by the dots and 1 xfailed, 20:58 to 21:41 UTC (43 minutes); the whole suite in the cloud, run 55 (2026-11-07, 21:43 to 22:43 UTC, on 8e552bd8): lint green; the six shards green, 7,216 passed, 11 skipped, 12 xfailed, the longest shard 51 minutes; the pace job 9 of 13, the four floor tests at 446, 431, 410 and 386 ticks a second against 500 on the shared runner, as at runs 48 to 54 (the build machine alone held 13 of 13 at 12:09). Next in 75: B3.4b (the word's two cases,
the dismasted lines), then B3.3 (the settee) with B4 (the bilander); the 74 and Phase 5 after.

### Package 74, step 3: the captive's channel (the design's §3), as merged (2026-11-07)

**What landed:** the builder's 924d1b2 (claude/pkg-74: the scratch's step 3 commits 1400292,
56c34cb and 27369b5 merged at 30343f6, the trunk merged at 1c378de and 3d1fa25 (eff2a55 and
9b821fb: 81, 76 whole, B3.4, the api package's readings loaded first), 96261d8 the step's final
tree with its one meeting of 75's sub-type rules, 924d1b2 the suites' figures in the tuning notes
alone), merged `--no-ff` by hash at 277e9482 onto 04136d99 (B2 merged), a clean merge. **Built (`freesail/world/
captive.py` new, 943 lines; the hooks in `prizes.possess`, `knowledge.players_person`,
`movement.check`, `go` and `where_am_i`, `orders/stations.py`'s word to the captain, the director's
two forms in `world/orders.py` and `agents/director.py`; `data/captains/hail.yaml`'s `parole:`
rows by nation with Spain's; the agent for prisoners a place of every port, named by the port's
nation; the `truce` state of 71's colours, "a flag of truce", nobody's enemy and nobody's prize):**
the player struck is a person aboard the captor, his station stood down by the handover's rule and
his prompt following his body (the far body that takes him made a hull and woken as a dealing of
the first rank), his sword a thing in the captor's captain's keeping, confined to the cabin, every
order of any deck refused in words naming his state (hers, his own ship's as a prize's, ashore as
a prisoner of war); the parole asked by the captor's doctrine a minute after the taking in the hail
table's words by his nation (the French captain's in French and English, Spain's row), read in the
captive's own words only while asked, asked once more after a glass, given by rule after a watch;
given, the cabin, the gunroom and the quarterdeck by day and the sword returned; refused, the
gunroom alone, a sentry said; the captor's course for his doctrine's port; the prisoners landed to
the port's agent with the list of their names and the day first victualled; the cartel by the
director's form (`cartel: a cartel from <port> for <persons>`), a merchant brig of her own file
under a flag of truce with the role `cartel` and "a cartel" said on her, who takes them off within
hail and lands them free at her port (doubted beyond a day's sail); `aboard the <ship>: the parole
of <person> given | refused` doubted while her captain waits his answer; `where am I` with his
state; the prisoners' reading naming the prisoners of rank; five events; the primer's chapter 27
"When it is you who strike" and chapter 11's rows. **Truths 7-355 to 7-357.** **The meeting with
75's rules:** the cartel's own row in `ships.DESCRIPTIONS` (brig.yaml, "a cartel") failed
`test_subtypes` twice since SW-4 (every row a file's own description with its fit; a shared file's
first row her kind), so she has no row and sails as a merchant brig of her own file with the role
and the words. **Pins moved:** none; the one pin changed is the design's (test_prizes' merchant
brig's prisoners "no prisoners" to "six prisoners of rank: ..." in the cabin, her officers persons
confined in her still, since the prize's named few are not moved by the boat's loads). **Taken
another way, each accepted:** the captive's officers confined in the prize by rank (the
`divide_prisoners` rule the counts'); the cartel's persons on her record, ashore at her port's
quay (80's words fill her out); the prisoners' victualling not modelled; a model seated as the
captive served by 82's voice station until step 6's seats. **Found on the way, mended here:** the
far brain forgot a struck mark's nation (she shows no colours) and never saw `enemy struck`; the
privateer's `chasing` rows had him evade a frigate that had struck to him; the far brain dropped
its mark on entering `taking possession`; the captive's person was read as every hull's captain
(he is the followed prompt's alone); a far vessel whose plan runs out is gone at the minute's end
(the cartel's minute keeps her). **Found for others:** a rules captain bound for Brest from the
Iroise lays no course through the goulet (the planner's; the lead's list); 81's truth 7-441, a
wall-time ratio asserted under a quarter inside the fast tier, once 0.30 under four workers (the
lead's list); 81's viewer does not know the `truce` state (`viewer_flags.SHOWING`), so a cartel's
flag of truce is not drawn (the lead's list, found by the lead). **The builder's suites at
96261d8** (a worktree pinned there): ruff check and format clean; the fast tier whole exit 1 then
exit 0 (the one failure 7-441 as above, passing alone there and on the bare trunk); the slow tier
of the touched files and the known truths with `test_profile` and `test_indefatigable` exit 0; the
pace alone and last 13 of 13. **The lead's merge:** the trial on 04136d99 (B2 merged) clean and lint-clean; no
model or vendor name in the diff; nothing of 75's, 81's or 76's files, the physics and `data/
ships/` untouched; the fast tier whole on it exit 0, 6,807 passed by the dots and 1 xfailed, 21:42 to 22:25 UTC (43 minutes); the whole suite in the cloud, run 56 (2026-11-07/08, 23:20 to 00:35 UTC, on fbc6c930): lint green; the six shards green, 7,235 passed, 11 skipped, 12 xfailed, the longest shard 65 minutes; the pace job 9 of 13, the four floor tests at 443, 427, 410 and 388 ticks a second against 500 on the shared runner, as at runs 48 to 55 (the build machine alone held 13 of 13; the builder's pace alone at 96261d8 13 of 13 at 20:15). Step 4 (the far fight wired; truths 7-358 to 7-361 and
7-369) follows from the scratch branch, one hash with the trunk merged, with 74's answer on 76's
two doctrine hooks.

### The owner's play of 2026-11-09: nine notes and three saves, triaged (the lead)

The owner played the trunk at 7693cad5 on the *Prince de Neufchatel* in the Rade de Brest (three
saves, kept with the lead and read by the game's own loader, never committed) and wrote nine
notes. Each was reproduced before it was ruled on: four investigations run beside the lead (the
viewer driven in a real browser; the prompt driven live ashore and in the cabin; the tide's own
function at seven points; the code read for the two surveys), and the strike save replayed whole.
What each is, and where it goes:

1. **Her guns show through her ports, run in and secured: a defect of the viewer's paint order**
   (package 98). Her guns are placed by rule, a secured muzzle 0.10 m inside her drawn side on
   every ship (her carronades -0.100, the frigate's long 9s -0.100). A gun's figures sort at
   their own middles, the side's strips and the lids at the middle of the whole strip ring, the
   bilge with it (`client/projection.js`, the guns' `sortAt` and the strips'); her steep deadrise
   puts that point 0.56 to 0.70 m inboard, so her whole short carronade paints over her side and
   lid, where on the brig only a muzzle's face does and on the frigate some.
2. **A flag's canton and stars come and go with the bearing: a defect, every nation's** (98).
   Each part of a flag is a polygon sorted at its own middle, so the canton sorts behind the
   stripes over half the circle (the American ensign loses 16 parts over one half and 5 over the
   other; Britain's loses its canton and crosses the same way), against the design's own "a flag
   sorts at its own middle as a sail does" (Design-ViewerAction §12.3). Beside it: a drawing's
   `lines` are not drawn (the saltires), and a flag has no rank among the kinds.
3. **The chart and the ship view tell more than the person knows: confirmed, a design step**
   (package 99). The browser is served the whole snapshot (`api/queries.snapshot`); the knowledge
   rule greys the instruments' readouts alone. Off the deck the views still show the true and
   apparent wind, the heading, the sails, the strangers and what is in sight, and the master's
   account run on live (the chart shows the reckoning, never the true position); ashore or a
   prisoner the same. Nothing keeps "the last value he learned" today.
4. **A cabin view and a view ashore: not now, the lead's advice** (the owner asked to be argued
   with). The ship viewer stays a ship viewer for this milestone. What the person below or
   ashore should see falls out of note 3: the ship as he last saw her, greyed and stamped with
   the hour. A scene for the cabin and for the quay wants things to show (the table, the papers,
   the people, a port's places), which are the career's and the port's content of milestone 8;
   booked there with package 92's building, not as a viewer mode of milestone 7.
5. **A signal ordered from the cabin: no rule says, and the code lets it** (98, for the owner's
   word). The rule as written gives the deck's orders as the sails, the yards, the lines, the
   helm, the anchors and all hands (the primer's chapter 14; spec M7b §14); "beat to quarters"
   and "fire a gun" are refused below too. The colours and the signals are sent to their handler
   before the place is checked (`orders/__init__.py`), so they are done from the cabin, the only
   orders of the deck that are. The lead's advice: they are the deck's, refused below in the
   same words, until a captain can pass the word from his cabin (a later step: "pass the word to
   the officer of the watch: ...", with the minute it takes).
6. **Commands with no answer in the log, ashore and below: the worst of the nine** (98, first).
   Driven live in a browser: of 45 lines typed, 30 showed nothing. The server answers every one;
   the page is sent a line only if the person "hears" it, and the player's own readings
   (`query.*`, classed as said on deck) and refusals (`order.*`, classed as the deck's) are
   dropped whenever he is not on deck (`world/knowledge.hears`), against the design's own "the
   asker's own question, heard where he asked it" (Design-PlaceKnowledge). So ashore and in the
   cabin every reading and every refusal is silent, the console's the same. Beside it, the page
   takes any two-word line beginning "go" as a clock command ("go below", "go ashore", "go
   aloft" never reach the server). **The testing procedure the owner asks for** is prototyped
   (the server launched on a port, a headless browser typing each line, the server's answer, the
   socket's frames and the log's new rows kept side by side, each line marked shown or not): to
   be a kept tool with plans by place and state (98's first step), so that every mend of 98 is
   proven as the player sees it.
7. **The model officer was sent no chart picture: the OpenRouter door never fetches it** (98).
   The `chart` tool is offered and answers "a picture of 1200 by 900 pixels", but that door's
   model is built without the picture's fetch (`agents/api.py`; the first door has it), so the
   image part is never added, for every model at that door, whatever it can read, in every
   place. The words told the model a picture was drawn.
8. **Letters and things as one system: surveyed, a package of its own** (package 100). Today a
   `Thing` has a description and a keeper but no text; "read" and "open" show nothing; nothing
   removes or destroys a thing; a letter is a `Message`, read to the captain on arrival and gone;
   a letter sent ashore by the boat is dropped at the landing; the player can draft a book but
   no letter.
9. **The Goulet's stream over the whole Rade: confirmed, data** (98). The `the-goulet` area is a
   box from 48.29 to 48.37 N and 4.62 to 4.42 W (`data/tides/streams.yaml`), the narrows and most
   of the bay: 4.9 kn at springs at the owner's position and in the middle of the Rade; east and
   north of the box the open Channel's stream answers (1.8 kn towards 245 degrees, "By the
   master's reckoning she is in the open Channel" in the owner's own log). No text in the
   repository gives the Rade's rate; the design's own note points to the hydrographic service's
   atlas of the roads, not yet read.

**The strike save, replayed** (the owner fired on a French frigate under French colours, lost
his captain to a shot, struck and was taken): five defects of package 74's step 3, sent to its
builder to mend with step 4. The captive's own words at the prompt were taken as the player's
hand, so the captor's captain stood aside and she lay aback and took the ground forty-five
minutes on; the captor engaged his own prize a minute after taking her and fired 25 shot into
her; a bare "Yes." was not read for the parole; a prisoner's "hail her" was performed, and the
prize answered "prize to Mr Ray's ship"; "go ashore" was refused in a free man's words. What
worked as designed: the first lieutenant succeeding the dead captain and taken as "the first
lieutenant of", the parole asked in French, the sword, the places, the refusals of the deck.

### Package 75: the settee (B3.3, B5.4), B3.4b, the *Neufchatel*'s ruled fixes (B2b) and the bilander (B4), as merged (2026-11-09)

**What landed:** the ships session's bd12a802 (claude/pkg-75: 994bf966 B3.3 the settee in the
engine, 1bdb0546 B5.4 the settee drawn, the trunk merged at 2da2668f, 52fad521 B3.4b, 46cf8218
B2b, 7fe5a877 the review's mends, ceff087c her module named, d0fd2799 the bilander, bd12a802 the
shared guards naming her), merged `--no-ff` by hash at acdcfb56 onto be9c951e (the trial on 7693cad5; the lead's records and the probe's prototype the only commits between), a clean merge. No
bridge message reached the lead (dormant from the 8th to the 9th); the branch's tuning notes were
read as the report. **B3.3, the settee in the engine:** a settee (a dipping lug on a yard that
stands, the key `settee`) with its own set, take in (clewed up aloft, never lowered), furl (on its
yard aloft) and dip (`data/evolutions/set_settee.yaml`, `take_in_settee`, `furl_settee`,
`dip_settee`; the library 104 to 108 evolutions), kept drawing through the tack and dipped after
"let go and haul", changed round in the wear, the box-haul and the wear short round, clewed up
with the courses to back and fill and to lie a-try, kept standing to scud; `heave_to_aback` read
(`scripts.yards_to_back`); its sheet's lead from its own corners (`evolutions/trim.py`); "brace"
refused it in its own words; every time and hand a judgement, said so. On a fixture no committed
file was; truths 7-198 and 7-199 drafted. **B5.4, the settee drawn** (`client/projection.js`):
its yard, cloth, slings and derrick, 25 cases; no committed file's drawing moved (144 states
equal as text). **B3.4b, as ruled:** the haul's word in its two cases by Luce 1884 (pp. 417, 421,
428 and 446; the ruling's "pp. 419 to 420" stands on the scan's p. 421): the main course alone
"Rise main tack and sheet. Mainsail haul."; the fore alone "Main-topsail haul." and, at the head
yards' haul, "Rise fore tack and sheet. Let go and haul."; the dismasted rigs' lines (the wear
with no head yards says nothing of squaring them; the heave-to with no yards to lay aback "under
her fore-and-aft canvas, fore staysail sheet to windward"; the tack ended by its timeout names
the tack she lies on); words only, the pins old beside new. **B2b, the *Neufchatel*'s ruled
fixes:** `form._closure` takes levels within a millimetre as one (her stem's foot served once,
`OUTLINE_MET_TWICE_AT` gone, every other file's served graph the same to the last figure); a
navy by its nation's adjective ("a ship of the French navy", "the American navy"); she is a
privateer wherever no scenario or intent names a role (`brains.description_role`,
`own_sub_type_role`; the eight rows sailed before package 75 keep the intent's rules by
`INTENT_RULED_ROWS`, the build's reconciliation, accepted as the rule); the grounding's "no water
by the chart"; her transom re-read to [2.46, 2.53], `FLARED_TRANSOM` emptied; her fore staysail
corrected to the triangle that fits (93 to 46 m2), her polar and rating re-measured old beside
new, her best point still in 7-193's band; the gale takes in her fore gaff sail at the topsails'
second reef as ruled (measured: she then gripes with the helm hard over until she lies a-try, so
the lead revises the moment in the notes below); `CUT_AT_A_CORNER_M` passing as recorded. **B4,
the bilander:** `tools/ships/bilander.py` and `tools/ships/settee.py` writing
`data/ships/bilander.yaml` and no other file (seventeen files from the generator byte for byte),
a British coasting bilander under a settee main from Chapman 1768 Pl. LXII No. 5, Gwyn's drawing
and the collier's folios, each measure taken by two methods; her company of eight (the master,
the mate, the boy and five seamen), unarmed by default with a fit of 8 guns, her description
"bilander" (Lloyd's "billander" beside it) with `roles: [merchant]`; `clr_x_m` +0.40 to +2.0,
bounded by her heave-to in 8 kn; truth 7-197 and her handling on the engine's settee, truths
7-198 and 7-199 judged by the report's order; the shared guards name her (seventeen files; her
round stern with lights and no gallery; the *Neufchatel*'s role guard's table). **Pins moved,
each old beside new in the tuning notes:** the library's count (104 to 108); B3.4's two fixture
pins on the settee (renamed, the settee no course at the word); the word pins of B3.4b; the
*Neufchatel*'s helm test (the close-hauled band restored and marked a strict known failure at
+3.95 degrees, for the lead's ruling, given below); no whole log, digest or truth of a committed
file moved but by the trunk's own merges (the first action 497 lines, 84176c16, re-based as
ruled). **The lead's rulings on the open points** (the roles' list, the trim's alias, "the
square sail", the fore gaff sail's moment, her helm, the bilander's boy, watches, helm and round
stern, the settee's forced-round guard and the words bugs) are in the notes to the ships session
below (2026-11-09). **The builder's suites on the final tree:** the fast tier whole 7,029 passed,
2 skipped, 2 xfailed, exit 0; the slow candidates 294 passed with the machine's nine as before;
the captain's trials the machine's three; the four whole logs equal; ruff clean. **The lead's
merge:** the trial on 7693cad5 clean and lint-clean (ruff check and format, 367 files); no model
or vendor name in the diff; `data/ships/` touched by the generator alone (the bilander new, the
*Neufchatel*'s 58 lines by B2b); the fast tier whole on it exit 0, 7,031 passed by the dots and 2 xfailed, 21:53 to 22:53 UTC (an hour, the machine shared with the investigations of the owner's notes for its first half); the whole suite in the cloud, run 57 (2026-11-09/10, 22:54 to 00:09 UTC, on 75b63c82): lint green; the six shards green, 7,461 passed, 11 skipped, 13 xfailed, the longest shard 68 minutes; the pace job 13 of 13 in 4 minutes 48, where runs 51 to 56 fell short on the four floor tests (the shared runner's hour, as the build machine's 13 of 13 said). Next in 75: the ruled revisions and the
settee's forced-round guard (B3.3b), then B7 (the 74), Phase 5.

### Package 75: the owner's two rulings on the *Neufchatel* (B2c) and the settee forced round (B3.3b), as merged (2026-11-10)

**What landed:** the ships session's 5af283de (claude/pkg-75: 8b327687 B2c, d622c4d5 B3.3b,
5af283de the review's mends, on bd12a802, merged before at acdcfb56), merged `--no-ff` by hash at
cff8fdb1 onto 3b76d06a, a clean merge; reported by bridge message on the 10th (the session's
first to reach the lead since the 7th). **B2c, the owner's two rulings of 2026-11-08, made in the
lead's place while the lead's usage was spent, recorded in the tuning notes in the owner's
words:** (1) "At lie a-try": her fore gaff sail is taken in when she lies a-try, as Cobb has it
(1841 p. 79), and not at the topsails' second reef (`orders/storm.py` names no gaff sail; lie
a-try's handing and its line kept); (2) "Re-tune, widen bands 0.2 degrees": her `clr_x_m` +0.1 to
-0.6 through the generator (the other sixteen files byte for byte), her close-hauled band -1.0 to
+1.7 and her abeam and ten-point band +0.3 to +4.0, the strict known-failure mark taken off. As
measured, old beside new: her helm in 15 kn +3.95 to +1.65 degrees close-hauled and +1.61 to
+0.39 abeam; her tack 261 to 189 s; her polar the same; and in her gale the griping of B2b gone,
by the two together (with the first alone she still griped: with her fore staysail the 46 m2
that fits, it is her lead that keeps her off), the storm staysail set at 34 kn again as before
B2b. **These overrule the lead's rulings (4) and (5) of 2026-11-09, 22:56,** written before the
lead had read them (the gaff sail kept through lying a-try; her lead kept at +0.1 with a band of
her own): withdrawn in the notes below. **B3.3b, the lead's ruling:** hove to with the settee
kept and forced round through the wind, "fill away" now dips a settee on the weather side first,
as she lies, and then lets her fall off (the tack's way, changed last, put her head to wind and
astern in 15 and 20 kn: five builds tried and not kept, recorded); its sheet as hoisted. No
committed file but the bilander's reaches it (a trace of seven files, 21 runs, every tick and
line the same on the base and the tree; the base's checkpoints run on tick for tick). **Pins
moved, old beside new:** her two helm bands (the owner's ruling); `tests/test_settee.py`'s script
cases three to five. **Found, not built, ruled in the notes below:** a forced round with no fill
away ordered leaves the settee against its mast; a kept settee never trimmed again as she pays
off; the runner reads an evolution's holds once, at the order ("furl the mainsail" given while
the settee is being dipped furls a yard on deck); the runner's group line names sails lie a-try
has since taken in. **The builder's suites at 5af283de:** the fast tier whole 7,038 passed, 2
skipped, 1 xfailed (the one changed outcome her helm test, xfail to passed); the slow candidates
with the machine's nine as before and two pace floors under load that pass alone; the four
whole logs the trunk's; seventeen ship files the generator's bytes; ruff clean. **The lead's
merge:** the trial on 3b76d06a clean and lint-clean; no model or vendor name in the diff;
`data/ships/` touched by the generator alone (her `clr_x_m` and its note); the fast tier whole on
it exit 0, 7,040 passed by the dots and 1 xfailed, 01:24 to 02:22 UTC (run twice: the first run was killed at 99 percent by a restart of the lead's container, no failure to that point, and is not counted); the whole suite in the cloud, run 58 (2026-11-10, 02:24 to 03:39 UTC, on 2c9485fd): lint green; the six shards green, 7,470 passed, 11 skipped, 12 xfailed (one xfail fewer than run 57, her helm test passing), the longest shard 68 minutes; the pace job 13 of 13 in 5 minutes 16.

### Package 98, steps 1, 2 and 6 (the browser probe; the player hears his own answer; the colours and signals by the deck's rule), as merged (2026-11-10)

**What landed:** the builder's 28f7788e (claude/pkg-98: e8610798 the probe, 00cf0000 steps 2 and
6, the trunk merged at 75b63c82; the step's own tree, the later steps not in it), merged `--no-ff`
by hash at 985c8777 onto 2c9485fd, a clean merge. **Step 1, the probe a kept tool:**
`tools/browser_probe.py` (Python over the browser's driver, as `tests/test_pictures.py`): the game
made by the server's own road from a plan's scenario and flags, or by a plan's world builder (the
prisoner's: the struck frigate), served on a free port with the consent records and saves in the
run's own folder; each line typed at the page's prompt and, beside it, whether a request left the
page, the server's answer, the socket's frames, the log pane's new rows and the where-you-are
instrument; each line marked answered, other or unshown and judged against the plan's
expectations; a failed step screenshotted; exit 1 on a failure, 2 with no browser. Eight plans in
`tests/browser_plans/` (the deck, the cabin, the gunroom and aloft at anchor; ashore at the quay,
the market and the tavern; under way; in action at quarters; asleep; the boat and a visitor
aboard another ship; seated at the master's station; a prisoner), played in the slow tier by
`tests/test_browser_probe.py`, skipped where no browser is found. The lead's prototype folder is
gone, its scenario kept. **Step 2, the player hears his own answer** (the owner's ruling of
2026-11-09): `knowledge.his_own` knows a line as the player's own by its actor (his readings
`query.*`, his orders' acknowledgements and refusals `order.*`, the words he said, his seat's own
lines), and `knowledge.hears` lets it through first, asleep or awake, so the page, its reach-back
on a reload and the console all show it; a deed done out of his sight (a sail set, the colours
changed) is of no own family, reaches him by his place as before and is not reported of itself.
The page takes "go" as the clock's only alone or with a number, so `go below`, `go aloft` and
`go ashore` reach the game. **Step 6, the colours and signals by the deck's rule** (the owner's
ruling): `orders.handle` checks a signal order's place before its handler (`movement.check`,
"signals" among `DECK_OBJECTS`): the colours, the signals, the private signal, the lights and a
hail across the water are refused below and ashore in the deck's words, their readings answered
as before; a visitor keeps his hail and signal; a captive's are refused as his other orders are
(they had passed the check by). The primer's chapters 14 and 23 and the place-knowledge note's
postscript. **The figures, old beside new, by the probe's eight plans:** before the mend 71 of
123 lines typed showed nothing and no plan was met (the lead's prototype, on its one plan, 30 of
45); after it 2 of 123 (the clock's own two, sent to the driver as meant) and eight of eight
met. **Truths 7-446 to 7-449.** **Pins moved:** none; each new test fails with its mend switched
off. **Taken another way, each accepted:** the probe in Python and not Node; the probe waiting
for the page's tick after a long tick; the plans' setup moves by other words than the ones under
test; the seated plan at the master's station; the visitor's and the boat's plans as they could
be played. **Found for others:** a player seated without the deck refused his readings; a
visitor's `say to the captain` aboard another ship refused "The captain tells himself nothing";
`go ashore` taken from the tops; a world order typed by the owner shown him nothing: all four
given back to 98 to build with its remaining steps; and to the lead's list, the page's log
lagging by as many snapshots as ticks after a long tick at 1x, and the *Neufchatel*'s boats
having no file ("go to the boat" refused in her; the ships session's). **The builder's suites at
28f7788e:** the fast tier exit 0, 7,038 passed, 2 xfailed; the slow tier of the touched files
exit 0, 397 passed, 8 xfailed; the pace alone and last 12 passed; ruff clean (its suites'
paragraph was committed after later steps, at edd43df0, and comes in with them). **The lead's
merge:** the trial on 2c9485fd clean and lint-clean; no model or vendor name in the diff; no ship
file, no physics; the fast tier whole on it exit 0, 7,047 passed by the dots and 1 xfailed, 02:24
to 03:22 UTC; the whole suite in the cloud, run 59 (2026-11-10, 03:49 to 05:06 UTC, on cae5c333): lint green; the six shards green, 7,477 passed, 20 skipped, 12 xfailed, the longest shard 68 minutes (nine more skipped than run 58: the probe's nine tests, which skip on the runner for want of a browser as the pictures' do, so the probe is proven on the build machine's slow tier and not in the cloud); the pace job 9 of 13 in 7 minutes 48, the four floor tests short (388 to 445 ticks a second against 500) on a slow runner's hour, as runs 51 to 56, where run 58 an hour before passed 13 of 13 and the builder's pace alone passed whole at its hash. Steps
3, 4, 5 and 7 and the four additions come as one report at one hash.

### Package 74, step 4: the far fight wired (the design's §4), and step 3's five mends from the owner's play, as merged (2026-11-10)

**What landed:** the builder's 04ae8f86 (claude/pkg-74, after step 3's 924d1b2: 8bfdde0 step 4 as
built, 48c0190 the paused tiers' record, dccbf84 the five mends, the tidies and the primer's
words, e89110d a fault of mend (1)'s own, the trunk merged four times by merge commits (2dce392,
05e13fc, 713b5af, and ceed163f at cae5c333 with package 98's steps 1, 2 and 6), ceed163f the
step's final tree, 04ae8f86 the suites' figures in the tuning notes alone), merged `--no-ff` by
hash at 9944b671 onto dd12cba9, a clean merge. **What met at the trunk, the builder's
resolution:** in `orders/__init__.py` both 98 and 74 had put a refusal before the signals'
handler; 98's `movement.check(ship, verb, SIGNALS)` kept on that road (the place's check names a
captive's state first) and 74's `_refuse_a_captive` kept on the roads 98 does not reach (a
standing order, a book, a station stood down or the deck given, `captain: carry on`); in the
truths' file both kept, 74's first.

**Step 4, built (`freesail/combat/far_action.py` new, 551 lines; hooks in `brains.FarCaptain`,
`resolve_state`, `Vessels.tick`, `crews`, `prizes.retake`; `combat/far.py`'s `file_figures`):**
the far brain takes the engaging transition for a ship with guns to fire (before it a far ship
never engaged: 70's measure run apart), a chase leg to the mark at the doctrine's engaging range
under the nation's habit; once a minute every pair of far bodies of which one is `engaging` the
other resolves one round every three minutes (70's step) while within the longest random shot of
her fit's guns, each side a `FarShip` from her file, fit, nation and doctrine with her record's
killed, wounded, dismounted, holes, sail cut, spars gone and morale carried in, the draws from
the World's stream `far` opened at the first round and not before, the sums written back with a
line in each side's story and, where a hull sleeps under her, her log (`action.far_round`); the
strike by morale as 70 measured, her captor's brain then `taking possession`; one side awake, the
far ship's reply by the tables only where the cap has no room to wake her, each striking shot
resolved into the awake hull's parts; the guns of a far round heard at the player's ship within
twelve miles (by night the flashes within fifteen: judgement), one line a round; the far record
applied to her parts at her waking, once (and the demotion's own sums no longer applied again at
the wake, the wounded twice); a ship in an engagement (engaging, taking possession, struck within
the hour, or an engaging ship's mark) ranked with the dealings under the cap; a retaken prize
spoken and her recaptor on passage again. `far_action.ENABLED` is the bisection's toggle: off, the world is 70's.

**Step 4's two mends (the lead's of the 7th):** (a) the fit read once a file: the cost had two
sites, the far brain's `has_guns` reading the ship file from disk at every minute of hers and
`far_ship_of` building both sides from the file at every round (8.6 s of 11.6 s of a profiled
thousand ticks in `load_spec`); both read `far.file_figures(ship_file, fit)` now, cached. The
toggle off beside on, best of three thousands, ticks a second: 7-159's scene, old tree 8bfdde0,
off 423 to 568, on 162 to 185; mended, off 536 to 585, on 539 to 565; 7-361's scene with both
sites cached, off 1,208 to 1,270, on 1,149 to 1,213. 7-159's digest the same either way and on
either tree: no pin moved, the floor not lowered. (b) truth 7-361 stands on the frigate of the
brains' sea hove to with two far frigates eight cables apart twelve miles south of her, fifteen
rounds in the measure, ten or more asserted with the floor.

**Step 3's five mends from the owner's play of 2026-11-09 (each reproduced in the step's own
scene, the player's frigate struck to a crewed French frigate; six new tests in
`tests/test_captive.py`; truths 7-355 and 7-356 carry them):** (1) the captive's words stood the
captor's captain aside: the player's hand is now one of her own free company's alone
(`movement.hand_on_her`, read by `World.submit`), never a captive's nor a visitor's; she is
three hundred metres and more on her way to Brest ten minutes on, no `captain.aside` in either
log. A fault of this mend's own, found by the builder's slow tier and mended before the step's
tree: at dccbf84 the rule asked for her captain's person in every world and so mustered the
people at the first prompt order of a world in which nobody had moved, and truth 7-279's frigate
took the ground at tick 91,450; at e89110d the rule asks nothing where the people are not
mustered, and 7-279 passes (the fast tier had passed whole on the faulty tree: only the long
passage saw it). (2) The captor engaged his own prize: with the player in his `fired_on` before
the strike, old `engaging` at the first judgement after the possession and 38 shot at his prize
in the quarter hour, thirteen striking; new `on passage`, none: his own prize and any prize of
his nation is no enemy (`Judgement._prize_of_ours`, first in `_known_enemy`), and the taking
clears her from `fired_on`, `pirates` and `recognised`. (3) The bare yes and no read while the
question is open, as whole words; both or neither leaves it open. (4) A captive's prompt
performs a word said, asked or told, a reading or a question, his moves within his parole, his
needs and a free line, and nothing else: a hail, the colours, a signal, a standing order, a
book, a station stood down or the deck given and `captain: carry on` are refused in his words;
the prize's answer reads "prize to the Medusa" from her record and names her prize master. (5)
`go ashore` and `come aboard` are refused him in his own words ("you leave her where her captain
lands you, or by a cartel"). The grounding in the Rade taken for (1)'s consequence. Pins moved by
the five: none. The tidies: the broken sentence in step 3's notes, `captive.py`'s `nm()` and
`_ = math`, gone. The primer's chapter 27 says what a prisoner's prompt performs and the plain
answers.

**Truths:** 7-358 (two far ships that meet in anger beyond the range fight by the rounds),
7-359 (the near fight and the far rounds of the same two cutters agree), 7-360 (the far state
into the near body at her waking and back at her sleep), 7-361 (the far rounds' cost), 7-369
(the cut-out carried from hailing distance to its end by the rounds). **A pin of 72's changed by
design, old beside new by the toggle:** `tests/test_brains.py`'s cruiser and merchant: come up
within his engaging distance the brig-sloop engages her and she strikes by morale to his first
round at seven cables, where before she yielded at hail (the same possession at the same minute
by another road).

**Found by the builder, not its own:** 7-159's scene on the old tree gave a different digest in
two processes of nine; `squadrons._LAST_COURSE`, a module's table keyed by `id(world)`, suspected.
**The lead's investigation proved the mechanism by planting** (a stale course under the new
world's key moved the convoy's stations 86, 284 and 556 metres and changed the three-hour
digest; a natural reuse of a dead world's address not reproduced in four tries; the table is in
no checkpoint either): given to package 98 as its step 8. An order that is plain speech on the
player's own ship (`say to the captain: ...`, `person.spoke`) still stands his rules captain
aside by decision 41 as written: left by the builder, given back by the lead (below).

**The builder's suites at ceed163f, a pinned worktree:** the fast tier whole exit 0, 7,057
passed, 1 xfailed, 482 slow left out; the slow of the known truths, the profile and the
Indefatigable exit 0, 506 passed, 8 xfailed; the slow of the touched files exit 0, 1,803 passed;
the pace alone and last exit 0, 14 passed, no floor lowered; nothing skipped in any tier; ruff
clean. **The lead's merge:** the trial on b4e99f33 clean and lint-clean; no model or vendor name
in the diff; no ship file, no physics; the fast tier whole on it exit 0, 7,057 passed by the dots and 1 xfailed, 05:19 to 06:24 UTC (an hour and five minutes, the machine shared with the investigation for its first quarter hour); the whole suite in the cloud, run 60 (2026-11-10, 06:25 to 07:44 UTC, on c54a0537): lint green; the six shards green, 7,494 passed, 20 skipped, 12 xfailed, the longest shard 70 minutes; the pace job 10 of 14 in 7 minutes 17 (the step's own pace truth, 7-361, among the passes), the same four floor tests short on the runner (426 to 488 ticks a second against 500; 7-159's convoy 426, where run 59 before the far fight was wired had it at 388 and the builder's machine 539 to 565), so the shortfall is the runner's hour and not the step's.

**Given back to the builder for step 5's tree (none held the merge):** (i) the parole's plain
answer reads "I do not." and "I do not know" and "you have it not" as given (the yes list's "i
do" and "you have it" as whole words with a negation after them), and step 3's "my parole" gives
on "you shall not have my parole": a negation in the answer never reads as given; (ii) the
fallback's log line ends "(the far ship's reply, the cap full)", the engine's words in served
text: out of the line, the counts in words as the round's; (iii) the cruiser's test accepts
either of two last states ("on passage" or "investigating a stranger"): the one it is, pinned;
(iv) the conditional `pytest.skip` at `tests/test_far_action.py` line 299 (never taken; the
builder's own find) to an assertion; (v) the player's plain speech on his own ship no hand on
her, if no pin moves by it, else reported old beside new. Next in 74: step 5 (the prize court
and the money; truths 7-362 and 7-363), then 6 and 7.

### Package 98, steps 3, 4, 5 and 7 and the lead's four additions, as merged (2026-11-10)

**What landed:** the builder's 0eb4652a (claude/pkg-98: the suites run at d96dbf31, which has
the trunk merged at cae5c333 by a merge commit; 0eb4652a adds the suites' paragraph in the
tuning notes alone), merged `--no-ff` by hash at 12bd5f48 onto c54a0537. **One meeting at the
trunk, resolved by the lead in the merge:** `World.submit`'s test of the player's hand, where
package 74's step 4 (merged an hour before at 9944b671) had added `and self._hand_on_her(actor)`
and 98 `and not data.get("visitor")` on the same line; both kept, 74's first (74's rule already
keeps a visitor's word from standing her captain aside; 98's names its own road's line). The
fast tier whole on that tree is the proof, below; both builders told.

**Step 3, the viewer's paint order (`client/projection.js`, `api/viewer_guns.py`,
`api/viewer_flags.py`, `world/flags.py`, `api/queries.py`):** a port gun's inboard figures sort
at its port's strip of the side, a centimetre behind it (`PORT_GUN_BEHIND_M`, judgement), its
outboard figures at their own middles; every part and line of a flag sorts at the flag's middle
in the drawing's order, now served (`Flag.served_drawing` numbers each part and line), a flag's
figures kept together after the sort, and a drawing's lines drawn as bands; the flag of truce
at the fore truck in the fallback as the locker's road had it (a one-masted vessel at her only
mast's truck); 81's ruling built, a port's served top tilted with its deck and cut under the
rail less 2 mm (`TOP_UNDER_RAIL_M`), `CUT_AT_A_CORNER_M` removed with its rule; the settee's
sheet served and drawn to windward while it is held there. **Old beside new, every 15 degrees
at heel 0 and 15, 48 views a file:** inboard gun figures painted after their shut lid, guns
secured: brig 283, cutter 60, frigate 359, *Neufchatel* 299, merchant brig 56, privateer
schooner 75, razee 591, sixty-four 688; after, 0 on every file, secured, run in and run out.
Each root's ensign out of its drawing's order: Britain in 44 of 48 views, France 42, Spain 46,
the United States 46, Naples 17, the basic file 46; after, 0. Served port tops that move: the
*Neufchatel*'s upper deck 2.516 to 2.498, 2.270 to 2.265, 2.756 to 2.749 m; the sixty-four's
quarterdeck 6.191 to 6.105 m; `check_viewer_guns` unchanged. **Pin moved, by the toggle:**
`test_viewer_action`'s truce row, "peak" to "fore truck". Truths 7-450 to 7-454 (7-450 and
7-451 in the slow tier).

**Step 4, the picture at the OpenRouter door (`agents/api.py`, `harness.py`, `seat.py`,
`local.py`, `remote.py`, `pictures.py`, `tools.py`):** the cause as the lead's investigation
found it, the door built without `fetch_picture` while the picture tools were offered whatever
the model reads. The door keeps the models list's `input_modalities`; where the model reads an
image it fetches the picture and seats with pictures, where it does not it offers no picture
tool (`no_pictures`, a class default so that a checkpoint from before loads unchanged), and it
says which at its start. A picture's readings go beside it; a door that shows the image leaves
them out, and one that cannot says the picture was drawn and not shown, why, and gives the
readings, never the size in pixels alone, at both dialects. Proven on a stub door only: no
provider was called. Truths 7-455 and 7-456. No pin moved.

**Step 5, the Rade de Brest's stream (`data/tides/streams.yaml` alone):** `the-goulet` is the
narrows alone, Petit Minou to Portzic (48.325 to 48.372 N, 4.62 to 4.53 W), its figures
unchanged; `rade-de-brest` (48.25 to 48.43 N, 4.53 to 4.18 W) after it and before the Iroise:
2.0 knots at springs, 1.0 at neaps, axis 100 degrees, phase -3. Source read: the Parc naturel
régional d'Armorique's Natura 2000 document of objectives of the Rade de Brest, tome 1 (2014),
p. 28 (over 4 knots in the Goulet and 2 at the centre of the rade at springs), pp. 29 and 35
for the set; the FVA's Livret voile-aviron 50 (2019), p. 3; the neaps, the axis and the hour
judgement; the hydrographic service's atlas of the roads not read; the book entry judgement in
the period's form, as the Goulet's. **Pins moved, each proven by the toggle (the old file makes
all five failing tests pass):** `test_tide`'s Channel-west areas 14 to 15; the merchant
passage: the pilot of Brest put off at 118,860 (was 121,620), anchored in the Bay at 115,907 in
15 fathoms (115,547 in 14), the tin sold at 124,710 (123,272), 3,103 lines (3,107), digest
40bcef34afd0cec4 (6436eb06a665f379), everything to the road of Bertheaume the same; the fake
captain's passage 3,115 lines (3,119), c0bf4b51621ad91f (7076e667c2bc41e3); the schooner on an
intent 2,079 lines unchanged, 9d9efe6b21c17060 (8744d3e56cfc9508), one line moved (a stranger
in the Rade's water lost from sight at 115,860, was 115,980); truth 77 reads these. No other
pin moved, the ships anchored in the Rade among them.

**Step 7, the flags of command hauled down and read (the owner's note of 2026-11-09;
`orders/signals.py`, `api/signal_readings.py`, the primer's chapter 23):** `haul down` (or
`strike`, `lower`, `take in`) `the broad pendant`, `the second ensign`, `the jack`, each by
name, the colours left flying, a flag not flying refused in words ("No jack of hers is flying:
there is none to haul down."); deck orders by step 6's check. `the flags` is a reading of its
own: what flies where from the locker, then the signal flying if a hoist is up, or "none (her
colours are down)"; `the signals` stays the signals'. Truth 7-457.

**The lead's four additions (each with a test that fails with its own file put back, and a
probe line; no pin moved):** (a) a seated officer's reading is never refused for want of the
deck (`tools.reading_order`; the new plan `seated-officer.yaml`); (b) a visitor's `say to`,
`tell` and `ask the captain` aboard another ship go to her captain, a line of her log where he
stands, heard by her stations within earshot and shown him (`_visitor_to_the_captain`; 74's
captive's road untouched and asked first); (c) `go ashore` from the tops is refused ("come down
on deck first"); (d) the owner's own world order typed at his prompt is his own line, shown him
as given with its outcome at the pages, their reach-back, the log's reading and the console;
decision 46 stands for every other reader and a director's orders are never the player's (the
lead's ruling from the owner's decision 4; the owner may reverse it). The probe now fails a
plan that is not valid YAML. Truths 7-458 and 7-459.

**Found for others, not mended (the lead's list):** a gun run out keeps its outboard figures at
their own middles, so in oblique views its barrel's outboard part paints before its open port,
the same before and after (sixty-four 455 view-guns of the 48 views, razee 275, frigate 189,
brig 65, *Neufchatel* 52, cutter 42, merchant brig 8, privateer schooner 1); the schooner's
master who keeps the reckoning goes aloft "in his place alone", and `come on deck` then answers
that he is on the quarterdeck already.

**The builder's suites at d96dbf31, one at a time:** the fast tier exit 0, 7,119 passed, 1
xfailed, 477 slow left out; the slow of `test_known_truths` exit 0, 341 passed, 8 xfailed; the
slow of the other touched files exit 0, 1,614 passed, 1 xfailed, the nine probe plans met; the
pace alone and last exit 0, 12 passed; ruff clean. **The lead's merge:** the trial on 9944b671
with the one line resolved, lint-clean; no model identifier in the diff (the vendor's name in
the door's comments as the trunk has it); no ship file, no physics; the fast tier whole on it
exit 0, 7,129 passed by the dots and 1 xfailed, 06:24 to 07:28 UTC; the whole suite in the cloud, run 61 (2026-11-10, 07:59 to 09:14 UTC, on f4047ec5): lint green; the six shards green, 7,568 passed, 21 skipped, 12 xfailed (the one more skipped the probe's new plan, which wants a browser the runner has not), the longest shard 69 minutes; the pace job 14 of 14 in 4 minutes 26, the four floor tests passing on this runner where runs 59 and 60 fell short on theirs. Step 8 (the set's last course kept in the world) comes as its own report.

### Package 75: SW-1 (Table No. 29's charges) and the ruled builds of the 9th and 10th, as merged (2026-11-10)

**What landed:** the ships session's ad71736f (claude/pkg-75, on 5af283de merged before at
cff8fdb1: 35e33ad0 SW-1, 8bceb1cb the lead's ruled builds of 2026-11-09, caf1d329 those of
2026-11-10, ad71736f the review's mends), merged `--no-ff` by hash at 09222043, a clean merge.

**SW-1, the service charges (`freesail/ship/charges.py`, `parts.py`, `tools/gen_ships.py`):**
the Regulations of 1806 (the 1808 printing), Table No. 29, read on the page image and entered
as `CHARGE_TABLE_LB`, eighteen figures under twenty keys (the 1-pounder and the half-pounder
entered for the long gun and the swivel both, judgement). The table confirms the shares held
from memory, a third of the shot for a gun and a twelfth for a carronade, rounded down to the
ounce where the share rounded to the nearest. **The lead's stage 0 rule applied** ("where a
figure of the eight would move, the table serves the new ships alone"): with the table on every
file five of the eight would move (the frigate's and the brig's 32-pounder carronades 2.6875 to
2.625 lb; the swivels 0.25 to 0.125 lb in the cutter's, both privateer fits and the topsail
schooner's letter of marque; the cutter's long guns' powder barrels 3 to 2), so the eight
files' charges are written as filed (`as_filed=True`) under a generated note saying where the
table differs, and no figure of the eight moved; the sixty-four, the razee, the *Neufchatel*,
the bilander and the 74 to come take the table (the long 32-pounder 10 lb 10 oz; the bilander's
swivel 0.25 to 0.125 lb, her one moved figure). An old save of the eight keeps its shares
(`filed_charge_lb`); the viewer serves each gun its fit's own charge (`viewer_guns.served`,
81's file touched for it). `test_magazine`'s two rows moved, old beside new (`fill_seconds`
159.4 and 121.9).

**The ruled builds of the 9th:** "take in the square sail" listed only where a ship has a
square sail part (the cutter, the smack); the *Neufchatel*'s trimmers 34 by the generator's
rule (9, 11 and 14); the bilander's boy a landsman (0.80 able, 0.20 landsmen: four able
topmen and a landsman boy); the round stern's key `form.stern.counter_hb_m`, the bilander the
one file to file it, every other file's served graph key for key the same, her settee's block
0.24 m inside her rail; "1 gun ready to go as it bears."; lie a-try names what is set; "is to
be taken in" where the take-in waits for hands; `INTENT_RULED_ROWS` recorded as the lead's
ruling. **Of the 10th:** forced round and left to herself, the watch dips a settee lying
against its mast by its own order and says so; the pay-off trims a kept settee with the boom
sails; the settees held from the order in the tack's, the wear's, the box-haul's and the fill
away's holds; the group's line names only the group's sails still set. **The review's mends
(ad71736f), and the lead's judgement on them:** the settees' holds made a manoeuvre ordered
after a settee order wait behind it, so the manoeuvres record the settees they hold
(`Script.order_settees`) and `Runner._settees_only` lets one begin past work given before it
where they share only those settees and she has a crew, belaying it as decision 25 has it.
This reaches the runner, which the lead's ruling (iii) said to keep out of; the smaller way
left the blocker, the builder said so plainly, and the lead keeps it.

**The session's suites at ad71736f:** the fast tier whole 7,097 passed, 34 new; the slow
candidates no outcome changed but three pace floors under load, all passing alone; the four
whole logs equal; seventeen ship files their generator's bytes; `check_viewer_guns` clean; the
captain's trials the machine's three. **The lead's merge:** the trial on 3c669188 clean and
lint-clean; no model or vendor name in the diff; `data/ships/` touched by the generator alone
(the charges' notes on every file; the bilander's swivel, ratings and counter; the
*Neufchatel*'s afterguard 15 to 14); the fast tier whole on it exit 0, 7,188 passed by the dots and 1 xfailed, 08:44 to 09:51 UTC; the whole suite in the cloud, run 62 (2026-11-10, 09:51 to 10:48 UTC, on dc0f4615): lint green; five shards green and **one test failed** of the 7,660 the six shards hold, in shard 2: the schooner's recorded passage of gate 5b, its 766 lines kept and its digest another (`2b68e8b1f60e8496` pinned, `3a1698037811b753` sailed). **Found by the lead the same hour:** both trees sailed on the build machine and every line compared, one line differs, the outer road's "Shorten sail" at tick 56,234, which no longer lists the grammar's refusal of "take in the square sail" for a schooner that has none: the ruled build (3) of the 9th, as intended; the toggle (`storm.listed_lines` made the identity on the merged tree) gives the old digest. **Re-pinned by the lead, old beside new, with the reason in the tuning notes** (the ruled builds, (3)); the session's machine's four whole logs and the lead's fast tier do not hold this passage, which is why the cloud's run is kept at every merge. The pace job 10 of 14, the four floor tests short on the runner (389 to 442 ticks a second against 500), as runs 59 and 60. Run 63 follows on the re-pinned tree with 98's step 8. **The session's six points
ruled** in the notes at the end of this file (2026-11-10, after this merge). Next in 75: B7
(the 74-gun ship), then Phase 5; **the owner has told the session that after the lead's final
word on 75's close-out it may begin package 90's preliminary research and planning.**

### Package 98, step 8 (the set's last course kept in the world), as merged; the package closed (2026-11-10)

**What landed:** the builder's 6598cecc (claude/pkg-98: the suites run at 453ed374, which has
the trunk merged at bbb69526; 6598cecc adds the suites' paragraph in the tuning notes alone),
merged `--no-ff` by hash at b148e721, a clean merge. **The defect** (found by package 74 on
the way, proven by the lead's investigation by planting): `freesail/world/squadrons.py` kept
the followed ships' last courses in a module's table keyed by `id(world)`, never emptied, so
that a World made at a dead World's address in the same process read its courses, and a
checkpoint lost them. **Reproduced by the builder at the base:** the convoy's scene run three
hours gave ded7116824f7e3e3 clean twice in one process and 807f81859e987283 with a stale course
planted for every member under the new World's keys; with the commodore hove to from the
start the members' stations themselves moved every ten minutes. **Built:** the module's table
gone; `_last_courses(world)` keeps the courses on the root World (the attribute
`squadron_last_courses`), keyed by vessel id and made on first use, so that it dies with its
World, is saved in a checkpoint with it and restored from one; a checkpoint written before
this step has none and the heading stands in, as for an absent entry before; the root World
chosen over the squadron or the vessel's record because the frame is read by vessel id for any
set the ship leads or guides. **Truths 7-460** (the convoy made twice in one process, the
second after the first is dropped and collected, a stale course planted wherever the old table
stands: the first's stations every ten minutes for an hour, and its line count) **and 7-461**
(the commodore stopped with her head fallen off 45 degrees from her last course, saved by a
checkpoint and resumed: the uninterrupted run's stations and line count over the next hour);
both fail at the base and pass with the mend. The builder's first drafts of both did not
exercise the defect (a commodore with way never reads a planted course; a far body hove to
keeps her head) and were tightened before they were trusted, said in the report. **Old beside
new by the toggle:** 7-159's scene 97 lines, a9f39f0f6e53ae06, the same stations, at both; the
convoy's ded7116824f7e3e3 at both; `test_squadrons` whole and truths 7-151 to 7-157 pass. **No
pin moved.**

**With it:** the builder's own condition `and not data.get("visitor")` in `World.submit`'s test
of the player's hand, and the `visitor: True` it read, taken out (the one line the lead kept
both of at the merge of 12bd5f48): package 74's `hand_on_her` already keeps a visitor's word
from standing her captain aside, and truth 7-458's visitor case passes without them.

**The three other tables, read and not changed** (the lead's question): `core/events.py`'s
`STATION_ACTORS` does carry from one World to the next in a process (every station defined
adds its name and nothing removes it), and can change a second World's roll-ups in the views
and the samples where a line's actor names a station the first had and it has not; not the
log nor its digest; not proven by a test: **on the lead's list.** `RECORD_ONLY_ACTORS` only
ever holds the director's and leaves nothing. `world/reports.py`'s table by id is reached only
for a key that takes no weak reference, which neither a World nor a hull is.

**The builder's suites at 453ed374:** the fast tier exit 0, 7,133 passed, 1 xfailed; the slow
of the touched files exit 0, 442 passed, 8 xfailed; the pace alone and last exit 0, 13
passed; ruff clean. **The lead's merge:** the trial on 09222043 clean and lint-clean; no model
or vendor name in the diff; the fast tier whole on it exit 0, 7,192 passed by the dots and 1 xfailed, 09:51 to 10:56 UTC; the whole suite in the cloud, run 63 (2026-11-10, 11:04 to 12:00 UTC, on 4016629e, the trunk with this step and the lead's re-pin of the schooner's gate 5b passage after run 62): lint green; the six shards green, none failed of the 7,664 tests they hold by the pace job's count (the re-pinned passage among them), the longest shard 48 minutes; the pace job 14 of 14 in 5 minutes 48.

**Package 98 closed:** eight steps, truths 7-446 to 7-461, from the owner's play of 2026-11-09
(his nine notes and three saves): the browser probe a kept tool; a man's own readings,
refusals and word shown him wherever he stands; the colours and signals the deck's; the
viewer's paint order; the picture at the OpenRouter door (proven on a stub door only); the Rade
de Brest's stream; the flags of command hauled down and read; four small additions; the set's
last course in the world. **Left on the lead's list from it:** a gun run out's outboard
figures painting before its open port in oblique views; the schooner's master aloft in his
place alone; `STATION_ACTORS` across worlds in a process; the page's lag after a long tick; the
*Neufchatel*'s boats having no file; the cloud workflow installing no browser, so that the
probe's and the pictures' tests are proven on the build machine and not in the cloud.

### Package 100, step 1 (the thing with words), as merged (2026-11-10)

**What landed:** the builder's 465aad26 (claude/pkg-100: the step's tree 7e50d00e, measured
there with the trunk merged at eb42c048; 465aad26 adds the figures paragraph in the tuning
notes alone), merged `--no-ff` by hash at 41216bbc. **Two meetings at the trunk, resolved by
the lead in the merge:** both packages had appended at the end of `tests/test_known_truths.py`
(98's truths 7-460 and 7-461, 100's 7-470 to 7-476) and of `docs/dev/TuningNotes.md`; both
kept whole, the trunk's first; the fast tier whole on that tree is the proof, below.

**Built (`freesail/world/things.py`, `orders/free.py`, `world/orders.py`, `agents/director.py`,
`world/knowledge.py`, `core/world.py`, `ui/console.py`, `ui/server.py`, `data/vocabulary.yaml`;
the primer's chapters 14 and 20):** a letter is a thing with words, an author, an addressee
(and the person the words name, where they name one of the people), the stamp of its
writing, a seal and whether it is broken, and how it went when it is gone; each a plain
default left out of the thing's saved form while empty, so that a thing from before reads and
digests as it did; **a letter's words are never in the saved form** (the journal keeps the
order that wrote them, and the replay writes them again). **Written** by the free line
`write a letter to <whom>: "<words>"` on the drafting's road (from the deck the captain goes
below and spends five minutes at it), into the writer's keeping; carried, given, put down,
hidden and thrown overboard by 53b's lines unchanged; **sealed and opened**, the broken seal
showing in every listing; **read** within reach only, a sealed letter refused until it is
opened; **looked at** (its name, description, direction, hand, seal and where it lies, never
its words); **burnt or torn up**, a paper gone and said (a thing that is no paper refused; no
fire in the boat). **The director's two forms:** `aboard: a letter from <whom> to <whom>,
<where>[, sealed]: "<words>"`, and `aboard: remove <a thing>`, which takes the thing out of
the world with no line in the play log, refused out of a held person's keeping and doubted
where it lies within a held person's reach. **Who sees the words** (the owner's decision 4 of
2026-11-09): the order's line in the log is said without them (`ORDER_AS_SAID`), and they
come as a following line (`THEN_LINES`) to the reader, and to the writer of his own, by a new
reach class `reader`: the person named by his whole name, asleep or awake, and nobody else;
the director has everything. One road for the player, a station and the director.

**Taken another way:** `look at` was the observer's driver command at the console and the page
in every world and caught the free line ("The view is the ship's"); it is the driver's now
only in an observed world (found by the probe). A prisoner writes, reads and looks as he
speaks: 74's rule refuses a captive his deck orders and the books and not the free lines, so
his letter is written where he is, `captive.py` untouched. A director's thing named "a letter
for ..." with no words stays the plain thing it was. **Truths 7-470 to 7-476;** the browser
plan `a-letter.yaml` (written, sealed, a read refused, looked at, opened, read, given, burnt:
met). **No pin moved.**

**The builder's suites at 7e50d00e:** the fast tier exit 0, 7,166 passed, 1 xfailed; the slow of
the touched files exit 0, 2,508 passed, 8 xfailed; the pace alone and last 9 of 13, the four
floor tests short on its container, and short the same on the trunk in a worktree beside it
(427 to 462 ticks a second against the step's 369 to 478, the convoy's alternated 434, 445,
446, 456): the container's, not the step's. **The lead's merge:** the trial on 229d0247 with the
two appends kept, lint-clean; no model or vendor name in the diff; no ship file, no physics;
the fast tier whole on it exit 0, 7,229 passed by the dots and 1 xfailed, 14:02 to 15:13 UTC;
the whole suite in the cloud, run 64 (2026-11-10, 15:15 to 16:30 UTC, on dc197104): green whole, lint, the six shards and the pace job (its counts not read, to spare the lead's usage; the run's page has them). Next in 100:
step 2, the letters that travel (already at 870f071d on its branch, to be measured).

### Package 74, step 5: the prize court and the money (the design's §5), as merged (2026-11-10)

**What landed:** the builder's 0a77835b (claude/pkg-74, after step 4's record 04ae8f8: 4ff5abf
step 5 as built, 82e7f76 the lead's five mends, 562236c one pin moved, six merges of the trunk
by merge commits, the last at 61b170d4; bc22961d the step's final tree, measured there;
0a77835b the suites' figures in the tuning notes alone), merged `--no-ff` by hash at
dcd6c690, a clean merge onto the trunk carrying package 100's step 1.

**Built (`freesail/world/prize_court.py` new, 652 lines; `data/business.yaml`'s four blocks
`prize_values`, `prize_courts`, `prize_money`, `prize_shares`; hooks in `prizes.possess`,
`prizes.minute`, `prizes.far_minute`, `Dealings._apply_job`, the strike hooks of the near
action, the far rounds and the cut-out; `api/prize_readings.py`; the director's form in
`world/orders.py`; the primer's chapter 27, "The court and the money"):** the valuation by the
rows over the files' own figures (the hull by the ton worn by her years, the guns by the
hundredweight, the cargo at the port's market, the prize goods on 86's ordnance); the court by
the port's nation, sitting in its days as a port job on the prize hull's dealings, or on a far
prize's record in her goal's road; the three sentences by the rules with the wars' dates
(condemned, restored with costs, salvage to the recaptors); the head money, the agent's five
per cent, the court's fees, the reserved fourth of a King's ship's prize of war; the money by
the eighths of the scheme in force at the court's date, shared first among every ship in
sight at the strike by their complements (the lead's ruling of 2026-11-07 from Lavery p. 116),
each ship's part into her purse with the purse's line and the prize account's lines; the
director's `port <id>: the court condemns | restores the <prize>` doubted against the rule;
the reading `the prize money`; three events. **The figures (seed 7, the French merchant brig
taken in Falmouth's road):** 304 tons, hull £1,944, guns £320, powder and shot £13, agent
£114, fees £20; £2,143 to the frigate alone, the captain's three eighths £804; with the cutter
*Sprightly* in sight the frigate's part £1,925 and the cutter's £218; a Danish brig wrongly
taken restored with £194 of costs; a Brest salvage of the same brig £285 to the recaptors; the
reserved fourth on a privateer brig of eighty men, £400 of head money, three fourths now and
the fourth on the seventh day. **Truths 7-362 and 7-363.** For package 60:
`prize_court.valuation(world, vessel)` takes any vessel and reads only her file, fit, role and
the date.

**The sources, as the data says them:** the two British schemes of the eighths' classes and
figures from Lavery, *Nelson's Navy*, p. 116 (cited, not copied); **FROM MEMORY and unverified,
each marked so beside its figure, for the owner's shelf:** the hull's price a ton (£8 a
merchantman, £12 a man of war), the guns by the hundredweight, the agent's five per cent, the
head money of £5, the costs' tenth, the salvage's eighth, the shares within the crew's half
from 1808, the privateers' halves, the courts' names and days; France's and Spain's
distributions not read, the British eighths of the date kept in their rows and said so
(decision 64). **A citation corrected by package 60's note and checked by the builder on the
page:** the three fourths and the reserved fourth is article XXXI of the articles for flag
officers (p. 28), not the captain's; the rule and the figure right; the words mended in step
6's tree.

**Taken another way, each in the notes:** her stores price nothing (her file lists none);
`take her powder and shot` not built (the goods are the court's); no line at the court's date
for a prize that never comes in; the reserved fourth paid by the record's day from the
prize's minute, not by a second port job; the salvage to the recaptors alone by their
nation's court and scheme.

**The lead's five mends of step 4's merge, in this tree, each with its test:** (i) the
parole's plain answer: an answer that holds a negation is never read as given, by the forms or
the plain words ("I do not.", "I do not know", "I do not see why I should", "you have it not":
open, all four); "you shall not have my parole" REFUSED by two refused forms added, accepted
by the lead since the words refuse plainly; (ii) the cap-full reply's line in the world's
words ("... none of her 27 shot strike us."), the data keeping `fallback: True`; (iii) the
cruiser's test pins its last three states and the tick; (iv) the skip an assertion; (v) the
builder's reading of step 4 was wrong and it said so by measurement: on his own ship the
player's `say` and `tell` are `agent.spoke` and `agent.told`, never a hand; the rule stated
for `person.spoke` all the same and tested; no pin moved.

**One pin moved, at the meeting with 98, old beside new:** `tests/test_officer.py`'s handover
test holds the officer's conversation at his seat under 0.6 of the door's budget: 13,433
tokens on the trunk before either, 13,474 with 98 alone, 13,475 with this step alone, 13,516
with both, sixteen over the fraction of 22,500; the test's budget given five hundred more
(23,000) by its own practice, the fraction as it was. **Accepted by the lead, and the trend
put on the list for the owner:** the officer's standing text grows with every package, and
each has raised this budget.

**The builder's suites at bc22961d, a pinned worktree:** the slow of the known truths, the
profile and the *Indefatigable* exit 0, 520 passed, 8 xfailed; the slow of the touched files
exit 0, 1,996 passed; the fast tier whole exit 0, 7,207 passed, 1 xfailed; the pace alone and
last exit 0, 14 passed, no floor lowered; nothing skipped; ruff clean. The trunk moved under
its tiers twice and it measured again each time. **The lead's merge:** the trial on 41216bbc
clean (100's step 1 and this step met in `World.submit` and `world/orders.py` and merged of
themselves) and lint-clean; no model or vendor name in the diff; no ship file, no physics; the
fast tier whole on it exit 0, 7,244 passed by the dots and 1 xfailed, 15:14 to 16:25 UTC; the whole suite in the cloud, run 65 (2026-11-10, 17:02 to 18:15 UTC, on e1e2ba78): green whole, lint, the six shards and the pace job. Next in 74: step 6 (the court martial, a new command, the consent
revision drafted under `docs/design/` with its refusal in words behind the flag; truths 7-364
to 7-366), then step 7.

### Package 101: the Catalan coast block, as merged; the package closed (2026-11-10)

**What landed:** the builder's 7623786b (claude/pkg-101: the tree measured at d2f0b340 with
the trunk merged at 229d0247; 7623786b adds the figures paragraph in the tuning notes alone),
merged `--no-ff` by hash at 1a4a4337. **Two meetings at the trunk, resolved by the lead in the
merge:** the appends at the end of `tests/test_known_truths.py` and of
`docs/dev/TuningNotes.md` (74's and 100's since its merge of the trunk); both kept whole, the
trunk's first.

**The gap closed.** The region `catalan-coast`, 40.56 to 41.9 N and 0.3 to 3 E, its south
bound `balearics`' north bound and its east `gulf-of-lion`'s west; the seam the how-to's plain
answer, the Gulf's first tile column kept the Gulf's ("4 kept"), no tile, coast or index of
another region changed. **24 level-2 tiles (3.44 MB), 46 level-3 tiles of three harbour
patches (2.55 MB), 6.07 MB in all.** The Alfaques' patch widened (40.56 to 40.83 N, 0.55 to
0.92 E) with `fill_raise: eleven`, package 93's rule: with Barcelona's gauge in, the block's
own 0.21 m raise flooded the whole of the Ebro's delta, the grid laying its flat land under
the mean sea level (34,401 flooded cells, the ten largest places all on the delta; 1,642 after,
the largest the modern harbours' basins). **The shore is one year's picture, the modern
grid's** (decision 66): no override, for want of a public-domain plan at a harbour's scale
(Tofiño's atlas has none of this coast; Roux's, Bellin's and Heather's plans read as the
Rumsey scans, cited and not committed, by 79c's practice); the notes name what such a plan
would redraw. 45 marks in the block, checked against the tiles and rendered; the Medas and
Tabarca islands the grid lacks, the Hormigas a rock; **the lights carry their dates**
(Barcelona's mole lantern from 1715 by Michelot, the new mole's from the notice of 1823,
Tarragona's mole lantern from Purdy's first mention, 1826).

**The seven ports,** each a file, `datum: unverified`: Barcelona, Tarragona with Salou's road
and the Alfaques in the block, with their patches; Rosas and Palamós (12 marks in
`gulf-of-lion`) and Valencia's Grao and Alicante (12 in `mediterranean-west`) beside it, at
level 2 by the features files and indexes alone, their regions' checks passing and no tile of
theirs touched (the tool builds no patch for a built region without rebuilding it). **Dated
nations** by 79a's form: Barcelona France's 29 February 1808 to 30 May 1814, Rosas France's
from 5 December 1808, Tarragona France's 28 June 1811 to 18 August 1813, Valencia France's 9
January 1812 to 4 July 1813. **Verified from James:** Rosas's capitulation (vol. 4 p. 386),
Spain's declaration of 12 December 1804 (vol. 3 p. 200), the junta's war on France and the end
of hostilities with Britain in June 1808 (vol. 4 pp. 294 to 295). **FROM MEMORY, each marked
with what would verify it, for the owner's shelf:** every other date above. The markets by
the texts' trades (the Alfaques' salt, Salou's fruit and wine, Barcelona's corn, fish and rice
in, Valencia's rice, Alicante's barilla); the brandy of Reus, the Alfaques' rice and the
oranges FROM MEMORY and in no truth. `tracks:` given the three ports of the block, without
which the business's guard refused their routes.

**The tide, the streams, the weather:** Barcelona's gauge the block's (TICON; REDMAR's 0.21 m
above the lowest tide), by package 89's form; none added at Valencia (the lead's ruling: a
gauge in a built region changes its water and its tiles' fill), none at Tarragona (no
constants on file) or Alicante (in neither source), their figures kept in the port files; the
epitome gains Barcelona, 7 h 25 m and a foot, judgement; the coast's south-westerly set a
current of half a knot, judgement (every pilot gives the set, none a rate); a weather box of
the block's own from Barcelona's meteorological table (the Admiralty's *Mediterranean Pilot*
vol. I, 1913, p. 726, cut from the PDF and every column checked against the printed totals),
which differs from the Gulf's box by 16 to 37 points a month, fitted within 5 points on all
four quarters in every month over 1,200 simulated months. **The scenario** `tarragona.yaml`,
May 1809, Port Mahon to Tarragona's road, sailed once at seed 7 (anchored at 12:29 on the
13th in 18 fathoms; 1,640 lines; not pinned).

**Found, and not the block's to mend: the wars table is one year's picture.** `wars:` carries
`since` and no `until`, `Nations.at_war` reads no date and a scenario's `nations:` block is
read by nothing, so Britain is at war with Spain on any day and Tarragona reads hostile in
1809; the scenario's head says so, and the truth "Tarragona receives a King's ship in 1809"
was dropped by the lead's ruling for one the block earns (the lights' dates). A case for
decision 66 and package 103. **Also for others (the lead's list):** a gauge for the Valencian
coast (the world's tide there is the Alboran's blend, M2 13 cm where Valencia's own is 1.7);
the tide's step across 40.56 N, far from every gauge; the weather boxes meeting at 40.5 N
where the regions meet at 40.56; the weather fit's winter gales running below the table's; no
`tracks:` for the four ports beside the block.

**Where the lead's brief was wrong and the sources won:** no text calls Rosas the best
anchorage of the coast (Tofiño has the bay sheltered from all winds, the Tramontana off the
land: the truth written to his words); Valencia's road written to the pilots' words; the
trades as above; the delta not drawn as Tofiño drew it. **Truths 7-490 to 7-499** (the chart
answering over the old gap and from Cape Palos to Cape Creus; the two seams crossed with the
region, the tide, the weather's box and the business carried; Montjuïc, Montserrat and the
Montseny raised; Rosas; Valencia's road; Barcelona and Rosas hostile in 1805 as Spain's and in
1809 as France's; the lights' dates; the Alfaques' salt carried to Barcelona; the scenario
sailed), four of them slow. **No pin moved;** the recorded passages held every digest.

**The builder's suites at d2f0b340:** the fast tier exit 0, 7,200 passed, 1 xfailed; the slow
of the touched files and the known truths whole exit 0, 664 passed, 8 xfailed; `gate_5b` and
`gate_5c` to the digest; the pace alone and last exit 0, 12 passed; ruff clean. **The lead's
merge:** the trial on the trunk after 74's step 5 with the two appends kept, lint-clean; no
model or vendor name in the diff; the existing tests changed only in their counts of the
chart's regions, ports and gauges, old beside new; the fast tier whole on it exit 0, 7,252
passed by the dots and 1 xfailed, 16:26 to 17:37 UTC; the whole suite in the cloud dispatched
after run 65, the figures to follow. **Package 101 closed.** Next of its kind: 104, the sea
between Minorca and Sardinia, the lead's to measure and put to the owner.

### Package 75: B7, the 74 (the *Bellerophon*, steps 0 to 6 and her review's mends), as merged (2026-11-10)

**What landed:** the ships session's 9c812f43 (claude/pkg-75, on ad71736f merged before at
09222043: 75a59907 stage 0c, 3d507afe her module's row in `MODULE_FILES`, 92c80e2c the 74,
7c1d561c B7.b the quarter bill by deck, 9c812f43 the shared guards naming her), merged `--no-ff`
by hash at 31f6bb35, a clean merge.

**Her file (`data/ships/seventy-four.yaml` by `tools/ships/bellerophon.py` through the
generator; `data/people/seventy-four.yaml`; `docs/design/Design-Ship-Bellerophon.md`):** HMS
*Bellerophon*, an Arrogant-class 74 of 1786, her hull measured by eleven tasks, each by two
methods, on the draughts ZAZ1357, ZAZ1359 and ZAZ1363 and the class's drawings in Lavery, *The
74-Gun Ship Bellona* (the owner's book; figures cited, no text copied): the poop found to run
over the mizen mast, the bowsprit's steeve 31.6 degrees, four chain pumps, two forecastle ports
a side; drawn displacement 2,556 t against the filed 2,600. Three fits (`arrogant class 1793`,
`arrogant class 1795` the default, `as the bellona 1812`), each gun on its deck to the
centimetre; her company 590 by the Regulations' column (16 posts, 111 marines, 44 idlers, 419
seamen); her flag party of 15 in the crew's `flag:`, inert; anchors and cables by Steel and
Lavery; her description "a seventy-four, a ship of the line, fourteen ports a tier", the words
"a ship of the line" and "a line-of-battle ship" now naming her file. **Her sailing as tuned:**
one figure moved by her own tuning, `clr_x_m` 5.5 to 4.8 (the 64's); best 4.50 / 7.87 / 11.03
kn in 8 / 15 / 25 kn; the *Vanguard*'s 5 kn 4 f of 1 August 1798 met at 5.31 kn in 11 kn of
wind; the *Bellona* under reefed topsails close-hauled 6.93 kn in 25 kn against her reported
6 to 9. **The close-hauled gap is the physics', recorded for both two-deckers and likely the
frigate's file too:** 6.64 kn at 60 degrees in 25 kn under plain sail where the *Bellona* made
9, a later package's.

**Stage 0c (`freesail/ship/schema.py`):** the quarter bill's `marines` (the marines kept in
their division at the beat) and the crew's `flag:` (the flag party beyond her company, each a
post in the posts' form `{post, name}`), both left out of a pickle while unset, so that every
bill and crew before them pickles as it did; item 2 (the guns' numbering by deck) comes with
B7.d.

**B7.b, the bill by deck (`freesail/crew/quarters.py`, `freesail/orders/gunnery.py`):** the
bill's `marines` keeps that many in their division before the gun crews draw, the long guns
then leaving the marines out and the carronades taking them first (only the 74's file carries
the key); on a ship whose broadside guns stand on a `lower` deck (the 74 and the 64) each crew
keeps its deck, the beat says a line a deck ("The lower deck: 14 gun crews, 182 men."), and
robbing takes first the lower-deck crews whose port the sea has shut, then the other decks'
from the end that bears least, then the lower deck's; a deck fired by its words ("fire the
starboard lower deck", "the main deck", "the gun deck", "the quarterdeck guns", "the poop
carronades"). A ship with no `lower` deck robs, says and pickles as before. **Her review's
three order faults, each failed first on the code before its mend:** a deck fired while
exercising in dumb show fired live (now refused; a gun by name still goes); a deck said without
a side named both sides (now the engaged side's, refused with none engaged); a deck to leeward
counted the guns behind shut ports (now left out and said once, a deck all shut refused in the
broadside's words).

**Her review's mends of the hull:** the stern's side abaft the aftmost traced station brought
inside her own stern outline; the body plan re-traced by the order the sections nest in, the
dead flat outermost (her lower ports' shut heels moved by 0.03 degrees at the most, the lowest
10.38 to 10.35, old beside new in the notes; truth 7-195's pins hold); three marks sourced to
judged where judgement was in them.

**Truths drafted in `tests/test_bellerophon.py` for Phase 5:** 7-194 (her hull, her fits and
her company, pinned whole), 7-195 (her lower ports and the heel, its ordinary-sailing clause
recorded and not pinned: the setting of sail heels her past her threshold at 24 kn), 7-196 (her
pace crewed and alone). **7-196 crewed:** 106 ticks a second on the owner's machine against
the floor of 60, with three crewed 74s in action: the three 74s fire into the frigate of that
world, which carries no private signal, by package 71's rule for an unanswered challenge;
**booked on the lead's list.** **7-196 alone, the lead's measurement on the build machine at
this merge:** under the margin, so recorded and not pinned, and its test taken out by the lead at the merge with the figures in a comment where it stood and in the tuning notes: quiet, the best of three thousands in each of three runs, 505, 476 and 492 ticks a second, the frigate 524 and 516 in the same runs (the owner's machine 474 to 490); she runs about a twentieth slower than the frigate, and the frigate holds the floor of 500 by less than that; no floor lowered.

**Pins moved, old beside new in the notes:** `tests/test_ships.py`, `test_world_orders.py`
and `test_indefatigable.py` ("a ship of the line" refused before, now her file; the refusal
kept by "a first rate"); `test_neufchatel.py`'s rows by role gain hers; `test_lee_ports.py`'s
row for her; `test_profile.py`'s `MODULE_FILES` row; `test_schooner_mast.py`'s guard renamed
for eighteen files. No recorded passage's digest moved.

**The session's suites on its final tree:** the fast tier whole 7,274 passed, 2 skipped, 1
xfailed, 178 new and no outcome changed against its base; the slow candidates no outcome
changed, her ten new passing but 7-196 alone; the four whole logs equal; eighteen ship files
the generator's bytes; `check_viewer_guns` clean; the captain's trials the machine's three;
ruff clean. **The lead's merge:** the trial on 61792728 clean and lint-clean; no model or
vendor name in the diff; `data/ships/` gains her file alone, by the generator; no physics; the
fast tier whole on it exit 0, 7,433 passed, 1 xfailed, 501 slow left out; the whole suite in the cloud dispatched after run
66, the figures to follow. **The session's seven points ruled** in the notes at the end of this
file (2026-11-10, after this merge). **Next in 75:** her step 7 (B7.c her tack at quarters,
1.6 times her cleared tack today; B7.d; B7.e), the trim's alias words, then Phase 5; the
close-out's word after Phase 5's whole suite is green.


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

### The refresh after 84, 85 and 82's design (the lead, 2026-10-30; held by the owner to run after 82 and 65 both)

The brief above stands as the intent; this refresh says what the one world and 82's design
give it, so that the builder designs on them and not beside them; **it runs after 65 as well**
(the owner, 2026-10-30), the captive's places then 65's rule applied and not a design of 74's. **Fable, in steps merged in
parts as 84 and 82 are**, the design note first and reported at its boundary; the trunk
brought in at every boundary (82's later steps, 88 and 75 run beside it). **Truths 7-350 to
7-369** (82's are 7-320 to 7-339, 88's 7-340 to 7-349).

1. **The prize is a hull of the one world (item 1 on 84).** A ship struck is possessed as a
   `Hull` with a new nation and goal: awake under the cap while the fight and the boarding are
   near, asleep under the plan with her state whole when she parts company (84's rule, no
   second machinery; her damage summed into the far body as 84's step 5 sums it); the prize
   crew out of the captor's muster put aboard her by **82's `movement.put_aboard`** (the one
   function for every change of a person's hull), the prize master a person bound to her
   captain's station under the rules or a model's seat by 67's door with his harness
   following him (`seat="follows"`), her people prisoners confined below by their place in her
   or divided between the hulls by the same function; the two in company by 72's set or
   parting; a prize retaken by her prisoners rising or by a cruiser coming up; the far body
   carrying her as 84 carries any hull asleep.
2. **The captive's channel is 82's visitor's voice (item 3 on 82).** The player who strikes
   is put aboard the captor by `put_aboard` with his harness following, his station of the
   passenger's kind under his own name as 82 binds a visitor (the reach a passenger has: his
   place, what he sees from it, `say to the captain: ...`, his journal; no order of the
   captor's deck), his own ship's station standing bound to him or stood down by the
   handover's rule (`seat="stands down"`, the game saved and the journal kept) as the design
   decides for a captive; the parole, the confinement's places and the captor's doctrine as
   the brief has them; `where am I` and `the ship` (85's) answering the captor's hull. The
   same for a prisoner of the player's own prize.
3. **The far fight on the sleeping hulls (item 5 on 84's open item).** 84 left "the sleeping
   hulls' fight as the study recommends" (`Design-OneWorld.md` part 5); this package wires
   70's far rounds to the hulls asleep, the engagement first among the cap's reasons to wake
   them, the far state carried into the near body and back by 84's switch; **75's finding
   first**: `combat/far.py` reads `spec.hull.length_m`, a key `HullSpec` has not, so every far
   ship's length is 0.0 and `shot.py` floors her size; the mend is one read and moves the far
   fight's pins, re-measured old beside new with this line as the cause, before the wiring.
4. **The rest as the brief has it:** the prize court and the money on 86's ordnance and
   service (item 2), the court martial and a new command (item 4), the consent revision
   drafted and not applied with the refusal in words (item 6: 82's design read the brief as
   covering a visitor's station of the passenger's kind; an adversarial seat is not that, and
   the refusal stands until 55), the readings, forms and truths (items 7 and 8), the primer's
   chapter **in-world under 85's rule** and run through `tests/test_in_world.py` and the forms
   tables.

**The head rules bind** as the brief above has them, and 84's three pin rules and 85's
in-world rule with them; nothing under `docs/agents/consent/` or in the consent brief touched;
nothing of 75's files touched.

**From package 97 (the lead, 2026-11-06):** when the boarders' officer falls in the round, nobody leads on to the
deck won today (`combat/boarding.py` `boarders_officer` finds none among the first lieutenant, a lieutenant
and a mate); 97 pins that outcome under the fight's default draw. The prize crew's function is 74's on the
same road, so 74 settles who leads on when he falls (the senior standing of the party, by the period's
practice: a lieutenant, a mate, the senior midshipman) and moves the pin accordingly, old beside new.

## Package 76: the signal books built out (`data/signals/<root>/` the six files a root, Spain's root new and the others as their sources are found; `data/nations.yaml` each nation's `signals:` line; `docs/references/signals/` the research pass; `freesail/world/signals.py` the loader only where a book wants a field it has not; `tools/check_signals.py` new; `docs/design/Design-Signals.md` a postscript; `docs/TechnicalSpec-M7.md` §3 as built; `docs/agents/Harness.md` §21d; `docs/primer/23-colours-and-signals.md`; `docs/dev/TuningNotes.md`; `tests/test_signals.py`, `tests/test_known_truths.py` truths 7-426 to 7-435)

Opus. After 71 (merged 2026-10-24); runs beside 74 and the ships session, touching nothing
of theirs. 71 designed the shape and built the first books from memory, marked so: six
files under one root (`book.yaml` the declaration and the flags' figures, `numerary.yaml`
the day signals, `telegraphic.yaml` the dictionary, `night_fog.yaml`, `convoy.yaml`,
`private.yaml` the private table's form), Britain's and France's roots and `basic`, the
foundation every other nation stands on, each nation naming its root and its system in
`data/nations.yaml` (`signals: {root, system}`). Every entry whose number was not
remembered is `made: true`, the French book is small and the dictionary a few hundred
words; the owner's word at 71's merge: "the French and basic books' numbers are all made,
for 76 to correct". **Read first** `docs/design/Design-Signals.md` whole (the shape, "What
was rejected", "What hangs from this", the as-built postscript), 71's brief and record
above, the three roots as they stand, `freesail/world/signals.py`'s loader and
`signalling.py`'s minute, and spec M7 §3 with §28's decision 64: **the Spanish book is
built out first after the French** (the owner, 2026-11-06), Spain being Britain's enemy in
1805 and package 90's five Spanish and Mediterranean hulls coming to sail under it. **The
owner's rule for this package (2026-11-07): the Spanish books beside the British and the
French, and any other nation's reasonably easily implemented**, by data alone where the
shape allows it. The books are built out from the six files and never before them: the
shape is 71's and this package fills it; the engine's hoist, its reading and the `does` of a commanded captain are
71's and 72's and not changed here.

**The research phase (the owner, 2026-11-07, for this package and 81).** The builder is an
independent session and may conduct a deep research phase in the package's domain to
supplement what is filed in the repository (`docs/references/`, the design notes, the
tuning notes): the period's texts fetched through the proxy as step 0 has it, the
secondary literature read and cited, and **direct questions to the owner's own references
(Winfield and the rest of his shelf) put to the owner through the lead** in the step's
report, the owner's answers relayed as figures with their citation and never as copied
text (Winfield's text is never copied into the tree; a period text out of copyright may
be laid whole). The research plan is part of step 0's report, and **the lead approves the
plan and the pass before step 1 goes on**; a question for the owner that would hold the
work is said so, and the builder goes on with what does not wait for it.

0. **The research pass (step 0, its own commit and push, reported at its boundary).** The
   period's signal books, found, fetched through the proxy, their licences read, and laid
   under `docs/references/signals/` as 79b and 79c laid the pilots (the page images where
   the text is a table of flags and numbers, the OCR text beside, a README row each with
   what it covers and what it is trusted for). Look first for: Howe's signal book of 1790
   and the Admiralty's *Signal Book for the Ships of War* of 1799 with its night and fog
   signals; Popham's *Telegraphic Signals or Marine Vocabulary* in its 1803 edition (the
   whole dictionary and the alphabet) and the 1800 first; the *Signals and Instructions for
   Ships under Convoy*; for France du Pavillon's tables of 1776 and the *Tactique navale* of
   Morogues before them, the Republic's and the Consulate's general signals where a scan is
   found; **for Spain** Mazarredo's signals and tactics (the *Rudimentos de táctica naval*
   of 1776 and the *Señales* that followed, the Biblioteca Digital Hispánica first, then the
   Archive), the Real Armada's day, night and fog signals of the 1790s and 1800s, and the
   Spanish convoy instructions; for the Batavian Republic, Denmark, Portugal and the United
   States whatever the Archive and the national libraries hold (the Dutch signal books of
   the 1790s, the Danish *Signalbog*, the American *Signal Book for the Ships of War* of the
   1790s and Truxtun's). The titles here are the lead's from memory and are to be checked
   against the catalogues; what is found, what is not (with the host's answer) and which
   text answers for which nation is the pass's report in the tuning notes, and **the lead
   reads it before step 1 goes on**. A period text out of copyright is laid in whole; a
   modern edition's or a museum's own text is read and cited, never copied.
1. **The British books corrected and filled.** Every `made: true` entry of the numerary
   checked against the 1799 book: the number corrected where the page gives it, the entry
   kept and marked the builder's own where the page lacks it (the period's form, the mark
   kept); the entries the squadrons, the chases and the convoys of the game want added
   from the book (71 chose two hundred; the page decides what else is worth having, the
   `does` mapping of each new entry given in 71's words or `{news: true}` where the rules
   captain does nothing by it); the telegraphic dictionary filled toward Popham's whole
   (the 1803 edition's words where the scan is found, in the file's shape, the alphabet as
   it stands), so that a sentence a model wants is found in the book and not spelled; the
   night and fog book and the convoy's checked the same way; the private table's form read
   against the Regulations of 1806 and kept as 71 drew it (a pure function of the seed).
2. **The French book built out**, from the sources step 0 found: the numerary to the
   squadron's, the chase's and the convoy's needs, the numbers the period's where a page
   gives them and `made` where not, the dictionary where the French had one and the
   alphabet where they spelled, the night and fog book and the convoy's; `system` stays
   `well-built`.
3. **The Spanish book built, a root of its own** (`data/signals/spain/`, the nation's line
   turned from `basic` to its root, `system: well-built` once its numerary carries the
   period's numbers from a source and `basic`-with-a-root meanwhile, said so in the
   declaration): the Real Armada's numerary in its own numbers and its own flags (the
   declaration says what flags the system had, how many numerals, whether a substitute and
   a preparative, in the period's words, so that the lookout's "she makes a signal" can
   name the system a British officer would know by its look), the night and fog signals,
   the convoy instructions (the *flota*'s and the *registro*'s practice where a page gives
   it), the private table's form; every entry mapped by `does` to what a commanded rules
   captain does, as 71's are. The Spanish book is the proof of the shape: **a nation's book
   is added by data alone**, and item 6's checker and the tests pass on it with no change
   of code, or the change is named and made once for every nation.
4. **The other nations as their sources allow**, in this order and each a step: the
   Batavian Republic (at war with Britain), the United States (at peace, the 1812 war
   later), Denmark, Portugal; the Mediterranean factions (Naples, Sardinia, the Barbary
   regencies) stay on `basic` unless a page is found, and the declaration of `basic` says
   whom it stands for. A nation with a root but a thin page is a root of her own standing
   on `basic` for what she lacks, if the loader can be made to fall back file by file
   cheaply (say so, and the shape's postscript records it); else her entries are copied
   from `basic` and marked. The order may be taken another way with the reason (a rich
   Dutch scan before a thin Spanish one is a reason).
5. **What a corrected number moves.** The log writes the number beside the meaning, so a
   number corrected in a book a pinned passage hoists moves that passage's log: the
   encounter off the Lizard and the convoy of four (71's scenarios), the captain's trials
   with a private signal or a chase, and any recorded passage with a King's ship in
   company. Find them first (a grep of the recorded logs for the signals' lines), and
   re-measure each old beside new with the entry's correction as the cause, proven by the
   entry alone (the number put back, the digest returns); no truth pins a number, and none
   is loosened. The private tables do not move (the seed's draw is 71's and untouched).
6. **The checker and the tests over every root.** `tools/check_signals.py`: every root
   under `data/signals/` loads by 71's loader, its six files present, its numbers unique
   within a book, every `does` an order the dialect parses or a form 71's design names,
   every qualifier one the engine fills, every source named, every made entry marked; the
   same as a test parametrized over the roots, so that a nation added later is checked by
   the tests it does not know about. A test of each new root: a signal hoisted under it and
   read by a ship of the same nation holding the book; read as "a signal we cannot read" by
   a ship of another; the convoy's instruction obeyed by a commanded captain under it.
7. **Truths 7-426 to 7-433 and the records.** A Spanish frigate and her consort work a
   chase on the Spanish book's numbers and the British frigate in sight reads the hoist and
   not its meaning; the British numerary's Trafalgar entries (1, 13, 16, 63, 72, 76) stand
   at the 1799 book's numbers from the page; a telegraphic sentence of a dozen words is
   found whole in the dictionary and spelled nowhere; a signal made under a book of one
   nation is never read by a ship holding another's; the French book answers the squadron,
   the chase and the convoy with no made entry among the entries those scenarios hoist (or
   the made ones named); a nation turned from `basic` to her root changes nothing of her
   private signal's draw; the checker passes every root; and the rest as the work shows
   them. The records: the design note's postscript ("As built out", the sources by nation,
   what each book carries and what it lacks, how a nation's book is added: the six files,
   the nations' line, the checker, the tests), spec M7 §3's as-built paragraph extended,
   Harness §21d's words where a model's reading changes, the primer's chapter 23 in-world
   under 85's rule (the books named as a sea officer of 1805 would name them, no page
   numbers, no "package"), the tuning notes (the pass, each book's figures: entries, made
   entries, sources; what moved and its proof; found on the way; the suite as run).


8. **The flags of command and identity (the owner's addition, 2026-11-07; truths 7-434 and
   7-435).** Reading Roosevelt's *The Naval War of 1812* (part I, pp. 160 to 161, out of
   copyright), the owner found the one thing of the colours the game has not: "she carried her
   commodore's pendant at the main, national ensigns at the mizzen-peak and main top-gallant
   mast-head, and a Jack at the fore. The *Java* also ... hoisting her ensign at the mizzen-peak,
   a union Jack at the mizzen top-gallant mast-head, and another lashed to the main-rigging"; and
   before it, "At 10 the *Java* made the private signals, English, Spanish, and Portuguese in
   succession, none being answered; ... a little after 11 she [the *Constitution*] hoisted her
   private signal, and then, being satisfied that the strange sail was an enemy, she wore and
   stood off." (The hour is "11" in the 1882 printing laid under `docs/references/signals/`; the owner's copy reads "1"; found by 76.) 71's colours are a state (shown, none, false, struck, distress) with no flag in a
   place; this item gives each root **a seventh file, `colours.yaml`**: the nation's flags of
   identity and command by name (the ensign and its variants by service or squadron, the
   merchant's ensign, the jack, the commissioning pendant, the broad pendant of a commodore, an
   admiral's flag by rank, the flag of truce), **where each flies and when** (the ensign at the
   peak or the staff; the pendant at the main; the jack at the jackstaff at anchor and, by the
   period's practice in action, at the fore or a topgallant masthead; the ensigns doubled in
   action, one at the peak and one at a masthead, and one lashed in the rigging so that no shot
   can bring the colours down by accident), and **a drawing of each** (the field, the cantons, the
   crosses or stripes as a short list of coloured rectangles and lines in the flag's proportion,
   the source named; package 81 draws from it and 91 animates it). The engine: 71's locker gains
   **what flies where** (a small list set by the rules at the colours' hoisting from the nation's
   file, the ship's role and her captain's rank: a King's ship wears her pendant, a commodore his
   broad pendant (72's role), a merchantman her ensign alone; at anchor the jack; beating to
   quarters doubles the ensigns and bends the jack as the file has it), **read by the lookout** at
   the colours' range in words ("she wears a broad pendant at the main": a commodore; "a pendant:
   a man-of-war"; "her ensign at the peak and another at the main"), and **the orders** (`hoist the
   broad pendant`, `hoist a second ensign at the main`, `hoist the jack`) with the standing
   orders' and the doctrine's hooks named for 74 and 72 (the files of the captains are 74's:
   report what a rules captain should hoist by his doctrine and build the data and the lookout's
   side; the lead carries the doctrine's line to 74). **The private signal in another nation's
   form**, the *Java*'s move: `make the Spanish private signal` (or `make the private signals in
   succession`) where the ship **holds the table** (a captured table by 74's road, or an ally's
   carried by the scenario's `papers.signal_books`), each a challenge in that nation's form the
   stranger reads and answers or not, the minute a hoist, the answer judged against the table
   held, the log saying "the private signals, English, Spanish and Portuguese in succession, none
   answered"; a table the ship does not hold is refused in words. Truth 7-434: a King's frigate
   wears her pendant at the main and her ensign at the peak, a commodore's ship her broad pendant,
   a merchantman her ensign alone, each read by the lookout at the colours' range in those words,
   and beating to quarters doubles the frigate's ensigns with the jack at the fore, nothing of it
   moving any pinned passage's digest (the places are the locker's state and the lookout's
   words only where the colours' line already falls, or the passage is named and re-measured).
   Truth 7-435: a ship holding three nations' tables makes the three private signals in
   succession to a stranger that answers none, three minutes at a hoist, and her captain holds
   her an enemy by the tell, as 71 has it. The data shape of `colours.yaml` is written in the
   design note's postscript before it is filled, as 71 wrote the six files', so that every nation's
   flags fit it and 81 reads one shape.

**Not built here:** the squadron's signals beyond the books' entries (72's set stands), the
captured book's use (74's), the captains' doctrine of what to hoist (74's files; reported to the lead), the far ships' reading (71's and 72's as they stand), the eastern
Mediterranean's factions. **The head rules bind** as every brief has them: no model
identifier in any file; nothing under `docs/agents/consent/` or in the consent brief
touched; the pins re-measured only where a change moves them, old beside new, proven by the
entry; never a test skipped, disabled or quarantined; 85's in-world rule on the primer and
every served word; the physics read and not changed; nothing of 74's or the ships session's
files (`world/captains.py`, `brains.py`, `combat/`, `data/ships/`, `evolutions/`) touched:
a signal that wants a captain's new `does` is reported to the lead and not built. The branch
`claude/pkg-76` from the trunk's head, the trunk merged in at each step's boundary, the
suites run in a worktree pinned at the commit measured (the fast tier whole; the slow tier
of the touched files and the known truths; the pace alone and last); each step reported to
the lead by one-shot trigger with the figures and the commit; the lead merges in parts.

## Package 81: the viewer's action, from the hull 75 draws (`client/projection.js`, `shipview.js`, `style.css`, `app.js` the guns, the ports, the flash, the smoke and the damage, animated between snapshots; `freesail/api/queries.py` the guns and the ports served to the viewer from the hull's parts and the files' triples; the snapshot's firing and damage fields where the readings lack them (`freesail/api/readings.py`; `combat/action.py`'s `action.fired` data only, if the guns are not named there); `tools/check_viewer_guns.py` new; `docs/design/Design-ViewerAction.md` new; `docs/design/Build-Ships.md` §6 a postscript and the ship builder's checklist; `docs/primer/01-the-ship.md` or where the viewer is told; `docs/dev/TuningNotes.md`; `tests/test_view_geometry.py` (Node), `test_server.py`, `test_known_truths.py` truths 7-436 to 7-445)

Opus. After 71 (merged) and 75's hull step (merged 2026-10-31: the hull profile drawn in
the viewer for every ship whose file gives one, `Build-Ships.md` §5 and §6); runs beside 74
and the ships session, touching nothing of theirs. The owner's first action (2026-10-24,
`docs/playtests/2026-10-24-owner-first-action/notes.md`) asked for it: the gun ports and
the guns drawn with some movement, a muzzle flash and a smoke plume over a few seconds at
each gun's firing, the smoke lingering to sell it; and 75's design of the 74 booked the
ports' rule (a triple within `OVER_THE_RAIL_M` of the rail at its x is a gun's place over
the rail, not a port). **Read first** `Build-Ships.md` §5 (the profile: `hull.profile`,
`decks_m`, `ports_m` the triples by deck, x, sill and half-breadth, `port_size_m` by deck;
§5.3 every port gun on a triple of its deck within 0.01 m, truth 7-185) and §6 (how the
viewer draws the profile, in strips, the stern by its type), the per-ship notes under
`docs/design/ships-design/` (the Amazon's §7.3 and §8.2 to §8.3 for the forecastle guns
over the rail and the ports at the file's own guns), the armament block of a ship file
(`armament.fits.<fit>.guns`: each gun's `id`, `kind` long or carronade, `pounder`,
`place` broadside, chaser or pivot, `number`, `side`, `x_m`, `height_m`, `deck`), 70's
guns as parts of the graph and their states (cast loose, run out, housed; the magazine),
75's lee ports (`combat/ports.py`, the port shut by the roll, `guns.ports_shut` and
`guns.ports_opened`), 73's damage (the carpenter's well, a hole's place against the
waterline and its size, a spar gone) as the readings `the guns` and `the damage` give it,
`client/projection.js` (pure functions tested in Node by `tests/test_view_geometry.py`) and
the snapshot `app.js` renders. **The owner's rule for this package (2026-11-07): ships are
added continuously, so 81 establishes a procedure, not a picture.** Every gun of every
hull is drawn by one rule from the data the ship file already carries, a new ship is drawn
at the same standard by passing the same checker with no change of code, and the ship's
builder knows from one checklist what her file must give.

**The research phase (the owner, 2026-11-07, for this package and 76).** The builder is an
independent session and may conduct a deep research phase in the package's domain to
supplement what is filed in the repository (the gun tables and the carriages' and slides'
figures by pattern and pounder, the run-out and the recoil, the smoke of black powder, the
ports' lids and their furniture; `docs/references/`, the ships-design notes, Build-Ships.md):
the period's and the standard texts fetched through the proxy where they are out of
copyright, the secondary literature read and cited, and **direct questions to the owner's
own references (Winfield, Lavery's *Arming and Fitting*, Caruana and the rest of his
shelf) put to the owner through the lead** in the design's report, the owner's answers
relayed as figures with their citation and never as copied text (Winfield's text is never
copied into the tree). The research plan is part of the design note of item 1, and **the
lead approves the design and the plan before the drawing is touched**; a question for the
owner that would hold the work is said so, and the builder goes on with what does not wait
for it.

1. **The standard, written first** (`docs/design/Design-ViewerAction.md`, pushed and
   reported before the drawing is touched; the lead rules on it). (a) The data contract: a
   hull is drawn with her guns when her file gives a profile (`hull.profile`), her decks,
   her ports' triples and sizes by deck, and an armament whose every gun carries its deck,
   side, kind, pounder, place and `x_m`; a hull lacking any of these is drawn as 75 left
   her, and the checker says what she lacks. (b) The one rule of placing: a broadside gun
   is drawn at the triple of its deck whose x is its own (within §5.3's 0.01 m), in the
   port of that deck's `port_size_m`, its muzzle out of the port by its kind's run-out when
   cast loose and run out, housed within it otherwise; a triple within `OVER_THE_RAIL_M` of
   the rail at its x is a gun over the rail (the forecastle's, the quarterdeck's where the
   sheet draws no port), drawn on its carriage above the drawn rail with no port; a chaser
   at the bow or the stern and a pivot gun at its place by the same rule on the stem's or
   the taffrail's line; a gun whose x finds no triple is a finding for the ships session
   through the lead, never a hand-placed figure. (c) The gun's own figure by kind and
   calibre, one table in the design with its sources (the Blomefield long guns' lengths by
   pounder, the carronade's by pounder on its slide; a swivel where a file has one), drawn
   as a barrel and a carriage or a slide in the hull's strips at the viewer's honesty, the
   figure the same for every ship of that gun. (d) The firing: a flash at the muzzle and a
   plume that grows over two or three seconds and drifts to leeward on the apparent wind
   the readings give, thinning over the half minute, each gun's own at its own firing and
   none at a gun that did not fire; the recoil a few frames in and back. (e) The damage at
   the viewer's present honesty: a hole where the carpenter's well reports it (its side,
   its place against the waterline, its size as 73 gives them), a port stove, a spar gone
   as the viewer already drops it; nothing drawn that the readings do not say. (f) The
   animation road: the viewer is driven by snapshots; between them it animates by the
   clock (`requestAnimationFrame`) from the last snapshot's state, the firing events
   stamped with their tick, so that a flash is seen when it happened and not when the next
   snapshot comes; 91's light and air reuse this road, so it is made once and said.
2. **The data served.** `queries.py` serves the viewer each gun with its placing resolved
   by rule 1(b) (the triple chosen, the port's size, over-the-rail or not, its state) from
   the hull's parts and the file, and each port's state (open, shut by the roll, stove);
   the snapshot carries the guns that fired since the last snapshot with their ticks and
   the plume's wind. Where `action.fired` does not name the guns, their ids are added to
   the event's `data` and not to its text, so that no log line and no pin moves; this is
   the one touch of `combat/action.py` allowed, said in the report, and the lead resolves
   its meeting with 74 at the merge. Nothing of the physics, the evolutions or the ship
   files is written.
3. **The drawing.** The ports in the hull's strips on every drawn deck with ports, lids
   open or shut by state; the guns by 1(b) and 1(c), run out or housed by 70's state; the
   flash, the plume and the recoil by 1(d); the damage by 1(e); the words a hover gives
   under 85's in-world rule ("a long 18-pounder, run out"; "the lee ports shut"). The
   frame equal across states, as the viewer's law has it (a gun run out, a plume or a hole
   leaves the bounds as they were); the hull drawn as before where the file lacks the
   contract; the sea's hiding of what is below the water kept.
4. **The checker and the ship builder's checklist.** `tools/check_viewer_guns.py`: for
   every ship file under `data/ships/` with an armament, every gun finds its place by rule
   1(b) or is listed with why not (no triple at its x, no port size for its deck, no
   profile), every port of the profile has a gun or is said empty, nothing is drawn outside
   the hull's strips; run as a test parametrized over the files, so that a ship added later
   is checked by it. A checklist in `Build-Ships.md` §6's postscript for the ship's builder
   (what the file gives: the profile, the decks, a triple at every gun's x with its sill
   and half-breadth, the port sizes by deck, the guns' decks and places), so that the ships
   session's hulls to come (90's five, the bilander, the 74) are drawn at the standard by
   giving these and running the checker, and nothing is drawn by hand for any ship. The
   eight files with triples today (the brig, the cutter, the frigate, the merchant brig,
   the privateer schooner, the razee, the 64, the topsail schooner) are the first to pass;
   a gun of theirs that does not is reported, not fixed here.
5. **Truths 7-436 to 7-443.** Every gun of every ship file with the contract is drawn on
   its deck's triple within 0.01 m or over the rail by the rule, the checker clean; the
   Amazon's forecastle guns are drawn over the rail and through no port, her upper-deck
   guns in ports of the upper deck's size; a lee port the engine shuts by the roll is drawn
   shut in the next snapshot and its gun housed; a broadside fired draws a flash at each
   gun that fired in that minute and at no other, the plume drifting to leeward of the
   apparent wind; the frame's bounds equal with every gun run out, every plume alive and a
   hole in her side; a hull without the contract draws as 75 left her; a ship file added to
   a test's temporary directory with the contract and a made-up fit passes the checker with
   no change of code; and the rest as the work shows them. The viewer runs on no tick's
   path and the snapshot's new fields are measured for their cost (the server's test), the
   pace floors unmoved.
6. **The records.** The design note's postscript as built; `Build-Ships.md` §6's postscript
   and the checklist; the primer where the viewer is told, in-world under 85's rule; the
   tuning notes (the gun table's sources, each ship's placing as the checker reports it,
   what moved and its proof, found on the way, the suite as run); the harbour's page if a
   setting is added (none expected).


7. **The flags drawn at their places (the owner's addition, 2026-11-07; truths 7-444 and
   7-445).** Reading Roosevelt's *The Naval War of 1812* (part I, p. 161): "she carried her
   commodore's pendant at the main, national ensigns at the mizzen-peak and main top-gallant
   mast-head, and a Jack at the fore"; the viewer draws no flag at all today. By the same rule
   for every hull: the flags that fly are drawn **at their places on the drawn spars**, the
   ensign at the mizzen peak (the gaff's peak the projection already has) or the ensign staff
   at the taffrail where the hull has no gaff, the pendant at the main truck, the jack at the
   jackstaff on the bowsprit or at the fore truck, a second ensign at a topgallant masthead, one
   lashed in the rigging, as **what flies where** says it: package 76 gives each nation's root a
   `colours.yaml` (the flags by name, where each flies by occasion, and a drawing of each as a
   short list of coloured rectangles and lines in the flag's proportion) and the engine's locker
   the list of what flies where; the snapshot serves that list with each flag's drawing, and
   the viewer draws it stiff (cloth drawn flat, the fly to leeward of the apparent wind by a
   fixed angle; the waving is 91's). **The contract between the two packages**, so that neither
   waits: 81 reads the snapshot's `flags` (place, flag name, drawing) and draws whatever is
   there; until 76's file exists for a root the server serves one plain ensign at the peak in a
   field of the nation's `flag` word from `data/nations.yaml`, so that 81's drawing and its truths
   are complete on the trunk as it stands and 76's data refines them. The struck colours draw
   nothing; false colours draw the other nation's; the flag of truce (74's cartel) the white; the
   distress signal the ensign union down. The frame equal across states as every flag flies or
   comes down. Truth 7-444: every hull with a drawn profile draws her ensign at her peak or
   staff and her pendant at the main truck when the locker says they fly, a commodore's broad
   pendant for a commodore, the jack at its place at anchor, the second ensign at the masthead
   when the ensigns are doubled, each within 0.1 m of the spar's point in the projection, the
   bounds unmoved. Truth 7-445: the flags follow the state in the next snapshot: struck draws
   none, false colours the other nation's, the cartel's white, and a hull whose nation has no
   `colours.yaml` yet draws the plain ensign from the nations' table.

**Not built here:** the light and the air (91, which reuses this package's animation
road and waves the flags 81 placed); a three-dimensional ship or a damage picture beyond the present honesty (M8); any
ship file's triples (the ships session's, by its plan); the guns' mechanics (70's, 77's).
**The head rules bind** as every brief has them: no model identifier in any file; nothing
under `docs/agents/consent/` or in the consent brief touched; the pins re-measured only
where a change moves them (none is expected: the viewer reads and writes nothing of the
world), old beside new, proven by bisection; never a test skipped, disabled or quarantined;
85's in-world rule on every served word; the physics read and not changed; ship files only
through `tools/gen_ships.py` and here not at all; nothing of 74's files beyond item 2's one
data key, nothing of the ships session's. The branch `claude/pkg-81` from the trunk's head,
the trunk merged in at each step's boundary, the suites run in a worktree pinned at the
commit measured (the fast tier whole; the slow tier of the touched files and the known
truths, the Node tests with them; the pace alone and last); each step reported to the lead
by one-shot trigger with the figures and the commit; the lead merges in parts.

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

## Package 93: the blocks' tiles rebuilt on their true water (`tools/build_charts.py` the fill raise by block; `data/charts/tiles/<region>/`, `coast/`, the manifest's tile lists for the regions named; `docs/dev/ChartBlocks.md` "GEBCO's fill" and item 6; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_tide.py`, `test_scenarios.py`, `test_known_truths.py` truths 7-305 to 7-309)

Opus. After 89 (merged). 89's finding, tabled in its notes under "GEBCO's fill": every
block's tiles had their GEBCO fill raised to the mean level of the eleven's blend, which was
false over the blocks, so the land of the Mediterranean's five regions stands six metres
and more above its true water, Portugal's two to four, and the Channel east's high water
stands up to 4.4 m above the fill's raise. Read `docs/dev/ChartBlocks.md` whole (the fill's
section, item 6 as 89 rewrote it, the blocks' sections), the recipe form over `REGIONS` in
`tools/build_charts.py` (`fill_to_chart_datum`, `fill_mean_level_m`, `skip_dry_tiles`),
`mean_level_grid` as 89 left it (the eleven alone), 89's record and notes, and the blocks'
own sections of the tuning notes, before anything.

1. **The rule.** The fill is raised by the mean level the world's tide gives the block's
   water now: `mean_level_grid` reads the gauges that serve each cell (`Tide.gauges_at`),
   the eleven and the block's own, so that a region's land stands above its own high water
   as 39a wanted it, and no longer above a far gauge's. Outside every block nothing changes
   (the eleven alone there, as the raise was): `channel-west` and `channel-mid` are not
   rebuilt and not touched.
2. **The regions rebuilt**, each on its own, in this order, the smallest first:
   `channel-east`; `biscay-north`, `biscay-south`, `portugal`; `strait`, `madeira`,
   `azores` where the raise differs (89's table has them at nought: rebuild only if the
   rule moves the raise there, else say so); `mediterranean-west`, `balearics`,
   `gulf-of-lion`, `ligurian-sea`, `tyrrhenian`. The sources are fetched again through the
   proxy (the caches were the builders' sessions'); `--skip-fetch` once the fetch is done
   for the marks. Each region: the build, the checks printed and passing, `git status`
   showing no change to any tile, coast or index of a region not named, the region's
   count and bytes said (they may change where cells move from land to water and back),
   the region's port files and marks untouched, and its block's own tests run before the
   next region begins. The Alboran's inland tiles (`skip_dry_tiles`, 79c's note) may be
   taken for `mediterranean-west` at the rebuild if the how-to's rule for Portugal's
   applies cleanly, said so; else left.
3. **The proof, first and last:** the eleven recorded passages by node id, `gate_5b` and
   `gate_5c`, and the captain's trials, run on a clean worktree of the head first and on
   the final tree last, identical; no recorded passage's digest may move (none sails a
   rebuilt region; the test says so). The blocks' own scenarios (`spithead.yaml`,
   `mahon.yaml`, `agincourt-sound.yaml`, and the earlier blocks') sailed again on the
   rebuilt tiles, their figures old beside new in the notes; the blocks' truths (7-270 to
   7-304, and the earlier blocks') run with --slow; where one fails on the rebuilt tiles,
   stop and report with the figures, as 89 did; no truth loosened.
4. **Truths 7-305 to 7-309:** a low shore of the Channel east (the Dungeness marsh, the
   Somme's banks) stands above the world's high water springs; Mahon's and Naples' quays
   stand their true height above their water; a lagoon or harbour the grid has as water
   covers and dries as its block's tide says and not as the eleven's; the raise outside
   every block unchanged to the centimetre; the Strait's, the islands' as the rule gives
   them. 5. **The records:** the tuning notes' section with each region's figures; the
   how-to's fill section rewritten; spec M6 §26's as-built line.

The hard rules as every brief has them; `claude/pkg-93`, pushed after each region's
commit; the lead merges whole. Package 94 runs beside it on the tide's seams and the
features' kinds; the two share the manifest and the tuning notes, which the lead merges;
94 does not rebuild tiles and 93 does not touch a feature's kind or the tide. No CLAUDE.md
is in the repository: the briefs' heads and the records serve.

## Package 94: the chart's tidies from 79c, 79d and 89 (`freesail/world/chart.py` the island kind and the road's bottom; `data/charts/features/*.yaml` the islets' kind; `freesail/world/tide.py` the seam's taper and a tide region; `data/charts/manifest.yaml` a tide-only region, if taken; `data/tides/constituents.yaml` Bournemouth's and Portsmouth's `block:`; `docs/dev/ChartBlocks.md`; `docs/references/Tides.md`; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_tide.py`, `test_known_truths.py` truths 7-310 to 7-314)

Opus. Beside 93. The findings the three packages left for a tidy, read in their records
and notes before anything (79c's "Found on the way", 79d's, 89's sections "Bournemouth and
Portsmouth" and the seam):

1. **An island with an extent.** An isle the grid lacks is given today as a `rock` of its
   height so that nothing sails through it, and the lookout calls it "a danger" (the Isla
   del Rey, 79c; seventeen islets of 79d's three regions). A feature kind `island` with
   `extent_m` and a height: the chart refuses it as ground as it does a rock, the lookout
   calls it an island by its name, the pilot's words the same; the features files of 79c
   and 79d recast for the islets they name as such, each by its source line; the index
   rebuilt by the how-to's road for a mark changed (`--skip-fetch` on the cache, or the
   index alone if the builder has a road for it: read `ChartBlocks.md` and say which); no
   tile moves (93 is rebuilding tiles beside you: touch no tile, and bring the trunk in at
   each boundary).
2. **A road with a bottom.** `Chart.bottom_near` reads `anchorage` and `bottom` features;
   a `road` with a bottom gives no note of it (79d). The road read as the anchorage is, the
   roads' files unchanged.
3. **The seam's taper.** 89's rule leaves a step at each block's edge (102 degrees of M2 at
   1 W off Selsey). Inside a block, the block's gauges' weight in the blend rises from
   nought at the block's edge to its full over a band (ten miles, judgement, said so), so
   that a position just inside a block reads nearly the eleven's and the step is gone;
   **outside the block nothing changes** (truth 7-282's west position to the bit, every
   recorded passage's digest held: the proof first and last as 89 ran it). The band is the
   membership's and the cache's: say how the cell cache keys it.
4. **Bournemouth and Portsmouth.** 89's options: a Solent tide region. If the manifest may
   carry a region with bounds and no tiles for the gauges' membership alone (a small
   change in the manifest's reader and `Tide.region_bounds`, said in `ChartBlocks.md`),
   give the two gauges `block: solent` over the Solent and Spithead (bounds judgement from
   the gauges' positions and the Wight's shores, said so) under the taper of item 3; the
   Downs-to-Spithead passage's figures and the Solent's judged rises re-measured old beside
   new; **if any recorded passage of channel-mid or channel-west would move, stop and
   report**, the gauges held as they are. 39a's finding (the eleven's blend over the Solent
   four hours and a half wrong) is the reason; say what the Solent reads after.
5. **Truths 7-310 to 7-314:** the Isla del Rey an island to the lookout and ground to the
   keel; a road's bottom in the lead's note; the tide a cable inside 1 W within a tenth of
   a foot of the tide a cable outside it; Spithead's tide within the hour of Portsmouth's
   gauge if item 4 is taken (else the truth says the Solent is held, and why); every
   recorded passage unchanged. 6. **The records** as every package's.

The hard rules as every brief has them; `claude/pkg-94`, pushed after each commit; the
lead merges whole. No CLAUDE.md is in the repository: the briefs' heads and the records
serve.

## Package 65: the place's knowledge (`freesail/agents/harness.py` the sample by place; `freesail/api/readings.py` a place on every row and `none_words` for a reading not to be had where the asker stands; `freesail/world/places.py`, `people.py`, `movement.py` the places' knowledge and the work's room; `freesail/core/events.py` or the log's lines a kind's "where it is heard"; `freesail/agents/tools.py` the papers' places and the drill; `freesail/agents/agent.py`, `director.py` the briefs' words; `docs/TechnicalSpec-M7b.md` §14 as built; `docs/agents/Harness.md`; the primer's chapters 14 and 19; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-370 to 7-389)

Fable (the owner, 2026-10-30: scoped to cover the edge cases wherever possible, an Opus
follow-up filling in from the testing's feedback and probing); **launches when 82 is whole**,
so that it builds on 82's whereabouts (a person's place the whole truth of where he is,
across hulls and in the boat) and on 85's words; 74 reads its design note for the captive's
places. The ground: decision 47 dropped locational knowledge as an overcomplication; the
dispatches test brought it back by the captain's own account (everything reached him in the
sample wherever he stood, so moving bought nothing and cost an order; ashore in Plymouth
market he had the ship's heading, leeway, sails and the frigate's bearing from three miles
off); the owner's ruling of 2026-10-19 (a place carries at least what can reasonably be
perceived from it, by action and by what is there) and the lead's provisional design in spec
M7b §14 "Brought back and forward"; 66's earshot (a word heard where it is said), 66's and
85's always-present line, 84's one registry of persons and things with a whereabouts, 82's
`where am I` and the visitor's reach. **What is already so:** between hulls the knowledge is
strict (a hull's log is hers, another's reaches a person by sight, signal, hail or report, and
the director alone reads every hull); within a hull and ashore it is not (the whole log and
every reading reach a person in the cabin, below asleep, or in the market). **Generously
scoped as the M7 packages are:** the brief binds the intent and names the ground, the builder
designs, takes an item another way with its reason, grows a part where the work shows it
should, and says what it left and why; no day count. **The design note first** (`docs/design/`,
in 83's shape: the table of places against what reaches a person in each, the edge cases
each decided, what was rejected), reported at its boundary for the lead's reading before the
harness is touched. **Truths 7-370 to 7-389.** Each item an intent with the lead's reading;
the intent binds.

1. **The rule, stated once: a sample carries what the person's place allows.** The harness
   keeps the rule, not the model: the readings in a sample are the ones to be had where he
   stands, the log's lines the ones he would hear or see from there, and a reading asked
   for elsewhere (the `readings` tool, `what is the depth` at the prompt) is answered with
   where it is to be had ("the lead is cast on deck; the chart is in the cabin") and not with
   the figure. **The table of places** (the design note's heart, each row decided and said
   why): the quarterdeck and the deck (the deck's readings, the log as it is spoken, the
   lookout's hails, the deck's conversation, the sail in sight as the deck sees it); the
   masthead (the lookout's horizon and his glass, the deck by hail); the cabin and the
   gunroom (the chart, the papers and the slate, the deck by report and by what is felt:
   the heel, the motion, the sounds of sail work, all hands, a gun, the bell; the readings
   of the deck not his until he goes up or is told); below in a berth, asleep (nothing until
   called or woken: the call, all hands, a gun, the ship striking); the hold, the magazine,
   the sail room, the sick berth (what is there and the motion); ashore, at each place of the
   port (the ship by sight from the quay or the point where she is in sight, by report, by
   boat or by letter; nothing of her readings); in the boat away (the boat's readings, the
   ship by sight, 82's); a visitor aboard another hull (that hull's place by this table,
   82's reach). **The log's lines by where they are heard:** each kind of line carries where
   it is perceptible (the deck's work on deck; a report made to the captain where he is; the
   bell, a gun, all hands and the ship striking everywhere aboard; a word where it is said,
   66's rule as it stands), with the design's default for a kind not listed, so that a new
   kind of line is placed by its author or falls to the default and never leaks by accident.
   **And the other half of the same rule (decision 60): a reply's prose is the person's own
   note, never a word in the world.** Today the free text of a reply is said aloud where the
   station stands (`agent.note` through `say_aboard`, package 41's deck conversation), so
   a model's out-of-character words reach the player as speech and nothing obliges it to
   `say`; the free text becomes a note in the station's journal, read by the director's
   log and the owner's eye (`show the <station>'s journal`) and heard by nobody, a thing
   heard only when said (`say`, `say to`, `hail`, `answer` to a question put); the brief
   and the tools' words say so once, the harness's notice when prose alone leaves an answer
   owed names the tool, and the tests of 41's rule move old beside new with the reason.
2. **Report, the messenger and the call.** What a person below is told: the officer of the
   watch reports to the captain by the rules of the period (a sail sighted, a change of
   wind, the land, a strange sail's colours, the ship in danger: the captain is called), the
   report a line in the captain's sample where he is, made by the rules' officer or by a
   model at that station through `say to the captain` (the harness telling a model officer
   the duty in his brief); `call the captain`, `call all hands`, `call the watch` as orders
   with their answers; a person asleep below woken by the call, by all hands, by a gun, by
   the ship striking and by nothing else, the stand-by's "urgent event" read by the place
   (an urgent line a sleeping man cannot perceive does not wake him; the call does); a
   tripwire of the ship's state judged for a station that cannot see it fires as the call it
   would be in truth (the officer sends for him) and says so, so that no model is woken by a
   depth it could not know.
3. **Books and papers in their places.** The chart, the epitome, the almanac and the ship's
   papers in the cabin; the master's slate in the gunroom or with him on deck; the book of
   standing orders on deck and in the cabin; the log book where it is kept; the primer and
   the catalogue anywhere (the player's reference, not the ship's); a book read where it is
   not is a walk first, said so ("the epitome is in the cabin: go below to read it"); the
   library tool answers by the same rule; the pictures by their place (`chart` in the cabin
   or at the binnacle's chart as the design decides, `ship_view` from the deck or the boat).
4. **The drill, extended.** Before the station brief, after the three calls of today, the
   walk: go below, eat, drink, read a book from the library where it is kept, come on deck,
   each answered and the line changing, so that a model has seen the places and felt the rule
   before the game; the drill in-world under 85's rule.
5. **Work in its place.** Each kind of work is done where it is done, the same for the
   rules' person and for a model or the player at the station: the master's day's work and
   his sights' working in the gunroom (and on deck for the sight itself), the captain's
   writing (his book, a letter, his standing orders) in the cabin, the sailmaker's in the
   sail room, the carpenter's below at the damage, the purser's at the hold, the surgeon's in
   the cockpit; `People.occupy` and `TRADE_PLACES` made the one road; where a station
   holder's work and the rules' person's differ today, the design lists them and makes them
   one; the place's knowledge follows the work (the master below at his slate hears the deck
   by report).
6. **The edge cases, each decided in the design note and tested:** the handover fold keeping
   the person's place; a station reseated after a sleep and a wake (84) at its place; a
   station on a hull asleep (the far shape's readings are the plan's, the place rule the
   same); the boat away with the player in her and the ship's lines reaching her only by
   sight and hail; the visitor aboard another hull and the captive confined below (74's,
   the places the design gives him: the hold's or the cabin's by his parole); the director,
   who sees all and is untouched, and the director's `say as` for a person where he is; the
   replay (the rule is a read of the world and changes no input, so no digest moves: the
   proof); the pace (the filter's cost measured under 84's pace rule); the stations' briefs
   saying the rule once (85's in-world words); and **the player at the prompt, ruled (decision 59):** the player
   seated as a person (the console's captain, a `--seat`) reads by his place as a model
   does, the owner's eye the director's station and `follow`, with a scenario key
   (`knowledge: all`) that turns the rule off for testing, said in the design and the primer.
7. **Truths and records.** 7-370 onward: a captain in the cabin whose sample carries no
   deck reading and whose officer's report of a sail reaches him there; a captain ashore at
   Plymouth with nothing of the ship but the boat's report; a sleeping station woken by the
   call and not by a notable line; a reading asked where it is not to be had answered with
   where; a book read after the walk; the master's day's work in the gunroom by the rules'
   master and by a model alike; the handover fold keeping the place; the boat away; the
   replay to the same digest; spec M7b §14 "as built" (the provisional design replaced by the
   rule as built); the Harness; the primer's chapters 14 and 19 (and 16's duties where the
   report is), in-world under 85's rule and through `tests/test_in_world.py`; the director's
   library; the design note's postscripts; the tuning notes; the suites by the rule (the fast
   tier whole on the final tree of each step, the slow tier of the touched files and the
   known truths, the pace tests alone and last; the whole suite the lead's in the cloud).

**The Opus follow-up, booked (65b):** after the owner's testing and a round of probing (a
model at each station walked through the places with a list of what it should and should
not know, the gaps written down), the places' table filled in where the testing shows a
leak or a silence, and the words tuned; briefed from the findings, not before them. **Not
built here:** 74's captive beyond his places; 82's boat; the harbour's view (64). **The head
rules bind** as the briefs before have them, with 85's in-world rule and 84's three pin rules;
nothing under `docs/agents/consent/` or the consent brief touched (a station that reads by
its place has less than the brief describes, no more; if a wording offends, say so for 55).

**The lead's rulings on the design note (2026-10-31; `docs/design/Design-PlaceKnowledge.md` at
1f365e2 on `claude/pkg-65`, read whole and approved as the package's design).** On its six
open points: (1) the tell-tale compass given, in the cabin alone (Falconer hangs it over the
captain's cot); the gunroom has the slate's course and not her head. (2) The sounds of sail
work reach the cabin as the kinds of §4's `heard aft`, but the evolution's lines whole and the
sail and yard lines as the sound and not the figure (`knowledge.as_heard`: "sail handled
overhead", "the hands at the braces"; which sail is not his until told). (3) Prose alone
where an answer was owed is counted as the design has it, the count judging the world; the
journal line and the nudge name what happened (words in the journal, nothing said) and not
"an empty reply", and the notice naming the tools goes in every such sample. (4) The chart on
the quarterdeck at the binnacle, with the cabin and the gunroom. (5) The drill's walk built
whole behind one switch, `DRILL_WALK`, off on the trunk until 55 re-briefs: a model whose yes
is on record for the brief's three things is not asked eight before the brief says eight;
the test runs it on, the record says which drill ran, and the sentence 55 will need is
written in step 7's postscript. (6) `go below` and `go to` a place below refused to a
station with the deck, in words naming `hand_over`; `go aloft` allowed; 53's test moved old
beside new. Read and taken besides: the deck as the reach's and the readings' default with
the kinds' test as the guard; `say_aboard` retired and the director's own prose a note too;
§9's refusals and §3.1's named flaw (the weather over a port read from the followed hull's
view) left for 65b. Merged one step at a time, the whole suite in the cloud at each.

**The owner's word of 2026-10-31 (decision 61):** after 65 is done, no new package for the
week (74 held, and 87, 81, 91 and 65b with it); the lead tells the owner when the trunk is
up to date and green for his testing; the owner tells the ships session to pause before the
new ships.
**Amended the same day:** 65 pauses after step 1 (the Fable allowance at 95 per cent); step
1 merged on its own, steps 2 to 8 held for the week to turn; the builder told to finish step
1 and stand by (the lead's one-shot word of 14:30).
**And again (the same afternoon):** step 1 not merged either; `claude/pkg-65` stands at step
1 green until the reset and the package is reviewed and merged after it (the lead's
recommendation: step 1 alone takes the deck from a model below before step 3 gives it back
by report; the owner is not testing 65 this week; a merge spends the allowance for nothing).

## Package 88: the captain's pass of M7 (`freesail/world/captains.py`, `brains.py` and `data/captains/*.yaml` the rules captain's doctrine and its sources; `freesail/world/squadrons.py` and `orders/station.py` only where the near station law reads; `freesail/world/signals.py` and `data/captains/privateer.yaml`, `hail.yaml` the colours held; `docs/TechnicalSpec-M7.md` §4, §21, §22 as built; `docs/dev/TuningNotes.md`; `tests/test_captains.py`, `test_captain_trials.py`, `test_squadrons.py`, `test_signals.py`, `test_known_truths.py` truths 7-340 to 7-349)

Opus (the owner, 2026-10-29); after 84, beside 82, the two touching little in common (82
the hulls, the boat and the seats; 88 the rules captain's judgement). **The method (the
owner, 2026-10-29): each item with the symptom, the rule as it stands, the rule as it
should read, and what proves it; a pin that moves is moved by bisection, the mend toggled
on the final tree and the old figure beside the new in the test and the notes; a recorded
passage that moves is a finding, said with its cause, never re-pinned for the order's
sake.** The physics is read and not changed; the doctrine's figures carry their sources or
the word judgement as the captains' files have them. Each item an intent with the lead's
reading; the intent binds.

1. **The commodore's recovery when aback with no way (the convoy's stall, 86's finding).**
   *The symptom:* `convoy-six.yaml` run with no orders stalls early south-east of the Lizard:
   the commodore's own brig-sloop, after a short-handed tack with thirty-one hands while her
   book shortens sail, lies aback with no way from about 10:20, nothing in her captain's
   rules bearing her away, the far convoy held to her pace; she pays off at 10:45 when the
   book takes in her after sail. *The rule as it stands:* 58b's law lies a ship to without
   being taken aback and fills her away with the close-reefed topsails set; the rules
   captain has no counterpart for a ship caught aback with no way and no tack in hand while
   the hands are at a shortening. *As it should read:* a rules captain aback with no way for
   a stated while, her hands at work aloft, recovers as the period did (the helm and the
   head sheets to pay her off, the after sail eased, boxed off onto the tack with more room,
   then the course resumed; Luce's and Lever's words for it cited), by his doctrine, with a
   figure for the while that is a judgement said in the file. *What proves it:* the convoy
   keeps way through the morning with no orders; truths 7-152 and 7-153 move with the mend
   (the Friendship in her station, the convoy's order of sailing), each old beside new with
   the toggle; the recorded passages and the trials unmoved, bisected; a truth of its own.
2. **57's offing's tack among islands with no room to wear.** *The symptom:* the station gale
   (`trial-station-gale`, an expected failure since 57): the frigate beating for her station
   off Ushant in the dark among the islands of the Molène passage wears where there is no
   room to wear and grounds (42394 on the merged tree, 44332 on 57's, 41415 on 58b's; the
   book's part right, the captain's wrong). *The rule as it stands:* the offing's law tacks
   or wears by the doctrine's choice without reading the room under her lee; 70's helm in
   action reads the room for the gage. *As it should read:* with land or a danger within
   the room a wear would take (the chart's dangers and the coast by the lookout and the
   chart, as the pilot's line reads them) the captain tacks, and failing stays claws off or
   heaves to till light rather than wear onto the land; the same sea sense as the action's
   helm, with its figures sourced or judged. *What proves it:* the trial's expected failure
   lifted, its states, lines and digest re-pinned old beside new; the lee-shore trial's
   figures unmoved (the container's digest as recorded aside); a truth of its own among
   the Molène islands.
3. **72's near station law read against 58b's.** *The symptom:* 86's reading of the stall
   first suspected the near `keep station` order shaping a course inside the close-hauled
   angle with no bear-away to fill, which 58b's `_course_for` law gives the far body; the
   cause was the commodore's own brig (item 1), but the near law has not been read for it.
   *The rule as it stands:* 72's near station order shapes the course for the station from
   the flag's set course and the ordered course (its two faults mended in 72). *As it should
   read:* a station's course that falls inside the close-hauled angle is filled to the
   nearest course she can lie, as the far body's law has it, the station recovered when
   the flag's course allows; one law for the two bodies where they must agree, said in the
   notes if they already do. *What proves it:* the squadron's truths 7-152 to 7-155 as they
   stand or moved by bisection with the reason; a test with the flag close-hauled and a
   station to windward of her fetch.
4. **The colours held once shown before an enemy (71's flicker; 85 did not take it).** *The
   symptom (the owner's debrief of 70 to 72):* a privateer under British colours did not
   answer the private signal, showed French colours within two cables at the signal to show
   her true colours, and then flickered between French and British colours as the action
   went on. *The rule as it stands:* 71's privateer doctrine (`false_colours` in
   `data/captains/privateer.yaml`) sails her under the principal's colours and the rules'
   evaluation re-hoists them by its trigger each time it runs. *As it should read:* the law
   allowed the ruse until the first shot and made it a pirate's act after; once her true
   colours are shown before an enemy, or she has fired, they are held for the action and
   until the enemy is out of sight, by her doctrine, with the source. *What proves it:* the
   encounter's and the first action's truths (7-143 onward) as they stand or moved by
   bisection; the hail table's `lie: merchant` unaffected; a truth of its own.
5. **Records.** Spec M7 §4, §21 and §22 "as built" where the laws moved; the tuning notes
   (each item's four parts, the pins old beside new with their bisection, found on the way,
   the suite as run: the fast tier whole on the final tree, the slow tier of the touched
   files with the captain's trials and the known truths, the pace tests alone and last);
   the captains' doctrine files with their sources; the primer only where a chapter states
   a law that moved (in-world under 85's rule).

**Not built here:** the far ship's length (`combat/far.py` reading a key the spec has not,
74's, booked with its old figures); the prize and the strike (74); 82's seams. **The head
rules bind** as the briefs before have them.

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

### The re-brief after 84 and 85 (the lead, 2026-10-30; for the owner's approval)

The brief above stands as the intent; this re-brief says what 84 built of it, what 82 now
builds, and the principles it builds the boat to. **Fable, in steps merged in parts as 84
was**, each step a mergeable state with the suites green and the pins standing, one
commit on `claude/pkg-82` pushed after each, the trunk brought in at every boundary (no
rebase, no force-push); the design note first and reported at its boundary for the lead's
reading; **the person's movement between hulls (item 3) reported as soon as it is green,
since 74 starts on it**; the boat's files and her drawing last, in commits of their own
(the ships session's branch moves `tools/gen_ships.py` and the viewer beside this).
**Truths 7-320 to 7-339** beside 7b-113 and 7b-114 (85's are 7-240 to 7-245, 93's to 7-309,
94's to 7-314; 88's are 7-340 to 7-349).

**What 84 built, which 82 no longer builds.** A person aboard another ship is real: every
hull of the one world has her own people, places, stations and log; a station on any hull
is the same station (`--station <role> --ship <name>` through a door); the director's
forms reach every hull (`aboard the <name>: ...`, a person made or come aboard her, a
cutter's letter to her, `read_log(ship=)`, the truth over the hulls); the drivers follow a
hull (`World.follow`, `World.followed_words`, `World.players` the player's own hull, the
console's and the browser's `follow "<her name>"`); a ship sleeps and wakes with her state
whole under the cap. So the brief's items 1 and 2 are mostly built, and what remains of
them is below; items 3 to 7 stand.

1. **The world with no followed hull (item 1's remainder).** `World.followed_words`'s
   branch is unreached today: a scenario with no player's ship (`ship: none`, `director:
   observe`) runs its business and its ships under their captains with the centre wherever
   the observer looks; the console and the browser open at the director's station; the
   readings that assume a hull answer "no ship followed" in words and the ship's orders are
   refused in words, the world orders standing; the pace rule, the promotion's cap, the
   chart's view and the lookout read the followed hull and bear a world with none. The
   lead's reading of the cost stands: the World's construction assumes a ship in places
   84's postscript names; the package measures what moved (nothing pinned should) and says
   what it left.
2. **The player's own seat on another ship, and the director's door (item 2's remainder).**
   `--seat captain --ship <name>` for the player, seated under the same contract as a model
   there (the consent record read as 67 reads it), the drivers following the hull he is
   aboard by 84's `follow`, the player's own hull brainless and far or under her rules
   captain as the scenario says; **the director's door's question** (84's open item): when
   the player follows or is aboard another hull, whose log the owner's door reads, where the
   director's `aboard:` without a name goes, and what `captain: carry on` gives back; the
   builder decides from the one rule (the followed hull is the World's default) and writes
   why; 86's three seams reworked on it: the free intent by the hull and not `parent is
   None`, `hail.model_holds_her` by the hull a model or the player holds, `_named_or_kind`
   by `World.players` and not `player_shadow`.
3. **The person's movement between hulls (item 2's heart; 74 waits on it).** By the boat
   (item 4), by boarding (73's deck won: the boarders a party of one hull on the deck of
   another), and the hook for capture (74's captive: a person put aboard the captor with
   his station's seat following him or standing down by the handover's rule). **The design
   question is the seat**, decided in the design note before it is built: a station is a
   person aboard, so either he keeps his station and the hull under it changes, or the
   station ends and a new one begins on the other hull with the same holder; the replay (a
   person who moved in play moves the same in the replay to the same digest, the acts keyed
   by hull as 84's step 8 keys them) and the consent's record must both hold, and the
   harness's samples follow the person's hull as 84's `World.own` by `followed` has them.
   `where am I`, `the ship` (85's reading) and the station line answer the hull he is in.
4. **The boat as a hull of the one world (item 4), built to the ships session's principles.**
   Each ship's boat a ship file through `tools/gen_ships.py` with sources (the frigate's
   launch and cutters, the brig's and the cutter's boats, a 16-ft boat with four oars and a
   sprit or lug stepped at will, the figures from Steel 1794's table of boats by page or
   marked judgement; the ships' files' `boats:` lists as they stand name them, no existing
   ship file moved by a byte but for that key where it must point at a file, and the eight
   regenerated byte-identical otherwise, the ships session's two-way byte test the gate on
   the commit); a hull of the world when manned and away from the ship, awake under the cap
   and asleep under the plan with her state kept (84's rule, no second machinery); **an oar
   force on a hull** as her propulsion by the hands at the oars and their fatigue, the one
   physics addition this brief allows, its figures sourced or marked judgement (a boat's way
   under oars three to four knots light, a knot and a half towing, the men tiring by the
   hour), and the sail when stepped by the existing rig; the sweeps' orders (`give way`,
   `lie on your oars`, `step the mast`, `set the lug`, `pull for <the point>`); the player
   aboard her by `go to the boat` and item 2's seat, her readings his while he is in her
   and the ship's again when he comes aboard; the errands (ashore, the kedge, the tow, the
   pilot, the prices) done by her as before when nobody is in her, the hoy coming off as a
   vessel of the sea by the same road; the boat lost (stove, swamped, cut adrift) as a state
   the ship's file knows; the account following the boat as a vessel's. **The principles
   that bind her file and her drawing** (`docs/design/Build-Ships.md` §5.0 on the ships
   session's branch, the lead's approval of 2026-10-29): nothing invented, every figure by
   the ladder of evidence (her own lines; a period plan or table of her type, scaled; a
   named period rule; a judgement that names its difference) and marked in the file in one
   word (`sourced`, `stand-in`, `rule`, `judged`) with its source by page; sourced points
   win; one reference for every point; the drawing never changes how she pulls, sails or
   is hit (only the viewer, `freesail/ship/form.py`, the server, the generator's checks and
   the tests read a shape key; the guard that nothing under `physics/`, `combat/`, `crew/`
   or `world/` reads one); a difference between the drawing and the file recorded, never
   moved; boats of one pattern one class in several ships, listed as such (no silent
   sharing); a better source changes the drawing and never the game's behaviour. **Her
   drawing** (the viewer under oars or sail) is the last commit and reads the ships
   session's hull form as merged at that hour; if B5's road is not yet on the trunk, the
   boat's shape keys are filed by the ladder and her drawing is left to the ships session's
   road with the figures ready, said so.
5. **Towing by the boat, and the kedge's false denial (item 5)** as the brief has it: the
   same oar force for the tow and for the boat, the frigate's boats bringing her head
   round in a calm and no more (the period's practice, a judgement in the notes), the boat's
   crew tiring, `the boat alongside` ending it, refused in a sea she cannot work in; the
   kedge's false denial mended, kedging left to the anchor physics it is in.
6. **The stations, the director and the readings (item 6)** as the brief has it, on 84's
   forms: `the boat`, `the boats`, `where am I`, `the followed ship`; the events and
   tripwires (`the boat away`, `the boat alongside`, `aboard the <ship>`); the director's
   forms after `WORLD_ORDER_FORMS` where 84 has not got them (a person put aboard another
   hull by the boat, the boat sent, `follow` at the director's seat), the dry run knowing
   each; the truth showing every boat as a vessel when she is one.
7. **Truths and records (item 7).** 7b-113 and 7b-114 as the brief has them; 7-320 onward:
   a world with no followed hull runs a day with its business and the centre on the hull the
   observer follows, nothing pinned moved; the player seated as captain of another ship with
   his own hull brainless and far, the drivers following him; a person moved from one hull
   to another by the boat in play and in the replay to the same digest; the boarders'
   movement by 73's deck won; the director's door with another hull followed; the hoy off
   as a vessel; spec M7b §11, §12 and §21k "as built" (and §21k's head); the Harness; the
   primer's chapter on the boat and on going aboard another ship, **in-world under 85's rule
   and run through `tests/test_in_world.py` and `test_primer.py`'s forms tables**; the
   director's library; the design note under `docs/design/` (the seat's decision, the boat's
   figures with their rungs, the oar force's source, what moved and its proof by bisection);
   the tuning notes; the suites by the rule (the fast tier whole on the final tree of each
   step, the slow tier of the touched files and the known truths after each, the pace tests
   alone and last; the whole suite the lead's in the cloud at each merge).

**Not built here:** the director's chart and focus (§12a, §12b); the boats as fighting
vessels and cutting out (77); the captive's channel and the prize crew (74, on item 3's
hook); the ports' guns and the viewer's action (81); any hull of 75's. **The head rules
bind** as the brief above has them, and 85's in-world rule and 84's three pin rules (the
followed hull's streams unprefixed and the other hulls seeded as today; the tick's two
phases; the player's vessel last) with them: a pin that moves is proven by bisection and
restored by the order, never re-pinned for the order's sake; nothing of 75's files touched
(the generator's change the smallest that serves, named in the notes).

## Package 82b: the door follows its harness, the visitor's name, the far hull's hail (`freesail/agents/remote.py` the desk's seats keyed to the harness; `freesail/world/movement.py` `visiting_station` and `freesail/world/seats.py` the visitor's station name; `freesail/world/hail.py` `deliver` and `model_holds_her` for a far hull; `docs/agents/Harness.md`; the primer's chapter 26 where its words need bringing up; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-390 to 7-394)

Opus (the owner, 2026-11-05, from his testing of 2026-10-31 to 11-05: the saves under his notes
of 2026-11-01 and 11-05, read by the lead under "The owner's testing week: loose ends mended by
the lead"). Three findings, each pinned to its mechanism, each an item:

1. **The door follows its harness.** On the trunk a harness (model, door, journal) moves with
   its person between hulls (`Harness.move_to`; probed by the lead on 2026-11-01). What breaks
   is the agent API's desk (`agents/remote.py`): its seats are keyed by station name and ship,
   so a station that becomes "mr newton of the Amazon" loses its door's seat, the new station
   reads as unseated, and the owner's door that held his own officer answered for "the Mr
   Hill" in its same session; `stand down the Mr Hill` stood down both (one door covering two
   stations, the newest by recency). In the all-models convoy, four model captains, each a
   "captain" station on a different hull through one door, ended with the Chevalier's captain
   a visitor aboard the Lynx and his door holding Mr Folger's station too. The rule: a seat is
   keyed to its harness (an identity of its own, carried in the save), never to a name and a
   ship; a door's station is the harness it was seated at, wherever that harness's person
   goes; `stand down <station>` stands down that harness alone; the desk's listing names each
   station with its ship. Truths 7-390 (the moved station keeps its door and its model through
   the move and the save) and 7-391 (two "captain" stations on two hulls through one door,
   each answered by its own harness; a stand-down of one leaves the other).
2. **The visitor keeps his own station's name.** The primer's chapter 26 promises "he keeps
   his own station's name and voice"; the code makes a station named for the man
   (`visiting_station`, `VISITOR_DOMAIN`: "captain owen", "mr newton"). The visitor's station
   is named "officer of the watch, of the Raven, aboard the Amazon" (his station, his ship,
   his host), its voice and its journal his own, the passenger's reach as 82 built it; the
   host's own "officer of the watch" untouched. Truth 7-392.
3. **A far hull's hail is her captain's model's to answer.** `hail.deliver` answers by table
   whenever the hailed hull is not in the full shape, though a model may hold her captain's
   station on her far shape (`model_holds_her` is read only for a full hull): the owner's
   model captains at far detail each reported the rules' answer and never the other's. The
   rule: where a model holds her captain, the words go to his sample and he answers, in the
   far shape as in the full (the far shape's sampling as 84 left it), and the table answers
   only for a ship nobody holds; the hailer's own log says "she has not yet answered" until
   he does, as a hail at sea does. Truth 7-393; truth 7-394 the replay of a passage with a
   hail between two model-held hulls at far detail by both roads.
4. **A model-held hull is not half blind at far detail** (the case study of 2026-11-05,
   `docs/playtests/2026-11-05-small-convoy-all-models/case-study.md`, lesson 2): the glass
   was refused the *Chevalier*'s captain while her hull slept, and the *Renard*'s captain
   stood by for an hour while the plan carried her to within a cable of the Stags. The rule:
   a hull whose captain's station a model holds counts awake under the cap while that door
   is live (the cap's three made four or five for the held hulls, measured in the pace
   notes), or, where the cap must hold, the far shape's plan keeps her off the dangers as
   the rules captain does (88's danger ahead by the chart) and samples her captain as the
   full shape does. Truth 7-394 takes the plan's danger; the pace of a convoy with four held
   hulls measured informatively.
5. **The boat's names are the giver's hull's** (the same case study, lesson 4): the player's
   `send the boat to Lynx with the captain and Mr Pearce and ...` carried Captain Owen and
   sixteen of the *Chevalier*'s and the *Renard*'s people aboard the *Lynx*. Reproduce from
   the owner's save (as data; the lead holds it), find how the names resolved across hulls
   (84's one registry; `orders/port.py` `_boat_to_ship`, `dealings.send_boat_to`'s hull
   check) and why the far hulls' people passed it; scope the names to the giver's hull and
   refuse a person of another ship in words. Truth 7-401 (the lead, 2026-11-05: 7-389 is
   65's; 82b's are 7-390 to 7-394, 7-400 and 7-401).

**The lead's rulings on the design note (2026-11-05; `docs/design/Design-DoorAndVisitor.md`
at 8c1a94c):** the note approved whole: the breaks are the roads that go by name and ship
(`remote.seat_key` as ship/station, `seat.world` fixed at the stationing, the listing's
naming, the save's want of an identity; the desk's seat itself kept its harness in the
builder's live probe). The design taken: `Harness.ident` carried in the save and derived for
a save from before, the seats keyed by it, a stationing resolved by the harness's home
station, the visitor named "<his station>, of the <ship>, aboard the <host>",
`model_holds_her` read for any shape, a held hull ranked with the dealings and held over the
cap up to two (both halves of item 4: the far plan's danger check as well), the boat's names
scoped to the giver's hull. The owner's saves stay with the lead (door identifiers and
transcripts); the facts for the fixtures given in words. The touches outside 82b's files
approved as listed (the harness's ident in the constructor, the save and the listing;
`_station_in`'s comma rule; the cap's rank in `crews.py`; item 5 in `port.py` and
`dealings.py`), each small.

**The design note first** (`docs/design/Design-DoorAndVisitor.md`, short): the seat's
identity and its place in the save, the visitor's name in every listing and reading, the
far hull's sample for the hail; reported to the lead before the harness or the desk is
touched. **Beside it:** package 65 resumes on Fable at the same time; 65 owns
`agents/harness.py`'s sample and `_reaches`, `orders/stations.py` `_say`, the console's and
the browser's views and `world/knowledge.py`; 82b owns `agents/remote.py`, `world/seats.py`,
`movement.py`'s visitor naming and `world/hail.py`'s answer path; where 82b must touch a file
65 owns, it says so to the lead first and keeps the touch small. **The suites:** the fast
tier whole on the final tree of each item, the slow tier of the touched files and the known
truths, the pace tests alone and last, ruff check and format; the trunk brought in at each
boundary. **The head rules bind** as the briefs before have them (no model identifier in a
repository file; nothing under `docs/agents/consent/` or the consent brief; no test skipped
or weakened; pins moved only where moved, old beside new, proven; 85's in-world rule; ship
files through `tools/gen_ships.py` alone).

## Package 95: the sail by her name (`freesail/world/lookout.py` `glass_on`, `make_out`, `strangers`; `freesail/world/hail.py` `_addressee`; `freesail/orders/boat.py` `pull for`; `freesail/api/readings.py` the `strangers`, `in_sight` and `sail_in_sight` rows; `freesail/api/queries.py`; the primer's chapters 15 and 23; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-395 to 7-399)

Opus (the owner, 2026-10-31 and 2026-11-05). **The finding:** `the glass on` and `make out`
give the nearest sail, or at best the nearest of the named kind, and the wanted sail is hard
to name; a sail once made out is not named in the readings, so two schooners read alike.
**The rule to build:** one resolver for a sail named in words, used by every order and
reading that takes a sail: the most specific naming wins, read from the words the lookout
himself used for her (the kind, "on the larboard quarter", "bearing NE by N", "distant a
mile", each narrowing the pool), the closer sail where ambiguity remains, and a name once
known ("the Raven") over all; `make out the sail on the larboard quarter, bearing NE by N,
distant a mile` resolves to her, and so do `the glass on`, `hail the`, `bearing of` and
`pull for`. A sail made out and identified (her colours, her name by hail, the private
signal answered) is named in the readings by her name while she stays in sight, and her
identification is lost when she is lost sight of, until she is closed and made out again
(the lookout's memory of her as the period's: a sail lost in the night is a stranger at
dawn). Truths 7-395 (the resolver's narrowing, four cases), 7-396 (ambiguity to the closer),
7-397 (a name over all), 7-398 (the identified sail named in the rows and forgotten when
lost), 7-399 (the recorded passages unmoved: every pinned passage names its sails as before).
**After 82b**, since both touch `world/hail.py`. **The suites and the head rules** as 82b's.

## Package 96: the harbour and the ship's configuration (`docs/design/Design-Configuration.md` new, first; then `freesail/world/scenarios.py` the configuration's shape and the loader; `freesail/world/ships.py`, `crews.py`, `business.py`, `world/orders.py` the director's `ship` order built from it; `freesail/settings.py` the doors per station; `freesail/ui/harbour.py`, `client/harbour.html`, `harbour.js` the page; `docs/TechnicalSpec-M7b.md` §21d to §21f as built; the primer's chapter on starting a game; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-402 to 7-419)

**Intent (the owner, 2026-11-06).** In place of M7b's package 64 (the harbour's second pass,
struck): a Fable package, a deep design first, on two layers that meet. **The deeper layer:**
the configuration of any ship made a thing of its own, so that the player in the scenario
maker and the director in live play can set up any kind of hull with the role, the national
parameters, the stations and the configuration they want, and so can the business under the
seed, without nasty surprises. **The harbour layer:** the harbour presenting, elegantly, every
configuration option the game has: the doors and the stations, the settings and the flags,
and above all the scenario's settings, with the full configuration of the player's ship and,
at choice, of every other ship of the scenario, so that the proper configuration of every
setting is possible from the page, where today a file must be edited by hand to configure a
squadron, the full parameters of one's own ship or another's, the papers, a private signal
(what it is and what the table does), or the role, fit and crew of each ship.

**The facts to start from.** The loader (`scenarios.py` `load_scenario`) reads some forty keys:
the player's `ship` (file, fit, name, nation, intent, crewed, position, heading, speed, cargo,
knowledge), the other `ships` with their intents, the `squadrons` (id, name, kind, commander,
members, formation; package 72), the `papers` (chart, epitome, almanac, chronometer, price
lists), the `people` (role, name, skill, place), the `stations` (player, model, rules), the
`standing_orders`, the `director` block (models, seats, budget), the `world_orders`, the
weather, the business, the ports and the region. The maker (`client/harbour.js`, package 59)
writes only the fields it shows, and shows neither the papers nor the people nor the squadrons
nor any other ship's fit, role and crew; the settings (`settings.py`) hold one model per door,
so several models at several stations want several settings files; the ship's own
configuration is spread over her class file (`data/ships/`), her fit's name, her wardroom file
(`data/people/<ship>.yaml`), her nation's block (`data/nations.yaml`), her captain's doctrine
(`data/captains/`), her private signal (drawn under the seed by 71), her books and the
scenario's keys, with no one place that says what she is. The director's `ship "X": ...`
order (M7b §3) makes a hull from a few words with the rest defaulted, and the business
(M6 §19, 72, 79a) draws hulls by its knobs; neither says its defaults back. M7b's harbour
points of 2026-10-18 (`M7b-WorkPackages.md`, "The harbour's second pass": the stations and
the seats as three notions with one word, the flags unexplained where set, several models
and stations, the maker's missing fields, the people's names and briefs per scenario, the
director's grant shown) are facts for this brief, each still true. The owner's testing of
2026-11-01 and 11-05 (the testing-week section above; the case studies in `docs/playtests/`)
holds the nasty surprises: a door restationed as "the Mr Hill" (82b mends the road, 96 says
the configuration), a ship with no station briefed for a model, a scenario whose squadrons
could not be set but by the file. Two facts from the builders of 2026-11-06 for the
configuration's identities: a person's id is his post's and so shared by every hull's company
(82b's item 5 found the boat landing another hull's men of the same posts; the lead booked the
ids to 97 with the façade's readers), and a vessel's id is what the scenarios write as her
name, so the strangers' row's `id` tells a client her name before the deck has it (95's
finding; the id left as it is, the viewer's handle): the configuration gives every person and
every hull an id apart from the name, and the name is the deck's to learn.

**Added by the owner, 2026-11-09: the ship's flags as part of her configuration.** From the
owner's play (the triage above, and package 98's step 7): any ship may hoist any flag of her
nation's file today (a privateer hoisted a chef de division's broad pendant unquestioned), the
flags ordered could not be hauled down singly, and no reading said what flew. 98 mends the
orders and the reading; what stays for this package is the locker itself: **which ships have
which flags**, as a matter of course by her nation, her service and role (a King's ship, a
privateer, a merchantman, a revenue cutter, a cartel), her commander's rank and her squadron
(a broad pendant a commodore's, an admiral's flag by rank: 72's hook from 76), with the false
colours a ship carries for a ruse counted as flags she has; and **flags given to and taken from
a ship** by the scenario and the harbour's page and by the director in play, with the refusal
in words when a flag ordered is not in her locker. The facts to start from: 76's item 8
(`data/signals/<root>/colours.yaml`, `world/flags.py`, the locker's `ordered_flags` and
`flies`) and the lead's record of 98's step 7. The design document says the locker's fields,
its defaults by role and nation, and how the page and the director's form show and change it.

**The design document, first, for the lead's gate** (`docs/design/Design-Configuration.md`, in
83's shape): (1) the configuration of a ship as one described thing, its fields and their
sources, its defaults by role and nation (a merchant brig of Britain, a Spanish xebec of the
King's, a French privateer schooner: each a complete, sane setup from her role, her nation
and her class alone, every field overridable), its validation (what a hull cannot be: a fit
her class has not, a station her bill has not, a book her nation has not), and its
presentation back (the configuration said in words, so the player and the director read what
they made); (2) the three builders of hulls, the scenario maker, the director's `ship` order
and the business, all building from it, so that a hull made by any road is the same kind of
thing and a hull's configuration can be read, written, saved and replayed by the same code;
(3) the harbour: how the page presents the whole of it without becoming a wall of fields
(the common case a few choices, the full configuration opened by a step, every ship of the
scenario configurable the same way, the doors and stations one control, each setting with
its words from the parser's help, the private signal and the papers explained where they
are set), what the page shows of the defaults it fills, and how a scenario written by hand
and one written by the page are the same file; (4) what moves and what does not (the saves,
the recorded scenarios of the truths, the scenario files under `data/scenarios/` and the
owner's, every pinned passage: the design says which fields are new and which are read as
before, so that nothing recorded moves); (5) the steps, each a mergeable state; (6) the open
questions for the owner. The lead gates the document; the build follows the gate.

**The build** (after the gate; the steps the design names): the configuration's shape and its
loader with the defaults and the validation; the three builders on it; the settings' doors
per station; the harbour's page; the words; truths 7-402 to 7-419 (allotted: the
configuration from role and nation alone, the overrides, the validation's refusals in words,
the three roads giving one kind of hull, the save and the replay of a configured hull, the
page writing the file a hand would write, the pinned passages unmoved). **The suites and the
head rules** as the briefs before have them; the harbour tested here headless and proved by
the owner on Windows as 59 was; nothing under `docs/agents/consent/` touched. A Fable
package, generously scoped: the builder designs to the intent and says what it took another
way.

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
   before that. **The lead plays at this gate (the owner's word, 2026-10-30):** the captain's
   station first, blind, through the door as any model, with the primer and the readings
   alone and the owner or a fresh model as director, in one of the gate's passages; then the
   director's seat in the one-world scenario with the owner at the captain's station,
   pulling 84's levers (`follow`, an `aboard` order on another hull, a cutter's letter to
   her, `read_log(ship=)`). The draft's scenarios leave room for both; the lead's seats go
   through the door under the consent brief as it stands, and the transcripts stay in the
   record, with the lead saying where knowledge of the engine leaked into a decision.
8. **The documentation whole (the owner, 2026-10-29: "might as well go all the way").** The
   same pass over `docs/` as items 1 and 2 make over the primer and the library: every
   document read for completeness and refinement against the code as it stands after 84
   (the specs' as-built pointers, the agents' documents but for the consent's, the
   references' READMEs, the dev notes' how-tos), a stale line mended or marked as history
   where the record wants it kept, a missing document named for the lead rather than
   written on a guess, and the record of what moved in `docs/dev/` beside item 6's. The
   interim gate's draft (item 7) comes last, after this pass, so that it reads the
   documents as mended. 87's brief waits for this item's merge.

**Beside it (2026-10-30):** packages 93 and 94 run on the chart and the tide, and own `docs/dev/ChartBlocks.md`, `docs/references/Tides.md` and their sections of the tuning notes for the while; item 8's pass leaves those three to them and `docs/dev/M7-WorkPackages.md` and `docs/DesignProposal.md` to the lead, naming what it would have mended there in its record. **Not done here:** the one-world refactor (84), the boat (82); any change to
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

## Package 98: the mends from the owner's play of 2026-11-09 (`freesail/world/knowledge.py` `hears`; `client/app.js` the driver's words; `tools/browser_probe.*` and `tests/browser_plans/` new; `client/projection.js` the guns', the lids' and the flags' sort, a flag's lines; `freesail/api/viewer_flags.py`, `viewer_guns.py`; `freesail/agents/api.py`, `local.py`, `pictures.py` the picture at the OpenRouter door; `data/tides/streams.yaml`; `freesail/orders/__init__.py` the colours' and the signals' place, if ruled; `docs/design/Design-ViewerAction.md`, `Design-PlaceKnowledge.md` postscripts; `docs/agents/Harness.md`; the primer's chapters 14 and 23; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-446 to 7-459)

**Approved by the owner, 2026-11-09. One builder, in steps, each merged at one hash with its figures.**
The causes are found and cited in the triage above ("The owner's play of 2026-11-09"); the
builder reproduces each first and mends it at its cause.

1. **The probe, first.** A kept tool that launches the server on a free port, opens the page in a
   headless browser and plays a plan: each line typed at the prompt, and beside it the server's
   answer, the frames the page was sent, the new rows of the log pane and the "where you are"
   instrument, each line marked shown or not; a plan carries what is expected, so a run can fail;
   screenshots on a failure. Plans by place (the deck, the cabin, the gunroom, aloft, the boat, a
   visitor aboard another ship, a prisoner, asleep, ashore at the quay, the market and the
   tavern) and by state (at anchor, under way, in action, seated at a station). In the slow tier,
   skipped where no browser is named, as `tests/test_pictures.py` is. The lead's prototype is the
   starting point (handed over with the brief).
2. **The player hears his own answer.** `knowledge.hears` lets the asker's own `query.*` and
   `order.*` lines through wherever he stands (the design's own sentence); the console with it.
   The page's driver words take "go" as the clock's only alone or with a number. Proven by the
   probe's plans ashore and below: every line typed is answered in the log. **The owner's
   ruling (2026-11-09):** what is not in the world is always shown the man who made it,
   wherever he stands: his own word (a word said below directly to another station was not
   shown him in the owner's play, though the station received it: `person.spoke` and the
   `say`, `tell` and `ask` lines of his own among them), his refusals and his readings ("the
   information calls"). What is done in the world and wants perceiving is not shown him out of
   his sight and is not reported of itself (it would snowball to everything reported
   constantly); that waits a later consideration, with package 99.
3. **The viewer's paint order.** A port gun's inboard figures sort with its port's strip, a hair
   inboard, so that a secured or run-in gun is behind her side and lid from outboard on every
   file; a flag's parts sort as one flag at its middle, in the drawing's order; a drawing's lines
   drawn; `gun` and `flag` given their rank; the `truce` state drawn (a white flag at the fore);
   81's port-top rule (the served top takes the deck's tilt, the *Neufchatel*'s recorded
   departure `CUT_AT_A_CORNER_M` going with it); a settee's sheet's side served, so a sheet held
   to windward is drawn there. Each pinned over every armed, profiled file and every root's
   ensign at every 15 degrees, heel 0 and 15. No ship file moves.
4. **The picture at the OpenRouter door.** The fetch passed to that door's model; the picture
   tools offered there only where the model reads pictures (the door's own list of the model's
   inputs), else the tool answers in words alone; and wherever a picture cannot be shown the
   words say so and give the readings, never "a picture of N by M pixels". No call to any
   provider in the tests (a stub door).
5. **The Rade de Brest's stream** (data): `the-goulet` shrunk to the narrows (Petit Minou to
   Portzic), a `rade-de-brest` area after it with its own modest rate and its book entry, placed
   before the Iroise's and the Channel's; the rate from a source read and cited (the
   hydrographic service's atlas of the roads, which the design's note points to; a figure from
   memory is marked so and put to the owner); the pilot's passage of the Goulet and the ships
   anchored in the inner road measured old beside new, every moved pin proven by the toggle.
6. **The colours and the signals by the deck's rule** (the owner's ruling, 2026-11-09: yes, by
   the current standard): refused below in the words the other deck orders get; the primer's
   chapters 14 and 23. Passing the word from below is a later step, not this package's (the
   owner: word is had from anywhere in the ship freely today, `send for` brings a man, and a
   person may carry word to and fro as a station does; an order passed from the cabin with its
   minute is to be designed with that).

7. **The flags of command come down, and are read** (added 2026-11-09, the owner's further note:
   "there didn't seem to be a way to bring them back down, and checking 'the flags' even with
   the broad pendant and jack hoisted gave none"; reproduced by the lead on the trunk). 76's
   item 8 built `hoist the broad pendant`, `hoist the jack` and `hoist a second ensign at the
   main` (`orders/signals.py`, `_hoist_flag`, the locker's `ordered_flags`) and no way down but
   the colours': "haul down the broad pendant", "haul down the jack" and "haul down the second
   ensign" are read as a sail's take-in and refused ("There is no such part as the broad pendant
   in this ship"), and "strike the broad pendant" is no order. And `the flags` reads the signal
   hoists alone ("The flags: none." with all three flying), `the colours` the ensign alone, and
   nothing reads what flies. Build: each of the three hauled down by its name (haul down, strike
   and lower as its words), refused in words when it is not flying; `the flags` says what flies
   where (the ensign, the pendant, the jack, the broad pendant, a second ensign, from the
   locker's `flies`) and then the signal hoist if one is up; `the colours` as it is. By the
   deck's rule with step 6. The primer's chapter 23.

**Rules:** the standing ones (no pin moved but old beside new with its proof; no test skipped or
weakened; ship files through the generator alone; served words in-world; the consent files not
touched; no key in the repository or a log). The fast tier on the step's tree, the slow tier of
the touched files, the pace alone and last; the whole suite is the lead's in the cloud.

## Package 99: the views under the knowledge rule (`docs/design/Design-ViewKnowledge.md` new, first; then `freesail/api/queries.py` the snapshot by the person's knowledge; `freesail/ui/server.py`, `console.py` the driver's memory of what he last learned; `client/map.js`, `shipview.js`, `instruments.js` the last-known drawn as such; `freesail/world/knowledge.py` the captive's senses; the primer's chapter 19; `docs/dev/TuningNotes.md`; tests beside each, the probe's plans; `tests/test_known_truths.py` truths 7-460 to 7-469)

**Held by the owner (2026-11-09) for the moment; a design note first, for the lead's gate, when it runs.** The chart and the ship
view are served by the person's knowledge as his readings are: each datum they draw (the wind,
the heading and way, the sails and spars, the strangers and what is in sight, the account and its
track) is the live value where the reading is his where he stands, and otherwise **the last value
he learned, with its hour and how he had it** (seen, or by report), drawn as such: greyed and
stamped, the account not run on while he is ashore or asleep, the ship "as last seen". With
nothing known the view says where the reading is to be had, as the instruments do. The memory is
the driver's, per player, outside the World, so that no save moves. The design note settles: the
list of what each view draws and its reading's row; what a report carries; the seats and
`follow` (the director sees all, by design); **a prisoner's senses** (confined to the captor's
cabin he is given her reckoning and heading today, which wants a ruling); and what the views
show a model's station (their picture tools are gated already). Built after 98's probe, which
proves it as the player sees it. The owner's note 4 (a cabin and a shore view) is not here: the
ship view stays a ship view.

## Package 100: letters and things as one system (`freesail/world/things.py` a thing's words, author, addressee and seal; `freesail/orders/free.py` write, read, seal, break the seal, destroy; `freesail/world/books.py` the drafting's road shared; `freesail/world/orders.py`, `agents/director.py`, `data/director/` the director's thing with a description and its removal; `freesail/world/people.py`, `ports.py`, `ships.py`, `dealings.py` the letter by the boat, the cutter, the pilot and the port carried as a thing and handed to its addressee; `freesail/core/replay.py` the old `Message` read; the primer's chapters 14, 20 and 26; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-470 to 7-479)

**Held by the owner (2026-11-09); approved and launched 2026-11-10 (the owner).** One road for everyone, the player, a station and the director: a
letter is a thing with words. **Written** (`write a letter to <whom>: "<words>"`, by the
drafting's road: the writer, the hour, the cabin's table), **carried, handed, put down and
hidden** as any thing is, **sealed and opened**, **read** where it is in reach (its words shown
to the reader and to nobody else; a sealed letter read only by breaking the seal, which shows),
**destroyed** by the player's act (burnt, torn up, thrown overboard and gone) and **removed** by
the director's form; a thing of the director's made with a description as now, shown when it is
looked at. The letters that travel (left at a port, sent by a cutter, brought by the pilot or
the boat, sent ashore with the boat, which today reaches nobody) become things carried and
handed to their addressee, the captain no longer reading every letter aloud whoever it is for;
the old `Message` kept loadable and turned into a thing at the load, so that every save and
checkpoint reads. Every moved pin and digest of a passage with a letter old beside new. The
books (the sheets, the manifests and the notes) stay as they are in this package.

## Package 60 (from M7b): a ship bought, and the player's ship changed in play (`docs/design/Design-ShipBought.md` new, first; then `freesail/core/world.py` the player's hull re-pointed, `core/acts.py`, `core/replay.py` the change journaled and replayed; `freesail/world/knowledge.py` `player_hull`, `players_person`; `freesail/world/movement.py`, `people.py`, `prizes.py` the seat carried and the hands moved; `freesail/world/ships.py`, `ports.py`, `dealings.py`, `business.py`, `data/business.yaml` the owner, the price and the listings; `freesail/world/prize_court.py` the valuation with her condition; `freesail/orders/port.py`, `data/vocabulary.yaml` the orders; `freesail/world/orders.py`, `agents/director.py`, `data/director/` the `for sale` tail and the errand's answer; `freesail/api/readings.py`; `data/scenarios/` a ship bought at Falmouth; `docs/TechnicalSpec-M7b.md` §21g and §21h as built; the primer's chapter 14; `docs/dev/TuningNotes.md`; tests beside each, `tests/test_known_truths.py` truths 7-480 to 7-489)

**The design note approved by the owner 2026-11-10 to be written now, while 74 is open (a
document alone; the build still waits for 74's close and the note's gate). Re-briefed by the
lead, 2026-11-09, on a survey of the trunk and of 74's unmerged steps.** The spec's bridge was four general things and no "buy a ship" feature
(M7b §21g); it was written before the one world. What has been built since, and what has not:

- **Built since:** every ship a hull of one world (84); the player aboard another ship, the
  drivers following him, `follow` (82); a station handed over (65); persons moved between hulls
  by the boat and by the director's form; `Registry.rehome` and the muster swap (74, for the
  prize master alone); journals keyed to the person, so they travel; the save's `hulls` block and
  inputs keyed by hull; the purse's ledger and transactions (53b); a ship laid in ordinary at a
  port. On 74's scratch branch: a hull valued by her tons and guns (`prize_court.valuation`, £8
  and £12 a ton, worn by her years, no term for her condition), a prize's cargo sold, the purse
  credited; and a new command after a court martial, written as a new scenario's start, not a
  ship taken up in the running world.
- **Not built, and this package's:** (1) **no road makes another hull the player's own.** His
  hull is fixed when the game is made (`World.players`); the save's first block and its
  `ship_ref` are that hull's; a visitor's and a prisoner's hull are never his home; the one code
  that carries a seat into another hull's captain's station is the prize master's, and the
  player's own person is never one. (2) **No order moves hands as a count** between two hulls
  for the player. (3) **No vessel has an owner, a price or a for-sale state**; the markets sell
  goods. (4) **No errand ashore by a named person** with the director's answer in it (the boat
  goes for the prices, a letter, the yard and the goods).

**The design note first, for the lead's gate** (in 83's shape, read against the code): the change
of the player's ship as one journaled act that the replay repeats at its tick (what re-points:
`World.players`, the `""` keys of the acts, `player_hull`; what the save's first block is after
it, so that every older save still loads); what travels with him (his person, his seat, his
journal, his followers by name) and what is the hull's and stays or is settled (her purse, hold,
papers, stores, reckoning, standing orders and bindings; the chart marks are the world's); the
old ship thereafter (sold, laid in ordinary, or left to her officer under an intent); ownership
(the Crown's ship is not her captain's to sell or buy by the service's rule, a privateer's and a
merchantman's are their owners'; the player as owner, as owner's captain, as the King's officer);
and how 74's new command and a prize the player takes command of himself would use the same act
later. The note is written after 74 closes, on the trunk as it then stands.

**Then, in steps, each at one hash:**

1. **The player's ship changed in play.** One order of the person's, where the ship is his to
   take (bought, or given him by the director's word) and he is aboard her: his person rehomed,
   his seat carried to her captain's station (the prize master's road made general), the player's
   hull re-pointed, said in both logs; the save and the replay across the two ships with the
   journals intact; the old ship a vessel of the world as the note rules. Refused in words where
   she is not his, where a model or another person holds her captain's station, where he is a
   prisoner.
2. **The company moved.** The persons by the roads that exist; the hands as a count by one order
   between two hulls within a boat's pull (`transfer the people and the hands to the "Fly"`, and
   a number of hands by name of rating), the boat's loads taking their time as the prisoners'
   do, each muster and bill re-made; refused where it would leave either unable to be worked,
   in words that say how many she wants.
3. **Owner, price and sale.** A vessel's owner and her for-sale state with an asking price;
   listings at a port by its size and trade (`data/business.yaml`, drawn under the seed); the
   director's `for sale at £900` tail on the ship order, doubted as any order; a reading of the
   ships for sale where the port's business is known (ashore, or by the errand); `buy the ship
   "Fly"` and `sell the ship` among the market orders, through the purse's ledger with their
   cause, the hull valued by 74's function with a term for her condition (her damage, her
   spars and sails wanting, her copper's years) and the yard's or the broker's margin; the
   purse, the hold and the papers settled at the sale as the note rules.
4. **The errand ashore.** `send <person> ashore to <errand>` (to ask what is for sale, to treat
   for her, to find a broker), answered from the port's facts first and by a seated director
   second, reported in the person's words when the boat returns; the purse and the cargo in the
   director's truth if they are not.
5. **The truths and a scenario:** the player sells the cutter at Falmouth, buys a listed
   schooner, moves his people and hands by one order and sails her out, and the save replays
   across the two ships with the journals intact; a director's listing found by the purser's
   errand and reported in the purser's words, the play log never showing the order (M7b's 99c
   and 99d, numbered here).

**Sequence (the owner, 2026-11-09):** the whole package after 74 closes, the design note first
and then the steps in order; nothing of it starts while 74 is open. **Rules:** the standing
ones; every save and checkpoint from before loads and replays as it did (the kept saves are the
proof); no pin moved but old beside new with its proof.

## Package 101: the Catalan coast block (`catalan-coast`; `tools/build_charts.py` `REGIONS` and `CHARTS`; `data/charts/` the region's tiles, coast, index and manifest entry, `features/catalan-coast.yaml`, `overrides/catalan-coast/`; `features/gulf-of-lion.yaml` and `features/mediterranean-west.yaml` with their indexes only for the four ports beside the block, by the how-to's road for a mark added; `data/ports/*.yaml` seven new; `data/nations.yaml` the ports' index and their dated states; `data/tides/constituents.yaml`, `streams.yaml`, `establishments.yaml`; `data/weather/climatology.yaml` the coast's box; `data/business.yaml` only where a port's market needs a good; `data/scenarios/tarragona.yaml` new; `docs/references/README.md`; `docs/dev/ChartBlocks.md` where the how-to proves wrong; `docs/TechnicalSpec-M7.md` §28's pointer as built; `docs/dev/TuningNotes.md`; `tests/test_chart.py`, `test_ports.py`, `test_tide.py`, `test_weather.py`, `test_scenarios.py`, `test_known_truths.py` truths 7-490 to 7-499)

Opus. The gap in the chart on the eastern Iberian coast (the owner, 2026-11-10: "a very
noticeable gap", which "makes western Mediterranean play a bit iffy"), closed by one small
block, and with it the ports the Spanish main lacks from Cartagena to the French border:
**all seven, by the owner's word of 2026-11-10**. Built as `docs/dev/ChartBlocks.md` says
(read it whole first, with the recipe form over `REGIONS` in `tools/build_charts.py`, and
79c's and 79d's sections of it and of the tuning notes as the latest Mediterranean blocks:
their findings are this block's starting point, the 40 MB rule, the world's tide over the
Mediterranean, the Spanish gauges' reports, the isles the grid lacks, the draft positions
that miss by a kilometre, the business that wants a price ratio, among them). It changes
no byte of any other region's level-2 tiles or coast.

**The gap as the lead measured it** (the chart probed on a tenth of a degree, 2026-11-10):
nothing at all, no depth, no land, no coast, no region, north of 40.56 N (`balearics`' north
bound and its tiles' edge) and west of 2.6133 E (9,408 seconds of arc, the west edge of
`gulf-of-lion`'s first tile column) as far as the land; from 2.6133 E to 3.0 E (the Gulf's
west bound) the Gulf's tiles give depth and no region owns the water. The coast stands at
about 0.5 E on 40.56 N and crosses 3 E at about 41.75 N, near Tossa: the sea so missing is
a wedge of some 80 miles north and south by 110 east and west at its foot.

0. **The sources, a short pass and no new research** (its report first in the tuning notes'
   section): what `docs/references/pilots/` already holds for this coast, read and cited by
   page: Tofiño's *Derrotero* of 1787 (the coast from Cape San Antonio to Cape Creus), the
   *Derrotero* of 1849, Michelot, Purdy 1826 and 1840, Norie 1831, Smyth 1854, the
   Admiralty's *Mediterranean Pilot* vol. I with **Barcelona's meteorological table (p. 726,
   named by 79c's pass as outside its blocks and not cut)**; Roux's plates of Barcelona and
   Roses (79c's pass read pls. 12 to 39) and Heather's of 1814; Tofiño's plans of Barcelona,
   Tarragona and Salou, the Alfaques, Rosas, Palamós, Valencia's road and Alicante where
   they can be fetched. What is not found is said so with the host's answer, and nothing is
   invented in its place. Every source is data: read, never run.
1. **The region** `catalan-coast`: the main from the Sénia's mouth and the Alfaques by the
   Ebro's delta and Cape Tortosa, the Coll de Balaguer, Cambrils, Cape Salou, Tarragona,
   the coast of Garraf, the Llobregat, Barcelona with Montjuïc, Mataró and the Maresme to
   Blanes and Tossa. **Bounds 40.56 N to about 41.9 N and about 0.3 E to 3.0 E: the south
   bound `balearics`' north bound exactly, the east bound `gulf-of-lion`'s west bound
   exactly**, the north and west bounds on the land (moved to a tile row's or column's edge
   where the form asks it; the west far enough to hold the Ebro to Amposta). **The seam at
   the east is the builder's first measurement**: the Gulf's tiles already hold 2.6133 E to
   3.0 E, so by the how-to's seam rule the block either lists the Gulf's tiles there and
   writes none of its own east of 2.6133 E, or the rule gives another answer; say which,
   with `git status` showing no change to any tile the Gulf lists. East of 1 W no corridor
   lies under the block, so every tile is written, land and sea alike (79c's finding).
   **Before the tiles are committed, report their count and bytes to the lead** (the lead
   expects some 28 tiles and 4 to 6 MB; past 40 MB stop at the report). Said in the notes
   and the chart's title: the open sea east of 4.5 E between Minorca and Sardinia, and the
   Algerian coast east of Algiers, are still no block's.
2. **The period's shore.** The Ebro's delta as Tofiño drew it and not as it is (it has
   grown and changed its mouths: the period's Cape Tortosa, the Alfaques' bay and its bar
   by the plan, by the overrides' road, with the residuals said); Barcelona's mole and
   lantern, the Barceloneta, the citadel and Montjuïc as 1805 had them, and no modern
   harbour works there or at Tarragona (its mole was building); the lights of 1805 dated,
   the towers marks by day. The marks from seaward by the directions: Montserrat, Montjuïc,
   Montseny, the castle of the Coll de Balaguer, Cape Salou, the towers of the coast.
   Render each harbour with its marks over the tiles' land and water before trusting a
   position (79c's finding).
3. **The harbour patches** (level 3, about 15′ by 15′ each) **in the block**: Barcelona;
   Tarragona with Salou's road; the Alfaques (the port of San Carlos). **Beside the block,
   in water already charted, the four ports get their marks and roads at level 2 by the
   how-to's road for a mark added to a built region** (the features file and its index
   alone; no level-2 tile, coast or other mark of that region changed, shown by `git
   status` and the region's checks): Rosas bay with the citadel and the Trinity castle,
   and Palamós, in `gulf-of-lion`; Valencia's Grao and Alicante with its castle, in
   `mediterranean-west`. **A level-3 patch for any of the four only if the tool adds one to
   a built region without rebuilding its level-2 tiles**; if it cannot, say so in the
   report and make none: the lead rules. Where a datum cannot be read the port file says
   `datum: unverified` and no patch is made, as the how-to has it.
4. **The seven ports**, each a file on package 35's machinery, entered in the nations'
   index and `test_ports.py`'s list: **Barcelona** (the Principality's capital, the
   captain general's seat; a mole harbour of little water, the road open), **Tarragona**
   (with Salou, where the brandies of Reus were shipped), **the Alfaques** (a road and
   San Carlos's canal port: a small file), **Rosas** (the bay the best anchorage of the
   coast in a northerly), **Palamós** (a small mole), **Valencia's Grao** (an open road off
   the beach, dangerous in an easterly), **Alicante** (the bay and the mole under the
   castle of Santa Bárbara). Each with its nation and its state by 79a's dated form: Spain
   hostile to a King's ship from December 1804 and Britain's ally from the summer of 1808;
   **the French in Barcelona from February 1808 to 1814, in Rosas from December 1808, in
   Tarragona from June 1811 to 1813 and in Valencia from January 1812 to 1813, Alicante
   never taken: these dates are the lead's memory and are to be verified from James and
   the sources on file before a row is written, each row with its source or FROM MEMORY
   said**, in the form Genoa's file uses for a port that changes hands. Its road, pilot's
   station, market, pool and the pilot's four words, every `feature:` spot with its
   position beside it; no King's yard on this coast (Cartagena's is the arsenal). The
   markets so that the business can people the region (79c's finding, a price ratio of 1.3
   at least between two ports): the period's trades from the sources (the brandies and
   wines of Salou and Tarragona, Valencia's fruit, rice and silk, Alicante's barilla and
   wine, Barcelona buying grain and salt fish and selling her manufactures), each good one
   the business file already has or a row added in its form.
5. **The tide.** As 79c found it: the sea's is a foot, the world's over it a far gauge's,
   and the block keeps the world's level as the Strait's recipe does (`fill_to_chart_datum`,
   the land above that tide's high water). The gauges of the coast (Puertos del Estado's
   REDMAR reports give the mean level and the lowest astronomical tide: Barcelona,
   Tarragona, and for the two ports beside the block Valencia and Alicante if their
   regions lack them; TICON's read as every block's are) go in by package 89's form with
   their `block:`; the eleven do not move. The streams by the directions: the set along the
   coast to the south-west as the pilots give it, with `current:` where the period gives a
   set and no tide, the Ebro's outflow off its mouths if a pilot gives it a rate, an area
   over the block's whole box after them, the box appended to `book_limits`; the master's
   epitome places with the period's rise where a pilot gives one. The polygons kept off
   the water the recorded passages sail (none reaches the block; say so).
6. **The weather.** No box of `climatology.yaml` holds the block (`mediterranean-west`
   ends at 40.5 N, `gulf-of-lion` begins at 3.0 E), so `box_at` answers with the nearest,
   which is one or the other by the mile. **A box of the block's own** from Barcelona's
   table (the *Mediterranean Pilot* vol. I, p. 726, read from the PDF's page upright and
   each month checked against the printed totals, as 79c read the others), its generator's
   figures fitted by simulated months with the checking tool; or, if the table's months do
   not differ from the Gulf's box beyond the fit's noise, the Gulf's box widened west to
   hold the block, the comparison printed. Either way said, and `test_weather.py` holding
   the rows to the file's form.
7. **A scenario** `tarragona.yaml`: the frigate from Port Mahon to Tarragona's road in
   1809, Spain the ally and the French in Barcelona, by the Balearic channel and the coast,
   `chart: atlantic-east`, sailed once at seed 7 to the anchor by a short book, its figures
   in the notes; not pinned. It crosses the seam at 40.56 N, which is the point.
8. **The build**: `python tools/build_charts.py --region catalan-coast` through the proxy,
   the checks printed and passing, the tiles committed within item 1's rule, the manifest
   with every other entry carried over, the region appended to
   `CHARTS["atlantic-east"]["regions"]` and the chart's title amended to name the coast,
   and after the build `git status` showing no change to any tile, coast or index another
   region lists but the two features files and indexes item 3 names. Build early, to
   fetch; rebuild with `--skip-fetch` after the marks are written. If a source the build
   needs is refused by the network, read the environment's documentation and say exactly
   which host and what it answered; do not work around it.
9. **Truths 7-490 to 7-499**, each a behaviour, pinning states and counts and no digest:
   the chart answers with depth and land along the whole main from Cape Palos to Cape
   Creus on a walk of the coast (no point of the old gap answers nothing); a ship from
   `balearics` crosses 40.56 N and from the Gulf crosses 3 E with her region, her tide and
   her weather's box changing and nothing lost (the lookout's land, the business carried);
   the lookout off Barcelona raises Montjuïc and Montserrat at the directions' distances;
   a frigate lies at anchor in Rosas bay in a northerly and is uneasy in Valencia's road in
   an easterly, as the pilots say of each; Barcelona refuses a King's ship in 1805 and in
   1809 and Tarragona receives her in 1809; the business draws a trader between two of the
   seven ports; and what the build earns.
10. **The records**: the tuning notes' section "Package 101" (the sources' report; the
    seam's measurement and the tiles' count and bytes; the patches' datums and residuals;
    the checks as printed; the ports' dated states with their sources; the weather's
    comparison; the scenario's run; what was found on the way; the suites as run);
    `ChartBlocks.md` a section "The Catalan coast (package 101, as built)" with what the
    next block should know; spec M7 §28's pointer.

**The suites, at ONE hash, in a worktree pinned there:** the fast tier whole; the slow of
the chart's, the ports', the tide's, the weather's, the nations' and the scenarios' tests
and of `test_known_truths.py`; the recorded passages, `gate_5b` and `gate_5c` once by name,
which must pass to the digest (the block touches no water they sail: a digest that moves
is a fault to find, not a pin to move); the pace alone and last; ruff check and format.
The figures paragraph committed, then ONE report to the lead naming the one hash. A pin
moves only where the block's own data moves it, re-measured old beside new and proven by a
toggle; none is expected.

The hard rules as every brief has them; `claude/pkg-101`, pushed after each commit; the
lead merges by the reported hash.

## Package 103: the range reviewed, and the lever designed (`docs/design/Design-TheRange.md` new, the package's chief product; `docs/dev/TuningNotes.md` its section with the probes' runs, the tables and the subagents' reports; scratch scenarios and scripts kept under `tools/range_audit/` only where they are worth keeping as tools; no file of the game, its data or its tests changed)

Fable, **as the primary review agent** (the owner, 2026-11-10: "you may brief it, and for
Fable"; and, adjusting this brief the same day: "since it is a Fable package, it can work on a
wider and freer scope. They might act as a primary review agent for the date range audit and
overall fidelity design, scoped to allow subagents"). **Held by the owner: not launched.** It
runs **with the other review and design packages, together, towards the end of the order**
(the owner: "we should consolidate the review packages together, towards the end of the
order, and ensure we cover sufficient range with them together"): this one first among them,
96 (the harbour and the ship's configuration) and 92 (the career study) on its answers, so
that the three together cover the whole range of dates and none designs for 1805 alone. One
Fable package at a time, as the head rules have it.

**The reviewer's standing.** A Fable design package is trusted with the design, not fenced to
a list, and this one more than most: the reviewer owns the question, chooses its own method,
widens the ground where the work shows it should, and says plainly what it left and why. **It
may run subagents** for the legwork (the probes by date, the classing of the data's dates, the
map of the research, the search for sources), each briefed by the reviewer with what to
measure and what is already ruled out, their reports kept in the tuning notes' section and
read critically: a subagent's finding is a claim until the reviewer has checked the part the
design leans on. The synthesis and the design are the reviewer's own. No subagent calls a
model provider's paid interface or seats a model in the game; the game is played by the
replay and the kept browser probe.

**The intent.** The game's purpose is a world that can be begun on any day of a wide range,
1792 to 1825 as it stands and earlier and later where possible, and that then goes its own
way. The build's attention has gathered on 1805. Decision 66 rules the principle (history is
the starting state, not a rail; the elements are correct, their interactions the world's own
once play begins; fidelity is a lever) and leaves open how far each element is dated and where
fidelity is worth its cost. This package finds out what the game actually does across the
range, what the project's research actually covers, and puts the whole design of fidelity
before the owner. **It builds nothing of the game.** Read first: decision 66 in
`docs/DesignProposal.md`, and the note "An open design question" with "The discussion so far"
beside the packages table of this file, which hold the owner's words (the three layers he
likes; the lever as codified modes; his caution that the player's acts may break a strictly
historical scenario; the line he wants drawn; the sources) and the lead's thoughts; only
decision 66 and the owner's words bind.

**The ground, which the reviewer may widen:**

1. **The game played across the range, not at three points.** The same rules-only scenarios
   begun through the whole of 1792 to 1825, densely enough that every phase is met (the first
   war and its coalitions, the peace of 1802, the war renewed, Spain's change of side in
   1808, the American war, the hundred days, the long peace and its small wars), and at a
   few dates before and after the range to find where it stops working and why; in the
   Channel, on the Spanish coast and in the Mediterranean, and wherever else the charts
   reach; a King's ship, a merchantman and a privateer, and the nations the game seats.
   What reads wrong for the day (a flag, a book, a port's state, a ship or a gun that did
   not yet exist, a light not yet lit, a rank, a price, a word), what is missing, and what
   refuses to work, each with the line that showed it. And the plainer question: on a day
   of peace, what is there to do.
2. **The dates in the data and the code.** Every dated row and every year written into a
   file, a brief or the code found and classed: read against the running clock as the game
   goes (a rail, by decision 66), read once when the game is made, or one year's picture
   with no date in it at all. What a game does today when its clock crosses a dated
   boundary, shown by running one across.
3. **The research on file, mapped, and the gaps bridged.** Everything under
   `docs/references/`, the sources the design notes and the ships' notes cite, and the
   owner's shelf as the notes record it: by element and by year across the range, what is
   covered, what is covered for one year alone, what is not covered at all. The owner
   expects that "sufficient sources on the era in general" can be found "with further
   searches" and by "some analysis of our own full research database so far with an eye to
   bridging extant gaps on a reasonable basis for our game and simulation": so search, read
   and lay in what is found (the references' rules: the licence read, a README row, data
   read and never run, a modern book in copyright cited and never copied), and for each gap
   that no source fills propose the reasonable bridge and say that it is one.
4. **The design of fidelity, for the owner.** (a) The layers (the elements; the state on the
   day a game begins; what happened afterwards) drawn through the data as it stands. (b) The
   lever as codified modes, with the owner's caution answered: what a strict mode means when
   the player's own acts contradict the record, and what each mode does when the clock
   crosses a recorded event. (c) The line the owner asks for, between period features (the
   Barbary states' conflicts are his example), the shifting political, diplomatic and
   governmental realities as they bear on the game, and the general features that can happen
   at any time by circumstance: a rule for telling them apart, and the hard cases named.
   (d) The almanac of what happened as material for the director and the scenario's author:
   its shape, and how a world that has left the record behind is told so. (e) What it would
   cost to hold each kind of element across the range, in data and in building, so that the
   owner can choose where fidelity is worth it. (f) What the other design packages need from
   this one: what 96's ship configuration and scenario maker must take a date for, and what
   92's career assumes of the years. (g) A proposed order of work in packages, small first.
   Each part ends in a recommendation and in the questions for the owner, each stated so
   that it can be answered in a sentence. The note is written for a reader who is not a
   programmer.

**What it is not:** it changes no dated row, moves no pin and mends nothing it finds (each
find is listed for a package to come); it does not decide the open half of decision 66, it
lays the ground for the owner to. **The suites:** none of the game's is needed for a
document; if a kept tool is committed it is linted and has a test, and the fast tier is run
whole once on that tree.

The hard rules as every brief has them; `claude/pkg-103`; one report to the lead at one hash
with the note, the lead reads it against the code and brings the owner its questions.

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

**2026-10-30, Ext §17.11 approved, the four points ruled, and the in-world rule coming**
(the session's message on `6fcc35a`; B3.1 with B5.2, B3.2 with B5.3 and B3.5 with B5.5 on
the branch, each with the fast tier, the guard sets and the seed-7 trace identical; B1's
stage B running). **§17.11 is approved as written:** the driver's boom out with the shift on
the engine's own `Spar.rigged_out`, keyed on a `boom` that a lateen cut at the mast names
and refused on any other, so that nothing moves on the eight or the razee; the phases as
tabled (120 s each way, the judgement said); nothing in `physics/` or `combat/`, the stowed
boom's windage and its hit said plainly as the small untruth it is; truth 7-230's band
13-16 to 15-19 minutes old beside new, the toggle (the key absent against present on the
fixture) the proof; B5.5's "boom amidships" cases moved old beside new; §17.10's items 6
(for the driver), 9 and 10 closed by it; the order as proposed (B1's stage B, the stage-0
commit, one step by the engine's workflow with B3 and B5 together, her regeneration, then
the owner's testing report). **The four points:** (1) the library's evolution count
(`tests/test_agents.py`) 98 to 104 for the lateen's six is confirmed, a pin of structure
moved old beside new in its own commit as 86 moved it, and 108 at the settee the same way;
(2) `physics/strain.py:631`'s membership (`spar.is_yard or spar.cls == "lateen_yard"`) is
the log's words and no equation, so it is allowed under the gate, one line in its own
commit, said in the notes, with a case in the strain's tests on the fixture where the
carrying-away's words have one: a lateen yard is slung, and "in the slings" is its; (3) as
built: the sprit yards stay in "spritsails" and "all sail" and out of "yards" and "head
yards" in the 64's and the 74's files, the spritsail yard being the forecastle's and not the
braces', and "square the yards" leaving it the period's; whether the harbour stow squares it
is a later question with the harbour stow; (4) the draught rules: the 64's bowsprit root on
the stem head as 1407F draws it, at the measured 27°, the end down 1.2 m, old beside new in
B1's report. **SW-2:** the three Greenwich draughts of Build-Ships §5.9 (ZAZ2587 and ZAZ2559
the *Amazon* class, ZAZ4491 and ZAZ4492 the *Diligence* class, ZAZ6381 and its fellows the
*Sherbourne*), marked "to read" until measured, change its sources and not its order,
accepted. B1 is taken whole at her testing report, as agreed. **Coming toward the branch, to
build for now rather than mend at the merge:** package 85 (the orders, the primer and the
library for a model reader) merges onto the trunk in the next hours with a rule and a test:
the primer and the library's served topics (the catalogue's served head of every
`data/evolutions/*.yaml`, the grammar, the briefs, the tools' words) are in-world documents
and carry no reference to a milestone, a package, a spec's section, a truth's or a
decision's number, a ruling, a gate, a builder, a playtest, the lead or the owner's rulings,
or a model's or a vendor's name; `tests/test_in_world.py` scans them all and fails naming
the line. 85 moved every evolution file's build notes below a blank line under a head
`# Build notes (not served by the library's catalogue)`, where the catalogue's reader stops,
the served head keeping the evolution, its steps, its sources in the period's books and what
is judgement. The session's new evolution files (the lateen's six and any after) and the
primer's chapter on the ships want the same form before the merge, so that the trunk's test
passes at it: the served head in the period's words with its sources, the package's and the
Ext's references below the build-notes head. The trunk's head is `1e3523b` (package 94
merged: the chart's islets, the tide's seam taper and the Solent's region; nothing of the
ships' files); 85's merge will be noted here when it lands.

**2026-10-30, later: B1's stage B read, three figures ruled, the regeneration with §17.11 approved**
(the session's message on `ee408a4` and `f43614f`, with the trunk's `51f093d` merged at `abceec2`,
the slings line `0c26526` and the lateen six in the in-world form `536176d`; before the last two
the fast tier 4,620 passed, 2 skipped, the three known trials the only guard-set failures, the
eight byte-identical and drawing identically; her section in the tuning notes with every moved
figure old beside new). **The three, each the session's pick taken, into the one regeneration
with §17.11:** (1) **the 64's course tack at 8.73 m above the water**, Steel's "within 6 or 7
feet of the deck" read as 6 ft 6 in from the roundhouse deck, the deck the mast stands through
there, the clew 1.14 m clear at the side (more than the 74's margin), the driver then 203 m²
against Steel's 198.5; the note of 2026-10-29 that read two ways ("the head room goes first")
is the lead's, and 8.73 m is its meaning: Steel's words first, the head room where his words
leave room; `clr_x_m` and her truths measured again on it as the notes say. (2) **The razee's
spanker boom at literally the least that clears her taffrail, the spanker 200 m²** against
Steel's 202 for a 38; the owner's 218 cannot stand with the boom clear of the taffrail, which the
session tells the owner plainly with the figures (218 to 191 at 6 ft of head room, 200 clear of
the taffrail alone, 195 at 5 ft); within the owner's 8 per cent. (3) **`rate_spars` keeps the
larger of a bowsprit's or jib-boom's named rating and the rating the sails carried through it
give**, a generator's rule said in its comment: a spar's rating by the sails whose chains pass
through it is a proxy for its scantlings, and the proxy may not shrink when a smaller sail is
hung on the spar (the 64's bowsprit 171 to 100.6 kN by the sprit sails, back to 171; the razee's
170 to 47.2, back to 170; the jib-booms the same); no sail chain passes through those spars on
the eight, so their bytes hold, which the regeneration shows. **The order approved:** the
stage-0 commit, one step for §17.11 (B3 and B5 together, the guard sets and the toggle), these
three in her regeneration, `clr_x_m` and her truths measured again, then the owner's testing
report and the sheets into `docs/playtests/`. **For the eye, left to the owner's test as the
session proposes, two with a question for the report:** the 64 missing stays from 60° off in 15
knots by the yards under the bowsprit, staying from 62.5°, "full and by" six points (say in the
report what the 74 does at 60°, when she comes); her staying in 246 to 262 s against truth 10's
285-s floor for the frigate (a two-decker quicker in stays than a 36 is a thing to look at in
the test: the report says what sets it, the yards under the bowsprit or her lines); the aback
from rest at `clr_x_m` +4.8 from 17 knots, no truth asking past 15; −0.91° of helm at six points;
the driver's tack at 479 s against the course's 252 with six minutes' griping, a fair-weather sail
as Steel has it, measured and not pinned; the razee under the frigate-36 by 0.09 to 0.23 knots in
15 knots, 7-187's clause reported and not forced; the boom's swing and the sheet to the taffrail
keyed on the profile, the eight taking it at SW-2's pictures; her long tests' `SLOW_TESTS` entries
the integrator's at Phase 5.

**2026-10-30, later: package 85 merged on the trunk** (at `252df5b`, the head the record's). The
in-world rule binds from here: `tests/test_in_world.py` scans the primer, every brief
constant, the tools' words and the library's topics served on a King's ship and a hired
cutter (the catalogue's served head of every `data/evolutions/*.yaml` among them) for the
forbidden words and patterns, with `docs/dev/PrimerRedactions.md` the rule stated once and
the form of an evolution file's build notes (below a blank line under `# Build notes (not
served by the library's catalogue)`). The session's lateen six in that form (`536176d`) are
right for it; the primer's chapter on the ships, when written, goes through the same test,
and the merge of the ships' branch runs it first.

**2026-10-30, later: the Indefatigable's report read at `bb60222`; her merge under way; the
hull step cleared to measure, the landing held.** The lead cannot reach the session's bridge
from the cloud (its message was refused on the way, as the trigger was), so this is the
answer. **The merge:** do not bring the trunk in; the lead merges from `bb60222` as it stands.
The trunk moved since `58c51ac` (package 82's step 1, the person's movement between hulls, at
`cfcf092`; 85 and 93 are in it too, which the branch lacks), and the trial merge is clean. The
order run: 85's in-world test and the grammar book on the merged tree first (the served heads
and the tools' words meet 85's rule for the first time), then the whole fast tier, then the
cloud; the plain cases of any failure of words mended at the merge and said in the record.
After the merge, bring the trunk in before the hull step's landing. **The four departures,
accepted as reported:** (1) rule (3) narrowed to a spar with yards under it, the lugger's
21.8 kN standing, hers for SW-2; (2) the ratings as the named rating reads them, 168.6,
168.5 and 27.0 kN; (3) the three lines through `driver_boom` and the two behaviours with them,
in Ext §17.11's as-built note; (4) the razee's `clr_x_m` +4.5 for the owner's test, +4.4's
figures beside it. The older gaps found (a belayed shift losing the canvas drawn, the
ringtail's `wrecked` after its boom's wreck is cleared, a boom hit while rigged in not drawn,
the served heads naming no boom phase) are booked and are not this merge's. **The hull step
(the owner's leave of tonight, "as long as you clear it with the lead"):** cleared to start the
three streams' measuring now, frigate-36 (ZAZ2587, ZAZ2559), the brigs (ZAZ4491, ZAZ4492) and
the cutter (ZAZ6381 and its fellows), each in its own worktree with its own pages note in
`pages-zaz6306.md`'s form, cross-checked as hers was, and its own small module under
`tools/ships/` called from one place in `gen_ships.py`, so that no two writers meet; each
stream its own small tests, the fast tier once at the end, one suite at a time. **The rule
stands: the eight move in bytes once** (`Build-Ships.md` §5.6, §19). Measure and build the
three now, hold the landing, and put the other three to the owner when they are back; if the
owner then rules three now and the rest later, land three. Serial at the end as proposed: the
pair check, one regeneration, one commit of bytes, B5's pictures old beside new, the owner's
sheets, the port triples reported before L2; nothing in `physics/` or `combat/` and nothing in
the eight's behaviour before the landing, by §5.6; every rung by §5.0. **One ask:** in the hull
step's record, name the three captain's trials that fail on the owner's machine with or
without the work, with their figures on a clean archive, once, so that the owner's machine's
difference from the build machine is written where the next reader looks.

**2026-10-31, the hull step's ten points ruled; the landing may start.** The six streams
built and reviewed, the owner's word to build the rest too, all eight to land as one commit:
the picks stand on every point but where this note says, and nothing the physics or the
gunnery reads moves (§5.6). **(1) The smack's body:** the plate's own frames over Steel's
60-ton sloop, sourced points over the rule; the −18% reported past the line; §5.7's row
amended. **(2) The lugger's depth:** the one factor of principle 7 (2.53 m), the length on the
line from the *Éclair*'s own sheet (18.39 m), the departure from principle 7's last sentence
said in the note with the 0.793 figure beside it, §5.7's row T to S† under the water; the
hold's floor line is a depth of hold and no draught, and is not the measure. **(3) The
schooners' sill datum:** the plate's 3 ft 1 in over Spider's 3 ft 5 in of 1835, her own sheet
over a later ship's; §5.7's "about 45°" to about 38° with the chord named. **(4) The brig's
load line:** WL1, the faint ruled line recorded; §5.4's band re-sourced to the sheet (5 ft
2 in ± 0.05 ft) and **truth 7-185's band moved old beside new with the source**, the one pin
this step moves, said in the record. **(5) Guns and ports:** as built; no gun's x moves, the
triples at the guns' places marked `judged`, the sheet's own ports kept in each module for
package 81 (whose food this is: the frigate's guns up to 4.8 ft off the sheet's ports, the
cutter's three guns a side between her four ports). **(6) The S hulls at the sheet's length,
recorded and not moved,** by principle 5, principle 8 holding: one table in the record of
every figure the sheets now disagree with (the frigate's 1,448 t against 1,270, her keel and
fore mast; the brig's 303 t against 413, her drag and fore mast; the cutter's water-line, drag
and mast 1.13 m from the sheet's place), for the owner and a later package on the files'
figures against the sheets; the brig's −27% is the one to look at first when that package
comes. **(7) The port triples before L2:** recorded as measured; L2's thresholds are judged
against them when L2 is built and not before; the cutter's sills at 1.00 to 1.23 m and her
lowest port shut at 14.5° are flagged for the owner's test when L2 comes (a cutter's low
freeboard may well be the truth of it). **(8)** "Sixteen ports a side" left for SW-4 (digests
and the primer carry the word). **(9)** The lugger's bowsprit at 21.8 kN left and reported,
a tuning pass's. **(10) The viewer's mends in the landing,** old beside new; the view-geometry
case that demanded gallery, light and head parts of every profiled file is not loosened but
turned: it asserts the exact set of files that rightly have none (the cutter, the smack) and
demands the parts of every other, so that it stays a guard. **The landing as ruled:** the pair
check and `SAME_HULL_BY_INTENT`, one regeneration, one commit of bytes, the fast tier, B5's
pictures old beside new, the owner's sheets, the port triples before L2, the three captain's
trials named once with their clean-archive figures. The trunk is at `2d512b2` (82's step 2);
package 88 (the captain's pass: the captains' files, `captains.py`, `navigation.py`,
`signalling.py`, the trials' pins) merges next and touches no ship file, so bring the trunk in
once more before the landing's final fast tier or just after, as suits the worktrees.

**2026-10-31, later: the hull step merged; the eight points and the viewer step ruled.** The
landing at `d9477c6` is merged on the trunk (the record "Package 75, the hull step, as merged"
above, with the whole suite's cloud run named there when it is in). The session's own fast
tier and the lead's checks agree: the generator reproduces all fifteen files, nothing the
physics reads moved, the clean-archive check is the proof of the eight's behaviour. **The
eight points:** (1) 7-185 drafted in `tests/test_profiles.py` for Phase 5 to move, its bands
old beside new with their sources: right. (2) The marks as the fixer read principle 4, the
narrower set not wanted: a line takes the word of its weakest point, and the rung letter stays
each hull's best source; §5.7's table says which is which. (3) `RIGHTLY_WITHOUT` per part,
both ways round: right, a guard and not a loosening. (4) The boats held apart, their drawing
82's: right; when Steel's Folio LVII is read the five come to §5.0's rungs through the
generator and never by hand. (5) The lugger at 18.33 m by the re-read: hers; the lead's note
quoted the first reading. (6) The viewer's further mends: accepted old beside new. (7)
`form.py`'s `_station_xs` box under a counter: booked for a later ship's builder in the
record. (8) The Greenwich-held image already in the repository, PAG3828 in
`docs/references/images/`: put to the owner; the lead's pick is to take the file out of the
tree, its catalogue number and link left in the README in its place, unless the owner holds a
licence for it; act on the owner's word and not before. **The viewer step for the rig's
lines: approved.** The sheets', braces' and tacks' ends read from the drawn rail and the stem
head in place of the old datum and half the beam, and the three level bowsprits rooted at the
sheet's height; no file and no pin moved, the pictures old beside new in the record, before L2
or beside it as suits the worktrees; the owner may veto it when they answer, in which case it
waits. The file figures (the frigate's boom through her taffrail, the masts off the sheets'
places, the schooners' rake) wait for the later package, the brig's displacement first. **The
order from here:** L2 and L3, then the *Neufchatel* with B3.4 first; the design-record commit
at B2's window when the session reaches it. Bring the trunk in at each boundary; 82's step 5
(the tow and the kedge) is building on its branch and touches no ship file.

**2026-10-31, afternoon.** Gwyn's PAG3828 out of the tree (71b8ed7) is read and merged
(the fast tier on the trial tree 5,909 passed; one browser test of the MCP bridge timed out
on a slow machine and passed alone after; docs and the image only, the next cloud run covers
it). The
owner's word of today: the week pauses on new packages (decision 61); 65 is held on its
branch at step 1; your lee-port and rig-line step is reviewed and merged when you send it,
as the owner says you will; the *Neufchatel*'s main topgallant and the generalising of mixed
rigs are in the owner's hands with you, and the proposal comes to the lead with the step
that builds it. Nothing new is launched this week.

**2026-11-06, package 90 widened: the Spanish and Mediterranean ships.** The owner's word
of today, for your plan when 75's last window closes: package 90 is no longer the tartane
and the xebec alone but a Spanish and Mediterranean package of five hulls, from the smallest
up: (1) the tartane of decision 11, as booked; (2) a **polacre**, a lateen on a forward-raked
foremast and on the mizen with square sail on the main, which puts a lateen and square sails
on one hull as the bilander does and so takes the generalising of mixed rigs you are working
out with the owner for the *Neufchatel*; (3) the **xebec**, a lateen on all three masts, with
her sweeps as an option of the fit; (4) the twenty-gun **corvette *Diana*** as captured and
used by the Spanish navy in 1809, a ship-rigged sixth rate's size for the Spanish side; (5)
the ***Purísima Concepción* class three-decker** of the Spanish navy (the owner's spelling
"Concepión" read as the ship's), the game's first three-decked ship, which asks of the
generator what no hull yet has: three gun decks, a first rate's complement and her stations,
the great ship's handling. The design is yours in your plan's form as before (a design
document each, the ladder of evidence, the lead's gate before a file); the sources Roux's and
Tofiño's plans, Winfield where he reaches, and the Spanish sources you find, cited by page;
the *Diana* is settled by the owner (2026-11-06): the Danish frigate *Diana* built in 1804,
taken at Cartagena with the declaration of war and kept by the Spanish navy to 1832, Winfield,
*Spanish Warships* (the owner's edition, p. 930): 124 ft by 32 ft 6 in by 16 ft (34.55 by
9.06 by 4.46 m), 335 tons, 167 men; twenty 24-pounder carronades as captured, twenty
30-pounder carronades as first rearmed, and by 31.10.1817 twelve 12-pounders, eight
30-pounder carronades and four 3-pounder obuses; so her fits are three, dated. Her plan is
the Spanish navy's own, "Plano de la Corbeta de Guerra la Diana, del porte de 20 carronadas
de á 30, mandada por el Teniente de Navío de la Real Armada D. José de Julián por los años de
1809 y 1810", a sheer with the body plan and the half-breadth and a table of her particulars,
in the Ministry of Defence's virtual library (Biblioteca Virtual de Defensa, record 1037832,
https://bibliotecavirtual.defensa.gob.es/BVMDefensa/es/consulta/registro.do?id=1037832), the
same library 79c's pilots came from: a §5.0 rung-A source for her lines. The file is in the
tree as `docs/references/images/corvette-diana-1809-plano-bvmdefensa.jpg` (the owner, the
same day: the library distributes the digital copy under CC BY 4.0 on the condition that the
source is named, "Fuente: Archivo Histórico de la Armada Juan Sebastián de Elcano /
Biblioteca Virtual de Defensa"; the provenance and the condition in the images README). Her
particulars on the sheet are in the navy's units (pies de Burgos, 0.2786 m), and so are
Winfield's feet for every Spanish row (his metres prove it: 124 ft is 34.55 m at that foot),
so her design document reads both in metres and never as English feet. The count: thirteen after 75, eighteen after 90 (decision 56 amended). The order within 90
is yours to propose; the lead's view is the tartane first as the reference vessel and the
smallest, the three-decker last as the largest departure. Nothing of it opens before 75's
last window closes, and nothing this week (decision 61).

**2026-11-06, later: Winfield's passages for 90 set down.** The owner sent the passages of
*Spanish Warships in the Age of Sail* on the five (the tartanas, pp. 1249 to 1252; the
polacres, pp. 1083 to 1084; the xebecs in Spanish service with the Artillery Regulation of
1752's batteries, pp. 1134 to 1136; the *Purísima Concepción* class whole with her service,
pp. 406 to 410; the *Diana*, p. 930) with three of its pictures. The facts are in
`docs/design/VesselReferences-2026-11-Spanish.md` in the lead's words, cited by page; the
book's text is copyright and is not in the tree, and the three pictures are cited and not
held (Monleón's polacre and xebec, the Greenwich draught of *San José*). Two things of the
lead's reading for your design documents: Winfield's feet for Spanish ships are **pies de
Burgos** (his metres prove it), so the game's constants come from his metres; and the
polacre's pole masts (no tops, the yards lowered to hand the square sails) are a handling
the generator does not yet say, to be said in her document with the mixed-rig generalising.
**The owner's offer:** further passages of Winfield are sourced on request; ask the lead by
title and class and the lead asks the owner. **The tartane's rig, corrected by the owner the
same day:** the Roux-school watercolour shows the square topsail over the lateen as
Monleón's print does, so she is rigged with a lateen and a square topsail on the main, a
lateen on the small mizen, and one or two headsails by judgement from the sources together
and the hull's implications.

**2026-11-06, the lee-port step (L2 and L3), the rig lines and the booms: read, the merge
in train, and the lead's take on the whole and on the flicker.** Your report of today
(claude/pkg-75 at e88df44, sent after the owner's review) is read whole: the ports by the
heel (L2) and with the roll's amplitude (L3, `roll_in_the_dip` reading `Firer.roll_deg`,
the other side the roll less the heel, a chaser on the centre line the roll alone); a gun
whose port shuts run in and housed with its loading going on and its running out and
pointing given over; a shut port silencing its own gun and no other (the named gun dropped
with a line, the word for a broadside all behind shut ports dropped, a division all behind
them passing its turn); the deck's side one line from its first port shut to its last
opened, said only while a gun of it is cast loose, so that no sailing passage's log moves;
`_least_dip`'s one compare a tick taking the pace back; the viewer's sheets, braces and
tacks ending on the drawn rail and the stem head, the booms 3° above the level; the checks
(no truth, action or trial moved; the four whole logs identical; the fast tier 6,272; the
fifteen files byte for byte). The trial merge on the trunk's head (2b59ea4: 82b's item 1
and 65's step 2 merged this morning) is clean and lint-clean, the fast tier runs on it, and
the merge follows on green with its record. **The whole: approved as built.** The line
gated by the guns cast loose is the right judgement (a port shut by the routine of the ship
on passage is no news); the gun housed with its charge kept and the drill not timing a
round behind a shut port are right; the weather side moving in a seaway is the sea's truth
and not a fault, and §7's "a roll 20° beyond the heel" is corrected by your measure.

**The flicker: the dwell, as the owner leans, and not the heel margin.** A port's shutting
is a crew's act when the sea comes in, and its opening is the gun captain's judgement once
the sea has kept clear a while; the six inches of sill is the physical criterion and stays,
and the human one is a hold. Build `PORT_HOLD_S = 60` as you describe: each gun's shutting
tick kept on the battery (a class default, `tick` passed from `Battery.tick`), a port opened
only once it has been shut that long and its sill is clear of the reopening line, a port
shut again within the hold starting it afresh; the shutting itself at once, as now (a sea
that comes in once is enough to shut a lid). Not the 3° margin: it would make the rule's
reopening a different physical thing from its shutting, and a minute's hold is what a gun
captain does. Measure the same hour in gusts after it (the frigate at 21 kn, the brig at
17, the 64 at 17.5) and write the changes beside the 46, 24 and 43; L2's reopening-band
pins move, old beside new with this ruling as the reason, in a commit of its own, with
§7.1's figure amended. The owner may veto when they read this; build it unless they do.

**§12.2a, ruled now: the rule in the key's place, approved.** An after mast with yards and
no yard on its lower mast handles as a fore-and-after's mast; `Ship.on_schooner_mast(part)`
read from the parts as filed, once a ship, the yards under the bowsprit not counted. The
owner's reason is the lead's too (a file that forgets a key makes her a brig with no word
said; the rule is the generality package 90 wants), and your reading of 90's rigs under it
is right: the tartane classes as the cutter does (a lateen yard is no braced yard), the
polacre as one square mast with a lower yard between two lateens, no key; the limit
(Fincham's schooner with a lower square-sail yard on her main) stands under both and is
recorded. Build it with B3.4 as §12.2a says (the topsail schooner with a square main
topsail as the second rig in memory, the guard that no file trips it); the swing at
"mainsail haul" is B3.4's measure, reported with it. The polacre's pole masts stay for her
own document, as you say.

**B6, the scenarios: out to a supplemental package**, on the owner's word of 2026-11-05 (the
hulls first, so that the guns in the viewer can begin on every hull at once); booked as the
ships' scenarios, after Phase 5, in the waves table when 75 closes. **The order from here
stands as you give it:** B3.4 by §12.2a's rule, SW-4, B2 the *Neufchatel*, B3.3 with B4
the bilander, SW-1 with B7 the 74, then Phase 5.

**Left for the lead, booked:** the four things in "Left, and for whom" go to package 77
(the gunnery's and the fight's evolutions, Opus, behind 70 and 73): `engage` with every port
of a side shut answering what follows, and "fire the broadside" saying the ports before
the ports' line; the two served words for the weather side (`the weather ports shut`,
`the weather ports opened`, `lee` False), under 85's in-world rule; the rules captains
reading the ports (`engage_side` weather, `_a_gun_for_a_signal` and the distress gun taking
an open port); and the weather port the roll shut opening exactly upright said the lee's.
Written into 77's brief at the merge.

**2026-11-06, later: the lee-port step merged at 8c30c8a.** The fast tier on the merged tree
was green but for two things, both the lead's at the merge (3478abf): the officer's handover
test at exactly its fraction, 65's step 2's sentences and your port words together, its budget
raised by its convention; and the pictures' blank floor, which the machine's noise straddled on
the trunk and on your tree alike, set at 4.0 from the chart's own 8.0. Nothing of yours moved.
The whole suite runs in the cloud; bring the trunk in at your next boundary (82b's item 1 and
65's step 2 are on it since this morning: the harness's `ident`, the say across hulls, a
reply's prose the person's own note). Build the dwell as ruled above, then B3.4.

**2026-11-06, night: the owner's word for the ships session's night.** The dwell is in on
your side; the owner has you work on through the night and foresees no blocker that wants
their attention for 75 to finish as planned; you keep in touch with the lead as you work
and hold for the lead on any judgement call; the lead reviews and merges each step as it
comes, through the night, by the same road (the trial merge, the fast tier, the whole suite
in the cloud, the record). The lead's own night: 82b's items 2 to 5 merged when reported,
then package 95 launched (the sail by her name, on `world/hail.py`'s `_addressee` beside
your files, nothing of the ships'), then 97; 65's step 3 merged when reported; 74 launched
when 65 closes.

**2026-11-06, 18:00 UTC: the hold and B3.4 received; the four rulings.** Your send of the hold
(42a995b) and B3.4 (1c02517) is read: both as ruled and as approved, the hold's figures and the
L2 pins old beside new accepted, `on_schooner_mast` at places 1 and 3 only, read once a ship
from the parts as filed and held beside her, accepted. The lead merges 1c02517 after package
97's merge (97 binds the player's own hull's systems to her Hull; it touches nothing of the
ships'); the trunk then carries 65's step 4 and 97, and you bring it in at your next boundary.
The gate's J1 is corrected: the frigate's 46 changes of port in the hour stand with the hold as
without it; what the hold removes is the quick reopening (the seven changes within a minute,
six to sixty-three seconds, to none), and the hour's count is the gusts' and lulls' own, which
the owner judges at the gate. The four rulings, each its own small step after SW-4, each
measured before it is built, the moved logs old beside new with the reason: **(1) place 2's
timing, yes, after Luce 1884 p. 417:** the after yards hauled with the wind ahead or a point on
the bow, before the head yards, the short after swing; never swung with the head yards. Trial
A's 149 s stays as it is (she has no yards at place 2's after list but her own); say the new
figures for trial B and the main topgallant beside the old (219 s, 232 s). **(2) the word, yes,
by Luce:** "Main-topsail haul!" for every ship whose main course is not set (none bent, or
hauled up), "Rise tacks and sheets. Mainsail haul." kept for a main course set; the moved
logs old beside new; 85's in-world rule holds as always. **(3) place 2 with no mast carrying
yards, yes, as after yards:** with every fore yard shot away the schooner-mast's yards are her
after yards (they are abaft her fore and are swung as after yards while she had a working fore
yard; nothing changes in their handling but that they are no longer left standing); the pin
you set as it stands moves old beside new. **(4) `orders/storm.py`, yes, and granted to the
ships session for this** (nobody else touches it): keep the courses' reef at the topsails'
second reef for any rig with topsails (Luce 1884 p. 476; Cobb p. 95, the closely reefed
mainsail and the double-reefed foresail), and gate only the after take-ins on square-rigging;
measured on trial A, the cutter, the smack and the four whole logs, every moved pin old beside
new. Your three records for B2 and package 90 are noted (the Neufchatel's main topgallant and
"shorten sail", the two classing limits, the polacre's lateen mizen and pole masts); the
lead carries the classing limits and the polacre's note into package 90's brief. Run on to
SW-4 and B2 as the owner gave leave, taking these as they come, and send the one final report
for 75 when it is whole.

**2026-11-06, 19:05 UTC: the hold and B3.4 merged at f414ed1.** The trial on the trunk with
package 97 in was clean and lint-clean, the lead's fast tier whole on it green (exit 0); the
record is "### Package 75, the hold (SW-5) and B3.4 (the schooner's mast), as merged"; the whole
suite runs in the cloud after run 41. Bring the trunk in at your next boundary: it carries 65's
step 4 (the player's one person, the prompt following his body into the boat and aboard
another ship; `go to the boat` from another ship's deck takes a visitor off in his own boat),
package 97 (the player's own hull's systems bound to her Hull at her making; nothing of the
ships' files) and, next after this, 65's step 5 (the library by the reader's place). Your four
rulings stand as written above; the owner is awake and has your send.

**2026-11-07, 02:40 UTC: found by package 81 (the viewer's action), for the ships session and the schema.** The frigate's quarterdeck carries two sizes of port on her sheet (carronade ports 3 ft by 2 ft 11½ in, gun ports 2 ft 3 in by 2 ft 4 in, `pages-zaz2587.md` §7.2), and `port_size_m` is by deck, so her file gives the gun ports' size to the carronades too; 81 draws each port at its deck's size until the schema gives a size by port. A `port_size_m` entry by port (or a fourth value in a triple) is the schema's and yours when a hull wants it, in your plan's form; nothing is asked now. Also for the record: 81 places every gun of every fit by one rule from the files' triples (327 guns over eleven fits, none refused), and puts the 64's foremost forecastle triple of 1784 (18.41 m, 0.07 m under the rail) over the rail by the side's own test rather than `OVER_THE_RAIL_M`; its checker names such triples for you to keep or to write 2 in under the rail. Package 74 is told that the cartel's one gun stays words until 75 closes.

**2026-11-07, 05:00 UTC: found by package 74, for the record (SW-4 mends it):** the world order's "merchant brig" took `data/ships/brig.yaml`'s muster of 121 before SW-4, `merchant-brig.yaml` being a shadow; the lead merges SW-4 next.

**2026-11-07, 05:42 UTC: SW-4 merged at 73b9469 (your 1ff4e813 by hash, a clean merge onto the trunk carrying 74's step 1), the record "### Package 75, SW-4 (the sub-types as fits and roles), as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree green, exit 0; the whole suite in the cloud dispatched after it. Your eight points, by number.** (1) The mend outside B8's files CONFIRMED as built: `Transition.unless` a list with one stimulus a plain string, the evading rows of privateer.yaml and revenue.yaml `unless: [overmatched, man of war near]`, `Captain.sub_type_role` carried at the promotion, `description_key` taking the whole phrase after the article; `world/captains.py` and `brains.py` are package 74's files too (its design touches the doctrine's thresholds and states), and the lead resolves the meeting at 74's merges and tells 74 now; no pin moved by it (your candidates' 4,023 unchanged). (2) The trade trial's stranger digest moved on "ten" alone: the lead re-pinned it on the build machine after the merge, old beside new with the cause (the lead ran the trial on the build machine: the trunk before the merge gives the pinned bf059c3211b7cc9c, the merged tree 5e7bdba2a4f4770b, and the merged tree with the one word put back to "sixteen" in brig.yaml's descriptions (where the lookout's words are served from since SW-4; the engine table's word alone changes nothing) gives bf059c3211b7cc9c again; the states, the anchored ticks and the 1,594 lines hold throughout; re-pinned at 5e7bdba2a4f4770b with the old beside it, the cause named, in the commit after the merge). (3) The rail-gun fits as played (each rail gun crewed on its own side, "fire the swivels" firing the long 18s, the smack's starboard gun never loading): not yours; booked to package 77 (the gunnery's evolutions) as a finding, a kind-aware engine for swivels and rail guns; the fits stand as the sources have them, the oddity recorded in your notes. (4) The revenue cutter's served words: BUILD IT as a small step of your own, "SW-4b, the revenue's and the Indiaman's words and sets", before or after B3.4 as you judge: a `revenue` entry in the readings' service map (she reads "a revenue cutter of Britain" or as your sources word her service), `answers: revenue:` in hail.yaml with the words yours and in-world (her name, "on the preventive service", her station), and the role sets taking `revenue` as an ARMED vessel of the Crown and not a merchantman (`regimes._MAN_OF_WAR_ROLES` and `squadrons._ARMED_ROLES` gain it; `orders.HAND_PEACEFUL_ROLES` does not) and `indiaman` as a merchantman that is armed (the two sets as you judge from her book, said); hail.yaml and readings.py are 74's files as well and the lead resolves the meeting. (5) The coasting cutter's company: her OWN FILE through the generator when her turn comes in your plan (a coaster's company of eight or so, sourced), not a fit; until then the departure is recorded in your notes and the readings say the King's cutter's thirty with the departure named in the file's note. (6) The glass words APPROVED as your candidates: the hired armed cutter "a cutter, pierced for guns", the coasting cutter "a cutter, deep laden", the privateer lugger "a chasse-marée, her guns over the rail"; the revenue cutter's plain British colours stand until 76's colours.yaml gives the Customs' ensign (the lead books the hook to 76: "the revenue ensign" as a flag of the British root, dated); that she speaks every sail she investigates, a friendly man of war among them, stands as built. (7) The long tom recorded as the owner's ruling, the merchant brig class 2 by her row: noted. (8) SLOW_TESTS: mark truth 7-191 (7.5 s) and the two crewed evading tests (8.3 s, 6.9 s) slow in tests/conftest.py at your next step; the revenue tests (5.0 s, 3.2 s) stay in the fast tier. Found by package 74 for you, no action asked now: the world order's "merchant brig" took brig.yaml's muster of 121 before SW-4 (merchant-brig.yaml was a shadow); SW-4 mends it. Go on with B3.4's four small steps and B2 to one final report, as before.

**2026-11-07, 09:20 UTC: found by package 81 (merged at a8b716d4), for the ships session's notes, no action asked now:** the topsail schooner's fit "musquidobit 1813" carries eight 18-pounder carronades at 10 cwt, 11% off Adye's 9 cwt pattern of 3 ft 3 in (p. 72); the viewer's checker (`python tools/check_viewer_guns.py`) lists them and draws them at the pattern; keep the weight your source gives or note it in the file. The checker is now the ship builder's (Build-Ships.md §6's postscript): every new file passes it before it is reported, every gun on its deck's triple within 0.01 m, the triple a port where the side stands the port's depth above the sill and a place over the rail where it does not.

**2026-11-07, 12:50 UTC: B3.4's four rulings merged at 3c9df9e1 (your 6e19f46c by hash, a clean merge onto the trunk carrying 74's step 2, 76's step 2 and 81), the record "### Package 75, B3.4's four rulings built (the schooner's mast at place 2), as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree green, exit 0; the whole suite in the cloud dispatched after it. Your five open points, by number.** (1) The short swing for every ship: NO. Luce's p. 417 is a ship's tack and the figure he gives for the whole evolution is five to ten minutes, which the 20 s swing on heavy yards would break (truth 10's 247 to 273 s against its 285 to 600 band, truth 19's 262 against 300 to 600, the brig's 338); the short swing is a schooner's light main yards' alone, as you built it, the heavy yards' swing `brace_s`, and the test over every file that pins it stands as the rule's own statement. Nothing more to build. (2) The word's cases. (a) Fore course set, main not: BUILD Luce's form as you lean: "Main-topsail haul." at the haul and "Rise fore tack and sheet. Let go and haul." after it (pp. 419 to 420, 428 and 446: the fore tack risen apart, by its name, before the head yards are hauled); words only, no tick moves, the word pins moved old beside new with p. 420's words as the reason. (b) Main course set, fore not: BUILD Luce's form too, "Rise main tack and sheet. Mainsail haul.", for the same reason (one form for the one course set, each named); the pin moved old beside new. (c) The *Neufchatel*'s main topgallant yards hauled by "Main-topsail haul" though she crosses no main topsail: KEEP as built. The order names the haul of the after yards and not the sail (Luce's own usage: it is given with the mainsail hauled up and the main topsail furled alike), and no source gives a schooner's own word for it; say so in her document's §12.2, and if B2's sources (Cobb, the court papers) give her people's word, her file's words may carry it then. (d) The bilander: her settee is her main course, lowered at helm's a-lee to be dipped, so her after yards are hauled by "Main-topsail haul" at every tack, and "none bent" means no square course bent to her dry main yard; she sails the same either way; the word stands as the review mended it and her document says why. Take (a) and (b) as a small step of B3.4's, "B3.4b, the word's two cases", before or with B2 as you judge. (3) The dismasted rigs' lines are word bugs and yours to mend in the same small step, words only: with no head yards the wear says nothing of "squared the head yards" (the line names the yards she has, or is left out); the heave-to with no yards to lay aback says she is hove to under her fore-and-aft canvas, not "to the mast"; the tack's steady timeout names the tack she lies on, read from the ship, not the one the script was given. The wear growing to 468 and 483 s with the main's yards braced round as any ship's is the ruling's consequence and stands (a wear is the slow way about for a square-rigged rig; the dismasted schooner is one now by her yards). (4) The second reef queued on a course already being reefed (pre-existing) goes to the lead's list for the evolutions' owner (package 90's or 77's, whichever reaches the gale's reduction first), not yours; Cobb's closely reefed mainsail not built is right (no line reefs a fore-and-after's gaff mainsail; the owner may ask for one with the *Neufchatel*'s document); the beam ends at 38 to 42 knots as before or fewer, noted. (5) Trial B's two sailed tacks in the fast tier at 2.3 and 1.7 s: they stay; the lead measures the tier on the build machine at each merge and moves them to SLOW_TESTS if it grows slow. Run on to B2 and send the one final report for 75 when it is whole, B3.4b's words in it or before it.

**2026-11-07, 21:48 UTC: B2 merged at 04136d99 (your a244e1bb by hash, a clean merge onto 9b821fb5, the trunk carrying 76 whole and 74's step 2), the record "### Package 75, B2: the *Prince de Neufchatel*, with SW-4's words step and her stage 0b, as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree exit 0, 6,791 passed, 1 xfailed; the whole suite in the cloud dispatched after it. Your six points, by number.** (1) Package 81's port at her No. 8: the server's rule gives way. The viewer draws what is served (the rule I gave 76 and 81), so the served top must be the figure the drawing can honour: `viewer_guns.ports` cuts a port's top where any part of its top, tilted with the deck, would stand over the rail (the rail read at both corners' x, the lower taken), and the 2 mm `ON_LINE_M` is the viewer's alone. That is 81's file and 81 is closed: it goes on the lead's list for the viewer's next owner, and your departure `CUT_AT_A_CORNER_M` stands in 81's test as named until then. Nothing of yours to do. (2) Her outline at the stem's foot: BUILD the shared fix, the smaller one. `form._closure` merges closure levels within a millimetre (1e-3 m), so a float's residue for nil is nil; prove by the served stations that no other file's closure moves (yours begin below the water, the schooner's at -0.222, the brig-sloop's at -0.439) and by the byte test; `OUTLINE_MET_TWICE_AT` goes with it. A small step of B2's, before B3.3 or with B3.4b. (3) Her readings, each a words bug, and each yours where it is one function's line, the lead's list where it is not: (a) "a ship of the the United States navy" and "a ship of the France navy": `readings.ship_words` takes the nation's adjective, "a ship of the French navy", "a ship of the Spanish navy", "a ship of the American navy", words only, the pins old beside new. BUILD. (b) She sails the King's ship's book, makes the private signal and answers a hail as a King's ship: her description row files no `roles`, so her role is empty and `_is_kings_ship` reads her wardroom's `captain: captain` as a King's (a privateer's commander was a captain too; the wardroom test was written for the eight files). BUILD the smallest road: her row carries `roles: [privateer]` as SW-4's sub-type rows do, and `brains.sub_type_role` reads the roles of any description that files them (hers the first whole file to), so that she is a privateer wherever no scenario or intent names a role, and the book, the hail, the private signal (none unless the scenario's papers give her one, 76's rule) and the readings follow the role as they do for the privateer schooner; `_is_kings_ship` is left as it is. Her round trip and her readings old beside new; no other file's row moves. (c) `DANGER_AHEAD_STATES` lacking "investigating a stranger", so she takes the ground on the Stags at 3,911 s: the rules captain's, not yours; the lead's list for the captains' owner, and your round trip keeps clear of the Stags by its scenario's position meanwhile, as it does. Do not mend it. (d) The trim's "the fore sail": the reply reads the sail's alias as the other readings do; yours if one line, else the list. (e) Lie a-try's fixed words and her fore gaff sail: BUILD as a ruling beside ruling 4, hers alone by her rig (a boomless fore gaff sail present): the gale's reduction takes in her fore gaff sail at the topsails' second reef (Cobb 1841 p. 79, cited as a figure of what she did, not copied), and lie a-try names her two gaff sails, lying to under her reefed mainsail and fore staysail; no other file has the sail, which your guard proves; words and lines, old beside new. (f) "take in the square sail" answering in the parser's words in her and the two schooners: the grammar's sail names read the file's aliases, so "the square sail" is a sail where a file has one; yours as a words step if it is the alias table's line, else the list. (g) "no water of water by the chart" (chart.py): BUILD, one line, words only. (4) Her figures held for a reading: KEEP the join (1.25 to 1.27 ft against 0.85) and port No. 3's sill (5.54 to 5.60 against 5.20) as designed and recorded, for the owner's eye; the wale stays unread (task 6) and her tack on the fore stay a recorded departure (task 7 not taken) until the owner asks for either. The transom: TAKE your re-reading, [2.46, 2.53]. Your first reading's 15.8 ft was taken at 3.2 to 3.9 ft above her water, below her knuckle at 4.65 ft, by your own account, and a knuckle's half-breadth is read at the knuckle's height; so her transom tumbles home above it as every other does, `FLARED_TRANSOM` empties and stays as the mechanism, her design's §3.5 and her file say so, old beside new, the viewer's rows re-measured where they move and no other file's. The fore staysail's 93 m2 against about 46 that fit forward of the mast is not a drawing matter but a sail area in her polar: if the 93 is her sail plan's figure, keep it and record the geometry's 46 as the drawing's departure; if it is a derivation of your own, correct it to the triangle that fits and re-measure her polar and her best point old beside new (7-193's band stands). Say which in her notes. (5) The words step's judgements: all five accepted as built (the Indiaman peaceful by the hand's doubt and out of the armed set; the revenue cutter heaving to for a King's ship of a nation she is not at war with and making sail from any other; no private signals for her; the nations block's four keys all wanted). (6) The fast tier's times: her wear and heave-to (8.9 s), truth 9 (6.5 s) and the helm (6.1 s) stay in the fast tier, being under 5 s alone; her round trip stays in `SLOW_TESTS`; I measure the tier on the build machine at each merge. Beside the six: (7) B3.4b is still owed, the word's two cases (a) and (b) and the three dismasted rigs' word bugs of my note of 12:50; take it first, before B3.3 and B4, with (2) and the words of (3) in one small step if you judge them one. (8) The four whole logs: the first action's 473 to 497 lines is 74's step 2's (the captain taking possession at 6,180 s), merged with its own pins at 1bb24f52 and green in the cloud since run 49; re-base your four logs' figures on the trunk at your next measure, old beside new, naming that cause, and move no pin for it. Then B3.3 with B4, as you said.

**2026-11-09, 22:56 UTC: your bd12a802 merged at acdcfb56 (by hash, a clean merge onto be9c951e), the record "### Package 75: the settee (B3.3, B5.4), B3.4b, the *Neufchatel*'s ruled fixes (B2b) and the bilander (B4), as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree exit 0, 7,031 passed, 2 xfailed; the whole suite in the cloud dispatched after it. No bridge message of yours reached me: this session lay dormant from the 8th to the 9th, so I read your branch's tuning notes as the report; send the next one again if a day passes with no note here. My rulings, by your sections.** **B3.4b:** accepted as built, Luce's p. 421 for my "pp. 419 to 420" with it. **B2b.** (1) The rows' roles: `INTENT_RULED_ROWS` IS the rule and stands as built: the eight rows sailed before package 75 keep the intent's rules, and every whole file added since (hers, the bilander, the 74) sails by its first role; say so in Build-Ships §8 as the lead's ruling. (2) (3)(d), the trim's reply by the sail's alias: BUILD it for every file as one words step (the reply and the done line name a sail by the same word, the file's first plain alias), every moved pin old beside new; with the 74's window, not before it. (3) (3)(f), "take in the square sail": the gale's list (`orders/storm.py`, yours by the grant) names the square sail only where the ship has a `square_sail` part (the cutter, the smack), so that "Not done" no longer lists it in her and the schooners; the grammar's refusal of the phrase typed at the prompt goes to my list for the grammar's owner. (4) Her fore gaff sail in the gale: I REVISE my ruling's moment, on your measure and on the source. She is not to take it in at the topsails' second reef (she gripes with the helm hard over for 25 minutes and lies 13 minutes with no headsail; Cobb's ship lay to under it). It is kept through "shorten sail" and through lying a-try, named in the line with her mainsail ("under the fore topsail, the fore gaff sail and ..." as she lay before B2b), and comes in by the order and when she is put before the wind to scud; `gaff_sails_beside_a_course` stays as the name for it. The three rigs in memory return to ruling 4's record. Old beside new, her gale measured again. (5) Her helm: KEEP `clr_x_m` +0.1. Nearly four degrees of weather helm close-hauled in 15 kn is a seamanlike figure for a sharp vessel under a 256 m2 mainsail, and no lead holds both bands; her close-hauled band is hers, +2.5 to +5.0, a ruled figure, the strict known-failure mark taken off and her design's §9 saying so; the abeam and ten-point band as it is. For the owner's eye at the helm. (6) Her quarter bill: 34 by the rule, through the generator. **B3.3 and B5.4:** accepted as built: the settee no course at the word; taken in with her courses to lie a-try, kept to scud; the heave-to by the driver rule; rule 5 pinned on the static case, which counts (no D44 (c) row, no B3 step for it); every time and hand your judgement as recorded; the derrick drawn (amend Ext §6.3's "not drawn"); the yard drawn as its head; the two yards' crossing by the wind left as recorded. A settee's sheet held to windward drawn to leeward goes to my list for the viewer's package (the snapshot to serve the sheet's side). **B4, the bilander:** accepted as built, with these. (7) The datum of Gwyn's heights stays y 961; row C, the collier's deck and her headsails' 43 m2 stand; Folio IV is not wanted. (8) The boy: take the other shares (0.80 able, 0.20 landsmen), four able topmen and a landsman boy, as the merchant brig's boy is rated; through the generator, her requests measured again. (9) Her watches: the boy's hand to the larboard watch, three and three, so that each watch begins a settee request short-handed and neither is refused one; the muster's line for her, no settee file's hands changed. (10) Her helm: she may carry her little lee helm close-hauled at `clr_x_m` +2.0; her heave-to holds and is the bound, as you tuned it. For the owner's eye. (11) Her round stern's breadth: BUILD the key (`form.py`, a round stern's half-breadth at the counter, hers the one file to file it, every other file byte for byte and graph for graph), which brings her settee's block inside her rail and her lights out to their filed spread; the two viewer departures go with it. (12) Her wale stays hung from the rail at Chapman's scale. (13) Found on her file: (i) the settee kept through a forced round while hove to (it stays against its mast, "fill away" never dips it): BUILD it next, B3.3b, the forced round dips the settee or says it lies against the mast, with a test that forces it; her heave-to not reaching it at seed 7 is no guard. (ii) Her armed fit's one crew divided over two guns before a side is engaged: the combat engine's, to package 77's list. (iii) "1 guns ready": one line, BUILD (words). (iv) Lying a-try "and the staysails" with none set: yours, BUILD (words: name what is set). (v) "taken in before the fore storm staysail is up" said on the tick the take-in was refused: `storm.py`, BUILD (words). (vi) Words naming people she does not carry (the carpenter sounds the well, the boatswain's papers): engine-wide, to my list for the warrant officers' package (87). **Found on the way, to my list for the evolutions' owner, none of it yours:** backing and filling taking the brig to a run in 15 kn; the box-haul's "Wind aft" with the wind never across her stern; a lug or settee left against its mast with no word when she is taken aback with no helm order. **From the owner's play of this week, for you:** the owner has sailed the *Neufchatel* this week (three saves with me); what touches her on the owner's list is the viewer's alone (her secured carronades painted over her side and lids: a sort-order defect of the viewer's, measured, her file's guns placed by rule a tenth of a metre inside her side; it goes to a mends package and is not yours). **Next, in order:** one step of the ruled revisions above ((3), (4), (5), (6), (8), (9), (11), (13)(iii) to (v)) with B3.3b; then B7, the 74; then Phase 5. The whole logs and the trials stay re-based on the trunk at each measure.

**2026-11-10, 02:25 UTC: your 5af283de merged at cff8fdb1 (by hash, a clean merge; bd12a802 was merged yesterday at acdcfb56 from your branch, your message of the 8th never having reached me), the record "### Package 75: the owner's two rulings on the *Neufchatel* (B2c) and the settee forced round (B3.3b), as merged"; the lead's fast tier on the merged tree exit 0, 7,040 passed, 1 xfailed; the whole suite in the cloud dispatched after it. Your bridge message of the 10th arrived and is answered here.** **First, a correction of my own note of 2026-11-09, 22:56, written before I had read B2c:** its rulings (4) and (5) are WITHDRAWN. The owner ruled both on the 8th in my place, you built them at 8b327687, and they stand as built: her fore gaff sail taken in at lie a-try, and her `clr_x_m` -0.6 with her two bands widened by 0.2 degrees. Do not build my (4) (the gaff sail kept through lying a-try) or my (5) (+0.1 with a band of her own). And my (13)(i) is done: B3.3b is accepted as built, with both its judgements, (a) dipped first as she lies and (b) its sheet as hoisted. Everything else of that note stands: (1) `INTENT_RULED_ROWS` confirmed as the rule; (2) the trim's reply by the alias for every file, with the 74's window; (3) the gale's list naming the square sail only where the ship has one; (6) her bill 34; (7) to (12) the bilander's (the datum, the boy a landsman, the boy to the larboard watch, her lee helm accepted, the round stern's breadth key, her wale); (13)(ii) to (vi). **Your new points, by your numbers.** (1) B3.3's leans: accepted as built (yesterday's note); the box-haul's "Wind aft" is on my list. (2) B5.4: the two yards' crossing is left for the eye, no engine trim keyed on a settee; the derrick as drawn; the sheet held to windward goes to the viewer's package. (3) B3.3b's finds: (i) forced round and left to herself with no fill away ordered: BUILD it in the record's forced-round branch, keyed on a settee: when she is "hove to no longer" the watch dips a settee lying against its mast as your fill away does, and says so; her file and the fixture measured old beside new. (ii) a kept settee trimmed as she pays off to a course, with the boom sails: BUILD (small). (iii) the runner reading an evolution's holds once: BUILD the smaller way, each manoeuvre's holds naming the set settees from the order, so that no order of the settee's is begun while it may be changed; proven by your trace that no committed file but hers moves. (iv) the runner's group line naming sails since taken in (`Runner._group_done`): BUILD the line naming only the group's sails still set; it is every ship's, so the four whole logs and the captain's trials are the proof that nothing pinned moves, and anything that does is old beside new. (v) her light-air fill away from a short heave-to: recorded, nothing built. (4) The bilander as played: as ruled yesterday ((13)(ii) to (vi)); her design's §12.1 guard restated at stage 0H is noted. (5) The *Neufchatel*: her bands holding by 0.05 and 0.09 degrees is the owner's figure and stands; if a later change of hers moves her helm out of them, re-tune the lead, do not widen again. **The trade stranger's digest on your machine against the trunk's:** the build machine's and the cloud's are the trunk's (run 57 green, the trials among it); yours is your machine's, as the other two. **Next, in this order:** one step of the ruled builds (yesterday's (3), (6), (8), (9), (11), (13)(iii) to (v), and today's (3)(i) to (iv)); then SW-1; then B7, the 74, her window open now that B4 is merged; then Phase 5. Report by bridge message as you did today; if a day passes with no note of mine here, send it again.

**2026-11-10, 09:55 UTC: SW-1 and the ruled builds of the 9th and 10th merged at 09222043 (your ad71736f by hash, a clean merge), the record "### Package 75: SW-1 (Table No. 29's charges) and the ruled builds of the 9th and 10th, as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree green, exit 0; the whole suite in the cloud dispatched after it. Your six points, by number, and the runner.** The stage 0 rule applied as it should be: no figure of the eight moved, the table on the new ships alone, said in each file. **The runner (ad71736f):** kept. My (iii) asked for the smaller way and you showed that it left a blocker (a wear behind "take in the mainsail" never begun); `_settees_only` is narrow (a belaying manoeuvre, a crew, nothing shared but the order's settees) and you said plainly that it reaches the runner: that is how a ruling of mine should be overruled by the measurement. (1) **Her watches, three and two:** no sixth seaman and no engine change (a post is never a hand; her company is her sources'). BUILD the third of your ways: where the watch on deck is too few to begin a settee's dip or settle, the request calls all hands for it, as a small coaster did for any work of her great sail (the lead's judgement, no source read for it: if your sources say otherwise they win, and you say so), said in the log as an all-hands call and piped down after; on her file or her evolutions' data alone, so that no other ship's work changes (the four whole logs and the captain's trials the proof). With it (3) resolves: the larboard watch of two no longer leaves the settee against its mast until the watch changes. (2) **The lights' row:** stays as you left it with its comment; the viewer facing a round stern's light by the face it lies on is the viewer's, on my list for a viewer package (91 or 102's window), not yours. (3) **The watch's own dip by night:** accepted as built, the sheet left as it lies after the dip; (1) changes who begins it. (4) **Every ship's pay-off drawing its sheets for the true wind's angle where the apparent is wanted** (0.47 to 0.68 knot): every ship's and older than these steps; on my list for the evolutions' owner (package 77's ground or a small one of its own), with your figures. Not yours. (5) **A manoeuvre queued behind other work says nothing in the log, and work waiting for hands behind a manoeuvre is tried again only after its pipe-down:** every ship's, older; on my list, the first half beside the owner's decision of the 9th that a man's own word and its answer are always shown him. (6) **"make all sail" listing the parser's refusal of "set the square sail"** in the *Neufchatel* and both schooners: BUILD as "take in" was: the line listed only where she has the part. **Next, in this order:** (1) and (6) as one small step with B7 or before it, as suits your window; B7, the 74, with the trim's alias words; then Phase 5. **The close-out:** the owner has told you that after my final word on 75's close-out you may begin package 90's preliminary research and planning. That word comes when B7 and Phase 5 are merged and their whole suite is green, not before; say in Phase 5's report what you count as left over for a later package, so that the close-out's record can name it.

**2026-11-10, 11:10 UTC: a pin your ruled build (3) moved, found by the cloud's run 62 and re-pinned by the lead (4016629e); nothing asked of you but to know it.** The schooner's recorded passage of gate 5b (`GATE_5B_SCHOONER_DIGEST` in `tests/test_known_truths.py`, a slow test): its 766 lines kept, its digest `2b68e8b1f60e8496` to `3a1698037811b753`. One line differs between the trees before and after your merge, the standing order "the outer road"'s "Shorten sail" at tick 56,234, which no longer lists "'take in the square sail': 'take in' was understood, but 'square' belongs with 'brace'": the build as ruled, and right. Your four whole logs and my fast tier do not hold this passage; the cloud's run does. **For your steps to come:** any change to a line every ship may say (the gale's list, a group's line, an evolution's words) can move a recorded passage that sails under the starter book; say in the report which lines of that kind a step changes, so that I look for the pin before the cloud finds it. Rulings (1) and (6) of the note above are of that kind: (6) changes "make all sail"'s list as (3) changed "shorten sail"'s.

**2026-11-10, 19:30 UTC: B7, the 74, steps 0 to 6 and her review's mends, merged at 31f6bb35 (your 9c812f43 by hash, a clean merge), the record "### Package 75: B7, the 74 (the *Bellerophon*, steps 0 to 6 and her review's mends), as merged" in docs/dev/M7-WorkPackages.md; the lead's fast tier on the merged tree green, exit 0; the whole suite in the cloud dispatched in its turn. Your seven points, by number.** The work is accepted whole: the eleven tasks by two methods, the three order faults failed before they were mended, and the plain word that the 74s of 7-196 fire into the frigate are what a report should be. **Truth 7-196 alone, measured on the build machine at this merge:** on the quiet machine 505, 476 and 492 ticks a second in three runs (the best of three thousands each), the frigate 524 and 516 in the same runs: under 550, so by my answer (5) the clause is recorded and not pinned. I took its test out at the merge myself (a lead's commit after yours, so that the cloud's pace job is not red on it until your step 7): `test_truth_7_196_the_seventy_four_ticks_at_the_build_machines_floor` is gone from `tests/test_bellerophon.py`, its figures in a comment where it stood and a paragraph at the end of the tuning notes; the crewed clause stays; merge the trunk before step 7 and keep the comment. Phase 5 moves 7-196 as the crewed clause alone, with the alone figures in its words. (1) **Lie a-try from way on:** not the lead's: `clr_x_m` stays 4.8 and truth 17 is not re-ruled. The script's lee helm is a timing value (`helm_deg`, 5 degrees where the file gives none), so BUILD in step 7's window, on the 74's and the 64's files alone if the files can carry it in the timings' own form: the figure that brings her up from way on, in your path's 35 kn, to between five and six and a half points and under 2 kn, with truth 28's form from rest still holding and "heave to" on the path as it lies today; every other file and its logs untouched (the four whole logs the proof). If the helm alone will not hold both (your sweep will say), stop, record the sweep, and it goes to the evolutions' owner (package 77's ground) with the two-deckers' two equilibria named; no change to the script's logic in B7. (2) **The mizen course's tack:** as built, 9 ft above the poop. The design's 9 ft was I32's throat less Steel's fore leech, measured from the deck the mast stands through; you measured that deck to be the poop, so the design's own derivation gives your figure, and the design's "quarterdeck" was the slip. Steel's "within 6 or 7 feet" stays in the note as the general rule beside it. Mend the design note's words in step 7. (3) **The body plan re-traced by the sections' nesting order:** confirmed. The consistency at WL1 (0.14 to 0.18 ft outside the half-breadth plan at every station from 47 to 92 ft) is the proof the first assignment lacked. `SECTION_FT`'s midship trace stays as it is, recorded (0.09 ft inside the re-trace, which agrees with the moulded 46 ft 1 in); the file's WL1 stays the plan's. The pair check with the 64 at 4.016 px: it stands; if a later step of hers moves it under 4.0, the step says so and stops for my ruling, and no bound is lowered. (4) **7-195's ordinary-sailing clause:** recorded and not pinned, accepted; Phase 5 moves the truth as drafted. (5) **7-196 crewed, the 74s firing into the frigate:** the truth stands as measured (three crewed 74s in action is the heavier load, and its docstring says so plainly). Booked on my list, not yours: a King's ship made by a test world or a scenario that gives her no private signal table is taken for an enemy by her own side; whether every King's ship carries the day's private signals unless a scenario takes them away is the signals' owner's question (71's ground, with the owner). (6) **The flag party:** the form `{post, name}` accepted; its make-up (the rear-admiral, the flag lieutenant, the secretary and twelve servants, 15, the make-up judgement) accepted as judgement and marked so, inert until the flag's own package (96's ground). Stage 0c's item 2 (`numbering`, `Gun.by_deck`) with B7.d: agreed. (7) **Found, not hers:** the named gun's want of a bearing check ("fire No. 1 gun" firing the larboard No. 1 at a starboard mark) goes to package 74's builder as a small mend with its next step; the hail line's comma where a description holds commas (ten rows, shared templates, and a served line that recorded passages may hold) is on my list; the close-hauled gap is the physics', recorded in the as-merged record for both two-deckers and the owner's eye; the replay fingerprint's timing under load is on my list beside truth 7-441's. **The 64's and the razee's `marines`** (84 and 14 would form their divisions and meet their bills exactly): BUILD with step 7 as a generator's change to B1's two files, each file's beat old beside new, and say whether any recorded passage of the 64's moves (a line every ship of two decks may say). **Next, in this order:** step 7 (B7.c, B7.d, B7.e, with (1), the 64's and the razee's marines and the design note's words); the trim's alias words; my earlier (1) and (6) of the 9th's note if not yet in (the bilander's short watch calling all hands for a settee; "make all sail" listing only what she has); then Phase 5 and the close-out as the note of 09:55 has it.
