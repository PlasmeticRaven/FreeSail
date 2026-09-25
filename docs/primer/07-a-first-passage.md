# 7. A first passage

Two hours at sea, one on each ship, that you can type along with. The logs are from seed 7 with a north wind of 15 knots; type exactly what is in the blocks and yours will match until the gusts begin to differ from what the tuning changes. Where a number is quoted, yours may differ by a few tenths.

## The frigate *Amazon*, morning watch

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

She lies with her head west-north-west, the wind on her starboard beam and a little forward of it, nothing set. Look at her:

```orders frigate
state
set the fore topsail
tick 360
state
```

```
Amazon: heading WNW (293°), speed 0.0 kn, leeway 0°, heel 0°
Apparent wind 0° on the starboard bow, 0.0 kn; helm +0°
Sail set: none
  Morning watch, 8 bells (04:00)  Order: set the fore topsail.
  Morning watch (04:00)  Hands aloft to loose the fore topsail.
  Morning watch (04:01)  Laid aloft and loosed the fore topsail.
* Morning watch (04:05)  Set the fore topsail.
Advanced 360 ticks to Morning watch (04:06).
Amazon: heading W (271°), speed 1.2 kn, leeway -163°, heel -1°
Apparent wind 94° on the starboard bow, 12.1 kn; helm -21°
```

Five minutes to set one topsail, and with the yards square it has driven her nowhere: she has drifted, swung to west and is going astern (leeway 163°). A topsail alone with a square yard is not a way of sailing; it was a way of seeing an evolution run. Now make sail properly and brace up for the tack she is on:

```orders frigate
set plain sail
brace sharp up on the starboard tack
tick 900
state
```

```
  Morning watch (04:06)  Order: set plain sail.
  Morning watch (04:06)  Order: brace sharp up on the starboard tack.
  Morning watch (04:06)  Hands aloft to loose the foresail.
  ...
* Morning watch (04:06)  Braced the fore yard; 55° from square.
* Morning watch (04:06)  Braced the fore topsail yard; 58° from square.
  ...
* Morning watch (04:07)  Set the fore topmast staysail.
* Morning watch (04:07)  Set the jib.
* Morning watch (04:09)  Set the spanker.
* Morning watch (04:09)  Set the foresail.
* Morning watch (04:09)  Set the mainsail.
* Morning watch (04:11)  Set the main topsail.
* Morning watch (04:11)  Set the mizzen topsail.
* Morning watch (04:11)  Set the fore topgallant.
  Morning watch (04:13)  Leeway 3° to larboard.
Advanced 900 ticks to Morning watch (04:21).
Amazon: heading WNW (293°), speed 8.0 kn, leeway -3°, heel -7°
Apparent wind 40° on the starboard bow, 16.6 kn; helm -2°
```

Twelve yards braced and eleven sails set in five minutes, and she is close-hauled on the starboard tack at 8 knots: 40° apparent is six points true (chapter 2), three degrees of leeway, seven of heel to larboard, and two degrees of weather helm (chapter 4). This is the ship at her best point for working to windward.

Feel a rope, then go about:

```orders frigate plain-sail
haul the weather main brace
tack ship
tick 600
state
```

```
  Morning watch (04:21)  Hauled the starboard (weather) main brace; the main yard now braced 50° for the starboard tack.
  Morning watch (04:21)  Order: tack ship.
  Morning watch (04:21)  Ready about. Helm's a-lee; eased off the head sheets.
  Morning watch (04:21)  All hands about ship.
* Morning watch (04:21)  Main course taken aback.
  Morning watch (04:21)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:22)  Let go and haul.
* Morning watch (04:25)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:26)  Steady on ENE (68°).
  Morning watch, 1 bell (04:30)  1 bell.
Advanced 600 ticks to Morning watch (04:31).
Amazon: heading ENE (67°), speed 9.2 kn, leeway 3°, heel 10°
Apparent wind 41° on the larboard bow, 19.1 kn; helm +2°
```

