# Design study: weather that comes from somewhere

From the owner's ruling 6 of 2026-09-29 on the M5 scoping draft (`TechnicalSpec-M5.md` §4):
pressure systems rather than a table of weather types, "with something more in depth
explored first". A design study for the 5a specification; not itself a specification.
Written 2026-09-29 from web research and the repository's own sources; every number that
could not be checked against a source it names is marked *(unverified)*.

Reads with: `ThreeDimensions.md` (the sea state as a field fed by the wind's history);
`InwardAndOutward.md` (weather arrives through the glass, the sky and the lookout, never
from nowhere); `freesail/physics/wind.py` and `freesail/world/weather_script.py` (the wind
the game has); `docs/dev/TuningNotes.md` M4c ("Gusts in a gale"); spec M4 §19.

## 1. The sea and its weather, as it is and as it was

The area is the western Channel and the Western Approaches, Falmouth to Ushant and Brest,
about a hundred miles square at 48 to 51 N, 3 to 8 W (ruling 1). It lies under the
North Atlantic storm track all year, closer to its southern edge in summer and under it
in winter.

### 1.1 The prevailing wind

Modern and historical data agree on the shape. The longest daily record there is comes
from the Channel itself: Mellado-Cano, Barriopedro, García-Herrera and Trigo (2020)
built four monthly indices of the proportion of days with the wind prevailing from each
quarter over the Channel (48 to 52 N, 10 W to 5 E) from Royal Navy logbooks 1685 to 1870
and ICOADS 1750 to 2014, published on PANGAEA under CC-BY-4.0 [S1]. I downloaded the
four files and averaged them by month (a westerly day is one with the prevailing wind
from 225 to 315 degrees true; the four quarters leave some ten per cent of days with no
prevailing quarter):

| Days in the month (%) | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Year |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1795 to 1815**, W | 27 | 37 | 22 | 24 | 26 | 23 | 38 | 43 | 33 | 35 | 34 | 35 | 31 |
| S | 25 | 24 | 19 | 23 | 29 | 16 | 27 | 23 | 23 | 26 | 19 | 19 | 23 |
| N | 17 | 18 | 16 | 25 | 21 | 14 | 15 | 16 | 16 | 17 | 15 | 24 | 18 |
| E | 24 | 18 | 27 | 24 | 22 | 10 | 10 | 10 | 18 | 18 | 17 | 22 | 18 |
| **1750 to 1854**, W | 29 | 34 | 31 | 30 | 28 | 33 | 44 | 41 | 35 | 34 | 35 | 32 | 34 |
| E | 22 | 17 | 23 | 23 | 23 | 15 | 11 | 13 | 19 | 19 | 16 | 20 | 18 |
| **1985 to 2014**, W | 34 | 29 | 33 | 27 | 28 | 37 | 48 | 46 | 33 | 30 | 34 | 35 | 35 |
| E | 17 | 18 | 19 | 19 | 23 | 12 | 11 | 9 | 20 | 19 | 13 | 20 | 17 |

So: westerlies on a third of days over the year and nearly half in high summer;
easterlies on a quarter of days in late winter and spring (the "Channel easterly" that
kept fleets in the Downs and let the French out of Brest) and a tenth in summer; the
south and north quarters steady near a quarter and a fifth. The period and the present
differ by less than the year-to-year scatter. 1805 itself was odd: the index gives June
1805 as 3% westerly and 43% easterly, December 1805 as 74% westerly. A scenario pinned
to a real month can take that month's values (§5).

Beaufort-force frequencies by month were not found in an open source I could read. The
Admiralty *Channel Pilot* (NP27) carries climatic tables for Scilly, Plymouth, Ushant and
Brest with percentage frequencies of wind by direction and force, of gales, fog and
calms by month [S2]; it is in copyright and was not readable here, and the game's
constants should be read from a printed copy before 5a is specified. The NGA *Atlas of
Pilot Charts, North Atlantic* (Pub. 106) is a United States government work with monthly
wind roses, percentage of gales and of fog by five-degree square [S3]; I could not fetch
the charts to read the numbers *(the values for the 45 to 50 N, 5 to 10 W square remain
to be read)*.

### 1.2 Gales by month

The one open monthly series found is Météo-France's climate sheet for Ouessant-Stiff
(the lighthouse station on Ushant, 1991 to 2020 normals) [S4]: days a month with a gust
of 16 m/s (31 knots) or more, January 23.6, February 19.9, March 18.6, April 15.0, May
11.6, June 7.0, July 6.3, August 6.0, September 9.0, October 16.0, November 21.3,
December 22.8, 177 a year; days with a gust of 28 m/s (54 knots) or more, January 4.5,
February 3.7, March 2.0, April 0.9, May 0.6, June 0.2, July 0.1, August 0.0, September
0.3, October 1.2, November 2.8, December 4.0, 20 a year. Taking a gust as about 1.25 of
the mean over water (§4), a 31-knot gust is a mean near force 6 and a 54-knot gust a mean
near force 9; so at Ushant a strong breeze or more blows on twenty-four days of January
and six of July, and a strong gale on four or five days of January and none of August.
Force 8 days fall between: *perhaps ten in January and one in July (an interpolation,
unverified)*. The station is on a cliff and reads high for the open sea.

Historically, Wheeler, García-Herrera, Wilkinson and Ward (2010) derived gale frequency
and quarter-wind indices for the Channel and its western approaches from Royal Navy
logbooks 1685 to 1750 and found a marked fall in gale frequency over that period [S5];
the paper's numbers were behind a login and are not quoted. Wheeler (2001) reconstructed
the weather of the European Atlantic seaboard for October 1805 from logbooks and shore
observatories: light and squally with rain on the morning of Trafalgar, a rising swell
during the action, a south-westerly gale by night that blew, on his reading, for the
best part of a week, "the meteorological event of the first half of the century" in
those waters [S6]. That is the period's own worst case, and a scenario's.

### 1.3 Depressions and their fronts

What passes over the area is the Atlantic depression with its warm and cold fronts, the
Norwegian model of Bjerknes (1919) and Bjerknes and Solberg (1922). The sequence a ship
south of the track sees, as the Met Office's teaching material gives it [S7]:

- **Ahead of the warm front**: the wind freshens and *backs* (toward the south); cirrus,
  then cirrostratus, altostratus, nimbostratus; rain sets in and grows steady; visibility
  falls in the rain; the glass falls at an increasing rate; temperature much the same.
- **At the warm front**: the wind *veers* (south to south-west); rain stops or turns to
  drizzle; the glass stops falling; it turns milder.
- **The warm sector**: wind steady in direction, south-west to west; stratus and
  stratocumulus; drizzle; visibility moderate or poor, fog possible; the glass steady, or
  falling if the low is deepening.
- **The cold front**: the wind backs a little and freshens close ahead of it, then
  *veers sharply*, often in a squall, west to north-west; heavy rain, perhaps hail and
  thunder; the glass jumps and rises; it turns colder.
- **Behind**: clearing skies with cumulus and showers, very good visibility between them,
  the wind gusty in the cold unstable air and often at its strongest here, the glass
  rising fast ("first rise after low foretells stronger blow").

North of the track the wind backs through east to north as the low passes and the glass
falls and rises without the veer; a ship there gets the long cold rain of the warm
front's northern side. Over the sea the surface wind blows across the isobars toward low
pressure at about 10 to 20 degrees and at about two thirds of the geostrophic speed
[S8]; at 50 N a gradient of 1 hPa per 100 km gives a geostrophic wind of 7.2 m/s (14
knots) and so a surface wind near 10 knots, a gale needing three to four hPa per 100 km.
Shipping-forecast usage classes a low's movement as slowly (under 15 knots), steadily
(15 to 25), rather quickly (25 to 35), rapidly (35 to 45) [S9]; central pressures of
Atlantic lows reaching the area run from 1000 hPa down to 950 and lower in a great storm.

### 1.4 Fog, visibility, sea breeze, calms

Sea fog in the western Channel is advection fog: warm moist south-westerly air over water
still cold from winter, so it is most frequent in late spring and early summer, and near
the coasts and the cold patches off Scilly and Ushant. Ship observations 1950 to 2007
put fog west of the United Kingdom at nearly 4% of observations in June to August and
under 2% in December to February [S10]. A source with monthly values for the Channel
itself was not reached *(the *Channel Pilot* tables have them)*. Fog goes with a slack
gradient and a stable warm sector or the western side of a high; a fresh wind lifts it to
low cloud; rain and drizzle bring "thick weather" of their own.

The sea breeze on the Cornish and Breton coasts is a summer, daylight, fine-weather wind
of some 10 knots at most, onshore, strongest in mid-afternoon, felt a few miles to sea
and dying at dusk; Simpson's studies of the south coast of England (1962 to 1973, and
*Sea Breeze and Local Winds*, 1994) are the standard reference [S11]. Calms come under
the centre of a high, in a col between systems and briefly at a low's centre; I found no
open monthly frequency of calms for the area *(the *Channel Pilot* table again)*. The
gate's day at 50 N off Falmouth sits in exactly this climate.

