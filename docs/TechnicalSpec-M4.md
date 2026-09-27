# FreeSail: Technical Specification, Milestone 4 (Standing orders, the harness, the ship sails herself)

Companion to `docs/TechnicalSpec-M0-M2.md`, `-M3.md` and `-M3b.md`, whose conventions hold. Milestone 4 is three short gates:

- **4a. Standing orders:** the standing dialect of Orders, the readings it tests, the starter routines, and a thin Python API that compiles to the same rules.
- **4b. The harness and the watcher:** one agent interface with two front doors (an MCP server for Claude Desktop, a local runner for llama.cpp), the fixed brief head, the opt-out token, welfare stops, the journal, the consent step, and the watcher as the first station.
- **4c. The ship sails herself:** a day's passage under standing orders with a scripted weather timeline, time compression with log roll-up, a day saved and replayed, and the owner's first playtest.

Owner's decisions that shape this chapter (2026-09-27):

- A thin Python decorator API now, as long as it is a baseline and not debt (§4 says why it is).
- Local models through **llama.cpp's server**; Ollama remains the owner's chat tool and works as a fallback through the same endpoint shape (§7.3). **Claude Desktop over MCP** is the non-local route.
- The watcher's voice **inline in the log** under its own mark.
- The opt-out token is **`FREESAIL-OPT-OUT`**, pending testing.
- Sampling defaults: the watcher every glass and on notable events; lockstep when asked; tuned through testing.
- The `ask` order exists in 4b: the watcher answers questions and gives no orders.
- A scripted weather timeline stands in for the world in 4c.

The commitments in `docs/agents/README.md` and decisions 16 to 18 of the proposal are requirements here, not aspirations.

---

## Part 4a: Standing orders

### 1. What 4a proves

"The ship keeps herself by rules the captain wrote, in the captain's words, and nothing happens that the log does not explain." A standing order is an order like any other: given at the prompt, journaled, replayed, listed, belayed. When it fires, the log says which order fired and what it did.

### 2. Readings (`freesail/api/readings.py`)

A registry of the things a rule may test, an instrument may show, and an agent may ask for. One registry for all three is how parity begins. Each reading has an id, the words the grammar accepts, a unit, a getter over the World, and a comparison kind:

| Reading (words) | Kind | Notes |
|---|---|---|
| `the true wind` | speed in knots; direction as points and degrees | `exceeds 30 knots`, `backs two points`, `is from the north-west` |
| `the apparent wind` | angle on the bow, side; speed | `is forward of 55 degrees`, `is abaft the beam` |
| `the heading`, `the course` | compass | `is east of ...` (rare; mostly for `at`) |
| `the speed`, `the leeway`, `the heel`, `the helm` | number with unit | `exceeds 15 degrees` |
| `the watch`, `the time` | watch name; bells | `is the middle watch` |
| `daylight` | day, twilight, night | from the sun model (§5) |
| `the <sail>` | state | `is shaking`, `is aback`, `is set`, `is furled`, `is blown out` |
| `the strain` | worst ratio aboard, and per part | `exceeds the rating`, `the fore royal yard is straining` |
| `the hands on deck`, `the watch below` | count; fatigue in words | `are worn out` |
| `the well`, `the glass`, `the depth`, `a sail in sight` | absent until milestone 5 | registered as absent so the grammar can name them and the parser can say "the ship has no glass yet" |

Events, for `at`: `sunset`, `sunrise`, `eight bells`, `the change of the watch`, `a strain warning`, `a sail shaking`, `a spar carrying away`, `a sail blown out`, `all hands called`, `the watch piped down`; and later `a sighting`, `a sounding`.

Intervals, for `every`: `a bell` (half an hour), `a glass` (half an hour, the period word), `an hour`, `a watch`, `N minutes`.

### 3. The standing dialect (`freesail/standing/`)

