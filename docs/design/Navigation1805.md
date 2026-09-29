# Design study: navigation in 1805, and whether the game takes lunars

From the owner's ruling 3 of 2026-09-29 on the M5 scoping draft: milestone 5 keeps two
positions apart, where the ship is and where she is reckoned to be, and the captain
navigates by the period's means; the lead recommended the floor (dead reckoning, the
lead, bearings, a noon latitude) plus a chronometer as a scenario item and no lunars, and
the owner asked why not, and wants the question explored before deciding. A design note
for the 5b section of the M5 specification; not itself a specification.

Reads with: `docs/TechnicalSpec-M5.md` §3 (5b) and §4; `docs/DesignProposal.md` §5.2
"Navigation" and §9; `docs/design/InwardAndOutward.md` (a feature exists when it has an
order or a reading); `docs/design/Papers-and-Books.md` (the Almanac and the Epitome as
things aboard). Sources are listed at the end with what was and was not verified; the
repository's own texts are cited by work and article as `docs/references/README.md` asks.

## 1. What the navigator actually did, 1805

### The frigate's master

The 1806 Regulations (the printing in `docs/references/admiralty/`, Master's articles
XXV to XXXII) make the master the navigator: he is "to provide himself with such Charts,
nautical Books, and Instruments as are necessary for astronomical observations and all
other purposes of Navigation" (XXV); he has, under the captain, "the charge of navigating
the Ship", is to be on deck whenever she approaches land or shoals, "always sounding to
inform himself of the situation of the Ship" (XXVI); and "every day at noon, or as soon
after as can be done", he delivers to the captain "the latitude and longitude she is in,
the variation of the compass; the bearing and distance of the place sailed from, or of
that to which the Ship is bound" (XXVII). He is to ascertain the latitude, longitude and
variation of every headland he passes, "the setting and velocity of the currents; the time
of high water at the full and change of the Moon" (XXVIII), to examine the charts of every
coast and record his opinion of their accuracy (XXXI), and to keep the log-book, written
by his mates and compared daily with the log-board (XXXII). The lieutenant of the watch is
not excused: he is "constantly to ascertain the latitude by observation at noon or by
double altitudes" and to keep his own account of the ship's way, "the course steered and
the distance run for each twenty-four hours, with the latitude and longitude she is in,
and the bearings and distance of some principal head-land" (Lieutenant, XVII). The
schoolmaster, examined by Trinity House in "the theory and practice of navigation", teaches
the young gentlemen (Schoolmaster, I and II). So on a frigate there were several people
working the reckoning independently every day, and one man answerable for it.

The day's round, from the period's own words:

- **The log, every hour.** "It is usual to heave the log once every hour in ships of war
  and East-Indiamen; and in all other vessels, once in two hours" (Falconer 1780, *Log*).
  The mate of the watch heaves it, one man holds the reel, another the glass; 12 to 15
  fathoms of stray line carry the chip clear of the wake before the glass is turned. If the
  wind has changed in the interval "the officer generally makes a suitable allowance for it,
  at the close of the watch". Falconer's line is 50 feet to the knot for a 30-second glass;
  the later standard was 47 feet 3 inches for 28 seconds; Luce (1866, *Log-line, Time-glasses*)
  says lines were deliberately marked 3 or 4 feet short so that the ship overruns her
  reckoning, "since it is best to err on the safe side", and that the glass "runs slower in
  damp weather than in dry" and must be tried against a pendulum; a following sea "will
  bring home the log", for which "it is customary to allow one mile in ten".
- **The traverse board and the log-board.** The helmsman pegs the course sailed each half
  hour on the traverse board, "particularly useful in light and variable winds" (Falconer,
  *Traverse-board*); the log-board carries the hours, winds, courses and occurrences "from
  noon to noon; together with the latitude by observation", and is copied into the log-book
  daily at noon (Falconer, *Log-board*). The traverse table reduces the watch's courses and
  distances to one difference of latitude and one departure (Falconer, *Traverse*).
- **The compass.** Variation was known and allowed for: Falconer (1780, *Variation*) gives
  London as "now more than 20 degrees to the westward", and quotes Robertson that mariners
  "should every day, or as often as they had opportunity", observe an amplitude or azimuth
  to find it where they are. The chart's isogonic lines were Halley's of 1700 re-drawn by
  Mountaine and Dodson in 1744 and 1756 from some fifty thousand log-book observations, and
  reissued as late as 1794 (Raremaps listing of the 1794 chart). Deviation, the ship's own
  iron pulling the needle, was observed but not understood or corrected: Flinders's paper on
  the *Investigator*'s needle is dated 1805, his memorandum to the Admiralty 1810, and
  swinging ship and the Flinders bar follow from that (Wikipedia, *Flinders bar*; a 1920
  *Nature* notice, seen in summary only). A frigate's iron guns, shot and an iron water-tank all pulled the compass,
  and nobody aboard could say by how much; *Apollo*, 1804, is the case (below).
