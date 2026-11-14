# Records reader 02: `docs/dev/M7-WorkPackages.md`, lines 5341 to 10510 (the packages' own sections)

The record is cited as `WP:<line>`. Code is at the commit under review. My half is almost
entirely **briefs** (what each package was asked to do), the lead's dated rulings inside
them, and, from `WP:9754` to the end, the lead's running notes to the ships session (package
75). **The "as merged" records of the packages are not in my half**: they sit in the head
(`WP:1262` to `WP:5165`, the other reader's). To answer (a), (b) and (c) I read the merge
records I needed there and say which (`## What I did not read`).

One short run settled several points (scratch probe, first action, seed 7, no key; output
quoted where used): `open the gunports`, `read the letter`, `the things`, `the ship`, `the war`,
`the date`, `hoist/haul down the broad pendant`, `the flags`, `dress ship`, `undress ship`,
`splice the main brace`, `tow her with the boat`, `beat to quarters`, `the guns`.

---

## 1. Where the record and the thing differ

**1.1 Package 74 is recorded "closed" with "the cruisers and the far fight" (`WP:4500`, run 71
"green whole"); the far fight it wired has a fault found after the close and not mended at
the commit.** On 2026-11-12 the lead, bisecting a test of the ships session's, found the 64
"stays 'on passage' and never engages", passing before 74's step 4 (cae5c333) and failing
from its merge (9944b671) (`WP:10498`). On 2026-11-13 he confirmed the cause: "a far ship of
war that goes engaging from a plan state ... `resolve_state` plans `("chase", None, ...)`, the
leg is dropped and the vessel marked done" (`WP:10500`), and gave the mend to package 75's
branch "(package 74 is closed and its files are free)". At 504a250 package 75's step 7 is "NOT
merged" (`WP:10498`, `WP:10500`; the record's last note, `WP:10510`, still before its hash), and
`freesail/world/brains.py:1053-1058` still plans `("chase", brain._stranger, ...)` with no
mark kept in hand. The closed package's record was not amended. *Weight: medium; sure.*

**1.2 The lead took a failing pace test out at a merge, under a head rule that forbids it.**
Every brief binds "never a test skipped, disabled or quarantined" (e.g. `WP:5470`, `WP:9735`).
At the 74's merge (2026-11-10): "I took its test out at the merge myself ... so that the
cloud's pace job is not red on it ... `test_truth_7_196_..._ticks_at_the_build_machines_floor`
is gone" (`WP:10496`); confirmed in the tree (`tests/test_bellerophon.py:2188-2196`: "The test
that asked it was taken out by the lead at the merge"). The lead's own earlier answer (5)
("pinned only if ... 550 or more; else recorded") is given as the warrant. Whatever its merit,
it is the lead waiving a head rule he enforces on builders, and the brief's item ("the pace of
a 74 crewed measured against the floors", `WP:9695-9696`) then had its crewed clause rewritten
too ("the docstring's 'in action' taken out", `WP:10500`), under "the owner's standing rule of
2026-11-12: a test superseded by design is accepted where said". *Weight: medium (method).*

**1.3 Package 111's brief promised a tool that "reads the chart as the game reads it
(`freesail/world/chart.py`, `tide.py`, the weather, the ports' loader)" (`WP:9196-9197`). The
tool re-implements the tide's blend without the seam's taper** (`tools/audit_chart.py:680-691`
against `tide.py:484-535`; `code-10`), and the merge records say nothing of it. The review's
row in head 5.4 stands and the record is the source of the claim it refutes.

**1.4 Package 102 (closed, `WP:5054`) as briefed against the thing.** Built as briefed and
proved in the probe: `dress ship` / `undress ship`, the flags reading, the days' files for
Britain, France and Spain. `splice the main brace` was "with it, if small" (`WP:8343-8344`)
and is not built; the probe's answer is the parser's ("There is no such part as the main brace
in this ship; did you mean the main topsail brace ... ('splice' was understood.)"). The record
says it was not built (`WP:4547`; TuningNotes 26727), so the record is true; the player's
answer is wrong (it should say the order is not in the game, not look for a rope). *Low.*

**1.5 Package 85's "the ship" reading answers "The ship: The ship: Sherbourne, H.M. armed
cutter ..."** (probe). Small, but 85's brief item 5 and its in-world guard (`WP:7528-7536`,
`tests/test_in_world.py`) are about exactly this text. 85's item 2 promised "no form the book
gives is refused" (`WP:7508-7510`); the review's faults (`faults-*`: every `veer` refused while
the primer's "every form is taken" stays green) show the guard does not hold that promise.

**1.6 Package 98's probe was briefed to skip, and runs were then recorded "green whole".** The
brief: "In the slow tier, skipped where no browser is named, as `tests/test_pictures.py` is"
(`WP:7767-7768`). The record was honest at the time (run 59: "the probe's nine tests, which skip
on the runner ... so the probe is proven on the build machine's slow tier and not in the
cloud", `WP:3665`), and the lead later corrected "every run recorded as 'green whole' up to run
77" (`WP:119`). Between, each cloud run was recorded "green whole" or "green". See (c).

**1.7 Where the review should be corrected or sharpened from this half.**
- *Ships as code* (review §3.3, F2.1): not drift. "The per-ship generator modules under
  `tools/ships/` imported by `tools/gen_ships.py`, the lead's structural decision, agreed"
  (`WP:9641-9642`, 2026-10-28) and "the ship files never edited by hand" as a head rule
  (`WP:9734`). The review should say it was decided, by whom and when.
- *The wheel shot away* (review §5.3, 5.3 item 8): the record shows how it was lost, not only
  that it is (see (d)).
- *The browser's hiding a grey* (decisions 59, 62): package 99 is the project's own design for
  exactly this ("each datum they draw ... the last value he learned ... drawn as such"), **held
  by the owner 2026-11-09** (`WP:7829-7842`). Known and booked; the review should say so.
- *Sight across the land* (F2.8): booked to package 78 from 71's brief on (`WP:5425`,
  `WP:5465`, `WP:5569`), never briefed in my half.
- *Ships on the land* (F2.8): package 109's step 5 measured it, mended the goal squares and
  said plainly "eight of thirty-five vessels still cross land at some sample, which is the
  steering's, package 61's" (`WP:5124`, the brief `WP:9055-9065`). The review may cite the
  project's own count.
- The review's head 3.7 on the browser tests is right and is the project's own finding (`WP:119`).

## 2. What the project already knew

| Review finding | Known? Where | What was done |
|---|---|---|
| The boundary (core imports agents) | No mention in my half ("boundary" here means a step's boundary). | Nothing booked. |
| The director's reach onto the player's ship | **Briefed as a feature.** 84's item 9: the forms "with a hull (`aboard the Raven: ...`, the followed when none is named ...)" (`WP:7670-7675`); 82's re-brief: "where the director's `aboard:` without a name goes, and what `captain: carry on` gives back" (`WP:7123-7126`); 74's item 7 the forms for "a prize condemned or restored ... a new command" (`WP:5785-5790`) and the close's form `ship "<name>": a prize of the <captor>` (`WP:4474`). The only limit in my half: "through plausible causes as always" (`WP:5755`). | No brief asks the limits ("cannot move the player's ship", "nobody dies") to be tested against these roads. Not known as a hole. |
| The checkpoint as a program | No. | |
| The server's open socket | No mention. | |
| Consent brief vs code | 74's item 6: adversarial seats refused until 55 revises the brief (`WP:5774-5784`; built: `world/seats.py:73-76`, `agents/remote.py:506-511`). The operator-voice rule appears once, as a truth's wording: "nowhere in the operator's voice, by the test's fake door" (`WP:5797`). | Decision 17(a)'s hole not known here. |
| True position on the wire | No. | |
| No player Python | No mention of a sandbox in my half. | |
| Evolutions and ships as code | Ships: decided (`WP:9642`, above). Evolutions: 85 moved build notes below a served head (`WP:10129-10134`), nothing on the scripts. | |
| The newcomer's first hour | **Not in the M7 record at all**: "tutorial", "first game", "newcomer" occur only in 114's brief (`WP:9457`). Package 96 (the harbour) is a configuration design, held to the milestone's end (`WP:7317-7406`, `WP:8254`). | Nothing booked. |
| Guns left secured | No (see (d)). A cousin is known: "with every port of a side shut, `engage` answers 'the guns to fire as they bear' and nothing follows" (`WP:237`, booked to 77, `WP:8413-8416`, 77 not launched). | Booked, unbuilt. |
| Purchase with the boat lost | The lost boat is known in other roads: 60's reading "A lost boat is used and comes back whole" (`WP:5027`) and "the boat lost outside a transfer ... leaves him in no hull and not dead" (`WP:5163`). The trade's road is not named. | Booked to 60, not merged. |
| Far world's faults | Ships on land: measured, booked to 61 (above). Far fight: 1.1. A far ship reading another's true class: "a far vessel reads another's true class whatever could be made out (`world/ships.py` about line 1943)", given to 75's Phase 5 (`WP:10498`). The far fisherman, the Black Rocks: not in my half. | In flight on an unmerged branch. |
| Tests that cannot fail, twins, hand-kept tiers | The tiers: the lead moves tests in and out of `SLOW_TESTS` by hand at merges ("mark truth 7-191 (7.5 s) ... slow", `WP:10480`; "I measure the tier on the build machine at each merge", `WP:10486`). Twins: no mention. | The hand list is the method, not a known fault. |
| The pace floors on the edge | Known and recurring: runs 51 to 56 and 59 short "(388 to 445 ticks a second against 500) on a slow runner's hour" (`WP:3665`); "It goes to the cold review with the earlier notes on those floors" (`WP:5016`); 7-196 removed (1.2). | Sent to this review. |

## 3. The method, as this half shows it

**Briefing.** The lead writes every brief; the owner approves in a sentence ("109 is approved
as briefed", `WP:8994`; "114 is approved by the brief", `WP:9412`). Early M7 briefs (70 to 75,
82, 84) are "generously scoped": "the brief binds the intent ... the builder designs, takes an
item another way with its reason, grows a part where the work shows it should ... no day
count" (`WP:5347-5350`, repeated in each). Late briefs (98 onward) are "steps, each at one
hash", "under 600 words" reports (`WP:9076`). The lead hands builders "the ground as the lead
had it read ... to check, not to trust" (`WP:8258`, `WP:8393`), sometimes "every line FROM
MEMORY" (`WP:8595`).

**Who builds.** "[the senior model]" for design-heavy packages, "[the second model]" for the rest; package 75 by "the
owner's own local session" on its own branch, which the lead "cannot message" (`WP:9756`) and
whose reports sometimes never arrive ("No bridge message of yours reached me: this session lay
dormant from the 8th to the 9th", `WP:10488`; "your message of the 8th never having reached
me", `WP:10490`; "its message was refused on the way", `WP:10187`). The remedy was a file the
ships session watches (`docs/dev/ShipsNudge.md`, `WP:9756`).

**What a builder runs before reporting.** In 2026-10-28's form: "the fast tier once on the final
tree and the slow tier of the touched files; ... the whole suite is the lead's in the cloud at
the merge" (`WP:7584`, `WP:7705`). By 11-11: "ruff check and format; the fast tier whole; the
slow tier of the touched files and of the known truths; the pace alone and last" (`WP:8360-8362`).
The browser plans entered the builder's list only after 109's miss (`WP:9634`: "the browser
plans none skipped").

**"Green".** Has meant: the builder's fast tier; the lead's fast tier on a trial merge; the
cloud's six shards (without a browser until run 81, `WP:119`); with or without the pace job
(merged with the pace job red, `WP:3665`). "Green whole" was used of runs that skipped the
browser plans and was corrected later (`WP:119`).

**How a pin moves.** "Old beside new, proven by bisection" or "by a toggle" in every brief
(`WP:5469-5470`, `WP:8358`). In practice the lead re-pins digests himself on the build machine
("The seven digests of the trim's words are mine and I re-pin them at the merge", `WP:10498`;
`WP:10494`: a pin moved by a ruled build "found by the cloud's run 62 and re-pinned by the
lead"). The owner's "standing rule of 2026-11-12" lets a test "superseded by design" be
rewritten "where said" (`WP:10500`; used in 109 step 1, `WP:4702-4706`).

**What goes to the owner.** Put well (a non-programmer can answer it): 77's six questions,
"each answerable in a word (the lead's recommendation first): (1) the hands for damage control
as 3(a) has them: yes ... (4) Fire aboard left out and unbooked for now: yes" (`WP:8476-8482`).
Put badly: 82's re-brief, written "for the owner's approval" (`WP:7086`), asks him to approve
"86's three seams reworked on it: the free intent by the hull and not `parent is None`,
`hail.model_holds_her` by the hull a model or the player holds, `_named_or_kind` by
`World.players` and not `player_shadow`" (`WP:7127-7129`). Most rulings to the ships session
(`WP:10219-10510`) are taken by the lead alone, by number, at a density only that session reads;
a few are the owner's own words relayed (`WP:10502`, `WP:10504`).

**Growth, splitting, re-opening (this half).** Lettered: 79a, 79b, 79c, 79d (`WP:6242-6527`);
82b (`WP:7210`); 103a (and 103b) (`WP:9614`, `WP:8140`); 106, 106a, 106b (`WP:8742-9079`);
78b and 65b named (`WP:8377`, `WP:6879`). Refreshed or re-briefed after first brief: 74 (twice,
`WP:5833`, plus 86's and 97's lines), 82 (`WP:7086`), 103 ("AMENDED", `WP:8125`), 77 (`WP:8446`,
item 4a added by the owner). Re-opened after close: 74's far fight (1.1), and 109's whole
reason for being: mends of merged work (b). Package 75's notes show a single package running
from 2026-10-28 to past 11-13 through sixteen dated merge-and-ruling cycles (`WP:9758-10510`).

**What went wrong, and whether the remedy was applied.** "The lesson kept: a step that changes
what an order answers runs the browser plans, and a trial run is not cancelled for another"
(`WP:4716`): applied (`WP:9634`; runs 83 to 91 name "the browser plans", `WP:4870-5142`).
"Any change to a line every ship may say ... can move a recorded passage ... say in the report
which lines of that kind a step changes" (`WP:10494`): written for the ships session; no check
enforces it. Builders' containers lacking Playwright or websockets: a setup script (`WP:117`).

## 4. The cost, as this half shows it

- Usage limits: "65 pauses after step 1 (the [the senior model's] allowance at 95 per cent)"; "a merge spends
  the allowance for nothing" (`WP:6886-6892`); "after the usage reset" (`WP:9964`); the owner:
  "The [the senior model's] usage and the weekly limit are acceptable to use even if the warning flag appears"
  (`WP:111`).
- A week paused on new packages (decision 61, `WP:6882`; again `WP:10289-10293`).
- Sessions out of reach: dormant a day (`WP:10488`); messages lost (`WP:10187`, `WP:10490`).
- Work redone at merge: 75's step 7 refused twice on the trunk (`WP:10498`, `WP:10500`); 60
  reported three times and not merged (`WP:5020`, `WP:5098`, `WP:5150`); the lead's own rulings
  withdrawn after the owner had ruled in his place ("its rulings (4) and (5) are WITHDRAWN",
  `WP:10490`).
- Suites: the cloud's longest shard 68 to 69 minutes (`WP:3665`, `WP:3869`); a whole run an
  hour to an hour and a half (run 91, "an hour and a half, the new truth reading every tile",
  `WP:5142`). My half gives counts, not durations, for most merges ("7,528 passed, 2 failed",
  `WP:10498`).
- The record itself: this file is 1,069,845 bytes and 10,510 lines; my half 501,693 bytes for
  45 package sections; one line runs 6,303 characters (`WP:10486`). The tuning notes beside it
  are 2,912,718 bytes. The lead's notes to one package (75) are some 750 lines of this file.

## 5. The record as a record

- **No section says the state of its package.** The sections in my half are briefs with dated
  addenda; whether 71, 72, 73, 76, 81, 82, 84, 85 or 86 is merged is said only in the head's
  table and the as-merged records thousands of lines away. A section's own head line still
  lists the files a brief meant to touch, not what was built.
- **Order is by when the brief was written, not by number or state** (71, 72, 73, 74, 76, 81,
  79a ... 65, 88, 82 ... 114, 92, 103a, 75). Briefs held, approved-not-launched, launched and
  closed lie side by side with the same typography; the reader must find the bold first line.
- **History and current are interleaved**: 74's brief, then its refresh, then lines from 86,
  75 and 97, then an "as built" line (`WP:5709-5890`). Package 75's section ends the file with
  a running correspondence, its newest note last.
- **What it leaves out**: what is unbuilt from a closed brief (74 closed; its far fight's fault
  sits in 75's notes, not in 74's section); any first-game or tutorial work; the director's
  limits as something to test.
- **What it holds that nobody will read**: the lead's rulings to the ships session on keys,
  rungs and page numbers of Steel and Luce, at several hundred words a paragraph.
- **Honesty**: the lead records his own errors plainly in places: "a correction of my own note
  ... its rulings (4) and (5) are WITHDRAWN" (`WP:10490`); "that is how a ruling of mine should
  be overruled by the measurement" (`WP:10492`); the correction to "green whole" (`WP:119`);
  "the note of 2026-10-29 that read two ways ... is the lead's" (`WP:10148-10149`). Less plainly:
  the removal of 7-196's test is filed as "recorded and not pinned" (1.2), and 74's section was
  not told of its far fight's fault (1.1).

---

## (a) Six merged packages: the brief against the code, and the merge record against both

| Package | Brief (my half) | Built? | Did the merge record say truly? |
|---|---|---|---|
| **74** prizes, strike, far fight | `WP:5709-5817`, refresh `WP:5833-5890` | Prize, captive, court, money, consent refusal built (`world/seats.py:73-76`, `world/prizes.py:1115`). The far fight: built and faulty when a far ship engages from her passage (1.1); and the player's shot into any **brainless** hull does nothing (refute-02 04-3; `world/crews.py:629-630` says honestly "Nothing of it is read yet beyond the record"). | The close (`WP:4469-4504`) calls it closed with "the cruisers and the far fight", lists two "seen, not mended" words. Neither fault is in 74's records. The brief's "the near action and the far one measured to agree within a round" (`WP:5772`) does not cover a near shot on a far hull. **Partly untrue by omission.** |
| **98** mends of 11-09 | `WP:7755-7825` | Probe built; `hears` mended; the flags of command come down and are read (probe: "A commodore's broad pendant hauled down"; "The flags: British colours, the red ensign at the peak; a commodore's broad pendant at the main truck"). | True, including that the probe skipped in the cloud (`WP:3665`). The brief itself designed the skip (1.6). |
| **102** signals seen, ship dressed | `WP:8244-8363` | Dress and undress, flags, days built (probe). `splice the main brace` not built. Only the basic root has `dressing.yaml`; France and Spain have `days.yaml` but no fashion of their own. | True on splice (`WP:4547`). The player's answer to `splice the main brace` is a rope hunt (1.4). |
| **109** mends of 11-12 | `WP:8992-9077` | Step 1 true in play ("open the gunports" refused with the order meant; "read the letter" refused, "You keep nothing, and nothing lies here"). Step 5 left eight of thirty-five ships crossing land, as the brief allowed ("stop and report", `WP:9062-9064`). Note a misdirected answer: "put the glass on the table" is refused with the list of strangers in sight. | True and unusually plain (`WP:4681-4713`, `WP:5115-5128`). Its step 1 broke a browser plan nobody ran (c). |
| **85** the orders and primer for a model reader | `WP:7478-7580` | `the date`, `the war`, `the ship`, `my keeping`, the in-world test: built. `the ship` doubles its own head (1.5). Item 7's "The lead plays at this gate ... blind" (`WP:7560-7567`): `docs/gates/gate-m7-interim.md` is "Pending", 17 boxes unticked, item 9 (the lead blind) among them. | 85's merge (`WP:1262`, not read whole) aside, the gate's draft claims of 70 "the guns cast loose ... by the quarter bill", which a player's `beat to quarters` does not do. |
| **111** the chart's audit | `WP:9185-9237` | Tool, ratchet, known list built (`tools/audit_chart.py`, `data/charts/audit-known.yaml`). Not "as the game reads it": its own tide blend (1.3). Only steps 1 and 2a merged; no close at the commit. | Silent on the copy. |

## (b) Package 109 and the "found on the way" faults: what, by whom, how long after

**Package 109 (the owner's third play notes, 2026-11-11 and 12; `WP:8994-9065`)** mends, all
found by **the owner playing**, none by a test:
- free orders answered "as said" though nothing happened (`orders/free.py`; the free verbs
  are older than M7, so weeks at the least);
- the boat waiting two hours for a watch, deck orders refused from the boat (the bilander,
  merged 2026-11-09 in 75's B4, `WP:10488`: about three days);
- the director's dry run saying "would be performed" for every order whenever a model was
  seated, because it pickled from a hull after package 97 (merged 2026-11-06, `WP:10466`) and
  swallowed the failure (`WP:4914-4917`): about six days; the tests ran without a seat;
- the page drawing the first ship's rig over the followed hull's state (since the drivers
  first followed another hull, 84 and 82 in late October: about two weeks);
- vessels on the land (the far body's straight legs, older than M7; weeks).
And deferred from the same notes: "clear for action" only writes lines (galley fire, boats never
touched, `WP:8451-8458`; package 70's, merged before 2026-10-24 (`WP:5894`): nineteen days or more), and the
74's chain pumps idle with 590 aboard (`WP:8468-8471`; 73's water).

**Package 98 (the owner's play of 2026-11-09)**: the player not hearing his own answer below
(65's place rule); the flags of command with no way down (76's item 8, merged about 11-07: two
days) (`WP:7770-7820`).

**Found by later builders, in my half:** 75 (2026-10-29) found `combat/far.py:111` reading a key
`HullSpec` lacks, every far ship's length 0.0 (package 70's, about five days; `WP:5827-5831`,
`WP:9955-9958`), mended in 74's step 1 on 11-07; 75 found "fire No. 1 gun" firing the larboard
gun at a starboard mark (`WP:10496`); a King's ship with no private signal table fired on by her
own side (71's ground, `WP:10496`); the far fight's fault (74's step 4, merged 11-10, found
11-12, two days, after 74 closed: `WP:10498-10500`); 81 found the frigate's two port sizes
(`WP:10476`); 74 found the merchant brig's muster of 121 (`WP:10478`). **Found by the cloud**:
a pin moved by a ruled build (run 62, `WP:10494`). **Found by the lead reading**: 74's two words
at its close (`WP:4472-4479`).

The pattern: faults of the fight and the world's joins are found by the owner's play and by the
ships session sailing its new hulls, days to weeks after merge; the merge's own suites pass.

## (c) The browser plans: the procedure, and the case the lead names

The probe and its plans are package 98's (`WP:7761-7769`), briefed to skip where no browser is
named. Cloud runs had no browser; the record noted the skip at run 59 (`WP:3665`) and run 61
(`WP:3869`) and nonetheless recorded later runs as green whole. **The case** (in the head,
`WP:4716`): package 109's step 1, merged at 00da8a1a, made a burnt letter's reading a refusal;
`tests/browser_plans/a-letter.yaml` expected "as said". "The builder's slow tier had left
`tests/test_browser_probe.py` out, the lead's fast tier does not run it, and the cancelled trial
would have"; the trunk "failed that one plan between 00da8a1a and the mend, and run 77 is
expected red on it", yet run 77 was "green in lint, the six shards and the pace job, **the
browser plans skipped there, as in every run before it**" (`WP:4780`). The correction: "the
cloud's runners had no browser, so the fourteen browser plans, the pictures' test and the truths
that read a page were skipped there in every run ... run 77 was green on a tree where the
letter's plan failed. From run 81 the workflow has a job that installs a browser" (`WP:119`).

What it shows: for the three days from 98's merge (11-10) to run 81 (11-13), "green" in the
cloud did not include the only tests that come in by the player's door, and the lead knew it
from run 59; the remedy came after a step that changed an answer had merged broken. 114's own
brief names it as "a case on file" (`WP:9482-9483`).

## (d) The combat core: what the record knows

- **Beat to quarters without casting loose, answered "firing as they bear already".** Not known
  in my half or in the head's lines I searched (`cast loose`, `as they bear`, `already`, `stand
  aside`). 70's brief made `fire as they bear` "a standing intention the divisions keep" and
  `beat to quarters` move the ship to the quarter bill (`WP:5194-5209`); 70's as-merged record
  accepted "`beat to quarters` a crew order ... `cast loose` and `secure the guns` evolutions"
  (`WP:292-293`). Nothing says beating to quarters leaves the guns secured, or that the player's
  first gun order makes the rules captain stand aside. The nearest known fault is "engage" with
  every port shut answering "fire as they bear" and nothing following (`WP:237`), booked to 77,
  not launched (`WP:8368-8370`). The interim gate's draft says the opposite of the play.
- **A wheel shot away is never mended.** The record lost it in a hand-off. 70's brief: "the
  wheel or the tiller ropes shot away (the helm lost until repaired)" (`WP:5256-5257`); the code
  says "until 73's repair" (`combat/hits.py:9`; `physics/hull.py:553`); the log promises "until
  the relieving tackles are rove" (`combat/hits.py:216`) and so does the primer
  (`docs/primer/22-an-action.md:79`). 73's brief lists the damage control to build and omits the
  helm (`WP:5609-5622`); 77's survey of what is "Not built at all" omits it too (`WP:8401-8402`).
  No code clears `extra["helm_lost"]`; no order rigs the relieving tackles.
- **A shot into a ship at coarse detail does nothing.** Not known as such. The design assumes the
  engagement wakes her: 74's refresh, "the engagement first among the cap's reasons to wake them"
  (`WP:5864-5865`); 84's acceptance test keeps "the lugger passed and not fought until 74"
  (`WP:7644`). Neither says a brainless hull is never woken (`crews.py:850`), nor that the far
  record of hits "is read by nothing" (`crews.py:629-630`, which says so honestly).

## (e) Package 114's brief, and what the lead expected

The brief (`WP:9410-9512`): approved 2026-11-13, "not launched: it begins when the work in flight
has settled, at a commit of the trunk the lead names"; cold means "forms its own picture ... from
the thing itself before it reads the project's account"; "**the lead's method, briefs, rulings and
records are under review with the rest,** and nothing in them is to be taken as true because it is
written there" (`WP:9431-9434`); a sub-reviewer for the tests whose brief already names the browser
plan miss (`WP:9482`); findings each "tried against a second reader told to refute it"; the report
"first two pages for the owner, who is not a programmer"; "the lead merges its document unedited
and may answer it in a document of its own beside it, never in it" (`WP:9511-9512`).

What the lead sent ahead to the review: "the pace floors ... goes to the cold review with the
earlier notes on those floors" (`WP:5016`); three weather boxes left "as findings in the known
list for the cold review" (`WP:4995`); "For the lead's list and the cold review ...: a rules
captain waits for his tide without a word ... she ... took the ground on mud at five knots"
(`WP:5166`); 103's "whole of fidelity" handed to 114 (`WP:8129`). The launch condition, "once 109,
111, and 60 are settled" (`WP:111`): at 504a250 package 60 has been "NOT merged" three times
(`WP:5020`, `WP:5098`, `WP:5150`) and 111 has no close; the other reader should weigh whether the
condition was met. The brief expected scope and tests to be the findings (its own six heads, the
owner's words); it named no expectation about the boundary, the director's limits or the guns.

---

## The ten things that matter

1. **A closed package's fault in another's notes.** 74 closed with its far fight broken for a far
   warship engaging from passage; the mend sits on 75's unmerged branch. `WP:4500`, `WP:10498-10500`;
   `freesail/world/brains.py:1053-1058`.
2. **"Green" without the player's door for weeks, known from run 59.** `WP:7767-7768`, `WP:3665`,
   `WP:119`, `WP:4716`, `WP:4780`.
3. **The lead removed a failing pace test at a merge under a no-skip rule he enforces.** `WP:10496`;
   `tests/test_bellerophon.py:2188-2196`.
4. **The wheel lost in a hand-off between briefs.** `WP:5256-5257`, `WP:5609-5622`, `WP:8401`;
   `combat/hits.py:9,212-221`; `docs/primer/22-an-action.md:79`.
5. **The guns-secured road is unknown to the record; the interim gate claims the opposite.**
   `WP:292-293`, `WP:5194-5209`; `docs/gates/gate-m7-interim.md` (70's bullet).
6. **Faults of joins are found by the owner's play, days to weeks after merge.** 98 and 109 whole:
   `WP:7755-7820`, `WP:8992-9065`; the dry run blind with a seat since 97, `WP:4914-4917`.
7. **The director's reach onto every hull was briefed as a feature; the limits were never briefed
   as tests.** `WP:7670-7675`, `WP:7123-7126`, `WP:5785-5790`; `WP:5755`.
8. **No first game anywhere in the M7 record.** Only `WP:9457`; 96 held, `WP:7317`, `WP:8254`.
9. **The record cannot tell a reader a package's state from its section.** Briefs with addenda,
   ordered by writing; states 4,000 lines away. `WP:5341-10510` throughout; `WP:5709-5890` as the
   example.
10. **Ships as code was the lead's decision, agreed**; the review should say so. `WP:9641-9642`,
    `WP:9734`.

## What I did not read

Read whole, line by line: `WP:5341-5891` (71, 72, 73, 74 and its refresh), `WP:6878-7477` (65's
end, 88, 82 and its re-brief, 82b, 95, 96), `WP:7478-7861` (85, 84, 86, 98, 99, 100's head),
`WP:8244-8497` (102, 77), `WP:8992-9078` (109), `WP:9185-9318` (111, 112), `WP:9410-9513` (114),
`WP:9614-9757` (103a, 75's brief), `WP:9910-10510` (the last 600 lines).

Read by heading, first lines, dated rulings and "found"/"as built" paragraphs only:
`WP:5892-6877` (76, 81, 79a, 79b, 79c, 79d, 89, 93, 94, 65's body), `WP:7411-7477` (83's body),
`WP:7862-8243` (60, 101, 103), `WP:8498-8991` (104, 107, 106, 106a, 105), `WP:9079-9184` (106b),
`WP:9319-9409` (110), `WP:9514-9613` (92), `WP:9758-9909` (the notes of 2026-10-28 and 10-29 to
the ships session).

Outside my half, read only as cited: `WP:83-119`, `WP:230-240`, `WP:271-296`, `WP:3618-3669`
(parts), `WP:3869`, `WP:4469-4504`, `WP:4681-4720`, `WP:4778-4782`, `WP:4908-4932`, `WP:4995`,
`WP:5016-5032`, `WP:5115-5130`, `WP:5160-5166`, `WP:5185-5270`. The as-merged records of 71, 72,
73, 76, 81, 82, 84, 85 and 86 were not read.