### 1.5 The historical data: CLIWOC and the reanalyses

**CLIWOC** (Climatological Database for the World's Oceans, 1750 to 1854) was an EU
project of 2001 to 2003 that abstracted the noon weather entry from British, Dutch,
French and Spanish naval logbooks [S12, S13]. Release 1.5 (April 2004) holds 280,195
observations from 1,674 logbooks and 4,942 voyages: Netherlands 126,300, England
88,473, Spain 54,082, France 10,632 [S13, Table I]. Each record is a date, a position,
the wind direction (magnetic in the English logs, converted to true in the database),
the wind force in the log-keeper's words and as a Beaufort equivalent from the
project's multilingual dictionary, the present weather in words, the sea state where
given, and, where the ship carried instruments, air temperature and barometer. The
dictionary's English equivalents: light airs 1 to 2, light breeze 2 to 3, moderate
breeze 4, fresh breeze 5, strong breeze 6, moderate gale 7, fresh gale 8, strong gale 9,
hard gale 10, storm 11 [S13]; the game's `units.describe_wind_strength` already uses the
same words at the same forces. Pressure and temperature are rare before 1800 and
number 48,779 each for 1800 to 1854 over all oceans [S13, Table IV]; ships that had a
barometer had a thermometer too. The North Atlantic has 134,143 of the observations,
with English coverage falling after 1800 (21,807 English observations after 1800 against
62,156 before) as the Dutch rise [S13, Table II].

Availability: the database is on PANGAEA as release 2.1 (Jones et al. 2007, 5,468
per-voyage datasets, tab-delimited, CC-BY-3.0) [S14]; on historicalclimatology.com as
a spreadsheet, a tab file and a GeoPackage [S15]; in IMMA format from KNMI; and the
observations were folded into ICOADS Release 3.0, which extends the marine record back
to 1662 [S16] *(the ICOADS deck number was not verified)*. The PANGAEA collection cannot
be fetched as one text file; it is a zip of the per-voyage files *(size unverified)*.

How it could calibrate the game for 1805 by month and area: select the records inside
the game's box (48 to 51 N, 3 to 8 W, or wider to 45 to 52 N, 0 to 12 W for numbers) for
1790 to 1820, and count by month the wind direction by eight points, the Beaufort force
by class, the weather words (rain, squally, hazy, fog, thick, clear), and the days with
gales; that gives the monthly tables §5's seeding needs, from the period's own logs. The
caveats are known: one observation a day at noon, direction to the nearest point,
force from words that differ by ship size, and a fleet's logs clustered off Brest and
in the Channel where the blockade kept them. The wind-direction indices of [S1] are the
same data already reduced by month, and are enough for direction alone.

**Reanalyses.** ERA5 (Copernicus, CC-BY-4.0, hourly from 1940) gives the modern
climatology of the box at 31 km, and its tracks of real lows are the natural source for
option (d)'s replayed sequences [S17]. NOAA's 20CRv3 (CC-BY-4.0 at NCAR) reconstructs
the global atmosphere eight times a day from surface pressure observations from 1836
publicly, with an experimental extension to 1806 [S18]; it cannot reach 1805 with any
skill over the Channel, since almost nothing instrumental was recorded at sea then, but
its early decades are a check on what a January or a June looks like day by day.

### 1.6 Beaufort's scale and notation, 1806

Beaufort wrote his scale into his journal in January 1806, commanding HMS *Woolwich*, as
thirteen forces from calm to storm in the words then in use, with no numbers of speed;
in its later form the forces were defined by the canvas a well-conditioned man-of-war
could carry, from "just sufficient to give steerage way" at force 1 to "that which no
canvas sails could withstand" at 12; FitzRoy used it in *Beagle* from 1831 and the
Admiralty made it the standard for logs in 1838 [S19]. His weather letters, also of this
period, are what the sky column of a log became: b blue sky, c detached clouds, d
drizzling rain, f fog, g dark gloomy, h hail, l lightning, m misty or hazy, o overcast,
p passing showers, q squally, r rain, s snow, t thunder, u ugly or threatening, v
unusual visibility, w wet or dew [S19]. *The 1806 wording force by force (the commonly
quoted "faint air just not calm", "gentle steady gale", "hard gale with heavy gusts") is
reproduced in Huler's* Defining the Wind *(2004) and the Met Office library factsheet;
neither was reachable, so it is not quoted here (unverified).* A log of 1805 does not
use the numbers; it says "Fresh breezes and cloudy", "Light airs and clear", "Strong
gales and squally with rain", "Moderate and hazy", the formulas CLIWOC's dictionary was
built to read, and *Victory*'s log for 21 October 1805 reads "Light winds and squally
with rain" [S6].

### 1.7 The barometer at sea in 1805

The marine barometer is Nairne's of about 1773: a stick barometer with the bore
constricted to stop the mercury pumping with the ship's motion, in a mahogany case hung
in brass gimbals; Cook carried one on his second voyage, and the National Maritime
Museum's example (Nairne & Blunt, after 1774, from the sale of Cook's widow's effects)
reads inches of mercury from 26.5 to 31 with a vernier to a hundredth [S20]. Mariners
used barometers in the eighteenth century and their use became general in the
nineteenth [S20]; officers of the Royal Navy carried them from about 1780 onward, as
their own possessions [S21]. In 1805 a glass aboard is the captain's or the master's, not
the Admiralty's, and a small vessel may have none; CLIWOC's counts (§1.5) say how few
logs recorded it. *When the Admiralty first supplied barometers to ships as stores was
not established (unverified; the 1840s under Beaufort as Hydrographer is my belief).*

What a captain read from it was the height and, above all, the tendency. The engraved
words on a common plate, Stormy 28, Much Rain 28.5, Rain 29, Change 29.5, Fair 30, Set
Fair 30.5, Very Dry 31 [S22], were already known to be worthless: FitzRoy's guide of
1859 says the words "should not be so much regarded for weather indications, as the
rising or falling of the mercury", that "the greatest depressions of the barometer are
with gales from the S.E., Southward, or S.W.; the greatest elevations, with winds from
the N.W., Northward, or N.E.", that "backing is a bad sign, with any wind", and gives the
rhymes "Long foretold, long last; short notice, soon past" and "First rise after low
foretells stronger blow" [S23]. Luce (1884, ch. "The Weather, the Barometer, Laws of
Storms"), quoting FitzRoy, adds the couplet every sailor knew, "When the wind shifts
against the sun, trust it not, for back it will run", the law that with east, south-east
and south winds the glass falls, with south-west it ceases to fall, with west, north-west
and north it rises, and that "in an ordinary gale, the wind often blows hardest when the
barometer is just beginning to rise, directly after having been very low"; the ordinary
range in high latitudes is 30.5 to 29 inches, the extremes 30.8 and under 28 [S24].
FitzRoy and Luce are fifty to eighty years after 1805, but they are writing down what
the trade already said; the pairing of a backing wind with a falling glass is the old
lore, and the rate rules ("a fall of a tenth in three hours means much wind") are
*common sailing-school teaching whose period source I could not find (unverified)*.
What was *not* known in 1805 is the shape of the thing: Dove's law of gyration (1828),
Redfield's rotary storms (1831), Reid's *Law of Storms* (1838), Buys Ballot's law (1857,
"back to the wind, low pressure on the left") [S25, S26] all lie ahead. A captain of
1805 knows the glass falls before a southerly gale and that the wind will veer through
west and the glass rise; he does not know there is a centre passing to the north of him.

