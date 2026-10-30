# 7. A first passage

An hour and a quarter at sea on each ship, that you can type along with. The logs are from seed 7 with a north wind of 15 knots; type exactly what is in the blocks and yours will match. The blocks quote the log's notable lines (marked `*`) and the routine lines that teach something, and cut the rest with a `...`: the hands' lines as a short watch takes the work in turn ("Only four hands to the jib; the rest are..."), "Man the ... braces", and the leeway said each minute while she gathers way; `state` prints seven lines, of which the three of the ship are quoted. Where a number is quoted, yours may differ by a few tenths.

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
Sail set: none; unbent: fore.storm_staysail, mizzen.storm_staysail, storm_mizzen, ringtail, fore.save_all.starboard, fore.save_all.larboard
  Morning watch, 8 bells (04:00)  Order: set plain sail.
  Morning watch, 8 bells (04:00)  Order: brace sharp up on the starboard tack.
  Morning watch (04:00)  Hands aloft to loose the foresail.
  ...
* Morning watch (04:00)  Bracing the yards: not hands enough for all at once; the watch takes them in turn.
  Morning watch (04:00)  Not hands enough on deck to brace the fore topsail yard; the watch is setting the foresail, the mainsail and the fore topsail and at other work.
  ...
  Morning watch (04:00)  Braced up for the starboard tack, the after yards two degrees sharper.
  Morning watch (04:01)  Laid aloft and loosed the main topsail.
  ...
* Morning watch (04:02)  Set the fore topmast staysail.
* Morning watch (04:02)  Set the jib.
* Morning watch (04:03)  Braced the fore yard; 62° from square.
* Morning watch (04:03)  Set the foresail.
* Morning watch (04:03)  Set the mainsail.
* Morning watch (04:04)  Set the main topsail.
* Morning watch (04:04)  Set the mizzen topsail.
* Morning watch (04:04)  Braced the fore royal yard; 68° from square.
  ...
* Morning watch (04:04)  Braced the crossjack yard; 60° from square.
* Morning watch (04:05)  Set the fore topsail.
* Morning watch (04:06)  Set the spanker.
* Morning watch (04:07)  Set the fore topgallant.
Advanced 480 ticks to Morning watch (04:08).
Amazon: heading NW by W (299°), speed 3.6 kn, leeway -5°, heel -2°
Apparent wind 47° on the starboard bow, 14.0 kn; helm -10°
Sail set: fore.course, fore.topsail, fore.topgallant, main.course, main.topsail, mizzen.topsail, mizzen.spanker, fore.topmast_staysail, jib; unbent: fore.storm_staysail, mizzen.storm_staysail, storm_mizzen, ringtail, fore.save_all.starboard, fore.save_all.larboard
```

The watch on deck is a hundred and eleven hands, and plain sail with twelve yards to brace is more work than they can take at once: the hands go to the courses and the fore topsail first, the braces wait on them ("not hands enough for all at once"), and the yards come round together at 04:04 once the first sails are loosed. Nine sails are set and twelve yards braced in seven minutes, the two topgallants still setting; eight minutes from the order she has three and a half knots and is still gathering way, her head fallen off to NW by W with the helm ten degrees a-weather to hold her. There is no *Taken aback* line: she neither rounds up nor gathers sternway getting under way. The sails bent to her and not set are listed as `unbent`: the storm canvas and the light sails she carries in the sail room, which chapter 3 bends. Give her five minutes more, then trim her to the wind:

```orders frigate plain-sail
tick 300
state
trim sails
tick 120
state
```

```
* Morning watch (04:09)  Set the main topgallant.
Advanced 300 ticks to Morning watch (04:13).
Amazon: heading WNW (293°), speed 4.9 kn, leeway -4°, heel -4°
Apparent wind 51° on the starboard bow, 14.3 kn; helm -6°
Sail set: fore.course, fore.topsail, fore.topgallant, main.course, main.topsail, main.topgallant, mizzen.topsail, mizzen.spanker, fore.topmast_staysail, jib; unbent: ...
  Morning watch (04:13)  Order: trim sails.
  Morning watch (04:13)  Braced twelve yards to the wind, 51° on the starboard bow, the after yards two degrees sharper; trimming the sheets of the mizzen spanker, the fore topmast staysail and the jib.
