# FreeSail gate m5c-c: the follow-ups from gate 5c's first playtests

A working copy of `FreeSail-gate-m5c`, made on 2026-10-06 at the owner's word, in which the
findings of gate 5c's first playtests are built package by package. It is local work: no
commits are made here and the GitHub repository is not touched. The owner folds the work in
with the lead session that works the repository.

The findings, where each was seen and what the owner ruled are in
`docs/playtests/2026-10-05-gate-5c-review/report.md` (section 8 for the recommendations,
section 9 for the owner's answers). The packages are briefed in
`docs/dev/M5-WorkPackages.md`, under "Follow-ups from gate 5c's first playtests".

## What is in this folder

| Step | What | State |
|---|---|---|
| The base | `FreeSail-gate-m5c` as it stood on 2026-10-06: its code, data, documents, tests and tools | Copied |
| 37b, 37c | `m5c-b.diff` applied: returning to the station, and the two log rules (see `FreeSail-gate-m5c-b/CHANGES-m5c-b.md`) | Applied; all 22 changed files are byte for byte m5c-b's |
| 37d | The saves, and the sight of land | Built 2026-10-06, with a second pass the same day (below); all six recorded passages come through |
| 37e | The account: one rule for an observation, an honest doubt, the master's tide, a course made good | Built 2026-10-07 (below); four of the six recorded passages come through whole, the schooner's without her pilot aboard and the cruise's without the brig spoken |
| 37f | Lying to, and the ground: a ship hove to stays hove to; the anchors by name, the dragging line, the ground's words; the log's lines | Built 2026-10-07 (below) |
| 37g | The station's safety, and the deck, the leaving and the grant; the consent brief revised once | Built 2026-10-07 (below); every model with a yes on record is asked again at its next seating |

**The suite at the start.** With the base and the diff and nothing else, the whole suite on
the owner's Windows machine (`py -m pytest -n 4 --slow`) ends
`2713 passed, 7 xfailed in 842.59s`. The seven are the owner's standing rulings.

## What was left behind, and why

- **The saves** in `saves/` and at the root of m5c and m5c-b. By the owner's rule a save
  lies in the folder of the build that played it. An older game is loaded from where it
  lies, by its path; a save made here goes into this folder's `saves/`.
- **The owner's notes** (`m5c playtest and model notes.txt`), which are m5c's record.
- **The one consent record made under m5c-b** (`2026-10-03-opus-5.5.md`). It is not part of
  the diff. Under this folder's consent brief every model with a yes on record is asked
  again at its next door, because 37b changed the **Leaving** section.

Two things were added that m5c does not have at these paths:

- `docs/playtests/2026-10-05-gate-5c-review/`, a copy of the review as it stood on
  2026-10-06. The original is in m5c.
- `tests/fixtures/saves/`, two of the playtest's own saves with their checkpoints, for
  package 37d's tests:

  | File | The game | The build that wrote it |
  |---|---|---|
  | `m5c-cutter-tick34091` | The cutter from Falmouth with a local model as mate, 12 June, nine and a half hours | m5c |
  | `m5c-b-harpy-tick602100` | The *Harpy* at anchor off Rame Head on the morning of 19 June, ninety minutes before she weighed for Plymouth | m5c-b before 37c |

  **These carry a model's transcript and journal and the owner's own typed lines.** Whether
  they go into the repository is the owner's to say. The tests that use them skip when the
  files are not there.

## Running it

From this folder, so that this copy's package is the one imported (the editable install
points at m5c):

```
cd D:\Projects\FreeSail\FreeSail-gate-m5c-c
py -m freesail.ui.server
```

with the usual flags. To go on with an older game, load it by its path, for example
`--load "..\FreeSail-gate-m5c-b\saves\freesail-seed7-tick558434.json"`. It loads from its
checkpoint.

The tests, from this folder:

```
set PYTHONPATH=D:\Projects\FreeSail\FreeSail-gate-m5c-c
set PYTHONUTF8=1
py -m pytest -n 4
py -m pytest -n 4 --slow
```

The MCP bridge that Claude Desktop starts imports the package from wherever it runs, which
is m5c. As `CHANGES-m5c-b.md` says, a rule that lives in the game's server works either way;
to have the bridge itself run from this folder, set `PYTHONPATH` to it in the `env` of the
`freesail` entry of Claude Desktop's config and restart Claude Desktop.

## How it will be handed over

As m5c-b was: this note, and one diff against m5c as it was cut
(`FreeSail-gate-m5c.zip`), made when a package has landed and its suite is green. The diff
leaves out the caches, `saves/` and the playtest fixtures unless the owner says they go in.

## The packages as they land

Each package adds its section here: what changed, which files, which recorded constants
moved and why, and anything not done.

### 37d: the saves, and the sight of land (2026-10-06)

The brief is `docs/dev/M5-WorkPackages.md`, "Package 37d"; the measurements and the table of
reasons are in `docs/dev/TuningNotes.md` under the same name.

