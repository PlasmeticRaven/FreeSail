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

At each heave the master brings up the account: the course steered since the last heave, corrected as he corrects it, and the run at the log's read, laid off on the chart from the last position. His corrections are the period's. He allows the chart's variation, which on his chart of 1794 is a decade old and moving; he allows the leeway he judges by eye when she is close-hauled, and none "whenever the wind is large" (Falconer, *Lee-way*); and he allows the tide, which he works himself as one more course of the traverse, from his own books and never from the sea ([chapter 13](13-the-tide-and-the-anchor.md) says how). The log gives her way at the moment it is hove, so where she has gained or lost way since the last heave he allows for that by eye, as the officer of the watch did (Falconer, *Log*). Hove to, he reckons her drift by eye and the clock runs on; becalmed, he runs nothing for her and the tide carries the account; only at anchor does the account stand still. What he cannot allow for is the deviation of the ship's own iron on the compass, which in 1805 nobody had a name for, and the drift of the variation since his chart was drawn; those move his account off the truth by a mile or two in every ten, and he never learns it except by the land.

The variation on his chart is ten years old, and what it has moved since is in every course he lays off and every bearing he takes: two or three degrees, which is a mile in every twenty run and half a mile on a mark ten miles off. `observe an amplitude`, as the sun rises or sets, finds the variation as it is today ([chapter 12](12-the-longitude.md)), and the master allows that from then on. It is an order of yours and not his routine: give it on a clear morning or evening before you close the land.

If you know the water better than his books do, give him your own allowance for a set: `allow two knots of set to the west` puts your set into the traverse and into every course shaped, in place of his own tide, until you hand the tide back with `allow the tide by the book`; `allow no set` tells him to allow nothing. Nothing turns your set for you when the tide turns, and the reading `the reckoning` says whose allowance stands.

```orders frigate
allow two knots of set to the west
allow no set
allow the tide by the book
```

The account is worked at the heave, at noon and when you ask; between times the readings bring it up to the moment at her way by the last read, the tide with it. `work up the reckoning` brings it up to the moment and says it, with the tide he is allowing:

```orders frigate
work up the reckoning
```

```
The reckoning worked up: 49° 50' N, 4° 59' W by account. I would not trust the reckoning within two miles east or west, nor two miles north or south. The tide allowed: the ebb, three quarters of a knot to the SW, by the directions for the open Channel and high water at the Lizard by the epitome.
```

## The master's doubt

The sentence in the middle is the master's own. He keeps, beside the position, how far he would trust it, and the game keeps it as an ellipse about the reckoned position, which the browser's chart draws faintly and never a number. It grows by the hour whatever she is doing, except riding at anchor. Under way the quarter-knot of the read and the helmsman's wander grow it as the square root of the hours; his log-line, which he knows may be marked a little long or short, grows it along the course, and his compass across it; and the stream grows it along its own set, since his books give a stream's rate to the half knot and its hour to the half hour. Hove to, it grows by her drift, which he has only by eye; becalmed, by the stream alone. The stream's part stops growing after three hours of a tide, since a stream cannot set her further than it runs. After a day or two without a sight the ellipse lies long east and west and thin north and south. That is the shape of a captain's worry in the Western Approaches: the latitude he can get at noon, the longitude he cannot.

When the doubt lies long and thin and not along the compass's quarters, he says it as it lies: "I would not trust the reckoning within three miles NE and SW, nor a mile across." Under a mile he speaks in cables.

His doubt is honest about what he knows and silent about what he does not. The log-line's short marking, the chart's stale variation and the ship's deviation are not in it, so the account can be further out than he says. That is not a fault of the model; it is what wrecked *Apollo* in 1804, five days from Cork with no sights and a compass pulled by a new iron tank, her captain believing himself forty miles off the coast. The reading says it in his words:

```
the reckoning's uncertainty is I would not trust the reckoning within 10 miles east or west, nor 2 miles north or south.
```

The book reads it for nothing: `when the reckoning's uncertainty exceeds 20 miles then heave the deep-sea lead` is a line a book may carry.

## The noon sight

At the sun's noon by the ship's clock the master is on deck with his instrument, the sextant in the frigate and the octant in the schooner (the scenario says which), for the last quarter of an hour, and if the sky allows he takes the meridian altitude and works it against the reckoned latitude by the one rule below; the longitude is carried on by account. The sight has the instrument's error and the horizon's, two miles or so with a good horizon and more in haze or a seaway. Then the day's work: he goes below for half an hour to work the traverse and the log-book's page turns.

