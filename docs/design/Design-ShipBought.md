# Design note: a ship bought, and the player's ship changed in play (package 60)

Written before anything of package 60 is built, as the brief asks (`docs/dev/M7-WorkPackages.md`,
"Package 60 (from M7b)", re-briefed by the lead on 2026-11-09; the owner approved on 2026-11-10
that this note be written now, while 74 is open, and the building waits for 74's close and the
lead's gate on this note). It is in package 83's shape, read against the code: the ground as it
stands with the seam named (§1), then one section for each thing the brief says the note must
settle (§2 to §9), each ending in **a ruling** the builder can build from or **a question for the
owner** that can be answered in a sentence, then the steps (§10), what was rejected (§11), and the
questions and the open items gathered (§12).

The ground read: the trunk `claude/dreamy-darwin-d77nty` at `ef0446c` (this branch was cut there);
spec M7b §21g and §21h; decisions 62, 63 and 66 (`docs/DesignProposal.md`); the notes of 74
(`Design-Prizes.md`) and 83 (`Design-OneWorld.md`) with their postscripts; and 74's unmerged work,
read only, on `claude/pkg-74-step3` at `073f4e7` (the scratch branch, steps 6 and 7) and
`claude/pkg-74` at `b14433a` (step 5). Line numbers are the trunk's at `ef0446c` unless a branch
is named. Where I proved a claim, I did it with small scripts in a scratch folder outside the
repository, against a scratch world (84's frigate with the brig X promoted beside her,
`tests/test_crews.py` `_frigate_and_the_brig_x_on_the_sea`); none of them is committed, and each
result is quoted where it is used.

**On the figures.** Every figure below is marked where it stands: a page on file named beside it;
FROM MEMORY where I recall it and no page on file gives it; JUDGEMENT where it is a choice. The
sources on file that speak to this package are few and are read in §7: Steel's *Naval
Architecture* (1805, the 1822 printing) for a hull's price a ton by contract; Steel's *Rigging
and Seamanship* (1794) for cordage's; the Regulations of 1806 (1808 printing) for how the service
surveys and values a ship it buys; Falconer (1780) for "owner" and "ordinary"; Röding (1794) for
the ship broker; Luce (1884, late) for the bill of sale.

**The player's pronoun.** The game's role of "the player" is written "he" as decisions 62 and 63
write it; he is a character of the game, not the owner. Of the owner and the lead, nothing here
needs a pronoun.

## 1. The ground as it stands: one hull meaning two things

### 1.1 The seam in one paragraph

Since package 84 the world is one world of hulls (`World.hulls`, `freesail/core/world.py:713`),
and the player's ship is one hull among them. But **one object, `World._own`, means two
different things at once**, and nothing in the code tells them apart: it is *the game's first
hull* (the hull the scenario built, which keeps the sea, the game's seed and scenario, the save's
first block and the director's station) and it is *the player's ship* (the hull whose captain is
the player's person, which the far brains, the sets, the prize code and the readers mean by "the
player's"). As long as the player can never change ship, the two are the same hull and the
confusion costs nothing. This package is the first that makes them differ, so the first ruling
of the note (§2) is to part them: the game's first hull stays fixed for the whole game, and a new,
separate pointer says which hull is the player's ship now.

### 1.2 What lives on `World._own` today

Read from the code, each with its line:

- **The player's ship by name.** `World.players` (`world.py:556-560`) returns `_own` itself:
  "The player's own hull (her ship's; `hulls[PLAYER_ID]`)". It is read by about twenty-five
  readers (counted in §9.1).
- **The sea.** `World.sea_vessels` (`world.py:562-566`) is `_own.vessels`: the one `Vessels` of the
  whole sea is kept as a per-ship field of the first hull (`hulls.py:65-75`, `"vessels"` among
  `PER_SHIP_FIELDS`, with the comment "the `Vessels` of the sea for the followed hull, a `HullView`
  of every far body but her own for another"). Every other hull's `vessels` is a `HullView` whose
  `sea` is the sea (`crews.py:174-175`).
- **The game's seed, scenario and streams.** `seed`, `scenario` and `rng` are per-ship fields too
  (`hulls.py:69-72`): the game's own on `_own`, a copy on every other hull (`crews._crew_scenario`).
- **The save's first block.** `World.save` (`world.py:2555-2561`) writes the save "with the
  player's own hull current", so the top of the save (`seed`, `scenario`, `ship_ref` at
  `world.py:2575`, `standing_orders`, `agents` at `world.py:2588`, `agent_journals`, `stations`)
  is hers, and `_hull_blocks` (`world.py:2627-2631`) writes every *other* hull in `hulls`,
  skipping `_own`. The replay rebuilds the game from that first block (`replay.py:127-146`,
  `build_world`: `World(seed, scenario, ship_factory(ship_ref))`).
- **The id "the ship".** Her id is `own_id()` (`hulls.py:207-213`), the constant `PLAYER_ID = "the
  ship"` (`world/ships.py:67`). Her vessel on the sea, the "shadow", is made under that id
  (`ships.py:1811-1870`, `Vessels.player_shadow`, "the one vessel the sea never moves"). About
  thirty places compare a vessel's id with `PLAYER_ID` to mean "the player's ship" (§9.1).
- **The `""` key of the acts.** A station's act on the first hull is journaled with no `ship` key
  (`core/acts.py:118-126`, `hull_id_of`: `""` when the id is `PLAYER_ID`), and replayed onto
  `World.players` (`acts.py:145-155`, `act_target_of`).
- **The director's station.** `director_hull` (`agents/director.py:1482-1488`) keeps the
  director's station and log on `World.players`, and the harness writes a station's notes into
  the director's log through it (`agents/harness.py:2663`).
- **Who is never put to sleep.** `crews.crewed` (`crews.py:554-565`) leaves `World.players` out of
  the hulls the cap may demote: "the player's own hull is awake always".

The inputs keyed `""` are a different key from the acts' and need no change: an input names a
hull only when the order was given to a hull that is not the followed one (`world.py:2001-2002`),
and `""` means "the followed hull" (`replay.py:302-308`, `acts.target_of`), which the replay
re-creates at its tick because `follow` is itself journaled.

### 1.3 The roads already built that this package uses

- **The player aboard another ship as her captain** (`--seat captain --ship X`, package 82,
  item 2): `ui/console.py:1057-1090` `aboard_ship` writes a `driver.left` line in the first hull's
  log and follows the other hull; `knowledge.player_hull` (`world/knowledge.py:753-784`) reads
  the last `driver.left` line to say which hull he is captain of; `players_person`
  (`knowledge.py:817-848`) is that hull's `people.captain`. This is the nearest thing to a change
  of ship today, and it leaves `World.players` alone. It is a starting arrangement only: the
  flag is given once, at the start.
- **One function for every change of a person's hull**: `movement.put_aboard`
  (`world/movement.py:1031-1151`), with the drivers following the player's body into the hull
  (`_drivers_follow`, `movement.py:1154-1185`, a consequence line `hull.followed`, never an input).
- **The prize master's road** (74, `world/prizes.py:858-881` `_put_master`): `Registry.rehome`
  (`world/people.py:603-613`) gives him the prize as his home, `people.command_passed_to`
  (`people.py:981-999`) makes him her captain, her captain's station is bound to him, and his
  harness or seat follows him into it (`prizes.py:508-529`, `_station_follows`). The muster swap
  (`prizes.py:387-467`: `remuster`, `_draw_prize_crew`, `_take_out`) moves sailors between two
  musters.
- **Journals keyed to the person by his name** (`agents/journal.py:95-145`, `World.
  person_journals`), so they go wherever he goes.
- **The purse's ledger** (`world/places.py:474-520`, package 53b): `receive`, `pay_to`, `owe`,
  each line with its cause.
- **A ship laid in ordinary** at a port (`world/regimes.py:74-85` `put_in_ordinary`, and the
  director's `ship "<name>": in ordinary at <port>`, `agents/director.py:836-848`).
- **Whose service the ship is in** (`world/service.py:90`, `service_of`): King's, privateer or
  merchant, from her papers, her captain's role, or her wardroom file.
- **On 74's branches**: the valuation (`prize_court.py` `valuation`, lines 144-169 on
  `claude/pkg-74-step3`: tons burthen from the displacement, £8 a ton for a merchant hull and £12 for
  a man of war's, both FROM MEMORY in 74's `data/business.yaml` lines 130-131, worn two per cent a
  year by JUDGEMENT, the guns by the hundredweight, the stores nothing); and the new command after a
  court martial (`court.py` `new_command`, line 673 on the same branch), a director's world order
  `command: a new command for <person>: the <description> "<name>" at <port>` that **writes a new
  scenario file** for either driver and changes nothing in the running world.

### 1.4 Two experiments, and what they showed

**The raw re-pointing.** In the scratch world I set `World._own` to the brig X's hull and the
drivers to follow her, the plainest reading of "the player's hull re-pointed". Four things broke
at once:

1. `players_person` answered the brig's own master, Mr Bradley, not Captain Bowen: the person
   does not travel by re-pointing; he has to be moved.
2. The first tick never returned: a `RecursionError` in `crews.py:175`, `HullView.player_shadow`
   calling itself, because the sea (`sea_vessels`) is now the brig's `HullView`, whose `sea` is
   itself. The sea cannot follow the player's hull without being moved off it.
3. The save's first block became the brig's (`ship_ref: data/ships/merchant-brig.yaml`), and the
   frigate vanished from the save altogether (she was no longer `_own` and held no station).
4. The replay of that save rebuilt a different game: its log's digest differed from the played
   one, and its `players` was a new hull "the ship" built from the brig's file.

**The split.** In a second scratch run I left `World._own` where it was, made `World.players` read
a new field naming the player's hull (the first hull when it is unset), wrote the save's first
block from `_own`, and made the change by hand at a tick: his person put aboard the X by
`put_aboard`, rehomed to her by `Registry.rehome`, her command passed to him, the new field set,
a line in both logs. Then I gave an order, ran ten minutes, saved, and replayed the save with the
same change made again at the same tick. **Both logs replayed to the same digests, the first
block was the frigate's as it always was, and the replay's player's person was Captain Bowen
aboard the X.** The same two hand changes, applied to the suite's tests of the save, the
checkpoint and the player aboard another ship (`tests/test_replay.py`, `tests/test_checkpoint.py`,
`tests/test_aboard_another.py`, with the kept saves of `tests/fixtures/saves/`), are reported in
§9.4.

The second run also found what the brief did not know (§1.5, item 1): **the old ship, left with
no plan, is lost from the world within a minute.**

### 1.5 Where the brief is wrong about the code, or did not know

1. **The old ship is not "a vessel of the world thereafter" by itself.** Once she is not
   `World.players`, `crews.crewed` (`crews.py:554-565`) counts her among the hulls the cap may
   demote; the switch measures each hull's distance only for a vessel with a far brain
   (`crews.py:850-855`), so the old ship, which has none, is "beyond the range" though she lies
   alongside, and is put to sleep at once (`crews.py:882-884`; the scratch run: "Amazon asleep at
   far detail: beyond the range of the ship"). Asleep, her far body is moved by its plan, and a far
   body with an empty plan is *done* (`ships.py:862-866`); `release_done` (`crews.py:702-714`) then
   discharges her company out of the registry and drops her hull from `World.hulls`. In the scratch
   run, a minute after the change her hull was gone from `World.hulls`, her company was empty, and
   yet she was still `World._own` and still the sea's `Vessels.own`. The note rules this (§4).
2. **"The boat's loads taking their time as the prisoners' do" (step 2): the prisoners take no
   time.** `take the prisoners aboard` (`orders/prize.py:181-203`) checks the boat is ready and
   moves them at once (`prizes.py:1238-1270`): the words say "by the boat", the clock does not.
   The hands' move must have its own loads and time (§6).
3. **"Listings at a port by its size and trade": no port has a size.** Neither `data/ports/*.yaml`
   (Falmouth's file: `id`, `name`, `nation`, the roads, the market, `dockyard: {kind: chandlers}`,
   powder, the pool) nor `data/business.yaml` carries one. The listings need a new key (§7.4).
4. **"The purse and the cargo in the director's truth if they are not": they are**, since package
   52 (`api/readings.py:4206-4212`, the player's; `4279-4285`, every other hull's, awake or
   asleep). Nothing to add.
5. **"No road makes another hull the player's own" is true, but there is half of one**: the
   `--ship` flag (§1.3) already makes him another hull's captain at the prompt without touching
   `World.players`, and `player_hull` already distinguishes "the ship he is captain of" from "his
   own". The act of §2 must end that arrangement cleanly when it is in force (§2.3, item 7).
6. **"The prize master's seat carried, made general"** is right as far as the seat goes, but the
   prize master keeps a *home* to go back to (`prizes.py:517-529`: `home = h._home or ...`), and the
   player changing ship must not: the new ship is his home. The act clears it (§2.3, item 5).
7. **The time of a valuation on 74's branch reads `spec.built`** (`prize_court.py:132-141` on
   `claude/pkg-74-step3`), but **no ship file has a build year** (no `built:` or `launched:` key in
   `data/ships/*.yaml`), so every hull is valued as ten years old (`age_years_unknown`). Ten files
   mention copper (the boats, the brig, the cutter, the frigate and others), none with its years.
   The condition term (§7.2) has to bring its own figures.
8. **74's note cites the purchase of a prize at three fourths as "the Captain's art. XXXI"**
   (`Design-Prizes.md` lines 27 and 724). On the page on file (the Regulations, 1808 printing,
   OCR lines 1975-1990, p. 28) art. XXXI sits in the articles addressed to the commander in chief
   ("the Commander in Chief when he orders a prize Ship to be purchased"), well before the
   Captain's. The figure is right; the attribution is for the lead to check.

## 2. The change of the player's ship, one act (item 1)

### 2.1 The design in one paragraph

**The game's first hull stays where it is for the whole game; a new field says which hull is the
player's ship.** `World._own` keeps everything that is the game's (the sea, the seed, the
scenario and its streams, the save's first block, the director's station, the id "the ship" and
the `""` key of the acts that mean *that hull*), and never moves. `World.players` stops reading
`_own` and reads `World._players`, the id of the player's ship, falling back on `_own` when the
field is unset, which it is in every game until the first change and in every save and checkpoint
written before this package. The change itself is **one function** (`take_up`, §2.3), which
moves his person into her, carries his seat, passes her command to him, sets `_players`, and says
so in both ships' logs. It is called by one order of his person's, `take command of the "Fly"`,
which is an input of the journal like every order, so the replay repeats the act at its tick by
repeating the order, and no new kind of input is needed. What makes a ship his to take (bought,
or given him by the director's word) is a fact set earlier by its own input; the act only reads it.

### 2.2 Why the split and not the move

The move (re-pointing `_own` itself) would have to carry the sea, the game's scenario, seed and
streams, and the save's first block with it, rewrite what the replay builds the game from, and
leave the old ship holding the id "the ship" that thirty places read as "the player's" (§1.4,
the first experiment). The split moves none of these: the first hull keeps her identity and her
role as the game's keeper, the player's ship is whatever hull the new field names, and every
older save, in which the field never appears, reads exactly as it did (§1.4, the second
experiment). The cost of the split is that every reader of "the player's ship" must be read and
sorted into one of two kinds, *the player's ship now* or *the game's first hull*; §9.1 sorts all
of them.

### 2.3 What the act does, in order

`take_up(world, person, hull, *, settle, why, by)`, a new function (JUDGEMENT on its home: a small
module `freesail/world/command.py`, beside `movement.py`, which it calls; the builder may put it in
`movement.py`). With `old = world.players`:

1. **The checks** (refused in words, nothing changed): §2.5.
2. **His person into her**: already aboard her (the check), so `put_aboard` is not called again;
   `world.registry.rehome(person, hull.id)` (`people.py:603-613`). A person whose id is taken in her
   company is told apart by his old home after a colon (`captain:the ship`); `command_passed_to`
   and the records read the id as it stands after the move, as 74's prize master's do
   (`prizes.py:868`).
3. **Her command his**: `hull.people.command_passed_to = person.id`, so that `People.captain`
   (`people.py:984-999`) answers him before her own master or captain; her `captain` station bound
   to him (`stations.bind("captain", person, quiet=True)`, as `prizes._bind_captain`); her rules
   captain stood aside at his hand, as he stands aside for the player under `--ship`
   (`tests/test_aboard_another.py`: `hull.captain.aside`); her far brain, if she had one, dropped
   (`vessel.brain = None`), since the player's ship is awake always.
4. **Her own master or captain** (the person her file made to command her) stays aboard as one of
   her people under him, his role unchanged, until §4 or §6 settles him (ashore with the seller at
   a sale, or kept by the player's order). JUDGEMENT: the act moves no one but the player's person.
5. **His seat, if he has one** (`--seat officer` and the like): moved to her captain's station
   with **no home kept** (`s.move_to(hull, captain_station(world=hull), None)`), where the prize
   master's road keeps one (`prizes.py:526-529`). A harness cannot hold him: a model at his own
   station makes `players_person` None, and the act is then refused (§2.5).
6. **The player's ship re-pointed**: `world.__dict__["_players"] = str(hull.id)`.
7. **The `--ship` arrangement ended**, where it stood: `player_hull` answers `world.players`
   whenever `_players` is set (its scan of `driver.left` lines, `knowledge.py:766-784`, stands only
   before the first change). Since the flag is given at the start alone, no `driver.left` line can
   come after the act.
8. **The drivers' follow**: the drivers already follow his body into her (`_drivers_follow`,
   `movement.py:1154-1185`). If the owner has since followed some third hull by hand, the act
   leaves the owner's eye where it is (decision 62's line between play and the owner's eye).
9. **The old ship settled** by `settle` (§4): sold, laid in ordinary or laid up, or left to her
   senior officer under an intent; in every case **her far body given a plan before the act
   returns** (§4.2), since a far body with none is lost within the minute (§1.5, item 1).
10. **Said in both logs**: one notable line `ship.taken_up` in hers ("Captain Bowen takes command of
    the Fly; the Amazon is laid up at Falmouth.") and one in the old ship's ("Captain Bowen leaves
    the Amazon for the Fly; the command devolves on Mr Ryan" where she keeps a company), with data
    `{person, ship, from, settle, by}`. The kind is placed in the knowledge table (`REACH`, the
    deck's; `tests/test_knowledge.py` walks every kind and would fail without it).

The act returns the line of hers, which the order that called it gives as its outcome.

### 2.4 Journaled, and replayed at its tick

**Ruling.** The act is journaled **by its cause**, which is always an input already: the player's
order `take command of the "Fly"` (§2.6), at the captain's prompt or from his seat, an order like
every other in `World.inputs`. What made her his to take came earlier by inputs of its own: his
`buy the ship "Fly"` (§5.4), or the director's world order giving her (74's `command:` form given in
play, §5.5), which a director's station gives as its `order` act (`core/acts.py`) and a replay by its
acts gives again. The replay gives the same input at the same tick after the same count of inputs
(`replay.py:149-277`), the act runs again inside it, and the state after it is the same; the second
experiment (§1.4) proved this for the two logs, the first block and the person. **No new input
kind**, and so nothing new in `replay._give` (`replay.py:302-388`) for an older save to meet.

**What the save's first block is afterwards: exactly what it was.** The game's first hull's seed,
scenario, `ship_ref`, standing orders, the stations seated on her, her journals and her bindings
(`world.py:2555-2611`), whether she is still the player's ship or not. The builder changes one
line: `World.save` writes the first block with `_own` current, not `self.players`
(`world.py:2560`). The new ship's block is in `hulls` (`world.py:2627-2649`) as any hull's, once she
holds a station or a journal; with neither, the replay makes her again from the inputs as the
switch and the seat do now. **For the reader** only, the save carries `"player_ship": "<hull id>"`
beside `"hulls"` when `_players` is set, read by nothing at a load; left out while it is unset, so
that every save of a game with no change is the same bytes as before (JUDGEMENT).

**The checkpoint** pickles the World's dict, the new `_players` field with it; a checkpoint
written before this package has none and loads with the class default (`None`: the first hull),
as every field added since 33a does (`replay.py` head, "every new field on a class it holds has a
plain class default").

**The `""` key of the acts keeps its meaning: the game's first hull** (`acts.py:118-126` writes it
for `PLAYER_ID`, which is that hull's id for ever). The builder changes `act_target_of`
(`acts.py:145-155`) to give an act keyed `""` to `world.__dict__["_own"]` where it gives it to
`world.players` now. For every save without a change the two are one hull, so every recorded
passage replays as it did; after a change an act of the old ship's stations goes to the old ship,
and an act on the new ship is keyed by her id, as every other hull's is.

**Ruling (§2, item 1).** The player's ship is `World._players` (a hull id; unset means the first
hull); `World.players` reads it; the act `take_up` sets it with the person, the seat, the command
and the settlement of the old ship, said in both logs; it is journaled by its cause and replayed
by its cause; the save's first block, the acts' `""` key, the sea, the seed and the director stay
the first hull's; older saves and checkpoints, which never set the field, load and replay as they
did.

### 2.5 The refusals

Refused in words, nothing changed, each a sentence the builder can use:

- **She is not his to take** (§5): "The Fly is not yours: she is her owners'; buy her first, or
  have her given you." / "The Fly is the King's; she is given by an order, not taken."
- **He is not aboard her**: "You are aboard the Amazon; go aboard the Fly first." (He is moved
  by the boat or a waterman, as now; the act never moves him across the water.)
- **Another holds her captain's station**: a model, or the player's own seat already there under
  another person: "Her captain's station is held; the Fly has a captain who is not yours to
  displace." A rules captain holds nothing and stands aside (§2.3, item 3).
- **He is a prisoner**, on parole or confined (`captive.captive_person`, `captive.py:147-162`;
  `is_captive`): "You are a prisoner of the *Bellone*; you can take command of nothing."
- **An observed world** (`World.observed`): there is no ship of the player's to leave.
- **The old ship commands a set or is a member of one** (`squadrons`): refused in step 1 with the
  words "The Amazon leads the squadron; shift the broad pendant first" (JUDGEMENT; carrying a
  set's command to another hull touches fifteen places in `squadrons.py`, §9.1, and is left for
  a later step; see §12.2, item 3).
- **The old ship's settlement cannot be made** (§4.3): she is under way with no officer to leave
  her to, or not in a port for laying up: "The Amazon has nobody to leave her to; bring her to
  an anchor first."

### 2.6 The order

`take command of the "Fly"` (and `take command of her` aboard her; `take her up as my ship` and
`shift into the Fly` as synonyms in `data/vocabulary.yaml`), with an optional tail for the old
ship: `..., and lay the Amazon up` / `and leave the Amazon to Mr Ryan to <intent>` / nothing,
when §4's default for his relation applies. The grammar's object is a ship by name, read as the
boat's orders read one (`orders/boat.py:150`, `world/orders.py:306` `hull_named`). JUDGEMENT on
the words: "to take command" is the period's phrase for a King's officer and serves the owner and
the master as well.

## 3. What travels with the person, and what is the hull's (item 2)

### 3.1 What travels

- **His person**: the one `Person` of the registry, rehomed (§2.3, item 2); his skill, his
  outline, his place and his record (74's `Person.record` on `claude/pkg-74-step3`, the career's
  memory) are his object's and go with it.
- **His seat**, where he has one (§2.3, item 5), and the captain's prompt where he has none: the
  prompt is his person's (decision 62), which `players_person` finds through `player_hull`, which
  now answers the new ship.
- **His journal**: journals are kept by the person's name on the World (`World.person_journals`,
  `agents/journal.py:121-145`), so his is the same object aboard the new ship; her station's name
  for it (`hull.agent_journals["captain"]`) is re-pointed to it the first time her captain's
  station reads it (`journal_of`, `journal.py:95-117`). The old ship's `agent_journals["captain"]`
  keeps pointing at his journal, which is harmless (it is read only where a station is bound to
  him); the builder may drop it at the act.
- **The things he keeps**: the registry's things whose keeper is his person (a letter, the
  captain's papers he carries) go with their keeper as they do now.
- **His followers, by name**: never moved by the act itself (§2.3, item 4). They go by the roads
  that exist: the boat with the persons named (`send the boat to the "Fly" with Mr Ryan and the
  coxswain`, `orders/port.py:146`), each put aboard by `put_aboard`; and their home is changed by
  step 2's order (§6), which rehomes each person it moves to the new ship as the act rehomes him.

### 3.2 What is the hull's and stays

Each is a per-ship field of the hull (`hulls.py:121-147`) and stays with her, unless the sale
settles it (§5.4):

- **Her purse** (`places.Purse`): the money aboard is the ship's account, her owner's (the
  scenario's own words, `places.py:475`: "the captain's or the owner's"). It stays, except where
  he is the owner of both ships, when the balance is carried by the ledger (§5.4).
- **Her hold**: the cargo stays in her; sold with her at a sale, at the market price of the day
  (§7.3), unless he lands and sells it first by the market orders.
- **Her papers** (`places.Papers`, `places.py:689`): the chart, the epitome, the almanac, the price
  lists. They stay (JUDGEMENT; but see the owner's question Q2, §12: in the period the master's
  own epitome and instruments were commonly his own).
- **Her stores** (provisions, water, powder and shot): stay, and are valued with her at a sale
  (§7.2).
- **Her reckoning** (`navigation`): hers. The new ship's reckoning is her own; at anchor in a port
  it is fixed by the port's known position anyway.
- **Her standing orders** (`standing`): her book stays, written for her sail and her watch; the
  player gives his orders again aboard the new ship (a book file named in the scenario can be read
  into her by the order that reads one).
- **Her bindings** (`stations`): stay, but for her captain's station, which the act binds to him.
- **Her muster's hands** (`ship.extra["crew"]`): hers until step 2's order moves them (§6).
- **Her log**: hers. From the act the drivers show the new ship's log (the followed hull's); the
  old one keeps everything up to the act and whatever her people do after it.
- **The chart marks** (`World.chart_marks`) are the world's, not a hull's, and are untouched.

**Ruling (§3, item 2).** His person, his seat or prompt, his journal, his record and the things he
keeps travel with him by the act; his followers by name travel by the boat and step 2's order,
never by the act. Her purse, hold, papers, stores, reckoning, standing orders, bindings, muster and
log are the hull's and stay, settled only by a sale as §5.4 rules; the chart marks are the
world's. **Question for the owner (Q2):** should a master's own books and instruments (his epitome,
his almanac, his quadrant) go with him to a new ship, as they commonly did, or stay with the hull
as the game's papers do now?

## 4. The old ship thereafter (item 3)

### 4.1 Three settlements

The order, or the director's word, names one; where it names none, the default is by the
player's relation to the old ship (§5.2):

1. **Sold** (the owner's sale, §5 and §7): she passes to her buyer. Where the buyer is the port's
   yard or a broker, she becomes a listing of the port (`for_sale`, §7.4) at the price the yard
   asks, her owner the buyer; where the director has made a buyer, his. Her people who are not moved
   by step 2's order are paid off and go ashore at the port (`movement.go_ashore`'s road, their
   whereabouts the port's), her hands with them (her muster cut to none, as the far prize's muster
   is cut to its counts, `prizes.fill_far_prize`, `prizes.py:922-946`). Her hull is laid up at the
   port's anchorage (`regimes.put_in_ordinary`, `regimes.py:74-85`) until the business or the
   director commissions her (JUDGEMENT: the business's traders' knobs commission a laid-up merchant
   hull as a trader after a draw of days, as they commission a nation's ships in ordinary).
2. **Laid in ordinary, or laid up**: she lies at the port's anchorage with no company and no intent.
   For a King's ship this is the ordinary of Falconer (1780, ORDINARY, OCR l. 13147-13154: "the
   establishment of the persons employed by the government to take charge of the ships of war,
   which are laid-up in the several harbours adjacent to the royal dock-yards. These are principally
   composed of the warrant-officers of the said ships, as the gunner, boatswain, carpenter,
   deputy-purser and cook, and their servants"); for a merchantman the same regime in the code,
   said "laid up". JUDGEMENT: a King's ship laid in ordinary keeps her warrant officers aboard as
   Falconer says and pays off the rest; a merchantman laid up keeps her mate and a ship-keeper.
3. **Left to her officer under an intent**: decision 63's devolution, made standing. Her senior
   officer commands her by her captain's authority with the intent the order gives (`leave the
   Amazon to Mr Ryan to sail for Plymouth`), her far brain made with that intent and her rules
   captain sailing her by it (`prizes._give_intent`'s road, `prizes.py:612-650`), said in her log
   ("the command devolves on Mr Ryan"). This is the settlement for a King's officer shifted by an
   order (§5.5) and for an owner who keeps the old ship working (a second vessel of his).

**The defaults** (JUDGEMENT): an owner's old ship, *laid up* at the port unless the order sells her;
a King's officer's old ship, *left to her senior officer* under her standing intent or the
director's (the Admiralty appoints her next captain; until then the first lieutenant commands); an
owner's captain cannot leave his owners' ship but by their word (§5.3), and their word names the
settlement.

### 4.2 What the act must do for her in every case

The two experiments (§1.5, item 1) say that a hull which is no longer the player's ship and has no
far brain is put to sleep at once and lost within the minute. So the act, before it returns:

- **gives her far body a plan**: the anchor at the port for 1 and 2 (`put_in_ordinary` sets
  `plan = [("anchor", port.id)]`, `regimes.py:78`), her intent's legs for 3 (the brain's). A far body
  with an empty plan is *done* (`ships.py:862-866`), and `release_done` (`crews.py:702-714`)
  discharges a done body's company and drops her hull. The anchor plan is the floor: no settlement
  leaves her without one;
- **lets her far brain be made**: `prizes._give_intent` refuses a brain to a vessel whose id is
  `PLAYER_ID` (`prizes.py:619-620`, "the player's own hull is awake always"), which after a change is
  the *old* ship's id; the test must become "is the player's ship now" (§9.1);
- **keeps the first hull in `World.hulls`**: `release_done` must never drop `_own`, whatever her
  far body does (she holds the sea and the save's first block; a sunk or burnt first hull stays a
  hull asleep, her body done, her company whatever the event left);
- **measures her by her own position**: the switch reads each body's distance only where it has a
  brain (`crews.py:850-855`), so a laid-up hull is "beyond the range" alongside the player and
  sleeps; it must read every crewed body's distance by its position, so that a ship laid up beside
  him sleeps or wakes by the cap like any other (her *sleeping* is fine; her being thought far away
  is not).

### 4.3 When she cannot be settled

Refused before anything moves (§2.5): under way with no officer aboard to leave her to; laid up
or sold away from a port's anchorage (there is no anchorage to lay her up at); her company a
prize crew of hers away in a prize, where leaving her would leave them without their ship
(JUDGEMENT: refused with the words "the Amazon has a prize crew in the Bellone; recall them first").

**Ruling (§4, item 3).** The old ship is settled by the act as sold, laid up (in ordinary for the
King's), or left to her senior officer under an intent, the default by the player's relation; the
act always gives her far body a plan, lets her brain be made, keeps the first hull in the world's
hulls whatever befalls her, and the switch measures her by her position.

## 5. Ownership (item 4)

### 5.1 What the code knows today

Nothing of owners. No vessel, hull or scenario has an owner, a price or a for-sale state (no
`owner` field in `world/ships.py`, `business.py`, `dealings.py` or `core/world.py`; the market
sells goods). What it does know is **whose service she is in** (`service.service_of`,
`service.py:90`): a King's ship, a privateer or a merchantman, read from her papers
(`papers: {service: ...}`), her captain's role, or her wardroom file (a captain or a commander
commands a King's ship, a master a merchantman). Falconer (1780, OWNER, OCR l. 13237): "the
proprietor of a ship, by whom she is freighted to the merchant for a sea-voyage."

### 5.2 The owner, as a fact of the vessel

**Ruling.** A vessel gains `owner: str` (a far body's field, and the player's ship's through her
vessel), saved with the vessel as every field since 75 is (left out while empty, so that no
saved form moves). Empty means **by her service**: the Crown for a King's ship; "her owners" for a
privateer (the adventurers who fitted her out, under her letter of marque) and for a merchantman;
**except the player's own first ship when she is a merchantman**, whose owner with none written is
his person (JUDGEMENT: the spec's goal, M7b §21g, is the player trading in his own cutter, and every
merchant scenario on file names no owner; see Q5).
Otherwise it is a person's name (the player's person's, when he owns her) or words for a firm
(`Fox and Company`). The scenario says the player's ship's owner by `papers: {owner: the captain}`
(or a name); the director by a tail on the ship order (`..., owned by Messrs Fox`); a sale writes
it. Read by one function, `owner_of(world, vessel)`, which answers the words and whether it is the
player's person.

**The player's three relations to a ship**, read from her owner and her service:

- **The owner** (her owner is his person): she is his to sell, lay up or leave to her mate; he may
  buy another with her purse and take command of any ship he owns.
- **The owner's captain** (a merchantman or a privateer not his): he commands her for her owners.
  She is not his to sell, and her purse is theirs. He may take command of another of theirs, or of a
  ship given him, only by their word (the director's `command:` form, §5.5, standing for the
  owners' letter). He may not buy a ship on their account. FROM MEMORY: a master's power to sell
  his owners' ship was a power of necessity alone (a ship damaged in a distant port, the owners not
  to be reached), and the courts looked hard at it; the game leaves it out.
- **The King's officer** (her service the King's): **the Crown's ship is not her captain's to sell or
  buy.** The Regulations on file say the purchase of a ship for the service is the commander in
  chief's, and only on an absolute necessity or an order (Regulations of 1806, 1808 printing,
  pp. 27-28, OCR l. 1908-1966: "He is not to purchase, nor to hire, any Ship or Vessel to be armed and
  fitted as a Ship of War, or as a Tender to the Fleet; unless there be an absolute necessity for
  his doing so, in order to replace a Ship or Vessel that may have been lost, and there be not time
  for him to represent such necessity to the Lords Commissioners of the Admiralty"). A King's
  officer takes command of another ship only by an order (the director's `command:` form, §5.5), and
  of a prize only as Falconer has it, by putting his officer in her "until a captain is appointed by
  the commander in chief" (ENGAGEMENT, quoted in `Design-Prizes.md`): 74's prize master, not the act.
  He buys nothing with the purse of a King's ship but stores, under the rules 86 built.

A privateer's captain is an owner's captain of her adventurers, and her owner when the scenario
says so (a captain who fitted her out himself).

### 5.3 What each may do, as a table

| | sell her | buy another | take command of another | his purse |
|---|---|---|---|---|
| owner | yes, `sell the ship` | yes, `buy the ship "Fly"`, with her purse | of any ship he owns; of one given him | carried to the new ship by the ledger |
| owner's captain | no | no | of his owners' or one given him, by their word | stays: it is the owners' |
| King's officer | no | no | by an order (the director's `command:`) alone | stays: it is the ship's account |

Each "no" is a refusal in words that says why ("The Amazon is the King's ship; she is not yours
to sell." / "The Lively is her owners'; you command her for them.").

### 5.4 The purse, the hold and the papers at a sale

**Ruling** (JUDGEMENT throughout, the figures in §7):

- **Selling** (`sell the ship`, the owner aboard her in port, a buyer there: the yard, a broker, or a
  buyer the director has made): the price (§7.3) paid into her purse by the buyer (`Purse.receive`,
  the cause "the Amazon sold to Mr Pascoe, broker, at Falmouth"); her hold's cargo sold with her at
  the port's market price of the day unless landed first; her stores valued in the price; her papers
  stay with her. **A bill of sale** written as a paper of the sale (a new paper of
  `data/papers/papers.yaml`, the instrument "by which a vessel is transferred to a purchaser", Luce
  1884, OCR l. 44295-44296, a late source for an old instrument), and her register's change of owner
  said in the line (FROM MEMORY: a British ship's register was indorsed on a sale under the
  registry Act of 1786; not on file).
- **Buying** (`buy the ship "Fly"`, the owner in port where she is listed, within a boat's pull or
  alongside): the price paid from his present ship's purse (`Purse.pay_to`, the cause "the Fly
  bought of her owners at Falmouth"), refused below nothing as every payment is; the Fly's owner
  becomes his person; her hold, papers and stores are hers and come with her; her own master and
  people stay aboard until he moves or discharges them (§6, §4.1).
- **His purse carried**: at the act, where he is the owner of both ships, the old ship's balance is
  paid out of her purse and into the new ship's in one pair of ledger lines with the cause ("carried
  to the Fly"), so that the money he trades with goes with him and the old ship's ledger closes at
  nought (or at what he leaves for her keepers, named in the order). Where he is not her owner,
  nothing is carried.

**Question for the owner (Q1):** a captain's own money (his prize shares, his savings) is not
modelled apart from the ship's purse: 74's prize money goes into the captor's purse. When a King's
officer or an owner's captain leaves a ship, should the game give the person a purse of his own
that goes with him (the captain's share and his pay in it), or leave all money as the ship's until
the career of M8?

### 5.5 How 74's two later uses take the same act

1. **The new command after a court martial** (74's `court.py` `new_command`, line 673 on
   `claude/pkg-74-step3`): today the `command:` form writes a scenario file. **Ruling:** where the
   ship it names already lies at the named port in this world (a hull or a far body of that name
   there), the form gives her to the person in play instead (a field on the vessel, `given_to`, the
   person's name and the tick, said in the port's news and the person's record), and nothing else;
   he goes aboard by the boat and takes command by `take command of the "Sparrow"`, which calls the
   act with the settlement the form's tail names for his old ship (or none: a captain who lost his
   ship has none). Where she does not lie there, the scenario road stands as 74 built it. The form
   is doubted as every director's order is (74's `command_doubt`), and the play log never shows it.
2. **A prize the player takes command of himself**: allowed to an owner and a privateer's captain
   who owns her or whose owners have given him leave by the form (`take command of the prize`, the
   prize lying within a boat's pull and possessed), calling the act with his old ship *left to her
   senior officer* by default; **refused to a King's officer** (the prize is the commander in chief's
   to give, §5.2), who may be given her by the director's form when she is purchased for the service.
   The act shares the prize master's machinery (`Registry.rehome`, `command_passed_to`,
   `_bind_captain`, `_station_follows`) and differs from `_put_master` (`prizes.py:858-881`) in one
   thing: no home is kept, so he does not go back.

**Ruling (§5, item 4).** A vessel has an owner (by her service when none is written); the player is
her owner, her owner's captain or the King's officer as her owner and service say; only the owner
sells, buys and carries his purse; the owner's captain and the King's officer change ship by an
order (the director's `command:` form given in play), and the King's officer takes a prize into the
service by the prize master and the commander in chief, never by the act. 74's new command and a
prize taken up by an owner or a privateer call the same act.

## 6. The company moved between two hulls (item 5)

### 6.1 Persons, by the roads that exist

The named few (her officers, the coxswain, a servant, a passenger) are persons of the registry and
go by `put_aboard` (`movement.py:1031`), carried by the boat (`send the boat to the "Fly" with Mr
Ryan and the coxswain`, `orders/port.py:146-238`), by a waterman in port, or alongside. What is new
is their **home**: today a person put aboard another hull is a visitor there and keeps his home
(`movement.py:1073-1113`). Step 2's order rehomes each person it moves (`Registry.rehome`, as the
act rehomes the player), so that he belongs to the new ship's company, her watch bill and her
muster's roles find him, and his station there is his own and not a visitor's voice.

### 6.2 The hands, as a count, by one order

**The order:** `transfer the people and the hands to the "Fly"` (everyone of the old ship's company
the order may move: §6.3), `transfer twenty hands to the "Fly"`, `transfer six able seamen and four
ordinary to the "Fly"` (a number by name of rating, the ratings of the muster's
`data/crew/` tables), `transfer Mr Ryan and twelve hands to the "Fly"` (persons by name and hands by
count in one order). Given aboard either ship, of the other within a boat's pull
(`movement.BOAT_BETWEEN_NM`, `movement.py:88`, a mile) or alongside, both ships his to man (§6.3).

**The move**, made general from 74's muster swap: the sailors chosen from the giving muster as
`prizes._draw_prize_crew` chooses (`prizes.py:428-451`: fit, at no work, by id; the order's ratings
first), taken out of the giving muster and its quarter bill (`_take_out`, `prizes.py:454-467`),
added to the receiving muster, each muster re-made (`remuster`, `prizes.py:387-414`: the routine
re-pointed, the quarter bill reckoned afresh, the battery's word dropped) and its watches dealt
again (`_watches`, `prizes.py:417-425`). These are 74's functions; the builder lifts them into a
shared place (`movement.py` or the new `command.py`) with 74's callers kept, once 74 has closed.

**The boat's loads take time** (new; §1.5, item 2: the prisoners' move takes none). JUDGEMENT: a
ship's largest boat carries twelve men and their bags a load (no boat file carries a capacity;
`data/ships/boat-cutter-23.yaml` and the rest give the hull and the oars only); a load is pulled
across, cleared and pulled back in a quarter of an hour within two cables, half an hour at a mile;
alongside, the hands go across by the gangway in a quarter of an hour for the whole. The men in the
boat are in neither muster while she is away (the boat's own list, as `send_boat`'s passengers are,
`dealings.py:2978-2986`), and each load is said in the receiving ship's log as it comes aboard.
The order is refused while the boat is away on another errand, as every boat order is.

### 6.3 When it is refused

- **Either left unable to be worked.** No figure in the code says how many hands a ship needs to be
  worked (no `least`, `min_crew` or the like; the files give a `complement` and the hands per
  station, `data/ships/cutter.yaml:786-797`). JUDGEMENT: **she can be worked by one watch at her
  sail-handling stations**, half the hands her file puts at the forecastle, the afterguard, the
  waisters and the tops (the cutter: 8 + 10 + 6 = 24, so 12; the topsail schooner's by her file), and
  never fewer than four. The words say how many she wants: "The Amazon would keep nine hands; she
  wants twelve to be worked. Transfer fewer, or lay her up first." **Except** where the old ship is
  being sold or laid up by the same order or before it: a ship laid up needs only her keepers
  (§4.1), so `transfer the people and the hands to the "Fly", and lay the Amazon up` moves everyone
  but the keepers.
- **The receiving ship cannot berth them.** JUDGEMENT: never more than her file's complement and a
  half (a merchantman crowded for a short passage); "The Fly berths sixty; she has fifty-two."
- **The company is not his to move.** An owner moves his own ship's company to his own ship. A
  King's officer moves a King's ship's company only to another King's ship and only by an order
  (the director's form); the men are borne on her books and turned over by the Admiralty's order,
  FROM MEMORY, not on file. Merchant hands go as men who sign the new ship's articles, said in the
  line ("twenty hands sign the Fly's articles"; FROM MEMORY, the articles of a merchantman were for
  the ship and the voyage; JUDGEMENT that they all sign).
- **Beyond a boat's pull**, the boat away, either ship under way and not hove to, a prisoner giving
  it, an observed world: refused as the boat's orders refuse.

**Ruling (§6, item 5).** Persons move by the roads that exist and are rehomed by step 2's order;
the hands move as a count by one order, drawn and re-mustered by 74's functions made shared, the
boat's loads taking time by the JUDGEMENT figures above; refused where either ship would be left
with fewer than one watch at her sail-handling stations (unless she is laid up or sold by the same
order), where the receiver would hold more than a complement and a half, where the company is not
his to move, and where a boat order would be refused.

## 7. The price (item 6)

### 7.1 The period's way of valuing a ship, on file

The Regulations say how the service values a ship it buys, and it is the shape the game's price
should have: a survey by the trades, **a rate a ton for the hull and a value for each article**
(1806, 1808 printing, pp. 27-28, OCR l. 1927-1958: the vessel is to be surveyed and valued by "two
of the most intelligent and best qualified Carpenters, and two Smiths ... her Masts, Yards, iron
work, &c. and two of the best qualified Masters, two Boatswains, and two Sailmakers, to assist in
surveying and valuing her rigging and sails. And if the Vessel be found to be in good condition
... and may be purchased at a fair and equitable price", the survey and appraisement to show "the
rate per ton for the Ship, and the number, weight, quality, rate and value of each Article"); and
for a prize, three fourths of the appraised value paid at once and a fourth reserved (art. XXXI,
l. 1975-1990), which 74 built.

What a ton was worth, on file:

- **A new man of war's hull by contract, £19 10s a ton burthen.** Steel, *Naval Architecture*
  (1805; the 1822 printing on file), "Form of a Contract" for a brigantine for the Navy Board,
  29 May 1804, p. lxvi (OCR l. 44743-44750): "after the rate of nineteen pounds ten shillings for each
  ton; namely, for so many tons as the said brigantine shall measure, not exceeding 382 tons" (the
  fraction after 382 lost to the OCR), "the full and entire compensation". The hull built, launched
  and delivered afloat (l. 44719-44723), without her masts, rigging and stores, which the yard
  supplied apart.
- **Cordage, £41 10s a ton** to the government in 1792 (Steel, *Rigging and Seamanship*, 1794,
  vol. I, OCR l. 7999-8000), the figure for rigging wanting.
- **What a used hull sold for: nothing on file.** 74's figures stand: £8 a ton for a merchant hull
  and £12 for a man of war's, both FROM MEMORY (74's `data/business.yaml`, lines 130-131 on
  `claude/pkg-74-step3`), worn two per cent a year (JUDGEMENT). Beside Steel's contract, £12 is
  about three fifths of a new hull's price a ton, which is a fair reading for a used hull (JUDGEMENT,
  for the lead to keep or move with the Steel figure written beside 74's in the data).

At those rates, by 74's function with its ten years' wear (no file has a build year, §1.5 item 7),
measured on the files: **the cutter** (78 tons burthen by her displacement) about £500 as a merchant
hull, her guns £144; **the topsail schooner** (155 tons) about £990 as a merchant hull, no guns; **the
merchant brig** (304 tons) about £1,940. The spec's example of the director's listing, "for sale at
£900" (M7b §21g, item 3), is a schooner just under her valuation.

### 7.2 The valuation with her condition

**Ruling.** The price is 74's `valuation(world, vessel)` (one function for the court, the yard, the
broker and the listing), with **a term for her condition** in the Regulations' shape, each article
apart:

- **the hull** at the rate a ton by her kind, worn by her years (`wear_per_year`), and less her
  damage: her far record's shot holes and holes below the water (`crews.write_damage`,
  `crews.py:625-650`; for an awake hull the same counts read from her parts), each hole below the
  water at the cost of its stopping at the port's yard and each above at a tenth of it (JUDGEMENT);
- **her spars and sails wanting**: each spar wrecked and each sail blown out at the port's dockyard
  list (`data/ports/<port>.yaml` `dockyard.items`; Falmouth's, all JUDGEMENT in that file: a topmast
  £40, a yard £25, a suit of sails £25 the hundred square metres, cordage a shilling the fathom),
  taken off the price;
- **her copper**: a coppered hull's copper at its years (a new key `coppered_year` on the vessel or
  her file; none has one, §1.5 item 7), worth a sum a ton of her burthen new and nothing at eight
  years (JUDGEMENT: £2 a ton new, FROM MEMORY of the order of the cost of coppering, unverified);
- **her guns** by the hundredweight (74's), **her stores** at the port's market price of the day
  (74 counts them nothing; at a sale they are worth what the market would give: JUDGEMENT), her boats
  in her hull's price (JUDGEMENT).

The survey is the yard's (a King's yard's officers or the port's shipwrights), its sum written in
the bill of sale's lines as the Regulations' appraisement is: the rate a ton and each article.

### 7.3 The margins

- **Selling to the yard or a broker**: the valuation less the buyer's margin. The ship broker is
  the period's trade on file (Röding, 1794, vol. II, SCHIFFSMÄKLER, OCR l. 50186-50206: "Engl. Ship
  broker"; in my translation, "a broker in sea towns, whose business is to procure freights for
  masters or owners, to clear ships in and out, to collect freights and to render the owners an
  account of everything, less their brokerage"), with no rate given. JUDGEMENT: the broker pays
  **a fifth under** the valuation (he must hold her and sell her again), the yard **a quarter under**.
- **Buying a listing**: the asking price is the valuation with the seller's margin, drawn under the
  seed between a tenth and a quarter over (JUDGEMENT), and **treating** (the errand's "treat for her",
  §8) brings it down by a draw toward the valuation, never under it (JUDGEMENT).
- **The broker's own commission** on a sale he arranges between the player and a third party:
  JUDGEMENT two and a half per cent of the price, paid by the seller (FROM MEMORY of the usual
  brokerage on ships, unverified).
- **A prize condemned** by 74's court and not purchased for the service is listed at her port at her
  valuation, sold by the captors' agent (FROM MEMORY: prizes were sold by auction by the agents), so
  that an owner may buy a prize.

All the rows go in `data/business.yaml` under a block `ship_sales:`, each with its source or its
mark beside it, as 74's rows are.

### 7.4 The listings at a port

No port has a size (§1.5, item 3). **Ruling:** a port's file may carry `ships_for_sale:` (how many
at most, the kinds by the business's `trader_kinds`, the chance a day of a new one); a port without
the key takes the default by its dockyard's kind (JUDGEMENT: a King's yard none for private buyers
but the condemned prizes; the chandlers' and the merchants' ports one or two, drawn at the start
under the seed and renewed at a chance a day; a port with no dockyard none). A listing is a far
body of the port's anchorage in the regime "laid up" (`put_in_ordinary`'s road, §4.1), her owner
"her owners" or a named seller, `for_sale: {asking, by}` on her vessel. The director adds one by a
tail on the ship order (`ship: a topsail schooner "Fly" of britain at Falmouth, for sale at £900`,
M7b §21g), doubted as any order (an asking price under half her valuation or over twice it is
doubted; JUDGEMENT), never shown in the play log. **A reading of the ships for sale** (`the ships for
sale`) answers from what the player's person knows: what he has seen ashore at the port, what the
errand brought back (§8), what a broker's letter said; never from the truth.

**Ruling (§7, item 6).** One valuation for every price (74's), in the Regulations' shape (a rate a
ton for the hull, each article apart), with her damage, her spars and sails wanting, her copper,
her guns and her stores in it; Steel's £19 10s a ton (1804) written beside 74's £12 as the new
hull's ceiling; the broker's, the yard's and the seller's margins and the commission JUDGEMENT in
`data/business.yaml`; listings by a new port key with a default by the dockyard's kind, and the
director's `for sale at` tail.

## 8. The errand ashore by a named person, and the director's part (item 7)

### 8.1 The errand

**The order:** `send <person> ashore to <errand>`, three errands to begin: `to ask what ships are for
sale` (or `to look for a ship`), `to treat for the "Fly" [up to £950]`, and `to find a broker`. It
is the boat's errand of today (`Dealings.send_boat`, `dealings.py:2952-2991`) with a person and an
errand word: the person goes in the boat as a passenger goes now (`_passengers`,
`dealings.py:2993-3029`, refused for the captain, who goes by his own word), the boat's time is the
boat's, and what he does ashore is done while the boat waits at the quay. The order is refused where
the boat order is refused today (not in port, under way, the port hostile, the boat away), and for
a person who cannot go (sick, at work, a prisoner).

**What he finds, from the port's facts first** (the rules, read when the boat leaves the quay to come
back, so that what the world holds by then is what he finds):

- **asking**: every listing of the port (§7.4) by her description, her name, where she lies, her
  asking price and her seller; and a condemned prize for sale there;
- **treating**: the named listing's price brought down by the draw toward her valuation, never
  under it, and never over his limit; the price **held for him a day** (JUDGEMENT), so that `buy the
  ship "Fly"` within the day pays the agreed price; refused ashore where she is not for sale;
- **finding a broker**: a broker of the port, made as a person of the port's place the first time
  (a name drawn under the seed from the port's nation's lists, `data/crew/names.yaml`; JUDGEMENT),
  who from then on can be named in a later errand (`to sell the Amazon by Mr Pascoe`) and through
  whom the yard's and the broker's margins of §7.3 apply.

**What he reports, in his own words, when the boat returns**: one line of his (the words' kind, as
`say` lines are, `person.spoke` with him as the speaker) on the quarterdeck where the player hears
it, in the form a table of `data/director/` gives (JUDGEMENT on the words: "Mr Pengelly reports a
topsail schooner, the *Fly*, lying in the inner road for sale at nine hundred pounds, her owners
Messrs Fox; he could hear of nothing else."). **What the player's person learns** is kept on his
hull's dealings as the price lists are (`Dealings.price_lists`, `dealings.py:177`): the listings
known, with the tick and who brought them, which the reading `the ships for sale` reads (§7.4).

### 8.2 The director's part

The director's part is to put facts in the world before the boat comes back; the finding, the
treating, the sale and the move are the rules' and the player's (M7b §21g, "neither side needs a
script"):

- it sees the boat's going in the log and the port and the purse in the truth (the purse and the
  cargo are in it already, `api/readings.py:4206-4212`; §1.5, item 4);
- it may place a listing by the ship order's tail (§7.4), make a broker or a seller as a person
  (`person: make "Mr Pascoe", a ship broker of Falmouth, ...`, `agents/director.py:797-803`), send a
  merchant's message, and **speak as the person on the errand** when the boat returns (`say as Mr
  Pengelly: "..."`, `director.py:893-894`): **ruling** (JUDGEMENT), where the director has said a line
  as him between his going and the boat's return, that line is his report and the rules' line is not
  written; where it has not, the rules' line is. Either is a line of the play log in his words; the
  director's order never is (truth 7-488).
- it may not complete a sale, move hands, credit the purse for a hull, or make a ship the player's
  own; it may give a King's officer or an owner's captain a ship by the `command:` form (§5.5), as
  the Admiralty or the owners would, doubted as every form is.

The answer is deterministic in the replay: the boat's return is a consequence of the boat's order,
the rules' finding reads the world as the replay has rebuilt it, and the director's `say as` and its
listing are world orders of the journal.

**A model at the purser's station** (M7b §21g, item 4: "optional later") is not this package's; the
errand is written so that a seated purser would answer in the director's place by the same rule
(his line before the boat's return is the report), when stations as data seat one.

**Ruling (§8, item 7).** `send <person> ashore to ask what ships are for sale | to treat for the "X"
[up to £n] | to find a broker`: the boat's errand with the person; found from the port's facts as
they stand when the boat leaves the quay, by the rules; reported in his words when the boat
returns, the director's `say as` him in the meantime standing for the rules' line; what he learns
kept as the price lists are and read by `the ships for sale`; the director places listings, brokers
and the words, never the sale.

## 9. The risks (item 8)

### 9.1 Every place that assumes the player's hull never changes

Found by reading every reader of `World.players`, of `World._own` and of `PLAYER_ID` (the string
"the ship") in `freesail/`, and the places that write or compare the word "the ship" as a vessel's
id. Each is sorted into one of three kinds, which is the builder's whole work list for step 1:

- **P, the player's ship now**: must read `world.players` (or its id, by one new function
  `players_id(world)`), so that it follows the change;
- **F, the game's first hull**: must read `world.__dict__["_own"]` (or `PLAYER_ID` as the first
  hull's id), so that it does not move;
- **I, an identity**: compares a vessel's id with "the ship" to mean *that vessel*, the first hull's
  shadow; correct as it stands.

**How each row was sorted** (the gate's addition (b)): a row marked **[run]** was proved by one of
the scratch runs of §1.4, §9.2 and §9.4 (the behaviour seen, not only read); every other row was
sorted by reading alone, and the builder proves it by a test at the step that changes it.

For every save with no change, P and F are one hull, so every one of these edits leaves every older
game as it was.

*The core*

| Where | What it assumes | Kind |
|---|---|---|
| `core/world.py:556-560` `World.players` | the player's ship is `_own` | P: reads `_players` **[run]** |
| `core/world.py:562-566` `sea_vessels` | the sea is on the player's hull | F (it is, and stays) **[run]** |
| `core/world.py:597` `follow "the ship"` | the player's ship by name | P (`players`, as now) |
| `core/world.py:2560` `save` | the first block is the player's | F **[run]** |
| `core/world.py:2627-2631` `_hull_blocks` skips `_own` | the first block holds the player's | F (as now) **[run]** |
| `core/acts.py:118-126` `hull_id_of` | `""` is the player's hull | F (writes as now) |
| `core/acts.py:145-155` `act_target_of` | `""` goes to `players` | F: to `_own` |
| `world/hulls.py:207-213` `own_id` | the first hull's id is the player's | I |
| `world/hulls.py:300-310` `Hull.parent`, `326-331` `is_followed` | `_own` is the fallback with nothing followed | F (the observer's) |

*The player's person, his place and the drivers*

| Where | What it assumes | Kind |
|---|---|---|
| `world/knowledge.py:753-784` `player_hull` | his own hull is `players`; `--ship` by the first hull's log | P, with §2.3 item 7 **[run]** |
| `world/knowledge.py:817-848` `players_person` | his hull's `people.captain` | P (through `player_hull`) **[run]** |
| `world/knowledge.py:879-917` `players_senses` | the fallback with nothing followed is `players` | P |
| `world/movement.py:1154-1185` `_drivers_follow` | none (follows his body) | nothing to change **[run]** |
| `world/boats.py:745` going aboard "the ship" | `players` | P |
| `world/orders.py:306-349` `hull_named` ("the ship", "us") | `players` | P |
| `world/orders.py:1342-1349`, `1866` the player's ship in the world orders | `players` | P |
| `api/readings.py:2679` the followed reading | `players` | P |
| `api/readings.py:4234` the truth's vessels | `players` | P |
| `ui/console.py:1057-1090` `aboard_ship` | the `driver.left` line in the first hull's log | F (the line's place; §2.3 item 7) |

*The director*

| Where | What it assumes | Kind |
|---|---|---|
| `agents/director.py:1482-1488` `director_hull` | the director's station lives on `players` | **F**: its station, its log and its holder stay on the first hull, so that the director's log is one log for the game |
| `agents/harness.py:2663` a station's note into the director's log | through `players` | F (follows `director_hull`) |
| `api/readings.py:4152` `director_readings` (the truth; the player's block at `4190-4212`) | "the player's first" is the current hull's | **P**: the player's ship's block read with `players` current, since the director's station is no longer on her |

*The sea, the sleep and the far bodies*

| Where | What it assumes | Kind |
|---|---|---|
| `world/ships.py:1209-1222` `players_current` | the shadow's hull is `_own` | I (the shadow is the first hull's vessel) |
| `world/ships.py:1811-1870` `player_shadow`, "the one vessel the sea never moves" | the first hull's vessel is the player's and is never moved by the sea | I for the id; **the "never moved" must become "while she is the player's ship"**, and the player's ship's own far body must be brought to her truth every tick (§9.2) **[run]** |
| `world/ships.py:769-781` `_target_of` (`target_id == PLAYER_ID`: the target at `world.position`) | a chase of "the ship" is a chase of the player | I: a chase of the first hull's vessel; and a brain that means "the player" must target `players_id` (§9.3) |
| `world/ships.py:1024-1032` a carrier's `to_ship` leg | goes to `players` | P |
| `world/ships.py:1986-1995` `_deliver_to_hulls` | `players` | P |
| `world/ships.py:2165` `_player_id` | the player's id is "the ship" | P: `players_id` |
| `world/ships.py:862-866` a far body with no plan is done | every crewed hull but the player's has a plan or a brain | the act gives the old ship one (§4.2) **[run]** |
| `world/crews.py:554-565` `crewed` leaves `players` out | the player's hull is the one never demoted | P, **and** the first hull never released (§4.2) **[run]** |
| `world/crews.py:702-714` `release_done` drops a done hull | the first hull is never done | F: never drop `_own` **[run]** |
| `world/crews.py:850-855` the switch's distance by the brain only | every crewed far body but the player's has a brain | read every crewed body's position (§4.2) **[run]** |
| `world/crews.py:429` the sky with nothing followed | `players` is the observer's | F |
| `world/crews.py:174-175` `HullView.player_shadow` | the sea is not the player's hull's view | F (stays true under the split; it recursed under the move, §1.4) **[run]** |

*The squadrons, the signals and the far brains*

| Where | What it assumes | Kind |
|---|---|---|
| `world/squadrons.py:175` `commander: str = PLAYER_ID`; `1204-1242` the spec's default commander and members | a set with no commander named is the player's | F at the start (the scenario's player's ship is the first hull) |
| `world/squadrons.py:521`, `578`, `704`, `992`, `1025`, `1051` `== PLAYER_ID` | the commander "the ship" is the player's | P in meaning; **refused in step 1** while the old ship commands or is in a set (§2.5) |
| `world/squadrons.py:1392-1402` `_followed_hull` (`hull is _own`) | the player's body reads her live frame | P |
| `world/squadrons.py:1405-1408` `_players_captain` | `players` | P |
| `world/ships.py:660-663` `under_orders_of` ("'the ship' for the player's"); `world/signals.py:1327` `boss == "the ship"` | "under the orders of the ship" means the player | P in meaning: a ship put under the player's orders by the director follows the player's ship; the stored word stays "the ship" for the saves, read through `players_id` |
| `world/signals.py:1394-1398` `own_id` ("her vessel's, or 'the ship'") | a World with no vessel is the player's | I (the first hull has no `vessel` field of her own; the new ship has her vessel's id) |
| `world/brains.py:723` `other_id != PLAYER_ID` (the spoken hail) | the player's ship is not spoken through the sea | P |
| `world/prizes.py:619-620` `_give_intent` refuses a brain to `PLAYER_ID` | the first hull is the player's | **P**: refuse it to `players_id` alone (§4.2) |
| `world/prizes.py:674`, `756` `prize.id == PLAYER_ID` (the player struck, the captive's channel) | the player's ship is "the ship" | **P**: else the player struck in the new ship is never taken captive |
| `combat/far_action.py:442` the guns heard at `players` | `players` | P |
| `combat/far_action.py:455-457` a far fight with "the ship" in it is "our own action" | the player's ship is "the ship" | P |
| `combat/action.py:363`, `568`; `combat/boarding.py:131-134`; `combat/small_arms.py:282-285` (`PLAYER_ID` for the hull with no vessel) | the World's own hull is the player's and has no vessel | I for the first hull; the new ship has her vessel and her id |
| `world/hail.py:390` `is_players` | `players` | P |
| `world/captive.py:942` `cartel_doubt` reads `players.position` | `players` | P |

On 74's branches, the same: `prizes.py` and `captive.py` carry more `PLAYER_ID` reads on
`claude/pkg-74-step3` (the struck player's record, the captive's home); the builder sorts them at the
step after 74 merges, by the same three kinds.

### 9.2 Found on the way: the followed ship's far body is left behind (a fault on the trunk)

Under the `--ship` road as it stands on the trunk, the ship the player is aboard (the followed hull)
is never brought up to her truth on the sea: `Vessels.tick_crews` skips the followed hull ("the
followed hull's tick is the World's own", `ships.py:1792-1800`), and `_tick_vessels` brings only the
first hull's shadow up to hers (`world.py:1645-1648`). Measured in the scratch world, with no change
of ship at all (`--ship X`, the royals set): her far body stood **934 metres** from her truth after
five minutes and **3,803 metres** after twenty, growing at her speed, while the shadow stood at
nought. Every other ship's brain, lookout and hail reads her far body, so for them she is where she
was. It is the same after the act (4,763 metres after twenty-five minutes in the second experiment).
**Ruling:** step 1 brings the player's ship's far body up to her truth every tick, as the shadow's is
(`mirror`, `crews.py`, on the followed hull or on `players` whichever is awake), and the `--ship` road
is mended by the same lines; a truth of its own (§10, 7-481).

### 9.3 What a model seated at a station sees across the change

- **At the new ship's stations** (her mate, an officer): one line of her log, "Captain Bowen takes
  command of the Fly", and from then her captain's orders are the player's; a told order is the
  captain's word (decision 63). Her captain's station held by a model refuses the act (§2.5), so no
  model is ever displaced from it.
- **At the old ship's stations**: the line "Captain Bowen leaves the Amazon for the Fly" and the
  devolution's line (decision 63, `the command devolves on Mr Ryan`) where she keeps a company; the
  senior officer, preferring a held station, holds the captain's authority with the intent the
  settlement gives (§4.1, 3). Where she is laid up or sold, a station whose person is paid off ashore
  is stood down by the handover's rule (`put_aboard`'s `seat="stands down"`, `movement.py:1074-1075`)
  in words ("stood down: the Amazon is laid up"); where step 2 moves the person, his harness follows
  him as his own station there (§6.1), not as a visitor's voice.
- **At the director's seat**: nothing moves. Its station, log and holder stay on the first hull
  (§9.1); its truth's player's block reads the new ship from the act (§9.1, `director_readings`). It
  sees the act's two lines as any line of the play.
- **A model on a hull a model holds elsewhere** (82b's): nothing, unless the new ship is in sight.

### 9.4 Older saves and checkpoints

The two edits that change what every game reads (`World.players` through `_players`, the first
block from `_own`) were made by hand in a scratch run over the suite's own proofs:
`tests/test_aboard_another.py`, `tests/test_checkpoint.py` (which loads the kept checkpoints of
`tests/fixtures/saves/`), `tests/test_replay.py`, `tests/test_hulls.py` and `tests/test_lee_ports.py`,
in one process: **all their fast tests passed** (the nine slow ones left out by the suite's tier).
This proves the split is invisible to every game with no change; it is not the builder's proof,
which is the whole suite at step 1's hash with every pin standing.

### 9.5 What the knowledge rule says of a ship he has left

**Ruling: nothing new is needed.** From the act his person is in the new ship and the drivers follow
her; the old ship's lines reach him only as any other ship's do (a hail within hearing, a letter, the
port's news, a person's word), because his senses are read where his person is
(`knowledge.players_senses`, `knowledge.py:879-917`). What he knew of her is what he wrote in his
journal and what his person heard; there is no reading of her purse, her hold or her people by
name once he has left her. The owner's `follow "Amazon"` shows her whole, as the owner's eye always
does on a hull the player holds no person in (`knowledge.py:904`, `912`), which decision 62
keeps out of play.

## 10. The steps, each at one hash (item 9)

Each step a commit or a few on the package's branch, brought onto the trunk as it stands after 74's
close, its final runs the fast tier whole, the slow tier of the touched files and the known truths
(ruff clean), its postscript below, reported to the lead at its boundary. The brief's five steps,
with this note's order inside them:

0. **This note**, gated by the lead; the §9.1 table read again against the trunk with 74 merged (74's
   `PLAYER_ID` reads sorted by the same three kinds) before a line is written.
1. **The player's ship changed in play.** First, before the act and each with its own test (the
   gate's addition (a); faults waiting whether or not a ship is ever changed): the four floors of
   §4.2 (a far body always given a plan, a brain allowed to any ship but the player's, the first hull
   never released, the switch measuring every crewed body by its position); and the followed ship's
   far body brought to her truth (§9.2) if nobody has mended it by then, proved by 7-481 either way.
   Then the split (`World._players`, `World.players`, the first
   block from `_own`, `act_target_of`, `director_hull` and the truth's player's block); every P of
   §9.1; the followed ship's far body at her truth (§9.2, the `--ship` road mended with it); the old
   ship's floor (§4.2: a plan always, her brain allowed, the first hull never released, the switch by
   position); `take_up` and `take command of the "X"` for a ship *given* him (74's `command:` form
   given in play, §5.5), with the settlements laid up and left to her officer (sold waits for step 3);
   the refusals of §2.5; the line `ship.taken_up` placed in the knowledge table. **Proves:** the act,
   its replay and the kept saves (7-480, 7-482), the far body (7-481), the old ship kept (7-483).
2. **The company moved.** `transfer ... to the "X"` with persons by name and hands by count and
   rating; the persons rehomed; 74's muster functions shared; the boat's loads in their time; the
   refusals of §6.3. **Proves:** 7-484.
3. **Owner, price and sale.** `Vessel.owner`, `for_sale`, `owner_of`, `papers: {owner: ...}` and the
   ship order's tails (`owned by`, `for sale at £n`); the valuation's condition term and the margins
   in `data/business.yaml` `ship_sales:` (Steel's figure beside 74's); the port key `ships_for_sale`
   and its default; `buy the ship "X"` and `sell the ship` among the market orders through the ledger
   with their causes, the bill of sale written, the purse carried where he owns both; the settlement
   *sold*; the reading `the ships for sale`. **Proves:** 7-485, 7-486.
4. **The errand ashore.** `send <person> ashore to ...` (ask, treat, find a broker); the broker made;
   the report in his words from a table of `data/director/`; the director's `say as` standing for it
   (§8.2); what he learnt kept with the price lists. **Proves:** 7-487, 7-488.
5. **The truths and a scenario.** `data/scenarios/ship-bought-falmouth.yaml` (the merchant cutter at
   Falmouth with a purse, a topsail schooner listed, the purser aboard); spec M7b §21g and §21h as
   built; the primer's chapter 14; `docs/dev/TuningNotes.md` (every JUDGEMENT figure of §6 and §7);
   these postscripts. **Proves:** 7-489.

### 10.1 The truths 7-480 to 7-489, a line each

- **7-480.** The player takes command of a ship given him and aboard her: his person, his seat and
  his journal go with him, her command is his, both logs say so, and `World.players` is she.
- **7-481.** The player's ship's far body stands at her truth every tick, whichever hull she is (the
  `--ship` road mended with it).
- **7-482.** A save with a change of ship replays to the same digests of both ships' logs, its first
  block the game's first hull's; every kept save and checkpoint from before loads and replays as it did.
- **7-483.** The old ship is settled by the act (laid up, sold, or left to her officer under an
  intent) and never lost from the world: her hull kept, her far body planned, her company where the
  settlement puts it.
- **7-484.** The people and the hands move by one order within a boat's pull, by loads in their time,
  each muster re-made; refused in words saying how many she wants where either could not be worked.
- **7-485.** Only an owner sells or buys: the King's ship and an owner's ship are refused to her
  captain in words; a sale and a purchase go through the purse's ledger with their causes, the bill
  of sale is written, and the purse is carried where he owns both.
- **7-486.** The price is the valuation with her condition: a hull with shot holes and spars and
  sails wanting is worth less by the yard's prices, and the broker's and the yard's margins apply.
- **7-487.** `send the purser ashore to ask what ships are for sale` finds the port's listings as they
  stand when the boat leaves the quay and reports them in his words when it returns; what he learnt is
  the reading `the ships for sale`.
- **7-488** (M7b's 99d). A director's listing by the ship order's tail, placed while the boat is away,
  is found by the purser's errand and reported in his words (or in the director's `say as` him); the
  play log never shows the order.
- **7-489** (M7b's 99c). The player sells the cutter at Falmouth, buys a listed schooner, moves his
  people and hands by one order and sails her out; the save replays across the two ships with the
  journals of the people intact.

## 11. What was rejected, and why

- **Moving `World._own` to the new hull** (the brief's "the player's hull re-pointed", read
  literally): the sea, the game's seed, scenario and streams, the save's first block and the
  director would have to move with it; the first experiment broke on the first tick and wrote a save
  that replayed another game (§1.4).
- **Swapping the two hulls' ids**, so that the new ship becomes "the ship": every reference to her by
  her own id (the brains chasing her, the sets, the letters for her, the registry's whereabouts, the
  director's seats, her own inputs and acts journaled before the change) would have to be re-keyed at
  the act and again by the replay; too many readers to find with confidence, where the split's list
  (§9.1) is finite and read.
- **A new kind of input for the change**: every road that causes it is an input already (§2.4); a new
  kind would be one more thing for `replay._give` and for older builds to meet, for nothing.
- **The change as a driver's line, as `--ship` is**: decision 62 keeps the drivers' commands out of
  play; a change of ship is the person's act by an order of the game.
- **A person's own purse in this package**: left to the owner (Q1) and to M8's career.

## 12. The questions for the owner, and the open items for the lead

### 12.1 For the owner, each answerable in a sentence (answered at the gate: §13)

- **Q1.** When a captain leaves a ship, should his own money (his prize shares, his pay) go with him
  in a purse of his own, or should all money stay the ship's until M8's career, as this note rules?
- **Q2.** Should a master's own books and instruments (his epitome, his almanac, his quadrant) go
  with him to a new ship, as they commonly did in the period, or stay with the hull as the game's
  papers do now?
- **Q3.** Is the director's word (standing for the commander in chief's order or the owners' letter)
  the only road by which a King's officer or an owner's captain takes command of another ship or of a
  prize, as this note rules?
- **Q4.** May the player, as an owner, keep his old ship working under her mate with an intent while
  he sails the new one (owning two vessels at once), as this note allows?
- **Q5.** In a merchant scenario that names no owner (every one on file), is the player his ship's
  owner, free to sell her, as this note rules, or her owners' master, who may not?

### 12.2 For the lead (ruled at the gate: §13)

1. **The split** (§2.1, §2.2): one new field, `World._players`, and the first hull kept as the game's;
   the move and the id swap rejected (§11).
2. **The act journaled by its cause** (§2.4), with no new input kind.
3. **A set's command not carried in step 1** (§2.5): refused while the old ship commands or is in a
   set; which package carries the broad pendant to another hull.
4. **The fault of §9.2 on the trunk** (the followed ship's far body left behind under `--ship`): mended
   in step 1 as this note rules, or by a small package of its own before 60.
5. **74's files touched after its close**: `prizes.py` (`_give_intent`'s test, the muster functions
   shared, §6.2), `court.py` (the `command:` form's branch in play, §5.5), `prize_court.py` (the
   condition term in the one valuation, §7.2).
6. **The attribution of art. XXXI** in 74's note (§1.5, item 8).
7. **The ports' data**: a new optional key `ships_for_sale` in `data/ports/*.yaml` (§7.4).
8. **The JUDGEMENT figures**, all to `docs/dev/TuningNotes.md` at their steps: the margins (a fifth,
   a quarter, a tenth to a quarter over, two and a half per cent), the boat's load (twelve men, a
   quarter to half an hour), the least to work her (one watch at the sail-handling stations, never
   under four), the most she berths (a complement and a half), the copper (£2 a ton new, nothing at
   eight years), the price held a day.

## 13. The gate (2026-11-10)

The lead accepted the note at the gate on 2026-11-10. The owner's answers and the lead's rulings
stand here; where they differ from the text above, this section governs.

### 13.1 The owner's answers to §12.1

- **Q1.** All money stays the ship's until milestone 8's career; no purse of the person's own in this
  package; an owner's purse is carried by the ledger as §5.4 rules.
- **Q2.** A master's own books and instruments stay with the hull for now (§3.2); revisit with the
  career.
- **Q3.** Yes: the director's word is the only road by which a King's officer or an owner's captain
  takes another ship or a prize (§5.2, §5.5).
- **Q4.** Yes: an owner may keep his old ship working under her mate with an intent while he sails
  the new one (§4.1, 3).
- **Q5.** Yes: in a merchant scenario that names no owner the player is her owner, free to sell her
  (§5.2); a scenario may say otherwise.

### 13.2 The lead's rulings on §12.2

1. **The split** is accepted: `World._players`, the first hull kept as the game's; the move and the id
   swap rejected as §11 argues.
2. **The act journaled by its cause**, with no new input kind: accepted.
3. **A set's command not carried in step 1**, refused in words: accepted; the broad pendant shifted to
   another hull is a later package's, on the lead's list.
4. **The fault of §9.2 is real**: the lead reproduced it on the trunk with the suite's own helper
   (`tests/test_aboard_another.aboard_x`): the followed hull against her far body 0.0 m at tick 61,
   933.8 m at tick 361 and 3,803.4 m at tick 1,261. It is said to the owner, whose word it is whether
   it is mended in 60's step 1 or by a small step sooner, since he tests with that road. Step 1 mends
   it if nobody has by then, and proves it by 7-481 either way (§10, step 1).
5. **74's files touched after its close** (`prizes.py`, `court.py`, `prize_court.py`): accepted, after
   74 closes and not before.
6. **Art. XXXI's attribution** (§1.5, item 8): the lead tells 74.
7. **The ports' key `ships_for_sale`**: accepted, optional, with the default by the dockyard's kind
   (§7.4).
8. **The JUDGEMENT figures** are accepted as marked, each to the tuning notes at its step. By decision
   66, each price and rate in the data says which year's picture it is (Steel's contract of 1804, the
   Regulations of 1806, a FROM MEMORY figure's war years), since a game begins on any day of 1792 to
   1825 and a price is one of the things a year changes: the builder files the year beside the figure,
   and the valuation takes no date yet; a scaling by date is not this package's.

### 13.3 The lead's two additions, made in the text

- **(a)** The four floors of §4.2 are step 1's first work, before the act, each with its own test,
  since they are faults waiting whether or not a ship is ever changed (§10, step 1).
- **(b)** The table of §9.1 marks the readers proved by a run (**[run]**) apart from those sorted by
  reading alone, so that the builder knows which to prove.

## As built (the postscripts, step by step)

Each step's postscript says here what was built, what was taken another way and what was found.

### Step 1 (2026-11-12, built at 2370a2d)

**Built as the note says:** the four floors of §4.2, each with its test; the followed ship's far
body mirrored to her truth (§9.2: 934 m off after five minutes and 3,803 m after twenty on the
trunk, none now; truth 7-481); the split of §2 (`World._players`, `players`, `first_hull`, the
save's first block from the first hull and `"player_ship"` only when set, the acts' `""` key and
the director's station on the first hull, `hulls.players_id` for the P readers of §9.1); the act
(`world/command.take_up`, the order `take command of`, the director's `command:` form giving a ship
lying at the named port in play); truths 7-480 to 7-483. Nothing in the note had to change after
package 74 closed but its line numbers.

**Taken another way:** a ship laid up keeps her company aboard in this step, her paying off left to
steps 2 and 3; the refusal for a squadron is made also when the new ship is in a set or has ships
under her orders; the director's truth reads the player's ship only when called on the director's
own station's hull (the first hull), so that a reader of another hull reads that hull still; the
order's reply carries the line the act would have written in the new ship's log, written once.

**Found:** a ship in ordinary has no captain, so no hull can be made for her nor can she be boarded
(the test's ship is a merchant brig under an intent instead); the listings of step 3 must give a
ship in ordinary a hull another way, or list only ships with a master.

**Mended at the lead's review (2026-11-12)**, each with a test that fails on 2370a2d (the tuning
notes give the measures): the act's own line kept for a direct call (step 3's purchase calls it
so); the boat that brought him across pulls home and is hoisted in; her late master gives her up
in his own name before the command passes (§2.3, item 3: never the player "standing aside"); the
`command:` form doubted for a ship of another nation, an enemy's or a prize not condemned (§5.5:
the director's word stays the road); a chase of `PLAYER_ID` steers for the first hull's body after
a change, and the player's ship is the witness of another's fire by `players_id` (§9.1); "under
the orders of the ship" is the player's ship by her id, and a set of his is refused in words
after a change (§2.5: a set's command is not carried to another hull yet, and every reader of a
set takes `PLAYER_ID` for the player's); a kept hull asleep wakes within the range (§4.2); a weigh
waiting on the furling of a coming to anchor is no longer belayed (a fault of every ship's, met
at the act); truth 7-482 with an order after the act and a checkpoint between.

**The one exception to "every save from before replays as it did"** (the lead's ruling): a save
or checkpoint from before this step that was played aboard another ship than the first (`--ship`,
or `follow` of another hull) parts from its game as played, since the followed ship's far body
stood off her hull then and stands at it now (§9.2), so the ships about her see another sea: the
lead's trunk checkpoint agreed at 600 ticks and parted by 3,600. No legacy mode keeps the drift;
the save of this build carries `followed_body`, and the loader says so in words of a save without
it whose inputs show it was played aboard another ship (`replay.followed_body_words`).
