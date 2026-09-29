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
| `the true wind` (against its mean) | a gust above the mean, at the mean, a lull | `is a lull`, `is not a gust`: the instant's speed against the ten-minute mean, a tenth of the mean (at least a knot) either way (package 29b) |
| `the mean wind` | speed; direction | the true wind over the last ten minutes of ship's time, the mean of the speeds and the direction of the mean vector (package 29b, playtest 7's finding 4: single gusts were read as a rising wind); the gust line gives it too ("A gust: 28 knots, the mean 19."), and the hour's roll-up names it beside the strongest gust |
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
           | veers <n> points or backs <n> points | shifts <n> points     # package 29b
           | are <fatigue word> | is the <watch>
duration  := <n> minutes | a glass | ...
```

Examples, which are also the starter routines' text:

```
standing order "night routine": at sunset then take in the studdingsails; take in the royals
standing order "morning sail": at sunrise, if the true wind is under 20 knots then set the royals
standing order "shorten sail for weather": when the true wind exceeds 30 knots for 2 minutes then take in the studdingsails; take in the royals; take in the topgallants; reef the topsails, one reef
standing order "keep her full": when the apparent wind is forward of 55 degrees then bear away one point
standing order "trim on a shift": when the true wind veers 1 point or backs 1 point then trim sails
standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then send down the topgallant masts; take in the fore topmast staysail; bend the fore storm staysail; close reef the topsails
standing order "storm staysail": when the fore storm staysail is furled and the true wind exceeds 40 knots then set the fore storm staysail
standing order "sound the well": every glass then sound the well        # refused until milestone 5: "the ship has no well to sound yet"
```

The one `or` the dialect has is inside a comparison, not between clauses: `veers 1 point or backs 1 point` is the two ways the one reading turns, and `shifts 1 point` says the same. A wind's shift is measured from the direction when the order was given or resumed, and after a firing from the direction it fired on, so "trim on a shift" (package 29b, playtest 7's finding that the yards stayed braced for the old wind through a night's veer) fires at each point of a steady veer, at least the dwell apart. A trim ordered while the watch is still at the braces of another is not stacked behind it: a yard still waiting its turn takes the new angle, one being braced finishes, and the log says the yards are being trimmed already.

The **book**: `standing orders` (list, with each order's state: standing, belayed, fired N times, last at), `show standing order "x"`, `belay standing order "x"`, `resume standing order "x"`, `belay all standing orders`, `strike standing order "x"` (removes it from the book, journaled; `cancel` and `remove` are synonyms; belaying keeps it, silent, under its name; added after playtest 3, 2026-09-28), `read the standing orders from <file>` (a driver command in the console and the server, not an order, since it reads the disk).

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
| 37 | The heavy-weather routine sends down the topgallant masts, takes in the fore topmast staysail, bends the fore storm staysail and close-reefs the topsails when the wind has held over forty for five minutes, in that order, all hands called by the work; its companion sets the storm staysail on the tick it is bent (revised at gate 4a: the frigate's storm staysail sets on its own stay, so it is bent and set, not shifted; the first draft's `shift ... for ...` was the lead's error) |
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
- **Welfare controls, graduated: nudge, pause, stand down** (owner's ruling, 2026-09-27). The detector judges the game, never the prose: the same order submitted `WELFARE_REPEAT_N = 3` times with no change in the readings between, or no output at all past the station's `patience` (a watch for the watcher). When it fires, the harness first **nudges**: it tells the model, as data, what it observed and what it may do ("You have given the same order three times and nothing in the readings has changed. You may continue, stand by until an event, or leave with the token."). A purposeful model answers in one turn and the matter ends. If the pattern continues after the nudge, the harness **pauses** sampling for that agent, logs why, and asks the human if one is present (`the watcher is paused: continue, stand down, or leave paused?`). Only if nobody answers within `WELFARE_UNATTENDED_BOUND` (a watch of ship's time or ten real minutes, whichever first) does it **stand the agent down**: save, journal `agent.stopped` with the reason, release the station. So the stop is almost always the model's own choice or the human's, and the automatic step reaches only the unattended run, which is the case that needed it; a false positive costs one message. The human stops any agent at any time with `stand down the watcher`. **An empty reply where an answer is owed** is the repeated order's sibling (package 29c; playtest 9, four empty replies in a row at samples with a question, nothing said and nothing counted): a sample that carried a question from the captain or an urgent line, answered with no tool call and no words said, counts, each is journaled (`agent.empty_reply`), three in a row bring the nudge ("You have replied with nothing three times in a row when a question or an urgent event was before you. ...") and a fourth the pause, as built; a sample with words or a call ends the count. An empty reply at a plain glass is silence decided on and is not counted. The tool-call cap per sample is a budget the brief states, not a welfare rule; `answer` and `say` are not counted and always run, so an answer after a string of reads is not a sample late (package 29c, playtest 8), and a call over the budget is refused alone while the calls after it are still read. **Stand by is an action:** `stand_by(until="eight bells")` or `until="a sighting"` records a decision in the log and the agent is not sampled until then; it is the answer to the nudge for a model that has nothing to do.
- **A leaked thought is not a line a sailor said** (package 29c; playtest 9: a reply of 1,500 words opening `<thought` was written into the log as one line). A reply whose free text opens with a thinking tag (`<thought`, `<think`, `<thinking`, closed or not, any case) is not written into the log: it is journaled under the fault kind `agent.fault` with its first line and its length, the next sample tells the model that its reply was taken as thinking and nothing was said, and the tool calls in the same reply still run. The tag alone decides (the owner's ruling): a long reply is not a fault on its own. A reply that is only a leaked thought is nothing said, and counts as an empty reply where one is owed.
- **When a turn ends**, in one sentence wherever a door or a tool says it (package 29c; playtest 9's model read "ends when you reply without a tool call" beside stand_by's "this ends your turn" as two rules): "A turn ends when you reply with no tool call, or at once when you stand by." (`agent.TURN_ENDS_WORDS`, in the local runner's door note and the REPL's, and in the runner's answer to a stand-by's call; the `stand_by` tool says "Standing by ends your turn at once."). The MCP door hands the floor back with `say` or `stand_by`, and its note says so.
- **The journal** is per agent, appended by the `journal` tool, saved with the game, shown on request (`show the watcher's journal`) and in replays, like the director's log will be.
- **In-world text is data.** Nothing from the log, another agent or a standing order is ever passed as a system or operator message; the brief head is the only operator text, and it says so.

