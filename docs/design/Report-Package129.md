# Package 129: the trader at the Little Road, the harbour's King's ship, the prisoner's checkpoint

The design and report of package 129: faults 16, 17 and 18 of `docs/dev/CarriedForward-M7.md`, section 4, two of them found by the owner in their own play (their notes of 27 November). Each was reproduced first, its cause found, and mended at the cause. New truths 7-790 to 7-799: 7-790 to 7-793, 7-795 and 7-796 in `tests/test_weigh_signals_checkpoint.py`, 7-794 and 7-798 in `tests/test_harbour.py`, 7-797 and 7-799 in `tests/test_checkpoint.py`. No pin of before moved. The first build (c22aa834) was not passed; the lead's list of it and what was done is below ("The second build"), and the sections here are as the second build has it.

## Fault 17: a far trader at anchor never sails, and costs the game its pace

**Seen.** The owner's cruise off Dover (channel-east, from 05:00 of 12 June 1805, seed 1805, the hermaphrodite brig a King's ship by her papers, climatology and the business on) drew `business-16`, "trade 33 tons of brandy from the Havre to Dover", lying in the Little Road of the Havre. On the trunk (66d2db30) she laid her passage 193 times between 08:00 and 21:00 of the first day and never moved; the laying cost some 204 s of the day's play, and about 120 layings an hour at the next dawn. Put at the Little Road by herself (7-790's ship), she laid it 179 times between 10:00 and 13:00 and lay at 0.0 nm.

**Cause.**

1. The Little Road is three miles inside the Great Road, the Havre's outer road, beyond the 2 nm the far captain takes for "in port" of it; so she is drawn "at anchor".
2. Her first resolve saves her plan, `[anchor le-havre]`; her weigh after the hour at anchor restores it, and she lies.
3. The next minute she weighs again, and lays her passage afresh. The Havre's track to sea begins with the Little Road, a mark of kind `anchorage`, and the plan of such a leg ends with an anchor: her plan begins `("anchor", "le-havre")`, and she lies where she is.
4. And so every minute of daylight.

The body's own course out of a port (`ships.port_course`) drops the departing port's anchorage legs already; the far captain's plan did not.

**Mend** (`freesail/world/brains.py` alone; the planner and `captains.py` untouched):

