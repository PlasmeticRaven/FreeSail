# 7. A first passage

An hour and a quarter at sea on each ship, that you can type along with. The logs are from seed 7 with a north wind of 15 knots and the physics as package 10 tuned it; type exactly what is in the blocks and yours will match. Where a number is quoted, yours may differ by a few tenths.

## The frigate *Amazon*, morning watch

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

She lies with her head west-north-west, the wind on her starboard bow six points off, nothing set and no way on her. Look at her, then make plain sail and brace up for the tack she is on, both at once, and give her eight minutes:

```orders frigate
state
set plain sail
brace sharp up on the starboard tack
tick 480
state
```

```
Amazon: heading WNW (293°), speed 0.0 kn, leeway 0°, heel 0°
Apparent wind 0° on the starboard bow, 0.0 kn; helm +0°
Sail set: none
  Morning watch, 8 bells (04:00)  Order: set plain sail.
  Morning watch, 8 bells (04:00)  Order: brace sharp up on the starboard tack.
  Morning watch (04:00)  Hands to the spanker halyards and outhaul.
* Morning watch (04:00)  Braced the fore yard; 55° from square.
* Morning watch (04:00)  Braced the fore topsail yard; 58° from square.
  ...
* Morning watch (04:01)  Set the fore topmast staysail.
* Morning watch (04:01)  Set the jib.
* Morning watch (04:03)  Set the spanker.
* Morning watch (04:03)  Set the foresail.
* Morning watch (04:03)  Set the mainsail.
* Morning watch (04:05)  Set the fore topsail.
* Morning watch (04:05)  Set the main topsail.
* Morning watch (04:05)  Set the mizzen topsail.
* Morning watch (04:05)  Set the fore topgallant.
Advanced 480 ticks to Morning watch (04:08).
Amazon: heading WNW (296°), speed 2.8 kn, leeway -11°, heel -3°
Apparent wind 52° on the starboard bow, 13.1 kn; helm -7°
```

Twelve yards braced and eleven sails set in five minutes, and three minutes after the last of them she has 2.8 knots and is still gathering way, her head held off a little by the helm while she does. There is no *Taken aback* line: she neither rounds up nor gathers sternway getting under way (truth 17 of the tuning notes). Give her five minutes more, then trim her to the wind with the order the owner asked for at gate M1:

```orders frigate plain-sail
tick 300
state
trim sails
tick 120
state
```

```
Advanced 300 ticks to Morning watch (04:13).
Amazon: heading WNW (293°), speed 4.6 kn, leeway -4°, heel -3°
Apparent wind 49° on the starboard bow, 14.4 kn; helm -1°
  Morning watch (04:13)  Order: trim sails.
  Morning watch (04:13)  Braced 12 yards to the wind, 49° on the starboard bow; trimmed the sheets of the mizzen spanker; the fore topmast staysail; the jib.
* Morning watch (04:13)  Braced the fore yard; 55° from square.
  ...
Advanced 120 ticks to Morning watch (04:15).
Amazon: heading WNW (293°), speed 4.7 kn, leeway -4°, heel -3°
Apparent wind 49° on the starboard bow, 14.2 kn; helm -1°
```

Close-hauled on the starboard tack at a little under five knots: 49° apparent is six points true (chapter 2), four degrees of leeway, three of heel to larboard, and a degree of weather helm (chapter 4). `trim sails` found every yard already at its limit, which is where the wind at 49° wants them, so nothing moved; it is the order to give after a tack or a shift of wind. This is the ship at her best point for working to windward, and the slowest she will go anywhere but dead before the wind.

Feel a rope, watch the watch put it back, then go about:

```orders frigate plain-sail
haul the spanker sheet
tick 60
ease the spanker sheet a fathom
tack ship
tick 720
state
```

```
  Morning watch (04:15)  Hauled the mizzen spanker sheet; the mizzen spanker now 19° off the centreline.
Advanced 60 ticks to Morning watch (04:16).
  Morning watch (04:16)  Eased the mizzen spanker sheet; the mizzen spanker now 29° off the centreline.
  Morning watch (04:16)  Order: tack ship.
  Morning watch (04:16)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:16)  All hands about ship.
* Morning watch (04:16)  Fore course taken aback.
* Morning watch (04:16)  Main course taken aback.
  Morning watch (04:17)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:18)  Let go and haul.
* Morning watch (04:21)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:22)  Steady on ENE (68°).
Advanced 720 ticks to Morning watch (04:28).
Amazon: heading ENE (67°), speed 5.1 kn, leeway 4°, heel 4°
Apparent wind 49° on the larboard bow, 15.5 kn; helm +1°
```