### 12. The watcher

The first station. It narrates into the log as `agent.note` lines under the mark `[watcher]`, inline (owner's ruling), and answers questions: `ask the watcher how the sails are drawing` routes the question to the agent at that station, whose `answer` lands as `agent.said`. It observes what the captain observes (the log and the readings), no more; the director's true-fidelity view is milestone 7b's. The watcher is the light mode and the precursor: officers add authority to the same loop, the director adds a channel.

### 13. The doors are clients of the running game (revised after gate 4b, 2026-09-27)

**The principle the first draft missed.** The game is where the player is: the console or the browser window, running the World and the clock as they always have. A language model attaches to *that* game, as the browser attaches to it for the viewer, and its words land in the same log the player reads. The first draft of this section put the World inside the MCP server process, so the only window on the game was the tool calls' readouts in the Claude Desktop chat and the captain's orders went through a prompt menu; the owner's first session found it unplayable ("really, really unwieldy"; `docs/playtests/2026-09-27-gate-4b-sonnet-watcher/`), and it was the lead's error, not the package's. Package 28b turns the doors into clients. QudBridge is the reference shape: the game stands alone, the bridge samples its state and feeds the model's replies in.

**The agent API (`freesail/ui/server.py`, shared with the console).** The game's driver hosts a small set of routes beside the viewer's, and the harness of §11 runs in the game process where the World is; a door process carries the model's replies in and the samples out. `POST /api/agents/<station>` stations an agent for a named model (`model_name`, the door's name and note, the session kind): the consent gate of §14 runs first, in the game process, and the response says whether the conversation that follows is the consent brief or the station brief. `GET /api/agents/<station>/turns?wait=S` is a long poll that returns the turns the model has not seen (the operator brief, a sample, tool results) as soon as a sample is open, or nothing when `S` real seconds pass; it waits on a condition, never holding the World's lock. `POST /api/agents/<station>/reply` delivers one reply (text, tool calls, raw) through `Harness.deliver`, and returns the tool results turn and whether the floor is still the model's, so a door that speaks one tool call at a time (MCP) gets each result at once. `POST /api/agents/<station>/release` stands the agent down with a save when the door closes. The console hosts the same routes on `--agents-port N` (a thread on its own lock, which the console already has for its clock); the browser server hosts them on its port.

