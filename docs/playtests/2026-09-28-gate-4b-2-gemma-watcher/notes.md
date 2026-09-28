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

## The likely cause

Ollama loads a model with a small default context window unless told otherwise; the
brief is about 1,150 tokens and the tool definitions 900, so the window overflows within
a few turns and Ollama drops the oldest text, which is the brief. Repetition and runaway
generation follow. `Harness.md` mentioned raising Ollama's context; nothing enforced it.
To confirm on the owner's machine: `ollama ps` (the loaded context size) and the server
log (`%LOCALAPPDATA%\Ollama\server.log`, "truncating input prompt").

## Follow-ups (package 28c, item 9)

A successful `stand_by` ends the turn at once on every door; the runner puts a reply
budget and a per-request timeout on every call and retries at the next sample rather
than standing down on one timeout; the runner refuses to station a model whose loaded
context is smaller than the brief and tools need, and says how to raise it; `Harness.md`
says all of it.