The spanker was sheeted to 24° for the wind; you hauled it to 19°, and in the minute before you eased it the watch had eased it back to 24° themselves, so your fathom took it to 29° (chapter 4). Chapter 5 reads the tack line by line: five minutes to *Tacked*, and twelve minutes after the order she is back at five knots on the other tack. Leeway, heel and helm have all changed sign: the lee side is now starboard.

Haul a brace to feel it, wear her back onto the starboard tack, and, once she is round, take a reef in the topsails against the freshening breeze:

```orders frigate plain-sail larboard
haul the weather main brace
wear ship
tick 900
state
reef the topsails, one reef
tick 500
state
```

```
  Morning watch (04:28)  Hauled the larboard (weather) main brace; the main yard now braced 50° for the larboard tack.
  Morning watch (04:28)  Order: wear ship.
  Morning watch (04:28)  Stand by to wear ship. Up helm; brace in the after yards.
  Morning watch (04:28)  Stations for wearing ship.
  Morning watch (04:29)  Wind aft. Squared the head yards; hauled out and braced up.
  Morning watch, 1 bell (04:30)  1 bell.
* Morning watch (04:30)  Fore topgallant taken aback.
  Morning watch (04:32)  Main topsail filled again.
* Morning watch (04:37)  Wore ship; braced sharp up on the starboard tack, heading WNW (293°).
  Morning watch (04:37)  Steady on WNW (293°).
Advanced 900 ticks to Morning watch (04:43).
Amazon: heading WNW (293°), speed 5.4 kn, leeway -4°, heel -4°
Apparent wind 49° on the starboard bow, 16.5 kn; helm -1°
  Morning watch (04:43)  Order: reef the topsails, one reef.
  Morning watch (04:43)  All hands reef the fore topsail.
  Morning watch (04:44)  Settled the fore topsail halyards and clewed down; hauled out the reef tackles.
  Morning watch (04:47)  A gust: 17 knots.
  Morning watch (04:47)  Laid out and passed the earings of the fore topsail.
* Morning watch (04:49)  Reefed the fore topsail; now set, 1 reef.
Advanced 500 ticks to Morning watch (04:51).
Amazon: heading WNW (293°), speed 5.3 kn, leeway -4°, heel -4°
Apparent wind 50° on the starboard bow, 16.8 kn; helm -1°
```

On the larboard tack the weather main brace was the larboard one. Nine minutes from *Stand by to wear* to *Wore ship*, and she came round with the yards following the wind and lost a sixth of a mile to leeward doing it. A reef takes six minutes and a tenth of a knot.

Heave to, watch her ten minutes, fill away, set again what heaving to took in, and save the voyage:

```orders frigate plain-sail
heave to
tick 600
state
fill away
tick 400
state
set the courses
set the spanker
tick 300
state
save voyage.json
replay voyage.json
quit
```

```
  Morning watch (04:51)  Order: heave to.
  Morning watch (04:51)  Hauled up the courses; brailed up the spanker.
  Morning watch (04:51)  Clewed up the fore topgallant.
  Morning watch (04:51)  Braced the main topsail aback; helm a-lee.
* Morning watch (04:52)  Hove to, main topsail to the mast, helm a-lee.
  Morning watch (04:52)  A gust: 25 knots.
Advanced 600 ticks to Morning watch (05:01).
Amazon: heading NW by W (298°), speed 1.4 kn, leeway -44°, heel -4°
Apparent wind 56° on the starboard bow, 14.2 kn; helm +15°
Sail set: fore.topsail, main.topsail, main.topgallant, mizzen.topsail, mizzen.topgallant, fore.topmast_staysail, jib
  Morning watch (05:01)  Order: fill away.
  Morning watch (05:01)  Hauled aft the head sheets; kept the helm a-lee to let her fall off.
  Morning watch (05:01)  Braced the main topsail full.
* Morning watch (05:02)  Filled away; braced full and steering WNW (293°).
  Morning watch (05:03)  Steady on WNW (293°).
Advanced 400 ticks to Morning watch (05:08).
Amazon: heading WNW (293°), speed 4.2 kn, leeway -5°, heel -3°
Apparent wind 52° on the starboard bow, 14.7 kn; helm +6°
* Morning watch (05:11)  Set the spanker.
* Morning watch (05:11)  Set the foresail.
* Morning watch (05:11)  Set the mainsail.
Advanced 300 ticks to Morning watch (05:13).
Amazon: heading WNW (295°), speed 3.8 kn, leeway -5°, heel -3°
Apparent wind 50° on the starboard bow, 13.6 kn; helm -3°
Saved to voyage.json at tick 4380.
Replaying voyage.json to tick 4380...
Replayed. Log digest 07d5978d56b0eb4c. Clock held.
```

