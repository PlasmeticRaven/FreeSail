# Design: the corvette *Diana*, a Danish light frigate of 1804 in the Spanish navy (package 90, second draft)

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
Every `file:line` is at that head; a builder re-checks a line before using it.

**Marks.** *read*, *read (OCR)*, *measured* (off the held plan at 11.40 px a pie, ±2 px, about
±5 cm, where a line is clear), *observed* (printed by a scratch probe on the engine run from the
worktree with `py`, the tree first on `sys.path`; the scripts are in the session's scratch,
`scratchpad/p90/diana/probe/`, not filed; no tracked file changed, Python's git-ignored bytecode
caches aside), *judgement*, marked
**JUDGEMENT** where it is a figure a file would carry. Rungs are the brief's: **A** her own plans,
**B** a historian's particular, **C** judgement or a named rule on her particulars; in a file's
`marks` they are §5.0's words, `sourced` (A), `rule` and `judged` (C).

**One sentence.** One module writes one file: the Spanish navy's own plan of her at its own scale
(34.55 by 9.06 m, 497 t, drawing 3.57 m), a flush-decked light frigate of eleven ports a side with
her masts where the plan steps them, ship-rigged by the generator's frigate chain on her own
particulars, carrying twenty carronades of 30 by default and her other fits by date, her company
of 167, made out "a ship" by the tops and "a corvette" by the glass; the engine sails her today
with nothing new but her rows, once her stiffness is given her.

---

