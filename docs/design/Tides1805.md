# Design study: the tide, 1805

From the owner's ruling 4 of 2026-09-29 on the milestone 5 scoping draft: the tide is
to be explored before deciding. Milestone 5's sea is the western Channel and the
Western Approaches, Falmouth to Ushant and Brest. The tide has to set the ship, open
and close harbours, and be something a captain of 1805 reckons with by the period's
means. The lead recommended a simplified semi-diurnal model with springs and neaps and
streams by area, on the ports' real establishments. This study asks whether that is
right, what the alternatives cost, and what data is open. A design note for the M5b
specification; not itself a specification.

Sources are cited inline. Modern figures come from the tide-gauge constants of the
TICON dataset (CC BY 4.0), SHOM's published levels (Licence Ouverte), and published
summaries of the Admiralty atlases; period practice from Moore 1799, Bowditch 1802,
Norie 1803 and Whewell 1833, read in the Internet Archive scans, and from the texts
already in `docs/references/`. Section 6 lists what could not be verified.

## 1. The tide as it is

### Heights

The whole area is semi-diurnal: two tides a day of nearly equal height, the range
doubling from neaps to springs, the wave running up-Channel from the Atlantic so that
high water comes about six hours earlier at Scilly than at Dover. Amplitudes in metres
from the TICON constants (Piccioni et al. 2019, PANGAEA 896587, from the GESLA-2
records of BODC, REFMAR and UHSLC gauges; CC BY 4.0), with the form factor
F = (K1+O1)/(M2+S2) and the mean lunitidal interval taken as the M2 phase lag divided
by 28.984 degrees per hour (my computation from the file):

| Gauge | M2 | S2 | N2 | K1 | O1 | F | 2(M2+S2) | 2(M2-S2) | M2 lag |
|---|---|---|---|---|---|---|---|---|---|
| St Mary's, Scilly | 1.76 | 0.60 | 0.35 | 0.06 | 0.05 | 0.05 | 4.7 m | 2.3 m | 4h 31m |
| Newlyn (for Falmouth) | 1.71 | 0.57 | 0.33 | 0.06 | 0.05 | 0.05 | 4.6 m | 2.3 m | 4h 37m |
| Devonport (Plymouth) | 1.68 | 0.61 | 0.32 | 0.08 | 0.06 | 0.06 | 4.6 m | 2.2 m | 5h 18m |
| Brest | 2.05 | 0.75 | 0.42 | 0.06 | 0.07 | 0.05 | 5.6 m | 2.6 m | 3h 46m |
| Le Conquet | 2.02 | 0.73 | 0.41 | 0.07 | 0.07 | 0.05 | 5.5 m | 2.6 m | 3h 49m |
| Roscoff | 2.69 | 1.00 | 0.53 | 0.08 | 0.07 | 0.04 | 7.4 m | 3.4 m | 4h 54m |
| St Helier, Jersey | 3.34 | 1.30 | 0.66 | 0.09 | 0.08 | 0.04 | 9.3 m | 4.1 m | 6h 17m |
| Saint-Malo | 3.68 | 1.44 | 0.72 | 0.09 | 0.08 | 0.03 | 10.2 m | 4.5 m | 6h 08m |
| Cherbourg | 1.87 | 0.70 | 0.37 | 0.09 | 0.06 | 0.06 | 5.1 m | 2.3 m | 7h 53m |
| Weymouth | 0.60 | 0.31 | 0.13 | 0.09 | 0.05 | 0.15 | 1.8 m | 0.6 m | 6h 36m |
| Dover | 2.25 | 0.71 | 0.41 | 0.05 | 0.06 | 0.04 | 5.9 m | 3.1 m | 11h 27m |

