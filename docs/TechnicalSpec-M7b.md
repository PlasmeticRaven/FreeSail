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

### 2a. The director's seat made real (package 67; the owner, 2026-10-19; built 2026-10-23)

**As it stands.** `seat: <the model's exact name> as captain of <ship> for <n> samples|hours`
(43's form) checks the consent record, the owner's grant (the scenario's `director:` block:
`models`, `seats` at once, `seats_in_voyage`) and the budget, and writes a seat on the
World; the budget is enforced (`crews.enforce_budgets` stands the holder down when it is
spent). But no door is started by it, and the desk admits a door for another ship's
captain by the ordinary station rules without reading the seat: the seat is a record of
intent and a budget, and its result's words ("a door that comes for her under that name is
admitted") overstate it. The owner's ruling: **the director seats through the API door,
bounded by the grant's budget.**

**The design, for the brief:**

- **The desk reads the seat.** A door for a model and a ship with a held seat is admitted
  under its budget; a door without one is admitted as now; a seat held for a model that
  never comes is stood down with the voyage's end or by `unseat:`.
- **The director's door.** On `seat:`, the game starts the API door itself as a subprocess
  of the server, as the harbour of package 59 starts one from its page (`ui/harbour.py`'s
  `Door` and `door_argv`: the module's own flags, the key from the credential store, the
  model's name and dialect from the settings or the seat's words, the station the
  captain's, `--ship` the seated ship), the pane shown in the harbour's doors tab beside
  the owner's own, stopped by `unseat:` or the spent budget; where the server has no
  harbour (the console) the seat stays a record and says so. The grant's models are the
  models the settings know how to call; a model the settings cannot call is refused in
  words at the seat.
- **What a seat costs, said.** The brief tells the director that a seat runs a model on the
  owner's key for its budget, in samples or hours, and that the grant is the owner's
  spending; the harness counts the seat's samples as it counts the director's.
- **Other stations.** The form widens to `seat: <model> as <station> of <ship>` for the
  stations a ship has (an officer of the watch, a lookout on the player's own ship under
  the owner's grant), the player's own ship included where the grant allows it; the
  captain stays the default.
- **The harbour.** The grant is not exposed anywhere a player would find it: it lives in
  the scenario's `director:` block, which the maker does not show, and the per-seat budget
  only in the seat order's words. Package 64 (the harbour's second pass) shows the grant on
  the game tab and in the maker's brief section, with the models the settings can call,
  and the doors tab shows the director's doors as it shows the owner's.

- **An out-of-character channel (the owner, 2026-10-23).** A `director:` word at the
  player's prompt goes to the director's log only, never the play log, and comes to the
  director in his next sample as the player's word apart from the game; the director's
  answer to it goes back the same way, apart from the play log, and the play log says
  nothing. The brief's rule stands beside it: plans and the truth stay in the journal, and
  a question to the player is phrased without world detail.

Package 67, Opus, after 68; the brief at the lead's hand on the owner's word.

**As built (package 68; the cold review of 2026-10-22, R-35).** The truth says the player's
ship's own state (`readings._own_state_truth`: aground, where, on what ground and since when,
the tide rising or falling; at anchor, riding or dragging; under way), which a director once
read wrong from her speed alone; a ship sailing by her captain's intent shows the intent and
no goal (every business ship was made with the placeholder "bound for Falmouth", and the
truth showed it); and `truth(within=<miles>)` keeps the ships within so many miles of the
player's and their people, the rest counted ("the ships within 20 miles of the Amazon; 3
more beyond, not shown"), a cheaper read. The director is hidden from every station as
§6 has it: with `--ease-on-station` its samples ease nothing and write no driver's line
(R-20; `ui/server.Driver._samples_now`).

**As built (package 67, 2026-10-23; `freesail/world/seats.py` new, `orders._seat` and
`_unseat` its doors; `agents/remote.py`, `ui/harbour.py`, `ui/server.py`, `agents/api.py`,
`agents/director.py`, `settings.py`; `tests/test_director.py`, `test_agent_api.py`,
`test_harbour.py`; truths 7b-130 to 7b-132).**

- **The form widened** (`seats.hold`): `seat: <model> as <station> [of <ship>] for <n>
  samples|hours[, within <time>]`, for the captain, an officer of the watch, the master, the
  lookout and a passenger of another ship or of the player's own (no `of`, or her name),
  the player's own allowed unless the grant says `seats_on_the_players_ship: false`; the
  rule of reach (`orders.held_stations`) refuses a station the player or a model holds,
  the captain while the player is at the prompt among them. A person by his name is
  seated at the station he is bound to, and one nobody holds **as his voice**, the
  honest smaller version of the brief's: a station of the passenger's kind bound to him
  under his name (`VOICE_KIND`, the binding quiet, the world order being the input, and
  its lines for the record), his brief (`VOICE_BRIEF`: no order of any ship's, `say`,
  `ask`, `tell`, the journal, the readings, the stand-by), heard where he stands, and the
  director's `say as` for him refused by the rule of reach while a model holds him. A
  person aboard another ship is refused in words (no other ship has a World of people to
  bind him in; package 68's refusal of one made there). The seats' keys are the ship's id
  for her captain (43's, so that a save from before reads), `<id>/<station>`, `own/
  <station>` and `voice/<station>`; `unseat:` takes the same words, or a ship's name for
  every seat on her as before.
- **The desk reads the seat** (`Desk.station`, `seats.match`, `seats.admit`): a door for
  the seat's model at its station is admitted under the seat's budget, its samples or
  hours counted from the admission (an input, `seat_admitted`, replayed), its door note and
  its first answer saying so; any other door is admitted as before. Kept once a minute by
  the World whatever sail is about (`crews.enforce_budgets`, now `seats.enforce`): spent,
  the station is stood down with the reason; a seat whose station is released after its
  admission ends with it; one whose door never came lapses after its `within`; the
  director's log says each (`director.seat`). A seat held when the voyage ends ends with
  the game.
- **The director's door** (`Harbour.tend_seats`, called by the driver's clock every tenth
  of a second): for each seat held the harbour starts the API door with the module's own
  command line (`door_argv`'s `seat_model`: the seat's model, its dialect from the settings,
  `--station`, `--ship`, `--budget-tokens` where the settings name one), the key read by the
  door's own process, the pane in the doors tab marked the director's seat's
  (`Door.by`); a seat gone before its door was admitted has its door stopped, one stood
  down lets its door end of itself (*its station was released*). **The models the
  settings can call** (`settings.callable_models`: the API door's model and
  `doors.api.models`, each a name or `{name, dialect}`): a `seat:` for another is refused
  before the World (`director.uncallable_seat`, at the director's door and at the
  owner's `world:` in the browser), in words naming the API door's model to the director
  alone; checked before the World so that no log, save or replay depends on the settings
  and the settings' model's name reaches no log (truth 7b-110). Without a harbour (the
  console) the seat is a record; its result says the door to start by hand, the same
  words either way so that a replay writes the same line.
- **The cost** (R-34): the brief's paragraph on a seat's cost and the channel
  (`director.SEAT_AND_CHANNEL_BRIEF`, after the fixed part and before the player's brief,
  apart from the forms reference); `seat:`'s result repeats the budget and the cost's shape;
  the director's budget line names the seats held and their spending
  (`seats.spending_words` in `director.budget_words`). A door under a seat has its handover
  fold counted from **two fifths of its model's context** (`remote.SEAT_BUDGET_SHARE`; the
  owner's review), or the figure the door asks (`--budget-tokens`, which any API door takes;
  the settings' `doors.api.seat_budget_tokens` for a seat's door, in tokens or a share); a
  reply cut off at its limit twice folds the conversation (`remote.CUT_FOLD_NOTE`); the API
  door says the conversation's size at each fold; and a station taken again says which of
  the captain's grants lapsed with its leaving (`Harness._lapsed`).
- **The channel** (R-21, R-24): `director: <words>` at the prompt (`console.director_word`;
  `director: brief`, `budget` and the bare prefix the brief's as before) is
  `director.player_word`: an input (`player_word`, replayed), the director's log
  (`director.player`), the director's next sample as *The player, apart from the game:
  ...* (a word, which wakes a stand-by), and the drivers' listeners; the director's answer
  is `answer the player: <words>` (`director.direct` before any world order, or a reply's
  text or an `answer` opening with it, `director.thought`), no act counted, to the
  director's log (`director.answered`) and the listeners: the console prints it as its own
  line, the browser's server sends it to a small pane (`#channel-panel`; `GET
  /api/director/channel`). The play log carries neither. The director's own words out of
  turn are answered as its log's, never "in the log under your mark", at the desk and the
  MCP bridge.
- **Taken another way**: the person aboard another ship (refused, above); the settings'
  "account" read as the dialect, the credential store not read by the game to check a key
  is there (the door says so in its pane when it has none: the key is read by the door's
  own process alone); the fold after a double cut-off made by the desk on the door's
  words (`Harness._fold_handover` with a note of its own) rather than by the harness.
- **Found on the way and mended**: a seat held under consent records kept elsewhere
  (`--consent-records`) was refused in the replay, the records not being the replay's, and
  the log diverged; a replay now reads a seat's consent from the world orders' outcomes in
  play (`World.replayed_orders`, set by `replay.replay`).

### 3. The world orders (`freesail/world/orders.py`)

The channel as M5 and M6 built it, with the orders the director needs added and the
guardrail enforced on every one:

- **The weather:** `weather:` as it stands (a low with fronts, a squall line, the glass),
  with a bound: a change the systems could make from where they are (a front not more than
  so many hours sooner or later than the climatology allows, a wind not stronger than the
  season's record for the box); refused in words beyond it.
- **Ships:** `ship:` as it stands, with 43's `intent:`; `ship "X": intent ...` to change a
  mind; a ship put on the sea only where she could be (not inside the player's horizon
  unless the visibility hides her; not aground). **A free intent** (the owner's of
  2026-10-26 and 27, folded in by package 86; PROVISIONAL in form, for 82 and 84 to
  rework): words no intent's form reads are taken, with the warning and why, as the goal a
  model at her captain's station is told (the scenario's `free_intent:` takes any words so);
  her rules-based captain does not sail by it but lies her to where she is (the far body by
  its plan's `lie_to`, the crewed captain by one `heave to` on his passage), keeping her
  service's role and doctrine for the weather and strangers. A misspelt port is so taken
  too; whether an unreadable intent should instead be refused unless a word asks for the
  free form is the owner's open question.
- **People:** `person:` as M6 §11 outlined it (`person: "Mr Fox" comes aboard as master`),
  made real here (§8).
- **Aboard:** `aboard: the fore topmast is found sprung`, `aboard: a cask found stove`, the
  carpenter's and the purser's reports, from a table of things that can be found aboard
  (`data/director/aboard.yaml`), each with what it does in the part graph or the stores.
  **As built, widened by the owner's hotfix of 20 October 2026** (reviewed and folded in on
  the 23rd): twenty-four things, each with a plausibility rule and its doubt, a `harm`
  level under the brief's "nobody dies", a report in a period voice and an effect on a
  modelled quantity where one exists ("nothing modelled yet" said where none does): spars
  sprung and rotten, sails and lines chafed, canvas mildewed, cordage spoiled, casks stove
  and leaking, the water foul (cleared by watering) and brackish, the bread spoiled, the
  meat rotten, rats and weevils, the cargo wet, the chronometer stopped, the glass broken,
  the compass sticking, a seam working, the bilge foul; and two forms of the hull's
  repair, `aboard: the leak stopped` and `aboard: the well pumped out`, labelled stopgaps
  that set two quantities at once with no time or hands, until milestone 7's taking on
  water brings the pumps and the carpenter's work (the well is sounded and read since the
  same hotfix: `sound the well`, `the well`).
- **The news and the letters:** `news:` (a war declared, a peace made, a price heard) and
  `letter:` as they stand.
- **The mark:** 45c's `mark:` point of interest.
- **The seat:** 43's `seat:` and `unseat:` by the owner's grant and budget.
- **The director's hand** (the owner's proposal of 2026-10-18; package 62): `ship "<name>":
  order <an order of the ship's own grammar>` passes the order to her captain's station as
  his own: her log says "by the captain: ...", the director's log keeps it as the director's
  act with its doubt and reason, at far detail through the far orders that stations on
  other ships use (`crews.far_order`, `submit_far`), when she is crewed through her World
  as any captain's order; refused in words where a model or a player holds her captain
  (the rule of reach: the director writes to him by letter instead). No seating and no
  model: the minute that matters, a hail, a heave-to, a boat lowered, is the director's
  without a second conversation. **The director seated in her** is the same package's
  second item, later: the director takes a ship's captain's station outright, her log and
  readings in its samples beside the truth while it holds her, for the hours that want
  judgement rather than a rule.

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

**As built (package 62, 2026-10-18; `freesail/world/crews.py` `hand`; `orders.py`;
`tests/test_world_orders.py`, `test_director.py`, truth 7b-113).** The hand is the `ship`
channel's: `ship "<name>": order <words>` (`orders._hand`, `is_hand`) hands the words to
`crews.hand`. **Crewed**, they go to her World's `submit` as her captain's order under his
rules' actor (`captains.actor_for` his state: not journaled in her World, the director's act
or input being the record), so that her grammar is his domain and nothing more: what she
cannot do is refused in her own words, a reading or a sentence of her deck is no order, a
world order inside the hand is no order of hers. **At far detail**, through the far shape's
orders: `far_order` on the far body (a light stand-in for her World, `_FarBody`, since
`far_order` reads only her vessel and the parent's sea), or `submit_far` where a station keeps
her World in the far shape. **Her log says it as his**: "By the captain: heaving to." in her
World's log, or, for a far body with no World, in her **short story** (`Vessel.story`, the
ground of §12b's "a far ship keeps a short story of her own", saved in her dict only when
there is one); never a line of the player's log, whose lookout sees what she does (the glass
on her heaving to). **Her captain is told it came over his head**: the crewed `Captain`
(`over_his_head`) has his state's book struck as at the player's hand and his judgements held;
the far `FarCaptain` (`over_his_head`) keeps the plan as it stood before the first such order
and does not judge; either holds a glass (`crews.HAND_HOLD_S`, 1,800 s) or until the
director's next order to her, which sets it again, then takes her up again from where she
is (the near captain's first state entered afresh, filling away from a heave-to; the far
plan laid back, its sail order with it; a line in her log); `ship "X": order carry on` gives
her back sooner. The hold crosses the promotion both ways. A far vessel with no captain of
her own (a goal and no intent) obeys and holds by it until the next order. **What the far
shape cannot carry** (a sail by name, a boat lowered) is answered as the game's honest "no
way as said", naming the eleven orders it carries (`crews.FAR_SHAPE_WORDS`), logged
unperformed or, with a reason, attempted; within the promotion's range the answer adds that
the director may ask for her crewed first: `ship "X": crewed` (`crews.ask_crewed`) promotes
her now when the cap has room and she is in no state a ship is not crewed in, and is refused
in words beyond the range or with the cap full, the cap and its order unchanged (the owner's
budget). **The rule of reach** (`orders.reach`, `_hand_reach`; `crews.captain_held_by`):
refused outright, logged `director.refused`, where a model or the player holds her captain's
station ("Hazard's captain (Captain Reynolds) is held by a model: his orders are his holder's
own, and nobody gives one through him; write to him instead ('message: ...')"), and for the
player's own ship whoever holds her. **The doubt** (`_doubt_hand`): an anchor let go deeper
than thirty fathoms by the chart, plain sail made in a wind at her over thirty-four knots,
a chase given by a master of the merchant's, the fisherman's or the packet's doctrine; the
rest of a captain's orders are plausible causes of themselves. The director's log keeps the
act as every act (`director.order`, `.doubted`, `.reentered`, `.unperformed`, `.attempted`,
`.refused`), its kinds' descriptions naming the hand. The station brief names the hand
among the examples with its refusal, and a brief may carry the player's own `examples`
(each starter one order by the hand; the dispatches brief the frigate's four), read to the
director as examples, not a rule. **The director seated in a ship** (the paragraph above) is
not built.

**As built (package 66, 2026-10-19; `crews.hold_of`, `hold_event_came`, `HOLD_EVENTS`;
truth 7b-119).** The hold is named (the dispatches test's finding 4: a glass is three miles
and a half at seven knots, and steering the frigate across eight miles took two orders and
still failed): `ship "X": order <order> for a watch` (`for two glasses`, `for an hour`, `for
a day`) holds her captain that long; `... until <an event>` until one of her own events
comes to her, read from her truth as her far captain perceives it whichever body moves her
(`brains.perceive_vessel`): `a sail within hail` (four cables, `HAIL_REACH_M`), `a sail in
sight`, `a landfall` (the land in sight from her), `hove to`, `at anchor`; an event so named
holds a day at most (`HOLD_UNTIL_MAX_S`, judgement), and one she cannot be held until is
refused in words naming those she can. The default is still the glass; `carry on` still
gives her back sooner; the event is kept beside the tick on both captains
(`Captain.over_head_event`, the far captain's `over_head["event"]`) and crosses the
promotion both ways. The crewed captain looks for it once a minute, the far captain at his
judgement's cadence. The dispatches brief's examples gain `ship "Medusa": order give chase
until a sail within hail`.

**As built (package 68; the cold review of 2026-10-22, R-43, R-41 and 61's simple half).**
**The new ship's form read clause by clause** (`orders.new_ship_spec`), each checked in turn
and the refusal naming the clause at fault ("the description 'a whaler' is no description a
far-detail ship takes", "the nation 'Narnia' ...", "the place '...' ...", "the goal 'bound
for Atlantis': ..."): a description after its adjectives ("a French lugger", "a small
fishing lugger", "a deep laden merchant brig"; `ships.description_key`); any clause of her
colours, shown or not ("British colours", "colours shown", "flying French colours", "no
colours"), never read as her goal; an intent with commas in it, everything after its word;
a port in the `of` slot, her nation the port's. **A place on the land is refused** in words
with the nearest water a ship floats in named ("is on the land by the chart, and no ship is
put there; the nearest water she floats in is N of it, 1 cables off, at 50° 09' N, 5° 04'
W"), whatever reason is given: the land's doubt is the form's refusal now, since no reason
puts a hull ashore. **A ship made in a port's harbour** (within a mile and a half of its
roads or anchorage, `HARBOUR_NM`) goes out by the port's track to sea before her goal's
legs, or her intent's (`departing`, as the world's business ships do). **The form before
the doubt** (`orders.form_error`, in `director.direct`): a malformed order is answered
honestly in words, never "doubted" alone, so that a doubted order is one that can be
performed when entered again. **A reason on the first entry** answers no doubt the director
has not seen (`director._doubt_shown`): the doubt is shown, and the order entered again
with its reason is performed. Not taken: a reason that does not answer the doubt still
overrides it (R-41's second case), the hard half of 61 (a route laid clear of the land),
"whaler" and the forms the directors asked for (R-42).

**As built (package 58a; R-42's reference and dry run, R-39's small part).** The forms are
one table (`director.WORLD_ORDER_FORMS`: each form's words, what it does, and examples a
test performs by dry run on the world it is meant for), the library's grammar topic's fourth
part ("the world orders") and the source of the station brief's and the starter briefs'
examples. `world_order(text, dry_run=true)` answers in the channel's own order (§12's as
built). A system appended in play grows in from nothing at the order's tick (`System.
ramp_from`, `ramp_until`: over `APPEND_RAMP_S`, an hour, at the least, or until its first
point's time), a waypoint appended to a track that had ended runs from where the system
stands at the order's tick, reached an hour on at the soonest (and is doubted for its speed
from there), and **a high is doubted like a low**: above the season's ceiling (the month's
background with its strongest high's anomaly and `HIGH_CEILING_MARGIN_HPA` over), or one
`LOW_DEEP_HPA` strong within `LOW_NEAR_KM` of her out of a glass that has not been rising.
Kept out, as briefed: the summed field's seasonal bound and the climatology's drift onto
Iberia (M7's weather). The scenario's own world orders take the same rules; no recorded
passage appends a system, and its waypoints all extend tracks still running.

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

**As built (package 68; the cold review of 2026-10-22, R-38 and R-61).** **The enemy's
weight** is ranked as the tops rank a sail (`captains.size_rank_of`, the words of
`_SIZE_WORDS`) for the description and for the limit alike: "brig" held none of the
ranking's keys, and a French frigate passed the dispatches', the chase's and the
interesting passage's briefs of no enemy heavier than a brig. A test for each starter's
limit against each class (truth 7b-123). **The brief in play**: `director: budget 60
samples, 10 acts` (either figure alone) gives the brief as it stands with its budget
changed, an input replayed (`director.set_budget`); `director: brief <words>` that name no
starter and no file changes the tone and the name and keeps the limits, the cadence, the
budget and the examples (`director.brief_in_words`; a starter's name or a file is a brief
whole, as before); a new brief whose budget the day's counts are within lifts a hold the
old one made, and the log says so (`director._lift_hold`).

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

**As built (package 66, 2026-10-19; `harness.Harness.line`, `readings.station_line`,
`director_line`; `remote.Desk._own_act`; `harness.Harness._reaches`; truths 7b-117 and
7b-118).** After the dispatches test (findings 9, 17, 18, 19, 22 and 25, and the captain's
debrief):

- **The line.** Every sample of a seated person opens with one line of his own
  (`Sample.you`, first in the sample's data, and printed first under a text door's head):
  who he is, where he is and since when, the deck (his, another's by name, the captain's
  book's or nobody's), and his state in the needs' words ("You: the captain, ashore at
  Falmouth, at the market, since 10:38; the deck yours; on your feet since 10:00."). One
  line, never more; the needs' notices come as §20 has them. Built in one function in
  `readings.py` (`station_line`) from the people's place (`People.effective_place`, the
  port's place ashore), the stations held (where the deck is kept) and the needs
  (`NeedsKeeper.showing`, `hours`); the "since" is the harness's, kept when the person's
  place changes (looked at after every order, once a minute and at the sample, and read
  back from the log's last line that moved him). `how am I` answers with the same line.
  The director's line says the day's budget and whose turn the clock waits on (every
  station with an open sample). The line is the sample's, never the log's: no pin moves.
- **A model's own order ends its stand-by.** A reply sent while the game has the floor that
  acts (any call but the meanwhile reads, a journal note, shelving, or a lone `stand_by`)
  ends the stand-by, or the wait for the turn, at the model's own word, logged as such
  ("The captain ends its stand-by (until a glass) at its own word; it is sampled again."),
  opens the turn and is run in it; recorded as the model's own word (`door_act` "speak",
  by "its own order") and the reply after it, so that a replay opens and runs it at the
  same point. The door's answer says so. Nothing is dropped with "Nothing was run" but
  while the station is paused. The meanwhile reads are unchanged and never end it; the
  director's **truth** (and `read_journal`) join them (`remote.READ_ONLY_TOOLS`); its chart
  was among them already as a picture tool.
- **A wake carries a line.** A stand-by's event, an urgent line and a notable line that
  samples a station by its cadence wake or sample it only when the line reaches it
  (`Harness._reaches`): a word said in a place (`agent.spoke`, a station's `agent.note`
  with where it was said, `person.spoke`, a word told or asked, an answer) when its hearers
  name the station, it was said within its earshot, or to it; the ship's own lines reach
  every station; the director hears everything. The empty wake of 15:44 is the test (truth
  7b-118).
- **Not taken**: the sample's deltas and the repeated history (58), the readings by place
  (65).

**As built (package 68; the cold review of 2026-10-22, R-25, R-27, R-28, R-30, R-61).**
**The MCP door**: the bridge's default wait is fifty seconds (`MCP_WAIT_S`), under the sixty
after which the desktop and Claude Code clients cut a call, and the harbour writes `--wait
50` into every desktop entry (the settings' own figure where given); a door of the same
model that asks for its station within five real minutes of its door holding a call open
for the next turn (`remote.RECONNECT_S`, `Seat.held_at`) is a cut call, not a new chat: it is
seated again as before, and its first result opens with the words that say so and the turn,
the brief not sent again (it stays the `brief` prompt and the `freesail://brief`
resource). "Still waiting" says the ship's time now and the owner's clock ("It is now
Morning watch, 8 bells (04:00), the clock at 60x", `Harness.interim`'s `now` and `clock`).
The officer's brief and the `stand_by` tool's words give the compound stand-by ("tacked, or
ten minutes, or a sail sighted"), and the MCP door's words tell a seated model never to end
its reply in the chat. **A stand-by replaced**: a `stand_by` for another thing, sent while
the model stands by, replaces the stand-by, its result and the log's line say which ("Standing
by until two bells, in place of the stand-by until eight bells"), and the same stand-by asked
again goes on (`remote.Desk._stand_by_out_of_turn`, compared by the stand-by's own reading).
**The director's own lines** wake it not: the lines its own world order writes (a `say as`, a
thing found aboard, a ship put on the sea) are spans of the log its harness passes over
for its policy, its stand-by and its folds (`Harness._own_lines`); every other station meets
them as before.

**As built (package 58a; the cold review of 2026-10-22, R-26, R-31, R-04, R-39, R-42 and
§7's accounts; `harness.Harness._as_told`, `_delta_keys`, `_as_before`; `mcp_server.
still_waiting`, `Bridge._listed`; `agents/tripwires.py`; `readings.ahead_words`; `World.
record`'s `RECURRING_KINDS`; truths 7b-124 to 7b-126).**

- **The deltas.** A sample after the first carries what changed since the model's last
  reply: the log lines since, the readings changed (31c), the sails in one line only when a
  sail's state changed, the sail rows (`SAIL_ROWS`: the strangers, a sail in sight, a
  stranger in sight) compared by each sail and how far she is made out, not by her bearing;
  the lookout's row by who holds the masthead and his last hail, the officer's by all but
  the captain's words to him; the captain's word or question to the station not again in
  the log beside the sample's `word`; the stand-by's notable lines counted (`lines_in`, the
  log below) and not listed twice. A sample of deltas closes with `as_before` ("As before:
  the sails, two sail in sight, the book; the other readings as last told (readings gives
  every row).") for the owner's caution that a model may forget a thing is still so. The
  first sample of a seating and the first after a handover fold are whole; `readings` gives
  everything. The standing orders reach a sample only by the `captain` row, which the deltas
  carry when the book changes. *Taken another way*: a cursor per part was not kept beside the
  log's (the brief's reading); the deltas compare the parts' own keys with the last told,
  which is the same and keeps nothing more in the save.
- **Still waiting**: the MCP bridge lists only the notable lines since its last result of
  the same wait (`still_waiting(..., listed)`), the earlier ones counted. The bridge keeps
  the count, not the game: a door's poll is not an act, and nothing of the replay moves.
- **The cost of thinking**: the station's line and the director's close with "<n> minutes
  of the ship's time since your last reply" (`Harness._replied_tick`, `cost_words`).
- **Tripwires** (`agents/tripwires.py`): `her way settled` (speed within a quarter knot and
  head within a quarter point for two minutes, begun again at every order), `depth under
  <n> fathoms` (the chart at the account, or the lead), `speed under/over <n> knots`, `the
  wind over <n> knots`, `a point of interest within <n> miles` (the chart's places, marks,
  lights and dangers and the world's `mark:`s, new within the miles of the account); each a
  condition watched once a tick as the dialect's are, its wake naming what it found.
- **The notable-noise rules** (`core/world.py`): a line of `RECURRING_KINDS`
  (`evolution.waiting`, `sounding`, `aboard.found`, `well.sounded`) whose words equal the
  last of its kind is routine; light airs fall light under the floor held
  `WIND_LIGHT_HOLD_S` (ten minutes) and settle `WIND_SETTLE_BAND_KN` (two knots) above it,
  within a point, held `WIND_SETTLE_S` (ten minutes); the swing at the turn is said once a
  turn, its cause mended: `TideState.flood` is None where no stream runs (`NO_STREAM`), and
  the riding words there are "head to wind" (§12a's world orders and M5 §16 unchanged
  otherwise).

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

**As built (package 68; R-20).** The director's samples ease nothing under
`--ease-on-station` and write no driver's line, and its own lines, being for the record, ease
nothing; a standing order's refusal names the stations aboard and never the director ("the
director is above the game; a standing order may tell or ask the ...").

**As built (package 67; §2a's channel).** The director's log gains three kinds: `director.seat`
(a seat held, its door admitted, stood down at its spent budget, ended with its station, or
lapsed), `director.player` (the player's word apart from the game, *The player, apart
from the game: ...*) and `director.answered` (the director's answer to him, *To the player,
apart from the game: ...*). Both channel kinds are in `two stories` beside the play log
as every entry is, and neither is a line of the play log, its replay's or a station's
sample but the director's own; the player's word is an input (`player_word`), so that a
replay makes its entry and its notice again. The browser's pane for the channel
(`#channel-panel`) is apart from the director's log's pane: it shows the player's words
and the director's answers as they come, shut until a line comes, and reading it
(`GET /api/director/channel`) is no reveal of the log. A voice's binding and unbinding
(§2a) carry the director's actor and are for the record.

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

**As built (package 68; the cold review of 2026-10-22, R-15).** A person is made aboard
the player's ship or ashore, and words that name another ship ("aboard the Two Brothers",
"on the quarterdeck of Cudlip's Boat", "onto the Lydia's quarterdeck") are refused in words
and nothing is made: three foreign captains had been put on the Sherbourne's quarterdeck
and in her people. The player's own ship by her name ("onto the Amazon's quarterdeck",
"aboard the Amazon, in the gunroom") is aboard, at the place said (`orders._ship_said`); a
place said is honoured and the cabin is the default only where none is. Binding a person to
another crewed ship through her World was not taken: her World is made and folded with her
promotion, and a person kept in it would be lost at the fold. The `say as` refusal that
advised "make him first" says that the people of another ship are not kept.

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

**As built in part by package 84 (step 10; `docs/design/Design-OneWorld.md`, the postscript
"Step 10"):** the followed ship, `world.followed`, with the player's ship the followed by
default; `follow "X"` a driver's line replayed; the World's names, the snapshot, the chart
and the prompt reading the followed hull; the words "no ship followed" stand ready for the
world with no player's ship, which is this package's.

### 12. The player on another ship, and the replay of a station there (`crews.py`; `core/replay.py`)

`--seat captain --ship <id>` for the player (43 left it): the drivers' centre follows the
ship the player is aboard, the player seated under the same contract as a model there; and
a save with a station on another ship replays that station's acts as it replays the
player's (43's checkpoint carries the other ship whole; the acts are keyed by ship).

**As built in part by package 84 (steps 8 and 9; `docs/design/Design-OneWorld.md`):** a save
holds every hull's stations (`hulls`), each input and act of a station on another ship names
her hull and a replay gives them to her by either road; a seat may be at a person aboard any
hull. The player's own seat on another ship and the drivers following him are this
package's.

**As built (package 58a; the observed world as a station reads it ahead, and the
director's lookups).** **`ahead`** is a row of the registry (`readings.ahead_words`): what
lies on her course within the next glass at her speed, from the deck's own knowledge (her
position by account, her head, the log's speed, the chart, the lookout's sail), in one line,
nearest first: the land, a charted danger within two cables of her track with too little
water for her, the depth by the chart where it shoals under ten fathoms or changes by a
third, a sail in sight within two points of her head; at anchor, aground or with no way on,
nothing. Every station that has the deck's readings has it; the director's is the truth's,
the player's ship's entry in `truth` carrying `ahead` from her true place, head and speed
(the owner's ruling of 2026-10-23). **The truth's lookups** (`truth(ports=, grounds=,
systems=, at=)`; `readings.truth_ports`, `truth_grounds`, `truth_systems`, `truth_at`): a
port's places, people and prices; the fishing grounds; every weather system with its
centre, pressure and track, and the field at the ship (that systems add); a point at sea or
on the land with its depth by the chart and its stream. Each is a small read in place of the
whole truth (R-35's seven to twelve thousand tokens). **The dry run** (`director.dry_run`;
spec §3's channel): what a world order would do, read by performing it on a copy of the
world made by the checkpoint's own pickling and let go, the world itself untouched, so a
replay is the same with it or without. *Taken another way*: the doubt a dry run shows is not
a doubt on the record (68's rule that a reason answers only a doubt the director has seen
reads the director's log, and a dry run writes nothing anywhere, so as to replay alike by
the transcript and by the acts); the dry run's words say to enter the order once, then with
its reason.

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

**As built in part by package 84 (step 9; `docs/design/Design-OneWorld.md`):** the director's
`read_log(ship=)` reads any hull's log, awake or asleep, by her name; the truth names every
hull with her purse, cargo and water and the persons ashore at every port. The attention's
tiers and `focus` are this section's still.

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

**As built (package 53, 2026-10-17; `freesail/world/movement.py` new, `places.py`,
`people.py`, `ports.py`; `freesail/orders/people.py`, `port.py`, `orders/__init__.py`;
`data/vocabulary.yaml`; `data/ports/falmouth.yaml`, `plymouth.yaml`, `brest.yaml`;
`tests/test_orders_places.py`; truths 7b-100 and 7b-101).** **Who goes** is the giver of the
order (`movement.person_of_actor`): the captain for the player at the prompt, the station's
person for a model at its station or the player at his seat; a standing order's firing, a
rule and the director have no place and nothing checks them. `go below` (the captain to his
cabin as always, `captain.below`; anyone else to his berth, the gunroom or his trade's
place), `come on deck` (the quarterdeck for the captain and the officers, the deck for the
rest), `go to the <place>` and `go aloft`, each a `person.moved` line; his duty allows every
place aboard but the captain's cabin, which a man reaches by being sent for. `go ashore`
sends the boat with him to the quay of the port she lies in (the errand `landing`) and she
comes back without him (`person.ashore`: "Mr Travers landed at the quay at Falmouth."); `come
aboard` sends her from the ship lying at his port (`fetch`), and he steps in at the quay and
comes aboard with her (`person.came`). A man with the deck at his station hands it over
first; the master who keeps the reckoning does not leave the ship unless he commands her
(the schooner's and the cutter's). Ashore he is at one of the port's places
(`Person.ashore_at`: the quay where the boat landed him; a person made ashore, where his role
is found). **What he can do where he is** (`movement.check`, from `orders.handle` before an
order is carried out): the deck's orders (the vocabulary's sail, yards, line, heading, points,
none, wreck, work and anchor objects, and the master's helm verbs `put her about`, `shape a
course for`, `give chase`) from the quarterdeck or the deck alone, refused in words naming
the way back ("You are in the cabin; go on deck to give the helm an order."; "You are ashore
at Falmouth, on the quay; come aboard to make or take in sail."), where he is being where he
went by his own word (the reckoning's own taking of the master below to his sights is not his
going below, and the schooner's master who is her captain gives his orders from there as
before; a station bound to nobody named moves nobody); the boat sent and a man sent
for from aboard alone; the market ashore in person at the market, else by the boat from
aboard as always (`movement.market_way`; `Ports.trade_list(person=)`: the prices read at the
market and the price list his, the purse paid at once, the purchase off by the port's lighter
as a job of `BOAT_ASHORE_S["purchase"]`, `LIGHTER_S_PER_TON` a ton and the pull to the ship:
"10 tons of tin came off by the lighter from Falmouth and were struck down into the hold");
every other order (the people's, the port's business by the boat, the reckoning's, the book,
the deck's conversation, the readings) from anywhere he is. The state and the muster say his
place: `the people` and `where is` ("ashore at Falmouth, at the market"; an officer at his
station "off watch, in the gunroom", "with the deck, in the gunroom"), and the muster ends
with the people's places. Nothing moves a person's place by itself but the boat and the
watch's routine (the bill's sleepers, the man sent for, the officer coming up to relieve the
deck, §17). **A world in which nobody moves is as it was**: the place's checks do nothing until
the people are mustered (any move musters them), so that no recorded passage's line moves.
**The port's places** (`places.PORT_PLACES`, `port_places`): the quay, the market, the counting
house, the tavern and the pilots' office at every port, each with what is done there and who
is found there in words, and a port's own beside them from `places:` in its file (Falmouth's
packet office; Plymouth's dockyard and the port admiral's office; Brest's maritime
prefecture). `the places ashore` (or `the port's places`), asked at anchor in a port or
ashore, reads them in words, with the world's people ashore at each by name (package 52's
people made ashore are found where the words put them, `person: make "Mr Gill", a merchant,
ashore at Falmouth, in the tavern`, else where their role is: a pilot at the pilots' office, a
merchant at the counting house, anyone else on the quay); a question answered in the log and
never journaled, and not a reading of the registry, so that `the port` and every sample are
what they were (the lead's reading had them in `the port`, whose words a pinned passage
asks for in port: truth 78's). At the console `go` alone still runs the clock; with words
after it, it is an order.

**Brought back and forward: the place's knowledge (package 65, provisional; the owner,
2026-10-19, on the dispatches test).** Decision 47 dropped locational knowledge as an
overcomplication; the first director's test brought it back by the captain's own account:
everything reached him in the sample wherever he stood, so moving bought nothing and cost
an order, and the station felt like a fixed seat with a view; ashore in Plymouth market he
had the ship's heading, leeway, sails and the frigate's bearing from three miles off. The
owner's ruling: a place is to carry at least what can reasonably be perceived from it, by
action and by what is there. Provisionally, then, and for the brief to settle:

- **What a place gives.** The quarterdeck: the deck's readings, the log as it is spoken,
  the lookout's hails, the conversation of the deck. The masthead: the lookout's horizon
  and his glass, the deck by hail. The cabin: the chart, the papers and the quiet to work a
  course, the deck by report (the officer's word, the messenger) and by what is felt (the
  heel, the motion, the sounds of sail work and all hands). The gunroom: the master's day's
  work and his slate. Below, asleep: nothing until called or woken. Ashore: the port's
  places as §14 has them, and the ship by report, by boat or by letter only; the readings
  of the ship come to nobody ashore. The harness keeps the rule, not the model: a sample
  carries the readings the place allows, and a reading asked for elsewhere is answered
  with where it is to be had ("the chart is in the cabin").
- **Books and papers in their places.** The library's chart, epitome, almanac and papers
  are in the cabin; the master's slate in the gunroom or on deck with him; the book of
  standing orders on deck and in the cabin; the primer and the catalogue anywhere (they
  are the player's reference, not the ship's). A book read where it is not is a walk first.
- **The always-present line.** Every sample of a seated person opens with one line of his
  own: who he is, where he is and since when, the deck (his, another's, nobody's), and his
  state in the needs' words ("You: the captain, ashore at Plymouth, at the market, since
  15:43; the deck the officer's; on your feet since 05:02, hungry"). The owner's thought
  was the `how am I` reading printed each sample; this is that reading with the place and
  the deck added, one line, never more, and the needs' cautions when they come as §20 has
  them. It is the sample's first line so that a model never has to remember where it is.
- **The drill.** Before the station brief, after the three calls of today, a short walk: go
  below, eat, drink, read a book from the library where it is kept, come on deck; each
  answered, so that the model has seen the places and its own line change before the game.
- **Work in its place (the owner, 2026-10-19).** Each kind of work is done where it is
  done: the sailmaker's in the sail room, the master's day's work and his sights' working
  in the gunroom, the captain's writing (his book, a letter) in the cabin, the carpenter's
  below at the damage, the purser's at the hold. Today the rules' people are occupied with
  a place that is only "on deck" or "below" (`People.occupy`, the reckoning's master and
  the mirrored persons), the muster's trades go to their trade's place when sent
  (`TRADE_PLACES`, `movement.py`), and a station holder's own work moves him nowhere but
  the master's, whose sights and day's work occupy him on deck and below through the same
  reckoning whoever holds the station. 65 makes the work's place the room itself, the same
  for the rules' person and for a model or the player at the station doing the same work
  (the model master working the day's work goes to the gunroom and is occupied there, as
  the rules' master is; the captain writing his standing orders is in the cabin), so that
  the place's knowledge follows the work: the master below at his slate hears the deck by
  report. Where a station holder's work and the rules' person's differ today, the brief
  lists them and makes them one.
- **What is not done yet.** Hearing by place is in (§14's earshot); the readings by place,
  the papers' places, the line and the drill are 65's. Decision 47's other dropped item,
  the papers kept in a place, comes with this one as far as the library is concerned and no
  further.

**As built (package 66, 2026-10-19; `freesail/world/hearing.py` new; `orders._say_as`,
`orders/stations.py` `_say`; `agents/tools.py` `submit_order`; the console and the
server).** Who heard a word, and where:

- **Ashore** a word is heard at the same place of the same port (`hearing.spot_of`:
  ("ashore", the port, the place ashore)): the captain at the counting house hears the
  clerk there, and at the market he does not; before, a person's words ashore were heard
  by no station at all, and a station's `say` ashore by every station ashore anywhere. A
  station's `say` ashore says where in its line ("The captain (Mr Travers), ashore at
  Falmouth, at the counting house: ..."), where it said "ashore" alone. Aboard nothing
  changes (the exact place for a `say`, the earshot for a person's words).
- **Who heard** is said in the result of the order that said the words, never in the
  log's line (`hearing.said_tail`, `heard_words`): the stations held that heard it first,
  by their person's name, then the people within hearing by name, four at most and the
  rest counted ("Heard by Mr Veale, ashore at Falmouth, at the counting house."); with
  nobody, "heard by nobody, in the gunroom", and for the director's `say as` where the
  captain is ("heard by nobody: the captain is ashore at Falmouth, at the market"). A
  model reads it at the end of `submit_order`'s result; the player under the order at the
  console and as an unlogged line in the browser.
- **A question to a person nobody holds** says in the asker's result until when it waits
  ("his answer is awaited until 11:08, when the glass is out, and you will be told if none
  comes"); the director's sample carried it already. The thread form ("say to <person>",
  "<person> answers") stays 52's.
- **`say as` by station or trade** (`orders.Voice`, `VOICE_WORDS`, `_by_station_or_voice`):
  one of the people by role or name first as before, then the person a station is bound
  to (`say as the officer of the watch`, `the second officer`), then the ship's own voices,
  which are no persons: `say as the lookout` (his hail from the masthead, heard on the
  open deck and aloft: "The lookout, from the masthead: Sail ho!") and `say as the hands`
  (on the deck); then a man of the muster by his trade. The rule of reach holds: the
  lookout's station held is refused as any held station.
- **Merchant words** (`agent.merchant_ship`, `MERCHANT_OFFICER`): where her wardroom file
  binds the captain's station to a master (or, with no file, her rules-based captain sails
  by the merchant's, the packet's or the fisherman's doctrine), the officer of the watch
  bound to nobody is "the mate" in his brief and the harness's default words; a King's
  ship, and a point world with neither, keep the lieutenant.

**As built (package 68; the cold review of 2026-10-22, R-62 and the D8 note).** `send
the boat ashore with <names>` carries each person named (the captain, the mate and the
boatswain by their roles or names, joined by commas or "and"), or refuses the order in
words and the boat stays: a name nobody answers to, or the captain, who goes ashore by his
own word; before, both were dropped and the errand fell back to the prices. **A waterman**:
`hire a waterman` takes the giver ashore from the ship lying at a port, or off to her from
the quay where he stands, for a shilling a head from the purse, whether her own boat is
away or not; he is in the waterman's boat for the pull (two knots and a half, and five
minutes to shove off and come alongside, judgement) and lands or comes aboard when it is
done (a job of the port's, `Ports.waterman`). The port's own fare is not data yet: a
shilling everywhere. **A thing in the boat**: `in the boat` is a place a thing may lie
(`things.IN_THE_BOAT`), aboard while she is at the booms, and landed on the quay when she
goes ashore.

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

**As built (package 53; `freesail/world/books.py` new; `orders/__init__.py`;
`agents/tools.py`; `data/vocabulary.yaml`, the object `book`; `tests/test_orders_places.py`;
truth 7b-102).** `draft a book "<title>": <its lines, ; between them>`, read before the grammar
as the standing dialect is: every line a standing order (`standing order "x": ...`, or `"x":
...` with the words left out) makes a **sheet**, each read by the standing grammar at the
drafting; every line a bargain (`buy <n> tons of <good>`, `sell ...`, `and` between bargains
split) a **manifest**, read as the market reads one; anything else a **note**, kept as
written. A line of a sheet or a manifest the ship cannot read refuses the draft whole in
words, as do a title the library has already and no lines. The book carries the drafter's
mark (his name, by the order's actor as §14 reads it) and his rank, the day and the hour
(`book.drafted`); it is kept on the World (`books_of`), made again by a replay from the order
that drafted it, and served by the library under `books` to every station from anywhere (a
section a book; listed in the contents once there is one), and at the prompt by `the books`
and `show the book "<title>"`. `post the book "<title>"` (or `post the night orders`) enters
a sheet's orders in the book in the poster's rank (`book.posted`): a line naming another rank
is refused, an order of the same name the poster gave (any, for the captain) is struck and
entered anew, and a sheet that would write over another's order is refused whole. `give the
book "<title>" to the boat` strikes a manifest's bargains together and sends the boat once
(`Ports.trade_list`: every bargain read and weighed first, the room in the hold net of what is
sold and the purse net of what is taken, one that cannot be struck refusing the whole), from
aboard alone. From a station: drafting and reading are anyone's; a sheet posted is judged
order by order as the standing orders the station gives (its rank, its domain;
`tools._book_judged`); a manifest given to the boat as the boat sent on the port's business,
kept back from an officer as that is. The papers kept in a place are not built.

### 17. The equal reach (`tools.py`; `stations.py`)

Every stationed person has the same basic reach: tell and ask any other person aboard or
within hail, go where his duty allows, read what is where he is, journal, stand by; the
domain orders are the station's authority as now. Several stations of one kind on a ship
(45c's groundwork): the frigate's lieutenants as officers under the first, each with his
place and watch.

**As built (package 53; `agents/tools.py`, `agent.py`, `seat.py`, `remote.py`,
`repl.py`, `watches.py` new; `world/stations.py`; `orders/stations.py`; `core/world.py`;
`data/people/frigate-36.yaml`; `tests/test_orders_places.py`).** **The equal reach**
(`tools.judge`, `tools.reach_order`): a station's own move (`go below`, `come on deck`, `go
to ...`, `go aloft`, `go ashore`, `come aboard`) and a book drafted or read are every
station's whatever its domain, with the deck or without; a word or a question (`tell`, `ask`:
package 41's to a station, package 52's to a person nobody holds through a director) reaches a
person within hail (`movement.within_hail`, `orders.stations._within_hail`: both aboard, or
both ashore at one port; out of hail it is refused, "A letter by the boat reaches him, or go
where he is."); the readings, the library and the journal from anywhere, as before; the domain
orders stay the station's authority. A word told a person nobody holds with no director
seated stays refused, as truth 96 has the question. **Several stations of one kind**: the
frigate's file binds the third lieutenant as `third officer` beside package 45c's `second
officer` (each `{kind: officer of the watch}`); the doors and the seat name them by their
number (`officer 2`, `officer 3`; `officer 1` the officer of the watch's own;
`agent.STATION_ALIASES`) or by their person (`--seat "Mr Russell"`; `Stations.resolve`). The
officer's factory takes the station's name (`agent.officer(name=)`, `agent.make_bound`), so
that the second officer is made for Mr Pascoe in the lieutenant's rank (until now a station
renamed kept the first lieutenant's person and outline in its brief), and each officer's brief
says who is first and whose watch is whose (`agent.officers_words`). `Mr Russell, you have the
deck` (or `third officer, you have the deck`) gives the deck to his station, and `I have the
deck` takes it from whichever has it. **The deck by the watch bill** (`agents.watches`, on the
hour from `World.tick`): where two officers' stations are held (a model's or the player's) and
the one with the deck keeps a watch, at the change of the watch the deck passes to the officer
whose watch comes on deck, he on the quarterdeck, given it as at the captain's words (the night
orders, the grants, the last handover note), with one notable `watch.deck_passed` line; the
first lieutenant keeps no watch and keeps it until the captain takes it, and an officer whose
relief nobody holds keeps it.

**As built (package 68; the cold review of 2026-10-22, R-13 and R-14).** A word or a
question from a station to the captain the player holds at the prompt (`held_stations`:
no model at the captain's station, the player seated nowhere else) reaches him: the line
itself, notable in the play log under the speaker's own mark and place ("The officer of
the watch (Mr Pearce), on the quarterdeck, to the captain: no land in sight yet"), nothing
kept in a journal for nobody (`stations._to_the_player_captain`); every model officer's
report to a player captain had been logged "The captain to the captain ... (nobody holds
the station)". A word kept for a station nobody holds is kept under its speaker's mark. The
addressee's words are counted and cut on one tokenisation (`stations._after_words`), and
the longest naming wins ("Captain Bowen," is two words, not one): "Mr Bowen, no land in
sight yet" had lost its "no". Truth 7b-121.

### 17a. Things, free lines and transactions (package 53b; the owner and the lead, 2026-10-19; built the same day)

The owner's question after the dispatches test, where the packet was handed over in words
and the twenty guineas never reached the purse: the director makes people with rigour, so
he could make things the same way, but that invites a large design; eating and drinking
already take any words after the verb and log them; so may a free order be accepted and
logged for the story, and may the director change the purse, or any variable, outright?
The lead's answer, which the owner may overrule, in three parts, none of them a new
simulation:

**Things are the people's sibling.** A thing is made from words as a person is (`aboard: a
sealed packet, in the captain's keeping` or `person: make` for people), with a name, a
description, where it is (a place aboard or ashore by §14's places, or a person's keeping)
and nothing else until a system needs more; weight and size are not kept until the hold or
the boat counts them, and cargo stays the hold's. It moves by hands and places, the game
guaranteeing only its place and its keeper: given to a person it is his, stowed it is in
the place, left ashore it stays there, and it is found where it is by anyone who looks (a
boarding officer's search is the director's story, but the packet's place is the game's).
It appears in the readings of the place and the person, in the people's words ("Mr Veale,
clerk, at the counting house, a sealed packet in his keeping") and in the truth. Made,
moved and kept by the same machinery as people, less their needs and their mouths.

**Free lines.** A short list of verbs takes any words after it and does what the game can
with them, no more, and says so in the log in the words as used: `give <thing> to
<person>`, `hand`, `show`, `take`, `stow <thing> in <place>`, `hide`, `open`, `read`, `put`,
`throw <thing> overboard`, beside `eat` and `drink`, which already work so. Where the words
name a known thing and a known person or place, the thing moves; where they do not, the
line is accepted as said and nothing moves, the log saying "as said; nothing of the ship's
changed" so that the record and the replay stay honest and a model does not learn that the
ship did what it only said. The director reads the free lines in his sample as he reads
the deck's conversation, and answers them in the story. The rule generalises the needs'
orders of package 54 (`eat a fine meal`, `drink three cups of wine`, the verb taken and
the words kept) and costs one list and one logging form.

**Transactions, not variables.** The purse is not to be set; it is to be paid. `aboard:
twenty guineas paid into the purse by Mr Veale` is a world order like any other, doubted
where implausible (money from nobody, a sum beyond a port's means), logged with its cause,
written in the purse's own ledger as "paid by Mr Veale, twenty guineas; the purse £55",
and replayed through the inputs as every act is. The same for a cargo given or taken
(`aboard: ten tons of wool freighted by Mr Veale`), a debt, a bill. The lead's reason for
holding the line against a raw setter: the director's channel exists to produce *data by
which the sets of reasonable acts are refined* (decision 50), and a variable set by hand is
an act with no cause in the record, so it refines nothing; the ledgers and the recorded
passages pin their digests on causes; and a model given a setter uses it where a cause was
available, so that the story loses the texture that made Mr Veale's words good. What the
director cannot do by a form he may already attempt, and the attempt is logged: the purse
was never tried in the test. The owner's prompt, as the owner and not the director, may
keep a developer's setter outside the brief if testing wants one; the director's brief
does not.

**Not done in this part:** a thing's weight in the boat or the hold; a thing's value at a
market (a thing sold is a transaction with a price the director names); a thing searched
for by a person's action rather than found where it lies; locks, seals and keys beyond the
words. Each waits for a system that needs it.

**As built (package 53b, 2026-10-19; `freesail/world/things.py` and `freesail/orders/free.py`
new; `world/people.py`, `orders.py`, `places.py`, `ports.py`, `business.py`, `scenarios.py`;
`core/world.py`; `orders/__init__.py`, `grammar.py`, `vocabulary.py`; `agents/agent.py`,
`tools.py`, `harness.py`, `director.py`; `api/readings.py`; `data/vocabulary.yaml`;
`data/scenarios/dispatches-falmouth.yaml`, `data/director/briefs/dispatches.yaml`;
`tests/test_people.py`, `test_world_orders.py`, `test_business.py`, `test_director.py`;
truths 7b-114 to 7b-116).**

- **A thing** (`things.Thing`) is an id, its name as said ("a sealed packet"), a
  description (the rest of the words that made it) and where it is: a person's keeping
  (`keeper`, his id: it is where he is, aboard, in the boat or ashore at his place of the
  port), a place aboard of §14's with its spot in words (`place`, `spot`: "on the table" in
  the cabin), a place ashore (`place` "shore" with `port` and `ashore_at`), or over the side
  (`OVERBOARD`). Nothing more. The registry is the World's `People` (`People.things`), so a
  checkpoint holds them whole and a replay makes them again from the orders and the
  scenario that made them and the free lines that moved them. Made **by the scenario**
  (`things:`, each the words of the `aboard:` form or `{name, where, description}`, made
  with the people at their muster: `People._scenario_things`; a where that names nobody is
  the scenario's error in words; `Scenario.things` absent from the save's dict when empty)
  and **by the channel**: `aboard: <a thing>, <where>[, <more of it>]` makes one, `aboard:
  the <thing>, <where>` moves one known (`orders._aboard_thing`). The where's forms
  (`things.read_where`): `in the captain's keeping`, `in the keeping of Mr Veale`, `kept by
  ...`; `in the hold`, `on the cabin table`, `on the table in the gunroom`, `under the cabin
  table` (the place found among the words, the spot the rest); `ashore at Plymouth[, at the
  counting house]`, `at the counting house at Plymouth`. Any other phrase is the thing's
  description; no where said is refused in words naming the forms, so that the table's
  things (`aboard: a cask found stove`) and the free words of 50's honest answer (`aboard:
  the cook reports the beef cask found rotten`) are what they were. The play log says
  nothing of a thing made (decision 46): it is met where it is. **The readings** say it
  where there is one and only then, so that a world with no thing reads as it did: the
  people's words end a person's line with what he keeps (`People.keeping_words`: "Mr Veale,
  clerk: ashore at Plymouth, at the counting house, a sealed packet in his keeping."; the
  same in `where is`), and `people` carries a `things` list; `the places` adds what lies in
  each place aboard ("In the cabin: a sealed packet on the table.", and `items[place].things`);
  `the places ashore` adds "lying there" at each place of the port; the truth carries
  `things` and says them in its words. **Reach** (`things.reach_why`, `same_place`): a thing
  in his keeping, or lying in his place, or within earshot of it on the open deck (§14's
  `earshot`), or at the same place of the same port ashore; a person likewise. **The rule
  of reach** (`orders._aboard_reach`, through `reach` for every source as the person's
  rule is): nothing put into the keeping of a person a model or the player holds, nor taken
  out of it, refused in words that say to leave it where he can take it ("on the cabin
  table") and say so. **The doubt**: a thing made never; a thing moved from one port to
  another, or between the ship and a port beyond `BOAT_REACH_NM`, by no hand that could
  carry it. A person leaving the world (the pilot put off) takes what he keeps ashore at his
  port.
- **The free lines** (`orders/free.py`): `give` (and `hand ... to ...`, the sail's bare
  `hand` being `take in` still), `show`, `take` (`pick up`), `stow`, `hide` (`conceal`),
  `put`, `open` (`unseal`, `break the seal of`), `read`, `throw` (`toss`), each a verb of
  the vocabulary's object `free`, listed with `eat` and `drink` in its `free_lines` (the
  class; the needs' orders unchanged). The giver is the order's person
  (`movement.person_of_actor`); a rule, a standing order's firing and the director are
  refused in words (no hands aboard). The words after the verb are read for a thing known
  (`things.find`: its name whole, its noun, either side of "of") and a person (`People.find`)
  or a place: `give <thing> to <person>` or `give <person> <thing>`; `stow|hide|put <thing>
  in|on|under ... <where>` (a place aboard within his reach, or a spot in his own place,
  or, ashore, his place of the port); `throw <thing> overboard|over the side`. Where they
  name a thing within reach, and a person within reach for a giving, the thing moves and
  the line says where it is now ("By the captain, ashore at Plymouth, at the counting house:
  gave the packet to Mr Veale; the sealed packet is in Mr Veale's keeping."); where they do
  not, or the verb moves nothing (`show`, `open`, `read`), the line is "..., as said;
  nothing of the ship's changed" with the reason in brackets when a thing or a person was
  named. A thing given to a person a model or the player holds lies before him (`spot`
  "before Mr Pearce"), and his own `take` makes it his. The line is the order's kind
  `free.line`, notable, in the words as used with the verb put in the past, heard by the
  stations held within the giver's reach (`Harness.hear`; `free.line` among
  `WORDS_BETWEEN_PEOPLE`, its hearers named, so that `stand_by('a word on deck')` wakes
  there and nowhere else), read by the director in his sample as the deck's conversation,
  and journaled as the order it is. Every station's, with the deck or without
  (`Domain.why_not` allows the object `free` as it does `needs` and `glass`; `tools.
  own_order` exempts it from the deck's check, with the needs).
- **Transactions** (`orders._aboard_transaction`, `_freight`; `places.Purse.receive`,
  `pay_to`, `owe`, `ledger`; `places.Hold.freight`, `freights`): `aboard: <a sum> paid into
  the purse by <payer>[ for <cause>]`, `... paid from the purse to <payee>[ for ...]`, `a
  debt of <a sum> owed to|by <party>`, and `<n> tons of <good> freighted by <freighter>[ at
  <place>][ for <port>]`. The sum is read in the clerk's figures or words (`read_sum`:
  "£30", "£6 10s", "twenty guineas" at twenty-one shillings, "thirty pounds ten
  shillings"). Each is written in the purse's or the hold's own ledger with its cause (the
  purse's `entries` as every sum's, "paid by Mr Veale, twenty guineas (£21)", and its
  `ledger` of the channel's kinds `received`, `paid`, `owed`, `owing` with the party and the
  purse after) and as a notable line of the purser's books or the manifest in the play log
  (`purse.received`: "Paid into the purse by Mr Veale, twenty guineas (£21); the purse
  £55."; `purse.paid`; `purse.owed`; `hold.freighted`), the director's log keeping the act.
  A sum paid out beyond the purse is refused ("nothing is paid below nothing"); a debt moves
  no money. A freight is the market's own form at no price: off by the port's lighter where
  she lies in port (the market's `lighter` job, its line "came off by the lighter ... and
  were struck down into the hold"), struck down at once where the freighter is aboard, the
  manifest written with its cause; the hold's room for it is what is left after the
  purchases in the boat and the lighter (`_tons_coming`). The `purse` reading carries
  `ledger` and `debts` only once there are any. **The doubt** (`_doubt_aboard_new`): money or goods from nobody, or
  from a person the world does not know; a payer, payee or freighter neither aboard nor at a
  port she lies within `BOAT_REACH_NM` of; a sum beyond the port's means
  (`business.port_means_pounds`: the business's largest cargo, 120 tons, at the dearest
  price of the port's market as of the day; judgement); a freight to a ship in no port by a
  freighter not aboard. **The reach**: a held person's own payment, freight or debt owed by
  him is refused (his holder's word).
- **The director's brief** (`DIRECTOR_BRIEF`) gives a thing made or moved and the four
  transactions among the examples and says that his words move no money and no thing,
  that a sum changes only by a transaction with its cause, that nothing is set, the reach
  for a held person's keeping, and that the free lines are the people's, read in his
  sample. The dispatches brief's examples gain the sum paid, the freight and a letter left
  on the cabin table; the dispatches scenario carries the packet as a thing in the
  captain's keeping, from the Custom House.

**Taken another way.** (1) *The lead's reading had a freight the hold cannot stow doubted*:
it is refused in words, as a payment below nothing is. The hold's tons are the game's (the
cargo stays the hold's, item 1), so no reason makes room; entered again with a reason it is
logged as attempted, the honest road for an order the game cannot perform. (2) *A sum
beyond a port's means "by the business's figures"*: the business keeps no figure of a
port's money, so the bound is made of the figures it has (its largest cargo at the port's
dearest price), judgement in the tuning notes. (3) *The lead's reading had the free verbs
"one list in the vocabulary with the verb's class `free`"*: they are verbs of the object
`free` beside a `free_lines` list naming the class with `eat` and `drink`, since `hand` is
the sail's word already and `eat` and `drink` keep their object `needs` unchanged; `hand`
is a giving only with "to" and no sail after it. (4) *Show, open and read*: the game keeps
nothing of a thing's being seen, opened or read (locks, seals and a thing's contents are
kept out), so each is "as said" whatever the words name. (5) The places' reading carries
the things lying there; a hidden thing is no different from one put down (no flag kept),
and every station reads it until the place's knowledge (package 65) decides who sees what
in a place.

### 18. Truths for 7b-iv

- 100. A person who goes below is below in the muster and the state; an order of the
  deck's from him is refused in words until `go on deck` brings him back.
- 101. The player ashore buys at the market in person; aboard, by the boat.
- 102. A drafted manifest given to the boat trades its goods in one errand; a drafted
  night-orders sheet posted is the standing orders.

**As built (package 53; `tests/test_known_truths.py`, truths 7b-100 to 7b-102).** 7b-100:
the frigate at seed 7 off the Lizard with a fake officer of the watch given the deck, who goes
below (the gunroom his place in the people and the muster, "with the deck, in the gunroom"),
is refused `take in the royals` in the words naming the way back, and a glass later comes on
deck and has it carried out; the captain at the prompt alike, refused the helm in his cabin;
the save replayed by the transcript and by the acts to the same digest. 7b-101: the schooner
at anchor in Carrick Road, her master (the player) landed at the quay by the boat, refused the
deck and then the market until he goes to it, buying ten tons of tin there in person with the
boat at the booms and the tin off by the lighter, brought aboard by `come aboard`, and aboard
buying by the boat; the save replayed to the same digest. 7b-102: the same road, a manifest of
two purchases given to the boat trading them in one errand, and a sheet of two standing
orders posted, in the book in the master's rank and firing; both books in the library with his
mark from the officer's station; the save replayed to the same digest and the same books. No
recorded passage's pin moved: none moves a person, goes ashore or drafts a book, and the
place's checks muster nobody.

Package 53b's (§17a):

- 114. A thing made by the director in the cabin is given by the captain to a person ashore
  by a free line when he is there, is in that person's keeping in the people's reading and
  the truth, and stays there through a save and a replay.
- 115. A free line that names nothing known is logged "as said; nothing of the ship's
  changed" and moves nothing, and `eat` and `drink` log as before.
- 116. `aboard: twenty guineas paid into the purse by Mr Veale` with Mr Veale ashore at the
  ship's port credits the purse with the ledger's line, is doubted with him thirty miles
  off, and a payment below nothing is refused.

**As built (package 53b; `tests/test_known_truths.py`, truths 7b-114 to 7b-116).** The
schooner at seed 7 at anchor in Carrick Road, her master who commands the player at the
prompt, the director's orders given at his door as the player's seat gives them (inputs,
replayed through the door). 7b-114: Mr Veale made a clerk ashore at Falmouth (at the
counting house by his role) and the packet on the cabin table; from the quarterdeck `give
the packet to Mr Veale` is "as said" (the packet in the cabin); below, `take the packet`;
ashore by the boat with it in his keeping, at the counting house, `give the packet to Mr
Veale` moves it, and the people's words, the reading and the truth say it is Mr Veale's;
the save replayed to the same digest and the same things, and a checkpoint holds them.
7b-115: ten free lines of the verbs, each naming nothing the world knows, each a notable
line ending "as said; nothing of the ship's changed", journaled, the things, the purse, the
hold and the people as they were; `eat a fine meal` and `drink three cups of wine` answered
to him alone, no line of the log, the words in the record. 7b-116: the twenty guineas paid
by Mr Veale at Falmouth undoubted, the purse £21 the richer, its ledger "Paid by Mr Veale,
twenty guineas (£21); the purse ..." and the purser's notable line, the director's log
"director.order"; in the same water with Mr Veale made at Plymouth instead, thirty-four
miles off, the same order doubted (neither aboard nor at a port she lies within a boat's
reach of) and nothing paid; a sum from the purse a pound beyond it refused "nothing is paid
below nothing", the purse as it was. No recorded passage's pin moved: none has a thing, a free line or a payment by the
channel, and every reading's new key is there only when one is.

## Part 7b-v: Needs

### 19. Provisions and water (`freesail/crew/`, `freesail/world/stores.py` or where the stores live; `data/ships/*.yaml`)

The crew eat and drink on the schedule as they rest (M3's watches): the ship's provisions
and water fall by the ration a day (the period's: a pound of biscuit, a pound of salt meat
or its day's kind, a gallon of beer or a quart of water, from the Regulations; the figures
in the ship files), the purser's reading says what remains and for how long, the market
sells them, short allowance is an order with its effect on the hands and their temper,
water found foul is a thing the director may do aboard (§3).

**As built (package 54, 2026-10-17; `freesail/crew/victuals.py` new, `crew/routine.py`,
`world/places.py` `Stores`, `api/readings.py`, `ship/schema.py` and `tools/gen_ships.py` for
`crew.ration`; `data/crew/ration.yaml` new; `tests/test_stores.py` new; truth 7b-103).** The
ration is data (`data/crew/ration.yaml`): the Navy's table of the Regulations of 1806 (Sect.
IX, Chap. I, Art. I, the 1808 printing in `docs/references/admiralty/`) by the day of the
week, a pound of biscuit and a gallon of beer every day, beef on Tuesday and Saturday, pork
and pease on Sunday and Thursday, oatmeal, butter and cheese on the banyan days (the table's
heads and the substitutes of Art. II are legible in the OCR, its figures are not, and are
given as the printed table has them, to be checked; its sugar column is left out, not
guessed); the meals at eight, noon and four, a third of the day's ration each (judgement);
252 gallons to the ton of water (a tun, wine measure); short allowance a half. Each ship file
names its table and the water a man a day in a `crew.ration` block (`table: navy`,
`water_gallons: 1`, the figure her water was sized at), written by the generator for all
six. At each meal (`victuals.tick`, once a minute from the World) the provisions fall by the
meal's share in days at full allowance for the company mustered and the water by its share
of the company's gallons, at the allowance she is at; nothing of it is a line: the purser's
reading (`the stores`, and the purser's books) says what remains, for how long at the
allowance (the water's days and the provisions'), what is expended since she was stored and
the day's proportion a man. The log hears of the stores when one runs out ("The last of the
water started at supper: the ground tier is dry", notable, once) and of `short allowance` and
`whole allowance`, the captain's orders (object `allowance`, outside every lesser domain),
whose notable line says the share, that every man is alike, and the people's temper ("The
people take it sullenly"). The hands: the routine's fatigue rates scaled by a hardship
(`Routine.hardship`, 0 to 1, set from the stores each minute): short allowance its
shortfall, a store run out the whole, the water found foul a quarter (drunk in the grog and
the coppers at a cost); work and idleness tire `1 + 0.5 h` as fast and rest makes up `1 -
0.5 h` as much (judgement); at nought the routine is as it was to the bit. The market and the
yard sell water and provisions as before (`take in water`, `take in provisions`). A ship
whose file keeps neither is not victualled. Class defaults on `Stores` and `Routine` let a
checkpoint from before load.

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

**As built (package 54; `freesail/world/needs.py` new, `people.py` `Person.needs` and the
asleep state's words, `core/world.py`, `agents/harness.py`, `agents/model.py` `Sample.needs`,
`agents/tools.py`, `orders/needs.py` new, `data/vocabulary.yaml`, `ui/console.py`,
`ui/server.py`; `data/crew/needs.yaml` new; `tests/test_people.py`; truth 7b-104).** The
needs live on the person (`Person.needs`, made at the first look) and are kept by the
World's `NeedsKeeper` once a minute: the hours since he last ate and drank, and for fatigue
the hours of waking he owes, made up eight to the hour asleep below and four where he fell
asleep. The steps are `data/crew/needs.yaml`'s (hunger at 12, 30, 40 and 48 hours; thirst at
10, 28, 38 and 46; fatigue at 20, 36, 44, 50 and, the last, asleep where he stands at 56;
judgement, set so that once a day to eat and drink and a sleep every day or two keep a man
clear of every line, and two days without bring every urgent line and the third the sleep).
**By hand at a filled station**: the person of a model's station, of the player's seat, and
the captain while the player is at the prompt (a driver listening, or after an order of his
own needs) and no model holds the captain's station (`held_stations`, package 52); taken in
hand from what the routine made of him (fed at the last meal, awake since the morning watch,
none of it before the scenario began), and given back to the routine when nobody holds him.
Everyone else is reckoned by the clock, never shown. A person who is also a hand (drawn
from a station of the muster) has the crew's fatigue read at the file's bounds (`crew/
hands.py` stays the crew's), and the watch bill rests him. **The lines**: the first step
never; a notable line at the change of the watch, at most one a watch, every need risen
since said together; an urgent one at once; nothing while he sleeps. They go to the person
stationed alone: a model's next sample as a notice ("You are quite thirsty.
(submit_order('drink'))") and its `needs` while any shows; the player's through the keeper's
listeners (the console prints the line, the server sends it to the pages as an event), never
the log. **His orders** (object `needs`, every station's domain): `eat` (at a table in the
cabin, the gunroom, the galley or ashore; elsewhere a biscuit and cheese brought up from the
stores; half a meal at short allowance; refused when the provisions are expended), `drink`
(the scuttle-butt on deck; his beer when the water is foul; `drink the foul water` at six
hours on his fatigue), `sleep` (the player below to his berth, the cabin for the man who
commands, the gunroom else, until his next order, an urgent line or rested; refused with the
deck below the captain's and within the hour of his last sleep; called, he goes back where
he turned in from) and `how am I`; each answered to him as an unlogged kind
(`needs.answer`, `UNLOGGED_KINDS`), kept in the inputs so that a replay answers it again.
A model turns in with `stand by, asleep below until called` (`harness.ASLEEP_BELOW`), its own
stand-by line in the log, woken by a word, a question, an urgent line or its rest; at
fatigue's last step the harness stands it by asleep where it stood (`fall_asleep`), quietly,
its journal saying so; an urgent need wakes any other stand-by. The player asleep is woken by
his next order (`World.submit`). The people's state says "asleep, in the cabin" or "asleep
where he stood, on the quarterdeck" for a stationed person asleep by his needs. While a
model holds the captain's station the owner at the prompt has no needs and `eat` is refused
in words.

### 21. Truths for 7b-v

- 103. The frigate's provisions fall by the ration for her complement; the purser's
  reading says the days remaining; short allowance halves it.
- 104. A player who neither eats nor sleeps for two days reads the urgent lines in order
  and is asleep on the third; eating from the stores and a night below reset them; an
  unseated person's needs never show.

**As built (package 54; `tests/test_known_truths.py`, truths 7b-103 and 7b-104).** The
frigate at seed 7 on the plane from 06:00 on 10 June to 05:00 on the 13th with the player at
the prompt (a listener, as the console), the fixture `needs_days` of the slow tier. 7b-103: a
day's three meals take a day of provisions and 264/252 tons of water; the reading says
"water 99 tons for 94.5 days, provisions for 119 days"; a meal at short allowance takes a
sixth of a day and the reading doubles the days; the order's notable line with the temper is
the one line of the stores in the log. 7b-104: the player's lines in order (thirst and
hunger at noon on the 11th, parched and drowsy at the first watch, very hungry at midnight,
then urgent: desperately thirsty, absolutely starving, hardly able to keep his eyes open) and
asleep where he stood at 14:01 on the 12th; eating and drinking wake him, a night below
rests him, and at five on the 13th nothing is said of him; the first lieutenant, whom nobody
holds, is the routine's; no line of the needs in the log. No recorded passage's pin moved: a
passage has nobody at the prompt, the stores' fall writes nothing, and the routine's
hardship is nought at whole allowance with sweet water.

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

**As built (package 56; `freesail/world/fishing.py` new, `freesail/orders/fishing.py` new,
`data/fishing/fish.yaml`, `channel-west.yaml` and `biscay-north.yaml` new, eight gear
evolutions under `data/evolutions/` with `scripts.FishingGearScript`, the gear in the ship
files through `tools/gen_ships.py` and `ship/schema.py` `GearSpec`).** The grounds are
tables keyed to the chart's features (the business's Eddystone, Poll Bank, Iroise, Ushant
and Glenan grounds) or pricked at a position with their source (the seine grounds of Gerrans
Bay and St Ives Bay, the drift ground of Mount's Bay, the trawling ground off Berry Head),
each fish with its gear, months, hour (night, day, any) and yield in tons an hour of the
gear fishing; a bottom or a bank the tables do not name keeps a default. The seasons and the
gear's forms and hours are Holdsworth 1874's (the OCR in `docs/references/holdsworth/`) and
the Britannica of 1810's (CLUPEA, after Pennant and Borlase), the Breton sardine's the Musée
de la Pêche's; every yield, keeping time and fish-quay price is judgement with its
reasoning (`docs/dev/TuningNotes.md`, package 56). **One catch function** (`fishing.take`),
called a minute at a time by the player's and a crewed fisherman's World (`Fishery.tick`)
and by the far body (`fishing.far_work`, the same evolutions' shoot and haul times), with
the hour's factor (the night's fish half as much again at the change of light), the wind's
(full to six tenths of the gear's most, half at the most, nothing beyond) and, for the
trawl, the way's (one to four knots). The smack carries a 36-ft beam trawl, longlines and a
small tuck-sean for her boat; the lugger a fleet of sixty drift nets and lines; no other
ship any. The orders: `shoot`/`haul the trawl`, `the nets`, `the seine`, `set`/`haul the
lines`, `shoot`/`haul the gear`, `sell the catch`, `the catch`, `the fishing grounds`
(object `fishing`); a shot is refused in words for gear she lacks, off every ground, out of
season, at the wrong hour or in too much wind; the hauls are all hands. While the gear is
out the work in hand says "towing her trawl", "riding to her nets", and a sail beyond the
gear's allowance is refused in `orders.verbs._sail_check`; **the trawl drags** (a drag on
her way in `physics/integrate.py`, `ship.extra["gear_drag"]`, set only while a trawl is
down: the smack tows at two and a quarter knots in fourteen of wind under plain sail).
The catch goes into the well first (a ton to three cubic metres, three tons in the
Culloden's), alive for the fish that live there and cool for a day for those that do not,
then the hold, salted while the salt lasts, else spoiling in hours by the season; a lot
that turns is a notable line, and the catch's line is said each morning at eight. The fish
quays are `fish.yaml`'s twelve ports with a factor on each fish's price, fresh or salted,
apart from the ports' cargo markets (which deal in the cured hogshead and were left
untouched so that no price list moves). The business's fisherman shoots the gear her
ground wants, fishes and hauls by the same times and the same function, hauls on her
trip's end and lands her catch at home's quay (`Drawn.landed`); she is crewed like any
other ship near the player (`crews.FAR_ONLY_ROLES` empty), her World and her far body
sharing one `Fishery`, her captain working the gear in Python from `Captain._station`
(`fishing.captain_work`: shoot when it fishes at the hour, heave to riding to it, haul
when full or when the hour no longer serves, home when the hours are done), the doctrine's
tables unchanged. A fishing trip's mark is the ground itself, not a station a league off
(which put a bay's station on the land). Truths 7b-105 and 7b-106.

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

**As built (package 56; `freesail/world/lookout.py` `glass_tier`, `glass_state`,
`glass_words`, `Lookout.glass_on` and `_glass_line`; `freesail/orders/glass.py` new).** The
tiers at two miles, eight cables and four, each bounded by the visibility, a tier less at
the twilight, and by night within a mile only a light (a fishing vessel at her gear hangs a
lantern; others show none). A crewed ship's words are her own World's: the manoeuvre in
hand, the heave-to's record (her tack and the sail aback, "main topsail aback"), the work
in hand's gerunds, her gear; a far ship's her plan's leg (lying to, at anchor), her sail
state, her tack and point of sailing from her heading and the wind, and her far gear's
phase. The lookout says "The glass on the brig on the starboard bow: ..." unasked when a
sail comes within the tiers and when her state, her work, her light or a nearer tier
changes the words (her point of sailing alone is not a change, and a ship running before
it is read on neither tack), not oftener than five minutes, and never of a boat under oars;
**it moves the recorded passages' pins** wherever a sail comes within two miles by day (the
pilot cutters, the strangers of the trials: `docs/dev/TuningNotes.md`, package 56); `the glass
on <ship>` is a reading every station may ask (`agents.agent.Domain.why_not`). **The
sighting says her heading**: every `lookout.made_out` line now gives her relative bearing,
her compass bearing and the course she stands ("The sail on the larboard bow, bearing SW by
S, is a brig, standing to the eastward (E by N), under plain sail."), and `a sail in sight`
adds the course once her rig is made out, which is what a sample carries. Truth 7b-107.

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

**As built (package 59; `freesail/__main__.py`, `freesail/settings.py`,
`freesail/ui/harbour.py`, `client/harbour.html`, `harbour.js`; `docs/agents/Harness.md`
§22).** `py -m freesail` takes the server's own command line (`server.server_parser`, two
flags added to it: `--business on|off` and `--director-brief BRIEF`) with `--no-browser` and
`--settings FILE`; the settings give the flags' defaults (`ap.set_defaults`), so a flag given
wins for the run; it goes to the game's folder (the paths given made absolute first) and
serves the harbour at `/harbour`, opening the browser on it. With no scenario, ship or save
named, no game is in play: the server holds a point-ship World at tick 0 and `/` leads to
`/harbour` until a game is started. **A game started from the harbour is the server's
game**: the page's choices become the flags' namespace and the server's own
`prepare_game` (the server's `main` factored, every step in its old order: the World, the
scenario's lines and orders, the standing orders, the crewed budget, the director's brief,
the seat, the book's opening words) makes it; `Driver.replace_world` takes it up in place
(the clock held, the old World's log no longer heard, the pace and compression set, the
painter and the consent records moved to it, `{"type": "restart"}` to every open page,
which reloads), one server process with the harbour reachable throughout. The page's
controls are the flags: the scenario (the game's and the player's own, by name), a ship
file, a save, the seed, the seat (as the scenario says, the captain at the prompt, or a
station below or above), the compression, the pace (the pace rule, lockstep,
free-running), the crewed cap and range, the business, a director's brief (a starter, a
file or words), the standing orders and the easing on a station. It shows the game in play,
the stations held and by whom (the agent API's, a model's through its door, and the
player's seat), the doors started from it and the desktop client's entries present.
**The settings** (`freesail/settings.py`): `%APPDATA%\FreeSail\settings.yaml` on Windows,
`~/Library/Application Support/FreeSail/` on macOS, `$XDG_CONFIG_HOME/freesail/` elsewhere,
`FREESAIL_SETTINGS` naming another: the server's host, port and whether to open the browser;
the game's default seat, compression, pace and crewed budget; the places of the saves, the
player's scenarios (both beside the settings unless named; never inside the repository),
the consent records (the game's own unless named) and the desktop client's file; per door
the model's name, the API door's dialect, effort and flags, the local runner's endpoint,
model and flags. A field named for a key, a value of a key's shape, or a value holding the
key the credential store has, is refused in words and nothing is written; the harbour says
only whether the store holds a key (truth 7b-110). The harbour does not take a key: it is
put in the store at a terminal (`py -m freesail.agents.api --store-key`), as package 42 left
it. **The doors**: one desktop entry per station ticked, `freesail-<station>` (and
`freesail-<station>-<ship>` on another ship), in `.mcp.json`'s form (`py` on Windows,
`python3` elsewhere; the game's address; `--station`; `--model-name` from the settings or a
placeholder that says to set it; the game's folder on `PYTHONPATH`), the client's whole file
shown as it would read first and written only on the player's word with the old file kept
beside it (`.bak`), every other server in it kept. The API door and the local runner are
started as the server's subprocesses with their own command lines (`python -m
freesail.agents.api` or `.local`, `--game`, `--station`, `--ship`, the settings' model and
flags; nothing re-implemented), their output in a pane with a line to their terminal for
the owner's word in a consent conversation, each stoppable (the door's own Ctrl-C where the
platform has a signal for it, then its station released at the game by the desk as the
door's Ctrl-C releases it); a door that ends says so in its pane with its exit code in
words (`EXIT_UNREACHABLE`: it could not reach the game or its model, or would not start).
A shortcut that starts the harbour (`FreeSail.cmd` on the Windows desktop) is shown and
written on the word. Truth 7b-108.

**The owner's first use (2026-10-18; package 64, provisional).** The harbour as merged works
and is not yet a usable interface: unclear to a newcomer; the station and seat settings not
explained against each other (the settings' seat, the scenario's `stations:` and the doors'
"on another ship" are three notions and the page says nothing of which is which); the flags
not explained where they are set, though the parser holds every help line; one model per
door, so several models at several stations want several settings files, where a
per-station entry is wanted; the maker without the papers (the chronometer first) and the
people, which the loader reads; and no way to write the people aboard into a scenario by
name with a short brief each, which the owner hoped for (`people:` takes a role, a name, a
skill and a place; the character, rank, traits, history and station brief, is the ship's
wardroom file's `Outline` per role, the same in every scenario; the owner's clarification
of the same day: the people, not the stations). The refinement is package 64, briefed after
the owner's testing round; `docs/dev/M7b-WorkPackages.md`, "The harbour's second pass".

### 21e. The scenario maker (`client/harbour.js`; `freesail/world/scenarios.py` `write_scenario`)

A form on the harbour that writes a scenario file from choices, in the file's own form so
that a hand may still edit it: the ship, the start (a port's road or a position pricked on
the chart), the date and hour, the weather (a preset of the climatology's, or a scripted day
from the forms the primer gives), the other ships with their intents, the business on or
off, the crewed budget, the standing orders (a starter book, or a drafted one), the stations
and who holds them, a director's brief from the starters or the player's own; saved under
the player's scenarios place and listed by the harbour; loaded back into the form for
editing. The scenario is proved by loading it as the console would.

**As built (package 59; `freesail/world/scenarios.py` `scenario_text`, `write_scenario`,
`read_scenario_text`, `stations:`; `Harbour.prove`, `save_scenario`; `client/harbour.js`).**
The writer works on the file's own fields (a mapping, as YAML reads it, dates in their ISO
words). Without the text they were read from it writes a new file in the hand's form: a
header saying what made it and how to start it at either driver, the fields in the
docstring's order, each section under a comment a hand would want, a plain mapping or list
in flow, the other sail and the waypoints an item a line wrapped as a hand wraps them, the
first orders a line each, `business: on|off` in the hand's words. **With the text it was
read from, only the changed fields are written again**: the file is cut into its top-level
fields (each with the margin comments just above it and its body to its last indented
line), an unchanged field keeps its lines and every comment above and beside it, a changed
one is written in the hand's form under its own comments (a one-line field keeps the
comment beside it), a field taken out goes with its comments, a field put in goes after
the field it follows in the hand's order under its section's comment; the line ending is
the original's (`newline_of`: a file Windows wrote keeps its CRLF). Every text is proved to
read back as its fields before it is returned. **Every scenario of `data/scenarios/` is
written again byte for byte with nothing changed**, and written as a new file each loads to
the same `Scenario`; through the page, the owner's four (`smack-falmouth`,
`lugger-roscoff`, `directed-passage`, `dispatches-falmouth`) read into the form and saved
are their own bytes (`tests/test_harbour.py`). The form keeps the fields it read and writes
over them only those the player touched, so that an untouched field is never rewritten by
the form's own reading of it. Its parts: the day (name, seed, start, nation); the ship
(file, heading, the glass, the instrument, the purse, the intent); the start (a port's road
from the ports' files placed by the chart's features, a region, or a position pricked on
a simplified drawing of the region's coast, `GET /api/harbour/chart`); the weather (the
month's climatology, the wind pinned by the hour in a table of waypoints, or as written, a
hand's systems kept untouched); the business, the crewed budget, the ports, the other sail
with their intents in a table (a row's other fields kept), the world orders by time; the
starter books and a drafted book (written beside the scenario as `<name>.orders` and named
in its standing orders), the first orders; the stations and who holds them; the director's
brief as a starter, a file or words, or written in the form (name, tone, challenge, the
limits, the cadence, the budget), started from a starter if wished. **`stations:`** is a new
field of the file (`{captain: model, officer: player, director: model}`; holders `player`,
`model`, `rules`; one seat for the player), read by the loader, and the player's seat it
names is taken by either driver as `--seat` would take it, the flag winning (`--seat
captain` now means the captain's prompt, no seat, where it was refused). **The proof** is
the console's road: the text loaded by `load_scenario`, its World made, its standing
orders and first orders given (an order refused is a refusal), the player's seat found;
the loader's refusal shown in the form in its own words with no temporary file named
(`data/ships/nope.yaml: no such ship file.`). Saved only under the player's scenarios
place (never inside the repository), a name already there refused unless the player says
to write over it; listed by the harbour as his own and read back from there. Truth 7b-109.

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

## Part 7b-x: The boat (the owner, 2026-10-18)

### 21k. Towing by the boat, and the boat as a vessel (`freesail/physics/` an oar force on a hull; `freesail/evolutions/`; `data/ships/boat-*.yaml` through `tools/gen_ships.py`; `freesail/world/crews.py` the boat crewed; `freesail/orders/`; the viewer)

**Kedging needs no package.** The owner's test on the m6c build (2026-10-18): a kedge laid
out ninety fathoms to the west of a ship heading north and hove short brought her head to
the westward and drew her toward it; the pull has been in the anchor physics since package
34 (heaving in shortens the scope, the cable comes taut at the hawse, her head swings to the
pull and she comes ahead), so kedging by hand is lay out, heave short, weigh, lay out again,
and the rules captain is not given it until a case calls for it. One fault from that test
is mended here: a **false denial**, "the boat was not sent away", said while the lay-out
evolution went on and completed.

**Towing by the boat:** `tow her with the boat [to <the point or bearing>]`, the boat ahead
on a tow-line with her oars, the ship's head brought round or the ship moved at the boat's
pace against her resistance and the tide (a quarter of a knot to a knot for a cutter or a
lugger by the boat's size and hands; little or nothing for the frigate, whose boats towed
her head round in a calm and no more: the period's practice and a judgement in the tuning
notes); the boat's crew tiring by the hour; `the boat alongside` ends it; refused in a sea
the boat cannot work in. The force is an **oar force on a hull** by the hands at the oars
and their fatigue, one mechanic for the tow and for the boat herself.

**The boat as a vessel** (the owner: the player can now go aboard the boat, 53's places,
and the larger boats should be able to be rigged with a very simple rig, or at least
ordered under sweeps): each ship's boat gets a ship file through the generator (a 16-ft
boat with four oars and a sprit or lug sail stepped at will, the frigate's launch and
cutter larger, with their sources or the word judgement), and is a vessel of the world
when manned and away from the ship: crewed by the promotion's machinery (her own World,
small), the oars her propulsion by the oar force and the sail when stepped, the sweeps'
order (`give way`, `lie on your oars`, `step the mast`, `set the lug`, `pull for <the
point>`); **the player aboard her** by `go to the boat` and the seat on another vessel
(51's `--seat captain --ship "the boat"`, or the console's seat following him into her),
her readings his while he is in her, the ship's again when he comes aboard; the errands
(ashore, the kedge, the tow, the pilot) done by her as before when nobody is in her;
the viewer drawing her under oars or sail; the account following the boat as a vessel's.
After 51, which gives the player a seat on another vessel.

### 21l. Truths for 7b-x

- 113. The lugger becalmed with the ebb setting her toward the Lavandière is towed clear by
  her boat at half a knot; the frigate's boats bring her head round in a calm and move her
  no distance worth the account's notice.
- 114. The player in the cutter's boat pulls ashore at Falmouth from Carrick Road under
  oars, steps the mast and sails her back under her lug, the readings his in the boat and
  the ship's again aboard; the boat's errands run as before with nobody in her.

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
  **As built (package 58b, 2026-10-23): 57's debt, the gale book's mending.** The book's
  mending is built and the judgement of it waits for the lead's playtest: a head sail
  straining at its bolt-ropes in a wind over the shorten-sail line is taken in before it
  blows out (the fore topmast staysail, blown out at 8983 in the station gale before, is
  taken in at 8820 and nothing is lost); filling away from lying to with the wind still
  strong the close-reefed topsails are set to go through the water; a lugger lies to under
  her own storm canvas, the storm lug (the taille-vent) and the storm jib, hove to when it
  is set (the Éclair in a gale, never aback). The band under the reefs, a good full by
  compass a point free of the helm's full and by, was tried and withdrawn (aback every two
  minutes and a half in the trials); the helm's own band is kept. The station gale lies
  a-try four hours under the book never aback (truth 7b-129) and still takes the ground
  among the Molène islands later in the day, at 41415 (44332 before), aback five minutes
  in the day (seven); the lee-shore trial keeps her off Ushant, never aground, the day
  falling otherwise from her second lying-to. Both trials are expected failures with their
  new figures beside the old, for the lead (the tuning notes, "Package 58b").
- **58 (Opus): the captain's sea sense, third pass**, from the owner's runs of gate 6c
  (`docs/dev/M6-WorkPackages.md`, "The notes of 2026-10-17, read"): the offing by the
  account not its doubt, the guard against land ahead within the visibility, the book
  taking a bearing when the doubt is wide, the headsail shifted, the trim's cadence, the
  merchant book's track into Bertheaume's road, all sail in a chase, the station's regain
  against the wearing order, the lay line and the sea-route mark, Roscoff's and St Mary's
  tracks. Beside 53 and 54.
  **And the sample's deltas** (the owner's observation of 2026-10-17 after the Éclair's
  cruise: a model acts on a snapshot while a human watches the change, and the delta,
  with time folded in, is what it cannot intuit): the head of every station's sample says
  what changed since its last turn as rates over the time elapsed ("since your last turn,
  twenty-three minutes: the land has closed from three miles to nine cables; the wind has
  backed two points; the water has shoaled from thirteen fathoms to eight"); an "at this
  rate" reading, `ahead`, of what she meets on this course and speed with the stream
  allowed within the hour and when (the rules captain's time-to-danger as words for every
  station: "the Triagons abeam in forty minutes at two miles; the land under Cézembre
  close aboard in an hour and a quarter"); and the cost of thinking, the ship's time the
  station's last turn took, said in the sample so that a slow door stands by for shorter
  intervals. The parity test lists `ahead` for every station.
- **59 (Opus): the harbour, the scenario maker and the settings** (§21d to §21f), beside
  53 and 54: a page of the game's own server, so built and tested here headless and proved
  by the owner on Windows; the Windows-only pieces (the desktop client's configuration path,
  the settings' place, a shortcut) small and tested by path, with a local session on the
  owner's machine kept as the fallback if the browser's opening or the shortcut want it.
- **60 (Opus): a ship bought** (§21g) after 51 and 53: listings by the port's business and
  by the director's ship order, the hull's valuation, the ship bought and sold through the
  market orders, the transfer of the people and the hands, the errand ashore; the goal's
  scenario for the gate.
- **62 (Opus): the director's hand** (§3), beside 59: an order of a ship's own grammar
  given to her captain's station by the director as his own, at far detail and crewed, refused
  where a model or the player holds him; the director seated in a ship as its second item
  when wanted. A day's package in the channel and the far orders.
- **61 (Fable, provisional): the land-avoiding route** (§21i) beside 51 and before 58's
  tracks: the route over the chart's own data for every captain and the player, the legs
  said as the plan, the pilot's joining leg from the same path; planned in full at briefing.
- **63 (Opus): the boat** (§21k), after 51: towing by the boat by an oar force on the hull,
  the boat as a vessel the player can pull or sail with the seat on another vessel, the
  kedge's false denial mended; kedging itself needs no package (the pull exists).
- **55 (Opus): the solo director and the gate's scenarios** after 51, 52, 56, 57, 58, 59, 60, 61 and 63: the starter
  briefs, the local-model director's run, the directed regatta course, the consent
  revision drafted for the owner (§22), the gate document.

Gate 7b after 55, carrying gate 6c's untested items (decision 50).

## 25. What this milestone does not do

Powder, damage and the prize (M7); the ends of the needs and the surgeon (M7's health); the
gybe as an evolution and the sails at fine control (M7); signals and the hail between ships
(M7); two directors competing; the supply-and-demand
loop; the orders system's review (deferred to a cold review).

## 26. Open items carried in

**The chart's drawn coast at the harbours** (the owner's finding on the Éclair's first
cruise, 2026-10-17; the lead's measurement): the coast the chart draws and the lookout's
nearest land come from the region's level-2 contour of the EMODnet grid (cells of about
115 m), while the grounding test reads the finest tile under the keel, the harbour patch
where one exists (Roscoff has one, its shoalest sounding 6.6 m above the datum). At the
eastern narrows of the channel of Bas the drawn coast's gap is 92 m, half a cable, though
the depth cells along the track held six fathoms: the ship sailed through a channel the
chart draws as all but closed, with "the land a cable" at every reading. For 61's
preparation or a chart item of its own: draw the coast and read the nearest land from the
finest level where a harbour patch exists, or from the Histolitt shoreline for the French
harbours, so that the picture, the lookout and the keel agree; and the owner to try the
passage himself first, since the lead's run is one data point.
**The owner's check of 2026-10-18** (`docs/playtests/2026-10-18-owner-chart-checks/`): the
same at Santoña (the road drawn inside a closed polygon) and Passages (the inlet drawn as
detached fragments, the contour cut at the patch's edge); with the channel of Bas, the
Goulet and Carrick Road, the test cases of the fix.

From M6: the Goulet on a flood (43b), Torbay's stream (43b), the held gauges' blend, the
deep-sea tiles' rule, the land-avoiding route (brought in as 61, §21i), the test battery's cost (eaten by the owner's
word), the orders review (deferred).
