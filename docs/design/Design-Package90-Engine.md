# Design note: the engine for package 90 (November 2026; second draft)

Package 90's preliminary work, the engine's part (the lead's note of 2026-11-18 at 00:50 UTC,
nudge 15; `docs/dev/M7-WorkPackages.md`, row 90). It does two things. It reports item 37 of the
ships session's list of 79, the generator's own copy of the sail-force law, as the lead asked
(what it is read for, what would move if it were the engine's, what reads those figures, what I
would do), without changing it. And it sets down what the engine does **today** with each thing
the five hulls ask of it (the tartane, the polacre, the xebec, the corvette *Diana* and the
*Purísima Concepción* class three-decker), each run in scratch and not guessed, with what the
build would want. **This is the second draft (2026-11-18)**, by the plan's form
(`Plan-ShipsWorkflow.md`): it answers the critic's reading of the first ("How this draft answers
the critic", after the brief), takes the settlements of package 90's plan
(`docs/design/Plan-Package90.md` §4) and, as the plan asks of it (its §3, Phase 2), sets down the
engine's steps by the plan's names, A0 to A9 with the viewer's V1 to V4, as **one design for the
lead's approval before stage 0L** (§14), as `Design-ShipsEngineExtensions.md` was before package
75's stage 0E.

Nothing is built here. No code, no ship file, no generator change, no test, nothing the suite
reads: this note is a new document, with the package's other new documents the only change to the
tree.

## 0. Marks, probes, the tree

**The marks**, as `Research-ShipsEngine-2026-10.md` uses them: **read** (the code or the page at
the place cited), **observed** (seen in a run), **measured** (a figure from a run), and
**judgement** (reasoning, mine unless said). A JUDGEMENT that a file or a design would carry is
written so.

**The tree** is package 90's branch at 68e769ef (the trunk at nudge 15). Every line cited is that
tree's.