## 2. Model options

Each option must give, at every reading and for every ship in the world: the true wind's
direction and speed with gusts and wander; the glass and its tendency; the sky; rain;
visibility; temperature perhaps. The game ticks once a second of ship's time at about a
thousand ticks a second for one frigate (truth 51), so the weather has a budget of a few
microseconds a tick, or the same work done once a minute of ship's time. Everything must
be deterministic given the seed and the scenario, and replay tick for tick.

### (a) A table of weather types with Markov transitions per month

A dozen states (fair W, fair E, fine calm, warm-sector SW drizzle, frontal rain, NW
squally clearing, fog, gale SW, gale NW, ...), each with a distribution of wind, sky and
glass, and a transition matrix per month, as Richardson's stochastic weather generator
does with wet and dry days [S27]. It gives everything but a reason: the glass has to be
scripted per state, so its tendency is a property of the state, not a cause of the next
one; "wait for the trend" cannot be learned because the trend does not exist between
the states. The wind is the same everywhere in the box, so two ships sixty miles apart
see one weather. Cost nil; data a matrix per month, which CLIWOC could fill; determinism
trivial. The right shape for a fair-weather idle and for nothing else, and the owner's
ruling has already passed it over.

### (b) Point pressure systems with fronts

A small number of centres (two to four in the box's neighbourhood at once): each a
position, a velocity, a central pressure anomaly (a low negative, a high positive), a
radius, and for a low a deepening-and-filling curve over its life; the pressure at a
point is a background (say 1015 hPa, seasonal) plus the sum of the anomalies with a
smooth radial profile (a Gaussian or a Rankine bell). The geostrophic wind is the
gradient of that sum turned ninety degrees, and the surface wind is that turned inward
about 15 degrees and scaled by about 0.7 (§1.3), capped in strong curvature. Fronts are
two lines hinged at the low's centre, a warm front ahead and a cold front behind, each a
bearing, a length and a width, rotating and trailing as the low moves and the cold front
catches the warm to occlude; crossing a front adds the veer, and the sector a ship is
in (ahead, warm, behind) fixes the sky, the rain, the visibility and the temperature by
the table of §1.3. The sea breeze is a term added within a few miles of a coast by day
under a weak gradient; fog is a state entered when the sector, the sea temperature and
the gradient allow it, and left when the wind rises. The glass at the ship is the
pressure sum in inches; the tendency is its change over the last three hours, kept by
the ship's own record.

Everything a reading needs has one cause. Cost: for each system, one exponential and a
few multiplies at each point asked, so a handful of microseconds a ship a tick; fronts
are two segment-distance tests a low. Data: the monthly climatology of §1 (how many
lows a month, their tracks, speeds and depths; how often a high sits over the area; the
easterly share); those can be set from the tables and tuned to the CLIWOC counts.
Determinism: the systems are drawn from a seeded stream separate from the wind's at
the scenario's start and each time one leaves the box, and thereafter everything is
arithmetic. The weakness is that real weather is not a sum of bells: the strongest
winds in a Channel gale are in the cold air behind the front and in the warm sector's
tight isobars, not symmetric about the centre; a profile per sector fixes most of it.

### (c) A coarse 2D pressure field advected and perturbed

A grid (say 32 by 32 cells over twice the box) holding pressure, advected by a steering
wind and perturbed by random forcing with the right spectrum; wind from the gradient as
in (b). It gives asymmetric, evolving systems for free and two ships their own weather,
but the fronts and the sky still have to be inferred from the field (temperature
advection, gradient sharpness), which is the hard part of (b) made harder; it needs
tuning nobody here has done; a 1,024-cell update a tick in Python is the whole weather
budget many times over unless it runs once a minute of ship's time; and determinism
across machines is fine but the field is opaque to a scenario author and a director,
who cannot say "a low to the north-west, deepening" and get it. More model than the
readings can use.

### (d) Replaying real sequences

Take real tracks from ERA5 (any day since 1940) or 20CRv3 (1836 on), or a CLIWOC
month's daily winds, and drive (b)'s systems along them with noise. Perfect texture, the
period's own weeks, the Trafalgar week for a scenario; but the data have to be shipped
with the game or reduced to tracks by a build step, ERA5 and 20CRv3 are the wrong years
and CLIWOC has one noon a day with no pressure, so it is a source of *tracks and
statistics* for (b), not a model on its own.

### Mixing

The natural combination: (b) as the engine; its systems seeded from a monthly
climatology (§5) drawn from the tables and checked against CLIWOC; a scenario able to
pin a system's track outright, which is (d) by hand and is what the M4c weather script
becomes; and (a) only as the fair-weather idle inside (b), where a high sits for days and
the daily cycle (sea breeze, morning fog, evening calm) is the whole weather.

## 3. How the state becomes words

The readings the registry already reserves are `the glass` (absent today, "that reading
comes with the world") and, for the sky, nothing yet; a captain, a rule and a model read
the same rows [`freesail/api/readings.py`]. What 5a adds:

- **`the glass`**: inches to the hundredth, as the vernier reads ("29.72"), and
  **`the tendency`**: the change over the last three hours and the last hour, in the
  period's words: steady, rising, falling, falling fast; "the glass has fallen a tenth
  since the forenoon watch" in the log. The number is the model's pressure at the ship
  converted (33.86 hPa an inch), with the ship's own reading noise (a marine glass
  pumps in a seaway; a hundredth or two). No hectopascals anywhere a player sees.
- **`the sky`**: Beaufort's letters as words: clear, detached clouds, overcast, dark and
  gloomy, threatening, hazy, thick; and the signs Luce lists for the log's colour: a high
  dawn, hard-edged clouds, the scud. Chosen from the sector and the distance to the
  front, with a little noise so two hours differ.
- **`the weather`**: rain, drizzle, passing showers, squally, thunder, fog. "Squally with
  rain" is a state with consequences: squalls are the gusts of unstable air (§4).
- **`the visibility`** in the lookout's terms: how far a sail can be seen (the horizon,
  a few miles, a mile, a cable), the number the sighting model of 5c consumes.
