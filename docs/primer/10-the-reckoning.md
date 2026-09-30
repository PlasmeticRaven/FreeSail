# 10. The reckoning

Since milestone 5 the ship is on a real sea, and the game keeps two positions of her. The world knows where she is, to the yard, and never tells you. The master keeps his account of where she is, by the log-line, the compass and the noon sun, and that account is what every reading gives, what the chart in the browser draws, and what your landfall is made on. The difference between the two is the passage's game: the world keeps the truth and the captain keeps his account, as he did in 1805. This chapter says how the account is kept, what the master's words mean, and what the orders are.

## The log-line

The ship's speed is had by heaving the log: a flat board on a line, veered from a reel while a sand-glass of twenty-eight seconds runs, the line knotted so that the knots run out in the glass are the miles run in the hour (Falconer, *Log*; Luce 1884, ch. I, "Heaving the Log"). "It is usual to heave the log once every hour in ships of war and East-Indiamen; and in all other vessels, once in two hours" (Falconer), and the game does the same of itself: hourly in a ship of war, which is a ship that musters marines, and every two hours in the schooner, the cutter and the brig. The mate of the watch heaves it with a hand at the reel and one at the glass; the reading is to a quarter of a knot:

```
  Forenoon watch (10:00)  Hove the log: six knots and a half.
```

You may heave it yourself between times:

```orders frigate
heave the log
```

The line is marked short. Luce says lines were cut "3 or 4 feet" under their proper length so that "a ship will generally overrun her reckoning ... since it is best to err on the safe side", and so the game's log reads a few per cent over the truth, by an amount the seed draws for the ship and nobody aboard knows. The reckoning is therefore a little ahead of the ship, which is where a careful master wanted it: he expects the land before he reaches it.

## The traverse

At each heave the master brings up the account: the course steered since the last heave, corrected as he corrects it, and the run at the log's read, laid off on the chart from the last position. His corrections are the period's. He allows the chart's variation, which on his chart of 1794 is a decade old and moving; he allows the leeway he judges by eye when she is close-hauled, and none "whenever the wind is large" (Falconer, *Lee-way*); he allows for a set only if you tell him to (`allow one knot of set to the east`; `allow no set` clears it). What he cannot allow for is the deviation of the ship's own iron on the compass, which in 1805 nobody had a name for, and the drift of the variation since his chart was drawn; those move his account off the truth by a mile or two in every ten, and he never learns it except by the land.

The account is worked at the heave, at noon and when you ask; between times the readings project it forward at the last read. `work up the reckoning` brings it up to the moment and says it:

```orders frigate
work up the reckoning
```

```
The reckoning worked up: 49° 44' N, 5° 05' W by account; run since noon 14 miles, course made good N by E. I would not trust the reckoning within 2 miles east or west, nor a mile north or south.
```

## The master's doubt

The last sentence is the master's own. He keeps, beside the position, how far he would trust it, and the game keeps it as an ellipse about the reckoned position, which the browser's chart draws faintly and never a number. It grows with the run: the quarter-knot of the read and the helmsman's wander grow it as the square root of the hours, and the set of the Channel's streams that he did not allow for grows it in a straight line, east and west above all, so that after a day or two without a sight the ellipse lies long east and west and thin north and south. That is the shape of a captain's worry in the Western Approaches: the latitude he can get at noon, the longitude he cannot.

His doubt is honest about what he knows and silent about what he does not. The log-line's short marking, the chart's stale variation and the ship's deviation are not in it, so the account can be further out than he says. That is not a fault of the model; it is what wrecked *Apollo* in 1804, five days from Cork with no sights and a compass pulled by a new iron tank, her captain believing himself forty miles off the coast. The reading says it in his words:

```
the reckoning's uncertainty is I would not trust the reckoning within 10 miles east or west, nor 2 miles north or south.
```

The book reads it for nothing: `when the reckoning's uncertainty exceeds 20 miles then heave the deep-sea lead` is a line a book may carry.

## The noon sight

At the sun's noon by the ship's clock the master is on deck with his instrument, the sextant in the frigate and the octant in the schooner (the scenario says which), for the last quarter of an hour, and if the sky allows he takes the meridian altitude and the observed latitude replaces the reckoned one; the longitude is carried on by account. The sight has the instrument's error and the horizon's, two miles or so with a good horizon and more in haze or a seaway. Then the day's work: he goes below for half an hour to work the traverse and the log-book's page turns.

```
  Afternoon watch, 8 bells (11:59)  Noon. Latitude by observation 49° 23' N; the reckoning was 49° 27' N. Course made good since the departure N, 56 miles. Longitude by account 4° 58' W.
```

In cloud, rain or fog there is no sight, and the line says so: "Noon. No sight; the sun was hid at noon in fog. Latitude by account 49° 27' N." A captain may ask for the sun himself in the quarter of an hour before noon, `observe the sun`, and out of its hour he is told that the sun is not yet on the meridian or that noon is past; at ten in the forenoon, where this book's blocks stand, the order is refused:

```orders frigate
# rejected: observe the sun
```

Double altitudes when noon is clouded, the chronometer and the lunar are not in this build.

## The lead

