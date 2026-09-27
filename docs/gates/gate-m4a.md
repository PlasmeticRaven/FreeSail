# Gate M4a: Standing orders

**Verdict:** pending.

## Headline

Milestone 4a claims:

1. **The ship keeps herself by rules the captain wrote, in the captain's words.** `standing order "night routine": at sunset then take in the studdingsails; take in the royals` is an order like any other: given at the prompt, journaled, replayed, listed, belayed and resumed. When it fires the log says which order fired and what it did, and nothing happens that the log does not explain.
2. **One registry of readings.** What a rule may test (the true wind, the apparent wind, the heading, the speed, the heel, the watch, daylight, a sail by name, the strain, the hands) is what `state` and the browser window show and what an agent will ask for in 4b. A reading added once is known everywhere.
3. **The sun.** Sunrise, sunset and civil twilight come from the date and the ship's latitude (50 N, the Channel) by the standard approximation, within two minutes of the almanac; `at sunset` fires on the sun's own tick.
4. **Three guards against thrashing.** Durations debounce (a two-minute gust to 32 knots does not fire a rule that wants thirty for two minutes), a `when` order fires once on the edge and waits five minutes of false before it may fire again, and two orders on the same part are settled by rank with a line in the log.
5. **One engine.** A rule written in Python builds the same order, enters the same book and gives the same log, to the letter.

Seven truths (34 to 40) were added; six pass, and one half of truth 37 comes to you as a ruling (item 5).

## What you need

As before: Python 3.11 or newer (`py` works where `python` does not) and the gate zip extracted to a fresh folder.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest
```
*Takes about twelve minutes. Ends `1253 passed, 8 xfailed`. The eight expected failures are the seven earlier rulings (truth 3 for the schooner, truth 11's ground, truth 18's times, and truths 24, 26, 28 and 31) and one of this milestone marked for your ruling (truth 37's storm staysail, item 5). A `failed` is a fault.*

## Checklist

Seed 7, wind from the north, as at the earlier gates. The console's wind gusts and wanders, so a speed can differ from these by a few tenths of a knot and a firing that depends on the wind by some minutes; the sun's times and the log lines should match to the minute. Commands after `>` are typed at the prompt; `tick` is game seconds. A whole day is 86,400 ticks and takes the console about three minutes to run through; the items below run to sunset where they must and stop short where they can.

### Part A: the night routine, the book, the belay

```
py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180
```

She lies head south with the wind dead aft, so the studding sails will draw.

- [ ] **1. The night routine, given at the prompt and run to sunset.** Type `make all sail`, `tick 600`, `rig out the studdingsails, both sides`, `tick 300`, `set the studdingsails, both sides`, `tick 600`, `state`. Expect ten `Rigged out the ... studdingsail boom.` lines at 04:10, the ten studding sails set between 04:19 and 04:24, and in `state` a new third line: `Day. Sunrise 03:56, sunset 19:58; civil twilight from 03:13 and until 20:41.` (about `6.5 kn`). Now give the order and read it back:

  ```
  standing order "night routine": at sunset then take in the studdingsails; take in the royals
  standing orders
  ```
  Expect `Standing order 'night routine' entered in the book: at sunset then take in the studdingsails; take in the royals.` and `Standing orders (1):` with `"night routine" (the captain): ... Standing; never fired.` Then `tick 55500` (about two minutes of real time; bells, watch changes and gusts scroll by) and `state`: `Last dog watch (19:50)`, still `Day.` Then `tick 600`. Expect, at 19:59, three notable lines together:

  ```
  * Last dog watch (19:59)  Sunset.
  * Last dog watch (19:59)  By standing order 'night routine': taking in the studdingsails.
  * Last dog watch (19:59)  By standing order 'night routine': taking in the royals.
  ```
  and then the hands' ordinary lines as the studding sails and royals come in. `state` now says `Twilight.`; `standing orders` says `Standing; fired once, last at Last dog watch (19:59).` The "By standing order" line is notable and stands where a typed order's "Order:" line would. Type `quit`.

- [ ] **2. Read the book from the file.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293`. Type `read the standing orders from data/standing_orders/starter.orders`. Expect five `Standing order '...' entered in the book: ...` lines (night routine, morning sail, shorten sail for weather, keep her full, heavy weather), one refusal, `Order not carried out ('standing order "sound the well": every glass then sound the well'): In standing order 'sound the well', 'sound the well': The ship has no well to sound yet; that reading comes with the world.`, and `Read 6 standing orders from data/standing_orders/starter.orders.` The refused line did not stop the rest. Type `standing orders`: `Standing orders (5):`, each with who gave it, its text and `Standing; never fired.` Then `show standing order "keep her full"`: the order, its state, and `Armed; waiting for its condition.` Keep this console.

