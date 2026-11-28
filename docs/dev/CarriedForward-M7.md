# Carried forward from milestone 7

Milestone 7 was closed by the owner on 2026-11-24, **closed, with a list** (`docs/gates/gate-m7.md`). This page is what it still owes, in one place, and is the first input to the shape of milestone 8 (`docs/DesignProposal.md`, section 11). Nothing here is launched by being written here: each package is proposed to the owner in a few lines and begins at his word.

## 1. The owner's list: mended first in milestone 8

From his play of the gate (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`):

1. **The first passage teaches the time's compression**, not `tick` after `tick`, once the first `tick` has shown what one is.
2. **A game can be ended from the harbour**, without stopping the harbour or beginning another. **Mended: package 126, part one, merged 27 November at 7bc7de20.**
3. **Fog comes on and clears over a time**, and is said as it does ("the fog seems to be clearing", "a fog is settling in"), as far as the weather's simulation allows. **Mended: package 126, part one, merged 27 November at 7bc7de20.**
4. **The game's own captain replaces a spar carried away.** In the first action the Renard sailed three hours with her main topgallant mast gone and never shifted it; the work exists for a player. **Mended: package 126, part two, merged 27 November at 1a55c9c2, in four passes.**

**Placed by the owner the same day (the proposal's decision 79):** the first goes with the milestone of the player's first hours; the other three open milestone 8 as its mending step, with the older faults of section 4 and package 125, the test suite's package planned beside it.

## 2. Not played at the gate

- **Step 9, a model commanding the other ship in a fight**, was not played on the gate's build. The owner passed it on an action he had fought on an earlier build, which ended before parole was built. The seat at war with a human's ship under the revised consent brief, through to a parole asked by a model, has therefore not been seen by him. A model captor still has no forms for parole or for landing prisoners.
- Step 4, a wheel shot away, did not arise.
- Steps 6 to 8, the director and the models at stations, were played on his own build of a few days before the cut, not on the cut.

## 3. Known at the gate and not mended

As the gate's page lists them:

- Handed back to the game's own captain in a fight, the cutter can lie aback for an hour.
- `give chase` sets one course and does not follow.
- *A first passage* begun without bracing up leaves her aback for a quarter of an hour.
- A game with a model seated loads by replay, minutes for a day's play.
- No road of news (a letter, a report) carries what the player no longer learns of far ships he cannot see.
- A privateer's or a merchantman's people are still the ship file's (booked, package 124).
- The log read back is judged by where the player stands now; the game's own captain orders `fill away` twice (booked, package 122).
- The studding-sail booms stand an hour of 32 knots; their wear is to be measured.
- Leeway under reduced sail shrinks where Moore and Steel have it grow, and is large with little way on.
- Six prize-doctrine keys nothing reads.

Mended on the trunk since the cut, and so not in the gate's build: the flags by her service (package 121's follow-up); the harbour's start, where a page asking as a game began could be shown a world and a game that did not match.

## 4. Older faults on today's ships, found since the cut

Found by the ships' session's builders and the lead's readers while gating package 90; none is package 90's doing, and none is mended.

1. An order made to wait behind other work says so in its reply alone, never in the log.
2. A tack that fails can be logged "Tacked", the ship having come through the wind and swung back.
3. "Filled away" is said of a ship then going astern (the bilander, the lugger; the cutter and the smack after lying a-try).
4. Plain-sail work sets a topsail in a gale after `take in all sail`.
5. A ship hung in stays cancels the player's take-in when she boxes herself off.
6. The stations' table of the harbour keeps one game's choice of doors into the next.
7. The dire strain warning of a part can be held back ten minutes by a lesser warning of the same part.
8. The smack's cast says "Hoist away the topsail" while her topsail stays furled.
9. A `set the topsail` waiting for hands is never taken up again, and nothing says so.
10. Five ships draw a gun outboard of the side it is mounted in (the brig by 0.05 m, the hermaphrodite brig 0.15, the razee 0.35, the 74 0.18, the 64 0.10).
11. The merchant brig and the bilander never complete a tack within fifteen minutes, in any wind, under plain sail or shortened.
12. Under the game's own captain, `lie a-try` ordered with the wind abeam is not taken.
13. `clear for action` says "The boats are out and towing astern" of a boat at the booms.
14. The helm is kept as for headway while she makes sternway: the cutter, after `lie a-try` and `fill away`, sags to 39 degrees off the wind with 29 degrees of rudder the wrong way and goes astern at a knot for an hour (found by package 127's builder, 24 November; every ship's helm; package 127 makes the log say it and mends nothing of it).

15. A boat stove on the booms by a shot still reads as on the booms and can be sent ashore (found 24 November by the lead's reader; on the trunk before package 90).

16. A save of *the first action* has its checkpoint refused on loading ("names pathlib.PosixPath") and the game is replayed from its journal instead: it loads rightly, a minute and a half slower (found 24 November by the lead, loading the owner's gate save).

17. **A far ship at anchor that never sails, and costs the pace** (the owner's note 6 of 27 November, found by the lead in his cruise's saves). A trader of the background trade lying at anchor off the port she is to load at ("trade 33 tons of brandy from the Havre to Dover", at anchor off Le Havre) weighs every minute of the day, lays her whole passage over the chart afresh, finds its first leg is to anchor where she lies, and stays; the next minute she does it again. She never sails, and each laying of the passage costs about three-quarters of a second on the build machine: in his cruise about two-thirds of the machine's time by day, the pace falling to some fifty ticks a second with two crewed ships near him where the same sea without her cost runs about a hundred and fifty. By night she does not weigh, and the pace comes back; at dawn it falls again. One ship of the ten in his sea did it; it is on the trunk as on the gate's build.

18. **A ship made a King's ship in the harbour carries no private signals** (the owner's note 10 of 27 November; confirmed). The month's table is given by the captain's place (a King's ship's, a cruiser's, a commodore's) or by a scenario's `papers: {private_signals: true}`; the harbour writes `papers: {service: kings}` and neither, so `the private signal` is refused aboard her with the merchantman's reason. The primer's chapter 23 says it is so ("a King's ship by her papers or her wardroom alone ... carries none"); no scenario of the game is touched, only a game made in the harbour.

19. **A privateer made a crewed ship never closes a stranger she is looking at** (found by package 127's builder and the lead's reader, 27 November). Fully crewed, the convoy's privateer keeps about 2.1 miles from the stranger she investigates and takes up evading only at 1.94 to 2.00 miles; the builder reads the cause as her near lookout making out colours at two miles without the glass where her far captain used three with it (`captains._keep_stranger`); the reader saw the distances and could not confirm the glass. So the convoy of six's day turns on where she is placed: a cable farther and nothing happens, a cable nearer and she is judged an enemy but no straggler is signalled; with other seeds the exchange comes later. Truth 7-153 pins the day as shipped, at one seed.

20. Small things of package 127's new words, left as found by the lead's reader: "will follow the same work" said of a signal waiting behind a different signal; "some of it waits its turn" where all of it waits; an order's wait logged a tick after a line of the same moment that belays what it waited for; and a wait said for a `weigh` that will be refused, there being no anchor down.

Of these, package 127 (**merged 27 November at 572133ac**) mended 1, 3, 4, 7, 8, 9 and 13; package 125 takes 2 and 11; package 126 mended 6 in its part one (merged 27 November at 7bc7de20) and mended 12 in its part two (merged 27 November at 1a55c9c2); 5 could not be reproduced by a player's orders and is dropped; 10 is for the ships' session; 14 is not yet placed; 16, 17 and 18 are package 129, launched 27 November at the owner's word; 19, 20, 21, 22 and 23 are not yet placed; 24 is the ships' session's; 25 and 26 are for a later package of the captain's (22 is for the ships' session and a later package of the physics).

21. The saves a stand-down writes are named by seed and tick, and two written at one tick overwrite one another (found by package 126's builder; the desk's naming, older than the package).

22. **A wreck left hanging helps some hulls** (found by package 126's builder, 27 November, measuring the captain's spar work against the trunk). A wrecked sail gives no drive, but its windage and its spars' count three times over (`physics.sails`), and the wreck does her no harm: a topmast's wreck forward pays her off like a head sail. With the wreck cleared at the moment it falls, no hands and no time spent, the trunk's own captain makes less in seven of twenty-eight passages than with it left hanging (the 74 in 20 knots rising to 38: 0.8 miles made good against 9.6; the bilander in the same: 2.3 against 8.9), and more in the rest (the merchant brig in the rising wind 9.1 against -5.5). Nothing of the physics is changed by package 126; the captain clears a wreck as a seaman would, by the lead's ruling (section 7).

23. The box off's own line can name the wrong tack: "Boxed her off; braced sharp up on the starboard tack, full and by." said with her lying on the larboard tack, after `keep her full and by` and a box off had worn her round (the cutter and both schooners in 20 to 30 knots; found by the lead's reader of package 125 and traced by its builder, 27 November; older than the package).

24. Words of three ships' class and one's: the razee, the 64 and the 74 read "hMS as razeed, 1795", "hMS as built, a 64-gun ship ..." and "hMS a 74-gun ship ..." where a leading capital is made small; the smack reads "a Navy's smack" (found by the *Diana*'s builder, 27 November; for the ships' session with its third pass). **Mended 28 November at d8031973** (package 90's fourth pass): at the class words' cause for every file, the razee's note at her generator.

25. **A topsail schooner without her fore topmast will not always heave to in a rising gale, and her captain then falls silent** (package 126's part two, declared; the lead's reader, 27 November). With no topsail to lie under she is given `heave to`; in 38 knots it can fail ("she would not lie to on the larboard tack; the helm amidships"), is given again and fails again, and for about an hour and a half he gives no order while she neither lies to nor sails her course (15.9 miles made good in three hours where the trunk's, refused `lie a-try` once, sailed on and made 27.1). On another seed she heaves to and lies so.

26. The smack's heave-to in a gusty gale from the start fails three times and holds only after two and a half hours; in a steady gale she is never brought to, as before (the lead's reader of package 126's part two; she keeps her topsail now).
27. From rest, `set plain sail` and a course alone leave her yards unbraced for it (found by the tartane's builder, 28 November, measured on the trunk): the merchant brig started from a standstill heading 000, 045 and 315 with the wind north at 12 kn is 34 to 62 degrees off the course given after twenty minutes, at 1 to 1.7 kn, until `trim sails` or `brace sharp up` is ordered; she keeps headway and wears. Whether the watch should brace for the course given is a question of handling, for a later package of today's ships.
28. A world with no ship file whose sea holds crewed hulls raises in the glass (`lookout._glass_crewed` reads `ship.dyn` of a stub ship): reached only by a replay made without the game's ship factory, as a tool of the lead's did; no game a player runs has a stub ship.
29. A course given dead before the wind in a shifting wind can be lost (found by the tartane's builder from the owner's preview of 28 November, seed 7, the default gusts): from rest heading 292 with the wind three degrees east of north, `steer south` is read by the helm as a course across the wind by the stern; she is kept full and by and a wear is ordered; the wear is refused for want of way ("She has no way on her to wear"), the helm stays "Steady, full and by", and south is never steered again, whatever sail is then taken in. In steady wind every seed bears away; of six gusty seeds two never reach south in 1,500 s. It reaches any ship; with fault 27 it is why a ship started from rest by two orders alone can sit aback. For the same later package of handling.
30. A tack's time does not grow with a ship's size and mass as it should (found by the *Concepción*'s builder, 28 November): the three-decker of 4,440 tons goes about in 258 to 293 seconds where the 74 takes 237 to 258 and Luce gives a first-rate five to ten minutes; no setting of her file that holds her helm reaches it. It reaches every ship, the largest most. For the later package of handling, with 27 and 29.

## 5. Booked by the owner or the lead, not launched

- **Package 122:** the log read back as it was shown, and the captain's order given once (the owner, 20 November; low priority).
- **Package 123:** the corsair, by rules, so that no model need be seated (decision 76); placed in the career milestone.
- **Package 124:** a privateer's and a merchantman's own people (milestone 8).
- **Package 125, booked by the lead and placed by the owner in the mending step ("The mending step may come next, with package 125 as well") and launched on 24 November with packages 126 and 127: the moment of the haul.** The tack's script calls "mainsail haul" within a point of the wind for every ship; a ship that comes round slowly is turned back by it, and the same sentence of Luce gives the other moment, with the wind ahead. With it: a jib taken in by `shorten sail` where a ship cannot be held without it; a light ship not shortened in time by the game's own captain; item 2 and item 11 above. It changes how today's ships tack, and is gated as such.

## 6. Package 90, the ships, in hand across the gate

Released across the gate by the owner on 19 November. Merged so far: the helm's kind and a tiller's words; the whole lateen and its strain; a yard's level by its place on its mast and the topsail on a pole; the boat in tow. The lateen hulls' list of eight was merged on 24 November and its second pass the same day; its third and fourth passes joined on 28 November at d8031973; what is owed before the tartane's file now is the engine's step for what the client is served (a boat in tow, a lateen changed in a manoeuvre, the tréou and the great lateen). **The corvette *Diana* joined on 27 November at a9e0a3f7**, by the owner's word "Join now": a light ship with a small rudder, slack in stays in a fresh breeze under all plain sail, who wants her jib; her helm and her tacks are measured again, and the moment of her haul set in her file, when package 125 lands. **The three-decker's engine step (A9: three gun decks at quarters and in the orders) joined on 28 November at 89478745.** **The viewer's whole lateen and pole mast joined the same day at cfc1032b**, with a sail's belly and its foot's sag reckoned by each edge's own length: eighteen of the nineteen files' sail outlines moved, declared, and seen by the owner. Then the engine's fourth pass, a step for what the client is served, the tartane, the polacre, the xebec and the three-decker.

**The rule the lead set, the owner's to overturn:** lateen and tow steps join the trunk when today's ships are proven unmoved; every fault that reaches only a lateen hull or a boat in tow is owed in full, and proven, before any lateen hull's file joins.

## 7. The lead's rulings that are the owner's to overturn

Each was told to him when it was made and is in the records of its package. **On 27 November he said of those made that day and before: "your rulings stand."** **And later that day, of the rulings on package 126's part two merged over its reader, on consent records kept in a player's own data folder when the game runs from a download, and on the plainer word when the game is already running: "the rulings are good."**

- A model's station may not show, resume or stand down another's (package 117).
- After the player's own `hold your fire`, `engage` no longer opens fire (package 115 D).
- A ship lost to or parted from his own convoy is still said in his log (package 118).
- The boat in tow was widened to three files, and her drag is carried.
- The *Diana* files the displacement her own plan gives; the three-decker her drawn displacement.
- A ship with a wheel takes the tiller's orders and repairs her wheel; the hermaphrodite brig's helm is left as filed.
- Three outcomes on the smack with her topsail set (heaving to in 30 knots; a tack from hove to; backing and filling).
- Milestone 7's merges over a reader's NOT PASS by the rule of the lateen hulls' list (package 90: a lateen-only fault is owed in full before any lateen hull's file joins).
- In package 125, the rule that every captain takes in topgallants when a topgallant yard strains was built at the lead's ruling and then taken out by him: in the lee-shore trial it left her four miles further to leeward and filled her away into a gale two miles from the land. It is kept on the builder's branch with its cause.
- The game's own captain clears a wreck as soon as he has hands for it, and does not leave it hanging where the physics makes it serve her (package 126's part two; fault 22 of section 4): so his spar work is measured against the trunk where clearing is no loss, and against the wreck cleared at once where it is.
- The moment of the tack's "mainsail haul" is a habit of the ship, said in her file (package 125): a ship filed as slack in stays has her after yards hauled with the wind ahead when her way is gone, every other ship at the point as before. The builder showed that the slack ship and the gust-checked one cannot be told apart before the haul, and that the rule given to every ship cost the 74 and the 64 a minute to four in five cells of fifteen hundred; no ship of today's sets it, and the ships' session sets it for the *Diana*.
- In heavy or worsening weather the game's own captain does no work on a spar, the clearing of a wreck with it, until she lies to;; a ship with no topsail to lie under is given `heave to` (package 126's part two). Giving her her course again after two failed tries was built and did not restore her, so it was left out and the case is carried (fault 25).
- A player's own spar work gives way to a later order of his that is short of hands, and is taken up again after (package 126's part two).
- Package 126's part two was merged over its reader's "not pass" on one finding: the cutter, in a steady gale from the start, is brought to nineteen minutes later than the trunk's, having first taken in the light topsail the trunk's cutter lay under and lost; she ends hove to with her sail whole where the trunk's ends sailing on.
- A ship with no spare of the spar she has lost sails on without it until a yard refits her: the *Renard*'s captain clears the wreck, says there is no spare topgallant mast aboard, and keeps her one spare topmast for the loss of her topmast. **The owner, 27 November: "I am OK with leaving it (as recommended)".** **The owner, later the same day: "the work of a spar being converted to another that it could act as should come with the addition of the carpenter station"**: it is written into package 87's line of the proposal and its row.

- Readers at the gate: **the owner, 28 November: "You may read multiple packages at once, as the Opus usage for simply reading and reviewing is reasonable."** Several readers at once, each on Opus; the one-at-a-time rule of the 26th is lifted.

- Package 90, rulings of 28 November in the lead's notes to the ships' session (nudges 88 to 91): what the client is served of a boat in tow and of a lateen changed inside a manoeuvre is an engine step of its own, owed before the tartane's file (the rule above); the tartane's square topsail is re-cut three pieds clear of her lateen yard's slings, its foot nine tenths of its own yard, 8.5% under Forfait's sail area and declared as judgement (its depth had no source); her tréou and her great lateen do not stand together (Forfait p. 124), each order taking the other in first, and `all sail` keeps the great lateen; the tréou's yard hoists one pied below the slings; her plain sail is set jib and topsail first; lowering a great yard on deck is wanted seamanship, not owed for her file. The viewer's frame holds a lateen's peaked yard, so that the view never rescales: **the owner's word as the ships' session relays it, "(a) Fixed frame (Recommended)"**, and of the mended belly seen live, **"Both fixes look clean to me, very good."**

- Package 130: the game's console resolves its output when a console is made, not when its file is first read (two lines of `freesail/ui/console.py`, the cause of a test failing by the order of the tests), allowed inside the package. **The owner, 28 November: "You may allow it, as recommended ... It is fully allowed as far as I am concerned."**

## 8. Waiting on a decision of the owner's

- (Settled 24 November: the line between milestone 8's two gates, and the crew's morale and skill; the proposal's decision 79.)
- Milestone 7c, the data made true across 1792 to 1825: not begun.
- The older gates (6a with 6b, 6c, and the director's 7b) are closed with milestone 7 by his word of 24 November; what 7b left unbuilt is placed in section 9, the lead's proposal.
- The chart's work, parked; its records say where it stopped.
- **The owner's notes of 27 November** (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`, his later notes), with the lead's proposed placing, his to change: an order of succession appointed by the captain (his note 7; decision 63 gives the command to the senior officer) with milestone 8's second half, her people; a raking fire (note 8: a shot is placed anywhere along her length whatever her aspect, and nothing rakes) with the fight's known faults in milestone 8's first half, a package of its own from the sources; fire aboard, its fighting and the magazine (note 9) with package 77, and the guns' faults, condition and care with the gunner's station of package 87; temperature (note 11; the spec's deferred section 26) in two layers, the thermometer and the fog that comes of warm air over cold water with the weather of the world that moves, the cold with the crew's health in milestone 8's second half. **Settled the same day, as proposed ("The bookings read right to me"): packages 131 and 132 booked, packages 77 and 87 widened, temperature placed in its two layers; written into the proposal's roadmap.**
- Package 128 (the test suite): proposed, not launched. (Package 129, faults 16 to 18 above: launched 27 November at his word.)

## 9. What the director's milestone (7b) left unbuilt, placed

Gate 7b is closed with milestone 7 (the owner, 24 November). Of the packages decision 51 left on its books, 60, 63 and 65 were brought into milestone 7 and built, 64 was struck, and the heart of 51 landed as package 82. Four remain. **The placing below is the lead's proposal and the owner's to change; none is launched by it.**

| Left by 7b | What it is | Placed |
|---|---|---|
| The rest of package 51 | The director's chart, the truth drawn; the director's focus, and the ships' logs by kind and by a range of ticks | The world that moves and the career: the director's tools for a world that goes on without the player |
| Package 61 | A course laid clear of the land and the dangers, for every captain and the player, its legs said as the plan | The world that moves and the career, with the design package on how far the land goes |
| Package 69 | Five recorded passages that give another answer on Windows than on Linux; the harbour's banner test; the maker's doubled line ends on Windows | Milestone 8's structural work: the test suite's package, since the owner plays on Windows |
| Package 55 | The solo director and the gate's scenarios; the consent brief's revision; the gate's document | The revision is done (package 117) and the gate is closed. The solo director, a director with no player's ship, goes with the rest of 51 |
