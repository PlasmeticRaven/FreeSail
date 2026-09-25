# Gate M0: Skeleton and log

**Verdict:** Pending.

**Download:** the release page for `gate-m0` at https://github.com/PlasmeticRaven/FreeSail/releases/tag/gate-m0, or the plain zip of the tagged project at https://github.com/PlasmeticRaven/FreeSail/archive/refs/tags/gate-m0.zip. Either contains everything below.

## Headline

Milestone 0 claims four things:

1. **The clock ticks and keeps a ship's log.** Time advances one game second at a time, bells strike, and everything that happens is written as a log line in a ship's-log voice.
2. **The wind lives.** There is a wind that wanders a little, gusts now and then, and never dies, and the log notices when it shifts.
3. **There is a ship, of a sort.** For this milestone it is only a point that can be told to steer a course and make a speed. There are no sails yet.
4. **Nothing is lost and nothing is random by accident.** A save file holds only the starting seed and the orders you gave. Rebuilding from it produces exactly the same log, line for line. Two runs with the same seed and the same orders are identical.

Nothing else is claimed. In particular there is no physics, no rigging and no browser window yet.

## What you need

- A Windows PC (Mac and Linux work the same way; the commands are identical).
- **Python 3.11 or newer.** Get it from https://www.python.org/downloads/ and, on the first screen of the installer, tick **"Add python.exe to PATH"** before clicking Install. The Microsoft Store version of Python also works.
- The gate zip, extracted to a folder. The examples below assume `D:\Projects\FreeSail-gates\gate-m0`.

## Setup

Open a terminal in the extracted folder. On Windows: open the folder in File Explorer, click in the address bar, type `cmd` and press Enter. A black window opens with the folder's path shown.

Type each line and press Enter. What you should see is in *italics*.

```
python --version
```
*Python 3.11.x or higher. If you see "not recognized", Python was not added to PATH; try `py --version`, and if that works use `py` wherever `python` appears below.*

```
pip install -e ".[dev]"
```
*A few lines about collecting and installing packages, ending in "Successfully installed ..." (the exact list varies). This can take a minute the first time.*

```
python -m pytest
```
*Dots, then a line reading `55 passed in ...s`. Anything saying `failed` is a fault; note the name of the failing test.*

## Checklist

Tick each item. The exact words to type are in code; what to look for follows.

Start the console:

```
python -m freesail.ui.console --seed 7
```

- [ ] **1. It starts and reads like a log.** The first line is `* Morning watch, 8 bells (04:00)  Open water. Wind SW, 15 knots, a moderate breeze. Heading N (0°).` followed by a line about the seed and how to get help. The clock is held: nothing scrolls until you say `go`.

- [ ] **2. Orders are acknowledged.** Type `steer south-west by west`. Two lines appear: `Order: steer south-west by west.` and `Helm ordered: steer SW by W (236°).`

- [ ] **3. The ship comes round.** Type `tick 60`. You should see `Steady on SW by W (236°)` among the lines, then `Advanced 60 ticks to Morning watch (04:01).` (The point ship turns two degrees a second; 236 degrees takes just under two minutes, so it is steady before the minute is out because it turned the short way, through west.)

- [ ] **4. She makes way.** Type `speed 6 knots`, then `tick 1800`, then `state`. The state shows `Speed 6.0 kn` and a position with both numbers negative, since south-west by west is south and west of the start. Roughly `-4500 m E, -3000 m N` after half an hour at six knots.

- [ ] **5. Bells strike.** In the same output you should have seen `Morning watch, 1 bell (04:30)  1 bell.` Type `tick 1800` again and look for `2 bells` at 05:00.

- [ ] **6. Nonsense is refused politely.** Type `splice the mainbrace`. You should see `Order not carried out ('splice the mainbrace'): 'splice' is not an order this ship understands. Try 'steer', 'speed' or 'stop'.` The clock does not stop and nothing else changes.

