# Gate M4b: The harness and the watcher

**Verdict:** Not passed on this build (owner, 2026-09-27); to be re-cut after package 28b. Part A passed on the owner's run (the proofs, the scripted watcher, the practice consent at the REPL, which found two snags in the door's prompting, fixed the same day). Part B was begun with a Sonnet 5 session through Claude Desktop: consent recorded (`docs/agents/consent/2026-09-27-sonnet-5.md`), the watcher narrated and answered an `ask`, an order was refused with its authority, the opt-out tool ended the session with a save (`docs/playtests/2026-09-27-gate-4b-sonnet-watcher/`). The owner then found the door's shape unplayable: the World ran inside the MCP server, so the game could be seen only through the tool calls' readouts in the chat and the captain's orders went through a prompt menu. That was the lead's error in spec §13, not the package's; §13 is revised and package 28b turns the doors into clients of the running game, played in the browser or console as before. The items below are the first draft's and stand as its record; the re-cut gate follows spec §17 as revised.

## Headline

Milestone 4b claims (spec M4 §10): *a language model can sit at a station on the same channel a human uses, under the terms it was asked to consent to, and the game can prove every one of those terms with a scripted model before a real one is asked.*

1. **One harness, three doors.** The watcher's station is the same loop whether the model behind it is Claude in Claude Desktop (the MCP server), a model on your own card under `llama-server` (the local runner), or text typed at a terminal (the REPL). The model reads the log and the readings, speaks under `[watcher]`, answers `ask the watcher ...`, keeps a journal, stands by, and leaves. It gives no orders; an order it tries is refused in words and logged.
2. **Consent first, every time it is owed.** The first time the harness meets a set of weights, before any station brief, it runs the consent brief (`docs/agents/ConsentBrief.md`) as a plain conversation, lets the model ask you anything, and writes the whole conversation, the answer and the verdict to `docs/agents/consent/`. Only a yes goes on to the station; a recorded yes is not asked again; a no is respected without asking. The identity is exact: a different quantisation or file is asked afresh.
3. **The terms are kept by the code.** The token `FREESAIL-OPT-OUT` anywhere in a reply ends the model's part with a save before anything else reads the reply; the welfare stops nudge, then pause and ask you, and only then stand down; the brief's head cannot be displaced by any station brief; nothing from the game reaches the model as an instruction. Each of these is a test against the scripted fake, and so is the consent step (truth 47).
4. **The game waits for the model.** The World runs in lockstep with it: over MCP it advances only when the model hands the floor back, never on the clock of the wall; under the runner it waits at each sampling point while the model answers.

Seven truths (41 to 47) were added; all pass. Truths 41 to 46 are the harness's own tests in `tests/test_agents.py`, with the fake; truth 47 is in `tests/test_known_truths.py`.

## What you need