- [ ] **3. Belay and resume.** Continue: `belay standing order "keep her full"`: `Standing order 'keep her full' belayed.` `show standing order "keep her full"`: `Belayed; never fired.` `belay standing order "keep her full"` again: refused, `belayed already`. `resume standing order "keep her full"`: `Standing order 'keep her full' resumed.` `belay all standing orders`: `All 5 standing orders belayed.` `belay standing order "night routin"` (misspelt): `There is no standing order 'night routin' in the book; did you mean 'night routine'?` Type `quit`. Every one of these but the queries is journaled, so a save replays them (item 7).

  The same file loads at the start on both drivers: `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --standing-orders data/standing_orders/starter.orders` prints the same eleven lines before the prompt, and `py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --standing-orders data/standing_orders/starter.orders` the same into the browser's log.

### Part B: the guards

- [ ] **4. The gust that does not fire.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,27 --heading 282`. Type `set plain sail`, `tick 600`, `trim sails`, then

  ```
  standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef
  ```
  and `tick 3600`. The console's gusts in the hour reach `A gust: 44 knots.` (04:52) and last seconds; the wind's mean stays under thirty; nothing fires. `show standing order "shorten sail for weather"`: `Standing; never fired.` and `Armed; waiting for its condition.` Type `quit`. Now the same with `--wind 0,33`: the same four commands, then `tick 600`. The mean wind wanders about the threshold and holds over thirty for two minutes together at 04:17: `* Morning watch (04:17)  By standing order 'shorten sail for weather': reefing the topsails, one reef.`, after two routine lines saying the studding sails and royals were already in (`Standing order 'shorten sail for weather': order not carried out ('take in the studdingsails'): Nothing done: ... already furled ...`). It fires once; `tick 1800` and it has not fired again, the wind still over thirty. Type `quit`.

  In steady wind the truth measures it exactly: 119 seconds over thirty and a fall does not fire it; 120 does, once; under thirty for 299 seconds and up again does not re-arm it; 300 does (truth 35). The console cannot raise or steady the wind, which is why the base is 33 here and the measured times are the truth's.

- [ ] **5. The heavy-weather routine in a gale.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,45 --heading 282`. Type `call all hands`, `set the topsails`, `set the courses`, `set the fore topmast staysail`, `tick 900`, `state` (the courses, topsails and fore topmast staysail set by 04:07; about `1.6 kn` still gathering way). Then

  ```
  standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then send down the topgallant masts; shift the fore topmast staysail for the fore storm staysail; close reef the topsails
  ```
  `tick 300`, `tick 3000`. Expect at 04:20 (five minutes after the order, the wind over forty the whole time) three lines together, in the routine's order:

  ```
  * Morning watch (04:20)  By standing order 'heavy weather': sending down the topgallant masts.
    Morning watch (04:20)  Standing order 'heavy weather': order not carried out ('shift the fore topmast staysail for the fore storm staysail'): ...
  * Morning watch (04:20)  By standing order 'heavy weather': close reefing the topsails.
  ```
  In the console's gusty 45 knots the fore topmast staysail split and blew out a minute before (04:21 in the run this was measured on; the tick differs with the gusts), so the refusal reads `The fore storm staysail is not bent in the fore topmast staysail's place`; had it still been set, it reads `The fore topmast staysail is set; take it in before shifting it.` Either way the shift is not done. Then `Sent down on deck the fore topgallant yard, ...` (04:33), `* Sent down the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast; the upper spars on deck.` (04:45), and `Reefed the fore topsail; now set, 3 reefs.` (04:53), the main (05:02) and the mizzen after. `show standing order "heavy weather"`: `Fired; its work is still in hand.` Type `quit`.

  **Your ruling (truth 37).** The routine as the specification writes it cannot shift the staysail: the shift evolution refuses a sail that is set, and in a gale rising to 45 knots the head sails blow out at about 44 before the five minutes are up. The truth's masts, reefs, order and all hands pass; its storm staysail is a strict expected failure. Two ways out are in `docs/dev/TuningNotes.md` ("Found on the way (package 26)"): a shift that takes the sail in first, or a routine that shortens sail earlier and shifts at forty. Rule which.

- [ ] **6. The conflict line.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293`. Type `set plain sail`, `set the royals`, `brace sharp up on the starboard tack`, `tick 600`, then the captain's order and the master's:

  ```
  standing order "royals in": every glass then take in the royals
  standing order "royals" by the master: every glass then set the royals
  ```
  Expect `Standing order 'royals' entered in the book by the master: ...` for the second. `tick 2400`. At 04:40, half an hour after they were given, both fall due on the one tick; the captain's is given and the master's is not:

  ```
  * Morning watch (04:40)  By standing order 'royals in': taking in the royals.
  * Morning watch (04:40)  Standing order 'royals' (the master) countermanded by 'royals in' (the captain).
  ```
  and the royals come in (`Took in the fore royal; hanging in the gear.` at 04:42). `standing orders`: the master's `Standing; never fired.` Type `quit`. Two of the captain's own that conflict are noted, not countermanded: item 5's run has `Standing orders 'shorten sail for weather' and 'heavy weather' (both the captain's) give contrary orders on the fore topsail, the main topsail and the mizzen topsail; the later stands.` when the whole starter file is loaded in a gale.

### Part C: a day replayed, and the Python twin

- [ ] **7. A day under the starter routines, saved and replayed.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180 --standing-orders data/standing_orders/starter.orders`. The five orders enter and the well's is refused before the prompt. Type `make all sail`, `tick 600`, `rig out the studdingsails, both sides`, `tick 300`, `set the studdingsails, both sides`, `tick 56700` (to 20:00; about two minutes). Expect the sunset and the night routine's two lines at 19:59 as in item 1, and nothing from the other routines (the wind never reached thirty, and running she is never pinched). `save day.json`: `Saved to day.json at tick 57600.` `replay day.json`: `Replaying day.json to tick 57600...` (about two minutes more) and `Replayed. Log digest d82a69017b59b63d. Clock held.`, then `state` as before the save, `Twilight.` and about `7.0 kn`. `standing orders`: the five, the night routine `fired once, last at Last dog watch (19:59)`. The firings were not in the save; the replay re-fired them from the seed and the journal. One line the replay does not carry is the well's refusal at the start: a refused order is not journaled (as at every gate since M0), so the replayed log is one line shorter than the one you watched, though the ship, the book and every firing are the same. Type `quit`.

