# Milestone 7b work packages

The packages of `docs/TechnicalSpec-M7b.md` (§24), briefed in turn for the owner's approval
and launched on his word. The head rules of `M6-WorkPackages.md` hold: the heavy design to
Fable and the standard work to Opus; each item an intent with the lead's reading of a way,
the intent binding; the budget the owner's; nothing under `docs/agents/consent/` or in
`docs/agents/ConsentBrief.md` touched but by the package the specification names (55's
draft, the revision after); no model identifier in any file of the repository; a world
order never shown as sent (decision 46); the recorded passages' pins re-measured only where
a change moves them, with the old figure beside the new and the reason in the tuning
notes; the fast tier and the slow tier of the files touched before the report, the whole
slow tier once at the end; a section in the tuning notes and a report to the lead.

## Waves

| Package | Builder | What | State |
|---|---|---|---|
| 50 | Fable | The director proper: the station above the game, the world orders doubted not refused, the brief and its limits, the budget, the hidden log revealed on request and inline in replays | briefed 2026-10-17, brought forward to the close of M6 (decision 50); approved and launched the same day; **built the same day** (spec §2 to §7 as built, the Harness's §19, the primer's chapter 20, the tuning notes; the owner's refinement of the examples-not-a-rule framing in the brief and the channel); **merged 2026-10-17** (the record below) |
| 52 | Opus | The director's voice: people from words, `say as`, the unseated answered; the word heard a word on deck; the truth of who commands told to every station | briefed 2026-10-17, after 50; **built the same day** (spec §8, §9, §10 and §15 as built; the Harness's §19; the primer's chapters 19 and 20; the tuning notes, "Package 52"; truths 7b-95 to 7b-97); **merged 2026-10-17** (the record below) |
| 53 | Opus | People in places: a person's place as an aspect of his state tied to what he can do, the player ashore, books drafted, the equal reach, several stations of a kind | briefed 2026-10-17; approved and launched the same day, the three together |
| 54 | Opus | Needs: provisions and water, hunger, thirst and fatigue in a few steps, sleep below | briefed 2026-10-17; approved and launched the same day, the three together |
| 51 | Fable | The observed world: the followed ship in place of the given one, no player's ship, the player on another ship, the replay of a station there; the director's chart, the truth drawn (spec §12a); provisionally the director's focus and the ships' logs by kind and tick range (spec §12b; both the owner's word of 2026-10-17) | brief to write, after 50 |
| 56 | Opus | Fishing for the player with the fisherman's parity and the fishermen promoted; the glass on a near ship by tiers; a sighting saying her heading | brief to write |
| 57 | Opus | The frigate's staysails from Steel's list through the generator, the period's shapes; the chasse-marée's rig put right (lug topsails, not square; the lugs slung a third from the fore end and set to leeward of the mast; the trim rule reading a lug as fore-and-aft) and the viewer's draw order by aspect and the brace shown (the owner's notes of the Éclair's first cruise, `docs/playtests/2026-10-17-eclair-first-cruise/owner-notes.md`) | briefed 2026-10-17; approved and launched the same day, the three together |
| 58 | Opus | The captain's sea sense, third pass (the owner's runs of gate 6c); a leg re-laid as the stream changes; the sample's deltas, the `ahead` reading and the cost of thinking (the owner's observation of 2026-10-17) | brief to write |
| 59 | Opus | The harbour: a launcher in the browser, the scenario maker, the settings and the doors started from it (the owner, 2026-10-17) | brief to write |
| 60 | Opus | A ship bought (the owner's design goal of 2026-10-17; spec §21g): listings, the hull's valuation, the ship bought and sold through the market orders, the transfer of the people and the hands, the errand ashore | brief to write, after 51 and 53 |
| 61 | Fable | The land-avoiding route, provisional (spec §21i; the owner, 2026-10-17, brought in from the carried items): the course laid clear of the land and the dangers over the chart's own data for every captain and the player, the legs said as the plan | to plan in full at briefing; beside 51, before 58's tracks |
| 55 | Opus | The solo director and the gate's scenarios; the consent revision's draft; the gate document | brief to write, last |

## Package 50: the director proper (`freesail/agents/director.py` new; `agent.py`, `tools.py`, `harness.py`, `journal.py`, `seat.py`, the doors `remote.py`, `mcp_server.py`, `local.py`, `api.py`; `freesail/world/orders.py` for the channel's doubt and the brief's limits; `freesail/api/readings.py` for the truth's readings; `freesail/world/stations.py` for the director's binding; `freesail/core/world.py` and `core/replay.py` for the director's log in the save and the replay; `freesail/ui/console.py`, `ui/server.py` and `client/` for the director's station at the prompt, the log's pane and the replay view; `data/director/briefs/*.yaml` and `data/director/aboard.yaml` new; `docs/agents/Harness.md` a section; `docs/primer/` a chapter for the director; `docs/TechnicalSpec-M7b.md` §2 to §7 as built; `docs/dev/TuningNotes.md`; `tests/test_director.py` new, `test_world_orders.py`, `test_parity.py` (the director's surface by design), `test_replay.py`, `test_known_truths.py` truths 90 to 94)

Fable. Spec M7b §2 to §7; the proposal's §7.6; decisions 39 (the lead's first play at the
director's station), 43, 46 and 50 (brought forward; doubted, not refused). The world-order
channel as M5 and M6 built it (`orders.py`; 43's `seat:`/`unseat:` and the live `world:`
prefix; 45c's `mark:` and the lines kept for the record only) is the ground. Each item an
intent with the lead's reading; the intent binds.

1. **The director's station** (§2): a station of the kind `director`, bound on the World to
   no person of any ship (`Stations.bind("director", "", kind="director")`, made when a
   scenario asks `director: {brief: ...}` or the owner seats one), held through any door and
   by the player at the console (`--seat director`) or the browser; the fixed brief head as
   every station's, the body the player's brief (item 3); the tools the world orders, the
   truth's readings, the director's log, and the library, journal and stand-by every station
   has, with `stand by until the next glass | watch | <event>` as its clock. **The director
   sees the truth**: a reading surface of its own (`readings.director`: every ship's true
   position, heading, sail and state; the weather as it is and as the systems will make it
   for the next watch; the tide; the people aboard every ship and their states; the markets
   and the news), listed in the parity test as by design.
2. **The world orders, doubted not refused** (§3; decision 50). The channel's orders as they
   stand, with the director's needs added where missing: `weather:` (a change the systems
   could make from where they are, bounded by the climatology's season and the box), `ship:`
   with 43's `intent:` and `ship "X": intent ...`, `person:` as 52 will fill it (the hook
   only here), `aboard: <a thing found aboard>` from a table (`data/director/aboard.yaml`:
   a topmast found sprung, a cask stove, a seam working, the water foul, each with what it
   does in the part graph or the stores and its source), `news:`, `letter:`, `mark:`,
   `seat:`/`unseat:`. **The feasibility check**: an order that the simulation could not have
   produced on its own from where it is (a ship put inside the player's horizon in clear
   weather, a gale out of a steady glass, a letter from a port she has not touched) is not
   refused: the channel answers with the reason the act is doubted and the words "if you
   think the action you requested is still reasonable, you may enter it again along with a
   `[reason: ...]`, and it will be logged and performed"; entered again with its reason, it
   is performed, and the director's log keeps the act, the doubt and the reason together.
   The brief's hard limits (item 3) refuse outright, with the reason. Both the doubt and the
   refusal go to the director's log, never the play log; the effects alone reach the play
   log (decision 46, as 45c built it). **The orders are examples, not a rule** (the owner,
   2026-10-17, sent to the builder in flight): the director's brief never says only certain
   orders are allowed; it says a set of reasonable orders is given as examples and others
   should be attempted when thought reasonable; the same in every domain's contents (the
   things found aboard, the weather's changes, the ships and intents, the news), the tables
   being what the game can do and not what the director may say; an order in a form the
   game cannot perform is answered honestly and, re-entered with its reason, logged as an
   attempted act the game could not do, with the words, for the record.
3. **The brief and its limits** (§4): the player's brief as a file beside the scenario
   (`scenario.director.brief`) or given at the console (`director: brief ...`), with the tone
   of the voyage, the challenge wanted and the limits set (no gale above such a force, no
   enemy heavier than a brig, nobody dies, the war and the chart as they are); the limits
   enforced by the channel, not trusted to the model; starter briefs under
   `data/director/briefs/` (a quiet passage, an interesting passage, a hard cruise, a
   chase), the quiet passage the gate's.
4. **Sampling, the budget and the clock** (§5): the director samples on notable events and
   on its slow clock (every glass by default, every watch by the brief) under the pace rule
   as every station; the budget in the brief as samples a day and acts a day of the ship's
   time; spent, it stands by until the next day and says so in its log; the owner's
   compression untouched.
5. **The director's log, hidden and revealed** (§6): every act (an order given, doubted,
   re-entered with its reason, or refused; a thought it chose to write) to the director's
   log with its tick and its reason; hidden in play from every station and the player;
   revealed on request (`the director's log`, by the player at any time, which the director
   is told of), shown inline in replays beside the play log, kept in the save with the
   stations' acts and never in the play log or a station's journal; the browser's pane for
   it shut during play; the handover note of a director that leaves says only that it left.
