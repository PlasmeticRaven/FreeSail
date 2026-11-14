# The cold review of milestone 7: the lead's sealed notes

**Reviewer: do not read past this paragraph until your own findings under heads 1 to 5 of
your brief are written down and committed on your branch** (`docs/reviews/ColdReview-M7-Brief.md`,
"The order of reading"). What follows is what the lead already believes or suspects. It is
kept from you at the start so that your picture is your own; it is given to you afterwards
so that nothing the lead knows is lost. Every item is a claim to be tried, not a finding.

---

## The lead's examples, taken out of the brief

- Under head 4 (built inefficiently, or more than once), the lead's guesses at matters
  handled in two or more places that do not know of each other: the ways a ship is set up;
  the ways a thing is dated; the ways hands are called, work waits and a line is said; the
  orders, the forms and the readings; regions of the chart, of the tide and of the weather.
- Under the test suite's sub-review, (d) the procedure: the browser plan missed at package
  109's step 1 is a case on file (a step that changed what an order answers was merged
  with a browser plan broken, because no cloud run before run 81 played the browser plans
  at all and the trial that would have caught it was cancelled for another).

## The lead's running list, as it stood at the launch (2026-11-14)

What the game does:

- "take the purse" is read as a reading. Refusals leak where a thing is, or that it is gone.
- A rules captain waits for his tide (a port's `leave_on`) without a word: a player who
  leaves a ship with orders sees nothing happen for hours.
- Rules captains and the ground: the schooner of the recorded merchant passage takes the
  ground thirteen times as recorded (and never with one more hand, by the ships session's
  measure); a cutter left to cruise from Falmouth weighed on the ebb and took the ground
  on mud at five knots nine minutes later.
- Vessels cross the land: on a busy day 8 of 35 and 6 of 24 at some ten-minute sample
  (package 109's measure, written up for package 61; a guard that steers round by the sea
  road cost the busy sea 22 to 56 in a hundred of its pace because the road's graph is
  rebuilt at every call).
- A far ship under a rules captain riding at an anchor, woken to full detail, was not at
  anchor and sailed off (being mended in package 60, in flight).
- A boat lost while carrying a person leaves him in no hull and not dead (in flight, 60).
- Until 2026-11-14 a game saved and loaded lost the chart it began with (a `region:`
  scenario came back with that one region); found by chance in package 112's first
  measurement, not by any test.
- The coarse chart layers stand at mean sea level and the game adds the level above low
  water again: 765 coarse shore cells flood at mean tide.
- The ocean outside the chart's blocks reads the Channel's eleven gauges alone.
- A port file has no served field for decision 68's statement; it stands in comments.
- A book of orders cannot say a clock hour, only bells.
- Spain's "two flags at the main"; a yardarm hoist past the view's frame on three hulls.

The data:

- Port tracks are the way the land allows, not sounded channels: many cross water no
  trader floats in at low water (package 111, in flight, is adding a check; its first
  form under-read narrow shoals because it sampled every 20 m).
- Genoa, Cartagena, Oran and St Malo cannot be entered on the chart as it is.
- The nations' days: the French all from memory, the British and Spanish dates mostly.
- Every port datum of the Canaries is unverified; gauge levels judged from constituents
  in Sicily and proposed for the open ocean.

The tests:

- The pace floors (truth 7-159's and the gate day's) sit inside the machine's noise: the
  unchanged trunk fails them on a builder's machine beside a tree that passes.
- `tests/test_known_truths.py` defines the helper `_until` twice; the second silently
  replaces the first for the tests between.
- Truths that only import and call tests of another file.
- Truth 7b-130 failed once under load and passed alone twice.
- No cloud run before run 81 played the browser plans; every "green whole" claim before it
  was green without them.
- Independent readings of package 60 found, in three rounds, some twenty faults that the
  builder's green suites did not, and each round's mends brought new ones; package 111's
  tracks were on the wrong side of a rock by the pilot's own text with every test green.

The process:

- Builders stall silently when a container restarts; three were found asleep for hours.
  Scheduled messages have arrived up to 45 minutes late.
- Builders' containers lacked part of the test set-up (the Playwright package; the
  server's websocket library), so browser tests skipped or timed out unseen; a setup
  script was added to the environment on 2026-11-13.
- A builder told to merge the trunk after every landing never reported, since each merge
  restarted two hours of suites (the lead's own instruction).
- The suites cost an hour for the fast tier on four workers and an hour to an hour and a
  half whole in the cloud; a builder's three tiers take about four hours.
- The ships session, on the owner's computer, cannot be messaged; a file it watches is
  the only road.
- One cloud run took ninety minutes where the others take sixty, unexplained.
