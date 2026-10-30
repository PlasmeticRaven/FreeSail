# The Sailing Master's Primer

How to sail the ships of FreeSail in the manner of 1805 and in the words of 1805, using the game's own Orders. It is written for a reader who knows in theory how a sailing vessel works but has not the habit of the terminology, and it does not spare the terminology: the game refuses "left" and accepts "larboard", and so does this book. Every word it uses is one that Falconer, Lever or Luce used, and the last chapter says where.

The same text is what a player reads and what a language-model officer is given as its documentation, so it says exactly what the game does and no more. Where a real sailing master would do something the game cannot yet do, the chapter says so.

## How to use it

Start the frigate in the console and read with it open:

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

Every order in this book is shown in a code block like this one:

```orders frigate
set the fore topsail
# rejected: set the topsail
```

Lines are orders to type, one per line. A line beginning `# rejected:` is an order the ship refuses, shown so that you learn the refusal. A line such as `tick 300` or `state` is a console command, not an order to the ship; chapter 6 lists them. The word after `orders` names the ship the block is for, and a word after that (`plain-sail`, `all-sail`, `reefed`, `larboard`) says what state she is in when the block begins. The game's own tests run every such block through the parser and fail if the book and the ship disagree, so what is printed here is what she understands.

A block tagged `orders-pending` (there are none at present) shows an order that is being added and is not yet in the vocabulary; the test skips it until the verb exists.

What the log will say is shown in plain code blocks, copied from a run with seed 7 and a north wind of 15 knots. Chapter 7's logs are recorded from the game as it stands, so that yours match them line for line; the other chapters' were recorded as each was written, and the words are the game's where a figure may since have moved by a few tenths.

## The chapters

