# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: milestone 3b built, rig geometry and canvas (brace limits from Fincham's measured angles, the after yards braced sharper than the head yards, bowlines and catharpins with their prices, the adjacent-yard clearance, canvas numbers and condition with wear, the sail room, storm canvas, the ringtail, save-alls and water sail, studding sails that stall and flog through the physics with their booms rigged in, and thirty-three known truths); its gate is pending (`docs/gates/gate-m3b.md`). Milestone 3 (the crew: a mustered ship's company in two watches, every evolution drawing its hands from the watch on deck, all hands called and piped down, fatigue) and milestone 2 (verified reference ships, strain and carrying away, the browser client, the Sailing Master's Primer) were passed at their gates. See `docs/TechnicalSpec-M3b.md` for rig geometry and canvas, `docs/TechnicalSpec-M3.md` for the crew, `docs/TechnicalSpec-M0-M2.md` §11 for the milestone plan and `docs/gates/` for the gate reports.

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
