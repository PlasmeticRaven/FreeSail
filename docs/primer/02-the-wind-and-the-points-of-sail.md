# 2. The wind and the points of sail

## The true wind

Sailors name a wind by where it comes from: a north wind blows from the north (Falconer, *Wind*). The log says so at the start of every voyage and whenever it changes:

```
* Morning watch, 8 bells (04:00)  Open water. Wind N, 15 knots, a moderate breeze. Heading WNW (293°).
  Morning watch (04:47)  A gust: 17 knots.
```

The strength words follow the old scale of breezes: *light airs*, *a light breeze*, *a gentle breeze*, *a moderate breeze*, and so on up to a gale (Luce 1866, ch. XXVIII Storms, 'Table of force and velocity of wind'). The wind wanders a little and gusts; with the same seed it wanders the same way every time (chapter 6).

## The apparent wind

The wind you feel on deck is the true wind combined with the ship's own motion. A ship making 5 knots to windward in a 15-knot breeze feels it a little stronger and a good deal further ahead; running before it she feels it lighter. The sails know only the apparent wind, and so it is the apparent wind that `state` reports, as an angle from the bow and the side it is on:

```
Amazon: heading WNW (293°), speed 4.6 kn, leeway -4°, heel -3°
Apparent wind 49° on the starboard bow, 14.4 kn; helm -1°
```

Here the true wind is north, 67° from her heading of 293°, but she feels it at 49°; on a beam reach at 8 knots she would feel a 15-knot wind at 59° and 18 knots. This difference is the whole reason a square-rigger cannot point higher: see below.

## The tack

"A ship is said to be on the starboard or larboard tack, when she is close-hauled, with the wind upon the starboard or larboard side" (Falconer, *Tack*). The game uses it at every point of sail: **the tack is the side the wind is on**. Wind on the starboard bow, starboard tack. *Weather* is that side; *lee* is the other (Falconer, *Lee*). Every *weather* and *lee* in an order is resolved from the tack she is on when you give it, and the log tells you which rope that turned out to be:

```
  Morning watch (04:21)  Order: haul the weather main brace.
  Morning watch (04:21)  Hauled the starboard (weather) main brace; the main yard now braced 50° for the starboard tack.
```

## The compass

Thirty-two points of 11¼° each, named as Falconer names them: north, north by east, north-north-east, north-east by north, north-east, and so round (Lever, figure 396: "which should be diligently got by rote"). The log gives both the point and the degrees: `WNW (293°)`. You may steer by either, and the parser takes the long names, the short ones and the old contractions:

```orders frigate
steer west-north-west
steer WNW
steer nor'west by west
steer 293
steer 293 degrees
steer two points to starboard
steer three points off
# rejected: steer two points
```

"Two points" alone is refused with "Steer how many points which way? Say 'up', 'off', 'to starboard' or 'to larboard'." *Up* is toward the wind, *off* away from it.

