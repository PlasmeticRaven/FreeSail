# Ground report: package 90, before any code (19 November 2026)

**The count: 25 pinned tests change outcome** with the card's four candidate steps applied
together (item 37, the tiller's key, the words of a rig with no yards, and the smack's topsail),
every one from passed to failed, both tiers run whole, old beside new. With two digests that move
inside tests already failing at the base, **27 pinned results move**. That is more than the card's
"about twenty", so **by the card's own rule the package comes back to the owner before anything is
built**. The narrowest reading is still over the line: two of the 25 are faults of the A6 draft's
own words and go if it is drafted without them, which leaves 23.

Of the 25, **17 are moves the card names and 8 are moves it does not** (§6: stops, not rulings).
Only two of the 25 are how a ship sails, item 37's truth 35 and the frigate at six points, and the
card expects both. Every other move is a word, a key in a file, a count, or the draft's own fault.
Wherever words move, every tick and every kind of line is the same.

This is the card's first step (`Plan-Package90.md` §14, "First step, before any code"), with the
backed square topsail that nudge 20 asks for beside the bad hand's figures (§4).

**The tree.** The package's branch at 5067945e: the trunk merged in as at a07a6928, and documents
only on the branch. Each candidate was built in a detached scratch worktree at 5067945e and saved
as a unified diff. Its tests were run with `py` from that worktree's root, under these conditions:
- the root first on `sys.path`, and `freesail.__file__` asserted under it in the controller and in
  every worker;
- `-p no:cacheprovider -o addopts="--dist loadgroup"`, at two workers for the single steps and at
  four for the tiers.

Each worktree was removed when done. Nothing was committed but this document, and the package's
tree was not touched. Ship files moved only through the generator. The patches, the probes and
their outputs are kept in the session's scratch (`p90/ground/`), not in the repository:
- `g1`: item 37 and the backed topsail;
- `g2`: the tiller;
- `g3`: the words, the smack and the rank words;
- `count`: the two tiers.

**The marks**, as the engine note uses them: **measured** (a figure from a run), **read** (the
code, the file or the page cited), **computed** (arithmetic on measured figures, not run),
**judgement**. Every figure of the measurers' reports was checked here against their saved
outputs. §7 lists what reading corrected.

## In brief

- **(a)** The trunk is merged in as at a07a6928; it has moved since, by package 118's merge, which
  shares no file with the candidates (§1.1). No text the game reads as a vessel's words holds a new
  rank word (§1.2).
- **(b)** What moves, by step (§2): item 37, 7 tests; the tiller's key, 11; the words of a rig with
  no yards, 4, and two digests in failing tests; the yard's level, none; the pole's handing, 5.
  The schooners' two records are moved by item 37 and the tiller alike, so the sum is 25 (§2.5).
- **(c)** Six files steer by a tiller, each by judgement. Only the two schooners have a direct
  source; the hermaphrodite brig has none, and is the least sure (§3).
- **The backed square topsail** on the brig, the hull the polacre and xebec probes stand on (§4):
  - held aback, its yard strains from about 40 kn and is at risk in no wind to 60;
  - taken aback by a shift, it strains from about 33 kn at its peak and is at risk from about 42;
  - no backed topsail brings a mast to risk, and no lower mast passes 0.62 of its rating.
- **The bad hand's factor** that puts its strain at the topsail's own wind (§4.4):
  - about 2.5 against the topsail held aback (strain about 40 kn, risk about 49);
  - about 3.3 at the lead's expected 35 kn (risk about 43);
  - about 3.5 to 4 against a shift's peak (33 kn).
  - At any of them a rules captain on the bad hand under 12 kn stays under a fifth of the rating.
- **Stops** (§6):
  - the tiller's key needs seven files the card does not name for it;
  - eight pinned results move that the card does not name;
  - several unpinned lines reach ships the card does not name.

## 1. (a) The trunk merged in, and the rank words

### 1.1 The trunk

- **At 5067945e** the trunk is merged as at a07a6928 ("The gate of milestone 7 worked up"), which
  carries nudge 20.