Hove to she lies five points off the wind making a knot and a half, half of it sideways, and holds so through a 25-knot gust; filled away she is steady on her course in two minutes and has four knots seven minutes after the order, with no *Taken aback* line (chapter 5). The courses and spanker come back in three minutes, and she is a little slower for the moment while the breeze eases. The replay must print the same state as the one before the save, to the last digit, and the log digest in yours must be the one above.

## The schooner *Speedwell*, morning watch

```
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
```

Same wind, head north-west by west. Her sails have different names and different evolutions under them, and the language does not change:

```orders schooner
state
set plain sail
brace sharp up on the starboard tack
tick 900
state
```

```
  Morning watch (04:00)  Hands to the foresail halyards and outhaul.
  Morning watch (04:00)  Hands to the mainsail halyards and outhaul.
  Morning watch (04:00)  Hands aloft to loose the fore topsail.
  Morning watch (04:00)  Clear away the jib; man the halyards.
* Morning watch (04:00)  Braced the fore topsail yard; 58° from square.
  Morning watch (04:01)  Cast off the gaskets and cleared away the brails of the foresail.
* Morning watch (04:01)  Set the fore staysail.
* Morning watch (04:01)  Set the jib.
* Morning watch (04:03)  Set the foresail.
* Morning watch (04:03)  Set the mainsail.
* Morning watch (04:05)  Set the fore topsail.
* Morning watch (04:05)  Set the fore topgallant.
Advanced 900 ticks to Morning watch (04:15).
Speedwell: heading NW by W (300°), speed 5.7 kn, leeway -4°, heel -7°
Apparent wind 40° on the starboard bow, 15.0 kn; helm +1°
Sail set: fore.topsail, fore.topgallant, fore.sail, main.sail, fore.staysail, jib
```

Two gaff sails, two headsails and two square sails on the fore, and she lies almost a point nearer the wind than the frigate (40° apparent, 60° true) at nearly six knots. Give her the gaff topsail and try to go about:

```orders schooner plain-sail
set the gaff topsail
tick 300
state
tack ship
wear ship
tick 900
state
```

```
* Morning watch (04:17)  Set the gaff topsail.
Advanced 300 ticks to Morning watch (04:20).
Speedwell: heading NW by W (300°), speed 5.8 kn, leeway -4°, heel -9°
Apparent wind 40° on the starboard bow, 15.0 kn; helm -4°
  Morning watch (04:20)  Order not carried out ('tack ship'): She is not close-hauled; bring her by the wind before going about.
  Morning watch (04:20)  Order: wear ship.
  Morning watch (04:20)  Stand by to wear ship. Up helm; brace in the after yards.
  Morning watch (04:21)  Wind aft. Squared the head yards; hauled out and braced up.
* Morning watch (04:22)  Fore topsail taken aback.
  Morning watch (04:25)  Fore topsail filled again.
* Morning watch (04:28)  Wore ship; braced sharp up on the larboard tack, heading ENE (68°).
  Morning watch (04:28)  Steady on ENE (68°).
Advanced 900 ticks to Morning watch (04:35).
Speedwell: heading ENE (68°), speed 7.8 kn, leeway 3°, heel 15°
Apparent wind 44° on the larboard bow, 18.1 kn; helm +7°
```

The refusal is a known fault, not seamanship: she *is* close-hauled, but the runner judges it by her square topsail, which wants ten degrees more wind than her gaff sails do (chapter 5, and `docs/dev/TuningNotes.md`). Wear her instead: eight minutes, and she comes up on the larboard tack a knot faster in a freshening breeze. Now bear away to a reach, ease the main sheet, reef the mainsail, and heave to with the fore topsail to the mast:

```orders schooner plain-sail larboard
steer east
tick 300
state
ease the main sheet a fathom
reef the mainsail, one reef
tick 400
state
heave to
tick 600
state
fill away
tick 400
state
# rejected: set the mizzen topsail
quit
```