- **Leeway,** estimated by eye from the angle of the wake to the keel and allowed in points
  on the course; "very inconsiderable, except when the ship is close-hauled, and is
  accordingly disregarded whenever the wind is large" (Falconer, *Lee-way*; the theory in
  Steel 1794 vol. II). The game already computes leeway; the point here is that the
  navigator *estimated* it, and the estimate is a source of error.
- **The lead.** Two leads (Falconer, *Sounding*): the hand lead of 7 to 9 pounds on a
  20-fathom line, marked at 2, 3, 5, 7, 10, 13, 15 and 17 with leather and rags so that the
  marks can be told by feel at night, hove from the chains with the depth called in the
  leadsman's chant; and the deep-sea lead of 25 to 30 pounds, for which "it is usual
  previously to bring-to the ship", or, with way on, to pass the line forward and heave from
  the spritsail yardarm (Lever 1808, deep-sea lead). The lead is armed with tallow, which
  "brings up some of that substance which lies on the surface, such as Sand, Coral, Shells,
  Oaze, &c. and by these (from repeated trials being made and marked in the Charts), the
  bearings of certain Head-lands, Rocks, Buoys, Sands, &c. are generally known" (Lever). The
  depth and the ground are entered in the log "as well to determine the distance of the
  place from the shore, as to correct the observations of former pilots" (Falconer). This is
  the homeward-bounder's fix: the Western Approaches were called "the Channel Soundings"
  (the Regulations use the phrase as a place, in the article on a commander-in-chief's
  power to fill vacancies), and the song has it exactly, "we hove
  our ship to, for to strike soundings clear ... forty-five fathoms with a white sandy bottom".
- **Landfall by bearings.** The first land seen after a passage (Falconer, *Land-fall*),
  identified from the chart and the sailing directions, gives a bearing; two headlands give
  a fix, a transit of two marks gives an exact line. The Regulations' insistence on "the
  bearings and distance of some principal head-land" at every noon shows the habit.
- **The noon latitude.** "The most useful, as well as the most general, for taking
  observations at sea is the octant" (Falconer, *Quadrant*), Hadley's; by 1805 the sextant
  was common among naval officers, the octant remaining the cheap everyday instrument for
  latitude, the sextant the one you bought for lunars (Oxford History of Science Museum,
  *Octant*). The meridian altitude of the sun's lower limb, corrected for dip, refraction,
  semi-diameter and the day's declination from the Almanac, gives the latitude in a few
  lines of arithmetic; double altitudes when noon is clouded (Lieutenant, XVII).
- **The day's work at noon.** The reckoning is brought up from the log-board by the
  traverse table, the noon latitude replaces the reckoned latitude (Falconer, *Dead-reckoning*:
  the reckoning "is always to be corrected, as often as any good observation of the sun can
  be obtained"), the longitude is carried forward by account, and the master reports to the
  captain. Noon is when the ship's day changes and the log-book's page turns.

### The merchant schooner's master

Less was written down. Merchant officers had no formal examination before 1845 and relied
on "practical experience regarding seamanship and gained knowledge of navigation and
charting" (National Maritime Museum Cornwall, *Sailing Masters*). The instruments were the
same and fewer: compass, log, glass, lead and quadrant, and Falconer's every-two-hours log.
Coasting was by the lead and the land; on a passage the same dead reckoning and noon
latitude, and longitude by account unless the master could work a lunar. The famous
counter-example is Bowditch, who on a Salem merchantman resolved to "put down in the book
nothing I can't teach the crew" and taught the lunar to a crew of twelve including the
cook (USNI 2003, *The World According to Bowditch*; Penobscot Bay History); that it was
remarkable says what the norm was. At the other end of the merchant service the East India
Company's captains had chronometers on 80 per cent of voyages by 1792 (Davidson 2016, from
587 logs). A Baltimore schooner in the Channel trade in 1805 sits at the poor end of that
range; Chapelle (1930) says nothing about her navigation. *Unverified beyond the above:*
how many merchant masters of small vessels could work a lunar. The Almanac and an Epitome
were cheap (Slocum bought his Almanac for 2s 6d a century later; Norie's Epitome of 1805
was written for exactly this reader), so the question is skill, not kit.

## 2. Longitude in 1805

### Chronometers

