# Design: HMS *Indefatigable*, the 64 of 1784 and the razee of 1795 (package 75, Phase 3)

The design for the first ship of package 75 to be built. It was judged from two drafts, one
written for fidelity and one for buildability, and every claim kept was checked against the code
at this head and against the notes. Where the drafts disagreed, or one was wrong, this document
says so and gives its reason (the table below). It is for her builder (B1) and for the
synthesis's build document; its §0 and §12.2 are also for the lead, who gates the engine
extensions she waits on. Nothing here is built.

**What binds, in order:** the brief (`docs/dev/M7-WorkPackages.md`, its head rules and
"Package 75", l. 1540 on); the lead's go-ahead of 2026-10-28 (Phase 3, then the build one ship at
a time, the *Indefatigable* first; the generator modules, hull profiles and ship files need no
gate; the gate stands on the engine extensions only); the plan (`Plan-ShipsWorkflow.md`, Phase 3,
the per-ship modules under `tools/ships/`); the owner's answers and the lead's rulings
(`Decisions-ShipsRound2-2026-10.md` l. 1-60; every decision not named there taken as
recommended; D31 (a) for her guns and (c) for her crews; **D18 and D25 open: proposed here, not
settled**); the research notes.

**Code** is cited as file:line at the package branch's head 6b94731 (the lead's 3421829 merged:
packages 73, 86 and 84's steps 1 and 2). **Sources** are cited by note section: **Ind**
(`Research-Indefatigable-2026-10.md`), **Eng** (`Research-ShipsEngine-2026-10.md`), **Bel**
(`Research-74-2026-10.md`), and by decision number (D8, D9, ...). The owner's private books are
cited by page only (Winfield 1793-1817 pp. 99-100); none of their text is here. **Marks:** read,
read (OCR), measured, catalogue, secondary, memory, judgement, observed. "Measured here" means
arithmetic on the notes' figures, or a page image read, by this document's scratch scripts
outside the repository (`scratchpad/design/indj/figs.py`, `figs2.py`; the import probe in
`indj/hook/`; Steel 1794 vol. I p. 49 and table IV read on the held page images). Nothing in
the repository was changed, and no test was run.

**The maps.** The code maps cited as *map-engine* and *map-generator*, and the shared-work
draft folded into `Build-Ships.md`, are filed beside this document in `ships-design/`. The
scratch scripts named are not.

**One sentence.** One module writes two files, the 64 first and the razee derived from her as
data; both are built at once except two pieces of the 64 (her mizen course on its yard, and her
yards under the bowsprit), which wait behind two stubs for the gated engine design, while the
64 sails meanwhile on a stand-in whose physics is already the owner's. Both files take the hull's
shape keys at stage B (§3.5 item 8).

---

## How the two drafts were judged

| Question | Taken from | Why, in short |
|---|---|---|
| The module's shape: particulars as data, the razee by named steps, one ship function | buildability | Each step carries its source; the derivation's checks are asserted before a file is written. The fidelity draft's one function with a variant branch in each place would do the same work less legibly |
| Data in the drawings' frame (ft from AP, ft above K), converted once | fidelity | Every figure reads as the source gives it; the conversion is checked once |
| One frame for every height (above the ship's own water), D18 one figure | buildability | D18 becomes `datum_z`; the rise and the cut are arithmetic |
| D18 proposed | buildability: **(a)** | The razee's arrangement (a continuous gun deck, a quarterdeck and forecastle joined by gangways) is the frigate-36's, so the same rule for the same arrangement. The fidelity draft's (c) is one figure away and shown on screenshots (§2.2) |
| Displacements | buildability (2,170 and 1,925 t) | Both inside Ind §2.3.3's own bands, their difference the measured slice. The fidelity draft's razee (1,880 t) lay below the razee's own band |
| Half-breadth at the lower sill | buildability (6.67 m) | Measured here: the sill stands 23.8 ft above the rabbet, where the section is 21.52 ft moulded; the fidelity draft read the section at 24.6 ft (6.64 m). Both give 10.6° |
| Gun heights to the centimetre, the sill itself | fidelity, by the buildability draft's means | `broadside_pair` rounds to 0.1 m (`gen_ships.py:3722-3723`); the height is reassigned after it, as the merchant brig reassigns the crew (`:4397`) |
| Steel's topgallants and royals against Steel's spars | fidelity | A real conflict (measured here, §4.3); the buildability draft listed the sail table's areas, which cannot hang on the spars |
| Broadside by 70's rule | fidelity (714 and 510 lb; frigate 421) | `far_ship` counts one side's broadside guns and **every** chaser (`combat/far.py:104-108`). The buildability draft's 690 and 403 left the chasers out; the fidelity draft's 64 at 870 lb was an error (600 lb measured here) |
| Gun weights in a shared period table | both, as stage 0's (fidelity) | The 74's builder needs the same table; stage 0 lays it so neither builder waits on the other |
| 18-pdr of the 64 at 40 cwt | fidelity | One reading for both two-deckers of the package (Bel §13.1 answer 12; Lavery's Table 17 via Bel §13.4) |
| Trimmers and the marines' division | fidelity | The seamen's remainder, so that the marines not at the carronades form their division as Falconer quarters them (§6.4) |
| Small arms | neither; the frigate-36's share | Falconer's figures run close to whole detachments of marines (§18), so the fidelity draft's reading of them as seamen is doubtful; the buildability draft's figures were unexplained |
| Ground tackle cables | fidelity (Steel's seven, laid as Lever's Channel service) | The period's own count, where the house rule splices two |
| The import hook | buildability (measured), re-measured here | Mixing two copies of the generator fails at `dump` (§1.2) |
| The gate's contract | both, merged | The fidelity draft's point that the sail's lateral offset must come from the part abaft the truss; the buildability draft's six-item contract |
| "A ship of the line" | buildability | Refused in three places; no description of hers takes those words (§8) |
| The razee's spritsail yards | fidelity's finding, put to the owner | Steel p. 49 gives the 44 and the 38 both yards (read here on the page image) |
| D25 and D48 | merged | The fidelity draft's table of options; the buildability draft's "what is common is a test, not a scenario file" |

---

## Decisions taken

| # | Decision | Why, in short |
|---|---|---|
| 1 | One module `tools/ships/indefatigable.py`, `build(out_dir)` writing two files: `data/ships/sixty-four.yaml` then `data/ships/razee-44.yaml` (names the lead's to change) | The lead's structural decision; type names as the house has them (`frigate-36.yaml`), the ship named in `ship.name` |
| 2 | The razee is **derived as data**: `razeed(sixty_four())` applies the dockyard's work by named steps; one `write(out_dir, p)` builds each file in full. No Builder is copied or edited | A Builder cannot be dumped twice (`dump` mutates the doc, map §1.6); a second full build is the house pattern (`brig(merchant=True)`) |
| 3 | No existing function or table of `gen_ships.py` is edited; her figures come from the module and from a shared stage-0 `tools/ships/period.py` | Byte identity of the eight files by construction |
| 4 | Every height is held above the variant's own load water at its station; the file's convention is applied once by `to_file` | D18 becomes one figure; the rise (δT) and the cut (c) are arithmetic |
| 5 | Hull: D28 (a), D29 (b), D34 (a). LWL 48.8 m, beam 13.54 m, draught 6.33 / 5.88 m to K, lateral plane 305.5 / 283.4 m² | As decided; Ind §2.3-2.4, measured |
| 6 | Displacement 2,170 t and 1,925 t: the difference is the measured slice, 245 t | Inside both of Ind §2.3.3's bands (judgement on measured lines) |
| 7 | **D18 (open) proposed (a):** the 64's upper deck, 3.22 m; the razee's gun deck, 1.39 m | The frigate-36's rule for the same arrangement; (c), 3.66 m, is one figure and is shown beside it on screenshots (§2.2) |
| 8 | A hull profile under `hull.profile` (a stage-0 key): keel, stem, stern, rail, wales, decks, ports as `[x, sill, half-breadth]` triples by deck, the midship section; z above the load water | D14 (c); the owner's lee-port rule reads the sill and the half-breadth from it (Bel §13.1 answer 7) |
| 9 | Each broadside gun's `x_m` and `height_m` are its port's measured position and sill, to the centimetre | The lead's ruling (sourced sills); rounding to 0.1 m would shut the 64's lowest port 0.26° early (measured here) |
| 10 | Masts and yards by Steel 1794 vol. I p. 49's 64 column; positions, heels, rakes measured; heads by Steel's rule; the razee's lower masts cut by the measured c (D19 (a)) | Ind §3.1, §3.3 |
| 11 | Sails by Steel's table IV, 64 column, where they fit Steel's spars; topgallants and royals cut to the spars, the table's figures in the notes | Steel's two tables disagree above the topmast caps (§4.3); put to the owner |
| 12 | **The 64's mizen course, stage A:** a loose-footed gaff-class sail on spar `mizzen.yard` (class `gaff`, the yard's after part); **stage B** the gated class. Ids, area, corners and groups final from the first commit | The physics of either gated route is a loose-footed fore-and-aft sail by its sheet (map-engine §1.6); only the spar's class, length, lines and drawing change |
| 13 | **The 64's spritsail and sprit-topsail yards** are not written until stage B (`head_yards()` a stub) | A bowsprit yard reclasses her head yards and breaks the stagger today (map-engine §3.2) |
| 14 | The razee carries no yards under the bowsprit (D8 (b) as answered) | **Plainly:** Steel p. 49 gives the 44 and the 38 both yards; put to the owner (§17) |
| 15 | The razee's mizen: gaff 40 ft 10 in, boom 65 ft 4 in (D20 (a), Steel p. 40); the sail about 240 m² | As decided; the area by the frigate's spanker rule (measured here) |
| 16 | Fits: the 64 **"ardent class 1784"** (default) and **"ardent class 1794"**; the razee **"as razeed 1795"** (the brief's words) and **"as carried 1796"** (default: the owner, 2026-10-28) | D17 with the brief; Winfield 1793-1817 p. 99; James vol. 1 pp. 361, 454 |
| 17 | Patterns (Adye 1804 pp. 72, 155): 24-pdr 9 ft 6 in 49½ cwt; 18-pdr 9 ft 40 cwt; 12-pdr 9 ft 6 in 34 cwt; 9-pdr 7 ft 6 in 24½ cwt; carronades 42-pdr 22¼, 24-pdr 13, 18-pdr 9 cwt | D31 (a) for the razee; the 74's reading for the 64's 18s and 9s (judgement for hers) |
| 18 | Crews by Falconer (11, 9, 7, 6 to the 24, 18, 12, 9) and Douglas (4 to any carronade), in both files | D31 (c); Bel §13.1 answer 12 |
| 19 | Guns numbered on across decks from forward; a `deck` word on each gun when stage 0 lands the key | `(number, side)` unique in a fit (`schema.py`; map §0 item 17); a number is one crew (`parts.py:553-559`) |
| 20 | Exercise: the 64 a third of her 26 upper-deck guns (8), the razee a fourth (6) | The Regulations, the Gunner, Art. XXI (read (OCR) here, l. 13118-13144) |
| 21 | The charges note overridden in her fits to cite Table No. 29 as read | The engine's shares give every calibre of her fits to the ounce (Ind §6.4) |
| 22 | Company: the razee 330 (D32 (a): the 294 column, 36 seamen over, 50 marines); the 64 491 (the 491 column, 84 marines) | Ind §4.2; the 64's privates judgement on the *Bellona*'s share in 1761 (Lavery 1985 p. 17, via Bel §13.4) |
| 23 | Trimmers are what the **seamen** leave when one side's guns and the wheel are manned, the marines taking the carronades first | **Plainly:** the frigate-36's count also spends her marines at the guns; Falconer quarters the marines apart (§6.4) |
| 24 | Ground tackle: Steel's 64 in both files (D33 (a)), four bowers of 57 cwt, seven 21-in cables laid three, two, one, one | Steel's tables (Ind §6.2); Lever 1808 p. 67 as the generator cites it |
| 25 | Size and rate (D16 (a)): "sixty-four" rank 4, "razee" rank 3; `("razee", 3)` first in `_SIZE_WORDS`, then `("sixty-four", 4)` | Without that order the razee's own words rank her 4 (§8) |
| 26 | Polar measured and recorded; `hull_speed_kn` and `clr_x_m` tuned only against sourced bands; not forced | D24 (a); realism, not pacing |
| 27 | D48 (a) meets a named fit; three ways laid out, the lead's call | §11.1 |
| 28 | D25 open: each option's needs laid out; what is common built now as a test, no scenario file | §11.2 |
| 29 | Five truths proposed by content (§14) | The brief's and the plan's for her |

---

## 0. The gate: what her builder builds at once, what waits, behind which stub

The lead's gate stands on the engine extensions only (the settee, the lateen class finished with
the mizen course cut at the mast, the yards under the bowsprit: one design document to the lead
before their builders start). The razee needs none of them. The 64 needs two: her mizen course on
its yard (D9 (c) as revised in Bel §13.5) and her yards under the bowsprit (D8 (b)).

**Stage A, at once, no gate:**
- the module, both people files, and both ship files complete in hull, profile, masts, yards,
  sails, lines, groups, guns, crew, quarter bill, ground tackle, boats, pumps, hold and stores;
- the razee's file **final** but for the hull's shape keys, which both files take at stage B
  (§3.5 item 8);
- the 64's file complete but for two pieces, each in one function of the module and switched by
  one module constant:
  - `mizen_course(b, p)` with `MIZEN_COURSE = "stand-in"`: the course as a loose-footed
    `gaff`-class sail on spar `mizzen.yard` of class `gaff` (§4.4). The owner rules this sail "in
    the physics, a four-sided, loose-footed sail, like the gaff sail" (Bel §13.5), so her polar,
    her heave-to and her handling are already the owner's;
  - `head_yards(b, p)` with `BOWSPRIT_YARDS = False`: writes nothing; its docstring and the
    bowsprit's note say the yards are Steel's and come with the gate.
- every id final from the first commit: `mizzen.yard`, `mizzen.course`, `spritsail.yard`,
  `spritsail`, `sprit_topsail.yard`, `sprit_topsail`, so that stage B renames nothing and moves no
  group member.

**Stage B, once the gated design is approved and its builder's stage 0 is in:**
- `MIZEN_COURSE = "gated"`: `mizzen.yard` takes the gated spar class at its whole 77 ft 0 in,
  slung at its truss with its fore part bare; the sail takes the gated class and roles; the
  yard's lines become the engine design's (its §3.4: no truss or brail lines); Steel's driver
  is left out and named in her note (§4.4, as settled);
- `BOWSPRIT_YARDS = True`: the two yards and their sails, at the station along the bowsprit the
  gated design gives a key for (§4.6);
- *chosen since by the owner (the engine design §17, its §17.9 item 1; approved by the lead, 2026-10-29):*
  `DRIVER = True`, a third flip: Steel's driver boomsail in the sail room, `in_place_of` the
  course, and its boom on the mizen mast; only with `MIZEN_COURSE = "gated"`, and only after
  the engine's step B3.5 and the viewer's drawing of it (§4.4);
- each flip regenerates `sixty-four.yaml` alone; every figure it moves (her polar, her balance,
  her truths' measures) is shown old beside new in the review and the tuning notes.

**If the gate slips past the package's merge.** The 64 goes in on the stand-in with no sprit
yards. **Plainly:** that departs from D8 (b) and D9 (c); her file notes, the tuning notes and
spec §27 as built say so, and her rig-dependent truth clauses are pinned on the stand-in and
re-measured, old beside new, when stage B lands. The razee, the main goal, is untouched by any of
this.

What the gated design must give her is §12.2.

---

## 1. The module and the generator

### 1.1 Files

| Path | What | Owner |
|---|---|---|
| `tools/ships/__init__.py` | docstring only: what the package is and how it is imported | stage 0 |
| `tools/ships/period.py` | the period's tables both two-deckers read (§12.1 item 4); constants only, no Builder calls | stage 0, append-only after |
| `tools/ships/indefatigable.py` | `Particulars`, `sixty_four()`, `razeed(p)`, `write(out_dir, p)`, `mizen_course(b, p)`, `head_yards(b, p)`, `build(out_dir)` | B1 |
| `data/ships/sixty-four.yaml`, `data/ships/razee-44.yaml` | generated only | B1, through the generator |
| `data/people/sixty-four.yaml`, `data/people/razee-44.yaml` | the wardroom files, hand-written data, the frigate-36's form | B1 |

Each file's header is its own literal string and contains "Generated by tools/gen_ships.py" (the
phrase `tests/test_fishing.py:99` reads for the smack).

### 1.2 The import (measured here)

Stage 0's entry block (`tools/gen_ships.py:8479-8490`), after `smack(out)` and before the final
print:

```python
    # package 75: the per-ship modules under tools/ships/, each importing this running script
    # as `gen_ships`, so that its Builders, DesignLoads and helpers are these, one copy
    sys.modules.setdefault("gen_ships", sys.modules[__name__])
    for name in SHIP_MODULES:          # the four modules, named in stage 0, each a stub until built
        importlib.import_module(f"ships.{name}").build(out)
```

The module begins `import gen_ships as g` and takes every helper as `g.<name>`. **Rule:** a ship
module is imported only inside the `__main__` block, after the alias.

Measured here, in a scratch copy of the generator's entry with a probe module that builds a mast,
a gaff and a gaff sail rated by `design_kn`:

| Case | Result |
|---|---|
| With the alias | the module's `gen_ships` is `__main__`; the probe dumps and its two spars carry "Rating:" |
| Without the alias, the module using one copy throughout | a second copy loads (re-reading the wardroom files at import) and works |
| A Builder of one copy with a `DesignLoad` of the other | fails at `dump`: `yaml.representer.RepresenterError: ('cannot represent an object', 6.1)` |

The buildability draft measured the same; the map's judgement (map §1.10) is now measured twice.
`tools/` is on the path when the script runs (the script's own directory; `REPO_ROOT` is
inserted before it at `:122-124` and holds no `ships`), so `ships` resolves to `tools/ships/`; the byte-identity test runs the script from the root
(`tests/test_ship_particulars.py:555-562`), so the same holds there. `wardroom(stem)`
(`gen_ships.py:3507-3525`) is called inside `build()`, never at import, so a missing people file
breaks only her build (Eng §1.2).

### 1.3 What B1 reuses, read-only, and what it writes anew

**Reused** (lines in `gen_ships.py`): `Builder` and its methods (`:573-1078`); `ft`, `FT`,
`SIDES`, `rope_kn` (`:410`), `quarter`, `DesignLoad`, `design_kn` (`:444`), `DESIGN_WIND_KN`;
`cloth`, `canvas_note`, `FRIGATE_CANVAS` (`:184`; Steel's by sail, not by rate, so it serves a
64; the 64's mizen course takes its `mizzen.spanker` entry, Steel's 'Mizen-course', `:227-231`);
`square_sail_lines` (`:1433`), `FRIGATE_ROPE` (`:1473`) scaled, `HORSE_NOTE`;
`stay_sail_cut` (`:1110`), `staysail_from_cut` (`:1148`), `between_the_masts` (`:1197`),
`_quad_area_centroid` (`:7030`); `raked_x` (`:2519`), **always with `deck_m=` her own datum**
(its default is the frigate's 1.8); `fit_magazine` (`:3618`), `filling_party` (`:3665`),
`broadside_pair` (`:3709`), `chasers` (`:3730`), `KINGS_ROUNDS` (`:3606`), `MAGAZINE_NOTES`
(`:3674`), `FILLING_NOTE`, `QUARTER_BILL_NOTE`, `PRIORITY_NOTE`; `hold_for` (`:3367`),
`boat_entries` (`:3378`), `pump_entries` (`:3437`), `ration_entries` (`:3535`), `wardroom`,
`PUMPS_NOTE`, `BOATS_NOTE`, `SHOT_PLUGS_NOTE`, `SMALL_ARMS_NOTE`, `BOARDERS_NOTE`.

**Written anew in the module, modelled on the frigate's lines** (`frigate()` takes no
particulars and dumps itself, so it is not touched: Eng §1.3): the mast and yard loop
(`:1713-1839`), the head (`:1908-2003`), the studding sails (`:2019-2094`), storm and occasional
canvas (`:2096-2301`), groups and aliases (`:2303-2424`). The module's `geom[mast]` uses **the
frigate's keys** (`above`, `head`, `t_hoist`, `g_hoist`, `r_hoist`, `yard`, `topsail_yard`,
`tg_yard`, `royal_yard`, `yard_h`, `topsail_h`, `tg_h`, `royal_h`; `:1582-1632`), filled from
Steel's table, so that `between_the_masts` and the copied loops run unchanged.

### 1.4 The data, the frame and the conversion

- **Data at the top of the module, in the drawings' frame** (feet forward of AP, feet above K,
  as Ind gives them), each figure with its source in a comment: `WL1` (21.22-21.27 ft above K at
  AP, 20.16-20.26 at 160 ft: Ind §2.3.1), `RAZEE_RISE` (1.45 ft aft, 1.47 forward, parallel),
  `DECKS` (Ind §2.3.5), `PORTS` and `SILLS` (Ind §2.3.7), `WALES` (§2.3.5), `STEM`, `POST`,
  `KEEL` (§2.3.6), `SECTION` (§2.3.2), `MASTS` (positions, heels, rakes: §3.1), `STEEL_64`
  (spars: §3.1), `STEEL_SAILS_64` (Ind §5), `CUT` (c per mast: §3.3).