- **`the sea`** in the period's words (a smooth sea, a short chopping sea, a heavy sea, a
  long swell from the westward), from the sea-state field of `ThreeDimensions.md`; the
  Douglas scale is 1921 and its numbers are not spoken [S28].
- **`the temperature`** perhaps, since a change of air is a warm or a cold front and the
  thermometer went with the barometer; if not now, then when a fire or the sick list
  wants it.

The wind's readings stay as they are (`the true wind`, its veer and back in points);
the veer at a front and the back before it come out of the model and the existing log
lines say them.

What an experienced seaman infers, and so what the primer and the standing-order
grammar should let a captain express: a backing wind and a falling glass mean a gale from
the southward, reef early; a veer through west with the glass at its lowest and turning
means the worst is to come in a squall from the north-west and then the clearing; a slow
rise with drying air is fair weather; a rapid rise is unsettled; long foretold, long
last. The game keeps to the period's knowledge by giving no reading that names a front,
a centre, an isobar or a track; the director and the scenario author see them (world
orders name systems, §5), the captain never does. Buys Ballot's rule can be *discovered*
by a player from the readings, as it was; that is the seamanship the owner wants
"wait for the trend" to become.

## 4. The gust factor and the wander

**What the game does.** `Wind.step` starts a gust with probability gustiness × 0.002 a
second (at 0.3, one every 28 minutes), holds it 5 to 30 seconds, and multiplies the
speed by a factor drawn uniformly from 1.1 to 1.5 whatever the mean; so 45 knots gusts to
67 (the M4c note). The direction walks without bound at 0.0002 × variability rad/√s, and
the speed wanders about the base as a mean-reverting walk with a 33-minute time
constant and a stationary spread of about 0.32 × variability of the base (10% at 0.3,
the four knots at 45 the tuning notes measured).

