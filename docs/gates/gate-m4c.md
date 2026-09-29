# Gate M4c: The ship sails herself

**Verdict:** Passed (owner, 2026-09-29). The day was sailed end to end by a real watcher through Claude Desktop, Sonnet 5.5, with the held `stand_by` call open across a glass and longer (playtest 7, `docs/playtests/2026-09-29-gate-4c-sonnet-5.5-watcher/`), which the owner judged a clean gate on the basis of the session; the provisional local test the owner asked for was two further sessions on this build through Ollama and the local runner, Qwen3.8 27B and Gemma4 26B (playtests 8 and 9, `2026-09-29-gate-4c-qwen-watcher/` and `2026-09-29-gate-4c-gemma-watcher/`), both ending amicably by the opt-out tool at the captain's word with no runaway, no forced stop and the one runner timeout retried as built; `--load` was not exercised and is carried to the first M5 gate. The Claude Code item was not run and is carried likewise. A test fault found on Windows at this gate (a ship's path compared with the platform's separator) was fixed on the main branch after the cut and the owner chose not to re-cut. The findings of the three playtests are in their notes; the two faults of playtest 7 and the missing starter line, reading, groupings and wake-up word are package 29b, and the stuck mainsail of playtest 8 (no order belays work in hand or waiting; a named party that cannot man the job waits forever) with the harness robustness items of playtests 8 and 9 (an answer refused by the tool budget, a leaked thought said as a line, empty replies uncounted) are proposed as package 29c. The original verdict line and items follow as the record of what was cut.

**As cut:** pending. Gate 4b-3 was passed on the local-model items (2026-09-28); the items the owner did not run there are carried into this gate and count for both: a real watcher through Claude Desktop with the held `stand_by` call (does it stay open across a glass?), the same through Claude Code opened on the gate folder, and a save with a station replayed to the same digest (item 8 below covers the last for any door). The report for this gate is your playtest, on the form in `docs/playtests/README.md` (spec M4 §22): the items below are the day to sail and what to look for; the form is what you write.

## Headline

Milestone 4c claims (spec M4 §18): *left to her standing orders, with a watcher narrating, the ship makes a day's passage through a changing wind, the crew tires and rests, and the whole day saves, replays and reads as a log a sailor would recognise.*

1. **A day's weather, as data.** A scenario file (`data/scenarios/gate-4c-day.yaml`) gives the ship, the start, the latitude and a weather script: waypoints of time, wind direction and strength, the wind turning and freshening in a straight line between them, with the gusts and the wander it always had riding on it. The gate's day: a fresh breeze from the west at dawn, veering north-west and rising to a strong gale in the middle watch, easing at the next dawn. The script is saved with the game, so a replay follows the same wind. `--scenario FILE` on the console and the browser server.
2. **Time compression to 300, and a log you can read at it.** `speed N` (or `time N`) up to 300 on both drivers; the buttons go to 300x. At 60x and above the log rolls up each hour's routine lines into one line in the log's voice, marked `=` ("All hands up twice, piped down three times, the hands at their work (7 steps), 4 gusts, the strongest 48 knots; 18 routine entries."), and every notable and urgent line and every order of yours stays as it is. The roll-up is a view: every line is still in the store, and in the browser a roll-up opens to show them. A watcher's samples carry the same roll-up at the same speeds, so you and it read the same digest of the same hour.
3. **Auto-slow on alarm.** An urgent line (a sail blown out, a spar carried away, a line parted) while the clock runs faster than 1x eases it to 1x and says so in the log: "Compression eased to 1x: <the line>." You speed up again when you choose; the instruments show the notice until you do.
4. **The day saves and replays.** Save at any tick (`save PATH` in the order box or the console, or the browser's download); the replay from the seed and the save's inputs gives the same log to the last line, refused orders and queries included (new: before this build a refused order was not replayed, so a day that read the starter file replayed one line short); the browser server now loads a save and goes on (`--load SAVE`), as the console always has.
5. **`tell the watcher ...`** (your tenth item): a word to a station that is not a question. "The captain to the watcher: ...", notable, journaled like `ask`; the watcher hears it in its next sample and owes no answer.

Four truths (48 to 51) were added. Three pass as the spec states them; the fourth, the performance budget, is asserted at what the build machine measures and the budget itself comes to you as a ruling (item 8).

## What you need

As before: Python 3.11 or newer (`py`) and the gate zip extracted to a fresh folder. For a real watcher instead of the scripted one, what gate 4b-3 needed for the door you choose (`docs/agents/Harness.md`).

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server,agents]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest -n 4
```
*Ends `1496 passed, 7 xfailed` (the build machine: 646 seconds on four workers). The seven expected failures are your earlier rulings (truth 3 for the schooner, truth 11's ground, truth 18's times, and truths 24, 26, 28 and 31). A `failed` is a fault. The gate's day runs in it (truths 48 to 50).*

## The day

**The scenario.** `data/scenarios/gate-4c-day.yaml`, seed 7 (the file's): the frigate at 04:00 on 1 June 1805, 50 N, heading south-east, plain sail and the royals ordered at four. The wind: W 17 knots at dawn, a fresh breeze through the day, 19 knots at 19:30; after dark veering to WNW and a moderate gale (29 knots) by 22:00, NW and 36 knots by midnight, a strong gale of 45 knots from 01:00 to 03:00; easing to 26 by 05:00 and 18 by 07:00. Every waypoint has a comment in the file saying why.

**The standing orders.** The starter routines (gate 4a's book, with the topgallants now in its shortening line by the owner's ruling) and three of the captain's for this passage (`data/scenarios/gate-4c-day.orders`, sources in the file): take in the topgallants at thirty knots; the gale canvas at thirty-six (the jib, the spanker and the mainsail in: she scuds before the gale under the topsails and foresail); make sail after the gale (storm staysail in, topgallant masts up, reefs out, plain sail, when the wind has been under twenty-five for half an hour); and the topgallants again when their masts are up. **Why the four:** under the starter routines alone the day loses canvas. The first runs blew out two topgallants and carried away the fore topgallant yard at 35 knots, and the mainsail, spanker and jib at 45: the starter book reefs once at thirty and does nothing more until forty. Truth 48 is asserted with the four, and the spec's "under the starter routines" reads here as "under the starter routines and the captain's own for the day". Say in the form whether that is the day you wanted (the ruling in item 8).

**The watcher.** Either one works, and the items say what each shows:

- the scripted watcher, `--watcher fake`: a line of the readings at each glass and each notable event, and the readings again when you tell it something; or
- a real one, as at gate 4b-3: start the game as below without `--watcher`, then connect a door to `http://localhost:8000` (`docs/agents/Harness.md`: Claude Desktop §3, Claude Code §4, the local runner §5).