- **The file frame.** x in metres forward of the mid-perpendiculars, 80 ft forward of AP:
  `x_m(ft_from_ap) = (ft_from_ap − 80) × 0.3048`. With D29 (b)'s length rabbet to rabbet at WL1,
  this is the middle of the load waterline (Ind §2.4). z in metres **above the variant's own
  load water at that station**: `z_m(ft_above_k, ft_from_ap, waterline)`. The water is inclined
  to the keel by the drawn drag (1.04 ft over 160 ft), and the engine has no trim, so a height
  above the water at its own station is what the engine believes.
- **`to_file(p)`, once:** a lower spar's `height_m` is its z less `p.datum_z` (the D18 deck at
  midships); an upper mast's is its hoist above the cap below; `corners_m` heights are above the
  datum; a sail's `centre_height_m` and a gun's `height_m` stay above the water. These are the
  file's conventions (map §2.2; `schema.py`, the spar and sail specs; map-engine §1.1).
  **Plainly:** "above the datum" means above a horizontal plane at the datum's midship height,
  not above the local deck, because the engine and the viewer read every spar height from one
  `deck_height_m` (`physics/sails.py:1560-1566`; `client/projection.js:275`).
- **Rounding.** `ft()` rounds to 0.1 m (`gen_ships.py:395-397`). The module rounds measured
  figures to 0.01 m (sills, decks, hull, profile) and spar and sail figures as the frigate's are.
  It rounds early, at the measured value, so that a last-bit difference in `math.tan` between
  platforms cannot flip a written figure (§16, risk 4).

### 1.5 The razeeing as data: `razeed(p64)`

Each step is a named function of `p`, and each writes its source into the note it changes.

