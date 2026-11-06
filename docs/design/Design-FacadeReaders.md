# Design note: the hull façade's readers (package 97)

Written before the mends are merged, as the brief asks (`docs/dev/M7-WorkPackages.md`, the
waves row of package 97, and the two findings it rests on: "Package 82b, items 2 to 5 ... as
merged" and "Package 65, step 2 ... as merged", with 65's "Found on the way" (a) and (e) in
`docs/dev/TuningNotes.md`). The audit's list first (§2), then the two mends and why each reader
takes the one it takes (§3), the guard (§4), what is booked and not taken (§5), and what moves
(§6). Postscripts say what was built and what was taken another way.

## 1. The fault in one paragraph

84's World keeps one ship's fields on a `Hull` (`hulls.PER_SHIP_FIELDS`) and installs each as a
property of `World` that reads `world.own`, the hull whose block is running (`World.as_hull`),
else the followed hull. A **reader** is an object of one hull, or a function about one hull,
that reaches her fields through a **World handle** (`self.world.people`, `world.stations`,
`log_of(world)`, `station_spot(world, ...)`): it answers for whichever hull is current when it
is read, which is hers only while her block is running or she is followed. Inside another
hull's block (an order, a tick, a hail, a word of the other hull's) or under `follow`, it reads
the other hull's. A crewed ship's hull never had the fault in her systems, for `crews.
adopt_hull` walks her graph and makes every reference to her building World her Hull
(`_rebind_world`); **the player's own hull was never walked**: `World.__init__` builds her
`People(self)`, `Stations(self)`, `Dealings(self)` and the rest with the World itself.

The recorded passages run one hull's block at a time with the player's ship followed, so the
fault is latent in every pin.

## 2. The audit: every reader of a per-hull field through a World handle

Found by reading every holder of a `world` back-reference (`grep self.world`, 28 modules), every
`as_hull` site (17), every function that takes a World and is reached from another hull's block,
and by two probes on the trunk at `eabf20f`: (a) a differential, the player's hull's systems read
at home and inside the brig X's block (the frigate and the brig X promoted beside her, the
fixture of `tests/test_crews.py`); (b) an instrumented run of the 23 test files that build more
than one hull, recording every per-ship property of the World read from a method of an object
bound to the World while another hull was current (the tally in §2.4).

### 2.1 The player's own hull's systems, built with the World

| # | Reader (its `world`) | Belongs to | May run in | Reads wrongly today | Mend |
|---|---|---|---|---|---|
| 1 | `world/stations.py` `Stations` (`world`, `domain`): `holder`, `names`, `aboard`, `_file_kinds`, the bindings' lines | the player's hull | another hull's block (a hail, a `say`, a visitor's binding, `model_holds_her`, `hearing.station_spot`); outside any block under `follow` | **82b's finding**: `holder("captain")` in X's block is X's captain (Captain Pope for Captain Bowen); `holder("master")` X's master; `names()` X's wardroom | bound at construction |
| 2 | `world/people.py` `People`: the muster, `captain`, places, `ashore_words`, the stations' persons, the needs' hand, the pass of the word | the player's hull | as 1 | `self.world.ship`, `.scenario`, `.agents`, `.stations`, `.dealings` read X's | bound at construction |
| 3 | `world/places.py` `Papers` | the player's hull | as 1 (the papers' readings from another hull's order) | `world.people`, `world.scenario` X's | bound at construction |
| 4 | `world/dealings.py` `Dealings` (108 reads) | the player's hull | a port's job ticked for another hull, the boat road | `world.ship` X's in the probe | bound at construction |
| 5 | `world/reckoning.py` `Navigation` (89 reads; also `ship.extra["navigation"]`) | the player's hull | an order of another hull reading her account; the boat road | `world.ship` X's | bound at construction |
| 6 | `world/ground.py` `Ground` | the player's hull | as 1 | `world.ship`, the tide at her | bound at construction |
| 7 | `world/needs.py` `NeedsKeeper` (also made at a tick, `_tick_needs`) | the player's hull, and any hull's made at her tick | as 1 | `world.ship`, `.people`, `.log` X's | bound at construction; the late keeper made on `self.own` |
| 8 | `world/water.py` `Water` (also made at a tick) | as 7 | as 1 | `world.ship`, `.motion`, `.sea` X's | as 7 |
| 9 | `crew/health.py` `Health` (also made at a tick) | as 7 | as 1 | `world.ship`, `.people`, `.needs`, `.rng` X's | as 7 |
| 10 | `standing/runtime.py` `Runtime` (also `ship.extra["standing"]`) | the player's hull | as 1 (the readings a book reads) | `world.ship`, `.record` X's | bound at construction |
| 11 | `world/captains.py` `Captain` (82 reads) | the player's hull | `hail.model_holds_her` reads `captain.commands` from the hailer's block | `world.ship` X's | bound at construction |
| 12 | `core/world.py` the followed hull's readings view (`_readings_view`, `REGISTRY.at(self)` for the followed hull) | the followed hull | read after the block that made it, inside another hull's block (`Hull.readings` returns the view and the caller reads it after the block ends) | every row of the followed hull's read at the running hull | read in its own block: the view made over her Hull (`REGISTRY.at(self.own)`), as every other hull's already was |
| 13 | `agents/harness.py` `Harness.world` for a station seated on the player's hull with the World (the console, the runner, the doors, `seat_station`) | the player's hull | another hull's block (`add_word` from her order, `hear`, `_stations_held` from a hail); a door's thread with no block under `follow` | the harness's samples, its `agents`, its log and readings read the running hull's; a harness seated with the World while X is followed is X's (entered in her `agents`, `seated_on` hers) and reads the player's ship once the drivers follow her again | bound at construction (`self.world = world.own`): **65's file, one line; said to the lead before it is touched** |
| 14 | `agents/seat.py` `seat_world` (`PlayerSeat.world`): the World itself for the player's hull | the player's hull | as 13 | as 13 | bound at construction (`world.own`) |

