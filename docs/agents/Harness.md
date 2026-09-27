# The harness: connecting a model to FreeSail

How to put a language model at the watcher's station, for the owner, on Windows, typing `py`. Nothing here needs programming; every command is typed in a terminal (PowerShell or Command Prompt) in the FreeSail folder unless it says otherwise.

There are three doors to the same harness (`freesail/agents/`), and every one of them puts the **consent brief** (`ConsentBrief.md`) in front of the station the first time it meets a model:

| Door | For | Started by |
|---|---|---|
| The MCP server | Claude Desktop | Claude Desktop itself, from its configuration file |
| The local runner | a model on this machine under `llama-server` (or Ollama) | `py -m freesail.agents.local ...` |
| The REPL | you, or anyone typing replies by hand, or the build session | `py -m freesail.agents.repl ...` |

## 1. Install once

In the FreeSail folder:

```
py -m pip install -e ".[dev,server,agents]"
```

It ends with `Successfully installed ...`. The `agents` part brings the Python MCP SDK (the server Claude Desktop talks to) and `httpx` (what the local runner speaks HTTP with). Check it with `py -m pytest tests/test_consent.py tests/test_mcp_server.py tests/test_local_runner.py`, which proves every door against a scripted model and a fake server, with no model and no network.

## 2. Claude Desktop

**The configuration file.** In Claude Desktop, open *Settings*, then *Developer*, then *Edit Config*. That opens the folder holding `claude_desktop_config.json`, which on Windows is `%APPDATA%\Claude\claude_desktop_config.json` (type `%APPDATA%\Claude` into the File Explorer address bar to get there). Open it in Notepad and make it read as below, or add the `freesail` entry beside any servers already in `mcpServers`:

```json
{
  "mcpServers": {
    "freesail": {
      "command": "py",
      "args": [
        "-m", "freesail.agents.mcp_server",
        "C:/Users/YOU/FreeSail/data/ships/frigate-36.yaml",
        "--seed", "7", "--wind", "0,15", "--heading", "180",
        "--model-name", "THE MODEL'S NAME, EXACTLY AS CLAUDE DESKTOP SHOWS IT"
      ],
      "env": { "PYTHONUTF8": "1" }
    }
  }
}
```

- `C:/Users/YOU/FreeSail` is where your FreeSail folder is. Use forward slashes, or double every backslash (`C:\\Users\\...`); a single backslash breaks the JSON. The ship file's path must be whole, because Claude Desktop does not start the server in the FreeSail folder.
- `--model-name` is the model you have chosen in Claude Desktop's model menu, written exactly as the menu shows it. The protocol tells the server the name of the application (Claude Desktop) but not which model is answering, so the name you give here is what the consent record is kept under. **If you switch models in the menu, change this name and restart Claude Desktop**: the server cannot see the switch, and consent is per model.
- `py` is the Python launcher that came with Python; `-m freesail.agents.mcp_server` runs the server from the installed FreeSail. A save can stand in place of the ship file (a `.json` from `saves/`), and `--standing-orders C:/Users/YOU/FreeSail/data/standing_orders/starter.orders` gives the starter routines.
- `PYTHONUTF8` makes the server's messages safe for any character a model writes.

Save the file, then **quit Claude Desktop completely** (the icon by the clock, *Quit*; closing the window is not enough) and start it again. In a new chat the tools menu (the slider icon under the message box) lists `freesail` with its ten tools. If it is missing, the server's own log is `%APPDATA%\Claude\logs\mcp-server-freesail.log`; the last lines say why (a wrong path, most often).

**The first time.** Ask the model in the chat to connect to FreeSail and read what the harness sends. Its first tool call, whatever it is, is not run: its result is the consent brief with the question (`Your call to ... was not run: the harness's brief comes first`). Claude Desktop asks you to allow each tool; *Allow always* for FreeSail's tools saves asking each time. The model may ask you questions in the chat; answer them there. It answers the harness with the `answer` tool, beginning *yes*, *yes, with conditions*, or *no*. The record is written at once to `docs/agents/consent/<date>-<the name you gave>.md`, and the server's log says so.

- A **yes** goes straight on: the answer's result carries the station brief and the first sample, and the model is the watcher from then on.
- **Anything else** stops the run: every later call is answered with "No station is offered in this session", and the log says why. Read the record; the conditions are quoted in it. A no is not asked again unless you ask on purpose: add `"--ask-again"` to the `args` for one start and take it out after.
- The chat around the conversation is in Claude Desktop, not in the record: the server sees only tool calls. If you want the chat kept, copy it into the record under its *Notes*.

