# 6. The watch and the log

## Watches and bells

The day at sea is kept in **watches** of four hours, except the two **dog watches** of two hours each between four and eight in the evening, "the intent of which is to change the period of the night-watch every twenty-four hours" (Falconer, *Watch*). A **bell** is struck every half hour, counting up from one to eight through the watch; eight bells ends a watch and begins the next. The ship's company is in two watches, **starboard** and **larboard**, which take the deck in turn; the dog watches make the turn come round differently each day, so that the watch that had the middle watch last night has the first watch tonight.

| Watch | Hours | Bells |
|---|---|---|
| Middle watch | 00:00 to 04:00 | 1 to 8 |
| Morning watch | 04:00 to 08:00 | 1 to 8 |
| Forenoon watch | 08:00 to 12:00 | 1 to 8 |
| Afternoon watch | 12:00 to 16:00 | 1 to 8 |
| First dog watch | 16:00 to 18:00 | 1 to 4 |
| Last dog watch | 18:00 to 20:00 | 4 at 18:00, then 1, 2, 3, and 8 at 20:00 |
| First watch | 20:00 to 24:00 | 1 to 8 |

The log stamps every entry with the watch and the clock, and with the bells when the entry falls on one:

```
  Morning watch, 1 bell (04:30)  1 bell.
  Morning watch (04:31)  Order: reef the topsails, one reef.
```

The game's tick is one second of ship's time, and a voyage begins at eight bells in the morning watch, four in the morning, on the first of June 1805.

## The ship's company and the watch bill

Every hand aboard has a **station**, his part of the ship, and a watch. The **forecastlemen** work the head: the headsails, the anchors, the bowsprit gear; they are the best and oldest seamen. The **fore, main and mizzen topmen** go aloft on their own mast to loose, furl and reef, "the smartest of the young seamen" (Luce). The **afterguard** work the quarterdeck: the main and mizzen braces, the spanker, the sheets aft. The **waisters**, mostly landsmen, haul in the waist: the fore and main sheets and tacks, the pumps. The **marines** stand watch with the seamen and work as afterguard on deck; they never go aloft. The **idlers** (the carpenter's and sailmaker's crews, the cooper, the armourer, cooks, stewards, servants) "stand no night watches": they come up at six in the morning and go below after the last dog watch. The officers are on the quarterdeck; they give the orders and do not haul.

On deck at any moment are the watch whose turn it is, the idlers by day, and everyone when all hands are called. The watch changes itself at eight bells, and the log says so:

```
  Morning watch, 4 bells (06:00)  Idlers up.
  Forenoon watch, 8 bells (08:00)  Eight bells. The larboard watch relieved the deck.
```

A hand at work when his watch is relieved stays until the job is done, then goes below. `state` shows the watch in one line, and **muster** (a console command like `state`, never an order to the ship) reads the whole bill: each station with its hands on deck, below and at work, and how tired they are, in the words *fresh*, *tired* and *worn out*; then the officers by name. The frigate at the start of the voyage:

```
> muster
Mustered the Amazon's company, 264 souls: twelve officers, 182 seamen, 40 marines and 30 idlers.
The starboard watch has the deck, the idlers below: 111 hands on deck.
Forecastlemen, 28 (26 able, 2 ordinary): 14 on deck, 14 below, none at work; fresh.
Fore topmen, 24 (10 able, 14 ordinary): 12 on deck, 12 below, none at work; fresh.
...
Captain Adam Bowen.
Mr. Fredk. Pearce, first lieutenant.
```

Every evolution asks for so many hands of a rating from its stations (setting a topsail wants twelve, topmen first), and the watch on deck is the pool it draws from. With enough, the work goes at its proper pace. Short, it goes slower, and the log says so in a routine line: *Only seven hands to the mizzen topgallant; the rest are setting the foresail, the mainsail and the fore topsail and at other work.* With fewer than half, it waits for hands, and says so once, in a notable line. An order that starts many at once, such as `set plain sail`, says it once for them all: *Setting plain sail: not hands enough for all at once; the watch takes the sails in turn.* Tired hands work slower too.