- `FarCaptain._weighed_from`: every port's track to sea begins at its own anchorage (the 67 ports with a track to sea, each with the anchorage first). Where she lies at it as she weighs (within its leg's reach), that one leg is left out: it is where she is, not a mark to anchor at. Only it: a passage laid later, home to that port, anchors her there. Where it was the only anchorage of the legs (the planner lays the destination's anchorage only when the legs hold none, `Planner.legs_for`), the destination's is laid at their end, so that she comes to in the port she is bound for.
- `perceive_vessel`: she is in port by the world's own rule (`Ports.in_port_at`), within the port's reach of its outer road, its anchorage or its mooring, where the far captain had read the outer road alone. A ship come to at the Havre's Little Road, three miles inside the Great Road, is in port; so is a ship the business draws lying there (`Business._anchored_in`: "a ship drawn lying in a port"), and she does her business and sails when it is done.
- A weigh from an anchorage that lays a fresh plan is marked in her business (`WEIGHED`, its tick; `WEIGH_TRIES`, how many in a row). Each weigh that leaves her riding there doubles the wait before the next, from `AT_ANCHOR_LEAST_S` (an hour, as before) to `AT_ANCHOR_MOST_S` (a day, JUDGEMENT), by day and in clear weather as before; the count begins afresh when she comes to anew.
- The first weigh, which restores a saved plan, is as it was.

**Old beside new.** The Little Road's trader: 179 layings in three hours and 0.0 nm off, against 1 laying and 9.74 nm off at 13:00, on passage for Dover by the track's mark 49 33 N 0 05 W.

### The ports whose track to sea begins at an anchorage

Every port with a track to sea (67) begins it at its own anchorage. For ten of them the lead asked whether the mend covers a trader drawn lying there: for each, a trader drawn lying at its anchorage as the business draws her (`Business._anchored_in`; the probe's ship as 7-790's), bound to a port the business pairs it with, sailed 48 hours with the player's ship in mid Channel or mid sea, out of the near detail's reach of her (below).

| port, bound for | trunk | c22aa834 (the first build) | this build: her voyage in 48 h |
|---|---|---|---|
| the Havre, for Dover | lay looping, never moved | reached Dover at about 40 h, `done` 0.13 nm off, nothing sold | in port at Dover at 37 h; wine sold; salt beef bought for the Havre; sailing at 46 h |
| Favignana, for Trapani | 2,341 layings, never moved | in port at Trapani | in port at Trapani at 10 h; wine sold, salt bought; in port at Favignana at 27 h, salt sold; home to Trapani at 37 h |
| Palermo, for Milazzo | 2,341, never moved | `done` 0.08 nm off Milazzo, never in port | in port at Milazzo at 30 h; wine sold, wine bought for Palermo; sailing at 39 h |
| Portsmouth, for the Havre | 1,887, never moved | rode at the Havre's anchorage "on passage" | in port at the Havre at 24 h; wine sold, brandy bought for Portsmouth; sailing at 33 h |
| Trapani, for Favignana | 1,556, never moved | in port at Favignana, home | in port at Favignana at 16 h; wine sold; home to Trapani, in port at 27 h, done |
| San Fiorenzo, for Bastia | sailed | sailed | in port at Bastia at 17 h, wine sold, cheese bought; in port at San Fiorenzo at 37 h, cheese sold; sailing home at 46 h |
| Syracuse, for Augusta | 2,341, never moved | `done` 0.11 nm off Augusta | in port at Augusta at 17 h; wine sold; home to Syracuse, in port at 32 h, done |
| Torbay, for Dartmouth | 1,904, never moved | traded, then rode at Torbay "on passage" | in port at Dartmouth at 16 h; wine sold; home to Torbay, in port at 28 h, done |
| Weymouth, for Poole | 2,341, never moved | rode at Poole's anchorage "on passage" | in port at Poole at 18 h; wine sold; home to Weymouth, in port at 42 h, done |
| Lampedusa, St Helier | not drawn | not drawn | not drawn |

Every trader of the table ends her voyage in port with her cargo sold, and none is `done` at sea or rides "on passage" at rest. The causes of the first build's ends:

- `done` off the port (the Havre, Palermo, Syracuse): her track out held the passage's only anchorage, so the planner laid none at the destination (`Planner.legs_for` lays it only when the legs hold none), and the first build then left that one out. Her plan ran out off the port. Mended: the destination's anchorage is laid where it was the only one (`_weighed_from`).
- riding "on passage" at an anchorage (Portsmouth at the Havre's, Weymouth at Poole's, Torbay home): the anchorage is beyond 2 nm of the outer road (the Havre's Little Road 3.2 nm, Portsmouth's 4.2, Torbay's 2.2), and the far captain read "in port" by the outer road alone; anchored there "on passage", no transition of her doctrine took her from it (`merchant.yaml`: `on passage` goes `in port` only `on anchored in port`). Mended: in port by the world's own rule (`Ports.in_port_at`).

**With the player's ship at the destination's road** (as the first table was sailed, the player put at the road the trader is bound for): she passes within two miles of the player's ship, and for those minutes the game's own crewed captain sails her (`ships.NEAR_DETAIL_NM`). Found, not mended (`captains.py`, outside the one check opened to this package): the crewed captain lays her passage with the port she left as the port departing (`Captain._plan`, `departing = p.in_port or self._departing`), so the track out of that port is laid again from mid sea, its anchorage first; the far body takes that plan when she leaves the near detail, and sails back to the port she left. Torbay for Dartmouth, the player at Dartmouth's road: crewed at 12 h, far again at 13 h with the plan "Brixham road, anchor at Torbay", in port at Torbay at 16 h, nothing sold. The Havre's trader, the player off Dover: crewed in Dover's road, in port there and sailing nine hours on with her cargo unsold (the crewed captain's sale is by the boat and the prices, `Captain._sell`, not `business.transact`). It is the crewed captain's own form of this fault; the far captain's is mended.

Lampedusa and St Helier: the business draws no trader lying there, on the trunk or on this package. Every port tried as her destination (Licata, Valletta, Girgenti, Porto Palo, Pantelleria, Syracuse; St Peter Port, St Malo, Alderney, Weymouth, Poole) gives a plan the land guard refuses, and the business passes the pair over (`Business.refused`). Found, carried by the lead.

**Found, not mended: ships that take the ground.** In the first build's table (the player at the road), Syracuse's trader beating out was aground 6.2 nm off at 21 h, Portsmouth's going in at the Havre at 27 h, Trapani's at 6 h and off again. With the player away none of these took the ground in 48 hours; Favignana's, outward again after her round, was in distress at 32 h in the run with the player at the road. Their courses are the planner's tracks and the body's beating, unchanged by this package. Carried by the lead.

### The tile cache

`chart.Level` kept 16 tiles, the first in let go first. One laying of the Havre's passage reads 33 distinct tiles of one level and 31 of another, so with 16 every laying loaded them all again (37 loads; 0.62 s of 3.4 s over three layings). The bulk of a laying is the planner's own search (`nearest_shore`), not the tiles. Mended: the least lately read is let go, and 64 are kept (`TILE_CACHE`, JUDGEMENT, measured). A tile is the same read from the cache or the disk, so no answer changes: the same legs are laid with 16 and with 64 kept (7-792).

**Memory.** The chart has four levels: two fine, two coarse (one tile each in the owner's sea). In the owner's sea over 24 hours, the game's resident memory at its most was 116 MB on the trunk and 209 MB on this package, the fine levels holding 61 and 64 tiles at the end. The bound is 64 tiles a level, about 64 MB a fine level, so some 230 MB at the most. The same day ran in 293 s against the trunk's 705 s.

### The truths of the passage

- 7-790 (slow): the Havre's trader at the Little Road is in port, sails, and her plan ends at an anchor in Dover, never at the Little Road; and a smack twelve miles off Dover, the port she weighed from, runs home and comes to in it (the lead's finding (1): the first build left every anchorage of that port out, and she was `done` at sea).
- 7-791 (slow): a ship riding at sea, out of any port's reach, whose every weigh anchors her again: the waits run an hour, two, four, then eight through the night; after twenty, a day and once; and come to anew, the hour again.
- 7-792: the tiles, as before.
- 7-793 (slow, the lead's finding (4)): the owner's sea a day, no far vessel laying her passage more than three times in any hour, nor, her anchor down, more than three times in the day (measured at most two); and the Havre's trader comes to in Dover within 42 hours (measured 37), sells her wine there, and sails with a return cargo.

## Fault 18: the harbour's King's ship has no private signals

**Seen.** A ship made a King's ship in the harbour (the naval cruise, the hermaphrodite brig, papers `service: kings`): "the private signal" read "The private signal: none aboard."

**Cause.** `signals.table_of` gave the table by the captain's place alone (a King's ship's, a cruiser's, a commodore's) or by `papers: {private_signals: true}`. The hermaphrodite brig's captain has the Neufchatel's place, a privateer's; the papers' service was not read.

**Mend.** Where her captain's place gives no table, a King's ship by her papers (`service.papers_service`, `kings`) carries her nation's. `private_signals: false` still takes it from any ship and `true` still gives it; a privateer's or a merchantman's papers carry none, as before. The primer's chapter 23 says so.

**The other readers.** `flags.world_role` reads the papers first already, so her colours and her role were right. Found, not mended (the lead carries them):

- a privateer's or a merchantman's papers under a captain of a King's place still carry the table: the place wins;
- a King's ship by her wardroom alone, her captain given no such place and her papers no service, carries none, as the primer now says.

7-794 is the harbour's own form (the naval cruise made a King's ship and started: the table read; and with no service, none). 7-795 is `table_of` over eight papers.

## Fault 16: the first action's checkpoint refused

**Seen** (the owner's): a game of the first action, begun from the harbour's page, the colours struck and the parole given aboard the Renard, saved by the game's own save; loaded, the checkpoint was refused ("names pathlib.PosixPath") and the game replayed.

**Two walls, both on this road.**

1. **A path object in the world.** The server, made with the harbour's place of the consent records, put it in the world as it was given (`world.consent_records_dir`, for the seat hook), and again in every world the harbour begins or takes up. Given as a path, as `tests/test_harbour.py`'s harbour and any caller passing one gives it, every save of every game so begun held a `PosixPath` (a `WindowsPath` on Windows), a name the loader refuses. Found by `tools/checkpoint_holders.py` (below) on the first action begun through the harbour's own start and saved by the driver: "`pathlib._local.PosixPath` held by `consent_records_dir`". Mended: the server and the console keep the place as words (`str`), which the one reader (`seats._consent_record`, through `consent.check`) takes as it took the path.
2. **The prisoner's header.** With the player aboard her captor, the world's per-ship names (seed, journal, inputs) read the Renard's hull, and the checkpoint was headed with them: seed 1673561565 against the save's 7. The loader found it "not this save's" and replayed. Mended: `replay.write_checkpoint` heads it with the first hull's seed, journal and inputs, as the save is written. The digest is as before.

**What the owner's own road puts there.** `py -m freesail` with the settings' `consent_records` empty passes none, and the server puts nothing in the world; with a place given, it is words already (the start resolves path flags to strings). So the first wall is not certainly the owner's: the lead remembers the owner may have written the checkpoint again on the build machine in reading it, and the harbour began with a path there would hold one. The owner's save is not to hand. Tried, and no other path found: every shipped scenario begun as the harbour begins it, run ten minutes, saved and read by names (7-797); the first action through the harbour's start, with the place given as a path and as none, saved a prisoner by the driver (7-798); the census's own worlds, and five hours of captivity, earlier. When the save comes, `python -I tools/checkpoint_holders.py <save>.checkpoint` names what it holds and where, without loading it.

**The reader of names.** `tools/checkpoint_holders.py` walks a checkpoint's opcodes (`pickletools.genops`) and the memo as the loader would, and calls nothing in the file: no class is looked up, nothing built. For each name not admitted it prints the strings pushed nearest before it (the attribute or key that holds it), the classes about it and the strings after it (its words). 7-799 plants a path in a scenario and reads it back so, the unpickler made to fail if called.

**Truths.** 7-796: the first action, guns fired, colours struck, parole given, saved and loaded through the server's start: by its checkpoint, the same digest, and the same after ten minutes more. 7-797: every shipped scenario (49), begun as the harbour begins it, run ten minutes and saved, holds no path and no refused name, and loads by its checkpoint as saved. 7-798: the first action begun through the harbour's start, a prisoner, saved by the driver, read by names (no path, nothing refused), taken up again from the harbour by its checkpoint, the same digest; the server's own first world keeps the place as words.

## What moves

**The shipped scenarios.** All 49, begun as the harbour begins them, were run 13 hours on the trunk (ae16dc3e) and on this build, compared every ten minutes: every far vessel's position, state, done mark and first leg, and the log's lines. 42 are the same in every row. Seven move, every one with the business on and every one at Brest, and the player's log is the same in all seven:

| scenario | from | what moves |
|---|---|---|
| merchant-brig | 9 h | business-17 and business-18, drawn lying in the Bay of Brest, the port's anchorage, are in port and wait out their business there, where on the trunk they weighed at the hour as at anchor; at 13 h in port at Brest, where the trunk had them at sea off the Goulet; business-14, a privateer, chases where she ran on |
| merchant-cutter | 9 h | the same two; business-14 evades a little east of the trunk's |
| merchant-schooner-plymouth | 9 h | the same two, in port at 13 h |
| merchant-ship | 8 h | business-22, the same |
| smack-falmouth | 9 h | business-23, the same; and three Brest fishermen run home and land their catch at Brest (0.5, 0.6 and 2.1 tons sold), where on the trunk they were still "on passage" off Brest at 40 h, and the business draws three ships more in their place |
| prize-home | 10 min | business-26 in the Bay of Brest in port; the ships about Brest a little elsewhere, and two cruisers keeping station where on the trunk they were engaging |
| the-channel-observed | 10 min | business-26, the same; the ships about Brest a little elsewhere, and one ship more drawn |

The Bay of Brest, Brest's anchorage, is 8.1 miles inside the road of Bertheaume, its outer road. The business means such a ship to be in port ("a ship drawn lying in a port, at anchor at its anchorage, her business there part done"); the far captain now reads her so. The business-on scenarios run faster, as in the first build (merchant-brig 576 s to 295 s on this machine, prize-home 439 to 337).

**Pins.** No pin of before moved. This package's own truths of the first build were restated for the lead's list (7-790, 7-791 and 7-793; above).

**What a player or seat sees:**

- a far trader drawn lying at an anchorage beyond two miles of its outer road (the Havre's Little Road, the Bay of Brest, Portsmouth's, Torbay's) is in port there, and sails when her business in port is done (up to the twelve hours of `IN_PORT_WAIT_S`, less the hours the draw gives her), where on the trunk she weighed at the hour, or never;
- the far traders make their voyages: in port at the destination, the cargo sold and the return voyage begun, home and in port;
- a far ship bound home to a port beyond two miles of its anchorage comes to in it, where on the trunk she rode at it "on passage";
- a far ship that cannot get away from an anchorage is asked to weigh at an hour, two, four, eight and so to a day, not every hour;
- the private signal read in a ship made a King's ship by her papers;
- a game begun in the harbour, and a prisoner's game, load by their checkpoints.

## Mutants

Each mend taken out in a worktree of the hash, the truths that read it run. The first build's, all killed:

| mutant | killed by |
|---|---|
| no departing-anchorage filter in `_plan` | 7-790; and 7-793 |
| no `WEIGHED` wait | 7-791 |
| sixteen tiles kept | 7-792 |
| first in, first out (64 kept) | 7-792 (its eviction check) |
| no table by papers | 7-795 |
| the header from the followed hull | 7-796 |
| the place a path in the server's first world | 7-798 (its first-world check) |
| the place a path in a world taken up | 7-798 |
| the names' reader forgets the memo | 7-799 |

The lead's of the first build: the place a path in the console survived (62 tests passed); now killed by 7-798's console truth (`tests/test_console.py`). The second build's, all killed:

| mutant | killed by |
|---|---|
| every anchorage of the port she weighed from left out (the first build's) | 7-790, the smack home |
| no destination's anchorage laid | 7-790, the Little Road |
| in port by the outer road alone | 7-790, the Little Road |
| no doubling of the wait | 7-791 |
| doubling without its bound | 7-791 |
| the count not begun afresh when she comes to anew | 7-791 (its check added when this one first survived) |
| a name fetched again from the memo not told | 7-799 |
| "within" every object on the stack | 7-799 |
| an object told by its maker (`replay._new`), not its class | 7-799 |

## The trunk merged

The trunk was merged at 93cf624c (nineteen ship files, the corvette Diana; package 126's second part, its `captains.py`, `runner.py` and `scripts.py`). One conflict, in `docs/dev/TuningNotes.md`, where both sides had added a section at the end: both kept whole, 126's second part first, then this package's. No code conflicted; `captains.py` was not touched here. Nothing of this package counts the ship files: 7-797 takes every scenario the trunk ships, as it finds them. The tiers were run on the merged hash.

The trunk was merged again at 9c6a5c3e (documents only since 93cf624c: the work packages, the carried list, the ships' nudge, the proposal); no conflict.

The trunk was merged a third time at b122b23e, as merge ed173ca0. It was not documents only: package 90's A9 (`freesail/crew/quarters.py`, `freesail/orders/gunnery.py`, `tests/test_three_decks.py`) and its viewer (`client/projection.js`, `tests/test_view_geometry.py`), with their reports and pictures. One conflict, in `docs/dev/TuningNotes.md`, where both sides had added a section at the end: both kept whole, package 90's viewer first, then this package's. No code conflicted; no file of this package was touched by it. The tiers were run again on the merged hash.

## The second build: the lead's list of c22aa834

The first build was read by an independent reader and the lead and not passed, on six things; each was taken up here.

1. **A ship bound home to the port she weighed from never anchored there** (a regression of the first build). The first build left out every anchorage of the port in `_departing`, which is never cleared at sea, so a passage home to it lost its own anchorage. Mended at its cause: the one left out is the anchorage she lies at as she weighs, the first leg of the track out, when she is within its reach (`_weighed_from`). The reader's probe (a smack 12 nm off Falmouth, Plymouth and Dover, departing it, running home, 18 h): the trunk in port at all three; the first build `done` 1.7 nm off Falmouth and 0.1 nm off Dover, "on passage"; this build in port at all three, at the same hours as the trunk. smack-falmouth's fishermen: above. Pinned, 7-790's smack.
2. **The trader sailed and never arrived.** Two causes, both mended (above, the ports' table): the destination's anchorage laid where the track out held the only one; in port by the world's rule. `Planner.legs_for` is untouched: its check would have moved the crewed captain's plans too, so the mend is in `brains.py`. The riding cases' cause, and the crewed captain's form of the fault, are told above.
3. **7-799 on Python 3.11.** A path pickles as its words whole on 3.13 and as its parts on 3.11; the truth now holds the place by its words on either (`Path(*words)`). The tiers were run on Python 3.11 (below).
4. **7-793 could not tell health from a slow loop.** Restated (above). The weigh's wait doubles to a day (`AT_ANCHOR_MOST_S`, JUDGEMENT), pinned by 7-791.
5. **The console's road.** The console's `serve_agents` keeps the place as words as the server does; a truth of 7-798 in `tests/test_console.py` hosts the agents with a place given as a path, saves, reads the names (no path), and loads by the checkpoint.
6. **The reader's "within".** It named the last classes pushed before a path, not the objects holding it. Now the reader keeps the loader's stack by each opcode's own account (`pickletools`), and "within" is the objects on the stack whose state is given them after the name (their BUILD later), outermost first, an object made by the game's `replay._new` told by its class. A name fetched again from the memo is told as its own place, where the first build told a class only where it was first named: a second path in the same checkpoint was missed. A planted scenario path is told within `World < Hull < World < Scenario` (the world's façade), a planted `consent_records_dir` within `World`. Its words are the strings it is called with: a path's words on either Python.

## The tiers

On ed173ca0 (this package at 82d04503 with the trunk at b122b23e merged), on Python 3.11.18, four workers, `__pycache__` cleared before each run:

- The fast tier, whole: 9322 passed, 1 xfailed (1 h 12 min).
- The slow tier (`--slow -m "slow and not pace"`), every file a change of this package can reach, in three runs: the first 32 files 84 passed (12 min); the next 33 294 passed, 8 xfailed (1 h 35 min); the last 30 56 passed, 2 xfailed (18 min). The files are named one by one in the build's report.
- `tests/test_api_door.py`: 19 passed.

Before the third merge the same tiers passed on 757f2eab (fast 9201 passed, 1 xfailed; the slow runs all passed). The trunk's two new test files are not reached by this package and were run in the fast tier only. The commit that adds this section changes this report alone.