```
  Morning watch (04:35)  Helm ordered: steer E (90°).
  Morning watch (04:36)  Steady on E (90°).
Advanced 300 ticks to Morning watch (04:40).
Speedwell: heading E (90°), speed 8.5 kn, leeway 2°, heel 12°
Apparent wind 57° on the larboard bow, 15.7 kn; helm +6°
  Morning watch (04:40)  Eased the main sail sheet; the main sail now 37° off the centreline.
  Morning watch (04:40)  Hands to reef the mainsail.
  Morning watch (04:41)  Settled the mainsail halyards.
  Morning watch (04:45)  Hauled out the reef earing of the mainsail and tied the points.
Advanced 400 ticks to Morning watch (04:46).
Speedwell: heading E (91°), speed 8.2 kn, leeway 2°, heel 11°
Apparent wind 59° on the larboard bow, 15.4 kn; helm +3°
  Morning watch (04:46)  Order: heave to.
  Morning watch (04:46)  Braced the fore topsail aback; helm a-lee.
* Morning watch (04:46)  Reefed the mainsail; now set, 1 reef.
* Morning watch (04:47)  Hove to, fore topsail to the mast, helm a-lee.
  Morning watch (04:52)  A gust: 25 knots.
* Morning watch (04:52)  Main topmast bending like a whip; she will carry it away if sail is not shortened.
Advanced 600 ticks to Morning watch (04:56).
Speedwell: heading NE (49°), speed 3.9 kn, leeway 11°, heel 13°
Apparent wind 37° on the larboard bow, 16.4 kn; helm -15°
  Morning watch (04:56)  Order: fill away.
  Morning watch (04:56)  Hauled aft the head sheets; kept the helm a-lee to let her fall off.
  Morning watch (04:56)  Fallen off; braced the fore topsail full.
* Morning watch (04:58)  Filled away; braced full and steering ENE (67°).
Advanced 400 ticks to Morning watch (05:03).
Speedwell: heading ENE (67°), speed 7.1 kn, leeway 3°, heel 12°
Apparent wind 44° on the larboard bow, 16.8 kn; helm +2°
  Morning watch (05:03)  Order not carried out ('set the mizzen topsail'): There is no such part as the mizzen topsail in this ship; did you mean the topsails, the mainsail or the gaff topsail? ('set' was understood.)
```

Four things to notice. Bearing away from 68° to east she goes from 7.8 to 8.5 knots, the apparent wind draws aft from 44° to 57°, and the watch eased the sheets for you: your `ease the main sheet a fathom` found the boom already 32° off and took it to 37°. The 25-knot gust with her gaff topsail still set loads her main topmast past its rating, and the log says so (chapter 6): shorten sail or lose the spar. The schooner does not lie to: with only one small square sail to lay aback against two big gaff sails she keeps four knots of way with her head coming up to four points off, which is not hove to; a schooner is properly hove to by hauling a head sheet to windward, an evolution the game has not got (chapter 5). And the last line is the ship refusing a sail she has not got, and suggesting the ones she has.

## Standing orders: the ship keeps herself

A standing order is an order like any other, given at the prompt and journaled, with a trigger in front of it: *when* a reading holds (for a while, if you say so), *at* an event, or *every* interval. When it fires, the log says which order fired and what it did, and nothing happens that the log does not explain. The words a condition may test are the ship's own readings, the same ones `state` shows: the true wind, the apparent wind, the heading, the speed, the heel, the watch, daylight, a sail by name, the strain, the hands on deck. The starter routines come with the game in `data/standing_orders/starter.orders`; here they are, given one at a time on the frigate before the wind (`--heading 180`, so the studding sails will draw), with the book's own orders after them:

```orders frigate all-sail
standing order "night routine": at sunset then take in the studdingsails; take in the royals
standing order "morning sail": at sunrise, if the true wind is under 20 knots then set the royals
standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef
standing order "keep her full": when the apparent wind is forward of 55 degrees then bear away one point
standing order "trim on a shift": when the true wind veers 1 point or backs 1 point then trim sails
standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then send down the topgallant masts; shift the fore topmast staysail for the fore storm staysail; close reef the topsails
# rejected: standing order "sound the well": every glass then sound the well
standing orders
show standing order "keep her full"
belay standing order "keep her full"
resume standing order "keep her full"
belay all standing orders
strike standing order "heavy weather"
# rejected: show standing order "heavy weather"
# rejected: standing order "night routine": at sunset then take in the royals
standing order "glass": when the glass is falling fast then shorten sail
# rejected: standing order "x": at sunset then set the royls
```

