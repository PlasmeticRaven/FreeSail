# Playtest 2: the first watcher, a Claude Sonnet 5 session through Claude Desktop, gate 4b build

The first session with a real language model at a station. `save.json` is the game the
harness wrote when the model left by the `opt_out` tool at 07:05 ship's time (the ship
file's path made relative for the repository); it holds the journal of orders, the
agent's transcript (every reply, tool calls and all) and the watcher's journal. The
owner played through the MCP door as the gate 4b report describes; the consent
conversation for these weights is the record under `docs/agents/consent/`.

## The scenario and seed

Frigate, seed 7, the `gate-m4b` release, the default scenario: 04:00 on 1 June 1805,
wind north 15 knots, head south, at rest. The watcher stationed at tick 0 in a play
session with the owner as captain. `set plain sail` at 05:00; one question asked at
05:05; the model left at 07:05 at the owner's request, to test the opt-out path.

## What happened

- **The model's first samples** read the state, the library's contents, the log and the
  ship's names, tried `set the fore topsail` to see the refusal ("confirmed the watcher
  has no order authority", it wrote in its journal), and said a line in a sailor's voice.
- **At one bell it noticed the physics.** "She's making three knots over the ground, with
  not a stitch of canvas bent nor set. No sailor lets that pass without remark." Asked by
  the owner whether three knots under bare poles was unreasonable, it answered from first
  principles: windage scales near the square of the wind, a ship drifts a knot or so under
  bare poles in a gale, so at fifteen knots bare poles should buy her a few tenths, not
  three. It then stood by until eight bells. **Recorded as an open item**: the frigate's
  windage under bare poles with the wind aft looks high; to measure against the sources
  (Luce on drift under bare poles; the hull and rig windage in `physics/`).
- **The opt-out** by the tool, with a reason, saved the game and journaled the exit; the
  station was released. The model then tried `library` and `say` after leaving, at the
  owner's request, and was refused as a released station (the owner's report; not in
  the save, which is right).

## What the owner found

The door's shape, not the harness, is the finding (owner, mid-session): the World ran
inside the MCP server, so the game could be seen only through the tool calls' readouts
in the Claude Desktop chat, and the captain's orders went through a prompt menu ("really,
really unwieldy"). The owner pictured, rightly, playing as before in the console or the
browser window with the model alongside, as QudBridge attaches to Caves of Qud. The lead's
spec §13 had put the World in the wrong process. Package 28b turns the doors into clients
of the running game; gate 4b is re-cut after it.

## Follow-ups raised

1. The doors attach to the running game (package 28b); the `captain` prompt goes away.
2. Windage under bare poles: measure and tune against the sources.
3. The consent record for these weights belongs in the repository.
