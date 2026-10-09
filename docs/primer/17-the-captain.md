# 17. The captain

Chapter 16 gave the ship an officer of the watch, who holds the deck from the captain's word and gives the orders of the watch within a stated domain. This chapter gives her a captain: first the one she always had and the game never named, the rules-based captain who sails her when nobody is seated, and then the captain's station, where a language model (or, one day, you) commands her with the player's whole surface. It also says who the people of the wardroom are, since a station is held by one of them, and what the owner keeps whatever station he holds. Everything here is spec M6 §2 to §4 and §7 as package 40 built them, and the practice of 1805 as the sources have it (the end of the chapter says which).

## The ship's company, by name

Chapter 14 named the few people the story needed: the master, the mate, the pilot, the purser. Each ship now has her wardroom as data (`data/people/<ship>.yaml`): on the frigate the captain, the three lieutenants, the master and his mates, the boatswain, the gunner, the carpenter, the purser and the surgeon; on the schooner, the cutter and the brig in trade the master, who is the captain, and the mate; on the brig-sloop the commander, a lieutenant and the master. Each is a person of the muster, his name drawn under the seed as before, with a rank, a place aboard at the start, a station where the file binds one, and an outline: a few traits, a line of history, and a brief for his station, in a sentence or two. `the people` lists them with their places and says who is in command; the outlines are read by the captain's station in its brief, and by you in the file:

```orders frigate plain-sail
the people
the captain
who commands
# rejected: stand down the captain
# rejected: resume the captain
# rejected: captain: trade tin from Falmouth to Brest
```

The last line is refused because it is a world order (chapter 15): the intent a ship sails by is the scenario's to give, in its file, and never the captain's own order to himself. The two before it are refused on a ship whose captain's station nobody holds.

**Stations are the people's.** The harness's stations bind to a person at seating, and the binding is the file's and not a name in the code: `station: first lieutenant` under the lieutenant's outline makes him the officer of the watch on the frigate, `station: mate` on the rest; `station: captain` under the captain's, the master's or the commander's makes him the captain's station's. A scenario may name any of them (`people: - {role: master, name: Mr Travers}`), and the name is his for the voyage. A station nobody holds is held by its person under the rules below: the frigate's captain, the schooner's master and part owner, sails her by his doctrine when no model and no player does.

## The rules-based captain

What the game does when nobody is seated is now a named thing: a captain in three layers, **intent, plan and behaviour**, written as a goal, a book and a few judgements (spec M6 §4; `freesail/world/captains.py`; the doctrines in `data/captains/<role>.yaml`).

**The intent** is the goal and its parameters, in words the scenario file gives: *trade tin from Falmouth to Brest*, *keep the station between Ushant and the Lizard*, *carry a letter to Plymouth*, *run home to Falmouth*. It is read against the chart and the ports, and refused in words if a place is not on the chart or a cargo is not a goods. A scenario with `intent:` and no `standing_orders:` is sailed by the captain alone; a scenario with a book and no intent is sailed by its book, as the merchant passage and the naval cruise always were, and the captain stands aside (truth 77: their logs do not move).

**The plan** is a sequence of legs worked from the intent at sea, never written in advance: a passage planner over the chart's own data (the ports' tracks to sea and in, the period's common tracks between the headlands, the offing a headland is given, the port's pilot water and its anchorage), each leg shaped with the player's own `shape a course for`, and the plan worked again on an event. A course the wind will not allow is beaten by a rule: stand on the tack that makes the most good, go about when the other tack makes better or the offing closes.

