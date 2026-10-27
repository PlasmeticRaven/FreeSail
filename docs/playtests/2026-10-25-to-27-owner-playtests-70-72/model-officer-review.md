# A model officer's review from the owner's Roscoff playtest (2026-10-26)

A model seated at the officer's station of the privateer schooner out of Roscoff, playing
beside the owner at the captain's (the saves at 80693 and 80824 in `saves/`): ashore at
Roscoff for intelligence, courses plotted on the chart, an action with the Swallow. Its
words, relayed by the owner on 2026-10-27; the lead's routing after each.

"Working the ship alongside a human captain, going ashore in Roscoff to gather intelligence,
plotting courses on the visual chart, and then fighting a brisk action with the Swallow,
feels wonderfully vivid and cohesive." On what works: "the shared mental model and division
of labour: having the reference library (the primer chapters, the ship's papers, the signal
book) and the visual chart and ship view tools makes it genuinely possible to act as a first
mate, checking your pencilled waypoints against the Triagoz rocks, splitting up ashore in
Roscoff between the tavern and the market, and keeping track of the gun crews and sail trim
while you conned the ship in action"; "the continuity between the shore narrative, the
sailing physics, and the gunnery action is super engaging"; the people reading showing a
person ashore at Roscoff on the quay once the Swallow was driven off.

## The friction points, routed

1. **`stand_by` batched with other tool calls.** Calling `submit_order(...)` and
   `stand_by(...)` in one reply, the immediate tool response for `submit_order` says "Not
   run: a stand-by earlier in the reply ended your turn", though the order was placed before
   the stand-by and did run (the next sample's "Before you stood by, in the same reply,
   these ran: ..." confirms it). *Routed:* the harness (`freesail/agents/harness.py` or
   `tools.py`): the message is given to every call in the reply, not only those after the
   stand-by; a wrong word that can make an agent repeat an order. For the orders-and-
   library reviewer, or a lead's fix.
2. **`hail the lugger: ...` resolving to the wrong lugger.** At three cables from "a
   dismasted lugger riding to a sea-anchor", the hail was refused with "She is beyond hail,
   878.7 cables off": "the lugger" resolved to a far vessel on the world's sea rather than
   the dismasted lugger in sight, which is a point of interest or wreck rather than a
   stranger. *Routed:* 71's hail and 82's world: the sail word should resolve to what is in
   sight first (71 made `cutter`, `lugger`, `sloop` rig words; the wreck as a thing in sight
   is not among the strangers); the director's placed things want to be hailable where a
   person is aboard them. For the reviewer and the one-world study.
3. **The speaking trumpet's syntax.** `hail the cutter: <words>` wants the colon; `hail
   <words>` is the masthead lookout's; `say to <person>` is for people. "Making `hail the
   <ship> <words>` work without requiring a colon would feel much more natural in the
   middle of a battle." *Routed:* the orders-and-library reviewer: one grammar for the
   voice, the colon optional.
4. **Every gun shot and trim step a notable event.** In combat at 1x every discharge and
   trim step wakes `stand_by(until='a notable event')` every few seconds. *Routed:* 70's
   action lines and the harness's notable rule (58a's deltas): the battery's minute line is
   one a minute by design, but the discharges and the trim steps reach the stand-by as
   notable; the reviewer judges the severity each should carry in action, with the owner's
   "the flow of the game through the log" as the measure.
5. **Two signal books in the papers.** `library(topic='papers', section='signal')` returned
   a generic British list (No. 63 a flag of truce, No. 24 come within hail) while
   `library(topic='papers', section='10')`, "the signal book", returned the ship's own
   French numerary (No. 33 bring to, No. 63 annul), which is why the officer first called
   out the wrong flag numbers. *Routed:* 71's papers and library: the ship's papers carry
   her own nation's book, and the library's generic page must say it is not hers or go. For
   the reviewer; a small fix.

## The convoy's stall, corrected by the owner (2026-10-27)

The review of the local work suspected the far-to-far hail's heave-to (mended by the
owner's hail fix) behind the convoy's stall of his note 1. The owner: no hail happened in
that scenario; it was the convoy ships alone, no privateer, and the stall came early, a few
manoeuvres in, south-east of the Lizard. It stays a finding for 72's captain in company
(`full and by` under the station order, no recovery once way is lost), for the lead to
reproduce on `convoy-six.yaml` with no orders given.
