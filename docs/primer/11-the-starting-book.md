# 11. The starting book

A captain's standing orders are his own. They say what the officer of the watch is to do without asking: take in the light sails at sunset, shorten sail when it blows, call him when the glass falls. The game keeps them in a **book** (chapter 7 shows the book at work), and comes with one ready written, the **starter book**, `data/standing_orders/starter.orders`. It is a choice and never a requirement: a game begins with an empty book unless its scenario names the starter (the gates' days and passages do) or you ask for it, and the console and the browser say so in their opening words. Load it whole at the prompt, or at the start:

```
read the standing orders from data/standing_orders/starter.orders
python -m freesail.ui.console data/ships/frigate-36.yaml --standing-orders data/standing_orders/starter.orders
python -m freesail.ui.server data/ships/frigate-36.yaml --standing-orders data/standing_orders/starter.orders
```

Or begin with none, and give the ones you want one at a time, or write your own. This chapter prints each of the starter's routines with the reason it exists, so that you can judge which suit your ship and your passage, and then the dialect whole, so that you can write the rest. A passage's own orders (the noon cast, the lead going in, lying off at the end) are not in the starter: they belong to the passage, and the gates keep theirs in their scenario's file (`data/scenarios/gate-5b-passage.orders` is a passage's book, worth reading for its reasons too).

## The routines, and why each

**The night routine.** The light sails come in for the dark hours. Luce's routine of the day has the topgallant yards sent down at sunset, and before a squall "furl the topgallant sails and royals, and stow the light sails"; at sea, with the yards kept across, the game's version takes in the studding sails and the royals, the light sails a watch cannot see to handle in the dark.

```orders frigate all-sail
standing order "night routine": at sunset then take in the studdingsails; take in the royals
```

**The morning sail.** The reverse at daylight, if the breeze allows: under twenty knots every sail is carried without a strain line (the strain tables and truth 9); over it the royals stay in.

```orders frigate
standing order "morning sail": at sunrise, if the true wind is under 20 knots then set the royals
```

**Shortening sail for weather.** Thirty knots is where the strain truths begin to bite: in thirty-five the royals and topgallants carry away within twenty minutes under all sail. Two minutes lets a gust pass. The order of shortening is Luce's as it freshens: the royals, the topgallants, then the reefs.

```orders frigate all-sail
standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; take in the topgallants; reef the topsails, one reef
```

**Keeping her full.** On a wind the frigate carries the apparent wind at 48 to 52 degrees; forward of 55 she is pinching, and a point off brings her back to a good full. (It is refused while she is hove to: a course is given her by filling away.)

```orders frigate
standing order "keep her full": when the apparent wind is forward of 55 degrees then bear away one point
```

**Trimming on a shift.** The yards are trimmed to the wind as it shifts, a point at a time, as Luce's table of the yard's best angle is given point by point. It is measured afresh from each firing, so a wind veering steadily through a night has the yards trimmed to it point by point. Not while she is hove to: her yards are then set against each other on purpose, and in two playtests this rule braced a hove-to ship's backed yard round and filled her. The guard is the dialect's own, `and the manoeuvre in hand is not hove to`; with it the rule sleeps while she lies to and wakes when she has filled away. (`trim sails` given by hand to a ship hove to is refused in words; chapter 5.) Put the same guard on any trimming rule of your own.

```orders frigate
standing order "trim on a shift": when the true wind veers 1 point or backs 1 point and the manoeuvre in hand is not hove to then trim sails
```

**Tending the sheets.** The sheet holds the trim (chapter 4): a jib's or a spanker's sheet stays where it was worked until hands work it again, so the afterguard's routine is to tend the fore-and-aft sheets every glass, and a sheet within a degree of its trim stands. It has the same guard: hove to, the watch tends the spanker and jib sheets to keep her head where it lies, and not to the wind.

```orders frigate
standing order "tend the sheets": every glass, if the manoeuvre in hand is not hove to then trim the sheets
```

