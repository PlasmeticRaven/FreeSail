# 9. The glass and the sky

Since milestone 5 the wind has a cause. Somewhere beyond the horizon a low is passing or a high is sitting, and what the ship feels of it comes through three things a captain of 1805 could read: the barometer in his cabin, the sky over his masthead, and the wind itself. This chapter says what the game gives you of each, in what words, and what a seaman of the period made of them. It does not tell you where the low is. The game keeps the truth and you keep your account, as he did.

## The glass

If the ship carries a barometer (the scenario file says, `glass: true` under `ship:`; the frigate of the gate's day has her captain's own, and a small vessel may well have none), `the glass` is a reading: the height of the mercury in inches, to the hundredth, as the vernier of a marine barometer reads it.

```
the glass is 29.72 inches
```

A marine glass of the period is Nairne's pattern of about 1773, a stick barometer with its bore pinched to stop the mercury pumping with the ship's motion, hung in gimbals in the cabin; Cook carried one, and by 1805 an officer who wanted one bought it himself, since the Admiralty did not yet issue them. The reading you get carries the ship's own noise, half a hundredth either way; the seaway's pumping comes with the next package.

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

## What a captain of 1805 did not know

He knew the glass falls before a southerly gale, that the wind will back as the gale comes on and veer through west as it passes, and that the glass rises after; and that a slow rise with drying air is fair weather and a rapid one unsettled. He did not know the shape of the thing. Dove's law of the gyration of the wind is 1828; Redfield's rotary storms 1831; Reid's *Law of Storms* 1838; Buys Ballot's rule, that with your back to the wind the low pressure is on your left hand, 1857. Nothing in the game names a front, a centre or an isobar in any line you read, and nothing gives the pressure in any unit but inches, because those are the century after. The rules above can be discovered from the readings the game gives, as they were.

## Where the weather comes from

A scenario file gives its weather in two forms, and a captain need know neither (`freesail/world/scenarios.py` has the syntax; the author's view, not the deck's). The pinned `wind` waypoints of milestone 4 set the wind directly and are what every truth is measured on. The `systems` are the milestone 5 form: a low or a high as a track of positions and central pressures, from which the wind, the glass and the sky at the ship follow; or `climatology: true`, and the month's systems are drawn from `data/weather/climatology.yaml`, the first pass of a table that says how often the lows come, where they pass, how deep they are and where the highs sit, checked against the shares of westerly and easterly days that the Royal Navy's logbooks of 1750 to 1854 give for the Channel. When both forms are given the pinned wind wins and the systems give only the sky and the glass. The gate's day of milestone 4 (`data/scenarios/gate-4c-day.yaml`) now carries both: a low passing well north of Falmouth with the ship in its warm sector, the cold front through at ten in the evening, the gale in the cold air behind it and the ridge by dawn, the glass falling slowly all day and rising fast in the gale.
