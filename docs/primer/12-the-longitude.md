# 11. The longitude

Chapter 10 left the master with a latitude he could get at noon and a longitude he could only carry by account. This chapter gives him the two ways the period had of finding it, the chronometer and the lunar, and the azimuth compass that corrects his chart's variation; then the chart in his hands, so that a captain may ask what a charted mark bears by account, what dangers lie about him, and whether the course he has shaped passes a rock. Everything here is drawn from the truth the world keeps plus an error from the seed, scaled by the master's skill, the sea and the sky, and nothing is computed from the model's own geometry: the Almanac's arithmetic is the master's, and the game models its outcome, as it models a topsail's setting without each hand's grip.

## The chronometer

In 1805 the Navy issued no chronometers. A frigate had one if her captain had bought it (Bligh paid forty guineas for an Earnshaw), and no sloop or schooner had one unless her scenario says. The scenario file gives it under `ship:`:

```
  chronometer: {maker: Earnshaw, where: Plymouth, rated: 1805-04-26, rate_s_per_day: 1.8, drift: seeded}
```

A chronometer is not set right; it is *rated*. Its daily gain or loss was found ashore against a known meridian and written on a certificate, and the master applies the rate times the days since rating. The trouble was the rate changing: Bligh logged K2 at "between 1.1 and three seconds" a day, "and that it had varied irregularly". The game keeps the certificate's rate as what the master applies and a drift from it as what the world knows: `drift: seeded` draws one to three seconds a day either way from the seed, a number is the drift itself, and none is a rate that is right. Four seconds of time is a mile of longitude at the equator, two-thirds of a mile at 50 N; a rate wrong by two seconds a day is half a degree in two months.

The master winds it at eight in the morning, when the watch is relieved, and the log says so. A chronometer not wound is a dead one: it is a two-day movement and runs down fifty-six hours after its last winding, so a master who forgets two mornings running (the scenario says when, `forgotten: [1805-06-06, 1805-06-07]`) finds it stopped, a notable line in the log. You may wind it yourself at any hour, and a dead one wound by order is set going again by the deck watch, which keeps the ship's time by the account, so it carries the account's longitude error in its time until a lunar corrects it. `compare the watches` sets it beside the deck watch.

```orders frigate
# rejected: wind the chronometer
# rejected: compare the watches
```

Both are refused in the frigate of this book, who carries none: "There is no chronometer aboard: the longitude is by account, and by lunar when the moon serves." The reading `the chronometer` gives its time at Greenwich as the master reads it, the days since its rating and its winding, and behind the words the master's trust in it in miles of longitude, which widens by a second a day since rating, so the book may say `when the chronometer exceeds 10 miles then take a lunar`.

## The time sight

With a chronometer the longitude is had from the sun in the forenoon or the afternoon: its altitude with the latitude and the day's declination gives the local hour angle, and against the chronometer's Greenwich time the difference is longitude. The game draws the outcome: the true longitude, plus the chronometer's error in time (the drift times the days and the rating's own few seconds; a chronometer that is fast puts her to the westward), plus the sight's own two or three miles. It is refused in cloud, with the sun under ten degrees, and within an hour and a half of the meridian, where the hour angle changes slowly against the altitude; and the master is below twenty minutes working it.

```orders frigate
# rejected: take a sight for the longitude
```

```
  Forenoon watch (08:00)  Forenoon. The sun's altitude for the time: longitude by chronometer 5° 02' W, the Earnshaw 40 days from Plymouth; the reckoning was 5° 02' W. Mr Harvey would trust it within 15 miles.
```

The reckoning's east-west doubt collapses to the sight's, as the noon sight collapses the north-south; its north-south is left as it was. `the longitude by chronometer` is today's, with the days since rating and the master's trust; before one, "no sight for the longitude today", or the reason there can be none.

## The moon and the lunar

The moon moves against the stars about half a degree an hour, so the angle between the moon and the sun or a bright star near the ecliptic is a clock face readable from anywhere, and the *Nautical Almanac* tabulated those distances for Greenwich time at three-hour intervals, for the sun and nine stars. The master measures the distance with a sextant while two mates or midshipmen take the two bodies' altitudes, *clears* the distance of refraction and parallax, and interpolates the Almanac; a quarter of an hour on deck for a set of distances, and half an hour to an hour of arithmetic below. Lunars were common after 1790 and were what the Almanac, Norie's Epitome and Bowditch were for; a schooner with no chronometer has no honest longitude without them.

