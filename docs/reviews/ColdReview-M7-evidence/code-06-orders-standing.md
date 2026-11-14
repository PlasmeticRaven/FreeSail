# Reader 06: the order language (freesail/orders, freesail/standing, the vocabulary, the starter book, the Python API)

Tree at 504a25066c6995ce9829a19ffc597feb510a1870. Nothing under docs/dev, docs/design, docs/playtests or docs/gates was opened, nor the sealed notes. No test suite was run. Short Python probes were run (each a few seconds); their scripts are in the session scratchpad, not the tree.

## 1. What it is

**Size.** freesail/orders: 29 files, 18,446 lines; freesail/standing: 6 files, 3,505 lines; 21,951 in all, 683 functions. data/vocabulary.yaml 2,494 lines (593 verbs, 4,345 verb phrases once synonyms, aliases and the 285 generated reading-verbs are counted; `load_vocabulary()` probe). data/standing_orders: starter.orders 139 lines (7 rules), fighting.orders 16 lines (7 rules). Whole-line comments and docstrings are at least 17% of the 21,951 lines (3,830 lines by an ast count that ignores trailing comments); the strings "package NN", "playtest N", "gate N", "game N" and "owner's ruling" occur 544 times in the two packages (verbs.py 70, stations.py 64, navigation.py 53).

**What it does in the game.** Every line the player (or a station, a rules captain, a standing order) types becomes `World.submit(text, actor)` (freesail/core/world.py:1969), which calls `ship.handle_order` (freesail/ship/graph.py:339) whose handler is `orders.handle` (set at freesail/api/session.py:44). `orders.handle` (freesail/orders/__init__.py:59-179) is a ladder of recognisers tried in turn, each with its own reader of the words:

1. the world channel and the literal `captain: carry on` (__init__.py:71-83; `freesail.world.orders.recognises`);
2. the standing dialect (`standing.grammar.recognises`, then `bare_book_sentence`) (:84-92);
3. the signals and the hail (`orders.signals.recognises`, 26 compiled regexes in `_FORMS`, signals.py:86-245, plus `_HAIL`/`_SAY_TO`) (:93-106);
4. the station sentences (`orders.stations.recognises`, 13 regexes, stations.py:137-176) (:107-116);
5. the books (`freesail.world.books.recognises`) (:117-122);
6. `refused_phrases` from the vocabulary (:123-128);
7. only then the grammar proper, `orders.grammar.parse` (:130), with two fall-backs on failure: `prompt.answer_unparsed` for a reading or a part named without a verb (:131-137), and `_stores_order` / `free.hand_line` for "take in twenty tons of water" and "hand the packet to ..." (:138-150);
8. dispatch on the verb's `object` kind to one of 17 executors by a chain of `if vocab.verbs[order.verb].object == "..."` branches (__init__.py:235-325): navigation, anchor, person, port, boat, needs/allowance, fishing, glass, gunnery, signals, damage, fight, prize, and the sail/yard/line/helm verbs in `verbs.py` (3,248 lines).

Main types: `Order` (grammar.py:73), `Vocabulary`/`VerbSpec` (vocabulary.py:23-117), `NounTable`/`Noun`/`Resolution` (resolve.py:62-131), `OrderError` and its subclasses (errors.py:21-35; the base class lives in freesail/ship/stub.py). Standing: `Rule`, `Trigger`, `Condition`, `Clause`, `Comparison` (standing/rules.py), `Book` (book.py:100), `Runtime` (runtime.py:268), ticked from `World.tick`.

**What the player sees.** The line accepted ("Order: set the royals.") or "Order not carried out ('...'): <sentence>" (world.py:2042-2071). Standing orders: "Standing order 'x' entered in the book: ..." (book.py:178), "By standing order 'x': taking in the royals" (runtime.py:564), "Standing order 'x' <trigger>: not carried out; <why>" (runtime.py:538).

**Tests that belong to it.** 59 of 174 test files import freesail.orders or freesail.standing. The ones named for it: tests/test_orders.py 2,877, tests/test_standing.py 2,211, tests/test_world_orders.py 1,070, tests/test_practice_orders.py 908, tests/test_signals.py 754, tests/test_tackle_orders.py 754, tests/test_powder_orders.py 504, tests/test_orders_places.py 482, tests/test_python_api.py 405, tests/test_crew_orders.py 392, tests/test_orders_m4a.py 351, tests/test_trim_order.py 331, tests/test_grammar_book.py 186, tests/test_complete.py 164; and much of tests/test_known_truths.py (17,391).