* Morning watch (04:13)  Bracing the yards: not hands enough for all at once; the watch takes the sails in turn.
* Morning watch (04:13)  Braced twelve yards to the wind; 56° to 64° from square.
  Morning watch (04:14)  Trimmed the sheets of the fore topmast staysail, the jib and the spanker; 23° to 28° off the centreline.
Advanced 120 ticks to Morning watch (04:15).
Amazon: heading WNW (292°), speed 5.4 kn, leeway -4°, heel -4°
Apparent wind 52° on the starboard bow, 14.2 kn; helm -1°
```

Close-hauled on the starboard tack at five knots and a half: 52° apparent is six points true (chapter 2), four degrees of leeway, four of heel to larboard, and a degree of weather helm (chapter 4). The yards were braced sharp up at the start, 60° to 70° from square, and `trim sails` eased them to the 56° to 64° the wind at 51° wants and sheeted the fore-and-aft sails to it; the helm, ten degrees a-weather while she gathered way, came back to one as the trim took the gripe out of her. It is the order to give after a tack or a shift of wind. This is the ship at her best point for working to windward, and the slowest she will go anywhere but dead before the wind. The mizzen topgallant is still setting, seven hands at it: the last sail of plain sail waits for hands as the others are finished.

Feel a rope, see that it stays where you left it, then go about:

```orders frigate plain-sail
ease the spanker sheet
tick 60
haul the spanker sheet
tack ship
tick 720
state
```

```
  Morning watch (04:15)  Eased the mizzen spanker sheet; the mizzen spanker now 32° off the centreline.
Advanced 60 ticks to Morning watch (04:16).
  Morning watch (04:16)  Hauled the mizzen spanker sheet; the mizzen spanker now 28° off the centreline.
  Morning watch (04:16)  Order: tack ship.
* Morning watch (04:16)  All hands! (to tack ship)
* Morning watch (04:16)  Belayed setting the mizzen topgallant: all hands about ship.
  Morning watch (04:16)  Ready about. Helm's a-lee; ease off the head sheets; haul aft the spanker sheet.
  Morning watch (04:16)  All hands about ship.
  Morning watch (04:16)  Rise tacks and sheets. Mainsail haul.
  Morning watch (04:17)  All hands on deck.
  Morning watch (04:17)  Let go and haul. Draw jib; trim aft the head sheets.
  Morning watch (04:18)  Steady on ENE (72°).
* Morning watch (04:20)  Tacked; braced up on the larboard tack, heading ENE (67°).
  Morning watch (04:20)  Piped down; the starboard watch has the deck.
* Morning watch (04:20)  Set the mizzen topgallant.
  Morning watch (04:21)  Steady on ENE (67°).