**What the sea does.** The gust factor (peak few-second gust over the 8- to 10-minute
mean at buoy height) over water is about 1.2 to 1.25 and nearly flat with wind speed:
Kramer's climatology for the Carolina coast gives marine and shoreline sites 1.22, 1.21,
1.22 and 1.23 for means of 10 to 15, 15 to 20, 20 to 25 and over 25 knots (land sites
1.57 falling to 1.37) [S29]; Blaes and others found 1.23 with a standard deviation of
0.055 at buoys in ten tropical cyclones, 61% of factors between 1.2 and 1.3, with a
slight rise as the wind rose, where land factors fell [S30]; a North Carolina buoy and
tower study gives 1.25 near neutral stability [S31]. The WMO guideline for converting
averaging periods (Harper, Kepert and Ginger 2010) recommends 1.23 for the 3-second
gust over the 10-minute mean at sea *(quoted from secondary sources; the table itself
was not reached, unverified)* [S32]. Stability matters more than speed: gust factors
rise as the air becomes less stable, with cold air over a warmer sea, which is the
north-westerly behind a cold front with its showers and squalls; in the stable warm
sector they fall toward 1.1. Over land or in convective squalls a factor of 1.5 and more
is ordinary; over the open sea it is a squall, not a gust.

**So:** the M4c note is right that 1.5 is high, and the answer is not to ease the factor
with the mean wind, which the sea does not do, but to draw it about the air mass: a
warm sector 1.10 to 1.20, neutral air 1.15 to 1.30, unstable air behind a front 1.20 to
1.45 with the top of the range reserved for squalls, which are their own events lasting
minutes, veering the wind a point or two and bringing rain, logged as "a squall" and
shortening sail for it as the period did. The 45-knot gale of the gate's day then gusts
to 55 or so, and to 65 only in a squall, which the log names. The gust *mechanism*
(start, hold, release) can stay.