## 2. The proposal's promises, one by one

### 2.1 "One channel: every actor's order goes through one `submit`"

**Largely built, with three bypasses.** The player, the stations (agents), the rules captains and the standing runtime all go through `World.submit` (world.py:1969; standing firing at runtime.py:561; Python rules fire the same way). Bypasses:

- A sleeping hull's orders go to `world.crews.submit_far` (world.py:1976-1985 into crews.py:1328), which has its own regex reader for "shape/lay a course for" (crews.py:1118) and its own routing ladder `_needs_no_physics` (crews.py:1286-1325) that re-asks signals, stations, standing and books in a different order. A second channel with a second parser.
- Orders given from inside code call `orders.handle` directly, unlogged as orders and unjournaled: evolutions/scripts.py:5576 ("brace sharp up"), orders/navigation.py:1226 (tack or wear for `put her about`), orders/port.py:312 (the pilot's wants), orders/storm.py:136 (`verbs.execute` direct). Deterministic, so not a replay hazard, but they do not pass the movement and authority checks that `handle` and `submit` apply.
- The agent's authority check (agents/tools.py:942-1010) re-implements the head of the ladder (standing, bare book, stations, books, parse, then the private `orders._stores_order`) in its own order and without the signals step. Two copies of the router that must agree.

Weight medium, confidence sure.

### 2.2 "A parser of a few hundred lines"

**Not built as promised.** The core grammar is grammar.py, 919 lines, with `parse` 172 lines (grammar.py:129) and `_parse_modifiers` 171 lines (:712). But the player's words are read in at least sixteen places, most of them hand-written matchers that know nothing of the grammar:

| Reader | Where | How |
|---|---|---|
| world channel | world/orders.py:224 | regex `_HEAD` |
| `captain: carry on` | orders/__init__.py:72 | literal string compare |
| standing sentence, trigger, condition | standing/grammar.py (1,392 lines; `_parse_comparison` alone 448 lines, :696-1143) | hand-written phrase tables (`_GT`, `_LT`, `_SEA_SAID`, `_MOTION_SAID`...) and 3 regex calls |
| bare book sentence | standing/grammar.py:1342-1375 | `_BARE_BOOK` table |
| signals, colours, lights, hail | orders/signals.py:86-255 | 28 compiled regexes |
| station sentences | orders/stations.py:137-176 | 13 compiled regexes |
| books | world/books.py:170 and its own quote reader `_title` (:184) | phrase match |
| refused phrases | vocabulary.py:99 | prefix match |
| the grammar | orders/grammar.py | token matcher over the vocabulary |
| readings without a verb, a part by name | orders/prompt.py:207-277 | its own match, reusing `grammar._match_object` |
| stores ("twenty tons of water") | orders/__init__.py:328 | hand matcher |
| free lines | orders/free.py:109, 213, 379, 531, 792, 820 | 4 compiled regexes, 2 inline |
| each object kind's words after the verb | navigation.py (3 compiled, 4 inline), ground_tackle.py (3, 7), port.py (2, 7), gunnery.py (3, 1), ordnance.py (7, 2), station.py (2, 1), boat.py (1), prize.py (1) | regexes over `order.object`, which the grammar hands on unparsed for 15 kinds (grammar.py:180-210) |
| far hull | world/crews.py:1118 | regex |
| completion | orders/complete.py | its own tables of sentences and comparisons |

In orders and standing together: 71 `re.compile` and 34 direct `re.match/search/sub` calls. The grammar's own docstring (grammar.py:3-21) describes only the sail/line/helm order; for 15 of the 29 object kinds the grammar takes the verb and passes every remaining word through as `object` text (grammar.py:180-210), so each kind's module is a parser of its own. **It is a verb-by-verb accretion around one real grammar, not one grammar.** Weight high (it is where the next bug in reading a player's words will be, and nowhere is there a single statement of what the game accepts), confidence sure.

Concrete duplications inside it:

- The same `re.sub(r"\b(from|the|yard|chandlers|a|an|spare)\b", ...)` three times in port.py (:116, :349, :374); `parse_position(re.sub(r"\b(degrees?|minutes?)\b", ...))` four times in navigation.py (:110, :189, :1431, :1542).
- The signal verbs are listed twice: as vocabulary synonyms (data/vocabulary.yaml:1784-1790, "hoist the colours" with eight synonyms) and as regexes (signals.py:86-100). They differ: the regex takes "set the flag again" and "run up our flag" (probe: both answered "Her own colours are flying already"), the vocabulary lists neither; "fly the ensign" is in neither. Since signals.recognises runs first, the vocabulary's synonyms serve only hints and completion.
- The station sentences are listed three times: `STATION_VERBS` (stations.py:99), per-station rows in vocabulary.yaml ("ask the master", "ask the lookout", vocabulary.yaml:1182-1205, 33 verbs of object `station`), and complete.py:52-57, which still offers only "the watcher".
- Two quoted-name readers: standing/grammar.py:124-147 pairs the closing quote with the opening (a fix recorded at :133-135, "package 79c"), world/books.py:184-196 still closes on any quote character, so a book title with an apostrophe in double quotes breaks there.
- The vocabulary's `numbers:` table (vocabulary.yaml:2163-2178: one to twelve, sixteen and half, no thirteen to fifteen) is no longer a number reader; `orders.numbers` replaced it (numbers.py:1-6 says five readers had become one). The YAML values are never read as numbers; the keys survive only as leading/modifier words (grammar.py:535, :639). Dead data that reads as live. `grammar._count(word, vocab)` and `_count_at(words, i, vocab)` (grammar.py:678-691) take `vocab` and ignore it.
- `port.number_in` (port.py:54) is a one-line wrapper of `numbers.number_in` (numbers.py:209).
- The completion's condition words (complete.py:60-72) cover 11 kinds; the condition grammar takes 25 (`_HOW`, standing/grammar.py:397-464).

### 2.3 "A vocabulary generated from the ship file: the parser knows the grammar, the ship file supplies the nouns"

**Built for the rig, and well.** `resolve.build_noun_table` (resolve.py:284-350) generates every part's names from its id, the ship file's aliases and groups, contractions ("tops'l"), sided families and plurals, and shorthands that are refused with candidates when ambiguous ("The topsail could be the fore topsail, the main topsail or the mizzen topsail; say which", probe on the frigate). The frigate's table has 8,685 entries. The verbs are hand-written data (vocabulary.yaml:25-1885); the readings' query verbs are generated from the readings registry (vocabulary.py:319-364). The parser carries no ship-specific noun.

Limits: the guns are kept out of the table (resolve.py:291) and read by gunnery.py's own regexes; people, places, marks, stations and other ships are each found by their module's own finder, not by the table.

**A bug in it (shown):** no sail without a side is ever offered as a spelling hint. `build_noun_table` first enters the raw id with `suggest=False` (resolve.py:295-297); `key("fore.topsail")` normalises to "fore topsail" (vocabulary.py:123, 154), so the later entry of the plain words finds the key taken and is never added to `_names` (resolve.py:90-104). On the frigate 26 of 38 sails are missing from the hint list (only the sided studding sails are in it). The player sees, for a typo of a sail, the sail's lines:

    set the fore topsial -> There is no such part as the fore topsial in this ship; did you mean the fore topsail lift, the fore topsail halyard or the fore topsail sheet?
    set the fore royl   -> ... did you mean the fore royal lift, the fore royal sheet or the fore royal brace?

The standing condition grammar builds its own hint list from `display_name` of every sail (standing/grammar.py:583) and so gets this right: two suggestion lists that disagree. Weight medium (the player's main teacher, errors.py:3-7, teaches the wrong noun for the commonest typo), confidence sure.

### 2.4 "A standing dialect and a Python API that compile to the same rule"

**Built.** Both make `standing.rules.Rule` (dialect: grammar.py:188; Python: python_api.py:238), enter it through `Book.enter` (book.py:174), are evaluated by one `Runtime.tick` (runtime.py:383) and fire through `World.submit` (runtime.py:561). `tools/python_twin.py` and tests/test_python_api.py check the two give one log. The Python API is "thin on purpose" (python_api.py:1-2): the decorated body is run once at registration, its `order(...)` strings collected (python_api.py:261-279) and parsed by the dialect's own `_parse_actions` (python_api.py:234, a private function of standing/grammar). So the Python rule is a macro for a dialect rule; it computes nothing at firing.

Who reaches it: `bind/when/at/every` are imported only by tools/python_twin.py:31 and tests (grep of freesail/ui, agents, world, core: none). There is no way in the console, the server or a scenario to load a player's Python file; `restore_absent` (python_api.py:294) is reached from ui/console.py:447 to list a saved Python rule as "not loaded". Module-level mutable state `_bound` and `_collecting` (python_api.py:86-87). Weight low as a defect, but the feature is test-and-tool only.

### 2.5 "Scripts run restricted with a time budget per tick and no filesystem or network"

**Not built. There is no sandbox.** grep of freesail, client, tools and pyproject.toml for sandbox, RestrictedPython, `__builtins__`, `exec(`, `eval(`, setrlimit, a time budget: the only hits are two sentences in python_api.py (:29 "milestone 6's sandbox is where the body runs", :44 "Computation on the readings *at firing* is what milestone 6's sandbox adds, under a time budget"), which describe something that does not exist. The body is ordinary Python called in-process (`fn()` / `fn(world.readings)`, python_api.py:273-276) with the game's full privileges, and the rule is marked `trusted=True` (:246). It is safe today only because nothing in the game runs a player's Python. The comment and the code differ: a finding. Weight medium (a promised feature absent, with comments implying it), confidence sure.

## 3. How a new verb is added

- A new verb of an existing kind: one entry in data/vocabulary.yaml, and a branch in that kind's executor (for a sail verb, an `evolutions:` row and perhaps a refusal; for gunnery, a case in gunnery.py's own dispatch on `order.verb`). Two files, more if the verb wants its own words read (its module's regexes) or a conflict grain (`GUNNERY_PARTS`, standing/runtime.py:118).
- A new kind of verb (as `fishing`, `prize`, `boat` were): data/vocabulary.yaml; a new orders/<kind>.py; the `_carry_out` chain (orders/__init__.py:235-325); the pass-through tuple in grammar.py:180-196; `read_whole` if give-time checks are wanted (__init__.py:204-231); the place rule (world/movement.py:117 `DECK_OBJECTS`, and world/knowledge.py:395-440 has a place table by family that a test checks); the officers' domains (agents/agent.py:318-345, by `object:<kind>`); the conflict rule's parts (standing/runtime.py:143-186, which otherwise treats it as touching "the ship"); completion (complete.py, 23 `object` tests). Seven to nine files. `grep "spec.object|.object ==|.object in"`: complete.py 23, agents/agent.py 16, orders/__init__.py 15, grammar.py 9, agents/tools.py 8, verbs.py 6, runtime.py 5, stations.py 4. Weight medium, confidence sure.

`VerbSpec.object`'s comment lists eight kinds (vocabulary.py:29); there are 29 (probe: query 283, none 40, station 33, navigation 23, signals 20, gunnery 19, damage 18, sail 15, port 14, free 14 ...).

## 4. The orders code and the world, the agents and the simulation

- orders reaches into world heavily: 125 `from freesail.world` imports across the package (movement 13, geo 11, reckoning, places, lookout, flags 5 each, captive 4, captains 3, and others), most inside functions.
- orders imports the agents: orders/stations.py:78 at module level (`freesail.agents.agent`), and inside functions stations.py:493, 505, 534-535, 826, 898, 927, 1104, 1245; signals.py:366; free.py:226, 843-844 (including the private `harness._stations_held`). Importing `freesail.orders.stations` loads `freesail.agents.harness`, `.model`, `.tools` and `.fake` (probe of `sys.modules`). Every order a player gives therefore runs through a module that has pulled in the model harness.
- The reverse: world reaches back into orders' private names (world/signalling.py imports `_start_hoist`; world/reckoning.py `_off_a_place`); agents/tools.py uses `orders._stores_order`; world/scenarios.py:998 imports `freesail.ui.console.read_standing_orders` to load a scenario's books (the world importing the user interface).
- The hard boundary of the proposal (core, ship, physics, crew must not import client or agents): core, ship, physics and crew import from orders only `OrderError` and the standing runtime (core/world.py:1075; crew/victuals.py:274; crew/health.py:706, 1061). The boundary is kept in the letter. In effect it is not: `World.submit` calls `orders.handle`, which imports `orders.stations`, which imports the agents at module level. Weight medium, confidence sure.
- Function-level imports: 275 in orders, 14 in standing, most of them to dodge cycles with world and agents.

## 5. What happens to an order the parser does not know

The refusal is a sentence and usually names what was understood. Probes on the frigate (`World.submit`):

    frobnicate the mizzen     -> 'frobnicate the mizzen' is not an order this ship understands. An order begins with a verb such as set, take in, furl, reef, shake out, brace, trim or haul.
    please set the jib        -> ... did you mean 'ease'? ...
    ask the bosun how she does-> ... did you mean 'take the sun', 'ask the pilot' or 'ask the master'? ...
    sail away                 -> ... did you mean 'shorten sail' or 'fother a sail'? ...
    brace the yards sharply   -> There is no such part as the yards sharply in this ship. ('brace' was understood.)
    steer sw by w and a bit   -> 'steer' was understood, but not 'and'; did you mean 'hand'? ...
    heave to and steer north  -> 'heave to' was understood, but not 'and steer'; did you mean 'hand' or 'steer for'? ...
    steer north; set the jib  -> 'steer' was understood, but not 'set the jib'; did you mean 'set up', 'either' or 'jibe'? ...
    furl the mainsail ;drop dead -> There is no such part as the mainsail drop dead in this ship; did you mean the mainsail brace, ...
    as you were               -> 'As you were' is not an order the ship keeps: say 'belay that' ... (a hand-written refused phrase)

Sound in shape: a misspelt verb or a wrong-kind object gets a usable sentence, and an ambiguous noun lists the candidates. Faults: the hints are spelling neighbours and often absurd ('ease' for 'please', 'hand' for 'and', 'take the sun' for 'ask the bosun'); a stray adverb is folded into the noun ("the yards sharply"); the semicolon that separates orders in the standing dialect (standing/grammar.py:270) is not a separator at the prompt and is read as part of a noun; and a typo of a sail suggests its lines (2.3). Weight medium, confidence sure.

## 6. The starter book on the cutter

**Is the starter book written for the frigate alone?** In effect, yes. It claims to be "the general and instructive routines of a ship at sea" (starter.orders:3), but its reasons are the frigate's ("where the frigate's sails just fill", :50-54; truth 9 and the frigate's strain tables, :33-39), its own load instructions name data/ships/frigate-36.yaml (:17-18), and three of its seven rules name royals or studding sails. Probe: each of the seven rules parsed with `parse_standing` against every ship in data/ships:

| Ship | Rules taken | Refused |
|---|---|---|
| frigate-36, razee-44, sixty-four, seventy-four, brig, merchant-brig, hermaphrodite-brig | 7/7 | none |
| cutter, smack, lugger, bilander | 4/7 | night routine, morning sail, shorten sail for weather (no studdingsails, no royals) |
| topsail-schooner, privateer-schooner | 4/7 | the same three (no royals) |
| the five boats | 3/7 | the same three and heavy weather (no topsails) |

Eleven of eighteen ships lose rules. Scenarios that load the starter on such a ship: first-action, leak and merchant-cutter (cutter); gate-5b-passage-schooner, merchant-passage and merchant-schooner-plymouth (topsail schooner). The loss is not cosmetic: on the cutter "shorten sail for weather" (starter.orders:47-48) is refused whole because its first order names the studding sails, so its last order, the reef of the topsails at 30 knots, is lost with it. The cutter goes to sea with no rule to shorten sail in a rising wind.

**How a standing order naming a part the ship lacks is meant to behave.** The code is consistent with itself and inconsistent with the group evolutions. A standing order's orders are read whole at give time (`_parse_actions`, standing/grammar.py:260-309, calling `orders.read_whole`, __init__.py:182-232), and any order naming no part of this ship raises, so the whole rule is refused with the sentence the reviewer saw ("In standing order 'night routine', 'take in the studdingsails' is refused: There is no such part as the studdingsails in this ship..."). The docstring says this is deliberate, so that "a misspelt sail ... is refused when the standing order is given and not when it fires" (standing/grammar.py:24-27). But a group evolution's lines that name a missing part are passed over in silence (`_group_evolution`, __init__.py:387-421: "a schooner has no royals to set"). The dialect cannot tell a misspelling from a part this class of ship lacks, and has no way to say "the royals, where she has them". There is a "held" mechanism for an order on an absent *reading* (grammar.py:274-289, `Rule.held`) but none for an absent *part*. A scenario's books are loaded by submitting each line as the captain's order (ui/console.py:140-151), so each refusal is one rejected line at the start of the log and the remaining rules still load (rules captains' books use `Runtime.load_book`, runtime.py:293-353, the same per-line behaviour). Weight high, confidence sure.

**Does any test load the starter book on every ship?** No. Every test that loads it does so on the frigate: tests/test_orders_m4a.py:318-341 (`close_hauled_frigate()`, asserting no `order.rejected`), tests/test_agents.py:445-452 (`frigate_world()`), tests/test_replay.py:87/114, tests/test_lying_to.py:719/766, tests/test_weather_script.py:231/326 (the gate day, frigate), tests/test_practice_orders.py:858 (asserts the scenario lists the file, frigate). Several tests loop over every ship (tests/test_readings.py:41, tests/test_server.py:89, tests/test_captains.py:131, tests/test_stores.py:64) but none of them loads a book. No test plays first-action with its books and counts rejected lines (grep of tests for first-action: test_known_truths.py, test_sail_by_name.py, test_service.py; none asserts on refusals).

## 7. "Standing order 'more of her' at a sail made out: not carried out; a stranger in sight is no stranger in sight."

**Where it is made.** The rule is in the rules captains' books: data/captains/kings-ship.yaml:204 and :217, revenue.yaml:152/156, cruiser.yaml:183/187 (`standing order "more of her": at a sail made out, if a stranger in sight is in sight then make her out` / `... then give chase`), and data/scenarios/naval-cruise.orders:76. The cutter's commander in first-action keeps a King's ship's doctrine, so this book is loaded by `Runtime.load_book`. When the trigger fires (a sail made out) and the `if` fails, `Runtime._fire` writes "Standing order '{name}' {trigger}: not carried out; {explain}." (standing/runtime.py:523-543). The explanation is `Clause.describe` (standing/rules.py:324-348). The reading's value when no stranger is in sight is the lookout's `{"in_sight": False, "words": "no stranger in sight"}` (world/lookout.py:1132). `describe` has a short cut (rules.py:342-347) meant for "the land is not in sight": when the comparison's words ("in sight") occur inside the reading's words, it writes "<phrase> is <reading's words>" instead of "<phrase> is <words>, not <comparison>". Here "in sight" is a substring of "no stranger in sight", so the line becomes "a stranger in sight" + " is " + "no stranger in sight". Reproduced (probe: `parse_condition('a stranger in sight is in sight')` and `describe` over the lookout's words gives exactly "a stranger in sight is no stranger in sight"; the same code gives "the land is not in sight" for the land, the case it was written for).

**What it was meant to say.** That the sail just made out is no stranger (she is known for one of the ship's own nation, or has been spoken: lookout.py:1119-1131 filters those out), so the chase is not given: in the code's own words, "no stranger in sight", or "not carried out; no stranger is in sight". Two faults stack: the condition is phrased awkwardly in the data (the reading's own name ends "in sight", so "a stranger in sight is in sight"), and the substring test in `describe` treats any reading whose words contain the comparison's as already saying it. No test covers it (grep of tests for "no stranger in sight": none). Weight low to medium (a nonsense line in every cruise where a friendly sail is made out), confidence sure.

## 8. Built more than once (summary)

1. The router ladder: orders/__init__.py:59-179, agents/tools.py:942-1010, world/crews.py:1286-1325, in three orders. Joining: one `classify(text, ship) -> (route, verb)` used by all three.
2. Signals: vocabulary synonyms against signals.py regexes (2.2).
3. Stations: `STATION_VERBS`, vocabulary rows, complete.py (2.2).
4. Quoted names: standing/grammar.py:124 against world/books.py:184.
5. Hints for a sail: resolve's `_names` (broken for sails) against standing/grammar.py:583.
6. "Shape a course for": orders/navigation.py against world/crews.py:1118.
7. Numbers: orders/numbers.py against vocabulary.yaml `numbers:` (dead values).
8. Condition words: standing/grammar.py `_GT/_LT/...` against complete.py:60-72.
9. Conflict and undo: `ActionParts.conflicts_with` (runtime.py:94) and `undoes` (runtime.py:751) are deliberately two relations (the docstring says so, runtime.py:757-760); kept apart by design, not a bug.

## 9. Size and shape as a hazard

Longest functions: standing/grammar.py:696 `_parse_comparison` 448 lines; orders/verbs.py:1014 `_trim` 321 (7 parameters); orders/navigation.py:1502 `execute` 238; orders/verbs.py:619 `_brace` 229; orders/ground_tackle.py:212 `execute` 173; orders/station.py:293 `_work` 172; orders/grammar.py:129 `parse` 172; orders/grammar.py:712 `_parse_modifiers` 171; orders/navigation.py:469 `judge_course` 156; orders/fight.py:95 `execute` 144. Longest modules: verbs.py 3,248; navigation.py 1,833; stations.py 1,464; gunnery.py 1,437; standing/grammar.py 1,392; signals.py 1,258.

Module-level caches and mutable state: `load_vocabulary` is `lru_cache`d and returns a mutable dataclass shared by every caller (vocabulary.py:175); complete.py's own `_vocab` cache (:75); `rules._EVENT_CONDITIONS` (rules.py:437); the noun table cached on `ship.extra["orders.nouns"]` (resolve.py:469-475) and never rebuilt (a suspicion only: I did not find a path that adds parts to a ship after the first order); python_api's `_bound`, `_collecting`.

Comments: the docstrings are long and mostly history ("package 37l; the review of gate 5c's playtests, G17: ..."). The reasons are often there, but a newcomer has to read a project diary to find the rule. 544 history markers in 21,951 lines. Some are now false: standing/grammar.py:388-394 and :705-707 refuse a condition on the well "until milestone 7's pumps (taking on water) give it a rule", but milestone 7's pumps exist (`man the pumps`, orders/damage.py), and "when the well is over 2 feet" is still refused. The vocabulary's `VerbSpec.object` comment is eight kinds behind 29 (vocabulary.py:29).

## 10. Dead or test-only

- The "held for an absent reading" path: `_parse_actions` (standing/grammar.py:274-289), `Rule.held` (rules.py:514), the "Held until ..." line (book.py:180-184), the runtime's skip (runtime.py:395), `prompt.absent_named` (prompt.py:230) and its use at __init__.py:254. At this commit no reading in the registry is absent (probe: no row has `is_absent`), so none of it can fire. Dead until a future absent row.
- The Python API: reached by tools/python_twin.py and tests only (2.4).
- The vocabulary's `numbers:` values (2.2).
- `_count`/`_count_at`'s `vocab` parameter (2.2).

## 11. Correctness and honesty (beyond the above)

- `absent_named` and `_parse_actions` match an absent reading by substring of its words anywhere in the order (`f" {w} " in norm`, prompt.py:235, standing/grammar.py:286): an ordinary order containing such words would be held or refused. Harmless today because no row is absent.
- The Python API comments promise a sandbox (2.5).
- `Clause.describe`'s substring short cut (section 7).
- The noun-table hint bug (2.3).
- Nondeterminism: I saw none. `errors.nearest` uses difflib (deterministic) over lists kept in insertion order; the runtime iterates the book in list order (runtime.py:394); `frozenset` part sets are compared, not iterated for output (`_where` sorts, runtime.py:796).

## 12. Thin or overgrown

Overgrown at the edges, sound at the centre. The sail and line grammar with the generated noun table (grammar.py, resolve.py, vocabulary.py, ~2,000 lines) is a real design and does what the proposal asked. Around it, every milestone has added a kind of order with its own reader, its own branch in `_carry_out`, and its own prose of refusals, so that the order language is now some 22,000 lines in which the grammar is a tenth. The standing dialect's condition reader is a single 448-line function of phrase tables, one per reading kind. Meanwhile the thing the player meets first on a small ship, a starter book that works on her, is missing, and the proposal's sandbox is absent.

## 13. What is not tested

By a grep of tests/ for the names (public functions of the two packages): `errors.unknown_verb`, `unknown_noun`, `unknown_words`, `ambiguous_noun`, `suggest` and `join_names` are never called by name (only their sentences matched through orders); `resolve.build_noun_table`, `compound_span`, `pluralise`, `singularise`, `resolve_side`; `prompt.answer_unparsed`, `absent_named`; `signals.hail_parts`; `stations.for_standing`, `read_grant`, `thing_named`; `storm.set_storm_staysails`, `keep_storm_canvas`, `flying_topsail_lines`; `verbs.reeve_every_parted_line`, `boom_fouled_by_brace`, `manoeuvre_for_course`; `book.check_places`; standing `parse_book_command`, `bare_book_sentence`, `rank_of`, `said_as_done`; `orders.crew.call_watch`, `beat_to_quarters`, `take_hands_from`; `navigation.carry_out`, `keep_course_pending`, `steer_degrees`, `mark_in_sight`. Many are exercised indirectly through `World.submit`. Behaviour the tests cannot see: the starter book on any ship but the frigate; the spelling hint for a misspelt sail (no test asserts a sail is hinted); the "not carried out" line of a failing `if` on a `sight` reading; a scenario's books loaded with zero rejected lines.

## The ten findings that matter

1. **The starter book is the frigate's.** On 11 of 18 ships it loses three or four of its seven rules at the start, including the cutter's only rule to shorten sail in weather, because a standing order naming a part the ship lacks is refused whole at give time (standing/grammar.py:260-309) while a group evolution passes such a part over (orders/__init__.py:387-421). No test loads it on any ship but the frigate (tests/test_orders_m4a.py:318). High, sure.
2. **No sandbox exists.** Player Python is not run anywhere in the game; the Python API is a registration-time macro used by a tool and the tests, running unrestricted in-process with `trusted=True`, and its comments speak of a sandbox and time budget that are not in the tree (python_api.py:29, 44, 273-276). Medium, sure.
3. **Not one parser but sixteen readers.** 71 compiled and 34 inline regexes across 13 files, a router ladder of eight recognisers before the grammar (orders/__init__.py:59-179), the grammar passing raw words on for 15 kinds (grammar.py:180-210). High, sure.
4. **The router is built three times** (orders/__init__.py:59, agents/tools.py:942, world/crews.py:1286) in three orders, and a sleeping hull has a second channel with its own regexes (crews.py:1118, 1328). Medium, sure.
5. **A misspelt sail is never hinted as itself**: 26 of the frigate's 38 sails are missing from the hint list because the raw id takes the key first (resolve.py:295-297, 90-104); "set the fore topsial" offers its lift, halyard and sheet. Medium, sure.
6. **"a stranger in sight is no stranger in sight"** is made by `Clause.describe`'s substring short cut (rules.py:342-347) over the lookout's words (lookout.py:1132), fired from runtime.py:538; it meant "no stranger is in sight". Untested. Low to medium, sure.
7. **A new kind of verb touches seven to nine files** across orders, world, agents and standing (`_carry_out`, grammar.py:180, movement.DECK_OBJECTS, knowledge.py place table, agents/agent.py domains, runtime.action_parts, complete.py). Medium, sure.
8. **The orders package imports the agents at module level** (stations.py:78); importing it loads the model harness, so every order passes through it, and world imports the UI to load books (world/scenarios.py:998). Medium, sure.
9. **Duplicated word lists that already differ**: signal verbs as vocabulary synonyms and as regexes; station sentences in three places (complete.py offers only "the watcher"); two quoted-name readers, one with the apostrophe fix and one without (world/books.py:184); the dead `numbers:` table in vocabulary.yaml. Medium, sure.
10. **Refusals are plain sentences but the hints mislead**: 'ease' for 'please', 'hand' for 'and', 'take the sun' for 'ask the bosun'; "the yards sharply" read as a part; the dialect's semicolon not a separator at the prompt. And the well, now with pumps, still cannot be compared in a standing order, by a comment that says "until milestone 7" (standing/grammar.py:388-394). Medium, sure.

## What I did not read

Read whole: orders/__init__.py, grammar.py, vocabulary.py, errors.py, resolve.py; standing/__init__.py, rules.py, book.py, grammar.py, runtime.py, python_api.py; data/standing_orders/starter.orders and fighting.orders.

Read in part: orders/verbs.py lines 1-700 of 3,248; orders/stations.py 1-420 of 1,464; orders/signals.py 1-100 and 280-420 of 1,258; orders/prompt.py 195-277 of 277; orders/complete.py 1-120 of 528; orders/numbers.py 1-50 and 200-223.

Not read beyond their docstrings, their regexes (by grep) and function lists: orders/navigation.py, gunnery.py, free.py, port.py, ground_tackle.py, station.py, storm.py, ordnance.py, crew.py, work.py, boat.py, fishing.py, needs.py, glass.py, people.py, prize.py, fight.py, damage.py. data/vocabulary.yaml was read only at the sections cited (section heads by grep; verbs 1182-1205, 1784-1790; numbers 2160-2190). Findings about those files are limited to what the greps and probes above show; I make no claim about their internal correctness.