- **The Royal Navy did not issue them.** "In the late eighteenth century, the Admiralty
  did not possess enough chronometers as they were not yet mass-produced, and it only
  provided a limited number of government-owned chronometers to expeditions of particular
  importance, most notably the voyages of exploration" (Mariner's Mirror 2013, the Greenwich
  chronometer service; read in summary, see Sources). In September 1821 the Board of
  Longitude's list ran to 131 government-owned timekeepers and the ships they were in (same
  article). General issue began in 1825, and even then one per ship "unless the Captain
  personally owned one", in which case a second was issued to make three, "reasoning that a
  ship with two was no better off than with one since a faulty instrument could not be
  identified" (Wikipedia, *Ship's chronometer from HMS Beagle*, citing the RMG). A search
  summary attributes to USNI (2019) the flat statement that chronometers were not issued to
  Nelson's fleet of 1805; I did not read the article, but it agrees with the rest. So in
  1805 a King's frigate had a chronometer if her captain had bought one. Bligh paid 40
  guineas for Earnshaw no. 1503 for *Providence* in 1791 (Wikipedia, *Thomas Earnshaw*);
  a boxed Earnshaw is quoted at "as little as £65" by the 1780s and "more than 5,000
  chronometers in existence" by 1815 (a popular horology site, *unverified* against Gould or
  Davies 1978, which I could not reach). A captain on £200 to £300 a year could own one and
  many did; a master on £90 mostly could not. *Not found:* any count of how many RN
  captains owned one in 1805. The honest statement for the game is "some frigates, at the
  captain's charge; no sloop or schooner unless the scenario says so".
- **The merchant service** ran ahead of the Navy where the voyages were long and the
  owners rich: Davidson's 587 East India logs show the chronometer used on 80 per cent of
  voyages by 1792, and in 1780 "52 percent of longitude entries were measured using the
  lunar method while the remainder relied on dead reckoning". Short-haul and coasting
  vessels had no reason to spend the money.
- **Rate and its error.** A chronometer is not set right, it is *rated*: its daily gain
  or loss is found ashore against a known meridian and written on a certificate, and the
  navigator applies rate times days since rating (Wikipedia, *Marine chronometer*). A good
  instrument held half a second a day; the trouble was the rate *changing*: Bligh logged K2
  in 1787 at "between 1.1 and three seconds" a day "and that it had varied irregularly"
  (Wikipedia, *Larcum Kendall*). Four seconds of time is a mile of longitude at the equator,
  two-thirds of a mile at 50 N. A rate wrong by two seconds a day is a minute of time in a
  month and half a degree of longitude in two months. Hence the lunar's second life: it was
  the check on the chronometer's rate at sea, which is how Mears used it in 1773 and how the
  Company's captains used it after (Davidson).

### Lunars

- **The method.** The moon moves against the stars about half a degree an hour, so the
  angle between the moon and the sun or a bright star near the ecliptic is a clock face
  readable from anywhere. Maskelyne's *Nautical Almanac* (from 1767) tabulates that distance
  for Greenwich time at three-hour intervals for the sun and a set of stars (UKHO history;
  de Grijs 2020 §5); the navigator measures the distance with a sextant, measures or
  computes the two bodies' altitudes, *clears* the distance of refraction and the moon's
  parallax, interpolates the Almanac for Greenwich time, compares with local time from an
  altitude, and the difference is longitude. Maskelyne's *Tables Requisite* (1766) carried
  the working; Lyons's and Witchell's short methods were adopted for the Almanac (de Grijs);
  Mendoza y Ríos (1797, 1805), Norie's *Complete Set of Nautical Tables* (1803) and *Epitome*
  (1805), and Bowditch (1802, "four methods") each made the clearing shorter (de Grijs §6
  and endnote 16; Wikipedia, *History of longitude*).
- **How long.** The masters who testified for Mayer's tables in 1765 said "they could make
  the observations in a few hours, not exceeding four hours" (Board of Longitude minutes,
  quoted in de Grijs); Wikipedia's *History of longitude* gives "up to four hours" before the
  Almanac; with the Almanac and the short methods the clearing came down to "about twenty
  minutes of work" (Reed, *Longitude by Lunars*). For 1805, with a competent master and
  Norie or Bowditch open on the table: a quarter of an hour on deck with the sextant for a
  set of distances, and half an hour to an hour of arithmetic below. *Unverified:* any
  1805 diary timing it; the twenty minutes is a modern practitioner's figure for the same
  arithmetic.