**Shortening sail, and the head sails.** The book's thirty knots gives `shorten sail`, and since package 37p `shorten sail` does more than its list as the wind rises (chapter 9): a jib loaded near its rating comes in before a gust blows it out, the courses are reefed with the second reef and the mainsail and the spanker taken in with the third, and the storm staysails go up over forty knots or when the fore topmast staysail is loaded near its rating. In the captain's trials, before it did, the frigate's jib and fore topmast staysail blew out of their bolt-ropes and she lay aback for an hour with nothing set forward.

**Heavy weather, and the storm staysails.** Forty knots is a gale; five minutes tells a gale from a squall. The close reef leads, because the hands go to the first clause first and the topsails must be reefed before the weather comes; the topgallant masts come down next; and `set the storm staysails` bends them from the sail room, sets each as soon as it is bent, and takes in the head sails and the spanker it replaces once it is set, so that she is never left with nothing forward. Lying to is not the book's: whether she has the sea room to lie to is the captain's judgement (`lie a-try`, chapter 9).

```orders frigate
standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then close reef the topsails; send down the topgallant masts; set the storm staysails
```

**The well.** Sounding the well every glass is the pump routine of Luce's day. The ship has no well yet, so the order is entered in the book and held, the line that enters it saying why, and it never fires until the well is a reading; it is kept so that the book is complete when the well arrives.

```orders frigate
standing order "sound the well": every glass then sound the well
standing orders
```

## Writing your own

A standing order is one sentence:

```
standing order "<name>" [by the <officer>]: <trigger> [, if <condition>] then <order> [; <order> ...]
```

The **name** is in quotes, and the book finds it again by it, without regard to capitals and by any part of it that names one order and no other: `belay standing order "trim by the wind"` belays "Trim Sails by the Wind". The book's own orders may drop the words *standing order* when the name is in quotes: `belay "blind lead"`, `resume "trim by the wind"`, `show "night routine"`.

The **trigger** is when it fires. `when <condition>` fires as the condition comes to hold, and not again until it has been false for five minutes and the work it began has ended; `for 2 minutes` after it means the condition must hold that long first. `at <event>` fires at each event. `every <interval>` fires on the interval, a glass, an hour, a watch or so many minutes.

The **condition** is one or more readings compared, joined by `and`. The readings are the ship's (`state` and the browser's instruments show them; chapter 9 and chapter 10 describe the weather's and the reckoning's), with or without their article: the true wind, the mean wind, the apparent wind, the heading, the course, the speed, the leeway, the heel, the helm, the watch, the time, daylight, a sail or a part by its name, the strain, the hands on deck, the watch below, the glass, the sky, the weather, the visibility, the sea, the motion, what is in sight, the land, the depth, the ground, the reckoning and its uncertainty, the distance run since noon, the master, and the manoeuvre in hand (`she is hove to`). A condition after `, if` is tested when the trigger fires; when it fails, the log says so the first time and then once a watch, not at every firing.

The **orders** after `then` are plain orders to the ship, as you would type them, separated by `;`, and given in that order: the hands go to the first first. They are read when you give the standing order, so a misspelt sail is refused then and not on the night it fires.

```orders frigate
standing order "glass": when the glass is falling fast then shorten sail
standing order "squall": at a squall then take in the royals
standing order "lead going": every 10 minutes, if the land is in sight and the depth is under 20 fathoms then heave the lead
standing order "trim when full": when the true wind veers 1 point or backs 1 point, if she is not hove to then trim sails
standing order "night sails": when the daylight is night then take in the royals
standing order "royals" by the master: at eight bells then set the royals
belay "night sails"
resume standing order "NIGHT SAILS"
show "trim when full"
strike standing order "glass"
# rejected: standing order "no colon" every glass then trim sails
# rejected: standing order "x": when the wind is shaking then trim sails
```

Two orders that lay hands on the same part within five minutes, while the first one's work is still in hand, are settled by rank, the captain's standing over the master's, and two of the captain's own give the later the day with a plain note. A sail, a yard or a line is its own part; the helm is one; a manoeuvre (tacking, wearing, heaving to, filling away) is the helm's and the yards'; the lead is the leadsman's, the log the log's, a bearing and the account the master's; so `heave the lead` while she heaves to is no contrary order.

## The dialect's forms, in a table

