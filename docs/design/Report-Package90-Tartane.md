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

**The lead's nudge 38 (§12).** The trader now takes the `french` list of names, and the
guarda-costa keeps the `spanish` one. Truth **7-695**, her watch by night, is written. Her
larboard watch's three call all hands for heaving to and filling away, and her starboard
watch's four, exactly half, do not. The fast tier whole on 8998c08 changed no test of the base:
four tests are new, one renamed pin is gone, and the same 16 viewer cases fail.

**The lead's nudge 41 (§13).** Her bill is mended to her design: four at the forecastle and three
in the afterguard, so each watch has three able seamen, and the boy goes to the starboard. Her
words now say so. Truth 7-695's counts hold, four and three. The fast tier whole on 3a5c96b
changed no test of the base, and one test is new. Her wear from 292.5 degrees no longer comes
round on the new bill: the knife's edge of §3, recorded.

**The owner's note on her topsail, and the lead's nudge 42, point 5 (§14).** Her file already
carries decision 9: the tréou is set flying, on deck with its yard in plain sail and at her
start, swayed up when set and sent down when taken in, as measured. The askew foot is the
viewer's: `squareCut` takes the tréou's yard on deck as the yard below. Its mend is one
condition in `client/projection.js`, V2's, not mine; nothing in the tree moved.

**The lead's nudge 88: her topsail's foot and her lateen yard (§15).** The foot's mended
arithmetic gives her topsail 0.03 m over her lateen yard, and by her file's cut it is none: the
topsail is cut down to the hounds, where the lateen yard is slung. The pole's head (Forfait's 26
pieds) and the lateen's hoist (Forfait p. 121, as read) stand. The topsail's depth is mine, the
cutter's rule with no source behind it, and it does not stand. §15.3 gives the re-cut for the
lead to rule, owed with her hash.

**The branch.** `…/pkg-90-tartane`, cut from f6f26f8a (`git log -1` checked). I merged
nothing from `…/pkg-90`, so my base and my final run are on the same tree. Nothing was
rebased or forced.

## 1. The commits

