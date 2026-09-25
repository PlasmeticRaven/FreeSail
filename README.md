# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: milestone 1 built (ship files, sail and hull physics, the Orders language, nominal-duration evolutions). See `docs/TechnicalSpec-M0-M2.md` §11 for the milestone plan and `docs/gates/` for the gate reports.

## Running it

Requires Python 3.11 or newer.

```
pip install -e ".[dev]"
python -m pytest              # the test suite
python -m freesail.ui.console data/ships/frigate-36.yaml --wind 0,15 --heading 293
```

In the console, driver commands (`hold`, `go`, `time 30`, `tick 600`, `state`, `log`, `save file.json`, `replay file.json`, `quit`) control the clock and the session. Anything else is an order to the ship in the Orders language: `set plain sail`, `brace sharp up on the starboard tack`, `reef the topsails, one reef`, `haul the weather main brace`, `steer west by north`, `tack ship`, `wear ship`. Two draft ships are in `data/ships/`: a 36-gun frigate and a topsail schooner. Without a ship file the console runs the milestone 0 point ship (`steer`, `speed`, `stop`).

- `docs/DesignProposal.md`: the current design proposal (v0.2).
- `docs/TechnicalSpec-M0-M2.md`: technical specification for the first three milestones.
- `docs/references/`: public-domain seamanship texts and a chapter map from Luce to game systems.
- `docs/gates/`: the milestone gate process and one gate report per milestone, written for a non-programmer to check live.
- `docs/InitialDesignBrainstorm.txt`: the original brainstorm the proposal responds to.