**Behaviour** is a state machine whose states are books in the dialect of chapter 11, loaded into the book of standing orders on entering the state and unloaded on leaving it, under the state's name: *in port*, *on passage*, *beating*, *hove to for weather*, *running for shelter*, *at anchor*, *investigating a stranger*, *chasing*, *evading*, *keeping station*, *in distress*, and *engaging* (present and empty until milestone 7). The book of a state is the doctrine's, role by role (the merchant, the King's ship, the packet, the commodore), with its thresholds as data; `show the standing orders` lists the loaded state's rules beside your own, each marked with its book's name, and yours stand through every change of state. A transition is an event the ship perceives: *under way*, *anchored in port*, *course not laid*, *course laid*, *gale*, *gale over*, *lee shore*, *thick near the land*, *hostile stranger*, *stranger lost*, *aground*, *afloat*. The few judgements a book cannot make by its own conditions, the captain makes in code with his figures in the tuning notes: buying the cargo and sailing on the tide that serves, the lee shore, the pilot taken, the anchor on a foul berth, the chase and the chase given up.

**Perception on the player's terms.** The captain reads what you read and nothing else: the readings, the lookout's sightings, the glass, the sky, the tide by the almanac, the people, the port. `tests/test_captains.py` proves it two ways: nothing in `captains.py` reaches the world's truth by any road, and two ships of one seed whose true places differ and whose accounts are one are judged alike. No captain knows where another ship is until his lookout could.

**The rule of the road as 1805 had it.** No regulations yet, but the custom: the ship close-hauled on the starboard tack stands on, the larboard-tack ship gives way, and a ship running keeps clear of one by the wind; a reflex at a few cables, said in the log as his order, and never for a pilot boat or a sail already spoken.

**One brain, two bodies.** The same state machine runs for a ship at far detail (chapter 15): her state resolves into her plan (hove to is no way; on passage is her legs), so that the crewed promotion of milestone 6c changes the body only.

Every doing of his is an order, given through the same grammar as yours, under the actor *captain's rule '<state>'* and logged as his (`By the captain, on passage: shaping a course for the Lizard (the leg for 49 52 N 5 06 W).`), and never journaled: his judgements are a function of the seed and the journal, as a standing order's firings are, and a save replays them. `the captain` reads his name, his intent, his state and the book he sails by.

## The captain's station

The captain's station is the third station and the first with the player's whole surface: every reading, every order at every level, the standing orders as his own book, the port's business, the people, the papers, and the deck to give and take. A model's door seats it with `--station captain` (`docs/agents/Harness.md`, section 14), after the consent question and the drill as for the officer. Its brief says the voyage first: the scenario's name, the intent or the book, the ship and her nation, the people aboard with their outlines, and the book as it stands. **No model is seated here yet**: the station is a kind of thing the consent brief does not describe, and by the owner's rule the question is put again, once, with a brief revised for it; the package drafted the revision and the owner approves it.

**The deck is his by right of the station.** There is no `you have the deck` for the captain: from the moment he is seated the log says `The captain's station has the deck (Mr Travers); the ship is commanded from it, by direct orders and by the book.`, and an order of his goes to the ship as yours does, logged as a captain's: `By the captain: shaping a course for the Lizard.` His standing orders are the book; where the scenario gives the rules-based captain an intent, the state's book is loaded under its name and shown to him as his night orders, to keep, belay or write over. He is refused by the grammar as you are, and never by a domain.

**When his door is silent, the deck passes to his book.** An hour of ship's time with no reply, and the harness tells him so and says, urgently, `The captain's door has given no reply for an hour and has been told so; the deck passes to his book; the rules-based captain's judgements stand in, until he gives an order again.` (on a scenario with a book and no intent: `the standing orders hold the deck`). The book sails her meanwhile, exactly as it does with nobody seated; his next order takes the deck back (`The captain's door answers again (an order given); he has the deck, and his book stands as his night orders.`). `hand_over(note)` at this station lends the deck to the book with his note and keeps him at the station. A paused captain's station (`The captain is paused (...); the deck is his book's.`) is the owner's to resume or stand down.

**The officer under him.** From the captain's station the officer of the watch is given the deck, allowed things by name or in general, told and asked, by the sentences of chapter 16 given through `submit_order`; the log says them as his (`By the captain: you have the deck.`). What the harness counts at this station is what it counts at the officer's, by the officer's numbers (chapter 16), since the orders are the same kind of thing. The three ways of stopping are the officer's: the deck lent and he stays; `stand_down` or the owner's `stand down the captain`, with the game saved and the station open to be taken again, the rules holding her meanwhile; the token or `opt_out`.

## The owner, and the player's seat

**You are the owner at the door, whatever station you hold or none** (the owner's ruling of 9 October 2026). The stop, the consent question and the drill, `you may` and `stand down` for any station, the save and the clock are yours; your words reach a station as the owner's and never as another station's; and where things have gone wrong past remedy, the responsibility is yours. The captain's station, whoever holds it, gives `you may` to the officer as you do, and your word stands over all.

Beside that, you and a model are at parity for the roles on ships: **you may take a station below the captain's yourself**, under a model captain or under the rules. The console and the browser seat you at the officer of the watch's station with `--seat officer`, and the log says `The player takes the officer of the watch's station (...); his orders are judged by the station's authority and the captain's word, and the deck is the captain's until he gives it.` From then an order you type is judged exactly as a model's at that station would be: refused without the deck, refused outside the officer's domain unless the captain's word allows it (chapter 16), given under the station's actor and journaled when it passes (`Order: set the royals.` by *the officer of the watch (the player)*). The stations' sentences you type stay yours (`you have the deck`, `you may wear ship`, `I have the deck`, `stand down the officer`), and a model captain gives them to you the same way; `tell the officer ...` reaches you as his word in the log, and `ask the officer ...` as a question you answer with `answer <words>`. This book is your brief. A save made with you seated replays with you seated again.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `the captain` | `who commands` | who holds the captain's station and through which door, whose the deck is, the book he sails by; or the rules-based captain, his intent and his state |
| `the people` | | the ship's company with their ranks and places; who is in command |
| `stand down the captain` | | the owner's: the station stood down, with a save, the rules holding her; to be taken again |
| `resume the captain` | | the owner's answer to a pause; the deck is his again |
| `show the standing orders` | `the standing orders`, `list the standing orders` | the book of standing orders, a state's rules marked with the book's name beside your own |
| `intent: trade tin from Falmouth to Brest` | in the scenario file | the rules-based captain's intent; `captain: <intent>` is a world order, the scenario's and the director's |
| `--station captain` | at every door | a model at the captain's station (`docs/agents/Harness.md` §14) |
| `--seat officer` | at the console and the browser | the player at the officer of the watch's station, under that station's authority |
| `answer <words>` | at the player's seat | the answer to a question put to the seat |

## Where it comes from

The Regulations and Instructions of 1806 (the 1808 printing in `docs/references/admiralty/`), the Captain: that he commands the ship and answers for her, that the lieutenant who commands the watch "is never to change the ship's course without the captain's directions, unless to avoid an immediate danger" (chapter 16's rule, seen from the other side). Falconer 1780, CAPTAIN and MASTER, for the merchant master who is both. For the rule of the road, the custom before any regulation: the starboard-tack ship's right of way is in the earliest rules of the road (the Trinity House rules of 1840 wrote down what the practice had been), and a ship running keeping clear of one by the wind is of the same custom. For the passage planner, the common tracks of the Channel are the ports' and the features' files, from the sailing directions the chapters 10 to 15 cite. The design is spec M6 §2 to §4 and §7, the owner's principles of 9 October 2026 (decision 40: a rules-based captain functional without being pre-planned, never a fixed route that relies on a weather) and his ruling of the same day on the owner's place and the player's seat (decision 39, ruling 1); the package is 40 in `docs/dev/M6-WorkPackages.md`, and the figures of the doctrines are in `docs/dev/TuningNotes.md` under it.