## All hands and piping down

**All hands!** turns the watch below out of their hammocks. They come up over a minute and a half, a third at once and the rest by the ladders, and the log marks it notable. Tacking, wearing and reefing topsails are all-hands work and call them by themselves. A manoeuvre stops the work in hand: "Ready about!" **belays** what the watch was at while she goes about (*Belayed setting the fore topgallant: all hands about ship.*) and it is taken up again after. Sail work with all hands does not: a reef called while the topgallants are coming in begins with the hands that are free and the watch below as it comes up, and the topgallant men join it when they are done (*Only 108 hands to the fore topsail; the rest are taking in the fore topgallant, ...*), so the reef begins short and speeds up. When the last of the all-hands work is done the hands are **piped down** and the watch below goes below. Called by the captain, all hands stay up until he pipes them down himself. `pipe down` is refused while the hands are still about ship. A call at night costs the watch below their sleep, and the morning watch is slower for it.

```orders frigate
call all hands
turn the hands up
pipe down
pipe down
all hands
pipe the watch below
```

A second call is answered in words and changes nothing (*All hands are called already; the watch below is coming up.*, or once they are up, *All hands are on deck already; they stay up until piped down.*), and a second `pipe down`, with nobody up, *Nobody is turned up; the starboard watch has the deck.* (at the start of a voyage, when the starboard watch has the morning watch).

## Sending a watch or a station

Any order that sets men to work can name the hands for it: the request is then filled from that watch or that station alone. Said Luce's way, `send the ... to ...`; or with the hands after the order, `... with the starboard watch`. A watch that is below is **turned up** for the work, coming up as all hands do (*Turned up the larboard watch.*, at the start of a voyage), and stays up until piped down.

```orders frigate
send the larboard watch aloft to loose the fore topsail
send the fore topmen aloft to furl the fore topsail
set the jib with the forecastlemen
brace the main yard sharp up with the afterguard
set the spanker with the marines
set plain sail with the starboard watch
pipe down
# rejected: send the marines aloft to loose the main topsail
# rejected: tack ship with the larboard watch
# rejected: haul the main brace with the starboard watch
# rejected: send the larboard watch aloft
```

Marines and idlers do not go aloft; the ship's evolutions (tacking, wearing) take all hands and no smaller party; and a level-0 order such as hauling a brace is the officer's own adjustment, with no hands to name. The schooner has no marines and no main top:

```orders schooner
send the fore topmen aloft to loose the fore topsail
set the foresail with the larboard watch
# rejected: set the mainsail with the marines
# rejected: send the main topmen to loose the fore topsail
```

A party too small for the work is refused at once, with the numbers, since waiting would not make it larger: by day, `reef the mainsail, one reef with the idlers` in the schooner is answered *The idlers are four; reefing the mainsail wants ten. Call all hands, or name the watch.* The watch on deck short of hands because some are at other work is another matter: the work waits for them (chapter 3), and they come.

## Relieving the watch

`relieve the watch` changes the watch early: the other watch takes the deck until the clock's next watch change gives it back to the bill. It is for when all hands have upset the turn, or a watch has been kept long at hard work.

```orders frigate
relieve the watch
relieve the watch
change the watch
```

## The marks

Each line is marked by its severity in the first column:

| Mark | Severity | What it is |
|---|---|---|
| (blank) | routine | orders as given, hands sent to a job, steps of an evolution, small changes of leeway, gusts, bells, the watch relieved, idlers up and down, piped down, short-handed |
| `*` | notable | an evolution completed (*Set the fore topsail*, *Tacked*), a sail taken aback, a large wind shift, a spar or rope under dangerous strain, *All hands!*, work waiting for hands or belayed |
| `!` | urgent | anything carried away, missing stays, the ship taken aback and stopped |

The entries you will see most:

```
  Morning watch (04:21)  Order: haul the weather main brace.
  Morning watch (04:58)  Order not carried out ('set the mizzen topsail'): There is no such part as the mizzen topsail in this ship; did you mean the topsails, the mainsail or the gaff topsail? ('set' was understood.)
  Morning watch (04:06)  Hands aloft to loose the foresail.
* Morning watch (04:09)  Set the foresail.
  Morning watch (04:12)  Leeway 4° to larboard.
  Morning watch (04:26)  Steady on ENE (68°).
  Morning watch (04:47)  A gust: 17 knots.
* Morning watch (04:21)  Main course taken aback.
  Morning watch (04:22)  Main course filled again.
! Morning watch (05:09)  Taken aback: the sails pressed against the masts and she lost her way.
* Morning watch (04:52)  Main topmast bending like a whip; she will carry it away if sail is not shortened.
```

*Order:* is the ship accepting what you said, in the words you said it. *Order not carried out* is a refusal, and its sentence always says what was understood and what was not; the refusal is logged and nothing else happens. *Steady on* is the helmsman reporting the course made good. A sail *taken aback* has the wind on its forward side; the ship *Taken aback* has lost her way to it. A spar *working* or *bending like a whip* is loaded past its rating and may carry away if you do not shorten sail (package 9): in this book's breeze that line comes only in a gust with everything set.

Every entry also carries a machine-readable kind (`order.accepted`, `sail.set`, `ship.tacked`, `wind.gust` and so on) and data in SI units, which the browser client and, later, standing orders read (`docs/TechnicalSpec-M0-M2.md` §5).

## The console commands

The console reads a line and decides whether it is for the clock or for the ship. These are for the clock and are never journaled as ship's orders:

| Command | What it does |
|---|---|
| `tick N` | advance N ticks (N seconds of ship's time), then hold |
| `go` | run the clock at the current compression |
| `hold` | stop it |
| `time N` | set the compression to N seconds of ship's time per real second |
| `state` | the one-screen summary of chapter 2, with the watch on deck and the hands at work |
| `muster` | the watch bill, station by station (also `muster the crew`) |
| `log N` | the last N entries again (default 20) |
| `save FILE` | write the voyage to a file |
| `replay FILE` | rebuild a voyage from a file and go on from it |
| `help` | this list |
| `quit` | leave |

Anything else goes to the ship. Type `hold` or `go` at the ship's prompt in the browser and she answers "'hold' is a console command, not an order to the ship".

```orders frigate
state
muster
set the fore topsail
tick 300
state
log 5
```

This book uses `tick` throughout so that its logs are exact. At the console `go` with `time 30` is the natural way to sail a passage; above ten times compression, routine entries are rolled up into a count at each bell:

```
  (27 routine entries)
  Morning watch, 2 bells (05:00)  2 bells.
```

## Seeds, saving and replaying

Nothing in the game is random except through a seeded stream: the same seed, the same orders at the same ticks, the same log to the last word. `--seed 7` on the command line gives this book's voyages; leave it off and the seed is 1805. The wind's wandering and gusts come from the seed, and later so will everything else that chance decides.

`save voyage.json` writes the seed, the scenario and the **journal**: every accepted order with the tick it was given at. `replay voyage.json` rebuilds the ship and runs the journal through to the same tick; the state it prints must match, number for number, the state before the save. That is the whole of the save file, and it is why *weather* and *lee* are journaled already resolved to a side: a replay must not have to guess which tack she was on.

```
> save voyage.json
Saved to voyage.json at tick 4380.
> replay voyage.json
Replaying voyage.json to tick 4380...
Replayed. Log digest 07d5978d56b0eb4c. Clock held.
```

## Starting a voyage

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

`--wind FROM,KNOTS` sets the true wind (from the north, 15 knots); `--heading` the ship's head in degrees; `--time` the starting compression. She starts with all sail furled, yards square, no way on her, and the first line of the log is the weather.