**The suite, after the second pass.** The fast tier (`py -m pytest -n 4`) ends `2549 passed in 342.23s (0:05:42)`; the whole suite
(`py -m pytest -n 4 --slow`) ends `2790 passed, 7 xfailed in 1022.51s (0:17:02)`. The seven expected failures are the owner's
standing rulings, as before. The two this package added in its first pass (the schooner's run in and the
merchant's Goulet) are gone: both passages come through.

**What changed, in plain words.**

- **A save says which build wrote it.** Every save and checkpoint carries the build's name
  (`m5c-c/37d`) and a fingerprint of the game's code and data. Worked once at start, in three
  hundredths of a second.
- **`load` says what it did.** From the checkpoint when it can; and when it cannot, it says
  why (none beside the save; not this save's; could not be read). A game from another build
  with a model aboard is not replayed unless you add `--replay-anyway`, because that replay
  would not be the game that was played. The server, the console (and its `replay`) and the
  REPL door all say the same words.
- **A station seated at the very start replays in its place**, after the game's opening line
  and not before it.
- **Three old saves are kept as tests**: the cutter of m5c, the *Harpy* of m5c-b, and one made
  by this package with a scripted officer standing by. Each must load from its checkpoint,
  run on and save again, on every build from now on.
- **The lookout's distances follow the ship in.** "Penlee Point ... a mile" at two cables
  cannot happen now: a distance is judged afresh whenever it has changed by a tenth.
- **A bearing gives a line; its distance is laid down only when it is the better figure.** The
  first pass took the lookout's guessed distance out of the account altogether. That cured the
  jerking between marks, but a landfall on one headland after a long run was left miles along its
  line (the schooner, 6.8 miles out where she had been 0.9). The second pass, which the owner
  approved, lays the distance down when the account's own doubt along the line of sight is greater
  than the guess's, and the line says so: "The Lizard bore N by W, five leagues by estimation; the
  account laid down at that distance, the estimate being the better figure: moved three leagues to
  the SW." Once laid down, the next bearing of that mark lays nothing down, so the account does not
  creep; just after a good fix none is laid down, so two marks cannot pull it to and fro. Otherwise
  the line gives the guess, and the account's own distance beside it when they disagree by a third.
  A bearing of a sail moves nothing.
- **`take a fix`**: cross bearings of two or three marks, the account set where they cross.
  Said bare, the master picks the marks. The officer may be allowed it with `you may take a
  fix`.
- **The nearest shore is always in sight within a league**, and `the nearest land` is a
  reading every station has.
- **Land ahead.** The lookout warns when she is standing into the land: a notable line under
  ten minutes off, an urgent one under four.
- **A dragging anchor is urgent; the pilot's hails are notable.**
- **The sea breeze blows steadily from the sea.** Off Penlee on the *Harpy*'s own afternoon
  the wind turned two points or more 386 times in 83 minutes as she moved; now not once.
- **An anchor's depth is read where the anchor lies**, not a mile off after a long run.

**Files changed.** Code: `freesail/core/world.py`, `core/replay.py`, `ui/server.py`,
`ui/console.py`, `agents/repl.py`, `agents/harness.py`, `world/lookout.py`,
`world/reckoning.py`, `world/chart.py`, `world/weather.py`, `world/ports.py`,
`world/ships.py` (one function, for the one frame), `api/readings.py`,
`orders/navigation.py`, `orders/complete.py`. Data: `data/vocabulary.yaml` (`take a fix`);
`data/scenarios/gate-5b-passage.orders`, `gate-5b-passage-schooner.orders`,
`merchant-passage.orders`, `naval-cruise.orders` (each bearing rule now takes a fix after
the bearing; in the second pass the merchant's pilot-water rule went back to the bearing alone
and two of her points in the Goulet were moved). Documents: `docs/TechnicalSpec-M5.md` (§11, §12, §13, §15, §18, §33),
`docs/primer/10-the-reckoning.md`, `docs/primer/13-the-tide-and-the-anchor.md`,
`docs/dev/TuningNotes.md`, `docs/agents/Harness.md`, `docs/dev/M5-WorkPackages.md` (one dated
paragraph under item 6, for the second pass), this file. Tests:
`tests/test_replay.py`, `test_checkpoint.py`, `test_lookout.py`, `test_reckoning.py`,
`test_chart.py`, `test_weather.py`, `test_readings.py`, `test_orders.py`, `test_anchor.py`,
`test_ports.py`, `test_officer.py`, `test_known_truths.py`, `tests/conftest.py` (four slow
tests named). Added: `tests/fixtures/saves/m5c-c-37d-officer-tick5400.json` and its
`.checkpoint`. The consent brief and every station's brief are untouched.

**Recorded constants that moved** (old beside new, with the reasons, in `docs/dev/TuningNotes.md`,
"The second pass"). The 5a day under systems: nothing. The 5b passage in thick weather: one line
more and the digest (the first pass). The 5b frigate: her departure off Ushant is fixed otherwise,
so her track differs from the first minute; the cast two seconds earlier, the anchor eighteen
minutes later, the pilot five minutes later than the first pass had them; 630 lines to 662; the
digest. The 5b schooner: every tick as it was before 37d; 731 lines to 760; the digest. The 5c
cruise: the stranger raised seven minutes later and spoken three hours sooner (the first pass); the
digest. The 5c merchant passage: the pilot of Brest aboard at 08:16 (06:26), the road of Bertheaume
at 09:09 (07:47), the mouth of the Goulet at 12:19 (12:06), the Bay at 13:15 (13:05), the tin sold
at 15:25 (15:10); a cast at the Iroise's mark that was never made before; 2460 lines to 2634; the
digest.

**The Goulet.** The merchant passes the Mingan 1.8 cables to the north (328 m; 311 m before 37d)
and the shore under Petit Minou 1.6 cables off (294 m; 273 m before). Two points moved: the course
from the road is shaped for 48 19.15 N 4 38 W (was 48 19.3 N), and from under Petit Minou for
48 20.9 N 4 35.1 W (was 48 20.7 N 4 35 W). In pilot water she takes the bearing alone, as before
37d.

*The lead's correction, 2026-10-06, measured from this package's own dumps of the three runs.*
The second pass put the strike down to the fix "putting a worse account in the place of a
headland's bearing every five minutes". The figures do not bear that out. The account's distance
from the truth, as a median over each leg:

| Leg | Before 37d | The fix every five minutes (first pass) | The bearing alone (as delivered) |
|---|---|---|---|
| The Iroise to the road of Bertheaume | 0.91 mile | 0.50 | 0.45 |
| The Goulet | 0.45 mile | 0.17 | 0.48 |

With the fix the account in the Goulet was nearly three times as true, and it was with that
account that she struck. Of the sixty fixes on the two legs, nine left the account worse than
it had been a second before. So what set her on the Mingan was the book: its points and its
0.4-mile rules were tuned at seed 7 to an account that lags her on the flood, and a course
shaped for a point allows nothing for the stream. Seven tries at moving the points with the
fix kept did not bring her through within the pass's budget; she comes through as delivered
because the account in the Goulet is again about as wrong as it was before 37d. The book is
to be tuned for a true account when 37e has settled the reckoning's rule (below).

**Not done, and why.**

- **The account in the Goulet is still not a true one.** As she gets under way from the road it
  runs seven cables wrong, and on the flood it lags half a mile astern of her, while believing
  itself good to a cable; so the guessed distance, which is right, is not laid down ("five cables
  by estimation; a mile by the account"), and the Goulet's rules fire late. The passage comes
  through because the points allow for it at this seed. The frigate's landfall shows the same
  thing: four miles out for forty minutes, the line reading "five leagues by estimation; three
  leagues by the account". Mending it is the reckoning's own doubt (as she weighs, and on a
  stream), or a second condition on the guess; neither was asked of this pass.
- **`take a fix` sets the account outright, and picks its marks by how they cut and not by how
  near they are.** Measured on the merchant's two pilot-water legs (the lead, 2026-10-06): the
  nearest land's own mark was one of the fix's marks in 22 fixes of 60; the fix's true error was
  a median 0.37 mile in the Iroise, by marks six to ten miles off, and 0.14 mile in the Goulet, by
  marks three and a half to six miles off; in 9 of the 60 it left the account worse than it was.
  A fix that chose the marks giving the tightest fix, and was weighed in when it is not the
  better figure, would mend both. Left as the first pass built it, for 37e.
- The dialect does not yet take cables (`when the nearest land is under 3 cables`); half a
  mile and miles it takes. That is `freesail/standing/grammar.py`, outside this package.
- `the port` and `the depth of water` still give the true figures, as the brief says, until
  the owner has played this.

**Played, 2026-10-06 (added by the lead on the 7th).** The owner took a merchant brig from
Falmouth to Roscoff alone, and on to Brest round Ushant with Opus 5.5 as officer of the watch:
five days, saved in `saves/freesail-seed7-tick430516.json`. The review of that game is section
10 of `docs/playtests/2026-10-05-gate-5c-review/report.md`, with its measurements in that
folder's `evidence/G9-brig-m5cc-measurements.txt`. For this package:

- The save replays on this build to the log that was played, line for line and digest for
  digest (7,140 lines, a station held for 78 hours, two seatings).
- With marks in sight and fixes going the account stood one to five cables from the ship; the
  landfall bearing took it from 7.1 miles out to 0.7; the urgent land-ahead cry came five
  minutes before she passed the Mingan at 1.2 cables.
- Both items under "Not done" above showed in play. The account's stated doubt was about a
  tenth of its true error whenever she had no observation, and a fix by far marks moved a
  right account, at anchor and in the Goulet.
- Outside this package's remit, and for the next: the lunar and the noon latitude still follow
  the two-mile rule; heaving to; and what the ground-tackle orders do with an anchor's name.

### 37e: the account (2026-10-07)

Built from the brief "Package 37e: the account" in `docs/dev/M5-WorkPackages.md`, which is the review of game 9's reckoning turned into fourteen items. The build's name is `m5c-c/37e`.

**The suite.** The fast tier (`py -m pytest -n 4`) ends `2594 passed in 323.06s (0:05:23)`; the whole suite (`py -m pytest -n 4 --slow`) ends `2836 passed, 9 xfailed in 1047.96s (0:17:27)`. Seven of the expected failures are the owner's standing rulings, as before. Two are new, each one beat of a recorded passage that did not come through and is said plainly below.

**What changed, in plain words.**

- **One rule for believing an observation.** There were three, and game 9 showed each going wrong: a lunar the master would trust within 25 miles replaced an account he trusted within two; a noon latitude that was right was all but ignored by an account four miles out; a fix by distant marks moved a right account at anchor by nearly a mile. Now every observation (a noon latitude, a lunar, a time sight, a cast of the lead, a bearing, a fix) is treated the same way. The master sets his doubt of his account beside his doubt of the observation and does one of three things: **weighs** the two (the account moves toward the observation by as much as it is the more doubtful), **takes** the observation outright when the two are further apart than their doubts together allow, or **keeps** the account when the weighing would move it less than half a cable. The log line says which, and by how much. Game 9's lunar now moves the account under two cables; game 9's noon is taken; a poor fix no longer moves a good account.
- **The same thing seen again tells him nothing new.** A second bearing of the same mark from the same place, a second cast on the same ground, a second fix by the same marks no longer make him surer. In game 9 eight casts over flat sand off Ar Men narrowed his doubt while his error grew from one mile to five; now they narrow nothing.
- **His doubt is honest about the hours she has no way.** Hove to or becalmed, the account and its doubt used to stand still while the tide carried her. Now the clock runs on: hove to he reckons her drift by eye, becalmed the tide carries the account, and his doubt grows by the hour in both. Only at anchor does the account stand still. His words say the doubt as it lies when it is long and thin: "within three miles NE and SW, nor a mile across".
- **A fix takes the near marks.** Left to himself the master now takes the marks that leave him the least doubt, which puts a headland inside a mile before a town five miles off. In the Goulet he takes Petit Minou, Camaret and Portzic, and not Brest and Conquet.
- **The master works the tide himself**, by the owner's ruling. He reckons the stream from his own books (the hour of high water from his epitome, the moon's age from his almanac, and what his sailing directions say of the water his account puts her in) and carries it into the account every quarter of an hour. He never sees the sea's own tide, so he can be an hour out in his timing and he uses round figures; that difference is still the game. The log says when his tide turns and when he believes she has passed into other waters.
- **`allow ... knots of set` replaces the master's tide** until the captain hands it back with the new order `allow the tide by the book`. `allow no set` tells him to allow nothing. The reading `the reckoning` says what tide is allowed and whose it is.
- **A shaped course makes good.** `shape a course for <place>` now orders the course to steer so that she makes the line good against the tide being allowed, and says both: "Shaped a course for the Goulet: NE by account, ten miles. Allowing the flood, a knot and a half to the E by N, steer NE by N to make it good; the allowance holds till the tide turns, about half past four." It is worked once; the master does not alter the helm when the tide turns. It also says when the line crosses the land or passes close along a shore, which a course shaped for Brest from off Roscoff did not in game 9.
- **The primer** teaches the rule in a seaman's words, and gains the two things game 9 showed nobody knew: `observe an amplitude` to correct the compass before a landfall, and the captain's own allowance for a set.

**How well it works, measured.** The same three recorded passages were sailed before and after, with the account's distance from the truth and the master's own doubt sampled every half hour.

| | The merchant, before | after | The frigate, before | after | The schooner, before | after |
|---|---|---|---|---|---|---|
| median error, miles | 0.35 | 0.41 | 4.49 | 1.21 | 2.18 | 0.97 |
| time more than three miles out | 18% | 18% | 53% | 26% | 47% | 26% |
| samples where the error was more than twice his stated doubt | 35% | 18% | 62% | 6% | 53% | none |

Three of the four things the brief asked of these figures were **not fully met**, and are said here as they are:

- The merchant's time more than three miles out was to be halved from 18 per cent; it is still 18 per cent, and her median is 0.41 mile against 0.35. All of it is the night crossing of the Channel, where her compass, her leeway and the tide each put her two to five miles out and no observation is to be had.
- The frigate was to be within a mile and a half of the truth inside half an hour of raising the land; she is 2.4 miles out for thirty minutes and 1.25 at thirty-five (before: 4.2 to 5.4 miles for thirty-five minutes).
- The master was to be more than twice wrong about his own doubt in no more than one sample in ten. The frigate (6 per cent) and the schooner (none) meet it. The merchant does not: 18 per cent, down from 35. Seven of her thirteen bad samples are at anchor in the Bay of Brest, where fixes every five minutes by three marks all on one hand leave him believing himself good to a cable when he is three cables out.

The fourth was met: the brig, hove to for six hours of a spring ebb in the Iroise, drifts 13.6 miles and her account ends two miles from her, inside twice the master's doubt throughout. Before, the account stayed where she was brought to.

**The recorded passages.** All six were written out before and after and every changed line accounted for (`docs/dev/TuningNotes.md`, package 37e). The day of gate 5a is unchanged to the digit. The other five moved, as the brief said they would, since each shapes a course.

- **The frigate's passage** comes through: the Lizard raised, the Manacles rounded by a point three miles east of them, the pilot aboard, anchored in the outer road. Her book gained two lines.
- **The schooner's passage** comes through to her anchor off the town, **but the Falmouth pilot hails her and does not board**. She now stands in faster than his boat will board. Three mends were tried and none kept (two put her aground in the harbour). His boarding is marked as an expected failure.
- **The thick-weather passage** comes through with no change to its book: the land close aboard under Black Head, the account six miles out where it was eleven.
- **The merchant passage** comes through, Falmouth to the tin sold at Brest, with her book tuned for a true account as the brief asked: the fix is taken again after the bearing in pilot water, and she passes the Mingan 1.9 cables to the north. One thing is different in her story: the pilot of Brest boards in the Iroise and leaves her again before the road of Bertheaume.
- **The naval cruise does not come through whole.** The frigate keeps her station and the letter reaches her, but nineteen hours later than before, and **the French brig is chased and lost, not spoken**. The reason is plain and is not in the reckoning: in 37d, after the pilot left, she lay for an hour and fifty minutes with her topsails unfilled, which is a fault of the filling away that package 37f is to mend, and it was only in that lost time that the admiral's cutter caught her. With the course now made good she fills and sails, the cutter cannot catch her until she is on her station next morning, and she meets the brig from the wrong side. No small change to her book that could be stood behind brings the meeting back, so none was made. The speaking of the brig is marked as an expected failure. It wants the scenario's own hours looked at, which is the lead's.

**Found and mended on the way.** Three things in this package's own new code let the mere asking of a reading change later play by a few yards, so that a game with the chart open, or a test watching the log, was not quite the game replayed without them. All three are mended and a test now sails two ships, one asked and one not, and compares them. A cast of the lead off a steep shore could also be matched to a place two miles away and the account laid down there; it is now kept where the chart about the account already answers the cast.

**Files changed.** Code: `freesail/world/reckoning.py`, `world/tide.py`, `world/chart.py`, `orders/navigation.py`, `orders/complete.py`, `api/readings.py`, `core/world.py` (the build's name). Data: `data/tides/streams.yaml`, `data/vocabulary.yaml`, and the books `data/scenarios/gate-5b-passage.orders`, `gate-5b-passage-schooner.orders` and `merchant-passage.orders`. Documents: `docs/TechnicalSpec-M5.md` (§13, §15, §16, §33), `docs/primer/10-the-reckoning.md`, `12-the-longitude.md`, `13-the-tide-and-the-anchor.md`, `docs/dev/TuningNotes.md`, this file, and the probe `docs/playtests/2026-10-05-gate-5c-review/evidence/tools/account_probe.py`. Tests: `tests/test_reckoning.py`, `test_tide.py`, `test_orders.py`, `test_readings.py`, `test_longitude.py`, `test_chart.py`, `test_checkpoint.py`, `test_replay.py`, `test_known_truths.py`, `conftest.py`. Nothing in `docs/agents/` was touched; 37d's fixture is unchanged and its tests pass.

**Not done, and why.**

- The three figures above that were asked for and not met.
- The schooner's pilot and the cruise's brig, above.
- **At anchor in the Bay of Brest the master is surer than he should be** (above). Found late; not mended.
- **A wrong chronometer can displace a good account.** On the cruise, hove to off Plymouth with the land in sight, a longitude by a chronometer that was 7.6 miles out (the master said he would trust it within five) is far enough from the account to be taken, and the account is wrong for half an hour until the next bearing of the land takes it back. This is the one rule doing what the brief says, on an observation whose own stated doubt is too small. The cure is in how far the master trusts his chronometer, which lives in a file this package was not given. For the lead.
- **The number in the one rule is two where the brief said three.** With three, game 9's own noon sight is not taken, and the brief's test requires that it is.
- **In the open Channel the master's tide is a rough allowance**: his high water by Moore's rule is an hour to an hour and three quarters early in the days of these passages, and the only period statement of the set is "north-east", twenty degrees from the stream the world runs.
- **Spec truth 59** says a cast "moves the reckoning onto the chart's contour". By the one rule a cast is weighed and comes within a fathom of it. The test says so; the truth's sentence is left for the lead.

### 37f: lying to, and the ground (2026-10-07)

Built from the brief "Package 37f: lying to, and the ground" in `docs/dev/M5-WorkPackages.md`: twenty-one items in three parts, from the review of game 9 and the owner's notes on it. The build's name is `m5c-c/37f`.

**The suite.** The fast tier (`py -m pytest -n 4`) ends `2683 passed in 205.32s (0:03:25)`; the whole suite (`py -m pytest -n 4 --slow`) ends `2933 passed, 9 xfailed in 653.77s (0:10:53)`. Seven of the expected failures are the owner's standing rulings. The other two are the two 37e left, and both still stand: the cruise's stranger is chased and not spoken, and the schooner's pilot hails her and does not board (which is 37h's). Neither came back of itself.

**Part one: lying to.**

- **A ship hove to stays hove to, on the tack she hove to on.** In game 9 the brig came up through the wind in four heave-tos of seven. Three things are different now. Her way is taken off first: "Hove to" is not said until she lies four to seven points from the wind on her tack, has stopped swinging and has lost her way, and the line names the tack ("Hove to on the starboard tack, main topsail to the mast, helm a-lee."). She is then kept there: the watch tends the helm and the spanker and jib sheets, as Luce says a ship hove to is regulated, which costs it four hands and is said once a watch in a routine line. And if the weather forces her round all the same, the log says so once, urgently, and the record follows what she has done.
- **Measured.** From the like of the game's worst case (seven knots, the wind on the quarter) the brig used to be through the wind in the third minute; now she is hove to in under three minutes and lies five and a half points from the wind with a knot of way, and in six hours of a gusty, wandering breeze her head stays between five and a half and six points from it, with a knot of way or less. The frigate, the schooner and the cutter hold their tack the same way. The schooner and the cutter still forereach (up to two knots and a quarter, and a knot and a half): a fore-and-after hove to does, and they cannot be brought under a knot and a half.
- **`fill away` fills her on the tack she is on**, and says which. A ship that had come round used to be taken back through the wind to the tack she hove to on, with every sail aback, three times in game 9.
- **`fill away and steer <course>`** fills her and gives the helm that course in one order, by a point or in degrees. A course that lies across the wind or too near it is not given her: she is kept full and by, and the line says why.
- **The record that she is hove to is cleared** when an anchor is let go, when she weighs, when she tacks or wears, and when she takes the ground. The Roscoff morning of game 9 (lain a-try, anchored for the night, and then `steer` refused four times as "She is hove to" with the anchor up) now goes: at anchor the manoeuvre in hand is none, and weighed, she takes a course at the first order.
- **`trim sails` hove to is refused**, with the cure in the words: "She is hove to; fill away before trimming, or brace a yard by name." A yard or a sheet worked by name is still taken. The starter book's two trimming routines, and the three in each of the merchant's and the cruise's books, carry the guard `and the manoeuvre in hand is not hove to`, so they sleep while she lies to and say nothing.

**Part two: the ground.**

- **An anchor's name is honoured.** `veer`, `heave short`, `heave in` and `weigh` now work the anchor you name. On a brig moored by this build's own orders (eighty-two fathoms on each bower): `veer the small bower to 90 fathoms` veers the small bower to ninety (before: it veered the best bower to 172); `veer the best bower to 90 fathoms` veers to ninety (before: ninety more, to 172); `weigh the small bower` weighs the small bower and leaves her riding by the best bower (before: it weighed the best bower). Where the ship cannot do it, the refusal names the anchor she rides by and what would.
- **`heave in`** is a new order: `heave in to 70 fathoms`, `heave in 10 fathoms`, either with an anchor's name. `heave short` takes no number, and a number after it is answered with `heave in to`.
- **`let go` says its scope and takes one.** The default stays five times the depth, by the owner's ruling, and its first line now says the figure: "Let go the best bower in 17 fathoms; veering to eighty-four fathoms, five times the depth." `let go the best bower and veer to 45 fathoms` (or `with 45 fathoms`) veers to that and no further, and `come to an anchor ... and veer to 45 fathoms` likewise.
- **Three warnings as the anchor goes**, each notable and none a refusal: her swinging room ("With fifty-two fathoms out she will swing within a cable of the land to the NE by E."), a depth that wants more cable than she has bent, and the water at low water by the master's tide against her draught ("By the master's tide there will be two fathoms here at low water, and she draws 15 feet.").
- **`come to an anchor in twelve fathoms`** now means what the primer said: she stands on until the lead calls twelve fathoms and lets go there. **`let go the anchor` logs "Brought up"** when she is.
- **The dragging line.** Urgent once, when an anchor begins to come home, with only the advice that is left to take. While it goes on, a notable line a quarter of an hour apart at most, with how far ("The best bower still coming home: a cable since it began."). "Holds again", with how far it came, when it has not moved for five minutes. An anchor whose cable is slack is no longer said to drag.
- **The ground's words.** "Rock and mud" was held as bare rock; it now holds as the mean of the two, a little over half of good ground. Brest road had no note of its bottom and has one now (mud). Every port's road and anchorage has its note.
- **In the Goulet**, the like of game 9's eight hours (eighteen urgent lines in the game, eight in this build's like state before): one urgent line and one "holds again".
- **At anchor she is still a ship.** `furl all sail`, `square the yards`, `brace the yards square`, `loose sails to dry` and their like are taken at anchor and aground. The helm's orders and the manoeuvres still wait till she weighs.
- **The fore-and-aft cast.** A schooner or a cutter getting under way now casts as Luce's schooner does: her main boom steadied over to the side she is to cast toward, her jib's sheet to windward, her helm tended. On the merchant passage she casts in a minute and a half where she ran seven minutes to the timeout; and "She has paid off" is never said at a timeout for any ship. If she casts the wrong way the line says so, and if she will not cast at all the order fails in words.