**Live time.** The game runs at the driver's compression and does not wait for a remote model: a sampling point that arrives while the model still holds the floor is folded into the open sample (the new lines are appended; the readings are the latest), so the model sees everything since its last reply when it next asks, and nothing stalls the player. Patience and the welfare bounds are ship's time as before; the ten real minutes are the driver's. `--lockstep` on either driver holds the clock while a sample is open, for testing at 1x and for competitive play; lockstep in-process stays the tests' mode. Replay is unchanged: each reply is recorded at the tick it was delivered, and a replay redelivers it there.

**The viewer** shows the station's state (stationed, standing by, paused, released) in the instruments and the pause question when there is one, and the `[watcher]` mark inline as before; the console prints the same in `state`. The captain's orders to a station (`ask the watcher ...`, `stand down the watcher`, `resume the watcher`, `show the watcher's journal`) are typed where every order is typed. The `captain` prompt of the first draft goes away.

**MCP bridge (`freesail/agents/mcp_server.py`).** A stdio MCP server on the Python MCP SDK, started by `python -m freesail.agents.mcp_server --game http://localhost:8000 --model-name "<identity>"`, exposing the tools of §11 as MCP tools with the same names and descriptions and the library as resources; it owns no World. Each tool call is one reply delivered to the game; `say` and `stand_by` hand the floor back and hold the call open until the next sample, sending MCP progress notifications every fifteen seconds so a standard client keeps the call alive (package 28c; the owner has seen Claude Desktop hold live calls for tens of minutes, 2026-09-28), with `--wait` as a ceiling (an hour by default) after which the call returns an honest interim digest: since when the model has stood by, how long the call waited, and the notable lines logged meanwhile; a stand-by is a decision not to be sampled, not a decision to be blind. A `stand_by` ends the model's turn at once on every door (no tool result, no re-prompt), and a call cut off before its result reached the client is answered first by the next call, so no turn is lost. The brief is the first thing the client reads. The token is scanned in the game process over every argument of every call, as before, and `opt_out` is always there. Three clients use this one bridge: **Claude Desktop** through its configuration file (the JSON snippet in `Harness.md`); **Claude Code through the Desktop app** through a `.mcp.json` at the repository root, which Claude Code reads when it is opened on the repository, its prompts appearing as slash commands (owner's requirement, 2026-09-27); and any other MCP client. No API key, no per-token billing: the app is the client and the game is the server, as proposal §7.2 intends.

