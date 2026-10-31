# Research note: the engine and the viewer for the three ships (October 2026)

Phase 1 of the ships workflow (`Plan-ShipsWorkflow.md` §2), the engine's part: how the
generator would build HMS *Indefatigable* (the 64 of 1784 and the razee of 1795), the
*Prince de Neufchatel* and the coasting bilander; how the razee can be derived from the 64
in code; what the *Neufchatel*'s rig does in the engine; what the settee needs beyond the
lug; and how the viewer draws, with the four current ships as the standard. It is written
from R4's findings, the checker's re-reading of every cited line, the critic's four gaps
and the gap round's trials, all of 2026-10-25. Where the researcher and the checker
differ, the checker's figure is given. The owner's decisions in the plan's §0 are binding
here; the points they leave open are in §9.

Nothing in the research worktree was changed by this research but this note. No test suite
was run.

## 0. Marks, trials and sources

**Access.** Each fact carries one mark, as the checker found it:

- **read**: the code at the line cited, or the page (an OCR text says so);
- **observed**: seen in a run: the game in the built-in browser, or the engine driven by a
  scratch script from the worktree root, as stated;
- **measured**: timed on this machine (§2.7), or measured off an image (the image and
  scale given);
- **catalogue**, **snippet**, **secondary**, **memory**: as they say;
- **judgement**: reasoning, R4's or the lead's.

**The trials.** The gap round built rig variants in memory from the committed ship files
and drove them through the evolution runner, `polar_of` and the Node projection, from the
worktree root with `py`. The scripts and their outputs are kept outside the repository,
in the owner's notes (`owner-notes/engine/measurements/engine/`: `variants.py`, `rigs.py`,
`sprit.py`, `crewtime*.py`, `crewpace*.py`, `out/`), with the checker's re-runs beside them
(`owner-notes/engine/measurements/check_engine/`). Seed 7, heading 292.5°, no gusts,
unless stated. Absolute times in a trial move by up to about 60 s with the settling time
before the order (work still in hand is finished first); comparisons within one run hold.

