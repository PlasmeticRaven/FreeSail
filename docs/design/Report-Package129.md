# Package 129: the trader at the Little Road, the harbour's King's ship, the prisoner's checkpoint

The design and report of package 129: faults 16, 17 and 18 of `docs/dev/CarriedForward-M7.md`, section 4, two of them found by the owner in their own play (their notes of 27 November). Each was reproduced first, its cause found, and mended at the cause. New truths 7-790 to 7-799: 7-790 to 7-793, 7-795 and 7-796 in `tests/test_weigh_signals_checkpoint.py`, 7-794 and 7-798 in `tests/test_harbour.py`, 7-797 and 7-799 in `tests/test_checkpoint.py`. No pin of before moved.

## Fault 17: a far trader at anchor never sails, and costs the game its pace

**Seen.** The owner's cruise off Dover (channel-east, from 05:00 of 12 June 1805, seed 1805, the hermaphrodite brig a King's ship by her papers, climatology and the business on) drew `business-16`, "trade 33 tons of brandy from the Havre to Dover", lying in the Little Road of the Havre. On the trunk (66d2db30) she laid her passage 193 times between 08:00 and 21:00 of the first day and never moved; the laying cost some 204 s of the day's play, and about 120 layings an hour at the next dawn. Put at the Little Road by herself (7-790's ship), she laid it 179 times between 10:00 and 13:00 and lay at 0.0 nm.

**Cause.**

1. The Little Road is three miles inside the Great Road, the Havre's outer road, beyond the 2 nm the far captain takes for "in port" of it; so she is drawn "at anchor".
2. Her first resolve saves her plan, `[anchor le-havre]`; her weigh after the hour at anchor restores it, and she lies.
3. The next minute she weighs again, and lays her passage afresh. The Havre's track to sea begins with the Little Road, a mark of kind `anchorage`, and the plan of such a leg ends with an anchor: her plan begins `("anchor", "le-havre")`, and she lies where she is.
4. And so every minute of daylight.

The body's own course out of a port (`ships.port_course`) drops the departing port's anchorage legs already; the far captain's plan did not.

**Mend** (`freesail/world/brains.py` alone; the planner and `captains.py` untouched):

- `FarCaptain._plan` drops the legs to the anchorage of the port she is departing (`_departing`), as `port_course` does. Her course out begins with the track's next mark.
- A weigh that lays a fresh plan is marked in her business (`WEIGHED`, its tick), and the weigh from an anchorage is tried again only when `AT_ANCHOR_LEAST_S` (the hour, as before) has passed since the later of her state's entry and that mark. A weigh that leaves her at anchor waits the hour again, never a minute.
- The first weigh, which restores a saved plan, is as it was, so that a ship whose business is off moves not at all.

**Old beside new.** The Little Road's trader: 179 layings in three hours and 0.0 nm off, against 1 laying and 9.74 nm off at 13:00, on passage for Dover by the track's mark 49 33 N 0 05 W.

### The other ports whose track to sea begins with an anchorage

Ten other ports' `to_sea` tracks begin with an anchorage that is not the outer road: Favignana, Lampedusa, Palermo, Portsmouth, San Fiorenzo, St Helier, Syracuse, Torbay, Trapani and Weymouth. For each, a trader was drawn lying at its anchorage as the business draws her (`Business._anchored_in`; the probe's ship as 7-790's), bound to a port the business pairs it with, and sailed 48 hours, on the trunk and on this package.

**The ground report was wrong in one thing.** It said a ship drawn *in port* at one of these (the anchorage within reach of the outer road) would loop every twelve hours. It loops every minute, as the Havre's: in port, her business done, she lays her passage, the track's first leg anchors her where she is, and the next minute she lays it again. The mend covers in port as at anchor.

| port, bound for | anchorage to outer road | drawn | trunk: layings in 48 h, where | package: layings, where at 48 h |
|---|---|---|---|---|
| Favignana, for Trapani | 1.94 nm | in port | 2,341, never moved | 3; sailed, in port at Trapani |
| Palermo, for Milazzo | 0.56 nm | in port | 2,341, never moved | 2; on passage, 88.7 nm on |
| Portsmouth, for the Havre | 4.22 nm | at anchor | 1,887, never moved | 2; sailed, in the Havre's road at 18 h, aground going in (below) |
| Trapani, for Favignana | 0.62 nm | in port | 1,556, never moved | 3; sailed, in port at Favignana, home again |
| San Fiorenzo, for Bastia | 2.01 nm | at anchor | 5, sailed | 5, sailed: the same, hour by hour |
| Syracuse, for Augusta | 1.15 nm | in port | 2,341, never moved | 2; sailed, aground 6.2 nm out (below) |
| Torbay, for Dartmouth | 2.23 nm | at anchor | 1,904, never moved | 2; sailed, in port 4.7 nm on |
| Weymouth, for Poole | 1.68 nm | in port | 2,341, never moved | 2; on passage, 19.0 nm on |
| Lampedusa | | | not drawn | not drawn |
| St Helier | | | not drawn | not drawn |

San Fiorenzo's trader did not loop on the trunk and sails the same on both. Lampedusa and St Helier: the business draws no trader lying there, on the trunk or on this package. Every port tried as her destination (Licata, Valletta, Girgenti, Porto Palo, Pantelleria, Syracuse; St Peter Port, St Malo, Alderney, Weymouth, Poole) gives a plan the land guard refuses ("plan crosses the land on the leg to ..."), and the business passes the pair over (`Business.refused`). That is the planner's track out of those two ports, not this fault, and is not mended here; found, for the lead.

**Found, not mended: ships that now sail and take the ground.** Three of the ships that lay looping on the trunk now sail, and meet what any far ship under way may: the ground.

