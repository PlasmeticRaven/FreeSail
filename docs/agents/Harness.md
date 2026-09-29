# The harness: connecting a model to FreeSail

How to put a language model at the watcher's station, for the owner, on Windows, typing `py`. Nothing here needs programming. **Start your game, then connect**: you play in the browser window (or the console) exactly as before, and the model attaches to that game from outside, as a second player at the watcher's station. Its lines appear in the same log you read, under `[watcher]`, and you give every order, `ask the watcher ...` included, where you always type orders.

Every command is typed in a terminal (PowerShell or Command Prompt) in the folder you extracted the gate zip into, unless it says otherwise. In the configuration files below that folder is written **`<the folder you extracted the gate zip into>`**; for example `D:/Projects/FreeSail/FreeSail-gate-m4b`. Write it with forward slashes (`D:/Projects/...`), or double every backslash (`D:\\Projects\\...`): a single backslash breaks the JSON. **The path changes with every gate**, since each gate is its own folder; until the install is simplified (an open item after milestone 4: one installed location, a single command, and a setup step that writes these configurations for you), change it in Claude Desktop's configuration each time you move to a new gate folder.

There are three doors to the same harness (`freesail/agents/`). Every one of them meets the **consent brief** (`ConsentBrief.md`) the first time a model comes to the game, and the game, not the door, runs it and keeps the record:

| Door | For | Started by |
|---|---|---|
| The MCP bridge (`freesail.agents.mcp_server`) | Claude Desktop; Claude Code in the Desktop app; any MCP client | the app itself, from its configuration |
| The local runner (`freesail.agents.local`) | a model on this machine under `llama-server` (or Ollama) | `py -m freesail.agents.local ...` in a second terminal |
| The REPL (`freesail.agents.repl`) | you, typing a model's replies by hand, in a game of its own | `py -m freesail.agents.repl ...` |

The first two are clients of the running game: they own no game of their own, and they reach it at its address (`http://localhost:8000` for the browser game). The REPL is the practice door and runs its own game, as it did at gate 4b's first draft.

## 1. Install once, in each gate folder

```
py -m pip install -e ".[dev,server,agents]"
```

It ends with `Successfully installed ...`. The `server` part is the browser game; the `agents` part brings the Python MCP SDK (the bridge Claude talks to), `httpx` (what the doors speak to the game and to a model server with) and `gguf` (llama.cpp's reader of a model file's header, for the context budget in section 5). Check it with `py -m pytest tests/test_agent_api.py tests/test_mcp_server.py tests/test_local_runner.py`, which proves every door against a scripted model, a fake model server and the game's own app, with no model and no network.

## 2. Start your game

```
py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180
```

It prints `FreeSail server. Seed 7. Open http://127.0.0.1:8000/` and `A model's door connects to http://localhost:8000 (docs/agents/Harness.md).` Open the address in your browser and sail as always. Leave this terminal open: the game prints its own lines about the model there (`FreeSail: ...`: who asked for the station, where the consent record went, where the game was saved and the log's digest at that moment).

When a model connects, the log says `The watcher takes the station; sampled every glass and on notable and urgent events.`, and the instruments gain a **Stations** row with one line per station, for example `The watcher (<its name>, through the MCP bridge): stationed; its turn is open.` If the watcher is paused (below), the row shows the question in red: *The watcher is paused: continue, stand down, or leave paused? Say 'resume the watcher' or 'stand down the watcher'.*

**How the watcher's turns go.** The game runs on its own clock at the speed you set and never waits for the model. At each glass (half an hour of ship's time) and at each notable event the watcher's **turn** opens: the model is sent what happened since its last turn and the readings. Whatever happens while it is still thinking is added to the same turn (the log lines since, the latest readings, your question if you ask one), so when it answers it has everything; the brief tells it so. It answers by speaking a line into the log, answering your question, writing in its journal, or standing by; then its turn closes until the next one. The brief puts the rule in one sentence: a turn ends when the model replies with no tool call, or at once when it stands by.