Every form of a trigger, a condition and the book's orders; the test (`tests/test_primer.py`) gives each in the table's first column to the frigate as a standing order, and fails if one is not taken.

| Form | What it waits for, or does |
|---|---|
| `when the true wind exceeds 30 knots`, `when the true wind is under 12 knots`, `when the mean wind exceeds 25 knots`, `when the true wind exceeds thirty knots`, `when the true wind is 12 knots`, `when the speed is five knots` | the wind's speed, gusts in it or its ten minutes' mean; a number in words as in figures; *is 12 knots* holds within half a knot of it, so that it fires as the wind comes to twelve from above or below |
| `when the true wind veers 1 point`, `when the true wind backs 2 points`, `when the true wind shifts 1 point`, `when the true wind veers 1 point or backs 1 point`, `when the true wind is from the north-west` | the wind's direction, from where it stood when the order last fired |
| `when the true wind is a gust`, `when the true wind is a lull` | the wind against its mean |
| `when the apparent wind is forward of 55 degrees`, `when the apparent wind is abaft the beam`, `when the apparent wind is on the starboard bow` | the apparent wind on the bow |
| `when the heading is east of south-west`, `when the course is north`, `when the speed is under 3 knots`, `when the heel exceeds 15 degrees`, `when the leeway exceeds 10 degrees` | the ship's own motion |
| `when the watch is the middle watch`, `when the time is eight bells`, `when daylight is night`, `when the daylight is not day` | the clock and the sun |
| `when the fore royal is shaking`, `when the main topsail is aback`, `when the royals are set`, `when the fore storm staysail is furled`, `when the main topmast is straining`, `when the strain exceeds the rating` | a sail by name, a part by name, the worst strain aboard |
| `when the hands on deck are tired`, `when the hands on deck are under 40 hands` | the watch on deck |
| `when the glass is under 29.5 inches`, `when the glass is falling fast`, `when the glass is turning`, `when the sky is threatening`, `when the weather is squally`, `when the visibility is a mile`, `when the sea is heavy`, `when the sea gets up`, `when the motion is labouring heavily` | the weather (chapter 9) |
| `when the land is in sight`, `when the depth is under 20 fathoms`, `when the ground is not rock`, `when the reckoning's uncertainty exceeds 20 miles`, `when the distance run since noon exceeds 30 miles`, `when the master is below` | the chart and the reckoning (chapter 10) |
| `when she is hove to`, `when she is not hove to`, `when the manoeuvre in hand is tacking`, `when the manoeuvre in hand is none` | what she is about |
| `when the true wind exceeds 30 knots for 2 minutes`, `when the sea is heavy for half an hour` | a condition held for a time |
| `at sunset`, `at sunrise`, `at eight bells`, `at the change of the watch`, `at a squall`, `at a wind shift`, `at the glass falling fast`, `at a strain warning`, `at a sail blown out`, `at noon`, `at a sounding`, `at a landfall`, `at hove to`, `at filled away`, `at tacked`, `at wore` | an event |
| `every glass`, `every hour`, `every watch`, `every 10 minutes`, `every half an hour` | an interval |
| `every glass, if the land is in sight`, `at sunrise, if the true wind is under 20 knots`, `at noon, if she is not hove to` | a condition tested at the firing |

The orders after `then` are read whole when the standing order is given, every one of them by the reader that carries it out: a sail named ambiguously, a mark or a place the chart has not got, the marks of a fix that are none, an anchor she does not carry, a number that cannot be read, each refused then with the order named (package 37l).

The book's orders: `standing orders` lists the book, each order with who gave it and its state (standing, belayed, held, fired how often and when last); `show standing order "x"`; `belay standing order "x"` keeps it idle in the book; `resume standing order "x"`; `belay all standing orders`; `strike standing order "x"` (or `cancel`, `remove`) takes it out; and `read the standing orders from <file>` gives every order in a file of them.

## Sources

The starter's reasons are its file's comments, with their sources in full (`data/standing_orders/starter.orders`): Luce 1866, ch. XXIV and XXXII; Luce 1884, ch. XXV, XXVII and XXIX; the strain truths and the tuning notes for the thresholds.