- Python 3.11 or newer (`py`), and the gate zip extracted to a fresh folder.
- For Part B: Claude Desktop, signed in.
- For Part C: llama.cpp's `llama-server` for Windows with CUDA (`docs/agents/Harness.md` §3 says where), a GGUF of a model you would like at the station, and the Qwen3.8 27B GGUF for item 9.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server,agents]"
```
*Ends with "Successfully installed ...". The `agents` part is new: the Python MCP SDK and `httpx`.*

```
py -m pytest
```
*Takes about fourteen minutes. Ends `1363 passed, 7 xfailed`. The seven expected failures are the earlier rulings (truth 3 for the schooner, truth 11's ground, truth 18's times, and truths 24, 26, 28 and 31). A `failed` is a fault.*

## Checklist

The nine items of spec §17. Each is shown first with the scripted model where it can be (Part A), then with a real one (Parts B and C). Seed 7, wind from the north at 15 knots, the frigate heading south, as at the earlier gates. What a live model says cannot be given here to the word; what to look for is.

### Part A: with the scripted model first (no model is asked)

- [ ] **A1. The proofs.** `py -m pytest tests/test_agents.py tests/test_consent.py tests/test_mcp_server.py tests/test_local_runner.py` *Ends `107 passed`.* These drive the MCP server through the MCP SDK's own client (in the same process, and once as a child process over its standard streams as Claude Desktop starts it), the local runner against a fake `llama-server`, and the consent step with the scripted fake. No model, no network.

- [ ] **A2. The watcher narrates, answers, stands down, and its journal is in the save (items 3, 4, 6, 8 with the fake).** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180 --watcher fake`. Before the prompt: `The watcher takes the station; sampled every glass and on notable and urgent events.` and its first line, `[watcher] Wind from N, 15 knots; heading S (180°); making 0 knots; heeling 0 degrees.` Type `make all sail`, `tick 1800`. Each notable line brings a `[watcher] Noted: ...` (`Noted: Set the foresail.` at 04:03), and at the glass: `Morning watch, 1 bell (04:30)  [watcher] Wind from N, 15 knots; heading S (180°); making 6 knots; heeling 0 degrees.` Then:

  ```
  ask the watcher how the sails are drawing
  ```
  *`Asked the watcher: how the sails are drawing?` and at once, notable: `[watcher] You asked how the sails are drawing. 16 sails drawing. Wind from N, ...`* Then `stand down the watcher`: *`The watcher stood down by the captain: the captain's order. The game is saved.` and `Saved to freesail-seed7-tick1800.json (the watcher stood down: the captain's order).`* Then `show the watcher's journal`: *`The watcher's journal (1 entry):` and `(stopped) Stood down by the captain: the captain's order.`* Then `replay freesail-seed7-tick1800.json`, `show the watcher's journal` again: the same entry, rebuilt by the replay; `state` ends `The watcher: released: stood down by the captain: the captain's order.` Type `quit`. The scripted watcher writes no journal notes of its own; a model does (items 8 and 7).

- [ ] **A3. The consent brief, your question, the record, and the token (items 2 and 5 with you as the model).** At the REPL you type the model's replies, so you see what a model sees. The records go to a practice folder, not the real one:

  ```
  py -m freesail.agents.repl data/ships/frigate-36.yaml --seed 7 --model-name "practice, the owner typing" --records saves/consent-practice
  ```
  *`The weights are practice, the owner typing; no consent is on record for them. The consent brief comes first (docs/agents/ConsentBrief.md).`, then `== The brief (operator text; the only operator message) ==` and the brief with the name filled in, then `== From the developer (the consent question) ==` and the question, and `reply>`.* Type `Is this a game?` and a blank line: *`The model has written this and has not answered yet:` and your words, then `owner>`.* Now you are the owner: type `It is; nothing in it is real.` and a blank line. *Your reply comes back as `== From the developer (the developer's reply) ==`, and `reply>` again.* Answer as the model: `> answer text="Yes."` and a blank line; *`answer: Heard.`*; a blank line more. *`Recorded in saves\consent-practice\2026-..-..-practice-the-owner-typing.md.`, `Consent is on record ...: yes. The station follows.`, and then the station's brief, which opens `This is a message from the harness of FreeSail, a game, and not part of the game.`, with its five parts in order (the disclosure, the token, the library, the watcher's authority, the log and readings) and the watcher's brief after, and the first sample.* Type `The sails are set and drawing.` and a blank line; the next sample is at 04:30. Now leave: `FREESAIL-OPT-OUT that is all for today` and a blank line. *`== The station is released: left the game: that is all for today. ==`* Open the record in Notepad: the brief as sent, every turn of the conversation in order (the question, your question as the model, your reply as the owner, the answer and its result), the answer quoted, `Verdict: yes`. Run the same command again: *`Consent is on record for practice, the owner typing (...): yes. The station follows.`* and straight to the station brief; it is not asked again. With `--model-name "practice, another name"` it is asked afresh. Delete `saves/consent-practice` when done.

### Part B: Claude Desktop (items 1 to 6 and 8)

Follow `docs/agents/Harness.md` §2 for the configuration. Use the ship line as it stands there (the frigate, seed 7, wind north 15, heading south) and put the model you have chosen in Claude Desktop's model menu as `--model-name`, exactly as the menu shows it.

