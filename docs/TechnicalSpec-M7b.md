# FreeSail: Technical Specification, Milestone 7b (The director)

**Draft of 2026-10-16 for the owner's review.** Companion to `docs/TechnicalSpec-M0-M2.md`,
`-M3.md`, `-M3b.md`, `-M4.md`, `-M5.md` and `-M6.md`, whose conventions hold. By the owner's
word of 2026-10-16 (decision 47) this milestone runs before M7 (powder): it depends only on
M5's world orders and M6's agent plumbing, both in, and it is what opens the world for the
experimentation the owner wants. The proposal's M7b (§7.6: the director agent on the
world-order channel with a brief, a hidden director's log and a replay view) is its core;
the owner's notes of gate m6a-2 (`docs/playtests/2026-10-13-gate-m6a-2-owner-runs/`) and
the decisions of October grow it to five parts:

- **7b-i. The director proper:** an agent above the game on the world-order channel, with a
  brief and its guardrails, a hidden log revealed on request and inline in replays,
  sampling on events and the slow clock, a budget.
- **7b-ii. The director's voice:** the director answering as the unseated people of the
  world, `say as <person>`, people made from words who persist, the point of interest.
- **7b-iii. The observed world:** a world with no player's ship, watched from the
  director's station with world orders; the player at a station on another ship; the
  replay of such a station from a save.
- **7b-iv. People in places:** a person's place as an aspect of his state, aboard or
  ashore, tied to what he can do there; the player on the shore; books drafted; the equal
  reach between stationed persons. (Not a simulation of each place: the owner, 2026-10-16.)
- **7b-v. Needs:** provisions and water consumed, hunger, thirst and fatigue in a few steps
  with the master's cautions, "stand by, asleep below until called", the hooks for M7's
  health.
- **7b-vi. Fishing, and the glass on a near ship:** fishing for the player at the level the
  game can honestly simulate, with the far-detail fisherman given the same catch so the two
  bodies agree; and what the glass shows of a near ship's work and manoeuvre in hand (the
  owner, 2026-10-17).

*Proves: a voyage is two stories, the one the player lived and the one that was arranged;
and the world runs, peopled and observed, with no player's ship at all.*

The rules of the earlier milestones run through every section (everything inward reachable
by an order or a reading, everything outward through something the ship models; the world
keeps the truth and the captain his account; a station is a person aboard and a person
aboard is a station, what no model holds the rules hold). This milestone's rule is the
proposal's own: **the director acts only through plausible causes.** It cannot move the
player's ship, change a sail or countermand an order; it changes the world the ship is in,
and only in ways the simulation could have produced on its own. Every director's act is
something that could have happened anyway, so the physics stays honest and the player's
agency whole. And its corollary from decision 46: **a world order is never shown as sent;
the play log carries its effects.**

---

## Part 7b-i: The director proper

### 1. What 7b-i proves

A model above the game shapes a voyage through world orders alone, within a brief the
player wrote, on a budget, and the record of what it did and why is a second story read
after the voyage.

### 2. The director's station (`freesail/agents/director.py` new; `agent.py`, `tools.py`, `harness.py`, the doors)

A station of a new kind, `director`, held through any door (the MCP bridge, the local
runner, the API door) and by the player at the console or the browser. It is bound to no
person of any ship: its binding is on the World (`Stations.bind("director", "", kind=
"director")`, made when a scenario or the owner asks for one), its authority the owner's
on the world-order channel and nothing on any ship's. Its brief head is fixed as every
station's is (the consent brief's rule); its body is the player's own brief (§4). Its tools
are the world orders (§3), the truth's readings (§5), the director's log (§6) and the same
library, journal and stand-by every station has, with `stand by until the next glass` and
`until <event>` as the slow clock.

**The director sees the truth.** Its readings are the world's, not an account: every ship's
true position, heading, sail and state, the weather as it is and as the systems will make
it, the tide, the people aboard every ship and their states, the markets, the news. A
reading surface of its own (`readings.director`), listed in the parity test as by design
(the director is not a station on a ship).

**As built (package 50, 2026-10-17; `freesail/agents/director.py`; `tests/test_director.py`;
`docs/primer/20-the-director.md`; `docs/agents/Harness.md` §19).** The kind `director` is a
factory in `agent.STATION_FACTORIES` and a `WORLD_KINDS` entry: a kind that is the game's and
not a ship's, which `world.stations.Stations.names()` lists only when it was bound
(`bind("director", "", kind="director")`), so that a world with no director is as it was
(every pinned passage stands). It is bound when a brief is given: by a scenario's `director:
{brief: ...}` at the World's making, by `director: brief ...` at the prompt (an input,
`director_brief`, replayed), or when the player sits at it (`--seat director`, the binding
an input before the seat's line). Its `Authority.DIRECTOR` and `DIRECTOR_DOMAIN` refuse every
order of any ship in words, the deck's conversation included (it has no place aboard:
`STATION_PLACES[DIRECTOR]` is none, so nothing said on deck reaches it and it says nothing
there); the readings and the queries pass. Its tools are the station's own (`tools.
DIRECTOR_TOOLS`, `Tool.director_only`, offered at the director's station alone and refused in
words at every other): `world_order(text)`, the channel's door with the brief's limits and
the doubt (`director.direct`), and `truth()`, the reading surface; beside the library, the
journal (which is the director's log), `read_journal`, `stand_by`, `stand_down`, `opt_out`,
`shelve`, `readings`, `read_log`, `state` and `submit_order` for the readings; never
`hand_over` or `handover_note`; at a door that carries pictures, `chart` and not `ship_view`
(the director stands on no deck; `call` refuses the view in words), the chart's words at
this station its own (`Tool.at_director`, `tools.description_of`): the player's chart as
the browser page draws it, his ship by her account and no other ship, nothing of the
truth, for planning; a director's own chart is a package to come. The session kind is its own (`SESSION_DIRECTOR`: above the
game, the player at the prompt of his ship below it). **The truth** is `readings.
director_readings(world)`, a surface and not a registry row (a row is read at the prompt
and at every station alike, and truth 81 gives the captain no road to the truth): every
ship's true position, heading, speed, sail and state with her captain's intent and her
brain's state, her bearing and distance from the player's ship; the weather as it is at the
ship and as the systems will make it a watch on (the systems moved along their tracks or
by their velocities, read, and put back), with the systems by name; the tide; the people
aboard every crewed ship; the markets' prices; the wars and the ports' news. A book, put
back with `shelve`. The lead's `readings.director` is this function; the parity test lists
the two tools as by design (`TOOL_COUNTERPARTS`) and the console's three requests
(`the director's log`, `two stories`, `director:`) as the player's own.

### 3. The world orders (`freesail/world/orders.py`)

The channel as M5 and M6 built it, with the orders the director needs added and the
guardrail enforced on every one:

- **The weather:** `weather:` as it stands (a low with fronts, a squall line, the glass),
  with a bound: a change the systems could make from where they are (a front not more than
  so many hours sooner or later than the climatology allows, a wind not stronger than the
  season's record for the box); refused in words beyond it.
- **Ships:** `ship:` as it stands, with 43's `intent:`; `ship "X": intent ...` to change a
  mind; a ship put on the sea only where she could be (not inside the player's horizon
  unless the visibility hides her; not aground).
- **People:** `person:` as M6 §11 outlined it (`person: "Mr Fox" comes aboard as master`),
  made real here (§8).
- **Aboard:** `aboard: the fore topmast is found sprung`, `aboard: a cask found stove`, the
  carpenter's and the purser's reports, from a table of things that can be found aboard
  (`data/director/aboard.yaml`), each with what it does in the part graph or the stores.
- **The news and the letters:** `news:` (a war declared, a peace made, a price heard) and
  `letter:` as they stand.
- **The mark:** 45c's `mark:` point of interest.
- **The seat:** 43's `seat:` and `unseat:` by the owner's grant and budget.

Every order is journaled at its tick, replays, and is kept for the record only (decision
46): the play log carries the effects (the sail sighted, the glass falling, the carpenter's
report), never the order. **An order that would not be a plausible cause is doubted, not
refused** (the owner, 2026-10-17, decision 50): the channel states the reason the act is
doubted and says that if the director thinks the act still reasonable it may be entered
again with a `[reason: ...]`, and it will be logged and performed; entered so, it is done,
and the director's log keeps the act, the doubt and the reason together, which is the data
by which the sets of reasonable acts are refined. Only the brief's hard limits (§4, the
player's own) refuse outright. The doubt and the refusal both go to the director's log, not
the play log. **The orders are examples, not a rule** (the owner, 2026-10-17): the director
is not told that only certain orders are allowed; its brief says that a set of reasonable
orders is given as examples and that orders beyond them should be attempted when thought
reasonable, so that in testing the director is unconstrained within the plausible-cause
rule and tries a wide variety of things, and the record shows what is good, bad, useful or
useless. The same holds in every domain's contents, not the order forms alone (the owner's
clarification of the same day): the things found aboard, the weather's changes, the kinds
of ship and intent, the news and the letters are each given as examples of reasonable
things, never as the list of what is allowed, and the brief says that within each domain,
and in domains the examples do not name, the director should attempt whatever it thinks
reasonable; the tables are what the game can do, not what the director may say. An order
in a form the game has no way to perform is answered honestly ("the game
has no way to do this as said; say it another way, or enter it again with a `[reason:]` and
it will be logged as attempted"), and re-entered with its reason it is logged in the
director's log as an attempted act the game could not perform, with the words: the data for
what to build next.

**As built (package 50).** `aboard:` is a channel of its own (`CHANNELS`, the vocabulary's
list), its things the table's (`data/director/aboard.yaml`, `orders.aboard_table`): `the
<spar> is found sprung` (the spar's condition cut to the table's thirty, so that it carries
away the sooner under a press of sail; the carpenter's report), `a cask found stove` (a ton
of water from the stores; the cooper's), `a seam found working` (the carpenter's report;
nothing of the hull is modelled yet, said so in the table), `the water found foul` (the
stores' water marked foul, `Stores.foul`, said on the purser's page and left for package
54's needs); each a notable `aboard.found` line of the play log that never names the order.
`news:` and `letter:` are not channels: the news is a port's and the nations' (read in the
truth), a letter is `message:` as it stands; the brief's "as they stand" is kept so. **The
doubt** is `orders.doubt(world, order)`, by channel (the primer's chapter 20 has the table):
a new sail inside the lookout's horizon in clear daylight (the height of a brig's trucks,
cut to the visibility) or on the land by the chart; a mark inside the horizon; a low deeper
than the season's floor for the month and the box (`MonthTable.central_hpa`), a deep low
(twelve hectopascals under the background) within three hundred kilometres out of a glass
that has not been falling, a waypoint faster than the season's fastest low with a half over
or deepening below the floor; a cutter with a letter from a port beyond sixty miles; a price
moved by more than three parts in ten; a thing found aboard with no cause (`plausible_when`:
a strain line of the spar's or above the figure in the last watch, or a fresh mean wind; a
sea beyond smooth; five days out). A mind changed, a person named, a letter left at a port, a
port's stance and the seat are never doubted. `parse` peels the `[reason: ...]` tail into
`WorldOrder.reason` (`split_reason`); the channel is never doubted for the scenario or the
owner's `world:` order, which are their own word: the doubt is the director's door's
(`director.direct`). **The owner's refinement (2026-10-17)**: the forms, and every domain's
contents (the table's things, the weather's changes, the kinds of ship and intent), are given
to the director as examples of reasonable orders and never as the list of what is allowed,
and the brief says that within each domain and in domains the examples do not name the
director should attempt whatever it thinks reasonable. So an order in no form the game has,
or free words a table does not know (`aboard: the cook reports the beef cask found rotten`,
`news: war declared ...`, `say as the carpenter: ...`), is not refused as "not allowed" but
answered honestly (`director.NO_WAY_WORDS`: the game has no way to do this as said; say it
another way, or enter it again with a `[reason: ...]` and it will be logged as attempted),
written in the log as `director.unperformed`; entered again with its reason it is written
as `director.attempted` with the words and the reason, performed not at all, counted against
no budget: the data for what to build next. The brief's limits alone refuse
(`director.refused`). A world order given while a station acts is the station's act
(`core.acts`, kind `world_order`, applied aside so that its effects' lines are the order's
own), never an input, and a replay by the acts gives it again through the channel; the
player's order at his seat is an input of its own (`director_order`), replayed through the
director's door so that the doubt and the log are what they were.

### 4. The brief and its guardrails (`data/director/briefs/*.yaml`; `freesail/agents/director.py`)

The player writes the brief: the tone of the voyage (a quiet passage, a hard-luck cruise, a
chase), the kind of challenge wanted, the limits set (no gale above such a force, no
enemy heavier than a brig, nobody dies), the period's bounds the director must keep (the
war as it is, the chart as it is). The brief is a file beside the scenario
(`scenario.director.brief`) or given at the console (`director: brief ...`); its limits are
enforced by the channel, not trusted to the model: a world order outside the brief's limits
is refused as outside the brief, and the refusal logged. Starter briefs under
`data/director/briefs/` (a quiet passage, an interesting passage, a hard cruise, a chase),
one of them the gate's.

**As built (package 50; `director.DirectorBrief`).** A brief is `name`, `tone`, `challenge`,
`limits`, `cadence` (`glass` or `watch`) and `budget` (`samples_a_day`, `acts_a_day`), from
a starter's name (`quiet-passage`, with or without its article), a file, the mapping itself,
or the player's words at the prompt (`director: brief <words>`: the tone, no limits beyond
the channel's doubt, the defaults for the rest; `director: brief` alone reads it). The
scenario's `director: {brief: ...}` is read at the load (refused in words when it cannot
be) and kept in the scenario as the mapping, so that the save carries it whole and the
replay has it from tick 0; the prompt's is an input. The limits the channel enforces
(`DirectorBrief.limit_of`): `wind_max_kn` (or `gale_max_force`, turned to knots by the
Admiralty scale's tops), judged by the surface wind a `weather:` order's system would make
at its tightest (the Gaussian bell's steepest gradient at one radius, the gradient-wind
rule and `SURFACE_SCALE`, as the systems' own wind is made: a low of 965 hPa and 450 km
blows 42 knots, one of 1000 hPa 16); `enemy_heaviest` (a `ship:` whose nation is at war with
the ship's own and whose description ranks above the limit by `captains.SIZE_RANK`);
`nobody_dies` (a thing found aboard whose `harm` is deadly: none in the table yet);
`the_war_as_it_is` (a port closed to or opened to the ship's own nation);
`the_chart_as_it_is` (declared, refusing nothing yet: a mark is not the chart). The brief's
body is the last part of the station brief, after the fixed part (`DIRECTOR_BRIEF`), and the
station is refreshed with it when the brief changes or a save is loaded. The four starters:
the quiet passage (force 6, a cutter, four acts a day; the gate's), the interesting passage
(force 7, a brig, six), the hard cruise (force 9, a frigate, eight) and the chase (force 7, a
brig, six).

### 5. Sampling, the budget and the clock (`harness.py`; `core/world.py`)

The director samples on notable events and on the slow clock (every glass by default,
every watch by the brief), under the pace rule of M6 §12 as every station does (the clock
to 1x while its sample is open), and lockstep as an option. **The budget**: the brief gives
it in samples per day of the ship's time and in acts per day (so that it cannot make every
day a hurricane); spent, it stands by until the next day; said in its log. The owner's
compression is untouched: a director that stands by for a watch lets the player run at
300x.

**As built (package 50; `director.DayBudget`, `World.director_state`).** The cadence is the
brief's: `cadence_policy("glass", "director", world=)` reads every watch where the brief
says so, every glass else, and the notable and urgent lines at either; a door's `--cadence`
stands over it. The budget is counted by the ship's calendar day on the World (so that a
model's harness and the player's seat share one count), the samples at each sample (a
fold into an open turn is none), the acts at each world order performed (a doubt, a
refusal, an attempt and an unperformed order cost none). Either count spent, the director is
held until the tick the ship's day turns (`held_until`), said in its log and in the result
of the act that spent it: no sample opens meanwhile, whatever the policy, a stand-by or an
urgent line would do; the day turned, the next sample says the budget is renewed. Every
sample carries the budget as it stands in a notice. The save holds the brief and the day's
counts (`"director"`); a replay by the acts re-counts the acts and takes the save's samples.

### 6. The director's log, hidden and revealed (`freesail/agents/journal.py`; `core/replay.py`; `ui/`)

Every act of the director (an order given, an order refused, a thought it chose to write)
goes to the director's log with its tick and its reason, hidden during play from every
station and the player (a director you can see coming is not a director), and:

- **revealed on request**, by the player at the end of the voyage or at any time he asks
  for it by name (`the director's log`), which the director is told of in its sample;
- **shown inline in replays**, beside the play log at each tick, so that a voyage reads as
  two stories;
- **kept in the save** with the stations' acts, never in the play log or a station's
  journal; the handover note of a director that leaves says only that it left.

The browser gains a pane for the director's log, shut during play and opened by the same
request; the console the reading.

**As built (package 50).** The director's log is the station's own journal (`journal_of(world,
"director")`, bound to no person; `director.KINDS`): `director.brief`, `.order`, `.doubted`,
`.reentered` (the act, the doubt and the reason in one entry), `.refused`, `.unperformed`,
`.attempted`, `.budget`, `.revealed`, and `note` for a thought (the `journal` tool, the free
text of a reply and an `answer`, none of which is a line of the play log). It is kept in
the save as a station's journal is (`agent_journals["director"]`) and replayed as a
station's notes are, by either road. **Hidden**: every line of the director's in the log
(its seating, its stand-bys, its leaving, its binding) carries the actor `the director`,
which `events.for_the_record` makes record-only beside the `world.order` kind, so that no
station's sample or `read_log`, no browser play log or `/api/log`, and now the console's
own view carry it; the director is left out of the `state` tool and the `stations` reading
as the other stations read them; `ask`, `tell` and `show the journal of` the director are
refused in words. **Revealed**: `the director's log` at the console or in the browser's
order box (`director.reveal`): a driver's line `director.revealed` for the record (an
input, replayed), the log's entry, the director's notice in its next sample, and the lines;
the browser's pane (`#director-panel`, in the ship view's place beside the play log) opens
on the answer and is shut until then; `GET /api/director/log` is the same reveal. **Inline
in the replay**: `two stories [N]` (`director.two_stories`) prints the play log with the
director's log inline by tick, each of its entries marked `D`. A director that stands down
leaves its note in its log, and its line says only that it left a note there.

### 7. Truths for 7b-i (behavioural)

- 90. A director on the quiet-passage brief raises no gale above the brief's force in a
  week at seed 7; an order beyond it is refused with the reason in the director's log.
- 91. A world order given by the director appears in no station's sample and no play log;
  its effect does, when met.
- 92. The director's log is empty to every station and the player until asked for, and
  then shows every act with its reason; a replay shows it inline.
- 93. A director on a budget of three acts a day gives no fourth; the sample says the
  budget is spent.
- 94. A directed voyage saved and replayed gives the same log, the director's acts among
  the inputs.

**As built (package 50; `tests/test_known_truths.py`, truths 7b-90 to 7b-94; M6 had used the
numbers 90 and 91 for the regatta and the parity, so the director's are cited as 7b-90 to
7b-94).** The frigate at seed 7 off the Lizard under the climatology's weather, a day with
the fake director (`fake.director_above_the_game`) on the quiet-passage brief and the fake
captain beside it. 7b-90: the gale's low refused by the brief with the reason, the soft low
appended, and the limit holding for a week of gale orders by the same rule. 7b-91: the
captain's nineteen samples carry no order and no word of the director; the cooper's report
and the sail sighted are in them. 7b-92: the log empty to every station until asked, then
every act with its reason, the two-stories view inline. 7b-93: three prices given on a
budget of three acts, the fourth refused with the words, the hold said. 7b-94: the day's
save replayed by the transcript and by the acts to the same digest and the same director's
log entry for entry. No recorded passage's pin moved: none has a director, and a world with
no director bound is as it was (`tests/test_director.py`).

## Part 7b-ii: The director's voice

### 8. People made from words (`freesail/world/people.py`; `orders.py` `person:`)

`person: make "Mr Fox", a Guernsey pilot of sixty, ...` makes a person with an outline from
the words (a name, a role or none, an age, a place, a line of history), who persists in the
world's people, may be bound to a station of a ship (`person: "Mr Fox" comes aboard as
master`, M6 §11's outline), may be ashore at a port, and is saved and replayed. `person:
"Mr Fox" goes ashore`, `... leaves the ship at <port>`. The director's chief tool for the
story; the player's too, at the console, for scenarios.

**As built (package 52, 2026-10-17; `freesail/world/orders.py`, `people.py`, `places.py`;
`tests/test_people.py`, `test_world_orders.py`, `test_director.py`; truth 7b-95).**
`person: make "<name>"` and, after commas in any order, what the words say of him: who he
is (`a Guernsey pilot`, an age at its end, `of sixty`), an age (`aged forty-five`, `sixty
years old`), a place aboard (`aboard in the cabin`, `in the gunroom`) or ashore (`ashore at
Brest`, `at Brest`), and any other words as his line of history. The role is the people's
table's word at the end of who he is (`pilot`, `master's mate`), else its last word, or
none; who he is as said is his rank (`Guernsey pilot`, `merchant of Bristol`); the outline
keeps the age and the words he was made from (`Outline.age`, `Outline.said`) and says him
in one sentence ("Mr Fox, Guernsey pilot, sixty years of age, who knew the captain's
father."), which is what a model bound to him reads in its brief. With no place said he is
aboard, in the cabin (his trade's place for a cook or a cooper); ashore with no port, at
the nearest. He is among the world's people from then on (`the people`, `where is`, `find`
by his name and, after every name, by his role). The moves: `person: "Mr Fox" comes
aboard [as <station>]` (from his port to the quarterdeck, a notable `person.aboard` line;
a station of that name or kind bound to him, quietly within the order so that the replay
binds it again, with its own `station.bound` line; `as <a role no station has>` bears him
in that role and binds nothing), `person: "Mr Fox" goes ashore` (at the nearest port) and
`person: "Mr Fox" leaves the ship at <port>` (a notable `person.ashore` line; a station
bound to him goes back to the wardroom file's holder where he is another and aboard, the
master's to Mr Harvey, and is unbound else). The man who keeps the reckoning and the one
who commands are not put ashore (the player ashore is §14's). **The doubt** (decision 50):
a move where no boat could carry him, beyond `BOAT_REACH_NM` (six miles, judgement: a
shore boat or a pilot's comes off to a ship lying off the port) of his port or the one
named; a person made and a word said are never doubted (a supernumerary the story names,
and a man's words, want no cause of the sea's). The old forms (`person: <role> "<name>"
aboard in the <place>`, `... ashore at <port>`) stand as they were. Saved and replayed as
the world order that made him (the input, or the director's act), the binding with it; a
load gives the save's bindings back only when the save was replayed to its end, since a
person made after the tick handed over at is nobody yet. **A man of the muster by his
trade** (the cook, the cooper, a steward: an idler the named few do not hold) is found by
his trade when the voice reaches him (`People.of_the_company`) and drawn from the muster
under his own name at his trade's place (`TRADE_PLACES`: the cook in the galley, the
cooper in the hold), one of the people from then on; nothing draws him otherwise, so a
world in which nobody speaks as him or asks him is as it was. **The galley** is a place
now (under the forecastle, open to the waist), listed after the hold.

### 9. Speaking as the world (`orders.py` `say as`; `harness.py`)

`say as <person>: <words>` puts words in a person's mouth: a person of the ship's company
nobody holds (the carpenter, the cook), a person ashore (the harbourmaster, a merchant, a
tavern's talk), a person made in §8, the pilot; heard where the person is (§13) and
journaled as his; and answering what a station asked of an unseated person. **The rule of
reach**: the director speaks as anyone no model or player holds, never as a held station,
whose words are its own. `ask the <role>` and `tell the <role>` to an unseated person wait a
sample for the director when one is seated (the rules answer as now when none is), with a
bound (the asker's stand-by wakes at the answer or after a glass).

**As built (package 52; `orders.py` `say as`, `reach`; `director.py` `ask_unheld`,
`answer_questions`; `orders/stations.py`; `harness.py`; truths 7b-96, 7b-97).** `say as
<person>: <his words>` is the `say` channel's (a bare `say <words>` is the deck's
conversation still): the person is one of the people or a man of the muster by his trade
(§8); his words, quotes peeled, are a notable `person.spoke` line of the play log in his
name where he is ("Mr Squire, the cook, in the galley: Pease and pork, sir."), never the
order, heard by the stations held within earshot (`places.earshot`: the quarterdeck, the
deck and the galley open to one another, every other place alone), each told in its next
sample under `heard`, and journaled as his (`journal.person_journal`, `person.said`: his
journal by his name, the same object the station bound to him reads back, package 45c). A
person ashore is heard aboard only while the ship lies within a boat's reach of his port;
farther, and for a stranger never made, the game has no way to do it as said, and says
how (a letter, or make him first). **The rule of reach** (`orders.reach`): nobody speaks
as, moves, or binds another to the station of, a person a model or the player holds (a
harness, the player's seat, the captain by the player at the prompt while no model holds
it and he is seated nowhere else: `held_stations`). It holds whoever gives the order (the
channel refuses it in `apply`), and at the director's door it is a refusal before the
brief's limits, in the director's log as `director.refused`, its words naming the stations
held ("the stations held now: the officer of the watch (Mr Pearce, a model); the captain
(Captain Bowen, the player at the prompt)"); the truth reads them too. Moving a held
person and binding a held station are read as within the rule (the holder's person is
his to move), the lead's to confirm. **The asked unseated person**: with a director seated
(a model's harness or the player's seat), `ask` and `tell` put to a person nobody holds (a
station unheld bound to him: `ask the first lieutenant ...` with nobody at the officer's;
or a person no station is bound to: `ask the cook ...`, `tell Mr Fox ...`) are said where
they were said ("The officer of the watch (Mr Pearce), on the quarterdeck, asks Mr Squire,
the cook (in the galley): what is for dinner?"), journaled in his journal and the
director's log (`director.asked`), and put to the director as a word in its next sample,
waking its stand-by, with whom it was put by and until when it waits. Its answer as him
(`say as`) costs none of the day's acts and goes back to the asking station as a word
under his name (`harness.deliver_answer`), ending its wait and waking its stand-by; with
no answer in a glass (`QUESTION_BOUND_S`) the asker is told so by a word, which wakes it
too. A word told an unheld station is kept in its journal as before and the director told
besides. With no director seated, everything is as it was: `ask the cook` is refused in
the words it always was, and no man is drawn. The stations whose rules answer keep them
whoever is above (the masthead's sight, package 45c; the master's reckoning, the reading
form): the facts are the game's and the lead's reading is that the player should not wait
a glass on a model for what the game knows. `ask the director`, `tell the director` and
`show the director's journal` stay refused: a word to it from the prompt would want the
order's accepted line kept from the play log, which is `World.submit`'s and beyond this
package; the player's word reaches it by the brief (`director: brief ...`).

**The truth of who commands** (42b's leftover; `agent.commander_of`, `under_whom`). A
station below the captain's is told in its session kind who commands: "a play session with
a human captain at the prompt" (and, where the rules-based captain sails her by his
intent, "...; the game's rules-based captain sails her by his book under him until he
takes her in hand"); "a play session for its own sake, with no human captain over you; a
model holds the captain's station and commands the ship"; or "...; the game's rules-based
captain commands the ship by his book" (the player seated elsewhere, or the ship
another's). The kinds before the semicolon are the consent brief's, unchanged. The desk
tells it at the seating (`session_kind_of(..., world=)`), and the station's next sample
says so once when it changes ("Who commands has changed: this session is now ...").

### 10. Truths for 7b-ii

- 95. A person made from words is on the muster of the ship he joins, holds the station
  he is bound to, and is there after a save and a replay.
- 96. A question to the cook, with a director seated, is answered in the cook's words at
  the galley and heard by those within earshot; with none, by the rules as before.
- 97. `say as` a held station is refused.

**As built (package 52; `tests/test_known_truths.py`, truths 7b-95 to 7b-97).** The frigate
at seed 7 off the Lizard under the climatology's weather, two hours with the fake director
on the quiet-passage brief giving its voice (`fake.director_above_the_game(..., answers=)`)
and a fake officer of the watch who asks the cook. 7b-95: Mr Fox made at Falmouth, brought
aboard as master (doubted, forty-two miles off, and entered again with the reason), among
the people, the master's station his (a model seated there is in his place, his outline
in its brief), his own words said on the quarterdeck; the save replayed by the transcript
and by the acts to the same digest, Fox and his binding the same. 7b-96: the officer's
question to the cook, the director's sample carrying it, the cook's answer at the galley
heard by the officer and returned to him as a word within the glass, no act counted; with
no director seated, the refusal word for word as in a world with no brief. 7b-97: the
captain's and the officer's mouths refused by the rule of reach in the director's log, no
word said in either name, never an order on the channel. No recorded passage's pin moved:
none has a director or a `person:` order, and a world with neither is as it was.

## Part 7b-iii: The observed world

### 11. A world with no player's ship (`core/world.py`; `ui/console.py`, `ui/server.py`; the drivers)

A scenario may have no player's ship (`ship: none`, or `director: observe`): the world
runs its business, its ships under their captains (43's brains), its weather and tides,
with the game's centre (the promotion's, the chart's, the pace rule's) wherever the
observer looks: the chart's view, or a ship named (`follow "Palinure"`). The readings that
assume a ship answer "no ship followed" in words until one is followed; the orders of the
ship are refused in words; the world orders stand. The console and the browser open on
such a world at the director's station by default. **The lead's reading of the cost:** the
World's construction assumes a ship in the readings registry, the lookout, the reckoning,
the pace rule's centre and the drivers; the package that builds this makes the ship a
followed ship rather than a given one, with the player's ship the followed ship by default,
and measures what moved (nothing pinned should).

### 12. The player on another ship, and the replay of a station there (`crews.py`; `core/replay.py`)

`--seat captain --ship <id>` for the player (43 left it): the drivers' centre follows the
ship the player is aboard, the player seated under the same contract as a model there; and
a save with a station on another ship replays that station's acts as it replays the
player's (43's checkpoint carries the other ship whole; the acts are keyed by ship).

### 12a. The director's chart (`freesail/agents/pictures.py`, `tools.py`; `client/map.js` or a painter of the server's own)

The director holds the `chart` tool today as every station does through a door that
carries pictures, and package 50 says at that station what the picture is: the player's
chart as the browser page draws it, the player's ship by her account, no other ship and no
truth on it (the owner's question of 2026-10-17; the truth is in words from `truth`). A
director planning from it would read the captain's guess as the world. This section gives
it a chart of its own: every ship drawn where she truly is and named, the player's ship by
truth with her account faintly beside it and the master's doubt about the account, the
coast, the dangers and the marks as the chart has them; `span` as the player's chart has
it, centred on a named ship or a named place (`chart span=coast at="Palinure"`), the
followed ship when none is named (§11). **The design question is where it is drawn.** The
browser page paints every picture today, and sending it the truth for an off-screen draw
puts the truth on the player's machine; the builder chooses between a painter of the
server's own for this one view (preferred: headless, no page needed, and nothing of the
truth leaves the server) and the page painting it from a truth the server sends for that
draw alone, with the lead's reading of the cost in the hand-back. The picture is a book as
every picture is (shelved with a note). The director has no `ship_view`.

### 12b. The director's attention: focus, and the ships' logs (provisional; `freesail/agents/tools.py`, `harness.py`; `crews.py`)

Booked on the owner's word of 2026-10-17; the mechanics provisional, kept or reshaped by
what the first director runs want, the goal not: **the director can know the basic
history of any ship, far-detail or not.** Package 50's director reads one log, the player's
ship's, and the truth as a snapshot (§2); what a crewed ship does between its samples
reaches it only as a changed state. The owner's three tiers of attention order what
reaches it unasked: first the player's ship, where events matter most (her notable lines
in every sample, as today); second the ships involved with the player's in one way or
another, which need close attention (focused, below); third the ships not likely to be
involved, which need some attention or which the director wants for a reason of its own
(the truth's snapshot, and their history on request). This section gives it the attention
and the history:

- **Focus.** `focus ship="Palinure"` and `unfocus`: a focused ship's notable lines arrive in
  the director's sample tagged with her name, as an urgent line wakes a watcher, until it
  unfocuses her; several at once, up to the crewed cap, since a dealing with the player's
  ship is always between two or more. Focus is attention, not the centre: it does not
  promote her, move the chart or change the pace (the centre is `follow`'s, §11). A far
  ship focused gives her state changes in words, the sample saying she is in the far
  shape; a director that wants her crewed early says so by a world order in plain words,
  doubted as any other, and the owner's cap stands.
- **The ships' logs.** The log tool takes a ship and a kind family (`read_log ship="Palinure"
  kind="sighting" since_tick=.. before_tick=..`; the kinds the log's own: helm, sail,
  sighting, hail, business, ground, damage, people), paged and bounded as it is today; a
  book, shelved. A far ship, which has no log, keeps a short story of her own: her brain's
  state changes with their ticks, her port calls and her cargo's business, what she sighted
  and who hailed her, as the far shape records them (a few lines a day), served by the same
  call, so that the basic history of every ship is there to be read whatever her shape. **A crewed ship
  that demotes keeps her log** as a sealed record keyed to her for the director's reading
  (today her World and her log are dropped); its weight in the save is measured in the
  hand-back.
- Notable lines of the player's ship's log reach the director as today; nothing here
  changes what any station on a ship may read.

### 13. Truths for 7b-iii

- 98. A world with no player's ship runs a day at seed 7 with the business on and a
  director observing; followed ships change the centre; the pace truth holds.
- 99. The player at the captain's station of the Palinure sails her through the station
  trial; the save replays with his acts.
- 99a. The director's chart at seed 7 with the business on shows every ship where the truth
  has her and the player's ship by truth and by account; the player's chart, drawn in the
  same minute, shows none of the truth.
- 99b (provisional). A director focusing the Palinure is woken by her taking the ground
  within her own log's tick; a director reading her log by kind and tick range gets the
  same lines her captain's station would; a demoted ship's log is still read.

## Part 7b-iv: People in places

### 14. Places and movement (`freesail/world/people.py`, `places.py` new; `data/people/*.yaml`; `data/ports/*.yaml`)

A place is an aspect of a person's state, not a simulation of its own (the owner,
2026-10-16: "the goal of locations needn't be super deep simulation of each location, but
just an aspect of each person's status, as well as tying in to the actions they can
perform"). The ship's places as M6 §2 named them (the quarterdeck, the deck, the tops, the
cabin, the wardroom, below, the galley, the hold) are where a person is and may go: `go to
the cabin`, `go below`, `go on deck`, `go ashore` (by the boat, at a port's reach), `come
aboard`; a person's place in his state and the muster; the player's place as a person's
(the player is on the quarterdeck by default, may be in the cabin or ashore, and acts where
he is: the market only ashore or by the boat, the helm only on deck). A port's places
ashore (the quay, the market, the counting house, the tavern, the pilots' office), each with
what can be done there and who is found there (§8's people and the port's own).

### 15. What is heard where: dropped

Locational knowledge (a station's log carrying only what its person could hear from where
he is) is dropped as an overcomplication for now (the owner, 2026-10-16). Every station
reads the log as it does today. One small thing stays from the owner's note 15: a word
said between people and heard by another counts as "a word on deck" for the stand-bys.

**As built (package 52; `harness.Harness._heard_between`; `tests/test_director.py`).** A
stand-by until "a word on deck" ends, as before, at a `say` (`agent.spoke`), and now also
at a word said between people that the station heard: a word told (`agent.told`), a
question (`agent.asked`), an answer (`agent.said`) or a person's words (`person.spoke`),
said by another and not to the station itself (whose own word wakes it as a word), within
earshot of where the station is (the speaker's place by `place_of`, the captain's for the
player at the prompt; `places.earshot`) or named among its hearers. The captain's word to
the master on the quarterdeck wakes the officer standing by there; the same word from the
cabin does not. The standing orders' event of the same words is unchanged (it reads the
log's kind alone), and nothing is added to any line's data, so no pin moves.

### 16. Books drafted (`freesail/agents/tools.py`; `data/papers/`)

`draft a book "night orders": ...` writes a standing-orders sheet, a note for the ship's
papers or a manifest to buy and sell several goods at once, as a book in the library with
the person's mark, the record for the immersion and the use functional (the sheet becomes
the standing orders when posted, the manifest the trade when given to the boat). The papers
kept in a place aboard, read only where they are, is dropped as an overcomplication for now
(the owner, 2026-10-16): the library is read from anywhere, as today.

### 17. The equal reach (`tools.py`; `stations.py`)

Every stationed person has the same basic reach: tell and ask any other person aboard or
within hail, go where his duty allows, read what is where he is, journal, stand by; the
domain orders are the station's authority as now. Several stations of one kind on a ship
(45c's groundwork): the frigate's lieutenants as officers under the first, each with his
place and watch.

### 18. Truths for 7b-iv

- 100. A person who goes below is below in the muster and the state; an order of the
  deck's from him is refused in words until `go on deck` brings him back.
- 101. The player ashore buys at the market in person; aboard, by the boat.
- 102. A drafted manifest given to the boat trades its goods in one errand; a drafted
  night-orders sheet posted is the standing orders.

## Part 7b-v: Needs

### 19. Provisions and water (`freesail/crew/`, `freesail/world/stores.py` or where the stores live; `data/ships/*.yaml`)

The crew eat and drink on the schedule as they rest (M3's watches): the ship's provisions
and water fall by the ration a day (the period's: a pound of biscuit, a pound of salt meat
or its day's kind, a gallon of beer or a quart of water, from the Regulations; the figures
in the ship files), the purser's reading says what remains and for how long, the market
sells them, short allowance is an order with its effect on the hands and their temper,
water found foul is a thing the director may do aboard (§3).

### 20. Hunger, thirst and fatigue (`freesail/world/people.py`)

Named people, the player among them, have the three needs in three to five steps each,
rising with the ship's time, eased by eating and drinking (at a place with food: the cabin,
the wardroom, below, the shore; from the stores) and by sleeping below; notable then urgent
lines to the person stationed only ("you are feeling a bit drowsy", "you are quite thirsty",
"you are absolutely starving"); once a day to eat and drink, a sleep every day or two; by
hand at a filled station to begin with (the owner, 2026-10-15), automatic where nobody is
seated and for the crew; `stand by, asleep below until called` as a stand-by of its own
(the master's suggestion); never busywork (the master's warning). The ends (death by hunger
or thirst, collapse by fatigue, the surgeon) are M7's with health; this milestone stops at
the last step's urgent line and a person who falls asleep where he is.

### 21. Truths for 7b-v

- 103. The frigate's provisions fall by the ration for her complement; the purser's
  reading says the days remaining; short allowance halves it.
- 104. A player who neither eats nor sleeps for two days reads the urgent lines in order
  and is asleep on the third; eating from the stores and a night below reset them; an
  unseated person's needs never show.

---

## Part 7b-vi: Fishing, and the glass on a near ship

### 21a. Fishing for the player, and the fisherman's catch (`freesail/evolutions/`, `freesail/world/business.py`, `ports.py`, `data/fishing/*.yaml` new; the smack's and the lugger's files)

Fishing exists in m6c as a far-detail behaviour only (the `fish` intent and the fisherman's
doctrine, no catch). The owner, 2026-10-17: a player who wants to fish at the level the game
can reasonably simulate should be able to; not a fishing simulation, but researched
grounds, real catches to market, reasonable period evolutions, and the well's spoilage. So:
the fishing grounds of each region as features with their season, their fish and their
yield (the pilchard fishery of Cornwall by the seine and the drift net, the mackerel and
the herring, the Channel's trawl grounds, the Biscay sardine, from the period's and the
fisheries' sources, verified or marked); the evolutions of the gear (the nets shot and
hauled, the lines, the trawl towed under easy sail, the seine with the boats), with the
hands at them and their hours; the catch into the hold or the well by the ground, the
season, the hours and the weather, the well keeping fish alive for so long and the hold's
salt or none (the spoilage); sold at a port that buys fish at its price. The far-detail
fisherman given the same catch and the same spoilage, so a fishing smack of the business
and the player's are one thing at two details; **and the crewed promotion includes the
fishermen** (the owner, 2026-10-17): a fishing vessel near the player is promoted like any
other and fishes at full detail by the same evolutions under her rules-based captain, so
that the glass on her shows the work truly and the promotion's rule has no exception to
confuse (43b's "never crewed" is lifted; the cap's order unchanged). The smack and the lugger
carry the gear their files say.

### 21b. The glass on a near ship (`freesail/world/lookout.py`, `ships.py`, `crews.py`)

What the glass shows of a near ship beyond her rig and her colours: her manoeuvre and her
work in hand, by tiers of distance in daylight and clear weather, the lead's reading for
the owner's word: **within two miles**, what any seaman reads at a look (under way or at
anchor, which tack, hove to, tacking or wearing, running, her sail set or shortening);
**within eight cables**, the work on deck and aloft (reefing, making or taking in sail, a
boat hoisting out or in, the hands at the nets or the lines, the anchor coming up);
**within four cables**, the evolution's own words as the log would say them of the player's
ship ("the hands are hauling the seine", "she is hove to on the starboard tack, main
topsail aback"). A crewed ship gives the true evolution's name; a far-detail vessel the
words her plan's leg and her sail state give; at night and in thick weather only what the
visibility allows. Asked through `the glass on <ship>` or given by the lookout when a ship
is made out and when her work changes.

### 21c. Truths for 7b-vi

- 105. The smack on a pilchard ground in season, the seine shot and hauled, fills her well
  by the ground's yield; the fish sold at Falmouth at the market's price; a well kept too
  long spoils its catch.
- 106. The business's fisherman on the same ground brings home the same catch at far
  detail.
- 107. The glass on the Palinure hove to at a mile says she is hove to and on which tack;
  at four cables the main topsail aback; at night, only her light if any.

## Part 7b-vii: The launcher, the scenario maker and the settings

### 21d. The harbour: a launcher in the browser (`freesail/ui/harbour.py` new, served by `ui/server.py`; `client/harbour.html`, `harbour.js` new; `freesail/__main__.py`; `freesail/settings.py` new)

The owner, 2026-10-17: the terminals, the flags, the desktop client's configuration and the
scenarios made by hand in a file have become tedious, and any long use or a presentation
wants a launcher, a scenario maker and settings. The lead's reading, for the owner's word:
the launcher is a page of the game's own server, not a program apart, so that it runs the
same on Windows and elsewhere and is tested here headless with the browser the tests
already drive. `py -m freesail` (a `__main__`) starts the server and opens **the harbour**:
a page that lists the scenarios (the game's and the player's own), the ships, the seats and
the doors; starts a game with the choices made (the flags of the console and the server
become the page's controls: the seed, the seat, the crewed budget, the compression, the
business, a director's brief); shows which doors are up and which stations are held; and
holds the **settings** (`settings.py`, a file in the player's own place outside the
repository, `%APPDATA%\FreeSail\settings.yaml` on Windows and the XDG place elsewhere):
the key in the credential store as 42 left it, the model names the player uses for each
door (outside the repository, so a model's name may live there), the local runner's
endpoint, the default seat and compression, where the saves go. The **doors** from the
harbour: a button that writes the desktop client's MCP entry into its configuration file
(the path by platform, the player confirming, the entry shown first), the API door and the
local runner started as the server's subprocesses with their flags from the settings and
their output in a pane, each stoppable. The console stays as it is for those who want it.

### 21e. The scenario maker (`client/harbour.js`; `freesail/world/scenarios.py` `write_scenario`)

A form on the harbour that writes a scenario file from choices, in the file's own form so
that a hand may still edit it: the ship, the start (a port's road or a position pricked on
the chart), the date and hour, the weather (a preset of the climatology's, or a scripted day
from the forms the primer gives), the other ships with their intents, the business on or
off, the crewed budget, the standing orders (a starter book, or a drafted one), the stations
and who holds them, a director's brief from the starters or the player's own; saved under
the player's scenarios place and listed by the harbour; loaded back into the form for
editing. The scenario is proved by loading it as the console would.

### 21f. Truths for 7b-vii

- 108. `py -m freesail` opens the harbour, a game is started from it with a seat and a
  director's brief, and the doors' states are shown true.
- 109. A scenario written by the maker loads in the console and the server as a hand-made
  one does, and reads back into the form unchanged.
- 110. The settings file holds no key; the credential store does; a model's name in it never
  enters the repository, a save or a log.

## Part 7b-viii: A ship bought (the owner's design goal of 2026-10-17)

### 21g. The goal, and the lead's reading

The player builds a purse trading in the cutter and moors in a large, busy port. The
director notices the purse and the port. The player sends the purser ashore to look for a
ship to buy; the director sees it, and by its doing the purser finds a schooner for sale
and says so. The player sells the cutter, moves her people and hands out, buys the
schooner and takes her up as his ship, the same people and hands aboard her.

**On the shape of 50 and 52** the director can set the scene and do none of the sale: it
reads the boat's going in the log and the port in the truth (the player's purse and cargo
are added to the truth's snapshot: small, 50 or 51); it may speak as the purser when the
boat returns (§9; he is a person nobody holds), make a broker from words (§8), put a
schooner at the port (§3) and send a merchant's message; but no ship has an owner or a
price, the boat brings back prices and letters only, nothing credits the purse for a hull
or moves hands between ships, and the player's ship is the World's one ship. The purser is
a role of the muster, not a station a model holds.

**The bridge is four general things, no "buy a ship" feature among them:**

1. **A ship is a World with a vessel; the player's ship is the one held** (§11, §12,
   package 51): taking up the schooner is her promotion to crewed from her ship file, as
   promotion builds a World today, the player seated as her captain, the cutter a vessel
   in the world thereafter; the replay keys acts by ship.
2. **People are of the world, not of the ship** (§14, package 53): a person's place may be
   aboard a named ship or ashore at a port; the company moves by each going ashore and
   coming aboard her, the hands as a count by one order (`transfer the people and the
   hands to the "Fly"`); the journals keyed to the person travel.
3. **Ownership and price as facts the port's business knows** (package 60, new): a vessel
   at a port may be for sale at an asking price; busy ports generate listings by their
   size (`data/business.yaml`); the director places one by a tail on the ship order
   (`ship: a topsail schooner "Fly" of britain at Falmouth, for sale at £900`), doubted
   as any order; `buy the ship "Fly"` and `sell the ship` join the market orders beside the
   goods, the yard valuing a hull by tonnage and condition, the purse by the same channel.
4. **An errand ashore** (§14, §17; package 60): `send <person> ashore to <errand>`, answered
   from the port's facts first and by the director second (§9), reported when the boat
   returns. A model at the purser's station is optional later, through stations as data.

With these the director's part is to put facts in the world (the listing, the broker, the
purser's words); the sale, the transfer and the taking-up are the player's ordinary port
orders, and neither side needs a script. The scenario is a gate 7b item.

### 21h. Truths for 7b-viii

- 99c. The player sells the cutter at Falmouth, buys a listed schooner, transfers the people
  and the hands by one order, and sails her out; the save replays across the two ships with
  the journals of the people intact.
- 99d. A director's listing by the ship order is found by the purser's errand and reported
  in the purser's words when the boat returns; the play log never shows the order.

## Part 7b-ix: The land-avoiding route (provisional; the owner, 2026-10-17)

### 21i. The route over the chart's own data (`freesail/world/captains.py` `Planner`; `freesail/world/chart.py`; `freesail/world/brains.py`; `orders/`)

Brought into M7b from the carried items on the owner's word ("pretty important and not
combat-centric"); booked provisionally, to be planned in full at its briefing. **Today**
the planner (`Planner.legs_for`) joins the period's common tracks where the chart has them
and otherwise lays the straight line, giving a headland in the way an offing (`OFFING_NM`
3, `DANGER_BERTH_NM` 1, `PLANNER_ROUNDS` 6) and leaving the rest to `via` marks given by
hand; the known failures are the legs laid across the land (Machico, the Manacles, Keller;
a next leg after a land berth laid across Keller; the owner's runs of gate 6c), the
pilot's joining leg found clear only within the rounds, and the tracks into Roscoff and
St Mary's and the reach into Brest (package 58's notes).

**The intent:** a course shaped for a place, by the player or by any captain the game
sails, is laid clear of the land and the charted dangers over the chart's own data, from
the account and never the truth, with the offing and the berth as the captain's book has
them; the legs are said in the log as the captain's plan ("by Ushant, then Finisterre")
and `via` marks still bind where given. **The lead's reading of a way:** a graph over the
coast's outward corners pushed out by the offing and the dangers pushed out by the berth,
searched for the shortest clear path, cached per chart and refreshed when the offing
changes; cheap enough for a far ship's brain at promotion and under the pace budget
(`tools/pace.py` measures it); the pilot's joining leg and the rules captain's offing
rule (58) drawn from the same path; the lay line (the open item of 43b) considered beside
it, since a route that cannot be laid on the wind is laid in boards. The deep-sea tiles'
rule and the held gauges stay where they are. Builder Fable (geometry and design heavy);
sequenced at briefing beside 51 and before the half of 58 that lays tracks, so that 58
measures against it rather than around it.

**The owner's framing (2026-10-17), which governs the briefing:** models should for the
most part not need an automatic route's hand-holding; the route is mostly for the
rules-based captains, and for a model that misreads or ignores the land-crossing warning
or does not grasp the situation. So **a simple solution may be acceptable, nothing
over-designed**; the design starts from the scenarios where the rules-based captains want
it and from where a route would plainly fail or be counter-productive (a route laid round
a headland the captain meant to close; a board the route cannot know; a chart whose data
is thin), and not from the general problem. **Before it is briefed, more testing of the
captains' present behaviour and its edge cases, by the owner in play**; the briefing
draws on those notes, and the lead's reading above is one way, not the plan.

### 21j. Truths for 7b-ix (provisional)

- 99e. The frigate shaped for Lisbon from Falmouth with no `via` clears Ushant and
  Finisterre by the offing; the brig shaped for Funchal clears Machico; the smack shaped for
  Falmouth from the Lizard clears the Manacles; each on the whole chart, run until past.

## 22. Consent (one revision for the milestone)

The consent brief is revised once more by a named package at the milestone's end, the
re-asks the owner's: the director's station as a thing a model may be seated at (above the
game, the truth seen, the world shaped through plausible causes on a budget, the log read
afterwards), the director's voice (a model speaking as the unseated), the observed world,
and the needs a model's person may have.

## 23. Gate 7b (outline)

One gate, the owner's runs on the playtest form: a directed quiet passage on a local model
(the solo mode the owner looks to) and on a hosted model; the director's log read after;
an observed world for a day with the business on; the player ashore at Falmouth and in the
cabin (his place and what he can do there); a day's fishing in the smack and the catch sold;
the glass on a near ship; a game started from the harbour with a scenario the maker wrote; a drafted manifest's trade; a week's needs; the regatta's course with a director
seated above it. The lead's first play is at the director's station, as decision 39 held.

## 24. Packages (outline; the allocation)

In waves, written for the owner's approval in turn, each launched on his word:

- **50 (Fable): the director proper** (§2 to §7): the station, the channel's doubt and the
  brief's limits, the budget, the hidden log and its reveal, the replay view. **Brought
  forward to the close of M6 by decision 50**, with 52 after it; design-heavy throughout.
- **53 (Opus): people in places** (§14, §16, §17) beside 50: movement and places, the
  books drafted, the papers in their place, the equal reach and several of a kind; the
  journal keyed to the person is in. No dependence on 50.
- **54 (Opus): needs** (§19, §20) beside 50 and 53: the rations, the three needs, the
  sleep below. Data and rules on the people, no dependence on the director.
- **51 (Fable): the observed world** (§11, §12, §12a, §12b provisional) after 50: the followed ship in place of the
  given one across the World, the player on another ship, the replay of a station there,
  and the director's chart (the owner's word of 2026-10-17). Cross-cutting and design-heavy.
- **52 (Opus): the director's voice** (§8, §9) after 50, brought forward with it: people
  from words, `say as`, the asked unseated person answered by the director; the word heard
  counting as a word on deck (§15); and a station below the captain's told the truth of who
  commands (42b's leftover).
- **56 (Opus): fishing, and the glass on a near ship** (§21a, §21b), beside 51 and 52: the
  grounds researched, the gear's evolutions, the catch and the well, the fisherman's parity,
  the glass's tiers.
- **57 (Opus): the frigate's staysails** beside 53 and 54: her complement between the masts
  from Steel's list (the main, middle, main topgallant, mizzen, mizzen topmast and mizzen
  topgallant staysails) through the generator with Steel's dimensions and canvas numbers,
  the shapes of the period (the lower and middle staysails four-sided, the topgallants
  triangular, each with Steel's page beside it), the orders and the heavy-weather book
  reading them, the ship file regenerated, the pins it moves re-measured once; the brig's
  set checked against Steel's for a brig (the owner's finding at gate 6c, 2026-10-17).
  **And the chasse-marée's rig** (the owner's notes on the Éclair's first cruise, 2026-10-17,
  `docs/playtests/2026-10-17-eclair-first-cruise/owner-notes.md`): lug topsails in place of
  the square ones, trimmed with the lugs as fore-and-aft sails; the lugs drawn slung a third
  from the fore end and set to leeward of the mast on either tack; the viewer's draw order
  by the aspect (the sail before the mast hides it from ahead, the mast the sail from
  astern) and the yards' brace shown in the picture.

  **As built (package 57).** The staysails between the masts are Steel's list for a ship
  (1794 vol. I, Sail-making): the main, main topmast, middle and main topgallant staysails
  between the fore and the main, the mizzen, mizzen topmast and mizzen topgallant staysails
  between the main and the mizzen, each cut in `tools/gen_ships.py` (`between_the_masts`,
  `stay_sail_cut`) as Steel cuts it, square on the foot with the head on its stay, the
  leech's depth and the foot's cloths by his rule where he gives one and the bunt as the
  stay then leaves it, his page and the rule in the comment beside each; the stays they set
  on are new where the file had none (the main staysail stay, the middle staysail stay, the
  main topgallant stay, the mizzen staysail stay, the mizzen topmast and topgallant stays).
  The shapes are Steel's own and not the brief's reading: his main staysail is triangular
  and every other staysail between the masts four-sided, the topgallant staysails among
  them (his canvas rule groups them with the middle staysail; the tuning notes say so). A
  sail's cut is in its file (`corners_m`, a new key) and the viewer draws it from there. The
  brig's set is Steel's for a brig, the middle staysail added and the canvas his numbers.
  Lying to (Steel 1794 vol. II, 'Lying-to under the main staysail'): `lie a-try` sets the
  file's `lying-to staysails` (the main staysail) short of the storm line, and over it the
  storm staysails stand for it as package 37p left them, `shorten sail` and `set the storm
  staysails` taking the main staysail in. **A sail set flying** is a handling class carried
  as a key beside the sail's cut (`flying: true`), since its curve is its cut's (a royal is
  a square sail, a lug topsail a lug): it is swayed up from the deck with its yard and sent
  down whole (`set_flying`, `take_in_flying`), never reefed, a furled one *sent down* in the
  log's and the readings' words with its yard on deck; the frigate's and the brig's royals
  (Steel p. 214, ROYALS "Are set flying") and the lugger's topsails are in it. **The
  chasse-marée's topsails** are lugs on lug yards on the topmasts, slung a third from the
  fore end, their tacks at the lower mast heads and their clews sheeted to the lower lugs'
  peaks (`sheeted_to`, a new key): the sheet reading of a lug topsail is its lower lug's
  (`evolutions/trim.py`), so it lies on the same side and angle, goes round with it at the
  dip and flogs while it is lowered; Forfait's braces and lifts are on its yard, none braced
  by an order. **The viewer** draws a lug from its cut on its side of the mast, swung about
  its slings by the sheet's angle, two thirds of it abaft and to leeward, nearly square and
  offset when running, lowered on deck; a square yard is slung before its mast, every sail
  and yard sorted against its own mast where it stands (the rake corrected), a lug cut at
  its mast; a flying sail sent down is not drawn and its yard lies on deck; the brace was
  drawn before and is now said in the yard's title too. Truths 7b-111 and 7b-112 (numbered
  after the spec's 110). A staysail between the masts stowed on its stay has half its
  class's furled windage (judgement, set between truths 8 and 10), and its sheet is sized
  to its cloth. The captain's gale trial (`trial-station-gale`) falls otherwise from its
  first course under the new rig and takes the ground among the Molène islands after two
  failed wears: an expected failure, for package 58. The tuning notes, "Package 57", have
  the figures and the pins.
- **58 (Opus): the captain's sea sense, third pass**, from the owner's runs of gate 6c
  (`docs/dev/M6-WorkPackages.md`, "The notes of 2026-10-17, read"): the offing by the
  account not its doubt, the guard against land ahead within the visibility, the book
  taking a bearing when the doubt is wide, the headsail shifted, the trim's cadence, the
  merchant book's track into Bertheaume's road, all sail in a chase, the station's regain
  against the wearing order, the lay line and the sea-route mark, Roscoff's and St Mary's
  tracks. Beside 53 and 54.
- **59 (Opus): the harbour, the scenario maker and the settings** (§21d to §21f), beside
  53 and 54: a page of the game's own server, so built and tested here headless and proved
  by the owner on Windows; the Windows-only pieces (the desktop client's configuration path,
  the settings' place, a shortcut) small and tested by path, with a local session on the
  owner's machine kept as the fallback if the browser's opening or the shortcut want it.
- **60 (Opus): a ship bought** (§21g) after 51 and 53: listings by the port's business and
  by the director's ship order, the hull's valuation, the ship bought and sold through the
  market orders, the transfer of the people and the hands, the errand ashore; the goal's
  scenario for the gate.
- **61 (Fable, provisional): the land-avoiding route** (§21i) beside 51 and before 58's
  tracks: the route over the chart's own data for every captain and the player, the legs
  said as the plan, the pilot's joining leg from the same path; planned in full at briefing.
- **55 (Opus): the solo director and the gate's scenarios** after 51, 52, 56, 57, 58, 59, 60 and 61: the starter
  briefs, the local-model director's run, the directed regatta course, the consent
  revision drafted for the owner (§22), the gate document.

Gate 7b after 55, carrying gate 6c's untested items (decision 50).

## 25. What this milestone does not do

Powder, damage and the prize (M7); the ends of the needs and the surgeon (M7's health); the
gybe as an evolution and the sails at fine control (M7); signals and the hail between ships
(M7); two directors competing; the supply-and-demand
loop; the orders system's review (deferred to a cold review).

## 26. Open items carried in

From M6: the Goulet on a flood (43b), Torbay's stream (43b), the held gauges' blend, the
deep-sea tiles' rule, the land-avoiding route (brought in as 61, §21i), the test battery's cost (eaten by the owner's
word), the orders review (deferred).