- **How accurate.** The Board's own witnesses said the result "always agreed with the
  making of land ... to one degree" (1765). Cook and Green, both expert, differed from each
  other "by upwards of one arcminute" on the same distance (Wales 1788, in de Grijs). An
  experienced observer in calm weather gets the distance to a quarter of a minute of arc;
  the two sources of error together "typically amount to about one-half arc-minute in Lunar
  distance, equivalent to one minute in Greenwich time ... one-quarter of a degree of
  longitude, or about 15 nautical miles at the equator" (Wikipedia, *Lunar distance*; de
  Grijs endnote 5). The Almanac's own lunar predictions were good to about half a minute of
  arc in the early 1700s and "roughly halved by 1810" (de Grijs endnote 8). Put together for
  1805: a good lunar is within a quarter of a degree of longitude, an ordinary one within
  half a degree, a poor one within a degree. At 50 N a degree of longitude is 38.6 miles, so
  those are 10, 19 and 39 miles. (The scoping draft's "thirty miles at 50 N" for half a
  degree is wrong; it is nineteen. Thirty miles is half a degree at the equator.) Note the
  asymmetry with latitude: an arcminute of altitude error is a mile of latitude; an
  arcminute of distance error is two minutes of time, thirty miles of longitude at the
  equator and nineteen at 50 N, because the moon is a slow clock hand.