## Decisions proposed

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/diana.py`, `build(out_dir)` writing **`data/ships/corvette-20.yaml`**, `ship.name` *Diana*; added to `SHIP_MODULES` (`tools/gen_ships.py:10399`) | The package 75 pattern (one module a ship); the file named by type and guns as `frigate-36` and `razee-44` are |
| 2 | Her particulars as data in the plan's own units (pies, pulgadas, toneladas and libras, and the plan's pixels at 11.40 a pie), converted once in a frozen `Particulars` | Every figure reads as its source gives it (the *Bellerophon*'s §1.4) |
| 3 | **Her hull is the plan's, rung A, `sourced`**: LWL 34.40 m, beam 9.06 m (Winfield), draught **3.57 m** to the keel's lower edge at the plan's arrowed line, displacement **497,200 kg** (the table's 540 t 691 lb), deck 1.40 m | Dia §2.3-§2.5 |
| 4 | **GM 1.5 m, JUDGEMENT**, tuned to her captain's "stiff" (Dia §6) | The frigate's ratio (1.0 m) heels her 1.7 times the frigate (observed, §9); 1.5 brings her within 15% of it |
| 5 | Her profile wholly from the plan: rail, half-breadths by station, keel, stem, stern, wales, section, the gun deck and its eleven port triples, the port size [0.87, 0.66]; `form.stern: square`, `form.head: knee` | Dia §2.5-§2.7; Build §5.1; package 81's checklist |
| 6 | Masts at the plan's places and rakes (A); **every spar by Luce's chain on her particulars** (the generator's frigate rule), Falconer's yard rule and Chapman's the checks, Steel's 20-gun column read at step 1 as the third (C) | No spar of hers survives; the rule the game already uses for its frigate (Dia §3.2) |
| 7 | Her sails the frigate's set by the same chain: courses, topsails, topgallants and royals on fore and main, topsail, topgallant and royal on the mizen over a dry crossjack, the driver, three headsails, the staysails between the masts, studding sails | The 1809 drawing (eye, Dia §3.1); the frigate's file the pattern |
| 8 | **Four fits proposed**, three of them the owner's: `danish 1807` (16 × 30-pdr carronades, 4 × 8-pdr long guns; **the owner's to accept**), `as captured 1809` (20 × 24-pdr carronades), **`carronadas de a 30 1810`** (20 × 30-pdr carronades, **the default**, the plan's own), `1817` (12 × 12-pdr, 8 × 30-pdr carronades, 4 × 3-pdr obuses) | Winfield p. 930; Roos pp. 94, 101; owner's question 1 |
| 9 | Company **167** (Winfield), on the frigate's shares of stations scaled, 10 posts; two watches; **ruling 11 does not reach her** | Dia §5; she is a man-of-war in every fit |
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
- **What waits on sources**: Winfield's passages (Dia §11); Steel's 20-gun column on the page image;
  the Danish draught, if the owner wants it sought.
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
section; `raked_x` (:3202), with `deck_m=` her own 1.40; `broadside_pair` (:4519, `deck="upper"`),
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
  `LIBRA_KG = 0.4601`, `TONELADA_LIBRAS = 2000`.
- **The frame.** x in metres forward of the middle of her load waterline (image x 826.5: the
  post's after face at x 123 and the stem's fore face at x 1530 on the line); z above the line
  (image y 311). A spar's `height_m` and a sail's `corners_m` above her datum, the gun deck at
  midships, 1.40 m (D18 (a): her uppermost continuous deck, flush from end to end; no rival); a
  sail's centre above the water.
- **Checks before the file is written**, each `raise ValueError` with a sentence: the table's
  arithmetic (the two bodies sum to the total, the difference holds); Winfield's metres within
  0.01 m of the table's pies at 0.278635; every port gun on its triple to the centimetre; the drawn
  displacement against the table's (recorded beside it, never in its place: §5.0 principle 8);
  every mast's heel below the deck and above the keel.

---

## 2. The hull blocks

| Field | Figure | Source and rung |
|---|---|---|
| `length_waterline_m` | **34.40** | The plan, the post's after face to the stem's fore face at the arrowed line, 1,407 px (Dia §2.4, measured). A. The rabbets 33.56 m in the note |
| `beam_m` | **9.06** | Winfield's metres for the table's 32 pies 6 pulgadas, extreme (the body plan's frame, measured 32½ pies). A and B |
| `draught_m` | **3.57** | The arrowed line 11.45 pies above the rabbet, the keel 1.36 pies under it: 12.8 pies to the keel's lower edge, even keel (Dia §2.4). A for the drawing, **JUDGEMENT** on the arrow's meaning, checked by the table's displacement (Cb 0.48, Cp 0.72) |
| `displacement_kg` | **497,200** | The table's 540 t 691 lb at 2,000 libras of 0.4601 kg (Dia §2.3). A. The frigate's rule (Cb 0.55) would make her 627 t, 26% more: not taken |
| `gm_m` | **1.5** | **JUDGEMENT**: Meyer's "stiff" (Roos p. 94) against the frigate's heel in the same wind (§9). The frigate's 1.3 m scaled by the breadth gives 1.0, which heels her 19° abeam in 22 knots under plain sail |
| `clr_x_m` | **2.5** to start | The frigate's lead (3.0 m on 41.8) scaled by the length; tuned for Meyer's "steers splendidly" (truth D, §14) |
| `lateral_area_m2` | 104.4 | LWL × draught × 0.85, the generator's rule; the plan's profile under the line measured beside it (§3.6 task 2) |
| `hull_speed_kn` | **11.8** | The frigate's 13.0 by √(34.40 / 41.8); holds Meyer's 10-11 knots (observed, §9). Tuned within 11.0-12.5 by truth B |
| `deck_height_m` | **1.40** | The gun deck at side at midships above the line (Dia §2.5, measured) |
| `rudder` | area **3.0 m²**, span 3.57, 35°, 3.0°/s | The plan's blade under the line (Dia §2.5, measured ±0.3 m²); the frigate's stop and rate |
| `profile` | §3 | Build §5.1 |

**Her tons.** Winfield's 335 t is not the displacement; the rule behind it is asked (Dia §11). Where
the generator reads tons (the anchors, the boat, the hold: `ground_tackle_for`, `hold_for`) it wants
an English burthen, its tables being English. By the builder's old measure on her gun deck (124
pies, 113.4 English ft) and breadth (29.7 ft), (113.4 − 3/5 × 29.7) × 29.7 × 14.86 / 94 = **449
tons** (arithmetic; the frigate's 933 is matched by the same rule on her own figures within 1%).
*Pick:* 449 for the helpers, Winfield's 335 beside it in her note with its rule once Winfield's
passage gives it.

---

## 3. The hull profile and her shape (Build §5.0-§5.3)

### 3.1 What the sources give, by rung

| Feature | Source | Rung, mark |
|---|---|---|
| Length, breadth, depth, displacement | The plan's table, Winfield's row | A, B; `sourced` |
| The sheer, the rail, the deck, the wales, the keel, the stem, the post, the counter, the head's knee, the hawse holes, the ports | The plan's sheer (Dia §2.5, §2.7) | A; `sourced` |
| The half-breadths by station; the midship section; the after body's hollow garboards | The plan's half-breadth and body plans (Dia §2.6; the stations' half-breadths are §3.6's task) | A; `sourced` |
| The load line | The arrowed line (Dia §2.4) | A drawn, its meaning JUDGEMENT; `sourced` with the note |
| The stern lights | None drawn in the profile; a frigate-built ship certainly had them | C; `judged` by Steel's sheer-draught method (§5.0 principle 9), tagged on the owner's sheets |
| The figure | None drawn | none (`head: knee`) until the Danish draught or the 1809 picture shows one |
| The paint | The 1809 drawing: a light band along the ports, dark lids (eye) | words in her note only |

### 3.2 Her points (file frame, metres; Dia §2.5-§2.7, measured)

- **`rail_m`**: the waist rail, the bulwark's top: (−18.25, 3.52), (−16.78, 3.50), (−15.31, 3.35),
  (−12.87, 3.13), (−10.42, 2.96), (−7.98, 2.84), (−5.54, 2.74), (−3.09, 2.74), (−0.65, 2.69),
  (1.80, 2.69), (4.24, 2.69), (6.68, 2.74), (9.13, 2.81), (11.57, 2.88), (13.53, 3.01),
  (16.46, 3.01), (17.44, 3.10), to the stem head at (17.33, 4.91) by the head's knee. The taffrail
  above the counter at (−18.73, 4.23). **JUDGEMENT**: the solid side is the rail; the hammock rail
  above it (3.18 to 4.23 m) has no key and is in her note (§13).
- **`decks_m.upper`**: (−16.78, 2.08), (−15.31, 1.91), (−12.87, 1.78), (−10.42, 1.66), (−7.98, 1.54),
  (−5.54, 1.49), (−3.09, 1.44), (−0.65, 1.39), (1.80, 1.39), (4.24, 1.42), (6.68, 1.44), (9.13, 1.44),
  (11.57, 1.54), (14.01, 1.59), (15.97, 1.69).
- **`ports_m.upper`**: eleven triples [x, sill, half-breadth], sills from Dia §2.7: (−13.46, 2.33),
  (−10.69, 2.11), (−7.78, 1.98), (−4.84, 1.87), (−2.11, 1.81), (0.76, 1.78), (3.63, 1.78),
  (6.53, 1.83), (9.30, 1.91), (12.25, 2.04), (16.07, 2.33); the half-breadth at each sill from the
  body plan (task 1; at midships 4.46). **`port_size_m.upper`**: [0.87, 0.66]. The profile is one
  for every fit, so all eleven triples are written: the default fit's guns stand on ports 1 to 10,
  and the 1817 fit's obuses on the bow ports (§5.1). The generator's check (every port gun on its
  triple to the centimetre, Build §5.3) runs for every fit.
- **`keel_m`**: the lower edge, z −3.57, from the post's heel at x −16.59 to the forefoot about
  +15.2; **`rabbet_m`** reserved, z −3.19 over the same run.
- **`stem_m`**: (15.2, −3.57) by the forefoot's curve to (17.20, 0.0) and up to (17.33, 4.91)
  (task 3 traces the curve).
- **`stern_m`**: the post from (−16.59, −3.57) to (−17.20, 0.0) and (−17.71, 3.21), the counter to
  the taffrail (−18.73, 4.23).
- **`head_m`**: the knee's fore edge forward to about x 18.7 at z 2.4 to 3.3 (task 3).
- **`wales_m`**: [x, 0.10, 0.95] at midships, rising to [17.0, 0.95, 1.22] and [−17.0, 0.81, 1.47]
  (task 4 traces both edges along the length).
- **`section_m`**: Dia §2.6's fifteen points, plank on.
- **`form`**: `stern: {type: square, knuckle_z_m, transom_hb_m}` (task 5); `head: knee`;
  `fullness` from the traced sections.
- **`marks`**: every line `sourced` but `form.stern.lights_m` (`judged`).

### 3.3 The hawse holes, the chains, the sweep ports

The hawse holes (16.70, 2.35) and (16.90, 2.35), the chains' deadeyes at the rail, and the small
square openings between the ports (Dia §2.7) have no key in the profile. They go into her note;
the small openings are read as sweep ports (JUDGEMENT), and **no sweeps fit is proposed**: no source
says she rowed.

### 3.4 Why every hull line is `sourced`

The plan is hers, drawn by the navy that held her, with her name, her guns and her captain on it;
nothing is scaled from another hull. The only judgement in the shape is the load line's meaning,
and the displacement check stands beside it (§3.6 task 2).

### 3.5 What the drawing must show her to be

A small flush-decked ship of one tier: a long straight sheer rising gently to both ends with no
step for a quarterdeck or forecastle, a bulwark pierced for eleven guns a side with the hammock
nettings above it, the wale close above the water, a square stern on a raked post, a knee of the
head with two rails and no figure, and a sharp rising floor under the water (kept as data). She is
to be told at a glance from the frigate (taller, stepped, longer) and from the brig-sloop (two
masts).

### 3.6 The builder's measuring tasks (step 1)

1. **The half-breadths by station** at the line and at the rail (`breadth_m`), and at each port's
   sill (the triples), on the half-breadth and body plans; each station labelled as the plan
   labels it (aft 11 to 1, m, m, m, fore 1 to 11, every 4.49 pies).
2. **The drawn displacement**: the sections integrated to the arrowed line, against the table's 497 t
   (Research-74 §3.5's method); and the profile's area under the line, against 104.4 m². If the
   drawn volume misses the table by more than 5%, the load line is put to the lead before anything
   else is filed.
3. **The stem's fore edge, the forefoot and the head's knee** traced point by point.
4. **The wales' two edges** traced the whole length.
5. **The transom**: its breadth at the taffrail and at the knuckle from the body plan's aftermost
   section; the counter's knuckle on the sheer.
6. **Steel 1794 vol. I, the "20 Guns" column of the masts and yards** (pp. 49-50), read on the page
   image, beside §4.1's Luce figures.
7. **A larger image of the plan**, if the Biblioteca Virtual de Defensa's viewer serves one, to read
   the small lettering and the hourglass fitting at x +7.05.

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

| Spar | Place (x at the deck), rake | Length or height, by the chain | Check |
|---|---|---|---|
| Fore mast | +12.47, plumb | 0.9 × 71.3 = 64.2 ft (19.6 m) heel to head | Babron's Spanish corvette 1.1° |
| Main mast | −2.31, 5° aft | 71.3 ft (21.7 m) | Babron 6.2° (corvette), 4.4° (frigate) |
| Mizen mast | −11.40, 5½° aft | 13/15 of the main above the deck | Chapman's mizen at 0.181 L |
| Topmasts, topgallant and royal masts | — | 0.6, then halves, then two-thirds | the frigate's chain |
| Main yard | — | 10/11 × 71.3 = 64.8 ft (**19.76 m**) | Falconer 19.87 m; Chapman 17.97 m |
| Main topsail, topgallant, royal yards | — | 14.82, 9.53, 6.35 m | Chapman's topsail 14.20 m |
| Fore yards | — | 0.9 of the main's (fore yard 17.8 m) | |
| Crossjack and mizen yards | — | 5/7 of the main's (crossjack 14.1 m) | |
| Bowsprit | stem head, steeved about 21° (A) | 5/8 × 71.3 = 44.6 ft (13.6 m), a third inboard | Babron 17.3° to 30.2°; Chapman 29.7° |
| Driver boom, gaff | — | 35.6 ft (10.9 m), 28.5 ft (8.7 m) | |

Her masthead stands about **29 m** above the water (observed on the scratch file: 29.1 m; the
frigate's 35.9), which sets her horizon (`world.ships.rig_height_m`). **Brace limits**: the
frigate's, level for level (no source for hers).

### 4.2 Sails

The frigate's set at 0.8132 in length and 0.661 in area: **plain sail 1,047 m²** (the frigate's
1,584; observed). Courses, topsails, topgallants and royals on fore and main; topsail, topgallant
and royal on the mizen; the driver on its gaff and boom; the fore topmast staysail, jib and flying
jib; the main and mizen staysails; the studding sails and save-alls; the storm canvas. Reef bands,
canvas numbers and cloth ratings as the frigate's (the ratings at the area's scale). The 1809
drawing (eye) shows every one of these but the studding sails.

### 4.3 The handling (Dia §3.3)

No lateen: B3.1 does not reach her. Her mizen carries its crossjack, so B3.4's rule classes all
three masts square (observed); neither classing limit touches her. She heaves to with the main
topsail aback, as the frigate does (observed, §9).

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

| Posts (10) | captain, first lieutenant, second lieutenant, master, boatswain, gunner, carpenter, purser, surgeon, sailmaker |
|---|---|
| Stations (157) | forecastle 17, fore top 15, main top 19, mizzen top 9, afterguard 31, waisters 22, marines 25, idlers 19 |
| Ratings | the frigate's shares (0.3 able, 0.4 ordinary, 0.3 landsmen) |
| Idlers by trade | the frigate's shares scaled to 19 |

- **Marines**: Spain's soldiers embarked, the nation's kit (`data/nations.yaml`, Spain `marines:
  {kit: basic}`); 25 by the frigate's share (JUDGEMENT). The Danes carried a petty officer and ten
  soldiers (Roos p. 94): in the note.
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
or nine, as package 116's road for a small company has it).

### 6.3 The people file and her name

`data/people/corvette-20.yaml`: her posts' people. **Their names**: Spain's row in
`data/nations.yaml` reads `names: english` today, so a Spanish ship's people would be named in
English. A Spanish list of names is new data, the package's to add once for the xebec and the
three-decker as well; the owner's (§17.1 question 6). Her captain of 1809-1810 was Teniente de Navío
José de Julián (the plan) and of 1807 Captain-lieutenant C. N. Meyer (Roos); a scenario may name
them, her file names none.

### 6.4 Package 116

Her company meets package 116's evolutions: `rig the relieving tackles` wants six of the afterguard
and waisters (she has 31 and 22), `repair the wheel` four able hands of the idlers and afterguard.
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
(read at step 1 with §3.6 task 6).

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
half-breadths less: task 1). Under L2 and L3 and the 60-second hold (package 75) her ports shut by
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
- **The masts at her rakes**: the main's 5° and the mizen's 5½° show (1.7 m of lean at a 20-m head);
  the bowsprit at 21°.
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
| A | **Her particulars hold their sources**: 124 × 32½ × 16 pies are 34.55 × 9.06 × 4.46 m; 540 t 691 lb is 497.2 t; she floats at 3.57 m; eleven ports a side at the plan's sills within 1 cm; each fit's guns by date | equalities on the file | — |
| B | **Meyer's speed**: with the wind 112° to 124° off in 24 to 27 knots, under the sail her book carries in that wind, she makes 9.5 to 11.5 knots | sailed, settled | 10.66 kn at 118° in 25 kn under plain sail (GM 1.5); to be re-measured under her book's reduced sail |
| C | **She is stiff**: close-hauled and abeam under plain sail in 22 knots she heels no more than 1.15 times the frigate does, and her midship lee port stays open | sailed, both ships | 8.2° against 7.3° close-hauled, 12.9° against 11.3° abeam (1.12, 1.14) at GM 1.5 |
| D | **She steers well**: close-hauled in 15 knots 0.5° to 3° of weather helm, abeam 1° to 3° | sailed | +1.8° (heel 3.8°) and +2.0° (heel 6.1°) at GM 1.5; the frigate +1.3° and +2.0° |
| E | **She goes about as a ship should**: tacks from the three headings in 285 to 600 s and wears in 360 to 720 s (truths 10 and 11's bands) | the truths' helpers | 349, 369 and 164 s; wears 491 s: **fails from 295°** |
| F | **Her lee port**: the midship lee port shuts at 21.8° ± 0.5° of heel | L2's rule on her triple | — |

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
   the book's "as captured" (Dia §11). *What you would see:* in an 1807 scenario off Cartagena she shows a
   long gun at each end of her battery on either side and carronades between; in 1809 and after, as
   Winfield has her.
2. **How a Spanish or Danish gun's pounds are written.** A Spanish "30-pounder" fires 30 Spanish
   pounds (about 30½ English); a Danish one about 33 English. *Pick:* write the gun as its own navy
   named it (a 30-pounder), with the English weight in its note; the game's range and weight of
   broadside then read it a little light (by 1.5% for Spain). The other way writes the English
   weight (30.4, 33) and the words say "30-pounder" from a separate word key. *What you would see:*
   "the 30-pounder carronades" in her log and on her deck, as her people said it.
3. **Her stiffness.** Her captain called her stiff. With the frigate's proportion she would heel half
   again as much as the frigate and lay her lee ports under in a strong breeze. *Pick:* make her as
   stiff as the frigate (GM 1.5 m). *What you would see:* on a reach in a strong breeze she leans as
   the frigate does, a little more, and her carronades on the lee side keep firing.
4. **Her masts and yards.** None survive. *Pick:* the rule the game already uses for its frigate,
   applied to her size (her main yard about 19.8 m), with Chapman's Scandinavian rule (about 18 m)
   and Steel's British table as checks. *What you would see:* a lofty small ship, her royals about
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
