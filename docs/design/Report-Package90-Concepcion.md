# Report: package 90, the *Purísima Concepción* (her builder, from 28 November 2026)

Her builder's report to the coordinating session, in plan §8.0's form, one dated section per hash.
The branch is `…/pkg-90-concepcion`, cut from 93cf624c. This first section is A9's alone: its
hash goes to the lead on its own, merged before her file. Her file, her tests and her truths
follow in a later section with their own hash.

## 2026-11-28: A9, three gun decks, for the lead on its own: `eb018d1`

**In short.** A9 is built as plan §6 and Eng §6 describe:
- the quarter bill shuts and robs a `middle` deck with the lower;
- "the second deck" and "the third deck" name a three-decker's middle and upper decks;
- "the main deck" is refused in words on a three-decker, naming her three decks.

It is keyed on a broadside gun on a `middle` deck, which no committed file carries. So nothing
committed moves, and no pin moves. Its proof is `tests/test_three_decks.py`, 32 cases on stage 0's
probe with a middle deck. Besides that, all nineteen committed files were recorded before and after
A9: their beat to quarters, robbing, gunnery words and two passages, the same to the line (§A.3).
**The hash for the lead is `eb018d1`.** Its fast tier, whole, against a base on its merged tree:
**no test changed outcome.** There were 9,221 passed, 8 skipped and 1 xfailed: the base's
9,189, 8 and 1, with A9's 32 new cases, all passing. The 60 slow tests it can reach all pass
(§A.5).

### A.1 The branch and the merges

| Commit | What | Files |
|---|---|---|
| `14a0b5a` | A9: three gun decks in the quarter bill and the gun deck's words | `freesail/crew/quarters.py`, `freesail/orders/gunnery.py`, `tests/test_three_decks.py` (new) |
| `eb018d1` | `git merge --no-edit origin/…/pkg-90` at 6c29d1d (nudge 87 and its documents) | `docs/design/DesignProposal.md`, `CarriedForward-M7.md`, `M7-WorkPackages.md`, `ShipsNudge.md`; no conflict |
| this report | the commit that adds this file, the branch's head | `docs/design/Report-Package90-Concepcion.md` |

- The merge brought documents only. `git diff 93cf624c 6c29d1d -- freesail tests data tools client`
  is empty, so A9's code stands on 93cf624c's.
- No rebase and no force. No branch but this one was pushed to. The authors are left as the cloud
  gives them, and there is no trailer.
- The package's branch has since moved to a027600 (ef5a9dd and a027600: the tartane's live preview,
  its pictures and two lines of the decisions). Those are documents only and are not merged into
  A9's hash: they come in with her file's hash.

### A.2 What A9 changes, by file

**`freesail/crew/quarters.py`** (its two readers, as plan §6 names them):
- `_shut_crews` takes the crews of a `middle` deck behind shut ports as it takes the lower's:
  `_SHUT_DECKS = (LOWER, MIDDLE)`.
- `_rob_order` ranks:
  - the shut crews first (0), whatever their deck;
  - then the upper works (1);
  - then the middle deck (2);
  - then the lower deck, last (3).

  Before A9 the lower deck ranked 2. A two-decker has no rank-2 crew, so her order is crew for
  crew what it was. `tests/test_three_decks.py` holds it against the old function, copied into the
  test, on the 74 and the 64 at 8, 12.5, 30 and 40 degrees of heel.
- The docstrings of `_deck_lines` and `_decks_words` say that the beat names a middle deck between
  the lower and the upper. Their code reads the decks from the file as it did.

**`freesail/orders/gunnery.py`** (the gun deck's words):
- On a ship with broadside guns on a `middle` deck:
  - "the second deck" (or "second-deck") names the middle deck;
  - "the third deck" names the upper;
  - "the middle deck" names the middle, as any deck named by its own word does.
- On any other ship, "second" and "third" name no gun, and the refusal is the old generic one.
- On a three-decker, "the main deck" is refused (§13.1 item 7, ruled the lean). The refusal reads:
  "She has three gun decks, the lower deck, the middle deck and the upper deck, and 'the main deck'
  names none of them: name the deck, as 'fire the middle deck' (or 'the second deck'; 'the third
  deck' is the upper)."
- On a two-decker, "the main deck" names the upper deck's guns as before.
- The words are read by the deck readers that every phrase goes through: `_deck_of_word` in
  `_guns_of_a_deck` and `_number_on_a_deck`. So "No. 3 gun of the second deck" and "the third
  deck's No. 3" work, and are refused in the same places, on the same ships.

### A.3 Today's nineteen files unmoved: old beside new (nudge 87)

One script, run with each tree first on `sys.path`, recorded for every committed ship file:
- **her beat to quarters**: the order's whole reply, and `quarters_of(ship).describe()` 30
  ticks after;
- **her robbing** at 8, 12.5, 20, 30 and 40 degrees of heel, engaged to starboard, with the ports
  updated by the engine's own rule:
  - the shut crews;
  - the robbing order at each of the three `first` values;
  - `lend(60)`'s count and words;
- **the gunnery words**: `guns_named` and `_fire_words` of 26 phrases. Among them are "the lower
  deck", "the middle deck", "the main deck", "the second deck", "the third deck", "No. 3 gun of
  the second deck", "the third deck's No. 3", "the gun deck", "the quarterdeck guns" and "the
  poop";
- **a passage at quarters** off Brest, 49.5 N 5.5 W:
  - cast loose and engage a mark four cables on the starboard beam;
  - nine fire orders, among them "fire the second deck", "fire the third deck", "fire the main
    deck", "fire the starboard main deck" and "fire No. 3 gun of the second deck";
  - then `tack ship` at quarters and 900 ticks more, with every log line and her end state
    recorded;
- **a passage under sail**, in truth 7-136's world: close-hauled on the starboard tack, her guns
  ready and run out, sail before guns, a tack, then "fire the starboard main deck" and "fire the
  second deck". Every log line and her end state were recorded.

Before was the tree at 6c29d1d's code (`/home/user/FreeSail`, code the same as 93cf624c's); after
was the branch at A9. **The two records are equal, file for file and line for line.** That covers
19 files, two passages each and 2,517 log lines, with no file crashing in either. On the 74, for
example:
- "fire the second deck" is refused as before: "'the second deck' names no gun of hers";
- "the main deck" names her fourteen upper-deck guns a side as before.

### A.4 Its tests: `tests/test_three_decks.py`, 32 cases, all passing

The tests run on stage 0's probe (`rig_fixtures.three_decker_probe_doc()`, written with
`write_ship`). The probe is the 74's file with her upper deck renamed `middle`, a new `upper` deck
over it carrying copies of her upper-deck guns, and a company of 839: scratch figures, not the
*Concepción*'s. They hold:
- No committed file has a broadside gun on a middle deck (her file, later, alone).
- The beat names the lower, the middle and the upper deck, each with its crews and men, from below.
- Heeled 35 degrees, the middle deck's crews behind shut ports are robbed with the lower's.
- The robbing order at 12.5 and 35 degrees, word for word.
- A two-decker's robbing is as before, against the old function: the 74 and the 64 at four heels.
- Her deck words on the probe: lower, middle, upper, second, third, with each side and the bare
  deck.