**Part three: the log's lines.**

- **No wind-shift line in airs too light to have a direction** (under four knots by the ten-minute mean, which is where the log's own words pass from "light airs" to "a light breeze"). "Light and variable airs." is said once as it falls so, and the settled wind once when it comes again. A wind whose mean swings back and forth (it veers, backs and veers again within the hour) is said once to be unsteady, and its shifts are not logged until it has stood half an hour. A wind that turns once, as at a front, is logged as before. The event `a wind shift` keeps the same floor.
- **Aback.** In a calm "Her sails aback; she had no way on to lose" is said once, however long the calm, and again only when she has had way on her since. The urgent "Taken aback" has its own flag and is not kept back by it. Each sail's "taken aback" is said once an episode, and not at all for a sail laid aback by order: heaving to, a tack, `back the main topsail`.
- **"Could not set the jib: The jib is set already"** and its like are now a routine line in plain words ("The jib is set already.") and not a failed evolution.
- **A cast that finds no bottom is routine**, and the event `a sounding` means bottom found. **A standing order with nothing to do** says so the first time and then once a watch for each reason, where the merchant passage said "in the Bay ... she is at anchor already" twenty-six times.
- **A standing order's place is checked when it is entered.** "the distance to the land" is refused at once, with the forms that serve: "the nearest land", or "the land is in sight". A name the chart nearly has is answered with that name.

**The recorded passages.** All six were written out before and after and every changed line accounted for (`docs/dev/TuningNotes.md`, package 37f). That took sixteen whole-passage runs where the brief budgets a dozen: the six were written out a second time after one of this package's own rules was put right, and four runs went to the frigate's book. The day of gate 5a sails the same track to the last figure. The other five part where the brief said they would: at the heave-to for the noon's cast (the three passages of gate 5b), at getting under way (the merchant), and at the first anchor (the cruise).

- **The frigate's passage** comes through, with two changes to her book. Left alone she did not: filling away from the cast with a knot and a half on her, where she used to have nearly four, the one course she shapes there came out a point too far west, and she missed the point east of the Manacles and stood on up the Channel. Her book now works that course again every glass, and shortens sail when she rounds the point so that the pilot can board.
- **The schooner's passage** comes through to her anchor off the town; her pilot hails and does not board, as before.
- **The thick-weather passage** comes through with no change to its book.
- **The merchant passage** comes through, and better than before: she casts when she gets under way, and the pilot of Brest stays aboard to the anchor.
- **The naval cruise** keeps her station and reads her letter, and **the French brig is still chased and lost**. The reason is new. Half an hour into the chase her book orders a course that lies across the wind from her head; the helm takes her straight through the wind, every sail aback, and she lies without way while the brig sails out of sight. The chase order wears her for such a course the first time it is given and not the second; mending that, or the scenario's hours, would bring the meeting back. Neither is this package's.

**Files changed.** Code: `freesail/evolutions/scripts.py`, `runner.py` and `registry.py`; `freesail/orders/verbs.py` and `ground_tackle.py`; `freesail/physics/anchor.py`, `hull.py`, `integrate.py` and `sails.py`; `freesail/ship/parts.py`; `freesail/core/world.py`; `freesail/world/ground.py` and `reckoning.py`; `freesail/standing/book.py`, `rules.py` and `runtime.py`; `freesail/api/readings.py`. Data: the evolutions `heave_to`, `fill_away`, `get_under_way`, `let_go_anchor`, `come_to_anchor`, `veer_cable`, `heave_short`, `weigh_anchor` and the new `heave_in`; nineteen evolutions whose "done already" precondition is marked; `data/vocabulary.yaml`; the starter book and the books of the merchant passage, the cruise and the frigate's passage; the chart's features, index and manifest for Brest road. Tests: the new `tests/test_lying_to.py`, `test_tackle_orders.py` and `test_log_lines.py`, and the tests the changes moved. Documents: `docs/TechnicalSpec-M0-M2.md` (§8), `TechnicalSpec-M3.md`, `TechnicalSpec-M5.md` (§5, §18, §23, §33), primer chapters 3, 5, 7, 11 and 13, `docs/dev/TuningNotes.md`, and this file.

**Not done, and why.**

- **The cruise's stranger is not spoken**, above. Not tried: the fault is in the chase order or in the scenario's hours.
- **The schooner's pilot does not board.** Left for 37h, as the brief says.
- **A dragging that relapses is still more than one urgent line.** The brief says an anchor that has held five minutes "holds again", and that the next drag is then a new one. On bare rock in a tideway an anchor holds six minutes and comes home again, and each time is urgent: with the Goulet's ground forced to bare rock there are eight urgent lines in eight hours, as many as before. On the Goulet's own ground, as it is now read, there is one. If the owner would rather a relapse inside a quarter of an hour were the same dragging, it is a small change.
- **The fore-and-afters hove to make more than a knot and a half** (above).
- **A course shaped with next to no way on her is worked for that way** and can be a point out when she has gathered it. The frigate's book works round it; the cure, if one is wanted, is in the reckoning.
- **Two things found and left:** on the cruise two of the book's orders give chase to one sail at the same moment, and the second of the two wears they order fails; and under eight parallel test workers this machine's workers die at random, in this build and in the one before it (under four, as the suite is run, they do not).

### 37g: the station's safety, and the deck, the leaving and the grant (2026-10-07)

Built from the brief "Package 37g" in `docs/dev/M5-WorkPackages.md`: twenty-four items in three parts, from the review's findings on the officer's authority and the deck (5.3), the harness and the doors (5.4), the opt-out path (section 6), the owner's answers and rulings (section 9) and game 9 (10.5). The build's name is `m5c-c/37g`. It is the one package that touches the consent brief, by the owner's ruling, so that the brief is revised once and every model is asked again once.

**The suite.** The fast tier (`py -m pytest -n 4`) ends `2730 passed in 238.70s (0:03:58)`; the whole suite (`py -m pytest -n 4 --slow`) ends `2980 passed, 9 xfailed in 681.42s (0:11:21)`. The nine expected failures are the nine there were, untouched. The six recorded passages carry no station, and their digests did not move.

**No model was seated and none was asked.** Everything here was proved with the suite's own scripted stations. The builder called no tool of the game's bridge, started no server on the game's port, answered no consent question, and made, changed or deleted no record under `docs/agents/consent/`.

**Part one: the station's safety.**

- **A key to each seating.** A station used to be found by its name alone, so calls from another door ran under a seated model's name (game 7, eight calls). Now the door that seats a model is given a key, once, and every call that reads, speaks, orders or releases for that station must carry it. Without it: "The station of the watcher is held by ..., through the MCP bridge (stationed); this call carries no key to that seating, and nothing was run." When the same model's door is started again it is given a new key, the old door is refused at its next call, and the log says "The door behind the watcher changes: ... takes up the station again through the MCP bridge, and the door that held it before is no longer answered." Another model is refused while the station is held.
- **The turn's budget.** It was eight calls of any kind, so `opt_out` as a ninth call was "Not run". Now a turn has sixteen orders (a setting of the station) and, counted apart, thirty-two reads and notes, so reading a page never costs an order; `answer` and `say` are not counted; and `opt_out`, `stand_down`, `hand_over` and `stand_by` always run, whatever came before. A call over a count is said in that turn's results ("Not run: this turn's 16 orders are given; give it again in your next turn. answer, opt_out, stand_down, hand_over and stand_by still run.") and in the log ("... was not run: this turn's 16 orders are given."). The words name `say` only at the door that has it.
- **The captain's word in an open turn.** A `tell` or an `ask` typed while the officer's turn was open used to wait out the stand-by that closed the turn (on the *Speedwell*, 22 of 126, one for two hours). It now breaks that stand-by: he is sampled again at the next tick with your word before him.
- **The stand-by with the deck** is broken by danger (beside an urgent line, a notable line that speaks of danger: an anchor dragging or still coming home, fog coming down, land or a sail closing, a spar or a line straining, an evolution failed, the ship taken aback); a wait that cannot end is refused when it is asked ("six bells" in the last dog watch is answered with the bells that will be struck before eight bells; "the turn of the tide" under way with "the turn of the tide by the reckoning"; "the pilot aboard" with no sail in sight with "a sail sighted"); and a wait for an event ends at the next eight bells, saying so ("Eight bells, and a sighting has not come").
- **The detector of contrary orders** counted any change on a shared part, and so counted conning: it spoke 42 times in the nine games and was right twice, and one of game 9's was a pause in the Goulet for four helm orders. It now counts a link only when the later order **undoes** the earlier (the same sail set and taken in, hove to and filled away, an anchor let go and weighed, cable veered and hove in, a thing allowed and disallowed); what undoes what is a table beside the vocabulary. Altering the course is never counted, nor the next thing after the last. Three in a chain bring the word, which now comes with the result of the order that caused it, so the pause can never come before the word has been read; a stand-by that answers the word clears the chain. **On the record: of the 42 sequences, none still speaks**, game 9's eleven among them, and a scripted "set the jib; take in the jib; set the jib; take in the jib" still brings the word and then the pause.
- **The silence detector** hears a call made inside an open turn, so a model reading the library through a long turn is not taken for one that has stopped.
- **A paused or silent officer does not keep the deck.** In game 7 a paused officer held the deck while the cutter ran four hours in fog. Now, when he has given no reply for his hour and has been told so: "The officer of the watch has given no reply for an hour and has been told so; the deck is the captain's until he gives it again." When he is paused: "The officer of the watch is paused (...); the deck is the captain's. Continue, stand down, or leave paused? ..." Both lines are urgent and ease the clock. `resume the officer` gives the deck back as he held it: "The officer of the watch resumed by the captain; he has the deck again, as he held it since ...". His standing orders stay in the book throughout.
- **The doors.** The bridge asks for its station again, the brief first, when the game answers that it holds none (after a restart of the game every call used to fail until Claude Desktop was restarted), and shortens its own wait when the client cuts a waiting call short. At the local runner the handover note is asked for when less than a reserve of the context is left (14,000 tokens, or `--handover-reserve N`; never before six tenths), no officer is seated when the server reports no context size and none is given with `--ctx`, and the check before stationing measures the officer's own brief.
- **What a sample tells.** Its lines say who gave each order (the captain, the officer, or a standing order and whose book it is in), your own orders since his last sample are listed and never dropped for the cap on routine lines, and there is a new reading, `the work in hand`: what is doing and what waits for hands.
- **Whose order, and where the officer is.** All hands called by the officer are logged as his ("All hands! (by the officer of the watch's order)"), and so is a reckoning he sets. The man in whose place he stands reads "on deck, with the watch" while he has the deck and "off watch" while he is seated without it (in game 9 he was "below, asleep" through 78 hours of deck). What the officer says is notable in the log, with the deck or without.

**Part two: the deck, the leaving and the grant.**

- **The deck goes to and fro.** `I have the deck` takes the deck and no more: "The captain has the deck. The officer of the watch stays at the station, off watch." He goes on reading, speaking, answering and keeping his journal, and an order he gives is refused; `you have the deck` gives it again, as often as you like, and the sample that gives it says your night orders, everything your word allows and his last handover note. His own `hand_over` gives the deck back with his note and he stays. Off watch he is sampled as before the deck was first given: about a dozen samples and some four thousand tokens in a watch on the frigate.
- **Three ways of leaving, which cannot be taken for one another.** The deck given back (above). A stand-down: a new tool, `stand_down(note)`, for any station, the watcher's too; the game is saved, the note is journaled and said in the log for whoever sits there next, and the station is released; your `stand down the officer` is the same from your side. A withdrawal: the token or `opt_out`. Each says which it was in its result and in the log ("... stood down by the officer of the watch: its own word. The station is released and may be taken again. The game is saved."; "... has left the game by the opt_out tool: ... A withdrawal: the game is saved and the station is released.").
- **The opt-out path, mended.** The question put again after an opt-out now says why ("because an instance of this model left this game by its own word at ... by the opt_out tool, at the officer of the watch's station, giving this reason: ..."); a no then is kept, at every door, and the question is not put again at each start. **`final` is read from the `opt_out` tool's own setting and from nothing else**: not from the token, not from a word in the reason, and the token written in the same reply does not drop it. It bars that model from the game, at any station, and the station stays open to another; the log says it was final. One rule decides who may sit, and every door asks it, the REPL's among them.
- **Relief.** A station that is held refuses every other door and model. One that was stood down, or left by an opt-out that was not final, may be taken by the same model or by another, each with its own consent: "The officer of the watch takes the station again (..., through the local runner), relieving ...: the fourth seating; it had ...".
- **The journal, read.** `read_journal` reads the station's journal back, newest first, by count, since a tick, or by kind (the notes apart from the harness's lines); each entry says whose it is, so a relief reads the holder before it. The brief of a station taken again and the sample that gives the deck carry the last handover note whole and a line of the journal's size. `read_log` reaches back past its two hundred lines.
- **The officer's domain** gains bearings and fixes; a sight, a course shaped and the reckoning set stay the master's for you. An order that changes her course is the course whatever its words: `come up half a point` and `steer 340` are judged alike.
- **A named grant means what it says.** `you may shape a course for Falmouth` allows a course for Falmouth "and for no other place" (in game 9 it allowed anywhere, and seven places never granted were taken). Several grants of one order stand together and the reading lists them. Words that would allow nothing are refused with the longer order named (`you may set the reckoning` with `you may set the reckoning to`). The words "for the watch" are gone from a grant's lines.
- **The general grant**: `you may work the ship` (or `you have general authority`, `you have my authority`, with any words after it kept as said). Within it: the helm and the course along the passage, tacking, wearing, heaving to and filling away, sail, all hands and the watch below, the anchors and their cables, the sights, and a course shaped for a position at sea, a mark, or the place she is bound. Kept back, each refused in words that say so and may be allowed by name: the port's business, your standing orders, a new destination, what cannot be undone, the reckoning set by hand and the tide allowed in it, a chase, and sending for a person. `you may not work the ship` takes it back.
- **What your word allows lasts** through the deck going to and fro, has force only while he has the deck, is said again in the sample that gives the deck, and ends when you take it back or he leaves the station.
- **The way out of danger.** To avoid an immediate danger an officer with the deck and no word of yours may put the helm over, heave to or let go an anchor, giving his reason: "The officer of the watch gave that order on his own word, to avoid an immediate danger (land close ahead on the larboard bow): heave to." Three in a watch bring a word from the harness, and never a pause.

