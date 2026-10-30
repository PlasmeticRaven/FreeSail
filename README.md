# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: gate m6c passed (`docs/gates/gate-m6c.md`); milestone 7 is in build, its interim gate drafted in `docs/gates/gate-m7-interim.md`; the gate process and every gate's report are in `docs/gates/`.

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