## Items

- [ ] **1. Start the day in the browser.** In a terminal in the folder:
  ```
  py -m freesail.ui.server --scenario data/scenarios/gate-4c-day.yaml --watcher fake
  ```
  *The terminal prints `Scenario: The gate's day (data/scenarios/gate-4c-day.yaml).` and the weather in words, a line a waypoint (`The weather: From W, 17 knots (a fresh breeze) at 04:00 on 1 June, freshening;` ... `to NW, 18 knots (a fresh breeze) at 07:00 on 2 June.`), then `FreeSail server. Seed 7. Open http://127.0.0.1:8000/`.* Open it. *The log: `The gate's day. Wind W, 17 knots, a fresh breeze. Heading SE (135°).`, the watcher stationed, ten `Standing order '...' entered in the book` lines and the well's refusal, `Order: set plain sail.` and `Order: set the royals.`; the sails going up over the first ten minutes.* Type `standing orders` in the order box: *ten orders, the captain's three last.*

- [ ] **2. 1x and 10x: the morning.** Press **go** at 1x for a few minutes: *every line, the hands at work, the watcher's `[watcher] ...` at each notable line.* Then **10x**: *the same lines, faster; the watcher's line of the readings at each glass (`[watcher] Wind from W, 17 knots; heading SE (135°); making 7 knots; ...`).* Look for whether 10x is a speed you can sail at, and write it in the form (section 6).

- [ ] **3. A word and a question.** Type `tell the watcher we make for Falmouth; keep an eye on the weather`. *`The captain to the watcher: we make for Falmouth; keep an eye on the weather`, notable; at the next second a `[watcher]` line (the scripted one gives the readings; a real one whatever it makes of the word).* Then `ask the watcher how the sails are drawing`: *`Asked the watcher: how the sails are drawing?` and at once a notable `[watcher]` answer.* Neither is a question you must wait on; the word owes no answer.

- [ ] **4. 60x: the roll-up.** Press **60x** (an hour a minute). *From the next hour on, each hour's routine lines come as one line marked `=` at the hour's end, stamped `Forenoon watch (09:00-10:00)`; notable lines and yours as they are.* Click a roll-up line: *it opens to show the hour's lines, fetched from the store.* The watcher's samples are rolled up the same way (a real watcher sees `log.rollup` lines in its samples and can say so if asked).