| Step | Commit | Files |
|---|---|---|
| 1, `lateen.py` alone | `bfec7fa3307162bc7fc23845b60cb6784ca903c9` | `tools/ships/lateen.py`; `tests/test_tartane.py` (its eight tests); `tests/test_probes_90.py` (the stub's pin restated); `docs/dev/TuningNotes.md` ("Package 90, the tartane", step 1) |
| 2 to 4, her module and her files, and two mends found by the tests | `0dbd4fc933df9b37adac5fb8b8dbe2ab318d6dfa`; mends `b4e814c7e9bc99d285d6b57c7644f3fd820877b5` and `ecf61800db82ce5cc3bb3de31b61a3b69e185b5d` (§8, §9) | `tools/ships/tartane.py`; `data/ships/tartane.yaml` and `data/ships/coastguard-tartane.yaml` (generated); `data/people/tartane.yaml` and `data/people/coastguard-tartane.yaml`; `freesail/world/ships.py` (her two `DESCRIPTIONS` rows and her words); `freesail/world/captains.py` (the coastguard's `SIZE_RANK` row); `tests/test_tartane.py`; the moved pins (§8); `docs/dev/TuningNotes.md` (step 2 and the mends) |
| her rows in the viewer's tables, and her storm jib's corners (§10) | `b33adfd69facb88dfc007b9e4cf37e61b32b0119` | `tests/test_view_geometry.py` (widened to me, §10); `tools/ships/tartane.py`; her two ship files (generated); `docs/dev/TuningNotes.md` |
| the lead's nudge 38: her names, and truth 7-695 (§12) | `07aed62807521f61749c169e4df57b3fec6f7c73`; `8998c087f23f4cd2cf3b5e195c17962ec746684f` | `tools/ships/tartane.py`; `data/ships/tartane.yaml` (generated); `data/people/tartane.yaml` (its header); `tests/test_tartane.py`; `docs/dev/TuningNotes.md` |
| the lead's nudge 41: her bill mended to her design (§13) | `3a5c96bbf952358403bdef2dea57f1327ae688e1` | `tools/ships/tartane.py`; `data/ships/tartane.yaml` (generated); `tests/test_tartane.py`; `docs/dev/TuningNotes.md` |
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
(The lead's nudge 41 mended her bill: §13.2 gives the figures that moved, her wear from 292.5
among them.)

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
- **7-695** (the lead's nudge 38, question 4), her watch by night. A watch of hers too few on
  deck calls all hands to heave to and fill away, by order and by a standing order, and is
  piped down (§12.2). Its counts held when her bill was mended at the lead's nudge 41 (§13.2).

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

   **Answered by the page (77ead1d0).** The coordinating session read Forfait p. 121 on its page
   image, IA leaf n166 (`pages-tartane.md` §1.3 at 77ead1d0 on `…/pkg-90`). The page puts the
   clew on the deck at the mast's foot with the yard fully peaked (figs. 35 to 38), and the car
   tacked at the stem (fig. 35). The design's reading, taken literally, is therefore the page's,
   and the cut stands as filed. The *Humble*'s own ends in Table II lie under the page's general
   band, and her row stands. Leaf n179 gives her surface as 2,237½ square pieds, 236.1 m² at the
   pied du roi, Forfait's total as §2 has it. Nothing of hers changes.
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
    files.** (The file has since been widened to me for her rows, and 16 cases remain: §10.) That file is the viewer's (the plan's §7.1), and I have not edited it. None is a
    fault of her files that is mine to mend. Each wants either her row in one of its measured
    tables, or the viewer's reading of a whole lateen with its cut, which no file carried before
    (V1: her design's §10). The cases are listed in §9. Her files are sound to the generator, the
    form's check and `check_viewer_guns`; the viewer draws her today without a NaN in the hull
    cases that pass.
8. **The fisherman** waits on a Gulf of Lion fishing-grounds file, by the card. No gear or
   description of hers is written.
9. **Words outside her files**, for A2: her wear's and heave-to's "after yards" and "after
   braces" (§3). They are mended on the package's branch, which I have not merged.

**Questions 2 to 10 were ruled at the lead's nudge 38**, in the note at the end of
`docs/dev/M7-WorkPackages.md` on the trunk at 8a78bd2a. Two were mine to build, and §12 has
them: question 4, her watch by night (truth 7-695), and question 6, the trader's names from
the `french` list. Question 7's longest test is now truth 7-695, at 12.4 s (§12.2). The rest
are settled or noted there, and nothing of them is mine to change.

**The lead answered §12 at nudge 41**, in the same note on the trunk at bb66331a. Point 3 was
mine, her complement's words against her bill, and §13 has it. Point 1 leaves the starboard's
four as the engine has it. Point 2, 7-695's "and under way", is owed when A5 and her files are
both on `…/pkg-90`.

**Owed together, when A1a and A5 and her files are on `…/pkg-90`** (nothing built now):
- truth 7-695's "and under way" clause (the lead's nudge 41, point 2);
- the lead's nudge 43 (trunk d6159090), pinned with her case. On a rig of whole lateens the
  heave-to's check asks whether she has a yard to bring her to, by what she carries, not by what
  is set. With her topsail furled, `heave to` is refused in the words "No head sail is set to haul
  to windward, nor a topsail to lay aback."; with it set, she heaves to.

**Owed with her hash when A4 and her files are on `…/pkg-90`** (the lead's nudge 44, trunk
dd09a54a, read whole; nothing built now). Hers is the first file that tows:
1. `freesail/world/movement.py`, `_in_the_boat_at_the_side`: a person in a towed boat while she
   is hauled alongside is "in the boat at the side", as one in a boat hoisting out is. The one
   line, `boat.phase not in dealings.OUT_PHASES`, with a proof.
2. `freesail/combat/hits.py`, "stove on the booms by a shot": said of a towed boat, it is words
   only. She is stove where she tows, with no change to what is hit or how often. This comes after
   A3 is on the trunk, and A3 is merged there now (2e7b8ce2; the lead's nudge 45), so it is clear
   to build with her hash.
3. The clearing for action (`freesail/evolutions/action_scripts.py`): no clearing time for boats
   already astern, and the line does not say they were got out. A ship with a boat on the booms
   keeps today's time and words, to the digest.
4. Her file's known list: no order veers a towed boat long or hoists her in on passage (her
   design's §11, "hoisted in, or veered long, in a blow"), with her drag past her hull speed.
   Listed for the ship and her people's milestone.

Items 1 to 3 are engine files outside my §7.1 row, so I will build them on the lead's nudge 44
alone. **Item 4's place, answered by the lead's nudge 45** (trunk 6038f23a, read whole). No ship
file carries a known list, so it goes in two places:
- her ship file's note on her boat, written through `tools/ships/tartane.py` and the generator.
  It says that no order veers the boat long or hoists her in on passage, and gives her drag past
  her hull speed;
- one line in her design's open list (`docs/design/Design-Ship-Tartane.md`) pointing at that note.

Both are owed with her hash, beside the other towing items. Also noted there, and not mine: a
towed boat with no file of her own puts no drag on the ship, and the generator may refuse `towed`
on such a boat when her files come.

**Owed with her hash, as the lead rules on §15.3** (the lead's nudge 88): her topsail cut clear
above the lateen yard's slings.

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

## 11. The lead's nudge 35: authorship and the Harbour

**Authorship.** Step 1's commit, bfec7fa, keeps the author I set by hand (§1). It was not
rewritten and nothing was forced. No later commit sets its author, and none will.

**The Harbour.** My tests do not patch a loader or count loads, and none builds a Harbour:
- `tests/test_tartane.py` runs the generator in a subprocess and imports her module by path;
- its `load_ship` calls only read her two files;
- my other edits to tests are rows in tables and lists.

**The harbour and browser tests on a tree with her files.** None failed in any run:
- the fast tier's 43 (`tests/test_harbour.py` and `tests/test_browser_probe.py`) passed in the
  base and in each of my runs: on b4e814c, on ecf6180 and on b33adfd, and in the targeted run
  of the file-iterating files;
- the slow tier's 18 harbour, browser and Harbour-truth cases, collected by name from
  `--slow -m slow`, were run on 675fd50 and then on the base f6f26f8a in a scratch worktree.
  **18 passed on each.**

## 12. The lead's nudge 38: her watch by night and her names

The lead ruled questions 2 to 10 at nudge 38, in the note at the end of
`docs/dev/M7-WorkPackages.md` on the trunk at 8a78bd2a, which I read whole. Two were for me to
build: question 4, her watch by night, and question 6, her names. The rest are settled or noted
there, and nothing of them is mine to change. I merged nothing; the tree is mine as it was.

| What | Commit | Files |
|---|---|---|
| Question 6, her names | `07aed62807521f61749c169e4df57b3fec6f7c73` | `tools/ships/tartane.py`; `data/ships/tartane.yaml` (generated); `data/people/tartane.yaml` (its header); `tests/test_tartane.py`; `docs/dev/TuningNotes.md` |
| Question 4, truth 7-695 | `8998c087f23f4cd2cf3b5e195c17962ec746684f` | `tests/test_tartane.py`; `docs/dev/TuningNotes.md` |
| this section | the commit that adds it | `docs/design/Report-Package90-Tartane.md` |

Each commit's author is as the cloud gives it, and neither has a trailer.

### 12.1 Question 6: the trader's names from the `french` list

The trader *Saint-Pierre* now takes the `french` list, her design's default (§6.4), and the
guarda-costa *San Pedro* keeps the `spanish`. Her module gives each role its list, and the
generator (`python tools/gen_ships.py`) wrote the files. `data/ships/tartane.yaml` moves in two
lines, its names line and that line's note. The other nineteen files are byte for byte (`cmp`),
the guarda-costa's among them.

**Passing on 07aed62:** truth 7-680, the names' guard (`test_every_names_list_has_its_nation`)
and her own tests, 27 passed together. A new case holds the ruling's purpose. With no nation
given, the trader reads as France's and the guarda-costa as Spain's, and every sailor's names
come from their file's list.

**Two things found, recorded, and not mine to change:**
- The muster writes every list's given names with an English muster book's short forms
  (`freesail/crew/muster.py`, `GIVEN_ABBREVIATIONS`). So the `french` list's Charles becomes
  "Chas.": her first muster at seed 7 has a Chas. Lecoq. The lugger's French list meets the same.
  My case compares names as the muster writes them, through its own `abbreviate`.
- The `french` list's names are of Brittany and Normandy (Kerjean, Kervella, Gosselin): the
  lugger's list, not Provence's.

### 12.2 Question 4: her watch by night, truth 7-695

**The number.** 7-681 to 7-689 are T-1 to T-9's, each written or waiting, so none is free. The
truth takes **7-695 from the spare** (the plan's table on `…/pkg-90`: 7-695 to 7-699). No
branch of package 90 and not the trunk uses it.

**Measured** as truth 7-704 measures the merchant brig: the trader off the Lizard at 02:00, seed
7, a westerly of 14 kn. Her bill draws four able seamen to the starboard watch, and two and the
boy to the larboard. Her design's §6.1 gives "watches of three seamen (four with the boy)", so
the counts on deck are its counts. Heaving to and filling away want twelve by their files,
clamped to the eight her company can give: the seven of the watches and the cook. A watch under
half of that calls all hands (`too_few: all hands`, package 119).

| Her `hands:` | The starboard's four | The larboard's three |
|---|---|---|
| none, as filed | begins each itself, short, 4 of 8, and no one is called: hove to in 103 s (104 by the standing order), filled away in 181 (182) | **all hands called** once for each: hove to in 76 s (77) and piped down; filled away in 181 (182), the watch below up at 90, and piped down |
| the bilander's six (0dbd4fc; taken out at b4e814c), measured on this tree | begins each itself, short, and no one is called: hove to in 82 s (83), filled away in 181 (182) | begins each itself, short, and no one is called: hove to in 112 s (113), filled away in 181 (182) |

Nothing waits and nothing fails either way. **The six are not put back:** they would have no one
call all hands, which the truth asks for. **Her own is none,** the file's twelve under package
119, as she stood. The pin in `tests/test_mends_75.py` that holds the section to the bilander is
untouched, since nothing of hers needs it moved.

**Truth 7-695** holds both watches as measured, on 8998c08:
- the larboard's three: by order and by a standing order (to lie to over ten knots, then to fill
  away under eight, the wind falling to six), all hands are called once for each, she is hove to
  and filled away, and the hands are piped down with the larboard watch on deck;
- the starboard's four: half of eight, so not too few. The watch begins each itself, short, four
  of eight, and nobody is called or piped down.

It takes 12.4 s, over the slow tier's threshold of 5 s, as 7-703 (15.8 s) and 7-704 (15.7 s)
do. `tests/conftest.py`'s `SLOW_TESTS` is not mine, so it runs in the fast tier beside them.

**For the lead: the starboard's four.** The ruling has all hands called for "a watch of hers". On
her larboard watch they are; on her starboard they are not, because four is half her clamped
eight and the engine calls all hands only under half (`hands.too_few_on_deck`). No figure a ship
file gives can change it, because her company's clamp holds the want at eight. Whether a watch
at exactly half should call all hands for a manoeuvre is the engine's rule, not hers.

**Recorded, not asserted: filled away, she is not under way.** By the player's order, the wind
at 14 kn, she lies 20 to 45 degrees off the wind after "Filled away ... steering SSW (202°)".
She wanders between 226 and 250 degrees at 0.8 to 1.3 kn for the thirty minutes traced. By the
standing order, the wind fallen to six, she makes 0.38 kn at 900 s. The merchant brig in the same
world steadies on 202.5 at 4.17 kn within 300 s.
- **The cause:** her heave-to hauls up her topsail as a course ("Hauled up the courses.", read on
  this tree), and filling away does not set it again. Left under her two lateens and her jib,
  she cannot bear away. The same happens with all hands up first, and with `steer 202` given
  again.
- **With `set the main topsail`** after filling away, she steadies on 202 to 203 degrees at
  3.77 kn by 800 s after the order.

It is the engine's reading of her topsail, which A5 changes, so her truth asserts no speed.
7-704's last clause ("and under way") waits on A5 for her.

**One more found:** my complement words say "six able seamen in two watches of three". The bill
draws four able seamen to the starboard and two with the boy to the larboard. At seed 7 it deals
each station's hands alternately from the starboard: her forecastle's three, and her
afterguard's four with the boy among them. The counts on deck are her design's either way, and
the truth reads them, so I have not moved her stations. Recorded for the lead. (The lead's
nudge 41 had it mended, and §13 has the mend. The watches are the muster's rule 3, not the
seed's: every seed deals them so.)

### 12.3 What moved, old beside new

- **Her trader's file**, `data/ships/tartane.yaml`: `names: spanish` becomes `names: french`, with
  its note. Nothing else of the twenty files moved.
- **The names pin** in `tests/test_tartane.py`:
  `test_her_companies_ten_and_thirty_four_with_spanish_names` becomes
  `test_her_companies_ten_and_thirty_four_the_trader_french_the_guarda_costa_spanish`. Old
  (71dd278): both `spanish`. New: `("french", "spanish")`.
- **New:** `test_each_of_her_files_reads_as_its_lists_nation_with_no_nation_given` (two cases),
  and truth 7-695.
- **Her people file's header** names the `french` list.
- **TuningNotes**, her section: the nudge 38 measurements above. I also corrected a count of mine
  there: the great lateen's sheet accounts for 10 of the viewer's 16 remaining cases, not 12.

### 12.4 The tests, on 8998c08

- **The fast tier whole** ran in the same six chunks as §9 and §10. I compared it test by test
  with the run on b33adfd, the base on the same tree: between b33adfd and 71dd278 only this
  report changed, and I merged nothing.
  - **8,633 tests: 8,608 passed, 16 failed, 9 skipped and xfailed.** On b33adfd: 8,630 tests,
    8,605 passed, the same 16 failed and the same 9 skipped and xfailed.
  - **No test of the base changed its outcome.** The only differences:
    - the old names pin is gone (it passed on b33adfd);
    - four tests are new, all passing: the renamed pin, the two nation cases and truth 7-695.
  - **The 16 that fail are §10's 16 viewer cases**, the same node ids in both runs.
- **The harbour and browser tests (nudge 35):** none failed.
  - The fast tier's 43 passed in both runs.
  - The slow tier's 18, the list §11 ran, passed on 8998c08.
- **The slow tier of her files:**
  - `--slow tests/test_tartane.py tests/test_probes_90.py`: **116 passed**, §9's 113 and the
    three new tests;
  - her four anchorage cases (§10) passed, so **120 in all**.
- **At this step's end:**
  - `python tools/gen_ships.py <scratch>` gave all twenty files byte for byte as committed;
  - ruff is clean;
  - every file is LF only;
  - no added Python line is over 100 characters;
  - no added line names a model or its maker.

**A correction to §6.** Its answer to question 1, as committed at 71dd278, wrote the package's
branch in full. It now reads `…/pkg-90`, as §1 writes it, so that no line names a model's maker.

## 13. The lead's nudge 41: her bill mended to her design

The lead answered §12 at nudge 41, in the note at the end of `docs/dev/M7-WorkPackages.md` on the
trunk at bb66331a, which I read whole. One point was mine to build, point 3: her complement's
words must say what her bill draws, for a player reads the muster.
- **Point 1**, the starboard's four: it stays as the engine has it, one rule for every ship.
- **Point 2**, filled away and not under way: it is owed later. When A5 and her files are together
  on `…/pkg-90`, truth 7-695 takes 7-704's "and under way" clause, measured, and this report gives
  the figure.
- **Recorded by the lead, not mine:** the muster's short forms on French names, and the Breton
  and Norman `french` list.

The note also asks for the trunk to be merged before the next hash. That merge is the coordinating
session's, into `…/pkg-90`, and my brief lets me merge only that branch; its message says I need
not have it for this. I merged nothing, so the tree is mine as it was.

| What | Commit | Files |
|---|---|---|
| Point 3, her bill mended to her design | `3a5c96bbf952358403bdef2dea57f1327ae688e1` | `tools/ships/tartane.py`; `data/ships/tartane.yaml` (generated); `tests/test_tartane.py`; `docs/dev/TuningNotes.md` |
| this section | the commit that adds it | `docs/design/Report-Package90-Tartane.md` |

Its author is as the cloud gives it, and it has no trailer.

### 13.1 Which, and why: the bill mended to her design

- **The design is what is meant.** Her design's §6.1 says it twice: six seamen, "able ..., three
  a watch", and "her watches of three seamen (four with the boy) and an officer". My complement's
  words said the same. The bill did not, because of my stations.
- **The cause was my stations, not the words.** The design gives no split of her seamen and the
  boy between the forecastle and the afterguard; three and four were my judgement. The muster
  watches each station's hands alternately, and the odd hands of odd stations go by turns, the
  first to the starboard (`freesail/crew/muster.py`, rule 3). So the forecastle's three went
  starboard, larboard, starboard. The afterguard's four, the boy last, went starboard, larboard,
  starboard, larboard. The starboard had four able seamen and the larboard two with the boy.
- **The mend: her stations four and three.** The forecastle's four go two a watch. The
  afterguard's two able seamen go one a watch, and its odd hand, the boy, goes to the starboard.
  Each watch has three able seamen, and the starboard has the boy as well.
- **Why four forward and not two:** two at the forecastle and five aft would give the same
  watches, by number. Her forecastle's words carry the most gear: the jib, the anchors, and the
  great lateen's car and both ourses, the car tacked at the stem. The afterguard keeps the
  sheets, the mizen and the helm. That is JUDGEMENT.
- **The words** now name the boy's watch: "six able seamen in two watches of three, a boy in the
  starboard watch, and a cook". The afterguard's line says how the muster watches them.
- **The generator** wrote the file. `data/ships/tartane.yaml` moves in its complement's note and
  its two stations with their notes. The other nineteen files are byte for byte (`cmp`), the
  guarda-costa's among them.

### 13.2 What moved, old beside new

**Her bill** (old on 8998c08). Each number keeps its name and its skills, which the muster draws
in the books' order. Only s006 to s009 change station or watch.

| | Old: forecastle 3, afterguard 4 | New: forecastle 4, afterguard 3 |
|---|---|---|
| The starboard watch | s003, s005 (forecastle), s006, s008 (afterguard): four able | s003, s005 (forecastle), s007 (afterguard), able, and s009, the boy |
| The larboard watch | s004 (forecastle), s007 (afterguard), able, and s009, the boy | s004, s006 (forecastle), s008 (afterguard): three able |
| Her complement's words | "six able seamen in two watches of three, a boy and a cook" | "six able seamen in two watches of three, a boy in the starboard watch, and a cook" |

**Truth 7-695: its counts held.** The starboard has four on deck and the larboard three, as
before, so its assertions stand unchanged. Only its docstring is restated, for the watches'
new make-up. Its figures (the standing order's in brackets):

| | Old | New |
|---|---|---|
| The starboard's four, short, no call: hove to; filled away | 103 s (104); 181 (182) | 110 s (111); 181 (182) |
| The larboard's three, all hands called: hove to; filled away, all hands up | 76 s (77); 181 (182), up at 90 (91) | the same |
| With the bilander's six, no call on either: the starboard hove to; the larboard | 82 s (83); 112 (113) | 87 s (88); 103 (104) |

The calls do not move. The larboard calls all hands for each and is piped down, and the
starboard calls no one. With the six neither does, so the six stay out. The starboard heaves to
7 s slower, the boy in place of an able seaman.

**A new test:** `test_her_trader_is_watched_three_able_seamen_a_side_the_boy_to_the_starboard`.
It holds her stations at four and three, three able seamen a watch, the boy in the afterguard
and the starboard watch, and her file's words saying so.

**Her other figures**, in §3's harness, each old one measured again on 8998c08 (they are §3's as
reported):
- her polar, truth 7-688's 4.69, 4.35 and 4.86 kn, and her speeds 67.5 and 90 degrees off (4.65
  and 5.80 kn): unchanged. Her helm 67.5 degrees off moves from +0.25 to +0.27 degrees;
- `heave to` from 292.5: hove to in 145 s, now 144; 49.9 degrees off at 0.80 kn at +300 s, now
  49.8 at 0.79; 48.8 at 0.82 at +600 s, now 48.5 at 0.80;
- `tack ship` from 290, 292.5 and 295: 165, 393 and 394 s, now 156, 393 and 394. To windward in
  fifteen minutes: 621, 126 and 50 m, now 625, 130 and 32;
- `wear ship` from the same: 585, 734 and 486 s, now 571, **not worn**, and 482. To windward:
  -21, -149 and 63 m, now -7, -591 and 68;
- the topsail set again after filling away, the larboard by night: 3.57 kn at 600 s, now 3.63;
  3.77 at 800 s, unchanged.

**For the lead: her wear from 292.5 degrees.** On the new bill she no longer comes round from
292.5. "Could not wear: she would not come round." comes at 901 s, and she is left 43 degrees off
at 0.7 kn, her helm hunting. Traced, the two wears run alike to a tenth of a degree for 180 s and
part after 500 s. The bill tips her over §3's knife's edge, as the headings between show:

| From | 291.25 | 292 | 292.5 | 293 | 293.75 |
|---|---|---|---|---|---|
| Old | 640 s | 647 | 734 | 715 | not worn (901) |
| New | 598 s | 643 | not worn (901) | not worn (901) | 474 |

Each bill has a heading in that quarter point from which she will not wear. A1a to A1d change her
going about wholly, so this is recorded, not tuned. No test reads her wear: T-3 waits on them.

### 13.3 The tests, on 3a5c96b

- **The fast tier whole** ran in the same six chunks as §12.4. I compared it test by test with
  §12.4's run on 8998c08, the base on the same tree: between 8998c08 and bdd2227 only this
  report changed, and I merged nothing.
  - **8,634 tests: 8,609 passed, 16 failed, 9 skipped and xfailed.** On 8998c08: 8,633 tests,
    8,608 passed, the same 16 failed and the same 9 skipped and xfailed.
  - **No test of the base changed its outcome.** The only difference is the new test of §13.2,
    which passes. Truth 7-695 passes with its counts held, and truth 7-700, each ship file's two
    watches and each station's share equal or one apart, passes on her new stations.
  - **The 16 that fail are §10's 16 viewer cases**, the same node ids in both runs.
- **The harbour and browser tests (nudge 35):** none failed.
  - The fast tier's 43 (`tests/test_harbour.py` and `tests/test_browser_probe.py`) passed in
    both runs.
  - The slow tier's 18, the list §11 ran, passed on 3a5c96b.
- **The slow tier of her files:**
  - `--slow tests/test_tartane.py tests/test_probes_90.py`: **117 passed**, §12.4's 116 and the
    new test;
  - her four anchorage cases (§10) passed, so **121 in all**.
- **At this step's end:**
  - `python tools/gen_ships.py <scratch>` gave all twenty files byte for byte as committed;
  - ruff is clean;
  - every file is LF only;
  - no added Python line is over 100 characters;
  - no added line names a model or its maker.

## 14. The owner's note on her topsail, and the lead's nudge 42, point 5

The owner looked at her on b9ebd761 and saw her topsail's loose foot trimmed to the wind,
askew of its yard. The lead's nudge 42, point 5, in the note at the end of
`docs/dev/M7-WorkPackages.md` on the trunk at 11c7e67e, which I read whole: her design's
decision 9 is the answer at the cause. In plain sail the tréou's yard is on deck with its sail,
sent down as the game already sends a yard down, and goes aloft when the tréou is set. Do that
in her file's plain sail and her start, if the engine's sent-down yard serves her set flying. If
it does not, say what it lacks before building anything in the engine. The check for her final
version is her loose foot square with its own yard.

**In short: her file already does it, the engine serves it, and the askew foot is the viewer's.**
Nothing in the tree is changed for this. The mend is one condition in `client/projection.js`,
which is not mine, so I stopped there under the stop rule.

### 14.1 Her file and the engine: decision 9 as built

Her tréou has been `flying: true` since step 2 (0dbd4fc), and it is in neither her plain sail
nor her start. The engine's sail set flying (package 57, the lug topsails and the royals of
1794) is decision 9's way:
- furled, it is on deck with its yard ("sent down");
- `set` sways the yard up from the deck with the sail bent (`data/evolutions/set_flying.yaml`);
- `take in` sends it down whole.

Measured at seed 7, 12 kn, all hands, by the game's own orders:

| Her state | The tréou | Its yard |
|---|---|---|
| her start | furled, sent down | on deck |
| plain sail, by the wind and before it | furled, sent down | on deck |
| `set the treou` | "Swayed up the square sail's yard from the deck with the sail bent." at +85 s; "Set the square sail, flying." at +129 s | aloft at the main's hounds, 8.85 m above her water |
| `take in the treou` | "Took in the square sail; sent down on deck with its yard." at +86 s | on deck |

**The cutter's way does not serve her.** That is the yard's own `sent_down`, as the topgallant
yards are sent down:
- no ship file can start a spar sent down (`SparSpec` has no such key);
- the send-down and the sway-up go by a class of mast (`topgallant_mast`). Hers is a pole main
  of class `mast`, so the class would take every yard on both her masts;
- `set` refuses a sail whose yard is sent down, so the tréou would want a sway-up first. That is
  not set flying.

### 14.2 Where the foot goes askew: the viewer's `squareCut`

`squareCut` hangs a square sail's clews at the arms of the yard below it, by the file's heights.
It skips that yard only when the spar's own state is `sent_down`. A flying yard on deck is served
`sound`, because its sail says it is down. The viewer reads that (`yardOnDeck`) and draws the yard
on deck, fore and aft, 1.44 m above her water and 1.65 m to starboard (`sent_down_flying`).
`squareCut` still takes it as the yard below. So her topsail's clews go to its arms, fore and aft,
raised to the hoist's height.

Her topsail's foot, measured with `buildSkeleton` from the game's snapshot, against her topsail
yard in plan:

| Her state | On the tree | On a scratch copy, the one condition added |
|---|---|---|
| her start; plain sail before the wind; the tréou taken in | **90 degrees askew**: the foot fore and aft from x -2.12 to 9.86 m, 8.85 m above her water, under a yard square at x 4.20 | square with its yard: 9.35 m broad, its clews 8.09 m above her water |
| plain sail by the wind (her topsail yard braced 64 degrees) | **26 degrees askew**: the foot still fore and aft | square with its yard |
| the tréou set | square: the clews at the tréou's yard's arms, 8.85 m | the same |

**What it lacks:** one condition in `squareCut`. A yard on deck with its flying sail
(`B.flyingDown`) should be read as no yard below. Her topsail then hangs from its own yard, 0.9
of it broad and as deep as its area over that breadth, as every square sail with no yard below
does. I measured that on a scratch copy of `client/projection.js` and did not commit it. It is
V2's: "a loose-footed topsail along its own yard wherever the yard below carries no sail".

**Only her two files are touched.** In every ship file, the one square sail over a flying yard
is her topsail, over the tréou's yard, in `tartane.yaml` and `coastguard-tartane.yaml`. The
royals and the lug topsails have no square sail over them, so no other ship's drawing moves.

### 14.3 Found, recorded, not mine

- **The engine braces a flying yard on deck with the rest.** Her tréou's yard was at 58 degrees
  by the wind, and the frigate's main royal yard at 59. The snapshot serves it `sound` and braced,
  as the owner's preview showed (42.2 degrees there). The viewer draws it on deck either way.
- **The trim's words count it.** "Braced two yards to the wind" after the tréou is taken in counts
  the yard on deck. Both are package 57's reading of a yard sent down with its sail, every ship's.

### 14.4 What moved

Nothing. No file of the tree changed for this section, so the §13 figures all stand:
- truth 7-695's counts;
- her figures;
- the twenty ship files, byte for byte from the generator.

13.3's fast tier whole on 3a5c96b is this tree's, since b9ebd76 changed only this report, so I
ran no new tier. When V2's condition is on `…/pkg-90`, her final version's check is a view
case: her topsail's foot square with its own yard at her start, in plain sail, and with the
tréou set and taken in. I will write it then, in the viewer's file as widened to me for her rows
(§10).

## 15. The lead's nudge 88: her topsail's foot and her lateen yard

The lead's nudge 88, point 4, in the note at the end of `docs/dev/M7-WorkPackages.md` on the
trunk at dc7a1f7c, which I read whole. `ship/graph._square_foot_m` overstates a square sail's
foot by twice her deck's height, and the engine mends it in the served step. Mended, her
topsail's foot clears her lateen yard by 0.03 m, not 1.11 m, "no clearance at all by a seaman's
eye". The lead asks whether her ruled figures stand with that clearance, or what her source
gives for the topsail's depth, the pole's head and the lateen yard's hoist. Nothing is built
now. This is the answer, and the mend it asks for is owed with her hash.

**In short: the head and the hoist are her source's, and they stand. The topsail's depth is
mine, with no source behind it, and it does not stand.** Cut to the hounds, its foot comes down
to where the lateen yard is slung.

### 15.1 The clearance as her file cuts it: none

Her module's figures, unrounded, above her water:
- the main's hounds at 8.848 m and her head at 17.293 m;
- the topsail yard at 16.319 m, 3 pieds under the head;
- the topsail cut from its yard down to the hounds, 7.470 m deep;
- the lateen yard slung at the hounds, 8.848 m.

So the foot and the slings are at one height, 0.00 m apart by the cut. The 0.03 m is the file's
rounding: the topsail's centre, 12.584 m, is written 12.6, and the foot doubles that (2 × 0.016).
The doubled deck height comes from the datums: the file's yard heights are above her deck datum
(0.54 m), and the sails' centres are above her water.

**For the engine's step.** A5 classes her topsail as a topsail, not a course, because its foot
stands above the lateen yard (`foot > lat.height_m`). With the arithmetic mended, that holds by
the rounding alone. On the unrounded figures the two are equal, and she would read as a course.
The re-cut in §15.3 takes her off that edge.

### 15.2 What her source gives

| Figure | Her file | Her source |
|---|---|---|
| The pole's head | 8.45 m from the hounds to the head: the hounds 8.00 m and the head 16.44 m above her deck at the mast | Forfait 1788 Table II, the *Humble*: the main 59 pieds, its head (*ton*) 26 pieds (8.45 m). Chapman's sheer, measured: the hounds 7.7 to 8.0 m and the head 16.2 to 16.4 m above the deck (Pages §6.4). **Stands** |
| The lateen yard's hoist | at the hounds, the foot of the head | Forfait p. 121: hoisted until its halyard block touches the one aloft, the halyard through the calcet's sheave. Read as the hounds, below the 26-pied head (Tar §2.1, JUDGEMENT on the reading). **Stands as read** |
| The topsail's depth | 7.47 m, from its yard to the hounds | **None.** Forfait gives its yard (32 pieds) and the whole sail with a topgallant (2,237½ square pieds), not the topsail apart. The depth is mine: the cutter's topsail rule (Steel 1794 p. 125), for a topsail sheeted to the square-sail yard below it. I cut it so before decision 9's revision took the tréou's yard down in plain sail, and did not cut it again after. **Does not stand** |

The foot's breadth comes from the same rule: 0.9 of the tréou's yard (11.99 m), a foot spread on
that yard. For a loose foot no source gives it either. V2 draws it 9.35 m, 0.9 of its own yard.

### 15.3 The mend, for the lead to rule (JUDGEMENT)

Cut her loose foot clear above the lateen yard's slings. The table gives her plain sail against
Forfait's 216.0 m² (his whole sail less the topgallant's 20):

| Clearance above the slings | Depth | Foot 0.9 of the tréou's yard: the topsail; her plain sail | Foot 0.9 of its own yard: the topsail; her plain sail |
|---|---|---|---|
| none, as filed | 7.47 m | 76.6 m²; 216.1 m² (+0.0%) | 66.8; 206.3 (-4.5%) |
| 1 pied (0.32 m) | 7.15 m | 73.3; 212.8 (-1.5%) | 63.9; 203.4 (-5.8%) |
| 3 pieds (0.97 m), her topsail yard's own place under the head | 6.50 m | 66.6; 206.1 (-4.6%) | 58.1; 197.6 (-8.5%) |

Every one is inside the ±15% band.

**My pick: 3 pieds, with the foot 0.9 of its own yard.**
- The cut then matches the drawing. V2 takes a loose sail's depth as its area over that foot.
  Its clews then stand 1.26 m above the slings; as filed they hang 0.76 m below them (8.09 m
  above her water, §14.2).
- It keeps her topsail off A5's edge by a margin a seaman would see.

It is built with her hash, through `tools/ships/tartane.py` and the generator:
- her topsail's area, centre and note, and her plain sail's check;
- old beside new in `docs/dev/TuningNotes.md`;
- her figures measured again. She sails on her topsail, so her polar and truth 7-688 may move.

### 15.4 Found by the same question: the tréou's yard at the lateen's slings

The tréou's yard is hoisted to the hounds, the cutter's square-sail yard's place, where the lateen
yard is slung. Both are at 8.31 m above her deck datum, 0.00 m apart on the mast. In plain sail
the tréou's yard lies on deck (§14), so nothing meets. Whenever the tréou is set, the two yards
stand at one height on the mast. Its hoist rests on the same reading of Forfait p. 121 and on
the cutter's precedent. Recorded for the lead with the depth.