- [ ] **8. The Python twin.** At the terminal (not in the console):

  ```
  py tools/python_twin.py
  ```
  The script builds two frigates from seed 7 at 19:40, head south with the wind north, and both make all sail. One is given the night routine at the prompt, in the dialect; the other is given the same rule in Python, through the API:

  ```python
  bind(python)

  @at("sunset", name="night routine")
  def night_routine():
      order("take in the studdingsails")
      order("take in the royals")
  ```
  Both run twenty-five minutes through sunset. *Prints the Python rule's firing at 19:59 (`By standing order 'night routine': taking in the royals.`, after a line saying the studding sails were already in, since this frigate has no booms out), then `same log after the order: True`: every event after the tick the rules were given is the same text at the same tick in both logs. The last lines read `Standing order "night routine", given by the captain (python): at sunset then ... Standing; fired once, last at Last dog watch (19:59).`* The script is `tools/python_twin.py`, short enough to read; truth 40 does the same with the studding sails set and compares 63 events.

## Guide

**The sun.** NOAA's solar position approximation (the declination and the equation of time as series in the day of the year; sunrise at a zenith of 90.833°, civil twilight at 96°), checked against the U.S. Naval Observatory's figures for 50 N on 1 June: sunrise 03:56, sunset 19:58 to 19:59, twilight 03:13 to 20:41, all within two minutes of the almanac. The scenario carries `latitude_deg` (50) and saves it. `daylight` is a reading: `state` shows it, and a rule may say `when daylight is night`. The default scenario opens four minutes after sunrise, and a sunrise before the log opened is not an event of it.

**The starter routines.** `data/standing_orders/starter.orders`, with a comment above each naming where its numbers come from: Luce's routine of the day for the night and morning routines, the strain truths for thirty and forty knots, the pointing truths for 55 degrees. The well's line is kept in the file and refused at load, to show that a refused line stops nothing.

**Orders added.** `trim the fore topsail` (that sail's yard braced to the wind), `trim the jib` (its sheet), `trim the topsails`, `tend the sheets` (every fore-and-aft sheet, no brace), and for bearing away the words you reached for at the first playtest: `fall off`, `off the wind`, `steer off the wind`, `bear off the wind`. `by and large` is still refused: it describes how she sails and is not a helm order. `steady out the bowlines` re-hauls the bowlines after she has fallen off far enough for the yards to come in (past forty degrees from square, when the hands let them go with a log line) and been brought by the wind again; chapter 4 of the primer says when.

**Runtime cost.** The frigate under five standing orders ticks at about 457 a second on the build machine against 503 bare.

## Not in this milestone

- **A wind that rises at the prompt.** The console's wind gusts and wanders about its base; nothing at the prompt raises it. The rising gale of truth 37 is blown in the test; the gate's gale starts at 45.
- **A Python rule's body run at firing.** The body runs once as the rule is entered and its `order(...)` calls are collected; computation on the readings at firing is milestone 6's sandbox.
- **A rule that waits.** A firing's orders go on one tick; `take in the staysail; shift it` cannot be said yet (item 5).
- **The well, the glass, the depth and sightings** as readings: milestone 5. Naming them is refused with the sentence.

## What to report back

- Pass or fail for items 1 to 8.
- Your ruling on truth 37's storm staysail (item 5), and on the head sails blowing out at 42 to 44 knots before the courses and topsails complain (`docs/dev/TuningNotes.md`, "Head canvas in a gale").
- Whether "By standing order 'x': ..." and the refusals ("Standing order 'x': order not carried out (...)", "not carried out; the true wind is 25 knots, not under 20 knots") read as a ship's log.
- Whether `keep her full` at 55 degrees apparent is the routine you want (it bears away once from six points off and then holds her a point off; the frigate carries 55 degrees apparent at seven and a half points off the true wind), or whether the starter file should say 50.
