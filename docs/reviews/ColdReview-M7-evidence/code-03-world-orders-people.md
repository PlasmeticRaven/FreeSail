# Code reader 03: the world-order channel, the people, the places and the ports

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read under READERS.md and CODEREADERS.md: nothing
under docs/dev, docs/design, docs/playtests or docs/gates opened; no test suite run; the only file
written is this one. The short Python commands I ran (each a few seconds: a World made with
`make_world`, one function called) are given with their output where a finding rests on them.

## 1. What it is

**Size.** Thirteen modules in `freesail/world/`, 19,943 lines:

| module | lines | what it is |
|---|---:|---|
| orders.py | 4,746 | the world-order channel: parser, performer, the "doubt" check, the rule of reach |
| dealings.py | 3,954 | one hull's dealings with the ports: the pilot and his conn, the boat's errands, the market, the yard, the crew pool |
| people.py | 1,763 | the named persons, the one registry of persons and things, the wardroom files |
| ports.py | 1,487 | the port files loaded, the market's price rule, `Ports` (the world's), shared constants |
| scenarios.py | 1,423 | the scenario file reader and writer |
| knowledge.py | 1,248 | what a person perceives from where he is (which log lines and readings reach him) |
| boats.py | 1,036 | the ship's boat as a hull of her own (manned, towing, lost) |
| places.py | 1,022 | the places aboard and ashore; `Hold`, `Purse`, `Stores`; the ship's papers |
| needs.py | 837 | hunger, thirst and fatigue of a stationed person |
| reports.py | 835 | the officer's reports and calls to the captain below; the command devolved |
| things.py | 818 | things (a packet, a letter) and who can reach them |
| books.py | 475 | books drafted: a sheet of standing orders, a manifest of bargains, a note |
| hearing.py | 299 | who heard a word said |

Comment and docstring share runs 13% to 26% a module (ports.py 26%, hearing.py 24%; counted by
tokenize and ast). 544 lines in these files cite a package number, a decision or an owner's or
lead's ruling (orders.py 147, dealings.py 107). Many docstrings carry history ("package 68; the cold
review of 2026-10-22, R-43: 24 of a small model's 29 `ship:` orders refused",
`orders.py:1273-1275`) where an explanation of the present code would serve. A newcomer is told
why each clause exists and in what order it was added, rarely what the whole does.

**Data.** `data/ports/`: 121 files, 14,306 lines, about 800 KB. `data/people/`: 12 wardroom files,
1,866 lines. `data/papers/papers.yaml`: 93 lines. `data/scenarios/`: 73 files (47 `.yaml`, 21
`.orders`), 5,135 lines. `data/director/`: 7 files, 548 lines (`aboard.yaml` and six briefs).

**Tests.** By import of these modules: orders 21 files, scenarios 48, people 11, things 10, ports
6, places 6, boats 5, knowledge 4, books 3, hearing 2, dealings 1, reports 1, needs 0 (needs is
reached through the World). The named suites: `tests/test_world_orders.py` 1,070 lines (28 tests),
`test_ports.py` 2,401, `test_knowledge.py` 2,104, `test_people.py` 971, `test_scenarios.py` 532,
`test_places.py` 292, `test_scenario_nations.py` 235; much of the rest is in
`tests/test_known_truths.py` (17,391 lines). I did not read the tests beyond the head of
`test_world_orders.py`.

**What a "world order" is.** A line of text that changes the world rather than the ship: put a
ship on the sea, append a weather system, leave a letter at a port, close a port, make a person,
put words in his mouth, find a thing aboard, take a prize, try a court martial. It is parsed by
`orders.parse` (`orders.py:243`), performed by `orders.apply` (`orders.py:255`) and journaled by
`World.world_order` / `_apply_world_order` (`core/world.py:1677-1731`) as a `world.order` line at
the "driver" actor. It is given by four doors: a scenario's `world_orders:` list at its time
(`core/world.py:1733`), the owner at the prompt as `world: <order>` (`ui/console.py:221-235, 731`;
`ui/server.py:584-604`), the director model's tool (`agents/director.py:2018`), and a replay
(`core/replay.py:309`). At the captain's prompt a line that looks like one is refused with
`REFUSAL` (`orders/__init__.py:71-83`).