**The period sources cited here** (rows in `docs/references/README.md`, or the owner's):

| Source | Used for | Access |
|---|---|---|
| Winfield, *British Warships in the Age of Sail 1793-1817*, pp. 99, 100, 335-336 (the owner's copy, `owner-notes\winfield\`) | The 64's and the razee's guns and men; the *Neufchatel*'s guns and the caption of Reed's model | read |
| The owner's notes (Vanguard kit), `owner-notes\indefatigable\vanguard-notes.md` | The razee's masts and poop | read; the kit's text, probably from Gardiner 2006 (secondary), not confirmed by a public-domain source |
| The research note of 2026-10-25, `owner-notes\indefatigable\research-note-2026-10-25.md` | R1's starting point: draughts, Steel's 64, the gaff mizen | read (its own marks kept) |
| Osler 1835, *Life of Exmouth*, pp. 107-108, 111 (OCR lines 3860, 3987) | The reduced rig "slow and unmanageable"; 19 ft 6 in abaft, May 1795 | read (OCR) |
| James 1837, *Naval History*, vol. 1 p. 454 (OCR line 33385); vol. 5 p. 428 (line 21884) | The razee's complement, 310 then 330; the three 64s of 1794 cut down level with the upper deck but for the bulwark abaft the gangway | read (OCR) |
| Adye, *The Bombardier and Pocket Gunner* (the title from memory; 1804 by the images' file names), pp. 72 and 155: page images `owner-notes\indefatigable\rmg\adye1804-p072-carronades-IAleaf95.jpg` and `adye1804-p155-iron-guns-IAleaf178.jpg`, downloaded for R1 | The weights of the 24-pounder long gun and the 42-pounder carronade | read (page images) |
| Cobb 1841, *A Green Hand's First Cruise*, vol. I pp. 38, 41, 79, 91, 108 | The *Neufchatel*'s rig and company (her name is not in Cobb's text: the identification is judgement) | read (OCR, pages by the running heads) |
| Coggeshall 1856, *History of the American Privateers*, p. 241 (OCR line 13090) | "hermaphrodite rigged", 310 tons, 17 guns | read (OCR) |
| Stevens 1915, USNI *Proceedings* vol. 41 (whole no. 155), p. 27 | The *Neufchatel*'s mixed company | read (OCR in the scratchpad, page by the running heads; the Internet Archive identifier not known) |
| Röding 1794, *Allgemeines Wörterbuch der Marine*, vol. I BILANDER (OCR line 62604), vol. II Ruthen-Segel and Lugger-Segel (lines 62861-62890, 63265-63286) | The bilander's yard at about 45°, and her sail lowered and shifted in going about | read (OCR; the column numbers the librarian's) |
| Falconer 1780, Steel 1794, Lescallier 1791 p. 390, Fincham 1843 p. 59 | The settee's gear and working | as summarised in `VesselReferences-2026-10.md` §3.1-3.2 (lines 417-462); not reopened here (R3's) |

Wikipedia and modern books appear only as pointers, marked secondary.

## 1. The generator, the per-ship modules and the tests

### 1.1 How a ship file is made

- **One script.** `tools/gen_ships.py` is 8,242 lines. Its main block (8231-8242) calls
  `frigate`, `schooner`, `schooner(armed=True)`, `cutter`, `brig`, `brig(merchant=True)`,
  `lugger` and `smack`, writing to `sys.argv[1]` or `data/ships`. Read.
- **The Builder** (`class Builder`, 573; the class ends about 1032) holds one doc (ship,
  hull, spars, sails, lines, groups, aliases) and tables of notes. Methods: `spar` 591,
  `sail` 605, `line` 613, `crew` 639, `people` 740, `armament` 760, `quarter_bill` 787,
  `rate_spars` 810, `whole_ship_groups` 875, `descriptions` 892, `dump` 902. Read.
- **`dump()`** adds the whole-ship groups, then runs `rate_spars`, then writes the YAML with
  the notes as comments and each `corners_m` on one line. Read.
- **The rating pass.** `rate_spars` (810-873) loads a deep copy of the doc through the
  engine's `ship_from_dict` (818-823). It re-rates every spar whose rating is a
  `DesignLoad` (415-431) from the static peak-coefficient load (`static_kn`, 434-441) of
  every sail whose spar chain passes through it, at that sail's own height, times
  `SUSTAINED_FRACTION` 0.85 (144), and appends a "Rating:" clause to the note. Read.
- **It changes the Builder in place.** Each `DesignLoad` becomes a plain float in `b.doc`,
  and the clause is added to `b.notes`. A dumped Builder cannot be re-rated; any copy must
  be taken before `dump()`. Read (checker).
- **`DesignLoad` survives `copy.deepcopy`.** It defines `__reduce__` (430-431). A copy kept
  27.1 kN at 40 kn of wind, alone, inside a doc and inside a whole Builder. Observed
  (scratch run of `import gen_ships`, researcher and checker).

### 1.2 Per-ship modules (the plan's structural decision)

The plan puts the new ships in `tools/ships/indefatigable.py`, `neufchatel.py` and
`bilander.py`, imported and called by `gen_ships.py` (§2, Phase 3).

- **The imports allow it.** At module level the script imports only `copy`, `math`, `os`,
  `re`, `sys` and `yaml` (112-118). Every `freesail` import is inside a function (350, 359,
  367, 818, 824, 3487). `REPO_ROOT` is put at `sys.path[0]` (122-125). Neither the
  repository root nor `tools/` has a `ships` module, and there is no `tools/__init__.py`, so
  a package `tools/ships/` with an `__init__.py` imports as `ships` when the script runs as
  `py tools/gen_ships.py`. Read.
- **The double import.** A ship module that does `import gen_ships` while the script runs
  as `__main__` loads the 8,000-line file a second time, as a separate module with its own
  `Builder` and `DesignLoad` classes; the second copy re-reads every wardroom file at
  import (3386-3390, 6791, 7576). Avoid it by importing the ship modules inside the
  `__main__` block after `sys.modules.setdefault("gen_ships", sys.modules["__main__"])`, or
  by passing the helpers to each module's `build(out, g)`. Judgement: standard Python, not
  run with a real package.
- **The wardroom read at import is strict.** `wardroom(stem)` (3365-3390) opens
  `data/people/<stem>.yaml` and raises if it is missing. A ship module that calls it at
  import breaks generation until its people file exists, so the people files belong in
  stage 0 or the call belongs inside `build()`. Read; the consequence judgement.
- **Nothing existing need move.** The existing builders stay where they are; the new
  modules write new files only. Judgement.

### 1.3 What a new module reuses, and what it must not touch

- **`frigate()` is the Amazon's alone** (1469-2453). It takes no particulars:
  - gun deck 143.2 ft, its mast places, `SPANKER_AREA` 167 and `SPANKER_CENTRE` 9.8
    (2466-2467), `FRIGATE_RAKE_DEG` and `FRIGATE_DECK_M` 1.8 (2455-2456);
  - `frigate_crew` (4237), `frigate_armament` (3674), and `FRIGATE_POSTS`/`FRIGATE_DRAWN`
    from `wardroom("frigate-36")` (3386).

  It also calls `b.dump()` itself (2436) and returns nothing. Read.
- **The 64's builder should be a copy of `frigate()` in the new module**, returning `b`
  before `dump`, so that the razee can be cut from it. Making `frigate()` take parameters
  puts `frigate-36.yaml`'s bytes at risk. Judgement.
- **The module-level helpers a 64 would reuse** (read; lines in `gen_ships.py`):

  | Helper | Line | | Helper | Line |
  |---|---|---|---|---|
  | `FRIGATE_CANVAS` | 184 | | `hold_for` | 3306 |
  | `rope_kn` | 410 | | `boat_entries` | 3317 |
  | `static_kn`, `design_kn` | 434, 444 | | `wardroom` | 3365 |
  | `ground_tackle_for` | 494 | | `ration_entries` | 3393 |
  | `stay_sail_cut` | 1063 | | `gun_crew` | 3449 |
  | `staysail_from_cut` | 1101 | | `fit_magazine` | 3476 |
  | `between_the_masts` | 1150 | | `exercise_allowance`, `filling_party` | 3514, 3523 |
  | `square_sail_lines` | 1386 | | `broadside_pair`, `chasers` | 3567, 3588 |
  | `raked_x` | 2459 | | `pivot_gun`, `swivels` | 3607, 3623 |

- **`raked_x` defaults `deck_m` to `FRIGATE_DECK_M`** (2459), so a 64 must pass her own
  deck. Read (checker).

### 1.4 The shared tables

- **What they lack.** `PEAK_COEFF` (135) has no "lateen". `LONG_GUN_CWT` (3435) has no
  24- or 32-pounder; `CARRONADE_CWT` (3436) has no 42-pounder. Read.
- **Adding keys is byte-safe.** Each table is only ever indexed by key: `PEAK_COEFF[cls]`
  at 440, and the gun tables at 3691-4186. No other file uses them. Read (grep).
- **The weights by Adye** (read, the page images):

  | Piece | Length | Weight |
  |---|---|---|
  | 24-pounder long gun | 10 ft 0 in | 52 cwt |
  | | 9 ft 6 in | 49 cwt 2 qr |
  | | 9 ft 0 in | 47 cwt 2 qr |
  | 42-pounder carronade | 4 ft 3½ in | 22 cwt 1 qr |

  Sources: Adye p. 155, "Length and Weight of English Iron Guns"; p. 72, "Carronades.
  Their Weight and Dimensions".

  Which length of 24-pounder the 64's lower deck carried is R1's. The generator's 18- and
  12-pounders (42 and 34 cwt) match Adye's 9 ft 6 in guns of those natures (judgement:
  the pattern to follow). Its 18- and 12-pounder carronades (10 and 6 cwt) are heavier
  than Adye's 9 cwt and 5 cwt 3 qr 10 lb. That is noted only: those entries feed the
  existing files and do not change.

### 1.5 Files beyond the ship file

- **People files.** At run time `people.load_wardroom` looks for
  `data/people/<ship file's stem>.yaml` (`world/people.py:239-244`, `_attach_wardroom`
  524-545). With none, no outlines or station holders are bound. Read.
  - The privateer schooner reuses the schooner's posts only in the generator. There is no
    `data/people/privateer-schooner.yaml`, so she sails with no runtime wardroom.
  - Each new file that should have outlines and stations needs a people file of its own
    stem: four in all (the 64 and the razee as two).
  - A wardroom's outline can fix a nationality. The topsail schooner's master is out of
    Baltimore (`data/people/topsail-schooner.yaml:25`).
  - A scenario's `people:` can rename a post-holder by role (`people.py:548-571`).
- **Registries keyed on a ship's description or rig words.** None is written by the
  generator. Read (checker's list):

  | Registry | Where | What it means for a new ship |
  |---|---|---|
  | `DESCRIPTIONS`, `_DESCRIPTION_WORDS` | `world/ships.py:163, 205` | An entry and its words per description. "a ship" already maps to the frigate |
  | `SHADOW_FILES` | `world/ships.py:283` (used at 1463) | A player's file with no entry is seen by others as "a ship" |
  | `SIZE_RANK`, `_SIZE_WORDS` | `world/captains.py:286, 296` | The frigate is the top rank, 3; "a ship" is 3 |
  | `MAN_OF_WAR_WORDS` | `world/captains.py:190-198` | Includes "frigate" and "ship of the line" |
  | `_MAN_OF_WAR_DESCRIPTIONS` | `world/regimes.py:158`; `world/squadrons.py:1520`, and the tuple at `squadrons.py:467` | {frigate, brig-sloop}: a 64 or razee description must be added, or she is not treated as a King's ship |
  | `role_for` | `world/brains.py:169-176` | "frigate" gives kings-ship, "brig-sloop" cruiser |
  | `_RIG_WORDS` | `world/lookout.py:300` | |
  | `_SAIL_WORDS` | `orders/signals.py:166-187`; `orders/stations.py:836`; the word list in `orders/navigation.py:872` | |
  | The header `rig` | `api/queries.py:391`, shown by `client/app.js:125` | Display only |

- **The caches.** `file_descriptions`, `rig_height_m` and `polar_of` are each
  `lru_cache(maxsize=8)` (`world/ships.py:266, 297, 423`), keyed by the path string. There
  are eight ship files today and will be twelve. A world using more than eight distinct
  files recomputes polars, and the same file under two spellings takes two slots. A cost,
  not a fault; not measured. Read.

### 1.6 The tests that regenerate or read every file

- **One test regenerates.** `tests/test_ship_particulars.py:555-582`,
  `test_generator_reproduces_the_committed_files`, runs `tools/gen_ships.py` in a
  subprocess (cwd the repository root, `check=True`, output to `tmp_path`). It compares
  the eight files named at 29-39 as UTF-8 text. Read.
  - A new file is compared only once added to that tuple.
  - Extra files do not break the test, but a new module that raises does.
  - The other mentions of the generator in `tests/` are docstrings or assertions on its
    output.
- **One test reads every file.** `tests/test_stores.py:28` globs `data/ships/*.yaml`.
  Lines 64-67 then require `crew.ration == {table: navy, water_gallons: 1}` in every file,
  the privateer's and the bilander's included. Read.
- **The harbour lists ship files by glob** (`freesail/ui/harbour.py:82, 382`), so new files
  appear there without a registry. Read.

## 2. The razee derived from the 64

### 2.1 Two files, each with fits by year

An armament fit carries only `source`, `guns` and the magazine keys (`Builder.armament`
760-785; `FIT_KEYS`, `freesail/ship/schema.py:214`). The 64 and the razee differ in hull,
rig and crew, so they must be two ship files, each with its armament by year as fits.
Each gun carries its own `height_m`, so the razee's 24-pounders need their own heights as
well. Judgement, on the code read.

### 2.2 Her decks, and which deck the file names

- **The 64** (Winfield p. 99, read). She carried 24-pounders on the lower deck,
  18-pounders on the upper, 9-pounders on the quarterdeck and forecastle, and from 1794
  24-pounder carronades on the forecastle and 18-pounder carronades on the roundhouse.
  Her company was 500, 491 from 1794.
- **The razee** (Winfield p. 99, read). She kept the 64's lower-deck 24-pounders as her
  main battery. Her quarterdeck had 8 × 12-pounders and 4 × 42-pounder carronades, her
  forecastle 4 × 12-pounders and 2 × 42-pounder carronades. Her complement was 310 at
  first and 330 afterwards (James vol. 1 p. 454, read).
- **The cut.** The three 64s of 1794 were cut down level with the upper deck, but for the
  bulwark abaft the gangway (James vol. 5 p. 428, read).
- **The decks that follow.** The razee's main deck is the 64's lower deck, and her
  quarterdeck and forecastle stand at the 64's upper-deck level. Judgement, agreeing with
  the research note §4.1 (the *Magnanime* plans, catalogue).
- **The reference deck is open.** The frigate's `deck_height_m` names her upper (gun)
  deck, 1.8 m (`tools/gen_ships.py:1486`; `data/ships/frigate-36.yaml:34-35`). For the 64
  it may name her upper deck (the uppermost continuous deck, as the frigate's does) or her
  lower deck (the razee's main deck). The choice fixes every spar, corner and gun height,
  and the freeboard the viewer draws (§8, item 2; it bears on §9, question 4).

### 2.3 The pattern: new, and before the dump

- **The existing derivations are flag branches, not edits.** Read (checker).
  - `brig(merchant=True)` builds the *Harpy*'s hull, spars, sails, lines, groups and ground
    tackle. It then branches before `brig_crew` and `brig_armament` (6348-6350), and
    `merchant_brig` (6424-6488) gives the new name, era notes, crew, armament, hold, boats
    and descriptions.
  - `schooner(armed=True)` adds `schooner_armament` inside `schooner()` (3226).
    `privateer_schooner` (3926-3959) changes only the era notes and descriptions.
  - Neither touches the hull or the spars, and nothing is ever removed from a built
    Builder.
- **The razee is therefore a new pattern.** The 64's builder returns `b` undumped. The
  razee is `copy.deepcopy(b)` cut down, and both are then dumped, the 64 last or from her
  own copy. While her spars still carry `DesignLoad` ratings, the razee's ratings follow
  her lowered sails by themselves, a little lower for the wind shear. Her notes must be
  rewritten by hand. Judgement on §1.1.

### 2.4 What the cut-down changes

Conventions, read:
- `height_m` is above the deck at midships for lower masts, yards, gaffs, booms and
  studding-sail booms, and for the outer end of a bowsprit-family spar
  (`client/projection.js:23-24`).
- An upper mast's `height_m` is its own height above the head of the mast below
  (`projection.js:509-523`; `lookout.height_of_eye`, `world/lookout.py:207-224`; `sails._spar_centre_height`,
  1560-1566). In the frigate's file the fore topmast is 10.4 m against the fore mast's
  19.8 m.
- `corners_m` heights are above the deck (`schema.py:414-419`).
- A sail's `centre_height_m` and a gun's `height_m` are above the waterline
  (`docs/TechnicalSpec-M0-M2.md:240`).

Let Δdeck be the height of the 64's upper deck above her lower deck at midships, c the cut
at the lower masts' heels, and δT the rise of the hull as the lighter razee floats higher.
All three are R1's figures. The research note §10 has c measured off ZAZ2371 as the height
of the deck removed; Osler p. 111 gives 19 ft 6 in abaft in May 1795 (read). Taking the
64's file to name her upper deck, the razee's to name her main deck:

| Field | The razee's value against the 64's |
|---|---|
| `deck_height_m` | − Δdeck + δT |
| `draught_m`, `displacement_kg`, `gm_m`, `clr_x_m`, `lateral_area_m2`, `hull_speed_kn` | Her own figures (R1's, and §2.5) |
| Lower masts' `height_m` | + Δdeck − c |
| Topmasts, topgallant and royal masts | Unchanged |
| Yards, gaffs, the driver boom, the studding-sail booms carried aloft | + Δdeck − c |
| The lower studding-sail booms (1.0 m above the deck in the frigate's file), swung from the side | At the new deck as at the old (judgement) |
| Bowsprit and jib-boom (outer end) | + Δdeck, if the bowsprit keeps its place in the hull (the checker). The viewer roots it at the deck (`projection.js:528-533`), so it is drawn from the lower deck |
| `corners_m` of sails hung from the masts | Heights + Δdeck − c; tacks made fast at the deck by their own fixing (judgement) |
| Every sail's `centre_height_m` | − c + δT; `x_m` where the rake moves it |
| Sail areas | The 64's (the same yards) |
| Upper-deck guns | Removed |
| Lower-deck guns' `height_m` | + δT |
| Quarterdeck and forecastle guns | New, at about the 64's upper-deck gun heights + δT (judgement on §2.2) |
| `fit_magazine`, `exercise_allowance`, `filling_party`, the quarter bill | Rerun for the new guns |
| Crew | Complement, stations, ratings, posts, people, stores, boats |
| Text | Descriptions, era notes, every spar and hull note |

On the rig the sources say less than the kit:
- **The kit.** The owner's notes (Vanguard kit) say she was first rigged with a 50's masts
  and abandoned them for want of stability, then took the 64's masts again, cut only at
  the lower masts' heels so that the courses came down in proportion to her lowered sides.
  Read; unconfirmed.
- **Osler.** The razee plan reduced the masts and rigging in proportion to the hulls. All
  three ships proved slow and unmanageable until Pellew was allowed to alter his (Osler
  pp. 107-108, read).
- **The mizen.** By April 1796 she set her mizen on a gaff (the *Virginie* action, Gazette
  13887; James vol. 1 p. 361: the research note §4.4, read by R1). Steel's 64 has a long
  mizen yard and no gaff (Steel 1794 vol. I p. 49, read by R1). A mizen yard would be a
  lateen-type yard, which the engine cannot yet carry or draw (§4.7, §6.3), so the gaff is
  also the buildable choice. Judgement.

### 2.5 What the engine can show of "lighter, stiffer, faster"

The engine keeps no weight inventory. Read:
- **Stability.** The righting moment is `displacement_kg × g × gm_m × sin(heel)`
  (`physics/hull.py:352-367`).
- **Masses.** Surge, sway and yaw masses come from the displacement (224-237).
- **Resistance.** It comes from the wetted area L(1.7T + 0.7B) (`ship/parts.py:1795-1798`)
  and `hull_speed_kn` (`hull.py:245-257`).
- **Windage.** Hull and topside windage are not modelled.
- **The deck height.** It also sets every spar's windage height (`sails.py:1560-1566`) and
  the deck's apparent wind (`hull.py:388`).
- **Guns.** A gun's `weight_cwt` enters only the combat's cycle times and hits
  (`combat/far.py:124-128`, `guns.py:527-528`, `hits.py:241`), never stability.

So the razee's advantage can come only from figures the generator computes:
displacement, GM, draught (through the wetted and lateral areas), the lower sail centres
and the hull speed. The period's own comparison runs the other way at first: slow and
unmanageable before Pellew's alteration (Osler). Judgement.

### 2.6 The gun deck

- **Any calibre works.** `gun_crew(kind, cwt)` gives a long gun 2 + cwt/5 men and a
  carronade 3 + cwt/8 (3449-3455). `ballistics_of` scales point-blank and random range by
  log2 of the calibre (`combat/shot.py:78-93`). The charge goes by share
  (`ship/parts.py:582-585`), and resupply is generic by calibre. Only the two weights of
  §1.4 are missing. Read.
- **Exercise.** `exercise_allowance` (3514-3520) applies the one-deck rule, a fourth of
  the upper-deck guns. Its docstring cites a third for ships of two or three decks, which
  the 64 needs. The note written into each fit comes from the shared
  `MAGAZINE_NOTES["exercise_charges"]` (3532ff), which says "a fourth ... one deck";
  editing it changes every King's file. So the 64 must override `b.armament_notes` after
  `armament()`. Read.
- **Numbering.** `broadside_pair` writes ids `gun.N.side` (3567), and the quarter bill
  keys one crew per number (`gun:N`). The gun keys have no deck field, so the 64's two
  decks must be numbered on from each other, not 1 to 13 twice. Read.
- **Ports.** `lee_port_shut(sill_height_m, heel_deg, half_beam_m)` and `PORT_SHUT_M` (one
  foot) are defined and exported (`combat/shot.py:22, 48-53, 65, 116-120`) but called
  nowhere. So the 64's lee lower-deck ports never shut with heel. Read.
  - Wiring it would change existing combat. From the files' gun heights the ports shut at
    about 21° of heel in the frigate, 25° in the brig, 24° in the cutter and 11° in the
    privateer schooner, the ship it changes most. Read (the checker's arithmetic).
- **The *Neufchatel*'s pivot.** `GUN_PLACES` has "pivot" (`schema.py:200`) and
  `pivot_gun` exists (3607-3620, PROVISIONAL). The privateer's docstring saying the schema
  knows no pivot is stale (3970-3971). Read.

### 2.7 A company of 491 to 500

Every man is mustered and quartered individually (`crew/quarters.py:1-30`). The largest
company so far is the frigate's 264 (`gen_ships.py:4245`). The gap round scaled
`frigate-36` in memory to 491 men, the stations and idlers scaled and the 12 posts kept,
with 40 guns, or 66 (26 extra 24-pounders). Measured on the owner's 32-thread machine:

| Measure | 264 men, 40 guns | 491 men, 40 guns | 491 men, 66 guns |
|---|---|---|---|
| Parse and validate | 1.9 ms | | 3.6 ms |
| `muster()` | 2.7 ms | | 2.9 ms |
| `Quarters.beat()`, the quarter bill | 0.3 ms | 0.8 ms | 1.2 ms |
| Steady sailing, ticks per CPU-second (rounds alternated) | 610-653 (the checker's re-run 593-610) | | 598-604 (566-593) |
| The crew package's own time per 1,000 ticks | 0.07 s | | 0.12 s |
| At quarters, ticks per second | 579 | 569 | 552 |
| Beside a crewed frigate-36, ticks per second (pace.py's form) | 299 (294 at quarters) | | 291 (286) |

- **Where the time goes.** `compute_sail_forces` takes about 80% of a tick
  (`physics/sails.py:335`). `routine._fatigue` is about 0.1 ms a tick at 491. Setting
  plain sail from furled, the crew costs 0.18 s per 1,000 ticks at either size, once the
  first world is discounted.
- **pace.py, crewed.** 289, 185, 83 and 48 ticks/s with 1, 3, 6 and 12 crewed ships.
  `CREWED_CAP` is 3 and the floor 60 ticks/s (`world/crews.py:90-91`). The owner plays at
  60×.
- **The 66-gun bill.** It has 34 gun crews, 338 men at the guns, 82 trimmers and 42 at the
  powder, and puts no marines in the divisions, against 51 at 40 guns (the checker, from
  `crewtime.txt`).
- **The first world timed in a process reads 1.5 to 2 times fast:** 867 to 1,177 ticks/s
  against 572 to 602, whatever the ship. Alternate the measures or discard the first;
  pace.py's first figure may be inflated the same way. The cause was not found.
- **Conditions.** Another workflow's tests ran during the first measures. pace.py was run
  after they finished, with idle processes of the owner's other sessions on the machine.

No part of the crew work scales badly. Measured.

## 3. The *Prince de Neufchatel*'s rig in the engine

### 3.1 What the sources say of the rig

The rig is R2's to settle. What bears on the engine:
- **Hermaphrodite rigged.** Cobb p. 38 (read, OCR): "her foremast was rigged as a brig,
  while her mainmast was rigged as a schooner".
- **A schooner's main.** Her main mast went up high in one piece, with no top, the
  crosstrees being the first landing place. Its topgallant mast was housed in the gale
  (Cobb p. 91, read).
- **A fore-and-aft foresail.** She lay to under the fore-and-aft foresail (p. 79), and
  later under the storm staysail alone (p. 91), read.
- **Coggeshall.** "hermaphrodite rigged" (p. 241, read).
- **Winfield.** He calls her a schooner, and his caption a schooner-brigantine
  (pp. 335-336, read).
- **Reed's model** (the picture in Winfield) seems to show a small square sail at the
  main masthead (plan §1; the picture not measured here).

### 3.2 Every sail she needs exists

Read: the parts of `brig.yaml`, `topsail-schooner.yaml`, `cutter.yaml` and
`frigate-36.yaml`, dumped.

| What she needs | Where the engine already has it |
|---|---|
| A square fore: course, topsail, topgallant, royal | `brig.yaml`, `fore.yard` to `fore.royal.yard` |
| A loose-footed gaff sail on a mast that carries square sails | `topsail-schooner.yaml` `fore.sail`, class gaff on `fore.mast`/`fore.gaff`, no boom, a sheet each side and a tack (`gen_ships.py:2825-2843`) |
| A gaff sail on the same mast as a lower yard | The brig's `main.yard` with `main.spanker`; the frigate's crossjack with its spanker |
| A boomed gaff main with a gaff topsail | The schooner's `main.sail` and `main.gaff_topsail`, jibheaded on `main.topmast` |
| Square sails above a gaff main | The cutter's `topsail.yard` on `main.topmast`, sheeted to `square_sail.yard` |
| Square sails set flying | The royals, `flying: true`, frigate and brig |

No new sail or spar class is needed.

### 3.3 The main yard decides how she is handled

- **What counts.** `_square_rigged` (`physics/sails.py:852-866`) counts the masts that
  carry any braced yard, and caches the answer per ship. The heave-to's `fore_and_after`
  (`scripts.py:2162-2167`, through `_masts_with_yards`, 472-479) counts `working_yards`,
  which leave out yards wrecked or struck. A flying sail stowed does not strike its yard,
  so flying yards count. Read.
- **What follows from two masts with yards.** Read:
  - the helm steers full and by by the highest square sail set (`sails.py:365, 444-449`);
  - the heave-to backs yards (`scripts.py:2187-2196`);
  - `after_gaff_sails` (553-582) makes the main gaff sail a driver to be brailed up;
  - the gale's `_after_sail_lines` (`orders/storm.py:370-411`, 384) adds "take in the
    mainsail" at the third reef.
- **The trials** (the checker read the outputs; not re-run). Variant A is the topsail
  schooner with a fore yard 14.6 m long, 14 m up, braced to 58°, and a 105 m² fore course.
  Variant B is A with a 30 m² main topsail on a yard at the main topmast. At 15 kn of
  wind; SETTLE 2,400 s, because the schooner's 40 men had not set plain sail with the
  course in 1,000 s. Observed:

  | | Topsail schooner | A: fore course, no main yard | B: A with a main topsail |
  |---|---|---|---|
  | How the engine counts her | Fore-and-after | Fore-and-after; head yards fore topsail, topgallant and the fore yard | Square-rigged |
  | Tack | 142 s | 149 s | 219 s, with a "Mainsail haul" swinging the main topsail yard |
  | Wear | 462 s | 449 s | "Up helm; brail up the mainsail" |
  | Heave to | 49° off, 2.65 kn | Courses hauled up, then the fore-and-after's way: 50° off, 2.65 kn (both forereach) | Fore topsail aback, mainsail brailed up: 68° off at 2.74 kn (+150 s), 70° at 1.83 kn (+300 s) |
  | Getting under way | | Under the fore topsail, mainsail and jib; the course not set | |
  | Polar, 70° and 90° | 7.16 and 7.92 kn | 7.09 and 8.13 kn | |

  One small yard on the main switches every handling path. Without it she is a
  fore-and-after carrying a full fore course, a combination no current file has, and it
  works.
- **A main topsail without a main yard.** The schooner's fore topsail already sheets to a
  bare spread yard that is not a part (`gen_ships.py:2584`), and the viewer draws it by
  `bareFoot` (`projection.js:452-466`, 1012-1023). A main topsail could do the same, but
  its own yard is braced, so it still counts as a yard on the main. Read.
- **The choices.** Carry no main square sail; accept the brig's handling; or carry it on a
  spar the classification leaves out. The last needs an engine rule, a stage-0 or B2
  design matter. Judgement; §9 question 5.

### 3.4 Her guns

Winfield gives 16 × 12-pounder carronades and 2 × 6-pounders, the men left blank
(pp. 335-336, read). Both natures are in the generator's tables (3435-3436). Coggeshall
gives 17 guns (p. 241). The rest of her armament by date is R2's.

### 3.5 Her hands' names, and her nation

The owner's ruling is that her file carries no nation (plan §0). Read:
- **The names list fixes the hands.** Every ship file names one list in `crew.names`, any
  non-empty string (`schema.py:512, 1714-1718`). It is checked only at muster, against
  `data/crew/names.yaml` (english, american, french; `crew/muster.py:168-174`).
  `attach_crew` always musters from the file's list (`api/session.py:77`), and a crewed
  vessel's hands also come from its file's list (`world/crews.py:309-346`).
- **The scenario fixes the nation.** `Scenario.nation` (`core/world.py:191-198`) wins in
  `Ports.ship_nation` (`world/ports.py:926-933`), which `signals.own_nation`
  (`world/signals.py:413-418`), the gunnery, the captains, the ordnance and the director
  read.
  - Only when it is None does `nation_of_names` map english, american and french to
    Britain, the United States and France. Any other list maps to Britain
    (`world/nations.py:39, 153-155`).
  - 29 scenario files already set `nation:` (24 in `data/scenarios/`, 5 in `trials/`): 16
    Britain, 12 the United States, 1 France.
  - `Nation.names` (`nations.py:226`) is read only for recruits entered in port
    (`ports.py:3468-3477`).
- **The options** (judgement):
  1. `names: french`, so she is French by default, as the plan's scenario wants, and
     scenarios set `nation:`. Her hands keep French names when she sails as an American.
     Since the schema requires some list, every list implies a default nation, so this is
     no worse than another.
  2. A mixed "privateer" list in `names.yaml`. This is data only, but it defaults to
     Britain unless stage 0 adds it to `NAMES_TO_NATION`.
  3. An opt-in `Scenario.names` hook on the fit's pattern: `Scenario.fit`
     (`core/world.py:244`), read from the scenario's ship section (`scenarios.py:320-321`)
     and set from the vessel (`crews.py:343`). It is stage-0 work, and the 29 scenarios
     do not change.
- **A stale comment.** `data/nations.yaml:61` says `names.yaml` has no french list; it
  has one (`names.yaml:94`). Read.
- **Her company was mixed.** Read:
  - Stevens says the defenders in the boat action were of many nations: Ordronaux a
    Frenchman, the first mate a Swede, several languages before the mast (p. 27).
  - Cobb's captain of December 1814 was a Frenchman by birth (p. 41).
  - Six French and Portuguese seamen from her former cruises messed apart from the
    Americans (Cobb p. 108).

## 4. The settee

The owner's ruling: a real settee main, the four-cornered lateen on a long oblique yard,
built on the lug's yard and dipping machinery, set and clewed up as Lescallier gives it
(plan §0).

### 4.1 What the lug gives

Read:

| Feature | Where |
|---|---|
| Class `lug`, its yard role a `lug_yard` | `schema.py:100` |
| A `lug_yard` has no braces or lifts and is not a braced yard (`is_yard` is True only for `yard` and `lateen_yard`) | `ship/parts.py:238-243` |
| The sheet holds the trim | `evolutions/trim.py:420-463` (`read_sheet`) |
| `dipping` and `lug_side`; only a lug may dip; only a lug may be `sheeted_to` another sail | `parts.py:262-268`; `schema.py:1292-1293, 1303` |
| `corners_m` as [tack, throat, peak, clew] drive the drawing | `schema.py:414-419` |
| The cut in the generator | `lugger()` (6809): the yard slung a third from its fore end and peaked 25° from the horizontal (6877); area and centroid by `_quad_area_centroid` (6794-6806); the corners written at 6979-6980; lug topsails flying and sheeted to the lower lug (7090-7101) |
| The dip | `dip_lug.yaml`: lower (30 s, in the gear), shift the yard abaft the mast (60 s, `lug_side` to the lee side), hoist (60 s); 6 able hands, forecastle and afterguard. `LugDip` (`scripts.py:336-404`) does the same within the tack (1081-1124, `dip_s` default 90 s) and the wear (1525-1545) |
| The penalty | `against_the_mast` (`sails.py:657-664`) cuts the drawing area to 2/3 (`LUG_AGAINST_MAST_AREA`, 127-135), only for a sail with `dipping` lying on the weather side |
| The evolutions | `set_lug` (hoist 75 s, `lug_side` the lee side, sheet \|awa\| − 25° clamped 8-85°; 6 ordinary hands, forecastle and afterguard); `take_in_lug` (lower the yard on deck 30 s, stow 60 s); `trim_lug_sheet` (0.4 s/m², 20-120 s, 6 afterguard); `reef_lug`; `shake_out_lug`; `dip_lug` |
| The words | `data/vocabulary.yaml:1570-1680` maps lug to set, take in, reef, shake out, dip, bend, unbend, shift and trim; "furl" on a lug means take in (`orders/verbs.py:416`) |
| The choice of evolution | By the sail's class, matched exactly (`verbs.py:419-422`; `runner.py:566-602`); `flying` is the only override key |

### 4.2 What is new beyond the lug

From the period, as summarised in `VesselReferences-2026-10.md` §3.2 (lines 445-462), and
Röding read here:

- **The geometry.** The yard hangs obliquely in the fore-and-aft plane. Its after end is
  peaked to about 45° and hangs over the stern, and its fore end comes about as far
  forward as the middle of the ship. The tack goes to a ringbolt amidships, the sheet to
  the taffrail (Falconer 1780). Röding gives the yard at about 45° to the mast, its upper
  end over the stern and its lower about amidships above the deck (vol. I, BILANDER, read
  in the OCR). Against the lugger's 25° peak (`gen_ships.py:6877`) this is a far steeper
  yard.
  - On the brig's hull the main mast stands at x −3.9 m (`brig.yaml:119`). A yard whose
    fore end is near midships is then slung about a fifth along it, not a third.
    Judgement, for R3 to measure off Gwyn's drawing.
- **The gear** (Lescallier p. 390): a parrel, a halyard, a lift, two vangs and a brace.
  The sail tacks to the weather side, sheets to the taffrail, and is clewed up by
  buntlines and clewlines like a square sail. In the engine:
  - The lift, vang and brace classes exist (`schema.py:119-160`). A `lug_yard` accepts two
    vangs, and a scratch file with them loads. Observed.
  - Nothing reads a vang on a lug yard. "vang" appears in `scripts.py` only in the
    reeving tables (4961, 4972) and in `verbs.py:1561` for gaff and boom. Read.
  - A brace on a lug yard would take 0.3 of the sail's force (`BRACE_LOAD_FRACTION`,
    `sails.py:117`; 1507-1508), and the schema allows it (1509). No order works it. Read.
- **Clewed up aloft.** `take_in_lug` lowers the yard to the deck. A settee needs a take-in
  that clews up with the yard aloft, and a furl aloft. The square sail's evolutions are
  the pattern: `take_in_square` clews up (60 s, in the gear) and hauls up (45 s), 10
  hands; `furl_square` lays aloft and furls (150 s), 12 hands. Both are
  `applies_to: {class: square}`. Read; the use of them judgement.
- **The sheet.** The loose-footed sheet geometry assumes a foot of 0.8√A and a block one
  fathom abaft the clew (`trim.py:274-279, 371-396`). It knows no lead to the taffrail.
  Read.
- **Shifted or standing.** The sources disagree; R3's to settle, the owner's to rule:
  - Steel says the bilander's yard hangs to the main mast as a ship's does to the mizen
    mast (`VesselReferences` §3.2, OCR), which points to a yard that is not shifted.
  - Röding puts the bilander's great sail with the lug, whose sheet cannot serve as a
    tack, "so muss es beym Wenden erst gestrichen und durchgekaiet werden" (vol. II,
    Lugger-Segel, OCR lines 63274-63286, read). That is, it must first be lowered and
    passed round in going about.
  - Röding's lateen mizen entry (vol. II, Ruthen-Segel, lines 62877-62890, read) gives
    the reason ships went over to the half mizen ending at the mast: a lateen reaching
    before the mast had to be passed round at every tack.
  - Lescallier's shift of the lateen ("muder", pp. 377-380) brings the yard upright and
    passes it round, unlike the lug's lowering dip (`VesselReferences` §3.1).
- **The penalty.** A settee that is not shifted would want the against-the-mast penalty
  on one tack. Today `against_the_mast` returns False for any sail without `dipping`
  (`sails.py:657-664`). Read; the need judgement.

### 4.3 The physics of an oblique yard

Read:
- **The slope is never read.** A fore-and-aft sail's force is its class curve at a chord
  equal to the sheet angle, times area and q (`sails.py:575-617, 1047-1056`). Its moments
  use `x_m` and `centre_height_m` (426-429).
- **Unboomed sails.** With no boom or gaff, the lateral offset is 0.5 × 0.8√A ×
  sin(sheet) (1320-1351) and the blanketing height 1.2√A (1354-1360).
- **The yard's windage** acts at the mast's x and the yard's sling height (1552-1576).
- **The sheet floor.** The lug's is 8°, the gaff's 18° (`trim.py:256-269`).

So the oblique yard reaches the physics only through the area and the centroid the
generator computes from the corners. A high peak aft raises the heeling moment and moves
the centre of effort aft, as it should. The lateen's greater liability to be taken aback
(Fincham p. 59, `VesselReferences` §3.1) can come only from the class curve. The lateen
curve in `data/sail_classes.yaml:93-104` (lift 0.8, 1.1, 1.15, peak at 35°, luff angle
18°, furled windage 0.08) sits a little below the lug's (0.85, 1.15, 1.2), and was never
tuned (`docs/dev/TuningNotes.md:127` calls the lug, lateen and sprit curves untested
rigs).

### 4.4 The trials: a scratch bilander

**The variant.** `brig.yaml`, with `main.course`, `main.spanker`, `main.gaff`, `main.boom`
and the storm trysail removed. In their place:
- a lug-class `main.settee` on a `main.lug_yard` on the main mast, its corners
  [[-0.6, 0.3], [-1.4, 5.5], [-21.0, 19.5], [-14.5, 0.6]], 175.7 m² by those corners;
- two vangs on the yard;
- the bare main yard kept as a dry yard, with the main topsail, topgallant and royal.

The brig's main course and spanker together are 94 + 162 = 256 m². The settee's size and
corners are the researcher's judgement, not Gwyn's.

**Two faults in the variant itself.**
- Its `centre_height_m` (7.2 m) is the corners' centroid above the **deck**. The engine
  reads it above the **water**, as the lugger's file does (each lug's centroid plus the
  1.0 m deck). Her centre of effort is therefore 1.5 m too low, a small effect on the
  polar and the heel. Read (checker).
- The peak at x −21.0 m lies far abaft the taffrail of a hull whose stern is at −13.4 m.

Neither alters the mechanisms below.

**Classification**, observed, the same whether the settee dips or not:
- She counts as square-rigged. The masts with yards are the fore and the main (the dry
  main yard counts; the `lug_yard` never does).
- The head yards are the four fore yards; the after yards are the dry main yard and the
  main topsail, topgallant and royal yards.
- `yards_to_back` (`scripts.py:504-524`) returns the **fore** yards. It picks the mast with
  the most square area, and with the main course gone the fore has more.

Results, observed. The checker's corrections are applied; at 15 kn and 20 kn of wind:

| Evolution | Dipping settee | Standing settee | The brig (*Harpy*) |
|---|---|---|---|
| Tack, 20 kn | At helm's a-lee "lower the mainsail"; through the wind "Dip the mainsail; shift the tacks to the weather bow"; the dip took 130 s. Tacked in 207 s (re-runs: 249 s at SETTLE 1,000, 200 s at 2,400); 6.5 kn afterwards | "haul aft the mainsail sheet" at helm's a-lee (taken as a boom sail); 184 s; full speed after | "Tacked" at 466 s, on the timeout (below) |
| Tack, 15 kn | Dip 116 s; tacked in 232 s; 5.0 kn after | 293 s | 454 s, also on the timeout, nearly without way |
| Wear, 20 kn | "Lowered the mainsail to dip them"; hoisted on the new lee 123 s later; 529 s; 6.5 kn after | 528 s | 570 s |
| Wear, 15 kn | Dip 112 s; 492 s; 5.0 kn after | 539 s | 474 s |
| Heave to | Settee lowered (in the gear, `scripts.py:2241-2249`), fore course hauled up, fore topsail aback. 70° off at 1.96 kn (15 kn) and 71° at 2.39 kn (20 kn) at +150 s; 79° and 87° off at +300 s, still falling off | The settee stays set, sheet eased to 36°: forereaching at 2.7-3.6 kn, 64° off | Main topsail aback: 63-64° off at 1.36-1.78 kn |
| Getting under way, 10 kn, from the outer road | The lugger's path (below): **fails** at 1,842 s, "she hangs two points and a half from the wind and will not cast" | Under way in 1,342-1,343 s under topsails and jib; the settee never set; the log says "set the spanker" | 1,342-1,343 s |
| Polar at 15 kn: 60°, 70°, 90°, 100° | 4.07, 5.64, 7.44, 7.47 kn; closest 50° | | 4.26, 5.88, 7.83, 7.92 kn; closest 50° |

- **The dip works on a square-rigged ship.** `LugDip` runs unchanged, and the tack cannot
  finish while the lug is down (`scripts.py:1218-1229`, `_lugs_down`). The log's plural
  words ("shift the tacks", "to leeward of the masts", "dip them") are the lugger's and
  read oddly for one sail (1535-1538). Observed.
- **The brig's tack is called before she is round.** This is existing behaviour, but the
  bilander's hull is a brig's. Observed (the checker's trace, `check_engine\brig_tack.py`):
  - She is through the wind by about +120 s.
  - Sternway then carries her head back onto the old tack: at +241 s she was 34° off on
    the starboard tack, 2.8 kn astern.
  - Once `through` is set nothing checks again for a miss; the checks live only under
    `if not self.through` (`scripts.py:1129`).
  - The steady phase ends on `steady_timeout_s`, 300 s (`tack.yaml:50`;
    `scripts.py:1218-1226`), and logs "Tacked". At that tick she lay 148° off on the
    starboard tack with 0.77 kn sternway.
  - The event therefore cannot be taken as proof that she came round. A settee truth
    pinned on it would pin the fault.
- **Getting under way takes the lugger's path.** `self.lugger = bool(_lugs_all(ship))`
  (`scripts.py:6925-6927`) makes her fore-and-aft. Read; observed in the trial.
  - The lugger's `_begin_loose` loosens nothing aloft (6963-6974), so her topsails are
    never loosed.
  - "Man the fore lug halliard" is hard-coded (7086-7089).
  - The lugger hoists `_lugs_all[:1]` (7116-7118) and fails at the cast timeout
    (7210-7222).
  - `after_gaff_sails_all` takes gaff sails only (7354-7365), so a standing settee is
    never set after the cast, while 7265 still says "set the spanker".
  - A guard such as "the lugger's path only when there are no working square yards" is
    feasible. A real lugger's yards are all `lug_yard`s, so `working_yards` is empty for
    her. Judgement (checker).
- **Hove to, neither settee stops her.** A standing settee is a boom sail
  (`boom_sails`, `scripts.py:217-233`) and keeps drawing, so she forereaches. The dipping
  one is lowered, but she backs her fore topsail and falls off. Luce's "main topsail to
  the mast" (cited by the researcher) would need a rule or a file field. Observed.
- **A standing settee is still drawn on a side.** `set_lug` writes a `lug_side` for any
  lug (the hoist step), so the viewer draws it on that side after every tack. Read.

The lugger's tack refused at 1.7 kn in R4's browser session is `tack.yaml:29`, "She has
not way enough on her to stay". It is a precondition, checked before the script begins,
so the dip has nothing to do with it. Read.

### 4.5 Evolutions and crew stations

- **Topmen.** An evolution's topmen are found from the mast id's prefix
  (`evolutions/runner.py:1048-1056`) through `TOP_OF_MAST` {fore, main, mizzen}
  (`crew/hands.py:104-108`). New masts must be named `fore.`, `main.` and `mizzen.`; an
  unlisted prefix (the lugger's `mizen.`) falls back to the other tops. Read.
- **Stations.** The station list is fixed (`schema.py:277-286`). None of the three ships
  needs a new station. Read.
- **The lug's hands are all on deck.** The lug evolutions take 6 hands from the
  forecastle and afterguard (`set_lug.yaml:40`, `take_in_lug.yaml:25`, `dip_lug.yaml:47`,
  `reef_lug.yaml:31`). Read.
- **What a settee needs** (judgement on §4.2):
  - set and dip as the lug's;
  - clew up with the yard aloft, and furl aloft by the main top's men, as `furl_square`
    sends topmen;
  - a trim of its own: the lug's `trim_lug_sheet` serves only class lug;
  - and, if the vangs are to mean anything, an order that works them.
- **The lateen's words lead nowhere.** `vocabulary.yaml:1577, 1586, 1679` map set, take in
  and trim on a lateen to `set_lateen`, `take_in_lateen` and `trim_gaff_sheet`. The first
  two files do not exist, so the runner refuses with "There is no such evolution"
  (`runner.py:311-313`). `trim_gaff_sheet` applies to class gaff only, so the runner
  refuses that too: "The mainsail is a lateen sail; 'trim_gaff_sheet' is for a gaff
  sail." The same holds for sprit. Observed (scratch run).

### 4.6 Lug-keyed code a settee filed as a lug would meet

Read; what each does to the scratch settee where it was tried:

| Path | Where | What it does to a settee |
|---|---|---|
| `boom_sails` | `scripts.py:217-233` | A lug neither dipping nor `sheeted_to` is a boom sail, hauled aft and held over in the tack (observed) |
| `dipping_lugs`, `LugDip` | 327-404 | The dip in tack and wear: works (observed) |
| The heave-to | 2241-2250 | Dipping lugs lowered (observed) |
| Rounding to | 6070-6080 | Not tried |
| `_lugs_all`, `_standing_lugs_all`, getting under way "as a lugger" | 6800-6837, 6925-7230 | Takes the lugger's path whenever any lug exists; fails (observed) |
| Navigation's watch on the stern | `orders/navigation.py:778-835` | Reports a dipping lug left against its mast once the wind crosses the stern, with square yards left by the lee: correct for a dipping settee |
| The captains' storm lug | `world/captains.py:2639-2648, 2783-2792` | Taken only if `_lugs_all` and a sail with the id `taille_vent` exist; a bilander without one falls through to lying a-try |
| The gale's after sail | `orders/storm.py:370-411` | Square-rigged ships only, and the driver only through `after_gaff_sails`, which is gaff-only: never takes in a settee. Whether shorten-sail's list reefs it was not checked |
| `FURLED_AS_TAKEN_IN` | `orders/verbs.py:416` | "furl" means take in: wrong for a settee furled aloft |

### 4.7 The three ways to build it

| Way | What it reuses | What it needs | Against it |
|---|---|---|---|
| 1. A lug variant: class lug, a `lug_yard`, `corners_m`, and a new flag routing to new evolutions | The dip, the sheet trim, `lugCut`, the against-the-mast penalty | A new key in `evolution_key` (only `flying` exists); new evolution files with `applies_to` class lug; a guard on every path of §4.6 | Every lugger path must be checked and guarded |
| 2. Finish the dormant `lateen` class | Schema (`schema.py:68-117`, 245: `lateen_yard` in `YARD_LIKE_CLASSES`, 60 kN default), curve, trim figures (`trim.py:260, 267`), vocabulary | Set, take-in and trim evolutions; the yard taken out of the braced yards, or its brace given meaning; dipping allowed for a lateen (`schema.py:1292`); `PEAK_COEFF["lateen"]`; a viewer branch; tuning | The schema refuses dipping on anything but a lug, and `LugDip`, `dipping_lugs`, `against_the_mast` and `_lugs_all` all key on class lug, so it loses the whole dip. Its yard is `is_yard` (`parts.py:238-243`): braced by every brace order, it makes the ship square-rigged by itself. The viewer draws a lateen without its corners, as a rectangle under a braced yard tilted a fixed 0.8 rad (`projection.js:612, 1067-1072`). Least in keeping with the ruling |
| 3. A new `settee` class | Clean isolation | About twelve places: `schema.py:93-117, 1289-1307`, `sail_classes.yaml`, `trim.py:256-269`, `parts.py:360-362`, `PEAK_COEFF`, the vocabulary, evolution files, the viewer's `SAIL_CLASS_RANK` (`projection.js:66`) and a drawing branch, `against_the_mast` | The most code, and the dip is reused only by generalising it |

The choice also decides her classification. With a `lateen_yard` the bilander is
square-rigged on two masts whatever else she carries. With a `lug_yard` her main counts
nothing, and she is a fore-and-after unless the main carries another yard (in the
trial's bilander it does: the dry main yard). Read; observed.

## 5. A yard on the bowsprit

Steel's 64 has a spritsail yard and a sprit-topsail yard (Steel 1794 vol. I p. 49, read by
R1). Lescallier's *bélandre* (Pl. XXII, R3's) has a spritsail yard, and the *Neufchatel*
had a yard for a square sail under her bowsprit (R2's). No ship file carries one.

| Point | Finding | Access |
|---|---|---|
| The schema | A yard `on: bowsprit` validates: the checks are only that a parent exists and that root spars are a mast or a bowsprit (`schema.py:1409-1446`) | observed (scratch load) |
| Classification | `mast_of` returns "the lower mast (or bowsprit)" (`ship/graph.py:174-181`), so `_masts_with_yards` counts the bowsprit. On the brig the head yards become the spritsail yard alone and the after yards all eight fore and main yards, so "Mainsail haul" swings the fore yards too. On the topsail schooner it flips her to square-rigged: she heaves to the square-rigger's way ("Braced the fore topsail aback; hauled aft the head sheets") at 64° off and 4.07 kn, against her own 49° and 2.65 kn, and her tack gains a "Mainsail haul" | observed (researcher and checker) |
| Force and handling | Computed as any square sail's, loaded through the yard to the bowsprit; braced to its 45° limit by the trim and by "brace sharp up"; `_yard_level` 0, a course (`sails.py:869-881`); left out of `lowest_square_sails` (`scripts.py:618-626`), so it stays set and braced when hove to; at 60° of wind, braced to 45°, its thrust was negative (−0.12 kN); "set the spritsail" works, the log saying only eight hands could be spared; no top for the bowsprit in `TOP_OF_MAST` | observed |
| The viewer | The yard stands at the bowsprit's own `x_m` (its heel, at the stem: 13.4 m on the brig, half her length), at deck + `height_m`, athwartships (`projection.js:528-533, 575-617`). A square sail with no yard below hangs area/(0.9 L) deep (1024-1028): the scratch spritsail (yard 1.0 m up, 45 m²) hangs at the stem with its foot 2.0 m below the water | observed (scratch raster) |
| What it needs | Bowsprit-rooted yards left out of `_masts_with_yards` and `_square_rigged` and put with the head yards; their own heave-to and trim rules; in the viewer, a station along the bowsprit (a file field or a rule) and a spritsail cut | judgement |

Leaving the spritsail out costs nothing in the engine (§9, question 7).

## 6. The viewer

### 6.1 How it draws

`client/projection.js` (1,598 lines, no DOM) builds a three-dimensional skeleton and
projects it orthographically for a facing, by default abeam to leeward
(`client/app.js:46, 74`), with the heel. Read.
- **Its inputs.** The skeleton comes from `/api/ship` (`queries.ship_graph`,
  `api/queries.py:316-406`) and the snapshot: brace and sheet angles, states, `lug_side`.
- **The rendering.** `client/shipview.js` (94 lines) renders the SVG, a flat sky and sea
  rectangle, the figures and a caption (36-92). Its viewBox fits `scene.bounds`, so size
  does not matter.
- **What the graph serves:**
  - the hull: LWL, beam, draught, deck height, displacement, GM, CLR;
  - each spar: class, x, height, length, parent, side, brace, rake;
  - each sail: class, roles, area, x, centre, reefs, sheet angle, dipping, flying,
    `sheeted_to`, `corners_m`;
  - the lines.

  No armament, deck or port data is served.

| Element | How it is drawn (read) |
|---|---|
| Hull | One generic lens for every ship (`hullFigures`, 1416-1448). The half-breadth is B/2·(1 − \|t\|^2.2)^0.55, the transom 0.28 B, the stern at −0.52 L and the bow at +0.56 L. The sheer is F(1 + 0.12t² + 0.1t), the sides run down to −0.8 m. Only LWL, beam and `deck_height_m` vary. No ports, wales, head, galleries, furniture, boats or guns. Colours: hull #4a3d31, deck #b9a37e |
| Masts | Lower masts raked by `rake`; upper masts continue their line with a 12% doubling (`DOUBLING`, 51) |
| Square yards | Slung 0.05 B before the mast. A hoisting yard sits on the cap while its sail is not set, halfway while its halyards are worked, and drops with each reef. Struck topmasts are drawn housed; royals sent down lie fore and aft on deck |
| Lug yards | From the corners (541-557) |
| Gaffs and booms | A gaff at a fixed 35° whatever the file says (`GAFF_PEAK_ANGLE`, 44); booms swing by the sheet angle |
| Square sails | `squareCut` (990-1029): the head along the yard as it stands, the clews at 0.9 of the yard below (`yardBelowId`, 432-446); with no yard below, 0.9 of its own yard wide and area/width deep; `bareFoot` over an absent yard (452-466) |
| Lugs | `lugCut` (365-393, 1050-1063): `corners_m` swung about the slings, a third along throat→peak, by the sheet angle, on `lug_side`; lowered, along the deck |
| Staysails between the masts | `corners_m` (1125-1136) |
| Jibs | Along the stay, the luff 0.7 of it (`JIB_LUFF_FRACTION`, 46) |
| Gaff sails | Throat, peak, boom; a loose-footed clew placed from the area, the foot fixed 1.5 m above the deck (`LOOSE_FOOT_HEIGHT_M`, 45; 1087-1117) |
| Others | The gaff topsail a triangle up the topmast; studding sails, ringtail and water sail |
| Every sail | Bellies 12% to leeward with a 6% foot sag (48-49); drawn by state: bundle, festoons, torn, drooping, or the backed colour. At a depth tie the class rank orders them (`SAIL_CLASS_RANK`, 66) |
| Lines | Braces, sheets and hauled bowlines only (1292-1344), at opacity 0.28, brightened while their evolution runs. A brace is drawn on any yard with an arm, a `lug_yard` included. Stays are computed to place the head sails (758-790) but never drawn; no shrouds, ratlines, backstays, halyards, vangs, tacks or lifts |
| Colours | Sky #dfe7ea, sea #5f7d8c with the sea line #3f5d6b, canvas #ece5d3 (#cfc7b3 furled, #e4dccb loose or sheeted, #b7ab95 aback), spars #3b3128, rope #5a5147 (#c2782e busy) (`client/style.css:13-31, 149-187`) |
| Motion | None. No animation or wave texture; the picture changes only with each snapshot |

### 6.2 The standard: the four current ships in the browser

R4's views in the built-in browser, 2026-10-25, through `freesail.ui.server` on
`http://localhost:8765`, wind north 15 kn, judged at 800 × 600. Observed by R4. The
checker did not repeat them, and found the code supports each point.

| Ship | What the view showed |
|---|---|
| `frigate-36` (*Amazon*), heading 293 | **Furled:** staysails and jibs as grey bundles along their stays, the square sails as small blobs on the yards seen end-on, the royal yards on deck, the braces faint. **After "make sail" and "trim sails", close-hauled, from the larboard beam:** three raked masts; courses, topsails and topgallants bellied; fore topmast staysail and jib; the spanker on gaff and boom; the mizzen topgallant, only sheeted, in a darker fill. **From ahead and the starboard quarter:** braced yards and bellied sails, the transom face. **After "square the yards", from the beam:** the square sails as thin edge-on slivers |
| `brig` (*Harpy*), heading 295 | **Close-hauled after "trim sails",** heeled 5° to larboard, seen to leeward: the tan deck on the slab-sided hull; course, topsail and topgallant on each mast, the royals sent down; the main spanker; jib and fore topmast staysail; the staysails between the masts furled as diagonal bundles. **From 34° on the starboard bow:** bellied slivers |
| `lugger` (*Éclair*), heading 300 | **Close-hauled at 338 in a 26° apparent wind:** three lugs and two lug topsails from their corners, oblique yards rising aft, four-cornered sails on the larboard side of their masts, the topsails' clews at the lower lugs' peaks, the jib on the running bowsprit. **From ahead:** the lugs to leeward of the masts. **After "take in the main lug":** the lug and yard along the deck, its topsail down with it. A dip in progress was not seen (the tack refused at 1.7 kn, §4.4) |
| `topsail-schooner` (*Speedwell*), heading 300 | **Yards square:** the fore topsail and topgallant edge-on from the beam. **After "trim sails"** (yards 58° and 56° from square, foresail sheet 64° to 25°, main 18°), **from 74° off the larboard bow:** the topsails' faces above a loose-footed gaff foresail, its foot about 1.5 m above the deck, its clew reaching towards the main mast; the main gaff sail on its boom with the gaff topsail above; jib and fore staysail |

That is the standard to match: a generic hull, the spars and sails each by its class's
rule or its corners, the braces and sheets faint, every state drawn, and nothing else.

### 6.3 What each new ship needs

| Ship | Drawn as today, with nothing new | New work |
|---|---|---|
| The 64 | A three-master by the frigate's path, framed by `fullRigFrame` (1383-1414); nothing depends on size | Two tiers of ports, if wanted, need a new hull field, off by default (§9, question 4). A spritsail (§5) or a mizen yard (§4.7: a `lateen_yard` is drawn across the ship) needs new branches; a gaff mizen does not |
| The razee | As the 64, with a lower `deck_height_m` and the heights of §2.4 | The bowsprit is rooted at the reference deck (528-533), so it is drawn from her main deck. The cut-down topsides show only through the hull field above |
| The *Neufchatel* | The fore course from its yard; the fore topsail's clews to the fore yard's arms (`yardBelowId`); the loose-footed gaff foresail abaft the mast, its clew from its area (1102); a main topsail over a bare yard by `bareFoot`. Read; drawn in a scratch raster of the projection's figures from a hand-made snapshot (not the game's renderer) | Not new, but seen: the gaff foresail and the course overlap on the one mast, and the gaff peaks at the fixed 35° |
| The bilander | A lug-class settee with four `corners_m` gets an oblique yard and a four-cornered sail on its side of the mast through `lugCut` (scratch raster). A brace on its yard is drawn already | 1. **The sling point.** `lugCut` pivots the cut a third along throat→peak and shifts it so that point meets the mast (370-376). For the scratch settee the drawn throat was at x +1.3 m and the peak at −16.4 m, against the corners' −1.4 and −21.0 m, while the physics' `x_m` (−10.9) comes from the unshifted corners. A settee slung elsewhere needs a per-sail sling point, or its corners must be cut with the slings at the mast, or drawing and physics disagree. 2. **Clewed up aloft.** `lugHoisted` is false in the gear, so it is drawn on deck (355-360, 378-380); `gathered()` (868-884) could hang it from the yard. 3. **The sheet** runs from the clew to the lee rail 1 m abaft it (1309-1315), not to the taffrail. 4. **Vangs and lift** are not drawn. 5. **The brace's lead** may want its own rule |

### 6.4 Tools for B5

- **Pictures.** `window.FreeSailApp.picture("ship", facingDeg)` returns a promise of
  {width, height, ms, span, png}, the png a 960 × 720 data URL (`client/app.js:189-258,
  729`). Read.
- **Turning the view.** The developer switch `?facing=DEG` and the `[` and `]` keys turn it
  (`app.js:4-8`). Read.
- **Node.** `tests/test_view_geometry.py` runs `projection.js` under Node, and Node
  v22.23.2 is installed. Read.
- **The pane.** The built-in pane's screenshots are 800 × 600, and the ship panel about
  420 × 180 px unless the SVG is enlarged. When the pane was hidden, screenshots came back
  at 240 × 180 until the viewport was set again. Observed by R4.

## 7. The risks, ranked

Judgement, on the findings above.

| # | Risk | Why | Where it bites |
|---|---|---|---|
| 1 | The settee meets the lugger's paths | Getting under way fails outright (§4.4). Heave-to and the gale's reduction do not stop or hand a settee. "furl" means take in. Every path of §4.6 must be guarded without moving the lugger's pins | B3, B4 |
| 2 | One yard changes how a ship is handled | A main topsail yard (*Neufchatel*), a spritsail yard, a `lateen_yard` or the bilander's dry main yard each switch the helm, tack, wear, heave-to and gale paths (§3.3, §4.4, §5) | B2, B3, B4 and every truth |
| 3 | A false "Tacked" on a brig hull | Existing behaviour (`scripts.py:1129`; `tack.yaml:50`); a fix moves the brig's own pins, which the plan forbids | B4's and Phase 5's truths |
| 4 | The razee's cut-down is a new pattern | No precedent for removing guns or changing heights. The copy must be taken before `dump()`; `frigate()` must not be touched; upper masts and the bowsprit follow different rules (§2.3-2.4) | B1; the byte-identity lens |
| 5 | The heave-to backs the fore topsail | The bilander's main lost its course, so the fore wins by area (§4.4); the period's main topsail to the mast needs a rule or a field | B3, B4 |
| 6 | The settee's drawing and physics disagree | `lugCut`'s fixed third against a settee slung near its fore end; centre heights mistaken for deck heights (§4.4, §6.3) | B4, B5 |
| 7 | Registries keyed on descriptions | A 64 or razee missing from the man-of-war sets is not treated as a King's ship (§1.5) | Stage 0 |
| 8 | People files by stem, strict at generation | `wardroom()` raises on a missing file; at run time a missing file leaves no wardroom (§1.2, §1.5) | Stage 0, B1, B2, B4 |
| 9 | The names list fixes a default nation | The ruling against the schema's required list (§3.5) | B2, or stage 0 if a hook |
| 10 | The untuned lateen or lug curve for a settee | The physics of the settee is its curve and its corners alone (§4.3) | B3, the sailing lens |
| 11 | The 64's quarter bill at 66 guns leaves no marines in the divisions | Seen in the timing run (§2.7), not examined | B1, the gun-deck lens |
| 12 | The polar cache of eight | Twelve files; a cost, not a fault (§1.5) | Performance |
| 13 | The first-world timing artifact | A pace truth measured first in its process may read high (§2.7) | Phase 5 pace truths |
| 14 | The crew of 491 | Measured cheap: 2-8% slower a tick than 264, 0-6% in the checker's re-run (§2.7) | Low |

## 8. What is open

1. **Δdeck, c and δT** for the cut-down (§2.4): R1's figures, off ZAZ2371 and the
   sources.
2. **Which deck** the 64's `deck_height_m` names (§2.2).
3. **The length of the 64's 24-pounders**, and so their weight by Adye (§1.4): R1's.
4. **The exercise allowance:** a third for the 64 by a per-file override (§2.6); the
   razee is one deck.
5. **Ports.** Whether the 64's lee lower-deck ports should shut with heel. Wiring
   `lee_port_shut` changes the existing ships' combat, the privateer schooner's most
   (§2.6).
6. **The 66-gun quarter bill without marines** in the divisions (§2.7): why, and whether
   it is right.
7. **The *Neufchatel*'s main yard** (§3.3), and if carried, whether the classification
   needs an override.
8. **The settee shifted or standing** (§4.2): Röding against Steel; Lescallier's text for
   R3.
9. **The settee's sling point, peak and size** off Gwyn's drawing (R3), so that the
   corners can be cut with the slings at the mast (§6.3).
10. **The settee's curve:** lug, lateen or a new one (§4.3); and its take-in, furl aloft,
    trim and vang orders (§4.5).
11. **The bilander's heave-to:** a rule or a field for the main topsail to the mast
    (§4.4); a standing settee must be lowered or brailed when she heaves to.
12. **The getting-under-way guard**, and setting the settee as the driver after the cast
    (§4.4, `scripts.py:6925, 7354-7365`).
13. **The brig hull's false "Tacked"** (§4.4): reported to the lead. Whether to fix it is
    not this build's to decide, since it moves the brig's pins.
14. **Untried paths:** rounding to (`scripts.py:6070-6080`) and shorten-sail's base list,
    for a settee.
15. **The polar cache size** (§1.5).
16. **The size ranks** for the 64, the razee and the *Neufchatel* (§1.5).
17. **Not reached:**
    - the Stevens 1915 text's Internet Archive identifier, and its page numbers against a
      page image;
    - a lug dip seen in progress in the browser.
18. **pace.py on an empty machine** (§2.7): it was quiet, not empty, when measured.

## 9. The owner's questions

1. **The settee in the engine.** Your ruling builds it on the lug. That fits way 1 (a lug
   variant with a flag, every lugger path guarded) or way 3 (a new class that reuses the
   dip). Way 2, the dormant lateen class, would lose the dip and make the bilander
   square-rigged by its yard alone (§4.7). Which?
2. **Dipped round at every tack, or kept on one side?** Röding has the bilander's sail
   lowered and passed round like a lug; Steel has it hanging to the main mast as a ship's
   mizen does (§4.2). The engine can do either. A dipped settee loses a third of its
   drawing area if it is not dipped. A standing one keeps drawing when hove to unless it
   is lowered.
3. **The 64 and the razee as two ship files,** each with its armament by year as fits?
   Fits cannot carry hull, rig or crew changes (§2.1).
4. **The viewer's standard.** Keep the generic hull, with no ports and one freeboard, so
   that the 64 and the razee differ only in height? Or add an off-by-default hull field so
   that the two tiers of ports and the cut-down topsides show (§6.3)?
5. **A small square main topsail on the *Neufchatel*,** as Reed's model seems to show?
   Cobb has her main rigged as a schooner's, with no top. A main yard makes the game
   handle her as a brig: the helm by the highest square sail, the heave-to by backing
   yards, the mainsail brailed up (§3.3).
6. **The size ranks.** The 64 above the frigate, a new rank 4? The razee 3, as a frigate?
   The *Neufchatel*, at 328 tons, 1 as the privateer schooner or 2 as a brig?
7. **The spritsail and the 64's mizen yard.** Leave out the spritsail yard (the 64's, the
   bélandre's, the *Neufchatel*'s) and give the 64 a gaff mizen, as she had by 1796? Both
   period spars need engine and viewer work before any file carries them (§2.4, §5).
8. **The *Neufchatel*'s hands.** French names by default, with the scenario choosing her
   nation (no engine change)? Or a mixed privateer company, as Stevens and Cobb record
   (§3.5)?
