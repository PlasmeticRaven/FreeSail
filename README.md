# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: milestone 4a built, standing orders (a readings registry that a rule tests, an instrument shows and an agent will ask for; the standing dialect, `standing order "night routine": at sunset then take in the studdingsails; take in the royals`, with durations, the dwell, the conflict rule by rank and the book; the sun with sunrise, sunset and twilight at the scenario's latitude; seven starter routines in `data/standing_orders/starter.orders`; a thin Python API that builds the same rules; `trim the <sail>` and `tend the sheets`; and forty known truths); its gate was passed (`docs/gates/gate-m4a.md`). Milestone 3b (rig geometry and canvas), milestone 3 (the crew) and milestone 2 (verified reference ships, strain and carrying away, the browser client, the Sailing Master's Primer) were passed at their gates. See `docs/TechnicalSpec-M4.md` for standing orders, the harness and the ship sailing herself, `docs/TechnicalSpec-M3b.md` for rig geometry and canvas, `docs/TechnicalSpec-M3.md` for the crew, `docs/TechnicalSpec-M0-M2.md` §11 for the milestone plan and `docs/gates/` for the gate reports.

## Running it

Requires Python 3.11 or newer.

```
python -m pip install -e ".[dev]"
python -m pytest              # the test suite
python -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
python -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
python -m pip install -e ".[dev,server]"     # once, for the browser client
python -m freesail.ui.server data/ships/frigate-36.yaml --wind 0,15 --heading 293
```

The server prints an address (normally `http://localhost:8000`); open it in a browser for the log, instruments, ship view and map. The command line at the foot of the log takes the same orders and driver commands as the console. Add `?facing=45` to the address, or press `]` and `[`, to look at the ship from another bearing.

In the console, driver commands (`hold`, `go`, `time 30`, `tick 600`, `state`, `muster`, `log`, `save file.json`, `replay file.json`, `quit`) control the clock and the session. Anything else is an order to the ship in the Orders language: `set plain sail`, `brace sharp up on the starboard tack`, `reef the topsails, one reef`, `haul the weather main brace`, `steer west by north`, `tack ship`, `wear ship`, `call all hands`, `pipe down`, `send the larboard watch aloft to furl the main course`. Two draft ships are in `data/ships/`: a 36-gun frigate and a topsail schooner. Without a ship file the console runs the milestone 0 point ship (`steer`, `speed`, `stop`).

- `docs/DesignProposal.md`: the current design proposal (v0.2).
- `docs/TechnicalSpec-M0-M2.md`: technical specification for the first three milestones.
- `docs/TechnicalSpec-M3.md`: technical specification for milestone 3, the crew.
- `docs/TechnicalSpec-M3b.md`: technical specification for milestone 3b, rig geometry and canvas.
- `docs/primer/`: the Sailing Master's Primer, the period words and orders in eight short chapters.
- `docs/references/`: public-domain seamanship texts and a chapter map from Luce to game systems.
- `docs/gates/`: the milestone gate process and one gate report per milestone, written for a non-programmer to check live.
- `docs/InitialDesignBrainstorm.txt`: the original brainstorm the proposal responds to.
