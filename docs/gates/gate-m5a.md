# Gate M5a: The sea and the sky

**Verdict:** pending.

**As cut:** package 30 (weather systems, the glass and the sky, the scenario's systems, the gate's day as a system), 30b (clearing a wreck, spare spars, the storm mizzen in the viewer, two result strings) and 31 (the sea and the ship's motion, windage under bare poles, the day under systems alone). Two items are carried from gate 4c and count for both: `--load` of a save with a station (item 8) and a watcher through Claude Code, which item 6 may be run with instead of the local runner. The report for this gate is your playtest, on the form in `docs/playtests/README.md`: the items below are the day to sail and what to look for; the form is what you write. Three rulings are asked of you (item 10).

## Headline

Milestone 5a claims (spec M5 §1): *the wind has a cause the captain can read from the glass and the sky before it arrives, and a seaway that the hands aloft and the hull feel. The gate's day of 4c is sailed again under a system instead of a script, the readings the watcher of playtest 7 asked for are there, and nothing in it names a front or a centre.*

1. **Weather that comes from somewhere.** A scenario gives its weather as pressure systems (a low with its two fronts, a high, a background) that move along a track, or seeds a month's systems from a climatology; the wind at the ship is the surface wind those systems make, with the gust factor by the air the ship is in, squalls behind a cold front, and the direction's wander about it. The pinned `wind` of milestone 4 is still there as a second form and is what every truth is measured on; the gate's day now exists in both (`data/scenarios/gate-4c-day.yaml`, both forms, the pinned wind winning; `data/scenarios/gate-5a-day.yaml`, the systems alone).
2. **The glass, the sky, the weather and the visibility as readings** in the period's words: the glass in inches to the hundredth with its tendency over three hours (steady, rising, falling, falling fast), Beaufort's words for the sky with Luce's signs, the weather (rain, drizzle, passing showers, squally, fog), how far a sail can be seen. The log says them by the hour and at the change of the watch, and the standing orders read them for nothing (`when the glass is falling fast then shorten sail`). No line names a front, a centre, an isobar or a hectopascal.
3. **The sea and the ship's motion.** The sea at the ship is raised by the wind's ten-minute mean and outlasts it; a low leaves a swell behind it; the words are the period's (a smooth sea, a short chopping sea, a heavy sea, a long swell from the westward, a confused sea) and never a number. The ship rolls, pitches and heaves in it as three reduced quantities with their words (easy, rolling heavily, pitching into it, labouring heavily), and the hands and the gear feel it: a reef in a heavy sea takes half as long again, the spars and the gear are judged harder in a seaway, a head sea costs speed, the glass pumps. Nothing of it moves the ship on the plane.
4. **The day under systems alone.** The same day, the same standing orders, no pinned wind: the frigate scuds through the gale in a very heavy sea; the squalls of the cold air cost her the close-reefed mizzen topsail and the main topsail's brace and sheet; the sea is a heavy sea until the afternoon.

Six truths (52 to 57) were added; all pass. The windage under bare poles (M4 open item 7) was measured against the sources and not moved: the measurement and the reason come to you as a ruling (item 10).

## What you need

As before: Python 3.11 or newer (`py`) and the gate zip extracted to a fresh folder. For a real watcher, what gate 4b-3 needed for the door you choose (`docs/agents/Harness.md`); item 6 asks for the local runner.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server,agents]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest -n 4
```
*Ends `1712 passed, 7 xfailed` (the build machine: about eleven minutes on four workers). The seven expected failures are your earlier rulings (truth 3 for the schooner, truth 11's ground, truth 18's times, and truths 24, 26, 28 and 31). A `failed` is a fault. The gate's day runs in it twice: pinned (truths 48 to 51) and under systems (truth 56 and the day's own constants).*

## The day

**The scenario.** `data/scenarios/gate-5a-day.yaml`, seed 7 (the file's): the frigate at 04:00 on 1 June 1805, 50 N, heading south-east, plain sail and the royals ordered at four, her captain's glass aboard. The weather is three systems and a background, and nothing else: "the low" passing well north of Falmouth with the ship in its warm sector all day (W by N, 17 to 19 knots), the cold front through at ten in the evening (the wind veering to NW by N with squalls), the gale in the cold air behind it (45 to 48 knots from midnight to three), "the ridge" from the Atlantic bringing the ease by dawn (18 knots by seven) and the clearing. The old high over Biscay gives the glass its height at the start. Every waypoint has its reason in `gate-4c-day.yaml`, which carries the same systems beside the pinned wind.

**The standing orders.** The starter routines and the captain's three for the passage (`data/scenarios/gate-4c-day.orders`), as at gate 4c.

**The watcher.** The scripted one (`--watcher fake`) for items 1 to 5; a real one through the local runner for item 6, or through Claude Desktop or Claude Code if you prefer (`docs/agents/Harness.md` §3 to §5).

## Items

- [ ] **1. Start the day in the browser.**
  ```
  py -m freesail.ui.server --scenario data/scenarios/gate-5a-day.yaml --watcher fake
  ```
  *The terminal prints `Scenario: The gate's day under systems (data/scenarios/gate-5a-day.yaml).`, then `The systems (the wind, the sky and the glass):` and three lines naming them (the author's view: this is the only place the low is named), `She carries a glass.`, `The sea and the ship's motion are kept.`, then `FreeSail server. Seed 7. Open http://127.0.0.1:8000/`.* Open it. *The log opens `The gate's day under systems. Wind W, 18 knots, a fresh breeze. Heading SE (135°).`; the instruments show a Glass row (`30.01 in`, and after an hour its tendency), a Sky row (`hazy; drizzle; a few miles`) and a Sea row (`a moderate sea from the westward; easy`, then `rolling easily` as she gathers way).* Type `state` in the order box: *the weather's two lines among the ship's: `The glass 30.01; hazy, drizzle; a few miles.` and `A moderate sea from the westward; easy.`*