6. **Truths 90 to 94** (§7) and the records: §2 to §7 as built; the Harness section (how to
   seat a director through each door, the brief's form, the log's reveal); the primer's
   chapter for the director (what it may do, the plausible cause, the `[reason:]`); the
   tuning notes (what the doubt caught in the first runs, the acts the starter briefs made
   on a day at seed 7, the suite as run).

### Package 50 as merged (2026-10-17)

Merged `--no-ff` from the builder's worktree (seven commits on `dc69b78`; 47 files, ~4,150
lines), ruff clean, the fast tier run on the merged tree by the lead; the builder's slow
tier whole and the pace tests alone passed on the final tree (`docs/dev/TuningNotes.md`,
"Package 50"). Built as briefed, with both of the owner's refinements of the day (every
domain's contents as examples, not a rule; an order the game cannot perform answered
honestly and logged as attempted when re-entered with a reason) and the lead's note on the
pictures (`chart` kept and described as the player's chart by account; no `ship_view`
above the game). No pin moved.

**Open items, carried:**

- `news:` and `letter:` are not channels (`message:` stands for a letter); both are
  attempted-and-logged today. A channel for the news when a package wants it (52 or 55).
- `nobody_dies` and `the_chart_as_it_is` are declared in the brief's limits and read to the
  director in words, with nothing yet for them to refuse.