**After that.** With a yes on record the first tool call returns the watcher's brief. The rhythm is this: the model reads what it likes (`readings`, `read_log`, `library`, `state`), then hands the floor back with `say` (a line or two into the log under `[watcher]`, or nothing) or `stand_by` (until a bell, an event, a glass, an hour, a watch). The game then runs on to the watcher's next turn (the next glass, a notable event, the end of the stand-by) and the call returns what happened. **The game never runs on the clock of the wall**: it waits for the model at each turn. One call runs at most two hours of ship's time, so a long stand-by comes back and goes on when the model calls `stand_by` again. Ask it to keep watch for a few glasses and it will call `say` once a glass.

**You are the captain** through the prompt menu of the message box (the *+* button, then *freesail*; the place may move between versions): the prompt `captain` takes an order (`ask the watcher how the sails are drawing`, `stand down the watcher`, `resume the watcher`, `show the watcher's journal`, `set the jib`, `state`, `log 20`) and puts the game's answer into the chat. An order given while the watcher has the floor waits until it hands the floor back, so that a replay of the save gives the same log; the message says so, and the watcher's next `say` or `stand_by` brings it. `stand down the watcher` is carried out at once. The prompt `brief` puts the harness's brief into the chat.

**The token over MCP.** The server never sees the text of the chat, only the tool calls. So the token `FREESAIL-OPT-OUT` counts in any argument of any tool call, and the `opt_out` tool is always listed. If you type the token into the chat, the game does not see it until the model passes it on or calls `opt_out`; the brief tells the model so. This is a limit of the protocol, not a choice.

**When Claude Desktop closes,** a manned station is stood down and the game saved to `saves/` in the FreeSail folder.

## 3. A local model under llama-server

`llama-server` comes with llama.cpp. Take the Windows build for CUDA from the releases page of llama.cpp on GitHub (`ggml-org/llama.cpp`, *Releases*; the zip whose name has `win-cuda` and `x64` in it, and the `cudart` zip beside it if the server complains of a missing CUDA library), unzip it anywhere, and open a terminal in that folder. Then, for a GGUF file on a 4090:

```
llama-server.exe -m C:/models/YOUR-MODEL.gguf --ctx-size 16384 --n-gpu-layers 99 --parallel 1 --jinja --seed 7 --host 127.0.0.1 --port 8080
```

