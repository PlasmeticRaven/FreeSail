# The primer and the library redacted for a model reader (package 85, item 1)

**The rule, stated once.** The primer (`docs/primer/`) and the library's topics as the game
serves them (the catalogue of evolutions, the grammar, the world page, the tools' words,
the ship's papers), with the stations' briefs and the brief head a model is given, are
in-world documents for whoever reads them, human or model, at any station, in any
scenario, on any ship. Nothing in them may be true only for one scenario, one signal
book, one ship, one voyage or one stage of the build: no particular signal book presented
as the reader's; no pilot's news, price or stranger given as if of the reader's own voyage
unless marked as an example and set apart; no reference to milestones, packages, gates,
builders, the owner's rulings, the lead, a model's or a vendor's name, an instance, a
playtest or the development at all. The documents speak of "a model" and "the officer",
never of a vendor. "The owner" stands where it means the owner of the game at the door,
whom the consent brief names and whose grant, key and sentences the briefs speak of; the
project's owner ruling and judging is cut.

**The test** is `tests/test_in_world.py`: every primer chapter, every brief constant, every
tool's words, the library's topics rendered on a King's ship (`naval-cruise.yaml`) and on
a hired cutter (`dispatches-falmouth.yaml`), the brief head built for every station, and
the director's starter briefs' bodies, scanned for the forbidden words and patterns, with
an allow-list for the few words that are in-world too (the test's docstring says each
reason). It fails naming the line when one returns.

**This record** keeps what was cut and is still worth keeping: the history of a page, the
provenance of a figure, the packages that built each thing, so that a builder who reads a
chapter and wants to know where it came from finds it here and not in the chapter. The
evidence that moved the review: the owner's notes 3 to 6 of 2026-10-27 and the model
officer's five points (`docs/playtests/2026-10-25-to-27-owner-playtests-70-72/`), among
them a model reasoning the war's state from the primer's pilot example.

## What was cut from the primer, by chapter

The pattern throughout: a parenthetical naming the package that built a thing ("(package
57)", "since package 32e", "(spec M7b §14, package 53)") is gone from the chapter, the
thing itself staying; the package is named here against the chapter. A pointer to the
tuning notes or a truth's number ("`docs/dev/TuningNotes.md`, truth 27") is gone, the
figure staying where the chapter gave it; the truths are in `tests/test_known_truths.py`
and the notes under the package's section. A ruling of the owner's with its date is gone,
the rule staying as the chapter states it; the rulings are in `docs/DesignProposal.md`
and the packages' records.

| Chapter | Cut, and where it lives |
|---|---|
| README | the test's path (`tests/test_primer.py` runs every orders block); "the physics as tuned by package 10": chapter 7's logs are now recorded from the game as it stands, the other chapters' as each was written (said so in the README); "the gate M1 checklist" as the reader's first sail (the gates are `docs/gates/`); the chapter 25 row's broken formatting mended and the row brought into the table. |
| 1 | the royals set flying and Steel's staysails: package 57; the brig's middle staysail "was the main topmast staysail's other name before" (57); **stale and mended:** "you do not give orders to masts in this milestone" (the masts are sent down since milestone 3) and the whole section "What you cannot yet name" (there is no anchor, boat, gun, pump, log-line or crew), which said what milestones 5 to 7 built; replaced by "What else she carries", pointing at the chapters. |
| 2 | the helmsman's mark: package 37p; the half point steered to its last word before package 37l ("west, six and a half points from what was said"); the lugger and the smack: 43b, the lug topsails from the owner's first cruise in her (57; his note of 2026-10-17 that the lug topsail is set flying); "Fincham's rule, truth 25"; "a lug's gybe ... is milestone 7's" recast as not yet in the game, with what the helm does meanwhile (58b); `docs/DesignProposal.md` §4.3 for the readings a standing order tests. |
| 3 | the royals set flying (57); `docs/references/RigGeometryNotes.md` §8 (the ringtail and the save-alls) and §4 (the canvas numbers); "the sailmaker's mending comes with milestone 8"; "the 35-knot gale of gate M2" and truth 27 (a new royal holds, a worn one blows out); **stale and mended:** "what the game does not yet do is let her lie quietly: she goes astern at four knots" (truth 28; mended by package 37p, chapter 9 has her drifting at a knot and a half to two); "the schooner of the tenth playtest". |
| 4 | the three levels of bracing: 37p; the helmsman's old rule with the yards sharp up: package 45, from the owner's first run of gate m6a (she pinched until she was aback, boxed off and did it again); the sheet holds the trim: 32e, and the retired watch that tended every sheet a degree a second before it; `trim`: package 13, the order the owner reached for at gate M1; the trims by a point of sail: package 44, the owner's note 25, kept on the regatta's measure; the pointing figures: truths 1, 2 and 32; the after yards sharper: truth 24 ("the owner is judging it"); the weather helm figures: package 10's measurement, truth 6. |
| 5 | the sheets worked through the tack: 32e; Luce's five to ten minutes: truth 10; `put her about`: 45; RigGeometryNotes §5; the missed-stays rule: 32e; the lifting line's cause: 45c, and the point's trim: 44; the wear's nine minutes: truth 11; a course across the wind: the owner's ruling of 2026-10-09; "club-hauling needs an anchor and cable, which no ship file has yet (milestone 5)", stale, mended; "the M2 simplification"; hove to: truth 12; "the brig, who would not lie to at all in the playtest of 6 October"; "there are no tides until milestone 5" (backing and filling), stale, mended; the fore-and-after's turn: 32e, spec M5 open item 12; the turning circles: 32e. |
| 6 | "Her sails aback" (37c); the strain line (package 9); the kinds and SI data: spec M0 to M2 §5; "what the log says once": 58a, from the owner's playtests of October; `ahead`: 58a. |
| 7 | the physics as package 10 tuned it; truth 17 (no "taken aback" getting under way); "the order the owner asked for at gate M1" (`trim sails`); the schooner's refused tack: a note that the tuning notes had it; the well standing order's holding (the well is a reading since the ground, chapter 11); "since package 58b" (the course held till she has gathered way); the measurement behind the clauses' order (the tuning notes). The chapter's logs are to be recorded again from the game as it stands (item 2 of the review): the frigate's and the schooner's runs both differ from the chapter's as it stood, the schooner's tack now carried through where the chapter called it "a known fault". |
| 8 | "the milestones that use them" (the Luce chapter map); "Milestone 3 brought the catalogue to thirty-nine"; the stale list of evolutions not yet written (anchoring and weighing are, since milestone 5); the section "The game's own documents" (`docs/DesignProposal.md` §2, §4, §6.2; `docs/TechnicalSpec-M0-M2.md` §4, §8, §9; `docs/gates/gate-m1.md`, the checklist from which chapter 7 was drawn), replaced by the game's own data files. |
| 9 | "since milestone 5 the wind has a cause"; "the pinned wind of milestone 4"; the tuning notes for the sea's words and figures; "before package 37p she lay steady head to sea and went astern at four and a half". |
| 10 | "since milestone 5"; the account at anchor: package 68 and the cutter off Horta; "not in this build"; the nearest land's old words before 37l ("not to be seen: in this weather the shore shows within a cable at most", which an officer took for land within a cable and hove to in mid-Channel); the test's path; the sources' pointer to `docs/design/Navigation1805.md` §3 and the tuning notes (the two unverified figures stay named). |
| 11 | "the gates' days and passages" (the shipped days and passages); `gate-5b-passage.orders` as a passage's book (now `naval-cruise.orders`); truth 9; the lead's playtest of the second wave in which the Éclair's `at the anchor aweigh then steer E` put her helm over too soon (the lesson stays, the lugger unnamed); "in two playtests this rule braced a hove-to ship's backed yard round"; `shorten sail`'s widening (37p) and the captain's trials in which the frigate's jib blew out before it; **stale and mended:** "the pumps are a later milestone's" and "the water in the well is a grounding's leak's and nothing else's" (chapter 25); the test's path; 37l; "the strain truths and the tuning notes". |
| 12 | the chapter's heading, which read "11" (mended to 12); "the whole chart as built (package 45)"; the design study `docs/design/Navigation1805.md` §2 to §5 as the figures' source and the tuning notes for the unverified ones. |
| 13 | "decision 29's" rule; **stale and mended:** "past two metres in the well she is waterlogged and nothing more is modelled (the pumps are a later milestone's; until then a director may have the carpenter stop the leak ...)"; spec §7.5 for the cable's rating; "as the gate's frigate was found to be the first time the lead tried it"; `docs/references/Tides.md`, `docs/design/Tides1805.md` and package 34's notes as the tide's sources. |
| 14 | spec M7b §14 and package 53 (where you are is what you can do); spec M4 §12 (the papers by handle); package 54 (the stores eaten); "package 32b's cutter at far detail"; the owner's ruling on the pilot's boat bearing away unanswered; "the gate's books"; the owner's ruling that the pilot is a carrier of the truth; the tuning notes for the market's figures; package 53 (ashore), spec M7b §16 (the books), 53b and §17a (the things), 68 (the lugger got under way); package 36 (the pilot's vessel from the file), 37h (St Mary's rocks named; the tuning notes' figures); "that run waits for the colours of a later milestone" (Roscoff), recast on the code as it stands: the port reads a ship's nation and not the colours she shows; Bellin's sheet "(package 35b; the tuning notes say what is judgement)"; the sources' pointers to 54, 35, 37h, the owner's rulings of 5 and 7 October 2026, spec M5 §22 to §24 and `docs/design/InwardAndOutward.md`. **The pilot's news** example of a June 1805 log is now marked as one pilot's, from the voyage it was copied from, with the reading `the war` named for the reader's own (item 3). |
| 15 | "this milestone" throughout; 43b (the lugger and the smack; the business); milestone 6, spec M6 §4 and §19 (a captain of her own); **84 said:** "within four miles of you such a ship is a full ship ... beyond six miles she is a far thing again with her captain's state kept" recast as awake and asleep, her state whole; "three such ships at once is the most the clock affords (the tuning notes, package 43)" recast as the clock's default allowance with the cap's order of 84's step 7; "no price is moved by what they carry (a later milestone's)" recast as the far trader's transaction at the port's prices (84's step 4); 56 and the owner's note at gate 6c (the course in the lookout's line); 56 and spec M7b §21b (the glass's tiers); truth 7b-107 (the Palinure, now "a brig-sloop"); the tiers' judgement named in the tuning notes; "there this milestone stops: what follows a chase, the gun and the boat and the prize, is milestone 7's", recast on what is built; "the lead's test harness may give one too"; decision 46 and 45c (the world order's line for the record); "since milestone 6"; the Harness's "section 17" kept; "two scenarios ship with this milestone and are the gate's" and "their numbers at seed 7 are pinned in the tests"; the sources' pointers (spec M6 §4, §19, §20, package 43, 36, the chart study C §5.5, spec M5 §25 to §27, the proposal's §5.2, §6.1, §7.6, `docs/design/InwardAndOutward.md`). |
| 16 | spec M5 §29, §33, §34; "since package 40", "since package 41"; the MCP bridge or the local runner named for the door (the Harness document kept); `I have the deck` standing the station down before 37g, the owner's ruling of 5 October 2026; "in one game the owner said 'you have the con and nav and general authority in to Brest' and then gave twenty-three grants by name" (kept as a captain's); "Claude through Desktop keeps its own window" (a model whose client keeps its own window); the sources' pointers (spec M4 §11, M5 §29, §33, §34, `tests/test_officer.py`, the cold review of 2026-09-30 §3, the review of gate 5c's playtests, package 37g, the owner's rulings of 5 and 7 October 2026). |
| 17 | spec M6 §2 to §4 and §7, package 40; `freesail/world/captains.py`; truth 77; "*engaging* (present and empty until milestone 7)", stale, mended; "his figures in the tuning notes"; `tests/test_captains.py` (the game's own tests); "What the first runs of gate 6a taught him (package 45)" and 45c's sail made again by steps (the frigate aback by turns for an hour before it); "since package 43"; "package 84" for the one world; **stale and cut:** "No model is seated here yet: the station is a kind of thing the consent brief does not describe ... the package drafted the revision and the owner approves it" (42a made the brief; the station has been held since); the owner's ruling of 9 October 2026 on the owner's place; the Harness's §14 and §17 as sections; package 43 (the far captain); the sources' pointers (spec M6 §2 to §4 and §7, decisions 39 and 40, `docs/dev/M6-WorkPackages.md`, the tuning notes). |
| 18 | "the officer of the ninth game" and "the owner" as the two who did not know (a model at the officer's station and the captain over it); the tuning notes' section for package 40b (every order and the minute); the sources' pointers (spec M6 §5 and §6, the review of gate 5c's playtests, G19, `docs/dev/M6-WorkPackages.md`, the tuning notes). The officer's two conditions stay as its own words, quoted. |
| 19 | spec M6 §11 and §12, package 41; "since package 52" (the director's forms); 45c (the lookout unheld answered by the masthead; the owner's models asked it all the same; a station's name not its kind's); spec M5 open item 6; truth 84; 52 (a passenger brought aboard; a person nobody holds; who commands, "42b's leftover"); spec M7b §15 (earshot); spec M7b §14 and §17, package 53 (the equal reach); "45c's groundwork, completed by package 53" (several officers); **84 said:** "seats it in her own World ... beyond six miles she is demoted to far detail ... moving up a layer to work her in the plan layer's own shape" recast as a hull of the one world, awake and asleep; "the director of milestone 7b"; package 45 (the pictures drawn on canvases) and 45c (the picture never put back by itself; the owner's models doubted they had seen it); "the owner's testing setting is the default (decision 39, ruling 2)"; package 54, spec M7b §20, the owner's ruling of 2026-10-15 (the needs); "the ends ... are a later milestone's" (chapter 25); package 66 and the dispatches test (the station's line); package 58a and the owner's playtests of October (the deltas; the million characters); "the owner's lesson to the lugger's" ("steer, settle, trim"); the Harness's §15 and §17 as sections; the sources' pointers (spec M6 §11 and §12, the owner's rulings of 2026-10-09 and 2026-10-10, decision 39, package 41, spec M7b §9, §15, §20, packages 52 and 54, the master's suggestion, the tuning notes). |
| 20 | spec M7b §2 to §9, packages 50, 52, 62, the proposal's §7.6, decisions 39, 43, 46 and 50; the Harness's §17 (now section 19); **stale and mended:** "the hull's repair until milestone 8's pumps and carpenter come" (chapter 25); 52, 53b, 67, 68 by their forms; the owner's word of 2026-10-17 (examples, not a rule); 58a and the lugger director's asks (the forms verified, the dry run; 37% of its orders refused); R-39 (the weather grows in); "the owner's rule of decision 50" and "the owner's words" (doubted, not refused); 52, 66 (the voice by station or trade), 53b and the owner's question after the dispatches test (things and money), 62 and the owner's proposal of 2026-10-18 (the hand), 66 (the hold named); **84 said:** "a far ship has no log of her own: the line goes into her short story, which the director's truth will read when package 51 gives it the ships' logs", recast: a ship asleep keeps her log, `read_log(ship=)` reads it; "the gate's" brief (`quiet-passage`); 66 (the director's line), 58a, the dispatches test's finding 9; decision 46; 67 and the owner's word of 2026-10-23 after the cold review (the word apart from the game); spec M6 §23, M7b §2a, packages 43 and 67 (the seats); the Harness's §19 as a section; the sources' paragraph whole, recast as the director's principles without their decisions' numbers. |
| 21 | package 56, spec M7b §21a; "as the owner put it" (not a fishing simulation); the tuning notes for the yields; truth 106; "since this package". |
| 22 | package 70, spec M7 §7 to §12; "later chapters' (the milestone's next packages)" and "the next package's" (chapter 25); "a later package's" (the prize); the sources' pointer to spec M7 and the tuning notes. |
| 23 | package 71, spec M7 §1 to §6; "the hoists the builder made in the period's form" (made up). |
| 24 | package 72, spec M7 §21 to §23; truths 7-152 to 7-155; **a pinned figure moved by 84's step 6 and not yet in the chapter:** the Friendship back in her station at 5280, now 6420 (the one clock; the notes under 84's step 6); "promoted" (woken). |
| 25 | package 73, spec M7 §11, §11a, §13 to §17, `docs/design/Design-WaterAndHealth.md`; "the next milestone's" (the prize); the tuning notes. |

## The library's topics, the briefs and the tools

- **The catalogue of evolutions** serves the comment block each file of `data/evolutions/`
  opens with. Seventy-three of the ninety-eight carried the build in that block: the spec's
  section and the package in the first sentence, the owner's rulings with their dates, the
  playtests and the reviews, truths' numbers. Each file now opens with the in-world
  description (the evolution, its steps, its sources in the period's books, its times and
  what is judgement), and its build notes stand below a blank line under the head "Build
  notes (not served by the library's catalogue)", where the catalogue's reader stops; a
  parenthetical that mixed a source with a package keeps the source. The appendix below
  lists what was cut from each served head. Two `source:` fields that named the spec and
  the design study (`clear_for_action`, `take_lunar`) now name the figure's judgement and
  de Grijs.
- **The grammar's world orders** (`director.WORLD_ORDER_FORMS`): the notes of three forms
  named packages 71 and 72 and spec M7 §21 and §22 (whose signals command her; the
  regimes; a set made); the captain's intent form's note said "the owner's seam" (now "the
  followed ship's rules-based captain given an intent").
- **The world page** (`director.world_page`): "appended in play (package 58a)"; its fifth
  section opened "Package 73: the water, the wounded and the fight on deck".
- **The captain's brief** (`agent.CAPTAIN_BRIEF`): "(primer 23; package 71)" and "(primer
  24; package 72)".
- **The director's brief** keeps the owner at the door, as the consent brief has him; the
  starter briefs' limits line said "(package 71)" of false colours, and the channel's
  refusal the same.
- **The tools** `world_order` and `truth` opened "(spec M7b §3)" and "(spec M7b §2)".
- **The people's outlines** (`data/people/frigate-36.yaml`, `brig.yaml`), read into the
  captain's brief head: the gunner's station said "the quarters and the drill are his when
  milestone 7 brings them"; they are his.

## Not touched, and noted for the lead

- `docs/agents/ConsentBrief.md` and `docs/agents/consent/` are package 55's: the consent
  brief's head names the owner's consent-and-preference brief of 2026-09-26, the build
  session, packages 37g and 42b, decision 48 and spec M6 §15 and §23 in its own preamble.
  Those are the brief's provenance, in its words; a model reads them. If the rule is to
  reach the consent brief, package 55 is where.
- The playtest folders under `docs/playtests/` are named for the models that played
  (gate 4b's watcher and the rest); they are the record, not the library, and the rule
  does not reach them.
- The captains' doctrine files (`data/captains/*.yaml`) carry their figures' sources with
  the packages and the spec's sections named; they are read by the rules captain and by
  nobody at a station, so the rule does not reach them. The ship files' sources likewise.
- `freesail/core/world.py` stamps every save `BUILD_NAME = "m6c"`, and the console says so
  at a replay ("The save is this build's (m6c, ...)"), a name of the gate the stamp was
  last set for; `tests/test_replay.py` pins it. It reaches a player, not a station; the
  lead's to move when a gate is cut.

## Appendix: the evolution headers' cuts

| Evolution | What was cut from the served head |
|---|---|
| `back_anchor` | spec M5 §18 |
| `back_anchor` | package 34 |
| `back_anchor` | package 35 |
| `back_and_fill` | There are no tides until milestone 5, so what the manoeuvre keeps her is her place, not a channel: the tideway half of Luce's handling is left out. |
| `batten_down` | spec M7 §13 |
| `batten_down` | package 73 |
| `bend_sail` | spec 3b §6.3 |
| `bend_sail` | the storm mizzen while the spanker is bent, spec 3b §6.4 |
| `bend_sail` | Milestone 3b: the sail room holds sails, each made for one sail of the ship with its canvas number and condition (the ship file's `crew.stores.sails`, or for a file with only a count that many made-up sails for any yard). |
| `bend_sail` | milestone 3b: storm canvas and the occasional sails are jib-headed, gaff and studding-class sails that start in the sail room |
| `box_off` | package 37p |
| `cast_loose_guns` | spec M7 §8 |
| `cast_loose_guns` | package 70 |
| `cat_and_fish_anchor` | spec M5 §18 |
| `cat_and_fish_anchor` | package 34 |
| `clear_for_action` | spec M7 §8, §8a |
| `clear_for_action` | package 70 |
| `clear_for_action` | spec M7 §8 |
| `clear_wreck` | package 30b, playtest 10's finding 1: a studding-sail boom carried away and no order could clear it |
| `come_to_anchor` | spec M5 §18 |
| `come_to_anchor` | package 34 |
| `come_to_anchor` | decision 30: "full Luce/reference based anchor handling" |
| `come_to_anchor` | the M2 simplification heave_to uses: the sails' states set, the hands' time the phase's |
| `come_to_anchor` | paragraph moved: Package 37f (the review of gate 5c's playtests, 5.8): "come to an anchor in twelve fathoms" is the d |
| `cut_away_mast` | spec M7 §14 |
| `cut_away_mast` | package 73 |
| `dip_lug` | package 43b |
| `dip_lug` | the proposal's §4.4, the lugger's rig-specific evolution, written as the running bowsprit was for the cutter, package 32b |
| `dip_lug` | the dip of later boatmen round the mast without lowering, which was quicker, is not in the period's texts, `docs/design/VesselReferences-2026-10.md` § 1.4 |
| `ease_catharpins` | milestone 3b, spec 3b §3 |
| `ease_catharpins` | spec 3b §3 |
| `fill_away` | package 10, truth 12 |
| `fill_away` | package 37f |
| `fill_away` | three times in the playtest |
| `fish_spar` | spec M7 §14 |
| `fish_spar` | package 73 |
| `fother_sail` | spec M7 §14 |
| `fother_sail` | package 73 |
| `furl_gaff` | Not in the required list for M2, but the verb table's `furl` needs a `furl_<class>` for every class. |
| `furl_jibheaded` | Not required for M2 but completes the `furl_<class>` set. |
| `get_under_way` | spec M5 §23 |
| `get_under_way` | package 35 |
| `get_under_way` | the owner, 2026-10-02: `weigh` alone leaves her with the anchor up and no sail set, and `get under way` is Luce's whole sequence |
| `get_under_way` | the review of gate 5c's playtests, 5.8, "Getting under way" |
| `get_under_way` | Package 37f: the fore-and-aft cast, and no cast said at a timeout. |
| `get_under_way` | In the playtests her mainsail was set flat aft for the tack and her jib to leeward, all three of a schooner's casts ran to the timeout, and each was logged "She has paid off". |
| `goose_wing` | the game follows Luce, as the spec does. |
| `grapple` | spec M7 §11a |
| `grapple` | package 73 |
| `haul_bowline` | milestone 3b, spec 3b §4 |
| `haul_lines` | package 56 |
| `haul_nets` | package 56 |
| `haul_seine` | package 56 |
| `haul_trawl` | package 56 |
| `heave_deep_sea_lead` | spec M5 §13, §15 |
| `heave_deep_sea_lead` | package 33a |
| `heave_deep_sea_lead` | N §1 |
| `heave_in` | package 37f |
| `heave_in` | paragraph moved: The review of gate 5c's playtests, 5.8 and 10.4: `heave in 70 fathoms` ran as `heave short` and a hu |
| `heave_lead` | spec M5 §13, §15 |
| `heave_lead` | package 33a |
| `heave_log` | spec M5 §15 |
| `heave_log` | package 33a |
| `heave_mark` | practice and resupply, between packages 72 and 73 |
| `heave_mark` | docs/design/Build-PracticeAndResupply.md §6 |
| `heave_short` | spec M5 §18 |
| `heave_short` | package 34 |
| `heave_short` | paragraph moved: Package 37f: the anchor named is the anchor hove short (parameter `anchor`; the one she rides by whe |
| `heave_to` | package 32e |
| `heave_to` | the sail aback by its sheet, the physics of package 32e |
| `heave_to` | package 37f |
| `heave_to` | in the playtest the brig did so from seven knots inside a minute, the helm fixed at helm_deg |
| `heave_to` | package 37p, the captains' trials: in a gale she gathered four knots astern under the backed topsail and the evolution waited for her way to come off, failing at the end of its time and leaving her aback |
| `heave_to` | truth 12 |
| `jury_mast` | spec M7 §14 |
| `jury_mast` | package 73 |
| `lay_out_kedge` | spec M5 §23 |
| `lay_out_kedge` | package 35 |
| `lay_out_kedge` | package 34's note "a kedge laid by the boat" |
| `lay_out_kedge` | Warping to it (heaving the ship up to the kedge) is milestone 8's |
| `let_go_anchor` | spec M5 §18 |
| `let_go_anchor` | package 34 |
| `let_go_anchor` | paragraph moved: Package 37f (the review of gate 5c's playtests, 5.8; the owner's ruling of 2026-10-07): it says its  |
| `lie_a_try` | package 57: the ship file's `lying-to staysails`, Steel's main staysail, 1794 vol. II, "Lying-to under the main staysail" |
| `lie_a_try` | package 10 found the same for heave_to |
| `make_signal` | spec M7 §3 |
| `make_signal` | package 71 |
| `make_signal` | docs/design/Design-Signals.md |
| `moor` | spec M5 §23 |
| `moor` | package 35 |
| `moor` | package 34's note: "mooring with two anchors and the hawse" |
| `plug_shot_hole` | spec M7 §14 |
| `plug_shot_hole` | package 73 |
| `reef_bowsprit` | package 32b |
| `reef_bowsprit` | spec M5 §23 |
| `reef_lug` | package 43b |
| `reeve_line` | package 31b, from playtest 11's finding 7: a parted sheet could not be repaired, and the refusal's "spliced or rove afresh" named no order |
| `rig_out_bowsprit` | package 32b |
| `rig_out_bowsprit` | spec M5 §23 |
| `rig_out_studdingsail_boom` | spec 3b §7 |
| `rig_out_studdingsail_boom` | Milestone 3b: every boom starts rigged in, as at sea, and the ship files say so (tools/gen_ships.py) |
| `rig_preventers` | spec M7 §14 |
| `rig_preventers` | package 73 |
| `secure_guns` | spec M7 §8 |
| `secure_guns` | package 70 |
| `send_boat` | spec M5 §23 |
| `send_boat` | package 35 |
| `send_boat` | freesail/world/people.py, truth 68 |
| `serve_small_arms` | spec M7 §11 |
| `serve_small_arms` | package 73 |
| `set_flying` | package 57 |
| `set_flying` | the owner's note of 2026-10-17 (the lug topsail swayed up from the deck and sent down whole). |
| `set_lines` | package 56 |
| `set_lug` | package 43b |
| `set_studding` | paragraph moved: Milestone 3b (package 23, spec 3b §7): nothing here refuses a studding sail on a wind. Forward of Lu |
| `set_studding` | paragraph moved: Milestone 3b (package 22, spec 3b §6.4): the ringtail and the water sail are studding-class sails wi |
| `set_up_rigging` | spec M7 §14 |
| `set_up_rigging` | package 73 |
| `shake_out_lug` | package 43b |
| `shift_sail` | spec 3b §6.3: params `canvas_no`, `heavy`, or `for` another sail bent in this one's place, "shift the spanker for the storm mizzen" |
| `shift_sail` | Shift a sail (scripted, ShiftScript in scripts.py): unbend the old one and bend another in its place, the one repair of milestone 8 brought forward because it is the heaviest crew work the ship does and it lets a gale's blown-out sails be made good. |
| `shift_sail` | A drawing sail is taken in first and the new one set in its place when the work is done (gate 4a's ruling, 2026-09-27: shifting a sail is the whole of taking it in and replacing it |
| `shift_spar` | package 30b |
| `shoot_nets` | package 56 |
| `shoot_seine` | package 56 |
| `shoot_trawl` | package 56, spec M7b §21a |
| `swifter_in_catharpins` | milestone 3b, spec 3b §3 |
| `swifter_in_catharpins` | spec 3b §3 |
| `tack` | spec §8.5, scripted |
| `tack` | spec M5 open item 12 |
| `tack` | docs/dev/TuningNotes.md, package 32e |
| `tack` | Package 32e: the miss-stays rule reads the vessel. |
| `take_in_flying` | package 57 |
| `take_in_flying` | the owner's note of 2026-10-17: the lug topsail "sent down whole when taken in", and in a breeze the topmast itself struck |
| `take_in_lug` | package 43b |
| `take_lunar` | N §2 |
| `take_lunar` | N §2: the quarter of an hour the study's, the hour below UNVERIFIED there, and `sights.LUNAR_CLEARING_MINUTES` says so |
| `take_lunar` | Take a lunar (spec M5 §14 |
| `take_lunar` | package 33b |
| `take_lunar` | N §2, §4(c), §5): a set of distances of the sun or a star from the moon, with the two altitudes. |
| `trim_gaff_sheet` | package 32e, spec M5 open item 13 |
| `trim_jib_sheet` | package 32e, spec M5 open item 13 |
| `trim_lug_sheet` | package 43b |
| `trim_lug_sheet` | package 32e, spec M5 open item 13 |
| `unbend_sail` | spec 3b §6.3 |
| `unbend_sail` | milestone 3b |
| `unmoor` | spec M5 §23 |
| `unmoor` | package 35 |
| `veer_cable` | spec M5 §18 |
| `veer_cable` | package 34 |
| `veer_cable` | paragraph moved: Package 37f (the review of gate 5c's playtests, 5.8 and 10.4): the cable veered is the anchor's that |
| `wear` | spec §8.5, scripted |
| `weigh_anchor` | spec M5 §18 |
| `weigh_anchor` | package 34 |
| `weigh_anchor` | the package's measure, docs/dev/TuningNotes.md |
| `weigh_anchor` | paragraph moved: Package 37f (the review of gate 5c's playtests, 5.8 and 10.4): the anchor named is the anchor weighe |