- The player's purse and cargo are not in the truth's snapshot (the owner's design goal of
  the same day, spec §21g): 51 or 52 adds them.
- `ask the director`, `tell the director` and `show the director's journal` are refused
  until 52 gives the director a voice.
- The director's truths are `7b-90` to `7b-94` in `tests/test_known_truths.py`; M6 had used
  90 and 91 for its own, so the prefix tells them apart; left as named.
- Truth 90 is measured over a day of ship's time, not a week (a day shows every kind of
  entry; the week would cost a quarter of an hour a brief).
- A director's own chart: spec §12a, package 51. The director's attention and the ships'
  logs: spec §12b, provisional, package 51.
- The builder mended `tests/test_rollup.py`'s server speed test to the thousand of the
  compression change (one assertion that the slow tier on the main line had failed since
  `b9052c5`); kept.

### Package 52 as merged (2026-10-17)

Merged `--no-ff` from the builder's worktree (five commits on `e06b5d3`; 26 files, ~2,200
lines), ruff clean, the fast tier run on the merged tree by the lead; the builder's slow
tier alone and the pace tests passed on the final tree (`docs/dev/TuningNotes.md`,
"Package 52"). Built as briefed. No pin moved. The truth's snapshot now carries the
player's purse and cargo and the stations held (package 50's open item, closed).

**Taken another way, accepted by the lead, for the owner's overrule if he wants it:**

- **The rule of reach extended** from speaking to moving and binding: a held person is his
  holder's to move, and no other person is bound to a held station; refused outright in
  words naming the stations held, logged `director.refused`. Conservative (it refuses
  more, never less), and in the spirit of §9; spec §9 says so.