**The probes** were run with `py` from scratch folders outside the repository, the worktree first
on `sys.path` and `freesail.__file__` asserted under it; no tracked file changed (`git status`
clean but for the new documents), the only things written in the worktree being Python's bytecode
caches, which git ignores (later probes run with `PYTHONDONTWRITEBYTECODE=1`). Every speed in knots
in §2 and §4 is the ship's speed, `dyn.speed`, the measure truth 12 reads (`knots()`,
`tests/test_known_truths.py:120-121`). The rigs in
memory were made from the committed files by the lead's helpers in `tests/rig_fixtures.py`
(imported, not changed): the lead's `tartane_probe` and `polacre_probe` (made for classing and
never sailed; sailed here in scratch to see what the engine does with them), and two made the same
way for this note, a **xebec probe** (the polacre probe with her square main replaced by a third
whole lateen on a 19 m yard, 150 m², scratch figures) and a **three-decker probe** (the 74's file
with her upper deck renamed `middle`, a new `upper` deck and her upper works raised 2.3 m, each
fit's upper-deck guns copied onto the new deck, her stations scaled to a company of 839: scratch
figures, not the *Concepción*'s). The harness is the settee tests' (`tests/test_settee.py`,
`_world`): `make_world` at seed 7, a steady northerly, no gusts, the ship on the starboard tack
67.5° off the wind, plain sail set, trimmed every two minutes after the first five, settled 1,800
s, then the order and 900 s. Item 37's measure ran on a copy of `tools/` in scratch (§1.3), and
its suites against the scratch files by a read redirect in scratch (§1.4). The probes' scripts and
their outputs are kept with the session's scratch, not in the repository.

## In brief

| Need | What the engine does today (measured unless marked) | What the build wants |
|---|---|---|
| Item 37, `PEAK_COEFF["studding"]` | 1.25 where the engine's curve peaks at 1.4396 at 35°; read by the rating pass alone, for the studding-sail booms and the ringtail booms. Made the engine's: **74 figures in 9 of the 18 files move**, every one a studding-sail boom's or a ringtail boom's `rating_kn`, up 15 per cent; nothing else in any file | The generator reading the engine's curves (§1.5). In both tiers on the moved files: truth 35's last clause and `test_studding`'s frigate brought up to six points move (no boom carries away), five records of "no figure moved" name the booms, seven byte pins hold again by the regeneration; truth 9 and truth 14 hold. For the owner, before any new file is generated |
| Whole lateens worn and dipped (B3.1) | No dip: the schema refuses `dipping` on any sail but a lug. The tartane, the polacre and the xebec probes **tack** in 89, 164 and 101 s, the lateens swung over as gaff sails with no word, drawing alike on both tacks (5.07 and 5.02 kN, the polacre's fore lateen); a wear says nothing of them | The plan's A1 (§14): `dipping` allowed on a whole lateen for its side and its loss against the mast; a new `change_lateen` evolution on the settee's model; "worn, not tacked" where the main is a whole lateen; the lateen mizen worked as a ship's mizen and kept set hove to; the words (§2) |
| A square topsail over a lateen (the tartane) | Classed as the cutter is, by B3.4's rule as the lead read it: her main her one mast with yards, the topsail her head yard, no after yards, not square-rigged; hove to with it aback **on the probe, whose topsail stands on the cutter's topmast**; on her design's pole main (the yard on the lower mast's head) the topsail is a course today and is hauled up hove to (Tar-D §5.1a) | Nothing new for the classing; A5 and A6 for her topsail on a pole main (§14); her *tréou* for her document; her boat in tow, which no boat's entry can say today (§3) |
| The pole mast (the polacre) | No such thing in the engine: every square sail is furled aloft by topmen; her main topsail yard put on the lower mast classes as the probe does | The pole known to the square sails' take-in and furl, the topmast evolutions and the viewer, read from the parts as filed (the polacre's design's reading); item 8 settled in her document (§4) |
| Sweeps | A ship's file may carry a boat's `oars:`, and is then a boat to the game (no bells, "a boat under oars, with no rig to draw"); `give way` mans every oar at once from nobody (the probe's 121 men untouched), no evolution, no time; 20 oars at a boat's figures move the xebec probe 1.6 kn in a calm | Sweeps of a ship's own, apart from a boat's oars; as a fit; an evolution drawing the men from the company; men to a sweep; the guns' crews against the oars (§5) |
| Three gun decks | The probe loads, names, beats to quarters by deck, fires by deck, shuts its lee ports by deck and passes the viewer's check. Two readers of the quarter bill single out the lower deck (the crews behind shut ports, the order the crews are robbed in); the clearing time stops at the frigate's; the viewer says "a lower port", "a middle port"; a first rate has no words or rank | The few two-deck places generalised; her words, her rank, her bill by deck (§6) |
| A first rate's company and the pace | In truth 7-196's world three 74s crewed run 79 to 81 ticks a second, three three-decker probes of 839 run 72 to 75, the floor 60; alone, 514 and 487 | Nothing of its own: the cap and the floor serve her (§7) |
| The regency's cruiser | A role is a book of `data/captains/` with `thresholds:`; package 116 put the prize doctrine's thirteen keys there and read seven | A `corsair` (or `regency`) book on the cruiser's and the privateer's form (§8) |
| The harbour's shelves | Every ship file is offered for a bare start; a scenario on no shelf goes to "Not yet sorted" and fails `tests/test_harbour.py:131` | A shelf line for each new scenario (§9) |
| The wheel and the tackles | Every hull, the tiller-steered cutter and tartane among them, says "the wheel is shot away", rigs the tackles "to the tiller" and repairs "the wheel" with "new wheel-ropes" | A hull's helm read from her file, a tiller's words (§10) |
| Package 81's viewer checklist | The xebec probe and the three-decker probe pass `tools/check_viewer_guns.py`; a whole lateen is drawn as a four-sided sail under its yard, or as a lug | Each hull's ports and decks to the checklist; the whole lateen drawn as its own; the obús is no gun kind (§11, §6.3) |

## How this draft answers the critic

| Finding | What the first draft said | This draft |
|---|---|---|
| F7: the lateen mizen | §2.3 item 5: the mizen "read by the driver's paths ... handled hove to by the driver rule" | **Held.** Restated as the plan's §4 row 4 settles it on the polacre's measure: hauled aft as she comes to (and at helm's a-lee on a square main), eased at "up helm", kept set hove to, never read by the driver rule (§2.3 item 5, §14 A1) |
| F3: the tartane's topsail | §3: she "heaves to with the topsail aback" | **Held.** So on the probe, whose topsail yard is on the cutter's topmast; on her own design's pole main the topsail is a course to the engine and is hauled up (the critic's run, re-run for the tartane's second draft: Tar-D §5.1a). A5 and A6 come before her file (§3, §14) |
| F25: "nothing in the tree written" | §0 | **Held.** Reworded: no tracked file changed; Python's git-ignored bytecode caches were written by the probes (§0) |
| F22 (with the plan): the far body's pace | §5 named no file for it | `world/ships.py`'s far pace (`VESSEL_MIN_SPEED_KN`, l. 98, read at l. 849 and 865) is A7's (§14; Plan §7.1) |
| The plan's settlements | the dip's key or the settee's machinery, "the lead's choice"; the Spanish pound "the English pounds" | the plan's proposal for A1 (§2.3 item 1, §14); the Spanish pound the owner's, the pick the nominal pounder (§6.3; Plan §4 row 8, Dec 9) |

---

## 1. Item 37: the generator's copy of the sail-force law

### 1.1 What it is

`tools/gen_ships.py:134-140` (read):

```
# The engine's force coefficient at the peak of each class's curve (data/sail_classes.yaml,
# |(C_L, C_D)| at the best angle). Package 10: if the curves change, change these and rerun.
PEAK_COEFF = {"square": 1.23, "studding": 1.25, "gaff": 1.29, "jibheaded": 1.32, "lug": 1.29}
...
PEAK_COEFF["lateen"] = 1.25
```

The engine's own peaks, from its curves as it reads them (`freesail.physics.sails.SAIL_CLASSES`,
`_interp` sampled every 0.01° from 0 to 90°; measured):

| Class | The engine's peak of \|(C_L, C_D)\| | at | `PEAK_COEFF` |
|---|---|---|---|
| square | 1.2265 | 40° | 1.23 |
| gaff | 1.2903 | 30° | 1.29 |
| jibheaded | 1.3220 | 28° | 1.32 |
| lug | 1.2851 | 35° | 1.29 |
| lateen | 1.2462 | 35° | 1.25 |
| sprit | 1.2000 | 90° (the drag alone) | none (a KeyError at the rating pass, `map-engine.md` §4) |
| **studding** | **1.4396** | **35°** (1.35 and 0.50) | **1.25** |

Five agree to the second place; the studding class is 13 per cent short. The cold review's
evidence traces the drift to one table of package 10 (`docs/dev/TuningNotes.md` l. 131, the
studding peak raised to 1.35 for truth 14, and l. 142, `PEAK_COEFF` set to 1.25 in the same
table; `docs/reviews/ColdReview-M7-evidence/records-04-tuning-notes.md`, row 1b). The other
copies of the law the generator keeps agree today: `RHO_AIR` 1.225 and `KNOT` 0.514444
(`gen_ships.py:396-397`; `freesail/units.py:26, 33`), and the shear `(h / 10) ** 0.11`
(`gen_ships.py:444`; `freesail/physics/wind.py:123-124`) (read).

### 1.2 What it is read for

Read, in order:

1. `PEAK_COEFF` is read in one place, `static_kn` (`gen_ships.py:439-446`): the static force of a
   list of (area, centre height, class) sails at a design wind, each sail at its class's peak
   coefficient, with the engine's shear.
2. `design_kn` (449-451) is `static_kn` times `SUSTAINED_FRACTION` (0.85), returned as a
   `DesignLoad` carrying its design wind. A ship's script calls it for every rated spar, naming the
   sails it thinks the spar carries; for a studding-sail boom and a ringtail boom the script names
   the boom's own sail as class `"studding"` at `DESIGN_WIND_KN["studding"]`, 18 kn ("light spars,
   fair-weather sails", 161).
3. `Builder.rate_spars` (1421-1511), **the rating pass**, loads the document through the engine's
   own loader and re-rates every `DesignLoad` spar from every sail whose spar chain the engine
   hangs on it, at the spar's design wind, times 0.85, at least 1 kN. **Studding sails are counted
   only on a spar of class `studdingsail_boom`** (1468-1471): a yard or a mast never carries its
   studding sail's load in the rating. A spar the graph loads nothing on keeps the script's own
   `DesignLoad` (1497-1503). So the studding entry reaches the files in two ways: the studding-sail
   booms and the ringtail booms by the pass, and any boom whose fallback is the script's figure.
4. The `rating_kn` so written is the strain model's yardstick (`freesail/physics/strain.py:1-20,
   94-100`): the load over the rating; above 1.0 the spar wears and the log is warned, above 1.5
   it may carry away at any substep (`0.002 × (ratio − 1.5)²`), and it goes for certain when its
   condition reaches nought.

What it means at sea (arithmetic on the rating, not sailed; judgement on the reading): a boom is
rated for its sail at the peak coefficient in 18 kn, times 0.85. Its sail at the engine's real
peak loads it 1.44 / (1.25 × 0.85) = 1.355 times its rating in that wind, so at the curve's peak
the boom begins to strain at 15.5 kn and may carry away from 18.9 kn. With the engine's 1.44 the
same boom strains from 16.6 kn and may carry away from 20.3 kn. Before the wind the studding
sail works at its drag of 1.25 at 90° and the gap closes; it is widest on the quarter and the
beam, where the sail is near its peak.

### 1.3 What moves if it is made the engine's (measured)

The method: `tools/` copied whole to a scratch tree with `data/` (all but `data/charts/`, which
the generator does not read); the copy's generator run into a scratch folder by a runner that
imports `freesail` from the worktree (asserted) and the copy's `gen_ships.py` and `ships/` after
it; every output compared with `data/ships/` byte for byte, and then parsed and compared figure
by figure (every leaf of every document, lists by `id`).

- **The baseline:** the copy unchanged writes all eighteen files **byte for byte** as committed.
- **`PEAK_COEFF["studding"]` = 1.44**, everything else as it is: **nine files change, nine do
  not.** In the nine, **74 figures move, every one a `rating_kn`**: 70 of studding-sail booms and
  four of ringtail booms (the frigate's, the razee's and the two schooners'), each up by the ratio
  1.44 / 1.25 (15 per cent; 9 to 18 per cent as the tenths round). The byte diffs also carry each
  boom's comment line, "Rating: ... in 18 kn -> N kN.", where the file has one (the hermaphrodite
  brig's booms have none). Nothing else changes: no other spar, no line, no sail, no figure of the
  hull, the crew or the guns.
- **The unrounded 1.4396** gives the same eighteen files as 1.44, byte for byte.
- **Unchanged:** `bilander`, `cutter`, `lugger`, `smack` and the five boats (no studding sails).

| File | Figures | The booms, old → new (kN) |
|---|---|---|
| `frigate-36` | 11 | fore lower 4.2 → 4.9, fore topmast 5.6 → 6.4, fore topgallant 1.8 → 2.1, main topmast 7.0 → 8.1, main topgallant 2.3 → 2.6 (each a pair); ringtail 4.0 → 4.6 |
| `razee-44` | 11 | fore lower 6.0 → 6.9, fore topmast 7.9 → 9.0, fore topgallant 2.7 → 3.2, main topmast 9.4 → 10.9, main topgallant 3.4 → 3.9 (pairs); ringtail 3.7 → 4.2 |
| `sixty-four` | 10 | fore lower 6.1 → 7.0, fore topmast 8.0 → 9.2, fore topgallant 2.8 → 3.2, main topmast 9.5 → 11.0, main topgallant 3.4 → 4.0 (pairs) |
| `seventy-four` | 10 | fore lower 8.4 → 9.7, fore topmast 10.9 → 12.5, fore topgallant 3.9 → 4.5, main topmast 15.0 → 17.3, main topgallant 4.9 → 5.7 (pairs) |
| `brig`, `merchant-brig` | 10 each | fore lower 2.1 → 2.4, fore topmast 2.9 → 3.3, fore topgallant 1.1 → 1.2, main topmast 3.1 → 3.6, main topgallant 1.1 → 1.3 (pairs) |
| `hermaphrodite-brig` | 6 | fore lower 3.4 → 3.9, fore topmast 3.5 → 4.0, fore topgallant 1.3 → 1.5 (pairs) |
| `privateer-schooner`, `topsail-schooner` | 3 each | fore topmast 2.2 → 2.6 (a pair); ringtail 3.9 → 4.5 |

**The cause's mend, measured the same way:** the copy's generator computing its table from the
engine's curves (the greatest \|(C_L, C_D)\| over each class's tabulated points, which is the
curve's peak, the curves being piecewise linear and the norm convex along each piece), rounded to
two places as the table is now: the same eighteen files as 1.44, byte for byte, the sprit class
gaining its 1.20. **Unrounded**, it moves 208 figures in 13 files, 134 of them the rounding's dust
in every class (0.1 to 1.0 kN on masts, yards and bowsprits: the frigate's main mast 669.1 →
668.5); so the mend rounds, as the table's comment always meant.

### 1.4 What reads those figures (measured)

The files read through a redirect in scratch (`sitecustomize` on `PYTHONPATH`, answering every
read of `data/ships/<name>.yaml` from the scratch file of that name, the worktree first on the path
and `freesail` asserted under it, `-p no:cacheprovider`, nothing written to the tree), then the
tests failing there run again on the files as committed. First the studding sails' readers by
name (truths 9, 14, 35 and 7-185, the *Neufchatel*'s truth 9, `tests/test_studding.py` whole: 45
tests), then both tiers whole:

- **Truth 7-185** (`tests/test_known_truths.py:10765`), the generator run into a scratch folder and
  every file compared as text: fails on the moved files, as it must; it is the pin that the files
  are the generator's, and it holds again once the generator and the files move together.
- **Truth 35** (`tests/test_known_truths.py:1587-1633`): its last clause, "every boom whips on
  the first second of the blow and one carries away on the second, before the routine can fire",
  the main topmast boom first. With the booms at the engine's figure **no boom carries away** in
  the 121 s at 32 kn before "shorten sail for weather" takes the studding sails in; every clause
  before it holds. Passes on the committed files.
- **`tests/test_studding.py::test_brought_up_to_six_points_they_shake_strain_and_carry_away[frigate]`**:
  kept at six points for half an hour, her studding sails shivering and flogging, "no boom went".
  Passes on the committed files. (Its schooner case is an expected failure on both.)
- **Held with the moved files:** both of truth 9's (`test_truth_9_royals_and_topgallants_carry_away_in_thirty_five_knots`,
  the frigate and the schooner's `test_truth_9_nothing_carries_away_in_twenty_knots_under_plain_sail`),
  both of truth 14's, the *Neufchatel*'s truth 9 (`tests/test_neufchatel.py:1626`), and the other
  35 cases of `tests/test_studding.py` (its two schooner cases expected failures on both, "the
  schooner's setup in irons").
- **The fast tier whole** on the moved files (`-n 8`, 51 min): **13 failed, 8,337 passed**, 13
  skipped, 1 expected failure; the 13 run again on the committed files: all 13 pass. They are of
  three kinds:
  - **seven byte pins**, the files compared with what the tree's generator writes: truth 7-185;
    `tests/test_ship_particulars.py::test_generator_reproduces_the_committed_files`;
    `tests/test_profile.py::test_the_hook_runs_the_four_ships_modules_after_the_eight_each_writing_its_own`;
    `tests/test_neufchatel.py::test_the_generator_writes_her_file_as_committed_and_reports_its_checks`
    (the hermaphrodite brig's booms); and the generators' reports of the 74
    (`tests/test_bellerophon.py`), of the 64 and the razee (`tests/test_indefatigable.py`) and of
    the schooners (`tests/test_hull_schooner.py`). Each holds again when the generator and the
    files move together, by construction: the moved files are the moved generator's own output,
    byte for byte (§1.3);
  - **five figure pins against the record**, each file compared with git at a commit before its
    profile, every key but the drawing's equal: `test_no_figure_the_physics_or_the_gunnery_reads_moved`
    of the frigate (`tests/test_hull_frigate.py:499`), the brig and the merchant brig
    (`tests/test_hull_brig.py`), and `test_no_figure_the_physics_reads_moved` of the two schooners
    (`tests/test_hull_schooner.py`). These are the pinned figures that move: each would have the
    booms' ratings named in it, old beside new;
  - **one artefact of the probe**: `tests/test_replay.py::test_the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings`
    failed on its time limit (0.51 s against 0.5 s) under the redirect's extra work at every
    `open` and a loaded machine; it passes on the committed files.
- **The slow tier whole** on the moved files (`--slow -m "slow and not pace"`, `-n 8`, 54 min):
  **12 failed, 530 passed**, 14 skipped, 11 expected failures. Two are the change's: truth 35 and
  the frigate brought up to six points (above). The other ten fail on the committed files too,
  run again there with the same messages, digest for digest: this machine's, not the change's (the
  merchant passage's, the schooner's and the intent's constants, truths 77, 78 and 79 on the
  cruise, the captain's three trials' digests, among them `TRIAL_TRADE_THICK`'s de00808076d8cccf
  the notes already name for re-pinning on the build machine, and the harbour maker's refusal
  worded with the absolute path). The pace tests are not in it; they read no rating.

**Truth 9's strain**, as the lead asked: it is untouched by the change (its two clauses hold). Its
35-knot clause is the royals and topgallants carrying away under all sail, and the studding
booms are not what it counts on; its 20-knot clause sets plain sail, no studding sail. Package
10's `SUSTAINED_FRACTION` of 0.85 was measured on the topgallant yards (TuningNotes l. 142), not the
booms, and does not move.

### 1.5 What I would do (for the owner)

**The plain account.** The game rates each studding-sail boom for the wind it should stand in,
18 knots with its sail drawing its hardest. To do that sum, the ship-building script keeps its own
copy of how hard each kind of sail pulls, and its figure for a studding sail is about a seventh
lower than the figure the sailing itself uses. So every studding-sail boom in the game is rated a
seventh weaker than intended: with its sail drawing its hardest, a boom begins to strain at about
15½ knots where the rule meant 16½, and may carry away from about 19 knots where it meant 20. It
was a slip in one table in package 10, not a choice.

**What I would do:** mend the cause, not the number. The generator reads the engine's own curves
for its peaks (and its air density, knot and shear from the engine's modules), rounded to two
places as the table is, and a test holds the two together, which the cold review found missing
(`code-08-core-ship-physics.md` l. 329). Measured: only the studding-sail booms and the ringtail
booms move (74 figures in nine files, §1.3); the sprit class gains a peak; every other figure of
every file stays byte for byte.

**Where a pinned ship moves**, the owner's to rule:

1. **Truth 35's last clause**, the frigate before the wind in 32 knots: today a boom carries away
   in the first seconds of the blow, before the routine's two minutes can take the studding sails
   in; with the booms rated as intended, the routine takes them in first and nothing carries away.
   The truth's sentence was written to the old figure ("the routine's two minutes are long for
   studding sails before the wind in 32 knots"); I would re-measure it old beside new and keep the
   routine's firing, its count and its timing pinned as they are, the clause about the boom
   carrying away re-stated for the new figure (or moved to a stronger blow where a boom still
   goes before the routine).
2. **The frigate brought up to six points** (`tests/test_studding.py`): today her shivering
   studding sails carry a boom away within half an hour; with the booms as intended, none goes in
   the half hour. Re-measured: how long it takes now, or in what wind it happens in half an hour.
3. **The five records of no figure moved** (`tests/test_hull_frigate.py:499`, the brig's and the
   merchant brig's in `tests/test_hull_brig.py`, the two schooners' in `tests/test_hull_schooner.py`),
   each its file against git before its profile: the booms' ratings named in them as moved, old
   beside new, with this ruling as the reason.
4. **The seven byte pins** (truth 7-185 and its kin, §1.4): passed again by the regeneration
   itself, the files being the generator's.

Nothing else of either tier moves (measured, §1.4); truth 9 and truth 14 hold.

**The other ways**, for the owner's choice: (b) keep 1.25 and write it as a JUDGEMENT with a
reason (light booms rated below their sail on purpose, so that they whip and go first, which is
truth 35's story); or (c) lower the studding curve's peak to 1.25 instead, which moves every
polar with studding sails set and truth 14's "fifteen per cent on a broad reach" (not
recommended). **My pick: (a), the mend**, because the rule the table's comment states ("the
engine's force coefficient at the peak of each class's curve") is the right one and the drift is
a slip.

**Why it is settled before any new file** (the lead's word): of package 90's hulls the *Diana*
and the *Concepción* are ship-rigged and would carry studding sails; generated before the ruling,
both files would be generated again after it.

---

## 2. The lateens: worn, not tacked, the yard dipped round the mast (B3.1)

### 2.1 What the engine has

Read: a whole lateen is the `lateen` class, on a `lateen_yard` slung at its truss, with its own
curve (peak lift 1.15 at 35°), its sheet floor and its evolutions from package 75's B3.1
(`set_lateen`, `take_in_lateen`, `furl_lateen`, `reef_lateen`, `shake_out_lateen`,
`trim_lateen_sheet`; Ext §3.6 and §3.7). The yard is out of `is_yard` (`parts.py`; Ext §3.3), so
it is no braced yard: no brace order touches it and it makes no mast "a mast with yards". The
dip, the lug's going-about, keys on the sail's `dipping` and its class: `schema.py:2363-2364`
refuses `dipping` on any sail but a lug ("only a lug is dipped"); `dipping_lugs`,
`lugger_lugs` and `_lugs_all` take `cls == "lug" and dipping` (`evolutions/scripts.py:343-366,
8062-8072`); `LugDip` (486) works the dipping lugs of a manoeuvre; `against_the_mast`
(`physics/sails.py:673-680`) loses the cloth of a dipping sail on the weather side of its mast,
and is False for any sail without `dipping`. The settee came into the dip by the `settee` key
(B3.3, Ext §5.4); the 64's and the 74's mizen course, a lateen cut at the mast (`cut_at_mast`),
is not dipped and goes about as a ship's mizen, its curve the gaff's.

### 2.2 What it does with whole lateens today (measured)

Each rig from the starboard tack, 67.5° off a steady 15 kn northerly, settled under plain sail
(§0); the order given and 900 s run. The files they come from sailed in the same harness for the
comparison.

| Rig | Tack: done at | Tack: what is said of the lateens | Lateens drawing, before → after (kN, force) | Wear: done at | Heave to: lying at 900 s |
|---|---|---|---|---|---|
| Tartane probe (lateen main under a square topsail, lateen mizen) | 89 s | nothing | main 6.66 → 6.70, mizen 1.05 → 1.05 | 487 s | 54.5° off, 3.14 kn; "Hove to on the starboard tack, topsail to the mast" at 125 s |
| Polacre probe (fore and mizen lateens, square main) | 164 s | nothing | fore 5.07 → 5.02, mizen 2.08 → 2.06 | 464 s | 58.6° off, 1.65 kn; main topsail to the mast at 182 s |
| Xebec probe (three lateens) | 101 s | nothing | fore 5.13 → 5.14, main 6.49 → 6.50, mizen 2.10 → 2.10 | 254 s | 53.5° off, 2.89 kn; "under her fore-and-aft canvas" at 126 s |
| The cutter (as filed) | 106 s | | | 458 s | 46.9° off, 1.92 kn |
| The lugger (as filed) | 180 s, her lugs lowered and dipped | | | 171 s, dipped | 83.8° off, 1.65 kn |
| The brig (as filed) | 454 s | | | 474 s | 64.1° off, 1.38 kn |

(A wear with a braced yard waits for it to come round at the wear's brace rate, as B3.4's ruling
3 recorded, so the tartane's, the polacre's, the cutter's and the brig's take 458 to 487 s and the
xebec's, with no braced yard, 254 s. The xebec's research note sailed a probe of its own with no
head sail, `Research-Xebec-2026-11.md` §9: she tacks in 346 s, her leeway to 37° in stays, wears in
167 s and is refused the heave-to; this one keeps the brig's head sails, which carry her round in
101 s and give her heave-to a head sheet to windward. The two agree on what this section draws
from them: no dip, no word of the lateens, the lateens flipped over with nothing done at the
yards.)

What this shows:

1. **No lateen is dipped, lowered, peaked or changed.** Offered `dipping: true`, all three rigs are
   refused at load ("sail 'fore.lateen' is a lateen sail; only a lug is dipped").
2. **Every whole-lateen rig tacks**, faster than the lugger that dips, the lateens' sheets shifted
   over as a gaff sail's are. The tack's lines are a fore-and-after's ("Ready about. Helm's a-lee;
   ease off the head sheets.", "Draw jib; trim aft the head sheets.", "Tacked; braced up on the
   larboard tack"); the polacre's and the tartane's add "Let go and haul" for their square yards.
3. **No lateen loses anything on the tack where it would lie against its mast**: its force is
   the same within one per cent on both tacks (the table), since `against_the_mast` reads
   `dipping` alone.
4. **The wear** shifts the sheets over ("Wind aft. Shifted over the sheets; hauled out and braced
   up.") and says nothing of the lateens. Its first line, "Stand by to wear ship. Up helm; brace in
   the after yards." (`scripts.py:1987-1994`, said whatever the rig), is said by the xebec, which
   has no braced yard; the lugger as filed says the same (observed), and so does any rig with no
   after yards (read), so it is older than package 90 and of the kind the lead's (3) of 2026-11-07
   named for the dismasted rigs' words.
5. **Hove to**, the lateens keep drawing: the xebec forereaches at 2.9 kn and the tartane at 3.1 kn
   after a quarter of an hour, where the cutter lies at 1.9 and the lugger at 1.7. The heave-to's
   driver rule (`after_gaff_sails`) reaches none of the three rigs' lateens (each rig's list is
   empty), so a lateen mizen is kept as a fore-and-after's mizen hove to: item 8's first half, for
   the polacre's document.

### 2.3 What the build wants

By the package's brief, B3.1's handling: worn, not tacked; the yard dipped round the mast (the
Levant's *muder*, Lescallier 1791 p. 378 and Willaumez p. 406 as `Research-Bilander-2026-10.md`
§1.5 reads them: the yard topped up toward the mast's line, its heel passed abaft the mast, the
tack shifted to the new weather side, "so that on the other tack the sail is not pressed on the
mast"). The engine's parts of it, in the order I would build them:

1. **The dip for a lateen.** `dipping: true` allowed on the `lateen` class (`schema.py:2363`), the
   dip's machinery read from `dipping` and not from `cls == "lug"` (the places of §2.1 and the
   lug-keyed readers the settee's step listed, Ext §5.4, each read again for a lateen), with the
   lateen's own words and time: the yard not lowered to the deck as a lug's is, but peaked and
   passed round, the *muder*'s minutes the hull documents' JUDGEMENT from the sources. The settee's
   step (B3.3) is the precedent for the cost: one key, every path read for it, no committed file
   moving. The polacre's design (`Design-Ship-Polacre.md` §5) names the settee's own change
   machinery for the same act, nearer in its handling of a yard slung on a mast that carries other
   yards; the dip's key is the smaller change to the schema. One of the two is built once for the
   three hulls: the lead's choice. **The plan proposes both halves** (its §4 row 3): the dip's key
   for the side and the loss against the mast, and a new `change_lateen` evolution whose scripts
   take the settee's change as their model, for the act itself (§14, A1).
2. **The loss against the mast.** `against_the_mast` reading `dipping` would give a dipping
   lateen left on its weather side the lug's loss (it draws with two thirds of its cloth,
   `LUG_AGAINST_MAST_AREA`, `sails.py:126-135`, itself a judgement); whether a lateen's figure is
   the lug's is the hull documents' (judgement:
   Fincham p. 59, "more liable to be taken aback than the common lug", `VesselReferences-2026-10.md`
   §3.1).
3. **Worn, not tacked.** A rule of the rig, not of a file: a ship whose working canvas includes a
   dipping lateen goes about by wearing. Today the choice between a tack and a wear is package 45's
   (`data/vocabulary.yaml` l. 238-243: `put her about` wears when her sail is short or after she has
   missed stays, the log saying why); the lateen rig is one more reason to wear, said. What `tack
   ship` itself answers on such a rig is the owner's (§12, question 2).
4. **The wear's lateens.** In the wear the lateens dipped as she runs off, as the lugger's lugs are
   lowered and dipped in hers today ("Lowered the foresail and the mainsail to dip them" at 36 s,
   "Dipped ...; hoisted on the starboard side, to leeward of the masts" at 149 s, observed), the
   lateen's way and words.
5. **Heaving to, and the lateen mizen as a ship's mizen.** The period's way of lying to under
   lateens is the hulls' research (the *cape*); the engine's heave-to today forereaches them at
   three knots (§2.2, 5). **The lateen mizen is worked as a ship's mizen and is not read by the
   driver rule** (the plan's §4 row 4, on the polacre's measure): a whole lateen on the aftermost
   mast with a mast before it is hauled aft as she comes to in the wear (and at helm's a-lee where
   a square main tacks), eased at "up helm", and **kept set hove to**; `after_gaff_sails` never
   takes a whole lateen, and a guard over every file holds it. Taken in hove to, the polacre probe
   falls off past the beam and does not heave to at all (`Design-Ship-Polacre.md` §5.2), so the
   driver rule must not reach it. A hull that forereaches past truth 12's band is mended by her
   own file's lever (the tartane's great lateen's trim; the polacre's fore lateen's sheet),
   measured on her file. **Plainly:** the first draft had the mizen read by the driver's paths and
   "handled hove to by the driver rule"; the measure rules that out. One step (A1) serves the
   three hulls.
6. **The shift alone.** An order for a lateen left on the bad hand by a shift of wind, as `dip the
   foresail` is for a lug (the tartane's design, §5.4 item 5, `shift the mainsail`); refused in
   words on the good hand. Its word wants care: `shift` is already the sail room's ("shift the
   mainsail for the small mainsail", `Research-Xebec-2026-11.md` §9 item 7).
7. **The lateens' evolutions sized to the hull.** B3.1's `set_lateen`, `take_in_lateen`,
   `furl_lateen` and `reef_lateen` were sized for the 64's mizen course (Ext §3.6); a small
   company's great lateen calls all hands where the watch is too few (`too_few: all hands`,
   package 116's and the settee's road), so nothing waits for ever.
8. **The words.** "Brace in the after yards" left out where she has no after yards (the three
   probes, and the lugger, the cutter and the smack as filed), and the tack's "Tacked; braced up on
   the larboard tack" where she has no yard at all (the xebec): words only, moving those files'
   wear lines; the lead's to place, with the evolutions' owner or here.

**What it moves:** nothing of the eighteen files, none of which carries a whole lateen (the 64's
and the 74's mizen course is `cut_at_mast` and stays a ship's mizen): keyed on a dipping lateen,
the change is the settee's kind, byte for byte for the rest (judgement, to be measured at the
build as B3.3 was).

---

## 3. A square topsail over a lateen on one mast (the tartane), and B3.4's classing

**Today (measured, on the lead's probe, whose topsail yard stands on the cutter's topmast,
`on: main.topmast`):** the tartane probe classes exactly as the lead read her under B3.4's rule and
as `tests/test_schooner_mast.py:259` holds: masts with yards `[main.mast]`; head yards
`[topsail.yard]`; no after yards; the topsail the yard laid aback hove to; not square-rigged; no
driver; `on_schooner_mast` true of no part (her main is the foremost mast with a braced yard, the
lateen yard being no braced yard). She tacks in 89 s, swinging her topsail at "Let go and haul" at
23 s as a cutter swings hers; she heaves to with the topsail aback ("Hove to on the starboard tack,
topsail to the mast, helm a-lee") and forereaches at 3.1 kn, her two lateens drawing (§2.2).
**Her own design's main is a pole** (`Design-Ship-Tartane.md` §4.1: the topsail yard hoisted on the
lower mast's head, no topmast). With the probe's topsail yard so filed, the engine counts the
topsail a course (`scripts.lowest_square_sails`, `evolutions/scripts.py:860-868`): hove to she
hauls it up ("Hauled up the courses.") and lies "under her fore-and-aft canvas", 51.8° off at
3.29 kn at +600 s (the critic's run, re-run for her second draft: Tar-D §5.1a). Her classing is the
same either way; her handling is not, so A5 and A6 (§14) come before her file.

**B3.4's two limits** (the lead's note of 2026-11-06; the list of 79, item 8): a lower square-sail
yard on an after mast, and a pole main with its topsail yard on the lower mast, each still a brig
by the rule. Neither reaches the tartane: whether her topsail yard stands on a topmast or on the
lower mast's head, the main is her foremost mast with yards, and the rule reads only after masts.
Measured on the polacre (§4): with her main topsail yard's parent moved onto the lower mast, her
classing is the same, field for field.

**What the build wants:** nothing new for the classing. For her own document: the topsail's
handling on her short main (set flying or on a yard hoisted on the mast's head, Monleón's print
and the Roux-school watercolour, `VesselReferences-2026-11-Spanish.md` §1); her heave-to (§2.3, 5);
and her *tréou*, the square sail Lescallier says tartanes rig to run or in a wind too strong
(pp. 400-401, `VesselReferences-2026-10.md` §3.1): a sail of the sail room bent in the lateen's
place, the settee's and the driver's road (`in_place_of`), if her document takes it.

**Her boat in tow** (the brief: "the boat in tow"). Today a ship's boats are a list with no place:
a boat's entry takes `id`, `kind`, `name`, `length_ft`, `oars`, `crew`, `tons` and `file`
(`schema.BOAT_KEYS`), and one offered `towed: true` is refused at load ("boat #1 has 'towed',
which a boat does not take"; measured on the tartane probe). The only thing towed astern with a
drag is the trawl (`physics/integrate.py:126-130`, `gear_drag`); "the boats are out and towing
astern" at the clearing for action is words alone (`action_scripts.py:134`). For her document: the
boat's place (on deck or towed) as a key of the boat, read by the boat's orders (manned from
alongside, not hoisted out) and by the words; a towed boat's drag left out as small beside her
hull's at her speeds (JUDGEMENT, to be measured against the trawl's form if it is not).

---

## 4. The pole mast (the polacre): cross-reference

Item 8 of the list of 79 (the polacre's pole masts; her lateen mizen kept hove to as a
fore-and-after's and whether the heave-to's driver rule reaches it; a whole lateen hauled aft at
helm's a-lee by nothing; the schooner's-mast rule's limits for whichever file has a pole main
first) is the lead's for **the polacre's design document** (`Design-Ship-Polacre.md` §5, with
her research note, `Research-Polacre-2026-11.md`), which settles it with what the engine does run
and not guessed.
What this note measured, for that document to cite or measure again:

- **There is no pole mast in the engine** (read: no key, no class; `schema.py`, `graph.py`).
  Every square sail's furl is aloft by topmen (`data/evolutions/furl_square.yaml`, "Lay aloft and
  furl the {sail}", its step `aloft: true`); `strike_topmasts`, `send_down_topgallant_masts` and
  their kin assume a topmast to strike; the viewer draws a topmast's doubling and its cap.
- **A pole main, as the classing reads it** (the polacre probe with her main topsail yard's parent
  moved from the topmast to the lower mast, at its own height; her topmast and the mast's height
  left as they were, the classing reading only the yards' parents) loads, and classes field for
  field as the probe does: masts with yards `[main.mast]`, head yards `[main.yard,
  main.topsail.yard]`, no after yards, not square-rigged, no driver, nothing on a schooner's mast
  (measured). Her square main is her foremost mast with yards between two lateens, so B3.4's rule
  never reads it. A whole pole (one spar, no topmast, its stays and staysails re-led) was not
  built here; it is her document's to make and sail.
- **Her lateen mizen hove to** is kept drawing as a fore-and-after's mizen: `after_gaff_sails` is
  empty for her, so the driver rule does not reach it; she lies 58.6° off at 1.65 kn at 900 s, the
  main topsail to the mast (measured, §2.2): her speed by truth 12's measure, 0.05 kn over its
  1.6 kn. The polacre's second draft agrees (her headway is 1.49 kn: `Design-Ship-Polacre.md`
  §5.2).
- **At helm's a-lee nothing hauls a whole lateen aft** (the tack's lines for her, §2.2: "Ready
  about. Helm's a-lee; ease off the head sheets.", and no line of the lateens).

**What a pole mast would want of the engine** (judgement): the pole known to the square sails'
take-in and furl (the yard lowered to hand the sail), to the topmast evolutions (refused in words:
there is no topmast to strike), to the viewer (no top, no cap, no doubling), and, if the sources
give it, to the strain (Winfield's "a mast less able to stand a strong wind", pp. 1083-1084). My
first reading was a key on the mast with the sails handed from the deck. The polacre's design,
drafted beside this note (`Design-Ship-Polacre.md` §5.1), reads it better: **no key**, the pole
read from the parts as filed (a lower mast with braced yards above its lowest and no topmast), for
B3.4's own reason ("a file that forgets a key makes her a brig with no word said"), and the
furlers **on the yard below**, not on deck (Falconer; Steel p. 236). I take her reading; the lead
rules it in her document.

---

## 5. Sweeps

**Today (measured).** The oars are the boats' (package 82, item 4): an `oars:` section of a ship's
file (`schema.py:1638-1655`: a number, a pull on the blade at no way, a power and the hours that
halve a man's strength) read by `physics/oars.py` as a thrust along the axis,
`min(F_0, P / max(u, 0.3)) × manned × stroke × fatigue` (124-130), and worked by the boat's
orders (`orders/boat.py`: `give way`, `easy all`, `lie on your oars`, `out oars`, `boat your
oars`). The schema does not keep it to boats. The xebec probe given a boat's figures for twenty
oars (50 N, 60 W, four hours, one man an oar: scratch figures):

| Wind, sail | Way at 60 s / 300 s / 900 s / 1800 s |
|---|---|
| Calm, no sail | 0.27 / 1.10 / 1.60 / 1.58 kn |
| Calm, lateens set | 0.28 / 1.11 / 1.60 / 1.58 kn |
| 3 kn, lateens set | 0.52 / 1.23 / 1.57 / 1.54 kn |

- `give way` ships every oar and mans it at once ("Give way together: the full stroke."):
  `manned = number`, from nobody: her company of 121 is untouched, no hand is drawn from the watch
  or the bill, and no evolution or time stands between the order and the stroke.
- The men tire as a boat's crew do: half an hour's pulling is half an hour at the oars.
- A lateen drawing does not stop the stroke: only a set lug does (`_lug_drawing`, `boat.py:265`).
- A ship without `oars:` is told "this hull has no oars" and sent to her boat.
- **A file with `oars:` is a boat to the game**: `world.boats.is_boat` and
  `world.movement.is_boat_hull` are both "her file has oars" (`boats.py:97-100`,
  `movement.py:911-914`), true of the xebec given them and false of her without (measured); with
  them she struck no bell in an hour, where without she struck one bell and two (measured), and
  the readers that ask it read her as a ship's boat manned as a hull: the viewer's server would
  say "a boat under oars, with no rig to draw" (`ui/server.py:213`), the readings name a boat of
  her ship's (`api/readings.py:2727`), and the command, the knowledge and the movement readers
  treat her as a boat (read). The xebec's research note found the same with figures of its own
  (`Research-Xebec-2026-11.md` §9, item 8: no bell, the boat's tick and its swamping run on her).

**What the build wants** (judgement): **a ship's sweeps kept apart from a boat's oars**, so that
the boat predicates stay "a ship's boat" and a xebec with sweeps is still a ship (a key of their
own, or the boat predicates read from the file's rig, `rig: boat`, as the harbour's `_is_boat`
already reads it, `ui/harbour.py:198-206`); sweeps **as a fit** of the xebec (the brief: her
sweeps a fit), so a file says whether she carries them and how many; **an evolution** to get them out and
in, its men drawn from the company (all hands, or a watch, by the fit), several men to a sweep (the
figure from the sources: Winfield's picture of oarsmen "crowded between the gunports on the gun
deck", `VesselReferences-2026-11-Spanish.md` §3; the men to a sweep and the sweeps' number are the
xebec's research, and a passage of Winfield's to ask for, §12); **the guns against the oars**: the
sweeps worked from the gun deck by the men who would fight the guns, so the quarter bill and the
oars share the deck and the men, which the boat's model knows nothing of; **the thrust**: the boat's
form serves (a pull and a power a sweep, its men's sum), its figures fitted to what the sources say
a xebec makes under sweeps; and **the words** of the ship's own orders ("out sweeps", "in sweeps",
the stroke's), the boat's kept for the boat.

---

## 6. Three gun decks

### 6.1 The probe (measured)

The three-decker probe (§0): six decks with guns in her profile (`lower`, `middle`, `upper`,
`quarterdeck`, `forecastle`, `roundhouse`), 28 guns on each of the three gun decks: 102, 110 and
106 guns in the 74's three fits so raised, 110 in her default (the 74's 1795 fit).

- **It loads.** `schema.DECK_WORDS` already holds `middle` (`schema.py:339`).
- **Her guns are named by deck**, the 74's `numbering: by deck` carried: "No. 1 starboard gun of the
  middle deck".
- **The beat to quarters says each deck**: "The lower deck: 14 gun crews, 182 men." "The middle
  deck: 14 gun crews, 126 men." "The upper deck: 14 gun crews, 126 men.", then the quarterdeck's
  seven, the forecastle's three and the poop's three; 504 of 839 at the guns (`_deck_lines`,
  `crew/quarters.py:497`, wants a lower and an upper deck and takes a middle between them).
- **The guns' orders by deck are understood**: "fire No. 3 gun of the middle deck" ("No. 3
  starboard gun of the middle deck and No. 3 larboard gun of the middle deck to fire as soon as cast
  loose and ready"); "fire the middle deck" with no side engaged asks which side, as on a 74.
- **The lee ports shut deck by deck** in their order, each in the log's words: "The lee lower-deck
  ports are shut", "The lee middle-deck ports ...", "The lee upper-deck ports ..."
  (`combat/ports.py:79`, `_DECKS_SAID_SO`), heeled by hand, at 10.5°, 32.5° and 66.5° on the
  probe's scratch sills.
- **The viewer's check** (`tools/check_viewer_guns.py`) is clean on her file, every port gun on its
  triple, the over-the-rail notes the 74's.

### 6.2 What the code assumes of two decks (read: `lower`, `upper`, `middle` grepped)

| Place | What it assumes | For a three-decker |
|---|---|---|
| `crew/quarters.py:418-435`, `_shut_crews` | only the lower deck's crews can be robbed for their shut ports | a middle deck's crews behind shut ports are not counted |
| `crew/quarters.py:668-687`, `_rob_order` | the lower deck's shut crews first, "the other decks" next, the lower deck's last | her middle deck ranks with her upper works; the order by deck to be her document's (judgement) |
| `crew/quarters.py:559-563`, `_keeps_its_deck` | the crews keep their deck where a broadside gun stands on `lower`, or the guns are numbered by deck | holds for her |
| `orders/gunnery.py:222-225` | "the main deck" is the upper (Cumby's word for a 74) | which deck the word names on a three-decker is her document's, from the period's usage; the Spanish *baterías*' words are hers too |
| `client/projection.js:3956` | "upper-deck port", and any other deck its bare word | "a lower port", "a middle port" (the 74's "a lower port" is said today); the log's "-deck" form would serve |
| `evolutions/action_scripts.py:49-57`, `clear_seconds` | the time to clear by length, capped at the frigate's quarter of an hour | a first rate clears as the 74 and the frigate do: cleared at 1,086 s and beat to quarters at 1,195 s, the 74 as filed to the second (measured) |
| `world/ships.py:380` | "a ship of the line" names the 74's file | a three-decker wants her own words beside it |
| `world/captains.py:296-359`, `SIZE_RANK`, `size_rank_of` | ranks to 4, the ship of the line | "a three-decker" and "a first rate" rank nothing (measured: `None`); "a xebec", "a polacre", "a tartane", "a corvette" nothing either |
| `tools/ships/bellerophon.py:2499` (`GUN_DECKS`), 2506 | the 74's module's own list of decks; the exercise allowance "a third in a ship of two decks" | `gen_ships.exercise_allowance(n, decks=3)` already takes three (the Regulations' "two or three decks", 4425-4436); a new module lists its own decks |

### 6.3 What the build wants

Each of §6.2's places read again for a third deck (none needs more than its list widened or its
words; judgement); her words and rank in the two tables (the rank of a first rate against a 74's
4 is the owner's, §12); her quarter bill by deck from the Spanish sources (the probe's is the 74's
bill on 839 men and says nothing of hers); the clearing time of a first rate, if her sources give
one longer than a 74's; and **the obús** (the 1803 and 1817 fits' howitzers): today "a gun is one
of long, carronade, swivel" (`schema.py:271`; measured: refused at load), while a 48-pounder
carronade is accepted. Whether the obús is a new kind or carried as a carronade by JUDGEMENT is her
document's (and the *Diana*'s, whose 1817 fit has four 3-pounder obuses), and the magazine's, the
far fight's and the viewer's tables are to be measured for a 48-pounder before her file.

**The pound of a Spanish gun.** The engine reads a gun's `pounder` as the weight of its shot in
English pounds: the broadside by package 70's rule sums it (`combat/action.py:469, 487`), the ball's
diameter is the 18-pounder's 5.04 inches scaled by it (`combat/hits.py:106-109`), the magazine keys
its cartridges and shot on it (read). Winfield gives the Spanish broadsides in *libras* with their
pounds beside (1,212 libras as 1,308 lb, 1,188 as 1,282, 1,508 as 1,627:
`VesselReferences-2026-11-Spanish.md` §4), the same ratio in all three. The lead's note says to
take the book's pairs as it gives them and not to re-derive the ratio. **The owner's** (the
decisions sheet's question 9); the plan's pick (its §4 row 8) is the gun filed as her navy named it
(`pounder: 36`), the book's pairs in the note as it gives them, the broadside then reading a little
light in English pounds and the notes saying so; the other way is the English weight in `pounder`,
from Winfield's volume by calibre if it gives them (a passage to ask for, §12), with the words
taken from a separate key. Either way the gun's calibre in libras is in its words and its note. The
generator's weight tables (`gen_ships.py:4295-4296`, `period.py`) are English patterns, and the
Spanish guns' weights come from the Spanish sources.

---

## 7. A first rate's company and the pace

**The measures** (measured on this machine, quiet: the two suites of §1.4 finished, the processor
at 1 to 5 per cent before each; seed 7; a thousand ticks to settle, then the best of three timed
thousands, truth 51's form):

| World | The 74 as filed (590) | The three-decker probe (839) |
|---|---|---|
| Her file alone on the gate's day (`tools/pace.py`'s `seventy_four_alone`, truth 51's form) | 514 ticks a second | 487 |
| Truth 7-196's own world (its body run in scratch: the frigate hove to off the Lizard, three of the file in her squadron one to three miles off; `CREWED_CAP` 3) | 79 and 81 (two runs; the thousands 55 to 81) | 72 and 75 (the thousands 47 to 75) |

In truth 7-196's world every run kept the cap at three, the three in company within 2.8 miles at
each thousand's end (S2 at 2.79, as the truth's docstring has it), every company whole and no line
of an action in any log; the truth itself passes on this tree (78.7 s). Its floor,
`CREWED_FLOOR_TICKS_S`, is 60 (`world/crews.py:99`); truth 51's, `BUILD_MACHINE_FLOOR`, 500, the
74's own clause recorded and not pinned (the docstring of truth 7-196).

**What it says** (judgement on the figures): three crewed first rates of 839 cost about a tenth
more a tick than three 74s of 590 (72 to 75 against 79 to 81), for 42 per cent more men: a crewed
ship's tick is not in proportion to her company (what is most of it, her hull, her rig or her
captain's brain, was not profiled here). Alone, the first rate runs a twentieth slower than the 74 (487 against 514), as the 74
runs a twentieth slower than the frigate (the docstring). So **839 wants nothing of its own of the
engine for its pace**: the crewed cap of three and the floor of 60 serve her as they serve the 74,
on this machine with a margin of a fifth; on the build machine the figure is the cloud's pace job
to give, not this note.

**Two things found, for the lead:**
1. Truth 7-196's world gives 79 to 81 here against the 150, 151 and 147 its docstring records on
   the owner's machine on 13 November, the same world to the mile. Whether the machine or the
   tree since then makes the difference is not measured here.
2. `tools/pace.py seventy-four`'s crewed measure is not truth 7-196's world: it puts the three 74s
   beside the frigate with no squadron, and they fight her ("A frigate has struck her colours!" at
   tick 2,280 of 4,000; her company 264 to 44, a 74's 590 to 546 over the measure), so its figures
   (167 with three 74s, 86 with three of the probe) time an action. The truth's docstring says why
   its own world was changed; the tool's was not.

---

## 8. The regency's cruiser as a role (package 116's road)

**Today (read, and the doctrines loaded):** a role is a book of `data/captains/` (`role:`, `name:`,
`source:`, `thresholds:`, its transitions and books), read by `load_doctrine`
(`world/captains.py:1017`), each threshold `{value, source}`, and named in the code's `ROLES`
(`world/captains.py:137-150`, ten roles). Loaded: the cruiser's book has 65 thresholds, the
revenue cutter's 66 and the privateer's 70 (`board_odds` 1.3, 1.3 and 1.0; `engage_nm` 1.0, 1.0
and 1.5; `man_of_war_nm` none, 6 and 2.5); a role of no book is refused in words ("There is no
doctrine for the role 'corsair'; the roles: kings-ship, merchant, ..."). Package 116 moved the prize
doctrine's thirteen keys under `thresholds:` in `cruiser.yaml` and the revenue cutter's
`revenue.yaml` (whose book is the cruiser's), seven of them read by the code and six not
(`mans_prizes`, `divide_prisoners`, `prisoners_most`, `burns_when`, `worth_least`, `fit_least`;
its record). The revenue book is the form for a role that is another's book with its differences
stated at its head (four, each judgement).

**What the build wants:** a role's name in `ROLES` and its book (code and data, the revenue
cutter's step of SW-4 the precedent); the Barbary regency's cruiser as a book on that form, the corsair's
differences from the privateer's and the cruiser's said at its head, each with its source: whom she
chases (a Christian merchantman of a nation at war with her regency, or without a passport), her
boarding (the xebec's company boards: `board_odds`, `board_when`), her prize doctrine (the thirteen
keys, the prisoners the cargo: the six unread keys matter to her more than to any King's ship, and
what acts on them is not built), her `engage_nm` and `man_of_war_nm`; and the Spanish navy's
xebec on the King's ship's or the cruiser's book with the coastguard's station. The regency as a
nation for the world's business (its flag, its ports, its relations with each power by the year)
is the nations' table's and not the engine's; the lead's to place (§12).

---

## 9. The harbour's shelves (package 96)

**Today (observed):** the harbour offers every ship file of `data/ships/` but the boats for a bare
start, her fits read from her file, her kinds and roles from `world/ships.py`'s `DESCRIPTIONS`
(seventeen rows); a scenario is offered from `client/harbour-shelves.yaml` with one sentence, and
one that no shelf names stands on "Not yet sorted" (`Harbour._shelve`: a scenario named
`xebec-off-algiers` went to `unsorted`, `mahon` to `passages`). `tests/test_harbour.py:131`
asserts that no scenario of the game is unsorted.

**What the build wants:** a shelf line for each new scenario, a sentence each, in the shelf it
belongs to (the Mediterranean passages' or the trade's); a `DESCRIPTIONS` row for each new kind
(her rig's word, her roles), which the harbour reads for her kinds and roles. The ship's whole
configuration as one thing (`Design-Harbour.md`) is designed and not built, and nothing of this
package waits on it.

---

## 10. The wheel shot away, and the relieving tackles (package 116)

**Today (observed, on the cutter as filed and the tartane probe):** the hit sets `helm_lost` to "the
wheel shot away" for every hull (`combat/hits.py:216-229`); the helm orders and the manoeuvres are
refused in the ship's words ("The wheel is shot away and the helm does not answer: rig the
relieving tackles ... or repair the wheel ..."); `rig the relieving tackles` waits for hands while
the watch is at other work ("Not hands enough on deck to rig the relieving tackles"), begins 151 s
(the cutter) and 47 s (the tartane) after the order and is done at 515 s and 412 s: "The relieving
tackles are rove to the tiller and manned below: the helm answers again, steered by the tackles,
and more slowly than by the wheel."; `repair the wheel` takes the carpenter's crew of four, "new
wheel-ropes to be rove", done in 2,387 and 2,410 s. **On a tiller-steered hull every one
of those words is a wheel's**: the cutter's own file says "One man at the tiller (a cutter steers
with a tiller; judgement)" (`data/ships/cutter.yaml` l. 869), and she is told her wheel is shot
away and repaired with new wheel-ropes.

**What the build wants:** the hull's helm read from her file (a wheel, or a tiller worked from the
deck by hand or by tiller ropes, by her sources: the small lateen craft by tiller, the
three-decker and likely the *Diana* by a wheel), and the tiller's words: the tiller (or its ropes)
shot away, the relieving tackles hooked to the tiller as now, and the repair a spare tiller shipped
or new tiller ropes rove, its time and hands the hull's. It is every tiller-steered hull's
(the cutter, the lugger, the smack, the schooners), and moves their words where a helm is shot
away (truth 7-626 is the one recorded passage with a wheel shot away); the owner's whether it is
built for all of them at once (§12).

---

## 11. Package 81's viewer checklist for a lateen hull and a three-decker

The checklist (`Build-Ships.md` §6, its postscript): `hull.profile` with `rail_m`, `breadth_m` and
`decks_m`; `ports_m.<deck>` a triple at every broadside gun's and chaser's `x_m`; `port_size_m` a
deck; every gun's kind, pounder, place, side, `x_m`, `weight_cwt` and deck; then
`tools/check_viewer_guns.py` clean, and the test.

- **A lateen hull** (the xebec probe, the brig's hull and guns under three lateens): clean, "18 guns:
  18 port; empty ports a side: upper 1" (measured). Nothing in the checklist reads the rig. For the
  xebec's own file: the sweep ports between the gun ports are no gun's and are not in `ports_m`
  (the viewer draws ports where guns stand); if her document draws them, that is a viewer change
  beyond the checklist (judgement). **Her lateens are not drawn as lateens yet** (read): with no
  `corners_m` a lateen is drawn as a four-sided sail hanging under its yard, "from its yard's ends,
  its area over the yard" (`projection.js:1536-1541`), the yard at a fixed tilt of 0.8 rad (904);
  with `corners_m`, by the lug's cut as a standing lug on its lee side (1506-1509), the code's own
  comment saying "until the package that builds a whole lateen draws it as its own" (815-816). A
  whole lateen's triangle, its side read from the sail as a dipping lug's is, and the yard's own
  peak are viewer work of this package's (Ext §3.7), beyond package 81's checklist.
- **A three-decker** (the probe): clean, every port gun on its triple, the notes the 74's
  over-the-rail ones (measured). The viewer reads `ports_m` and `decks_m` by their keys
  (`projection.js:2499, 3037`), so three tiers are drawn as two are; its words for a port are the
  one place it names a deck (§6.2). Her stern's three tiers of lights and galleries are her
  profile's (`galleries_m`, a tier each: `projection.js:3357-3389`) and the viewer takes any number.

---

## 12. For the owner, and passages to ask for

**Decisions** (my pick first; the decisions sheet, `Decisions-Package90-2026-11.md`, puts them to
the owner as its questions 2 (item 37), 3 (going about), 6 (the sweeps) and 8 (the rank), and takes
5 and 6 as recommended in its Part E):

1. **Item 37.** (a) The generator reads the engine's curves, rounded to two places, with a test
   holding them together; truth 35's last clause and the frigate's six-points test re-measured old
   beside new, and the five records of no figure moved naming the booms; or (b) 1.25 kept as a
   stated JUDGEMENT; or (c) the studding curve lowered. Before any new file is generated.
2. **`tack ship` on a lateen rig.** (a) Answered in her words and nothing done, naming the wear
   (the tartane's design has "She does not stay under her lateen; wear her.", its decision 13),
   with `put her about` choosing the wear and saying why; or (b) taken as a wear and said so. Which
   rigs it reaches (a whole lateen on the main, as the tartane's design has it, or any whole lateen
   bent) is the same decision's, the polacre's square main being the case that tells them apart.
3. **The sweeps' men.** (a) Drawn from her company by an evolution, so many to a sweep by the
   sources, and not at the guns while they pull; or (b) the boat's model as it is.
4. **A first rate's rank** in the captains' judgement: (a) a rank of her own above the 74s', or (b)
   the ship of the line's 4.
5. **The tiller's words** for every tiller-steered hull at once, or for the new hulls alone.
6. **The obús**: a gun kind of its own, or a carronade by judgement.

**Passages of Winfield's Spanish volume to ask for** (the owner sources them; by title and class):
- *Jabeques* (the xebecs), the 30- and 32-gun classes and the 14- to 22-gun classes by name: the
  number of sweeps (*remos*) and the men to each, and anything on going about under the lateens.
- The *Purísima Concepción* class (pp. 406-410 held): her masting and sails if given (whether she
  crossed studding sails), her steering, and the division of the 839 (seamen, gunners, marines).
- Wherever the volume gives it (its introduction to the artillery, or the Artillery Regulation of
  1752's table, pp. 1134-1136 held): the weight of shot of each Spanish calibre in English pounds,
  for the guns' `pounder` (§6.3), and the weights of the guns and of the obuses.
- The *Diana* (p. 930 held): her rig and masting, and her steering, if the entry gives them.
- *Tartanas* (pp. 1249-1252 held): the companies of the navy's seven, for the coastguard role.
- *Polacras* (pp. 1083-1084 held): the eight in the records, any that gives her masts' and yards'
  handling.

---

## 13. Found on the way

1. Every wear begins "Up helm; brace in the after yards." whether she has after yards or not (the
   lugger as filed; `scripts.py:1987-1994`); words only, older than package 90 (§2.2, 4).
2. Every tiller-steered hull is told of a wheel and its wheel-ropes when her helm is shot away
   (§10).
3. The viewer says "a lower port" of the 74's and the 64's lower-deck ports where the log says
   "the lee lower-deck ports" (`projection.js:3956`; §6.2).
4. The sprit class has no `PEAK_COEFF` entry, so a sprit sail on a rated spar raises at generation
   (`map-engine.md` §4, read); the mend of §1.5 gives it the engine's 1.20.
5. The generator's helpers are English feet (`gen_ships.FT`, `ft()`, the proportions' rules from
   Steel and Fincham in feet). A Spanish hull's module takes Winfield's metres for its constants and
   states its own pie de Burgos (0.2786 m) for the plans' figures, as the 74's module keeps its own
   constants (`VesselReferences-2026-11-Spanish.md`, "Units"); the ship file itself is in metres.
6. Truth 7-196's world runs at 79 to 81 ticks a second on this machine against the 150 its
   docstring records for 13 November; and `tools/pace.py seventy-four` times a fight, not that
   world (§7).
7. A ship file with `oars:` is taken for a ship's boat by every boat predicate (§5).

---

## 14. The steps, as the plan names them: the design for the lead's approval

The plan's A0 to A9 and V1 to V4 (`Plan-Package90.md` §6) as one design, drawn from §1 to §11 above
and from the hulls' second drafts. **The lead approves it, A1's above all, before stage 0L** lays
the whole lateen's interfaces (the plan's §5.2). Each step is keyed on what no committed file
carries except where its last column says what moves, each is merged alone and measured old beside
new, and the files each may change are the plan's §7.1.

| Step | The design | Key | What it moves (measured at the ground report) | Here |
|---|---|---|---|---|
| **A0** | Item 37: the generator's `PEAK_COEFF` read from the engine's curves (`data/sail_classes.yaml`), rounded to two places as now; a test holding the two together; the sprit class gaining the engine's 1.20. Only under the owner's (a) | the generator | 74 `rating_kn` figures in 9 files (the studding-sail and ringtail booms, about 15 per cent up); truth 35's last clause and `test_studding`'s frigate at six points re-stated; five "no figure moved" records naming the booms; seven byte pins passing again by the regeneration; truths 9 and 14 hold | §1.3-§1.5 |
| **A1** | **The whole lateen going about.** (1) Its side: `dipping` allowed on a whole lateen (class `lateen`, no `cut_at_mast`); `Sail.lug_side` kept for it; `against_the_mast` reads it, the loss the lug's two-thirds of the cloth (JUDGEMENT, the hulls' to measure). (2) The change: a new evolution `change_lateen`, the yard peaked up beside the mast by its halyard and ourses, its heel passed abaft the mast, the tack hooked on the new weather side and the sheet hauled aft to leeward, **never lowered**, its scripts on the settee's `SetteeChange` (B3.3), its hands by `too_few: all hands`, its time JUDGEMENT. (3) Going about, keyed on the main sail: `Ship.wears_only()` (a whole lateen as her main) answers `tack ship` in her words ("She does not stay under her lateen; wear her.") and does nothing; `put her about` chooses the wear and says why (package 45's road); the captains' books and the director meet the same; the wear changes each whole lateen at "wind aft". A square main (the polacre) tacks as a brig's, her aftermost whole lateen hauled aft at helm's a-lee (measured on her probe: 157 s against 164 s), the foremost eased with the head sheets and drawn at "let go and haul", both changed after. (4) The lateen mizen: hauled aft as she comes to, eased at "up helm", kept set hove to; `after_gaff_sails` never takes a whole lateen. (5) `shift the mainsail` and `shift the mizen` (`dip` its synonym for a lateen) for a lateen left on the bad hand, refused in words on the good, kept apart from the sail room's "shift ... for ...". (6) `set_lateen`, `take_in_lateen`, `furl_lateen` and `reef_lateen` sized by the ship's data or `too_few: all hands`. (7) The heave-to refused, for a rig with neither head sail nor braced yard, in the xebec's words ("She will not lie to under her lateens: there is no sail to bring her to."), her lying to booked | `dipping` on a whole lateen; `wears_only()` | nothing of the eighteen files (none carries a whole lateen; the 64's and the 74's mizen courses are `cut_at_mast`); the probes' tests as filed | §2.3 items 1-7 |
| **A2** | The words of a rig with no yards, the cause's mend for every rig: the wear's "brace in the after yards" said only where she has after yards; the tack's "braced up on the ... tack" only where she has a braced yard | the rig as filed | the wear's first line and the tack's last line in the lugger's, the cutter's and the smack's recorded passages: words only | §2.3 item 8; §13 item 1 |
| **A3** | The helm's kind, for every tiller-steered hull: `helm: wheel` or `tiller` (default `wheel`); on a tiller the hit says the tiller or its ropes are shot away, the relieving tackles hook to the tiller as now, and `repair the wheel` is answered as the tiller's repair (a spare tiller shipped, or new tiller ropes rove), its time and hands JUDGEMENT for the lead | `helm: tiller` | the six files whose notes say tiller (the cutter, the lugger, the smack, the two schooners, the hermaphrodite brig), regenerated with the key; their words where a helm is shot away; truth 7-626 measured | §10 |
| **A4** | The boat in tow: a boat's `towed: true`, manned from alongside and not hoisted out; its words; its drag left out as small beside the hull's at her speeds (JUDGEMENT, measured against the trawl's form) | a boat's `towed` | nothing (no file tows a boat) | §3 |
| **A5** | A yard's level read from its place: `Ship.yard_level(yard)`, the rank by height of a braced yard among the braced yards on its own lower mast (0 the course), the yards under the bowsprit apart, read once a ship from the parts and held beside her as B3.4's memo is; read at the twelve places that read the parent's class today (`Design-Ship-Polacre.md` §5.1). A square yard over a whole lateen on the same mast with no braced yard below it (the tartane if her tréou is left out) counts the lateen yard as the level below (JUDGEMENT; the lead rules: Tar-D §5.1a). **Before the tartane's file**, the package's first pole main | the parts as filed | the smack: her topsail a topsail, not a course, in the heave-to, lie a-try and the take-in words with it set (no pinned passage sets it); a guard over every file's yard levels, old beside new, equal but for the smack | §4; Pol-D §5.1 |
| **A6** | The pole mast's quick handing ("amener en paquet"): the upper square sails of a pole lowered together onto the yard below, furled and reefed from it, the men on the yard below (Falconer; Steel p. 236); the topmast evolutions refused in words; times JUDGEMENT for the lead | a lower mast carrying braced yards above its lowest, with no topmast (the smack's, the tartane's and the polacre's mains) | the smack's topsail taken in and furled so (measured) | §4; Pol-D §5.1 |
| **A7** | Sweeps of a ship's own, never `oars:`: the `sweeps:` section (number, men each, a man's thrust and power, the tiring), package 82's law in the ship's substep, its state in `ship.extra["sweeps"]`; `out sweeps`, `in sweeps`, `give way`, `easy all`, `lie on your sweeps` where the hull has sweeps; an evolution manning `number × men_each` from the watch or all hands, the men taken from the sails and the guns while they pull; **the far body's pace in a calm** (`world/ships.py`'s `VESSEL_MIN_SPEED_KN`, l. 98, read at l. 849 and 865); the boat predicates kept a boat's | `sweeps:` | the library's count of evolutions; the vocabulary's order lists; the checkpoint's names list | §5 |
| **A8** | The lateen in a gale: the reduction shifts storm canvas set `in_place_of` a whole lateen (the xebec's small lateens, the tartane's bouffette) at the topsails' second reef (Luce p. 476's level), in place of reefing; a whole lateen in no "courses" group. **The lateen row tuned** once, before the xebec's merge, on the truths of the lateen hulls on the branch then (the polacre's re-measured old beside new when she lands); the lead's leftover 4 of 2026-11-07 (the second reef queued on a course already being reefed) if the lead gives it here | storm canvas `in_place_of` a whole lateen; the lateen row, which no committed sail reads | nothing committed; the lateen hulls' own figures; `PEAK_COEFF["lateen"]` follows the row by A0 (a) | Tar-D §5.4 item 6; Xeb-D §5 |
| **A9** | Three decks: `_shut_crews` and `_rob_order` for a middle deck (`crew/quarters.py:418-435`, `:668-687`), the upper deck's crews robbed before the middle's; "the second deck" and "the third deck" in `orders/gunnery.py`; "the main deck" refused on a three-decker in words naming her decks; her words and rank are her rows (stage 0 and her builder) | a `middle` deck | nothing (no file has one) | §6.2-§6.3; Con-D §5.5, §6.3 |
| **V1** | The whole lateen drawn: three corners on its yard slung at a third on the mast's raked line, on its lee side; peaked up its mast while it is changed; against its mast on the bad hand (`client/projection.js:815-816`, `904`, `1506`, `1537`) | as A1 | every committed file's picture unchanged | §11 |
| **V2** | The pole mast drawn with no doubling; the upper yards drawn down on the lower while lowered | as A6 | the smack's picture with her topsail lowered | Pol-D §13 |
| **V3** | The towed boat drawn astern on its painter | as A4 | none | §3 |
| **V4** | A port's words in the log's "-deck" form ("a middle-deck port") | the deck words | the 74's and the 64's "a lower port" become "a lower-deck port": words, old beside new | §6.2; §13 item 3 |