**How many kinds.** 17 channels (`CHANNELS`, `orders.py:125-149`): weather, ship, message, port,
person, captain, mark, seat, unseat, aboard, say, squadron, convoy, cartel, court, command, follow.
Under them `agents/director.py:594` lists 41 forms (`WORLD_ORDER_FORMS`); the channel itself has
58 compiled regular expressions (`grep -c "re.compile(" orders.py`). The `ship:` channel alone
carries nine distinct acts (new ship, change goal, give intent, the director's "hand", ask for
full detail, make a prize, under the orders of, in ordinary, commissioned; `orders.py:752-838`),
and `aboard:` carries five (a thing found from the 34-row table, a transaction of the purse, a
freight, a thing made or moved or removed, a captive's parole; `orders.py:3350-3377`) with 25
effects (`_ABOARD_EFFECTS`, `orders.py:3689-3717`).

**What uses it in play.** Of 47 scenario files, 8 carry `world_orders:`, 15 orders in all, on 4
channels (message 4, weather 4, ship 4, aboard 3; counted by a short script over
`data/scenarios/*.yaml`). Everything else in the channel is reached by the director model, by the
owner's `world:` prefix, or by tests (the tests give `ship` 67 times, `aboard` 50, `person` 30,
`say` 16, `court` 8, `unseat` 7, `captain` 7, `port` 6). The channel is mainly the director's
instrument.

**The people, places and ports in a page.** Each hull has a `People` (`people.py:671`), a view on
one `Registry` of persons and things shared by every World of the game (`people.py:524`). A
`Person` (`people.py:330`) has a place (`places.PLACES`, 13 entries), a hull, a home, a port and a
place ashore. The world's `Ports` (`ports.py:1193`) loads every port file when the scenario names
none and the world has a chart (`ports.py:1214-1234`); each hull's `Dealings` (`dealings.py:115`)
holds her pilot, boat, price lists and jobs and delegates the port facts back to `world.ports`
(`dealings.py:236-275`). The player meets this part through the orders in section 2 below, through
readings (`the port`, `the prices`, `the people`, `the places ashore`), through the log lines
filtered by `knowledge.reaches` and `knowledge.hears`, and through the pilot's lines on arrival.

## 2. Is it reached?

### What a player can do in a port today, traced

The captain's verbs whose object is `port` (read from `load_vocabulary()`): buy, sell, demand,
enter, send the boat, take in water, take in provisions, take in powder and shot, take the pilot,
decline the pilot, hail the pilot, let the pilot take her in / out, I have the conn. Beside them
`go ashore`, `hire a waterman`, `come aboard`, `the market`, `the places ashore`. All go
`orders.handle` -> `orders/port.py:execute` (`orders/port.py:284`) -> `world.dealings`.

* **Arrive.** Under way by day within the pilot's cruising ground, the cutter is launched
  (`dealings.py:433-456`), hails within four cables (`dealings.py:578`), the player answers `take
  the pilot` (`dealings.py:676`), the pilot boards under six knots (`dealings.py:776`). He is put
  off at the anchor and paid from the purse (`dealings.py:879, 902-943`). Reached in play.
* **In port** means at anchor within `reach_nm` (2 miles by default) of the roads or mooring
  (`dealings.py:267-272`, `ports.py:1264-1272`). Every port order below is refused otherwise.
* **Go ashore.** `go ashore` -> `movement.go_ashore` (`world/movement.py:802`) ->
  `Dealings.land_person` (`dealings.py:3586`): the boat's evolution starts with him in it; at the
  quay `_land_and_take_off` sets him ashore at the quay (`dealings.py:3737-3750`). `hire a
  waterman` is a job of the port at a shilling (`dealings.py:3620-3689`). `come aboard` sends the
  boat for him (`dealings.py:3691`). Reached.
