# Playtest 9: Gemma4 26B (uncensored, Q4_K_M) as watcher through Ollama and the local runner, gate 4c build

The topsail schooner from rest in a 20-knot northerly, seed 10, the owner as captain in the
browser, 04:00 to 07:43 of ship's time on 1 June 1805; the same weights as playtest 4
(consent `docs/agents/consent/2026-09-28-gemma4-26b-a4b-uncensored-hauhaucs-balanced-q4_k_m.md`),
on the gate 4c build. `save.json` is the game as the harness saved it when the model left by
`opt_out` at the captain's word (the ship path's slashes made forward); `runner-log.txt` is
the runner's terminal. No new consent. The owner counts this and playtest 8 as the
provisional local test that closes gate 4c (2026-09-29).

## The session

Sail made in stages to the fore topgallant and a weather studdingsail; two standing orders
to steer by the studdingsail and the fore topsail (belayed before the tack); a tack; the
session ended at the captain's word. Thirty turns; the model stood by "a glass" nearly
every turn and once "ten minutes" when the captain suggested shorter waits; it read the
library four times, answered five questions and wrote three journal notes, the last a
session review; it noticed the main topmast working under the press of sail and said so
three times. No runaway, no timeout, no nudge: the 28c fixes hold on the model that found
them (playtest 4).

## Findings

1. **A leaked thought as narration.** At 06:53, asked "how is she looking now?" with the
   studdingsail boom bending like a whip, the model replied with 1,500 words beginning
   `<thought` and ending mid-sentence, no tool call. The harness took it as the reply's
   text and wrote it into the log as one routine `[watcher]` line (`harness.py`, the free
   text under the mark), so the captain read a page of the model arguing with itself about
   whether `answer` ends a turn. A reply that opens with an unclosed thought tag, or that
   is longer than a station's line or two by an order of magnitude, should be journaled as
   a fault and not said. Its confusion was real, too: the door note says a turn "ends when
   you reply without a tool call" and the `stand_by` tool says it ends the turn; the two
   sentences together read as a contradiction to it. One sentence to fix in the note.
2. **Four empty replies in a row** (06:58 to 07:10: the tack, the glass, two braces), then
   a normal stand-by. Nothing was said and nothing was journaled; the runner counts
   failures, not empties. An empty reply at a sample with a question owed should count
   toward the nudge, and the journal should record it.
3. **A shallow watcher.** Against Qwen (playtest 8) on the same ship and seed, Gemma stood
   by a glass at a time, answered in one line, and noticed one thing (the topmast) again
   and again; it never used `find`, never shelved, never stood by on an event. Fine for a
   feature test; below Qwen for play. Its own review says the harness was smooth and the
   task well supported, which is true, and says nothing a captain would learn from.
4. **`ten minutes` accepted as a stand-by** after the captain's word; a good sign for the
   tool's parsing of durations.

## What it shows

The build is sound for a local model of this size: no fault in the harness, the stand-by
and the turn's end as 28c made them. The two findings are a robustness gap (a leaked
thought or an empty reply is not a line a sailor said) and a wording in the door note.
