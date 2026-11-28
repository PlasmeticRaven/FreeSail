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