```
  Afternoon watch, 8 bells (11:59)  Noon. Latitude by observation 49° 28' N; the reckoning was 49° 23' N: the account moved three miles to the NNE. Course made good since the departure N, 54 miles. Longitude by account 4° 59' W. The day's work carried the master's tide by the directions and the epitome.
```

In cloud, rain or fog there is no sight, and the line says so: "Noon. No sight; the sun was hid at noon in fog. Latitude by account 49° 27' N." A captain may ask for the sun himself in the quarter of an hour before noon, `observe the sun`, and out of its hour he is told that the sun is not yet on the meridian or that noon is past; at ten in the forenoon, where this book's blocks stand, the order is refused:

## When an observation is believed

A noon latitude, a longitude by lunar or by chronometer, a cast of the lead, a bearing, a transit and a fix are each an observation, and the master believes each by one rule. He sets his own doubt of his account beside his doubt of the observation and does one of three things, and the line in the log says which:

- **Weighed.** Commonly the two are weighed: the account moves toward the observation by as much as the account is the more doubtful of the two. A good sight moves a doubtful account nearly the whole way; a poor sight hardly moves a good one. "... the account moved four cables to the N."
- **Taken.** When the two stand further apart than their doubts together allow (twice the two doubts added), the account is plainly out: he lays it down on the observation and takes the observation's doubt for his own in that direction. "... the reckoning was out by it; laid down by the observation: moved five miles to the S." This is Falconer's "the reckoning is always to be corrected, as often as any good observation can be obtained", kept for the case it was written for.
- **Kept.** When the weighing would move the account less than half a cable, he keeps it. "... which he would trust within 25 miles, and the account within two miles: the account kept."

The same thing seen again tells him nothing new. A second bearing of one mark from the same place, a second cast on the same ground, a second fix by the same marks all carry the same compass, the same chart and the same allowance for the tide as the first, so they do not make him surer than the first did. The lookout's distance by estimation is only ever weighed: an eye's guess does not lay an account down. The rule does not look at how far she has run since the last observation, as it did before; what it looks at is the two doubts.

The rule is as good as the doubts are honest. An observation whose own doubt is said too small can lay down a good account wrongly: a chronometer whose rate has gone further out than the master allows will do it, and the next bearing of the land puts it back. Read the line; it says what he did and by how much.

```orders frigate
# rejected: observe the sun
```

Double altitudes when noon is clouded are not in this build. The chronometer, the time sight, the lunar and the amplitude are [chapter 12, the longitude](12-the-longitude.md), which has them in the master's words, with every form their orders take and the readings they carry (`the chronometer`, `the longitude by chronometer`, `the longitude by lunar`, `the chronometer's error by lunar`, `the moon`, `the variation`), and the chart in the captain's hands (`the bearing of <mark> by the chart`, `the distance to <mark>`, `the dangers`, and what `shape a course for <place>` says of a rock on the line).

## The lead

Two leads. The hand lead, seven to nine pounds on twenty fathoms of line marked at 2, 3, 5, 7, 10, 13, 15 and 17 with leather and rags that can be told by feel in the dark (Lever, *The Hand-Lead*; Luce 1884, ch. I, *The Lead*), is hove from the chains with way on, and the leadsman calls what he finds: "By the mark seven" at a mark, "By the deep nine" at a deep, "And a half seven", "And a quarter five", "Quarter less five" between. The deep-sea lead, twenty to thirty pounds, is for the Channel Soundings, and "it is usual previously to bring-to the ship" for it (Falconer, *Sounding*), or with a light breeze to pass the line forward along the weather side to the spritsail yardarm and heave from there as she advances (Lever, fig. 506); it takes a dozen hands and a quarter of an hour, and with more than four knots of way on her it does not get bottom. Both leads are armed with tallow, which brings up the ground, "Sand, Coral, Shells, Oaze", by which, "from repeated trials being made and marked in the Charts", a ship's place is known (Lever).

```orders frigate
heave the lead
heave the deep-sea lead
```

```
  Afternoon watch (12:18)  Fifty-five fathoms; fine grey sand with black specks. The account kept.
  First watch (20:02)  And a half fifteen; good ground. The account moved a cable to the ENE.