| Step | What changes | Figures | Source |
|---|---|---|---|
| 1. The rise | the waterline drops: every z rises by δT at its station | 1.45 ft aft, 1.47 ft forward (0.44-0.45 m) | D28 (a); Ind §2.3.1 |
| 2. The upper works | the 64's quarterdeck, forecastle and their sides off, and the upper deck in the waist (gangways kept); the roundhouse shortened, unmeasured and left out of the profile | the razee's quarterdeck the old upper deck to its breast at 74.4 ft, gangways 74.5-118.5 ft, forecastle from 118.5 ft | James vol. 5 p. 428; ZAZ2371 N.B.; ZAZ2375 (Ind §2.2, §2.3.5) |
| 3. The datum | D18 (a): the 64's upper deck gives way to the razee's gun deck (the 64's lower deck) | 3.22 → 1.39 m above her water | §2.2 |
| 4. The heels cut | each lower mast shortened at the heel by the height of the deck removed | fore 6 ft 3 in, main 6 ft 7 in, mizen 6 ft 9 in | D19 (a); Ind §3.3 (the kit's account, measured on ZAZ1280) |
| 5. The upper spars | topmasts, topgallants, every square yard, the crossjack, the studding-sail booms the 64's, standing on the new heads | Steel p. 49 | D19 (a); Ind §3.3 |
| 6. The mizen | the 64's mizen yard and course give way to gaff, driver boom and spanker | §4.5 | D20 (a) |
| 7. The head | bowsprit and jib-boom the 64's, in their place in the hull; no sprit yards | Δdeck 7 ft 5 in at midships against the new datum | D8 (b) as answered; Eng §2.4 |
| 8. Guns, people, stores | her own fits, company, bill | §5-§7 | D17, D30-D32 |
| 9. The hull block | her own measured figures, not transforms | §2.1 | Ind §2.4 |

**Checks raised inside `razeed()` before any file is written** (with `raise ValueError(...)`
and a sentence, not `assert`, which `python -O` strips):
- the razee's midship gun-deck sill within 0.03 m of ZAZ2371's measured 1.96 m (6 ft 5 in): an
  independent measurement (the frame gives 1.98, measured here);
- her old upper deck at midships within 0.05 m of 3.66 m above her water (Ind §2.3.5, measured on
  2371 and 1280T; the frame gives 3.66);
- each lower mast's head above K lower than the 64's by exactly its c;
- the two displacements differing by 238-244 tons of 35 cu ft (the measured slice ±5%, at
  1.016 t a ton).

---

## 2. The hull blocks

### 2.1 The figures

| Field | The 64 | The razee | Source |
|---|---|---|---|
| `length_waterline_m` | 48.8 | 48.8 | D29 (b): rabbet to rabbet at WL1, measured (Ind §2.3.2, §2.4); 50.2 / 49.9 m outside post and stem in the note |
| `beam_m` | 13.54 | 13.54 | D34 (a): 44 ft 5 in extreme as built (Winfield 1793-1817 p. 100) |
| `draught_m` | 6.33 | 5.88 | D29 (b), D28 (a): mean to K, the band's bottom (Ind §2.3.1). The main-keel figures (6.15 / 5.71) and Osler's 19 ft 6 in abaft (p. 111) in the note |
| `displacement_kg` | 2,170,000 | 1,925,000 | judgement within Ind §2.3.3's bands (2,120-2,240 t; 1,900-1,955 t); the difference is the measured slice, 238-244 tons of 35 cu ft (±5%) |
| `gm_m` | 1.35 | 1.65 | judgement within Ind §2.3.4's 1.2-1.5 and 1.5-1.8; KM measured 7.3 / 7.25 m above K, KG about 1 ft lower after the razeeing |
| `clr_x_m` | +4.1 to start | +4.1 to start | the measured centroid of the plane the file counts (hull with the band, no rudder: −0.55 and −0.61 m, Ind §2.3.6), plus the frigate-36's tuned lead of 9.6% of her load line (her +3.0 against a centroid about 1.0 m abaft midships, `gen_ships.py:1563-1570`; judgement). Tuned against the helm truths (6, 17) and recorded tuned |
| `lateral_area_m2` | 305.5 | 283.4 | D29 (b): with the band, measured (Ind §2.3.6) |
| `hull_speed_kn` | 12.8 | 14.0 | D24 (a): the razee the frigate-36's 13.0 carried by √(160/137) = 14.05 (measured here), tuned within 13-14.5; the 64 within 12.5-13.0. **Plainly:** both hulls have one length, so the gap is the decision's ranking, not the waterline's |
| `deck_height_m` | 3.22 | 1.39 | measured (Ind §2.3.5; the frame here); D18 (a) proposed, §2.2 |
| `rudder` | area 8.95, span 6.47, 35°, 3.0°/s | area 8.45, span 6.04, 35°, 3.0°/s | measured (Ind §2.3.6), the razee at D28 (a)'s line; the angle and rate the frigate-36's (judgement) |
| `profile` | §3 | §3 | D14 (c); the key is stage 0's |

**The masts** stand in both files where ZAZ1280 measures them (Ind §3.1): mizen −16.33 m (rake
2.15°), main −2.78 m (1.4°), fore +19.23 m (0.3°). The razee kept their places (measured there).

### 2.2 Which deck is the datum (D18, open): the proposal

The owner's measure: "whichever choice gives the best impression in the viewer and matches the
sources. The convention may change, so long as the change is an improvement." The lead's reading:
with the profile drawn (D14 (c)), the deck height serves the physics and the spar heights alone.
What the datum still reaches at this head is small and known: the deck wind's eye
(`physics/sails.py:349`, at the datum + 1.5 m) and `apparent_wind` (`physics/hull.py:391`); the
readings (`api/readings.py:382`); the lookout's eye (`world/lookout.py:215`, the datum plus the
masts: invariant here, since the masts are measured from it); and in the viewer the generic hull
(`projection.js:1416-1448`), the bowsprit's root (`:528-544`) and the loose foot of a gaff sail
(`LOOSE_FOOT_HEIGHT_M`, 1.5 m above the datum).

| | (a) the uppermost continuous deck (proposed) | (c) the deck she was worked from |
|---|---|---|
| The 64 | upper deck, 3.22 m | the same |
| The razee | gun deck, 1.39 m | old upper deck (quarterdeck, gangways, forecastle), 3.66 m |
| Her lower masts' `height_m` (main) | 23.68 m | 21.41 m |
| The deck wind's eye | 2.9 m above the water; the frigate-36's 3.3 m on the same rule | 5.2 m, where her officers stood |
| The frigate helpers' fixed heights "above the deck" (the mizen staysail's foot 6 ft 6 in, `:1275-1287`; the lower studding-sail booms 1.0 m) | land about her quarterdeck as on the frigate (her quarterdeck 7 ft 5 in above the datum, the frigate's 6 ft 11 in) | land 7 ft 5 in higher, so the module sets them in its frame |
| The bowsprit drawn from the datum | 2.3 m below the stem head, until the viewer roots it from the profile (§12.3; done at B5.3, 2026-10-29) | where it stood |
| The generic hull before the profile is drawn | a low side, about right | as high-sided as the 64: wrong until the profile is drawn |

**Proposed: (a).** The razee's arrangement is the frigate-36's own: a continuous gun deck with a
quarterdeck and forecastle above it joined by gangways (ZAZ2375; Ind §2.2). (a) gives the two
frigates of her scenario the same rule for the same arrangement, so their deck winds, their
helpers' heights and their drawings compare like with like, and it is the decision sheet's
recommendation. The fidelity draft's case for (c) is real: the deck wind on her quarterdeck, the
bowsprit drawn where it stood, the masts' heads "the same height above the working deck". The
frame keeps the heads where they stood under either choice (it measures them above the water),
and the bowsprit is the viewer's to root from the profile (§12.3), so what (c) buys reduces to
the deck wind's eye, 2.3 m higher, in a shear the physics barely reads. **The owner's measure
is the picture:** the builder shows the razee beside the 64 and the frigate-36, abeam to leeward,
under (a) and under (c) (one figure, `datum_z`, changes), once the profile is drawn, and the
owner chooses. Under (a) the "Plainly" is none: it is the sheet's recommendation; under (c) it
would depart from the frigate-36's convention, and both files and the tuning notes would say so.

---

## 3. The hull profile (D14 (c))

### 3.1 The form proposed (stage 0 owns the key; the synthesis fixes it for every ship)

```yaml
hull:
  ...
  profile:      # x forward of the mid-perpendiculars; z above the load water at that station
    keel_m:  [[x, z], ...]                # K, the band's bottom, post heel to forefoot
    stem_m:  [[x, z], ...]                # the stem's fore edge, forefoot to stem head
    stern_m: [[x, z], ...]                # the post's after edge, then counter and taffrail
    rail_m:  [[x, z], ...]                # the top of the side as drawn, taffrail to stem head
    breadth_m: [[x, hb_water, hb_rail], ...]  # required with rail_m: half-breadths by station
    wales_m: [[x, z_lower, z_upper], ...]
    decks_m: {lower: [[x, z], ...], upper: [...], quarterdeck: [...], forecastle: [...]}
    ports_m: {lower: [[x, sill_z, half_breadth], ...], upper: [...], ...}  # one side's ports
    port_size_m: {lower: [width, depth], upper: [width, depth], ...}
    section_m: [[z, half_breadth], ...]   # the midship section, plank on
```

- *Settled by `Build-Ships.md` §5.1:* this form for every ship, with `breadth_m` (the shared
  work's: the viewer needs half-breadths along the length to draw a true side) required beside
  `rail_m`, and the key order and refusals given there.
- **Every z above the load water**, so the profile is independent of D18, and the viewer, which
  draws the water at z = 0, takes it as it stands.
- **Ports as triples.** The lee-port rule wants each port's sill and the side's half-breadth at
  that sill (Bel §13.1 answer 7); the triple gives the wiring a lookup with no geometry of its
  own. **The contract:** every broadside gun's `(x_m, height_m)` equals one triple's `(x,
  sill_z)` of its deck, to the centimetre. Package 81 draws the ports from the same triples and
  `port_size_m`.
- **The deck words** are the gun `deck` key's (§12.1 item 3): `lower`, `upper`, `quarterdeck`,
  `forecastle`, `roundhouse` (`middle` for a three-decker later). The razee's gun deck is `upper`:
  ZAZ2374 titles it "Upper Deck for the Indefatigable", and Winfield 1793-1817 p. 99 calls it her
  upper deck as a frigate.
- **Stage 0's work:** `HullSpec.profile`, optional, `None` by default, its shape validated and
  **unknown keys inside it refused** (a misspelt key would otherwise vanish, as an unknown hull
  key does today: map §0 item 4) (`schema.py:345-356`, `_parse_hull` `:1245-1267`); served by
  `ship_graph` only when present (`api/queries.py:380-406`); optionally a `dump` regex keyed to
  `profile:` that sets each pair list on one line, as `corners_m` is set (`gen_ships.py:938-950`;
  that regex matches only a two-space `corners_m:` and so cannot touch a profile). No existing
  file carries the key, so the byte test proves it inert.
- **Its note.** One note above `profile:` (the dump notes two-space hull keys,
  `gen_ships.py:1072-1074`) names the sources by line; the module's comments carry each point's.
- **If stage 0 is late,** B1 writes the key anyway: the parser drops unknown hull keys silently,
  so the data waits in the file. **Plainly:** a fallback, not the plan.

### 3.2 Her points (file frame, metres; verified here against the notes' figures)

| Line | The 64 | The razee | Source and mark |
|---|---|---|---|
| Keel (K) at AP; at the band's fore end | (−24.38, −6.48); (+20.65, −6.18) | each +0.44 to +0.45 | measured (Ind §2.3.1, §2.3.6) |
| Stem, fore edge below water | (+25.44, 0.00), (+24.67, −1.55), (+23.90, −3.38), (+23.23, −4.60), (+22.72, −5.21), (+21.88, −5.82), (+21.41, −6.00), to the band at about +20.65 | each z +0.44 | measured, ±0.05-0.15 ft (Ind §2.3.6) |
| Stem above water to the stem head | **to measure** on 1407F / 1280T | stem head at x +24.57 (160.6 ft on ZAZ2375); height **to measure** | Ind §2.3.5 (measured, the position) |
| Post | heel (−24.36, −6.48); at WL1 (−24.76, 0.00), raking 3.5° | each z +0.44 | measured (Ind §2.3.6) |
| Taffrail | **to measure** (the 64's upper works reach about 49 ft above K, tentative) | x −26.06 (5 ft 6 in abaft AP); height **to measure** on 2371 | Ind §2.3.5 |
| Lower deck (the razee's `upper`) | (−23.16, 1.28), (0.00, 0.95), (+19.81, 1.18) | (−23.16, 1.72), (0.00, 1.39), (+19.81, 1.62) | measured (Ind §2.3.5) |
| Upper deck (the razee's quarterdeck and forecastle) | (−23.16, 3.46), (0.00, 3.22), (+19.81, 3.36) | (−23.16, 3.90), (0.00, 3.66), (+19.81, 3.81); open in the waist from x −1.71 to +11.73 (74.4-118.5 ft), gangways along the sides | measured (Ind §2.3.5) |
| The 64's quarterdeck; forecastle | (−23.16, 5.57) to (−2.07, 5.25); (+12.10, 5.21) to (+19.81, 5.26) | cut away | measured (Ind §2.3.5) |
| Rail | the 64's quarterdeck, forecastle and roundhouse rails **to measure** (1407T, 1280T, 1953) | the waist top-side (0.00, 3.51); the quarterdeck rail 4 ft 6 in above the quarterdeck (not re-measured); roundhouse **to measure** | Ind §2.3.5; the roundhouse after December 1794 unmeasured (Ind §10.9) |
| Main wale; channel wale (midships) | −0.16 to 1.21; 2.46 to 3.04 | 0.28 to 1.65; 2.90 to 3.48 | measured on 2371, not re-measured (Ind §2.3.5) |
| Section | Ind §2.3.2's outermost section, plus 4½ in of plank, in z above WL1 | the same, each z −0.44 | measured (1407T, ±0.15 ft) |
| Port size | lower 0.99 × 0.81 m; upper 0.81 × 0.79 m | upper (her gun deck) 0.99 × 0.81; quarterdeck about 0.91 wide | measured (Ind §2.3.7) |

Until a point marked "to measure" is measured it is written as judgement in the note, never left
out silently.

### 3.3 The sills and the half-breadths

- **The gun deck** (the 64's lower, the razee's `upper`): thirteen ports a side at x +19.90,
  +16.58, +13.20, +9.78, +6.40, +3.02, −0.40, −4.18, −7.53, −10.94, −14.30, −17.71, −21.09 m
  (from forward; Ind §2.3.7, measured). Five sills are measured above WL1 (Ind's ports 13, 10, 7,
  4, 1 from aft: 6.03, 5.30, 5.02, 5.35, 6.09 ft). The other eight are interpolated (judgement)
  until measured on 1407F at the same scale. From forward the 64's run 1.84, 1.76, 1.69, 1.62,
  1.59, 1.56, **1.53**, 1.56, 1.60, 1.63, 1.71, 1.78, 1.86 m; the razee's 2.29, 2.21, 2.14, 2.06,
  2.03, 2.00, **1.98**, 2.01, 2.04, 2.07, 2.15, 2.22, 2.30 m (each + δT at its station; measured
  here). ZAZ2371 measures her midship sill at 1.96 m and her end ports at about 2.29 m (Ind
  §2.3.7): the derivation agrees within 0.02 m.
- **The 64's upper deck:** thirteen a side at +18.26 to −22.56 m (Ind §2.3.7, measured); the
  sill 3.63 m at midships (11 ft 11 in above WL1, not re-measured), 0.41 m above the deck; along
  the side the deck's sheer plus 0.41 m (judgement) until measured.
- **The razee's quarterdeck and forecastle:** six ports a side at −22.28, −19.05, −15.79, −12.86,
  −9.94, −6.86 m and three at +13.53, +16.67, +21.03 m (Ind §2.3.7, measured). The first four
  quarterdeck ports are the 64's upper-deck ports 1-4 within 0.8 ft, so the sills are the 64's
  upper-deck sills + δT (judgement) until measured on 2371.
- **The 64's quarterdeck and forecastle:** five a side at −17.83 to −5.85 m and one at +18.41 m
  (measured, tentative); sills the deck + 0.41 m (judgement).
- **Half-breadth at the sill.** At the lower midship sill (23.8 ft above the rabbet) the section
  is 21.52 ft moulded, plus 4½ in of plank: **6.67 m**, against half the extreme beam's 6.77 m;
  at the upper midship sill, **5.68 m** (measured here on Ind §2.3.2). The razee's ports are the
  same physical ports, with the same half-breadths. At the end ports the side is finer; B1
  measures each on 1407T's body plan at the port's station, the midship figure the fallback
  (which shuts the end ports a little early: the safe side).

### 3.4 What the sills give (heel alone, 70's rule `combat/shot.py:116-120`; measured here)

| Port | Sill | Shut at (half-breadth at the sill) | (half the beam) |
|---|---|---|---|
| The 64, lowest (No. 7) | 1.53 m | **10.6°** | 10.4° |
| The 64, end ports | 1.84-1.86 m | 13.4° | 13.2° |
| The 64 at Steel's 5 ft 6 in (Folio I, Ind §2.3.1) | 1.68 m | 11.9° | 11.7° |
| The razee, lowest | 1.98 m | **14.5°** | 14.3° |
| The razee, end ports | 2.30 m | 17.4° | 17.1° |
| The 64's upper deck, midships | 3.63 m | 35.8° | 29.4° |
| The frigate-36's gun deck, for comparison | 2.40 m (deck + `PORT_SILL_M`, judgement) | | 21.0° (map §3.3) |

Rounding the 64's lowest sill to 1.5 m would shut it at 10.32° (measured here). Under the owner's
rule the roll's amplitude adds to the heel. The 64's lower tier shuts where the *Bellona*'s
does on her own reported sill (10.6°, Bel §13.1 answer 5): a coincidence of two ships' figures,
not a source for either. **Plainly:** the razee's main battery, on measured sills, shuts at a
lower heel than the frigate-36's on judged ones; and the Gazette has her fighting her main deck
in a high sea with "the People on the Main Deck up to their Middles in Water" (Gazette 13972; Ind
§7.1 item 8), which the rule with the roll will often forbid. D12 (b) stands; her truths do not
pin that night.

### 3.5 B1's measuring tasks

On the held images (`owner-notes/indefatigable/rmg/`), by the research's method (registered
scale strips, a checker), with scratch scripts outside the repository; the figures go in, the
images never do:
1. the eight interpolated lower sills (1407F), and the upper-deck sills at the ends (1407T);
2. the half-breadth at each port's sill at its station (1407T's body plan), and the
   half-breadths at the water and at the rail by station, for `breadth_m`;
3. the stem above water to the stem head, the taffrail, the rails and the roundhouse (1407F,
   1280T, 1953 for the 64; 2371 for the razee);
4. the razee's quarterdeck and forecastle sills (2371);
5. the bowsprit's heel, and so its outboard length (1280T);
6. Steel's table IV, the 44's and the 38's mizen course and driver rows (the held page image), as
   the check on the razee's gaff mizen (§4.5);
7. the brace check of §4.2 against the measured channels.
8. **At stage B, the hull's shape** (`Build-Ships.md` §5.0, §5.7; the pilot, §2.6; after the lead's approval, stage 0H and SW-2b.1). For both files:
   - **`sections_m`** from Ind §2.3.2's WL1-WL5 by station (measured; no new reading; the razee's z each +0.44 m);
   - **`breadth_line_m`**: 1407T's main-breadth line, with its heights of breadth from 1407F (task 2 extended);
   - **`channel_wales_m`**: §3.2's channel wale;
   - **`form`**: the stern `square`, from 1407T's body plan and 1407F (2371 for the razee; Steel's 64 Folio LI on the cached leaf as a check; task 3 extended to the stern face):
     - its knuckle;
     - the transom's half-breadths at the taffrail and the knuckle;
     - the galleries' tiers and the lights, at their measured positions;
     - the head `figure`, `judged` until read;
   - **`marks`**;
   - **`head_m`**: the knee of the head as measured on 1407F, kept until then in the module's notes (item 9).

   Each measured port triple must lie within 0.05 m of the drawn side at its sill (`g.hull_form`). An end port still on the midship fallback (§3.3) is either measured on 1407T or stays on the fallback, its gap reported. No triple is taken from the drawing. Nothing of this at stage A.