* **Buy and sell.** `buy 20 tons of tin` -> `port.execute` (`orders/port.py:352-372`) -> one of
  three methods: `trade` for one bargain from aboard (`dealings.py:2276`), `trade_together` for
  several (`dealings.py:2375`), `trade_list` when the player stands at the market in person
  (`dealings.py:3769`, via `movement.market_way`, `world/movement.py:488`). A fourth door is
  `give the book "<manifest>" to the boat` (`world/books.py:444-475`) -> `trade_list`. The price
  is the port file's base times a season factor, a war factor of 1.5 and a supply factor of 1% a
  ton net bought or sold, recovering a seventh a day (`ports.py:333-339, 410-437`). The purse is
  debited at once; the goods arrive when the boat comes back (`dealings.py:3320-3341`) or by the
  lighter job (`dealings.py:2795-2815`). The prices must first be fetched by sending the boat
  ashore (`dealings.py:2294-2298`). Reached; see finding R1 for a bug on this path.
* **Repair.** There is no repair in port. `demand a topmast from the yard` (`dealings.py:2529`)
  is a job that, when due, adds one spare to the booms (`dealings.py:2773-2777`); the ship's own
  people then shift it. Water, provisions, cordage and a suit of sails are likewise stores
  (`dealings.py:2747-2772`). Nothing in the dockyard touches the hull's condition, shot holes or a
  leak; `grep -i "repair\|careen\|refit"` over `data/vocabulary.yaml` finds only the carpenter's
  `caulk the seams` (line 1584), a shipboard order. A new boat for one lost is a two-day job
  (`dealings.py:2492-2527`).
* **Recruit.** `enter six able seamen` -> `Dealings.enter_hands` (`dealings.py:2612`): the
  bounty paid, the port's pool decremented, a `recruits` job; when due `_muster_recruits`
  (`dealings.py:2817`) appends new `Sailor`s. The pool is never replenished
  (`pool["hands"] = have - taken`, `dealings.py:2658`; `grep crew_pool` finds no other writer).
  Reached; see finding R2 for a bug.

### Port data read by nothing in play

Keys counted over the 121 files with a short script; readers by grep over `freesail/ tools/`.