- The stations the rules answer (the masthead, the master's reckoning) answer by their
  rules whoever is seated above: the game's facts, which the player should not wait a
  glass for.
- `ask the director`, `tell the director` and `show the director's journal` stay refused:
  the player's accepted order line would go to the play log, which wants a change in
  `World.submit`; the player reaches the director by `director: brief ...`. A word to the
  director is 55's or a later package's, when wanted.
- Truth 7b-92's directed day uses `say as the harbourmaster of Falmouth` for its order the
  game cannot perform, since `say as the carpenter` now performs; the play log unchanged.

**Open items, carried:** `news:` as a channel; a word from the player to the director; the
director's fixed brief says the grammar topic lists every form, which it never has; a pilot
by trade with a port listed "pilot of <port>".

## Package 52: the director's voice (`freesail/world/people.py`, `orders.py` `person:` and `say as`; `freesail/agents/harness.py`, `agent.py` for the asked unseated person and the session kind; `freesail/core/events.py` for the word heard; `freesail/world/stations.py`; `docs/agents/Harness.md`; the primer's chapter 19 and the director's; `docs/TechnicalSpec-M7b.md` §8, §9 and §15 as built; `docs/dev/TuningNotes.md`; `tests/test_people.py`, `test_world_orders.py`, `test_director.py`, `test_captain.py`, `test_known_truths.py` truths 95 to 97)

Opus, after 50 (its channel and station are the ground; merge the head with 50 in before
starting, or the lead launches you after it). Spec M7b §8, §9 and §15; decisions 43, 46 and
50. Each item an intent with the lead's reading; the intent binds.

1. **People made from words** (§8): `person: make "Mr Fox", a Guernsey pilot of sixty, ...`
   makes a person with an outline from the words (a name, a role or none, an age, a place, a
   line of history), persisting in the world's people, bindable to a ship's station
   (`person: "Mr Fox" comes aboard as master`, M6 §11's outline), able to be ashore at a port
   (`person: "Mr Fox" goes ashore`, `... leaves the ship at <port>`), saved and replayed; the
   director's chief tool for the story, the player's at the console for scenarios.
2. **Speaking as the world** (§9): `say as <person>: <words>` puts words in the mouth of a
   person nobody holds (a person of the ship's company unheld, a person ashore, a person made
   in item 1, the pilot), heard where he is and journaled as his; `ask the <role>` and `tell
   the <role>` to an unseated person wait a sample for the director when one is seated, with
   a bound (the asker's stand-by wakes at the answer or after a glass), and are answered by
   the rules as now when none is; **the rule of reach**: the director speaks as anyone no
   model or player holds, never as a held station.
3. **The word heard** (§15): a word said between people and heard by another counts as "a
   word on deck" for the stand-bys (the owner's note 15 of gate m6a-2).
4. **The truth of who commands**: a station below the captain's is told who commands (a
   human captain at the prompt, a model captain, the rules-based captain by his book) in
   its session kind, as 42b told the captain's station (its leftover).
5. **Truths 95 to 97** and the records: §8, §9 and §15 as built; the Harness section; the
   primer; the tuning notes.

## Package 53: people in places (`freesail/world/people.py`, `places.py`; `data/people/*.yaml`, `data/ports/*.yaml` for the ports' places and people; `freesail/orders/` and `data/vocabulary.yaml` for `go`, `come aboard`, `draft a book`, `post`, the market in person; `freesail/orders/port.py`; `freesail/agents/tools.py` for the drafted book and the equal reach; `freesail/world/stations.py` and `agents/seat.py` for several stations of a kind; `docs/agents/Harness.md`; the primer; `docs/TechnicalSpec-M7b.md` §14, §16, §17 as built; `docs/dev/TuningNotes.md`; `tests/test_people.py`, `test_places.py` new, `test_orders_*`, `test_known_truths.py` truths 100 to 102)

Opus, beside 54 and 57; no dependence on the director. The ground is 52's people made from
words (a person made ashore at a port, come aboard, gone ashore; the galley a place) and
M6's places of the ship. Spec M7b §14, §16, §17; the owner's rulings of 2026-10-16 (a place is
an aspect of a person's state, not a simulation; the papers kept in a place are dropped).
Each item an intent with the lead's reading; the intent binds.

1. **Places and movement** (§14): any person, the player among them, goes where his duty
   allows and is where he went: `go to the cabin`, `go below`, `go on deck`, `go ashore` (by
   the boat, at a port's reach), `come aboard`; his place in his state and in the muster;
   and what he can do depends on it: the deck's orders from the quarterdeck or the deck,
   the market ashore in person or by the boat from aboard, a book read from anywhere (the
   owner's ruling). *The lead's reading:* the places exist (`places.PLACES`, `Person.where`);
   the work is the verbs, the player as a person with a place (on the quarterdeck by
   default), and the check in the order's domain with the refusal in words naming the way
   back ("you are in the cabin; go on deck to give the helm an order"). A stationed person
   below is below in the muster and his deck orders are refused until he comes up (truth
   100). Nothing moves a person's place by itself but the boat and the watch's routine.
2. **The port's places** (§14): the quay, the market, the counting house, the tavern, the
   pilots' office, each with what is done there and who is found there (the port's own
   people: the harbourmaster, a merchant, the pilots; 52's people placed there by
   `person: make ... ashore at <port>`); the player ashore buys at the market in person,
   aboard by the boat (truth 101). *The lead's reading:* a default set of places for every
   port in `data/ports/` with a port's own additions, read as words into `the port` and
   `where is`; a person ashore is at one of them; the market's orders check the place.
3. **Books drafted** (§16): `draft a book "night orders": ...` writes a standing-orders
   sheet, a note for the ship's papers or a manifest to buy and sell several goods at once,
   a book in the library with the person's mark; `post the book "night orders"` makes the
   sheet the standing orders, `give the book "manifest" to the boat` trades it in one
   errand (truth 102). The papers kept in a place aboard are not built.
4. **The equal reach** (§17): every stationed person may tell and ask any person aboard or
   within hail, go where his duty allows, read what is where he is, journal and stand by;
   the domain orders stay the station's authority. **Several stations of one kind**: the
   frigate's lieutenants as officers under the first, each with his place and his watch,
   the deck passing among them by the watch bill. *The lead's reading:* 45c's groundwork
   (`Stations.bind(name, person, kind)`) takes a second officer as `officer 2` of kind
   officer; the brief tells each who is first and whose watch is whose; `--seat` and the
   doors name him by his number or his person.
5. **Truths 100 to 102 and the records**: §14, §16, §17 as built; the Harness and the primer
   where they speak of places and the reach; the tuning notes.

## Package 54: needs (`freesail/crew/` the bill and the routine; `freesail/world/places.py` `Stores`; `freesail/world/people.py`; `data/ships/*.yaml` the rations and the stores; `freesail/orders/` and `data/vocabulary.yaml` for `short allowance`, `eat`, `drink`, `sleep`; `freesail/api/readings.py` the purser's reading and the person's needs; `freesail/agents/harness.py` the stand-by asleep below; `docs/agents/Harness.md`; the primer; `docs/TechnicalSpec-M7b.md` §19, §20 as built; `docs/dev/TuningNotes.md`; `tests/test_stores.py` new, `test_people.py`, `test_known_truths.py` truths 103 and 104)

Opus, beside 53 and 57; data and rules on the people, no dependence on the director. Spec
M7b §19, §20; the owner's rulings (by hand at a filled station to begin with, 2026-10-15;
never busywork). Each item an intent with the lead's reading; the intent binds.

1. **Provisions and water** (§19): the crew eat and drink on the watches' schedule; the
   ship's provisions and water fall by the ration a day for her complement (the period's
   ration from the Regulations, the figures in the ship files: a pound of biscuit, a pound
   of salt meat or its day's kind, a gallon of beer or a quart of water); the purser's
   reading says what remains and for how long; the market sells them; `short allowance`
   is an order that halves the ration with its effect on the hands (the crew factor's
   fatigue and a line on their temper); water found foul (50's `aboard:`) is drunk at a
   cost or not drunk. Truth 103. *The lead's reading:* `Stores` already counts water by the
   ton and provisions by the day; the day's fall by the complement is the new rule, and
   the reading its words; the ration table is data.
2. **Hunger, thirst and fatigue** (§20): named people, the player among them, have the three
   needs in three to five steps each, rising with the ship's time, eased by eating and
   drinking at a place with food (the cabin, the wardroom, below, the shore) or from the
   stores, and by sleeping below; notable then urgent lines to the person stationed only
   ("you are feeling a bit drowsy", "you are quite thirsty", "you are absolutely
   starving"); once a day to eat and drink and a sleep every day or two; by hand at a
   filled station (`eat`, `drink`, `sleep` as orders of the person), automatic where
   nobody is seated and for the crew; `stand by, asleep below until called` a stand-by
   of its own; never busywork: no line until the second step, and the lines spaced by
   watches. The milestone stops at the last step's urgent line and a person who falls
   asleep where he is; the ends are M7's with health. Truth 104. *The lead's reading:* the
   needs live on `Person` beside his place, stepped by the routine's clock; the crew's
   fatigue (`crew/hands.py`) stays the crew's and the people's fatigue mirrors it for a
   person who is also a hand.
3. **Truths 103 and 104 and the records**: §19, §20 as built; the Harness (the needs in a
   station's sample; the stand-by asleep); the primer; the tuning notes with the steps'
   hours and the reasons.

## Package 57: the rig through the generator (`tools/gen_ships.py`; `data/ships/frigate-36.yaml`, `brig.yaml`, `lugger.yaml` regenerated; `freesail/ship/` the sails' classes and the trim; the heavy-weather books (`data/standing_orders/`, `freesail/world/captains.py`); `client/shipview.js` and `freesail/agents/pictures.py` for the picture; `docs/dev/TuningNotes.md`; `docs/TechnicalSpec-M7b.md` §24's 57 as built; `tests/test_ships.py`, `test_shipview.py` or where the viewer's scene is tested, `test_known_truths.py` a truth for the lugger's lugs and one for the frigate's staysails)

Opus, beside 53 and 54. The owner's findings at gate 6c (the frigate's staysails; the brig's
set) and his notes on the Éclair's first cruise (`docs/playtests/2026-10-17-eclair-first-cruise/owner-notes.md`, with his pictures). The ship files are generated: every change goes through `tools/gen_ships.py` with its source cited beside it, as the files do today, never by hand. Each item an intent with the lead's reading; the intent binds.

1. **The frigate's staysails from Steel's list**: her complement between the masts (the
   main, middle, main topgallant, mizzen, mizzen topmast and mizzen topgallant staysails)
   with Steel's dimensions and canvas numbers, the shapes of the period (the lower and
   middle staysails four-sided, the topgallant staysails triangular), each with Steel's
   page beside it in the generator; the orders to set and take them in; the heavy-weather
   books reading them (lying to under a staysail; the storm staysails as M6's package left
   them); the ship file regenerated; **the pins it moves re-measured once**, the old figure
   beside the new and the reason in the tuning notes; the brig's set checked against
   Steel's for a brig and put right where it differs.
2. **The chasse-marée's rig put right** (the owner's notes 1 to 4): her topsails are lug
   topsails, fore-and-aft sails set above the lower lugs and trimmed with them, not square
   topsails braced by the yards; today `lugger.yaml` classes them `square` with Forfait's
   braces and lifts, and the trim rule braces them as yards while the lugs are sheeted as
   fore-and-aft sails, so that the two disagree at every point of sailing and the ship is
   taken aback on a shift or a turn (three times in the owner's cruise). *The lead's
   reading:* a class for the lug topsail, trimmed as a lug with the lower lug's sheet and
   dip, keeping the braces and lifts Forfait gives them (pp. 52 to 55, cited in the file)
   for the setting and the picture, not for a square trim (Lescallier 1791 p. 408, in
   `docs/design/VesselReferences-2026-10.md`, has the lugger's masts each with a topmast fidded
   abaft in an iron ring and *lug topsails*: the sail is a lug, whatever tackle it
   carries; the owner's citation of 2026-10-17); the lugs slung a third of the
   yard from the fore end with two thirds of the sail abaft and to leeward of the mast,
   dipped round it at the tack (the owner's confirmation of 2026-10-17; the settee and
   lateen rule alike where the generator meets them later); the lugger's pins re-measured
   once as in item 1. Where Forfait and the owner's reading of the lug topsail differ, say
   so in the tuning notes and take Forfait for the parts and the owner for the handling.
   **Set flying** (the owner's note of 2026-10-17, the lead's reading agreeing): the lug
   topsail is a flying sail, its yard swayed up from the deck with the sail bent on the
   topmast halyard, sheeted to the lower lug yard's peak, and sent down whole when taken
   in; nothing is furled aloft, and in a breeze the topmast itself is struck and housed
   (Forfait pp. 52 to 55 and Lescallier p. 408 for the lugger; the Deal and Cornish
   luggers alike). The same class covers the royals of Steel's day, set flying with the
   yard sent up and down with the sail and sent down at night or in a breeze (Steel 1794;
   Falconer, art. ROYAL), and the studding sails later. So a sail class *flying*, with two
   states, *sent down* (on deck or in the top) and *swayed up*, worked by hands on deck
   rather than topmen aloft, never reefed aloft, and taken in whole as the wind rises; the
   lugger's topsails in it now, the frigate's royals where Steel's practice of 1794
   supports it (the builder checks Steel's article and says in the tuning notes where the
   sources disagree), the viewer drawing a sent-down sail as absent and its yard on deck.
3. **The viewer and the picture** (the owner's note 5 and the lead's finding of 18:29):
   the draw order by the aspect (the sail before the mast hides it from ahead; from
   astern the mast hides the sail), the yards' brace shown in the drawing, the lug drawn
   on its side of the mast with the yard slung as the file has it, on either tack and
   running; the station's picture (`pictures.py`) the same, since it is the page's drawing.
4. **Truths and the records**: a truth that the lugger close-hauled on either tack at seed
   7 shows every lug to leeward of its mast and no sail aback through a tack and a wear,
   and one that the frigate lies to under a staysail by the heavy-weather book in the
   gale trial; §24's 57 as built; the tuning notes (Steel's and Forfait's pages, the pins
   moved, found on the way).