**The wander** wants one change once the base has a cause: the direction's random walk
grows without bound (0.7 degrees an hour standard deviation at variability 1, not the
"about 1 point per hour" its comment claims; a point would take days) and would carry
the wind off the systems' wind over a passage. Make it mean-reverting like the speed's,
with a spread of some 5 to 10 degrees in unstable air and less in stable, and the same
for a gust's direction. The synoptic turn (the veer at a front, the slow back ahead of a
low) comes from the systems and is far larger than the wander. Speed wander at 10% of
the mean is about right for ten-minute means about an hourly one over the sea
*(order of magnitude from the gust studies' scatter, unverified as a number)*.

## 5. Recommendation

**Option (b), point systems with fronts, seeded from a monthly climatology, with the
weather script kept as a pinned track.** Reasons: it is the only option where every
reading has one cause and the glass leads the wind, which is what makes "wait for the
trend" seamanship (ruling 6); it costs microseconds a ship a tick, so a dozen far-detail
ships have their own weather (5c); it is deterministic by construction; a scenario
author and a director can say "a low, 985, passing north of Scilly at 25 knots, cold
front through Falmouth at the change of the middle watch" and have it happen, which (c)
cannot give and (a) cannot mean; and the data it needs are exactly the tables §1 names.

**Seeding from a monthly climatology.** A table per month: the rate of lows crossing the
region (from the gale and westerly frequencies: perhaps six to eight a month in winter
and three to four in summer *(to be set from the tables, unverified)*), the distribution
of their tracks (bearing and distance of closest approach: most pass north of the box,
toward the Irish Sea and Scotland, a few through it or south of it), speeds (15 to 35
knots), central pressures (winter deeper), and the probability that a high sits over the
area with a given orientation (the spring easterly, the summer Azores ridge, the winter
Scandinavian high that brings the easterly gale). Draw the next system's parameters from
those when a system leaves the box or its life ends, from a seeded stream of the world's
own; keep the glass's background at the monthly mean. Calibrate by running a thousand
simulated months and comparing the direction shares to the 1750 to 1854 row of §1.1,
the gale days to Ushant's counts, and the fog and rain to the tables; the CLIWOC
extraction of §1.5 is the second pass, if the tables alone do not settle it. For a
scenario on a real month, the indices of [S1] for that month (June 1805: easterly) can
replace the climatological direction shares.

**The M4c script becomes a scenario's pinned track.** The scenario file's `weather`
grows a `systems` list: each system a name, a kind (low, high), waypoints of position,
central pressure and time, a radius and, for a low, its fronts' initial bearings; the
model follows those waypoints exactly as `WeatherScript.at` interpolates today, and
draws nothing while a scripted system is present. The gate's day (W 17 all day, veering
WNW and NW to 45 knots in the middle watch, easing by dawn) is a low passing well north
of Falmouth with the ship already in its warm sector, the cold front through at 22:00,
the north-westerly gale in the cold air behind and the ridge building by morning; the
glass falls slowly through the day, checks at the front and rises fast in the gale,
which is the day the watcher's finding 5 asked for, said by the instruments. The old
wind waypoints stay as a second form, `wind`, that pins the base wind directly for tests
and truths (steady wind, gustiness 0, as every truth is measured); when both are given
the pinned wind wins and the systems supply only the sky and the glass. The director's
world order of proposal §7.6 appends a system or a waypoint, journaled at its tick, as
spec M4 §19 already provides for wind waypoints.