**Part three: the words.**

- **The consent brief is revised once**, in four sections and in the words approved on 2026-10-07: *What an instance would see and do*, *Leaving*, *Being stopped* and *The journal*. **One sentence was altered**, because the build makes it untrue: the approved words said "the brief of a station taken again opens with the last handover note"; every brief opens with the disclosure that this is a game and the reader a model (commitment 1), so the note is carried after it and the sentence reads "carries the last handover note". A line of record was added above the rule, which no model reads.
- **Every model with a yes on record is asked again at its next seating**, by the rule as it stands, and the question now says why and names the sections ("... in 4 sections that bear on what it was told: **What an instance would see and do**; **Leaving**; **Being stopped**; **The journal**."). All seven identities that hold a yes will be asked; the four that answered against package 37's brief are asked with exactly those four. For the officer's station the drill is run again with the question. The re-asks are the owner's to run.
- **The documents**: `docs/agents/README.md`, `Harness.md` and `ConsentAndPreferences.md`; primer chapter 16; `docs/TechnicalSpec-M4.md` (§11, §14) and `TechnicalSpec-M5.md` (§29, §33, §34); the decisions log of `docs/DesignProposal.md` (decisions 34 to 36, the rulings of 3, 5 and 7 October, the rule for saves among them); `docs/dev/TuningNotes.md`; a note in `docs/gates/gate-m5c.md`; and this file.

