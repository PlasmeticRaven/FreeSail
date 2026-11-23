# Report: package 90, the corvette *Diana* (her builder, 20 November 2026)

**In short.** Her module, `tools/ships/diana.py`, writes `data/ships/corvette-20.yaml` through the
generator, and every other ship file comes out byte for byte. Her people file, her description row
and words, and `tests/test_diana.py` with her six truths drafted (7-660 to 7-665) are on the branch,
with the eight guards her file moves recorded old beside new. Her hull is her own plan's (measured,
Pages §6.2), her rig Luce's chain on her particulars, her four fits by date on her ports. Two of her
design's judgement figures are tuned, old beside new: **GM 1.5 to 1.75** (truth C) and **`clr_x_m`
2.5 to 2.8** (truth D). **Her mass is her drawn body outside the plank, 470 t** (the lead's ruling of
nudge 30; the table's 498 t before it, recorded beside it); what that moved is in §2.5. **Her tack
is not brought into truth 10's 285 to 600 s by her helm or her rudder** (§4): truth E is drafted with
her own band, 180 to 600 s, marked JUDGEMENT, for the lead. The review lenses ran on her second
commit and found her headsails' centres below their tacks, mended at the cause in her third; the
viewer's tests found her rail begun abaft her taffrail, mended in her fifth.

**I stop here, early, under the stop rule** (§5). Her fast tier is not green on files that are not
mine to edit:
- **the viewer's `tests/test_view_geometry.py`**: 14 of its tests fail on her file, each wanting her
  rows in its per-file tables;
- **`tests/test_magazine.py`'s rule** that a new ship's charges are Table No. 29's: her foreign
  calibres are not in the table;
- **the ranges audit's known list**, `tools/range/audit-known.yaml`, and truth 7-590's count.

Each is set out in §5 with what it needs. Everything of hers that her row covers is built and
pushed, with the guards that only count her file moved.

**After the stop (§8).** The lead ruled on all three in nudge 32 and widened my row to the viewer's
tests. Her rows are in its tables, two of them recorded departures for the lead (the viewer's, not
mended). A foreign gun's charge is its kind's share, her audit entry is filed, and truth E's band is
180 to 330 s. The package's branch is merged at 00382c4 (`72127c9`). Her final fast tier whole,
against a base on that tree, differs from the base only by her own tests and her cases, all
passing. A race in the harbour's start failed one browser test once; it passed on its rerun, and
is recorded for the lead. The slow tier of her files, pace tests excepted, passes. **I stop at the owner's
stopping point 1.**

**On the package's branch (§9, nudge 58).** Her branch takes the package's at 329648e9 (merge
`defc026`), one file resolved by hand, TuningNotes, at its end. Her rows are in the package's new
tables, and the review lenses were read on her merged hash: nothing blocks her gate, four word
mends are made, and four records are for the lead, her spanker first. Her tiers wait for A4's
verdict, as the lead holds them.

**Nudge 59 (§10).** Her bow port's half-breadth is now her drawn side's, 1.86 m, so the 1817
fit's bow obuses stand in her side; `check_viewer_guns` is left as it is, since the outboard rule
fails five committed ships. **Her spanker cut on her own spars is stopped, as the ruling says:**
with it, no `clr_x_m` holds truths D and E together, so her file keeps the larger sail until the
lead rules which truth to restate.

**The owner's (a) (§11).** Her spanker is now the one her spars carry, 95 m2 at 9.7 m, and
`clr_x_m` is 2.65, chosen by a wide table of her tacks across 8 to 25 kn. Truth D is restated as
measured: close-hauled her helm is within half a degree of amidships (-0.33 deg), and abeam she
carries 1.54 deg of weather helm. Her other truths hold, each with its figure, and her picture
does not move. For the lead: she misses stays in 20 and 25 kn with either sail.

**Why she misses stays in a breeze (§12, nudge 65): measured, nothing filed.** Her weight comes
first, as the lead suspected: she is the lightest ship of war for her tonnage, and her yards stand
2.5 times the frigate's against her yaw inertia. At 597 to 611 t she would stay in 8 to 15 kn from
every heading, with truth D in its first band. Her strong-wind misses also want her rig against her
inertia. Both are the lead's to rule.

**Hers, or every square-rigger's (§13, nudge 66): measured, nothing filed.** In a breeze under plain
sail the misses are hers alone. The tack script calls "mainsail haul" a point off the wind for every
ship, and that moment is what turns her back. Hauled with the wind ahead, as Luce also allows, or a
point past, she stays in 20 and 25 kn from every heading, and the frigate-36 stays either way. Her
8-knot misses are shared with the 64, the 74 and the razee. Her rudder is traced from her plan. The
choice is the lead's and the owner's.

## 0. The branch and the merges

- Her branch, `…/pkg-90-diana`, as N1 to N3 left it at 04aa24a6, **fast-forwarded to the package's
  branch at 8b8a982d** (`git merge --no-edit 8b8a982d`): ad8827e2 (stage 0L, her measuring note, her design
  as ruled, and the lead's two follow-ups, `NAMES_TO_NATION`'s `spanish` row and Spain's kit) and
  the trunk with package 119. The coordinating session asked for cb8c445b and then ad8827e2; the
  merge was put to my user, my first brief having said never to merge, and my user allowed it at
  8b8a982d and gave a standing permission to merge the package's branch into this one. No
  rebase, no force, no other branch touched.
- Her base, the fast tier whole, ran on the merged tree, 8b8a982d (§5).

## 1. The commits

| Commit | What | Files |
|---|---|---|
| `133ccb3` | her module and her file by the generator, her people file and her rows, and the pins they move | `tools/ships/diana.py`, `data/ships/corvette-20.yaml`, `data/people/corvette-20.yaml`, `freesail/world/ships.py`, `tests/test_profile.py`, `tests/test_probes_90.py`, `tests/test_schooner_mast.py`, `tests/test_lee_ports.py`, `tests/test_known_truths.py`, `docs/dev/TuningNotes.md` |
| `50afd35` | her tests and her six truths drafted as 7-660 to 7-665 | `tests/test_diana.py` |
| `e561b0d` | the review lenses' mends: her headsails on her own tacks; GM 1.65 and `clr_x_m` 2.8 | `tools/ships/diana.py`, `data/ships/corvette-20.yaml`, `tests/test_diana.py`, `docs/dev/TuningNotes.md` |
| `8536975` | her mass the body as drawn outside the plank, 470 t, by the lead's ruling of nudge 30; GM 1.75 | the same four |
| `73630e3` | her rail from her taffrail; the guards over every file that her file moves (package 119's muster truths, the *Neufchatel*'s rows) | `tools/ships/diana.py`, `data/ships/corvette-20.yaml`, `tests/test_known_truths.py`, `tests/test_neufchatel.py`, `docs/dev/TuningNotes.md` |
| this report | the commit that adds this file, the branch's head | `docs/design/Report-Package90-Diana.md` |

**Her harbour shelf line**: none. The card's "Does not build" names "any scenario or shelf line",
and `client/harbour-shelves.yaml` is a file nobody touches after stage 0. Her design's two lines are
in its §11 for the scenarios' package. `tests/test_harbour.py` passes with her row.

## 2. The basics

### 2.1 Her particulars against their sources

| Clause | In her file | Band or check | Source |
|---|---|---|---|
| Length on the line | 34.47 m | the post's after face to the stem's fore face on the line, 123.7 pies, 0.998 of the table's 124 (124 pies x 0.99 before, a wrong ratio: §9.4); the table's 124 pies is 34.55 m (her module's check) | the plan, measured (Pages §4.1); Winfield et al. 2023, p. 930 |
| Breadth | 9.06 m | 32 pies 6 pulgadas at the book's pie, within 0.01 m (her check) | Winfield p. 930; the table |
| Depth in hold | not a key | 16 pies, 4.46 m, within 0.01 m (her check) | the table |
| Draught | 3.78 m | the mean to K, 3.91 m aft and 3.65 m forward; to the keel's lower edge 3.63 m (her note) | the lead's ruling 1 and note of 09:40, item (1); Pages §4.2 |
| Displacement | 470,000 kg | her body drawn to her line outside the plank, 465.6 to 473.6 t at 3 to 4 pulgadas (JUDGEMENT), the middle; beside it the table's 540 toneladas 691 libras, 498.0 t at the book's libra (its arithmetic her check), most likely reckoned level at her after draught | the lead's ruling of nudge 30; Pages §4.3-§4.5; the table; Winfield et al. 2023, pp. 41-46 |
| Lateral area | 122.2 m2 | the post's after face, K and the knee's fore edge, no rudder | ruling 4; Pages §5.6; D29 (b) |
| Deck at side | 1.33 m | the upper red line at the middle | ruling 5 (JUDGEMENT); Pages §5.2 |
| GM | 1.75 m | heel within 1.15 times the frigate-36's in 22 kn (truth C): 1.10 close-hauled, 1.12 abeam | JUDGEMENT on Meyer's "stiff" (Roos 1957 p. 94); tuned from 1.5 |
| `clr_x_m` | 2.8 m | weather helm in 15 kn 0.5 to 3 deg close-hauled, 1 to 3 abeam (truth D): 0.82, 2.02 | JUDGEMENT on Meyer's "steers splendidly"; tuned from 2.5 |
| Hull speed | 11.8 kn | the frigate's 13.0 by the root of the lengths; Meyer's 10 to 11 kn met (truth B: 10.28 to 11.29) | Dia-D §2 |
| Rudder | 3.0 m2, span 3.90 m, 35 deg, 3 deg/s | the blade under the line, measured +-0.3 m2; the stop and rate the frigate's | Pages §5.5 |
| Ports | eleven a side, 0.83 by 0.66 m, Pages §5.7's sills and half-breadths, and a place over the rail between ports 1 and 2 | every gun of every fit on its triple to the centimetre (her check); `check_viewer_guns` clean | the plan; ruling 6; Dia-D §5.2 |
| Masts | fore 64.3 ft, main 71.4 ft, mizen 62.8 ft heel to head, at the plan's places and rakes (0.5, 5.5, 6.0 deg in the line's frame) | Steel's 20-gun column 64, 72 and 61 ft (Pages §7) | Luce 1866 ch. VII on her particulars; the plan |
| Main yard | 19.79 m | Steel's 19.20 (-3.0%); Falconer's 19.87; Chapman's 17.97 | Luce; Pages §7; Dia-D §4.1 |
| Masthead | 29.0 m above her water (`rig_height_m`; the frigate's 35.9) | her design's "about 29 m" | computed |
| Plain sail | 1,054 m2 | the frigate-36's 1,584 by her chain's square, 0.663 (Dia-D §4.2's "about 1,051") | computed |
| Company | 167; ten posts; forecastle 14, fore top 12, main top 15, mizzen top 7, afterguard 25, waisters 18, soldiers 50, idlers 16 | sum 167 (her check) | Winfield p. 930; the regulation of 1788's fifty soldiers (p. 1446 and following: VR-Sp §15); the rest her design's table, JUDGEMENT |
| Names | `spanish` | reads as Spain's where a scenario names no nation (truth 7-680) | N1 and the lead's follow-up |
| Soldiers' kit | Spain's, `spanish` | the basic kit's figures | N3 and the lead's follow-up |
| Ground tackle | bowers of 22.4 cwt (1,140 kg) on cables of 15 in | Luce's rule on 449 tons burthen, the old English measure on her gun deck and breadth | Dia-D §2, §7 |
| Boats | launch 28 ft, cutter 25 ft, jolly boat 18 ft | the frigate's allowance at her size | JUDGEMENT (Dia-D §7) |
| Hold | 45 tons | 0.1 of 449 tons burthen | the house's rule for a ship of war |

### 2.2 Her polar beside the frigate-36's (`world.ships.polar_of`, the best speed and its angle)

| Wind | Hers | The frigate-36's |
|---|---|---|
| 8 kn | 4.61 kn at 100 deg | 4.62 kn at 90 |
| 15 kn | 8.01 kn at 90 | 8.19 kn at 90 |
| 25 kn | 11.18 kn at 100 | 11.63 kn at 100 |

Sailed close-hauled in 15 kn, 66 deg off, she makes 4.73 kn; abeam 7.81 (the frigate 4.80 and 7.97).

### 2.3 Her tack, wear and heave-to at seed 7, the ticks of each part

By the truths' helpers: close-hauled on the starboard tack in 15 kn, the wind from the north.

**Tack from 292.5 deg, 215 s** (from 290 and 295, 206 and 216 s):
- 1 s: "All hands! (to tack ship)"; "Ready about. Helm's a-lee; ease off the head sheets; haul aft
  the spanker sheet."
- 59 s: "Rise tacks and sheets. Mainsail haul."
- 71 s: "Her way is gone; she hangs in stays. Helm kept a-lee; the head yards aback to box her
  off".
- 117 s: "Her head is through the wind; the head sails aback pay her off."; "Let go and haul. Draw
  jib; trim aft the head sheets."
- 215 s: "Tacked; braced up on the larboard tack, heading ENE (68°)." Piped down. Ground lost 42 m
  (28 and 46 m from 290 and 295).

**Wear, 492 s** (truth 11's 360 to 720):
- 1 s: "Stand by to wear ship. Up helm; brail up the spanker; brace in the after yards."
- 74 s: "Wind aft. Squared the head yards; shifted over the sheets; hauled out and braced up."
- 422 s: "By the wind. Haul out the spanker!"
- 492 s: "Wore ship; braced sharp up on the larboard tack, heading ENE (68°)." About 250 m to
  leeward.

**Heave to** from 5 kn close-hauled: at 1 s the courses hauled up, the spanker brailed, the fore
topgallant clewed up, the main topsail braced aback and the helm a-lee. At 126 s "Hove to on the
starboard tack, main topsail to the mast, helm a-lee": lying 56 to 57 deg off at 1.1 kn for the next
ten minutes, never aback (the frigate: 220 s, 58 to 62 deg, 1.4 kn). **Fill away**: filled away at
59 s, close-hauled at three knots by 156 s (the frigate's 59 and 161).

### 2.4 The work particular to her

- **Her captain's case** (Meyer: 10 to 11 knots with the wind two or three points abaft the beam in
  a fresh breeze; Roos 1957 p. 94). Under plain sail, which her book carries below 30 kn: 10.53,
  10.42 and 10.28 kn at 112, 118 and 124 deg off in 24 kn; 10.78, 10.68 and 10.54 in 25; 11.29,
  11.16 and 11.03 in 27 (truth 7-661's band 9.5 to 11.5).
- **Her heel against the frigate's** under plain sail in 22 kn: 8.10 against 7.34 deg
  close-hauled (1.10), 12.61 against 11.30 abeam (1.12); truth 7-662's 1.15. At her design's GM of
  1.5, the table's mass and her headsails as first cut, 1.17 and 1.20.
- **The lee port at 21.1 deg.** Her midship port's sill, 1.72 m over 4.46 m, comes to the water at
  21.09 deg (atan: ruling 6's figure). The game's lee-port rule (L2, §7.1) shuts a port a foot short
  of the water: her lowest lee port, that one, at 18.50 deg, with ports 5, 7 and 4 within the next
  degree (18.67, 19.08 and 19.45). Her heel abeam in 22 kn, 12.6 deg, leaves them open. Her design's
  truth F reads "shuts at 21.1 deg by L2's rule"; the two figures are not one measure, and truth
  7-665 holds both (§6, question 3).
- **Her four fits**:
  - `danish 1807`: sixteen 30-pounder carronades in ports 2 to 9 and four long 8s in ports 1 and
    10.
  - `as captured 1809`: twenty 24-pounder carronades.
  - `carronadas de a 30 1810`, the default: twenty 30-pounder carronades.
  - `1817`: twelve long 12s in ports 1 to 6, eight 30-pounder carronades in ports 7 to 10, and four
    3-pounder obuses carried as carronades, two in the bow ports and two over the rail between
    ports 1 and 2.

  Broadsides 256, 240, 300 and 198 lb; 44, 40, 40 and 62 men at the guns of a side; 18.6, 13.2,
  17.4 and 28.3 t of guns. Every gun is on its port to the centimetre, and `check_viewer_guns` is
  clean, the bow port empty in the first three fits. **At the beat to quarters every crew of every
  fit is manned whole**; in the 1817 fit, twelve crews of 62, 21 of them her soldiers at the
  carronades and obuses, 29 soldiers kept in their division (`tests/test_diana.py`).
- **Every evolution's want against her watches**: her watches are 71 and 70, 46 and 45 seamen with
  25 soldiers each. Asked of either watch alone through the muster's request, all 83 numbered
  evolutions are manned whole, and the 27 others are all hands' work by their files. None calls all
  hands for too few, and none waits. The request takes any idle hand on deck, its stations ranked
  first, so her design's "the anchor's twelve forecastle hands against her watch's seven" is made
  up from the watch's other hands.
- **Plain sail from furled**: her watch sets it in 12.8 minutes and all hands in 16.4, where the
  frigate's take 16.4 and 5.6. Her design left this to her builder; it is explained in §6, item 6.

### 2.5 Her drawn depth and displacement beside the filed ones, and her mass

The generator's form (`freesail/ship/form.py`) draws her hull from her profile at **448 t against
the filed 470 t (-5%)**, recorded and not moved, and **3.26 m deep at the greatest section** (to the
rabbet) against her draught of 3.78 m (to K). Her measuring beside them (Pages §4.3): 435.6 t
moulded; 441.7 t with the keel, post, stem and gripe; 465.6 to 473.6 t outside 3 to 4 pulgadas of
plank (JUDGEMENT). The generator's drawing is its own rule's integration of her profile, not her
measuring's (Pages §4.3's sections and waterlines): recorded beside, not reconciled; why the two part
by 18 to 26 t was not looked into.

**What the file floats her at, and why** (the lead's note of 09:40, item (3); answered at
`8536975`): **470,000 kg, her body as drawn outside 3.5 pulgadas of plank, to the arrowed line as
drawn, 3.78 m to K at the middle.**
- The physics takes her mass from `displacement_kg` and her water from `draught_m`, and reads
  nothing of the drawn body (Build-Ships.md §5.0 principle 8). So mass and line must agree, and since
  the lead's ruling of nudge 30 they do: her mass is what her drawn body displaces at her drawn line.
  Every other figure of her file (her draught, her breadth at the water, her lateral area) is
  reckoned to that line.
- The plank is unsourced, so her mass is one figure of the range 465.6 to 473.6 t, the middle
  (JUDGEMENT); the range is in her note.
- The table's 498.0 t (540 toneladas 691 libras at the book's libra) is recorded beside it. It was
  most likely reckoned on a level line at her after draught (499 t, its bodies 1.10 to 1 against the
  table's 1.089; the lead's ruling 3). Filed at her first three commits, it would have floated her
  about 6% deeper than her file draws her.
- The engine has no trim, so she floats level at the mean; her 0.27 m of drag is in her profile
  alone.

**What the change moved** (498,000 to 470,000 kg; measured, `docs/dev/TuningNotes.md`):

| Measure | At 498 t, GM 1.65 (`e561b0d`) | At 470 t, GM 1.65 | At 470 t, **GM 1.75** (`8536975`) |
|---|---|---|---|
| Heel in 22 kn, close-hauled and abeam (the frigate's 7.34, 11.30) | 8.12, 12.62 (1.11, 1.12) | 8.59, 13.35 (1.17, 1.18; over truth C) | 8.10, 12.61 (1.10, 1.12) |
| Weather helm in 15 kn, close-hauled and abeam | 0.80, 2.02 | 0.83, 2.02 | 0.82, 2.02 |
| Tacks from 290, 292.5 and 295 (s) | 197, 212, 218 | 207, 215, missed stays | 206, 215, 216 |
| Wear (s) | 492 | 493 | 492 |
| Hove to; filled away and settled | 130 s; 59 s, 160 s | 126 s; 59 s, 156 s | the same |
| Meyer's case (kn) | 10.28 to 11.28 | not run | 10.28 to 11.29 |
| Polar's best in 8, 15 and 25 kn | 4.61, 8.01, 11.18 | the same (the polar reads no mass) | the same |
| The generator's drawn hull against the filed | 448 against 498 t (-10%) | 448 against 470 (-5%) | the same |

So **her GM goes from 1.65 to 1.75**, and her stiffness stays where her captain's word and truth C
set it: her righting moment is her mass times her GM, 470 t at 1.75 near 498 t at 1.65. Her file's
other figures are unchanged (her rail's start, moved after it in `73630e3`, is the drawing's
alone, read by no physics). Nothing of hers is merged, so no pin of the trunk's moves. Her own
tests moved their figures: truth 7-660's mass with the table's beside it, the report's line, and the
measured figures in the docstrings.

### 2.6 What was taken as judgement

Her design's own judgements, filed as it gives them:
- K as a false keel; the upper red line as her deck at side; the plank, 3 to 4 pulgadas; the
  stern's reading; the bow port's half-breadth.
- GM and `clr_x_m`, tuned (§2.1).
- Her company's shares beside her 50 soldiers; one company for every fit.
- The obús's weight and crew; the long 8's weight; the 1817 fit's ports and the obuses' places.
- Her boats; her burthen of 449 tons for the English helpers.

And mine, each named in her notes:
- **The headsails** are the frigate-36's, scaled by her chain: their areas by its square, their
  places from her stem head, and their centres above their tacks' spar ends (the review's mend).
- **The spanker** is the frigate's, scaled. Its boom stands 2.9 m above her datum, raised from the
  frigate's 2.4 to clear her taffrail by 0.2 m.
- **Rope and shrouds**: her rope is the frigate's by the root of her plain sail over the
  frigate's (0.816), as the 74's and the 64's. Her shrouds keep the frigate's counts.
- **The staysails between the masts** keep the shared helper's stays at the frigate's sizes (§6,
  item 8).
- **The crews by D31 (c)'s period sources**, Falconer and Douglas, where her design's §5.3 words
  say `gun_crew`. The long 8 takes Falconer's figure for a 9.
- **The idlers by trade** are the frigate's thirty shared to her sixteen by the largest remainders,
  which leaves no armourer and no clerk.
- **Stores** are the frigate's scaled by her company or her sail: 63 t of water, 400 fathoms of
  cordage, 25 shot plugs.
- **Her stern lights**: a band of four over the knuckle within 1.5 m of the middle (Steel 1805
  p. 240: in a small ship, the great cabin windows only).
- **`sections_m`** carries each measured port's sill reading, over the line's half-breadth carried
  between stations, so it is marked `judged` (her design had every line but the lights
  `sourced`).
- **The stem head** is filed a centimetre forward of its reading, 17.31 for 17.30 (§6, item 7).
- **`keel_m` is K**, the false keel's lower edge, as the drawn hulls file it and as her draught is
  counted. Her design's §3.2 words name the keel's lower edge for `keel_m`; that line is in the
  note.
- **Truth E's band**, 180 to 600 s (§4).

## 3. Pictures

None: a cloud session has no browser, and the coordinating session takes them (its message of
2026-11-20). By §8.0's list they are:
- abeam to leeward, on the quarter, ahead and astern, furled and under plain sail;
- her own states: her fits' guns run out, and hove to;
- beside the frigate-36 at one scale, and her hull alone beside the frigate's with her rung letters
  under it (A, her own plan, on every line; `sections_m`, the lights and the ends' fullness
  judged);
- heeled 10 deg, seen from windward.

To look at: the stem head standing 1.5 m above the rail's end, the scroll head at x +20.6, the
stern lights' band over the knuckle (§6, item 9), and her sloping keel.

## 4. Her going about: what was tried, and her band

Plan §8.4 and the coordinating session asked her tack from 295 deg to be tuned into truth 10's 285
to 600 s by her helm and her rudder. On her measured hull and rig all three of her tacks are fast:
206, 215 and 216 s as committed. The frigate-36 shoots through stays with way on, then spends most
of her 340 to 450 s griping up on the new tack with too little way for her helm. The *Diana* hangs in
stays, is boxed off by her head yards, and settles on the new tack at once.

What was tried (docs/dev/TuningNotes.md, "Package 90, the Diana", every cell):
- **More weather helm** (`clr_x_m` 2.5 to 3.5) takes her round sooner, and from 2.9 or 3.5 she
  misses stays from one heading.
- **Her rudder's rate**, 3 down to 1 deg/s, lengthens the tacks only to 251 to 263 s.
- **Its area**: 2.0 to 2.5 m2 gives 214 to 244 s; 3.3 to 5.5 m2 is a knife edge, one heading
  longer and another shorter (161 to 303 s).

No figure within her sources, her measured 3.0 m2 at +-0.3 and a credible helm, brings all three
into the band. So **her rudder is kept as measured**, and truth 7-664 is drafted with her own band:
**three to ten minutes, 180 to 600 s (JUDGEMENT, for the lead)**, Luce's ceiling kept. She wears in
492 s, inside truth 11's band. Each of her three tacks loses 28 to 46 m, where truth 10 has the
frigate's three gain together; this is recorded, not asserted.

## 5. The tests

Run from the worktree's root with `python -m pytest -p no:cacheprovider -o addopts="--dist
loadgroup"`. The base ran in the main checkout, left at 8b8a982d, the merged tree. Each fast tier
whole ran as four pytest runs over the test files (187 on her tree, 186 on the base; `-n 4`, each
with its own `--junitxml`), the four junit files then read together.

| Set | Tree | Result |
|---|---|---|
| **The base**: the fast tier whole | 8b8a982d | **8,471 passed, 8 skipped, 1 xfailed** (8,480); 583 slow left out; no failure |
| Her own tests, `tests/test_diana.py` | `73630e3` | 29 passed |
| The generator into scratch, and `cmp` of every committed ship file | each commit | 19 of 19 byte for byte (her file the generator's; the other 18 unmoved) |
| `tools/check_viewer_guns.py` on her file | each commit | clean |
| The 16 guard files that range over `data/ships` (`test_probes_90`, `test_profile`, `test_schooner_mast`, `test_subtypes`, `test_lee_ports`, `test_harbour`, `test_people`, `test_check_viewer_guns`, `test_wardroom`, `test_hull_form`, `test_ship_particulars`, `test_ships_hierarchy`, `test_rig_classing`, `test_profiles`, `test_scenario_nations`, `test_catalogue`) | `133ccb3` before its moves | 914 passed, 3 failed (the three pins moved in it) |
| The same files' moved tests, and truth 7-190's | `133ccb3` | passed (268; 15 and 165) |
| **Her final fast tier whole**, shards 1 to 3 | `8536975` | 5,380 passed, **20 failed**, 7 skipped, 1 xfailed; **shard 4 cut** by the container's two-hour limit for one background command |
| The moved guards after it (truths 7-700 and 7-701, the *Neufchatel*'s rows) and her tests | `73630e3` | 32 passed |
| `tests/test_view_geometry.py`, her cases | `73630e3` | **14 failed**, 39 passed |
| **The slow tier of her files**: her own and the five test files she moved pins in have none, but for `tests/test_known_truths.py`'s 218 | base 8b8a982d | 206 passed, 8 xfailed, **4 failed: four pace tests**, which measure ticks a second against the build machine's floor and are meant to run alone (`pyproject.toml`'s `pace` mark), run here beside a fast tier of four workers |
| The same without the pace tests | `8536975` | 196 passed, 8 xfailed, **1 failed: truth 7-590** (the ranges audit), hers |
| The 13 pace tests alone, on either tree | | **not run**: they want the machine to themselves, and are for the fast tier's last run |

**The final tier beside the base, test by test** (shards 1 to 3 of `8536975` against the base, the
5,340 tests run by both):
- **outcome changed: four**, each passed on the base and failed on hers:
  - truths 7-700 and 7-701 (package 119's musters by file) and the *Neufchatel*'s rows-by-intent
    test, all mended in `73630e3` as guards that grow by her file (TuningNotes);
  - `tests/test_magazine.py`'s new ships and the table (stop 2, below).
- **only in her tree: 68**, her own 29 and her cases of the parametrized tests over every file; 52
  passed and 16 failed, all in `tests/test_view_geometry.py` (14 after `73630e3`'s rail; stop 1).
- **in the base and not run on hers**: shard 4's tests (the cut).
- the skips and the xfail the base's.

**The stops** (the stop rule: a step that needs a file my row and the card do not name, said and
not edited):
1. **`tests/test_view_geometry.py`**, the viewer's (Plan §7.1: "The viewer ... `tests/test_view_geometry.py`").
   Its per-file tables want her rows, each a figure of the drawing measured by the viewer's own
   probes: `BOWSPRIT_DRAWN` (her bowsprit's drawn forwardness and steeve), `TIERS_IN_THE_SIDE`,
   `CHORD_OFF_THE_SIDE_M`, `LINES_ON_THE_RAIL`, `STEM_TACKED` and `BOOM_SAIL` (her spanker).
   `RIGHTLY_WITHOUT["gallery"]` wants her file, since she has no quarter galleries. And two of its
   tests assume every square stern files `form.stern.round_up_m` and `galleries_m`; her measuring
   read neither (Pages §5.5), and I have not invented them to suit a test. 14 tests in all.
2. **The charge of a foreign gun.** `tests/test_magazine.py` holds every new ship's charges to Table
   No. 29 (`freesail/ship/charges.py`, `CHARGE_TABLE_LB`). By the owner's decision 9 her guns'
   pounds are as her navy named them: her 30-pounder carronades (every fit but one), the Danish
   long 8s and the 1817 obuses of 3 are not in the table, and `charge_lb` gives each its kind's
   share. The rule for a foreign gun's charge (the table's nearest, the share, or a row of the
   table's own) is the lead's, and the three-decker's 36s will meet it too.
3. **The ranges audit**: `v-fit-ahead:corvette-20:carronadas de a 30 1810` (her default fit, dated
   1810, on a far corvette's days before it) is a mechanical finding the audit makes of her, as it
   makes the frigate's, the brig's, the 74's and the rest. It wants her entry in
   `tools/range/audit-known.yaml` (a tools file outside the card) and truth 7-590's mechanical count
   moved 60 to 61.

When they are settled, her fast tier whole runs again on the head, compared with the base, and the
pace tests alone on both trees.

## 6. Her open questions

For the lead:
1. **Truth E's band** (§4): her own, 180 to 600 s, or Luce's 285 to 600 s with a change to her hull
   or helm I could not find within her sources.
2. **Her rank at the rig's distance**, her design's §17.2 item 1: "a ship" ranks her a frigate
   until she is made out. Filed as designed.
3. **Truth F's figure** (§2.4): the dip at 21.1 deg or L2's shut at 18.50. Both are held now.
4. **The 1817 fit's ports**: "ports 1 to 6" for the long 12s counted from aft (the measuring note's
   numbering) puts the long guns aft and the carronades forward. Her design's wording predates that
   numbering; confirm the intent.
5. **`keel_m`**: K, as the drawn hulls file it, where her design's §3.2 words name the keel's lower
   edge (§2.6).
6. **Found, not mended: a numbered job begun short is not topped up** when other jobs' hands come
   free (`crew/hands.py`, `top_up` serves all-hands work alone). It is why all hands set her plain
   sail slower than her watch does: her eight square sails begun at once want 96 hands aloft
   against her 91 seamen, and the last, the mizzen topgallant, begins with seven of twelve and is
   set at 1,074 s, every other sail by 665 s.
7. **Found, not mended: the drawn top of the side** (`freesail/ship/form.py`, `_top_at` and `check`)
   refuses a rail point with a stem head directly over it, the side's top drawn straight to the stem
   head beyond the rail's last point. She files her stem head 1 cm forward, within its reading.
8. **Found, not mended: the staysails between the masts** keep the shared helper's stays at the
   frigate's sizes (`gen_ships.between_the_masts`). They rate about half again as strong as hers
   would by her rope's scale, as they do in the brig-sloop's file.
9. **Her stern lights** stand over the knuckle, partly above her bulwark rail at the stern (3.52 m),
   with no cabin under a quarterdeck behind them (she is flush-decked). The flush-decked brig files
   none. Judged; the owner's sheets will show it.

For the owner: none new. Her design's §17.1 questions were answered on 2026-11-18 and 2026-11-19.

## 7. Other things to know

- **The review lenses** (Plan §10.2) were read on 50afd35 by a reviewer who was not her builder.
  - **Mended in e561b0d**:
    - her headsails' centres, below their tacks;
    - a computed weight in the 1817 fit's note;
    - measured figures in her tuned figures' notes;
    - the stations' note's wording;
    - the tests' assertions that could not fail, and docstrings that named figures the tests did
      not hold;
    - three small points of words.
  - **Recorded and not mended**, as findings above: the staysails' stays, the stem head's
    centimetre, the measured ports' check passing by construction (each port's reading being among
    her sections), the lights, and the 1817 ports' counting.
- **A rule followed**: her persons are they and them in her people file and her notes.
- **The commits' author** is the identity this cloud session was given, which names a maker. It is
  not a file or a message, and I did not change it. The messages carry no trailer.
- **The stop**: I stop here, early, for the three things of §5, before the owner's stopping point
  1. Everything else of hers is pushed; this report is the last commit.

## 8. After the stop: the lead's rulings of nudge 32

The lead answered the three stops of §5 and the questions of §6 in nudge 32
(`docs/dev/M7-WorkPackages.md` on the package's branch), widening my row to
`tests/test_view_geometry.py`. What each ruling moved, old beside new, is in
`docs/dev/TuningNotes.md`, "The Diana: the lead's rulings of nudge 32".

### 8.1 The branch and its commits since §7

- **Merged the package's branch at 00382c4** (package 90's A2, the words of a rig with no yards;
  the tartane's step 1 and nudges 27 to 29), under my user's standing permission (§0), as the merge
  commit `72127c9`. One file conflicted, `docs/dev/TuningNotes.md`, where both sides only added
  sections. Both sides' sections are kept, the package's and then mine. No generated file
  conflicted. No rebase, no force, no other branch touched.
- **The base** for the final tier is the fast tier whole on the merged tree's package side, 00382c4,
  in a worktree of its own (§8.4).
- **Her figures after the merge**, measured again on the head, are as before it: her tacks 206, 215
  and 216 s (ground lost 28, 42 and 46 m), her wear 492 s, her heel in 22 kn 8.10 and 12.61 deg,
  hove to in 126 s lying 56 to 57 deg off at 1.1 kn, filled away in 59 s and settled in 156 s.

| Commit | What | Files |
|---|---|---|
| `2cd5caa` | the rulings of nudge 32: her viewer rows and the two departures, the charges' rule, her audit entry and truth 7-590's count, truth E's band, the 1817 ports, no stern lights | `tools/ships/diana.py`, `data/ships/corvette-20.yaml`, `tests/test_view_geometry.py`, `tests/test_magazine.py`, `tests/test_diana.py`, `tests/test_known_truths.py`, `tools/range/audit-known.yaml`, `docs/dev/TuningNotes.md` |
| `4dec517` | the ranges audit's two ceilings her file moves, and two histories in her people file mended without a year | `tools/range/audit-known.yaml`, `data/people/corvette-20.yaml`, `docs/dev/TuningNotes.md` |
| `72127c9` | the merge of the package's branch at 00382c4 | the package's |
| `acd85fa` | the known list's count of the data's entries, 28 to 29 | `tests/test_range_audit.py`, `docs/dev/TuningNotes.md` |
| this section | the branch's head; and two figures of mine mended in TuningNotes (§8.2 items 1 and 4) | `docs/design/Report-Package90-Diana.md`, `docs/dev/TuningNotes.md` |

### 8.2 What each ruling moved

1. **The viewer's tables** (`tests/test_view_geometry.py`). Her rows, each read off the case's own
   probe on her file:

   | Table | Her row |
   |---|---|
   | `BOWSPRIT_DRAWN` | 2.014 m forward of B5.1's rule, drawn 32.13 deg steeved (her file's 21.5: item (b) below) |
   | `TIERS_IN_THE_SIDE` | none drawn (item (a) below) |
   | `CHORD_OFF_THE_SIDE_M` | 0.004 m, her main wale's |
   | `LINES_ON_THE_RAIL` | the frigate-36's own set |
   | `STEM_TACKED`, `STEM_TACK_Z_M` | her storm staysail; its tack at 5.11 m, 2 cm over her stem head's top |
   | `BOOM_SAIL`, with `FRAME_MOVED_OLD_M`, `SHEET_END_X_M`, `BOOM_OVER_TAFFRAIL_M` | her spanker; 4.86 m; x -24.05 to -18.63; 0.20 m level, 0.58 m topped up |
   | `NO_GALLERY_OR_LIGHT` (into `RIGHTLY_WITHOUT["gallery"]` and `["light"]`) | her file, with its reason |
   | `ROUND_UP_UNREAD` (new) | her file, with its reason; the transom case's branch draws her foot straight across at the knuckle, with no tuck |

   The two cases that held every square stern to `round_up_m` and `galleries_m` name her and her
   reason and no other file. A square stern that merely forgets them still fails. I checked this
   with a throwaway copy of the frigate-36's file with the two keys and their marks taken out, not
   committed: the transom case fails on its new assertion ("a square stern files its round-up, or
   is named with its reason in ROUND_UP_UNREAD"), the gallery case on its `galleries_m`, and the
   closed-hull case on its gallery.

   Her cases in that file number 58, all passing. My TuningNotes line said 59, a miscount of mine:
   neither the file nor her ship file has moved since. This commit mends the line to 58.

   Two of her rows are **recorded departures, for the lead**. Their cause is the viewer's
   (`client/projection.js`), which is not in my row, so I did not mend them:
   - **(a) No port band is drawn on her** (`BAND_UNDRAWN`, joined to `RIGHTLY_WITHOUT["band"]` as
     the *Neufchatel*'s `WALE_UNREAD` is to the wale's). Her eleven ports a side are cut in her
     side, but her one tier also holds the 1817 fit's place over the rail, whose middle stands 0.28 m
     over it. The viewer reads a tier as cut in the side only when every triple in it is.
   - **(b) Her stem head stands 1.50 m over her rail's fore end** (measured: 5.09 against 3.59 m),
     where every other file's is within 0.14 m of its rail or under it. The viewer roots the
     bowsprit and the fore stay at the lower of the two. So it draws her bowsprit 10.6 deg steeper
     than her file and lands her fore stay 1.5 m under her stem head's top. And it raises her storm
     staysail's tack 10.6% up the stay (`TACK_UP_HER_STAY`, every other file's under 4%), 0.53 m off
     her side (her row of `TACK_OFF_HER_SIDE_M`, beside the *Neufchatel*'s 0.20).
2. **A foreign gun's charge is its kind's share** (`parts.charge_lb`; no reader changed).
   `tests/test_magazine.py` now holds every new ship's charge to `parts.charge_lb` for its kind and
   calibre, and keeps the guard that every gun of the table gets the table's figure. Her guns outside
   the table: the 30-pounder carronade (2 lb 8 oz), the Danish long 8 (2 lb 11 oz) and the obús of 3
   (4 oz). Their calibres are as her navy named them. **Found, not mended: the pounds differ.** The
   Spanish libra is 0.4608 kg, the English pound 0.4536, and a Danish 30-pounder fires about 33
   English pounds. Every reader takes a `pounder` as English, so her charges, ranges and weight of
   broadside read a Spanish gun 1.6% light and a Danish one about 9% light.
3. **The ranges audit**: her entry in `tools/range/audit-known.yaml`
   (`v-fit-ahead:corvette-20:carronadas de a 30 1810`, as the other hulls' default fits have), and
   truth 7-590's mechanical count 60 to 61, the old beside the new. The audit's slow sweeps then
   found three counts over their ceilings with her file:
   - `u-ships`, 19 against 18. Every ship file is counted, since the schema has no year, and hers is
     the nineteenth. The ceiling is raised by one, with its reason.
   - `x-words:ship-words`, 18 against 17. Her `era_notes` date her building, her taking and her
     service, as the other files' do. The ceiling is raised by one, with its reason.
   - `x-words:people-words`, 12 against 10. Two histories in her people file named a year ("after
     the peace of 1802", "at Toulon in 1793"). They were my outlines' words, not a source's, so I
     **mended them at the cause**: they are rewritten without the year, and the ceiling stays 10.

   And `tests/test_range_audit.py` counts the known list's entries by owner: the data's 28 to 29 with
   her entry, the engine's 38 unmoved, old beside new in its comment. It failed in the final tier's
   first run (§8.4) and is mended in `acd85fa`.
4. **Truth E's band, 180 to 330 s** (it was her own 180 to 600). The floor is JUDGEMENT, a small ship
   quick in stays; the ceiling is about half again her slowest tack, also JUDGEMENT. Her three tacks,
   measured again after the merge, are 206, 215 and 216 s from 290, 292.5 and 295 deg, unchanged.
   What was tried is §4: her weather helm (`clr_x_m` 2.5 to 3.5), her rudder's rate (3 down to 1
   deg/s) and its area (2.0 to 5.5 m2). Her rudder is kept as measured, 3.0 m2 at 3 deg/s. The
   ground each tack loses, 28, 42 and 46 m, is recorded, not asserted. My TuningNotes line for this
   ruling said "her rudder from 2.0 to 4.5 m2", but the trials' own table there runs to 5.5. This
   commit mends my line to the table, and to the rate's trials beside it.
5. **Held as designed**: her rank at the rig's distance; truth F with both figures, the dip at 21.1
   deg and L2's shut at 18.50; `keel_m` at K. **Her 1817 fit by the measuring note's numbering**:
   the long 12s forward and amidships in ports 5 to 10, the 30-pounder carronades aft in ports 1 to 4
   (JUDGEMENT, her note says so), and the obuses where they were. At quarters there are twelve crews
   of 62, all manned: 20 soldiers at the guns and 30 kept in their division (21 and 29 before).
   **Her stern lights: none filed**, as for the flush-decked brig, until the owner's sheets show them
   (JUDGEMENT, her note says so). Her marks are `sourced` but `sections_m` and the ends' fullness.
6. **The engine's faults found** (§6, items 6 to 8): nothing to do, by the ruling.

### 8.3 Why other ships' rows moved for her file

Each of these tests holds a table by file over every file of the tree. Each grew by her row, and no
figure of another ship changed. I checked each table's other rows against the base, and every one is
as it stood.
- **The *Neufchatel*'s rows-by-intent** (`tests/test_neufchatel.py`,
  `test_her_row_sails_by_her_first_role_and_no_other_row_moves`). This test holds every row of
  `DESCRIPTIONS` (`freesail/world/ships.py`) to the kind each intent sails it as, and every file to
  its own first role. Her row, `corvette`, is a new row of that table, so the test's two maps took
  her line: `"corvette": ["kings-ship"] * 4 + _TAIL`, as the 74's, and her file
  `"corvette-20.yaml": "kings-ship"`. No other row's value moved.
- **Package 119's truths 7-700 and 7-701** (`tests/test_known_truths.py`). Truth 7-700 holds every
  ship file's two watches equal or one apart, and 7-701 holds the eighteen musters as they were
  before package 119's rule for the odd hands. Both read every file by glob, so her file joined
  them. For 7-700 she is a row of `_MUSTERED_AFTER_119`, her watches 71 and 70, beside the eighteen
  of `_MUSTERED_BEFORE_119`, which are unchanged. For 7-701, a muster made after the rule has no
  muster before it to be held to, so the truth iterates the eighteen it was written for. Their
  figures are as they stood.

### 8.4 The tests on the head

Run as in §5, from the worktree's root. Each fast tier whole ran as four pytest runs (`-n 4`, each
with its own `--junitxml`), one after another in one command under the two-hour limit, and the four
junit files were then read together.

| Set | Tree | Result |
|---|---|---|
| **The base**: the fast tier whole | 00382c4 | **8,500 passed, 8 skipped, 1 xfailed** (8,509); no failure |
| Her fast tier whole, first run | `72127c9` | shards 1 to 3: 6,502 passed, 7 skipped, 1 xfailed, **1 failed**: the known list's count of the data's entries, 28 against her 29 (§8.2 item 3), moved in `acd85fa`; shard 4 not run |
| **Her final fast tier whole** | `acd85fa` | **8,607 passed, 8 skipped, 1 xfailed, 1 failed** (8,617): the harbour's stations table, below |
| The harbour's test alone, five times | `acd85fa` | 5 passed |
| Shard 2 whole again, alone | `acd85fa` | **3,422 passed**, the harbour's test among them |
| **The final tier with shard 2's rerun** in place of its first | `acd85fa` | **8,608 passed, 8 skipped, 1 xfailed** (8,617); no failure |
| **The slow tier of her files**, pace tests excepted (`--slow -m "slow and not pace"`) | `acd85fa` | **209 passed, 8 xfailed**, no failure (46 minutes): `tests/test_known_truths.py` 197 and its eight marked xfails, the base's eight (§5); `tests/test_range_audit.py`'s 11 sweeps; `tests/test_neufchatel.py`'s 1 |
| The 13 pace tests of `tests/test_known_truths.py` | | **not run**: they want the machine to themselves, and the coordinator runs them |
| The generator into scratch, and `cmp` of every committed ship file | `acd85fa` | 19 of 19 byte for byte |
| `tools/check_viewer_guns.py` on her file | `acd85fa` | clean: "fit '1817': 24 guns: 22 port, 2 over the rail" |
| `ruff check` and `ruff format --check` on her Python files | `acd85fa` | clean; no line the branch adds is over 100 characters |

**The final tier beside the base, test by test** (`acd85fa` against 00382c4):
- **only in her tree: 109**, all passed. 29 are her own tests (`tests/test_diana.py`). 79 are her
  cases of the tests over every file, 58 of them in `tests/test_view_geometry.py`. The last is the
  schooner-mast guard renamed "nineteen files" from "eighteen" by her file (133ccb3, TuningNotes).
- **only in the base: 1**, that guard's old name.
- **outcome changed: 1**, `tests/test_harbour.py::test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered`,
  passed on the base and failed in her final tier's shard 2. Its row for the officer's station read
  `""` where the scenario's plan says `"a model"`. **It is a race in the harbour's start, not her
  file's.** The start (`freesail/ui/harbour.py`, under the harbour's lock) sets the game started,
  then reads and parses the scenario's plan of its stations (`self.plan(scenario)`), and only then
  files the game with its plan. The game's state is read meanwhile under the driver's lock, not
  the harbour's. So a state read in that gap shows the game started with no plan (`chosen` still
  `{}`), and the page (`client/harbour.js`, the table's `plan[station]`) draws the table from it
  with the plan's column empty until its next read. The test reads the table as soon as its first
  row is drawn, and under four workers its read fell in the gap. Nothing on this branch touches
  the harbour, its page or its test. The same test passed in the
  first run's shard 2 at `72127c9`, and `acd85fa` changes only `tests/test_range_audit.py` and a
  line of TuningNotes. It passed five times of five alone on the head, and again in shard 2 whole,
  run again on its own. With that rerun in place of the shard's first run, **no outcome differs
  from the base**. Not mine to mend: the start's plan, the stations table and its test are
  package 96b's, step 9. Recorded for the lead.
- **the skips and the xfail** are the base's, the same tests.

### 8.5 Her open questions now

For the lead:
- the two viewer departures of §8.2 item 1, (a) and (b);
- the pounds of §8.2 item 2;
- the harbour test's race of §8.4.

The rest of §6 is answered by nudge 32. For the owner: none new.

**I stop here, at the owner's stopping point 1.** This section is the branch's last commit.

## 9. Her hash brought onto the package's branch at 329648e9 (nudge 58, 2026-11-23)

The lead's nudge 58 (the trunk at ec28f4cd, `docs/dev/M7-WorkPackages.md`): "**The Diana:** yes,
bring her hash onto `…/pkg-90` now and name what is resolved by hand; **hold her tiers until
A4's verdict.**" So this section merges the package's branch into hers, gives her a row in each
new table over every file, runs the checks and the review lenses with their fixer, and sets out
her gate. **Her fast and slow tiers whole are not run**, as the lead holds them. They run on the
hash sent when A4's verdict comes, after a further merge of the package's branch if that verdict
brings a mend. Commands here run with `python`, since this container has no `py` launcher.

### 9.1 The merge, and every line resolved by hand

- **Merged the package's branch at 329648e9** (A2's re-mend, A3 the helm, A1a to A1d the whole
  lateen, A5 and A6 the yard's level and the pole, A4 the boat in tow, and the trunk at 9c95644b)
  into hers at 0305040, under my user's standing permission (§0), as the merge commit `defc026`.
  It is 169 commits on the package's side, over 115 files. No rebase, no force, no other branch
  touched.
- **Resolved by hand: one file, `docs/dev/TuningNotes.md`, at its end and nowhere else.** Both
  sides had added sections after the text they share, 00382c4's:
  - the package's side, from "### Second pass: the lead's list of nudge 34 (2026-11-20)" to "##
    Package 90, with A4's hash: the pole evolutions' marks glossed where they are served (the
    lead's nudge 56, 2026-11-23)" and its last line, 980 lines;
  - hers, from "## Package 90, the Diana: her file, her tuning and the pins she moves
    (2026-11-20)" to the end of "### The Diana: the lead's rulings of nudge 32", 139 lines.

  Both are kept whole, the package's first and then hers, as at the merge of 00382c4. Checked: the
  resolved file is 329648e9's text exactly, followed by her sections exactly, and no marker is
  left. The package's other changes inside the shared text merged without conflict.
- **Merged by git, and read after it**: `freesail/world/ships.py`, `tests/test_known_truths.py` and
  `tests/test_probes_90.py`. Against 329648e9, each differs by her lines alone: her description row
  and her rank words; truth 7-190's tenth file, truth 7-590's count, and package 119's
  `_MUSTERED_AFTER_119`; and stage 0's `FILLED`.
- **The generator on the merged tree**, into scratch: **19 of 19 files byte for byte** with the
  committed ones. Her file is written as committed, so nothing was regenerated, and the eighteen
  others are the package's own.

### 9.2 Her rows in the package's tables over every file

In `ff5bfc0`. Each row is read off her file as committed by the test's own reader. Each table's
other rows are as the package has them, and no other ship's figure moved. Old beside new in
`docs/dev/TuningNotes.md`, "The Diana on the package's branch at 329648e9".

| Table | Old | New | Read off her file |
|---|---|---|---|
| `COMMITTED_YARD_LEVELS` (`tests/test_yard_level.py`), held both ways | no row; 91 yards | her row; 103 yards | `ship.yard_level` of her twelve yards, the frigate-36's at the same levels (each mast's lower yard 0, its topsail, topgallant and royal 1 to 3; the mizen's crossjack 0); the old formula by its spar agrees |
| `BRACES_SQUARE_SET` (`tests/test_rig_words.py`) | eighteen rows, eight with after braces | nineteen, nine: hers `"after braces"` | four head yards on the fore and eight after yards; her after braces manned and worked as filed and with every square sail set; not one-masted |
| her evolutions against her watches (`tests/test_diana.py`, her own) | 110: 83 numbered, 27 all hands' work | 113: 85 and 28 | the package's `take_in_pole` and `furl_pole` (A5 and A6) numbered and manned whole by either watch, `change_lateen` (A1a) all hands' work by its file; every other evolution's answer as before, compared one by one against her branch at 0305040 |
| stage 0's `KEY_CARRIERS` (`tests/test_probes_90.py`), held both ways | no row | no row | she carries none of the four keys: no `helm` in her hull (so the wheel by default), no sweeps, no boat towed, no whole lateen; its case on her file passes |

The package's other cases over every file pass on her file as committed:
- `tests/test_helm_kind.py`: the wheel, with no `helm` key;
- `tests/test_pole_mast.py`: no pole;
- `tests/test_boat_towed.py`: no boat in tow;
- `tests/test_lateen_whole.py`: five cases, no whole lateen.

Before her rows, the run of §9.3 failed three tests, the two yard-level cases on her file and her
evolutions' count. No other test failed.

### 9.3 The checks on the merged tree

| Check | Tree | Result |
|---|---|---|
| `ruff check .` and `ruff format --check .` | `ff5bfc0` and `2fba3b3` | clean, 432 files; no line the branch adds is over 100 characters |
| The generator into scratch, and `cmp` of every committed ship file | `defc026`, `ff5bfc0` and `2fba3b3` | 19 of 19 byte for byte |
| `tools/check_viewer_guns.py` on her file | `ff5bfc0` and `2fba3b3` | clean: "fit '1817': 24 guns: 22 port, 2 over the rail" |
| The package's changed test files, the guards over `data/ships` and the files with her cases: 42 files, the fast cases (not the tier whole) | `defc026` | 3,842 passed, 5 skipped, 1 xfailed, **3 failed**: her rows wanted (§9.2) |
| The three edited test files whole, and her 13 cases of the package's tables | `ff5bfc0` | 153 passed; 13 passed |
| The same 42 files, after the lenses' mends | `2fba3b3` | **3,846 passed, 5 skipped, 1 xfailed**; no failure (her row of `BRACES_SQUARE_SET` the one test more) |
| Her tack, wear, heel and heave-to at seed 7, by the truths' helpers, on both trees | `0305040` and `ff5bfc0` | the same to the second and the hundredth: tacks 206, 215 and 216 s (ground lost 28, 42 and 46 m); wear 492 s; heel in 22 kn 8.10 and 12.61 deg; weather helm in 15 kn 0.82 and 2.02 deg; hove to in 126 s at 56.3 to 57.4 deg off and 1.12 kn, never aback; filled away in 59 s and settled in 156 s |
| The review lenses (Plan §10.2, `Build-Ships.md` §17), read by a reviewer who is not her builder | `ff5bfc0` | nothing blocks her gate; four word mends made in `2fba3b3`, four records for the lead (§9.4) |

No harbour or browser test failed on the merged tree, in either run (nudge 35's ask).

### 9.4 The review lenses, and the fixer's mends

The eight lenses were read on `ff5bfc0` by a reviewer who is not her builder, through her files,
her rows, her notes and the lead's rulings, with targeted tests and probes of their own. **Nothing
blocks her gate.** Lenses 3 (the generator), 6 (the engine's keys: she sails as she did under the
helm, the yard's level, the pole, the boat in tow, the whole lateen and the sweeps) and 7 (names,
pace and checkpoints) found nothing. Old beside new in `docs/dev/TuningNotes.md`, "The Diana's
review lenses at ff5bfc0, and the fixer's mends".

**Mended in `2fba3b3`, words only.** Her file was regenerated by the generator and moved by its
notes alone; her figures and the eighteen are unmoved.
1. **Her length's ratio** (lens 1). Her note and §2.1 above said "124 pies x 0.99", a wrong ratio:
   124 x 0.99 pies is 34.21 m. Her 11,886.8 px at 96.1 a pie is **123.7 pies, 0.998 of the table's
   124**. The filed 34.47 m is her measuring note's, and unmoved. The same words stand in her
   measuring note (`docs/design/ships-design/pages-diana.md:216`), which is step 1's and not in my
   row, so it is recorded here and not edited.
2. **What her design puts in her note** (lens 1; lens 6, the `sweeps` key). Dia-D §3.3 and §13
   say her hawse holes, chains and deadeyes, sweep ports and paint are "said in her note"; only
   the hammock rail was. They are now in her profile's note: the hawse holes at (16.72, 2.40) and
   (16.92, 2.40); the chains' deadeyes at the rail; the small square openings read as sweep ports
   (JUDGEMENT), with no sweeps filed, since no source says she rowed; her paint by the 1809
   drawing.
3. **Her rank's wording** (lens 1). Three lines still said her rank at the rig's distance is "the
   lead's to rule": her description's note, `freesail/world/ships.py`'s comment and her test's
   docstring. They now say it is held as designed by nudge 32.
4. **Three persons named where "his" stood** (the rule): Adye, Steel and Meyer, in her module, her
   test and her TuningNotes.

**Recorded, for the lead:**
1. **Her spanker is the frigate-36's scaled, not cut on her own spars** (lenses 2 and 8). It is
   the cause her headsails were mended for in `e561b0d`, and the spanker was not looked at then.
   - Its area and centre are the frigate's scaled from the deck, 111 m2 at 7.8 m above her water.
     Her boom was raised to 2.9 m to clear her taffrail, and the figures were not cut again.
   - Cut by her note's rule on her own boom and gaff, it would be 95 m2 with its centroid at
     9.7 m (the reviewer's reckoning). The frigate's own filed figure is 106% of its cut, with its
     centre 1.75 m under its centroid.
   - **I sailed a variant** at the frigate's ratios, 101 m2 at 8.3 m, at seed 7 by the truths'
     helpers. Her weather helm close-hauled in 15 kn goes from 0.82 to **0.00** deg, under truth
     D's 0.5. Her tacks from 290, 292.5 and 295 deg go from 206, 215 and 216 s to **223 s and two
     missed stays**, outside truth E. Her heel, wear and heave-to barely move.
   - So the mend would fail truths D and E and want `clr_x_m` tuned again. I have not made it at
     her gate. It is the lead's to rule: hold the spanker as filed (JUDGEMENT, the frigate's
     scaled, as her note says), or cut it on her spars and tune her helm again.
2. **Her bow port stands 0.24 m outside her drawn side at its sill** (lenses 4 and 5). Its
   half-breadth, 2.1 m (JUDGEMENT +-0.2), is beyond the judgement's own band. The generator reports
   it ("-0.24 m; more than 0.05 m at x 15.96, reported and never moved"), and her test holds it.
   The viewer draws the 1817 fit's two bow obuses there, outboard of her planking
   (`freesail/api/viewer_guns.py`, the muzzle at the triple's half-breadth), and
   `check_viewer_guns` checks only that the side is there. It was said in no report before this.
3. **Truth 9 on her file, measured, not asserted** (lens 2). The truth's cases are the
   frigate-36's and the schooner's. On her file, in 20 kn under plain sail for 20 minutes, nothing
   carries away, no line parts and no strain warning is raised. In 35 kn under all sail, her main
   royal yard, her fore and mizzen royal masts and her fore topgallant yard carry away, each
   urgent, with 44 strain warnings. The reviewer's probe, run again by me.
4. **Two audit ceilings moved beyond nudge 32's wording** (`4dec517`: `u-ships` 18 to 19,
   `x-words:ship-words` 17 to 18, §8.2 item 3). Each is old beside new with its reason, as every
   file's era notes carry their years, but the ruling named only her entry and truth 7-590's
   count.

### 9.5 Her gate, in the lead's words

- **Her files by the generator, byte for byte.** `tools/ships/diana.py` writes
  `data/ships/corvette-20.yaml` as committed, on the merged tree (§9.3). Her figures last changed
  in `2cd5caa`, by the nudge 32 rulings (§8.2); the merge left her file as it was, and the lenses'
  mends moved its notes alone (§9.4).
- **The eighteen unmoved.** The other eighteen files are 329648e9's exactly (`git diff 329648e9
  ff5bfc0 -- data/ships` names her file alone), and the generator writes each byte for byte.
- **The guards' tables with her rows.** Each grows by her row alone, no other ship's figure moved,
  and each moved count has its old figure beside it:
  - `tests/test_view_geometry.py`: her rows of nudge 32 and the two departures (§8.2 item 1);
  - `tests/test_known_truths.py`: truth 7-190's tenth file, truth 7-590's count 61, and package
    119's truths 7-700 and 7-701 (§8.3);
  - `tests/test_neufchatel.py`'s rows by intent (§8.3); `tests/test_magazine.py` (§8.2 item 2);
  - `tests/test_lee_ports.py`'s row, 18.50 deg with four ports;
  - `tests/test_schooner_mast.py`'s nineteen files; `tests/test_profile.py`'s and
    `tests/test_probes_90.py`'s filled module;
  - `tests/test_range_audit.py`'s count of the data's entries, and the known list's ceilings
    (§8.2 item 3);
  - and the package's new tables (§9.2).
- **Her truths as bands** (`tests/test_diana.py`), each passing on the merged tree:

  | Truth | Holds | Band | Hers |
  |---|---|---|---|
  | 7-660 | her particulars hold their sources | the table's measures within 0.01 m; her mass the drawn body's middle, 470,000 kg; the table's 498,000 kg beside it | as filed |
  | 7-661 | Meyer's speed, wind abaft the beam in a fresh breeze | 9.5 to 11.5 kn (truth B) | 10.28 to 11.29 |
  | 7-662 | stiff, as her captain said | heel in 22 kn within 1.15 times the frigate-36's, and under 18.5 deg (truth C) | 1.10 and 1.12 times |
  | 7-663 | she steers well | weather helm in 15 kn 0.5 to 3 deg close-hauled, 1 to 3 abeam (truth D) | 0.82, 2.02 |
  | 7-664 | she goes about as a small ship does | each tack 180 to 330 s (truth E, nudge 32); the wear 360 to 720 s (truth 11) | 206, 215, 216; 492 |
  | 7-665 | her midship lee port | its sill dips at 21.1 deg (+-0.05) and L2 shuts it at 18.50 (+-0.05), both held | 21.1; 18.50 |
- **The lead's rulings, each shown** (nudge 30's mass; the rest nudge 32's):
  - her drawn displacement: 470,000 kg, her body drawn outside the plank to her line; the
    generator's drawing 448 t beside it (-5%), recorded (§2.5);
  - the viewer's rows: §8.2 item 1, with the two departures for the viewer's step;
  - the charges: a foreign gun's its kind's share, `tests/test_magazine.py` (§8.2 item 2);
  - her ports of 1817: the long 12s in ports 5 to 10, the carronades in 1 to 4 (§8.2 item 5);
  - no stern lights filed (§8.2 item 5).

### 9.6 Her figures: measured, Winfield's by page, or judgement

Each figure's own note in her file says which it is; §2.1 gives each clause with its source, and
§2.6 every judgement. In short:
- **Measured off her plan** (her measuring note, "Pages", by section):
  - her length on the line, 34.47 m (§4.1); her draught, 3.78 m to K (§4.2);
  - her body's displacement outside the plank, 465.6 to 473.6 t (§4.3 to §4.5);
  - her profile's points: the rabbet, the stem, the post and the knuckle (§3.1, §4.1, §5.1);
  - her deck at side, 1.33 m (§5.2); her stem head, 5.09 m (§5.4); her rudder, 3.0 m2 on a span
    of 3.90 m (§5.5); her lateral plane, 122.2 m2 (§5.6);
  - her eleven ports a side, their sills and half-breadths (§5.7); K (§6.2);
  - her masts' places and rakes, off the plan.
- **Winfield et al. 2023, by page:**
  - p. 930, her entry: the table's eslora of 124 pies, her breadth of 32 pies 6 pulgadas (9.06 m),
    her depth in hold of 16 pies, the table's 540 toneladas 691 libras, her 335 toneladas de arqueo,
    her company of 167, her fits by their dates, and the 1817 fit's long 12s, carronades and obuses;
  - pp. 41 to 46: the pie de Burgos and the libra castellana, 0.4608 kg;
  - p. 1446 and following: the regulation of 1788's fifty soldiers.
- **From other sources, by page:**
  - Luce 1866 ch. VII, her masts and yards on her particulars, against Steel's 20-gun column;
  - Roos 1957 p. 94, Meyer's words, for her speed, stiffness and steering;
  - Falconer and Douglas, her guns' crews;
  - Steel 1805 p. 240, once for her lights, now none filed.
- **Computed by rule:**
  - her hull speed, 11.8 kn, the frigate's by the root of the lengths;
  - her masthead, 29.0 m, and her plain sail, 1,054 m2;
  - her ground tackle, by Luce's rule on 449 tons burthen; her hold, 45 tons;
  - the table's 498.0 t, at the book's libra.
- **JUDGEMENT** (42 notes in her module say so):
  - her GM, 1.75 m, and `clr_x_m`, 2.8 m, each tuned to her captain's word (truths C and D);
  - the plank, 3 to 4 pulgadas, so her mass the middle of the range;
  - K as a false keel, the upper red line as her deck at side, the stern's reading, the bow port's
    half-breadth;
  - her company's shares beside her soldiers, one company for every fit;
  - the obús's weight and crew, the long 8's weight, the 1817 ports and the obuses' places;
  - her boats; her burthen of 449 tons for the English helpers;
  - her headsails, spanker, rope, staysails and stores scaled from the frigate-36;
  - her idlers by trade; `sections_m`'s carried half-breadths (marked `judged`);
  - her stem head a centimetre forward; `keel_m` at K; her bow port's half-breadth (§9.4);
  - the small openings between her ports read as sweep ports;
  - no stern lights, until the owner's sheets show them;
  - truth E's band: the floor a small ship's quickness in stays, the ceiling half again her slowest
    tack.

### 9.7 Now

Her hash for the lead's queue is the commit that adds this section, the branch's head. Her tiers
wait for A4's verdict. When it comes, I merge the package's branch again if the verdict brings a
mend. Then I tier the exact hash I send: the fast tier whole beside a base on the merged tree, and
the slow tier of her files with the pace tests excepted.

For the lead: her spanker (§9.4, record 1), the one that would move her figures; her bow port
(record 2); the audit's two ceilings (record 4). For the coordinator: her measuring note's "124
pies × 0.99" (§9.4, mend 1), which is not in my row. For the owner: none new.

## 10. The lead's rulings of nudge 59 on her four records (2026-11-23)

The lead's nudge 59 (the trunk at a8913da6, `docs/dev/M7-WorkPackages.md`) ruled the four records
of §9.4 before her tiers. A4's verdict is not in, so her tiers stay held. Old beside new, with
every figure, in `docs/dev/TuningNotes.md`, "The Diana: the lead's rulings of nudge 59 on her four
records". The work is in `79ed403`.

### 10.1 Her spanker cut on her own spars: stopped, as the ruling says

"If she will not hold both D's and E's bands with the spanker she can carry, stop and say what she
does." She will not, so I stopped. **Her file keeps the spanker as it stood, 111 m2 at 7.8 m**,
and nothing of the cut is filed.

**The cut**, by her note's rule worked afresh on her spars as filed:
- the boom 10.9 m at 2.9 m above her deck, the gaff 8.7 m with its jaws at 11.8 m, her deck 1.33 m
  above her water, as the physics reads a spar's height;
- the foot 0.9 of the boom, the head 0.9 of the gaff peaked 40 deg, the luff the hoist from boom to
  jaws;
- so **95.0 m2, its centroid 9.71 m above her water**, and 4.35 m abaft the mast, which is the
  note's own "0.4 of the boom" (4.36 m). The rule closes on itself, and the reviewer's figure
  stands. Filed it would be 95 m2 at 9.7 m, its x -16.6 (old -16.1).
- Taken with the mizen's 6-deg rake, which the rule does not name, it is 92.7 m2 at 9.65 m.
  Recorded, not used.

In her module it is `spanker_figures` working those four corners (tack, clew, peak, throat) from
`spanker_spars`, the boom and gaff her rig files, in place of the frigate's figure scaled. Through
the generator it would move:
- the spanker's area, centre and x, and its cloth's rating, 35.5 to 30.4 kn;
- her plain sail, 1,054 to 1,038 m2, and so her rope's scale, 0.816 to 0.810;
- 56 ratings, through her rope's scale and her spars' design wind.

The eighteen would not move.

**What she does with it**, at seed 7 by the truths' helpers, GM 1.75 and her rudder as measured,
`clr_x_m` tuned from 2.0 to 4.2. The whole scan is in TuningNotes.

| `clr_x_m` | Weather helm in 15 kn, close-hauled and abeam | Tacks from 290, 292.5 and 295 deg | Truth D | Truth E |
|---|---|---|---|---|
| 2.6 | -0.48, 1.46 deg | 235, 238, 241 s | no: lee helm | yes |
| 2.75 | -0.10, 1.70 | 226, 229, 229 | no: lee helm | yes |
| 2.8, as filed | 0.12, 1.78 | 223, 226, missed stays | no | no |
| 2.94 | 0.56, 2.01 | 213, missed stays, missed stays | yes | no |
| 3.0 to 3.6 | 0.73 to 2.54, 2.11 to 3.02 | missed stays from two headings, then all three | yes | no |

- **Close-hauled, she carries lee helm until `clr_x_m` about 2.93.** Truth D asks 0.5 to 3 deg of
  weather helm.
- **From there she misses stays from 292.5 and 295 deg**, each miss said 79 to 91 s after the
  order. Truth E asks all three tacks in 180 to 330 s.
- No figure holds both bands. Where E holds (2.75 and below, but for a miss from 295 at 2.7), D
  fails.
- Her heel in 22 kn stays 8.16 and 12.63 deg throughout, inside truth C's band. Her wear stays
  492 s, inside truth 11's. She heaves to in 135 s at 2.6 and in 123 s at 2.94.

**So the lead's choice is which truth to restate as measured**, or whether to keep the larger
sail. Restating D means lee helm close-hauled with the cut sail, -0.10 deg at 2.75, with her three
tacks inside E. Restating E means two of three tacks missed from 2.94 up, with her helm inside D.

**Her viewer's picture would not move with the cut.** The viewer draws a gaff sail with a boom
between its spars' ends (`client/projection.js`, a gaff sail with no `corners_m`), not from its
area or centre, and her boom and gaff are unchanged. What the owner saw ("she looks right to me")
is the sail her spars draw, and the cut leaves it as it is.

### 10.2 Her bow port on her drawn side: filed

- **Old: 2.1 m, JUDGEMENT +-0.2, 0.24 m outside her drawn side at its sill. New: 1.86 m, her drawn
  side's at its sill** (x 15.96, sill 2.38). It is read with `freesail/ship/form.py`'s
  `half_breadth_at` on her drawn lines, the generator's own hull: 1.861 m, computed.
- Her drawn hull is unmoved by it (448 t, 3.26 m deep), since the bow port is not among the
  sections the hull is drawn from.
- The generator now holds all eleven ports within 0.05 m of her drawn side. Before, it held ten
  and reported the bow port.
- The 1817 fit's two bow obuses stand in her side, 0.24 m inboard of where they were drawn.
- Her file moved by that triple and its note alone. Her test's ports and the generator's report
  line it holds moved with it, old beside new.

**`check_viewer_guns` is left as it is.** I ran the rule over every committed file first: a gun in
a port or over the rail whose half-breadth stands more than 0.05 m (the generator's
`PORT_GAP_M`) outside the drawn side at its sill. It fails five committed ships, so by the ruling
it is not added. Each ship's most outboard:

| Ship | Most outboard | Where |
|---|---|---|
| the brig | +0.051 m | her Diligence fit's guns 2 |
| the hermaphrodite brig | +0.153 m | her 1814 fit's bow chasers, and six ports more |
| the razee | +0.350 m | her bow chasers of 1796; her ports 3 to 7 +0.05 to +0.18 |
| the 74 | +0.180 m | her quarterdeck's ports 2 to 7, and her lower and upper ports 14 |
| the 64 | +0.097 m | her lower ports 4 to 7 and upper 3 to 6 |

The other eight armed files pass it, and so does hers, at +0.015 m (her place over the rail).

### 10.3 Truth 9, and the two audit ceilings

- **Truth 9 on her file** is noted by the lead as measured, as a ship of her force should be
  (§9.4, record 3). Nothing changes.
- **The two audit ceilings**, `u-ships` 18 to 19 and `x-words:ship-words` 17 to 18, are allowed by
  the lead, old beside new with their reasons as filed in `4dec517`. Nothing changes.

### 10.4 The checks on the head

| Check | Tree | Result |
|---|---|---|
| `ruff check .` and `ruff format --check .` | `79ed403` | clean, 432 files; no line the branch adds is over 100 characters |
| The generator into scratch, and `cmp` of every committed ship file | `79ed403` | 19 of 19 byte for byte |
| The eighteen | `79ed403` | `git diff 329648e9 79ed403 -- data/ships` names her file alone |
| `tools/check_viewer_guns.py` on her file | `79ed403` | clean |
| Her tests, the viewer's, the guns', the lee ports' and the magazine's | `79ed403` | 1,523 passed |
| Truths 7-190, 7-665, 7-700 and 7-701, and her cases of the known truths | `79ed403` | 17 passed |
| The 42 targeted files of §9.3 | `79ed403` | **3,846 passed, 5 skipped, 1 xfailed**; no failure, no harbour or browser test among any |

### 10.5 Her gate list now

As §9.5 sets it out, with two changes:
- her bow port's half-breadth leaves §9.6's judgements and is computed off her drawn lines;
- her truths D and E stand on the spanker as filed, 111 m2 at 7.8 m, until the lead rules on
  §10.1.

The rest is as it stands: her files by the generator, the eighteen unmoved, the guards' tables
with her rows, her truths as bands, and the rulings of nudges 30 and 32 each shown.

### 10.6 Now

Her hash for the lead's queue is the commit that adds this section, the branch's head. For the
lead: §10.1, which truth to restate, or whether the larger sail stays. Her tiers wait for A4's
verdict, and for the spanker's ruling if it moves her file. Then I tier the exact hash I send, the
fast tier whole beside a base on the merged tree and the slow tier of her files, pace tests
excepted. For the owner: the spanker's restatement, if the lead puts it to them.

## 11. Her spanker as her spars carry it: the owner's (a) (2026-11-23)

The owner's word, in Decisions Part F, row D-s2 (on the package's branch at a6f7bc95): "My
apologies, I answered the lead but wasn't aware you had an open question here with a different
(a). Let's go with (a), as told to the lead." It supersedes row D-s ("Steel's boom, then
measure"), and the lead's nudge 64 withdraws nudge 63. So, by the lead's nudges 61 and 62:
- the spanker her spars carry, with her tacks kept;
- `clr_x_m` chosen by the wide table;
- truth D restated as measured.

Old beside new, with the whole table, in `docs/dev/TuningNotes.md`, "The Diana: her spanker as her
spars carry it". The work is in `36b4a3e`.

### 11.1 Her boom's ground, as it is

- **Her boom**, 10.9 m, is half her main mast by Luce's chain: **a rule, not a source**.
- **Steel's 20-gun ship of 429 tons**, her near comparator, lists a driver boom of 45 ft 6 in
  (13.9 m; Steel 1794 vol. I p. 50: Pages §7), 28% longer. It is known and not used, by the
  owner's word.
- **Her gaff**, 8.7 m, is Luce's 4/5 of the boom, the length of Steel's mizen yard (28 ft 6 in).

Both notes in her file now say so. Before D-s2 arrived, I had measured Steel's boom at one seed:
her rule cuts 114 m2 at 9.6 m on it. That figure is recorded and not used.

### 11.2 The spanker, and what it moved

- **Old:** the frigate-36's 167 m2 scaled by her chain, 111 m2 at 7.8 m above her water, x -16.1.
- **New: 95 m2 at 9.7 m, x -16.6**, cut on her boom and gaff by her note's rule (`spanker_figures`
  working from `spanker_spars`; §10.1 gives the method).
- Through the generator, her plain sail goes from 1,054 to 1,038 m2 and her rope's scale from 0.816
  to 0.810. The spanker's cloth rating and 56 ratings move with them.
- Her spars and the eighteen are unmoved.

### 11.3 The wide table, and the figure

Her tacks from 290, 292.5 and 295 deg, in 8, 12, 15, 20 and 25 kn, at seeds 1 to 8, with her helm
close-hauled and abeam at each wind and seed. **The eight seeds agree to the tick in every cell.**
The truths' scenario has no gusts and no wind shifts, so a seed reaches nothing her going about
reads, and the spread is across the winds and headings.

| `clr_x_m` | Stayed, of 120 | 15 kn | Helm close-hauled, 8 to 25 kn |
|---|---|---|---|
| 2.600 | 56 | all three, 235 to 241 s | -0.63 to -0.31 deg |
| 2.625 | 56 | all three, 233 to 240 | -0.55 to -0.22 |
| **2.650** | **56** | **all three, 232 to 238** | **-0.47 to -0.14** |
| 2.675 | 56 | all three, 231 to 237 | -0.39 to -0.05 |
| 2.700 | 48 | **missed stays from 295** | -0.32 to +0.03 |
| 2.725 | 56 | all three, 228 to 231 | -0.24 to +0.12 |
| 2.750 | 56 | all three, 226 to 229 | -0.16 to +0.11 |
| the sail as it was filed, 111 m2 at 2.8 | 56 | all three, 206 to 216 | +0.69 to +1.13 |

In every row:
- **12 kn:** she stays from all three headings.
- **8 kn:** she stays only from 290.
- **20 and 25 kn:** she does not stay at all.

Each tack not made is a missed stay, said 59 to 107 s after the order.

- **What the larger sail bought:** weather helm close-hauled, inside the old band, and tacks in
  15 kn quicker by 22 to 26 s. It bought no tack the smaller sail does not make, in any wind
  measured.
- **The figure, 2.65 (JUDGEMENT).**
  - From 2.6 to 2.675 she stays in every cell this band has, and at seed 7 her tacks held down to
    2.0. At 2.7 she misses from 295 in 15 kn. 2.725 and 2.75 are a narrow island between that miss
    and the one at 2.8.
  - In the broad band, 2.65 is the lowest figure at which her close-hauled helm is within half a
    degree of amidships at every wind measured. That is 0.05 short of the miss at 2.7.
  - At 2.625 her close-hauled helm in 8 kn is -0.55 deg, outside the half degree.

**For the lead: she misses stays in 20 and 25 kn under plain sail from all three headings, with
either sail.** The frigate-36 stays from 292.5 in both, in 232 and 248 s. Truth E tests 15 kn
alone, so no truth caught it. It is in her file as it was before this change, and is not the sail's
doing.

### 11.4 Truth D restated, and her other truths

**Truth D (7-663), restated as measured:**
- **Old:** close-hauled in 15 kn, 0.5 to 3 deg of weather helm, and abeam 1 to 3, Meyer's "steers
  splendidly". She met it at 0.82 and 2.02.
- **New: close-hauled, her helm within half a degree of amidships; abeam, 1 to 3 deg of weather
  helm.** She meets it at **-0.33 and 1.54**.
- The reason is in the test's docstring and TuningNotes: with the 95 m2 her spars carry, no
  `clr_x_m` gives her that weather helm close-hauled and her tacks too, and the owner chose the sail
  and her tacks.

Her other truths, measured again at seed 7 by the truths' helpers. The old figures are with the
frigate's spanker scaled.

| Truth | Band | Old | New |
|---|---|---|---|
| B (7-661), Meyer's speed | 9.5 to 11.5 kn | 10.28 to 11.29 | 10.30 to 11.26 |
| C (7-662), heel in 22 kn against the frigate-36's | 1.15 times at most | 8.10, 12.61 deg (1.10, 1.12) | 8.17, 12.63 deg (1.11, 1.12) |
| E (7-664), each tack | 180 to 330 s | 206, 215, 216 s; ground lost 28, 42, 46 m | 232, 235, 238 s; 34, 44, 56 m |
| the wear, truth 11's | 360 to 720 s | 492 s | 492 s |
| F (7-665) and 7-660 | as filed | as filed | unmoved |
| hove to; filled away and settled | | 126 s at 56 to 57 deg, 1.12 kn; 59, 156 s | 133 s at 59.8 to 60.1 deg, 1.16 kn; 59, 140 s |
| truth 9, measured and not asserted | | 20 kn: nothing; 35 kn: her main royal yard, fore and mizzen royal masts and fore topgallant yard, 44 warnings | 20 kn: nothing; 35 kn: her three royal masts and the fore topgallant yard, each urgent, 50 warnings |

### 11.5 Her viewer's picture

**It does not move.** The viewer draws a gaff sail with a boom between its spars' ends
(`client/projection.js`), reading neither its area nor its centre, and her boom and gaff are
unchanged. Her 66 cases of the viewer's tests pass with her rows as they stood: the boom's frame,
the sheet's end, and the boom over her taffrail. What the owner looks at live is what they saw.

### 11.6 The checks on the head

| Check | Tree | Result |
|---|---|---|
| `ruff check .` and `ruff format --check .` | `36b4a3e` | clean, 432 files; no line the branch adds is over 100 characters |
| The generator into scratch, and `cmp` of every committed ship file | `36b4a3e` | 19 of 19 byte for byte |
| The eighteen | `36b4a3e` | `git diff 329648e9 36b4a3e -- data/ships` names her file alone |
| `tools/check_viewer_guns.py` on her file | `36b4a3e` | clean |
| Her own tests, `tests/test_diana.py` | `36b4a3e` | 29 passed |
| The 42 targeted files of §9.3 | `36b4a3e` | **3,846 passed, 5 skipped, 1 xfailed**; no failure, no harbour or browser test among any |

### 11.7 Now

Her hash for the lead's queue is the commit that adds this section, the branch's head. Her gate
list is §9.5's with §10.5's two changes, the second now settled: truth D restated, on the spanker
her spars carry. Her tiers wait for the engine's one A4 commit on the package's branch, as the
coordinator holds them. Then I merge the package's branch once more, and tier the exact hash I
send: the fast tier whole beside a base on the merged tree, and the slow tier of her files with
the pace tests excepted.

For the lead: her missed stays in 20 and 25 kn (§11.3). For the owner: none new.

## 12. Why she misses stays in a breeze: measured, nothing filed, for the lead (2026-11-23)

The lead's nudge 65 (the trunk at 85364f45) ruled the finding of §11.3: mend it before her gate,
with the cause found first. **I have found the cause, and the mend it points to is not mine to
make.** It is her displacement, which is the lead's ruling of nudge 30, and her rig against it.
Neither is one of my JUDGEMENT figures. By the ruling, a mend that moves more than those comes to
the lead first. **Nothing is filed.** Her file is as at 8ce21bd, and her tiers wait. Every run
below is a probe on a scratch copy of her file, read through the engine as it stands; no equation
or script was changed.

### 12.1 The plain figures, every committed square-rigged ship

Plain sail is what the game itself sets on "set plain sail", summed. The burthen is each file's
own, old-rule tons.

| Ship | Displacement | Burthen | Displacement / burthen | Plain sail | Per tonne | Rudder / lateral plane | Lateral plane / displacement |
|---|---|---|---|---|---|---|---|
| **the Diana** | **470 t** | **449** | **1.05** | **1,038 m2** | **2.21 m2** | **0.025** | **0.260 m2/t** |
| the frigate-36 | 1,270 | 933 | 1.36 | 1,584 | 1.25 | 0.037 | 0.126 |
| the razee | 1,925 | 1,384 | 1.39 | 1,899 | 0.99 | 0.030 | 0.147 |
| the 74 | 2,600 | 1,604 | 1.62 | 2,225 | 0.86 | 0.030 | 0.127 |
| the 64 | 2,170 | 1,384 | 1.57 | 1,803 | 0.83 | 0.029 | 0.141 |
| the brig | 413 | 316 | 1.31 | 766 | 1.85 | 0.037 | 0.194 |
| the merchant brig | 413 | 316 | 1.31 | 188 | 0.46 | 0.037 | 0.194 |
| the bilander | 229 | 128 | 1.79 | 196 | 0.86 | 0.037 | 0.280 |
| the hermaphrodite brig | 288 | 328 | 0.88 | 959 | 3.33 | 0.026 | 0.354 |

- **She is the lightest ship of war for her tonnage**, 1.05 where the others are 1.31 to 1.62. Only
  the hermaphrodite brig is lighter for hers, and she is a brigantine (below).
- **She carries more canvas to the tonne** than any ship but the hermaphrodite brig: 2.21 m2, the
  frigate-36 1.25 and the brig 1.85.
- **Her rudder to her lateral plane is the smallest** of the ships, 0.025.
- Her block coefficient to K is 0.39, the frigate-36's 0.55 and the brig's 0.50: a fine hull, and
  a light one, for her measured length, breadth and draught.
- The merchant brig's and the bilander's plain sail is what their books set on the order; it is
  not their whole rig.

### 12.2 A missed tack in 20 knots, tick by tick

From 292.5 deg, close-hauled on the starboard tack, settled as the truths' helpers settle her, her
`clr_x_m` 2.65. The yaw moments are read each tick: the sails' totals, each sail's own side force
on its lever from the centre of lateral resistance, and the rudder's by `hull.rudder_forces`.

| | The Diana | The frigate-36 | The brig |
|---|---|---|---|
| At the order | 6.47 kn, 67.4 deg off | 6.54 kn, 67.4 deg off | 6.05 kn, 66.0 deg off |
| Her swing at its peak | 1.89 deg/s at 13 s, 5.4 kn | 1.92 deg/s at 17 s, 5.6 kn | 2.76 deg/s at 13 s, 5.2 kn |
| **At "mainsail haul"** (her head within a point) | **48 s, 9.9 deg off: 1.86 kn, swinging 0.72 deg/s** | **42 s, 9.9 deg off: 3.30 kn, 1.18 deg/s** | 30 s, 8.5 deg off: 3.14 kn, 1.83 deg/s |
| The rudder then (hard over, 35 deg) | 51 kN m | 326 kN m | 96 kN m |
| After the haul, the after yards swung, then the square sails aback | -197 to -272 kN m: her swing stops in 4 s and turns back at up to 1.5 deg/s | -337 kN m at the most: her swing slows to 0.36 deg/s and carries her through | her after yards' swing opposes her by almost nothing |
| Her closest to the wind | **8.1 deg off, at 52 s, with 1.43 kn** | through it at 58 s, with 1.6 kn | through it |
| The end | **"Missed stays: she fell off on the old tack"**, at 68 s, two points off | tacked in 232 s | "tacked" in 459 s (below) |

- **The yaw inertia is the difference.** The engine's is the mass times her length's quarter
  squared, times 1.5, for every ship. Hers is 5.24e7 kg m2, a quarter of the frigate's 2.08e8.
  The same order of moment from the after yards (-272 against -337 kN m) stops her swing at 0.30
  deg/s every second, the frigate's at 0.09.
- **She comes to the haul with 56% of the frigate's way and 61% of her swing.** Her sails' drag
  aback in the luff is 1.5 times the frigate's per tonne (-17 kN on 494 t moved, against -30 on
  1,334), so her way goes sooner, and with it her rudder (its moment goes as the square of her way).
- **Her square sails per unit of yaw inertia**, area times lever from her centre of lateral
  resistance: her fore +61, her main -52 and her mizzen -41 (x 10^-6). The frigate-36's are +25,
  -18 and -20, the razee's +20, -14 and -12, the brig's fore +82 and main -58. **Her after yards
  stand 2.5 times the frigate's against her inertia.** Their centre about her lateral resistance is
  the frigate's (5.6% of her length abaft it, the frigate's 4.9%), so it is the inertia they act
  on, not their place.
- In 15 kn she fails the same way at the haul (8.8 deg off at the closest) but hangs, and the head
  yards box her off before she falls back two points. In 20 kn the yards' push is (20/15)^2 = 1.78
  times as strong, and she falls back in 12 s.
- The hermaphrodite brig carries more canvas to the tonne still and stays from every heading in
  every wind: she is square on her fore alone, and has no after yards to haul.
- The brig's 20-knot tack came through the wind, swung on round to her old tack, and was called
  "Tacked; braced up on the starboard tack, heading SW by S (211°)" at 459 s. That is the brig's
  and the script's, not my row: noted for the lead.

### 12.3 What moves it, each measured on a scratch copy

Her tacks from 290, 292.5 and 295 deg in 8, 12, 15, 20 and 25 kn at seed 7 (the seeds alike to
the tick, §11.3): **S** for stayed, **m** for missed stays.

| Variant (all else as filed) | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed, of 15 | Helm close-hauled, abeam in 15 kn |
|---|---|---|---|---|---|---|---|
| **as filed: 470 t, `clr_x_m` 2.65** | S m m | S S S | S S S | m m m | m m m | 7 | -0.33, 1.54 |
| 470 t, `clr_x_m` 3.0 | S m m | S S S | S m m | m m m | m m m | 5 | 0.73, 2.11 |
| 498 t (her table's), 3.0 | S S m | S S S | S m m | m m m | m m m | 6 | 0.70, 2.10 |
| 546 t, 3.0 | S S m | S S S | S S ? | m m m | m m m | 7 | 0.70, 2.10 |
| **597 t, 3.0** | **S S S** | **S S S** | **S S S** | m m m | m m m | **9** | **0.64, 2.10** |
| **611 t, 3.0** | **S S S** | **S S S** | **S S S** | m m m | m m m | **9** | **0.74, 2.10** |
| 700 t, 3.0 | S S S | S S S | S S S | S m m | m m m | 10 | 0.74, 2.09 |
| 800 t, 3.0 | S S S | S S S | S S S | S S S | m m m | 12 | 0.65, 2.09 |
| 950 t, 3.0 | S S S | S S S | S S S | S S S | S S m | 14 | 0.72, 2.09 |
| 1,100 t, 3.0 | S S S | S S S | S S S | S S S | S S S | 15 | 0.72, 2.08 |
| her lateral plane 108 m2 (the frigate's fill), 470 t, 3.0 | S S m | S S S | S S m | m m m | m m m | 7 | 0.41, 2.10 |
| her square sails 0.75 of their area, 470 t, 3.0 | S m m | S S S | S S S | m m m | m m m | 7 | 0.26, 2.12 |
| her square sails 0.85, 611 t, 3.0 | S S S | S S S | S S S | S m m | m m m | 10 | 0.76, 2.29 |
| her square sails 0.75, 611 t, 3.0 | S S S | S S S | S S S | S S S | m m m | 12 | 0.24, 2.11 |
| the frigate-36, as filed | S S S | S S S | S S S | S S S | S S S | 15 | 1.31, 1.99 |

(At 546 t the 295-deg tack in 15 kn had not ended in 900 s.)

1. **Her weight is the first cause, as the lead suspected.** At 597 to 611 t she stays from every
   heading in 8, 12 and 15 kn, **with truth D in its first band** (0.64 to 0.74 deg of weather helm
   close-hauled, 2.1 abeam, at `clr_x_m` 3.0). So a displacement re-ruled there would put D back to
   its first band, as the lead's ruling has it, and her tacks in light and working winds with it.
2. **It is not the whole of it.** By her mass alone she would want about 800 t to stay in 20 kn and
   1,100 t in 25. That is 1.7 and 2.3 times her filed displacement, which no reading of her plan
   gives. The
   rest is her canvas against her inertia. A quarter less square sail, with 611 t, stays in 20 kn
   but not in 25.
3. **Not her lateral plane.** Cut to the frigate's fill of length times draught, it changes nothing
   in a breeze.
4. **Under the sail a man-of-war carried in a breeze**, her topgallants taken in, she stays in 20 kn
   from all three headings (290, 269 and 219 s). In 25 kn she misses from 290 and 292.5 and stays
   from 295 (213 s). The frigate-36 stays so in both (244 to 317 s).

### 12.4 Her comparator, and her draught as drawn

- **What her drawn hull floats at each displacement**, by the form module's own integration carried
  above her line. Her drawn body is 448.4 t at her line, the generator's figure, and her plank is
  in her filed 470 t. Each tenth of a metre adds about 25 t.

  | Displacement | Her water raised | Draught to K (filed 3.78 m) | At the greatest section (drawn 3.26 m) |
  |---|---|---|---|
  | 470 t, as filed | 0 | 3.78 m | 3.26 m |
  | 498 t, her table's | 0.11 m | 3.89 | 3.37 |
  | 546 t | 0.30 | 4.08 | 3.56 |
  | 588 t, the brig's ratio on her 449 tons | 0.46 | 4.24 | 3.72 |
  | 611 t, the frigate-36's ratio | 0.55 | 4.33 | 3.81 |
  | 800 t | about 1.3 | about 5.1 | about 4.6 |
- **Her comparator.** Steel's 20-gun ship of 429 tons gives no displacement, only her spars. On the
  ratios of the ships we have (1.31 to 1.62), a ship of 449 tons burthen displaces about 590 to 730
  t. Her own table's is 498 t, at the book's libra.
- **Her measured line says 470.** Her arrowed load line on her plan, the lead's ruling 1, floats her
  drawn body at 448 t, 470 with her plank. To float her at 590 to 610 t she would lie about half a
  metre below her plan's line. So her plan and her tonnage disagree: either her drawn body is a
  light ship's, as it measures, or her line is drawn light. That is the lead's to rule, with the
  owner's sheets if they show her draught.
- **Her rig is Luce's chain on her particulars.** Steel's 20-gun column is shorter in every yard
  (the main yard 3%, aloft 6 to 10%, the crossjack 14%: Pages §7). On her inertia, the rig carries
  the rest of the fault in a breeze.

### 12.5 Truth E across the winds: the count that stays

Her tacks from the three headings in 8, 12, 15, 20 and 25 kn at seeds 1 to 8:

| | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed, of 120 |
|---|---|---|---|---|---|---|
| **the Diana, as filed** (95 m2, `clr_x_m` 2.65, 470 t) | 8 of 24 | 24 | 24 | 0 | 0 | **56** |
| **the frigate-36, as filed** (`clr_x_m` 3.0) | 24 | 24 | 24 | 24 | 24 | **120** |

The frigate-36's eight seeds agree to the tick as hers do, her tacks 174 to 447 s.

### 12.6 For the lead

The measure is in. I have not tuned her helm round it, and nothing is filed. What I'd put before
the lead:
1. **Her displacement**, re-ruled at her comparators' ratio, about 590 to 610 t, floating her about
   half a metre below her plan's line. It gives her tacks in 8 to 15 kn from every heading, and
   truth D in its first band. Or kept at 470 t, as her plan's line measures.
2. **The rest, in 20 and 25 kn:** her rig against her inertia. Three options:
   - Steel's spars for Luce's chain, which is a ruling on her rig;
   - truth E restated across the winds as she measures, under plain sail in working winds and
     topgallants in by 20 kn;
   - both.
3. **The engine's one inertia for every ship** (a radius of gyration of a quarter of her length,
   half again for the water) is read and not changed, as the ruling says. If a light, fine ship
   swings quicker than that rule gives her, the rule is the engine's, for the lead.

Her tiers wait for the lead's ruling here, and for the engine's one A4 commit.

## 13. Hers, or every square-rigger's? The count, the haul, her rudder (2026-11-23)

The lead's nudge 66 (the trunk at 531f8896):
- her displacement is not re-ruled and stays as filed;
- Steel's spars are not taken;
- one table more, by probes only, and nothing tuned toward any outcome.

**Nothing is filed.** Her file is as at 8ce21bd, and her tiers wait. Every figure here comes from a
probe through the engine as it stands, at seed 7 (the seeds agree to the tick, §11.3), her tacks
from 290, 292.5 and 295 deg as the truths' helpers settle her. Where the probe calls "mainsail
haul" at another moment, it rewrites that one condition of the tack script in its own process (§13.2).
No file is changed.

### 13.1 Every committed square-rigged ship: the count that stays

**Under plain sail** (the game's own "set plain sail"), in 8, 12, 15, 20 and 25 kn. **S** is
stayed, with its seconds; **m** is missed stays; **·** is no end in 900 s.

| Ship | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed, of 15 |
|---|---|---|---|---|---|---|
| **the Diana** | S m m | S S S | S S S | **m m m** | **m m m** | **7** |
| the frigate-36 | S S S | S S S | S S S | S S S | S S S | 15 |
| the razee | S m m | S S S | S S S | S S S | S S S | 13 |
| the 74 | m m m | S S S | S S S | S S S | S S S | 12 |
| the 64 | S m m | S S S | S S S | S S S | S S S | 13 |
| the brig | S S S | S S S | S S S | S S S | S S S | 15 |
| the hermaphrodite brig | S S S | S S S | S S S | S S S | S S S | 15 |
| the merchant brig | · · · | · · · | · · · | · · · | · · · | 0 |
| the bilander | · · · | · · · | · · · | · · · | · · · | 0 |

**Under the sail the game's own shortening leaves each, in 20 and 25 kn.** The order given was
**"shorten sail"**, after plain sail was set and braced up, with 600 s more, trimmed every 120 s,
before "tack ship". By the vocabulary's list it takes in the studding sails, the square sail, the
royals, the flying jib and the topgallants, and any head sail loaded to its rating.

| Ship | Left set | 20 kn | 25 kn | Stayed, of 6 |
|---|---|---|---|---|
| **the Diana** | 901 m2: the courses, the three topsails, the fore topmast staysail, the jib and the spanker | S235 S234 S235 | S275 **m** S260 | **5** |
| the frigate-36 | 1,291 to 1,375 m2, the same sails | S268 S260 S259 | S475 S223 S241 | 6 |
| the razee | 1,521 to 1,665 m2 | S395 S376 S368 | S483 S485 S486 | 6 |
| the 74 | 1,771 to 1,941 m2 | S229 S186 S255 | S254 S285 S202 | 6 |
| the 64 | 1,425 to 1,569 m2 | S225 S244 S254 | S246 S278 S207 | 6 |
| the brig | 675 m2 | · S456 S203 | S477 S519 S441 | 5 |
| the hermaphrodite brig | 901 m2 | S145 S150 S149 | S162 S160 S159 | 6 |
| the merchant brig | 188 m2: her two courses | · · · | · · · | 0 |
| the bilander | 196 m2: her fore course, fore topsail and main settee | · · · | · · · | 0 |

- **In a breeze under plain sail, the misses are hers alone** among the ships that tack at all.
  Every ship of war but she stays in 20 and 25 kn.
- **In 8 kn they are not hers alone.** The 74 misses from all three headings, and the razee and the
  64 from 292.5 and 295, as she does.
- **Under the sail the game's shortening leaves, she stays in 20 kn from all three headings, and in
  25 from two.** Her one miss, from 292.5 in 25 kn, came with the shortening not finished: her
  mizzen topgallant still set, 931 m2 against the 901 of her other five.
- **For the lead, not mine:** the merchant brig and the bilander never tack within 900 s, under
  plain sail or shortened, with the little their books set (188 and 196 m2). The brig's 20-kn tack
  from 292.5 came through and swung back to her old tack, and was still called tacked (§12.2).

### 13.2 Where "mainsail haul" is called, and what a later haul does

**The rule, for every ship** (`TackScript.tick`): "mainsail haul" is called when `abs(rel) <=
POINT or self.through`. That is her head within a point (11.25 deg) of the wind, or through it.
The after yards are then swung over `brace_s` (`_after_swing_s`). The script's own note cites Luce
1884 p. 417 for the after yards hauled "with the wind ahead or a point on the bow", and the script
takes the point on the bow.

**At what angle and swing it is called**, in the ticks of §12.2 and here:

| | Wind | Called at | Off the wind | Way | Swing |
|---|---|---|---|---|---|
| **the Diana** | 20 kn | 48 s | 9.9 deg | 1.86 kn | **0.72 deg/s** |
| the Diana | 15 kn | 60 s | 10.4 deg | 1.57 kn | 0.58 deg/s |
| the frigate-36 | 20 kn | 42 s | 9.9 deg | 3.30 kn | **1.18 deg/s** |
| the brig | 20 kn | 30 s | 8.5 deg | 3.14 kn | 1.83 deg/s |

**What a later haul does**, probes only. The one condition is rewritten in the probe's process:
- "ahead": within half a degree of the wind, or through it, Luce's other reading;
- "past": a point through the wind.

| | Haul | 8 kn | 12 kn | 15 kn | 20 kn | 25 kn | Stayed, of 15 |
|---|---|---|---|---|---|---|---|
| **the Diana** | as the script has it | S m m | S S S | S S S | m m m | m m m | **7** |
| **the Diana** | with the wind ahead | S m m | S S S | S S S | **S S S** | **S S S** | **13** |
| **the Diana** | a point past | S m m | S S S | S S S | **S S S** | **S S S** | **13** |
| the frigate-36 | as the script has it | S S S | S S S | S S S | S S S | S S S | 15 |
| the frigate-36 | with the wind ahead | S S S | S S S | S S S | S S S | S S S | 15 |
| the frigate-36 | a point past | S S S | S S S | S S S | S S S | S S S | 15 |

Her times with the later haul:

| Haul | 15 kn | 20 kn | 25 kn |
|---|---|---|---|
| with the wind ahead | 208, 313, 341 s | 228 to 232 s | 220 to 273 s |
| a point past | 292 to 303 s | 219, 220, 220 s | 226 to 275 s |

With the wind ahead, one 15 kn tack of 341 s is over truth E's 330 ceiling. The frigate's tacks
slow with the later haul (25 kn: 244 to 485 s with the wind ahead, 496 to 502 a point past), and
every one is made.

**What her after yards do, hauled later** (20 kn from 292.5):
- **As called** (§12.2): at 9.9 deg off the hauled after yards, then the square sails aback, give
  -197 to -272 kN m. Her swing stops in 4 s, and she falls back and misses.
- **With the wind ahead:** she hangs at 57 s, way gone, but her after yards are still unhauled.
  Her square sails aback before the wind help her round (+33 kN m at 56 s), and nothing of the size
  the hauled yards gave opposes her (the sails' total then -5 kN m). Her swing carries her to the
  wind, and she crosses at about 62 s with 0.6 kn. The haul is called at 63 s, her head at the wind;
  she is through at 64 s, and the head yards aback box her off. Tacked in 229 s.
- **A point past:** the same, the haul called at 76 s, 13 deg through. Tacked in 219 s.

**So in a breeze it is the script's one moment that turns her back.** Hauled at a point on the bow,
the swung after yards take what swing a light, fine ship has left. Hauled with the wind ahead, as
Luce allows, she stays in 20 and 25 kn from every heading. The frigate-36 stays either way. By the
lead's words, that is the engine's and every ship's, and a package for the owner and a gate of
today's ships, not a thing to be tuned into her file. Her 8-kn misses are another thing, shared
with the 64, the 74 and the razee, and the later haul does not touch them.

### 13.3 Her rudder

- **Its ground: traced from her plan.** The blade under the line is 3.0 m2 (measured, Pages §5.5:
  its after edge at the line at (-17.88, 0.01), its heel at (-17.47, -3.90)). Its stop and rate are
  the frigate-36's.
- **What the lateral plane's re-measure did to the ratio:**
  - 104.4 m2 by the generator's rule, length times draught times 0.85, on her first particulars:
    3.0 / 104.4 = **0.0287**;
  - re-measured off her plan by the lead's ruling 4, to the false keel and the gripe, the rudder
    left out as for the 64, the razee and the 74: 3.0 / 122.2 = **0.0245**;
  - with the rudder in, 125.2 m2: 0.0240.

  The measured ships of the line carry 0.029 to 0.030; the frigate-36 and the brig 0.0375.
- Her rudder is not what turns her back. In the luff it is hard over, 35 deg, and its moment goes
  with the square of her way (§12.2). The later haul alone gives her the breeze, on the same rudder.

### 13.4 The engine's one inertia

Read, not changed: every ship's yaw inertia is her mass times the square of a quarter of her length,
and half as much again for the water swung with her (`hull.yaw_inertia`). Noted for the lead, as in
§12.6.

### 13.5 Now

Nothing filed. For the lead's ruling: she joins as her plan makes her and as the engine sails her,
slack in stays in a breeze and said so in her truths, with the haul's one moment booked as the
engine's package; or she waits for that package. Her tiers wait for the ruling, and for the
engine's one A4 commit.