- Syracuse for Augusta: beating out, aground 6.2 nm from the Great Harbour at 21 h, and there to the end of the 48 h.
- Portsmouth for the Havre: in the Havre's Great Road at 18 h; going in for the Little Road at 27 h, aground some 2.7 nm on, and there to the end.
- Trapani for Favignana: aground 0.4 nm out at 6 h, off again by 15 h, and her voyage made.

Their courses are the planner's tracks and the body's beating, both unchanged by this package (the same legs are laid, 7-792; no route changes). None of the shipped scenarios draws such a ship within thirteen hours (below). A player in sight of one would see a far ship aground where, on the trunk, they saw a ship at anchor that never weighed.

### The tile cache

`chart.Level` kept 16 tiles, the first in let go first. One laying of the Havre's passage reads 33 distinct tiles of one level and 31 of another, so with 16 every laying loaded them all again (37 loads; 0.62 s of 3.4 s over three layings). The bulk of a laying is the planner's own search (`nearest_shore`), not the tiles. Mended: the least lately read is let go, and 64 are kept (`TILE_CACHE`, JUDGEMENT, measured). A tile is the same read from the cache or the disk, so no answer changes: the same legs are laid with 16 and with 64 kept (7-792).

**Memory.** The chart has four levels: two fine, two coarse (one tile each in the owner's sea). In the owner's sea over 24 hours, the game's resident memory at its most was 116 MB on the trunk and 209 MB on this package, the fine levels holding 61 and 64 tiles at the end. The bound is 64 tiles a level, about 64 MB a fine level, so some 230 MB at the most. The same day ran in 293 s against the trunk's 705 s.

### The pace truth

7-793 counts layings, not seconds: the owner's sea for 24 hours, no far vessel laying her passage more than three times in any hour (JUDGEMENT: a far captain lays it on weighing, his business in port done, a chase or a gale over; measured at most two), and the Havre's trader on passage. It is in the slow tier (`SLOW_TESTS`) and runs some 300 s.

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

**What the owner's own road puts there.** `py -m freesail` with the settings' `consent_records` empty passes none, and the server puts nothing in the world; with a place given, it is words already (the start resolves path flags to strings). So the first wall is not certainly the owner's: the lead remembers he may have written the checkpoint again on the build machine in reading it, and the harbour began with a path there would hold one. The owner's save is not to hand. Tried, and no other path found: every shipped scenario begun as the harbour begins it, run ten minutes, saved and read by names (7-797); the first action through the harbour's start, with the place given as a path and as none, saved a prisoner by the driver (7-798); the census's own worlds, and five hours of captivity, earlier. When the save comes, `python -I tools/checkpoint_holders.py <save>.checkpoint` names what it holds and where, without loading it.

**The reader of names.** `tools/checkpoint_holders.py` walks a checkpoint's opcodes (`pickletools.genops`) and the memo as the loader would, and calls nothing in the file: no class is looked up, nothing built. For each name not admitted it prints the strings pushed nearest before it (the attribute or key that holds it), the classes about it and the strings after it (its words). 7-799 plants a path in a scenario and reads it back so, the unpickler made to fail if called.

**Truths.** 7-796: the first action, guns fired, colours struck, parole given, saved and loaded through the server's start: by its checkpoint, the same digest, and the same after ten minutes more. 7-797: every shipped scenario (49), begun as the harbour begins it, run ten minutes and saved, holds no path and no refused name, and loads by its checkpoint as saved. 7-798: the first action begun through the harbour's start, a prisoner, saved by the driver, read by names (no path, nothing refused), taken up again from the harbour by its checkpoint, the same digest; the server's own first world keeps the place as words.

## What moves

**The shipped scenarios: nothing.** All 49, begun as the harbour begins them, were run 13 hours on the trunk and on this package, compared every ten minutes: every far vessel's position, state, done mark and first leg, and the log's lines. All 49 the same, the business on or off. The business-on ones run faster from the tiles kept (merchant-brig 399 s to 174 s; prize-home 471 to 330; the-channel-observed 202 to 116).

**Recorded passages.** None with a player's or a model's orders has the business on.

**Pins.** None moved.

**Far ships that now sail**, a player or seat seeing the difference: a trader drawn lying at the Little Road of the Havre, or lying at the anchorage of Favignana, Palermo, Portsmouth, Trapani, Syracuse, Weymouth or Torbay, weighs and sails her voyage where she lay looping; some take the ground on the way (above). The private signal is read in a ship made a King's ship by her papers. A game begun in the harbour, and a prisoner's game, load by their checkpoints where they replayed.

## Mutants

Each mend taken out in a worktree of the hash, the truths that read it run. All killed:

| mutant | killed by |
|---|---|
| no departing-anchorage filter in `_plan` | 7-790; and 7-793 |
| no `WEIGHED` wait | 7-791 |
| sixteen tiles kept | 7-792 |
| first in, first out (64 kept) | 7-792 (its eviction check, added when this one first survived) |
| no table by papers | 7-795 |
| the header from the followed hull | 7-796 |
| the place a path in the server's first world | 7-798 (its first-world check, added when this one first survived) |
| the place a path in a world taken up | 7-798 |
| the names' reader forgets the memo | 7-799 |

## The trunk merged

The trunk was merged at 93cf624c (nineteen ship files, the corvette Diana; package 126's second part, its `captains.py`, `runner.py` and `scripts.py`). One conflict, in `docs/dev/TuningNotes.md`, where both sides had added a section at the end: both kept whole, 126's second part first, then this package's. No code conflicted; `captains.py` was not touched here. Nothing of this package counts the ship files: 7-797 takes every scenario the trunk ships, as it finds them. The tiers were run on the merged hash.