The card of the period is cut finer than the thirty-two points: each point into quarters, a hundred and twenty-eight in all, and a course between two points is said from the nearer whole point toward another within eight points of it, *south by west half west*, *north-east three quarters north* (Bowditch's table; Falconer, *Compass*). The parser reads the whole of it, in words, figures or the signs, and the log shows it as the card has it, with the degrees: "Helm ordered: steer S by W ½ W (197°)."

```orders frigate
steer south by west half west
steer S by W 1/2 W
steer S by W ½ W
steer west-north-west half west
steer WNW 1/2 W
steer NE by N 1/4 N
steer north-north-east three quarters east
steer north half east
# rejected: steer south by west half
# rejected: steer north half south
# rejected: steer west two
# rejected: steer south-west, 245
```

A course is steered as it was said or not at all. A half with no point after it ("toward which point?"), a fraction reckoned toward a point more than eight points off ("north half south" is no course), two courses in one order, or a course with a count of points after it are refused in words that say how a half point is said; none is steered to the last word of it, which before package 37l is what *south by west half west* got: west, six and a half points from what was said.

Numbers are taken in words as in figures wherever an order wants one: *steer two hundred and forty-five degrees*, *veer five fathoms*, *a hundred and eighty-five fathoms*, *take in provisions for sixteen days*, *haul in the jib sheet a quarter fathom*, *bear away a point and a half*. One reader serves every order (the teens, the tens, the hundreds and a thousand, a half, a quarter and three quarters, *and a half* after a number), and a number it cannot read is refused, never taken as some other.

## The points of sail

Counting from the wind round to dead astern (Lever, figures 397 and 398; Falconer, *Close-hauled*, *Large*):

| Wind from the bow | Name | What it means |
|---|---|---|
| under six points | (she cannot lie there) | the sails shake or are taken aback |
| six points (67°) | **close-hauled**, *by the wind*, *on a wind*, *on a bowline* | as near the wind as a square-rigged ship will lie |
| seven points | *one point free* | eased off a point; faster, and further from the wind |
| eight points (90°) | **wind abeam**, *on the beam* | the wind blows on the ends of the beams |
| nine to thirteen points | **the wind large**, *on the quarter*, *quartering* | "when it crosses the line of a ship's course in a favourable direction, particularly on the beam or quarter" |
| sixteen points (180°) | **before the wind**, *running*, *wind aft*, *dead aft* | the yards square; the after sails blanket the head sails |

Sailing with the wind on the beam or abaft it is *sailing large* or, from the quarter, *reaching* in the later word; *going free* is anything not close-hauled. Sailing so far off that the wind comes on the same side as the boom is *by the lee*, which is a fault, not a point of sail.

### Why six points

Falconer: "In this manner of sailing the keel commonly makes an angle of six points with the line of the wind; but sloops, and some other small vessels, are said to sail almost a point nearer." Lever: "A square rigged Ship, when close-hauled, can lie no nearer to the Wind than six Points... In practice the Yard is braced up sharper, to make the Sail stand to the most advantage."

The reason is in two numbers the ship file gives every yard. A yard cannot be braced past its **brace limit**, about 55° from square for the lower yards and a little more aloft, because the shrouds are in the way; so its sail can lie no nearer than 35° to the keel. A coarse flax sail needs the wind some 15° to 20° off its own surface before it draws at all, so the apparent wind can come no nearer than about 45° from the bow before the weather leech lifts and the sails go dead. And because she is moving, the apparent wind is always ahead of the true: 49° apparent at 5 knots in a 15-knot breeze is about 67° true, which is six points. Her best course to windward, the one that makes the most ground against the wind, is a degree or two either side of it at about 5 knots; she will hold three knots to 58° off, but only on her jibs and spanker, with the square sails shaking. The game does not assume the six points; it comes out of the yards, the sails and the speed. A fore-and-aft sail sheets much nearer the centreline, which is why the schooner in chapter 7 lies half a point nearer.

Add to that the **leeway**: "All vessels, however, are supposed to make nearly a point of lee-way, when close-hauled" (Falconer). The log reports it as it changes and `state` shows it:

```
  Morning watch (04:12)  Leeway 4° to larboard.
```

Leeway means something only when she has way on. Under half a knot of headway, gathering way from rest, in stays, or going astern (*sternway*, which you will see when hove to), the log writes no leeway line and the readings say "no way on; course and leeway not meaningful" (or "making sternway; ...") instead of a number.

The apparent wind is named by where it lies, in the points of sail above: forward of seven and a half points it is *on the bow*; about eight points, *on the beam*; from nine to fourteen points, *on the quarter*, abaft the beam; beyond that, *astern*.

### Full and by

Close-hauled, the helmsman keeps her *full and by*: by the wind, but with the sails full. Luce's conning words for it are *No higher!*, *Nothing off!*, *Keep her a good full and by!*, *Very well thus* (Luce 1866, ch. XXIV Working to Windward, 'Conning'). In Orders the helm verbs are:

```orders frigate
keep her full
full and by
come up a point
luff
come up two points
come up half a point
bear away
bear away two points
bear away a point and a half
fall off
off the wind
steer off the wind
bear off the wind
# rejected: by and large
keep her off two points
steer full and by
nothing off
no higher
luff and touch her
bring her by the wind
```

`keep her full` (or `full and by`, *bring her by the wind*, *steer by the wind*) hands the helmsman the standing task: he steers as close as she will lie with the sails drawing, and follows the wind as it shifts. On the frigate that is about 58° apparent, 70° true, at five and a half knots; a good full, a few degrees off the closest she can point, because the sails draw better there. Luce's *Nothing off!*, *No higher!* and *Luff and touch her!* are the same order given from either side of it, and the log echoes the word you used: "Helm ordered: no higher; keep her full and by." `come up` (*luff*) and `bear away` (*keep away*, *bear up*, *bear off*, *fall off*, *off the wind*, *steer off the wind*, *bear off the wind*) move the ordered course by a point, or the number of points you give (halves are taken: *half a point*, *a point and a half*), and put her on a fixed compass course from then on; say `keep her full` again to go back to sailing by the wind. *By and large* is not a helm order but a description of how she sails, and the ship refuses it. Falconer, *Luff*: "the order from the pilot to the steersman to put the helm towards the lee-side of the ship, in order to make the ship sail nearer the direction of the wind."

### A course across the wind

A helmsman given a course on the other side of the wind does not simply put the helm over: turned the shorter way she would come head to wind with her yards braced for the old tack and be taken aback, or swing her stern through the wind with every square sail pressed back against the masts. Every order that gives her a course (`steer`, `come up`, `bear away`, `steer two points to starboard`, and the master's `shape a course for` and `give chase`, chapters 10 and 15) is judged by one rule against her head and the wind, and the line says what she does, so that you can countermand it:

| The course | What she does |
|---|---|
| on the tack she is on | the helm: she is steered to it |
| across the wind's eye, the shorter way | put about for it (chapter 5), with way enough to stay (two knots); with less, worn round for it, "when ... the vessel has not sufficient headway for tacking" (Luce 1866, ch. XXIV, 'Wearing') |
| across the wind by the stern, more than eight points round | worn round for it if she has a square sail set, a square-rigged ship or a fore-and-after with her topsail set, since her yards must be braced round; a fore-and-after with no square sail set gybes by the helm, her boom coming over, as she always has |
| nearer the wind than six points, on the other tack | put about or worn for that tack, and kept full and by on it |
| within a point of the wind's eye, given to the helm | steered as given, and the line warns that she will be taken aback |
| across the wind, put about, worn or gybed by the rows above, but with too little way on her for it | kept full and by on the tack she is on, the course held; when she has the way (three knots to go about, or after three minutes with a knot, worn; a knot to wear; steerage way to gybe) she is put about, worn or gybed for it as above, and ends on it |

The tack or the wear ends by steering the course (chapter 5), so you need not give it again. A course shaped or a chase's nearer the wind than she will lie on the tack she is on is not steered: she is kept full and by, as the pilot's course is. Your own `steer` on the tack she is on is carried out however near the wind it is: pinching her, the sails "just lifting", is yours to order (Fincham's rule, truth 25), and her sails lifting and her being taken aback are said as they come (chapter 5). With no way on her, gathering way from rest or after filling away, a course on the tack she is on is steered as you say; one across the wind is held for her ("WSW (245°) lies across the wind's eye from her head, and she has no way on her; she is kept full and by on the larboard tack until she has, then put about for it."), and given her when she has the way, in a line of its own ("She has way on her now: ..."). Another course, `keep her full`, a word to the wheel or a manoeuvre gives it up; an order in points from her course does not.

```
  Morning watch (04:25)  Helm ordered: steer E by N (79°); E by N (79°) lies across the wind's eye from her head; she is put about for it. All hands about ship.
  Morning watch (04:25)  Helm ordered: steer SE (135°); SE (135°) lies across the wind from her head, by the stern; she is worn round for it. Stations for wearing ship.
  Morning watch (04:25)  Helm ordered: steer NE by E (56°); NE by E (56°) lies too near the wind to be laid; she is put about and kept full and by on the larboard tack. All hands about ship.
* Morning watch (04:25)  Helm ordered: steer N by W (349°); N by W (349°) lies in the wind's eye from her head; she will be taken aback.
```

Those are the frigate's, close-hauled on the starboard tack heading WNW in a northerly; the last is notable, and is followed within seconds by her sails lifting and "Taken aback". `tack`, `wear` and `heave to` by their own words are unchanged: they are the manoeuvre, not a course.

### Conning the helm

The rest of the conning words (Luce 1866, ch. XXIV, 'Conning'; Falconer, *Helm*) speak to the wheel rather than to the course, and the game takes them as they were meant:

```orders frigate
steady
steady as she goes
meet her
right the helm
hard a-lee
helm's a-lee
hard up
helm a-weather
up helm
down helm
```

| Order | What the helmsman does |
|---|---|
| **steady**, *steady as she goes*, *very well thus*, *thus* | holds the heading she has at that moment, as a compass course |
| **meet her**, *check her* | meets her swing with the opposite helm and steadies her on the heading she has |
| **right the helm**, *helm amidships*, *midships* | puts the rudder amidships and leaves it there: she steers herself until you say otherwise |
| **hard a-lee**, *helm's a-lee*, *down helm*, *put the helm down* | rudder hard over to windward, her head coming up to the wind, and left there |
| **hard up**, *helm a-weather*, *up helm*, *put the helm up* | rudder hard over to leeward, her head paying off, and left there |

*Helm* here is the tiller: the helm a-lee puts the rudder to windward, which is why "helm's a-lee" begins a tack. The log says which way the rudder went: "Helm ordered: hard a-lee; rudder hard over to windward (35° to starboard), her head coming up to the wind." After *hard a-lee* or *hard up* nobody is steering a course: she turns until you say *meet her* or *steady*, or give a course. This is what the tack and the wear do for themselves in chapter 5, and it is how you would work a box-haul by hand.

## What `state` reports

```
Morning watch (04:21)
Wind N, 14 knots, a moderate breeze
Amazon: heading WNW (293°), speed 4.6 kn, leeway -4°, heel -3°
Apparent wind 49° on the starboard bow, 14.4 kn; helm -1°
Sail set: fore.course, fore.topsail, fore.topgallant, main.course, main.topsail, main.topgallant, mizzen.topsail, mizzen.topgallant, mizzen.spanker, fore.topmast_staysail, jib
```

Line by line:

1. The ship's time (chapter 6).
2. The true wind, where from and how strong.
3. Her **heading** (where the bow points, as a point and in degrees true), **speed** through the water in knots, **leeway** and **heel** in degrees. Leeway and heel are signed: **positive is to starboard, negative to larboard.** On the starboard tack she heels away from the wind to larboard and is pushed to larboard, so both are negative; after a tack both change sign.
4. The **apparent wind**, angle from the bow and side, and its speed; and the **helm**, the rudder angle, positive when put to starboard. Chapter 4 says how to read the helm.
5. The sails that are set, by their ids.

Nothing in `state` is hidden from the physics or the physics from it: these are the readings a standing order will one day test against (`docs/DesignProposal.md` §4.3).