Published mean levels agree. Falmouth MHWS 5.3, MHWN 4.2, MLWN 1.9, MLWS 0.6 m, so
4.7 m at springs and 2.3 m at neaps; Plymouth 5.5, 4.4, 2.2, 0.8 m (4.7 and 2.2 m);
St Mary's 5.7, 4.3, 2.0, 0.7 m (5.0 and 2.3 m); the same sites give high water at
HW Dover -0610, -0540 and -0630 respectively (eoceanic harbour pages, crediting UKHO
data via "Tide Times"). SHOM's Références Altimétriques Maritimes (RAM 2025, CSV in the
7z package on data.gouv.fr, Licence Ouverte 2.0) give Brest PMVE 7.05, PMME 5.50,
NM 4.14, BMME 2.70, BMVE 1.15 m above chart datum, so 5.9 m at mean springs and 2.8 m
at mean neaps, the extreme astronomical range 7.7 m; Le Conquet 6.85/1.10; the Stiff
on Ushant 7.15/1.00; Roscoff 8.90/1.30; Saint-Malo PMVE 12.20, PMME 9.30, BMME 4.30,
BMVE 1.50 m, so 10.7 m at springs, with Granville 12.85 m PMVE; Cherbourg 6.45/1.15.
Jersey's springs run to about 11 m above datum and "up to 12+ m" in extreme tides
(Government of Jersey tide page); Braye, Alderney, springs to 6.3 m (search summary of
pilot data, unverified against a primary). For contrast the whole game area has 4.6 to
5.9 m springs; the Gulf of St Malo two to three times that.