Chapter 5 reads the tack line by line. Note that the weather main brace you hauled was the starboard one, and that after the tack leeway, heel and helm have all changed sign: the lee side is now starboard.

It is freshening a little. Take a reef in the topsails and, while the topmen are on the yards, wear her back onto the starboard tack:

```orders frigate plain-sail larboard
reef the topsails, one reef
tick 400
wear ship
tick 900
state
```

```
  Morning watch (04:31)  Order: reef the topsails, one reef.
  Morning watch (04:31)  All hands reef the fore topsail.
  Morning watch (04:32)  Settled the fore topsail halyards and clewed down; hauled out the reef tackles.
  Morning watch (04:36)  Laid out and passed the earings of the fore topsail.
Advanced 400 ticks to Morning watch (04:37).
  Morning watch (04:37)  Order: wear ship.
  Morning watch (04:37)  Stand by to wear ship. Up helm; brace in the after yards.
* Morning watch (04:38)  Reefed the fore topsail; now set, 1 reef.
  Morning watch (04:38)  Wind aft. Squared the head yards; hauled out and braced up.
* Morning watch (04:40)  Wore ship; braced sharp up on the starboard tack, heading WNW (292°).
  Morning watch (04:41)  Steady on WNW (292°).
  Morning watch (04:47)  A gust: 17 knots.
Advanced 900 ticks to Morning watch (04:52).
Amazon: heading WNW (293°), speed 9.7 kn, leeway -3°, heel -11°
Apparent wind 41° on the starboard bow, 20.4 kn; helm -2°
```

A reef takes seven minutes and does not stop the ship being worked; the wear ran through it. She is back where she started at a faster 9.7 knots in the freshening breeze, and lost ground to leeward doing it that the map will one day show.

Heave to, watch her a quarter of an hour, fill away, and save the voyage:

```orders frigate plain-sail
heave to
tick 900
state
fill away
tick 600
state
save voyage.json
replay voyage.json
quit
```

```
  Morning watch (04:52)  Order: heave to.
  Morning watch (04:52)  Hauled up the courses.
  Morning watch (04:52)  Braced the main topsail aback; helm a-lee.
* Morning watch (04:53)  Hove to, main topsail to the mast, helm a-lee.
Advanced 900 ticks to Morning watch (05:07).
Amazon: heading NW (315°), speed 2.4 kn, leeway -163°, heel -6°
Apparent wind 51° on the starboard bow, 11.3 kn; helm +15°
  Morning watch (05:07)  Order: fill away.
  Morning watch (05:07)  Righted the helm; hauled aft the head sheets.
* Morning watch (05:08)  Filled away; braced full and steering WNW (293°).
! Morning watch (05:09)  Taken aback: the sails pressed against the masts and she lost her way.
```

She lies hove to with sternway, and fills away badly: both are the known state of the physics before the tuning package (chapter 5). The replay must print the same state as the one before the save, to the last digit.

## The schooner *Speedwell*, morning watch

```
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
```

Same wind, head north-west by west. Her sails have different names and different evolutions under them, and the language does not change:

```orders schooner
set the foresail
set the mainsail
set the jib
set the fore topsail
brace sharp up on the starboard tack
tick 900
state
```

```
  Morning watch (04:00)  Hands to the foresail halyards and outhaul.
  Morning watch (04:00)  Hands to the mainsail halyards and outhaul.
  Morning watch (04:00)  Clear away the jib; man the halyards.
  Morning watch (04:00)  Hands aloft to loose the fore topsail.
* Morning watch (04:00)  Braced the fore topsail yard; 58° from square.
  Morning watch (04:01)  Cast off the gaskets and cleared away the brails of the foresail.
* Morning watch (04:01)  Set the jib.
* Morning watch (04:03)  Set the foresail.
* Morning watch (04:03)  Set the mainsail.
* Morning watch (04:05)  Set the fore topsail.
Advanced 900 ticks to Morning watch (04:15).
Speedwell: heading NW by W (300°), speed 7.1 kn, leeway -2°, heel -7°
Apparent wind 37° on the starboard bow, 16.3 kn; helm +1°
Sail set: fore.topsail, fore.sail, main.sail, jib
```

