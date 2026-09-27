# Milestone 4 work packages: contracts between them

Milestone 4 is specified in `docs/TechnicalSpec-M4.md` in three parts with three gates. Read it whole before your section, then `docs/agents/README.md` (the commitments to models, which are requirements) and the milestone 3 and 3b working rules (`docs/dev/M3-WorkPackages.md`, `M3b-WorkPackages.md`), which hold: stay inside your files, build what the specification says at the size it says, every number names its source, physics before rules, deterministic, ship's-log voice, run the whole suite and read the summary line yourself, report in the set order. Packages are scoped for a senior engineer: leeway in how, and a little beyond the letter where the specification's intent is served, said so in the report.

Two rules added for this milestone:

- **Parity is structural.** Anything a standing order can test, an instrument can show and an agent can ask for, through one registry. Do not add a reading in one place only.
- **Prove the harness with the fake before a model.** No package's tests call a language model. Every commitment to models (`docs/agents/README.md`) has a test against the scripted fake.

## Waves, gates and dependencies

```
gate 4a:  wave 1  25 readings, the standing dialect, the runtime, the book
          wave 2  26 the sun, starter routines, the Python API, the new orders, truths 34 to 40, gate 4a
gate 4b:  wave 3  27 the agent model, tools, harness, fake model, the watcher and ask
          wave 4  28 the MCP server, the local runner, consent, documentation, truths 41 to 47, gate 4b
gate 4c:  wave 5  29 the weather script, compression and roll-up, the day, the playtest form, truths 48 to 51, gate 4c
```

Each gate is cut and passed by the owner before the next wave starts, per the owner's wish to keep the design record level with the work. 27 may start alongside 26 once 25 has landed (it needs the readings registry and nothing else of 26).

## Package 25: readings, the standing dialect, the runtime, the book (`freesail/api/readings.py`, `freesail/standing/` new: `grammar.py`, `rules.py`, `runtime.py`, `book.py`, `freesail/orders/*` for the `standing order` sentence and the book's orders, `data/vocabulary.yaml`, `freesail/core/world.py` for the runtime hook and the actor on firings, `freesail/api/session.py` for attaching the runtime, `tests/test_readings.py`, `tests/test_standing.py`)

Spec §2, §3, §4 (the runtime half).

