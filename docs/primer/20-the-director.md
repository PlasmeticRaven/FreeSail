# 20. The director

Every station before this one is a person aboard a ship: the officer of the watch, the captain, the master, the lookout, a passenger, a captain of another ship. This chapter gives the game a station that is on no ship at all: **the director**, who sits above the game, sees the world as it is, and shapes the voyage you sail through the world the ship is in. A language model may hold it through any door; you may hold it yourself at the console or in the browser; and whoever holds it, you read what it did and why only when you ask, so that a voyage becomes two stories: the one you lived and the one that was arranged. Everything here is spec M7b §2 to §6 as package 50 built them, and §8 and §9 as package 52 gave the director a voice (people made from words, words in the mouths of those nobody holds), on the proposal's §7.6 and the owner's rulings of October (decisions 39, 43, 46 and 50; the end of the chapter says which).

## What the director is, and the one rule

The director's station is bound on the world and to nobody of the ship's company: it exists when a brief is given for it (a scenario's `director: {brief: ...}`, or `director: brief ...` at the prompt), or when you sit at it yourself (`--seat director`), and a world with neither is exactly as it was. It is not among the ship's stations: `the stations` does not list it, and no station aboard is told it is there.

**The one rule** is the proposal's: the director acts only through plausible causes. It cannot move your ship, change a sail or countermand an order; every order of the ship's is refused at its station, the deck's conversation included, since it has no place aboard to speak from. It changes the world the ship is in, and only in ways the simulation could have produced on its own: a sail that comes up over the horizon, a low that deepens where the season allows, a letter a port could have sent, a spar the carpenter finds sprung after a night of carrying sail. Every act of the director is something that could have happened anyway, so the physics stays honest and your agency stays whole.

```orders frigate plain-sail
the people
# rejected: weather: low "the low" radius 450 km at 1805-06-13T04:00 -300 500 990
# rejected: ship: a brig-sloop "Harpy" of France at the Iroise, running home to Brest
# rejected: aboard: the fore topmast is found sprung
```

The three refusals are the captain's grammar's, as chapter 15 had them: a world order is the scenario's, the director's and the owner's, never the captain's. At the director's station the same lines are the director's hand.

## The world orders: examples, not a rule

The director's tool is the world-order channel (chapter 15 and `docs/agents/Harness.md` §17), with what the director needed added. The forms the game performs today are:

- **the weather**: `weather: low "the low" radius 450 km fronts 140 300 at <time> <x_km> <y_km> <hPa>` appends a system, `weather: waypoint for "the low" at <time> <x_km> <y_km> <hPa>` moves one along its track;
- **a ship put on the sea, or a mind changed**: `ship: a merchant brig "Nancy" of Britain at 49 00 N 6 20 W, bound for Falmouth, intent: bound for Falmouth`, `ship "Nancy": intent run home to Falmouth`;
- **a thing found aboard** (new in this package, from the table `data/director/aboard.yaml`): `aboard: the fore topmast is found sprung` (the spar's condition cut to thirty, so that it carries away the sooner under a press of sail; the carpenter's report in your log), `aboard: a cask found stove` (a ton of water from the stores; the cooper's report), `aboard: a seam found working` (the carpenter's report; nothing of the hull is modelled yet, and the table says so), `aboard: the water found foul` (the purser's page says it; the needs of a later package read it);
- **a letter**: `message: at Brest from the agent: "..."` left at the port for the pilot to bring, `message: by a cutter from Plymouth from the port admiral: "..."` sent out to find her;
- **a port's stance or a price**: `port brest: closed to Britain`, `port falmouth: price of tin 130`;
- **a point of interest**: `mark: a wreck, her masts showing above the water at 49 58 N 5 16 W`;
- **a person named**: `person: supercargo "Mr Pentreath" aboard in the cabin`, `person: agent "Mr Fox" ashore at Brest`;
- **a person made from words, moved, or bound to a station** (package 52): `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth, who knew the captain's father`, `person: "Mr Fox" comes aboard as master`, `person: "Mr Fox" goes ashore`, `person: "Mr Fox" leaves the ship at Brest`;
- **words in the mouth of a person nobody holds** (package 52): `say as the cook: "Pease and pork, sir."`, `say as Mr Fox: "I knew your father, sir."`;
- **a model seated as the captain of another ship**, under your grant: `seat: <the model's exact name> as captain of <ship> for 20 samples`, `unseat: <ship>`.

These are given to the director **as examples of reasonable orders, never as the list of what is allowed** (the owner's word of 2026-10-17). Within each domain, and in domains the examples do not name at all, the director is told to attempt whatever it thinks reasonable: `news: war declared between Britain and Denmark`, `aboard: the cook reports the beef cask found rotten`, `say as the harbourmaster of Falmouth: "The packet is in."` (a stranger nobody has made yet). The game answers such an order honestly, never as "not allowed": *The game has no way to do this as said: ... Say it another way, or enter it again with a `[reason: ...]` and it will be logged as attempted.* Entered again with the reason, it is written in the director's log as an attempted act the game could not perform, with the words, so that the record says what is good, bad, useful or useless, and what the game should learn to do next. The tables (the things found aboard, the forms of the weather, the kinds of ship and intent) are what the game can do, not what the director may say.

## Doubted, not refused

The channel keeps the one rule with the director, and it does so by the owner's rule of decision 50: **a doubtful order is doubted, not refused.** An order the simulation could not have produced on its own from where it is gets the reason the act is doubted and the owner's words, *if you think the action you requested is still reasonable, you may enter it again along with a `[reason: ...]`, and it will be logged and performed.* Entered again so, it is performed, and the director's log keeps the act, the doubt and the reason together, which is the data by which the sets of reasonable acts are refined. What the channel doubts, by channel:

| Order | Doubted when |
|---|---|
| `ship: ...` a new sail | she is put inside the lookout's horizon in clear daylight (she would have been seen coming up over it), or on the land by the chart |
| `mark: ...` | the mark is inside the horizon in clear daylight (it would have been in sight already) |
| `weather: low ...` | the low is deeper than the season's floor for these waters (the climatology's table for the month and the box), or a deep low is put within three hundred kilometres out of a steady glass |
| `weather: waypoint ...` | the waypoint moves the system faster than the season's lows move, or deepens a low below the floor |
| `message: by a cutter from <port> ...` | the ship is beyond sixty miles of the port, which could not know where to find her |
| `port <id>: price of ...` | the price moves by more than three parts in ten in a word |
| `aboard: ...` | the thing has no cause in the ship's state: a spar found sprung with no strain on it and no fresh wind in the last watch, a cask stove or a seam working on a smooth sea, the water foul within five days of the voyage's start |
| `person: "<name>" comes aboard ...`, `goes ashore`, `leaves the ship at <port>` | no boat could carry him: she is more than six miles from his port, the nearest, or the one named |

A mind changed (`ship "X": intent ...`), a letter left at a port, a port closed or opened, a person named or made from words, a word said as someone, and the seat under your grant are never doubted. Your own live order (`world: ...` at the prompt) is never doubted either: it is the owner's word.

## The director's voice: people made from words, and words in their mouths

Since package 52 the director may make the people its story needs and speak for those nobody holds (spec M7b §8, §9).

**A person from words** stays in the world: `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth, who knew the captain's father` gives him who he is, his age, where he is and a line of history, in any order after his name, and his outline says it in one sentence (*Mr Fox, Guernsey pilot, sixty years of age, who knew the captain's father.*). He is among the people from then on (`the people`, `where is Mr Fox`). `person: "Mr Fox" comes aboard as master` brings him aboard (a line of your log: *Mr Fox came aboard from Falmouth.*) and binds the master's station to him, so that a model seated at the master's is in his place and reads his outline; `goes ashore` and `leaves the ship at <port>` put him ashore, his station going back to the ship's own master or unbound. A move no boat could make is doubted, and done with a reason. You may give the same orders as the owner (`world: person: make ...`) to set a scenario's people; they are saved and replayed with the game.

**Words in a mouth**: `say as the cook: "Pease and pork, sir."` is a line of your log in his name where he is (*Mr Squire, the cook, in the galley: Pease and pork, sir.*), heard by the stations within earshot (the quarterdeck, the deck and the galley hear one another; below, each place alone) and written in his own journal, which a model bound to him later reads back; never the order. A man of the ship's company by his trade, the cook or the cooper, is found when he is first spoken for; a person ashore is heard only while she lies within a boat's reach of his port; a stranger is made first.

**The rule of reach**: the director speaks as anyone no model or player holds, and never as a held station, whose words are its holder's own; and so it moves nobody held and binds nobody to a held station. Your captain is yours while you are at the prompt, and the officer is the model's while one holds his station: `say as the captain: ...` is refused outright, in the director's log, the result naming the stations held (*the stations held now: the officer of the watch (Mr Pearce, a model); the captain (Captain Bowen, the player at the prompt)*). It is the one refusal beside your brief's limits.

**Questions to people nobody holds.** While a director is seated, `ask the cook what is for dinner` (yours, or a station's) is said where it is said and put to the director in its next sample, with until when it waits: it may answer in the cook's words with `say as`, which costs none of its day's acts, and the answer goes back to the station that asked, waking it; unanswered within a glass, the station is told so. A word (`tell the boatswain ...`) goes to it the same, and wants no answer. With no director seated, such a question is refused as it always was; the masthead and the master's reckoning answer by their rules whoever is above.

```orders frigate plain-sail
# rejected: say as the cook: "Pease and pork, sir."
# rejected: person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth
```

At your prompt both are world orders, refused as chapter 15 has them; at the director's seat, or after `world:`, they are the director's and the owner's.

## The brief and its limits

You write the director's brief: the tone of the voyage, the challenge wanted, the limits set, the period's bounds the director must keep. It is a file beside the scenario or given at the prompt:

```yaml
# data/director/briefs/quiet-passage.yaml, the gate's
name: A quiet passage
tone: >
  A quiet passage in fair weather, with the texture of a real sea ...
challenge: >
  Interest, not danger. One notable thing a watch at most ...
limits:
  wind_max_kn: 27          # no gale: nothing above force 6 by any system appended or moved
  enemy_heaviest: cutter   # no enemy heavier than a cutter put on the sea
  nobody_dies: true
  the_war_as_it_is: true
  the_chart_as_it_is: true
cadence: glass
budget: {samples_a_day: 48, acts_a_day: 4}
```

Four starters are under `data/director/briefs/`: `quiet-passage` (the gate's), `interesting-passage`, `hard-cruise` and `chase`. A scenario names one, a file or the mapping itself (`director: {brief: quiet-passage}`); at the prompt `director: brief quiet-passage` gives a starter, `director: brief a quiet passage with a chase on the second day` gives your own words with no limits beyond the channel's doubt, and `director: brief` alone reads the brief as it stands. **The limits are the channel's to enforce, never the model's to remember**: a `weather:` order whose system would blow above the brief's knots at its tightest is refused with the reason, an enemy heavier than the brief allows is refused, a thing found aboard that would kill is refused where nobody dies, a port closed to or opened to your own nation is refused where the war is as it is. These are the only refusals the director meets; everything else is doubted or attempted. The brief's words, limits and budget are the last part of the station brief the model reads, after the fixed part every director reads.

## The clock and the budget

The director samples on the notable and urgent lines and on a slow clock: every glass by the brief's default, every watch where the brief says `cadence: watch`, under the pace rule like every station (chapter 19), so your clock slows to 1x while its sample is open and runs at your compression when it stands by. A director that stands by for a watch lets you run at three hundred times. Its budget is the brief's, in **samples a day and acts a day** of the ship's time (an act is a world order performed; a doubt, a refusal and an attempt cost none): spent, either count holds the director until the next day of the ship's calendar, the log says so, and the sample that renews the day says the budget is renewed. The owner's compression is untouched.

## The log, hidden and revealed

Every act of the director goes to the **director's log** with its tick and its reason: an order given, one doubted, one entered again with its reason, one refused by the brief, one the game had no way to perform and one attempted all the same, the budget spent and renewed, the brief given, and every thought the director writes (its journal, and whatever it says in a reply, which is never a line of your log). It is the station's own journal, kept in the save with the stations' acts and replayed as a station's notes are, and it is **hidden in play from every station and from you**: nothing of the director reaches the play log, a station's sample, its `read_log`, its `state` or the `stations` reading (a director you can see coming is not a director); the play log carries only the effects of its acts as they are met (the sail sighted, the glass falling, the carpenter's report), as it carries the effects of your own `world:` orders since decision 46.

You may ask for it at any time, by name:

```
the director's log
```

at the console or in the browser's order box. The log is printed (in the browser, in a pane of its own beside the play log, shut until you ask), the asking is written in the record as a driver's line, and **the director is told in its next sample that you asked**. `two stories [N]` prints the last lines of the play log with the director's log inline, each of its entries marked `D`: the replay view, which reads a saved voyage as two stories. `show the director's journal`, `ask the director` and `tell the director` are refused in words: the director is above the game, and the log is read by name.

## Holding the station yourself

`--seat director` at the console or the browser seats you at the director's station, above your own ship:

```
py -m freesail.ui.console --scenario data/scenarios/merchant-intent.yaml --seat director
```

A bare world order typed there is the director's, through the channel's door: doubted with its reason, entered again with a `[reason: ...]`, refused by the brief's limits if one is given, and written in the director's log under your name; `the truth` reads the world as the director sees it (every ship's true position, heading and sail, the weather as it is and as the systems will make it for the next watch, the tide, the people aboard every crewed ship, the markets and the news); an order of the ship's is refused. Your own `world:` order is still yours as the owner, undoubted and unlogged in the director's log. A model at the station reads the same truth through its `truth` tool and gives its orders with `world_order`; `docs/agents/Harness.md` §19 says how to seat one through each door.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `director: brief quiet-passage` | `director: brief <file>`, `director: brief <your words>`, `director: brief` | the director's brief given at the prompt (a starter, a file, or words), the station bound; alone, the brief as it stands |
| `the director's log` | at the console and in the browser | the director's log revealed: every act with its reason; the director told you asked |
| `two stories 40` | `two stories` | the last lines of the play log with the director's log inline, each of its entries marked `D` |
| `--seat director` | at the console and the browser | you at the director's station; a bare world order there is the director's |
| `the truth` | at the director's seat | the world as it is: every ship, the weather now and in a watch, the tide, the people, the markets, the news |
| `--station director` | at the MCP bridge, the local runner and the API door | a model at the director's station, when the game has a brief for one |
| `chart(span)` | at a door that carries pictures | the player's chart as the browser draws it, his ship by her account and no other ship: for planning, not the truth; there is no `ship_view` above the game |
| `world_order(text)` | the station's tool | a world order through the brief's limits and the channel's doubt, logged in the director's log |
| `<order> [reason: ...]` | | an order doubted, entered again with its reason and performed; one the game cannot perform, logged as attempted |
| `aboard: the fore topmast is found sprung` | `aboard: a cask found stove`, `aboard: a seam found working`, `aboard: the water found foul` | a thing found aboard, from the table, the people's report in the play log |
| `person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Falmouth` | `..., aboard in the cabin`, `..., aged forty-five`, `..., who knew the captain's father` | a person made from words, with his outline, among the people from then on |
| `person: "Mr Fox" comes aboard as master` | `person: "Mr Fox" goes ashore`, `person: "Mr Fox" leaves the ship at Brest` | a person moved, a station bound to him or given back; doubted beyond a boat's reach |
| `say as the cook: "Pease and pork, sir."` | `say as Mr Fox: ...`, `say as the carpenter: ...` | words in the mouth of a person nobody holds, heard within earshot, in his journal; refused for a held station |
| `ask the cook what is for dinner` | `tell the boatswain <words>`, with a director seated | a question to a person nobody holds, put to the director; its answer as him back to the asker, or after a glass the asker told none came |
| `director: {brief: quiet-passage}` | in a scenario file, beside `models`, `seats`, `seats_in_voyage` | the brief given by the scenario, the station bound when the game is made |

## Where it comes from

The proposal's §7.6 (the director as an agent on a different channel, acting only through plausible causes, its actions visible after the fact, sampling on events and a slow clock, with a brief as the guardrail); decision 39 (the lead's first play is at the director's station), decision 43 (stations are data bound at run time, so that a station on no ship is a binding like any), decision 46 (a world order is never shown as sent) and decision 50 (the director brought forward; a world order doubted, not refused; the brief's hard limits refusals), with the owner's refinement of 2026-10-17 that the forms and the tables are examples and not a rule. The sources of the things found aboard are in the table itself (Falconer 1780, SPRUNG; the Regulations and Instructions of 1806, the Purser). The design is spec M7b §2 to §6, and §8, §9 and §15 for the voice; the packages are 50 and 52 in `docs/dev/M7b-WorkPackages.md`, and their days' figures are in `docs/dev/TuningNotes.md` under each.