Advanced 720 ticks to Morning watch (04:28).
Amazon: heading ENE (67°), speed 5.2 kn, leeway 4°, heel 4°
Apparent wind 48° on the larboard bow, 15.7 kn; helm +1°
```

The spanker was sheeted to 28° for the wind by `trim sails`; you eased it a fathom of the fall to 32°, and a minute later it was still there, for nobody tends a sheet but hands sent to it (chapter 4); your haul took it back to 28°. Tacking calls all hands (chapter 6): the mizzen topgallant's party is belayed and piped to the braces, and the sail is set after she is round, when the watch is piped down. Chapter 5 reads the tack line by line: four minutes to *Tacked*, and twelve minutes after the order she is at five knots on the other tack, her sheets trimmed by the tack for the wind she came to. Leeway, heel and helm have all changed sign: the lee side is now starboard.

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
  Morning watch (04:28)  Hauled the larboard (weather) main brace; the main yard now braced 59° for the larboard tack.
  Morning watch (04:28)  Order: wear ship.
* Morning watch (04:28)  All hands! (to wear ship)
  Morning watch (04:28)  Stand by to wear ship. Up helm; brail up the spanker; brace in the after yards.
  Morning watch (04:28)  Stations for wearing ship.
  Morning watch (04:29)  Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up.
  Morning watch (04:29)  All hands on deck.
  Morning watch, 1 bell (04:30)  1 bell.
  Morning watch (04:34)  By the wind. Haul out the spanker!
* Morning watch (04:36)  Wore ship; braced sharp up on the starboard tack, heading WNW (293°).
  Morning watch (04:36)  Piped down; the starboard watch has the deck.
  Morning watch (04:37)  Steady on WNW (293°).
Advanced 900 ticks to Morning watch (04:43).
Amazon: heading WNW (293°), speed 4.3 kn, leeway -6°, heel -4°
Apparent wind 46° on the starboard bow, 16.2 kn; helm -1°
  Morning watch (04:43)  Order: reef the topsails, one reef.
* Morning watch (04:43)  All hands! (to reef the fore topsail)
  Morning watch (04:43)  All hands reef the fore topsail.
  Morning watch (04:43)  All hands reef the main topsail.
  Morning watch (04:43)  All hands reef the mizzen topsail.
  Morning watch (04:44)  Settled the fore topsail halyards and clewed down; hauled out the reef tackles.
  ...
  Morning watch (04:47)  A gust: 18 knots, the mean 16.
  Morning watch (04:47)  Laid out and passed the earings of the fore topsail.
  ...
* Morning watch (04:49)  Reefed the fore topsail; now set, 1 reef.
* Morning watch (04:49)  Reefed the main topsail; now set, 1 reef.
* Morning watch (04:49)  Reefed the mizzen topsail; now set, 1 reef.
  Morning watch (04:49)  Piped down; the starboard watch has the deck.
Advanced 500 ticks to Morning watch (04:51).
Amazon: heading WNW (293°), speed 4.4 kn, leeway -6°, heel -4°
Apparent wind 48° on the starboard bow, 16.4 kn; helm -1°
```

On the larboard tack the weather main brace was the larboard one. Eight minutes from *Stand by to wear* to *Wore ship*, and she came round with the yards following the wind and lost a quarter of a mile to leeward doing it; seven minutes after she is round she has four knots and a half, still gathering way close-hauled. The three topsails are reefed together by all hands, six minutes from the order to the last *Reefed*, and the breeze has got up a knot meanwhile, so her speed holds.

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
  Morning watch (04:51)  Braced the main topsail aback; hauled aft the head sheets; helm a-lee.
  Morning watch (04:51)  Hands to the after braces; heave to.
  Morning watch (04:52)  A gust: 20 knots, the mean 16.
* Morning watch (04:54)  Hove to on the starboard tack, main topsail to the mast, helm a-lee.
  Morning watch, 2 bells (05:00)  2 bells.
Advanced 600 ticks to Morning watch (05:01).
Amazon: heading NW by W (301°), speed 1.6 kn, leeway -39°, heel -4°
Apparent wind 56° on the starboard bow, 14.2 kn; helm +24°
Sail set: fore.topsail, main.topsail, main.topgallant, mizzen.topsail, mizzen.topgallant, fore.topmast_staysail, jib; unbent: ...
  Morning watch (05:01)  Order: fill away.
  Morning watch (05:01)  Hauled aft the head sheets; kept the helm a-lee to let her fall off.
  Morning watch (05:01)  Fill away; man the after braces.
  Morning watch (05:01)  Braced the main topsail full.
