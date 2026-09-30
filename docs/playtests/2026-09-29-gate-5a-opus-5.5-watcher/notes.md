# Playtest 11: the gate 5a day with Opus 5.5 as watcher through Claude Desktop

The gate's day under systems (`data/scenarios/gate-5a-day.yaml`, seed 7), the owner as
captain in the browser, from 04:00 on 1 June 1805 to 09:21 on 2 June, the model attached
through the MCP bridge from Claude Desktop, on the `gate-m5a-2` build. `save.json` is the
game as the harness saved it when the model left by `opt_out` at the captain's word;
`post-session-report.txt` is its closing message in the chat. The consent for these
weights is `docs/agents/consent/2026-09-29-opus-5.5.md`: a yes with three notes offered
"as a colleague rather than as terms" (mention versus use of the token; what one yes can
promise; candour at the station), kept there.

## The day

Eleven standing orders (the starter book, the captain's three for the passage, and a
`glass` order the captain added at the prompt: royals in on a falling glass). 130 turns
from the model: 40 stand-bys (19 until a glass, 4 an hour, 4 an urgent event, the rest
named bells, sunset, ten and five minutes, a notable event), 38 journal notes, 33 said
lines, 8 library reads, 4 shelvings, one answer. The captain spoke to it 19 times with
`tell` and once with `ask`. The model kept an hourly weather record in its journal through
the whole day (the wind, the mean, the glass and its tendency, the sky, the sea, the
motion, the speed) and a crib for the night from the primer's chapter 9, then watched the
lore play out: the backing wind with the falling glass at 19:30, the glass falling in
earnest from sunset, the veer to NW at 01:03 as the glass bottomed at 29.66, the hardest
squalls around the first rise, the clearing by dawn. It corrected its own two misreads of
a slowing fall. The night's cost: the mizzen topsail and the foresail blown out, the
larboard main topsail brace and sheet and the starboard fore topsail sheet parted, the
topsails never close-reefed because the send-down took the hands first; the mizzen
topsail and the foresail shifted and set again by 02:31.

## Findings (the model's, its order; the owner's after)

1. **Context cost.** Every sample repeats all the readings, about thirty sail lines, most
   unchanged; bundled samples each carry a full copy. Send only what changed since the
   last sample, and a compact sail line ("all studdingsails furled; storm canvas unbent").
2. **The Desktop client cuts a tool call at four real minutes.** At 1x, `stand_by` by a
   glass or an urgent event timed out repeatedly. The MCP door's wait should default under
   four minutes for a `claude-ai` client.
3. **Weather events to stand by for**: a wind shift, the glass turning or falling fast,
   the sea getting up, a change in the sky. And standing orders cannot `tell` or `ask` the
   watcher, which the captain tried three ways at 04:50 (the owner's finding 1 below).
4. **`read_log` with no `since_tick` returned the whole day**; a default of "since my last
   sample" would be safer.
5. **The journal is refused while standing by**, though readings and the log run;
   journalling changes nothing in the game.
6. **A bell that falls while a call is in flight is skipped**: "eight bells" asked at 03:58
   woke it at 08:00.
7. **A parted sheet cannot be repaired**: the refusal says "spliced or rove afresh", but no
   order does it and the library has no evolution for it; the fore topsail later showed
   sheeted and set with the sheet never repaired.
8. **The brace line is garbled** when yards are sent down: "Braced 6 yards to the wind ...
   Not the fore topgallant yard is sent down; the fore royal yard is sent down; ...".
9. **The primer's chapter 9 describes the gate's day hour by hour** ("Where the weather
   comes from"), and the log's first line names the scenario, so a reader of the library
   can foresee the night. It did not use it.
10. **The heavy-weather routine's order of work**: the send-down took the hands first and
    the topsails never got their close reefs before the 63-knot squall. "A realistic
    lesson and a good one", but the primer could say the order of an order's clauses is
    the order of the work.
11. **Sails taken in stay hanging in the gear**, not furled; a primer line would tell the
    captain whether that matters in a blow.
12. **The release line's double full stop** after a reason ending in one.

**The owner's (2026-09-30):**

13. `standing order "sea": when the sea is heavy then tell the watcher the sea is getting
    up` is refused: "'tell the watcher' is said to an agent's station, and names one".
    The standing grammar does not know the station verbs.
14. **All hands to one sail.** During "shorten sail for weather" the hands coming on deck
    all went to reefing the fore topsail, 152 at least, while the main and mizzen topsails
    waited "in turn". A bound on the hands any one job can use, the surplus to the queued
    work, and more hands visibly faster up to that bound.

**Liked:** the consent step and the brief ("one operator voice, with the exit put first");
the library ("the best part": learning the lore and then watching it come true); stand-by
by event with the notable lines listed on waking and the urgent lines cutting through;
the strain vocabulary escalating legibly; the harness notices.

## What it shows

The whole day through a real door at 1x for most of it, the held call surviving the
Desktop client's four-minute cut by re-issue, the shelf, the roll-up, `tell`, the urgent
wake-ups and the weather readings all doing what they were built for; the model's own
record of the day is the gate's report in a watch-keeper's hand. The findings are the
game's and the door's: the cost of the samples (1), the door's wait (2), the wake-up words
and the station verbs in the book (3, 13), three small harness gaps (4, 5, 6), the rigging
repair (7), a garbled line (8), a spoiler (9), the hands' distribution (14, and 10 with
it), two primer lines (10, 11), a full stop (12). Gate 5a's third ruling (the sea's cost)
is answered by 14: the night's cost came as much from three topsails reefed one after
another by all hands as from the sea.