9. **Before B5.1 draws her files** (`Build-Ships.md` §2.6 step 5): `stem_m` is the stem's fore
   edge up to the stem head and no further, and `rail_m` ends where her side ends (at the
   forecastle's fore end, abaft the stem head, if that is where it ends), as `Build-Ships.md`
   §5.1 has them. The working file's `rail_m` ends at x 24.63, 0.8 m abaft the stem's fore edge
   at the water (x 25.44), so its foremost point is not the stem head; the knee of the head
   goes to `head_m` at stage B (item 8).

---

## 4. The rig

### 4.1 Masts (Steel 1794 vol. I p. 49, the 64 column, read twice in Ind §3.1 and again here)

| | Main | Fore | Mizen | Source |
|---|---|---|---|---|
| x at the partners; rake | −2.78 m; 1.4° | +19.23 m; 0.3° | −16.33 m; 2.15° | measured (Ind §3.1) |
| Heel shoulder above K | 7.15 ft | 9.67 ft | 10.35 ft | measured (Ind §3.1) |
| Lower mast; head | 101-0; 14-0 | 89-7; 12-5 | 86-0; 9-7 | Steel p. 49; Steel's head rule (OCR l. 4695-4699) |
| The 64: head above her water | 26.63 m | 24.06 m | 22.94 m | measured here (the rake's cosine neglected, under 0.1 ft) |
| The 64: `height_m` above 3.22 | 23.41 | 20.84 | 19.72 | measured here |
| The razee: cut c (D19 (a)) | 6-7 | 6-3 | 6-9 | measured, judgement on the kit (Ind §3.3) |
| The razee: head above her water | 25.07 m | 22.60 m | 21.33 m | measured here |
| The razee: `height_m` above 1.39 (a) / 3.66 (c) | 23.68 / 21.41 | 21.21 / 18.94 | 19.94 / 17.67 | measured here |
| Topmast; hoist above the lower cap | 58-6; 13.56 m | 53-0; 12.36 m | 43-6; 10.34 m | Steel p. 49 less the lower head |
| Topgallant with its royal pole; above the topmast cap | 29-3; 6.93 m | 26-6; 6.28 m | 21-9; 5.34 m | Steel p. 49 less the topmast head |

Steel's 64 has no royal masts (the "Royal" rows read 0 0 on p. 49, read here): the royal sets on
the topgallant's pole. The module files the pole as a `royal_mast` stepped on the topgallant, as
the frigate-36 files hers, so that the engine's levels (`evolutions/trim.py:98-228`) see the royal
yard on its own spar; the note says it is one stick.

### 4.2 Yards, brace limits, rope

- **Yards**, Steel's (Ind §3.1): main 90-4, fore 79-6, crossjack 57-6; topsail yards 65-4, 57-6,
  43-3; topgallant 39-0, 34-6, 29-0; royal 32-0, 28-6, 21-0; the 64's mizen yard 77-0 (§4.4).
  The razee's the same (Ind §3.3: the kit; *Magnanime*'s 64's masts and yards, catalogue,
  self-contradictory).
- **Heights** by the frigate's rules (`gen_ships.py:1609-1614`): lower yards slung 2 ft below the
  hounds, topsail yards hoisted to the topmast hounds, and so on. The 64's main yard stands 60.9 ft
  above her datum; the razee's 61.7 ft above hers under (a) (measured here), its course's foot so
  12 ft above her quarterdeck as the 64's was above hers: the kit's "courses in proportion to the
  lowered sides" falls out of the cut.
- **Brace limits:** the frigate-36's (Fincham 1843 art. 102: main 64°, fore 62°, crossjack 60°,
  two degrees more a level aloft; `:1674-1700`), judgement for both. B1 checks them by the yard
  against the lee shrouds from the measured channels (the razee's lowered to 32.1 ft above K main
  and fore, 37.3 ft mizen, Ind §2.3.8; Rodd's remark that her channels differed from a regular
  frigate's, ADM 1/2408/84, catalogue), the method the 74 uses on Lavery's leads (Bel §13.5). The
  scratch 74 found these limits set her pointing (Bel §7.4). Open (§17).
- **Rope:** `FRIGATE_ROPE` scaled by √(her plain sail ÷ the frigate's 1,584 m²): 1.074 for the
  64 (1,826 m²), about 1.11 for the razee (about 1,960 m²) (measured here; judgement), so that a
  line's rating grows with the sail it works and truth 9's strain behaves as the frigate's. Steel's
  64 rigging table (vol. II, Quantities and Dimensions of Rigging) is a check where its OCR is
  legible. Spar ratings come from the rating pass.

### 4.3 Sails

- **Courses and topsails** from Steel's table IV, 64 column (Ind §5; areas at 22½ in a cloth,
  ±10%, judgement): main course 313 m², fore 219; main topsail 320, fore 247, mizen 147. They fit
  the spars: the main topsail's 17½ yards is the 52-54 ft from the lower yard to the topmast hounds
  (measured here).
- **Topgallants and royals: Steel's two tables disagree.** The main topgallant's 9 yards and the
  main royal's 7 yards make 48 ft of sail; between the main topsail yard hoisted and the pole's
  head the spars leave about 29 ft (the topmast head's 6 ft 6 in and the 22 ft 9 in of topgallant
  and pole above the cap; measured here). Both cannot hang there. **Plainly:** the module cuts them
  between their yards as the spars stand (the frigate's method, its widths Steel's cloths), and
  writes the table's cloths and areas (111 and 64 m² for the main) in the note. This lowers her
  light-air sail; put to the owner (§17).
- **Canvas** by Steel's ranges for a 64 (Ind §5), `FRIGATE_CANVAS`'s number where it lies in the
  range.
- **Reefs** by Steel (Ind §5): two in each course; four in the main topsail, three in the fore
  and mizen topsails (Steel's "three or four" in the main; the fore judgement); one in the mizen
  course a fifth up its mast leech. **Plainly:** the frigate-36 reefs her courses once
  (`frigate-36.yaml`, `reef_bands: 1`); she follows Steel for her rate. The engine reads any count
  (`orders/verbs.py:490-505`).
- **Royals** set flying (Steel 1794 vol. I p. 214, as the frigate-36's file cites it).
- **Staysails** between the masts by `between_the_masts(..., brig=False)` on her geometry,
  checked against Steel's cloths (main staysail 102 m², fore staysail 57, main topmast about 190,
  middle about 110, main topgallant about 90, mizen about 100, mizen topmast about 80; the
  four-sided ones ±25%).
- **Headsails:** fore staysail 57 m², fore topmast staysail 75, the jib 144 (Steel's "Jib
  Flying", set on the jib-boom). One jib-boom, no flying jib-boom: Steel's table has none, and Steel's
  "flying jib boom" rule is the jib-boom's (Ind §3.1, judgement). The engine's jib takes a stay;
  the note says Steel's was set flying on its traveller.
- **Studding sails** as the frigate-36's set: the fore lower, the fore and main topmast and
  topgallant (Steel's cloths: 102, 115, 135, 42, 52 m²; Ind §5); booms Steel's. Steel's table
  also lists a main lower studding sail against one pair of lower booms; the note records it.

### 4.4 The 64's mizen course (D9 (c), one rig: Bel §13.5)

Steel's sail (Ind §5): 14½ cloths at the head, 15½ at the foot, fore leech 9¼ yards, after
leech 17¼ yards; about 104 m². Measured here from those figures: the head runs 8.29 m aft and
rises 7.32 m (41°), 11.1 m along the yard. Its tack 3 ft above her quarterdeck at the mizen
(judgement; the quarterdeck there 5.47 m above the water), its throat at the truss 14.8 m and its
peak 22.2 m above the water (11.6 m and 18.9 m above her datum). One reef band a fifth up the mast
leech; canvas No. 2 (`FRIGATE_CANVAS["mizzen.spanker"]`, Steel's 'Mizen-course' No. 2 or 3).
The yard: 77 ft 0 in by 14 in (Steel p. 49), slung at its truss with lifts, its fore part bare
(Lavery 1985 I31-I32, the 74's; Steel's mizen course "bent to the mizen yard or gaff", Bel §5.6).

**Stage A** (`MIZEN_COURSE = "stand-in"`):
- spar `mizzen.yard`, class `gaff`, on `mizzen.mast`, `length_m` 11.1 (the sail's head: the
  yard's after part), `height_m` the truss (11.6 above her datum);
- sail `mizzen.course`, class `gaff`, roles `mast` and `gaff`, no boom: loose-footed; area,
  corners, centre and reef band as above, area checked against 104 m² ±10%;
- lines as the frigate's spanker less the outhaul: throat and peak halyards (standing for the
  yard's jeers), sheet, vangs;
- the storm mizen `in_place_of` it.

What holds already: the physics is a loose-footed fore-and-aft sail by its sheet, its lateral
offset from the gaff's length (`physics/sails.py:1342-1350`); it is the driver
(`after_gaff_sails`, `evolutions/scripts.py:553-581`): brailed up hove to, taken in at the gale's
third reef (`orders/storm.py:396-411`); its evolutions are the gaff's (set, brail up, furl,
reef, trim). What is wrong until stage B: the spar's class says "gaff"; the viewer draws it at a
fixed 35° with no bare fore part and no lifts, and its loose foot at 1.5 m above the datum
(`projection.js`, `LOOSE_FOOT_HEIGHT_M`), 0.8 m below her quarterdeck. Her note says
"PROVISIONAL, behind the lead's gate".

**Stage B** (`MIZEN_COURSE = "gated"`): the yard takes the gated spar class at its whole 77 ft,
slung at its truss with the fore part bare; the sail the gated class and roles; the lifts,
truss and brails as lines (Steel's 74 list: peak, middle, throat and foot brails, Bel §5.4); and
**Steel's driver** as an occasional, unbent sail: 22½ / 29 cloths, fore leech 9½, after leech 20
yards, about 198 m², set "occasionally ... to the mizen-yard or gaff, in light fair winds" (Steel,
OCR l. 13822; Ind §5) on a driver yard the length of the fore topgallant yard, 34 ft 6 in
(Steel p. 40). *Agamemnon* set one in March 1795 (Nicolas vol. 2 pp. 12-14).

*Settled by `Build-Ships.md` §1 (decision 29):* the yard's lines are the engine design's (its
§3.4: the jeers, the lifts, the vangs, the heel's bowlines as guys, one sheet, one tack). The
schema has no `truss` or `brail` line class (`schema.py:119-141`), and `take_in_lateen` brails
without one. Steel's driver is **left out** and named in her file's note: no engine path hangs a
sail from another sail's yard (the engine design §14 item 10). *Since asked for by the owner
(2026-10-28; `Build-Ships.md` §19.1 item 13):* the engine design's addendum (its §17) proposes
Steel's driver boomsail, bent on a boom in the mizen course's place and built at her stage B
behind its own flip, `DRIVER`. The owner chose it (2026-10-28; its §17.9 item 1); the lead
approved it (2026-10-29).

### 4.5 The razee's mizen (D20 (a))

Gaff 40 ft 10 in (12.45 m) and driver boom 65 ft 4 in (19.91 m) by Steel p. 40 on the 64's main
topsail yard (read on the page image in Ind §3.1). The boom overhangs the taffrail by 33-34 ft
(Ind §3.3; 29.4 ft as her taffrail was since measured); no source objects. The spanker cut by the frigate's rule on her gaff, boom and mast
(head 0.9 of the gaff, foot 0.9 of the boom, the gaff peaked 40°, `gen_ships.py:1841-1906`): about
**240 m²** (measured here: a hoist of 43.7 ft from boom to throat; judgement, ±10%), against the
frigate-36's 167 m² and Steel's 64 driver of about 198 m². B1 reads Steel's table IV rows for the
44's and the 38's mizen course as the check (§3.5 item 6). She lost "her Gaff and Mizen-Top-Mast"
on 20 April 1796 (Gazette 13887 p. 388), the only after-rig recorded on her. Her balance is tuned
with this sail (§16, risk 6).

### 4.6 The head, and the yards under the bowsprit (D8 (b))

- Bowsprit 60 ft 4 in, jib-boom 43 ft 9 in (Steel p. 49), steeved about 27° (±2°; Ind §3.1). Its
  outboard length from its heel measured on 1280T (§3.5 item 5), failing that a third inboard
  (the frigate's Luce rule, judgement). Its `x_m` at the stem head, +24.57 m.
- **The 64, stage B:** spritsail yard 57-6 × 12⅛ under the bowsprit; sprit-topsail yard 34-6 × 7
  on the jib-boom (Steel p. 49, read again here); the sprit course 102 m² (No. 2 or 3) and the
  sprit topsail 103 m² (No. 6 or 7) (Ind §5); aliases "spritsail" and "sprit topsail". The
  station along the bowsprit is the gated design's key. The data she offers it: the course is 7½
  yards deep, so its yard must stand about 24 ft or more above the water for its foot to clear
  (judgement on the steeve and the stem head), which puts the yard about halfway out. **Proposed
  (judgement):** both sails in "all sail" and the occasional sails, not in "plain sail", so that
  the far polar is unchanged at stage B; the gated design may rule otherwise.
- **The razee:** none, by D8 (b) as answered ("the 64's ... and the bilander's"). **Plainly:**
  Steel's 1794 table gives the 44 a spritsail yard of 52-0 and a sprit-topsail yard of 32-0, and
  the 38 53-0 and 32-9 (read here on p. 49's page image), and Steel's table IV carries sprit course
  and sprit topsail rows in the 44 and 38 columns (seen here). She kept the 64's spars by the only
  account. "Where the period shows them" may therefore include her: put to the owner. Either way
  she waits for the same gate, so stage A is unchanged.
  - **Answered (the owner, 2026-10-28):** she crosses the spritsail yard, as an occasional sail,
    and no sprit-topsail yard (the owner's reading of photographs of a modern model of her,
    secondary). Her yard is taken from the 64's spar (she kept the 64's spars), with the sprit
    course as the 64's, out of "plain sail".

### 4.7 Storm, occasional sails, groups and aliases

- **Storm canvas and occasional sails** as the frigate-36's pattern (`:2096-2301`; judgement):
  the storm mizen `in_place_of` `mizzen.course` (the 64) or `mizzen.spanker` (the razee); the
  ringtail on the razee only (she has the driver boom); the save-alls as the frigate's.
- **Groups**, the frigate-36's set (`frigate-36.yaml`, groups), with the names the engine reads
  (map §1.4): "plain sail" (courses, topsails, topgallants, fore topmast staysail, jib, and the
  mizen course or the spanker: the polar reads this group alone, `world/ships.py:364-372`),
  "topsails", "courses", "headsails", "jibs", "storm canvas", "storm staysails", "lying-to
  staysails" (the main staysail, Steel vol. II, as the frigate's), "occasional sails", "all
  sail", and the yard groups ("head yards", "after yards" and the rest).
- **Aliases** in the period's words: the 64 "mizen", "mizzen", "mizen course", "mizzen course" →
  `mizzen.course` and "mizen yard" → `mizzen.yard`; the razee the frigate's ("spanker",
  "driver", "mizzen"). **Mast ids `mizzen.`** (two z), so that the mizzen top answers her
  evolutions (`crew/hands.py:104-108`; map-engine §2.5).

---

## 5. The guns

### 5.1 The fits

| File | Fit | Guns, by place and number | Source |
|---|---|---|---|
| razee | **"as razeed 1795"** | gun deck 1-13: long 24. Quarterdeck 14-17: long 12 in the four foremost ports a side; 18-19: 42-pdr carronades in the two aftmost. Forecastle 20-21: long 12 in the after two; 22: 42-pdr carronade in the foremost | Winfield 1793-1817 p. 99; ZAZ2371's and ZAZ2398's tables (read); James vol. 1 p. 454. The establishment fills the ports exactly (six and three a side: ZAZ2375, measured). The split within each deck is judgement: a carronade's short recoil where the room is least, by the cabin and wheel aft and the catheads and bitts forward |
| razee | **"as carried 1796"** (default) | gun deck 1-13: long 24; quarterdeck 14-19 and forecastle 20-22: 42-pdr carronades; `chaser.bow.*`: two long 12s as bow chasers at about x +22.9 m, 4.25 m above the water (judgement: no bow port measured) | James vol. 1 p. 361; Troude vol. 3 p. 31; D30 (a) |
| 64 | **"ardent class 1784"** (default) | lower deck 1-13: long 24; upper deck 14-26: long 18; quarterdeck 27-31: long 9 in the five ports a side; forecastle 32: long 9 | ZAZ1407's gun table (read; written for *Stately* on the shared sheet); Winfield 1793-1817 p. 99; D17 (a) |
| 64 | **"ardent class 1794"** | as 1784, plus forecastle 33: 24-pdr carronades at about +14.6 m; roundhouse 34-36: 18-pdr carronades between −23 and −17 m (the roundhouse unmeasured; judgement) | Winfield 1793-1817 p. 99: the class's from 1794, never hers (Ind §4.1, judgement) |

- **James's statement** that none of the three razees went to sea with the establishment's long
  guns ("The Indefatigable mounted but 28", vol. 1 p. 454) goes in the 1795 fit's note.
  **Plainly:** fidelity argues that the fit she carried in every action read (1796 to 1805)
  should be her default; the brief names "as razeed 1795" and the decision sheet makes it the
  default, the owner able to say otherwise. Put to the owner (§17), who made "as carried 1796"
  the default (2026-10-28); §11.1's second way holds. What is set against the default fit (the
  filling party, the quarter bill, `Quarters.beat` at muster) is taken on the 1796 fit, and B1
  records the figures it gives where this document gives the 1795 fit's.
- The 1796 fit's note says she carried it in January 1797 (James vol. 2 pp. 16-17) and in 1805
  (vol. 3 p. 313; ADM 1/2408/84, catalogue).

### 5.2 Places, numbers and the deck

- **Built with `g.broadside_pair` and `g.chasers`**, then three keys reassigned on each gun dict
  (assigning an existing key keeps the key order, as `gen_ships.py:4397` does for the crew):
  `x_m` the port's measured x to 0.01 m, `height_m` the port's sill (§3.3) to 0.01 m, and `crew`
  (§5.3).
- **Numbered on across decks from forward**, as the frigate-36 numbers hers
  (`gen_ships.py:3836-3893`): the `(number, side)` rule and `pair_key` require it while no deck
  is read. **Plainly:** the period numbered each deck from No. 1 (Bel §7.2).
- **The deck word.** If stage 0 adds the inert `deck` gun key (§12.1 item 3), each gun carries
  it last: the 64's `lower`, `upper`, `quarterdeck`, `forecastle`, `roundhouse`; the razee's
  `upper`, `quarterdeck`, `forecastle`. If not, the deck is in the notes only. Renumbering from
  No. 1 on each deck waits for a deck-aware pair key, the 74's design to propose, and both
  files then take it alike.

### 5.3 Patterns, weights and crews

| Piece | Pattern and weight | Crew | Note |
|---|---|---|---|
| Long 24 | 9 ft 6 in, 49 cwt 2 qr (Adye p. 155) | 11 | D31 (a); the razee kept the 64's 24s |
| Long 18 | 9 ft 0 in, 40 cwt (Adye p. 155) | 9 | the 74's answer's pattern (Bel §13.1 answer 12; Lavery's Table 17 gives 40 cwt in 1761, via Bel §13.4); judgement for hers |
| Long 12 | 9 ft 6 in, 34 cwt (Adye p. 155) | 7 | D31 (a), the generator's pattern; Ind §6.4's lean to a short 12 for the chasers in the note |
| Long 9 | 7 ft 6 in, 24 cwt 2 qr (Adye p. 155) | 6 | the 74's pattern; judgement for hers |
| 42-pdr carronade | 4 ft 3½ in, 22 cwt 1 qr (Adye p. 72) | 4 | D31 (a) |
| 24-pdr carronade | 3 ft 7½ in, 13 cwt (Adye p. 72) | 4 | the 1794 fit |
| 18-pdr carronade | 3 ft 3 in, 9 cwt (Adye p. 72) | 4 | the 1794 fit |

Crews by Falconer 1780, QUARTERS (read (OCR) here, l. 14315-14340: men to a gun "when the ship is
well manned, so as to fight both sides at once occasionally"), and Douglas 1829 art. 136 for a
carronade (Ind §6.3); D31 (c). One side's guns, chasers included, take 197 men in the razee's 1795
fit, 193 in 1796, 296 in the 64's 1784 fit and 312 in 1794 (measured here). The weight enters only
the cycle and the dismount: a long gun's phases scale by its weight against 42 cwt, never above
one (`combat/guns.py:116-117, 565-570`), so her 24s serve at the 18s' pace.

**Plainly:** D31 (a) asked for new keys in `LONG_GUN_CWT` and `CARRONADE_CWT`
(`gen_ships.py:3577-3578`). The figures are D31 (a)'s, but they live in stage 0's
`tools/ships/period.py`, because Adye's 18-pdr carronade (9 cwt) and 9-pdr (24½) differ from the
shared table's 10 and 26 (from memory), which feed the eight files: one honest table for both
two-deckers, the shared ones untouched.

### 5.4 The magazine

- `fit_magazine` with `KINGS_ROUNDS` (60 round, 6 grape, 6 chain a gun; judgement after Lavery).
- **Charges** from the engine's shares (`ship/parts.py`, `charge_lb`), which give every calibre of
  her four fits to the ounce of the Regulations' Table No. 29 (Ind §6.4, read on the page image):
  24-pdr 8 lb, 18-pdr 6, 12-pdr 4, 9-pdr 3; carronades 42-pdr 3 lb 8 oz, 24-pdr 2 lb, 18-pdr 1 lb
  8 oz. Her `("magazine", fit, "charges")` notes in `b.armament_notes` are overridden after
  `armament()` to cite the Table as read; the shared UNVERIFIED note and the eight files are
  untouched. *Settled by `Build-Ships.md` §10:* the override holds only until the shared work's
  Table No. 29 step (SW-1) lands, when the shared note cites the table and serves her.
- **Exercise** (`exercise_charges`): the Regulations, the Gunner, Art. XXI: "one third of the
  number of the upper deck guns, in Ships of two or three decks; or one fourth for Ships of one
  deck" (read (OCR) here, l. 13118-13144). The razee one deck: `exercise_allowance(26)` = 6
  (`gen_ships.py:3656-3662`). The 64 two decks: 26 // 3 = **8**, by stage 0's
  `exercise_allowance(26, decks=2)` (`Build-Ships.md` §3.1 item 6), with her `exercise_charges`
  note overridden likewise from `period.py` (Eng §2.6).
- **Filling:** `filling_party(<default fit>)` gives the razee 11 and the 64 16, which are the
  Regulations' quarter gunners of the 294 and 491 columns (Ind §4.2): the period's figure twice
  over, and the note says so.

### 5.5 Broadside weight by 70's rule (measured here)

`far_ship` counts one side's broadside guns and **every** chaser (`combat/far.py:98-122`; the
rule at `:104-108`):

| | Broadside | Against the frigate-36's 421 lb |
|---|---|---|
| Razee, as razeed 1795 | 510 lb | 1.21 |
| Razee, as carried 1796 | 714 lb | 1.70 |
| The 64, ardent class 1784 | 600 lb | 1.43 |
| The 64, ardent class 1794 | 678 lb | 1.61 |

The frigate-36's 421 lb is her file as it stands, its quarterdeck marked INCORRECT
(`gen_ships.py:3819-3834`); Winfield 1793-1817 p. 143's establishment would give about 416 lb,
which the band of §14's truth holds. James gives the razee's 1796 broadside as 702 lb (vol. 1
p. 362), counting one 12; the rule counts both chasers, and her note gives both figures.

### 5.6 Later armaments, as data for the scenario editor

The degrees the sources allow: on the quarterdeck and forecastle's eighteen ports a long 12 or a
42-pdr carronade in any mix (the two fits are its ends); the two bow chasers present or not; the
gun deck's 26 × 24 fixed. In November 1805 Rodd asked to keep her carronades rather than the
9-pdrs lately ordered (ADM 1/2408/84, catalogue): an order whose count no source gives, so it is
a note, not a fit. The form the editor reads is the package's sub-types design (brief item 4).

---

## 6. The company, the marines, the quarter bill and the people files

### 6.1 The razee, 330 (D32 (a))

On the Regulations' 294 column (a 44; Ind §4.2, read on the page images), with 36 seamen over it
(James vol. 1 p. 454: 310 at first, then 330).

| Station | Count | Basis |
|---|---|---|
| Posts | 12 | the frigate-36's: captain, three lieutenants, master, boatswain, gunner, carpenter, purser, surgeon, sailmaker, master-at-arms (`data/people/frigate-36.yaml`) |
| Marines | 50 | the column's 7 officers and NCOs (two lieutenants, two serjeants, two corporals, a drummer) and about 43 privates (D32: the frigate-36's share, judgement) |
| Idlers | 30 | the column's rows by trade: carpenter's crew 7 (mate, five crew, caulker), sailmaker's crew 3 (mate, one crew, ropemaker), armourer 2, surgeon's mate 1, clerk 2 (clerk, schoolmaster), master-at-arms's party 2 (corporals), cook 1, steward 1; by judgement a cooper, a cook's mate as cook, a gunroom steward and 8 servants |
| Forecastle, fore top, main top, mizzen top, afterguard, waisters | 37, 31, 39, 18, 66, 47 (238) | the frigate-36's shares of her seamen (judgement); the column's petty officers and its 20 boys among them, the boys in the afterguard as landsmen (spec M3 §9 item 6) |

Ratings 0.30 able, 0.40 ordinary, 0.30 landsmen (the frigate-36's, judgement). The idlers' trades
are `IDLER_TRADES` (`schema.py:298-309`); stations plus posts make the complement
(`schema.py`, `_parse_crew`).

### 6.2 The 64, 491 (D17 (a))

On the 491 column (the Regulations p. 165; Winfield 1793-1817 p. 99).

| Station | Count | Basis |
|---|---|---|
| Posts | 14 | the frigate-36's with five lieutenants |
| Marines | 84 | the column's 8 (a captain, two lieutenants, two serjeants, two corporals, a drummer) and about 76 privates: judgement at the *Bellona*'s share in 1761, 97 marines in 567 (Lavery 1985 p. 17, Table 7, via Bel §13.4); the frigate-36's share would give 74. No establishment of private marines was found (Ind §10.8) |
| Idlers | 42 | the column's rows: carpenter's crew 11, sailmaker's crew 4, armourer 3, surgeon's mates 2, clerk 2, corporals 2, cook 2, steward 3; by judgement a cooper and 12 servants |
| The six seamen's stations | 54, 46, 58, 27, 96, 70 (351) | the frigate-36's shares (judgement) |

### 6.3 The people files (B1's, hand-written data)

The frigate-36's form (`data/people/frigate-36.yaml`): the posts in order; the drawn roles
(master's mates, a midshipman; the lieutenant and serjeant of marines drawn `{station: marines,
rating: marine}`, and for the 64 the captain of marines too); the harness's stations bound by
role (captain; officer of the watch the first lieutenant; master; second and third officers). The
outlines name no one: the files serve 1795 to 1816, and a scenario names Pellew, Rodd or Moore by
`people:` (`world/people.py:548-571`). Her own test file runs `tests/test_wardroom.py:42-57`'s
check on both files (*settled by `Build-Ships.md` §4.1*: no builder edits a shared test list).

### 6.4 The quarter bills (one per file, set against the default fit)

| | The razee (as razeed 1795) | The 64 (ardent class 1784) |
|---|---|---|
| Men at one side's guns, chasers included | 197, the 12 at the carronades from the marines first (`crew/quarters.py:437-460`) | 296; no carronades |
| Trimmers (forecastle, fore top, main top, mizzen top, afterguard) | 9, 12, 14, 7, 9: **51** | 10, 12, 14, 7, 10: **53** |
| Helm | 2 (the frigate-36's, judgement) | 2 |
| Powder | 0 (the idlers pass, as the frigate's) | 0 |
| Filling | 11 | 16 |
| Priority | sail before guns | sail before guns |
| Small arms | 26 | 39 |
| Boarders | 60 | 88 |
| The marines' division at the beat (judgement; measured by B1) | 38 | 84 |

- **Trimmers** are what the seamen leave when one side's guns (the marines taking the carronades
  first) and the wheel are manned: 238 − 185 − 2 = 51; 351 − 296 − 2 = 53; split by the
  frigate-36's trimmer shares (8, 10, 12, 6, 8 of 44). **Plainly:** the frigate-36's count is what
  her whole company less posts and idlers leaves (`gen_ships.py`, the forecastle trimmers' note:
  "the 44 hands the 264 leave"), which spends her marines at the guns. Falconer quarters the
  marines on the poop and forecastle or gangway, assisting at the great guns only in distant
  cannonading (QUARTERS, read (OCR) here), so the marines not at the carronades form their
  division. Eng §2.7's 66-gun bill with no marines in the divisions came from the generator's
  heavier crews.
- **Small arms:** the frigate-36's share of her seamen (20 of 182; judgement, as hers). Falconer's
  "men to the small arms" (5th rate 50; 4th rate of 60 guns 70; read (OCR) here, l. 14340-14362)
  run close to whole detachments of marines (Falconer's 3rd rate of 70 guns 80, against the *Bellona*'s
  97 marines in 1761), so they are the note's proxy for the whole party, marines and seamen.
- **Boarders:** a quarter of the seamen, the shared note's rule (`BOARDERS_NOTE`).
- **B1 measures `Quarters.beat` at muster** (`crew/quarters.py:155-242`) for each default fit and
  records whether every gun crew fills, how many marines go to the carronades, and the marines'
  division left. That answers Eng §8's item 6 on her own figures.

---

## 7. Ground tackle, boats, pumps, hold and stores

**Ground tackle** (D33 (a), both files; Steel 1794 vol. I, the anchor and cordage tables, read on
the page images: Ind §6.2), written through `b.ground_tackle(note, anchors, chain=False)`
(`gen_ships.py:676-698`), not `ground_tackle_for` (`:494-565`, two bowers by Luce's rule):

| Id | Kind | Name | Weight | Cable |
|---|---|---|---|---|
| `best_bower` | bower | the best bower | 57 cwt, 2,896 kg | 360 fathoms (three cables) of 21 in, 683 kN |
| `small_bower` | bower | the small bower | 57 cwt | 240 fathoms (two) of 21 in |
| `sheet` | sheet | the sheet anchor | 57 cwt | 120 fathoms of 21 in |
| `spare_anchor` | sheet | the spare anchor | 57 cwt | 120 fathoms of 21 in |
| `stream` | stream | the stream anchor | 15 cwt, 762 kg | 120 fathoms of 11½ in, 205 kN |
| `kedge` | kedge | the kedge | 7 cwt 2 qr, 381 kg | a hawser of 10½ in (half the bower cable, the house rule, judgement) |

Steel's seven bower cables laid as Lever's Channel service, "three Cables on the best Bower, two
on the small Bower" (Lever 1808 p. 67, as the generator cites it, `:472-473`); 120 fathoms a cable
(Falconer, CABLE). The spare is of kind `sheet`: the schema's kinds are four (`schema.py:181`),
and the moorings' "two bowers down" counts kind `bower` (`evolutions/scripts.py:6892`). The cables
rated by `rope_kn` (Luce ch. IV).

**The rest:**
- **Boats**, both files: the frigate-36's allowance (launch, barge, pinnace, two cutters, jolly
  boat) by Luce's rule on 160 ft, `boat_entries(160.1, True, ...)` (`:3378`): launch 33 ft
  (measured here, 2.6√160). Her own boats as a frigate were not found (Ind §10.11); Steel's 64
  list (Ind §6.1) and Lavery's six for a 74 of about 1800 (Bel §13.4) agree in kind.
- **Pumps:** two chain and two hand, `pump_entries(2, 2, ...)`; the well round the main mast
  (ZAZ2372, read).
- **Hold:** `hold_for(b, 1384, True, ...)`, 138 t.
- **Stores** (judgement): water at the frigate-36's 100 t for 264, by the complement, 125 t and
  186 t; provisions 120 days; cordage 750 and 1,100 fathoms likewise; shot plugs one a gun of the
  default fit, 44 and 64; spare spars and the sail room by the frigate's method on her own spars
  and sails; the ration `ration_entries("a King's ship")`, which `tests/test_stores.py:28` asks of
  every file.

---

## 8. Far description, vessel type, size class and rate (D16 (a))

**In her files**, `b.descriptions(...)` (`gen_ships.py:923-931`), as the brig writes hers:

| Key | rig | what | note |
|---|---|---|---|
| `sixty-four` | "a ship" | "a sixty-four, a ship of the line of two tiers of ports" | Winfield 1793-1817 p. 99; a third rate (Falconer, RATES) |
| `razee` | "a ship" | "a razee, a heavy frigate cut down from a sixty-four, one tier of twenty-four-pounders" | rated a 44 in Steel's List 1799-1802, the Navy List 1815-16 and James for 1805 (vol. 3 p. 311) |

The vessel type is the rig word "ship", as the frigate's. Both "what"s already carry a man-of-war
word ("ship of the line", "frigate": `world/captains.py:190-198`).

**Stage 0's registries** (shared with the 74):
- `DESCRIPTIONS` and `_DESCRIPTION_WORDS` (`world/ships.py:163-242`): the two keys with their
  files; words "a sixty-four", "sixty-four", "a 64", "a sixty-four gun ship" → `sixty-four`; "a
  razee", "razee", "a razee frigate", "a cut-down sixty-four" → `razee`. *Settled by
  `Build-Ships.md` §1 (decision 15):* these rows are written by B1 with her files (step 5),
  since a row names a file and the harbour offers every row to the scenario editor; the keyed
  rows below are stage 0's.
- `SIZE_RANK` (`captains.py:286-295`): `razee` 3, `sixty-four` 4.
- `_SIZE_WORDS` (`captains.py:296-305`), matched in order by `size_of_words` (the head before the
  first comma) and `size_rank_of` (the whole words): **`("razee", 3)` first, then
  `("sixty-four", 4)`**, then the existing entries. Otherwise "cut down from a sixty-four" ranks
  the razee 4, and "a ship" ranks the 64 a frigate. The 74's builder adds its own rank-4 words
  after "razee".
- `_MAN_OF_WAR_DESCRIPTIONS` (`world/regimes.py:158`; `world/squadrons.py:1520`) and the tuple at
  `squadrons.py:467`: both keys.
- `brains.role_of_vessel` (`world/brains.py:151-178`): both keys give "kings-ship", as "frigate"
  does.
- The three caches of eight (`world/ships.py:266, 297, 423`) raised to 32: results unchanged, the
  pace with ten or more files kept.

**"A ship of the line" is not one of her words.** Three assertions refuse those words today:
`tests/test_ships.py:99` (`description_key("a ship of the line") is None`; the generator map's
":101" is :99 at this head), `:188`, and `tests/test_world_orders.py:98`. The 74 is the type they
name; her builder moves them, old beside new. None of this ship's words appear in any existing
text (grep over `freesail/`, `data/`, `tests/`, `tools/`), so the new size words move no existing
ranking.

---

## 9. The polar: what B1 measures and records

**Measure** `polar_of` on both files (`world/ships.py:423-447`): the speeds at 8, 15 and 25 kn,
40° to 180°; `closest_deg`; `beat_deg(15)`; and the sailed figure at 90° in 15 kn (speed, heel,
helm). Record them in the tuning notes beside the frigate-36's (best 4.62, 8.19 and 11.63 kn) and
the scratch 74's (4.48, 7.83, 10.99) (Bel §7.4). Test both files in `tests/test_indefatigable.py`
in the form of `tests/test_ships.py`'s polar test (`:74-93`), with their own measured beam
reaches, ±0.5 (that file is not hers: `Build-Ships.md` §4.1).

**Targets**, bands on read sources (D24 (a); Ind §7.1, §7.3; each judgement):
- the razee faster than the 64 at every angle from her closest to 180° in 15 and 25 kn;
- the razee faster than the frigate-36 close-hauled (60-70°) and running large (120-150°) in
  15 kn: the *Virginie* chase, *Amazon* and *Concorde* run out of sight by evening (Osler p. 125;
  Gazette 13887 p. 388);
- the razee's best in 25 kn at or above 11.2 kn (the chase's 15-hour mean from lying to);
- the 64 not pinned against the frigate-36 (D24's "Plainly");
- `closest_deg` within a step of the frigate-36's (the same brace limits until §4.2's check).

**The risk, measured here from the figures:** plain sail per (displacement)^(2/3) is 10.9 for
the 64, about 12.7 for the razee (with her 240-m² spanker) and 13.5 for the frigate-36. So the
razee may not beat the frigate on the polar.

**The knobs, in this order:** `hull_speed_kn` within D24's 13-14.5; `clr_x_m` for the helm;
the brace limits, only with a source. Each tuned figure is recorded beside its start. **Realism,
not pacing:** if she is still not faster, B1 reports it with the figures and does not force it.
The frigate-36's Luce-ruled sail areas are the lead's file, not B1's.

---

## 10. The lee ports: what her files supply

Her files supply, per broadside gun, a sourced sill (`height_m`, equal to its port's triple),
and per port, in the profile, the half-breadth at the sill (§3.3). The wiring (one builder for
every ship, after 86's head; the lead's ruling) reads them. Her needs of that design:
- the half-breadth from the profile's port triple where a file has one, else half the beam
  (`combat/action.py:221`);
- the gate at the battery's choice of guns that fire (`Battery._fire`, `combat/guns.py:788-810`)
  and at running a lee gun out (`wants_work`, `:331-340`);
- the roll her own, read through the names the Hull keeps (`ship.extra["motion"]`, as
  `evolutions/runner.py:359` reads it; Design-OneWorld §2.2), never the followed ship's; no sea,
  no roll (`action.py:218`). *Settled by `Build-Ships.md` §7.1:* read as `Firer.roll_deg`,
  built from `world.motion` (a `PER_SHIP_FIELDS` name); the same `Motion` as
  `ship.extra["motion"]` (`core/world.py:655`).

Her shut heels are §3.4. Her lines in the package's lee-port truth come after the wiring (§14).

---

## 11. Where she sails

### 11.1 The 64 (D48 (a)) meets a named fit

**Found:** `make_scenario_world` takes the command line's ship file and the scenario's own
`Scenario`, fit included (`world/scenarios.py:738-748`), and `Ship(spec, fit)`
(`ship/graph.py:30-45`) calls `ArmamentSpec.fit`, which refuses a name the file lacks
(`ship/schema.py:589-594`). D48 (a) assumed the razee had one fit and her scenario named none. She
now has two, and a scenario of 1796 or 1805 would name "as carried 1796", which the 64 lacks.
Three ways:
1. the scenario names no fit, and the razee sails her default (the cost: the established long 12s
   she never carried, in any scenario after 1795);
2. the owner makes "as carried 1796" her default, and the scenario names none (§17 item 3);
3. a few lines in `make_scenario_world`: a command-line ship that lacks the scenario's fit takes
   her own default, with a line in the log. It changes behaviour only where today raises, and
   serves every file with named fits (the 74's included). It is world code outside the brief's
   list, so it is the lead's call.

Not B1's to decide; nothing of B1's waits on it.

### 11.2 The razee's scenario (D25, open): what each option needs

| | (a) Ushant, westerly (plan §3) | (b) off Brest, 22 Aug 1805 | (c) off the Lizard, 20 Apr 1796 (the lead's view) | (d) Brest approaches, 13-14 Jan 1797 |
|---|---|---|---|---|
| Chart | channel-west (exists) | channel-west | channel-west | channel-west to biscay-north (the Penmarks) |
| Date | 1795-99 or 1805-09 (laid up 1802-03: Winfield 1793-1817 p. 100) | 22 Aug 1805 | 20 Apr 1796 | 13 Jan 1797 |
| Weather pinned | a westerly no source gives (Ind §8.3) | N by E, moderate, hazy (James vol. 3 pp. 311-313) | SE, fresh (Clowes vol. 4 p. 497; Troude) | W, hard, rising sea (James vol. 2 pp. 12-13) |
| Her fit | 1795 for 1795 dates (no fit named: the 64 can sail it); else 1796 | as carried | as carried 1796 | as carried |
| Others | a frigate-36 under French colours standing out of the Iroise | the same, in the *Alexandre*'s place; *Niobe* optional as a frigate-36 | *Amazon* and *Concorde* (two frigate-36s, British, in company: 72's squadron); the *Virginie* a frigate-36 under French colours (James vol. 1 pp. 361-362) | *Amazon*; a French 74 (the *Bellerophon*'s file under French colours, or the later *Téméraire*-class file) |
| Start | open | 9 a.m., she ahead of the fleet | lying to under the Lizard, the stranger to seaward; the action after midnight | the chase from noon |
| Truths it feeds | none read | none read | Ind §7.1 items 5 and 6 (the chase; losing her after-sail) | items 7 and 8 |
| Against it | no account of the French standing out in a westerly | one account, a fleet sortie | Osler's wind "off the land" against SE in the logs | a 74 coming in, not a frigate standing out; needs a 74 file |

**Built now, common to all:** both files with both fits; the descriptions and roles; a test that
she sails under rules captains at seed 7 in a world with no named fit
(`make_world(7, <file>, Scenario())`), for both files. No scenario file before D25 is answered;
once it is, the scenario is one YAML file (B6's), on `first-action.yaml`'s shape.

---

## 12. Interfaces

### 12.1 What stage 0 lays for her (behaviour-free; each checked by the byte test and the fast tier)

1. **The hook:** in `gen_ships.py`'s `__main__` block (`:8479-8490`), after `smack(out)`:
   `sys.modules.setdefault("gen_ships", sys.modules[__name__])` and a loop over a
   `SHIP_MODULES` tuple calling `importlib.import_module(f"ships.{name}").build(out)`;
   `tools/ships/__init__.py` (docstring only). *Settled by `Build-Ships.md` §3.1:* the tuple
   names all four modules from stage 0, each a stub writing nothing until its builder fills it,
   so that no ship builder edits `gen_ships.py`. Each module's interface: `build(out_dir: str) ->
   None`, imported only there.
2. **`HullSpec.profile`** (`schema.py:345-356`, `_parse_hull` `:1245-1267`): optional, `None` by
   default, shape validated, unknown keys inside it refused; served by `ship_graph`
   (`api/queries.py:380-406`) only when present; optionally a `dump` regex keyed to `profile:`
   that sets each pair list on one line (§3.1).
3. **`deck` in `GUN_KEYS`** (`schema.py:202-214`), optional, from a tuple (`lower`, `middle`,
   `upper`, `quarterdeck`, `forecastle`, `roundhouse`), stored on `GunSpec` and read by nothing
   yet (the 74's design gives it its meaning; `pair_key` unchanged until then).
4. **`tools/ships/period.py`**, constants with their sources: Adye 1804's long guns by pounder and
   length (24: 9-6 49.5, 9-0 47.5, 10-0 52; 18: 9-6 42, 9-0 40; 12: 9-6 34; 9: 7-6 24.5) and
   carronades (42: 22.25; 32: 17 cwt 0 qr 14 lb; 24: 13.0; 18: 9.0); `FALCONER_CREW` {42: 15, 32:
   13, 24: 11, 18: 9, 12: 7, 9: 6, 6: 5, 4: 4, 3: 3} and `DOUGLAS_CARRONADE_CREW` 4; `STEEL_ANCHORS`
   by rate (the 64's here; the 74's by her design); `REGULATIONS_COLUMNS` (491, 343, 294).
5. **The registries** of §8: `DESCRIPTIONS`, `_DESCRIPTION_WORDS`, `SIZE_RANK`, `_SIZE_WORDS` in
   the order given, `_MAN_OF_WAR_DESCRIPTIONS` (two places and a tuple), `role_of_vessel`; the
   three caches raised from 8 to 32. *Settled by `Build-Ships.md` §3.1:* every row keyed by a
   description in stage 0; the `DESCRIPTIONS` and `_DESCRIPTION_WORDS` rows with her files (§8).
6. **The byte test**: her two files added to the tuple at `tests/test_ship_particulars.py:563-572`
   and to `test_period_names_resolve`'s parameters (`:470-552`). Proposed beside it: the test made
   two-way, comparing every `data/ships/*.yaml` and refusing a generated file that is not
   committed, so that builders no longer edit one tuple (a strengthening; the eight still
   compared). *Settled by `Build-Ships.md` §3.1 item 26:* the two-way form is taken in stage 0,
   so no tuple is edited (the list is at :563-572 at this head).

B1 proceeds without items 2 and 3 if they are late (§3.1, §5.2).

### 12.2 What the gated design must give her (stage B only; the contract for the lead's gate)

For the mizen course on its yard:
1. the spar class and its keys for a yard slung across the mast at its truss, its fore part bare:
   the whole 77-0 length, and where the truss sits along it (a key);
2. the sail's class and roles (the lateen cut at the mast, or a gaff sail hung from a yard), and
   whether `corners_m` is read;
3. **that the sail's lateral offset comes from the part abaft the truss**, as a gaff sail's comes
   from its gaff's length (`physics/sails.py:1342-1350`); else her balance moves at stage B;
4. whether the yard is braced: it is trimmed by its sheet, and `Spar.is_yard` braces a
   `lateen_yard` today (`ship/parts.py:243-248`; map-engine §3.3);
5. its lines (lifts, truss, brails, the sheet to the taffrail, the tack to the mast) and their
   classes; its evolutions' class keys and words (set, brail up, furl, reef, trim);
6. that it remains the driver for `after_gaff_sails` (`evolutions/scripts.py:553-581`) and the
   gale's reduction (`orders/storm.py:381-411`), or what replaces them;
7. `PEAK_COEFF` for any new class (`gen_ships.py:135`; the rating pass raises a KeyError without
   it, `:434-441`);
8. the class and roles of Steel's occasional driver at the yard's peak.

For the yards under the bowsprit:
9. a station along the bowsprit and the jib-boom (a file key or a rule);
10. how a bowsprit-rooted yard is kept out of `working_yards` and `_square_rigged`, or given its
    place, so that the fore yards stay her head yards and the stagger keeps its head (map-engine
    §3.1-3.2);
11. their heave-to and trim rules, their hands (no top for the bowsprit in `TOP_OF_MAST`), and
    whether they belong in "plain sail" (proposed not: §4.6);
12. the spritsail's cut in the viewer, its foot clear of the water.

Under the route "a gaff sail hung from a yard" the sail's class, curve, evolutions and
`after_gaff_sails` paths stay as stage A has them, and only the spar's class, length and truss
key change; under the lateen route her curve changes (lateen 1.15 at its peak against the gaff's
1.25: map-engine §1.2), so her polar moves. That choice is the gated design's, not this one's.

*Answered by the engine design and settled by `Build-Ships.md` §1:* the class is lateen with
`cut_at_mast: true`, read through `curve_class` with the gaff's curve and trim (items 1-2, 6-7;
the engine design §3.1-§3.5); the yard is not braced (item 4, §3.3); the truss's place along the
yard follows from the corners on the mast and `length_m`. **Item 3 is answered otherwise:** the
offset comes from 0.8√A, 8.16 m against Steel's foot of 8.86 m (§3.2 there), with no physics
change; the stand-in reads its 11.1-m head and overstates it, so the move at stage B is the
stand-in's error, shown old beside new. Item 5: no `truss` or `brail` lines (§3.4 there). Item 8:
Steel's driver is left out (§4.4 above); *chosen since by the owner (the engine design §17,
2026-10-28; its §17.9 item 1)*: class `lateen` cut at the mast with roles `yard`, `mast` and `boom`,
bent `in_place_of` the course, at her stage B behind `DRIVER`. Item 9: each yard's own `x_m`
and `height_m` are its station (§4.1 there). Items 10-12: §4.2, §4.3 and §6.2 there.

### 12.3 What the viewer builder (B5) is asked for

Her profile drawn from `hull.profile` (sides, sheer, wales, decks, rails; the ports from the
triples for 81 to build on); **a bowsprit rooted at the profile's stem head** where a file has a
profile (`projection.js:528-544` roots it at the datum today), which removes (a)'s one visible
cost; D18 (a) and (c) on the owner's first sheet at B5.1 (§2.2; `Build-Ships.md` §2.6 step 5); and, at stage B, the 64's mizen yard with its
bare fore part and lifts, her loose foot from `corners_m`, and the spritsail.

**The hull's shape** (`Build-Ships.md` §6, B5.1 and B5.6):
- **After stage A (B5.1):** her two files, the first with a profile, are drawn by B5.1's strips from their stage-0 profiles, with the measured `section_m` as it stands.
  - The side closes forward up `stem_m` to the stem head, where the bowsprit's heel is drawn, then to `rail_m`'s foremost point abaft it (§3.5 item 9).
  - The knee of the head is `head_m`, drawn by B5.6.
- **At stage B:** her shape keys (§3.5 item 8) are drawn by B5.6: her sections, her main breadth, the channel wale, the square stern with its galleries (two tiers on the 64, one on the razee, tentative), and her head (`head_m`).

---

## 13. File ownership, and the road

**B1 owns:** `tools/ships/indefatigable.py`; the two ship files (generated); the two people files;
her new tests in `tests/test_ship_particulars.py` and `tests/test_ships.py`; her truths in
`tests/test_known_truths.py`; her section of `docs/dev/TuningNotes.md`. **B1 never touches:** any
existing function or table of `tools/gen_ships.py`; `freesail/ship/schema.py`, `freesail/world/*`
(but her two rows in `world/ships.py`, below), `freesail/combat/*`, `client/*` (stage 0's, the gated builder's, the lee-port builder's, B5's);
the eight existing ship files; anything under `docs/agents/consent/`.

*Settled by `Build-Ships.md` §4.1:* her tests go in a new `tests/test_indefatigable.py`; her
truths are drafted and measured there under their numbers and moved into
`tests/test_known_truths.py` in Phase 5; her tuning notes are text in her branch's report, folded
in Phase 5. She also owns `tools/ships/mizen_yard.py` and `tools/ships/spritsail_yards.py` (at
stage B; the engine design §9.3), appends to `tools/ships/period.py` in her window, and writes
her two `DESCRIPTIONS` rows and their words in `freesail/world/ships.py` in her window (§8), the
one edit she makes under `freesail/`.

**The road.** Every step ends with `py tools/gen_ships.py <scratch>` from the tree root, a `cmp`
of the eight existing files against `data/ships/`, and `load_ship` on the new files. The fast tier
runs once at the end, with the slow tier of the files touched, by the suites' rules.

| Step | What | Proves | Waits on |
|---|---|---|---|
| 0 | Stage 0 (§12.1) | nothing changes (the eight files; the fast tier) | — |
| 1 | The measuring tasks (§3.5), scratch scripts outside the repository | the profile's and the sills' figures | — |
| 2 | `sixty_four()`; `write()` to the hull, profile, masts, yards, square sails, head and groups, with the stand-in mizen course | the 64's file loads, rates and polars | 0, 1 |
| 3 | `razeed()`; the razee's file through the same `write()` | the derivation's checks (§1.5) | 2 |
| 4 | Staysails, studding sails, storm and occasional canvas, aliases | every group the engine reads by name exists | 2 |
| 5 | Fits, magazine, quarter bill, crew, people files, stores, sail room, ground tackle, boats, pumps, hold, descriptions | `Quarters.beat` fills every crew of each default fit; the marines' division recorded | 2-4 |
| 6 | Tests and truths; both polars measured, tuned within bounds, recorded | §14 | 5 |
| 7 | **After the gate's builder merges:** `MIZEN_COURSE = "gated"`, `BOWSPRIT_YARDS = True`, `DRIVER = True` (Ext §17.8), the 64 regenerated, her polar and her rig clauses re-measured; the shape keys of both files (§3.5 item 8) | old beside new for the 64's rig, polar and balance; both files' bytes for the shape keys; the measured port triples within 0.05 m of the drawn side | the gated builder (B3.1, B3.2, B3.5 and B5's drawings); for the shape keys, the lead's approval of the hull's design, stage 0H and B8's SW-2b.1 (`Build-Ships.md` §2.6) |
| 8 | **Held for the owner's first test** of the whole ship, in the game, after the owner's sheets of her two files (D18 (a) and (c) at B5.1; the rest at B5.6) and their choices applied (`Build-Ships.md` §2.6) | — | 7; B5.6's drawing of her two files |

---

## 14. Tests and truths

**Her tests** (band form, the source in a comment, as `test_frigate_hull_is_an_amazon_class_frigate`,
`tests/test_ship_particulars.py:93-104`): her two hulls, profiles and sills against the measured
lines; her spars against Steel p. 49; her sails against table IV (±10%); her guns, fits, crews,
exercise and filling against Winfield, James, Adye, Falconer and the Regulations; her company,
posts and marines against the columns and the wardroom files; her ground tackle against Steel's
64; her descriptions and size ranks; her names resolving (`test_period_names_resolve`); her polars
in `tests/test_ships.py:74-93`'s form; the round-trip under rules captains at seed 7 (§11.2).

**Truths proposed** (by content; numbers among 7-185 to 7-199 assigned by the build document; the
last at this head is 7-184, `tests/test_known_truths.py:10426`). States, counts, ticks and bands
only, never a digest (decision 26). Written against the names the Hull keeps (`world.ship`,
`world.motion`, `world.sea`, `world.clock`; Design-OneWorld §2.2; `world/hulls.py:52-154`), never
an `isinstance(..., CrewedWorld)`.

*Numbered by `Build-Ships.md` §15:* 1 is 7-186, 2 is 7-187, 3 is 7-188; 4 is a clause of 7-187,
added only if the measure bears it out; 5 is a test of the scenario builder's, not a truth; and
the engine design's offered handling truth of the 64 is hers as 7-189, at stage B.

1. **Her particulars hold their sources, and the razee is the 64 cut down.** Both files load;
   beam 13.5 ± 0.1 m (44 ft 5 in); LWL 48.8 ± 0.3 m; draughts 6.33 and 5.88 ± 0.1 m; the razee's
   profile below the old upper deck the 64's raised 0.44 ± 0.02 m; the lowest gun-deck sill 1.53 ±
   0.03 m and 1.98 ± 0.03 m (ZAZ2371's 1.96); the lower masts' heads c lower (6 ft 3 in-6 ft 9 in)
   less the rise; 26 × 24 in every fit of both files; complements 491 and 330, marines 84 and 50;
   four bowers of 57 cwt. Pinned at once.
2. **The razee lighter, stiffer and faster than the 64 she was cut from** (the plan's).
   Displacement less by 238-244 tons of 35 cu ft; draught less by 0.44 ± 0.03 m; righting moment
   at 10° greater by at least 4% (8.4% by the files); heel at 90° in 15 kn under plain sail less;
   speed greater at every angle from her closest to 180° in 15 and 25 kn. The first four pinned at
   once; the speed clause after stage B (on the stand-in, said so, if the gate slips).
3. **Her broadside's weight and rate against the frigate-36's, by 70's rule** (the brief's).
   `far_ship(...).broadside_lb` 510 (1795) and 714 (1796) against 421: ratios 1.21 ± 0.05 and
   1.70 ± 0.05 (counts). The mean interval of a starboard 24-pdr over twenty minutes at a mark
   abeam, in truth 7-135's form (`_frigate_interval`, `tests/test_known_truths.py:8118`) on her
   file: within the frigate's bands, 90-125 s with the full company and 140-210 s with a quarter of
   each crew struck down. Pinned at once.
4. **The razee outsails the frigate-36 close-hauled and running large** (D24; the *Virginie*
   chase). Her polar speed at 60-70° and 120-150° in 15 kn above the frigate-36's, and her best in
   25 kn at or above 11.2 kn. **Pinned only if §9's measure bears it out after tuning within D24's
   bounds; else reported, not forced.**
5. **Her scenario round-trips and runs at seed 7, and the 64 sails it by the command line** (D48
   (a), under §11.1's way). Its behaviour waits on D25.

Her lee ports shutting (10.6° and 14.5°, heel alone) are one line of the package's lee-port truth,
after the wiring. Her files' byte identity is the package's generator truth.

---

## 15. Pins her work could move

- **None of the existing ships' passages.** The module writes new files only; no shared function
  or table changes; `frigate()` is untouched.
- **Lists, not pins:** none edited. The byte test is two-way from stage 0; her names, her
  wardroom check and her polar test run in `tests/test_indefatigable.py`, in the form of
  `test_period_names_resolve`, `tests/test_wardroom.py:42-57` and `tests/test_ships.py:74-93`
  (`Build-Ships.md` §3.1 item 26, §4.1).
- **The registries:** new keys and words only; no existing scenario, business table or test names
  "razee" or "sixty-four" (grep); `tests/test_ships.py:99` and its two kin stand.
- **The caches:** raised, results unchanged.
- **The harbour's glob** (`ui/harbour.py:382`) lists her files; its test checks membership only.
- **Within the package:** stage B moves `sixty-four.yaml`'s rig and her own truth clauses pinned
  after it, each old beside new, and both files' bytes for the hull's shape keys (no behaviour).
- **Not hers:** the lee-port wiring moves existing combat pins; it is the lee-port builder's.

---

## 16. Risks, ranked

1. **The gate slips past the merge.** The 64 then ships on the stand-in with no sprit yards,
   departing from D8 (b) and D9 (c); her rig clauses are pinned on the stand-in and re-measured
   at stage B. The razee is untouched.
2. **The razee may not outsail the frigate-36 on the polar** (10.9 / 12.7 / 13.5 m² of plain sail
   per t^(2/3), §9). Tuned within D24's bounds, never forced; reported if short.
3. **The stage-A mizen course's balance moves at stage B:** the engine design takes its lateral
   offset from 0.8√A, 8.16 m, where the stand-in reads its 11.1-m head (§12.2, as answered).
   Her polar keeps the gaff's curve. Shown old beside new.
4. **Byte identity on the build machine.** A last-bit difference in `math.tan` or `math.sin`
   between platforms could flip a value on a rounding boundary. The eight files show it is rare;
   the module rounds early, at the measured figures; the lead's suite on the build machine proves
   it.
5. **The quarter bills at 44-72 guns** (193-312 men at the guns) may leave a crew unfilled or the
   marines' division empty; B1 measures `Quarters.beat` and records it.
6. **The razee's spanker** (about 240 m² as first cut, 200 m² as filed, against the frigate's 167; a
   33-34 ft overhang, 29.4 ft as filed) moves
   her balance; `clr_x_m` is tuned with it and recorded as tuned.
7. **Unmeasured profile points** (stem head, rails, roundhouse, taffrail, end-port half-breadths,
   the upper and quarterdeck sills) until §3.5's tasks are done; each marked judgement meanwhile.
   The midship half-breadth shuts the end ports early.
8. **Steel's topgallants and royals** cut to the spars lower her light-air polar (§4.3).
9. **D18 (a)** draws the razee's bowsprit 2.3 m low until the viewer roots it from the profile;
   if B5 slips, the owner's screenshots show the generic convention.
10. **`_SIZE_WORDS` order:** if "razee" does not come first, the razee ranks 4 by her own words.
11. **D48 (a) breaks on a named fit** (§11.1) until the owner or the lead chooses a way.
12. **The lee ports once wired:** the 64's lower tier shuts at 10.6° less the roll, so
    close-hauled in a near-gale she loses her lee lower battery; the razee's main battery at 14.5°
    less the roll, against the Gazette's high sea of January 1797. Faithful to the rule, strong in
    any scenario she sails.
13. **The brace limits** are the frigate's until §4.2's check; a two-decker's lowered channels may
    brace otherwise and move `closest_deg`.
14. **The frigate-36's quarterdeck** is INCORRECT and kept by the owner's ruling; correcting it
    moves her broadside to about 416 lb, inside truth 3's band.
15. **A future top-level `ships` package on the path** would shadow `tools/ships/` (none today:
    map §1.10).

---

## 17. Open for the owner or the lead

**Answered by the owner (2026-10-28; Decisions, "The design's questions").** Item 3: the razee's
default fit is "as carried 1796", so §11.1's second way holds for her. Item 5: the razee crosses
a spritsail yard, out of plain sail, and no sprit-topsail yard; `head_yards()` writes the
spritsail yard for both files and the sprit-topsail yard for the 64 alone. Item 6: the spars
rule. Item 10: as proposed. Steel's driver (§4.4) stays left out unless the owner asks for it.
*The owner has since asked for it (`Build-Ships.md` §19.1 item 13); the engine design's §17
proposes Steel's driver boomsail, which the owner chose (2026-10-28; its §17.9 item 1).*

1. **D18 (owner):** (a) proposed, the razee's gun deck at 1.39 m; (c), her old upper deck at
   3.66 m, one figure away; decided on screenshots of both beside the 64 and the frigate-36 (§2.2).
   *Answered (2026-10-29): (c) for the razee* (`Build-Ships.md` §5.5): her datum her old upper
   deck, her working deck in the waist her gun deck (`Particulars.datum_line`); the 64 keeps (a).
   With it, her short roundhouse is in her profile (ZAZ2371's note of the December 1794 warrant;
   measured on ZAZ2371): her taffrail at 7.15 m, her stern lights and gallery under it. *Open, at
   her stage B:* her driver boom's jaws, 6 ft 6 in above her quarterdeck, now run under her
   roundhouse; raising them clear moves her spanker and her sailing figures, for the owner and
   the lead.
   *Her roundhouse's after face (the lead's question of 2026-10-29; answered by the owner,
   2026-10-30): plain, no lights.* "I looked again at the model, and at a painting I found of
   Indefatigable fighting Virginie ... both seem to agree that the roundhouse had no lights ...
   I think we can keep it plain." Judged from pictures, for the eye (`Build-Ships.md` §5.8), since
   ZAZ2371 is a side elevation and cannot show that face; her file's note says so at her stage B.
2. **D25 (owner):** the razee's scenario among (a)-(d) (§11.2); what is common is built now.
3. **The razee's default fit (owner):** "as razeed 1795" by the brief, or "as carried 1796", the
   guns of every action read (§5.1); it also settles §11.1's second way.
4. **D48 against a named fit (lead):** the three ways of §11.1; the third is world code outside
   the brief's list.
5. **The razee's yards under the bowsprit (owner):** Steel 1794 p. 49 gives the 44 and the 38
   both yards; D8 (b) as answered named only the 64's and the bilander's (§4.6).
6. **Steel's topgallants and royals (owner):** Steel's spar and sail tables disagree above the topmast
   caps; proposed that the spars rule and the sails be cut to them (§4.3).
7. **Stage 0's shape (lead, at the synthesis):** the profile format (§3.1), the `deck` key and its
   words (§12.1 item 3, with the 74's design), `tools/ships/period.py`, the two-way byte test, the
   caches.
8. **The gate's contract (lead):** §12.2's twelve items, for the one engine-extension document;
   whether the spritsail sets belong in "plain sail".
9. **File and fit names (lead or owner):** `sixty-four.yaml`, `razee-44.yaml`; "ardent class
   1784", "ardent class 1794", "as razeed 1795", "as carried 1796".
10. **Judgement figures for the owner's eye:** the 64's private marines (76, the *Bellona*'s share;
    74 by the frigate's); the 64's 18-pdr at 40 cwt (the 74's) or 42 (the generator's); the split
    of the 1795 establishment's 12s and carronades within each deck; the small-arms men at the
    frigate's share; the 64's exercise allowance read as a third of her upper-deck guns.
11. **Brace limits** for a two-decker and the razee's lowered channels (§4.2).

**Answered by the owner (2026-10-29), on stage A's open items** (the staysails, the spanker, the
razee against the frigate-36, the brace limits):
- **The staysails between the masts:** "Agreed" to the proposal: the main, middle, mizen and
  mizen topmast staysails cut to Steel's table IV figures for a 64 (§4.3's bands), and the mizen
  topgallant staysail, which his 64 column has not, left out. Done at the refinement of stage A
  (§3.5 item 9's step).
- **The razee's spanker:** kept at 218 m², the frigate's rule on her spars, within 8% of
  Steel's driver for a 38 (202 m²) (the owner: "meant 218"). *Since (the lead's ruling of
  2026-10-30, the owner told):* 218 m² cannot stand with her boom clear of her taffrail, and it
  is 200 m² at the least that clears, within the owner's 8% (191 at 6 ft of head room, 195 at 5).
- **The razee against the frigate-36** (7-187's clause 4, 0.13-0.26 kn short in 15 kn): "We'll
  rely on tuning for this, the razee could be right and the frigate-36 too fast, or the razee
  too slow and the frigate-36 right." Left to tuning of both ships against the period's
  accounts, neither presumed the one at fault; reported, not forced.
- **Brace limits (item 11):** the frigate's limits kept, on the reading that the lee topmast
  backstays were eased when the yards were braced sharp up ("Reasonable").
- **Her topgallants and royals by Steel p. 42's long pole-heads** (put with the 74's design,
  Design-Ship-Bellerophon.md §17.0): "Agreed", for both ships. The pole-heads read as rising
  above the listed topgallant masts, so her topgallants and royals are cut to Steel's sail table
  within the spars so read (the owner's spars rule kept). Taken at her stage B, her file
  regenerated, her polar and light-air figures old beside new.

---

## 18. Found on the way

1. **Steel 1794 p. 49 gives the 44 and the 38 a spritsail yard and a sprit-topsail yard** (52-0
   and 32-0; 53-0 and 32-9; read here on the page image), and Steel's table IV carries sprit course
   and sprit topsail rows in those columns. The decision sheet read the razee as having none in the
   period.
2. **70's rule counts both chasers.** The razee's 1796 broadside by her file is 714 lb (James's
   702 counts one 12), and the frigate-36's is 421 lb. The buildability draft's 690 and 403 left
   the chasers out; the fidelity draft's 64 at 870 lb was an error (600 lb).
3. **The derivation checks against an independent measure:** the razee's midship sill from the
   64's plus the rise (1.98 m) and ZAZ2371's measured 1.96 m agree within 0.02 m.
4. **"A ship of the line" is refused in three places** (`tests/test_ships.py:99`, `:188`;
   `tests/test_world_orders.py:98`); the generator map's ":101" is :99.
5. **D48 (a) cannot carry a named fit** (`world/scenarios.py:738-748`, `ship/graph.py:30-45`,
   `ship/schema.py:589-594`).
6. **Two copies of the generator fail only when mixed**, and then at `dump` with yaml's
   `RepresenterError`, not with a message naming the cause (measured here).
7. **`filling_party` gives exactly the Regulations' quarter gunners** for both her columns (16 and
   11).
8. **Adye p. 72 gives the 18-pdr carronade 9 cwt and p. 155 the 9-pdr 24½,** where the shared
   table has 10 and 26 (from memory); the existing files are the lead's.
9. **The half-breadth at the 64's lower midship sill is 6.67 m** (the sill 23.8 ft above the
   rabbet), not the 6.64 m read at 24.6 ft.
10. **Falconer's small-arms men by rate run close to the marines' detachments** (Falconer's 3rd rate of
    70 guns 80; the *Bellona*'s 97 marines in 1761), so they are not seamen beyond the marines
    (judgement).
11. **Steel's table IV topgallant and royal depths do not fit Steel's spar table's topgallant mast and
    pole** for the 64 (§4.3); the 74's note left the same question open (Bel §10 item 5).
12. **The fidelity draft's razee displacement (1,880 t)** lay below the razee's own measured band
    (1,900-1,955 t); taking the 64 at 2,170 t keeps both files inside their bands with the
    measured slice between them.
13. **The frigate-36's trimmers spend her marines at the guns** (the 44 hands "the 264 leave"),
    which leaves her no marines' division at quarters; a question for the frigate's own file, not
    this ship's.