* Morning watch (05:02)  Filled away on the starboard tack; braced full and steering WNW (297°).
  Morning watch (05:04)  Steady on WNW (297°).
Advanced 400 ticks to Morning watch (05:08).
Amazon: heading WNW (297°), speed 3.8 kn, leeway -6°, heel -3°
Apparent wind 49° on the starboard bow, 14.6 kn; helm +5°
  Morning watch (05:08)  Order: set the courses.
  Morning watch (05:08)  Order: set the spanker.
  Morning watch (05:08)  Man the foresail sheets; let go the clewlines and buntlines.
  ...
* Morning watch (05:10)  Set the foresail.
* Morning watch (05:10)  Set the mainsail.
* Morning watch (05:10)  Set the spanker.
Advanced 300 ticks to Morning watch (05:13).
Amazon: heading WNW (297°), speed 3.7 kn, leeway -6°, heel -3°
Apparent wind 51° on the starboard bow, 13.4 kn; helm -7°
Saved to voyage.json at tick 4380.
Replaying voyage.json to tick 4380...
Replayed. Log digest 989736f3e847a6fc. Clock held.
```

Hove to she lies five points off the wind making a knot and a half, most of it sideways (leeway 39°), with the helm hard a-lee to hold her so, and holds so through a 20-knot gust; filled away she is steady on her course in three minutes and has nearly four knots seven minutes after the order, with no *Taken aback* line (chapter 5). The courses and spanker come back in two minutes, and she is a little slower for the moment while the breeze eases to thirteen knots. The replay must print the same state as the one before the save, to the last digit, and the log digest in yours must be the one above; the line after it names the save's build, which is the game's own.

## The schooner *Speedwell*, morning watch

```
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
```

Same wind, head north-west by west. Her sails have different names and different evolutions under them, and the language does not change; her watch is seventeen hands, so plain sail is set a sail or two at a time:

```orders schooner
state
set plain sail
brace sharp up on the starboard tack
tick 900
state
```

```
  Morning watch, 8 bells (04:00)  Order: set plain sail.
  Morning watch, 8 bells (04:00)  Order: brace sharp up on the starboard tack.
  Morning watch (04:00)  Hands to the foresail halyards and outhaul.
  Morning watch (04:00)  Hands to the mainsail halyards and outhaul.
* Morning watch (04:00)  Setting plain sail: not hands enough for all at once; the watch takes the sails in turn.
* Morning watch (04:00)  Bracing the yards: not hands enough for all at once; the watch takes them in turn.
  Morning watch (04:01)  Cast off the gaskets and cleared away the brails of the foresail.
  Morning watch (04:01)  Cast off the gaskets and cleared away the brails of the mainsail.
* Morning watch (04:03)  Set the foresail.
  Morning watch (04:03)  Hands aloft to loose the fore topsail.
* Morning watch (04:04)  Her sails aback; she had no way on to lose.
* Morning watch (04:05)  Set the mainsail.
  ...
* Morning watch (04:09)  Set the fore topsail.
  ...
* Morning watch (04:11)  Set the fore staysail.
* Morning watch (04:11)  Set the jib.
* Morning watch (04:12)  Braced the fore topsail yard; 58° from square.
* Morning watch (04:12)  Braced the fore topgallant yard; 60° from square.
* Morning watch (04:14)  Her sails lifting, the wind 51° on the starboard bow: keep her away, or she will be taken aback.
Advanced 900 ticks to Morning watch (04:15).
Speedwell: heading NW by W (299°), speed 3.2 kn, leeway -6°, heel -3°
Apparent wind 53° on the starboard bow, 12.9 kn; helm +18°
Sail set: fore.topsail, fore.sail, main.sail, fore.staysail, jib; unbent: storm_trysail, storm_jib, ringtail, water_sail
```

Two gaff sails, two headsails and two square sails on the fore. With seventeen hands the gaff sails go up first and the square sails wait for them, so she is a quarter of an hour making sail where the frigate took seven minutes; her fore-and-aft canvas filled before her topsail was braced, which is why the log says *her sails aback* with no way to lose and, as she gathers way at 300°, *her sails lifting*: four points off the wind is as close as she will lie with the topsail drawing, and the helm is eighteen degrees a-weather to keep her there. Give her the gaff topsail and go about:

```orders schooner plain-sail
set the gaff topsail
tick 300
state
tack ship
tick 900
state
```

```
* Morning watch (04:15)  Set the fore topgallant.
* Morning watch (04:16)  Set the gaff topsail.
Advanced 300 ticks to Morning watch (04:20).
Speedwell: heading NW by W (299°), speed 2.8 kn, leeway -6°, heel -3°
Apparent wind 50° on the starboard bow, 12.8 kn; helm +12°
  Morning watch (04:20)  Order: tack ship.