| | Chapter | What it teaches |
|---|---|---|
| 1 | [The ship](01-the-ship.md) | Every part of the frigate *Amazon* and the schooner *Speedwell* by its name, so that you can point at any noun the parser accepts. |
| 2 | [The wind and the points of sail](02-the-wind-and-the-points-of-sail.md) | True and apparent wind, tacks, close-hauled, full and by, reaching, running; why a square-rigger lies six points off; what `state` reports; the compass to the quarter point (*south by west half west*) and numbers in words. |
| 3 | [Making and shortening sail](03-making-and-shortening-sail.md) | Plain sail, the order of setting and taking in, reefing, studding sails; the words of command and what they mean. |
| 4 | [Trimming](04-trimming.md) | Bracing the yards, tending the sheets, the `trim` order, weather and lee helm. |
| 5 | [Going about](05-going-about.md) | Tacking as the log shows it, missing stays, wearing, box-hauling, heaving to and filling away. |
| 6 | [The watch and the log](06-the-watch-and-the-log.md) | Bells and watches, the marks in the log, the console commands, saving and replaying. |
| 7 | [A first passage](07-a-first-passage.md) | A worked hour on each ship that you can type along with; standing orders, read whole when they are given; the words the ship takes and those it refuses with what to say instead. |
| 8 | [Where to read more](08-where-to-read-more.md) | The chapters of Luce, Lever and Falconer behind each evolution; where each thing is in the library a station reads, topic by topic. |
| 9 | [The glass and the sky](09-the-glass-and-the-sky.md) | The barometer and its tendency, Beaufort's words for the sky, the weather and the visibility as readings and as lines in the book; the sea in the period's words and the ship's motion in it, what the hands and the gear feel of a seaway; what a captain of 1805 knew of the weather and what he did not. |
| 10 | [The reckoning](10-the-reckoning.md) | The log-line, the traverse and the master's doubt; the noon sight; the lead and its arming; bearings and the landfall; the captain's override; shaping a course by account; the readings and what the master's words mean; every form of the master's orders and the reckoning's readings in a table. |
| 11 | [The starting book](11-the-starting-book.md) | The starter book of standing orders, a choice and never a requirement: each routine with the reason it exists, how to load it or begin with none, and the standing dialect whole for writing your own, its forms in a table; every event the book's `at` takes, by family. |
| 12 | [The longitude](12-the-longitude.md) | The chronometer and the time sight; the moon and the lunar, drawn and not computed; the amplitude and the azimuth for the variation; the chart in the captain's hands (a bearing by account, the dangers, a course that passes a rock); the lookout's distances; every form the longitude's orders take, in a table. |
| 13 | [The tide and the anchor](13-the-tide-and-the-anchor.md) | The world's tide under the lead and in the track, and the captain's by his epitome and the moon's age; taking the ground and floating off; the ground tackle by the ship's size; coming to an anchor, riding, dragging and weighing in Luce's words; the readings and events of it, in a table. |
| 14 | [The port](14-the-port.md) | The named people aboard and where they are; the places and the ship's papers by handle; the pilot who comes off in his cutter and what he knows; the anchorage, the moor and the kedge; the boat ashore, the market and its rules, the yard and the crew pool; getting under way as Luce has it, with the tide; every form in a table. |
| 15 | [Other sail](15-other-sail.md) | The dozen other ships at far detail and what the lookout makes out of a sail as she nears: the hail, her rig, her colours or none, what she is; the strangers, the glass aloft and the chase; what a world order is and why the captain cannot give one; the two passages that ship with the game; the forms in a table. |
| 16 | [The officer of the watch](16-the-officer-of-the-watch.md) | The first station with authority: who the officer is, how the captain gives and takes the deck, what the station may order and may not and why, the night orders and standing orders by rank, standing by with the deck, the handover note, what the harness watches for; the forms in a table. |
| 17 | [The captain](17-the-captain.md) | The ship's company by name, with the wardroom's ranks, places and outlines and the stations bound to them; the rules-based captain who sails her when nobody is seated, in three layers (intent, plan and behaviour as books of a state) and by perception on the player's terms; the captain's station with the player's whole surface, the deck his by right and lent to his book when his door is silent; the owner's place and the player's seat at a lesser station; the forms in a table. |
| 19 | [The wardroom](19-the-wardroom.md) | The stations as the ship's own, bound to her people at run time; the master's station, whose figure is the ship's account when it comes in time; the lookout's, which hails the deck; a passenger's; the deck's conversation (say, tell, ask, heard by place); who may give what, and the rules-based captain over a seated officer; the stand-by on several conditions; the pace rule and each seating's cadence; the forms in a table. |
| 20 | [The director](20-the-director.md) | A station above the game, bound to no ship's person, which sees the truth and shapes the voyage through world orders alone, by plausible causes: the forms as examples and not a rule, an order doubted and entered again with a reason, one the game cannot perform logged as attempted, the brief and the limits the channel enforces, the budget by the ship's day, the log hidden until asked for and inline in the replay view; the forms in a table. |
| 21 | [The fisherman](21-the-fisherman.md) | The grounds of the Channel and the Bay with their fish, seasons and yields; the gear the smack and the lugger carry and the evolutions that shoot and haul it, with their hours and the sail each allows; the catch in the well and the hold, the salt and the spoilage; the fish quay; the business's fishermen at both details. |
| 22 | [An action](22-an-action.md) | From clearing for action to the colours struck, in the player's words: the guns as parts with their crews from the quarter bill, the drum that never queues, the standing intentions and the one-shot orders of the gun deck, the fall of shot by the range and the heel, a hit as a change of the ship's own state, the fighting book and the doctrine as data, morale and the strike by rule, the first action at seed 7; the orders in two tables. |
| 23 | [Colours, the private signal, a hail, a signal made and read](23-colours-and-signals.md) | The voice between ships before a gun is fired: the colours as a state every lookout reads by what is shown (true, false, none, struck, distress) and the pirate's act of a shot under false colours; the private signal of the month, carried by the King's ships, challenged and judged right, wrong or none; the signal books by nation in one shape, a signal made by its meaning and read a minute after it is seen by whoever has the book, the telegraphic sentence, the convoy under your orders tacking in succession on one hoist; the hail within four cables answered by table, by a model or by the player; the lights by night and the bell in fog; the forms in a table. |
| 24 | [The squadron, the convoy and the station](24-the-squadron.md) | Ships in company as a genuine set: the squadron and the convoy with their order of sailing, formation and pace; the station kept at far detail by a leg and on the near body by the order `keep station`, read from the lookout and the set's course; the commodore's book in data signalling a straggler, closing the convoy, bearing a blockade up for its rendezvous in a gale; the succession by the wake; the regimes of a nation's ships and the business drawing convoys and blockades and following your ship across the regions; the three days at seed 7; the forms in a table. |
| 25 | [Water, wounds and the fight on deck](25-water-wounds-and-the-fight-on-deck.md) | The well and the pumps, the carpenter's and the boatswain's repairs, the surgeon and the sick list, the marines and the boarders; what happens to the person a station holds when he is hit. |
| 18 | [The lessons](18-lessons.md) | Worked passages, each a duty an officer must be able to do alone, sailed at seed 7 and quoted from the log: a landfall on one headland; his own reckoning from the master's slate, judged at noon; a pilotage by cross bearings and the allowance for a set; heaving to for a pilot; coming to an anchor in a tideway; a night standing off a lee shore; each with the rule of the period, the orders, what the log says when it goes right, and the usual mistake; the path to a command. |

## Where to start

If you have sailed her once already, go straight to chapter 2, then 4 and 5; chapter 1 is for looking things up. If you have not, chapter 7 is the checklist rewritten as a passage: type it through once, then read chapters 2 to 5 to learn what you did. Before a first watch at the officer's station, yours at the console or a model's, read chapter 16 for the station and chapter 18 for its duties, and sail the lessons.

## Sources

Three books, all in `docs/references/` as OCR text:

- **Falconer**, *An Universal Dictionary of the Marine*, 1780 edition. The names of things. Cited as "Falconer, *Brace*".
- **Lever**, *The Young Sea Officer's Sheet Anchor*, 1827 printing of the 1808 book. In period; the manoeuvres with their figures. Cited as "Lever, 'Tacking Expeditiously'".
- **Luce**, *Seamanship*, 1866 (1877 printing) and *Text-Book of Seamanship*, 1884. Later and American, but the fullest sequences of orders. Cited by chapter and sub-heading as the evolution files cite them: "Luce 1866, ch. XXIV Working to Windward, 'Tacking'".

Where Luce says "port" the game says "larboard": the Royal Navy did not change until 1844 (see `docs/references/LuceChapterMap.md`).