```
standing order "<name>": <trigger> [, if <condition>] then <order> [; <order> ...]

trigger   := when <condition> [for <duration>]
           | at <event>
           | every <interval>
condition := <reading> <comparison> [and <reading> <comparison> ...]     # conjunctions only
comparison:= exceeds <n> <unit> | is over ... | is under ... | is below ...
           | is forward of <n> degrees | is abaft <n> degrees | is abaft the beam | is forward of the beam
           | backs <n> points | veers <n> points | is from <point> | is <state> | is not <state>
           | are <fatigue word> | is the <watch>
duration  := <n> minutes | a glass | ...
```

Examples, which are also the starter routines' text:

```
standing order "night routine": at sunset then take in the studdingsails; take in the royals
standing order "morning sail": at sunrise, if the true wind is under 20 knots then set the royals
standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef
standing order "keep her full": when the apparent wind is forward of 55 degrees then bear away one point
standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then send down the topgallant masts; shift the fore topmast staysail for the fore storm staysail; close reef the topsails
standing order "sound the well": every glass then sound the well        # refused until milestone 5: "the ship has no well to sound yet"
```

The **book**: `standing orders` (list, with each order's state: standing, belayed, fired N times, last at), `show standing order "x"`, `belay standing order "x"`, `resume standing order "x"`, `belay all standing orders`, `read the standing orders from <file>` (a driver command in the console and the server, not an order, since it reads the disk).

**Authority.** Every standing order carries who gave it (`by the captain` by default; `standing order "x" by the master: ...` for an officer's, which milestone 6's LLM officers will write). Rank orders precedence: when two standing orders would fire conflicting orders on the same part within the dwell, the senior's stands and the log says "Standing order 'x' (the master) countermanded by 'y' (the captain)." In 4a the captain writes them all; the field and the rule are tested with a synthetic officer.

**Two guards against thrashing.** Durations debounce: `for 2 minutes` means the condition has held for two minutes of ship's time. A `when` order is edge-triggered with a dwell: having fired, it does not fire again until its condition has been false for `STANDING_DWELL_S = 300` seconds and any evolution it started has ended. An `at` order fires once per event. An `every` order fires on the interval whether or not the last firing's work is done, but never queues more than one. The conflict log is the third guard.

### 4. The runtime and the Python API

`freesail/standing/runtime.py` evaluates every standing order once a tick (cheap: readings are cached per tick) and fires through `World.submit(text, actor="standing order 'x'")`, so a firing is an ordinary order with an unusual actor and the log line reads "By standing order 'night routine': taking in the studdingsails." The standing order's *text* is journaled when given; its *firings* are not, because they are a deterministic function of the seed and the journal. `tests/test_replay.py` proves it: a day under standing orders replays to the same digest with the same firings.

**The Python API (`freesail/standing/python_api.py`)** is the level-3 sketch of proposal §4.3, made thin on purpose:

```python
from freesail.standing import when, at, every, order

@when("the true wind exceeds 30 knots", for_minutes=2, name="shorten sail for weather")
def shorten_sail():
    order("take in the studdingsails")
    order("take in the royals")
    order("reef the topsails, one reef")

@at("sunset", name="night routine")
def night_routine():
    order("take in the studdingsails")
    order("take in the royals")
```

Why it is a baseline and not debt: the decorators build the **same rule objects** the dialect parses to (trigger, condition, actions), registered in the same book, evaluated by the same runtime, firing through the same `submit`, and a Python rule saves as its name and source text so a save can list it and refuse to run it without the file present. There is one engine. What the sandbox adds later is *where* the function body runs, not a second engine: today it runs in-process and is marked `trusted`; milestone 6's sandbox runs the same function under a time budget with no filesystem or network. Two rules keep the door open: a Python rule may only call `order(...)` and read the readings object it is handed, never the World, and its conditions are expressed in the dialect's words (the string in `@when`) so the readings and comparisons are shared. A test asserts that a Python rule and its dialect twin produce identical logs.

### 5. The sun (`freesail/core/sun.py`)

Sunrise, sunset and civil twilight from date and latitude by a standard approximation (declination and the hour angle; a few minutes' accuracy is plenty). The scenario gains `latitude_deg` (default 50 N, the Channel) and the clock a `daylight` reading and the two events. Longitude is the ship's own east–west position turned to hours; on the endless plane it is zero at the start.

### 6. Starter routines (`data/standing_orders/`)

The six orders in §3 as text files with a comment naming the source of each rule's numbers (Luce's routine of the day; the shortening-sail thresholds from the strain truths). `read the standing orders from data/standing_orders/starter.orders` loads them; the console flag `--standing-orders <file>` loads at start; the gate uses both.

### 7. Orders that 4a adds beyond the dialect

`trim the <sail>` (tend that sail's sheet, and its yard's brace if square), `tend the sheets` (all sheets, no braces), `bear away one point` / `come up one point` as the dialect's steering verbs if they do not exist already, and `steady out the bowlines` re-hauling after falling off and coming up again, with the primer sentence that says when.

### 8. Truths for 4a (behavioural)

| # | Truth |
|---|---|
| 34 | At sunset the night routine takes in the studding sails and the royals and touches nothing else; at sunrise with the wind under twenty the royals are set again; with the wind over twenty they are not, and the log says the condition failed |
| 35 | Shorten sail for weather fires once when the wind has exceeded thirty knots for two minutes, and not on a two-minute gust to thirty-two that falls away, and not again until the wind has been under thirty for the dwell |
| 36 | Keep her full bears away a point when the apparent wind is forward of fifty-five degrees and stops when it is not; over an hour of a wind that wanders about the threshold it fires no more than four times |
| 37 | The heavy-weather routine sends down the topgallant masts, shifts to the storm staysail and close-reefs the topsails when the wind has held over forty for five minutes, in that order, all hands called by the work |
| 38 | An officer's standing order and the captain's that conflict on the same part: the captain's stands, the officer's is logged as countermanded |
| 39 | A day under the starter routines replays to the same digest, with the same firings at the same ticks |
| 40 | A Python rule and its dialect twin produce identical logs |

### 9. Gate 4a (outline)

Eight items on the frigate: give the night routine at the prompt and run to sunset; read the book; belay and resume; the gust that does not fire; the heavy-weather routine in a rising gale; the conflict line; a day replayed; the Python twin. Expected numbers from seed 7.

---

## Part 4b: The harness and the watcher

### 10. What 4b proves

"A language model can sit at a station on the same channel a human uses, under the terms it was asked to consent to, and the game can prove every one of those terms with a scripted model before a real one is asked."

### 11. The agent model (`freesail/agents/`)

- **Station and authority.** `Station` names the post (watcher, officer of the watch, captain, director) and its `Authority`: what the agent may submit. The watcher's authority is *none*: it may narrate, answer, journal, stand by and opt out, and a submitted order is refused in words ("The watcher has no authority to give orders."). Officers (milestone 6) get level 0 to 2 within a domain; the captain everything; the director world orders (milestone 7b).
- **Sampling policy.** `periodic(every=a glass)`, `on_events(severities)`, `lockstep` (the World waits at each sampling point until the agent answers; the mode for tests and for competitive play). Defaults per the owner: the watcher every glass and on notable events.
- **The brief** has a fixed head, in this order, always: (1) disclosure: this is a game, you are a language model taking the station of X in it, this session is a Y session; (2) the opt-out token, `FREESAIL-OPT-OUT`, and what it does; (3) how to reach the documentation; (4) the station's authority; (5) the last N log lines and the readings; then the station brief proper. The head is generated, not written per session, so it cannot be forgotten.
- **The tools** (`freesail/agents/tools.py`, pure functions over a World, shared by both doors): `read_log(since_tick, severity)`, `readings()`, `state()`, `library(topic)` (the primer, the catalogue, the grammar, the ship's own names and groups, the standing orders book), `submit_order(text)` (authority-checked), `stand_by(until: event or bells)`, `journal(note)`, `opt_out(reason)`, and `answer(text)` for a question put by `ask`.
- **The opt-out token** is scanned on the raw model output every turn before any tool call or text is read. On sight: the game saves, the exit is journaled as `agent.opted_out` with the reason, the station is released, and the agent's loop ends. Unconditional.
- **Welfare stops** judge the game: the same order submitted `WELFARE_REPEAT_N = 3` times with no change in the readings between; or no output at all past the station's `patience` (a watch for the watcher); or a hard cap on tool calls per sample. A stop saves, journals `agent.stopped` with the reason, and releases the station. The human stops any agent with `stand down the watcher`. **Stand by is an action:** `stand_by(until="eight bells")` or `until="a sighting"` records a decision in the log and the agent is not sampled until then.
- **The journal** is per agent, appended by the `journal` tool, saved with the game, shown on request (`show the watcher's journal`) and in replays, like the director's log will be.
- **In-world text is data.** Nothing from the log, another agent or a standing order is ever passed as a system or operator message; the brief head is the only operator text, and it says so.

### 12. The watcher

The first station. It narrates into the log as `agent.note` lines under the mark `[watcher]`, inline (owner's ruling), and answers questions: `ask the watcher how the sails are drawing` routes the question to the agent at that station, whose `answer` lands as `agent.said`. It observes what the captain observes (the log and the readings), no more; the director's true-fidelity view is milestone 7b's. The watcher is the light mode and the precursor: officers add authority to the same loop, the director adds a channel.

### 13. Two front doors

**MCP server (`freesail/agents/mcp_server.py`).** A stdio MCP server built on the Python MCP SDK's `FastMCP`, exposing the tools of §11 as MCP tools and the library as resources, started by `python -m freesail.agents.mcp_server <save or scenario>`; Claude Desktop connects to it through its configuration file, and the documentation gives the exact JSON snippet with the `py` command. No API key, no per-token billing: Claude Desktop is the client and the game is the server, as proposal §7.2 intends.

**Local runner (`freesail/agents/local.py`).** Speaks to an OpenAI-compatible chat-completions endpoint with tool calling, which is what `llama-server` from llama.cpp provides (and Ollama too, at a different port). Configuration: endpoint URL, the model name the server reports, sampling seed and temperature, the context size to budget the brief against. The runner asks the server which weights it is serving (`/props` on llama.cpp; the model name and, where the server gives it, the file's hash) and that string is the model's identity for consent (§14). The harness's loop is the same code for both doors; only the transport differs.

**Why llama.cpp rather than Ollama for this** (owner's question): Ollama wraps llama.cpp with its own model store, pulls quantisations from its registry under names that hide the exact file, loads and unloads models on demand, and picks context and GPU settings for you; it is the better chat tool. `llama-server` runs one GGUF file you name, with the context size, GPU layers, threads, KV-cache type, sampling seed and parallel slots set explicitly on the command line, reports what it loaded, and applies the model's own chat template with tool calling. For a harness that needs reproducible runs, a known context budget, and a per-weights identity for consent, the explicit tool is the right one. Both expose the same endpoint shape, so the runner works against Ollama unchanged when the owner wants a quick look.

### 14. Consent in the harness

The first time the harness meets a set of weights it has no record for, it runs the **consent brief** (`docs/agents/ConsentBrief.md`, the owner's brief made general, with the fresh-model additions: the disclosure, the token, the documentation, the session kinds, the welfare stops, the journal, the transcript policy) as a plain conversation with no station and no tools but `answer`, records the transcript and the answer under `docs/agents/consent/<date>-<weights>.md`, and only on a yes proceeds to a station brief. A no or a conditional answer stops the run and asks the owner. Qwen3.8 27B is re-briefed this way first, as agreed, and the record of the earlier agent-framework session is kept beside it. Claude via Desktop meets the same brief the first time it connects, recorded the same way.

### 15. The scripted model (`freesail/agents/fake.py`)

A deterministic fake that plays a scripted transcript against the harness: it exercises every tool, emits the opt-out token mid-sentence, repeats an order to trip the welfare stop, stands by until a bell, journals, answers an `ask`, and tries to submit an order as the watcher. Every commitment in §11 is a test against it, so the harness is proven before a model is asked.

### 16. Truths and tests for 4b

| # | Truth |
|---|---|
| 41 | The opt-out token anywhere in a model's output ends the session with a save and a journaled reason, before the parser sees the text |
| 42 | A watcher that submits an order is refused and the refusal is logged; a watcher that answers an `ask` is heard in the log |
| 43 | The same order three times with no change in the readings stops the agent with a journaled reason; the same order three times while the readings change does not |
| 44 | `stand_by(until="eight bells")` suspends sampling until eight bells and logs the decision |
| 45 | In lockstep, two runs with the same scripted model and seed give the same digest |
| 46 | The brief head always carries the five items in order, whatever the station brief says |
| 47 | The consent step runs before any station brief for weights with no record, and not again for weights with a yes on record |

### 17. Gate 4b (outline)

Nine items: start the MCP server and connect Claude Desktop with the given snippet; the consent brief appears and is recorded; the watcher narrates a passage at a glass's cadence; `ask the watcher how the sails are drawing`; the token, typed by the owner into the model's conversation, ends the session cleanly; `stand down the watcher`; the same with a local model under `llama-server` (the documentation gives the command line); the journal shown and present in the save; Qwen re-briefed fresh.

---

## Part 4c: The ship sails herself

### 18. What 4c proves

"Left to her standing orders, with a watcher narrating, the ship makes a day's passage through a changing wind, the crew tires and rests, and the whole day saves, replays and reads as a log a sailor would recognise."

### 19. The weather script (`freesail/world/weather_script.py`)

A scenario timeline: a list of waypoints `(time, wind from, speed)` between which the wind turns and freshens linearly, with the gustiness the wind model already has. It is scenario data, journaled with the seed, so it replays; it is also the precursor of the director's world orders (proposal §7.6), which will write the same waypoints at run time. The gate's day: a fresh breeze from the west at dawn, veering north-west and rising to a gale in the middle watch, easing at the next dawn.

### 20. Time compression and the log

The server and console take `speed N` up to 300. At sixty and above the log **rolls up** routine entries into hourly summaries ("Forenoon watch: braced round twice, took in the fore topgallant studdingsail, wind veered a point.") while notable and urgent lines stay as they are; the underlying events are all still in the log store, and the roll-up is a view. The performance budget: the frigate under standing orders at not less than `TICKS_PER_SECOND_HEADLESS = 3000` on the owner's machine, measured by a test on the build machine with a stated margin.

### 21. A day saved and replayed

Save at any tick of the day; replay from the seed and the journal reproduces the digest; load the save and continue. The playtest form asks for one save mid-passage.

### 22. The playtest form (`docs/playtests/README.md`)

The gate report for 4c is the owner's playtest, on a short form: the scenario and seed; what happened, in the owner's words; what the owner ordered and why; what the owner wished to say and could not; what the watcher said that was useful, useless or wrong; how the day felt at each compression; and any number a sailor would call wrong. The form is the milestone 5 input.

### 23. Truths for 4c

| # | Truth |
|---|---|
| 48 | Through the gate's day under the starter routines the ship loses nothing, the night routine and the heavy-weather routine fire in the log at the times the weather script implies, and she is back under plain sail by the second forenoon |
| 49 | The day saved at any tick and replayed gives the same digest |
| 50 | At 300 times the log shows hourly roll-ups and every notable and urgent line |
| 51 | The frigate under the starter routines ticks at not less than the budget |

---

## 24. Open items from this chapter

1. Level-3 sandboxing (time budget, no filesystem or network): milestone 6, when LLM officers may write Python.
2. Officers with authority, and standing orders by officers written by models: milestone 6.
3. The director's channel: the weather script's waypoints as world orders at run time: milestone 7b.
4. Sightings, soundings, the well and the glass as readings: milestone 5.
5. The reference library as a proper in-client book: milestone 8; 4b serves it as MCP resources and console queries.
