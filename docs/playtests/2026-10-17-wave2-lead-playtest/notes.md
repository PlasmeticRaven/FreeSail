# The second wave's playtest by the lead (2026-10-17)

A local game in the lead's container: the Éclair out of Roscoff (`data/scenarios/lugger-roscoff.yaml`,
seed 7, the business on), the lead at the captain's station through its client at the
game's agent API, the consent record of the earlier scratch run (kept out of the repository),
a headless browser page open on the game so that the station's pictures could be drawn.
Three hours of ship's time, 05:00 to 08:00 on the 12th; the save at the stand-down in
`save/`; three pictures in `pictures/`. The head rules' two kinds of note are kept apart.

## Findings grounded in the log

1. **The lugs are not dipped when a helm order carries the wind across the stern.** At
   05:58 she ran E by N with the apparent wind 166° astern, a little on the starboard
   quarter; `steer NE` at 05:59; `Steady on NE (45°)` at 06:02 with the apparent wind 135°
   on the larboard quarter; no wear and no dip in the log between. The picture from right
   ahead at 08:00 shows the three lugs still on the larboard side of their masts, now the
   weather side, set against the masts (`pictures/from-ahead-after-the-turn-08-00.png`,
   against `from-ahead-running-05-58.png`). She kept her five knots. This is the owner's
   "aback" finding of the first cruise from the other end: a course change inside the
   running band is a helm alteration to the game and a wear to the sails. For 58 (the
   helm rule orders a wear, or the dip is done, when the wind crosses the stern) and the
   lugger's model (the lug's side a state the trim reads). Not 57's fault: 57 drew what the
   model holds.
2. **57's lug topsails set flying** read "sent down" at the start, `Set the fore topsail,
   flying` at 05:29 and the main at 05:30, "plain sail set" after; the pictures draw them
   above the lugs on the lugs' side.
3. **54's readings answer at a station:** `how am I` ("You are fed, watered and rested. You
   last ate at 05:00 ...") and `the stores` ("water 4 tons for 33.6 days, provisions for 30
   days") in the first reply, unlogged.
4. **The standing order `at the anchor aweigh then steer E` steers her before she has way**,
   as in the owner's cruise: aweigh at 05:16, steering E at once, her head fallen off to S
   by 05:24 with the land a cable on the bow, the helm order at the sample bringing her up.
   For 58's captain and the primer's starting book: the course is given when she gathers
   way, not when the anchor breaks out.
5. The game's clock is held at tick 0 until a driver says `go` through `/api/driver`, and
   `time 60` is refused at `/api/order` as a console command: right, and worth a line in the
   Harness for a door that starts a game headless.

## Impressions from the station (for the owner's read)

- Running dead before it with the lugs squared out, the beam view shows the lugs edge-on
  and the ahead view shows them broad; both are right, and from the beam a lugger running
  looks like a ship under bare poles with three slivers. A note in the picture's words
  ("the lugs squared out") would spare a model a doubt.
- `ship_view facing="0"` was read as no facing and gave "abeam to leeward"; "right ahead"
  worked. A zero that means ahead should mean ahead.
- The lead could not tell from the readings that the wind had crossed the stern between
  samples; only the picture showed the lugs on the wrong side. The deltas booked with 58
  (the sample saying "the wind has drawn from the starboard quarter to the larboard")
  would have said it in words.
