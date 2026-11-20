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
| Length on the line | 34.47 m | the post's after face to the stem's fore face on the line, 124 pies x 0.99; the table's 124 pies is 34.55 m (her module's check) | the plan, measured (Pages §4.1); Winfield et al. 2023, p. 930 |
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