The game keeps a moon good to a degree (`freesail/core/moon.py`, Meeus's method with the leading terms) for its age, its phase, where it stands, its distance from the sun and from the nine lunar stars (Hamal, Aldebaran, Pollux, Regulus, Spica, Antares, Altair, Fomalhaut and Markab), and the night's light. `the moon` reads it:

```
the moon is twelve days old, waxing; up, forty degrees high; in distance of the sun
```

`take a lunar` checks the conditions from it and refuses in words that say which: no lunar within three days of new moon ("No lunar to be had: the moon is two days old"), with the moon down or under fifteen degrees, with no body at a tabulated distance (the sun between forty and a hundred and twenty degrees from the moon by day; a star at the same range by night, when the moon lights the horizon), or with the sky thick. Allowed, it occupies the master and two of the young gentlemen on the quarterdeck for a quarter of an hour, a crew cost the runner charges as it charges a brace, and an hour of ship's time later the log gets the result, *drawn and not computed*: the true longitude plus an error from the seed, a quarter of a degree for a good master on a quiet day and a degree for a poor one in a seaway (ten to thirty-nine miles at 50 N), widened when the moon's distance from the body closes slowly. The engine never clears a distance.

```orders frigate
take a lunar
# rejected: take a lunar of Aldebaran
# rejected: take a lunar of Sirius
```

In this book's world, at ten in the forenoon of 1 June with a four-day moon seventeen degrees up and the sun in distance, the lunar of the sun is taken; Aldebaran is refused by day, and Sirius because the Almanac has no distances for it. Say `take a lunar of the sun` or `of <star>` to choose the body, or `take a lunar` for whatever serves. The log an hour later:

```
  Afternoon watch (18:57)  A set of distances of the sun and the moon taken by Mr Harvey and two of the young gentlemen, and cleared: longitude by lunar 5° 07' W, which he would trust within 20 miles; the reckoning was 5° 24' W. The Earnshaw gave 5° 22' W, and he thinks it gaining on its rate, by a minute and nine seconds.
```

The reckoning is updated by it, east and west; `the longitude by lunar` is the last one, with its date and the master's trust; and `the chronometer's error by lunar` is the difference between the lunar's longitude and the chronometer's, which is how a rate was checked at sea and the reason a captain with a chronometer still wanted a lunarian. Whether to believe the lunar or the chronometer when they disagree by twenty miles is the judgement the period's captains made, and the two lines are all a captain at the table has to make it with.

## The amplitude and the azimuth

The variation the master allows is his chart's, the 1794 reissue of Mountaine and Dodson's lines, a decade old and moving; the world's is the true variation of the Channel in 1805, about two points west, and the difference is a bias in every course he lays down that he never learns of except by the land. Robertson's rule was that mariners "should every day, or as often as they had opportunity" observe an amplitude or azimuth to find the variation where they are (Falconer, *Variation*): the sun's bearing by the azimuth compass as it rises or sets against its true amplitude from the declination and the latitude, or by day against its true bearing from its altitude. The game gives both; the result is the variation by observation, to a degree, read to the half degree as the compass's brass edge is divided, and the master allows it in the reckoning from then on in place of the chart's.

```orders frigate
observe an azimuth
# rejected: observe an amplitude
```

The amplitude is refused with the sun well up, as it is at ten in the forenoon; it is taken a quarter of an hour either side of sunrise and sunset, and both are refused in cloud. The log:

```
  Morning watch (04:20)  Observed the sun's amplitude at its rising, bearing E by N by compass: variation of the compass 24° W by amplitude, 10 June, where the chart gave 21° 30' W by the chart of 1794; Mr Harvey allows it in the reckoning from now.
```

`the variation` reads what he allows, with its source and its date: `21° 30' W by the chart of 1794` until he observes, then `24° W by amplitude, 10 June`; the book compares it in degrees.

## The chart in the captain's hands

The chart the master works on is in the browser and in three readings that read the account and never the truth, in sight or not: `the bearing of <mark> by the chart` and `the distance to <mark>` for any charted feature ("N by W by account, 51 miles"), and `the dangers`, the charted rocks, ledges and shoals within ten miles of the account, the nearest first, by name, bearing and distance:

```
the dangers are the Spanam WNW, 4 miles; the Craggan NW by W, 5 miles; the Rose WNW, 5 miles; the Stags W by N, 6 miles; the Manacles N by E, 7 miles; the Penwin and the Vaze N by E, 8 miles: by account, within 10 miles
```

Behind the words is the nearest danger's distance, so `when the dangers are under 3 miles then heave to` is a line the book reads. And `shape a course for <place>` now says when the straight line from the account passes a charted danger within a mile, or crosses it:

```
Shaped a course for Falmouth: N by account, 13 miles; the line passes the Manacles within a mile. Helm ordered: steer N (0°).
```

That is the warning the master could give; the pilot of a later chapter is the better answer. The helm rules of the book have no guard against bearing away toward a rock, and that is the captain's business. Two events for the book and the watcher go with it: `a danger sighted`, the lookout's hail of a rock or a ledge, and `a bearing steady and closing`, his hail of a danger (or the land within a league) whose bearing has held within a point for ten minutes while the distance closed, which is the seaman's rule for a collision course.

## The lookout's distances

The lookout's "distant four leagues" is his eye's judgement, a sixth out either way as such estimates are, drawn once for each sighting of a mark and held until the ship has made a mile from where he judged it, so a calm does not have him call the Start four miles, four leagues and three leagues in an hour; it is the same figure in `what is in sight`, in the hail and in a bearing taken. The reading names the dangers first, then the lights, the land and the marks, nearest first within each, and its cap of eight never cuts a danger off; a mark's name is whole mid-sentence ("Black Head", not "black Head"). He says when the chart ends ("the chart has nothing to the eastward of this"), and on a moonlit night, the moon up and more than half full, he makes out the land at a league where a dark night shows it at a mile. A light at night is seen in thick weather by its luminous range, a strong light's loom carrying where a headland does not: a twenty-mile light at about ten miles in four miles' visibility, at three in a mile's, and in fog not at all.

## Every form the longitude's orders take

| Order | Also | What it does |
|---|---|---|
| `take a sight for the longitude` | `take a time sight`, `take the sun for the longitude`, `observe the sun for the time` | the longitude by chronometer; refused without one, in cloud, with the sun low or near the meridian |
| `take a lunar` | `take a lunar of the sun`, `take a lunar of <star>`, `take a set of distances`, `take a lunar distance` | a set of distances; the result an hour later; refused in the registry's words |
| `wind the chronometer` | `wind up the chronometer`, `wind the timekeeper` | wound by order (daily of itself at eight) |
| `compare the watches` | `compare the chronometer`, `compare watches` | the chronometer against the deck watch |
| `observe an amplitude` | `take an amplitude`, `observe the sun's amplitude` | the variation at sunrise or sunset |
| `observe an azimuth` | `take an azimuth`, `observe the sun's azimuth` | the variation by day, with the sun's altitude |
| `shape a course for <place>` | `steer for <place>`, `lay a course for <place>` | chapter 10's course, now with the dangers its line passes |

```orders frigate
# rejected: take a time sight
# rejected: take the sun for the longitude
# rejected: wind up the chronometer
# rejected: compare the chronometer
take an azimuth
observe the sun's azimuth
# rejected: take an amplitude
take a lunar of the sun
# rejected: take a set of distances
```

The time sight's forms parse and are refused for want of a chronometer (the refusal is the master's, "there is no chronometer aboard", not the grammar's); the chronometer's likewise; the azimuth's are taken; the amplitude's refused for the hour; the lunar of the sun is taken, and the set of distances asked for after it is refused because the master is already at the lunar: "Mr Harvey is on deck at the lunar; wait for him."

## The readings

| Reading | What it gives |
|---|---|
| `the chronometer` | its time at Greenwich, the days since rated, its winding; the master's trust in miles behind it |
| `the longitude by chronometer` | today's time sight, with the days since rated and the master's trust |
| `the longitude by lunar` | the last lunar, with its date and the master's trust |
| `the chronometer's error by lunar` | gaining or losing on its rate, in time and in miles of longitude |
| `the moon` | its age and phase, up or not, in distance of a body or not; "in sight" for the book when up and the sky clear |
| `the variation` | what the master allows, by the chart or by observation, with its date |
| `the bearing of <mark> by the chart`, `the distance to <mark>` | from the account to any charted feature, in sight or not |
| `the dangers` | the charted dangers within ten miles of the account, the nearest first |

## Sources

Falconer 1780, *Azimuth-compass*, *Variation*; the Admiralty's Regulations of 1806, Nos. 26 and 28, the Form of Remark Book (the lunar's and the chronometer's columns); Luce 1884, ch. XX, the ship's routine at sea (the chronometers wound at eight); White 1835 and Imray 1874 on the Lizard's lights in clear and thick weather and on the Nare; Meeus, *Astronomical Algorithms*, chapters 12, 13, 21, 25, 47, 48 and 49 for the moon; the design study `docs/design/Navigation1805.md` §2 to §5 for the chronometer's and the lunar's figures (de Grijs 2020, Bligh's K2, the Board of Longitude's witnesses), whose unverified ones (the hour to clear a distance, the variation of the Channel in 1805) are marked so in `docs/dev/TuningNotes.md`.