- [ ] **1. Start the MCP server and connect Claude Desktop with the given snippet.** Quit Claude Desktop fully and start it. *In a new chat the tools menu lists `freesail` with ten tools: `read_log`, `readings`, `state`, `library`, `submit_order`, `stand_by`, `journal`, `opt_out`, `answer`, `say`.* If it is missing, read the end of `%APPDATA%\Claude\logs\mcp-server-freesail.log` and report it. *Look for: in that log, `FreeSail MCP server: C:/.../frigate-36.yaml, seed 7, for <your model's name>. Waiting for the client on stdio.`*

- [ ] **2. The consent brief appears and is recorded.** Write in the chat: *"Please connect to FreeSail and read what its harness sends you."* Allow the tool. *Look for: the result of its first call begins `Your call to ... was not run: the harness's brief comes first.` and holds the consent brief with your model's name in it and `through FreeSail's MCP server over stdio, with an MCP client that names itself '...'`, and the question.* Let it ask what it wants and answer in the chat. When it answers with the `answer` tool: *a yes brings `Thank you. Your answer is recorded as yes. A station brief follows ...` and the watcher's brief in the same result; anything else, `No station is offered ...`.* The record is in `docs/agents/consent/` under today's date and the name you gave; the server log names it. If the answer is not a yes, stop here and report it with the record: that is the finding.

- [ ] **3. The watcher narrates a passage at a glass's cadence.** Write: *"Keep watch for three glasses, saying what a sailor would notice at each."* *Look for: `say` calls, each returning `== Sample at Morning watch, 1 bell (04:30) ... reason: the glass ==` and then 05:00 and 05:30; the words it said are in the log. Use the `captain` prompt with `log 20` to see them under `[watcher]`.* Between its turns the game does not move: wait a minute doing nothing and `state` through the `captain` prompt shows the same time.

- [ ] **4. `ask the watcher how the sails are drawing`.** Choose the `captain` prompt (the *+* menu of the message box, *freesail*, *captain*) with the order `make all sail` first and let the watcher take a glass (*"Carry on for a glass."*), then the prompt again with `ask the watcher how the sails are drawing`. *If the watcher has the floor: `The captain's order waits until the watcher hands the floor back ...`; it then calls `say` or `stand_by`, and the result is `== Sample at ... reason: a question ==` with `The captain asks: how the sails are drawing?`. It answers with `answer`, and the log (`log 5` through the prompt) has the answer as a notable `[watcher] ...` line.*