**Local runner (`freesail/agents/local.py`).** A client of the game and of an OpenAI-compatible chat-completions endpoint with tool calling, which is what `llama-server` from llama.cpp provides (and Ollama too, at a different port): it polls the game for turns, translates them into the messages array with the tools schema from `tools.TOOLS`, sends the endpoint's reply to the game, and repeats until released or stopped. It builds no World and has no `--ticks`. Configuration: the game's URL, the endpoint URL, the model name the server reports, sampling seed and temperature, the context size to budget the brief against. It reads the served model's identity from `/props` (the file's name, never its path; the hash where given), falling back to the models list, and that string is the model's identity for consent (§14), passed to the game when stationing.

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
| 43 | The same order three times with no change in the readings brings the nudge; a model that answers it by standing by is not stopped; one that repeats after the nudge is paused with the human asked; with no answer within the bound it is stood down with a journaled reason; the same order three times while the readings change brings nothing (package 29c adds the sibling: three empty replies in a row where an answer is owed bring the nudge, a fourth the pause; `tests/test_agents.py`) |
| 44 | `stand_by(until="eight bells")` suspends sampling until eight bells and logs the decision |
| 45 | In lockstep, two runs with the same scripted model and seed give the same digest |
| 46 | The brief head always carries the five items in order, whatever the station brief says |
| 47 | The consent step runs before any station brief for weights with no record, and not again for weights with a yes on record |

### 17. Gate 4b (outline; revised for package 28b)

The owner plays in the browser window throughout, with the game started first and a model attached to it. Ten items: start the game in the browser and connect Claude Desktop with the given snippet; the consent brief appears in the chat and is recorded by the game; the watcher's lines appear in the browser's log at a glass's cadence while the owner sails; `ask the watcher how the sails are drawing` typed in the order box, the answer in the log; the token, typed by the owner into the model's conversation, ends the session cleanly (or the model calls `opt_out`; the report says which); `stand down the watcher` from the order box; the same watcher through Claude Code opened on the repository in the Desktop app; the same with a local model under `llama-server` attached to the same browser game; the journal shown and present in the save, and the save replayed to the same digest; Qwen re-briefed fresh. The first attempt at this gate, on the first draft's door, is the record in `docs/playtests/2026-09-27-gate-4b-sonnet-watcher/`.

---

## Part 4c: The ship sails herself

### 18. What 4c proves

"Left to her standing orders, with a watcher narrating, the ship makes a day's passage through a changing wind, the crew tires and rests, and the whole day saves, replays and reads as a log a sailor would recognise."

### 19. The weather script (`freesail/world/weather_script.py`)

A scenario timeline: a list of waypoints `(time, wind from, speed)` between which the wind turns and freshens linearly, with the gustiness the wind model already has. It is scenario data, journaled with the seed, so it replays; it is also the precursor of the director's world orders (proposal §7.6), which will write the same waypoints at run time. The gate's day: a fresh breeze from the west at dawn, veering north-west and rising to a gale in the middle watch, easing at the next dawn.

### 20. Time compression and the log