```

A cast is an observation. The master looks for the nearest place on his chart that answers the cast and the ground, and works it by the rule above as a line across the bottom's slope there. It is as good a line as the bottom is steep: where the chart shelves a fathom or two in a mile a cast places her to a mile or two, and over a flat bottom it is no line at all and narrows nothing, however often the lead is hove. A second cast on the same ground narrows nothing further. Where the chart about his account already shows less water on one hand and more on the other than the cast, the cast agrees with the account and he keeps it. This is still the homeward-bounder's fix, and Rennell's rule for the Channel, "get the latitude, then expect soundings around 49° 30' N, and run in on the soundings". The readings `the depth` and `the ground` are the last cast's, with its age, and the book reads them: `when the depth is under 40 fathoms then heave the lead every glass`; `at a sounding then fill away`.

## Bearings and the landfall

When the lookout raises the land, a bearing of a mark of the chart is a line of position, and the master works his account against that line by the rule above: one bearing says which way the mark lies, and how far off she is only by the lookout's eye. Two or three bearings cross to a point, which is a fix (below); a transit of the chart's two marks in one is exact. Name the mark as the lookout named it, or say the land for the nearest land in sight (at night, the nearest light):

```orders frigate
take a bearing of the Lizard
take a bearing of the land
```

```
  First dog watch (16:26)  The Beast bore NNW, four leagues by estimation: the account moved three leagues to the SW.
```

The bearing is by compass, as he reads it, so it carries the compass's errors as the traverse does, and his doubt of a bearing's line grows with the distance of the mark for that reason: two and a half degrees, or a degree and a half once he has observed the variation, is a quarter of a mile at five miles and half a mile at ten. The distance in the line is the lookout's estimate by eye, a fifth out either way as such estimates are, never the truth; it is judged afresh as she closes or opens the mark. It is weighed with the bearing, along the line of sight, and counts for much only when the master's own doubt that way is the greater: at a landfall on one headland after a long run, or a departure. The line says how far the account moved, or that it was kept:

```
  First dog watch (16:30)  The Beast bore NNW, four leagues by estimation: the account kept.
```

A second bearing of the same mark from the same place moves nothing, for the reason given above; from a new place it is a new line. When the account's own distance from the mark differs from the lookout's by more than a third the line says both, and that disagreement is worth a second look at the chart:

```
  Forenoon watch (10:00)  St Anthony's Head bore NW by N, six miles by estimation; five leagues by the account.
```

A mark not in sight is refused in words. A bearing of a sail is given and moves nothing: she is no mark of the chart. The reading `the bearing of <mark>` gives the bearing of any mark in sight.

## A fix by cross bearings

With two or three charted marks in sight whose bearings cut well, the master takes them at one stroke and works the point where the lines cross against his account, by the same rule: weighed, taken when the account is plainly out, kept when it would move under half a cable. A good fix still rules a doubtful account, and a poor one, by far marks that cut fine, no longer moves a good account: "... good to four cables, the fix the poorer figure; the account kept, within half a cable of it."

```orders frigate
take a fix
take a fix by Manacle Point and St Michael's Mount
```

```
  Forenoon watch (10:00)  Fixed by cross bearings: Black Head SW by W, St Anthony's Head NW by N, the Deadman NE by N; the lines met within six cables. The account moved three leagues and a half to the NW: 50° 05' N, 4° 57' W by the fix, good to three cables.
```

Said bare, the master chooses the marks: of all the sets of two or three in sight that cut by thirty degrees or more, the set that leaves him the least doubt, which sets a near mark before a far one, since a bearing's doubt grows with the distance. In the Goulet, under Petit Minou, he takes Petit Minou, Camaret and Portzic, each within three miles, and not Brest and Conquet five miles off; the Mingan lies in one line with Petit Minou there and adds nothing to it. Name two or three to choose them yourself, joined by `and`. The marks are headlands, lights, marks and a danger that shows; never the shore close aboard, a sail or a transit. Two lines that cut by less than thirty degrees are no fix, and the refusal says so with how the marks bear; with one mark only in sight it says to take a bearing of it. With three marks the lines seldom meet in a point, and the triangle they make (the cocked hat) is said: a large one means a bearing or the compass is out. "Good to" is his doubt of the fix: the marks' distances, the compass's allowance, which is the same in every bearing of the set, and half the cocked hat. The line is notable when the account moved more than a mile. `every glass, if the land is in sight then take a fix` is a sound standing order in pilot waters, and `at a fix` is an event for the book.

The compass's own error is common to every bearing of a set, so a fix carries it, and the master allows for it in "good to". What he allows is his chart's figure for the variation; what the compass is really out by may be more. With every mark in one quarter of the compass a fix can stand three cables from the truth and say two, and the lead, or a mark on the other hand, is the check on it.

## The nearest land, and land ahead

Within a league of any shore by day (a mile on a dark night, the visibility in thick weather) the lookout has the shore itself in sight beside whatever headlands are, and hails it once: "The land about Rame Head on the larboard bow, bearing NW, distant a mile", and "close aboard" within a mile. The reading `the nearest land` (or `the nearest shore`) is that sighting at any moment, in his words:

```
  Forenoon watch (10:02)  The nearest land: the land about Rame Head, on the larboard bow, bearing NW, nine cables.