Two leads. The hand lead, seven to nine pounds on twenty fathoms of line marked at 2, 3, 5, 7, 10, 13, 15 and 17 with leather and rags that can be told by feel in the dark (Lever, *The Hand-Lead*; Luce 1884, ch. I, *The Lead*), is hove from the chains with way on, and the leadsman calls what he finds: "By the mark seven" at a mark, "By the deep nine" at a deep, "And a half seven", "And a quarter five", "Quarter less five" between. The deep-sea lead, twenty to thirty pounds, is for the Channel Soundings, and "it is usual previously to bring-to the ship" for it (Falconer, *Sounding*), or with a light breeze to pass the line forward along the weather side to the spritsail yardarm and heave from there as she advances (Lever, fig. 506); it takes a dozen hands and a quarter of an hour, and with more than four knots of way on her it does not get bottom. Both leads are armed with tallow, which brings up the ground, "Sand, Coral, Shells, Oaze", by which, "from repeated trials being made and marked in the Charts", a ship's place is known (Lever).

```orders frigate
heave the lead
heave the deep-sea lead
```

```
  Afternoon watch (12:20)  Fifty-two fathoms; fine grey sand with black specks.
  First watch (20:02)  And a quarter seventeen; good ground.
```

A cast is an observation. The master moves his account onto the nearest point of the chart's depth contour that answers the cast and the ground, and his doubt across the contour shrinks to a few miles while along it stays as it was: that is the homeward-bounder's fix, and Rennell's rule for the Channel, "get the latitude, then expect soundings around 49° 30' N, and run in on the soundings". The readings `the depth` and `the ground` are the last cast's, with its age, and the book reads them: `when the depth is under 40 fathoms then heave the lead every glass`; `at a sounding then fill away`.

## Bearings and the landfall

When the lookout raises the land, a bearing of a mark of the chart is a line of position, and the master puts his account on it, at the distance off he judges by eye. Two bearings cross to a point; a transit of the chart's two marks in one is exact. Name the mark as the lookout named it, or say the land for the nearest land in sight (at night, the nearest light):

```orders frigate
take a bearing of the Lizard
take a bearing of the land
```

```
  First dog watch (16:32)  The Lizard bore NNW, four leagues by estimation.
```

The bearing is by compass, as he reads it, so it carries the compass's errors as the traverse does, and the distance is the master's estimate, a fifth out either way as such estimates are, never the truth. A mark not in sight is refused in words. The reading `the bearing of <mark>` gives the bearing of any mark in sight.

The land itself, close aboard in thick weather before any headland is made out, is hailed as the land and counts as land in sight for the book, but it is no mark to take a bearing of.

## The captain's override

The master's account is the master's. If you know better, say so:

```orders frigate
set the reckoning to 49 52 N 6 10 W
```

The account is set there with a fresh doubt of a mile, and everything the master kept of the run since the last fix is forgotten.

## Shaping a course

`shape a course for <place>` reads the reckoning and the chart's places, never the truth: the master lays off the course from where he thinks she is to where the chart puts the place, and the helm is ordered to it. Where the chart has no such place the order is refused with the places it has.

```orders frigate
shape a course for Falmouth
# rejected: shape a course for Timbuctoo
```

```
Shaped a course for Falmouth: NNE by account, 21 miles. Helm ordered: steer NNE (21°).
```

If the account is six miles east of the truth, the course laid off for Falmouth brings the ship to the land six miles west of it, and the first thing the lookout raises tells you so. That is the landfall by the reckoning, and it is the whole game of a passage: the log hove hourly, the sun at noon, the lead in the Soundings, the land when it comes, and the account corrected by each.

## The readings

| Reading | What it gives |
|---|---|
| `the reckoning` | the position by account: "49° 52' N, 6° 10' W by account" |
| `the reckoning's uncertainty` | the master's sentence; the book compares it in miles |
| `the depth`, `the ground` | the last cast, with its age; "no cast yet" before one |
| `the bearing of <mark>` | a mark in sight, by compass |
| `the distance run since noon`, `the course made good` | by account; "no noon yet" before the first |
| `the latitude by observation` | today's, or why there is none |
| `the master` | his name, his place (on deck, below) and what occupies him |
| `what is in sight`, `the land` | the lookout's, as chapter 9's neighbour built them |

Each has its absent pattern, and a ship on the endless plane of the earlier chapters, with no position, has none of them: "No reckoning is kept: the scenario gives no position, and there is no sea here."

## Sources

Falconer 1780, *Dead-reckoning*, *Lee-way*, *Log*, *Log-board*, *Sounding*, *Traverse*, *Quadrant*; Lever 1808, *The Hand-Lead*, *The Deep-Sea Lead* and the passage on arming the lead and getting soundings under way (fig. 506); Luce 1866, "Log-line, Time-glasses"; Luce 1884, ch. I, "The Log", "The Lead"; the Admiralty's Regulations of 1806, the Master's articles XXV to XXXII. The error terms and their sizes are the design study's (`docs/design/Navigation1805.md` §3), and every constant is in `docs/dev/TuningNotes.md` with its source or the word "judgement"; two figures the study could not verify, the Channel's variation in 1805 and the size of a wooden frigate's deviation, are marked so there.
