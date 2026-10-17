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

### 5. Sampling, the budget and the clock (`harness.py`; `core/world.py`)

The director samples on notable events and on the slow clock (every glass by default,
every watch by the brief), under the pace rule of M6 §12 as every station does (the clock
to 1x while its sample is open), and lockstep as an option. **The budget**: the brief gives
it in samples per day of the ship's time and in acts per day (so that it cannot make every
day a hurricane); spent, it stands by until the next day; said in its log. The owner's
compression is untouched: a director that stands by for a watch lets the player run at
300x.

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

## Part 7b-ii: The director's voice

### 8. People made from words (`freesail/world/people.py`; `orders.py` `person:`)

`person: make "Mr Fox", a Guernsey pilot of sixty, ...` makes a person with an outline from
the words (a name, a role or none, an age, a place, a line of history), who persists in the
world's people, may be bound to a station of a ship (`person: "Mr Fox" comes aboard as
master`, M6 §11's outline), may be ashore at a port, and is saved and replayed. `person:
"Mr Fox" goes ashore`, `... leaves the ship at <port>`. The director's chief tool for the
story; the player's too, at the console, for scenarios.

### 9. Speaking as the world (`orders.py` `say as`; `harness.py`)

`say as <person>: <words>` puts words in a person's mouth: a person of the ship's company
nobody holds (the carpenter, the cook), a person ashore (the harbourmaster, a merchant, a
tavern's talk), a person made in §8, the pilot; heard where the person is (§13) and
journaled as his; and answering what a station asked of an unseated person. **The rule of
reach**: the director speaks as anyone no model or player holds, never as a held station,
whose words are its own. `ask the <role>` and `tell the <role>` to an unseated person wait a
sample for the director when one is seated (the rules answer as now when none is), with a
bound (the asker's stand-by wakes at the answer or after a glass).

### 10. Truths for 7b-ii

- 95. A person made from words is on the muster of the ship he joins, holds the station
  he is bound to, and is there after a save and a replay.
- 96. A question to the cook, with a director seated, is answered in the cook's words at
  the galley and heard by those within earshot; with none, by the rules as before.
- 97. `say as` a held station is refused.

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
- **55 (Opus): the solo director and the gate's scenarios** after 51, 52, 56, 57, 58, 59 and 60: the starter
  briefs, the local-model director's run, the directed regatta course, the consent
  revision drafted for the owner (§22), the gate document.

Gate 7b after 55, carrying gate 6c's untested items (decision 50).

## 25. What this milestone does not do

Powder, damage and the prize (M7); the ends of the needs and the surgeon (M7's health); the
gybe as an evolution and the sails at fine control (M7); signals and the hail between ships
(M7); two directors competing; a land-avoiding route for the planner; the supply-and-demand
loop; the orders system's review (deferred to a cold review).

## 26. Open items carried in

From M6: the Goulet on a flood (43b), Torbay's stream (43b), the held gauges' blend, the
deep-sea tiles' rule, the land-avoiding route, the test battery's cost (eaten by the owner's
word), the orders review (deferred).
