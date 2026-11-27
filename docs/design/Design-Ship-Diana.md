# Design: the corvette *Diana*, a Danish light frigate of 1804 in the Spanish navy (package 90, second draft)

**Revised 2026-11-20 on her measuring and the lead's rulings of that day (nudge 24).** Her step 1
measured her plan again, on the Biblioteca Virtual de Defensa's larger image (16,868 × 5,949 px,
96.1 px a pie). The measuring is set down in `docs/design/ships-design/pages-diana.md` (**Pages**),
and the lead ruled on it the same day. Old beside new, each where it falls:
- **the frame's datum**, one cause mended at the cause: the level line at the small image's y 311
  becomes the arrowed line itself, inclined to the keel by 0.46°, with z square to it. Every z moves:
  −0.26 m at the taffrail, −0.06 m at midships, +0.05 m at the stem (Pages §4.1, §8; here §1.3,
  §3.2, §4.1).
- **the load line** (ruling 1): the arrowed line as drawn, with its 0.27 m of drag. The draught was
  3.57 m on an even keel; it is now **3.78 m** mean to the false keel's lower edge (3.91 at the
  post, 3.65 at the stem), with 3.63 m (3.76, 3.49) to the keel's lower edge beside it. The two
  other readings are recorded and not taken (§2).
- **the drawn displacement** (rulings 2 and 3): about **466 to 474 t** outside a plank of 3 to 4
  pulgadas, with the keel and its timbers (no source for the plank found: JUDGEMENT), against the
  table's 498.0 t. The table was most likely reckoned on a level line at the after draught. The miss
  stands, recorded and explained. `displacement_kg` stays 498,000, and the file floats her at that
  mass to the drawn line (§2).
- **the lateral area** (ruling 4): 104.4 m² by the generator's 0.85 rule becomes **122.2 m²**,
  measured, by the method of the hulls drawn from their draughts: D29 (b), to the false keel, the
  knee counted, the rudder left out (§2).
- **the deck at side** (ruling 5): the upper red line, JUDGEMENT; 1.40 becomes **1.33 m** at
  midships, for the datum alone (§2, §3.2).
- **accepted** (ruling 6): the lee port at **21.1°** (was 21.8°; §10, §14), and the head ending in a
  **scroll** (`form.head: scroll`, was `knee`; §3).
- **measured** (Pages):
  - her waterline 34.40 becomes 34.47 m;
  - the ports 0.87 becomes 0.83 m wide, with their sills and half-breadths;
  - every line of her profile traced, the stem, the head, the stern and the wales among them;
  - Steel 1794's 20-gun column read (§4.1);
  - the hourglass fitting found to be a ship's bell (§3.6).
- **for the lead** (§17.2 items 7 to 9): the draught's datum, where the ruling's figures and its
  words differ; the length by D29 (b); and a finding on the 0.85 rule (§18 item 5).

**Revised 2026-11-19 on Winfield's passages sent by the owner, and the owner's answers of that
day.** The owner sent her whole entry (Winfield et al. 2023, p. 930; "this is the entirety of it",
their words), the units (pp. 41-46), the corvettes' chapter (pp. 904-906) and the complements of 1788
(p. 1446 and following), set down in `VesselReferences-2026-11-Spanish.md` §7, §14, §15 and §17.
**Her entry holds only what VR-Sp §5 already had**: no service line, no source for "as captured",
no rule for her 335 t, nothing of her rig; her fits, her 167 and her figures stand. What the other
passages settle here, old beside new:
- **her 335 t is toneladas de arqueo**, a capacity of about 476 m³ (computed), not a weight (§2's
  tons);
- **the libra is 0.4608 kg** by the book, where §1.3 took 0.4601 from memory: her displacement from
  her plan's table moves from 497,200 to **498,000 kg** (computed, 0.16 per cent; §1.3, §2, decision
  3);
- **her soldiers by the 1788 regulation** for a corvette of 18 to 22 guns, **50** (40 infantry and 10
  infantry-artillery) where §6.1 had 25 by the frigate's share, JUDGEMENT; her other stations scaled
  to the rest (§6.1, §6.2, §6.4); her commander a teniente de navío, as the regulation and her plan
  both have it;
- what still waits (§0, §17): the source of "as captured", her rig's rule, Steel's 20-gun column, the
  Danish draught: other research or judgement, by the owner's word.

**Second draft (2026-11-18).** The design for the fourth hull of package 90 (the lead's order: the
tartane, the polacre, the xebec, the *Diana*, the *Purísima Concepción* class). By
`Plan-ShipsWorkflow.md`'s method it answers the critic's reading of the first draft ("How this
draft answers the critic", below the decisions) and takes the settlements of package 90's plan
(`docs/design/Plan-Package90.md` §4, its step names in §6); nothing here is built, and no build
begins before a scope card agreed with the owner (`docs/dev/ScopeCards-BeforeTheGate.md`, "How a
package runs, as amended by the owner on 2026-11-16"). Its form is the bilander's and the
*Bellerophon*'s designs'. It works from her research note, `docs/design/Research-Diana-2026-11.md`
(**Dia**), and names what her builder would build, from what, and what is the owner's.

**What binds, in order:**
1. The lead's note of 2026-11-18 (nudge 15, `docs/dev/M7-WorkPackages.md`): package 90's
   preliminaries only; nothing that the suite reads is changed.
2. The owner's settling of 2026-11-06 (the lead's note of that day): the Danish frigate *Diana* of
   1804, taken at Cartagena and kept by Spain to 1832; Winfield p. 930's row; **her three fits,
   dated**; her plan the Spanish navy's of 1809-1810, held in the tree, read in its own units and
   never as English feet.
3. `docs/design/Build-Ships.md`: §5.0 (the aim, the principles, the ladder), §5.1-§5.3 (the
   profile and its shape keys), §5.8 (pictures for the eye), §6's postscript (**package 81's
   checklist** for her guns to be drawn), §7 (the lee ports), §8 (fits and roles), §9.