The RAM file also carries the establishment of each port as a decimal hour
("Etablissement décimal", per SHOM's product description): Brest 3.75 (3h 45m), Le
Conquet 3.81, Lampaul 3.81, the Stiff 4.13, Roscoff 4.90, Saint-Malo 6.13, Granville
6.34, Cherbourg 7.88. These match the M2 lags above to within a few minutes, which
confirms the arithmetic and shows that a modern establishment is nothing more than
the M2 phase.

### The spring-neap cycle and the inequalities

S2/M2 is 0.33 to 0.39 everywhere in the area, so springs are about 1.35 times the mean
range and neaps about 0.65, springs twice neaps; the cycle is 14.77 days. Springs fall
one to two days after new and full moon (the "age of the tide"; Bowditch 1802 says
"about three days after"). N2/M2 is 0.19 to 0.20, so perigean springs exceed apogean
by about 20%, a difference the period knew (Bowditch: "when the moon is in her perigee
... the tides rise higher"). The diurnal constituents are 5 to 9 cm each; F is 0.03 to
0.06 at every port, so successive high waters differ by 10 to 20 cm and the model can
ignore them. Weymouth's F of 0.15 with a 14 cm M4 is the signature of Portland's
double tides and shows what a model without shallow-water terms will miss east of
Start Point; inside the M5 box nothing of the kind occurs.

### Streams

Rates from published summaries of the Admiralty tidal stream atlases (NP250 English
Channel West, NP255 Falmouth to Padstow, NP257 Portland), as quoted on eoceanic's
route pages and in the search digests; the atlases themselves are Crown copyright and
were not read.

- **Open Channel off the Lizard**, 5 miles south: 2.3 knots at springs, 1.1 at neaps,
  both directions, nearly rectilinear ("off Lizard point and off Start point the
  streams are fairly strong and nearly rectilinear"). A race lies up to 2 miles south
  of the point where the streams meet over uneven ground.
- **Falmouth approaches**: 5 miles east of St Anthony Head 0.7 knots, the east-going
  stream beginning at HW Dover +0245 (HW Devonport -0400), the west-going at HW Dover
  -0330; off the Manacles 1.1 to 1.3 knots, rotating clockwise; the harbour entrance
  1 knot at springs and 0.5 at neaps; Carrick Roads 1.5 to 2 knots in the lower
  reaches, 3 in the upper (visitmyharbour, Carrick Roads).
- **Start Point**, 3 miles south: the WSW-going stream from HW Dover -0120 to +0445,
  the ENE-going from +0445 to -0120; 3 knots off the point, a race a mile south and
  east, "particularly pronounced during spring tides".
- **Scilly**: rotary streams round the isles, 0.6 to 1.5 knots at springs; between
  the isles and Land's End 1.8 knots SSE-going at HW Dover -0340 and 1.6 knots N-going
  at +0245; the Runnel Stone west-going window HW Dover -0200 to +0100 ("only a 3-hour
  window of fair west-going tide from Land's End to the Scillies"); from Scilly an
  eastward stream from +0500 to -0500.
- **Portland**: 5 miles south of the Bill the east-going stream begins at HW Dover
  +0545; the race is charted at 7 knots and 10 have been reported; slack about
  HW Dover +0500 for eastbound passages. Outside the M5 box but the Channel's worst.
- **The Alderney Race**: north-going 5 m/s (9.5 knots) and south-going 3.5 m/s
  (6.75 knots) at springs, the race 4 miles wide over 30 to 40 m (Southampton SERG,
  Bahaj and Myers 2004-05); Wikipedia's "up to 12 knots" is uncited. Slack about
  HW St Helier +0400, or half an hour before HW Dover (pilot books quoted second-hand
  on a yachting forum; unverified).
- **Ushant and the Fromveur**: the Fromveur (about 2 miles wide) "regularly exceeds
  6 knots at springs" and reaches 9 locally (Figaro Nautisme 2026), 4 m/s in the
  academic literature (Charlier 2003 via Wikipedia); neaps 20 to 30% less (Ifremer);
  the Chenal du Four 3 to 5 knots; the Goulet de Brest 4 to 5 knots (bateaux.com).
  The timing of the Fromveur's turn against HW Brest was not found in an open source.

The turn of the stream relative to high water is the point that matters for a model.
In the western Channel the wave is largely progressive, so the streams run strongest
near local high and low water and slack near half tide: at Start Point the ENE-going
stream ends about four hours after HW Plymouth; off St Anthony Head the east-going
runs from about three hours before to three hours after HW Falmouth. The period knew
exactly this. Bowditch 1802 prints, from the English tables, a headland table with
three columns, "the time of high water at the principal headlands in the channel on
full and change days", "the time the current runs after high water" and "the time the
current has done running": Lizard 5h 00m, 3h 00m, 8h 00m; Eddystone 5h 30m, 3h 00m,
8h 30m; the Start 6h 10m, 2h 30m, 8h 40m; Portland 7h 15m, 3h 00m, 10h 15m; the Isle of
Wight 8h 14m, 3h 15m, 11h 29m; and states "the Current in the Mid. Channel is N.E.
about 1 H. 30 M. after High Water". Three hours after local high water is within an
hour of the modern atlas at every headland.

## 2. What a captain of 1805 knew and used

**The establishment.** Every port had a "time of high water at full and change", the
hour of high water on the day of new or full moon, called the establishment of the
port; Whewell 1833 distinguishes this "vulgar establishment" from the "corrected
establishment", the mean interval between the moon's transit and high water. The
period's figures for our ports, from Dessiou's Plymouth tide tables and Sailing
Directions and from Daussy in the Connaissance des Temps for 1834, all quoted by
Whewell: Scilly 4h 10m (Lubbock 4h 30m), Land's End 4h 20m, Mount's Bay and the Lizard
4h 30m, Falmouth Harbour 5h 15m, Fowey 5h 15m, Eddystone 5h 15m, Plymouth 5h 33m
(the mean establishment), Dartmouth and Torbay 6h 00m, Portland Bill 5h 30m, Dover
10h 50m; Ushant 3h 47m, Brest 3h 48m, Morlaix 5h 15m, St Malo 6h 00m, Jersey 6h 10m,
Guernsey 6h 30m, Alderney 6h 45m, Cherbourg 7h 45m. Set against the modern M2 lags
these are right to within twenty minutes at Brest, St Malo and Plymouth and within
half an hour elsewhere; the older tables were worse. Moore's New Practical Navigator
(1799 edition) arranges its table by the moon's bearing at high water, a point of the
compass to every 45 minutes ("S. by W." 12h 45m, "S.S.W." 1h 30m, ... "W." 6h 00m ...),
in the manner of the seventeenth-century pilots, and groups Brest with the 3h 45m
places, Ushant and Scilly at 4h 30m, and Plymouth, Ramhead and Torbay at 6h; the OCR
does not let me pin Falmouth's group with confidence. Norie's Complete Set of Nautical
Tables (1803) has a Table XLI, "the times of high water at full and change, and the
vertical rise of the tide at spring tides, the names of the places being
alphabetically arranged", with the author's plea to mariners to report errors.

**The rule for the hour.** Moore 1799, in the catechism: "I multiply the moon's age by
48, and divide the product by 60, the quotient will be the hours, and the remainder
the minutes when she is on the meridian past noon; or ... multiply the moon's age by 4,
and divide the product by 5"; then "the hours and minutes ... being added to the time
of high water on the change and full days, at any place, will ... give the time of high
water there". The moon's age came from the almanac or the golden-number table ("page
138"). Bowditch 1802 uses 49 minutes a day, adds a "Table B" for the sun's priming and
lagging, and is candid: the simple rule "will sometimes differ an hour from the truth,
owing to the neglect of the disturbing force of the sun". Norie 1803 has the same
correction as Table XLII, by the moon's quarter and the interval. The inverse problem
is also in Moore: in a strange harbour, note the hour of high water by the watch,
subtract the moon's southing, and you have the establishment.

**The tables that existed.** Liverpool's tables by Richard and George Holden from 1770,
built on the dock master William Hutchinson's observations of 1764 to 1767 and claiming
in 1773 agreement "within seven inches and within five minutes" (tide-and-time.uk,
NOC), were the only predicted tables of the kind; the Admiralty's first Tide Tables
came in 1833 for four ports (London, Plymouth, Portsmouth, Sheerness) by Lubbock's
method of averages (Hughes and Wall, J. Navigation 2004), and Whewell's cotidal map the
same year. In 1805 a Channel captain had the establishments in his epitome, the
almanac for the moon, and the sailing directions for the streams; nothing else.

**The sailing directions.** The English Pilot (to 1803) and the Channel Pilots carried
tide notes with each harbour; Collins's Coasting Pilot (1693) advertised "the setting
and flowing of the tides"; Bougard's Petit Flambeau de la Mer (1684 to 1789) served the
French side. Moore's catechism has Falmouth itself: "there is a rock, called the Black
Rock, with a pole on it, and shews itself at half tide; it lies nearest to the west
shore; I may sail in on either side of it, but the east side is the best. If I would
sail into Carrick road, I must keep in the fair way, and my lead going as there is a
narrow deep channel all the way, of 16 or 18 fathoms; may borrow on St. Maw's side in
5 or 6 fathoms." Steel 1794 (vol. II, getting under way from river moorings): "let it
be a rule, when the tide serves, to get underway, and sail against the flood"; and on
anchoring, let go "stemming the tide, especially with a rapid tide, for it gives an
opportunity to observe at what rate the ship drives astern". Lever 1808 and Luce 1866
supply the vocabulary the log will need: windward tide, leeward tide, weather flood,
lee ebb, to stem the tide, to be neaped.

**The rule of twelfths.** Absent from Moore 1799, Bowditch 1802 and Norie 1803, which
give the hour by the moon's age and the height only as the "spring rise" of the port.
A full-text search of the Internet Archive's scanned books for the phrase returns
only late-twentieth-century yachting manuals (RYA, Cunliffe, Reeds); its origin is
unverified and it should not be put in an 1805 mouth. The period judged the height
between the tides by eye and by the lead.

**The lead as a tide gauge.** Falconer 1780, "Sounding": the hand lead of 8 or 9 lb
on a 20-fathom line marked at 2, 3, 5, 7, 10, 13, 15 and 17 fathoms, called "by the
mark five", "and a quarter five", "a quarter less five"; the deep-sea lead of 25 to
30 lb. A lead over the side at anchor shows the water making or falling, and the
sounding compared with the chart's depth is the height of the tide; that this was
done is an inference from practice, not a quoted rule.

**The set in the reckoning.** Bowditch 1802, "Currents": "the set of a current is that
point of the compass towards which the waters run, and its drift is the rate it runs
per hour"; to find an unknown current, a boat holds a kettle sunk 80 or 100 fathoms and
heaves the log against it; and the rule, "all cases of sailing in a current are
calculated upon the principle, that the ship is affected in the same manner by the
current, as if she had sailed in still water, with an additional course and distance
exactly equal to the course and set of the current", worked in the traverse table as
one more course. The journal form in the same book carries a column for it. The
master's estimate of the tide's set was therefore an entry in the day's traverse, and
its error an error in the reckoning.

## 3. Open data

- **The IHO Tidal Constituent Bank** was run by the Canadian Hydrographic Service for
  the IHO from 1978 and disbanded in 2000 (IHO Circular Letter 19/2000) because member
  states restricted dissemination as commercial use grew. It is not a source.
- **UKHO.** Harmonic constants for UK ports are Crown copyright and sold or licensed
  (the gov.uk algorithmic transparency record for UKHO tidal analysis; the Admiralty
  EULA). The UK Tidal API's Discovery tier is free (10,000 calls a month, seven days of
  predictions) but is predictions only and not redistributable. The tidal stream
  atlases NP250, NP255 and NP257 are copyright; sites that show them license them.
- **BODC / NTSLF.** The quality-controlled tide-gauge records from 1915 are "available
  free of charge" after registration and agreement to a data licence (BODC UK tide
  gauge network page); I could not confirm it is the Open Government Licence. One may
  analyse the records oneself; GESLA and TICON did.
- **TICON (2019)**, Piccioni, Dettmering, Bosch and Seitz, PANGAEA 896587, CC BY 4.0:
  40 constituents at 1,145 gauges from GESLA-2, including St Mary's, Newlyn, Devonport,
  Weymouth, Dover, Brest, Le Conquet, Roscoff, Saint-Malo, St Helier and Cherbourg,
  the figures in section 1. **TICON-3** (Hart-Davis et al. 2022, PANGAEA 951610,
  CC BY 4.0) has 3,471 gauges but its public file has none of the western Channel
  stations (Dover is its westernmost in the Channel); I did not find the reason. TICON
  2019 is the open answer for the ports.
- **SHOM.** The RAM (levels and establishments, all French ports) is Licence Ouverte
  2.0. The 2D tidal current atlases in NetCDF (Shom 2026, DOI
  10.17183/ATLASCOURANTS2D_NETCDF, Licence Ouverte 2.0) give surface U and V hour by
  hour from six hours before to six after high water at a reference port, for mean
  neaps and mean springs (coefficients 45 and 95), from TELEMAC-2D models; the western
  Brittany set covers 47.63 to 48.89 N, 5.56 to 4.22 W at 500 m, the Iroise at 250 m,
  Brest roads at 100 m. That is the Fromveur, the Four and the Goulet, open. A Channel
  set exists; its western limit I did not confirm. SHOM's harmonic constants are a
  priced product and not open (not fully verified).
- **Global models.** EOT20 (DGFI-TUM, SEANOE, CC BY 4.0): 17 constituents at 1/8
  degree, elevations only; may ship. FES2014 (AVISO, registration): elevations "issued
  for any type of application", currents "for scientific applications and
  non-commercial use", 1/16 degree, 34 constituents with U and V. FES2022: 1/30 degree,
  elevations; currents on request only. TPXO (OSU copyright): free for academic and
  non-commercial use with registration, commercial use licensed separately; not for an
  open game's data files. pyTMD (MIT) reads all of them. All are too coarse at the
  coast for a harbour and none is needed if the ports come from TICON.
- **Copernicus Marine NWSHELF** (1/36 degree, about 3 km): hourly and 15-minute
  currents and sea level from a tidal model; the licence is free, permits
  redistribution and derived works "for any purpose" with attribution. A month of its
  output analysed harmonically would give an open stream field for the whole box, at a
  resolution that blurs a 2-mile race.
- **Deriving streams.** Depth-averaged shallow-water models reproduce the Channel's
  streams: Pingree and Maddock 1977 (tidal residuals, JMBA 57), Pingree and Griffiths
  1979 (M2 and M4 interactions), Le Provost and Fornerino 1985 (tidal spectroscopy of
  the Channel, JPO); SHOM's atlases are such a model's output. So streams can be
  computed rather than tabulated, if the raster is fine enough. The height gradient
  alone does not give the stream: the streams of a progressive wave are in phase with
  the height, those of a standing wave a quarter period out, and the Channel is a
  mixture. EMODnet's bathymetry DTM 2024 (about 115 m, CC BY 4.0) would serve a model.

## 4. Three models

**(a) One cosine per port, spring-neap modulated, streams by area, all hand-tabulated.**
Height h = A(t) cos(2π (t − t_HW)/12.42 h) with A swinging between the neap and spring
half-ranges on the 14.77-day cycle, t_HW from the establishment and the moon's age;
each area a direction axis, a spring rate, a neap rate and a phase against local high
water, from Bowditch's headland table checked against section 1. Fidelity: the hour
right to half an hour, the range right to 10%, no perigean tides, no age of the tide
unless added by hand. Data: a table of a dozen ports and a dozen areas, all from the
period texts (public domain) and this study. Code: a hundred lines; per tick a cosine
at the ship's position, evaluated once a simulated minute. Play: the window at
Falmouth (the flood to carry her in, the ebb to carry her out), the set across the
Channel (a knot for six hours each way, a net drift of a mile or two on a crossing),
a race zone with an extra rate and a sea.

**(b) A few constituents per port from TICON, interpolated, streams by area.**
h = Σ f_i A_i cos(ω_i t + V_i + u_i − g_i) for M2, S2, N2 (K1 and O1 are 5 cm and can be
dropped); amplitudes and phases interpolated along the coast between gauges and
across the Channel by the cotidal geometry of section 1; the ship's own tide from the
nearest interpolated point. The astronomical arguments V_i for 1805 are three
formulae (the moon's mean longitude, the sun's, the lunar perigee) or, simpler and in
the period's own terms, are set so that high water at full and change falls at the
port's establishment, the moon's age being what the scenario's almanac says. Streams
as in (a), since the gradient will not give them. Fidelity: heights right to 10 cm
and ten minutes at the gauges, the spring-neap and perigean cycles for free, the
inequality ignored. Data: eleven gauges from one CC BY file, the RAM for the French
establishments. Code: (a) plus a constituent table, perhaps 150 lines, and a
generator to check the phases against the establishments. Per tick, five cosines.
Play: as (a), plus tides that behave over a month as the almanac says they should.

**(c) A depth-averaged shallow-water model on the chart raster.** Solve the 2D
equations on EMODnet depths, forced at the open boundaries from EOT20 or FES; height
and stream fall out together, including the races and the eddies behind headlands.
Fidelity: the best available in principle, but only at 100 to 250 m cells, where the
Fromveur is ten cells wide; at the 1 km the chart study proposes it is two, and the
race is smeared. Stability wants a time step under 30 s at 1 km over 100 m depths,
and friction and boundary tuning against data that is not open for the English side.
Data: the raster (CC BY 4.0) and a global model's boundary values (EOT20 may ship).
Code: a week to run, longer to trust; per tick, 40,000 cells every 30 simulated
seconds, feasible in numpy at 40x compression but a permanent load on the pace
(truth 51) for a field that repeats every 14.77 days. The honest form of (c) is to run
it once offline and ship the result as a tabulated field, which is what SHOM does; and
then it is (b) with a better stream table.

## 5. Recommendation

Build (b), with the streams tabulated by area as in (a), and keep two tides apart as
the reckoning keeps two positions apart.

1. **The world's tide** is M2, S2 and N2 at the eleven TICON gauges, interpolated, with
   the streams by area from the figures in section 1 and the SHOM atlas where it
   covers (the Fromveur, the Four, the Goulet). This is the truth the ship moves in:
   the depth under the lead, the set on the track, the rock that covers.
2. **The captain's tide** is the establishment of the port from his epitome and the
   moon's age from his almanac, worked by Moore's rule of 48 minutes a day; it is wrong
   by up to an hour, as Bowditch admits, and by more when his book's establishment is
   an old one (Moore's 45-minute compass points). The difference between the two tides
   is play, exactly as the difference between the true and the reckoned position is.

Why not (a): a cosine with a spring-neap swing is M2 and S2 by another name; adding
N2 costs nothing and buys the perigean springs that the period noticed and that make
one spring tide flood the quay and the next not. Why not (c): the box is a hundred
miles square and the ship is one; a field that repeats every fortnight is a table, not
a simulation, and the one place the raster cannot resolve (the Fromveur) is the one
place SHOM has already tabulated under an open licence.

**Exposure, by the period's means only.** No tide readout, ever. The captain has:

- The establishment table in the ship's papers (`Papers-and-Books.md`): the epitome's
  table of high water at full and change, by port, in hours and minutes or in points
  of the moon's bearing, with the spring rise; a poorer ship has a poorer table.
- The moon's age and phase from the almanac (the scenario already gives the sun a
  date; the moon follows), and the moon itself in the sky reading of M5a.
- The lead: `heave the lead` returns the true depth under the keel, which includes the
  tide; against the chart's depth that is the height of the tide, and at anchor the
  lead over the side says whether it is making or falling.
- The shore: a landmark's state (the Black Rock shows at half tide; the sands dry;
  St Mawes bar covers) is a reading in the log line the lookout gives.
- The ship: she rides to the tide at anchor, the cable slackens at slack water, she
  stems the ebb or drives with it; the log's line says "riding to the flood, wind
  across the tide". These are consequences the sail and hull model already show; the
  tide adds its water to the same equations.
- The reckoning: the master's estimate of set and drift goes into the traverse as a
  course (`work up the reckoning` takes an allowance for the tide); the error is
  discovered by a bearing or a landfall, as in 5b's gate.

**What the language-model captain reads.** Exactly the same: the papers by handle
(the establishment table, the almanac's moon), the readings registry (depth by the
lead, the lookout's landmark states, the ship's riding), the log lines, and its own
reckoning. No model gets a number the human does not, per `InwardAndOutward.md`. The
primer should carry the rule of 48 minutes and the headland table, since a captain of
1805 knew them by heart.

**For the M5b specification**, in order: the constituent table (a data file naming
TICON and the RAM as sources, CC BY 4.0 and Licence Ouverte, with the licence text
under `docs/references/`); the stream areas as a data file naming Bowditch 1802 and
the atlas summaries; the two-tide rule stated as a truth; the readings and orders
above; the Falmouth and Brest scenarios that use them (the flood into Carrick Roads;
the Goulet against the ebb); a playtest form asking whether the tide was ever seen
as a number.

## 6. What could not be verified

- Norie's 1805 Epitome and the Nautical Almanac for 1805 were not read; that the
  Almanac carried no tide table is my belief, not a checked fact. Norie's 1803 tables
  were read in OCR and Table XLI's Channel rows were illegible; the establishments here
  are Dessiou's and Daussy's as quoted by Whewell 1833, and Moore's 1799.
- The Admiralty atlases were not read; every stream figure is a published summary of
  them, and the timing of the Fromveur and the Alderney Race against high water rests
  on secondary or forum sources.
- The rule of twelfths' origin; the Braye range; the BODC licence's exact terms; the
  reason TICON-3 omits the western Channel gauges; SHOM's terms for its harmonic
  constants; the western limit of SHOM's Channel current atlas.
- The RAM 2025 PDF and the SHOM atlas samples are image PDFs and were not read; the RAM
  figures are from the CSV in the same package.

## Sources

Period, in `docs/references/`: Falconer 1780 ("Tide", "Sounding", "Ebb"); Steel 1794
vol. II (getting under way from river moorings; to come to an anchor with the wind
across the tide); Lever 1827 printing (glossary, "Neap Tides", "Neaped"; anchoring in a
tideway); Luce 1866 ch. on tides ("Definition of Tides"). Period, read online: J. H.
Moore, The New Practical Navigator, 1799 (archive.org
bim_eighteenth-century_the-practical-navigator_moore-john-hamilton_1799), tide rule,
table by the moon's bearing, catechism on Falmouth; N. Bowditch, The New American
Practical Navigator, 1802 (archive.org newamericanpract00bowd), "Tides", "Currents",
the Channel headland table; J. W. Norie, A Complete Set of Nautical Tables, 1803
(archive.org 11766165bsb), Tables XLI and XLII; W. Whewell, "Essay towards a first
approximation to a map of cotidal lines", Phil. Trans. 1833 (darwin-online
1833_Whewell_A839), establishments and the vulgar/corrected distinction.