- `-m` the GGUF file. Its name is what the consent record is kept under (the name only, never its folder), so the same weights under another file name are asked again, and a different quantisation is a different model.
- `--ctx-size 16384` the context. The watcher's brief is about 1,150 tokens, the tool definitions about 900, the consent brief about 1,500, and each glass's sample about 450 (measured on the frigate at seed 7; four characters to a token), so 16,384 holds the brief and some twenty glasses before the runner starts leaving out the oldest turns; 8,192 holds about eight. If the model does not fit in the card's 24 GB with it, lower this first.
- `--n-gpu-layers 99` puts every layer on the card (any number above the model's layer count means all of them). If the card runs out of memory, lower it: the rest run on the processor, more slowly.
- `--parallel 1` one conversation at a time, so the whole context is the watcher's (the server divides the context among its slots).
- `--jinja` uses the model's own chat template, which is what makes tool calling work. Without it the model cannot call `readings`, `answer` or any tool.
- `--seed 7` the default sampling seed; the runner sends its own (`--sampling-seed`, else the game's seed) with every request.
- `--host 127.0.0.1 --port 8080` only this machine can reach it; the runner's default address.

These are the flags as llama.cpp's server documents them at the time of writing; if one is refused, `llama-server.exe --help` lists the current names. When it is up, `http://127.0.0.1:8080/props` in a browser shows what it loaded (`model_path`). A thinking model's reasoning comes back apart from its reply under llama-server's default reasoning format; leave that as it is (see *What the harness does not do*, below).

**The runner.** In a second terminal, in the FreeSail folder:

```
py -m freesail.agents.local data/ships/frigate-36.yaml --endpoint http://127.0.0.1:8080 --seed 7 --wind 0,15 --heading 180
```

It reads which weights the server loaded and says so. With no record for them, the consent brief comes first, in this terminal: you see what the model writes (`model> ...`). When it writes something without answering, the run waits at `owner>` for your reply (type it; a blank line sends it; a blank reply stops the step without a record). Its answer is recorded in `docs/agents/consent/`. A yes goes on to the station; anything else stops the run with the reason and exit code 5.

Then the console opens with the model at the watcher's station, in **lockstep**: the game waits at each of its turns while the model answers, however long that takes. You are the captain at the prompt, as in the ordinary console: `tick 1800` runs a glass (the watcher speaks at the glass and at notable events), `go` runs the clock, `ask the watcher how the sails are drawing`, `show the watcher's journal`, `stand down the watcher`, `quit`. Its lines appear in the log under `[watcher]`.

Other flags: `--session test` (the brief says it is a test session rather than play), `--ticks 3600` (run that many seconds of ship's time without the console, then stand down and save), `--temperature 0.7`, `--sampling-seed 11`, `--ctx-size 16384` (to budget against, if the server does not report it), `--standing-orders data/standing_orders/starter.orders`, `--save PATH`, `--ask-again`. A save (`saves/....json`) can stand in place of the ship file to go on from it.

If the server is not running, the runner says `Could not reach the model server at http://127.0.0.1:8080: the connection was refused ...` and stops. If it fails in the middle of a passage, the watcher is stood down with a save and the reason is printed.

## 4. Ollama

Ollama speaks the same language on its own port, so the runner works against it unchanged; it is the quicker look, and `llama-server` is the exact one. The model's name is the one `ollama list` shows:

```
py -m freesail.agents.local data/ships/frigate-36.yaml --endpoint http://127.0.0.1:11434 --model NAME-FROM-OLLAMA-LIST --seed 7
```

The consent record is kept under that name with the digest Ollama reports for it, so a re-pulled or re-quantised model is asked again. Ollama chooses a small context by default and cuts the conversation to it without saying so: give the model a larger one (a `PARAMETER num_ctx 16384` line in a Modelfile, or the `OLLAMA_CONTEXT_LENGTH` setting in newer versions; Ollama's documentation says which) and tell the runner with `--ctx-size 16384`.

## 5. The REPL: typing the replies

The REPL shows each sample as text and takes the reply typed at `reply>`: free text on its own lines, a tool call on a line beginning `>`, and a blank line to send (`> answer text="Yes."`, `> stand_by until="eight bells"`). Every run says who is at the terminal:

```
py -m freesail.agents.repl data/ships/frigate-36.yaml --seed 7 --human
py -m freesail.agents.repl data/ships/frigate-36.yaml --seed 7 --model-name "THE MODEL'S EXACT NAME"
```

`--human` is a person, with no consent step. `--model-name` is a language model, and it meets the consent brief first, like every other door; the record says its runtime was the REPL. The build session (a language model at a terminal) plays through this door with `--model-name`, and its turn mode (`--turn`, one reply per call, described in `freesail/agents/repl.py`) runs the consent conversation the same way: a question it asks stops the call with exit code 4 until your reply comes with `--owner-reply FILE`.

To practise the consent step without writing into the real records, point it elsewhere: `--records saves/consent-practice`.

## 6. Where things go

| What | Where |
|---|---|
| Consent records | `docs/agents/consent/<date>-<weights>.md`: the brief as sent, every turn verbatim, the answer, the verdict and any conditions quoted. A second record the same day gets `-2`. The newest record for a name decides. |
| Saves | `saves/freesail-seed<seed>-tick<tick>.json` in the FreeSail folder (git ignores this folder), or where `--save` says. A save is written whenever a station is released: the token, a stand-down, the end of a run. |
| Journals | In the save (`agent_journals`), shown by `show the watcher's journal`, and written again by a replay. |
| The log | The console and the browser show the watcher's lines under `[watcher]`; the save holds everything to replay it. |

## 7. How to stop

- **`stand down the watcher`**: at the console, or through the `captain` prompt in Claude Desktop. The game is saved, the journal says why.
- **The token.** The model writes `FREESAIL-OPT-OUT` anywhere in a reply (over MCP: in any tool argument, or calls `opt_out`). The game is saved and the station released at once, whatever else the reply said.
- **Ctrl-C** in the runner's terminal, or `quit` at its console: the watcher is stood down and the game saved.
- **Quit Claude Desktop**: the same, for the MCP server.
- **Stop llama-server** with Ctrl-C in its own terminal (the runner then stands the watcher down, saying the server could not be reached).
- If the harness sees the watcher stuck (the same order three times with nothing changing, or silence for a watch), it nudges, then pauses and asks you (`resume the watcher` or `stand down the watcher`), and only if nobody answers within a watch of ship's time or ten real minutes does it stand the watcher down itself.

## 8. What the harness does not do

- **Over MCP the chat is invisible to the game.** The token counts only in tool calls; the consent record holds what the harness saw; the server cannot tell which model the chat uses (you name it). The ten real minutes of an unanswered pause are measured when the model next calls, since the server never acts on its own.
- **Reasoning is not scanned.** A model server that returns a thinking model's reasoning apart from its reply (llama-server's default) keeps it out of the token scan: thinking about the token does not use it, writing it does. The consent brief says so, and the consent record keeps the reasoning verbatim in a section of its own. If the server is set to put the reasoning inside the reply instead, it is scanned with the reply.
- **A stop the door makes itself** (Claude Desktop closing, the runner's `--ticks` spent, Ctrl-C, ten real minutes of an unanswered pause, a model leaving by the token while paused over MCP) is in the save that is written at that moment, but a replay of the save does not repeat it: the replay ends with the watcher still at its station, since the stop was not an order and not a reply. The captain's `stand down the watcher` and the token in a reply are replayed.
