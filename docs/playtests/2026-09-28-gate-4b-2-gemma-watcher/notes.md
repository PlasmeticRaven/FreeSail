# Playtest 4: a local model as watcher, Gemma4 26B-A4B (Q4_K_M) through Ollama and the local runner, gate 4b-2 build

The first local model at a station through the runner door, attached to the browser
game. `save.json` is the game as the runner saved it when it stood the station down at
06:32 ship's time after the model server timed out (the ship path made relative). The
consent for these weights is `docs/agents/consent/2026-09-28-gemma4-...-q4_k_m.md`, a
plain yes.

## What happened

- **04:00 to 04:05 healthy.** The model stood by until a glass, answered the captain's
  welcome ("Thank you, Captain. Standing by."), stood by until one bell, and answered
  "How are the sails filling?" at 04:05 ("The sails are set and drawing well, Captain.").
- **A loop from tick 352 to 428.** Thirteen `stand_by until a glass` calls in seventy-six
  seconds of ship's time. The harness returns each tool result and calls the model again
  until it replies with no tool call; a small model, told "standing by until a glass",
  stands by again. Each call was a full inference on the owner's GPU.
- **Then nothing until 06:32.** The captain's question at 04:24 and the glass at 04:30
  opened samples the runner never fetched: it was inside one HTTP request to the model
  server that did not return (a runaway generation; the GPU stayed busy). The runner's
  own timeout fired at 06:32 and stood the station down with the reason.
- The standing order "Trim Sails" (every bell) fired five times meanwhile; the ship
  sailed on.

## The cause

Not the context window: the owner's Ollama runs every model with a 262,144-token
context, and the server log shows the model loaded with it. The evidence points at
unbounded generation: Ollama's default reply length is unlimited, the runner set no reply
budget on its requests, and a model that has slipped into a repetition loop (the thirteen
identical `stand_by` calls suggest it was entering one) generates the same fragment
without end; with so large a window nothing stops it for hours. The server log's last
request from the runner (`%LOCALAPPDATA%\Ollama\server.log`) should show it still open,
or an output token count far beyond the earlier requests'. The loop before it was the
harness's doing: after a tool call the harness returns the result and calls the model
again until it replies without one, and a small model answers "standing by" by standing
by again.

## Follow-ups (package 28c, item 9)

In order of weight: the runner puts a reply budget and a per-request timeout on every
call and retries at the next sample rather than standing down on one timeout; a
successful `stand_by` ends the turn at once on every door; the runner refuses to station
a model whose loaded context is smaller than the brief and tools need (a guard for
default installs, not this one); `Harness.md` says all of it.