- On a two-decker, the second and third deck name no gun, and the main deck names her upper.
- On the probe, "fire the second deck" gives "The starboard second-deck guns to fire each as soon
  as it is ready, 14 guns.", and "the main deck" is refused with the exact text above.
- On the 74, "fire the second deck" gets the old generic refusal, and "fire the main deck" fires.

### A.5 The tiers on `eb018d1`

**The base: the fast tier whole on 6c29d1d**, the merged tree. Its code is 93cf624c's, so it
also stands as the brief's base on 93cf624c. It ran from the root with `python -m pytest -n 3 -p
no:cacheprovider -o addopts="--dist loadgroup" --junitxml=...`, in four shards of the test files
taken in turn, each with its own junit:
- 9,198 tests: 9,189 passed, 8 skipped, 1 xfailed;
- **none failed and none errored.**

My first two attempts at a base were not used: one was cut by the session's 30-minute limit on a
background command, and one by a restart of the container at its memory limit.

**A9: the fast tier whole on `eb018d1`**, the same way, with the junit compared test by test
against the base's:
- 9,230 tests: 9,221 passed, 8 skipped, 1 xfailed;
- **no test changed outcome, and none of the base's is missing;**
- the 32 found only on A9 are `tests/test_three_decks.py`'s, all passed.

On A9's tree the shards ran on one, one, two and three workers, to use a spare core beside the
base's last shard. The new file moves the files' turn by one, so the shards' counts differ from the
base's, but not the whole. No harbour or browser test failed in either run.

**The slow tests A9 can reach, on `eb018d1`**, with `--slow -m "slow and not pace"`, one process
each:
- **the slow tests of the 24 files that beat to quarters, fire or read the quarter bill**
  (`tests/test_bellerophon.py`, `test_bilander.py`, `test_bill_by_fit.py`,
  `test_bill_marines_and_flag.py`, `test_captive.py`, `test_company_moved.py`, `test_diana.py`,
  `test_dumb_show.py`, `test_far_action.py`, `test_far_last_list.py`, `test_fight.py`,
  `test_filling.py`, `test_flags.py`, `test_health.py`, `test_held_work.py`,
  `test_indefatigable.py`, `test_lee_ports.py`, `test_neufchatel.py`, `test_pivot_gun.py`,
  `test_practice.py`, `test_practice_orders.py`, `test_stand_by_words_and_action_flow.py`,
  `test_subtypes.py`, `test_three_decks.py`): **46 passed.** By file:

  | file | passed |
  |---|---|
  | `test_bellerophon.py` | 21 |
  | `test_far_action.py` | 12 |
  | `test_flags.py` | 4 |
  | `test_bilander.py` | 2 |
  | `test_captive.py` | 2 |
  | `test_subtypes.py` | 2 |
  | `test_company_moved.py` | 1 |
  | `test_far_last_list.py` | 1 |
  | `test_neufchatel.py` | 1 |

  The other fifteen files have no slow test.
- **the slow truths of `tests/test_known_truths.py` that fight, fire or tack at quarters:**
  7-133, 7-135, 7-136, 7-137, 7-148, 7-149, 7-161, 7-191, 7-231, 7-352, 7-353, 7-358, 7-368 and
  7-450. **14 passed.**

A9 reaches neither the captain's files nor the runner's, nor a passage in a rising gale, so nudge
87 does not ask for `tests/test_mends_126.py --slow` on this hash. It is run with her file's
hash.

**The form:**
- `git diff 93cf624c eb018d1 | tr -cd '\r' | wc -c` is 0;
- `ruff check` and `ruff format --check` are clean on A9's three files;
- no Python line is over 100 characters;
- no name of a model or its maker is in the commit's message or its files. The commit's author is
  as the cloud gives it.

### A.6 For the lead

- **A9's hash, `eb018d1`, is ready to merge on its own.** It moves nothing committed, and no pin.
- No question is open on A9. The questions on her file come with her hash.

## 2026-11-28: her file, her tests and her truths, and A9's mend: `8cf2c05`

**In short.** Her module, `tools/ships/concepcion.py`, writes `data/ships/three-decker.yaml`
through the generator. The other nineteen files come out byte for byte: her generator was run whole
into scratch, and every file of `data/ships` was compared with `cmp`. Also on the branch:
- her people file, `data/people/three-decker.yaml`, with `names: spanish`;
- her description row and words;
- `tests/test_concepcion.py`, with her five truths, 7-735 to 7-739.

The nine guards her file moves are recorded old beside new in `docs/dev/TuningNotes.md`, under
"Package 90, the Purísima Concepción".

Her figures are as ruled:
- her hull is PB-039's at rung S, unscaled, on her line as traced;
- her mass is 4,440 t, with Winfield's 5,167 t recorded beside it;
- her decks, ports, rudder, lateral plane, stern lights and masts' places are as measured;
- her rig is the 74's by Steel's rule, scaled 1.15;
- she has two fits on one hull, 1797 the default.

`check_viewer_guns` is clean on both fits.

Two of her design's figures are tuned, old beside new: **`clr_x_m` 5.7 to 6.3, and her rudder's
greatest angle 35 to 25 degrees.** With them her tack is no quicker than the 74's from any of
truth 10's headings: 258, 276 and 293 s against 237, 243 and 258.

**Luce's five to ten minutes is not reached by any setting that holds her helm: the band is the
lead's** (§B.4).

**A9's mend (nudge 94, the lead's reader) is on this hash** (§B.0). On a file with guns on a
middle deck and not on all three gun decks:
- "the main deck" is refused naming the gun decks the file gives;
- the beat says a line a deck wherever the crews stand on two gun decks or more.

Her words and every committed file's are as they were, and two new cases pin it.

**I stop on four matters in files that are not mine, and hold one row.** None of the four is in
my row, so I have not touched them. What each needs is in §B.7:
- **the viewer's `tests/test_view_geometry.py`**: fifteen of its cases fail on her file. Thirteen
  want her rows in its per-file tables, and two are the viewer's drawing rules meeting a
  three-decker's spacing;
- **the ranges audit's known list, `tools/range/audit-known.yaml`**: her default fit of 1797 is
  sailed on days from 1792, as the *Diana*'s of 1810 was. Three tests fail for that one finding,
  truth 7-590 among them. Her entry is written out, in the *Diana*'s form, for the lead;
- **"a first rate"**, which her design's §8.2 gives her words: four tests of
  `tests/test_ships.py`, `tests/test_world_orders.py` and `tests/test_bellerophon.py` use it as
  their example of words that name no description. Package 75 chose it when "a ship of the line"
  became the 74's;
- **the engine track's `tests/test_yard_level.py`**: its table of every file's yard levels wants
  her row, which is written out.

Four more counts that grow by her file showed only on this hash's tier, in older guards that no
builder of package 90 owns: the fits with their own trimmers, the fits with their own marines, the
files whose bills keep the marines, and the files numbered by deck. Their rows are written out and
held for the next hash (§B.7 item 11).

**Her fast tier whole on `8cf2c05`**, compared test by test with its base:
- 9,339 tests: 9,305 passed, 8 skipped, 1 xfailed, **25 failed**;
- every one of the 25 is named in §B.7;
- no other test changed outcome.

Her own 55 cases, in `tests/test_concepcion.py` and `tests/test_three_decks.py`, all pass. The
slow tier of her files, pace excepted, has 244 passed, 8 xfailed (the file's own) and 3 failed.
The 3 are the ranges audit's one finding (§B.7 item 8). `tests/test_mends_126.py --slow` passes
all 31.

### B.0 A9's mend: true of whatever gun decks a file gives (nudge 94)

The lead's reader found, on A9 as merged, a file that loads with guns on a middle deck and not on
all three gun decks. That file was told "She has three gun decks" and then only the decks that
carry guns, with a stray comma when there was one. Its beat said no deck's line, because
`_deck_lines` wanted both a lower and an upper deck. The loader is not in my row, so I have made
the sentences true of whatever a file gives, in A9's two files:
- **`orders/gunnery.py`, `_the_main_deck_of_three`:**
  - with guns on all three gun decks, her words as before;
  - with guns on two, "She has guns on two gun decks, the middle deck and the upper deck, and 'the
    main deck' names neither of them: name the deck, as 'fire the middle deck' (or 'the second
    deck'; 'the third deck' is the upper).";
  - with guns on one, "She has guns on one gun deck, the middle deck, and 'the main deck' does not
    name it: name the deck, as 'fire the middle deck' (or 'the second deck').".

  The third deck's word is given only where she has upper-deck guns.
- **`crew/quarters.py`, `_deck_lines`:** a line a deck wherever the crews stand on two gun decks or
  more of the lower, the middle and the upper (`_GUN_DECKS`). Before, the lower and the upper were
  both wanted. With no middle deck the two rules are one, so every committed file's beat is as it
  was. A file with guns on its middle deck alone says no deck's line, as a frigate's one gun deck
  does not.
- **The pins,** two new cases in `tests/test_three_decks.py`. Each uses stage 0's probe with some
  decks' guns taken away (its magazine and shot left with the calibres kept, which the loader
  wants), and holds its beat and its refusal, old beside new in their docstrings:
  - without its lower deck's guns;
  - with its middle deck's guns alone.
- **The nineteen files, again:** §A.3's script was run on this hash's tree. Its record of the
  nineteen committed files equals the record taken before A9, file for file and line for line:
  their beat, robbing, gunnery words and two passages each, 2,517 log lines, none crashing. Her
  own file, the twentieth, gives her three-deck words.

### B.1 The branch and the merges

| Commit | What | Files |
|---|---|---|
| `1df8bb5` | her module and her file by the generator, her people file, her rows, her tests and truths, and the pins her file moves | `tools/ships/concepcion.py`, `data/ships/three-decker.yaml`, `data/people/three-decker.yaml`, `freesail/world/ships.py`, `tests/test_concepcion.py`, `tests/test_profile.py`, `tests/test_probes_90.py`, `tests/test_schooner_mast.py`, `tests/test_diana.py`, `tests/test_lee_ports.py`, `tests/test_known_truths.py`, `tests/test_magazine.py`, `tests/test_neufchatel.py`, `docs/dev/TuningNotes.md` |
| `f041758` | A9's report section (pushed first, alone) | `docs/design/Report-Package90-Concepcion.md` |
| `a12c9d4` | her commit merged onto A9's report | no conflict |
| `d4f9d19` | `origin/…/pkg-90` merged at 55d2dda: the tartane's live previews, their pictures and the owner's notes (ef5a9dd, a027600, 55d2dda) | documents and pictures only; no conflict |
| `3fdde4f` | `origin/…/pkg-90` merged at 157f870: the trunk with A9 as merged (8947874), nudges 88 to 94 and the carried list | documents only beyond A9; no conflict |
| `8cf2c05` | A9's mend, nudge 94 (§B.0) | `freesail/orders/gunnery.py`, `freesail/crew/quarters.py`, `tests/test_three_decks.py`, `docs/dev/TuningNotes.md` |
| this report's section | the commit that adds it, the branch's head | `docs/design/Report-Package90-Concepcion.md` |

- Her commit was made on A9's hash and held unpushed until A9's section was pushed, so that A9 went
  to the lead alone.
- No rebase and no force. The authors are as the cloud gives them, and there is no trailer.
- **Her base is A9's tier on `eb018d1` (§A.5).** `git diff eb018d1 157f870 -- freesail tests data
  tools client` is empty: the package's branch at 157f870 carries A9's code and documents beyond
  it. No test reads the documents it adds; I looked for each by name. So A9's fast tier whole is
  the fast tier of her merged tree without her file, and her tier is compared with it test by
  test.
- `d4f9d19` was tiered in part before nudge 94 came: its first two shards. Those runs found the
  three tests of "a first rate" (§B.7 item 9). The rest of that run was stopped for this hash.
- A9's merge `eb018d1` carries git's default message, which names the branches in full. My later
  merges are worded without them, as the *Diana*'s are.
- **The package's branch has moved since this hash, to 8a95cb6,** with the viewer's V1 and V2 as
  merged (`cfc1032`): `client/projection.js` and 1,139 lines of `tests/test_view_geometry.py`. That
  is code, so it is not merged into this hash, which is the one tiered as nudge 94 asked, at
  157f870. The next hash takes it, with a base on that tree.
  - On a scratch merge, not pushed, her file's viewer cases on the viewer's new code fail the same
    fifteen as item 1, and 39 pass.
  - That merge conflicts in `docs/dev/TuningNotes.md` alone, the viewer's sections and hers at
    its end. The next hash keeps both whole.
- No scenario, and no shelf line (the card's "Does not build").

### B.2 The basics

#### B.2.1 Her particulars against their sources

| Figure | Filed | Source |
|---|---|---|
| length on her line | 61.26 m | PB-039, the post's after face to the stem's fore face on her line as traced (Pages §5.1, measured); Winfield's rebuilt eslora 61.30 m within 0.1% (ruling 3) |
| breadth | 16.54 m | James (Con-D §2) |
| draught | 7.94 m to K at the middle of her line | her line as traced: 8.02 m at the post's after face, 7.94 at the middle, 7.65 at the stem's fore face (Pages; the lead's ruling) |
| `deck_height_m` | 5.99 m | the 74's method: the mean of PB-039's pair of red lines, 0.055 m under Pages' upper line (the generator: 5.995 at the middle) |
| displacement | 4,440 t | her drawn body outside the plank, the ruled range 4,421 to 4,473 t; Winfield's 5,167 t in her record beside it |
| ports | lower 16 (the sixteenth empty), middle 16, upper 16 a side | ZAZ0100 and PB-039 (Pages §11.3, measured); the sixteenth lower pair cut at Cádiz in 1791 and unarmed (VR-Sp §4) |
| the lee port | the midship lower port, No. 8 at x +0.18, dips at 13.19 deg | 13.3 on L0 (Pages §5.2); 13.2 on her line as traced |
| rudder | 13.3 m2 over a span of 8.29 m | PB-039 (measured) |
| lateral plane | 473.5 m2 | PB-039 (measured) |
| masts' places | fore x +23.37, main −3.47, mizen −18.94, upright | PB-039 (measured) |
| her rig | the 74's chain by Steel's rule, lengths x 1.15, areas x 1.3225; plain sail 2,947 m2 | Con-D §4; the 74's module copied, not imported |
| GM | 1.5 m | JUDGEMENT (Con-D §2: no more heel than the 74); close-hauled in 15 kn she heels 3.1 deg, the 74 3.6 |
| her fits | 1797: 112 pieces, 1,188 libras; 1809: 116 pieces, 1,508 libras | her own record by deck (Con-D §5); weights Con-D §5.3's interim figures; `pounder: 36` as her navy named it |
| company | 877, of whom 225 soldiers (168 infantry, 57 infantry-artillery); 21 posts in her people file | the regulation of 1 January 1788 (Winfield et al. 2023, p. 1446 ff.: VR-Sp §15); her own 839 (pp. 406-410: VR-Sp §4) in her note beside it, four per cent under |

**The mass her file floats her at is 4,440 t** (`displacement_kg` 4,440,000). It is her body as
drawn on PB-039, outside the plank, at her load line as traced, by the lead's ruling, in its range
of 4,421 to 4,473 t (the plank's thickness JUDGEMENT). Winfield's 5,167 t is recorded beside it in
her notes, and `check_hull` holds the range. Every other figure is reckoned to the same line: her
draught of 7.94 m, her breadth at the water and her lateral area. Her GM, 1.5 m, is her design's
judgement and not reckoned from the line.

The generator reports her hull as drawn by `freesail/ship/form.py`:
- 4,643 t, 5% over the filed 4,440 t;
- 7.02 m deep at the greatest section, against the file's draught of 7.94 m.

Each of her 47 measured port triples is within 0.05 m of the drawn side. Every port of her three
tiers stands on that side, at +0.00 m.

#### B.2.2 Her polar beside the 74's

`world.ships.polar_of`, best speed in knots by the true wind's angle off the bow. The closest angle
is 50 deg for both ships, and at 40 deg both make 0.0:

| wind | ship | 50 | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 140 | 150 | 180 | best |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 kn | *Concepción* | 0.99 | 2.21 | 3.26 | 4.08 | **4.53** | 4.45 | 4.39 | 4.27 | 3.83 | 3.57 | 3.09 | 4.53 at 90 |
| 8 kn | the 74 | 0.94 | 2.17 | 3.22 | 4.04 | **4.50** | 4.46 | 4.40 | 4.27 | 3.78 | 3.55 | 3.14 | 4.50 at 90 |
| 15 kn | *Concepción* | 1.85 | 4.14 | 6.05 | 7.43 | **8.02** | 7.94 | 7.86 | 7.67 | 6.98 | 6.56 | 5.74 | 8.02 at 90 |
| 15 kn | the 74 | 1.76 | 4.06 | 5.95 | 7.30 | **7.87** | 7.83 | 7.75 | 7.51 | 6.83 | 6.48 | 5.80 | 7.87 at 90 |
| 25 kn | *Concepción* | 3.08 | 6.79 | 9.52 | 11.05 | 11.38 | **11.41** | 11.37 | 11.18 | 10.47 | 10.05 | 9.04 | 11.41 at 100 |
| 25 kn | the 74 | 2.93 | 6.64 | 9.25 | 10.67 | 10.98 | **11.03** | 10.99 | 10.75 | 10.09 | 9.77 | 8.99 | 11.03 at 100 |

In 15 kn the frigate-36's best is 8.19 kn.

In 15 and 25 kn she is a little faster than the 74 from 50 to 160 deg off the wind. In 8 kn the
two are within 0.05 kn of each other at every angle. The sources call her a fast first rate
(Brenton via Winfield; James vol. 6 pp. 3-4). In 15 kn her best stands between the 74's and the
frigate's (truth 7-738).

#### B.2.3 Tack, wear and heave-to at seed 7

The truths' own helpers were used (`close_hauled_on_starboard`, `until`), in 15 kn unless said:

| | *Concepción* | the 74 |
|---|---|---|
| tack from 290 / 292.5 / 295 deg | 258 / 276 / 293 s | 237 / 243 / 258 s |
| ... her way going in | 5.47 / 5.00 / 4.51 kn | 5.38 / 4.92 / 4.43 kn |
| ... ground gained to windward | 159 / 136 / 111 m | 105 / 95 / 69 m |
| tack from 292.5 in 8 kn | missed stays, 2.7 kn going in | missed stays, 2.6 kn |
| ... in 12 kn | 349 s | 220 s |
| ... in 20 kn | 266 s | 312 s |
| ... in 25 kn | 280 s | 265 s |
| wear (truth 11's form) | 503 s, 376 m to leeward | 499 s, 241 m |
| heave to (truth 12's form), 600 s after 300 | under 1.31 kn, 55.3 to 63.6 deg off | under 1.18 kn, 56.5 to 63.4 deg off |

### B.3 The work particular to her

#### B.3.1 Beat to quarters by three decks

In her default fit, 1797, the beat says:

> Beat to quarters! Quarters: 56 gun crews manned, the trimmers 15, the helm 4, the powder 42, the
> marines 225. The lower deck: 15 gun crews, 210 men. The middle deck: 16 gun crews, 176 men. The
> upper deck: 16 gun crews, 112 men. The quarterdeck: six gun crews, 36 men. The forecastle: three
> gun crews, 18 men. The guns are secured: 'cast loose the guns' to serve them.

In the 1809 fit, with its own bill:

> Beat to quarters! Quarters: 58 gun crews manned, the trimmers 13, the helm 4, the powder 42, the
> marines 197. The lower deck: 15 gun crews, 210 men. The middle deck: 16 gun crews, 176 men. The
> upper deck: 16 gun crews, 144 men. The quarterdeck: five gun crews, 24 men. The forecastle: three
> gun crews, 16 men. The poop: three gun crews, 12 men. ...

Engaged to starboard, the gun deck's words are A9's on her file:
- "fire the starboard middle deck" gives "The starboard middle-deck guns to fire each as soon as
  it is ready, 16 guns." These are her sixteen 24-pounders.
- "fire the second deck" fires the same deck.
- "fire the third deck" fires her upper deck's sixteen 12-pounders (18-pounders in 1809).
- "fire No. 3 gun of the second deck" gives "No. 3 starboard gun of the middle deck to fire as
  soon as ready."
- A bare "fire No. 3 gun" is refused, naming her five decks.
- "fire the main deck" is refused with A9's words naming her three gun decks.

Each is held by truth 7-736.

#### B.3.2 The robbing

Engaged to starboard and heeled by hand, each fit, `lend(60)`:

| heel | shut crews | lend(60), 1797 |
|---|---|---|
| 11.0 deg | none | 66 men, from the upper deck, Nos. 11 to 16, and the quarterdeck, Nos. 3 to 6 |
| 11.6 deg | 4, lower | 63, from the lower deck, Nos. 6 to 9, their ports shut, and the upper deck, No. 16 gun |
| 12.5 deg | 7, lower | 70, from the lower deck, Nos. 7 to 11, their ports shut |
| 20 deg | 14, lower | 70, from the lower deck, Nos. 11 to 15, their ports shut |
| 35 deg | 20, lower and middle | 70, from the lower deck, Nos. 11 to 15, their ports shut |

In 1809 the upper works come first in the same way: at 11.0 deg, 60 men from the upper deck, Nos.
13 to 16, the poop, Nos. 1 to 3, and the quarterdeck, Nos. 4 to 6. From 11.6 deg the same shut
crews as 1797 come first.

At 35 deg five of her lee middle ports are shut. "fire the starboard middle deck" then says:
"eleven guns; five are behind ports the sea has shut."

#### B.3.3 The lee ports by deck (truth 7-737)

| tier | lowest lee port shuts by the engine's rule (`shot.lee_port_shut`, the sill within a foot of the water) |
|---|---|
| lower | 11.33 deg, at the midship port (the 74's lowest, 10.35); six of her lee lower tier within the next degree |
| middle | 33.7 deg |
| upper | 65.4 deg |

The design's dip, the sill over its half-breadth, is 13.19 deg at the midship lower port. On her
battery she is open at 11.0 deg. At 11.6 deg her lee lower tier amidships is shut and said once:
"The lee lower-deck ports are shut, the sea at their sills." Her middle tier is still open there.
Her row is in truth 7-190's table (`tests/test_lee_ports.py`).

#### B.3.4 Her tack against the 74's

It is set out in §B.2.3 and §B.4. In 15 kn she is slower than the 74 from every heading, and inside
600 s.

#### B.3.5 Three of her crewed at the pace floor (truth 7-739)

This is written in the 74's 7-196 form, with her file in the 74's place. It is marked `pace`, so
it goes to the pace run on the build machine. **Its local run is left to the coordinating session,
as the brief says,** and its figure is to be recorded in the truth's docstring then. The engine
note's three-decker probe made 72 to 75 ticks a second (Eng §7). I have not run it.

### B.4 Her tack: what was tried, and her band

The brief asks for a tack "no quicker than the 74's and inside Luce's five to ten minutes". The
levers are her helm's lead (`clr_x_m`), her rudder's greatest angle and its rate.

All three were swept on scratch copies of her file, from truth 10's three headings in 15 kn. The
table is in TuningNotes. In short:
- **The rate hardly matters.** At 3, 2 and 1.5 deg/s she tacks in 210, 214 and 217 s from 290.
- **The lead slows her, but it is bounded by truth 17's form.** At 7.0 m and above she is taken
  aback getting under way from rest. At 7.7 m she tacks in 304 to 335 s, but is aback. At 6.3 m
  she gets under way with a margin: 62.9 deg off at the nearest, settled in 391 s. That is the
  74's 4.8 m chosen the same way (59.6 deg and 451 s), and her helm there is near the 74's at
  each heading of truth 6.
- **The angle slows her.** At 25 deg she tacks in 258, 276 and 293 s, each slower than the 74's.
  At 23 deg she misses stays in 12 kn, and at 22 and 20 deg she misses stays from 295 deg.

So no setting that holds her helm brings her tack to 300 s from every heading. **Her filed
setting, 6.3 m and 25 deg, meets "no quicker than the 74's" and not Luce's band: the band is the
lead's.**

The cause is the engine's: its tack does not slow with a ship's size or mass (Con-D §9, §19). Her
rudder, 13.3 m2 against the 74's 9.82, turns her quicker, and her mass, 4,440 t, does not slow her.
Con-D §9 measured the same on 4,200 and 5,167 t.

Truth 7-738 holds what she does: each tack no quicker than the 74's and inside 600 s. It is written
as a state, with the band's gap said plainly in its docstring.

### B.5 What was taken as judgement

Her module marks 136 notes JUDGEMENT. These are the ones that bear on what she does:
- **her lines:**
  - the body plan read as moulded, her plank in her mass and not on her lines;
  - aft of about x −8 m, her water stands up to 0.14 m under L0, and the water's half-breadth
    there is L0's. The after sections were not read again at that height (Pages §12.1, to do).
- **her stern** (its board ZAZ0101's, not read): the knuckle 0.82 m over the lower deck, the
  transom's shares and round-up the 74's, and the taffrail as measured.
- **her head and stem head:** the upper deck plus 1.23 m on the 74's rake, and the 74's knee
  scaled.
- **the sixteenth lower port's sill:** her lower tier's sheer carried aft. Its half-breadth is
  the drawn side's, by the *Diana*'s nudge-59 road.
- **the upper works' places:**
  - the forecastle's three a side over the upper tier's three foremost ports;
  - the poop's places over the rail;
  - sills 1 ft over the deck;
  - the rail 1.0 m over each deck.
- **GM 1.5 m** (her design's); her plank's thickness.
- **her fits:** the obuses on the ports nearest the ends (Con-D §3), and the 1809 fit's bill, its
  obuses taking soldiers first.
- **her company:** the 60 idlers by trade; her ratings at 0.33, 0.22 and 0.45; the helm 4.
- **her ground tackle:** the 74's anchors scaled by her rig's area, x 1.32; the bower cable
  Steel's largest, 24 in; the stream cable x 1.15. Steel's 100-gun row is garbled in the OCR and is
  to be read on the page image. Her boats are the 74's six with a second launch.
- **tuned:** `clr_x_m` 6.3 and the rudder's 25 deg (§B.4).

### B.6 The truths written and those waiting

| Truth | What it holds | State on this hash |
|---|---|---|
| 7-735 | her particulars against their sources: length, breadth, three tiers of sixteen, both fits' pieces and libras, the regulation's company, her mass in the ruled range and Winfield's figure in her record | written, passing |
| 7-736 | three gun decks at quarters: the beat's decks in order, "fire the starboard middle deck" her sixteen 24-pounders, a bare number refused naming her decks, "the main deck" refused naming her three | written, passing |
| 7-737 | her lower ports shut at the heel her plan gives: dip 13.0 to 13.5 deg, the engine's threshold 11.2 to 11.45 deg, the middle tier 33.5 to 34.0, the upper 65 to 66; open at 11.0 and shut at 11.6, said once | written, passing |
| 7-738 | a fast first rate: best in 15 kn between the 74's and the frigate's; each tack no quicker than the 74's and inside 600 s; wear in 360 to 720 s; hove to under 1.6 kn, 45 to 65 deg off | written, passing |
| 7-739 | three of her crewed hold the crewed floor, 60 ticks a second | written; **its run is the coordinating session's**, on the build machine |

Each truth is written as states, with no digest. None is xfailed, skipped or loosened.

### B.7 Stops and open questions, for the lead

1. **Stop: the viewer's `tests/test_view_geometry.py`, fifteen cases on her file.** The file is the
   viewer's (§7.1), and neither my row nor the card names it for me, so I have not edited it.
   - **Thirteen want her row in the viewer's per-file tables.** Each fails with a `KeyError` on
     her path, or because she is named in no table where she should be:
     - the bowsprit's `BOWSPRIT_DRAWN` and `LEVEL_ROOT_M`;
     - the galleries' two files, the frigate-36 and the 74: she has galleries and lights too;
     - `TIERS_IN_THE_SIDE`, served;
     - the bulkheads' ends, served, where she has (roundhouse, fore), (quarterdeck, fore) and
       (forecastle, aft) against no row;
     - `NO_BOOM`, the bilander's and the lugger's set, for the gaff sail's test and the boom's: her
       mizen course has no boom;
     - `LINES_ON_THE_RAIL`, both sides, the "no profile" case both sides, and "as the game serves
       her";
     - `STEM_TACKED`, `STEM_TACK_Z_M`, `TACK_OFF_HER_SIDE_M` and `TACK_UP_HER_STAY`, both sides.

     These are the counts that grow by a file. The *Diana*'s were ruled the same way (nudge 32).
   - **Two are the viewer's drawing rules meeting her spacing.** I measured both and found no
     fault in her data:
     - *A lower mast's foot sorted behind the near side*, on the quarter, for her main mast: her
       upper deck's strip at the mast sorts at −2.519 against the foot's −2.454.
       - The viewer sorts a deck strip at its middle, with a fixed 0.5 m bias behind
         (`DECK_BEHIND_M`), and her strips run between her ports' stations, 1.76 m apart.
       - Her main mast stands 0.08 m aft of the station at x −3.39, so the strip's middle is 0.8 m
         aft of the mast. On the quarter that is 0.57 m of depth, over the bias by 0.066.
       - A station added at her mast would hide the rule, not mend it, so I left it.
     - *A band follows the drawn side between its two heights*, at her lower tier's after end:
       the band's after corner at x −28.775 is 0.244 m off the side.
       - Her sixteenth lower port at x −28.27 is her aftmost station, and its band runs half a
         port's width, 0.505 m, aft of it.
       - The side there is the viewer's closure to her stern, which stands at x −30.69 at that
         height, so the port is well inside her hull.
       - The test allows a hair off "beside a closure", and this one is 0.244 m.
       - Once the band is mended, this test wants her row in `CHORD_OFF_THE_SIDE_M` too.
   - Pictures are the coordinating session's. A cloud session has no browser, and I have taken
     none.
2. **The 1809 fit's company.** The 1809 fit stands on her one file with the 1797 company of 877.
   The 1803 regulation's 1,015, of whom 275 soldiers, is recorded in the fit's note as a
   departure, as the brief rules. Its own bill holds 197 soldiers in their division and 13
   trimmers, its obuses taking 28 soldiers first. **I judge a second file is not wanted.** Every
   crew of the 1809 fit is manned from the 877, so nothing of the fit fails for the smaller
   company. A second file would only carry 138 more men. That is the lead's.
3. **Her tack's band** (§B.4): Luce's five to ten minutes is not reached. The band is the lead's.
4. **The engine's rule that marines serve no long gun** leaves no crew of hers empty. It does take
   her trimmers: 15 in 1797, where the 74's share of her seamen would be 75, and 13 in 1809. That
   is few hands to trim a first rate's sail at quarters. For the lead, with the quarter bill.
5. **The relieving tackles' hands** (the lead's ruling 8): eight are proposed, a first rate's
   heavier tiller against the frigate's six. A ship file's `timing:` carries an evolution's timing
   and not its crew, so the number is not filed. It stands in her module as
   `TACKLES_HANDS_PROPOSED` for the lead.
6. **Her drawn body** displaces 4,643 t, 5% over the filed 4,440, and is 7.02 m deep at the
   greatest section against the filed 7.94 m. The filed figures are the ruled ones, and the drawn
   hull is the viewer's and the generator's check. I record the gap, as the *Diana*'s report did
   (her §2.5), and have not chased its cause.
7. **Her after sections** were not read again at her water's height aft of x −8 m (§B.5). It is a
   to-do of Pages §12.1, worth 0.14 m at most.
8. **Stop: the ranges audit's known list, `tools/range/audit-known.yaml`.** The file is not in my
   row, so I have not edited it. Three tests fail on her tree for one finding:
   - `tests/test_range_audit.py::test_the_sampled_sweep_is_the_known_list`;
   - `tests/test_range_audit.py::test_the_full_sweep_is_the_known_list_exactly`;
   - truth 7-590, `test_truth_7_590_the_ranges_audit_by_the_readers_road_is_its_known_list`.

   The finding is `v-fit-ahead:three-decker:concepcion 1797`: "a three-decker sails the fit
   'concepcion 1797' on days before 1797 (a scenario may name her); 1792-1796; 1". It is the
   *Diana*'s case, whose entry the lead ruled filed (nudge 32; `4dec517`). The same entry in her
   form would clear it:
   ```yaml
   - key: v-fit-ahead:three-decker:concepcion 1797
     what: a three-decker sails the fit 'concepcion 1797' on days before 1797 (a scenario may name her)
     years: 1792-1796
     basis: mechanical
     owner: a data fault for milestone 7c
     reason: the description's default fit is of a later year than the day (package 90, the
       Concepción; her file's other fit, of 1809, is later still). An earlier fit, or an earlier
       class, for that description clears it by today's readers; a fit chosen by the day would want
       a reader first (u-ships)
     most: 1
   ```
   An earlier fit of hers would clear it too. She was launched in December 1779, but her two fits
   are the owner's Dec 8, so I have added none. The run's other 62 tests pass on her tree. That run
   was `tests/test_range_audit.py` and the range truths of `tests/test_known_truths.py`, with
   `--slow`.

9. **Stop: "a first rate" in her words, and four tests that use it as no description's words.**
   Her design gives "a first rate" and "a first-rate" to her description (Con-D §8.2: "'a first
   rate' names her description in a scenario's words"). I filed them, with "first rate" and
   "first-rate". Four tests in files that are not mine use the words as their example of words
   that name no description. Package 75 chose them when "a ship of the line" became the 74's, old
   beside new in each:
   - `tests/test_ships.py::test_the_descriptions_name_the_four_files_and_the_brigs_two_come_from_her_file`:
     `description_key("a first rate") is None` now reads `'three-decker'`;
   - `tests/test_ships.py::test_a_goal_makes_a_plan_and_a_goal_the_captain_does_not_know_is_refused_in_words`:
     `put(w, "first rate", ...)` is no longer refused for "no description";
   - `tests/test_bellerophon.py::test_her_description_names_her_file_and_ranks_her_a_ship_of_the_line`:
     its list of words that name no description holds "a first rate";
   - `tests/test_world_orders.py::test_each_channel_is_carried_out_in_words_and_a_bad_one_refused_in_words`:
     'ship: a first rate "Victory" of Britain at the Iroise, bound for Brest' is now carried out,
     "a three-decker, sixteen ports a tier 'Victory' of Britain put on the sea, bound for Brest
     (her plan crosses the land on the leg to Brest)", where the test wants it refused.

   **Two ways, the lead's:**
   - (a) each test takes another example that names no file, old beside new, as package 75 did.
     "A bomb vessel" is one the game lacks.
   - (b) her words lose the four first-rate forms, against her design's §8.2.

   I would take (a), since her design rules the words. A first rate in a scenario's words is a
   three-decker, and the description sails her file. That a British first rate such as the
   *Victory* would then sail a Spanish ship's file is the scenarios' package's, as Con-D §8.1
   leaves it.

10. **Stop: the engine track's `tests/test_yard_level.py`, `COMMITTED_YARD_LEVELS`.** It wants a row
    for every committed file, and two tests fail without hers. The file is the engine track's new
    file (§7.1), and the *Diana*'s row went in at nudge 58's word (`ff5bfc0`), so I have not edited
    it. Her row, read off her file with `ship.yard_level`, has fourteen yards, the 74's at the 74's
    levels:
    ```python
    "three-decker": {
        "fore.yard": 0, "fore.topsail.yard": 1, "fore.topgallant.yard": 2, "fore.royal.yard": 3,
        "main.yard": 0, "main.topsail.yard": 1, "main.topgallant.yard": 2, "main.royal.yard": 3,
        "mizzen.topsail.yard": 1, "mizzen.topgallant.yard": 2, "mizzen.royal.yard": 3,
        "mizzen.crossjack.yard": 0, "spritsail.yard": -1, "sprit_topsail.yard": -1,
    },
    ```
11. **Held for the next hash: four more tables that count her file, in older guards no builder of
    package 90 owns.** They are the same kind of count as the five I moved (§B.8), but they showed
    only on this hash's tier, after the hash was made. Four cases fail for want of her rows:
    | table | file | her row, read off her file | failing case |
    |---|---|---|---|
    | `FIT_TRIMMERS`, the fits that give their own trimmers (old: the razee's 'as razeed 1795' alone) | `tests/test_bill_by_fit.py` | `"three-decker.yaml": {"concepcion 1809": {"forecastle": 2, "fore_top": 3, "main_top": 4, "mizzen_top": 2, "afterguard": 2}}` | `test_a_fit_gives_its_own_trimmers_only_where_ruled_and_pickles_as_before_without[three-decker]` |
    | `FIT_MARINES`, the fits that give their own marines (old: the 64's and the razee's) | `tests/test_bill_marines_and_flag.py` | `"three-decker.yaml": {"concepcion 1809": 197}` | `test_a_fit_gives_its_own_marines_only_where_ruled_and_pickles_as_before_without[three-decker]` |
    | `KEYED_FILES`, the files whose bills keep the marines in their division (old: the 74's, the 64's and the razee's) | `tests/test_bill_marines_and_flag.py` | `"three-decker.yaml"`; her bill keeps 225, and she carries no flag party | `test_no_file_carries_either_key_and_each_pickles_as_before[three-decker]` |
    | `NUMBERED_BY_DECK`, the files whose guns are numbered by deck (old: the 74 and the 64) | `tests/test_bellerophon.py` | her file, `numbering: by deck` | `test_only_the_two_deckers_carry_the_numbering_key_and_every_other_gun_is_as_it_was` |

    Rather than re-tier this hash for four rows, I hold them, unless the lead wants them sooner,
    for the hash that the lead's rulings on items 1, 8, 9 and 10 will want anyway. Each would go in
    old beside new in TuningNotes, as the others did.

### B.8 The pins her file moves

Each is recorded old beside new in `docs/dev/TuningNotes.md`, "Package 90, the Purísima
Concepción", and each is a count or table that grows by her file. The brief names these four:
- `tests/test_schooner_mast.py`: the guard reads twenty files (old nineteen), and its name with it.
- `tests/test_lee_ports.py`, truth 7-190's table by file: her row (old: no row).
- `tests/test_known_truths.py`, truth 7-190's count of armed files: eleven (old ten).
- `tests/test_diana.py`, the doubled-article guard over every file: twenty files (old nineteen).

The other five are the same kind of count, each moved the *Diana*'s way in the same place. I name
them so that a reader can pass or return them:
- `tests/test_known_truths.py`, truth 7-700's `_MUSTERED_AFTER_119`: her muster, 398 and 398 (old:
  the *Diana*'s alone).
- `tests/test_profile.py`, `MODULE_FILES`: `ships.concepcion` writes `three-decker.yaml` (old: none,
  a stub).
- `tests/test_probes_90.py`, `FILLED`: `("diana", "concepcion")` (old: the *Diana*'s alone).
- `tests/test_magazine.py`: the foreign calibres, her long 36 and her obús of 48, beside the
  *Diana*'s three (old: the three).
- `tests/test_neufchatel.py`, `ROLE_BY_INTENT`: her row, a King's ship's at every intent's kind as
  the 74's, and her file's first role (old: no row).

`tests/test_subtypes.py`'s rows and the harbour's list needed no move: both pass with her file. No
figure of another ship moved, and each table's other rows read as before.

### B.9 The test sets, against the base

**The base** is A9's fast tier whole on `eb018d1` (§A.5): 9,230 tests, 9,221 passed, 8 skipped, 1
xfailed, none failed. Its code is the merged tree's (§B.1).

**Her hash: the fast tier whole on `8cf2c05`**, from the root with `python -m pytest -n 3 -p
no:cacheprovider -o addopts="--dist loadgroup" --junitxml=...`, in four shards of the test files
taken in turn, each with its own junit. It was compared test by test with the base's junit:
- **9,339 tests: 9,305 passed, 8 skipped, 1 xfailed, 25 failed.**
- **Six of the base's tests changed outcome, passed to failed.** All six are named in §B.7:
  - three of "a first rate" (item 9): `test_ships.py`'s two and `test_world_orders.py`'s one;
  - `test_bellerophon.py`'s "a first rate" case (item 9);
  - `test_bellerophon.py`'s files numbered by deck (item 11);
  - `test_yard_level.py`'s table of every file (item 10).
- **One of the base's tests is missing:** `test_schooner_mast.py`'s
  `test_the_guard_reads_nineteen_files_...`, renamed `..._twenty_files_...` with its pin (§B.8). It
  passes under its new name.
- **110 tests are found only on her hash**, her file's cases among every file's, and her own tests.
  - 91 passed. Among them:
    - her own 21 fast cases and the mend's 2 new cases in `tests/test_three_decks.py`;
    - `tests/test_check_viewer_guns.py` on her file;
    - truth 7-190's row of hers;
    - 38 of the viewer's cases on her file;
    - `test_view_action.py`'s 6.
  - 19 failed, each named in §B.7:
    - the viewer's 15 (item 1);
    - `test_yard_level.py`'s row of hers (item 10);
    - the three of her fits' own bill (item 11).
- No other test changed outcome, and none errored. No harbour or browser test failed.

The same tier on `d4f9d19`, before nudge 94's mend, was stopped after two shards. Those shards
gave the same outcomes, test for test, as this hash's first two.

**The slow tier of her files on `8cf2c05`**, with `--slow -m "slow and not pace"`, in two runs:
- **her files and the guards they move, but the known truths:** `tests/test_concepcion.py`,
  `test_three_decks.py`, `test_lee_ports.py`, `test_diana.py`, `test_neufchatel.py`,
  `test_magazine.py`, `test_probes_90.py`, `test_profile.py`, `test_schooner_mast.py`,
  `test_range_audit.py`, `test_mends_126.py` (nudge 87), `test_subtypes.py` and
  `test_harbour.py`. Four workers; a first run on one worker hit its two-hour limit and is not
  used. **48: 46 passed, 2 failed.** By file:
  | file | passed | failed |
  |---|---|---|
  | `test_mends_126.py` | 31 | 0 |
  | `test_range_audit.py` | 9 | 2 |
  | `test_harbour.py` | 3 | 0 |
  | `test_subtypes.py` | 2 | 0 |
  | `test_neufchatel.py` | 1 | 0 |

  The two failures are the audit's sampled and full sweeps against its known list, the one
  finding of §B.7 item 8. The other eight files have no slow test.
- **the slow truths of `tests/test_known_truths.py`**, four workers. **207: 198 passed, 8 xfailed,
  1 failed.**
  - The one failure is truth 7-590, the ranges audit by the readers' road: the known list's one
    finding (§B.7 item 8).
  - The 8 xfailed are the file's own marks, which my changes to it do not touch (`git diff eb018d1
    8cf2c05 -- tests/test_known_truths.py` names no xfail). They are the frigate's bowlines
    sweep four times, her lying a-try, her plain sail, truth 11 and truth 7b-100's old case.

Her pace truth, 7-739, is the coordinating session's to run on the build machine, and it is not
in either run.

Nothing of hers reaches the captain's files or the runner's. `tests/test_mends_126.py` is run with
`--slow` all the same, as nudge 87 asks of a passage in a rising gale. Its result is in the first
run above.

**The form on `8cf2c05`:**
- `git diff 93cf624c 8cf2c05 | tr -cd '\r' | wc -c` is 0;
- `ruff check` and `ruff format --check` are clean on every Python file the branch changes;
- no Python line is over 100 characters;
- no name of a model or its maker is in a commit's message or in a file;
- "she" for ships, and they/them for persons, but for three comments in her module. At lines 528,
  2274 and 2275 they say "his" of Steel and Falconer. They are comments, so her file does not move
  for them, and they are held for the next hash with item 11's rows. Her file's notes also say
  "his" in three places that come from the generator's shared text (`tools/gen_ships.py`'s water
  line) and the 74's sail notes. The 74's file says the same, and those are not mine;
- nothing is under `docs/agents/consent/`.

**The step's end on `8cf2c05`:**
- `python tools/gen_ships.py <scratch>` wrote twenty files, each `cmp`-equal to the committed file;
- only her file differs from the package's `data/ships` at 157f870;
- `load_ship` on her file loads 112 guns in her default fit;
- `tools/check_viewer_guns.py` on her file is clean.
