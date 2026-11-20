# Report: package 90, the tartane (her builder, 20 November 2026)

**In short.** `tools/ships/lateen.py` is filled and committed alone first. Her module then writes
her two files: `data/ships/tartane.yaml`, the trader *Saint-Pierre* (ten hands, unarmed), and
`data/ships/coastguard-tartane.yaml`, the guarda-costa *San Pedro* (thirty-four, Chapman's eight
long 4-pounders and four swivels). Both are one hull in two roles. Her main stands **upright**,
by the owner's rule: it measured the better sailing of the two rakes. Her `displacement_kg` is
**142,200 kg**, her drawn body outside the plank at H. Of her nine truths, **two hold on the tree
as it stands and are written** (7-681 and 7-688). Seven wait on engine steps not yet merged. No
other ship file moved: the eighteen are byte for byte.

**The tests.** The final fast tier on my head (b33adfd), compared test by test with the base on
f6f26f8a: **no test of the base changed its outcome**. Of the 152 new tests, 136 pass and **16
fail**. All 16 are `tests/test_view_geometry.py`'s cases on her two files:
- 14 want the viewer's drawing of a whole lateen (V1);
- 2 want the viewer's rule for a level spar, which roots her beak at the rail.

That file was the viewer's, and §9 lists its 44 cases as they stood on ecf6180, unedited under
the stop rule. The coordinating session then widened it to me for her rows (the lead's nudge 32,
item 1). §10 has her rows, her named rows with their reasons, and the 16 that remain. The slow
tier of her files passes: 117 tests, among them four anchorage cases §9's run had left out
(§10).

**The branch.** `…/pkg-90-tartane`, cut from f6f26f8a (`git log -1` checked). I merged
nothing from `…/pkg-90`, so my base and my final run are on the same tree. Nothing was
rebased or forced.

## 1. The commits

