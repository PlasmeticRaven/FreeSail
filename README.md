# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: the last gate passed is m5c, on 8 October 2026 (`docs/gates/gate-m5c.md`). Milestone 6's gates were not passed: m6a stands open, m6a-2 was not cut, and m6c was run in part (`docs/gates/gate-m6c.md`), its untested items deferred to a gate that was not run. Milestone 7's interim gate is a draft and has not been run (`docs/gates/gate-m7-interim.md`). A cold review of the whole was made on 14 November 2026 (`docs/reviews/ColdReview-M7.md`); new work is held while what it found unsafe or untrue is mended. The gate process and every gate's report are in `docs/gates/`.

## Running it

Requires Python 3.11 or newer.

```
py -m pip install -e ".[dev,server,agents]"     # once (python3 in place of py off Windows)
py -m freesail                                  # the harbour: start a game in the browser
```

`py -m freesail` starts the game's server and opens **the harbour** in the browser (package 59; `docs/agents/Harness.md` §22): a game started from a page with the server's flags as its controls (a scenario, the seat, the compression, the pace, a director's brief), the stations held and the doors up, the desktop client's entries written one per station, the API door and the local runner started with their panes, the scenario maker (a scenario read into a form and written back in the file's own form, unchanged where nothing changed) and your settings (`%APPDATA%\FreeSail\settings.yaml` on Windows; no key is ever in it). The clock is held at the start until you say `go`. The commands below are the same game by hand:

```
python -m pip install -e ".[dev]"
python -m pytest -n auto      # the fast tier of the tests; add --slow for the whole suite (docs/gates/README.md)
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
python -m freesail.ui.console data/ships/cutter.yaml --seed 7 --wind 0,15 --heading 300
python -m freesail.ui.console data/ships/brig.yaml --seed 7 --wind 0,15 --heading 295
python -m pip install -e ".[dev,server]"     # once, for the browser client
python -m freesail.ui.server data/ships/frigate-36.yaml --wind 0,15 --heading 293
python -m freesail.ui.server --scenario data/scenarios/gate-5b-passage.yaml --watcher fake --ease-on-station
```

The server prints an address (normally `http://localhost:8000`); open it in a browser for the log, instruments, ship view and map. The command line at the foot of the log takes the same orders and driver commands as the console, and offers the console's completions under the line as you type (Tab takes the first, the arrows move through them, Escape puts them away). `library` at the command line, or the *library* button, opens the reference library beside the log (the primer by chapter and section, the catalogue of evolutions, the grammar, the ship's names, the book and the model's tools, the same pages a model reads with `library`, with a find box) and the ship's papers (`the booms`, `the sail room`, `the boatswain's store`); *pop out* puts it in a window of its own; `library primer 3`, `library find goose-wing` and `library papers` open it there. The wheel zooms the map and a drag pans it; *centre* follows the ship again and *fit* goes back to the whole track. `--ease-on-station`, or the option under the clock in the instruments, eases the clock to 1x whenever a station is sampled or speaks, as an urgent line does, and the log says so. Add `?facing=45` to the address, or press `]` and `[`, to look at the ship from another bearing.

**The game answers its own page alone** (package 115). While the server runs, no other web page open in the same browser can watch the game, give it an order or reach a file through it: the server writes a mark into its own pages as it serves them, and refuses any socket or order that does not carry it, that comes from another site, or that names an address that is not the game's. Nothing is asked of you on the machine the game runs on. The agents' doors come in as before, by the key each is given when it is seated. **Playing from another device** (a tablet beside the chart table): start the server with `--host 0.0.0.0` (or `server: host` in the settings), and the terminal prints a second address, `From another device, open http://NAME:8000/...?page=...`; open exactly that address on the other device, once (the page keeps the mark for its later loads; the harbour's own link is `/harbour?page=...`). Whoever has that address can play the game and start one from the harbour, so give it only to a device of your own, on a network you trust; the mark is new each time the server starts. The harbour's settings, the desktop client's file, the shortcut and the doors are changed only at the machine the game runs on, never from another device. A model's door run on another machine is refused unless its requests carry that same mark; the doors as the game ships them carry none, so run them on the machine the game runs on.

**Saves and books in the browser** (package 115). At the browser's order line, `save NAME` writes `NAME.json` (and its checkpoint) in the saves place (`--saves`; under `py -m freesail` without it, the settings' saves place, `saves` beside your settings file; under `python -m freesail.ui.server` without it, `saves/` in the game's folder; the reply says where it went), and a path anywhere else is refused: to keep a copy elsewhere, copy the file from the saves place. `read the standing orders from` takes a book by its name (`starter`) or by a path in the game's `data/` folder, your scenarios place or the saves place (the primer's `data/standing_orders/starter.orders` as ever). The harbour takes up a save (a `.json` file) from the saves place, or one lying directly in the game's folder or its `saves/`; one kept elsewhere still loads with `py -m freesail --load PATH`, or once moved into the saves place. The console, and every flag on the command line, take any path as before.

In the console, driver commands (`hold`, `go`, `time 30`, `tick 600`, `state`, `muster`, `log`, `save file.json`, `replay file.json`, `quit`) control the clock and the session. Anything else is an order to the ship in the Orders language: `set plain sail`, `brace sharp up on the starboard tack`, `reef the topsails, one reef`, `haul the weather main brace`, `steer west by north`, `tack ship`, `wear ship`, `call all hands`, `pipe down`, `send the larboard watch aloft to furl the main course`. Four reference ships are in `data/ships/`: a 36-gun frigate, a topsail schooner, a cutter with a running bowsprit and a brig, all written by `tools/gen_ships.py` from the period's rules. Without a ship file the console runs the milestone 0 point ship (`steer`, `speed`, `stop`).

- `docs/DesignProposal.md`: the current design proposal, with its decisions.
- `docs/TechnicalSpec-M0-M2.md` to `docs/TechnicalSpec-M7b.md`: the technical specifications by milestone (M0 to M2, 3, 3b, 4, 5, 6, 7 and 7b), each with its "as built" pointers into the code.
- `docs/design/`: the design studies and proposals (the one world, the signals, the squadrons, water and health, the weather systems, the charts, the tides of 1805, the vessels).
- `docs/dev/`: the work packages by milestone, the tuning notes (why every number is what it is, read beside `tests/test_known_truths.py`), the chart blocks, the primer's redactions record.
- `docs/agents/`: how a language model is connected to a station (`Harness.md`), and the consent brief.
- `docs/primer/`: the Sailing Master's Primer, the period words and orders in twenty-five chapters, which is also the library a model at a station reads.
- `docs/references/`: public-domain seamanship texts and a chapter map from Luce to game systems.
- `docs/gates/`: the milestone gate process and one gate report per milestone, written for a non-programmer to check live.
- `docs/InitialDesignBrainstorm.txt`: the original brainstorm the proposal responds to.