```

Beyond a league it reads "no land within a league"; by night or in thick weather, when he cannot see so far, "not to be seen" with how far he can see, and what lies beyond that he cannot say. The book compares it in miles, by what he said: `when the nearest land is under half a mile then heave the lead`.

When she has way on and is standing into the land, the lookout says so without being asked. He watches her course made good, a point either side of it, for the first dry ground at the present state of the tide or a danger that shows:

```
  Forenoon watch (10:07)  Land ahead, fine on the larboard bow, six cables: she is standing into it.
  Forenoon watch (10:13)  Land close ahead, two cables! She will be on it in three minutes.
```

The first is a notable line, said when she would be on it in under ten minutes at her present speed over the ground; the second is urgent, under four minutes, and wakes a station that is standing by. Each is said once an approach, and again only after she has stood clear for five minutes. A charted danger is named ("The Manacles ahead, fine on the starboard bow, four cables: she is standing into danger"). The events are `land ahead` and `land close ahead`. He warns only of what he can see: at night within the mile, and in fog not at all, where the lead is the guard. He sees dry ground and rocks that show, not shoal water: a ship can take the ground before the land ahead is close.

The land itself, the nearest shore, is hailed as the land and counts as land in sight for the book, but it is no mark to take a bearing of or to fix by.

## The captain's override

The master's account is the master's. If you know better, say so:

```orders frigate
set the reckoning to 49 52 N 6 10 W
```

The account is set there with a fresh doubt of a mile, and everything the master kept of the run since the last fix is forgotten.

## Shaping a course

`shape a course for <place>` reads the reckoning and the chart's places, never the truth. The master lays off the line from where he thinks she is to where the chart puts the place, and the helm is ordered the course to steer so that she makes that line good: against the tide he is allowing at that hour (his own, or yours), with the leeway he allows when she must lie close-hauled, at her way by the log's last read or by eye. The words give both the line and the course, and how long the allowance holds. It is worked once, when the course is shaped, and again each time a standing order shapes one; the master does not alter the helm of himself when the tide turns, so shape it again then (`at the turn of the tide by the reckoning` is an event for the book). Where the chart has no such place the order is refused with the places it has.

```orders frigate
shape a course for Falmouth
# rejected: shape a course for Timbuctoo
```

```
Shaped a course for 50° 02' N, 4° 58' W: NNE by account, 14 miles. Allowing the flood, a knot and a quarter to the E, steer N by E to make it good; the allowance holds till the tide turns, about half past five in the evening. Helm ordered: steer N by E (11°).
```

The line is tried against the land and the charted dangers, and the words say what it meets: "the line passes the Manacles within a mile", "the line crosses the land about Black Head", "the line passes the shore under Petit Minou within two cables". The chart's coast is your own paper, so this gives nothing away; a course across a headland is still ordered, and it is yours to shape another. With no way on her there is no allowance to work ("She has no way on to work an allowance by ...; shape it again when she has gathered way"), and where the stream is too strong for her way the words say that no course makes it good and give the one that loses least.

If the account is six miles east of the truth, the course laid off for Falmouth brings the ship to the land six miles west of it, and the first thing the lookout raises tells you so. That is the landfall by the reckoning, and it is the whole game of a passage: the log hove hourly, the sun at noon, the lead in the Soundings, the land when it comes, and the account corrected by each.

## The readings

| Reading | What it gives |
|---|---|
| `the reckoning` | the position by account, and the tide allowed in it and by whom: "49° 50' N, 4° 59' W by account; the tide allowed: the ebb, three quarters of a knot to the SW, by the directions for the open Channel and high water at the Lizard by the epitome" |
| `the reckoning's uncertainty` | the master's sentence, as his doubt stands at this moment; the book compares it in miles |
| `the depth`, `the ground` | the last cast, with its age; "no cast yet" before one |
| `the bearing of <mark>` | a mark in sight, by compass |
| `the distance run since noon`, `the course made good` | by account; "no noon yet" before the first |
| `the latitude by observation` | today's, or why there is none |
| `the master` | his name, his place (on deck, below) and what occupies him |
| `what is in sight`, `the land` | the lookout's, as chapter 9's neighbour built them |
| `the nearest land` | the nearest shore within a league as the lookout sees it: where it lies from her head, its bearing, its distance by estimation, the coast's name |

