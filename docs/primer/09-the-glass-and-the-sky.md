# 9. The glass and the sky

Since milestone 5 the wind has a cause. Somewhere beyond the horizon a low is passing or a high is sitting, and what the ship feels of it comes through three things a captain of 1805 could read: the barometer in his cabin, the sky over his masthead, and the wind itself. This chapter says what the game gives you of each, in what words, and what a seaman of the period made of them. It does not tell you where the low is. The game keeps the truth and you keep your account, as he did.

## The glass

If the ship carries a barometer (the scenario file says, `glass: true` under `ship:`; the frigate of the scenarios shipped with the game has her captain's own, and a small vessel may well have none), `the glass` is a reading: the height of the mercury in inches, to the hundredth, as the vernier of a marine barometer reads it.

```
the glass is 29.72 inches
```

A marine glass of the period is Nairne's pattern of about 1773, a stick barometer with its bore pinched to stop the mercury pumping with the ship's motion, hung in gimbals in the cabin; Cook carried one, and by 1805 an officer who wanted one bought it himself, since the Admiralty did not yet issue them. The reading you get carries the ship's own noise, half a hundredth either way, and in a seaway the mercury pumps with the ship's motion, a hundredth or two in a heavy sea (the section on the sea below).

What the period read from the glass was not its height but its **tendency**, and so the game keeps a second reading, `the tendency`, from the ship's own record of the glass over the last three hours: steady, rising, falling, rising fast, falling fast, with the change in hundredths.

```
the tendency is falling; fallen five hundredths in three hours, two in the last hour
```

A ship with no glass has no tendency either, and both readings answer "the ship carries no glass". A ship that has one has watched it for an hour before the tendency will speak.

The book of standing orders reads both for nothing:

```orders frigate
standing order "the glass": when the glass is falling fast then shorten sail
standing order "low glass": when the glass is under 29.5 inches then take in the topgallants
standing order "clearing": when the glass is rising and the sky is clear then set the royals
```

## What the glass means

The words engraved on a common barometer's plate, Stormy at 28 inches, Rain at 29, Change at 29.5, Fair at 30, Set Fair at 30.5, were known to be worthless long before anyone wrote it down. FitzRoy, whose *Barometer and Weather Guide* of 1859 is the first plain statement of the rules, says the words "should not be so much regarded for weather indications, as the rising or falling of the mercury"; that "the greatest depressions of the barometer are with gales from the S.E., Southward, or S.W.; the greatest elevations, with winds from the N.W., Northward, or N.E."; and that "backing is a bad sign, with any wind". His two rhymes every sailor came to know: *Long foretold, long last; short notice, soon past*, and *First rise after low foretells stronger blow*.

Luce's *Text-Book of Seamanship* of 1884, in its chapter on the weather, the barometer and the laws of storms, quotes FitzRoy and adds the couplet *When the wind shifts against the sun, trust it not, for back it will run*; the law that with east, south-east and south winds the glass falls, with south-west it ceases to fall, and with west, north-west and north it rises; and the warning that "in an ordinary gale, the wind often blows hardest when the barometer is just beginning to rise, directly after having been very low". The ordinary range in these latitudes he gives as 30.5 to 29 inches, the extremes 30.8 and under 28.

FitzRoy and Luce are fifty and eighty years after 1805. They wrote down what the trade already said, and the pairing of a backing wind with a falling glass is the old lore; but the rule of rates, that a fall of a tenth in three hours means much wind, is sailing-school teaching whose period source has not been found, and the game's "falling fast" is set at that tenth while saying so. What the game does with all of this is nothing: it gives you the glass and the sky and lets you learn the rules by sailing under them, which is how they were learned.

## The sky and the weather

`the sky` is given in the words Beaufort was writing into his journal in January 1806, commanding *Woolwich*, which became the weather column of every log: clear, detached clouds, overcast, dark and gloomy, threatening, hazy, thick. To them the game adds, when they apply, the signs Luce lists for the log's colour: "a high dawn" (the first streaks of morning light over a bank of cloud, which foretells wind); "hard-edged and oily-looking" clouds, which foretell wind; "small inky clouds", rain; "a light scud driving across" heavy clouds, wind and rain; and the "streaked and spotty clouds high up" that are the first sign of a change in fine weather.

```
the sky is overcast, small inky clouds
```

`the weather` is fine, rain, drizzle, passing showers, squally, thunder or fog, and `the visibility` is how far a sail could be seen, in the lookout's terms: the horizon, a few miles, a mile, a cable.

The log says these by the hour, with the glass when the ship has one, and at the change of each watch it says how the glass has moved since the watch before:

```
  Forenoon watch, 8 bells (08:00)  Overcast, drizzle; the glass 29.96, fallen two hundredths since the morning watch.
  Afternoon watch (15:13)  The sky threatening, small inky clouds.
  Afternoon watch (15:13)  Rain set in.
```

When the log is rolled up at speed, each hour's line carries the sky, the weather and the glass's movement. The standing dialect compares all three, `the sky is overcast`, `the weather is not rain`, `the visibility is a mile`, on a ship with a glass or without.

## Squalls

Over the open sea a gust is a fifth or a quarter again the mean wind and no more; a wind that does more is a squall, its own event of a few minutes in the cold unstable air behind a front, veering the wind a point or two and bringing rain. The log names it at its start and its end, as a notable line, and the standing orders may wait for it:

```
* First dog watch (16:44)  A squall: the wind veers 2 points to NW by W and freshens to 43 knots, with rain.
* First dog watch (16:48)  The squall passed; the wind W by N, 29 knots.
```

```orders frigate
standing order "squall": at a squall then take in the royals
```

The period shortened sail for a squall it saw coming, by the look of the cloud and the darkening of the water to windward, and made sail again as it passed; the sky's words and the weather's "squally" are what it saw.

## The sea

The wind raises a sea, and the sea outlasts the wind. When a scenario's wind has a cause (the systems of the section below, rather than the pinned wind of milestone 4), the game keeps the sea at the ship, raised by the wind of the last ten minutes and read once a minute, and `the sea` is a reading in the words the period's logs used, never in feet or metres and never in the numbers of the Douglas scale, which is 1921:

```
the sea is a short chopping sea
the sea is a heavy sea
the sea is a moderate sea and a long swell from the westward
the sea is a heavy confused sea, the swell from the north-westward
```

The words are Falconer's and Luce's. Falconer's article *Sea* (1780) has the sailor's uses: "a heavy sea broke over our quarter", "there is a great sea in the offing"; "a long sea implies an uniform and steady motion of long and extensive waves; on the contrary, a short sea is when they run irregularly, broken, and interrupted, so as frequently to burst over a vessel's side or quarter"; and a ship "is said to head the sea, when her course is opposed to the setting or direction of the surges". His *Swell* is "the fluctuating motion of the sea, which remains after the expiration of a storm". Luce (1884, in the weather chapter) gives "a heavy swell or confused agitation of the sea not accounted for in any other way" among the signs of a coming gale, and "a smooth sea" and "a head sea" throughout his chapter on a gale. "A short chopping sea" is the phrase of the period's logs for a fresh breeze's young sea; it is not in the game's copies of the references, and the tuning notes say so.

What the game does with the words: a smooth sea under half a metre of significant height, a moderate sea to a metre and a half, a short chopping sea to two and a half, a heavy sea to six, a very heavy sea above; a swell is named when it stands above the wind's own sea and comes from another quarter, a long swell or a heavy swell; and a swell that crosses the wind by more than five points makes a confused sea. The heights come from the open-sea relation of the wind's speed (a fresh breeze of a day raises a sea of about two metres, a strong gale of a night six or seven) with a lag of hours to build and of hours to go down, and the swell a gale leaves decays over a day. The numbers are in `docs/dev/TuningNotes.md` and nowhere a player reads.

The log says the sea when its words change, and the hour's line carries it with the glass:

```
  Forenoon watch (10:41)  A short chopping sea getting up.
  First dog watch (17:26)  A heavy sea getting up.
  Middle watch, 5 bells (02:30)  Overcast, drizzle; the glass 29.62; a heavy sea, rolling heavily.
  Afternoon watch (13:07)  A heavy sea, the sea going down.
```

## The ship's motion

A ship in a sea rolls, pitches and heaves, and the game keeps the three as numbers with the period's words for them in `the motion`: *easy*; *rolling easily*, *rolling*, *rolling heavily*; *pitching a little*, *pitching into it*, *pitching heavily into it* (or, with the sea under her stern, *pitching heavily, the sea under her stern*); and *labouring heavily* when she does both. Falconer's *Rolling* is "the motion by which a ship rocks from side to side like a cradle, occasioned by the agitation of the waves", and his *Sea-boat* "a vessel that bears the sea firmly, without labouring heavily, or straining her masts and rigging"; Luce's chapter on a gale has a vessel that "labors much in a seaway" and a pitching that "is hard and quick".

```
the motion is rolling heavily
the ship's motion is easy
```

The roll comes from the sea on the beam against the ship's stability: the frigate rolls at her own period of about eight seconds, and rolls most in the sea whose period is near her own, a moderate gale's sea, and less in a long swell however high; she rolls some with the sea on her quarter and little with it right ahead or astern. The pitch comes from the sea ahead or astern, and a ship does not pitch to a sea shorter than herself. Nothing in this moves the ship over the water: it is what the hands and the gear feel.

What they feel, each in one place: the hands aloft work slower as she rolls, so a reef in a heavy sea takes half as long again as in a smooth one (Luce: "when a vessel labors much in a seaway ... the sails should never be hoisted up, or the braces hauled, as taut as in a smooth sea; for the jerk of the masts will either carry away the braces and sheets or spring the yards"); the spars and their gear are judged against their ratings with that jerk added, a fifth more at twenty degrees of roll, so the same canvas that stands in a smooth sea carries away in a heavy one; a head sea costs her speed ("by forcing her through a head sea, you strain every mast and yard, and injure the rigging", Luce again); and the glass pumps. The standing orders read both readings:

```orders frigate
standing order "heavy sea": when the sea is heavy then take in the topgallants
standing order "labouring": when the motion is labouring heavily then reef the topsails, one reef
standing order "easy again": when the sea is not heavy and the motion is easy then set the topgallants
```

The log says the motion when its words have changed and held for five minutes:

```
  Last dog watch (18:33)  Rolling heavily.
  First watch (23:19)  Labouring heavily.
  Morning watch (05:52)  Pitching heavily, the sea under her stern.
```

## A gale: storm canvas, lying to, and boxing her off

Luce's order of reducing sail to a gale is the game's (Luce 1884, ch. XXIX, 'Reducing Sail to a Gale'; his journal's scale, Luce 1866, ch. XXVIII: "7. Moderate gale; double reefed topsails. 8. Fresh gale; treble reefed topsails and reefed courses. 9. Strong gale; close reefs. 10. Whole gale; close reefed main topsail"). `shorten sail` takes in the light sails and reefs the topsails once each time it is given, as chapter 3 says, and as the wind rises it does more:

- **the jibs by their ratings.** A jib whose load is three quarters of what its canvas is rated for is taken in, the outermost first, before a gust blows it out of the bolt-ropes ("To take in the jib when blowing hard, it is always better to run the ship off if possible");
- **the after sail with the head sail.** With the second reef in the topsails the courses are reefed; with the third, the mainsail is hauled up and the spanker taken in, so that a ship that has lost her jibs does not come to against her helm with her mainsail and spanker driving her stern off;
- **the storm staysails** over forty knots of wind, or sooner if the fore topmast staysail is loaded near its rating.

**Set the storm staysails** is the order for them, in any wind: each storm staysail the ship carries in her sail room is bent if it is not, set as soon as it is bent, and what it replaces taken in once it is set, so that she is never without a head sail while the hands rouse it up ("To set fore-storm staysail, and haul down fore topmast staysail, proceed as in taking in jib and setting fore topmast staysail", Luce 1884, p. 477). The fore storm staysail replaces the fore topmast staysail and the jibs; the mizzen's (the brig's main storm staysail) replaces the spanker as the after sail. A schooner or a cutter carries a storm jib in the jib's place, and it is shifted for the jib.

```orders frigate plain-sail
set the storm staysails
shorten sail
```

```
  First watch (21:16)  Order: set the storm staysails.
  First watch (21:16)  Bend sail! Rouse up the fore storm staysail from the sail room. Bend sail! Rouse up the mizzen storm staysail from the sail room. The fore storm staysail and mizzen storm staysail to be set as soon as they are bent.
  ...
  First watch (21:41)  Clear away the fore storm staysail; man the halyards.
  First watch (21:43)  Set the fore storm staysail.
  First watch (21:43)  The fore storm staysail set in place of the fore topmast staysail and the jib.
```

**Lying to in a gale** is under the close-reefed main topsail, braced up, and the storm staysails, the helm a little a-lee: `lie a-try` (chapter 5's evolutions) takes in every other square sail and the jibs and brails up the spanker. "After she has recovered from the first shock of the sea, and has lost her headway, she will, with the helm a-lee, and under a proper arrangement of the sails, lie to, coming up and falling off two or three points, and drifting bodily to leeward" (Luce 1884, ch. XXIX); "in a gale, with a heavy sea, vessels lying to will come up and fall off four or five points" (the same, ch. XXIV). So she does in the game: the frigate in forty-five knots comes up to three points and falls off to the beam every two minutes or so, and drifts to leeward at a knot and a half to two through the water (before package 37p she lay steady head to sea and went astern at four and a half). `heave to`, with the main topsail to the mast, is for a working breeze; given in a gale with no way to take off, it lies her to with the way she has, and the line says she drifts ("Hove to on the starboard tack, main topsail to the mast, helm a-lee; she has three knots of sternway, and drifts.").

**Taken aback** (Luce 1866, ch. XXV, Wind Baffling). A ship that comes to against her helm, or is caught by a shift, has her sails pressed back against the masts and gathers sternway. Going astern her keel grips the water near the stern, and the sails' push to leeward then swings her head off; the helmsman keeping her full and by shifts the helm hard over for the sternway ("the moment she gets sternboard, shift the helm, and she will fall off briskly"), and as the sails fill and she gathers way he brings her by the wind again. If she will not pay off, **box her off**: "Up mainsail and spanker! ... Brace abox the head yards! ... and when the after sails fill, let go and haul as in tacking". The after yards are squared, the head yards laid aback to press her head off; when she has fallen off seven points from the wind on her tack, a point beyond her close-hauled angle, every yard is braced up for it, the mainsail and spanker set again, and she is kept full and by. The helmsman orders it himself when she has been aback two minutes with the helm full and by, or two minutes in irons, her head in the wind and her sails shaking, going astern faster than a knot ("Two minutes in irons, going astern, and she will not pay off: box her off!"):

```orders frigate plain-sail
box her off
box off
```

```
* Forenoon watch (10:12)  Two minutes aback and she will not pay off: box her off!
  Forenoon watch (10:12)  Up mainsail and spanker! Square away the after yards! Brace abox the head yards!
  Forenoon watch (10:13)  Her head falls off.
  Forenoon watch (10:14)  Her after sails take. Let go and haul! Brace up for the starboard tack. Board the main tack and haul aft the sheet! Haul out the spanker!
* Forenoon watch (10:15)  Boxed her off; braced sharp up on the starboard tack, full and by.
```

The captain of chapter 17 does all of this by his doctrine: in a gale with sea room he shortens sail and lies her to, his book's lines take another reef and set the storm staysails as the wind rises again, send down the topgallant masts (`lie a-try` has hauled the courses up in their gear); and when the wind has been under twenty-five knots for half an hour after it, the topgallant masts go up, the reefs come out and plain sail is set ("After the gale abates, sail should not be made upon the vessel too rapidly", Luce 1884, p. 479).

## What a captain of 1805 did not know

He knew the glass falls before a southerly gale, that the wind will back as the gale comes on and veer through west as it passes, and that the glass rises after; and that a slow rise with drying air is fair weather and a rapid one unsettled. He did not know the shape of the thing. Dove's law of the gyration of the wind is 1828; Redfield's rotary storms 1831; Reid's *Law of Storms* 1838; Buys Ballot's rule, that with your back to the wind the low pressure is on your left hand, 1857. Nothing in the game names a front, a centre or an isobar in any line you read, and nothing gives the pressure in any unit but inches, because those are the century after. The rules above can be discovered from the readings the game gives, as they were.

## Where the weather comes from

The shape behind all of these readings, which the game never names in any line you read, is the depression of the kind that crosses the Channel most weeks of the year, and it is worth knowing in general terms. Its centre passes to the north of a ship in the Channel more often than to the south. Ahead of it the glass falls and the wind backs into the south or south-west; the sky thickens from the westward, high cloud first and then a low grey sheet with rain or drizzle, which is the warm front going over. Behind that front the ship is in the warm sector: the wind steady in the south-west or west, the glass still falling but slowly, the air mild and hazy with drizzle, and it may stay so for a day. Then the cold front: the wind veers sharply, three or four points toward the north-west, the glass touches its lowest and turns, and the air behind is cold and unstable, clear between hard-edged showers, with the squalls of the section above; it is here that the wind blows hardest, Luce's "just beginning to rise, directly after having been very low". The gale eases as the glass climbs and a ridge of high pressure follows the low, the sky clearing, the wind falling light and the sea, which was slower to rise than the wind, slower to go down. A low that passes to the south of the ship gives the mirror of it: an easterly backing through north, cold and wet, and no warm sector at all. How long each stage lasts and how hard it blows is the low's own business and differs from one to the next; a scenario's day may hurry it or draw it out, and the log's first line names the scenario, which is all a captain is told.

A scenario file gives its weather in one of two forms, and a captain need know neither (`freesail/world/scenarios.py` has the syntax; the author's view, not the deck's). A pinned `wind` is a list of waypoints the wind follows exactly, its gusts and its wander drawn as in neutral air unless a waypoint says the air is warm or unstable from its moment on; `systems` are a low or a high as a track of positions and central pressures, from which the wind, the glass and the sky at the ship follow, the air being whatever sector the ship is in; or `climatology: true`, and the month's systems are drawn from `data/weather/climatology.yaml`, the first pass of a table that says how often the lows come, where they pass, how deep they are and where the highs sit, checked against the shares of westerly and easterly days that the Royal Navy's logbooks of 1750 to 1854 give for the Channel. When both forms are given the pinned wind wins and the systems give only the sky and the glass. The days the tests are measured on exist in both forms; what they hold, hour by hour, is for the tests and not for the deck.
