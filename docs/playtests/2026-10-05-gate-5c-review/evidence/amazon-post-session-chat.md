# The *Amazon*'s officer after the session: its own account

Supplied by the owner on 2026-10-05, from the Claude Desktop chat of game 8 (the *Amazon* as a
merchant ship, Opus 5.5 as officer of the watch). This is the chat side of the session, which
no save holds. It is the model's own account and opinion, kept as the playtest form's
section 9 asks; the review's report says which parts the logs and the code bear out.

## The owner

> Thank you, definitely some useful notes. The true position leak is a good one, but actually
> I think that one of the main problems so far has been in maneuvering close-in to land in
> good weather, where the reckoning should basically be perfect just by visually seeing the
> land nearby relative to yourself, actual charting notwithstanding.

## Opus 5.5

I agree, and it's the more fundamental problem. In clear weather a mile off a well-marked
island, a real officer isn't doing dead reckoning at all. He's looking, and his position is
good to a cable or two. The game made me navigate that water half-blind, and the leak only
mattered because the honest channels were so coarse.

Here is what it looked like from my side:

- Distances didn't resolve as we closed. The Lavandière read "two miles by estimation" for
  about twenty minutes while we closed on it at three knots. Then it jumped to "a mile". Close
  in, distance should sharpen as it shrinks, to cables and then ship's lengths.
- Bearings came only to the point, 11¼°. At two miles that's about 0.4 miles of sideways
  error, which is roughly the width of the gap between the island and the Lavandière. Near
  land an officer reads a bearing to a degree or two off the compass, or simply sees that the
  rock is "fine on the starboard bow".
- Nothing told me what was safe. Each landmark is a point with a bearing, so I couldn't see
  that the island's west end, the Lavandière and the drying ground formed a gap. That's why I
  aimed at the rock instead of the channel. The pilot's directions are written in visual
  terms ("keep it close aboard to starboard", "haul toward the island"), and I had nothing
  visual to follow them against.
- Taking a bearing didn't always give a fix. One bearing moved the account onto a line at the
  nearest point, which was fine. But crossing two bearings never visibly collapsed the doubt,
  and the lookout's distance estimates fed the account even though they're the weakest
  information there is.

Some ideas, roughly in order of payoff:

1. Sharpen what's in sight with distance and weather. Within a few miles in clear weather,
   give bearings in degrees and distances in cables, with error that grows with range and
   haze. Far off, keep the points and leagues.
2. Add a "fix" order. It would cross two or three bearings, or a bearing and a sounding, and
   set the account with a small doubt. Close in, that's what the reckoning should be.
3. Report how marks relate to each other. For example: "the Lavandière open of the island's
   west end", "the church on with the mill", or "the west end of the isle abeam, four
   cables". Transits are how period pilots gave directions, and they'd let the pilot's prose
   be checked against what's seen.
4. Let the pilot con when he has charge. Historically he would. If the officer keeps the
   helm, the pilot should at least hail when she's standing into danger. That would have
   stopped me well before three fathoms.
5. Give the officer a word picture of the near coast. You have the top-down map and I have a
   list of bearings. One reading listing the visible dangers within a mile or two, with true
   bearing and distance when visibility allows, would roughly match what you see on the map.

To be fair to the game, some of the trouble was mine. With points, leagues and the pilot's
prose I could have worked out that the passage lay east of the rock, and I didn't. But better
instruments close in would have made that mistake much harder to make.

## Opus 5.5, shown a picture of the chart near the Isle of Bas

Yes, I can make quite a lot of it, and it explains the near-grounding better than anything I
had at the time.

**Where we were.** At the 1-mile scale bar (about 250 px), the account's track comes down
from the north and ends at the anchoring, around x 375, y 405. That point sits almost on the
outline of the Isle of Bas's western end, among the ledges off its north-west corner. The
Lavandière (425, 622) is about nine cables south of it, and the western entrance marker
(400, 572) is about seven cables south. So we were never "a mile north of the Lavandière in
open water". By account we were on the island's own western ledges. The soundings agree:
three and a half fathoms over ground the chart dries. For once, account and lead tell the
same story.

**Why I didn't know.** At that moment the readings gave the Isle of Bas "E by S, two miles".
The label sits at the island's middle (770, 437), and that is what was being reported: the
centre of a mile-and-a-half island, while its shore was a cable or two off our bow. Every
landmark is a single point, so the nearest land never appears. That's your point exactly. A
man on deck would have seen rocks and surf close aboard to larboard. I saw an island two
miles off.

**What the right approach would have been.** The entrance marker lies north-west of the
Lavandière. The passage between the rock and the island's south-west shore is roughly a third
of a mile wide. So the approach is from the west: stand well out, to around the track's x 250
or further, run south until the entrance is abeam, then turn east and pass close north of the
Lavandière, keeping it to starboard. My advice to "aim at the island's west end within
gunshot from the north-east" was wrong too. It would have brought her down the same
ledge-strewn western shore she nearly found. The pilot's "come to the end of the isle within
cannon-shot" only works coming from seaward on the west.

**Display issues visible in the screenshot:**

- Soundings render as "NaN fm". The leadsman's words ("and a quarter fifteen", "by the deep
  nine") apparently aren't being parsed back into numbers. It looks like the depth value is
  lost on every sounding.
- Bearing lines never expire. By the end, dozens of old lines from three landmarks fill the
  chart. Fading lines older than a glass, or keeping only the latest pair per mark, would
  leave the current fix readable.
- The in-sight text overflows the top of the map, and sounding labels overlap one another
  along the track.

**The bigger fix.** Even without a true-position view, the game can give both of us the
land's edges instead of its centroids. A "nearest land" line in the readings would have
changed the afternoon on its own, for example "the west end of the Isle of Bas, two cables E"
or "rocks breaking close aboard to larboard". So would sighted features named by their parts:
the west end, the south-west point, the ledge off the north shore. That's the information a
period officer has by eye in clear weather, and its absence is what turned a straightforward
pilotage into blind groping.