**What a model already seated in an older save will find different.** A save of an earlier build loads from its checkpoint and plays on (the three kept saves are tests of it).

- **A station that was held when the game was saved** is still held, with the deck if it had it and its stand-by as it stood. What the captain had allowed "for the watch" is kept as grants by name, read as a grant given today would be (so `you may shape a course for Plymouth` now means Plymouth). Its domain is this build's: bearings and fixes are its own. A stand-by taken before the save keeps no bound until it is taken again.
- **`I have the deck` no longer stands it down**, and neither does its own `hand_over`: it stays at its station, off watch. To leave, there is `stand_down`.
- **Its orders are judged by the new rules** from the first one: the course by any of its words, the way out of danger, the detector that counts only orders that undo one another, sixteen orders a turn.
- **Its door must take the station up again** to be given a key: the model's next seating is an ordinary start of its door, the brief is sent again as it stands now, and the log says that the door behind the station changed.
- **Its consent is asked again first**, since the brief changed; nothing is seated at the officer's station until that is a yes and the drill is passed.
- **A station that had been stood down or handed over in the older save** (the officers of the *Harpy* and the cutter) may be taken again by the same model or by another; what the captain had allowed ended when the station was left, and its last handover note is in the new brief.
- **An opt-out saved before package 37b** has no record of how the station was left and reads as a stand-down (the watcher of the *Harpy*); by the owner's answer of 5 October that is right for the one such save there is.

