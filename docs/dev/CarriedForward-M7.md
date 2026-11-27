# Carried forward from milestone 7

Milestone 7 was closed by the owner on 2026-11-24, **closed, with a list** (`docs/gates/gate-m7.md`). This page is what it still owes, in one place, and is the first input to the shape of milestone 8 (`docs/DesignProposal.md`, section 11). Nothing here is launched by being written here: each package is proposed to the owner in a few lines and begins at his word.

## 1. The owner's list: mended first in milestone 8

From his play of the gate (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`):

1. **The first passage teaches the time's compression**, not `tick` after `tick`, once the first `tick` has shown what one is.
2. **A game can be ended from the harbour**, without stopping the harbour or beginning another.
3. **Fog comes on and clears over a time**, and is said as it does ("the fog seems to be clearing", "a fog is settling in"), as far as the weather's simulation allows.
4. **The game's own captain replaces a spar carried away.** In the first action the Renard sailed three hours with her main topgallant mast gone and never shifted it; the work exists for a player.

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

Of these, package 127 (**merged 27 November at 572133ac**) mended 1, 3, 4, 7, 8, 9 and 13; package 125 takes 2 and 11; package 126 takes 6 and 12; 5 could not be reproduced by a player's orders and is dropped; 10 is for the ships' session; 14 is not yet placed; 16, 17 and 18 are the lead's proposed package 129, not launched; 19 and 20 are not yet placed.

## 5. Booked by the owner or the lead, not launched

- **Package 122:** the log read back as it was shown, and the captain's order given once (the owner, 20 November; low priority).
- **Package 123:** the corsair, by rules, so that no model need be seated (decision 76); placed in the career milestone.
- **Package 124:** a privateer's and a merchantman's own people (milestone 8).
- **Package 125, booked by the lead and placed by the owner in the mending step ("The mending step may come next, with package 125 as well") and launched on 24 November with packages 126 and 127: the moment of the haul.** The tack's script calls "mainsail haul" within a point of the wind for every ship; a ship that comes round slowly is turned back by it, and the same sentence of Luce gives the other moment, with the wind ahead. With it: a jib taken in by `shorten sail` where a ship cannot be held without it; a light ship not shortened in time by the game's own captain; item 2 and item 11 above. It changes how today's ships tack, and is gated as such.

## 6. Package 90, the ships, in hand across the gate

Released across the gate by the owner on 19 November. Merged so far: the helm's kind and a tiller's words; the whole lateen and its strain; a yard's level by its place on its mast and the topsail on a pole; the boat in tow. The lateen hulls' list of eight was merged on 24 November and its second pass the same day; a third pass of five is owed before the tartane's file. Then the corvette *Diana*, by the owner's word "Join now": a light ship with a small rudder, slack in stays in a breeze under all plain sail, who wants her jib; her helm and her tacks are measured again when package 125 lands. Then the tartane, the polacre, the xebec and the three-decker.

**The rule the lead set, the owner's to overturn:** lateen and tow steps join the trunk when today's ships are proven unmoved; every fault that reaches only a lateen hull or a boat in tow is owed in full, and proven, before any lateen hull's file joins.

## 7. The lead's rulings that are the owner's to overturn

Each was told to him when it was made and is in the records of its package.

- A model's station may not show, resume or stand down another's (package 117).
- After the player's own `hold your fire`, `engage` no longer opens fire (package 115 D).
- A ship lost to or parted from his own convoy is still said in his log (package 118).
- The boat in tow was widened to three files, and her drag is carried.
- The *Diana* files the displacement her own plan gives; the three-decker her drawn displacement.
- A ship with a wheel takes the tiller's orders and repairs her wheel; the hermaphrodite brig's helm is left as filed.
- Three outcomes on the smack with her topsail set (heaving to in 30 knots; a tack from hove to; backing and filling).

## 8. Waiting on a decision of the owner's

- (Settled 24 November: the line between milestone 8's two gates, and the crew's morale and skill; the proposal's decision 79.)
- Milestone 7c, the data made true across 1792 to 1825: not begun.
- The older gates (6a with 6b, 6c, and the director's 7b) are closed with milestone 7 by his word of 24 November; what 7b left unbuilt is placed in section 9, the lead's proposal.
- The chart's work, parked; its records say where it stopped.
- **The owner's notes of 27 November** (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`, his later notes), with the lead's proposed placing, his to change: an order of succession appointed by the captain (his note 7; decision 63 gives the command to the senior officer) with milestone 8's second half, her people; a raking fire (note 8: a shot is placed anywhere along her length whatever her aspect, and nothing rakes) with the fight's known faults in milestone 8's first half, a package of its own from the sources; fire aboard, its fighting and the magazine (note 9) with package 77, and the guns' faults, condition and care with the gunner's station of package 87; temperature (note 11; the spec's deferred section 26) in two layers, the thermometer and the fog that comes of warm air over cold water with the weather of the world that moves, the cold with the crew's health in milestone 8's second half.
- Package 128 (the test suite) and package 129 (faults 16 to 18 above): proposed, not launched.

## 9. What the director's milestone (7b) left unbuilt, placed

Gate 7b is closed with milestone 7 (the owner, 24 November). Of the packages decision 51 left on its books, 60, 63 and 65 were brought into milestone 7 and built, 64 was struck, and the heart of 51 landed as package 82. Four remain. **The placing below is the lead's proposal and the owner's to change; none is launched by it.**

| Left by 7b | What it is | Placed |
|---|---|---|
| The rest of package 51 | The director's chart, the truth drawn; the director's focus, and the ships' logs by kind and by a range of ticks | The world that moves and the career: the director's tools for a world that goes on without the player |
| Package 61 | A course laid clear of the land and the dangers, for every captain and the player, its legs said as the plan | The world that moves and the career, with the design package on how far the land goes |
| Package 69 | Five recorded passages that give another answer on Windows than on Linux; the harbour's banner test; the maker's doubled line ends on Windows | Milestone 8's structural work: the test suite's package, since the owner plays on Windows |
| Package 55 | The solo director and the gate's scenarios; the consent brief's revision; the gate's document | The revision is done (package 117) and the gate is closed. The solo director, a director with no player's ship, goes with the rest of 51 |
