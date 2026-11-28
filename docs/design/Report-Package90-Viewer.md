# Report: package 90, the viewer (V1 to V3)

The viewer's session for package 90: the engine's new lateen, pole-mast and towed-boat states drawn
in the client, before the tartane's report (`docs/design/Plan-Package90.md` §6 rows V1 to V4, §7.1,
§9.1). Started by the owner on 2026-11-27. Branch `claude/pkg-90-viewer`, cut from 93cf624c (the
package's branch, carrying A1a to A1d, A4, A5 and A6).

The files this row owns, and the only ones edited for the steps: `client/projection.js` and
`tests/test_view_geometry.py`. `client/shipview.js`, `client/style.css` and `tests/test_pictures.py`
are untouched. The notes' section is "Package 90, the viewer" in `docs/dev/TuningNotes.md`.

## 2026-11-28: V1 and V2 built; V3 stopped; two questions and a choice for the lead

**Built** (each its own commit, pushed; the tiers on one hash follow in a later section):
- **V1**, the whole lateen drawn as its own (e0cba7d).
- **V2**, the pole mast and the yard below that does not stand, mended at its cause (24d239a).
- The notes' section, "Package 90, the viewer" (427ca81).

The measured figures, old beside new, the tartane's topsail among them, are in the notes' section.
In short: her topsail's loose foot is square with its own yard in each of her report's §14.2
states, 9.35 m broad, its clews 8.09 m over her water, as her builder measured in scratch; before,
90° askew before the wind and 26° by the wind braced 64°. The smack's topsail yard lies on her
square-sail yard (11.15 m over her water, against 14.35) whenever her topsail is not set, her start
and plain sail among them, since A6 furls it there: the plan's one expected move.

### Stopped: V3, the towed boat drawn astern (the stop rule)

The client is served no boat. `/api/ship` (`freesail/api/queries.py`, `ship_graph`) serves the
spars, sails, lines, hull, guns and ports, and no boats; `/api/state` (`snapshot`) serves no boat
in tow. A4 keeps her in the engine alone (`ship.extra["boat_in_tow"]`, `boats.keep_in_tow`;
TuningNotes, "Package 90, A4"). Drawing her needs `freesail/api/queries.py` to serve, for
instance:
- in the graph, each boat whose file tows her, with her `towed` key and her length (her own file's
  hull, which A4 already reads for her drag);
- in the snapshot, whether she is in tow now (A4's key: there while she is in tow, gone while she
  is away on an errand, manned or lost).

That file is neither in the viewer's row of §7.1 nor named by the card for it, so I have not
edited it. Once served, V3 is the viewer's alone: her hull on her painter A4's `TOWED_ASTERN_M`
(12 m) dead astern of the taffrail, at her file's length, and the painter from the taffrail to her
stem; nothing committed moves (no file tows a boat). **Asked:** whose step serves it, and whether
V3 waits for it in this package or goes to a later one.

### Not served: a manoeuvre's change of the lateens (V1's "peaked up its mast while it is changed")

The shift by itself is served exactly: `change_lateen` in hand on the sail, the sail in its gear.
V1 draws it peaked up the mast. A manoeuvre's change is not. In a tack, a wear, a fill away, a
box-haul or a box off (`LateenChange`, held on the manoeuvre's script), and for the yards a belay
hands on beyond the longest (the handed-on `change_lateen`'s one subject), the snapshot serves only
the manoeuvre and each sail `in_the_gear`, as it serves a lateen brailed up before the manoeuvre
began. Measured on the xebec probe (`tack ship`, 15 kn): from +60 s to +250 s her three lateens
were served `in_the_gear` with `lug_side` the old side, the only work in hand `('tack', 'Harpy',
'steady')`.

So in a manoeuvre the yards being shifted are drawn brailed up under their yards aloft, not
peaked. Guessing from "in the gear while a tack is in hand" would draw a lateen brailed up before
the tack peaked too, so I did not. The settee's mirror would serve it: a key on the snapshot's
sail, served only while its change is in hand, as `yard_lowered` is for a settee
(`api/queries.py`, and a mark the change keeps on the sail, `evolutions/scripts.py`: the engine
track's files). With it the drawing reads the key in one condition. **Asked:** is it wanted before
the tartane's report?

### A choice for the lead: the fixed frame and the peaked yard (JUDGEMENT)

The frame holds every state's figures (spec M3 §9 item 14). With her great yard peaked, the
tartane's frame top rises from 17.59 to 25.50 m (abeam 18.80 to 26.72 m high), so she is drawn about
30 per cent smaller in every view, to keep the view from rescaling for the minute her yard is
shifted. Left out of the frame, she is drawn at today's scale and the view zooms out while the yard
stands peaked. **Built the first way**; the second is one line. No committed file's frame moves.

### Found on the way (the engine's, not mine)

`ship/graph._square_foot_m`, read by A5's lateen rule, mixes a sail's centre above the water with
its yard's height above the deck. It overstates the foot by twice the deck's height: 1.08 m on the
tartane, whose topsail clears her lateen's yard by 0.03 m, not 1.11 m. It moves no classing on her
files. The viewer keeps the engine's arithmetic so that the two read every pole alike.

I carry on with the tiers on one hash for V1 and V2, and write them here when they are done.

## 2026-11-28: the hash for V1 and V2, with V1's mend: 20aca5e

**The reported hash is 20aca5e**, tiered whole on that exact hash (below). It is V1 and V2 as one
hash, without V3, on the lead's terms of nudge 88. It carries the package's branch merged three
times, each docs only, at 6c29d1d, ef5a9dd and a027600. The commits:

| Commit | What |
|---|---|
| e0cba7d | V1: the whole lateen drawn as its own |
| 24d239a | V2: the pole mast, and a yard below that does not stand |
| 427ca81 | the notes: V1 and V2 measured old beside new |
| 0000168 | this report: V1 and V2 built, V3 stopped, the questions |
| c28eeee | merge of `claude/pkg-90` at 6c29d1d (docs only) |
| 450108d | the notes: the owner's fixed frame, its figures on the page, the lead's rulings of nudge 88 |
| 1c27d37 | merge of `claude/pkg-90` at ef5a9dd (docs only) |
| fe22edd | V1's mend: each edge of a sail bellied by its own length (the owner's note T-v2) |
| 20aca5e | merge of `claude/pkg-90` at a027600 (docs only) |

Every commit's author is as the cloud gives it. My commits changed only `client/projection.js`,
`tests/test_view_geometry.py`, `docs/dev/TuningNotes.md` and this report; the merges bring the
package's docs alone. The figures,
old beside new, are in the notes' section "Package 90, the viewer".

### V1: the whole lateen (`client/projection.js`)

- **Keyed** as A1a keys it: `wholeLateen`, a lateen with `dipping`, not cut at the mast. No
  committed file carries one.
- **Its cut and yard** (`lateenCorners`, `lateenCut`):
  - three corners on its yard, from the file's cut;
  - the yard drawn whole from car to penne, slung a third of its length from the car where the
    head crosses the yard's filed height, on the mast's raked line;
  - a mast's half-diameter to the side the game serves it hanging (`lug_side`);
  - the whole cut swung about its slings by its sheet.
- **Its cloth**: to the lee of the tack on either hand, so against its mast on the bad hand; to
  windward when served `backed` (A1d).
- **Its placement** (`placeSpars`'s whole-lateen branch, before the lug's): aloft in every state.
  - Brailed up under its yard in its gear; a bundle along its head furled.
  - Peaked up its mast's raked line, abaft the mast, while `change_lateen` is in hand on it
    (`shifting`).
- **Its sheet**: to her rail on the side its cloth lies on, two metres abaft its clew.
- **Filed with no cut** (the probes): cut from its yard and its area.
- **The frame**: reaches its swing every way at its heights, and its yard peaked (`framePts`).
- **On her great lateen, old beside new:**
  - before, the yard was drawn as the head alone (23.63 m), it lay on deck in the gear and
    furled, and on the bad hand its cloth swung to windward;
  - now the yard is the file's 24.36 m, aloft in every state, and on the bad hand the cloth lies
    to leeward against the mast.

### V2: the pole mast, and the yard below that does not stand

- **The cause, mended where it lives** (`standsBelow`): a yard below is taken only where it
  stands, aloft, neither sent down nor on deck with its flying sail. It is read in the four places
  that choose a yard below:
  - the clews, `squareCut`;
  - the sheets, `yardBelow`;
  - a hoisting yard's reefed height;
  - where a pole's yard is lowered to.
- **The pole** (`poleYard`, mirroring `Ship.on_pole` with the engine's arithmetic): its upper
  yards drawn down onto the yard below, or to the hounds, while their sails are not set; halfway
  in `lower_and_clew_up`. A pole is drawn with no doubling.
- **The tartane's topsail**: its loose foot is square with its own yard in her report's three
  §14.2 states. It is 9.35 m broad, its clews 8.09 m over her water, as her builder measured in
  scratch. Before, it was 90° askew before the wind and 26° by the wind braced 64; with the tréou
  set, unchanged.
- **The smack's topsail yard** lies on her square-sail yard, 11.15 m over her water against 14.35
  m, whenever her topsail is not set, her start and plain sail among them; halfway, 12.75 m, in the
  lowering. This is the plan's one expected move (§6, §10.4), measured; her frame and scale are
  unmoved.

### V1's mend: each edge's belly by its own length (the owner's note T-v2, at the live look)

- **The cause.** A sail's belly was reckoned once for the whole sail and laid on every curved edge
  whatever its length. The whole lateen's 0.30 m luff at its car took the sail's whole belly and
  stood out a thin tongue: 2.56 m off its chord on her great lateen, 1.65 m on her mizen.
- **Mended where the belly is laid** (`edgeControl`), in the four-cornered sails' path
  (`quadSail`: square, gaff, lug, settee, lateen), the jib's and the goose-winged. No edge bellies
  more than `BELLY` of its own length; an edge as long as the length the belly is reckoned by is
  drawn as before. Her luffs now stand 0.04 m off their chords.
- **The same cause elsewhere**, found by measuring every committed file with every sail set. The
  outlines of sails on **15 of the 19 committed files move**, declared old beside new in the notes'
  table. The largest are:
  - the bilander's settee luff, 1.35 m off a 1.81 m luff, the same tongue as the lateen's, now
    0.22 m;
  - her jib's leech, 1.22 to 0.66 m;
  - the hermaphrodite brig's main topmast staysail, 1.16 to 0.67 m;
  - the 64's, the razee's and the 74's main staysails, about 0.4 m less;
  - the boats' lug luffs, about 0.15 m less;
  - the lugger's mizen lug's foot, 1.02 to 0.85 m.
- **What does not move:** the rest are a few centimetres. The cutter, the smack and the two
  schooners do not move. On every file no corner, spar, line, frame or view's bounds moves,
  measured at eight facings and four heels. **These moves lie outside the card's named moves.**
  They are built in this hash at the coordinating session's word ("mend it at its cause, in the
  hash you send now") and are declared for the lead's reading.

### The frame: the owner's choice

The owner chose **(a), the fixed frame**, at a live look on 2026-11-28
(Decisions-Package90-2026-11.md Part F, row T-f). The frame holds every state's figures, the peaked
yard among them; the reason put to them was that by her default practice she shifts at every tack
and wear. Measured on the page (`shipview.js`'s box, abeam): 35.80 × 25.27 m before, 36.89 × 33.54 m
now. So where the page's width sets her scale she is drawn 3 per cent smaller, and where its height
does, about 25 per cent. The coordinating session's preview with the peak left out showed her scale
unchanged because its view was set by its width, which the swing, not the peak, moves. Leaving the
peak out is `framePts` alone, which takes the height back to 19.23 m. No committed file's frame
moves.

### Pins moved, old beside new

**None.** One docstring's words changed, with its name and assertions kept:
`test_a_whole_lateen_with_its_cut_is_drawn_as_a_standing_lug_to_leeward` takes a lateen with
neither key. No threshold of `tests/test_pictures.py` moved, and that file is untouched.

**New cases: 71 in `tests/test_view_geometry.py`.** V1 has 24, V2 19 and the edge's belly 28;
none of the base's cases was removed or renamed (collected both ways). Run on the code before
them:
- V1's and V2's 43, on 93cf624c's projection: 32 fail and 11 pass. The 11 hold what was drawn so
  before: the unswung cut, the aback side, four of the frame's six facings, the pole as one stick,
  the topsail set aloft, and the clews to a yard below that stands.
- The belly's 28, on V2's: 17 fail and 11 pass, the 11 being files with no short edge drawn
  whole.

### Taken as judgement

- The peaked pose: the yard up the mast's raked line, a mast's half-diameter abaft it, slung
  where it was, raised only to keep its car `ON_DECK_M` over the deck.
- The whole lateen's sheet two metres abaft its clew, as any single sheet.
- The cut made for a whole lateen filed with none: `LATEEN_TILT`, the clew a loose foot's height
  over the deck by its area.
- A pole's yard lowered `YARD_ON_CAP_M` over the yard below, or over the hounds: the filed height
  of the highest yard below on its mast, of any class.
- Halfway in `lower_and_clew_up`.
- The edge's cap at `BELLY` of its own length.

### V3 and V4

On the lead's ruling (nudge 88), V3 waits for the engine's served step. That step serves each towed
boat (`towed`, her length, whether she is in tow now) and a whole lateen's change inside a
manoeuvre, a key served only while it is in hand. The viewer then draws both in the hash with V3
and V4, after that step and A9. Until then a manoeuvre's lateens being shifted are drawn brailed
under their yards aloft. The engine's `_square_foot_m` is mended in the same step, and the viewer
follows its arithmetic.

### The tests on 20aca5e

Every run is on the exact hash, with `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist
loadgroup"`.

- **The fast tier, whole, compared test by test with the base's** (93cf624c; junit both ways):
  - on 20aca5e, 9,269 cases: 9,260 passed, 8 skipped, 1 xfailed;
  - on the base, 9,198 cases: 9,189 passed, 8 skipped, 1 xfailed.
  - No case changed its outcome and none is gone. The 71 new cases are the view geometry's, and
    all pass.
- **The slow tier of the files the steps reach, with `--slow`**: 1,327 cases, all passed.
  - `tests/test_view_geometry.py` whole: 1,174 cases, none of them slow.
  - `tests/test_pictures.py` whole, 2, and `tests/test_flag_drawings.py` whole, 27: none of them
    slow.
  - `tests/test_browser_probe.py`: the 12 browser plans, every one. They are a-letter, action,
    ashore, asleep, boat-and-visitor, deck-and-below, dressed, prisoner, seated-officer, seated,
    signals and under-way.
  - `tests/test_harbour.py` whole, 50, with its 3 slow among them: the maker's save in the
    player's place, the API door started from the harbour, and the four scenarios' round trip in
    the browser.
  - `tests/test_server.py` whole, 61, with its 2 slow: the frigate's snapshot through state
    changes, and the clock eased on station.
  - No harbour or browser test failed in these runs. No loader was patched.
- **The merged base's practice tests**: `tests/test_practice.py` on a027600, in a detached
  worktree, 25 passed. It is the one test that reads the docs the merges changed, and it has no slow
  case.
- **The file rules**:
  - ruff clean on the whole tree;
  - no Python line over 100 characters;
  - `git diff 93cf624c..20aca5e | tr -cd '\r' | wc -c` is 0;
  - the view geometry's ids collected on the base and on this hash: 1,103 against 1,174, 71 added,
    none removed or renamed.

That is the hash. I stop here and wait for the lead's word; nothing more is pushed until it comes.

## 2026-11-28: nudge 93's list, built; the hash: 856dbcc

**The reported hash is 856dbcc**, tiered whole on that exact hash (below): 20aca5e (V1, V2 and V1's
mend) with the reader's list of nudge 93 built on it. The commits since 20aca5e:

| Commit | What |
|---|---|
| b9a2162 | this report: the hash 20aca5e and its tests |
| 3fc7b19 | nudge 93: the cut keeps its curves; a foot sags by its own length; three pins bite |
| 9aeeaa9 | the notes: nudge 93's list, every outline move declared old beside new |
| 856dbcc | merge of `claude/pkg-90` at 55d2dda (docs only: the owner's T-v3 and its pictures) |

Every commit's author is as the cloud gives it. My commits changed only `client/projection.js`,
`tests/test_view_geometry.py`, `docs/dev/TuningNotes.md` and this report. The measures in full,
the table of every moved edge among them, are in the notes' subsection "The reader's list of
nudge 93".

### 1. Every outline move, declared

- **Measured again** with every sail a file can bend bent and set, the unbent as filed among them.
  Her yards are braced to their limits and square, on either tack, with the wind at 40, 60, 90 and
  135 degrees. Each edge's bulge is given three ways: before the mend (V2), at 20aca5e, and now.
- **The table has 78 rows**, a pair of studding sails taking one. Each row is marked by what moves
  it: the belly, the mend of 20aca5e; or the sag, item 3.
- **The sprit topsails.** The reader's "leech and foot" are its two leeches: 0.99 to 0.89 m on the
  64 and 1.10 to 1.00 m on the 74. Its foot does not move.
- **Now declared too:**
  - the ringtails on the five files with one;
  - the storm staysails of the razee, the 64 and the 74.
- **The schooners, as it is.** At 20aca5e they moved by their ringtails alone (1.14 to 1.12 m).
  In this hash they move also:
  - by the foot's sag: their ringtails to none, their fore sails' loose feet, their studding
    sails' feet;
  - by the cut's curves, 0.04 m.

  Of the 19 files only the cutter does not move. The smack moves only by the cut's curves (her
  jib, 0.02 m).
- **Nothing else moves.** I measured V2 beside this hash on every file in 18 states, at eight
  facings and four heels:
  - no corner, spar, mast, yard, line, hull point or frame point moves;
  - no view's bounds moves;
  - no point is NaN.

  A cut sail's centre, which places its pieces along the view axis, moves with its sampled
  outline: by the sag alone, up to 0.14 m on the lugger's lugs.

### 2. The three pins, made to bite

Each fails with its rule taken out:
- **(a) The frame holding the peaked yard.** A new case on the tartane probe with her main struck
  to a pole (`_main_a_pole`; the jibs go with the topmast their stay was set up to). Her main's
  head is 17.0 m over her water. The frame's top is the peaked penne, 21.52 m. With the peak left
  out of the frame it falls to 17.0 m, and all four facings fail.
- **(b) The car lifted clear of the deck.** A new case with the probe's great yard slung at 5 m.
  Peaked where it was slung, its car would stand under the deck; it is raised to `ON_DECK_M` over
  the deck, no higher. With the lift taken out, both tacks fail. On the probe as rigged the car
  stood 4.69 m up.
- **(c) The every-ship guard.** It now takes:
  - every sail a file can bend, and the sails cut at their masts in their pieces;
  - both bracings, either tack and four winds;
  - besides the belly across, an up-or-down bound.

  With a four-cornered sail's leech uncapped, it fails on the 64 and the 74, by their sprit
  topsails at the winds other than 60.
- **The other mutants**, run on the new pins and the belly's, the sag's and the cut's cases:
  - the luff uncapped: 17 fail;
  - the foot uncapped: 8;
  - the jib's leech uncapped: 9;
  - the sag by the depth again: 11;
  - the cut made on the sampled outline: 5.

### 3. The foot's sag by its own length (`footSag`)

- **The cause.** A foot sagged FOOT_SAG of the sail's depth whatever its length. A ringtail's foot
  has no length, so with its belly capped (20aca5e) it hung a spike straight down from its clew:
  0.80 m on the corvette's to 1.12 m on the schooners'.
- **The mend.** Like the belly's: never more than FOOT_SAG of the foot's own length. A foot at
  least as long as the depth sags as before. The boomed spanker takes back exactly the sag it is
  given.
- **The moves.** The table's sag rows: the ringtails, the studding sails' feet, the lugs' feet and
  the schooners' fore sails' feet. The largest is the lugger's main lug's sag, 1.23 to 0.62 m.

### 4. The launch's lug: the cut at the mast, not the cap

- **The cause.** Its luff stands wholly forward of the mast (0.23 to 0.73 m). A sail cut at its
  mast was cut on its outline sampled at six points an edge and drawn as straight pieces. Seen from
  the quarter, the luff's corners turned 6 to 9 degrees each (8 to 13 before the mend). The cap
  made the luff lie along the mast, where those corners show against its straight line.
- **The mend** (`splitPathAtX`). Each curved edge is split at the mast and kept a curve. The luff
  is one curve again.
- **The bounds.** A curve's control point stands off it. On the yawl's lug, seen from ahead heeled
  0.3 rad, one stood 0.013 m past the frame, which would have rescaled her view while the lug is
  set. So a piece holds its share of the bounds, and its place along the view axis, by its sampled
  outline, as before. No bound moves.
- **The cut's own move** is at most 0.05 m (the hermaphrodite brig's jib).
- **The staysail pin** `test_a_staysail_that_crosses_a_mast_is_drawn_in_two_parts` holds
  unchanged: its straight edge is now the cut.

### Pins moved, old beside new

- **None of the base's.** No threshold moved, and `tests/test_pictures.py` is untouched.
- **This package's own cases:**
  - the every-ship guard is made stricter, as (c) above, with its name and its 19 files kept;
  - the frame case's views and assertions are moved unchanged into two helpers it shares with
    (a);
  - `lateen_by_the_wind` takes a rigged document.
- **New: 18 cases**: the frame over short masts 4, the low-slung lift 2, the ringtails 5, the
  foot's sag 1, the cut on a lens 1, the boats' luffs 5. That makes 89 in the package, none of the
  base's removed or renamed (collected both ways: 1,103 against 1,192).

### Taken as judgement

- A cut piece's share of the bounds and its centre come from its sampled outline, as before, while
  it is drawn with its curves.
- The guard's up-or-down bound is BELLY and FOOT_SAG of the edge, because a tilted cloth's belly
  has an upright part.
- The probes for (a) and (b): her main struck to a pole, with the jibs; and her great yard slung at
  5 m.

### The tests on 856dbcc

Every run is on the exact hash, with `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist
loadgroup"`.

- **The fast tier, whole, compared test by test with the base's** (93cf624c; junit both ways):
  - on 856dbcc, 9,287 cases: 9,278 passed, 8 skipped, 1 xfailed;
  - on the base, 9,198 cases: 9,189 passed, 8 skipped, 1 xfailed.
  - No case changed its outcome and none is gone. The 89 new cases are the view geometry's, and
    all pass.
- **The slow tier of the files the steps reach, with `--slow`**: 1,345 cases, all passed.
  - `tests/test_view_geometry.py` whole: 1,192 cases, none of them slow.
  - `tests/test_pictures.py` whole, 2, and `tests/test_flag_drawings.py` whole, 27: none of them
    slow.
  - `tests/test_browser_probe.py`, 13: the 12 browser plans, every one, and the plans' own case.
    The plans are a-letter, action, ashore, asleep, boat-and-visitor, deck-and-below, dressed,
    prisoner, seated-officer, seated, signals and under-way.
  - `tests/test_harbour.py` whole, 50, with its 3 slow among them.
  - `tests/test_server.py` whole, 61, with its 2 slow.
  - No harbour or browser test failed in these runs. No loader was patched.
- **The merged base's practice tests**: `tests/test_practice.py`, 25 passed. They ran on 55d2dda
  alone, and again in the fast tier on 856dbcc. It is the one test file that reads the docs the
  merge changed.
- **The file rules**:
  - `ruff check .` and `ruff format --check .` clean on the whole tree;
  - no Python line over 100 characters;
  - `git diff 93cf624c..856dbcc | tr -cd '\r' | wc -c` is 0;
  - the view geometry's ids collected on the base and on this hash: 1,103 against 1,192, 89
    added (18 since 20aca5e), none removed or renamed.

That is the hash. I stop here and wait for the lead's word; nothing more is pushed until it comes.

## 2026-11-28: V4 built on A9, held for the hash with V3

The coordinating session's word (nudge 94): A9 is in `claude/pkg-90` at 157f870d, so V4 may be
built; its hash goes with V3, after the engine's served step (the towed boat, and the lateen's
change in a manoeuvre: nudge 88). So **this is a finished step, not a hash for the gate.**

| Commit | What |
|---|---|
| 93f9565 | merge of `claude/pkg-90` at 157f870d (A9 with the *Concepción*'s report, nudge 94) |
| 367e123 | V4: a port named by its deck as the log names it |

V4 changes only `client/projection.js`, `tests/test_view_geometry.py` and the notes' subsection "V4:
a port's words by the log's "-deck" form", where the measures are in full. Every commit's author is
as the cloud gives it.

### V4: what it says, and where

- **The cause.** The viewer said "-deck" of the upper deck alone, and every other deck by its bare
  word (`portFigures`). The log says the lower, the middle and the upper deck with "-deck"
  (`freesail/combat/ports.py`, `_DECKS_SAID_SO`): "The lee lower-deck ports are shut". So the 74
  and the 64 said "a lower port", and a three-decker would say "a middle port".
- **The mend**, where a port's words are made: `DECKS_SAID_SO`, the log's list, in the exported
  `constants`. A port on one of its decks is said "<deck>-deck port"; every other deck by its own
  word, as before. No other place in the client names a deck.
- **A test holds the viewer's list to the log's**, since one is JavaScript and the other Python.

### Measured, old beside new

Every port's and lid's words, on every committed file and on the three-decker probe, her guns
secured, run out, and shut by the sea: 1,710 figures. **Words alone move**, and every figure's
deck, side, place, part and state is the same.

- **The 74's lower-deck ports** (28 figures) and **the 64's** (26): "a lower port" becomes "a
  lower-deck port" in each of its four forms ("its lid shut", "open", "'s lid, hauled up", "shut,
  the sea at its sill").
- **The probe's middle-deck ports**: "a middle port" becomes "a middle-deck port"; her lower-deck
  ports move as the 74's.
- **Nothing else moves:** "an upper-deck port", "a quarterdeck port", the razee's "a forecastle
  port", and the empty ports, on every file.

### Tests

- **New: 18 cases**, each made to fail with its rule taken out:
  - the viewer's list is the log's, 1;
  - every port on the 14 files with a hull profile, 14;
  - the 74's and the 64's lower-deck ports, 2;
  - the probe's middle-deck ports, 1.

  With the old rule put back, 5 fail. With the quarterdeck added to the list, 7.
- **Pins moved: none**, of the base's or of this package's. There are now 107 cases in the package,
  none of the base's removed or renamed.
- **Run on this tree**, with `python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist
  loadgroup" --slow`, all passed:
  - 1,564 cases: every test that runs the client, and the three decks' and the lee ports' tests,
    which say the log's words. The client's are the view geometry whole (1,210), the view action,
    the boats' and the flags' drawings, the map view, the pictures, and the 12 browser plans;
  - the viewer's known truths, 7-437 to 7-444: 20 cases;
  - the harbour whole and the server whole, with their slow cases: 111;
  - the practice tests: 25.
- **No harbour or browser test failed.**
- **The file rules:** ruff check and ruff format clean on the whole tree, no Python line over 100
  characters, and no CR byte.
- **Not yet run: the whole fast tier** and its comparison with a base on the merged tree. Those
  go with the hash, once V3 is built.

### Held

- **V3, and the lateen's change in a manoeuvre,** wait for the engine's served step (nudge 88).
- **If the reader's report on 856dbcc brings a list,** it comes before anything more here.

I stop here and wait for the coordinating session's word.