Two gaff sails, a jib and a square topsail, and she lies half a point nearer the wind than the frigate (37° apparent) at 7 knots. Give her the rest of her canvas and go about:

```orders schooner
set the gaff topsail
set the fore staysail
tick 300
tack ship
tick 600
state
```

```
* Morning watch (04:17)  Set the gaff topsail.
* Morning watch (04:17)  Set the fore staysail.
  Morning watch (04:20)  Order: tack ship.
  Morning watch (04:20)  Ready about. Helm's a-lee; eased off the head sheets.
* Morning watch (04:20)  Fore topsail taken aback.
  Morning watch (04:20)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:21)  Let go and haul.
* Morning watch (04:22)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:24)  Steady on ENE (68°).
Advanced 600 ticks to Morning watch, 1 bell (04:30).
Speedwell: heading ENE (68°), speed 8.5 kn, leeway 2°, heel 12°
Apparent wind 41° on the larboard bow, 17.7 kn; helm -2°
```

Two minutes in stays. Now bear away to a reach, ease the main sheet, reef the mainsail in the freshening breeze, and heave to with the fore topsail to the mast:

```orders schooner plain-sail larboard
steer east
tick 300
state
ease the main sheet a fathom
reef the mainsail, one reef
tick 400
heave to
tick 600
state
fill away
tick 400
# rejected: set the mizzen topsail
quit
```

```
  Morning watch, 1 bell (04:30)  Helm ordered: steer E (90°).
  Morning watch (04:31)  Steady on E (90°).
Advanced 300 ticks to Morning watch (04:35).
Speedwell: heading E (90°), speed 9.6 kn, leeway 2°, heel 10°
Apparent wind 55° on the larboard bow, 16.9 kn; helm -0°
  Morning watch (04:35)  Eased the main sail sheet; the main sail now 35° off the centreline.
  Morning watch (04:35)  Hands to reef the mainsail.
  Morning watch (04:36)  Settled the mainsail halyards.
  Morning watch (04:40)  Hauled out the reef earing of the mainsail and tied the points.
  Morning watch (04:41)  Order: heave to.
  Morning watch (04:41)  Braced the fore topsail aback; helm a-lee.
* Morning watch (04:41)  Reefed the mainsail; now set, 1 reef.
* Morning watch (04:42)  Hove to, fore topsail to the mast, helm a-lee.
Advanced 600 ticks to Morning watch (04:51).
Speedwell: heading NE (48°), speed 6.9 kn, leeway 5°, heel 15°
Apparent wind 31° on the larboard bow, 19.0 kn; helm -15°
  Morning watch (04:51)  Order: fill away.
* Morning watch (04:52)  Filled away; braced full and steering ENE (67°).
  Morning watch (04:58)  Order not carried out ('set the mizzen topsail'): There is no such part as the mizzen topsail in this ship; did you mean the topsails, the mainsail or the gaff topsail? ('set' was understood.)
```

Two things to notice. Bearing away from 68° to east, the apparent wind draws aft from 41° to 55° and the watch eased the sheets for you; your `ease the main sheet a fathom` found the boom already 30° off and took it to 35°. And the schooner does not heave to: with only one small square sail to lay aback against two big gaff sails she keeps 7 knots of way with her head coming up. A schooner is properly hove to by luffing with the head sheets to windward and the foresail eased, which is not an evolution the game has (Luce 1884, ch. XXXIV Handling Fore-and-Afters). The last line is the ship refusing a sail she has not got, and suggesting the ones she has.