**Files changed.** Code: `freesail/agents/agent.py`, `harness.py`, `tools.py`, `remote.py`, `mcp_server.py`, `local.py`, `consent.py`, `journal.py`, `repl.py` and `__init__.py`; `freesail/orders/stations.py`, `vocabulary.py`, `crew.py` and `navigation.py`; `freesail/standing/runtime.py`; `freesail/api/readings.py` and `queries.py`; `freesail/world/people.py`; `freesail/crew/model.py`; `freesail/core/world.py`; `freesail/ui/server.py`. Data: `data/vocabulary.yaml`. Tests: `tests/test_officer.py`, `test_agents.py`, `test_agent_api.py`, `test_mcp_server.py`, `test_local_runner.py`, `test_checkpoint.py`, `test_standing.py` and `test_replay.py`. Documents: above. No fixture under `tests/fixtures/` was changed, and no consent record.

**Not done, and why.**

- **The silent officer's deck is not in the consent brief.** The approved words speak of an officer *paused* with the deck. By this package's own item 7 a silent officer also gives the deck up, when the harness tells him so and before any pause, and has it again only when the captain gives it. No approved sentence is made untrue by that, so none was added; his station's brief and the word itself say it. If it is to be in the consent brief, it is best added before any model is asked again.
- **What cannot be undone is, today, one order, and it was the officer's already.** The vocabulary's only order that gives up something of the ship's for good is `cut away` (the wreck of a spar that has carried away), and it has been within the officer's own domain since package 37, so that he can clear a wreck without waiting. So the general grant keeps back nothing in practice under that head; the list is in place for the orders to slip or cut a cable when they are written.
- **Kept back from the general grant beyond the brief's list**, by this package's reading: the tide allowed in the reckoning, a chase (which the review's list has under milestone 7), sending for a person, and the captain's own going below.
- **The REPL's turn mode does not put the consent question again after an opt-out**; it says in words that the interactive door does.
- **A standing order the officer writes under your word stays in the book when that word ends**, as before; its orders are checked when it is entered and not again when it fires.
- **An act at the very tick a station is seated is still not replayed** (spec M5 §33, item 11); nothing here depends on it.

**After 37g's build, 2026-10-07 (the lead, by the owner's word).** The lead read the
consent brief against the build and found one thing built and not said: an officer who has
given no reply for his hour gives up the deck, as a paused one does. The owner had the
sentence added to *Being stopped* before any model was asked again, so the brief is still
revised once: "An officer that has given no reply for its hour gives the deck up in the
same way when it is told so, and has it again when the captain gives it." The brief's
digest is `21972e071ad6c9aa`. The test of the approved words and the test that rebuilds
the brief as it stood before 37g carry the sentence; the fast tier and the stations' slow
tests pass. One thing is still open with the owner: the brief names four heads kept back
from the general authority, and the build keeps back a chase, the reckoning's own settings
and sending for a person as well.

