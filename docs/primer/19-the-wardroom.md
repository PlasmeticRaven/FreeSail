# 19. The wardroom

Chapter 16 gave the ship an officer of the watch and chapter 17 a captain; this chapter gives her the rest of the wardroom that a model or you may hold: the master's station, the lookout's, and a passenger's, and the three things that make several stations one ship's company: that they speak to one another, that the deck's word flows down the ranks, and that the clock keeps a pace all of them can live at. Everything here is spec M6 §11 and §12 as package 41 built them, and the practice of 1805 as the sources have it (the end of the chapter says which). Since package 41 the stations themselves are data on the ship, bound to her people at run time and never a table in the code: the wardroom file's `stations:` is only where the binding begins.

## The stations are the ship's, bound to her people

A station is a post a model or you may hold through a door: the watcher's, the officer of the watch's, the captain's, the master's, the lookout's, a passenger's. Which of them a ship has, and which of her people holds each, is a binding on the world (`the stations` at the prompt lists it): on the frigate the master's station is her master's, on the schooner and the cutter the mate's (who is the officer of the watch's too; a small vessel carries no master beside the man who commands her), on the brig-sloop her master's; the lookout's is a hand at the masthead with no name, and a passenger's is nobody's until somebody comes aboard. A station bound is one a door may ask for (`--station master`, `--station lookout`, `--station passenger`); a station the ship has not got is refused in words, with the stations aboard named. The binding moves by two operations the harness has and a world order will drive later (the director's `person: "Mr Fox" comes aboard as master`, in milestone 7b): a station bound to a person of the company, whose outline (his rank, his station aboard, his history) then builds the brief a model at it is given; and a station unbound, which releases a model holding it with a line saying why, as `stand down the master` does, and is refused to a door afterwards.

```orders frigate plain-sail
the stations
tell the master we shall want the reckoning worked at the fix
# rejected: ask the lookout what sail is in sight
```

(The word to the master is kept in his station's journal for whoever takes it, as chapter 16 has it; the question to the lookout is refused because nobody holds that station in this book's ship: a question wants somebody to answer it.)

## The master's station

The master is the ship's navigator (Falconer 1780, MASTER: "the officer entrusted with the navigation of the ship ... to keep the reckoning"); a model at his station works the reckoning when the ship's own master would: at noon, at a fix by cross bearings, and at the captain's word (`work up the reckoning`). At each of those he is sampled with the master's slate in his sample's notice (chapter 10: where the slate begins, each board as the master laid it down with the tide he allowed, each sight worked in, and the noon's observation as the ship took it), works it by the traverse and gives his figure with `my reckoning is <position>`. A figure given within half an hour of the working, the time the ship's own master is below at the day's work (`MASTER_WORKING_S`), **is the ship's account**, and the log says it was his: *The master's figure is the ship's account: 49° 50' N, 5° 17' W as of 12:00 for the noon, 0.3 miles W of the ship's master's ...; worked at the master's station by Mr Harvey (...), and the account runs on from it.* None within that time, and the ship's own master's figure stands, said in the log (*No figure came from the master's station for the noon (none came within 30 minutes); the ship's master's account stands*). A figure given at any other time is his own reckoning, kept beside the master's and said at noon, as an officer's is (chapter 16). This is G19's third step, and the fake master proves it both ways.

His domain is the reckoning, the sights, the lead and the chart's queries (the log hove, the lead cast, the observations, the chronometer, a bearing, a fix, the depth by the chart, the dangers), and he gives no order of the deck: not the sails, the helm, the course, a manoeuvre, the anchor, the hands, the port or the book. The course shaped and the reckoning set by hand stay the captain's, whom he advises. **There is no deck at his station**: nothing gives or takes one, and an order of his is judged by his domain alone. A named thing may be allowed him by you or by the captain's station, said with his station or his name before the comma, and taken back the same way:

```orders frigate plain-sail
# rejected: master, you may heave to
# rejected: master, you may work the ship
```

(Both are refused in this book's ship because nobody holds the master's station; with a model or you at it the first stands and the second is still refused, since the general authority to work the ship is the deck's, and he has none. A grant of a thing that is his already, `master, you may heave the lead`, is refused as allowing nothing, as the officer's is.) `the master` reads the ship's master's place and, when the station is held, who holds it and the working open for him.

## The lookout's station

The lookout is at the masthead, for a small model (spec M5 open item 6): he sees what the masthead sees (the sample's log carries each sighting as the game makes it, and `what is in sight`, `the nearest land` and `the lookout` say what is in sight now), puts it into a lookout's words and **hails the deck**: `hail sail ho, two points on the larboard bow` (or any words said at his station) is a line in the log from the masthead, notable, heard by whoever is on deck, and it wakes an officer with the deck who stands by, as a line that speaks of danger does. He has one order of the ship beside it, `make her out` (the glass is his), and gives no other: the deck is not his to order, only to warn. His cadence is the masthead's lines (a sighting, a sail made out, a sail lost, the land ahead, a bearing steady and closing), an urgent line and each glass, never the minute and never the quarterdeck's notable lines; so a say on the quarterdeck is not heard aloft (truth 84), and a model there is sampled a few times in a watch of empty sea. `the lookout` (or `who is at the masthead`) reads who holds the station, what is in sight and his last hail.

## A passenger

A passenger's station is a person aboard with no duty and no order: a model or you may be aboard to see the game, and a person brought aboard by the director later has a station to stand in before he is bound to another. He reads every reading and the library, keeps a journal, speaks (`say`), asks and tells, and leaves; every order of the ship's is refused in words (*a passenger gives no order of the ship*). The consent brief covers it in kind already (the watcher's authority or less), so no question is put again for it.

## The deck's conversation

A station addresses another by its station or by its person's name or role, and the words are a log line with a place aboard and a hearer, carried in the hearer's next sample under the speaker's name, never as the operator's:

```orders frigate plain-sail
say we shall have a blow before night
# rejected: hail sail ho
```

- `say <words>` is heard by whoever stands where the speaker does: the quarterdeck is the captain's, the officer's, the master's and a passenger's; the cabin the captain's when he has gone below; the masthead the lookout's. A `say` of yours at the prompt is the captain's, on the quarterdeck (the second line above is refused because a hail is the lookout's, from the masthead). What is heard rides the hearer's next sample as `heard`, with no sample forced and no answer owed; what is said is a log line everyone reads.
- `tell the master <words>` and `tell the first lieutenant to shorten sail` reach the station as the captain's `tell` does (chapter 16), under the speaker's name and place: *The captain (Mr Bowen), on the quarterdeck, to the officer of the watch: keep her full and by.* The leading *to* or *for* of the sentence is not part of the words.
- `ask the master for a course` puts the question to his station, answered on his next sample; the answer comes back to the asker as a word (*The master (Mr Harvey) answers your question (a course?): south by east, sir*), and when none comes within the asked station's patience the asker is told once, in his next sample. `ask the master <reading>` with nobody at the master's station is still the reading's own form (chapter 6): the ship's own master answers at once.
- The player at his seat speaks the same way: `say`, `tell` and `ask` typed at his seat are his station's; the owner's sentences (`you may`, `you have the deck`, `stand down`, `resume`) stay his.

## Who may give what

`you may` flows down the ranks and never up: you, the owner at the door, to any station; the captain's station to the officer's and the master's, by the same sentences (`master, you may wear ship` through `submit_order`); the officer and the master may give no station's sentence but the conversation's. A station's `stand_down` is its own; `stand down the <station>` is yours and the captain's.

**The rules-based captain over a seated officer.** On an intent scenario with nobody at the captain's station (chapter 17), a model or you at the officer's station is given the deck by the captain's own words at his judgement, his standing orders (the state's book) in force over it: *Mr Pearce, you have the deck. ... (Mr Travers, by his rule, on passage; his standing orders stand over it.)* He takes it back, saying so, for a judgement that needs the deck (the gale and the shelter, a stranger investigated, chased or evaded, distress), and gives it again when the state is a quiet one. The seat under him is yours with `--seat officer`, as before; `--seat master`, `--seat lookout` and `--seat passenger` seat you at the lesser stations, each with its own authority and no deck.

## The pace, and the cadence

The owner's testing setting is the default (decision 39, ruling 2): **the clock slows to 1x while any model's sample is open**, whoever holds it, at whatever station, and runs at the set compression again when every open sample has been answered or has stood by. It is not lockstep: the ship sails on at her own second while the model thinks, and a slow answer lands late; `--lockstep` holds the clock for a door with the floor and stays the separate option, and `--free-running` runs at the set compression with no slowing, for the solo player who wants a model to think while he sails at sixty times. The rule moves no tick of the world, only how many of them a real second brings, so a recorded passage replays to its digest under any of the three. `the pace` reads the set compression, the rule, and which samples are open and since when; the log says once when the clock has been held at 1x for a station longer than two real minutes (`driver.pace`), so that a slow door is seen and not suffered.

Each station's **cadence** is a setting of its seating, said in its brief: `--cadence glass` (every glass and on the notable and urgent events, the default), `--cadence watch`, or `--cadence events` (on events only), the station's own lines kept whatever it is; so a lookout on a small model is not sampled as often as the captain.

## The forms, in a table

| Form | Also taken | What it does |
|---|---|---|
| `the stations` | | the stations aboard, each with the person who holds it by the binding |
| `--station master` | `--station lookout`, `--station passenger`, at every door | a model at the master's, the lookout's or a passenger's station (`docs/agents/Harness.md` §15) |
| `--cadence glass` | `--cadence watch`, `--cadence events`, at every door | the seating's cadence, said in the brief |
| `--seat master` | `--seat lookout`, `--seat passenger`, at the console and the browser | the player at a lesser station, with its authority and no deck |
| `my reckoning is 49 52 N 6 10 W` | at the master's station, within a working | the master's figure, which is the ship's account when it comes in time |
| `hail sail ho, on the larboard bow` | `say ...` at the lookout's station | the lookout's hail from the masthead, heard on deck, waking an officer who stands by |
| `make her out` | at the lookout's station | the glass aloft, his to send |
| `say we shall have a blow` | at the prompt or at a station | a word in the speaker's place, heard by whoever stands there |
| `tell the master <words>` | `tell the mate <words>`, `tell Mr Harvey <words>` | a word to a station by its name or its person's, under the speaker's name and place |
| `ask the master for a course` | `ask the lookout what she is` | a question to a station, its answer back to the asker; the asker told when none comes by the patience |
| `master, you may heave to` | `Mr Harvey, you may heave to`, `master, you may not heave to` | a named thing allowed the master's station by the owner or the captain's station, and taken back |
| `stand by until noon, or a fix, or the true wind exceeds 30 knots` | a model's `stand_by` | a stand-by on several conditions in the dialect's words, any of which wakes the station, the wake's line naming which |
| `the master` | | the ship's master, and the master's station when it is held, with the working open for it |
| `the lookout` | `who is at the masthead` | who holds the lookout's station, what is in sight, his last hail |
| `the pace` | `the clock's pace` | the compression set, the rule, the samples open and since when |
| `--free-running` | at the console and the browser | no slowing while a sample is open |

## Where it comes from

Falconer 1780, MASTER ("the officer entrusted with the navigation of the ship under the captain ... to keep the reckoning") and the Regulations and Instructions of 1806 (the 1808 printing in `docs/references/admiralty/`), the Master, art. I to IV, for the master's working and his having no order of the deck; the Lieutenant's art. XIII for the deck under the captain's directions, which the rules-based captain's book is. Luce 1884 ch. XX for the lookouts at the mastheads and the hail ("Sail ho!" "Where away?"), and the custom of the deck's answer. The design is spec M6 §11 and §12 (the owner's ruling 2 of 2026-10-09, decision 39, the pace rule as the default; his note 3 of the same day, the stand-by on several conditions; his word of 2026-10-10 through the lead, the stations as data bound at run time and the passenger's station); the package is 41 in `docs/dev/M6-WorkPackages.md`, and the constants are in `docs/dev/TuningNotes.md` under it.