**What is not a line in the log** (package 29c). A reply that opens with a thinking tag (`<thought`, `<think`, `<thinking`), which a local model sometimes writes into its reply by mistake, is not said: the harness writes it in the model's journal as a fault, with its first line and its length, tells the model in its next turn that nothing was said, and still runs any tool call in it. An empty reply to your question, or to an urgent line, is counted: three in a row bring the nudge, a fourth the pause, as the same order repeated does; each is in the journal. An empty reply at a plain glass is silence the model chose, and is not counted. A turn may make up to eight tool calls; `answer` and `say` are not counted, so the model's answer is never held to the next glass by the reads before it.

**Standing by.** A stand-by ends the model's turn at once: it is not asked anything more until the stand-by ends (playtest 4's model, told "Standing by until a glass" and asked again, stood by thirteen times in a turn that never closed). The turn that ends it begins by saying so (*You stood by until a glass at ...; it is now ...*). The model may stand by until an event (`eight bells`, `sunset`, `a strain warning`, ...), an interval (`a glass`, `an hour`, `5 minutes`, `ten minutes`), `a notable event` or `an urgent event`. Whatever it stands by for, **an urgent line in the log wakes it at once** (something carried away, taken aback), the line named as the reason; the **notable lines** logged while it stood by come with the turn that wakes it, counted and listed, besides the log as ever. A stand-by is a decision not to be sampled, not a decision to be blind (the owner's ruling, 2026-09-28). **At 1x a glass is half an hour of real time**: for a watcher that speaks every glass, run the clock at `time 30` or `time 60` (a glass in a minute or in thirty seconds), or sail and let the notable events bring its turns.

Other flags of the game: `--lockstep` (section 8), `--consent-records DIR` (where the consent records are read and written; `docs/agents/consent` by default), `--saves DIR` (where the game is saved when a station is released; `saves` by default), `--port 8001` (another port; the doors then need `--game http://localhost:8001`), `--standing-orders data/standing_orders/starter.orders`, `--watcher fake` (the scripted watcher of section 9, in place of a model).

## 3. Claude Desktop

**The configuration file.** In Claude Desktop, open *Settings*, then *Developer*, then *Edit Config*. That opens the folder holding `claude_desktop_config.json`, which on Windows is `%APPDATA%\Claude\claude_desktop_config.json` (type `%APPDATA%\Claude` into the File Explorer address bar to get there). Open it in Notepad and make it read as below, or put the `freesail` entry beside any servers already in `mcpServers` (replacing the first draft's `freesail` entry, which named a ship file):

```json
{
  "mcpServers": {
    "freesail": {
      "command": "py",
      "args": [
        "-m", "freesail.agents.mcp_server",
        "--game", "http://localhost:8000",
        "--model-name", "THE MODEL'S NAME, EXACTLY AS CLAUDE DESKTOP SHOWS IT"
      ],
      "env": {
        "PYTHONPATH": "<the folder you extracted the gate zip into>",
        "PYTHONUTF8": "1"
      }
    }
  }
}
```

- `PYTHONPATH` is the gate folder, for example `"D:/Projects/FreeSail/FreeSail-gate-m4b-3"`, so that the bridge Claude Desktop starts is this gate's. Change it with every gate.
- `--game` is the game's address as it printed it. The bridge holds no game of its own; start the game first.
- `--model-name` is the model you have chosen in Claude Desktop's model menu, written exactly as the menu shows it. The protocol tells the bridge the name of the application but not which model is answering, so the name you give here is what the consent record is kept under. **If you switch models in the menu, change this name and restart Claude Desktop**: the bridge cannot see the switch, and consent is per model.
- `PYTHONUTF8` makes the bridge's messages safe for any character a model writes.

Save the file, then **quit Claude Desktop completely** (the icon by the clock, *Quit*; closing the window is not enough) and start it again. In a new chat the tools menu (the slider icon under the message box) lists `freesail` with ten tools. If it is missing, the bridge's own log is `%APPDATA%\Claude\logs\mcp-server-freesail.log`; its first line is `FreeSail MCP bridge for <the name>, to the game at http://localhost:8000. Waiting for the client on stdio.`, and the last lines say what went wrong (a wrong path in `PYTHONPATH`, most often).

**The first connection.** With the game running in the browser, write in a new chat *"Please connect to FreeSail and read what its harness sends you."* (or choose the prompt `keep_watch` from the *+* menu of the message box, *freesail*). Claude Desktop asks you to allow each tool; *Allow always* for FreeSail's tools saves asking each time. The model's first tool call, whatever it is, is not run: its result is the brief (`Your call to ... was not run: the harness's brief comes first`).

- **With no consent on record** for the name you gave, the brief is the consent brief with the question, and the game's terminal says `FreeSail: The watcher is asked for by <the name>, through the MCP bridge; no consent is on record for it. The consent brief comes first`. The model may ask you questions in the chat; answer them there. It answers the harness with the `answer` tool, beginning *yes*, *yes, with conditions*, or *no*. An answer of *yes, with conditions* with nothing after it is followed by one more question in the answer's own result (*You answered yes with conditions; please state them, ...*), and the second answer decides; the record holds both. The game writes the record at once to `docs/agents/consent/<date>-<the name>.md` and its terminal says so; the record's *Runtime* line names the game, the bridge and Claude Desktop. The answer's result ends with a line for you, *For the owner: the consent record is written (...). You may write to the model here in the chat ...*: this is your turn to ask or say something before you go on, in the chat, which the record does not see unless you paste it in. A **yes** goes straight on: the answer's result carries the station brief and the first turn, and the browser's log says `The watcher takes the station ...`. **Anything else** stops it: every later call is answered "No station is offered in this session", with the reason. A no is not asked again unless you ask on purpose: add `"--ask-again"` to the `args` for one start and take it out after.
- **With a yes on record**, the first call returns the watcher's brief and its first turn, and the browser's log says `The watcher takes the station ...`.

The chat around the consent conversation is in Claude Desktop, not in the record: the game sees only tool calls. If you want the chat kept, copy it into the record under its *Notes*.

**How to play.** Sail in the browser. Ask the model in the chat to keep watch for a while (*"Keep watch for the next few glasses, saying what a sailor would notice."*). It reads what it likes (`readings`, `read_log`, `library`, `state`), then hands its turn back with `say` (a line or two into the log under `[watcher]`) or `stand_by` (above). The call is then **held open until its next turn opens**, and returns it, the first line saying whose turn it is (`Your turn is open: sample at Morning watch, 1 bell (04:30) (the glass).`). While it waits the bridge sends the client a progress note every fifteen seconds (*Waiting for the next turn: 45 seconds so far; standing by until a glass; ...*), which a client shows and which keeps it from giving up on the call. Its lines appear in the browser's log as they are said. Type `ask the watcher how the sails are drawing` in the order box: its turn opens at once, the waiting call returns with your question, and its answer appears in the log as a notable `[watcher] ...` line.

**How long a call is held.** At most an hour of real time by default (`--wait`, in seconds; at most four hours). The owner has seen Claude Desktop hold a live tool call open for many minutes and tens of minutes (2026-09-28), and at 1x a glass is thirty real minutes, so an hour spares the model a string of empty calls. If no turn opens by then, the call returns *Still waiting: this call waited ... and no turn opened.* with since when the model has been standing by (or waiting), until what, and the notable lines logged since, in the log's own words; the model calls `stand_by` again to go on with the same wait, or says something (`say`), which puts its words in the log, ends the stand-by as its own decision and opens its turn at once. **If Claude Desktop cuts long calls whatever the progress** (its log, `mcp-server-freesail.log`, shows the call cancelled, or the model's next result begins *Your call to ... was not run: your last call was cut off by the client*), add `"--wait", "50"` to the `args`: the model then waits in fifty-second calls, each ending with that digest. Report what you see; the default is set from it.

**A call cut off loses nothing.** If the client gives up on a call (its own timeout, or you stop the model) while the bridge is waiting, and the model's turn opens just then, the model's next call returns that turn first (*Your call to stand_by was not run: your last call was cut off by the client before its result reached you, and that result comes first*) and is not itself run, so the model never answers a turn it has not read (playtest 3's lost question). A cut-off wait in which no turn opened is only noted after the next call's result. In the same way, if the model's turn opened while no call of its was waiting (its last call had come back *Still waiting*, and it had gone on in the chat), its next call returns that turn first (*Your call to ... was not run: this turn opened after your last result, and it comes first.*); and what was added to its open turn while it was reading comes with the result of its next call, so nothing the game sent goes unread.

**The token.** The game never sees the text of the chat, only the tool calls. So the token `FREESAIL-OPT-OUT` counts in any argument of any tool call, and the `opt_out` tool is always listed. If you ask the model in the chat to leave, it calls `opt_out` or passes the token on; the game is saved and the station released. This is a limit of the protocol, not a choice.

**When Claude Desktop closes** (or the chat's server is stopped), the bridge releases the station: the watcher is stood down *by the MCP bridge: the client disconnected*, and the game is saved. The game goes on without it.

**A new chat** in the same Claude Desktop session uses the same bridge and the same station; the model in the new chat has not read the brief, so start it with the prompt `brief` (the *+* menu, *freesail*, *brief*), which puts the brief as it stands into the chat.

## 4. Claude Code in the Desktop app

Claude Code reads a file named `.mcp.json` at the top of the folder it is opened on, and the gate folder has one, pointing at the same bridge by its module name, so it works from whichever folder you extracted:

```json
{
  "mcpServers": {
    "freesail": {
      "command": "py",
      "args": [
        "-m", "freesail.agents.mcp_server",
        "--game", "http://localhost:8000",
        "--model-name", "SET THE MODEL'S EXACT NAME HERE"
      ],
      "env": { "PYTHONUTF8": "1" }
    }
  }
}
```

1. **Set the model's name.** Open `.mcp.json` in Notepad and replace `SET THE MODEL'S EXACT NAME HERE` with the model you use in Claude Code, exactly as Claude Code names it (its model menu, or `/model`). Until you do, every call is answered "No station is offered: the bridge was started without the model's name", and no record is written under the placeholder.
2. **Start your game** in the browser (section 2).
3. **Open the gate folder in Claude Code** in the Desktop app (the *Code* tab; choose the folder `<the folder you extracted the gate zip into>`). The first time, Claude Code asks whether to use the MCP servers the project's `.mcp.json` names: allow `freesail`. `/mcp` in the prompt lists it with its tools.
4. **Play** as with Claude Desktop (section 3): ask it to connect and keep watch; the consent brief comes first for a name with no record; sail in the browser; `ask the watcher ...` in the order box. The bridge's two prompts appear as slash commands: `/mcp__freesail__brief` and `/mcp__freesail__keep_watch` (type `/` and look for *freesail* if the form has moved).

This file's shape is Claude Code's project configuration as documented when it was written; if Claude Code does not pick it up, check `claude mcp --help` (or Claude Code's documentation on MCP) for where project servers are kept now, and report it.

## 5. A local model under llama-server

`llama-server` comes with llama.cpp. Take the Windows build for CUDA from the releases page of llama.cpp on GitHub (`ggml-org/llama.cpp`, *Releases*; the zip whose name has `win-cuda` and `x64` in it, and the `cudart` zip beside it if the server complains of a missing CUDA library), unzip it anywhere, and open a terminal in that folder. Then, for a GGUF file on a 4090:

```
llama-server.exe -m C:/models/YOUR-MODEL.gguf --ctx-size 16384 --n-gpu-layers 99 --parallel 1 --jinja --seed 7 --host 127.0.0.1 --port 8080
```

- `-m` the GGUF file. Its name is what the consent record is kept under (the name only, never its folder), so the same weights under another file name are asked again, and a different quantisation is a different model.
- `--ctx-size 16384` the context. The watcher's brief is about 1,630 tokens, the tool definitions about 1,270, the consent brief about 1,480, and each glass's turn about 450 (measured on the frigate at seed 7 for package 28d, the shelf; four characters to a token), and the runner keeps the reply budget of 4,096 free (below), so 16,384 holds the brief and some twenty glasses before the runner starts leaving out the oldest turns; 8,192 holds two or three. A library read now costs what it serves (a section of the primer is a few hundred tokens, a whole chapter up to about 9,710), and a book the model shelves costs its one line from then on. A turn that grew while the model was thinking (things added to it) is longer. If the model does not fit in the card's 24 GB with it, lower this first.
- `--n-gpu-layers 99` puts every layer on the card (any number above the model's layer count means all of them). If the card runs out of memory, lower it: the rest run on the processor, more slowly.
- `--parallel 1` one conversation at a time, so the whole context is the watcher's (the server divides the context among its slots).
- `--jinja` uses the model's own chat template, which is what makes tool calling work. Without it the model cannot call `readings`, `answer` or any tool.
- `--seed 7` the default sampling seed; the runner sends its own with every request when you give it `--seed`.
- `--host 127.0.0.1 --port 8080` only this machine can reach it; the runner's default address.

These are the flags as llama.cpp's server documents them at the time of writing; if one is refused, `llama-server.exe --help` lists the current names. When it is up, `http://127.0.0.1:8080/props` in a browser shows what it loaded (`model_path`). A thinking model's reasoning comes back apart from its reply under llama-server's default reasoning format; leave that as it is (see section 12).

**The runner.** Start your game in the browser (section 2). Then, in a second terminal in the gate folder:

```
py -m freesail.agents.local --game http://localhost:8000 --endpoint http://127.0.0.1:8080 --seed 7
```

It reads which weights the server loaded and says so (`The model server serves <the file's name>.`), then asks the game for the watcher's station under that name. With no record for them, the consent brief comes first; the runner's terminal shows what the model writes (`model> ...`), and when it writes something without answering, the run waits at `owner>` for your reply (type it; a blank line sends it; a blank reply stops the step without a record). An answer of *yes, with conditions* with nothing after it is asked for the conditions once more. **After the answer, you have a turn at `owner>`** before the record closes: the runner shows the answer (`The model has answered (yes): ...`), and anything you type goes to the model, which may reply once, and both are kept in the record; a blank line at once closes the record. Its answer is recorded by the game in `docs/agents/consent/`. A yes goes on to the station; anything else stops the run with the reason and exit code 5.

At the station, the runner keeps going on its own: it asks the game for the watcher's next turn, sends it to the model, and hands the model's reply back, and prints a line for each turn (`== Morning watch, 1 bell (04:30): a turn, the glass ==`) and what the model says (`model> ...`). You play in the browser: the watcher's lines are in its log, and `ask the watcher ...`, `show the watcher's journal`, `stand down the watcher` go in the order box. When the station is released (the token, `stand down the watcher`, the welfare stop), the runner says so and ends with exit code 3.

Other flags: `--session test` (the brief says it is a test session rather than play), `--temperature 0.7`, `--seed 11` (the sampling seed), `--ctx 16384` (the context to budget against, if the server does not report it), `--max-reply 4096` (the reply budget, below), `--model NAME` (where the server serves several), `--ask-again`.

**The reply budget and the timeout.** Every request to the model server carries a reply budget, `max_tokens`, 4,096 tokens unless `--max-reply` says otherwise (the owner's ruling, 2026-09-28: generous, so that a long answer, a journal note or a thinking model's reasoning is never cut; a runaway is still stopped within about a minute and a half on a 4090). A request that has not answered in ten minutes (`--request-timeout` changes it) is given up: the runner prints `The model server did not answer within 600 s; the sample is left open. (1 of 3; asking again)`, reads the game again (anything that happened meanwhile, your question included, is added to the model's open turn) and asks again. Three failures in a row stand the watcher down with the reason, and the game saves. The timeout is long on purpose: a thinking model writing a long note can run to the whole reply budget, and a 27B model at four bits on a 4090 takes three minutes and more to generate 4,096 tokens after reading a long prompt; playtest 6 (Qwen3.8 27B) lost its farewell to a three-minute timeout. The budget bounds a reply; the timeout is only for a server that has hung.

**The context check.** Before it asks the game for the station, the runner asks the model server what context it gives the model (`/props` for llama-server; `/api/ps`, or the model's `num_ctx` from `/api/show`, for Ollama) and measures what the watcher needs (the brief and the tool definitions, counted at four characters a token, a turn, and the reply budget). If the context is smaller it stops before anything is asked, saying both numbers and how to raise it; otherwise it prints `The context is enough: ...`. If the server does not say (an Ollama model not yet loaded), it says so, and `--ctx` is your word for it.

**The context budget, measured.** How large a `--ctx-size` your card holds depends on the model: its weights, and its cache of keys and values, which grows with every token of the context. `tools/context_budget.py` reads the model file's header and works it out:

```
py tools/context_budget.py C:/models/YOUR-MODEL.gguf --vram 24 --headroom 1.5
```

It prints the model's layers, key-value heads and head width, the weights' size (the file on disk), the cache a token at f16 (llama-server's default) and at q8_0 (`--cache-type-k q8_0 --cache-type-v q8_0`, about half, which llama.cpp gives the value cache only with flash attention, `-fa`), and the largest `--ctx-size` that fits: the card's memory (`--vram`, in GiB; a 4090 is 24) less the weights and less a headroom you set (`--headroom`, 1.5 GiB by default, for the CUDA context, llama.cpp's working buffers and the desktop). The formula is in the script's opening words with its sources: two tensors a layer, times the key-value heads, times the head width, times two bytes at f16. A model with a sliding window (some of its layers attend only to the last few thousand tokens) keeps those layers' cache small unless llama-server is started with `--swa-full`; the script prints the figure with every layer at the whole context (an upper bound) and, where the header says which layers slide, the figure with those at their window, which is the one to go by. Where the header gives the window but not the layers, it says so, and `--swa-every N` (every N-th layer attends to the whole context, from the model's card) gives it. If the weights and the headroom alone do not fit, it says so with the numbers.

The table, one row for each model with a consent record, filled from the script (and the last column from use):

| Model (the consent record's name) | Layers, KV heads, head width | Weights | Cache a token, f16 / q8_0 | Largest `--ctx-size`, f16 / q8_0 | Observed in use |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

**The check.** The owner's observed range for the 26B and 27B models on the 4090 is **80k to 110k tokens** of context in practice (2026-09-28, anecdotal, from Hermes Agent sessions). The script's figures are to be checked against it: a figure far below the range probably means the sessions ran with a q8_0 cache or a sliding window the script was not told of, and one far above it that the headroom is too small; say which in the last column.

**The shelf: what the model keeps in its context.** The library is served in pieces with their sizes, so a local model reads what it needs and not a chapter at a time: `library()` lists the topics and what each costs, `library(topic='primer 3')` a chapter's sections with theirs, `section='reefing'` one section, `find='goose-wing'` the paragraphs that match. Every read is a *book* with a number (`primer 3, reefing, opened 04:10; book 7`), and the model puts it back with `shelve`: from its next request the runner sends that result as its one line (`You read primer 3, reefing, at 04:10; shelved (book 7). library(...) opens it again.`), so the pages are really gone from the model's context. A book left open goes back by itself after three more of the model's turns, and the next turn says so. Nothing leaves the library: any book opens again on request, and the brief tells the model its journal is where to keep what it took from a page.

If the model server is not running, the runner says `Could not reach the model server at http://127.0.0.1:8080: the connection was refused ...` and stops. If the game is not running, it says `Could not reach the game at http://localhost:8000 ...` and stops. If the model server fails in the middle of a watch, the runner prints why and releases the station, and the game saves.

## 6. Ollama

Ollama speaks the same language on its own port, so the runner works against it unchanged; it is the quicker look, and `llama-server` is the exact one. The model's name is the one `ollama list` shows:

```
py -m freesail.agents.local --game http://localhost:8000 --endpoint http://127.0.0.1:11434 --model NAME-FROM-OLLAMA-LIST
```

The consent record is kept under that name with the digest Ollama reports for it, so a re-pulled or re-quantised model is asked again.

**The context.** A default Ollama install gives a model a small context and cuts the conversation to it without saying so. The runner's context check (section 5) catches it before anything is asked. To raise it, set `OLLAMA_CONTEXT_LENGTH` (for example `16384`) before starting `ollama serve`, or put a `PARAMETER num_ctx 16384` line in the model's Modelfile; with the context set large (the owner's Ollama runs every model at 262,144 tokens) the check passes and says so.

**A request that never ends.** If the runner seems stuck while the card stays busy for minutes on end, it is a **runaway generation**: the model has fallen into repeating itself and, with no limit, generates without end, since Ollama's own default reply length is unlimited. Playtest 4 was one: the harness of that build returned each `stand_by` as a tool result and asked the model again (a turn ended only on a reply with no tool call), so the model stood by thirteen times in a turn that never closed, and the last of those requests ran to 76,674 tokens before Ollama gave it up at ten minutes; the captain's questions and the glass meanwhile went into that open turn and were never answered. Now a stand-by ends the turn at once (section 2, *Standing by*), and the runner's reply budget (`--max-reply`, 4,096 tokens by default) bounds any runaway within about a minute and a half on a 4090; its timeout gives up a request after ten minutes, says so (`The model server did not answer within 600 s; the sample is left open.`) and asks again. Two things to check:

- `ollama ps` in a terminal: the model loaded, its context (`CONTEXT`), and whether it is on the card (`PROCESSOR`, `100% GPU`).
- Ollama's server log, `%LOCALAPPDATA%\Ollama\server.log`: its request lines (`[GIN] ... | POST "/v1/chat/completions"`) give each request's status and how long it took, so a runaway shows as a request of minutes where the others took seconds, and near it a cancelled request with a large `n_tokens`; a line with `truncating input prompt` means instead that the context is too small for the conversation (raise it, above).

## 7. The console instead of the browser

The console hosts the same connection for the doors on a port of its own:

```
py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180 --agents-port 8000
```

It prints `A model's door connects to http://localhost:8000`. The doors connect with the same `--game http://localhost:8000` (so the configurations above are unchanged, as long as the browser game is not running on the same port). `state` prints the station's line (`The watcher (<name>, through the local runner): stationed; its turn is open.`), and the watcher's lines print in the log as every line does. The console's own flags `--lockstep`, `--consent-records DIR` and `--saves DIR` are as the browser game's.

## 8. `--lockstep`: the game waits for the model

Either game takes `--lockstep`: then the clock **holds while the model has its turn** and runs on when it hands the turn back. It is for testing at 1x (the model is never behind), and for competitive play later. The instruments' *Clock* row says `running at 1x, waiting for the watcher` while it waits, and `tick 600` in the order box stops at the watcher's next turn. Without `--lockstep`, the game does not wait: what happens while the model thinks is added to its turn. The REPL and the tests always run in lockstep.

## 9. Practice without a model

- **The scripted watcher.** `py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 180 --watcher fake` stations a watcher played by a small script in the game itself: a line from the readings at each glass and each notable event, and an answer to `ask the watcher ...`. Everything else (the log, the order box, `stand down the watcher`, the journal, the save) is as with a model.
- **The REPL: typing the replies.** `py -m freesail.agents.repl data/ships/frigate-36.yaml --seed 7 --human` puts you at the watcher's station of a game of its own, in the terminal: each turn is shown as text and you type the reply at `reply>` (free text; a tool call on a line beginning `>`, such as `> answer text="Yes."` or `> stand_by until="eight bells"`; a blank line sends). `--model-name "a name"` instead of `--human` is a language model at the terminal, and it meets the consent brief first (with your turn at `owner>` after its answer, as at the runner); to practise the consent step without writing into the real records, add `--records saves/consent-practice`. The build session (a language model at a terminal) plays through this door; its turn mode (`--turn`) is described in `freesail/agents/repl.py`.

## 10. Where things go

| What | Where |
|---|---|
| Consent records | `docs/agents/consent/<date>-<weights>.md` in the gate folder, written by the game (or where its `--consent-records` says): the brief as sent, every turn verbatim, the answer, the verdict and any conditions quoted, and a *Runtime* line naming the game, the door and its client. A second record the same day gets `-2`. The newest record for a name decides. Copy new records back into the repository with the gate report. |
| Saves | `saves/freesail-seed<seed>-tick<tick>.json` in the gate folder (git ignores this folder), or where the game's `--saves` says. A save is written whenever a station is released: the token, `opt_out`, a stand-down, the door closing. The game's terminal names the file and the log's digest at that moment. |
| Journals | In the save (`agent_journals`), shown by `show the watcher's journal`, and written again by a replay. |
| The log | The browser and the console show the watcher's lines under `[watcher]`; the save holds everything to replay it, the model's replies and the moments they came included. |

## 11. How to stop

- **`stand down the watcher`** in the order box (or at the console). The game is saved, the journal says why. The door is told at its next call.
- **The token.** The model writes `FREESAIL-OPT-OUT` anywhere in a reply (over MCP: in any tool argument, or calls `opt_out`). The game is saved and the station released at once, whatever else the reply said, whether or not it was the model's turn.
- **Close the door.** Quit Claude Desktop, close Claude Code, or press Ctrl-C in the runner's terminal: the door releases the station, the game saves, and you sail on.
- **Stop llama-server** with Ctrl-C in its own terminal: the runner then releases the station, saying the model server could not be used.
- If the harness sees the watcher stuck (the same order three times with nothing changing, or its turn left open with no reply for a watch of ship's time), it nudges, then pauses and asks you in the log and in the instruments (`resume the watcher` or `stand down the watcher`), and only if nobody answers within a watch of ship's time or ten real minutes does it stand the watcher down itself.

## 12. What the harness does not do

- **Over MCP the chat is invisible to the game.** The token counts only in tool calls; the consent record holds what the game saw; the bridge cannot tell which model the chat uses (you name it).
- **Over MCP (and at the REPL) shelving cannot take pages back.** The conversation is the client's (or what the terminal printed), so `shelve` notes the book, the game never shows its pages again, and the result says plainly that the client keeps its own copy. Claude's own window keeps itself; the journal carries the habit.
- **Reasoning is not scanned.** A model server that returns a thinking model's reasoning apart from its reply (llama-server's default) keeps it out of the token scan: thinking about the token does not use it, writing it does. The consent brief says so, and the consent record keeps the reasoning verbatim in a section of its own. If the server is set to put the reasoning inside the reply instead, it is scanned with the reply.
- **The game does not wait** for a model unless you start it with `--lockstep`. A slow model's turn grows while it thinks; nothing is lost, and the watcher is judged by ship's time, not by how long it takes to type.
- **Every stop replays.** The model's replies are kept with the moment each came (the tick and how many of your orders came before it), and so are the stops that come from outside (a door closing, the token sent out of turn, the ten real minutes): a replay of the save makes them at the same moments and gives the same log.
