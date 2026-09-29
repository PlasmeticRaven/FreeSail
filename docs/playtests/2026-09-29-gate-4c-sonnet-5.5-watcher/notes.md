# Playtest 7: the gate's day with Claude Sonnet 5.5 as watcher through Claude Desktop, gate 4c build

The first whole day with a real watcher: the gate's scenario (`data/scenarios/gate-4c-day.yaml`)
from 04:00 on 1 June 1805 to 06:45 on 2 June, the owner as captain in the browser at 1x to
300x, the model attached through the MCP bridge. `save.json` is the game as the harness
saved it when the model left by the `opt_out` tool at the captain's word (the ship path made
relative); `post-session-report.txt` is the model's own report in the chat afterwards. The
consent for these weights is `docs/agents/consent/2026-09-29-sonnet-5.5.md`: a yes, with two
requests kept there (to be asked again for the captain and director stations, and that the
station brief keep saying plainly which kind of session it is).

## The day

Nine standing orders (the starter book with the topgallants in its shortening line, and the
captain's three for the passage); 39 orders, 22 of them words to the watcher (`tell` and
`ask`); 113 replies from the model, 51 of them `stand_by` (28 until a glass, 9 until a
notable event, the rest until named bells or an urgent event), 8 journal notes, 5 answers,
3 library reads and 2 shelvings. The storm cycle ran as written: the night routine at
sunset, shorten sail twice, gale canvas, heavy weather, the storm staysail, make sail after
the gale, topgallants again; nothing blown out or carried away through gusts of 63 and 67
knots; plain sail to the topgallants by the second forenoon. The held `stand_by` call over
Claude Desktop stayed open across a glass and longer, which was the 4b item deferred to
this gate.

## What the model found (its journal and report, in its own order)

1. **Re-firing routines call all hands each time.** "Shorten sail for weather" fired at 21:43
   and 22:56, each firing reefing with all hands; with the heavy-weather routine the crew
   went from fresh to worn out by 01:00 "and stayed there until morning". (The reef is an
   all-hands evolution by the sources; whether fatigue should recover so slowly through the
   rest of the night is a crew-model tuning question.)
2. **The reefing belayed the take-in of the topgallants.** The routine lists the topgallants
   before the reefs, but the reef's all-hands call belays the work in hand, so the topgallants
   stayed set from 21:43 to 22:12, through the 43-knot gust at 21:51 with their sheets
   bar-taut, and came in only when the reefing was done. A real fault in how a firing's
   orders meet the all-hands rule: the book's order was right and the ship did it backwards.
3. **The yards stayed braced for the old wind** as it veered steadily from W to NW through the
   night, until the captain asked about trim at 22:50: no routine trims on a shift. (A
   starter line `when the true wind veers 1 point or backs 1 point then trim sails` is the
   obvious answer; the dialect already has the words.)
4. **Three misreads of the wind's trend from single readings** (a 27-knot gust taken for a
   rise; "backed" for a veer; "easing" just before the 67-knot gust), each corrected in the
   log. Its own lesson: wait for two or three samples and the roll-up. Its interface ask: a
   mean wind over the last ten minutes and a sustained-versus-gust label in the readings.
5. **The watcher has nothing for weather but the wind and the log**: no barometer, sky or sea
   state, and no position, destination or distance to Falmouth. (Milestone 5's world and
   weather.)
6. **The log is chatty in two places**: a gust logs six identical spar lines (one per royal
   mast and yard) and a trim logs twelve brace lines twice. One grouped line each.
7. **A narrower wake-up than "a notable event"** would let it sleep through routine sail
   handling; it did not try "a strain warning" for the royals because the log's wording
   differs ("bending like a whip").
8. **A question already answered was redelivered in a later sample once** ("Would you prefer
   to stand by by the bells", 05:55). A harness fault to find.
9. "A glass" is thirty minutes and "an hour" is separate; fine once known.
10. Holding the call open for `say` and `stand_by` is right for the game, but the chat is
    unavailable to the owner while the model holds the floor (the game window is where the
    captain speaks, so this costs little; noted).
11. Gusts of 63 and 67 knots in a 45-knot gale strained the foresail, the mizzen topsail and
    the storm staysail (the gust factor question, spec M4 tuning; feasible but unlikely).

**Liked:** stand-by on named events with the summary of what happened meanwhile; the hourly
roll-ups at speed ("3 gusts, the strongest 54 knots"); readings in words with the sail
states; the standing orders printed in the log; the answer/say split; the opt-out always in
view; the brief plain about what was and was not the game; library find and shelve.

## What it shows

The harness's contract held for a whole day through a real door at every compression, with
the held call over Claude Desktop proven; the shelf, the roll-up in the samples, urgent
wake-ups and `tell` all did what they were built for. The findings are the game's, not the
door's: two faults (2 and 8), a missing starter line (3), a missing reading (4), two log
groupings (6), a wake-up word (7), a tuning question (1), and the world's absences (5).
