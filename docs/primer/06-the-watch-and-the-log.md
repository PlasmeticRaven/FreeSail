# 6. The watch and the log

## Watches and bells

The day at sea is kept in **watches** of four hours, except the two **dog watches** of two hours each between four and eight in the evening, "the intent of which is to change the period of the night-watch every twenty-four hours" (Falconer, *Watch*). A **bell** is struck every half hour, counting up from one to eight through the watch; eight bells ends a watch and begins the next. The ship's company is in two watches, starboard and larboard, but the crew is not modelled yet (milestone 3), so for now the watches are only how the clock is told.

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

## The marks

Each line is marked by its severity in the first column:

| Mark | Severity | What it is |
|---|---|---|
| (blank) | routine | orders as given, hands sent to a job, steps of an evolution, small changes of leeway, gusts, bells |
| `*` | notable | an evolution completed (*Set the fore topsail*, *Tacked*), a sail taken aback, a large wind shift |
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
```

*Order:* is the ship accepting what you said, in the words you said it. *Order not carried out* is a refusal, and its sentence always says what was understood and what was not; the refusal is logged and nothing else happens. *Steady on* is the helmsman reporting the course made good. A sail *taken aback* has the wind on its forward side; the ship *Taken aback* has lost her way to it.

Every entry also carries a machine-readable kind (`order.accepted`, `sail.set`, `ship.tacked`, `wind.gust` and so on) and data in SI units, which the browser client and, later, standing orders read (`docs/TechnicalSpec-M0-M2.md` §5).

## The console commands

The console reads a line and decides whether it is for the clock or for the ship. These are for the clock and are never journaled as ship's orders:

| Command | What it does |
|---|---|
| `tick N` | advance N ticks (N seconds of ship's time), then hold |
| `go` | run the clock at the current compression |
| `hold` | stop it |
| `time N` | set the compression to N seconds of ship's time per real second |
| `state` | the one-screen summary of chapter 2 |
| `log N` | the last N entries again (default 20) |
| `save FILE` | write the voyage to a file |
| `replay FILE` | rebuild a voyage from a file and go on from it |
| `help` | this list |
| `quit` | leave |

Anything else goes to the ship. Type `hold` or `go` at the ship's prompt in the browser and she answers "'hold' is a console command, not an order to the ship".

```orders frigate
state
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
Saved to voyage.json at tick 4660.
> replay voyage.json
Replaying voyage.json to tick 4660...
Replayed. Log digest 67a280d7f8549dea. Clock held.
```

## Starting a voyage

```
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

`--wind FROM,KNOTS` sets the true wind (from the north, 15 knots); `--heading` the ship's head in degrees; `--time` the starting compression. She starts with all sail furled, yards square, no way on her, and the first line of the log is the weather.