**What is built in 5a.** The systems and fronts, the surface-wind rule, the sector
table for sky, rain, visibility and temperature, the glass and its tendency as readings
in inches, the sky and weather and visibility readings and their log lines, the gust
factor by air mass and squalls as events, the mean-reverting wander, the monthly seeding
table with first-pass values from §1 and the `Channel Pilot` tables read from a printed
copy, the scenario file's `systems`, the gate's day re-expressed as one, and the
climatology check as a test (a thousand months' direction shares within a few points of
§1.1). The sea state and the reduced motions of `ThreeDimensions.md` are 5a's other half
and read the wind's history from this model.

**What waits.** The sea breeze and coastal fog need a coast, so they come with 5b's
chart (the model's hook, a distance-to-coast, is left in). The CLIWOC extraction is a
build-time study, done when the first-pass table proves wrong, not before. Replayed real
tracks (d) wait for a scenario that wants a real week (the Trafalgar storm is the
candidate). Temperature as a reading waits for something that reads it. The 1806 Beaufort
wording, the Admiralty's issue of barometers, the *Channel Pilot* numbers, the pilot-chart
percentages and the WMO gust table are the five things to verify before the
specification quotes them.

## What was and was not verified

Verified against a source I read: the Channel direction indices and their licence (the
files were downloaded and averaged here) [S1]; the Ouessant gust-day counts [S4]; the
CLIWOC counts, fields, dictionary and pressure numbers from the KNMI description paper
[S13] and the PANGAEA release page [S14]; the front sequence [S7]; the marine gust
factors [S29, S30, S31]; FitzRoy's rules [S23] and Luce's chapter [S24, in the
repository]; Beaufort's letters and adoption dates [S19]; the barometer's history and
Cook's instrument [S20, S21]; the dates of Dove, Redfield, Reid and Buys Ballot [S25,
S26]; ERA5 and 20CRv3 coverage and licences [S17, S18]; Wheeler's papers' existence and
scope [S5, S6]. Not verified, and marked so above: Beaufort's 1806 wording; the
Admiralty's first issue of barometers; the WMO 1.23 table; force-8 days by month; monthly
fog and calm percentages for the Channel; the rate-of-fall rules' period source; the
number of lows a month; the CLIWOC ICOADS deck and zip size. The Springer papers, the
*Channel Pilot*, Simpson's book and the Met Office factsheet were behind logins, sales or
dead links.

## Sources

- [S1] Mellado-Cano, J., Barriopedro, D., García-Herrera, R., Trigo, R. M. (2019),
  *Monthly wind directional indices based on ships logbooks observations*, WI, SI, NI,
  EI, PANGAEA, CC-BY-4.0, https://doi.org/10.1594/PANGAEA.906066 (and 906065, 906064,
  906063); in supplement to Climate Dynamics 54, 823–841 (2020).
- [S2] Admiralty Sailing Directions, *Channel Pilot* NP27, 14th ed. 2023 (UKHO; not read).
- [S3] NGA, *Atlas of Pilot Charts, North Atlantic Ocean*, Pub. 106 (monthly charts; not
  read).
- [S4] Météo-France, fiche climatologique Ouessant-Stiff (29155005), normals 1991–2020,
  https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/REF_STATION/FICHECLIM_29155005.pdf
  (gust-day counts as reported by the search index; the sheet fetched here showed the
  precipitation table).
- [S5] Wheeler, D., García-Herrera, R., Wilkinson, C. W., Ward, C. (2010), "Atmospheric
  circulation and storminess derived from Royal Navy logbooks: 1685 to 1750", Climatic
  Change 101, 257–280; abstract at https://docta.ucm.es/handle/20.500.14352/43025.
- [S6] Wheeler, D. A. (2001), "The weather of the European Atlantic seaboard during
  October 1805: an exercise in historical climatology", Climatic Change 48, 361–385;
  summarised with *Victory*'s log at
  https://collingwoodsociety.co.uk/21st-october-1805-0800-hours-and-now-the-shipping-forecast/.
- [S7] Royal Meteorological Society / Met Office teaching resource, "Anticyclones,
  depressions, fronts", https://www.metlink.org/wp-content/uploads/2014/03/anticyclones_depressions_fronts.pdf;
  Bjerknes, J. (1919), "On the structure of moving cyclones", Geofysiske Publikationer
  1(2); Bjerknes and Solberg (1922), "Life cycle of cyclones and the polar front theory of
  atmospheric circulation", Geofys. Publ. 3(1).
- [S8] Surface wind over the ocean at 10 to 20 degrees to the isobars and about two
  thirds of geostrophic: standard textbook statement, as at
  https://theweatherprediction.com/habyhints3/742 and Britannica "geostrophic wind".