Each has its absent pattern, and a ship on the endless plane of the earlier chapters, with no position, has none of them: "No reckoning is kept: the scenario gives no position, and there is no sea here."

Every reading may be asked at the prompt: type its words, alone or after `what is` or `ask the master`, and the answer is a line of the log in the same words the instruments and a model's `readings` give, and nothing more:

```
  Afternoon watch (12:29)  The reckoning: 49° 23' N, 4° 58' W by account.
  Afternoon watch (12:30)  The master: Mr Harvey, on deck.
  Afternoon watch (12:32)  The bearing of the Lizard: not in sight.
```

A question is never journaled and changes nothing aboard; a reading the ship has not got answers so ("The ship has no well to sound yet; that reading comes with the world.").

## Every form, in a table

Every way the grammar takes each of the master's orders and each of the reckoning's readings; the first form of a row is the one this chapter uses, the rest are taken the same. A test in the repository (`tests/test_primer.py`) reads this table and gives every form in its first two columns to the frigate off the Lizard, and fails if any is not understood. The names of marks and places are examples: a mark is named as the lookout names it, or by any of its words when one mark in sight answers to them (`manacle` for Manacle Point; the Manacles themselves, the rocks, are another feature and the refusal says so), or `the land`, or `the light`.

| Order or reading | Also taken | What it does |
|---|---|---|
| `heave the log` | `heave log`, `heave the log line` | the log hove now; hourly of itself in a ship of war |
| `heave the lead` | `heave lead`, `heave the hand lead`, `sound with the hand lead`, `a cast of the lead`, `get a cast of the lead`, `try the lead`, `take a sounding`, `get a sounding`, `sound`, `sound with the lead`, `cast the lead` | the hand lead from the chains, to twenty fathoms |
| `heave the deep-sea lead` | `heave the dipsey lead`, `strike soundings`, `try for soundings`, `sound with the deep-sea lead`, `get a cast of the deep-sea lead`, `a cast of the deep-sea lead` | the deep-sea lead, with the ship brought to or the line passed forward |
| `take a bearing of the Lizard` | `take the bearing of the Lizard`, `take a bearing on the Lizard`, `bearing of the Lizard`, `take bearings of the Lizard`, `get a bearing of the Lizard`, `take a bearing of the land`, `take a bearing of the light`, `take a bearing of Lizard Point`, `take a bearing of lizard` | a line of position from a mark in sight; refused in words when it is not |
| `take a fix` | `take a fix by Black Head and St Anthony's Head`, `take a fix by Black Head, St Anthony's Head and the Deadman`, `fix her position`, `fix the position`, `take cross bearings`, `take cross bearings of Black Head and St Anthony's Head`, `cross bearings`, `get a fix` | cross bearings of two or three charted marks in sight, the account set at their crossing; the master chooses the marks when none is named |
| `work up the reckoning` | `work the reckoning`, `work up the dead reckoning`, `bring up the reckoning`, `the day's work`, `work up a reckoning`, `work up reckoning`, `work up the reckoning's uncertainty`, `work up the reckoning's doubt` | the account brought up to now, with the master's doubt |
| `observe the sun` | `take the sun`, `take a sight of the sun`, `take the noon sight`, `take the sun's altitude`, `observe the sun at noon`, `take a meridian altitude` | the noon sight by order, in the quarter of an hour before noon |
| `set the reckoning to 49 52 N 6 10 W` | `set the reckoning at 49 52 N 6 10 W`, `correct the reckoning to 49 52 N 6 10 W`, `put the reckoning at 49 52 N 6 10 W` | the captain overrides the master |
| `allow one knot of set to the east` | `allow for one knot of set to the east`, `allow half a knot of set to the south west`, `allow no set` | your own set in the traverse and in a course shaped, in place of the master's tide until you hand it back |
| `allow the tide by the book` | `allow the tide`, `allow for the tide`, `allow the tide by the directions`, `allow the master's tide`, `work the tide yourself`, `work the tide by the book`, `reckon the tide by the book`, `hand the tide back`, `hand back the tide` | the tide in the reckoning handed back to the master |
| `shape a course for Falmouth` | `shape a course to Falmouth`, `shape course for Falmouth`, `lay a course for Falmouth`, `set a course for Falmouth`, `make for Falmouth`, `steer for Falmouth`, `head for Falmouth` | the course to steer to make good the line from the account to a place of the chart, the tide allowed |
| `the reckoning` | `the dead reckoning`, `the position by account`, `the position`, `what is the reckoning`, `ask the master the reckoning`, `ask the master for the reckoning` | the position by account |
| `the reckoning's uncertainty` | `the uncertainty`, `the reckoning's doubt`, `the master's doubt`, `what is the reckoning's uncertainty`, `take the reckoning's uncertainty` | the master's doubt in his words |
| `the depth` | `the last cast`, `the soundings`, `what is the depth` | the last cast, with its age |
| `the ground` | `the bottom`, `what is the ground` | what the arming brought up at the last cast |
| `the bearing of the Lizard` | `what is the bearing of the Lizard`, `ask the master the bearing of the Lizard` | a mark in sight, by compass |
| `the distance run since noon` | `the run since noon`, `the distance run` | by account; before the first noon, the run since the departure |
| `the course made good` | `what is the course made good` | since noon, by account |
| `the latitude by observation` | `the observed latitude`, `the latitude` | today's noon latitude, or why there is none |
| `the master` | `what is the master` | his name, his place and what occupies him |
| `what is in sight` | `the sightings`, `sightings` | the lookout's sightings, by bearing and estimated distance |
| `the land` | `what is the land` | whether any land is in sight, and the nearest |
| `the nearest land` | `the nearest shore`, `what is the nearest land` | the nearest shore within a league as the lookout sees it |
| `the depth of water` | `the water` | the chart's depth where she is (the truth's chart, which the lead finds and the master does not see) |