- **What it needs.** The moon well clear of the horizon (parallax and refraction go bad
  low down) and a clear sky at the moment; a body at a tabulated distance, which in
  practice is the sun by day when the moon is between roughly first and last quarter, and a
  star by night; and the altitudes. Ideally three observers at once, one on the distance and
  one on each altitude, which is how a frigate did it (the master and two mates or
  midshipmen), or one observer with a watch to carry the time between his three
  measurements, taking each in turn; the altitudes can also be computed from the reckoned
  position and the time, which Bowditch shows. Near new moon there is no lunar for three or
  four days; near full a sun-lunar is impossible (the distance is off the tables' range) and
  one turns to a star, at night, with a worse horizon. *My own estimate from the geometry,
  not a source:* the sky allows a lunar of some kind on about twenty days in the lunation,
  and the Channel's weather in a bad month halves that. On a four-day passage from
  Finisterre it is quite possible to get none.
- **Who could do it.** Masters, whose Trinity House examination was in navigation, and the
  better lieutenants; midshipmen were taught it because the schoolmaster's whole business
  was the mathematics of navigation (Regulations, Schoolmaster II), and "lunar distances
  started to be used by ordinary navigators in the 1780s, and became common after 1790"
  (Wikipedia, *History of longitude*). The 1880s complaint that a captain "has not fallen in
  with a dozen men who had themselves taken Lunars" (Lecky, in de Grijs §7) is about the
  chronometer's victory, not 1805. *Unverified:* whether the Trinity House examination for
  masters set a lunar question in 1805.

## 3. The error model a game needs

Small and honest: every term below is something a 1805 master would have named, each has
a period source for its size, and the whole is a random walk with a few biases, which is
what dead reckoning is. The game keeps the *true* position from the physics and a
*reckoned* position with an uncertainty; nothing here touches the physics.

| Term | Character | Size, with the source | What collapses it |
|---|---|---|---|
| Log-line | random each heave, plus a bias | speed read to a quarter knot; the line marked short so the ship overruns the reckoning by 3 to 8 per cent (Luce); the glass slow in damp; "one in ten" home in a following sea (Luce); the hour's run inferred from one heave | nothing at sea; a fix |
| Compass, variation | a bias that moves slowly | the chart's variation a decade or more old and moving a quarter of a degree a year; an azimuth observation gets it to a degree | an azimuth or amplitude on a clear day |
| Compass, deviation | a bias by heading, unknown to the navigator | not corrected at all in 1805; a few degrees in a wooden ship with iron guns, more with iron stowed near the binnacle (the *Apollo* tank) | nothing; the player cannot even ask for it, only suffer it |
| Steering | random, small | half a point in a seaway, a quarter in smooth water; the traverse board's half-hourly peg averages it | a fix |
| Leeway | a bias when close-hauled | the estimate a half point out either way; nil off the wind (Falconer) | a fix |
| Current and tidal set | a bias the navigator does not know | Rennell's current a mile an hour to the northward for days in south-westerly gales, 46 miles in two days in one log; Channel streams one to three knots turning with the tide, allowed for only if the master knows the establishment and his own longitude | a sounding, a landfall, a noon latitude (for the north-south part) |
| Noon latitude | random, once a day, if the sun shows | sextant to a minute, octant to two or three; the horizon in haze or swell two to five minutes; call it 2 to 5 miles with a good horizon, none in cloud | itself: it collapses the north-south axis |
| Chronometer | a bias growing linearly | rate wrong by 1 to 3 seconds a day (Bligh's K2), so one to three and a half miles of longitude a week at 50 N and twenty to sixty over a four-month cruise, plus a one-time offset from the rating; a stopped chronometer (not wound) is a dead one | a lunar; a known meridian in port |
| Lunar | random per sight, plus the Almanac's small bias | a quarter to one degree of longitude by skill and sea (10 to 39 miles at 50 N); averaging a set of distances narrows it | itself: it collapses the east-west axis, by that much |
| Sounding | a line, not a point | depth to a fathom, the ground from the arming; matched against the chart's soundings it gives a band a few miles wide along the depth contour, and the ground picks between candidates | itself |
| Bearing of a landmark | a line of position | a degree or two by compass, which at ten miles is a quarter mile; two bearings a fix; a transit exact | itself |

A note on the sizes: a modern statistical study of 1885 logs finds dead-reckoning
uncertainty of about 0.15 to 0.18 degrees per two-hourly step and celestial fixes uncertain
by 0.22 degrees in latitude and 0.30 in longitude (Chan et al. 2021, arXiv 1910.04843).
Those are posterior figures over many ships and include every kind of sloppiness, late in
the century; the game's per-observation errors should be smaller and the compounding should
produce those totals. The M5 spec should tune against them, not adopt them.

**How they compound.** The reckoning advances each hour by the logged run along the
compass course corrected for variation and leeway. The random terms grow the uncertainty
as the square root of the number of steps; the biases (deviation, current, the short line)
grow it in a straight line, and they are the ones that kill. After a day's run of 150 miles
the random part is perhaps 5 to 10 miles; an unknown current of a knot for that day is 24
miles in one direction. At each clear noon the north-south uncertainty falls to the
latitude's few miles and the east-west one is untouched, so the uncertainty becomes a flat
ellipse lying east and west, and that is the shape of the captain's worry. Coming up from
Finisterre in thick weather with no sight for four days, the ellipse is 30 to 50 miles
long. "We should be seeing the Lizard by now" is the ellipse's eastern end passing the
Lizard's longitude while the ship is still at its western end. *Apollo* is what happens
when the ellipse is drawn too small: five days from Cork with no sights, a compass pulled
by a new iron tank, Captain Dixon believing himself forty miles off the coast, and
twenty-nine sail of a convoy of sixty-seven ashore south of Cape Mondego (Wikipedia, *HMS
Apollo (1799)*, citing the Naval Chronicle). Rennell's answer for the Channel was procedure:
get the latitude, then "expect soundings around lat. 49° 30' N", and run in on the
soundings.

**How a landfall or a sounding collapses it.** A sounding is a line: the reckoning is moved
onto the nearest point of the chart's depth contour consistent with the ground, and the
uncertainty across the contour shrinks to a few miles while along it stays as it was. A
single bearing is a line at an angle; it cuts the ellipse to a strip. Two bearings or a
bearing and a sounding cross, and the uncertainty is a point again. The engine needs one
representation for this: the reckoned position with a two-by-two covariance, grown each
hour by the terms above and updated by each observation as a linear line-or-point
measurement. That is a Kalman filter in its simplest form, twenty lines of arithmetic,
deterministic under the seed, and it is what a covariance ellipse on a modern chart
plotter draws. The player never sees a matrix. The master says "I would not trust the
reckoning within twenty miles east or west, nor five north or south", and the viewer's
chart draws the ellipse, faintly, around the reckoned position and never the truth.

The one rule that keeps this honest is that the *player's* errors come from the model and
the *world's* truth from the physics: the log-line's misreading is drawn from the seed, the
current that sets her is the tide model's real stream, and the difference between them is
what the player discovers.

## 4. Three options, and what each costs and gives

In all three the two positions are kept apart from the first line of 5b, the readings
registry (spec M4 §2) carries every number a captain can ask for, and the orders are lines
in the same grammar the model reads, so parity is structural: a language-model captain at
the table has the master's noon report and nothing the human has not got.

### (a) The floor: reckoning, lead, bearings, noon latitude

- **Orders.** `heave the log` (also automatic every hour, every two in the schooner,
  logged in the roll-up); `heave the lead`, `heave the deep-sea lead` (the latter brings her
  to, or runs the line forward at a cost in hands and time); `take a bearing of <the
  Lizard>` (refused in words if it is not in sight); `work up the reckoning` (the day's
  work on demand; automatic at noon); `observe the sun` (automatic at noon if the sky
  allows; refused in cloud); `set the reckoning to <lat> <long>` (the captain overrides the
  master, as he could). Later, `shape a course for <place>` reads the reckoning, not the
  truth.
- **Readings.** `the reckoning` (reckoned latitude and longitude, in words: "49° 52' N, 6°
  10' W by account"); `the reckoning's uncertainty` in the master's words; `the depth`,
  `the ground` (from the last cast, with its age); `the bearing of <landmark>` when in
  sight; `the distance run since noon`; `the course made good`; `the latitude by
  observation` (today's, if any). The registry's *absent* pattern says why a reading is not
  to be had ("No sight today; the sun was hid at noon").
- **Log lines.** "Hove the log: six knots and a half." "By the mark seven; fine grey sand
  with black specks." "The Lizard bore N by E, twelve miles by estimation." "Noon. Latitude
  by observation 49° 48' N; the reckoning was 49° 56'. Course made good since yesterday
  ENE, 131 miles. Longitude by account 5° 40' W." At compression the roll-up keeps the noon
  line and the casts.
- **Cost.** The reckoning state and its covariance; the error terms as seeded draws; the
  traverse arithmetic; the noon sight from the sun model already in `core/sun.py`
  (declination and hour angle are there); landmark visibility from the coast data and the
  sky; a depth and ground lookup from 5b's raster. Something like 600 to 900 lines with
  tests, on top of the chart data which 5b builds regardless; two new verbs' worth of
  grammar. Nothing here is astronomy beyond what M4 has.
- **For the model captain.** The lines above are the whole of it, and they are the same
  lines a human reads. The model's task becomes genuinely the master's: hold the two
  numbers apart in its own journal, ask for the lead when the reckoning says the shelf is
  near, and doubt. The watcher's lesson from playtest 7 (wait for the trend) becomes "do
  not stand on through the night on the reckoning alone".

### (b) The floor plus a chronometer as a scenario item

- **Scenario.** `chronometer: {maker: Earnshaw, rated: 1805-05-20, rate_s_per_day: +1.8,
  drift: seeded}`; absent in the schooner's scenario unless the owner's story puts one
  aboard. The captain's own possession, which the papers study already frames.
- **Orders.** `wind the chronometer` (daily, at the same hour, or the log says the master
  did it; forgetting is a scenario event, not a routine one); `take a sight for the
  longitude` (a morning or afternoon sun altitude, needing a latitude and the chronometer,
  refused in cloud or with the sun too low); `compare the watches`.
- **Readings.** `the chronometer` (its time, and days since rated); `the longitude by
  chronometer` (today's, with the master's stated trust, which widens with the days since
  rating). The reckoning's covariance is updated by it as by a lunar, the error being the
  rate error times the days plus the sight's own two or three miles.
- **Log lines.** "Forenoon. Sun's altitude for the time; longitude by chronometer 6° 04' W,
  the chronometer 41 days from Plymouth." "Wound the chronometer."
- **Cost.** Over (a), the time sight is one formula (local hour angle from altitude,
  latitude and declination), the chronometer a small state with a rate and a seeded drift,
  and the order and the two readings: 200 to 300 lines with tests. Cheap because (a) built
  the covariance and the sun.
- **For the model captain.** A longitude line most clear mornings, with its trust stated,
  so the model has an east-west number to argue with the reckoning, and a growing reason to
  distrust it as the weeks pass. Without (c) it has no way to check it, which is the true
  1805 position of a captain with one chronometer and no lunarian aboard.

### (c) The floor, the chronometer, and `take a lunar`

- **The order.** `take a lunar` (or `take a lunar of the sun`, `of Aldebaran`). The world
  checks the conditions: is the moon up and more than, say, fifteen degrees high; is there a
  body at a distance the tables cover (the sun between roughly 40 and 120 degrees from the
  moon by day, a bright star by night); is the sky clear enough; is the horizon usable (a
  night lunar needs star altitudes, which need a horizon, so a moonlit or twilight sky).
  If not, the order is refused in the registry's words: "No lunar to be had: the moon is
  two days old." If so, the master and two mates are on the quarterdeck for a quarter of an
  hour (a crew cost, the master unavailable for the reckoning meanwhile), and an hour of
  ship's time later the log gets the result. The result is *drawn, not computed*: the true
  longitude plus an error drawn from the seed with a spread set by the master's skill, the
  sea state (the ship's motion from 5a) and the distance's rate of change, a quarter of a
  degree for a good master on a quiet day, a degree for a poor one in a seaway. The engine
  never clears a distance. This is the whole trick: the Almanac's arithmetic is the
  master's, and the game models its *outcome*, as it models a topsail's setting without
  modelling each hand's grip.
- **What it needs that (b) has not got.** The moon's position and age to about a degree,
  which is a low-precision lunar ephemeris of sixty to a hundred lines (Meeus's short
  method or the Astronomical Almanac's), and the sky and the ship's motion from 5a. The
  tide model of `Tides1805.md` needs the same moon for springs and neaps, so the moon is
  paid for once and used twice; the night sky (moonlight for the lookout, the deck view
  at night) is a third use.
- **Readings.** `the longitude by lunar` (the last one, with its date and the master's
  trust); `the moon` (its age, whether it is up, whether it is "in distance"); and, the one
  that closes the loop, `the chronometer's error by lunar`: the difference between the lunar
  longitude and the chronometer's, which is how a rate was checked at sea and the reason a
  captain with a chronometer still wanted a lunarian.
- **Log lines.** "Afternoon watch. The master, Mr. Ellis, and two of the young gentlemen
  took a set of distances of the sun and moon. Longitude by lunar 6° 20' W, which Mr. Ellis
  would trust within twenty miles; the chronometer gives 5° 58' W, and he thinks it gaining
  on its rate." And the scene the order exists for: "No lunar: overcast." three days running,
  while the ellipse grows.
- **Cost.** Over (b): the moon, the conditions, the order, the drawn result with the skill
  term, three readings and the tests: 300 to 450 lines. The master's skill as a number is
  something the crew model of 5c wants anyway for named people.
- **For the model captain.** The same lines, and a real decision: is it worth heaving to
  the master's attention (and, for a night lunar, the watch's) for a longitude within twenty
  miles, against standing on by account? Whether to believe the lunar or the chronometer
  when they disagree by twenty miles is exactly the judgment the period's captains made, and
  a model at the table can make it from the two lines and the days since rating. Parity is
  intact because the model does no arithmetic the human does not: both read a result.

## 5. Recommendation

Build (a) in 5b with the covariance from the first line, (b) in 5b as the scenario item
already recommended, and (c) in 5b as well, as the order `take a lunar` with drawn results,
unless the moon model proves dearer than a hundred lines, in which case it opens 5c. The
lead's "lunars never" was wrong, for four reasons.

1. **They are cheap once (b) exists.** The dear part of longitude in the game is the
   covariance, the sun and the sight machinery, and (a) and (b) pay for those. A lunar adds
   a moon that the tide needs regardless, a conditions check, and a seeded draw. It is not
   a morning's arithmetic for the engine; it is a morning's arithmetic for the *master*, and
   the game models that as time and a person occupied, which is the inward minimum
   `InwardAndOutward.md` already asks 5c for.
2. **They are the period's method, not a curiosity.** In 1805 the Navy issued no
   chronometers; a frigate had one if her captain had paid forty guineas, and a merchant
   schooner in the Channel had none. Lunars were "common after 1790" and were what the
   Almanac, Norie's Epitome and Bowditch were *for*. A game that offers a chronometer and no
   lunar gives the 1805 navigator the 1830 kit and takes away his own. The schooner scenario
   in particular has no honest longitude at all without them.
3. **They make the chronometer honest.** A chronometer with no check is a number the
   player must trust blindly, and the game has no way to make its drift matter except by
   wrecking him. With lunars the drift is a discoverable fact ("the chronometer is gaining on
   its rate"), and the pairing of a fallible clock with a coarse but unbiased check is the
   best small piece of real navigation the period offers.
4. **They are a good scene, and they cost the player something.** The conditions refuse
   more often than they allow; when they allow, the master and two mates are taken off other
   work for a quarter of an hour and the answer comes an hour later, twenty miles wide.
   That is the correct shape for a "cool obscure" feature: rare, earned, and consequential,
   with a line in the log a reader will remember.

The bounds that keep it small: no real lunar arithmetic in the engine, ever; a moon good to
a degree and no better; results drawn from the seed with the master's skill, the sea and
the moon's rate as the only inputs; the refusal sentences in the registry's absent pattern;
the same order and the same lines for both ships and both kinds of captain. If the M5
budget bites, the order to cut first is the *star* lunar (night, worse horizon, more
conditions), keeping the sun lunar, which covers most of the lunation's useful days.

Two small things for the scoping draft while it is open: the brief for this study put half
a degree of longitude at 50 N at thirty miles, and the figure will otherwise find its way
into the spec; it is nineteen. And the draft's "a chronometer in 1805 is a captain's own
possession" should add "and rare in small vessels", since the schooner's scenario will
otherwise be given one by default.

## Sources

Verified in the repository's texts (cite by work and article, `docs/references/README.md`):

- Admiralty, *Regulations and Instructions*, 1806 (1808 printing): Lieutenant art. XVII;
  Master arts. XXV, XXVI, XXVII, XXVIII, XXXI, XXXII; Schoolmaster arts. I, II; "the Channel
  Soundings" as a place, in the article on a commander-in-chief filling vacancies.
- Falconer, *Universal Dictionary of the Marine*, 1780: *Dead-reckoning*, *Land-fall*,
  *Lee-way*, *Log*, *Log-board*, *Quadrant*, *Sounding*, *Traverse* and *Traverse-board*,
  *Variation*.
- Lever, *Young Sea Officer's Sheet Anchor*, 1808 (1827 printing): the deep-sea lead and
  arming (with figs. 505 and 506).
- Luce, *Seamanship*, 1866: "Log-line, Time-glasses" (the short line, the damp glass, one in
  ten in a following sea). Later than the period; consistent with Falconer.
- Steel, *Rigging and Seamanship*, 1794, vol. II: the theory of lee-way.

Read on the web, with what was read:

- R. de Grijs, "A (not so) brief history of lunar distances", *J. Astron. Hist. Heritage*
  2020, arXiv:2007.14504. Full text read (extracted from the PDF). The 1765 witnesses ("a
  few hours, not exceeding four hours", "to one degree"), Lyons and Witchell, Norie 1803 and
  1805, Bowditch's four methods, Cook and Green's arcminute, endnotes 5 and 8 on accuracy,
  Lecky's "dozen men", the Almanac's lunars to 1907.
- Wikipedia, *Lunar distance (navigation)*; *History of longitude* ("up to four hours",
  "common after 1790", Mendoza y Ríos 1805); *Marine chronometer* (rating, half a second a
  day, four seconds a mile, general RN supply by 1825); *Ship's chronometer from HMS Beagle*
  (general issue from 1825, the one-plus-two policy, citing RMG); *Larcum Kendall* (Bligh on
  K2); *Thomas Earnshaw* (Bligh's 40 guineas for no. 1503); *HMS Apollo (1799)* (the wreck,
  the iron tank, Dixon's forty miles, 29 of 67 ashore); *Flinders bar* (the 1805 paper);
  *Magnetic deviation* (Churchman's swinging proposal of 1794).
- S. C. Davidson, "The Use of Chronometers to Determine Longitude on East India Company
  Voyages", *Mariner's Mirror* 102:3, 2016. Abstract only (the text is paywalled): 587 logs
  1770 to 1792, 80 per cent by the end, 52 per cent of longitudes by lunar in 1780, Mears
  1773.
- "A Place for Managing Government Chronometers", *Mariner's Mirror* 99:1, 2013. Paywalled;
  read in search summary only: the late-eighteenth-century policy and the 1821 list of 131.
  *Treat the 131 as unverified until someone reads the article.*
- J. Rennell, "Observations on a current that often prevails to the westward of Scilly",
  *Phil. Trans.* 1793, and "Some farther observations", 1815 (OCR at jimclifford.ca, read
  in summary): a mile an hour, 46 miles in two days, the *Hope* 48 miles north of her
  reckoning, "expect soundings around lat. 49° 30' N".
- USNI, *Naval History* Oct. 2019, "John Harrison and the Longitude Problem": chronometers
  not issued to Nelson's fleet of 1805 (seen in a search summary, not read). USNI, *Naval
  History* Apr. 2003, "The World According to Bowditch": the crew of twelve (same).
- National Maritime Museum Cornwall, "Sailing Masters in the Age of Sail" (2025): the
  Trinity House examination; merchant qualification not formalised before 1845.
- Oxford History of Science Museum, *Octant*: the octant cheap and everyday for latitude,
  the sextant for lunars.
- F. Reed, *Longitude by Lunars* (reednavigation.com): "about twenty minutes of work".
- W. Brunner, "Longitude by the Method of Lunar Distance" (Starpath): one arcminute of
  distance error is thirty miles; averaging a set.
- D. Chan et al., "Late 19th-century navigational uncertainties", *Ann. Appl. Stat.* 2021
  (arXiv:1910.04843): the 1885 figures.
- The Raremaps listing of the 1794 Mountaine and Dodson variation chart (Halley's lines
  re-drawn 1744 and 1756 from Navy and Company logs).

Not verified, and marked so in the text: the count of RN captains with chronometers in
1805 (none found); "over 5,000 chronometers by 1815" and "£65 for a boxed Earnshaw" (a
popular horology site; Gould and Davies 1978 not reached); Nelson's Emery pocket
chronometer (same); the Channel's variation in 1805 (Falconer's "more than 20 degrees" at
London in 1780 and 21° 09' W at Greenwich in 1773 are the anchors; the value for the
Lizard in 1805 should be computed from the gufm1 field model when the chart is built, and
will be about two points west); the size of a wooden frigate's deviation; whether the
Trinity House master's examination set lunars; the days per lunation a lunar is possible
(my estimate from the geometry); the time an 1805 master took to clear a distance.
Paywalled or unreachable: the two Mariner's Mirror articles' texts, the Journal of
Navigation on Flinders, USNI 1954 on navigation 175 years ago, the UKHO Almanac history
page (503 at the time).