The server and console take `speed N` up to 300. At sixty and above the log **rolls up** routine entries into hourly summaries ("Forenoon watch: braced round twice, took in the fore topgallant studdingsail, wind veered a point.") while notable and urgent lines stay as they are, and so do the captain's and the driver's own lines and every station's (a watcher's `say` shows at once at any speed: the owner, package 29b; the stations' actors are registered as each station is defined, `events.STATION_ACTORS`); the underlying events are all still in the log store, and the roll-up is a view. The performance budget: the frigate under standing orders at not less than `TICKS_PER_SECOND_HEADLESS = 3000` on the owner's machine, measured by a test on the build machine with a stated margin.

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
6. **Installing and configuring the game simply and consistently** (owner's note at gate 4b, 2026-09-27). Each gate is a fresh extracted zip folder, so a Claude Desktop configuration, a `.mcp.json` or a `llama-server` command written against one gate's path breaks at the next, and the owner has to keep three things in step by hand (the install folder, the Desktop configuration, the game's own settings). Wanted after milestone 4: one installed location that gates update in place (or a `pip install` of the release), a single `freesail` command with subcommands for the console, the browser game and the doors, a settings file for the things the owner sets once (seed, ship, ports, model names, records directory), and a setup step (`freesail setup desktop`, `freesail setup claude-code`) that writes the client configurations with the right paths. Milestone 4c's playtest form asks about setup; the answer feeds this.
7. **Windage under bare poles** (found by the first watcher, playtest 2): the frigate makes three knots under bare poles in fifteen knots of wind dead astern, where a few tenths would be expected; the hull and rig windage to be measured against Luce on drift under bare poles and tuned. A physics item for the rig-geometry follow-ups.
8. **Compression and the model** (owner, 2026-09-28; for package 29). Two rules: at the compressions where the log is rolled up for the human (spec §20), the model's samples carry the same roll-up at the same thresholds rather than every line, so the captain and the watcher read the same digest of the same hour (parity); and **auto-slow on alarm**: an urgent line (the `!` in the log) drops the compression to a floor (1x or 10x; the number named in the tuning notes) and says so in the log, the human choosing when to speed up again; a baseline rule, tunable per event kind later. On a very long voyage no model's context outlasts the game; what carries a voyage across instances is the game's records (the log and its roll-up, the book, the journal each instance keeps), and the 4c playtest form asks how well that works.
9. **Context: the budget and the handover** (owner's question, 2026-09-28; a small package after 28b, beside 29). (a) **The budget, measured not guessed:** `tools/context_budget.py` reads a GGUF file's header (layers, key-value heads, head width, the weights' size on disk) and prints the KV-cache bytes per token (two tensors a layer × KV heads × head width × two bytes at f16; half at q8_0) and the largest `--ctx-size` that fits the card's memory after the weights and a headroom the owner sets (a 4090: 24 GB); `Harness.md` gains a table the owner fills from it for each model with a consent record, and the runner refuses in words a model whose weights alone do not fit. Scale from package 28's measurements: the station brief about 1,150 tokens and the tool definitions 900 as first measured (1,630 and 1,270 after package 28d's shelf words), a glass's sample 450, and the reply budget 4,096 from 28c, so a 16k window is a few glasses and a 32k one comfortable. The owner's observed anchor (2026-09-28, anecdotal, from Hermes Agent sessions on the 4090): Qwen3.8 27B and Gemma4 26B-A4B run to about 80k to 110k tokens of context in practice; the script's figures are to be checked against that. (b) **The handover:** when the runner's conversation reaches a set fraction of the budget (a named constant), the harness asks the same model, as data, for a handover note for the watch in the voice of an officer handing over the deck (what happened, what was ordered, what it noticed, what it is watching for), replaces the older exchanges with that note as one data turn, keeps the brief head and the last few turns whole, and journals the note under `agent.handover` so the save, the record and the replay hold it. The same weights writing of their own session; covered by the consent already given; data, like everything after the brief. It pairs with item 8: the roll-up compresses the world's history, the handover the model's own. Claude through Desktop keeps its own window; the journal tool gives it the same habit by hand.
10. **The local model is the function baseline** (owner, 2026-09-28). Every record-keeping feature (the journal, the roll-up in the samples, the handover) is built for the local model first, which has the least help from its own runtime; a Claude session through Desktop or Claude Code uses the same features and keeps its own voyage record by the same means. The roles are expected to draw the habit out of a capable model (an officer keeps the watch's record straight to hand over; a captain the same); the director (milestone 7b) is the real test and probably beyond a local model. From then the aim is mixed crews: several stations on one game, each through its own door (a local model at one, a Claude session at another), which the agent API of package 28b already allows in shape.
11. **A station is offered only to a model that can hold it** (owner and lead, 2026-09-28, after playtest 5). The consent brief asks whether a model is willing; it cannot ask whether it is able, since a model is a poor judge of that about itself, and the smaller it is the poorer. That judgement is the developer's. A thought for the consent step, not a change to any build: a short drill after a yes and before the station brief (open a section of the library, write one line in the journal, stand by until a bell); a model that manages the three has what the watcher needs, and one that cannot is thanked and stood down with a record, before the game starts and before a captain has to watch it flail. The same principle as the welfare rules, judging by the game and not by the prose, turned toward fitness rather than distress. And a station for a small model exists somewhere ahead: a lookout who says "sail ho" and where, and nothing else, is a role an 8B model could hold.