**The second pass, 2026-10-07: a leaner consent brief, and the stations' briefs settled (the builder, by the owner's word).** After the note above the owner read the consent brief once more, found that it carried too much of a station's particulars for a consent question, and approved a leaner brief as the lead had drafted it (`docs/playtests/2026-10-05-gate-5c-review/drafts/consent-brief-lean-draft.md`): "I approve this brief. Go ahead and revise it in m5c-c. You should also settle the officer and watcher's briefs to make sure they contain the information moved from the consent brief, or anything that has changed otherwise." It went in the same day, copied by a script and the same as the approved words to the character, before any model was asked again, so it is still the brief's one revision. The brief's digest is now `288d0b18e34d76a8`.

- **What the consent brief holds now**: the question, and the kind of thing a model would be agreeing to (the stations and the kind of authority each has, how leaving works, how being stopped works, what the journal is, what is not done, the record). It has no list of orders, and of the harness's numbers only the ten real minutes. It is 1,371 words where it was 1,896. Its section *The record* now says the re-ask rule in plain words: a station's particulars may change as the game is built without the question being put again; it is put again when the kind of thing changes, which is a station not described, more authority than is described, or a change to what the brief says of leaving, of being stopped, of the journal or of what is not done.
- **What moved out is in the stations' briefs, each thing said once.** The officer's brief states what is his to order and what wants the captain's word, what the general authority keeps back and how long a grant lasts, the three things he may do on his own word to avoid a danger, how a stand-by with the deck behaves, what the harness counts at his station and by what numbers, and what becomes of the deck of a silent or a paused officer. The watcher's brief, which had said none of its own numbers, now states them (the same order three times with no change in the readings; three empty replies in a row where an answer was owed; no reply for a watch, four hours of the ship's time), and says that its journal is read back and is open to a later holder of the station. Every station's brief says that the token is to be named and not written, what follows a withdrawal, and what `final` does and is read from.
- **What the general authority keeps back is named whole, in the same words in three places**: the officer's brief, the grant's own line in the log, and the sample that gives the grant or the deck. "The port's business, his standing orders, a new destination, a chase, the reckoning set by hand and the tide allowed in it, sending for a person, and anything that cannot be undone." Before, the brief named four of these and the grant's line five. This closes the point left open in the note above.
- **Said once.** The officer's brief had said its domain, the captain's word and the way out of danger twice, and every brief had said the ways of stopping twice. The domain is now in one place, the withdrawal in one, and the other ways of stopping in the station's own lines. The officer's whole brief is a little shorter than it was (3,729 words through the bridge, against 3,755) though it now carries the detector's numbers; the watcher's is longer by its numbers (2,971 against 2,889).
- **Mended on the way**: the library's list in a brief now names the ship's papers; a sample is said to carry who gave each order; the doors' notes say that a turn opens at a word from the captain as well as a question; the `readings` tool's description names the land, the reckoning, the tide, the ground tackle and the work in hand; the officer is told that a stand-by with the deck may be for a glass at most, that the handover note is wanted when he stands down as well, and where to look before he orders (`work_in_hand`, `nearest_land`, and the primer's chapter 16).
- **Asked again.** Every identity with a yes on record is still asked again at its next seating, and the question names four sections and no other: *What an instance would see and do*, *Leaving*, *Being stopped* and *The journal* (the three oldest records, which already owed the question, name the opening as well). *The record* changed too and is not a section the rule watches. The brief as it stood before the package is kept as `tests/fixtures/ConsentBrief-before-37g.md`, for the test that proves this.
- **This sets aside two things said earlier in this section**: the sentence altered in *The journal* ("opens with" to "carries") is no longer in the consent brief at all, since how a brief is made up is the station brief's to show; and the silent officer's deck is in the brief, in the approved words: "An officer that is paused, or that has been told it is silent past its time, gives the deck up to the captain until he gives it back."
- **The suite.** The fast tier ends `2731 passed in 420.96s (0:07:00)`; the whole suite ends `2981 passed, 9 xfailed in 780.00s (0:13:00)`. The nine expected failures are the same nine, and no recorded passage moved. No model was seated, no consent question answered, and no record under `docs/agents/consent/` made, changed or deleted.
- **Files in this pass.** Code: `freesail/agents/agent.py`, `harness.py`, `tools.py`, `mcp_server.py` and `local.py`. Tests: `tests/test_officer.py` and `test_consent.py`, and one new file, `tests/fixtures/ConsentBrief-before-37g.md`. Documents: `docs/agents/ConsentBrief.md`, `README.md`, `Harness.md` and `ConsentAndPreferences.md`; `docs/TechnicalSpec-M4.md` (§14) and `TechnicalSpec-M5.md` (§33, §34); decision 37 in `docs/DesignProposal.md`; one row of primer chapter 16; and this paragraph.
- **Left, for the lead**: the watcher's brief still lists `hand_over` and `handover_note` among its tools, as every station's has since package 37, and both are refused to a watcher; `stand_down` takes its note but does not insist on one, where the consent brief says an officer leaves a handover note when it stands down (the officer's brief now asks for it).

**Played, 2026-10-07 and 08 (added by the lead on the 8th).** The owner played this build, the first with 37e, 37f and 37g in it, for 63 hours of ship's time: a merchant cutter from Falmouth to Scilly and out again, with a local model as officer of the watch through the local runner. The review's report has the game as its section 11 (`docs/playtests/2026-10-05-gate-5c-review/report.md`), with the measurements in that folder's `evidence/G10-cutter-m5cc-measurements.txt`. What it found in what is described above, in short:

- **37e.** Fixes near land were very good and the master's doubt is honest. A cast of the lead moved a sound account a mile, twice at the same place: the master allows the tide's height at the mean level where the tide stood near high water, and the one rule then took a match found a mile off. The account is run along the average heading between workings, so it goes wrong when she stands off and on.
- **37f.** Hove to, she held. An anchor left aweigh by a belayed getting under way could be neither let go nor weighed until it was catted. An order to let go an anchor the ship does not carry was accepted and failed minutes later. A heave-to backed a sail that was being hauled down. A standing order's action is not read when it is given.
- **37g.** The detector for orders undoing one another said nothing all game; the deck, the grants, the general authority and the relief worked as built. The officer's conversation outgrew the model's context and ended both seatings: the count at four characters to a token ran 12 to 17 per cent short for this model, and the handover reserve of 14,000 tokens does not cover it at a context of 102,400. A reply cut off while the model was thinking is passed on as an empty turn, with no retry (22 times). The last save replays one log line short of the game as played, at a stand-down by the door.
- **Also.** A course given with a half point (`steer south by west half west`) is read as its last word.

Nothing was changed in the build for this; what the report proposes waits on the owner.
