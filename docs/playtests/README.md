# The playtest form

The report the owner fills after a playtest: for gate 4c (spec M4 §22) and for every
playtest after. The form is the milestone 5 input. It asks for the owner's words; the
build session may draft from the save and the log, but anything it drafts is marked as
drafted and the owner amends it.

## Where a record goes

A folder `docs/playtests/<date>-<gate or occasion>-<who is at the stations>/` holding:

- `notes.md`: this form, filled.
- `save.json`: the game's save (the console's `save`, the browser's `save PATH` or
  `/api/save`, or the save a station wrote on leaving). A save is the seed, the scenario
  (the weather script with it), every order and driver's line in the order given, the
  standing orders, and each station's transcript and journal, so a replay rebuilds the
  day. Make the ship file's path relative (`data/ships/...`) before committing it.
- Anything else worth keeping: the log as the viewer served it (`/api/log?limit=5000`),
  a model's own account after the session (as playtest 3's
  `sonnet-5-post-test-notes.txt`), a screenshot.

## The form

Copy the headings into `notes.md` and answer under each. A heading with nothing to say
says so in a line; an empty heading is information too.

### 1. The scenario, the seed and the build

- The scenario (`--scenario data/scenarios/<name>.yaml`, or the ship, `--wind` and
  `--heading`), the seed, and the build (the gate's release name, or the commit).
- The driver (console or browser) and its flags; the stations manned and through which
  door (`--watcher fake`, Claude Desktop, Claude Code, the local runner with the model's
  file name), and the consent record for each model.
- The ship's time the session covered, and the compressions played at.

### 2. What happened, in the owner's words

The day as the owner saw it, in order, with the ship's times from the log. What the ship
did, what the standing orders did, what the weather did, what carried away or did not.

### 3. What the owner ordered, and why

The orders given at the prompt and the standing orders written or belayed, with the
reason for each: a sailor's reason ("the wind was freshening"), a test ("to see the
refusal"), or curiosity. The save has the orders; this section has the why.

### 4. What the owner wished to say and could not

Every order refused that the owner meant, and what was meant by it: a sailor's word the
vocabulary lacks, a sentence the grammar will not take, a thing the ship cannot do yet.
The refusals are in the log; list them with what they should have done.

### 5. What the watcher (or any model at a station) said

- Useful: a line that told the owner something true and timely.
- Useless: a line with nothing in it, or a line said too often.
- Wrong: a number, a word or a judgement a sailor would correct.

Quote the lines with their ship's times. Say what the model was asked and what it
answered. If a model stood by, paused, was nudged or left, say when and why.

### 6. How the day felt at each compression

For each speed played (1x, 10x, 60x, 300x): could the owner follow the ship, read the
log, and give an order in time? At 60x and above the log rolls up by the hour: did the
roll-up keep what mattered and drop what did not? Was an alarm eased to 1x when it should
have been, and was it easy to speed up again?

### 7. Any number a sailor would call wrong

A speed, a heel, a leeway, a strain, a time an evolution took, a wind strength's name:
the number, where it was seen (the log, the instruments, a model's line), and what a
sailor would expect, with a source if there is one.

### 8. How the setup went

The install, the configuration and the doors (spec M4 §24 item 6): what the owner had to
type, copy or edit to start the game and attach each door, what failed on the way, and
what should have been one step. Name the files touched (the Claude Desktop configuration,
`.mcp.json`, the `llama-server` command line) and where each lives.

### 9. What to keep from the model's own account

If a model at a station was asked about the session afterwards (as playtest 3's), what in
its account is a finding (a fault it hit, a word it wanted, a wait that was too long), what
is its preference, and what is only its politeness. Keep its words in a file of their own;
this section says which of them to act on.

### 10. Follow-ups

The owner's and the build session's list of what to change, each one line, in order of
weight. The lead turns these into packages.

## The records so far (the form's precedents)

Each predates the form or was its first use; their headings are the form's raw material.

1. `2026-09-27-gate-3b/`: the frigate under all sail at 60x, the owner alone. The first
   record: what was said and could not be (the refused orders grouped, section 4), and the
   leeway from a standing start (section 7).
2. `2026-09-27-gate-4b-sonnet-watcher/`: the first watcher, Claude Sonnet 5 through
   Claude Desktop on the first draft's door. The model's own find (windage under bare
   poles, section 5) and the door's shape as the finding (section 8).
3. `2026-09-28-gate-4b-2-sonnet-watcher/`: the first live session, the doors as clients.
   The model's own account kept beside the save (`sonnet-5-post-test-notes.txt`, section
   9), and eight findings from it.
4. `2026-09-28-gate-4b-2-gemma-watcher/`: a local model through the runner. A failure
   found and its cause reasoned from the server's log (sections 5 and 8).