- [ ] **5. 300x: the evening and the night.** Press **300x** (an hour in twelve seconds; the whole day in about six minutes on your machine). *What to look for, at seed 7 with the scripted watcher (a real watcher changes the log's lines, not the ship):*
  - *19:50 `Sunset.` and on the same second `By standing order 'night routine': taking in the royals.` (the studding sails were never set, and it says so).*
  - *About 21:44 the wind passes thirty: `By standing order 'shorten sail for weather': taking in the topgallants.` and `... reefing the topsails, one reef.`, all hands called; `Wind veered to WNW, a moderate gale.` about 21:59; a second reef about 22:56 as the wind comes and goes about thirty.*
  - *About 00:14 `By standing order 'gale canvas': taking in the jib.` (and the spanker and the mainsail).*
  - *About 00:39, in the middle watch, the heavy-weather routine: the topgallant masts sent down, the fore topmast staysail taken in, the storm staysail bent, and the close reef refused in words (three reefs are in already); about 01:15 `By standing order 'storm staysail': setting the fore storm staysail.`*
  - *Nothing blown out, carried away or parted all night: the strain lines (`straining at the bolt-ropes`, `bar-taut and surging on the pin`) are notable and many, and none urgent.*
  - *03:41 `Sunrise.` and the morning sail held (`the true wind is 45 knots, not under 20 knots`); about 05:55 `By standing order 'make sail after the gale': ...` four orders; about 06:34 the topgallants set again; by 07:00 plain sail.*

  Press **hold** when you like. Say in the form how the night read at 300x: did the roll-up keep what mattered?

- [ ] **6. An alarm eases the clock.** The day as written has no urgent line. To see one, start it again (Ctrl-C and item 1's command) and, before 21:00, type `belay standing order "shorten sail for weather"` and `belay standing order "gale canvas"` (the topgallants now come in with the starter's shortening line, so belaying it leaves them and the unreefed topsails standing into the gale); run at **300x**. *At seed 7 the heavy-weather routine still sends the topgallant masts down and close-reefs at 00:38, and the first alarm is the jib, about 01:54: `! Jib split and blew out of the bolt-ropes.` and at once `Compression eased to 1x: Jib split and blew out of the bolt-ropes.`; the clock row in the instruments reads `running at 1x; eased from 300x on an alarm: ...` until you press a speed button.* The console does the same (item 9). Say in the form whether 1x was the right floor (spec open item 8 offers 1 or 10).

- [ ] **7. Save mid-passage, load and continue, replay.** In the first game (or a new one run to the gale), type `save day.json` in the order box at a moment of your choosing, say in the first watch. *The log: `Saved to day.json at tick <N>; the log's digest is <sixteen characters>.` Note both.* Stop the server (Ctrl-C). Load it and go on:
  ```
  py -m freesail.ui.server --load day.json --watcher fake
  ```
  (`--watcher fake` puts the scripted watcher back at the station the save holds; with a real watcher, leave it off and connect the door again.)
  *The terminal: `Loaded day.json: replayed to tick <N>, <the ship's time>; the log's digest is <the same sixteen characters>.` (about a minute and a half for a day's save). The browser shows the ship where she was, the weather script still in force (the save holds it), the book as it was; press **go** and the night goes on as before.* Then the replay in the console:
  ```
  py -m freesail.ui.console
  ```
  and `replay day.json`: *`Replayed. Log digest <the same sixteen characters>. Clock held.`* The console also takes `--scenario` and `--load` as the server does, and `speed 300`.

- [ ] **8. Rulings wanted.**
  - **The budget** (spec §20, truth 51): the frigate under standing orders at 3,000 ticks a second on your machine. The build machine went from 420 to about 1,000 in this package (the profile and what was made faster are in `docs/dev/TuningNotes.md`, M4c), every number unchanged; at the assumed two to one, about 2,000 on yours. Measure it: `py -m pytest tests/test_known_truths.py -k truth_51 -s` runs the test (a thousand ticks thrice); for the figure itself, `py -c "import time; from freesail.world.scenarios import *; sf=load_scenario('data/scenarios/gate-4c-day.yaml'); w=make_scenario_world(sf); begin(w, sf); w.run(1000); t=time.perf_counter(); w.run(3000); print(round(3000/(time.perf_counter()-t)), 'ticks a second')"`. 300x needs 300; the rest is headroom for the doors and the later milestones. Rule on the budget (keep 3,000 as a target, set it at what your machine measures, or ask for the next step: fewer substeps in steady weather, or a compiled core, either of which changes numbers).
  - **The day's standing orders**: the topgallants are now in the starter book's shortening line (the owner's ruling before this gate); the captain's three for the passage beside it. Say whether the day's orders read as a captain's night orders should.
  - **Auto-slow's floor**: 1x as built, or 10x.

- [ ] **9. The console at the same speeds** (optional): `py -m freesail.ui.console --scenario data/scenarios/gate-4c-day.yaml --watcher fake`, `go`, `speed 300`: *the roll-up lines start with `=`; an alarm prints `* ... Compression eased to 1x: ...`.*

## The report

Fill `docs/playtests/README.md`'s form in a new folder, `docs/playtests/<date>-gate-4c-<the watcher>/notes.md`, with `day.json` beside it (the ship's path made relative). Its sections are the gate's questions: the scenario and seed; what happened in your words; what you ordered and why; what you wished to say and could not; what the watcher said that was useful, useless or wrong; how the day felt at 1x, 10x, 60x and 300x; any number a sailor would call wrong (the tuning notes name one already: a gust of 67 knots in a 45-knot gale); how the setup went; and what to keep from a model's own account if a real one kept the watch. The form is the input to milestone 5.

## What this gate does not do

- **The director's world orders** (milestone 7b): the weather script's waypoints are what a director will write at run time, appended at the tick they are given and journaled like an order, so a replay follows them; nothing here builds it.
- **Weather with a reason** (milestone 5): the script stands in for moving systems; the gusts are still the M2 wind's.
- **The handover** (spec open item 9b): a model's context across a long day is carried by the roll-up in its samples, its journal and the shelf; the handover note follows when a session has run long enough to need it. The form asks how well that worked.
