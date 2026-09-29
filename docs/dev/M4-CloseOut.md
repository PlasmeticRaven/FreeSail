# Milestone 4 close-out: the package 29 set

A record for the owner and the lead of what the last three packages of milestone 4 built
(29, 29b, 29c), what moved and why, what the three playtests of gate 4c found and where
each finding went, and what milestone 4 hands to milestone 5. Not a gate: gate 4c was
passed on 2026-09-29 (`docs/gates/gate-m4c.md`, decision 26) and this note closes the
milestone's code behind it. Written 2026-09-29 as 29c merged.

## Where milestone 4 ended

The suite: 1565 passed, 7 xfailed (the seven are the owner's rulings on truths 3, 11,
18, 24, 26, 28 and 31, unchanged since milestone 3b). Truths 1 to 51. Four gates passed
(4a, 4b at its third build, 4c), nine playtests filed under `docs/playtests/`, six consent
records under `docs/agents/consent/`, the gate 4c release `gate-m4c` published. The main
branch carries the path fix found at the 4c cut and the three close-out packages below,
which the release does not; the first M5 gate is cut on all of it.

## Package 29: the ship sails herself (gate 4c)

The weather script as scenario data (`data/scenarios/gate-4c-day.yaml`), the wind veering
and rising to a gale in the middle watch and easing by dawn; `speed N` to 300 with the log
rolled up by the hour at 60x and above, the same roll-up in a model's samples; an urgent
line easing the clock to 1x; a day saved at any tick and replayed to the same digest;
`--load` and `--scenario` on the server; `tell the <station>` as a word beside `ask`'s
question; the playtest form; truths 48 to 51; performance from 420 to about 1000 ticks a
second by caching (truth 51's floor 500; the spec's 3000 not met and left). The shift
evolution learned to take a drawing sail in before setting the new one, and the starter
book gained the storm-staysail companion line and, by the owner's ruling, the topgallants
in its shortening line.

## Package 29b: the findings of the gate's day

From playtest 7 (Sonnet 5.5 through Claude Desktop, the whole day) and the owner's
rulings on them.

- **All hands is a pool action** (decision 25). A call for all hands turns the watch below
  up and changes who is on deck; a reef or a furl with all hands takes the idle hands and
  the arrivals and belays nothing, the work in hand finishing and its hands joining.
  Manoeuvres (tack, wear, boxhaul, wearing short round, lying a-try) keep the belay by an
  explicit `belays: true` in their files, since "ready about" stops the work; truth 19
  stands. Sending down the topgallant masts belays only the sail work on the masts being
  struck, a parts rule and not an all-hands one. On the gate's day the topgallants now
  come in while the reef is being taken, and one call per firing replaced six calls and
  six pipe-downs, which turned out to be the whole of the fatigue finding: the crew now
  peak at tired rather than worn out, and no fatigue constant moved. The night's end at
  04:00 doubles as the hour a call costs broken sleep; moving it to Luce's 07:00 is a
  structural item in the tuning notes for later.
- **The redelivered question**: a fold into an open turn carried the sample's question
  again; a fold now carries a question only if it is new.
- **Trim on a shift**: the starter book's eighth line; the dialect gained its one "or"
  (`veers 1 point or backs 1 point` is one comparison, and `shifts N points` means either
  way); a shift that fires is spent, so the order stands again; a trim already in hand is
  folded, not stacked.
- **The mean wind**: a ten-minute record; `the mean wind` and a gust-or-lull label in
  the registry; the gust line says the mean; the roll-up says the mean of the hour.
- **Grouped log lines**: one line for a gust's alike strains (79 lines of the day became
  14), one for a trim's twelve braces.
- **The strain wake-up word**: the event was always matched on the log's kind; the model
  was not told, and now is, in the tool and the brief.
- **A station's words are never rolled up**: any station's actor is kept as the captain's
  is, the set registered by the stations themselves.
- **Setting from in the gear**: the stow-undoing step runs only from furled; from in the
  gear a short deck step takes its place for square, gaff and jib-headed sails, with
  `instead_of` in the step so the nominal timings and truth 18 do not move.

What moved: the day's digest (427 lines from 480, by the grouping), `GATE_DAY_SHORTEN_SAIL_TICKS`
(three firings, not two, since the reefs finish earlier under one call), truth 48's
heavy-weather count (three orders carried out and the close reef refused as already
done), truth 50's counts, the starter book's line count. All in `docs/dev/TuningNotes.md`.

## Package 29c: belaying work, and the harness findings of playtests 8 and 9

From playtest 8 (Qwen3.8 27B, the local runner) and 9 (Gemma4 26B, the same), and the
owner's rulings.

- **Belaying work** (`freesail/orders/work.py`): `belay <the work>` by the log's name, by
  the order's words, by the kind of work or by its subject; `belay that` for the last
  order whose work is still in hand or waiting; `belay all work`; "avast" as the period's
  word (Falconer 1780). The hands are released and the job is gone, a sail half set left
  as its last finished step left it, the log saying what was belayed and how it was
  left. Every form the captain of playtest 8 tried now parses. The manoeuvres' own belay
  keeps its name and its line.
- **A named party that cannot man the job is refused at once**, with the numbers ("The
  idlers are four; reefing the mainsail wants ten. Call all hands, or name the watch.");
  the watch on deck short of hands still waits.
- **`answer` and `say` are always allowed past the tool budget.**
- **A leaked thought is not a line a sailor said**: a reply opening with a thinking tag is
  journaled as a fault and not written into the log, the model told at its next sample;
  the tag only, no length rule. The door note's two sentences about the turn's end became
  one.
- **An empty reply where an answer is owed counts toward the nudge**, three bringing the
  nudge and a fourth the pause; an empty reply at a plain glass is a decision and is not
  counted.

## The playtests and where each finding went

| Playtest | Model, door | Findings | Where |
|---|---|---|---|
| 7 | Sonnet 5.5, Claude Desktop | eleven, listed in its notes | 29b (faults 2 and 8, the starter line, the reading, the groupings, the wake-up word, fatigue); the world's absences to M5; the gust factor to the weather study and package 30 |
| 8 | Qwen3.8 27B, local runner | the stuck mainsail, the answer past the budget, the bend-a-storm-sail chain, the wind's build | 29c (the first two); the schooner's `shift the mainsail for the storm trysail` an M5 open item; the wind's build to package 30 |
| 9 | Gemma4 26B, local runner | the leaked thought, the empty replies, the door note's wording | 29c |

## What milestone 4 hands to milestone 5

Spec M4 §24's open items as they stand: install simplification (6); windage under bare
poles (7, measured in package 31); compression and the model (8, built); the context
budget and the handover (9, the budget script built, the handover not); the local model
as the function baseline (10, confirmed by playtests 6 and 8); a station offered only to a
model that can hold it (11, the fitness drill not built). From this note: the night's end
constant split from the broken-sleep hour; `--load` and the Claude Code door unexercised
live, carried to gate 5a; the schooner's storm trysail shift; re-manning a released
station in a loaded game; the sail room in the browser, held for M5's places. The
design notes of 2026-09-29 (`docs/design/InwardAndOutward.md`, `Presentation.md`) and
the four M5 studies were written beside this work and are the milestone's other output.