- [ ] **7. The wind wanders and gusts.** Type `time 300` (five game minutes per real second), then `go`. Let it run for about a minute of real time, then type `hold` and `state`. The wind line should still be near 15 knots (anywhere from about 10 to 22 is normal) and may show a different point from SW. Scroll up: over five game hours there will usually be some lines marked `*` reading `Wind veered to ...` or `Wind backed to ...`, and some `A gust: 19 knots.` style lines may have been rolled up into `(N routine entries)` summaries at each bell. The exact numbers depend on the seed; that is the point of the next two items.

- [ ] **8. Saving and rebuilding gives the identical log.** Type `save voyage.json`. Then type `replay voyage.json`. You should see `Replaying voyage.json to tick N...`, then `Replayed. Log digest ...`, then a state block. The state block must match what `state` showed you just before, number for number, including the wind. (What a digest is, and why this matters, is in the guide below.)

- [ ] **9. The same seed always gives the same voyage.** Type `quit`. Start again with exactly the same command, `python -m freesail.ui.console --seed 7`, and type `tick 18000` then `state`. Write down the wind and position. Quit, start it a third time with the same command, do the same, and compare. They must be identical to the last digit. Then start it with `--seed 8` and do the same: the wind should differ.

- [ ] **10. Compression rolls up the routine.** Start again, type `time 60` and `go`. The bells still print every half game minute of real time, and the small stuff between them is summarised as `(N routine entries)` rather than scrolling by. Type `hold` and `time 1` and `go`: now every line prints as it happens. `quit` to leave.

## Guide to the technical ideas in the checklist

**Tick.** One tick is one second of game time. `tick 1800` advances half an hour instantly. Nothing happens between ticks.

**Compression** (`time N`). How many game seconds pass per real second while the clock is running. `time 1` is real time. `time 300` is five game minutes per real second, so an hour of sailing takes twelve seconds to watch.

**Seed.** A number that fixes every "random" choice the simulation will make: how the wind wanders, when gusts come. Two runs with the same seed and the same orders make the same choices, which is why item 9 works. `--seed 7` and `--seed 8` are two different weathers. This is what will later let a storm be replayed a hundred times to test a language model against it.

**Save file and replay.** A save is *not* a snapshot of the ship. It is the seed, the starting conditions and the list of orders you gave with the tick each was given at. `replay` rebuilds the world from nothing and re-gives the orders at the same ticks. If the code is honest, the result is the same. If someone later introduces hidden randomness by mistake, replay will show a different result, and the automated test for that will fail.

**Digest.** A fingerprint of the whole log: a string of letters and numbers computed from every line. If one character of one line differs, the digest differs. It is how the tests compare two logs without printing them, and it is what `replay` prints so you can compare a rebuilt voyage with the original at a glance.

**Log marks.** A line starting with a space is routine. `*` is notable (a wind shift, a completed evolution later on). `!` is urgent (nothing produces it yet; carrying away a spar will).

**Bells.** Eight bells end a watch. The dog watches are split: the first dog watch runs one, two, three bells; the last dog watch strikes four at its start, then one, two, three, and eight at 20:00. This is the Royal Navy convention of the period; say if you would prefer plain one-to-eight.

## Not in this milestone

- No sails, rigging, physics or crew. `speed 6 knots` is an order the point ship obeys directly; a real ship will get its speed from the wind in milestone 1.
- No browser window. The map, profile and log panels arrive in milestone 2.
- The Orders language is not present yet; `steer`, `speed` and `stop` are parsed by hand and will be replaced.
- No world: the ship sails on an endless flat plane and positions are metres from where it started.

## What to report back

- Pass or fail for each of the ten items. For a fail, what you typed and what you saw, pasted or photographed.
- Anything in the voice of the log that reads wrongly to a sailor's ear.
- Whether the setup steps were clear enough, and where you hesitated.