Modern: TICON, Piccioni et al. 2019, Geoscience Data Journal 6(2), data PANGAEA
doi:10.1594/PANGAEA.896587 (CC BY 4.0); TICON-3, Hart-Davis et al. 2022, PANGAEA
doi:10.1594/PANGAEA.951610; SHOM, Références Altimétriques Maritimes 2025, data.gouv.fr
(Licence Ouverte 2.0) and its product description; SHOM, 2D tidal current atlas in
NetCDF, doi:10.17183/ATLASCOURANTS2D_NETCDF; EOT20, Hart-Davis et al. 2021, ESSD 13,
SEANOE 00683/79489; AVISO FES2014/FES2022 product page; OSU TPXO registration page;
Copernicus Marine service licence; gov.uk algorithmic transparency record, UKHO tidal
harmonic analysis; BODC UK tide gauge network; IHO Circular Letter 19/2000; eoceanic
harbour and route pages for Falmouth, Plymouth, St Mary's, Start Point to the Lizard,
Land's End to Scilly; visitmyharbour, Carrick Roads and Portland; Southampton SERG,
Alderney tidal race study 2005; Figaro Nautisme, Passage du Fromveur, 2026; Wikipedia,
Fromveur Passage, Alderney Race, Establishment of a port, Rule of twelfths (and its
references); tide-and-time.uk (Holden and Hutchinson); Hughes and Wall, "Admiralty
tidal predictions of 1833", J. Navigation 2004; Pingree and Maddock 1977; Pingree and
Griffiths 1979; Le Provost and Fornerino 1985.