4. Package 75's rulings as merged: ruling 11 (a merchantman's working officers; §6 says why it
   does not reach her), the made-out rule (the lead's ruling 17 of 2026-11-12: what the tops make
   out at the rig's distance, then the glass), B3.4's schooner's-mast rule and its classing limits
   (`Design-ShipsEngineExtensions.md`).
5. Package 116 (the wheel shot away, `rig the relieving tackles`, `repair the wheel`; the cruiser's
   doctrine read from `thresholds:`) and package 96 (the harbour's shelves,
   `client/harbour-shelves.yaml`, a sentence each).
6. The owner's books: Winfield's facts only, cited by page as `VesselReferences-2026-11-Spanish.md`
   sets them down; further passages asked for by title (Dia §11).

**Where.** The worktree `D:/Projects/FreeSail/FreeSail-pkg-90` on the package's branch at 68e769ef.
Every `file:line` is at that head; a builder re-checks a line before using it. **2026-11-20:** the
lines cited for the rulings (§2, §18) are at 780a7c06.

**Marks.** *read*, *read (OCR)*, *measured* (off the held plan at 11.40 px a pie, ±2 px, about
±5 cm, where a line is clear; **2026-11-20:** off the library's larger image at 96.1 px a pie, ±2 px
(±0.6 cm) on a clear line found by a script, ±5 px (±1.5 cm) by eye, the held file being the same
sheet at 1/8.43: Pages §1.1, §3), *computed* (arithmetic on measured or read figures), *observed*
(printed by a scratch probe on the engine run from the
worktree with `py`, the tree first on `sys.path`; the scripts are in the session's scratch,
`scratchpad/p90/diana/probe/`, not filed; no tracked file changed, Python's git-ignored bytecode
caches aside), *judgement*, marked
**JUDGEMENT** where it is a figure a file would carry. Rungs are the brief's: **A** her own plans,
**B** a historian's particular, **C** judgement or a named rule on her particulars; in a file's
`marks` they are §5.0's words, `sourced` (A), `rule` and `judged` (C).

**One sentence.** One module writes one file: the Spanish navy's own plan of her at its own scale
(34.55 by 9.06 m, 497 t, 498 t at the book's libra since 2026-11-19, drawing 3.57 m; 3.78 m at the middle of her waterline to the false keel, trimmed by the stern as drawn, since 2026-11-20), a flush-decked light frigate of eleven ports a side with
her masts where the plan steps them, ship-rigged by the generator's frigate chain on her own
particulars, carrying twenty carronades of 30 by default and her other fits by date, her company
of 167, made out "a ship" by the tops and "a corvette" by the glass; the engine sails her today
with nothing new but her rows, once her stiffness is given her.

---

## Decisions proposed

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/diana.py`, `build(out_dir)` writing **`data/ships/corvette-20.yaml`**, `ship.name` *Diana*; added to `SHIP_MODULES` (`tools/gen_ships.py:10399`) | The package 75 pattern (one module a ship); the file named by type and guns as `frigate-36` and `razee-44` are |
| 2 | Her particulars as data in the plan's own units (pies, pulgadas, toneladas and libras, and the plan's pixels at 11.40 a pie), converted once in a frozen `Particulars`. **2026-11-20:** the plan's figures are Pages §6.2's metres in the corrected frame (the larger image at 96.1 a pie), the table's in its own units as before | Every figure reads as its source gives it (the *Bellerophon*'s §1.4) |
| 3 | **Her hull is the plan's, rung A, `sourced`**: LWL 34.40 m, beam 9.06 m (Winfield), draught **3.57 m** to the keel's lower edge at the plan's arrowed line, displacement **497,200 kg** (the table's 540 t 691 lb), deck 1.40 m. **2026-11-19:** displacement **498,000 kg**, the table's libras at the book's libra of 0.4608 kg (Winfield et al. 2023, pp. 41-46) in place of memory's 0.4601. **2026-11-20:** LWL **34.47 m** (measured); draught **3.78 m**, the mean to the false keel's lower edge at the arrowed line as drawn, drag 0.27 m (the lead's ruling 1); displacement **498,000 kg** stands, the drawn 466-474 t beside it (rulings 2, 3); lateral area **122.2 m²** (ruling 4); deck **1.33 m** (ruling 5) | Dia §2.3-§2.5; VR-Sp §7; Pages §4-§5 |
| 4 | **GM 1.5 m, JUDGEMENT**, tuned to her captain's "stiff" (Dia §6) | The frigate's ratio (1.0 m) heels her 1.7 times the frigate (observed, §9); 1.5 brings her within 15% of it |
| 5 | Her profile wholly from the plan: rail, half-breadths by station, keel, stem, stern, wales, section, the gun deck and its eleven port triples, the port size [0.87, 0.66]; `form.stern: square`, `form.head: knee`. **2026-11-20:** every line from Pages §6.2 in the corrected frame; the port size **[0.83, 0.66]** (measured); `form.head: scroll` (read; the lead's ruling 6) | Dia §2.5-§2.7; Build §5.1; package 81's checklist; Pages §5, §6 |
| 6 | Masts at the plan's places and rakes (A); **every spar by Luce's chain on her particulars** (the generator's frigate rule), Falconer's yard rule and Chapman's the checks, Steel's 20-gun column read at step 1 as the third (C). **2026-11-20:** Steel's column read (Pages §7): the masts within 1% of Luce's chain, the main yard 63 ft 0 in (19.20 m) 2.8% under it; the pick stands | No spar of hers survives; the rule the game already uses for its frigate (Dia §3.2) |
| 7 | Her sails the frigate's set by the same chain: courses, topsails, topgallants and royals on fore and main, topsail, topgallant and royal on the mizen over a dry crossjack, the driver, three headsails, the staysails between the masts, studding sails | The 1809 drawing (eye, Dia §3.1); the frigate's file the pattern |
| 8 | **Four fits proposed**, three of them the owner's: `danish 1807` (16 × 30-pdr carronades, 4 × 8-pdr long guns; **the owner's to accept**), `as captured 1809` (20 × 24-pdr carronades), **`carronadas de a 30 1810`** (20 × 30-pdr carronades, **the default**, the plan's own), `1817` (12 × 12-pdr, 8 × 30-pdr carronades, 4 × 3-pdr obuses) | Winfield p. 930; Roos pp. 94, 101; owner's question 1 |
| 9 | Company **167** (Winfield), on the frigate's shares of stations scaled, 10 posts; two watches; **ruling 11 does not reach her**. **2026-11-19:** her soldiers **50** (was 25), by the 1788 regulation for a corvette of 18 to 22 guns, the rest on the frigate's shares | Dia §5; she is a man-of-war in every fit; Winfield et al. 2023, p. 1446 and following (VR-Sp §15) |
| 10 | Description key **`corvette`**: the tops make out **"a ship"**, the glass **"a corvette, flush-decked, eleven ports a side"**; `SIZE_RANK` 2; roles `kings-ship`, `cruiser` | The made-out rule (§8) |
| 11 | People file `data/people/corvette-20.yaml`, her people's names Spanish (**the owner's**: Spain's `names` is `english` today) | §6.3 |
| 12 | No engine change for her rig; her stage 0 the rows a new man-of-war's description needs (§12) | Observed: she sails, tacks, wears and heaves to as the frigate does (§9) |
| 13 | Six truths proposed (§14) | Her sources' particulars, Meyer's speed, her stiffness, her helm, her going about, her lee port |

---

## How this draft answers the critic

The critic's findings that touch her, and the plan's settlements:

| Finding | What the first draft said | This draft |
|---|---|---|
| F14: the 1809 drawing | "a drawing made aboard in 1809"; the reproduction "on the owner's word" | **Held.** The drawing is signed "Thomsen pinx 1809" (perhaps her officer of that name, Roos): its making aboard is not known. Roos's 1957 reproduction is not offered for the tree until its status and the artist are vetted (artist, date, licence, namesake, as the README's rows are); the museum's own image with its terms is the road (§17.1 question 1, §17.2 item 5) |
| F17 (from the three-decker's): Winfield's length | her plan's 124 pies measured as the gun deck from post to stem (Dia §2.2-§2.3) | kept; the three-decker's design now cites her case as its reason for reading Winfield's "length" so (Con-D §2) |
| F19: a unit | Babron's main "25 mm in 325" | **Held.** 25 in 325 (Dia §3.2) |
| The plan's settlements | her `DESCRIPTIONS` row among her stage-0 rows; two scenarios proposed; her place in the order "offered for the plan" | her row lands with her file, from her builder (Plan §5.1 item 8); no scenario in the card (Plan §4 row 15); the plan takes her first on the ship-rigged road, her builder laying the shared data N1 to N3 first, each merged alone (Plan §7.1, §9.1) |

---

## 0. The gate: what waits, and on whom

- **Nothing is built from this draft.** The critic reads it; the second draft answers; the lead
  gates the design; the owner agrees a scope card for the package's build (one building package at
  a time); then her builder works from the second draft.
- **What waits on the owner** (§17.1): her first fit (the Danish papers against Winfield), the rule
  for a foreign pounder, her stiffness, her spars' rule, a Danish fit and colours, her people's
  names.
- **What waits on the lead** (§17.2): the made-out rank at the rig's distance, her file's name,
  the stage-0 rows, item 37 (the generator's studding law) settled before her file is generated.
  **2026-11-20:** the load line is ruled (nudge 24); three points of the rulings' application wait
  on the lead's word (§17.2 items 7 to 9).
- **What waits on sources**: Winfield's passages (Dia §11); Steel's 20-gun column on the page image;
  the Danish draught, if the owner wants it sought. **2026-11-19:** Winfield's passages came; her
  entry holds nothing new, and nothing of her waits on the book now. What it does not give (the
  source of "as captured", her rig) stays as designed, by the owner's word: other research or
  judgement. **2026-11-20:** Steel's column is read (Pages §7). Her plank's thickness was sought in
  her class's timber regulations and not found, so it stands as a range, JUDGEMENT (§2). The Danish
  draught still waits.
- **Her place in the package's build.** She asks nothing new of the engine (§9), so her build is the
  smallest of the five and the natural one on which to settle the package's shared rules first: the
  foreign pounder, the Spanish names, the nations' dated wars (§11), each of which the xebec and the
  three-decker need too. **The plan takes it** (Plan §9.1): she is first on the ship-rigged road,
  and her builder lays the shared data N1 to N3 (the Spanish names, the corsair's role, a Spanish
  marines kit), each merged alone before her file. The lead's order stands for the lateen road.

---

## 1. The module and the generator

### 1.1 Files

| Path | What | Owner |
|---|---|---|
| `tools/ships/diana.py` | the data at the head; `particulars()`; `write(out_dir, p)` and its section functions; `build(out_dir)` | her builder |
| `data/ships/corvette-20.yaml` | generated only | her builder, through the generator |
| `data/people/corvette-20.yaml` | her posts' people and names | her builder, hand-written data |
| `tests/test_diana.py` | her tests and her truths' drafts | her builder |
| `freesail/world/ships.py`, `world/captains.py`, `world/brains.py`, `world/regimes.py`, `world/squadrons.py`, `orders/signals.py` | her rows (§12), in her stage 0 | stage 0 |
| `tools/gen_ships.py` | `SHIP_MODULES` gains `diana`, nothing else | stage 0 |

### 1.2 What she reuses, read only, and what is new

**Reused** (`tools/gen_ships.py` at 68e769ef): `Builder` and its `descriptions` (:1525);
`hull_profile` (:587), `hull_form` (:691), `midship_section` (:869) only where §3 has no traced
section; `raked_x` (:3202), with `deck_m=` her own 1.40 (**1.33** since 2026-11-20, §2); `broadside_pair` (:4519, `deck="upper"`),
`gun_crew` (:4309), `fit_magazine` (:4337); `hold_for` (:4082), `boat_entries` (:4093),
`pump_entries` (:4155), `ground_tackle_for` (:499), `wardroom` (:4225); the frigate's rope and cloth
helpers and notes. From `tools/ships/period.py`: `ADYE_CARRONADE_CWT` and
`DOUGLAS_CARRONADE_CREW`.

**Written anew in the module, on the frigate's lines** (`frigate()`, :2169, builds itself and takes
no particulars, so it is not touched): Luce's chain with her own `main_len` and her own mast heels
(§4.1); the three masts' loop, the yards, the square sails' cut, the head, the staysails, the
driver, the studding sails, the storm canvas, groups and aliases, copied from the frigate's
function with her figures in place of its constants. As the *Bellerophon*'s module did, nothing is
imported from another ship's module; the duplication is reported.

### 1.3 The data, the frame, the checks

- **Data at the head**, each with its source in a comment, in its own units: `PLAN` (the plan's
  pixel figures of Dia §2, with `PX_PER_PIE = 11.40` and the origin x 826.5, y 311); `TABLE` (the
  table: 124 pies, 32 pies 6 pulgadas, 16 pies; 540 t 691 lb and its two bodies); `WINFIELD` (the
  book's metres, men and fits); `ROOS` (the Danish guns, men and Meyer's speed); `PIE_M = 0.278635`,
  `LIBRA_KG = 0.4601`, `TONELADA_LIBRAS = 2000`. **2026-11-19:** `PIE_M` is the book's own pie
  (278.635 mm, Winfield et al. 2023, pp. 41-46), and **`LIBRA_KG = 0.4608`**, the book's libra (was
  0.4601, memory); `TONELADA_LIBRAS = 2000` stands, proved by the table's carry (Dia §2.3), where
  the book's "about 1,150 kg" ton of weight does not equal its own 2,000 libras (921.6 kg, computed:
  VR-Sp §7). **2026-11-20:** `PLAN` is no longer pixels from a level y. It holds Pages §6.2's metres
  in the corrected frame, or the larger image's pixels at 96.1 a pie with Pages' transform: the
  sheet's bow taken out, the line straight, z square to it, the origin at its middle, x 6,958.0 on
  the larger image (Pages §3.3, §4.1). The level datum of y 311 was the cause of every z's error,
  and it is mended there.
- **The frame.** x in metres forward of the middle of her load waterline (image x 826.5: the
  post's after face at x 123 and the stem's fore face at x 1530 on the line); z above the line
  (image y 311). A spar's `height_m` and a sail's `corners_m` above her datum, the gun deck at
  midships, 1.40 m (D18 (a): her uppermost continuous deck, flush from end to end; no rival); a
  sail's centre above the water. **2026-11-20:** the same words on the line as drawn.
  - The post's after face and the stem's fore face meet the line at larger-image x 1,014.6 and
    12,901.4 (small 120.3 and 1,529.7), 34.47 m apart; the middle lies 3.7 cm aft of the old origin.
  - **z is square to the arrowed line**, which is inclined to the keel by 0.46°, so she is drawn
    trimmed by the stern (Pages §4.1).
  - The datum deck is 1.33 m at midships (§2).
- **Checks before the file is written**, each `raise ValueError` with a sentence: the table's
  arithmetic (the two bodies sum to the total, the difference holds); Winfield's metres within
  0.01 m of the table's pies at 0.278635; every port gun on its triple to the centimetre; the drawn
  displacement against the table's (recorded beside it, never in its place: §5.0 principle 8);
  every mast's heel below the deck and above the keel. **2026-11-20:** the drawn displacement is
  recorded, not raised on.
  - The generator's form check notes its own drawn figure beside the filed one
    (`freesail/ship/form.py`:241).
  - Her note carries the measured 466-474 t beside it, with the miss and its reason (§2: −6.5% to
    −4.9%; the table reckoned on a level line at the after draught).
  - The lead ruled the miss recorded and not closed.

---

## 2. The hull blocks

| Field | Figure | Source and rung |
|---|---|---|
| `length_waterline_m` | **34.40** → **34.47** (2026-11-20) | The plan, the post's after face to the stem's fore face at the arrowed line, 1,407 px (Dia §2.4, measured). A. The rabbets 33.56 m in the note. **Revised:** 11,886.8 px at 96.1 a pie on the larger image, the same two faces on the line (Pages §4.1, measured, +0.2%); 34.83 m to the knee's fore edge (computed); between the rabbets about 33.6 m, not re-measured. By D29 (b) the drawn hulls file the length rabbet to rabbet: for the lead (§17.2 item 8) |
| `beam_m` | **9.06** | Winfield's metres for the table's 32 pies 6 pulgadas, extreme (the body plan's frame, measured 32½ pies). A and B. **2026-11-20:** the frame 32.47 pies on the larger image (measured, −0.1%); the drawn sections 4.53 m a side at the line amidships (Pages §3.1, §5.1) |
| `draught_m` | **3.57** → **3.78** (2026-11-20) | The arrowed line 11.45 pies above the rabbet, the keel 1.36 pies under it: 12.8 pies to the keel's lower edge, even keel (Dia §2.4). A for the drawing, **JUDGEMENT** on the arrow's meaning, checked by the table's displacement (Cb 0.48, Cp 0.72). **Revised, the lead's ruling 1: her load line is the arrowed line as drawn**, inclined to the keel by 0.46°, a drag of 0.27 m (measured, Pages §4.1-§4.2). The draught is the mean to the false keel's lower edge, K: 3.91 m at the post's after face and 3.65 m at the stem's fore face. To the keel's lower edge it is 3.63 m (3.76, 3.49). The line stands 11.71 pies (3.26 m) above the rabbet at the midship station; the keel's lower edge lies 1.28 pies (0.36 m) under the rabbet, K 1.82 pies (0.51 m). K is taken by the ruling's words and by D29 (b), as the drawn hulls file theirs; the ruling's figures, 3.76 and 3.49, are the keel's (§17.2 item 7). The two other readings are recorded, not taken (below). A; K a false keel by **JUDGEMENT** (Pages §4.1). The drawn body: Cb 0.43 (moulded, between the rabbets, to the rabbet), Cm 0.68, Cp 0.63 (computed, Pages §4.3) |
| `displacement_kg` | **497,200** → **498,000** (2026-11-19) | The table's 540 t 691 lb at 2,000 libras of 0.4601 kg (Dia §2.3). A. The frigate's rule (Cb 0.55) would make her 627 t, 26% more: not taken. **Revised:** at the book's libra of 0.4608 kg (Winfield et al. 2023, pp. 41-46), 1,080,691 libras are 497,980 kg (computed), 0.16 per cent more; the drawn displacement is set against it as before. **2026-11-20, the lead's rulings 2 and 3: 498,000 stands, the table's.** The file floats her at that mass to the drawn line. Beside it, drawn to the arrowed line (measured, computed, Pages §4.3): 435,600 kg moulded; 441,700 with the keel, post, stem and gripe (−11.3%); **465,600 to 473,600 with 3 to 4 pulgadas of plank** (−6.5% to −4.9%). The plank is **JUDGEMENT**: no source found (Pages §4.5). The miss is explained, not closed (below) |
| `gm_m` | **1.5** | **JUDGEMENT**: Meyer's "stiff" (Roos p. 94) against the frigate's heel in the same wind (§9). The frigate's 1.3 m scaled by the breadth gives 1.0, which heels her 19° abeam in 22 knots under plain sail |
| `clr_x_m` | **2.5** to start | The frigate's lead (3.0 m on 41.8) scaled by the length; tuned for Meyer's "steers splendidly" (truth D, §14) |
| `lateral_area_m2` | 104.4 → **122.2** (2026-11-20) | LWL × draught × 0.85, the generator's rule; the plan's profile under the line measured beside it (§3.6 task 2). **Revised, the lead's ruling 4: by the method of the hulls drawn from their draughts.** That method is measured, to the false keel's lower edge with the stem, gripe and knee, the rudder left out (D29 (b)). The 64's and razee's files hold `"lateral_area_m2": 305.5,` and `283.4,` (`tools/ships/indefatigable.py`:891, :1640), "with the band, the rudder left out" (:915, :1667). The 74's holds `330.0,` (`tools/ships/bellerophon.py`:737), "below WL1 to K ... the rudder left out" (:768). The *Neufchatel*'s holds `102.0,` (`tools/ships/neufchatel.py`:725), "to the false keel's bottom, keel, gripe and post counted and the rudder not" (:759-760). Hers is the post's after face, K and the knee's fore edge: **122.2 m²** (measured, Pages §5.6). Beside it: 120.0 to the keel's lower edge and the stem's fore face (the figure the ruling named; §17.2 item 7); 125.2 with the rudder; 104.4 by the rule as first written. A |
| `hull_speed_kn` | **11.8** | The frigate's 13.0 by √(34.40 / 41.8); holds Meyer's 10-11 knots (observed, §9). Tuned within 11.0-12.5 by truth B. **2026-11-20:** √(34.47 / 41.8) gives the same 11.8 (computed) |
| `deck_height_m` | **1.40** → **1.33** (2026-11-20) | The gun deck at side at midships above the line (Dia §2.5, measured). **Revised:** the same upper red line, re-referenced to the line as drawn and traced along its length (Pages §5.2, measured). **The lead's ruling 5: which red line is her deck at side is this design's.** The upper one is taken (**JUDGEMENT**): it puts her sills 0.38 to 0.50 m above the deck at ports 1 to 10, the nearest of the three readings to a carronade's port. Steel's 36 has carronade ports 11 in above the plank and long guns' 1 ft 7 in (Steel 1805, Folios XLII and XLVI; `pages-steel-1805-bodies.md` §4); the third line with the plank (1.18 m) would put them 0.53 to 0.65 m above it, a long gun's height (Pages §5.2) |
| `rudder` | area **3.0 m²**, span 3.57 → **3.90** (2026-11-20), 35°, 3.0°/s | The plan's blade under the line (Dia §2.5, measured ±0.3 m²); the frigate's stop and rate. **Revised:** 3.0 m² on the larger image (measured, unchanged); its span from the line to its heel on K, (−17.47, −3.90) (Pages §5.5, measured) |
| `profile` | §3 | Build §5.1 |

**Her load line and her table (the lead's rulings of 2026-11-20).** The drawn displacement to the
arrowed line missed the table's by more than 5%, so by `Plan-Package90.md` §8.4 it went to the lead
before anything else was filed. The three readings of her sources (computed, Pages §4.4):

| Reading | Tonnes (the keel and its timbers, 3 pulgadas of plank) | Against the table's 498.0 t | Bodies, fore to aft (the table's 281 t to 258 t, 1.089) | Standing |
|---|---|---|---|---|
| The arrowed line as drawn, drag 0.27 m | 465.6 (473.6 at 4 pulgadas; 441.7 with no plank) | −6.5% (−4.9%; −11.3%) | 1.040 | **her load line** (ruling 1) |
| The arrowed line raised half a pie (0.14 m), parallel | 499.1 | +0.2% | 1.040 | recorded, not taken |
| The after draught carried level (3.76 m to the keel's lower edge from end to end) | 498.9 | +0.2% | 1.101 | recorded, not taken |

- **What the table most likely is** (ruling 3; **JUDGEMENT**, for no word on the sheet says how the
  table was reckoned): the third reading gives 499 t against the table's 498.0, and the bodies 1.10
  against its 1.089; the drawn line gives 1.040. So the constructor's table was most likely
  reckoned on a level line at the after draught. It is not her displacement at the line she is
  drawn floating at, and §8.4's comparison is not like for like for her. That is why the 5% band is
  missed, and the miss is not closed: **−11.3% moulded with her keel; −6.5% to −4.9% outside the
  plank.** No further chase.
- **Her plank** (ruling 2) is not chosen by the 5% band. A source was sought with its page: her
  class's scantlings in the timber regulations of her day (Danish of 1804, Spanish after her taking
  in 1809) or her own sheet. Her sheet gives none, and none was found on the web (Pages §4.5). So it
  is a range, **3 to 4 pulgadas**, and her drawn displacement the range it gives, **about 466 to
  474 t** outside the plank with the keel and its timbers: **JUDGEMENT**.
- **Her file floats her at the generator's mass to the drawn line either way**: `displacement_kg`
  498,000, z = 0 on the arrowed line.

**Her tons.** Winfield's 335 t is not the displacement; the rule behind it is asked (Dia §11). Where
the generator reads tons (the anchors, the boat, the hold: `ground_tackle_for`, `hold_for`) it wants
an English burthen, its tables being English. By the builder's old measure on her gun deck (124
pies, 113.4 English ft) and breadth (29.7 ft), (113.4 − 3/5 × 29.7) × 29.7 × 14.86 / 94 = **449
tons** (arithmetic; the frigate's 933 is matched by the same rule on her own figures within 1%).
*Pick:* 449 for the helpers, Winfield's 335 beside it in her note with its rule once Winfield's
passage gives it. **2026-11-19:** the book's units say what the 335 t is, not its rule: **toneladas
de arqueo**, a measure of capacity of about 1.42 m³ each, as the English ton burthen is (Winfield et
al. 2023, pp. 41-46; VR-Sp §7), so about 476 m³ (computed). The measuring (arqueamiento) is not
given; her whole entry (p. 930) gives nothing more. The pick stands: 449 for the helpers, her 335
toneladas de arqueo in her note as such.

---

## 3. The hull profile and her shape (Build §5.0-§5.3)

### 3.1 What the sources give, by rung

| Feature | Source | Rung, mark |
|---|---|---|
| Length, breadth, depth, displacement | The plan's table, Winfield's row | A, B; `sourced` |
| The sheer, the rail, the deck, the wales, the keel, the stem, the post, the counter, the head's knee, the hawse holes, the ports | The plan's sheer (Dia §2.5, §2.7) | A; `sourced` |
| The half-breadths by station; the midship section; the after body's hollow garboards | The plan's half-breadth and body plans (Dia §2.6; the stations' half-breadths are §3.6's task; **2026-11-20:** measured, Pages §5.1, §6.2) | A; `sourced` |
| The load line | The arrowed line (Dia §2.4); **2026-11-20:** inclined to the keel, drag 0.27 m (Pages §4.1) | A drawn, its meaning JUDGEMENT; `sourced` with the note. **2026-11-20:** ruled her load line as drawn, with its drag (the lead, ruling 1) |
| The stern lights | None drawn in the profile; a frigate-built ship certainly had them | C; `judged` by Steel's sheer-draught method (§5.0 principle 9), tagged on the owner's sheets |
| The figure | None drawn | none (`head: knee`) until the Danish draught or the 1809 picture shows one. **2026-11-20:** the knee ends in a scroll, no figure (read on the larger image, Pages §5.4): **`head: scroll`** (the lead's ruling 6), A, `sourced` |
| The paint | The 1809 drawing: a light band along the ports, dark lids (eye) | words in her note only |

### 3.2 Her points (file frame, metres; Dia §2.5-§2.7, measured)

**2026-11-20:** every key below is now Pages §6.2's, measured on the larger image in the corrected
frame (z square to the line as drawn). Each key's first reading (Dia §2.5-§2.7, the small image,
z from a level y 311) is given after it as *was*. Most of each move is the datum's alone: −0.26 m at
the taffrail, −0.22 at x −15, −0.16 at −10, −0.06 at midships, +0.02 at +10, +0.05 at the stem
(computed, Pages §8). Where a move has another cause, it is named.

- **`rail_m`**: the waist rail, the bulwark's top (its upper edge). 33 points, Pages §6.2: (−18.82,
  3.52), (−18.0, 3.43), (−17.0, 3.33), (−16.0, 3.23), (−15.0, 3.13), (−14.36, 3.08) ... the station
  x's ... (−0.62, 2.62), (0.63, 2.62) ... (14.38, 3.19), (15.63, 3.34), (16.0, 3.39), (17.0, 3.54),
  (17.3, 3.59). The stem head is at **(17.30, 5.09)** and the taffrail's top at **(−18.63, 4.03)**
  (measured).
  - Forward of x +13.5 the first reading followed a head rail's band, not the bulwark rail, which
    sweeps up 0.3 to 0.4 m higher at x +16 to +17: a local cause, the crowding at the bow on the
    small image (Pages §8).
  - **JUDGEMENT**: the solid side is the rail. The hammock rail above it, 3.17 m at midships to 4.01
    at the stern and 4.10 at the bow, has no key and is in her note (§13).
  - *Was*: (−18.25, 3.52), (−16.78, 3.50), (−15.31, 3.35), (−12.87, 3.13), (−10.42, 2.96), (−7.98,
    2.84), (−5.54, 2.74), (−3.09, 2.74), (−0.65, 2.69), (1.80, 2.69), (4.24, 2.69), (6.68, 2.74),
    (9.13, 2.81), (11.57, 2.88), (13.53, 3.01), (16.46, 3.01), (17.44, 3.10); the stem head (17.33,
    4.91), the taffrail (−18.73, 4.23); the hammock rail 3.18 to 4.23 m.
- **`decks_m.upper`**: **the deck at side, the upper red line** (the lead's ruling 5: this design's
  choice, **JUDGEMENT**, §2), traced along its length (measured, Pages §5.2): (−16.78, 1.84),
  (−15.31, 1.69), (−12.87, 1.59), (−12.0, 1.53), (−10.0, 1.47), (−8.0, 1.42), (−6.0, 1.38), (−4.0,
  1.35), (−2.0, 1.33), (0.0, 1.33), (2.0, 1.35), (4.0, 1.37), (6.0, 1.41), (8.0, 1.46), (10.0, 1.52),
  (12.0, 1.60), (14.0, 1.70), (15.0, 1.76), (16.0, 1.85), (17.0, 1.93). The first three are the
  first reading's, re-referenced (computed).
  - *Was*: (−16.78, 2.08), (−15.31, 1.91), (−12.87, 1.78), (−10.42, 1.66), (−7.98, 1.54), (−5.54,
    1.49), (−3.09, 1.44), (−0.65, 1.39), (1.80, 1.39), (4.24, 1.42), (6.68, 1.44), (9.13, 1.44),
    (11.57, 1.54), (14.01, 1.59), (15.97, 1.69).
- **`ports_m.upper`**: eleven triples [x, sill, half-breadth], the sheet's own centres, the
  half-breadth at each sill read on the body plan (measured, Pages §5.7; task 1): [−13.49, 2.11,
  3.19], [−10.69, 1.93, 3.77], [−7.81, 1.82, 4.14], [−4.93, 1.75, 4.34], [−2.06, 1.72, 4.42], [0.80,
  1.72, 4.46], [3.65, 1.75, 4.42], [6.42, 1.82, 4.33], [9.37, 1.91, 4.14], [12.27, 2.06, 3.74],
  [15.96, 2.38, 2.1]. The bow port's half-breadth is **JUDGEMENT**, ±0.2 m. **`port_size_m.upper`**:
  **[0.83, 0.66]** (measured: 286.5 by 229 px). The profile is one for every fit, so all eleven
  triples are written: the default fit's guns stand on ports 1 to 10, and the 1817 fit's obuses on
  the bow ports (§5.1). The generator's check (every port gun on its triple to the centimetre, Build
  §5.3) runs for every fit; the guns' `x_m` are set on the sheet's centres (the checklist's rule).
  - *Was*: sills from Dia §2.7, (−13.46, 2.33), (−10.69, 2.11), (−7.78, 1.98), (−4.84, 1.87),
    (−2.11, 1.81), (0.76, 1.78), (3.63, 1.78), (6.53, 1.83), (9.30, 1.91), (12.25, 2.04), (16.07,
    2.33); the half-breadths to be measured (at midships 4.46); the size [0.87, 0.66]. The sills move
    by the datum, −0.22 m aft to +0.05 m forward, and by the larger image's edges.
- **`keel_m`**: the keel's lower edge from **(−16.54, −3.75) to the forefoot at (13.84, −3.51)**.
  It slopes in the frame because she trims by the stern. **K**, the false keel's lower edge, runs
  from (−16.54, −3.91) to (14.65, −3.66), and her draught is counted to it (§2). **`rabbet_m`**:
  (−16.55, −3.40) to (13.45, −3.15), then up the stem's rabbet (Pages §5.4). All measured.
  - *Was*: the lower edge level at z −3.57 from x −16.59 to about +15.2, the rabbet at z −3.19
    over the same run. The keel was read level, but it is drawn with a drag; a false keel is drawn
    under it (Pages §4.1).
- **`stem_m`**: the forefoot (13.84, −3.51), (14.80, −3.25), (15.25, −3.00), (15.56, −2.75), (15.83,
  −2.50), (16.06, −2.25), (16.26, −2.00), (16.59, −1.50), (16.86, −1.00), (17.07, −0.50), **(17.23,
  0.00)**, (17.37, 0.50), (17.47, 1.00), (17.54, 1.50), (17.60, 2.00), (17.64, 2.50), (17.67, 3.00),
  (17.69, 3.50), (17.69, 4.00), the head (17.30, 5.09). Traced (measured, Pages §5.4; task 3).
  - *Was*: (15.2, −3.57) by the forefoot's curve to (17.20, 0.0) and up to (17.33, 4.91).
- **`stern_m`**: the heel at K (−16.54, −3.91), plumb to (−16.54, −3.40); the post's after face
  **(−17.23, 0.00)** at the line, raked 10.5° to the line's square; the post's head (−17.84, 2.94);
  the tuck (−17.78, 2.65); **the knuckle (−18.57, 3.20)**, the sloping counter meeting an upright
  upper stern; that stern's top (−18.57, 3.60); the taffrail's top **(−18.63, 4.03)**. Measured;
  what each line is, **JUDGEMENT** (Pages §5.5, task 5; the stern's reading is the weakest of the
  measuring).
  - *Was*: the post from (−16.59, −3.57) to (−17.20, 0.0) and (−17.71, 3.21), raked 9.4°; the
    counter to the taffrail (−18.73, 4.23).
- **`head_m`**: the knee's fore edge from K at (14.65, −3.66), (15.56, −3.25), (16.32, −2.50),
  (16.64, −2.00), (17.16, −1.00), **(17.60, 0.00)** at the line, (18.10, 1.00), (18.93, 2.00),
  (19.62, 2.50), (20.33, 3.00), to the scroll: its foot (20.51, 3.15), its fore side (20.65, 3.49),
  its top (20.52, 3.64). Measured (Pages §5.4, §6.2's twenty points; task 3).
  - *Was*: the knee's fore edge forward to about x 18.7 at z 2.4 to 3.3. That end was where the
    body plan's frame begins on the sheet, and the knee runs on over it: a local cause (Pages §8).
- **`wales_m`**: the main wale, a band of three strakes, both edges traced the whole length
  (measured, Pages §5.3; task 4). 34 points [x, lower edge, upper edge], from [−16.0, 0.66, 1.38]
  aft, by **[0.0, 0.02, 0.88]** at midships, to [17.0, 1.06, 1.90] forward. Its lower edge lies on
  the line amidships within 2 cm.
  - *Was*: [x, 0.10, 0.95] at midships, rising to [17.0, 0.95, 1.22] and [−17.0, 0.81, 1.47]. The
    datum moved it 0.07 m amidships, and the bow's upper edge sweeps up 0.7 m higher than was read.
- **`breadth_m`**: 25 triples [x, half-breadth at the line, half-breadth at the rail], one a
  station (measured, Pages §5.1, §6.2; task 1): from (−14.36, 1.55, 2.85) at aft 11 to (15.63, 1.34,
  2.59) at fore 11, with 4.53 and 4.42 m at the three "m". The stations lie every **4.506 pies
  (1.255 m)**. The half-breadths are as drawn; moulded or outside the plank is **JUDGEMENT** (Pages
  §6.4).
- **`section_m`**: the midship station "m" as drawn, 21 points, from (−3.26, 0.09) by (0.00, 4.53)
  to (2.62, 4.42) (measured, Pages §6.2). Its area to the line is 20.16 m², Cm 0.68 (computed).
  Whether its half-breadths are over the plank is **JUDGEMENT** (Pages §6.4).
  - *Was*: Dia §2.6's fifteen points, plank on. The datum moved them −0.07 m.
- **`form`**: `stern: {type: square, knuckle_z_m: 3.20, transom_hb_m: [1.95, 1.99]}`. The transom is
  the body plan's upright aftermost line, at 7.0 to 7.13 pies; the stern's reading does not close
  (Pages §5.5), so this is **JUDGEMENT**. **`head: scroll`** (was `knee`; read, the lead's ruling 6).
  `fullness` from the traced sections.
- **`marks`**: every line `sourced` but `form.stern.lights_m` (`judged`).

### 3.3 The hawse holes, the chains, the sweep ports

The hawse holes (16.70, 2.35) and (16.90, 2.35), the chains' deadeyes at the rail, and the small
square openings between the ports (Dia §2.7) have no key in the profile. They go into her note;
the small openings are read as sweep ports (JUDGEMENT), and **no sweeps fit is proposed**: no source
says she rowed. **2026-11-20:** the hawse holes are (16.72, 2.40) and (16.92, 2.40), re-referenced
for the datum (computed, not re-measured; Pages §6.2). The sweep ports were not re-measured.

### 3.4 Why every hull line is `sourced`

The plan is hers, drawn by the navy that held her, with her name, her guns and her captain on it;
nothing is scaled from another hull. The only judgement in the shape is the load line's meaning,
and the displacement check stands beside it (§3.6 task 2). **2026-11-20:** the load line is ruled.
The judgements left in the shape are four, each marked where it falls:
- the false keel's reading (Pages §4.1);
- the deck's red line (§2);
- the plank, moulded or not and how thick (§2);
- the stern's reading (Pages §5.5).

### 3.5 What the drawing must show her to be

A small flush-decked ship of one tier: a long straight sheer rising gently to both ends with no
step for a quarterdeck or forecastle, a bulwark pierced for eleven guns a side with the hammock
nettings above it, the wale close above the water, a square stern on a raked post, a knee of the
head with two rails and no figure, and a sharp rising floor under the water (kept as data). She is
to be told at a glance from the frigate (taller, stepped, longer) and from the brig-sloop (two
masts). **2026-11-20:** the knee of the head ends in a scroll, no figure (read; Pages §5.4).

### 3.6 The builder's measuring tasks (step 1)

**Done 2026-11-20** (Pages), each as noted:

1. **The half-breadths by station** at the line and at the rail (`breadth_m`), and at each port's
   sill (the triples), on the half-breadth and body plans; each station labelled as the plan
   labels it (aft 11 to 1, m, m, m, fore 1 to 11, every 4.49 pies). *Done*: Pages §5.1, §5.7. The
   stations are every **4.506 pies (1.255 m)** (measured on the larger image).
2. **The drawn displacement**: the sections integrated to the arrowed line, against the table's 497 t
   (Research-74 §3.5's method); and the profile's area under the line, against 104.4 m². If the
   drawn volume misses the table by more than 5%, the load line is put to the lead before anything
   else is filed. *Done*: Pages §4.3, §5.6. It missed (−6.5% at three pulgadas), and it went to the
   lead and was ruled (§2).
3. **The stem's fore edge, the forefoot and the head's knee** traced point by point. *Done*: Pages
   §5.4.
4. **The wales' two edges** traced the whole length. *Done*: Pages §5.3.
5. **The transom**: its breadth at the taffrail and at the knuckle from the body plan's aftermost
   section; the counter's knuckle on the sheer. *Done*: Pages §5.5, with the reading marked
   JUDGEMENT.
6. **Steel 1794 vol. I, the "20 Guns" column of the masts and yards** (pp. 49-50), read on the page
   image, beside §4.1's Luce figures. *Done*: Pages §7 (p. 50, "20 GUNS. 429 Tons."; §4.1).
7. **A larger image of the plan**, if the Biblioteca Virtual de Defensa's viewer serves one, to read
   the small lettering and the hourglass fitting at x +7.05. *Done*: 16,868 × 5,949 px, the record's
   image group 350671 (Pages §1.1). Nothing more is written on the sheet than the stations, the
   diagonals' numbers and the table (read). The hourglass fitting is **a ship's bell in a red
   belfry at x +7.14**, its mouth about 2.5 m and its frame's top about 3.3 m above the line (read,
   measured; judgement on its use: Pages §5.8).

---

## 4. The rig

### 4.1 Masts and yards (rung C by Luce's chain; places and rakes rung A)

Her `main_len` by Luce = (LWL + breadth) / 2 = (112.9 + 29.7) / 2 = **71.3 ft (21.73 m)** heel to
head, against the frigate's 87.7: **every spar is the frigate's times 0.8132**. Her own mast heels
replace the frigate's 14 ft from the step to the deck: the main's 3.53 m (11.6 ft), the fore's 3.27 m
and the mizen's 3.40 m (the plan's heels at z −2.10, −1.69 and −1.69 to the deck at side over each,
measured). Her heights above the deck follow from her own heels; the scratch probe of §9 took the
frigate's 14 ft scaled instead, which stands her main 0.2 ft (6 cm) higher (arithmetic; the
difference moves nothing measured).

**2026-11-20.**
- **The heels** in the corrected frame are z −2.18 (main), −1.66 (fore) and −1.87 (mizen) (computed,
  Pages §6.2; not re-measured). The deck moves with them, so each heel-to-deck stands within 2 cm.
- **The chain on her measured waterline**, 34.47 m (113.1 ft): Luce's main is (113.1 + 29.7) / 2 =
  **71.4 ft (21.77 m)**, and every spar is the frigate's times **0.8145** (was 0.8132; computed).
  That is +0.17%: the main yard 19.79 m, the bowsprit 13.60 m, the rest alike. The module computes
  them from its particulars; the table keeps the first figures, each 0.17% short.
- **The places and rakes** are taken into the line's frame (computed, not re-measured; Pages §6.2).
  The places move 2 or 3 cm. The line slopes 0.53° on the image, so each rake gains 0.5° aft and the
  bowsprit's steeve 0.5°.

| Spar | Place (x at the deck), rake | Length or height, by the chain | Check |
|---|---|---|---|
| Fore mast | +12.47, plumb → **+12.50, 0.5° aft** (2026-11-20) | 0.9 × 71.3 = 64.2 ft (19.6 m) heel to head | Babron's Spanish corvette 1.1°; **Steel 64 ft 0 in (−0.3%)** |
| Main mast | −2.31, 5° aft → **−2.29, 5.5°** | 71.3 ft (21.7 m) | Babron 6.2° (corvette), 4.4° (frigate); **Steel 72 ft 0 in (+1.0%)** |
| Mizen mast | −11.40, 5½° aft → **−11.38, 6°** | 13/15 of the main above the deck | Chapman's mizen at 0.181 L; Steel 61 ft 0 in |
| Topmasts, topgallant and royal masts | — | 0.6, then halves, then two-thirds | the frigate's chain; Steel's within 1%, with no royal masts (Steel's royals on the topgallants' poles) |
| Main yard | — | 10/11 × 71.3 = 64.8 ft (**19.76 m**) | Falconer 19.87 m; Chapman 17.97 m; **Steel 63 ft 0 in, 19.20 m (−2.8%)** |
| Main topsail, topgallant, royal yards | — | 14.82, 9.53, 6.35 m | Chapman's topsail 14.20 m; Steel's topsail yard 45 ft 6 in, 13.87 m (−6.4%) |
| Fore yards | — | 0.9 of the main's (fore yard 17.8 m) | Steel's fore yard 55 ft 0 in, 16.76 m (−5.8%) |
| Crossjack and mizen yards | — | 5/7 of the main's (crossjack 14.1 m) | Steel's cross jack 40 ft 0 in, 12.19 m (−13.6%) |
| Bowsprit | stem head, steeved about 21° (A) → **about 21.5°** to the line | 5/8 × 71.3 = 44.6 ft (13.6 m), a third inboard | Babron 17.3° to 30.2°; Chapman 29.7°; Steel 43 ft 6 in, 13.26 m (−2.5%) |
| Driver boom, gaff | — | 35.6 ft (10.9 m), 28.5 ft (8.7 m) | Steel's driver boom 45 ft 6 in, 13.87 m (+28%); Steel's mizen yard 28 ft 6 in, the gaff's length |

Steel's column (1794, vol. I p. 50, "20 GUNS. 429 Tons.", read on the page image: Pages §7) is
set against the first figures. Steel's masts agree with Luce's chain within 1%; the yards are shorter,
by 3% at the main yard, 6 to 10% aloft and 14% at the cross jack, and the royal yards and driver boom
are longer. So Steel stands between Luce and Chapman, nearer Luce, and the pick stands. On the chain at
34.47 m Steel's main yard is 3.0% under it (computed).

Her masthead stands about **29 m** above the water (observed on the scratch file: 29.1 m; the
frigate's 35.9), which sets her horizon (`world.ships.rig_height_m`). **Brace limits**: the
frigate's, level for level (no source for hers).

### 4.2 Sails

The frigate's set at 0.8132 in length and 0.661 in area: **plain sail 1,047 m²** (the frigate's
1,584; observed). **2026-11-20:** at 0.8145 on her measured waterline (§4.1), 0.663 in area, about
1,051 m² (computed). Courses, topsails, topgallants and royals on fore and main; topsail, topgallant
and royal on the mizen; the driver on its gaff and boom; the fore topmast staysail, jib and flying
jib; the main and mizen staysails; the studding sails and save-alls; the storm canvas. Reef bands,
canvas numbers and cloth ratings as the frigate's (the ratings at the area's scale). The 1809
drawing (eye) shows every one of these but the studding sails.

### 4.3 The handling (Dia §3.3)

No lateen: B3.1 does not reach her. Her mizen carries its crossjack, so B3.4's rule classes all
three masts square (observed); neither classing limit touches her. She heaves to with the main
topsail aback, as the frigate does (observed, §9).

**As built and measured, 2026-11-24** (her builder's report §§11 to 16; the owner's word, Decisions
Part F, rows D-s2 and D-j3; the lead's nudges 61 to 70): **a light ship with a small rudder: in a
fresh breeze keep her jib on her; taken in, she gripes up past her helm and will not be held until
it is set again.**
- **Her spanker** is the 95 m2 her own spars carry by her note's rule, not the frigate's scaled
  111 m2. Her helm is about amidships close-hauled, and truth D is restated as measured.
- **Under all plain sail** she stays in 12 and 15 kn, in 8 kn from one heading of three, and she is
  slack in stays in 20 and 25 kn. In a breeze the cause is the tack script's one moment for
  "mainsail haul", a point on the bow for every ship, which takes what swing a light, fine ship has
  left. Hauled with the wind ahead, Luce's other reading, she stays.
- **Shortened by the game's own order** she stays in 20 kn. In 25 kn that order takes her jib in,
  and with it in she gripes past her rudder (the least of any committed ship's to her lateral
  plane, 0.0245, traced from her plan). With `set the jib` again she bears away, gathers way and
  stays.
- **The engine's part** (the haul's moment; a jib taken in where a ship cannot be held without it)
  is booked as package 125. When it lands she is measured again, and truth D goes back to its first
  band if she then holds it.

### 4.4 Item 37, the generator's studding law

Her studding sails are written by the generator's copy of the sail-force law (the studding class at
1.25 where the engine reads 1.44: the lead's note of 2026-11-18). By the lead's word it is settled
before any new file is generated; her file takes whatever is then the generator's, and her
studding sails' figures move with it. Nothing of hers decides it.

---

## 5. The guns (package 81's checklist)

### 5.1 The fits

| Fit | Guns | Ports | Source |
|---|---|---|---|
| `danish 1807` (**proposed; the owner's**) | 16 × 30-pdr carronades, 4 × 8-pdr long guns | carronades in ports 2 to 9 a side, the long 8s in ports 1 and 10 (JUDGEMENT: no source places them) | Roos p. 94; the 1809 caption (p. 101) |
| `as captured 1809` | 20 × 24-pdr carronades | ports 1 to 10 a side | Winfield p. 930 |
| **`carronadas de a 30 1810`** (default) | 20 × 30-pdr carronades | ports 1 to 10 a side | Winfield p. 930; the plan's title |
| `1817` | 12 × 12-pdr long guns, 8 × 30-pdr carronades, 4 × 3-pdr obuses | the 12s in ports 1 to 6, the carronades in 7 to 10 a side (JUDGEMENT), two obuses in the bow ports and two over the rail by the mizen (JUDGEMENT) | Winfield p. 930 |

**The default is the plan's own fit**, the one her lines are drawn for; a scenario of 1807 or 1817
names its fit.

### 5.2 The checklist, item by item

1. `hull.profile` with `rail_m`, `breadth_m` and `decks_m.upper`: §3.2.
2. `ports_m.upper`: a triple at every broadside gun's and chaser's `x_m`, the sill the plan's at
   that x, the half-breadth the side's at the sill (§3.6 task 1); the obuses over the rail by the
   mizen get triples whose sill stands 2 in under the rail (`OVER_THE_RAIL_M`).
3. `port_size_m.upper`: [0.87, 0.66], one size on the deck (the plan's ports are alike).
   **2026-11-20:** **[0.83, 0.66]**, measured on the larger image (widths 284 to 293 px, the median
   286.5; Pages §5.7).
4. Every gun's `kind` (`carronade`, `long`; the obús a `carronade`'s pattern or its own word,
   the lead's: §17.2), `pounder` (by the owner's rule: §17.1 question 2), `place` (`broadside`;
   the obuses' place JUDGEMENT), `side`, `x_m`, `weight_cwt`, `deck: upper`. **Weights** (no source
   gives hers; each listed as more than a tenth off where it may be): the 30-pdr carronade 17.1 cwt
   (Adye's 32-pdr pattern), the 24-pdr 13.0 (Adye's 24), the long 8 about 23 (JUDGEMENT, drawn as
   the long 9's pattern), the long 12 34.0 (the generator's British 12), the obús about 3
   (JUDGEMENT).
5. `python tools/check_viewer_guns.py data/ships/corvette-20.yaml` clean, and its test.

### 5.3 Crews, the magazine, the weight

- **Crews**: the carronades by Douglas's four (`DOUGLAS_CARRONADE_CREW`), the long guns by
  `gun_crew` on their weight (D31 (c)'s rule for the new ships), the obuses two (JUDGEMENT).
- **The magazine** by `fit_magazine` on each fit's guns; the pounders' keys as the rule of question
  2 files them.
- **The weight on her deck**: twenty 30-pdr carronades about 17 t; the 1817 fit about 28 t (twelve
  long 12s), higher in her than the carronades. A fit carries guns and stores only, so her GM is
  one figure for every fit; the 1817 fit's tenderness is in her note and the risks (§16), not
  modelled.

---

## 6. The company and the people file

### 6.1 167, and how it is made up

Winfield's 167 for the Spanish ship (B). The Danish 161 aboard in 1807 is within 4% (Roos p. 90),
so **one company of 167 serves every fit** (a fit cannot change the muster; JUDGEMENT), the Danish
establishment of 120 and the 161 in her note. **How the 167 are made up is JUDGEMENT** until
Winfield's establishment for a corvette is read (Dia §11 item 2): the frigate's shares scaled.

**Revised 2026-11-19: the establishment is read.** The regulation of 1 January 1788 (Winfield et al.
2023, p. 1446 and following; VR-Sp §15), the first to name corvettes (pp. 904-906), gives a
corvette of 18 to 22 guns in peace **138**: a teniente de navío commanding, a teniente de fragata
and three alféreces; 5 major officers (purser, chaplain, surgeon, pilots); 11 sea officers; **40
infantry and 10 infantry-artillery**; 21 artillery; 20 seamen, 20 landsmen and 6 boys. Her own 167
is 29 more (computed); it stays her company, as her entry gives it. **Her soldiers are the
regulation's 50** (was 25 by the frigate's share, JUDGEMENT), the count sourced and its place in
her 167 JUDGEMENT; the other seven stations take the remaining 107 on their old shares (computed,
rounded by the largest remainders):

| Posts (10) | captain, first lieutenant, second lieutenant, master, boatswain, gunner, carpenter, purser, surgeon, sailmaker |
|---|---|
| Stations (157) | forecastle 17, fore top 15, main top 19, mizzen top 9, afterguard 31, waisters 22, marines 25, idlers 19 → **2026-11-19:** forecastle 14, fore top 12, main top 15, mizzen top 7, afterguard 25, waisters 18, **marines 50**, idlers 16 |
| Ratings | the frigate's shares (0.3 able, 0.4 ordinary, 0.3 landsmen) |
| Idlers by trade | the frigate's shares scaled to 19 (16 since 2026-11-19) |

- **Marines**: Spain's soldiers embarked, the nation's kit (`data/nations.yaml`, Spain `marines:
  {kit: basic}`); 25 by the frigate's share (JUDGEMENT). The Danes carried a petty officer and ten
  soldiers (Roos p. 94): in the note. **2026-11-19: 50**, the 1788 regulation's infantry and
  infantry-artillery for her rate (the Spanish kit, N3, if it lands first). In the engine marines
  serve carronades and no long gun (Bel-D §6.3), so in her carronade fits they man guns; in the
  1817 fit, with twelve long 12-pounders, her builder measures whether every crew is manned, and
  says so if not (as the three-decker's: Con-D §6.1).
- **The posts' words are the game's English**, as for every ship (the *teniente de navío* who
  commanded her is "the captain").

### 6.2 Her watches, and ruling 11

Two watches, starboard and larboard, each station halved, the posts and idlers keeping none: the
King's ship's rule, as the frigate's. **Package 75's ruling 11** (a merchantman's master or mate
counted a hand of their own watch where the watch is too small for the work) is a merchantman's
rule; every fit
of hers is a man-of-war's, so it does not reach her, and no merchant fit is proposed (no source
puts her in trade). Her builder runs every evolution's want against her watches (about 56 a watch)
and lists those that call all hands (the anchor's twelve forecastle hands against her watch's eight
or nine, as package 116's road for a small company has it). **2026-11-19:** with 50 marines, about
45 a watch and seven of the forecastle (computed), so more of her work calls all hands; her builder
lists it.

### 6.3 The people file and her name

`data/people/corvette-20.yaml`: her posts' people. **Their names**: Spain's row in
`data/nations.yaml` reads `names: english` today, so a Spanish ship's people would be named in
English. A Spanish list of names is new data, the package's to add once for the xebec and the
three-decker as well; the owner's (§17.1 question 6). Her captain of 1809-1810 was Teniente de Navío
José de Julián (the plan) and of 1807 Captain-lieutenant C. N. Meyer (Roos); a scenario may name
them, her file names none.

### 6.4 Package 116

Her company meets package 116's evolutions: `rig the relieving tackles` wants six of the afterguard
and waisters (she has 31 and 22; 25 and 18 since 2026-11-19), `repair the wheel` four able hands of
the idlers and afterguard.
She steers by a wheel (JUDGEMENT: a frigate-built ship of 1804; the plan's inboard works aft are
not read for it, §3.6 task 7).

---

## 7. Ground tackle, boats, pumps, hold and stores

By the generator's helpers on her burthen (§2: 449 tons by the old English measure) and the
frigate's patterns scaled:
`ground_tackle_for`, `boat_entries` (a launch, a cutter and a jolly boat by the frigate's
allowance at her size: JUDGEMENT; the launch, the "chalup", was put down in 1807, Roos p. 99),
two chain pumps and two hand pumps (`pump_entries`, JUDGEMENT), `hold_for`, the frigate's ration
and stores per man. Steel 1794's anchor and cable tables, the "20 guns" column, are the check
(read at step 1 with §3.6 task 6). **2026-11-20:** not read at step 1, whose task 6 was the masts
and yards (Pages §7); still open, for her builder.

---

## 8. Far description, rank and the made-out words

### 8.1 Her description

| Key | rig (the tops, at the rig's distance) | what (the glass, at `MADE_OUT_NM`) | note |
|---|---|---|---|
| `corvette` | **"a ship"** | **"a corvette, flush-decked, eleven ports a side"** | The Spanish navy's corvette of 1809-1817, the Danish light frigate of 1804 (Winfield p. 930; Roos p. 94): what the glass makes out, one tier of ports in a flush side, three masts square-rigged on a small hull |

With `fit: carronadas de a 30 1810` and `roles: [kings-ship, cruiser]`. **The roles.** `kings-ship`
first, as every navy's warship of the game's: Spain's corvette 1809-1832, Denmark's light frigate
1804-1809. `cruiser` second: a corvette sent against an enemy's trade or privateers on a coast, her
prize doctrine read from `data/captains/cruiser.yaml`'s `thresholds:` as package 116 made it read,
with no row of her own. **No regency role**: the Barbary regencies' cruisers are the xebec's role in
this package; no source puts the *Diana* in a regency's service (she called at Algiers once, with
Denmark's tribute: Roos p. 87). No merchant, packet or privateer role: no source.

### 8.2 The made-out rule, applied

- **At the rig's distance** (`RIG_MADE_OUT_NM`, 4 nm; 6 with a glass aloft): "a ship". By
  `captains._SIZE_WORDS` "a ship" is **rank 3, a frigate's class**, so a lone brig-sloop that sights
  her there takes her for a frigate. Her size is all that could tell otherwise, and a 113-ft ship
  and a 140-ft one are not told apart at four miles by a lookout's eye (JUDGEMENT). **Pick: keep
  it so**; the lead's to rule (§17.2), since the 74's ruling gave the line-of-battle ship her class
  there by her two tiers, which a corvette has no counterpart for.
- **Made out** (`MADE_OUT_NM`, 1.5 nm; 2.25 with the glass): "a corvette, flush-decked, eleven
  ports a side", **rank 2** (a new size word "corvette" at 2, placed before "a ship" in
  `_SIZE_WORDS`): the brig-sloop's class, a match for her.
- **Her words in `_DESCRIPTION_WORDS`**: "a corvette", "corvette", "a ship-sloop", "ship-sloop",
  "a ship sloop". **Not taken**: "a sloop of war" (the brig-sloop's today), "a light frigate" and
  "a frigate" (which would rank her 3 as made out). "Ship-sloop" holds "a ship" when padded
  (`size_rank_of`), so the size words ("ship-sloop", 2) and ("ship sloop", 2) go before
  ("a ship", 3) with "corvette"'s (read: `_SIZE_WORDS` is matched in order, the first word found
  ranking).
- **Her colours** are the scenario's: Spain's red and yellow, or Denmark's Dannebrog for 1807
  (`data/nations.yaml`, read).

---

## 9. What the engine does today, and what it must be given (observed)

**The probe.** A scratch file built in memory from `data/ships/frigate-36.yaml` and validated by
`spec_from_dict`: her hull block (§2, at the first reading's 3.58 m and 1.39 m, with the frigate's
rudder scaled to 3.84 m² and no profile); every spar and sail the frigate's times 0.8132; her masts
at the plan's first reading (+12.47, −2.38, −11.42; raked 1.0°, 4.4°, 5.5°); her company of 167 on
the frigate's stations scaled; the frigate's guns moved to her length. Run with the
truths' own helpers (`tests/test_known_truths.py`: `under_plain_sail`, `close_hauled_on_starboard`,
`until`, `plain_sail_minutes`; seed 7, the wind from the north, no gusts) and `world.ships.polar_of`.

| Measure | Her | The frigate |
|---|---|---|
| Static polar, 8 / 15 / 25 kn, best | 4.58 / 7.96 / 11.11 kn, at 90° to 100° | 4.62 / 8.19 / 11.63 |
| Closest course; `beat_deg(15)` | 50°; 60° | 50°; 60° |
| 15 kn, 66° / 90° / 112° / 135° / 160° (GM 1.0) | 4.71 / 7.74 / 7.52 / 6.96 / 6.16 kn; heel 5.7 / 9.2 / 6.2 / 1.9 / 0.2°; helm +1.8 / +2.0 / +2.1 / +0.5 / −0.3° | 4.80 / 7.97 / 7.73 / 7.10 / 6.28; heel 3.4 / 5.5 / 3.7 / 1.1 / 0.1; helm +1.3 / +2.0 / +2.1 / +0.5 / −0.4 |
| 15 kn, 66° / 90° (GM 1.5) | 4.72 / 7.76 kn; heel 3.8 / 6.1°; helm +1.8 / +2.0° | as above |
| 22 kn, 90°, heel by GM 1.0 / 1.5 / 1.8 | 19.0° / 12.9° / 10.8° (10.0-10.1 kn) | 11.3° (10.45 kn) |
| 22 kn, 66°, heel by GM 1.0 / 1.5 / 1.8 | 12.3° / 8.2° / 6.8° | 7.3° |
| Meyer's case, 118°, 18 / 25 kn, plain sail (GM 1.5) | 8.67 / 10.66 kn, heel 4.7 / 8.0° | — |
| The same on Chapman's smaller rig (0.739) | 8.10 / 10.15 kn | — |
| Hull speed 11.0 / 12.5 (GM 1.5), 118° in 25 kn | 10.35 / 10.90 kn | — |
| Tack (truth 10: 290°, 292.5°, 295°), GM 1.5 | 349 / 369 / **164 s**, each losing 13 / 36 / 9 m | 343 / 447 / 370 s, +51 / −37 / +25 m |
| Wear (truth 11), GM 1.5 | 491 s, 259 m to leeward | 513 s, 234 m |
| Heave to, 15 kn; fill away | hove to in 132 s, 61° off at 1.3 kn after ten minutes; filled in 59 s | 220 s, 62°, 1.3 kn; 59 s |
| Plain sail from furled, the watch / all hands | 11.5 / 9.6 min | 16.4 / 5.6 min |
| Masts classed by B3.4 | all three square | the same |

**What it shows.**
- **Her rig needs nothing new.** Every evolution tried is the frigate's and works on her.
- **Meyer's 10 to 11 knots** with the wind 2-3 points abaft the beam in a fresh breeze are met at the
  breeze's strong end (10.7 kn at 25 kn) by the frigate's hull speed scaled by √L; the weaker end
  (8.7 kn at 18) is under the report's figure, given as the best of a freshening wind (truth B's band
  is set on the strong end: §14).
- **She must be given her stiffness**: GM 1.5 (decision 4). The frigate's GM scaled by her breadth
  makes her heel 1.7 times the frigate because her displacement is 0.39 of the frigate's while
  Luce's rig gives her 0.54 of its heeling moment; Meyer called her stiff.
- **The tack from 295° in 164 s** falls under truth 10's 285-second floor: a knife-edge tack of a
  light sharp hull; the builder tunes `clr_x_m` and the rudder against the three headings, or argues
  her own band (truth E).
- **All hands set her plain sail slower than the frigate's** (9.6 against 5.6 minutes), the watch
  faster (11.5 against 16.4): the sails' wants are per sail, so her smaller company tells when all
  are called; why her watch is the quicker was not found and is the builder's to explain before her
  pins are set (observed, not explained).
- **Her lee ports**: §10.

**What it must be given**: her file (§1-§7) with her profile; her GM (decision 4); her helm tuned
(`clr_x_m`, truth D); her rows (§12); nothing in `physics/`, `combat/` or the evolutions.

---

## 10. The lee ports

Her midship sill stands 1.78 m above the line over a half-breadth of 4.46 m: **her lee port dips at
about 21.8° of heel** (arithmetic on the plan), the ends' ports later (their sills higher, their
half-breadths less: task 1). **2026-11-20, accepted by the lead (ruling 6):** her midship sill
stands **1.72 m** above the line as drawn, over 4.46 m (port 6, measured), so **her lee port dips
at 21.1°** (computed). Port 5 dips at 21.2°, ports 4 and 7 at 22.0° and 21.6°, port 2 at 27.1°,
port 10 at 28.9° and port 1 at 33.5°; the bow port at about 48° (Pages §5.7). Most of the 0.06 m is
the datum's; the rest is the larger image's edges. Under L2 and L3 and the 60-second hold (package 75) her ports shut by
her triples with no new code. At GM 1.5 she heels 12.9° abeam in 22 knots under plain sail: her
carronades fight in any breeze she carries topgallants in, which is what a flush-decked carronade
ship's high sills were for (judgement).

---

## 11. Where she sails

- **Her waters are in the game**: Cartagena, Málaga, Alicante, Almería, Algiers and Gibraltar have
  port files (`data/ports/`, read) on 79c's charts.
- **Her years ask dated wars of `data/nations.yaml`**, which holds 1805's (Britain against France,
  the Batavian Republic and Spain; Denmark at peace with all). A scenario of hers wants: Britain and
  Denmark at war from 1807; Britain and Spain at peace from 1808 and allied from 1809; Spain and
  Denmark at war from 1809 (memory; each to be sourced by the scenario's package). That is a
  scenario's data change, not hers.
- **Scenarios proposed** (booked for a card of their own after the nations' dated wars, the plan's
  §4 row 15: none is in the build's card, and she is offered from the harbour for a bare start;
  nothing is written here):
  1. *Off Cartagena, 17 September 1807*: the Danish light frigate from Algiers, her bowsprit sprung,
     a British 44 that has chased her a day coming up under her lee at dawn; the `danish 1807` fit
     under the Dannebrog. Her captain lay to and spoke the Briton (Roos pp. 98-99).
  2. *Out of Cartagena, 1810*: the Spanish corvette of twenty carronades on the coast of Murcia and
     Valencia, French privateers about; the default fit.
- **Shelf lines** (`client/harbour-shelves.yaml`, a sentence each, for the scenario's package):
  - "The Danish light frigate Diana off Cartagena in September 1807, her bowsprit sprung and a British forty-four closing under her lee."
  - "The Spanish corvette Diana out of Cartagena in 1810, twenty carronades and the French privateers of the coast about."

---

## 12. Interfaces: her stage 0 and the engine's rows

The package's stage 0 lays, behaviour-free, the keyed rows a new man-of-war's description needs
(the 74's lesson, Research-74 §7.6 item 1: without them a far ship of hers sails as a merchant), and
her `DESCRIPTIONS` row and words land with her file, from her builder (Plan §5.1 items 6 to 8; a row
names a file, and the harbour offers every row):

| Where (at 68e769ef) | Row |
|---|---|
| `freesail/world/ships.py` `DESCRIPTIONS` (:181) | `"corvette": {"file": "data/ships/corvette-20.yaml", "rig": "a ship", "what": ...}`, with her file |
| `freesail/world/ships.py` `_DESCRIPTION_WORDS` | §8.2's words, with her file |
| `freesail/world/captains.py` `SIZE_RANK` (:296) | `"corvette": 2` |
| `freesail/world/captains.py` `_SIZE_WORDS` (:331) | `("corvette", 2)`, `("ship-sloop", 2)` and `("ship sloop", 2)` before `("a ship", 3)` |
| `freesail/world/brains.py` `role_of_vessel` (:245) | `corvette` with the King's ships, or her file's first role through `sub_type_role` (the builder says which reaches first) |
| `freesail/world/regimes.py` (:197), `world/squadrons.py` (:474, :1577) | `corvette` in the men-of-war's descriptions |
| `freesail/orders/signals.py` (:277) | "corvette" among the words a hail is heard by |
| `tools/gen_ships.py` `SHIP_MODULES` (:10399) | `diana` |

The descriptions' caches hold 32 files (`world/ships.py`, `file_descriptions` and its kin): eighteen
today, twenty-six with the package's eight (the tartane's two, the polacre's two, the xebec's two,
hers and the three-decker's: Plan §10.4); no change.

---

## 13. What the viewer must draw

From her profile, by the viewer's rules as they stand (Build §6, package 81):
- **The hull**: the flush sheer and the bulwark to the waist rail; the eleven ports a side with their
  lids (81's rule from the triples); the wale's band close above the water; the square transom on
  the raked post and the counter; the knee of the head with no figure; judged stern lights.
  **2026-11-20:** the knee ending in its scroll (`head: scroll`), the post raked 10.5°, the counter's
  knuckle and the upright upper stern (§3.2); the hull trimmed by the stern as drawn, its keel
  sloping 0.27 m in her length.
- **The masts at her rakes**: the main's 5° and the mizen's 5½° show (1.7 m of lean at a 20-m head);
  the bowsprit at 21°. **2026-11-20:** in the line's frame the main's 5.5° and the mizen's 6° (1.9 m
  of lean at a 20-m head, computed), the bowsprit at about 21.5° (§4.1).
- **Not drawn, said in her note**: the hammock nettings over the rail (no key), the chains and
  deadeyes (the viewer draws shrouds to the rail), the hawse holes, the sweep ports, the paint (the
  1809 drawing's light band and dark lids, in words).
- **The owner's sheets** (Build §6): her hull alone beside the frigate and the brig-sloop at one
  scale and normalised; her rung letters under it; the 1809 drawing beside her if the owner allows
  it into the tree (Dia §9).

---

## 14. Tests and truths proposed (numbers the lead's)

| | Truth | Measure | Today (observed) |
|---|---|---|---|
| A | **Her particulars hold their sources**: 124 × 32½ × 16 pies are 34.55 × 9.06 × 4.46 m; 540 t 691 lb is 497.2 t; she floats at 3.57 m; eleven ports a side at the plan's sills within 1 cm; each fit's guns by date. **2026-11-20:** 540 t 691 lb is **498.0 t** at the book's libra (the 2026-11-19 revision's figure, missed here then); she floats at **3.78 m** mean to the false keel's lower edge on the arrowed line as drawn, 3.91 m aft and 3.65 m forward (the lead's ruling 1; §17.2 item 7); her lateral area is the measured 122.2 m² (ruling 4); the sills are Pages §5.7's | equalities on the file | — |
| B | **Meyer's speed**: with the wind 112° to 124° off in 24 to 27 knots, under the sail her book carries in that wind, she makes 9.5 to 11.5 knots | sailed, settled | 10.66 kn at 118° in 25 kn under plain sail (GM 1.5); to be re-measured under her book's reduced sail |
| C | **She is stiff**: close-hauled and abeam under plain sail in 22 knots she heels no more than 1.15 times the frigate does, and her midship lee port stays open | sailed, both ships | 8.2° against 7.3° close-hauled, 12.9° against 11.3° abeam (1.12, 1.14) at GM 1.5 |
| D | **She steers well**: close-hauled in 15 knots 0.5° to 3° of weather helm, abeam 1° to 3° | sailed | +1.8° (heel 3.8°) and +2.0° (heel 6.1°) at GM 1.5; the frigate +1.3° and +2.0° |
| E | **She goes about as a ship should**: tacks from the three headings in 285 to 600 s and wears in 360 to 720 s (truths 10 and 11's bands) | the truths' helpers | 349, 369 and 164 s; wears 491 s: **fails from 295°** |
| F | **Her lee port**: the midship lee port shuts at 21.8° ± 0.5° of heel. **2026-11-20:** at **21.1° ± 0.5°** (1.72 m over 4.46 m, Pages §5.7; accepted, the lead's ruling 6) | L2's rule on her triple | — |

**Her tests** (`tests/test_diana.py`): her file regenerates byte for byte; her table's arithmetic;
the checklist's check clean; her description, rank and words served; her fits load and fill their
magazines; her people file resolves; every evolution's want against her watches listed.

---

## 15. Pins her work could move

No existing file's bytes (she is a new file). The shared guards that range over every file move by
her row, each old beside new: `tools/check_viewer_guns.py`'s test over `data/ships/`; truth 7-190's
lowest lee port by file; the profile tests' pair check (her outline against the brig's and the
frigate's: §3.5 says they must differ); `tests/test_subtypes.py`'s rows with fits and roles; the
harbour's list of files. No test today names "corvette" (searched: none), so no refusal moves.

---

## 16. Risks, ranked

1. **The load line.** If the arrow does not mark her load line, every z of her profile, her draught
   and her lee port move together (by up to 0.3 m for a foot). Task 2 measures it first.
   **2026-11-20: measured and ruled.** The drawn body misses the table by −6.5% to −4.9% at 3 to 4
   pulgadas of plank (−11.3% with none). A line 0.14 m higher, or the after draught carried level,
   would meet it. The lead ruled the arrowed line as drawn her load line and the miss recorded and
   explained: the table was most likely reckoned on the after draught carried level (§2). The risk
   left is the plank's judgement, 8 t a pulgada (§2), and the false keel's reading (Pages §4.1).
2. **Her first fit.** The owner's ruling and her own papers disagree (§17.1 question 1).
3. **Her stiffness is a judgement on a word.** GM 1.5 is tuned to "stiff"; Fincham's ratio for
   corvettes, which would give her more (Research-PrinceDeNeufchatel-2026-10.md §2.5: 2.51 m on the
   *Neufchatel*'s hull), is of the 1830s' corvettes and not taken.
4. **The foreign pounder** is a rule for every foreign gun to come (the xebec's, the three-decker's);
   settled once for the package (question 2).
5. **The 1817 fit's weight** (28 t on her deck against 17) under one GM: she would sail stiffer in
   the game than she did in 1817 (judgement).
6. **Her spars by rule**: Luce's chain may overspar a Danish light frigate; Chapman's is 9% smaller
   (question 4).
7. **The knife-edge tack** (164 s from 295°).
8. **Names** (Spain's `names: english`).

---

## 17. Open for the owner or the lead

### 17.1 For the owner (few, plain; each with the design's pick)

1. **Her guns when she was taken.** Your ruling of 2026-11-06 gives Winfield's three fits, the first
   "twenty 24-pounder carronades as captured". Her own papers (Roos 1957, p. 94) and the caption of a
   drawing of her signed "Thomsen pinx 1809" (perhaps her officer of that name) say the Danes armed
   her with sixteen 30-pounder carronades and four long 8-pounders. *Pick:* keep Winfield's three as you ruled and **add a fourth fit, "Danish 1807"**,
   from her papers, for a scenario under Danish colours; and ask Winfield's p. 930 for the source of
   the book's "as captured" (Dia §11). *2026-11-19:* the whole entry gives no source (VR-Sp §17);
   your four fits stand as answered. *What you would see:* in an 1807 scenario off Cartagena she shows a
   long gun at each end of her battery on either side and carronades between; in 1809 and after, as
   Winfield has her.
2. **How a Spanish or Danish gun's pounds are written.** A Spanish "30-pounder" fires 30 Spanish
   pounds (about 30½ English); a Danish one about 33 English. *Pick:* write the gun as its own navy
   named it (a 30-pounder), with the English weight in its note; the game's range and weight of
   broadside then read it a little light (by 1.5% for Spain; 1.6% by the book's libra, 2026-11-19). The other way writes the English
   weight (30.4, 33) and the words say "30-pounder" from a separate word key. *What you would see:*
   "the 30-pounder carronades" in her log and on her deck, as her people said it.
3. **Her stiffness.** Her captain called her stiff. With the frigate's proportion she would heel half
   again as much as the frigate and lay her lee ports under in a strong breeze. *Pick:* make her as
   stiff as the frigate (GM 1.5 m). *What you would see:* on a reach in a strong breeze she leans as
   the frigate does, a little more, and her carronades on the lee side keep firing.
4. **Her masts and yards.** None survive. *Pick:* the rule the game already uses for its frigate,
   applied to her size (her main yard about 19.8 m), with Chapman's Scandinavian rule (about 18 m)
   and Steel's British table as checks (*2026-11-20:* read, the main yard 19.2 m: Pages §7). *What you would see:* a lofty small ship, her royals about
   29 m above the water against the frigate's 36.
5. **Her colours in 1807.** *Pick:* the scenario chooses; her file carries no nation, as the
   privateer's does not. *What you would see:* the Dannebrog at her gaff in 1807, Spain's red and
   yellow after.
6. **Her people's names.** Spain's people are named in English in the game today. *Pick:* a list of
   Spanish names for this package's Spanish ships, hers first. *What you would see:* her lieutenant
   and her boatswain with Spanish names in her log.

### 17.2 For the lead

1. **The rank at the rig's distance** (§8.2): "a ship" ranks her a frigate until made out; keep, or a
   rule for small ship-rigged vessels?
2. **Her file's name**, `corvette-20.yaml`, and the description key `corvette`.
3. **The obús's `kind`**: a carronade's pattern, or a word of its own (it is a howitzer); with the
   xebec's and the three-decker's obuses in mind (the three-decker's 1803 fit has 48- and 24-pdr
   obuses).
4. **Item 37** settled before her file is generated (§4.4).
5. **The 1809 drawing** for `docs/references/images/` with its README row (Dia §9): the original is
   public domain by age; the road is the museum's own image with its terms, vetted as the README's
   rows are (artist, date, licence, namesake). Roos's 1957 reproduction is not offered until its
   status (a photograph in a work taken as in copyright, its page stating no licence) and the
   artist ("Thomsen", perhaps her officer) are vetted.
6. **Her place in the build order** (§0): the smallest build of the five, offered as the one on
   which the package's shared rules are settled first.
7. **The draught's datum** (2026-11-20, rulings 1 and 4). Ruling 1 gives her "3.76 m at the post
   and 3.49 m at the stem, to the false keel's lower edge", and ruling 4 names 120.0 m² for a
   measured area. Both figures are the keel's lower edge's. The false keel's lower edge, K, gives
   3.91 m and 3.65 m (3.78 mean), and 122.2 m² with the knee.
   - *Taken:* K for both, by ruling 1's words and by D29 (b), the method the hulls drawn from their
     draughts use: one deepest line for the draught and the lateral plane
     (`Decisions-ShipsRound2-2026-10.md`:516).
   - *If the keel's lower edge was meant:* `draught_m` 3.63 m, `lateral_area_m2` 120.0 m², truth A
     at 3.63 m; nothing else moves.
8. **Her length by D29 (b).** The drawn hulls file `length_waterline_m` rabbet to rabbet at the load
   line (the 64, the razee, the *Neufchatel*). Hers is the post's after face to the stem's fore face,
   34.47 m, as decision 3 has it since the first draft; between the rabbets she is about 33.6 m (Dia
   §2.4, not re-measured). Not changed here. If it is changed, her hull speed by √L (11.8 → 11.7 kn)
   and Luce's chain (−2.0%) follow (computed).
9. **The 0.85 rule** (a finding, §18 item 5): every hull drawn so far fills 0.93 to 0.99 of its
   length times its draught under the line, and the rule stands in the files of six hulls whose
   profiles are drawn. Whether those files move is the lead's and the owner's.

---

## 18. Found on the way

1. `docs/design/VesselReferences-2026-11-Spanish.md` §5 and the images README say the *Diana* was
   "taken at Cartagena with the declaration of war": Roos dates it to **26 September 1809**, two
   years after she came in (Spain's war on Denmark following its alliance with Britain of July
   1809). Not changed here (not a new document); for the lead.
2. The Wikipedia article on her (HDMS *Diana*, 1804) has her leaving Copenhagen on 7 July 1807; Roos,
   its own source, has command hoisted on the 6th and the anchor weighed on the 17th.
3. Winfield's broadside pairs (1,212 libras as 1,308 lb, a ratio of 1.079) are not the ratio of the
   libra castellana to the English pound (1.014); the lead's rule (take Winfield's pairs, do not re-derive)
   stands, and question 2 meets it.
4. `data/nations.yaml` has no war between Britain and Denmark and none dated after 1805 (§11).
5. **The generator's 0.85 rule is under every hull drawn from its draught** (2026-11-20, found
   reading the drawn hulls' method for ruling 4; Pages §5.6). On their notes' own bases the drawn
   profile under the line fills of the length times the mean draught: the 64 0.97 (Ind §2.3.6), the
   74 0.96 (Research-74 §3.2.6), the *Neufchatel* 0.99 (Neuf §2.6), the frigate-36 about 0.95
   (`pages-zaz2587.md` §9.1's 242 m², computed), hers 0.93 to 0.96. Yet the rule is still filed in
   six hulls whose profiles are drawn, recorded beside and not moved by package 75's rule:
   - the frigate-36's 160 m² against about 242 drawn (`tools/gen_ships.py`:2213);
   - the brig, cutter, lugger and smack at 0.85 (:7067, :6109, :8336, :9145);
   - the schooners at 0.78 (:3281);
   - the bilander, not drawn, by "the brig's rule" (`tools/ships/bilander.py`:406).

   A figure the physics reads, so a finding for the lead, not a change here (§17.2 item 9).
6. `docs/design/Plan-Package90.md` §8.0's report row for her still names "the lee port at 21.8°",
   now 21.1° (§10); not this change's file.