* Morning watch (04:20)  All hands! (to tack ship)
  Morning watch (04:20)  Ready about. Helm's a-lee; ease off the head sheets; haul aft the mainsail sheet.
  Morning watch (04:20)  All hands about ship.
  Morning watch (04:21)  Her way is gone; she hangs in stays. Helm kept a-lee; the head yards aback to box her off; the head sheets held to windward; the mainsail boom hauled over to windward.
  Morning watch (04:21)  Her head is through the wind; the head sails aback pay her off.
  Morning watch (04:21)  Let go and haul. Draw jib; trim aft the head sheets.
  Morning watch (04:21)  All hands on deck.
  ...
* Morning watch (04:25)  Tacked; braced up on the larboard tack, heading ENE (68°).
  Morning watch (04:25)  Piped down; the starboard watch has the deck.
  Morning watch (04:26)  Steady on ENE (68°).
  Morning watch, 1 bell (04:30)  1 bell.
Advanced 900 ticks to Morning watch (04:35).
Speedwell: heading ENE (68°), speed 5.8 kn, leeway 3°, heel 8°
Apparent wind 49° on the larboard bow, 16.8 kn; helm +5°
```

Pinched at three knots she has not the way to shoot through the wind: she *hangs in stays*, and the deck does what Luce has it do for a ship that misses stays (chapter 5): the helm kept a-lee, the head yards laid aback to box her off, the head sheets held to windward and the main boom hauled over, until her head is through and the head sails aback pay her off. Five minutes from the order to *Tacked*, and fifteen minutes after it she is on the larboard tack at nearly six knots in a breeze that has freshened to sixteen, her head a point and a half freer than the frigate's close-hauled course. Now bear away to a reach, ease the main sheet, reef the mainsail, and heave to with the fore topsail to the mast:

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
Speedwell: heading E (90°), speed 8.4 kn, leeway 2°, heel 11°
Apparent wind 61° on the larboard bow, 15.1 kn; helm +5°
  Morning watch (04:40)  Order: ease the main sheet a fathom.
  Morning watch (04:40)  Eased the main sail sheet; the main sail now 35° off the centreline.
  Morning watch (04:40)  Order: reef the mainsail, one reef.
  Morning watch (04:40)  Hands to reef the mainsail.
  Morning watch (04:41)  Settled the mainsail halyards.
  Morning watch (04:45)  Hauled out the reef earing of the mainsail and tied the points.
Advanced 400 ticks to Morning watch (04:46).
Speedwell: heading E (91°), speed 7.5 kn, leeway 2°, heel 9°
Apparent wind 66° on the larboard bow, 14.3 kn; helm +3°
  Morning watch (04:46)  Order: heave to.
  Morning watch (04:46)  Only seven hands to heave to; the rest are reefing the mainsail.
  Morning watch (04:46)  Hauled flat aft the mainsail sheet; the fore staysail sheet to windward; braced the fore topsail aback; helm a-lee.
  Morning watch (04:46)  Hands to the after braces; heave to.
* Morning watch (04:47)  Reefed the mainsail; now set, 1 reef.
  Morning watch (04:47)  A gust: 18 knots, the mean 16.
* Morning watch (04:49)  Hove to on the larboard tack, fore topsail to the mast, helm a-lee.
  Morning watch (04:52)  A gust: 20 knots, the mean 16.
Advanced 600 ticks to Morning watch (04:56).
Speedwell: heading NE (50°), speed 1.2 kn, leeway 64°, heel 8°
Apparent wind 47° on the larboard bow, 13.7 kn; helm -4°
  Morning watch (04:56)  Order: fill away.
  Morning watch (04:56)  Hauled aft the head sheets; kept the helm a-lee to let her fall off.
  Morning watch (04:56)  Fill away; man the after braces.
  Morning watch (04:56)  Fallen off; braced the fore topsail full.
* Morning watch (04:57)  Filled away on the larboard tack; braced full and steering ENE (64°).
  Morning watch (04:58)  Steady on ENE (64°).
  Morning watch, 2 bells (05:00)  2 bells.
Advanced 400 ticks to Morning watch (05:03).
Speedwell: heading ENE (64°), speed 5.5 kn, leeway 4°, heel 7°
Apparent wind 44° on the larboard bow, 16.2 kn; helm +2°
  Morning watch (05:03)  Order not carried out ('set the mizzen topsail'): There is no such part as the mizzen topsail in this ship; did you mean the topsails, the mainsail or the gaff topsail? ('set' was understood.)
```