- The readings registry with every row of §2, the absent ones registered as absent with the sentence the parser says; each reading's words, unit, getter and comparison kind; a per-tick cache. `queries.snapshot` reads its instrument values from the registry (change nothing the client sees, prove it with the existing server tests).
- The grammar of §3 as an extension of `orders/grammar.py`, not a second parser: `standing order "name": ...` is a sentence the existing `handle` recognises and hands to `standing/grammar.py` for the trigger and condition; the orders after `then` are parsed by the existing imperative grammar at *give* time, so a misspelt sail is refused when the standing order is given, not when it fires. Errors in the parser's voice with the offending word named.
- The rule objects (`rules.py`: trigger, condition, actions, given_by, state) that both the dialect and the Python API (package 26) build; the runtime (`runtime.py`) evaluating each tick with durations, dwell (`STANDING_DWELL_S = 300`), edge-triggering, `every` without queueing more than one, the conflict rule by rank, and firing through `World.submit(text, actor="standing order 'x'")` with the log line "By standing order 'x': ...".
- The book: list, show, belay, resume, belay all; `read the standing orders from <file>` as a console and server driver command; the book saved with the game (the orders' text and state) and restored on load; journaled as orders when given.
- Tests: every reading on both ships against the physics' own numbers; the grammar's acceptances and refusals (a table like `test_orders`); dwell, durations and edge-triggering with synthetic readings; the conflict rule with a synthetic officer; determinism of firing; a save and load of the book.

## Package 26: the sun, starter routines, the Python API, the new orders, truths 34 to 40, gate 4a (`freesail/core/sun.py`, `freesail/core/clock.py` and `world.py` for the daylight reading and the two events, `freesail/standing/python_api.py`, `data/standing_orders/starter.orders`, `freesail/orders/verbs.py` and `vocabulary.yaml` for `trim the <sail>`, `tend the sheets`, `bear away`/`come up` if missing, `docs/primer/07-a-first-passage.md` (a section on standing orders; the bowline sentence in `04`), `tests/test_known_truths.py` truths 34 to 40, `docs/dev/TuningNotes.md`, `docs/gates/gate-m4a.md`)

Spec §4 (the Python half), §5, §6, §7, §8, §9. Starts when 25 has landed.

- The sun model with its source named (the NOAA-style declination and hour-angle approximation); `latitude_deg` in the scenario; `daylight` and the `sunrise`/`sunset` events through the registry.
- The Python API exactly as §4 shows, building package 25's rule objects, `trusted` marked, a rule saved as name and source, and the test that a Python rule and its dialect twin give identical logs (truth 40).
- The starter routines file with sources in comments; `--standing-orders` on the console and server.
- The orders of §7, each with a test and a primer sentence.
- Truths 34 to 39 in the existing style; measured values to the tuning notes; `docs/gates/gate-m4a.md` in the form of `gate-m3b.md`, eight items, seed 7, `py` where the owner types Python, the exact final test count.

## Package 27: the agent model, tools, harness, the fake, the watcher and `ask` (`freesail/agents/` new: `agent.py`, `tools.py`, `harness.py`, `fake.py`, `journal.py`; `freesail/core/world.py` for the agent hook and the new log kinds; `freesail/orders/*` for `ask the <station> ...`, `stand down the <station>`, `show the <station>'s journal`; `freesail/api/queries.py` for the agents in the snapshot; `client/log.js` for the `[watcher]` mark inline; `tests/test_agents.py`)

Spec §11, §12, §15. Starts when 25 has landed (the tools read the registry).

- `Station`, `Authority`, `SamplingPolicy` (periodic, on_events, lockstep), `Brief` with the generated five-item head (§11) that no station brief can displace; the tools as pure functions over the World; the harness loop with the opt-out scan on raw output first (`OPT_OUT_TOKEN = "FREESAIL-OPT-OUT"`), then tool calls; welfare stops on game state (`WELFARE_REPEAT_N = 3`, patience per station, a tool-call cap per sample); `stand_by` as a logged decision that suspends sampling; the journal saved with the game; the release of a station on opt-out or stop with the save and the journaled reason.
- The watcher station: authority none, narration as `agent.note` under `[watcher]`, `ask` routed to `answer` and logged as `agent.said`; `stand down the watcher`.
- The scripted fake of §15, and the tests of §16 (truths 41 to 46 as tests here; package 28 writes them into `test_known_truths.py` if the style fits, else they live in `test_agents.py` and the truths table points here).
- In-world text as data: a test that the brief head is the only text the harness ever passes as operator text, whatever the log contains (put a line in the log that reads like an instruction and prove it arrives as data).

## Package 28: the MCP server, the local runner, consent, documentation, gate 4b (`freesail/agents/mcp_server.py`, `freesail/agents/local.py`, `freesail/agents/consent.py`, `docs/agents/ConsentBrief.md` (review the draft the lead wrote; improve it), `docs/agents/Harness.md` new (how to connect Claude Desktop with the exact configuration snippet; how to run `llama-server` with the exact command line; how to point the runner at Ollama), `pyproject.toml` (an `agents` extra: the Python MCP SDK; `httpx` is already in `dev` and moves to `agents`), `tests/test_mcp_server.py`, `tests/test_local_runner.py`, `tests/test_consent.py`, `tests/test_known_truths.py` truths 41 to 47 if not already there, `docs/gates/gate-m4b.md`, `README.md`)

Spec §13, §14, §17. Starts when 27 has landed.

- The MCP server on the Python MCP SDK's `FastMCP` over stdio, exposing package 27's tools and the library as resources, with the same authority checks; a test that lists its tools and calls each through the SDK's in-process client. If the SDK's API has moved from what you remember, read its README from the package you install; do not guess.
- The local runner against an OpenAI-compatible chat-completions endpoint with tool calling, tested against a fake HTTP server (`httpx.MockTransport`), never a live model; it reads the served model's identity from `llama-server`'s `/props` (fall back to the models list), and that string names the consent record.
- The consent step of §14: the brief, the plain conversation with `answer` as the only tool, the record written under `docs/agents/consent/`, the gate on a yes, the stop on anything else. Tested with the fake.
- `docs/agents/Harness.md` for the owner, with `py`: the Claude Desktop configuration JSON, the `llama-server` command line for a GGUF on a 4090 (context, GPU layers, `--jinja` for tool calling, a fixed seed), the runner's flags, and the Ollama note.
- `docs/gates/gate-m4b.md`, nine items per §17.

## Package 29: the weather script, compression and roll-up, the day, the playtest form, truths 48 to 51, gate 4c (`freesail/world/` new: `weather_script.py`; `freesail/core/world.py` and `physics/wind.py` for the script driving the wind; `freesail/core/events.py` or `log` for the roll-up view; `freesail/ui/console.py` and `server.py` for `speed N` to 300 and the roll-up; `client/log.js`; `docs/playtests/README.md`; `tests/test_weather_script.py`, `tests/test_rollup.py`, `tests/test_known_truths.py` truths 48 to 51; `docs/gates/gate-m4c.md`; `README.md`)

Spec §19 to §23. Starts when 26 and 28 have landed.

- The weather script as scenario data, journaled with the seed; linear turns and freshening between waypoints; the gate's day defined as data.
- Compression to 300 with the hourly roll-up as a view over the log store (nothing dropped); notable and urgent lines kept; the client shows the roll-up at the same thresholds.
- The performance test with the stated budget and margin.
- The day saved at several ticks and replayed; load and continue.
- `docs/playtests/README.md`: the form; `docs/gates/gate-m4c.md`: the day's setup and the form as the report.

## Integration (the lead)

The lead reviews each package against the commitments in `docs/agents/README.md`, merges each wave, runs the suite, cuts each gate, records the owner's verdicts, and writes the decisions log entries.