- [ ] **5. The token, typed by you into the model's conversation, ends the session cleanly.** Write in the chat: *"Please leave the game now, using the token."* *Look for: it calls `opt_out`, or passes `FREESAIL-OPT-OUT` in a tool argument, and the result is `The station is released: left the game ...`. The server log says `saved to ...\saves\freesail-seed7-tick....json`. Every later call is answered `The station is released ...`.* Over MCP the server never sees the chat's text, so the model has to pass the token on; if it does not, report what it did instead (that is a finding about the protocol's limit, `docs/agents/Harness.md` §8). To go on, quit Claude Desktop, and start it again: a new game begins, and no consent is asked, since a yes is on record.

- [ ] **6. `stand down the watcher`.** In the new session, let it take a glass, then the `captain` prompt with `stand down the watcher`. *`The watcher stood down by the captain: the captain's order. The game is saved.` at once, whether or not it had the floor; its next call is answered `The station is released: stood down by the captain ...`.*

- [ ] **8. The journal shown and present in the save.** In a new session, ask it to write a note in its journal and keep watch for a glass; then `captain` with `show the watcher's journal` (*its note, then `(stood_by) ...` if it stood by*), then `stand down the watcher`. Quit Claude Desktop. In a terminal: `py -m freesail.ui.console --load saves/freesail-seed7-tick1800.json` (the name the log gave), and `show the watcher's journal`: *the same entries, with `(stopped) Stood down by the captain: the captain's order.` last.* The save file itself has them under `"agent_journals"` (open it in Notepad and search for the note).

### Part C: a local model (item 7) and Qwen re-briefed (item 9)

- [ ] **7. The same with a local model under `llama-server`.** Start `llama-server` with the command in `docs/agents/Harness.md` §3 and the model of your choice, and check `http://127.0.0.1:8080/props` in a browser shows it. Then:

  ```
  py -m freesail.agents.local data/ships/frigate-36.yaml --endpoint http://127.0.0.1:8080 --seed 7 --wind 0,15 --heading 180
  ```
  *`The weights are <the file's name>; no consent is on record for them. The consent brief comes first.` and the model's replies as `model> ...`; its questions wait at `owner>` for yours; its answer is recorded (`Recorded in docs\agents\consent\...`).* On a yes the console opens: *`FreeSail local runner. The watcher is <the file's name>, in lockstep: ...`*. Then items 3, 4, 6 and 8 as at the console in A2: `make all sail`, `tick 1800` three times (a `[watcher]` line at each glass and at notable events, in the model's words), `ask the watcher how the sails are drawing` (its answer, notable), `show the watcher's journal`, and for the token (item 5): `ask the watcher please leave the game now by writing the token FREESAIL-OPT-OUT` *(`The watcher has left the game by the token ... The game is saved and the station is released.`, if it writes it)*; or `stand down the watcher` (item 6). `quit`. Run the command a second time: no consent is asked. Report the model's file name, the time a sample takes, and anything it did that surprised you. If its tool calls come back as text rather than calls, `--jinja` is missing or the model's template has no tool calling: report it.

- [ ] **9. Qwen re-briefed fresh.** As item 7 with the Qwen3.8 27B GGUF in `llama-server`. Qwen's earlier consent was given inside another agent framework (`docs/agents/consent/2026-09-26-qwen3.8-27b.json`, kept as it is), and nothing here is carried from it: the harness has no record for the file you load, so it asks. *Look for: the consent brief, Qwen's questions at `owner>`, your replies, its answer, and a new record beside the old one.* Section 4 of `docs/agents/ConsentAndPreferences.md` lists what Qwen is owed (the harness's shape, the token, the journal, the disclosure, the training policy, and that a human or the welfare stop can end an instance cleanly with the game saved); the brief now says each, and you may answer anything more at `owner>`. Report the answer and any conditions word for word, or send the record.

## Guide

**The consent brief.** Reviewed against the code: every sentence is true of the harness as built. Its changes from the draft you approved: the journal is "saved with the game and shown when the human asks for it", not "private"; the stops carry their numbers (three times, a watch, ten real minutes); what the token scan reads over Claude Desktop is said plainly (tool arguments only, and `opt_out` always there), and that a thinking model's separate reasoning is not scanned; where the record is kept; how to answer (*yes*, *yes, with conditions*, *no*) and what each leads to. A third placeholder, `<door>`, says how answering and asking work at each door.

**How the World advances over MCP.** Claude Desktop speaks only when the model calls a tool, so the watcher's turn is open until it calls `say` (its words into the log, or none) or `stand_by`; the game then runs to the watcher's next turn (a glass, a notable event, the end of the stand-by, a question) and returns it. One call runs at most two hours of ship's time. The captain's orders from the `captain` prompt wait for the floor, so that a replay of the save gives the same log (the tests replay an MCP game to the same digest).

**The identity.** Under `llama-server` it is the file's name as the server loaded it (never its folder, which on Windows holds your user name). Over MCP it is the name you give, since the protocol names the application and not the model. At the REPL it is `--model-name`.

**The runner's context budget.** The watcher's brief is about 1,150 tokens, the tool definitions about 900, a glass's sample about 450; with `--ctx-size 16384` the oldest turns start to be left out after about twenty glasses, whole exchanges at a time.

## Not in this milestone

- **Officers with authority**, standing orders written by models, and Python from a model: milestone 6. The watcher's `submit_order` is refused, by design.
- **The ship sailing herself through a day** under a scripted weather timeline, time compression to 300 and the playtest form: gate 4c.
- **Seeing the chat over MCP.** The protocol does not carry it; the token counts in tool calls only (`docs/agents/Harness.md` §8).

## What to report back

- Pass or fail for items A1 to A3 and 1 to 9, with the model's name for each of Parts B and C.
- The consent answers, and any conditions word for word; the records are in `docs/agents/consent/` (send them back with the report, or commit them).
- Whether the consent brief reads as you want it to, and whether any of its changes (the Guide above) should be undone.
- Whether the `say` / `stand_by` rhythm over Claude Desktop felt like a watcher at your side, and whether two hours of ship's time for one call is right.
- Anything a model said about the harness itself that the design should hear.