Four things to notice. Bearing away from 68° to east she goes from 5.8 to 8.4 knots, the apparent wind draws aft from 49° to 61°, and the watch eased the sheets for you: your `ease the main sheet a fathom` found the boom already 30° off and took it to 35°. The reef is a fore-and-aft sail's (chapter 3): the halyards settled, the earing hauled out and the points tied, seven minutes with ten hands, so the heave-to that follows gets seven hands until they are done. A schooner heaves to by her own evolution, which is not the frigate's: the main sheet hauled flat aft, the fore staysail sheet to windward and the fore topsail laid aback, and she lies two points closer to the wind than the frigate did, making a knot with the sea setting her bodily to leeward (leeway 64°). Filled away she is back at five knots and a half in six minutes. And the last line is the ship refusing a sail she has not got, and suggesting the ones she has.

## Standing orders: the ship keeps herself

A standing order is an order like any other, given at the prompt and journaled, with a trigger in front of it: *when* a reading holds (for a while, if you say so), *at* an event, or *every* interval. When it fires, the log says which order fired and what it did, and nothing happens that the log does not explain. The words a condition may test are the ship's own readings, the same ones `state` shows: the true wind, the apparent wind, the heading, the speed, the heel, the watch, daylight, a sail by name, the strain, the hands on deck. The starter routines come with the game in `data/standing_orders/starter.orders`, a book to begin with if you choose and never one you must (chapter 11 prints each with its reason, and how to write your own); here they are, given one at a time on the frigate before the wind (`--heading 180`, so the studding sails will draw), with the book's own orders after them:

```orders frigate all-sail
standing order "night routine": at sunset then take in the studdingsails; take in the royals
standing order "morning sail": at sunrise, if the true wind is under 20 knots then set the royals
standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef
standing order "keep her full": when the apparent wind is forward of 55 degrees then bear away one point
standing order "trim on a shift": when the true wind veers 1 point or backs 1 point and the manoeuvre in hand is not hove to then trim sails
standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then close reef the topsails; send down the topgallant masts; shift the fore topmast staysail for the fore storm staysail
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

Belaying an order keeps it in the book, idle, until you resume it; striking it (`strike standing order "x"`, or `cancel` or `remove`) takes it out of the book altogether, and its name may be given again. The glass is a reading (chapter 9), so a rule on it is a book's line in any ship, and in one that carries no glass it simply never fires; a second order of a name already in the book is refused; a misspelt sail is refused when the order is given, not on the night it fires. The whole file loads in one line at the prompt, `read the standing orders from data/standing_orders/starter.orders`, or at the start with `--standing-orders data/standing_orders/starter.orders`; each line is given as an order, and one the ship refuses does not stop the rest.

To see one fire, sail her to sunset. At seed 7 with the wind north 15 knots and her head south, under all sail with the studding sails set as chapter 3 sets them (`make all sail`, then `rig out the studdingsails, both sides` and `set the studdingsails, both sides`), give the night routine and `tick 56000`; `state` on the way says where the sun stands:

```
Day. Sunrise 03:56, sunset 19:58; civil twilight from 03:13 and until 20:41.
Amazon: heading S (180°), speed 6.5 kn, leeway 0°, heel 0°
...
* Last dog watch (19:59)  Sunset.
* Last dog watch (19:59)  By standing order 'night routine': taking in the studdingsails.
* Last dog watch (19:59)  By standing order 'night routine': taking in the royals.
```

The "By standing order" line is notable and stands in for the "Order:" line a captain's order gets; what follows it is the hands' ordinary work. `standing orders` afterwards reads `"night routine" (the captain): at sunset then take in the studdingsails; take in the royals. Standing; fired once, last at Last dog watch (19:59).` An order the ship cannot carry out when it fires is refused in the log's words too: `Standing order 'morning sail' at sunrise: not carried out; the true wind is 25 knots, not under 20 knots.` for a failed `if` (said the first time, and then once a watch while the `if` goes on failing, so that an `every 10 minutes, if ...` order does not fill the log), and `Standing order 'x': order not carried out ('take in the royals'): Nothing done: the fore royal is already furled; ...` for an order the ship refuses.

Three guards keep a standing order from thrashing. A duration debounces: `for 2 minutes` means the wind has been over thirty for two minutes of ship's time together, so the console's gusts, which last seconds, never fire it. A `when` order fires once, on the edge, and not again until its condition has been false for five minutes and the work it started has ended; `keep her full` bears away a point and then waits. `trim on a shift` shows the edge at work on the wind's direction: `veers 1 point or backs 1 point` is measured from the wind as it was when the order last stood, and once fired it measures afresh, so a wind that veers from west to north-west through a night has the yards trimmed to it point by point, five minutes at least apart. A gust does not move the wind's direction, so it never fires it, though the wind's wander about its base, a few degrees either way, moves the firing some minutes and in the unstable air behind a cold front may fire it by itself now and then; and a trim the watch is still at is not stacked behind: a yard still waiting its turn takes the new angle, and the log says the yards are being trimmed already. And two orders that lay hands on the same part within those five minutes, while the first one's work is still in hand, are settled by rank (a sail, a yard or a line is its own part; the helm is one; a manoeuvre is the helm's and the yards'; the lead is the leadsman's, the log the log's and a bearing the master's, so `heave the lead` and `heave to` are not contrary): the captain's stands over the master's, and the log says `Standing order 'royals' (the master) countermanded by 'royals in' (the captain).`; two of the captain's own give the later the day, with a plain note.

Two things the ship holds back for you. A course given after weighing, at the prompt or by a standing order such as `at the anchor aweigh then steer E`, is not put on the helm while the jib and the helm are still casting her: it is held until she has gathered way, a knot through the water with her sails drawing, and the log says so twice, at the aweigh ("E (90°) is held till she has gathered way") and when it is steered ("She has gathered way, 1.1 knots, her sails drawing: E (90°) is steered"); chapter 11 has the reason. And a helm order that carries the wind across her stern orders no sail work: a boom gybes by itself, a lugger's lugs are left against their masts and square yards braced for the old tack are left by the lee, and the deck says it once for the crossing ("The wind has come across the stern to the larboard quarter: the foresail and the mainsail are against their masts; dip them when you will."). The dip, the brace and the sheet are your next orders; the rules-based captain gives them as his.

The order of an order's clauses is the order of the work. When a standing order fires several clauses on one tick, the hands go to the first clause first, and each clause after it gets what is left and what comes free, so a clause that must be done before the weather comes belongs at the head. The starter's heavy-weather routine has the close reef of the topsails first for that reason (three parties of forty, reefed together), and the sending down of the topgallant masts, which takes every hand it can get, second: written the other way round, the send-down took the hands and the topsails were still unreefed when the first squall of the middle watch came, on the day the tests measure (chapter 3 says how a reef is manned).

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

An order after `then` is read whole when the standing order is given, by the reader that will carry it out, and every order of it, not its first word alone: a sail the ship has two of and that is not named which, a mark the chart has not got (`take a bearing of the moon made of cheese`), the marks of a fix that are no marks (`take a fix as soon as a bearing can be taken`), a place the chart does not name, an anchor she does not carry, a number of fathoms or of days that cannot be read: each is refused at the giving, the refusal naming the order, and not met at sea at the first firing. What depends on the moment (what is in sight, an anchor down, whether she is in port) is still the order's business when it fires.

```orders frigate
# rejected: standing order "three": every glass then heave the lead; trim sails; set the topsail
# rejected: standing order "fathoms": every glass then heave the lead; veer umpteen fathoms
```

## Saying it

The ship takes the words a seaman would use and refuses, in words that say what to say instead, the ones she cannot take. A course with a half or a quarter point is read whole (chapter 2): `steer south by west half west` is S by W ½ W (197°). Numbers are read in words as in figures by every order that takes one, from *a quarter* and *half a* to *a hundred and eighty-five*. The helm takes *steady on*, *close hauled* (keep her full and by) and *bring her up* (come up); a headsail is backed by hauling its sheet to windward; a jib, a staysail or the water sail told to *furl* is handed and stowed, which is taking it in; *lower* is said of a jib and a studding sail as of a gaff sail.

```orders frigate plain-sail
steer south by west half west
steer WNW 1/2 W
bear away a point and a half
steady on
close hauled
bring her up a point
trim the headsail sheets
furl the jibs
# rejected: steer south by west half
# rejected: as you were
# rejected: put the helm over
```

Some words are refused with what to say instead: *as you were* is answered with `belay that`; *put the helm over*, which says not which way, with `helm a-lee` and `hard a-weather`. At sea with a chart, `where is Ushant` says where a mark of the chart lies, in sight by the lookout's bearing and estimate, or by account from the master's position ("Ushant: not in sight; by account it bears S by E, 88 miles."), and `shape a course for a mile west of Ushant` lays off a point from a place of the chart (chapter 10). A mark's name is taken without its accents or its apostrophes: *lavandiere* is the Lavandière, *st anthonys head* St Anthony's Head. A word to a station nobody holds (`tell the watcher keep a sharp lookout`) is kept in its journal and passed to whoever takes the station, and the log says so.

## A day of it, and a word with the watcher

The scenario `data/scenarios/gate-4c-day.yaml` is a whole day under standing orders, the wind scripted to veer and rise to a gale in the middle watch and ease at the next dawn: start it with `--scenario data/scenarios/gate-4c-day.yaml` on the console or the browser server, and run it at `speed 60` or `speed 300`, where the log rolls up each hour's routine lines into one line (marked `=`) and keeps every notable and urgent line as it is; an urgent line eases the clock to 1x and says so. With a watcher at its station, `ask the watcher how the sails are drawing` puts a question it answers in the log, and `tell the watcher we make for Falmouth` (or `say to the watcher ...`) gives it a word it hears and owes no answer to. `stand down the watcher` releases the station with a save, `resume the watcher` answers a pause, and `show the watcher's journal` reads what it wrote; the same three sentences serve every station of the wardroom (chapter 19).