In the book, the same readings are the standing dialect's (chapter 11, the starting book, has the dialect whole); every one of these is taken, and the test reads them too:

| Condition or event | What it waits for |
|---|---|
| `when the reckoning's uncertainty exceeds 20 miles` | the master's doubt grown past twenty miles |
| `when the depth is under 40 fathoms` | a cast under forty fathoms |
| `when the ground is sand`, `when the ground is not rock` | the arming's ground at the last cast |
| `when the distance run since noon exceeds 20 miles` | the run by account |
| `when the reckoning is north of 49 30 N`, `when the reckoning is west of 6 W` | the account past a latitude or a longitude |
| `when the land is in sight`, `when the land is not in sight` | the lookout's word |
| `when the nearest land is under half a mile`, `when the nearest shore is under 2 miles` | the shore's distance as the lookout says it |
| `at a fix`, `at land ahead`, `at land close ahead` | a fix by cross bearings taken; the lookout's warning, and his urgent one |
| `at the turn of the tide by the reckoning` | the master's own tide turning, under way as at anchor: the moment to shape a course again |
| `when the master is on deck`, `when the master is below` | the master's place |
| `at noon`, `at a sounding`, `at a sighting`, `at a landfall` | the day's work, a cast, the lookout's hail, the land raised |
| `at hove to`, `at filled away`, `at tacked`, `at wore` | a manoeuvre's end |
| `if she is hove to`, `if she is not hove to`, `when the manoeuvre in hand is tacking`, `when the manoeuvre in hand is none` | what she is about: hove to (from the moment the heave-to begins until she fills away), tacking, wearing, heaving to, filling away, or none |

## Sources

Falconer 1780, *Dead-reckoning*, *Lee-way*, *Log*, *Log-board*, *Sounding*, *Traverse*, *Quadrant*; Lever 1808, *The Hand-Lead*, *The Deep-Sea Lead* and the passage on arming the lead and getting soundings under way (fig. 506); Luce 1866, "Log-line, Time-glasses"; Luce 1884, ch. I, "The Log", "The Lead"; the Admiralty's Regulations of 1806, the Master's articles XXV to XXXII. The error terms and their sizes are the design study's (`docs/design/Navigation1805.md` §3), and every constant is in `docs/dev/TuningNotes.md` with its source or the word "judgement"; two figures the study could not verify, the Channel's variation in 1805 and the size of a wooden frigate's deviation, are marked so there.