| key | in files | read by |
|---|---:|---|
| `datum` | 116 | nothing (`load_port`, `ports.py:663-770`, never asks for it) |
| `tide.establishment` | 121 | nothing; the master's tide comes from `data/tides/establishments.yaml` through `world/tide.py`, a second table of the same fact (Falmouth 5h 15m in both) |
| `tide.leave_on` | 121 | nothing (only `enter_on` is read, `dealings.py:2043`) |
| `market.currency` | 121 | stored in `Market.currency`, read by nothing |
| `pilot.words.tide` | 124 rows | nothing: `pilot_words` and `answer` read channel, marks and anchorage only (`dealings.py:2066-2104`) |
| `mooring.deep_draught_ft` | 52 | `Port.mooring_for` (`ports.py:601`), called only by `tests/test_ports.py:261-262` |
| spot `depth_fathoms` / `bottom` | 209 / 110 | stored in `Spot.depth_m` / `bottom`; `Spot.depth_words` (`ports.py:363`) has no caller; likely nothing reads them (grep on `anchorage.depth`, `spot.bottom`, `.depth_words`) |
| `source` (port) | 121 | stored in `Port.source`, no reader found |
| goods' `note`, yard items' `note` | 1,405 / 372 | stored, never read (they are the files' provenance, kept as data) |
| wardroom `flag:` (data/people) | 15 | not parsed by `_wardroom` (`people.py:260-313`); the `flag` read in `orders/station.py` is a different key |

Also unread: `Port.on_day` (`ports.py:553`, no caller; its docstring says it is "kept for a reader
that sets a port to a day by design"), `Port.nation_on` (called only by tests),
`ports._after` (`ports.py:1447`, no caller), and `DEALINGS_NAMES` lists `stance_of_hers`
(`ports.py:1178`), a name `Dealings` does not define. The scenario's `nations:` block is parsed,
validated and saved but read by nothing; the module's own docstring says so
(`scenarios.py:124-132`). The vocabulary's `world_orders.channels` and `world_orders.words`
(`data/vocabulary.yaml:2393-2396`) are loaded into `Vocabulary` (`orders/vocabulary.py:245-247`)
and read only by a test; `recognises` uses its own regex. The words "order to the world" and
"order the world" in that list are not recognised by the code (my run:
`recognises('order to the world: a gale')` -> False).

### Flags and parameters nobody sets

* `WorldOrder.by` and `PURVIEWS` (`orders.py:189-207`): every caller in `freesail/` passes no
  `by` (`agents/director.py:2018`; the console and server give `source` only); only
  `tests/test_world_orders.py:1062` exercises `purview_allows`. A hook for a later milestone.
* `Dealings.send_boat_to(..., by_the_director=True)` is passed only by the world order
  (`orders.py:2011`).

## 3. Built more than once

**3.1 Two order languages, sharing little.** `freesail/world/orders.py` is a second order language
beside `freesail/orders/`. The captain's grammar is vocabulary-driven: `orders.grammar.parse`
(`orders/grammar.py:129`) matches verb phrases from `data/vocabulary.yaml` and resolves nouns
against the ship's parts; it has no regular expressions of its own (`grep -c re.compile` = 0). The
world channel is 58 hand-written regular expressions, one or more per form, each with its own
refusal text. What they share: the number reader (`orders.numbers.read`, `read_all`, used at
`orders.py:902, 1140, 1252, 1704, 2954, 3092`), the part names (`orders.resolve.display_name`,
`family_name`, `orders.py:2697`), the gun names (`orders.gunnery.guns_named`, `orders.py:2264`),
`OrderError` (caught at `orders.py:2012`) and `orders.free.spoken` (`orders.py:2467`). There is a
third grammar under both: the captain's intent (`captains.read_intent`, `world/captains.py:770`),
which the `captain:` and `ship "X": intent` channels hand their words to. And a fourth set of
forms lives in the director (`WORLD_ORDER_FORMS`, 41 `Form`s, `agents/director.py:594`), with the
director re-using private regexes of orders.py (`_SYSTEM`, `_WAYPOINT`, `_SHIP_NEW`, `_PORT`,
`_aboard_match`; `agents/director.py:339-410`). Joining them is not a small job; at least the
forms table and the regexes could be one table from which both the parser and the director's
grammar are made.

**3.2 The channel list four times.** `CHANNELS` (`orders.py:125`), the `_HEAD` regex alternation
(`orders.py:161-167`), the refusal text of `parse` (`orders.py:247-250`, which omits `follow`),
and `data/vocabulary.yaml:2394` (guarded equal to `CHANNELS` by a test). `REFUSAL`
(`orders.py:152`) and the vocabulary's `refusal` are the same sentence twice.

**3.3 Trading built four times.** `trade` (`dealings.py:2276-2373`), `trade_together`
(`dealings.py:2375-2488`) and `trade_list` (`dealings.py:3769-3934`) each repeat the in-port,
stance, price-list and boat-away checks and the purse-and-market moves; `trade` is a special case
of `trade_together`, which is a special case of `trade_list`. The `aboard: ... freighted` world
order is a fifth road into the hold with its own lighter job (`orders.py:3083-3147`). The three
share the R1 bug below, which shows the cost.

**3.4 Finding a person, four rules.** `People.find` (role, then surname, then name;
`people.py:1024`), `People.find_anywhere` (first surname match among other hulls,
`people.py:1054-1074`), `People.find_aboard` (`people.py:1076`), and `orders._person_anywhere`,
which refuses a surname two persons share (`orders.py:1953-1969`). So "Mr Pope" with two Popes on
two hulls is found by `find_anywhere` (the first) and not by `_person_anywhere`. Joining them:
one finder with an "ambiguous" answer.

**3.5 Finding a ship, five ways inside orders.py.** `hull_named` (with the lookout's words,
`orders.py:314`), `_taken_parts.find` (`orders.py:678`), `_ship_named` (strips "the ",
`orders.py:1002`), `world.vessels.find` raw in `_ship` and `_hand` (`orders.py:763, 1488`), and
`_prize_named` with its own loop (`orders.py:4467`). Whether "the Harpy" finds the Harpy depends
on the channel.

**3.6 Finding a port, two roads.** `world.dealings.find` -> `Ports.find` (most channels) and
`orders._port_named` over `world.ports.ports` (cartel and exchange, `orders.py:3918-3925`), whose
refusal lists every port in the world (121 names in one sentence).

**3.7 Near-by rules three times.** `hearing.within_hearing` (`hearing.py:128`),
`things.same_place` (`things.py:568`) and the class rules of `knowledge.reaches`
(`knowledge.py:542-614`), each with `places.earshot`. `knowledge._OPEN_DECK` (`knowledge.py:100`)
is a copy of `places.OPEN_DECK` (`places.py:178`).

**3.8 Small copies.** `reports.MESSENGER_S = 60` is `people.PASS_THE_WORD_S` again
(`reports.py:76-78` says so). `people._number_words` (`people.py:1757`) beside
`crew.model.number_words`. `_and` is written four times (`ports.py:1484`, `hearing.py:207`,
`needs.py:814`, `boats.py:767`, which raises on an empty list).
`needs.NIGHT_ENDS_HOUR = 4` and the hard 20:00 (`needs.py:82, 288`) restate the watch routine.

**3.9 The boat twice.** The scripted boat of `Dealings` (a `BoatState` moving at a constant
`BOAT_PACE_KN = 4`, `ports.py:305`; jobs on a sleeping hull, `dealings.py:2918-2958`; `boat_to`
jobs between hulls, `dealings.py:3347-3449`) and the physical boat of `boats.py` (a hull with oars
and a lug under the integrator). A boat sent to another ship by `send the boat to` takes the job
road; the same boat manned by `go to the boat` takes the physics road. Two models of one boat.

**3.10 Two copies of the port files read.** `world/ordnance.py:206-216` re-reads the port YAML
for its `ordnance:` block beside `load_port`; `ui/harbour.py:443-447` loads every port again for
its list (and drops silently any that fails, `except Exception`).

## 4. Size and shape as a hazard

* **Longest functions** (ast): `scenarios.load_scenario` 497 lines (`scenarios.py:446`);
  `orders._squadron` 183 (`orders.py:1051`); `dealings.trade_list` 166; `dealings._conn` 161;
  `orders._make_person` 141; `dealings._tick_pilot` 140; `places.Papers._lines` 134;
  `dealings._apply_job` 132 (an if-chain over eight job kinds); `dealings._warn` 117;
  `orders._move_person` 115.
* **In-function imports**: 126 in orders.py, 62 in dealings.py, 28 in reports.py, 24 in boats.py,
  about 325 across the thirteen. Many are the circular-import dodge (things.py imports
  `orders.held_stations` inside `held_by`, `things.py:535`; orders.py imports `things` inside
  six functions).
* **The world layer imports the agents and the UI.** orders.py imports `freesail.agents` nine
  times (`agents.agent`, `agents.harness._stations_held`, `agents.journal`, `agents.director`;
  e.g. `orders.py:2383-2385, 2402, 2473`), reports.py ten, knowledge.py, hearing.py and needs.py
  three each; knowledge.py and needs.py import `freesail.api.readings`; `scenarios.begin` imports
  `freesail.ui.console.read_standing_orders` (`scenarios.py:998`). The proposal's hard boundary
  names core, ship, physics and crew; `world/` is not on that list, but `core/world.py` imports
  `world.orders` (`core/world.py:1705`), so the simulation's tick reaches the agents through this
  part. Sure that the imports exist; whether the boundary is breached in letter depends on
  whether `world/` counts as simulation.
* **A hand list kept in step.** `DEALINGS_NAMES` (`ports.py:1074-1190`), 115 names refused on
  `Ports` by `__getattr__`, already out of step (`stance_of_hers`).
* **dealings imports 70 names from ports**, most of them module constants, some private
  (`_ERRAND_WORDS`, `_and`, `_cap`, `_possessive`, ...; `dealings.py:27-100`): the split of
  `Ports` into `Ports` and `Dealings` left the constants and helpers in the wrong module.
* **Two fields for one fact.** `Person.aboard` (a property over `hull`) and `Person.place` /
  `where` are set separately at every move (`orders.py:2033-2036, 2109-2110, 2176-2179`;
  `dealings.py:2707, 2715, 3742`); `people.py:337-343` says "the thirty places that move a person
  stand". Nothing keeps them consistent.
* **Module state.** `reports._STATE_CACHE` and `_STATE_CACHE_BY_ID` (`reports.py:567-568`; the
  second, keyed by `id()`, never evicts), `places._FILE_PAPERS` (`places.py:1003`), the
  `lru_cache`s on `aboard_table`, `_wardroom`, `load_needs`.
* **Every World parses all 121 port files.** When the scenario names no ports and there is a
  chart, `Ports._load` loads every file (`ports.py:1220`), with no cache. Parsing them took 1.10 s
  on this machine (my timing of `yaml.safe_load` over the files). A cost on every world a test
  makes.

## 5. Correctness and honesty

**R1. A purchase or sale with the boat lost takes the money and delivers nothing.** `trade`
checks `self.boat.away` (`dealings.py:2299`) but not `boat.lost` nor a missing boat or runner;
it pays the purse and moves the market (`dealings.py:2327-2328`) and only then calls
`_send_boat`, which raises on a lost boat (`dealings.py:2887-2889`). Nothing is rolled back.
`trade_together` (`dealings.py:2446-2459`) and `trade_list` by the boat (`dealings.py:3861-3906`)
have the same order; on a sale the hold has already been broken out. My run, a schooner at
Falmouth (in_port stubbed, prices written, £500 received, `d.boat.lost='stove'`):
`trade('buy',1,'tin')` -> `OrderError: The long-boat is lost ...`; purse 500.0 -> 380.0;
market `net_sold {} -> {'tin': -1.0}`; hold empty. Weight high (the player's money silently gone);
sure.

**R2. Recruits are given ids that collide.** `_muster_recruits` numbers new men
`s{len(crew.sailors)+i+1:03d}` (`dealings.py:2833-2844`). Sailors are removed from the list by
burial (`crew/health.py:973`) and by prize crews (`world/prizes.py:460`), so the next id can be one
already in use. My run on the frigate: 264 sailors, one removed, two able seamen entered ->
265 sailors, duplicate id `s264`, `crew.by_id` 264 entries (one man shadowed). Persons and the
quarter bill key on `sailor_id`. Weight medium; sure.

**R3. A told prohibition is read as permission.** `reports.told_covers` (`reports.py:802-835`)
accepts an order when `mine in c` or `c in mine` for any clause of what the captain told. My run:
`told_covers(None, ['do not wear her'], 'wear')` -> True;
`told_covers(None, ['never let go the anchor'], 'let go the anchor')` -> True;
`told_covers(None, ['take in the royals'], 'take in')` -> True. Its callers
(`agents/tools.py:1014, 1130`) let such an order through a station's authority as `TOLD`.
Weight medium (a model officer can cite "do not X" as leave to X); sure.

**R4. A malformed live world order escapes as an exception, after being journaled.**
`World.world_order` appends the input to `self.inputs` (`core/world.py:1694-1701`) and then
`_apply_world_order` calls `world_orders.parse(text)` outside its `try` (`core/world.py:1707`);
only `apply`'s `WorldOrderError` is caught (`core/world.py:1710-1714`). My run:
`w.world_order('hello there','the owner')` raised `WorldOrderError` and `w.inputs` grew by one.
The console passes `world: <anything>` straight in (`ui/console.py:731-737`) with no `except`
up to its loop (`ui/console.py:595-600, 825-836, 947-953`), so a mistyped `world:` line likely
ends the console with a traceback, and the save carries an input that raises again on replay
(`core/replay.py:309-313`). The scenario's own orders are parsed at load (`scenarios.py:758-766`),
so this bites the owner and the director only. Weight medium; sure of the raise and the journal,
likely of the console's death (I did not run the console). The server path
(`ui/server.py:604`) I did not trace to its handler.

**R5. Stores have no capacity.** `take in 500 tons of water` passes the number to
`Dealings.demand("water", n)` (`orders/port.py:385-400`), which charges and, when due, adds it
(`dealings.py:2748`); `Stores` has no limit (`places.py:553-581`). Only `take in water` with no
number stops at the ship file's allowance. The hold has a capacity; the water and provisions do
not. Weight low to medium; sure from the code (not run).

**R6. Two hulls' persons share ids, and reach ignores it.** `things._keeps` checks the keeper's
home hull because ids like `master` repeat across hulls (`things.py:162-168, 329-335`), but
`reach_why` starts with `if thing.keeper == person.id: return None` (`things.py:585`), so another
hull's master reaches a thing kept by this hull's master. Weight low; likely (read, not run).

**R7. "Doubt" is a plausibility screen, and says so.** `orders.doubt` (`orders.py:4087`) does not
simulate; it refuses to perform without a stated reason an order the code judges implausible (a
sail inside the horizon by day, a low below the season's floor, a price swing over 30%), and
performs it when the director appends `[reason: ...]` (`orders.py:175-177, 233-240`). The
docstrings describe this honestly. The thresholds are marked judgement
(`orders.py:3841-3854, 4193-4206`). Sound as described.

**R8. Other small faults.**
* `_doubt_ship`'s docstring says a ship "on the land" is doubted (`orders.py:4091-4092`); the code
  leaves it to `form_error` (`orders.py:4177-4178`). A comment and the code differ; harmless.
* Pilotage unpaid for want of money is not entered as a debt (`dealings.py:917-921`), though the
  purse has a debt ledger (`places.py:506-515`).
* `Papers._match` takes the first catalogue entry whose handle *contains* the key
  (`places.py:805-809`): "list" finds whichever of "the price list" and "the booms' list" comes
  first.
* `knowledge._for_me` treats a line as for a person when its `to` ends with his surname
  (`knowledge.py:627`): any Fox is "Mr Fox".
* The ports module's docstring still says "Falmouth, Plymouth and Brest" (`ports.py:1-3`); there
  are 121, and it names `Ports._warn` and `Ports._apply_job`, which are now `Dealings`'
  (`ports.py:32, 1060`).
* Determinism: randomness is drawn from named streams of the world's seeded RNG
  (`world.rng.stream("recruits")`, `"people"`, `"health"`, `"business"`; `dealings.py:809, 2829`;
  `orders.py:914, 3591`). I found no wall-clock time, unseeded random or set iteration in these
  files. Dict order is relied on (the port files' order for "nearest" ties, `ports.py:1255-1259`),
  which is stable in Python. Sound.

## 6. Thin or overgrown

Overgrown at the edge the director uses, thin at the centre the player uses.

* The world channel (4,746 lines, 17 channels, 41 forms) serves a director model and the owner's
  test harness. The game's own scenarios give it 15 orders on 4 channels. The `aboard:` table
  alone has 25 effects and 11 plausibility conditions (`orders.py:3689-3828`); the rule of reach,
  the doubt and the reason peel are elaborate machinery around a text interface for one consumer.
* The pilot is very detailed: `_tick_pilot`, `_warn`, `_fix` and the conn (`_conn`,
  `_joined_track`, `_leg_made`, `_foul_leg`, `_bring_up_to_wait`, `_wait_at_anchor`, ...)
  occupy roughly lines 417-2060 of dealings.py, some 1,600 lines, with 50 constants in ports.py
  (`ports.py:133-299`), many tuned to one save ("from 114000, his five-point turn to NNE",
  `ports.py:283-288`).
* Against that, the port's economy is a price table with three multipliers, a crew pool that never
  refills, and no repair: what a merchant or a captain would come into port for (refit, careen,
  sell a prize, find freight) is absent or a store purchase. The 121 port files carry about 1,400
  annotated prices and positions for depth and bottom that nothing reads.
* needs.py (837 lines) has no consequence yet: "the needs stop at the last step's urgent line"
  (`needs.py:27-30`). It produces words for the stationed person and nothing in the world.

## 7. What is not tested

From grep of `tests/` (I did not read the test files' bodies):
* No test exercises a purchase with the boat lost or absent (R1): `grep "boat.lost"
  tests/test_ports.py` finds nothing.
* No test enters recruits after a man is removed from the muster (R2).
* `told_covers` appears only in `tests/test_known_truths.py`; nothing tests a negative told
  order (R3).
* No test gives `world_order` an unparseable line (R4); `test_world_orders.py:116` tests only that
  `parse` raises.
* No test file imports `needs`; it is reached only through the World.
* `Port.on_day`, `ports._after` and `Spot.depth_words` are called by nothing, tests included.
* What a player meets and the tests cannot see: whether the log a person below receives makes
  sense (`knowledge.REACH`, 118 kinds and 88 families hand-placed, `knowledge.py:243-369`, with "deck" as the
  default for any kind forgotten); the test named in the docstring (`knowledge.py:30-32`) checks
  that each kind is placed, not that it is placed right.

## The ten findings that matter

1. **R1: buying or selling with the boat lost takes the money and delivers nothing.**
   `dealings.py:2299, 2327-2329, 2887-2889`; my run: purse 500 -> 380, no tin. The same order in
   `trade_together` and `trade_list`. High; sure.
2. **The world-order channel is a second order language beside `freesail/orders/`**: 58 regexes,
   17 channels, 41 forms (a further copy in `agents/director.py:594`, which also re-uses
   orders.py's private regexes), sharing only the number reader and a few name helpers with the
   captain's grammar, and a third grammar (`captains.read_intent`) under both. High (each new form
   is a new parser and a new refusal text); sure.
3. **Trading is written three times in `Dealings`** (`trade`, `trade_together`, `trade_list`) plus
   the freight order, each a superset of the last, and they share bug R1. Medium; sure.
4. **R2: recruits get duplicate sailor ids after a death or a prize crew**, `dealings.py:2833-2844`;
   my run gave `s264` twice. Medium; sure.
5. **R3: `told_covers` reads "do not wear" as leave to wear**, `reports.py:821-823`; my run. Medium;
   sure.
6. **R4: an unparseable `world:` line raises out of `World.world_order` after being journaled**,
   `core/world.py:1694-1707`; likely fatal to the console and repeated on replay. Medium; sure of
   the raise, likely of the crash.
7. **Much of the port files' data is read by nothing**: `datum` (116 files),
   `tide.establishment` and `tide.leave_on` (121 each, the establishment duplicating
   `data/tides/establishments.yaml`), `market.currency` (121), `pilot.words.tide` (124),
   spot depths and bottoms (319), `deep_draught_ft` (52, read only by a test), and the scenario's
   `nations:` block. Medium; sure for the first five by grep, likely for the depths.
8. **A port offers stores, not service**: no repair, a crew pool that never refills
   (`dealings.py:2658`), stores with no capacity (R5), while the pilot's conn alone is some 1,600
   lines. The player's port is thinner than its pilot. Medium; sure.
9. **The world layer reaches up into the agents, the API and the UI** (orders.py 9 imports of
   `freesail.agents`, reports.py 10, `scenarios.begin` imports `ui.console`), and about 325
   imports inside functions dodge the resulting cycles; `core/world.py:1705` pulls all of it into
   the tick. Medium (any change here risks a cycle or a hidden dependency); sure of the imports.
10. **Persons, ships and ports are found by several rules that differ** (four person finders, one
    refusing an ambiguous surname and one taking the first; five ship lookups in orders.py; two
    port lookups), and the near-by rule exists three times. Low to medium (bugs waiting); sure.

## What I did not read

* `freesail/world/dealings.py` lines about 976 to 2060 (the pilot's `_warn` from line 976, `_fix`,
  the conn and the wait for the stream): skimmed for function names, exceptions and clock use only.
  Every other line of the thirteen modules was read.
* The data files were read by script for their keys and counts, not line by line: I read
  `data/ports/falmouth.yaml` whole and the vocabulary's world-order block; I did not read the 46
  other scenario files, the 21 `.orders` books, the director's briefs, `data/director/aboard.yaml`'s
  rows, or the wardroom files.
* The tests: only the head of `tests/test_world_orders.py`. Test coverage above is by grep.
* The callers outside my part were read only where cited (`orders/port.py` whole,
  `orders/__init__.py` to line 230, `core/world.py:1670-1750`, `world/movement.py:488-520` and
  `802-882`, `agents/director.py:575-600`). I did not trace the server's handler around
  `ui/server.py:604`, nor run the console.
