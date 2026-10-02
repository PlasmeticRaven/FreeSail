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

Lines are orders to type, one per line. A line beginning `# rejected:` is an order the ship refuses, shown so that you learn the refusal. A line such as `tick 300` or `state` is a console command, not an order to the ship; chapter 6 lists them. The word after `orders` names the ship the block is for, and a word after that (`plain-sail`, `all-sail`, `reefed`, `larboard`) says what state she is in when the block begins. A test in the repository (`tests/test_primer.py`) runs every such block through the parser and fails if the book and the ship disagree, so what is printed here is what she understands.

A block tagged `orders-pending` (there are none at present) shows an order that is being added and is not yet in the vocabulary; the test skips it until the verb exists.

What the log will say is shown in plain code blocks, copied from a run with seed 7 and a north wind of 15 knots with the physics as tuned by package 10 (`docs/dev/TuningNotes.md`), so that your log matches this book line for line until the first gust.

## The chapters

| | Chapter | What it teaches |
|---|---|---|
| 1 | [The ship](01-the-ship.md) | Every part of the frigate *Amazon* and the schooner *Speedwell* by its name, so that you can point at any noun the parser accepts. |
| 2 | [The wind and the points of sail](02-the-wind-and-the-points-of-sail.md) | True and apparent wind, tacks, close-hauled, full and by, reaching, running; why a square-rigger lies six points off; what `state` reports. |
| 3 | [Making and shortening sail](03-making-and-shortening-sail.md) | Plain sail, the order of setting and taking in, reefing, studding sails; the words of command and what they mean. |
| 4 | [Trimming](04-trimming.md) | Bracing the yards, tending the sheets, the `trim` order, weather and lee helm. |
| 5 | [Going about](05-going-about.md) | Tacking as the log shows it, missing stays, wearing, box-hauling, heaving to and filling away. |
| 6 | [The watch and the log](06-the-watch-and-the-log.md) | Bells and watches, the marks in the log, the console commands, saving and replaying. |
| 7 | [A first passage](07-a-first-passage.md) | A worked hour on each ship that you can type along with. |
| 8 | [Where to read more](08-where-to-read-more.md) | The chapters of Luce, Lever and Falconer behind each evolution. |
| 9 | [The glass and the sky](09-the-glass-and-the-sky.md) | The barometer and its tendency, Beaufort's words for the sky, the weather and the visibility as readings and as lines in the book; the sea in the period's words and the ship's motion in it, what the hands and the gear feel of a seaway; what a captain of 1805 knew of the weather and what he did not. |
| 10 | [The reckoning](10-the-reckoning.md) | The log-line, the traverse and the master's doubt; the noon sight; the lead and its arming; bearings and the landfall; the captain's override; shaping a course by account; the readings and what the master's words mean; every form of the master's orders and the reckoning's readings in a table. |
| 11 | [The starting book](11-the-starting-book.md) | The starter book of standing orders, a choice and never a requirement: each routine with the reason it exists, how to load it or begin with none, and the standing dialect whole for writing your own, its forms in a table. |
| 12 | [The longitude](12-the-longitude.md) | The chronometer and the time sight; the moon and the lunar, drawn and not computed; the amplitude and the azimuth for the variation; the chart in the captain's hands (a bearing by account, the dangers, a course that passes a rock); the lookout's distances; every form the longitude's orders take, in a table. |
| 13 | [The tide and the anchor](13-the-tide-and-the-anchor.md) | The world's tide under the lead and in the track, and the captain's by his epitome and the moon's age; taking the ground and floating off; the ground tackle by the ship's size; coming to an anchor, riding, dragging and weighing in Luce's words; the readings and events of it, in a table. |
| 14 | [The port](14-the-port.md) | The named people aboard and where they are; the places and the ship's papers by handle; the pilot who comes off in his cutter and what he knows; the anchorage, the moor and the kedge; the boat ashore, the market and its rules, the yard and the crew pool; getting under way as Luce has it, with the tide; every form in a table. |
| 15 | [Other sail](15-other-sail.md) | The dozen other ships at far detail and what the lookout makes out of a sail as she nears: the hail, her rig, her colours or none, what she is; the strangers, the glass aloft and the chase; what a world order is and why the captain cannot give one; the two passages of the gate; the forms in a table. |
| 16 | [The officer of the watch](16-the-officer-of-the-watch.md) | The first station with authority: who the officer is, how the captain gives and takes the deck, what the station may order and may not and why, the night orders and standing orders by rank, standing by with the deck, the handover note, what the harness watches for; the forms in a table. |

## Where to start

If you have run the gate M1 checklist, go straight to chapter 2, then 4 and 5; chapter 1 is for looking things up. If you have not, chapter 7 is the checklist rewritten as a passage: type it through once, then read chapters 2 to 5 to learn what you did.

## Sources

Three books, all in `docs/references/` as OCR text:

- **Falconer**, *An Universal Dictionary of the Marine*, 1780 edition. The names of things. Cited as "Falconer, *Brace*".
- **Lever**, *The Young Sea Officer's Sheet Anchor*, 1827 printing of the 1808 book. In period; the manoeuvres with their figures. Cited as "Lever, 'Tacking Expeditiously'".
- **Luce**, *Seamanship*, 1866 (1877 printing) and *Text-Book of Seamanship*, 1884. Later and American, but the fullest sequences of orders. Cited by chapter and sub-heading as the evolution files cite them: "Luce 1866, ch. XXIV Working to Windward, 'Tacking'".

Where Luce says "port" the game says "larboard": the Royal Navy did not change until 1844 (see `docs/references/LuceChapterMap.md`).