Items 1 to 11 and 14 have one cause and one mend. The differential on the trunk:

    people.captain             Captain Bowen  | Captain Bowen   (the registry's view, by her id)
    stations.names             (... 'second officer', ...) | (... 'passenger')   DIFFERS
    stations.holder(master)    Mr Harvey      | Mr Hart          DIFFERS
    water / health / navigation / needs / standing / captain / dealings / papers
                               Amazon         | X                DIFFERS (each)

and on the branch every row the same both sides.

### 2.2 The director's own writes and reads, the game's one, on the player's hull

| # | Reader | Belongs to | May run in | Reads wrongly today | Mend |
|---|---|---|---|---|---|
| 15 | `agents/director.py` `log_of(world)` (`journal_of(world, DIRECTOR)`): the brief's, the budget's, the order's, the refusal's, the channel's, the reveal's lines (20 appends), and its readers (`log_lines`, `two_stories`, the doubt, the harness's notes count) | the director, kept on the player's own hull (65's step 2: "the game's one director's log ... on the player's own hull") | the followed hull's shared tick under `follow` (the seats' budgets, line 2394 of `core/world.py`), a world order given under `follow`, a door with no block | **65's finding**: the lines land in the followed hull's `agent_journals["director"]` | read in its own hull's block: `director_hull(world)` (`world.players`, her own handle) for the journal, and each append given her handle so that its act is keyed to her |
| 16 | `world/seats.py` `_log` (`director.seat`) | as 15 | as 15 | as 15 | as 15 |
| 17 | `agents/director.py` `seated`, `set_brief`'s binding of the director's station and its holder, `noticed_reveal`'s holder | as 15 | as 15 | the director's station bound on the followed hull; its holder looked for in her `agents` and not found | as 15 |
| 18 | `core/acts.py` `target_of`: an act keyed `""` (`hull_id_of`, the player's own hull) given to `world`, which reads the followed hull | the player's hull's stations and the director | a replay under `follow` | an act of hers in play is given to the followed hull in the replay (65's `_say` copy into the director's log included) | read in its own hull's block: `world.players` when another hull is current, the World itself otherwise (every recorded passage) |

### 2.3 Readers that read another hull's by a hull's handle, and are right

Listed so that the list is whole; none is changed.

- A crewed hull's systems, harnesses and seats: rebound to her Hull at `adopt_hull`; a façade
  method runs under her block (`Hull.__getattr__`).
- `hearing.station_spot_on` (65, step 2) and `reports.py`'s boat report (`root.as_hull(ship)`,
  65, step 3): read in the hull's own block; right, and after item 1's mend the block is no
  longer needed for the stations (kept: 65's lines).
- `ships.players_current`, `boats.follow_into`, `crews.far_submit`, `Vessels.tick_crews`: blocks
  made for the hull they read.
- `agents/harness.py` `_say`'s copy into the director's log under `root.as_hull(players)`: right
  in play; its replay under `follow` is item 18's.

### 2.4 The probe's tally

The instrumented run on the trunk (23 files, 8 minutes 20 seconds under four workers, every test
passed): each count a read of a per-ship property of the World made from a method of an object
whose `world` is the World while another hull was current, "block" inside another hull's block,
"follow" outside any block with another hull followed.

| Reader | Where | Reads | The road (a sample) | Item |
|---|---|---|---|---|
| `Stations` | block | 77 (`people`) | `hearing.station_spot` from another hull's `say`; `visiting_station` | 1 |
| `Stations` | follow | 1 | | 1 |
| `People` | follow 62, block 5 | `agents` 25, `ship` 15, `captain` 11, `dealings` 10, `scenario` 4, `navigation` 2 | the stations' persons, the muster read under `follow` | 2 |
| `Dealings` | block | 42 (`scenario`) | `ship_nation` from the boarding's round, ticked for the other hull (`boarding.tick` → `small_arms.kit_of`) | 4 |
| `Water` | follow | 16 (`ship` 14, `motion`, `sea`) | the director's truth (`readings._truth_action` → the `damage` row → `Water.state`) of the player's ship while X is followed | 8 |
| `Harness` | block | 1 (`agents`) | a station on the player's hull reached from another hull's block | 13 |
| `Console`, `Driver` | follow | 6 (`log`, `agents`) | the drivers' views | by design: the drivers show the followed hull (84, step 10) |
| `FarCaptain`, `Business` | follow | 16 (`vessels`) | `World.vessels` is the sea whichever hull is current | right (the sea's own property) |
| `Vessels` (the sea) | follow | 78 (`conditions`) | `strangers_of`: the far captains' perception judged "within the player's visibility" | the sea's, reading the followed hull's sky as its one visibility since 84's step 10 (the promotion's and the lookout's range are hers); not a hull's reader, not changed, noted for M8's weather at each body |

Every reader the instrumented run met is in §2.1 or §2.2 or is the drivers' or the sea's by
design; the run met no reader the reading had not listed. Items 3, 5, 6, 7, 9, 10, 11, 12, 14 to
18 were not met by these tests' roads and stand on the differential and the reading.

## 3. The mends, two roads only

**Bound to its own hull at construction (items 1 to 11, 13, 14).** The walk that rebinds a
crewed hull's graph (`crews._rebind_world`) moves to `hulls.bind_to_hull(hull, building)` and
binds the World's own hull too, at the end of `World.__init__` and of `World.__setstate__` (a
checkpoint of before), with one difference: her own `hull.world` back-reference is kept. The
keepers made at a tick for an old checkpoint (`Water`, `NeedsKeeper`, `Health`) are made on
`self.own`, the hull being ticked, not the World. A harness and the player's seat take the
current hull (`world.own`) at their seating, which is the hull whose `agents` they enter.

**Read in its own hull's block (items 12, 15 to 18).** The readings view is made over the hull
it is cached on. The director's station, holder and log are read by `director.director_hull
(world)`, the player's own hull's handle (`World.players`); its appends are given that handle,
so that the act each journals is keyed to her (`acts.hull_id_of` gives `""`); `acts.target_of`
gives an act keyed `""` to `world.players` when another hull is current or followed.

No new global and no third road: a reader holds its hull, or is read with its hull's handle.

## 4. The guard

`tests/test_facade_readers.py::test_the_guard_...` walks every hull's own graph (her systems,
her `ship.extra`, her harnesses and seat, the shared things not entered) in a world of two hulls
with a director's brief and a station seated, through `follow` and back and a checkpoint's round
trip, and fails by path on any reference to the World itself, but for the two kept by design
(a `HullView`'s `game`, the sea she views; her far body's brain, the sea's). A new system built
with `X(self)` in `World.__init__`, or a reader seated with the World, fails it loudly.

## 5. Booked to 97 by 82b, outside the waves row (for the lead's ruling, not taken)

- **The shared person ids.** Ids are post-based and shared across hulls (82b's item 5 mended the
  boat's map with `in_boat` and `aboard_her`). A reader that finds a person by id over the
  registry without her hull is the same family by another road; none was found by the audit
  outside the boat's, which 82b mended.
- **The replay's seating order.** On the transcript road, harnesses on two hulls seated in the
  same tick are seated again in hull order, not play order (`core/replay.py`; 7-394 staggers).
  Not a façade reader; left.

## 6. What moves

Nothing in a recorded passage: each mend changes what a reader answers only inside another
hull's block or under `follow`, and the recorded passages run the player's ship followed, one
hull's block at a time. The proof is the pins unmoved on the final tree (the suites' figures in
the postscript).