| Step | Commit | Files |
|---|---|---|
| 1, `lateen.py` alone | `bfec7fa3307162bc7fc23845b60cb6784ca903c9` | `tools/ships/lateen.py`; `tests/test_tartane.py` (its eight tests); `tests/test_probes_90.py` (the stub's pin restated); `docs/dev/TuningNotes.md` ("Package 90, the tartane", step 1) |
| 2 to 4, her module and her files, and two mends found by the tests | `0dbd4fc933df9b37adac5fb8b8dbe2ab318d6dfa`; mends `b4e814c7e9bc99d285d6b57c7644f3fd820877b5` and `ecf61800db82ce5cc3bb3de31b61a3b69e185b5d` (§8, §9) | `tools/ships/tartane.py`; `data/ships/tartane.yaml` and `data/ships/coastguard-tartane.yaml` (generated); `data/people/tartane.yaml` and `data/people/coastguard-tartane.yaml`; `freesail/world/ships.py` (her two `DESCRIPTIONS` rows and her words); `freesail/world/captains.py` (the coastguard's `SIZE_RANK` row); `tests/test_tartane.py`; the moved pins (§8); `docs/dev/TuningNotes.md` (step 2 and the mends) |
| her rows in the viewer's tables, and her storm jib's corners (§10) | `b33adfd69facb88dfc007b9e4cf37e61b32b0119` | `tests/test_view_geometry.py` (widened to me, §10); `tools/ships/tartane.py`; her two ship files (generated); `docs/dev/TuningNotes.md` |
| this report | `e743467`, and §10 in the commit that adds it | `docs/design/Report-Package90-Tartane.md` |

**Step 1's commit carries the owner's name as its author.** I set it by hand for that one commit.
Every later commit is under the session's own default identity, as the other cloud builders'
are. No commit message names a model or its maker, and none has an attribution trailer.

**Files beside my row, each within the card.** My §7.1 row names `tests/test_tartane.py`, my two
ship files and their people files, my row of `MODULE_FILES` and my `DESCRIPTIONS` rows and words.
These are beside it:
- the stage-0 pins of the two stubs I filled, in `tests/test_probes_90.py` ("the tests of these",
  the card's "May change": the tests of `lateen.py` and the five modules);
- the pins that count ship files or their rows: those the plan's §10.4 names for each hull, in
  `tests/test_schooner_mast.py`, `tests/test_lee_ports.py`, `tests/test_known_truths.py` (truth
  7-190) and `tests/test_subtypes.py`; and those the fast tier found beside them, in
  `tests/test_schooner_mast.py` (the gale's list), `tests/test_profiles.py` (the pair check),
  `tests/test_known_truths.py` (truths 7-700 and 7-701) and `tests/test_neufchatel.py` (the
  rows' roles);
- one `SIZE_RANK` row in `freesail/world/captains.py`, for the coastguard's description key. The
  cutter's sub-types each have one, and the card names "the rows of `world/ships.py` and
  `world/captains.py`".

If the coordinating session reads the row more narrowly, those are the edits to look at.

## 2. The basics (the plan's §8.0 form)

### 2.1 Her particulars against their sources

| Clause | Filed | Source and band |
|---|---|---|
| Length, breadth | 20.38 m on Forfait's length (her factors' base); `beam_m` 6.60 | Forfait 1788 Table II, the *Humble*, 62¾ by 20⅓ pieds (read on the page image). 20⅓ pieds is 6.604 m at the tree's `PIED_DU_ROI_M` (0.3248); her design's 6.61 is at 0.32484. A centimetre, within her check |
| Waterline, draught | 18.47 m; 2.38 m mean on H | Pages §4.1, §4.2 (measured; the lead's rulings 1 and 4) |
| Displacement | **142,200 kg** | her drawn body outside the plank at H (the lead's nudge 30): Chapman's body to H with its keel, 135.2 t moulded (Pages §4.3, ±6%), plus a plank of 2½ pouces, 7.0 t; **2 to 3 pouces give 140.8 to 143.6 t** (JUDGEMENT). Her profile's own drawing, with the plank, gives 143 t (+1%) |
| KM, GM | `gm_m` 0.8 | KM 3.15 m on H (Pages §4.3), so KG is 2.35 m; GM is JUDGEMENT (her design) |
| Lateral area, hull speed | 40.9 m²; 10.4 kn | Pages §5.6; the files' rule on 18.47 m |
| `deck_height_m` | 0.54 | Pages §5.2; the lead's ruling 2 |
| `clr_x_m` | +2.0 | tuned for her helm, the house's way (§3) |
| Masts | the main 59 pieds at x +3.87 on the deck, upright; the mizen 30 pieds at x -4.44, raked 10 degrees aft | Forfait Table II and his places from the middle of the perpendiculars (x +0.49: Pages §6.4); heels on a keelson of 0.25 m (JUDGEMENT); the mizen's rake JUDGEMENT (Forfait p. 128; the lead's ruling 7) |
| Yards | great lateen 75 pieds (24.36 m), topsail 32 (10.39), tréou 41 (13.32), mizen lateen 47 (15.27), éperon 10½ (3.41) | Forfait Table II; the éperon by the lead's ruling 3. Each within a centimetre (truth 7-681) |
| Sail | plain sail 216 m²: the great lateen 79, the topsail 77, the jib 34, the mizen lateen 26; the tréou 81 (flying); in the sail room, the bouffette 53 and the storm jib 23 | Forfait's *Humble*, 236.1 m² with a topgallant; less his topgallant's 20 m² (JUDGEMENT), 216.0: **+0.0%**, inside her design's ±15% |
| Centre of effort | (2.55, 8.53) m | Forfait's (1.60, 8.19): reported, not tuned to (her design's §4.5) |

### 2.2 Her drawn depth and displacement beside the filed

- Drawn to the keel's lower edge, 2.07 m at the greatest section (x -0.23), against the file's
  2.38 m. The form's drawing measures the depth at the midship frame, where the plate's keel
  sits under the base line. The 2.38 m is the mean to the keel's lower edge on H (Pages §4.2).
  Recorded, not moved.
- Drawn displacement 143 t against the filed 142 t (+1%).

### 2.3 What was taken as judgement

- **The cut of her two lateens.** I took her design's reading of Forfait p. 121 literally (the
  clew on the deck at the foot of the mast, the car tacked at the stem), and the yard's angle
  follows from it: 34.4 degrees upright. The mizen lateen is cut alike, "semblable" (Forfait
  pp. 124-125), at the great yard's angle. Of four readings, this one alone meets Forfait's
  total (§6, question 1).
- The tack a 0.3 m luff under the throat, so that the sail is written with four corners for the
  drawing.
- Her main's hounds are the sling, the halyard's block at the foot of the ton (Tar §2.1's
  reading).
- The topsail yard 3 pieds under the masthead.
- The topsail by the cutter's rule, its foot 0.9 of the tréou's yard; the tréou from its yard at
  the hounds to the bulwark's top at the mast.
- The jib by Fincham's rule for the cutter's foresail, on her stay from the hounds to the
  berthelot's end.
- The bouffette two-thirds of the great lateen, cut alike about its throat.
- The outrigger the lugger's 0.364 of the length, two-thirds outboard; its end is no part.
- The plank, 2½ pouces (2 to 3); the keelson, 0.25 m; the rabbet's half-siding by the house's
  share; the fourth port's half-breadth read between fore 6 and fore 9 (±0.09 m: Pages §5.7), so
  its gap of +0.08 m is reported and not held.
- Rope sizes, canvas numbers (the lateens No. 2 and 3, the bouffette No. 1), and the brace
  limits (the cutter's).
- The rudder: the cutter's blade by her length and draught, 1.3 m², its span 2.3 m.
- Her company: ten (8 to 12) and thirty-four, the stations, the shares by rating, the stores,
  the one boat of 4.5 m (a yawl by the house's kinds), the hold, and two hand pumps.
- The coastguard's four swivels, two a side aft on the rail; her shot the hired cutter's.
- Her names, Saint-Pierre and San Pedro. Both people files are on the `spanish` list by the
  brief's word; her design's §6.4 had `french` for the trader by default.
- The bulwark kept on the trader as on the war tartane (her design left it to me).

## 3. Her polar beside the cutter's, her helm, and her tack, wear and heave-to

All at seed 7, 15 kn from the north, no gusts. All hands called, plain sail set and braced
sharp up, then trimmed every two minutes (the known truths' `settle`, 1,800 s and 1,200 s).
Her figures are upright at `clr_x_m` +2.0, as filed.

| | Her | The cutter |
|---|---|---|
| Polar at 40, 50, 60, 70, 90, 120, 150, 180 degrees (kn) | 1.29, 2.72, 3.84, 4.89, 5.77, 5.61, 5.11, 4.69 | 1.96, 4.36, 5.89, 6.59, 7.23, 6.79, 5.68, 5.40 |
| Closest (the polar's first angle of a knot); beat | 40; 60 | 40; 60 |
| Best way made good to windward (polar) | 1.92 kn | 2.95 kn |
| Sailed 67.5 and 90 degrees off: knots; helm (weather +) | 4.65, 5.80; +0.25, +0.79 | 6.11, 7.17; +2.18, +5.74 |
| `tack ship` from 290, 292.5, 295 degrees: s; m to windward in 15 min | 165, 393, 394; 621, 126, 50 | 107, 106, 106; 898, 897, 896 |
| `wear ship` from the same | 585, 734, 486; -21, -149, 63 | 458 each; 642 each |
| `heave to` from 292.5: off and knots at +300 and +600 s | 49.9 and 48.8 degrees; 0.80 and 0.82 | 47.3; 2.04 |

**She is slower than the cutter** at every angle but her closest. She carries 216 m² of plain
sail on 142 t, where the cutter's file carries more on 106 t. Forfait's sail is what it is, and
no source gives a tartane's speed. Recorded, not tuned (the lateen row is A8's to tune: her
design's §15 risk 4).

**Her tack, wear and heave-to as they stand, part by part** (her file as filed, from 292.5
degrees):
- `tack ship`:
  - +1 s "Ready about. Helm's a-lee; ease off the head sheets." and "All hands about ship.";
  - +36 "Let go and haul. Draw jib; trim aft the head sheets.";
  - +393 "Tacked; braced up on the larboard tack, heading NE (43°)": she comes out of stays at
    43 degrees off and 0.74 kn.

  Nothing is said or done of either lateen, which has no side until A1a.
- `wear ship`:
  - +1 "Stand by to wear ship. Up helm; brace in the after yards.";
  - +49 "Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up.";
  - +401 "Steady on ENE (68°)", with leeway up to 58 degrees between;
  - +734 "Wore ship; braced sharp up on the larboard tack".

  "Brace in the after yards" is said of a ship with none. That is the fault A2 mended at its
  cause on the package's branch (00382c4), after my base; I did not merge it.
- `heave to`:
  - +1 "Hauled up the courses." (her topsail, a course on her pole main until A5), "The jib sheet
    to windward; helm a-lee.", "Hands to the after braces; heave to." (A2's words again);
  - +145 "Hove to on the starboard tack, under her fore-and-aft canvas". She then lay 49 to 50
    degrees off at 0.8 kn, inside truth 12's band.

  This is not yet her heave-to: her topsail is hauled up as a course, not laid aback (A5).

**The knife's edge.** Her tack and her wear vary widely by heading and by a quarter metre of
`clr_x_m`. At `clr_x_m` 0.0 she tacked from 292.5 in 298 s, gaining 488 m; at +2.0, in 393 s,
gaining 126 m. The going-about truth for the frigate says the same of the model. A1a to A1d
change her going about wholly, so these are a record of the tree as it stands, not her handling.

## 4. Her main's rake, by the owner's rule

**Upright, as measured.** The owner's rule of 2026-11-20: "Use the rake which provides the
better sailing characteristic, upright, or slightly forward raked." The rake is one figure in her
module, `MAIN_RAKE_DEG`. Both ways were measured on the same harness, the yard re-cut each way
(39.3 degrees at 3 forward, 34.4 upright, its car tacked at the stem from the mast's line):

| | 3 degrees forward | Upright |
|---|---|---|
| Polar in 15 kn | 1.29, 2.66, 3.78, 4.84, 5.71, 5.56, 5.08, 4.66 | 1.29, 2.72, 3.84, 4.89, 5.77, 5.61, 5.11, 4.69 |
| Best way to windward | 1.89 kn | **1.92 kn** |
| Helm at `clr_x_m` 0.0, close-hauled and abeam | -11.71, -6.34 | **-9.71, -5.05** |
| At a matched helm (+2.25 forward, +2.0 upright): close-hauled, abeam | 4.58, 5.72 kn | **4.65, 5.80 kn** |
| `tack ship`, three headings: mean s, mean m | 252, 416 | 317, 266 |
| `wear ship`, three headings | 647, -102 | **602, -36** |
| `heave to` | 50.3 then 49.4 degrees, 0.8 kn | 49.9 then 48.8 degrees, 0.8 kn |

Every measure that does not turn on one heading favours upright, and Chapman draws it so (Pl.
LXII No. 16, Pages §7). Her tack and her wear split between the two by heading, and each rake has
one heading that goes badly. So neither is the better on going about, and the speed and the helm
decide. This is the owner's rule applied; her design's 3 degrees forward was its provisional pick.

## 5. Her truths: written, and waiting

**Written in `tests/test_tartane.py`, each a state that holds on the tree as it stands:**
- **7-681 (T-1)**, her particulars hold their sources: her length, breadth, masts, yards and
  places Forfait's within rounding; her lines Chapman's at her factors; her drawn displacement
  within Pages §4.3's band.
- **7-688 (T-8)**, before the wind the tréou set adds way, and the great lateen is taken in for
  it. Dead before 15 kn: 4.69 kn under plain sail, 4.35 with the great lateen in, and 4.86 with
  the tréou set flying.

**Waiting, each left drafted in her design's §13:**

| Truth | Waits on | Why |
|---|---|---|
| 7-682 (T-2), a point nearer the wind than a square-rigger | **A8** (the lateen row tuned), and **A1a** (her lateen's bad hand on one tack) | Measured from the same settle, she lies 60 degrees off making 1.91 kn to windward. The merchant brig holds 63.75 making 1.89, and comes up and stalls at 60. That is a third of a point and 0.02 kn, not "about a point". By the polar she is closest at 40 against the brig's 50, but makes less to windward (1.92 kn against 2.13). Not written: it would stand on a 1% margin |
| 7-683 (T-3), her tack and wear with her yards shifted or left | **A1a, A1b, A1c**, re-measured after **A1d** | the yard's change, the practice, `put her about` over 22 kn |
| 7-684 (T-4), the bad hand and `shift the mainsail` | **A1a** | the side, `against_the_mast`, `change_lateen` |
| 7-685 (T-5), hove to within truth 12's band | **A5, A6** | today she heaves to with her topsail hauled up as a course (inside truth 12's band, 49 to 50 degrees and 0.8 kn); her design reads T-5 after A5, her topsail a topsail |
| 7-686 (T-6), the gale: the great lateen in before 30 kn, lying to under the mizen and the storm jib | **A8**, with A1a's lateen evolutions | the gale's reduction of a whole lateen and the bouffette |
| 7-687 (T-7), a watch calls all hands for her great sail | **A1a** | `set_lateen` wants ten hands and has no `too_few` today |
| 7-689 (T-9), taken aback and on the bad hand | **A1d**, with **A1c**'s wear over 22 kn | the strain aback |

**Keys her files will take when the steps merge:**
- `dipping: true` on her two lateens (A1a);
- `helm: tiller` (A3);
- her boat `towed: true` (A4).

Each is a stage-0 guard's today ("no committed file carries it": `tests/test_probes_90.py`), so
her files carry none of them yet.

## 6. Her open questions

1. **For the lead: the cut of her lateens.** Her design reads Forfait p. 121 as putting the clew
   on the deck at the foot of the mast, with the yard peaked as she carries it and the car tacked
   at the stem. I took it literally, which sets the yard's angle (34.4 degrees). Her plain sail is
   then Forfait's to a tenth of a per cent, but the great lateen is 79 m² and the mizen 26 m²,
   both under her design's own bands (100 to 140 and 30 to 45 m², JUDGEMENT). The other three
   readings fail Forfait's total:
   - the great lateen's clew at the mizen's foot, 272.0 m² (+25.9%);
   - Chapman's 55 degrees with the clew at the main's foot, 181.4 m² (-16.0%);
   - Chapman's 55 degrees with the clew at the mizen's foot, 262.5 m² (+21.5%).

   Is the reading right, or does p. 121 read otherwise on its page? I cannot read it: the note is
   OCR.
2. **The mizen's clew at its own mast's foot**, its sheet led to the outrigger 10 m aft. That is
   the rule taken alike; the watercolour shows the clew out at the outrigger (for the eye only).
   With its clew at the outrigger's end at the taffrail's height the mizen would be 55.5 m².
3. **T-2** may not stand after A8 either: she makes less to windward than the merchant brig by
   the polar. A8's tuning of the lateen row is where it is settled.
4. **Her watch by night.** I took out the bilander's (C2) six for heaving to and filling away
   (her commit b4e814c): it was unmeasured for her, and a pin holds that section to the bilander.
   Whether a watch of hers begins a heave-to by night is to be measured when asked.
5. **The tréou's yard.** It is set flying (its sail sent down when taken in), and the engine keeps
   the yard aloft as a crossed yard for classing either way. A5's predicate must read her topsail
   the same with the tréou's yard up or not (her design's §5.1a); today the yard is always there.
6. **Her names**: the `spanish` list for the Provençal trader, by the brief's word, where her
   design's §6.4 had `french` by default. The list makes her read as Spain's with no nation given.
7. **Her slow tests**: `tests/conftest.py` sets the tier and is not mine. None of her tests
   needs a `SLOW_TESTS` entry: the longest, truth 7-688, takes 2.5 s (§9).
10. **For the viewer (the stop rule): the 44 cases of `tests/test_view_geometry.py` on her
    files.** That file is the viewer's (the plan's §7.1), and I have not edited it. None is a
    fault of her files that is mine to mend. Each wants either her row in one of its measured
    tables, or the viewer's reading of a whole lateen with its cut, which no file carried before
    (V1: her design's §10). The cases are listed in §9. Her files are sound to the generator, the
    form's check and `check_viewer_guns`; the viewer draws her today without a NaN in the hull
    cases that pass.
8. **The fisherman** waits on a Gulf of Lion fishing-grounds file, by the card. No gear or
   description of hers is written.
9. **Words outside her files**, for A2: her wear's and heave-to's "after yards" and "after
   braces" (§3). They are mended on the package's branch, which I have not merged.

## 7. The pictures

I took none: a cloud session has no browser. The coordinating session takes them by the plan's
§8.0: 800 × 600 and 960 × 720; abeam to leeward, on the quarter, ahead and astern, furled and
under plain sail; her own states; beside the cutter at one scale and her hull alone beside the
cutter's with her rung letters; heeled 10 degrees from windward. **For the eye on them:**
- the great lateen's car stands at the stem head (x 10.38, 4.10 m above her water), its peak
  high over the stern at (-9.13, 17.74);
- its clew is at the main's foot, so the sail is a long narrow triangle under the yard;
- the beak is level to its eye, the berthelot at 10½ pieds;
- the waist bulwark, the sharp stern and the wale awash amidships;
- the coastguard's four ports a side;
- the viewer draws her whole lateens by `lugCut` as standing lugs on the lee side until V1.

## 8. Each moved pin

Each is in `docs/dev/TuningNotes.md`, "Package 90, the tartane", old beside new.
- **Step 1:** `tests/test_probes_90.py::test_the_lateens_cut_is_a_docstring_alone_until_the_tartanes_builder_fills_it`,
  restated for the filled cut (`..._filled_by_the_tartanes_builder_has_no_build_and_no_modules_row`).
- **Step 2:**
  - `tests/test_profile.py`'s `MODULE_FILES`, her row;
  - `tests/test_probes_90.py`'s stub test, her module built (`BUILT_MODULES`);
  - `tests/test_schooner_mast.py`'s eighteen files, now twenty (renamed);
  - its gale's list of fore-and-afters, with her two;
  - truth 7-190's rows (her row: 14.53 degrees, one port) and its count of armed files, ten;
  - `tests/test_subtypes.py`'s `TABLE`, her two rows;
  - `tests/test_profiles.py`'s `SAME_HULL_BY_INTENT`, her pair by the owner's Part E answer.
- **Found by the fast tier whole on b4e814c** (commit ecf6180):
  - truth 7-700's files, now the eighteen of `_MUSTERED_BEFORE_119` and her two, mustered by
    package 119's rule alone and held to its purpose (4 and 3; 15 and 14);
  - truth 7-701 reading exactly the eighteen it names;
  - `tests/test_neufchatel.py`'s `ROLE_BY_INTENT` and own roles, her two rows (a merchant; the
    revenue's).

  The schooner's-mast gale list, the pair check, 7-700, 7-701 and the *Neufchatel*'s row test
  are not named by the plan's §10.4. Each is a list of the files or the rows, moved because the
  files grew.

**Two mends of my own files, found by the same run** (ecf6180, at their cause):
- her traced frames' heads put on her rail (Pages §5.1: the frames cut at the profile's rail;
  the plate's rounding left them up to 2 cm off, and aft 7's cut at the lower rail beside the
  bulwark's end);
- her breadth's rail half-breadth taken from the traced frame's head, the one measure.

Her design's **"lateens" group comes out of her file** until A1b. Truth 7-625 holds the
standing book's sail families (`freesail/standing/book.py`, not mine) to the files' one-word
groups, "a new one is added on purpose", and the group serves A1b's orders alone.

**Her own `hands:` taken out** (b4e814c): see §6, question 4.

## 9. Each test set, and the base comparison

All from the repository's root:

```
python -m pytest -n 4 -p no:cacheprovider -o addopts="--dist loadgroup"
```

**The base, the fast tier whole on f6f26f8a**, in a clean worktree. It ran in six chunks, each
with its own `--junitxml`, so that none passed the container's two-hour limit for a background
run: `tests/test_known_truths.py` in three parts by test function, and the other 182 files in
three. **8,471 passed, 8 skipped and 1 xfailed: 8,480 tests, none failed.** A first base run
whole was stopped at the limit, a third of the way through.

**The final, the fast tier whole on ecf6180**, the same six chunks with `tests/test_tartane.py`
added to the last. **8,644 tests: 8,591 passed, 9 skipped and xfailed (the base's own), and 44
failed.** Compared test by test (the two junit sets, by node id):
- **no test of the base changed its outcome**;
- **2 tests are the base's only**, each a pin renamed and restated (§8):
  `test_probes_90::test_the_lateens_cut_is_a_docstring_alone_until_the_tartanes_builder_fills_it`
  and `test_schooner_mast::test_the_guard_reads_eighteen_files_...`;
- **166 tests are new**: her own 23 in `tests/test_tartane.py` (the lateen cut's eight, her
  files' thirteen, truths 7-681 and 7-688) and 143 file-parametrised cases of the suite on her
  two files. 122 of the 166 pass; the 44 that fail are all `tests/test_view_geometry.py`'s on
  her files (below);
- **no new test takes 5 s or more** (the slow tier's threshold): the longest, truth 7-688, takes
  2.5 s, so `tests/conftest.py`'s `SLOW_TESTS` wants no entry of hers.

**The run before it, on b4e814c**, failed 53. The 44 below, and five tests of the base:
- truths 7-625, 7-700 and 7-701 and the *Neufchatel*'s row test, each mended or moved in
  ecf6180 (§8);
- truth 7-284, the pace of the tide's blend: 0.0101 s against 1.25 × 0.0077. It is a timing
  measure, failed under the chunk's load, passes alone twice and passed in the run on ecf6180,
  and reads nothing of hers.

**The slow tier of her files**: `--slow tests/test_tartane.py tests/test_probes_90.py`, 113
passed in 5.9 s. Neither file has a test in the slow tier. (This run left out the four
anchorage cases on her ship files in `tests/test_take_up_at_anchor.py`. §10 runs them.)

**The targeted runs on the way** (no junit kept for the comparison):
- the file-iterating files on 0dbd4fc: 1,562 passed and the base's xfail; 2 failed, both mended
  in b4e814c (the pair check; her `hands:`);
- each moved pin's file after its move.

**At each step's end** (the plan's §7.3):
- `python tools/gen_ships.py <scratch>` and a `cmp` of the eighteen committed files, byte for
  byte at every step, her two the only files that changed;
- `load_ship` on both her files;
- `python tools/check_viewer_guns.py` on both, clean (the trader no armament; the coastguard's
  12 guns, 8 in ports and 4 on the rail);
- ruff clean, no Python line over 100, LF only (`git diff | tr -cd '\r' | wc -c` is 0).

**The viewer's 44 cases on her files, as they stood on ecf6180** (`tests/test_view_geometry.py`,
the viewer's file: not edited then, under the stop rule; §10 has them after it was widened to
me). Two of each, except where four:
- **her row in a table of measured figures, or her file in a list of the files without a part**:
  - her round stern with no transom, no lights and no galleries, as the lugger's:
    `test_every_file_draws_a_closed_hull_with_no_nan` (`RIGHTLY_WITHOUT`'s gallery), `test_the_transom_runs_from_the_knuckle_to_the_taffrail`,
    `test_the_transom_stands_at_the_taffrail_and_transom_hb_m_its_foot_rounded_up`,
    `test_the_stern_lights_are_seen_only_from_abaft_the_transom`,
    `test_each_gallery_and_band_of_lights_lies_at_its_place`,
    `test_the_stern_seen_from_abaft_is_painted_after_the_rest_of_the_hull`;
  - her éperon, level and under her rail at the stem, with no jib boom:
    `test_the_bowsprit_stands_from_the_stem_head_its_length_up_to_its_ends_height` (`BOWSPRIT_DRAWN`),
    `test_a_level_bowsprit_is_rooted_at_the_rail_at_the_stem_beside_its_sheets_height` (`LEVEL_ROOT_M`),
    `test_on_a_hull_drawn_from_her_profile_the_yards_hang_from_the_bowsprit_as_it_stands` (the head chain's `jib_boom`);
  - her side's bands: `test_each_tier_of_ports_cut_in_the_side_is_drawn_as_a_band` (`TIERS_IN_THE_SIDE`), `test_a_band_follows_the_drawn_side_between_its_two_heights` (`CHORD_OFF_THE_SIDE_M`);
  - no boom: `test_every_boom_on_a_drawn_hull_is_topped_up_to_clear_her_taffrail` and
    `test_every_other_gaff_sail_keeps_the_foot_and_the_bundle_it_was_drawn_with` (`NO_BOOM`);
  - her lines on the rail: `test_the_lines_come_down_on_the_rail_as_the_game_serves_her`
    (`LINES_ON_THE_RAIL`'s and its kin's rows by file);
- **the viewer's drawing of a whole lateen with its cut**, which no committed file carried
  before (V1; her design's §10):
  - her great lateen's one sheet, its lead from the clew at the main's foot:
    `test_each_line_that_comes_down_ends_on_her_drawn_rail` (four),
    `test_a_stay_to_the_stem_lands_on_the_stem_head_and_its_sails_foot_stands_over_the_rail` (four),
    `test_with_no_profile_the_lines_come_down_as_before` (four);
  - the fixed frame across states, her great lateen's peak high over the stern:
    `test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number` (`OVER_THE_FRAME`) and
    `test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states`.


## 10. The viewer's cases, after the widening (the coordinating session's message; the lead's nudge 32, item 1)

`tests/test_view_geometry.py` was widened to me for her rows, "as every hull's builder must at
her file". Commit b33adfd. Of the 44 cases that failed on her files:
- **16 now pass**;
- **12 are no longer run on her files**, because her named rows (below) say she rightly has
  none of the part they test: her transom, her galleries and lights, her stern's layer, and the
  yards under a jib-boom;
- **16 remain**, each the viewer's.

Two cases that passed before are also no longer run on her: those of
`test_the_stern_stays_under_a_rig_figure_abaft_and_nearer`. They follow from the stern row by
the file's own derivation. `STERN_LAYERED` takes a file with a transom or lights, and she has
neither, as the lugger has neither.

**(a) Her rows**, each measured by the file's own probes on her files:

| Table | Her row |
|---|---|
| `BOWSPRIT_DRAWN` | (0.902, 0.0), each file |
| `LEVEL_ROOT_M` | (3.67, 3.67, 2.85): the root drawn at her bow rail at the stem, the stem head by the rule, and her plate's beak level at 2.85 m (Pages §5.4) |
| `TIERS_IN_THE_SIDE` | the trader none; the guarda-costa `{"upper"}` |
| `CHORD_OFF_THE_SIDE_M` | 0.032, each file |
| `LINES_ON_THE_RAIL` | the jib's two sheets and the two lateens' one sheet each |
| `STEM_TACKED` | none: her jib and storm jib are cut from her file's corners, as the 64's are |

**(b) The parts she has none of, as named rows with their reasons:**
- `SHARP_STERNED`, her two files: Chapman's plate draws a sharp stern, the planking closing on a
  raked post, with no transom, counter, gallery or light (Pages §5.5). Her files join
  `RIGHTLY_WITHOUT`'s gallery, light and transom rows, and the transom's case keeps them out as
  it keeps the lugger and the bilander. The trader alone joins its band row: she files no ports.
- `NO_BOOM`: her two files (no part of hers is on a boom).
- The yards under the bowsprit: her two files kept out beside the cutter, the lugger and the
  smack. Her éperon carries the berthelot and no jib-boom (her design's §4.3).

**The throwaway check.** I made a copy of her file under a name no row names
(`data/ships/zz-forgetful.yaml`, never committed, and deleted after the run). Its run was
`tests/test_view_geometry.py -k forgetful`: **22 failed and 31 passed**. Those 22 are the same 22 cases
each of her files failed before her rows, the stern's, the boom's and the jib-boom's among them.
Nothing passes for a hull that merely leaves a part out, and nothing was invented for her.

**Found and mended in her own file:** her storm jib had no corners. The viewer therefore cut it
on her jib's stay, which it lands on her stem head, and its tack stood 0.53 m off her side. It now
files its corners, two-thirds of the jib cut alike about the jib's tack at the berthelot's end
(Steel 1794 p. 190). This mend passes the four cases of
`test_a_stay_to_the_stem_lands_on_the_stem_head_and_its_sails_foot_stands_over_the_rail`, which
§9 had put under V1. They were mine, not the viewer's. Nothing else of her files moved, and the
eighteen are byte for byte.

**(c) The 16 that remain, and why** (exactly these; none edited, none loosened):

| Case (each on both her files) | Cases | Why |
|---|---|---|
| `test_each_line_that_comes_down_ends_on_her_drawn_rail` (both tacks) | 4 | the whole lateen's sheet: drawn as a standing lug's, a metre abaft the clew, where the case's rule for a lateen is two. **V1** |
| `test_with_no_profile_the_lines_come_down_as_before` (both tacks) | 4 | the same sheet, with no profile. **V1** |
| `test_the_lines_come_down_on_the_rail_as_the_game_serves_her` | 2 | the same sheet, as served. **V1** |
| `test_the_frame_is_unmoved_across_states_and_no_figure_lacks_a_number` | 2 | dressed, her great yard's penne stands 0.15 m over the fixed frame. The lugger's lugs, drawn by the same cut, are `OVER_THE_FRAME`; how the frame holds a whole lateen's yard is **V1**'s |
| `test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states` | 2 | furled, the viewer lays her yard and sail on deck as a lowered lug's, so her bounds move from furled to set. A whole lateen's yard stays aloft furled (her design's §5.4 item 7). **V1** |
| `test_a_level_bowsprit_is_rooted_at_the_rail_at_the_stem_beside_its_sheets_height` | 2 | her beak runs level **under** her bow rail: the plate's 2.85 m against the rule's root, 3.67 m at the rail, 0.82 m over the case's 0.15. **Not V1**: the viewer's rule for a level spar, which roots every one at the rail at the stem. Her row records the figures; I did not touch the rule |

Two figures of the drawing beside them, for the viewer's eye:
- the stay her jib sets on is drawn to her stem head, while her jib is drawn from its corners,
  its tack 3.41 m farther out at the berthelot's end;
- her topsail's sheets are drawn to the tréou's yard's arms in plain sail, where her design has
  no yard crossed under the topsail until the tréou is set (decision 9).

**The tests, on b33adfd** (the same six chunks and command as §9's):
- **The fast tier whole: 8,630 tests. 8,605 passed, 9 skipped and xfailed (the base's own),
  and 16 failed.** Compared test by test with the base on f6f26f8a:
  - **no test of the base changed its outcome**;
  - the same 2 tests are the base's only (§9);
  - 152 tests are new, and the 16 that fail are exactly the 16 of (c);
  - no new test takes 5 s or more.
- **Against the run on ecf6180:**
  - 16 cases went from failed to passed;
  - 14 left her parametrisation: the 12 above, and the 2 stern-layer cases that passed;
  - nothing else changed.
- **The slow tier of her files:** `--slow tests/test_tartane.py tests/test_probes_90.py` and
  `test_take_up_at_anchor.py`'s `test_a_ship_taken_up_asleep_at_her_anchor_is_laid_at_it_on_every_hull`
  on her two files, **117 passed**. **A correction to §9:** its slow-tier run left out those
  four anchorage cases. They are the only slow cases on her ship files, found by collecting
  `--slow -m slow` (587 tests) and searching the node ids. The other 113 are §9's.
- **At this step's end:**
  - `python tools/gen_ships.py <scratch>` gave all twenty files byte for byte as committed;
  - since f6f26f8a, only her two ship files have changed;
  - `load_ship` and `check_viewer_guns` are clean on both her files;
  - ruff is clean, LF only, and no Python line is over 100 characters.