- **The trunk has moved since**, to 4b0dbff4 (read, 2026-11-19, 16:00 UTC):
  - package 118 merged at 0e534dd3, by its reported hash 1e373bd0;
  - the lead's note on Winfield's passages (the polacre's mizen topsail carried; the polacre's
    files and the three-decker's manning and calibres released);
  - nudge 21 (hold the next message to the lead until 19:05 UTC today).
- **Read:** none of the 32 files the four candidates touch is among the 24 the trunk has changed
  since a07a6928. Package 118 changed `core/world.py`, `core/replay.py`, `world/ships.py`,
  `world/crews.py`, `world/lookout.py`, `world/chart.py` and the rest. So the merge should not meet
  the candidates; whether it moves any figure of this report is not measured.
- **The lead's note of 11:00 UTC** asks for the trunk merged in before the next reported hash. That
  is for stage 0's commit, not this one.

**Not caused by any candidate**, both ways (measured):
- the base's ten slow failures stand unchanged:
  - the gate constants: the merchant passage at seed 7, the schooner's octant passage, the schooner
    on an intent at seed 7, and truths 77, 78 and 79;
  - three captain's trials: `station_gale`, `trade_thick` and `trade_stranger`;
  - the harbour maker, whose message differs only by the worktree's path.
- four pace tests stay under the 500 ticks a second floor: 424 to 475 at the base, 446 to 500
  patched (load).
- the fingerprint test of `tests/test_replay.py` failed once in the patched fast run, on its timing
  clause (1.78 s against 0.5 s). It passed when re-run on all six trees.

### 1.2 The rank words

The rank words are those stage 0 puts in `SIZE_RANK` and `_SIZE_WORDS` (plan §5.1 item 6): tartane,
polacre, xebec, corvette, three-decker, first rate, ship-sloop and ship sloop.

**Grepped** (measured, `g3`, and again here on 5067945e) over `freesail/`, `data/`, `client/` and
`docs/primer/`:
- **None is in any text the game reads as a vessel's words or ranks.** None is in
  `data/scenarios/`, `client/` or `docs/primer/`.
- **Comments:**
  - three code comments naming the probes (`orders/storm.py:445`, `ship/graph.py:227-228`,
    `ship/schema.py:611`);
  - "first rates" in five ship files' comments from Luce;
  - "three decks" in the 74's and the 64's comments from the Regulations;
  - corvette and xebec in comments of `data/captains/` and `data/ports/`.
- **Source citations:**
  - xebec and corvette in sixteen chart `source:` lines;
  - ship-sloop in two source strings (`data/nations.yaml:80`, `data/regimes.yaml:57`).
- **Five pilot's lines the player reads.** Each is the period's word, and no ranking or description
  lookup reads it:
  - `data/charts/features/balearics.yaml:894` ("xebecs");
  - `biscay-south.yaml:259` ("corvettes");
  - `mediterranean-west.yaml:733` and `:825` ("xebecs");
  - `data/ports/stora.yaml:69` ("brigs and corvettes").
- **Read** (`g3`): rank 5 is only compared, never an index into a table. A lone 74 will take the
  three-decker for a superior force, and the three-decker is never under the rank-4 haul-off
  herself, as Con-D §8.3 intends.

## 2. (b) What moves, run and not guessed

### 2.1 Item 37 (A0)

**The candidate** (`tools/gen_ships.py`, a new `tests/test_peak_coeff.py`, nine ship files
regenerated). The generator's `PEAK_COEFF` is read from the engine's own curves
(`freesail.physics.sails.SAIL_CLASSES`): the greatest |(C_L, C_D)| over each class's tabulated
points, rounded to two places. It replaces the hand table and its lateen line:

| Class | square | studding | gaff | jibheaded | lug | lateen | sprit |
|---|---|---|---|---|---|---|---|
| Old | 1.23 | **1.25** | 1.29 | 1.32 | 1.29 | 1.25 | (none) |
| New | 1.23 | **1.44** | 1.29 | 1.32 | 1.29 | 1.25 | **1.20** |

The new test file holds three tests:
- each class's peak to two places, against the engine sampled every 0.01°;
- the table itself;
- the generator's air density, knot and shear, the same as the engine's.

**The generator, measured:**
- The unchanged generator writes all 18 files byte for byte.
- The patched one writes 9 byte for byte: the bilander, the cutter, the lugger, the smack and the
  five boats.
- In the other 9, **74 figures move, every one a `rating_kn`**: 70 studding-sail booms and 4
  ringtail booms, each up by 1.44/1.25, about a seventh. Nothing else in any file moves.
- The booms' "Rating: ... in 18 kn -> N kN." comments change in 37 lines, in the brig, the merchant
  brig, the frigate and the two schooners.
- This is the preliminaries' table (Eng §1.3).

| File | Booms, old -> new kN (each a pair unless named) |
|---|---|
| frigate-36 | fore lower 4.2 -> 4.9, fore topmast 5.6 -> 6.4, fore topgallant 1.8 -> 2.1, main topmast 7.0 -> 8.1, main topgallant 2.3 -> 2.6; ringtail 4.0 -> 4.6 |
| razee-44 | 6.0 -> 6.9, 7.9 -> 9.0, 2.7 -> 3.2, 9.4 -> 10.9, 3.4 -> 3.9; ringtail 3.7 -> 4.2 |
| sixty-four | 6.1 -> 7.0, 8.0 -> 9.2, 2.8 -> 3.2, 9.5 -> 11.0, 3.4 -> 4.0 |
| seventy-four | 8.4 -> 9.7, 10.9 -> 12.5, 3.9 -> 4.5, 15.0 -> 17.3, 4.9 -> 5.7 |
| brig, merchant-brig | 2.1 -> 2.4, 2.9 -> 3.3, 1.1 -> 1.2, 3.1 -> 3.6, 1.1 -> 1.3 |
| hermaphrodite-brig | 3.4 -> 3.9, 3.5 -> 4.0, 1.3 -> 1.5 |
| both schooners | fore topmast 2.2 -> 2.6; ringtail 3.9 -> 4.5 |

**Truth 35, on real ticks** (measured):
- **Old:** the main topmast studding-sail boom (larboard) carries away on the 2nd second of the
  first 32-kn gust, the booms at 2.38 of their rating, and its starboard fellow on the 2nd second of
  the second blow.
- **New:** no boom goes anywhere in the run (the booms at 2.11 at most). The routine fires as
  before: 120 s, three orders, once and then twice.
- **One blow held 121 s on the candidate:**
  - in 32, 34 and 35 kn nothing goes;
  - in 36 kn the fore lower studding-sail boom (starboard) goes on the 2nd second, and three more
    booms by 102 s, booms only;
  - in 37 kn the mizzen royal yard goes first.
- So the clause can be restated at a 36-kn blow. Which boom goes, and when, is the strain stream's
  draw at the truth's seed.

**The frigate brought up to six points** (`tests/test_studding.py`, measured):
- **Old, in 13 kn:** booms go at 374, 1,134 and 1,635 s (peak 1.90).
- **New:** none goes in the half hour (peak 1.63). Kept on, the first goes at 6,615 s (1 h 50 min),
  its condition worn to nought.
- In 14 kn the first goes at 978 s, and in 15 kn at 99 s.

**Tests** (62 run on the candidate: the 59 that bear on it, which at the base gave 57 passed and the
schooner's 2 expected failures, and the 3 new ones, which pass): **7 move**, each listed in §2.5.

**The seven byte pins** pass on the candidate, because the generator and the files move together.
With the generator moved and the files not, all seven fail, so they do hold the files to the
generator:
- truth 7-185;
- `test_ship_particulars`'s `test_generator_reproduces_the_committed_files`;
- `test_profile`'s hook test;
- `test_neufchatel`'s writer test;
- the generator's report tests of `test_bellerophon`, `test_indefatigable` and
  `test_hull_schooner`.

**Held** (measured):
- truths 9 and 14 (both tests of each), and the Neufchatel's truth 9;
- the rest of `test_studding`;
- `test_lateen`'s rating pass at the gaff's peak, and `test_profile`'s lateen rating;
- `test_strain`, `test_canvas`, `test_sails` and `test_catalogue` run whole: 152 passed and 1
  expected failure, the same both ways.

### 2.2 The tiller's key (A3)

**The candidate.** A unified diff of 19 files: 188 insertions and 38 deletions.
- **The key:** `hull.helm`, wheel or tiller, defaulting to wheel (`freesail/ship/schema.py`, stage
  0's item 5). Anything else is refused: "hull has 'helm' = 'yoke'; a helm is one of wheel,
  tiller." It is pickled only where it is not the wheel.
- **The files:** `helm: tiller` with a sourced note, written by the generator into the six tiller
  files (§3). That is two lines under `hull:` in each, and the other twelve files are
  byte-identical.
- **The tiller's words** wherever a helm is shot away, rigged round or mended: the hit, the refusal,
  the heave-to's aside, the tackles' lines, the repair's lines, the captain's reason and mend order,
  and the work's name in the log.
  - The wheel's words are package 116's exactly, and `HELM_LOST_WORDS` and `HELM_LOST_ASIDE` are
    kept as the wheel's.
  - The hit's random draws are unchanged.
- **Four synonyms** of `repair the wheel` (`data/vocabulary.yaml`): "ship the spare tiller", "ship a
  spare tiller", "ship a new tiller" and "repair the tiller".

**Measured, old beside new.** Each of the six files, and the brig as the wheel's control, starts
bare from the harbour at seed 7. At 60 s her helm is shot away by `combat.hits._deck_hit` itself,
its draw forced and nobody hurt. Then the orders are given in turn: `steer north`, `rig the
relieving tackles`, `repair the wheel` (twice), `repair the tiller` and `ship the spare tiller`.

| Ship | Lines (all ticks and kinds the same) | Rove (sampled) | Mended (sampled) |
|---|---|---|---|
| cutter | 12 of 12 | 390 s | 2,610 s |
| lugger | 11 of 11 | 390 s | 2,610 s |
| smack | 12 of 12 | 480 s | 2,640 s |
| topsail schooner | 11 of 11 | 450 s | 2,670 s |
| privateer schooner | 12 of 12 | 450 s | 2,670 s |
| hermaphrodite brig | 12 of 12 | 450 s | 2,640 s |
| brig (wheel) | 12 of 12 | 450 s | 2,670 s |
| first action, seed 6, the player at the prompt | 24 of 24 | 1,510 s | 5,595 s |
| first action, seed 6, left to the captain | 32 of 32 | 1,380 s | (the captain's repair at 4,620 s) |

On a tiller hull these lines move, words only:

| Line | Old | New |
|---|---|---|
| The hit | "The wheel is shot away; the helm is lost until the relieving tackles are rove: 'rig the relieving tackles'." | "The tiller is shot away; ..." (the rest the same) |
| The refusal | "... The wheel is shot away and the helm does not answer: rig the relieving tackles ('rig the relieving tackles') to steer her from below, or repair the wheel ('repair the wheel')." | "... The tiller is shot away ... to steer her by them, or ship the spare tiller ('ship the spare tiller')." |
| The heave-to's aside | "the helm not answering, the wheel shot away" | "... the tiller shot away" |
| The tackles begin | "Rig the relieving tackles! Hands below to the tiller." | "Rig the relieving tackles! Hands aft to the tiller." |
| The minute line | "Shot from the enemy: the wheel shot away." | "... the tiller shot away." |
| The tackles rove | "The relieving tackles are rove to the tiller and manned below: ... more slowly than by the wheel." | "The relieving tackles are hooked to the stump of the tiller and manned on deck: ... more slowly than by the tiller." |
| The repair begins | "Repair the wheel! The carpenter's crew to the wheel; new wheel-ropes to be rove." | "Ship the spare tiller! The carpenter's crew aft to the rudder head." |
| At quarters | "Repairing the wheel at quarters: four hands taken from No. 3 gun ..." | "Shipping the spare tiller at quarters: ..." |
| Given twice | "The hands are repairing the wheel already." | "The hands are shipping the spare tiller already." |
| The repair done | "The wheel is repaired and new wheel-ropes rove: she steers by the wheel again; the relieving tackles are cast off." | "The spare tiller is shipped in the rudder head: she steers by the tiller again; the relieving tackles are cast off." |
| The helm whole | "the wheel is whole and she steers by it" | "the tiller is whole and she steers by it" |
| The captain | "By the captain, engaging: rigging the relieving tackles (the wheel shot away)."; "By the captain, taking possession: repairing the wheel (...)" | "... (the tiller shot away)."; "... shipping the spare tiller (...)" |
| `repair the tiller`, `ship the spare tiller` | "... is not an order this ship understands ..." | understood: "the tiller is whole and she steers by it" |

- **On the brig**, a wheel hull, only the two new synonyms move: "not an order this ship
  understands" becomes "the wheel is whole and she steers by it". Every wheel word is the same.
- **The first action's ship is the cutter** (`data/scenarios/first-action.yaml:38`), a tiller hull.
  So her passage moves in words:
  - the hit; the refusal; the aside; the tackles' start; the minute line, "Shot from a cutter: the
    tiller shot away."; the tackles rove; the repair's start; the robbed gun's line; the order given
    twice; the repair done; the helm whole.
  - Unmoved: "The hands are rigging the relieving tackles already." and the belay line.
- **The tests** (`--slow`, `-n 2`):
  - the first candidate, 702 tests: 692 passed and 10 failed;
  - the fuller one, which adds the work's name and the captain's mend order (`test_held_work` whole
    and the four helm truths): 50 passed and 3 failed;
  - the base, the moved files and truths on 5067945e: 111 passed.
  - The grammar book passes with the new synonyms, which flow into its generated page. The
    checkpoint's, the boats', the fight's and the far action's tests pass.
- **11 pinned results move** (§2.5). Truth 7-626 holds: its asserted words are the same on either
  helm. Without the candidate's second part (the work's name and the captain's mend order) the count
  is 10, and those two lines keep the wheel's words on a tiller hull.
- **Left as the wheel's, not measured:** the tackles' 300 s with six hands and the mend's 1,800 s
  with four. The design wants "its time and hands the hull's". A shorter mend on a tiller would move
  the six hulls' ticks after the mend begins, and no wheel ship's.

### 2.3 The words of a rig with no yards (A2)

**The candidate** changes `freesail/evolutions/scripts.py` alone, with no new field, so no
checkpoint name changes:
- the tack's end says "braced up" only if she has head or after yards;
- the wear's up-helm line says "; brace in the after yards" only if she has after yards, in both
  the bowline branch and the plain one;
- the wind-aft line says "; hauled out and braced up" only if she has a braced yard;
- the wear's end says "braced" or "braced sharp up" only if she has a braced yard;
- a new `CourseToSteer.unbraced()` gives "full and by", or "trimmed" where a course clause follows,
  so that "full and by" is not said twice. That word is JUDGEMENT, and no test reaches it.

**Measured.** All 18 files, tack and wear, were run in the lugger's pinned harness: seed 7, 15 kn,
the wind from 0°, her head 292.5°, plain sail braced sharp up, settled 2,400 s, then 600 s
recorded. In all 36 runs the ticks, the event kinds and the 10-second trace of heading, speed and
position are identical. **18 lines move, in 11 runs:**

| Run | Tick | Old | New |
|---|---|---|---|
| lugger, tack | 180 s | "Tacked; braced up on the larboard tack, heading ENE (68°)." | "Tacked; full and by on the larboard tack, heading ENE (68°)." |
| lugger, wear | 1 s | "Stand by to wear ship. Up helm; brace in the after yards." | "Stand by to wear ship. Up helm." |
| lugger, wear | 36 s | "Wind aft. Shifted over the sheets; hauled out and braced up. Lowered the foresail and the mainsail to dip them." | "Wind aft. Shifted over the sheets. Lowered the foresail and the mainsail to dip them." |
| lugger, wear | 171 s | "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)." | "Wore ship; full and by on the larboard tack, heading ENE (68°)." |
| cutter, smack, topsail schooner, privateer schooner: wear | 1 s | "Stand by to wear ship. Up helm; brace in the after yards." | "Stand by to wear ship. Up helm." |
| the five boats: wear | 1 s | as the row above | as the row above |
| the five boats: wear | 30 to 43 s | "Wind aft. Shifted over the sheets; hauled out and braced up." | "Wind aft. Shifted over the sheets." |

- The cutter's and the smack's wind-aft lines and wear's ends stand, since both have head yards.
- The boats' tacks are refused for want of way, and their wears do not end within 600 s.
- The smack's tack is refused at the harness, as the plan said: "She is not close-hauled; bring her
  by the wind before going about."
- Unchanged: the bilander, the brig, the merchant brig, the frigate, the razee, the 74, the 64 and
  the hermaphrodite brig.

**Tests**, the fast tier of 23 files (2,289 tests): **4 failed**, all A2's words (§2.5).
- **The count found two digests more**, in tests that already fail at the base, so their outcome
  does not change:
  - the captain's trial `trade_stranger`: 028b011b3d6b2ccb becomes afd52152da8112d2 (pinned
    48c8948f87088a76);
  - truth 77: f9851749c0d55427 becomes 5bee74a129515ca6 (pinned 16272dee77120779).
  - Which line moves in them is not traced.
- **The primer's schooner log** (`docs/primer/05-going-about.md:357`), which no test reads, keeps
  "Up helm; brace in the after yards." It is already out of date: it has no "shifted over the
  sheets".

**The same cause, found and left out of the narrow patch** (read, not measured):
- the lugger's heave-to says "Hands to the after braces";
- her fill-away says "man the after braces", "Braced the yards full" and "braced full";
- the cutter's box her off, box-haul and wear short round all say "Wind aft; braced up the after
  yards" of a rig with no after yards.
- Of these only "braced full and" in `tests/test_lying_to.py` is pinned, and its ship was not
  traced.

### 2.4 The smack's topsail (A5, A6)

**A5, a yard's level.** `Ship.yard_level()` in `ship/graph.py` gives the level of the spar the yard
is slung on, plus one for each yard slung below it on that spar by height:
- a whole lateen's yard below counts as a level (the lean ruled for the tartane);
- yards under the bowsprit are 0;
- the level is kept in a `WeakKeyDictionary`, never pickled with the ship;
- it is read at the ten functions (twelve places) of Pol-D §5.1, in `scripts.py`, `trim.py`,
  `verbs.py` and `physics/sails.py`.

Measured (17 cases of the smack: seed 7, 15 kn unless said, her head 292.5°, figures taken 600 to
900 s after the order):
- **The guard over every file's yard levels:** every braced yard of the 18 files is equal, but the
  smack's `topsail.yard`, which goes from 0 to 1.
- **Heave to with her topsail set:**
  - old: "Hauled up the courses." and, at 164 s, "Hove to on the starboard tack, under her
    fore-and-aft canvas, foresail sheet to windward, helm a-lee."; 47.26° off the wind, 2.615 kn;
  - new: "...; braced the topsail aback; helm a-lee." and, at 153 s, "Hove to on the starboard tack,
    topsail to the mast, helm a-lee."; 50.55° off, 2.873 kn;
  - she forereaches 0.26 kn faster with the topsail to the mast, which wants the builder's reading.
- **Lie a-try with her topsail set:** refused before ("She has no topsail to lie a-try under."),
  done now: at 298 s she is "Lying a-try under the topsail and the foresail, helm a-lee.", 43.2° off
  at about 1.0 kn.
- **Two sets of words want mending:**
  - lie a-try under plain sail is now refused with "The topsail is not set; set it, close-reefed, to
    lie a-try under it.", but her topsail has no reef bands;
  - "haul up the topsail", obeyed before as a course, is now refused: "A topsail or light sail is
    clewed up, not hauled up ...".
- **Unchanged:** heave to under plain sail; take in, clew up, furl, set and reef (no bands); trim
  with all sail; send down the topgallant yards and strike the topmast (both already refused in
  words); wear with the topsail set; shorten sail at 30 kn.
- **Tests:** 268 smack tests, the slow ones among them, all passed. They include the seine passage,
  her sweep and polar, truths 7b-105, 7b-106 and 7-625, the hull and the fishing. **No pinned result
  moves.**

**A6, the pole's quick handing**, on A5:
- `Ship.on_pole()`: a braced yard at a level above 0 on a lower mast with no topmast;
- `evolution_key` routes it to a "pole" key, and the runner accepts the class;
- `data/vocabulary.yaml` gains pole rows for take in, furl and reef;
- three new files:
  - `take_in_pole.yaml`: one 60 s step, no settling;
  - `furl_pole.yaml`: the lowering 60 s, then the furl at 120 s (JUDGEMENT: 150 s less 30 s for the
    climb);
  - `reef_pole.yaml`: the yard lowered onto the yard below first.
- No "lowered" state is kept; V2's drawing will want one.

Measured, beside A5:

| Order | A5 | A6 |
|---|---|---|
| take in the topsail | 1 s "Hands to the topsail clewlines and buntlines."; 88 s "Clewed up the topsail."; 154 s "Took in the topsail; hanging in the gear." | 1 s "Let go the topsail halyards; hands to the clewlines and buntlines."; 88 s "Lowered the topsail down onto the yard below and clewed it up there."; 88 s "Took in the topsail; lowered on the yard below, hanging in the gear." |
| clew up the topsail | as take in | as take in |
| lower the topsail | refused | obeyed, as take in |
| haul up the topsail | refused ("A topsail or light sail is clewed up, not hauled up ...") | refused: "A pole sail is lowered, not hauled up; say 'lower the topsail' or 'take in the topsail'." (the words want mending) |
| furl the topsail, set | "Lay aloft and furl the topsail."; furled at 350 s | "Lay out on the yard below and furl the topsail."; "Furled the topsail on the yard below." at 300 s |

- Unchanged: reef (no bands, so `reef_pole` reaches no committed file); set; heave to; lie a-try;
  trim; send down; strike; wear; shorten sail.
- Tests: her slow set, 56 passed. A fast set of 3,809 tests: 2 failed and 1 xfailed. The count found
  three more (§2.5).

### 2.5 The count, both tiers whole

**Run** (measured; the `count` folder). The four patches were applied in a fresh scratch worktree at
5067945e, in this order:
1. item 37's source patch;
2. A2;
3. A5 and A6 together;
4. A3 without its ship files;
5. the ship files, regenerated by `py tools/gen_ships.py`.

All applied cleanly, and the 12 regenerated files are the measurers' own, file for file. A5 and A6
move no ship file.

| Tier | Base (5067945e) | With the four |
|---|---|---|
| Fast, `-n 4` | 8,370: 8,356 passed, 13 skipped (the browser tests), 1 xfailed; 1 h 26 min | 8,373: 8,335 passed, 24 failed (23 the candidates', 1 the replay's timing), 13 skipped, 1 xfailed; 1 h 35 min |
| Slow, `--slow -m "slow and not pace"` | 567: 532 passed, 10 failed (the base's, §1.1), 14 skipped, 11 xfailed | 567: 530 passed, 12 failed (the base's 10, truth 35 and the frigate at six points), 14 skipped, 11 xfailed |
| Pace, `--slow -m pace` | 15: 11 passed, 4 failed (under the floor) | the same 4 and 11 |

**Each mover was re-run alone** on the base, on each candidate alone and on the four together. The
four together fail exactly the union of the single steps' failures: the candidates do not interact.
A5 alone moves nothing.

| # | Test (passed -> failed) | Step | Old | New |
|---|---|---|---|---|
| 1 | `tests/test_known_truths.py::test_truth_35_shorten_sail_fires_once_after_two_minutes_over_thirty_and_not_on_a_gust` (slow) | A0 | a studding-sail boom goes on the 2nd second of a 32-kn gust | none goes; restated at 36 kn (§2.1) |
| 2 | `tests/test_studding.py::test_brought_up_to_six_points_they_shake_strain_and_carry_away[frigate]` (slow) | A0 | first boom at 374 s in 13 kn | none in the half hour; first at 6,615 s, or 978 s in 14 kn |
| 3 | `tests/test_hull_frigate.py::test_no_figure_the_physics_or_the_gunnery_reads_moved` | A0 | as filed | 11 boom ratings |
| 4 | `tests/test_hull_brig.py::test_no_figure_the_physics_or_the_gunnery_reads_moved[data/ships/brig.yaml]` | A0 | as filed | 10 boom ratings |
| 5 | the same, `[data/ships/merchant-brig.yaml]` | A0 | as filed | 10 boom ratings |
| 6 | `tests/test_hull_schooner.py::test_no_figure_the_physics_reads_moved[data/ships/topsail-schooner.yaml]` | A0 and A3, each alone | as filed | 3 boom ratings; the hull's `helm: tiller` |
| 7 | the same, `[data/ships/privateer-schooner.yaml]` | A0 and A3, each alone | as filed | the same |
| 8 | `tests/test_settee.py::test_the_luggers_tack_and_wear_are_as_they_were[tack ship-lines0]` | A2 | "Tacked; braced up ..." at 180 s | "Tacked; full and by ..." |
| 9 | the same, `[wear ship-lines1]` | A2 | the lines at 1, 36 and 171 s | as §2.3 |
| 10 | `tests/test_evolutions.py::test_with_no_head_yards_the_wear_squares_none[the lugger]` | A2 | "Wind aft. Shifted over the sheets; hauled out and braced up." | "Wind aft. Shifted over the sheets." |
| 11 | `tests/test_rig_geometry.py::test_going_about_lets_the_bowlines_go_and_steadies_them_out_again[wear-schooner]` | A2 | "Stand by to wear ship. Up helm; clear away the bowlines; brace in the after yards." | "Stand by to wear ship. Up helm; clear away the bowlines." (the test's own comment says the schooner "has no after yards") |
| 12 | `tests/test_agents.py::test_the_contents_says_what_each_topic_costs_measured_from_the_text_served` | A6 | "110 evolutions" | 113 (112 without `reef_pole`) |
| 13 | `tests/test_catalogue.py::test_the_catalogue_reaches_forty_and_every_file_loads` | A6 | passes | "reef_pole takes everyone and names no party": `ALL_HANDS_SAIL_WORK` (l. 48) would have to name it; goes if `reef_pole` is left out |
| 14 | `tests/test_held_work.py::test_every_work_is_named_by_one_road_in_both_forms_where_a_line_names_the_work` | A6 | passes | fails on `furl_pole`: its sweep sails the bilander, the topsail schooner and the 74, none with a pole |
| 15 | `tests/test_held_work.py::test_no_line_that_names_a_work_names_it_by_its_id` | A6 | passes | the same |
| 16 | `tests/test_in_world.py::test_the_library_topics_are_in_world_on_a_kings_ship[catalogue]` | A6 | passes | the three new files' descriptions, served to the player, say "(package 90, A6)" and name a design document: the draft's own fault |
| 17 | `tests/test_hull_cutter.py::test_the_hull_figures_stand_as_filed` | A3 | the hull as filed | with `'helm': 'tiller'` |
| 18 | `tests/test_hull_cutter.py::test_a_diff_of_her_physics_keys_against_git_shows_none` | A3 | no key | the one key |
| 19 | `tests/test_hull_lugger.py::test_no_hull_figure_the_physics_reads_moved` | A3 | as filed | the one key |
| 20 | `tests/test_hull_lugger.py::test_a_diff_of_her_files_physics_keys_against_git_shows_none` | A3 | no key | the one key |
| 21 | `tests/test_hull_smack.py::test_no_figure_the_physics_reads_has_moved_by_the_pins` | A3 | as filed | the one key |
| 22 | `tests/test_hull_smack.py::test_her_file_but_for_her_lines_is_what_it_was_against_git` | A3 | as filed | the one key |
| 23 | `tests/test_known_truths.py::test_truth_7_632_the_wheel_shot_away_stops_the_helm_until_the_tackles_are_rove` | A3 | the refusals end with the wheel's `HELM_LOST_WORDS`; the aside "the wheel shot away" | the tiller's (§2.2); its two assertions on the constant hold |
| 24 | `tests/test_known_truths.py::test_truth_7_633_by_the_tackles_she_answers_at_half_the_wheels_rate_until_it_is_repaired` | A3 | the relieved, repaired, given-twice and whole lines in the wheel's words | the tiller's; the rates unmoved (half the wheel's by the tackles) |
| 25 | `tests/test_known_truths.py::test_truth_7_634_the_games_own_captain_answers_a_lost_wheel_as_a_seaman_would` | A3 (its second part) | "By the captain, taking possession: repairing the wheel (...)" | "... shipping the spare tiller (...)" |

**By step:** A0 7, A2 4, A5 0, A6 5, A3 11, less the 2 schooner records counted under both: **25**.
With A2's two digests (§2.3): **27 pinned results move**.
- **The three new tests** of `tests/test_peak_coeff.py` pass.
- **No byte pin of the generator changes outcome.** The seven pass by the regeneration.

## 3. (c) The tiller-steered files, read from their sources

The six files of the plan's A3 row are confirmed by their notes. The Decisions note's "the
Neufchatel" is the hermaphrodite brig. Every helm note is judgement; the sources behind them differ
in strength. The sources were read in `docs/references/`, with the OCR's lines.

| File | Her note | The source behind it |
|---|---|---|
| topsail-schooner, privateer-schooner (Lynx's draught) | "One man at the tiller (a Baltimore schooner steered with a tiller; judgement)" | **Direct.** Chapelle 1930, p. 83, on H.M. schooner *Musquidobit*, late *Lynx* (fig. 17): she "apparently steered with a tiller, from the position of her rudder head" (OCR l. 4855); the deck plan on that page shows the rudder head and a tiller |
| lugger (*L'Éclair*, ZAZ6306) | "One man at the tiller (a lugger steers with a tiller; judgement)" | **The type.** Holdsworth 1874, p. 104: the Yarmouth luggers' mizen stepped to port for the tiller's play (OCR l. 4776); pp. 196-197: the Cornish luggers' mizen stepped forward, out of the tiller's way. Her sheet shows "a Y-shaped fitting on the rudder head" (`pages-zaz6306.md:121`), read and not identified |
| cutter (*Sherbourne*, ZAZ6381) | "One man at the tiller (a cutter steers with a tiller; judgement)" | **The rule only.** Falconer 1780, HELM: the wheel, "except in small vessels, where the wheel is unnecessary" (OCR l. 9815); Lever 1827, the Rudder, fig. 373, the tiller moved by a wheel in large ships. No draught's helm is read in her notes |
| smack (*Culloden*; Chapman Pl. LIX No. 3) | "One man at the tiller (judgement)" | **The rule only**, as the cutter's |
| hermaphrodite-brig (*Prince de Neufchatel*, 110 ft 8 in on deck) | "One man at the tiller, as the privateer schooner's (judgement)" | **None read for her helm.** Against it, Chapelle 1930, p. 136: the slave brig *Diligente* of 1839, 100 ft between perpendiculars, built "probably" at Baltimore or Havana (p. 135), whose plan "does not show whether she steered with a tiller or wheel, but probably the latter" (OCR l. 8475). The least sure of the six; her draughts ZAZ6177 and ZAZ6179 are not yet read for it |

**By the wheel** (twelve files, the key's default):
- the frigate-36, the razee-44, the 74 and the 64: "Two quartermasters at the wheel (Luce 1884 ch.
  XX ...)";
- the brig: the same note. Steel 1805's contract for the *Raven* brig of 18 guns (p. lxv) has both
  a wood tiller and a steering wheel;
- the merchant brig: by judgement;
- the bilander: "One man at the helm, as the merchant brig's (judgement)". No source either way, and
  Falconer's "small vessels" might reach her. She is left on the wheel by default, outside the six;
- the five boats: steered by a yoke and its lines by their own files (for example
  `boat-cutter-23.yaml:36`). They read `wheel` by the key's default. No road was found in which a
  boat takes a deck hit (`resolve_shot` is called only from the action's battery and on far hulls),
  and the two helm evolutions apply only to class ship.

## 4. The backed square topsail beside the lateens (nudge 20)

### 4.1 The hull and the run

**The hull.** The brig: 26.8 m on the water, 413 t (`data/ships/brig.yaml`). Of the eighteen ships
with a square topsail on a topmast, she lies in length between the polacre (about 24.5 m in her
design) and the xebec (28.5 m, about 330 t). She is also the very hull the polacre and xebec probes
stand on (`tests/rig_fixtures.py`, `polacre_probe_doc`), so the figures differ by the rig alone. Two
checks were run as well:
- the cutter, 15.2 m and 106 t, the tartane probe's own hull;
- the bilander, 21.5 m and 229 t, a square topsail over a settee.

**The run** (measured on the base, nothing changed; `g1/ts`):
- settled close-hauled under plain sail in 15 kn, as the lateen probes start; then the topgallants
  and the courses taken in ("alone"), or plain sail kept ("plain");
- the wind raised to the target over 60 s, with no gust and no sea;
- the ratings the file's own, by the generator's rule. The brig's main topsail yard is rated
  37.7 kN, her main topmast 144.8 kN and her main lower mast 436.6 kN.

Three ways of being aback were run:
- **held aback**: `heave to`, the main topsail to the mast and the helm tended;
- **taken aback by a shift**: the wind shifted 20° onto her other bow on one tick with her way on,
  the lateens' own measure, every square sail aback;
- **drawing**, for scale: close-hauled with the sails trimmed.

### 4.2 The brig

**Held aback** (the main topsail's chain; the mean over the last 120 s):

| kn | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 | 56 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Main topsail yard | 0.29 | 0.41 | 0.55 | 0.69 | 0.85 | 0.99 | 1.13 | 1.24 | 1.33 | 1.40 | 1.43 |
| Main topmast | 0.07 | 0.11 | 0.14 | 0.18 | 0.22 | 0.26 | 0.29 | 0.32 | 0.35 | 0.36 | 0.37 |
| Main lower mast | 0.03 | 0.05 | 0.06 | 0.08 | 0.10 | 0.12 | 0.14 | 0.16 | 0.17 | 0.18 | 0.19 |

- The yard strains from 40.2 kn and is at risk in no wind to 60 (its peak 1.48).
- The cloth reaches 1.44 at 60; it splits at 1.8.
- Drawing close-hauled, the same yard stands at 0.66 at 40 kn and 0.81 at 44, so held aback it
  carries about one and a half times its drawing load.
- Under plain sail, hove to with the topgallant aback as well: the topsail yard strains from 41.6
  kn. The main topgallant yard, rated for 25 kn, carries away from 40 kn (at 281 s; at 69 s in 44).
  The topmast is at most 0.46 and the lower mast at most 0.22.

**Taken aback by a shift** (peaks):

| kn | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 | 56 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Main topsail yard | 0.40 | 0.54 | 0.75 | 0.96 | 1.19 | 1.40 | 1.57 | 1.66 | 1.78 | 1.99 | 2.24 |
| Main topmast | 0.10 | 0.14 | 0.19 | 0.25 | 0.31 | 0.36 | 0.41 | 0.43 | 0.46 | 0.52 | 0.58 |
| Main lower mast | 0.05 | 0.06 | 0.08 | 0.12 | 0.13 | 0.19 | 0.21 | 0.24 | 0.26 | 0.18 | 0.21 |
| Fore topsail yard | 0.38 | 0.62 | 0.74 | 0.96 | 1.12 | 1.52 | 1.83 | 1.65 | 1.77 | 1.98 | 2.23 |
| Fore topmast | 0.24 | 0.34 | 0.47 | 0.61 | 0.74 | 0.88 | 0.96 | 0.61 | 0.65 | 0.73 | 0.82 |
| Fore lower mast | 0.10 | 0.14 | 0.20 | 0.26 | 0.31 | 0.37 | 0.40 | 0.26 | 0.27 | 0.30 | 0.34 |

- The main yard strains from 32.7 kn at its peak and is at risk from 42.4; the fore yard from 33.0
  and 39.8.
- The main yard's two-minute mean strains only from 40.4 kn.
- Both topsails split on the shift's first second at 56 and at 60 kn, so their yards' peaks there
  are an instant's.
- The jib and the fore topmast staysail blow out from 40 kn.

### 4.3 The checks, and the winds together

| Hull and case | Yard strains (1.0) from | Yard at risk (1.5) from | Topmast at most | Lower mast at most |
|---|---|---|---|---|
| **Brig, held aback** | **40.2 kn** | **none to 60** (1.43 at 60) | 0.39 | 0.20 |
| Brig, plain sail hove to | 41.6 kn | none to 60 | 0.46 | 0.22 |
| **Brig, a shift's peak** | **32.7 kn** (fore 33.0) | **42.4 kn** (fore 39.8) | 0.96, the fore, for an instant at 44 kn | 0.40, the fore, at 44 kn |
| Cutter, held aback | 43.2 kn | none to 60 (1.22 at most) | 0.60 | 0.32 |
| Cutter, a shift's peak | 30.2 kn | her light topsail splits at a shift of 40 kn as the yard reaches 1.50 | 0.64 while it stands; 1.06 to 1.28 for one second as it splits, at 52 kn and over | 0.44 |
| Bilander, a shift's peak | 40.2 kn | 45.7 kn | the main 0.77; the fore 1.04 for an instant at 48 kn | the main 0.40; the fore 0.62 |

The bilander's `heave to`, ordered with her topgallants and courses in, set about loosing her main
topgallant and did not lie her to in 15 minutes. So she has no held-aback figure (seen on the way,
not diagnosed).

**What the engine does with a backed square sail, then:** it strains its yard and splits its cloth.
It brings a topmast to the strain line only for an instant, and never to risk, and no lower mast
passes 0.62 of its rating on the three hulls in any wind to 60 kn. The reason is the generator's
rule: a topmast is rated for all the sail it can carry, and a lower mast for everything on it in 55
kn (Eng §2.4.3).
- On the brig the topmast is rated at about four times its topsail yard, and the lower mast at
  about twelve times.
- A lateen's mast that carries only its lateen (the polacre's and the xebec's mizens, the xebec's
  three) is rated as its yard, and strains with it.
- A lateen's mast that carries more (the tartane's main, with her topsail) is rated about twice its
  yard. Aback at the ruled factor, it strains from about 38 kn.
- So A1d's lateen loads its mast where a backed topsail, today, does not. The owner's sentence
  ("as a backed square sail does ... the sail may strain the mast") is answered in kind for a
  lateen mast, and not by the square sail's own figures. This is set out for the lead, not ruled.

**The lateens beside** (the nudge 19 probes, re-run on 5067945e: digit for digit the preliminaries'
figures, so the trunk's merge moved nothing under them):

| | Strains its yard from | May carry it away from | The factor |
|---|---|---|---|
| A lateen aback by a shift (**ruled**) | about 28 kn (1.02 to 1.08 in 28.6) | about 35 kn (1.35 to 1.46 in 34.3) | `LATEEN_ABACK_LOAD` about 2.5 |
| A lateen aback in stays (**ruled**) | about 30 kn | about 36 kn | the same |
| **The bad hand, as drawn** | **about 45 kn** (the polacre probe's 0.985 and 1.014 in 45.5) | **about 55 kn** | `LATEEN_BAD_HAND_LOAD` about 2, on the two-thirds' pull |
| A square topsail aback by a shift (the brig) | 32.7 kn | 42.4 kn | none: the plate's own force |
| A square topsail held aback (the brig) | 40.2 kn | none to 60 | none |

- The ruled aback figures are about 5 kn under a square topsail taken aback by the same shift on the
  hull of like size.
- Corrected by this run: Eng §2.4.3 gave a backed square sail, "read, not run", a strain from about
  45 kn and a risk from about 56.

### 4.4 The bad hand's factor, for the lead's ruling

The load on the chain is the factor times the pull, so the factor for a strain at a wind W is 2.0
divided by the yard's ratio at factor 2 in W (computed).

**The bad hand at factor 2** (measured; the yards' peaks):

| kn | 33 | 35 | 36 | 38 | 40 | 42 | 44 | 45.5 |
|---|---|---|---|---|---|---|---|---|
| Polacre probe, fore / mizzen | 0.50 / 0.58 | 0.56 / 0.64 | 0.60 / 0.70 | aback | aback | aback | 0.94 / 0.93 | 0.985 / 1.014 |
| Tartane probe, great yard (heeled) | 0.556 | 0.601 | 0.622 | 0.665 | 0.705 | 0.746 | 0.784 | 0.807 |

The polacre probe goes aback on the bad hand at 38 to 42 kn, and the xebec probe from 33 kn up, so
neither gives a bad-hand figure there.

**The factor for a given strain wind:**
- for a strain at 40 kn: about 2.5 (the polacre probe 2.5 to 2.6; the tartane's great yard 2.8, her
  mizen 3.4);
- at 35 kn: about 3.3 (3.1 to 3.6);
- at 33 kn: 3.5 to 4.0.
- The wind of risk is about the strain's wind times √1.5, the load going as the wind's square
  (computed).

**Each factor, and what it does in the rules captain's own handling.** The figures at factor 2 are
Eng §2.4.3's, measured; the rest are scaled by the factor (computed, not run):

| Factor | Strains from | At risk from | 12 kn, 1,800 s (the rules captain's board) | 15.6 kn (a 12-kn wind's top gust) | A lateen waiting its turn after a wear, 28.6 kn | the same, 39 kn (a 30-kn wind's top gust) |
|---|---|---|---|---|---|---|
| 2 (as drawn) | about 45 kn | about 55 | 0.07 to 0.10 | 0.12, 0.14 | 0.36 to 0.47 | 0.59 to 0.83 |
| **2.5** (the topsail held aback) | **about 40 kn** | **about 49** | 0.09 to 0.13 | 0.15, 0.18 | 0.45 to 0.59 | 0.74 to 1.04 |
| **3.3** (the lead's 35 kn) | **about 35 kn** | **about 43** | 0.12 to 0.17 | 0.20, 0.23 | 0.59 to 0.78 | 0.97 to 1.37 |
| 3.75 (a shift's peak, 33 kn) | about 33 kn | about 40 | 0.13 to 0.19 | 0.23, 0.26 | 0.68 to 0.88 | 1.11 to 1.56 |

- **The lean (JUDGEMENT): 2.5, beside the topsail held aback.** The bad hand is a sail pressed
  steadily against its mast, a standing state and not a shift's blow, and so is a topsail held to
  the mast. It is also the aback factor already ruled, the same figure on its own pull. It strains
  from about 40 kn and is at risk from about 49. A lateen waiting its turn after a wear, in a 30-kn
  wind's top gusts, touches its rating for a moment and is not at risk.
- **The lead's 35 kn** wants about 3.3. It is also inside the rules captain's book: the board under
  12 kn stays under a fifth of the rating. But a lateen waiting its turn after a wear in a 30-kn
  wind's top gusts would then work under strain, up to 1.37, short of the risk.
- **At a shift's peak** (3.5 to 4) that same lateen comes to the risk line: 1.45 at 3.5, 1.56 at
  3.75. That is the one figure here that meets the rules captain's own wearing.
- **Masts at the same factors** (computed from the tartane probe's main mast, which carries her
  topsail too: 0.61 of its rating at 45.5 kn at factor 2):
  - at 2.5 it stands at 0.76 there;
  - at 3.3 it reaches its rating at about 45 kn;
  - a mast that carries only its lateen strains with its yard at any factor.

## 5. What the card expected, against what moves

| The card's "Expected to move" | Measured |
|---|---|
| Item 37's: truth 35's last clause, `test_studding`'s frigate case, five records naming the booms, and seven byte pins by regeneration | **As expected.** The 7 tests (§2.5, rows 1 to 7); the seven byte pins pass by the regeneration; the 74 figures in 9 files; truths 9 and 14 hold |
| A tiller's key in six files, and their words where a helm is shot away | **As expected in kind.** The six files, two lines each; their eight "no figure moved" records (rows 6, 7, 17 to 22: the plan's "their records name the key"). The words move on the six, ticks the same. **Not foreseen:** the first action's ship is the cutter, so the three truths of package 116 that pin those words move (rows 23 to 25); the plan expected truth 7-626 to hold "if her ship steers by a wheel" (she does not; 7-626 holds by its own assertions) |
| The words of a rig with no yards: the lugger's two transcripts in `tests/test_settee.py`, her wind-aft case in `tests/test_evolutions.py`, every tick the same; the cutter's and the smack's wear's first line, pinned by no test | **As expected**, rows 8 to 10, every tick the same; the cutter's and the smack's first line. **Beyond it:** `tests/test_rig_geometry.py`'s wear-schooner case (row 11); both schooners' wear's first line; the five boats' first and wind-aft lines; two digests in failing tests |
| The smack's topsail handled as a topsail (A5), lowered onto the yard below and furled from it (A6), and drawn so (V2) | **A5 as expected**: no pinned result; her heave-to and lie a-try move. **A6:** the handing as expected (take-in 154 -> 88 s, furl 350 -> 300 s, both JUDGEMENT); five pinned results move (rows 12 to 16), of which the card names one in kind, the count of evolutions |
| The counts that grow by a file, a role or an evolution (plan §10.4) | The evolutions' count, 110 -> 113 (row 12). It is in A6's step, which §10.4 does not list for it, but the card names such counts in kind |
| The 74's and 64's port word (V4); the lateen steps' counts and lists (A1a, A1b, A7); the bow's watch line; the primer named | Not measured here: none of these steps is drafted at the ground report |
| Each measured old beside new | Done for every move above |

**17 of the 25 are named by the card**, by name or by its lists: rows 1 to 10, 12, and 17 to 22.
**8 are not**: rows 11, 13 to 16 and 23 to 25 (§6).

## 6. What moves that the card does not name (stops, not rulings)

Each of these stops until the lead's word. None is ruled here.

**Pinned results the card does not name (8, and 2 digests):**
1. `tests/test_rig_geometry.py`'s wear-schooner case (A2): words only.
2. Truths 7-632, 7-633 and 7-634 (A3): words only. The card names "their words where a helm is shot
   away" in kind, but not these truths, and the plan expected the first action to steer by a wheel.
   Truth 7-634 moves only by the candidate's second part (the work's name and the captain's mend
   order).
3. `tests/test_catalogue.py`'s `reef_pole` (A6). It goes if `reef_pole` is left out, since the
   smack's topsail has no reef bands and no committed file reaches it.
4. `tests/test_held_work.py`, its two sweeps (A6). Their three ships carry no pole, so they find no
   ship for `furl_pole`. Mending it wants a pole ship in the sweep, a change to a test the card does
   not name.
5. `tests/test_in_world.py`'s catalogue case (A6): the draft's own words, which name a package and a
   design document to the player. It goes if the step is written in-world.
6. Two digests in tests already failing at the base (A2): `trade_stranger`'s and truth 77's.

**Unpinned moves on ships the card does not name:**
- A2: the two schooners' wear's first line, and the five boats' first and wind-aft lines.
- A3: the four synonyms reach the twelve wheel files too, so `ship the spare tiller` repairs a
  wheel; it was refused before as an order not understood.
- A5: the smack's "haul up the topsail", obeyed before as a course, is refused. Her lie a-try
  refusal says "close-reefed" of a topsail with no reef bands (a words fault).
- A6: the "haul up the topsail" refusal says "A pole sail is lowered" (the words want mending).

**Files the step needs that the card does not name for it (A3).** By the card, a step that needs any
other file stops, and the builder says so before touching it:
- `tools/gen_ships.py` beyond `SHIP_MODULES` and item 37: five hull dicts, the two schooners
  sharing one;
- `tools/ships/neufchatel.py`, the hermaphrodite brig's module;
- `freesail/evolutions/repair_scripts.py`: the tackles' and the repair's words;
- `freesail/orders/damage.py`: "The hands are {mending} already.";
- `freesail/world/captains.py`: two repair lines, outside its going-about rows;
- `data/evolutions/relieving_tackles.yaml` and `repair_wheel.yaml`: their start and fail lines.

`freesail/ship/schema.py` is stage 0's (the key is its item 5), so it is in order. The files A3's row
does name are `combat/hits.py`, `evolutions/scripts.py`, `runner.py`, `orders/verbs.py` and
`data/vocabulary.yaml`.

**Found by the same cause and left out of the narrow patches** (read, not measured):
- A2: the lugger's heave-to and fill-away braces' words, and the cutter's box her off, box-haul and
  wear short round "braced up the after yards". Only "braced full and" in `tests/test_lying_to.py`
  is pinned.
- A3: the primer's chapter 25 table (ll. 63-70) still gives the wheel's words, and no step names it.
  A saved game of one of the six from before the key reads `wheel` until a new start.

## 7. Corrections found by reading the outputs

- **A2 moves 18 lines in 11 runs**, not 12: the lugger's tack and wear, four wears (the cutter, the
  smack and the two schooners) and the five boats' wears.
- **The backed topsail's masts.** The reports said none ever strains. In fact:
  - the bilander's fore topmast touches 1.04 for an instant at a shift of 48 kn;
  - the cutter's topmast passes 1.0 (1.06 to 1.28) for one second as her topsail splits, in shifts
    of 52 kn and over;
  - the brig's fore topmast reaches 0.96 at a shift of 44 kn;
  - the lower masts reach 0.62 at most (the bilander's fore), and the cutter's 0.44 at a shift of
    56 kn.
  - None is at risk. "Never strains" holds for every mast held aback, and for every main topmast and
    lower mast at a shift.
- **The *Diligente*** is a Baltimore clipper of 1839 whose place of building Chapelle gives as
  "probably Baltimore or Havana" (p. 135), not a Baltimore-built brig.
- **Eng §2.4.3's backed square sail** (45 and 56 kn, read and not run) is corrected by the run: 40
  kn held aback, and 33 and 42 at a shift's peak (§4.3).
- **Eng §10 and the plan's A3 row** expected truth 7-626 to hold if the first action's ship steers
  by a wheel. She is the cutter. Her passage is pinned by truths 7-632, 7-633 and 7-634 as well as
  7-626, and the three move.
- **The plan's A2 row** names only the cutter's and the smack's wear's first line. Both schooners'
  first lines move too, and so do the five boats' first and wind-aft lines.
- **The plan's A5 and A6 rows** (§6, §10.4) expect no pinned passage. A5 moves none, but A6 moves
  five pinned results (§2.5, rows 12 to 16).

## 8. For the lead (and what goes to the owner)

1. **The count is over the line, so it goes to the owner:** 25 tests (27 with the two digests; 23 if
   A6 is drafted without its own two faults). Only item 37's two are how a ship sails; the rest are
   words, a key and counts, every tick the same.
   - **Pick: build**, with A6 drafted without `reef_pole` and in-world (rows 13 and 16 then do not
     move), and the card widened by name for A3's seven files and for the moves of §6 that remain:
     rows 11, 14, 15 and 23 to 25, and the two digests.
   - The other road: the owner trims a step, for example A3 without the captain's two lines (10
     instead of 11), at the cost of the wheel's words left on a tiller hull.
2. **The bad hand's factor** (§4.4). **Pick: 2.5**, beside the topsail held aback: strain about 40
   kn, risk about 49. The lead's 35 kn wants about 3.3, risk about 43. Either keeps the rules
   captain's board under 12 kn below a fifth of the rating.
3. **A3's seven files** (§6). **Pick: add them to the card.** Without the generator's hull dicts and
   `tools/ships/neufchatel.py` the key cannot be written into the six files at all. Without the
   other five, the tiller's words reach the hit and the refusal but not the tackles, the mend or the
   captain's lines, so the mend is half made. The other road: A3 kept to the files named, with those
   lines left in the wheel's words on the six hulls.
4. **A3's words and times** (JUDGEMENT, plan §13.1 item 3):
   - the tackles "hooked to the stump of the tiller and manned on deck";
   - the mend "Ship the spare tiller! The carpenter's crew aft to the rudder head";
   - the times and hands left as the wheel's.
   Pick: as drafted.
5. **A2's wider reach** (§6, the same cause). **Pick: inside A2**, at the cause, each line measured
   old beside new. The other road: left as listed.
6. **The hermaphrodite brig's tiller** (§3). Pick: keep it by judgement, as filed. The other road:
   read her draughts' deck (ZAZ6177, ZAZ6179) at stage 0. The bilander stays on the wheel by
   default.
7. **The trunk** (§1.1): merged into the package's branch before stage 0's hash, as the lead's
   note of 11:00 UTC asks. Not done in this commit.