- [S9] Shipping-forecast terms for the movement of systems, https://www.fatbadgers.co.uk/shipping.htm.
- [S10] "Marine fog over northern Europe based upon ship observations for 1950–2007",
  AMS 97th Annual Meeting, https://ams.confex.com/ams/97Annual/webprogram/Paper307556.html.
- [S11] Simpson, J. E. (1994), *Sea Breeze and Local Winds*, Cambridge University Press;
  Simpson, "The sea-breeze at Lasham", OSTIV; the Reading summary at
  https://www.met.reading.ac.uk/~sws00rsp/teaching/postgrad/keith.pdf.
- [S12] García-Herrera, R. et al. (2005), "CLIWOC: a climatological database for the
  world's oceans 1750–1854", Climatic Change 73, 1–12 (paywalled); Wikipedia "CLIWOC".
- [S13] Können, G. P., Koek, F. B. (2005), "Description of the CLIWOC database", Climatic
  Change 73, 117–130; preprint https://cdn.knmi.nl/system/data_center_publications/files/000/066/393/original/konnen_2004_cc_preprint.pdf
  (Tables I to VI read here).
- [S14] Jones, P. D. et al. (2007), *Climatological observations from ship logbooks
  between 1750 and 1854 (release 2.1)*, PANGAEA, CC-BY-3.0,
  https://doi.org/10.1594/PANGAEA.611088.
- [S15] HistoricalClimatology.com, "Climate history databases",
  https://www.historicalclimatology.com/databases.html.
- [S16] Freeman, E. et al. (2017), "ICOADS Release 3.0: a major update to the historical
  marine climate record", Int. J. Climatol. 37, 2211–2232.
- [S17] ERA5, Copernicus Climate Change Service, CC-BY-4.0, 1940 to present,
  https://climate.copernicus.eu/hourly-weather-and-climate-snapshots-now-available-1940.
- [S18] NOAA-CIRES-DOE Twentieth Century Reanalysis v3, 1836 (public) and 1806
  (experimental) to 2015, CC-BY-4.0 at NCAR RDA; https://reanalyses.org/node/3637.
- [S19] Wikipedia, "Beaufort scale" (history, letters, adoption), and "Francis Beaufort".
- [S20] Royal Museums Greenwich, marine barometer by Nairne & Blunt, after 1774
  (Cook's), https://www.rmg.co.uk/collections/objects/rmgc-object-43017; Nairne's 1773
  patent design as described at https://www.oldsaltblog.com/?p=90.
- [S21] The National Archives, "Sailors, storms and science: how Royal Navy logbooks help
  us understand climate change", https://media.nationalarchives.gov.uk/index.php/sailors-storms-and-science-how-royal-navy-logbooks-help-us-understand-climate-change.
- [S22] Barometer plate words and inches, museum examples, e.g.
  https://data.fitzmuseum.cam.ac.uk/id/object/95988; Scientific American, Notes and
  Queries, 7 October 1911.
- [S23] FitzRoy, R. (1859), *Barometer and Weather Guide*, 3rd ed., Project Gutenberg
  23921, https://www.gutenberg.org/files/23921/23921-h/23921-h.htm.
- [S24] Luce, S. B. (1884), *Text-Book of Seamanship*, "The Weather, the Barometer, Laws
  of Storms", `docs/references/luce/luce-1884-textbook-of-seamanship-ocr.txt` from line
  32060.
- [S25] Wikipedia, "Buys Ballot's law" (Comptes Rendus, 9 November 1857; Ferrel 1856).
- [S26] Ross, J., *The Law of Storms* (Project Gutenberg 55774), on Brandes, Dove 1828,
  Redfield 1831, Reid 1838; Wikipedia "Henry Piddington" (Horn-Book 1844, 1848).
- [S27] Richardson, C. W. (1981), "Stochastic simulation of daily precipitation,
  temperature, and solar radiation", Water Resources Research 17, 182–190.
- [S28] Wikipedia, "Douglas sea scale" (1921).
- [S29] Kramer, M., NWS Charleston, "Wind gust climatology" (2013),
  https://www.weather.gov/media/chs/research/Kramer-WindGustClimo.pdf.
- [S30] Blaes, J. et al., NWS Raleigh, "Developing a dataset of wind gust factors", NWA
  2013 poster, https://www.weather.gov/media/rah/science/NWA_2013_RAH_Blaes_poster_Gust_Factor_final.pdf;
  Vickery, P. J., Skerlj, P. F. (2005), J. Appl. Meteor. 44, 1807–1826.
- [S31] "An overwater relationship between the gust factor and the exponent of power-law
  wind profile", Mariners Weather Log, April 2008, https://vos.noaa.gov/MWL/apr_08/overwater.shtml.
- [S32] Harper, B. A., Kepert, J. D., Ginger, J. D. (2010), *Guidelines for converting
  between various wind averaging periods in tropical cyclone conditions*, WMO/TD-No.
  1555 (table not reached).