- [ ] **2. The glass at every watch change, the sky at every bell.** Press **60x**. *At each hour a routine line `Hazy, drizzle; the glass 30.01; a short chopping sea, rolling.` (the sky, the weather, the glass, the sea, the motion), and at 08:00, the change of the watch, `..., fallen a hundredth since the morning watch` or `steady since ...`; in the roll-up each hour's line carries the same. The sky's changes as their own lines (`The sky overcast.`, `Drizzle.`, `The weather cleared.`).* Type `the glass` questions as standing orders to see the dialect read it: `standing order "glass": when the glass is falling fast then take in the royals` and `standing orders`: *the order enters the book; it fires in the evening (item 4).* Say in the form whether the glass's words and the tendency's are a barometer as you would read one.

- [ ] **3. The sea's words.** Watch the Sea row and the log through the forenoon at 60x: *`A short chopping sea getting up.` at 05:04, then the motion's lines as she rolls with the sea on her quarter (`Rolling.`, `Rolling easily.`; the words hold five minutes before the log says they changed).* Type `standing order "sea": when the sea is heavy then tell the watcher the sea is getting up` (a line the dialect takes; it fires at 20:45). Say in the form whether "a short chopping sea" is the sea a fresh breeze of a day makes in the Channel.

- [ ] **4. 300x: the evening, the front and the gale.** Press **300x**. *What to look for, at seed 7 with the scripted watcher (a real watcher changes the log's lines, not the ship):*
  - *19:50 `Sunset.` and the night routine's royals.*
  - *20:45 `A heavy sea getting up.` as the wind passes a strong breeze; 21:33 `By standing order 'shorten sail for weather': taking in the topgallants.` and the one reef; 21:57 `Rolling heavily.`; from 22:54 `Labouring heavily.` and `Rolling heavily.` by turns as the sea comes onto the quarter.*
  - *From about 22:00 the wind veers with the cold front, `Wind veered to ...` lines as it hauls to the north-west; 23:11 the captain's `gale canvas`; 00:06 `Rain set in.`, 00:51 `Squally.`; 00:37 the heavy-weather routine, its four orders on one tick, the close reef taken.*
  - *01:17, in the middle watch: `A squall: the wind veers 2 points to NW by N and freshens to 65 knots, with rain.` and on the same second `! Mizzen topsail split and blew out of the bolt-ropes.`, then `! Larboard main topsail yard brace parted; the main topsail yard swung round to the wind.` and `! Larboard main topsail sheet parted; the main topsail flogging itself to ribbons.`; the clock eases to 1x on the first (`Compression eased to 1x: ...`). Press 300x again. `The squall passed; the wind NW, 47 knots.` at 01:21; squalls at 01:37 (67 knots), 02:13, 03:04 and 03:55, each ended in the log; `Wind backed to NW by W, a fresh gale.` at 02:36 as the ridge comes.*
  - *01:51 `A very heavy sea getting up.`; 01:04 and again from 04:26 `Pitching heavily, the sea under her stern.` as she scuds with the sea right astern.*
  - *The glass: 29.90 at 21:00, 29.71 at midnight (`fallen 22 hundredths since the first watch`), 29.74 at three, 29.98 at six, 30.11 at nine; the tendency `falling fast` from ten in the evening to one, `rising` at three, `rising fast` from four.*
  - *03:40 `Sunrise.`; the sky `Detached clouds, hard-edged and oily-looking, passing showers` at three and `Clear, fine` by six.*
  - *08:14 `By standing order 'make sail after the gale': ...` four orders; 08:22 `A heavy sea, the sea going down.`; at nine the hour's line still says `a heavy sea, pitching heavily, the sea under her stern` with the wind a fresh breeze since seven (truth 56: the sea outlasts the gale by hours).*

  Press **hold** after nine. Say in the form what the squalls and their cost read like, and whether the sea's and the motion's lines are the right number of lines for a night.

- [ ] **5. Save, replay, load.** In the same game, `save day.json`: *`Saved to day.json at tick <N>; the log's digest is <sixteen characters>.`* Stop the server (Ctrl-C). Replay in the console: `py -m freesail.ui.console`, `replay day.json`: *`Replayed. Log digest <the same sixteen characters>. Clock held.` The sea and the motion are raised again from the wind; nothing of them is saved.* Then `--load` (carried from gate 4c, item 8):
  ```
  py -m freesail.ui.server --load day.json --watcher fake
  ```
  *`Loaded day.json: replayed to tick <N>, <the ship's time>; the log's digest is <the same>.`; the watcher at its station in the instruments; press go and the day goes on.*

- [ ] **6. The watcher asked what the glass says.** A fresh game (item 1's command without `--watcher fake`), a model connected through the local runner (`docs/agents/Harness.md` §5; Qwen3.8 27B as at gate 4c, or the model you have), run at 60x into the evening. Type `ask the watcher what does the glass say, and what do you make of it`. *A notable `[watcher] ...` answer that reads the glass's height and its tendency from the readings (it has `the glass`, `the tendency`, `the sky`, `the weather`, `the visibility`, `the sea` and `the motion` in every sample) and says what a seaman would: a falling glass and a backing wind, shorten sail. What it says beyond that is the form's to judge.* Then, in the gale, `ask the watcher how is she taking the sea`.

- [ ] **7. Two days from the climatology.** Two scenario files are a few lines each; write them in the extracted folder:
  ```
  name: A January day
  seed: 7
  start: 1805-01-10T04:00
  ship: {file: data/ships/frigate-36.yaml, heading_deg: 135, glass: true}
  weather: {climatology: true}
  standing_orders: [data/standing_orders/starter.orders]
  orders: [set plain sail]
  ```
  and the same with `start: 1805-07-10T04:00` and `name: A July day`. Run each in the console at `speed 300` for a day (`py -m freesail.ui.console --scenario january.yaml`, `go`, `speed 300`; `hold` after 04:00 next day). *The terminal's first lines say `The weather from the climatology for January.` and the systems drawn (by name: a low, a high); the day's wind, glass, sky and sea follow from them. At seed 7 the January day and the July day differ in the way the table says they should: more wind and a lower glass in January, more hazy and fine in July.* Then the month's shares:
  ```
  py tools/climatology_check.py --months 1000 --seed 7
  ```
  *A table of twelve months: the westerly and easterly shares within five points of the study's in every month (truth 53), the strong-breeze days beside Ushant's.* Say in the form whether the two days read as winter and summer in the Channel.

- [ ] **8. The pinned day still holds.** `py -m pytest tests/test_known_truths.py -k "truth_48 or truth_49 or truth_50 or truth_51 or truth_52" -n 4`: *`6 passed`* (truth 48 is two tests). The pinned day's ticks did not move with the sea (the sea is not kept under a pinned wind); the day under systems has its own (`test_the_day_under_systems_alone_at_seed_7_has_its_own_constants`).

- [ ] **9. The console at the same speeds** (optional): `py -m freesail.ui.console --scenario data/scenarios/gate-5a-day.yaml --watcher fake`, `go`, `speed 300`: *the roll-up lines start with `=` and carry the sea by the hour; `state` prints the two weather lines.*

- [ ] **10. Rulings wanted.**
  - **The pinned form and the air-mass rule** (spec M5 §3 as built). Under a fixed or a pinned wind the gusts are still milestone 2's draws (1.1 to 1.5 whatever the mean, so the pinned gale gusts to 67), and every truth from 1 to 51 is measured so; under the systems the gust factor is drawn by the air mass (1.10 to 1.30) and the top of the unstable range, 1.30 to 1.45, is a squall the log names (the 65 of item 4). Rule whether the pinned form should also take the air-mass rule, which would re-measure truths 48 to 51 and their digest, or stay as the fixture it is.
  - **Windage under bare poles** (M4 open item 7). The frigate under bare poles in fifteen knots dead astern makes 2.9 knots, and lying a-hull with the wind abeam drifts half a knot to leeward; in a strong gale 8 and 2.7. The rig's windage was measured and not moved: the numbers, the arithmetic and the sources (Steel 1794 on running half a league under bare poles; Falconer on scudding under bare poles; Luce on lying to, "drifting bodily to leeward") are in `docs/dev/TuningNotes.md`, M5a. Rule whether the running figure stands, or whether the spars' shielding of one another with the wind on the axis (a fifth at most, to about two and a half knots) should be added.
  - **The sea's cost.** The day under systems loses the close-reefed mizzen topsail and the main topsail's brace and sheet in the first squall of the middle watch (a 65-knot squall on a 45-knot gale, the sea's extra load on the gear about a tenth). Rule whether that is the night a frigate shortening sail in time should have, or whether the squalls should be capped lower for the gate's day (the gust factor's top, spec M5 §3) or the seaway's load eased.

## The report

Fill `docs/playtests/README.md`'s form in a new folder, `docs/playtests/<date>-gate-5a-<the watcher>/notes.md`, with `day.json` beside it (the ship's path made relative). Any number a sailor would call wrong (section 7): the sea's height is never printed, so the words are what to judge, and the tuning notes give the metres behind them.

## What this gate does not do

- **The coast** (5b): no sea breeze, no coastal fog, no horizon read by anything; the hooks are inert.
- **Pitch and roll on the plane**: nothing here moves the ship by her motion; no six-degree body, no wave-by-wave motion (spec M5 §4).
- **The temperature** (deferred until something reads it).
- **The glass's check at the cold front** (open item 8 of spec M5 §33): the pressure at the ship is a sum of bells, and a frontal trough would give it.
