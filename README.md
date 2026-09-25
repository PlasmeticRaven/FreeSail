# FreeSail

A ticked, text-first sailing simulation of a late-age-of-sail ship, controlled through layered orders (from hauling a single line to standing orders and scripts), with language models able to watch, crew, or captain through the same channel a human uses.

Status: milestone 0 (skeleton and log) built. See `docs/TechnicalSpec-M0-M2.md` §11 for the milestone plan.

## Running it

Requires Python 3.11 or newer.

```
pip install -e ".[dev]"
python -m pytest              # the test suite
python -m freesail.ui.console # the console; type 'help', then 'go'
```

In the console, driver commands (`hold`, `go`, `time 30`, `tick 600`, `state`, `log`, `save file.json`, `replay file.json`, `quit`) control the clock and the session. Anything else is an order to the ship. In milestone 0 the ship is a point that understands `steer <compass point or degrees>`, `speed <knots>` and `stop`.

- `docs/DesignProposal.md`: the current design proposal (v0.2).
- `docs/TechnicalSpec-M0-M2.md`: technical specification for the first three milestones.
- `docs/references/`: public-domain seamanship texts and a chapter map from Luce to game systems.
- `docs/InitialDesignBrainstorm.txt`: the original brainstorm the proposal responds to.