Belaying an order keeps it in the book, idle, until you resume it; striking it (`strike standing order "x"`, or `cancel` or `remove`) takes it out of the book altogether, and its name may be given again. The well one is refused until the ship has a well to sound, and the refusal says so; the glass is a reading since milestone 5 (chapter 9), so a rule on it is a book's line in any ship, and in one that carries no glass it simply never fires; a second order of a name already in the book is refused; a misspelt sail is refused when the order is given, not on the night it fires. The whole file loads in one line at the prompt, `read the standing orders from data/standing_orders/starter.orders`, or at the start with `--standing-orders data/standing_orders/starter.orders`; each line is given as an order, and the refused one does not stop the rest.

To see one fire, sail her to sunset. At seed 7 with the wind north 15 knots and her head south, under all sail with the studding sails set as chapter 3 sets them (`make all sail`, then `rig out the studdingsails, both sides` and `set the studdingsails, both sides`), give the night routine and `tick 56000`; `state` on the way says where the sun stands:

```
Day. Sunrise 03:56, sunset 19:58; civil twilight from 03:13 and until 20:41.
Amazon: heading S (180°), speed 6.5 kn, leeway 0°, heel 0°
...
* Last dog watch (19:59)  Sunset.
* Last dog watch (19:59)  By standing order 'night routine': taking in the studdingsails.
* Last dog watch (19:59)  By standing order 'night routine': taking in the royals.
```

The "By standing order" line is notable and stands in for the "Order:" line a captain's order gets; what follows it is the hands' ordinary work. `standing orders` afterwards reads `"night routine" (the captain): at sunset then take in the studdingsails; take in the royals. Standing; fired once, last at Last dog watch (19:59).` An order the ship cannot carry out when it fires is refused in the log's words too: `Standing order 'morning sail' at sunrise: not carried out; the true wind is 25 knots, not under 20 knots.` for a failed `if`, and `Standing order 'x': order not carried out ('take in the royals'): Nothing done: the fore royal is already furled; ...` for an order the ship refuses.

Three guards keep a standing order from thrashing. A duration debounces: `for 2 minutes` means the wind has been over thirty for two minutes of ship's time together, so the console's gusts, which last seconds, never fire it. A `when` order fires once, on the edge, and not again until its condition has been false for five minutes and the work it started has ended; `keep her full` bears away a point and then waits. `trim on a shift` shows the edge at work on the wind's direction: `veers 1 point or backs 1 point` is measured from the wind as it was when the order last stood, and once fired it measures afresh, so a wind that veers from west to north-west through a night has the yards trimmed to it point by point, five minutes at least apart. A gust does not move the wind's direction, so it never fires it; and a trim the watch is still at is not stacked behind: a yard still waiting its turn takes the new angle, and the log says the yards are being trimmed already. And two orders that lay hands on the same part within those five minutes are settled by rank: the captain's stands over the master's, and the log says `Standing order 'royals' (the master) countermanded by 'royals in' (the captain).`; two of the captain's own give the later the day, with a plain note.

The same rules can be written in Python, for a script rather than the prompt, and they are the same rules: the decorators build the same order, enter it in the same book, and the log reads the same to the letter. Bind a world first; the body runs once as the rule is entered and may only call `order(...)` with the words you would have typed.

```python
from freesail.standing import bind, when, at, order

bind(world)

@at("sunset", name="night routine")
def night_routine():
    order("take in the studdingsails")
    order("take in the royals")

@when("the true wind exceeds 30 knots", for_minutes=2, name="shorten sail for weather")
def shorten_sail():
    order("take in the studdingsails")
    order("take in the royals")
    order("reef the topsails, one reef")
```

A saved game lists a Python rule by its name and its source; loaded without the script that defined it, the rule is in the book, belayed, and `resume` says why it will not run.

## A day of it, and a word with the watcher

`data/scenarios/gate-4c-day.yaml` is a whole day under standing orders, the wind scripted to veer and rise to a gale in the middle watch and ease at the next dawn: start it with `--scenario data/scenarios/gate-4c-day.yaml` on the console or the browser server, and run it at `speed 60` or `speed 300`, where the log rolls up each hour's routine lines into one line (marked `=`) and keeps every notable and urgent line as it is; an urgent line eases the clock to 1x and says so. With a watcher at its station, `ask the watcher how the sails are drawing` puts a question it answers in the log, and `tell the watcher we make for Falmouth` (or `say to the watcher ...`) gives it a word it hears and owes no answer to.
