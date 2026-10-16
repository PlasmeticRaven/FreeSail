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
- **7b-iv. People in places:** movement between places aboard and ashore, the player on the
  shore; what is heard where; books drafted; the papers kept in a place; the equal reach
  between stationed persons.
- **7b-v. Needs:** provisions and water consumed, hunger, thirst and fatigue in a few steps
  with the master's cautions, "stand by, asleep below until called", the hooks for M7's
  health.

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
report), never the order. An order that would not be a plausible cause is refused with the
reason, and the refusal goes to the director's log, not the play log.

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

### 13. Truths for 7b-iii

- 98. A world with no player's ship runs a day at seed 7 with the business on and a
  director observing; followed ships change the centre; the pace truth holds.
- 99. The player at the captain's station of the Palinure sails her through the station
  trial; the save replays with his acts.

## Part 7b-iv: People in places

### 14. Places and movement (`freesail/world/people.py`, `places.py` new; `data/people/*.yaml`; `data/ports/*.yaml`)

The ship's places as M6 §2 named them (the quarterdeck, the deck, the tops, the cabin,
the wardroom, below, the galley, the hold) become somewhere a person is and may go: `go to
the cabin`, `go below`, `go on deck`, `go ashore` (by the boat, at a port's reach), `come
aboard`; a person's place in his state and the muster; the player's place as a person's
(the player is on the quarterdeck by default, may be in the cabin or ashore, and acts where
he is: the market only ashore or by the boat, the helm only on deck). A port's places
ashore (the quay, the market, the counting house, the tavern, the pilots' office), each with
what can be done there and who is found there (§8's people and the port's own).

### 15. What is heard where (`core/events.py`; `harness.py`)

A word said in a place is heard in that place and the places that hear it (the quarterdeck
hears the deck, the cabin hears neither but the knock at the door); the log a station
reads carries what its person could hear and see from where he is for the routine and the
notable, and everything urgent (the ship's safety is everyone's); the player's own log the
same for his place, with the full log a reading apart (`the log` whole) so that nothing is
lost to him. A word heard counts as "a word on deck" for the stand-bys (the owner's note
15). **A step the owner called possibly too far; built behind one switch
(`scenario.hearing: by place | all`), `all` the default until the gate says otherwise.**

### 16. Books drafted, and the papers in their place (`freesail/agents/tools.py`; `data/papers/`)

`draft a book "night orders": ...` writes a standing-orders sheet, a note for the ship's
papers or a manifest to buy and sell several goods at once, as a book in the library with
the person's mark, the record for the immersion and the use functional (the sheet becomes
the standing orders when posted, the manifest the trade when given to the boat); the
papers and the books kept in their place aboard (the cabin's desk, the master's chest, the
purser's slops) so that reading one means being where it is or sending for it, behind the
same switch as §15.

### 17. The equal reach (`tools.py`; `stations.py`)

Every stationed person has the same basic reach: tell and ask any other person aboard or
within hail, go where his duty allows, read what is where he is, journal, stand by; the
domain orders are the station's authority as now. Several stations of one kind on a ship
(45c's groundwork): the frigate's lieutenants as officers under the first, each with his
place and watch.

### 18. Truths for 7b-iv

- 100. A person who goes below is in the muster below and hears the deck's routine no
  more with hearing by place; an urgent line reaches him; `go on deck` brings him back.
- 101. The player ashore buys at the market in person; aboard, by the boat; the papers
  read where they are.
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
cabin; a drafted manifest's trade; a week's needs; the regatta's course with a director
seated above it. The lead's first play is at the director's station, as decision 39 held.

## 24. Packages (outline; the allocation)

In waves, written for the owner's approval in turn, each launched on his word:

- **50 (Fable): the director proper** (§2 to §7): the station, the channel's guardrails
  and the brief's enforcement, the budget, the hidden log and its reveal, the replay view.
  First, and design-heavy throughout.
- **53 (Opus): people in places** (§14, §16, §17) beside 50: movement and places, the
  books drafted, the papers in their place, the equal reach and several of a kind; the
  journal keyed to the person is in. No dependence on 50.
- **54 (Opus): needs** (§19, §20) beside 50 and 53: the rations, the three needs, the
  sleep below. Data and rules on the people, no dependence on the director.
- **51 (Fable): the observed world** (§11, §12) after 50: the followed ship in place of the
  given one across the World, the player on another ship, the replay of a station there.
  Cross-cutting and design-heavy.
- **52 (Opus): the director's voice** (§8, §9) and **what is heard where** (§15) after 50
  and 53: people from words, `say as`, the asked unseated person answered by the director,
  the hearing by place behind its switch.
- **55 (Opus): the solo director and the gate's scenarios** after 51 and 52: the starter
  briefs, the local-model director's run, the directed regatta course, the consent
  revision drafted for the owner (§22), the gate document.

Gate 7b after 55.

## 25. What this milestone does not do

Powder, damage and the prize (M7); the ends of the needs and the surgeon (M7's health); the
gybe as an evolution and the sails at fine control (M7); signals and the hail between ships
(M7); two directors competing; a land-avoiding route for the planner; the supply-and-demand
loop; the orders system's review (deferred to a cold review).

## 26. Open items carried in

From M6: the Goulet on a flood (43b), Torbay's stream (43b), the held gauges' blend, the
deep-sea tiles' rule, the land-avoiding route, the test battery's cost (eaten by the owner's
word), the orders review (deferred).
